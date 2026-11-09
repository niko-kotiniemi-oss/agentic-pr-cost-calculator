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
inline code, a `<`, an `&`, a backslash, a `|`, a `](` or a `]:`, with which GitHub
would hide or show text otherwise than OpenSpec and agents read it.

A spec's lines are then read in one pass as OpenSpec reads them (R175, DR-193): an
optional title before any heading, then the sections that OpenSpec reads, `## Purpose`
and `## Requirements` in a main spec, each once, and in a change's spec `## Purpose`,
once, and `## ADDED Requirements`, `## MODIFIED Requirements`, `## REMOVED Requirements`
and `## RENAMED Requirements`, each written as OpenSpec's template writes it. A section
that gives requirements holds blank lines, then `### Requirement: ` headings, each with
its name, its text and its `#### Scenario: ` headings; `RENAMED Requirements` holds only
blank lines and pairs of `FROM:` and `TO:` lines. Any other heading fails, and so does a
line that starts, after spaces or tabs, with `#` or with three backticks or tildes, a
line of `=` or `-` signs alone, with which GitHub makes the line above it a heading, and
a line before the first requirement of its section. A closing run of `#` signs after a
space, which GitHub and OpenSpec both leave out of a heading's name, is allowed, and a
title that OpenSpec would read as the Requirements section fails.

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
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path

import pytest
import spec_form
from spec_form import Spec, find_specs, problems_in, prose_of, shown

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


def tree(root: Path, files: dict[str, str | bytes]) -> Path:
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


def test_a_byte_order_mark_fails(tmp_path: Path) -> None:
    assert problems_of(tmp_path, MAIN_ALPHA, "\ufeff" + ALPHA) == [
        f"{MAIN_ALPHA}:1: holds U+FEFF, which is not printable ASCII or a line feed"
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
    new = "The tool SHALL hold | the first | rule <here> & <there>, \\o/ [a](b) [c]: d."
    assert problems_of(tmp_path, MAIN_ALPHA, planted(ALPHA, TEXT, new)) == [
        f'{MAIN_ALPHA}:{number}: holds "{mark}" outside inline code'
        for mark in ("<", "&", "\\", "|", "](", "]:")
    ]


def test_those_marks_pass_inside_inline_code(tmp_path: Path) -> None:
    new = "The tool SHALL hold `<` `&` `\\` `|` `](` `]:` and ``a ` b``, in `<!-- x -->`."
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
HASH = 'starts with "#" but is not a heading in form'
FENCE = "starts with three backticks or tildes, as a fence does"
UNDERLINE = 'holds only "=" or "-" signs, with which GitHub can make the line above it a heading'
BEFORE = "stands before the first requirement of its section"
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
    ("heading", "what"),
    [
        ("### Requirement:", "requirement"),
        ("### Requirement: ", "requirement"),
        ("### Requirement:   ", "requirement"),
        ("### Requirement: #", "requirement"),
        ("### Requirement: ###   ", "requirement"),
    ],
)
def test_a_requirement_s_heading_without_a_name_fails(
    tmp_path: Path, heading: str, what: str
) -> None:
    defect = planted(ALPHA, FIRST, heading)
    assert problems_of(tmp_path, MAIN_ALPHA, defect)[:1] == [
        f"{MAIN_ALPHA}:{line(ALPHA, FIRST)}: is a {what}'s heading without a name"
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


def test_a_title_after_lines_of_prose_passes(tmp_path: Path) -> None:
    assert problems_of(tmp_path, MAIN_ALPHA, f"Prose first.\n\n{ALPHA}") == []


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


@pytest.mark.parametrize("signs", ["===", "---", "-", "= =", "- - -", "=-=", "  ==  "])
def test_a_line_of_equals_or_minus_signs_fails(tmp_path: Path, signs: str) -> None:
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
# scenario's line, a label, a rename, a run of backticks and a word.
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
    for text in (f"{TEXT}{LONG_RUN}x", f"{FIRST}{LONG_RUN}x", runs, single, f"#{LONG_RUN}#"):
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
