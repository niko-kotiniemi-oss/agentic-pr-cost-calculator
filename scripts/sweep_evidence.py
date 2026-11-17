"""Show that the sweep of B-022 lost no clause.

    python3 scripts/sweep_evidence.py [DEFAULT]

Run anywhere in the repository, it compares HEAD with its merge base with DEFAULT, which
is `refs/remotes/origin/main` unless given, in every file that GitHub shows as Markdown,
by the extensions that `scripts/wording.py` lists, that changed between them other than
the mapping, `docs/evidence/B-022-mapping.md`, read from git and not from the working
tree (design decision 19; T173, T195, T198, T199). It serves the one pull request that
sweeps B-022 and finishes it: at a later head the mapping no longer describes the diff.
It reads each file as units: a heading, a table row, a list item with the lines that
continue it, a fenced block taken whole, and each sentence of a paragraph. For each unit
that the base holds and HEAD does not, the mapping, as HEAD holds it, must give an entry
whose clauses, each quoted from the unit, cover every word of it, and each clause must
have a place that exists at HEAD: the entry's new unit, which HEAD's page must hold, or
the page itself, either holding the clause as whole words; a requirement of the
register, which a rewritten unit's new unit cites, by its ID or in a range; a scenario
of a spec, as `capability`: "name"; a decision record; a task of a change; or, for a
clause that the pull request's own work changes rather than the sweep, such as a status
or a count, `changed, ` and why, which the output lists apart for the review, as it
lists a clause of one word or none placed anywhere but the new unit. It fails on a
change to a spec, since the sweep writes none, on a changed file read as no units, on a
run that compares no page, on an entry for a unit that HEAD still holds, and on a
mapping out of its form.

It prints Markdown for the pull request: both commits by their full hashes, each file
with the number of units that it read at the base and at HEAD and of its entries, and
each problem. It exits 0 when there is none, 1 when there are problems, and 2, saying
why, when it cannot compare, as when git cannot list the changed files or the files at
HEAD, cannot show a file that it lists, or gives output that is not UTF-8. Run it after
the pull request's last rebase or push, and have the review in a context other than the
builder's run it again at the head that the owner is asked to merge (T198).
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field

from wording import DEFAULT_BRANCH, MARKDOWN

MAPPING = "docs/evidence/B-022-mapping.md"
SPEC = re.compile(r"^openspec/(?:.+/)?specs/")
FENCE = re.compile(r"^( *)(`{3,}|~{3,})")
LIST_ITEM = re.compile(r"^( *)(?:[-*+]|\d+[.)]) ")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9`*\[(_\"])")
WORD = re.compile(r"\w+")
REQUIREMENT = re.compile(r"R\d+")
RECORD = re.compile(r"DR-\d{3,}")
TASK = re.compile(r"task (\d+\.\d+)")
SCENARIO = re.compile(r'`([a-z0-9-]+)`: "(.+)"')
CITED = re.compile(r"\bR(\d+)\b")
CITED_RANGE = re.compile(r"\bR(\d+) to R(\d+)\b")
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
    try:
        return done.stdout.decode("utf-8")
    except UnicodeDecodeError:
        raise Unreadable(f"git's output is not UTF-8, from `git {' '.join(args)}`") from None


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


def blocks(lines: list[str], start: int) -> tuple[list[tuple[str, str, int]], int]:
    """Each label of an entry with its fenced text, from `start` to the next heading, and
    the line where that heading is."""
    found: list[tuple[str, str, int]] = []
    index = start
    while index < len(lines) and not lines[index].startswith("#"):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        end = index + 3
        while end < len(lines) and lines[end] != "~~~~":
            end += 1
        if (
            not line.endswith(":")
            or end >= len(lines)
            or lines[index + 1].strip()
            or lines[index + 2] != "~~~~text"
        ):
            raise Unreadable(f"the mapping is not in its form at line {index + 1}")
        found.append((line[:-1], "\n".join(lines[index + 3 : end]), index + 1))
        index = end + 1
    return found, index


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
            labels, stop = blocks(lines, index + 1)
            for label, body, number in labels:
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
            index = stop
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


def side(commit: str, path: str, there: bool, name: str) -> str | None:
    """The file at a commit, None where git says it is not there; Unreadable where git
    says it is there and cannot show it."""
    if not there:
        return None
    text = git("show", f"{commit}:{path}")
    if text is None:
        raise Unreadable(f"git cannot read `{path}` at {name}")
    return text


def head_places() -> Head:
    listed = git("ls-tree", "-r", "-z", "--full-tree", "--name-only", "HEAD")
    if listed is None:
        raise Unreadable("git cannot list the files at HEAD")
    files = listed.split("\0")
    register = side("HEAD", "docs/requirements.md", "docs/requirements.md" in files, "HEAD") or ""
    requirements = set(re.findall(r"^\| (R\d+) \|", register, re.MULTILINE))
    records = {
        m.group(1) for f in files if (m := re.match(r"docs/decisions/(DR-\d{3,})-", f)) is not None
    }
    live = [f for f in files if f.startswith("openspec/") and "/archive/" not in f]
    tasks: set[str] = set()
    scenarios: set[tuple[str, str]] = set()
    for name in live:
        if name.endswith("/tasks.md"):
            text = side("HEAD", name, True, "HEAD") or ""
            tasks |= set(re.findall(r"^- \[[ x]\] (\d+\.\d+) ", text, re.MULTILINE))
        spec = re.search(r"specs/([a-z0-9-]+)/spec\.md$", name)
        if spec:
            text = side("HEAD", name, True, "HEAD") or ""
            for title in re.findall(r"^#### Scenario: (.+)$", text, re.MULTILINE):
                scenarios.add((spec.group(1), title.strip()))
    return Head(requirements, records, tasks, scenarios)


def changed_reason(place: str) -> str | None:
    """The reason that a place `changed, ` gives, or None when it is not one."""
    reason = place[len(CHANGED) :].strip() if place.startswith(CHANGED) else ""
    return reason or None


def holds(text: str, clause: str) -> bool:
    """Whether the text holds the clause, and not as a part of a longer word."""
    before = r"(?<!\w)" if WORD.match(clause) else ""
    after = r"(?!\w)" if WORD.match(clause[-1:]) else ""
    return re.search(before + re.escape(clause) + after, text) is not None


def cited(text: str) -> set[int]:
    """The numbers of the requirements that a unit cites, each by its ID or in a range."""
    numbers = {int(number) for number in CITED.findall(text)}
    for first, last in CITED_RANGE.findall(text):
        numbers |= set(range(int(first), int(last) + 1))
    return numbers


def place_problem(place: str, clause: str, entry: Entry, page: str, head: Head) -> str | None:
    if place == NEW_UNIT:
        if entry.new is None:
            return f"a clause placed in a new unit that the entry does not give: {clause}"
        if holds(entry.new, clause):
            return None
        return f"the new unit does not hold the clause: {clause}"
    if changed_reason(place):
        return None
    if place == PAGE:
        return None if holds(page, clause) else f"HEAD's page does not hold the clause: {clause}"
    if REQUIREMENT.fullmatch(place):
        if place not in head.requirements:
            return f"{place} is not in the register at HEAD"
        if entry.new is not None and int(place[1:]) not in cited(entry.new):
            return f"the new unit does not cite {place}: {clause}"
        return None
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
        while at != -1 and clause and all(covered[at : at + len(clause)]):
            following = entry.old.find(clause, at + 1)
            if following == -1:
                break
            at = following
        if at == -1 or not clause:
            problems.append(f"the old unit does not hold the clause: {clause}")
        else:
            covered[at : at + len(clause)] = [True] * len(clause)
        problem = place_problem(place, clause, entry, page, head)
        if problem:
            problems.append(problem)
    gap = [w.group(0) for w in WORD.finditer(entry.old) if not all(covered[w.start() : w.end()])]
    if gap:
        problems.append(f"no clause places: {' '.join(gap)}")
    return problems


Rows = list[tuple[str, int, int, int]]


@dataclass
class Comparison:
    """What the script found: both commits, a row for each file, the problems, and the
    clauses that it lists apart for the review."""

    base: str
    head: str
    rows: Rows = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    changes: list[str] = field(default_factory=list)
    short: list[str] = field(default_factory=list)


def compare(reference: str) -> Comparison:
    base = git("merge-base", "HEAD", reference)
    head = git("rev-parse", "HEAD")
    if base is None or head is None:
        raise Unreadable(f"cannot resolve the merge base with {reference}")
    found = Comparison(base.strip(), head.strip())
    mapping_text = git("show", f"HEAD:{MAPPING}")
    if mapping_text is None:
        raise Unreadable(f"HEAD holds no {MAPPING}")
    entries = parse(mapping_text)
    listed = git(
        "diff",
        "-z",
        "--name-status",
        "--no-renames",
        "--no-relative",
        found.base,
        found.head,
        "--",
        *MARKDOWN,
    )
    if listed is None:
        raise Unreadable("git cannot list the files that changed")
    fields = listed.split("\0")
    changed = dict(zip(fields[1::2], fields[0::2], strict=False))
    places = head_places()
    for path in sorted(changed):
        if path == MAPPING:
            continue
        if SPEC.match(path):
            found.problems.append(f"`{path}`: the sweep changes a spec")
            continue
        status = changed[path]
        before_text = side(found.base, path, status != "A", "the base")
        after_text = side(found.head, path, status != "D", "HEAD")
        before = units(before_text) if before_text is not None else []
        after = units(after_text) if after_text is not None else []
        for name, text, read in (("the base", before_text, before), ("HEAD", after_text, after)):
            if text is not None and not read:
                found.problems.append(f"`{path}`: read as no units at {name}")
        held = Counter(after)
        gone = Counter(before) - held
        page = " ".join((after_text or "").split())
        given = entries.get(path, [])
        found.rows.append((path, len(before), len(after), len(given)))
        for entry in given:
            if gone[entry.old] == 0:
                found.problems.append(
                    f"`{path}`: an entry for a unit that HEAD still holds, or that the base"
                    f" does not: {entry.old}"
                )
                continue
            gone[entry.old] -= 1
            for clause, place in entry.clauses:
                reason = changed_reason(place)
                if reason:
                    found.changes.append(f"`{path}`: {clause} ({reason})")
                elif place != NEW_UNIT and len(clause.split()) <= 1:
                    found.short.append(f"`{path}`: {clause} ({place})")
            for problem in entry_problems(entry, page, held, places):
                found.problems.append(f"`{path}`: {problem}")
        for unit, count in gone.items():
            for _ in range(count):
                found.problems.append(
                    f"`{path}`: no entry for a unit that HEAD does not hold: {unit}"
                )
    if not found.rows:
        found.problems.append("no changed page was compared")
    for path in sorted(set(entries) - {row[0] for row in found.rows}):
        found.problems.append(f"`{path}`: entries for a file that did not change")
    return found


def main(argv: Sequence[str]) -> int:
    reference = argv[0] if argv else DEFAULT_BRANCH
    try:
        found = compare(reference)
    except Unreadable as reason:
        print(f"Cannot compare: {reason}.")
        return 2
    print(
        f"Compared HEAD at `{found.head}` with `{found.base}`, its merge base with `{reference}`.\n"
    )
    print("| File | Units at the base | Units at HEAD | Entries |")
    print("|---|---|---|---|")
    for path, before, after, given in found.rows:
        print(f"| `{path}` | {before} | {after} | {given} |")
    for title, listed in (
        ("Changed by this pull request's own work", found.changes),
        ("Clauses of one word or none placed outside the new unit", found.short),
    ):
        if listed:
            print(f"\n## {title}\n")
            for line in listed:
                print(f"- {line}")
    if not found.problems:
        print("\nNo problems.")
        return 0
    print("\n## Problems\n")
    for problem in found.problems:
        print(f"- {problem}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
