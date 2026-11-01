"""git reads `GIT_NO_LAZY_FETCH`, and with it set fetches nothing.

The capture step runs every git command with `GIT_NO_LAZY_FETCH=1` (R111), so
that a partial clone whose sparse checkout leaves `.pr-cost/` out does not fetch
ledger blobs from its remote (T45). This file reproduces what was seen with git:
in a clone made with `--filter=blob:none`, a command that needs a blob that the
clone lacks fetches it from the remote, and with the variable set, the same
command fails and fetches nothing. The assumptions record the build that this was
seen on, and the releases whose source names the variable nowhere, where it does
not hold.

The remote is a repository in the test's own folder, reached over `file://`, so
no test opens a connection. Each git runs with every `GIT_` variable of the
caller's environment removed and with empty global configuration and no system
configuration, so that no setting of the person running the tests takes part.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

LEDGER = ".pr-cost/ledger/2026-11/entry.jsonl"
CONTENT = '{"model":"example"}\n'


def git(cwd: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, env=env, capture_output=True, text=True)


@dataclass(frozen=True)
class Clone:
    path: Path
    blob: str
    env: dict[str, str]

    def git(
        self, *args: str, extra: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        return git(self.path, {**self.env, **(extra or {})}, *args)

    def has_blob(self) -> bool:
        """Whether the clone holds the blob, read without asking any remote for it."""
        listed = self.git("cat-file", "--batch-all-objects", "--batch-check=%(objectname)")
        assert listed.returncode == 0, listed.stderr
        return self.blob in listed.stdout.split()


def isolated_env(folder: Path) -> dict[str, str]:
    empty = folder / "empty.gitconfig"
    empty.write_text("")
    env = {name: value for name, value in os.environ.items() if not name.startswith("GIT_")}
    return {
        **env,
        "GIT_CONFIG_GLOBAL": str(empty),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.invalid",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.invalid",
    }


def run(env: dict[str, str], cwd: Path, *args: str) -> str:
    done = git(cwd, env, *args)
    assert done.returncode == 0, f"git {' '.join(args)}: {done.stderr}"
    return done.stdout.strip()


@pytest.fixture
def clone(tmp_path: Path) -> Clone:
    env = isolated_env(tmp_path)
    remote = tmp_path / "remote"
    remote.mkdir()
    run(env, remote, "init", "-q")
    ledger = remote / LEDGER
    ledger.parent.mkdir(parents=True)
    ledger.write_text(CONTENT)
    run(env, remote, "add", LEDGER)
    run(env, remote, "commit", "-q", "-m", "A ledger file")
    run(env, remote, "config", "uploadpack.allowFilter", "true")
    blob = run(env, remote, "rev-parse", f"HEAD:{LEDGER}")
    url = remote.resolve().as_uri()
    run(env, tmp_path, "clone", "-q", "--no-checkout", "--filter=blob:none", url, "clone")
    found = Clone(tmp_path / "clone", blob, env)
    assert not found.has_blob(), "the partial clone holds the blob, so nothing below is tested"
    return found


def test_git_no_lazy_fetch_keeps_a_partial_clone_from_fetching(clone: Clone) -> None:
    held = clone.git("cat-file", "-s", clone.blob, extra={"GIT_NO_LAZY_FETCH": "1"})
    # The design records that git was seen to exit with 128, its fatal error.
    assert held.returncode == 128, f"git exited with {held.returncode}: {held.stderr}"
    assert not clone.has_blob()

    fetched = clone.git("cat-file", "-s", clone.blob)
    assert fetched.returncode == 0, fetched.stderr
    assert fetched.stdout.strip() == str(len(CONTENT.encode()))
    assert clone.has_blob()


def test_a_variable_that_git_does_not_read_leaves_lazy_fetching_on(clone: Clone) -> None:
    # A git that ignores GIT_NO_LAZY_FETCH treats it as it treats this name, so
    # the test above fails on such a git.
    fetched = clone.git("cat-file", "-s", clone.blob, extra={"GIT_NO_LAZY_FETCH_UNREAD": "1"})
    assert fetched.returncode == 0, fetched.stderr
    assert clone.has_blob()
