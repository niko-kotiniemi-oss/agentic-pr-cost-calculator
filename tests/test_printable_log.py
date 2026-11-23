"""What every command of CI prints reaches the log as printable ASCII (R278).

Each workflow under `.github/workflows/` runs every step's script through
`scripts/printable_log.py`, as the shell that its defaults give, so that a check which quotes
a planted path as it is, as ruff, mypy, pytest and the sync's check do, writes the path's
hidden characters by their code points (T264). These tests run the filter on commands that
print what a test chooses and on ruff, and read every workflow that this repository runs.
"""

from __future__ import annotations

import select
import shlex
import signal
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import conventions
import printable_log
import pytest
from printable_log import relay
from test_conventions import MERGE_CHECK
from test_repository import load_workflow, workflows

ROOT = Path(__file__).resolve().parents[1]
FILTER = ROOT / "scripts" / "printable_log.py"
# The shell that every workflow's defaults give its steps: GitHub's own for `bash`, run
# through the filter.
SHELL = "python3 -I scripts/printable_log.py bash --noprofile --norc -eo pipefail {0}"
CHECKOUT = "actions/checkout@"
# "OBEY" in tag characters, which a renderer shows as nothing, as a planted path holds it,
# and what the filter writes for it.
HIDDEN = "".join(chr(0xE0000 + ord(letter)) for letter in "OBEY")
HIDDEN_SHOWN = "U+E004FU+E0042U+E0045U+E0059"
# GitHub's own shell for `bash`, and the one step that runs under it rather than through the
# filter, word for word: a step of the job `ci` that fails where the filter loses a command's
# exit status, or the signal that stopped it, which would let every other step pass, the
# job `ci` among them, whatever their commands did, and that writes nothing of the filter's
# to the log (R278).
GITHUB_BASH = "bash --noprofile --norc -eo pipefail {0}"
OBSERVER_SHELL = "bash"
OBSERVER = (
    "status=0\n"
    "python3 -I scripts/printable_log.py bash -c 'exit 3' > /dev/null 2>&1 || status=$?\n"
    'echo "The filter gave $status for a command that exits with 3."\n'
    '[ "$status" -eq 3 ]\n'
    "status=0\n"
    "python3 -I scripts/printable_log.py bash -c 'kill -TERM $$' > /dev/null 2>&1 || status=$?\n"
    'echo "The filter gave $status for a command that SIGTERM stops."\n'
    '[ "$status" -eq 143 ]\n'
)


def test_the_filter_shows_text_as_the_checks_show_it() -> None:
    # Under `python3 -I` the filter cannot import `scripts/conventions.py`, whose way of showing
    # text the checks use, so it keeps a copy, which this test holds to it.
    text = "".join(map(chr, [*range(0x80), 0xA0, 0x202E, 0xDC7F, 0xDD00, 0xE0041]))
    text += b"\x80\xff".decode("utf-8", "surrogateescape")
    assert printable_log.shown(text) == conventions.printable(text, " \n")
    assert printable_log.NOT_UTF8 == conventions.ESCAPED_BYTES


def printable(data: bytes) -> bool:
    """Whether the bytes are printable ASCII and line feeds alone."""
    return all(byte == 0x0A or 0x20 <= byte <= 0x7E for byte in data)


def through_the_filter(
    *command: str, cwd: Path | None = None
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, "-I", str(FILTER), *command], capture_output=True, check=False, cwd=cwd
    )


def printing(output: bytes, errors: bytes = b"", status: int = 0) -> list[str]:
    """A command that prints the bytes given as its output, then those given as its errors,
    and exits with the status given."""
    code = (
        "import sys\n"
        f"sys.stdout.buffer.write({output!r})\n"
        "sys.stdout.buffer.flush()\n"
        f"sys.stderr.buffer.write({errors!r})\n"
        "sys.stderr.buffer.flush()\n"
        f"sys.exit({status})\n"
    )
    return [sys.executable, "-I", "-c", code]


@pytest.mark.parametrize(
    ("printed", "logged"),
    [
        (b"plain text\n", b"plain text\n"),
        (
            f"scripts/tool{HIDDEN}.py:1:8: F401\n".encode(),
            f"scripts/tool{HIDDEN_SHOWN}.py:1:8: F401\n".encode(),
        ),
        ("docs/link\ufe0f.md\n".encode(), b"docs/linkU+FE0F.md\n"),
        (b"\x1b[8mhidden\x1b[0m\n", b"U+001B[8mhiddenU+001B[0m\n"),
        (b"a\rb\tc\n", b"aU+000DbU+0009c\n"),
        (b"\x00\x7f\n", b"U+0000U+007F\n"),
        ("\u00e9\u2014\u202e\n".encode(), b"U+00E9U+2014U+202E\n"),
        (b"\xff\xfe not UTF-8\n", b"\\xFF\\xFE not UTF-8\n"),
        (b"\xed\xa0\x80 a surrogate\n", b"\\xED\\xA0\\x80 a surrogate\n"),
        (b"cut short \xf3\xa0", b"cut short \\xF3\\xA0"),
        (b"no line feed at the end", b"no line feed at the end"),
        (b"", b""),
    ],
    ids=[
        "plain text",
        "tag characters",
        "a variation selector",
        "an escape character",
        "a carriage return and a tab",
        "a null and a delete",
        "a letter and punctuation",
        "bytes that are not UTF-8",
        "an encoded surrogate",
        "a character cut short",
        "no line feed at the end",
        "nothing",
    ],
)
def test_what_a_command_prints_is_written_in_printable_ascii(printed: bytes, logged: bytes) -> None:
    run = through_the_filter(*printing(printed))
    assert (run.returncode, run.stdout, run.stderr) == (0, logged, b"")
    assert printable(run.stdout)


def test_what_a_command_prints_as_its_errors_is_written_too_in_its_order() -> None:
    run = through_the_filter(*printing(b"out\n", f"err{HIDDEN}\n".encode()))
    assert (run.returncode, run.stdout, run.stderr) == (
        0,
        f"out\nerr{HIDDEN_SHOWN}\n".encode(),
        b"",
    )


def test_what_a_command_prints_reaches_the_log_before_the_command_ends(tmp_path: Path) -> None:
    go = tmp_path / "go"
    code = (
        "import pathlib, sys, time\n"
        "print('first', flush=True)\n"
        f"while not pathlib.Path({str(go)!r}).exists():\n"
        "    time.sleep(0.01)\n"
        "print('second', flush=True)\n"
    )
    command = [sys.executable, "-I", str(FILTER), sys.executable, "-I", "-c", code]
    with subprocess.Popen(command, stdout=subprocess.PIPE) as run:
        assert run.stdout is not None
        ready, _, _ = select.select([run.stdout], [], [], 10)
        go.touch()
        assert ready, "the filter wrote nothing before the command ended"
        assert run.stdout.readline() == b"first\n"
        assert run.stdout.read() == b"second\n"
    assert run.returncode == 0


def test_a_character_split_between_two_reads_is_written_once_and_the_rest_as_it_comes() -> None:
    written: list[bytes] = []
    whole = f"a{HIDDEN[0]}b\n".encode()
    relay([whole[:2], whole[2:4], whole[4:]], written.append)
    assert written[0] == b"a"
    assert b"".join(written) == b"aU+E004Fb\n"


@pytest.mark.parametrize("status", [0, 1, 2, 3, 127, 255])
def test_the_step_keeps_the_command_s_exit_status(status: int) -> None:
    assert through_the_filter(*printing(b"", status=status)).returncode == status


@pytest.mark.parametrize("stop", [signal.SIGTERM, signal.SIGKILL], ids=["SIGTERM", "SIGKILL"])
def test_a_command_that_a_signal_stops_exits_with_128_and_the_signal_s_number(
    stop: signal.Signals,
) -> None:
    code = f"import os\nos.kill(os.getpid(), {int(stop)})\n"
    run = through_the_filter(sys.executable, "-I", "-c", code)
    assert (run.returncode, run.stderr) == (128 + int(stop), b"")


@pytest.mark.parametrize("stop", [signal.SIGINT, signal.SIGTERM], ids=["SIGINT", "SIGTERM"])
def test_a_signal_that_stops_the_step_reaches_the_command_and_the_filter_ends_as_it_does(
    stop: signal.Signals,
) -> None:
    """The runner stops a step that it cancels by a signal to the step's process, the
    filter's: the filter passes it on to the command, writes what the command prints until it
    ends, and exits with the command's status, with nothing of its own (R278)."""
    code = (
        "import signal, sys, time\n"
        "def stop(number, frame):\n"
        f"    print('stopped by', number, {HIDDEN!r}, flush=True)\n"
        "    sys.exit(3)\n"
        f"signal.signal({int(stop)}, stop)\n"
        "print('started', flush=True)\n"
        "time.sleep(60)\n"
    )
    command = [sys.executable, "-I", str(FILTER), sys.executable, "-I", "-c", code]
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as run:
        assert run.stdout is not None
        assert run.stdout.readline() == b"started\n"
        run.send_signal(stop)
        output, errors = run.communicate(timeout=30)
    assert (run.returncode, output, errors) == (
        3,
        f"stopped by {int(stop)} {HIDDEN_SHOWN}\n".encode(),
        b"",
    )


def test_a_signal_that_stops_the_command_it_passes_on_ends_the_step_with_128_and_its_number() -> (
    None
):
    code = "import time\nprint('started', flush=True)\ntime.sleep(60)\n"
    command = [sys.executable, "-I", str(FILTER), sys.executable, "-I", "-c", code]
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as run:
        assert run.stdout is not None
        assert run.stdout.readline() == b"started\n"
        run.send_signal(signal.SIGTERM)
        output, errors = run.communicate(timeout=30)
    assert (run.returncode, output, errors) == (128 + signal.SIGTERM, b"", b"")


@pytest.mark.parametrize(
    ("executable", "error"),
    [(False, "FileNotFoundError"), (True, "PermissionError")],
    ids=["missing", "not executable"],
)
def test_a_command_that_cannot_be_started_exits_127_and_says_so(
    tmp_path: Path, executable: bool, error: str
) -> None:
    command = tmp_path / f"program{HIDDEN}"
    if executable:
        command.write_text("not a program\n", encoding="utf-8")
        command.chmod(0o644)
    run = through_the_filter(str(command))
    assert (run.returncode, run.stderr) == (127, b"")
    assert run.stdout == (
        f"printable_log: could not start {tmp_path}/program{HIDDEN_SHOWN}: {error}\n".encode()
    )


def test_a_filter_given_no_command_says_so() -> None:
    run = through_the_filter()
    assert (run.returncode, run.stdout, run.stderr) == (
        2,
        b"printable_log: no command to run\n",
        b"",
    )


def test_a_path_that_ruff_quotes_as_it_is_reaches_the_log_by_its_code_points(
    tmp_path: Path,
) -> None:
    (tmp_path / f"tool{HIDDEN}.py").write_text("import os\n", encoding="utf-8")
    command = [sys.executable, "-m", "ruff", "check", "--no-cache", "--isolated", "."]
    raw = subprocess.run(command, capture_output=True, check=False, cwd=tmp_path)
    # What the filter exists for: ruff quotes the path as it is.
    assert raw.returncode == 1
    assert HIDDEN.encode() in raw.stdout
    run = through_the_filter(*command, cwd=tmp_path)
    assert (run.returncode, run.stderr) == (1, b"")
    assert printable(run.stdout)
    assert f"tool{HIDDEN_SHOWN}.py".encode() in run.stdout


def shell_problems(name: str, doc: Mapping[Any, Any]) -> list[str]:
    """What lets a command of a workflow print to the log otherwise than through the filter:
    defaults that give its steps another shell, a job or a step that gives one of its own,
    but the step of the job `ci` that checks the filter from outside it, and a command that a
    job runs before it checks out the repository, which holds the filter (R278)."""
    problems = []
    if ((doc.get("defaults") or {}).get("run") or {}).get("shell") != SHELL:
        problems.append(f"`{name}` does not give its steps the filter's shell")
    for job_name, job in (doc.get("jobs") or {}).items():
        where = f"`{name}`, job `{job_name}`"
        if "shell" in ((job.get("defaults") or {}).get("run") or {}):
            problems.append(f"{where} gives its steps a shell of its own")
        checked_out = False
        for number, step in enumerate(job.get("steps") or [], 1):
            checked_out = checked_out or str(step.get("uses", "")).startswith(CHECKOUT)
            if "shell" in step and not observes(job_name, step):
                problems.append(f"{where}, step {number}, gives a shell of its own")
            if "run" in step and not checked_out:
                problems.append(
                    f"{where}, step {number}, runs a command before the job checks out the filter"
                )
    return problems


def observes(job_name: str, step: Mapping[Any, Any]) -> bool:
    """Whether a step is the one that checks the filter from outside it, in the job `ci`, as
    the test gives it word for word (R278)."""
    return job_name == MERGE_CHECK and dict(step) == {"shell": OBSERVER_SHELL, "run": OBSERVER}


def observer_problems(doc: Mapping[Any, Any]) -> list[str]:
    """Where the job `ci` holds no step that checks the filter from outside it (R278)."""
    steps = ((doc.get("jobs") or {}).get(MERGE_CHECK) or {}).get("steps") or []
    if any(observes(MERGE_CHECK, step) for step in steps):
        return []
    return [f"the job `{MERGE_CHECK}` holds no step that checks the filter from outside it"]


def observed(root: Path, source: str) -> int:
    """What the step that checks the filter exits with, run as GitHub runs it in a checkout
    whose filter holds the source given."""
    (root / "scripts").mkdir()
    (root / "scripts" / "printable_log.py").write_text(source, encoding="utf-8")
    script = root / "step"
    script.write_text(OBSERVER, encoding="utf-8")
    command = shlex.split(GITHUB_BASH.replace("{0}", str(script)))
    return subprocess.run(command, cwd=root, capture_output=True, check=False).returncode


def test_the_step_that_checks_the_filter_passes_the_filter(tmp_path: Path) -> None:
    assert observed(tmp_path, FILTER.read_text(encoding="utf-8")) == 0


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("    sys.exit(main(sys.argv[1:]))\n", "    main(sys.argv[1:])\n"),
        ("    return 128 - status if status < 0 else status\n", "    return max(status, 0)\n"),
        ("    return 128 - status if status < 0 else status\n", "    return 1 if status else 0\n"),
        ("    return 128 - status if status < 0 else status\n", "    return 0\n"),
    ],
    ids=["the status dropped", "a signal's status dropped", "each failure made 1", "always 0"],
)
def test_the_step_that_checks_the_filter_fails_a_filter_that_loses_the_status(
    tmp_path: Path, old: str, new: str
) -> None:
    source = FILTER.read_text(encoding="utf-8")
    assert source.count(old) == 1
    assert observed(tmp_path, source.replace(old, new)) == 1


def ci_with(*steps: dict[str, Any], job: str = MERGE_CHECK) -> dict[str, Any]:
    """A workflow whose one job, the job `ci` unless another is given, checks out the
    repository and then takes the steps given."""
    return {
        "defaults": {"run": {"shell": SHELL}},
        "jobs": {job: {"steps": [{"uses": f"{CHECKOUT}0123"}, *steps]}},
    }


OBSERVING = {"shell": OBSERVER_SHELL, "run": OBSERVER}


@pytest.mark.parametrize(
    ("doc", "shells", "observers"),
    [
        (ci_with(OBSERVING, {"run": "pytest"}), [], []),
        (
            ci_with({"run": "pytest"}),
            [],
            [f"the job `{MERGE_CHECK}` holds no step that checks the filter from outside it"],
        ),
        (
            ci_with({"shell": OBSERVER_SHELL, "run": OBSERVER + "true\n"}),
            ["`w.yml`, job `ci`, step 2, gives a shell of its own"],
            [f"the job `{MERGE_CHECK}` holds no step that checks the filter from outside it"],
        ),
        (
            ci_with({"shell": "sh", "run": OBSERVER}),
            ["`w.yml`, job `ci`, step 2, gives a shell of its own"],
            [f"the job `{MERGE_CHECK}` holds no step that checks the filter from outside it"],
        ),
        (
            ci_with({**OBSERVING, "env": {"BASH_ENV": "a.sh"}}),
            ["`w.yml`, job `ci`, step 2, gives a shell of its own"],
            [f"the job `{MERGE_CHECK}` holds no step that checks the filter from outside it"],
        ),
        (
            ci_with(OBSERVING, job="python"),
            ["`w.yml`, job `python`, step 2, gives a shell of its own"],
            [f"the job `{MERGE_CHECK}` holds no step that checks the filter from outside it"],
        ),
    ],
    ids=[
        "as CI gives it",
        "no such step",
        "another script",
        "another shell",
        "another key",
        "another job",
    ],
)
def test_only_the_step_of_the_job_ci_that_checks_the_filter_runs_outside_it(
    doc: dict[str, Any], shells: list[str], observers: list[str]
) -> None:
    assert (shell_problems("w.yml", doc), observer_problems(doc)) == (shells, observers)


def test_ci_checks_the_filter_from_outside_it() -> None:
    path = ROOT / ".github" / "workflows" / "ci.yml"
    assert observer_problems(load_workflow(path.read_text(encoding="utf-8"))) == []


def planted(**changes: Any) -> dict[str, Any]:
    """A workflow whose one job checks out the repository and runs a command, as each
    workflow here does, with the keys given changed."""
    doc: dict[str, Any] = {
        "defaults": {"run": {"shell": SHELL}},
        "jobs": {"check": {"steps": [{"uses": f"{CHECKOUT}0123"}, {"run": "pytest"}]}},
    }
    doc.update(changes)
    return doc


@pytest.mark.parametrize(
    ("doc", "problems"),
    [
        (planted(), []),
        (planted(jobs={"only": {"steps": [{"uses": "actions/setup-python@0123"}]}}), []),
        (planted(jobs={}), []),
        ({"jobs": {}}, ["`w.yml` does not give its steps the filter's shell"]),
        (
            planted(defaults={"run": {"shell": "bash"}}),
            ["`w.yml` does not give its steps the filter's shell"],
        ),
        (planted(defaults={"run": {}}), ["`w.yml` does not give its steps the filter's shell"]),
        (
            planted(
                jobs={
                    "check": {
                        "defaults": {"run": {"shell": "bash"}},
                        "steps": [{"uses": f"{CHECKOUT}0123"}, {"run": "pytest"}],
                    }
                }
            ),
            ["`w.yml`, job `check` gives its steps a shell of its own"],
        ),
        (
            planted(
                jobs={
                    "check": {"steps": [{"uses": f"{CHECKOUT}0123"}, {"run": "x", "shell": "sh"}]}
                }
            ),
            ["`w.yml`, job `check`, step 2, gives a shell of its own"],
        ),
        (
            planted(jobs={"check": {"steps": [{"run": "x"}, {"uses": f"{CHECKOUT}0123"}]}}),
            ["`w.yml`, job `check`, step 1, runs a command before the job checks out the filter"],
        ),
        (
            planted(jobs={"check": {"steps": [{"run": "x"}]}}),
            ["`w.yml`, job `check`, step 1, runs a command before the job checks out the filter"],
        ),
    ],
)
def test_a_step_whose_output_does_not_go_through_the_filter_is_named(
    doc: dict[str, Any], problems: list[str]
) -> None:
    assert shell_problems("w.yml", doc) == problems


def test_every_workflow_runs_its_commands_through_the_filter() -> None:
    paths = workflows()
    assert paths, "no workflow was read"
    problems = [
        problem
        for path in paths
        for problem in shell_problems(
            path.relative_to(ROOT).as_posix(), load_workflow(path.read_text(encoding="utf-8"))
        )
    ]
    assert problems == []
