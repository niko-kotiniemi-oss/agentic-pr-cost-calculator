"""The roadmap says what is now, next and later, and leads only to this repository.

`docs/roadmap.md` is linked from the README's list of documentation, opens, before
its first section, with the sentence that `ROADMAP_OPENING` gives, and its sections
are Now, Next, Later, Known limitations and Known bugs, each once and in that order;
Now ends with one line, not an item, that links a change's `proposal.md` and
`tasks.md`, which are the build's home (R206, DR-225). A section is a `## ` line at
the start of a line, read outside fenced code; the roadmap holds no heading indented
or underlined. An item is a line that starts with `- `, with the lines indented by
two spaces that follow it. What Now, Next and Later list, as the index of the backlog
items, is `tests/test_backlog.py`'s to check (R213, R214).

Every risk that the risks and trade-offs of a change's design give, active or
archived, as a line that opens with `- [title]` and an arrow, is listed by its
title, as a line `- **title**: ...`, under Known limitations or in the section on
known limitations and the roadmap of a page in `docs/features/` named for a spec.
A line under a design's risks that starts with `- ` in another form fails, and so
does a design without that section, or two changes of one name. Each such page has
that section, once, which links the roadmap, and Known limitations says that it is
a short list and links each section. A listed title that no design gives fails too
(R208, DR-220, T162).

Every link in the roadmap, in each Markdown file in `docs/backlog/` and in each
feature page's section, is read from its `](` over the whole text, whatever its text
holds, and names a heading of its page, or a tracked file of this repository outside
`vendor/` and `.claude/skills/`, whose files others write, by a relative path that
stays inside it, with a heading of that file when the link names one, and gives no
title. The pages give no web address, no `@`, no image, no fenced or indented code,
no inline code that holds a space or a line break, so that no command stands in them,
and no `owner/repo` that is not the path of such a file from the repository's root,
in prose and code alike, so that issues and pull requests are named by number alone.
Nor do they name a host, read as two or more labels joined by dots whose last is made
of letters, unless it is a tracked file's path or a name in `NOT_HOSTS`, which gives
each name's reason; in prose, the emphasis marks next to a dot, which GitHub does not
show, are read as gone. Nor do they give four numbers joined by dots, as an IP address
is, or a commit ID, read as seven or more hexadecimal digits that hold both a digit
and a letter (R209, DR-227, DR-228, T160, T163, T164). They hold printable ASCII and
line feeds only, and no `<`, `&`, backslash, `]:` or `|`, inline code included (R210,
T165). `link_problems_in` and `hidden_text_problems_in` read any text so, and the
guide's test reads the guide with them (R221).

Each change's `tasks.md`, active or archived, gives each task once, on a line that
opens with `- [ ]` or `- [x]`, a space, its number and a space, as `TASK_LINE` reads
it, and holds no other line with a checkbox, no HTML comment, no line that opens with
`<` and no code fence, so that the checks that wait on a tick, or refuse one, read the
tasks that GitHub shows (R232, T184).

Each check is shown to fail on a synthetic tree, a git repository so that its
tracked files can be read, into which the defect is planted. The tree holds backlog
items and a roadmap that lists them, so that `tests/test_backlog.py` plants its
defects into the same tree.
"""

from __future__ import annotations

import os
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

import pytest
from spec_form import find_specs

ROOT = Path(__file__).resolve().parents[1]

ROADMAP = "docs/roadmap.md"
SECTIONS = ("Now", "Next", "Later", "Known limitations", "Known bugs")
BACKLOG = "docs/backlog"
ROADMAP_OPENING = (
    "The roadmap describes: an item here is neither a promise nor a date, and it is not a "
    "request to start the work."
)
LATER_OPENING = (
    "Work on an item here that is open to feedback and contributions starts with an issue. "
    "An item is built only once it is Planned, which only a pull request that the owner "
    "merges makes it, and some items need a spec, a threat review and the owner's decision "
    "first."
)
SHORT_LIST = "This is a short list."
FEATURE_SECTION = "Known limitations and the roadmap"
NOT_SUPPORTED = "Not supported in this first version"
DOCUMENTATION = "Documentation"
RISKS = "Risks / Trade-offs"

HEADING = re.compile(r"^(#{1,6}) +(.+?) *$")
FENCE = re.compile(r"^ *(```|~~~)")
MISPLACED_HEADING = re.compile(r"^ {1,3}#{1,6}( |$)|^ {0,3}(=+|-+) *$")
# The marks of block quotes and list items that open a line, after which code can
# start as it does at the start of a line.
CONTAINER = re.compile(r"^(?: {0,3}> ?| {0,3}(?:[-*+]|\d+[.)]) )*")
LIST_MARKER = re.compile(r"^ *([-*+]|\d+[.)])( |$)")
RECORD_NAME = re.compile(r"\bDR-\d{3}\b")
# A link to a change's proposal or tasks, from the roadmap's folder.
BUILD_LINK = re.compile(r"\]\(\.\./openspec/changes/([a-z0-9-]+)/(proposal|tasks)\.md\)")
# Inline code, over line breaks, as Markdown reads it: a run of backticks to the next
# run of the same length.
INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.S)
# What the reading of links says of inline code that holds a space, from which the
# guide's fixed opening is exempt.
SPACED_CODE = "holds inline code that holds a space, as a command does"
REGISTER_ROW = re.compile(r"^\| (R\d+) \| ", re.M)
THREAT_HEADING = re.compile(r"^### (T\d+)\. ", re.M)
RECORD_FILE = re.compile(r"(DR-\d{3})-[a-z0-9-]+\.md")
CLOSED_BY = re.compile(r"^- \*\*Closed by:\*\* (.+?) *$", re.M)
TASK_LINE = re.compile(r"^- \[([ xX])\] ([0-9]+\.[0-9]+) ", re.M)
# A checkbox as GitHub shows one in a list, and a line that opens or closes fenced code.
BOX = re.compile(r"\[[ xX]\]")
CODE_FENCE = re.compile(r"\s*(```|~~~)")
# The change that the build follows, whose tasks this repository's own gates read, and
# where tests plant its tasks, active or archived.
BUILD_CHANGE = "add-pr-cost-calculator"
CHANGE_TASKS = f"openspec/changes/{BUILD_CHANGE}/tasks.md"
ARCHIVED_TASKS = f"openspec/changes/archive/2026-01-01-{BUILD_CHANGE}/tasks.md"
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
# Emphasis or strikethrough marks next to a dot, which GitHub does not show, so that
# `evil.*example*` shows as one name.
BESIDE_A_DOT = re.compile(r"[*_~]+(?=\.)|(?<=\.)[*_~]+")
NAME = re.compile(r"[A-Za-z0-9_./-]+")
LETTERS = re.compile(r"[A-Za-z]+")
ADDRESS = re.compile(r"\d+(?:\.\d+){3}")
COMMIT_ID = re.compile(r"(?<![0-9A-Za-z])[0-9A-Fa-f]{7,}(?![0-9A-Za-z])")
# Folders whose files others write: a vendored tree and the generated skills.
OTHERS_WRITE = ("vendor/", ".claude/skills/")
# Names that read as hosts, two or more labels joined by dots whose last is made of
# letters, but name none, each with its reason.
NOT_HOSTS = {
    "core.autocrlf": "a git configuration key, which the usage feature's page names",
    "B-NNN-words.md": "the form of a backlog item's file name, which the backlog's page gives",
}
HIDING = (
    ("<", "<, with which Markdown starts HTML"),
    ("&", "&, with which Markdown writes a character by its code"),
    ("\\", "a backslash, with which Markdown undoes what a mark does"),
    ("]:", "]:, with which Markdown defines a link that it does not show"),
    ("|", "|, with which Markdown builds a table, whose cells past its header's it hides"),
)

GIT_ENVIRONMENT = {
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
}


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


def task_list_problems(root: Path) -> list[str]:
    """Each change's `tasks.md` gives each task once, on a line that `TASK_LINE` reads,
    and holds no other line with a checkbox, no HTML comment, no line that opens with
    `<` and no code fence, so that `tasks` reads the tasks that GitHub shows (R232)."""
    problems = []
    for _, path in changes(root):
        name = (path / "tasks.md").relative_to(root).as_posix()
        given: dict[str, list[int]] = {}
        for number, line in enumerate(read(path / "tasks.md").split("\n"), 1):
            task = TASK_LINE.match(line)
            if task:
                given.setdefault(task.group(2), []).append(number)
            elif BOX.search(line):
                problems.append(
                    f"{name}:{number} holds a checkbox that the checks do not read as a task"
                )
            if "<!--" in line:
                problems.append(
                    f"{name}:{number} holds an HTML comment, which GitHub does not show"
                )
            elif line.lstrip().startswith("<"):
                problems.append(
                    f"{name}:{number} opens with <, with which Markdown starts HTML that can hide "
                    "the lines after it"
                )
            if CODE_FENCE.match(line):
                problems.append(
                    f"{name}:{number} holds a code fence, inside which GitHub shows a tick as code"
                )
        problems += [
            f"{name} gives task {ident} on lines {', '.join(map(str, lines[:-1]))} and {lines[-1]}"
            for ident, lines in given.items()
            if len(lines) > 1
        ]
    return problems


def padless(code: str) -> str:
    """Inline code as Markdown shows it: one space stripped from each end, when both
    ends have one and the code is not all spaces."""
    if len(code) > 2 and code[0] == code[-1] == " " and code.strip():
        return code[1:-1]
    return code


def ends_on_the_build(lines: list[str]) -> bool:
    """Whether a section's last line, not an item, links one change's proposal and tasks."""
    last = next((line for line in reversed(lines) if line.strip()), "")
    if last.startswith("- "):
        return False
    linked: dict[str, set[str]] = {}
    for change, page in BUILD_LINK.findall(last):
        linked.setdefault(change, set()).add(page)
    return any(pages == {"proposal", "tasks"} for pages in linked.values())


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
        first = next((start for _, start, _ in sections(text)), len(text.split("\n")) + 1)
        opening = " ".join(line.strip() for line in text.split("\n")[: first - 2])
        if ROADMAP_OPENING not in opening:
            problems.append(f"{ROADMAP} does not open with what it says of its items")
        if "Now" in found and not ends_on_the_build(section_of(text, "Now")[1]):
            problems.append(
                f"{ROADMAP}: Now does not end with the line on the build, which links a "
                "change's proposal and tasks"
            )
    _, documentation = section_of(read(root / "README.md"), DOCUMENTATION)
    if f"]({ROADMAP})" not in "\n".join(documentation):
        problems.append(f"README.md's list of documentation does not link {ROADMAP}")
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
    """The text that R209 and R210 hold: the roadmap, each feature page's section and
    each Markdown file in the backlog's folder, each with its name, the folder its links
    resolve from, its first line's number, its lines, and its page's whole text, whose
    headings its links may name."""
    found = []
    roadmap = read(root / ROADMAP)
    if roadmap:
        found.append((ROADMAP, "docs", 1, roadmap.split("\n"), roadmap))
    for page in feature_pages(root):
        text = read(page)
        start, lines = section_of(text, FEATURE_SECTION)
        if lines:
            found.append((page.relative_to(root).as_posix(), "docs/features", start, lines, text))
    for page in sorted((root / BACKLOG).glob("*.md")):
        if page.is_file() and not page.is_symlink():
            text = read(page)
            found.append((page.relative_to(root).as_posix(), BACKLOG, 1, text.split("\n"), text))
    return found


def unlinked(text: str) -> str:
    """The text with each link's target taken out, which its own check reads, keeping the
    target's line feeds so that each line keeps its number."""
    return TARGET.sub(lambda target: "](" + "\n" * target.group(0).count("\n"), text)


def shown(text: str) -> str:
    """The text near enough as GitHub shows it to read a name in: inline code as written,
    without its backticks, and prose without the emphasis marks next to a dot."""
    parts, last = [], 0
    for code in INLINE_CODE.finditer(text):
        parts += [BESIDE_A_DOT.sub("", text[last : code.start()]), code.group(2)]
        last = code.end()
    return "".join([*parts, BESIDE_A_DOT.sub("", text[last:])])


def others_write(path: str) -> str:
    """The folder whose files others write that a path lies in, or nothing."""
    return next((folder for folder in OTHERS_WRITE if path.startswith(folder)), "")


def address_problems(name: str, start: int, text: str, files: set[str]) -> list[str]:
    """The paths that the text gives, which name only tracked files outside the folders
    that others write, and the hosts, IP addresses and commit IDs that it names, in prose
    or in inline code."""
    problems = []
    bare = unlinked(text)
    for offset, line in enumerate(bare.split("\n")):
        for token in OWNER_REPO.findall(line):
            path = token.rstrip(".")
            if path not in files:
                problems.append(
                    f"{name}:{start + offset} names {path}, which is not a tracked file of "
                    "this repository"
                )
            elif folder := others_write(path):
                problems.append(
                    f"{name}:{start + offset} names {path}, a file under {folder} that others write"
                )
    seen = shown(bare)

    def at(found: re.Match[str]) -> str:
        return f"{name}:{start + seen.count(chr(10), 0, found.start())}"

    for found in NAME.finditer(seen):
        token = found.group(0).rstrip(".")
        if token in files:
            continue
        for segment in token.split("/"):
            host = segment.strip("._")
            labels = host.split(".")
            if len(labels) > 1 and LETTERS.fullmatch(labels[-1]) and host not in NOT_HOSTS:
                problems.append(f"{at(found)} names {host}, which reads as a host")
    for found in ADDRESS.finditer(seen):
        problems.append(f"{at(found)} names {found.group(0)}, which reads as an IP address")
    for found in COMMIT_ID.finditer(seen):
        ident = found.group(0)
        if any(c.isdigit() for c in ident) and not ident.isdigit():
            problems.append(f"{at(found)} names {ident}, which reads as a commit ID")
    return problems


def link_problems(root: Path) -> list[str]:
    return link_problems_in(root, checked_text(root))


def link_problems_in(root: Path, texts: list[tuple[str, str, int, list[str], str]]) -> list[str]:
    """R209's reading of each text: its name, the folder its links resolve from, its first
    line's number, its lines, and its page's whole text, whose headings its links may name."""
    files = tracked(root)
    problems = []
    for name, base, start, lines, page in texts:
        own = anchors(page)
        text = "\n".join(lines)
        for offset, line in enumerate(lines):
            where = f"{name}:{start + offset}"
            inner = CONTAINER.sub("", line, count=1)
            if FENCE.match(inner):
                problems.append(f"{where} holds a fenced code block")
            if inner.startswith("    "):
                problems.append(f"{where} holds indented code")
            if WEB_ADDRESS.search(line):
                problems.append(f"{where} gives a web address")
            if "@" in line:
                problems.append(f"{where} holds @, which GitHub turns into a link or a mention")
            if "![" in line:
                problems.append(f"{where} holds an image")
            if EMPHASIZED_PATH.search(line):
                problems.append(f"{where} marks a path with emphasis")
        problems += address_problems(name, start, text, files)
        for code in INLINE_CODE.finditer(text):
            if " " in padless(code.group(2)) or "\n" in code.group(2):
                number = start + text.count("\n", 0, code.start())
                problems.append(f"{name}:{number} {SPACED_CODE}")
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
    if folder := others_write(resolved):
        return [f"{where} links to {address}, a file under {folder} that others write"]
    if resolved not in files or path.endswith("/"):
        return [f"{where} links to {address}, which is not a tracked file of this repository"]
    if fragment and fragment not in anchors(read(root / resolved)):
        return [f"{where} links to {address}, whose file has no such heading"]
    return []


def hidden_text_problems(root: Path) -> list[str]:
    return hidden_text_problems_in(checked_text(root))


def hidden_text_problems_in(texts: list[tuple[str, str, int, list[str], str]]) -> list[str]:
    """R210's reading of each text, given as `link_problems_in` takes it."""
    problems = []
    for name, _, start, lines, _ in texts:
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
        + risk_problems(root)
        + link_problems(root)
        + hidden_text_problems(root)
    )


def test_the_repository_has_no_roadmap_problem() -> None:
    assert roadmap_problems(ROOT) == []


def test_the_repository_gives_each_check_something_to_examine() -> None:
    """A check that examined nothing fails."""
    assert len(risks(ROOT)[0]) > 0
    assert len(feature_pages(ROOT)) > 0
    backlog = sorted((ROOT / BACKLOG).glob("*.md"))
    assert len(backlog) > 1
    assert len(checked_text(ROOT)) == len(feature_pages(ROOT)) + 1 + len(backlog)
    assert [path for _, path in changes(ROOT) if (path / "tasks.md").is_file()]


# A synthetic tree that has no problem. Each test plants one defect into it.


def item(
    number: int,
    title: str,
    status: str,
    brief: str,
    rests: str = "none",
    issue: str = "none",
    pulls: str = "none",
    changed: str = "2026-01-01",
    why: str = "",
) -> str:
    """A backlog item's text in its form."""
    text = (
        f"# B-{number:03d}: {title}\n\n"
        f"- **Status:** {status}\n"
        f"- **Last changed:** {changed}\n"
        f"- **Brief:** {brief}\n"
        f"- **Rests on:** {rests}\n"
        f"- **Issue:** {issue}\n"
        f"- **Pull requests:** {pulls}\n\n"
        "## Problem\n\nWhy it matters.\n\n"
        "## What done looks like\n\nWhat holds once it is done.\n\n"
        "## Postponed points\n\nNone.\n"
    )
    return text + (f"\n## Why it was dropped\n\n{why}\n" if why else "")


ITEMS = {
    f"{BACKLOG}/B-001-a-thing.md": item(
        1, "A thing", "Planned", "A thing to build first.", "R1, task 1.1 of `c`", pulls="7"
    ),
    f"{BACKLOG}/B-002-another-thing.md": item(
        2,
        "Another thing",
        "Open to feedback and contributions",
        "Another thing. It rests on more.",
        "T1, A1, B-001",
        issue="3",
    ),
    f"{BACKLOG}/B-003-other-agents.md": item(
        3, "Other agents", "Planned", "Agents other than one.", "DR-003, DR-001"
    ),
    f"{BACKLOG}/B-004-a-done-thing.md": item(
        4, "A done thing", "Done", "It is done.", "task 1.2 of `c`", pulls="5, 6"
    ),
    f"{BACKLOG}/B-005-a-dropped-thing.md": item(
        5, "A dropped thing", "Dropped", "It was dropped.", "R1", why="Nobody needs it."
    ),
}


def index_line(name: str) -> str:
    """The roadmap's line for an item of the synthetic tree."""
    head = ITEMS[name].split("\n")
    ident, title = head[0][2:].split(": ", 1)
    status, changed, brief = (line.split(":** ", 1)[1] for line in head[2:5])
    target = f"backlog/{name.rsplit('/', 1)[1]}"
    return f"- [{ident}: {title}]({target}) - {status}, last changed {changed}. {brief}"


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
    "openspec/changes/c/proposal.md": "# Proposal\n",
    "docs/assumptions/README.md": "# Assumptions\n\n- **A1.** An assumption.\n",
    **ITEMS,
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
    "vendor/a/SKILL.md": "# A skill that others write\n",
    ".claude/skills/a/SKILL.md": "# A skill that others write\n",
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
        f"{ROADMAP_OPENING} Issues are named by number.\n\n"
        "## Now\n\n"
        "What is under way.\n\n"
        f"{index_line(f'{BACKLOG}/B-001-a-thing.md')}\n\n"
        "Then the build, by its [proposal](../openspec/changes/c/proposal.md) and "
        "[tasks](../openspec/changes/c/tasks.md).\n\n"
        "## Next\n\n"
        "What follows.\n\n"
        f"{index_line(f'{BACKLOG}/B-002-another-thing.md')}\n\n"
        "## Later\n\n"
        f"{LATER_OPENING}\n\n"
        f"{index_line(f'{BACKLOG}/B-003-other-agents.md')}\n\n"
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
        ("## Now\n\n", "", f"{ROADMAP} has no section Now"),
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
            f"{ROADMAP}:36 holds a fenced code block",
        ),
        ("None yet.\n", "None yet.\n\nPromises\n--------\n", f"{ROADMAP}:37 holds a heading"),
        ("None yet.\n", "None yet.\n\n ## Promises\n", f"{ROADMAP}:36 holds a heading"),
    ],
)
def test_a_section_out_of_form_is_reported(
    tmp_path: Path, old: str, new: str, problem: str
) -> None:
    found = section_problems(planted(tmp_path, ROADMAP, old, new)) + link_problems(tmp_path)
    assert [p for p in found if p.startswith(problem)], found


def test_a_roadmap_without_its_opening_is_reported(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, f"{ROADMAP_OPENING} ", "")
    assert section_problems(root) == [f"{ROADMAP} does not open with what it says of its items"]


def test_the_opening_must_come_before_the_first_section(tmp_path: Path) -> None:
    text = TREE[ROADMAP].replace(f"{ROADMAP_OPENING} ", "")
    text = text.replace("What is under way.", f"What is under way. {ROADMAP_OPENING}")
    root = make_tree(tmp_path, {ROADMAP: text})
    assert section_problems(root) == [f"{ROADMAP} does not open with what it says of its items"]


NO_BUILD_LINE = (
    f"{ROADMAP}: Now does not end with the line on the build, which links a change's "
    "proposal and tasks"
)


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("Then the build, by its", "- Then the build, by its"),
        ("[tasks](../openspec/changes/c/tasks.md)", "tasks"),
        ("[proposal](../openspec/changes/c/proposal.md)", "proposal"),
        (
            "[tasks](../openspec/changes/c/tasks.md)",
            "[tasks](../openspec/changes/old/tasks.md)",
        ),
        (".md).\n\n## Next", ".md).\n\nAnd more.\n\n## Next"),
    ],
)
def test_now_without_the_line_on_the_build_is_reported(tmp_path: Path, old: str, new: str) -> None:
    root = planted(tmp_path, ROADMAP, old, new)
    assert NO_BUILD_LINE in section_problems(root)


def test_sections_out_of_order_are_reported(tmp_path: Path) -> None:
    now = TREE[ROADMAP][TREE[ROADMAP].index("## Now") : TREE[ROADMAP].index("## Next")]
    text = TREE[ROADMAP].replace(now, "").replace("## Known bugs\n", f"{now}## Known bugs\n")
    root = make_tree(tmp_path, {ROADMAP: text})
    assert section_problems(root) == [
        f"{ROADMAP} gives its sections out of order: "
        "Next, Later, Known limitations, Now, Known bugs"
    ]


def test_two_changes_of_one_name_are_reported(tmp_path: Path) -> None:
    root = make_tree(tmp_path, {"openspec/changes/old/tasks.md": "- [ ] 2.1 Do it again\n"})
    assert change_problems(root) == [
        "two changes are named `old`, so a task cannot be named by its change"
    ]


# R232: each change's tasks are read as GitHub shows them.

TASKS = "openspec/changes/c/tasks.md"
OLD_TASKS = "openspec/changes/archive/2026-01-01-old/tasks.md"
UNREAD = "holds a checkbox that the checks do not read as a task"
COMMENT = "holds an HTML comment, which GitHub does not show"
HTML = "opens with <, with which Markdown starts HTML that can hide the lines after it"
FENCED = "holds a code fence, inside which GitHub shows a tick as code"


def with_tasks(root: Path, added: str, where: str = TASKS) -> Path:
    """The synthetic tree with lines added to the end of a change's `tasks.md`."""
    return make_tree(root, {where: TREE[where] + added})


def test_a_task_list_read_as_github_shows_it_has_no_problem(tmp_path: Path) -> None:
    root = with_tasks(tmp_path, "\n## 2. More\n\n- [X] 2.1 Did more\n  - A note on it.\n")
    assert task_list_problems(root) == []


@pytest.mark.parametrize(
    "line",
    [
        "  - [x] 1.3 Did a thing",
        "* [x] 1.3 Did a thing",
        "+ [x] 1.3 Did a thing",
        "1. [x] 1.3 Did a thing",
        "> - [x] 1.3 Did a thing",
        "- [x]  1.3 Did a thing",
        "- [x]\t1.3 Did a thing",
        "- [x] **1.3** Did a thing",
        "- [x] 1.3: Did a thing",
        "- [x] 1.3.1 Did a thing",
        "- [x] \uff11.3 Did a thing",
        "- [X]1.3 Did a thing",
        "- [x] 1.3",
        "- [ ]  1.3 Do a thing",
        "Then - [x] 1.3 Did a thing",
        "\\- [x] 1.3 Did a thing",
    ],
)
def test_a_checkbox_that_the_checks_do_not_read_as_a_task_is_reported(
    tmp_path: Path, line: str
) -> None:
    assert task_list_problems(with_tasks(tmp_path, line + "\n")) == [f"{TASKS}:3 {UNREAD}"]


@pytest.mark.parametrize(
    ("added", "problems"),
    [
        ("<!--\n- [x] 1.3 Did a thing\n-->\n", [(3, COMMENT)]),
        ("- [ ] 1.3 Do a thing <!-- and another -->\n", [(3, COMMENT)]),
        ("<!-- - [x] 1.3 Did a thing -->\n", [(3, UNREAD), (3, COMMENT)]),
        ("<details>\n\n- [x] 1.3 Did a thing\n\n</details>\n", [(3, HTML), (7, HTML)]),
        ("  <div>\n- [x] 1.3 Did a thing\n", [(3, HTML)]),
        ("\t<script>\n", [(3, HTML)]),
        ("```\n- [x] 1.3 Did a thing\n```\n", [(3, FENCED), (5, FENCED)]),
        ("~~~ text\n- [x] 1.3 Did a thing\n~~~\n", [(3, FENCED), (5, FENCED)]),
        ("   ```\n", [(3, FENCED)]),
    ],
)
def test_text_that_github_does_not_show_in_a_task_list_is_reported(
    tmp_path: Path, added: str, problems: list[tuple[int, str]]
) -> None:
    found = task_list_problems(with_tasks(tmp_path, added))
    assert found == [f"{TASKS}:{number} {problem}" for number, problem in problems]


@pytest.mark.parametrize(
    ("added", "problem"),
    [
        ("- [ ] 1.2 Did a thing again\n", "gives task 1.2 on lines 2 and 3"),
        ("- [x] 1.1 Did a thing\n", "gives task 1.1 on lines 1 and 3"),
        ("- [ ] 1.1 Do it\n- [ ] 1.1 Do it\n", "gives task 1.1 on lines 1, 3 and 4"),
    ],
)
def test_a_task_given_twice_is_reported(tmp_path: Path, added: str, problem: str) -> None:
    assert task_list_problems(with_tasks(tmp_path, added)) == [f"{TASKS} {problem}"]


def test_an_archived_task_list_is_read_too(tmp_path: Path) -> None:
    root = with_tasks(tmp_path, "<!--\n- [ ] 2.1 Did an old thing\n-->\n", OLD_TASKS)
    assert task_list_problems(root) == [
        f"{OLD_TASKS}:2 {COMMENT}",
        f"{OLD_TASKS} gives task 2.1 on lines 1 and 3",
    ]


def test_each_change_s_tasks_are_read_as_github_shows_them() -> None:
    assert task_list_problems(ROOT) == []


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
    ("`git config --global pr-cost.capture true`", "holds inline code that holds a space"),
    ("``a ` b``", "holds inline code that holds a space"),
    ("`git\nconfig`", "holds inline code that holds a space"),
    ("    pip install something", "holds indented code"),
    (">     pip install something", "holds indented code"),
    ("-     pip install something", "holds indented code"),
    ("> ~~~", "holds a fenced code block"),
    ("- ```", "holds a fenced code block"),
    ("```", "holds a fenced code block"),
    ("example.org", "names example.org, which reads as a host"),
    ("See example.org.", "names example.org, which reads as a host"),
    ("`example.org`", "names example.org, which reads as a host"),
    ("a.example.org/", "names a.example.org, which reads as a host"),
    ("GitHub.com", "names GitHub.com, which reads as a host"),
    ("[example.org](#now)", "names example.org, which reads as a host"),
    ("evil.*example*", "names evil.example, which reads as a host"),
    ("*evil*.example", "names evil.example, which reads as a host"),
    ("**evil**.__example__", "names evil.example, which reads as a host"),
    ("evil.~~example~~", "names evil.example, which reads as a host"),
    ("evil.`example`", "names evil.example, which reads as a host"),
    ("192.0.2.1", "names 192.0.2.1, which reads as an IP address"),
    ("`192.0.2.1`", "names 192.0.2.1, which reads as an IP address"),
    ("0123abc", "names 0123abc, which reads as a commit ID"),
    ("`0123ABCDEF`", "names 0123ABCDEF, which reads as a commit ID"),
    ("[a skill](../vendor/a/SKILL.md)", "links to ../vendor/a/SKILL.md, a file under vendor/"),
    (
        "[a skill](../.claude/skills/a/SKILL.md)",
        "links to ../.claude/skills/a/SKILL.md, a file under .claude/skills/",
    ),
    ("vendor/a/SKILL.md", "names vendor/a/SKILL.md, a file under vendor/"),
    (
        "`.claude/skills/a/SKILL.md`",
        "names .claude/skills/a/SKILL.md, a file under .claude/skills/",
    ),
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
    new = new.replace("](%2e%2e/%2e%2e/x", "](%2e%2e/%2e%2e/%2e%2e/x").replace("](../", "](../../")
    problem = problem.replace("features/", "").replace("%2e%2e/%2e%2e/x", "%2e%2e/%2e%2e/%2e%2e/x")
    problem = problem.replace("to ../", "to ../../")
    found = link_problems(planted(tmp_path, FEATURE, "holds the rest.", f"holds the rest.\n{new}"))
    assert [p for p in found if p.startswith(FEATURE) and problem in p], found


ITEM = f"{BACKLOG}/B-001-a-thing.md"


@pytest.mark.parametrize(("new", "problem"), LINKS_ELSEWHERE)
def test_a_link_elsewhere_in_a_backlog_item_is_reported(
    tmp_path: Path, new: str, problem: str
) -> None:
    new = new.replace("](../", "](../../").replace("](features/", "](../features/")
    new = new.replace("](roadmap.md", "](../roadmap.md")
    new = new.replace("](%2e%2e/%2e%2e/x", "](%2e%2e/%2e%2e/%2e%2e/x")
    problem = problem.replace("to ../", "to ../../").replace("features/", "../features/")
    problem = problem.replace("%2e%2e/%2e%2e/x", "%2e%2e/%2e%2e/%2e%2e/x")
    found = link_problems(planted(tmp_path, ITEM, "Why it matters.", new))
    assert [p for p in found if p.startswith(ITEM) and problem in p], found


def test_the_backlog_page_is_held_too(tmp_path: Path) -> None:
    page = f"{BACKLOG}/README.md"
    root = make_tree(tmp_path, {page: "# Backlog\n\nSee [the roadmap](../roadmap.md) and a@b.\n"})
    assert link_problems(root) == [f"{page}:3 holds @, which GitHub turns into a link or a mention"]


def test_padding_that_markdown_strips_from_inline_code_is_no_space(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, "None yet.", "A backtick, `` ` ``, and ` x `.")
    assert link_problems(root) == []


LOOKS_LIKE_A_HOST = [
    "README.md, `README.md`, docs/requirements.md and `docs/requirements.md`.",
    "It ends *here*. It ends _here_. It ends **here**. It ends ~~here~~.",
    "Python 3.11, version 1.2.3, task 1.29 and the file `.claude`.",
    "A glob, `DR-*.md`, is read as written.",
    "It was defaced 1234567 times.",
]


@pytest.mark.parametrize("new", LOOKS_LIKE_A_HOST)
def test_what_only_looks_like_a_host_an_address_or_a_commit_id_passes(
    tmp_path: Path, new: str
) -> None:
    assert link_problems(planted(tmp_path, ROADMAP, "None yet.", new)) == []
    assert link_problems(planted(tmp_path, ITEM, "Why it matters.", new)) == []


@pytest.mark.parametrize("name", sorted(NOT_HOSTS))
def test_a_name_listed_as_no_host_passes_until_it_is_taken_off_the_list(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    root = planted(tmp_path, ROADMAP, "None yet.", f"`{name}` and {name}.")
    assert link_problems(root) == []
    monkeypatch.delitem(NOT_HOSTS, name)
    assert link_problems(root) == [f"{ROADMAP}:34 names {name}, which reads as a host"] * 2


def test_a_host_is_reported_at_its_line_after_a_target_that_spans_lines(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, "None yet.", '[Now](#now\n"a title") and\nexample.org')
    assert sorted(link_problems(root)) == [
        f"{ROADMAP}:34 holds a link with a title",
        f"{ROADMAP}:36 names example.org, which reads as a host",
    ]


def test_a_link_reports_the_line_its_target_stands_on(tmp_path: Path) -> None:
    root = planted(tmp_path, ROADMAP, "None yet.", "None\n[yet](../../../issues/15).")
    assert link_problems(root) == [
        f"{ROADMAP}:35 links to ../../../issues/15, which leaves the repository"
    ]


HIDDEN_TEXT = [
    ("A\u200bB", "holds U+200B"),
    ("A\u202eB", "holds U+202E"),
    ("A\rB", "holds U+000D"),
    ("A<!-- hidden -->B", "holds <, with which Markdown starts HTML"),
    ("`<!-- hidden -->`", "holds <, with which Markdown starts HTML"),
    ("[x]: features/thing.md", "holds ]:, with which Markdown defines a link"),
    ('[a`]: x "` hidden"', "holds ]:, with which Markdown defines a link"),
    ("A &#65; B", "holds &, with which Markdown writes a character"),
    ("\\`<!-- hidden -->\\`", "holds a backslash"),
    ("A | B", "holds |, with which Markdown builds a table"),
    ("`a|b`", "holds |, with which Markdown builds a table"),
]


@pytest.mark.parametrize(("new", "problem"), HIDDEN_TEXT)
def test_hidden_text_in_the_roadmap_is_reported(tmp_path: Path, new: str, problem: str) -> None:
    found = hidden_text_problems(planted(tmp_path, ROADMAP, "None yet.", new))
    assert f"{ROADMAP}:34 {problem}" in [p[: len(ROADMAP) + 4 + len(problem)] for p in found], found


@pytest.mark.parametrize(("new", "problem"), HIDDEN_TEXT)
def test_hidden_text_in_a_feature_section_is_reported(
    tmp_path: Path, new: str, problem: str
) -> None:
    root = planted(tmp_path, FEATURE, "holds the rest.", f"holds the rest.\n{new}")
    found = hidden_text_problems(root)
    assert f"{FEATURE}:11 {problem}" in [p[: len(FEATURE) + 4 + len(problem)] for p in found], found


def test_text_outside_the_feature_section_is_not_held(tmp_path: Path) -> None:
    root = make_tree(tmp_path)
    assert hidden_text_problems(root) == [] and link_problems(root) == []


@pytest.mark.parametrize(("new", "problem"), HIDDEN_TEXT)
def test_hidden_text_in_a_backlog_item_is_reported(tmp_path: Path, new: str, problem: str) -> None:
    found = hidden_text_problems(planted(tmp_path, ITEM, "Why it matters.", new))
    assert f"{ITEM}:12 {problem}" in [p[: len(ITEM) + 4 + len(problem)] for p in found], found
