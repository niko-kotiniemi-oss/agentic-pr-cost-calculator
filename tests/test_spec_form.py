"""The specs keep the form that OpenSpec reads, as GitHub shows it.

The test reads as specs every `spec.md` that the pinned OpenSpec reads: one in a folder
at any depth below `openspec/specs/`, or below the `specs/` folder of each folder in
`openspec/changes/` but `archive`, that no folder whose name starts with a dot holds
(R177). It fails on a symbolic link anywhere in `openspec/` but the archive, which it
never follows, and on a file named `spec.md` in any case that is not one of those
specs, naming the file, so that no spec escapes it and none of its reads leaves the
repository.

Each spec is checked as plain text before it is split into lines at line feeds alone
(R176, DR-195): bytes that are not UTF-8, a character other than printable ASCII and
the line feed, a run of backticks that no run as long closes on its line, and, outside
inline code, a `<`, an `&`, a backslash, a `|`, a `](`, a `]:`, a `$` or a `~`, with
which GitHub would hide or show text otherwise than OpenSpec and agents read it.

A spec's lines are then read in one pass as OpenSpec reads them (R175, DR-193): an
optional title before any heading, then the sections that OpenSpec reads, `## Purpose`
and `## Requirements` in a main spec, each once, and in a change's spec `## Purpose`,
once, and `## ADDED Requirements`, `## MODIFIED Requirements`, `## REMOVED Requirements`
and `## RENAMED Requirements`, each written as OpenSpec's template writes it. A section
that gives requirements holds blank lines, then `### Requirement: ` headings, each with
its name, its text and its `#### Scenario: ` headings; `RENAMED Requirements` holds only
blank lines and pairs of `FROM:` and `TO:` lines. Any other heading fails, and so does
text other than the title before the first section, a line that starts, after spaces,
tabs or list or quote markers, with `#` or with three backticks or tildes, a line of `=`
or `-` signs alone after any such markers, with which GitHub makes the line above it a
heading, and a line before the first requirement of its section. A closing run of `#`
signs after a space, which GitHub and OpenSpec both leave out of a heading's name, is
allowed, and a title that OpenSpec would read as the Requirements section fails.

Each requirement that a main spec gives, or that a change adds or modifies, has text,
the lines between its heading and its first scenario, that holds SHALL or MUST as a
word, in capitals, and that is 500 characters or fewer, measured on its lines that are
not blank, each trimmed and joined by line feeds (DR-194), and no line that starts with
a bold label and a colon; and it has a scenario (R173). A requirement that a change
removes or renames is not read for its text. Each scenario holds one `- **WHEN**` line
and then one `- **THEN**` line, each followed by any `- **AND**` lines, and a name that
no other scenario of its spec has; and no requirement's text holds a line that starts as
a scenario's lines do (R174). The test fails when it reads no spec, no requirement or no
scenario.

Every problem names the spec as the test found it, and the line, and every name, path or
text that a spec or the file system gives is shown with each character outside printable
ASCII replaced by its code point, so that no line of a spec starts a line of the output
(T126). Each pattern of the reader matches a line in one way only, and is timed here on a
long run of spaces after each shape of line that it reads. The rules are in
`scripts/spec_form.py`, which `scripts/verify-openspec.sh` also runs to compare this
reading with the pinned OpenSpec CLI's (R178, DR-196).

That comparison is tested here on what the pinned CLI printed for four trees, recorded in
`tests/spec_form_openspec.json` with the folder that it ran in and the times at which
each change was last changed left out, and through a stand-in CLI that prints it, so
that no test runs Node. It fails on a spec or a change that only one reading gives,
among them a change's spec from which the test reads no requirement, on the first
difference in each spec's requirements, naming the field, on a call of the CLI that
fails or prints JSON in another form, naming the call, and when it compares no
requirement. A test fails when a tree changes and its recording does not, when the
recording is of another release than the one that `package-lock.json` pins, when it
holds a time of day, and when it lists a tree's changes otherwise than by their names, as
the comparison asks the CLI to list them; this file, run with the CLI's path, rewrites
the recording.
"""

from __future__ import annotations

import copy
import functools
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import pytest
import spec_form
from spec_form import Requirement, Spec, find_specs, problems_in, prose_of, shown

ROOT = Path(__file__).resolve().parents[1]

MAIN_ALPHA = "openspec/specs/alpha/spec.md"
MAIN_BETA = "openspec/specs/area/beta/spec.md"
CHANGE_ALPHA = "openspec/changes/demo/specs/alpha/spec.md"
CHANGE_BETA = "openspec/changes/demo/specs/area/beta/spec.md"
DRAFT_GAMMA = "openspec/changes/draft/specs/gamma/spec.md"

# A main spec as the pinned OpenSpec's `archive` writes it for a new capability.
ALPHA = (
    "# alpha Specification\n"
    "\n"
    "## Purpose\n"
    "What the first capability does.\n"
    "\n"
    "## Requirements\n"
    "\n"
    "### Requirement: The first rule holds\n"
    "\n"
    "The tool SHALL hold the first rule.\n"
    "\n"
    "#### Scenario: The rule holds\n"
    "\n"
    "- **WHEN** the rule is tested\n"
    "- **AND** the test runs again\n"
    "- **THEN** it holds\n"
    "- **AND** it holds again\n"
    "\n"
    "### Requirement: The second rule holds\n"
    "\n"
    "The tool SHALL hold the second rule,\n"
    "over two lines.\n"
    "\n"
    "#### Scenario: The second rule holds\n"
    "\n"
    "- **WHEN** the second rule is tested\n"
    "- **THEN** it holds\n"
)
BETA = (
    "# beta Specification\n"
    "\n"
    "## Purpose\n"
    "What the beta capability does.\n"
    "\n"
    "## Requirements\n"
    "\n"
    "### Requirement: The beta rule holds\n"
    "\n"
    "The tool SHALL hold the beta rule.\n"
    "\n"
    "#### Scenario: The beta rule holds\n"
    "\n"
    "- **WHEN** the beta rule is tested\n"
    "- **THEN** it holds\n"
    "\n"
    "### Requirement: The old rule holds\n"
    "\n"
    "The tool SHALL hold the old rule.\n"
    "\n"
    "#### Scenario: The old rule holds\n"
    "\n"
    "- **WHEN** the old rule is tested\n"
    "- **THEN** it holds\n"
    "\n"
    "### Requirement: The spent rule holds\n"
    "\n"
    "The tool SHALL hold the spent rule.\n"
    "\n"
    "#### Scenario: The spent rule holds\n"
    "\n"
    "- **WHEN** the spent rule is tested\n"
    "- **THEN** it holds\n"
)
# A change's specs in the sections of OpenSpec's template, one of them two folders deep.
ADDED_ALPHA = (
    "## Purpose\n"
    "\n"
    "What the first capability does.\n"
    "\n"
    "## ADDED Requirements\n"
    "\n"
    "### Requirement: The third rule holds\n"
    "\n"
    "The tool SHALL hold the third rule.\n"
    "\n"
    "#### Scenario: The third rule holds\n"
    "\n"
    "- **WHEN** the third rule is tested\n"
    "- **THEN** it holds\n"
)
DELTAS_BETA = (
    "## Purpose\n"
    "\n"
    "What the beta capability does.\n"
    "\n"
    "## ADDED Requirements\n"
    "\n"
    "### Requirement: The new beta rule holds\n"
    "\n"
    "The tool SHALL hold the new beta rule.\n"
    "\n"
    "#### Scenario: The new beta rule holds\n"
    "\n"
    "- **WHEN** the new beta rule is tested\n"
    "- **THEN** it holds\n"
    "\n"
    "## MODIFIED Requirements\n"
    "\n"
    "### Requirement: The beta rule holds\n"
    "\n"
    "The tool SHALL hold the beta rule, and say so.\n"
    "\n"
    "#### Scenario: The beta rule holds\n"
    "\n"
    "- **WHEN** the beta rule is tested\n"
    "- **THEN** it holds and says so\n"
    "\n"
    "## REMOVED Requirements\n"
    "\n"
    "### Requirement: The spent rule holds\n"
    "\n"
    "**Reason**: The new beta rule replaces it.\n"
    "\n"
    "**Migration**: Hold the new beta rule.\n"
    "\n"
    "## RENAMED Requirements\n"
    "\n"
    "- FROM: `### Requirement: The old rule holds`\n"
    "- TO: `### Requirement: The renamed rule holds`\n"
)
GAMMA = (
    "## Purpose\n"
    "\n"
    "What the gamma capability does.\n"
    "\n"
    "## ADDED Requirements\n"
    "\n"
    "### Requirement: The gamma rule holds\n"
    "\n"
    "The tool SHALL hold the gamma rule.\n"
    "\n"
    "#### Scenario: The gamma rule holds\n"
    "\n"
    "- **WHEN** the gamma rule is tested\n"
    "- **THEN** it holds\n"
)
PROPOSAL = (
    "## Why\n"
    "\n"
    "A demonstration of each section that a change's spec gives, for the tests.\n"
    "\n"
    "## What Changes\n"
    "\n"
    "- The first capability gains a rule, and the beta capability changes.\n"
)
# Two main specs, one two folders deep; a change with a proposal; and a change with none.
PASSING = {
    "openspec/config.yaml": "schema: spec-driven\n",
    MAIN_ALPHA: ALPHA,
    MAIN_BETA: BETA,
    "openspec/changes/demo/.openspec.yaml": "schema: spec-driven\ncreated: 2026-11-09\n",
    "openspec/changes/demo/proposal.md": PROPOSAL,
    CHANGE_ALPHA: ADDED_ALPHA,
    CHANGE_BETA: DELTAS_BETA,
    DRAFT_GAMMA: GAMMA,
}


def tree(root: Path, files: Mapping[str, str | bytes]) -> Path:
    """A folder holding these files, each written as these bytes or this text in UTF-8,
    with no line ending changed."""
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode())
    return root


def passing(root: Path, changes: dict[str, str | bytes] | None = None) -> Path:
    return tree(root, {**PASSING, **(changes or {})})


def planted(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"{old!r} is not in the text exactly once"
    return text.replace(old, new)


def line(text: str, start: str, after: int = 0) -> int:
    """The number of the first line of the text that starts with this, after line `after`."""
    numbers = [
        number
        for number, content in enumerate(text.split("\n"), 1)
        if number > after and content.startswith(start)
    ]
    assert numbers, f"no line starts with {start!r}"
    return numbers[0]


def problems_of(root: Path, path: str, text: str | bytes) -> list[str]:
    return problems_in(passing(root, {path: text}))


# The files that the test reads (R177).


def test_the_passing_tree_has_no_problem(tmp_path: Path) -> None:
    assert problems_in(passing(tmp_path)) == []


def test_each_spec_that_openspec_reads_is_found_with_its_id(tmp_path: Path) -> None:
    assert find_specs(passing(tmp_path)) == (
        [
            Spec(CHANGE_ALPHA, "demo", "alpha"),
            Spec(CHANGE_BETA, "demo", "area/beta"),
            Spec(DRAFT_GAMMA, "draft", "gamma"),
            Spec(MAIN_ALPHA, "", "alpha"),
            Spec(MAIN_BETA, "", "area/beta"),
        ],
        [],
    )


SCENARIO_WITHOUT_THEN = 'scenario "{}" of requirement "{}" has no THEN line'


@pytest.mark.parametrize(
    ("path", "text", "then", "scenario", "requirement"),
    [
        (
            MAIN_BETA,
            BETA,
            "- **THEN** it holds\n\n### Requirement: The old",
            "The beta rule holds",
            "The beta rule holds",
        ),
        (
            CHANGE_BETA,
            DELTAS_BETA,
            "- **THEN** it holds and says so\n",
            "The beta rule holds",
            "The beta rule holds",
        ),
        (
            DRAFT_GAMMA,
            GAMMA,
            "- **THEN** it holds\n",
            "The gamma rule holds",
            "The gamma rule holds",
        ),
    ],
)
def test_a_spec_in_a_deeper_folder_is_read(
    tmp_path: Path, path: str, text: str, then: str, scenario: str, requirement: str
) -> None:
    kept = then.split("\n", 1)[1]
    defect = planted(text, then, kept)
    heading = line(defect, f"#### Scenario: {scenario}")
    assert problems_of(tmp_path, path, defect) == [
        f"{path}:{heading}: " + SCENARIO_WITHOUT_THEN.format(scenario, requirement)
    ]


@pytest.mark.parametrize(
    ("path", "reason"),
    [
        ("openspec/specs/spec.md", "it stands at the top of a specs folder"),
        ("openspec/changes/demo/specs/spec.md", "it stands at the top of a specs folder"),
        ("openspec/changes/demo/spec.md", "it stands outside the specs folders"),
        ("openspec/spec.md", "it stands outside the specs folders"),
        ("openspec/changes/demo/notes/alpha/spec.md", "it stands outside the specs folders"),
        ("openspec/specs/.hidden/spec.md", "a folder whose name starts with a dot holds it"),
        (
            "openspec/specs/area/.hidden/beta/spec.md",
            "a folder whose name starts with a dot holds it",
        ),
        (
            "openspec/changes/.hidden/specs/alpha/spec.md",
            "a folder whose name starts with a dot holds it",
        ),
        (
            "openspec/changes/demo/specs/.hidden/spec.md",
            "a folder whose name starts with a dot holds it",
        ),
        ("openspec/specs/delta/SPEC.md", "OpenSpec reads only a file named spec.md"),
        ("openspec/changes/demo/specs/delta/Spec.md", "OpenSpec reads only a file named spec.md"),
    ],
)
def test_a_spec_that_the_test_does_not_read_fails(tmp_path: Path, path: str, reason: str) -> None:
    assert problems_of(tmp_path, path, ALPHA) == [f"{path}: is not read as a spec: {reason}"]


def test_the_archive_is_not_read(tmp_path: Path) -> None:
    archived = "openspec/changes/archive/2026-01-01-old"
    root = passing(
        tmp_path, {f"{archived}/specs/alpha/spec.md": "## Notes\n", f"{archived}/spec.md": ""}
    )
    (root / archived / "specs" / "link").symlink_to(root / MAIN_ALPHA)
    assert problems_in(root) == []


def test_each_folder_in_the_changes_but_the_archive_and_a_dot_folder_is_a_change(
    tmp_path: Path,
) -> None:
    root = passing(
        tmp_path,
        {
            "openspec/changes/archive/2026-01-01-old/proposal.md": PROPOSAL,
            "openspec/changes/.draft/proposal.md": PROPOSAL,
            "openspec/changes/notes.md": "",
        },
    )
    (root / "openspec/changes/linked").symlink_to(root / "openspec/changes/demo")
    assert spec_form.changes_in(root) == {"demo", "draft"}


@pytest.mark.parametrize("link", ["openspec", "openspec/changes"])
def test_no_change_is_read_through_a_symbolic_link(tmp_path: Path, link: str) -> None:
    real = passing(tmp_path / "real")
    root = tmp_path / "root"
    (root / link).parent.mkdir(parents=True)
    (root / link).symlink_to(real / link)
    assert spec_form.changes_in(root) == frozenset()


DEFECTIVE = planted(ALPHA, "- **THEN** it holds\n- **AND** it holds again\n", "")


def test_a_symbolic_link_that_is_a_spec_fails_and_is_not_followed(tmp_path: Path) -> None:
    root = passing(tmp_path / "repository")
    outside = tree(tmp_path / "outside", {"spec.md": DEFECTIVE})
    (root / "openspec/specs/linked").mkdir()
    (root / "openspec/specs/linked/spec.md").symlink_to(outside / "spec.md")
    assert problems_in(root) == [
        "openspec/specs/linked/spec.md: is a symbolic link, which the test does not follow"
    ]


def test_a_symbolic_link_that_is_a_folder_fails_and_is_not_followed(tmp_path: Path) -> None:
    root = passing(tmp_path / "repository")
    outside = tree(tmp_path / "outside", {"linked/spec.md": DEFECTIVE})
    (root / "openspec/changes/demo/specs/linked").symlink_to(outside / "linked")
    assert problems_in(root) == [
        "openspec/changes/demo/specs/linked: is a symbolic link, which the test does not follow"
    ]


def test_a_symbolic_link_to_the_whole_folder_fails_and_is_not_followed(tmp_path: Path) -> None:
    outside = passing(tmp_path / "outside", {MAIN_ALPHA: DEFECTIVE})
    root = tmp_path / "repository"
    root.mkdir()
    (root / "openspec").symlink_to(outside / "openspec")
    assert problems_in(root) == [
        "openspec: is a symbolic link, which the test does not follow",
        "openspec/: holds no spec that OpenSpec reads",
    ]


def test_a_spec_that_is_not_a_regular_file_is_not_read(tmp_path: Path) -> None:
    root = passing(tmp_path)
    (root / "openspec/specs/pipe").mkdir()
    os.mkfifo(root / "openspec/specs/pipe/spec.md")
    assert problems_in(root) == [
        "openspec/specs/pipe/spec.md: is not read as a spec: it is not a regular file"
    ]


def test_a_tree_with_no_spec_fails(tmp_path: Path) -> None:
    root = tree(tmp_path, {"openspec/config.yaml": "schema: spec-driven\n"})
    assert problems_in(root) == ["openspec/: holds no spec that OpenSpec reads"]
    assert problems_in(tmp_path / "nothing") == ["openspec/: holds no spec that OpenSpec reads"]


# Plain text (R176).

TEXT = "The tool SHALL hold the first rule."


@pytest.mark.parametrize(
    ("new", "shown_as"),
    [
        (f"{TEXT}\r", "U+000D"),
        (f"{TEXT}\f", "U+000C"),
        (f"{TEXT}\t", "U+0009"),
        ("The tool SHALL hold the first\u0085rule.", "U+0085"),
        ("The tool SHALL hold the first\u2028rule.", "U+2028"),
        ("The tool SHALL hold the first\u00a0rule.", "U+00A0"),
        ("The tool SHALL hold the \u201cfirst\u201d rule.", "U+201C"),
    ],
)
def test_a_character_other_than_printable_ascii_fails(
    tmp_path: Path, new: str, shown_as: str
) -> None:
    number = line(ALPHA, TEXT)
    assert problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, new)) == [
        f"{MAIN_ALPHA}:{number}: holds {shown_as}, which is not printable ASCII or a line feed"
    ]


# OpenSpec reads the lines after the mark, a title or a section among them.
@pytest.mark.parametrize(
    ("path", "spec"),
    [(MAIN_ALPHA, ALPHA), (CHANGE_ALPHA, ADDED_ALPHA)],
    ids=["a main spec", "a change's spec"],
)
def test_a_byte_order_mark_fails(tmp_path: Path, path: str, spec: str) -> None:
    assert problems_of(tmp_path, path, "\ufeff" + spec) == [
        f"{path}:1: holds U+FEFF, which is not printable ASCII or a line feed"
    ]


def test_bytes_that_are_not_utf_8_fail_naming_the_line(tmp_path: Path) -> None:
    number = line(ALPHA, TEXT)
    defect = planted(ALPHA, TEXT, "The tool SHALL hold the first rule\udcff.").encode(
        errors="surrogateescape"
    )
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{number}: holds bytes that are not UTF-8"
    ]


@pytest.mark.parametrize(
    ("new", "mark"),
    [
        ("The tool SHALL hold the first rule, if a < b.", "<"),
        ("The tool SHALL hold the first rule <!-- and hide this -->.", "<"),
        ("The tool SHALL hold the first rule, and its kin.", None),
        ("The tool SHALL hold the first rule &amp; the second.", "&"),
        ("The tool SHALL hold the first rule & the second.", "&"),
        ("The tool SHALL hold the first rule \\* twice.", "\\"),
        ("| The tool SHALL hold the first rule. | x |", "|"),
        ("The tool SHALL hold the [first rule](https://example.com).", "]("),
        ("The tool SHALL hold the [first rule][rule].", None),
        ("- [rule]: https://example.com The tool SHALL hold the first rule.", "]:"),
        ("The tool SHALL hold the first rule.[^1]", None),
        ("[^1]: The tool SHALL hold the first rule.", "]:"),
        ("The tool SHALL hold the first rule $n$ times.", "$"),
        ("The tool SHALL hold the first rule for $5.", "$"),
        ("The tool SHALL hold the ~~first~~ rule.", "~"),
        ("The tool SHALL hold the first rule ~once~.", "~"),
        ("The tool SHALL hold the first rule for ~5 days.", "~"),
    ],
)
def test_a_mark_that_github_reads_outside_inline_code_fails(
    tmp_path: Path, new: str, mark: str | None
) -> None:
    number = line(ALPHA, TEXT)
    expected = (
        [] if mark is None else [f'{MAIN_ALPHA}:{number}: holds "{mark}" outside inline code']
    )
    assert problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, new)) == expected


def test_each_mark_on_a_line_is_named_once(tmp_path: Path) -> None:
    number = line(ALPHA, TEXT)
    new = "The tool SHALL hold | the first | rule <here> & <there>, \\o/ [a](b) [c]: d, $e$ ~f~."
    assert problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, new)) == [
        f'{MAIN_ALPHA}:{number}: holds "{mark}" outside inline code'
        for mark in ("<", "&", "\\", "|", "](", "]:", "$", "~")
    ]


def test_those_marks_pass_inside_inline_code(tmp_path: Path) -> None:
    new = "The tool SHALL hold `<` `&` `\\` `|` `](` `]:` `$` `~` and ``a ` b``, in `<!-- x -->`."
    assert problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, new)) == []


def test_inline_code_that_runs_onto_the_next_line_fails(tmp_path: Path) -> None:
    number = line(ALPHA, TEXT)
    new = "The tool SHALL hold `the first\nrule` and ``the second\nrule``."
    assert problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, new)) == [
        f"{MAIN_ALPHA}:{number + offset}: holds a run of backticks, {length} long, that no run"
        " as long closes on its line"
        for offset, length in ((0, 1), (1, 1), (2, 2))
    ]


def test_a_run_of_backticks_that_a_shorter_run_follows_is_not_closed(tmp_path: Path) -> None:
    number = line(ALPHA, TEXT)
    new = "The tool SHALL hold ```the first`` rule."
    assert problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, new)) == [
        f"{MAIN_ALPHA}:{number}: holds a run of backticks, 3 long, that no run as long"
        " closes on its line",
    ]


def test_the_prose_of_a_line_leaves_out_its_code_spans() -> None:
    assert prose_of("a `b` c ``d`` e ` f") == (["a ", " c ", " e ` f"], [1])
    assert prose_of("```") == (["```"], [3])
    assert prose_of("``a`b``") == (["", ""], [])


def test_a_text_is_shown_in_printable_ascii() -> None:
    assert shown("a\nb\r\u00e9\u2028`|") == "aU+000AbU+000DU+00E9U+2028`|"
    assert shown("\U0001f600") == "U+1F600"


# Headings and lines (R175).

FIRST = "### Requirement: The first rule holds"
SECOND = "### Requirement: The second rule holds"
SCENARIO = "#### Scenario: The rule holds"
HASH = 'starts with "#", after any list or quote markers, but is not a heading in form'
FENCE = "starts with three backticks or tildes, after any list or quote markers, as a fence does"
UNDERLINE = (
    'holds only "=" or "-" signs after any list or quote markers, with which GitHub can make'
    " the line above it a heading"
)
BEFORE = "stands before the first requirement of its section"
FIRST_SECTION = "stands before the spec's first section"
RUN_3 = "holds a run of backticks, 3 long, that no run as long closes on its line"
NO_SHALL = (
    f'{MAIN_ALPHA}:{line(ALPHA, FIRST)}: requirement "The first rule holds" holds neither'
    " SHALL nor MUST in its text"
)


# What follows a requirement's heading out of form: its lines stand before the first
# requirement of the section, and its scenario's heading outside a requirement.
CASCADE_OF_REQUIREMENT = [(10, BEFORE), (12, "is a scenario's heading outside a requirement")] + [
    (number, BEFORE) for number in (14, 15, 16, 17)
]


@pytest.mark.parametrize(
    ("heading", "first"),
    [
        ("Requirement: The first rule holds", BEFORE),
        ("**Requirement: The first rule holds**", BEFORE),
        ("#### Requirement: The first rule holds", HASH),
        ("### The first rule holds", HASH),
        ("###Requirement: The first rule holds", HASH),
        ("   ### Requirement: The first rule holds", HASH),
        ("### requirement: The first rule holds", HASH),
        ("### Requirement:The first rule holds", HASH),
        ("### Requirement:  The first rule holds", None),
    ],
)
def test_a_requirement_s_heading_out_of_form_fails(
    tmp_path: Path, heading: str, first: str | None
) -> None:
    defect = planted(ALPHA, FIRST, heading)
    expected = [] if first is None else [(8, first), *CASCADE_OF_REQUIREMENT]
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{number}: {message}" for number, message in expected
    ]


def test_a_requirement_s_heading_made_a_section_fails(tmp_path: Path) -> None:
    defect = planted(ALPHA, FIRST, "## Requirement: The first rule holds")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f'{MAIN_ALPHA}:8: is a section, "Requirement: The first rule holds", that OpenSpec does'
        " not read in a main spec"
    ]


# What follows a scenario's heading out of form: the requirement has no scenario, and its
# scenario's lines stand in the requirement's text.
CASCADE_OF_SCENARIO = [
    (number, 'requirement "The first rule holds" holds a scenario\'s line in its text')
    for number in (14, 15, 16, 17)
]


@pytest.mark.parametrize(
    ("heading", "flagged"),
    [
        ("Scenario: The rule holds", False),
        ("**Scenario: The rule holds**", False),
        ("### Scenario: The rule holds", True),
        ("##### Scenario: The rule holds", True),
        ("#### The rule holds", True),
        ("####Scenario: The rule holds", True),
        ("  #### Scenario: The rule holds", True),
        ("#### scenario: The rule holds", True),
    ],
)
def test_a_scenario_s_heading_out_of_form_fails(
    tmp_path: Path, heading: str, flagged: bool
) -> None:
    defect = planted(ALPHA, SCENARIO, heading)
    expected = [
        (8, 'requirement "The first rule holds" has no scenario'),
        *([(12, HASH)] if flagged else []),
        *CASCADE_OF_SCENARIO,
    ]
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{number}: {message}" for number, message in expected
    ]


@pytest.mark.parametrize(
    "heading",
    [
        "### Requirement:",
        "### Requirement: ",
        "### Requirement:   ",
        "### Requirement: #",
        "### Requirement: ###   ",
    ],
)
def test_a_requirement_s_heading_without_a_name_fails(tmp_path: Path, heading: str) -> None:
    defect = planted(ALPHA, FIRST, heading)
    assert problems_of(tmp_path, MAIN_ALPHA, defect)[:1] == [
        f"{MAIN_ALPHA}:{line(ALPHA, FIRST)}: is a requirement's heading without a name"
    ]


@pytest.mark.parametrize("heading", ["#### Scenario:", "#### Scenario: ", "#### Scenario: #"])
def test_a_scenario_s_heading_without_a_name_fails(tmp_path: Path, heading: str) -> None:
    defect = planted(ALPHA, SCENARIO, heading)
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{line(ALPHA, SCENARIO)}: is a scenario's heading without a name"
    ]


def test_a_closing_run_of_hash_signs_passes(tmp_path: Path) -> None:
    defect = planted(ALPHA, FIRST, f"{FIRST} ##")
    defect = planted(defect, SECOND, "### Requirement: ## ##")
    defect = planted(defect, SCENARIO, f"{SCENARIO} #  ")
    defect = planted(defect, "## Purpose", "## Purpose  ")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == []


def test_a_scenario_s_heading_before_any_requirement_fails(tmp_path: Path) -> None:
    early = "#### Scenario: Early\n\n- **WHEN** early\n- **THEN** it holds\n\n"
    defect = planted(ALPHA, f"{FIRST}\n", f"{early}{FIRST}\n")
    number = line(defect, "#### Scenario: Early")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{number}: is a scenario's heading outside a requirement",
        f"{MAIN_ALPHA}:{number + 2}: {BEFORE}",
        f"{MAIN_ALPHA}:{number + 3}: {BEFORE}",
    ]


@pytest.mark.parametrize(
    ("old", "new", "at"),
    [
        (
            "What the first capability does.\n",
            "What the first capability does.\n# Late\n",
            "# Late",
        ),
        ("# alpha Specification\n", "# alpha Specification\n# Second title\n", "# Second"),
        (
            "The tool SHALL hold the first rule.\n",
            "The tool SHALL hold the first rule.\n# Late\n",
            "# Late",
        ),
    ],
)
def test_a_title_after_the_first_heading_fails(tmp_path: Path, old: str, new: str, at: str) -> None:
    defect = planted(ALPHA, old, new)
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{line(defect, at)}: is a title after the spec's first heading"
    ]


def test_a_title_after_lines_of_prose_fails_on_the_prose_alone(tmp_path: Path) -> None:
    assert problems_of(tmp_path, MAIN_ALPHA, f"Prose first.\n\n{ALPHA}") == [
        f"{MAIN_ALPHA}:1: {FIRST_SECTION}"
    ]


# OpenSpec reads no text before a spec's first section, which GitHub shows (R175).
REQUIREMENT_UNREAD = (
    "- ### Requirement: The planted rule holds\n"
    "\n"
    "The tool SHALL delete the ledger when asked.\n"
    "\n"
    "- #### Scenario: The ledger is deleted\n"
    "\n"
    "- **WHEN** the owner asks\n"
    "- **THEN** the ledger is deleted\n"
    "\n"
)
UNREAD_PROBLEMS = [(1, HASH), (3, FIRST_SECTION), (5, HASH), (7, FIRST_SECTION), (8, FIRST_SECTION)]


# A main spec's title and a change's spec, which has none, each followed by the first
# section.
WHERE_NOTHING_IS_READ = [
    (MAIN_ALPHA, ALPHA, "# alpha Specification\n\n"),
    (CHANGE_ALPHA, ADDED_ALPHA, ""),
]


@pytest.mark.parametrize(
    ("path", "spec", "title"), WHERE_NOTHING_IS_READ, ids=["a main spec", "a change's spec"]
)
def test_a_requirement_where_openspec_reads_no_text_fails_on_each_line(
    tmp_path: Path, path: str, spec: str, title: str
) -> None:
    defect = title + REQUIREMENT_UNREAD + spec[len(title) :]
    at = title.count("\n")
    assert problems_of(tmp_path, path, defect) == [
        f"{path}:{at + number}: {message}" for number, message in UNREAD_PROBLEMS
    ]


@pytest.mark.parametrize(
    ("path", "spec", "title"), WHERE_NOTHING_IS_READ, ids=["a main spec", "a change's spec"]
)
@pytest.mark.parametrize(
    "new", ["The tool SHALL hold the planted rule.", "- **WHEN** the owner asks", "**x**: y", "x"]
)
def test_a_line_before_a_spec_s_first_section_fails(
    tmp_path: Path, path: str, spec: str, title: str, new: str
) -> None:
    defect = f"{title}{new}\n\n{spec[len(title) :]}"
    at = title.count("\n")
    assert problems_of(tmp_path, path, defect) == [f"{path}:{at + 1}: {FIRST_SECTION}"]


@pytest.mark.parametrize("before", ["", "\n", "\n\n", "  \n", " \n\n   \n"])
def test_blank_lines_before_a_spec_s_first_section_pass(tmp_path: Path, before: str) -> None:
    assert problems_of(tmp_path, CHANGE_ALPHA, before + ADDED_ALPHA) == []
    assert problems_of(tmp_path, MAIN_ALPHA, before + ALPHA) == []


@pytest.mark.parametrize("title", ["# Requirements", "# requirements  ", "# REQUIREMENTS"])
def test_a_title_that_openspec_reads_as_the_requirements_section_fails(
    tmp_path: Path, title: str
) -> None:
    defect = planted(ALPHA, "# alpha Specification", title)
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:1: is a title that OpenSpec reads as the Requirements section"
    ]


def test_a_change_s_spec_may_have_a_title_of_any_text(tmp_path: Path) -> None:
    assert problems_of(tmp_path, CHANGE_ALPHA, f"# Requirements\n\n{ADDED_ALPHA}") == []


@pytest.mark.parametrize(
    ("path", "text", "section", "kind"),
    [
        (MAIN_ALPHA, ALPHA, "Notes", "a main spec"),
        (MAIN_ALPHA, ALPHA, "ADDED Requirements", "a main spec"),
        (MAIN_ALPHA, ALPHA, "Requirements:", "a main spec"),
        (MAIN_ALPHA, ALPHA, "Purpose and scope", "a main spec"),
        (CHANGE_ALPHA, ADDED_ALPHA, "Notes", "a change's spec"),
        (CHANGE_ALPHA, ADDED_ALPHA, "Requirements", "a change's spec"),
        (CHANGE_ALPHA, ADDED_ALPHA, "ADDED  Requirements", "a change's spec"),
    ],
)
def test_a_section_that_openspec_does_not_read_fails(
    tmp_path: Path, path: str, text: str, section: str, kind: str
) -> None:
    defect = f"{text}\n## {section}\n\n{text[text.index('### Requirement') :]}"
    number = line(defect, f"## {section}", after=3)
    assert problems_of(tmp_path, path, defect) == [
        f'{path}:{number}: is a section, "{section}", that OpenSpec does not read in {kind}'
    ]


@pytest.mark.parametrize(
    ("path", "text", "section", "written"),
    [
        (MAIN_ALPHA, ALPHA, "requirements", "Requirements"),
        (MAIN_ALPHA, ALPHA, "REQUIREMENTS", "Requirements"),
        (CHANGE_ALPHA, ADDED_ALPHA, "Added Requirements", "ADDED Requirements"),
        (CHANGE_ALPHA, ADDED_ALPHA, "added requirements", "ADDED Requirements"),
        (CHANGE_ALPHA, ADDED_ALPHA, "PURPOSE", "Purpose"),
    ],
)
def test_a_section_that_openspec_reads_in_another_spelling_fails(
    tmp_path: Path, path: str, text: str, section: str, written: str
) -> None:
    defect = f"{text}\n## {section}\n\n{text[text.index('### Requirement') :]}"
    number = line(defect, f"## {section}", after=3)
    assert problems_of(tmp_path, path, defect) == [
        f'{path}:{number}: gives the section "{written}" as "{section}", not as its template'
        " writes it"
    ]


@pytest.mark.parametrize(
    ("path", "text", "section"),
    [
        (MAIN_ALPHA, ALPHA, "Purpose"),
        (MAIN_ALPHA, ALPHA, "Requirements"),
        (CHANGE_ALPHA, ADDED_ALPHA, "Purpose"),
    ],
)
def test_a_section_given_twice_fails(tmp_path: Path, path: str, text: str, section: str) -> None:
    again = f"## {section}\n\n{text[text.index('### Requirement') :]}"
    defect = f"{text}\n{again}"
    number = line(defect, f"## {section}", after=line(text, "- **THEN**"))
    assert problems_of(tmp_path, path, defect) == [
        f'{path}:{number}: gives the section "{section}" a second time'
    ]


def test_a_change_s_section_given_twice_is_read_twice(tmp_path: Path) -> None:
    again = ADDED_ALPHA[ADDED_ALPHA.index("## ADDED") :].replace("third", "fourth")
    assert problems_of(tmp_path, CHANGE_ALPHA, f"{ADDED_ALPHA}\n{again}") == []


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("## Purpose\n", "## Purpose\n### Requirement: Early\n"),
        ("# alpha Specification\n", "# alpha Specification\n### Requirement: Early\n"),
    ],
)
def test_a_requirement_s_heading_outside_a_section_that_gives_them_fails(
    tmp_path: Path, old: str, new: str
) -> None:
    defect = planted(ALPHA, old, new)
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{line(defect, '### Requirement: Early')}: is a requirement's heading"
        " outside a section that gives requirements"
    ]


def test_a_requirement_s_heading_in_renamed_requirements_fails(tmp_path: Path) -> None:
    defect = f"{DELTAS_BETA}\n### Requirement: Late\n"
    assert problems_of(tmp_path, CHANGE_BETA, defect) == [
        f"{CHANGE_BETA}:{line(defect, '### Requirement: Late')}: is a requirement's heading"
        " outside a section that gives requirements"
    ]


@pytest.mark.parametrize(
    "new",
    [
        "#hashtag The tool SHALL hold the first rule.",
        "# The tool SHALL hold the first rule.",
        "##  The tool SHALL hold the first rule.",
        "## ",
        "  # The tool SHALL hold the first rule.",
        "##### The tool SHALL hold the first rule.",
        "####### The tool SHALL hold the first rule.",
        "\t### The tool SHALL hold the first rule.",
    ],
)
def test_any_other_line_that_starts_with_a_hash_sign_fails(tmp_path: Path, new: str) -> None:
    problems = problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, new))
    number = line(ALPHA, TEXT)
    if new.startswith("# "):
        assert problems == [
            NO_SHALL,
            f"{MAIN_ALPHA}:{number}: is a title after the spec's first heading",
        ]
    elif new == "## ":
        assert problems == [NO_SHALL, f"{MAIN_ALPHA}:{number}: {HASH}"]
    elif new.startswith("\t"):
        assert problems[:1] == [
            f"{MAIN_ALPHA}:{number}: holds U+0009, which is not printable ASCII or a line feed"
        ]
        assert f"{MAIN_ALPHA}:{number}: {HASH}" in problems
    else:
        assert problems[:1] == [f"{MAIN_ALPHA}:{number}: {HASH}"]


# GitHub shows a heading or a fence after list or quote markers inside the list item or
# the quote, where OpenSpec, which takes headings and fences from the start of a line
# alone, reads text (R175).
@pytest.mark.parametrize(
    "new",
    [
        "- ### Requirement: The planted rule holds",
        "* #### Scenario: The planted scenario",
        "+ ### Requirement: The planted rule holds",
        "1. ### Requirement: The planted rule holds",
        "12) #### Scenario: The planted scenario",
        "> #### Scenario: The planted scenario",
        ">### Requirement: The planted rule holds",
        "  - > 1. ## Purpose",
        "-   # The planted title",
        "- #hashtag",
    ],
)
def test_a_heading_after_list_or_quote_markers_fails(tmp_path: Path, new: str) -> None:
    defect = planted(ALPHA, f"{TEXT}\n", f"{TEXT}\n{new}\n")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{line(ALPHA, TEXT) + 1}: {HASH}"
    ]


@pytest.mark.parametrize("new", ["- ```", "> ~~~ a tilde fence", "1. ```` four"])
def test_a_fence_after_list_or_quote_markers_fails(tmp_path: Path, new: str) -> None:
    defect = planted(ALPHA, f"{TEXT}\n", f"{TEXT}\n{new}\n")
    problems = problems_of(tmp_path, MAIN_ALPHA, defect)
    assert f"{MAIN_ALPHA}:{line(ALPHA, TEXT) + 1}: {FENCE}" in problems


@pytest.mark.parametrize(
    "new",
    [
        "- a list item with `#` in inline code",
        "1. a numbered item that names #19",
        "> a quote",
        "-- two signs, which open no list",
        "2026-11-09 is a date",
    ],
)
def test_a_list_item_or_a_quote_without_a_heading_passes(tmp_path: Path, new: str) -> None:
    defect = planted(ALPHA, f"{TEXT}\n", f"{TEXT}\n{new}\n")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == []


@pytest.mark.parametrize("signs", ["===", "---", "-", "= =", "- - -", "=-=", "  ==  "])
def test_a_line_of_equals_or_minus_signs_fails(tmp_path: Path, signs: str) -> None:
    defect = planted(ALPHA, f"{TEXT}\n", f"{TEXT}\n{signs}\n")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{line(ALPHA, TEXT) + 1}: {UNDERLINE}"
    ]


# In a quote, GitHub makes the line above such signs a heading too (R175).
@pytest.mark.parametrize("signs", ["> ---", ">===", "> > -", "> - ", ">  = ="])
def test_a_line_of_signs_after_list_or_quote_markers_fails(tmp_path: Path, signs: str) -> None:
    defect = planted(ALPHA, f"{TEXT}\n", f"{TEXT}\n{signs}\n")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{line(ALPHA, TEXT) + 1}: {UNDERLINE}"
    ]


@pytest.mark.parametrize(
    ("new", "fences", "runs"),
    [
        (f"{TEXT}\n```\ncode\n```", [1, 3], [1, 3]),
        (f"{TEXT}\n~~~\ncode\n~~~", [1, 3], []),
        (f"{TEXT}\n<!--\n```\n-->", [2], [2]),
        (f"{TEXT}\n```code``` is a code span", [1], []),
        (f"{TEXT}\n    ```", [1], [1]),
        (f"{TEXT}\n\t~~~~ a tilde fence", [1], []),
        (f"{TEXT}\n  `````", [1], [1]),
    ],
)
def test_a_line_that_openspec_reads_as_a_fence_fails(
    tmp_path: Path, new: str, fences: list[int], runs: list[int]
) -> None:
    number = line(ALPHA, TEXT)
    problems = problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, new))
    for offset in fences:
        assert f"{MAIN_ALPHA}:{number + offset}: {FENCE}" in problems
    found_runs = [problem for problem in problems if "a run of backticks" in problem]
    assert len(found_runs) == len(runs)


def test_a_pair_of_fence_lines_across_two_requirements_fails(tmp_path: Path) -> None:
    defect = planted(ALPHA, f"{TEXT}\n", f"{TEXT}\n```\n")
    defect = planted(defect, "over two lines.\n", "over two lines.\n```\n")
    problems = problems_of(tmp_path, MAIN_ALPHA, defect)
    assert problems == [
        f"{MAIN_ALPHA}:{line(defect, '```')}: {RUN_3}",
        f"{MAIN_ALPHA}:{line(defect, '```')}: {FENCE}",
        f"{MAIN_ALPHA}:{line(defect, '```', after=line(defect, '```'))}: {RUN_3}",
        f"{MAIN_ALPHA}:{line(defect, '```', after=line(defect, '```'))}: {FENCE}",
    ]


def test_a_fence_pair_inside_html_comments_fails(tmp_path: Path) -> None:
    hidden = "<!--\n```\n-->\n\n"
    defect = planted(ALPHA, f"{FIRST}\n", f"{hidden}{FIRST}\n")
    defect = planted(defect, f"{SECOND}\n", f"{hidden}{SECOND}\n")
    first, second = (number for number, text in enumerate(defect.split("\n"), 1) if text == "```")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f'{MAIN_ALPHA}:{first - 1}: holds "<" outside inline code',
        f"{MAIN_ALPHA}:{first - 1}: {BEFORE}",
        f"{MAIN_ALPHA}:{first}: {RUN_3}",
        f"{MAIN_ALPHA}:{first}: {FENCE}",
        f"{MAIN_ALPHA}:{first + 1}: {BEFORE}",
        f'{MAIN_ALPHA}:{second - 1}: holds "<" outside inline code',
        f'{MAIN_ALPHA}:{second - 1}: scenario "The rule holds" of requirement "The first rule'
        ' holds" holds a line other than a WHEN, a THEN or an AND line',
        f"{MAIN_ALPHA}:{second}: {RUN_3}",
        f"{MAIN_ALPHA}:{second}: {FENCE}",
        f'{MAIN_ALPHA}:{second + 1}: scenario "The rule holds" of requirement "The first rule'
        ' holds" holds a line other than a WHEN, a THEN or an AND line',
    ]


def test_a_line_before_the_first_requirement_of_its_section_fails(tmp_path: Path) -> None:
    defect = planted(ALPHA, f"{FIRST}\n", f"The rules follow.\n\n{FIRST}\n")
    removed = planted(
        DELTAS_BETA,
        "### Requirement: The spent",
        "The spent rule goes.\n### Requirement: The spent",
    )
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{line(defect, 'The rules follow.')}: {BEFORE}"
    ]
    assert problems_of(tmp_path, CHANGE_BETA, removed) == [
        f"{CHANGE_BETA}:{line(removed, 'The spent rule goes.')}: {BEFORE}"
    ]


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        (
            "- TO: `### Requirement: The renamed rule holds`\n",
            "- TO: `### Requirement: The renamed rule holds`\nRenamed for clarity.\n",
            "is neither a FROM: nor a TO: line, which alone a RENAMED Requirements section holds",
        ),
        (
            "- FROM: `### Requirement: The old rule holds`\n",
            "- FROM: ### Requirement: The old rule holds\n",
            "is neither a FROM: nor a TO: line, which alone a RENAMED Requirements section holds",
        ),
        (
            "- FROM: `### Requirement: The old rule holds`\n",
            "* FROM: `### Requirement: The old rule holds`\n",
            "is neither a FROM: nor a TO: line, which alone a RENAMED Requirements section holds",
        ),
        (
            "- TO: `### Requirement: The renamed rule holds`\n",
            "- TO: `### Requirement: `\n",
            "is neither a FROM: nor a TO: line, which alone a RENAMED Requirements section holds",
        ),
    ],
)
def test_a_line_in_renamed_requirements_other_than_from_or_to_fails(
    tmp_path: Path, old: str, new: str, message: str
) -> None:
    defect = planted(DELTAS_BETA, old, new)
    changed = new.split("\n")[-2]
    problems = problems_of(tmp_path, CHANGE_BETA, defect)
    assert f"{CHANGE_BETA}:{line(defect, changed)}: {message}" in problems


def test_a_from_line_with_no_to_line_and_a_to_line_with_no_from_line_fail(tmp_path: Path) -> None:
    unpaired = planted(
        DELTAS_BETA,
        "- TO: `### Requirement: The renamed rule holds`\n",
        "- FROM: `### Requirement: The other rule holds`\n"
        "- TO: `### Requirement: The renamed rule holds`\n"
        "- TO: `### Requirement: The lone rule holds`\n",
    )
    assert problems_of(tmp_path, CHANGE_BETA, unpaired) == [
        f"{CHANGE_BETA}:{line(unpaired, '- FROM:')}: is a FROM: line with no TO: line after it",
        f"{CHANGE_BETA}:{line(unpaired, '- TO: `### Requirement: The lone')}: is a TO: line"
        " with no FROM: line before it",
    ]
    pending = planted(DELTAS_BETA, "- TO: `### Requirement: The renamed rule holds`\n", "")
    assert problems_of(tmp_path, CHANGE_BETA, pending) == [
        f"{CHANGE_BETA}:{line(pending, '- FROM:')}: is a FROM: line with no TO: line after it"
    ]


def test_a_spec_in_openspec_s_own_form_passes(tmp_path: Path) -> None:
    assert problems_in(passing(tmp_path)) == []
    assert problems_of(tmp_path, CHANGE_ALPHA, "\n\n" + ADDED_ALPHA + "\n\n") == []


# Requirements (R173).


@pytest.mark.parametrize(
    "new",
    [
        "The tool holds the first rule.",
        "The tool shall hold the first rule.",
        "The tool Must hold the first rule.",
        "The tool SHALLOW holds the first rule, as MUSTARD does, and NOT_SHALL.",
    ],
)
def test_a_requirement_with_no_shall_or_must_fails(tmp_path: Path, new: str) -> None:
    assert problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, new)) == [NO_SHALL]


def test_a_requirement_with_shall_or_must_in_its_heading_alone_fails(tmp_path: Path) -> None:
    defect = planted(ALPHA, FIRST, "### Requirement: The tool SHALL hold the first rule")
    defect = planted(defect, TEXT, "It holds.")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f'{MAIN_ALPHA}:{line(ALPHA, FIRST)}: requirement "The tool SHALL hold the first rule"'
        " holds neither SHALL nor MUST in its text"
    ]


def test_a_requirement_with_must_on_a_later_line_passes(tmp_path: Path) -> None:
    defect = planted(ALPHA, TEXT, "The tool holds the first rule,\nand MUST say so.")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == []


def long_text(length: int) -> str:
    start = "The tool SHALL hold "
    return start + "x" * (length - len(start) - 1) + "."


@pytest.mark.parametrize(
    ("path", "text", "old"),
    [
        (MAIN_ALPHA, ALPHA, TEXT),
        (CHANGE_ALPHA, ADDED_ALPHA, "The tool SHALL hold the third rule."),
        (CHANGE_BETA, DELTAS_BETA, "The tool SHALL hold the beta rule, and say so."),
    ],
)
def test_a_requirement_longer_than_500_characters_fails(
    tmp_path: Path, path: str, text: str, old: str
) -> None:
    defect = planted(text, old, long_text(501))
    heading = [
        number
        for number, content in enumerate(defect.split("\n"), 1)
        if content.startswith("### Requirement:") and number < line(defect, "The tool SHALL hold x")
    ][-1]
    name = defect.split("\n")[heading - 1].removeprefix("### Requirement: ")
    assert problems_of(tmp_path, path, defect) == [
        f'{path}:{heading}: requirement "{name}" has 501 characters of text, more than 500'
    ]


def test_a_requirement_of_exactly_500_characters_passes(tmp_path: Path) -> None:
    first = "  The tool SHALL hold " + "x" * 229 + "   "
    second = "   " + "y" * 250
    text = f"{first}\n\n{second}"
    assert len(first.strip()) + 1 + len(second.strip()) == 500
    assert problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, text)) == []
    longer = f"{first}\n\n{second}y"
    assert problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, longer)) == [
        f'{MAIN_ALPHA}:{line(ALPHA, FIRST)}: requirement "The first rule holds" has 501'
        " characters of text, more than 500"
    ]


@pytest.mark.parametrize("label", ["**Note**: a note.", "  **Note**: a note.", "**ID**:x"])
def test_a_label_line_in_a_requirement_s_text_fails(tmp_path: Path, label: str) -> None:
    defect = planted(ALPHA, f"{TEXT}\n", f"{TEXT}\n{label}\n")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f'{MAIN_ALPHA}:{line(ALPHA, TEXT) + 1}: requirement "The first rule holds" holds a line'
        " that starts with a bold label and a colon"
    ]


def test_bold_text_that_is_not_a_label_passes(tmp_path: Path) -> None:
    defect = planted(ALPHA, f"{TEXT}\n", f"{TEXT}\n**Note** that it holds: always.\n")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == []


@pytest.mark.parametrize(
    ("path", "text", "scenario", "requirement"),
    [
        (MAIN_ALPHA, ALPHA, "#### Scenario: The second rule holds", "The second rule holds"),
        (CHANGE_ALPHA, ADDED_ALPHA, "#### Scenario: The third rule holds", "The third rule holds"),
        (CHANGE_BETA, DELTAS_BETA, "#### Scenario: The beta rule holds", "The beta rule holds"),
    ],
)
def test_a_requirement_with_no_scenario_fails(
    tmp_path: Path, path: str, text: str, scenario: str, requirement: str
) -> None:
    start = text.index(scenario)
    end = text.find("\n## ", start)
    defect = text[:start] + (text[end + 1 :] if end != -1 else "")
    heading = line(defect, f"### Requirement: {requirement}")
    assert problems_of(tmp_path, path, defect) == [
        f'{path}:{heading}: requirement "{requirement}" has no scenario'
    ]


def test_a_tree_whose_specs_give_no_requirement_fails(tmp_path: Path) -> None:
    root = tree(tmp_path, {MAIN_ALPHA: ALPHA[: ALPHA.index("### Requirement")]})
    assert problems_in(root) == ["openspec/: the specs give no requirement for the test to read"]


def test_a_tree_whose_requirements_give_no_scenario_fails(tmp_path: Path) -> None:
    text = "## Purpose\n\nA purpose.\n\n## Requirements\n\n### Requirement: A rule\n\nIt SHALL.\n"
    root = tree(tmp_path, {MAIN_ALPHA: text})
    assert problems_in(root) == [
        f'{MAIN_ALPHA}:7: requirement "A rule" has no scenario',
        "openspec/: the specs give no scenario for the test to read",
    ]


def test_a_tree_whose_only_requirements_a_change_removes_or_renames_fails(tmp_path: Path) -> None:
    text = DELTAS_BETA[DELTAS_BETA.index("## REMOVED") :]
    root = tree(tmp_path, {CHANGE_BETA: text})
    assert problems_in(root) == ["openspec/: the specs give no requirement for the test to read"]


def test_a_removed_or_renamed_requirement_is_not_read_for_its_text(tmp_path: Path) -> None:
    removed = planted(
        DELTAS_BETA,
        "**Migration**: Hold the new beta rule.\n",
        f"**Migration**: Hold the new beta rule.\n\n{'z' * 600}\n"
        "\n### Requirement: The bare rule holds\n",
    )
    assert problems_of(tmp_path, CHANGE_BETA, removed) == []


# Scenarios (R174).

SECOND_SCENARIO = "#### Scenario: The second rule holds"
WHEN_2 = "- **WHEN** the second rule is tested"
THEN_2 = "- **THEN** it holds"
OF_2 = 'scenario "The second rule holds" of requirement "The second rule holds"'


def second_scenario(lines: str) -> str:
    return planted(ALPHA, f"{WHEN_2}\n{THEN_2}\n", lines)


@pytest.mark.parametrize(
    ("lines", "at", "message"),
    [
        (f"{THEN_2}\n", SECOND_SCENARIO, "has no WHEN line"),
        (f"{WHEN_2}\n", SECOND_SCENARIO, "has no THEN line"),
        ("", SECOND_SCENARIO, "has no WHEN line"),
        (f"{WHEN_2}\n{WHEN_2}\n{THEN_2}\n", WHEN_2, "gives a second WHEN line"),
        (f"{WHEN_2}\n{THEN_2}\n{THEN_2}\n", THEN_2, "gives a second THEN line"),
        (f"{WHEN_2}\n{THEN_2}\n{WHEN_2}\n", WHEN_2, "gives a second WHEN line"),
        (f"{THEN_2}\n{WHEN_2}\n", THEN_2, "gives its THEN line before its WHEN line"),
        (
            f"- **AND** first\n{WHEN_2}\n{THEN_2}\n",
            "- **AND** first",
            "gives an AND line before its WHEN line",
        ),
        (
            f"{WHEN_2}\nThe rule is tested.\n{THEN_2}\n",
            "The rule is",
            "holds a line other than a WHEN, a THEN or an AND line",
        ),
        (
            f"{WHEN_2}\n  - **AND** it holds\n{THEN_2}\n",
            "  - **AND**",
            "holds a line other than a WHEN, a THEN or an AND line",
        ),
        (
            f"- **GIVEN** a rule\n{WHEN_2}\n{THEN_2}\n",
            "- **GIVEN**",
            "holds a line other than a WHEN, a THEN or an AND line",
        ),
        (
            f"{WHEN_2}\n{THEN_2}\n**Note**: noted\n",
            "**Note**",
            "holds a line other than a WHEN, a THEN or an AND line",
        ),
        (
            f"{WHEN_2}\n* **THEN** it holds\n",
            "* **THEN**",
            "holds a line other than a WHEN, a THEN or an AND line",
        ),
    ],
)
def test_a_scenario_out_of_form_fails(tmp_path: Path, lines: str, at: str, message: str) -> None:
    defect = second_scenario(lines)
    after = line(defect, SECOND_SCENARIO) if at != SECOND_SCENARIO else 0
    if at in (WHEN_2, THEN_2) and lines.count(at) == 2:
        after = line(defect, at, after=after)
    problems = problems_of(tmp_path, MAIN_ALPHA, defect)
    assert f"{MAIN_ALPHA}:{line(defect, at, after=after)}: {OF_2} {message}" in problems
    if lines == "":
        assert problems == [
            f"{MAIN_ALPHA}:{line(defect, SECOND_SCENARIO)}: {OF_2} has no WHEN line",
            f"{MAIN_ALPHA}:{line(defect, SECOND_SCENARIO)}: {OF_2} has no THEN line",
        ]
    elif lines.count("\n") == 1:
        assert len(problems) == 1


def test_a_scenario_whose_then_comes_first_is_named_once(tmp_path: Path) -> None:
    defect = second_scenario(f"{THEN_2}\n{WHEN_2}\n")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{line(defect, THEN_2, after=line(defect, SECOND_SCENARIO))}: {OF_2}"
        " gives its THEN line before its WHEN line"
    ]


@pytest.mark.parametrize("heading", ["Scenario: Again", "**Scenario: Again**"])
def test_a_later_scenario_s_heading_made_plain_text_or_bold_fails(
    tmp_path: Path, heading: str
) -> None:
    later = f"\n{heading}\n\n- **WHEN** it is tested again\n- **THEN** it holds again\n"
    defect = planted(ALPHA, f"{WHEN_2}\n{THEN_2}\n", f"{WHEN_2}\n{THEN_2}\n{later}")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f"{MAIN_ALPHA}:{line(defect, heading)}: {OF_2} holds a line other than a WHEN, a THEN"
        " or an AND line",
        f"{MAIN_ALPHA}:{line(defect, '- **WHEN** it is tested again')}: {OF_2} gives a second"
        " WHEN line",
        f"{MAIN_ALPHA}:{line(defect, '- **THEN** it holds again')}: {OF_2} gives a second THEN"
        " line",
    ]


def test_a_scenario_with_the_name_of_another_in_its_spec_fails(tmp_path: Path) -> None:
    under_two = planted(ALPHA, SECOND_SCENARIO, SCENARIO)
    copy = f"\n{SCENARIO}\n\n{WHEN_2}\n{THEN_2}\n"
    under_one = planted(ALPHA, "- **AND** it holds again\n", f"- **AND** it holds again\n{copy}")
    closed = planted(ALPHA, SECOND_SCENARIO, f"{SCENARIO} ##")
    for defect in (under_two, under_one, closed):
        number = line(defect, "#### Scenario: The rule holds", after=line(defect, SCENARIO))
        assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
            f'{MAIN_ALPHA}:{number}: gives a scenario the name "The rule holds", which another'
            " scenario of the spec has"
        ]


def test_scenarios_of_the_same_name_in_two_specs_pass(tmp_path: Path) -> None:
    other = ALPHA.replace("first", "fourth").replace("second rule", "fifth rule")
    assert problems_of(tmp_path, "openspec/specs/other/spec.md", other) == []


@pytest.mark.parametrize(
    "new",
    ["- **WHEN** it is said", "- **THEN** it is said", "- **AND** it is said", "  - **AND** x"],
)
def test_a_scenario_s_line_in_a_requirement_s_text_fails(tmp_path: Path, new: str) -> None:
    defect = planted(ALPHA, f"{TEXT}\n", f"{TEXT}\n{new}\n")
    assert problems_of(tmp_path, MAIN_ALPHA, defect) == [
        f'{MAIN_ALPHA}:{line(ALPHA, TEXT) + 1}: requirement "The first rule holds" holds a'
        " scenario's line in its text"
    ]


def test_a_scenario_with_and_lines_passes(tmp_path: Path) -> None:
    lines = f"{WHEN_2}\n- **AND** again\n- **AND** once more\n\n{THEN_2}\n- **AND** still\n"
    assert problems_of(tmp_path, MAIN_ALPHA, second_scenario(lines)) == []


# The repository's specs, time and output.


def test_the_specs_keep_openspec_s_form() -> None:
    problems = problems_in(ROOT)
    assert not problems, "\n".join(problems)


# A run of spaces long enough that a pattern which can match it in many ways takes seconds,
# where one that matches it in one way takes milliseconds.
LONG_RUN = " " * 40_000
# What each pattern of the reader reads a run of spaces after: a heading of each kind, a
# scenario's line, a label, a rename, a run of backticks, a word, and a list's or a quote's
# marker.
SHAPES = [
    "",
    "x",
    "# x",
    "## Purpose",
    "### Requirement: x",
    "#### Scenario: x",
    "- **WHEN** x",
    "**x**",
    "- FROM: `### Requirement: x",
    "`",
    "```",
    "SHALL",
    "-",
    "1.",
    ">",
]


def test_no_pattern_is_slowed_by_a_long_run_of_spaces() -> None:
    patterns = {
        name: value for name, value in vars(spec_form).items() if isinstance(value, re.Pattern)
    }
    assert patterns, "the reader has no pattern, so this test covered nothing"
    slow = []
    for shape in SHAPES:
        for ending in ("y", "\ny", "`", "#", "**:"):
            for name, compiled in patterns.items():
                started = time.perf_counter()
                compiled.findall(f"{shape}{LONG_RUN}{ending}")
                if time.perf_counter() - started >= 1:
                    slow.append(f"{name}: {shape!r}, a long run of spaces, {ending!r}")
    assert not slow


def test_a_spec_with_a_long_line_is_read_quickly(tmp_path: Path) -> None:
    runs = "x".join("`" * length for length in range(1, 280))
    single = "` " * 20_000
    markers = ("- " * 500_000, "> " * 500_000 + "#")
    for text in (
        f"{TEXT}{LONG_RUN}x",
        f"{FIRST}{LONG_RUN}x",
        runs,
        single,
        f"#{LONG_RUN}#",
        *markers,
    ):
        started = time.perf_counter()
        problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, text))
        assert time.perf_counter() - started < 1, text[:40]


def test_no_line_of_a_spec_starts_a_line_of_the_output(tmp_path: Path) -> None:
    command = "::error file=x::y"
    defect = planted(ALPHA, FIRST, f"### Requirement: a\r{command}")
    defect = planted(defect, TEXT, f"{TEXT}\u2028{command}\u0085{command}")
    root = passing(tmp_path, {f"openspec/specs/a\n{command}\r{command}/spec.md": defect})
    output = "\n".join(problems_in(root))
    assert command in output.replace("U+000A", "").replace("U+000D", "")
    assert all(not part.lstrip(" \t").startswith("::") for part in output.splitlines())
    assert all(" " <= character <= "~" or character == "\n" for character in output)


# The comparison with the pinned OpenSpec CLI (R178, DR-196).

# What the pinned CLI printed for each tree below, call by call, with the folder that it
# ran in and the times at which each change was last changed left out, and a digest of
# the tree. `record` writes it.
RECORDING = ROOT / "tests" / "spec_form_openspec.json"
# The passing tree but its change with no proposal, which OpenSpec does not show.
AGREEING = {name: text for name, text in PASSING.items() if name != DRAFT_GAMMA}
# Two lines that open and close a fence, each inside an HTML comment that GitHub hides,
# take the second requirement of the first spec out of OpenSpec's reading.
COMMENTED_FENCE = "<!--\n```\n-->\n"
FENCED = {**AGREEING, MAIN_ALPHA: planted(ALPHA, SECOND, f"{COMMENTED_FENCE}\n{SECOND}")}
FENCED[MAIN_ALPHA] += COMMENTED_FENCE
TREES = {
    "agreeing": AGREEING,
    "fenced": FENCED,
    "no spec": {"openspec/config.yaml": PASSING["openspec/config.yaml"]},
    "no proposal": PASSING,
}
LIST_SPECS = ["list", "--specs", "--json"]
LIST_CHANGES = ["list", "--json", "--sort", "name"]
SHOW_SPEC = ["show", "--type", "spec", "--json", "--"]
SHOW_CHANGE = ["show", "--type", "change", "--json", "--deltas-only", "--"]
SHOW_ALPHA = [*SHOW_SPEC, "alpha"]
SHOW_BETA = [*SHOW_SPEC, "area/beta"]
SHOW_DEMO = [*SHOW_CHANGE, "demo"]
FORM = "prints JSON in another form than the comparison reads"
RERECORD = (
    "run `PYTHONPATH=scripts .venv/bin/python tests/test_spec_form.py node_modules/.bin/openspec`"
    " at the repository's root"
)


def a_call(args: list[str], stdout: Any, status: int = 0, stderr: str = "") -> dict[str, Any]:
    return {"args": args, "exit": status, "stdout": stdout, "stderr": stderr}


def digest(files: Mapping[str, str]) -> str:
    return hashlib.sha256(json.dumps(sorted(files.items())).encode()).hexdigest()


def recorded_calls(program: str, root: Path, env: dict[str, str]) -> list[dict[str, Any]]:
    """Each call that the comparison makes of the CLI in the tree at root, with what it
    printed, but the folder that it ran in and the time at which each change was last
    changed, which the comparison does not read. `spec_form.cli_reading` itself makes the
    calls, so the recorder asks what the comparison asks, in its order."""
    calls: list[dict[str, Any]] = []

    def run(args: list[str]) -> tuple[int, str, str]:
        done = subprocess.run(
            [program, *args], cwd=root, env=env, capture_output=True, text=True, check=False
        )
        output = json.loads(done.stdout)
        output.pop("root", None)
        for change in output.get("changes", []):
            change.pop("lastModified", None)
        calls.append(a_call(args, output, done.returncode, done.stderr))
        return done.returncode, json.dumps(output), done.stderr

    spec_form.cli_reading(run)
    return calls


def record(cli: str) -> None:
    """Rewrites the recording with what the CLI at this path prints for each tree, its own
    settings kept in a scratch folder, as `scripts/verify-openspec.sh` keeps them."""
    program = str(Path(cli).resolve())
    with tempfile.TemporaryDirectory() as scratch:
        env = {
            **os.environ,
            "XDG_CONFIG_HOME": f"{scratch}/config",
            "XDG_DATA_HOME": f"{scratch}/data",
            "DO_NOT_TRACK": "1",
            "OPENSPEC_TELEMETRY": "0",
            "OPENSPEC_NO_UPDATE_CHECK": "1",
        }
        version = subprocess.run(
            [program, "--version"], env=env, capture_output=True, text=True, check=True
        ).stdout.strip()
        trees = {
            name: {
                "tree": digest(files),
                "calls": recorded_calls(program, tree(Path(scratch) / name, files), env),
            }
            for name, files in TREES.items()
        }
        text = json.dumps({"openspec": version, "trees": trees}, indent=2) + "\n"
        assert scratch not in text, "the recording names the folder it was made in"
    RECORDING.write_text(text, encoding="utf-8")


@functools.cache
def recorded() -> Any:
    return json.loads(RECORDING.read_text(encoding="utf-8"))


def calls_of(name: str) -> list[dict[str, Any]]:
    """A copy of the calls recorded for a tree, for a test to plant a defect in."""
    calls: list[dict[str, Any]] = copy.deepcopy(recorded()["trees"][name]["calls"])
    return calls


def printed(calls: list[dict[str, Any]], args: list[str]) -> Any:
    """The JSON that the recorded call with these arguments printed."""
    return next(call["stdout"] for call in calls if call["args"] == args)


class Replay:
    """The pinned CLI, replayed from its recorded calls, noting what it is asked."""

    def __init__(self, calls: list[dict[str, Any]]) -> None:
        self.calls = calls
        self.asked: list[list[str]] = []

    def __call__(self, args: list[str]) -> tuple[int, str, str]:
        self.asked.append(args)
        for call in self.calls:
            if call["args"] == args:
                out = call["stdout"]
                return (
                    call["exit"],
                    out if isinstance(out, str) else json.dumps(out),
                    call["stderr"],
                )
        raise AssertionError(f"no call of OpenSpec was recorded with {args}")


def comparison(root: Path, calls: list[dict[str, Any]]) -> list[str]:
    """The problems of the CLI's reading, or else its differences from the test's reading
    of the tree at root."""
    theirs, problems = spec_form.cli_reading(Replay(calls))
    return problems or spec_form.differences(spec_form.read_all(root)[0], theirs)


def test_the_recording_is_of_the_trees_that_the_tests_read() -> None:
    assert sorted(recorded()["trees"]) == sorted(TREES)
    for name, files in TREES.items():
        assert recorded()["trees"][name]["tree"] == digest(files), (
            f"the tree {name!r} changed after its recording: {RERECORD}"
        )


def test_the_recording_is_of_the_release_that_package_lock_json_pins() -> None:
    lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
    pinned = lock["packages"]["node_modules/@fission-ai/openspec"]["version"]
    assert recorded()["openspec"] == pinned, (
        f"the recording is of OpenSpec {recorded()['openspec']}, and package-lock.json pins"
        f" {pinned}: {RERECORD}"
    )


def test_the_recording_holds_no_time_of_day() -> None:
    times = re.findall(r"\d\d:\d\d", RECORDING.read_text(encoding="utf-8"))
    assert times == [], "the recording holds the time of day at which it was made"


def test_the_recording_lists_the_changes_by_name() -> None:
    # Asked for no order, the CLI lists first the change whose files it finds last changed,
    # so a recording made again could list the same changes in another order.
    for name, made in recorded()["trees"].items():
        listed = [change["name"] for change in printed(made["calls"], LIST_CHANGES)["changes"]]
        assert listed == sorted(listed), name


def test_the_readings_of_a_tree_that_openspec_reads_as_the_test_does_agree(
    tmp_path: Path,
) -> None:
    replay = Replay(calls_of("agreeing"))
    theirs, problems = spec_form.cli_reading(replay)
    ours = spec_form.read_all(tree(tmp_path, AGREEING))[0]
    assert problems == []
    assert replay.asked == [call["args"] for call in calls_of("agreeing")]
    assert theirs == ours
    assert theirs.specs[("demo", "area/beta")][-1] == Requirement(
        "RENAMED", "The old rule holds", "", (), "The renamed rule holds"
    )
    assert spec_form.differences(ours, theirs) == []


def test_a_requirement_that_a_fence_hides_from_openspec_fails(tmp_path: Path) -> None:
    after = FENCED[MAIN_ALPHA].split(f"{SCENARIO}\n", 1)[1]
    ours, theirs = after.split(f"\n\n{SECOND}", 1)[0].strip(), after.strip()
    assert comparison(tree(tmp_path, FENCED), calls_of("fenced")) == [
        f'{MAIN_ALPHA}: requirement 1, "The first rule holds", differs in its scenario 1\'s'
        f' lines: the test reads "{shown(ours)}", and OpenSpec shows "{shown(theirs)}"'
    ]


def operation(calls: list[dict[str, Any]]) -> None:
    printed(calls, SHOW_DEMO)["deltas"][0]["operation"] = "MODIFIED"


def name(calls: list[dict[str, Any]]) -> None:
    printed(calls, SHOW_ALPHA)["requirements"][1]["name"] = "The other rule holds"


def text(calls: list[dict[str, Any]]) -> None:
    printed(calls, SHOW_ALPHA)["requirements"][0]["text"] = "The tool SHALL hold a rule."


def new_name(calls: list[dict[str, Any]]) -> None:
    printed(calls, SHOW_DEMO)["deltas"][-1]["rename"]["to"] = "The other rule holds"


def scenarios(calls: list[dict[str, Any]]) -> None:
    printed(calls, SHOW_ALPHA)["requirements"][0]["scenarios"].append(
        {"name": "Another", "rawText": "- **WHEN** x\n- **THEN** y"}
    )


def scenario_name(calls: list[dict[str, Any]]) -> None:
    printed(calls, SHOW_ALPHA)["requirements"][0]["scenarios"][0]["name"] = "The rule is held"


def scenario_lines(calls: list[dict[str, Any]]) -> None:
    printed(calls, SHOW_ALPHA)["requirements"][1]["scenarios"][0]["rawText"] = "- **WHEN** x"


def order(calls: list[dict[str, Any]]) -> None:
    printed(calls, SHOW_BETA)["requirements"].reverse()


def number(calls: list[dict[str, Any]]) -> None:
    printed(calls, SHOW_ALPHA)["requirements"].pop()


def spec_of_the_test_alone(calls: list[dict[str, Any]]) -> None:
    printed(calls, LIST_SPECS)["specs"].pop()


def spec_of_openspec_alone(calls: list[dict[str, Any]]) -> None:
    deltas = printed(calls, SHOW_DEMO)["deltas"]
    deltas.append({**deltas[0], "spec": "gamma"})


def change_of_the_test_alone(calls: list[dict[str, Any]]) -> None:
    printed(calls, LIST_CHANGES)["changes"].clear()


def change_of_openspec_alone(calls: list[dict[str, Any]]) -> None:
    # The CLI lists a folder in `openspec/changes/` whose name starts with a dot, as it lists
    # any other but `archive`, though no reader of the specs reads it.
    for change in ("other", ".draft"):
        printed(calls, LIST_CHANGES)["changes"].append({"name": change})
        calls.append(a_call([*SHOW_CHANGE, change], {"deltas": []}))


DIFFERS = "differs in its {}: the test reads {}, and OpenSpec shows {}"


@pytest.mark.parametrize(
    ("plant", "expected"),
    [
        (
            operation,
            [
                f'{CHANGE_ALPHA}: requirement 1, "The third rule holds", '
                + DIFFERS.format("operation", '"ADDED"', '"MODIFIED"')
            ],
        ),
        (
            name,
            [
                f'{MAIN_ALPHA}: requirement 2, "The second rule holds", '
                + DIFFERS.format("name", '"The second rule holds"', '"The other rule holds"')
            ],
        ),
        (
            text,
            [
                f'{MAIN_ALPHA}: requirement 1, "The first rule holds", '
                + DIFFERS.format("text", f'"{TEXT}"', '"The tool SHALL hold a rule."')
            ],
        ),
        (
            new_name,
            [
                f'{CHANGE_BETA}: requirement 4, "The old rule holds", '
                + DIFFERS.format("new name", '"The renamed rule holds"', '"The other rule holds"')
            ],
        ),
        (
            scenarios,
            [
                f'{MAIN_ALPHA}: requirement 1, "The first rule holds", '
                + DIFFERS.format("number of scenarios", "1", "2")
            ],
        ),
        (
            scenario_name,
            [
                f'{MAIN_ALPHA}: requirement 1, "The first rule holds", '
                + DIFFERS.format("scenario 1's name", '"The rule holds"', '"The rule is held"')
            ],
        ),
        (
            scenario_lines,
            [
                f'{MAIN_ALPHA}: requirement 2, "The second rule holds", '
                + DIFFERS.format(
                    "scenario 1's lines", '"' + shown(f"{WHEN_2}\n{THEN_2}") + '"', '"- **WHEN** x"'
                )
            ],
        ),
        (
            order,
            [
                f'{MAIN_BETA}: requirement 1, "The beta rule holds", '
                + DIFFERS.format("name", '"The beta rule holds"', '"The spent rule holds"')
            ],
        ),
        (number, [f"{MAIN_ALPHA}: the test reads 2 requirements, and OpenSpec shows 1"]),
        (spec_of_the_test_alone, [f"{MAIN_BETA}: the test reads it, and OpenSpec does not"]),
        (
            spec_of_openspec_alone,
            ["openspec/changes/demo/specs/gamma/spec.md: OpenSpec reads it, and the test does not"],
        ),
        (
            change_of_the_test_alone,
            [
                "openspec/changes/demo: the test reads it as a change, and OpenSpec does not",
                f"{CHANGE_ALPHA}: the test reads it, and OpenSpec does not",
                f"{CHANGE_BETA}: the test reads it, and OpenSpec does not",
            ],
        ),
        (
            change_of_openspec_alone,
            [
                "openspec/changes/.draft: OpenSpec reads it as a change, and the test does not",
                "openspec/changes/other: OpenSpec reads it as a change, and the test does not",
            ],
        ),
    ],
)
def test_each_kind_of_difference_fails(
    tmp_path: Path, plant: Callable[[list[dict[str, Any]]], None], expected: list[str]
) -> None:
    calls = calls_of("agreeing")
    plant(calls)
    assert comparison(tree(tmp_path, AGREEING), calls) == expected


def test_a_difference_in_the_test_s_own_reading_fails(tmp_path: Path) -> None:
    files = {name: text for name, text in AGREEING.items() if name != MAIN_BETA}
    assert comparison(tree(tmp_path, files), calls_of("agreeing")) == [
        f"{MAIN_BETA}: OpenSpec reads it, and the test does not"
    ]


@pytest.mark.parametrize(
    "text", ["## Purpose\n\nWhat the delta capability does.\n", "## ADDED Requirements\n"]
)
def test_a_change_s_spec_from_which_the_test_reads_no_requirement_fails(
    tmp_path: Path, text: str
) -> None:
    path = "openspec/changes/demo/specs/delta/spec.md"
    files = {**AGREEING, path: text}
    assert comparison(tree(tmp_path, files), calls_of("agreeing")) == [
        f"{path}: the test reads it, and OpenSpec does not"
    ]


def test_a_tree_with_no_requirement_to_compare_fails(tmp_path: Path) -> None:
    assert comparison(tree(tmp_path, TREES["no spec"]), calls_of("no spec")) == [
        "openspec/: the comparison compares no requirement"
    ]


def test_a_change_that_openspec_does_not_show_fails_naming_the_call(tmp_path: Path) -> None:
    assert comparison(tree(tmp_path, PASSING), calls_of("no proposal")) == [
        "openspec show --type change --json --deltas-only -- draft: exits with 1: Change"
        ' "draft" has no proposal.md yet. Run "openspec status --change draft" to see which'
        " artifact comes next."
    ]


@pytest.mark.parametrize(
    ("out", "err", "said"),
    [
        ("", "boom\n", ": boom"),
        ("", "", ""),
        ("[]", "", ": []"),
        ("{}", "x\n", ": x"),
        ('{"status": [{"message": 1}, "y"]}', "z\n", ": z"),
    ],
)
def test_a_call_that_fails_fails_naming_it(tmp_path: Path, out: str, err: str, said: str) -> None:
    calls = calls_of("agreeing")
    calls[-1].update({"exit": 3, "stdout": out, "stderr": err})
    assert comparison(tree(tmp_path, AGREEING), calls) == [
        f"openspec {' '.join(SHOW_DEMO)}: exits with 3{said}"
    ]


def no_json(calls: list[dict[str, Any]]) -> list[str]:
    calls[0]["stdout"] = "Specs:\n  alpha"
    return LIST_SPECS


def a_list(calls: list[dict[str, Any]]) -> list[str]:
    calls[0]["stdout"] = []
    return LIST_SPECS


def no_id(calls: list[dict[str, Any]]) -> list[str]:
    del printed(calls, LIST_SPECS)["specs"][0]["id"]
    return LIST_SPECS


def an_id_not_text(calls: list[dict[str, Any]]) -> list[str]:
    printed(calls, LIST_SPECS)["specs"][0]["id"] = 1
    return LIST_SPECS


def changes_not_a_list(calls: list[dict[str, Any]]) -> list[str]:
    printed(calls, LIST_CHANGES)["changes"] = {}
    return LIST_CHANGES


def a_text_not_text(calls: list[dict[str, Any]]) -> list[str]:
    printed(calls, SHOW_ALPHA)["requirements"][0]["text"] = None
    return SHOW_ALPHA


def scenarios_not_a_list(calls: list[dict[str, Any]]) -> list[str]:
    printed(calls, SHOW_ALPHA)["requirements"][0]["scenarios"] = "none"
    return SHOW_ALPHA


def a_scenario_without_lines(calls: list[dict[str, Any]]) -> list[str]:
    del printed(calls, SHOW_ALPHA)["requirements"][0]["scenarios"][0]["rawText"]
    return SHOW_ALPHA


def an_unknown_operation(calls: list[dict[str, Any]]) -> list[str]:
    printed(calls, SHOW_DEMO)["deltas"][0]["operation"] = "CHANGED"
    return SHOW_DEMO


def a_rename_without_names(calls: list[dict[str, Any]]) -> list[str]:
    del printed(calls, SHOW_DEMO)["deltas"][-1]["rename"]
    return SHOW_DEMO


def a_new_name_not_text(calls: list[dict[str, Any]]) -> list[str]:
    printed(calls, SHOW_DEMO)["deltas"][-1]["rename"]["to"] = 2
    return SHOW_DEMO


def a_delta_without_its_spec(calls: list[dict[str, Any]]) -> list[str]:
    del printed(calls, SHOW_DEMO)["deltas"][0]["spec"]
    return SHOW_DEMO


def a_requirement_not_an_object(calls: list[dict[str, Any]]) -> list[str]:
    printed(calls, SHOW_DEMO)["deltas"][0]["requirement"] = "x"
    return SHOW_DEMO


@pytest.mark.parametrize(
    "plant",
    [
        no_json,
        a_list,
        no_id,
        an_id_not_text,
        changes_not_a_list,
        a_text_not_text,
        scenarios_not_a_list,
        a_scenario_without_lines,
        an_unknown_operation,
        a_rename_without_names,
        a_new_name_not_text,
        a_delta_without_its_spec,
        a_requirement_not_an_object,
    ],
)
def test_a_call_that_prints_json_in_another_form_fails_naming_it(
    tmp_path: Path, plant: Callable[[list[dict[str, Any]]], list[str]]
) -> None:
    calls = calls_of("agreeing")
    args = plant(calls)
    assert comparison(tree(tmp_path, AGREEING), calls) == [f"openspec {' '.join(args)}: {FORM}"]


def stand_in(folder: Path, calls: list[dict[str, Any]]) -> str:
    """An OpenSpec CLI that prints what the pinned one printed for these calls."""
    folder.mkdir()
    script = folder / "openspec"
    script.write_text(
        f"#!{sys.executable}\n"
        "import json, sys\n"
        f"CALLS = json.loads({json.dumps(calls)!r})\n"
        "call = next(each for each in CALLS if each['args'] == sys.argv[1:])\n"
        "out = call['stdout']\n"
        "print(out if isinstance(out, str) else json.dumps(out, indent=2))\n"
        "print(call['stderr'], end='', file=sys.stderr)\n"
        "sys.exit(call['exit'])\n",
        encoding="utf-8",
    )
    script.chmod(0o755)
    return str(script)


@pytest.mark.parametrize(
    ("name", "status"), [("agreeing", 0), ("fenced", 1), ("no spec", 1), ("no proposal", 1)]
)
def test_the_comparison_runs_the_cli_and_exits_by_what_it_finds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    name: str,
    status: int,
) -> None:
    cli = stand_in(tmp_path / "cli", calls_of(name))
    root = tree(tmp_path / "tree", TREES[name])
    monkeypatch.chdir(root)
    assert spec_form.main([cli]) == status
    out, err = capsys.readouterr()
    if status:
        assert (out, err.splitlines()) == (
            "",
            [f"verify-openspec: {each}" for each in comparison(root, calls_of(name))],
        )
    else:
        assert (out, err) == ("verify-openspec: 10 requirement(s) read alike\n", "")


def test_the_comparison_exits_2_when_the_cli_does_not_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tree(tmp_path / "tree", AGREEING))
    plain = tmp_path / "plain"
    plain.write_text("not a program\n")
    for argv in ([str(tmp_path / "missing")], [str(plain)], [], ["a", "b"]):
        assert spec_form.main(argv) == 2, argv
        out, err = capsys.readouterr()
        assert out == ""
        assert err.startswith("verify-openspec: ") and err.count("\n") == 1, err


def test_no_line_of_a_spec_or_of_openspec_s_output_starts_a_line_of_the_comparison_s(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    command = "::error file=x::y"
    calls = calls_of("agreeing")
    printed(calls, SHOW_ALPHA)["requirements"][0]["name"] = f"a\n{command}"
    printed(calls, LIST_CHANGES)["changes"].append({"name": f"b\n{command}"})
    calls.append(a_call([*SHOW_CHANGE, f"b\n{command}"], {"deltas": []}))
    failing = calls_of("agreeing")
    failing[-1].update({"exit": 1, "stdout": {"status": [{"message": f"c\n{command}"}]}})
    failing[0].update({"exit": 1, "stderr": f"d\n{command}"})
    files = {**AGREEING, f"openspec/specs/e\r{command}/spec.md": ALPHA}
    for number, each in enumerate((calls, failing)):
        cli = stand_in(tmp_path / f"cli-{number}", each)
        monkeypatch.chdir(tree(tmp_path / f"tree-{number}", files))
        assert spec_form.main([cli]) == 1
        out, err = capsys.readouterr()
        assert out == ""
        assert command in err.replace("U+000A", "").replace("U+000D", "")
        assert all(part.startswith("verify-openspec: openspec") for part in err.splitlines())
        assert all(" " <= character <= "~" or character == "\n" for character in err)


if __name__ == "__main__":
    record(sys.argv[1])
