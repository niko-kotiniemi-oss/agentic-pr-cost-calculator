"""The roadmap says what is now, next and later, and leads only to this repository.

`docs/roadmap.md` is linked from the README's list of documentation, and its
sections are Now, Next, Later, Known limitations and Known bugs, in that order
(R206, DR-218). An item is a line under a section that starts with `- `, with the
indented lines that follow it.

Each item under Next and Later opens with `**Planned.**` or `**Open to feedback and
contributions.**` (R207, DR-219), and names what it rests on: a requirement (`R`
and digits) that the register holds, a record (`DR-` and three digits) that
`docs/decisions/` holds, a threat (`T` and digits) that the threat model holds, or
a task, as `task 1.26 of` and the change's name as code, that a change's
`tasks.md`, active or archived, holds. An item whose named tasks are all ticked, or
that names a closed record, is stale (R206, T161). No test reads an issue, so
whether an issue that an item names is still open rests on review. Later opens
with the sentence that `LATER_OPENING` gives, and each record that the README's
list of what the first version does not support links is named by an item under
Later (R207).

Every risk that the risks and trade-offs of a change's design give, active or
archived, as a line that opens with `- [title]` and an arrow, is listed by its title, as a line
`- **title**: ...`, under Known limitations or in the section on known limitations
and the roadmap of a page in `docs/features/` named for a spec. Each such page has
that section, which links the roadmap, and Known limitations says that it is a
short list and links each section. A listed title that no design gives fails too
(R208, DR-220, T162).

Every link in the roadmap names one of its headings, or a tracked file of this
repository by a relative path that, resolved from `docs/`, stays inside it, with a
heading of that file when the link names one. The roadmap gives no web address,
no fenced code, and no `owner/repo` that is not a tracked file's path from the
repository's root, in prose and code alike, so that issues and pull requests are
named by number alone (R209, DR-221, DR-224, T160, T163, T164). The roadmap, and
each feature page's section, hold printable ASCII and line breaks only, and
outside inline code no `<`, no `]:`, no character reference and no link with a
title (R210, T165).

Each check is shown to fail on a synthetic tree, a git repository so that its
tracked files can be read, into which the defect is planted.
"""

from __future__ import annotations

import os
import posixpath
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

import pytest

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
FEATURE_ANCHOR = "known-limitations-and-the-roadmap"
NOT_SUPPORTED = "Not supported in this first version"
DOCUMENTATION = "Documentation"
RISKS = "Risks / Trade-offs"

HEADING = re.compile(r"^(#{1,6}) +(.+?) *$")
REQUIREMENT_NAME = re.compile(r"\bR\d+\b")
RECORD_NAME = re.compile(r"\bDR-\d{3}\b")
THREAT_NAME = re.compile(r"\bT\d+\b")
TASK_NAME = re.compile(r"\btask (\d+\.\d+) of `([a-z0-9-]+)`")
REGISTER_ROW = re.compile(r"^\| (R\d+) \| ", re.M)
THREAT_HEADING = re.compile(r"^### (T\d+)\. ", re.M)
RECORD_FILE = re.compile(r"(DR-\d{3})-[a-z0-9-]+\.md")
CLOSED_BY = re.compile(r"^- \*\*Closed by:\*\* (.+?) *$", re.M)
TASK_LINE = re.compile(r"^- \[([ x])\] (\d+\.\d+) ", re.M)
ARCHIVED = re.compile(r"\d{4}-\d{2}-\d{2}-(.+)")
RISK = re.compile(r"^- \[(.+?)\] → ", re.M)
LISTED = re.compile(r"^- \*\*(.+?)\*\*: ", re.M)
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\n]*)\)")
LINK_TARGET = re.compile(r"\]\([^)\n]*\)")
CODE_SPAN = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
# A web address in a form that GitHub links or that an agent could follow.
WEB_ADDRESS = re.compile(r"//|(?<![\w.-])www\.|(?:\]\(|<)\s*[a-z][a-z0-9+.-]*:", re.I)
OWNER_REPO = re.compile(r"(?<![\w./-])[\w.-]+(?:/[\w.-]+)+/?")
FENCE = re.compile(r"^\s*(```|~~~)")
CHARACTER_REFERENCE = re.compile(r"&(?:#[0-9]+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);")
TITLED_LINK = re.compile(r"\]\([^)\s]*\s+[\"'(]")

GIT_ENVIRONMENT = {
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
}


@dataclass(frozen=True)
class Item:
    section: str
    line: int
    text: str


def git_environment() -> dict[str, str]:
    """The environment with no git variable of the session's, such as an index file,
    that would make git read another repository than the one it runs in."""
    kept = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    return {**kept, **GIT_ENVIRONMENT}


def tracked(root: Path) -> set[str]:
    done = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
        env=git_environment(),
    )
    return {name for name in done.stdout.decode().split("\0") if name}


def sections(text: str) -> list[tuple[str, int, list[str]]]:
    """Each `## ` section: its heading, the number of its first line, and its lines."""
    found: list[tuple[str, int, list[str]]] = []
    for number, line in enumerate(text.split("\n"), 1):
        heading = HEADING.match(line)
        if heading and heading.group(1) == "##":
            found.append((heading.group(2), number + 1, []))
        elif found:
            found[-1][2].append(line)
    return found


def section_of(text: str, name: str) -> tuple[int, list[str]]:
    for heading, start, lines in sections(text):
        if heading == name:
            return start, lines
    return 0, []


def items(name: str, start: int, lines: list[str]) -> tuple[list[str], list[Item]]:
    """A section's opening lines, before its first item, and its items."""
    opening: list[str] = []
    found: list[Item] = []
    for offset, line in enumerate(lines):
        if line.startswith("- "):
            found.append(Item(name, start + offset, line))
        elif found and line.startswith(" ") and line.strip():
            last = found[-1]
            found[-1] = Item(last.section, last.line, f"{last.text}\n{line.strip()}")
        elif not found:
            opening.append(line)
    return opening, found


def slug(heading: str) -> str:
    text = heading.replace("`", "").lower()
    text = re.sub(r"[^a-z0-9 _-]", "", text)
    return text.replace(" ", "-")


def anchors(text: str) -> set[str]:
    return {slug(heading.group(2)) for line in text.split("\n") if (heading := HEADING.match(line))}


def records(root: Path) -> dict[str, bool]:
    """Each record's ID, and whether it is closed."""
    found = {}
    for path in sorted((root / "docs" / "decisions").glob("DR-*.md")):
        name = RECORD_FILE.fullmatch(path.name)
        if not name:
            continue
        closer = CLOSED_BY.search(path.read_text(encoding="utf-8"))
        found[name.group(1)] = closer is not None and closer.group(1) != "none"
    return found


def changes(root: Path) -> dict[str, Path]:
    """Each change's folder, active or archived, by the change's name."""
    folder = root / "openspec" / "changes"
    found = {}
    for path in sorted(folder.glob("*")):
        if path.is_dir() and path.name != "archive":
            found[path.name] = path
    for path in sorted((folder / "archive").glob("*")):
        named = ARCHIVED.fullmatch(path.name)
        if path.is_dir() and named:
            found[named.group(1)] = path
    return found


def tasks(root: Path) -> dict[tuple[str, str], bool]:
    """Each task, by its change and number, and whether it is ticked."""
    found = {}
    for name, path in changes(root).items():
        listed = path / "tasks.md"
        if listed.is_file():
            for tick, number in TASK_LINE.findall(listed.read_text(encoding="utf-8")):
                found[(name, number)] = tick == "x"
    return found


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def section_problems(root: Path) -> list[str]:
    roadmap = root / ROADMAP
    problems = []
    if not roadmap.is_file():
        problems.append(f"{ROADMAP} is missing")
    else:
        found = [heading for heading, _, _ in sections(read(roadmap))]
        problems += [f"{ROADMAP} has no section {name}" for name in SECTIONS if name not in found]
        problems += [
            f"{ROADMAP} has a section {name}, which a roadmap does not keep"
            for name in found
            if name not in SECTIONS
        ]
        if sorted(found) == sorted(SECTIONS) and found != list(SECTIONS):
            problems.append(f"{ROADMAP} gives its sections out of order: {', '.join(found)}")
    _, documentation = section_of(read(root / "README.md"), DOCUMENTATION)
    if f"]({ROADMAP})" not in "\n".join(documentation):
        problems.append(f"README.md's list of documentation does not link {ROADMAP}")
    return problems


def item_problems(root: Path) -> list[str]:
    text = read(root / ROADMAP)
    register = set(REGISTER_ROW.findall(read(root / "docs" / "requirements.md")))
    threats = set(THREAT_HEADING.findall(read(root / "docs" / "threat-model.md")))
    held = records(root)
    listed = tasks(root)
    problems = []
    for name in MARKED:
        start, lines = section_of(text, name)
        for item in items(name, start, lines)[1]:
            where = f"{ROADMAP}:{item.line}"
            if not item.text.startswith(tuple(f"- {mark} " for mark in MARKS)):
                problems.append(f"{where} has an item under {name} that opens with neither mark")
            requirements = REQUIREMENT_NAME.findall(item.text)
            named = RECORD_NAME.findall(item.text)
            threat_names = THREAT_NAME.findall(item.text)
            task_names = [(change, number) for number, change in TASK_NAME.findall(item.text)]
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
    opening, found = items("Later", start, lines)
    problems = []
    if LATER_OPENING not in " ".join(line.strip() for line in opening):
        problems.append(f"{ROADMAP}: Later does not open with how work on an item starts")
    named = {ident for item in found for ident in RECORD_NAME.findall(item.text)}
    _, unsupported = section_of(read(root / "README.md"), NOT_SUPPORTED)
    for ident in sorted(set(RECORD_NAME.findall("\n".join(unsupported)))):
        if ident not in named:
            problems.append(
                f"no item under Later names {ident}, which the README's list of what the "
                "first version does not support links"
            )
    return problems


def specs(root: Path) -> set[str]:
    folders = [root / "openspec" / "specs"]
    folders += [path / "specs" for path in sorted((root / "openspec" / "changes").glob("*"))]
    return {spec.parent.name for folder in folders for spec in folder.glob("*/spec.md")}


def feature_pages(root: Path) -> list[Path]:
    names = specs(root)
    folder = root / "docs" / "features"
    return [page for page in sorted(folder.glob("*.md")) if page.stem in names]


def risks(root: Path) -> dict[str, str]:
    """Each risk's title, and the design that gives it, from every change."""
    found: dict[str, str] = {}
    for path in changes(root).values():
        design = path / "design.md"
        _, lines = section_of(read(design), RISKS)
        for title in RISK.findall("\n".join(lines)):
            found.setdefault(title, design.relative_to(root).as_posix())
    return found


def risk_problems(root: Path) -> list[str]:
    roadmap = read(root / ROADMAP)
    _, limitations = section_of(roadmap, "Known limitations")
    known = "\n".join(limitations)
    given = risks(root)
    problems = []
    listed: set[str] = set()
    if SHORT_LIST not in known:
        problems.append(f"{ROADMAP}'s Known limitations does not say that it is a short list")
    pages: list[tuple[str, str]] = [(ROADMAP, known)]
    targets = set(LINK.findall(known))
    for page in feature_pages(root):
        name = page.relative_to(root).as_posix()
        _, lines = section_of(read(page), FEATURE_SECTION)
        if not lines:
            problems.append(f"{name} has no section on known limitations and the roadmap")
            continue
        body = "\n".join(lines)
        pages.append((name, body))
        if not any(link.split("#")[0] == "../roadmap.md" for link in LINK.findall(body)):
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


def link_problems(root: Path) -> list[str]:
    text = read(root / ROADMAP)
    files = tracked(root)
    own = anchors(text)
    problems = []
    for number, line in enumerate(text.split("\n"), 1):
        where = f"{ROADMAP}:{number}"
        if FENCE.match(line):
            problems.append(f"{where} holds a fenced code block")
        if WEB_ADDRESS.search(line):
            problems.append(f"{where} gives a web address")
        for token in OWNER_REPO.findall(LINK_TARGET.sub("](", line)):
            path = token.rstrip(".")
            if path not in files:
                problems.append(
                    f"{where} names {path}, which is not a tracked file of this repository"
                )
        for target in LINK.findall(line):
            problems += target_problems(root, where, target.strip(), files, own)
    return problems


def target_problems(
    root: Path, where: str, target: str, files: set[str], own: set[str]
) -> list[str]:
    address = target.split()[0] if target.split() else ""
    if not address:
        return [f"{where} gives a link with no target"]
    if SCHEME.match(address) or address.startswith("//"):
        return []  # A web address, which `WEB_ADDRESS` reports.
    if address.startswith("#"):
        if address[1:] not in own:
            return [f"{where} links to {address}, which is not a heading of the roadmap"]
        return []
    path, _, fragment = address.partition("#")
    path = unquote(path)
    if "\\" in path or path.startswith("/"):
        return [f"{where} links to {address}, which is not a relative path"]
    resolved = posixpath.normpath(posixpath.join("docs", path))
    if resolved == ".." or resolved.startswith("../"):
        return [f"{where} links to {address}, which leaves the repository"]
    if resolved not in files:
        return [f"{where} links to {address}, which is not a tracked file of this repository"]
    if fragment and fragment not in anchors(read(root / resolved)):
        return [f"{where} links to {address}, whose file has no such heading"]
    return []


def hidden_problems(name: str, start: int, lines: list[str]) -> list[str]:
    problems = []
    for offset, line in enumerate(lines):
        where = f"{name}:{start + offset}"
        others = sorted({ord(c) for c in line if not " " <= c <= "~"})
        if others:
            problems.append(f"{where} holds {', '.join(f'U+{code:04X}' for code in others)}")
        plain = CODE_SPAN.sub("", line)
        if "<" in plain:
            problems.append(f"{where} holds <")
        if "]:" in plain:
            problems.append(f"{where} holds ]:")
        if CHARACTER_REFERENCE.search(plain):
            problems.append(f"{where} holds a character reference")
        if TITLED_LINK.search(plain):
            problems.append(f"{where} holds a link with a title")
    return problems


def hidden_text_problems(root: Path) -> list[str]:
    problems = []
    roadmap = root / ROADMAP
    if roadmap.is_file():
        problems += hidden_problems(ROADMAP, 1, read(roadmap).split("\n"))
    for page in feature_pages(root):
        start, lines = section_of(read(page), FEATURE_SECTION)
        problems += hidden_problems(page.relative_to(root).as_posix(), start, lines)
    return problems


def roadmap_problems(root: Path) -> list[str]:
    return (
        section_problems(root)
        + item_problems(root)
        + later_problems(root)
        + risk_problems(root)
        + link_problems(root)
        + hidden_text_problems(root)
    )


def test_the_repository_has_no_roadmap_problem() -> None:
    assert roadmap_problems(ROOT) == []


def test_the_repository_gives_risks_feature_pages_and_items_to_check() -> None:
    """A check that examined nothing fails."""
    text = read(ROOT / ROADMAP)
    assert len(risks(ROOT)) > 0
    assert len(feature_pages(ROOT)) > 0
    for name in MARKED:
        start, lines = section_of(text, name)
        assert items(name, start, lines)[1], f"{name} has no item"


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
        f"# Design\n\n## {RISKS}\n\n- [A risk] → What.\n- [Another risk] → What.\n\n"
        "## Open Questions\n\n- [Not a risk] → What.\n"
    ),
    "openspec/changes/archive/2026-01-01-old/tasks.md": "- [x] 2.1 Did an old thing\n",
    "openspec/changes/archive/2026-01-01-old/design.md": (
        f"# Design\n\n## {RISKS}\n\n- [An old risk] → What.\n"
    ),
    "docs/features/README.md": "# Features\n\n- [Thing](thing.md)\n",
    "docs/features/thing.md": (
        "# Thing\n\nIt says `<x>` and → outside the section.\n\n"
        f"## {FEATURE_SECTION}\n\n"
        "- **Another risk**: what it means.\n"
        "- **An old risk**: what it means, with `<code>`.\n\n"
        "The [roadmap](../roadmap.md) holds the rest.\n\n"
        "## See also\n"
    ),
    ROADMAP: (
        "# Roadmap\n\n"
        "## Now\n\n"
        "- The build.\n\n"
        "## Next\n\n"
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


def make_tree(root: Path, changed: dict[str, str | None] | None = None) -> Path:
    for name, text in {**TREE, **(changed or {})}.items():
        if text is None:
            continue
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    environment = git_environment()
    for args in (["init", "-q"], ["add", "-A"]):
        subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, env=environment)
    return root


def planted(root: Path, name: str, old: str, new: str) -> Path:
    text = TREE[name]
    assert old in text, old
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
        (
            "## Now\n\n- The build.\n\n## Next\n",
            "## Next\n",
            f"{ROADMAP} has no section Now",
        ),
        (
            "## Known bugs\n",
            "## Questions\n\n## Known bugs\n",
            f"{ROADMAP} has a section Questions, which a roadmap does not keep",
        ),
        (
            "## Now\n\n- The build.\n\n",
            "",
            f"{ROADMAP} has no section Now",
        ),
    ],
)
def test_a_section_missing_or_extra_is_reported(
    tmp_path: Path, old: str, new: str, problem: str
) -> None:
    assert problem in section_problems(planted(tmp_path, ROADMAP, old, new))


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
            f"{ROADMAP}:9 has an item under Next that opens with neither mark",
        ),
        (
            "- **Planned.** A thing",
            "- **Planned** A thing",
            f"{ROADMAP}:9 has an item under Next that opens with neither mark",
        ),
        (
            "- **Open to feedback and contributions.** Other",
            "- **Open to contributions.** Other",
            f"{ROADMAP}:16 has an item under Later that opens with neither mark",
        ),
        (
            "rests on R1 and T1, and on task 1.1 of `c`\n  and task 2.1 of `old`.",
            "rests on nothing.",
            f"{ROADMAP}:9 has an item under Next that names no requirement, record, threat or task",
        ),
        (
            "rests on R1 and",
            "rests on R9 and",
            f"{ROADMAP}:9 names R9, which the register does not hold",
        ),
        (
            "and T1, and",
            "and T9, and",
            f"{ROADMAP}:9 names T9, which the threat model does not hold",
        ),
        (
            "(DR-003, DR-001)",
            "(DR-003, DR-009)",
            f"{ROADMAP}:16 names DR-009, which docs/decisions/ does not hold",
        ),
        (
            "task 1.1 of `c`",
            "task 9.9 of `c`",
            f"{ROADMAP}:9 names task 9.9 of `c`, which no change's tasks.md holds",
        ),
        (
            "task 1.1 of `c`",
            "task 1.1 of `none`",
            f"{ROADMAP}:9 names task 1.1 of `none`, which no change's tasks.md holds",
        ),
        (
            "(DR-003, DR-001)",
            "(DR-003, DR-002)",
            f"{ROADMAP}:16 names DR-002, which is closed",
        ),
        (
            "task 1.1 of `c`",
            "task 1.2 of `c`",
            f"{ROADMAP}:9 names only finished tasks",
        ),
    ],
)
def test_an_item_out_of_form_is_reported(tmp_path: Path, old: str, new: str, problem: str) -> None:
    assert item_problems(planted(tmp_path, ROADMAP, old, new)) == [problem]


def test_an_item_under_now_needs_no_mark_or_anchor(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, "- The build.", "- The build, which names R99.")
    assert item_problems(root) == []


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


def test_a_risk_that_no_page_lists_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, "- **A risk**: what it means.\n", "")
    assert risk_problems(root) == [
        "the risk 'A risk' of openspec/changes/c/design.md is listed neither on the roadmap "
        "nor on a feature page"
    ]


def test_a_risk_of_an_archived_design_that_no_page_lists_is_reported(tmp_path: Path) -> None:
    feature = "docs/features/thing.md"
    root = planted(tmp_path, feature, "- **An old risk**: what it means, with `<code>`.\n", "")
    assert risk_problems(root) == [
        "the risk 'An old risk' of openspec/changes/archive/2026-01-01-old/design.md is "
        "listed neither on the roadmap nor on a feature page"
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


def test_a_feature_page_without_the_section_is_reported(tmp_path: Path) -> None:
    feature = "docs/features/thing.md"
    root = planted(tmp_path, feature, f"## {FEATURE_SECTION}", "## Limits")
    assert risk_problems(root) == [
        f"{feature} has no section on known limitations and the roadmap",
        "the risk 'Another risk' of openspec/changes/c/design.md is listed neither on the "
        "roadmap nor on a feature page",
        "the risk 'An old risk' of openspec/changes/archive/2026-01-01-old/design.md is "
        "listed neither on the roadmap nor on a feature page",
    ]


def test_a_section_that_does_not_link_the_roadmap_is_reported(tmp_path: Path) -> None:
    feature = "docs/features/thing.md"
    root = planted(tmp_path, feature, "The [roadmap](../roadmap.md) holds", "The roadmap holds")
    assert risk_problems(root) == [
        f"{feature}'s section on known limitations and the roadmap does not link the roadmap"
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


@pytest.mark.parametrize(
    ("old", "new", "problem"),
    [
        ("[Now](#now)", "[Now](https://example.com)", "gives a web address"),
        ("[Now](#now)", "www.example.com", "gives a web address"),
        ("[Now](#now)", "[Now](//example.com)", "gives a web address"),
        ("[Now](#now)", "[Now](mailto:someone)", "gives a web address"),
        ("[Now](#now)", "someone/else", "names someone/else, which is not a tracked file"),
        (
            "[Now](#now)",
            "`someone/else`",
            "names someone/else, which is not a tracked file",
        ),
        ("[Now](#now)", "[Now](#nowhere)", "links to #nowhere, which is not a heading"),
        (
            "[Now](#now)",
            "[an issue](../../../issues/15)",
            "links to ../../../issues/15, which leaves the repository",
        ),
        (
            "[Now](#now)",
            "[a page](features/none.md)",
            "links to features/none.md, which is not a tracked file",
        ),
        (
            "[Now](#now)",
            "[a page](features/thing.md#nowhere)",
            "links to features/thing.md#nowhere, whose file has no such heading",
        ),
        (
            "[Now](#now)",
            "[a page](%2e%2e/%2e%2e/x)",
            "links to %2e%2e/%2e%2e/x, which leaves the repository",
        ),
        ("[Now](#now)", "[a page](/README.md)", "links to /README.md, which is not a relative"),
        (
            "[Now](#now)",
            "[a page](features\\thing.md)",
            "links to features\\thing.md, which is not a relative",
        ),
        ("[Now](#now)", "[a page]()", "gives a link with no target"),
    ],
)
def test_a_link_elsewhere_is_reported(tmp_path: Path, old: str, new: str, problem: str) -> None:
    found = link_problems(planted(tmp_path, ROADMAP, old, new))
    assert len(found) == 1 and found[0].startswith(f"{ROADMAP}:20 {problem}"), found


def test_a_fenced_code_block_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, "None yet.\n", "None yet.\n\n```\ncode\n```\n")
    assert link_problems(root) == [
        f"{ROADMAP}:29 holds a fenced code block",
        f"{ROADMAP}:31 holds a fenced code block",
    ]


@pytest.mark.parametrize(
    ("new", "problem"),
    [
        ("A​B", "holds U+200B"),
        ("A‮B", "holds U+202E"),
        ("A<!-- hidden -->B", "holds <"),
        ("[x]: features/thing.md", "holds ]:"),
        ("A &#65; B", "holds a character reference"),
        ("A &amp; B", "holds a character reference"),
        ('[Now](#now "a title")', "holds a link with a title"),
    ],
)
def test_hidden_text_in_the_roadmap_is_reported(tmp_path: Path, new: str, problem: str) -> None:
    root = planted(tmp_path, ROADMAP, "None yet.", new)
    assert hidden_text_problems(root) == [f"{ROADMAP}:27 {problem}"]


@pytest.mark.parametrize(
    ("new", "problem"),
    [
        ("A​B", "holds U+200B"),
        ("A<!-- hidden -->B", "holds <"),
        ("[x]: ../roadmap.md", "holds ]:"),
        ("A &#65; B", "holds a character reference"),
        ('[r](../roadmap.md "a title")', "holds a link with a title"),
    ],
)
def test_hidden_text_in_a_feature_section_is_reported(
    tmp_path: Path, new: str, problem: str
) -> None:
    feature = "docs/features/thing.md"
    root = planted(tmp_path, feature, "holds the rest.", f"holds the rest.\n{new}")
    assert hidden_text_problems(root) == [f"{feature}:11 {problem}"]


def test_hidden_text_inside_inline_code_is_not_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, "None yet.", "None yet: `<x>` and `&amp;`.")
    assert hidden_text_problems(root) == []
