"""The threat model's answers point at things that exist.

`docs/threat-model.md` lists each threat with what holds its answer: a scenario
in a spec, a task or a decision of a change, a decision record, or a file in this
repository. A citation that names nothing reads as a control while holding none,
so every citation must resolve, and every threat must cite something or say why
it is accepted. A scenario resolves only in `openspec/specs/` and the active
changes, so that a title that a rewording changed cannot pass on an archived
copy. `tests/test_decisions.py` also fails when an answer cites a closed record,
since a closed decision no longer holds anything.

Threats are numbered from T1 in order. A threat that a change removes keeps its
number out of use in the list of retired IDs, so that a record or a document
citing it never comes to cite another threat. Only the section "Retired IDs"
retires an ID.

Each line of a threat is one of its fields. A line that is not would show on
GitHub as part of the field above it, while no check here would read it.

Every threat is also rated for impact and likelihood, from 1 to 3 each, and its
risk is their product. The risk matrix places each threat in the cell its two
ratings name, so a reader sees at a glance where the risk sits, and a rating
changed in one place and not the other is reported.

The model's opening says how many threats it holds and across how many trust
boundaries. A threat added without that sentence changing makes it wrong, so
the figures are compared with the threats' headings and the boundaries' headings.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
THREAT_MODEL = ROOT / "docs" / "threat-model.md"

FIELDS = ("Kind", "Impact", "Likelihood", "Risk", "What could happen", "Answer", "Held by")
KINDS = {
    "spoofing",
    "tampering",
    "repudiation",
    "information disclosure",
    "denial of service",
    "elevation of privilege",
    "reliability",
}
IMPACTS = {1: "low", 2: "medium", 3: "high"}
LIKELIHOODS = {1: "unlikely", 2: "possible", 3: "likely"}

HEADING = re.compile(r"^### (T(\d+))\. .+$", re.M)
ANY_HEADING = re.compile(r"^#{1,3} ", re.M)
FIELD = re.compile(r"^- \*\*([^*]+):\*\* ?(.*)$", re.M)
SCENARIO = re.compile(r"^#### Scenario: (.+?)\s*$", re.M)
SCENARIO_REF = re.compile(r'`([a-z0-9-]+)`: "([^"]+)"')
TASK_REF = re.compile(r"`([a-z0-9-]+)` task (\d+\.\d+)")
DECISION_REF = re.compile(r"`([a-z0-9-]+)` decision (\d+)")
RECORD_REF = re.compile(r"\bDR-(\d{3,})\b")
RETIRED = re.compile(r"^- T(\d+), removed by `[a-z0-9-]+`", re.M)
RETIRED_SECTION = re.compile(r"^## Retired IDs\n(.*?)(?=^## |\Z)", re.M | re.S)
PATH_REF = re.compile(r"`([^`\s]+)`")
ARCHIVE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
RATING = re.compile(r"([1-3]) \(([a-z]+)\)")
MATRIX_HEADING = re.compile(r"^## Risk matrix$", re.M)
MATRIX_ROW = re.compile(r"^\| ([1-3]) [a-z]+ \|(.*)\|\s*$", re.M)
THREAT_ID = re.compile(r"T\d+")
COUNT = re.compile(r"\bIt holds (\d+) threats across (\d+) trust boundaries\b")
BOUNDARY = re.compile(r"^## Boundary (\d+)\b", re.M)


@dataclass(frozen=True)
class Threat:
    ident: str
    number: int
    fields: dict[str, list[str]]
    others: tuple[str, ...] = ()


@dataclass(frozen=True)
class Index:
    scenarios: dict[str, set[str]]
    changes: dict[str, Path]


def threats_in(text: str) -> list[Threat]:
    marks = list(HEADING.finditer(text))
    found = []
    for mark in marks:
        body = text[mark.end() :]
        following = ANY_HEADING.search(body)
        if following:
            body = body[: following.start()]
        fields: dict[str, list[str]] = {}
        for field in FIELD.finditer(body):
            fields.setdefault(field.group(1), []).append(field.group(2).strip())
        # A line that is not a field is part of the field above it on GitHub, unread here.
        others = tuple(line for line in body.split("\n") if line.strip() and not FIELD.match(line))
        found.append(Threat(mark.group(1), int(mark.group(2)), fields, others))
    return found


def index(root: Path) -> Index:
    scenarios: dict[str, set[str]] = {}
    # A scenario resolves only where the specs hold it now, never in an archived copy.
    specs = [
        *(root / "openspec" / "specs").glob("*/spec.md"),
        *(root / "openspec" / "changes").glob("*/specs/*/spec.md"),
    ]
    for spec in sorted(specs):
        scenarios.setdefault(spec.parent.name, set()).update(SCENARIO.findall(spec.read_text()))
    changes: dict[str, Path] = {}
    base = root / "openspec" / "changes"
    for folder in sorted(base.glob("*")) + sorted((base / "archive").glob("*")):
        if folder.is_dir() and folder.name != "archive":
            changes[ARCHIVE_DATE.sub("", folder.name)] = folder
    return Index(scenarios, changes)


@dataclass(frozen=True)
class Citations:
    """What a Held by cites, by kind."""

    scenarios: list[tuple[str, str]]
    tasks: list[tuple[str, str]]
    decisions: list[tuple[str, str]]
    records: list[str]
    paths: list[str]


def citations(held: str) -> Citations:
    """Each kind is read from what the kinds before it leave, so that the name of a
    capability or a change, which is in backticks, is not read as a path."""
    scenarios = SCENARIO_REF.findall(held)
    rest = SCENARIO_REF.sub("", held)
    tasks = TASK_REF.findall(rest)
    rest = TASK_REF.sub("", rest)
    decisions = DECISION_REF.findall(rest)
    rest = DECISION_REF.sub("", rest)
    records = RECORD_REF.findall(rest)
    paths = PATH_REF.findall(RECORD_REF.sub("", rest))
    return Citations(scenarios, tasks, decisions, records, paths)


def citation_problems(ident: str, held: str, found: Index, root: Path) -> tuple[list[str], int]:
    problems: list[str] = []
    cited = citations(held)
    for capability, name in cited.scenarios:
        if name not in found.scenarios.get(capability, set()):
            problems.append(f'{ident} cites `{capability}`: "{name}", which no spec holds')
    for change, number in cited.tasks:
        tasks = found.changes[change] / "tasks.md" if change in found.changes else None
        line = re.compile(rf"^- \[[ x]\] {re.escape(number)} ", re.M)
        if tasks is None or not tasks.is_file() or not line.search(tasks.read_text()):
            problems.append(f"{ident} cites `{change}` task {number}, which does not exist")
    for change, number in cited.decisions:
        design = found.changes[change] / "design.md" if change in found.changes else None
        heading = re.compile(rf"^### {re.escape(number)}\. ", re.M)
        if design is None or not design.is_file() or not heading.search(design.read_text()):
            problems.append(f"{ident} cites `{change}` decision {number}, which does not exist")
    for number in cited.records:
        if not sorted((root / "docs" / "decisions").glob(f"DR-{number}-*.md")):
            problems.append(f"{ident} cites DR-{number}, which is not a decision record")
    for path in cited.paths:
        target = (root / path).resolve()
        if root.resolve() not in target.parents or not target.exists():
            problems.append(f"{ident} cites `{path}`, which is not a file in this repository")
    count = sum(
        len(kind)
        for kind in (cited.scenarios, cited.tasks, cited.decisions, cited.records, cited.paths)
    )
    return problems, count


def problems_in(text: str, root: Path) -> tuple[list[str], int]:
    threats = threats_in(text)
    if not threats:
        return ["no threat found"], 0
    problems: list[str] = []
    numbers = [threat.number for threat in threats]
    section = RETIRED_SECTION.search(text)
    retired = {int(number) for number in RETIRED.findall(section.group(1) if section else "")}
    last = max([*numbers, *retired])
    if numbers != [n for n in range(1, last + 1) if n not in retired]:
        problems.append(
            f"threats are not numbered T1 to T{last} in order, apart from retired IDs: {numbers}"
        )
    found = index(root)
    cited = 0
    for threat in threats:
        problems += [
            f"{threat.ident} has a line that is not a field, which no check reads: {line!r}"
            for line in threat.others
        ]
        missing = [name for name in FIELDS if not threat.fields.get(name)]
        doubled = [name for name, values in threat.fields.items() if len(values) > 1]
        if missing or doubled:
            problems.append(f"{threat.ident} lacks {missing} or repeats {doubled}")
            continue
        kinds = [kind.strip() for kind in threat.fields["Kind"][0].split(",")]
        unknown = [kind for kind in kinds if kind not in KINDS]
        if unknown:
            problems.append(f"{threat.ident} has a kind outside the list: {unknown}")
        problems += rating_problems(threat)
        held = threat.fields["Held by"][0]
        if held.lower().startswith("accepted"):
            if not re.match(r"accepted: \S", held):
                problems.append(f"{threat.ident} is accepted without a reason")
            continue
        found_problems, count = citation_problems(threat.ident, held, found, root)
        problems += found_problems
        cited += count
        if count == 0:
            problems.append(f"{threat.ident} cites nothing and is not accepted")
    problems += matrix_problems(text, threats)
    return problems, cited


def rating(value: str, levels: dict[int, str]) -> int | None:
    match = RATING.fullmatch(value)
    if not match or levels.get(int(match.group(1))) != match.group(2):
        return None
    return int(match.group(1))


def rating_problems(threat: Threat) -> list[str]:
    impact = rating(threat.fields["Impact"][0], IMPACTS)
    likelihood = rating(threat.fields["Likelihood"][0], LIKELIHOODS)
    problems = []
    if impact is None:
        problems.append(f"{threat.ident} has an impact outside the list")
    if likelihood is None:
        problems.append(f"{threat.ident} has a likelihood outside the list")
    if impact and likelihood and threat.fields["Risk"][0] != str(impact * likelihood):
        problems.append(f"{threat.ident} has a risk that is not impact times likelihood")
    return problems


def matrix_problems(text: str, threats: list[Threat]) -> list[str]:
    heading = MATRIX_HEADING.search(text)
    if not heading:
        return ["no risk matrix found"]
    body = text[heading.end() :]
    following = ANY_HEADING.search(body)
    if following:
        body = body[: following.start()]
    placed: dict[str, list[tuple[int, int]]] = {}
    rows = MATRIX_ROW.findall(body)
    for impact, cells in rows:
        columns = [cell.strip() for cell in cells.split("|")]
        if len(columns) != len(LIKELIHOODS):
            return [f"the risk matrix row for impact {impact} does not have three columns"]
        for likelihood, cell in enumerate(columns, start=1):
            for ident in THREAT_ID.findall(cell):
                placed.setdefault(ident, []).append((int(impact), likelihood))
    if sorted(int(impact) for impact, _ in rows) != sorted(IMPACTS):
        return ["the risk matrix does not have one row for each impact"]
    problems = []
    for threat in threats:
        expected = [
            (
                rating(threat.fields.get("Impact", [""])[0], IMPACTS) or 0,
                rating(threat.fields.get("Likelihood", [""])[0], LIKELIHOODS) or 0,
            )
        ]
        if placed.pop(threat.ident, []) != expected:
            problems.append(f"{threat.ident} is not in the one risk matrix cell its ratings name")
    problems += [f"the risk matrix names {ident}, which is not a threat" for ident in placed]
    return problems


def count_problems(text: str, threats: list[Threat]) -> list[str]:
    counts = COUNT.findall(text)
    if len(counts) != 1:
        return ['the model does not say once "It holds N threats across M trust boundaries"']
    held, boundaries = (int(value) for value in counts[0])
    named = len(set(BOUNDARY.findall(text)))
    problems = []
    if held != len(threats):
        problems.append(f"the model says it holds {held} threats, and it holds {len(threats)}")
    if boundaries != named:
        problems.append(
            f"the model says it has {boundaries} trust boundaries, and its headings name {named}"
        )
    return problems


def test_every_threat_cites_what_holds_its_answer() -> None:
    problems, cited = problems_in(THREAT_MODEL.read_text(), ROOT)
    assert not problems, "\n".join(problems)
    assert cited, "no citation was checked, so this test covered nothing"


def synthetic_repository(root: Path) -> None:
    change = root / "openspec" / "changes" / "demo"
    (change / "specs" / "thing").mkdir(parents=True)
    (change / "specs" / "thing" / "spec.md").write_text("#### Scenario: It works\n")
    (change / "tasks.md").write_text("- [ ] 1.1 Do it\n- [x] 1.2 Did it\n")
    (change / "design.md").write_text("### 1. A choice\n")
    old = root / "openspec" / "changes" / "archive" / "2026-01-01-old"
    old.mkdir(parents=True)
    (old / "tasks.md").write_text("- [x] 3.1 Done long ago\n")
    (root / "docs").mkdir()
    (root / "docs" / "note.md").write_text("A file.\n")
    (root / "docs" / "decisions").mkdir()
    (root / "docs" / "decisions" / "DR-001-a-choice.md").write_text("# DR-001: A choice\n")


MATRIX = (
    "## Risk matrix\n\n"
    "| Impact \\ Likelihood | 1 unlikely | 2 possible | 3 likely |\n"
    "|---|---|---|---|\n"
    "| 3 high | | | |\n"
    "| 2 medium | | | |\n"
    "| 1 low | {low} | | |\n"
)


def matrix(low: str = "T1") -> str:
    return MATRIX.format(low=low)


def threat(
    held: str,
    number: int = 1,
    kind: str = "tampering",
    impact: str = "1 (low)",
    likelihood: str = "1 (unlikely)",
    risk: str = "1",
) -> str:
    return (
        f"### T{number}. Something goes wrong\n\n"
        f"- **Kind:** {kind}\n"
        f"- **Impact:** {impact}\n"
        f"- **Likelihood:** {likelihood}\n"
        f"- **Risk:** {risk}\n"
        "- **What could happen:** a thing.\n"
        "- **Answer:** another thing.\n"
        f"- **Held by:** {held}\n"
    )


def test_citations_that_exist_resolve(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    held = (
        '`thing`: "It works"; `demo` task 1.1; `demo` task 1.2; `old` task 3.1; '
        "`demo` decision 1; DR-001; `docs/note.md`"
    )
    assert problems_in(threat(held) + matrix(), tmp_path) == ([], 7)


def test_a_record_in_backticks_is_read_as_a_record(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    assert problems_in(threat("`DR-001`") + matrix(), tmp_path) == ([], 1)


def test_an_accepted_risk_with_its_reason_cites_nothing(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    text = threat("accepted: the report is an estimate.") + matrix()
    assert problems_in(text, tmp_path) == ([], 0)


@pytest.mark.parametrize(
    ("held", "expected"),
    [
        ('`thing`: "It fails"', 'cites `thing`: "It fails", which no spec holds'),
        ('`other`: "It works"', 'cites `other`: "It works", which no spec holds'),
        ("`demo` task 9.9", "cites `demo` task 9.9, which does not exist"),
        ("`missing` task 1.1", "cites `missing` task 1.1, which does not exist"),
        ("`demo` decision 2", "cites `demo` decision 2, which does not exist"),
        ("DR-002", "cites DR-002, which is not a decision record"),
        ("DR-01", "cites nothing and is not accepted"),
        ("`docs/absent.md`", "cites `docs/absent.md`, which is not a file in this repository"),
        ("`../outside.md`", "cites `../outside.md`, which is not a file in this repository"),
        ("the hook, somehow", "cites nothing and is not accepted"),
        ("accepted", "is accepted without a reason"),
    ],
)
def test_a_citation_that_names_nothing_is_reported(
    tmp_path: Path, held: str, expected: str
) -> None:
    synthetic_repository(tmp_path)
    (tmp_path.parent / "outside.md").write_text("Outside the repository.\n")
    problems, _ = problems_in(threat(held) + matrix(), tmp_path)
    assert [problem for problem in problems if expected in problem], problems


def test_a_scenario_that_the_specs_hold_resolves(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    specs = tmp_path / "openspec" / "specs" / "thing"
    specs.mkdir(parents=True)
    (specs / "spec.md").write_text("#### Scenario: It holds\n")
    assert problems_in(threat('`thing`: "It holds"') + matrix(), tmp_path) == ([], 1)


def test_a_scenario_that_only_an_archived_change_holds_does_not_resolve(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    archived = tmp_path / "openspec" / "changes" / "archive" / "2026-01-01-old" / "specs"
    (archived / "thing").mkdir(parents=True)
    (archived / "thing" / "spec.md").write_text("#### Scenario: It once worked\n")
    problems, _ = problems_in(threat('`thing`: "It once worked"') + matrix(), tmp_path)
    assert problems == ['T1 cites `thing`: "It once worked", which no spec holds']


def test_a_threat_without_its_fields_is_reported(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    text = threat("`docs/note.md`").replace("- **Answer:** another thing.\n", "") + matrix()
    problems, _ = problems_in(text, tmp_path)
    assert problems == ["T1 lacks ['Answer'] or repeats []"]


def test_a_repeated_field_is_reported(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    text = threat("`docs/note.md`") + "- **Held by:** `docs/note.md`\n" + matrix()
    problems, _ = problems_in(text, tmp_path)
    assert problems == ["T1 lacks [] or repeats ['Held by']"]


def test_kinds_and_impacts_come_from_their_lists(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    text = threat("`docs/note.md`", kind="tampering, mischief", impact="huge") + matrix()
    problems, _ = problems_in(text, tmp_path)
    assert problems == [
        "T1 has a kind outside the list: ['mischief']",
        "T1 has an impact outside the list",
        "T1 is not in the one risk matrix cell its ratings name",
    ]


@pytest.mark.parametrize(
    ("impact", "likelihood", "risk", "expected"),
    [
        ("3 (high)", "2 (possible)", "6", []),
        ("2 (medium)", "3 (likely)", "6", []),
        ("3 (medium)", "1 (unlikely)", "3", ["T1 has an impact outside the list"]),
        ("high", "1 (unlikely)", "3", ["T1 has an impact outside the list"]),
        ("1 (low)", "4 (certain)", "4", ["T1 has a likelihood outside the list"]),
        ("1 (low)", "2 (likely)", "2", ["T1 has a likelihood outside the list"]),
        ("2 (medium)", "2 (possible)", "2", ["T1 has a risk that is not impact times likelihood"]),
        (
            "3 (high)",
            "3 (likely)",
            "9 (high)",
            ["T1 has a risk that is not impact times likelihood"],
        ),
    ],
)
def test_a_rating_is_a_level_from_its_list_and_risk_is_their_product(
    tmp_path: Path, impact: str, likelihood: str, risk: str, expected: list[str]
) -> None:
    synthetic_repository(tmp_path)
    held = "`docs/note.md`"
    text = threat(held, impact=impact, likelihood=likelihood, risk=risk)
    problems, _ = problems_in(text + matrix(""), tmp_path)
    assert [p for p in problems if "risk matrix" not in p] == expected


def test_each_threat_sits_in_the_matrix_cell_its_ratings_name(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    text = threat("`docs/note.md`", impact="3 (high)", likelihood="2 (possible)", risk="6")
    placed = MATRIX.format(low="").replace("| 3 high | | | |", "| 3 high | | T1 | |")
    assert problems_in(text + placed, tmp_path) == ([], 1)


@pytest.mark.parametrize(
    ("low", "expected"),
    [
        ("", ["T1 is not in the one risk matrix cell its ratings name"]),
        ("T1, T1", ["T1 is not in the one risk matrix cell its ratings name"]),
        ("T1, T2", ["the risk matrix names T2, which is not a threat"]),
    ],
)
def test_a_threat_missing_doubled_or_unknown_in_the_matrix_is_reported(
    tmp_path: Path, low: str, expected: list[str]
) -> None:
    synthetic_repository(tmp_path)
    problems, _ = problems_in(threat("`docs/note.md`") + matrix(low), tmp_path)
    assert problems == expected


def test_a_threat_in_the_wrong_cell_is_reported(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    moved = MATRIX.format(low="").replace("| 2 medium | | | |", "| 2 medium | T1 | | |")
    problems, _ = problems_in(threat("`docs/note.md`") + moved, tmp_path)
    assert problems == ["T1 is not in the one risk matrix cell its ratings name"]


def test_a_matrix_that_is_missing_or_malformed_is_reported(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    text = threat("`docs/note.md`")
    assert problems_in(text, tmp_path)[0] == ["no risk matrix found"]
    short = matrix().replace("| 2 medium | | | |\n", "")
    assert problems_in(text + short, tmp_path)[0] == [
        "the risk matrix does not have one row for each impact"
    ]
    narrow = matrix().replace("| 1 low | T1 | | |", "| 1 low | T1 | |")
    assert problems_in(text + narrow, tmp_path)[0] == [
        "the risk matrix row for impact 1 does not have three columns"
    ]


def test_threats_are_numbered_in_order(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    text = threat("`docs/note.md`", number=1) + "\n" + threat("`docs/note.md`", number=3)
    problems, _ = problems_in(text + matrix("T1, T3"), tmp_path)
    assert problems == [
        "threats are not numbered T1 to T3 in order, apart from retired IDs: [1, 3]"
    ]


def test_a_retired_id_leaves_a_gap_in_the_numbers(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    text = threat("`docs/note.md`", number=1) + "\n" + threat("`docs/note.md`", number=3)
    retired = "\n## Retired IDs\n\n- T2, removed by `demo`\n- T4, removed by `demo`\n"
    assert problems_in(text + matrix("T1, T3") + retired, tmp_path) == ([], 2)


@pytest.mark.parametrize(
    ("numbers", "retired", "expected"),
    [
        ([1, 2], "- T2, removed by `demo`\n", "T1 to T2 in order, apart from retired IDs: [1, 2]"),
        ([1, 3], "- T2, removed\n", "T1 to T3 in order, apart from retired IDs: [1, 3]"),
        ([2, 1], "", "T1 to T2 in order, apart from retired IDs: [2, 1]"),
    ],
)
def test_a_retired_id_still_in_use_or_without_its_change_is_reported(
    tmp_path: Path, numbers: list[int], retired: str, expected: str
) -> None:
    synthetic_repository(tmp_path)
    text = "\n".join(threat("`docs/note.md`", number=n) for n in numbers)
    placed = matrix(", ".join(f"T{n}" for n in numbers))
    problems, _ = problems_in(text + placed + "\n## Retired IDs\n\n" + retired, tmp_path)
    assert problems == [f"threats are not numbered {expected}"]


def test_a_field_that_runs_onto_another_line_is_reported(tmp_path: Path) -> None:
    # GitHub shows the line as part of the field, and no check here would read it.
    synthetic_repository(tmp_path)
    text = threat("`docs/note.md`") + "  DR-002; `docs/absent.md`\n" + matrix()
    problems, _ = problems_in(text, tmp_path)
    assert problems == [
        "T1 has a line that is not a field, which no check reads: '  DR-002; `docs/absent.md`'"
    ]


def test_a_retired_id_outside_its_section_explains_no_gap(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    text = "# Threats\n\n- T2, removed by `demo`\n\n" + threat("`docs/note.md`", number=1)
    text += "\n" + threat("`docs/note.md`", number=3) + matrix("T1, T3")
    problems, _ = problems_in(text + "\n## Retired IDs\n\nNone yet.\n", tmp_path)
    assert problems == [
        "threats are not numbered T1 to T3 in order, apart from retired IDs: [1, 3]"
    ]


def test_a_document_without_threats_is_reported(tmp_path: Path) -> None:
    synthetic_repository(tmp_path)
    assert problems_in("# Threat model\n\nNothing here.\n", tmp_path) == (["no threat found"], 0)


def test_the_model_counts_its_threats_and_trust_boundaries() -> None:
    text = THREAT_MODEL.read_text()
    assert threats_in(text), "no threat was read, so this test covered nothing"
    assert count_problems(text, threats_in(text)) == []


def counted(sentence: str) -> str:
    return (
        f"# Threat model\n\n{sentence}\n\n## Boundary 1: one\n\n"
        + threat("`docs/note.md`", number=1)
        + "\n## Boundary 2: two\n\n"
        + threat("`docs/note.md`", number=2)
        + "\n## Boundary 2, continued: found later\n\n"
        + threat("`docs/note.md`", number=3)
    )


def test_a_count_that_matches_the_headings_passes() -> None:
    text = counted("It holds 3 threats across 2 trust boundaries.")
    assert count_problems(text, threats_in(text)) == []


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        (
            "It holds 2 threats across 2 trust boundaries.",
            ["the model says it holds 2 threats, and it holds 3"],
        ),
        (
            "It holds 3 threats across 3 trust boundaries.",
            ["the model says it has 3 trust boundaries, and its headings name 2"],
        ),
        (
            "It holds threats across trust boundaries.",
            ['the model does not say once "It holds N threats across M trust boundaries"'],
        ),
        (
            "It holds 3 threats across 2 trust boundaries. It holds 3 threats across 2 trust"
            " boundaries.",
            ['the model does not say once "It holds N threats across M trust boundaries"'],
        ),
    ],
)
def test_a_count_that_the_headings_do_not_bear_out_is_reported(
    sentence: str, expected: list[str]
) -> None:
    text = counted(sentence)
    assert count_problems(text, threats_in(text)) == expected
