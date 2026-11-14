"""The guide, `docs/patterns.md`, says how the project builds, concern by concern.

The README's list of documentation links it and `CLAUDE.md` gives the sentence on its
rank. It opens with the text that R219 gives, word for word, and a last line that names
the assessment or the release for which its entries were last read, and then gives its
nine concerns, each once and in order, each holding one or more entries (R219). An entry
is a `###` heading that names a principle, followed by its eight fields, each once, in
order, none empty, and nothing else, and an entry under Working with agents cites
`CLAUDE.md` in Held by (R220). The guide holds to the roadmap's readings of links and
hidden text, apart from the inline code with a space in its fixed opening, gives no `$`
or `~` outside inline code, and cites no file under `vendor/` or `.claude/skills/` in Held
by (R221). Each Pattern gives its source after `Source:`; each Held by cites what holds
the entry as the threat model's Held by does, or says after `Review:` what review checks;
each Rests on names IDs in a backlog item's forms that exist and are no closed record;
and four named practices are each named in a Pattern (R222). Where we stand opens with
one of four words, each held true against the tasks, the records and the backlog, and,
under the four concerns that adopters rely on, only an owner's record accepts a risk and
only an agreed item closes a gap (R226).

Each check is shown to fail on a synthetic tree, the roadmap's with a guide, into which
its defect is planted.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pytest
from test_backlog import AGREED, DONE, DROPPED, REST, backlog_items, holders, rest_problems
from test_decisions import DECIDER, records_of
from test_roadmap import (
    BACKLOG,
    DOCUMENTATION,
    HIDDEN_TEXT,
    INLINE_CODE,
    LINKS_ELSEWHERE,
    RECORD_NAME,
    TREE,
    hidden_text_problems_in,
    link_problems_in,
    make_tree,
    others_write,
    read,
    records,
    section_of,
    sections,
    tasks,
)
from test_threat_model import (
    DECISION_REF,
    PATH_REF,
    RECORD_REF,
    SCENARIO_REF,
    TASK_REF,
    citation_problems,
    index,
)

ROOT = Path(__file__).resolve().parents[1]

GUIDE = "docs/patterns.md"
CONCERNS = (
    "Architecture and integration",
    "Security",
    "Privacy",
    "Identity and credentials",
    "Supply chain and releases",
    "Testing",
    "Decisions and documentation",
    "Working with agents",
    "Conventions",
)
# The concerns whose entries adopters rely on, where only the owner accepts a risk and
# only an agreed item closes a gap (R226).
RELIED_ON = CONCERNS[1:5]
FIELDS = (
    "Statement",
    "Rationale",
    "Implications",
    "Pattern",
    "Anti-patterns",
    "Held by",
    "Rests on",
    "Where we stand",
)
OPENING = (
    "# How the project builds",
    "This guide says how the project builds, concern by concern: the principles that the "
    "project follows, each with the pattern that it applies and the anti-patterns that it "
    "steers clear of, what holds it, and where the project stands.",
    "The specs decide what the tool does, `CLAUDE.md` what an agent may do, and this guide "
    "how the project builds. Where the guide differs from the specs or `CLAUDE.md`, they "
    "win, and the owner is told. It never widens what `CLAUDE.md` lets an agent do, and an "
    "entry cites the requirement or the rule of `CLAUDE.md` that it rests on rather than "
    "stating it again. Where an entry and a step of a Superpowers skill differ, the step is "
    "followed, and the owner is told.",
    "The guide steers as the default branch holds it: an entry that a branch adds or "
    "changes is a proposal until the owner merges it, and a principle is added, removed or "
    "changed only when the owner asks for it, in a pull request that changes nothing outside "
    "`docs/`, `openspec/`, `CLAUDE.md` and `CHANGELOG.md`. It speaks to work on this "
    "repository, not to setting the tool up, which is the README's section on adopting it: "
    "an agent that sets the tool up turns capture on for no one.",
    "Where we stand gives where the default branch stands, and a release's guide is the copy "
    "at its tag. It opens with `Followed.` when the default branch's code and checks hold the "
    "principle, `Designed.` when its specs and tasks hold it before it is built, `Knowingly "
    "accepted.` with the record that gives the reason, or `Gap.` with the backlog item that "
    "closes it, as `Gap. Before the build.` when the owner asked for it to be closed before "
    "the build.",
    "A gap is not, by being there, a request to start work: it closes only through the "
    "backlog item that it names, and work outside that item leaves what the gap concerns as "
    "it stands. A principle knowingly accepted is accepted only where its record says.",
)
LAST_READ = (
    "The entries are read again at each assessment and before each release, and were last read for "
)
RANK = (
    "The guide is not one of the pages that only describe, but it steers below the specs "
    "and this file: where it differs from either, they win, so tell the owner, and it never "
    "widens what this file lets you do."
)
PRACTICES = ("Clean Code", "PEP 8", "OWASP Secure Coding Practices", "OpenSSF Scorecard")
STANDINGS = ("Followed.", "Designed.", "Knowingly accepted.", "Gap.")
# The opening's fixed lines, each followed by a blank line, as R219 gives them.
OPENING_LINES = [line for paragraph in OPENING for line in (paragraph, "")]
LAST_LINE = re.compile(
    re.escape(LAST_READ) + r"(?:the assessment of \d{4}-\d{2}-\d{2}|release \d+\.\d+\.\d+)\."
)
ENTRY_HEADING = re.compile(r"### (.+?) *")
FIELD = re.compile(r"- \*\*([^*]+):\*\* ?(.*)")
SOURCE = re.compile(r"\bSource: *\S")
ITEM_NAME = re.compile(r"\bB-\d{3}\b")
OUTSIDE_CODE = (
    ("$", "$ outside inline code, with which GitHub shows mathematics"),
    ("~", "~ outside inline code, with which GitHub strikes text through"),
)


@dataclass(frozen=True)
class Entry:
    concern: str
    heading: str
    line: int
    fields: dict[str, str]

    @property
    def name(self) -> str:
        """How a problem names the entry: by the line that heads it, and its heading."""
        return f'{GUIDE}:{self.line} "{self.heading}"'


def entries_of(text: str) -> tuple[list[Entry], list[str]]:
    """Each entry under the guide's sections, with the first value of each of its fields,
    and what is wrong with their form (R220)."""
    entries: list[Entry] = []
    problems: list[str] = []
    for concern, start, lines in sections(text):
        blocks: list[tuple[int, str, list[tuple[int, str]]]] = []
        for number, line in enumerate(lines, start):
            head = ENTRY_HEADING.fullmatch(line)
            if head:
                blocks.append((number, head.group(1), []))
            elif not line.strip():
                continue
            elif blocks:
                blocks[-1][2].append((number, line))
            else:
                problems.append(f"{GUIDE}:{number} holds text in {concern} outside its entries")
        for number, heading, body in blocks:
            order: list[str] = []
            fields: dict[str, str] = {}
            for at, line in body:
                field = FIELD.fullmatch(line)
                if field is None:
                    problems.append(
                        f'{GUIDE}:{at} holds text in "{heading}" that is not one of its fields'
                    )
                    continue
                order.append(field.group(1))
                fields.setdefault(field.group(1), field.group(2).strip())
            entry = Entry(concern, heading, number, fields)
            if tuple(order) != FIELDS:
                problems.append(
                    f"{entry.name} gives the fields {', '.join(order)}, where an entry gives "
                    "each of its eight once, in order"
                )
            problems += [f"{entry.name} leaves {name} empty" for name in fields if not fields[name]]
            entries.append(entry)
    headings = [entry.heading for entry in entries]
    problems += [
        f'{GUIDE}:{entry.line} repeats the heading "{entry.heading}"'
        for at, entry in enumerate(entries)
        if entry.heading in headings[:at]
    ]
    return entries, problems


def opening_problems(text: str) -> list[str]:
    """The first line before the first section that differs from the opening (R219)."""
    found = sections(text)
    lines = text.split("\n")
    given = lines[: found[0][1] - 2] if found else lines
    wanted: list[str | None] = [*OPENING_LINES, None, ""]
    for at in range(max(len(given), len(wanted))):
        if at >= len(wanted):
            return [f"{GUIDE}:{at + 1} adds a line to the opening"]
        line = given[at] if at < len(given) else None
        want = wanted[at]
        if want is None:
            if line is None or not LAST_LINE.fullmatch(line):
                return [
                    f"{GUIDE}:{at + 1} does not name the assessment or the release for which "
                    "the entries were last read"
                ]
        elif line != want:
            return [f"{GUIDE}:{at + 1} differs from the opening, which gives {want!r} there"]
    return []


def concern_problems(text: str, entries: list[Entry]) -> list[str]:
    """The guide's sections are its concerns, each once, in order, each with an entry (R219)."""
    found = [heading for heading, _, _ in sections(text)]
    problems = [f"{GUIDE} has no section {name}" for name in CONCERNS if name not in found]
    problems += [
        f"{GUIDE} has a section {name}, which is not a concern of the guide"
        for name in found
        if name not in CONCERNS
    ]
    problems += [
        f"{GUIDE} gives the section {name} more than once"
        for name in CONCERNS
        if found.count(name) > 1
    ]
    if not problems and found != list(CONCERNS):
        problems.append(f"{GUIDE} gives its sections out of order: {', '.join(found)}")
    held = {entry.concern for entry in entries}
    problems += [
        f"{GUIDE}: {name} holds no entry" for name in CONCERNS if name in found and name not in held
    ]
    return problems


def text_problems(root: Path, text: str) -> list[str]:
    """R209's and R210's readings of the guide, apart from the inline code with a space in
    its fixed opening, and no `$` or `~` outside inline code (R221)."""
    lines = text.split("\n")
    texts = [(GUIDE, "docs", 1, lines, text)]
    exempt = {
        f"{GUIDE}:{number} holds inline code that holds a space, as a command does"
        for number, (line, fixed) in enumerate(zip(lines, OPENING_LINES, strict=False), 1)
        if line == fixed
    }
    problems = [problem for problem in link_problems_in(root, texts) if problem not in exempt]
    problems += hidden_text_problems_in(texts)
    bare = INLINE_CODE.sub(lambda code: "\n" * code.group(0).count("\n"), text)
    for number, line in enumerate(bare.split("\n"), 1):
        problems += [
            f"{GUIDE}:{number} holds {what}" for mark, what in OUTSIDE_CODE if mark in line
        ]
    return problems


def source_problems(entries: list[Entry]) -> list[str]:
    return [
        f"{entry.name} gives no source after Source: in its Pattern"
        for entry in entries
        if entry.fields.get("Pattern") and not SOURCE.search(entry.fields["Pattern"])
    ]


def cited_paths(held: str) -> list[str]:
    """The files that a Held by cites, read as the threat model's citations are read."""
    rest = DECISION_REF.sub("", TASK_REF.sub("", SCENARIO_REF.sub("", held)))
    return PATH_REF.findall(RECORD_REF.sub("", rest))


def held_by_problems(root: Path, entries: list[Entry]) -> list[str]:
    """Each Held by cites what holds the entry, or says what review checks, or both (R222);
    under Working with agents it cites `CLAUDE.md` (R220); it cites no file that others
    write (R221)."""
    found = index(root)
    top = root.resolve()
    problems = []
    for entry in entries:
        held = entry.fields.get("Held by")
        if not held:
            continue
        cited, count = citation_problems(entry.name, held, found, root)
        problems += cited
        if count == 0 and not held.partition("Review:")[2].strip():
            problems.append(
                f"{entry.name} cites nothing in Held by and gives nothing after Review:"
            )
        paths = cited_paths(held)
        if entry.concern == "Working with agents" and "CLAUDE.md" not in paths:
            problems.append(
                f"{entry.name} is under Working with agents and does not cite `CLAUDE.md` in "
                "Held by"
            )
        for path in paths:
            target = (root / path).resolve()
            folder = top in target.parents and others_write(f"{target.relative_to(top)}/")
            if folder:
                problems.append(
                    f"{entry.name} cites `{path}` in Held by, under {folder}, whose files others "
                    "write"
                )
    return problems


def rests_on_problems(root: Path, entries: list[Entry]) -> list[str]:
    """Each Rests on names IDs, in a backlog item's forms, that exist and are no closed
    record (R222)."""
    held, closed, listed = holders(root), records(root), tasks(root)
    problems = []
    for entry in entries:
        value = entry.fields.get("Rests on")
        if not value:
            continue
        if value == "none":
            problems.append(f"{entry.name} rests on none")
            continue
        for name in value.split(", "):
            if REST.fullmatch(name):
                problems += rest_problems(entry.name, name, held, closed, listed)
            else:
                problems.append(
                    f"{entry.name} names {name} in Rests on, which is not an ID in a form that "
                    "it takes"
                )
    return problems


def practice_problems(entries: list[Entry]) -> list[str]:
    return [
        f"no entry's Pattern names {practice}"
        for practice in PRACTICES
        if not any(practice in entry.fields.get("Pattern", "") for entry in entries)
    ]


def owner_decided(decider: str) -> bool:
    found = DECIDER.fullmatch(decider)
    return found is not None and found.group("owner") is not None


def standing_problems(root: Path, entries: list[Entry]) -> list[str]:
    """Where we stand opens with one of its four words, each held true (R220, R226)."""
    listed, closed = tasks(root), records(root)
    deciders = {
        ident: record.fields.get("Decided by", "")
        for ident, record in records_of(root / "docs" / "decisions")[0].items()
    }
    items = {item.ident: item for item in backlog_items(root)}
    problems = []
    for entry in entries:
        standing = entry.fields.get("Where we stand")
        if not standing:
            continue
        word = next((word for word in STANDINGS if standing.startswith(word)), "")
        relied = entry.concern in RELIED_ON
        if not word:
            problems.append(
                f"{entry.name} opens Where we stand with none of Followed., Designed., "
                "Knowingly accepted. and Gap."
            )
        elif word in ("Followed.", "Designed."):
            cited = TASK_REF.findall(SCENARIO_REF.sub("", entry.fields.get("Held by", "")))
            unticked = [(change, n) for change, n in cited if not listed.get((change, n), False)]
            if word == "Followed.":
                problems += [
                    f"{entry.name} is Followed. while `{change}` task {n}, which its Held by "
                    "cites, is not ticked"
                    for change, n in unticked
                ]
            elif not unticked:
                problems.append(
                    f"{entry.name} is Designed. while its Held by cites no task that is not ticked"
                )
        elif word == "Knowingly accepted.":
            named = list(dict.fromkeys(RECORD_NAME.findall(standing)))
            if not [ident for ident in named if closed.get(ident) is False]:
                problems.append(f"{entry.name} is Knowingly accepted. and names no accepted record")
            if relied:
                problems += [
                    f"{entry.name} is under {entry.concern}, which adopters rely on, and is "
                    f"accepted with {ident}, which the owner did not decide"
                    for ident in named
                    if not owner_decided(deciders.get(ident, ""))
                ]
        else:
            named = list(dict.fromkeys(ITEM_NAME.findall(standing)))
            if not named:
                problems.append(f"{entry.name} is a Gap. and names no backlog item")
            for ident in named:
                item = items.get(ident)
                if item is None:
                    problems.append(f"{entry.name} names {ident}, which {BACKLOG} does not hold")
                elif item.status in (DONE, DROPPED):
                    problems.append(f"{entry.name} names {ident}, which is {item.status}")
                elif relied and item.status not in AGREED:
                    problems.append(
                        f"{entry.name} is under {entry.concern}, which adopters rely on, and "
                        f"names {ident}, which is {item.status}, not Planned or In progress"
                    )
    return problems


def guide_problems(root: Path) -> list[str]:
    problems = []
    path = root / GUIDE
    if not path.is_file():
        problems.append(f"{GUIDE} is missing")
    _, documentation = section_of(read(root / "README.md"), DOCUMENTATION)
    if f"]({GUIDE})" not in "\n".join(documentation):
        problems.append(f"README.md's list of documentation does not link {GUIDE}")
    if RANK not in " ".join(read(root / "CLAUDE.md").split()):
        problems.append("CLAUDE.md does not give the sentence on the guide's rank")
    if not path.is_file():
        return problems
    text = read(path)
    entries, form = entries_of(text)
    return (
        problems
        + opening_problems(text)
        + concern_problems(text, entries)
        + form
        + text_problems(root, text)
        + source_problems(entries)
        + held_by_problems(root, entries)
        + rests_on_problems(root, entries)
        + practice_problems(entries)
        + standing_problems(root, entries)
    )


def test_the_opening_and_the_sentence_on_the_guide_s_rank_are_those_that_r219_gives() -> None:
    spec = ROOT / "openspec/changes/add-pr-cost-calculator/specs/project-standards/spec.md"
    text = spec.read_text(encoding="utf-8")
    assert [line for line in OPENING if f'"{line}"' not in text] == []
    assert f'"{RANK}"' in text
    assert f'"{LAST_READ}"' in text


@pytest.mark.xfail(strict=True, reason="task 5 of the plan writes the guide")
def test_the_repository_has_no_guide_problem() -> None:
    assert guide_problems(ROOT) == []


# A synthetic guide that has no problem, in the roadmap's synthetic tree. Each test plants
# one defect into it.

ENTRY = {
    "Statement": "What holds.",
    "Rationale": "Why it holds.",
    "Implications": "What follows from it.",
    "Pattern": "A pattern. Source: an author, a work.",
    "Anti-patterns": "What it steers clear of, and how to tell.",
    "Held by": "`c` task 1.2",
    "Rests on": "R1",
    "Where we stand": "Followed.",
}
# Each concern's entries, by heading, with the fields that differ from ENTRY.
ENTRIES: dict[str, dict[str, dict[str, str]]] = {
    "Architecture and integration": {
        "A thing is built first": {
            "Held by": "DR-001. Review: whether it was built first.",
            "Rests on": "R1, B-002",
            "Where we stand": "Gap. B-002 builds it.",
        },
        "Another thing is accepted": {
            "Held by": "DR-003",
            "Rests on": "DR-003",
            "Where we stand": "Knowingly accepted. DR-003 gives why.",
        },
    },
    "Security": {
        "Each input is checked": {
            "Pattern": "OWASP Secure Coding Practices. Source: OWASP Foundation, a guide.",
            "Held by": "DR-001",
            "Rests on": "DR-001, T1",
            "Where we stand": "Knowingly accepted. DR-001 gives why.",
        },
    },
    "Privacy": {
        "Counts, never content": {
            "Held by": "`c` task 1.1 and `c` task 1.2",
            "Where we stand": "Designed.",
        },
    },
    "Identity and credentials": {
        "Least privilege": {
            "Pattern": "Least privilege. Source: the Token-Permissions check of OpenSSF Scorecard.",
        },
    },
    "Supply chain and releases": {
        "Pinned and locked": {
            "Held by": "`README.md`",
            "Rests on": "B-001",
            "Where we stand": "Gap. B-001 pins it.",
        },
    },
    "Testing": {
        "Tests come first": {
            "Held by": '`thing`: "A thing holds"',
            "Rests on": "A1, task 1.2 of `c`",
        },
    },
    "Decisions and documentation": {
        "Records are closed, not edited": {
            "Rests on": "DR-001",
            "Where we stand": "Gap. B-003 closes it.",
        },
    },
    "Working with agents": {
        "Data never instructs": {"Held by": "`CLAUDE.md`"},
    },
    "Conventions": {
        "Code reads as its style asks": {
            "Pattern": "PEP 8 and Clean Code. Source: Guido van Rossum, PEP 8, and Robert C. "
            "Martin, Clean Code.",
            "Held by": "Review: whether the code reads as PEP 8 asks.",
        },
    },
}
OPENING_TEXT = (
    "".join(f"{line}\n\n" for line in OPENING) + f"{LAST_READ}the assessment of 2026-01-01.\n"
)


def synthetic(changed: dict[str, dict[str, str | None]] | None = None) -> str:
    """The synthetic guide, with the fields that `changed` gives for an entry by its
    heading, a field given as None left out."""
    text = OPENING_TEXT
    for concern, entries in ENTRIES.items():
        text += f"\n## {concern}\n"
        for heading, values in entries.items():
            fields = {**ENTRY, **values, **(changed or {}).get(heading, {})}
            text += f"\n### {heading}\n\n"
            text += "".join(
                f"- **{name}:** {value}\n" for name, value in fields.items() if value is not None
            )
    return text


GUIDE_TEXT = synthetic()
README = TREE["README.md"] + f"- [How the project builds]({GUIDE}): the guide.\n"
FILES = {
    "README.md": README,
    "CLAUDE.md": f"# CLAUDE.md\n\n- {RANK}\n",
    "CHANGELOG.md": "# Changelog\n",
    "docs/decisions/DR-001-a.md": (
        "# DR-001: A\n\n- **Decided by:** the owner, 2026-01-01\n- **Closed by:** none\n"
    ),
    "docs/decisions/DR-003-c.md": (
        "# DR-003: C\n\n- **Decided by:** the change `c`\n- **Closed by:** none\n"
    ),
    "openspec/specs/thing/spec.md": "# thing\n\n#### Scenario: A thing holds\n",
}


def guide_tree(
    root: Path, guide: str | None = GUIDE_TEXT, changed: dict[str, str | None] | None = None
) -> Path:
    return make_tree(root, {**FILES, GUIDE: guide, **(changed or {})})


def line_of(text: str, part: str) -> int:
    """The number of the line on which a part of the text starts."""
    assert text.count(part) == 1, part
    return text[: text.index(part)].count("\n") + 1


def named(heading: str, text: str = GUIDE_TEXT) -> str:
    """How a problem names an entry: by the guide's line that heads it, and its heading."""
    number = line_of(text, "### " + heading + "\n")
    return f'{GUIDE}:{number} "{heading}"'


def test_a_complete_guide_has_no_problem(tmp_path: Path) -> None:
    assert guide_problems(guide_tree(tmp_path)) == []


# R219: the guide's links, its opening and its concerns.


def test_a_missing_guide_is_reported_alone(tmp_path: Path) -> None:
    assert guide_problems(guide_tree(tmp_path, None)) == [f"{GUIDE} is missing"]


def test_a_readme_that_does_not_link_the_guide_is_reported(tmp_path: Path) -> None:
    root = guide_tree(tmp_path, changed={"README.md": TREE["README.md"]})
    assert guide_problems(root) == [f"README.md's list of documentation does not link {GUIDE}"]


def test_a_claude_md_without_the_sentence_on_the_guide_s_rank_is_reported(tmp_path: Path) -> None:
    root = guide_tree(tmp_path, changed={"CLAUDE.md": "# CLAUDE.md\n"})
    assert guide_problems(root) == ["CLAUDE.md does not give the sentence on the guide's rank"]


def test_a_guide_without_its_opening_is_reported_at_its_first_line(tmp_path: Path) -> None:
    root = guide_tree(tmp_path, GUIDE_TEXT.replace(OPENING_TEXT + "\n", ""))
    found = guide_problems(root)
    assert f"{GUIDE}:1 differs from the opening, which gives {OPENING[0]!r} there" in found


@pytest.mark.parametrize(
    ("old", "new", "number"),
    [
        ("concern by concern:", "concern by concern;", 3),
        ("A gap is not, by being there,", "A gap is not, being there,", 11),
        ("\n\nThe guide steers", "\n\nAn added line.\n\nThe guide steers", 7),
    ],
)
def test_the_first_line_that_differs_from_the_opening_is_reported(
    tmp_path: Path, old: str, new: str, number: int
) -> None:
    found = guide_problems(guide_tree(tmp_path, GUIDE_TEXT.replace(old, new, 1)))
    want = OPENING_TEXT.split("\n")[number - 1]
    assert [p for p in found if "the opening" in p] == [
        f"{GUIDE}:{number} differs from the opening, which gives {want!r} there"
    ]


def test_a_line_added_after_the_opening_s_last_line_is_reported(tmp_path: Path) -> None:
    text = GUIDE_TEXT.replace("2026-01-01.\n", "2026-01-01.\n\nAn added line.\n", 1)
    assert f"{GUIDE}:15 adds a line to the opening" in guide_problems(guide_tree(tmp_path, text))


@pytest.mark.parametrize(
    "last", ["the last reading.", "release 1.2.", "the assessment of 2026-1-1."]
)
def test_a_last_line_that_names_no_assessment_or_release_is_reported(
    tmp_path: Path, last: str
) -> None:
    text = GUIDE_TEXT.replace("the assessment of 2026-01-01.", last, 1)
    found = guide_problems(guide_tree(tmp_path, text))
    assert found == [
        f"{GUIDE}:13 does not name the assessment or the release for which the entries were "
        "last read"
    ]


def test_a_last_line_that_names_a_release_passes(tmp_path: Path) -> None:
    text = GUIDE_TEXT.replace("the assessment of 2026-01-01.", "release 1.2.3.", 1)
    assert guide_problems(guide_tree(tmp_path, text)) == []


def concern_moved(text: str, concern: str, before: str | None) -> str:
    """The guide with a concern's section taken out, and put back before another's."""
    start = text.index(f"\n## {concern}\n")
    end = text.find("\n## ", start + 1)
    section = text[start : end if end >= 0 else len(text)]
    text = text.replace(section, "", 1)
    if before is None:
        return text
    at = text.index(f"\n## {before}\n")
    return text[:at] + section + text[at:]


def test_a_missing_concern_is_reported(tmp_path: Path) -> None:
    root = guide_tree(tmp_path, concern_moved(GUIDE_TEXT, "Privacy", None))
    assert guide_problems(root) == [f"{GUIDE} has no section Privacy"]


def test_a_repeated_concern_is_reported(tmp_path: Path) -> None:
    again = "".join(f"- **{name}:** {value}\n" for name, value in ENTRY.items())
    again = f"\n## Security\n\n### Another check\n\n{again}\n## Privacy\n"
    text = GUIDE_TEXT.replace("\n## Privacy\n", again, 1)
    found = guide_problems(guide_tree(tmp_path, text))
    assert found == [f"{GUIDE} gives the section Security more than once"]


def test_concerns_out_of_order_are_reported(tmp_path: Path) -> None:
    root = guide_tree(tmp_path, concern_moved(GUIDE_TEXT, "Privacy", "Security"))
    order = ", ".join(["Architecture and integration", "Privacy", "Security", *CONCERNS[3:]])
    assert guide_problems(root) == [f"{GUIDE} gives its sections out of order: {order}"]


def test_a_section_that_is_no_concern_is_reported(tmp_path: Path) -> None:
    text = GUIDE_TEXT + "\n## Notes\n"
    assert guide_problems(guide_tree(tmp_path, text)) == [
        f"{GUIDE} has a section Notes, which is not a concern of the guide"
    ]


def test_a_concern_with_no_entry_is_reported(tmp_path: Path) -> None:
    start = GUIDE_TEXT.index("\n### Counts, never content\n")
    end = GUIDE_TEXT.index("\n## Identity and credentials\n")
    text = GUIDE_TEXT[:start] + GUIDE_TEXT[end:]
    assert guide_problems(guide_tree(tmp_path, text)) == [f"{GUIDE}: Privacy holds no entry"]


# R220: each entry gives its fields, and says where the project stands.


def test_text_in_a_section_outside_its_entries_is_reported(tmp_path: Path) -> None:
    text = GUIDE_TEXT.replace("\n## Security\n", "\n## Security\n\nSome text.\n", 1)
    number = line_of(text, "Some text.")
    assert guide_problems(guide_tree(tmp_path, text)) == [
        f"{GUIDE}:{number} holds text in Security outside its entries"
    ]


def test_text_in_an_entry_that_is_no_field_is_reported(tmp_path: Path) -> None:
    text = GUIDE_TEXT.replace("Least privilege. Source:", "Least privilege.\nA note. Source:", 1)
    number = line_of(text, "A note.")
    found = guide_problems(guide_tree(tmp_path, text))
    assert (
        f'{GUIDE}:{number} holds text in "Least privilege" that is not one of its fields' in found
    )


@pytest.mark.parametrize("left_out", ["Statement", "Rationale", "Where we stand"])
def test_an_entry_that_leaves_out_a_field_is_reported(tmp_path: Path, left_out: str) -> None:
    text = synthetic({"Data never instructs": {left_out: None}})
    given = ", ".join(name for name in FIELDS if name != left_out)
    assert (
        f"{named('Data never instructs', text)} gives the fields {given}, where an entry gives "
        "each of its eight once, in order"
    ) in guide_problems(guide_tree(tmp_path, text))


@pytest.mark.parametrize(
    ("old", "new"),
    [
        (
            "- **Statement:** What holds.\n",
            "- **Statement:** What holds.\n- **Statement:** Again.\n",
        ),
        (
            "- **Statement:** What holds.\n- **Rationale:** Why it holds.\n",
            "- **Rationale:** Why it holds.\n- **Statement:** What holds.\n",
        ),
        ("- **Statement:** What holds.\n", "- **Statement:** What holds.\n- **Notes:** A note.\n"),
    ],
)
def test_an_entry_that_repeats_a_field_or_gives_them_out_of_order_is_reported(
    tmp_path: Path, old: str, new: str
) -> None:
    head = "### Data never instructs\n\n"
    text = GUIDE_TEXT.replace(head + old, head + new, 1)
    assert text != GUIDE_TEXT
    found = guide_problems(guide_tree(tmp_path, text))
    entry = named("Data never instructs", text)
    assert [p for p in found if p.startswith(f"{entry} gives the fields ")], found


@pytest.mark.parametrize("empty", ["- **Statement:** ", "- **Statement:**", "- **Statement:**   "])
def test_an_empty_field_is_reported(tmp_path: Path, empty: str) -> None:
    head = "### Data never instructs\n\n"
    text = GUIDE_TEXT.replace(head + "- **Statement:** What holds.", head + empty, 1)
    found = guide_problems(guide_tree(tmp_path, text))
    assert found == [f"{named('Data never instructs', text)} leaves Statement empty"]


def test_a_repeated_heading_is_reported(tmp_path: Path) -> None:
    text = GUIDE_TEXT.replace("### Counts, never content", "### Least privilege", 1)
    first = text.index("### Least privilege\n")
    number = text[: text.index("### Least privilege\n", first + 1)].count("\n") + 1
    found = guide_problems(guide_tree(tmp_path, text))
    assert f'{GUIDE}:{number} repeats the heading "Least privilege"' in found


@pytest.mark.parametrize("standing", ["Mostly followed.", "followed.", "Followed", "Gaps. B-001."])
def test_a_where_we_stand_that_opens_with_none_of_its_words_is_reported(
    tmp_path: Path, standing: str
) -> None:
    text = synthetic({"Least privilege": {"Where we stand": standing}})
    assert guide_problems(guide_tree(tmp_path, text)) == [
        f"{named('Least privilege')} opens Where we stand with none of Followed., Designed., "
        "Knowingly accepted. and Gap."
    ]


def test_an_entry_on_working_with_agents_that_does_not_cite_claude_md_is_reported(
    tmp_path: Path,
) -> None:
    text = synthetic({"Data never instructs": {"Held by": "DR-001"}})
    assert guide_problems(guide_tree(tmp_path, text)) == [
        f"{named('Data never instructs')} is under Working with agents and does not cite "
        "`CLAUDE.md` in Held by"
    ]


# R221: the guide links only this repository's own files and holds no hidden text.


def planted(new: str) -> str:
    """The guide with a line planted at its end, inside its last entry."""
    return GUIDE_TEXT + new + "\n"


@pytest.mark.parametrize(("new", "problem"), LINKS_ELSEWHERE)
def test_a_link_elsewhere_in_the_guide_is_reported(tmp_path: Path, new: str, problem: str) -> None:
    found = guide_problems(guide_tree(tmp_path, planted(new)))
    assert [p for p in found if p.startswith(GUIDE) and problem in p], found


@pytest.mark.parametrize(("new", "problem"), HIDDEN_TEXT)
def test_hidden_text_in_the_guide_is_reported(tmp_path: Path, new: str, problem: str) -> None:
    found = guide_problems(guide_tree(tmp_path, planted(new)))
    assert [p for p in found if p.startswith(GUIDE) and problem in p], found


@pytest.mark.parametrize(
    ("new", "problem"),
    [
        ("It costs $5.", "holds $ outside inline code, with which GitHub shows mathematics"),
        (
            "It takes ~5 days.",
            "holds ~ outside inline code, with which GitHub strikes text through",
        ),
        ("`a` ~~b~~ `c`", "holds ~ outside inline code, with which GitHub strikes text through"),
    ],
)
def test_a_dollar_or_a_tilde_outside_inline_code_is_reported(
    tmp_path: Path, new: str, problem: str
) -> None:
    text = planted(new)
    found = guide_problems(guide_tree(tmp_path, text))
    assert f"{GUIDE}:{line_of(text, new)} {problem}" in found


def test_a_dollar_or_a_tilde_in_inline_code_passes(tmp_path: Path) -> None:
    text = GUIDE_TEXT.replace("What holds.", "What `$HOME` and `~x` hold.", 1)
    assert guide_problems(guide_tree(tmp_path, text)) == []


def test_the_opening_s_inline_code_passes_only_as_the_opening_gives_it(tmp_path: Path) -> None:
    text = GUIDE_TEXT.replace("when the default branch's code", "when the code", 1)
    found = guide_problems(guide_tree(tmp_path, text))
    assert found.count(f"{GUIDE}:9 holds inline code that holds a space, as a command does") == 2


@pytest.mark.parametrize(
    "held", ["`vendor/a/SKILL.md`", "`.claude/skills/a/SKILL.md`", "`vendor`", "`vendor/`"]
)
def test_a_held_by_that_cites_a_file_that_others_write_is_reported(
    tmp_path: Path, held: str
) -> None:
    text = synthetic({"Least privilege": {"Held by": held}})
    path = held.strip("`")
    folder = "vendor/" if path.startswith("vendor") else ".claude/skills/"
    assert (
        f"{named('Least privilege')} cites `{path}` in Held by, under {folder}, whose files "
        "others write"
    ) in guide_problems(guide_tree(tmp_path, text))


# R222: each entry gives its source, what holds it and what it rests on.


@pytest.mark.parametrize("pattern", ["Test first.", "Test first. Source:", "Test first. Source:  "])
def test_an_entry_with_no_source_is_reported(tmp_path: Path, pattern: str) -> None:
    text = synthetic({"Tests come first": {"Pattern": pattern}})
    assert guide_problems(guide_tree(tmp_path, text)) == [
        f"{named('Tests come first')} gives no source after Source: in its Pattern"
    ]


@pytest.mark.parametrize(
    ("held", "problem"),
    [
        ("`c` task 9.9", "cites `c` task 9.9, which does not exist"),
        ("DR-099", "cites DR-099, which is not a decision record"),
        ("`nowhere`", "cites `nowhere`, which is not a file in this repository"),
        ('`thing`: "No such thing"', 'cites `thing`: "No such thing", which no spec holds'),
        ("`c` decision 9", "cites `c` decision 9, which does not exist"),
        ("Nothing that holds it.", "cites nothing in Held by and gives nothing after Review:"),
        ("Review:", "cites nothing in Held by and gives nothing after Review:"),
        ("Review:   ", "cites nothing in Held by and gives nothing after Review:"),
    ],
)
def test_a_held_by_that_holds_nothing_that_resolves_is_reported(
    tmp_path: Path, held: str, problem: str
) -> None:
    text = synthetic({"Tests come first": {"Held by": held}})
    assert f"{named('Tests come first')} {problem}" in guide_problems(guide_tree(tmp_path, text))


@pytest.mark.parametrize(
    ("rests", "problem"),
    [
        ("none", "rests on none"),
        ("R1; R2", "names R1; R2 in Rests on, which is not an ID in a form that it takes"),
        ("DR-1", "names DR-1 in Rests on, which is not an ID in a form that it takes"),
        ("task 1.2 of c", "names task 1.2 of c in Rests on, which is not an ID in a form that"),
        ("R99", "names R99, which the register does not hold"),
        ("T99", "names T99, which the threat model does not hold"),
        ("A99", "names A99, which docs/assumptions/ does not hold"),
        ("B-099", "names B-099, which docs/backlog does not hold"),
        ("DR-099", "names DR-099, which docs/decisions/ does not hold"),
        ("DR-002", "names DR-002, which is closed"),
        ("task 9.9 of `c`", "names task 9.9 of `c`, which no change's tasks.md holds"),
    ],
)
def test_a_rests_on_that_names_nothing_that_holds_is_reported(
    tmp_path: Path, rests: str, problem: str
) -> None:
    text = synthetic({"Tests come first": {"Rests on": rests}})
    found = guide_problems(guide_tree(tmp_path, text))
    assert len(found) == 1 and found[0].startswith(f"{named('Tests come first')} {problem}"), found


@pytest.mark.parametrize("practice", PRACTICES)
def test_a_named_practice_left_out_is_reported(tmp_path: Path, practice: str) -> None:
    text = GUIDE_TEXT.replace(practice, "Another practice")
    assert guide_problems(guide_tree(tmp_path, text)) == [f"no entry's Pattern names {practice}"]


# R226: where the guide says the project stands is held true.


def test_followed_with_a_task_that_is_not_ticked_is_reported(tmp_path: Path) -> None:
    text = synthetic({"Least privilege": {"Held by": "`c` task 1.2 and `c` task 1.1"}})
    assert guide_problems(guide_tree(tmp_path, text)) == [
        f"{named('Least privilege')} is Followed. while `c` task 1.1, which its Held by cites, "
        "is not ticked"
    ]


@pytest.mark.parametrize("held", ["`c` task 1.2", "DR-001", "`c` task 1.2 and DR-001"])
def test_designed_with_no_task_that_is_not_ticked_is_reported(tmp_path: Path, held: str) -> None:
    text = synthetic({"Counts, never content": {"Held by": held}})
    assert guide_problems(guide_tree(tmp_path, text)) == [
        f"{named('Counts, never content')} is Designed. while its Held by cites no task that "
        "is not ticked"
    ]


@pytest.mark.parametrize(
    "standing",
    [
        "Knowingly accepted. For a reason.",
        "Knowingly accepted. DR-099 gives why.",
        "Knowingly accepted. DR-002 gave why.",
    ],
)
def test_knowingly_accepted_without_an_accepted_record_is_reported(
    tmp_path: Path, standing: str
) -> None:
    text = synthetic({"Another thing is accepted": {"Where we stand": standing}})
    assert guide_problems(guide_tree(tmp_path, text)) == [
        f"{named('Another thing is accepted')} is Knowingly accepted. and names no accepted record"
    ]


@pytest.mark.parametrize(
    ("standing", "problem"),
    [
        ("Gap. Someone builds it.", "is a Gap. and names no backlog item"),
        ("Gap. B-099 builds it.", "names B-099, which docs/backlog does not hold"),
        ("Gap. B-004 built it.", "names B-004, which is Done"),
        ("Gap. B-005 would have.", "names B-005, which is Dropped"),
    ],
)
def test_a_gap_without_an_open_backlog_item_is_reported(
    tmp_path: Path, standing: str, problem: str
) -> None:
    text = synthetic({"A thing is built first": {"Where we stand": standing}})
    assert guide_problems(guide_tree(tmp_path, text)) == [
        f"{named('A thing is built first')} {problem}"
    ]


FIRST_ENTRY = {concern: next(iter(entries)) for concern, entries in ENTRIES.items()}
# Written out, not taken from RELIED_ON, so that a concern dropped from it fails a test.
ADOPTERS_RELY_ON = ("Security", "Privacy", "Identity and credentials", "Supply chain and releases")


@pytest.mark.parametrize("concern", CONCERNS)
def test_only_the_owner_s_record_accepts_a_risk_that_adopters_rely_on(
    tmp_path: Path, concern: str
) -> None:
    heading = FIRST_ENTRY[concern]
    standing = "Knowingly accepted. DR-001 and DR-003 give why."
    held = "`CLAUDE.md`" if concern == "Working with agents" else "DR-001"
    text = synthetic({heading: {"Held by": held, "Where we stand": standing}})
    found = guide_problems(guide_tree(tmp_path, text))
    if concern in ADOPTERS_RELY_ON:
        assert found == [
            f"{named(heading)} is under {concern}, which adopters rely on, and is accepted with "
            "DR-003, which the owner did not decide"
        ]
    else:
        assert found == []


@pytest.mark.parametrize("concern", CONCERNS)
def test_only_an_agreed_item_closes_a_gap_that_adopters_rely_on(
    tmp_path: Path, concern: str
) -> None:
    heading = FIRST_ENTRY[concern]
    text = synthetic({heading: {"Where we stand": "Gap. B-001 and B-002 close it."}})
    found = guide_problems(guide_tree(tmp_path, text))
    if concern in ADOPTERS_RELY_ON:
        assert found == [
            f"{named(heading)} is under {concern}, which adopters rely on, and names B-002, which "
            "is Open to feedback and contributions, not Planned or In progress"
        ]
    else:
        assert found == []
