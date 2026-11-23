"""Write the risk register, `docs/risk-register.md`, from the threat model.

    python3 -I scripts/risk_register.py               writes the page
    python3 -I scripts/risk_register.py --check       writes nothing, and fails when the
                                                      committed page differs
    python3 -I scripts/risk_register.py --blind N     prints boundary N's threats without
                                                      their ratings

It reads the threat model, `docs/threat-model.md`, the specs under `openspec/` and the
register of requirements, `docs/requirements.md`, and nothing else, with the standard
library alone and no connection (R245, design decision 20, DR-256). The page gives the
bands, how many threats each holds, raw and with the answers in place (R247), a matrix
of each kind of rating, the high and critical risks with their further answers or
acceptances, and a row for each threat, highest risk with its answer in place first,
then highest raw risk, then by ID, that names what answers the threat by ID: the
requirement that holds each scenario that its Held by cites, each record, each task or
decision of a change and each file, and the assumptions that it rests on (R248).

It writes nothing and fails, naming the threat, on a rating that it cannot read, on a
scenario that the specs and the register cannot place under a requirement, and on text
that the roadmap's rule forbids in anything that it would copy onto the page: a `|`,
outside the separators of its tables, a `<`, a `&`, a backslash, a `]:` or a character
other than printable ASCII (R246). It refuses the threat model, the register of
requirements or the page when it, or a folder on its way, is a symbolic link, so that it
reads and writes only the repository's own files (R245). With `--check` it names the
threat whose row differs, is left out, is listed twice or is no threat, or the line that
differs.

With `--blind`, it prints the threat model's method, the boundary's line from the list
of trust boundaries, and the boundary's threats without any rating line, without an
acceptance and without the records that an acceptance cites, so that the reviewers of the
raw ratings are not shown the ratings with the answers in place (task 1.38, DR-254). It
keeps a further answer, which raw rating takes away, and which shows that a threat is high
or critical.

The bands are one table, `BANDS`, and a further answer that cites a backlog item is a plan
(`plan_items`, DR-255). The threat model's test imports both, and the release check,
which task 6.1 adds to this script as a mode of its own, since under `python3 -I` a script
cannot import a module beside it (design decision 20), reads them here.

It exits 0 when it has written or matched the page, 1 when it refuses or the page
differs, and 2 on a command line that it does not take.
"""

from __future__ import annotations

import difflib
import re
import sys
from dataclasses import dataclass, fields
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THREAT_MODEL = "docs/threat-model.md"
REGISTER = "docs/requirements.md"
PAGE = "docs/risk-register.md"

# OWASP's Risk Rating Methodology's table of overall risk severity, read for each score of
# impact times likelihood (R247, DR-253).
BANDS: dict[int, str] = {1: "note", 2: "low", 3: "medium", 4: "medium", 6: "high", 9: "critical"}
FURTHER = ("high", "critical")
IMPACTS = {1: "low", 2: "medium", 3: "high"}
LIKELIHOODS = {1: "unlikely", 2: "possible", 3: "likely"}
RATED = (
    ("Impact", IMPACTS),
    ("Likelihood", LIKELIHOODS),
    ("Raw impact", IMPACTS),
    ("Raw likelihood", LIKELIHOODS),
)
RATING_FIELDS = ("Impact", "Likelihood", "Risk", "Raw impact", "Raw likelihood", "Raw risk")

HEADING = re.compile(r"^### (T(\d+))\. (.+)$", re.M)
ANY_HEADING = re.compile(r"^#{1,3} ", re.M)
FIELD = re.compile(r"^- \*\*([^*]+):\*\* ?(.*)$", re.M)
BOUNDARY = re.compile(r"^## Boundary (\d+)\b", re.M)
BOUNDARY_LINE = re.compile(r"^(\d+)\. \*\*.+$", re.M)
METHOD = re.compile(r"^## How it was built\n.*?(?=^## )", re.M | re.S)
SCENARIO_REF = re.compile(r'`([a-z0-9-]+)`: "([^"]+)"')
TASK_REF = re.compile(r"`([a-z0-9-]+)` task (\d+\.\d+)")
DECISION_REF = re.compile(r"`([a-z0-9-]+)` decision (\d+)")
RECORD_REF = re.compile(r"\bDR-(\d{3,})\b")
ITEM_REF = re.compile(r"\bB-(\d{3})\b")
PATH_REF = re.compile(r"`([^`\s]+)`")
RATING = re.compile(r"([1-3]) \(([a-z]+)\)")
REQUIREMENT = re.compile(r"^### Requirement: (.+?)\s*$")
SCENARIO = re.compile(r"^#### Scenario: (.+?)\s*$")
REGISTER_ROW = re.compile(r"^\| (R\d+) \| [a-z-]+ \| `([a-z0-9-]+)` \| (.+?) \|\s*$", re.M)
ROW_ID = re.compile(r"^\| \[(T\d+)\]\(")
# The files that others write, under the vendored tree but its root lock and in the generated
# skills, which the roadmap's rule lets no page name (R209, R246), as `scripts/conventions.py`
# gives them. Under `python3 -I` this script cannot import that module, so it keeps this copy,
# which the register's test holds to it.
OTHERS_WRITE = re.compile(
    r"vendor/superpowers/(?!UPSTREAM\.lock\Z)|\.claude/skills/openspec-[^/]+/"
)
# What the roadmap's rule forbids, the table's `|` among them, since nothing that the page
# copies from the threat model stands as a separator (R246).
FORBIDDEN = ("|", "<", "&", "\\", "]:")


class RegisterError(Exception):
    """The script refuses its input, and writes nothing."""

    def __init__(self, problems: list[str]) -> None:
        super().__init__("\n".join(problems))
        self.problems = problems


@dataclass(frozen=True)
class Threat:
    ident: str
    number: int
    fields: dict[str, list[str]]
    others: tuple[str, ...]
    title: str
    boundary: int

    def field(self, name: str) -> str:
        return self.fields.get(name, [""])[0]


def threats_in(text: str) -> list[Threat]:
    """Each `### T<n>.` heading's threat: its fields, any line that is not a field, and the
    number of the `## Boundary` heading above it, or 0."""
    marks = list(HEADING.finditer(text))
    boundaries = [(found.start(), int(found.group(1))) for found in BOUNDARY.finditer(text)]
    found = []
    for mark in marks:
        body = text[mark.end() :]
        following = ANY_HEADING.search(body)
        if following:
            body = body[: following.start()]
        named: dict[str, list[str]] = {}
        for field in FIELD.finditer(body):
            named.setdefault(field.group(1), []).append(field.group(2).strip())
        # A line that is not a field is part of the field above it on GitHub, unread here.
        others = tuple(line for line in body.split("\n") if line.strip() and not FIELD.match(line))
        boundary = max(
            ((start, number) for start, number in boundaries if start < mark.start()),
            default=(0, 0),
        )[1]
        found.append(
            Threat(
                ident=mark.group(1),
                number=int(mark.group(2)),
                fields=named,
                others=others,
                title=mark.group(3).strip(),
                boundary=boundary,
            )
        )
    return found


@dataclass(frozen=True)
class Citations:
    """What a Held by cites, by kind."""

    scenarios: list[tuple[str, str]]
    tasks: list[tuple[str, str]]
    decisions: list[tuple[str, str]]
    records: list[str]
    paths: list[str]

    def __len__(self) -> int:
        """How many citations it holds, of every kind."""
        return sum(len(getattr(self, kind.name)) for kind in fields(self))


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


def rating(value: str, levels: dict[int, str]) -> int:
    """A rating's level, or 0 when the value is not a level from its list with its name."""
    match = RATING.fullmatch(value)
    if not match or levels.get(int(match.group(1))) != match.group(2):
        return 0
    return int(match.group(1))


def score_of(threat: Threat, impact: str = "Impact", likelihood: str = "Likelihood") -> int:
    """A threat's risk, raw or with its answer in place, or 0 when a rating is unreadable."""
    return rating(threat.field(impact), IMPACTS) * rating(threat.field(likelihood), LIKELIHOODS)


def plan_items(further: str) -> list[str]:
    """The backlog items that a further answer cites, in order. A further answer that cites
    one is a plan, whatever else it names: it does not count toward the rating with the
    answer in place until it cites what holds it alone (DR-255)."""
    return [f"B-{number}" for number in dict.fromkeys(ITEM_REF.findall(further))]


def band(score: int) -> str:
    return BANDS[score]


def bands_by_name() -> dict[str, list[int]]:
    by_name: dict[str, list[int]] = {}
    for score, name in BANDS.items():
        by_name.setdefault(name, []).append(score)
    return by_name


def bands_phrase() -> str:
    """The bands as R247 and DR-253 state them, from the table."""
    parts = [
        " and ".join(map(str, scores)) + f" {name}" for name, scores in bands_by_name().items()
    ]
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def slug(heading: str) -> str:
    """The anchor that GitHub gives a heading, as the roadmap's test reads it."""
    text = re.sub(r"[^a-z0-9 _-]", "", heading.replace("`", "").lower())
    return text.replace(" ", "-")


def forbidden(text: str) -> list[str]:
    marks = [mark for mark in FORBIDDEN if mark in text]
    marks += sorted({f"U+{ord(c):04X}" for c in text if not " " <= c <= "~"})
    return marks


@dataclass(frozen=True)
class Rated:
    """A threat as the page gives it."""

    threat: Threat
    ratings: dict[str, int]
    answered: str

    @property
    def risk(self) -> int:
        return self.ratings["Impact"] * self.ratings["Likelihood"]

    @property
    def raw(self) -> int:
        return self.ratings["Raw impact"] * self.ratings["Raw likelihood"]

    def key(self) -> tuple[int, int, int]:
        return (-self.risk, -self.raw, self.threat.number)


def linked(root: Path, name: str) -> bool:
    """Whether the file, or a folder on its way from root, is a symbolic link."""
    path = root
    for part in Path(name).parts:
        path = path / part
        if path.is_symlink():
            return True
    return False


def read(root: Path, name: str) -> str:
    """The file's text, or nothing when it does not exist. Raises RegisterError when it, or
    a folder on its way, is a symbolic link."""
    if linked(root, name):
        raise RegisterError([f"{name} is a symbolic link, which the script does not follow"])
    path = root / name
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def requirements_of(root: Path) -> dict[tuple[str, str], str]:
    """The ID of the requirement that holds each scenario, by capability and name, through
    the specs, active changes included and archived ones not, and the register."""
    registered = {
        (capability, name): ident
        for ident, capability, name in REGISTER_ROW.findall(read(root, REGISTER))
    }
    specs = [
        *(root / "openspec" / "specs").glob("*/spec.md"),
        *(root / "openspec" / "changes").glob("*/specs/*/spec.md"),
    ]
    held: dict[tuple[str, str], str] = {}
    for spec in sorted(specs):
        capability = spec.parent.name
        requirement = ""
        for line in spec.read_text(encoding="utf-8").split("\n"):
            if found := REQUIREMENT.match(line):
                requirement = registered.get((capability, found.group(1)), "")
            elif (found := SCENARIO.match(line)) and requirement:
                held[(capability, found.group(1))] = requirement
    return held


def shown_path(path: str) -> str:
    """A cited file as a row gives it: by its path, or, for a file that others write, which
    the roadmap's rule lets no page name, by the folder that holds it."""
    if not OTHERS_WRITE.match(path):
        return f"`{path}`"
    if path.startswith("vendor/"):
        return "a file under `vendor/`"
    return "a file of a generated skill under `.claude/`"


def answered_by(threat: Threat, held: dict[tuple[str, str], str]) -> tuple[str, list[str]]:
    """What answers a threat by ID, in the order the page gives it, and the problems."""
    cited = threat.field("Held by")
    if cited.lower().startswith("accepted"):
        return "accepted", []
    found = citations(cited)
    problems = []
    requirements = []
    for capability, name in found.scenarios:
        ident = held.get((capability, name))
        if not ident:
            problems.append(
                f'{threat.ident} cites `{capability}`: "{name}", which no requirement of the '
                "register holds"
            )
        elif ident not in requirements:
            requirements.append(ident)
    parts = [
        ", ".join(requirements),
        ", ".join(dict.fromkeys(f"DR-{number}" for number in found.records)),
        "; ".join(dict.fromkeys(f"`{change}` task {number}" for change, number in found.tasks)),
        "; ".join(
            dict.fromkeys(f"`{change}` decision {number}" for change, number in found.decisions)
        ),
        "; ".join(dict.fromkeys(shown_path(path) for path in found.paths)),
    ]
    return "; ".join(part for part in parts if part), problems


def rated(text: str, root: Path) -> list[Rated]:
    """Each threat with its ratings and what answers it, highest risk first.

    Raises RegisterError, naming each threat, when it cannot give one."""
    threats = threats_in(text)
    if not threats:
        raise RegisterError(["the threat model holds no threat"])
    held = requirements_of(root)
    problems = []
    found = []
    for threat in threats:
        ratings = {}
        for name, levels in RATED:
            ratings[name] = rating(threat.field(name), levels)
            if not ratings[name]:
                problems.append(f"{threat.ident} has no {name.lower()} that the script can read")
        answered, unplaced = answered_by(threat, held)
        problems += unplaced
        copied = {
            "title": threat.title,
            "kind": threat.field("Kind"),
            "assumptions": threat.field("Assumptions"),
            "further answer": threat.field("Further answer"),
            "acceptance": threat.field("Acceptance"),
            "Held by": answered,
        }
        for name, value in copied.items():
            if marks := forbidden(value):
                problems.append(f"{threat.ident}'s {name} holds {', '.join(marks)}")
        found.append(Rated(threat, ratings, answered))
    if problems:
        raise RegisterError(problems)
    return sorted(found, key=Rated.key)


def link(threat: Threat) -> str:
    return f"[{threat.ident}](threat-model.md#{slug(f'{threat.ident}. {threat.title}')})"


def cell(score: int, impact: int, likelihood: int) -> str:
    return f"{score} {band(score)} ({impact}, {likelihood})"


def matrix(threats: list[Rated], heading: str, impact: str, likelihood: str) -> list[str]:
    lines = [
        f"## {heading}",
        "",
        f"Each cell lists the threats whose {impact.lower()} and {likelihood.lower()} it names.",
        "",
        "| Impact by likelihood | 1 unlikely | 2 possible | 3 likely |",
        "|---|---|---|---|",
    ]
    ordered = sorted(threats, key=lambda each: each.threat.number)
    for level in sorted(IMPACTS, reverse=True):
        cells = [
            ", ".join(
                each.threat.ident
                for each in ordered
                if each.ratings[impact] == level and each.ratings[likelihood] == column
            )
            for column in sorted(LIKELIHOODS)
        ]
        row = "|".join(f" {cell} " if cell else " " for cell in cells)
        lines.append(f"| {level} {IMPACTS[level]} |{row}|")
    return [*lines, ""]


def page(text: str, root: Path) -> str:
    """The risk register, from the threat model's text and the specs and register at root.

    Raises RegisterError when it refuses its input."""
    threats = rated(text, root)
    lines = [
        "# Risk register",
        "",
        "`scripts/risk_register.py` writes this page from the threat model, "
        "[`docs/threat-model.md`](threat-model.md), the specs and the register of "
        "requirements. It is not edited by hand, and CI fails when it differs from what the "
        "script writes (R245, DR-256).",
        "",
        "Each threat has two ratings, each an impact and a likelihood from 1 to 3 as the "
        "threat model's method defines them, whose product is its risk. The raw rating takes "
        "the threat's answer as not built (R244, DR-254). The rating with the answer in place "
        "takes the answer as built as specified, before any code is built, until the review "
        "of what was built rates it again (DR-112).",
        "",
        "## Bands",
        "",
        "Each risk takes the band that the overall risk severity of OWASP's Risk Rating "
        "Methodology gives its score (R247, DR-253). Each threat whose risk with its answer "
        "in place is high or critical carries a further answer or, for a high one only, the "
        "owner's acceptance (R249, DR-255).",
        "",
        "| Band | Risk | Raw | With the answer in place |",
        "|---|---|---|---|",
    ]
    for name, scores in reversed(bands_by_name().items()):
        raw = sum(1 for each in threats if each.raw in scores)
        placed = sum(1 for each in threats if each.risk in scores)
        lines.append(f"| {name} | {' and '.join(map(str, scores))} | {raw} | {placed} |")
    lines += [f"| all | 1 to 9 | {len(threats)} | {len(threats)} |", ""]
    lines += matrix(threats, "Raw matrix", "Raw impact", "Raw likelihood")
    lines += matrix(threats, "Matrix with the answers in place", "Impact", "Likelihood")
    lines += [
        "## High and critical risks",
        "",
        "Each threat whose risk with its answer in place is high or critical, highest first, "
        "with its further answer or its acceptance (R249).",
        "",
    ]
    high = [each for each in threats if band(each.risk) in FURTHER]
    for each in high:
        threat = each.threat
        given = [
            f"{name}: {threat.field(name)}"
            for name in ("Further answer", "Acceptance")
            if threat.field(name)
        ]
        lines.append(
            f"- {link(threat)}: {threat.title}. {each.risk} {band(each.risk)}, raw {each.raw} "
            f"{band(each.raw)}. {' '.join(given) or 'Neither a further answer nor an acceptance.'}"
        )
    if not high:
        lines.append("None.")
    lines += [
        "",
        "## Every threat",
        "",
        "The highest risk with the answer in place first, then the highest raw risk, then by "
        "ID (R248). Each rating gives its risk, its band, and its impact and likelihood. What "
        "answers a threat names the requirement that holds each scenario that it cites, and "
        "each record, task, decision and file; its full answer is in the threat model, which "
        "its ID links.",
        "",
        "| ID | Threat | Boundary | Kind | Raw | With the answer in place | Answered by "
        "| Assumptions |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for each in threats:
        threat = each.threat
        r = each.ratings
        lines.append(
            f"| {link(threat)} | {threat.title} | {threat.boundary} | {threat.field('Kind')} "
            f"| {cell(each.raw, r['Raw impact'], r['Raw likelihood'])} "
            f"| {cell(each.risk, r['Impact'], r['Likelihood'])} | {each.answered} "
            f"| {threat.field('Assumptions') or 'none'} |"
        )
    return "\n".join(lines) + "\n"


def write(root: Path) -> str:
    """Writes the register at root, and returns it. Raises RegisterError, writing nothing,
    when it refuses its input."""
    text = page(read(root, THREAT_MODEL), root)
    read(root, PAGE)
    (root / PAGE).write_text(text, encoding="utf-8")
    return text


def check(root: Path, committed: str | None = None) -> list[str]:
    """How the committed register differs from what the script writes, by threat or line.

    Raises RegisterError when it refuses its input."""
    if committed is None:
        committed = read(root, PAGE)
        if not (root / PAGE).is_file():
            return [f"{PAGE} does not exist, so run python3 -I scripts/risk_register.py"]
    written = page(read(root, THREAT_MODEL), root)
    if committed == written:
        return []
    ours = {found.group(1): line for line in written.split("\n") if (found := ROW_ID.match(line))}
    theirs: list[tuple[str, str]] = [
        (found.group(1), line) for line in committed.split("\n") if (found := ROW_ID.match(line))
    ]
    listed = [ident for ident, _ in theirs]
    problems = [f"{ident} is left out of the register" for ident in ours if ident not in listed]
    problems += [
        f"{ident} is listed twice in the register"
        for ident in dict.fromkeys(listed)
        if listed.count(ident) > 1
    ]
    problems += [
        f"the register lists {ident}, which the threat model does not hold"
        for ident in dict.fromkeys(listed)
        if ident not in ours
    ]
    problems += [
        f"{ident}'s row differs from what the script writes"
        for ident, line in dict(theirs).items()
        if ident in ours and listed.count(ident) == 1 and line != ours[ident]
    ]
    if not problems:
        mine = written.split("\n")
        lines = committed.split("\n")
        matcher = difflib.SequenceMatcher(a=lines, b=mine, autojunk=False)
        for tag, start, end, other, _ in matcher.get_opcodes():
            if tag == "equal":
                continue
            if start == end:
                problems.append(f"the register lacks, after its line {start}, {mine[other]!r}")
            else:
                # A blank line's place is a guess of the matcher's; name a line with text.
                shown = next((n for n in range(start, end) if lines[n].strip()), start)
                problems.append(
                    f"line {shown + 1} of the register is not what the script writes: "
                    f"{lines[shown]!r}"
                )
    return problems


def blind(root: Path, boundary: int) -> str:
    """The method, the boundary's line and its threats, without any rating line, any
    acceptance, or the records that an acceptance cites in the threat's other fields.

    Raises RegisterError when the model holds no threat at the boundary."""
    text = read(root, THREAT_MODEL)
    threats = [threat for threat in threats_in(text) if threat.boundary == boundary]
    if not threats:
        raise RegisterError([f"the threat model holds no threat at boundary {boundary}"])
    method = METHOD.search(text)
    described = [
        found.group(0) for found in BOUNDARY_LINE.finditer(text) if int(found.group(1)) == boundary
    ]
    lines = [
        f"# The threats of trust boundary {boundary}, without their ratings",
        "",
        *described[:1],
        "",
        method.group(0).rstrip() if method else "",
        "",
    ]
    for threat in threats:
        lines += [f"### {threat.ident}. {threat.title}", ""]
        accepting = set(RECORD_REF.findall(threat.field("Acceptance")))
        for name, values in threat.fields.items():
            if name not in (*RATING_FIELDS, "Acceptance"):
                lines += [f"- **{name}:** {unaccepted(value, accepting)}" for value in values]
        lines.append("")
    return "\n".join(lines)


def unaccepted(value: str, accepting: set[str]) -> str:
    """A field without its citations of the records that the threat's acceptance cites, and
    the separators that they leave."""
    for number in accepting:
        value = re.sub(rf"(?:;\s*)?\bDR-{number}\b(?:;\s*)?", "; ", value)
    return value.strip("; ").replace(";  ", "; ")


def main(argv: list[str]) -> int:
    try:
        if argv == []:
            write(ROOT)
            return 0
        if argv == ["--check"]:
            if problems := check(ROOT):
                raise RegisterError(problems)
            return 0
        if len(argv) == 2 and argv[0] == "--blind" and re.fullmatch("[0-9]+", argv[1]):
            print(blind(ROOT, int(argv[1])), end="")
            return 0
    except RegisterError as error:
        for problem in error.problems:
            print(f"risk_register: {problem}", file=sys.stderr)
        return 1
    print(
        "risk_register: usage: python3 -I scripts/risk_register.py [--check | --blind N]",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
