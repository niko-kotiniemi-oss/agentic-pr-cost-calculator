"""Checks on the repository itself, before any calculator code exists.

These hold the properties the first pull request promises: the files a
standalone public repository needs, pinned tooling, a read-only CI token, and
nothing private carried over from elsewhere; and, until the tasks that bring
them are ticked, no switch, no ledger file and no reusable workflow (R223, R229).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import re
import subprocess
import tomllib
from collections.abc import Hashable, Iterable, Iterator
from pathlib import Path
from typing import Any

import pytest
import yaml
from test_roadmap import (
    ARCHIVED_TASKS,
    BUILD_CHANGE,
    CHANGE_TASKS,
    make_tree,
    tasks,
    tracked,
)

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CLAUDE.md",
    "renovate.json",
    "package.json",
    "package-lock.json",
    ".github/workflows/ci.yml",
    "openspec/config.yaml",
    "vendor/superpowers/UPSTREAM.lock",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    ".editorconfig",
    ".github/CODEOWNERS",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    "docs/requirements.md",
    "docs/how-it-works.md",
    "docs/features/README.md",
]

# Built from parts so that this file does not match its own patterns.
PRIVATE_PATTERNS = [
    re.compile(re.escape("claude.ai/code/" + "session_")),
    re.compile("cmsg" + r"_[0-9A-Za-z]{8,}"),
    re.compile("chan" + r"_[0-9A-Za-z]{8,}"),
    re.compile(re.escape("/mnt/" + "project-files")),
    re.compile("Claude-" + "Session:"),
]


# Names that must not appear in this repository, kept as SHA-256 hashes so that
# this file does not publish them. Each tracked file is lower-cased and split
# into words; every word and every pair of adjacent words joined by a hyphen is
# hashed and looked up, so a two-word name is caught however it is separated.
PRIVATE_NAME_HASHES = frozenset(
    {
        "9e55544b519dc9d719dd78d15d7c454ac85830b977a93e5c086275dc6b8732ce",
    }
)


def private_names_in(text: str, hashes: frozenset[str] = PRIVATE_NAME_HASHES) -> bool:
    words = re.findall(r"[a-z0-9]+", text.lower())
    candidates = set(words) | {f"{a}-{b}" for a, b in itertools.pairwise(words)}
    return any(hashlib.sha256(c.encode()).hexdigest() in hashes for c in candidates)


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
    ).stdout.decode()
    return [p for p in out.split("\0") if p]


def test_every_required_file_exists() -> None:
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).is_file()]
    assert not missing, f"missing: {missing}"


def test_the_licence_is_mit() -> None:
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert text.startswith("MIT License")


def private_references(
    path: str, text: str, hashes: frozenset[str] = PRIVATE_NAME_HASHES
) -> list[str]:
    """The private references in a file and in its path, named but not quoted."""
    hits = []
    for where, value in (("", text), (" in its path", path)):
        hits += [f"{path}: {p.pattern}{where}" for p in PRIVATE_PATTERNS if p.search(value)]
        if private_names_in(value, hashes):
            hits.append(f"{path}: a private name{where}")
    return hits


def private_reference_problems(files: Iterable[tuple[str, str]]) -> list[str]:
    """The private references in (path, text) pairs, and whether any text was read at all."""
    hits, read = [], 0
    for path, text in files:
        read += bool(text)
        hits += private_references(path, text)
    problems = [] if read else ["no tracked file was read, so this test covered nothing"]
    if hits:
        problems.append("private references found:\n" + "\n".join(hits))
    return problems


def tracked_texts() -> Iterator[tuple[str, str]]:
    """Each tracked file's path and text, with no text for a file that is not UTF-8."""
    for path in tracked_files():
        file = ROOT / path
        try:
            text = file.read_text(encoding="utf-8") if file.is_file() else ""
        except UnicodeDecodeError:
            text = ""
        yield path, text


def test_no_tracked_file_carries_a_private_reference() -> None:
    problems = private_reference_problems(tracked_texts())
    assert not problems, "\n".join(problems)


def test_a_read_that_finds_no_text_is_named() -> None:
    nothing = "no tracked file was read, so this test covered nothing"
    assert private_reference_problems([]) == [nothing]
    assert private_reference_problems([("empty.md", "")]) == [nothing]
    assert private_reference_problems([("plain.md", "plain text")]) == []


def test_a_private_reference_in_a_path_is_named() -> None:
    hashes = frozenset({hashlib.sha256(b"example-venture").hexdigest()})
    assert private_references("docs/DR-001-example-venture.md", "", hashes) == [
        "docs/DR-001-example-venture.md: a private name in its path"
    ]
    path = "docs/cmsg" + "_01ABCDEFGHJK.md"
    assert private_references(path, "cmsg" + "_01ABCDEFGHJK", hashes) == [
        f"{path}: cmsg_[0-9A-Za-z]{{8,}}",
        f"{path}: cmsg_[0-9A-Za-z]{{8,}} in its path",
    ]
    assert private_references("docs/a-plain-name.md", "plain text", hashes) == []


def test_the_privacy_patterns_catch_what_they_are_for() -> None:
    samples = [
        "see https://claude.ai/code/" + "session_01ABCDEF",
        "thread cmsg" + "_01ABCDEFGHJKMNPQ",
        "project chan" + "_01ABCDEFGHJKMNPQ",
        "/mnt/" + "project-files/example/",
        "Claude-" + "Session: x",
    ]
    for sample in samples:
        assert any(p.search(sample) for p in PRIVATE_PATTERNS), sample
    assert not any(p.search("an ordinary sentence about pull requests") for p in PRIVATE_PATTERNS)


def test_the_private_name_check_matches_the_name_however_it_is_written() -> None:
    # A made-up name and its hash stand in for the real ones, so that this test
    # publishes nothing: an encoded copy of a name is still the name.
    hashes = frozenset({hashlib.sha256(b"example-venture").hexdigest()})
    assert private_names_in("see github.com/Example-Venture/x", hashes)
    assert private_names_in("Copyright Example Venture", hashes)
    assert private_names_in("EXAMPLE_VENTURE", hashes)
    assert not private_names_in("an example of a venture", hashes)
    assert not private_names_in("Example-Ventures", hashes)
    assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in PRIVATE_NAME_HASHES)


def renovate() -> dict[str, Any]:
    config: dict[str, Any] = json.loads((ROOT / "renovate.json").read_text(encoding="utf-8"))
    return config


def test_renovate_waits_fourteen_days_for_every_datable_update() -> None:
    rules = [
        r
        for r in renovate().get("packageRules", [])
        if set(r.get("matchUpdateTypes", [])) >= {"major", "minor", "patch", "digest"}
    ]
    assert rules and all(r.get("minimumReleaseAge") == "14 days" for r in rules)


def vulnerability_fix_delays(config: dict[str, Any]) -> list[str]:
    """What would hold a vulnerability fix back: a release age, an approval, or alerts off."""
    alerts = config.get("vulnerabilityAlerts", {})
    delays = []
    if alerts.get("minimumReleaseAge", "unset") is not None:
        delays.append("vulnerability fixes wait for the release age")
    if alerts.get("dependencyDashboardApproval") is not False:
        delays.append("vulnerability fixes wait for approval on the dependency dashboard")
    if config.get("osvVulnerabilityAlerts") is not True:
        delays.append("OSV vulnerability alerts are off")
    return delays


def test_renovate_does_not_delay_vulnerability_fixes() -> None:
    assert vulnerability_fix_delays(renovate()) == []


def test_what_would_delay_a_vulnerability_fix_is_named() -> None:
    assert vulnerability_fix_delays({}) == [
        "vulnerability fixes wait for the release age",
        "vulnerability fixes wait for approval on the dependency dashboard",
        "OSV vulnerability alerts are off",
    ]
    fast = {"minimumReleaseAge": None, "dependencyDashboardApproval": False}
    assert vulnerability_fix_delays({"vulnerabilityAlerts": fast}) == [
        "OSV vulnerability alerts are off"
    ]


def test_renovate_reads_the_vendored_lock() -> None:
    config = renovate()
    assert not any("vendor" in p for p in config.get("ignorePaths", [])), config.get("ignorePaths")
    patterns = [
        p for m in config.get("customManagers", []) for p in m.get("managerFilePatterns", [])
    ]
    assert any("UPSTREAM" in p for p in patterns)


def workflows() -> list[Path]:
    folder = ROOT / ".github" / "workflows"
    return sorted([*folder.glob("*.yml"), *folder.glob("*.yaml")])


def test_every_workflow_declares_a_read_only_token() -> None:
    assert workflows(), "no workflow was found, so this test covered nothing"
    for path in workflows():
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert doc.get("permissions") == {"contents": "read"}, path.name


# The workflows that may grant a job a write permission, and which ones. The
# report's and the release's workflows add their entries when they are built.
WRITES_ALLOWED: dict[str, set[str]] = {}

# Triggers that run a workflow with this repository's token on someone else's code.
FORBIDDEN_TRIGGERS = {"pull_request_target", "workflow_run"}


class WorkflowLoader(yaml.SafeLoader):
    """YAML read as `yaml.safe_load` reads it, but a mapping that gives a key twice is
    refused, since PyYAML keeps its last value and another reader may not."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        seen: set[Any] = set()
        for key_node, _ in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                continue
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, Hashable):
                continue
            if key in seen:
                written = key_node.value if isinstance(key_node, yaml.ScalarNode) else key
                raise yaml.constructor.ConstructorError(
                    None, None, f"gives the key {written!r} twice", key_node.start_mark
                )
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def load_workflow(text: str) -> Any:
    loader = WorkflowLoader(text)
    try:
        return loader.get_single_data()
    finally:
        loader.dispose()


def triggers(doc: dict[Any, Any]) -> set[str]:
    """The events that a workflow names under `on`, quoted or bare, which YAML 1.1 reads
    as the boolean true, given as one name, as a mapping, or as a list of names and
    mappings."""
    found: set[str] = set()
    for on in (doc.get("on"), doc.get(True)):
        for item in on if isinstance(on, list) else [on]:
            if isinstance(item, str):
                found.add(item)
            elif isinstance(item, dict):
                found.update(str(key) for key in item)
    return found


def writes(permissions: Any) -> set[str]:
    if permissions == "write-all":
        return {"write-all"}
    if isinstance(permissions, dict):
        return {f"{scope}: write" for scope, level in permissions.items() if level == "write"}
    return set()


def workflow_problems(name: str, text: str) -> list[str]:
    doc = load_workflow(text)
    problems = [
        f"{name} triggers on {trigger}" for trigger in sorted(triggers(doc) & FORBIDDEN_TRIGGERS)
    ]
    blocks = [("the workflow", doc.get("permissions"))] + [
        (f"job `{job}`", body.get("permissions")) for job, body in (doc.get("jobs") or {}).items()
    ]
    allowed = WRITES_ALLOWED.get(name, set())
    for where, permissions in blocks:
        problems.extend(
            f"{name} {where} grants `{grant}`" for grant in sorted(writes(permissions) - allowed)
        )
    if re.search(r"\bsecrets\b", text):
        problems.append(f"{name} reads a secret")
    return problems


def test_no_workflow_writes_runs_on_foreign_triggers_or_reads_a_secret() -> None:
    problems = [
        problem
        for path in workflows()
        for problem in workflow_problems(path.name, path.read_text(encoding="utf-8"))
    ]
    assert not problems, problems


PLANTED_WORKFLOW = """\
on:
  pull_request_target:
  workflow_run:
    workflows: [ci]
  push:
permissions: write-all
jobs:
  a:
    permissions:
      contents: read
      issues: write
    steps:
      - run: echo ${{ secrets.TOKEN }}
"""


def test_the_workflow_checks_name_each_planted_violation() -> None:
    assert workflow_problems("x.yaml", PLANTED_WORKFLOW) == [
        "x.yaml triggers on pull_request_target",
        "x.yaml triggers on workflow_run",
        "x.yaml the workflow grants `write-all`",
        "x.yaml job `a` grants `issues: write`",
        "x.yaml reads a secret",
    ]


def test_a_write_the_workflow_is_allowed_is_not_reported(monkeypatch: Any) -> None:
    text = "on: push\njobs:\n  a:\n    permissions:\n      pull-requests: write\n"
    assert workflow_problems("r.yml", text) == ["r.yml job `a` grants `pull-requests: write`"]
    monkeypatch.setitem(WRITES_ALLOWED, "r.yml", {"pull-requests: write"})
    assert workflow_problems("r.yml", text) == []
    assert triggers({"on": ["push", "pull_request"]}) == {"push", "pull_request"}


@pytest.mark.parametrize(
    "text",
    [
        "'on': push\non: pull_request_target\n",
        "on: push\n'on': pull_request_target\n",
        "on: [push, {pull_request_target: {}}]\n",
    ],
)
def test_a_trigger_under_either_on_key_or_in_a_list_s_mapping_is_read(text: str) -> None:
    assert workflow_problems("x.yml", text) == ["x.yml triggers on pull_request_target"]


def test_a_workflow_that_gives_a_key_twice_is_refused() -> None:
    with pytest.raises(yaml.YAMLError, match="gives the key 'on' twice"):
        workflow_problems("x.yml", "on: pull_request_target\non: push\n")


def checkouts(name: str, text: str) -> tuple[list[str], int]:
    """The checkout steps that keep their credentials in the clone, and how many there are."""
    doc = yaml.safe_load(text)
    kept = []
    count = 0
    for job, body in (doc.get("jobs") or {}).items():
        for step in body.get("steps") or []:
            if str(step.get("uses", "")).startswith("actions/checkout@"):
                count += 1
                if (step.get("with") or {}).get("persist-credentials") is not False:
                    kept.append(
                        f"{name} job `{job}` checks out without `persist-credentials: false`"
                    )
    return kept, count


def test_every_checkout_leaves_its_credentials_out_of_the_clone() -> None:
    found = [checkouts(path.name, path.read_text(encoding="utf-8")) for path in workflows()]
    assert sum(count for _, count in found), "no checkout was found, so this test covered nothing"
    kept = [problem for problems, _ in found for problem in problems]
    assert not kept, kept


def test_a_checkout_that_keeps_its_credentials_is_named() -> None:
    step = "      - uses: actions/checkout@0123\n"
    text = (
        "jobs:\n  a:\n    steps:\n"
        + step
        + step
        + "        with:\n          persist-credentials: false\n"
        + step
        + "        with:\n          persist-credentials: 'false'\n"
        + "      - run: echo\n"
    )
    assert checkouts("x.yml", text) == (
        ["x.yml job `a` checks out without `persist-credentials: false`"] * 2,
        3,
    )


BASE_ENV = {"BASE_COMMIT": "${{ github.event.pull_request.base.sha || github.event.before }}"}
# GitHub's default activity types for a pull request, and `edited`, which a change of its
# base branch is.
TYPES = ["opened", "synchronize", "reopened", "edited"]


def history_problems(doc: dict[Any, Any]) -> list[str]:
    """What keeps the tests' job from comparing with its base: a clone of less than the
    whole history, a base commit that the tests are not given, or a run that a change of
    the pull request's base, or a push to the default branch, does not start."""
    steps = doc["jobs"]["python"]["steps"]
    checkout = next(s for s in steps if str(s.get("uses", "")).startswith("actions/checkout@"))
    tests = next(s for s in steps if s.get("run") == "pytest")
    problems = []
    if (checkout.get("with") or {}).get("fetch-depth") != 0:
        problems.append("the tests' checkout fetches less than the whole history")
    if tests.get("env") != BASE_ENV:
        problems.append("the tests name no base commit, or another one")
    on = doc.get("on", doc.get(True))
    pull_request = on.get("pull_request") if isinstance(on, dict) else None
    if not set(TYPES) <= set((pull_request or {}).get("types") or []):
        problems.append(
            "the tests do not run when a pull request is opened, pushed to, reopened or retargeted"
        )
    push = on.get("push") if isinstance(on, dict) else None
    if (
        not isinstance(push, dict)
        or "main" not in (push.get("branches") or [])
        or {"paths", "paths-ignore"} & push.keys()
    ):
        problems.append("the tests do not run on every push to the default branch")
    return problems


def test_ci_runs_the_tests_on_the_whole_history_and_names_their_base() -> None:
    # The decision-record checks compare with this base, so a clone of one commit,
    # or a run that names no base, would compare nothing.
    doc = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8"))
    assert history_problems(doc) == []


def test_a_test_job_without_the_history_or_its_base_is_named() -> None:
    def job(checkout: dict[str, Any], env: dict[str, str] | None) -> dict[Any, Any]:
        tests: dict[str, Any] = {"run": "pytest"} | ({"env": env} if env is not None else {})
        steps = [{"uses": "actions/checkout@0123", "with": checkout}, tests]
        on = {"pull_request": {"types": TYPES}, "push": {"branches": ["main"]}}
        return {True: on, "jobs": {"python": {"steps": steps}}}

    shallow = "the tests' checkout fetches less than the whole history"
    unnamed = "the tests name no base commit, or another one"
    assert history_problems(job({}, BASE_ENV)) == [shallow]
    assert history_problems(job({"fetch-depth": 1}, BASE_ENV)) == [shallow]
    assert history_problems(job({"fetch-depth": 0}, None)) == [unnamed]
    other = {"BASE_COMMIT": "${{ github.event.before }}"}
    assert history_problems(job({"fetch-depth": 0}, other)) == [unnamed]
    assert history_problems(job({"fetch-depth": 0}, BASE_ENV)) == []


def test_a_workflow_that_does_not_run_again_when_a_base_changes_is_named() -> None:
    steps = [
        {"uses": "actions/checkout@0123", "with": {"fetch-depth": 0}},
        {"run": "pytest", "env": BASE_ENV},
    ]
    unrun = "the tests do not run when a pull request is opened, pushed to, reopened or retargeted"
    unpushed = "the tests do not run on every push to the default branch"
    push = {"branches": ["main"]}
    for on, expected in (
        ({"pull_request": None, "push": push}, [unrun]),
        ({"pull_request": {"types": ["opened", "synchronize", "reopened"]}, "push": push}, [unrun]),
        ({"pull_request": {"types": ["edited"]}, "push": push}, [unrun]),
        ({"pull_request": {"types": TYPES}}, [unpushed]),
        ({"pull_request": {"types": TYPES}, "push": None}, [unpushed]),
        ({"pull_request": {"types": TYPES}, "push": {"branches": ["release"]}}, [unpushed]),
        ({"pull_request": {"types": TYPES}, "push": push | {"paths": ["src/**"]}}, [unpushed]),
        ({"pull_request": {"types": TYPES}, "push": push | {"paths-ignore": ["*.md"]}}, [unpushed]),
        (["pull_request", "push"], [unrun, unpushed]),
        ("pull_request", [unrun, unpushed]),
        (None, [unrun, unpushed]),
    ):
        assert history_problems({True: on, "jobs": {"python": {"steps": steps}}}) == expected, on


def unpinned_actions(files: Iterable[tuple[str, str]]) -> list[str]:
    """Each action that a workflow uses by anything but a full commit, and whether any was used."""
    used, unpinned = 0, []
    for name, text in files:
        for line in text.splitlines():
            m = re.search(r"uses:\s*([^\s#]+)", line)
            used += bool(m)
            if m and not re.fullmatch(r"[^@]+@[0-9a-f]{40}", m.group(1)):
                unpinned.append(f"{name}: {m.group(1)}")
    return unpinned if used else ["no action was found, so this test covered nothing"]


def test_every_action_is_pinned_to_a_full_commit() -> None:
    problems = unpinned_actions(
        (path.name, path.read_text(encoding="utf-8")) for path in workflows()
    )
    assert not problems, problems


def test_a_workflow_without_an_action_is_named() -> None:
    nothing = "no action was found, so this test covered nothing"
    assert unpinned_actions([]) == [nothing]
    assert unpinned_actions([("ci.yml", "    steps:\n      - run: pytest\n")]) == [nothing]
    pinned = "      - uses: actions/checkout@" + "0" * 40 + "\n"
    assert unpinned_actions([("ci.yml", pinned)]) == []
    tagged = "      - uses: actions/checkout@v4\n"
    assert unpinned_actions([("ci.yml", tagged)]) == ["ci.yml: actions/checkout@v4"]


def test_openspec_is_pinned_to_an_exact_version() -> None:
    deps = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["devDependencies"]
    assert re.fullmatch(r"\d+\.\d+\.\d+", deps["@fission-ai/openspec"])


# OpenSpec honours DO_NOT_TRACK; the vendored Superpowers reads its own switch.
TELEMETRY_SWITCHES = {"DO_NOT_TRACK": "1", "SUPERPOWERS_DISABLE_TELEMETRY": "1"}


def telemetry_left_on(env: dict[str, str]) -> list[str]:
    return sorted(name for name, value in TELEMETRY_SWITCHES.items() if env.get(name) != value)


def test_sessions_here_turn_telemetry_off() -> None:
    settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    assert telemetry_left_on(settings.get("env", {})) == []


def test_the_telemetry_check_names_a_switch_left_on() -> None:
    assert telemetry_left_on({"DO_NOT_TRACK": "1"}) == ["SUPERPOWERS_DISABLE_TELEMETRY"]
    assert telemetry_left_on({"DO_NOT_TRACK": "0", "SUPERPOWERS_DISABLE_TELEMETRY": "1"}) == [
        "DO_NOT_TRACK"
    ]


def lock_field(name: str) -> str:
    text = (ROOT / "vendor/superpowers/UPSTREAM.lock").read_text(encoding="utf-8")
    m = re.search(rf"^{name}=(.*)$", text, re.MULTILINE)
    assert m, name
    return m.group(1)


def test_the_vendored_lock_names_a_full_commit_and_a_tag() -> None:
    # The upstream itself is pinned here, so a lock cannot move to another
    # repository's tags without this line changing in review.
    assert lock_field("repo") == "obra/superpowers"
    assert re.fullmatch(r"[0-9a-f]{40}", lock_field("sha"))
    assert re.fullmatch(r"v\d+\.\d+\.\d+", lock_field("tag"))


def test_the_sync_script_and_the_lock_list_the_same_paths() -> None:
    script = (ROOT / "scripts/sync-superpowers.sh").read_text(encoding="utf-8")
    m = re.search(r"^PATHS=\((.*)\)$", script, re.MULTILINE)
    assert m
    assert m.group(1).split() == lock_field("vendored_paths").split(",")


# The oldest Python the tool supports. It rises only when this version nears
# its end of life, or when a security fix needs a newer one, so that adopters
# on older systems can keep using the tool.
def pyproject() -> dict[str, Any]:
    config: dict[str, Any] = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return config


def oldest_python() -> str:
    """The one source of the oldest supported Python: `requires-python`."""
    match = re.fullmatch(r">=(3\.\d+)", pyproject()["project"]["requires-python"])
    assert match, "requires-python is not of the form >=3.N"
    return match.group(1)


STATED_PYTHON = re.compile(r"\bPython (3\.\d+)\b")


def python_floor_problems(oldest: str, copies: dict[str, Any], prose: dict[str, str]) -> list[str]:
    """Name each copy of the oldest supported Python that disagrees with `oldest`.

    `copies` maps a setting to its value; `prose` maps a document to its text, where every
    "Python 3.N" it states must be the oldest version.
    """
    expected = {
        "ruff target-version": "py" + oldest.replace(".", ""),
        "mypy python_version": oldest,
        ".python-version": oldest,
    }
    problems = [
        f"{name} says {copies.get(name)!r}, not {value!r}"
        for name, value in expected.items()
        if copies.get(name) != value
    ]
    matrix = copies.get("CI matrix") or []
    if oldest not in matrix:
        problems.append(f"the CI matrix lacks the oldest supported Python {oldest}")
    if "3.x" not in matrix:
        problems.append("the CI matrix lacks the newest release, 3.x")
    for document, text in sorted(prose.items()):
        problems.extend(
            f"{document} names Python {version}, not {oldest}"
            for version in STATED_PYTHON.findall(text)
            if version != oldest
        )
    return problems


PYTHON_PROSE = [
    "README.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CLAUDE.md",
    "docs/features/releases-and-compatibility.md",
    "openspec/changes/add-pr-cost-calculator/specs/releases-and-compatibility/spec.md",
]


def test_every_copy_of_the_oldest_supported_python_matches_requires_python() -> None:
    config = pyproject()
    ci = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8"))
    copies = {
        "ruff target-version": config["tool"]["ruff"]["target-version"],
        "mypy python_version": config["tool"]["mypy"]["python_version"],
        ".python-version": (ROOT / ".python-version").read_text(encoding="utf-8").strip(),
        "CI matrix": ci["jobs"]["python"]["strategy"]["matrix"]["python-version"],
    }
    prose = {name: (ROOT / name).read_text(encoding="utf-8") for name in PYTHON_PROSE}
    assert all(STATED_PYTHON.search(text) for text in prose.values()), "a document states none"
    assert python_floor_problems(oldest_python(), copies, prose) == []


def test_a_copy_of_the_oldest_python_that_disagrees_is_named() -> None:
    copies = {
        "ruff target-version": "py311",
        "mypy python_version": "3.12",
        ".python-version": "3.11",
        "CI matrix": ["3.12"],
    }
    prose = {"README.md": "Runs on Python 3.10 and later.", "SECURITY.md": "Python 3.11."}
    assert python_floor_problems("3.11", copies, prose) == [
        "mypy python_version says '3.12', not '3.11'",
        "the CI matrix lacks the oldest supported Python 3.11",
        "the CI matrix lacks the newest release, 3.x",
        "README.md names Python 3.10, not 3.11",
    ]


def test_matching_copies_of_the_oldest_python_raise_nothing() -> None:
    copies = {
        "ruff target-version": "py312",
        "mypy python_version": "3.12",
        ".python-version": "3.12",
        "CI matrix": ["3.12", "3.x"],
    }
    assert python_floor_problems("3.12", copies, {"README.md": "Python 3.12 and later."}) == []


def test_the_project_version_is_semantic_and_the_changelog_has_an_unreleased_section() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", pyproject()["project"]["version"])
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert re.search(r"^## \[Unreleased\]$", changelog, re.MULTILINE)


def major_updates_need_approval(config: dict[str, Any]) -> bool:
    return any(
        rule.get("matchUpdateTypes") == ["major"] and rule.get("dependencyDashboardApproval")
        for rule in config.get("packageRules", [])
    )


def test_renovate_holds_major_updates_for_the_owner_and_lets_minor_and_patch_through() -> None:
    config = renovate()
    assert major_updates_need_approval(config)
    assert not config.get("dependencyDashboardApproval"), "every update would wait for approval"
    assert config.get("dependencyDashboard") is not False


def test_the_major_update_check_names_a_rule_that_is_missing() -> None:
    assert not major_updates_need_approval({"packageRules": []})
    assert not major_updates_need_approval(
        {
            "packageRules": [
                {"matchUpdateTypes": ["major", "minor"], "dependencyDashboardApproval": True}
            ]
        }
    )


def required_privacy_checkbox(form: dict[str, Any]) -> bool:
    return any(
        field.get("type") == "checkboxes"
        and field.get("id") == "privacy"
        and all(option.get("required") for option in field["attributes"]["options"])
        for field in form.get("body", [])
    )


def test_the_bug_report_form_requires_the_privacy_checkbox() -> None:
    form = yaml.safe_load(
        (ROOT / ".github/ISSUE_TEMPLATE/bug_report.yml").read_text(encoding="utf-8")
    )
    assert required_privacy_checkbox(form)


def test_a_bug_report_form_whose_privacy_checkbox_is_optional_is_refused() -> None:
    option = {"label": "No private text.", "required": False}
    field = {"type": "checkboxes", "id": "privacy", "attributes": {"options": [option]}}
    assert not required_privacy_checkbox({"body": [field]})
    assert not required_privacy_checkbox({"body": []})
    option["required"] = True
    assert required_privacy_checkbox({"body": [field]})


# R223 and R229: what this repository holds before the tool is turned on here.

NEITHER_TICKED = "- [ ] 4.3 Add the reusable workflow\n- [ ] 7.1 Turn the tool on here\n"
CAPTURE_ON = "- [ ] 4.3 Add the reusable workflow\n- [x] 7.1 Turn the tool on here\n"
GUARD_ADDED = "- [x] 4.3 Add the reusable workflow\n- [ ] 7.1 Turn the tool on here\n"
REUSABLE = "on:\n  workflow_call:\npermissions:\n  contents: read\n"


def ticked(root: Path, number: str) -> bool:
    """Whether a task of the change is ticked, in it or in its archived copy."""
    return tasks(root).get((BUILD_CHANGE, number), False)


def capture_file_problems(root: Path) -> list[str]:
    """R223: no switch and no ledger file at the root before task 7.1 turns the tool on."""
    if ticked(root, "7.1"):
        return []
    return [
        f"`{name}` is tracked at the root while task 7.1 of `{BUILD_CHANGE}` is not ticked"
        for name in sorted(tracked(root))
        if name == ".pr-cost.json" or name.startswith(".pr-cost/")
    ]


def reusable_workflow_problems(root: Path) -> list[str]:
    """R229: no workflow that another repository can call before task 4.3 adds its guard."""
    if ticked(root, "4.3"):
        return []
    problems = []
    for name in sorted(tracked(root)):
        if not name.startswith(".github/workflows/"):
            continue
        try:
            doc = load_workflow((root / name).read_text(encoding="utf-8"))
        except yaml.YAMLError:
            problems.append(
                f"`{name}` cannot be read as YAML, so it may declare `workflow_call` while "
                f"task 4.3 of `{BUILD_CHANGE}` is not ticked"
            )
            continue
        if isinstance(doc, dict) and "workflow_call" in triggers(doc):
            problems.append(
                f"`{name}` declares `workflow_call` while task 4.3 of `{BUILD_CHANGE}` is not "
                "ticked"
            )
    return problems


@pytest.mark.parametrize("name", [".pr-cost.json", ".pr-cost/a-ledger-file"])
def test_a_switch_or_a_ledger_file_at_the_root_before_task_7_1_is_named(
    tmp_path: Path, name: str
) -> None:
    root = make_tree(tmp_path, {CHANGE_TASKS: NEITHER_TICKED, name: "{}\n"})
    assert capture_file_problems(root) == [
        f"`{name}` is tracked at the root while task 7.1 of `add-pr-cost-calculator` is not ticked"
    ]


@pytest.mark.parametrize(
    "name",
    [
        "tests/golden/.pr-cost.json",
        "tests/golden/.pr-cost/a-ledger-file",
        ".pr-cost.json.example",
        ".pr-costs/a-file",
    ],
)
def test_a_name_that_is_not_the_switch_or_a_ledger_file_at_the_root_passes(
    tmp_path: Path, name: str
) -> None:
    root = make_tree(tmp_path, {CHANGE_TASKS: NEITHER_TICKED, name: "{}\n"})
    assert capture_file_problems(root) == []


def test_an_untracked_switch_is_not_named(tmp_path: Path) -> None:
    root = make_tree(tmp_path, {CHANGE_TASKS: NEITHER_TICKED})
    (root / ".pr-cost.json").write_text("{}\n")
    assert capture_file_problems(root) == []


@pytest.mark.parametrize("where", [CHANGE_TASKS, ARCHIVED_TASKS])
def test_a_switch_and_ledger_files_pass_once_task_7_1_is_ticked(tmp_path: Path, where: str) -> None:
    files: dict[str, str | None] = {
        where: CAPTURE_ON,
        ".pr-cost.json": "{}\n",
        ".pr-cost/a-ledger-file": "{}\n",
    }
    assert capture_file_problems(make_tree(tmp_path, files)) == []


def test_task_7_1_ticked_in_another_change_does_not_turn_the_tool_on_here(tmp_path: Path) -> None:
    files: dict[str, str | None] = {
        CHANGE_TASKS: NEITHER_TICKED,
        "openspec/changes/another/tasks.md": CAPTURE_ON,
        ".pr-cost.json": "{}\n",
    }
    assert capture_file_problems(make_tree(tmp_path, files)) == [
        "`.pr-cost.json` is tracked at the root while task 7.1 of `add-pr-cost-calculator` is "
        "not ticked"
    ]


@pytest.mark.parametrize(
    "workflow",
    [
        REUSABLE,
        "on: workflow_call\n",
        "on: [push, workflow_call]\n",
        "'on': {workflow_call: {inputs: {}}}\n",
        "'on': push\non: workflow_call\n",
        "on: push\n'on': workflow_call\n",
        "on: [push, {workflow_call: {}}]\n",
    ],
)
def test_a_reusable_workflow_before_task_4_3_is_named(tmp_path: Path, workflow: str) -> None:
    files: dict[str, str | None] = {
        CHANGE_TASKS: NEITHER_TICKED,
        ".github/workflows/report.yml": workflow,
    }
    assert reusable_workflow_problems(make_tree(tmp_path, files)) == [
        "`.github/workflows/report.yml` declares `workflow_call` while task 4.3 of "
        "`add-pr-cost-calculator` is not ticked"
    ]


@pytest.mark.parametrize("where", [CHANGE_TASKS, ARCHIVED_TASKS])
def test_a_reusable_workflow_passes_once_task_4_3_is_ticked(tmp_path: Path, where: str) -> None:
    files: dict[str, str | None] = {where: GUARD_ADDED, ".github/workflows/report.yml": REUSABLE}
    assert reusable_workflow_problems(make_tree(tmp_path, files)) == []


@pytest.mark.parametrize(
    ("name", "workflow"),
    [
        (".github/workflows/ci.yml", "on: [push, pull_request]\n"),
        (".github/workflows/ci.yml", "on: push\nx: &x {a: 1}\ny:\n  <<: *x\n  a: 2\n"),
        ("docs/a-reusable-workflow-shown.yml", REUSABLE),
    ],
)
def test_a_workflow_that_declares_no_workflow_call_or_lies_elsewhere_passes(
    tmp_path: Path, name: str, workflow: str
) -> None:
    files: dict[str, str | None] = {CHANGE_TASKS: NEITHER_TICKED, name: workflow}
    assert reusable_workflow_problems(make_tree(tmp_path, files)) == []


@pytest.mark.parametrize(
    "workflow",
    [
        "on: [workflow_call\n",
        "on: workflow_call\non: push\n",
        "a: 1\na: 2\n",
        "? [a, b]\n: c\n",
    ],
)
def test_a_workflow_that_cannot_be_read_is_named(tmp_path: Path, workflow: str) -> None:
    files: dict[str, str | None] = {
        CHANGE_TASKS: NEITHER_TICKED,
        ".github/workflows/broken.yml": workflow,
    }
    assert reusable_workflow_problems(make_tree(tmp_path, files)) == [
        "`.github/workflows/broken.yml` cannot be read as YAML, so it may declare "
        "`workflow_call` while task 4.3 of `add-pr-cost-calculator` is not ticked"
    ]


def test_this_repository_holds_no_switch_ledger_file_or_reusable_workflow_too_early() -> None:
    """A check that examined nothing fails: the tasks that each check waits for, and the
    workflows that one reads, are found."""
    change = "add-pr-cost-calculator"
    assert {(change, "4.3"), (change, "7.1")} <= tasks(ROOT).keys()
    assert any(name.startswith(".github/workflows/") for name in tracked(ROOT))
    assert capture_file_problems(ROOT) == []
    assert reusable_workflow_problems(ROOT) == []
