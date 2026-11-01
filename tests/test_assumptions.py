"""The assumptions say what rests on them, and how each of their facts is checked.

`docs/assumptions/` holds what the specs, the design, the threat model and the
records assume about Claude Code, GitHub, git, Python, the development tools,
prices, adopters and people (R135, R136, R140; design decision 14). Its index,
`README.md`, lists every assumption on one line, and a page per subject holds
each in full: what rests on it, by requirement, threat and record ID, what
changes if it is wrong, and its facts, each with where it is relied on and how it
is checked.

Each line of an assumption is one of its fields, and each line under a fact is
one of the fact's. A line that is not would show on GitHub as part of the field
above it, while no check here would read it.

A citation must resolve: a requirement in the register, a threat in the threat
model, a record in `docs/decisions/`, a task or a decision of a change, a
scenario in `openspec/specs/` or an active change, a file in this repository, or
a test that pytest collects. A threat that rests on an assumption names it in its
field `Assumptions`, and the assumption names the threat. Each ID that a fact is
relied on by rests on the fact's assumption, so the assumption names it too, and
its place in the list counts it.

A check is `tested`, `observed`, `documented` or `not yet`. No test may reach
Claude Code, GitHub, a vendor's prices, or adopters and people (DR-090), so a
fact on their pages, or in the section "Prices", is never `tested`. An
observation names a file under `tests/` that reproduces what was seen, the date,
and the program, the version that it prints and its build. Documentation is
linked by its address, on a host that `HOSTS` lists or as a GitHub file at a full
commit, with the date it was read; `HOSTS` changes only in a pull request that
the owner reviews (T95). Each setting in the threat model's section "Settings the
owner keeps" is a fact that cites the threat model and is `not yet`, since no
test may read a setting on GitHub.

The index lists the assumptions by the highest impact among the threats that
rest on them, then least checked first, an assumption being as checked as its
least checked fact, then by the highest risk among those threats, with the
assumptions that no threat rests on last, and each page keeps the index's order.
Each line of the index gives the impact and the risk that the threat model's
ratings give.

No page, and no file that an observation names, may hold a path under a home
folder or a session identifier. A problem names the file and the line, and quotes
neither. `~/` names no one's folder, so it is not such a path.
"""

from __future__ import annotations

import functools
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from itertools import pairwise
from pathlib import Path
from urllib.parse import urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = Path("docs") / "assumptions"
INDEX_PAGE = "README.md"

# Each subject page, its sections, and for each section the subject that no test
# may reach, or None where a test may. A page without sections has the one section "".
PAGES: dict[str, dict[str, str | None]] = {
    "claude-code.md": {"": "Claude Code"},
    "github.md": {"": "GitHub"},
    "git.md": {"": None},
    "python-tools-and-prices.md": {
        "Python": None,
        "The development tools": None,
        "Prices": "prices",
    },
    "adopters-and-people.md": {"": "adopters and people"},
}
# The vendors' documentation hosts that a documented fact may link (T95).
HOSTS = frozenset({"code.claude.com", "docs.github.com"})
GITHUB_HOST = "github.com"
# Least checked first.
LEVELS = {"not yet": 0, "documented": 1, "observed": 2, "tested": 3}
LIST_HEADING = "The assumptions, most at stake first"
RATING_NOTE = "rated with the assumption true"
SETTINGS_HEADING = "Settings the owner keeps"
THREAT_MODEL_PATH = "docs/threat-model.md"

ASSUMPTION_FIELDS = ("Rests on it", "If it is wrong")
FACT_FIELDS = ("Relied on", "Checked", "Handled by")

HEADING = re.compile(r"^#{2,3} (A([1-9]\d*))\. (.+?)\s*$")
SECTION = re.compile(r"^## (.+?)\s*$")
ANY_HEADING = re.compile(r"^#{1,6} ")
FIELD = re.compile(r"^- \*\*([^*]+):\*\* ?(.*?)\s*$")
SUBFIELD = re.compile(r"^  - \*\*([^*]+):\*\* ?(.*?)\s*$")
INDEX_ENTRY = re.compile(r"^- \*\*(A[1-9]\d*)\.\*\* (.*?)\s*$")
INDEX_LINE = re.compile(
    r"(.+?) (?:Impact ([1-3]), risk ([1-9])|No threat)\. Page: \[[^\]]+\]\(([a-z0-9-]+\.md)\)\."
)
PAGE_LINK = re.compile(r" Page: \[[^\]]+\]\(([a-z0-9-]+\.md)\)\.$")
RETIRED = re.compile(r"^- A([1-9]\d*), removed by `[a-z0-9-]+`$", re.M)
RETIRED_SECTION = re.compile(r"^## Retired IDs\n(.*?)(?=^## |\Z)", re.M | re.S)
THREAT_BLOCK = re.compile(r"^### (T\d+)\. .*?(?=^#{1,3} |\Z)", re.M | re.S)
THREAT_RATING = re.compile(r"([1-3]) \(")
ASSUMPTION_ID = re.compile(r"\bA[1-9]\d*\b")
SETTINGS_SECTION = re.compile(rf"^## {SETTINGS_HEADING}\n(.*?)(?=^## |\Z)", re.M | re.S)
SETTING = re.compile(r"^- \*\*(.+?)\*\*", re.M)
REGISTER_ROW = re.compile(r"^\| (R\d+) \|", re.M)
RECORD_FILE = re.compile(r"(DR-\d{3,})-[a-z0-9-]+\.md")
ARCHIVE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
TASK_LINE = re.compile(r"^- \[[ x]\] (\d+\.\d+) ", re.M)
DESIGN_HEADING = re.compile(r"^### (\d+)\. ", re.M)
SCENARIO = re.compile(r"^#### Scenario: (.+?)\s*$", re.M)

SCENARIO_REF = re.compile(r'`([a-z0-9-]+)`: "([^"]+)"')
TASK_REF = re.compile(r"`([a-z0-9-]+)` task (\d+\.\d+)")
DECISION_REF = re.compile(r"`([a-z0-9-]+)` decision (\d+)")
PATH_REF = re.compile(r"`([^`\s]+)`")
ID_REF = re.compile(r"\b(?:DR-\d{3,}|R\d+|T\d+)\b")
SEPARATORS = re.compile(r"[\s,]+")

NODE = re.compile(r"`([^`]+)`")
NODES = re.compile(r"`[^`]+`(?:, `[^`]+`)*")
OBSERVED = re.compile(
    r"observed: `(tests/[^`]+)`, (\d{4}-\d{2}-\d{2}), ([^,`]+), version `([^`]+)`,"
    r" build `([^`]+)`"
)
LINK_FORM = r"(?:<[^<>\s]+>|\[[^\]]*\]\([^()\s]+\))"
DOCUMENTED = re.compile(
    rf"documented: ({LINK_FORM}(?:, {LINK_FORM})*), read (\d{{4}}-\d{{2}}-\d{{2}})"
)
LINK = re.compile(r"<([^<>\s]+)>|\[([^\]]*)\]\(([^()\s]+)\)")
GITHUB_FILE = re.compile(r"/[^/]+/[^/]+/blob/[0-9a-f]{40}/[^/].*")
NONE_WILL = re.compile(r"\bnone will, since \S")

# Built from parts, so that this file does not match what it looks for.
HOME_PATH = re.compile(
    r"(?<![\w.~])(?:/" + "home/|/" + "Users/|/" + r"root/)|\b[A-Za-z]:\\" + r"Users\\"
)
SESSION_ID = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
    r"|\bsession" + r"_[0-9A-Za-z]{8,}"
)


@dataclass
class Fact:
    statement: str
    fields: dict[str, list[str]] = field(default_factory=dict)

    def one(self, name: str) -> str:
        values = self.fields.get(name, [])
        return values[0] if values else ""


@dataclass
class Assumption:
    ident: str
    number: int
    statement: str
    page: str
    section: str
    fields: dict[str, list[str]] = field(default_factory=dict)
    facts: list[Fact] = field(default_factory=list)
    stray: int = 0
    unknown: list[str] = field(default_factory=list)

    def one(self, name: str) -> str:
        values = self.fields.get(name, [])
        return values[0] if values else ""

    def read(self, line: str) -> None:
        """Read one line of the assumption's entry as one of its fields or its facts'."""
        if not line.strip():
            return
        if top := FIELD.match(line):
            name, value = top.groups()
            if name == "Fact":
                self.facts.append(Fact(value))
            elif name in ASSUMPTION_FIELDS:
                self.fields.setdefault(name, []).append(value)
            else:
                self.unknown.append(name)
        elif (sub := SUBFIELD.match(line)) and self.facts:
            name, value = sub.groups()
            if name in FACT_FIELDS:
                self.facts[-1].fields.setdefault(name, []).append(value)
            else:
                self.unknown.append(name)
        else:
            self.stray += 1


@dataclass(frozen=True)
class Listed:
    """An assumption's line on the index; its statement is None where the line is malformed."""

    ident: str
    statement: str | None = None
    rating: tuple[int, int] | None = None
    page: str | None = None


@dataclass(frozen=True)
class Threat:
    impact: int
    risk: int
    assumptions: frozenset[str]


@dataclass(frozen=True)
class Known:
    """What the repository holds for a citation to resolve to."""

    root: Path
    requirements: frozenset[str]
    threats: dict[str, Threat]
    records: frozenset[str]
    tasks: dict[str, frozenset[str]]
    decisions: dict[str, frozenset[str]]
    scenarios: dict[str, frozenset[str]]
    settings: tuple[str, ...]
    collected: frozenset[str]


@dataclass
class Checked:
    """What the checks of one assumption found."""

    problems: list[str] = field(default_factory=list)
    rests: list[str] = field(default_factory=list)
    forms: list[str | None] = field(default_factory=list)
    observed: list[Path] = field(default_factory=list)

    @property
    def level(self) -> int:
        return min((LEVELS.get(form or "", 0) for form in self.forms), default=0)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def assumptions_in(page: str, text: str) -> list[Assumption]:
    found: list[Assumption] = []
    current: Assumption | None = None
    section = ""
    for line in text.splitlines():
        if heading := HEADING.match(line):
            ident, number, statement = heading.groups()
            current = Assumption(ident, int(number), statement, page, section)
            found.append(current)
        elif ANY_HEADING.match(line):
            current = None
            if named := SECTION.match(line):
                section = named.group(1)
            elif line.startswith("# "):
                section = ""
        elif current is not None:
            current.read(line)
    return found


def threats_in(text: str) -> dict[str, Threat]:
    threats = {}
    for block in THREAT_BLOCK.finditer(text):
        fields: dict[str, str] = {}
        for line in block.group(0).splitlines():
            if found := FIELD.match(line):
                fields.setdefault(found.group(1), found.group(2))
        impact = THREAT_RATING.match(fields.get("Impact", ""))
        risk = fields.get("Risk", "")
        threats[block.group(1)] = Threat(
            int(impact.group(1)) if impact else 0,
            int(risk) if risk.isdigit() else 0,
            frozenset(ASSUMPTION_ID.findall(fields.get("Assumptions", ""))),
        )
    return threats


def change_folders(root: Path) -> dict[str, Path]:
    base = root / "openspec" / "changes"
    folders = {}
    for folder in sorted(base.glob("*")) + sorted((base / "archive").glob("*")):
        if folder.is_dir() and folder.name != "archive":
            folders[ARCHIVE_DATE.sub("", folder.name)] = folder
    return folders


def known_in(root: Path, collected: frozenset[str]) -> Known:
    model = read(root / THREAT_MODEL_PATH)
    settings = SETTINGS_SECTION.search(model)
    changes = change_folders(root)
    # A scenario resolves only where the specs hold it now, never in an archived copy.
    specs = [
        *(root / "openspec" / "specs").glob("*/spec.md"),
        *(root / "openspec" / "changes").glob("*/specs/*/spec.md"),
    ]
    scenarios: dict[str, set[str]] = {}
    for spec in specs:
        scenarios.setdefault(spec.parent.name, set()).update(SCENARIO.findall(read(spec)))
    return Known(
        root=root,
        requirements=frozenset(REGISTER_ROW.findall(read(root / "docs" / "requirements.md"))),
        threats=threats_in(model),
        records=frozenset(
            found.group(1)
            for path in (root / "docs" / "decisions").glob("DR-*.md")
            if (found := RECORD_FILE.fullmatch(path.name))
        ),
        tasks={
            name: frozenset(TASK_LINE.findall(read(folder / "tasks.md")))
            for name, folder in changes.items()
        },
        decisions={
            name: frozenset(DESIGN_HEADING.findall(read(folder / "design.md")))
            for name, folder in changes.items()
        },
        scenarios={name: frozenset(names) for name, names in scenarios.items()},
        settings=tuple(SETTING.findall(settings.group(1))) if settings else (),
        collected=collected,
    )


def id_problems(ident: str, ids: list[str], known: Known) -> list[str]:
    problems = []
    for each in dict.fromkeys(ids):
        if each.startswith("DR-"):
            if each not in known.records:
                problems.append(f"{ident} names {each}, which is not a decision record")
        elif each.startswith("R"):
            if each not in known.requirements:
                problems.append(f"{ident} names {each}, which is not a requirement in the register")
        elif each not in known.threats:
            problems.append(f"{ident} names {each}, which is not a threat")
    return problems


def task_problems(ident: str, text: str, known: Known) -> list[str]:
    return [
        f"{ident} names `{change}` task {number}, which does not exist"
        for change, number in TASK_REF.findall(text)
        if number not in known.tasks.get(change, frozenset())
    ]


def citations(ident: str, text: str, known: Known) -> tuple[list[str], list[str], str]:
    """The problems of what `text` cites, the IDs it cites, and the text left uncited."""
    problems = []
    for capability, name in SCENARIO_REF.findall(text):
        if name not in known.scenarios.get(capability, frozenset()):
            problems.append(f'{ident} names `{capability}`: "{name}", which no spec holds')
    rest = SCENARIO_REF.sub(" ", text)
    problems += task_problems(ident, rest, known)
    rest = TASK_REF.sub(" ", rest)
    for change, number in DECISION_REF.findall(rest):
        if number not in known.decisions.get(change, frozenset()):
            problems.append(f"{ident} names `{change}` decision {number}, which does not exist")
    rest = DECISION_REF.sub(" ", rest)
    for path in PATH_REF.findall(rest):
        target = (known.root / path).resolve()
        if known.root.resolve() not in target.parents or not target.exists():
            problems.append(f"{ident} names `{path}`, which is not a file in this repository")
    rest = PATH_REF.sub(" ", rest)
    ids = ID_REF.findall(rest)
    problems += id_problems(ident, ids, known)
    return problems, ids, SEPARATORS.sub("", ID_REF.sub(" ", rest))


def node_problems(ident: str, nodes: list[str], collected: frozenset[str]) -> list[str]:
    return [
        f"{ident} names {node}, which is not a collected test"
        for node in nodes
        if node not in collected and not any(each.startswith(f"{node}[") for each in collected)
    ]


def named_test_problems(ident: str, name: str, what: str, text: str, known: Known) -> list[str]:
    if not NODES.fullmatch(text):
        return [f"{name} names {what} with text that is not a test's name"]
    return node_problems(ident, NODE.findall(text), known.collected)


def date_problems(name: str, day: str) -> list[str]:
    try:
        date.fromisoformat(day)
    except ValueError:
        return [f"{name} gives a date that is not a day of the calendar: {day}"]
    return []


def link_problems(name: str, links: str) -> list[str]:
    problems = []
    for link in LINK.finditer(links):
        autolink, text, target = link.groups()
        address = autolink if autolink is not None else target
        if autolink is None and text != target:
            problems.append(f"{name} shows link text other than its address")
        parts = urlsplit(address)
        if parts.scheme != "https":
            problems.append(f"{name} links an address that is not https")
        elif parts.hostname == GITHUB_HOST:
            if not GITHUB_FILE.fullmatch(parts.path):
                problems.append(
                    f"{name} links a GitHub address that is not a file at a full commit"
                )
        elif parts.hostname not in HOSTS:
            problems.append(
                f"{name} links {parts.hostname}, which is not a documentation host that this"
                " test lists"
            )
    return problems


def check_problems(
    assumption: Assumption, name: str, checked: str, subject: str | None, known: Known
) -> tuple[str | None, list[str], Path | None]:
    """The form of a fact's check, its problems, and the file that an observation names."""
    form = next((each for each in LEVELS if checked.startswith(f"{each}: ")), None)
    ident = assumption.ident
    if form is None:
        return None, [f"{name} does not say how it is checked"], None
    rest = checked[len(form) + 2 :]
    if form == "tested":
        problems = named_test_problems(ident, name, "what checks it", rest, known)
        if subject:
            problems.append(
                f"{name} is about {subject}, which no test may reach, and is checked by a test"
                " alone"
            )
        return form, problems, None
    if form == "observed":
        observed = OBSERVED.fullmatch(checked)
        if not observed:
            return (
                form,
                [
                    f"{name} gives an observation without its file, its date, or its program,"
                    " version and build"
                ],
                None,
            )
        path, day = observed.group(1), observed.group(2)
        file = known.root / path
        tests = (known.root / "tests").resolve()
        problems = date_problems(name, day)
        if tests not in file.resolve().parents or not file.is_file():
            return form, [*problems, f"{name} names {path}, which is not a file under tests/"], None
        return form, problems, file
    if form == "documented":
        documented = DOCUMENTED.fullmatch(checked)
        if not documented:
            return (
                form,
                [f"{name} gives a documented check without its links or the date they were read"],
                None,
            )
        links, day = documented.groups()
        return form, [*link_problems(name, links), *date_problems(name, day)], None
    problems = task_problems(ident, rest, known)
    if not TASK_REF.search(rest) and not NONE_WILL.search(rest):
        problems.append(
            f"{name} is not yet checked and names neither the task that will check it nor why"
            " none will"
        )
    return form, problems, None


def fact_problems(
    assumption: Assumption, number: int, fact: Fact, known: Known, found: Checked
) -> None:
    ident = assumption.ident
    name = f"{ident}, fact {number},"
    problems = found.problems
    problems += [
        f"{name} gives {each} more than once"
        for each, values in fact.fields.items()
        if len(values) > 1
    ]
    if not fact.statement:
        problems.append(f"{name} states nothing")
    relied = fact.one("Relied on")
    if not relied:
        problems.append(f"{name} does not say where it is relied on")
    else:
        cited, ids, rest = citations(ident, relied, known)
        problems += cited
        if rest:
            problems.append(f"{name} says where it is relied on with text that is not a citation")
        problems += [
            f"{name} is relied on by {each}, which {ident} does not name as resting on it"
            for each in dict.fromkeys(ids)
            if each not in found.rests
        ]
    if "Handled by" in fact.fields:
        problems += named_test_problems(
            ident, name, "what handles it", fact.one("Handled by"), known
        )
    subject = PAGES[assumption.page].get(assumption.section)
    form, checked, observed = check_problems(assumption, name, fact.one("Checked"), subject, known)
    problems += checked
    found.forms.append(form)
    if observed:
        found.observed.append(observed)


def assumption_problems(assumption: Assumption, known: Known) -> Checked:
    ident = assumption.ident
    found = Checked()
    problems = found.problems
    problems += [
        f"{ident} has a field that the assumptions do not have: {name}"
        for name in dict.fromkeys(assumption.unknown)
    ]
    if assumption.stray:
        problems.append(f"{ident} has a line that is not a field, which no check reads")
    problems += [
        f"{ident} gives {name} more than once"
        for name, values in assumption.fields.items()
        if len(values) > 1
    ]
    if assumption.section not in PAGES[assumption.page]:
        problems.append(f"{ident} stands outside the sections of {assumption.page}")
    rests = assumption.one("Rests on it")
    found.rests = ID_REF.findall(rests)
    if not found.rests:
        problems.append(f"{ident} names nothing that rests on it")
    elif SEPARATORS.sub("", ID_REF.sub(" ", rests)):
        problems.append(f"{ident} names what rests on it with text that is not an ID")
    problems += id_problems(ident, found.rests, known)
    if not assumption.one("If it is wrong"):
        problems.append(f"{ident} does not say what changes if it is wrong")
    if not assumption.facts:
        problems.append(f"{ident} lists no fact")
    for number, fact in enumerate(assumption.facts, start=1):
        fact_problems(assumption, number, fact, known, found)
    return found


def index_in(text: str) -> tuple[list[Listed], list[str], set[int]]:
    """The index's lines, the problems of their form, and the retired numbers."""
    section = RETIRED_SECTION.search(text)
    retired = {int(number) for number in RETIRED.findall(section.group(1) if section else "")}
    heading = re.search(rf"^## {re.escape(LIST_HEADING)}\s*$", text, re.M)
    if not heading:
        return [], [f'the index has no section "{LIST_HEADING}"'], retired
    problems = []
    if RATING_NOTE not in text[: heading.start()]:
        problems.append(
            "the index does not say above its list that a risk is rated with the assumption true"
        )
    body = text[heading.end() :]
    if following := re.search(r"^## ", body, re.M):
        body = body[: following.start()]
    listed = []
    for line in body.splitlines():
        if not line.strip():
            continue
        entry = INDEX_ENTRY.match(line)
        if not entry:
            problems.append(
                "the index's list has a line that names no assumption, which no check reads"
            )
            continue
        ident, rest = entry.groups()
        if whole := INDEX_LINE.fullmatch(rest):
            statement, impact, risk, page = whole.groups()
            rating = (int(impact), int(risk)) if impact else None
            listed.append(Listed(ident, statement, rating, page))
            continue
        listed.append(Listed(ident))
        if PAGE_LINK.search(rest):
            problems.append(f"{ident}'s line on the index does not give its impact and its risk")
        else:
            problems.append(f"{ident}'s line on the index does not end with a link to its page")
    return listed, problems, retired


def rating(rests: list[str], known: Known) -> tuple[int, int] | None:
    threats = [known.threats[each] for each in rests if each in known.threats]
    if not threats:
        return None
    return max(threat.impact for threat in threats), max(threat.risk for threat in threats)


def stake(found: Checked, known: Known) -> tuple[int, int, int, int]:
    """The key that orders the assumptions, the most at stake first."""
    rated = rating(found.rests, known)
    if rated is None:
        return (1, 0, found.level, 0)
    impact, risk = rated
    return (0, -impact, found.level, -risk)


def numbering_problems(numbers: list[int], listed: set[int], retired: set[int]) -> list[str]:
    counts = Counter(numbers)
    problems = [
        f"A{number} is used more than once" for number in sorted(counts) if counts[number] > 1
    ]
    problems += [
        f"A{number} is retired and still in use"
        for number in sorted(retired & (set(counts) | listed))
    ]
    last = max([*counts, *retired], default=0)
    missing = [n for n in range(1, last + 1) if n not in counts and n not in retired]
    if missing:
        problems.append(
            f"the assumptions are not numbered from A1 to A{last} without a gap, apart from"
            " retired IDs; missing: " + ", ".join(f"A{n}" for n in missing)
        )
    return problems


def naming_problems(found: dict[str, Checked], known: Known) -> list[str]:
    problems = []
    for ident, checked in found.items():
        for each in dict.fromkeys(checked.rests):
            threat = known.threats.get(each)
            if threat is not None and ident not in threat.assumptions:
                problems.append(f"{ident} names {each}, which does not name {ident}")
    for each, threat in known.threats.items():
        for ident in sorted(threat.assumptions, key=lambda name: int(name[1:])):
            if ident not in found:
                problems.append(f"{each} names {ident}, which is not an assumption")
            elif each not in found[ident].rests:
                problems.append(f"{each} names {ident}, which does not name {each}")
    return problems


def listing_problems(
    listed: list[Listed], held: dict[str, Assumption], found: dict[str, Checked], known: Known
) -> list[str]:
    counts = Counter(entry.ident for entry in listed)
    problems = [f"{ident} is on the index more than once" for ident in counts if counts[ident] > 1]
    first: dict[str, Listed] = {}
    for entry in listed:
        first.setdefault(entry.ident, entry)
    for ident, entry in first.items():
        assumption = held.get(ident)
        if assumption is None:
            problems.append(f"{ident} is on the index and on no page")
            continue
        if entry.statement is None:
            continue
        if entry.page != assumption.page:
            problems.append(
                f"the index puts {ident} on {entry.page}, but it is on {assumption.page}"
            )
        if entry.statement != assumption.statement:
            problems.append(f"{ident}'s statement on the index differs from its page's")
        computed = rating(found[ident].rests, known)
        if entry.rating == computed:
            continue
        given = (
            f"impact {entry.rating[0]} and risk {entry.rating[1]}" if entry.rating else "no threat"
        )
        where = (
            f"its threats give impact {computed[0]} and risk {computed[1]}"
            if computed
            else "no threat rests on it"
        )
        problems.append(f"the index gives {ident} {given}, where {where}")
    problems += [
        f"{ident} is on {assumption.page} and not on the index"
        for ident, assumption in held.items()
        if ident not in first
    ]
    return problems


def order_problems(
    assumptions: list[Assumption], listed: list[Listed], found: dict[str, Checked], known: Known
) -> list[str]:
    position: dict[str, int] = {}
    for entry in listed:
        position.setdefault(entry.ident, len(position))
    ranked = sorted((ident for ident in position if ident in found), key=position.__getitem__)
    problems = [
        f"{after} stands after {before} on the index, though it has more at stake"
        for before, after in pairwise(ranked)
        if stake(found[after], known) < stake(found[before], known)
    ]
    sections: dict[tuple[str, str], list[str]] = {}
    for assumption in assumptions:
        if assumption.ident in position:
            sections.setdefault((assumption.page, assumption.section), []).append(assumption.ident)
    for (page, _), idents in sections.items():
        problems += [
            f"{before} stands before {after} on {page}, unlike the index"
            for before, after in pairwise(idents)
            if position[after] < position[before]
        ]
    return problems


def setting_problems(
    assumptions: list[Assumption], found: list[Checked], known: Known
) -> list[str]:
    problems = []
    for setting in known.settings:
        facts = [
            form
            for assumption, checked in zip(assumptions, found, strict=True)
            for fact, form in zip(assumption.facts, checked.forms, strict=True)
            if f"**{setting}**" in fact.statement
            and f"`{THREAT_MODEL_PATH}`" in fact.one("Relied on")
        ]
        if not facts:
            problems.append(
                f'the threat model\'s setting "{setting}" is in no fact that cites'
                f" `{THREAT_MODEL_PATH}`"
            )
        problems += [
            f'the threat model\'s setting "{setting}" is checked as {form}, though no test may'
            " read a setting on GitHub"
            for form in facts
            if form is not None and form != "not yet"
        ]
    return problems


def private_problems(root: Path, files: list[Path]) -> list[str]:
    """Where a page or an observation's file holds a private source, quoting neither."""
    problems = []
    for file in dict.fromkeys(files):
        where = file.relative_to(root).as_posix()
        for number, line in enumerate(read(file).splitlines(), start=1):
            if HOME_PATH.search(line):
                problems.append(f"{where}:{number} holds a path under a home folder")
            if SESSION_ID.search(line):
                problems.append(f"{where}:{number} holds a session identifier")
    return problems


def problems(root: Path, collected: frozenset[str]) -> tuple[list[str], int]:
    """Every problem of the assumptions under `root`, and how many facts were read."""
    folder = root / FOLDER
    pages = sorted(folder.glob("*.md")) if folder.is_dir() else []
    found: list[str] = []
    assumptions: list[Assumption] = []
    for page in pages:
        if page.name == INDEX_PAGE:
            continue
        if page.name not in PAGES:
            found.append(f"{page.name} is not a subject page that this test knows")
            continue
        held = assumptions_in(page.name, read(page))
        if not held:
            found.append(f"{page.name} holds no assumption")
        assumptions += held
    if not assumptions:
        return ["no assumption found"], 0
    known = known_in(root, collected)
    checked = [assumption_problems(assumption, known) for assumption in assumptions]
    for each in checked:
        found += each.problems
    held_by_id: dict[str, Assumption] = {}
    found_by_id: dict[str, Checked] = {}
    for assumption, each in zip(assumptions, checked, strict=True):
        held_by_id.setdefault(assumption.ident, assumption)
        found_by_id.setdefault(assumption.ident, each)
    listed, index_found, retired = index_in(read(folder / INDEX_PAGE))
    found += index_found
    found += numbering_problems(
        [assumption.number for assumption in assumptions],
        {int(entry.ident[1:]) for entry in listed},
        retired,
    )
    found += naming_problems(found_by_id, known)
    found += listing_problems(listed, held_by_id, found_by_id, known)
    found += order_problems(assumptions, listed, found_by_id, known)
    found += setting_problems(assumptions, checked, known)
    found += private_problems(root, [*pages, *(file for each in checked for file in each.observed)])
    return found, sum(len(assumption.facts) for assumption in assumptions)


@functools.cache
def collected_tests(root: Path) -> frozenset[str]:
    """The node IDs that pytest collects under `tests/`, listed without running a test."""
    listing = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "-o",
            "addopts=",
            "-p",
            "no:cacheprovider",
            "tests",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return frozenset(line for line in listing.stdout.splitlines() if "::" in line)


EXAMPLE_TEST = "tests/test_example.py::test_example"
COLLECTED = frozenset({EXAMPLE_TEST})

# Built from parts, so that this file does not match the patterns it plants.
HOME = "/ho" + "me/someone/work"
MAC_HOME = "/Us" + "ers/someone/work"
ROOT_HOME = "/ro" + "ot/work"
WINDOWS_HOME = "C:" + "\\Us" + "ers\\someone\\work"
SESSION = "0123abcd-" + "4567-89ab-cdef-0123456789ab"
SESSION_NAME = "sess" + "ion_0123456789abcdef"

REGISTER = """\
| ID | Kind | Spec | Requirement |
|---|---|---|---|
| R1 | functional | `thing` | One |
| R2 | functional | `thing` | Two |
"""

THREAT_MODEL = """\
# Threat model

### T1. One

- **Impact:** 3 (high)
- **Likelihood:** 1 (unlikely)
- **Risk:** 3
- **Assumptions:** A1

### T2. Two

- **Impact:** 2 (medium)
- **Likelihood:** 3 (likely)
- **Risk:** 6
- **Assumptions:** A2

### T3. Three

- **Impact:** 1 (low)
- **Likelihood:** 1 (unlikely)
- **Risk:** 1
- **Assumptions:** A3

## Settings the owner keeps

- **Approval for runs**, set to the strictest choice (T1).

## Retired IDs

None yet.
"""

INDEX = """\
# Assumptions

A risk below is rated with the assumption true, since the threat model rates each \
threat with its answer in place (DR-001).

## The assumptions, most at stake first

- **A1.** GitHub enforces what a workflow declares. Impact 3, risk 3. Page: [GitHub](github.md).
- **A2.** git stays offline when told to. Impact 2, risk 6. Page: [git](git.md).
- **A3.** git keeps its word. Impact 1, risk 1. Page: [git](git.md).
- **A4.** Prices change rarely. No threat. Page: [Python, the development tools and \
prices](python-tools-and-prices.md).

## Retired IDs

None yet.
"""

GITHUB = """\
# GitHub

No test may reach GitHub.

## A1. GitHub enforces what a workflow declares.

- **Rests on it:** R1, T1, DR-001
- **If it is wrong:** a workflow could do more than it declares.
- **Fact:** GitHub enforces the permissions that a workflow declares.
  - **Relied on:** T1, `a-change` task 1.1
  - **Checked:** documented: <https://docs.github.com/en/actions>, read 2026-11-01
  - **Handled by:** `tests/test_example.py::test_example`
- **Fact:** **Approval for runs** is as the threat model's settings list it.
  - **Relied on:** T1, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may read a setting on GitHub
"""

GIT = """\
# git

## A2. git stays offline when told to.

- **Rests on it:** R2, T2
- **If it is wrong:** capture could fetch from a remote.
- **Fact:** git reads `GIT_NO_LAZY_FETCH`.
  - **Relied on:** R2, `thing`: "It works"
  - **Checked:** observed: `tests/test_example.py`, 2026-11-01, git, version `git version \
2.43.0`, build `1:2.43.0-1ubuntu7.3`
- **Fact:** git's source reads it at a commit.
  - **Relied on:** T2, `a-change` decision 1
  - **Checked:** documented: \
<https://github.com/git/git/blob/1f2e64e22dee75db96b92d526d14003ba59a154e/promisor-remote.c>, \
read 2026-11-01

## A3. git keeps its word.

- **Rests on it:** T3
- **If it is wrong:** a check could pass on a git that behaves otherwise.
- **Fact:** git does what its own tests say.
  - **Relied on:** T3
  - **Checked:** tested: `tests/test_example.py::test_example`
"""

PRICES = """\
# Python, the development tools and prices

## Prices

### A4. Prices change rarely.

- **Rests on it:** DR-001
- **If it is wrong:** the price table would fall behind.
- **Fact:** A model's price changes rarely.
  - **Relied on:** DR-001
  - **Checked:** not yet: `a-change` task 1.1 checks it
"""


def synthetic_repository(root: Path) -> Path:
    files = {
        "docs/requirements.md": REGISTER,
        "docs/threat-model.md": THREAT_MODEL,
        "docs/decisions/DR-001-a-record.md": "# DR-001: A record\n",
        "openspec/changes/a-change/tasks.md": "## 1. Group\n\n- [ ] 1.1 Do it\n",
        "openspec/changes/a-change/design.md": "## Decisions\n\n### 1. A decision\n",
        "openspec/specs/thing/spec.md": "### Requirement: One\n\n#### Scenario: It works\n",
        "tests/test_example.py": "def test_example() -> None:\n    pass\n",
        "docs/assumptions/README.md": INDEX,
        "docs/assumptions/github.md": GITHUB,
        "docs/assumptions/git.md": GIT,
        "docs/assumptions/python-tools-and-prices.md": PRICES,
    }
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text)
    return root


def plant(root: Path, path: str, old: str, new: str) -> None:
    file = root / path
    text = file.read_text()
    assert text.count(old) == 1, f"{old!r} is not in {path} exactly once"
    file.write_text(text.replace(old, new))


def found(root: Path, collected: frozenset[str] = COLLECTED) -> list[str]:
    return problems(root, collected)[0]


def test_complete_assumptions_have_no_problem(tmp_path: Path) -> None:
    root = synthetic_repository(tmp_path)
    found_problems, facts = problems(root, COLLECTED)
    assert found_problems == []
    assert facts == 6


def test_a_folder_without_assumptions_is_reported(tmp_path: Path) -> None:
    root = synthetic_repository(tmp_path)
    for page in (root / "docs" / "assumptions").glob("*.md"):
        page.unlink()
    assert "no assumption found" in found(root)


# Each case plants one defect in the complete assumptions, and names a problem
# that the checks must report.
CASES = [
    # An assumption without its check fails CI.
    (
        "no-rests-on",
        "docs/assumptions/git.md",
        "- **Rests on it:** T3\n",
        "",
        "A3 names nothing that rests on it",
    ),
    (
        "prose-rests-on",
        "docs/assumptions/git.md",
        "- **Rests on it:** T3\n",
        "- **Rests on it:** the tests\n",
        "A3 names nothing that rests on it",
    ),
    (
        "rests-on-with-prose",
        "docs/assumptions/git.md",
        "- **Rests on it:** T3\n",
        "- **Rests on it:** T3 and more\n",
        "A3 names what rests on it with text that is not an ID",
    ),
    (
        "no-if-wrong",
        "docs/assumptions/git.md",
        "- **If it is wrong:** a check could pass on a git that behaves otherwise.\n",
        "",
        "A3 does not say what changes if it is wrong",
    ),
    (
        "no-relied-on",
        "docs/assumptions/git.md",
        "  - **Relied on:** T3\n",
        "",
        "A3, fact 1, does not say where it is relied on",
    ),
    (
        "no-check",
        "docs/assumptions/git.md",
        "  - **Checked:** tested: `tests/test_example.py::test_example`\n",
        "",
        "A3, fact 1, does not say how it is checked",
    ),
    (
        "unknown-check",
        "docs/assumptions/git.md",
        "  - **Checked:** tested: `tests/test_example.py::test_example`\n",
        "  - **Checked:** believed\n",
        "A3, fact 1, does not say how it is checked",
    ),
    (
        "not-yet-without-task-or-reason",
        "docs/assumptions/python-tools-and-prices.md",
        "not yet: `a-change` task 1.1 checks it",
        "not yet: soon",
        "A4, fact 1, is not yet checked and names neither the task that will check it nor why"
        " none will",
    ),
    (
        "no-facts",
        "docs/assumptions/python-tools-and-prices.md",
        "- **Fact:** A model's price changes rarely.\n  - **Relied on:** DR-001\n"
        "  - **Checked:** not yet: `a-change` task 1.1 checks it\n",
        "",
        "A4 lists no fact",
    ),
    (
        "fact-states-nothing",
        "docs/assumptions/git.md",
        "- **Fact:** git does what its own tests say.\n",
        "- **Fact:**\n",
        "A3, fact 1, states nothing",
    ),
    (
        "line-not-a-field",
        "docs/assumptions/git.md",
        "- **If it is wrong:** a check could pass on a git that behaves otherwise.\n",
        "- **If it is wrong:** a check could pass on a git\nthat behaves otherwise.\n",
        "A3 has a line that is not a field, which no check reads",
    ),
    (
        "fact-field-before-a-fact",
        "docs/assumptions/git.md",
        "- **Rests on it:** T3\n",
        "- **Rests on it:** T3\n  - **Relied on:** T3\n",
        "A3 has a line that is not a field, which no check reads",
    ),
    (
        "unknown-field",
        "docs/assumptions/git.md",
        "- **If it is wrong:** a check could pass on a git that behaves otherwise.\n",
        "- **If it is wrong:** a check could pass on a git that behaves otherwise.\n"
        "- **Owner:** someone\n",
        "A3 has a field that the assumptions do not have: Owner",
    ),
    (
        "unknown-fact-field",
        "docs/assumptions/git.md",
        "  - **Relied on:** T3\n",
        "  - **Relied on:** T3\n  - **Source:** a page\n",
        "A3 has a field that the assumptions do not have: Source",
    ),
    (
        "field-given-twice",
        "docs/assumptions/git.md",
        "- **Rests on it:** T3\n",
        "- **Rests on it:** T3\n- **Rests on it:** T3\n",
        "A3 gives Rests on it more than once",
    ),
    (
        "fact-field-given-twice",
        "docs/assumptions/git.md",
        "  - **Relied on:** T3\n",
        "  - **Relied on:** T3\n  - **Relied on:** T3\n",
        "A3, fact 1, gives Relied on more than once",
    ),
    # A citation of nothing fails CI.
    (
        "unknown-requirement",
        "docs/assumptions/git.md",
        "- **Rests on it:** R2, T2\n",
        "- **Rests on it:** R2, R9, T2\n",
        "A2 names R9, which is not a requirement in the register",
    ),
    (
        "unknown-threat",
        "docs/assumptions/git.md",
        "  - **Relied on:** T3\n",
        "  - **Relied on:** T3, T9\n",
        "A3 names T9, which is not a threat",
    ),
    (
        "unknown-record",
        "docs/assumptions/python-tools-and-prices.md",
        "- **Rests on it:** DR-001\n",
        "- **Rests on it:** DR-001, DR-009\n",
        "A4 names DR-009, which is not a decision record",
    ),
    (
        "unknown-task",
        "docs/assumptions/github.md",
        "`a-change` task 1.1\n",
        "`a-change` task 9.9\n",
        "A1 names `a-change` task 9.9, which does not exist",
    ),
    (
        "unknown-task-to-check",
        "docs/assumptions/python-tools-and-prices.md",
        "`a-change` task 1.1 checks it",
        "`a-change` task 9.9 checks it",
        "A4 names `a-change` task 9.9, which does not exist",
    ),
    (
        "unknown-decision",
        "docs/assumptions/git.md",
        "`a-change` decision 1\n",
        "`a-change` decision 9\n",
        "A2 names `a-change` decision 9, which does not exist",
    ),
    (
        "unknown-scenario",
        "docs/assumptions/git.md",
        '`thing`: "It works"',
        '`thing`: "It fails"',
        'A2 names `thing`: "It fails", which no spec holds',
    ),
    (
        "unknown-path",
        "docs/assumptions/github.md",
        "`docs/threat-model.md`",
        "`docs/missing.md`",
        "A1 names `docs/missing.md`, which is not a file in this repository",
    ),
    (
        "relied-on-prose",
        "docs/assumptions/git.md",
        "  - **Relied on:** T3\n",
        "  - **Relied on:** T3 and the tests\n",
        "A3, fact 1, says where it is relied on with text that is not a citation",
    ),
    (
        "relied-on-not-resting",
        "docs/assumptions/git.md",
        "  - **Relied on:** T3\n",
        "  - **Relied on:** T3, R1\n",
        "A3, fact 1, is relied on by R1, which A3 does not name as resting on it",
    ),
    (
        "test-not-collected",
        "docs/assumptions/git.md",
        "tested: `tests/test_example.py::test_example`",
        "tested: `tests/test_example.py::test_gone`",
        "A3 names tests/test_example.py::test_gone, which is not a collected test",
    ),
    (
        "tested-without-a-test",
        "docs/assumptions/git.md",
        "tested: `tests/test_example.py::test_example`",
        "tested: the example test",
        "A3, fact 1, names what checks it with text that is not a test's name",
    ),
    (
        "handled-by-not-collected",
        "docs/assumptions/github.md",
        "  - **Handled by:** `tests/test_example.py::test_example`\n",
        "  - **Handled by:** `tests/test_example.py::test_gone`\n",
        "A1 names tests/test_example.py::test_gone, which is not a collected test",
    ),
    (
        "handled-by-not-a-test",
        "docs/assumptions/github.md",
        "  - **Handled by:** `tests/test_example.py::test_example`\n",
        "  - **Handled by:** the example test\n",
        "A1, fact 1, names what handles it with text that is not a test's name",
    ),
    # An assumption and a threat that do not name each other fail CI.
    (
        "threat-does-not-name-assumption",
        "docs/threat-model.md",
        "- **Assumptions:** A1\n",
        "",
        "A1 names T1, which does not name A1",
    ),
    (
        "assumption-does-not-name-threat",
        "docs/threat-model.md",
        "- **Assumptions:** A3\n",
        "- **Assumptions:** A3, A2\n",
        "T3 names A2, which does not name T3",
    ),
    (
        "threat-names-no-assumption",
        "docs/threat-model.md",
        "- **Assumptions:** A3\n",
        "- **Assumptions:** A3, A9\n",
        "T3 names A9, which is not an assumption",
    ),
    # A fact that no test can reach, checked by a test alone, fails CI.
    (
        "github-fact-tested-alone",
        "docs/assumptions/github.md",
        "  - **Checked:** documented: <https://docs.github.com/en/actions>, read 2026-11-01\n",
        "  - **Checked:** tested: `tests/test_example.py::test_example`\n",
        "A1, fact 1, is about GitHub, which no test may reach, and is checked by a test alone",
    ),
    (
        "price-fact-tested-alone",
        "docs/assumptions/python-tools-and-prices.md",
        "  - **Checked:** not yet: `a-change` task 1.1 checks it\n",
        "  - **Checked:** tested: `tests/test_example.py::test_example`\n",
        "A4, fact 1, is about prices, which no test may reach, and is checked by a test alone",
    ),
    (
        "outside-the-sections",
        "docs/assumptions/python-tools-and-prices.md",
        "## Prices\n\n",
        "",
        "A4 stands outside the sections of python-tools-and-prices.md",
    ),
    # An observation that cannot be followed fails CI.
    (
        "observation-without-file",
        "docs/assumptions/git.md",
        "observed: `tests/test_example.py`, ",
        "observed: ",
        "A2, fact 1, gives an observation without its file, its date, or its program, version"
        " and build",
    ),
    (
        "observation-with-missing-file",
        "docs/assumptions/git.md",
        "observed: `tests/test_example.py`",
        "observed: `tests/test_missing.py`",
        "A2, fact 1, names tests/test_missing.py, which is not a file under tests/",
    ),
    (
        "observation-outside-tests",
        "docs/assumptions/git.md",
        "observed: `tests/test_example.py`",
        "observed: `docs/requirements.md`",
        "A2, fact 1, gives an observation without its file, its date, or its program, version"
        " and build",
    ),
    (
        "observation-climbing-out-of-tests",
        "docs/assumptions/git.md",
        "observed: `tests/test_example.py`",
        "observed: `tests/../docs/requirements.md`",
        "A2, fact 1, names tests/../docs/requirements.md, which is not a file under tests/",
    ),
    (
        "observation-without-date",
        "docs/assumptions/git.md",
        "`tests/test_example.py`, 2026-11-01, git",
        "`tests/test_example.py`, git",
        "A2, fact 1, gives an observation without its file, its date, or its program, version"
        " and build",
    ),
    (
        "observation-with-impossible-date",
        "docs/assumptions/git.md",
        "`tests/test_example.py`, 2026-11-01, git",
        "`tests/test_example.py`, 2026-13-01, git",
        "A2, fact 1, gives a date that is not a day of the calendar: 2026-13-01",
    ),
    (
        "observation-without-build",
        "docs/assumptions/git.md",
        ", build `1:2.43.0-1ubuntu7.3`",
        "",
        "A2, fact 1, gives an observation without its file, its date, or its program, version"
        " and build",
    ),
    # A documented fact that links elsewhere fails CI.
    (
        "documented-on-another-host",
        "docs/assumptions/github.md",
        "<https://docs.github.com/en/actions>",
        "<https://example.com/en/actions>",
        "A1, fact 1, links example.com, which is not a documentation host that this test lists",
    ),
    (
        "documented-on-a-host-behind-a-name",
        "docs/assumptions/github.md",
        "<https://docs.github.com/en/actions>",
        "<https://docs.github.com@example.com/en/actions>",
        "A1, fact 1, links example.com, which is not a documentation host that this test lists",
    ),
    (
        "documented-over-http",
        "docs/assumptions/github.md",
        "<https://docs.github.com/en/actions>",
        "<http://docs.github.com/en/actions>",
        "A1, fact 1, links an address that is not https",
    ),
    (
        "documented-github-not-at-a-full-commit",
        "docs/assumptions/git.md",
        "blob/1f2e64e22dee75db96b92d526d14003ba59a154e/",
        "blob/v2.43.4/",
        "A2, fact 2, links a GitHub address that is not a file at a full commit",
    ),
    (
        "documented-with-other-link-text",
        "docs/assumptions/github.md",
        "<https://docs.github.com/en/actions>",
        "[GitHub's documentation](https://docs.github.com/en/actions)",
        "A1, fact 1, shows link text other than its address",
    ),
    (
        "documented-on-a-day-that-is-not",
        "docs/assumptions/github.md",
        "<https://docs.github.com/en/actions>, read 2026-11-01",
        "<https://docs.github.com/en/actions>, read 2026-02-30",
        "A1, fact 1, gives a date that is not a day of the calendar: 2026-02-30",
    ),
    (
        "documented-without-date",
        "docs/assumptions/github.md",
        "<https://docs.github.com/en/actions>, read 2026-11-01",
        "<https://docs.github.com/en/actions>",
        "A1, fact 1, gives a documented check without its links or the date they were read",
    ),
    (
        "documented-without-link",
        "docs/assumptions/github.md",
        "<https://docs.github.com/en/actions>, read 2026-11-01",
        "GitHub's documentation, read 2026-11-01",
        "A1, fact 1, gives a documented check without its links or the date they were read",
    ),
    # The assumptions with the most at stake come first.
    (
        "higher-impact-listed-second",
        "docs/assumptions/README.md",
        "- **A1.** GitHub enforces what a workflow declares. Impact 3, risk 3. Page: "
        "[GitHub](github.md).\n- **A2.** git stays offline when told to. Impact 2, risk 6. "
        "Page: [git](git.md).\n",
        "- **A2.** git stays offline when told to. Impact 2, risk 6. Page: [git](git.md).\n"
        "- **A1.** GitHub enforces what a workflow declares. Impact 3, risk 3. Page: "
        "[GitHub](github.md).\n",
        "A1 stands after A2 on the index, though it has more at stake",
    ),
    (
        "index-line-without-impact",
        "docs/assumptions/README.md",
        "Impact 2, risk 6. Page: [git]",
        "Risk 6. Page: [git]",
        "A2's line on the index does not give its impact and its risk",
    ),
    (
        "index-line-without-page",
        "docs/assumptions/README.md",
        "Impact 1, risk 1. Page: [git](git.md).",
        "Impact 1, risk 1.",
        "A3's line on the index does not end with a link to its page",
    ),
    (
        "index-rating-differs",
        "docs/assumptions/README.md",
        "Impact 2, risk 6.",
        "Impact 2, risk 4.",
        "the index gives A2 impact 2 and risk 4, where its threats give impact 2 and risk 6",
    ),
    (
        "index-says-no-threat",
        "docs/assumptions/README.md",
        "Impact 1, risk 1.",
        "No threat.",
        "the index gives A3 no threat, where its threats give impact 1 and risk 1",
    ),
    (
        "index-rates-an-assumption-without-a-threat",
        "docs/assumptions/README.md",
        "No threat. Page: [Python",
        "Impact 1, risk 1. Page: [Python",
        "the index gives A4 impact 1 and risk 1, where no threat rests on it",
    ),
    (
        "index-without-the-rating-note",
        "docs/assumptions/README.md",
        "A risk below is rated with the assumption true",
        "A risk below is rated",
        "the index does not say above its list that a risk is rated with the assumption true",
    ),
    (
        "index-without-its-list",
        "docs/assumptions/README.md",
        "## The assumptions, most at stake first\n",
        "## The assumptions\n",
        'the index has no section "The assumptions, most at stake first"',
    ),
    (
        "index-line-names-no-assumption",
        "docs/assumptions/README.md",
        "## The assumptions, most at stake first\n\n",
        "## The assumptions, most at stake first\n\nAll of them:\n\n",
        "the index's list has a line that names no assumption, which no check reads",
    ),
    # An assumption is on the index and on its page, with one statement.
    (
        "on-the-index-and-on-no-page",
        "docs/assumptions/python-tools-and-prices.md",
        "### A4. Prices change rarely.",
        "### A5. Prices change rarely.",
        "A4 is on the index and on no page",
    ),
    (
        "on-a-page-and-not-on-the-index",
        "docs/assumptions/README.md",
        "- **A3.** git keeps its word. Impact 1, risk 1. Page: [git](git.md).\n",
        "",
        "A3 is on git.md and not on the index",
    ),
    (
        "on-the-index-twice",
        "docs/assumptions/README.md",
        "- **A3.** git keeps its word. Impact 1, risk 1. Page: [git](git.md).\n",
        "- **A3.** git keeps its word. Impact 1, risk 1. Page: [git](git.md).\n" * 2,
        "A3 is on the index more than once",
    ),
    (
        "index-names-another-page",
        "docs/assumptions/README.md",
        "Impact 1, risk 1. Page: [git](git.md).",
        "Impact 1, risk 1. Page: [GitHub](github.md).",
        "the index puts A3 on github.md, but it is on git.md",
    ),
    (
        "statement-differs",
        "docs/assumptions/README.md",
        "- **A3.** git keeps its word.",
        "- **A3.** git keeps its promises.",
        "A3's statement on the index differs from its page's",
    ),
    (
        "id-used-twice",
        "docs/assumptions/python-tools-and-prices.md",
        "### A4. Prices change rarely.",
        "### A3. Prices change rarely.",
        "A3 is used more than once",
    ),
    (
        "retired-and-in-use",
        "docs/assumptions/README.md",
        "## Retired IDs\n\nNone yet.\n",
        "## Retired IDs\n\n- A3, removed by `old-change`\n",
        "A3 is retired and still in use",
    ),
    # The threat model's settings are each a fact that is not yet checked.
    (
        "setting-in-no-fact",
        "docs/assumptions/github.md",
        "- **Fact:** **Approval for runs** is as the threat model's settings list it.\n",
        "- **Fact:** The approval is as the threat model's settings list it.\n",
        'the threat model\'s setting "Approval for runs" is in no fact that cites'
        " `docs/threat-model.md`",
    ),
    (
        "setting-checked",
        "docs/assumptions/github.md",
        "not yet: none will, since no test may read a setting on GitHub",
        "documented: <https://docs.github.com/en/actions>, read 2026-11-01",
        'the threat model\'s setting "Approval for runs" is checked as documented, though no'
        " test may read a setting on GitHub",
    ),
]


@pytest.mark.parametrize(("name", "path", "old", "new", "expected"), CASES)
def test_a_planted_defect_is_reported(
    tmp_path: Path, name: str, path: str, old: str, new: str, expected: str
) -> None:
    root = synthetic_repository(tmp_path)
    plant(root, path, old, new)
    assert expected in found(root), name


# The subjects that no test may reach (DR-090), written out rather than read from
# PAGES, so that a subject that PAGES stops naming fails here.
UNREACHABLE = [
    ("claude-code.md", "", "Claude Code"),
    ("github.md", "", "GitHub"),
    ("python-tools-and-prices.md", "Prices", "prices"),
    ("adopters-and-people.md", "", "adopters and people"),
]


@pytest.mark.parametrize(("page", "section", "subject"), UNREACHABLE)
def test_a_fact_that_no_test_may_reach_is_reported_when_tested_alone(
    tmp_path: Path, page: str, section: str, subject: str
) -> None:
    root = synthetic_repository(tmp_path)
    heading = f"## {section}\n\n### A5." if section else "## A5."
    (root / FOLDER / page).write_text(
        f"# A subject\n\n{heading} Something holds.\n\n"
        "- **Rests on it:** T1\n"
        "- **If it is wrong:** a figure would be wrong.\n"
        "- **Fact:** Something holds.\n"
        "  - **Relied on:** T1\n"
        f"  - **Checked:** tested: `{EXAMPLE_TEST}`\n"
    )
    assert (
        f"A5, fact 1, is about {subject}, which no test may reach, and is checked by a test alone"
        in found(root)
    )


def test_an_assumption_out_of_order_on_its_page_is_reported(tmp_path: Path) -> None:
    root = synthetic_repository(tmp_path)
    head, a2, a3 = re.split(r"(?=^## A)", GIT, flags=re.M)
    (root / "docs/assumptions/git.md").write_text(head + a3 + "\n" + a2.rstrip("\n") + "\n")
    assert "A3 stands before A2 on git.md, unlike the index" in found(root)


def test_an_id_left_out_of_the_numbers_is_reported(tmp_path: Path) -> None:
    root = synthetic_repository(tmp_path)
    plant(root, "docs/assumptions/python-tools-and-prices.md", "### A4.", "### A6.")
    plant(root, "docs/assumptions/README.md", "- **A4.**", "- **A6.**")
    assert (
        "the assumptions are not numbered from A1 to A6 without a gap, apart from retired IDs;"
        " missing: A4, A5"
    ) in found(root)
    plant(
        root,
        "docs/assumptions/README.md",
        "None yet.\n",
        "- A4, removed by `old`\n- A5, removed by `old`\n",
    )
    assert found(root) == []


def test_a_page_without_assumptions_or_unknown_to_the_test_is_reported(tmp_path: Path) -> None:
    root = synthetic_repository(tmp_path)
    (root / "docs/assumptions/claude-code.md").write_text("# Claude Code\n\nNothing yet.\n")
    (root / "docs/assumptions/other.md").write_text("# Other\n")
    problems_found = found(root)
    assert "claude-code.md holds no assumption" in problems_found
    assert "other.md is not a subject page that this test knows" in problems_found


@pytest.mark.parametrize(
    ("path", "private", "label"),
    [
        ("docs/assumptions/github.md", HOME, "a path under a home folder"),
        ("docs/assumptions/git.md", MAC_HOME, "a path under a home folder"),
        ("docs/assumptions/git.md", ROOT_HOME, "a path under a home folder"),
        ("docs/assumptions/git.md", WINDOWS_HOME, "a path under a home folder"),
        ("docs/assumptions/README.md", SESSION, "a session identifier"),
        ("docs/assumptions/git.md", SESSION_NAME, "a session identifier"),
        ("tests/test_example.py", HOME, "a path under a home folder"),
        ("tests/test_example.py", SESSION, "a session identifier"),
    ],
)
def test_a_private_source_is_reported_by_file_and_line_without_its_text(
    tmp_path: Path, path: str, private: str, label: str
) -> None:
    root = synthetic_repository(tmp_path)
    file = root / path
    file.write_text(file.read_text() + f"# Seen in {private}.\n")
    number = len(file.read_text().splitlines())
    problems_found = found(root)
    assert f"{path}:{number} holds {label}" in problems_found
    assert not any(private in problem for problem in problems_found)


def test_a_generic_home_path_is_not_a_private_source(tmp_path: Path) -> None:
    root = synthetic_repository(tmp_path)
    plant(
        root,
        "docs/assumptions/git.md",
        "git reads `GIT_NO_LAZY_FETCH`.",
        "git reads `~/.gitconfig`.",
    )
    assert found(root) == []


def test_a_changed_rating_or_check_moves_an_assumption_out_of_order(tmp_path: Path) -> None:
    root = synthetic_repository(tmp_path)
    # T3 now matters as much as T2, and A3's fact is no longer checked, so A3
    # belongs before A2, and its line on the index gives the old rating.
    plant(root, "docs/threat-model.md", "- **Impact:** 1 (low)", "- **Impact:** 2 (medium)")
    plant(root, "docs/threat-model.md", "- **Risk:** 1\n", "- **Risk:** 2\n")
    plant(
        root,
        "docs/assumptions/git.md",
        "tested: `tests/test_example.py::test_example`",
        "not yet: `a-change` task 1.1 checks it",
    )
    problems_found = found(root)
    assert "A3 stands after A2 on the index, though it has more at stake" in problems_found
    assert (
        "the index gives A3 impact 1 and risk 1, where its threats give impact 2 and risk 2"
        in problems_found
    )


def test_a_parametrized_test_is_named_without_its_parameters(tmp_path: Path) -> None:
    root = synthetic_repository(tmp_path)
    collected = frozenset({EXAMPLE_TEST, "tests/test_example.py::test_cases[one]"})
    plant(root, "docs/assumptions/git.md", "test_example`\n", "test_cases`\n")
    assert found(root, collected) == []
    plant(root, "docs/assumptions/git.md", "test_cases`\n", "test_case`\n")
    assert "A3 names tests/test_example.py::test_case, which is not a collected test" in found(
        root, collected
    )


def test_collected_tests_are_those_pytest_collects() -> None:
    collected = collected_tests(ROOT)
    assert "tests/test_assumptions.py::test_the_assumptions_hold" in collected
    assert "tests/test_assumptions.py::test_no_such_test" not in collected


def test_the_assumptions_hold() -> None:
    found_problems, facts = problems(ROOT, collected_tests(ROOT))
    assert not found_problems, "\n".join(found_problems)
    assert facts, "no fact was read, so this test covered nothing"
