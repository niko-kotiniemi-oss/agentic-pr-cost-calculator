#!/usr/bin/env python3
# The walking skeleton of the agentic PR cost calculator: not the tool or a release.
# Records the shape of the run's transcripts: the field names at a line's top level, in its
# `message` and in `message.usage`, each with its JSON type, and every other object and array as
# its type alone, with no value (R236, DR-244). It checks its own output and writes nothing when
# the check fails. Run in the scratch repository: `shape.py <transcript>... <out.json>`.
"""Record the value-free shape of transcripts, for the walking skeleton's run."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

NAME = re.compile(r"[A-Za-z0-9_]{1,40}")
IDENTIFIER_FORM = re.compile(r"[a-z]+_(?=[A-Za-z0-9]*[A-Z0-9])[A-Za-z0-9]{8,}")
# The only names kept at a line's top level: the fields that the design and the assumptions read.
# Any other top-level name, such as one of the host's own features, is counted and left out, and
# the check in `tests/test_skeleton_checks.py` holds the same list (R236).
TOP_LEVEL_NAMES = frozenset(
    {
        "agentId",
        "cwd",
        "gitBranch",
        "isMeta",
        "isSidechain",
        "leafUuid",
        "message",
        "parentUuid",
        "requestId",
        "sessionId",
        "summary",
        "timestamp",
        "toolUseResult",
        "type",
        "userType",
        "uuid",
        "version",
    }
)


def type_name(value: Any) -> str:
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int | float):
        return "number"
    return "null" if value is None else "string"


def entries_of(line: Any, left_out: set[str]) -> set[tuple[str, str]]:
    """The paths and types of one line, at the kept levels only; other top-level names go to
    `left_out`, to be counted."""
    found: set[tuple[str, str]] = set()
    if not isinstance(line, dict):
        return found
    for name, value in line.items():
        if name in TOP_LEVEL_NAMES:
            found.add((name, type_name(value)))
        else:
            left_out.add(name)
    message = line.get("message")
    if isinstance(message, dict):
        for name, value in message.items():
            found.add((f"message.{name}", type_name(value)))
        usage = message.get("usage")
        if isinstance(usage, dict):
            found |= {(f"message.usage.{name}", type_name(value)) for name, value in usage.items()}
    return found


def failing(entries: set[tuple[str, str]]) -> int:
    """How many entries give a name that R236 does not allow."""
    return sum(
        any(not NAME.fullmatch(n) or IDENTIFIER_FORM.fullmatch(n) for n in path.split("."))
        for path, _ in entries
    )


def main(argv: list[str]) -> int:
    # An output named like a transcript is refused, so that one is never written over.
    if len(argv) < 2 or argv[-1].endswith(".jsonl"):
        print("usage: shape.py <transcript>... <out.json>", file=sys.stderr)
        return 2
    *sources, target = (Path(arg) for arg in argv)
    entries: set[tuple[str, str]] = set()
    left_out: set[str] = set()
    for source in sources:
        for raw in source.read_bytes().split(b"\n")[:-1]:
            try:
                entries |= entries_of(json.loads(raw.decode("utf-8")), left_out)
            except ValueError:
                continue
    bad = failing(entries)
    if bad or not entries:
        print(
            f"shape.py: {bad} names fail the check, of {len(entries)}; nothing written",
            file=sys.stderr,
        )
        return 1
    shape = [{"path": path, "type": kind} for path, kind in sorted(entries)]
    target.write_text(json.dumps(shape, indent=2) + "\n", encoding="utf-8")
    print(f"shape.py: {len(left_out)} other top-level names left out", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
