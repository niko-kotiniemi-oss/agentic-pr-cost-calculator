#!/usr/bin/env bash
# Re-materialise vendor/superpowers from the upstream sha in UPSTREAM.lock, each
# file with the bytes and the mode that the pinned commit's objects give it.
#
# THE SCRIPT IS THE DEFINITION AND CI RUNS IT. `--check` re-syncs into a
# temporary tree and diffs; any difference fails, so a hand-edit to a vendored
# file is a red build rather than a silent fork. That is why no vendored file
# may be edited: the edit cannot survive the next sync and cannot hide.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT}/vendor/superpowers"
LOCK="${DEST}/UPSTREAM.lock"

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
  local into="$1" work path entry mode oid perm
  work="$(mktemp -d)"
  trap 'rm -rf "$work"' RETURN
  git init -q "$work/src"
  git -C "$work/src" fetch -q --depth 1 "$URL" "$SHA"
  for path in "${PATHS[@]}"; do
    git -C "$work/src" cat-file -e "${SHA}:${path}" 2>/dev/null || {
      echo "sync: ${REPO}@${SHA} gives no ${path}" >&2
      return 1
    }
  done
  git -C "$work/src" ls-tree -r -z "$SHA" -- "${PATHS[@]}" >"$work/listing"
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
    # Git's objects can name a path through `.`, `..` or a folder named `.git` in
    # any case, which no checkout writes and `git archive` refused as invalid.
    case "/${path}/" in
      */./* | */../* | */[.][gG][iI][tT]/*)
        printf 'sync: %s gives the path %q, which the sync does not write\n' \
          "${REPO}@${SHA}" "$path" >&2
        return 1
        ;;
    esac
    case "$path" in */*) mkdir -p "${into}/${path%/*}" ;; esac
    git -C "$work/src" cat-file blob "$oid" >"${into}/${path}"
    chmod "$perm" "${into}/${path}"
  done <"$work/listing"
}

if [ "${1:-}" = "--check" ]; then
  probe="$(mktemp -d)"
  trap 'rm -rf "$probe"' EXIT
  materialise "$probe"
  # The lock at the root is ours, not upstream's, so it is copied into the tree
  # built here, and the comparison leaves out no other path, whatever its name.
  cp "$LOCK" "${probe}/UPSTREAM.lock"
  if diff -r "$probe" "$DEST" >/dev/null 2>&1; then
    echo "sync: vendor/superpowers matches ${REPO}@${SHA}"
  else
    echo "sync: vendor/superpowers DIFFERS from ${REPO}@${SHA}" >&2
    diff -r "$probe" "$DEST" >&2 || true
    exit 1
  fi
else
  rm -rf "${PATHS[@]/#/${DEST}/}"
  materialise "$DEST"
  echo "sync: vendor/superpowers re-materialised from ${REPO}@${SHA}"
fi
