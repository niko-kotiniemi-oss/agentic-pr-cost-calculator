"""List each line that a rewording changed by more than a word to avoid replaced with its term.

    python3 scripts/rewording.py [BASE]

Run in the repository, it compares HEAD with where HEAD left BASE, which is
`refs/remotes/origin/main` unless given, in the Markdown files that the wording test
reads, and prints Markdown for the pull request (task 1.20; design decision 14; T90,
T94). It names both commits by their full hashes, compares a renamed page with what it
was, and names each changed file that it does not compare. It lists the changes to
`CLAUDE.md` first and those to the guide next, since both steer. It reads each page with
`scripts/wording.py`, as the wording test does, so that a word inside code, among the
glossary's words to avoid or in a title that an accepted record quotes is never taken
for a replacement. A replacement is judged by the glossary at HEAD, and a line that
replaces a word that the base's glossary does not give for the same term is also listed
apart, since that rule is the pull request's own. It exits 2, saying why, when it cannot
compare, as when the glossary at HEAD is not in its form.

Its output is a pull request's account of its own rewording, so run the copies of this
script and of `scripts/wording.py` that the default branch holds, not the pull
request's (T94):

    copy=$(mktemp -d)
    git show refs/remotes/origin/main:scripts/rewording.py > "$copy/rewording.py"
    git show refs/remotes/origin/main:scripts/wording.py > "$copy/wording.py"
    python3 "$copy/rewording.py"
"""

from __future__ import annotations

import difflib
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from wording import (
    BACKTICKS,
    DEFAULT_BRANCH,
    FINAL_Y,
    GLOSSARY,
    KEPT,
    MARKDOWN,
    Entry,
    found_words,
    glossary,
    kept_at,
    readable,
    same,
    shown,
)

USAGE = "usage: python3 scripts/rewording.py [BASE]"
# The files that steer, whose changes are listed first, in this order (T94).
STEERING = ("CLAUDE.md", "docs/patterns.md")
TOKEN = re.compile(r"\S+|\s+")
# How many tokens, each a word or the spaces after one, are shown on each side of a change.
CONTEXT = 8
# A control character, a line break among them, written as its escape inside a code span.
CONTROL = {char: f"\\x{char:02x}" for char in [*range(32), 127]}
ADDED = "An added file's lines are not compared, since the base holds none of them."
KEPT_AS_WRITTEN = "which keeps its words as written"


class Refused(Exception):
    """Why the comparison cannot be made."""


def git(*args: str, refused: str = "") -> str:
    """What a git command prints, a byte that is not UTF-8 kept as an escape. If it fails,
    the comparison is refused for the reason given, or, where none is given since the
    command should not fail, for git's own."""
    try:
        return shown(Path.cwd(), *args)
    except subprocess.CalledProcessError as failed:
        raise Refused(refused or failed.stderr.decode("utf-8", "replace").strip()) from None


def blob(commit: str, path: str) -> str:
    return git("cat-file", "blob", f"{commit}:{path}")


def ticks(text: str, least: int = 1) -> str:
    """A run of backticks longer than any in the text, and at least this long, so that the
    text cannot close it."""
    longest = max((len(run) for run in BACKTICKS.findall(text)), default=0)
    return "`" * max(least, longest + 1)


def code(text: str) -> str:
    """Text as a code span that nothing in it can close: its backticks outrun every run in
    the text, and each control character, a line break among them, is written as its
    escape. A space pads a text that starts or ends with a backtick or a space."""
    text = text.translate(CONTROL)
    run = ticks(text)
    pad = " " if text[:1] in ("`", " ") or text[-1:] in ("`", " ") else ""
    return f"{run}{pad}{text}{pad}{run}"


def entries_at(commit: str) -> list[Entry]:
    """The glossary's entries in a commit, none where it holds no glossary."""
    if not git("ls-tree", "--name-only", "--full-tree", commit, "--", GLOSSARY):
        return []
    return glossary(blob(commit, GLOSSARY))[0]


def new_words(entries: list[Entry], base: list[Entry]) -> frozenset[str]:
    """The words to avoid that the base's glossary does not give for the same term."""
    return frozenset(
        word
        for entry in entries
        for word in entry.avoid
        if not any(
            other.term == entry.term and any(same(word, given) for given in other.avoid)
            for other in base
        )
    )


def changed_files(since: str) -> list[tuple[str, str, str]]:
    """Each Markdown file that the branch changed, as its status, its path at the base and
    its path at HEAD, a rename's two paths differing."""
    fields = git(
        "diff-tree", "-r", "-z", "-M", "--name-status", since, "HEAD", "--", *MARKDOWN
    ).split("\0")[:-1]
    changes = []
    at = 0
    while at < len(fields):
        status = fields[at]
        if status.startswith("R"):
            changes.append((status, fields[at + 1], fields[at + 2]))
            at += 3
        else:
            changes.append((status, fields[at + 1], fields[at + 1]))
            at += 2
    return changes


def form(term: str, word: str, found: str) -> str:
    """The term in the form that the word to avoid was found in: plural where that was, and
    with its first letter raised where only the found word's was."""
    if found.split()[-1].casefold() != word.split(" ")[-1].casefold():
        term = term[:-1] + "ies" if FINAL_Y.search(term) else term + "s"
    if found[0].isupper() and word[0].islower():
        term = term[0].upper() + term[1:]
    return term


def replaced(line: str, read: str, entries: list[Entry]) -> tuple[str, list[str]]:
    """A line with each word to avoid that its readable text holds replaced with its term,
    and those words, as the glossary gives them."""
    parts: list[str] = []
    words: list[str] = []
    at = 0
    for start, end, word, term in found_words(read, entries):
        parts += [line[at:start], form(term, word, line[start:end])]
        words.append(word)
        at = end
    return "".join([*parts, line[at:]]), words


def part(tokens: list[str], start: int, end: int) -> str:
    """These tokens of a line, with an ellipsis on each side where the line goes on."""
    text = "".join(tokens[start:end])
    if start > 0:
        text = "… " + text.lstrip()
    if end < len(tokens):
        text = text.rstrip() + " …"
    return text


def changed_words(old: str, new: str) -> list[str]:
    """Each group of words that a pair of lines changed, with a few words around it."""
    before, after = TOKEN.findall(old), TOKEN.findall(new)
    matcher = difflib.SequenceMatcher(None, before, after, autojunk=False)
    shown = []
    for group in matcher.get_grouped_opcodes(CONTEXT):
        _, start, _, new_start, _ = group[0]
        _, _, end, _, new_end = group[-1]
        shown += [f"- {part(before, start, end)}", f"+ {part(after, new_start, new_end)}"]
    return shown


def lines(start: int, end: int) -> str:
    """The lines from this index up to that one, by their numbers."""
    return f"line {start + 1}" if end - start == 1 else f"lines {start + 1} to {end}"


def listed(label: str, shown: list[str]) -> list[str]:
    """A hunk as Markdown: its label, then its lines in a fence longer than any run of
    backticks that they hold."""
    fence = ticks("\n".join(shown), 3)
    return [label[0].upper() + label[1:] + ":", "\n".join([f"{fence}diff", *shown, fence])]


def compared(
    path: str,
    old: str,
    new: str,
    entries: list[Entry],
    kept: frozenset[str],
    fresh: frozenset[str],
) -> tuple[list[str], list[str], Counter[str], int]:
    """A changed file's hunks that are more than words to avoid replaced, and its lines that
    replace only words to avoid, one of them new to the glossary, as Markdown; the words
    that the lines that replace only words replaced; and how many lines those are."""
    before, after = old.split("\n"), new.split("\n")
    read = readable(path, old, kept)[0].split("\n")
    hunks: list[str] = []
    renewed: list[str] = []
    words: Counter[str] = Counter()
    only = 0
    matcher = difflib.SequenceMatcher(None, before, after, autojunk=False)
    for tag, start, end, new_start, new_end in matcher.get_opcodes():
        if tag == "replace" and end - start == new_end - new_start:
            for at, new_at in zip(range(start, end), range(new_start, new_end), strict=True):
                expected, found = replaced(before[at], read[at], entries)
                if expected == after[new_at]:
                    words.update(found)
                    only += 1
                    if fresh.intersection(found):
                        shown = changed_words(before[at], after[new_at])
                        renewed += listed(lines(new_at, new_at + 1), shown)
                else:
                    shown = changed_words(before[at], after[new_at])
                    hunks += listed(lines(new_at, new_at + 1), shown)
        elif tag != "equal":
            shown = [f"- {line}" for line in before[start:end]]
            shown += [f"+ {line}" for line in after[new_start:new_end]]
            if tag == "replace":
                label = f"{lines(new_start, new_end)}, in place of {lines(start, end)}"
            elif tag == "delete":
                label = f"{lines(start, end)} of the base, removed"
            else:
                label = f"{lines(new_start, new_end)}, added"
            hunks += listed(label, shown)
    return hunks, renewed, words, only


def counted(number: int, noun: str) -> str:
    return f"{number} {noun}" if number == 1 else f"{number} {noun}s"


def listed_first(change: tuple[str, str, str]) -> tuple[int, str]:
    """Where a changed file is listed: the files that steer first, in their order, a
    rename by either of its paths, then the rest by path."""
    _, old, new = change
    ranks = [STEERING.index(path) if path in STEERING else len(STEERING) for path in (old, new)]
    return (min(ranks), new)


def report(base: str) -> str:
    """The comparison of HEAD with where HEAD left the base, as Markdown."""
    tip = git("rev-parse", "--verify", f"{base}^{{commit}}", refused=f"{base} is not a commit")
    since = git(
        "merge-base", tip.strip(), "HEAD", refused=f"HEAD shares no history with {base}"
    ).strip()
    head = git("rev-parse", "--verify", "HEAD").strip()
    text = git("cat-file", "blob", f"HEAD:{GLOSSARY}", refused=f"HEAD holds no {GLOSSARY}")
    entries, problems = glossary(text)
    if problems:
        raise Refused("\n".join([f"{GLOSSARY} at HEAD is not in its form:", *problems]))
    if not any(entry.avoid for entry in entries):
        raise Refused(f"{GLOSSARY} at HEAD gives no word to avoid")
    fresh = new_words(entries, entries_at(since))
    try:
        kept = kept_at(Path.cwd(), since)
    except subprocess.CalledProcessError as failed:
        raise Refused(failed.stderr.decode("utf-8", "replace").strip()) from None
    changes = sorted(changed_files(since), key=listed_first)
    seen = {path for _, old, new in changes for path in (old, new)}
    every = git("diff-tree", "-r", "-z", "--name-only", since, "HEAD").split("\0")[:-1]
    skipped = [
        (path, f"- {code(path)}, which is not a Markdown file")
        for path in every
        if path not in seen
    ]
    hunks: list[str] = []
    renewed: list[str] = []
    files: list[str] = []
    words: Counter[str] = Counter()
    only = touched = 0
    added = False
    for status, old, new in changes:
        if KEPT.match(new):
            moved = f", renamed to {code(new)}" if old != new else ""
            skipped.append((old, f"- {code(old)}{moved}, {KEPT_AS_WRITTEN}"))
        elif status == "A":
            files.append(f"- Added: {code(new)}")
            added = True
        elif status == "D":
            files.append(f"- Removed: {code(new)}")
        else:
            if old != new:
                files.append(f"- Renamed: {code(old)} to {code(new)}")
            found, fresh_found, replacements, replacing = compared(
                new, blob(since, old), blob("HEAD", new), entries, kept, fresh
            )
            if found:
                hunks += [f"### {code(new)}", *found]
            if fresh_found:
                renewed += [f"### {code(new)}", *fresh_found]
            words += replacements
            only += replacing
            touched += bool(replacing)
    table = [
        f"| {code(word)} | {code(entry.term)} | {words[word]} |"
        f" {'yes' if word in fresh else 'no'} |"
        for entry in entries
        for word in entry.avoid
        if words[word]
    ]
    summary = [
        f"{counted(only, 'line')} in {counted(touched, 'file')} changed only by a word to avoid"
        " replaced with its term:",
        "\n".join(
            [
                "| Word to avoid | Term | Replaced | New to the glossary |",
                "|---|---|---|---|",
                *table,
            ]
        ),
    ]
    blocks = [
        f"Compared HEAD at {code(head)} with {code(since)}, where it left {code(base)}, in the"
        " Markdown files that the wording test reads.",
        "## Changed by more than a word to avoid",
        *(hunks or ["None."]),
        "## Only a word to avoid new to the glossary replaced",
        *(renewed or ["None."]),
        "## Added, removed or renamed",
        "\n".join(files) or "None.",
        *([ADDED] if added else []),
        "## Not compared",
        "\n".join(line for _, line in sorted(skipped)) or "None.",
        "## Only a word to avoid replaced",
        *(summary if only else ["None."]),
    ]
    return "\n\n".join(blocks) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        text = report(argv[0] if argv else DEFAULT_BRANCH)
    except Refused as refusal:
        print(f"rewording: {refusal}", file=sys.stderr)
        return 2
    sys.stdout.write(text.encode("utf-8", "surrogateescape").decode("utf-8", "replace"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
