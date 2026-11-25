"""Tests of the job that runs the base commit's own checks over a pull request (R299, R317).

The job runs `scripts/base_checks.py` from the base branch's checkout. It fetches the merge
commit that GitHub tests, checks that it merges the pull request's head, and runs the base's
own vendor check over that commit's tree where the pull request changes `vendor/`, saying in
its log what it compared or that nothing in scope changed. These tests run the real script
in a repository of their own, against a local remote that stands in for GitHub, with a stub
in the base's place of the sync script that says which copy ran: never the network.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

import pytest
from test_vendor_sync import git, isolated

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "base_checks.py"
NUMBER = "7"
REPOSITORY = "owner/repo"

# The base's copy of the sync script: it says that it ran and with what, and exits with the
# status that the file beside it gives.
BASE_SYNC = """\
#!/usr/bin/env bash
echo "the base's sync ran with $*"
exit "$(cat "$(dirname "$0")/status")"
"""
PR_SYNC = """\
#!/usr/bin/env bash
echo "the pull request's sync ran"
exit 0
"""


@dataclass(frozen=True)
class Pull:
    base: Path
    server: Path
    head: str
    merge: str


def commit_files(work: Path, files: dict[str, str], message: str) -> str:
    for path, text in files.items():
        (work / path).parent.mkdir(parents=True, exist_ok=True)
        (work / path).write_text(text, encoding="utf-8")
        git("add", "--", path, cwd=work)
    git("commit", "-q", "--allow-empty", "-m", message, cwd=work)
    return git("rev-parse", "HEAD", cwd=work)


def pull(tmp_path: Path, changes: dict[str, str], merge_ref: bool = True) -> Pull:
    """A remote that holds the base and the merge commit that GitHub would test for a pull
    request with these changes, and the base's checkout, which holds the job's script and a
    stub of the base's sync script."""
    work = tmp_path / "work"
    work.mkdir()
    git("init", "-q", "-b", "main", cwd=work)
    base_files = {
        "scripts/base_checks.py": SCRIPT.read_text(encoding="utf-8"),
        "scripts/sync-superpowers.sh": BASE_SYNC,
        "scripts/status": "0\n",
        "vendor/superpowers/LICENSE": "as released\n",
        "README.md": "a readme\n",
    }
    base = commit_files(work, base_files, "base")
    git("checkout", "-q", "-b", "topic", cwd=work)
    head = commit_files(work, changes, "the pull request")
    git("checkout", "-q", "main", cwd=work)
    git("merge", "-q", "--no-ff", "--no-edit", "topic", cwd=work)
    merge = git("rev-parse", "HEAD", cwd=work)
    server = tmp_path / "server"
    bare = server / f"{REPOSITORY}.git"
    bare.parent.mkdir(parents=True)
    git("clone", "-q", "--bare", str(work), str(bare), cwd=tmp_path)
    git("update-ref", "refs/heads/main", base, cwd=bare)
    if merge_ref:
        git("update-ref", f"refs/pull/{NUMBER}/merge", merge, cwd=bare)
    checkout = tmp_path / "base"
    git("clone", "-q", "--depth", "1", bare.as_uri(), str(checkout), cwd=tmp_path)
    (checkout / "scripts" / "sync-superpowers.sh").chmod(0o755)
    return Pull(checkout, server, head, merge)


def run(case: Pull, **given: str) -> subprocess.CompletedProcess[str]:
    environment = {
        **isolated(),
        "PR_NUMBER": NUMBER,
        "HEAD_SHA": case.head,
        "GITHUB_SERVER_URL": case.server.as_uri(),
        "GITHUB_REPOSITORY": REPOSITORY,
        **given,
    }
    return subprocess.run(
        ["python3", "-I", str(case.base / "scripts" / "base_checks.py")],
        cwd=case.base,
        env=environment,
        capture_output=True,
        text=True,
    )


def test_a_pull_request_that_changes_nothing_in_scope_passes_and_says_so(tmp_path: Path) -> None:
    done = run(pull(tmp_path, {"README.md": "changed\n"}))
    assert done.returncode == 0, done.stderr
    assert "nothing in scope changed, so nothing was compared" in done.stdout
    assert "sync ran" not in done.stdout


def test_a_pull_request_that_changes_the_vendored_copy_runs_the_base_s_check(
    tmp_path: Path,
) -> None:
    case = pull(tmp_path, {"vendor/superpowers/LICENSE": "edited\n"})
    done = run(case)
    assert done.returncode == 0, done.stderr
    assert f"the base's sync ran with --check-commit {case.merge}" in done.stdout
    assert f"ran the base's vendor check over {case.merge}, which exited 0" in done.stdout


def test_a_pull_request_whose_vendored_copy_the_base_refuses_fails(tmp_path: Path) -> None:
    case = pull(tmp_path, {"vendor/superpowers/LICENSE": "edited\n"})
    (case.base / "scripts" / "status").write_text("1\n", encoding="utf-8")
    done = run(case)
    assert done.returncode == 1
    assert "the base's sync ran" in done.stdout


def test_a_pull_request_that_weakens_the_check_and_changes_what_it_checks_runs_the_base_s(
    tmp_path: Path,
) -> None:
    changes = {"scripts/sync-superpowers.sh": PR_SYNC, "vendor/superpowers/LICENSE": "edited\n"}
    case = pull(tmp_path, changes)
    (case.base / "scripts" / "status").write_text("1\n", encoding="utf-8")
    done = run(case)
    assert done.returncode == 1
    assert "the base's sync ran" in done.stdout
    assert "the pull request's sync ran" not in done.stdout


def test_a_pull_request_that_changes_the_root_marketplace_file_says_what_the_base_holds(
    tmp_path: Path,
) -> None:
    done = run(pull(tmp_path, {".claude-plugin/marketplace.json": "{}\n"}))
    assert done.returncode == 0, done.stderr
    assert "the base holds no marketplace check yet" in done.stdout


def test_a_merge_commit_that_cannot_be_fetched_fails(tmp_path: Path) -> None:
    done = run(pull(tmp_path, {"README.md": "changed\n"}, merge_ref=False))
    assert done.returncode == 1
    assert "cannot fetch the merge commit" in done.stderr
    assert "nothing in scope changed" not in done.stdout


def loaded(case: Pull, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    """The base's copy of the script, loaded in this process with the environment that
    `run` gives it, so that a test can stand in for its waits."""
    for name in list(os.environ):
        monkeypatch.delenv(name)
    for name, value in isolated().items():
        monkeypatch.setenv(name, value)
    spec = importlib.util.spec_from_file_location(
        "base_checks", case.base / "scripts" / "base_checks.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def environ(case: Pull, **given: str) -> dict[str, str]:
    return {
        "PR_NUMBER": NUMBER,
        "HEAD_SHA": case.head,
        "GITHUB_SERVER_URL": case.server.as_uri(),
        "GITHUB_REPOSITORY": REPOSITORY,
        **given,
    }


def test_a_merge_commit_of_another_head_fails_after_each_wait(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    case = pull(tmp_path, {"README.md": "changed\n"})
    module = loaded(case, monkeypatch)
    waits: list[float] = []
    status = module.main(environ(case, HEAD_SHA="1" * 40), delays=(1.0, 2.0), sleep=waits.append)
    assert status == 1
    assert waits == [1.0, 2.0]
    assert f"merges {case.head}, not the pull request's head {'1' * 40}" in capsys.readouterr().err


def test_a_merge_commit_that_github_updates_during_a_wait_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    case = pull(tmp_path, {"README.md": "changed\n"})
    bare = case.server / f"{REPOSITORY}.git"
    git("update-ref", f"refs/pull/{NUMBER}/merge", f"{case.merge}^1", cwd=bare)
    module = loaded(case, monkeypatch)

    def github_catches_up(delay: float) -> None:
        git("update-ref", f"refs/pull/{NUMBER}/merge", case.merge, cwd=bare)

    status = module.main(environ(case), delays=(1.0,), sleep=github_catches_up)
    assert status == 0, capsys.readouterr().err
    assert "nothing in scope changed" in capsys.readouterr().out


def test_the_job_turns_workflow_commands_off_while_it_runs(tmp_path: Path) -> None:
    done = run(pull(tmp_path, {"README.md": "changed\n"}))
    first, *_, last = done.stdout.splitlines()
    assert first.startswith("::stop-commands::")
    token = first.removeprefix("::stop-commands::")
    assert len(token) == 32
    assert last == f"::{token}::"


@pytest.mark.parametrize(
    "path",
    [
        "Vendor/superpowers/skills/x/SKILL.md",
        "vendor/Superpowers/skills/x/SKILL.md",
        "vendor/superpowers./skills/x/SKILL.md",
        "vendor/superpowers /skills/x/SKILL.md",
        ".claude-plugin/Marketplace.json",
    ],
)
def test_a_path_that_a_case_insensitive_system_writes_into_a_checked_path_fails(
    tmp_path: Path, path: str
) -> None:
    done = run(pull(tmp_path, {path: "planted\n"}))
    assert done.returncode == 1
    assert f"changes {path!r}, which a case-insensitive system writes into a checked" in (
        done.stderr
    )
    assert "sync ran" not in done.stdout


def test_a_path_that_is_not_utf_8_is_read(tmp_path: Path) -> None:
    case = pull(tmp_path, {"README.md": "changed\n"})
    done = run(case)
    assert done.returncode == 0, done.stderr
    work = tmp_path / "odd"
    git("clone", "-q", str(case.server / f"{REPOSITORY}.git"), str(work), cwd=tmp_path)
    git("checkout", "-q", "--detach", case.head, cwd=work)
    (work / os.fsdecode(b"notes-\xff.txt")).write_text("odd\n", encoding="utf-8")
    git("add", "--", os.fsdecode(b"notes-\xff.txt"), cwd=work)
    git("commit", "-q", "-m", "an odd name", cwd=work)
    head = git("rev-parse", "HEAD", cwd=work)
    git("checkout", "-q", "--detach", case.merge + "^1", cwd=work)
    git("merge", "-q", "--no-ff", "--no-edit", head, cwd=work)
    merge = git("rev-parse", "HEAD", cwd=work)
    git(
        "push",
        "-q",
        str(case.server / f"{REPOSITORY}.git"),
        f"+{merge}:refs/pull/{NUMBER}/merge",
        cwd=work,
    )
    done = run(case, HEAD_SHA=head)
    assert done.returncode == 0, done.stderr
    assert "nothing in scope changed" in done.stdout


@pytest.mark.parametrize(
    ("variable", "value"),
    [
        ("PR_NUMBER", "7; rm -rf /"),
        ("PR_NUMBER", ""),
        ("HEAD_SHA", "--output=x"),
        ("GITHUB_REPOSITORY", "owner/repo/../other"),
        ("GITHUB_REPOSITORY", "--upload-pack=x"),
        ("GITHUB_SERVER_URL", ""),
    ],
)
def test_an_event_value_of_another_form_stops_the_job(
    tmp_path: Path, variable: str, value: str
) -> None:
    done = run(pull(tmp_path, {"README.md": "changed\n"}), **{variable: value})
    assert done.returncode == 2
    assert f"{variable} is not" in done.stderr
