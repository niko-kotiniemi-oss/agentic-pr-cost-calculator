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
out the lock at the root alone, by its path, and the mode that git's index
gives each with the mode that the commit gives it. It stops on a link in the
copy, on a path that git's checkout refuses on Windows or macOS and on a pinned
file that holds a carriage return, leaves the copy as it was where a refresh
stops, reads and writes no repository that a person's git variables name,
reads each path as the name that it is whatever they say of how git reads one,
works whatever object format git gives a new repository, replaces each vendored
path wherever the clone lies, and says how to write the copy again where a
vendored file holds a carriage return, which the commit's do not (R275, R276,
DR-275, DR-281, DR-284).

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
from conventions import NO_WINDOWS_LINE_ENDINGS, tracked_entries, written_by_others
from test_roadmap import (
    GIT_ENVIRONMENT,
    isolated_environment,
    saved_with_windows_line_endings,
    session_free_environment,
)

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
    bare copy that the sync fetches from, and a git repository that holds the script, with
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
    git("init", "-q", cwd=repo)
    shutil.copy(SCRIPT, repo / "scripts" / SCRIPT.name)
    (repo / "vendor" / "superpowers").mkdir(parents=True)
    return World(repo, remotes, tagged, untagged)


@pytest.fixture
def world(tmp_path: Path) -> World:
    return build_world(tmp_path)


# What the sync says of a link in the copy, and what its check says of a vendored file whose
# mode in git's index is not the pinned commit's, and of one that holds a carriage return
# that the pinned commit's does not, with the way back (R275, R276).
LINK = "sync: {path} is a link, which the sync does not follow"
MODE_DIFFERS = (
    "sync: git's index gives {path} the mode {staged}, not the mode {given} that the pinned"
    " commit gives it"
)
CARRIAGE_RETURN = "sync: {path} holds a carriage return that the pinned commit's file does not"
WAY_BACK = (
    "to write the pinned commit's files again, run scripts/sync-superpowers.sh, or delete"
    " vendor/superpowers and check it out again"
)


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
    if "\r\n" in ending:
        assert b"\r\n" in lock.read_bytes(), f"{lock.name}: the test {NO_WINDOWS_LINE_ENDINGS}"
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


def test_a_missing_vendored_file_fails_the_check_and_is_named(world: World) -> None:
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    (world.repo / "vendor" / "superpowers" / "LICENSE").unlink()
    done = sync(world, world.tagged, "v1.0.0", "--check")
    assert done.returncode == 1
    assert "DIFFERS" in done.stderr
    assert ": LICENSE" in done.stderr
    # The check reads no file that is not there.
    assert "No such file" not in done.stderr


def test_an_edited_vendored_file_fails_the_check(world: World) -> None:
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    (world.repo / "vendor" / "superpowers" / "LICENSE").write_text("edited by hand\n")
    done = sync(world, world.tagged, "v1.0.0", "--check")
    assert done.returncode == 1
    assert "DIFFERS" in done.stderr
    # An edit that holds no carriage return is given no advice on line endings.
    assert "carriage return" not in done.stderr


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
    "a default object format of SHA-256",
)


def prepared(tmp_path: Path, case: str) -> tuple[World, dict[str, str], str]:
    """A world, the environment that the sync runs in and how its lock's lines end, for the
    case: a global configuration that sets `core.autocrlf` to `true`, one whose template
    gives each new clone a `.git/info/attributes` that holds `* eol=crlf`, a lock whose
    lines end in CRLF, an upstream whose own attributes `git archive` would follow, or a
    git that gives a new repository SHA-256's object format, where upstream's is SHA-1's."""
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
    if case == "a default object format of SHA-256":
        environment["GIT_DEFAULT_HASH"] = "sha256"
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
    """Each file below the vendored root but the lock at the root, as `files_below` gives
    it."""
    given = files_below(world.repo / "vendor" / "superpowers")
    given.pop("UPSTREAM.lock", None)
    return given


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
    saved_with_windows_line_endings(root, ["LICENSE"])
    failed = sync(world, world.tagged, "v1.0.0", "--check", environment=environment, ending=ending)
    assert failed.returncode == 1
    assert "DIFFERS" in failed.stderr
    assert CARRIAGE_RETURN.format(path="vendor/superpowers/LICENSE") in failed.stderr
    assert WAY_BACK in failed.stderr


# R275: the sync writes only files, each with the mode that the pinned commit gives it, and
# only inside the folder that it writes the copy into.


def quoted(text: str) -> str:
    """The text as the script's `printf %q` writes it, in the environment that the script
    runs in."""
    done = subprocess.run(
        ["bash", "-c", 'printf %q "$1"', "bash", text],
        env=isolated(),
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout


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
    if case.startswith(FOLDER_NAMED):
        name = case.removeprefix(FOLDER_NAMED)
        config = blob("[core]\n\tfsmonitor = a command of upstream's\n")
        inner = tree(f"100644 blob {config}\tconfig")
        path = quoted(f"skills/{name}/config")
        return (
            f"040000 tree {inner}\t{name}",
            f"gives the path {path}, which the sync does not write",
        )
    if case == "a link":
        link = blob("../../../outside")
        return f"120000 blob {link}\tlink", "gives skills/link the mode 120000, which the sync"
    return f"160000 commit {world.untagged}\tsub", "gives skills/sub the mode 160000, which"


FOLDER_NAMED = "a folder named "
# Names that git's checkout refuses with the protections of NTFS and HFS+ on, since Windows
# or macOS opens each as `.git`: in another case, with a dot or a space at its end, as its
# short name, as one of its streams, and with a character that HFS+ ignores (T270).
OPENED_AS_GIT = (".GiT", ".git.", ".git ", "git~1", ".git::$INDEX_ALLOCATION", ".g\u200cit")
ENTRIES = (
    "a path up out of the copy",
    "a path through a dot",
    *(f"{FOLDER_NAMED}{name}" for name in (".git", *OPENED_AS_GIT)),
    "a link",
    "a submodule",
)


@pytest.mark.parametrize("args", [(), ("--check",)], ids=["refresh", "check"])
@pytest.mark.parametrize("protections", ["as git gives them", "turned off"])
@pytest.mark.parametrize("case", ENTRIES)
def test_the_sync_refuses_an_entry_that_is_not_a_file_inside_its_copy(
    tmp_path: Path, world: World, case: str, protections: str, args: tuple[str, ...]
) -> None:
    line, said = entry(world, case)
    commit = craft(world, "skills", added=(line,))
    # The check builds its copy in a temporary folder deep enough below the test's own that
    # a path up out of it would still land inside the test's folder.
    temporary = tmp_path / "temporary" / "a" / "b"
    temporary.mkdir(parents=True)
    environment = {"TMPDIR": str(temporary)}
    if protections == "turned off":
        # A person's own configuration can turn off the protections that git gives a
        # checkout, which the sync turns on for itself.
        configuration = tmp_path / "gitconfig"
        configuration.write_bytes(b"[core]\n\tprotectNTFS = false\n\tprotectHFS = false\n")
        environment["GIT_CONFIG_GLOBAL"] = str(configuration)
    done = sync(world, commit, "v2.0.0", *args, environment=environment)
    assert done.returncode == 1
    assert said in done.stderr
    assert not list(tmp_path.rglob("outside"))
    assert not list((world.repo / "vendor").rglob("config"))


@pytest.mark.parametrize("name", [".github", ".gitkeep", "git~2"])
def test_the_sync_writes_a_folder_whose_name_only_looks_like_git_s(world: World, name: str) -> None:
    bare = world.remotes / "owner" / "superpowers.git"
    note = git("hash-object", "-w", "--stdin", cwd=bare, stdin="A note.\n")
    inner = git("mktree", cwd=bare, stdin=f"100644 blob {note}\tconfig\n")
    commit = craft(world, "skills", added=(f"040000 tree {inner}\t{name}",))
    synced = sync(world, commit, "v2.0.0")
    assert synced.returncode == 0, synced.stderr
    written = world.repo / "vendor" / "superpowers" / "skills" / name / "config"
    assert written.read_bytes() == b"A note.\n"
    checked = sync(world, commit, "v2.0.0", "--check")
    assert checked.returncode == 0, checked.stderr


def test_the_sync_refuses_a_release_that_lacks_a_vendored_path(world: World) -> None:
    commit = craft(world, "hooks", dropped=("session-start",))
    done = sync(world, commit, "v2.0.0")
    assert done.returncode == 1
    assert f"sync: owner/superpowers@{commit} gives no hooks/session-start" in done.stderr


# R275: a pinned file that holds a carriage return stops the sync, since git commits one before
# a line feed as a line feed, so that the copy would no longer match the pinned commit, and the
# test of characters refuses one that git keeps (R269).

HELD_RETURNS = {
    "a carriage return before a line feed": "A licence.\r\n",
    "a lone carriage return": "A licence.\rAnd more.\n",
}


@pytest.mark.parametrize("args", [(), ("--check",)], ids=["refresh", "check"])
@pytest.mark.parametrize("text", list(HELD_RETURNS.values()), ids=list(HELD_RETURNS))
def test_the_sync_refuses_a_pinned_file_that_holds_a_carriage_return(
    world: World, text: str, args: tuple[str, ...]
) -> None:
    bare = world.remotes / "owner" / "superpowers.git"
    returned = git("hash-object", "-w", "--stdin", cwd=bare, stdin=text)
    commit = craft(world, "skills", added=(f"100644 blob {returned}\tLICENSE.txt",))
    # The copy as the pinned commit gives it, as the refresh wrote it before a commit, which a
    # check that compared it with the pinned commit's files alone would pass.
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    licence = world.repo / "vendor" / "superpowers" / "skills" / "LICENSE.txt"
    licence.write_bytes(text.encode())
    assert b"\r" in licence.read_bytes(), f"{licence.name}: the test planted no carriage return"
    before = vendored(world)
    done = sync(world, commit, "v2.0.0", *args)
    assert done.returncode == 1
    said = (
        f"sync: owner/superpowers@{commit} gives skills/LICENSE.txt a carriage return, which no"
        " vendored file may hold"
    )
    assert said in done.stderr
    assert vendored(world) == before


# R275: a refresh that stops, on what the pinned commit gives or on a fetch that fails, leaves
# the vendored copy as it was.

STOPS = (
    "a link that git lists before every vendored file",
    "a link that git lists after every vendored file",
    "a release that lacks a vendored path",
    "a fetch that fails",
)


def stopping(tmp_path: Path, world: World, case: str) -> tuple[str, str, dict[str, str], str]:
    """A pin on which the refresh stops, for the case, as its commit and its tag, with the
    environment that the refresh runs in and what it says there: a crafted release, or the
    tagged one where git's upload of the pinned commit fails, as where the network drops once
    the tag is read."""
    if case == "a fetch that fails":
        configuration = tmp_path / "gitconfig"
        configuration.write_bytes(b"[uploadpack]\n\tpackObjectsHook = false\n")
        return world.tagged, "v1.0.0", {"GIT_CONFIG_GLOBAL": str(configuration)}, "fatal: "
    if case == "a release that lacks a vendored path":
        commit = craft(world, "hooks", dropped=("session-start",))
        return commit, "v2.0.0", {}, "gives no hooks/session-start"
    # Git lists `.claude-plugin`, `LICENSE`, `hooks` and `skills` in this order, a folder's
    # `link` before `plugin.json` and after the folder `a`.
    folder = ".claude-plugin" if case.endswith("before every vendored file") else "skills"
    bare = world.remotes / "owner" / "superpowers.git"
    link = git("hash-object", "-w", "--stdin", cwd=bare, stdin="../../outside")
    commit = craft(world, folder, added=(f"120000 blob {link}\tlink",))
    return commit, "v2.0.0", {}, f"gives {folder}/link the mode 120000"


@pytest.mark.parametrize("case", STOPS)
def test_a_refresh_that_stops_leaves_the_vendored_copy_as_it_was(
    tmp_path: Path, world: World, case: str
) -> None:
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    # An edit that a refresh which wrote part of its copy would write over, so that one shows.
    (world.repo / "vendor" / "superpowers" / "LICENSE").write_bytes(b"Not upstream's.\n")
    before = vendored(world)
    commit, tag, environment, said = stopping(tmp_path, world, case)
    done = sync(world, commit, tag, environment=environment)
    assert done.returncode != 0
    assert said in done.stderr
    assert "re-materialised" not in done.stdout
    assert vendored(world) == before


# R275: a refresh replaces each vendored path wherever the clone lies, below a folder whose name
# holds `&` too, which bash 5.2 reads in the replacement of a substitution as the text matched.


def test_a_refresh_below_a_folder_whose_name_holds_an_ampersand_replaces_each_vendored_path(
    tmp_path: Path,
) -> None:
    (tmp_path / "R&D").mkdir()
    world = build_world(tmp_path / "R&D")
    # A copy where the folder's name without its `&` would lead, which no refresh may touch.
    decoy = tmp_path / "RD" / "repo" / "vendor" / "superpowers"
    for path in VENDORED:
        (decoy / path).parent.mkdir(parents=True, exist_ok=True)
        (decoy / path).write_bytes(b"A decoy's.\n")
    before = files_below(tmp_path / "RD")
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    # An edit that the second refresh must write over, in a copy whose paths are all there.
    (world.repo / "vendor" / "superpowers" / "skills/a/SKILL.md").write_bytes(b"Edited.\n")
    done = sync(world, world.tagged, "v1.0.0")
    assert done.returncode == 0, done.stderr
    assert vendored(world) == released(world)
    assert files_below(tmp_path / "RD") == before
    checked = sync(world, world.tagged, "v1.0.0", "--check")
    assert checked.returncode == 0, checked.stderr


def files_below(folder: Path) -> dict[str, tuple[int, bytes]]:
    """Each file below the folder by its path, with its mode and its bytes."""
    return {
        path.relative_to(folder).as_posix(): (stat.S_IMODE(path.stat().st_mode), path.read_bytes())
        for path in folder.rglob("*")
        if path.is_file() and not path.is_symlink()
    }


# R275: a link in the vendored copy, or one that leads to it, stops the sync before it reads
# or writes anything.

LINKED = {
    "a vendored folder": "vendor/superpowers/hooks",
    "a vendored file": "vendor/superpowers/skills/a/SKILL.md",
    "the vendored copy": "vendor/superpowers",
    "the vendor folder": "vendor",
}


@pytest.mark.parametrize("args", [(), ("--check",)], ids=["refresh", "check"])
@pytest.mark.parametrize("case", LINKED)
def test_a_link_in_the_vendored_copy_stops_the_sync_before_it_reads_or_writes(
    tmp_path: Path, world: World, case: str, args: tuple[str, ...]
) -> None:
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    link = world.repo / LINKED[case]
    outside = tmp_path / "outside"
    shutil.move(link, outside)
    link.symlink_to(outside, target_is_directory=outside.is_dir())
    # What the link leads to differs from upstream's release, so that a refresh that wrote
    # through it, and a check that read through it, would each show: the shortest of its
    # files, which is never the lock.
    if outside.is_dir():
        outside /= min(files_below(outside), key=len)
    outside.write_bytes(b"Not upstream's.\n")
    before = files_below(tmp_path)
    done = sync(world, world.tagged, "v1.0.0", *args)
    assert done.returncode == 1
    assert LINK.format(path=LINKED[case]) in done.stderr
    # It stops there, before it fetches or compares anything.
    assert "DIFFERS" not in done.stderr
    assert link.is_symlink()
    assert files_below(tmp_path) == before


# R275: the sync reads and writes no repository but its own and this one, whatever git
# variables of the person's name another, and reads each path as the name that it is,
# whatever they say of how git reads one.

# The variables that change how git reads a path, which git does not list among those that
# name a repository.
PATHSPEC_VARIABLES = (
    "GIT_LITERAL_PATHSPECS",
    "GIT_GLOB_PATHSPECS",
    "GIT_NOGLOB_PATHSPECS",
    "GIT_ICASE_PATHSPECS",
)
NAMINGS = (
    "GIT_DIR",
    "GIT_DIR and GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_COMMON_DIR",
    *PATHSPEC_VARIABLES,
)


def another_repository(tmp_path: Path) -> Path:
    """A repository of one commit beside the world's, which no sync may read or write."""
    other = tmp_path / "other"
    other.mkdir()
    git("init", "-q", cwd=other)
    (other / "file").write_bytes(b"Another repository's.\n")
    git("add", "--", "file", cwd=other)
    git("commit", "-q", "-m", "another", cwd=other)
    return other


def naming(other: Path, case: str) -> dict[str, str]:
    """The git variables that name the other repository, or a part of it, for the case, or
    the one that changes how git reads a path."""
    dot = other / ".git"
    return {
        "GIT_DIR": {"GIT_DIR": str(dot)},
        "GIT_DIR and GIT_WORK_TREE": {"GIT_DIR": str(dot), "GIT_WORK_TREE": str(other)},
        "GIT_INDEX_FILE": {"GIT_INDEX_FILE": str(dot / "index")},
        "GIT_OBJECT_DIRECTORY": {"GIT_OBJECT_DIRECTORY": str(dot / "objects")},
        "GIT_COMMON_DIR": {"GIT_COMMON_DIR": str(dot)},
        **{variable: {variable: "1"} for variable in PATHSPEC_VARIABLES},
    }[case]


@pytest.mark.parametrize("args", [(), ("--check",)], ids=["refresh", "check"])
@pytest.mark.parametrize("case", NAMINGS)
def test_the_sync_reads_and_writes_no_repository_that_a_person_s_git_variables_name(
    tmp_path: Path, world: World, case: str, args: tuple[str, ...]
) -> None:
    other = another_repository(tmp_path)
    if args:
        assert sync(world, world.tagged, "v1.0.0").returncode == 0
    before = files_below(other)
    done = sync(world, world.tagged, "v1.0.0", *args, environment=naming(other, case))
    assert done.returncode == 0, done.stderr
    assert vendored(world) == released(world)
    assert files_below(other) == before


@pytest.mark.parametrize("form", ["GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS"])
def test_the_sync_keeps_the_configuration_that_git_s_variables_give(
    world: World, form: str
) -> None:
    # A base that names nothing, which the configuration that the variables give rewrites to
    # the local upstream, so that the sync fetches only where it keeps them.
    nowhere = (world.remotes.parent / "nowhere").as_uri()
    key, value = f"url.{world.remotes.as_uri()}/.insteadOf", f"{nowhere}/"
    given = (
        {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": key, "GIT_CONFIG_VALUE_0": value}
        if form == "GIT_CONFIG_COUNT"
        else {"GIT_CONFIG_PARAMETERS": f"'{key}'='{value}'"}
    )
    unconfigured = sync(world, world.tagged, "v1.0.0", environment={"SYNC_REMOTE_BASE": nowhere})
    assert unconfigured.returncode == 1
    done = sync(world, world.tagged, "v1.0.0", environment={"SYNC_REMOTE_BASE": nowhere, **given})
    assert done.returncode == 0, done.stderr
    assert vendored(world) == released(world)


# R275: the check compares the mode that git's index gives each vendored file with the mode
# that the pinned commit gives it, whatever a variable of the person's says of how git reads
# a path.


@pytest.mark.parametrize("variable", [None, *PATHSPEC_VARIABLES])
@pytest.mark.parametrize(
    ("path", "change", "staged", "given"),
    [("hooks/run-hook.cmd", "-x", "100644", "100755"), ("LICENSE", "+x", "100755", "100644")],
    ids=["an executable file staged as not executable", "a file staged as executable"],
)
def test_a_vendored_file_that_git_s_index_gives_another_mode_fails_the_check(
    world: World, path: str, change: str, staged: str, given: str, variable: str | None
) -> None:
    environment = {variable: "1"} if variable else {}
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    git("add", "--", "vendor/superpowers", cwd=world.repo)
    passed = sync(world, world.tagged, "v1.0.0", "--check", environment=environment)
    assert passed.returncode == 0, passed.stderr
    git("update-index", f"--chmod={change}", "--", f"vendor/superpowers/{path}", cwd=world.repo)
    failed = sync(world, world.tagged, "v1.0.0", "--check", environment=environment)
    assert failed.returncode == 1
    assert "DIFFERS" in failed.stderr
    named = f"vendor/superpowers/{path}"
    assert MODE_DIFFERS.format(path=named, staged=staged, given=given) in failed.stderr


def test_the_check_reads_the_mode_of_a_vendored_name_that_git_could_take_as_a_pattern(
    world: World,
) -> None:
    bare = world.remotes / "owner" / "superpowers.git"
    note = git("hash-object", "-w", "--stdin", cwd=bare, stdin="A note.\n")
    # `[X].md`, read as a pattern, names `X.md` too, which git's index lists first.
    added = (f"100755 blob {note}\tX.md", f"100644 blob {note}\t[X].md")
    commit = craft(world, "skills", added=added)
    assert sync(world, commit, "v2.0.0").returncode == 0
    git("add", "--", "vendor/superpowers", cwd=world.repo)
    done = sync(world, commit, "v2.0.0", "--check")
    assert done.returncode == 0, done.stderr


def test_the_check_outside_a_git_repository_fails(world: World) -> None:
    # The check reads git's index, so it fails where there is none rather than compare no
    # mode.
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    shutil.rmtree(world.repo / ".git")
    ceiling = {"GIT_CEILING_DIRECTORIES": str(world.repo.parent)}
    done = sync(world, world.tagged, "v1.0.0", "--check", environment=ceiling)
    assert done.returncode != 0
    assert "not a git repository" in done.stderr


# R276: the check says how to write the vendored copy again where a vendored file holds a
# carriage return that the pinned commit's does not, as a clone made with `core.autocrlf`
# set to `true` before the repository's attributes keeps one.


@pytest.mark.parametrize("way", ["the refresh", "a checkout"])
def test_the_way_back_that_the_check_gives_writes_the_pinned_files_again(
    world: World, way: str
) -> None:
    assert sync(world, world.tagged, "v1.0.0").returncode == 0
    git("add", "--", "vendor/superpowers", cwd=world.repo)
    git("commit", "-q", "-m", "vendored", cwd=world.repo)
    root = world.repo / "vendor" / "superpowers"
    saved_with_windows_line_endings(root, ["LICENSE", "skills/a/SKILL.md"])
    failed = sync(world, world.tagged, "v1.0.0", "--check")
    assert failed.returncode == 1
    for path in ("LICENSE", "skills/a/SKILL.md"):
        assert CARRIAGE_RETURN.format(path=f"vendor/superpowers/{path}") in failed.stderr
    assert failed.stderr.count(WAY_BACK) == 1
    if way == "the refresh":
        assert sync(world, world.tagged, "v1.0.0").returncode == 0
    else:
        shutil.rmtree(root)
        git("checkout", "--", "vendor/superpowers", cwd=world.repo)
    checked = sync(world, world.tagged, "v1.0.0", "--check")
    assert checked.returncode == 0, checked.stderr


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


def test_the_editors_configuration_unsets_its_settings_only_for_the_files_that_others_write() -> (
    None
):
    """Every property that `.editorconfig` gives is unset for each file that others write, and
    none for a file that this repository writes, such as one of its own under `vendor/`, which
    the checks read, so that an editor writes it as they expect (R268, DR-274)."""
    own = ["vendor/notes.md", "vendor/tool.py", "vendor/tool.sh", ".claude/skills/a/SKILL.md"]
    tracked = [entry.path for entry in tracked_entries(ROOT, isolated_environment(ROOT))]
    paths = [*tracked, *own, "vendor/superpowers/b/SKILL.md", ".claude/skills/openspec-b/a.md"]
    assert any(map(written_by_others, paths)) and not all(map(written_by_others, paths))
    for path in paths:
        given = editor_settings(path)
        if written_by_others(path):
            assert set(given.values()) == {"unset"}, path
        else:
            assert "unset" not in given.values(), path
            kept = (given["charset"], given["end_of_line"], given["insert_final_newline"])
            assert kept == ("utf-8", "lf", "true"), path


# R299, R317: the base commit's sync checks a pull request's tree from git's objects alone,
# holding its lock to the base's repository and vendored paths, and fetching from GitHub
# whatever SYNC_REMOTE_BASE says.

LOCK_LINES = "repo=owner/superpowers\nsha={sha}\ntag=v1.0.0\n"
REGULAR = "100644"


def tree_commit(world: World, entries: dict[str, tuple[str, bytes]]) -> str:
    """A commit in the repository whose tree holds these entries, each a mode and the bytes
    of its blob, or the commit it names for a gitlink, written with git's plumbing alone."""
    index = world.repo / ".git" / "commit-index"
    index.unlink(missing_ok=True)
    for path, (mode, data) in entries.items():
        if mode == "160000":
            oid = data.decode()
        else:
            oid = git("hash-object", "-w", "--stdin", cwd=world.repo, stdin=data.decode())
        subprocess.run(
            # With NTFS's protections off, so that a test can plant a path that the
            # base's check must refuse.
            [
                "git",
                "-c",
                "core.protectNTFS=false",
                "update-index",
                "--add",
                "--cacheinfo",
                f"{mode},{oid},{path}",
            ],  # fmt: skip
            cwd=world.repo,
            env={**isolated(), "GIT_INDEX_FILE": str(index)},
            check=True,
            capture_output=True,
        )
    tree = subprocess.run(
        ["git", "write-tree"],
        cwd=world.repo,
        env={**isolated(), "GIT_INDEX_FILE": str(index)},
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return git("commit-tree", tree, "-m", "a pull request's tree", cwd=world.repo)


def pinned_entries(world: World, lock: str | None = None) -> dict[str, tuple[str, bytes]]:
    """The tree of a pull request whose copy is the pinned one, with its lock."""
    entries = {
        f"vendor/superpowers/{path}": ("100755" if path in EXECUTABLE else REGULAR, text.encode())
        for path, text in RELEASED.items()
    }
    text = lock if lock is not None else LOCK_LINES.format(sha=world.tagged)
    entries["vendor/superpowers/UPSTREAM.lock"] = (REGULAR, text.encode())
    return entries


def check_commit(
    world: World, commit: str, environment: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    """The base's script, with the base's lock, run over a commit's tree, with GitHub's
    address sent to the local upstream by git's own configuration."""
    lock = world.repo / "vendor" / "superpowers" / "UPSTREAM.lock"
    lock.write_bytes(LOCK_LINES.format(sha=world.tagged).encode())
    github = {
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": f"url.{world.remotes.as_uri()}/.insteadOf",
        "GIT_CONFIG_VALUE_0": "https://github.com/",
    }
    return subprocess.run(
        ["bash", str(world.repo / "scripts" / SCRIPT.name), "--check-commit", commit],
        env={**isolated(), **github, **(environment or {})},
        capture_output=True,
        text=True,
    )


def test_a_commit_whose_copy_is_the_pinned_one_passes_the_base_s_check(world: World) -> None:
    done = check_commit(world, tree_commit(world, pinned_entries(world)))
    assert done.returncode == 0, done.stderr
    assert "matches owner/superpowers" in done.stdout


def test_a_commit_that_edits_a_vendored_file_fails_the_base_s_check(world: World) -> None:
    entries = pinned_entries(world)
    entries["vendor/superpowers/LICENSE"] = (REGULAR, b"edited in a pull request\n")
    done = check_commit(world, tree_commit(world, entries))
    assert done.returncode == 1
    assert "DIFFERS" in done.stderr


def test_a_commit_that_gives_a_vendored_file_another_mode_fails_the_base_s_check(
    world: World,
) -> None:
    entries = pinned_entries(world)
    entries["vendor/superpowers/LICENSE"] = ("100755", RELEASED["LICENSE"].encode())
    done = check_commit(world, tree_commit(world, entries))
    assert done.returncode == 1
    assert "vendor/superpowers/LICENSE the mode 100755, not the mode 100644" in done.stderr


@pytest.mark.parametrize("line", ["repo=someone/superpowers", "vendored_paths=skills"])
def test_a_commit_whose_lock_points_elsewhere_fails_the_base_s_check(
    world: World, line: str
) -> None:
    lock = LOCK_LINES.format(sha=world.tagged)
    key = line.partition("=")[0]
    lock = "\n".join(x for x in lock.splitlines() if not x.startswith(f"{key}=")) + f"\n{line}\n"
    done = check_commit(world, tree_commit(world, pinned_entries(world, lock)))
    assert done.returncode == 1
    assert f"the pull request's lock gives {line}, not the base's" in done.stderr


@pytest.mark.parametrize(
    ("path", "mode"),
    [("vendor/superpowers/skills/b", "120000"), ("vendor/superpowers/skills/c", "160000")],
    ids=["link", "gitlink"],
)
def test_a_commit_with_a_link_or_a_gitlink_in_the_copy_fails_the_base_s_check(
    world: World, path: str, mode: str
) -> None:
    entries = pinned_entries(world)
    entries[path] = (mode, world.tagged.encode() if mode == "160000" else b"../../../etc")
    done = check_commit(world, tree_commit(world, entries))
    assert done.returncode == 1
    assert f"the pull request gives {path} the mode {mode}, which the check does not read" in (
        done.stderr
    )


@pytest.mark.parametrize(
    ("path", "mode"),
    [("vendor/other/link", "120000"), ("vendor/other/sub", "160000")],
    ids=["link", "gitlink"],
)
def test_a_commit_with_a_link_or_a_gitlink_elsewhere_under_vendor_fails_the_base_s_check(
    world: World, path: str, mode: str
) -> None:
    entries = pinned_entries(world)
    entries[path] = (mode, world.tagged.encode() if mode == "160000" else b"../superpowers")
    done = check_commit(world, tree_commit(world, entries))
    assert done.returncode == 1
    assert f"the pull request gives {path} the mode {mode}, which the check does not read" in (
        done.stderr
    )


def test_a_commit_with_a_regular_file_directly_under_vendor_passes_the_base_s_check(
    world: World,
) -> None:
    entries = pinned_entries(world)
    entries["vendor/README.md"] = (REGULAR, b"what is vendored here\n")
    done = check_commit(world, tree_commit(world, entries))
    assert done.returncode == 0, done.stderr
    assert "matches owner/superpowers" in done.stdout


def test_a_path_that_the_base_s_check_refuses_to_write_fails_it(world: World) -> None:
    entries = pinned_entries(world)
    entries["vendor/superpowers/skills/GIT~1/config"] = (REGULAR, b"[core]\n")
    done = check_commit(world, tree_commit(world, entries))
    assert done.returncode == 1
    assert "gives the path vendor/superpowers/skills/GIT~1/config, which the check does not" in (
        done.stderr
    )


def test_a_path_with_a_line_feed_reaches_the_log_quoted(world: World) -> None:
    entries = pinned_entries(world)
    entries["vendor/superpowers/skills/x\n::warning::planted"] = ("120000", b"elsewhere")
    done = check_commit(world, tree_commit(world, entries))
    assert done.returncode == 1
    assert "\n::warning::planted" not in done.stderr
    assert "$'vendor/superpowers/skills/x\\n::warning::planted'" in done.stderr


def test_a_commit_whose_vendor_folder_is_a_link_fails_the_base_s_check(world: World) -> None:
    done = check_commit(world, tree_commit(world, {"vendor": ("120000", b"elsewhere")}))
    assert done.returncode == 1
    assert "the pull request gives vendor the mode 120000" in done.stderr


def test_a_commit_with_no_lock_fails_the_base_s_check(world: World) -> None:
    entries = pinned_entries(world)
    del entries["vendor/superpowers/UPSTREAM.lock"]
    done = check_commit(world, tree_commit(world, entries))
    assert done.returncode == 1
    assert "the pull request's tree holds no vendor/superpowers/UPSTREAM.lock" in done.stderr


def test_the_base_s_check_with_no_commit_stops(world: World) -> None:
    done = sync(world, world.tagged, "v1.0.0", "--check-commit")
    assert done.returncode == 2
    assert "sync: --check-commit needs a commit" in done.stderr


def test_a_commit_that_cannot_be_read_fails_the_base_s_check(world: World) -> None:
    done = check_commit(world, "0" * 40)
    assert done.returncode != 0
    assert "matches" not in done.stdout


def test_the_base_s_check_fetches_from_github_whatever_sync_remote_base_says(
    world: World, tmp_path: Path
) -> None:
    nowhere = (tmp_path / "nowhere").as_uri()
    commit = tree_commit(world, pinned_entries(world))
    done = check_commit(world, commit, {"SYNC_REMOTE_BASE": nowhere})
    assert done.returncode == 0, done.stderr


def test_an_option_that_the_sync_does_not_have_stops_it_before_it_writes(world: World) -> None:
    done = sync(world, world.tagged, "v1.0.0", "--check-comit")
    assert done.returncode == 2
    assert "sync: --check-comit is not an option of the sync" in done.stderr
    assert not (world.repo / "vendor" / "superpowers" / "skills").exists()
