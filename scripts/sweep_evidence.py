"""Show that the sweep of B-022 lost no clause.

    python3 scripts/sweep_evidence.py [DEFAULT]

Run in the repository, it compares HEAD with its merge base with DEFAULT, which is
`refs/remotes/origin/main` unless given, in every Markdown file that changed between
them other than the mapping, `docs/evidence/B-022-mapping.md`, read from git and not
from the working tree (design decision 19; T173, T195, T198, T199). It reads each file
as units: a heading, a table row, a list item with the lines that continue it, a fenced
block taken whole, and each sentence of a paragraph. For each unit that the base holds
and HEAD does not, the mapping, as HEAD holds it, must give an entry whose clauses, each
quoted from the unit, cover every word of it, and each clause must have a place that
exists at HEAD: the entry's new unit, which HEAD's page must hold; the page itself; a
requirement of the register; a scenario of a spec, as `capability`: "name"; a decision
record; a task of a change; or, for a clause that the pull request's own work changes
rather than the sweep, such as a status or a count, `changed, ` and why, which the output
lists apart for the review. It fails on a change to a spec, since the sweep writes
none, on a changed file read as no units, on an entry for a unit that HEAD still holds,
and on a mapping out of its form.

It prints Markdown for the pull request: both commits by their full hashes, each file
with the units that it read at the base and at HEAD and its entries, and each problem.
It exits 0 when there is none, 1 when there are problems, and 2, saying why, when it
cannot compare. Run it after the pull request's last rebase or push, and have the
review in a context other than the builder's run it again at the head that the owner
is asked to merge (T198).
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field

MAPPING = "docs/evidence/B-022-mapping.md"
DEFAULT = "refs/remotes/origin/main"
SPEC = re.compile(r"(?:^|/)specs/.+\.md$")
FENCE = re.compile(r"^( *)(`{3,}|~{3,})")
LIST_ITEM = re.compile(r"^( *)(?:[-*+]|\d+[.)]) ")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9`*\[(_\"])")
WORD = re.compile(r"\w+")
REQUIREMENT = re.compile(r"R\d+")
RECORD = re.compile(r"DR-\d{3,}")
TASK = re.compile(r"task (\d+\.\d+)")
SCENARIO = re.compile(r'`([a-z0-9-]+)`: "(.+)"')
NEW_UNIT = "the new unit"
PAGE = "the page"
CHANGED = "changed, "
OTHER_SECTIONS = ("For B-007", "Left as it is")


class Unreadable(Exception):
    """The script cannot compare, and says why."""


def git(*args: str) -> str | None:
    done = subprocess.run(["git", *args], capture_output=True)
    if done.returncode != 0:
        return None
    return done.stdout.decode("utf-8")


def normal(text: str) -> str:
    """A unit's text with the white space of its lines joined, unless it is a fence."""
    if FENCE.match(text):
        return text.strip("\n")
    return " ".join(text.split())


def units(text: str) -> list[str]:
    """The units of a Markdown page, in order."""
    found: list[str] = []
    lines = text.split("\n")
    paragraph: list[str] = []
    item: list[str] | None = None
    item_indent = 0

    def close() -> None:
        nonlocal item, paragraph
        if item is not None:
            found.append(normal(" ".join(item)))
            item = None
        if paragraph:
            found.extend(normal(s) for s in SENTENCE_END.split(" ".join(paragraph)) if s.strip())
            paragraph = []

    index = 0
    while index < len(lines):
        line = lines[index]
        fence = FENCE.match(line)
        if fence:
            close()
            indent, marker = len(fence.group(1)), fence.group(2)
            block = [line[indent:]]
            index += 1
            while index < len(lines):
                inner = lines[index]
                stripped = inner[min(indent, len(inner) - len(inner.lstrip(" "))) :]
                block.append(stripped)
                index += 1
                if (
                    stripped.strip().startswith(marker[0] * len(marker))
                    and not stripped.strip(marker[0]).strip()
                ):
                    break
            found.append("\n".join(block))
            continue
        stripped = line.strip()
        listed = LIST_ITEM.match(line)
        if not stripped:
            close()
        elif stripped.startswith("#") or stripped.startswith("|"):
            close()
            found.append(normal(stripped))
        elif listed:
            close()
            item = [stripped]
            item_indent = len(listed.group(1))
        elif item is not None and len(line) - len(line.lstrip(" ")) > item_indent:
            item.append(stripped)
        else:
            if item is not None:
                close()
            paragraph.append(stripped)
        index += 1
    close()
    return found


@dataclass
class Entry:
    old: str
    new: str | None = None
    clauses: list[tuple[str, str]] = field(default_factory=list)


def blocks(lines: list[str], start: int) -> Iterator[tuple[str, str, int]]:
    """Each label of an entry with its fenced text, from `start` to the next heading."""
    index = start
    while index < len(lines) and not lines[index].startswith("#"):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if not line.endswith(":") or index + 2 >= len(lines):
            raise Unreadable(f"the mapping is not in its form at line {index + 1}")
        if lines[index + 1].strip() or lines[index + 2] != "~~~~text":
            raise Unreadable(f"the mapping is not in its form at line {index + 1}")
        end = index + 3
        while end < len(lines) and lines[end] != "~~~~":
            end += 1
        if end == len(lines):
            raise Unreadable(f"the mapping is not in its form at line {index + 1}")
        yield line[:-1], "\n".join(lines[index + 3 : end]), index + 1
        index = end + 1


def parse(text: str) -> dict[str, list[Entry]]:
    """The mapping's entries, by the file that each belongs to."""
    lines = text.split("\n")
    entries: dict[str, list[Entry]] = {}
    path: str | None = None
    index = 0
    while index < len(lines):
        line = lines[index]
        section = re.fullmatch(r"## `([^`]+)`", line)
        if section:
            path = section.group(1)
            entries.setdefault(path, [])
        elif line.startswith("## "):
            if line[3:] not in OTHER_SECTIONS:
                raise Unreadable(f"the mapping is not in its form at line {index + 1}")
            path = None
        elif line.startswith("### ") and path is not None:
            entry: Entry | None = None
            for label, body, number in blocks(lines, index + 1):
                if label == "Old" and entry is None:
                    entry = Entry(normal(body))
                elif entry is None:
                    raise Unreadable(f"the mapping is not in its form at line {number}")
                elif label == "New" and entry.new is None and not entry.clauses:
                    entry.new = normal(body)
                elif label.startswith("Clause, "):
                    entry.clauses.append((normal(body), label[len("Clause, ") :]))
                else:
                    raise Unreadable(f"the mapping is not in its form at line {number}")
            if entry is None or not entry.clauses:
                raise Unreadable(f"the mapping is not in its form at line {index + 1}")
            entries[path].append(entry)
            index += 1
            while index < len(lines) and not lines[index].startswith("#"):
                index += 1
            continue
        index += 1
    return entries


@dataclass
class Head:
    """What a place can name at HEAD."""

    requirements: set[str]
    records: set[str]
    tasks: set[str]
    scenarios: set[tuple[str, str]]


def head_places() -> Head:
    files = (git("ls-tree", "-r", "--name-only", "HEAD") or "").split("\n")
    register = git("show", "HEAD:docs/requirements.md") or ""
    requirements = set(re.findall(r"^\| (R\d+) \|", register, re.MULTILINE))
    records = {
        m.group(1) for f in files if (m := re.match(r"docs/decisions/(DR-\d{3,})-", f)) is not None
    }
    live = [f for f in files if f.startswith("openspec/") and "/archive/" not in f]
    tasks: set[str] = set()
    scenarios: set[tuple[str, str]] = set()
    for name in live:
        if name.endswith("/tasks.md"):
            text = git("show", f"HEAD:{name}") or ""
            tasks |= set(re.findall(r"^- \[[ x]\] (\d+\.\d+) ", text, re.MULTILINE))
        spec = re.search(r"specs/([a-z0-9-]+)/spec\.md$", name)
        if spec:
            text = git("show", f"HEAD:{name}") or ""
            for title in re.findall(r"^#### Scenario: (.+)$", text, re.MULTILINE):
                scenarios.add((spec.group(1), title.strip()))
    return Head(requirements, records, tasks, scenarios)


def place_problem(place: str, clause: str, entry: Entry, page: str, head: Head) -> str | None:
    if place == NEW_UNIT:
        if entry.new is None:
            return f"a clause placed in a new unit that the entry does not give: {clause}"
        return None if clause in entry.new else f"the new unit does not hold the clause: {clause}"
    if place.startswith(CHANGED) and place[len(CHANGED) :].strip():
        return None
    if place == PAGE:
        return None if clause in page else f"HEAD's page does not hold the clause: {clause}"
    if REQUIREMENT.fullmatch(place):
        return None if place in head.requirements else f"{place} is not in the register at HEAD"
    if RECORD.fullmatch(place):
        return None if place in head.records else f"{place} is not a record at HEAD"
    task = TASK.fullmatch(place)
    if task:
        return None if task.group(1) in head.tasks else f"{place} is in no change's tasks at HEAD"
    scenario = SCENARIO.fullmatch(place)
    if scenario:
        if (scenario.group(1), scenario.group(2)) in head.scenarios:
            return None
        return f"no spec at HEAD holds {place}"
    return f"{place.strip()} is not a place"


def entry_problems(entry: Entry, page: str, head_units: Counter[str], head: Head) -> list[str]:
    problems: list[str] = []
    if entry.new is not None and head_units[entry.new] == 0:
        problems.append(f"HEAD does not hold the new unit: {entry.new}")
    covered = [False] * len(entry.old)
    for clause, place in entry.clauses:
        at = entry.old.find(clause)
        if at == -1 or not clause:
            problems.append(f"the old unit does not hold the clause: {clause}")
        else:
            covered[at : at + len(clause)] = [True] * len(clause)
        problem = place_problem(place, clause, entry, " ".join(page.split()), head)
        if problem:
            problems.append(problem)
    gap = [w.group(0) for w in WORD.finditer(entry.old) if not all(covered[w.start() : w.end()])]
    if gap:
        problems.append(f"no clause places: {' '.join(gap)}")
    return problems


Rows = list[tuple[str, int, int, int]]


def compare(reference: str) -> tuple[str, str, Rows, list[str], list[str]]:
    base = git("merge-base", "HEAD", reference)
    head = git("rev-parse", "HEAD")
    if base is None or head is None:
        raise Unreadable(f"cannot resolve the merge base with {reference}")
    base, head = base.strip(), head.strip()
    mapping_text = git("show", f"HEAD:{MAPPING}")
    if mapping_text is None:
        raise Unreadable(f"HEAD holds no {MAPPING}")
    entries = parse(mapping_text)
    changed = (git("diff", "--name-only", "--no-renames", base, head) or "").split()
    places = head_places()
    rows: Rows = []
    problems: list[str] = []
    changes: list[str] = []
    for path in sorted(set(changed)):
        if not path.endswith(".md") or path == MAPPING:
            continue
        if SPEC.search(path) and path.startswith("openspec/"):
            problems.append(f"`{path}`: the sweep changes a spec")
            continue
        before_text = git("show", f"{base}:{path}")
        after_text = git("show", f"{head}:{path}")
        before = units(before_text) if before_text is not None else []
        after = units(after_text) if after_text is not None else []
        for side, text, read in (("the base", before_text, before), ("HEAD", after_text, after)):
            if text is not None and not read:
                problems.append(f"`{path}`: read as no units at {side}")
        gone = Counter(before) - Counter(after)
        given = entries.get(path, [])
        rows.append((path, len(before), len(after), len(given)))
        for entry in given:
            if gone[entry.old] == 0:
                problems.append(
                    f"`{path}`: an entry for a unit that HEAD still holds, or that the base"
                    f" does not: {entry.old}"
                )
                continue
            gone[entry.old] -= 1
            for clause, place in entry.clauses:
                if place.startswith(CHANGED) and place[len(CHANGED) :].strip():
                    changes.append(f"`{path}`: {clause} ({place[len(CHANGED) :].strip()})")
            for problem in entry_problems(entry, after_text or "", Counter(after), places):
                problems.append(f"`{path}`: {problem}")
        for unit, count in gone.items():
            for _ in range(count):
                problems.append(f"`{path}`: no entry for a unit that HEAD does not hold: {unit}")
    for path in sorted(set(entries) - {row[0] for row in rows}):
        problems.append(f"`{path}`: entries for a file that did not change")
    return base, head, rows, problems, changes


def main(argv: Sequence[str]) -> int:
    reference = argv[0] if argv else DEFAULT
    try:
        base, head, rows, problems, changes = compare(reference)
    except Unreadable as reason:
        print(f"Cannot compare: {reason}.")
        return 2
    print(f"Compared HEAD at `{head}` with `{base}`, its merge base with `{reference}`.\n")
    print("| File | Units at the base | Units at HEAD | Entries |")
    print("|---|---|---|---|")
    for path, before, after, given in rows:
        print(f"| `{path}` | {before} | {after} | {given} |")
    if changes:
        print("\n## Changed by this pull request's own work\n")
        for change in changes:
            print(f"- {change}")
    if not problems:
        print("\nNo problems.")
        return 0
    print("\n## Problems\n")
    for problem in problems:
        print(f"- {problem}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
