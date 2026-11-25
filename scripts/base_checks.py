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

It reads each changed path as a case-insensitive system writes it (R323), so that a path
that Windows or macOS would write into `vendor/superpowers/` is in scope and, spelt
otherwise, fails. GitHub's workflow commands stay off while it runs, so that a path or a
line of the pull request's tree in the log cannot act as one.
"""

from __future__ import annotations

import os
import re
import secrets
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MERGE = "refs/base-checks/merge"
NUMBER = re.compile(r"[1-9][0-9]{0,9}")
COMMIT = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
VENDOR = "vendor/"
CHECKED = "vendor/superpowers/"
MARKETPLACE = ".claude-plugin/marketplace.json"
# How long to wait before each new fetch while GitHub's merge commit still merges an
# earlier head, as it can just after a push, since the event does not wait for it.
DELAYS = (5.0, 10.0, 20.0)


def git(*args: str) -> subprocess.CompletedProcess[str]:
    # surrogateescape: a path that is not UTF-8 is read rather than stopping the job.
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=True,
        errors="surrogateescape",
        check=False,
    )


def folded(path: str) -> str:
    """The path as Windows and macOS write it: each part in lower case, with no trailing
    dot or space."""
    return "/".join(part.rstrip(". ").casefold() for part in path.split("/"))


def misspelt(path: str) -> bool:
    """Whether a path falls under the checked copy or is the root marketplace file, as a
    case-insensitive system writes it, without being spelt as that path is."""
    fold = folded(path)
    if fold == MARKETPLACE:
        return path != MARKETPLACE
    return (fold + "/").startswith(CHECKED) and not (path + "/").startswith(CHECKED)


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


def fetch_merge(
    number: str, head: str, remote: str, delays: Sequence[float], sleep: Callable[[float], None]
) -> tuple[str, str] | str:
    """GitHub's merge commit for the pull request and the head that it merges, fetched
    again after each delay while it merges another head than the event's; or what is wrong."""
    merge = merged = ""
    for delay in [0.0, *delays]:
        if delay:
            sleep(delay)
        fetched = git(
            "fetch", "-q", "--no-tags", "--no-recurse-submodules", "--depth=2",
            "--end-of-options", remote, f"+refs/pull/{number}/merge:{MERGE}",
        )  # fmt: skip
        if fetched.returncode != 0:
            return (
                f"cannot fetch the merge commit of pull request {number}, as where it"
                f" conflicts with its base: {fetched.stderr.strip()}"
            )
        merge = git("rev-parse", "--verify", "--end-of-options", f"{MERGE}^{{commit}}").stdout
        merge = merge.strip()
        merged = git("rev-parse", "--verify", "--end-of-options", f"{merge}^2").stdout.strip()
        if merged == head:
            return merge, merged
    return (
        f"GitHub's merge commit {merge} merges {merged or 'no head'}, not the pull request's"
        f" head {head}: GitHub has not made the merge commit of that head yet, or cannot, as"
        " where it conflicts with its base"
    )


def main(
    environ: Mapping[str, str],
    delays: Sequence[float] = DELAYS,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    values = given(environ)
    if isinstance(values, str):
        print(f"base checks: {values}", file=sys.stderr)
        return 2
    number, head, remote = values
    # No workflow command acts until the token is printed again (GitHub's stop-commands).
    token = secrets.token_hex(16)
    print(f"::stop-commands::{token}", flush=True)
    try:
        return checks(number, head, remote, delays, sleep)
    finally:
        sys.stderr.flush()
        print(f"::{token}::", flush=True)


def checks(
    number: str, head: str, remote: str, delays: Sequence[float], sleep: Callable[[float], None]
) -> int:
    fetched = fetch_merge(number, head, remote, delays, sleep)
    if isinstance(fetched, str):
        print(f"base checks: {fetched}", file=sys.stderr)
        return 1
    merge, _ = fetched
    listed = git(
        "diff-tree", "-r", "-z", "--no-renames", "--name-only", "--end-of-options",
        f"{merge}^1", merge,
    )  # fmt: skip
    if listed.returncode != 0:
        print(f"base checks: cannot list what {merge} changes: {listed.stderr.strip()}",
              file=sys.stderr)  # fmt: skip
        return 1
    changed = [path for path in listed.stdout.split("\0") if path]
    wrong = [path for path in changed if misspelt(path)]
    for path in wrong:
        print(
            f"base checks: the pull request changes {path!r}, which a case-insensitive system"
            " writes into a checked path that it does not spell so",
            file=sys.stderr,
        )
    if wrong:
        return 1
    status = 0
    compared = False
    if any(folded(path).startswith(VENDOR) for path in changed):
        compared = True
        sys.stdout.flush()
        checked = subprocess.run(
            ["bash", str(ROOT / "scripts" / "sync-superpowers.sh"), "--check-commit", merge],
            check=False,
        )
        print(
            f"base checks: ran the base's vendor check over {merge}, which exited"
            f" {checked.returncode}"
        )
        status = status or checked.returncode
    if MARKETPLACE in {folded(path) for path in changed}:
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
