"""The rewording script lists every change that is more than a word to avoid replaced.

`scripts/rewording.py` compares HEAD with where it left the default branch, in the
Markdown files that the wording test reads, and prints, for the pull request, both
commits by their full hashes; each line that changed by more than the glossary's words
to avoid replaced with their terms, `CLAUDE.md`'s first; apart from those, each line
that only replaced a word that the base's glossary did not give for its term; each file
added, removed or renamed; each changed file that it did not compare; and how many lines
only replaced a word, by word (task 1.20; design decision 14). A renamed page is
compared with what it was. It reads a page as the wording test does, so a word inside
code or in a title that an accepted record quotes is never taken for a replacement, and
a change to it is always listed (T90, T94). A path, and each word to avoid and term
in the table, is written as a code span that nothing in it can close, and the script
refuses a glossary out of its form, in which no term holds a backslash, so that no
file's name and no row of the glossary writes the output's prose.
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

import pytest
from rewording import main
from wording import GLOSSARY

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "rewording.py"
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
    GLOSSARY: GLOSSARY_TEXT,
    "CLAUDE.md": "# Rules\n\nRules for the calculator.\n",
    "docs/page.md": "The calculator counts calls.\nA capture hook runs.\n",
    "openspec/changes/demo/specs/thing/spec.md": f"#### Scenario: {TITLE}\n",
    "docs/decisions/DR-001-a-choice.md": f'- **Status:** accepted\n\nIt holds "{TITLE}".\n',
    "docs/threat-model.md": f'- **Held by:** `thing`: "{TITLE}"\n',
}
NOTHING_LISTED = "## Changed by more than a word to avoid\n\nNone.\n"
NOTHING_NEW = "## Only a word to avoid new to the glossary replaced\n\nNone.\n"
NOTHING_REPLACED = "## Only a word to avoid replaced\n\nNone.\n"
TABLE = "| Word to avoid | Term | Replaced | New to the glossary |\n|---|---|---|---|\n"


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
    where the branch left `main`."""
    write(root, BEFORE if before is None else before)
    git(root, "init", "-q", "-b", "main")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "Before")
    git(root, "update-ref", "refs/remotes/origin/main", "main")
    git(root, "checkout", "-q", "-b", "work")
    write(root, after)
    git(root, "add", "-A")
    git(root, "commit", "-q", "--allow-empty", "-m", "After")
    return git(root, "rev-parse", "main")


def rewording(
    root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], *args: str
) -> tuple[int, str, str]:
    monkeypatch.chdir(root)
    code = main(list(args))
    out, err = capsys.readouterr()
    return code, out, err


def section(out: str, title: str) -> str:
    """What the output gives under one of its headings, up to the next."""
    start = out.index(f"\n## {title}\n\n") + len(title) + 6
    end = out.find("\n## ", start)
    return out[start : None if end == -1 else end]


def test_a_line_that_only_replaces_a_word_to_avoid_is_counted_and_not_listed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    since = history(tmp_path, {"docs/page.md": "The tool counts calls.\nA capture step runs.\n"})
    head = git(tmp_path, "rev-parse", "HEAD")
    assert rewording(tmp_path, monkeypatch, capsys) == (
        0,
        f"Compared HEAD at `{head}` with `{since}`, where it left"
        " `refs/remotes/origin/main`, in the Markdown files that the wording test reads.\n"
        "\n"
        "## Changed by more than a word to avoid\n"
        "\n"
        "None.\n"
        "\n"
        "## Only a word to avoid new to the glossary replaced\n"
        "\n"
        "None.\n"
        "\n"
        "## Added, removed or renamed\n"
        "\n"
        "None.\n"
        "\n"
        "## Not compared\n"
        "\n"
        "None.\n"
        "\n"
        "## Only a word to avoid replaced\n"
        "\n"
        "2 lines in 1 file changed only by a word to avoid replaced with its term:\n"
        "\n"
        f"{TABLE}"
        "| `the calculator` | `the tool` | 1 | no |\n"
        "| `capture hook` | `capture step` | 1 | no |\n",
        "",
    )


def test_a_line_that_replaces_a_word_the_base_s_glossary_did_not_list_is_listed_apart(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {path: text for path, text in BEFORE.items() if path != GLOSSARY}
    page = "The tool counts calls.\nA capture hook runs.\n"
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": page}, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert section(out, "Only a word to avoid new to the glossary replaced") == (
        "### `docs/page.md`\n"
        "\n"
        "Line 1:\n"
        "\n"
        "```diff\n"
        "- The calculator counts calls.\n"
        "+ The tool counts calls.\n"
        "```\n"
    )
    assert NOTHING_LISTED in out
    assert f"{TABLE}| `the calculator` | `the tool` | 1 | yes |\n" in out


@pytest.mark.parametrize(
    ("glossary", "old", "new", "row"),
    [
        (
            GLOSSARY_TEXT + "| sometimes | Now and then. | never |\n",
            "Never merge a pull request.",
            "Sometimes merge a pull request.",
            "| `never` | `sometimes` | 1 | yes |",
        ),
        (
            GLOSSARY_TEXT.replace("| the tool |", "| the program |"),
            "The calculator counts calls.",
            "The program counts calls.",
            "| `the calculator` | `the program` | 1 | yes |",
        ),
    ],
    ids=["a new word to avoid", "a word to avoid given for a new term"],
)
def test_a_rule_that_the_pull_request_adds_is_listed_where_it_replaces_a_word(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    glossary: str,
    old: str,
    new: str,
    row: str,
) -> None:
    history(
        tmp_path, {GLOSSARY: glossary, "CLAUDE.md": new + "\n"}, {**BEFORE, "CLAUDE.md": old + "\n"}
    )
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert section(out, "Only a word to avoid new to the glossary replaced") == (
        f"### `CLAUDE.md`\n\nLine 1:\n\n```diff\n- {old}\n+ {new}\n```\n"
    )
    assert f"\n{row}\n" in out
    assert "### `docs/glossary.md`" in section(out, "Changed by more than a word to avoid")


def test_a_line_that_also_changes_another_word_is_listed_with_both(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    page = "The tool counts every call.\nA capture step runs.\n"
    history(tmp_path, {"docs/page.md": page})
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert section(out, "Changed by more than a word to avoid") == (
        "### `docs/page.md`\n"
        "\n"
        "Line 1:\n"
        "\n"
        "```diff\n"
        "- The calculator counts calls.\n"
        "+ The tool counts every call.\n"
        "```\n"
    )
    assert "1 line in 1 file changed only by a word to avoid" in out
    assert "| `capture hook` | `capture step` | 1 |" in out
    assert "| `the calculator` |" not in out


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


def test_a_word_to_avoid_that_the_base_gave_in_another_case_is_not_new(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {**BEFORE, GLOSSARY: GLOSSARY_TEXT.replace("| SBOM |", "| sbom |")}
    before["docs/page.md"] = "The SBOM lists them.\n"
    history(
        tmp_path,
        {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": "The bill of materials lists them.\n"},
        before,
    )
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert NOTHING_NEW in out
    assert "| `SBOM` | `bill of materials` | 1 | no |" in out


def test_a_raised_first_letter_a_plural_and_a_word_to_avoid_in_another_case_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {
        GLOSSARY: GLOSSARY_TEXT,
        "docs/page.md": (
            "The calculator's code.\n"
            "Two capture hooks and git directories.\n"
            "The SBOM and the calculator.\n"
            "Its sbom.\n"
        ),
    }
    page = "The tool's code.\nTwo capture steps and git common directories.\n"
    page += "The bill of materials and the tool.\nIts bill of materials.\n"
    history(tmp_path, {"docs/page.md": page}, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert NOTHING_LISTED in out
    assert NOTHING_NEW in out
    assert (
        "4 lines in 1 file changed only by a word to avoid replaced with its term:\n"
        "\n"
        f"{TABLE}"
        "| `the calculator` | `the tool` | 2 | no |\n"
        "| `capture hook` | `capture step` | 1 | no |\n"
        "| `SBOM` | `bill of materials` | 2 | no |\n"
        "| `git directory` | `git common directory` | 1 | no |\n"
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
    history(tmp_path, {"docs/page.md": page})
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert "### `docs/page.md`" in section(out, "Changed by more than a word to avoid")


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
    listed = section(out, "Changed by more than a word to avoid")
    headings = [line for line in listed.split("\n") if line.startswith("### ")]
    assert headings == [
        "### `CLAUDE.md`",
        "### `.github/pull_request_template.md`",
        "### `AAA.md`",
    ]


def test_the_guide_s_changes_come_right_after_claude_md_s(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {
        "CLAUDE.md": "Rules for the calculator.\n",
        "docs/patterns.md": "How the calculator builds.\n",
        "AAA.md": "About the calculator.\n",
        "docs/about.md": "The calculator's page.\n",
    }
    after = {
        GLOSSARY: GLOSSARY_TEXT,
        "CLAUDE.md": "Rules for the tool, always.\n",
        "docs/patterns.md": "How the tool builds, always.\n",
        "AAA.md": "All about the tool.\n",
        "docs/about.md": "The page of the tool.\n",
    }
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    listed = section(out, "Changed by more than a word to avoid")
    headings = [line for line in listed.split("\n") if line.startswith("### ")]
    assert headings == [
        "### `CLAUDE.md`",
        "### `docs/patterns.md`",
        "### `AAA.md`",
        "### `docs/about.md`",
    ]


def test_the_guide_renamed_with_changes_keeps_its_place(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    guide = "".join(f"Line {n} of how the project builds.\n" for n in range(9))
    before = {"CLAUDE.md": "Rules.\n", "docs/patterns.md": guide, "AAA.md": "About it.\n"}
    after = {
        GLOSSARY: GLOSSARY_TEXT,
        "CLAUDE.md": "Rules for the tool, always.\n",
        "docs/patterns.md": None,
        "docs/a-guide.md": guide + "How the tool builds, always.\n",
        "AAA.md": "All about the tool.\n",
    }
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    listed = section(out, "Changed by more than a word to avoid")
    headings = [line for line in listed.split("\n") if line.startswith("### ")]
    assert headings == ["### `CLAUDE.md`", "### `docs/a-guide.md`", "### `AAA.md`"]


def test_a_hunk_whose_removed_and_added_lines_differ_in_number_is_listed_whole(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    page = "The tool counts calls.\nIt has one more line.\nA capture step runs.\n"
    history(tmp_path, {"docs/page.md": page})
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
    assert NOTHING_REPLACED in out


@pytest.mark.parametrize(
    ("page", "expected"),
    [
        (
            "The calculator counts calls.\nA new line.\n",
            "Line 2:\n\n```diff\n- A capture hook runs.\n+ A new line.\n```",
        ),
        (
            "A capture hook runs.\n",
            "Line 1 of the base, removed:\n\n```diff\n- The calculator counts calls.\n```",
        ),
        (
            "The calculator counts calls.\nA capture hook runs.\nAnd one more.\n",
            "Line 3, added:\n\n```diff\n+ And one more.\n```",
        ),
    ],
)
def test_lines_added_and_removed_alone_are_listed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    page: str,
    expected: str,
) -> None:
    history(tmp_path, {"docs/page.md": page})
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert expected in out


def test_an_added_and_a_removed_file_are_listed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": None, "docs/new.md": "A new page.\n"})
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert section(out, "Added, removed or renamed") == (
        "- Added: `docs/new.md`\n"
        "- Removed: `docs/page.md`\n"
        "\n"
        "An added file's lines are not compared, since the base holds none of them.\n"
    )


def test_a_removed_file_alone_says_nothing_of_added_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": None})
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert section(out, "Added, removed or renamed") == "- Removed: `docs/page.md`\n"


RENAMED = "The calculator counts calls.\nIt reads its ledger.\nIt prices each call.\n"


def test_a_renamed_page_is_compared_with_what_it_was(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {**BEFORE, "docs/old.md": RENAMED + "It writes a comment.\nIt stops.\n"}
    after = {
        "docs/old.md": None,
        "docs/new.md": RENAMED.replace("calculator", "tool") + "It writes a comment.\nIt ends.\n",
    }
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert (
        section(out, "Added, removed or renamed") == "- Renamed: `docs/old.md` to `docs/new.md`\n"
    )
    assert section(out, "Changed by more than a word to avoid") == (
        "### `docs/new.md`\n\nLine 5:\n\n```diff\n- It stops.\n+ It ends.\n```\n"
    )
    assert "\n1 line in 1 file changed only by a word to avoid" in out


def test_each_changed_file_that_is_not_compared_is_named(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    record = "docs/decisions/DR-001-a-choice.md"
    archived = "openspec/changes/archive/2026-01-01-demo/page.md"
    after = {
        "docs/page.md": None,
        archived: BEFORE["docs/page.md"],
        record: BEFORE[record] + "Changed.\n",
        ".github/ISSUE_TEMPLATE/bug_report.yml": "name: Something the calculator does\n",
    }
    history(tmp_path, after)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert section(out, "Not compared") == (
        "- `.github/ISSUE_TEMPLATE/bug_report.yml`, which is not a Markdown file\n"
        f"- `{record}`, which keeps its words as written\n"
        f"- `docs/page.md`, renamed to `{archived}`, which keeps its words as written\n"
    )
    assert section(out, "Added, removed or renamed") == "None.\n"


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
    after: dict[str, str | None] = {path: "Something else, about the tool.\n" for path in kept[1:]}
    after[kept[0]] = BEFORE[kept[0]] + "Changed.\n"
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert NOTHING_LISTED in out
    assert NOTHING_REPLACED in out
    assert section(out, "Not compared") == "".join(
        f"- `{path}`, which keeps its words as written\n" for path in sorted(kept)
    )


def test_a_word_in_code_or_in_a_quoted_title_is_never_taken_for_a_replacement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before: dict[str, str | None] = {
        **BEFORE,
        "docs/page.md": "Set `the calculator` here.\n\n```text\nthe calculator\n```\n",
    }
    after = {
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
    assert NOTHING_REPLACED in out


def test_a_title_that_the_base_keeps_is_listed_when_the_branch_renames_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    spec = "openspec/changes/demo/specs/thing/spec.md"
    history(tmp_path, {spec: BEFORE[spec].replace("calculator", "tool")})
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert f"### `{spec}`" in out
    assert NOTHING_REPLACED in out


def test_every_markdown_file_is_compared_from_any_folder_of_the_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {
        **BEFORE,
        "NOTES.MARKDOWN": "The calculator.\n",
        "other/README.MD": "The calculator.\n",
        "docs/page.mkd": "The calculator.\n",
        "other/contents.lr": "The calculator.\n",
    }
    after = {
        "NOTES.MARKDOWN": "All about the tool.\n",
        "other/README.MD": "The tool.\n",
        "docs/page.mkd": "All about the tool.\n",
        "other/contents.lr": "The tool.\n",
        "docs/threat-model.md": BEFORE["docs/threat-model.md"].replace("calculator", "tool"),
    }
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path / "docs", monkeypatch, capsys)
    headings = [line for line in out.split("\n") if line.startswith("### ")]
    assert headings == [
        "### `NOTES.MARKDOWN`",
        "### `docs/page.mkd`",
        "### `docs/threat-model.md`",
    ]
    assert "\n2 lines in 2 files changed only by a word to avoid" in out


def test_a_word_to_avoid_added_to_the_glossary_is_listed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    glossary = GLOSSARY_TEXT.replace("| capture hook |", "| capture hook, hook script |")
    history(tmp_path, {GLOSSARY: glossary})
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
    assert "## Added, removed or renamed\n\nNone.\n" in out


def test_a_fence_in_the_output_is_longer_than_any_backticks_it_holds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = {"docs/page.md": "Write ```` here.\n"}
    history(tmp_path, {GLOSSARY: GLOSSARY_TEXT, "docs/page.md": "Write ````` here.\n"}, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert "``````diff\n- Write ```` here.\n+ Write ````` here.\n``````\n" in out


@pytest.mark.parametrize(
    ("path", "shown"),
    [
        ("docs/x` @someone `y.md", "``docs/x` @someone `y.md``"),
        ("`docs.md", "`` `docs.md ``"),
        ("docs/a\n@someone.md", "`docs/a\\x0a@someone.md`"),
    ],
    ids=["backticks inside it", "a backtick first", "a line break"],
)
def test_a_path_is_written_as_code_that_it_cannot_close(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    path: str,
    shown: str,
) -> None:
    history(
        tmp_path, {path: "The tool counts every call.\n"}, {**BEFORE, path: "The calculator.\n"}
    )
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert section(out, "Changed by more than a word to avoid").startswith(f"### {shown}\n")
    history_root = tmp_path / "added"
    history_root.mkdir()
    history(history_root, {path: "A page.\n"})
    _, out, _ = rewording(history_root, monkeypatch, capsys)
    assert section(out, "Added, removed or renamed").startswith(f"- Added: {shown}\n")


def test_a_term_and_its_word_to_avoid_are_written_as_code_that_they_cannot_close(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    term = "@someone, see [the rules](https://example.invalid/x) `x`"
    before = {**BEFORE, "docs/page.md": "A gadget runs.\n"}
    after = {
        GLOSSARY: GLOSSARY_TEXT + f"| {term} | A row. | gadget |\n",
        "docs/page.md": f"A {term} runs.\n",
    }
    history(tmp_path, after, before)
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert section(out, "Only a word to avoid replaced") == (
        "1 line in 1 file changed only by a word to avoid replaced with its term:\n"
        "\n"
        f"{TABLE}"
        "| `gadget` | `` @someone, see [the rules](https://example.invalid/x) `x` `` | 1 | yes |\n"
    )


def test_a_path_or_a_line_that_is_not_utf_8_is_shown_with_a_replacement_character(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {})
    (tmp_path / os.fsdecode(b"docs/caf\xe9.txt")).write_bytes(b"A file.\n")
    (tmp_path / "docs/page.md").write_bytes(b"The tool caf\xe9 counts.\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "Not UTF-8")
    code, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert code == 0
    assert section(out, "Not compared") == "- `docs/caf\ufffd.txt`, which is not a Markdown file\n"
    assert "+ The tool caf\ufffd counts.\n" in section(out, "Changed by more than a word to avoid")


def test_only_what_the_branch_changed_is_compared(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    since = history(tmp_path, {})
    git(tmp_path, "checkout", "-q", "main")
    write(tmp_path, {"docs/later.md": "A page that the default branch gained later.\n"})
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "Later")
    git(tmp_path, "update-ref", "refs/remotes/origin/main", "main")
    git(tmp_path, "checkout", "-q", "work")
    _, out, _ = rewording(tmp_path, monkeypatch, capsys)
    assert f"with `{since}`, where it left `refs/remotes/origin/main`," in out
    assert "docs/later.md" not in out
    later = git(tmp_path, "rev-parse", "main")
    code, out, _ = rewording(tmp_path, monkeypatch, capsys, later)
    assert code == 0 and f"with `{since}`, where it left `{later}`," in out


@pytest.mark.parametrize(
    ("after", "args", "message"),
    [
        ({GLOSSARY: None}, (), f"rewording: HEAD holds no {GLOSSARY}"),
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
            {GLOSSARY: GLOSSARY_TEXT + "| @someone \\\\| x | A row. | gadget |\n"},
            (),
            f"rewording: {GLOSSARY} at HEAD is not in its form:\n{GLOSSARY}:11: the term"
            ' "@someone \\\\| x" holds a backslash, so a pipe after it could split a table\'s'
            " cell",
        ),
        (
            {},
            ("no-such-branch",),
            "rewording: no-such-branch is not a commit",
        ),
        (
            {},
            ("HEAD:CLAUDE.md",),
            "rewording: HEAD:CLAUDE.md is not a commit",
        ),
        ({}, ("main..work",), "rewording: main..work is not a commit"),
        ({}, ("main", "work"), "usage: python3 scripts/rewording.py [BASE]"),
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
    history(tmp_path, {})
    git(tmp_path, "checkout", "-q", "--orphan", "unrelated")
    git(tmp_path, "commit", "-q", "-m", "Unrelated")
    git(tmp_path, "checkout", "-q", "work")
    assert rewording(tmp_path, monkeypatch, capsys, "unrelated") == (
        2,
        "",
        "rewording: HEAD shares no history with unrelated\n",
    )


@pytest.mark.parametrize(
    "lost", ["HEAD:docs/page.md", "main:openspec/changes/demo/specs/thing/spec.md"]
)
def test_a_git_command_that_fails_where_it_should_not_exits_2_with_git_s_words(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], lost: str
) -> None:
    history(tmp_path, {"docs/page.md": "The tool counts calls.\n"})
    gone = git(tmp_path, "rev-parse", lost)
    (tmp_path / ".git" / "objects" / gone[:2] / gone[2:]).unlink()
    code, out, err = rewording(tmp_path, monkeypatch, capsys)
    assert (code, out) == (2, "")
    assert err.startswith("rewording: ") and err.strip() != "rewording:"


def test_the_script_runs_as_a_command(tmp_path: Path) -> None:
    history(tmp_path, {"docs/page.md": "The tool counts calls.\n"})
    done = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=tmp_path, capture_output=True, text=True, check=False
    )
    assert (done.returncode, done.stderr) == (0, "")
    assert done.stdout.startswith("Compared HEAD at `")
    assert "where it left `refs/remotes/origin/main`," in done.stdout
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "no-such-branch"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert (done.returncode, done.stdout) == (2, "")
