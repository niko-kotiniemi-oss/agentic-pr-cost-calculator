"""How the specs are found and read, as the pinned OpenSpec reads them, where their
form fails, and where that reading differs from what the pinned OpenSpec CLI shows.

`tests/test_spec_form.py` describes these rules and holds them (R173 to R178; design
decision 12; DR-193 to DR-196). Like the tool, this runs on Python 3.11 and later with
the standard library alone, so that CI's `openspec` job, which installs no Python
package, runs the comparison: `python3 scripts/spec_form.py <openspec>`, at the
repository's root, as `scripts/verify-openspec.sh` does.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, NamedTuple, TypeVar

from wording import code_spans

OPENSPEC = "openspec"
ARCHIVE = "openspec/changes/archive"
CHANGES = "openspec/changes"

# What JavaScript's `trim` removes, its white space and its line terminators, so that a
# name or a text is trimmed here as OpenSpec trims it.
JS_SPACE = (
    "\t\n\v\f\r \u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009"
    "\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"
)
# A character that is not printable ASCII. A spec's lines end at line feeds, so none is
# left in a line.
NOT_PLAIN = re.compile(r"[^ -~]")
# As OpenSpec finds them: whole words, where a word is ASCII letters, digits and `_`.
SHALL_OR_MUST = re.compile(r"\b(?:SHALL|MUST)\b", re.ASCII)
# A line that starts with a bold label and a colon, as OpenSpec's METADATA_LINE matches a
# trimmed line. A label holds no `*`, so it is matched in one way only.
LABEL = re.compile(r"\*\*[^*]+\*\*:")
# A list's or a quote's marker and the spaces and tabs after it. GitHub starts a block,
# a heading or a fence among them, after each, where OpenSpec reads text (R175).
MARKER = re.compile(r"(?:[-*+][ \t]|\d{1,9}[.)][ \t]|>)[ \t]*")
# The marks with which GitHub would show a spec otherwise than its text: an HTML tag or
# comment, a character reference, an escaped character, a table's row, a link, a link
# reference definition or a footnote, a mathematical expression, and struck-through text.
MARKS = ("<", "&", "\\", "|", "](", "]:", "$", "~")
WHEN = "- **WHEN**"
THEN = "- **THEN**"
AND = "- **AND**"

PURPOSE = "Purpose"
REQUIREMENTS = "Requirements"
RENAMED = "RENAMED Requirements"
MAIN_SECTIONS = (PURPOSE, REQUIREMENTS)
CHANGE_SECTIONS = (
    PURPOSE,
    "ADDED Requirements",
    "MODIFIED Requirements",
    "REMOVED Requirements",
    RENAMED,
)
# The sections that give requirements, and the operation that each gives them.
OPERATIONS = {
    REQUIREMENTS: "",
    "ADDED Requirements": "ADDED",
    "MODIFIED Requirements": "MODIFIED",
    "REMOVED Requirements": "REMOVED",
}
# The requirements whose text OpenSpec reads and checks: a main spec's, and those that a
# change adds or modifies.
READ_FOR_TEXT = ("", "ADDED", "MODIFIED")
# A section that the spec gives but that is not read: one that OpenSpec does not read, or
# one given again.
UNREAD = "?"
LONGEST = 500

LINK = "is a symbolic link, which the test does not follow"
NO_SPEC = "openspec/: holds no spec that OpenSpec reads"
NO_REQUIREMENT = "openspec/: the specs give no requirement for the test to read"
NO_SCENARIO = "openspec/: the specs give no scenario for the test to read"
HASH = 'starts with "#", after any list or quote markers, but is not a heading in form'
FENCE = "starts with three backticks or tildes, after any list or quote markers, as a fence does"
UNDERLINE = (
    'holds only "=" or "-" signs after any list or quote markers, with which GitHub can make'
    " the line above it a heading"
)
BEFORE = "stands before the first requirement of its section"
FIRST_SECTION = "stands before the spec's first section"
NOT_RENAME = "is neither a FROM: nor a TO: line, which alone a RENAMED Requirements section holds"


class Spec(NamedTuple):
    """A spec that OpenSpec reads: its path from the repository's root, its change's
    folder, empty for a main spec, and the id that OpenSpec gives it, the folders below
    its specs folder joined by `/`."""

    path: str
    change: str
    ident: str


class Scenario(NamedTuple):
    """A scenario as OpenSpec shows it: its name, and its lines, trimmed as one text."""

    name: str
    text: str


class Requirement(NamedTuple):
    """A requirement as OpenSpec shows it. Its operation is empty in a main spec, and a
    rename gives its old name as `name` and its new one as `renamed_to`."""

    operation: str
    name: str
    text: str
    scenarios: tuple[Scenario, ...]
    renamed_to: str = ""


class Reading(NamedTuple):
    """The changes read, by folder name, and the requirements of each spec, by its
    change's folder name, empty for a main spec, and its id."""

    changes: frozenset[str]
    specs: dict[tuple[str, str], tuple[Requirement, ...]]


def shown(text: str) -> str:
    """The text with each character outside printable ASCII replaced by `U+` and its code
    point, so that no line of a spec or of the CLI's output starts a line here."""
    return "".join(
        character if " " <= character <= "~" else f"U+{ord(character):04X}" for character in text
    )


def js_trim(text: str) -> str:
    return text.strip(JS_SPACE)


def placed(path: str, regular: bool) -> Spec | str:
    """The spec that a file named `spec.md` in some case is, or why OpenSpec does not
    read it."""
    *folders, name = path.split("/")[1:]
    if name != "spec.md":
        return "OpenSpec reads only a file named spec.md"
    if not regular:
        return "it is not a regular file"
    if any(folder.startswith(".") for folder in folders):
        return "a folder whose name starts with a dot holds it"
    if folders[:1] == ["specs"]:
        change, below = "", folders[1:]
    elif len(folders) >= 3 and folders[0] == "changes" and folders[2] == "specs":
        change, below = folders[1], folders[3:]
    else:
        return "it stands outside the specs folders"
    if not below:
        return "it stands at the top of a specs folder"
    return Spec(path, change, "/".join(below))


def find_specs(root: Path) -> tuple[list[Spec], list[str]]:
    """The specs that OpenSpec reads, sorted by path, and a problem for each symbolic link
    in `openspec/` outside the archive, which is never followed, and for each file named
    `spec.md` in any case that is not one of them."""
    top = root / OPENSPEC
    if top.is_symlink():
        return [], [shown(f"{OPENSPEC}: {LINK}")]
    specs: list[Spec] = []
    problems: list[str] = []
    stack = [(top, OPENSPEC)] if top.is_dir() else []
    while stack:
        folder, name = stack.pop()
        with os.scandir(folder) as entries:
            for entry in entries:
                path = f"{name}/{entry.name}"
                if entry.is_symlink():
                    problems.append(f"{path}: {LINK}")
                elif entry.is_dir(follow_symlinks=False):
                    if path != ARCHIVE:
                        stack.append((Path(entry.path), path))
                elif entry.name.lower() == "spec.md":
                    spec = placed(path, entry.is_file(follow_symlinks=False))
                    if isinstance(spec, Spec):
                        specs.append(spec)
                    else:
                        problems.append(f"{path}: is not read as a spec: {spec}")
    return sorted(specs), sorted(shown(problem) for problem in problems)


def changes_in(root: Path) -> frozenset[str]:
    """The changes that the test reads: each folder in `openspec/changes/` but `archive`,
    a folder whose name starts with a dot, and a symbolic link."""
    folder = root / CHANGES
    if (root / OPENSPEC).is_symlink() or folder.is_symlink() or not folder.is_dir():
        return frozenset()
    with os.scandir(folder) as entries:
        return frozenset(
            entry.name
            for entry in entries
            if entry.is_dir(follow_symlinks=False)
            and entry.name != "archive"
            and not entry.name.startswith(".")
        )


def prose_of(line: str) -> tuple[list[str], list[int]]:
    """The parts of a line outside inline code, and the length of each run of backticks
    that no later run as long closes on the line, with the code spans that
    `scripts/wording.py` finds in a page's line."""
    spans, unclosed = code_spans(line)
    parts: list[str] = []
    start = 0
    for begin, end in spans:
        parts.append(line[start:begin])
        start = end
    parts.append(line[start:])
    return parts, unclosed


def plain_text(data: bytes) -> tuple[str | None, list[tuple[int, str]]]:
    """The spec's text, and each problem of its plain text by its line: bytes that are not
    UTF-8, after which nothing is read, a character other than printable ASCII, a mark
    that GitHub reads outside inline code, and a run of backticks left open."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        return None, [(data.count(b"\n", 0, error.start) + 1, "holds bytes that are not UTF-8")]
    problems: list[tuple[int, str]] = []
    for number, content in enumerate(text.split("\n"), 1):
        other = NOT_PLAIN.search(content)
        if other:
            problems.append(
                (number, f"holds {shown(other[0])}, which is not printable ASCII or a line feed")
            )
        parts, unclosed = prose_of(content)
        for mark in MARKS:
            if any(mark in part for part in parts):
                problems.append((number, f'holds "{mark}" outside inline code'))
        if unclosed:
            problems.append(
                (
                    number,
                    f"holds a run of backticks, {unclosed[0]} long, that no run as long closes"
                    " on its line",
                )
            )
    return text, problems


def without_closing_run(text: str) -> str:
    """The text without a closing run of `#` signs that spaces or tabs come before, as
    OpenSpec and GitHub leave it out of a heading."""
    end = text.rstrip(" \t")
    body = end.rstrip("#")
    if len(body) < len(end) and body[-1:] in (" ", "\t"):
        return body
    return text


class Line(NamedTuple):
    """What a line is: its kind; for a heading, the name that OpenSpec gives it, its text
    as OpenSpec trims it, and whether GitHub shows a name for it."""

    kind: str
    name: str = ""
    heading: str = ""
    named: bool = True


def starts(content: str) -> list[int]:
    """Where GitHub can start a block on a line: after its leading spaces and tabs, and
    after each list or quote marker that follows them."""
    at = len(content) - len(content.lstrip(" \t"))
    found = [at]
    while marker := MARKER.match(content, at):
        at = marker.end()
        found.append(at)
    return found


def classify(content: str) -> Line:
    """The kind of a line: a title, a section, a requirement's or a scenario's heading, each
    as OpenSpec's template writes it; another line that starts with `#`, a fence's line, a
    line of `=` or `-` signs, each after any spaces, tabs or list or quote markers; or a
    line of text."""
    if content.startswith("# ") and js_trim(content[2:]):
        return Line("title", js_trim(content[2:]))
    if content.startswith("## ") and content[3:].rstrip(" \t")[:1] not in ("", " ", "\t"):
        return Line("section", content[3:].rstrip(" \t"))
    if content.startswith("### Requirement:") and content[16:17] in ("", " "):
        heading = js_trim(content[4:])
        rest = js_trim(heading[len("Requirement:") :])
        name = js_trim(without_closing_run(rest))
        # GitHub reads a rest of `#` signs alone as the heading's closing run, and shows
        # no name, where OpenSpec names the requirement by them.
        return Line("requirement", name, heading, bool(rest.strip("#")))
    if content.startswith("#### Scenario:") and content[14:15] in ("", " "):
        heading = js_trim(content[5:])
        name = js_trim(without_closing_run(heading)[len("Scenario:") :])
        return Line("scenario", name, heading, bool(name))
    found = starts(content)
    if content.startswith("#", found[-1]):
        return Line("hash")
    if content.startswith(("```", "~~~"), found[-1]):
        return Line("fence")
    # Where the signs, spaces and tabs that end the line begin.
    signs = len(content.rstrip("=- \t"))
    if any(signs <= at < len(content) for at in found):
        return Line("underline")
    return Line("text")


FLAGGED = {"hash": HASH, "fence": FENCE, "underline": UNDERLINE}


@dataclass
class ScenarioLines:
    line: int
    name: str
    lines: list[tuple[int, str, bool]] = field(default_factory=list)


@dataclass
class Block:
    """A requirement as it is read: its heading's line, operation, name and text, the
    lines between its heading and its first scenario, and its scenarios. Each line is
    kept with whether its form is still to be checked."""

    line: int
    operation: str
    name: str
    heading: str
    text: list[tuple[int, str, bool]] = field(default_factory=list)
    scenarios: list[ScenarioLines] = field(default_factory=list)


class Reader:
    """Reads a spec's lines in one pass, keeping the section, the requirement and the
    scenario that each is in, and the problems of their form by line."""

    def __init__(self, main: bool) -> None:
        self.main = main
        self.sections = MAIN_SECTIONS if main else CHANGE_SECTIONS
        self.problems: list[tuple[int, str]] = []
        self.section: str | None = None
        self.headed = False
        self.seen: set[str] = set()
        self.block: Block | None = None
        self.scenario: ScenarioLines | None = None
        self.names: set[str] = set()
        self.blocks: list[Block] = []
        self.renames: list[tuple[str, str]] = []
        self.pending: tuple[int, str] | None = None

    def problem(self, number: int, message: str) -> None:
        self.problems.append((number, message))

    def read(self, number: int, content: str) -> None:
        line = classify(content)
        if line.kind == "title":
            self.title(number, line.name)
        elif line.kind == "section":
            self.start_section(number, line.name)
        elif line.kind == "requirement":
            self.start_requirement(number, line)
        elif line.kind == "scenario":
            self.start_scenario(number, line)
        else:
            flag = FLAGGED.get(line.kind)
            if flag:
                self.problem(number, flag)
            self.text(number, content, not flag)

    def title(self, number: int, name: str) -> None:
        if self.headed:
            self.problem(number, "is a title after the spec's first heading")
        elif self.main and name.lower() == REQUIREMENTS.lower():
            self.problem(number, "is a title that OpenSpec reads as the Requirements section")
        self.headed = True

    def start_section(self, number: int, name: str) -> None:
        self.close_block()
        self.close_renames()
        self.headed = True
        self.section = UNREAD
        written = {section.lower(): section for section in self.sections}.get(name.lower())
        if written is None:
            kind = "a main spec" if self.main else "a change's spec"
            self.problem(number, f'is a section, "{name}", that OpenSpec does not read in {kind}')
        elif written != name:
            self.problem(
                number, f'gives the section "{written}" as "{name}", not as its template writes it'
            )
        elif name in self.seen and (self.main or name == PURPOSE):
            self.problem(number, f'gives the section "{name}" a second time')
        else:
            self.seen.add(name)
            self.section = name

    def start_requirement(self, number: int, line: Line) -> None:
        self.headed = True
        if self.section in OPERATIONS:
            self.close_block()
            self.block = Block(number, OPERATIONS[self.section], line.name, line.heading)
            if not line.named:
                self.problem(number, "is a requirement's heading without a name")
        elif self.section != UNREAD:
            self.problem(
                number, "is a requirement's heading outside a section that gives requirements"
            )

    def start_scenario(self, number: int, line: Line) -> None:
        self.headed = True
        if self.block is None:
            if self.section != UNREAD:
                self.problem(number, "is a scenario's heading outside a requirement")
            return
        self.close_scenario()
        if not line.named:
            self.problem(number, "is a scenario's heading without a name")
        elif line.name in self.names:
            self.problem(
                number,
                f'gives a scenario the name "{line.name}", which another scenario of the spec has',
            )
        self.names.add(line.name)
        self.scenario = ScenarioLines(number, line.name)
        self.block.scenarios.append(self.scenario)

    def text(self, number: int, content: str, unchecked: bool) -> None:
        blank = not js_trim(content)
        if self.section in OPERATIONS:
            if self.scenario is not None:
                self.scenario.lines.append((number, content, unchecked))
            elif self.block is not None:
                self.block.text.append((number, content, unchecked))
            elif unchecked and not blank:
                self.problem(number, BEFORE)
        elif self.section == RENAMED and unchecked and not blank:
            self.rename(number, content)
        elif self.section is None and unchecked and not blank:
            self.problem(number, FIRST_SECTION)

    def rename(self, number: int, content: str) -> None:
        side, name = rename_of(content)
        if side == "FROM":
            self.close_renames()
            self.pending = (number, name)
        elif side == "TO" and self.pending is not None:
            self.renames.append((self.pending[1], name))
            self.pending = None
        elif side == "TO":
            self.problem(number, "is a TO: line with no FROM: line before it")
        else:
            self.problem(number, NOT_RENAME)

    def close_renames(self) -> None:
        if self.pending is not None:
            self.problem(self.pending[0], "is a FROM: line with no TO: line after it")
            self.pending = None

    def close_scenario(self) -> None:
        scenario, self.scenario = self.scenario, None
        if scenario is None or self.block is None:
            return
        of = f'scenario "{scenario.name}" of requirement "{self.block.name}"'
        when = then = False
        # A THEN line before any WHEN line, named once a WHEN line follows it; with none,
        # the scenario has no WHEN line.
        early: int | None = None
        for number, content, unchecked in scenario.lines:
            if not unchecked or not js_trim(content):
                continue
            if content.startswith(WHEN):
                if when:
                    self.problem(number, f"{of} gives a second WHEN line")
                elif early is not None:
                    self.problem(early, f"{of} gives its THEN line before its WHEN line")
                when = True
            elif content.startswith(THEN):
                if then:
                    self.problem(number, f"{of} gives a second THEN line")
                elif not when:
                    early = number
                then = True
            elif content.startswith(AND):
                if not when and not then:
                    self.problem(number, f"{of} gives an AND line before its WHEN line")
            else:
                self.problem(number, f"{of} holds a line other than a WHEN, a THEN or an AND line")
        if not when:
            self.problem(scenario.line, f"{of} has no WHEN line")
        if not then:
            self.problem(scenario.line, f"{of} has no THEN line")

    def close_block(self) -> None:
        self.close_scenario()
        block, self.block = self.block, None
        if block is None:
            return
        named = f'requirement "{block.name}"'
        lines = [(number, js_trim(content), unchecked) for number, content, unchecked in block.text]
        lines = [line for line in lines if line[1]]
        for number, content, unchecked in lines:
            if unchecked and content.startswith((WHEN, THEN, AND)):
                self.problem(number, f"{named} holds a scenario's line in its text")
        if block.operation in READ_FOR_TEXT:
            own = "\n".join(content for _, content, _ in lines)
            if not SHALL_OR_MUST.search(own):
                self.problem(block.line, f"{named} holds neither SHALL nor MUST in its text")
            if len(own) > LONGEST:
                self.problem(
                    block.line, f"{named} has {len(own)} characters of text, more than {LONGEST}"
                )
            for number, content, unchecked in lines:
                if unchecked and LABEL.match(content):
                    self.problem(
                        number, f"{named} holds a line that starts with a bold label and a colon"
                    )
            if not block.scenarios:
                self.problem(block.line, f"{named} has no scenario")
        self.blocks.append(block)

    def close(self) -> None:
        self.close_block()
        self.close_renames()

    def requirements(self) -> list[Requirement]:
        """The requirements as OpenSpec shows them: a main spec's in their order, and a
        change's added, modified and removed requirements, each in their order, then its
        renames."""
        found = [requirement_of(block) for block in self.blocks]
        if self.main:
            return found
        order = ("ADDED", "MODIFIED", "REMOVED")
        found.sort(key=lambda requirement: order.index(requirement.operation))
        renamed = [Requirement("RENAMED", old, "", (), new) for old, new in self.renames]
        return found + renamed


def rename_of(content: str) -> tuple[str, str]:
    """The side and the name of a rename's line in OpenSpec's template, or empty ones."""
    end = content.rstrip(" \t")
    for side in ("FROM", "TO"):
        start = f"- {side}: `### Requirement: "
        if content.startswith(start) and end.endswith("`") and len(end) > len(start):
            name = js_trim(without_closing_run(end[len(start) : -1]))
            if name:
                return side, name
    return "", ""


def requirement_of(block: Block) -> Requirement:
    """A requirement as OpenSpec shows it: its text is its lines that are not blank, each
    trimmed, leaving out label lines when others remain, or else its heading's text; and
    a scenario is one whose lines are not all blank."""
    captured: list[str] = []
    labels: list[str] = []
    for _, content, _ in block.text:
        trimmed = js_trim(content)
        if trimmed:
            (labels if LABEL.match(trimmed) else captured).append(trimmed)
    text = "\n".join(captured) or "\n".join(labels) or block.heading
    scenarios = tuple(
        Scenario(scenario.name, body)
        for scenario in block.scenarios
        if (body := js_trim("\n".join(content for _, content, _ in scenario.lines)))
    )
    return Requirement(block.operation, block.name, text, scenarios)


def read_spec(root: Path, spec: Spec) -> tuple[list[Requirement], list[str]]:
    """The spec's requirements as OpenSpec reads them, in the order that it shows them,
    and the spec's problems, each naming its line."""
    text, problems = plain_text((root / spec.path).read_bytes())
    if text is None:
        requirements: list[Requirement] = []
    else:
        reader = Reader(main=not spec.change)
        # OpenSpec reads a spec's lines after a byte-order mark, which plain_text reports.
        for number, content in enumerate(text.removeprefix("\ufeff").split("\n"), 1):
            reader.read(number, content)
        reader.close()
        problems += reader.problems
        requirements = reader.requirements()
    problems.sort(key=lambda problem: problem[0])
    return requirements, [shown(f"{spec.path}:{number}: {message}") for number, message in problems]


def read_all(root: Path) -> tuple[Reading, list[str]]:
    """The reading of every spec below `root`, and every problem of their form, with one
    when the test reads no spec, no requirement or no scenario."""
    specs, problems = find_specs(root)
    readings: dict[tuple[str, str], tuple[Requirement, ...]] = {}
    for spec in specs:
        requirements, found = read_spec(root, spec)
        readings[(spec.change, spec.ident)] = tuple(requirements)
        problems += found
    read = [
        requirement
        for requirements in readings.values()
        for requirement in requirements
        if requirement.operation in READ_FOR_TEXT
    ]
    if not specs:
        problems.append(NO_SPEC)
    elif not read:
        problems.append(NO_REQUIREMENT)
    elif not any(requirement.scenarios for requirement in read):
        problems.append(NO_SCENARIO)
    return Reading(changes_in(root), readings), problems


def problems_in(root: Path) -> list[str]:
    """Every problem of the form of the specs below `root`."""
    return read_all(root)[1]


# The comparison with the pinned OpenSpec CLI (R178, DR-196).

# A call of the CLI with these arguments: its exit code, and what it printed to standard
# output and to standard error.
Run = Callable[[list[str]], tuple[int, str, str]]
T = TypeVar("T")
SHOWN = ("ADDED", "MODIFIED", "REMOVED")
FORM = "prints JSON in another form than the comparison reads"
NOTHING_COMPARED = "openspec/: the comparison compares no requirement"


def text_of(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("not text")
    return value


def objects(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(each, dict) for each in value):
        raise ValueError("not a list of objects")
    return value


def listed_specs(value: Any) -> list[str]:
    return [text_of(each["id"]) for each in objects(value["specs"])]


def listed_changes(value: Any) -> list[str]:
    return [text_of(each["name"]) for each in objects(value["changes"])]


def shown_requirement(value: Any, operation: str) -> Requirement:
    scenarios = tuple(
        Scenario(text_of(each["name"]), text_of(each["rawText"]))
        for each in objects(value["scenarios"])
    )
    return Requirement(operation, text_of(value["name"]), text_of(value["text"]), scenarios)


def shown_spec(value: Any) -> list[Requirement]:
    return [shown_requirement(each, "") for each in objects(value["requirements"])]


def shown_change(value: Any) -> list[tuple[str, Requirement]]:
    """Each requirement that a change gives, with the id of its spec, in the CLI's order.
    When no spec of a change gives a delta section, the CLI gives instead each bullet of
    its proposal's What Changes that starts with a name in bold as a delta with neither a
    requirement nor a rename, which reads no spec, so the change gives no requirement."""
    given = objects(value["deltas"])
    if not any("requirement" in delta or "rename" in delta for delta in given):
        return []
    deltas = []
    for delta in given:
        operation = delta["operation"]
        if operation == "RENAMED":
            rename = delta["rename"]
            old, new = text_of(rename["from"]), text_of(rename["to"])
            requirement = Requirement(operation, old, "", (), new)
        elif operation in SHOWN:
            requirement = shown_requirement(delta["requirement"], operation)
        else:
            raise ValueError("not an operation")
        deltas.append((text_of(delta["spec"]), requirement))
    return deltas


def said(out: str, err: str) -> str:
    """What the CLI said of a call that failed: the messages that it prints as JSON with
    `--json`, or else what it printed."""
    try:
        status = json.loads(out)["status"]
        messages = [
            each["message"]
            for each in status
            if isinstance(each, dict) and isinstance(each.get("message"), str)
        ]
    except (ValueError, KeyError, TypeError):
        messages = []
    return "; ".join(messages) or err.strip() or out.strip()


def asked(run: Run, args: list[str], read: Callable[[Any], T], problems: list[str]) -> T | None:
    """What the CLI prints for these arguments, as `read` reads its JSON, or None, with a
    problem that names the call, when the call fails or prints JSON in another form."""
    status, out, err = run(args)
    command = shown(" ".join(["openspec", *args]))
    if status:
        message = said(out, err)
        problems.append(
            f"{command}: exits with {status}" + (f": {shown(message)}" if message else "")
        )
        return None
    try:
        return read(json.loads(out))
    except (ValueError, KeyError, TypeError):
        problems.append(f"{command}: {FORM}")
        return None


def cli_reading(run: Run) -> tuple[Reading, list[str]]:
    """The specs and the changes that the CLI lists, and the requirements that it shows of
    each, with a problem for each call that fails or prints JSON in another form."""
    problems: list[str] = []
    specs: dict[tuple[str, str], list[Requirement]] = {}
    for ident in asked(run, ["list", "--specs", "--json"], listed_specs, problems) or []:
        args = ["show", "--type", "spec", "--json", "--", ident]
        requirements = asked(run, args, shown_spec, problems)
        if requirements is not None:
            specs[("", ident)] = requirements
    changes = asked(run, ["list", "--json", "--sort", "name"], listed_changes, problems) or []
    for change in changes:
        args = ["show", "--type", "change", "--json", "--deltas-only", "--", change]
        for ident, requirement in asked(run, args, shown_change, problems) or []:
            specs.setdefault((change, ident), []).append(requirement)
    reading = Reading(frozenset(changes), {key: tuple(value) for key, value in specs.items()})
    return reading, problems


def spec_path(change: str, ident: str) -> str:
    folder = f"{CHANGES}/{change}/specs" if change else f"{OPENSPEC}/specs"
    return shown(f"{folder}/{ident}/spec.md")


def quoted(value: object) -> str:
    return f'"{shown(value)}"' if isinstance(value, str) else str(value)


def fields(ours: Requirement, theirs: Requirement) -> Iterator[tuple[str, object, object]]:
    """The fields of two requirements, in the order in which a difference is looked for."""
    yield "operation", ours.operation, theirs.operation
    yield "name", ours.name, theirs.name
    yield "text", ours.text, theirs.text
    yield "new name", ours.renamed_to, theirs.renamed_to
    yield "number of scenarios", len(ours.scenarios), len(theirs.scenarios)
    for number, (mine, its) in enumerate(zip(ours.scenarios, theirs.scenarios, strict=False), 1):
        yield f"scenario {number}'s name", mine.name, its.name
        yield f"scenario {number}'s lines", mine.text, its.text


def first_difference(ours: tuple[Requirement, ...], theirs: tuple[Requirement, ...]) -> str:
    for number, (mine, its) in enumerate(zip(ours, theirs, strict=False), 1):
        for label, one, other in fields(mine, its):
            if one != other:
                return (
                    f"requirement {number}, {quoted(mine.name)}, differs in its {label}: the test"
                    f" reads {quoted(one)}, and OpenSpec shows {quoted(other)}"
                )
    if len(ours) != len(theirs):
        return f"the test reads {len(ours)} requirements, and OpenSpec shows {len(theirs)}"
    return ""


def differences(ours: Reading, theirs: Reading) -> list[str]:
    """Each change or spec that only one reading gives, and the first difference in the
    requirements of each spec that both give, with one when no requirement was compared.
    The CLI shows a change's specs only by their requirements, so a change's spec from
    which the test reads no requirement is one that only the test's reading gives."""
    found = [
        f"{CHANGES}/{shown(change)}: the test reads it as a change, and OpenSpec does not"
        for change in sorted(ours.changes - theirs.changes)
    ] + [
        f"{CHANGES}/{shown(change)}: OpenSpec reads it as a change, and the test does not"
        for change in sorted(theirs.changes - ours.changes)
    ]
    mine, its = ours.specs, theirs.specs
    compared = 0
    for key in sorted(mine.keys() | its.keys()):
        path = spec_path(*key)
        if key not in its:
            found.append(f"{path}: the test reads it, and OpenSpec does not")
        elif key not in mine:
            found.append(f"{path}: OpenSpec reads it, and the test does not")
        else:
            compared += min(len(mine[key]), len(its[key]))
            difference = first_difference(mine[key], its[key])
            if difference:
                found.append(f"{path}: {difference}")
    if not compared:
        found.append(NOTHING_COMPARED)
    return found


def main(argv: list[str]) -> int:
    """Compares the test's reading of the specs below the current folder with what the
    OpenSpec CLI at the path given lists and shows, printing each problem of the CLI's
    reading, or else each difference: 0 when they agree, 1 when they do not, and 2 when
    the CLI does not run."""
    if len(argv) != 1:
        print("verify-openspec: usage: python3 scripts/spec_form.py <openspec>", file=sys.stderr)
        return 2
    cli = argv[0]

    def run(args: list[str]) -> tuple[int, str, str]:
        done = subprocess.run(
            [cli, *args], capture_output=True, encoding="utf-8", errors="replace", check=False
        )
        return done.returncode, done.stdout, done.stderr

    try:
        theirs, found = cli_reading(run)
    except OSError as error:
        print(f"verify-openspec: {shown(cli)} does not run: {shown(str(error))}", file=sys.stderr)
        return 2
    found = found or differences(read_all(Path.cwd())[0], theirs)
    for each in found:
        print(f"verify-openspec: {each}", file=sys.stderr)
    if found:
        return 1
    print(f"verify-openspec: {sum(map(len, theirs.specs.values()))} requirement(s) read alike")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
