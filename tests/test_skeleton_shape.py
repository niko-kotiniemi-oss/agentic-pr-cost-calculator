"""The walking skeleton's shape recorder, task 1.35 of `add-pr-cost-calculator`.

Transcripts here are written by the test, with values planted in every field. R236 in
`project-standards` and DR-244.
"""

from __future__ import annotations

import json
import random
import string
import subprocess
import sys
from pathlib import Path
from typing import Any

from test_repository import ROOT
from test_skeleton_checks import shape_problems

SHAPE = ROOT / "skeleton" / "shape.py"
IDENTIFIER = "toolu" + "_01PLANTEDIDENTIFIER"
PLANTED = [
    "planted-uuid",
    "planted-session",
    "/planted/working/directory",
    "planted-model",
    "planted-text",
    "planted-tool-input",
    "planted-tool-result",
    IDENTIFIER,
    "planted-command",
]


def planted_lines() -> list[dict[str, Any]]:
    return [
        {
            "type": "assistant",
            "uuid": "planted-uuid",
            "sessionId": "planted-session",
            "cwd": "/planted/working/directory",
            "isSidechain": False,
            "wireToolInputs": {IDENTIFIER: {"command": "planted-command"}},
            "toolUseResult": {"stdout": "planted-tool-result"},
            "message": {
                "id": "msg" + "_01PLANTEDMESSAGE",
                "model": "planted-model",
                "stop_reason": None,
                "content": [
                    {"type": "text", "text": "planted-text"},
                    {"type": "tool_use", "id": IDENTIFIER, "input": {"x": "planted-tool-input"}},
                ],
                "usage": {"input_tokens": 12345, "output_tokens": 678, "server_tool_use": {"a": 9}},
            },
        },
        {"type": "user", "message": {"role": "user", "content": "planted-text"}, "uuid": "u"},
        {"type": "summary", "summary": "planted-text", "leafUuid": "planted-uuid"},
    ]


def write_transcript(path: Path, lines: list[Any], tail: str = "") -> Path:
    path.write_text("".join(json.dumps(line) + "\n" for line in lines) + tail)
    return path


def record(*args: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", str(SHAPE), *map(str, args)], capture_output=True, text=True
    )


def test_the_shape_holds_names_and_types_at_the_kept_levels_only(tmp_path: Path) -> None:
    transcript = write_transcript(tmp_path / "main.jsonl", planted_lines(), '{"halfWritten": 1}')
    extra = write_transcript(tmp_path / "agent.jsonl", ["not an object", 3], "{not json\n")
    out = tmp_path / "transcript-shape.json"
    done = record(transcript, extra, out)
    assert done.returncode == 0, done.stderr
    assert done.stdout == ""
    text = out.read_text()
    for planted in PLANTED:
        assert planted not in text and planted not in done.stderr
    entries = json.loads(text)
    paths = {(entry["path"], entry["type"]) for entry in entries}
    assert ("wireToolInputs", "object") in paths
    assert ("toolUseResult", "object") in paths
    assert ("message.content", "array") in paths
    assert ("message.content", "string") in paths
    assert ("message.stop_reason", "null") in paths
    assert ("message.usage.input_tokens", "number") in paths
    assert ("message.usage.server_tool_use", "object") in paths
    assert ("isSidechain", "boolean") in paths
    assert ("halfWritten", "number") not in paths
    assert not any(
        path.startswith(("message.content.", "wireToolInputs.", "toolUseResult."))
        for path, _ in paths
    )
    assert entries == sorted(entries, key=lambda e: (e["path"], e["type"]))
    assert shape_problems(out, "recorded shape") == []


def test_it_writes_nothing_when_its_own_check_fails(tmp_path: Path) -> None:
    lines = [*planted_lines(), {IDENTIFIER: 1}, {"x" * 41: 1}, {"a-b": 1}]
    for number, line in enumerate(lines[-3:]):
        transcript = write_transcript(tmp_path / f"t{number}.jsonl", [lines[0], line])
        out = tmp_path / f"shape{number}.json"
        done = record(transcript, out)
        assert done.returncode == 1
        assert not out.exists()
        assert done.stdout == "" and IDENTIFIER not in done.stderr


def test_a_shape_of_nothing_is_not_written(tmp_path: Path) -> None:
    transcript = write_transcript(tmp_path / "empty.jsonl", [])
    out = tmp_path / "shape.json"
    assert record(transcript, out).returncode == 1
    assert not out.exists()


def test_it_needs_a_transcript_and_an_output(tmp_path: Path) -> None:
    assert record(tmp_path / "only.json").returncode == 2


def random_value(rng: random.Random, depth: int) -> Any:
    kind = rng.choice(
        ["str", "int", "float", "bool", "none", "list", "dict"] if depth < 3 else ["str"]
    )
    if kind == "str":
        return "v-" + "".join(rng.choices(string.ascii_letters + string.digits, k=12))
    if kind == "int":
        return rng.randint(10**6, 10**9)
    if kind == "float":
        return rng.random() + 7
    if kind == "bool":
        return rng.random() < 0.5
    if kind == "none":
        return None
    if kind == "list":
        return [random_value(rng, depth + 1) for _ in range(rng.randint(0, 3))]
    names = ["message", "usage", "content", "kk" + str(rng.randint(0, 9))]
    return {rng.choice(names): random_value(rng, depth + 1) for _ in range(rng.randint(0, 4))}


def all_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [v for item in value.values() for v in all_values(item)]
    if isinstance(value, list):
        return [v for item in value for v in all_values(item)]
    return (
        [str(value)] if isinstance(value, str | int | float) and not isinstance(value, bool) else []
    )


def test_no_value_of_any_random_transcript_reaches_the_shape(tmp_path: Path) -> None:
    # A seeded search over random transcripts stands in for a property-based test until the
    # build brings Hypothesis (design decision 8).
    rng = random.Random(20261116)
    for round_number in range(40):
        lines = [
            {"message": random_value(rng, 0), "kk": random_value(rng, 1)}
            if rng.random() < 0.7
            else random_value(rng, 0)
            for _ in range(rng.randint(1, 6))
        ]
        transcript = write_transcript(tmp_path / f"r{round_number}.jsonl", lines)
        out = tmp_path / f"r{round_number}.json"
        done = record(transcript, out)
        if done.returncode == 1:
            assert not out.exists()
            continue
        text = out.read_text()
        for value in all_values(lines):
            assert value not in text, value
        assert shape_problems(out, "random") == []
