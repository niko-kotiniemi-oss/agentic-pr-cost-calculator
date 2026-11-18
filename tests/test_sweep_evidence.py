"""The sweep's evidence script shows that the sweep of B-022 lost no clause.

`scripts/sweep_evidence.py` compares HEAD with its merge base with the default branch, in
every Markdown file that changed between them outside the specs and the mapping, unit by
unit, and checks that `docs/evidence/B-022-mapping.md` gives each unit that the base
holds and HEAD does not an entry whose every clause has a place that exists at HEAD
(design decision 19; T173, T195, T198, T199). Each test plants one defect in a
repository of its own and sees it reported, or a complete mapping pass.
"""

from __future__ import annotations

import os
import subprocess
from collections.abc import Mapping
from pathlib import Path

import pytest
from sweep_evidence import MAPPING, cited, holds, main, short, units

GIT_ENVIRONMENT = {
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.invalid",
}
REGISTER = (
    "| ID | Kind | Capability | Requirement |\n|---|---|---|---|\n| R12 | x | `ledger` | A |\n"
)
SPEC = (
    "### Requirement: A\n\nIt SHALL.\n\n"
    "#### Scenario: Counts are kept\n\n- **WHEN** a\n- **THEN** b\n"
)
TASKS = "## 1. First\n\n- [ ] 1.37 Sweep\n"
PAGE = (
    "# Page\n"
    "\n"
    "The ledger keeps counts. It never keeps text.\n"
    "\n"
    "- **Answer:** the ledger keeps counts, so text never leaks.\n"
    "\n"
    "| Part | Where |\n"
    "|---|---|\n"
    "| Ledger | `.pr-cost/` |\n"
    "\n"
    "```mermaid\n"
    "flowchart LR\n"
    "  A --> B\n"
    "```\n"
)
BEFORE = {
    "docs/requirements.md": REGISTER,
    "openspec/changes/demo/specs/ledger/spec.md": SPEC,
    "openspec/changes/demo/tasks.md": TASKS,
    "docs/decisions/DR-001-a-choice.md": "# DR-001: A choice\n",
    "docs/page.md": PAGE,
}
OPENING = "# B-022 mapping\n\nThe evidence of the sweep.\n"


def entry(old: str, clauses: list[tuple[str, str]], new: str | None = None) -> str:
    text = f"### Entry\n\nOld:\n\n~~~~text\n{old}\n~~~~\n\n"
    if new is not None:
        text += f"New:\n\n~~~~text\n{new}\n~~~~\n\n"
    for clause, place in clauses:
        text += f"Clause, {place}:\n\n~~~~text\n{clause}\n~~~~\n\n"
    return text


def mapping(*sections: tuple[str, list[str]]) -> str:
    text = OPENING
    for path, entries in sections:
        text += f"\n## `{path}`\n\n" + "".join(entries)
    return text


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
    root: Path, after: Mapping[str, str | None], before: Mapping[str, str] | None = None
) -> None:
    """`main` holds BEFORE and `before`, fetched as `origin/main`; a branch changes it to
    `after`."""
    write(root, {**BEFORE, **(before or {})})
    git(root, "init", "-q", "-b", "main")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "Before")
    git(root, "update-ref", "refs/remotes/origin/main", "main")
    git(root, "checkout", "-q", "-b", "work")
    write(root, after)
    git(root, "add", "-A")
    git(root, "commit", "-q", "--allow-empty", "-m", "After")


def run(
    root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], *args: str
) -> tuple[int, str]:
    monkeypatch.chdir(root)
    code = main(list(args))
    out, err = capsys.readouterr()
    return code, out + err


SWEPT = PAGE.replace(
    "The ledger keeps counts. It never keeps text.\n",
    "It never keeps text (R12).\n",
).replace(
    "- **Answer:** the ledger keeps counts, so text never leaks.\n",
    "- **Answer:** so text never leaks (R12).\n",
)
COMPLETE = mapping(
    (
        "docs/page.md",
        [
            entry("The ledger keeps counts.", [("The ledger keeps counts.", "R12")]),
            entry(
                "It never keeps text.",
                [("It never keeps text", "the new unit")],
                new="It never keeps text (R12).",
            ),
            entry(
                "- **Answer:** the ledger keeps counts, so text never leaks.",
                [
                    ("- **Answer:**", "the new unit"),
                    ("the ledger keeps counts,", '`ledger`: "Counts are kept"'),
                    ("so text never leaks", "the new unit"),
                ],
                new="- **Answer:** so text never leaks (R12).",
            ),
        ],
    )
)


def test_a_mapping_that_places_every_clause_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out
    base = git(tmp_path, "rev-parse", "main")
    head = git(tmp_path, "rev-parse", "HEAD")
    assert f"`{base}`" in out and f"`{head}`" in out
    assert "| `docs/page.md` | 8 | 7 | 3 |" in out
    assert out.rstrip().endswith("No problems.")


def test_a_removed_unit_without_an_entry_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = COMPLETE.replace(
        entry("The ledger keeps counts.", [("The ledger keeps counts.", "R12")]), ""
    )
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: missing})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert (
        "`docs/page.md`: no entry for a unit that HEAD does not hold: The ledger keeps counts."
        in out
    )


@pytest.mark.parametrize(
    ("place", "problem"),
    [
        ("R99", "R99 is not in the register at HEAD"),
        ('`ledger`: "No such scenario"', 'no spec at HEAD holds `ledger`: "No such scenario"'),
        ("DR-099", "DR-099 is not a record at HEAD"),
        ("task 9.9", "task 9.9 is in no change's tasks at HEAD"),
        ("somewhere", "somewhere is not a place"),
    ],
)
def test_a_place_that_resolves_to_nothing_is_reported(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    place: str,
    problem: str,
) -> None:
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: COMPLETE.replace("Clause, R12:", f"Clause, {place}:")},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert problem in out


def test_places_that_resolve_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    for place in ("DR-001", "task 1.37", "the page"):
        text = COMPLETE.replace("Clause, R12:", f"Clause, {place}:")
        history_root = tmp_path / place.replace(" ", "-")
        history_root.mkdir()
        after = {
            "docs/page.md": SWEPT
            + ("\n- Note: The ledger keeps counts. More.\n" if place == "the page" else ""),
            MAPPING: text,
        }
        history(history_root, after)
        code, out = run(history_root, monkeypatch, capsys)
        assert code == 0, (place, out)


def test_a_clause_that_the_page_does_not_hold_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: COMPLETE.replace("Clause, R12:", "Clause, the page:")},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`docs/page.md`: HEAD's page does not hold the clause: The ledger keeps counts." in out


def test_a_clause_that_the_page_holds_only_inside_a_longer_word_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    inside = COMPLETE.replace(
        "Clause, R12:\n\n~~~~text\nThe ledger keeps counts.\n~~~~\n",
        "Clause, R12:\n\n~~~~text\nThe ledger\n~~~~\n\n"
        "Clause, the page:\n\n~~~~text\nkeep\n~~~~\n\n"
        "Clause, R12:\n\n~~~~text\ns counts.\n~~~~\n",
    )
    assert inside != COMPLETE
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: inside})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`docs/page.md`: HEAD's page does not hold the clause: keep" in out


def test_a_clause_that_the_new_unit_holds_only_inside_a_longer_word_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    inside = COMPLETE.replace(
        "Clause, the new unit:\n\n~~~~text\nIt never keeps text\n~~~~\n",
        "Clause, the new unit:\n\n~~~~text\nIt never keeps tex\n~~~~\n\n"
        "Clause, the new unit:\n\n~~~~text\nt\n~~~~\n",
    )
    assert inside != COMPLETE
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: inside})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`docs/page.md`: the new unit does not hold the clause: It never keeps tex\n" in out
    assert "`docs/page.md`: the new unit does not hold the clause: t\n" in out


@pytest.mark.parametrize(
    ("text", "clause", "held"),
    [
        ("It keeps counts.", "keeps", True),
        ("It keeps counts.", "keep", False),
        ("It keeps counts.", "eeps", False),
        ("It keeps counts, so text", ", so", True),
        ("It keeps counts.Then", "counts.", True),
        ("- **Answer:** so", "- **Answer:**", True),
    ],
)
def test_a_clause_is_held_only_as_whole_words(text: str, clause: str, held: bool) -> None:
    assert holds(text, clause) is held


def test_a_rewritten_unit_that_head_does_not_hold_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    wrong = COMPLETE.replace(
        "New:\n\n~~~~text\nIt never keeps text (R12).",
        "New:\n\n~~~~text\nIt never keeps any text (R12).",
    )
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: wrong})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`docs/page.md`: HEAD does not hold the new unit: It never keeps any text (R12)." in out


def test_a_clause_said_to_be_in_the_new_unit_that_is_not_there_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    wrong = COMPLETE.replace('Clause, `ledger`: "Counts are kept":', "Clause, the new unit:")
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: wrong})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "the new unit does not hold the clause: the ledger keeps counts," in out


def test_a_clause_with_no_place_or_not_in_its_unit_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    gap = COMPLETE.replace(
        'Clause, `ledger`: "Counts are kept":\n\n~~~~text\nthe ledger keeps counts,\n~~~~\n\n', ""
    )
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: gap})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "no clause places: the ledger keeps counts" in out
    foreign = COMPLETE.replace(
        "~~~~text\nthe ledger keeps counts,\n~~~~", "~~~~text\nthe store keeps counts,\n~~~~"
    )
    other = tmp_path / "other"
    other.mkdir()
    history(other, {"docs/page.md": SWEPT, MAPPING: foreign})
    code, out = run(other, monkeypatch, capsys)
    assert code == 1
    assert "the old unit does not hold the clause: the store keeps counts," in out


def test_an_entry_for_a_unit_that_head_still_holds_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    stale = COMPLETE.replace(
        "\n## `docs/page.md`\n\n", "\n## `docs/page.md`\n\n" + entry("# Page", [("# Page", "R12")])
    )
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: stale})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert (
        "`docs/page.md`: an entry for a unit that HEAD still holds, or that the base does not:"
        " # Page" in out
    )


def test_a_change_to_a_spec_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(
        tmp_path,
        {
            "docs/page.md": SWEPT,
            MAPPING: COMPLETE,
            "openspec/changes/demo/specs/ledger/spec.md": SPEC + "\nA moved clause.\n",
        },
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`openspec/changes/demo/specs/ledger/spec.md`: the sweep changes a spec" in out


@pytest.mark.parametrize(
    "path",
    ["docs/a page.md", "docs/sivu-\u00e4.md", "docs/page.markdown", "docs/OTHER.MD", "docs/b.mdx"],
)
def test_a_page_whose_path_git_quotes_or_whose_extension_is_not_md_is_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], path: str
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE, path: SWEPT}, {path: PAGE})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert f"`{path}`: no entry for a unit that HEAD does not hold: The ledger keeps counts." in out


def test_a_change_to_a_spec_whose_path_git_quotes_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    spec = "openspec/specs/a b/spec.md"
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: COMPLETE, spec: SPEC + "\nA moved clause.\n"},
        {spec: SPEC},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert f"`{spec}`: the sweep changes a spec" in out


def test_a_file_that_is_not_markdown_is_not_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: COMPLETE, "docs/a.txt": "b\n"},
        {"docs/a.txt": "a\n"},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0
    assert "docs/a.txt" not in out


def test_a_changed_file_read_as_no_units_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE, "docs/empty.md": "\n\n"})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`docs/empty.md`: read as no units at HEAD" in out


def test_a_base_that_cannot_be_resolved_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE})
    code, out = run(tmp_path, monkeypatch, capsys, "refs/remotes/origin/nothing")
    assert code == 2
    assert "cannot resolve the merge base with refs/remotes/origin/nothing" in out


def test_a_missing_mapping_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 2
    assert f"HEAD holds no {MAPPING}" in out


def test_the_mapping_is_read_from_head_not_the_working_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE})
    write(tmp_path, {MAPPING: OPENING})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


@pytest.mark.parametrize(
    "broken",
    [
        COMPLETE.replace(
            "Old:\n\n~~~~text\nThe ledger keeps counts.\n~~~~", "Old:\n\nThe ledger keeps counts."
        ),
        COMPLETE.rstrip("\n").removesuffix("~~~~"),
    ],
    ids=["a label with no fence", "a last fence that never closes"],
)
def test_a_mapping_out_of_its_form_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], broken: str
) -> None:
    assert broken != COMPLETE
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: broken})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 2
    assert "the mapping is not in its form" in out


def test_units_are_sentences_list_items_rows_headings_and_whole_fences() -> None:
    assert units(PAGE) == [
        "# Page",
        "The ledger keeps counts.",
        "It never keeps text.",
        "- **Answer:** the ledger keeps counts, so text never leaks.",
        "| Part | Where |",
        "|---|---|",
        "| Ledger | `.pr-cost/` |",
        "```mermaid\nflowchart LR\n  A --> B\n```",
    ]


def test_a_list_item_runs_on_over_its_indented_lines_and_a_nested_item_is_its_own() -> None:
    text = "- First line\n  goes on. Still the item.\n  - Nested item.\n- Next.\n"
    assert units(text) == [
        "- First line goes on. Still the item.",
        "- Nested item.",
        "- Next.",
    ]


def test_a_paragraph_runs_over_lines_and_splits_only_before_a_new_sentence() -> None:
    text = "One sentence, e.g. with a\nbreak. Then `code` starts. 3 is a number. Done.\n"
    assert units(text) == [
        "One sentence, e.g. with a break.",
        "Then `code` starts.",
        "3 is a number.",
        "Done.",
    ]


def test_a_fence_in_a_list_item_and_a_tilde_fence_are_whole() -> None:
    text = "1. Step:\n\n   ```sh\n   run it\n   ```\n\n~~~\nx\n~~~\n"
    assert units(text) == ["1. Step:", "```sh\nrun it\n```", "~~~\nx\n~~~"]


def test_entries_for_a_file_that_did_not_change_are_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    extra = COMPLETE + "\n## `docs/requirements.md`\n\n" + entry("# Page", [("# Page", "R12")])
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: extra})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`docs/requirements.md`: entries for a file that did not change" in out


def test_a_clause_placed_in_a_new_unit_that_a_removed_entry_lacks_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: COMPLETE.replace("Clause, R12:", "Clause, the new unit:")},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert (
        "a clause placed in a new unit that the entry does not give: The ledger keeps counts."
        in out
    )


def test_a_section_that_is_neither_a_file_nor_a_list_is_out_of_form(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE + "\n## docs/page.md\n"})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 2
    assert "the mapping is not in its form" in out
    listed = COMPLETE + "\n## For B-007\n\n- A clause.\n\n## Left as it is\n\n- A sentence.\n"
    other = tmp_path / "other"
    other.mkdir()
    history(other, {"docs/page.md": SWEPT, MAPPING: listed})
    assert run(other, monkeypatch, capsys)[0] == 0


def test_a_clause_that_this_pull_requests_own_work_changed_is_listed_apart(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    changed = COMPLETE.replace("Clause, R12:", "Clause, changed, the status moves on:")
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: changed})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out
    assert (
        "## Changed by this pull request's own work\n\n"
        "- `docs/page.md`: The ledger keeps counts. (the status moves on)\n"
    ) in out
    empty = COMPLETE.replace("Clause, R12:", "Clause, changed, :")
    other = tmp_path / "other"
    other.mkdir()
    history(other, {"docs/page.md": SWEPT, MAPPING: empty})
    code, out = run(other, monkeypatch, capsys)
    assert code == 1
    assert "changed, is not a place" in out


def test_a_clause_that_the_old_unit_holds_twice_covers_its_second_place_too(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    before = "# Page\n\nCounts and tokens and calls.\n"
    after = "# Page\n\nCounts and tokens, and calls (R12).\n"
    text = mapping(
        (
            "docs/page.md",
            [
                entry(
                    "Counts and tokens and calls.",
                    [
                        ("Counts and tokens", "the new unit"),
                        ("and", "the new unit"),
                        ("calls", "the new unit"),
                    ],
                    new="Counts and tokens, and calls (R12).",
                )
            ],
        )
    )
    history(tmp_path, {"docs/page.md": after, MAPPING: text}, {"docs/page.md": before})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


def test_a_base_file_that_git_cannot_read_makes_the_script_unable_to_compare(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE})
    blob = git(tmp_path, "rev-parse", "main:docs/page.md")
    (tmp_path / ".git" / "objects" / blob[:2] / blob[2:]).unlink()
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 2
    assert "Cannot compare: git cannot read `docs/page.md` at the base." in out


def test_a_list_of_changes_that_git_cannot_give_makes_the_script_unable_to_compare(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE})
    tree = git(tmp_path, "rev-parse", "main:docs")
    (tmp_path / ".git" / "objects" / tree[:2] / tree[2:]).unlink()
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 2
    assert "Cannot compare: git cannot list the files that changed." in out


def test_a_page_that_head_deletes_is_compared_as_holding_no_unit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    record = "docs/decisions/DR-001-a-choice.md"
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE, record: None})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert f"| `{record}` | 1 | 0 | 0 |" in out
    assert f"`{record}`: no entry for a unit that HEAD does not hold: # DR-001: A choice" in out


def test_a_run_from_a_folder_compares_every_page_whatever_git_s_diff_relative_says(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE})
    for name, value in {
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "diff.relative",
        "GIT_CONFIG_VALUE_0": "true",
    }.items():
        monkeypatch.setenv(name, value)
    code, out = run(tmp_path / "docs", monkeypatch, capsys)
    assert code == 0, out
    assert out == run(tmp_path, monkeypatch, capsys)[1]


def test_an_entry_for_a_heading_is_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    heading = entry(
        "### T1. Old title",
        [("### T1.", "the new unit"), ("Old title", "changed, renamed")],
        new="### T1. New title",
    )
    text = COMPLETE + f"\n## `docs/other.md`\n\n{heading}"
    history(
        tmp_path,
        {"docs/page.md": SWEPT, "docs/other.md": "### T1. New title\n", MAPPING: text},
        {"docs/other.md": "### T1. Old title\n"},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


def test_a_run_that_compares_no_page_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {MAPPING: OPENING})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "no changed page was compared" in out


def test_places_resolve_when_run_from_a_folder_of_the_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE})
    code, out = run(tmp_path / "docs", monkeypatch, capsys)
    assert code == 0, out


def test_a_scenario_that_only_an_archived_change_holds_is_not_a_place(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    archived = "openspec/changes/archive/old/specs/ledger/spec.md"
    place = '`ledger`: "Only the archive says so"'
    history(
        tmp_path,
        {
            "docs/page.md": SWEPT,
            MAPPING: COMPLETE.replace("Clause, R12:", f"Clause, {place}:"),
            archived: "### Requirement: B\n\n#### Scenario: Only the archive says so\n",
        },
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert f"no spec at HEAD holds {place}" in out


def test_a_changed_file_read_as_no_units_at_the_base_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: COMPLETE, "docs/empty.md": "Text.\n"},
        {"docs/empty.md": "\n\n"},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`docs/empty.md`: read as no units at the base" in out


def test_an_entry_for_a_removed_fence_keeps_its_lines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fence = "```mermaid\nflowchart LR\n  A --> B\n```"
    text = COMPLETE + entry(fence, [(fence, "R12")])
    history(tmp_path, {"docs/page.md": SWEPT.replace(fence + "\n", ""), MAPPING: text})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


def test_a_page_that_is_not_utf_8_makes_the_script_unable_to_compare(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE})
    (tmp_path / "docs" / "bytes.md").write_bytes(b"Caf\xe9.\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "Bytes")
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 2
    assert "Cannot compare: git's output is not UTF-8" in out
    assert ":docs/bytes.md" in out


def test_a_clause_of_one_word_placed_outside_the_new_unit_is_listed_apart(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    split = (
        COMPLETE.replace(
            "Clause, R12:\n\n~~~~text\nThe ledger keeps counts.\n~~~~\n",
            "Clause, DR-001:\n\n~~~~text\nThe\n~~~~\n\n"
            "Clause, task 1.37:\n\n~~~~text\nledger\n~~~~\n\n"
            "Clause, the page:\n\n~~~~text\nkeeps\n~~~~\n\n"
            "Clause, R12:\n\n~~~~text\ncounts.\n~~~~\n",
        )
        .replace(
            '`ledger`: "Counts are kept":\n\n~~~~text\nthe ledger keeps counts,\n~~~~\n',
            '`ledger`: "Counts are kept":\n\n~~~~text\nthe ledger keeps\n~~~~\n\n'
            'Clause, `ledger`: "Counts are kept":\n\n~~~~text\ncounts,\n~~~~\n',
        )
        .replace(
            "Clause, the new unit:\n\n~~~~text\nIt never keeps text\n~~~~\n",
            "Clause, the new unit:\n\n~~~~text\nIt\n~~~~\n\n"
            "Clause, the new unit:\n\n~~~~text\nnever keeps text\n~~~~\n",
        )
    )
    assert split.count("Clause, ") == COMPLETE.count("Clause, ") + 5
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: split})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out
    assert (
        "## Clauses of one word or none, but IDs and punctuation placed on the new unit\n\n"
        "- `docs/page.md`: The (DR-001)\n"
        "- `docs/page.md`: ledger (task 1.37)\n"
        "- `docs/page.md`: keeps (the page)\n"
        "- `docs/page.md`: counts. (R12)\n"
        "- `docs/page.md`: It (the new unit)\n"
        '- `docs/page.md`: counts, (`ledger`: "Counts are kept")\n'
    ) in out
    assert "the ledger keeps (" not in out
    assert "never keeps text (" not in out


def test_a_clause_of_one_word_with_an_apostrophe_is_listed_apart(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    clauses = [("It", "R12"), ("doesn't", "R12"), ("keep text.", "R12")]
    history(
        tmp_path,
        {
            "docs/other.md": "Nothing is kept (R12).\n",
            MAPPING: mapping(("docs/other.md", [entry("It doesn't keep text.", clauses)])),
        },
        before={"docs/other.md": "It doesn't keep text.\n"},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out
    assert "- `docs/other.md`: It (R12)\n- `docs/other.md`: doesn't (R12)\n" in out
    assert "keep text. (R12)" not in out


def test_a_place_in_a_spec_whose_path_git_quotes_resolves(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    place = '`ledger`: "Only the quoted spec says so"'
    quoted = "openspec/changes/d\u00e9mo/specs/ledger/spec.md"
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: COMPLETE.replace('`ledger`: "Counts are kept"', place)},
        before={quoted: SPEC.replace("Counts are kept", "Only the quoted spec says so")},
    )
    assert git(tmp_path, "ls-tree", "-r", "--name-only", "HEAD", "openspec").count('"') == 2
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


def test_a_clause_placed_on_a_requirement_that_its_new_unit_does_not_cite_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    uncited = COMPLETE.replace(
        "Clause, the new unit:\n\n~~~~text\nIt never keeps text\n~~~~\n",
        "Clause, R13:\n\n~~~~text\nIt never keeps text\n~~~~\n",
    )
    assert uncited != COMPLETE
    register = REGISTER + "| R13 | x | `ledger` | B |\n"
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: uncited},
        before={"docs/requirements.md": register},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`docs/page.md`: the new unit does not cite R13: It never keeps text\n" in out


def test_a_requirement_that_the_new_unit_cites_alone_or_in_a_range_holds_its_clause(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    ranged = "It never keeps text (R12 to R14)."
    placed = COMPLETE.replace("It never keeps text (R12).", ranged).replace(
        "Clause, the new unit:\n\n~~~~text\nIt never keeps text\n~~~~\n",
        "Clause, R13:\n\n~~~~text\nIt never keeps text\n~~~~\n",
    )
    placed = placed.replace(
        "Clause, the new unit:\n\n~~~~text\nso text never leaks\n~~~~\n",
        "Clause, R12:\n\n~~~~text\nso text never leaks\n~~~~\n",
    )
    assert placed.count("Clause, R1") == COMPLETE.count("Clause, R1") + 2
    register = REGISTER + "| R13 | x | `ledger` | B |\n"
    history(
        tmp_path,
        {"docs/page.md": SWEPT.replace("It never keeps text (R12).", ranged), MAPPING: placed},
        before={"docs/requirements.md": register},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


def test_a_head_without_the_register_reads_no_requirement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE, "docs/requirements.md": None})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`docs/page.md`: R12 is not in the register at HEAD" in out
    assert "Cannot compare" not in out


@pytest.mark.parametrize(
    "path",
    [
        "docs/requirements.md",
        "openspec/changes/demo/tasks.md",
        "openspec/changes/demo/specs/ledger/spec.md",
    ],
)
def test_a_file_that_git_cannot_read_at_head_makes_the_script_unable_to_compare(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], path: str
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE})
    blob = git(tmp_path, "rev-parse", f"HEAD:{path}")
    (tmp_path / ".git" / "objects" / blob[:2] / blob[2:]).unlink()
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 2
    assert f"Cannot compare: git cannot read `{path}` at HEAD." in out


def test_a_tree_that_git_cannot_list_at_head_makes_the_script_unable_to_compare(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(tmp_path, {"docs/page.md": SWEPT, MAPPING: COMPLETE})
    tree = git(tmp_path, "rev-parse", "HEAD:openspec")
    (tmp_path / ".git" / "objects" / tree[:2] / tree[2:]).unlink()
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 2
    assert "Cannot compare: git cannot list the files at HEAD." in out


def test_a_removed_unit_placed_on_a_requirement_that_the_page_does_not_cite_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    moved = COMPLETE.replace(
        entry("The ledger keeps counts.", [("The ledger keeps counts.", "R12")]),
        entry("The ledger keeps counts.", [("The ledger keeps counts.", "R13")]),
    )
    assert moved != COMPLETE
    register = REGISTER + "| R13 | x | `ledger` | B |\n"
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: moved},
        before={"docs/requirements.md": register},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "`docs/page.md`: HEAD's page does not cite R13: The ledger keeps counts.\n" in out


@pytest.mark.parametrize("citation", ["(R13)", "(R11 to R14)"])
def test_a_removed_unit_placed_on_a_requirement_that_the_page_cites_alone_or_in_a_range_passes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    citation: str,
) -> None:
    moved = COMPLETE.replace(
        entry("The ledger keeps counts.", [("The ledger keeps counts.", "R12")]),
        entry("The ledger keeps counts.", [("The ledger keeps counts.", "R13")]),
    )
    register = REGISTER + "| R13 | x | `ledger` | B |\n"
    history(
        tmp_path,
        {"docs/page.md": SWEPT + f"\nCounts are kept {citation}.\n", MAPPING: moved},
        before={"docs/requirements.md": register},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


def test_a_clause_held_only_in_an_html_comment_of_the_page_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    hidden = SWEPT + "\n<!-- The ledger keeps counts. -->\n"
    history(
        tmp_path,
        {"docs/page.md": hidden, MAPPING: COMPLETE.replace("Clause, R12:", "Clause, the page:")},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert (
        "`docs/page.md`: HEAD's page holds an HTML comment, whose text GitHub does not show\n"
        in out
    )


def test_text_that_only_begins_as_an_html_comment_does_not_begin_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(
        tmp_path, {"docs/page.md": SWEPT + "\nThe text <!- opens no comment.\n", MAPPING: COMPLETE}
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


def test_an_html_comment_in_a_page_that_did_not_change_is_not_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: COMPLETE},
        before={"docs/template.md": "<!-- Say what changes. -->\n"},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


HIDDEN = '[//]: # "The ledger keeps counts."'
DEFINED = "`docs/page.md`: HEAD's page holds a link reference definition, whose text GitHub"


@pytest.mark.parametrize(
    "hidden",
    [
        f"\n{HIDDEN}\n",
        f"\n   {HIDDEN}\n",
        f"\n> {HIDDEN}\n",
        f"\n>\t{HIDDEN}\n",
        f"\n- {HIDDEN}\n",
        f"\n* {HIDDEN}\n",
        f"\n+\t{HIDDEN}\n",
        f"\n1. {HIDDEN}\n",
        f"\n10)\t{HIDDEN}\n",
        f"\n> - {HIDDEN}\n",
        f"\n- A point.\n  - {HIDDEN}\n",
        f"\n- A point.\n\t- {HIDDEN}\n",
        f"\n- A point.\n\n  {HIDDEN}\n",
        f"\n- A point.\n\n    {HIDDEN}\n",
        '\n[a\\]b]: # "The ledger keeps counts."\n',
        "\n[^1]: The ledger keeps counts.\n",
        f"\n- A point.\n  - Another.\n    - {HIDDEN}\n",
        f"\n100. A point.\n\n     {HIDDEN}\n",
        f"\n> > - {HIDDEN}\n",
        f"\n>{HIDDEN}\n",
        f"\r{HIDDEN}\r",
        '\n[a\\\nb]: # "The ledger keeps counts."\n',
        f"\nA note.\r\r{HIDDEN}\r",
        '\n[a\\ b]: # "The ledger keeps counts."\n',
    ],
    ids=[
        "at the start of a line",
        "indented three spaces",
        "in a block quote",
        "after a block quote's marker and a tab",
        "in a list item",
        "in an item marked with an asterisk",
        "in an item marked with a plus and a tab",
        "in a numbered item",
        "in an item numbered with a parenthesis and a tab",
        "in a list item in a block quote",
        "in a nested list item",
        "in a list item nested with a tab",
        "continuing a list item at two spaces",
        "continuing a list item at four spaces",
        "with an escaped bracket in its label",
        "a footnote's definition that nothing refers to",
        "in a list item nested twice",
        "continuing an item numbered 100 at five spaces",
        "in a list item in a block quote in a block quote",
        "after a block quote's marker with no space",
        "after a carriage return that no line feed follows",
        "with a backslash before a line break in its label",
        "after a paragraph and a blank line of lone carriage returns",
        "with a backslash before a space in its label",
    ],
)
def test_a_clause_held_only_in_a_link_reference_definition_of_the_page_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], hidden: str
) -> None:
    history(
        tmp_path,
        {
            "docs/page.md": SWEPT + hidden,
            MAPPING: COMPLETE.replace("Clause, R12:", "Clause, the page:"),
        },
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert f"{DEFINED} does not show\n" in out


def test_a_definition_on_the_first_line_after_a_byte_order_mark_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(
        tmp_path,
        {
            "docs/page.md": f"\ufeff{HIDDEN}\n\n{SWEPT}",
            MAPPING: COMPLETE.replace("Clause, R12:", "Clause, the page:"),
        },
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert f"{DEFINED} does not show\n" in out


def test_a_line_indented_as_code_is_taken_as_a_definition_since_it_may_continue_a_list_item(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    shown = SWEPT + "\n    [code]: a line that GitHub shows as code, but hides in a list item\n"
    history(tmp_path, {"docs/page.md": shown, MAPPING: COMPLETE})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 1
    assert f"{DEFINED} does not show\n" in out


def test_a_link_a_checkbox_a_bracket_within_a_line_or_inline_code_defines_no_link_reference(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    shown = SWEPT + (
        "\n[The guide](guide.md) shows how counts are kept.\n"
        "\n- [ ] A task that GitHub shows with a box.\n"
        "\nAs [the ledger]: its page says, counts are kept.\n"
        "\n`[code]: a span that GitHub shows as code`\n"
    )
    history(tmp_path, {"docs/page.md": shown, MAPPING: COMPLETE})
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


def test_a_link_reference_definition_in_a_page_that_did_not_change_is_not_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    history(
        tmp_path,
        {"docs/page.md": SWEPT, MAPPING: COMPLETE},
        before={"docs/template.md": "[//]: # (Say what changes.)\n"},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out


def test_a_word_of_its_own_on_the_new_unit_is_listed_apart_but_an_id_or_punctuation_is_not(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    clauses = [
        ("No", "the new unit"),
        ("text is kept", "the new unit"),
        (",", "the new unit"),
        ("ever", "the new unit"),
        ("(T4).", "the new unit"),
    ]
    new = "No text is kept, ever, by the ledger (T4)."
    history(
        tmp_path,
        {
            "docs/other.md": new + "\n",
            MAPPING: mapping(
                ("docs/other.md", [entry("No text is kept, ever (T4).", clauses, new)])
            ),
        },
        before={"docs/other.md": "No text is kept, ever (T4).\n"},
    )
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out
    assert (
        "## Clauses of one word or none, but IDs and punctuation placed on the new unit\n\n"
        "- `docs/other.md`: No (the new unit)\n"
        "- `docs/other.md`: ever (the new unit)\n"
    ) in out
    assert "(T4). (the new unit)" not in out
    assert ", (the new unit)" not in out


@pytest.mark.parametrize(
    ("clause", "place", "listed"),
    [
        ("No", "the new unit", True),
        ("30", "the new unit", True),
        ("CI", "the new unit", True),
        ("R4's", "the new unit", True),
        ("(T4).", "the new unit", False),
        ("DR-196)", "the new unit", False),
        ("(B-022)", "the new unit", False),
        (",", "the new unit", False),
        ("", "the new unit", False),
        ("no session value", "the new unit", False),
        ("keeps", "the page", True),
        ("(T4).", "R12", True),
        (",", "DR-001", True),
        ("", "R12", True),
        ("never keeps text", "R12", False),
    ],
)
def test_one_word_or_none_is_listed_apart_but_an_id_or_punctuation_in_the_new_unit(
    clause: str, place: str, listed: bool
) -> None:
    assert short(clause, place) is listed


def test_an_id_inside_a_longer_word_cites_no_requirement_alone_or_in_a_range() -> None:
    assert cited("PR40, PR1 to R3, and R7 to R9") == {3, 7, 8, 9}
