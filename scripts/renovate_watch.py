"""The daily check that warns the owner when Renovate stops proposing updates.

R263 in `releases-and-compatibility`, design decision 22 of `add-pr-cost-calculator`
and DR-267 give what it does. It reads the tools that `requirements-dev.txt` and
`package.json` pin, asks the Python Package Index and the npm registry when each of
their releases was published, and asks GitHub which pull requests Renovate opened and
when its dependency dashboard last changed. It names a finding for each minor or patch
release that Renovate should already have proposed and has not, and for five days in
which Renovate did nothing, and exits with 1 when it names one or cannot read what it
needs, so that the scheduled run fails and GitHub tells the owner. A tool whose registry
cannot be read is named as not read, and the rest are still checked.

Run it with `python3 -I scripts/renovate_watch.py`. It needs `GITHUB_REPOSITORY`,
`GITHUB_API_URL` and `GITHUB_TOKEN`, and writes its findings to `GITHUB_STEP_SUMMARY`
when that is set. It uses the standard library only, writes nothing else and sends the
token only to GitHub's API.
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

# Renovate's wait for a minor or patch update, as `renovate.json` sets it; a test holds
# the two equal.
WAIT = timedelta(days=14)
# Time for Renovate's own schedule to reach an update once its wait has passed.
GRACE = timedelta(days=3)
# How long Renovate may do nothing before the check names it.
QUIET = timedelta(days=5)

RENOVATE = "renovate[bot]"
DASHBOARD = "Dependency Dashboard"
# Renovate's title for an update of one dependency, after a prefix that ends in ": " and
# before a suffix that it adds for a vulnerability fix or a pull request that it closed.
# A title in any other form proposes nothing, so a change to Renovate's titles shows as a
# finding rather than hiding one.
TITLE = re.compile(
    r"(?:[^:]*: )?update dependency (?P<name>\S+) to v(?P<version>\S+)"
    r"(?: \[SECURITY\]| - autoclosed| - abandoned)?",
    re.IGNORECASE,
)
# A version of numbers and dots, in ASCII digits, each part short enough to read as a
# number at once.
VERSION = r"[0-9]{1,20}(?:\.[0-9]{1,20})*"
PIN = re.compile(rf"(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)==(?P<version>{VERSION})")
DAY = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
# An owner and a repository's name as GitHub allows them, and never `.` or `..`.
REPOSITORY = re.compile(r"[A-Za-z0-9-]+/(?!\.\.?$)[A-Za-z0-9_.-]+")

# The largest response that the check reads, so that a hostile one cannot exhaust the
# runner. The Python Package Index's documents for ruff are the largest it reads.
LIMIT = 64 * 1024 * 1024
TIMEOUT = 60
# How long to wait before trying a failed request once more.
PAUSE = 30
# The most pages of pull requests that it reads, so that a loop of links ends.
PAGES = 50


class ReadError(Exception):
    """What the check could not read. It fails the run, which never passes on it."""


@dataclass(frozen=True)
class Pin:
    name: str
    version: str
    registry: str


@dataclass(frozen=True)
class Response:
    body: bytes
    next: str | None


Fetch = Callable[[str], Response]


def numbers(version: str) -> tuple[int, ...] | None:
    """A version's numbers without its trailing zeros, so that 1.0 and 1.0.0 are one
    version, or None for one with anything but numbers and dots, such as a pre-release, a
    post-release or an epoch, which the check does not compare."""
    if not re.fullmatch(VERSION, version):
        return None
    parts = [int(part) for part in version.split(".")]
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


def normal(name: str, registry: str) -> str:
    """A tool's name as its registry compares it: a Python one in lower case with each run
    of -, _ and . read as one -, and an npm one as it is."""
    return re.sub(r"[-_.]+", "-", name).lower() if registry == "pypi" else name


def pins(root: Path) -> list[Pin]:
    """The tools that `requirements-dev.txt` and `package.json`'s development and runtime
    dependencies pin, in that order.

    Raises ReadError for a file that is missing or cannot be read, a line or a version
    that is not an exact pin, and a tree that pins nothing."""
    found: list[Pin] = []
    requirements = root / "requirements-dev.txt"
    try:
        lines = requirements.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        raise ReadError(f"could not read requirements-dev.txt: {type(error).__name__}") from None
    for number, line in enumerate(lines, 1):
        text = line.split("#", 1)[0].strip()
        if not text:
            continue
        pinned = PIN.fullmatch(text)
        if not pinned:
            raise ReadError(f"requirements-dev.txt:{number} is not an exact pin")
        found.append(Pin(pinned["name"], pinned["version"], "pypi"))
    try:
        package = json.loads((root / "package.json").read_text(encoding="utf-8"))
        sections = [package.get(key, {}) for key in ("devDependencies", "dependencies")]
    except (OSError, ValueError, AttributeError) as error:
        raise ReadError(f"could not read package.json: {type(error).__name__}") from None
    for section in sections:
        if not isinstance(section, dict):
            raise ReadError("could not read package.json: a section of dependencies")
        for name, version in section.items():
            if not isinstance(version, str) or not numbers(version):
                raise ReadError(f"package.json pins {name} to no exact version")
            found.append(Pin(name, version, "npm"))
    if not found:
        raise ReadError("found no pinned tool in requirements-dev.txt or package.json")
    return found


def moment(text: Any) -> datetime:
    """A time that GitHub or a registry gives, which must name its offset."""
    if not isinstance(text, str):
        raise ValueError("not a time")
    when = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if when.tzinfo is None:
        raise ValueError("a time with no offset")
    return when.astimezone(UTC)


def pypi_releases(doc: Any) -> dict[str, datetime]:
    """Each release that the Python Package Index's document gives, by the time of its
    earliest file, leaving out a release with no file and one whose files are yanked."""
    try:
        found = {}
        for version, files in doc["releases"].items():
            kept = [moment(f["upload_time_iso_8601"]) for f in files if not f["yanked"]]
            if kept:
                found[version] = min(kept)
        return found
    except (KeyError, TypeError, AttributeError, ValueError) as error:
        raise ReadError(f"a Python Package Index document: {type(error).__name__}") from None


def npm_releases(doc: Any) -> dict[str, datetime]:
    """Each version that the npm registry's document gives, by its time, leaving out a
    deprecated one."""
    try:
        times = doc["time"]
        return {
            version: moment(times[version])
            for version, about in doc["versions"].items()
            if "deprecated" not in about
        }
    except (KeyError, TypeError, AttributeError, ValueError) as error:
        raise ReadError(f"an npm registry document: {type(error).__name__}") from None


@dataclass(frozen=True)
class Renovate:
    # The versions that Renovate's pull requests propose, by the name of their tool as
    # normal() gives it for each registry.
    proposed: dict[str, list[tuple[int, ...]]]
    # When Renovate last opened a pull request or authored the head commit of an open one,
    # by the commit's author time, which a rebase by anyone else leaves as it was.
    last: datetime


def renovate(pulls: Any, issues: Any, fetch: Fetch, base: str, now: datetime) -> Renovate:
    """What Renovate's pull requests that existed at `now` propose, and when Renovate itself
    was last active before it, from GitHub's list of the repository's pull requests, the
    head commit of each open one of Renovate's, and the open issues that it opened, of
    which one must be its dashboard."""
    proposed: dict[str, list[tuple[int, ...]]] = {}
    times: list[datetime] = []
    heads: list[str] = []
    try:
        for item in pulls:
            if item["user"]["login"] != RENOVATE:
                continue
            opened = moment(item["created_at"])
            if opened > now:
                continue
            times.append(opened)
            if item["state"] == "open":
                sha = item["head"]["sha"]
                if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
                    raise ValueError("a head commit")
                heads.append(sha)
            title = TITLE.fullmatch(item["title"])
            if title and (version := numbers(title["version"])):
                for registry in ("pypi", "npm"):
                    proposed.setdefault(normal(title["name"], registry), []).append(version)
    except (KeyError, TypeError, ValueError) as error:
        raise ReadError(f"could not read the pull requests: {type(error).__name__}") from None
    if not times:
        raise ReadError("found no pull request of Renovate's")
    for sha in heads:
        commit = parsed(fetch(f"{base}/commits/{sha}").body, f"the commit {sha}")
        try:
            author = commit["author"]
            authored = moment(commit["commit"]["author"]["date"])
        except (KeyError, TypeError, ValueError) as error:
            raise ReadError(f"could not read the commit {sha}: {type(error).__name__}") from None
        if isinstance(author, dict) and author.get("login") == RENOVATE and authored <= now:
            times.append(authored)
    try:
        dashboards = [
            item
            for item in issues
            if item["user"]["login"] == RENOVATE
            and item["title"] == DASHBOARD
            and "pull_request" not in item
        ]
    except (KeyError, TypeError) as error:
        raise ReadError(f"could not read the issues: {type(error).__name__}") from None
    if not dashboards:
        raise ReadError("found no open dependency dashboard that Renovate opened")
    return Renovate(proposed, max(times))


def overdue(
    pin: Pin, releases: Mapping[str, datetime], proposed: Sequence[tuple[int, ...]], now: datetime
) -> str | None:
    """The finding for a pinned tool whose newest minor or patch release that passed the
    wait and the grace is newer than its pin and proposed by none of Renovate's pull
    requests, for it or a later version, or None."""
    current = numbers(pin.version)
    if current is None:
        raise ReadError(f"{pin.name} is pinned to no version of numbers")
    if not any(numbers(name) == current for name in releases):
        raise ReadError(f"the registry lists no release {pin.version} that the check can compare")
    due = [
        (version, name, published)
        for name, published in releases.items()
        if (version := numbers(name))
        and version > current
        and version[0] == current[0]
        and now - published > WAIT + GRACE
    ]
    if not due:
        return None
    newest, name, published = max(due)
    if any(version >= newest and version[0] == newest[0] for version in proposed):
        return None
    return (
        f"overdue update: {pin.name} {pin.version} to {name}, published"
        f" {published.date().isoformat()}, has no pull request from Renovate"
    )


def quiet(last: datetime, now: datetime) -> str | None:
    if now - last <= QUIET:
        return None
    return (
        "quiet: Renovate has opened no pull request, and authored no commit on its open ones,"
        f" since {last.strftime('%Y-%m-%d %H:%M')} UTC"
    )


def parsed(body: bytes, what: str) -> Any:
    """A response's JSON. An error names `what`, which the check built, and the kind of
    error, never the response's own text."""
    try:
        return json.loads(body)
    except ValueError as error:
        raise ReadError(f"could not read {what}: {type(error).__name__}") from None


def pages(fetch: Fetch, first: str) -> list[Any]:
    """Every item of a list that GitHub gives in pages, following each next link only over
    HTTPS on the host of the first page. An error names the first page's address, which
    the check built, and the page's number, never an address that a response gave."""
    host = urllib.parse.urlsplit(first).netloc
    items: list[Any] = []
    url = first
    for number in range(1, PAGES + 1):
        failed = ReadError(f"could not read page {number} of {first}")
        try:
            response = fetch(url)
        except ReadError:
            if number == 1:
                raise
            raise failed from None
        try:
            page = parsed(response.body, url)
        except ReadError:
            raise failed from None
        if not isinstance(page, list):
            raise failed
        items += page
        if response.next is None:
            return items
        link = urllib.parse.urlsplit(response.next)
        if link.scheme != "https" or link.netloc != host:
            raise ReadError(f"{first} gives its next page on another host or away from HTTPS")
        url = response.next
    raise ReadError(f"{first} gives more than {PAGES} pages")


def check(root: Path, fetch: Fetch, now: datetime, repo: str, api: str) -> list[str]:
    """Each finding, an overdue update or a registry not read for each tool in turn, and
    then the quiet days.

    Raises ReadError for anything else that it could not read."""
    tools = pins(root)
    base = f"{api.rstrip('/')}/repos/{repo}"
    pulls = pages(fetch, f"{base}/pulls?state=all&per_page=100")
    issues = pages(fetch, f"{base}/issues?state=open&creator=renovate%5Bbot%5D&per_page=100")
    activity = renovate(pulls, issues, fetch, base, now)
    findings = []
    for pin in tools:
        try:
            if pin.registry == "pypi":
                url = f"https://pypi.org/pypi/{urllib.parse.quote(pin.name)}/json"
                releases = pypi_releases(parsed(fetch(url).body, url))
            else:
                url = f"https://registry.npmjs.org/{urllib.parse.quote(pin.name, safe='@')}"
                releases = npm_releases(parsed(fetch(url).body, url))
            proposed = activity.proposed.get(normal(pin.name, pin.registry), [])
            finding = overdue(pin, releases, proposed, now)
        except ReadError as error:
            finding = f"not read: {pin.name} {pin.version}: {error}"
        if finding:
            findings.append(finding)
    if finding := quiet(activity.last, now):
        findings.append(finding)
    return findings


def next_page(link: str | None) -> str | None:
    """The address that GitHub's Link header gives as the next page, or None."""
    for part in (link or "").split(","):
        found = re.fullmatch(r'\s*<([^>]+)>\s*;\s*rel="next"\s*', part)
        if found:
            return found[1]
    return None


class Redirects(urllib.request.HTTPRedirectHandler):
    """Follows a redirect only over HTTPS to the same host, which carries no header that
    was added as unredirected, as the token is."""

    def redirect_request(
        self, req: urllib.request.Request, fp: Any, code: int, msg: str, headers: Any, newurl: str
    ) -> urllib.request.Request | None:
        old, new = urllib.parse.urlsplit(req.full_url), urllib.parse.urlsplit(newurl)
        if new.scheme != "https" or new.netloc != old.netloc:
            raise ReadError("refused a redirect to another host or away from HTTPS")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(Redirects)


def open_url(request: urllib.request.Request, timeout: float) -> Any:
    return OPENER.open(request, timeout=timeout)


def fetcher(token: str, api: str) -> Fetch:
    """A fetch function that reads over HTTPS only, sends the token only to the host of
    GitHub's API and never on a redirect, tries a failed request once more after a pause,
    and refuses a response larger than LIMIT."""
    api_host = urllib.parse.urlsplit(api).netloc

    def fetch(url: str) -> Response:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme != "https":
            raise ReadError(f"refused {url}: the check reads over HTTPS only")
        request = urllib.request.Request(
            url, headers={"Accept": "application/json", "User-Agent": "renovate-watch"}
        )
        if parts.netloc == api_host:
            request.add_unredirected_header("Authorization", f"Bearer {token}")
        for attempt in (1, 2):
            try:
                with open_url(request, TIMEOUT) as answer:
                    body = answer.read(LIMIT + 1)
                    link = answer.headers.get("Link")
                break
            except (urllib.error.URLError, OSError, ValueError, http.client.HTTPException) as error:
                if attempt == 2:
                    raise ReadError(f"could not read {url}: {type(error).__name__}") from None
                time.sleep(PAUSE)
        if len(body) > LIMIT:
            raise ReadError(f"{url} gave a response larger than {LIMIT} bytes")
        return Response(body, next_page(link))

    return fetch


def main(
    argv: Sequence[str],
    environ: Mapping[str, str],
    fetch: Fetch | None = None,
    clock: Callable[[], datetime] = lambda: datetime.now(UTC),
) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".", help="the checkout to read the pins from")
    parser.add_argument(
        "--now",
        default="",
        help="a day, YYYY-MM-DD in UTC, to check as at its start; empty for the clock's time",
    )
    args = parser.parse_args(argv)
    try:
        if args.now:
            if not DAY.fullmatch(args.now):
                raise ReadError("--now gives no day in the form YYYY-MM-DD")
            try:
                now = datetime.fromisoformat(args.now).replace(tzinfo=UTC)
            except ValueError:
                raise ReadError("--now gives no day that exists") from None
        else:
            now = clock()
        missing = [
            name
            for name in ("GITHUB_REPOSITORY", "GITHUB_API_URL", "GITHUB_TOKEN")
            if not environ.get(name)
        ]
        if missing:
            raise ReadError(f"the environment gives no {', '.join(missing)}")
        if not REPOSITORY.fullmatch(environ["GITHUB_REPOSITORY"]):
            raise ReadError("GITHUB_REPOSITORY gives no owner and name")
        api = environ["GITHUB_API_URL"]
        fetch = fetch or fetcher(environ["GITHUB_TOKEN"], api)
        findings = check(Path(args.root), fetch, now, environ["GITHUB_REPOSITORY"], api)
        lines = findings or ["no finding: Renovate is proposing updates"]
        status = 1 if findings else 0
    except ReadError as error:
        lines = [f"the check failed: {error}"]
        status = 1
    except Exception as error:  # noqa: BLE001 - its text may come from a response
        lines = [f"the check failed: {type(error).__name__}"]
        status = 1
    for line in lines:
        print(line)
    summary = environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        try:
            with open(summary, "a", encoding="utf-8") as out:
                out.write("## Renovate's proposals\n\n" + "".join(f"- {x}\n" for x in lines))
        except OSError as error:
            print(f"could not write the summary: {type(error).__name__}")
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], os.environ))
