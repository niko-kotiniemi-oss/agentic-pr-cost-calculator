"""`scripts/verify-openspec.sh` finds what the pinned OpenSpec CLI writes anywhere in the tree.

The script empties the generated `openspec-*` skills and has the CLI write them again, and
fails when they differ from what git holds. It also fails when the CLI's run changes
anything outside them, such as an `AGENTS.md` that a context file would not name, or a
`CLAUDE.local.md` that git ignores, while a person's own uncommitted work, there before
and after the run, passes (design decision 21). These tests run the script in a repository
of their own, with a stand-in for the CLI that writes what each test asks, so that no test
installs OpenSpec or uses the network.
"""

from __future__ import annotations

import json
import shutil
import stat
import subprocess
from pathlib import Path

import pytest
from test_roadmap import GIT_ENVIRONMENT, session_free_environment

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify-openspec.sh"
SKILL = ".claude/skills/openspec-explore/SKILL.md"
# The stand-in CLI: it gives the pinned version, writes the skill again, then whatever
# FAKE_WRITES names, and fails validation with its own code, so that a run that gets past
# the comparisons ends there, where a test can tell it from a failed comparison.
FAKE_CLI = """#!/usr/bin/env bash
case "$1" in
  --version) echo 9.9.9 ;;
  config) exit 0 ;;
  update)
    printf '%s\\n' "${FAKE_SKILL:-generated}" > .claude/skills/openspec-explore/SKILL.md
    if [ -n "${FAKE_WRITES:-}" ]; then
      mkdir -p "$(dirname "$FAKE_WRITES")"
      printf 'written by the CLI\\n' > "$FAKE_WRITES"
    fi
    ;;
  validate) exit 7 ;;
  *) exit 9 ;;
esac
"""
PAST_THE_COMPARISONS = 7
IDENTITY = {
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.invalid",
}


def environment(**extra: str) -> dict[str, str]:
    return {**session_free_environment(), **GIT_ENVIRONMENT, **IDENTITY, **extra}


def repository(root: Path) -> Path:
    """A repository with the script, a lock that pins the stand-in's version, one
    generated skill, a README and an ignore file, committed, and the stand-in CLI."""
    files = {
        "scripts/verify-openspec.sh": SCRIPT.read_text(encoding="utf-8"),
        "package-lock.json": json.dumps(
            {"packages": {"node_modules/@fission-ai/openspec": {"version": "9.9.9"}}}
        ),
        SKILL: "generated\n",
        "README.md": "A readme.\n",
        ".gitignore": "node_modules/\nCLAUDE.local.md\n",
    }
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    cli = root / "node_modules" / ".bin" / "openspec"
    cli.parent.mkdir(parents=True)
    cli.write_text(FAKE_CLI, encoding="utf-8")
    cli.chmod(cli.stat().st_mode | stat.S_IXUSR)
    for args in (["init", "-q"], ["add", "--", *files], ["commit", "-q", "-m", "Start"]):
        subprocess.run(["git", *args], cwd=root, check=True, env=environment())
    return root


def run(root: Path, **extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "scripts/verify-openspec.sh"],
        cwd=root,
        capture_output=True,
        text=True,
        env=environment(**extra),
        check=False,
    )


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    if shutil.which("bash") is None:
        pytest.fail("bash is not installed, so the script cannot run")
    return repository(tmp_path)


def test_a_run_that_writes_only_the_skills_gets_past_the_comparisons(repo: Path) -> None:
    done = run(repo)
    assert done.returncode == PAST_THE_COMPARISONS, done.stderr
    assert "--- every spec and change validates, strictly ---" in done.stdout


def test_a_person_s_own_uncommitted_work_passes(repo: Path) -> None:
    (repo / "README.md").write_text("A readme, being edited.\n", encoding="utf-8")
    (repo / "notes.md").write_text("Notes.\n", encoding="utf-8")
    (repo / "CLAUDE.local.md").write_text("Personal rules.\n", encoding="utf-8")
    done = run(repo)
    assert done.returncode == PAST_THE_COMPARISONS, done.stderr


@pytest.mark.parametrize(
    ("written", "shown"),
    [
        ("AGENTS.md", "+ ?? AGENTS.md"),
        ("openspec/AGENTS.md", "+ ?? openspec/AGENTS.md"),
        ("CLAUDE.local.md", "+ !! CLAUDE.local.md"),
        (".claude/commands/opsx/apply.md", "+ ?? .claude/commands/opsx/apply.md"),
        ("README.md", "+  M README.md"),
    ],
)
def test_a_file_that_the_cli_writes_outside_the_skills_fails(
    repo: Path, written: str, shown: str
) -> None:
    done = run(repo, FAKE_WRITES=written)
    assert done.returncode == 1
    assert "the pinned CLI changed files outside the generated skills" in done.stderr
    assert shown in done.stderr


def test_a_file_that_the_cli_rewrites_after_a_person_changed_it_fails(repo: Path) -> None:
    (repo / "README.md").write_text("A readme, being edited.\n", encoding="utf-8")
    done = run(repo, FAKE_WRITES="README.md")
    assert done.returncode == 1
    assert "-  M README.md " in done.stderr
    assert "+  M README.md " in done.stderr


def test_skills_that_differ_from_what_git_holds_still_fail(repo: Path) -> None:
    done = run(repo, FAKE_SKILL="another text")
    assert done.returncode == 1
    assert "the generated skills differ from what the pinned CLI writes" in done.stderr
    assert SKILL in done.stderr
