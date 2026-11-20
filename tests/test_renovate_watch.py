"""Tests of the daily check of Renovate's proposals (R263, DR-267, design decision 22).

No test uses the network or the clock: every response is a recorded or synthetic one,
given through the check's one fetch function, and every time is given."""

from __future__ import annotations

import http.client
import json
import re
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest
import renovate_watch as watch
import yaml

ROOT = Path(__file__).resolve().parents[1]
RECORDED = ROOT / "tests" / "fixtures" / "renovate-watch"
WORKFLOW = ROOT / ".github" / "workflows" / "renovate-watch.yml"
REPO = "owner/repo"
API = "https://api.github.com"
NOW = datetime(2026, 11, 20, 6, 0, tzinfo=UTC)


def recorded(name: str) -> Any:
    return json.loads((RECORDED / name).read_text(encoding="utf-8"))


def at(days_ago: float) -> str:
    return (NOW - timedelta(days=days_ago)).isoformat().replace("+00:00", "Z")


def pypi(*releases: tuple[str, float] | tuple[str, float, bool]) -> dict[str, Any]:
    """A Python Package Index document whose releases were each published so many days
    before NOW, and are yanked where a third value says so."""
    return {
        "releases": {
            version: [{"upload_time_iso_8601": at(age), "yanked": bool(rest and rest[0])}]
            for version, age, *rest in releases
        }
    }


def npm(*releases: tuple[str, float] | tuple[str, float, str]) -> dict[str, Any]:
    """An npm registry document whose versions were each published so many days before
    NOW, and are deprecated where a third value gives the reason."""
    return {
        "versions": {
            version: {"version": version, **({"deprecated": rest[0]} if rest else {})}
            for version, _, *rest in releases
        },
        "time": {"created": at(400), "modified": at(0)} | {v: at(age) for v, age, *_ in releases},
    }


def pull(
    title: str,
    days_ago: float,
    login: str = "renovate[bot]",
    state: str = "open",
    number: int = 1,
) -> dict[str, Any]:
    return {
        "number": number,
        "title": title,
        "user": {"login": login},
        "state": state,
        "created_at": at(days_ago),
        "updated_at": at(0),
        "head": {"sha": f"{number:040x}"},
    }


def dashboard(days_ago: float = 0) -> dict[str, Any]:
    return {
        "number": 4,
        "title": "Dependency Dashboard",
        "user": {"login": "renovate[bot]"},
        "updated_at": at(days_ago),
    }


def commit(
    days_ago: float, login: str | None = "renovate[bot]", committed: float | None = None
) -> dict[str, Any]:
    """A head commit as GitHub gives it, authored so many days before NOW by `login`, and
    committed then too unless `committed` says otherwise."""
    return {
        "author": {"login": login} if login else None,
        "commit": {
            "author": {"date": at(days_ago)},
            "committer": {"date": at(days_ago if committed is None else committed)},
        },
    }


def tree(
    tmp_path: Path,
    requirements: str,
    dev: dict[str, str] | None = None,
    runtime: dict[str, str] | None = None,
) -> Path:
    (tmp_path / "requirements-dev.txt").write_text(requirements, encoding="utf-8")
    package: dict[str, Any] = {"name": "x", "private": True, "devDependencies": dev or {}}
    if runtime is not None:
        package["dependencies"] = runtime
    (tmp_path / "package.json").write_text(json.dumps(package), encoding="utf-8")
    return tmp_path


def server(responses: dict[str, Any]) -> tuple[watch.Fetch, list[str]]:
    """A fetch function that answers each URL from `responses` and records what was asked.
    A URL that it does not hold fails, as a request that fails would."""
    asked: list[str] = []

    def fetch(url: str) -> watch.Response:
        asked.append(url)
        if url not in responses:
            raise watch.ReadError(f"could not read {url}")
        body = responses[url]
        if isinstance(body, watch.Response):
            return body
        return watch.Response(json.dumps(body).encode(), None)

    return fetch, asked


def urls(
    pypi_docs: dict[str, Any] | None = None,
    npm_docs: dict[str, Any] | None = None,
    pulls: list[dict[str, Any]] | None = None,
    issues: list[dict[str, Any]] | None = None,
    commits: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The responses for one run. Each open pull request of Renovate's gets a head commit
    that Renovate authored when it opened it, unless `commits` gives another by its SHA."""
    found: dict[str, Any] = {}
    for name, doc in (pypi_docs or {}).items():
        found[f"https://pypi.org/pypi/{name}/json"] = doc
    for name, doc in (npm_docs or {}).items():
        found[f"https://registry.npmjs.org/{name.replace('/', '%2F')}"] = doc
    found[f"{API}/repos/{REPO}/pulls?state=all&per_page=100"] = pulls or []
    found[f"{API}/repos/{REPO}/issues?state=open&creator=renovate%5Bbot%5D&per_page=100"] = (
        issues if issues is not None else [dashboard(1)]
    )
    for item in pulls if isinstance(pulls, list) else []:
        if isinstance(item, dict) and item.get("state") == "open" and item.get("head"):
            sha = item["head"]["sha"]
            days = (NOW - watch.moment(item["created_at"])) / timedelta(days=1)
            found[f"{API}/repos/{REPO}/commits/{sha}"] = commit(days)
    for sha, body in (commits or {}).items():
        found[f"{API}/repos/{REPO}/commits/{sha}"] = body
    return found


def run(root: Path, responses: dict[str, Any], now: datetime = NOW) -> list[str]:
    fetch, _ = server(responses)
    return watch.check(root, fetch, now, REPO, API)


# --- The pins it reads ------------------------------------------------------------


def test_the_pins_are_read_from_both_files(tmp_path: Path) -> None:
    root = tree(
        tmp_path,
        "# A comment.\n\nmypy==2.4.0  # why\nTypes_PyYAML==6.0.12.20260906\n",
        {"@fission-ai/openspec": "1.15.0"},
    )
    assert watch.pins(root) == [
        watch.Pin("mypy", "2.4.0", "pypi"),
        watch.Pin("Types_PyYAML", "6.0.12.20260906", "pypi"),
        watch.Pin("@fission-ai/openspec", "1.15.0", "npm"),
    ]


def test_a_package_s_runtime_dependencies_are_pins_too(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n", {"a": "1.0.0"}, {"b": "2.0.0"})
    assert [pin.name for pin in watch.pins(root)] == ["mypy", "a", "b"]


@pytest.mark.parametrize("section", [[], "x", {"a": 1}])
def test_a_package_section_that_cannot_be_read_fails(tmp_path: Path, section: Any) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    package = {"devDependencies": section}
    (root / "package.json").write_text(json.dumps(package), encoding="utf-8")
    with pytest.raises(watch.ReadError, match="package.json"):
        watch.pins(root)


def test_this_repository_s_pins_are_read() -> None:
    found = watch.pins(ROOT)
    assert {pin.registry for pin in found} == {"pypi", "npm"}
    assert all(watch.numbers(pin.version) for pin in found), found


@pytest.mark.parametrize(
    "line",
    [
        "mypy>=2.4.0",
        "mypy",
        "-r other.txt",
        "mypy==2.4.0; python_version<'3.12'",
        "mypy==2.*",
        "mypy==2.4.0 --hash=sha256:00",
        "mypy==\uff12.4.0",
    ],
)
def test_a_requirement_that_is_not_an_exact_pin_fails(tmp_path: Path, line: str) -> None:
    with pytest.raises(watch.ReadError, match="requirements-dev.txt"):
        watch.pins(tree(tmp_path, line + "\n"))


@pytest.mark.parametrize("version", ["^1.15.0", "~1.15.0", "latest", "1.15.0-beta.1"])
def test_a_package_that_is_not_an_exact_pin_fails(tmp_path: Path, version: str) -> None:
    with pytest.raises(watch.ReadError, match="package.json"):
        watch.pins(tree(tmp_path, "mypy==2.4.0\n", {"x": version}))


def test_a_tree_with_no_pin_fails(tmp_path: Path) -> None:
    with pytest.raises(watch.ReadError, match="no pinned tool"):
        watch.pins(tree(tmp_path, "# nothing\n"))


@pytest.mark.parametrize("name", ["requirements-dev.txt", "package.json"])
def test_a_missing_file_fails(tmp_path: Path, name: str) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    (root / name).unlink()
    with pytest.raises(watch.ReadError, match=re.escape(name)):
        watch.pins(root)


def test_a_package_json_that_cannot_be_read_fails(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    (root / "package.json").write_text("{", encoding="utf-8")
    with pytest.raises(watch.ReadError, match="package.json"):
        watch.pins(root)


# --- Versions -----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        ("2.4.1", (2, 4, 1)),
        ("6.0.12.20261103", (6, 0, 12, 20261103)),
        ("1", (1,)),
        ("1.0.0", (1,)),
        ("2.4.0", (2, 4)),
        ("0.0", (0,)),
        ("0.17.2", (0, 17, 2)),
        ("2.4.1rc1", None),
        ("1.6.0-beta.1", None),
        ("2.4.1.post1", None),
        ("1!2.0", None),
        ("v2.4.1", None),
        ("2..4", None),
        ("\uff12.\uff14.\uff11", None),
        pytest.param("2.4." + "9" * 5000, None, id="a part of 5000 digits"),
        ("", None),
    ],
)
def test_a_version_is_compared_by_its_numbers_alone(
    version: str, expected: tuple[int, ...] | None
) -> None:
    assert watch.numbers(version) == expected


def test_versions_compare_as_numbers_not_as_text() -> None:
    assert watch.numbers("1.0") == watch.numbers("1.0.0")
    assert watch.numbers("2.10.0") > watch.numbers("2.9.0")  # type: ignore[operator]
    assert watch.numbers("6.0.12.20261103") > watch.numbers("6.0.12.20260906")  # type: ignore[operator]


# --- Releases -----------------------------------------------------------------------


def test_the_recorded_pypi_document_gives_each_release_and_its_day() -> None:
    releases = watch.pypi_releases(recorded("pypi-mypy.json"))
    assert releases["2.4.1"] == datetime(2026, 10, 28, 19, 21, 4, 779148, tzinfo=UTC)
    assert set(releases) == {"2.3.1", "2.4.0", "2.4.1"}


def test_a_pypi_release_is_dated_by_its_earliest_file_and_a_yanked_one_is_left_out() -> None:
    doc = {
        "releases": {
            "1.0": [
                {"upload_time_iso_8601": at(3), "yanked": False},
                {"upload_time_iso_8601": at(5), "yanked": False},
            ],
            "1.1": [{"upload_time_iso_8601": at(30), "yanked": True}],
            "1.2": [],
        }
    }
    assert watch.pypi_releases(doc) == {"1.0": NOW - timedelta(days=5)}


def test_the_recorded_npm_document_gives_each_version_and_its_day() -> None:
    releases = watch.npm_releases(recorded("npm-openspec.json"))
    assert "created" not in releases and "modified" not in releases
    assert releases["1.16.0"].tzinfo is not None
    assert set(releases) == {"1.15.0", "1.16.0", "1.16.1", "1.17.0", "2.0.0", "2.1.0", "2.1.1"}


def test_a_deprecated_npm_version_is_left_out() -> None:
    releases = watch.npm_releases(npm(("1.0.0", 30), ("1.1.0", 30, "broken")))
    assert set(releases) == {"1.0.0"}


@pytest.mark.parametrize(
    "doc",
    [
        [],
        {},
        {"releases": []},
        {"releases": {"1.0": [{"yanked": False}]}},
        {"releases": {"1.0": [{"upload_time_iso_8601": "yesterday", "yanked": False}]}},
        {"releases": {"1.0": [{"upload_time_iso_8601": "2026-11-01T00:00:00", "yanked": False}]}},
    ],
)
def test_a_pypi_document_that_cannot_be_read_fails(doc: Any) -> None:
    with pytest.raises(watch.ReadError):
        watch.pypi_releases(doc)


@pytest.mark.parametrize(
    "doc",
    [
        [],
        {"versions": {}},
        {"versions": {"1.0.0": {}}, "time": {}},
        {"versions": {"1.0.0": {}}, "time": {"1.0.0": 5}},
        {"versions": [], "time": {}},
    ],
)
def test_an_npm_document_that_cannot_be_read_fails(doc: Any) -> None:
    with pytest.raises(watch.ReadError):
        watch.npm_releases(doc)


# --- Scenario: An update that Renovate has not proposed in time fails the check ------


@pytest.mark.parametrize(
    ("pypi_doc", "npm_doc"),
    [
        ({"releases": {}}, None),
        (pypi(("2.4.1rc1", 30)), None),
        (pypi(("2.4.1", 30)), None),
        (pypi(("2.4.0", 60), ("2.4.1", 30)), {"versions": {}, "time": {}}),
        (pypi(("2.4.0", 60), ("2.4.1", 30)), npm(("1.16.0", 30))),
    ],
)
def test_a_document_without_the_pin_is_named_as_not_read_and_the_rest_still_checked(
    tmp_path: Path, pypi_doc: dict[str, Any], npm_doc: dict[str, Any] | None
) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n", {"x": "1.15.0"})
    other = npm_doc if npm_doc is not None else npm(("1.15.0", 60))
    found = run(root, urls({"mypy": pypi_doc}, {"x": other}, pulls=[pull("y", 9, state="closed")]))
    reader = "mypy" if npm_doc is None else "x"
    assert [f.split(":")[0] for f in found if not f.startswith("overdue")] == ["not read", "quiet"]
    assert f"not read: {reader} " in "\n".join(found), found


def test_an_overdue_update_is_named_with_its_pin_version_and_day(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    found = run(root, urls({"mypy": pypi(("2.4.0", 60), ("2.4.1", 18))}, pulls=[pull("x", 1)]))
    day = (NOW - timedelta(days=18)).date().isoformat()
    assert found == [
        f"overdue update: mypy 2.4.0 to 2.4.1, published {day}, has no pull request from Renovate"
    ]


def test_the_recorded_responses_name_what_was_wrong_during_the_stop(tmp_path: Path) -> None:
    # As at 2026-11-18, during the stop: Renovate's last pull request then was opened on
    # 2026-11-09, and those that propose these updates were opened on 2026-11-20.
    root = tree(tmp_path, "mypy==2.4.0\n", {"@fission-ai/openspec": "1.15.0"})
    responses = urls(
        {"mypy": recorded("pypi-mypy.json")},
        {"@fission-ai/openspec": recorded("npm-openspec.json")},
        pulls=recorded("github-pulls.json"),
        issues=recorded("github-issues.json"),
    )
    assert run(root, responses, now=datetime(2026, 11, 18, tzinfo=UTC)) == [
        "overdue update: mypy 2.4.0 to 2.4.1, published 2026-10-28, has no pull request"
        " from Renovate",
        "overdue update: @fission-ai/openspec 1.15.0 to 1.16.0, published 2026-10-30, has no"
        " pull request from Renovate",
        "quiet: Renovate has opened no pull request, and authored no commit on its open ones,"
        " since 2026-11-09 13:43 UTC",
    ]


def test_an_overdue_npm_update_is_named(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n", {"@fission-ai/openspec": "1.15.0"})
    responses = urls(
        {"mypy": pypi(("2.4.0", 60))},
        {"@fission-ai/openspec": npm(("1.15.0", 60), ("1.16.0", 20), ("2.0.0", 20))},
        pulls=[pull("x", 1)],
    )
    assert run(root, responses) == [
        "overdue update: @fission-ai/openspec 1.15.0 to 1.16.0, published"
        f" {(NOW - timedelta(days=20)).date().isoformat()}, has no pull request from Renovate"
    ]


def test_the_newest_overdue_release_is_the_one_named(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    doc = pypi(("2.4.0", 90), ("2.4.1", 60), ("2.10.0", 30), ("2.9.0", 40), ("2.11.0", 2))
    found = run(root, urls({"mypy": doc}, pulls=[pull("x", 1)]))
    assert [f.split(",")[0] for f in found] == ["overdue update: mypy 2.4.0 to 2.10.0"]


@pytest.mark.parametrize(
    "title",
    [
        "Update dependency mypy to v2.4.0",
        "Update dependency mypy to v2.4.1rc1",
        "Update dependency mypyx to v2.4.1",
        "Update dependency mypy to v2.4.1 for review",
        "update mypy to 2.4.1",
        "Update dependency mypy-extensions to v2.4.1",
        "Update dependency mypy to v2.4.1x",
    ],
)
def test_a_pull_request_that_does_not_propose_the_update_leaves_it_overdue(
    tmp_path: Path, title: str
) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    found = run(root, urls({"mypy": pypi(("2.4.0", 60), ("2.4.1", 18))}, pulls=[pull(title, 1)]))
    assert len(found) == 1 and found[0].startswith("overdue update: mypy"), found


def test_a_pull_request_that_someone_else_opened_proposes_nothing(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    others = [pull("Update dependency mypy to v2.4.1", 1, login="someone"), pull("x", 1)]
    found = run(root, urls({"mypy": pypi(("2.4.0", 60), ("2.4.1", 18))}, pulls=others))
    assert len(found) == 1 and found[0].startswith("overdue update: mypy"), found


def test_a_pin_whose_version_cannot_be_compared_is_refused() -> None:
    with pytest.raises(watch.ReadError, match="no version of numbers"):
        watch.overdue(watch.Pin("x", "1.0rc1", "pypi"), {}, [], NOW, ["1.0rc1"])


def test_a_withdrawn_pin_still_has_its_overdue_update_named(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n", {"x": "1.15.0"})
    responses = urls(
        {"mypy": pypi(("2.4.0", 60, True), ("2.4.1", 30))},
        {"x": npm(("1.15.0", 60, "broken"), ("1.16.0", 30))},
        pulls=[pull("y", 1)],
    )
    assert [f.split(",")[0] for f in run(root, responses)] == [
        "overdue update: mypy 2.4.0 to 2.4.1",
        "overdue update: x 1.15.0 to 1.16.0",
    ]


# --- Scenario: An update inside its wait, a major update or one already proposed passes


@pytest.mark.parametrize(
    "releases",
    [
        [("2.4.0", 60), ("2.4.1", 17)],
        [("2.4.0", 60), ("2.4.1", 3)],
        [("2.4.0", 60), ("3.0.0", 60)],
        [("2.4.0", 60), ("2.4.1rc1", 60)],
        [("2.4.0", 60), ("2.4.1", 60, True)],
        [("2.4.0", 60), ("2.3.9", 30)],
        [("2.4.0", 60)],
    ],
)
def test_an_update_inside_its_wait_a_major_a_pre_release_or_a_withdrawn_one_passes(
    tmp_path: Path, releases: list[Any]
) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    assert run(root, urls({"mypy": pypi(*releases)}, pulls=[pull("x", 1)])) == []


def test_a_deprecated_npm_version_is_not_overdue(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n", {"@fission-ai/openspec": "1.15.0"})
    responses = urls(
        {"mypy": pypi(("2.4.0", 60))},
        {"@fission-ai/openspec": npm(("1.15.0", 60), ("1.16.0", 30, "broken"))},
        pulls=[pull("x", 1)],
    )
    assert run(root, responses) == []


@pytest.mark.parametrize(
    ("title", "state"),
    [
        ("Update dependency mypy to v2.4.1", "open"),
        ("Update dependency mypy to v2.4.1", "closed"),
        ("Update dependency mypy to v2.5.0", "closed"),
        ("chore(deps): update dependency mypy to v2.4.1", "open"),
        ("Update dependency mypy to v2.4.1 [SECURITY]", "open"),
        ("Update dependency mypy to v2.4.1 - autoclosed", "closed"),
        ("Update dependency mypy to v2.4.1 - abandoned", "open"),
        ("Update dependency MyPy to v2.4.1", "open"),
    ],
)
def test_an_update_that_renovate_proposed_passes(tmp_path: Path, title: str, state: str) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    proposed = pull(title, 40, state=state, number=2)
    responses = urls({"mypy": pypi(("2.4.0", 60), ("2.4.1", 18))}, pulls=[proposed, pull("x", 1)])
    assert run(root, responses) == []


def test_a_python_tool_s_name_is_compared_as_the_package_index_compares_it(
    tmp_path: Path,
) -> None:
    root = tree(tmp_path, "Types_PyYAML==6.0.12.20260906\n")
    proposed = pull("Update dependency types-pyyaml to v6.0.12.20261103", 30, number=2)
    doc = pypi(("6.0.12.20260906", 60), ("6.0.12.20261103", 20))
    responses = urls({"Types_PyYAML": doc}, pulls=[proposed, pull("x", 1)])
    assert run(root, responses) == []


def test_a_closed_pull_request_for_a_major_update_hides_no_minor_one(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    major = pull("Update dependency mypy to v3", 40, state="closed", number=2)
    major3 = pull("Update dependency mypy to v3.0.0", 40, state="closed", number=3)
    responses = urls(
        {"mypy": pypi(("2.4.0", 60), ("2.4.1", 18), ("3.0.0", 40))},
        pulls=[major, major3, pull("x", 1)],
    )
    found = run(root, responses)
    assert [f.split(",")[0] for f in found] == ["overdue update: mypy 2.4.0 to 2.4.1"]


def test_the_recorded_pull_requests_propose_the_updates_that_they_name(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\nruff==0.17.2\n", {"@fission-ai/openspec": "1.15.0"})
    responses = urls(
        {"mypy": pypi(("2.4.0", 60), ("2.4.1", 30)), "ruff": pypi(("0.17.2", 60), ("0.17.4", 30))},
        {"@fission-ai/openspec": npm(("1.15.0", 60), ("1.16.0", 30))},
        pulls=recorded("github-pulls.json"),
        issues=recorded("github-issues.json"),
    )
    sha = recorded("github-commit.json")["sha"]
    responses[f"{API}/repos/{REPO}/commits/{sha}"] = recorded("github-commit.json")
    assert run(root, responses, now=datetime(2026, 11, 21, tzinfo=UTC)) == []


# --- Scenario: Five quiet days fail the check ---------------------------------------


def test_five_quiet_days_are_named_with_the_last_activity(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    opened = pull("x", 9)
    responses = urls(
        {"mypy": pypi(("2.4.0", 60))}, pulls=[opened], commits={opened["head"]["sha"]: commit(5.5)}
    )
    last = (NOW - timedelta(days=5.5)).strftime("%Y-%m-%d %H:%M")
    assert run(root, responses) == [
        "quiet: Renovate has opened no pull request, and authored no commit on its open ones,"
        f" since {last} UTC"
    ]


def test_exactly_five_days_is_not_yet_quiet_and_a_second_more_is(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    assert run(root, urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", 5)])) == []
    past = 5 + 1 / 86400
    found = run(root, urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", past)]))
    assert [f.split(":")[0] for f in found] == ["quiet"]


def test_exactly_seventeen_days_is_not_yet_overdue_and_a_second_more_is(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    recent = [pull("x", 1)]
    assert run(root, urls({"mypy": pypi(("2.4.0", 60), ("2.4.1", 17))}, pulls=recent)) == []
    past = 17 + 1 / 86400
    found = run(root, urls({"mypy": pypi(("2.4.0", 60), ("2.4.1", past))}, pulls=recent))
    assert [f.split(",")[0] for f in found] == ["overdue update: mypy 2.4.0 to 2.4.1"]


def test_a_commit_that_renovate_authored_long_ago_and_someone_rebased_today_is_quiet(
    tmp_path: Path,
) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    item = pull("x", 9)
    commits = {item["head"]["sha"]: commit(9, committed=0)}
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[item], commits=commits)
    assert [f.split(":")[0] for f in run(root, responses)] == ["quiet"]


@pytest.mark.parametrize(
    ("opened", "state", "authored"),
    [(4.9, "closed", None), (9, "open", 4.9), (0, "open", 0), (4, "open", 30)],
)
def test_recent_activity_of_renovate_passes(
    tmp_path: Path, opened: float, state: str, authored: float | None
) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    item = pull("x", opened, state=state)
    commits = {item["head"]["sha"]: commit(authored)} if authored is not None else {}
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[item], commits=commits)
    assert run(root, responses) == []


def test_what_others_do_on_renovate_s_pull_requests_and_dashboard_is_not_its_activity(
    tmp_path: Path,
) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    # Renovate opened its pull request 9 days ago; since then someone opened one of their
    # own, pushed to Renovate's, and the dashboard and the pull request changed today.
    renovates = pull("x", 9, number=1)
    others = pull("y", 0, login="someone", number=2)
    issues = [dashboard(0), dashboard(0) | {"user": {"login": "someone"}, "number": 5}]
    commits = {renovates["head"]["sha"]: commit(0, login="someone")}
    responses = urls(
        {"mypy": pypi(("2.4.0", 60))}, pulls=[renovates, others], issues=issues, commits=commits
    )
    assert [f.split(":")[0] for f in run(root, responses)] == ["quiet"]


def test_a_commit_with_no_author_on_github_is_not_renovate_s(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    item = pull("x", 9)
    commits = {item["head"]["sha"]: commit(0, login=None)}
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[item], commits=commits)
    assert [f.split(":")[0] for f in run(root, responses)] == ["quiet"]


def test_both_signals_are_named_together(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    found = run(
        root,
        urls({"mypy": pypi(("2.4.0", 60), ("2.4.1", 20))}, pulls=[pull("x", 6, state="closed")]),
    )
    assert [f.split(":")[0] for f in found] == ["overdue update", "quiet"]


# --- Scenario: A check run as at another time reads only what existed then ----------


def test_a_pull_request_opened_after_the_check_s_time_is_left_out(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    later = pull("Update dependency mypy to v2.4.1", 1, number=2)
    responses = urls(
        {"mypy": pypi(("2.4.0", 60), ("2.4.1", 30))}, pulls=[pull("x", 5, state="closed"), later]
    )
    then = NOW - timedelta(days=2)
    found = run(root, responses, now=then)
    assert [f.split(",")[0] for f in found] == ["overdue update: mypy 2.4.0 to 2.4.1"]


def test_a_commit_authored_after_the_check_s_time_is_left_out(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    item = pull("x", 20)
    commits = {item["head"]["sha"]: commit(0)}
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[item], commits=commits)
    assert [f.split(":")[0] for f in run(root, responses, now=NOW - timedelta(days=7))] == ["quiet"]


def test_a_day_in_the_future_finds_renovate_quiet(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", 0)])
    found = run(root, responses, now=NOW + timedelta(days=30))
    assert [f.split(":")[0] for f in found] == ["quiet"]


# --- Scenario: Text from a response never reaches the run's commands or summary ------


def test_text_from_a_response_never_reaches_the_output(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "t").mkdir()
    root = tree(tmp_path / "t", "mypy==2.4.0\n")
    planted = "::stop-commands::x [click](https://example.com)"
    hostile = [
        pull(f"Update dependency mypy to v{planted}", 30, number=2),
        pull(planted, 30, number=3, state="closed"),
        pull("x", 9, state="closed"),
    ]
    doc = pypi(("2.4.0", 60), ("2.4.1", 30), (planted, 30))
    issues = [dashboard() | {"title": planted}, dashboard()]
    fetch, _ = server(urls({"mypy": doc}, pulls=hostile, issues=issues))
    assert watch.main(["--root", str(root)], environment(tmp_path), fetch, lambda: NOW) == 1
    out = capsys.readouterr().out
    summary = (tmp_path / "summary.md").read_text(encoding="utf-8")
    for text in (out, summary):
        assert "overdue update: mypy" in text and "quiet:" in text
        assert "::" not in text and "example.com" not in text and "](" not in text


def test_an_error_names_no_text_from_a_response(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "t").mkdir()
    root = tree(tmp_path / "t", "mypy==2.4.0\n")
    responses = urls({"mypy": {"releases": {"::x::": [{"upload_time_iso_8601": "::y::"}]}}})
    responses[f"{API}/repos/{REPO}/pulls?state=all&per_page=100"] = [pull("x", 1)]
    fetch, _ = server(responses)
    assert watch.main(["--root", str(root)], environment(tmp_path), fetch, lambda: NOW) == 1
    assert "::" not in capsys.readouterr().out


# --- Scenario: A check that cannot read fails ---------------------------------------


def test_a_registry_that_cannot_be_read_is_named_and_the_rest_still_checked(
    tmp_path: Path,
) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    found = run(root, urls(pulls=[pull("x", 9, state="closed")]))
    assert [f.split(":")[0] for f in found] == ["not read", "quiet"]
    assert found[0].startswith("not read: mypy 2.4.0: could not read https://pypi.org/pypi/mypy/")


@pytest.mark.parametrize(
    "body",
    [b"", b"<html>", b"[1,", b"\xff", pytest.param(b"[" * 200_000, id="nested 200000 deep")],
)
def test_a_response_that_is_not_json_fails_the_check(tmp_path: Path, body: bytes) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    responses = urls({"mypy": watch.Response(body, None)}, pulls=[pull("x", 1)])
    found = run(root, responses)
    assert len(found) == 1 and found[0].startswith("not read: mypy 2.4.0: could not read"), found


def test_a_registry_that_did_not_answer_is_not_asked_again(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\nruff==0.17.2\n", {"x": "1.15.0"})
    responses = urls(npm_docs={"x": npm(("1.15.0", 60))}, pulls=[pull("y", 9, state="closed")])
    fetch, asked = server(responses)
    found = watch.check(root, fetch, NOW, REPO, API)
    assert [url for url in asked if "pypi.org" in url] == ["https://pypi.org/pypi/mypy/json"]
    assert found == [
        "not read: mypy 2.4.0: could not read https://pypi.org/pypi/mypy/json",
        "not read: ruff 0.17.2: pypi.org did not answer an earlier request",
        found[2],
    ]
    assert found[2].startswith("quiet:")


def test_the_run_s_requests_that_fail_fit_inside_the_job_s_time_limit() -> None:
    # A request that fails costs two timeouts and a pause. GitHub's first failure ends the
    # run, and each registry's host is asked once more at most after it failed.
    hosts = 1 + len({"pypi.org", "registry.npmjs.org"})
    worst = hosts * (2 * watch.TIMEOUT + watch.PAUSE)
    limit = job(workflow())["timeout-minutes"] * 60
    assert worst < limit, (worst, limit)


def test_a_github_response_that_is_not_json_fails_the_check(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", 1)])
    responses[f"{API}/repos/{REPO}/pulls?state=all&per_page=100"] = watch.Response(b"<", None)
    with pytest.raises(watch.ReadError, match="could not read page 1 of"):
        run(root, responses)


@pytest.mark.parametrize(
    "pulls",
    [
        {"a": 1},
        [1],
        [{"title": "x"}],
        [{"title": "x", "user": {"login": "renovate[bot]"}, "created_at": "now"}],
        [pull("x", 1) | {"state": "open", "head": None}],
        [pull("x", 1) | {"head": {"sha": "../../evil"}}],
        [pull("x", 1) | {"head": {"sha": "A" * 40}}],
    ],
)
def test_pull_requests_that_cannot_be_read_fail_the_check(tmp_path: Path, pulls: Any) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    with pytest.raises(watch.ReadError, match="pull"):
        run(root, urls({"mypy": pypi(("2.4.0", 60))}, pulls=pulls))


def test_no_pull_request_of_renovate_s_fails_the_check(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", 1, login="a")])
    with pytest.raises(watch.ReadError, match="no pull request of Renovate's"):
        run(root, responses)


@pytest.mark.parametrize(
    "issues",
    [
        [],
        [dashboard() | {"pull_request": {}}],
        [dashboard() | {"user": {"login": "someone"}}],
        [dashboard() | {"title": "Dependency dashboard (old)"}],
    ],
)
def test_no_open_dashboard_of_renovate_s_fails_the_check(
    tmp_path: Path, issues: list[dict[str, Any]]
) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", 1)], issues=issues)
    with pytest.raises(watch.ReadError, match="no open dependency dashboard"):
        run(root, responses)


@pytest.mark.parametrize(
    "body",
    [{}, {"author": {"login": "renovate[bot]"}}, {"author": 1, "commit": {"committer": {}}}],
)
def test_a_commit_that_cannot_be_read_fails_the_check(tmp_path: Path, body: Any) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    item = pull("x", 1)
    responses = urls(
        {"mypy": pypi(("2.4.0", 60))}, pulls=[item], commits={item["head"]["sha"]: body}
    )
    with pytest.raises(watch.ReadError, match="commit"):
        run(root, responses)


def test_every_page_of_pull_requests_is_read(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    first = f"{API}/repos/{REPO}/pulls?state=all&per_page=100"
    second = f"{API}/repositories/1/pulls?state=all&per_page=100&page=2"
    responses = urls({"mypy": pypi(("2.4.0", 60), ("2.4.1", 18))}, pulls=[pull("x", 1)])
    responses[first] = watch.Response(json.dumps([pull("x", 1)]).encode(), second)
    responses[second] = [pull("Update dependency mypy to v2.4.1", 30)]
    fetch, asked = server(responses)
    assert watch.check(root, fetch, NOW, REPO, API) == []
    assert second in asked


PLANTED = "::stop-commands::x"


@pytest.mark.parametrize(
    "link",
    [f"https://example.com/{PLANTED}", f"http://api.github.com/{PLANTED}", f"//{PLANTED}"],
)
def test_a_next_page_on_another_host_or_away_from_https_is_refused_unnamed(
    tmp_path: Path, link: str
) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    first = f"{API}/repos/{REPO}/pulls?state=all&per_page=100"
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", 1)])
    responses[first] = watch.Response(b"[]", link)
    fetch, asked = server(responses)
    with pytest.raises(watch.ReadError, match="another host or away from HTTPS") as raised:
        watch.check(root, fetch, NOW, REPO, API)
    assert PLANTED not in str(raised.value) and "example.com" not in str(raised.value)
    assert link not in asked


@pytest.mark.parametrize("body", [None, b"<", b"{}"])
def test_a_next_page_that_cannot_be_read_is_named_by_its_number_alone(
    tmp_path: Path, body: bytes | None
) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    first = f"{API}/repos/{REPO}/pulls?state=all&per_page=100"
    second = f"{API}/{PLANTED}"
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", 1)])
    responses[first] = watch.Response(b"[]", second)
    if body is not None:
        responses[second] = watch.Response(body, None)
    with pytest.raises(watch.ReadError) as raised:
        run(root, responses)
    assert str(raised.value) == f"could not read page 2 of {first}"


def test_pages_that_never_end_are_refused(tmp_path: Path) -> None:
    root = tree(tmp_path, "mypy==2.4.0\n")
    first = f"{API}/repos/{REPO}/pulls?state=all&per_page=100"
    responses = urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", 1)])
    responses[first] = watch.Response(b"[]", first)
    with pytest.raises(watch.ReadError) as raised:
        run(root, responses)
    assert str(raised.value) == f"{first} gives more than {watch.PAGES} pages"


# --- The fetch function -------------------------------------------------------------


def test_only_https_is_fetched() -> None:
    with pytest.raises(watch.ReadError, match="HTTPS"):
        watch.fetcher("t0ken", API)("http://pypi.org/pypi/mypy/json")


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ('<https://api.github.com/x?page=2>; rel="next", <https://a/b>; rel="last"', None),
        ('<https://a/b>; rel="last"', None),
        (None, None),
    ],
)
def test_the_next_page_is_read_from_the_link_header(
    header: str | None, expected: str | None
) -> None:
    found = watch.next_page(header)
    if header and 'rel="next"' in header:
        assert found == "https://api.github.com/x?page=2"
    else:
        assert found == expected


class Answer:
    """A response as `urllib` gives it, with a body and a Link header."""

    def __init__(self, body: bytes = b"{}", link: str | None = None) -> None:
        self.body, self.headers = body, {"Link": link} if link else {}

    def __enter__(self) -> Answer:
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def read(self, size: int) -> bytes:
        return self.body[:size]


def test_the_token_is_sent_only_to_github_s_api_and_never_on_a_redirect(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sent: list[tuple[str, str | None, bool]] = []

    def open_url(request: Any, timeout: float) -> Answer:
        auth = request.get_header("Authorization")
        sent.append((request.full_url, auth, "Authorization" in request.headers))
        return Answer(b"[]", f'<{API}/x?page=2>; rel="next"')

    monkeypatch.setattr(watch, "open_url", open_url)
    fetch = watch.fetcher("t0ken", API)
    assert fetch(f"{API}/repos/{REPO}/pulls") == watch.Response(b"[]", f"{API}/x?page=2")
    fetch("https://pypi.org/pypi/mypy/json")
    fetch("https://api.github.com.example.com/x")
    assert sent == [
        (f"{API}/repos/{REPO}/pulls", "Bearer t0ken", False),
        ("https://pypi.org/pypi/mypy/json", None, False),
        ("https://api.github.com.example.com/x", None, False),
    ]


@pytest.mark.parametrize(
    "target",
    ["http://api.github.com/x", "https://example.com/x", "https://pypi.org.example.com/x"],
)
def test_a_redirect_away_from_https_or_to_another_host_is_refused(target: str) -> None:
    request = urllib.request.Request("https://api.github.com/x")
    with pytest.raises(watch.ReadError, match="redirect") as raised:
        watch.Redirects().redirect_request(request, None, 302, "Found", {}, target + PLANTED)
    assert PLANTED not in str(raised.value) and "/x" not in str(raised.value)


def test_a_redirect_on_the_same_host_over_https_is_followed() -> None:
    request = urllib.request.Request("https://api.github.com/x")
    request.add_unredirected_header("Authorization", "Bearer t0ken")
    followed = watch.Redirects().redirect_request(
        request, None, 301, "Moved", {}, "https://api.github.com/y"
    )
    assert followed is not None and followed.full_url == "https://api.github.com/y"
    assert followed.get_header("Authorization") is None


def test_the_opener_uses_the_redirect_rules() -> None:
    assert any(isinstance(h, watch.Redirects) for h in getattr(watch.OPENER, "handlers", []))


def test_a_response_larger_than_the_limit_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(watch, "LIMIT", 4)
    monkeypatch.setattr(watch, "open_url", lambda request, timeout: Answer(b"12345"))
    with pytest.raises(watch.ReadError, match="larger"):
        watch.fetcher("t0ken", API)("https://pypi.org/pypi/mypy/json")
    monkeypatch.setattr(watch, "open_url", lambda request, timeout: Answer(b"1234"))
    assert watch.fetcher("t0ken", API)("https://pypi.org/pypi/mypy/json").body == b"1234"


def test_a_failed_request_is_tried_once_more_then_named_without_its_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tries: list[float] = []

    def open_url(request: Any, timeout: float) -> Any:
        tries.append(timeout)
        raise urllib.error.URLError("<script>")

    monkeypatch.setattr(watch, "open_url", open_url)
    monkeypatch.setattr(time, "sleep", lambda seconds: tries.append(-seconds))
    with pytest.raises(watch.ReadError) as raised:
        watch.fetcher("t0ken", API)("https://pypi.org/pypi/mypy/json")
    assert str(raised.value) == "could not read https://pypi.org/pypi/mypy/json: URLError"
    assert tries == [watch.TIMEOUT, -watch.PAUSE, watch.TIMEOUT]


@pytest.mark.parametrize(
    "error",
    [
        http.client.IncompleteRead(b"::x"),
        http.client.RemoteDisconnected("::x"),
        http.client.BadStatusLine("::x"),
    ],
)
def test_a_failure_of_http_itself_is_tried_once_more_then_named_by_its_kind(
    monkeypatch: pytest.MonkeyPatch, error: Exception
) -> None:
    tries: list[str] = []

    def open_url(request: Any, timeout: float) -> Any:
        tries.append(request.full_url)
        raise error

    monkeypatch.setattr(watch, "open_url", open_url)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    with pytest.raises(watch.ReadError) as raised:
        watch.fetcher("t0ken", API)("https://pypi.org/pypi/mypy/json")
    assert len(tries) == 2
    assert str(raised.value) == (
        f"could not read https://pypi.org/pypi/mypy/json: {type(error).__name__}"
    )


def test_a_request_that_succeeds_the_second_time_is_read(monkeypatch: pytest.MonkeyPatch) -> None:
    answers: list[Any] = [OSError("reset"), Answer(b"[1]")]

    def open_url(request: Any, timeout: float) -> Any:
        answer = answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer

    monkeypatch.setattr(watch, "open_url", open_url)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    assert watch.fetcher("t0ken", API)("https://pypi.org/pypi/x/json").body == b"[1]"


# --- The command line ---------------------------------------------------------------


def environment(tmp_path: Path) -> dict[str, str]:
    return {
        "GITHUB_REPOSITORY": REPO,
        "GITHUB_API_URL": API,
        "GITHUB_TOKEN": "t0ken",
        "GITHUB_STEP_SUMMARY": str(tmp_path / "summary.md"),
    }


def test_a_run_with_no_finding_succeeds_and_says_so(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "t").mkdir()
    root = tree(tmp_path / "t", "mypy==2.4.0\n")
    fetch, _ = server(urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", 1)]))
    env = environment(tmp_path)
    assert watch.main(["--root", str(root)], env, fetch, lambda: NOW) == 0
    assert "no finding" in capsys.readouterr().out
    assert "no finding" in (tmp_path / "summary.md").read_text(encoding="utf-8")


def test_a_run_with_a_finding_fails_and_writes_it_to_the_summary(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "t").mkdir()
    root = tree(tmp_path / "t", "mypy==2.4.0\n")
    fetch, _ = server(urls({"mypy": pypi(("2.4.0", 60), ("2.4.1", 30))}, pulls=[pull("x", 1)]))
    env = environment(tmp_path)
    when = NOW.date().isoformat()
    assert watch.main(["--root", str(root), "--now", when], env, fetch, lambda: NOW) == 1
    out = capsys.readouterr().out
    summary = (tmp_path / "summary.md").read_text(encoding="utf-8")
    for text in (out, summary):
        assert "overdue update: mypy 2.4.0 to 2.4.1" in text


def test_a_run_that_cannot_read_fails_and_says_why(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "t").mkdir()
    root = tree(tmp_path / "t", "mypy==2.4.0\n")
    fetch, _ = server({})
    assert watch.main(["--root", str(root)], environment(tmp_path), fetch, lambda: NOW) == 1
    assert "could not read" in capsys.readouterr().out


def test_an_unexpected_failure_fails_the_run_named_by_its_kind_alone(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "t").mkdir()
    root = tree(tmp_path / "t", "mypy==2.4.0\n")

    def fetch(url: str) -> watch.Response:
        raise RuntimeError(PLANTED)

    assert watch.main(["--root", str(root)], environment(tmp_path), fetch, lambda: NOW) == 1
    out = capsys.readouterr().out
    summary = (tmp_path / "summary.md").read_text(encoding="utf-8")
    for text in (out, summary):
        assert "the check failed: RuntimeError" in text and PLANTED not in text


@pytest.mark.parametrize(
    "repo",
    ["owner", "a/b/c", "../x", "a/..", "a/.", "a b/c", "a/b?x=1", "a/b\n## x", "a/b#x", "/b", "a/"],
)
def test_a_repository_that_is_not_an_owner_and_a_name_fails(tmp_path: Path, repo: str) -> None:
    env = environment(tmp_path) | {"GITHUB_REPOSITORY": repo}
    fetch, asked = server({})
    assert watch.main(["--root", str(ROOT)], env, fetch, lambda: NOW) == 1
    assert asked == []
    assert "GITHUB_REPOSITORY" in (tmp_path / "summary.md").read_text(encoding="utf-8")


def test_a_summary_that_cannot_be_written_fails_the_run_and_says_so(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "t").mkdir()
    root = tree(tmp_path / "t", "mypy==2.4.0\n")
    fetch, _ = server(urls({"mypy": pypi(("2.4.0", 60))}, pulls=[pull("x", 1)]))
    env = environment(tmp_path) | {"GITHUB_STEP_SUMMARY": str(tmp_path / "missing" / "s.md")}
    assert watch.main(["--root", str(root)], env, fetch, lambda: NOW) == 1
    out = capsys.readouterr().out
    assert "no finding" in out
    assert "could not write the summary: FileNotFoundError" in out


@pytest.mark.parametrize("missing", ["GITHUB_REPOSITORY", "GITHUB_API_URL", "GITHUB_TOKEN"])
def test_a_run_without_its_environment_fails(tmp_path: Path, missing: str) -> None:
    env = environment(tmp_path)
    del env[missing]
    fetch, asked = server({})
    assert watch.main(["--root", str(ROOT)], env, fetch, lambda: NOW) == 1
    assert asked == []


@pytest.mark.parametrize("when", ["yesterday", "2026-13-01", "2026-11-20T06:00", "$(id)"])
def test_a_day_that_cannot_be_read_fails(tmp_path: Path, when: str) -> None:
    fetch, asked = server({})
    assert watch.main(["--now", when], environment(tmp_path), fetch, lambda: NOW) == 1
    assert asked == []


def test_an_empty_day_means_the_clock_s_time_and_a_given_day_its_start(tmp_path: Path) -> None:
    (tmp_path / "t").mkdir()
    root = tree(tmp_path / "t", "mypy==2.4.0\n")
    # 2.4.1 is 17.5 days old at NOW and so overdue; on the day before NOW it is not.
    responses = urls({"mypy": pypi(("2.4.0", 60), ("2.4.1", 17.5))}, pulls=[pull("x", 2)])
    env = environment(tmp_path)
    fetch, _ = server(responses)
    assert watch.main(["--root", str(root), "--now", ""], env, fetch, lambda: NOW) == 1
    day_before = (NOW - timedelta(days=1)).date().isoformat()
    assert watch.main(["--root", str(root), "--now", day_before], env, fetch, lambda: NOW) == 0


# --- Scenario: The check's wait and its workflow agree with what is designed --------


def configured_wait(config: Any) -> timedelta | None:
    """The wait that Renovate's configuration sets for minor and patch updates, or None
    unless every setting of a wait that can apply to one of them, at the top level or in
    a package rule, gives the same number of days, and package rules set it for both."""
    waits = []
    covered: set[str] = set()
    if "minimumReleaseAge" in config:
        waits.append(config["minimumReleaseAge"])
    for rule in config.get("packageRules", []):
        if "minimumReleaseAge" not in rule:
            continue
        kinds = rule.get("matchUpdateTypes")
        if kinds is not None and not isinstance(kinds, list):
            return None
        if kinds is None or {"minor", "patch"} & set(kinds):
            waits.append(rule["minimumReleaseAge"])
            covered |= {"minor", "patch"} & set(kinds or ["minor", "patch"])
    if covered != {"minor", "patch"} or len(set(map(str, waits))) != 1:
        return None
    days = re.fullmatch(r"([0-9]+) days", str(waits[0]))
    return timedelta(days=int(days[1])) if days else None


WORKFLOW_GRANTS = {"contents": "read"}
JOB_GRANTS = {"contents": "read", "pull-requests": "read", "issues": "read"}
# The longest that the job may run before GitHub stops it, in minutes.
TIME_LIMIT = 15


def workflow_problems(doc: dict[Any, Any]) -> list[str]:
    """What keeps the workflow from what R263 designs: run every day and by hand, on those
    events alone, with one job, the grants above and nothing else, a time limit, and a
    checkout that keeps no credentials."""
    on = doc.get("on", doc.get(True))
    events = on if isinstance(on, dict) else {}
    problems = []
    crons = [entry.get("cron", "") for entry in events.get("schedule") or []]
    if not any(re.fullmatch(r"[0-9]+ [0-9]+ \* \* \*", cron) for cron in crons):
        problems.append("the workflow runs on no daily schedule")
    if "workflow_dispatch" not in events:
        problems.append("the workflow cannot be started by hand")
    if set(events) - {"schedule", "workflow_dispatch"}:
        problems.append(f"the workflow runs on another event: {sorted(set(events))}")
    if doc.get("permissions") != WORKFLOW_GRANTS:
        problems.append(f"the workflow grants the workflow {doc.get('permissions')}")
    jobs = doc.get("jobs") or {}
    if len(jobs) != 1:
        problems.append("the workflow has not one job")
    for job in jobs.values():
        if job.get("permissions") != JOB_GRANTS:
            problems.append(f"the workflow grants the job {job.get('permissions')}")
        limit = job.get("timeout-minutes")
        if not isinstance(limit, int) or isinstance(limit, bool) or not 0 < limit <= TIME_LIMIT:
            problems.append(f"the workflow gives the job no time limit of {TIME_LIMIT} or less")
        checkouts = [
            step
            for step in job.get("steps") or []
            if str(step.get("uses", "")).startswith("actions/checkout@")
        ]
        if not checkouts or any(
            (step.get("with") or {}).get("persist-credentials") is not False for step in checkouts
        ):
            problems.append("the workflow checks out the code and keeps its credentials")
    return problems


def test_the_check_s_wait_is_the_one_that_renovate_s_configuration_sets() -> None:
    config = json.loads((ROOT / "renovate.json").read_text(encoding="utf-8"))
    assert configured_wait(config) == watch.WAIT


DESIGNED = {
    "matchUpdateTypes": ["major", "minor", "patch", "digest"],
    "minimumReleaseAge": "14 days",
}


def test_a_rule_that_sets_no_wait_or_none_for_minor_and_patch_leaves_it() -> None:
    pins = {"matchUpdateTypes": ["pin", "pinDigest"], "minimumReleaseAge": None}
    other = {"matchUpdateTypes": ["major"], "dependencyDashboardApproval": True}
    assert configured_wait({"packageRules": [DESIGNED, pins, other]}) == watch.WAIT


@pytest.mark.parametrize(
    "rules",
    [
        [{"matchUpdateTypes": ["minor", "patch"], "minimumReleaseAge": "21 days"}],
        [{"matchUpdateTypes": ["major"], "minimumReleaseAge": "14 days"}],
        [{"matchUpdateTypes": ["minor"], "minimumReleaseAge": "14 days"}],
        [{"matchUpdateTypes": ["minor", "patch"], "minimumReleaseAge": "2 weeks"}],
        [],
        [DESIGNED, {"matchUpdateTypes": ["patch"], "minimumReleaseAge": "30 days"}],
        [DESIGNED, {"matchPackageNames": ["mypy"], "minimumReleaseAge": "30 days"}],
        [DESIGNED, {"matchPackageNames": ["mypy"], "minimumReleaseAge": None}],
        [DESIGNED, {"matchUpdateTypes": "minor", "minimumReleaseAge": "30 days"}],
    ],
)
def test_a_wait_that_differs_or_cannot_be_read_is_named(rules: list[dict[str, Any]]) -> None:
    assert configured_wait({"packageRules": rules}) != watch.WAIT


def test_a_wait_at_the_top_level_that_differs_is_named() -> None:
    config = {"minimumReleaseAge": "3 days", "packageRules": [DESIGNED]}
    assert configured_wait(config) is None


def workflow() -> dict[Any, Any]:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(doc, dict)
    return doc


def job(doc: dict[Any, Any]) -> dict[str, Any]:
    return next(iter(doc["jobs"].values()))


def checkout(doc: dict[Any, Any]) -> dict[str, Any]:
    return next(
        step
        for step in job(doc)["steps"]
        if str(step.get("uses", "")).startswith("actions/checkout@")
    )


def test_the_workflow_runs_daily_and_by_hand_and_reads_only() -> None:
    assert workflow_problems(workflow()) == []


@pytest.mark.parametrize(
    ("change", "problem"),
    [
        (lambda d: d[True].pop("schedule"), "runs on no daily schedule"),
        (lambda d: d[True].update(schedule=[{"cron": "0 6 * * 1"}]), "runs on no daily schedule"),
        (lambda d: d[True].pop("workflow_dispatch"), "cannot be started by hand"),
        (lambda d: d[True].update(pull_request=None), "runs on another event"),
        (lambda d: d[True].update(push=None), "runs on another event"),
        (lambda d: d.update(permissions={"contents": "write"}), "grants the workflow"),
        (lambda d: d.pop("permissions"), "grants the workflow"),
        (lambda d: d.update(permissions="write-all"), "grants the workflow"),
        (
            lambda d: d.update(permissions={"contents": "read", "issues": "read"}),
            "grants the workflow",
        ),
        (lambda d: job(d).update(permissions={"issues": "write"}), "grants the job"),
        (lambda d: job(d).pop("permissions"), "grants the job"),
        (lambda d: job(d)["permissions"].update(actions="read"), "grants the job"),
        (lambda d: job(d)["permissions"].pop("issues"), "grants the job"),
        (lambda d: d["jobs"].update(other={"steps": []}), "one job"),
        (lambda d: job(d).pop("timeout-minutes"), "no time limit"),
        (lambda d: job(d).update({"timeout-minutes": 360}), "no time limit"),
        (lambda d: job(d).update({"timeout-minutes": 0}), "no time limit"),
        (lambda d: job(d).update({"timeout-minutes": "10"}), "no time limit"),
        (lambda d: job(d).update({"timeout-minutes": True}), "no time limit"),
        (lambda d: checkout(d).pop("with"), "keeps its credentials"),
        (
            lambda d: checkout(d)["with"].update({"persist-credentials": True}),
            "keeps its credentials",
        ),
        (lambda d: job(d).update(steps=[{"run": "x"}]), "keeps its credentials"),
    ],
)
def test_a_workflow_that_differs_from_its_design_is_named(change: Any, problem: str) -> None:
    doc = workflow()
    change(doc)
    found = workflow_problems(doc)
    assert any(problem in item for item in found), found


def test_the_workflow_passes_no_expression_into_a_command() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    runs = [step.get("run", "") for step in job(workflow())["steps"]]
    assert any("renovate_watch.py" in run for run in runs), runs
    assert all("${{" not in run for run in runs), runs
    assert "secrets" not in text
