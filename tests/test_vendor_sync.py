"""The vendor sync takes only the commit that its lock's tag names, and copies
it as git's objects hold it.

Upstream serves commits that no release contains, such as those of its open
pull requests, and a fetch by commit id takes any of them. A lock pointing at
one would pass a check that compares the vendored tree with that commit, so the
sync also requires the lock's tag to name the lock's commit.

The sync writes each vendored file with the bytes and the mode that the pinned
commit's objects give it, whatever the person's git converts, reads its lock
with each carriage return before a line feed taken as a line feed, and its
check compares every path below the vendored root with that commit's, leaving
out the lock at the root alone, by its path (R275, DR-275, DR-281).

These tests run the real script against a local upstream, never the network,
with no git variable of the session's and no global or system configuration
but what a test plants.
"""

from __future__ import annotations

import re
import shutil
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest
from test_roadmap import GIT_ENVIRONMENT, session_free_environment

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sync-superpowers.sh"
VENDORED = [".claude-plugin/plugin.json", "skills/a/SKILL.md", "hooks/run-hook.cmd"]
VENDORED += ["hooks/session-start", "LICENSE"]
# What upstream's release gives each file, with line feeds; the start hook's text is one that
# `export-subst` would rewrite.
RELEASED = {path: f"{path}, as released\n" for path in VENDORED}
RELEASED["hooks/session-start"] += "at $Format:%H$\n"
EXECUTABLE = {"hooks/run-hook.cmd", "hooks/session-start"}
# Upstream's own attributes, each of which `git archive` would follow.
UPSTREAM_ATTRIBUTES = (
    "* eol=crlf\nhooks/session-start export-subst\nskills/a/SKILL.md export-ignore\n"
)
IDENTITY = {
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.invalid",
}


@dataclass(frozen=True)
class World:
    repo: Path
    remotes: Path
    tagged: str
    untagged: str


def isolated() -> dict[str, str]:
    """The environment with no git variable of the session's and no global or system
    configuration."""
    return {**session_free_environment(), **GIT_ENVIRONMENT}


def git(*args: str, cwd: Path, stdin: str | None = None) -> str:
    done = subprocess.run(
        ["git", *args],
        cwd=cwd,
        input=stdin,
        env={**isolated(), **IDENTITY},
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout.strip()


def build_world(tmp_path: Path, attributes: str | None = None) -> World:
    """An upstream with a tagged release and a later commit that no release contains, a
    bare copy that the sync fetches from, and a repository that holds the script, with
    upstream's own attributes where given."""
    work = tmp_path / "upstream"
    work.mkdir()
    git("init", "-q", "-b", "main", cwd=work)
    for path in VENDORED:
        (work / path).parent.mkdir(parents=True, exist_ok=True)
        (work / path).write_bytes(RELEASED[path].encode("utf-8"))
        if path in EXECUTABLE:
            (work / path).chmod(0o755)
    if attributes is not None:
        (work / ".gitattributes").write_bytes(attributes.encode("utf-8"))
    git("add", "-A", cwd=work)
    git("commit", "-q", "-m", "release", cwd=work)
    tagged = git("rev-parse", "HEAD", cwd=work)
    git("tag", "-a", "v1.0.0", "-m", "v1.0.0", cwd=work)
    git("tag", "v1.0.0-light", cwd=work)
    (work / "skills/a/SKILL.md").write_bytes(b"changed in a commit no release contains\n")
    git("commit", "-q", "-a", "-m", "not released", cwd=work)
    untagged = git("rev-parse", "HEAD", cwd=work)

    remotes = tmp_path / "remotes"
    bare = remotes / "owner" / "superpowers.git"
    bare.parent.mkdir(parents=True)
    git("clone", "-q", "--bare", str(work), str(bare), cwd=tmp_path)
    git("config", "uploadpack.allowFilter", "true", cwd=bare)
    git("config", "uploadpack.allowAnySHA1InWant", "true", cwd=bare)

    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    shutil.copy(SCRIPT, repo / "scripts" / SCRIPT.name)
    (repo / "vendor" / "superpowers").mkdir(parents=True)
    return World(repo, remotes, tagged, untagged)


@pytest.fixture
def world(tmp_path: Path) -> World:
    return build_world(tmp_path)


def sync(
    world: World,
    sha: str,
    tag: str,
    *args: str,
    environment: dict[str, str] | None = None,
    ending: str = "\n",
    extra: str = "",
) -> subprocess.CompletedProcess[str]:
    """The script run with a lock that pins this commit and tag, each of its lines ending
    as given, and these lines after them, in an environment with only what is given."""
    lock = world.repo / "vendor" / "superpowers" / "UPSTREAM.lock"
    lines = (f"repo=owner/superpowers{ending}sha={sha}{ending}tag={tag}{ending}{extra}").encode()
    lock.write_bytes(lines)
    return subprocess.run(
        ["bash", str(world.repo / "scripts" / SCRIPT.name), *args],
        env={**isolated(), "SYNC_REMOTE_BASE": world.remotes.as_uri(), **(environment or {})},
        capture_output=True,
        text=True,
    )


def test_the_commit_the_tag_names_syncs_and_checks(world: World) -> None:
    synced = sync(world, world.tagged, "v1.0.0")
    assert synced.returncode == 0, synced.stderr
    checked = sync(world, world.tagged, "v1.0.0", "--check")
    assert checked.returncode == 0, checked.stderr
    vendored = world.repo / "vendor" / "superpowers" / "skills/a/SKILL.md"
    assert vendored.read_text() == "skills/a/SKILL.md, as released\n"


def test_syncing_a_commit_the_tag_does_not_name_is_refused(world: World) -> None:
    done = sync(world, world.untagged, "v1.0.0")
    assert done.returncode == 1
    assert f"tag v1.0.0 of owner/superpowers names {world.tagged}, not {world.untagged}" in (
        done.stderr
    )
    assert not (world.repo / "vendor" / "superpowers" / "skills").exists()


def test_a_tree_vendored_from_a_commit_the_tag_does_not_name_fails_the_check(
    world: World,
) -> None:
    # The tree matches its commit exactly, so only the tag rule can catch it.
    bare = world.remotes / "owner" / "superpowers.git"
    archive = subprocess.run(
        ["git", "archive", world.untagged], cwd=bare, check=True, capture_output=True
    ).stdout
    dest = world.repo / "vendor" / "superpowers"
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)
    done = sync(world, world.untagged, "v1.0.0", "--check")
    assert done.returncode == 1
    assert f"tag v1.0.0 of owner/superpowers names {world.tagged}, not {world.untagged}" in (
        done.stderr
    )


def test_a_lightweight_tag_names_its_commit_directly(world: World) -> None:
    assert sync(world, world.tagged, "v1.0.0-light").returncode == 0
    refused = sync(world, world.untagged, "v1.0.0-light", "--check")
    assert refused.returncode == 1
    assert f"names {world.tagged}, not {world.untagged}" in refused.stderr


def test_a_tag_upstream_does_not_have_is_refused(world: World) -> None:
    done = sync(world, world.tagged, "v9.9.9", "--check")
    assert done.returncode == 1
    assert "tag v9.9.9 of owner/superpowers names nothing" in done.stderr


def test_an_edited_vendored_file_fails_the_check(world: World) -> None:
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    (world.repo / "vendor" / "superpowers" / "LICENSE").write_text("edited by hand\n")
    done = sync(world, world.tagged, "v1.0.0", "--check")
    assert done.returncode == 1
    assert "DIFFERS" in done.stderr


# R275: the check compares every path below the vendored root with the pinned commit's.


@pytest.mark.parametrize(
    ("path", "named"),
    [
        ("skills/a/UPSTREAM.lock", "vendor/superpowers/skills/a: UPSTREAM.lock"),
        ("skills/UPSTREAM.lock/SKILL.md", "vendor/superpowers/skills: UPSTREAM.lock"),
    ],
)
def test_a_path_named_as_the_lock_below_the_vendored_root_fails_the_check(
    world: World, path: str, named: str
) -> None:
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    planted = world.repo / "vendor" / "superpowers" / path
    planted.parent.mkdir(parents=True, exist_ok=True)
    planted.write_bytes(b"Not upstream's.\n")
    done = sync(world, world.tagged, "v1.0.0", "--check")
    assert done.returncode == 1
    assert "DIFFERS" in done.stderr
    assert named in done.stderr


def test_the_check_passes_the_pinned_copy_whatever_the_root_lock_holds(world: World) -> None:
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    extra = "# A line of ours.\nvendored_at=2026-11-22\nanything=else\n"
    done = sync(world, world.tagged, "v1.0.0", "--check", extra=extra)
    assert done.returncode == 0, done.stderr


# R275: the sync copies the pinned commit's bytes whatever the person's git converts.

CONDITIONS = (
    "no condition",
    "a global core.autocrlf",
    "a template's info/attributes",
    "a lock with Windows line endings",
    "upstream's own attributes",
)


def prepared(tmp_path: Path, case: str) -> tuple[World, dict[str, str], str]:
    """A world, the environment that the sync runs in and how its lock's lines end, for the
    case: a global configuration that sets `core.autocrlf` to `true`, one whose template
    gives each new clone a `.git/info/attributes` that holds `* eol=crlf`, a lock whose
    lines end in CRLF, or an upstream whose own attributes `git archive` would follow."""
    world = build_world(
        tmp_path, UPSTREAM_ATTRIBUTES if case == "upstream's own attributes" else None
    )
    configuration = tmp_path / "gitconfig"
    if case == "a global core.autocrlf":
        configuration.write_bytes(b"[core]\n\tautocrlf = true\n")
    elif case == "a template's info/attributes":
        template = tmp_path / "template"
        (template / "info").mkdir(parents=True)
        (template / "info" / "attributes").write_bytes(b"* eol=crlf\n")
        configuration.write_bytes(f"[init]\n\ttemplateDir = {template}\n".encode())
    environment = {"GIT_CONFIG_GLOBAL": str(configuration)} if configuration.exists() else {}
    return world, environment, "\r\n" if case == "a lock with Windows line endings" else "\n"


def released(world: World) -> dict[str, tuple[int, bytes]]:
    """Each vendored file of the tagged commit by its path, with the mode and the bytes that
    git's objects give it."""
    bare = world.remotes / "owner" / "superpowers.git"
    listing = git("ls-tree", "-r", "-z", world.tagged, cwd=bare)
    given: dict[str, tuple[int, bytes]] = {}
    for entry in filter(None, listing.split("\0")):
        meta, path = entry.split("\t", 1)
        mode, _, oid = meta.split()
        if path in VENDORED:
            data = subprocess.run(
                ["git", "cat-file", "blob", oid],
                cwd=bare,
                env=isolated(),
                check=True,
                capture_output=True,
            ).stdout
            given[path] = (0o755 if mode == "100755" else 0o644, data)
    assert sorted(given) == sorted(VENDORED)
    return given


def vendored(world: World) -> dict[str, tuple[int, bytes]]:
    """Each file below the vendored root but the lock at the root, by its path, with its mode
    and its bytes."""
    root = world.repo / "vendor" / "superpowers"
    return {
        path.relative_to(root).as_posix(): (stat.S_IMODE(path.stat().st_mode), path.read_bytes())
        for path in root.rglob("*")
        if path.is_file() and path != root / "UPSTREAM.lock"
    }


@pytest.mark.parametrize("case", CONDITIONS)
def test_the_refresh_writes_and_the_check_passes_the_pinned_commit_s_bytes_and_modes(
    tmp_path: Path, case: str
) -> None:
    world, environment, ending = prepared(tmp_path, case)
    synced = sync(world, world.tagged, "v1.0.0", environment=environment, ending=ending)
    assert synced.returncode == 0, synced.stderr
    assert vendored(world) == released(world)
    checked = sync(world, world.tagged, "v1.0.0", "--check", environment=environment, ending=ending)
    assert checked.returncode == 0, checked.stderr


@pytest.mark.parametrize("case", CONDITIONS)
def test_the_check_passes_the_pinned_copy_and_fails_one_whose_line_endings_alone_differ(
    tmp_path: Path, case: str
) -> None:
    world, environment, ending = prepared(tmp_path, case)
    root = world.repo / "vendor" / "superpowers"
    given = released(world)
    for path, (mode, data) in given.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_bytes(data)
        (root / path).chmod(mode)
    passed = sync(world, world.tagged, "v1.0.0", "--check", environment=environment, ending=ending)
    assert passed.returncode == 0, passed.stderr
    (root / "LICENSE").write_bytes(given["LICENSE"][1].replace(b"\n", b"\r\n"))
    failed = sync(world, world.tagged, "v1.0.0", "--check", environment=environment, ending=ending)
    assert failed.returncode == 1
    assert "DIFFERS" in failed.stderr
    assert "vendor/superpowers/LICENSE" in failed.stderr


# R275: the sync writes only files, each with the mode that the pinned commit gives it, and
# only inside the folder that it writes the copy into.


def craft(
    world: World, folder: str, added: tuple[str, ...] = (), dropped: tuple[str, ...] = ()
) -> str:
    """A commit after the tagged release, tagged v2.0.0 in the bare upstream, whose folder
    holds the release's entries but those dropped, by name, and the entries added, as git's
    tree listing gives them, which no index could stage; its id."""
    bare = world.remotes / "owner" / "superpowers.git"
    kept = [
        line
        for line in git("ls-tree", f"{world.tagged}:{folder}", cwd=bare).splitlines()
        if line.split("\t", 1)[1] not in dropped
    ]
    inner = git("mktree", cwd=bare, stdin="".join(f"{line}\n" for line in [*kept, *added]))
    top = [
        line
        for line in git("ls-tree", world.tagged, cwd=bare).splitlines()
        if line.split("\t", 1)[1] != folder
    ]
    listing = [*top, f"040000 tree {inner}\t{folder}"]
    tree = git("mktree", cwd=bare, stdin="".join(f"{line}\n" for line in listing))
    commit = git("commit-tree", "-p", world.tagged, "-m", "crafted", tree, cwd=bare)
    git("tag", "-a", "v2.0.0", "-m", "v2.0.0", commit, cwd=bare)
    return commit


def entry(world: World, case: str) -> tuple[str, str]:
    """An entry of the skills folder that the sync refuses, as git's tree listing gives it,
    and what the sync says of it."""
    bare = world.remotes / "owner" / "superpowers.git"

    def blob(text: str) -> str:
        return git("hash-object", "-w", "--stdin", cwd=bare, stdin=text)

    def tree(line: str) -> str:
        return git("mktree", cwd=bare, stdin=f"{line}\n")

    if case == "a path up out of the copy":
        escaped = blob("Escaped.\n")
        inner = tree(f"100644 blob {escaped}\toutside")
        for _ in range(2):
            inner = tree(f"040000 tree {inner}\t..")
        path = "skills/../../../outside"
        return f"040000 tree {inner}\t..", f"gives the path {path}, which the sync does not write"
    if case == "a path through a dot":
        hidden = blob("Hidden.\n")
        inner = tree(f"100644 blob {hidden}\ta.md")
        return (
            f"040000 tree {inner}\t.",
            "gives the path skills/./a.md, which the sync does not write",
        )
    if case in ("a folder named .git", "a folder named .GiT"):
        name = case.rsplit(" ", 1)[1]
        config = blob("[core]\n\tfsmonitor = a command of upstream's\n")
        inner = tree(f"100644 blob {config}\tconfig")
        path = f"skills/{name}/config"
        return (
            f"040000 tree {inner}\t{name}",
            f"gives the path {path}, which the sync does not write",
        )
    if case == "a link":
        link = blob("../../../outside")
        return f"120000 blob {link}\tlink", "gives skills/link the mode 120000, which the sync"
    return f"160000 commit {world.untagged}\tsub", "gives skills/sub the mode 160000, which"


ENTRIES = (
    "a path up out of the copy",
    "a path through a dot",
    "a folder named .git",
    "a folder named .GiT",
    "a link",
    "a submodule",
)


@pytest.mark.parametrize("args", [(), ("--check",)], ids=["refresh", "check"])
@pytest.mark.parametrize("case", ENTRIES)
def test_the_sync_refuses_an_entry_that_is_not_a_file_inside_its_copy(
    tmp_path: Path, world: World, case: str, args: tuple[str, ...]
) -> None:
    line, said = entry(world, case)
    commit = craft(world, "skills", added=(line,))
    # The check builds its copy in a temporary folder deep enough below the test's own that
    # a path up out of it would still land inside the test's folder.
    temporary = tmp_path / "temporary" / "a" / "b"
    temporary.mkdir(parents=True)
    done = sync(world, commit, "v2.0.0", *args, environment={"TMPDIR": str(temporary)})
    assert done.returncode == 1
    assert said in done.stderr
    assert not list(tmp_path.rglob("outside"))


def test_the_sync_refuses_a_release_that_lacks_a_vendored_path(world: World) -> None:
    commit = craft(world, "hooks", dropped=("session-start",))
    done = sync(world, commit, "v2.0.0")
    assert done.returncode == 1
    assert f"sync: owner/superpowers@{commit} gives no hooks/session-start" in done.stderr


# R275 and DR-281: the editors' configuration gives the lock line feeds.


def editor_settings(path: str) -> dict[str, str]:
    """The properties that `.editorconfig` gives a file at this path, from each section whose
    glob matches it in turn, a later one over an earlier, reading a glob as the EditorConfig
    specification does where it holds only `*`, `**`, `?` and characters that stand for
    themselves, and refusing any other."""
    settings: dict[str, str] = {}
    pattern: re.Pattern[str] | None = None
    for line in (ROOT / ".editorconfig").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("[") and line.endswith("]"):
            glob = line[1:-1]
            assert not set(glob) & set("[]{}!\\"), f"the test reads no glob such as {glob}"
            body = "".join(
                ".*"
                if part == "**"
                else "[^/]*"
                if part == "*"
                else "[^/]"
                if part == "?"
                else re.escape(part)
                for part in re.split(r"(\*\*|\*|\?)", glob)
                if part
            )
            pattern = re.compile(body if "/" in glob else f"(?:.*/)?{body}")
        elif pattern is not None and pattern.fullmatch(path):
            key, _, value = line.partition("=")
            settings[key.strip().lower()] = value.strip()
    return settings


def test_the_editors_configuration_gives_the_lock_line_feeds() -> None:
    lock = editor_settings("vendor/superpowers/UPSTREAM.lock")
    assert lock["end_of_line"] == "lf"
    assert lock["charset"] == "utf-8"
    assert lock["insert_final_newline"] == "true"


def test_the_editors_configuration_leaves_the_vendored_files_as_upstream_wrote_them() -> None:
    for path in ("vendor/superpowers/LICENSE", "vendor/superpowers/skills/a/SKILL.md"):
        assert editor_settings(path)["end_of_line"] == "unset"
        assert editor_settings(path)["charset"] == "unset"
