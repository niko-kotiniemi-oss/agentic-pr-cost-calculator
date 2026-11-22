"""Run a command and write what it prints in printable ASCII.

Usage: python3 -I scripts/printable_log.py COMMAND [ARGUMENT ...]

Each workflow under `.github/workflows/` runs every step's script through this filter, as
the shell that its defaults give: `python3 -I scripts/printable_log.py bash --noprofile
--norc -eo pipefail {0}`, GitHub's own shell for `bash` (R278). The command's output and
its errors are read as one stream and written as they arrive, each character other than
printable ASCII and a line feed as `U+` and its code point, and each byte that is not UTF-8
as `\\x` and its value, so that no check that quotes a path or a file's text as it is, as
ruff, mypy, pytest and `diff` do, carries a hidden character into a log that a session
reads (T264). The filter exits with the command's status, with 128 and the signal's number
where a signal stopped the command, and with 127 where it could not start it.
"""

from __future__ import annotations

import codecs
import os
import subprocess
import sys
from collections.abc import Callable, Iterable, Iterator

# What a shell exits with where it cannot start a command, and where it is given none.
NOT_STARTED = 127
NO_COMMAND = 2
CHUNK = 65536
# The bytes that are not UTF-8, as `surrogateescape` reads them.
NOT_UTF8 = range(0xDC80, 0xDD00)


def shown(text: str) -> str:
    """The text with each character other than printable ASCII and a line feed given as `U+`
    and its code point, and each byte that is not UTF-8 as `\\x` and its value."""
    return "".join(
        character
        if " " <= character <= "~" or character == "\n"
        else f"\\x{ord(character) - 0xDC00:02X}"
        if ord(character) in NOT_UTF8
        else f"U+{ord(character):04X}"
        for character in text
    )


def relay(chunks: Iterable[bytes], write: Callable[[bytes], object]) -> None:
    """Write each chunk in printable ASCII as it arrives, holding back only the start of a
    character that a later chunk ends."""
    decoder = codecs.getincrementaldecoder("utf-8")("surrogateescape")
    for chunk in chunks:
        write(shown(decoder.decode(chunk)).encode("ascii"))
    write(shown(decoder.decode(b"", final=True)).encode("ascii"))


def reads(descriptor: int) -> Iterator[bytes]:
    """Each chunk that the descriptor gives, as soon as it gives one, up to its end."""
    while chunk := os.read(descriptor, CHUNK):
        yield chunk


def main(argv: list[str]) -> int:
    out = sys.stdout.buffer

    def write(data: bytes) -> None:
        out.write(data)
        out.flush()

    if not argv:
        write(b"printable_log: no command to run\n")
        return NO_COMMAND
    try:
        child = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except OSError as error:
        write(
            f"printable_log: could not start {shown(argv[0])}: {type(error).__name__}\n".encode(
                "ascii"
            )
        )
        return NOT_STARTED
    assert child.stdout is not None
    with child.stdout:
        relay(reads(child.stdout.fileno()), write)
    status = child.wait()
    return 128 - status if status < 0 else status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
