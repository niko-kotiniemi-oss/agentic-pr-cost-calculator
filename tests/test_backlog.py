"""Planned work is kept as backlog items, and the roadmap is their index.

Each Markdown file in `docs/backlog/` but `README.md` is an item, named
`B-NNN-words.md` and numbered from B-001 with no gap and no repeat; the folder holds
no other file, no folder and no symbolic link. An item opens with `# B-NNN: title`,
its number that of its file, then the fields Status, Last changed, Brief, Rests on,
Issue and Pull requests, each a line `- **Field:** value`, in that order, and then
the sections Problem, What done looks like and Postponed points, each once, in that
order and not empty, with Why it was dropped after them for a dropped item and for no
other. Last changed is a date as `YYYY-MM-DD`; Brief is one to three sentences, a
sentence being text that ends with a stop, a question mark or an exclamation mark
followed by a space or the end; Rests on is `none` or IDs separated by a comma and a
space; Issue is `none` or a number; Pull requests is `none` or numbers separated the
same way (R211, DR-225).

The status is one of five, written as `STATUSES` gives them; an item in progress or
done names a pull request, and a dropped item has its section on why (R207, DR-226).
Rests on names requirements, records, threats, assumptions, other items and tasks,
each of which exists, in active and archived changes alike; no item names a closed
record, and an item that is neither done nor dropped names no tasks that are all
ticked, which would make it stale (R215, T161). Every ID that the roadmap names, in any
section, exists too (T161).

Now, Next and Later give one line for each item that is open to feedback and
contributions, planned or in progress, and none for one that is done or dropped,
each line as `INDEX_LINE` reads it, giving the item's ID, title, status, date and
brief as the item does. Now lists only agreed items, and ends with the line on the
build, which `tests/test_roadmap.py` checks; each item listed under Next or Later
rests on at least one ID (R213). Later opens, before its first line, with the
sentence that `LATER_OPENING` gives, and each record that the README's list of what
the first version does not support links is named in Rests on by an item listed
under Later (R214).

`docs/backlog/README.md` links the roadmap, gives the form, says what an item is and
is not, and what each status means (R217). The README's section on working here
opens, before its setup, its first fenced block, with the statements of
`BRIEFING`, a link to `SECURITY.md` and the table of stages, whose columns and rows
are `COLUMNS` and `ROWS`, each row linking a page; no other tracked Markdown file
gives that table's header, and `CONTRIBUTING.md` and `docs/backlog/README.md` link
the section (R212, DR-229).

Compared with the base commits that `tests/test_decisions.py` uses, read from git's
trees so that a change counts once it is committed: no item that a base holds is
removed, renamed or moved; an item whose text changed gives a later date than the
base's, or the same date when that is the day of the run; no item gives a date after
the day of the run, in UTC (R216). An item that the base does not hold is open to
feedback and contributions or planned, and an item that the base gives as open or
dropped does not become in progress or done (R218, DR-226, T166). A base that does
not hold `docs/backlog/` is not compared, which is the case until the first items
reach the default branch.

Each check is shown to fail on the synthetic tree of `tests/test_roadmap.py`, with
the pages that this test reads added, into which its defect is planted.
"""

from __future__ import annotations

import os
import posixpath
import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from types import ModuleType
from urllib.parse import unquote

import pytest
from test_decisions import base_commits
from test_roadmap import (
    BACKLOG,
    FENCE,
    GIT_ENVIRONMENT,
    LATER_OPENING,
    LIST_MARKER,
    NOT_SUPPORTED,
    RECORD_NAME,
    REGISTER_ROW,
    ROADMAP,
    TARGET,
    THREAT_HEADING,
    TREE,
    index_line,
    make_tree,
    read,
    records,
    section_of,
    sections,
    session_free_environment,
    tasks,
    tracked,
)
from test_roadmap import (
    item as item_text,
)

ROOT = Path(__file__).resolve().parents[1]

STATUSES = ("Open to feedback and contributions", "Planned", "In progress", "Done", "Dropped")
OPEN, PLANNED, IN_PROGRESS, DONE, DROPPED = STATUSES
LISTED = (OPEN, PLANNED, IN_PROGRESS)
AGREED = (PLANNED, IN_PROGRESS)
INDEXED = ("Now", "Next", "Later")
FIELDS = ("Status", "Last changed", "Brief", "Rests on", "Issue", "Pull requests")
SECTIONS = ("Problem", "What done looks like", "Postponed points")
WHY = "Why it was dropped"

PAGE = f"{BACKLOG}/README.md"
PAGE_DESCRIBES = (
    "An item describes: it is neither a promise nor a date, and it is not a request to "
    "start the work."
)
DONE_MEANS = (
    "its pull requests have merged to the default branch, and `CHANGELOG.md` names the "
    "release that holds it"
)

WORKING = "Working on this repository"
WORKING_ANCHOR = "working-on-this-repository"
BRIEFING = (
    "Anyone may open an issue to propose a change, ask a question or report a bug, with "
    "no approval needed.",
    "An issue is public as soon as it is opened, so it holds nothing private",
    "What an issue proposes is neither planned nor committed to.",
    "A backlog item changes only through a pull request that the owner merges.",
)
COLUMNS = ("Step", "Where it lives", "What it holds", "Who writes it")
ROWS = ("An idea or a bug", "Agreed work", "Order", "Delivery", "Result")

ITEM_FILE = re.compile(r"B-(\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md")
ITEM_HEADING = re.compile(r"# (B-\d{3}): (\S.*)")
FIELD = re.compile(r"- \*\*([^*]+):\*\* (.*)")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
SENTENCE_END = re.compile(r"[.?!][)\"']*(?= |$)")
CLOSING = ")\"'"
REST = re.compile(r"R\d+|DR-\d{3}|T\d+|A\d+|B-\d{3}|task (\d+\.\d+) of `([a-z0-9-]+)`")
ISSUE = re.compile(r"none|[1-9]\d*")
PULLS = re.compile(r"none|[1-9]\d*(?:, [1-9]\d*)*")
INDEX_LINE = re.compile(
    r"- \[(B-\d{3}): (.+?)\]\(backlog/(B-\d{3}-[a-z0-9-]+\.md)\) - (.+?), "
    r"last changed (\S+)\. (.+)"
)
ID = re.compile(r"\b(?:DR-\d{3}|B-\d{3}|R\d+|T\d+|A\d+)\b")
ASSUMPTION = re.compile(r"^- \*\*(A\d+)\.\*\* ", re.M)
AUTHOR = {
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.invalid",
}


@dataclass(frozen=True)
class Item:
    path: str
    number: int
    text: str
    fields: dict[str, str] = field(default_factory=dict)

    @property
    def status(self) -> str:
        return self.fields.get("Status", "")

    @property
    def rests(self) -> list[str]:
        value = self.fields.get("Rests on", "none")
        return [] if value == "none" else value.split(", ")

    @property
    def ident(self) -> str:
        return f"B-{self.number:03d}"


def fields_of(text: str) -> dict[str, str]:
    """An item's fields, the first of each name, from the lines before its first section."""
    found: dict[str, str] = {}
    for line in text.split("\n"):
        if line.startswith("## "):
            break
        named = FIELD.fullmatch(line)
        if named:
            found.setdefault(named.group(1), named.group(2))
    return found


def item_from(path: str, text: str) -> Item | None:
    named = ITEM_FILE.fullmatch(path.rsplit("/", 1)[-1])
    return Item(path, int(named.group(1)), text, fields_of(text)) if named else None


def backlog_items(root: Path) -> list[Item]:
    """Each item in the backlog's folder, as its file is named, in the order of its name."""
    found = []
    for path in sorted((root / BACKLOG).glob("B-*.md")):
        if path.is_file() and not path.is_symlink():
            item = item_from(path.relative_to(root).as_posix(), read(path))
            if item:
                found.append(item)
    return found


def sentences(text: str) -> int:
    return len(SENTENCE_END.findall(text)) if text.rstrip(CLOSING)[-1:] in ".?!" else 0


def folder_problems(root: Path) -> list[str]:
    folder = root / BACKLOG
    if not folder.is_dir():
        return [f"{BACKLOG} is missing"]
    problems = []
    for path in sorted(folder.iterdir()):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            problems.append(f"{name} is a symbolic link")
        elif path.is_dir():
            problems.append(f"{name} is a folder")
        elif path.name != "README.md" and not ITEM_FILE.fullmatch(path.name):
            problems.append(f"{name} is neither README.md nor an item named B-NNN-words.md")
    numbers = [item.number for item in backlog_items(root)]
    if not numbers:
        problems.append(f"{BACKLOG} holds no item")
    problems += [
        f"{BACKLOG} gives B-{number:03d} more than once"
        for number in sorted(set(numbers))
        if numbers.count(number) > 1
    ]
    problems += [f"{BACKLOG} gives B-000, below B-001" for number in numbers if number == 0]
    problems += [
        f"{BACKLOG} has no B-{number:03d}, so its numbers have a gap"
        for number in range(1, max(numbers, default=0) + 1)
        if number not in numbers
    ]
    return problems


def item_form_problems(item: Item) -> list[str]:
    lines = item.text.split("\n")
    where = item.path
    problems = []
    heading = ITEM_HEADING.fullmatch(lines[0])
    if not heading or heading.group(1) != item.ident:
        problems.append(f"{where} does not open with its heading, # {item.ident}: and its title")
    preamble = []
    for number, line in enumerate(lines[1:], 2):
        if line.startswith("## "):
            break
        if line.strip():
            preamble.append((number, line))
    names = []
    for number, line in preamble:
        named = FIELD.fullmatch(line)
        if named:
            names.append(named.group(1))
        else:
            problems.append(f"{where}:{number} holds a line before its sections that is no field")
    if names != list(FIELDS):
        problems.append(
            f"{where} gives its fields as {', '.join(names) or 'none'}, not {', '.join(FIELDS)}"
        )
    values = item.fields
    changed = values.get("Last changed", "")
    if "Last changed" in values and not is_date(changed):
        problems.append(f"{where} gives {changed!r} in Last changed, which is not a date")
    brief = values.get("Brief")
    if brief is not None and not 1 <= sentences(brief) <= 3:
        problems.append(f"{where} gives a brief that is not one to three sentences")
    rests = values.get("Rests on")
    if (
        rests is not None
        and rests != "none"
        and not all(REST.fullmatch(name) for name in rests.split(", "))
    ):
        problems.append(f"{where} gives Rests on in a form other than none or IDs")
    for name, form in (("Issue", ISSUE), ("Pull requests", PULLS)):
        value = values.get(name)
        if value is not None and not form.fullmatch(value):
            problems.append(f"{where} gives {name} in a form other than none or numbers")
    found = [(heading, body) for heading, _, body in sections(item.text)]
    titles = [heading for heading, _ in found]
    if titles not in (list(SECTIONS), [*SECTIONS, WHY]) or (
        WHY in titles and item.status != DROPPED
    ):
        problems.append(
            f"{where} gives its sections as {', '.join(titles) or 'none'}, not "
            f"{', '.join(SECTIONS)}, with {WHY} after them only for a dropped item"
        )
    problems += [
        f"{where} has an empty section {heading}"
        for heading, body in found
        if not "".join(body).strip()
    ]
    return problems


def is_date(text: str) -> bool:
    if not DATE.fullmatch(text):
        return False
    try:
        date.fromisoformat(text)
    except ValueError:
        return False
    return True


def form_problems(root: Path) -> list[str]:
    problems = folder_problems(root)
    for item in backlog_items(root):
        problems += item_form_problems(item)
    return problems


def status_problems(root: Path) -> list[str]:
    problems = []
    for item in backlog_items(root):
        status = item.status
        if status not in STATUSES:
            problems.append(f"{item.path} gives the status {status!r}, which is not one of five")
        if status in (IN_PROGRESS, DONE) and item.fields.get("Pull requests") == "none":
            problems.append(f"{item.path} is {status} and names no pull request")
        if status == DROPPED and WHY not in [heading for heading, _, _ in sections(item.text)]:
            problems.append(f"{item.path} is dropped and does not say why")
    return problems


def holders(root: Path) -> dict[str, tuple[set[str], str]]:
    """Each kind of ID, by its prefix, with the IDs that exist and where they are held."""
    files = (
        ("R", REGISTER_ROW, "docs/requirements.md", "the register"),
        ("T", THREAT_HEADING, "docs/threat-model.md", "the threat model"),
        ("A", ASSUMPTION, "docs/assumptions/README.md", "docs/assumptions/"),
    )
    found = {
        prefix: (set(pattern.findall(read(root / path))), holder)
        for prefix, pattern, path, holder in files
    }
    found["DR-"] = (set(records(root)), "docs/decisions/")
    found["B-"] = ({item.ident for item in backlog_items(root)}, BACKLOG)
    return found


def holder_of(name: str, held: dict[str, tuple[set[str], str]]) -> tuple[set[str], str]:
    prefix = name[:3] if name.startswith("DR-") else name[:2] if name[1] == "-" else name[0]
    return held[prefix]


def rest_problems(
    where: str,
    name: str,
    held: dict[str, tuple[set[str], str]],
    closed: dict[str, bool],
    listed: dict[tuple[str, str], bool],
) -> list[str]:
    """What is wrong with one name of a Rests on that is in its form: a task that no
    change's tasks.md holds, an ID that its holder does not hold, or a closed record."""
    form = REST.fullmatch(name)
    if not form:
        return []
    if form.group(1):
        if (form.group(2), form.group(1)) not in listed:
            return [f"{where} names {name}, which no change's tasks.md holds"]
        return []
    idents, holder = holder_of(name, held)
    if name not in idents:
        return [f"{where} names {name}, which {holder} does not hold"]
    if closed.get(name):
        return [f"{where} names {name}, which is closed"]
    return []


def name_problems(root: Path) -> list[str]:
    held = holders(root)
    closed = records(root)
    listed = tasks(root)
    problems = []
    for item in backlog_items(root):
        named_tasks = []
        for name in item.rests:
            form = REST.fullmatch(name)
            if form and form.group(1):
                named_tasks.append((form.group(2), form.group(1)))
            problems += rest_problems(item.path, name, held, closed, listed)
        if (
            item.status not in (DONE, DROPPED)
            and named_tasks
            and all(listed.get(task, False) for task in named_tasks)
        ):
            problems.append(f"{item.path} is {item.status} and names only finished tasks")
    return problems


def roadmap_name_problems(root: Path) -> list[str]:
    """Every ID that the roadmap names, in any section, exists (T161)."""
    held = holders(root)
    problems = []
    for number, line in enumerate(read(root / ROADMAP).split("\n"), 1):
        for name in ID.findall(line):
            idents, holder = holder_of(name, held)
            if name not in idents:
                problems.append(f"{ROADMAP}:{number} names {name}, which {holder} does not hold")
    return problems


@dataclass(frozen=True)
class Line:
    section: str
    number: int
    ident: str
    title: str
    path: str
    status: str
    changed: str
    brief: str


def index_lines(root: Path) -> tuple[list[Line], list[str]]:
    """The lines of the index under Now, Next and Later, and the problems of their form."""
    text = read(root / ROADMAP)
    found = []
    problems = []
    for name in INDEXED:
        start, lines = section_of(text, name)
        if name == "Now":
            # The line on the build closes Now, and the roadmap's test holds it.
            last = max((i for i, line in enumerate(lines) if line.strip()), default=-1)
            if last >= 0 and not lines[last].startswith("- "):
                lines = [line if i != last else "" for i, line in enumerate(lines)]
        begun = False
        for offset, line in enumerate(lines):
            where = f"{ROADMAP}:{start + offset}"
            if line.startswith("- "):
                begun = True
                read_line = INDEX_LINE.fullmatch(line)
                if read_line:
                    found.append(Line(name, start + offset, *read_line.groups()))
                else:
                    problems.append(f"{where} is not a line of the index, as an item gives it")
            elif LIST_MARKER.match(line):
                problems.append(f"{where} gives a list item under {name} in a form other than `- `")
            elif begun and line.strip():
                problems.append(
                    f"{where} holds a line under {name} after its first item that is no item"
                )
    return found, problems


def index_problems(root: Path) -> list[str]:
    lines, problems = index_lines(root)
    items = {item.path.rsplit("/", 1)[-1]: item for item in backlog_items(root)}
    counts: dict[str, int] = {}
    for line in lines:
        where = f"{ROADMAP}:{line.number}"
        item = items.get(line.path)
        if item is None:
            problems.append(f"{where} links {line.path}, which is no backlog item")
            continue
        counts[line.path] = counts.get(line.path, 0) + 1
        given = (line.ident, line.title, line.status, line.changed, line.brief)
        heading = ITEM_HEADING.fullmatch(item.text.split("\n")[0])
        held = (
            item.ident,
            heading.group(2) if heading else None,
            item.status,
            item.fields.get("Last changed"),
            item.fields.get("Brief"),
        )
        differ = [
            what
            for what, mine, theirs in zip(
                ("ID", "title", "status", "date", "brief"), given, held, strict=True
            )
            if mine != theirs
        ]
        if differ:
            problems.append(f"{where} gives a {', '.join(differ)} that differs from its item's")
        if line.section == "Now" and item.status not in AGREED:
            problems.append(f"{where} lists {item.ident} under Now, which is {item.status}")
        if line.section != "Now" and not item.rests:
            problems.append(
                f"{where} lists {item.ident} under {line.section}, which rests on nothing"
            )
    for name, item in items.items():
        count = counts.get(name, 0)
        if item.status in LISTED and count == 0:
            problems.append(
                f"{item.path} is {item.status} and is listed in none of Now, Next and Later"
            )
        elif item.status in LISTED and count > 1:
            problems.append(f"{item.path} is listed more than once")
        elif item.status not in LISTED and count:
            problems.append(f"{item.path} is {item.status} and is still listed")
    return problems


def later_problems(root: Path) -> list[str]:
    _, lines = section_of(read(root / ROADMAP), "Later")
    opening = []
    for line in lines:
        if line.startswith("- "):
            break
        opening.append(line.strip())
    problems = []
    if LATER_OPENING not in " ".join(opening):
        problems.append(f"{ROADMAP}: Later does not open with how work on an item starts")
    items = {item.path.rsplit("/", 1)[-1]: item for item in backlog_items(root)}
    named = {
        name
        for line in index_lines(root)[0]
        if line.section == "Later" and line.path in items
        for name in items[line.path].rests
    }
    _, unsupported = section_of(read(root / "README.md"), NOT_SUPPORTED)
    linked = sorted(set(RECORD_NAME.findall("\n".join(unsupported))))
    if not linked:
        problems.append(
            "README.md's list of what the first version does not support links no record"
        )
    problems += [
        f"no item listed under Later names {ident} in Rests on, which the README's list of "
        "what the first version does not support links"
        for ident in linked
        if ident not in named
    ]
    return problems


def page_problems(root: Path) -> list[str]:
    path = root / PAGE
    if not path.is_file():
        return [f"{PAGE} is missing"]
    text = read(path)
    flat = " ".join(line.strip() for line in text.split("\n"))
    problems = []
    if "../roadmap.md" not in [target.split("#")[0] for target in TARGET.findall(text)]:
        problems.append(f"{PAGE} does not link the roadmap")
    if PAGE_DESCRIBES not in flat:
        problems.append(f"{PAGE} does not say what an item is and is not")
    problems += [
        f"{PAGE} does not give {name} in an item's form"
        for name in (*FIELDS, *SECTIONS, WHY)
        if f"**{name}" not in text
    ]
    lines = text.split("\n")
    for status in STATUSES:
        meant = [line for line in lines if line.startswith(f"- **{status}**: ")]
        if not meant:
            problems.append(f"{PAGE} does not say what {status} means")
        elif status == DONE and DONE_MEANS not in meant[0]:
            problems.append(f"{PAGE} does not say that Done means merged, with the release")
    return problems


def links_to_the_section(root: Path, name: str) -> bool:
    folder = posixpath.dirname(name)
    for target in TARGET.findall(read(root / name)):
        path, _, fragment = unquote(target).partition("#")
        if posixpath.normpath(posixpath.join(folder, path)) == "README.md" and (
            fragment == WORKING_ANCHOR
        ):
            return True
    return False


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def briefing_problems(root: Path) -> list[str]:
    _, lines = section_of(read(root / "README.md"), WORKING)
    if not lines:
        return [f"README.md has no section {WORKING}"]
    setup = next((i for i, line in enumerate(lines) if FENCE.match(line)), len(lines))
    briefing = lines[:setup]
    flat = " ".join(line.strip() for line in briefing)
    problems = [
        f"README.md's briefing, before its setup, does not say: {statement}"
        for statement in BRIEFING
        if statement not in flat
    ]
    if "](SECURITY.md)" not in flat:
        problems.append("README.md's briefing does not send a security problem to SECURITY.md")
    table = [line for line in briefing if line.startswith("|")]
    if not table:
        problems.append("README.md's briefing has no table of stages")
    else:
        if cells(table[0]) != list(COLUMNS):
            problems.append(
                f"README.md's table of stages gives the columns {', '.join(cells(table[0]))}, "
                f"not {', '.join(COLUMNS)}"
            )
        rows = table[2:]
        firsts = [cells(row)[0] for row in rows]
        if firsts != list(ROWS):
            problems.append(
                f"README.md's table of stages gives the rows {', '.join(firsts)}, "
                f"not {', '.join(ROWS)}"
            )
        problems += [
            f"README.md's table of stages has a row {cells(row)[0]} that links no page"
            for row in rows
            if "](" not in row
        ]
    for name in sorted(tracked(root)):
        if not name.endswith(".md") or name == "README.md":
            continue
        problems += [
            f"{name}:{number} gives the header of the README's table of stages, "
            "whose one home is the README"
            for number, line in enumerate(read(root / name).split("\n"), 1)
            if "|" in line and cells(line.lstrip(" >")) == list(COLUMNS)
        ]
    problems += [
        f"{name} does not link the README's section {WORKING}"
        for name in ("CONTRIBUTING.md", PAGE)
        if not links_to_the_section(root, name)
    ]
    return problems


def git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        check=False,
        env={**session_free_environment(), **GIT_ENVIRONMENT, **AUTHOR},
    )


def items_in(root: Path, commit: str) -> dict[str, Item]:
    """The items that a commit holds, by path.

    Raises LookupError when git cannot list the commit's files or read one of them."""
    listing = git(root, "ls-tree", "-r", "-z", "--name-only", commit, f"{BACKLOG}/")
    if listing.returncode != 0:
        raise LookupError(f"cannot list the files of {commit}")
    found = {}
    for path in listing.stdout.decode("utf-8").split("\0"):
        if not path:
            continue
        shown = git(root, "show", f"{commit}:{path}")
        if shown.returncode != 0:
            raise LookupError(f"cannot read {path} in {commit}")
        item = item_from(path, shown.stdout.decode("utf-8"))
        if item:
            found[path] = item
    return found


def history_problems(root: Path, *bases: str, today: date) -> list[str]:
    problems: dict[str, None] = {}
    for item in backlog_items(root):
        changed = item.fields.get("Last changed", "")
        if is_date(changed) and date.fromisoformat(changed) > today:
            problems[f"{item.path} gives {changed}, after the day of the run, {today}"] = None
    now = items_in(root, "HEAD") if bases else {}
    for base in bases:
        if git(root, "cat-file", "-e", f"{base}:{BACKLOG}").returncode != 0:
            continue
        before = items_in(root, base)
        for path, old in sorted(before.items()):
            new = now.get(path)
            if new is None:
                problems[f"{path}, which a base commit holds, was removed, renamed or moved"] = None
                continue
            was, given = old.fields.get("Last changed", ""), new.fields.get("Last changed", "")
            if new.text != old.text and is_date(was) and is_date(given):
                later = date.fromisoformat(given) > date.fromisoformat(was)
                same_day = given == was == today.isoformat()
                if not (later or same_day):
                    problems[
                        f"{path} was changed and gives {given} in Last changed, not a later "
                        f"date than the base's {was}"
                    ] = None
            if old.status in (OPEN, DROPPED) and new.status in (IN_PROGRESS, DONE):
                problems[
                    f"{path} moved from {old.status} to {new.status}, which skips agreement"
                ] = None
        for path, new in sorted(now.items()):
            if path not in before and new.status not in (OPEN, PLANNED):
                problems[
                    f"{path} was added as {new.status}, where an item is added only as "
                    f"{OPEN} or {PLANNED}"
                ] = None
    return list(problems)


def backlog_problems(root: Path) -> list[str]:
    return (
        form_problems(root)
        + status_problems(root)
        + name_problems(root)
        + roadmap_name_problems(root)
        + index_problems(root)
        + later_problems(root)
        + page_problems(root)
        + briefing_problems(root)
    )


def test_the_repository_has_no_backlog_problem() -> None:
    assert backlog_problems(ROOT) == []


def test_the_repository_has_no_problem_against_its_base() -> None:
    today = datetime.now(UTC).date()
    assert history_problems(ROOT, *base_commits(ROOT, os.environ), today=today) == []


def test_the_repository_gives_each_check_something_to_examine() -> None:
    """A check that examined nothing fails."""
    items = backlog_items(ROOT)
    assert items
    lines, _ = index_lines(ROOT)
    assert {line.section for line in lines} == set(INDEXED)
    assert {item.status for item in items} & set(LISTED)
    _, unsupported = section_of(read(ROOT / "README.md"), NOT_SUPPORTED)
    assert RECORD_NAME.findall("\n".join(unsupported))


# The synthetic tree of the roadmap's test, with the pages that this test reads.

BRIEFED = (
    "# A tool\n\n"
    f"## {NOT_SUPPORTED}\n\n"
    "- Other agents ([DR-003](docs/decisions/DR-003-c.md)).\n\n"
    "## Documentation\n\n"
    f"- [Roadmap]({ROADMAP}): what is now, next and later.\n\n"
    f"## {WORKING}\n\n"
    f"{BRIEFING[0]} {BRIEFING[1]}, and a security problem goes to\n"
    f"[the security page](SECURITY.md) instead. {BRIEFING[2]} {BRIEFING[3]}\n\n"
    f"| {' | '.join(COLUMNS)} |\n"
    "| --- | --- | --- | --- |\n"
    + "".join(f"| {row} | [a page]({ROADMAP}) | what | who |\n" for row in ROWS)
    + "\nSetup for a local clone:\n\n```sh\nmake\n```\n"
)
EXTRA = {
    "README.md": BRIEFED,
    "CONTRIBUTING.md": f"# Contributing\n\nSee [how work flows](README.md#{WORKING_ANCHOR}).\n",
    PAGE: (
        "# Backlog\n\n"
        f"{PAGE_DESCRIBES} The [roadmap](../roadmap.md) is their index, and\n"
        f"[how work flows](../../README.md#{WORKING_ANCHOR}) says the rest.\n\n"
        + "".join(f"- **{name}:** what it gives.\n" for name in FIELDS)
        + "".join(f"- **{name}**: what it says.\n" for name in (*SECTIONS, WHY))
        + "\n"
        + "".join(
            f"- **{status}**: {DONE_MEANS if status == DONE else 'what it means'}.\n"
            for status in STATUSES
        )
    ),
}
WHOLE = {**TREE, **EXTRA}
ITEM = f"{BACKLOG}/B-001-a-thing.md"
DROPPED_ITEM = f"{BACKLOG}/B-005-a-dropped-thing.md"
TODAY = date(2026, 1, 1)


def build(root: Path, changed: dict[str, str | None] | None = None) -> Path:
    return make_tree(root, {**EXTRA, **(changed or {})})


def plant(root: Path, name: str, old: str, new: str) -> Path:
    text = WHOLE[name]
    assert text.count(old) == 1, old
    return build(root, {name: text.replace(old, new)})


def test_a_complete_tree_has_no_problem(tmp_path: Path) -> None:
    root = build(tmp_path)
    assert backlog_problems(root) == []
    assert history_problems(root, today=TODAY) == []


FORM = [
    ("# B-001: A thing", "# B-002: A thing", "does not open with its heading"),
    ("# B-001: A thing", "B-001: A thing", "does not open with its heading"),
    ("# B-001: A thing", "# B-001 A thing", "does not open with its heading"),
    ("- **Status:** Planned\n", "", "gives its fields as Last changed"),
    (
        "- **Issue:** none\n",
        "- **Issue:** none\n- **Issue:** none\n",
        "gives its fields as Status, Last changed, Brief, Rests on, Issue, Issue",
    ),
    (
        "- **Status:** Planned\n- **Last changed:** 2026-01-01\n",
        "- **Last changed:** 2026-01-01\n- **Status:** Planned\n",
        "gives its fields as Last changed, Status",
    ),
    ("- **Brief:**", "- **Brief**:", "holds a line before its sections that is no field"),
    ("2026-01-01", "1 January 2026", "gives '1 January 2026' in Last changed, which is not"),
    ("2026-01-01", "2026-02-30", "gives '2026-02-30' in Last changed, which is not a date"),
    ("A thing to build first.", "A thing. To. Build. First.", "gives a brief that is not one"),
    ("A thing to build first.", "A thing to build first", "gives a brief that is not one"),
    (
        "A thing to build first.",
        'A thing (built first.) And more (later.) Again "so." Not.',
        "gives a brief",
    ),
    ("R1, task 1.1 of `c`", "R1 and task 1.1 of `c`", "gives Rests on in a form other"),
    ("R1, task 1.1 of `c`", "R1,task 1.1 of `c`", "gives Rests on in a form other"),
    ("R1, task 1.1 of `c`", "", "gives Rests on in a form other"),
    ("- **Issue:** none", "- **Issue:** #3", "gives Issue in a form other"),
    ("- **Pull requests:** 7", "- **Pull requests:** 7 and 8", "gives Pull requests in a form"),
    ("## Problem\n\nWhy it matters.\n\n", "", "gives its sections as What done looks like"),
    (
        "## Postponed points\n\nNone.\n",
        "## Postponed points\n\nNone.\n\n## Problem\n\nAgain.\n",
        "gives its sections as Problem, What done looks like, Postponed points, Problem",
    ),
    (
        "## Postponed points\n\nNone.\n",
        f"## Postponed points\n\nNone.\n\n## {WHY}\n\nNo reason.\n",
        f"gives its sections as Problem, What done looks like, Postponed points, {WHY}",
    ),
    ("## Problem\n\nWhy it matters.\n\n", "## Problem\n\n", "has an empty section Problem"),
]


@pytest.mark.parametrize(("old", "new", "problem"), FORM)
def test_an_item_out_of_form_is_reported(tmp_path: Path, old: str, new: str, problem: str) -> None:
    found = form_problems(plant(tmp_path, ITEM, old, new))
    assert [p for p in found if p.startswith(ITEM) and problem in p], found


@pytest.mark.parametrize(
    "brief", ["A thing (to build first.)", 'A thing "to build first."', "Why? Because. So!"]
)
def test_a_brief_whose_stop_stands_inside_a_closing_mark_passes(tmp_path: Path, brief: str) -> None:
    root = build(tmp_path, {ITEM: WHOLE[ITEM].replace("A thing to build first.", brief)})
    assert [p for p in form_problems(root) if "brief" in p] == []


def test_a_dropped_item_may_say_why(tmp_path: Path) -> None:
    root = plant(tmp_path, DROPPED_ITEM, f"## {WHY}", f"## {WHY}")
    assert form_problems(root) == [] and status_problems(root) == []


@pytest.mark.parametrize(
    ("changed", "problem"),
    [
        ({f"{BACKLOG}/notes.txt": "x\n"}, f"{BACKLOG}/notes.txt is neither README.md nor"),
        ({f"{BACKLOG}/B-6-x.md": "x\n"}, f"{BACKLOG}/B-6-x.md is neither README.md nor"),
        ({f"{BACKLOG}/B-006-X.md": "x\n"}, f"{BACKLOG}/B-006-X.md is neither README.md nor"),
        ({f"{BACKLOG}/sub/README.md": "x\n"}, f"{BACKLOG}/sub is a folder"),
        ({f"{BACKLOG}/B-007-x.md": WHOLE[ITEM]}, f"{BACKLOG} has no B-006, so its numbers"),
        ({f"{BACKLOG}/B-005-again.md": WHOLE[ITEM]}, f"{BACKLOG} gives B-005 more than once"),
        ({f"{BACKLOG}/B-000-zero.md": WHOLE[ITEM]}, f"{BACKLOG} gives B-000, below B-001"),
    ],
)
def test_the_folder_out_of_form_is_reported(
    tmp_path: Path, changed: dict[str, str | None], problem: str
) -> None:
    found = folder_problems(build(tmp_path, changed))
    assert [p for p in found if p.startswith(problem)], found


def test_a_symbolic_link_in_the_folder_is_reported(tmp_path: Path) -> None:
    root = build(tmp_path)
    (root / BACKLOG / "B-006-link.md").symlink_to(root / ITEM)
    assert folder_problems(root) == [f"{BACKLOG}/B-006-link.md is a symbolic link"]


def test_a_missing_folder_or_one_with_no_item_is_reported(tmp_path: Path) -> None:
    root = build(tmp_path / "a", {name: None for name in WHOLE if name.startswith(BACKLOG)})
    assert folder_problems(root) == [f"{BACKLOG} is missing"]
    root = build(tmp_path / "b", {name: None for name in WHOLE if name.startswith(f"{BACKLOG}/B-")})
    assert folder_problems(root) == [f"{BACKLOG} holds no item"]


@pytest.mark.parametrize(
    ("name", "old", "new", "problem"),
    [
        (ITEM, "Planned", "Planned.", "gives the status 'Planned.', which is not one of five"),
        (ITEM, "Planned", "Agreed", "gives the status 'Agreed', which is not one of five"),
        (ITEM, "Planned", "planned", "gives the status 'planned', which is not one of five"),
        (
            f"{BACKLOG}/B-004-a-done-thing.md",
            "- **Pull requests:** 5, 6",
            "- **Pull requests:** none",
            "is Done and names no pull request",
        ),
        (
            ITEM,
            "Planned\n- **Last changed:** 2026-01-01\n- **Brief:** A thing to build first.\n"
            "- **Rests on:** R1, task 1.1 of `c`\n- **Issue:** none\n- **Pull requests:** 7",
            "In progress\n- **Last changed:** 2026-01-01\n- **Brief:** A thing to build first.\n"
            "- **Rests on:** R1, task 1.1 of `c`\n- **Issue:** none\n- **Pull requests:** none",
            "is In progress and names no pull request",
        ),
        (DROPPED_ITEM, f"\n## {WHY}\n\nNobody needs it.\n", "", "is dropped and does not say why"),
    ],
)
def test_an_item_without_its_status_is_reported(
    tmp_path: Path, name: str, old: str, new: str, problem: str
) -> None:
    assert status_problems(plant(tmp_path, name, old, new)) == [f"{name} {problem}"]


@pytest.mark.parametrize(
    ("old", "new", "problem"),
    [
        ("R1, task", "R9, task", "names R9, which the register does not hold"),
        ("R1, task", "DR-009, task", "names DR-009, which docs/decisions/ does not hold"),
        ("R1, task", "T9, task", "names T9, which the threat model does not hold"),
        ("R1, task", "A9, task", "names A9, which docs/assumptions/ does not hold"),
        ("R1, task", "B-009, task", f"names B-009, which {BACKLOG} does not hold"),
        (
            "task 1.1 of `c`",
            "task 9.9 of `c`",
            "names task 9.9 of `c`, which no change's tasks.md holds",
        ),
        (
            "task 1.1 of `c`",
            "task 2.1 of `c`",
            "names task 2.1 of `c`, which no change's tasks.md holds",
        ),
        ("R1, task", "DR-002, task", "names DR-002, which is closed"),
        ("task 1.1 of `c`", "task 1.2 of `c`", "is Planned and names only finished tasks"),
        (
            "task 1.1 of `c`",
            "task 1.2 of `c`, task 2.1 of `old`",
            "is Planned and names only finished tasks",
        ),
    ],
)
def test_an_item_that_names_what_does_not_hold_is_reported(
    tmp_path: Path, old: str, new: str, problem: str
) -> None:
    assert name_problems(plant(tmp_path, ITEM, old, new)) == [f"{ITEM} {problem}"]


def test_names_in_an_archived_change_and_a_finished_done_item_pass(tmp_path: Path) -> None:
    root = plant(tmp_path, ITEM, "task 1.1 of `c`", "task 1.1 of `c`, task 2.1 of `old`")
    assert name_problems(root) == []


LINE_1 = "- [B-001: A thing](backlog/B-001-a-thing.md) - Planned, last changed 2026-01-01."


@pytest.mark.parametrize(
    ("old", "new", "problem"),
    [
        ("[B-001: A thing]", "[B-001: A thing!]", ":9 gives a title that differs from its item's"),
        ("[B-001: A thing]", "[B-002: A thing]", ":9 gives a ID that differs from its item's"),
        (
            "- Planned, last changed 2026-01-01. A thing",
            "- In progress, last changed 2026-01-02. A thing",
            ":9 gives a status, date that differs from its item's",
        ),
        ("A thing to build first.", "A thing to build.", ":9 gives a brief that differs"),
        (LINE_1, LINE_1.replace(" - ", " -- ", 1), ":9 is not a line of the index"),
        (LINE_1, LINE_1.replace("](backlog/", "](../docs/backlog/"), ":9 is not a line of"),
        (
            "B-001-a-thing.md) - Planned",
            "B-009-a-thing.md) - Planned",
            ":9 links B-009-a-thing.md, which is no backlog item",
        ),
        ("What is under way.", "* What is under way.", ":7 gives a list item under Now in a"),
        ("What follows.\n", "What follows.\n\n1. More.\n", ":17 gives a list item under Next"),
        (
            "## Later",
            "Another thing, as DR-001 says.\n\n## Later",
            ":19 holds a line under Next after its first item that is no item",
        ),
    ],
)
def test_a_line_that_differs_from_its_item_is_reported(
    tmp_path: Path, old: str, new: str, problem: str
) -> None:
    found = index_problems(plant(tmp_path, ROADMAP, old, new))
    assert [p for p in found if p.startswith(f"{ROADMAP}{problem}")], found


def test_now_without_its_line_on_the_build_still_reads_its_last_item(tmp_path: Path) -> None:
    build_line = next(
        line for line in WHOLE[ROADMAP].split("\n") if line.startswith("Then the build")
    )
    root = plant(tmp_path, ROADMAP, f"{build_line}\n\n", "")
    assert index_problems(root) == []
    text = WHOLE[ROADMAP].replace(f"{build_line}\n\n", "").replace("first.\n", "first!\n", 1)
    root = build(tmp_path / "other", {ROADMAP: text})
    assert index_problems(root) == [f"{ROADMAP}:9 gives a brief that differs from its item's"]


def test_the_roadmap_names_only_what_exists(tmp_path: Path) -> None:
    root = plant(tmp_path, ROADMAP, "None yet.", "- A bug that R99, DR-009, T9, A9 and B-009 hold.")
    assert roadmap_name_problems(root) == [
        f"{ROADMAP}:34 names R99, which the register does not hold",
        f"{ROADMAP}:34 names DR-009, which docs/decisions/ does not hold",
        f"{ROADMAP}:34 names T9, which the threat model does not hold",
        f"{ROADMAP}:34 names A9, which docs/assumptions/ does not hold",
        f"{ROADMAP}:34 names B-009, which {BACKLOG} does not hold",
    ]


def test_the_roadmap_names_what_exists(tmp_path: Path) -> None:
    root = plant(tmp_path, ROADMAP, "None yet.", "A bug that R1, DR-001, T1, A1 and B-005 hold.")
    assert roadmap_name_problems(root) == []


def test_a_line_on_the_build_written_as_an_item_is_reported(tmp_path: Path) -> None:
    root = plant(tmp_path, ROADMAP, "Then the build", "- Then the build")
    assert index_problems(root) == [f"{ROADMAP}:11 is not a line of the index, as an item gives it"]


def test_an_open_item_missing_or_listed_twice_is_reported(tmp_path: Path) -> None:
    text = WHOLE[ROADMAP]
    line_2 = next(line for line in text.split("\n") if line.startswith("- [B-002"))
    root = build(tmp_path / "a", {ROADMAP: text.replace(f"{line_2}\n", "")})
    assert index_problems(root) == [
        f"{BACKLOG}/B-002-another-thing.md is Open to feedback and contributions and is "
        "listed in none of Now, Next and Later"
    ]
    root = build(tmp_path / "b", {ROADMAP: text.replace(line_2, f"{line_2}\n{line_2}")})
    assert index_problems(root) == [f"{BACKLOG}/B-002-another-thing.md is listed more than once"]


@pytest.mark.parametrize(
    "name", [f"{BACKLOG}/B-004-a-done-thing.md", f"{BACKLOG}/B-005-a-dropped-thing.md"]
)
def test_a_done_or_dropped_item_still_listed_is_reported(tmp_path: Path, name: str) -> None:
    status = DONE if "done" in name else DROPPED
    line = index_line(name)
    root = plant(tmp_path, ROADMAP, "What follows.\n", f"What follows.\n\n{line}\n")
    assert index_problems(root) == [f"{name} is {status} and is still listed"]


def test_an_item_under_now_that_is_not_agreed_is_reported(tmp_path: Path) -> None:
    root = build(
        tmp_path,
        {
            ITEM: WHOLE[ITEM].replace("Planned", OPEN),
            ROADMAP: WHOLE[ROADMAP].replace(
                "- Planned, last changed", f"- {OPEN}, last changed", 1
            ),
        },
    )
    assert index_problems(root) == [f"{ROADMAP}:9 lists B-001 under Now, which is {OPEN}"]


def test_an_item_under_next_or_later_that_rests_on_nothing_is_reported(tmp_path: Path) -> None:
    root = plant(tmp_path, f"{BACKLOG}/B-002-another-thing.md", "T1, A1, B-001", "none")
    assert index_problems(root) == [f"{ROADMAP}:17 lists B-002 under Next, which rests on nothing"]


def test_an_item_under_now_may_rest_on_nothing(tmp_path: Path) -> None:
    root = plant(tmp_path, ITEM, "R1, task 1.1 of `c`", "none")
    assert index_problems(root) == []


def test_later_without_its_opening_is_reported(tmp_path: Path) -> None:
    root = plant(tmp_path, ROADMAP, f"{LATER_OPENING}\n\n", "")
    assert later_problems(root) == [
        f"{ROADMAP}: Later does not open with how work on an item starts"
    ]


def test_the_later_opening_must_come_before_the_first_item(tmp_path: Path) -> None:
    text = WHOLE[ROADMAP].replace(f"{LATER_OPENING}\n\n", "")
    text = text.replace("## Known limitations", f"{LATER_OPENING}\n\n## Known limitations")
    assert later_problems(build(tmp_path, {ROADMAP: text})) == [
        f"{ROADMAP}: Later does not open with how work on an item starts"
    ]


def test_a_record_the_readme_leaves_out_and_later_does_not_name_is_reported(
    tmp_path: Path,
) -> None:
    root = plant(tmp_path, f"{BACKLOG}/B-003-other-agents.md", "DR-003, DR-001", "DR-001")
    assert later_problems(root) == [
        "no item listed under Later names DR-003 in Rests on, which the README's list of "
        "what the first version does not support links"
    ]


def test_a_record_named_only_in_the_brief_or_under_next_does_not_count(tmp_path: Path) -> None:
    root = build(
        tmp_path,
        {
            f"{BACKLOG}/B-003-other-agents.md": WHOLE[f"{BACKLOG}/B-003-other-agents.md"]
            .replace("DR-003, DR-001", "DR-001")
            .replace("Agents other than one.", "Agents other than one, as DR-003 says."),
            f"{BACKLOG}/B-002-another-thing.md": WHOLE[f"{BACKLOG}/B-002-another-thing.md"].replace(
                "T1, A1, B-001", "DR-003"
            ),
        },
    )
    assert later_problems(root) == [
        "no item listed under Later names DR-003 in Rests on, which the README's list of "
        "what the first version does not support links"
    ]


def test_a_readme_whose_list_links_no_record_is_reported(tmp_path: Path) -> None:
    root = plant(tmp_path, "README.md", f"## {NOT_SUPPORTED}", "## Not supported yet")
    assert later_problems(root) == [
        "README.md's list of what the first version does not support links no record"
    ]


@pytest.mark.parametrize(
    ("old", "new", "problem"),
    [
        ("The [roadmap](../roadmap.md) is", "The roadmap is", "does not link the roadmap"),
        (PAGE_DESCRIBES, "An item describes.", "does not say what an item is and is not"),
        ("- **Brief:** what", "- Brief: what", "does not give Brief in an item's form"),
        (f"- **{WHY}**: what", f"- {WHY}: what", f"does not give {WHY} in an item's form"),
        (f"- **{PLANNED}**: ", f"- {PLANNED}: ", f"does not say what {PLANNED} means"),
        (f"- **{OPEN}**: ", f"- **{OPEN}.**: ", f"does not say what {OPEN} means"),
        (DONE_MEANS, "it is done", "does not say that Done means merged, with the release"),
    ],
)
def test_a_backlog_page_that_leaves_one_out_is_reported(
    tmp_path: Path, old: str, new: str, problem: str
) -> None:
    assert page_problems(plant(tmp_path, PAGE, old, new)) == [f"{PAGE} {problem}"]


def test_a_missing_backlog_page_is_reported(tmp_path: Path) -> None:
    assert page_problems(build(tmp_path, {PAGE: None})) == [f"{PAGE} is missing"]


@pytest.mark.parametrize(
    ("old", "new", "problem"),
    [
        (BRIEFING[0], "Open an issue.", f"does not say: {BRIEFING[0]}"),
        (BRIEFING[1], "An issue is public", f"does not say: {BRIEFING[1]}"),
        (BRIEFING[2], "", f"does not say: {BRIEFING[2]}"),
        (BRIEFING[3], "", f"does not say: {BRIEFING[3]}"),
        ("[the security page](SECURITY.md)", "the security page", "does not send a security"),
        ("| Step | Where", "| Stage | Where", "gives the columns Stage, Where it lives"),
        (" | Who writes it |", " |", "gives the columns Step, Where it lives, What it holds, not"),
        ("| Order |", "| Ordering |", "gives the rows An idea or a bug, Agreed work, Ordering"),
        ("| Result | [a page](docs/roadmap.md) | what | who |\n", "", "gives the rows"),
        (
            "| Delivery | [a page](docs/roadmap.md)",
            "| Delivery | a page",
            "row Delivery that links",
        ),
    ],
)
def test_a_briefing_out_of_form_is_reported(
    tmp_path: Path, old: str, new: str, problem: str
) -> None:
    found = briefing_problems(plant(tmp_path, "README.md", old, new))
    assert [p for p in found if p.startswith("README.md") and problem in p], found


def test_rows_out_of_order_are_reported(tmp_path: Path) -> None:
    agreed = "| Agreed work | [a page](docs/roadmap.md) | what | who |\n"
    order = "| Order | [a page](docs/roadmap.md) | what | who |\n"
    root = plant(tmp_path, "README.md", agreed + order, order + agreed)
    assert briefing_problems(root) == [
        "README.md's table of stages gives the rows An idea or a bug, Order, Agreed work, "
        "Delivery, Result, not An idea or a bug, Agreed work, Order, Delivery, Result"
    ]


def test_a_briefing_after_the_setup_is_reported(tmp_path: Path) -> None:
    start = BRIEFED.index(BRIEFING[0])
    end = BRIEFED.index("\nSetup for a local clone:")
    moved = BRIEFED[:start] + BRIEFED[end + 1 :] + "\n" + BRIEFED[start:end]
    found = briefing_problems(build(tmp_path, {"README.md": moved}))
    assert "README.md's briefing has no table of stages" in found
    assert len([p for p in found if "does not say" in p]) == len(BRIEFING)


def test_a_readme_without_the_section_is_reported(tmp_path: Path) -> None:
    root = plant(tmp_path, "README.md", f"## {WORKING}", "## Working here")
    assert briefing_problems(root) == [f"README.md has no section {WORKING}"]


def test_a_second_copy_of_the_table_is_reported(tmp_path: Path) -> None:
    table = f"| {' | '.join(COLUMNS)} |"
    root = build(tmp_path, {"docs/other.md": f"# Other\n\n{table.replace(' | ', '|')}\n"})
    assert briefing_problems(root) == [
        "docs/other.md:3 gives the header of the README's table of stages, whose one home is "
        "the README"
    ]


@pytest.mark.parametrize(
    "header",
    [" | ".join(COLUMNS), f"   | {' | '.join(COLUMNS)} |", f"> | {' | '.join(COLUMNS)} |"],
)
def test_a_copy_of_the_header_in_another_form_is_reported(tmp_path: Path, header: str) -> None:
    root = build(tmp_path, {"docs/other.md": f"# Other\n\n{header}\n"})
    assert briefing_problems(root) == [
        "docs/other.md:3 gives the header of the README's table of stages, whose one home is "
        "the README"
    ]


@pytest.mark.parametrize("name", ["CONTRIBUTING.md", PAGE])
def test_a_page_that_does_not_link_the_section_is_reported(tmp_path: Path, name: str) -> None:
    root = build(tmp_path, {name: WHOLE[name].replace(f"#{WORKING_ANCHOR}", "#elsewhere")})
    assert briefing_problems(root) == [f"{name} does not link the README's section {WORKING}"]


# The comparison with a base commit.


def commit(root: Path, message: str = "A change") -> str:
    for args in (["add", "-A"], ["commit", "-q", "--allow-empty", "-m", message]):
        assert git(root, *args).returncode == 0
    return git(root, "rev-parse", "HEAD").stdout.decode().strip()


def failing(module: ModuleType, command: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """Make each run of this git command from the module's functions fail, as in a clone
    that git cannot read."""
    real: Callable[..., subprocess.CompletedProcess[bytes]] = module.git

    def run(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
        if args[0] == command:
            return subprocess.CompletedProcess(["git", *args], 128, b"", b"fatal: planted")
        return real(root, *args)

    monkeypatch.setattr(module, "git", run)


def with_base(root: Path, changed: dict[str, str | None] | None = None) -> Path:
    """The tree, committed as the default branch, and then changed and committed."""
    build(root)
    commit(root, "The base")
    git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
    for name, text in (changed or {}).items():
        path = root / name
        if text is None:
            path.unlink()
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    commit(root)
    return root


def compared(root: Path, today: date = TODAY) -> list[str]:
    return history_problems(root, *base_commits(root, {}), today=today)


def test_an_unchanged_tree_passes_against_its_base(tmp_path: Path) -> None:
    assert compared(with_base(tmp_path)) == []


@pytest.mark.parametrize(
    ("command", "error"),
    [("ls-tree", "cannot list the files of HEAD"), ("show", f"cannot read {ITEM} in HEAD")],
)
def test_a_git_run_that_fails_is_an_error_not_an_empty_backlog(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, command: str, error: str
) -> None:
    root = with_base(tmp_path)
    bases = base_commits(root, {})
    failing(sys.modules[__name__], command, monkeypatch)
    with pytest.raises(LookupError, match=error):
        history_problems(root, *bases, today=TODAY)


def test_an_item_removed_renamed_or_moved_is_reported(tmp_path: Path) -> None:
    root = with_base(
        tmp_path,
        {ITEM: None, f"{BACKLOG}/B-001-a-renamed-thing.md": WHOLE[ITEM]},
    )
    found = compared(root)
    assert f"{ITEM}, which a base commit holds, was removed, renamed or moved" in found


def test_an_item_changed_without_a_later_date_is_reported(tmp_path: Path) -> None:
    root = with_base(tmp_path, {ITEM: WHOLE[ITEM].replace("Why it matters.", "Why.")})
    assert compared(root, date(2026, 1, 2)) == [
        f"{ITEM} was changed and gives 2026-01-01 in Last changed, not a later date than the "
        "base's 2026-01-01"
    ]


def test_an_item_changed_with_an_earlier_date_is_reported(tmp_path: Path) -> None:
    text = WHOLE[ITEM].replace("Why it matters.", "Why.").replace("2026-01-01", "2025-12-31")
    root = with_base(tmp_path, {ITEM: text})
    assert compared(root) == [
        f"{ITEM} was changed and gives 2025-12-31 in Last changed, not a later date than the "
        "base's 2026-01-01"
    ]


def test_an_item_changed_with_a_later_date_passes(tmp_path: Path) -> None:
    text = WHOLE[ITEM].replace("Why it matters.", "Why.").replace("2026-01-01", "2026-01-02")
    assert compared(with_base(tmp_path, {ITEM: text}), date(2026, 1, 2)) == []


def test_a_second_change_on_the_day_of_the_first_passes(tmp_path: Path) -> None:
    root = with_base(tmp_path, {ITEM: WHOLE[ITEM].replace("Why it matters.", "Why.")})
    assert compared(root, TODAY) == []


def test_a_date_after_the_day_of_the_run_is_reported(tmp_path: Path) -> None:
    root = plant(tmp_path, ITEM, "2026-01-01", "2026-01-02")
    assert history_problems(root, today=TODAY) == [
        f"{ITEM} gives 2026-01-02, after the day of the run, 2026-01-01"
    ]


@pytest.mark.parametrize("status", [IN_PROGRESS, DONE, DROPPED])
def test_an_item_added_past_agreement_is_reported(tmp_path: Path, status: str) -> None:
    text = item_text(6, "A new thing", status, "It is new.")
    root = with_base(tmp_path, {f"{BACKLOG}/B-006-a-new-thing.md": text})
    assert compared(root) == [
        f"{BACKLOG}/B-006-a-new-thing.md was added as {status}, where an item is added only "
        f"as {OPEN} or {PLANNED}"
    ]


@pytest.mark.parametrize("status", [OPEN, PLANNED])
def test_an_item_added_open_or_planned_passes(tmp_path: Path, status: str) -> None:
    text = item_text(6, "A new thing", status, "It is new.")
    assert compared(with_base(tmp_path, {f"{BACKLOG}/B-006-a-new-thing.md": text})) == []


@pytest.mark.parametrize(
    ("name", "old", "new"),
    [
        (f"{BACKLOG}/B-002-another-thing.md", OPEN, IN_PROGRESS),
        (f"{BACKLOG}/B-002-another-thing.md", OPEN, DONE),
        (DROPPED_ITEM, DROPPED, IN_PROGRESS),
        (DROPPED_ITEM, DROPPED, DONE),
    ],
)
def test_an_item_moved_past_agreement_is_reported(
    tmp_path: Path, name: str, old: str, new: str
) -> None:
    text = WHOLE[name].replace(f"**Status:** {old}", f"**Status:** {new}")
    root = with_base(tmp_path, {name: text})
    assert f"{name} moved from {old} to {new}, which skips agreement" in compared(root)


def test_an_item_moved_from_planned_to_done_passes(tmp_path: Path) -> None:
    root = with_base(tmp_path, {ITEM: WHOLE[ITEM].replace("Planned", DONE)})
    assert compared(root) == []


def test_no_base_that_holds_the_backlog_examines_nothing(tmp_path: Path) -> None:
    build(tmp_path, {name: None for name in WHOLE if name.startswith(BACKLOG)})
    commit(tmp_path, "The base")
    git(tmp_path, "update-ref", "refs/remotes/origin/main", "HEAD")
    for name in WHOLE:
        if name.startswith(BACKLOG):
            (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
            (tmp_path / name).write_text(WHOLE[name].replace("Planned", DONE), encoding="utf-8")
    commit(tmp_path)
    assert compared(tmp_path) == []
    # Once a base holds the backlog, every item is read.
    git(tmp_path, "update-ref", "refs/remotes/origin/main", "HEAD")
    (tmp_path / ITEM).unlink()
    commit(tmp_path)
    assert compared(tmp_path) == [
        f"{ITEM}, which a base commit holds, was removed, renamed or moved"
    ]
