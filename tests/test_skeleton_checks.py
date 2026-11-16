"""The checks that hold the walking skeleton to what it may be, task 1.31 of
`add-pr-cost-calculator`.

R234: nothing here registers the skeleton. R236: the kept transcript shape holds no values.
R237: the skeleton's workflow can do no more than post its comment. R242: the skeleton says
what it is. Each check is a function of what it reads, so that a test can plant the defect it
exists for, and a test runs it on this repository.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pytest
import yaml
from test_repository import ROOT, tracked_files, tracked_texts

SKELETON = ROOT / "skeleton"
TASKS = ROOT / "openspec/changes/add-pr-cost-calculator/tasks.md"
README = ROOT / "README.md"

# R234: the folders whose files could register, install or run the skeleton here.
REGISTERING_FOLDERS = (".claude/", ".claude-plugin/", ".github/")


def registration_problems(files: Iterable[tuple[str, str]]) -> list[str]:
    """Each file under a registering folder whose path or text names the skeleton, in any case."""
    return [
        f"{path} names the walking skeleton where it could register it (R234)"
        for path, text in files
        if path.startswith(REGISTERING_FOLDERS) and "skeleton" in (path + "\n" + text).lower()
    ]


# R236: the kept shape.
SHAPE_PREFIX = "transcript-shape"
TYPE_NAMES = frozenset({"object", "array", "string", "number", "boolean", "null"})
NAME = re.compile(r"[A-Za-z0-9_]{1,40}")
IDENTIFIER_FORM = re.compile(r"[a-z]+_(?=[A-Za-z0-9]*[A-Z0-9])[A-Za-z0-9]{8,}")
# The only names that a kept shape gives at a line's top level, the same list as the shape
# recorder's: the fields that the design and the assumptions read, and no name of the host's own.
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


def entry_problem(entry: object) -> str | None:
    """Why one entry of a kept shape is not a path of names at the kept levels and a type name."""
    if not isinstance(entry, dict) or set(entry) != {"path", "type"}:
        return "is not a path and a type alone"
    path, kind = entry["path"], entry["type"]
    if not isinstance(path, str) or not isinstance(kind, str) or kind not in TYPE_NAMES:
        return "is not a path and a JSON type name"
    names = path.split(".")
    for name in names:
        if not NAME.fullmatch(name):
            return f"has a name that is not 1 to 40 letters, digits and underscores: {name!r}"
        if IDENTIFIER_FORM.fullmatch(name):
            return f"has a name of an identifier's form: {name!r}"
    if len(names) == 1 and names[0] not in TOP_LEVEL_NAMES:
        return f"gives a top-level name that the recorder's list does not name: {names[0]!r}"
    kept_levels = len(names) == 1 or (
        names[0] == "message" and (len(names) == 2 or (len(names) == 3 and names[1] == "usage"))
    )
    return None if kept_levels else "gives a name below an object whose names are not kept"


def shape_problems(path: Path, label: str) -> list[str]:
    """The problems of one kept shape, each naming the file and the entry."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        return [f"{label}: not JSON ({type(error).__name__})"]
    if not isinstance(data, list) or not data:
        return [f"{label}: not a non-empty list of entries, so it examined nothing"]
    problems = []
    for number, entry in enumerate(data):
        why = entry_problem(entry)
        if why:
            problems.append(f"{label}: entry {number} {why} (R236)")
    return problems


def kept_shapes(paths: Iterable[str]) -> list[str]:
    """The tracked files under `tests/` whose name begins with the shape's prefix."""
    return [p for p in paths if p.startswith("tests/") and Path(p).name.startswith(SHAPE_PREFIX)]


def missing_shape_problems(tasks_text: str, shapes: list[str]) -> list[str]:
    """Once task 1.36 is ticked, a kept shape must exist."""
    ticked = re.search(r"^- \[x\] 1\.36 ", tasks_text, re.M | re.I)
    if ticked and not shapes:
        return ["task 1.36 is ticked, but the transcript shape is missing (R236)"]
    return []


# R237: the skeleton's workflow.
# Each checkout's ref and the folder it goes to, and the one command that reads them.
EVENT_REFS = {"${{ github.event.before }}": "before", "${{ github.event.after }}": "after"}
CHECKOUT_INPUTS = frozenset({"ref", "path", "persist-credentials"})
REPORT_COMMAND = "python3 -I after/skeleton/report.py before after"
FULL_COMMIT = re.compile(r"[0-9a-f]{40}")


def checkout_problems(where: str, step: dict[str, Any]) -> list[str]:
    """Why a step that uses an action is not `actions/checkout` as R237 allows it."""
    action, _, ref = str(step["uses"]).partition("@")
    if action != "actions/checkout":
        return [f"{where} uses another action: {action}"]
    problems = [] if FULL_COMMIT.fullmatch(ref) else [f"{where} pins no full commit"]
    given = step.get("with") or {}
    if given.get("persist-credentials") is not False:
        problems.append(f"{where} keeps its credentials")
    if given.get("ref") not in EVENT_REFS:
        problems.append(f"{where} fetches a ref other than the push's before and after")
    elif given.get("path") != EVENT_REFS[given["ref"]]:
        problems.append(f"{where} checks out into another path than the report reads")
    if set(given) - CHECKOUT_INPUTS:
        problems.append(f"{where} gives other inputs: {sorted(set(given) - CHECKOUT_INPUTS)}")
    if given.get("fetch-depth", 1) != 1 or given.get("fetch-tags"):
        problems.append(f"{where} fetches more than its one commit")
    return problems


def workflow_problems(text: str) -> list[str]:
    """What in the skeleton's workflow does more than post its comment (R237)."""
    data = yaml.safe_load(text)
    if not isinstance(data, dict) or not data.get("jobs"):
        return ["the workflow has no jobs, so this check examined nothing"]
    problems = []
    if re.search(r"\bsecrets\b", text):
        problems.append("the workflow reads a secret")
    event = data.get("on", data.get(True))
    if event != {"push": {"branches": ["main"]}}:
        problems.append(f"the workflow runs on another event: {event!r}")
    if data.get("permissions") != {"contents": "read", "pull-requests": "write"}:
        problems.append(f"the workflow asks for other permissions: {data.get('permissions')!r}")
    for name, job in data["jobs"].items():
        if "permissions" in job:
            problems.append(f"job {name} asks for permissions of its own")
        if not isinstance(job.get("timeout-minutes"), int):
            problems.append(f"job {name} sets no timeout-minutes")
        for number, step in enumerate(job.get("steps") or []):
            where = f"job {name}, step {number}"
            if "uses" in step:
                problems += checkout_problems(where, step)
            run = str(step.get("run", ""))
            if "run" in step and run.strip() != REPORT_COMMAND:
                problems.append(f"{where} runs another command than the report's: {run!r}")
            if "${{" in run:
                problems.append(f"{where} puts an expression inside its command")
            if re.search(r"\bgit\b.*\bfetch\b", run):
                problems.append(f"{where} fetches a ref other than the push's before and after")
    return problems


# R242: the skeleton says what it is.
COMMENTED = (".py", ".yml", ".yaml")


def opening_comment(text: str) -> str:
    """The comment lines that open a file, lower-cased and joined."""
    lines = []
    for line in text.splitlines():
        if not line.startswith("#"):
            break
        lines.append(line.lstrip("#!").strip())
    return " ".join(lines).lower()


def says_what_it_is(text: str) -> bool:
    words = " ".join(text.lower().split())
    return "walking skeleton" in words and "not the tool" in words


def identity_problems(skeleton: Path, readme_text: str) -> list[str]:
    """Each skeleton file that does not say it is the walking skeleton, and a silent README."""
    if not skeleton.is_dir():
        return [f"{skeleton.name}/ does not exist, so this check examined nothing"]
    problems = []
    for file in sorted(skeleton.rglob("*")):
        if file.suffix in COMMENTED and not says_what_it_is(opening_comment(file.read_text())):
            problems.append(f"{file.name} does not open by saying it is the walking skeleton")
    manifest = skeleton / "plugin.json"
    description = (
        json.loads(manifest.read_text()).get("description", "") if manifest.is_file() else ""
    )
    if not says_what_it_is(str(description)):
        problems.append("plugin.json's description does not say it is the walking skeleton")
    status = re.search(r"^\*\*Status:.*?(?=\n\n)", readme_text, re.M | re.S)
    if not status or "`skeleton/`" not in status[0] or not says_what_it_is(status[0]):
        problems.append("the README's status does not name `skeleton/` as the walking skeleton")
    return problems


# ---- This repository ----


def test_nothing_here_registers_the_walking_skeleton() -> None:
    files = list(tracked_texts())
    assert any(path.startswith(REGISTERING_FOLDERS) for path, _ in files), "examined nothing"
    assert registration_problems(files) == []


def test_each_kept_transcript_shape_holds_no_values() -> None:
    shapes = kept_shapes(tracked_files())
    problems = missing_shape_problems(TASKS.read_text(encoding="utf-8"), shapes)
    for shape in shapes:
        problems += shape_problems(ROOT / shape, shape)
    assert problems == []


def test_the_skeletons_workflow_can_do_no_more_than_post_its_comment() -> None:
    assert workflow_problems((SKELETON / "workflow.yml").read_text(encoding="utf-8")) == []


def test_the_walking_skeleton_says_what_it_is() -> None:
    assert identity_problems(SKELETON, README.read_text(encoding="utf-8")) == []


# ---- R234, planted ----


@pytest.mark.parametrize(
    ("path", "text"),
    [
        (".claude/settings.json", '{"hooks": {"Stop": [{"command": "python3 ./skeleton/c.py"}]}}'),
        (".claude/hooks/session-start.sh", "cp -r skeleton/ ~/plugins\n"),
        (".claude-plugin/marketplace.json", '{"plugins": [{"name": "Skeleton"}]}'),
        (".github/workflows/ci.yml", "run: python SKELETON/report.py\n"),
        (".github/workflows/skeleton.yml", "name: report\n"),
    ],
)
def test_a_file_that_names_the_skeleton_where_it_could_register_it_fails(
    path: str, text: str
) -> None:
    problems = registration_problems([(path, text)])
    assert len(problems) == 1 and path in problems[0]


def test_the_skeletons_own_files_pass_the_registration_check() -> None:
    files = [("skeleton/capture.py", "# the walking skeleton\n"), ("README.md", "`skeleton/`")]
    assert registration_problems(files) == []


# ---- R236, planted ----

GOOD_SHAPE = [
    {"path": "type", "type": "string"},
    {"path": "isSidechain", "type": "boolean"},
    {"path": "toolUseResult", "type": "object"},
    {"path": "message", "type": "object"},
    {"path": "message.content", "type": "array"},
    {"path": "message.stop_sequence", "type": "null"},
    {"path": "message.usage", "type": "object"},
    {"path": "message.usage.cache_creation_input_tokens", "type": "number"},
]


def write_shape(folder: Path, data: object) -> Path:
    path = folder / "transcript-shape.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_a_shape_of_names_and_types_passes(tmp_path: Path) -> None:
    assert shape_problems(write_shape(tmp_path, GOOD_SHAPE), "shape") == []


@pytest.mark.parametrize(
    "entry",
    [
        {"path": "message.model", "type": "string", "value": "a-model"},
        {"path": "message.model", "type": "a-model"},
        {"path": "message.model", "type": 3},
        "message.model",
        {"path": "cwd value/with a slash", "type": "string"},
        {"path": "message.na-me", "type": "string"},
        {"path": "a" * 41, "type": "string"},
        {"path": "message.content.text", "type": "string"},
        {"path": "toolUseResult.stdout", "type": "string"},
        {"path": "wireToolInputs.toolu" + "_01ABCDEFGHJKMNPQ", "type": "object"},
        {"path": "message.usage.extra.deeper", "type": "number"},
        {"path": "toolu" + "_01ABCDEFGHJKMNPQ", "type": "object"},
        {"path": "msg" + "_A1b2C3d4", "type": "string"},
    ],
)
def test_a_value_or_a_name_out_of_place_in_the_shape_fails(tmp_path: Path, entry: object) -> None:
    path = write_shape(tmp_path, [*GOOD_SHAPE, entry])
    problems = shape_problems(path, "tests/fixtures/transcript-shape.json")
    assert len(problems) == 1
    assert problems[0].startswith(f"tests/fixtures/transcript-shape.json: entry {len(GOOD_SHAPE)} ")


@pytest.mark.parametrize("text", ["[]", "{}", "not json", '{"path": "type"}'])
def test_a_shape_that_holds_no_entries_fails(tmp_path: Path, text: str) -> None:
    path = tmp_path / "transcript-shape.json"
    path.write_text(text, encoding="utf-8")
    assert shape_problems(path, "shape") != []


def test_a_top_level_name_outside_the_list_fails(tmp_path: Path) -> None:
    path = write_shape(tmp_path, [*GOOD_SHAPE, {"path": "hostFeatureState", "type": "object"}])
    problems = shape_problems(path, "shape")
    assert len(problems) == 1 and f"entry {len(GOOD_SHAPE)} " in problems[0]


def test_the_check_and_the_recorder_share_one_list_of_top_level_names() -> None:
    import shape

    assert shape.TOP_LEVEL_NAMES == TOP_LEVEL_NAMES
    assert {entry["path"] for entry in GOOD_SHAPE if "." not in entry["path"]} <= TOP_LEVEL_NAMES


def test_kept_shapes_are_the_tracked_files_under_tests_that_begin_with_its_name() -> None:
    paths = ["tests/fixtures/transcript-shape.json", "tests/transcript-shape-2.json", "docs/x"]
    paths += ["tests/fixtures/a-transcript-shape.json", "transcript-shape.json"]
    assert kept_shapes(paths) == paths[:2]


def test_no_kept_shape_after_the_run_fails() -> None:
    ticked = "- [x] 1.36 Run the walking skeleton once\n"
    assert missing_shape_problems(ticked, []) == [
        "task 1.36 is ticked, but the transcript shape is missing (R236)"
    ]
    assert missing_shape_problems(ticked, ["tests/fixtures/transcript-shape.json"]) == []
    assert missing_shape_problems("- [ ] 1.36 Run the walking skeleton once\n", []) == []


# ---- R237, planted ----

PIN = "3d3c42e5aac5ba805825da76410c181273ba90b1"
GOOD_WORKFLOW = f"""\
# The walking skeleton, not the tool.
name: report
on:
  push:
    branches: [main]
permissions:
  contents: read
  pull-requests: write
jobs:
  report:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@{PIN} # v7
        with:
          ref: ${{{{ github.event.before }}}}
          path: before
          persist-credentials: false
      - uses: actions/checkout@{PIN} # v7
        with:
          ref: ${{{{ github.event.after }}}}
          path: after
          persist-credentials: false
      - env:
          AFTER: ${{{{ github.event.after }}}}
        run: python3 -I after/skeleton/report.py before after
"""


def test_the_workflow_as_designed_passes() -> None:
    assert workflow_problems(GOOD_WORKFLOW) == []


@pytest.mark.parametrize(
    ("old", "new", "named"),
    [
        ("  push:\n    branches: [main]", "  pull_request_target:", "another event"),
        ("branches: [main]", "branches: [main, dev]", "another event"),
        ("contents: read", "contents: write", "other permissions"),
        ("    timeout-minutes: 5\n", "    timeout-minutes: 5\n    permissions: write-all\n", "own"),
        (
            f"- uses: actions/checkout@{PIN} # v7\n        with:\n"
            "          ref: ${{ github.event.before }}",
            "- uses: some/action@v1\n        with:\n          ref: ${{ github.event.before }}",
            "another action",
        ),
        (
            f"checkout@{PIN} # v7\n        with:\n          ref: ${{{{ github.event.after }}}}",
            "checkout@v7\n        with:\n          ref: ${{ github.event.after }}",
            "full commit",
        ),
        ("path: before\n          persist-credentials: false", "path: before", "credentials"),
        ("ref: ${{ github.event.before }}", "ref: refs/heads/dev", "other than the push"),
        ("path: after\n", "path: after\n          fetch-depth: 0\n", "more than its one commit"),
        ("run: python3", "run: GH=${{ secrets.TOKEN }} python3", "secret"),
        (
            "run: python3 -I",
            "run: echo ${{ github.event.head_commit.message }}; python3 -I",
            "expression",
        ),
        ("run: python3", "run: git fetch origin dev && python3", "other than the push"),
        ("    timeout-minutes: 5\n", "", "timeout-minutes"),
        ("path: after\n", "path: after\n          repository: someone/else\n", "other inputs"),
        ("run: python3", "run: echo '${{ toJSON(secrets) }}'; python3", "secret"),
        ("AFTER: ${{ github.event.after }}", "AFTER: ${{ secrets['PAT'] }}", "secret"),
        ("report.py before after", "report.py after before", "report"),
        ("path: before\n", "path: old\n", "path"),
    ],
)
def test_a_workflow_that_could_do_more_fails(old: str, new: str, named: str) -> None:
    assert old in GOOD_WORKFLOW
    problems = workflow_problems(GOOD_WORKFLOW.replace(old, new, 1))
    assert problems and any(named in p for p in problems), problems


def test_a_workflow_with_no_jobs_examined_nothing() -> None:
    assert workflow_problems("name: nothing\n") != []


# ---- R242, planted ----

SAYS = "# The walking skeleton of the agentic PR cost calculator: not the tool or a release.\n"
README_SAYS = (
    "**Status: proposal.** `skeleton/` is the walking skeleton, which is not the tool.\n\n"
)


def planted_skeleton(folder: Path) -> Path:
    skeleton = folder / "skeleton"
    skeleton.mkdir()
    (skeleton / "capture.py").write_text("#!/usr/bin/env python3\n" + SAYS + "import os\n")
    (skeleton / "workflow.yml").write_text(SAYS + "name: report\n")
    description = "The walking skeleton of the agentic PR cost calculator, not the tool."
    (skeleton / "plugin.json").write_text(json.dumps({"description": description}))
    return skeleton


def test_a_skeleton_that_says_what_it_is_passes(tmp_path: Path) -> None:
    assert identity_problems(planted_skeleton(tmp_path), README_SAYS) == []


@pytest.mark.parametrize("name", ["capture.py", "workflow.yml"])
def test_a_skeleton_file_that_does_not_say_what_it_is_fails(tmp_path: Path, name: str) -> None:
    skeleton = planted_skeleton(tmp_path)
    (skeleton / name).write_text("import os\n# The walking skeleton, not the tool.\n")
    problems = identity_problems(skeleton, README_SAYS)
    assert len(problems) == 1 and name in problems[0]


def test_a_manifest_that_does_not_say_what_it_is_fails(tmp_path: Path) -> None:
    skeleton = planted_skeleton(tmp_path)
    (skeleton / "plugin.json").write_text(json.dumps({"description": "Records your calls."}))
    problems = identity_problems(skeleton, README_SAYS)
    assert len(problems) == 1 and "plugin.json" in problems[0]


@pytest.mark.parametrize(
    "readme",
    ["**Status: proposal.** None of the tool's code exists yet.\n\n", "No status here.\n\n"],
)
def test_a_readme_silent_on_the_skeleton_fails(tmp_path: Path, readme: str) -> None:
    problems = identity_problems(planted_skeleton(tmp_path), readme)
    assert len(problems) == 1 and "README" in problems[0]


def test_no_skeleton_folder_examined_nothing(tmp_path: Path) -> None:
    assert identity_problems(tmp_path / "skeleton", README_SAYS) != []
