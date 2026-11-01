"""List each line that a rewording changed by more than a word to avoid replaced with its term.

    python3 scripts/rewording.py [BASE]

Run in the repository, it compares HEAD with where HEAD left BASE, which is
`refs/remotes/origin/main` unless given, in the Markdown files that the wording test
reads, and prints Markdown for the pull request (task 1.20; design decision 14; T90,
T94). It reads each page with `scripts/wording.py`, as the wording test does, so that a
word inside code, among the glossary's words to avoid or in a title that an accepted
record quotes is never taken for a replacement. It exits 2, saying why, when it cannot
compare.
"""

from __future__ import annotations

import difflib
import re
import subprocess
import sys
from collections import Counter

from wording import (
    FINAL_Y,
    GLOSSARY,
    KEPT,
    MARKDOWN,
    RECORD_FILE,
    SPEC_FILE,
    Entry,
    found_words,
    glossary,
    quoted_titles,
    readable,
)

DEFAULT_BASE = "refs/remotes/origin/main"
USAGE = "usage: python3 scripts/rewording.py [BASE]"
STEERING = "CLAUDE.md"
TOKEN = re.compile(r"\S+|\s+")
BACKTICKS = re.compile(r"`+")
# How many tokens, each a word or the spaces after one, are shown on each side of a change.
CONTEXT = 8


class Refused(Exception):
    """Why the comparison cannot be made."""


def git(*args: str, refused: str = "") -> str:
    """What a git command prints. If it fails, the comparison is refused for the reason
    given, or, where none is given since the command should not fail, for git's own."""
    done = subprocess.run(["git", *args], capture_output=True, check=False)
    if done.returncode:
        raise Refused(refused or done.stderr.decode("utf-8", "replace").strip())
    return done.stdout.decode("utf-8")


def blob(commit: str, path: str) -> str:
    return git("cat-file", "blob", f"{commit}:{path}")


def kept_at(commit: str) -> frozenset[str]:
    """The titles in a commit's specs that one of its accepted records quotes."""
    listing = git(
        "ls-tree",
        "-r",
        "-z",
        "--name-only",
        "--full-tree",
        commit,
        "--",
        "openspec",
        "docs/decisions",
    )
    paths = listing.split("\0")

    def texts(named: re.Pattern[str]) -> list[str]:
        return [blob(commit, path) for path in paths if named.fullmatch(path)]

    return quoted_titles(texts(SPEC_FILE), texts(RECORD_FILE))


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
    longest = max((len(run) for run in BACKTICKS.findall("\n".join(shown))), default=0)
    fence = "`" * max(3, longest + 1)
    return [label[0].upper() + label[1:] + ":", "\n".join([f"{fence}diff", *shown, fence])]


def compared(
    path: str, old: str, new: str, entries: list[Entry], kept: frozenset[str]
) -> tuple[list[str], Counter[str], int]:
    """A changed file's hunks that are more than words to avoid replaced, as Markdown; the
    words that its other changed lines replaced; and how many lines those are."""
    before, after = old.split("\n"), new.split("\n")
    read = readable(path, old, kept)[0].split("\n")
    hunks: list[str] = []
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
    return hunks, words, only


def counted(number: int, noun: str) -> str:
    return f"{number} {noun}" if number == 1 else f"{number} {noun}s"


def report(base: str) -> str:
    """The comparison of HEAD with where HEAD left the base, as Markdown."""
    tip = git("rev-parse", "--verify", f"{base}^{{commit}}", refused=f"{base} is not a commit")
    since = git(
        "merge-base", tip.strip(), "HEAD", refused=f"HEAD shares no history with {base}"
    ).strip()
    text = git("cat-file", "blob", f"HEAD:{GLOSSARY}", refused=f"HEAD holds no {GLOSSARY}")
    entries = glossary(text)[0]
    if not any(entry.avoid for entry in entries):
        raise Refused(f"{GLOSSARY} at HEAD gives no word to avoid")
    kept = kept_at(since)
    fields = git("diff-tree", "-r", "-z", "--name-status", since, "HEAD", "--", *MARKDOWN)
    named = fields.split("\0")[:-1]
    changes = sorted(
        (
            change
            for change in zip(named[::2], named[1::2], strict=True)
            if not KEPT.match(change[1])
        ),
        key=lambda change: (change[1] != STEERING, change[1]),
    )
    hunks: list[str] = []
    files: list[str] = []
    words: Counter[str] = Counter()
    only = touched = 0
    for status, path in changes:
        if status == "A":
            files.append(f"- Added: `{path}`")
        elif status == "D":
            files.append(f"- Removed: `{path}`")
        else:
            found, replacements, replacing = compared(
                path, blob(since, path), blob("HEAD", path), entries, kept
            )
            if found:
                hunks += [f"### `{path}`", *found]
            words += replacements
            only += replacing
            touched += bool(replacing)
    table = [
        f"| {word} | {entry.term} | {words[word]} |"
        for entry in entries
        for word in entry.avoid
        if words[word]
    ]
    summary = [
        f"{counted(only, 'line')} in {counted(touched, 'file')} changed only by a word to avoid"
        " replaced with its term:",
        "\n".join(["| Word to avoid | Term | Replaced |", "|---|---|---|", *table]),
    ]
    blocks = [
        f"Compared with `{base}` at `{since[:12]}`, where HEAD left it, in the Markdown files"
        " that the wording test reads.",
        "## Changed by more than a word to avoid",
        *(hunks or ["None."]),
        "## Added or removed",
        "\n".join(files) or "None.",
        "## Only a word to avoid replaced",
        *(summary if only else ["None."]),
    ]
    return "\n\n".join(blocks) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        text = report(argv[0] if argv else DEFAULT_BASE)
    except Refused as refusal:
        print(f"rewording: {refusal}", file=sys.stderr)
        return 2
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
