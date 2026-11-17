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
from sweep_evidence import MAPPING, main, units

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


def history(root: Path, after: Mapping[str, str | None]) -> None:
    """`main` holds BEFORE, fetched as `origin/main`; a branch changes it to `after`."""
    write(root, BEFORE)
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


def test_a_mapping_out_of_its_form_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    broken = COMPLETE.replace(
        "Old:\n\n~~~~text\nThe ledger keeps counts.\n~~~~", "Old:\n\nThe ledger keeps counts."
    )
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
    history(tmp_path, {"docs/page.md": before})
    git(tmp_path, "checkout", "-q", "main")
    write(tmp_path, {"docs/page.md": before})
    git(tmp_path, "commit", "-qam", "Base")
    git(tmp_path, "update-ref", "refs/remotes/origin/main", "main")
    git(tmp_path, "checkout", "-q", "work")
    git(tmp_path, "reset", "-q", "--hard", "main")
    write(tmp_path, {"docs/page.md": after, MAPPING: text})
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "Swept")
    code, out = run(tmp_path, monkeypatch, capsys)
    assert code == 0, out
