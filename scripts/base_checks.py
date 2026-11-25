"""Run the base commit's own checks over the merge commit that GitHub tests for a pull
request (R299, R317, DR-312).

The workflow of the base commit's checks runs this file from the base branch's checkout,
on `pull_request_target`, so that a pull request that changes a check together with what
it checks cannot change the check that judges it. It reads the pull request's tree only
from git's objects: it checks nothing out, runs nothing from that tree, and gives each
name to git after `--end-of-options` or `--`.

It fetches the merge commit that GitHub tests, fails where it cannot or where that commit
merges another head than the event's, and runs the base's own vendor check over the
commit's tree where the pull request changes `vendor/`. The base holds no marketplace
check until task 6.9 adds them, which the log says where the root marketplace file
changes. Either way, the log says what was compared, or that nothing in scope changed.

The event's values reach it only through the environment: `PR_NUMBER`, `HEAD_SHA`, and
GitHub's own `GITHUB_SERVER_URL` and `GITHUB_REPOSITORY`.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MERGE = "refs/base-checks/merge"
NUMBER = re.compile(r"[1-9][0-9]{0,9}")
COMMIT = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
VENDOR = "vendor/"
MARKETPLACE = ".claude-plugin/marketplace.json"


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=False
    )


def given(environ: Mapping[str, str]) -> tuple[str, str, str] | str:
    """The pull request's number, its head and the remote to fetch from, or what is wrong
    with the value that the event gave."""
    number = environ.get("PR_NUMBER", "")
    head = environ.get("HEAD_SHA", "")
    repository = environ.get("GITHUB_REPOSITORY", "")
    server = environ.get("GITHUB_SERVER_URL", "").rstrip("/")
    if not NUMBER.fullmatch(number):
        return "PR_NUMBER is not a pull request's number"
    if not COMMIT.fullmatch(head):
        return "HEAD_SHA is not a full commit id"
    if not REPOSITORY.fullmatch(repository) or ".." in repository:
        return "GITHUB_REPOSITORY is not an owner and a name"
    if not server:
        return "GITHUB_SERVER_URL is not set"
    return number, head, f"{server}/{repository}.git"


def main(environ: Mapping[str, str]) -> int:
    values = given(environ)
    if isinstance(values, str):
        print(f"base checks: {values}", file=sys.stderr)
        return 2
    number, head, remote = values
    fetched = git(
        "fetch", "-q", "--no-tags", "--no-recurse-submodules", "--depth=2",
        "--end-of-options", remote, f"+refs/pull/{number}/merge:{MERGE}",
    )  # fmt: skip
    if fetched.returncode != 0:
        print(
            f"base checks: cannot fetch the merge commit of pull request {number}, as where"
            " it conflicts with its base",
            file=sys.stderr,
        )
        return 1
    merge = git("rev-parse", "--verify", "--end-of-options", f"{MERGE}^{{commit}}").stdout.strip()
    merged = git("rev-parse", "--verify", "--end-of-options", f"{merge}^2").stdout.strip()
    if merged != head:
        print(
            f"base checks: GitHub's merge commit {merge} merges {merged or 'no head'}, not"
            f" the pull request's head {head}",
            file=sys.stderr,
        )
        return 1
    listed = git(
        "diff-tree", "-r", "-z", "--no-renames", "--name-only", "--end-of-options",
        f"{merge}^1", merge,
    )  # fmt: skip
    if listed.returncode != 0:
        print(f"base checks: cannot list what {merge} changes", file=sys.stderr)
        return 1
    changed = [path for path in listed.stdout.split("\0") if path]
    status = 0
    compared = False
    if any(path.startswith(VENDOR) for path in changed):
        compared = True
        checked = subprocess.run(
            ["bash", str(ROOT / "scripts" / "sync-superpowers.sh"), "--check-commit", merge],
            check=False,
        )
        print(f"base checks: compared vendor/superpowers at {merge} with its pinned commit")
        status = status or checked.returncode
    if MARKETPLACE in changed:
        compared = True
        print(
            f"base checks: {MARKETPLACE} changed, and the base holds no marketplace check yet;"
            " task 6.9 adds them"
        )
    if not compared:
        print(f"base checks: nothing in scope changed, so nothing was compared at {merge}")
    return 1 if status else 0


if __name__ == "__main__":
    sys.exit(main(os.environ))
