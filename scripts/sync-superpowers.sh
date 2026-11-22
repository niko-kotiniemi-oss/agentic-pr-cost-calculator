#!/usr/bin/env bash
# Re-materialise vendor/superpowers from the upstream sha in UPSTREAM.lock, each
# file with the bytes and the mode that the pinned commit's objects give it.
#
# THE SCRIPT IS THE DEFINITION AND CI RUNS IT. `--check` re-syncs into a
# temporary tree and diffs; any difference fails, so a hand-edit to a vendored
# file is a red build rather than a silent fork. That is why no vendored file
# may be edited: the edit cannot survive the next sync and cannot hide.
set -euo pipefail

# A variable that names a repository, such as a GIT_DIR that a person or a tool
# exports, would have git fetch into, read and write that repository rather than
# the sync's own and this one. Git lists them, and the sync drops each but the two
# that carry the person's configuration, as git does when it works in another
# repository.
for variable in $(git rev-parse --local-env-vars); do
  case "$variable" in
    GIT_CONFIG_PARAMETERS | GIT_CONFIG_COUNT) ;;
    *) unset "$variable" ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT}/vendor/superpowers"
LOCK="${DEST}/UPSTREAM.lock"

# A link in the copy, or one that leads to it, would have the refresh delete and
# write files outside the copy, and the check compare them, so the sync stops on
# each before it reads or writes anything.
links() {
  if [ -L "${ROOT}/vendor" ]; then
    printf '%s\0' "${ROOT}/vendor"
  elif [ -e "$DEST" ] || [ -L "$DEST" ]; then
    find "$DEST" -type l -print0
  fi
}
linked=0
while IFS= read -r -d '' link; do
  printf 'sync: %q is a link, which the sync does not follow\n' "${link#"${ROOT}/"}" >&2
  linked=1
done < <(links)
[ "$linked" = 0 ] || exit 1

# The vendored subset, and the only paths this script touches: the plugin
# manifest, the skills, the two hook scripts (not upstream's hook registrations,
# since .claude/settings.json registers the dispatcher itself) and the licence.
# tests/test_repository.py holds this list equal to UPSTREAM.lock's
# vendored_paths.
PATHS=(.claude-plugin skills hooks/run-hook.cmd hooks/session-start LICENSE)

# The lock as git would stage it: a carriage return before a line feed is part of
# the line's end, so that a lock that an editor saved with Windows line endings
# reads as one saved with line feeds.
LOCK_TEXT="$(cat "$LOCK"; printf x)"
LOCK_TEXT=${LOCK_TEXT%x}
LOCK_TEXT=${LOCK_TEXT//$'\r\n'/$'\n'}
read_lock() { printf '%s' "$LOCK_TEXT" | sed -n "s/^$1=//p"; }

REPO="$(read_lock repo)"
SHA="$(read_lock sha)"
[ -n "$REPO" ] && [ -n "$SHA" ] || { echo "sync: UPSTREAM.lock is missing repo= or sha=" >&2; exit 2; }
TAG="$(read_lock tag)"
[ -n "$TAG" ] || { echo "sync: UPSTREAM.lock is missing tag=" >&2; exit 2; }
# Tests point this at a local fixture so that they never use the network.
URL="${SYNC_REMOTE_BASE:-https://github.com}/${REPO}.git"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

# A fetch by commit id takes any commit upstream serves, including those of its
# open pull requests that no release contains. So the lock's tag must name the
# lock's commit: an annotated tag through its peeled line, a lightweight one
# directly.
tagged_commit() {
  local refs
  refs="$(git ls-remote "$URL" "refs/tags/${TAG}" "refs/tags/${TAG}^{}")"
  printf '%s\n' "$refs" | awk -v plain="refs/tags/${TAG}" -v peeled="refs/tags/${TAG}^{}" '
    $2 == plain { direct = $1 } $2 == peeled { commit = $1 }
    END { print (commit != "" ? commit : direct) }'
}
named="$(tagged_commit)"
if [ "$named" != "$SHA" ]; then
  echo "sync: tag ${TAG} of ${REPO} names ${named:-nothing}, not ${SHA}" >&2
  exit 1
fi

# Each vendored file is written from the pinned commit's objects, not through
# `git archive` or a checkout, whose output follows the person's core.autocrlf, a
# .git/info/attributes that git's template gives a new repository, and upstream's
# own attributes.
materialise() {
  local into="$1" path entry mode oid perm
  git init -q "${work}/src"
  git -C "${work}/src" fetch -q --depth 1 "$URL" "$SHA"
  for path in "${PATHS[@]}"; do
    git -C "${work}/src" cat-file -e "${SHA}:${path}" 2>/dev/null || {
      echo "sync: ${REPO}@${SHA} gives no ${path}" >&2
      return 1
    }
  done
  git -C "${work}/src" ls-tree -r -z "$SHA" -- "${PATHS[@]}" >"${work}/listing"
  mkdir -p "$into"
  while IFS= read -r -d '' entry; do
    read -r mode _ oid <<<"${entry%%$'\t'*}"
    path="${entry#*$'\t'}"
    # Only files: a link could point a vendored path anywhere, and a submodule
    # gives no file at all.
    case "$mode" in
      100644) perm=644 ;;
      100755) perm=755 ;;
      *)
        printf 'sync: %s gives %q the mode %s, which the sync does not copy\n' \
          "${REPO}@${SHA}" "$path" "$mode" >&2
        return 1
        ;;
    esac
    # Git's objects can name a path that no checkout writes: one through `.` or
    # `..`, or through a folder that git, Windows or macOS opens as `.git`, such as
    # `.git` in any case, `.git.`, `git~1` or `.git` with a character that HFS+
    # ignores. Git's own checkout refuses each with the protections of NTFS and
    # HFS+ on, so the sync asks git, in an index of its own, before it writes one.
    if ! git -C "${work}/src" -c core.protectNTFS=true -c core.protectHFS=true \
      update-index --add --cacheinfo "$mode" "$oid" "$path" 2>/dev/null; then
      printf 'sync: %s gives the path %q, which the sync does not write\n' \
        "${REPO}@${SHA}" "$path" >&2
      return 1
    fi
    case "$path" in */*) mkdir -p "${into}/${path%/*}" ;; esac
    git -C "${work}/src" cat-file blob "$oid" >"${into}/${path}"
    chmod "$perm" "${into}/${path}"
  done <"${work}/listing"
}

# The mode that git's index gives a path of this repository, in `staged`, or
# nothing where the index holds none. A failure of git, such as outside a
# repository, stops the check rather than leave it to compare no mode.
staged_mode() {
  local record=""
  git -C "$ROOT" ls-files --stage -z -- ":(literal)$1" >"${work}/staged"
  IFS= read -r -d '' record <"${work}/staged" || true
  staged="${record%% *}"
}

if [ "${1:-}" = "--check" ]; then
  probe="${work}/probe"
  materialise "$probe"
  # The lock at the root is ours, not upstream's, so it is copied into the tree
  # built here, and the comparison leaves out no other path, whatever its name.
  cp "$LOCK" "${probe}/UPSTREAM.lock"
  differs=0
  diff -r "$probe" "$DEST" >"${work}/report" 2>&1 || differs=1
  # Each file's mode, which `diff` does not compare, as git's index gives it,
  # which is what a commit holds on any system, and a carriage return that the
  # pinned commit's file does not hold, as a clone made with core.autocrlf set to
  # true before the repository's attributes keeps one, which the way back writes
  # again.
  returns=0
  while IFS= read -r -d '' entry; do
    read -r mode _ <<<"${entry%%$'\t'*}"
    path="vendor/superpowers/${entry#*$'\t'}"
    staged_mode "$path"
    if [ -n "$staged" ] && [ "$staged" != "$mode" ]; then
      printf "sync: git's index gives %q the mode %s, not the mode %s %s\n" \
        "$path" "$staged" "$mode" "that the pinned commit gives it" >>"${work}/report"
      differs=1
    fi
    if [ -f "${ROOT}/${path}" ] && LC_ALL=C grep -q $'\r' "${ROOT}/${path}" &&
      ! LC_ALL=C grep -q $'\r' "${probe}/${entry#*$'\t'}"; then
      printf "sync: %q holds a carriage return that the pinned commit's file does not\n" \
        "$path" >>"${work}/report"
      returns=1
    fi
  done <"${work}/listing"
  if [ "$differs" = 0 ]; then
    echo "sync: vendor/superpowers matches ${REPO}@${SHA}"
  else
    echo "sync: vendor/superpowers DIFFERS from ${REPO}@${SHA}" >&2
    cat "${work}/report" >&2
    if [ "$returns" = 1 ]; then
      echo "sync: to write the pinned commit's files again, run" \
        "scripts/sync-superpowers.sh, or delete vendor/superpowers and check it" \
        "out again" >&2
    fi
    exit 1
  fi
else
  rm -rf "${PATHS[@]/#/${DEST}/}"
  materialise "$DEST"
  echo "sync: vendor/superpowers re-materialised from ${REPO}@${SHA}"
fi
