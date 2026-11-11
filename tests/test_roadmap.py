"""The roadmap says what is now, next and later, and leads only to this repository.

`docs/roadmap.md` is linked from the README's list of documentation, and its
sections are Now, Next, Later, Known limitations and Known bugs, each once and in
that order (R206, DR-218). A section is a `## ` line at the start of a line, read
outside fenced code; the roadmap holds no heading indented or underlined. An item is
a line that starts with `- `, with the lines indented by two spaces that follow it.

Each item under Next and Later opens with `**Planned.**` or `**Open to feedback and
contributions.**` (R207, DR-219), and names what it rests on: a requirement (`R`
and digits) that the register holds, a record (`DR-` and three digits) that
`docs/decisions/` holds, a threat (`T` and digits) that the threat model holds, or
a task, as `task 1.26 of` and the change's name as code, that a change's
`tasks.md`, active or archived, holds. Under Next and Later, a list item in any
other form, or a line that is neither an item nor part of one after the first item,
fails. An item in any section that names what does not exist fails, and so does
one whose named tasks are all ticked, or that names a closed record, which is stale
(R206, T161). No test reads an issue, so whether an issue that an item names is
still open rests on review. Later opens with the sentence that `LATER_OPENING`
gives, and each record that the README's list of what the first version does not
support links is named by an item under Later; a README whose list links no record
fails (R207).

Every risk that the risks and trade-offs of a change's design give, active or
archived, as a line that opens with `- [title]` and an arrow, is listed by its
title, as a line `- **title**: ...`, under Known limitations or in the section on
known limitations and the roadmap of a page in `docs/features/` named for a spec.
A line under a design's risks that starts with `- ` in another form fails, and so
does a design without that section, or two changes of one name. Each such page has
that section, once, which links the roadmap, and Known limitations says that it is
a short list and links each section. A listed title that no design gives fails too
(R208, DR-220, T162).

Every link in the roadmap, and in each feature page's section, is read from its
`](` over the whole text, whatever its text holds, and names a heading of its page,
or a tracked file of this repository by a relative path that stays inside it, with
a heading of that file when the link names one, and gives no title. The pages give
no web address, no `@`, no image, no fenced or indented code, and no `owner/repo`
that is not a tracked file's path from the repository's root, in prose and code
alike, so that issues and pull requests are named by number alone (R209, DR-221,
DR-224, T160, T163, T164). They hold printable ASCII and line feeds only, and no
`<`, `&`, backslash or `]:`, inline code included (R210, T165).

Each check is shown to fail on a synthetic tree, a git repository so that its
tracked files can be read, into which the defect is planted.
"""

from __future__ import annotations

import os
import posixpath
import re
import subprocess
from dataclasses import dataclass, replace
from pathlib import Path
from urllib.parse import unquote

import pytest
from spec_form import find_specs

ROOT = Path(__file__).resolve().parents[1]

ROADMAP = "docs/roadmap.md"
SECTIONS = ("Now", "Next", "Later", "Known limitations", "Known bugs")
MARKED = ("Next", "Later")
MARKS = ("**Planned.**", "**Open to feedback and contributions.**")
LATER_OPENING = (
    "Work on an item here starts with an issue on which the owner agrees, and some items "
    "need a spec, a threat review and the owner's decision first."
)
SHORT_LIST = "This is a short list."
FEATURE_SECTION = "Known limitations and the roadmap"
NOT_SUPPORTED = "Not supported in this first version"
DOCUMENTATION = "Documentation"
RISKS = "Risks / Trade-offs"

HEADING = re.compile(r"^(#{1,6}) +(.+?) *$")
FENCE = re.compile(r"^ *(```|~~~)")
MISPLACED_HEADING = re.compile(r"^ {1,3}#{1,6}( |$)|^ {0,3}(=+|-+) *$")
LIST_MARKER = re.compile(r"^ *([-*+]|\d+[.)])( |$)")
REQUIREMENT_NAME = re.compile(r"\bR\d+\b")
RECORD_NAME = re.compile(r"\bDR-\d{3}\b")
THREAT_NAME = re.compile(r"\bT\d+\b")
TASK_NAME = re.compile(r"\btask (\d+\.\d+) of `([a-z0-9-]+)`")
REGISTER_ROW = re.compile(r"^\| (R\d+) \| ", re.M)
THREAT_HEADING = re.compile(r"^### (T\d+)\. ", re.M)
RECORD_FILE = re.compile(r"(DR-\d{3})-[a-z0-9-]+\.md")
CLOSED_BY = re.compile(r"^- \*\*Closed by:\*\* (.+?) *$", re.M)
TASK_LINE = re.compile(r"^- \[([ xX])\] (\d+\.\d+) ", re.M)
ARCHIVED = re.compile(r"\d{4}-\d{2}-\d{2}-(.+)")
RISK = re.compile(r"^- \[(.+?)\] \u2192 ")
LISTED = re.compile(r"^- \*\*(.+?)\*\*: ", re.M)
# A link's target, read from its `](` whatever stands before it, over line breaks.
TARGET = re.compile(r"\]\(([^)]*)\)")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
# A web address in a form that GitHub links or that an agent could follow.
WEB_ADDRESS = re.compile(r"//|(?<![A-Za-z0-9.-])www\.|(?:\]\(|<)\s*[a-z][a-z0-9+.-]*:", re.I)
OWNER_REPO = re.compile(r"(?<![\w.-])/?[\w.-]+(?:/[\w.-]+)+/?")
EMPHASIZED_PATH = re.compile(r"[*_]/|/[*_]")
HIDING = (
    ("<", "<, with which Markdown starts HTML"),
    ("&", "&, with which Markdown writes a character by its code"),
    ("\\", "a backslash, with which Markdown undoes what a mark does"),
    ("]:", "]:, with which Markdown defines a link that it does not show"),
)

GIT_ENVIRONMENT = {
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
}


@dataclass(frozen=True)
class Item:
    line: int
    text: str


def session_free_environment() -> dict[str, str]:
    """The environment with no git variable of the session's, such as an index file,
    that would make git read another repository than the one it runs in."""
    return {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}


def tracked(root: Path) -> set[str]:
    done = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
        env=session_free_environment(),
    )
    return {name for name in done.stdout.decode().split("\0") if name}


def read(path: Path) -> str:
    """A file's text with its line endings as written, so that a carriage return shows."""
    return path.read_bytes().decode("utf-8") if path.is_file() else ""


def unfenced(text: str) -> list[tuple[int, str]]:
    """Each line's number and text, outside fenced code."""
    found = []
    fence = ""
    for number, line in enumerate(text.split("\n"), 1):
        opened = FENCE.match(line)
        if fence:
            if opened and opened.group(1) == fence:
                fence = ""
        elif opened:
            fence = opened.group(1)
        else:
            found.append((number, line))
    return found


def sections(text: str) -> list[tuple[str, int, list[str]]]:
    """Each `## ` section outside fenced code: its heading, the number of its first
    line, and its lines."""
    found: list[tuple[str, int, list[str]]] = []
    lines = text.split("\n")
    heads = [
        (number, heading.group(2))
        for number, line in unfenced(text)
        if (heading := HEADING.match(line)) and heading.group(1) == "##"
    ]
    for index, (number, name) in enumerate(heads):
        end = heads[index + 1][0] - 1 if index + 1 < len(heads) else len(lines)
        found.append((name, number + 1, lines[number:end]))
    return found


def section_of(text: str, name: str) -> tuple[int, list[str]]:
    for heading, start, lines in sections(text):
        if heading == name:
            return start, lines
    return 0, []


def items(start: int, lines: list[str]) -> tuple[list[str], list[Item]]:
    """A section's opening lines, before its first item, and its items."""
    opening: list[str] = []
    found: list[Item] = []
    for offset, line in enumerate(lines):
        if line.startswith("- "):
            found.append(Item(start + offset, line))
        elif found and line.startswith("  ") and line.strip():
            found[-1] = replace(found[-1], text=f"{found[-1].text}\n{line.strip()}")
        elif not found:
            opening.append(line)
    return opening, found


def slug(heading: str) -> str:
    text = heading.replace("`", "").lower()
    text = re.sub(r"[^a-z0-9 _-]", "", text)
    return text.replace(" ", "-")


FEATURE_ANCHOR = slug(FEATURE_SECTION)


def anchors(text: str) -> set[str]:
    return {
        slug(heading.group(2)) for _, line in unfenced(text) if (heading := HEADING.match(line))
    }


def records(root: Path) -> dict[str, bool]:
    """Each record's ID, and whether it is closed."""
    found = {}
    for path in sorted((root / "docs" / "decisions").glob("DR-*.md")):
        name = RECORD_FILE.fullmatch(path.name)
        if not name:
            continue
        closer = CLOSED_BY.search(read(path))
        found[name.group(1)] = closer is not None and closer.group(1) != "none"
    return found


def changes(root: Path) -> list[tuple[str, Path]]:
    """Each change's name and folder, active or archived."""
    folder = root / "openspec" / "changes"
    found = [
        (path.name, path)
        for path in sorted(folder.glob("*"))
        if path.is_dir() and path.name != "archive"
    ]
    for path in sorted((folder / "archive").glob("*")):
        named = ARCHIVED.fullmatch(path.name)
        if path.is_dir() and named:
            found.append((named.group(1), path))
    return found


def change_problems(root: Path) -> list[str]:
    names = [name for name, _ in changes(root)]
    return [
        f"two changes are named `{name}`, so a task cannot be named by its change"
        for name in sorted({name for name in names if names.count(name) > 1})
    ]


def tasks(root: Path) -> dict[tuple[str, str], bool]:
    """Each task, by its change and number, and whether it is ticked."""
    found = {}
    for name, path in changes(root):
        for tick, number in TASK_LINE.findall(read(path / "tasks.md")):
            found[(name, number)] = tick != " "
    return found


def section_problems(root: Path) -> list[str]:
    roadmap = root / ROADMAP
    problems = []
    if not roadmap.is_file():
        problems.append(f"{ROADMAP} is missing")
    else:
        text = read(roadmap)
        found = [heading for heading, _, _ in sections(text)]
        problems += [f"{ROADMAP} has no section {name}" for name in SECTIONS if name not in found]
        problems += [
            f"{ROADMAP} has a section {name}, which a roadmap does not keep"
            for name in found
            if name not in SECTIONS
        ]
        if not problems and found != list(SECTIONS):
            problems.append(f"{ROADMAP} gives its sections out of order: {', '.join(found)}")
        problems += [
            f"{ROADMAP}:{number} holds a heading that is indented or underlined"
            for number, line in unfenced(text)
            if MISPLACED_HEADING.match(line)
        ]
    _, documentation = section_of(read(root / "README.md"), DOCUMENTATION)
    if f"]({ROADMAP})" not in "\n".join(documentation):
        problems.append(f"README.md's list of documentation does not link {ROADMAP}")
    return problems


def form_problems(name: str, start: int, lines: list[str]) -> list[str]:
    """Under Next and Later: no list item but `- ` at the start of a line, and no line
    after the first item that is neither an item nor part of one."""
    problems = []
    begun = False
    for offset, line in enumerate(lines):
        where = f"{ROADMAP}:{start + offset}"
        if line.startswith("- "):
            begun = True
        elif LIST_MARKER.match(line):
            problems.append(f"{where} gives a list item under {name} in a form other than `- `")
        elif begun and line.strip() and not line.startswith("  "):
            problems.append(
                f"{where} holds a line under {name} that is neither an item nor part of one"
            )
    return problems


def item_problems(root: Path) -> list[str]:
    text = read(root / ROADMAP)
    register = set(REGISTER_ROW.findall(read(root / "docs" / "requirements.md")))
    threats = set(THREAT_HEADING.findall(read(root / "docs" / "threat-model.md")))
    held = records(root)
    listed = tasks(root)
    problems = []
    for name in SECTIONS:
        start, lines = section_of(text, name)
        if name in MARKED:
            problems += form_problems(name, start, lines)
        for item in items(start, lines)[1]:
            where = f"{ROADMAP}:{item.line}"
            requirements = REQUIREMENT_NAME.findall(item.text)
            named = RECORD_NAME.findall(item.text)
            threat_names = THREAT_NAME.findall(item.text)
            task_names = [(change, number) for number, change in TASK_NAME.findall(item.text)]
            if name in MARKED:
                if not item.text.startswith(tuple(f"- {mark} " for mark in MARKS)):
                    problems.append(
                        f"{where} has an item under {name} that opens with neither mark"
                    )
                if not (requirements or named or threat_names or task_names):
                    problems.append(
                        f"{where} has an item under {name} that names no requirement, record, "
                        "threat or task"
                    )
            problems += [
                f"{where} names {ident}, which the register does not hold"
                for ident in requirements
                if ident not in register
            ]
            problems += [
                f"{where} names {ident}, which docs/decisions/ does not hold"
                for ident in named
                if ident not in held
            ]
            problems += [
                f"{where} names {ident}, which the threat model does not hold"
                for ident in threat_names
                if ident not in threats
            ]
            problems += [
                f"{where} names task {number} of `{change}`, which no change's tasks.md holds"
                for change, number in task_names
                if (change, number) not in listed
            ]
            problems += [
                f"{where} names {ident}, which is closed" for ident in named if held.get(ident)
            ]
            if task_names and all(listed.get(task, False) for task in task_names):
                problems.append(f"{where} names only finished tasks")
    return problems


def later_problems(root: Path) -> list[str]:
    text = read(root / ROADMAP)
    start, lines = section_of(text, "Later")
    opening, found = items(start, lines)
    problems = []
    if LATER_OPENING not in " ".join(line.strip() for line in opening):
        problems.append(f"{ROADMAP}: Later does not open with how work on an item starts")
    named = {ident for item in found for ident in RECORD_NAME.findall(item.text)}
    _, unsupported = section_of(read(root / "README.md"), NOT_SUPPORTED)
    linked = sorted(set(RECORD_NAME.findall("\n".join(unsupported))))
    if not linked:
        problems.append(
            "README.md's list of what the first version does not support links no record"
        )
    for ident in linked:
        if ident not in named:
            problems.append(
                f"no item under Later names {ident}, which the README's list of what the "
                "first version does not support links"
            )
    return problems


def feature_pages(root: Path) -> list[Path]:
    names = {spec.ident for spec in find_specs(root)[0]}
    folder = root / "docs" / "features"
    return [page for page in sorted(folder.glob("*.md")) if page.stem in names]


def risks(root: Path) -> tuple[dict[str, str], list[str]]:
    """Each risk's title, and the design that gives it, from every change, and the
    problems of form in the designs' risks."""
    found: dict[str, str] = {}
    problems = []
    for _, path in changes(root):
        design = path / "design.md"
        if not design.is_file():
            continue
        name = design.relative_to(root).as_posix()
        start, lines = section_of(read(design), RISKS)
        if not start:
            problems.append(f"{name} has no section {RISKS}")
        for offset, line in enumerate(lines):
            risk = RISK.match(line)
            if risk:
                found.setdefault(risk.group(1), name)
            elif line.startswith("- "):
                problems.append(
                    f"{name}:{start + offset} gives a risk in a form the test does not read"
                )
    return found, problems


def risk_problems(root: Path) -> list[str]:
    roadmap = read(root / ROADMAP)
    _, limitations = section_of(roadmap, "Known limitations")
    known = "\n".join(limitations)
    given, problems = risks(root)
    listed: set[str] = set()
    if SHORT_LIST not in known:
        problems.append(f"{ROADMAP}'s Known limitations does not say that it is a short list")
    pages: list[tuple[str, str]] = [(ROADMAP, known)]
    targets = set(TARGET.findall(known))
    for page in feature_pages(root):
        name = page.relative_to(root).as_posix()
        found = [heading for heading, _, _ in sections(read(page))]
        if found.count(FEATURE_SECTION) > 1:
            problems.append(
                f"{name} has more than one section on known limitations and the roadmap"
            )
        _, lines = section_of(read(page), FEATURE_SECTION)
        if not lines:
            problems.append(f"{name} has no section on known limitations and the roadmap")
            continue
        body = "\n".join(lines)
        pages.append((name, body))
        if not any(link.split("#")[0] == "../roadmap.md" for link in TARGET.findall(body)):
            problems.append(
                f"{name}'s section on known limitations and the roadmap does not link the roadmap"
            )
        if f"features/{page.name}#{FEATURE_ANCHOR}" not in targets:
            problems.append(f"{ROADMAP}'s Known limitations does not link {name}'s section")
    for name, body in pages:
        for title in LISTED.findall(body):
            listed.add(title)
            if title not in given:
                problems.append(f"{name} lists {title!r}, which no change's design gives as a risk")
    problems += [
        f"the risk {title!r} of {design} is listed neither on the roadmap nor on a feature page"
        for title, design in given.items()
        if title not in listed
    ]
    return problems


def checked_text(root: Path) -> list[tuple[str, str, int, list[str], str]]:
    """The text that R209 and R210 hold: the roadmap, and each feature page's section,
    each with its name, the folder its links resolve from, its first line's number, its
    lines, and its page's whole text, whose headings its links may name."""
    found = []
    roadmap = read(root / ROADMAP)
    if roadmap:
        found.append((ROADMAP, "docs", 1, roadmap.split("\n"), roadmap))
    for page in feature_pages(root):
        text = read(page)
        start, lines = section_of(text, FEATURE_SECTION)
        if lines:
            found.append((page.relative_to(root).as_posix(), "docs/features", start, lines, text))
    return found


def link_problems(root: Path) -> list[str]:
    files = tracked(root)
    problems = []
    for name, base, start, lines, page in checked_text(root):
        own = anchors(page)
        text = "\n".join(lines)
        for offset, line in enumerate(lines):
            where = f"{name}:{start + offset}"
            if FENCE.match(line):
                problems.append(f"{where} holds a fenced code block")
            if line.startswith("    "):
                problems.append(f"{where} holds indented code")
            if WEB_ADDRESS.search(line):
                problems.append(f"{where} gives a web address")
            if "@" in line:
                problems.append(f"{where} holds @, which GitHub turns into a link or a mention")
            if "![" in line:
                problems.append(f"{where} holds an image")
            if EMPHASIZED_PATH.search(line):
                problems.append(f"{where} marks a path with emphasis")
        unlinked = TARGET.sub("](", text).split("\n")
        for offset, line in enumerate(unlinked):
            for token in OWNER_REPO.findall(line):
                path = token.rstrip(".")
                if path not in files:
                    problems.append(
                        f"{name}:{start + offset} names {path}, which is not a tracked file of "
                        "this repository"
                    )
        found = list(TARGET.finditer(text))
        if text.count("](") != len(found):
            problems.append(f"{name} holds a link whose target this test cannot read")
        for target in found:
            where = f"{name}:{start + text.count(chr(10), 0, target.start())}"
            problems += target_problems(root, where, target.group(1), base, files, own)
    return problems


def target_problems(
    root: Path, where: str, target: str, base: str, files: set[str], own: set[str]
) -> list[str]:
    parts = target.split()
    if not parts:
        return [f"{where} gives a link with no target"]
    if len(parts) > 1:
        return [f"{where} holds a link with a title"]
    address = parts[0]
    if SCHEME.match(address) or address.startswith("//"):
        return [f"{where} links to {address}, a web address"]
    if address.startswith("#"):
        if address[1:] not in own:
            return [f"{where} links to {address}, which is not a heading of its page"]
        return []
    path, _, fragment = address.partition("#")
    path = unquote(path)
    if "\\" in path or path.startswith("/"):
        return [f"{where} links to {address}, which is not a relative path"]
    resolved = posixpath.normpath(posixpath.join(base, path))
    if resolved == ".." or resolved.startswith("../"):
        return [f"{where} links to {address}, which leaves the repository"]
    if resolved not in files or path.endswith("/"):
        return [f"{where} links to {address}, which is not a tracked file of this repository"]
    if fragment and fragment not in anchors(read(root / resolved)):
        return [f"{where} links to {address}, whose file has no such heading"]
    return []


def hidden_text_problems(root: Path) -> list[str]:
    problems = []
    for name, _, start, lines, _ in checked_text(root):
        for offset, line in enumerate(lines):
            where = f"{name}:{start + offset}"
            others = sorted({ord(c) for c in line if not " " <= c <= "~"})
            if others:
                problems.append(f"{where} holds {', '.join(f'U+{code:04X}' for code in others)}")
            problems += [f"{where} holds {what}" for mark, what in HIDING if mark in line]
    return problems


def roadmap_problems(root: Path) -> list[str]:
    return (
        section_problems(root)
        + change_problems(root)
        + item_problems(root)
        + later_problems(root)
        + risk_problems(root)
        + link_problems(root)
        + hidden_text_problems(root)
    )


def test_the_repository_has_no_roadmap_problem() -> None:
    assert roadmap_problems(ROOT) == []


def test_the_repository_gives_each_check_something_to_examine() -> None:
    """A check that examined nothing fails."""
    text = read(ROOT / ROADMAP)
    assert len(risks(ROOT)[0]) > 0
    assert len(feature_pages(ROOT)) > 0
    assert len(checked_text(ROOT)) == len(feature_pages(ROOT)) + 1
    _, unsupported = section_of(read(ROOT / "README.md"), NOT_SUPPORTED)
    assert RECORD_NAME.findall("\n".join(unsupported))
    for name in MARKED:
        start, lines = section_of(text, name)
        assert items(start, lines)[1], f"{name} has no item"


# A synthetic tree that has no problem. Each test plants one defect into it.

TREE = {
    "README.md": (
        "# A tool\n\n"
        f"## {NOT_SUPPORTED}\n\n"
        "- Other agents ([DR-003](docs/decisions/DR-003-c.md)).\n\n"
        f"## {DOCUMENTATION}\n\n"
        f"- [Roadmap]({ROADMAP}): what is now, next and later.\n"
    ),
    "docs/requirements.md": "| R1 | functional | `thing` | A thing |\n",
    "docs/decisions/DR-001-a.md": "# DR-001: A\n\n- **Closed by:** none\n",
    "docs/decisions/DR-002-b.md": "# DR-002: B\n\n- **Closed by:** DR-003\n",
    "docs/decisions/DR-003-c.md": "# DR-003: C\n\n- **Closed by:** none\n",
    "docs/threat-model.md": "# Threats\n\n### T1. A threat\n",
    "openspec/specs/thing/spec.md": "# thing\n",
    "openspec/changes/c/tasks.md": "- [ ] 1.1 Do a thing\n- [x] 1.2 Did a thing\n",
    "openspec/changes/c/design.md": (
        f"# Design\n\n```\n## {RISKS}\n\n- [A fenced risk] \u2192 What.\n```\n\n"
        f"## {RISKS}\n\n- [A risk] \u2192 What.\n- [Another risk] \u2192 What.\n"
        "  - a line of the risk above.\n\n"
        "## Open Questions\n\n- [Not a risk] \u2192 What.\n"
    ),
    "openspec/changes/archive/2026-01-01-old/tasks.md": "- [x] 2.1 Did an old thing\n",
    "openspec/changes/archive/2026-01-01-old/design.md": (
        f"# Design\n\n## {RISKS}\n\n- [An old risk] \u2192 What.\n"
    ),
    "docs/features/README.md": "# Features\n\n- [Thing](thing.md)\n",
    "docs/features/thing.md": (
        "# Thing\n\nIt says `<x>`, a@b and \u2192 outside the section.\n\n"
        f"## {FEATURE_SECTION}\n\n"
        "- **Another risk**: what it means.\n"
        "- **An old risk**: what it means, with `code`.\n\n"
        "The [roadmap](../roadmap.md) holds the rest.\n\n"
        "## See also\n"
    ),
    ROADMAP: (
        "# Roadmap\n\n"
        "## Now\n\n"
        "- The build.\n\n"
        "## Next\n\n"
        "What follows.\n\n"
        "- **Planned.** A thing that rests on R1 and T1, and on task 1.1 of `c`\n"
        "  and task 2.1 of `old`.\n\n"
        "## Later\n\n"
        f"{LATER_OPENING}\n\n"
        "- **Open to feedback and contributions.** Other agents (DR-003, DR-001).\n\n"
        "## Known limitations\n\n"
        f"{SHORT_LIST} Each feature page lists the rest: "
        f"[thing](features/thing.md#{FEATURE_ANCHOR}), and see [Now](#now) and\n"
        "[the index](decisions/DR-001-a.md) or docs/requirements.md.\n\n"
        "- **A risk**: what it means.\n\n"
        "## Known bugs\n\n"
        "None yet.\n"
    ),
}
FEATURE = "docs/features/thing.md"


def make_tree(root: Path, changed: dict[str, str | None] | None = None) -> Path:
    for name, text in {**TREE, **(changed or {})}.items():
        if text is None:
            continue
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    environment = {**session_free_environment(), **GIT_ENVIRONMENT}
    for args in (["init", "-q"], ["add", "-A"]):
        subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, env=environment)
    return root


def planted(root: Path, name: str, old: str, new: str) -> Path:
    text = TREE[name]
    assert text.count(old) == 1, old
    return make_tree(root, {name: text.replace(old, new)})


def test_a_complete_tree_has_no_problem(tmp_path: Path) -> None:
    assert roadmap_problems(make_tree(tmp_path)) == []


def test_a_missing_roadmap_and_link_are_reported(tmp_path: Path) -> None:
    root = make_tree(tmp_path, {ROADMAP: None, "README.md": "# A tool\n"})
    assert section_problems(root) == [
        f"{ROADMAP} is missing",
        f"README.md's list of documentation does not link {ROADMAP}",
    ]


def test_a_link_outside_the_list_of_documentation_is_not_counted(tmp_path: Path) -> None:
    root = make_tree(tmp_path, {"README.md": f"# A tool\n\nSee the [roadmap]({ROADMAP}).\n"})
    assert section_problems(root) == [f"README.md's list of documentation does not link {ROADMAP}"]


@pytest.mark.parametrize(
    ("old", "new", "problem"),
    [
        ("## Known bugs\n\nNone yet.\n", "", f"{ROADMAP} has no section Known bugs"),
        ("## Now\n\n- The build.\n\n", "", f"{ROADMAP} has no section Now"),
        (
            "## Known bugs\n",
            "## Questions\n\n## Known bugs\n",
            f"{ROADMAP} has a section Questions, which a roadmap does not keep",
        ),
        (
            "## Known bugs\n",
            "## Later\n\n- An item.\n\n## Known bugs\n",
            f"{ROADMAP} gives its sections out of order: "
            "Now, Next, Later, Known limitations, Later, Known bugs",
        ),
        (
            "None yet.\n",
            "None yet.\n\n```\n## Now\n```\n",
            f"{ROADMAP}:31 holds a fenced code block",
        ),
        ("None yet.\n", "None yet.\n\nPromises\n--------\n", f"{ROADMAP}:32 holds a heading"),
        ("None yet.\n", "None yet.\n\n ## Promises\n", f"{ROADMAP}:31 holds a heading"),
    ],
)
def test_a_section_out_of_form_is_reported(
    tmp_path: Path, old: str, new: str, problem: str
) -> None:
    found = section_problems(planted(tmp_path, ROADMAP, old, new)) + link_problems(tmp_path)
    assert [p for p in found if p.startswith(problem)], found


def test_sections_out_of_order_are_reported(tmp_path: Path) -> None:
    text = TREE[ROADMAP].replace("## Now\n\n- The build.\n\n", "")
    text = text.replace("## Known bugs\n", "## Now\n\n- The build.\n\n## Known bugs\n")
    root = make_tree(tmp_path, {ROADMAP: text})
    assert section_problems(root) == [
        f"{ROADMAP} gives its sections out of order: "
        "Next, Later, Known limitations, Now, Known bugs"
    ]


@pytest.mark.parametrize(
    ("old", "new", "problem"),
    [
        (
            "- **Planned.** A thing",
            "- A thing",
            f"{ROADMAP}:11 has an item under Next that opens with neither mark",
        ),
        (
            "- **Planned.** A thing",
            "- **Planned** A thing",
            f"{ROADMAP}:11 has an item under Next that opens with neither mark",
        ),
        (
            "- **Open to feedback and contributions.** Other",
            "- **Open to contributions.** Other",
            f"{ROADMAP}:18 has an item under Later that opens with neither mark",
        ),
        (
            "rests on R1 and T1, and on task 1.1 of `c`\n  and task 2.1 of `old`.",
            "rests on nothing.",
            f"{ROADMAP}:11 has an item under Next that names no requirement, record, threat "
            "or task",
        ),
        (
            "rests on R1 and",
            "rests on R9 and",
            f"{ROADMAP}:11 names R9, which the register does not hold",
        ),
        (
            "and T1, and",
            "and T9, and",
            f"{ROADMAP}:11 names T9, which the threat model does not hold",
        ),
        (
            "(DR-003, DR-001)",
            "(DR-003, DR-009)",
            f"{ROADMAP}:18 names DR-009, which docs/decisions/ does not hold",
        ),
        (
            "task 1.1 of `c`",
            "task 9.9 of `c`",
            f"{ROADMAP}:11 names task 9.9 of `c`, which no change's tasks.md holds",
        ),
        (
            "task 1.1 of `c`",
            "task 1.1 of `none`",
            f"{ROADMAP}:11 names task 1.1 of `none`, which no change's tasks.md holds",
        ),
        (
            "and task 2.1 of `old`.",
            "and task 2.1 of `old`, as R8 says.",
            f"{ROADMAP}:11 names R8, which the register does not hold",
        ),
        ("(DR-003, DR-001)", "(DR-003, DR-002)", f"{ROADMAP}:18 names DR-002, which is closed"),
        ("task 1.1 of `c`", "task 1.2 of `c`", f"{ROADMAP}:11 names only finished tasks"),
        (
            "- The build.",
            "- The build, which R99 holds.",
            f"{ROADMAP}:5 names R99, which the register does not hold",
        ),
        (
            "None yet.",
            "- A bug that DR-002 records.",
            f"{ROADMAP}:29 names DR-002, which is closed",
        ),
        (
            "\n\n## Later",
            "\n* Another thing.\n\n## Later",
            f"{ROADMAP}:13 gives a list item under Next in a form other than `- `",
        ),
        (
            "\n\n## Later",
            "\n1. Another thing.\n\n## Later",
            f"{ROADMAP}:13 gives a list item under Next in a form other than `- `",
        ),
        (
            "\n\n## Later",
            "\n - Another thing.\n\n## Later",
            f"{ROADMAP}:13 gives a list item under Next in a form other than `- `",
        ),
        (
            "\n\n## Later",
            "\n  - Another thing.\n\n## Later",
            f"{ROADMAP}:13 gives a list item under Next in a form other than `- `",
        ),
        (
            "\n\n## Later",
            "\nAnother thing, as DR-001 says.\n\n## Later",
            f"{ROADMAP}:13 holds a line under Next that is neither an item nor part of one",
        ),
    ],
)
def test_an_item_out_of_form_is_reported(tmp_path: Path, old: str, new: str, problem: str) -> None:
    assert item_problems(planted(tmp_path, ROADMAP, old, new)) == [problem]


def test_an_item_under_now_needs_no_mark_or_anchor(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, "- The build.", "- The build, in its own pull requests.")
    assert item_problems(root) == []


def test_two_changes_of_one_name_are_reported(tmp_path: Path) -> None:
    root = make_tree(tmp_path, {"openspec/changes/old/tasks.md": "- [ ] 2.1 Do it again\n"})
    assert change_problems(root) == [
        "two changes are named `old`, so a task cannot be named by its change"
    ]


def test_later_without_its_opening_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, f"{LATER_OPENING}\n\n", "")
    assert later_problems(root) == [
        f"{ROADMAP}: Later does not open with how work on an item starts"
    ]


def test_the_opening_must_come_before_the_first_item(tmp_path: Path) -> None:
    text = TREE[ROADMAP].replace(f"{LATER_OPENING}\n\n", "")
    text = text.replace("(DR-003, DR-001).\n", f"(DR-003, DR-001).\n\n{LATER_OPENING}\n")
    assert later_problems(make_tree(tmp_path, {ROADMAP: text})) == [
        f"{ROADMAP}: Later does not open with how work on an item starts"
    ]


def test_a_record_the_readme_leaves_out_and_later_does_not_name_is_reported(
    tmp_path: Path,
) -> None:
    root = planted(tmp_path, ROADMAP, "(DR-003, DR-001)", "(DR-001)")
    assert later_problems(root) == [
        "no item under Later names DR-003, which the README's list of what the first "
        "version does not support links"
    ]


def test_a_record_named_only_under_next_does_not_count_for_later(tmp_path: Path) -> None:
    text = TREE[ROADMAP].replace("(DR-003, DR-001)", "(DR-001)")
    text = text.replace("rests on R1 and", "rests on DR-003, R1 and")
    assert later_problems(make_tree(tmp_path, {ROADMAP: text})) == [
        "no item under Later names DR-003, which the README's list of what the first "
        "version does not support links"
    ]


def test_a_readme_whose_list_links_no_record_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, "README.md", f"## {NOT_SUPPORTED}", "## Not supported yet")
    assert later_problems(root) == [
        "README.md's list of what the first version does not support links no record"
    ]


def test_a_risk_that_no_page_lists_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, "- **A risk**: what it means.\n", "")
    assert risk_problems(root) == [
        "the risk 'A risk' of openspec/changes/c/design.md is listed neither on the roadmap "
        "nor on a feature page"
    ]


def test_a_risk_of_an_archived_design_that_no_page_lists_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, FEATURE, "- **An old risk**: what it means, with `code`.\n", "")
    assert risk_problems(root) == [
        "the risk 'An old risk' of openspec/changes/archive/2026-01-01-old/design.md is "
        "listed neither on the roadmap nor on a feature page"
    ]


def test_a_risk_out_of_form_or_a_design_without_risks_is_reported(tmp_path: Path) -> None:
    design = "openspec/changes/c/design.md"
    root = planted(tmp_path, design, "- [Another risk] \u2192 What.", "- [Another risk] -> What.")
    assert risk_problems(root) == [
        f"{design}:12 gives a risk in a form the test does not read",
        f"{FEATURE} lists 'Another risk', which no change's design gives as a risk",
    ]
    root = make_tree(
        tmp_path / "other", {"openspec/changes/archive/2026-01-01-old/design.md": "# Design\n"}
    )
    assert risk_problems(root) == [
        "openspec/changes/archive/2026-01-01-old/design.md has no section Risks / Trade-offs",
        f"{FEATURE} lists 'An old risk', which no change's design gives as a risk",
    ]


def test_a_listed_title_that_no_design_gives_is_reported(tmp_path: Path) -> None:
    root = planted(
        tmp_path, ROADMAP, "- **A risk**: what", "- **A risk**: what\n- **A rsik**: what"
    )
    assert risk_problems(root) == [
        f"{ROADMAP} lists 'A rsik', which no change's design gives as a risk"
    ]


def test_a_title_outside_the_risks_section_is_not_a_risk(tmp_path: Path) -> None:
    root = planted(
        tmp_path, ROADMAP, "- **A risk**: what", "- **A risk**: what\n- **Not a risk**: x"
    )
    assert risk_problems(root) == [
        f"{ROADMAP} lists 'Not a risk', which no change's design gives as a risk"
    ]


def test_a_fenced_title_is_not_a_risk(tmp_path: Path) -> None:
    root = planted(
        tmp_path, ROADMAP, "- **A risk**: what", "- **A risk**: what\n- **A fenced risk**: x"
    )
    assert risk_problems(root) == [
        f"{ROADMAP} lists 'A fenced risk', which no change's design gives as a risk"
    ]


def test_a_feature_page_without_the_section_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, FEATURE, f"## {FEATURE_SECTION}", "## Limits")
    assert risk_problems(root) == [
        f"{FEATURE} has no section on known limitations and the roadmap",
        "the risk 'Another risk' of openspec/changes/c/design.md is listed neither on the "
        "roadmap nor on a feature page",
        "the risk 'An old risk' of openspec/changes/archive/2026-01-01-old/design.md is "
        "listed neither on the roadmap nor on a feature page",
    ]


def test_a_feature_page_with_the_section_twice_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, FEATURE, "## See also\n", f"## {FEATURE_SECTION}\n\n## See also\n")
    assert risk_problems(root) == [
        f"{FEATURE} has more than one section on known limitations and the roadmap"
    ]


def test_a_section_that_does_not_link_the_roadmap_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, FEATURE, "The [roadmap](../roadmap.md) holds", "The roadmap holds")
    assert risk_problems(root) == [
        f"{FEATURE}'s section on known limitations and the roadmap does not link the roadmap"
    ]


def test_known_limitations_without_a_link_to_a_section_is_reported(tmp_path: Path) -> None:
    root = planted(
        tmp_path, ROADMAP, f"[thing](features/thing.md#{FEATURE_ANCHOR})", "thing's page"
    )
    assert risk_problems(root) == [
        f"{ROADMAP}'s Known limitations does not link docs/features/thing.md's section"
    ]


def test_known_limitations_that_does_not_say_it_is_short_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, f"{SHORT_LIST} Each", "Each")
    assert risk_problems(root) == [
        f"{ROADMAP}'s Known limitations does not say that it is a short list"
    ]


def test_a_page_not_named_for_a_spec_needs_no_section(tmp_path: Path) -> None:
    root = make_tree(tmp_path, {"docs/features/other.md": "# Other\n"})
    assert risk_problems(root) == []


LINKS_ELSEWHERE = [
    ("[Now](https://example.com)", "gives a web address"),
    ("www.example.com", "gives a web address"),
    ("_www.example.com_", "gives a web address"),
    ("[Now](//example.com)", "gives a web address"),
    ("[Now](mailto:someone)", "links to mailto:someone, a web address"),
    ("someone@example.com", "holds @"),
    ("![a picture](roadmap.md)", "holds an image"),
    ("someone/else", "names someone/else, which is not a tracked file"),
    ("`someone/else`", "names someone/else, which is not a tracked file"),
    ("/someone/else", "names /someone/else, which is not a tracked file"),
    ("someone/**else**", "marks a path with emphasis"),
    ("Add ](someone/else) here", "links to someone/else, which is not a tracked file"),
    ("[Now](#nowhere)", "links to #nowhere, which is not a heading"),
    ("[an issue](../../../issues/15)", "links to ../../../issues/15, which leaves the repository"),
    ("[an [open] issue](../../../issues/15)", "links to ../../../issues/15, which leaves"),
    ("[an open\nissue](../../../issues/15)", "links to ../../../issues/15, which leaves"),
    ("[a page](features/none.md)", "links to features/none.md, which is not a tracked file"),
    ("[a page](features/thing.md#nowhere)", "links to features/thing.md#nowhere, whose file"),
    ("[a page](%2e%2e/%2e%2e/x)", "links to %2e%2e/%2e%2e/x, which leaves the repository"),
    ("[a page](/README.md)", "links to /README.md, which is not a relative"),
    ("[a page](features/thing.md/)", "links to features/thing.md/, which is not a tracked"),
    ("[a page]()", "gives a link with no target"),
    ('[Now](#now "a title")', "holds a link with a title"),
    ('[Now](#now\n"a title")', "holds a link with a title"),
    ("[a page](features/thing.md", "holds a link whose target this test cannot read"),
    ("    pip install something", "holds indented code"),
    ("```", "holds a fenced code block"),
]


@pytest.mark.parametrize(("new", "problem"), LINKS_ELSEWHERE)
def test_a_link_elsewhere_in_the_roadmap_is_reported(
    tmp_path: Path, new: str, problem: str
) -> None:
    found = link_problems(planted(tmp_path, ROADMAP, "None yet.", new))
    assert [p for p in found if p.split(" ", 1)[1].startswith(problem)], found


@pytest.mark.parametrize(("new", "problem"), LINKS_ELSEWHERE)
def test_a_link_elsewhere_in_a_feature_section_is_reported(
    tmp_path: Path, new: str, problem: str
) -> None:
    new = new.replace("](features/", "](").replace("](roadmap.md", "](../roadmap.md")
    new = new.replace("](%2e%2e/%2e%2e/x", "](%2e%2e/%2e%2e/%2e%2e/x")
    problem = problem.replace("features/", "").replace("%2e%2e/%2e%2e/x", "%2e%2e/%2e%2e/%2e%2e/x")
    found = link_problems(planted(tmp_path, FEATURE, "holds the rest.", f"holds the rest.\n{new}"))
    assert [p for p in found if p.startswith(FEATURE) and problem in p], found


def test_a_link_reports_the_line_its_target_stands_on(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, "None yet.", "None\n[yet](../../../issues/15).")
    assert link_problems(root) == [
        f"{ROADMAP}:30 links to ../../../issues/15, which leaves the repository"
    ]


HIDDEN = [
    ("A\u200bB", "holds U+200B"),
    ("A\u202eB", "holds U+202E"),
    ("A\rB", "holds U+000D"),
    ("A<!-- hidden -->B", "holds <, with which Markdown starts HTML"),
    ("`<!-- hidden -->`", "holds <, with which Markdown starts HTML"),
    ("[x]: features/thing.md", "holds ]:, with which Markdown defines a link"),
    ('[a`]: x "` hidden"', "holds ]:, with which Markdown defines a link"),
    ("A &#65; B", "holds &, with which Markdown writes a character"),
    ("\\`<!-- hidden -->\\`", "holds a backslash"),
]


@pytest.mark.parametrize(("new", "problem"), HIDDEN)
def test_hidden_text_in_the_roadmap_is_reported(tmp_path: Path, new: str, problem: str) -> None:
    found = hidden_text_problems(planted(tmp_path, ROADMAP, "None yet.", new))
    assert f"{ROADMAP}:29 {problem}" in [p[: len(ROADMAP) + 4 + len(problem)] for p in found], found


@pytest.mark.parametrize(("new", "problem"), HIDDEN)
def test_hidden_text_in_a_feature_section_is_reported(
    tmp_path: Path, new: str, problem: str
) -> None:
    root = planted(tmp_path, FEATURE, "holds the rest.", f"holds the rest.\n{new}")
    found = hidden_text_problems(root)
    assert f"{FEATURE}:11 {problem}" in [p[: len(FEATURE) + 4 + len(problem)] for p in found], found


def test_text_outside_the_feature_section_is_not_held(tmp_path: Path) -> None:
    root = make_tree(tmp_path)
    assert hidden_text_problems(root) == [] and link_problems(root) == []
