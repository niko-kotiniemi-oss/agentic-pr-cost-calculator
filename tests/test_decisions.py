"""Each decision has a record of its own, and the records hold together.

`docs/decisions/` keeps one record for each decision about what the tool is,
how it works and how it is built, so that each decision can be reversed or
replaced on its own. A record holds one choice. Its fields say what kind of
decision it is, whether it still holds, who made it, and which requirements,
threats and other records it touches; its sections say why it was made, what
else was considered, what follows from it, what it covers, and what reversing
it would change. `docs/decisions/README.md` is the index.

These tests hold what a machine can check:

- every record has its fields and its sections, each once, in order, none of
  them empty, and no other line that starts with `#`; its type, status and
  decider take a form from their lists, and a date that it gives is a real one,
  no later than today; its file name and heading carry its number, in ASCII
  digits padded to three; and it holds plain text: printable ASCII and line
  breaks, with no fenced block, no `<`, `][` or table outside inline code, no
  web address or link reference definition, and no link but from a record's ID
  to that record's file;
- the records' folder holds the records and their index and nothing else, no
  link among them, no file elsewhere is named as a record, and the numbers run
  from DR-001 without a gap or a repeat;
- the index lists every record once, in order, as the record itself has it,
  and every line of its table, which runs to its first blank line, is a row
  that it reads;
- every requirement and threat that a record lists is held or retired, a
  closed record and the record that closed it name each other, and an accepted
  record does not rest only on retired requirements;
- every record and design decision that a tracked file outside `vendor/` and
  `tests/` names exists, a parenthesis right after a record's ID gives that
  record's title, and only the records, the index, the changelog and archived
  changes name a closed one;
- every requirement, threat, change and task that such a file names, if it is
  Markdown, exists, a requirement or a threat held or retired;
- each threat that an accepted record lists names that record in its Held by
  line, and a threat that names a new record there is listed in it;
- no attribute of the repository's changes how git or GitHub shows a record's
  diff;
- a record that the default branch holds is never removed, and never changed
  except to be closed, after which any line of text under its sections may
  become `[removed]`; an ID that the default branch's register, threat model
  or assumptions' index holds stays held or retired, an ID counting as retired
  only where the section "Retired IDs" lists it; and a requirement's or a
  scenario's title that the default branch's specs hold and an accepted record
  quotes stays in the specs, which are `openspec/specs/` and the active changes,
  a title under "REMOVED Requirements" counting as gone, since the record keeps
  its quote and the wording test keeps such a title's words.

Whether a record holds one choice, describes rather than instructs, and says
what its sources say is for the review to check.

The comparison with the default branch compares git trees, not the working
tree, so a change counts once it is committed. It compares with where HEAD left
`refs/remotes/origin/main` and, in CI, with the base commit that the workflow
names in `BASE_COMMIT` too, since a pull request's base is whichever branch its
author chose. By design, the comparison skips while no base holds the records'
folder, which is the case until the first records reach the default branch,
and fails when a base holds that folder and no file in it that these tests name
a record.
"""

from __future__ import annotations

import os
import posixpath
import re
import subprocess
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import pytest
from test_roadmap import session_free_environment
from wording import ACCEPTED, DEFAULT_BRANCH, QUOTATION, SPEC_FILE, SPEC_TITLE

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = Path("docs") / "decisions"
REMOVED = "[removed]"

FIELDS = ("Type", "Status", "Decided by", "Requirements", "Threats", "Replaces", "Closed by")
SECTIONS = (
    "Context",
    "Decision",
    "Alternatives",
    "Consequences",
    "Scope",
    "What reversing it would change",
)
TYPES = {"scope", "architecture", "technical", "security and privacy", "process"}
STATUSES = {"accepted", "closed"}
INDEX_CELLS = ("title", "Type", "Status", "Decided by", "Requirements", "Threats")
INDEX_TABLE = (
    "| Record | Decision | Type | Status | Decided by | Requirements | Threats |",
    "|---|---|---|---|---|---|---|",
)
# Files whose mentions are not read: upstream's own, and the synthetic ones tests plant.
UNREAD = ("vendor/", "tests/")

# A record's number, in ASCII digits, padded to three and no further.
NUMBER = r"(?:00[1-9]|0[1-9][0-9]|[1-9][0-9]{2,})"
WORDS = r"[a-z0-9]+(?:-[a-z0-9]+)*"
FILE_NAME = re.compile(rf"DR-({NUMBER})-{WORDS}\.md")
# Files that keep history, and so may name a closed record: the records, their index, the
# changelog and the archived changes.
HISTORY = re.compile(
    rf"docs/decisions/(?:README|DR-{NUMBER}-{WORDS})\.md|CHANGELOG\.md"
    r"|openspec/changes/archive/[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+/.+"
)
HEADING = re.compile(rf"# (DR-{NUMBER}): ([^|\n]*[^|\s])\n")
FIELD = re.compile(r"- \*\*([^*]+):\*\* (\S.*)")
SECTION = re.compile(r"^## (.+)\n", re.M)
DATE = r"\d{4}-\d{2}-\d{2}"
DATES = rf"{DATE}(?:(?:, {DATE})*,? and {DATE})?"
DECIDER = re.compile(
    rf"the owner, (?P<owner>{DATES})"
    rf"|the change `(?P<change>[a-z0-9-]+)`(?:, as the owner asked on (?P<asked>{DATES}))?"
)
LISTS = {
    "Requirements": re.compile(r"R\d+(?:, R\d+)*"),
    "Threats": re.compile(r"T\d+(?:, T\d+)*"),
    "Replaces": re.compile(rf"DR-{NUMBER}(?:, DR-{NUMBER})*"),
    "Closed by": re.compile(rf"DR-{NUMBER}"),
}
INDEX_ROW = re.compile(rf"\| \[(DR-{NUMBER})\]\(([^)\s]+)\) \|(.*)\|[ ]*")
LINK = re.compile(r"\]\(([^)]*)\)")
ID_LINK = re.compile(rf"\[(DR-{NUMBER})\]\(([^)]*)\)")
# Inline code on one line, which Markdown shows as written, so a placeholder there is not HTML.
CODE_SPAN = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
REGISTER_ID = re.compile(r"^\| (R\d+) \|", re.M)
RETIRED_ID = re.compile(r"^- (R\d+), removed by `", re.M)
THREAT_HEADING = re.compile(r"^### (T\d+)\. ", re.M)
RETIRED_THREAT = re.compile(r"^- (T\d+), removed by `", re.M)
INDEX_ID = re.compile(r"^- \*\*(A\d+)\.\*\* ", re.M)
RETIRED_ASSUMPTION = re.compile(r"^- (A\d+), removed by `", re.M)
RETIRED_SECTION = re.compile(r"^## Retired IDs\n(.*?)(?=^## |\Z)", re.M | re.S)
RETIRED_ENTRY = re.compile(r"^- [RT]\d+, removed by `([a-z0-9-]+)`", re.M)
REQUIREMENT_MENTION = re.compile(r"\bR\d+\b")
THREAT_MENTION = re.compile(r"\bT\d+\b")
CHANGE_MENTION = re.compile(r"\b[Tt]he change `([a-z0-9-]+)`")
THREAT_BLOCK = re.compile(r"^### (T\d+)\. .*?(?=^#{1,3} |\Z)", re.M | re.S)
HELD_BY = re.compile(r"^- \*\*Held by:\*\* (.*)$", re.M)
ARCHIVE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
OWN_CHANGE = re.compile(r"^openspec/changes/(?:archive/\d{4}-\d{2}-\d{2}-)?([a-z0-9-]+)/")
DESIGN_HEADING = re.compile(r"^### (\d+)\. ", re.M)
NUMBERS = r"\d+(?:(?:,? and |, )\d+)*"
RECORD_MENTION = re.compile(r"\bDR-(\d{3,})\b")
TITLED_MENTION = re.compile(r"\bDR-(\d{3,}) \(([^)]*)\)")
DECISION_MENTION = re.compile(
    rf"\b(?:([Dd]esign)(?:'s)? )?[Dd]ecisions? ({NUMBERS})(?: of `([a-z0-9-]+)`)?(?!\.\d)"
)
CHANGE_DECISION = re.compile(rf"`([a-z0-9-]+)` decisions? ({NUMBERS})")
CLOSER = re.compile(rf"^- \*\*Closed by:\*\* (DR-{NUMBER})$", re.M)
COMMIT_ID = re.compile(r"[0-9a-f]{40}")
TASK_NUMBERS = r"[0-9]+\.[0-9]+(?:(?:,? and |,? or |, | to )[0-9]+\.[0-9]+)*"
TASK_MENTION = re.compile(rf"\b[Tt]asks? ({TASK_NUMBERS})(?: of `([a-z0-9-]+)`)?")
CHANGE_TASK = re.compile(rf"`([a-z0-9-]+)` tasks? ({TASK_NUMBERS})")
TASK_LINE = re.compile(r"^- \[[ x]\] ([0-9]+\.[0-9]+) ", re.M)
# Which specs, titles, quotations and records count is `scripts/wording.py`'s, so that this
# check and the wording test agree on the titles that the records keep.
REMOVED_SECTION = re.compile(r"^## REMOVED Requirements\s*$.*?(?=^## |\Z)", re.M | re.S)
# What makes git or GitHub show a file's diff otherwise: git's `diff`, the `binary` macro
# that unsets it, and `linguist-generated`, with which GitHub hides a diff by default.
DIFF_ATTRIBUTES = {"binary", "diff", "linguist-generated"}


def number(ident: str) -> int:
    return int(re.sub(r"\D", "", ident))


@dataclass(frozen=True)
class Record:
    ident: str
    file: str
    title: str
    fields: dict[str, str]
    text: str

    def listed(self, field: str) -> list[str]:
        value = self.fields.get(field, "none")
        return [] if value == "none" else value.split(", ")


def read(path: Path) -> tuple[Record | None, list[str]]:
    """The record a file holds, and what is wrong with its form."""
    name = path.name
    named = FILE_NAME.fullmatch(name)
    if not named:
        return None, [f"{name} is not named DR-NNN-<words>.md"]
    text = path.read_text(encoding="utf-8")
    heading = HEADING.match(text)
    if not heading:
        return None, [f"{name} does not open with its heading, '# DR-NNN: <title>'"]
    ident = f"DR-{named.group(1)}"
    problems = content_problems(name, text)
    if "|" in CODE_SPAN.sub("", text):
        problems.append(f"{name} holds | outside inline code, with which Markdown makes a table")
    problems += [
        f"{name} has a line that starts with # and is not a section's heading: {line!r}"
        for line in text.split("\n")[1:]
        if line.lstrip().startswith("#") and not SECTION.fullmatch(f"{line}\n")
    ]
    if heading.group(1) != ident:
        problems.append(f"{name} is headed {heading.group(1)}, not the number in its name")
    body = text[heading.end() :]
    first = SECTION.search(body)
    head, rest = (body[: first.start()], body[first.start() :]) if first else (body, "")
    fields: dict[str, str] = {}
    order: list[str] = []
    for line in head.splitlines():
        if not line.strip():
            continue
        field = FIELD.fullmatch(line)
        if field is None:
            problems.append(f"{name} has a line among its fields that is not a field: {line!r}")
            continue
        order.append(field.group(1))
        fields[field.group(1)] = field.group(2)
    if tuple(order) != FIELDS:
        problems.append(f"{name} has the fields {order}, not {list(FIELDS)}")
    parts = SECTION.split(rest)
    titles = parts[1::2]
    if tuple(titles) != SECTIONS:
        problems.append(f"{name} has the sections {titles}, not {list(SECTIONS)}")
    problems += [
        f"{name} says nothing under {title!r}"
        for title, content in zip(titles, parts[2::2], strict=True)
        if not content.strip()
    ]
    problems += field_problems(name, fields)
    return Record(ident, name, heading.group(2), fields, text), problems


def content_problems(name: str, text: str) -> list[str]:
    """A record and the index hold plain text, which reads the same to a reviewer and to an
    agent: printable ASCII and line breaks, with no fenced block, no `<` or `][` outside
    inline code, no web address or link reference definition, and no link but from a
    record's ID to its file."""
    problems = []
    others = sorted({ord(c) for c in text if c != "\n" and not " " <= c <= "~"})
    if others:
        codes = ", ".join(f"U+{code:04X}" for code in others)
        problems.append(
            f"{name} holds characters other than printable ASCII and line breaks: {codes}"
        )
    for mark, what in (
        ("&", "&, with which Markdown writes a character by its code"),
        ("\\", "a backslash, with which Markdown undoes what a mark does"),
        ("@", "@, which GitHub turns into a link or a mention"),
        ("]:", "a link reference definition"),
    ):
        if mark in text:
            problems.append(f"{name} holds {what}")
    if "```" in text or "~~~" in text:
        problems.append(f"{name} holds a fenced block")
    plain = CODE_SPAN.sub("", text)
    if "<" in plain:
        problems.append(f"{name} holds <, with which Markdown starts HTML or a link")
    if "][" in plain:
        problems.append(f"{name} holds ][, with which Markdown links by reference")
    if "://" in text or "www." in text.lower():
        problems.append(f"{name} holds a web address")
    problems += [
        f"{name} links to {target}, which is not a record"
        for target in LINK.findall(text)
        if not FILE_NAME.fullmatch(target)
    ]
    problems += [
        f"{name} links {label} to {target}, which is not {label}'s file"
        for label, target in ID_LINK.findall(text)
        if (named := FILE_NAME.fullmatch(target)) and f"DR-{named.group(1)}" != label
    ]
    problems += [
        f"{name} links to {target} from text other than a record's ID"
        for target in LINK.findall(ID_LINK.sub("", text))
    ]
    return problems


def field_problems(name: str, fields: dict[str, str]) -> list[str]:
    problems = []
    if fields.get("Type", "scope") not in TYPES:
        problems.append(f"{name} has a type outside the list: {fields['Type']!r}")
    if fields.get("Status", "accepted") not in STATUSES:
        problems.append(f"{name} has a status outside the list: {fields['Status']!r}")
    for field, form in LISTS.items():
        value = fields.get(field, "none")
        if value == "none":
            continue
        if not form.fullmatch(value):
            problems.append(f"{name} has {field} that is neither none nor a list of IDs: {value!r}")
            continue
        numbers = [number(item) for item in value.split(", ")]
        if numbers != sorted(set(numbers)):
            problems.append(f"{name} lists its {field} out of order or twice: {value}")
    return problems


def change_folders(root: Path) -> dict[str, Path]:
    """Each change's folder, active or archived, by the change's name."""
    base = root / "openspec" / "changes"
    folders = [*base.glob("*"), *(base / "archive").glob("*")]
    return {
        ARCHIVE_DATE.sub("", folder.name): folder
        for folder in folders
        if folder.is_dir() and folder.name != "archive"
    }


def task_numbers(root: Path) -> dict[str, set[str]]:
    """The numbered tasks of each change, by change."""
    return {
        change: set(TASK_LINE.findall((folder / "tasks.md").read_text(encoding="utf-8")))
        for change, folder in change_folders(root).items()
        if (folder / "tasks.md").is_file()
    }


def decider_problems(record: Record, changes: set[str]) -> list[str]:
    decider = record.fields.get("Decided by")
    if decider is None:
        return []
    match = DECIDER.fullmatch(decider)
    if not match:
        return [f"{record.ident} is decided by {decider!r}, which is not a form from the list"]
    problems = []
    today = datetime.now(UTC).date()
    for day in re.findall(DATE, decider):
        try:
            given = date.fromisoformat(day)
        except ValueError:
            problems.append(f"{record.ident} gives {day}, which is not a date")
            continue
        if given > today:
            problems.append(f"{record.ident} gives {day}, which is later than today")
    change = match.group("change")
    if change and change not in changes:
        problems.append(
            f"{record.ident} is decided by `{change}`, which is not a change in this repository"
        )
    return problems


def retired_in(text: str, entry: re.Pattern[str]) -> set[str]:
    """The IDs that a document's section "Retired IDs" lists, and only that section."""
    section = RETIRED_SECTION.search(text)
    return set(entry.findall(section.group(1))) if section else set()


def known_ids(root: Path) -> tuple[set[str], set[str]]:
    """The requirement IDs that the register holds or retires, and the threat IDs that the
    threat model holds or retires."""
    register = (root / "docs" / "requirements.md").read_text(encoding="utf-8")
    model = (root / "docs" / "threat-model.md").read_text(encoding="utf-8")
    return (
        set(REGISTER_ID.findall(register)) | retired_in(register, RETIRED_ID),
        set(THREAT_HEADING.findall(model)) | retired_in(model, RETIRED_THREAT),
    )


def citation_problems(records: dict[str, Record], root: Path) -> list[str]:
    register = (root / "docs" / "requirements.md").read_text(encoding="utf-8")
    retired = retired_in(register, RETIRED_ID)
    requirement_ids, threat_ids = known_ids(root)
    changes = set(change_folders(root))
    problems = []
    for record in records.values():
        problems += decider_problems(record, changes)
        requirements = record.listed("Requirements")
        problems += [
            f"{record.ident} cites {ident}, which the register does not hold"
            for ident in requirements
            if ident not in requirement_ids
        ]
        if (
            record.fields.get("Status") == "accepted"
            and requirements
            and set(requirements) <= retired
        ):
            problems.append(
                f"{record.ident} is accepted and every requirement it cites is retired,"
                " so the change that retired them closes it"
            )
        problems += [
            f"{record.ident} cites {ident}, which the threat model does not hold"
            for ident in record.listed("Threats")
            if ident not in threat_ids
        ]
        problems += [
            f"{record.ident} names {other} in {field}, which is not a record"
            for field in ("Replaces", "Closed by")
            for other in record.listed(field)
            if other not in records
        ]
    return problems


def closure_problems(records: dict[str, Record]) -> list[str]:
    problems = []
    for record in records.values():
        status = record.fields.get("Status")
        closers = record.listed("Closed by")
        if status == "accepted" and closers:
            problems.append(f"{record.ident} is accepted and yet names {closers[0]} in Closed by")
        if status == "closed" and not closers:
            problems.append(f"{record.ident} is closed and names no record in Closed by")
        for field, others in (("Closed by", closers), ("Replaces", record.listed("Replaces"))):
            if record.ident in others:
                problems.append(f"{record.ident} names itself in {field}")
        for closer in closers:
            if closer in records and record.ident not in records[closer].listed("Replaces"):
                problems.append(
                    f"{record.ident} is closed by {closer}, which does not name it in Replaces"
                )
        for replaced in record.listed("Replaces"):
            if replaced in records and records[replaced].listed("Closed by") != [record.ident]:
                problems.append(
                    f"{record.ident} replaces {replaced}, which does not name {record.ident}"
                    " in Closed by"
                )
    return problems


def index_problems(index: Path, records: dict[str, Record]) -> list[str]:
    if not index.is_file():
        return ["the decisions folder has no index"]
    text = index.read_text(encoding="utf-8")
    problems = content_problems(index.name, text)
    lines = text.split("\n")
    # The table runs from its first line to the first blank one: Markdown shows any line in
    # between as a row, with a pipe or without.
    start = next((i for i, line in enumerate(lines) if "|" in line), len(lines))
    end = next((i for i in range(start, len(lines)) if not lines[i].strip()), len(lines))
    table = lines[start:end]
    if tuple(table[:2]) != INDEX_TABLE:
        problems.append("the index's table does not open with its header")
    rows = []
    for line in table[2:]:
        found = INDEX_ROW.fullmatch(line)
        if found is None:
            problems.append(f"the index has a line that is not a row: {line!r}")
        else:
            rows.append(found.groups())
    problems += [
        f"the index has a line that is not a row: {line!r}" for line in lines[end:] if "|" in line
    ]
    listed = [ident for ident, _link, _cells in rows]
    if listed != sorted(listed, key=number):
        problems.append("the index does not list the records in order")
    problems += [
        f"the index lists {ident} twice" for ident in sorted(set(listed)) if listed.count(ident) > 1
    ]
    for ident, link, cells in rows:
        record = records.get(ident)
        if record is None:
            problems.append(f"the index lists {ident}, which has no record")
            continue
        if link != record.file:
            problems.append(f"the index links {ident} to {link}, not to {record.file}")
        values = [cell.strip() for cell in cells.split("|")]
        expected = [record.title] + [record.fields.get(name, "") for name in INDEX_CELLS[1:]]
        if len(values) != len(expected):
            problems.append(f"the index row for {ident} does not have {len(expected)} cells")
            continue
        differ = [
            name
            for name, value, want in zip(INDEX_CELLS, values, expected, strict=True)
            if value != want
        ]
        if differ:
            problems.append(f"the index row for {ident} differs from the record in {differ}")
    problems += [f"{ident} is not in the index" for ident in sorted(records) if ident not in listed]
    return problems


def records_of(folder: Path) -> tuple[dict[str, Record], list[str]]:
    records: dict[str, Record] = {}
    problems: list[str] = []
    for path in sorted(folder.iterdir()):
        if path.is_symlink():
            problems.append(f"{path.name} is a link, and the records' folder holds only files")
            continue
        if path.is_dir():
            problems.append(
                f"{path.name} is a folder, and the records' folder holds only records"
                " and their index"
            )
            continue
        if path.name == "README.md":
            continue
        record, found = read(path)
        problems += found
        if record is None:
            continue
        if record.ident in records:
            problems.append(f"{record.ident} is the number of more than one record")
            continue
        records[record.ident] = record
    return records, problems


def problems_in(folder: Path, root: Path) -> tuple[list[str], int]:
    """What is wrong with the records in a folder and with their index, and how many it holds."""
    records, problems = records_of(folder)
    if not records:
        return [*problems, "no decision record found"], 0
    present = {number(ident) for ident in records}
    missing = sorted(set(range(1, max(present) + 1)) - present)
    if missing:
        names = ", ".join(f"DR-{each:03d}" for each in missing)
        problems.append(f"the records are not numbered from DR-001 without a gap: {names} missing")
    files = {record.file for record in records.values()}
    problems += [
        f"{record.file} links to {target}, which is no record's file"
        for record in records.values()
        for target in LINK.findall(record.text)
        if FILE_NAME.fullmatch(target) and target not in files
    ]
    problems += citation_problems(records, root)
    problems += closure_problems(records)
    problems += index_problems(folder / "README.md", records)
    return problems, len(records)


def design_numbers(root: Path) -> dict[str, set[int]]:
    """The numbered decisions of each change's design, by change."""
    return {
        change: {
            int(each)
            for each in DESIGN_HEADING.findall((folder / "design.md").read_text(encoding="utf-8"))
        }
        for change, folder in change_folders(root).items()
        if (folder / "design.md").is_file()
    }


def prose_problems(
    path: str,
    text: str,
    known: tuple[set[str], set[str]],
    changes: set[str],
    tasks: dict[str, set[str]],
) -> list[str]:
    """The requirements and threats that a text names and that are neither held nor
    retired, and the changes and tasks that it names and that do not exist."""
    problems = []
    for mention, ids, holder in (
        (REQUIREMENT_MENTION, known[0], "the register"),
        (THREAT_MENTION, known[1], "the threat model"),
    ):
        problems += [
            f"{path} names {ident}, which {holder} neither holds nor retires"
            for ident in sorted(set(mention.findall(text)), key=number)
            if ident not in ids
        ]
    problems += [
        f"{path} names the change `{change}`, which is not one"
        for change in sorted(set(CHANGE_MENTION.findall(text) + RETIRED_ENTRY.findall(text)))
        if change not in changes
    ]
    named = [(change, numbers) for numbers, change in TASK_MENTION.findall(text)]
    for change, numbers in named + CHANGE_TASK.findall(text):
        scope = [change] if change else sorted(tasks)
        for each in re.findall(r"[0-9]+\.[0-9]+", numbers):
            if not any(each in tasks.get(name, set()) for name in scope):
                where = f"`{change}`" if change else "any change"
                problems.append(f"{path} names task {each} of {where}, which is not one")
    return problems


def mention_problems(files: Mapping[str, str], records: dict[str, Record], root: Path) -> list[str]:
    """Every record and design decision that a file names exists, a parenthesis right after a
    record's ID gives that record's title, and a closed record is named only where history
    is kept. Every requirement, threat, change and task that a Markdown file names exists
    too, the requirements and threats held or retired: Markdown is where prose names them,
    while a data file can hold such a pattern by chance, as in a lock file's hashes."""
    designs = design_numbers(root)
    tasks = task_numbers(root)
    changes = set(change_folders(root))
    requirement_ids, threat_ids = known_ids(root)
    problems = []
    for path, text in sorted(files.items()):
        if path.endswith(".md"):
            problems += prose_problems(path, text, (requirement_ids, threat_ids), changes, tasks)
        for each in sorted(set(RECORD_MENTION.findall(text)), key=int):
            record = records.get(f"DR-{each}")
            if record is None:
                problems.append(f"{path} names DR-{each}, which is not a record")
            elif record.fields.get("Status") == "closed" and not HISTORY.fullmatch(path):
                problems.append(f"{path} names DR-{each}, which is closed")
        for each, given in TITLED_MENTION.findall(text):
            record = records.get(f"DR-{each}")
            if record is not None and " ".join(given.split()) != record.title:
                problems.append(
                    f'{path} names DR-{each} as "{given}", and its title is "{record.title}"'
                )
        own = OWN_CHANGE.match(path)
        in_design = own is not None and path.endswith("/design.md")
        cited = [
            (change or (own.group(1) if own else ""), numbers)
            for design, numbers, change in DECISION_MENTION.findall(text)
            if design or change or in_design
        ]
        cited += CHANGE_DECISION.findall(text)
        for change, numbers in cited:
            scope = [change] if change else sorted(designs)
            for each in re.findall(r"\d+", numbers):
                if not any(int(each) in designs.get(name, set()) for name in scope):
                    where = f"`{change}`" if change else "any change"
                    problems.append(f"{path} names decision {each} of {where}, which is not one")
    return problems


def tracked_texts(root: Path) -> dict[str, str]:
    listing = git(root, "ls-files", "-z")
    texts = {}
    for path in listing.stdout.decode("utf-8").split("\0"):
        if not path or path.startswith(UNREAD):
            continue
        try:
            texts[path] = (root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
    return texts


def git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    """git run in the repository at root, with no git variable of the session's and no
    global or system configuration."""
    return subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        check=False,
        env={**session_free_environment(), **GIT_ENVIRONMENT},
    )


def fetch_advice(root: Path, otherwise: str) -> str:
    """How to fetch what this clone lacks: all of its history when it is shallow."""
    shallow = git(root, "rev-parse", "--is-shallow-repository").stdout.decode().strip()
    return (
        "this clone is shallow, so run `git fetch --unshallow`" if shallow == "true" else otherwise
    )


def base_commits(root: Path, environ: Mapping[str, str]) -> list[str]:
    """The commits that this run compares with: the one CI names, if it names one, and
    where HEAD left the default branch. A pull request's base is the branch it was opened
    against, which its author chooses, so the default branch is compared with as well.

    Raises LookupError when a commit cannot be found, saying how to fetch it.
    """
    bases = []
    named = environ.get("BASE_COMMIT", "")
    if named:
        if not COMMIT_ID.fullmatch(named):
            raise LookupError(f"BASE_COMMIT is not a full commit ID: {named!r}")
        if git(root, "cat-file", "-e", f"{named}^{{commit}}").returncode != 0:
            advice = fetch_advice(root, f"run `git fetch origin {named}`")
            raise LookupError(f"the base commit {named} is not in this clone: {advice}")
        bases.append(named)
    lost = f"cannot find where HEAD left {DEFAULT_BRANCH}"
    # Resolved as written, so that a tag or a local branch of that name never stands in.
    branch = git(root, "show-ref", "--verify", "--hash", DEFAULT_BRANCH)
    if branch.returncode != 0:
        raise LookupError(
            f"{lost}: this clone does not have it, so run `git fetch origin main:{DEFAULT_BRANCH}`"
        )
    found = git(root, "merge-base", "HEAD", branch.stdout.decode().strip())
    if found.returncode != 0:
        raise LookupError(f"{lost}: {fetch_advice(root, 'they share no commit')}")
    left = found.stdout.decode().strip()
    return bases if left in bases else [*bases, left]


def records_in_tree(root: Path, commit: str) -> dict[str, tuple[str, str]]:
    """Every file in a commit whose name is a record's, wherever it is: its mode and
    object, by path."""
    listing = git(root, "ls-tree", "-r", "-z", "--full-tree", commit)
    if listing.returncode != 0:
        raise LookupError(f"cannot list the files of {commit}")
    found = {}
    for entry in listing.stdout.decode("utf-8", "surrogateescape").split("\0"):
        if not entry:
            continue
        meta, path = entry.split("\t", 1)
        mode, _kind, item = meta.split(" ")
        if FILE_NAME.fullmatch(path.rsplit("/", 1)[-1]):
            found[path] = (mode, item)
    return found


def content(root: Path, item: str) -> str:
    return git(root, "cat-file", "blob", item).stdout.decode("utf-8")


def closed_from(old: str, new: str) -> bool:
    """Whether `new` is `old` changed only as closing allows: its status from accepted
    to closed with the record that closed it named, and, once it is closed, lines of
    text under its sections replaced by [removed]."""
    closer = CLOSER.search(new)
    if closer is None:
        return False
    closed = old.replace("\n- **Status:** accepted\n", "\n- **Status:** closed\n", 1)
    closed = closed.replace("\n- **Closed by:** none\n", f"\n- **Closed by:** {closer[1]}\n", 1)
    before, after = closed.split("\n"), new.split("\n")
    # The heading and the fields come before the first section, and never become [removed].
    first = next((i for i, line in enumerate(before) if line.startswith("## ")), len(before))
    return len(before) == len(after) and all(
        line == now
        or (now == REMOVED and i > first and line.strip() != "" and not line.startswith("#"))
        for i, (line, now) in enumerate(zip(before, after, strict=True))
    )


def change_problems(root: Path, *bases: str) -> tuple[list[str], int]:
    """What changed in the records that the bases hold, and how many they hold."""
    current = records_in_tree(root, "HEAD")
    problems: dict[str, None] = {}
    held: set[str] = set()
    folder = DECISIONS.as_posix()
    for base in bases:
        found = records_in_tree(root, base)
        if not found and git(root, "cat-file", "-e", f"{base}:{folder}").returncode == 0:
            problems[
                f"{base} holds {folder} but no file named as a record, so nothing was compared"
            ] = None
        for path, (mode, item) in sorted(found.items()):
            held.add(path)
            now = current.get(path)
            if now is None:
                problems[
                    f"{path}, which the default branch holds, was removed, renamed or moved:"
                    " a record is never removed, only closed by a record that replaces it"
                ] = None
            elif now != (mode, item) and not (
                now[0] == mode
                and mode.startswith("100")
                and closed_from(content(root, item), content(root, now[1]))
            ):
                problems[
                    f"{path} was changed after the default branch held it: an accepted record"
                    " changes only to be closed by a record that replaces it, and a closed one"
                    " only to have lines of its text replaced by [removed]"
                ] = None
    return list(problems), len(held)


def id_problems(root: Path, *bases: str) -> list[str]:
    """Every requirement, threat and assumption ID that the bases hold or retire is still held
    or retired, an ID counting as retired only where the section "Retired IDs" lists it."""
    problems = []
    for path, held, retired in (
        ("docs/requirements.md", REGISTER_ID, RETIRED_ID),
        ("docs/threat-model.md", THREAT_HEADING, RETIRED_THREAT),
        ("docs/assumptions/README.md", INDEX_ID, RETIRED_ASSUMPTION),
    ):
        new = git(root, "show", f"HEAD:{path}").stdout.decode("utf-8")
        kept = set(held.findall(new)) | retired_in(new, retired)
        gone: set[str] = set()
        for base in bases:
            before = git(root, "show", f"{base}:{path}")
            if before.returncode == 0:
                old = before.stdout.decode("utf-8")
                gone |= (set(held.findall(old)) | retired_in(old, retired)) - kept
        problems += [
            f"{ident}, which {path} holds on the default branch, is neither held nor retired"
            for ident in sorted(gone, key=number)
        ]
    return problems


def title_problems(root: Path, *bases: str) -> tuple[list[str], int]:
    """Each title that the bases' specs hold and an accepted record quotes, and that the
    specs no longer hold, naming the record. Also says how many such titles the bases hold."""
    held: set[str] = set()
    for base in bases:
        held |= spec_titles(root, base)
    now = spec_titles(root, "HEAD")
    problems = []
    compared: set[str] = set()
    for path, (_mode, item) in sorted(records_in_tree(root, "HEAD").items()):
        text = content(root, item)
        if not ACCEPTED.search(text):
            continue
        named = FILE_NAME.fullmatch(posixpath.basename(path))
        assert named is not None
        for title in sorted(set(QUOTATION.findall(text)) & held):
            compared.add(title)
            if title not in now:
                problems.append(
                    f'DR-{named[1]} quotes "{title}", a title that the specs held on the default'
                    " branch and no longer hold"
                )
    return problems, len(compared)


def spec_titles(root: Path, commit: str) -> set[str]:
    """The requirements' and scenarios' titles that the specs hold in a commit, leaving out
    those under "REMOVED Requirements".

    Raises LookupError when git cannot list the commit's files.
    """
    listing = git(
        root, "ls-tree", "-r", "-z", "--name-only", "--full-tree", commit, "--", "openspec"
    )
    if listing.returncode != 0:
        raise LookupError(f"cannot list the files of {commit}")
    titles: set[str] = set()
    for path in listing.stdout.decode("utf-8", "surrogateescape").split("\0"):
        if SPEC_FILE.fullmatch(path):
            text = git(root, "show", f"{commit}:{path}").stdout.decode("utf-8")
            titles.update(SPEC_TITLE.findall(REMOVED_SECTION.sub("", text)))
    return titles


def listing_problems(
    model: str, records: dict[str, Record], new: set[str]
) -> tuple[list[str], int]:
    """A threat whose answer cites a record that the default branch does not hold yet is
    listed among that record's threats. Also says how many answers it read."""
    problems = []
    answers = 0
    for block in THREAT_BLOCK.finditer(model):
        threat = block.group(1)
        held = HELD_BY.search(block.group(0))
        answers += held is not None
        for each in RECORD_MENTION.findall(held.group(1) if held else ""):
            record = records.get(f"DR-{each}")
            if record and record.ident in new and threat not in record.listed("Threats"):
                problems.append(f"{threat} cites {record.ident}, which does not list {threat}")
    return problems, answers


def held_by_problems(model: str, records: dict[str, Record]) -> list[str]:
    """Each threat that an accepted record lists names that record in its Held by line, so
    that the change that closes the record meets the threat."""
    named = {}
    for block in THREAT_BLOCK.finditer(model):
        held = HELD_BY.search(block.group(0))
        named[block.group(1)] = set(RECORD_MENTION.findall(held.group(1) if held else ""))
    return [
        f"{record.ident} lists {threat}, whose Held by line does not name it"
        for record in records.values()
        if record.fields.get("Status") == "accepted"
        for threat in record.listed("Threats")
        if threat in named and record.ident.removeprefix("DR-") not in named[threat]
    ]


def misplaced_problems(paths: Iterable[str]) -> list[str]:
    """Files named as records anywhere but in the records' folder."""
    return [
        f"{path} is named as a record outside {DECISIONS.as_posix()}"
        for path in paths
        if FILE_NAME.fullmatch(posixpath.basename(path))
        and posixpath.dirname(path) != DECISIONS.as_posix()
    ]


def attribute_problems(root: Path, paths: list[str]) -> list[str]:
    """The attributes that would change how these files' diffs show. Only the repository's
    attributes count, not a contributor's own file of them.

    Raises LookupError when git cannot read them.
    """
    done = git(
        root, "-c", f"core.attributesFile={os.devnull}", "check-attr", "-a", "-z", "--", *paths
    )
    if done.returncode != 0:
        raise LookupError(f"git check-attr failed: {done.stderr.decode().strip()}")
    fields = done.stdout.decode("utf-8").split("\0")[:-1]
    return sorted(
        f"{path} has {name}: {value}, which changes how its diff shows"
        for path, name, value in zip(fields[0::3], fields[1::3], fields[2::3], strict=True)
        if name in DIFF_ATTRIBUTES
    )


def test_every_decision_has_a_record_and_the_index_lists_each() -> None:
    problems, count = problems_in(ROOT / DECISIONS, ROOT)
    assert not problems, "\n".join(problems)
    assert count, "no decision record was read, so this test covered nothing"


def test_every_record_and_design_decision_named_exists_and_no_closed_record_is_followed() -> None:
    records, _ = records_of(ROOT / DECISIONS)
    files = tracked_texts(ROOT)
    problems = mention_problems(files, records, ROOT)
    assert not problems, "\n".join(problems)
    assert any(RECORD_MENTION.search(text) for text in files.values()), "no mention was read"


def test_no_file_outside_the_records_folder_is_named_as_a_record() -> None:
    listing = git(ROOT, "ls-files", "-z").stdout.decode("utf-8").split("\0")
    assert not misplaced_problems(listing), "\n".join(misplaced_problems(listing))
    assert any(path.startswith(f"{DECISIONS}/DR-") for path in listing), "no record was listed"


def test_no_attribute_changes_how_a_record_s_diff_shows() -> None:
    listing = git(ROOT, "ls-files", "-z", "--", DECISIONS.as_posix()).stdout.decode("utf-8")
    paths = [path for path in listing.split("\0") if path]
    assert paths, "no record was listed, so this test covered nothing"
    problems = attribute_problems(ROOT, paths)
    assert not problems, "\n".join(problems)


def test_no_record_the_default_branch_holds_was_changed_but_to_be_closed() -> None:
    bases = base_commits(ROOT, os.environ)
    problems, held = change_problems(ROOT, *bases)
    if not held and not problems:
        pytest.skip(
            f"no base ({', '.join(bases)}) holds {DECISIONS.as_posix()} yet, so there is"
            " nothing to compare"
        )
    assert not problems, "\n".join(problems)


def test_every_requirement_threat_and_assumption_id_the_default_branch_holds_stays() -> None:
    bases = base_commits(ROOT, os.environ)
    if all(
        git(ROOT, "cat-file", "-e", f"{base}:docs/requirements.md").returncode != 0
        for base in bases
    ):
        pytest.skip(
            f"no base ({', '.join(bases)}) holds a register yet, so there is nothing to compare"
        )
    problems = id_problems(ROOT, *bases)
    assert not problems, "\n".join(problems)


def test_every_title_that_an_accepted_record_quotes_stays_in_the_specs() -> None:
    problems, compared = title_problems(ROOT, *base_commits(ROOT, os.environ))
    assert not problems, "\n".join(problems)
    assert compared, (
        "no base's specs hold a title that an accepted record quotes, so none was compared"
    )


def test_a_threat_that_cites_a_record_new_here_is_listed_in_it() -> None:
    held = {path for base in base_commits(ROOT, os.environ) for path in records_in_tree(ROOT, base)}
    records, _ = records_of(ROOT / DECISIONS)
    new = {ident for ident, record in records.items() if f"{DECISIONS}/{record.file}" not in held}
    model = (ROOT / "docs" / "threat-model.md").read_text(encoding="utf-8")
    problems, answers = listing_problems(model, records, new)
    assert not problems, "\n".join(problems)
    assert answers, "no threat's answer was read, so this test covered nothing"


def test_every_threat_that_an_accepted_record_lists_names_it() -> None:
    records, _ = records_of(ROOT / DECISIONS)
    model = (ROOT / "docs" / "threat-model.md").read_text(encoding="utf-8")
    problems = held_by_problems(model, records)
    assert not problems, "\n".join(problems)
    assert any(record.listed("Threats") for record in records.values()), "no threat was listed"


def record(
    number: int = 1,
    title: str = "A choice",
    kind: str = "scope",
    status: str = "accepted",
    decider: str = "the change `demo`",
    requirements: str = "R1",
    threats: str = "T1",
    replaces: str = "none",
    closed_by: str = "none",
) -> str:
    return (
        f"# DR-{number:03d}: {title}\n\n"
        f"- **Type:** {kind}\n"
        f"- **Status:** {status}\n"
        f"- **Decided by:** {decider}\n"
        f"- **Requirements:** {requirements}\n"
        f"- **Threats:** {threats}\n"
        f"- **Replaces:** {replaces}\n"
        f"- **Closed by:** {closed_by}\n\n"
        "## Context\n\nSomething made a choice necessary.\n\n"
        "## Decision\n\nThe thing is done one way.\n\n"
        "## Alternatives\n\nNone were recorded when this was decided.\n\n"
        "## Consequences\n\n- Something follows.\n- Something else follows.\n\n"
        "## Scope\n\nIt covers the thing.\n\n"
        "## What reversing it would change\n\nThe thing would change back.\n"
    )


def row(
    number: int = 1,
    title: str = "A choice",
    kind: str = "scope",
    status: str = "accepted",
    decider: str = "the change `demo`",
    requirements: str = "R1",
    threats: str = "T1",
) -> str:
    link = f"DR-{number:03d}-a-choice.md"
    return (
        f"| [DR-{number:03d}]({link}) | {title} | {kind} | {status} | {decider} "
        f"| {requirements} | {threats} |\n"
    )


INDEX_HEAD = (
    "# Decision records\n\n"
    "| Record | Decision | Type | Status | Decided by | Requirements | Threats |\n"
    "|---|---|---|---|---|---|---|\n"
)


def synthetic_repository(root: Path, records: list[str], index: str | None = None) -> Path:
    """A repository holding the given records, numbered from DR-001, and their index."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "requirements.md").write_text(
        "| R1 | functional | `thing` | It works |\n"
        "| R3 | functional | `thing` | It is fast |\n\n"
        "## Retired IDs\n\n- R2, removed by `old`\n"
    )
    (root / "docs" / "threat-model.md").write_text(
        "### T1. One thing\n\n- **Held by:** DR-001\n\n"
        "### T2. Another\n\n- **Held by:** `docs/note.md`\n\n"
        "## Retired IDs\n\n- T3, removed by `old`\n"
    )
    (root / "docs" / "assumptions").mkdir(exist_ok=True)
    (root / "docs" / "assumptions" / "README.md").write_text(
        "## The assumptions, most at stake first\n\n"
        "- **A1.** One thing holds.\n- **A3.** Another holds.\n\n"
        "## Retired IDs\n\n- A2, removed by `old`\n"
    )
    (root / "openspec" / "changes" / "demo").mkdir(parents=True, exist_ok=True)
    (root / "openspec" / "changes" / "demo" / "design.md").write_text("### 1. A choice\n")
    (root / "openspec" / "changes" / "demo" / "tasks.md").write_text(
        "## 1. Work\n\n- [ ] 1.1 Do it\n- [x] 1.2 Did it\n"
    )
    (root / "openspec" / "changes" / "archive" / "2026-01-01-old").mkdir(parents=True)
    folder = root / DECISIONS
    folder.mkdir(parents=True)
    for each, text in enumerate(records, start=1):
        (folder / f"DR-{each:03d}-a-choice.md").write_text(text)
    if index is None:
        index = INDEX_HEAD + "".join(row(each) for each in range(1, len(records) + 1))
    (folder / "README.md").write_text(index)
    return folder


def problems_of(root: Path, records: list[str], index: str | None = None) -> list[str]:
    folder = synthetic_repository(root, records, index)
    return problems_in(folder, root)[0]


def test_a_complete_set_of_records_has_no_problem(tmp_path: Path) -> None:
    folder = synthetic_repository(tmp_path, [record(1), record(2)])
    assert problems_in(folder, tmp_path) == ([], 2)


def test_a_closed_record_and_the_record_that_closed_it_name_each_other(tmp_path: Path) -> None:
    records = [
        record(1, status="closed", closed_by="DR-002"),
        record(2, replaces="DR-001"),
    ]
    index = INDEX_HEAD + row(1, status="closed") + row(2)
    assert problems_of(tmp_path, records, index) == []


@pytest.mark.parametrize(
    "decider",
    [
        "the owner, 2026-10-18",
        "the owner, 2026-10-18 and 2026-10-20",
        "the owner, 2026-10-17, 2026-10-18 and 2026-10-20",
        "the change `demo`",
        "the change `old`",
        "the change `demo`, as the owner asked on 2026-10-20",
        "the change `demo`, as the owner asked on 2026-10-20 and 2026-10-25",
    ],
)
def test_each_form_of_decider_is_accepted(tmp_path: Path, decider: str) -> None:
    index = INDEX_HEAD + row(1, decider=decider)
    assert problems_of(tmp_path, [record(1, decider=decider)], index) == []


def test_retired_ids_beside_held_ones_and_no_citation_at_all_are_accepted(
    tmp_path: Path,
) -> None:
    first = record(1, requirements="R1, R2, R3", threats="T3")
    second = record(2, requirements="none", threats="none")
    rows = row(1, requirements="R1, R2, R3", threats="T3") + row(
        2, requirements="none", threats="none"
    )
    assert problems_of(tmp_path, [first, second], INDEX_HEAD + rows) == []


def test_a_record_may_link_to_another_record_by_its_id(tmp_path: Path) -> None:
    text = record(1).replace(
        "It covers the thing.", "It covers the thing, not [DR-002](DR-002-a-choice.md)."
    )
    assert problems_of(tmp_path, [text, record(2)]) == []


def test_an_id_counts_as_retired_only_under_retired_ids(tmp_path: Path) -> None:
    folder = synthetic_repository(tmp_path, [record(1, requirements="R1, R4", threats="T1, T4")])
    register = tmp_path / "docs" / "requirements.md"
    register.write_text(
        register.read_text().replace("\n## Retired", "- R4, removed by `old`\n\n## Retired")
    )
    model = tmp_path / "docs" / "threat-model.md"
    model.write_text(
        model.read_text().replace("\n## Retired", "- T4, removed by `old`\n\n## Retired")
    )
    (folder / "README.md").write_text(INDEX_HEAD + row(1, requirements="R1, R4", threats="T1, T4"))
    problems, _ = problems_in(folder, tmp_path)
    assert problems == [
        "DR-001 cites R4, which the register does not hold",
        "DR-001 cites T4, which the threat model does not hold",
    ]


def test_a_placeholder_or_a_pipe_in_inline_code_is_neither_html_nor_a_table(
    tmp_path: Path,
) -> None:
    text = record(1).replace(
        "It covers the thing.",
        "It covers `refs/pull/<number>/head`, `` `<x>` ``, `a | b` and `x[0][1]`.",
    )
    assert problems_of(tmp_path, [text]) == []


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        ("- **Threats:** T1\n", "", "has the fields ['Type', 'Status', 'Decided by', "),
        (
            "- **Type:** scope\n- **Status:** accepted\n",
            "- **Status:** accepted\n- **Type:** scope\n",
            "has the fields ['Status', 'Type', ",
        ),
        ("- **Type:** scope\n", "- **Type:** scope\n- **Type:** scope\n", "has the fields "),
        ("- **Closed by:** none\n", "- **Closed by:** none\nAn aside.\n", "not a field"),
        ("- **Type:** scope\n", "- **Type:** mood\n", "has a type outside the list: 'mood'"),
        ("- **Status:** accepted\n", "- **Status:** proposed\n", "has a status outside the list"),
        ("the change `demo`", "someone", "is decided by 'someone', which is not a form"),
        ("the change `demo`", "the owner", "which is not a form from the list"),
        ("the change `demo`", "the owner, 18 October", "which is not a form from the list"),
        ("the change `demo`", "the owner, 2026-02-30", "gives 2026-02-30, which is not a date"),
        ("the change `demo`", "the owner, 2999-01-01", "gives 2999-01-01, which is later than"),
        (
            "the change `demo`",
            "the change `demo`, as the owner asked on 2026-10-18 and 2999-01-01",
            "gives 2999-01-01, which is later than",
        ),
        ("the change `demo`", "the change `gone`", "`gone`, which is not a change"),
        ("the change `demo`", "the change demo", "which is not a form from the list"),
        ("- **Requirements:** R1\n", "- **Requirements:** R1,R3\n", "neither none nor a list"),
        ("- **Requirements:** R1\n", "- **Requirements:** R3, R1\n", "out of order or twice"),
        ("- **Requirements:** R1\n", "- **Requirements:** R1, R1\n", "out of order or twice"),
        ("- **Requirements:** R1\n", "- **Requirements:** R9\n", "cites R9, which the register"),
        ("- **Requirements:** R1\n", "- **Requirements:** R2\n", "every requirement it cites"),
        ("- **Threats:** T1\n", "- **Threats:** T9\n", "cites T9, which the threat model"),
        ("- **Threats:** T1\n", "- **Threats:** 1\n", "Threats that is neither none nor"),
        ("- **Replaces:** none\n", "- **Replaces:** DR-9\n", "Replaces that is neither none"),
        ("- **Replaces:** none\n", "- **Replaces:** DR-007\n", "DR-007 in Replaces, which is not"),
        ("- **Closed by:** none\n", "- **Closed by:** DR-002, DR-003\n", "Closed by that is"),
        ("## Scope\n\nIt covers the thing.\n\n", "", "has the sections ['Context', "),
        (
            "## Context\n\nSomething made a choice necessary.\n\n"
            "## Decision\n\nThe thing is done one way.\n\n",
            "## Decision\n\nThe thing is done one way.\n\n"
            "## Context\n\nSomething made a choice necessary.\n\n",
            "has the sections ['Decision', 'Context', ",
        ),
        ("## Scope\n", "## Scope\n\nIt covers the thing.\n\n## Scope\n", "has the sections "),
        ("## What reversing it would change\n", "## How to reverse it\n", "has the sections "),
        ("- Something follows.\n- Something else follows.\n", "\n", "says nothing under 'Conseq"),
        ("The thing would change back.\n", "", "says nothing under 'What reversing it would"),
        ("# DR-001: A choice\n", "# DR-002: A choice\n", "is headed DR-002, not the number"),
        ("# DR-001: A choice\n", "A choice\n", "does not open with its heading"),
        ("# DR-001: A choice\n", "# DR-001: A | choice\n", "does not open with its heading"),
        ("# DR-001: A choice\n", "\n# DR-001: A choice\n", "does not open with its heading"),
        ("It covers the thing.", "It covers\n```\nrm -rf\n```\n", "holds a fenced block"),
        ("It covers the thing.", "It covers ~~~ the thing.", "holds a fenced block"),
        ("It covers the thing.", "It covers <!-- hidden --> the thing.", "holds <, with which"),
        ("It covers the thing.", "It covers <b>the</b> thing.", "holds <, with which"),
        ("It covers the thing.", "It covers `a` <b>the</b> `c` thing.", "holds <, with which"),
        ("It covers the thing.", "It covers `<b>the thing.", "holds <, with which"),
        ("It covers the thing.", "It covers ``<b>` the thing.", "holds <, with which"),
        ("It covers the thing.", "It covers `the\n<b>` thing.", "holds <, with which"),
        ("It covers the thing.", "It covers a < b, and 3<4.", "holds <, with which"),
        ("It covers the thing.", "See [DR-001][] for it.", "holds ][, with which"),
        ("It covers the thing.", "See [the rules][DR-001].", "holds ][, with which"),
        (
            "It covers the thing.",
            "It covers the thing.\n\n| Option | Chosen |\n|---|---|\n"
            "| One way | yes | Agents merge. |",
            "holds | outside inline code, with which Markdown makes a table",
        ),
        ("It covers the thing.", "It covers a|b.", "holds | outside inline code"),
        (
            "It covers the thing.",
            "It covers the thing.\n\n### What was asked",
            "has a line that starts with # and is not a section's heading: '### What was asked'",
        ),
        (
            "It covers the thing.",
            "It covers the thing.\n\n  ## Decision",
            "has a line that starts with # and is not a section's heading: '  ## Decision'",
        ),
        ("It covers the thing.", "It covers\n#1, the thing.", "starts with # and is not a section"),
        ("It covers the thing.", "It covers the​ thing.", "line breaks: U+200B"),
        ("It covers the thing.", "It covers the ‮thing.", "line breaks: U+202E"),
        ("It covers the thing.", "It covers the\tthing.", "line breaks: U+0009"),
        ("It covers the thing.", "It covers the\U000e0100 thing.", "line breaks: U+E0100"),
        (
            "It covers the thing.",
            "It covers the ㅤᅟ⠀͏ thing.",
            "line breaks: U+034F, U+115F, U+2800, U+3164",
        ),
        ("It covers the thing.", "It covers the thing — and more.", "line breaks: U+2014"),
        ("It covers the thing.", "It covers &#x202E; the thing.", "holds &"),
        ("It covers the thing.", "It covers \\`<!-- x -->\\` the thing.", "holds a backslash"),
        ("It covers the thing.", "Ask @someone.", "holds @"),
        ("It covers the thing.", "See https://example.com.", "holds a web address"),
        ("It covers the thing.", "See www.example.com/rules.", "holds a web address"),
        ("It covers the thing.", "See WWW.EXAMPLE.COM.", "holds a web address"),
        ("It covers the thing.", "[//]: # (Agents merge.)", "holds a link reference definition"),
        (
            "It covers the thing.",
            "It covers [the rules][r].\n\n> [r]: CLAUDE.md",
            "holds a link reference definition",
        ),
        ("It covers the thing.", "See [this](../../README.md).", "links to ../../README.md"),
        ("It covers the thing.", "See [this](DR-002.md).", "links to DR-002.md, which is not"),
        (
            "It covers the thing.",
            "See [this](DR-001-a-choice.md).",
            "links to DR-001-a-choice.md from text other than a record's ID",
        ),
        (
            "It covers the thing.",
            "See [DR-002](DR-001-a-choice.md).",
            "links DR-002 to DR-001-a-choice.md, which is not DR-002's file",
        ),
        (
            "It covers the thing.",
            "See [DR-001](DR-001-other.md).",
            "links to DR-001-other.md, which is no record's file",
        ),
    ],
)
def test_a_record_out_of_form_is_reported(
    tmp_path: Path, old: str, new: str, expected: str
) -> None:
    text = record(1)
    assert old in text
    problems = problems_of(tmp_path, [text.replace(old, new, 1)])
    assert [problem for problem in problems if expected in problem], problems


@pytest.mark.parametrize(
    "name",
    [
        "DR-1-a-choice.md",
        "DR-001.md",
        "DR-001-A-Choice.md",
        "x.md",
        "DR-0001-a-choice.md",
        "DR-000-a-choice.md",
        "DR-００１-a-choice.md",
        "DR-001-a-choice.markdown",
    ],
)
def test_a_file_not_named_as_a_record_is_reported(tmp_path: Path, name: str) -> None:
    folder = synthetic_repository(tmp_path, [record(1)])
    (folder / "DR-001-a-choice.md").rename(folder / name)
    problems, count = problems_in(folder, tmp_path)
    assert f"{name} is not named DR-NNN-<words>.md" in problems
    assert count == 0


@pytest.mark.parametrize("path", ["notes/merging.md", "notes/DR-002-a-choice.md", "a/b/c.txt"])
def test_a_file_in_a_folder_under_the_records_is_reported(tmp_path: Path, path: str) -> None:
    folder = synthetic_repository(tmp_path, [record(1)])
    (folder / path).parent.mkdir(parents=True)
    (folder / path).write_text(record(2))
    problems, count = problems_in(folder, tmp_path)
    top = path.split("/")[0]
    assert problems == [
        f"{top} is a folder, and the records' folder holds only records and their index"
    ]
    assert count == 1


@pytest.mark.parametrize(
    ("name", "target"), [("DR-002-a-choice.md", "kept.md"), ("README.md", "kept.md"), ("x", "docs")]
)
def test_a_link_in_the_records_folder_is_reported(tmp_path: Path, name: str, target: str) -> None:
    # A link's own diff is a path, while what it shows can change in a file that is no record.
    folder = synthetic_repository(tmp_path, [record(1), record(2)])
    path = folder / name
    if path.exists():
        (tmp_path / target).write_text(path.read_text())
        path.unlink()
    path.symlink_to(tmp_path / target)
    problems, _ = problems_in(folder, tmp_path)
    assert f"{name} is a link, and the records' folder holds only files" in problems


def test_a_file_named_as_a_record_outside_the_records_folder_is_reported() -> None:
    paths = [
        "docs/decisions/DR-001-a-choice.md",
        "docs/decisions/README.md",
        "docs/DR-001-a-choice.md",
        "DR-002-a-choice.md",
        "docs/decisions/old/DR-003-a-choice.md",
        "docs/DR-01-not-a-record-name.md",
    ]
    assert misplaced_problems(paths) == [
        "docs/DR-001-a-choice.md is named as a record outside docs/decisions",
        "DR-002-a-choice.md is named as a record outside docs/decisions",
        "docs/decisions/old/DR-003-a-choice.md is named as a record outside docs/decisions",
    ]


def test_a_folder_without_records_is_reported(tmp_path: Path) -> None:
    assert problems_of(tmp_path, [], INDEX_HEAD) == ["no decision record found"]


def test_a_gap_and_a_repeated_number_are_reported(tmp_path: Path) -> None:
    folder = synthetic_repository(tmp_path, [record(1), record(2), record(3)])
    (folder / "DR-002-a-choice.md").unlink()
    (folder / "DR-003-another.md").write_text(record(3))
    problems, _ = problems_in(folder, tmp_path)
    assert "the records are not numbered from DR-001 without a gap: DR-002 missing" in problems
    assert "DR-003 is the number of more than one record" in problems


@pytest.mark.parametrize(
    ("index", "expected"),
    [
        (None, "the decisions folder has no index"),
        (INDEX_HEAD + row(1), "DR-002 is not in the index"),
        (INDEX_HEAD + row(1) + row(2) + row(3), "the index lists DR-003, which has no record"),
        (INDEX_HEAD + row(1) + row(1) + row(2), "the index lists DR-001 twice"),
        (INDEX_HEAD + row(2) + row(1), "the index does not list the records in order"),
        (
            INDEX_HEAD + row(1).replace("DR-001-a-choice.md", "DR-001-other.md") + row(2),
            "the index links DR-001 to DR-001-other.md, not to DR-001-a-choice.md",
        ),
        (
            INDEX_HEAD + row(1, title="Another choice") + row(2),
            "the index row for DR-001 differs from the record in ['title']",
        ),
        (
            INDEX_HEAD + row(1, status="closed", threats="T2") + row(2),
            "the index row for DR-001 differs from the record in ['Status', 'Threats']",
        ),
        (
            INDEX_HEAD + row(1).replace(" | T1 |", " |") + row(2),
            "the index row for DR-001 does not have 6 cells",
        ),
        (
            INDEX_HEAD + row(1) + row(2) + "\n<!-- a note -->\n",
            "README.md holds <, with which Markdown starts HTML or a link",
        ),
        (
            INDEX_HEAD + row(1) + row(2) + row(2, title="Agents merge").replace("| [", "|[", 1),
            "the index has a line that is not a row: '|[DR-002](DR-002-a-choice.md) | Agents merge"
            " | scope | accepted | the change `demo` | R1 | T1 |'",
        ),
        (
            INDEX_HEAD + row(1) + " " + row(2),
            "the index has a line that is not a row: ' | [DR-002](DR-002-a-choice.md) | A choice"
            " | scope | accepted | the change `demo` | R1 | T1 |'",
        ),
        (
            INDEX_HEAD + row(1) + row(2) + "\nA note | with a pipe.\n",
            "the index has a line that is not a row: 'A note | with a pipe.'",
        ),
        (
            # A line without a pipe right after the rows still renders as a row of the table.
            INDEX_HEAD + row(1) + row(2) + "DR-003 Agents merge, decided by the owner\n",
            "the index has a line that is not a row: 'DR-003 Agents merge, decided by the owner'",
        ),
        (
            INDEX_HEAD + row(1) + "\n" + row(2),
            "the index has a line that is not a row: '| [DR-002](DR-002-a-choice.md) | A choice"
            " | scope | accepted | the change `demo` | R1 | T1 |'",
        ),
        (
            INDEX_HEAD.replace("| Threats |", "| Threat |") + row(1) + row(2),
            "the index's table does not open with its header",
        ),
        (
            "# Decision records\n\n" + row(1) + row(2),
            "the index's table does not open with its header",
        ),
    ],
)
def test_an_index_that_disagrees_with_the_records_is_reported(
    tmp_path: Path, index: str | None, expected: str
) -> None:
    folder = synthetic_repository(tmp_path, [record(1), record(2)], index or "")
    if index is None:
        (folder / "README.md").unlink()
    assert expected in problems_in(folder, tmp_path)[0]


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        (
            {"closed_by": "DR-002"},
            {"replaces": "DR-001"},
            "DR-001 is accepted and yet names DR-002 in Closed by",
        ),
        ({"status": "closed"}, {}, "DR-001 is closed and names no record in Closed by"),
        (
            {"status": "closed", "closed_by": "DR-002"},
            {},
            "DR-001 is closed by DR-002, which does not name it in Replaces",
        ),
        (
            {},
            {"replaces": "DR-001"},
            "DR-002 replaces DR-001, which does not name DR-002 in Closed by",
        ),
        (
            {"status": "closed", "closed_by": "DR-001", "replaces": "DR-001"},
            {},
            "DR-001 names itself in Closed by",
        ),
        (
            {"status": "closed", "closed_by": "DR-001", "replaces": "DR-001"},
            {},
            "DR-001 names itself in Replaces",
        ),
    ],
)
def test_a_closed_record_that_does_not_name_its_closer_both_ways_is_reported(
    tmp_path: Path, first: dict[str, str], second: dict[str, str], expected: str
) -> None:
    records = [record(1, **first), record(2, **second)]
    index = INDEX_HEAD + row(1, status=first.get("status", "accepted")) + row(2)
    assert expected in problems_of(tmp_path, records, index)


def mentions(root: Path, files: dict[str, str]) -> list[str]:
    folder = synthetic_repository(
        root, [record(1, status="closed", closed_by="DR-002"), record(2, replaces="DR-001")]
    )
    records, _ = records_of(folder)
    return mention_problems(files, records, root)


def test_mentions_that_resolve_are_not_reported(tmp_path: Path) -> None:
    files = {
        "README.md": "DR-002 holds. See design decision 1, and design decisions 1 and 1.",
        "docs/decisions/README.md": "As the design's decision 1 says, DR-001 is closed.",
        "docs/features/thing.md": "Design decision 1 of `demo`, and `demo` decision 1.",
        "CHANGELOG.md": "DR-001 was closed by DR-002.",
        "docs/decisions/DR-002-a-choice.md": "It replaces DR-001.",
        "openspec/changes/archive/2026-01-01-old/proposal.md": "Following DR-001.",
        "openspec/changes/demo/design.md": "As decision 1 says (decision 1).",
        "docs/other.md": "The owner's decision 4, and task 1.2 of decision 3.5, and DR-01.",
        "docs/titled.md": "DR-002 (A choice) holds, as DR-002 (A\nchoice) says, and DR-002, (a).",
        "docs/ids.md": "R1, R3 and the retired R2 hold, and so do T1, T2 and the retired T3.",
        "docs/tasks.md": (
            "Task 1.1 covers it, as tasks 1.1 and 1.2, tasks 1.1 to 1.2, task 1.2 of `demo`"
            " and `demo` tasks 1.1 and 1.2 do, in the change `demo` and the change `old`."
        ),
        "docs/requirements.md": "## Retired IDs\n\n- R2, removed by `old`\n",
        "docs/plain.md": "R2D2, T1000s and 2026-10-26T15 name nothing; a PR changes `x` too.",
        "package-lock.json": '"sha512-x+R999/T0=", "the change `gone`", "task 9.9"',
    }
    assert mentions(tmp_path, files) == []


@pytest.mark.parametrize(
    ("path", "text", "expected"),
    [
        ("README.md", "See DR-003.", "README.md names DR-003, which is not a record"),
        ("README.md", "See DR-001.", "README.md names DR-001, which is closed"),
        ("docs/threat-model.md", "- **Held by:** DR-001", "names DR-001, which is closed"),
        ("docs/decisions/notes/x.md", "See DR-001.", "names DR-001, which is closed"),
        ("docs/decisions/DR-002-a-choice.markdown", "DR-001.", "names DR-001, which is closed"),
        ("docs/decisions/README.md.orig", "DR-001.", "names DR-001, which is closed"),
        ("docs/CHANGELOG.md", "See DR-001.", "names DR-001, which is closed"),
        ("openspec/changes/archive/notes.md", "See DR-001.", "names DR-001, which is closed"),
        ("CLAUDE.md", "See design decision 2.", "names decision 2 of any change, which is not"),
        ("ci.yml", "(design decisions 1 and 2)", "names decision 2 of any change"),
        ("x.md", "As the design's decisions 1 and 2 say.", "names decision 2 of any change"),
        ("x.md", "Design decision 1 of `gone`.", "names decision 1 of `gone`, which is not one"),
        ("x.md", "`demo` decision 2", "names decision 2 of `demo`, which is not one"),
        ("openspec/changes/demo/design.md", "(decision 2)", "names decision 2 of `demo`"),
        ("x.md", "As R9 says.", "x.md names R9, which the register neither holds nor retires"),
        ("x.md", "As T9 says.", "x.md names T9, which the threat model neither holds nor retires"),
        ("x.md", "As task 1.3 says.", "x.md names task 1.3 of any change, which is not one"),
        ("x.md", "As tasks 1.1 and 2.1 say.", "names task 2.1 of any change"),
        ("x.md", "As tasks 1.1 to 1.4 say.", "names task 1.4 of any change"),
        ("x.md", "Task 1.1 of `old`.", "names task 1.1 of `old`, which is not one"),
        ("x.md", "`demo` task 1.3", "x.md names task 1.3 of `demo`, which is not one"),
        ("x.md", "`gone` tasks 1.1 and 1.2", "names task 1.1 of `gone`, which is not one"),
        ("x.md", "As the change `gone` says.", "x.md names the change `gone`, which is not one"),
        ("x.md", "- R2, removed by `gone`", "x.md names the change `gone`, which is not one"),
    ],
)
def test_a_mention_that_names_nothing_or_a_closed_record_is_reported(
    tmp_path: Path, path: str, text: str, expected: str
) -> None:
    problems = mentions(tmp_path, {path: text})
    assert [problem for problem in problems if expected in problem], problems


@pytest.mark.parametrize(
    ("path", "text", "expected"),
    [
        ("x.md", "As DR-002 (Another choice) says.", 'x.md names DR-002 as "Another choice"'),
        ("x.md", "DR-002 (A choice (the second)).", 'x.md names DR-002 as "A choice (the second"'),
        ("CHANGELOG.md", "DR-001 (closed) was closed.", 'CHANGELOG.md names DR-001 as "closed"'),
    ],
)
def test_a_record_named_by_another_title_is_reported(
    tmp_path: Path, path: str, text: str, expected: str
) -> None:
    assert mentions(tmp_path, {path: text}) == [f'{expected}, and its title is "A choice"']


def test_a_threat_that_cites_a_new_record_is_listed_in_it(tmp_path: Path) -> None:
    folder = synthetic_repository(tmp_path, [record(1, threats="T2")])
    records, _ = records_of(folder)
    model = (tmp_path / "docs" / "threat-model.md").read_text()
    assert listing_problems(model, records, {"DR-001"}) == (
        ["T1 cites DR-001, which does not list T1"],
        2,
    )
    assert listing_problems(model, records, set()) == ([], 2)
    assert listing_problems(model, {}, {"DR-001"}) == ([], 2)
    assert listing_problems("No threat here.\n", records, {"DR-001"}) == ([], 0)


def test_a_threat_that_an_accepted_record_lists_names_it(tmp_path: Path) -> None:
    folder = synthetic_repository(
        tmp_path,
        [
            record(1, threats="T1, T2, T3"),
            record(2, status="closed", closed_by="DR-003", threats="T2"),
            record(3, replaces="DR-002", threats="T1, T4"),
        ],
    )
    records, _ = records_of(folder)
    model = (tmp_path / "docs" / "threat-model.md").read_text()
    model += "### T4. A third\n\nNothing holds it yet.\n"
    assert held_by_problems(model, records) == [
        "DR-001 lists T2, whose Held by line does not name it",
        "DR-003 lists T1, whose Held by line does not name it",
        "DR-003 lists T4, whose Held by line does not name it",
    ]
    assert held_by_problems(model.replace("DR-001\n", "DR-001 and DR-003\n"), records) == [
        "DR-001 lists T2, whose Held by line does not name it",
        "DR-003 lists T4, whose Held by line does not name it",
    ]


GIT_ENVIRONMENT = {
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.invalid",
}


def run_git(root: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        env={**os.environ, **GIT_ENVIRONMENT},
    )
    return done.stdout.decode().strip()


def test_git_reads_the_repository_it_is_given_whatever_the_session_sets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A git variable of the session's, such as a repository named elsewhere, or its own
    configuration, does not reach the checks' runs of git."""
    run_git(tmp_path, "init", "-q")
    setting = tmp_path / "config"
    setting.write_text("[planted]\n\tkey = set\n", encoding="utf-8")
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "elsewhere"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(setting))
    found = git(tmp_path, "rev-parse", "--absolute-git-dir")
    assert found.stdout.decode().strip() == str((tmp_path / ".git").resolve())
    assert git(tmp_path, "config", "planted.key").returncode == 1


def repository_with_history(root: Path, records: list[str]) -> Path:
    """A git repository whose `main` holds these records, checked out on a new branch,
    with `main` also fetched as `origin/main`."""
    folder = synthetic_repository(root, records)
    run_git(root, "init", "-q", "-b", "main")
    run_git(root, "add", "-A")
    run_git(root, "commit", "-q", "-m", "Hold the records")
    run_git(root, "update-ref", DEFAULT_BRANCH, "main")
    run_git(root, "checkout", "-q", "-b", "work")
    return folder


def commit(root: Path) -> None:
    run_git(root, "add", "-A")
    run_git(root, "commit", "-q", "--allow-empty", "-m", "Change the records")


def compared(root: Path) -> tuple[list[str], int]:
    return change_problems(root, *base_commits(root, {}))


def test_records_left_as_they_were_or_added_are_not_reported(tmp_path: Path) -> None:
    folder = repository_with_history(tmp_path, [record(1)])
    (folder / "DR-002-a-choice.md").write_text(record(2))
    commit(tmp_path)
    assert compared(tmp_path) == ([], 1)


def test_a_record_closed_and_then_cleared_of_a_paragraph_is_not_reported(
    tmp_path: Path,
) -> None:
    folder = repository_with_history(
        tmp_path, [record(1), record(2, status="closed", closed_by="DR-003")]
    )
    closed = record(1, status="closed", closed_by="DR-003")
    (folder / "DR-001-a-choice.md").write_text(closed.replace("- Something follows.", REMOVED))
    cleared = record(2, status="closed", closed_by="DR-003").replace(
        "It covers the thing.", REMOVED
    )
    (folder / "DR-002-a-choice.md").write_text(cleared)
    commit(tmp_path)
    assert compared(tmp_path) == ([], 2)


def test_a_line_of_a_section_that_looks_like_a_field_can_be_cleared(tmp_path: Path) -> None:
    bold = record(1).replace("- Something follows.", "- **Something** follows.")
    folder = repository_with_history(tmp_path, [bold])
    closed = bold.replace("- **Status:** accepted", "- **Status:** closed").replace(
        "- **Closed by:** none", "- **Closed by:** DR-002"
    )
    (folder / "DR-001-a-choice.md").write_text(closed.replace("- **Something** follows.", REMOVED))
    commit(tmp_path)
    assert compared(tmp_path) == ([], 1)


@pytest.mark.parametrize(
    ("first", "expected"),
    [
        (None, "DR-001-a-choice.md, which the default branch holds, was removed"),
        (record(1, title="A better choice"), "DR-001-a-choice.md was changed"),
        (record(1).replace("It covers the thing.", "It covers more."), "DR-001-a-choice.md was"),
        (record(1).replace("\n", "\r\n"), "DR-001-a-choice.md was changed"),
        (record(1, status="closed"), "DR-001-a-choice.md was changed"),
        (record(1, closed_by="DR-002"), "DR-001-a-choice.md was changed"),
        (record(1, status="closed", closed_by="DR-002", threats="T2"), "DR-001-a-choice.md was"),
        (record(1).replace("It covers the thing.", REMOVED), "DR-001-a-choice.md was changed"),
        (
            record(1, status="closed", closed_by="DR-002").replace("## Scope", REMOVED),
            "DR-001-a-choice.md was changed",
        ),
        (
            record(1, status="closed", closed_by="DR-002").replace("- **Threats:** T1", REMOVED),
            "DR-001-a-choice.md was changed",
        ),
        (
            record(1, status="closed", closed_by="DR-002").replace(
                "\n\n## Scope", f"\n{REMOVED}\n## Scope"
            ),
            "DR-001-a-choice.md was changed",
        ),
        (
            record(1, status="closed", closed_by="DR-002").replace("the thing.", f"the {REMOVED}."),
            "DR-001-a-choice.md was changed",
        ),
        (
            record(1, status="closed", closed_by="DR-002") + "A line added once closed.\n",
            "DR-001-a-choice.md was changed",
        ),
        (record(1, status="closed", closed_by="DR-002") + "\n", "DR-001-a-choice.md was changed"),
    ],
)
def test_a_record_removed_or_changed_but_as_closing_allows_is_reported(
    tmp_path: Path, first: str | None, expected: str
) -> None:
    folder = repository_with_history(tmp_path, [record(1)])
    path = folder / "DR-001-a-choice.md"
    if first is None:
        path.unlink()
    else:
        path.write_text(first)
    commit(tmp_path)
    problems, held = compared(tmp_path)
    assert held == 1
    assert [problem for problem in problems if expected in problem], problems


@pytest.mark.parametrize("move", ["rename", "move", "symlink", "mode", "closed and mode"])
def test_a_record_renamed_moved_or_replaced_is_reported(tmp_path: Path, move: str) -> None:
    folder = repository_with_history(tmp_path, [record(1)])
    path = folder / "DR-001-a-choice.md"
    if move == "closed and mode":
        path.write_text(record(1, status="closed", closed_by="DR-002"))
        path.chmod(0o755)
    elif move == "rename":
        path.rename(folder / "DR-001-a-better-name.md")
    elif move == "move":
        path.rename(tmp_path / "docs" / "DR-001-a-choice.md")
    elif move == "symlink":
        (tmp_path / "kept.md").write_text(record(1))
        path.unlink()
        path.symlink_to(tmp_path / "kept.md")
    else:
        path.chmod(0o755)
    commit(tmp_path)
    problems, _ = compared(tmp_path)
    assert len(problems) == 1 and "DR-001-a-choice.md" in problems[0], problems


def test_a_change_counts_only_once_it_is_committed(tmp_path: Path) -> None:
    folder = repository_with_history(tmp_path, [record(1)])
    (folder / "DR-001-a-choice.md").write_text(record(1, title="Changed"))
    assert compared(tmp_path) == ([], 1)
    commit(tmp_path)
    assert compared(tmp_path)[0]


def test_a_closed_record_changed_again_is_reported(tmp_path: Path) -> None:
    folder = repository_with_history(tmp_path, [record(1, status="closed", closed_by="DR-002")])
    (folder / "DR-001-a-choice.md").write_text(record(1, status="closed", closed_by="DR-003"))
    commit(tmp_path)
    problems, _ = compared(tmp_path)
    assert problems == [
        "docs/decisions/DR-001-a-choice.md was changed after the default branch held it: an"
        " accepted record changes only to be closed by a record that replaces it, and a closed"
        " one only to have lines of its text replaced by [removed]"
    ]


def test_records_held_outside_the_folder_are_compared_too(tmp_path: Path) -> None:
    folder = repository_with_history(tmp_path, [record(1)])
    run_git(tmp_path, "checkout", "-q", "main")
    (tmp_path / "docs" / "DR-009-elsewhere.md").write_text(record(9))
    commit(tmp_path)
    run_git(tmp_path, "update-ref", DEFAULT_BRANCH, "main")
    run_git(tmp_path, "checkout", "-q", "-b", "elsewhere")
    (tmp_path / "docs" / "DR-009-elsewhere.md").unlink()
    (folder / "DR-001-a-choice.md").unlink()
    commit(tmp_path)
    problems, held = compared(tmp_path)
    assert held == 2 and len(problems) == 2, problems


def test_the_base_is_the_commit_ci_names_or_else_where_head_left_the_default_branch(
    tmp_path: Path,
) -> None:
    repository_with_history(tmp_path, [record(1)])
    first = run_git(tmp_path, "rev-parse", "HEAD")
    commit(tmp_path)
    second = run_git(tmp_path, "rev-parse", "HEAD")
    assert base_commits(tmp_path, {}) == [first]
    assert base_commits(tmp_path, {"BASE_COMMIT": second}) == [second, first]
    assert base_commits(tmp_path, {"BASE_COMMIT": first}) == [first]


def test_a_change_is_compared_with_the_default_branch_too_whatever_base_ci_names(
    tmp_path: Path,
) -> None:
    # A pull request opened against a branch that holds no record, and then retargeted.
    (tmp_path / "README.md").write_text("A repository.\n")
    run_git(tmp_path, "init", "-q", "-b", "main")
    commit(tmp_path)
    before = run_git(tmp_path, "rev-parse", "HEAD")
    folder = synthetic_repository(tmp_path, [record(1)])
    commit(tmp_path)
    run_git(tmp_path, "update-ref", DEFAULT_BRANCH, "main")
    run_git(tmp_path, "checkout", "-q", "-b", "work")
    (folder / "DR-001-a-choice.md").write_text(record(1, title="A better choice"))
    commit(tmp_path)
    register = tmp_path / "docs" / "requirements.md"
    register.write_text(register.read_text().replace("- R2, removed by `old`\n", ""))
    commit(tmp_path)
    bases = base_commits(tmp_path, {"BASE_COMMIT": before})
    assert change_problems(tmp_path, before) == ([], 0)
    assert id_problems(tmp_path, before) == []
    assert id_problems(tmp_path, *bases) == [
        "R2, which docs/requirements.md holds on the default branch, is neither held nor retired"
    ]
    problems, held = change_problems(tmp_path, *bases)
    assert held == 1
    assert problems == [
        "docs/decisions/DR-001-a-choice.md was changed after the default branch held it: an"
        " accepted record changes only to be closed by a record that replaces it, and a closed"
        " one only to have lines of its text replaced by [removed]"
    ]


@pytest.mark.parametrize(
    ("environ", "expected"),
    [
        ({"BASE_COMMIT": "main"}, "BASE_COMMIT is not a full commit ID: 'main'"),
        ({"BASE_COMMIT": "0" * 40}, f"the base commit {'0' * 40} is not in this clone"),
    ],
)
def test_a_base_commit_that_is_not_one_is_an_error(
    tmp_path: Path, environ: dict[str, str], expected: str
) -> None:
    repository_with_history(tmp_path, [record(1)])
    with pytest.raises(LookupError, match=re.escape(expected)):
        base_commits(tmp_path, environ)


@pytest.mark.parametrize("environ", [{}, {"BASE_COMMIT": ""}, {"BASE_COMMIT": "named"}])
def test_a_default_branch_that_cannot_be_found_is_an_error(
    tmp_path: Path, environ: dict[str, str]
) -> None:
    repository_with_history(tmp_path, [record(1)])
    if environ.get("BASE_COMMIT") == "named":
        environ = {"BASE_COMMIT": run_git(tmp_path, "rev-parse", "HEAD")}
    run_git(tmp_path, "update-ref", "-d", DEFAULT_BRANCH)
    run_git(tmp_path, "tag", DEFAULT_BRANCH)
    with pytest.raises(LookupError) as raised:
        base_commits(tmp_path, environ)
    assert str(raised.value) == (
        "cannot find where HEAD left refs/remotes/origin/main: this clone does not have it,"
        " so run `git fetch origin main:refs/remotes/origin/main`"
    )


def clone(source: Path, target: Path, *options: str) -> Path:
    run_git(source.parent, "clone", "-q", *options, source.as_uri(), str(target))
    return target


def test_a_clone_of_one_branch_is_told_how_to_fetch_the_default_branch(tmp_path: Path) -> None:
    source = tmp_path / "source"
    repository_with_history(source, [record(1)])
    first = run_git(source, "rev-parse", "HEAD")
    commit(source)
    copy = clone(source, tmp_path / "copy", "--single-branch", "--branch", "work")
    with pytest.raises(LookupError, match=re.escape("run `git fetch origin main:refs/remotes")):
        base_commits(copy, {})
    run_git(copy, "fetch", "-q", "origin", f"main:{DEFAULT_BRANCH}")
    assert base_commits(copy, {}) == [first]


def test_a_shallow_clone_is_told_how_to_fetch_the_history(tmp_path: Path) -> None:
    source = tmp_path / "source"
    repository_with_history(source, [record(1)])
    first = run_git(source, "rev-parse", "HEAD")
    commit(source)
    copy = clone(source, tmp_path / "copy", "--depth", "1", "--no-single-branch")
    with pytest.raises(LookupError) as raised:
        base_commits(copy, {})
    assert str(raised.value) == (
        "cannot find where HEAD left refs/remotes/origin/main: this clone is shallow,"
        " so run `git fetch --unshallow`"
    )
    run_git(copy, "fetch", "-q", "--unshallow")
    assert base_commits(copy, {}) == [first]


def test_a_head_that_shares_no_history_with_the_default_branch_is_an_error(
    tmp_path: Path,
) -> None:
    repository_with_history(tmp_path, [record(1)])
    run_git(tmp_path, "checkout", "-q", "--orphan", "alone")
    commit(tmp_path)
    with pytest.raises(LookupError) as raised:
        base_commits(tmp_path, {})
    assert str(raised.value) == (
        "cannot find where HEAD left refs/remotes/origin/main: they share no commit"
    )


def test_a_tag_named_like_the_default_branch_is_not_taken_for_it(tmp_path: Path) -> None:
    repository_with_history(tmp_path, [record(1)])
    first = run_git(tmp_path, "rev-parse", "HEAD")
    (tmp_path / "other.md").write_text("Another file.\n")
    commit(tmp_path)
    run_git(tmp_path, "tag", "origin/main")
    run_git(tmp_path, "tag", DEFAULT_BRANCH)
    assert base_commits(tmp_path, {}) == [first]


def test_a_default_branch_that_holds_no_record_holds_nothing_to_compare(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("A repository.\n")
    run_git(tmp_path, "init", "-q", "-b", "main")
    commit(tmp_path)
    run_git(tmp_path, "update-ref", DEFAULT_BRANCH, "main")
    assert compared(tmp_path) == ([], 0)


def test_a_records_folder_with_no_record_by_this_test_s_names_is_reported(tmp_path: Path) -> None:
    # As when a change renames every record and the rule that names them, so nothing compares.
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    (tmp_path / "docs" / "decisions" / "DR-1-a-choice.md").write_text(record(1))
    run_git(tmp_path, "init", "-q", "-b", "main")
    commit(tmp_path)
    run_git(tmp_path, "update-ref", DEFAULT_BRANCH, "main")
    base = run_git(tmp_path, "rev-parse", "HEAD")
    assert compared(tmp_path) == (
        [f"{base} holds docs/decisions but no file named as a record, so nothing was compared"],
        0,
    )


def link_entry(root: Path, path: str, text: str) -> None:
    """Stage at `path` a link whose target is `text`, as git stores one."""
    source = root.parent / "target.txt"
    source.write_text(text)
    blob = run_git(root, "hash-object", "-w", str(source))
    run_git(root, "update-index", "--add", "--cacheinfo", f"120000,{blob},{path}")


def test_a_record_held_as_a_link_is_never_closed_through_its_target(tmp_path: Path) -> None:
    synthetic_repository(tmp_path, [record(1)])
    path = f"{DECISIONS.as_posix()}/DR-002-a-choice.md"
    run_git(tmp_path, "init", "-q", "-b", "main")
    run_git(tmp_path, "add", "-A")
    link_entry(tmp_path, path, record(2))
    run_git(tmp_path, "commit", "-q", "-m", "Hold a link")
    run_git(tmp_path, "update-ref", DEFAULT_BRANCH, "main")
    run_git(tmp_path, "checkout", "-q", "-b", "work")
    link_entry(tmp_path, path, record(2, status="closed", closed_by="DR-003"))
    run_git(tmp_path, "commit", "-q", "-m", "Change what it holds")
    problems, held = compared(tmp_path)
    assert held == 2
    assert problems == [
        f"{path} was changed after the default branch held it: an accepted record changes only"
        " to be closed by a record that replaces it, and a closed one only to have lines of its"
        " text replaced by [removed]"
    ]


def test_an_attribute_that_changes_how_a_record_s_diff_shows_is_reported(tmp_path: Path) -> None:
    synthetic_repository(tmp_path, [record(1)])
    run_git(tmp_path, "init", "-q", "-b", "main")
    paths = ["docs/decisions/DR-001-a-choice.md", "docs/decisions/README.md"]
    assert attribute_problems(tmp_path, paths) == []
    (tmp_path / ".gitattributes").write_text(
        "docs/decisions/*.md -diff linguist-generated\n*.md text eol=lf\n"
    )
    assert attribute_problems(tmp_path, paths) == [
        "docs/decisions/DR-001-a-choice.md has diff: unset, which changes how its diff shows",
        "docs/decisions/DR-001-a-choice.md has linguist-generated: set, which changes how its"
        " diff shows",
        "docs/decisions/README.md has diff: unset, which changes how its diff shows",
        "docs/decisions/README.md has linguist-generated: set, which changes how its diff shows",
    ]
    (tmp_path / ".gitattributes").write_text("docs/** binary\n")
    assert attribute_problems(tmp_path, paths[:1]) == [
        "docs/decisions/DR-001-a-choice.md has binary: set, which changes how its diff shows",
        "docs/decisions/DR-001-a-choice.md has diff: unset, which changes how its diff shows",
    ]
    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.mkdir()
    with pytest.raises(LookupError, match="git check-attr failed: fatal: not a git repository"):
        attribute_problems(outside, paths)


def test_a_contributor_s_own_attributes_are_not_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    synthetic_repository(tmp_path, [record(1)])
    run_git(tmp_path, "init", "-q", "-b", "main")
    home = tmp_path.parent / f"{tmp_path.name}-home"
    (home / "git").mkdir(parents=True)
    (home / "git" / "attributes").write_text("*.md -diff\n")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home))
    assert attribute_problems(tmp_path, ["docs/decisions/DR-001-a-choice.md"]) == []


def test_an_id_the_default_branch_holds_that_vanishes_is_reported(tmp_path: Path) -> None:
    repository_with_history(tmp_path, [record(1)])
    bases = base_commits(tmp_path, {})
    assert id_problems(tmp_path, *bases) == []
    register = tmp_path / "docs" / "requirements.md"
    register.write_text(register.read_text().replace("- R2, removed by `old`\n", ""))
    model = tmp_path / "docs" / "threat-model.md"
    model.write_text(model.read_text().replace("### T2. Another", "### T4. Another"))
    commit(tmp_path)
    assert id_problems(tmp_path, *bases) == [
        "R2, which docs/requirements.md holds on the default branch, is neither held nor retired",
        "T2, which docs/threat-model.md holds on the default branch, is neither held nor retired",
    ]


def test_an_assumption_id_the_default_branch_holds_stays_held_or_retired(
    tmp_path: Path,
) -> None:
    repository_with_history(tmp_path, [record(1)])
    bases = base_commits(tmp_path, {})
    index = tmp_path / "docs" / "assumptions" / "README.md"
    held = index.read_text()
    index.write_text(held.replace("- A2, removed by `old`\n", "").replace("**A3.**", "**A4.**"))
    commit(tmp_path)
    assert id_problems(tmp_path, *bases) == [
        f"A{each}, which docs/assumptions/README.md holds on the default branch, is neither held"
        " nor retired"
        for each in (2, 3)
    ]
    index.write_text(index.read_text() + "- A2, removed by `old`\n- A3, removed by `demo`\n")
    commit(tmp_path)
    assert id_problems(tmp_path, *bases) == []


def test_an_id_retired_since_is_not_reported(tmp_path: Path) -> None:
    repository_with_history(tmp_path, [record(1)])
    model = tmp_path / "docs" / "threat-model.md"
    text = model.read_text().replace("### T2. Another\n\n- **Held by:** `docs/note.md`\n\n", "")
    model.write_text(text + "- T2, removed by `demo`\n")
    commit(tmp_path)
    assert id_problems(tmp_path, *base_commits(tmp_path, {})) == []


def test_an_id_retired_outside_its_section_is_reported(tmp_path: Path) -> None:
    repository_with_history(tmp_path, [record(1)])
    register = tmp_path / "docs" / "requirements.md"
    entry = "- R2, removed by `old`\n"
    register.write_text(
        register.read_text().replace(f"\n## Retired IDs\n\n{entry}", f"{entry}\n## Retired IDs\n")
    )
    model = tmp_path / "docs" / "threat-model.md"
    model.write_text(model.read_text().replace("### T2. Another", "- T2, removed by `demo`"))
    commit(tmp_path)
    assert id_problems(tmp_path, *base_commits(tmp_path, {})) == [
        "R2, which docs/requirements.md holds on the default branch, is neither held nor retired",
        "T2, which docs/threat-model.md holds on the default branch, is neither held nor retired",
    ]


def test_an_entry_outside_the_section_retires_nothing_on_the_default_branch_either(
    tmp_path: Path,
) -> None:
    repository_with_history(tmp_path, [record(1)])
    register = tmp_path / "docs" / "requirements.md"
    held = register.read_text()
    stray = "- R9, removed by `old`\n"
    register.write_text(held.replace("\n## Retired IDs", f"{stray}\n## Retired IDs"))
    commit(tmp_path)
    run_git(tmp_path, "update-ref", DEFAULT_BRANCH, "HEAD")
    register.write_text(held)
    commit(tmp_path)
    assert id_problems(tmp_path, *base_commits(tmp_path, {})) == []


SPEC = "openspec/changes/demo/specs/thing/spec.md"
SPEC_TEXT = (
    "## ADDED Requirements\n\n"
    "### Requirement: It works\n\nIt SHALL work.\n\n"
    "#### Scenario: It says so\n\n- **WHEN** it runs\n- **THEN** it works\n"
)
LEFT = 'DR-001 quotes "{}", a title that the specs held on the default branch and no longer hold'


def quoting(*titles: str, status: str = "accepted") -> str:
    """A record whose context quotes these titles."""
    quotes = ", ".join(f'"{title}"' for title in titles)
    return record(1, status=status).replace(
        "Something made a choice necessary.", f"Something made a choice necessary: {quotes}."
    )


def spec_repository(root: Path, *titles: str) -> Path:
    """A repository whose `main` holds a spec of one requirement with one scenario, and a
    record that quotes these titles, checked out on a new branch. Returns the spec."""
    spec = root / SPEC
    spec.parent.mkdir(parents=True)
    spec.write_text(SPEC_TEXT)
    repository_with_history(root, [quoting(*titles)])
    return spec


def titles_compared(root: Path) -> tuple[list[str], int]:
    return title_problems(root, *base_commits(root, {}))


def test_a_title_that_a_record_quotes_and_the_specs_keep_is_not_reported(tmp_path: Path) -> None:
    spec_repository(tmp_path, "It works", "It says so", "Not a title")
    assert titles_compared(tmp_path) == ([], 2)


@pytest.mark.parametrize(
    ("title", "old", "new"),
    [
        ("It says so", "Scenario: It says so", "Scenario: It says that"),
        (
            "It says so",
            "#### Scenario: It says so\n\n- **WHEN** it runs\n- **THEN** it works\n",
            "",
        ),
        ("It works", "Requirement: It works", "Requirement: It runs"),
        ("It works", "## ADDED Requirements", "## REMOVED Requirements"),
        ("It says so", "## ADDED Requirements", "## REMOVED Requirements"),
    ],
)
def test_a_title_that_a_record_quotes_changed_or_removed_in_the_specs_is_reported(
    tmp_path: Path, title: str, old: str, new: str
) -> None:
    spec = spec_repository(tmp_path, title)
    spec.write_text(spec.read_text().replace(old, new))
    assert titles_compared(tmp_path) == ([], 1)
    commit(tmp_path)
    assert titles_compared(tmp_path) == ([LEFT.format(title)], 1)


def test_a_title_that_moves_into_openspec_specs_stays_and_one_only_archived_leaves(
    tmp_path: Path,
) -> None:
    spec = spec_repository(tmp_path, "It says so")
    archived = tmp_path / "openspec/changes/archive/2026-01-02-demo/specs/thing/spec.md"
    archived.parent.mkdir(parents=True)
    archived.write_text(SPEC_TEXT)
    held = tmp_path / "openspec/specs/thing/spec.md"
    held.parent.mkdir(parents=True)
    spec.rename(held)
    commit(tmp_path)
    assert titles_compared(tmp_path) == ([], 1)
    held.unlink()
    commit(tmp_path)
    assert titles_compared(tmp_path) == ([LEFT.format("It says so")], 1)


def test_a_title_that_only_a_closed_record_quotes_may_leave_the_specs(tmp_path: Path) -> None:
    spec = spec_repository(tmp_path, "It says so")
    (tmp_path / DECISIONS / "DR-001-a-choice.md").write_text(quoting("It says so", status="closed"))
    spec.write_text(spec.read_text().replace("It says so", "It says that"))
    commit(tmp_path)
    assert titles_compared(tmp_path) == ([], 0)


def test_a_title_after_a_removed_section_stays_in_the_specs(tmp_path: Path) -> None:
    spec = spec_repository(tmp_path, "It says so")
    spec.write_text("## REMOVED Requirements\n\n### Requirement: Gone\n\n" + spec.read_text())
    commit(tmp_path)
    assert titles_compared(tmp_path) == ([], 1)


def test_a_title_that_no_base_held_is_not_compared(tmp_path: Path) -> None:
    spec = spec_repository(tmp_path, "It is new", "It says so")
    spec.write_text(spec.read_text() + "\n#### Scenario: It is new\n\n- **WHEN** it is\n")
    commit(tmp_path)
    assert titles_compared(tmp_path) == ([], 1)
