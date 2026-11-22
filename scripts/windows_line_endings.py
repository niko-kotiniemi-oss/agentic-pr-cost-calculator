"""Save each file that this repository writes, but its scripts, with Windows line endings.

CI's job `windows-line-endings` runs this on a fresh checkout and then every check that CI
runs on a pull request, so that a check which reads a file of the working tree otherwise than
git stages it, through `staged_bytes` of `scripts/conventions.py`, fails there (R276,
DR-281). It rewrites, in the working tree alone, each file that git's index tracks as a file,
that others do not write, that is no script, a file whose name ends in `.sh`, that starts
with `#!` or that git records as executable, and that holds a line feed, with a carriage
return before each line feed, and it stages nothing. It fails where it rewrote nothing, or
where a file that it rewrote holds no carriage return before a line feed, as where a later
attribute had a checkout write line feeds, and says that it examined no Windows line endings.
Like the tool, it runs on Python 3.11 and later with the standard library alone.

Usage: python scripts/windows_line_endings.py [root]

Exit 0 when it saved each such file so, 1 when it examined no Windows line endings, and 2
when git cannot list the tracked files.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from conventions import NO_WINDOWS_LINE_ENDINGS, is_script, shown_path, written_by_others

# The modes with which git's index tracks a file, and the one of an executable file.
FILES = ("100644", "100755")
EXECUTABLE = "100755"
# A line feed that no carriage return comes right before.
BARE_LINE_FEED = re.compile(rb"(?<!\r)\n")


class UnlistedError(Exception):
    """Raised when git cannot list the files that its index tracks."""


def save(root: Path) -> list[str]:
    """Each file that it saved with a carriage return before each line feed, by its tracked
    path. Raises UnlistedError when git cannot list the tracked files, as where root is no
    folder."""
    try:
        done = subprocess.run(
            ["git", "ls-files", "--stage", "-z"],
            cwd=root,
            capture_output=True,
            check=False,
            env={key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
        )
    except OSError as error:
        raise UnlistedError(error.strerror or type(error).__name__) from error
    if done.returncode != 0:
        raise UnlistedError(done.stderr.decode("utf-8", "replace").strip())
    saved = []
    for record in done.stdout.split(b"\0"):
        if not record:
            continue
        head, _, name = record.partition(b"\t")
        mode = head.split(b" ")[0].decode("ascii")
        path = name.decode("utf-8", "surrogateescape")
        file = root / path
        if mode not in FILES or written_by_others(path) or file.is_symlink() or not file.is_file():
            continue
        data = file.read_bytes()
        if b"\n" not in data or is_script(path, data, mode == EXECUTABLE):
            continue
        file.write_bytes(BARE_LINE_FEED.sub(b"\r\n", data))
        saved.append(path)
    return saved


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    try:
        saved = save(root)
    except UnlistedError as error:
        print(f"windows-line-endings: git ls-files failed: {error}", file=sys.stderr)
        return 2
    unmet = [path for path in saved if b"\r\n" not in (root / path).read_bytes()]
    if not saved or unmet:
        where = f" in {', '.join(map(shown_path, unmet))}" if unmet else ""
        print(f"windows-line-endings: {NO_WINDOWS_LINE_ENDINGS}{where}", file=sys.stderr)
        return 1
    print(f"windows-line-endings: saved {len(saved)} files with Windows line endings")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
