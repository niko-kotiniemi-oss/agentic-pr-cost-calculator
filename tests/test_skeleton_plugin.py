"""The walking skeleton's plugin, its hooks and the build of its zip, task 1.34 of
`add-pr-cost-calculator`. R239 and R243 in `project-standards`, and DR-245.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

import build_zip
import pytest
from test_backlog import AUTHOR
from test_repository import ROOT
from test_roadmap import isolated_environment, session_free_environment

SKELETON = ROOT / "skeleton"
COMMAND = 'python3 -I "${CLAUDE_PLUGIN_ROOT}/capture.py"; exit 0'
EVENTS = {"Stop", "SubagentStop", "SessionEnd", "PreToolUse", "PostToolUse", "PostToolUseFailure"}
TOOL_EVENTS = {"PreToolUse", "PostToolUse", "PostToolUseFailure"}
ZIP_NAMES = [".claude-plugin/plugin.json", "capture.py", "hooks/hooks.json"]


def manifest_problems(manifest: Any) -> list[str]:
    """What the manifest declares beyond its name, a version and a description (R243)."""
    if not isinstance(manifest, dict):
        return ["the manifest is not an object"]
    problems = [
        f"the manifest holds another key: {key}"
        for key in sorted(manifest)
        if key not in ("name", "version", "description")
    ]
    if manifest.get("name") != "pr-cost-skeleton":
        problems.append("the manifest's name is not pr-cost-skeleton")
    if not isinstance(manifest.get("version"), str) or not manifest.get("description"):
        problems.append("the manifest gives no version or no description")
    return problems


def hooks_problems(hooks: Any) -> list[str]:
    """Each hook that is not the guarded command hook for the events that the design names."""
    events = hooks.get("hooks") if isinstance(hooks, dict) and set(hooks) == {"hooks"} else None
    if not isinstance(events, dict):
        return ["the hooks file holds no hooks, or holds more than its hooks"]
    problems = []
    if set(events) != EVENTS:
        problems.append(f"the hooks are for other events: {sorted(events)}")
    for event, groups in sorted(events.items()):
        for number, group in enumerate(groups):
            where = f"{event} hook {number}"
            matcher = group.get("matcher")
            if matcher != ("Bash" if event in TOOL_EVENTS else None):
                problems.append(f"{where} matches {matcher!r}")
            for hook in group.get("hooks", []):
                if hook.get("type") != "command":
                    problems.append(
                        f"{where} is of another type than a command: {hook.get('type')}"
                    )
                elif hook.get("command") != COMMAND:
                    problems.append(f"{where} does not run python3 -I and end in ; exit 0")
            if set(group) - {"matcher", "hooks"} or not group.get("hooks"):
                problems.append(f"{where} declares more than its matcher and hooks, or no hook")
    return problems


def zip_problems(names: list[str]) -> list[str]:
    return [] if names == ZIP_NAMES else [f"the zip holds other files: {names}"]


def read(name: str) -> Any:
    return json.loads((SKELETON / name).read_text(encoding="utf-8"))


# ---- This repository ----


def test_the_skeletons_plugin_declares_nothing_but_its_command_hooks() -> None:
    assert manifest_problems(read("plugin.json")) == []
    assert hooks_problems(read("hooks.json")) == []


# ---- Planted ----


@pytest.mark.parametrize(
    ("change", "named"),
    [
        ({"mcpServers": {"x": {}}}, "mcpServers"),
        ({"hooks": "./hooks.json"}, "hooks"),
        ({"name": "pr-cost"}, "name"),
        ({"description": ""}, "description"),
    ],
)
def test_a_manifest_that_declares_more_fails(change: dict[str, Any], named: str) -> None:
    problems = manifest_problems({**read("plugin.json"), **change})
    assert problems and any(named in p for p in problems), problems


def planted_hooks(change: Any) -> list[str]:
    hooks = read("hooks.json")
    change(hooks["hooks"])
    return hooks_problems(hooks)


@pytest.mark.parametrize(
    ("change", "named"),
    [
        (lambda h: h["Stop"][0]["hooks"].append({"type": "prompt", "prompt": "x"}), "Stop hook 0"),
        (
            lambda h: h["PreToolUse"][0]["hooks"][0].update(command="python3 capture.py; exit 0"),
            "PreToolUse hook 0",
        ),
        (
            lambda h: h["Stop"][0]["hooks"][0].update(
                command='python3 -I "${CLAUDE_PLUGIN_ROOT}/capture.py"'
            ),
            "Stop hook 0",
        ),
        (lambda h: h["PostToolUse"][0].update(matcher="*"), "PostToolUse hook 0"),
        (lambda h: h.update(UserPromptSubmit=h["Stop"]), "other events"),
        (lambda h: h.pop("SessionEnd"), "other events"),
        (lambda h: h["Stop"][0].update(timeout=1), "Stop hook 0"),
    ],
)
def test_a_hook_of_another_type_or_without_its_guard_fails(change: Any, named: str) -> None:
    problems = planted_hooks(change)
    assert problems and any(named in p for p in problems), problems


def test_a_hooks_file_with_more_than_its_hooks_fails() -> None:
    assert hooks_problems({**read("hooks.json"), "mcpServers": {}}) != []
    assert hooks_problems([]) != []


def test_a_zip_that_holds_another_file_fails() -> None:
    assert zip_problems([*ZIP_NAMES, ".mcp.json"]) != []
    assert zip_problems(ZIP_NAMES) == []


# ---- The hook command never stalls or steers (R239) ----


def run_hook(root: Path, payload: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "-c", COMMAND.replace("python3", sys.executable, 1)],
        input=payload,
        env={**session_free_environment(), "CLAUDE_PLUGIN_ROOT": str(root)},
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize(
    "script", [None, "raise RuntimeError('planted')\n", "import sys\nsys.exit(2)\n"]
)
def test_a_hook_exits_with_success_and_prints_nothing_whatever_its_script_does(
    tmp_path: Path, script: str | None
) -> None:
    if script is not None:
        (tmp_path / "capture.py").write_text(script)
    done = run_hook(tmp_path, "{}")
    assert done.returncode == 0 and done.stdout == ""


def test_the_real_capture_script_under_its_hook_prints_nothing(tmp_path: Path) -> None:
    shutil.copy(SKELETON / "capture.py", tmp_path / "capture.py")
    for payload in ("not json", json.dumps({"hook_event_name": "Stop", "cwd": str(tmp_path)})):
        done = run_hook(tmp_path, payload)
        assert done.returncode == 0 and done.stdout == ""


# ---- The zip, built from git's objects ----


def repository_with_skeleton(root: Path) -> tuple[Path, dict[str, str]]:
    repo = root / "repo"
    shutil.copytree(SKELETON, repo / "skeleton", ignore=shutil.ignore_patterns("__pycache__"))
    env = {**isolated_environment(repo), **AUTHOR}
    for args in (["init", "-q", "-b", "main"], ["add", "-A"], ["commit", "-q", "-m", "Skeleton"]):
        subprocess.run(["git", *args], cwd=repo, env=env, check=True, capture_output=True)
    return repo, env


def test_two_builds_of_one_commit_give_the_same_zip(tmp_path: Path) -> None:
    repo, env = repository_with_skeleton(tmp_path)
    outputs = []
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, env=env, capture_output=True, text=True, check=True
    ).stdout.strip()
    for name in ("one.zip", "two.zip"):
        done = subprocess.run(
            [sys.executable, "-I", str(SKELETON / "build_zip.py"), commit, str(tmp_path / name)],
            cwd=repo,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        outputs.append(done.stdout)
    one, two = (tmp_path / "one.zip").read_bytes(), (tmp_path / "two.zip").read_bytes()
    assert one == two
    assert outputs[0] == outputs[1]
    named, digest = outputs[0].split()
    assert named == commit and len(digest) == 64
    with zipfile.ZipFile(tmp_path / "one.zip") as built:
        assert zip_problems(built.namelist()) == []
        assert all(info.compress_type == zipfile.ZIP_STORED for info in built.infolist())
        assert built.read("capture.py") == (SKELETON / "capture.py").read_bytes()
        assert json.loads(built.read(".claude-plugin/plugin.json")) == read("plugin.json")
        assert json.loads(built.read("hooks/hooks.json")) == read("hooks.json")


def test_the_zip_holds_the_commits_files_not_the_working_trees(tmp_path: Path) -> None:
    repo, env = repository_with_skeleton(tmp_path)
    (repo / "skeleton" / "capture.py").write_text("# changed after the commit\n")
    (repo / "skeleton" / ".mcp.json").write_text("{}")
    built = build_zip.build(repo, "HEAD", env)
    with zipfile.ZipFile(built) as archive:
        assert archive.namelist() == ZIP_NAMES
        assert archive.read("capture.py") == (SKELETON / "capture.py").read_bytes()


def test_a_commit_that_does_not_exist_builds_nothing(tmp_path: Path) -> None:
    repo, env = repository_with_skeleton(tmp_path)
    with pytest.raises(subprocess.CalledProcessError):
        build_zip.build(repo, "no-such-commit", env)


@pytest.mark.parametrize("revision", ["HEAD", "main", "abc1234"])
def test_a_revision_that_can_move_or_is_short_is_refused(tmp_path: Path, revision: str) -> None:
    repo, env = repository_with_skeleton(tmp_path)
    done = subprocess.run(
        [sys.executable, "-I", str(SKELETON / "build_zip.py"), revision, str(tmp_path / "x.zip")],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert done.returncode != 0 and not (tmp_path / "x.zip").exists()
    assert "full commit" in done.stderr


def test_a_replace_ref_never_changes_what_the_zip_holds(tmp_path: Path) -> None:
    """The zip holds the named commit's own bytes, whatever the clone's replace refs say."""
    repo, env = repository_with_skeleton(tmp_path)
    other = tmp_path / "other.py"
    other.write_text("# not the reviewed script\n")

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=repo, env=env, capture_output=True, text=True, check=True
        ).stdout.strip()

    git(
        "replace",
        git("rev-parse", "HEAD:skeleton/capture.py"),
        git("hash-object", "-w", str(other)),
    )
    with zipfile.ZipFile(build_zip.build(repo, git("rev-parse", "HEAD"), env)) as archive:
        assert archive.read("capture.py") == (SKELETON / "capture.py").read_bytes()
