#!/usr/bin/env python3
# The walking skeleton of the agentic PR cost calculator: not the tool or a release.
# Its figure is at a test price and is not a real cost (DR-246). Run by `workflow.yml` on the
# push that a merge makes to `main`, with the push's `before` and `after` commits checked out
# into two folders, it reads the ledger files that the push added and writes one figure to the
# job summary and as one comment (R241). Python's standard library only.
"""The walking skeleton's report: `report.py <before folder> <after folder>`."""

from __future__ import annotations

import json
import os
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

# The test price, in a currency of no one's, per million tokens of each kind. It is not a real
# price, so the figure it gives is not a real cost (DR-246).
TEST_PRICE_PER_MILLION_TOKENS = {
    "input_tokens": 1.0,
    "output_tokens": 2.0,
    "cache_creation_input_tokens": 3.0,
    "cache_read_input_tokens": 4.0,
}
COUNTS = tuple(TEST_PRICE_PER_MILLION_TOKENS)
HEADINGS = ("Input", "Output", "Cache write", "Cache read")
MODEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:@-]{0,99}")
LEDGER = Path(".pr-cost") / "ledger"
ZEROS = "0" * 40
MAX_COUNT = 10**15
NOT_A_COST = (
    "This is the walking skeleton's figure, at a test price: it is not a real cost, "
    "and the walking skeleton is not the tool."
)

Api = Callable[[str, str, Any], Any]


def github_api(env: dict[str, str]) -> Api:
    """GitHub's REST API, with the job's token, from inside a workflow."""
    base = env.get("GITHUB_API_URL", "https://api.github.com")

    def call(method: str, path: str, body: Any = None) -> Any:
        request = Request(
            base + path,
            method=method,
            data=None if body is None else json.dumps(body).encode(),
            headers={
                "Authorization": f"Bearer {env['GITHUB_TOKEN']}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
            },
        )
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read())

    return call


def is_count(value: Any) -> bool:
    """A token count: a whole number, not a boolean, from zero to below a bound."""
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value < MAX_COUNT


def ledger_files(folder: Path) -> set[Path]:
    """The ledger files in a checked-out tree, through no linked folder."""
    root = folder / LEDGER
    if root.parent.is_symlink() or root.is_symlink() or not root.is_dir():
        return set()
    return {path.relative_to(folder) for path in root.rglob("*.jsonl")}


def calls_added(before: Path, after: Path) -> tuple[dict[str, dict[str, Any]], int, int]:
    """Each call of the ledger files that `after` holds and `before` did not, by key, once;
    with the number of files read and of lines that could not be read."""
    calls: dict[str, dict[str, Any]] = {}
    added = sorted(ledger_files(after) - ledger_files(before))
    unread = 0
    for relative in added:
        path = after / relative
        try:
            if path.is_symlink():
                raise ValueError("a ledger file that is a link is not followed")
            text = path.read_text(encoding="utf-8")
        except (OSError, ValueError):
            unread += 1
            continue
        for raw in text.splitlines():
            try:
                line = json.loads(raw)
            except ValueError:
                unread += 1
                continue
            usable = (
                isinstance(line, dict)
                and isinstance(line.get("key"), str)
                and isinstance(line.get("model"), str)
                and MODEL.fullmatch(line["model"]) is not None
                and all(is_count(line.get(name)) for name in COUNTS)
            )
            if not usable:
                unread += 1
                continue
            calls.setdefault(line["key"], line)
    return calls, len(added), unread


def figure(calls: dict[str, dict[str, Any]], files: int, unread: int) -> str:
    """The figure by model, at the test price, as Markdown."""
    models: dict[str, list[int]] = {}
    for call in calls.values():
        row = models.setdefault(call["model"], [0] * (len(COUNTS) + 1))
        row[0] += 1
        for index, name in enumerate(COUNTS, start=1):
            row[index] += call[name]
    lines = [
        "## Walking skeleton: a figure at a test price",
        "",
        NOT_A_COST,
        "",
    ]
    if not files:
        lines.append("The push added no ledger file.")
    total = 0.0
    if models:
        lines += [
            "| Model | Calls | " + " | ".join(HEADINGS) + " | At the test price |",
            "|---|---:|" + "---:|" * len(HEADINGS) + "---:|",
        ]
        for model, row in sorted(models.items()):
            price = sum(
                row[i] * TEST_PRICE_PER_MILLION_TOKENS[name] / 1_000_000
                for i, name in enumerate(COUNTS, start=1)
            )
            total += price
            counts = " | ".join(f"{value:,}" for value in row[1:])
            # In a code span, which a model name cannot close, so it is never a link or a mention.
            lines.append(f"| `{model}` | {row[0]} | {counts} | {price:.2f} |")
    lines += ["", f"In all, **{total:.2f}** at the test price, which is not a real cost."]
    if unread:
        lines.append(f"{unread} ledger lines could not be read and are not counted.")
    return "\n".join(lines) + "\n"


def write_summary(env: dict[str, str], text: str) -> None:
    with open(env["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
        summary.write(text)


def main(argv: list[str], env: dict[str, str], api: Api) -> int:
    before, after = (Path(argument) for argument in argv)
    event = json.loads(Path(env["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    repository = env["GITHUB_REPOSITORY"]
    why = None
    if event["before"] == ZEROS:
        why = "the push creates the branch, so it has no commit before it to compare with"
    else:
        pulls = api("GET", f"/repos/{repository}/commits/{event['after']}/pulls", None)
        merged = [pull for pull in pulls if pull.get("merged_at")]
        if not merged:
            why = "GitHub gives no merged pull request for the push"
        elif len(merged) > 1:
            why = "GitHub gives more than one merged pull request for the push"
    if why:
        write_summary(env, f"## Walking skeleton\n\nNo comment: {why}.\n\n{NOT_A_COST}\n")
        return 0
    text = figure(*calls_added(before, after))
    write_summary(env, text)
    api("POST", f"/repos/{repository}/issues/{merged[0]['number']}/comments", {"body": text})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], dict(os.environ), github_api(dict(os.environ))))
