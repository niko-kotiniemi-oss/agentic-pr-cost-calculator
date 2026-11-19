"""The risk register is what `scripts/risk_register.py` writes from the threat model.

`docs/risk-register.md` gives each threat its raw rating, as if its answer were not
built, and its rating with the answer in place, each with its band, and what answers
it by ID (R245 to R248, design decision 20, DR-256). The script writes it from the
threat model, the specs and the register of requirements alone, so that each rating
lives in one place; these tests fail when the committed page differs from what the
script writes, naming the threat or the line.

They also read the page as a reader would, rather than trusting the script: each
threat sits once in the cell of each matrix that its ratings name, each band follows
its score, the bands' counts add up to the threats, and the page holds no text that
GitHub hides and links only this repository's files, by the roadmap's rules, but for
the `|` of its tables, each row of which holds as many cells as its header (R246).
The bands are one table in the script, `BANDS`, which this test and the threat model's
test import; R247 and DR-253 state the same lines, and a line moved in one place and not
the others fails.

Each check is shown to fail on a synthetic threat model, specs and register, into
which the defect is planted.
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest
import risk_register
from risk_register import (
    BANDS,
    PAGE,
    RegisterError,
    band,
    bands_phrase,
    blind,
    check,
    score_of,
    threats_in,
    write,
)
from test_roadmap import hidden_text_problems_in, link_problems_in, section_of

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "risk_register.py"
REQUIREMENTS_SPEC = (
    ROOT / "openspec" / "changes" / "add-pr-cost-calculator" / "specs" / "project-standards"
)
BANDS_RECORD = ROOT / "docs" / "decisions" / "DR-253-risk-bands.md"

ROW = re.compile(r"^\| \[(T\d+)\]\(threat-model\.md#[a-z0-9_-]+\) \|", re.M)
MATRIX_ROW = re.compile(r"^\| ([1-3]) [a-z]+ \|(.*)\|\s*$")
BAND_ROW = re.compile(r"^\| ([a-z]+) \| ([0-9a-z ]+) \| (\d+) \| (\d+) \|$")
RATED = re.compile(r"^(\d) ([a-z]+) \(([1-3]), ([1-3])\)$")
THREAT_ID = re.compile(r"T\d+")
# The raw rating and the rating with the answer in place, in the order of the rows' cells.
RATINGS = (("Raw impact", "Raw likelihood"), ("Impact", "Likelihood"))


# The page as a reader reads it.


def levels(threat: risk_register.Threat, impact: str, likelihood: str) -> tuple[int, int]:
    return (
        risk_register.rating(threat.field(impact), risk_register.IMPACTS),
        risk_register.rating(threat.field(likelihood), risk_register.LIKELIHOODS),
    )


def matrix_problems(page: str, text: str) -> list[str]:
    """Each threat once in the cell of each matrix that its ratings name (R247)."""
    problems = []
    for heading, impact, likelihood in (
        ("Raw matrix", "Raw impact", "Raw likelihood"),
        ("Matrix with the answers in place", "Impact", "Likelihood"),
    ):
        placed: dict[str, list[tuple[int, int]]] = {}
        rows = [found for line in section_of(page, heading)[1] if (found := MATRIX_ROW.match(line))]
        if sorted(int(row.group(1)) for row in rows) != [1, 2, 3]:
            problems.append(f"the {heading.lower()} does not have one row for each impact")
            continue
        for row in rows:
            cells = [cell.strip() for cell in row.group(2).split("|")]
            for column, cell in enumerate(cells, start=1):
                for ident in THREAT_ID.findall(cell):
                    placed.setdefault(ident, []).append((int(row.group(1)), column))
        for threat in threats_in(text):
            expected = [levels(threat, impact, likelihood)]
            if placed.pop(threat.ident, []) != expected:
                problems.append(f"{threat.ident} is not in its one cell of the {heading.lower()}")
        problems += [f"the {heading.lower()} names {ident}, not a threat" for ident in placed]
    return problems


def row_problems(page: str, text: str) -> list[str]:
    """Each threat once, in its order, each rating with the band that its score gives."""
    threats = {threat.ident: threat for threat in threats_in(text)}
    listed = ROW.findall(page)
    problems = [
        f"{ident} is listed twice" for ident in sorted(set(listed)) if listed.count(ident) > 1
    ]
    problems += [f"{ident} is left out" for ident in threats if ident not in listed]
    problems += [
        f"the register lists {ident}, not a threat" for ident in listed if ident not in threats
    ]
    order = []
    for line in page.split("\n"):
        row = ROW.match(line)
        if not row or row.group(1) not in threats:
            continue
        threat = threats[row.group(1)]
        cells = [cell.strip() for cell in line.strip("|").split(" | ")]
        scores = []
        for cell, (impact, likelihood) in zip(cells[4:6], RATINGS, strict=True):
            rated = RATED.match(cell)
            expected = levels(threat, impact, likelihood)
            if not rated or (int(rated.group(3)), int(rated.group(4))) != expected:
                problems.append(f"{threat.ident}'s row does not give its ratings: {cell!r}")
                continue
            score = int(rated.group(1))
            if score != expected[0] * expected[1] or rated.group(2) != BANDS[score]:
                problems.append(f"{threat.ident}'s row gives a band that its score does not")
            scores.append(score)
        order.append((-scores[-1] if scores else 0, -scores[0] if scores else 0, threat.number))
    if order != sorted(order):
        problems.append("the rows do not follow the risk, then the raw risk, then the ID")
    return problems


def count_problems(page: str, text: str) -> list[str]:
    """Each band's count, raw and with the answers in place, adds up to the threats."""
    threats = threats_in(text)
    counted = [found for line in section_of(page, "Bands")[1] if (found := BAND_ROW.match(line))]
    if [row.group(1) for row in counted] != [*dict.fromkeys(reversed(BANDS.values())), "all"]:
        return ["the bands' table does not give each band once, highest first, then all"]
    problems = []
    for column, (impact, likelihood) in enumerate(RATINGS, start=3):
        expected = {name: 0 for name in BANDS.values()}
        for threat in threats:
            expected[BANDS[score_of(threat, impact, likelihood)]] += 1
        given = {row.group(1): int(row.group(column)) for row in counted}
        if sum(given[name] for name in expected) != len(threats) or given["all"] != len(threats):
            problems.append(f"the bands' counts in column {column} do not add up to the threats")
        problems += [
            f"the {name} band's count in column {column} is {given[name]}, not {count}"
            for name, count in expected.items()
            if given[name] != count
        ]
    return problems


def hidden_problems(page: str, root: Path) -> list[str]:
    """R246: the roadmap's rules on links and hidden text, but for the `|` of the tables,
    whose rows each hold as many cells as their header."""
    lines = page.split("\n")
    shown = []
    problems = []
    header = 0
    for number, line in enumerate(lines, start=1):
        if line.startswith("|"):
            if number == 1 or not lines[number - 2].startswith("|"):
                header = line.count("|")
            elif line.count("|") != header:
                problems.append(f"{PAGE}:{number} holds a row whose cells differ from its header's")
            shown.append(line.replace("|", " "))
        else:
            shown.append(line)
    texts = [(PAGE, "docs", 1, shown, page)]
    return problems + link_problems_in(root, texts) + hidden_text_problems_in(texts)


def page_problems(page: str, text: str, root: Path) -> list[str]:
    return (
        row_problems(page, text)
        + matrix_problems(page, text)
        + count_problems(page, text)
        + hidden_problems(page, root)
    )


# The repository.


def test_the_committed_register_is_what_the_script_writes() -> None:
    assert check(ROOT) == []


def test_the_committed_register_reads_true() -> None:
    page = (ROOT / PAGE).read_text(encoding="utf-8")
    text = (ROOT / "docs" / "threat-model.md").read_text(encoding="utf-8")
    assert len(ROW.findall(page)) == len(threats_in(text)) > 0, "no row was read"
    assert page_problems(page, text, ROOT) == []


def test_the_script_runs_isolated_and_writes_nothing_with_check() -> None:
    before = (ROOT / PAGE).read_bytes()
    done = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), "--check"],
        cwd=ROOT / "docs",
        capture_output=True,
        text=True,
        check=False,
    )
    assert (done.returncode, done.stderr) == (0, "")
    assert (ROOT / PAGE).read_bytes() == before


@pytest.mark.parametrize(
    ("score", "name"),
    [(1, "note"), (2, "low"), (3, "medium"), (4, "medium"), (6, "high"), (9, "critical")],
)
def test_a_band_follows_its_score(score: int, name: str) -> None:
    assert band(score) == name


def test_the_bands_are_stated_alike_in_the_script_the_requirement_and_the_record() -> None:
    phrase = bands_phrase()
    assert phrase == "1 note, 2 low, 3 and 4 medium, 6 high and 9 critical"
    assert phrase in " ".join((REQUIREMENTS_SPEC / "spec.md").read_text(encoding="utf-8").split())
    assert phrase in " ".join(BANDS_RECORD.read_text(encoding="utf-8").split())


def test_a_line_between_the_bands_moved_in_one_place_is_reported(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(BANDS, 4, "high")
    phrase = bands_phrase()
    assert phrase == "1 note, 2 low, 3 medium, 4 and 6 high and 9 critical"
    assert phrase not in " ".join(
        (REQUIREMENTS_SPEC / "spec.md").read_text(encoding="utf-8").split()
    )


# A synthetic repository. Each test plants one defect into it.


def threat(
    number: int,
    title: str = "Something goes wrong",
    rated: tuple[int, int, int, int] = (1, 1, 2, 1),
    held: str = '`thing`: "It works"; DR-001; `demo` task 1.1; `demo` decision 1; `docs/note.md`',
    extra: str = "",
) -> str:
    impact, likelihood, raw_impact, raw_likelihood = rated
    impacts, likelihoods = risk_register.IMPACTS, risk_register.LIKELIHOODS
    return (
        f"### T{number}. {title}\n\n"
        "- **Kind:** tampering\n"
        f"- **Impact:** {impact} ({impacts[impact]})\n"
        f"- **Likelihood:** {likelihood} ({likelihoods[likelihood]})\n"
        f"- **Risk:** {impact * likelihood}\n"
        f"- **Raw impact:** {raw_impact} ({impacts[raw_impact]})\n"
        f"- **Raw likelihood:** {raw_likelihood} ({likelihoods[raw_likelihood]})\n"
        f"- **Raw risk:** {raw_impact * raw_likelihood}\n"
        "- **What could happen:** a thing.\n"
        "- **Answer:** another thing.\n"
        f"- **Held by:** {held}\n"
        f"{extra}"
        "- **Assumptions:** A1\n\n"
    )


METHOD = "## How it was built\n\n1. Draw.\n4. Rate each threat.\n\n"
BOUNDARIES = "The trust boundaries:\n\n1. **One.** The first.\n2. **Two.** The second.\n\n"
FURTHER = "- **Further answer:** B-007\n"


def model(*threats: str, boundaries: tuple[int, ...] = ()) -> str:
    text = "# Threat model\n\nIntro.\n\n" + METHOD + BOUNDARIES
    for number, body in enumerate(threats):
        boundary = boundaries[number] if boundaries else 1
        text += f"## Boundary {boundary}: somewhere\n\n{body}"
    return text + "## Risk matrix\n\nNot read here.\n"


def tree(root: Path, text: str, register: str | None = None) -> Path:
    files = {
        "docs/threat-model.md": text,
        "docs/note.md": "A file.\n",
        "docs/requirements.md": register
        or "| ID | Kind | Capability | Requirement |\n|---|---|---|---|\n"
        "| R1 | functional | `thing` | It does a thing |\n"
        "| R2 | functional | `other` | It does another thing |\n",
        "openspec/changes/demo/specs/thing/spec.md": (
            "## ADDED Requirements\n\n### Requirement: It does a thing\n\nText.\n\n"
            "#### Scenario: It works\n\n- **WHEN** a\n- **THEN** b\n"
        ),
        "openspec/specs/other/spec.md": (
            "## Requirements\n\n### Requirement: It does another thing\n\nText.\n\n"
            "#### Scenario: It also works\n\n- **WHEN** a\n- **THEN** b\n"
        ),
    }
    for name, body in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(body, encoding="utf-8")
    return root


def test_a_model_writes_a_page_that_reads_true(tmp_path: Path) -> None:
    text = model(
        threat(1),
        threat(2, rated=(3, 2, 3, 3), extra=FURTHER),
        threat(3, rated=(1, 2, 2, 2), held='`other`: "It also works"; `thing`: "It works"'),
    )
    root = tree(tmp_path, text)
    page = write(root)
    assert (root / PAGE).read_text(encoding="utf-8") == page
    assert check(root) == []
    assert ROW.findall(page) == ["T2", "T3", "T1"]
    assert row_problems(page, text) == []
    assert matrix_problems(page, text) == []
    assert count_problems(page, text) == []
    assert (
        "| [T1](threat-model.md#t1-something-goes-wrong) | Something goes wrong | 1 | tampering "
        "| 2 low (2, 1) | 1 note (1, 1) "
        "| R1; DR-001; `demo` task 1.1; `demo` decision 1; `docs/note.md` | A1 |" in page
    )
    assert "R2, R1 |" in page
    assert (
        "- [T2](threat-model.md#t2-something-goes-wrong): Something goes wrong. "
        "6 high, raw 9 critical. Further answer: B-007" in page
    )


def test_the_page_opens_by_saying_what_writes_it_and_what_its_ratings_take_as_built(
    tmp_path: Path,
) -> None:
    page = write(tree(tmp_path, model(threat(1))))
    opening = page.split("\n## ")[0]
    assert "`scripts/risk_register.py` writes this page from the threat model" in opening
    assert "not edited by hand" in opening
    assert "takes the answer as built as specified" in opening
    assert "until the review of what was built rates it again" in opening


def test_rows_follow_the_risk_then_the_raw_risk_then_the_id(tmp_path: Path) -> None:
    text = model(
        threat(1, rated=(1, 2, 1, 2)),
        threat(2, rated=(1, 2, 2, 2)),
        threat(3, rated=(2, 1, 2, 2)),
        threat(4, rated=(3, 1, 3, 1)),
    )
    page = write(tree(tmp_path, text))
    assert ROW.findall(page) == ["T4", "T2", "T3", "T1"]


def test_a_file_in_a_folder_that_others_write_is_named_by_its_folder(tmp_path: Path) -> None:
    held = "`vendor/superpowers/UPSTREAM.lock`; `.claude/skills/a/SKILL.md`; `docs/note.md`"
    page = write(tree(tmp_path, model(threat(1, held=held))))
    named = "a file under `vendor/`; a file of a generated skill under `.claude/`; `docs/note.md`"
    assert f"| {named} |" in page
    assert not [
        found for found in hidden_problems(page, ROOT) if "vendor" in found or ".claude" in found
    ]


def test_with_no_high_risk_the_page_says_so(tmp_path: Path) -> None:
    page = write(tree(tmp_path, model(threat(1))))
    assert section_of(page, "High and critical risks")[1][-2] == "None."


@pytest.mark.parametrize(
    ("change", "problem"),
    [
        (
            lambda page: page.replace("| T2 |", "| |", 1),
            "T2 is not in its one cell of the raw matrix",
        ),
        (
            lambda page: page.replace("| 3 high | | T2 | |", "| 3 high | T2 | | |"),
            "T2 is not in its one cell of the matrix with the answers in place",
        ),
        (
            lambda page: page.replace("| 2 medium | T1 |", "| 2 medium | T1, T9 |", 1),
            "the raw matrix names T9, not a threat",
        ),
    ],
)
def test_a_threat_in_a_wrong_cell_of_either_matrix_is_reported(
    tmp_path: Path, change: Callable[[str], str], problem: str
) -> None:
    text = model(threat(1), threat(2, rated=(3, 2, 3, 3), extra=FURTHER))
    page = write(tree(tmp_path, text))
    planted = change(page)
    assert planted != page
    assert problem in matrix_problems(planted, text)


def test_a_band_that_does_not_follow_its_score_is_reported(tmp_path: Path) -> None:
    text = model(threat(1), threat(2, rated=(3, 2, 3, 3), extra=FURTHER))
    page = write(tree(tmp_path, text))
    planted = page.replace("| 6 high (3, 2) |", "| 6 medium (3, 2) |")
    assert planted != page
    assert row_problems(planted, text) == ["T2's row gives a band that its score does not"]
    assert check(tmp_path, planted) == ["T2's row differs from what the script writes"]


def test_band_counts_that_do_not_add_up_are_reported(tmp_path: Path) -> None:
    text = model(threat(1), threat(2, rated=(3, 2, 3, 3), extra=FURTHER))
    page = write(tree(tmp_path, text))
    planted = page.replace("| high | 6 | 0 | 1 |", "| high | 6 | 0 | 2 |")
    assert planted != page
    assert count_problems(planted, text) == [
        "the bands' counts in column 4 do not add up to the threats",
        "the high band's count in column 4 is 2, not 1",
    ]


def add_row(page: str) -> str:
    found = re.search(r"^\| \[T1\].*\n", page, re.M)
    assert found
    row = found.group(0)
    return page.replace(row, row + row.replace("T1", "T7").replace("t1-", "t7-"))


@pytest.mark.parametrize(
    ("change", "problems"),
    [
        (
            lambda page: re.sub(r"^\| \[T1\].*\n", "", page, flags=re.M),
            ["T1 is left out of the register"],
        ),
        (
            lambda page: re.sub(r"^(\| \[T1\].*\n)", r"\1\1", page, flags=re.M),
            ["T1 is listed twice in the register"],
        ),
        (add_row, ["the register lists T7, which the threat model does not hold"]),
        (
            lambda page: page.replace(
                "Something goes wrong | 1 |", "Something went wrong | 1 |", 1
            ),
            ["T1's row differs from what the script writes"],
        ),
        (
            lambda page: page.replace("## Bands\n", "## Bands\n\nA line of its own.\n"),
            ["line 9 of the register is not what the script writes: 'A line of its own.'"],
        ),
    ],
)
def test_a_committed_page_that_differs_is_reported_by_threat_or_line(
    tmp_path: Path, change: Callable[[str], str], problems: list[str]
) -> None:
    root = tree(tmp_path, model(threat(1), threat(2)))
    page = write(root)
    planted = change(page)
    assert planted != page
    assert check(root, planted) == problems


def test_a_page_not_written_yet_is_reported(tmp_path: Path) -> None:
    root = tree(tmp_path, model(threat(1)))
    assert check(root) == [f"{PAGE} does not exist, so run python3 -I scripts/risk_register.py"]


def test_a_scenario_that_no_requirement_holds_stops_the_script(tmp_path: Path) -> None:
    root = tree(tmp_path, model(threat(1, held='`thing`: "It fails"')))
    with pytest.raises(RegisterError) as raised:
        write(root)
    assert raised.value.problems == [
        'T1 cites `thing`: "It fails", which no requirement of the register holds'
    ]
    assert not (root / PAGE).exists()


def test_a_requirement_that_the_register_does_not_list_stops_the_script(tmp_path: Path) -> None:
    register = "| ID | Kind | Capability | Requirement |\n|---|---|---|---|\n"
    root = tree(tmp_path, model(threat(1)), register=register)
    with pytest.raises(RegisterError) as raised:
        write(root)
    assert raised.value.problems == [
        'T1 cites `thing`: "It works", which no requirement of the register holds'
    ]


@pytest.mark.parametrize("mark", ["|", "<", "&", "\\", "]:", "é", "\t"])
def test_a_title_that_the_rule_forbids_stops_the_script(tmp_path: Path, mark: str) -> None:
    root = tree(tmp_path, model(threat(1, title=f"Something {mark} goes wrong")))
    with pytest.raises(RegisterError) as raised:
        write(root)
    assert [problem for problem in raised.value.problems if problem.startswith("T1's title holds ")]
    assert not (root / PAGE).exists()


@pytest.mark.parametrize(
    ("name", "line"),
    [
        ("kind", "- **Kind:** tampering\n"),
        ("assumptions", "- **Assumptions:** A1\n"),
        ("further answer", "- **Further answer:** B-007\n"),
        ("acceptance", "- **Acceptance:** DR-001\n"),
        ("Held by", '- **Held by:** `thing`: "It works"; DR-001\n'),
    ],
)
@pytest.mark.parametrize("mark", ["<", "&", "]:", "é"])
def test_text_that_the_rule_forbids_in_a_copied_field_stops_the_script(
    tmp_path: Path, name: str, line: str, mark: str
) -> None:
    body = threat(
        1, held='`thing`: "It works"; DR-001', extra=FURTHER + "- **Acceptance:** DR-001\n"
    )
    assert line in body
    planted = (
        line.replace("\n", f" {mark} x\n")
        if name != "Held by"
        else line.replace("; DR-001", f"; `docs/{mark}x.md`")
    )
    root = tree(tmp_path, model(body.replace(line, planted, 1)))
    with pytest.raises(RegisterError) as raised:
        write(root)
    assert [each for each in raised.value.problems if each.startswith(f"T1's {name} holds ")]
    assert not (root / PAGE).exists()


@pytest.mark.parametrize("name", ["docs/threat-model.md", "docs/requirements.md", PAGE, "docs"])
def test_a_symbolic_link_on_the_way_to_a_file_that_the_script_reads_or_writes_stops_it(
    tmp_path: Path, name: str
) -> None:
    root = tree(tmp_path / "repository", model(threat(1)))
    write(root)
    outside = tmp_path / "outside"
    outside.mkdir()
    moved = root / name
    moved.rename(outside / moved.name)
    moved.symlink_to(outside / moved.name)
    before = {path: path.read_bytes() for path in outside.rglob("*") if path.is_file()}
    for run in (write, check):
        with pytest.raises(RegisterError) as raised:
            run(root)
        (problem,) = raised.value.problems
        assert problem.endswith(" is a symbolic link, which the script does not follow")
        assert problem.startswith(name if name != "docs" else "docs/")
    assert {path: path.read_bytes() for path in outside.rglob("*") if path.is_file()} == before


@pytest.mark.parametrize(
    ("field", "problem"),
    [
        ("- **Raw impact:** 2 (low)\n", "T1 has no raw impact that the script can read"),
        ("- **Likelihood:** 4 (certain)\n", "T1 has no likelihood that the script can read"),
    ],
)
def test_a_rating_that_the_script_cannot_read_stops_it(
    tmp_path: Path, field: str, problem: str
) -> None:
    name = field.split(":**")[0]
    body = re.sub(rf"^{re.escape(name)}:\*\* .*\n", field, threat(1), flags=re.M)
    root = tree(tmp_path, model(body))
    with pytest.raises(RegisterError) as raised:
        write(root)
    assert problem in raised.value.problems


def test_a_threat_model_with_no_threat_stops_the_script(tmp_path: Path) -> None:
    root = tree(tmp_path, model())
    with pytest.raises(RegisterError) as raised:
        write(root)
    assert raised.value.problems == ["the threat model holds no threat"]


@pytest.mark.parametrize(
    ("planted", "problem"),
    [
        ("See [a site](https://example.com).", "gives a web address"),
        ("See [a page](../../outside.md).", "leaves the repository"),
        ("A <!-- hidden --> note.", "holds <, with which Markdown starts HTML"),
        ("A | outside a table.", "holds |, with which Markdown builds a table"),
        ("A \\ mark.", "holds a backslash"),
        ("| a | b | c |", "holds a row whose cells differ from its header's"),
    ],
)
def test_text_that_github_hides_or_a_link_outside_the_repository_is_reported(
    tmp_path: Path, planted: str, problem: str
) -> None:
    page = write(tree(tmp_path, model(threat(1))))
    assert not [found for found in hidden_problems(page, ROOT) if problem in found]
    if planted.startswith("| "):
        page = page.replace("|---|---|---|---|\n", f"|---|---|---|---|\n{planted}\n", 1)
    else:
        page = page.replace("\n## Bands\n", f"\n{planted}\n\n## Bands\n", 1)
    assert [found for found in hidden_problems(page, ROOT) if problem in found]


def test_the_blind_copy_holds_no_rating(tmp_path: Path) -> None:
    text = model(threat(1), threat(2, rated=(3, 2, 3, 3), extra=FURTHER), boundaries=(1, 2))
    root = tree(tmp_path, text)
    copy = blind(root, 2)
    assert "### T2. Something goes wrong" in copy and "### T1." not in copy
    assert "- **Further answer:** B-007" in copy
    assert "2. **Two.** The second." in copy and "4. Rate each threat." in copy
    assert not re.search(r"Impact|Likelihood|Risk|matrix", copy)


@pytest.mark.parametrize(
    ("held", "shown"),
    [
        ('`thing`: "It works"; DR-009', '`thing`: "It works"'),
        ('DR-009; `thing`: "It works"; DR-001', '`thing`: "It works"; DR-001'),
        ('`thing`: "It works"; DR-009; DR-001', '`thing`: "It works"; DR-001'),
    ],
)
def test_the_blind_copy_holds_no_acceptance_nor_the_record_it_cites(
    tmp_path: Path, held: str, shown: str
) -> None:
    accepted = "- **Acceptance:** DR-009: the owner accepts it.\n"
    root = tree(tmp_path, model(threat(1, rated=(3, 2, 3, 3), held=held, extra=accepted)))
    copy = blind(root, 1)
    assert f"- **Held by:** {shown}\n" in copy
    assert "Acceptance" not in copy and "DR-009" not in copy


def test_the_blind_copy_of_a_boundary_with_no_threat_is_refused(tmp_path: Path) -> None:
    root = tree(tmp_path, model(threat(1)))
    with pytest.raises(RegisterError) as raised:
        blind(root, 2)
    assert raised.value.problems == ["the threat model holds no threat at boundary 2"]


@pytest.mark.parametrize(
    ("argv", "code"),
    [
        ([], 0),
        (["--check"], 0),
        (["--blind", "1"], 0),
        (["--blind", "2"], 1),
        (["--blind"], 2),
        (["--blind", "\u00b2"], 2),
        (["--blind", "-1"], 2),
        (["--other"], 2),
    ],
)
def test_the_command_line(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, argv: list[str], code: int
) -> None:
    root = tree(tmp_path, model(threat(1)))
    write(root)
    monkeypatch.setattr(risk_register, "ROOT", root)
    assert risk_register.main(argv) == code


def test_the_command_line_fails_on_a_page_that_differs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tree(tmp_path, model(threat(1)))
    write(root)
    (root / PAGE).write_text("A page by hand.\n", encoding="utf-8")
    monkeypatch.setattr(risk_register, "ROOT", root)
    assert risk_register.main(["--check"]) == 1
    assert "risk_register: T1 is left out of the register" in capsys.readouterr().err


def test_the_command_line_writes_nothing_on_an_input_that_it_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tree(tmp_path, model(threat(1, held='`thing`: "It fails"')))
    monkeypatch.setattr(risk_register, "ROOT", root)
    assert risk_register.main([]) == 1
    assert "risk_register: T1 cites" in capsys.readouterr().err
    assert not (root / PAGE).exists()
