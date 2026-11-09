#!/usr/bin/env bash
# The one definition of "OpenSpec passes". CI and a person at a terminal run this
# same script.
#
#   1. The CLI is the version package-lock.json pins.
#   2. The generated openspec-* skills are exactly what that CLI writes.
#   3. Every spec and change validates under --strict, and there was something
#      to validate.
#   4. That CLI lists and shows every spec and change, and each requirement, as
#      tests/test_spec_form.py reads them, and there was something to compare.
#
# Exit 1 when a property does not hold, 2 when the check cannot run.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

OPENSPEC=node_modules/.bin/openspec
if [ ! -x "$OPENSPEC" ]; then
  echo "verify-openspec: no OpenSpec CLI at $OPENSPEC; run npm ci --ignore-scripts" >&2
  exit 2
fi

# OpenSpec's global state lives in a scratch directory for this run alone, so a
# user's own settings cannot change what is generated. Usage reporting is off.
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT
export XDG_CONFIG_HOME="$SCRATCH/config" XDG_DATA_HOME="$SCRATCH/data"
export DO_NOT_TRACK=1 OPENSPEC_TELEMETRY=0 OPENSPEC_NO_UPDATE_CHECK=1

pinned=$(python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["packages"]["node_modules/@fission-ai/openspec"]["version"])' package-lock.json)
installed=$("$OPENSPEC" --version 2>/dev/null) || { echo "verify-openspec: $OPENSPEC does not run here" >&2; exit 2; }
if [ "$installed" != "$pinned" ]; then
  echo "verify-openspec: installed $installed, package-lock.json pins $pinned" >&2
  exit 2
fi

SKILLS=':(glob).claude/skills/openspec-*/**'
if [ -z "$(git ls-files -- ':(glob).claude/skills/openspec-*/SKILL.md')" ]; then
  echo "verify-openspec: git tracks no generated OpenSpec skill" >&2
  exit 1
fi

echo "--- the generated skills are what the pinned CLI writes ---"
# The configuration is declared, not inferred: on a fresh config `update` infers
# the profile from the skills it finds, so a deleted skill would go unnoticed.
"$OPENSPEC" config set profile custom >/dev/null
"$OPENSPEC" config set delivery skills >/dev/null
"$OPENSPEC" config set workflows '["explore","propose","apply","update","sync","verify","archive"]' >/dev/null
# Each skill is emptied to one empty SKILL.md first, so every byte has to come
# back from the CLI: `update --force` rewrites but never deletes, and with no
# SKILL.md at all it writes nothing.
for skill in .claude/skills/openspec-*; do
  if [ -L "$skill" ] || [ ! -d "$skill" ]; then
    echo "verify-openspec: $skill is a link or not a directory" >&2
    exit 1
  fi
done
for skill in .claude/skills/openspec-*; do
  find "$skill" -mindepth 1 -delete
  : >"$skill/SKILL.md"
done
"$OPENSPEC" update --force >/dev/null
# Compared with the index, so a staged tree is checked as it will be committed:
# a line counts when its second column is not blank (the work tree differs from
# the index), which also catches untracked (??) and ignored (!!) files.
drift=$(git status --porcelain --untracked-files=all --ignored -- "$SKILLS" | awk 'substr($0, 2, 1) != " "')
if [ -n "$drift" ]; then
  echo "verify-openspec: the generated skills differ from what the pinned CLI writes:" >&2
  echo "$drift" >&2
  exit 1
fi

echo "--- every spec and change validates, strictly ---"
report="$SCRATCH/validate.json"
if "$OPENSPEC" validate --all --strict --json >"$report"; then status=0; else status=$?; fi
if [ "$status" -ne 0 ]; then
  "$OPENSPEC" validate --all --strict >&2 || true
  exit "$status"
fi
count=$(python3 -c 'import json, sys; print(len(json.load(open(sys.argv[1])).get("items") or []))' "$report")
if [ "$count" -eq 0 ]; then
  echo "verify-openspec: validation passed having examined nothing" >&2
  exit 1
fi
echo "verify-openspec: $count item(s) valid"

echo "--- the CLI reads every spec as the test of the specs' form reads it ---"
python3 scripts/spec_form.py "$OPENSPEC"
