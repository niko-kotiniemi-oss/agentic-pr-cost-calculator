#!/usr/bin/env bash
# Re-materialise vendor/superpowers from the upstream sha in UPSTREAM.lock, each
# file with the bytes and the mode that the pinned commit's objects give it.
#
# THE SCRIPT IS THE DEFINITION AND CI RUNS IT. `--check` re-syncs into a
# temporary tree and diffs; any difference fails, so a hand-edit to a vendored
# file is a red build rather than a silent fork. That is why no vendored file
# may be edited: the edit cannot survive the next sync and cannot hide.
#
# `--check-commit COMMIT` is the base commit's check of a pull request's tree
# (R299, R317): this copy of the script, from the base's checkout, compares the
# copy that COMMIT holds, read from git's objects alone, with the commit that
# COMMIT's own lock pins, and fails where that lock gives another `repo=` or
# `vendored_paths=` than the base's. It fetches from GitHub whatever
# SYNC_REMOTE_BASE says.
set -euo pipefail

MODE="${1:-}"
COMMIT=""
if [ "$MODE" = "--check-commit" ]; then
  COMMIT="${2:-}"
  [ -n "$COMMIT" ] || { echo "sync: --check-commit needs a commit" >&2; exit 2; }
elif [ -n "$MODE" ] && [ "$MODE" != "--check" ]; then
  echo "sync: $MODE is not an option of the sync" >&2
  exit 2
fi

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
# Git lists none of the variables that change how it reads a path, such as
# GIT_LITERAL_PATHSPECS, which would have the check read no mode from git's
# index, so the sync drops each, and git reads every path as the name it is.
unset GIT_LITERAL_PATHSPECS GIT_GLOB_PATHSPECS GIT_NOGLOB_PATHSPECS GIT_ICASE_PATHSPECS

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

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

if [ -n "$COMMIT" ]; then
  # The pull request's tree, read from git's objects: no checkout, so no
  # attribute, filter or submodule of its own runs, and a link or a gitlink
  # where the copy lies stops the check rather than be followed.
  commit_id="$(git -C "$ROOT" rev-parse --verify --quiet --end-of-options "${COMMIT}^{commit}")" || {
    printf 'sync: the commit %q cannot be read\n' "$COMMIT" >&2
    exit 1
  }
  git -C "$ROOT" ls-tree -z "$commit_id" -- vendor vendor/superpowers >"${work}/top"
  bad=0
  while IFS= read -r -d '' entry; do
    read -r mode _ <<<"${entry%%$'\t'*}"
    path="${entry#*$'\t'}"
    if [ "$mode" != 040000 ]; then
      printf 'sync: the pull request gives %s the mode %s, which the check does not read\n' \
        "$path" "$mode" >&2
      bad=1
    fi
  done <"${work}/top"
  [ "$bad" = 0 ] || exit 1
  git -C "$ROOT" ls-tree -r -z "$commit_id" -- vendor/superpowers >"${work}/theirs"
  while IFS= read -r -d '' entry; do
    read -r mode _ <<<"${entry%%$'\t'*}"
    path="${entry#*$'\t'}"
    case "$mode" in
      100644 | 100755) ;;
      *)
        printf 'sync: the pull request gives %s the mode %s, which the check does not read\n' \
          "$path" "$mode" >&2
        bad=1
        ;;
    esac
  done <"${work}/theirs"
  [ "$bad" = 0 ] || exit 1
  BASE_REPO="$(read_lock repo)"
  BASE_PATHS="$(read_lock vendored_paths)"
  THEIR_LOCK="${work}/their.lock"
  git -C "$ROOT" cat-file blob "${commit_id}:vendor/superpowers/UPSTREAM.lock" >"$THEIR_LOCK" || {
    echo "sync: the pull request's tree holds no vendor/superpowers/UPSTREAM.lock" >&2
    exit 1
  }
  LOCK="$THEIR_LOCK"
  LOCK_TEXT="$(cat "$LOCK"; printf x)"
  LOCK_TEXT=${LOCK_TEXT%x}
  LOCK_TEXT=${LOCK_TEXT//$'\r\n'/$'\n'}
  for key in repo vendored_paths; do
    case "$key" in repo) base="$BASE_REPO" ;; *) base="$BASE_PATHS" ;; esac
    theirs="$(read_lock "$key")"
    if [ "$theirs" != "$base" ]; then
      printf "sync: the pull request's lock gives %s=%s, not the base's %s=%s\n" \
        "$key" "$theirs" "$key" "$base" >&2
      bad=1
    fi
  done
  [ "$bad" = 0 ] || exit 1
fi

REPO="$(read_lock repo)"
SHA="$(read_lock sha)"
[ -n "$REPO" ] && [ -n "$SHA" ] || { echo "sync: UPSTREAM.lock is missing repo= or sha=" >&2; exit 2; }
TAG="$(read_lock tag)"
[ -n "$TAG" ] || { echo "sync: UPSTREAM.lock is missing tag=" >&2; exit 2; }
# Tests point this at a local fixture so that they never use the network. The
# check of a pull request's tree reads it not, since it is the base's check.
if [ -n "$COMMIT" ]; then
  URL="https://github.com/${REPO}.git"
else
  URL="${SYNC_REMOTE_BASE:-https://github.com}/${REPO}.git"
fi

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
  # In the object format of upstream's commit ids, SHA-1's, whatever format git
  # gives a new repository, as GIT_DEFAULT_HASH can: git fetches nothing from a
  # repository of another format.
  git init -q --object-format=sha1 "${work}/src"
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
    # Git commits a carriage return before a line feed as a line feed, so that
    # the copy would no longer match the pinned commit, and the test of
    # characters refuses one that git keeps, so no vendored file may hold one
    # (R269, R275).
    if LC_ALL=C grep -q $'\r' "${into}/${path}"; then
      printf 'sync: %s gives %q a carriage return, which no vendored file may hold\n' \
        "${REPO}@${SHA}" "$path" >&2
      return 1
    fi
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

if [ -n "$COMMIT" ]; then
  probe="${work}/probe"
  materialise "$probe"
  cp "$LOCK" "${probe}/UPSTREAM.lock"
  # The pull request's copy, each file written from its blob with the mode that
  # its tree gives it, and each path first put to git, in an index of its own,
  # with the protections of NTFS and HFS+ on, as the copy from upstream is.
  theirs="${work}/theirs-tree"
  mkdir -p "$theirs"
  declare -A their_mode=()
  while IFS= read -r -d '' entry; do
    read -r mode _ oid <<<"${entry%%$'\t'*}"
    path="${entry#*$'\t'}"
    path="${path#vendor/superpowers/}"
    if ! GIT_INDEX_FILE="${work}/protect-index" git -C "$ROOT" -c core.protectNTFS=true \
      -c core.protectHFS=true update-index --add --cacheinfo "$mode" "$oid" "$path" 2>/dev/null; then
      printf 'sync: the pull request gives the path %q, which the check does not write\n' \
        "vendor/superpowers/$path" >&2
      exit 1
    fi
    case "$path" in */*) mkdir -p "${theirs}/${path%/*}" ;; esac
    git -C "$ROOT" cat-file blob "$oid" >"${theirs}/${path}"
    their_mode["$path"]="$mode"
  done <"${work}/theirs"
  differs=0
  diff -r "$probe" "$theirs" >"${work}/report" 2>&1 || differs=1
  while IFS= read -r -d '' entry; do
    read -r mode _ <<<"${entry%%$'\t'*}"
    path="${entry#*$'\t'}"
    given="${their_mode[$path]:-}"
    if [ -n "$given" ] && [ "$given" != "$mode" ]; then
      printf "sync: the pull request gives %q the mode %s, not the mode %s %s\n" \
        "vendor/superpowers/$path" "$given" "$mode" "that the pinned commit gives it" \
        >>"${work}/report"
      differs=1
    fi
  done <"${work}/listing"
  if [ "$differs" = 0 ]; then
    echo "sync: the pull request's vendor/superpowers matches ${REPO}@${SHA}"
  else
    echo "sync: the pull request's vendor/superpowers DIFFERS from ${REPO}@${SHA}" >&2
    cat "${work}/report" >&2
    exit 1
  fi
elif [ "$MODE" = "--check" ]; then
  probe="${work}/probe"
  materialise "$probe"
  # The lock at the root is ours, not upstream's, so it is copied into the tree
  # built here, and the comparison leaves out no other path, whatever its name.
  cp "$LOCK" "${probe}/UPSTREAM.lock"
  differs=0
  diff -r "$probe" "$DEST" >"${work}/report" 2>&1 || differs=1
  # Each file's mode, which `diff` does not compare, as git's index gives it,
  # which is what a commit holds on any system, and a carriage return, which no
  # pinned file holds, as a clone made with core.autocrlf set to true before the
  # repository's attributes keeps one, which the way back writes again.
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
    if [ -f "${ROOT}/${path}" ] && LC_ALL=C grep -q $'\r' "${ROOT}/${path}"; then
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
  # The refresh writes the whole copy apart, and replaces the vendored paths
  # only then, so that one that stops, on what the pinned commit gives or on a
  # fetch that fails, leaves the vendored copy as it was. It names each path
  # whole, as it moves it, and in no replacement of a substitution, where bash
  # 5.2 reads each `&`, as a clone below a folder named `R&D` holds one.
  copy="${work}/copy"
  materialise "$copy"
  for path in "${PATHS[@]}"; do
    rm -rf "${DEST}/${path}"
    case "$path" in */*) mkdir -p "${DEST}/${path%/*}" ;; esac
    mv "${copy}/${path}" "${DEST}/${path}"
  done
  echo "sync: vendor/superpowers re-materialised from ${REPO}@${SHA}"
fi
