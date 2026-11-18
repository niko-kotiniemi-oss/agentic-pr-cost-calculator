#!/usr/bin/env python3
# The walking skeleton of the agentic PR cost calculator: not the tool or a release.
# It runs the thinnest path once, in a scratch repository, and the build replaces it (design
# decision 18 of `add-pr-cost-calculator`). It records a call only with the skeleton's own switch
# and the person's opt-in (R235), never stalls or steers the agent (R239), and stages a ledger
# file only for a commit it recognises (R240). Python's standard library only.
"""Capture for the walking skeleton, run by its plugin's hooks with the hook's input on stdin."""

from __future__ import annotations

import functools
import hashlib
import json
import os
import re
import secrets
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

STOP_EVENTS = frozenset({"Stop", "SubagentStop", "SessionEnd"})
TOOL_EVENTS = frozenset({"PreToolUse", "PostToolUse", "PostToolUseFailure"})
COUNTS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
MODEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:@-]{0,99}")
STATE = "pr-cost-skeleton"
# The skeleton's own opt-in, which the tool's opt-in, `pr-cost.capture`, never stands in for.
OPT_IN = "pr-cost-skeleton.capture"
LEDGER = ".pr-cost/ledger"


def git_environment() -> dict[str, str]:
    """The environment without the session's git variables, but with its `GIT_CONFIG_` ones."""
    return {
        key: value
        for key, value in os.environ.items()
        if not key.startswith("GIT_") or key.startswith("GIT_CONFIG")
    }


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=cwd, env=git_environment(), capture_output=True, text=True
    )


def toplevel(folder: Path) -> Path | None:
    if not folder.is_dir():
        return None
    done = git(folder, "rev-parse", "--show-toplevel")
    return Path(done.stdout.strip()).resolve() if done.returncode == 0 else None


def repositories(cwd: Path) -> list[Path]:
    """The repository that holds the folder or, where none does, each one directly inside it."""
    top = toplevel(cwd)
    if top or not cwd.is_dir():
        return [top] if top else []
    found = [toplevel(child) for child in sorted(cwd.iterdir()) if (child / ".git").exists()]
    return [top for top in found if top is not None and top.parent == cwd.resolve()]


def switch_on(repo: Path) -> bool:
    """The skeleton's own switch: `enabled` and `walking_skeleton` both `true` (R235)."""
    try:
        data = json.loads((repo / ".pr-cost.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return (
        isinstance(data, dict)
        and data.get("enabled") is True
        and data.get("walking_skeleton") is True
    )


def opted_in(repo: Path) -> bool:
    """The skeleton's opt-in, from the person's global files alone (R235). It is read without
    the session's git variables or `XDG_CONFIG_HOME`, should a repository's settings reach them
    (A5), with each value whole, so that a repository's own value is never read as a global
    one, and without asking git for a boolean, which one bad value anywhere would stop. A key
    written with no value, which git reads as true, is not taken: it fails toward not recording."""
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith("GIT_") and key != "XDG_CONFIG_HOME"
    }
    done = subprocess.run(
        ["git", "config", "--null", "--show-scope", "--get-all", OPT_IN],
        cwd=repo,
        env=environment,
        capture_output=True,
        text=True,
    )
    fields = done.stdout.split("\0")
    values = [
        value.strip().lower()
        for scope, value in zip(fields[0::2], fields[1::2], strict=False)
        if scope == "global"
    ]
    return bool(values) and is_true(values[-1])


def is_true(value: str) -> bool:
    """Whether git reads a written value as true."""
    if value in ("true", "yes", "on"):
        return True
    try:
        return int(value) != 0
    except ValueError:
        return False


# ---- The commands it recognises (R240) ----


@dataclass
class Commit:
    folder: Path
    adds: list[tuple[Path, list[str]]] = field(default_factory=list)
    all_tracked: bool = False


def written(folder: Path, path: str) -> Path | None:
    """A folder as a command writes it, or None for a form the skeleton leaves out."""
    return None if path.startswith(("-", "~")) else Path(os.path.normpath(folder / path))


def git_part(tokens: list[str], folder: Path) -> tuple[Path, str, list[str]] | None:
    """A git command's folder, with at most one written `-C`, its subcommand and its arguments."""
    if not tokens or tokens[0] != "git":
        return None
    rest = tokens[1:]
    if rest[:1] == ["-C"]:
        given = written(folder, rest[1]) if len(rest) > 1 else None
        if given is None:
            return None
        folder, rest = given, rest[2:]
    return (folder, rest[0], rest[1:]) if rest else None


def commit_options(args: list[str]) -> bool | None:
    """Whether the commit's options hold `-a`, or None when they are not only `-m`, `-a`, `-q`."""
    all_tracked, message, index = False, False, 0
    while index < len(args):
        option = args[index]
        if option == "-m" and index + 1 < len(args):
            message, index = True, index + 2
            continue
        if option not in ("-a", "-q"):
            return None
        all_tracked, index = all_tracked or option == "-a", index + 1
    return all_tracked if message else None


def recognised(command: str, cwd: Path) -> Commit | None:
    """The commit that a command makes, when the skeleton recognises its form, or None."""
    # With no `$`, backtick or backslash, a quoted span ends at its next quote, so a message's
    # own text is left out of the search for a message that is not quoted.
    unquoted = re.sub(r"'[^']*'|\"[^\"]*\"", "''", command)
    if (
        any(c in command for c in "$`\\\n\r")
        or re.search(r"(^|\s)-m\s+(?![\s'\"])", unquoted)
        # A word that the shell would expand, which git would read as a pathspec of its own.
        or re.search(r"[*?\[{]|(^|\s)~", unquoted)
    ):
        return None
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return None
    parts: list[list[str]] = [[]]
    for token in tokens:
        if token == "&&":
            parts.append([])
        elif token and set(token) <= set("();<>|&"):
            return None
        else:
            parts[-1].append(token)
    if any(not part for part in parts):
        return None
    folder, adds = cwd, []
    for part in parts[:-1]:
        if part[0] == "cd" and len(part) == 2:
            given = written(folder, part[1])
            if given is None:
                return None
            folder = given
            continue
        add = git_part(part, folder)
        if not add or add[1] != "add" or not add[2] or any(p.startswith("-") for p in add[2]):
            return None
        adds.append((add[0], add[2]))
    last = git_part(parts[-1], folder)
    if not last or last[1] != "commit":
        return None
    all_tracked = commit_options(last[2])
    return None if all_tracked is None else Commit(last[0], adds, all_tracked)


# ---- Transcripts ----


@dataclass
class Reading:
    transcripts: int = 0
    lines: int = 0
    unread: int = 0
    kept: int = 0
    without_stop_reason: int = 0
    outside: int = 0
    incomplete: int = 0
    differing: int = 0


def transcripts(payload: dict[str, Any]) -> list[Path]:
    """The session's transcript, its subagents' transcripts and any that the input names."""
    paths: list[Path] = []
    main = payload.get("transcript_path")
    if isinstance(main, str) and main:
        paths.append(Path(main))
        paths += sorted((Path(main).with_suffix("") / "subagents").glob("*.jsonl"))
    given = payload.get("agent_transcript_path")
    if isinstance(given, str) and given:
        paths.append(Path(given))
    return list(dict.fromkeys(paths))


def count(usage: dict[str, Any], name: str) -> int:
    value = usage.get(name, 0)
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else 0


@functools.cache
def in_working_tree(cwd: str, repo: Path) -> bool:
    """Whether an absolute folder lies in the repository's working tree, and in no repository
    inside it; asked once for each folder that a session's lines give."""
    if not Path(cwd).is_absolute():
        return False
    folder = Path(cwd).resolve()
    if not folder.is_relative_to(repo):
        return False
    return not any(
        (above / ".git").exists()
        for above in [folder, *folder.parents]
        if above != repo and above.is_relative_to(repo)
    )


def call_of(line: dict[str, Any], message: dict[str, Any], repo: Path) -> tuple[str, Any]:
    """A call's key and its kept fields, from a line that gives a stop reason, in the repository;
    or, for a call it leaves out, why: `outside` the repository or `incomplete`."""
    cwd, model, usage = line.get("cwd"), message.get("model"), message.get("usage")
    if not isinstance(cwd, str) or not in_working_tree(cwd, repo):
        return "outside", None
    if not isinstance(model, str) or not MODEL.fullmatch(model) or not isinstance(usage, dict):
        return "incomplete", None
    try:
        stamp = datetime.fromisoformat(str(line.get("timestamp")).replace("Z", "+00:00"))
        day = stamp.astimezone(UTC).date().isoformat()
    except ValueError:
        return "incomplete", None
    key = hashlib.sha256(str(message["id"]).encode()).hexdigest()
    return key, {"model": model, "day": day, **{name: count(usage, name) for name in COUNTS}}


def read_calls(paths: list[Path], repo: Path, store: dict[str, Any], reading: Reading) -> None:
    """Add each new call in the transcripts to the calls waiting, from complete lines only."""
    with_stop, without_stop = set(), set()
    left_out: dict[str, set[str]] = {"outside": set(), "incomplete": set()}
    usages: dict[str, Any] = {}
    differing = set()
    known = set(store["recorded"]) | set(store["waiting"])
    for path in paths:
        try:
            data = path.read_bytes()
        except OSError:
            continue
        reading.transcripts += 1
        for raw in data.split(b"\n")[:-1]:
            reading.lines += 1
            try:
                line = json.loads(raw.decode("utf-8"))
            except ValueError:
                reading.unread += 1
                continue
            message = line.get("message") if isinstance(line, dict) else None
            if not isinstance(message, dict) or not isinstance(message.get("id"), str):
                continue
            if message.get("stop_reason") is None:
                without_stop.add(message["id"])
                continue
            with_stop.add(message["id"])
            if usages.setdefault(message["id"], message.get("usage")) != message.get("usage"):
                differing.add(message["id"])
            key, call = call_of(line, message, repo)
            if call is None:
                left_out[key].add(message["id"])
            elif key not in known:
                known.add(key)
                store["waiting"][key] = call
                reading.kept += 1
    reading.without_stop_reason = len(without_stop - with_stop)
    reading.outside = len(left_out["outside"])
    reading.incomplete = len(left_out["incomplete"])
    reading.differing = len(differing)


# ---- The store, the ledger file and the log ----


def load_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"waiting": {}, "recorded": [], "staged": None}
    store = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(store, dict) or set(store) != {"waiting", "recorded", "staged"}:
        raise ValueError("the store is not the skeleton's")
    return store


def save(path: Path, text: str) -> None:
    """Write a file whole, by renaming a temporary file into place."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{secrets.token_hex(8)}")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def would_commit(commit: Commit) -> bool:
    """Whether the commit would commit something without the ledger file."""
    if git(commit.folder, "diff", "--cached", "--quiet").returncode == 1:
        return True
    if commit.all_tracked and git(commit.folder, "diff", "--quiet").returncode == 1:
        return True
    return any(
        git(folder, "status", "--porcelain", "--untracked-files=all", "--", *paths).stdout.strip()
        for folder, paths in commit.adds
    )


def stage(repo: Path, commit: Commit, store: dict[str, Any], command: str) -> str:
    """Write the calls waiting into one new ledger file and stage it; say what was done."""
    if not store["waiting"]:
        return "nothing_waiting"
    if not would_commit(commit):
        return "nothing_to_commit"
    month = datetime.now(UTC).strftime("%Y-%m")
    if (repo / LEDGER / month).resolve() != repo / LEDGER / month:
        return "ledger_is_a_link"
    relative = f"{LEDGER}/{month}/{secrets.token_hex(16)}.jsonl"
    lines = [
        json.dumps({"key": key, **call}, sort_keys=True, separators=(",", ":"))
        for key, call in sorted(store["waiting"].items())
    ]
    save(repo / relative, "\n".join(lines) + "\n")
    if git(repo, "add", "--", relative).returncode != 0:
        (repo / relative).unlink()
        return "add_failed"
    # The command's hash, not its text, which may hold the commit's message.
    digest = hashlib.sha256(command.encode()).hexdigest()
    store["staged"] = {"path": relative, "keys": sorted(store["waiting"]), "command": digest}
    return "staged"


def settle(repo: Path, store: dict[str, Any]) -> str:
    """After the command: record the calls of a committed file, or take an uncommitted one back."""
    staged = store["staged"]
    store["staged"] = None
    if git(repo, "ls-tree", "--name-only", "HEAD", "--", staged["path"]).stdout.strip():
        store["recorded"] += staged["keys"]
        for key in staged["keys"]:
            store["waiting"].pop(key, None)
        return "committed"
    git(repo, "rm", "--cached", "--quiet", "--ignore-unmatch", "--", staged["path"])
    (repo / staged["path"]).unlink(missing_ok=True)
    return "taken_back"


def own_hash() -> str:
    """The SHA-256 of this script as it runs, so that the run can tell which copy ran."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def ours(repo: Path, commit: Commit) -> bool:
    """Whether the commit and each of its adds are in this repository."""
    return all(toplevel(f) == repo for f in [commit.folder, *(f for f, _ in commit.adds)])


def handle(repo: Path, payload: dict[str, Any], event: str, commit: Commit | None) -> None:
    """Capture for one repository, with one line in its log."""
    if not switch_on(repo):
        return
    common = (repo / git(repo, "rev-parse", "--git-common-dir").stdout.strip()).resolve()
    if not common.is_relative_to(repo):
        return
    state = common / STATE
    reading = Reading()
    entry: dict[str, Any] = {
        "event": event,
        "capture_sha256": own_hash(),
        "opt_in": opted_in(repo),
        "staged": None,
        "error": None,
    }
    try:
        if not entry["opt_in"]:
            return
        try:
            store = load_store(state / "store.json")
        except ValueError:
            print("pr-cost-skeleton: the store could not be read", file=sys.stderr)
            raise
        read_calls(transcripts(payload), repo, store, reading)
        command = str((payload.get("tool_input") or {}).get("command", ""))
        digest = hashlib.sha256(command.encode()).hexdigest()
        if event == "PreToolUse" and commit and ours(repo, commit):
            if store["staged"]:
                settle(repo, store)
            entry["staged"] = stage(repo, commit, store, command)
        elif event == "PreToolUse" and not commit and re.search(r"\bcommit\b", command):
            entry["staged"] = "not_recognised"
        # After the command, the hook's folder may be where the command moved to (A4), so the
        # command is matched as written, not resolved again.
        elif event in ("PostToolUse", "PostToolUseFailure") and (
            store["staged"] and store["staged"].get("command") == digest
        ):
            entry["staged"] = settle(repo, store)
        save(state / "store.json", json.dumps(store, sort_keys=True))
    except Exception as error:  # noqa: BLE001 - the skeleton never stalls the agent (R239)
        entry["error"] = type(error).__name__
        if not isinstance(error, ValueError):
            print(f"pr-cost-skeleton: {type(error).__name__}", file=sys.stderr)
    finally:
        entry.update(
            transcripts_read=reading.transcripts,
            lines_read=reading.lines,
            lines_unread=reading.unread,
            calls_kept=reading.kept,
            calls_without_stop_reason=reading.without_stop_reason,
            calls_outside=reading.outside,
            calls_incomplete=reading.incomplete,
            calls_differing=reading.differing,
        )
        state.mkdir(parents=True, exist_ok=True)
        with (state / "log.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps(entry, sort_keys=True) + "\n")


def run(raw: str) -> None:
    payload = json.loads(raw)
    if not isinstance(payload, dict) or not isinstance(payload.get("cwd"), str):
        return
    event = payload.get("hook_event_name")
    if event not in STOP_EVENTS | TOOL_EVENTS:
        return
    cwd = Path(payload["cwd"])
    commit = None
    if event in TOOL_EVENTS:
        command = (payload.get("tool_input") or {}).get("command")
        if payload.get("tool_name") != "Bash" or not isinstance(command, str):
            return
        if not re.search(r"\bgit\b", command):
            return
        # Only the hook before a command resolves it; the one after matches it as written.
        commit = recognised(command, cwd) if event == "PreToolUse" else None
    for repo in repositories(cwd):
        handle(repo, payload, str(event), commit)


def main() -> int:
    try:
        run(sys.stdin.read())
    except Exception as error:  # noqa: BLE001 - the skeleton never stalls the agent (R239)
        print(f"pr-cost-skeleton: {type(error).__name__}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
