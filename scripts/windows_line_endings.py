"""Save each file that this repository writes, but its scripts, with Windows line endings.

CI's job `windows-line-endings` runs this on a fresh checkout and then every check that CI
runs on a pull request, so that a check which reads a file of the working tree otherwise than
git stages it, through `staged_bytes` of `scripts/conventions.py`, fails there (R276,
DR-281). It rewrites, in the working tree alone, each file that git's index tracks as a file,
that others do not write, that is no script, a file whose name ends in `.sh`, that starts
with `#!` or that git records as executable, and that holds a line feed, with a carriage
return before each line feed, and it stages nothing. It reads git's index and the working
tree as the test of characters does, so that it writes into no folder that a link names, and
it fails where it rewrote nothing, and says that it examined no Windows line endings.
Like the tool, it runs on Python 3.11 and later with the standard library alone.

Usage: python scripts/windows_line_endings.py [root]

Exit 0 when it saved each such file so, 1 when it examined no Windows line endings, and 2
when git cannot list the tracked files or root lies below the top of its working tree.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from conventions import (
    EXECUTABLE,
    FILE,
    NO_WINDOWS_LINE_ENDINGS,
    UnlistedError,
    in_working_tree,
    is_script,
    session_free_environment,
    shown_path,
    tracked_entries,
    written_by_others,
)

# A line feed that no carriage return comes right before.
BARE_LINE_FEED = re.compile(rb"(?<!\r)\n")


def below_the_top(root: Path) -> str:
    """The folder from the top of its working tree that root is, or nothing at the top,
    where git gives each tracked path as the files that others write are matched."""
    done = subprocess.run(
        ["git", "rev-parse", "--show-prefix"],
        cwd=root,
        capture_output=True,
        check=False,
        env=session_free_environment(),
    )
    if done.returncode != 0:
        raise UnlistedError(
            f"git rev-parse failed: {done.stderr.decode('utf-8', 'replace').strip()}"
        )
    return done.stdout.decode("utf-8", "surrogateescape").removesuffix("\n")


def save(root: Path) -> list[str]:
    """Each file that it saved with a carriage return before each line feed, by its tracked
    path, reading the working tree as the test of characters reads it, through no link.
    Raises UnlistedError when git cannot list the tracked files, as where root is no folder,
    or where root lies below the top of its working tree."""
    entries = tracked_entries(root)
    prefix = below_the_top(root)
    if prefix:
        raise UnlistedError(
            f"{shown_path(str(root))} is a folder below the top of its working tree,"
            f" {shown_path(prefix)}, where git would give each path from that folder"
        )
    folders: dict[str, str] = {}
    saved = []
    for entry in entries:
        if entry.mode not in (FILE, EXECUTABLE) or written_by_others(entry.path):
            continue
        held = in_working_tree(root, entry.path, folders)
        if held is None or held[0] != "file":
            continue
        data = held[1]
        if b"\n" not in data or is_script(entry.path, data, entry.mode == EXECUTABLE):
            continue
        (root / entry.path).write_bytes(BARE_LINE_FEED.sub(b"\r\n", data))
        saved.append(entry.path)
    return saved


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    try:
        saved = save(root)
    except UnlistedError as error:
        print(f"windows-line-endings: {error}", file=sys.stderr)
        return 2
    if not saved:
        print(f"windows-line-endings: {NO_WINDOWS_LINE_ENDINGS}", file=sys.stderr)
        return 1
    print(f"windows-line-endings: saved {len(saved)} files with Windows line endings")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
