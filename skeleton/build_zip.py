#!/usr/bin/env python3
# The walking skeleton of the agentic PR cost calculator: not the tool or a release.
# Builds the skeleton's plugin zip from git's objects of one commit, never from the working
# tree, the same bytes each time, and prints its SHA-256 for the owner to check before the
# upload (R243, DR-245, T192). Run from a clone: `build_zip.py <full commit id> <out.zip>`; it
# prints the commit beside the hash, so that the hash names what it was built from.
"""Build the walking skeleton's plugin zip, byte for byte the same from the same commit."""

from __future__ import annotations

import hashlib
import io
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

# Each file in the zip, and the file of the commit that it is built from.
FILES = {
    ".claude-plugin/plugin.json": "skeleton/plugin.json",
    "capture.py": "skeleton/capture.py",
    "hooks/hooks.json": "skeleton/hooks.json",
}
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def build(repo: Path, commit: str, env: dict[str, str]) -> io.BytesIO:
    """The zip of the commit's skeleton files, with fixed times, modes and order."""
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as archive:
        for name, source in sorted(FILES.items()):
            content = subprocess.run(
                ["git", "show", f"{commit}:{source}"],
                cwd=repo,
                env=env,
                check=True,
                capture_output=True,
            ).stdout
            info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
            # Stored, not compressed, so that the bytes do not depend on the zlib of the builder.
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            info.create_system = 3
            archive.writestr(info, content)
    out.seek(0)
    return out


def main(argv: list[str]) -> int:
    commit, target = argv
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        print("build_zip.py: give a full commit id, not a name that can move", file=sys.stderr)
        return 2
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    data = build(Path.cwd(), commit, env).getvalue()
    Path(target).write_bytes(data)
    print(commit, hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
