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

import os
import re
from dataclasses import dataclass
from dataclasses import fields as dataclass_fields
from pathlib import Path
from typing import TypedDict

import pytest
from risk_register import (
    BANDS,
    FURTHER,
    IMPACTS,
    LIKELIHOODS,
    RECORD_REF,
    Citations,
    Threat,
    citations,
    plan_items,
    rating,
    score_of,
    threats_in,
)
from test_backlog import AGREED, Item, backlog_items, items_in
from test_decisions import DECIDER, Record, attribute_problems, base_commits, git, records_of
from test_roadmap import (
    hidden_text_problems_in,
    link_problems_in,
    saved_with_windows_line_endings,
)

ROOT = Path(__file__).resolve().parents[1]
THREAT_MODEL = ROOT / "docs" / "threat-model.md"

FIELDS = (
    "Kind",
    "Impact",
    "Likelihood",
    "Risk",
    "Raw impact",
    "Raw likelihood",
    "Raw risk",
    "What could happen",
    "Answer",
    "Held by",
)
KINDS = {
    "spoofing",
    "tampering",
    "repudiation",
    "information disclosure",
    "denial of service",
    "elevation of privilege",
    "reliability",
}
# Each rating with the answer in place, and the raw rating that may not be lower (R244).
PAIRS = (("Impact", "Raw impact", IMPACTS), ("Likelihood", "Raw likelihood", LIKELIHOODS))
KINDS_OF_CITATION = [kind.name for kind in dataclass_fields(Citations)]
# What a pull request changes with a high rating that it lowers, so that its reason shows (R250).
REASONS = ("What could happen", "Answer", "Held by", "Further answer")

SCENARIO = re.compile(r"^#### Scenario: (.+?)\s*$", re.M)
RETIRED = re.compile(r"^- T(\d+), removed by `[a-z0-9-]+`", re.M)
RETIRED_SECTION = re.compile(r"^## Retired IDs\n(.*?)(?=^## |\Z)", re.M | re.S)
ARCHIVE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
ANY_HEADING = re.compile(r"^#{1,3} ", re.M)
MATRIX_HEADING = re.compile(r"^## Risk matrix$", re.M)
MATRIX_ROW = re.compile(r"^\| ([1-3]) [a-z]+ \|(.*)\|\s*$", re.M)
THREAT_ID = re.compile(r"T\d+")
COUNT = re.compile(r"\bIt holds (\d+) threats across (\d+) trust boundaries\b")
BOUNDARY = re.compile(r"^## Boundary (\d+)\b", re.M)
WHAT_DONE = re.compile(r"^## What done looks like\n(.*?)(?=^## |\Z)", re.M | re.S)


@dataclass(frozen=True)
class Index:
    scenarios: dict[str, set[str]]
    changes: dict[str, Path]


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
    return problems, len(cited)


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


def rating_problems(threat: Threat) -> list[str]:
    """Each rating a level from its list, each risk the product of its two, and neither raw
    rating lower than its rating with the answer in place (R31, R244)."""
    problems = []
    given = {}
    for low, raw, levels in PAIRS:
        for name in (low, raw):
            given[name] = rating(threat.fields[name][0], levels)
            if not given[name]:
                article = "an" if name == "Impact" else "a"
                problems.append(f"{threat.ident} has {article} {name.lower()} outside the list")
    for risk, impact, likelihood in (
        ("Risk", "Impact", "Likelihood"),
        ("Raw risk", "Raw impact", "Raw likelihood"),
    ):
        product = given[impact] * given[likelihood]
        if product and threat.fields[risk][0] != str(product):
            problems.append(
                f"{threat.ident} has a {risk.lower()} that is not {impact.lower()} times "
                f"{likelihood.lower()}"
            )
    for low, raw, _ in PAIRS:
        if given[low] and given[raw] and given[raw] < given[low]:
            problems.append(f"{threat.ident} has a {raw.lower()} lower than its {low.lower()}")
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
                rating(threat.field("Impact"), IMPACTS),
                rating(threat.field("Likelihood"), LIKELIHOODS),
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


def further_problems(text: str, root: Path, bases: list[str]) -> list[str]:
    """R249: each high or critical risk carries a further answer that adds to its Held by,
    or, if high, an acceptance that an open record of the owner's gives for it; neither
    line, on any threat, holds text that the roadmap's rule forbids. A backlog item that a
    further answer cites is Planned or In progress at each base and in this tree, and its
    What done looks like, as this tree holds it, names the threat."""
    found = index(root)
    records, _ = records_of(root / "docs" / "decisions")
    items = {item.ident: item for item in backlog_items(root)}
    statuses = [
        (base, {item.ident: item.status for item in items_in(root, base).values()})
        for base in bases
    ]
    problems = []
    for threat in threats_in(text):
        named = BANDS.get(score_of(threat), "")
        further, accepted = threat.field("Further answer"), threat.field("Acceptance")
        for name, value in (("further answer", further), ("acceptance", accepted)):
            if value:
                problems += rule_problems(f"{threat.ident}'s {name}", value, root)
        if named in FURTHER and not further and not accepted:
            problems.append(
                f"{threat.ident} is {named} and carries neither a further answer nor an acceptance"
            )
        if further:
            problems += further_answer_problems(threat, found, root, items, statuses)
        if accepted:
            if named == "critical":
                problems.append(f"{threat.ident} is critical and carries an acceptance")
            problems += acceptance_problems(threat, records)
    return problems


def rule_problems(name: str, value: str, root: Path) -> list[str]:
    """The roadmap's rule on links and hidden text, read with its own test, on one line."""
    texts = [(name, "docs", 1, [value], value)]
    found = link_problems_in(root, texts) + hidden_text_problems_in(texts)
    return [problem.replace(f"{name}:1 ", f"{name} ", 1) for problem in found]


def further_answer_problems(
    threat: Threat,
    found: Index,
    root: Path,
    items: dict[str, Item],
    statuses: list[tuple[str, dict[str, str]]],
) -> list[str]:
    further = threat.field("Further answer")
    problems, count = citation_problems(threat.ident, further, found, root)
    cited, held = citations(further), citations(threat.field("Held by"))
    new = any(set(getattr(cited, kind)) - set(getattr(held, kind)) for kind in KINDS_OF_CITATION)
    named = plan_items(further)
    if not count and not named:
        problems.append(f"{threat.ident}'s further answer cites nothing")
    elif not new and not named:
        problems.append(f"{threat.ident}'s further answer cites nothing that its Held by does not")
    for ident in named:
        item = items.get(ident)
        if item is None:
            problems.append(f"{threat.ident}'s further answer cites {ident}, not a backlog item")
            continue
        if item.status not in AGREED:
            problems.append(
                f"{threat.ident}'s further answer cites {ident}, which this tree does not give "
                "as Planned or In progress"
            )
        for base, status in statuses:
            if status.get(ident) not in AGREED:
                problems.append(
                    f"{threat.ident}'s further answer cites {ident}, which {base} does not give "
                    "as Planned or In progress"
                )
        done = WHAT_DONE.search(item.text)
        if not done or not re.search(rf"\b{threat.ident}\b", done.group(1)):
            problems.append(
                f"{threat.ident}'s further answer cites {ident}, whose What done looks like does "
                f"not name {threat.ident}"
            )
    return problems


def acceptance_problems(threat: Threat, records: dict[str, Record]) -> list[str]:
    cited = [
        f"DR-{number}" for number in dict.fromkeys(RECORD_REF.findall(threat.field("Acceptance")))
    ]
    if not cited:
        return [f"{threat.ident}'s acceptance cites no record"]
    problems = []
    for ident in cited:
        record = records.get(ident)
        decider = DECIDER.fullmatch(record.fields.get("Decided by", "")) if record else None
        if record is None:
            problems.append(f"{threat.ident}'s acceptance cites {ident}, not a decision record")
        elif record.fields.get("Closed by", "none") != "none":
            problems.append(f"{threat.ident}'s acceptance cites {ident}, which is closed")
        elif not decider or not decider.group("owner"):
            problems.append(
                f"{threat.ident}'s acceptance cites {ident}, whose decider is not the owner"
            )
        elif threat.ident not in record.listed("Threats"):
            problems.append(f"{threat.ident}'s acceptance cites {ident}, which does not list it")
    return problems


def reasons_for(old: Threat, new: Threat) -> list[str]:
    """The fields whose change shows why a rating is lowered (R250): a further answer
    removed, or one that cites a backlog item, is a plan that holds nothing yet (DR-255)."""
    changed = [name for name in REASONS if new.fields.get(name) != old.fields.get(name)]
    further = new.field("Further answer")
    if not further or plan_items(further):
        changed = [name for name in changed if name != "Further answer"]
    return changed


def lowered_problems(before: str, after: str) -> list[str]:
    """R250: a rating that the base gives a high or critical risk is lowered only with a
    change to what the threat says or what answers it."""
    was = {threat.ident: threat for threat in threats_in(before)}
    problems = []
    for threat in threats_in(after):
        old = was.get(threat.ident)
        if old is None:
            continue
        for impact, likelihood in (("Impact", "Likelihood"), ("Raw impact", "Raw likelihood")):
            then = (rating(old.field(impact), IMPACTS), rating(old.field(likelihood), LIKELIHOODS))
            now = (
                rating(threat.field(impact), IMPACTS),
                rating(threat.field(likelihood), LIKELIHOODS),
            )
            if BANDS.get(then[0] * then[1], "") not in FURTHER:
                continue
            lowered = now[0] < then[0] or now[1] < then[1]
            if lowered and not reasons_for(old, threat):
                problems.append(
                    f"{threat.ident}'s {impact.lower()} or {likelihood.lower()} is lowered from "
                    f"a risk of {then[0] * then[1]} with none of {', '.join(REASONS)} changed, "
                    "but for a further answer removed or one that is a plan"
                )
    return problems


def rewritten_problems(
    before: str, after: str, was: dict[str, Item], now: dict[str, Item], base: str
) -> list[str]:
    """R249: compared with a base, a further answer that cites a backlog item is added or
    changed only in a diff that changes that item too, since the item is agreed to what its
    further answers say."""
    old = {threat.ident: threat.field("Further answer") for threat in threats_in(before)}
    problems = []
    for threat in threats_in(after):
        further = threat.field("Further answer")
        if not further or further == old.get(threat.ident, ""):
            continue
        for ident in plan_items(further):
            if ident in was and ident in now and was[ident].text == now[ident].text:
                problems.append(
                    f"{threat.ident}'s further answer changes and cites {ident}, whose text is as "
                    f"{base} holds it"
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


HIGHEST = ("3 (high)", "3 (likely)", "9")


def threat(
    held: str,
    number: int = 1,
    kind: str = "tampering",
    impact: str = "1 (low)",
    likelihood: str = "1 (unlikely)",
    risk: str = "1",
    raw: tuple[str, str, str] | None = None,
    extra: str = "",
) -> str:
    raw_impact, raw_likelihood, raw_risk = raw or (impact, likelihood, risk)
    return (
        f"### T{number}. Something goes wrong\n\n"
        f"- **Kind:** {kind}\n"
        f"- **Impact:** {impact}\n"
        f"- **Likelihood:** {likelihood}\n"
        f"- **Risk:** {risk}\n"
        f"- **Raw impact:** {raw_impact}\n"
        f"- **Raw likelihood:** {raw_likelihood}\n"
        f"- **Raw risk:** {raw_risk}\n"
        "- **What could happen:** a thing.\n"
        "- **Answer:** another thing.\n"
        f"- **Held by:** {held}\n"
        f"{extra}"
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
    text = (
        threat("`docs/note.md`", kind="tampering, mischief", impact="huge", raw=HIGHEST) + matrix()
    )
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
    text = threat(held, impact=impact, likelihood=likelihood, risk=risk, raw=HIGHEST)
    problems, _ = problems_in(text + matrix(""), tmp_path)
    assert [p for p in problems if "risk matrix" not in p] == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (("2 (medium)", "2 (possible)", "4"), []),
        (("2 (medium)", "3 (likely)", "6"), []),
        (("1 (low)", "3 (likely)", "3"), ["T1 has a raw impact lower than its impact"]),
        (("3 (high)", "1 (unlikely)", "3"), ["T1 has a raw likelihood lower than its likelihood"]),
        (("2 (high)", "2 (possible)", "4"), ["T1 has a raw impact outside the list"]),
        (("2", "2 (possible)", "4"), ["T1 has a raw impact outside the list"]),
        (("2 (medium)", "2 (likely)", "4"), ["T1 has a raw likelihood outside the list"]),
        (
            ("2 (medium)", "2 (possible)", "6"),
            ["T1 has a raw risk that is not raw impact times raw likelihood"],
        ),
    ],
)
def test_a_raw_rating_is_a_level_not_below_its_rating_with_the_answer_in_place(
    tmp_path: Path, raw: tuple[str, str, str], expected: list[str]
) -> None:
    synthetic_repository(tmp_path)
    text = threat(
        "`docs/note.md`", impact="2 (medium)", likelihood="2 (possible)", risk="4", raw=raw
    )
    placed = MATRIX.format(low="").replace("| 2 medium | | | |", "| 2 medium | | T1 | |")
    assert problems_in(text + placed, tmp_path)[0] == expected


@pytest.mark.parametrize("name", ["Raw impact", "Raw likelihood", "Raw risk"])
def test_a_threat_without_its_raw_ratings_is_reported(tmp_path: Path, name: str) -> None:
    synthetic_repository(tmp_path)
    text = re.sub(rf"^- \*\*{name}:\*\* .*\n", "", threat("`docs/note.md`"), flags=re.M)
    assert problems_in(text + matrix(), tmp_path)[0] == [f"T1 lacks ['{name}'] or repeats []"]


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


# R249: a further answer or an acceptance for each high or critical risk.


def test_every_high_or_critical_risk_has_a_further_answer_or_an_acceptance() -> None:
    text = THREAT_MODEL.read_text()
    high = [
        threat
        for threat in threats_in(text)
        if threat.field("Further answer") or threat.field("Acceptance")
    ]
    assert high, "no further answer or acceptance was read, so this test covered nothing"
    assert further_problems(text, ROOT, base_commits(ROOT, os.environ)) == []


def test_no_further_answer_is_rewritten_while_its_item_stands() -> None:
    text = THREAT_MODEL.read_text()
    now = {item.ident: item for item in backlog_items(ROOT)}
    problems = []
    for base in base_commits(ROOT, os.environ):
        shown = git(ROOT, "show", f"{base}:docs/threat-model.md")
        if shown.returncode == 0:
            was = {item.ident: item for item in items_in(ROOT, base).values()}
            problems += rewritten_problems(shown.stdout.decode("utf-8"), text, was, now, base)
    assert problems == []


ITEM_PATH = "docs/backlog/B-007-a-thing.md"


def item_text(status: str = "Planned", done: str = "It answers T1 further.") -> str:
    return (
        f"# B-007: A thing\n\n- **Status:** {status}\n\n## Problem\n\nA problem.\n\n"
        f"## What done looks like\n\n{done}\n\n## Postponed points\n\nNone.\n"
    )


def record_text(decider: str = "the owner, 2026-01-01", threats: str = "T1") -> str:
    return (
        f"# DR-002: An acceptance\n\n- **Decided by:** {decider}\n- **Threats:** {threats}\n"
        "- **Closed by:** none\n\n## Decision\n\nThe owner accepts it.\n"
    )


def further_repository(root: Path, status: str = "Planned") -> str:
    """The synthetic repository, with B-007 and an owner's record, committed as the base."""
    synthetic_repository(root)
    (root / "docs" / "backlog").mkdir()
    (root / ITEM_PATH).write_text(item_text(status))
    (root / "docs" / "decisions" / "DR-002-an-acceptance.md").write_text(record_text())
    identity = ("-c", "user.name=Test", "-c", "user.email=test@example.invalid")
    for args in (("init", "-q"), ("add", "-A"), (*identity, "commit", "-qm", "base")):
        assert git(root, *args).returncode == 0
    return git(root, "rev-parse", "HEAD").stdout.decode().strip()


class Ratings(TypedDict, total=False):
    impact: str
    likelihood: str
    risk: str
    raw: tuple[str, str, str]


HIGH: Ratings = {"impact": "3 (high)", "likelihood": "2 (possible)", "risk": "6"}
CRITICAL: Ratings = {"impact": "3 (high)", "likelihood": "3 (likely)", "risk": "9"}
HIGH_RAW: Ratings = {**HIGH, "raw": ("3 (high)", "3 (likely)", "9")}
HIGH_RAW_LOWERED: Ratings = {**HIGH, "raw": ("3 (high)", "2 (possible)", "6")}


def high_threat(extra: str, rated: Ratings = HIGH, held: str = "`docs/note.md`") -> str:
    return threat(held, extra=extra, **rated)


@pytest.mark.parametrize(
    ("extra", "rated"),
    [
        ("- **Further answer:** B-007\n", HIGH),
        ("- **Further answer:** B-007\n", CRITICAL),
        ("- **Further answer:** `demo` task 1.2, which adds a second check\n", HIGH),
        ("- **Acceptance:** DR-002, as the owner chose\n", HIGH),
        ("", Ratings(impact="2 (medium)", likelihood="2 (possible)", risk="4")),
    ],
)
def test_a_high_or_critical_risk_answered_further_or_accepted_passes(
    tmp_path: Path, extra: str, rated: Ratings
) -> None:
    base = further_repository(tmp_path)
    assert further_problems(high_threat(extra, rated), tmp_path, [base]) == []


def test_a_further_answer_whose_item_and_record_are_saved_with_windows_line_endings_passes(
    tmp_path: Path,
) -> None:
    base = further_repository(tmp_path)
    saved_with_windows_line_endings(tmp_path, [ITEM_PATH, "docs/decisions/DR-002-an-acceptance.md"])
    for extra in ("- **Further answer:** B-007\n", "- **Acceptance:** DR-002, as the owner said\n"):
        assert further_problems(high_threat(extra), tmp_path, [base]) == []


@pytest.mark.parametrize(
    ("extra", "rated", "problem"),
    [
        ("", HIGH, "T1 is high and carries neither a further answer nor an acceptance"),
        ("", CRITICAL, "T1 is critical and carries neither a further answer nor an acceptance"),
        ("- **Further answer:** a second check\n", HIGH, "T1's further answer cites nothing"),
        (
            "- **Further answer:** `docs/note.md` again\n",
            HIGH,
            "T1's further answer cites nothing that its Held by does not",
        ),
        (
            "- **Further answer:** `demo` task 9.9\n",
            HIGH,
            "T1 cites `demo` task 9.9, which does not exist",
        ),
        (
            "- **Further answer:** B-008\n",
            HIGH,
            "T1's further answer cites B-008, not a backlog item",
        ),
        ("- **Acceptance:** the owner said so\n", HIGH, "T1's acceptance cites no record"),
        ("- **Acceptance:** DR-009\n", HIGH, "T1's acceptance cites DR-009, not a decision record"),
        ("- **Acceptance:** DR-002\n", CRITICAL, "T1 is critical and carries an acceptance"),
        ("- **Further answer:** B-007 <!-- x -->\n", HIGH, "T1's further answer holds <"),
        ("- **Acceptance:** DR-002 | more\n", HIGH, "T1's acceptance holds |"),
        ("- **Acceptance:** DR-002 \\ more\n", HIGH, "T1's acceptance holds a backslash"),
        (
            '- **Further answer:** B-007, as [the item](note.md "more words") says\n',
            HIGH,
            "T1's further answer holds a link with a title",
        ),
        (
            "- **Acceptance:** DR-002, as https://example.com says\n",
            HIGH,
            "T1's acceptance gives a web address",
        ),
        (
            "- **Further answer:** `demo` task 1.2, which @someone adds\n",
            Ratings(impact="2 (medium)", likelihood="2 (possible)", risk="4"),
            "T1's further answer holds @",
        ),
    ],
)
def test_a_further_answer_or_an_acceptance_that_adds_nothing_is_reported(
    tmp_path: Path, extra: str, rated: Ratings, problem: str
) -> None:
    base = further_repository(tmp_path)
    found = further_problems(high_threat(extra, rated), tmp_path, [base])
    assert [each for each in found if each.startswith(problem)], found


@pytest.mark.parametrize(
    ("status", "done", "problem"),
    [
        ("Open to feedback and contributions", None, "which {base} does not give as Planned"),
        ("Planned", "It answers T10 further.", "whose What done looks like does not name T1"),
    ],
)
def test_a_cited_item_not_agreed_at_the_base_or_not_naming_the_threat_is_reported(
    tmp_path: Path, status: str, done: str | None, problem: str
) -> None:
    base = further_repository(tmp_path, status)
    if done:
        (tmp_path / ITEM_PATH).write_text(item_text(done=done))
    found = further_problems(high_threat("- **Further answer:** B-007\n"), tmp_path, [base])
    assert [each for each in found if problem.format(base=base) in each], found


def test_an_item_done_in_the_tree_is_reported(tmp_path: Path) -> None:
    base = further_repository(tmp_path)
    (tmp_path / ITEM_PATH).write_text(item_text("Done"))
    found = further_problems(high_threat("- **Further answer:** B-007\n"), tmp_path, [base])
    assert found == [
        "T1's further answer cites B-007, which this tree does not give as Planned or In progress"
    ]


def test_an_item_made_planned_in_the_pull_request_itself_is_reported(tmp_path: Path) -> None:
    base = further_repository(tmp_path, "Open to feedback and contributions")
    (tmp_path / ITEM_PATH).write_text(item_text("Planned"))
    found = further_problems(high_threat("- **Further answer:** B-007\n"), tmp_path, [base])
    assert found == [
        f"T1's further answer cites B-007, which {base} does not give as Planned or In progress"
    ]


@pytest.mark.parametrize(
    ("record", "problem"),
    [
        (record_text(threats="T2"), "cites DR-002, which does not list it"),
        (record_text(decider="the change `demo`"), "cites DR-002, whose decider is not the owner"),
        (
            record_text().replace("- **Closed by:** none", "- **Closed by:** DR-003"),
            "cites DR-002, which is closed",
        ),
    ],
)
def test_an_acceptance_that_the_owner_did_not_give_for_the_threat_is_reported(
    tmp_path: Path, record: str, problem: str
) -> None:
    base = further_repository(tmp_path)
    (tmp_path / "docs" / "decisions" / "DR-002-an-acceptance.md").write_text(record)
    found = further_problems(high_threat("- **Acceptance:** DR-002\n"), tmp_path, [base])
    assert found == [f"T1's acceptance {problem}"]


# R250: a high or critical rating is lowered only with what lowers it.


def test_no_high_or_critical_rating_is_lowered_alone() -> None:
    text = THREAT_MODEL.read_text()
    compared = 0
    problems = []
    for base in base_commits(ROOT, os.environ):
        shown = git(ROOT, "show", f"{base}:docs/threat-model.md")
        if shown.returncode == 0:
            compared += 1
            problems += lowered_problems(shown.stdout.decode("utf-8"), text)
    assert problems == []
    if not compared:
        pytest.skip("no base holds the threat model, so there is nothing to compare")


LOWERED: Ratings = {"impact": "3 (high)", "likelihood": "1 (unlikely)", "risk": "3", "raw": HIGHEST}


@pytest.mark.parametrize(
    ("after", "expected"),
    [
        (threat("`docs/note.md`", **LOWERED), ["impact or likelihood is lowered from a risk of 6"]),
        (threat("`docs/note.md`", **LOWERED).replace("another thing.", "a stronger thing."), []),
        (threat("`docs/note.md`; DR-001", **LOWERED), []),
        (
            threat("`docs/note.md`", **LOWERED, extra="- **Further answer:** B-007\n"),
            ["impact or likelihood is lowered from a risk of 6"],
        ),
        (
            threat(
                "`docs/note.md`",
                **LOWERED,
                extra="- **Further answer:** `demo` task 1.2; B-007 writes the rest\n",
            ),
            ["impact or likelihood is lowered from a risk of 6"],
        ),
        (threat("`docs/note.md`", **LOWERED, extra="- **Further answer:** `demo` task 1.2\n"), []),
        (threat("`docs/note.md`", **HIGH_RAW), []),
        (threat("`docs/note.md`", **CRITICAL), []),
        (
            threat("`docs/note.md`", **HIGH_RAW_LOWERED),
            ["raw impact or raw likelihood is lowered from a risk of 9"],
        ),
    ],
)
def test_a_high_rating_lowered_alone_is_reported(after: str, expected: list[str]) -> None:
    before = threat("`docs/note.md`", **HIGH_RAW)
    found = lowered_problems(before, after)
    assert len(found) == len(expected)
    assert all(problem in each for problem, each in zip(expected, found, strict=True))


def test_a_rating_lowered_with_its_further_answer_removed_is_reported() -> None:
    before = threat("`docs/note.md`", **HIGH_RAW, extra="- **Further answer:** `demo` task 1.2\n")
    found = lowered_problems(before, threat("`docs/note.md`", **LOWERED))
    assert len(found) == 1
    assert "T1's impact or likelihood is lowered from a risk of 6" in found[0]


def test_a_rating_below_high_at_the_base_may_be_lowered_alone() -> None:
    before = threat("`docs/note.md`", impact="2 (medium)", likelihood="2 (possible)", risk="4")
    assert lowered_problems(before, threat("`docs/note.md`")) == []


def item(text: str) -> Item:
    return Item(path=ITEM_PATH, number=7, text=text, fields={"Status": "Planned"})


@pytest.mark.parametrize(
    ("before", "after", "changed", "expected"),
    [
        ("", "- **Further answer:** B-007 does it\n", False, ["cites B-007, whose text is as"]),
        (
            "- **Further answer:** B-007 does it\n",
            "- **Further answer:** B-007 does more\n",
            False,
            ["cites B-007, whose text is as"],
        ),
        (
            "- **Further answer:** B-007 does it\n",
            "- **Further answer:** B-007 does it\n",
            False,
            [],
        ),
        ("", "- **Further answer:** B-007 does it\n", True, []),
        ("- **Further answer:** B-007 does it\n", "", False, []),
        ("", "- **Further answer:** `demo` task 1.2\n", False, []),
    ],
)
def test_a_further_answer_rewritten_while_its_item_stands_is_reported(
    before: str, after: str, changed: bool, expected: list[str]
) -> None:
    was = {"B-007": item(item_text())}
    now = {"B-007": item(item_text(done="It answers T1 further, and more."))} if changed else was
    found = rewritten_problems(
        threat("`docs/note.md`", extra=before),
        threat("`docs/note.md`", extra=after),
        was,
        now,
        "abc",
    )
    assert len(found) == len(expected)
    assert all(problem in each for problem, each in zip(expected, found, strict=True))


# R134: no attribute hides the threat model's diff.


def test_no_attribute_changes_how_the_threat_model_s_diff_shows() -> None:
    assert attribute_problems(ROOT, ["docs/threat-model.md"]) == []


@pytest.mark.parametrize(
    ("attribute", "shown"),
    [
        ("binary", "binary: set"),
        ("-diff", "diff: unset"),
        ("diff=word", "diff: word"),
        ("linguist-generated", "linguist-generated: set"),
    ],
)
def test_an_attribute_that_hides_the_threat_model_s_diff_is_reported(
    tmp_path: Path, attribute: str, shown: str
) -> None:
    assert git(tmp_path, "init", "-q").returncode == 0
    (tmp_path / ".gitattributes").write_text(f"docs/*.md {attribute}\n")
    found = attribute_problems(tmp_path, ["docs/threat-model.md"])
    assert f"docs/threat-model.md has {shown}, which changes how its diff shows" in found
