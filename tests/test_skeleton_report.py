"""The walking skeleton's report, task 1.33 of `add-pr-cost-calculator`.

Driven with ledger files in a temporary git repository, whose commits the test checks out into
two folders as the workflow does, and recorded responses of GitHub's API. Nothing here uses the
network. R241 in `project-standards` and DR-246.
"""

from __future__ import annotations

import io
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import Any

import pytest
import report
from test_backlog import AUTHOR
from test_roadmap import isolated_environment, session_free_environment

ZEROS = "0" * 40
REPOSITORY = "someone/scratch"


def line(key: str, model: str = "model-a", tokens: int = 1_000_000) -> dict[str, Any]:
    return {
        "key": key,
        "model": model,
        "day": "2026-11-16",
        "input_tokens": tokens,
        "output_tokens": tokens,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }


class Repository:
    """A temporary repository whose main branch already holds one ledger file."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.path = root / "repo"
        self.path.mkdir()
        self.env = {**isolated_environment(self.path), **AUTHOR}
        self.git("init", "-q", "-b", "main")
        self.add_ledger("old", [line("k-old", "model-old")])
        self.git("commit", "-q", "-m", "Before")

    def git(self, *args: str) -> str:
        done = subprocess.run(
            ["git", *args], cwd=self.path, env=self.env, check=True, capture_output=True, text=True
        )
        return done.stdout.strip()

    def add_ledger(self, name: str, lines: list[dict[str, Any]]) -> None:
        path = self.path / ".pr-cost" / "ledger" / "2026-11" / f"{name}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(item) + "\n" for item in lines))
        self.git("add", "-A")

    def branch_with_two_commits(self) -> None:
        self.git("checkout", "-q", "-b", "work")
        (self.path / "one.txt").write_text("one\n")
        self.add_ledger("first", [line("k1"), line("k2", "model-b")])
        self.git("commit", "-q", "-m", "First")
        (self.path / "two.txt").write_text("two\n")
        self.add_ledger("second", [line("k2", "model-b"), line("k3")])
        self.git("commit", "-q", "-m", "Second")
        self.git("checkout", "-q", "main")

    def tree(self, commit: str, name: str) -> Path:
        """Check a commit out into a folder of its own, as the workflow's checkout does."""
        folder = self.root / name
        folder.mkdir()
        archive = subprocess.run(
            ["git", "archive", commit], cwd=self.path, env=self.env, check=True, capture_output=True
        ).stdout
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            tar.extractall(folder, filter="data")
        return folder


class GitHub:
    """Recorded responses of GitHub's API, and the requests made of it."""

    def __init__(self, pulls: list[dict[str, Any]]) -> None:
        self.pulls = pulls
        self.requests: list[tuple[str, str, Any]] = []

    def __call__(self, method: str, path: str, body: Any = None) -> Any:
        self.requests.append((method, path, body))
        return self.pulls if method == "GET" else {"id": 1}

    @property
    def comments(self) -> list[str]:
        return [body["body"] for method, _, body in self.requests if method == "POST"]


MERGED = {"number": 7, "merged_at": "2026-11-16T03:00:00Z"}


def run(
    tmp_path: Path,
    before: str,
    after: str,
    before_tree: Path | None,
    after_tree: Path,
    github: GitHub,
) -> str:
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"before": before, "after": after}))
    summary = tmp_path / "summary.md"
    summary.write_text("An earlier step's summary.\n")
    env = {
        "GITHUB_EVENT_PATH": str(event),
        "GITHUB_REPOSITORY": REPOSITORY,
        "GITHUB_STEP_SUMMARY": str(summary),
    }
    trees = [str(before_tree or tmp_path / "no-before"), str(after_tree)]
    assert report.main(trees, env, github) == 0
    text = summary.read_text()
    assert text.startswith("An earlier step's summary.\n")
    return text


def merged_by(repository: Repository, how: str) -> tuple[str, str]:
    """Merge the work branch into main as GitHub would; give the push's before and after."""
    before = repository.git("rev-parse", "HEAD")
    if how == "merge":
        repository.git("merge", "-q", "--no-ff", "-m", "Merge", "work")
    elif how == "squash":
        repository.git("merge", "-q", "--squash", "work")
        repository.git("commit", "-q", "-m", "Squash")
    else:
        repository.git("cherry-pick", "work~1", "work")
    return before, repository.git("rev-parse", "HEAD")


@pytest.mark.parametrize("how", ["merge", "squash", "rebase"])
def test_a_merge_a_squash_and_a_rebase_give_the_files_that_the_push_added(
    tmp_path: Path, how: str
) -> None:
    repository = Repository(tmp_path)
    repository.branch_with_two_commits()
    before, after = merged_by(repository, how)
    github = GitHub([MERGED])
    summary = run(
        tmp_path,
        before,
        after,
        repository.tree(before, "before"),
        repository.tree(after, "after"),
        github,
    )
    (comment,) = github.comments
    assert github.requests[0] == ("GET", f"/repos/{REPOSITORY}/commits/{after}/pulls", None)
    assert github.requests[1][1] == f"/repos/{REPOSITORY}/issues/7/comments"
    for text in (comment, summary):
        assert "| `model-a` | 2 | 2,000,000 | 2,000,000 | 0 | 0 | 6.00 |" in text
        assert "| `model-b` | 1 | 1,000,000 | 1,000,000 | 0 | 0 | 3.00 |" in text
        assert "model-old" not in text
        assert "**9.00** at the test price" in text


def test_one_call_in_two_ledger_files_is_counted_once(tmp_path: Path) -> None:
    repository = Repository(tmp_path)
    repository.branch_with_two_commits()
    before, after = merged_by(repository, "merge")
    github = GitHub([MERGED])
    run(tmp_path, before, after, repository.tree(before, "b"), repository.tree(after, "a"), github)
    assert "| `model-b` | 1 |" in github.comments[0]


def test_the_comment_says_that_its_figure_is_not_a_real_cost(tmp_path: Path) -> None:
    repository = Repository(tmp_path)
    repository.branch_with_two_commits()
    before, after = merged_by(repository, "merge")
    github = GitHub([MERGED])
    summary = run(
        tmp_path, before, after, repository.tree(before, "b"), repository.tree(after, "a"), github
    )
    for text in (github.comments[0], summary):
        assert "walking skeleton" in text
        assert "test price" in text and "not a real cost" in text


@pytest.mark.parametrize(
    ("before", "pulls", "why"),
    [
        (ZEROS, [MERGED], "creates the branch"),
        (None, [], "no merged pull request"),
        (None, [{"number": 7, "merged_at": None}], "no merged pull request"),
        (None, [MERGED, {"number": 8, "merged_at": "2026-11-16T04:00:00Z"}], "more than one"),
    ],
)
def test_a_push_with_no_single_merged_pull_request_posts_no_comment(
    tmp_path: Path, before: str | None, pulls: list[dict[str, Any]], why: str
) -> None:
    repository = Repository(tmp_path)
    repository.branch_with_two_commits()
    real_before, after = merged_by(repository, "merge")
    github = GitHub(pulls)
    before_tree = None if before == ZEROS else repository.tree(real_before, "b")
    summary = run(
        tmp_path, before or real_before, after, before_tree, repository.tree(after, "a"), github
    )
    assert github.comments == []
    assert "No comment" in summary and why in summary


def test_a_push_that_added_no_ledger_file_says_so(tmp_path: Path) -> None:
    repository = Repository(tmp_path)
    before = repository.git("rev-parse", "HEAD")
    (repository.path / "plain.txt").write_text("plain\n")
    repository.git("add", "-A")
    repository.git("commit", "-q", "-m", "Plain")
    after = repository.git("rev-parse", "HEAD")
    github = GitHub([MERGED])
    run(tmp_path, before, after, repository.tree(before, "b"), repository.tree(after, "a"), github)
    assert "no ledger file" in github.comments[0]


def test_a_line_it_cannot_read_and_a_model_name_it_does_not_take_are_counted(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path)
    before = repository.git("rev-parse", "HEAD")
    folder = repository.path / ".pr-cost" / "ledger" / "2026-11"
    odd = [line("k5", "[a link](https://example.invalid)"), line("k6"), {"key": "k7"}]
    (folder / "odd.jsonl").write_text(
        "{not json\n" + "".join(json.dumps(item) + "\n" for item in odd) + json.dumps([1]) + "\n"
    )
    repository.git("add", "-A")
    repository.git("commit", "-q", "-m", "Odd")
    after = repository.git("rev-parse", "HEAD")
    github = GitHub([MERGED])
    run(tmp_path, before, after, repository.tree(before, "b"), repository.tree(after, "a"), github)
    comment = github.comments[0]
    assert "example.invalid" not in comment and "| `model-a` | 1 |" in comment
    assert "4 ledger lines could not be read" in comment


def test_the_test_price_is_named_as_one() -> None:
    assert set(report.TEST_PRICE_PER_MILLION_TOKENS) == {
        "input_tokens",
        "output_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
    }


class Response(io.BytesIO):
    def __enter__(self) -> Response:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def test_the_api_is_called_with_the_token_and_gives_json(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[Any] = []

    def recorded(request: Any, timeout: float) -> Response:
        seen.append((request, timeout))
        return Response(b'[{"number": 7}]')

    monkeypatch.setattr(report, "urlopen", recorded)
    api = report.github_api({"GITHUB_TOKEN": "a-token", "GITHUB_API_URL": "https://api.invalid"})
    assert api("POST", "/repos/x/y/issues/7/comments", {"body": "b"}) == [{"number": 7}]
    request, timeout = seen[0]
    assert request.full_url == "https://api.invalid/repos/x/y/issues/7/comments"
    assert request.get_method() == "POST" and request.data == b'{"body": "b"}'
    assert request.get_header("Authorization") == "Bearer a-token"
    assert timeout > 0


def test_the_script_runs_as_the_workflow_runs_it(tmp_path: Path) -> None:
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"before": ZEROS, "after": "a" * 40}))
    summary = tmp_path / "summary.md"
    env = {
        **session_free_environment(),
        "GITHUB_EVENT_PATH": str(event),
        "GITHUB_REPOSITORY": REPOSITORY,
        "GITHUB_STEP_SUMMARY": str(summary),
        "GITHUB_TOKEN": "a-token",
    }
    done = subprocess.run(
        [
            sys.executable,
            "-I",
            str(Path(report.__file__)),
            str(tmp_path / "b"),
            str(tmp_path / "a"),
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    assert done.returncode == 0, done.stderr
    assert "No comment" in summary.read_text()


# ---- Found at the threat review at implementation ----


def test_a_count_that_is_negative_a_boolean_or_too_large_is_not_counted(tmp_path: Path) -> None:
    repository = Repository(tmp_path)
    before = repository.git("rev-parse", "HEAD")
    bad = [
        {**line("k8"), "input_tokens": -5},
        {**line("k9"), "output_tokens": True},
        {**line("k10"), "input_tokens": 10**400},
        line("k11"),
    ]
    folder = repository.path / ".pr-cost" / "ledger" / "2026-11"
    (folder / "bad.jsonl").write_text("".join(json.dumps(item) + "\n" for item in bad))
    (folder / "latin.jsonl").write_bytes(b"\xff\xfe not utf-8\n")
    repository.git("add", "-A")
    repository.git("commit", "-q", "-m", "Bad")
    after = repository.git("rev-parse", "HEAD")
    github = GitHub([MERGED])
    summary = run(
        tmp_path, before, after, repository.tree(before, "b"), repository.tree(after, "a"), github
    )
    comment = github.comments[0]
    assert (
        "| `model-a` | 1 |" in comment
        and "**3.00**" in comment
        and "-" not in comment.split("**")[1]
    )
    assert "4 ledger lines could not be read" in comment and summary.endswith(comment)


def test_a_ledger_file_that_is_a_link_is_not_followed(tmp_path: Path) -> None:
    repository = Repository(tmp_path)
    before_tree = repository.tree(repository.git("rev-parse", "HEAD"), "b")
    after_tree = repository.tree(repository.git("rev-parse", "HEAD"), "a")
    outside = tmp_path / "outside.jsonl"
    outside.write_text(json.dumps(line("k12", "model-outside")) + "\n")
    (after_tree / ".pr-cost" / "ledger" / "2026-11" / "link.jsonl").symlink_to(outside)
    github = GitHub([MERGED])
    run(tmp_path, "b" * 40, "c" * 40, before_tree, after_tree, github)
    assert "model-outside" not in github.comments[0]
    assert "1 ledger lines could not be read" in github.comments[0]


# ---- Found by the review lanes ----


@pytest.mark.parametrize("link", [".pr-cost", ".pr-cost/ledger"])
def test_a_ledger_folder_that_is_a_link_is_not_followed(tmp_path: Path, link: str) -> None:
    repository = Repository(tmp_path)
    before_tree = repository.tree(repository.git("rev-parse", "HEAD"), "b")
    after_tree = repository.tree(repository.git("rev-parse", "HEAD"), "a")
    outside = tmp_path / "outside"
    (outside / "ledger" / "2026-11").mkdir(parents=True)
    (outside / "2026-11").mkdir()
    for folder in (outside / "ledger" / "2026-11", outside / "2026-11"):
        (folder / "x.jsonl").write_text(json.dumps(line("k13", "model-outside")) + "\n")
    shutil.rmtree(after_tree / ".pr-cost")
    if link == ".pr-cost":
        (after_tree / ".pr-cost").symlink_to(outside, target_is_directory=True)
    else:
        (after_tree / ".pr-cost").mkdir()
        (after_tree / ".pr-cost" / "ledger").symlink_to(outside, target_is_directory=True)
    github = GitHub([MERGED])
    run(tmp_path, "b" * 40, "c" * 40, before_tree, after_tree, github)
    assert "model-outside" not in github.comments[0]


def test_a_folder_named_like_a_ledger_file_is_counted_as_unread(tmp_path: Path) -> None:
    repository = Repository(tmp_path)
    before_tree = repository.tree(repository.git("rev-parse", "HEAD"), "b")
    after_tree = repository.tree(repository.git("rev-parse", "HEAD"), "a")
    folder = after_tree / ".pr-cost" / "ledger" / "2026-11" / "x.jsonl"
    folder.mkdir()
    (folder / "inside.txt").write_text("text\n")
    github = GitHub([MERGED])
    summary = run(tmp_path, "b" * 40, "c" * 40, before_tree, after_tree, github)
    assert "1 ledger lines could not be read" in github.comments[0]
    assert summary.endswith(github.comments[0])


def test_a_model_name_is_written_as_code_so_that_it_is_never_a_link(tmp_path: Path) -> None:
    repository = Repository(tmp_path)
    before = repository.git("rev-parse", "HEAD")
    repository.add_ledger("named", [line("k14", "www.example.com"), line("k15", "a.@someone")])
    repository.git("commit", "-q", "-m", "Named")
    github = GitHub([MERGED])
    run(
        tmp_path,
        before,
        repository.git("rev-parse", "HEAD"),
        repository.tree(before, "b"),
        repository.tree("HEAD", "a"),
        github,
    )
    assert "| `www.example.com` | 1 |" in github.comments[0]
    assert "| `a.@someone` | 1 |" in github.comments[0]


def test_capture_and_the_report_agree_on_the_ledgers_form() -> None:
    """Each script runs alone, so each keeps its own copy of what the other writes or reads."""
    import capture

    assert capture.COUNTS == report.COUNTS
    assert capture.MODEL.pattern == report.MODEL.pattern
    assert Path(capture.LEDGER) == report.LEDGER
