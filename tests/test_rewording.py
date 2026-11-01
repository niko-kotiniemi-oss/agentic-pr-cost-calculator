"""The rewording script lists every change that is more than a word to avoid replaced.

`scripts/rewording.py` compares HEAD with where it left the default branch, in the
Markdown files that the wording test reads, and prints, for the pull request, each line
that changed by more than the glossary's words to avoid replaced with their terms,
`CLAUDE.md`'s first, each file added or removed, and how many lines only replaced a
word, by word (task 1.20; design decision 14). It reads a page as the wording test does,
so a word inside code or in a title that an accepted record quotes is never taken for a
replacement, and a change to it is always listed (T90, T94).
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

import pytest
from rewording import main

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "rewording.py"
GLOSSARY = "docs/glossary.md"
GIT_ENVIRONMENT = {
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.invalid",
}
GLOSSARY_TEXT = (
    "# Glossary\n"
    "\n"
    "## The tool\n"
    "\n"
    "| Term | Meaning | Words to avoid |\n"
    "|---|---|---|\n"
    "| the tool | What this repository builds. | the calculator |\n"
    "| capture step | The code that records calls. | capture hook |\n"
    "| bill of materials | What a release lists. | SBOM |\n"
    "| git common directory | The directory that worktrees share. | git directory |\n"
)
TITLE = "The calculator says so"
BEFORE = {
    "CLAUDE.md": "# Rules\n\nRules for the calculator.\n",
    "docs/page.md": "The calculator counts calls.\nA capture hook runs.\n",
    "openspec/changes/demo/specs/thing/spec.md": f"#### Scenario: {TITLE}\n",
    "docs/decisions/DR-001-a-choice.md": f'- **Status:** accepted\n\nIt holds "{TITLE}".\n',
    "docs/threat-model.md": f'- **Held by:** `thing`: "{TITLE}"\n',
}
NOTHING_LISTED = "## Changed by more than a word to avoid\n\nNone.\n"


@pytest.fixture(autouse=True)
def isolated_git(monkeypatch: pytest.MonkeyPatch) -> None:
    for name, value in GIT_ENVIRONMENT.items():
        monkeypatch.setenv(name, value)


def git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
    return done.stdout.decode().strip()


def write(root: Path, files: Mapping[str, str | None]) -> None:
    for path, text in files.items():
        target = root / path
        if text is None:
            target.unlink()
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


def history(
    root: Path, after: Mapping[str, str | None], before: Mapping[str, str | None] | None = None
) -> str:
    """A repository whose `main` holds `before`, fetched as `origin/main`, and a branch
    checked out that changes it to `after` in one commit, None removing a file. Returns
    where the branch left `main`, as the script abbreviates it."""
    write(root, BEFORE if before is None else before)
    git(root, "init", "-q", "-b", "main")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "Before")
    git(root, "update-ref", "refs/remotes/origin/main", "main")
    git(root, "checkout", "-q", "-b", "work")
    write(root, after)
    git(root, "add", "-A")
    git(root, "commit", "-q", "--allow-empty", "-m", "After")
    return git(root, "rev-parse", "main")[:12]


def rewording(
    root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], *args: str
) -> tuple[int, str, str]:
    monkeypatch.chdir(root)
    code = main(list(args))
    out, err = capsys.readouterr()
    return code, out, err


def test_a_line_that_only_replaces_a_word_to_avoid_is_counted_and_not_listed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    after = {
        GLOSSARY: GLOSSARY_TEXT,
        "docs/page.md": "The tool counts calls.\nA capture step runs.\n",
    }
    since = history(tmp_path, after)
    assert rewording(tmp_path, monkeypatch, capsys) == (
        0,
        f"Compared with `refs/remotes/origin/main` at `{since}`, where HEAD left it, in the"
        " Markdown files that the wording test reads.\n"
        "\n"
        "## Changed by more than a word to avoid\n"
        "\n"
        "None.\n"
        "\n"
        "## Added or removed\n"
        "\n"
        "- Added: `docs/glossary.md`\n"
        "\n"
        "## Only a word to avoid replaced\n"
        "\n"
        "2 lines in 1 file changed only by a word to avoid replaced with its term:\n"
        "\n"
        "| Word to avoid | Term | Replaced |\n"
        "|---|---|---|\n"
        "| the calculator | the tool | 1 |\n"
        "| capture hook | capture step | 1 |\n",
        "",
    )


def test_a_line_that_also_changes_another_word_is_listed_with_both(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    page = "The tool counts every call.\nA capture step runs.\n"
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": page})
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert (
        "## Changed by more than a word to avoid\n"
        "\n"
        "### `docs/page.md`\n"
        "\n"
        "Line 1:\n"
        "\n"
        "```diff\n"
        "- The calculator counts calls.\n"
        "+ The tool counts every call.\n"
        "```\n"
        "\n"
        "## Added or removed\n"
    ) in out
    assert "1 line in 1 file changed only by a word to avoid" in out
    assert "| capture hook | capture step | 1 |" in out
    assert "| the calculator |" not in out


def test_a_long_line_shows_each_change_with_a_few_words_around_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    words = " ".join(f"w{each}" for each in range(30))
    before = {"docs/page.md": f"The calculator {words} ends.\n"}
    after = {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": f"The tool {words} stops.\n"}
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert (
        "Line 1:\n"
        "\n"
        "```diff\n"
        "- The calculator w0 w1 w2 w3 …\n"
        "+ The tool w0 w1 w2 w3 …\n"
        "- … w26 w27 w28 w29 ends.\n"
        "+ … w26 w27 w28 w29 stops.\n"
        "```\n"
    ) in out


def test_a_change_of_spaces_alone_is_shown_with_as_many_words_around_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    words = [f"w{each}" for each in range(30)]
    spaced = " ".join(words[:15]) + "  " + " ".join(words[15:])
    before = {"docs/page.md": spaced + "\n"}
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": " ".join(words) + "\n"}, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert (
        "```diff\n"
        "- … w11 w12 w13 w14  w15 w16 w17 w18 …\n"
        "+ … w11 w12 w13 w14 w15 w16 w17 w18 …\n"
        "```\n"
    ) in out


def test_a_raised_first_letter_a_plural_and_a_word_to_avoid_in_another_case_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {
        "docs/page.md": (
            "The calculator's code.\n"
            "Two capture hooks and git directories.\n"
            "The SBOM and the calculator.\n"
            "Its sbom.\n"
        )
    }
    page = "The tool's code.\nTwo capture steps and git common directories.\n"
    page += "The bill of materials and the tool.\nIts bill of materials.\n"
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": page}, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert NOTHING_LISTED in out
    assert (
        "4 lines in 1 file changed only by a word to avoid replaced with its term:\n"
        "\n"
        "| Word to avoid | Term | Replaced |\n"
        "|---|---|---|\n"
        "| the calculator | the tool | 2 |\n"
        "| capture hook | capture step | 1 |\n"
        "| SBOM | bill of materials | 2 |\n"
        "| git directory | git common directory | 1 |\n"
    ) in out


def test_lines_that_only_replace_a_word_are_counted_by_the_files_that_hold_them(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {
        **BEFORE,
        "docs/other.md": "About the calculator.\n",
        "docs/third.md": "A page.\n",
    }
    after = {
        GLOSSARY: GLOSSARY_TEXT,
        "docs/page.md": "The tool counts calls.\nA capture step runs.\n",
        "docs/other.md": "About the tool.\n",
        "docs/third.md": "Another page.\n",
    }
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert "\n3 lines in 2 files changed only by a word to avoid" in out
    assert "### `docs/third.md`" in out


@pytest.mark.parametrize(
    "page",
    [
        "the Tool counts calls.\nA capture step runs.\n",
        "The calculator counts calls.\nA capture steps runs.\n",
        "The tool  counts calls.\nA capture step runs.\n",
    ],
)
def test_a_replacement_in_another_form_is_listed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    page: str,
) -> None:
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": page})
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert "### `docs/page.md`" in out


def test_claude_md_s_changes_come_before_every_other_file_s(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {
        "CLAUDE.md": "Rules for the calculator.\n",
        ".github/pull_request_template.md": "Describe the calculator's change.\n",
        "AAA.md": "About the calculator.\n",
    }
    after = {
        GLOSSARY: GLOSSARY_TEXT,
        "CLAUDE.md": "Rules for the tool, always.\n",
        ".github/pull_request_template.md": "Describe the change to the tool.\n",
        "AAA.md": "All about the tool.\n",
    }
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    headings = [line for line in out.split("\n") if line.startswith("### ")]
    assert headings == [
        "### `CLAUDE.md`",
        "### `.github/pull_request_template.md`",
        "### `AAA.md`",
    ]


def test_a_hunk_whose_removed_and_added_lines_differ_in_number_is_listed_whole(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    page = "The tool counts calls.\nIt has one more line.\nA capture step runs.\n"
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": page})
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert (
        "### `docs/page.md`\n"
        "\n"
        "Lines 1 to 3, in place of lines 1 to 2:\n"
        "\n"
        "```diff\n"
        "- The calculator counts calls.\n"
        "- A capture hook runs.\n"
        "+ The tool counts calls.\n"
        "+ It has one more line.\n"
        "+ A capture step runs.\n"
        "```\n"
    ) in out
    assert "## Only a word to avoid replaced\n\nNone.\n" in out


def test_lines_added_and_removed_alone_are_listed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    page = "The calculator counts calls.\nA new line.\n"
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": page})
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert "Line 2:\n\n```diff\n- A capture hook runs.\n+ A new line.\n```" in out
    history_root = tmp_path / "other"
    history_root.mkdir()
    history(history_root, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": "A capture hook runs.\n"})
    _, out, _ = rewording(history_root, monkeypatch, capsys)
    assert "Line 1 of the base, removed:\n\n```diff\n- The calculator counts calls.\n```" in out
    history_root = tmp_path / "third"
    history_root.mkdir()
    page = "The calculator counts calls.\nA capture hook runs.\nAnd one more.\n"
    history(history_root, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": page})
    _, out, _ = rewording(history_root, monkeypatch, capsys)
    assert "Line 3, added:\n\n```diff\n+ And one more.\n```" in out


def test_an_added_and_a_removed_file_are_listed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    after = {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": None, "docs/new.md": "A new page.\n"}
    history(tmp_path, after)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert (
        "## Added or removed\n"
        "\n"
        "- Added: `docs/glossary.md`\n"
        "- Added: `docs/new.md`\n"
        "- Removed: `docs/page.md`\n"
    ) in out


def test_a_file_that_keeps_its_words_is_never_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    kept = [
        "docs/decisions/DR-001-a-choice.md",
        "docs/decisions/README.md",
        "openspec/changes/archive/2026-01-01-old/proposal.md",
        "vendor/superpowers/README.md",
        ".claude/skills/openspec-propose/SKILL.md",
    ]
    before: dict[str, str | None] = {**BEFORE, **{path: "The calculator.\n" for path in kept}}
    after: dict[str, str | None] = {GLOSSARY: GLOSSARY_TEXT}
    after |= {path: "Something else, about the tool.\n" for path in kept[1:]}
    after[kept[0]] = BEFORE[kept[0]] + "Changed.\n"
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert NOTHING_LISTED in out
    assert not [path for path in kept if path in out]


def test_a_word_in_code_or_in_a_quoted_title_is_never_taken_for_a_replacement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before: dict[str, str | None] = {
        **BEFORE,
        "docs/page.md": "Set `the calculator` here.\n\n```text\nthe calculator\n```\n",
    }
    after = {
        GLOSSARY: GLOSSARY_TEXT,
        "docs/page.md": "Set `the tool` here.\n\n```text\nthe tool\n```\n",
        "docs/threat-model.md": BEFORE["docs/threat-model.md"].replace("calculator", "tool"),
    }
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert (
        "### `docs/page.md`\n"
        "\n"
        "Line 1:\n"
        "\n"
        "```diff\n"
        "- Set `the calculator` here.\n"
        "+ Set `the tool` here.\n"
        "```\n"
        "\n"
        "Line 4:\n"
        "\n"
        "```diff\n"
        "- the calculator\n"
        "+ the tool\n"
        "```\n"
        "\n"
        "### `docs/threat-model.md`\n"
        "\n"
        "Line 1:\n"
    ) in out
    assert "## Only a word to avoid replaced\n\nNone.\n" in out


def test_a_title_that_the_base_keeps_is_listed_when_the_branch_renames_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    spec = "openspec/changes/demo/specs/thing/spec.md"
    after = {GLOSSARY: GLOSSARY_TEXT, spec: BEFORE[spec].replace("calculator", "tool")}
    history(tmp_path, after)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert f"### `{spec}`" in out
    assert "## Only a word to avoid replaced\n\nNone.\n" in out


def test_every_markdown_file_is_compared_from_any_folder_of_the_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {
        **BEFORE,
        "NOTES.MARKDOWN": "The calculator.\n",
        "other/README.MD": "The calculator.\n",
    }
    after = {
        GLOSSARY: GLOSSARY_TEXT,
        "NOTES.MARKDOWN": "All about the tool.\n",
        "other/README.MD": "The tool.\n",
        "docs/threat-model.md": BEFORE["docs/threat-model.md"].replace("calculator", "tool"),
    }
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path / "docs", monkeypatch, capsys)
    headings = [line for line in out.split("\n") if line.startswith("### ")]
    assert headings == ["### `NOTES.MARKDOWN`", "### `docs/threat-model.md`"]
    assert "\n1 line in 1 file changed only by a word to avoid" in out


def test_a_word_to_avoid_added_to_the_glossary_is_listed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before: dict[str, str | None] = {**BEFORE, GLOSSARY: GLOSSARY_TEXT}
    glossary = GLOSSARY_TEXT.replace("| capture hook |", "| capture hook, hook script |")
    history(tmp_path, {GLOSSARY: glossary}, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert (
        "### `docs/glossary.md`\n"
        "\n"
        "Line 8:\n"
        "\n"
        "```diff\n"
        "- … records calls. | capture hook |\n"
        "+ … records calls. | capture hook, hook script |\n"
        "```\n"
    ) in out
    assert "## Added or removed\n\nNone.\n" in out


def test_a_fence_in_the_output_is_longer_than_any_backticks_it_holds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {"docs/page.md": "Write ```` here.\n"}
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": "Write ````` here.\n"}, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert "``````diff\n- Write ```` here.\n+ Write ````` here.\n``````\n" in out


def test_only_what_the_branch_changed_is_compared(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    since = history(tmp_path, {GLOSSARY: GLOSSARY_TEXT})
    git(tmp_path, "checkout", "-q", "main")
    write(tmp_path, {"docs/later.md": "A page that the default branch gained later.\n"})
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "Later")
    git(tmp_path, "update-ref", "refs/remotes/origin/main", "main")
    git(tmp_path, "checkout", "-q", "work")
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert f"at `{since}`, where HEAD left it" in out
    assert "docs/later.md" not in out
    later = git(tmp_path, "rev-parse", "main")
    code, out, _ = rewording(tmp_path, monkeypatch, capsys, later)
    assert code == 0 and f"Compared with `{later}` at `{since}`" in out


@pytest.mark.parametrize(
    ("after", "args", "message"),
    [
        ({}, (), f"rewording: HEAD holds no {GLOSSARY}"),
        (
            {
                GLOSSARY: GLOSSARY_TEXT.replace("| the calculator |", "| |")
                .replace("| capture hook |", "| |")
                .replace("| SBOM |", "| |")
                .replace("| git directory |", "| |")
            },
            (),
            f"rewording: {GLOSSARY} at HEAD gives no word to avoid",
        ),
        (
            {GLOSSARY: GLOSSARY_TEXT},
            ("no-such-branch",),
            "rewording: no-such-branch is not a commit",
        ),
        (
            {GLOSSARY: GLOSSARY_TEXT},
            ("HEAD:CLAUDE.md",),
            "rewording: HEAD:CLAUDE.md is not a commit",
        ),
        ({GLOSSARY: GLOSSARY_TEXT}, ("main..work",), "rewording: main..work is not a commit"),
        ({GLOSSARY: GLOSSARY_TEXT}, ("main", "work"), "usage: python3 scripts/rewording.py [BASE]"),
    ],
)
def test_what_cannot_be_compared_exits_2(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    after: dict[str, str | None],
    args: tuple[str, ...],
    message: str,
) -> None:
    history(tmp_path, after)
    assert rewording(tmp_path, monkeypatch, capsys, *args) == (2, "", message + "\n")


def test_a_base_that_shares_no_history_with_head_exits_2(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT})
    git(tmp_path, "checkout", "-q", "--orphan", "unrelated")
    git(tmp_path, "commit", "-q", "-m", "Unrelated")
    git(tmp_path, "checkout", "-q", "work")
    assert rewording(tmp_path, monkeypatch, capsys, "unrelated") == (
        2,
        "",
        "rewording: HEAD shares no history with unrelated\n",
    )


def test_a_git_command_that_fails_where_it_should_not_exits_2_with_git_s_words(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": "The tool counts calls.\n"})
    changed = git(tmp_path, "rev-parse", "HEAD:docs/page.md")
    (tmp_path / ".git" / "objects" / changed[:2] / changed[2:]).unlink()
    code, out, err = rewording(tmp_path, monkeypatch, capsys)
    assert (code, out) == (2, "")
    assert err.startswith("rewording: ") and err.strip() != "rewording:"


def test_the_script_runs_as_a_command(tmp_path: Path) -> None:
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": "The tool counts calls.\n"})
    done = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=tmp_path, capture_output=True, text=True, check=False
    )
    assert (done.returncode, done.stderr) == (0, "")
    assert done.stdout.startswith("Compared with `refs/remotes/origin/main` at ")
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "no-such-branch"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert (done.returncode, done.stdout) == (2, "")
