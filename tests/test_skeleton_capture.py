"""The walking skeleton's capture script, task 1.32 of `add-pr-cost-calculator`.

Driven through the seam that design decision 18 names (DR-246): a hook's input on standard
input, transcript files that the test writes, and a real git repository in a temporary folder,
with a global git configuration of the test's own for the opt-in. Nothing here reads a real
transcript or uses the network. R235, R239 and R240 in `project-standards`.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from test_repository import ROOT
from test_roadmap import session_free_environment

CAPTURE = ROOT / "skeleton" / "capture.py"
SWITCH_ON = {"enabled": True, "walking_skeleton": True}
# Values planted in every transcript line, none of which may reach a ledger file or the log.
SECRET = "planted-secret-text"
MESSAGE_ID = "msg" + "_01PLANTEDMESSAGEID"
COMMIT = "cd {repo} && git add change.txt && git commit -m 'Change it'"


def git(cwd: Path, env: dict[str, str], *args: str, check: bool = True) -> str:
    done = subprocess.run(
        ["git", *args], cwd=cwd, env=env, check=check, capture_output=True, text=True
    )
    return done.stdout


class Session:
    """A temporary folder with a repository, a person's global git configuration and a session's
    transcripts, and a way to run capture as the plugin's hooks run it."""

    def __init__(self, root: Path, switch: dict[str, Any] | None = SWITCH_ON, opt_in: bool = True):
        self.root = root
        self.repo = root / "clone"
        self.repo.mkdir()
        # The person's global file, where git finds it from `HOME` alone: capture reads the opt-in
        # without the session's git variables (R235).
        self.global_config = root / ".gitconfig"
        lines = ["[user]", "\tname = Test", "\temail = test@example.invalid"]
        if opt_in:
            lines += ["[pr-cost-skeleton]", "\tcapture = true"]
        self.global_config.write_text("\n".join(lines) + "\n")
        self.env = {
            **session_free_environment(),
            "GIT_CONFIG_NOSYSTEM": "1",
            "HOME": str(root),
            "GIT_EDITOR": "false",
        }
        git(self.repo, self.env, "init", "-q", "-b", "main")
        if switch is not None:
            (self.repo / ".pr-cost.json").write_text(json.dumps(switch))
        (self.repo / "readme.txt").write_text("hello\n")
        git(self.repo, self.env, "add", "-A")
        git(self.repo, self.env, "commit", "-q", "-m", "Start")
        self.transcript = root / "project" / "session-one.jsonl"
        self.transcript.parent.mkdir()
        self.transcript.write_text("")
        self.calls = 0

    @property
    def common_dir(self) -> Path:
        return self.repo / ".git"

    @property
    def store(self) -> Path:
        return self.common_dir / "pr-cost-skeleton" / "store.json"

    def call(
        self,
        model: str = "model-a",
        cwd: Path | None = None,
        stop_reason: str | None = "end_turn",
        transcript: Path | None = None,
        message_id: str | None = None,
        newline: bool = True,
    ) -> str:
        """Append one call's line, as Claude Code writes it, and return its message id."""
        self.calls += 1
        message_id = message_id or f"{MESSAGE_ID}{self.calls:04d}"
        line: dict[str, Any] = {
            "type": "assistant",
            "timestamp": "2026-11-16T03:04:05.678Z",
            "sessionId": "planted-session-identifier",
            "cwd": str(self.repo if cwd is None else cwd),
            "message": {
                "id": message_id,
                "model": model,
                "stop_reason": stop_reason,
                "content": [{"type": "text", "text": SECRET}],
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 20,
                    "cache_creation_input_tokens": 30,
                    "cache_read_input_tokens": 40,
                },
            },
        }
        if cwd == Path("/none"):
            del line["cwd"]
        with (transcript or self.transcript).open("a") as out:
            out.write(json.dumps(line) + ("\n" if newline else ""))
        return message_id

    def hook(
        self, event: str, cwd: Path | None = None, **extra: Any
    ) -> subprocess.CompletedProcess[str]:
        payload = {
            "session_id": "planted-session-identifier",
            "transcript_path": str(self.transcript),
            "cwd": str(self.repo if cwd is None else cwd),
            "hook_event_name": event,
            **extra,
        }
        done = subprocess.run(
            [sys.executable, "-I", str(CAPTURE)],
            input=json.dumps(payload),
            env=self.env,
            capture_output=True,
            text=True,
        )
        assert done.returncode == 0, done.stderr
        assert done.stdout == "", done.stdout
        return done

    def bash(self, event: str, command: str, cwd: Path | None = None) -> None:
        self.hook(event, cwd, tool_name="Bash", tool_input={"command": command})

    def commit(self, command: str | None = None, cwd: Path | None = None) -> int:
        """Run a command as the agent would, between its two hooks; return its exit code."""
        command = command or COMMIT.format(repo=self.repo)
        self.bash("PreToolUse", command, cwd)
        done = subprocess.run(
            ["bash", "-c", command], cwd=cwd or self.repo, env=self.env, capture_output=True
        )
        self.bash("PostToolUse" if done.returncode == 0 else "PostToolUseFailure", command, cwd)
        return done.returncode

    def change(self, text: str = "a change\n") -> None:
        (self.repo / "change.txt").write_text(text)

    def ledger_files(self, commit: str = "HEAD") -> list[str]:
        out = git(self.repo, self.env, "show", "--name-only", "--format=", commit)
        return [p for p in out.splitlines() if p.startswith(".pr-cost/ledger/")]

    def ledger_lines(self, commit: str = "HEAD") -> list[dict[str, Any]]:
        lines = []
        for path in self.ledger_files(commit):
            text = git(self.repo, self.env, "show", f"{commit}:{path}")
            lines += [json.loads(line) for line in text.splitlines()]
        return lines

    def staged(self) -> list[str]:
        return git(self.repo, self.env, "diff", "--cached", "--name-only").splitlines()

    def untracked_ledger(self) -> list[Path]:
        return (
            list((self.repo / ".pr-cost").rglob("*.jsonl"))
            if (self.repo / ".pr-cost").exists()
            else []
        )

    def waiting(self) -> int:
        return len(json.loads(self.store.read_text())["waiting"])

    def log(self) -> list[dict[str, Any]]:
        path = self.common_dir / "pr-cost-skeleton" / "log.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()]


@pytest.fixture
def session(tmp_path: Path) -> Session:
    return Session(tmp_path)


def assert_recorded_nothing(session: Session) -> None:
    assert not session.store.exists()
    assert session.staged() == []
    assert session.untracked_ledger() == []


# ---- R235: only with the skeleton's own switch and the opt-in ----


@pytest.mark.parametrize(
    "switch",
    [
        None,
        {"enabled": True},
        {"enabled": False, "walking_skeleton": True},
        {"enabled": True, "walking_skeleton": "true"},
        ["enabled"],
    ],
)
def test_without_the_skeletons_switch_it_records_nothing(tmp_path: Path, switch: Any) -> None:
    session = Session(tmp_path, switch=switch)
    session.call()
    session.hook("Stop")
    session.change()
    assert session.commit() == 0
    assert_recorded_nothing(session)
    assert session.ledger_files() == []


def test_a_switch_that_is_not_json_records_nothing(tmp_path: Path) -> None:
    session = Session(tmp_path, switch=None)
    (session.repo / ".pr-cost.json").write_text("{not json")
    session.call()
    session.hook("Stop")
    assert not session.store.exists()


def test_without_the_opt_in_in_the_global_configuration_it_records_nothing(tmp_path: Path) -> None:
    session = Session(tmp_path, opt_in=False)
    git(session.repo, session.env, "config", "pr-cost-skeleton.capture", "true")
    session.call()
    session.hook("Stop")
    session.change()
    assert session.commit() == 0
    assert_recorded_nothing(session)


def test_an_opt_in_that_is_not_true_records_nothing(tmp_path: Path) -> None:
    session = Session(tmp_path, opt_in=False)
    with session.global_config.open("a") as out:
        out.write("[pr-cost-skeleton]\n\tcapture = maybe\n")
    session.call()
    session.hook("Stop")
    assert not session.store.exists()


@pytest.mark.parametrize("variables", ["count", "global file", "config home"])
def test_the_sessions_variables_never_give_the_opt_in(tmp_path: Path, variables: str) -> None:
    """A repository's settings can set a session's variables, so they never opt anyone in."""
    session = Session(tmp_path, opt_in=False)
    elsewhere = tmp_path / "elsewhere"
    (elsewhere / "git").mkdir(parents=True)
    opt_in = "[pr-cost-skeleton]\n\tcapture = true\n"
    (elsewhere / "gitconfig").write_text(opt_in)
    (elsewhere / "git" / "config").write_text(opt_in)
    session.env.update(
        {
            "count": {
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "pr-cost-skeleton.capture",
                "GIT_CONFIG_VALUE_0": "true",
            },
            "global file": {"GIT_CONFIG_GLOBAL": str(elsewhere / "gitconfig")},
            "config home": {"XDG_CONFIG_HOME": str(elsewhere)},
        }[variables]
    )
    session.call()
    session.hook("Stop")
    assert not session.store.exists()
    assert session.log()[-1]["opt_in"] is False


def test_the_global_file_under_the_default_config_home_opts_in(tmp_path: Path) -> None:
    session = Session(tmp_path, opt_in=False)
    (tmp_path / ".config" / "git").mkdir(parents=True)
    (tmp_path / ".config" / "git" / "config").write_text("[pr-cost-skeleton]\n\tcapture = true\n")
    session.call()
    session.hook("Stop")
    assert session.waiting() == 1


def test_a_repositorys_value_that_is_not_a_boolean_leaves_the_opt_in_as_it_is(
    session: Session,
) -> None:
    git(session.repo, session.env, "config", "pr-cost-skeleton.capture", "maybe")
    session.call()
    session.hook("Stop")
    assert session.waiting() == 1


def test_a_later_global_false_turns_the_opt_in_off(tmp_path: Path) -> None:
    session = Session(tmp_path)
    with session.global_config.open("a") as out:
        out.write("[pr-cost-skeleton]\n\tcapture = false\n")
    session.call()
    session.hook("Stop")
    assert not session.store.exists()


@pytest.mark.parametrize("where", ["outside", "none", "relative"])
def test_a_call_made_outside_the_repository_is_not_kept(session: Session, where: str) -> None:
    other = session.root / "other"
    other.mkdir()
    cwd = {"outside": other, "none": Path("/none"), "relative": Path("clone")}[where]
    session.call(cwd=cwd)
    session.call(cwd=session.repo / "sub" / "folder")
    session.hook("Stop")
    assert session.waiting() == 1


def test_where_no_repository_holds_the_folder_it_works_on_each_clone_inside_it(
    session: Session,
) -> None:
    session.call()
    session.hook("Stop", cwd=session.root)
    assert session.waiting() == 1
    session.change()
    assert session.commit(cwd=session.root) == 0
    assert len(session.ledger_files()) == 1


def test_a_folder_with_no_repository_near_it_records_nothing(tmp_path: Path) -> None:
    session = Session(tmp_path)
    empty = tmp_path / "empty"
    empty.mkdir()
    session.call()
    session.hook("Stop", cwd=empty)
    session.hook("Stop", cwd=tmp_path / "missing")
    assert not session.store.exists()


# ---- R240: a recognised commit holds one ledger file ----


def test_a_recognised_commit_after_calls_holds_one_ledger_file(session: Session) -> None:
    first = session.call("model-a")
    session.call("model-b")
    session.call("model-a")
    session.change()
    assert session.commit() == 0
    shown = git(session.repo, session.env, "show", "--name-only", "--format=", "HEAD").splitlines()
    assert "change.txt" in shown
    files = session.ledger_files()
    assert len(files) == 1 and re.fullmatch(
        r"\.pr-cost/ledger/\d{4}-\d{2}/[0-9a-f]{32}\.jsonl", files[0]
    )
    lines = session.ledger_lines()
    assert sorted(line["model"] for line in lines) == ["model-a", "model-a", "model-b"]
    assert {key for line in lines for key in line} == {
        "key",
        "model",
        "day",
        "input_tokens",
        "output_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
    }
    assert all(line["day"] == "2026-11-16" and line["output_tokens"] == 20 for line in lines)
    text = git(session.repo, session.env, "show", f"HEAD:{files[0]}")
    for planted in (SECRET, first, "planted-session-identifier", str(session.repo), "end_turn"):
        assert planted not in text
    assert session.staged() == []
    assert session.waiting() == 0


def test_a_call_is_recorded_once(session: Session) -> None:
    session.call()
    session.hook("Stop")
    session.hook("Stop")
    session.change()
    assert session.commit() == 0
    session.hook("Stop")
    session.change("another change\n")
    assert session.commit() == 0
    assert session.ledger_files() == []
    assert len(session.ledger_lines("HEAD~1")) == 1


def test_a_streamed_call_is_kept_once_from_its_line_with_a_stop_reason(session: Session) -> None:
    session.call(stop_reason=None, message_id=MESSAGE_ID)
    session.call(stop_reason="tool_use", message_id=MESSAGE_ID)
    session.call(stop_reason=None, message_id=MESSAGE_ID + "X")
    session.hook("Stop")
    assert session.waiting() == 1
    assert session.log()[-1]["calls_without_stop_reason"] == 1


def test_a_subagents_calls_are_read_from_its_own_transcript(session: Session) -> None:
    folder = session.transcript.with_suffix("") / "subagents"
    folder.mkdir(parents=True)
    session.call("model-main")
    session.call("model-sub", transcript=folder / "agent-one.jsonl")
    elsewhere = session.root / "agent-two.jsonl"
    session.call("model-given", transcript=elsewhere)
    session.hook("SubagentStop", agent_transcript_path=str(elsewhere))
    session.change()
    assert session.commit() == 0
    models = sorted(line["model"] for line in session.ledger_lines())
    assert models == ["model-given", "model-main", "model-sub"]


def test_a_half_written_last_line_waits_for_its_line_break(session: Session) -> None:
    session.call(newline=False)
    session.hook("Stop")
    assert session.waiting() == 0
    assert session.log()[-1]["lines_unread"] == 0
    with session.transcript.open("a") as out:
        out.write("\n")
    session.hook("Stop")
    assert session.waiting() == 1


def test_a_line_that_is_not_json_is_counted_and_skipped(session: Session) -> None:
    with session.transcript.open("a") as out:
        out.write("{not json\n" + json.dumps(["a list"]) + "\n")
    session.call()
    session.hook("Stop")
    assert session.waiting() == 1
    assert session.log()[-1]["lines_unread"] == 1


@pytest.mark.parametrize(
    "command",
    [
        "cd {repo} && git add change.txt && git commit --amend -m 'Change it'",
        "cd {repo} && git add change.txt && git commit -m 'Change it' change.txt",
        "cd {repo} && git add change.txt && git commit -m 'Change it' | cat",
        "cd {repo} && git add change.txt; git commit -m 'Change it'",
        "cd {repo} && git add -A && git commit -m 'Change it'",
        'cd {repo} && git add change.txt && git commit -m "$(echo it)"',
        "cd {repo} && git add change.txt && GIT_DIR=.git git commit -m 'Change it'",
        "cd {repo} && git add change.txt && git -C . -C . commit -m 'Change it'",
        "cd {repo} && git add change.txt && git commit -m 'Change it' > /dev/null",
        "cd {repo} && git add change.txt && git commit -m",
        "cd {repo} && git add change.txt && git commit -m 'unclosed",
        "cd && git commit -m 'Change it'",
        "cd {repo} && git add change.txt && git status",
        "cd {repo} && git add change.txt && git commit -v -m 'Change it'",
        "cd {repo} && git add change.txt && git commit -q",
    ],
)
def test_a_commit_in_another_form_gets_no_ledger_file(session: Session, command: str) -> None:
    session.call()
    session.change()
    session.commit(command.format(repo=session.repo))
    assert session.untracked_ledger() == []
    assert ".pr-cost" not in " ".join(session.staged() + session.ledger_files())
    assert session.waiting() == 1
    assert "staged" not in [entry["staged"] for entry in session.log()]


@pytest.mark.parametrize(
    "command",
    [
        "git add change.txt && git commit -m 'Change it'",
        "git add change.txt && git commit -q -m 'Change it'",
        "git add change.txt && git commit -m 'Change it' -m 'Co-Authored-By: A <a@x.invalid>'",
        "git -C {repo} add change.txt && git -C {repo} commit -m 'Change it'",
        "cd {repo} && git commit -a -m 'Change it'",
        "cd sub && cd .. && git add change.txt && git commit -m 'Change it'",
    ],
)
def test_each_recognised_form_gets_its_ledger_file(session: Session, command: str) -> None:
    (session.repo / "sub").mkdir()
    session.call()
    session.change()
    if "-a" in command:
        (session.repo / "readme.txt").write_text("changed\n")
    assert session.commit(command.format(repo=session.repo)) == 0
    assert len(session.ledger_files()) == 1


def test_a_commit_with_nothing_to_commit_stays_empty(session: Session) -> None:
    session.call()
    head = git(session.repo, session.env, "rev-parse", "HEAD")
    for command in (
        "cd {repo} && git commit -m 'Nothing'",
        "cd {repo} && git commit -a -m 'Nothing'",
        "cd {repo} && git add readme.txt && git commit -m 'Nothing'",
    ):
        assert session.commit(command.format(repo=session.repo)) != 0
    assert git(session.repo, session.env, "rev-parse", "HEAD") == head
    assert session.untracked_ledger() == []
    assert session.waiting() == 1


def test_no_calls_waiting_gets_no_ledger_file(session: Session) -> None:
    session.change()
    assert session.commit() == 0
    assert session.ledger_files() == []


@pytest.mark.parametrize("outcome", ["PostToolUseFailure", "PostToolUse"])
def test_a_file_that_a_commit_did_not_take_is_taken_back(session: Session, outcome: str) -> None:
    session.call()
    session.change()
    command = COMMIT.format(repo=session.repo)
    session.bash("PreToolUse", command)
    assert any(p.startswith(".pr-cost/ledger/") for p in session.staged())
    session.bash(outcome, command)
    assert session.staged() == []
    assert session.untracked_ledger() == []
    assert session.waiting() == 1
    assert session.commit() == 0
    assert len(session.ledger_files()) == 1


def test_another_command_leaves_a_staged_file_alone(session: Session) -> None:
    session.call()
    session.change()
    command = COMMIT.format(repo=session.repo)
    session.bash("PreToolUse", command)
    session.bash("PostToolUse", "ls")
    session.bash("PostToolUse", "cd /elsewhere && git commit -m 'x'")
    assert any(p.startswith(".pr-cost/ledger/") for p in session.staged())


# ---- R239: never stalls or steers ----


def test_a_truncated_store_is_reported_on_standard_error(session: Session) -> None:
    session.call()
    session.hook("Stop")
    session.store.write_text(session.store.read_text()[:10])
    done = session.hook("Stop")
    assert "store" in done.stderr
    assert session.log()[-1]["error"] == "JSONDecodeError"


@pytest.mark.parametrize("given", ["not json", "[]", '{"cwd": 3}', "{}"])
def test_an_input_it_cannot_read_exits_with_success(session: Session, given: str) -> None:
    done = subprocess.run(
        [sys.executable, "-I", str(CAPTURE)],
        input=given,
        env=session.env,
        capture_output=True,
        text=True,
    )
    assert done.returncode == 0 and done.stdout == ""


def test_a_missing_transcript_is_counted_and_skipped(session: Session) -> None:
    session.transcript.unlink()
    session.hook("Stop")
    assert session.log()[-1]["transcripts_read"] == 0


# ---- The run's log: names and counts only ----


LOG_KEYS = {
    "event",
    "capture_sha256",
    "opt_in",
    "transcripts_read",
    "lines_read",
    "lines_unread",
    "calls_kept",
    "calls_without_stop_reason",
    "calls_outside",
    "calls_incomplete",
    "calls_differing",
    "staged",
    "error",
}


def test_each_runs_log_line_holds_names_and_counts_only(session: Session) -> None:
    session.call()
    session.hook("Stop")
    session.change()
    session.commit()
    session.commit(f"cd {session.repo} && git commit --amend -m x")
    log_text = (session.common_dir / "pr-cost-skeleton" / "log.jsonl").read_text()
    for planted in (SECRET, MESSAGE_ID, "planted-session-identifier", str(session.root), "model-a"):
        assert planted not in log_text
    entries = session.log()
    assert len(entries) == 5
    for entry in entries:
        assert set(entry) == LOG_KEYS
        assert all(
            isinstance(v, bool | int) or v is None or v.isidentifier()
            for k, v in entry.items()
            if k != "capture_sha256"
        )
        assert entry["capture_sha256"] == hashlib.sha256(CAPTURE.read_bytes()).hexdigest()
    assert [e["staged"] for e in entries] == [None, "staged", "committed", "not_recognised", None]
    assert entries[0] == {
        **entries[0],
        "event": "Stop",
        "opt_in": True,
        "transcripts_read": 1,
        "lines_read": 1,
        "calls_kept": 1,
    }


def test_the_log_says_why_nothing_was_staged(session: Session) -> None:
    session.bash("PreToolUse", COMMIT.format(repo=session.repo))
    session.call()
    session.bash("PreToolUse", COMMIT.format(repo=session.repo))
    assert [e["staged"] for e in session.log()] == ["nothing_waiting", "nothing_to_commit"]


def test_without_the_opt_in_the_log_says_so_and_reads_no_transcript(tmp_path: Path) -> None:
    session = Session(tmp_path, opt_in=False)
    session.call()
    session.hook("Stop")
    entry = session.log()[-1]
    assert entry["opt_in"] is False
    assert entry["transcripts_read"] == 0


def test_a_command_that_runs_no_git_is_left_alone_quickly(session: Session) -> None:
    session.call()
    session.bash("PreToolUse", "ls -la")
    assert not session.store.exists()


# ---- The rest of its branches ----


@pytest.mark.parametrize(
    "command",
    [
        "cd {repo} && git add change.txt && git -C",
        "cd {repo} && git add change.txt && git -C ~/elsewhere commit -m 'Change it'",
        "cd {repo} && && git commit -m 'Change it'",
        "cd {repo} && git add change.txt && git",
    ],
)
def test_a_command_of_a_broken_form_gets_no_ledger_file(session: Session, command: str) -> None:
    session.call()
    session.change()
    session.commit(command.format(repo=session.repo))
    assert session.untracked_ledger() == [] and session.waiting() == 1


@pytest.mark.parametrize(
    "change",
    [
        {"model": "a model with spaces"},
        {"model": 3},
        {"usage": "many"},
        {"timestamp": "yesterday"},
    ],
)
def test_a_line_without_what_a_call_needs_is_not_kept(
    session: Session, change: dict[str, Any]
) -> None:
    session.call()
    line = json.loads(session.transcript.read_text())
    target = line if "timestamp" in change else line["message"]
    target.update(change)
    session.transcript.write_text(json.dumps(line) + "\n")
    session.hook("Stop")
    assert session.waiting() == 0


def test_a_change_staged_before_the_command_is_a_commit(session: Session) -> None:
    session.call()
    session.change()
    git(session.repo, session.env, "add", "change.txt")
    assert session.commit(f"cd {session.repo} && git commit -m 'Change it'") == 0
    assert len(session.ledger_files()) == 1


def test_a_ledger_file_that_git_will_not_add_is_removed(session: Session) -> None:
    (session.repo / ".gitignore").write_text(".pr-cost/\n")
    session.call()
    session.change()
    assert session.commit() == 0
    assert session.ledger_files() == [] and session.untracked_ledger() == []
    assert [e["staged"] for e in session.log()][-2] == "add_failed"
    assert session.waiting() == 1


def test_a_file_left_staged_is_taken_back_before_the_next_one(session: Session) -> None:
    session.call()
    session.change()
    command = COMMIT.format(repo=session.repo)
    session.bash("PreToolUse", command)
    session.bash("PreToolUse", command)
    assert len([p for p in session.staged() if p.startswith(".pr-cost/")]) == 1
    assert len(session.untracked_ledger()) == 1


def test_an_error_of_another_kind_is_reported_and_logged(session: Session) -> None:
    session.store.mkdir(parents=True)
    session.call()
    done = session.hook("Stop")
    assert "IsADirectoryError" in done.stderr
    assert session.log()[-1]["error"] == "IsADirectoryError"


def test_a_store_that_is_not_the_skeletons_is_not_used(session: Session) -> None:
    session.store.parent.mkdir(parents=True)
    session.store.write_text('{"something": "else"}')
    session.call()
    session.hook("Stop")
    assert session.log()[-1]["error"] == "ValueError"


def test_another_event_or_tool_is_left_alone(session: Session) -> None:
    session.call()
    session.hook("UserPromptSubmit")
    session.hook("PreToolUse", tool_name="Write", tool_input={"command": "git commit -m 'x'"})
    assert not session.store.exists()


def test_a_subagents_transcript_alone_is_read(session: Session) -> None:
    elsewhere = session.root / "agent.jsonl"
    session.call(transcript=elsewhere)
    session.hook("SubagentStop", transcript_path=None, agent_transcript_path=str(elsewhere))
    assert session.waiting() == 1


# ---- Found at the threat review at implementation ----


def test_the_tools_own_opt_in_alone_records_nothing(tmp_path: Path) -> None:
    session = Session(tmp_path, opt_in=False)
    with session.global_config.open("a") as out:
        out.write("[pr-cost]\n\tcapture = true\n")
    session.call()
    session.hook("Stop")
    assert not session.store.exists()


def test_an_opt_in_in_the_system_configuration_records_nothing(tmp_path: Path) -> None:
    session = Session(tmp_path, opt_in=False)
    system = tmp_path / "system.gitconfig"
    system.write_text("[pr-cost-skeleton]\n\tcapture = true\n")
    del session.env["GIT_CONFIG_NOSYSTEM"]
    session.env["GIT_CONFIG_SYSTEM"] = str(system)
    session.call()
    session.hook("Stop")
    assert not session.store.exists()


def test_a_commit_in_another_repository_than_its_adds_gets_no_ledger_file(
    session: Session,
) -> None:
    other = session.root / "other"
    other.mkdir()
    git(other, session.env, "init", "-q", "-b", "main")
    (other / ".pr-cost.json").write_text(json.dumps(SWITCH_ON))
    git(other, session.env, "add", "-A")
    git(other, session.env, "commit", "-q", "-m", "Start")
    session.call(cwd=other)
    session.call()
    session.change()
    head = git(other, session.env, "rev-parse", "HEAD")
    command = "cd clone && git add change.txt && cd ../other && git commit -m 'Change it'"
    assert session.commit(command, cwd=session.root) != 0
    assert git(other, session.env, "rev-parse", "HEAD") == head
    command = "git -C clone add change.txt && git -C other commit -m 'Change it'"
    assert session.commit(command, cwd=session.root) != 0
    assert git(other, session.env, "rev-parse", "HEAD") == head
    assert (
        not list((other / ".pr-cost").rglob("*.jsonl")) if (other / ".pr-cost").exists() else True
    )


def test_the_log_counts_the_calls_it_leaves_out_and_why(session: Session) -> None:
    session.call(cwd=session.root)
    session.call(cwd=Path("/none"))
    session.call(model="a model with spaces")
    session.call(message_id=MESSAGE_ID + "D")
    with session.transcript.open("a") as out:
        line = json.loads(session.transcript.read_text().splitlines()[-1])
        line["message"]["usage"]["output_tokens"] = 500
        out.write(json.dumps(line) + "\n")
    session.hook("Stop")
    entry = session.log()[-1]
    assert entry["calls_kept"] == 1
    assert entry["calls_outside"] == 2
    assert entry["calls_incomplete"] == 1
    assert entry["calls_differing"] == 1


# ---- Found by the review lanes ----


def test_a_call_made_in_a_repository_inside_the_repository_is_not_kept(session: Session) -> None:
    inner = session.repo / "vendor" / "inner"
    inner.mkdir(parents=True)
    git(inner, session.env, "init", "-q", "-b", "main")
    session.call(cwd=inner / "src")
    session.call(cwd=session.repo / "vendor")
    session.hook("Stop")
    assert session.waiting() == 1
    assert session.log()[-1]["calls_outside"] == 1


def test_a_quoted_message_that_holds_a_message_option_is_recognised(session: Session) -> None:
    session.call()
    session.hook("Stop")
    session.change()
    command = f"cd {session.repo} && git add change.txt && git commit -m 'explain the -m flag'"
    assert session.commit(command) == 0
    assert len(session.ledger_files()) == 1


@pytest.mark.parametrize("value", ["yes", "on", "1", "TRUE"])
def test_each_way_git_writes_true_opts_in(tmp_path: Path, value: str) -> None:
    session = Session(tmp_path, opt_in=False)
    with session.global_config.open("a") as out:
        out.write(f"[pr-cost-skeleton]\n\tcapture = {value}\n")
    session.call()
    session.hook("Stop")
    assert session.waiting() == 1


def test_a_worktree_whose_common_directory_lies_outside_it_gets_no_state(
    session: Session,
) -> None:
    """A folder whose git directory names a common directory elsewhere, as a worktree or an
    unpacked archive's `.git` does, never makes capture write there (design decision 18)."""
    tree = session.root / "tree"
    git(session.repo, session.env, "worktree", "add", "-q", str(tree))
    session.call(cwd=tree)
    assert (tree / ".pr-cost.json").exists()
    session.hook("Stop", cwd=tree)
    assert not (session.common_dir / "pr-cost-skeleton").exists()


def test_a_linked_ledger_folder_leaves_nothing_outside_the_repository(session: Session) -> None:
    outside = session.root / "outside"
    outside.mkdir()
    (session.repo / ".pr-cost").symlink_to(outside, target_is_directory=True)
    session.call()
    session.hook("Stop")
    session.change()
    session.commit()
    assert list(outside.iterdir()) == []
    assert session.ledger_files() == []
    assert session.log()[-2]["staged"] == "ledger_is_a_link"


@pytest.mark.parametrize("hook", ["refuses", "accepts"])
def test_a_relative_cd_settles_after_the_command_from_where_it_moved(
    session: Session, hook: str
) -> None:
    """Claude Code gives the hook after a command the folder the command moved to (A4)."""
    session.call()
    session.hook("Stop", cwd=session.root)
    session.change()
    if hook == "refuses":
        pre_commit = session.repo / ".git" / "hooks" / "pre-commit"
        pre_commit.write_text("#!/bin/sh\nexit 1\n")
        pre_commit.chmod(0o755)
    command = "cd clone && git add change.txt && git commit -m 'Change it'"
    session.bash("PreToolUse", command, session.root)
    done = subprocess.run(["bash", "-c", command], cwd=session.root, env=session.env)
    event = "PostToolUse" if done.returncode == 0 else "PostToolUseFailure"
    session.bash(event, command, session.repo)
    if hook == "refuses":
        assert session.log()[-1]["staged"] == "taken_back"
        assert session.staged() == ["change.txt"] and session.untracked_ledger() == []
        assert session.waiting() == 1
    else:
        assert session.log()[-1]["staged"] == "committed"
        assert len(session.ledger_files()) == 1 and session.waiting() == 0


@pytest.mark.parametrize("words", ["*.txt", "chan?e.txt", "[c]hange.txt", "{change,x}.txt"])
def test_a_word_that_the_shell_expands_is_not_recognised(session: Session, words: str) -> None:
    session.call()
    session.hook("Stop")
    session.change()
    session.commit(f"cd {session.repo} && git add {words} && git commit -m 'Change it'")
    assert session.log()[-2]["staged"] == "not_recognised"
    assert session.ledger_files() == []


def test_a_message_after_two_blanks_is_recognised(session: Session) -> None:
    session.call()
    session.hook("Stop")
    session.change()
    assert (
        session.commit(f"cd {session.repo} && git add change.txt && git commit -m  'Change it'")
        == 0
    )
    assert len(session.ledger_files()) == 1


def test_a_new_file_is_seen_whatever_the_person_shows_of_untracked_files(
    session: Session,
) -> None:
    with session.global_config.open("a") as out:
        out.write("[status]\n\tshowUntrackedFiles = no\n")
    session.call()
    session.hook("Stop")
    session.change()
    assert session.commit() == 0
    assert len(session.ledger_files()) == 1
