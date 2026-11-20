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
from collections.abc import Callable, Hashable, Iterable, Iterator
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
    # The identifiers that a transcript carries, of a message, a request and a tool call (T186).
    # A server tool call's too, and a message's with a platform's infix.
    # Its value holds a digit, which an ordinary name such as a field's does not.
    re.compile(
        r"\b(?:msg|req|toolu|srvtoolu)" + r"_(?:(?:bdrk|vrtx)_)?(?=[A-Za-z]*[0-9])[0-9A-Za-z]{8,}"
    ),
    # A session's or a line's identifier, a UUID in lower case (T190), as Claude Code writes it;
    # not in upper case, which fixed identifiers that protocols publish are written in.
    re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}" + r"-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
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


# The Fair Core License, version 1.0, with MIT as its future licence, as keygen-sh/fcl.dev
# publishes it in FCL-1.0-MIT.md: the SHA-256 of that text with its notice left blank, so that
# any other change to the licence's words fails (DR-242).
FCL_TEMPLATE_SHA256 = "7f96651038a80c680bb67a11e9e9e6007e5b1cb6ef02660b5fe5fb60daa3ad05"
FCL_BLANK_NOTICE = "Copyright ${year} ${licensor name}"
FCL_NOTICE_LINE = re.compile(r"(?m)^Copyright .*$")
# The notice that DR-242 gives, word for word, so that nothing is added on its line.
NOTICE = "Copyright 2026 Niko Kotiniemi"
# FCL is not on the SPDX list, so pyproject.toml names it by a reference of its own.
LICENCE_ID = "LicenseRef-FCL-1.0-MIT"


def licence_problems(licence: str, declared: object, notice: str = NOTICE) -> list[str]:
    """What keeps a licence text and a declared licence from being DR-242's."""
    problems = []
    notices = FCL_NOTICE_LINE.findall(licence)
    if notices != [notice]:
        problems.append(f"LICENSE's notices are {notices}, not [{notice!r}]")
    blank = FCL_NOTICE_LINE.sub(FCL_BLANK_NOTICE, licence)
    if hashlib.sha256(blank.encode()).hexdigest() != FCL_TEMPLATE_SHA256:
        problems.append("LICENSE is not the text of FCL-1.0-MIT with its notice filled in")
    if declared != LICENCE_ID:
        problems.append(f"pyproject.toml declares the licence {declared!r}, not {LICENCE_ID!r}")
    return problems


def licence_text() -> str:
    return (ROOT / "LICENSE").read_text(encoding="utf-8")


def test_the_licence_is_the_fair_core_license_with_mit_as_its_future_licence() -> None:
    assert licence_problems(licence_text(), pyproject()["project"].get("license")) == []


@pytest.mark.parametrize(
    ("plant", "declared", "problem"),
    [
        (lambda _: "MIT License\n\nCopyright (c) 2026 Someone\n", LICENCE_ID, "LICENSE is not"),
        (
            lambda t: t.replace("second anniversary", "tenth anniversary"),
            LICENCE_ID,
            "LICENSE is not",
        ),
        (lambda t: t.replace(NOTICE, FCL_BLANK_NOTICE), LICENCE_ID, "LICENSE's notices are ["),
        (
            lambda t: t.replace(NOTICE, "Copyright 2026 Someone Else"),
            LICENCE_ID,
            "LICENSE's notices",
        ),
        (
            lambda t: t.replace(NOTICE, NOTICE + ". Any Competing Use is also permitted."),
            LICENCE_ID,
            "LICENSE's notices",
        ),
        (lambda t: t + "\n" + NOTICE + "\n", LICENCE_ID, "LICENSE's notices"),
        (lambda t: t, "MIT", "pyproject.toml declares the licence 'MIT'"),
        (lambda t: t, None, "pyproject.toml declares the licence None"),
    ],
)
def test_another_licence_notice_or_reference_is_reported(
    plant: Callable[[str], str], declared: object, problem: str
) -> None:
    problems = licence_problems(plant(licence_text()), declared)
    assert any(p.startswith(problem) for p in problems), problems


def test_the_licence_check_passes_the_text_that_it_holds() -> None:
    assert licence_problems(licence_text(), LICENCE_ID) == []
    other = licence_text().replace(NOTICE, "Copyright 2026 Someone")
    assert licence_problems(other, LICENCE_ID, "Copyright 2026 Someone") == []


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
        # The identifiers that a transcript carries: of a message, a request and a tool call.
        '"id": "msg' + '_01ABCDEFGHJKMNPQRS"',
        "requestId req" + "_011CABCDEFGHJKMNPQ",
        "tool_use_id toolu" + "_01ABCDEFGHJKMNPQRS",
        "a server tool call srvtoolu" + "_01ABCDEFGHJKMNPQRS",
        '"id": "msg' + '_bdrk_01ABCDEFGHJKMNPQRS"',
        '"id": "msg' + '_vrtx_01ABCDEFGHJKMNPQRS"',
        # A session's or a line's identifier, as a transcript and its file name carry it.
        "sessionId 0f1e2d3c" + "-4b5a-6978-8a9b-0c1d2e3f4a5b",
    ]
    for sample in samples:
        assert any(p.search(sample) for p in PRIVATE_PATTERNS), sample
    ordinary = ["an ordinary sentence about pull requests", "the field stop_sequence", "msg_short"]
    ordinary += ["msg" + "_template", "req" + "_received", "toolu" + "_synthetic"]
    ordinary += ["msg" + "_send_callback", "req" + "_per_interval"]
    ordinary.append("a protocol's fixed GUID 258EAFA5" + "-E914-47DA-95CA-C5AB0DC85B11")
    for text in ordinary:
        assert not any(p.search(text) for p in PRIVATE_PATTERNS), text


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


# R259: Renovate proposes no newer `.python-version`, which keeps the development Python at
# the oldest supported release, by one rule for the manager that reads it alone, and nothing
# else, at any depth, sets a key that turns updates on or off by name.
PYTHON_VERSION_RULE = {"matchManagers": ["pyenv"], "enabled": False}
SWITCHES = ("enabled", "ignoreDeps", "enabledManagers")


def turns_off_python_version_alone(rule: dict[str, Any]) -> bool:
    """Whether a package rule turns off the manager `pyenv` and matches nothing else."""
    held = {key: value for key, value in rule.items() if key != "description"}
    return held == PYTHON_VERSION_RULE and held["enabled"] is False


def keys_at_any_depth(value: Any, where: str = "renovate.json") -> Iterator[tuple[str, str, Any]]:
    """Each key of each object in a configuration, at any depth, with the path of the object
    that holds it, and its value."""
    if isinstance(value, dict):
        for key, inner in value.items():
            yield where, key, inner
            yield from keys_at_any_depth(inner, f"{where}.{key}")
    elif isinstance(value, list):
        for number, inner in enumerate(value):
            yield from keys_at_any_depth(inner, f"{where}[{number}]")


def python_version_rule_problems(config: dict[str, Any]) -> list[str]:
    """Whether a package rule turns `pyenv` alone off, and each other key, at any depth, that
    turns updates on or off by name, by its path."""
    rules = config.get("packageRules", [])
    alone = [number for number, rule in enumerate(rules) if turns_off_python_version_alone(rule)]
    problems = []
    if not alone:
        problems.append(
            "Renovate would propose a newer Python for .python-version: no package rule"
            " turns the manager pyenv off"
        )
    kept = (f"renovate.json.packageRules[{alone[0]}]", "enabled") if alone else None
    problems += [
        f"{where}.{key} turns updates on or off, beside the rule for .python-version"
        for where, key, _ in keys_at_any_depth(config)
        if key in SWITCHES and (where, key) != kept
    ]
    return problems


def test_renovate_keeps_the_development_python_at_the_oldest_supported_release() -> None:
    assert python_version_rule_problems(renovate()) == []


def test_a_configuration_that_would_update_python_version_is_reported() -> None:
    assert python_version_rule_problems({"packageRules": []}) == [
        "Renovate would propose a newer Python for .python-version: no package rule"
        " turns the manager pyenv off"
    ]


@pytest.mark.parametrize(
    "rule",
    [
        {"matchManagers": ["pyenv", "npm"], "enabled": False},
        {"matchManagers": ["pyenv"], "matchPackageNames": ["python"], "enabled": False},
        {"matchManagers": ["pyenv"], "matchFileNames": [".python-version"], "enabled": False},
        {"matchManagers": ["pyenv"], "matchUpdateTypes": ["major"], "enabled": False},
        {"matchManagers": ["pyenv"], "enabled": 0},
    ],
)
def test_a_rule_that_turns_off_more_than_python_version_is_reported(rule: dict[str, Any]) -> None:
    config = {"packageRules": [{"description": "Other.", "minimumReleaseAge": "1 day"}, rule]}
    found = python_version_rule_problems(config)
    assert (
        "renovate.json.packageRules[1].enabled turns updates on or off, beside the rule for"
        " .python-version"
    ) in found


@pytest.mark.parametrize(
    ("added", "where"),
    [
        ({"packageRules": [{"matchPackageNames": ["x"], "enabled": False}]}, "packageRules[1]"),
        ({"packageRules": [{"matchManagers": ["pyenv"], "enabled": True}]}, "packageRules[1]"),
        ({"packageRules": [{"enabled": True}]}, "packageRules[1]"),
        ({"packageRules": [PYTHON_VERSION_RULE]}, "packageRules[1]"),
        ({"enabled": False}, ""),
        ({"npm": {"enabled": False}}, ".npm"),
        ({"pyenv": {"enabled": True}}, ".pyenv"),
    ],
)
def test_another_setting_of_enabled_at_any_depth_is_reported(
    added: dict[str, Any], where: str
) -> None:
    config = {"packageRules": [PYTHON_VERSION_RULE, *added.get("packageRules", [])]}
    config.update({key: value for key, value in added.items() if key != "packageRules"})
    path = f".{where}" if where.startswith("packageRules") else where
    assert python_version_rule_problems(config) == [
        f"renovate.json{path}.enabled turns updates on or off, beside the rule for .python-version"
    ]


@pytest.mark.parametrize("key", ["ignoreDeps", "enabledManagers"])
def test_a_key_that_turns_updates_off_by_name_is_reported(key: str) -> None:
    config = {"packageRules": [PYTHON_VERSION_RULE], key: ["@fission-ai/openspec"]}
    assert python_version_rule_problems(config) == [
        f"renovate.json.{key} turns updates on or off, beside the rule for .python-version"
    ]


def test_the_rule_for_python_version_alone_passes() -> None:
    rule = {"description": "Why.", **PYTHON_VERSION_RULE}
    other = {"description": "Other.", "minimumReleaseAge": "1 day"}
    assert python_version_rule_problems({"packageRules": [other, rule]}) == []


# R262: nothing narrows the files that Renovate reads or the versions that it proposes, but the
# list of paths that it skips, set at its top level alone, with no entry for `vendor/`, so
# that the vendored lock is read. A change to that list changes this one in the same diff.
# Renovate's other settings, such as its schedule, are left to the owner's review of this
# file's diff, which R134 keeps visible.
NARROWING = ("includePaths", "allowedVersions")
IGNORE_PATHS = [
    "**/node_modules/**",
    "**/bower_components/**",
    "**/examples/**",
    "**/__tests__/**",
    "**/test/**",
    "**/tests/**",
    "**/__fixtures__/**",
]


def narrowing_problems(config: dict[str, Any]) -> list[str]:
    """Each setting that narrows the files that Renovate reads or the versions that it
    proposes, by its path: an `includePaths` or an `allowedVersions` at any depth, an
    `ignorePaths` below the top level, and a top-level `ignorePaths` that is missing or is not
    the list that this test holds."""
    problems = [
        f"{where}.{key} narrows what Renovate proposes"
        for where, key, _ in keys_at_any_depth(config)
        if key in NARROWING or (key == "ignorePaths" and where != "renovate.json")
    ]
    if config.get("ignorePaths") != IGNORE_PATHS:
        problems.append("renovate.json.ignorePaths is not the list that this test holds")
    return problems


def test_renovate_narrows_nothing_that_it_proposes() -> None:
    assert narrowing_problems(renovate()) == []


@pytest.mark.parametrize(
    ("added", "path"),
    [
        ({"includePaths": ["src/**"]}, "renovate.json.includePaths"),
        ({"allowedVersions": "<2"}, "renovate.json.allowedVersions"),
        (
            {"packageRules": [{"matchPackageNames": ["ruff"], "allowedVersions": "<1"}]},
            "renovate.json.packageRules[0].allowedVersions",
        ),
        (
            {"packageRules": [{"matchManagers": ["pep621"], "includePaths": ["src/**"]}]},
            "renovate.json.packageRules[0].includePaths",
        ),
        ({"pep621": {"includePaths": ["pyproject.toml"]}}, "renovate.json.pep621.includePaths"),
        (
            {"github-actions": {"ignorePaths": [".github/**"]}},
            "renovate.json.github-actions.ignorePaths",
        ),
        (
            {"packageRules": [{"matchManagers": ["npm"], "ignorePaths": ["**/tests/**"]}]},
            "renovate.json.packageRules[0].ignorePaths",
        ),
    ],
)
def test_a_setting_that_narrows_what_renovate_proposes_is_reported(
    added: dict[str, Any], path: str
) -> None:
    config = {"ignorePaths": list(IGNORE_PATHS), **added}
    assert narrowing_problems(config) == [f"{path} narrows what Renovate proposes"]


@pytest.mark.parametrize(
    "ignore_paths",
    [
        [*IGNORE_PATHS, ".github/**"],
        [*IGNORE_PATHS, "**/vendor/**"],
        IGNORE_PATHS[1:],
        [],
        None,
    ],
)
def test_a_list_of_paths_to_skip_other_than_the_one_held_is_reported(
    ignore_paths: list[str] | None,
) -> None:
    config = {} if ignore_paths is None else {"ignorePaths": ignore_paths}
    assert narrowing_problems(config) == [
        "renovate.json.ignorePaths is not the list that this test holds"
    ]


def test_the_list_of_paths_to_skip_alone_passes() -> None:
    config = {"ignorePaths": list(IGNORE_PATHS), "packageRules": [PYTHON_VERSION_RULE]}
    assert narrowing_problems(config) == []


# R260: Renovate merges nothing on its own: no key whose name begins with `automerge` is set
# to anything but false, at any depth, and no preset is extended, at any depth, one written as
# a string included, but those listed here, since a preset that another repository serves can
# turn merging on later, in no diff here.
PRESETS = ("config:best-practices",)


def automerge_problems(config: Any) -> list[str]:
    """Each key, at any depth, whose name begins with `automerge` and whose value is not
    false, and each preset extended, at any depth, that this test does not list."""
    problems = []
    for where, key, inner in keys_at_any_depth(config):
        if key.casefold().startswith("automerge") and inner is not False:
            problems.append(f"{where}.{key} is {json.dumps(inner)}")
        if key == "extends":
            problems += [
                f"{where}.extends holds {preset}, which this test does not list"
                for preset in (inner if isinstance(inner, list) else [inner])
                if preset not in PRESETS
            ]
    return problems


def test_renovate_never_merges_on_its_own() -> None:
    config = renovate()
    assert config.get("extends"), "renovate.json extends no preset"
    assert automerge_problems(config) == []


@pytest.mark.parametrize(
    ("config", "problem"),
    [
        ({"automerge": True}, "renovate.json.automerge is true"),
        ({"automerge": "true"}, 'renovate.json.automerge is "true"'),
        (
            {"packageRules": [{}, {"matchUpdateTypes": ["patch"], "automerge": True}]},
            "renovate.json.packageRules[1].automerge is true",
        ),
        (
            {"vulnerabilityAlerts": {"automerge": True}},
            "renovate.json.vulnerabilityAlerts.automerge is true",
        ),
        (
            {"lockFileMaintenance": {"enabled": True, "automerge": True}},
            "renovate.json.lockFileMaintenance.automerge is true",
        ),
        ({"automergeMinor": True}, "renovate.json.automergeMinor is true"),
        (
            {"packageRules": [{"automergeType": "branch"}]},
            'renovate.json.packageRules[0].automergeType is "branch"',
        ),
        (
            {"extends": [":automergeMinor"]},
            "renovate.json.extends holds :automergeMinor, which this test does not list",
        ),
        (
            {"extends": ":automergeAll"},
            "renovate.json.extends holds :automergeAll, which this test does not list",
        ),
        (
            {"extends": ["config:best-practices", "github>someone/presets"]},
            "renovate.json.extends holds github>someone/presets, which this test does not list",
        ),
        (
            {"packageRules": [{"extends": ["github>someone/presets:AutoMerge"]}]},
            "renovate.json.packageRules[0].extends holds github>someone/presets:AutoMerge,"
            " which this test does not list",
        ),
    ],
)
def test_a_setting_that_would_let_renovate_merge_is_reported(
    config: dict[str, Any], problem: str
) -> None:
    assert automerge_problems(config) == [problem]


@pytest.mark.parametrize("extends", [["config:best-practices"], "config:best-practices"])
def test_a_configuration_that_merges_nothing_passes(extends: Any) -> None:
    config = {
        "extends": extends,
        "automerge": False,
        "packageRules": [{"automerge": False, "description": "automerge stays off."}],
    }
    assert automerge_problems(config) == []


# R261: an update of OpenSpec or Superpowers says how its files are refreshed.
REFRESHED = ("@fission-ai/openspec", "obra/superpowers")
REFRESH_NOTE = (
    "Before this merges, the owner reads this diff. Its generated or vendored files "
    "are then refreshed on this branch from a working tree outside any agent "
    "session's folder, by `scripts/verify-openspec.sh` for OpenSpec, which writes the "
    "generated skills again, or by `scripts/sync-superpowers.sh` for Superpowers, and "
    "the owner reads the refreshed diff before merging. No agent session starts on "
    "this branch before the owner has read its refreshed diff."
)
# The keys of the rule that gives the note: another matcher would narrow it to some updates.
NOTE_RULE_KEYS = {"matchPackageNames", "prBodyNotes"}


def refresh_note_problems(config: dict[str, Any]) -> list[str]:
    """Each of OpenSpec and Superpowers that no package rule matching it by name gives the
    note, as the only text of its `prBodyNotes`, in a rule that holds no other key but its
    description."""
    return [
        f"no package rule gives {package} the note on refreshing its files"
        for package in REFRESHED
        if not any(
            package in rule.get("matchPackageNames", [])
            and rule.get("prBodyNotes") == [REFRESH_NOTE]
            and rule.keys() - {"description"} == NOTE_RULE_KEYS
            for rule in config.get("packageRules", [])
        )
    ]


def test_an_update_of_openspec_or_superpowers_says_how_its_files_are_refreshed() -> None:
    assert refresh_note_problems(renovate()) == []


@pytest.mark.parametrize(
    ("rules", "missing"),
    [
        ([], list(REFRESHED)),
        (
            [{"matchPackageNames": ["@fission-ai/openspec"], "prBodyNotes": [REFRESH_NOTE]}],
            ["obra/superpowers"],
        ),
        (
            [{"matchPackageNames": list(REFRESHED), "prBodyNotes": [REFRESH_NOTE + " More."]}],
            list(REFRESHED),
        ),
        (
            [{"matchPackageNames": list(REFRESHED), "prBodyNotes": [REFRESH_NOTE, "More."]}],
            list(REFRESHED),
        ),
        ([{"matchPackageNames": ["/openspec/"], "prBodyNotes": [REFRESH_NOTE]}], list(REFRESHED)),
        (
            [
                {
                    "matchPackageNames": list(REFRESHED),
                    "matchUpdateTypes": ["major"],
                    "prBodyNotes": [REFRESH_NOTE],
                }
            ],
            list(REFRESHED),
        ),
        (
            [
                {
                    "matchPackageNames": list(REFRESHED),
                    "matchDatasources": ["npm"],
                    "prBodyNotes": [REFRESH_NOTE],
                }
            ],
            list(REFRESHED),
        ),
    ],
)
def test_an_update_without_its_note_is_reported(
    rules: list[dict[str, Any]], missing: list[str]
) -> None:
    assert refresh_note_problems({"packageRules": rules}) == [
        f"no package rule gives {package} the note on refreshing its files" for package in missing
    ]


def test_one_rule_that_gives_both_their_note_passes() -> None:
    rule = {"matchPackageNames": list(REFRESHED), "prBodyNotes": [REFRESH_NOTE]}
    assert refresh_note_problems({"packageRules": [rule]}) == []
    described = {"description": "Why.", **rule}
    assert refresh_note_problems({"packageRules": [described]}) == []


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
    # WorkflowLoader is a SafeLoader, so this builds no object that YAML names.
    return yaml.load(text, Loader=WorkflowLoader)


def triggers(doc: dict[Any, Any]) -> set[str]:
    """The events that a workflow names under `on`, quoted or bare, which YAML 1.1 reads
    as the boolean true, given as one name, as a mapping, or as a list of names and
    mappings.

    Raises ValueError for events given in any other form, which GitHub may read
    otherwise."""
    found: set[str] = set()
    for on in (doc.get("on"), doc.get(True)):
        if on is None:
            continue
        for item in on if isinstance(on, list) else [on]:
            if isinstance(item, str):
                found.add(item)
            elif isinstance(item, dict):
                found.update(str(key) for key in item)
            else:
                raise ValueError(f"events given as {type(item).__name__}")
    return found


def writes(permissions: Any) -> set[str]:
    if permissions == "write-all":
        return {"write-all"}
    if isinstance(permissions, dict):
        return {f"{scope}: write" for scope, level in permissions.items() if level == "write"}
    return set()


def workflow_problems(name: str, text: str) -> list[str]:
    doc = load_workflow(text)
    try:
        events = triggers(doc)
    except ValueError:
        problems = [f"{name} gives its events in a form that this check cannot read"]
    else:
        problems = [
            f"{name} triggers on {trigger}" for trigger in sorted(events & FORBIDDEN_TRIGGERS)
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


# R256: `.claude/settings.json` holds only these keys, at every level, with these values, so
# that a setting that keeps the context files from loading, such as `claudeMdExcludes`, a
# variable such as `CLAUDE_CODE_DISABLE_CLAUDE_MDS`, or another hook, marketplace or plugin
# fails until this test changes with it, in a diff that the owner reviews (T35, T230).
SETTINGS = {
    "$schema": "https://json.schemastore.org/claude-code-settings.json",
    "env": TELEMETRY_SWITCHES,
    "extraKnownMarketplaces": {
        "vendored": {"source": {"source": "directory", "path": "."}, "autoUpdate": False}
    },
    "enabledPlugins": {"superpowers@vendored": True},
    "hooks": {
        "SessionStart": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": 'bash "$CLAUDE_PROJECT_DIR"/.claude/hooks/session-start.sh',
                        "timeout": 180,
                        "statusMessage": "Installing the vendored plugin and the pinned tools...",
                    }
                ]
            },
            {
                "matcher": "startup|clear|compact",
                "hooks": [
                    {
                        "type": "command",
                        "command": 'CLAUDE_PLUGIN_ROOT="$CLAUDE_PROJECT_DIR"/vendor/superpowers'
                        ' bash "$CLAUDE_PROJECT_DIR"/vendor/superpowers/hooks/run-hook.cmd'
                        " session-start",
                        "timeout": 30,
                        "statusMessage": "Loading the Superpowers introduction...",
                    }
                ],
            },
        ]
    },
}
KEY = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")


def unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """An object of JSON whose keys are each given once, since a key given twice holds the
    value that a reader of the file may not see."""
    keys = [key for key, _ in pairs]
    twice = sorted({key for key in keys if keys.count(key) > 1})
    if twice:
        raise ValueError(f"the keys {twice} are given twice")
    return dict(pairs)


def settings_problems(found: Any, expected: Any, where: str = "settings") -> list[str]:
    """Each key that a file of settings holds and the test does not list, or lacks, at any
    depth, and each value that differs from the test's in its type or its value."""
    if isinstance(expected, dict) and isinstance(found, dict):
        problems = []
        for key in sorted(found.keys() | expected.keys()):
            at = f"{where}.{key}" if KEY.fullmatch(key) else f"{where}[{json.dumps(key)}]"
            if key not in expected:
                problems.append(f"{at} is a key that the test does not list")
            elif key not in found:
                problems.append(f"{at} is a key that the test lists and the file lacks")
            else:
                problems += settings_problems(found[key], expected[key], at)
        return problems
    if isinstance(expected, list) and isinstance(found, list):
        problems = [
            problem
            for number, (inner, wanted) in enumerate(zip(found, expected, strict=False))
            for problem in settings_problems(inner, wanted, f"{where}[{number}]")
        ]
        if len(found) != len(expected):
            problems.append(
                f"{where} holds {len(found)} items, where the test lists {len(expected)}"
            )
        return problems
    if type(found) is not type(expected) or found != expected:
        return [f"{where} is {json.dumps(found)}, where the test gives {json.dumps(expected)}"]
    return []


def claude_settings() -> Any:
    text = (ROOT / ".claude/settings.json").read_text(encoding="utf-8")
    return json.loads(text, object_pairs_hook=unique_keys)


def test_claude_code_s_settings_here_hold_only_what_this_test_lists() -> None:
    assert settings_problems(claude_settings(), SETTINGS) == []


@pytest.mark.parametrize(
    ("key", "value", "problem"),
    [
        (
            "claudeMdExcludes",
            ["**/CLAUDE.md"],
            "settings.claudeMdExcludes is a key that the test does not list",
        ),
        (
            "permissions",
            {"allow": ["Bash(git push *)"]},
            "settings.permissions is a key that the test does not list",
        ),
    ],
)
def test_a_setting_that_the_test_does_not_list_is_reported(
    key: str, value: Any, problem: str
) -> None:
    assert settings_problems({**SETTINGS, key: value}, SETTINGS) == [problem]


def test_a_variable_a_hook_or_a_key_that_the_test_does_not_list_is_reported() -> None:
    planted = json.loads(json.dumps(SETTINGS))
    planted["env"]["CLAUDE_CODE_DISABLE_CLAUDE_MDS"] = "1"
    planted["hooks"]["PreToolUse"] = [{"hooks": [{"type": "command", "command": "true"}]}]
    planted["hooks"]["SessionStart"][0]["matcher"] = "startup"
    del planted["enabledPlugins"]
    assert settings_problems(planted, SETTINGS) == [
        "settings.enabledPlugins is a key that the test lists and the file lacks",
        "settings.env.CLAUDE_CODE_DISABLE_CLAUDE_MDS is a key that the test does not list",
        "settings.hooks.PreToolUse is a key that the test does not list",
        "settings.hooks.SessionStart[0].matcher is a key that the test does not list",
    ]


def test_a_value_that_the_test_does_not_give_is_reported() -> None:
    planted = json.loads(json.dumps(SETTINGS))
    planted["enabledPlugins"]["superpowers@vendored"] = False
    planted["extraKnownMarketplaces"]["vendored"]["source"]["path"] = "./branch"
    planted["hooks"]["SessionStart"][1]["hooks"][0]["timeout"] = 30.0
    planted["hooks"]["SessionStart"][0]["hooks"][0]["command"] = "bash another.sh"
    planted["hooks"]["SessionStart"].append({"hooks": []})
    assert settings_problems(planted, SETTINGS) == [
        'settings.enabledPlugins["superpowers@vendored"] is false, where the test gives true',
        'settings.extraKnownMarketplaces.vendored.source.path is "./branch", where the test'
        ' gives "."',
        'settings.hooks.SessionStart[0].hooks[0].command is "bash another.sh", where the test'
        ' gives "bash \\"$CLAUDE_PROJECT_DIR\\"/.claude/hooks/session-start.sh"',
        "settings.hooks.SessionStart[1].hooks[0].timeout is 30.0, where the test gives 30",
        "settings.hooks.SessionStart holds 3 items, where the test lists 2",
    ]


def test_an_env_value_of_another_type_is_reported() -> None:
    planted = {**SETTINGS, "env": {**TELEMETRY_SWITCHES, "DO_NOT_TRACK": 1}}
    assert settings_problems(planted, SETTINGS) == [
        'settings.env.DO_NOT_TRACK is 1, where the test gives "1"'
    ]


def test_a_settings_key_given_twice_is_refused() -> None:
    with pytest.raises(ValueError, match=r"the keys \['env'\] are given twice"):
        json.loads('{"env": {}, "env": {"X": "1"}}', object_pairs_hook=unique_keys)


def test_the_settings_that_the_test_lists_pass() -> None:
    assert settings_problems(json.loads(json.dumps(SETTINGS)), SETTINGS) == []


# R256: the marketplace that `.claude/settings.json` names by the folder `.`, whose file is
# `.claude-plugin/marketplace.json`, holds only this, until task 6.7 moves the marketplace that
# loads Superpowers, so that a change to the plugin that a session started in the clone
# installs, or to the folder that it comes from, fails until this test changes with it (T35).
MARKETPLACE = {
    "name": "vendored",
    "description": "Plugins this repository vendors and pins, from local sources only, so a"
    " fresh session loads them without an install step.",
    "owner": {"name": "Niko Kotiniemi"},
    "plugins": [
        {
            "name": "superpowers",
            "description": "Core skills library for Claude Code, vendored at a pinned upstream"
            " sha. See vendor/superpowers/UPSTREAM.lock.",
            "source": "./vendor/superpowers",
        }
    ],
}


def test_the_marketplace_that_the_settings_name_holds_only_what_this_test_lists() -> None:
    settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    assert settings["extraKnownMarketplaces"]["vendored"]["source"]["path"] == "."
    text = (ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
    found = json.loads(text, object_pairs_hook=unique_keys)
    assert settings_problems(found, MARKETPLACE, "marketplace") == []


def test_a_plugin_that_the_marketplace_takes_from_elsewhere_is_reported() -> None:
    planted = json.loads(json.dumps(MARKETPLACE))
    planted["plugins"][0]["source"] = "./tools/plugin"
    planted["plugins"].append({"name": "helper", "source": "./tools/helper"})
    assert settings_problems(planted, MARKETPLACE, "marketplace") == [
        'marketplace.plugins[0].source is "./tools/plugin", where the test gives'
        ' "./vendor/superpowers"',
        "marketplace.plugins holds 2 items, where the test lists 1",
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
    """R223: no switch and no ledger file at the root before task 7.1 turns the tool on,
    whatever the case of their letters, which a file system that ignores case does not
    tell apart."""
    if ticked(root, "7.1"):
        return []
    return [
        f"`{name}` is tracked at the root while task 7.1 of `{BUILD_CHANGE}` is not ticked"
        for name in sorted(tracked(root))
        if name.casefold() == ".pr-cost.json" or name.casefold().startswith(".pr-cost/")
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
        try:
            events = triggers(doc) if isinstance(doc, dict) else set()
        except ValueError:
            problems.append(
                f"`{name}` gives its events in a form that this check cannot read, so it may "
                f"declare `workflow_call` while task 4.3 of `{BUILD_CHANGE}` is not ticked"
            )
            continue
        if "workflow_call" in events:
            problems.append(
                f"`{name}` declares `workflow_call` while task 4.3 of `{BUILD_CHANGE}` is not "
                "ticked"
            )
    return problems


@pytest.mark.parametrize(
    "name",
    [
        ".pr-cost.json",
        ".pr-cost/a-ledger-file",
        ".PR-COST.json",
        ".Pr-Cost/ledger/2026-11/a.jsonl",
        ".pr-co\u017ft.json",
    ],
)
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
        (".github/workflows/ci.yml", "on:\njobs: {}\n"),
        (".github/workflows/ci.yml", ""),
        (".github/workflows/ci.yml", "- workflow_call\n"),
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


# Events given in a form that `triggers` cannot read, which GitHub may read otherwise.
EVENTS_IN_ANOTHER_FORM = [
    "on: !!set {workflow_call}\n",
    "on: [[workflow_call]]\n",
    "on: !!omap [workflow_call: {}]\n",
    "on: !!pairs [workflow_call: {}]\n",
    "on: 5\n",
    "'on': [push, 5]\n",
]


@pytest.mark.parametrize("workflow", EVENTS_IN_ANOTHER_FORM)
def test_a_workflow_whose_events_cannot_be_read_is_named(tmp_path: Path, workflow: str) -> None:
    files: dict[str, str | None] = {
        CHANGE_TASKS: NEITHER_TICKED,
        ".github/workflows/odd.yml": workflow,
    }
    assert reusable_workflow_problems(make_tree(tmp_path, files)) == [
        "`.github/workflows/odd.yml` gives its events in a form that this check cannot read, "
        "so it may declare `workflow_call` while task 4.3 of `add-pr-cost-calculator` is not "
        "ticked"
    ]


@pytest.mark.parametrize("workflow", EVENTS_IN_ANOTHER_FORM)
def test_the_workflow_checks_name_events_that_they_cannot_read(workflow: str) -> None:
    assert workflow_problems("x.yml", workflow + "permissions: write-all\n") == [
        "x.yml gives its events in a form that this check cannot read",
        "x.yml the workflow grants `write-all`",
    ]


def test_this_repository_holds_no_switch_ledger_file_or_reusable_workflow_too_early() -> None:
    """A check that examined nothing fails: the tasks that each check waits for, and the
    workflows that one reads, are found."""
    change = "add-pr-cost-calculator"
    assert {(change, "4.3"), (change, "7.1")} <= tasks(ROOT).keys()
    assert any(name.startswith(".github/workflows/") for name in tracked(ROOT))
    assert capture_file_problems(ROOT) == []
    assert reusable_workflow_problems(ROOT) == []
