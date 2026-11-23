"""`scripts/verify-openspec.sh` finds what the pinned OpenSpec CLI writes anywhere in the tree.

The script empties the generated `openspec-*` skills and has the CLI write them again, and
fails when they differ from what git holds. It also fails when anything outside them
changes between its first call of the CLI and its end, on whatever path it ends, such as
an `AGENTS.md` that a context file would not name, or a `CLAUDE.local.md` that git ignores,
while a person's own uncommitted work, there before and after the run, passes; and it stops
with 2, before it empties a skill, when it cannot read the working tree (design decision
21). These tests run the script in a repository of their own, with a stand-in for the CLI
that writes what each test asks, in the call that it names, so that no test installs
OpenSpec or uses the network.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest
from test_roadmap import GIT_ENVIRONMENT, session_free_environment
from test_vendor_sync import IDENTITY

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify-openspec.sh"
SKILL = ".claude/skills/openspec-explore/SKILL.md"
# The stand-in CLI: it gives the pinned version, writes the skill again, adds a line to
# whatever FAKE_WRITES names in the call that FAKE_WHEN names, `update` unless it names
# another, and fails validation with its own code, so that a run that gets past the
# comparison of the skills ends there, where a test can tell it from a failed comparison.
FAKE_CLI = """#!/usr/bin/env bash
write() {
  if [ -n "${FAKE_WRITES:-}" ] && [ "${FAKE_WHEN:-update}" = "$1" ]; then
    mkdir -p "$(dirname "$FAKE_WRITES")"
    printf 'written by the CLI\\n' >> "$FAKE_WRITES"
  fi
}
case "$1" in
  --version) write version; echo 9.9.9 ;;
  config) write config ;;
  update)
    printf '%s\\n' "${FAKE_SKILL:-generated}" > .claude/skills/openspec-explore/SKILL.md
    write update
    ;;
  validate) write validate; exit 7 ;;
  *) exit 9 ;;
esac
"""
PAST_THE_COMPARISONS = 7
CHANGED = "files outside the generated skills changed during the run"


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
    assert CHANGED in done.stderr
    assert shown in done.stderr


@pytest.mark.parametrize("when", ["version", "config", "validate"])
def test_a_file_that_the_cli_writes_in_any_of_its_calls_fails(repo: Path, when: str) -> None:
    done = run(repo, FAKE_WRITES="AGENTS.md", FAKE_WHEN=when)
    assert done.returncode == 1, done.stderr
    assert CHANGED in done.stderr
    assert "+ ?? AGENTS.md" in done.stderr


def test_the_message_names_another_process_as_a_possible_writer(repo: Path) -> None:
    done = run(repo, FAKE_WRITES="AGENTS.md")
    assert "by the pinned CLI or by another process running beside it" in done.stderr


def test_a_file_that_the_cli_rewrites_after_a_person_changed_it_fails(repo: Path) -> None:
    (repo / "README.md").write_text("A readme, being edited.\n", encoding="utf-8")
    done = run(repo, FAKE_WRITES="README.md")
    assert done.returncode == 1
    assert "-  M README.md " in done.stderr
    assert "+  M README.md " in done.stderr


def test_a_rename_that_only_the_working_tree_holds_is_shown_with_its_old_name(
    repo: Path,
) -> None:
    lines = "".join(f"Line {number} of a guide.\n" for number in range(20))
    (repo / "guide.md").write_text(lines, encoding="utf-8")
    for args in (["add", "--", "guide.md"], ["commit", "-q", "-m", "Guide"]):
        subprocess.run(["git", *args], cwd=repo, check=True, env=environment())
    (repo / "guide.md").rename(repo / "moved.md")
    subprocess.run(["git", "add", "-N", "--", "moved.md"], cwd=repo, check=True, env=environment())
    done = run(repo, FAKE_WRITES="moved.md")
    assert done.returncode == 1
    assert "+  R moved.md from guide.md " in done.stderr


def test_a_working_tree_that_cannot_be_read_stops_the_run_before_a_skill_is_emptied(
    repo: Path, tmp_path: Path
) -> None:
    real = shutil.which("git")
    assert real
    wrapper = tmp_path / "bin" / "git"
    wrapper.parent.mkdir()
    wrapper.write_text(
        f'#!/usr/bin/env bash\n[ "$1" = status ] && exit 128\nexec "{real}" "$@"\n',
        encoding="utf-8",
    )
    wrapper.chmod(wrapper.stat().st_mode | stat.S_IXUSR)
    done = run(repo, PATH=f"{wrapper.parent}{os.pathsep}{os.environ['PATH']}")
    assert done.returncode == 2, done.stderr
    assert "cannot read the working tree" in done.stderr
    assert (repo / SKILL).read_text(encoding="utf-8") == "generated\n"


def test_skills_that_differ_from_what_git_holds_still_fail(repo: Path) -> None:
    done = run(repo, FAKE_SKILL="another text")
    assert done.returncode == 1
    assert "the generated skills differ from what the pinned CLI writes" in done.stderr
    assert SKILL in done.stderr


@pytest.mark.parametrize("refresh", [None, "false"], ids=["by default", "with no refresh"])
def test_a_skill_that_differs_from_git_s_record_only_in_its_size_on_disk_passes(
    repo: Path, refresh: str | None
) -> None:
    """A clone that checked the skills out with Windows line endings before the attributes
    keeps them so, and git's index records the size of each such copy, so that once the CLI
    writes a skill again with line feeds, `git status` takes it for changed without reading
    it, though git would commit it unchanged. The skills are compared by content, whatever
    the clone's `diff.autoRefreshIndex` says (R276)."""
    (repo / ".gitattributes").write_text("* text=auto eol=lf\n", encoding="utf-8")
    for args in (["add", "--", ".gitattributes"], ["commit", "-q", "-m", "Attributes"]):
        subprocess.run(["git", *args], cwd=repo, check=True, env=environment())
    if refresh is not None:
        setting = ["git", "config", "diff.autoRefreshIndex", refresh]
        subprocess.run(setting, cwd=repo, check=True, env=environment())
    (repo / SKILL).write_bytes(b"generated\r\n")
    subprocess.run(["git", "update-index", "--", SKILL], cwd=repo, check=True, env=environment())
    status = ["git", "status", "--porcelain", "--", SKILL]
    assert subprocess.run(status, cwd=repo, capture_output=True, env=environment()).stdout == b""
    done = run(repo)
    assert done.returncode == PAST_THE_COMPARISONS, done.stderr
    assert (repo / SKILL).read_bytes() == b"generated\n"
    assert subprocess.run(status, cwd=repo, capture_output=True, env=environment()).stdout


def test_a_replace_ref_hides_no_change_to_a_skill(repo: Path) -> None:
    """Git reads a replace ref's object in place of the one that it replaces, so a ref that
    gave the skill's object what the CLI writes would hide a change: the comparison reads
    git's own objects (R276)."""

    def git(*args: str, stdin: bytes = b"") -> str:
        done = subprocess.run(
            ["git", *args], cwd=repo, input=stdin, capture_output=True, env=environment()
        )
        assert done.returncode == 0, done.stderr
        return done.stdout.decode("ascii").strip()

    git(
        "replace",
        git("rev-parse", f":{SKILL}"),
        git("hash-object", "-w", "--stdin", stdin=b"another text\n"),
    )
    done = run(repo, FAKE_SKILL="another text")
    assert done.returncode == 1, done.stderr
    assert "the generated skills differ from what the pinned CLI writes" in done.stderr
    assert f"M\t{SKILL}" in done.stderr


@pytest.mark.parametrize(
    ("written", "shown"),
    [
        (".claude/skills/openspec-explore/extra.md", "?? .claude/skills/openspec-explore/extra.md"),
        (
            ".claude/skills/openspec-explore/CLAUDE.local.md",
            "!! .claude/skills/openspec-explore/CLAUDE.local.md",
        ),
    ],
)
def test_a_file_that_git_does_not_track_or_ignores_among_the_skills_fails(
    repo: Path, written: str, shown: str
) -> None:
    done = run(repo, FAKE_WRITES=written)
    assert done.returncode == 1, done.stderr
    assert "the generated skills differ from what the pinned CLI writes" in done.stderr
    assert shown in done.stderr


def test_a_tracked_file_of_a_skill_that_the_cli_no_longer_writes_fails(repo: Path) -> None:
    kept = ".claude/skills/openspec-explore/references/kept.md"
    (repo / kept).parent.mkdir(parents=True)
    (repo / kept).write_text("Kept.\n", encoding="utf-8")
    for args in (["add", "--", kept], ["commit", "-q", "-m", "Kept"]):
        subprocess.run(["git", *args], cwd=repo, check=True, env=environment())
    done = run(repo)
    assert done.returncode == 1, done.stderr
    assert f"D\t{kept}" in done.stderr
