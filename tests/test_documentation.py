"""The documentation says what the repository holds, and keeps saying it.

Three documents describe the tool, and each is checked against what it
describes, so that one cannot quietly fall behind:

- `docs/requirements.md` registers every requirement in the specs, once, with
  its kind. A requirement added to a spec and not to the register is reported,
  and so is a row for a requirement that no spec holds.
- `docs/features/` has one page per feature, and each feature is one spec. A
  page is named for its spec, names every requirement that the spec holds and
  no other, and says how the feature is validated; every spec has a page, and
  the index links every page.
- `docs/how-it-works.md` explains the tool as a whole. It names every
  permission that a workflow grants and every action that a workflow runs, and
  draws each flow it lists.

Each change's proposal is checked too: it lists every spec that the change
holds as a capability, and gives each a row of its own, with a statement, in
its section on how the outcome is validated.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]

KINDS = ("functional", "behavioural", "non-functional")
REQUIREMENT = re.compile(r"^### Requirement: (.+?)\s*$", re.M)
REGISTER_ROW = re.compile(r"^\| (R\d+) \| ([a-z-]+) \| `([a-z0-9-]+)` \| (.+?) \|\s*$", re.M)
RETIRED_ROW = re.compile(r"^- (R\d+), removed by `([a-z0-9-]+)`", re.M)
PAGE_REQUIREMENTS = re.compile(r"^\*\*Requirements:\*\* (.+)$", re.M)
PAGE_SPEC = re.compile(r"^\*\*Spec:\*\* `([a-z0-9-]+)`\s*$", re.M)
CAPABILITY_LINE = re.compile(r"^- `([a-z0-9-]+)`: ", re.M)
VALIDATION_ROW = re.compile(r"^\| `([a-z0-9-]+)` \|([^|\n]*)\|", re.M)
CHANGES = ROOT / "openspec" / "changes"
REQUIREMENT_ID = re.compile(r"R\d+")
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
USES = re.compile(r"^\s*-?\s*uses:\s*([^\s@#]+)@", re.M)
PERMISSION_ROW = re.compile(r"^\| `([^`]+\.ya?ml)` \| `([^`]+)` \| (.+?) \|\s*$", re.M)


@dataclass(frozen=True)
class Row:
    ident: str
    kind: str
    capability: str
    name: str


def spec_requirements(root: Path) -> set[tuple[str, str]]:
    found = set()
    for spec in sorted((root / "openspec").rglob("spec.md")):
        for name in REQUIREMENT.findall(spec.read_text(encoding="utf-8")):
            found.add((spec.parent.name, name))
    return found


def register_rows(text: str) -> list[Row]:
    return [Row(*match) for match in REGISTER_ROW.findall(text)]


def register_problems(text: str, root: Path) -> list[str]:
    rows = register_rows(text)
    if not rows:
        return ["the register holds no requirement"]
    problems = []
    idents = [row.ident for row in rows]
    retired = [ident for ident, _change in RETIRED_ROW.findall(text)]
    numbers = sorted(int(ident[1:]) for ident in idents + retired)
    if numbers != list(range(1, len(numbers) + 1)):
        problems.append("the register's and the retired IDs do not run from R1 without a gap")
    if idents != sorted(idents, key=lambda ident: int(ident[1:])):
        problems.append("the register's IDs are not in order")
    problems += [f"{ident} is both registered and retired" for ident in idents if ident in retired]
    problems += [
        f"{row.ident} has a kind outside the list" for row in rows if row.kind not in KINDS
    ]
    listed = [(row.capability, row.name) for row in rows]
    specified = spec_requirements(root)
    for capability, name in sorted(specified - set(listed)):
        problems.append(f'`{capability}`: "{name}" is in a spec and not in the register')
    for row in rows:
        if (row.capability, row.name) not in specified:
            problems.append(f"{row.ident} names a requirement that no spec holds")
        if listed.count((row.capability, row.name)) > 1:
            problems.append(f"{row.ident} registers a requirement twice")
    return problems


def feature_problems(register: str, features: Path) -> list[str]:
    rows = {row.ident: row for row in register_rows(register)}
    index = features / "README.md"
    if not index.is_file():
        return ["the features folder has no index"]
    pages = sorted(p for p in features.glob("*.md") if p.name != "README.md")
    if not pages:
        return ["the features folder has no page"]
    problems = []
    linked = {(features / link).resolve() for link in LINK.findall(index.read_text())}
    capabilities = {row.capability for row in rows.values()}
    paged: set[str] = set()
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if page.resolve() not in linked:
            problems.append(f"{page.name} is not linked from the index")
        specs = PAGE_SPEC.findall(text)
        named = PAGE_REQUIREMENTS.findall(text)
        if len(specs) != 1 or len(named) != 1:
            problems.append(
                f"{page.name} does not have one line naming its spec and one its requirements"
            )
            continue
        spec = specs[0]
        if page.stem != spec:
            problems.append(f"{page.name} is not named for its spec `{spec}`")
        if spec not in capabilities:
            problems.append(
                f"{page.name} names the spec `{spec}`, which the register does not hold"
            )
        paged.add(spec)
        idents = REQUIREMENT_ID.findall(named[0])
        for ident in idents:
            if ident not in rows:
                problems.append(f"{page.name} names {ident}, which the register does not hold")
            elif rows[ident].capability != spec:
                problems.append(
                    f"{page.name} names {ident}, which `{rows[ident].capability}` holds"
                )
        problems += [
            f"{ident} is not on the page for `{spec}`"
            for ident, row in rows.items()
            if row.capability == spec and ident not in idents
        ]
        if not section(text, "How it is validated").strip():
            problems.append(f"{page.name} does not say how it is validated")
    for link in sorted(linked):
        if not link.is_file():
            problems.append(f"the index links {link.name}, which does not exist")
    for capability in sorted(capabilities - paged):
        held = ", ".join(ident for ident, row in rows.items() if row.capability == capability)
        problems.append(f"`{capability}` has no feature page for {held}")
    return problems


def proposal_problems(proposal: str, specs: set[str]) -> list[str]:
    listed = CAPABILITY_LINE.findall(section(proposal, "Capabilities"))
    problems = [
        f"`{name}` is a spec the proposal does not list" for name in sorted(specs - set(listed))
    ]
    problems += [
        f"the proposal lists `{name}`, which has no spec" for name in sorted(set(listed) - specs)
    ]
    validated = {
        name: cell.strip()
        for name, cell in VALIDATION_ROW.findall(section(proposal, "How the outcome is validated"))
    }
    problems += [
        f"the proposal does not say how `{name}` is validated"
        for name in sorted(specs)
        if not validated.get(name)
    ]
    return problems


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, re.M)
    if not match:
        return ""
    body = text[match.end() :]
    following = re.search(r"^## ", body, re.M)
    return body[: following.start()] if following else body


# A job that declares no permissions, in a workflow that declares none, gets
# whatever the repository's settings give the token, so the page must say so.
DEFAULT = "repository default"


def permission_set(block: Any) -> set[str]:
    if isinstance(block, dict):
        return {f"{scope}: {level}" for scope, level in block.items()}
    if isinstance(block, str):
        return {block}
    return {DEFAULT}


def granted(workflow: dict[str, Any]) -> dict[str, set[str]]:
    """Each job's effective permissions: its own block, else the workflow's."""
    top = workflow.get("permissions")
    return {
        name: permission_set(job.get("permissions", top))
        for name, job in (workflow.get("jobs") or {}).items()
    }


def images(workflow: dict[str, Any]) -> set[str]:
    found = set()
    for job in (workflow.get("jobs") or {}).values():
        container = job.get("container")
        if isinstance(container, str):
            found.add(container)
        elif isinstance(container, dict) and container.get("image"):
            found.add(container["image"])
        for service in (job.get("services") or {}).values():
            if isinstance(service, dict) and service.get("image"):
                found.add(service["image"])
    return found


def listed_permissions(section_text: str) -> dict[tuple[str, str], set[str]]:
    table = {}
    for workflow, job, cell in PERMISSION_ROW.findall(section_text):
        table[(workflow, job)] = set(re.findall(r"`([^`]+)`", cell))
    return table


def how_it_works_problems(text: str, workflow_files: list[Path]) -> list[str]:
    problems = []
    permissions = section(text, "Credentials and permissions")
    connections = section(text, "Connections to the outside world")
    flows = section(text, "Flows")
    for heading, body in [
        ("Credentials and permissions", permissions),
        ("Connections to the outside world", connections),
        ("Flows", flows),
    ]:
        if not body.strip():
            problems.append(f"how it works has no section {heading!r}")
    table = listed_permissions(permissions)
    seen = set()
    for path in workflow_files:
        source = path.read_text(encoding="utf-8")
        workflow = yaml.safe_load(source)
        for job, effective in sorted(granted(workflow).items()):
            seen.add((path.name, job))
            listed = table.get((path.name, job))
            if listed is None:
                problems.append(f"{path.name} job `{job}` is not in the permissions table")
                continue
            for permission in sorted(effective - listed):
                problems.append(f"{path.name} job `{job}` gets `{permission}`, which is not listed")
            for permission in sorted(listed - effective):
                problems.append(
                    f"{path.name} job `{job}` is listed with `{permission}`, not granted"
                )
        for action in sorted(set(USES.findall(source))):
            if f"`{action}`" not in connections:
                problems.append(f"{path.name} runs `{action}`, which is not listed")
        for image in sorted(images(workflow)):
            if f"`{image}`" not in connections:
                problems.append(f"{path.name} runs the image `{image}`, which is not listed")
    for workflow_name, job in sorted(set(table) - seen):
        problems.append(
            f"the permissions table lists {workflow_name} job `{job}`, which no workflow has"
        )
    parts = re.split(r"^### (.+?)\s*$", flows, flags=re.M)
    names = parts[1::2]
    if flows.strip() and not names:
        problems.append("how it works lists no flow")
    for name, body in zip(names, parts[2::2], strict=True):
        if "```mermaid" not in body:
            problems.append(f"the flow {name!r} has no diagram")
    return problems


def workflows(root: Path = ROOT) -> list[Path]:
    folder = root / ".github" / "workflows"
    return sorted([*folder.glob("*.yml"), *folder.glob("*.yaml")])


def test_the_register_holds_every_requirement_once() -> None:
    text = (ROOT / "docs" / "requirements.md").read_text(encoding="utf-8")
    assert not register_problems(text, ROOT), "\n".join(register_problems(text, ROOT))
    assert spec_requirements(ROOT), "no requirement was found in the specs"


def test_every_feature_page_resolves_and_every_requirement_has_a_feature() -> None:
    register = (ROOT / "docs" / "requirements.md").read_text(encoding="utf-8")
    problems = feature_problems(register, ROOT / "docs" / "features")
    assert not problems, "\n".join(problems)


def test_how_it_works_names_every_permission_and_action_and_draws_every_flow() -> None:
    text = (ROOT / "docs" / "how-it-works.md").read_text(encoding="utf-8")
    assert workflows(), "no workflow was found, so this test covered nothing"
    problems = how_it_works_problems(text, workflows())
    assert not problems, "\n".join(problems)


def synthetic_specs(root: Path) -> None:
    spec = root / "openspec" / "changes" / "demo" / "specs" / "thing" / "spec.md"
    spec.parent.mkdir(parents=True)
    spec.write_text("### Requirement: It works\n\n### Requirement: It is fast\n")


REGISTER = (
    "| ID | Kind | Capability | Requirement |\n"
    "|---|---|---|---|\n"
    "| R1 | functional | `thing` | It works |\n"
    "| R2 | non-functional | `thing` | It is fast |\n"
)


def test_a_complete_register_has_no_problem(tmp_path: Path) -> None:
    synthetic_specs(tmp_path)
    assert register_problems(REGISTER, tmp_path) == []


def test_a_retired_id_keeps_its_number_out_of_use(tmp_path: Path) -> None:
    synthetic_specs(tmp_path)
    register = REGISTER.replace("| R2 | non", "| R3 | non") + "\n- R2, removed by `old-change`\n"
    assert register_problems(register, tmp_path) == []


@pytest.mark.parametrize(
    ("register", "expected"),
    [
        ("", ["the register holds no requirement"]),
        (
            REGISTER.replace("| R2 | non-functional | `thing` | It is fast |\n", ""),
            ['`thing`: "It is fast" is in a spec and not in the register'],
        ),
        (
            REGISTER + "| R3 | functional | `thing` | It flies |\n",
            ["R3 names a requirement that no spec holds"],
        ),
        (
            REGISTER + "| R3 | functional | `thing` | It works |\n",
            ["R1 registers a requirement twice", "R3 registers a requirement twice"],
        ),
        (
            REGISTER.replace("| R2 | non", "| R5 | non"),
            ["the register's and the retired IDs do not run from R1 without a gap"],
        ),
        (
            REGISTER.replace("| R1 | fun", "| R3 | fun") + "\n- R1, removed by `old-change`\n",
            ["the register's IDs are not in order"],
        ),
        (
            REGISTER + "\n- R2, removed by `old-change`\n",
            [
                "the register's and the retired IDs do not run from R1 without a gap",
                "R2 is both registered and retired",
            ],
        ),
        (
            REGISTER.replace("non-functional", "nice-to-have"),
            ["R2 has a kind outside the list"],
        ),
    ],
)
def test_a_register_out_of_step_with_the_specs_is_reported(
    tmp_path: Path, register: str, expected: list[str]
) -> None:
    synthetic_specs(tmp_path)
    assert register_problems(register, tmp_path) == expected


PAGE = (
    "**Spec:** `thing`\n\n**Requirements:** R1, R2\n\n## How it is validated\n\nBy its scenarios.\n"
)


def synthetic_features(root: Path, index: str, page: str, name: str = "thing.md") -> Path:
    features = root / "features"
    features.mkdir(parents=True)
    (features / "README.md").write_text(index)
    (features / name).write_text(page)
    return features


def test_a_complete_feature_folder_has_no_problem(tmp_path: Path) -> None:
    features = synthetic_features(tmp_path, "- [Thing](thing.md)\n", PAGE)
    assert feature_problems(REGISTER, features) == []


@pytest.mark.parametrize(
    ("index", "page", "expected"),
    [
        ("Nothing linked.\n", PAGE, ["thing.md is not linked from the index"]),
        (
            "- [Thing](thing.md)\n",
            PAGE.replace("R1, R2", "R1, R2, R9"),
            ["thing.md names R9, which the register does not hold"],
        ),
        (
            "- [Thing](thing.md)\n",
            PAGE.replace("**Requirements:** R1, R2\n", "No requirements named.\n"),
            [
                "thing.md does not have one line naming its spec and one its requirements",
                "`thing` has no feature page for R1, R2",
            ],
        ),
        (
            "- [Thing](thing.md)\n",
            PAGE.replace("**Spec:** `thing`\n", ""),
            [
                "thing.md does not have one line naming its spec and one its requirements",
                "`thing` has no feature page for R1, R2",
            ],
        ),
        (
            "- [Thing](thing.md)\n- [Gone](gone.md)\n",
            PAGE,
            ["the index links gone.md, which does not exist"],
        ),
        (
            "- [Thing](thing.md)\n",
            PAGE.replace("R1, R2", "R2"),
            ["R1 is not on the page for `thing`"],
        ),
        (
            "- [Thing](thing.md)\n",
            PAGE.replace("R1, R2", "R1"),
            ["R2 is not on the page for `thing`"],
        ),
        (
            "- [Thing](thing.md)\n",
            PAGE.replace("## How it is validated\n\nBy its scenarios.\n", ""),
            ["thing.md does not say how it is validated"],
        ),
        (
            "- [Thing](thing.md)\n",
            PAGE.replace("By its scenarios.\n", ""),
            ["thing.md does not say how it is validated"],
        ),
    ],
)
def test_a_feature_folder_out_of_step_with_the_register_is_reported(
    tmp_path: Path, index: str, page: str, expected: list[str]
) -> None:
    features = synthetic_features(tmp_path, index, page)
    assert feature_problems(REGISTER, features) == expected


def test_a_page_is_named_for_its_spec_and_holds_only_its_spec_requirements(
    tmp_path: Path,
) -> None:
    features = synthetic_features(tmp_path, "- [Other](other.md)\n", PAGE, name="other.md")
    assert feature_problems(REGISTER, features) == ["other.md is not named for its spec `thing`"]
    register = REGISTER + "| R3 | functional | `else` | It flies |\n"
    features = synthetic_features(
        tmp_path / "b", "- [Thing](thing.md)\n", PAGE.replace("R1, R2", "R1, R2, R3")
    )
    assert feature_problems(register, features) == [
        "thing.md names R3, which `else` holds",
        "`else` has no feature page for R3",
    ]


def test_a_page_for_a_spec_the_register_does_not_hold_is_reported(tmp_path: Path) -> None:
    ghost = "**Spec:** `ghost`\n\n**Requirements:** none\n\n## How it is validated\n\nBy review.\n"
    features = synthetic_features(tmp_path, "- [Ghost](ghost.md)\n", ghost, name="ghost.md")
    assert feature_problems(REGISTER, features) == [
        "ghost.md names the spec `ghost`, which the register does not hold",
        "`thing` has no feature page for R1, R2",
    ]


def test_a_features_folder_without_an_index_or_pages_is_reported(tmp_path: Path) -> None:
    (tmp_path / "features").mkdir()
    assert feature_problems(REGISTER, tmp_path / "features") == ["the features folder has no index"]
    (tmp_path / "features" / "README.md").write_text("Index.\n")
    assert feature_problems(REGISTER, tmp_path / "features") == ["the features folder has no page"]


def change_problems(changes: Path) -> list[str]:
    problems = []
    for proposal in sorted(changes.rglob("proposal.md")):
        specs = {spec.parent.name for spec in (proposal.parent / "specs").glob("*/spec.md")}
        text = proposal.read_text(encoding="utf-8")
        problems += [f"{proposal.parent.name}: {p}" for p in proposal_problems(text, specs)]
    return problems


def test_each_proposal_lists_its_specs_and_says_how_each_is_validated() -> None:
    assert list(CHANGES.rglob("proposal.md")), "no proposal was found, so this test covered nothing"
    problems = change_problems(CHANGES)
    assert not problems, "\n".join(problems)


PROPOSAL = (
    "## Capabilities\n\n### New Capabilities\n\n- `thing`: does it.\n\n"
    "## How the outcome is validated\n\n| `thing` | by its scenarios |\n"
)


def test_a_proposal_out_of_step_with_its_specs_is_reported() -> None:
    assert proposal_problems(PROPOSAL, {"thing"}) == []
    assert proposal_problems(PROPOSAL, {"thing", "else"}) == [
        "`else` is a spec the proposal does not list",
        "the proposal does not say how `else` is validated",
    ]
    assert proposal_problems(PROPOSAL, set()) == ["the proposal lists `thing`, which has no spec"]


@pytest.mark.parametrize(
    "row",
    ["", "| `thing` |  |", "`thing` is not validated yet."],
    ids=["no row", "an empty row", "a mention that is not a row"],
)
def test_a_capability_without_a_validation_row_is_reported(row: str) -> None:
    unvalidated = PROPOSAL.replace("| `thing` | by its scenarios |", row)
    assert proposal_problems(unvalidated, {"thing"}) == [
        "the proposal does not say how `thing` is validated"
    ]


def test_a_capability_listed_outside_its_section_is_not_counted() -> None:
    elsewhere = PROPOSAL.replace("- `thing`: does it.\n\n", "") + (
        "\n## Impact\n\n- `thing`: does it.\n"
    )
    assert proposal_problems(elsewhere, {"thing"}) == [
        "`thing` is a spec the proposal does not list"
    ]


def test_a_validation_row_outside_its_section_is_not_counted() -> None:
    elsewhere = PROPOSAL.replace("| `thing` | by its scenarios |\n", "") + (
        "\n## Impact\n\n| `thing` | by its scenarios |\n"
    )
    assert proposal_problems(elsewhere, {"thing"}) == [
        "the proposal does not say how `thing` is validated"
    ]


def test_every_change_is_checked_against_its_own_specs(tmp_path: Path) -> None:
    for name in ("one", "archive/2026-01-01-two"):
        spec = tmp_path / name / "specs" / "thing" / "spec.md"
        spec.parent.mkdir(parents=True)
        spec.write_text("### Requirement: It works\n")
        (tmp_path / name / "proposal.md").write_text(PROPOSAL)
    assert change_problems(tmp_path) == []
    for name in ("one", "archive/2026-01-01-two"):
        (tmp_path / name / "specs" / "else").mkdir()
        (tmp_path / name / "specs" / "else" / "spec.md").write_text("### Requirement: It flies\n")
    assert change_problems(tmp_path) == [
        "2026-01-01-two: `else` is a spec the proposal does not list",
        "2026-01-01-two: the proposal does not say how `else` is validated",
        "one: `else` is a spec the proposal does not list",
        "one: the proposal does not say how `else` is validated",
    ]


WORKFLOW = """\
permissions:
  contents: read
jobs:
  report:
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
"""

HOW_IT_WORKS = """\
## Credentials and permissions

| Workflow | Job | Permissions |
|---|---|---|
| `report.yml` | `report` | `contents: read`, `pull-requests: write` |

## Connections to the outside world

- `actions/checkout`, from GitHub, over HTTPS.

## Flows

### A merge

```mermaid
flowchart LR
  A --> B
```
"""


def synthetic_workflow(root: Path, text: str = WORKFLOW) -> list[Path]:
    path = root / "report.yml"
    path.write_text(text)
    return [path]


def test_a_complete_how_it_works_page_has_no_problem(tmp_path: Path) -> None:
    assert how_it_works_problems(HOW_IT_WORKS, synthetic_workflow(tmp_path)) == []


@pytest.mark.parametrize(
    ("page", "expected"),
    [
        (
            HOW_IT_WORKS.replace(", `pull-requests: write`", ""),
            ["report.yml job `report` gets `pull-requests: write`, which is not listed"],
        ),
        (
            HOW_IT_WORKS.replace(
                "`pull-requests: write`", "`pull-requests: write`, `issues: write`"
            ),
            ["report.yml job `report` is listed with `issues: write`, not granted"],
        ),
        (
            HOW_IT_WORKS.replace("| `report.yml` | `report` |", "| `report.yml` | `other` |"),
            [
                "report.yml job `report` is not in the permissions table",
                "the permissions table lists report.yml job `other`, which no workflow has",
            ],
        ),
        (
            HOW_IT_WORKS.replace("`actions/checkout`", "a checkout"),
            ["report.yml runs `actions/checkout`, which is not listed"],
        ),
        (
            HOW_IT_WORKS.replace("```mermaid\nflowchart LR\n  A --> B\n```\n", "Words only.\n"),
            ["the flow 'A merge' has no diagram"],
        ),
        (
            HOW_IT_WORKS.replace("### A merge", "A merge"),
            ["how it works lists no flow"],
        ),
    ],
)
def test_a_how_it_works_page_missing_a_permission_action_or_diagram_is_reported(
    tmp_path: Path, page: str, expected: list[str]
) -> None:
    assert how_it_works_problems(page, synthetic_workflow(tmp_path)) == expected


def test_a_how_it_works_page_missing_a_section_is_reported(tmp_path: Path) -> None:
    page = HOW_IT_WORKS.replace("## Flows", "## Other")
    assert how_it_works_problems(page, synthetic_workflow(tmp_path)) == [
        "how it works has no section 'Flows'"
    ]


def test_each_job_gets_its_own_permissions_or_else_the_workflows() -> None:
    text = (
        "permissions: read-all\njobs:\n  a:\n    permissions:\n      actions: read\n"
        "  b:\n    runs-on: x\n"
    )
    assert granted(yaml.safe_load(text)) == {"a": {"actions: read"}, "b": {"read-all"}}
    assert granted(yaml.safe_load("jobs:\n  c:\n    runs-on: x\n")) == {"c": {DEFAULT}}


def test_a_widened_job_permission_is_reported_even_when_the_page_mentions_it(
    tmp_path: Path,
) -> None:
    widened = WORKFLOW.replace("contents: read\n      pull", "contents: write\n      pull")
    page = HOW_IT_WORKS + "\nIt needs no `contents: write`.\n"
    assert how_it_works_problems(page, synthetic_workflow(tmp_path, widened)) == [
        "report.yml job `report` gets `contents: write`, which is not listed",
        "report.yml job `report` is listed with `contents: read`, not granted",
    ]


def test_a_container_or_service_image_must_be_named(tmp_path: Path) -> None:
    text = (
        WORKFLOW
        + "    container: alpine@sha256:abc\n    services:\n      db:\n        image: postgres:16\n"
    )
    assert how_it_works_problems(HOW_IT_WORKS, synthetic_workflow(tmp_path, text)) == [
        "report.yml runs the image `alpine@sha256:abc`, which is not listed",
        "report.yml runs the image `postgres:16`, which is not listed",
    ]


def test_workflows_ending_in_yaml_are_collected(tmp_path: Path) -> None:
    folder = tmp_path / ".github" / "workflows"
    folder.mkdir(parents=True)
    (folder / "a.yml").write_text(WORKFLOW)
    (folder / "b.yaml").write_text(WORKFLOW)
    assert [p.name for p in workflows(tmp_path)] == ["a.yml", "b.yaml"]


# What crosses the tool's boundary, the README's uses to avoid, and the diagrams' form
# (R279, R280, R281; design decision 24 of `add-pr-cost-calculator`).

RECORD_FIELD = re.compile(r"^- \*\*(Boundary|Status|Closed by):\*\* (.+?)\s*$", re.M)
RECORD_ID = re.compile(r"\bDR-\d+\b")
CITED_ID = re.compile(r"\bDR-\d+\b|\bR\d+\b")
HEADING = re.compile(r"^## (.+?)\s*$", re.M)
SUBHEADING = re.compile(r"^### (.+?)\s*$", re.M)
WILL_DO = "What it will do"
USES_HEADING = "What it is for, and what to avoid using it for"
DOCUMENTS = "Documentation"
OWN_REASONS = frozenset({"R279", "DR-286"})
FIRST_STEP = re.compile(r"^[ \t]*(?:[-*+]|\d+[.)])[ \t]|`|~~~", re.M)
LIST_ITEM = re.compile(r"^(?:[-*+]|\d+[.)])[ \t]")
REQUIREMENT_ID = re.compile(r"\bR\d+\b")
ANY_MERMAID_FENCE = re.compile(r"^[ \t>]*(?:`{3,}|~{3,})[ \t]*mermaid\b", re.M | re.I)
WORKFLOW_INPUT = re.compile(
    r"^\s*(?:-\s+)?(?:uses:\s*([^@\s]+)@|runs-on:\s*([^\s#]+)|python-version:\s*(.+?)\s*$"
    r"|(?:python|node)-version-file:\s*([^\s#]+))",
    re.M,
)
INPUTS = "Inputs and outputs"
CROSSING = "What comes in and what goes out"
TOOL_IN = "What the tool takes in when it runs"
REPOSITORY_IN = "What this repository takes in to be built and checked"
GOES_OUT = "What goes out to adopters"
TABLES = (TOOL_IN, REPOSITORY_IN, GOES_OUT)
MERMAID = re.compile(r"^```mermaid[ \t]*\n(.*?)^```[ \t]*$", re.M | re.S)
QUOTED_NUMBER = re.compile(r'"(\d+)\) ')
BARE_NUMBER = re.compile(r"(?:[\[({>|]|^)[ \t]*(\d+)\)", re.M)
SEQUENCE_NUMBER = re.compile(r"(?::|\bas)[ \t]+(\d+)\) ")
EXPLAINED = re.compile(r"^- (\d+)\) ")
IDENTIFIER = re.compile(r"[A-Za-z0-9]{1,3}")
ARROW = re.compile(r"<?(?:-{2,}|={2,}|-\.+-|~{3,})[->ox]?|<?-+>>?|<?-->>|<<-+|-\)|--\)|-x|--x")
BRACKETS = re.compile(r"[\[({][^\[\](){}]*[\])}]|>[^\[\](){}]*\]")
FLOW_WORDS = frozenset({"flowchart", "graph", "direction", "end"})
SEQUENCE_WORDS = frozenset(
    {
        "Note",
        "note",
        "loop",
        "alt",
        "else",
        "opt",
        "par",
        "and",
        "rect",
        "end",
        "autonumber",
        "activate",
        "deactivate",
        "critical",
        "break",
        "option",
        "box",
    }
)
HOW_IT_WORKS_LINK = re.compile(r"\]\((?:\./)?docs/how-it-works\.md\)")


@dataclass(frozen=True)
class Record:
    boundary: str
    open: bool


def decision_records(root: Path) -> dict[str, Record]:
    """Each decision record by its ID, with the boundary that it faces and whether it is
    open: accepted and closed by none."""
    found = {}
    for path in sorted((root / "docs" / "decisions").glob("DR-*.md")):
        ident = RECORD_ID.match(path.name)
        if not ident:
            continue
        fields = dict(RECORD_FIELD.findall(path.read_text(encoding="utf-8")))
        found[ident[0]] = Record(
            fields.get("Boundary", ""),
            fields.get("Status") == "accepted" and fields.get("Closed by") == "none",
        )
    return found


def register_ids(root: Path) -> set[str]:
    text = (root / "docs" / "requirements.md").read_text(encoding="utf-8")
    return {row.ident for row in register_rows(text)}


def slug(heading: str) -> str:
    """The fragment that GitHub gives a heading."""
    return re.sub(r"[^a-z0-9 _-]", "", heading.lower()).replace(" ", "-")


def cited_problem(ident: str, records: dict[str, Record], requirements: set[str]) -> str:
    if ident.startswith("DR-"):
        record = records.get(ident)
        if record is None:
            return f"{ident}, which no record holds"
        return "" if record.open else f"{ident}, which is closed"
    return "" if ident in requirements else f"{ident}, which the register does not hold"


def readme_uses_problems(
    readme: str, records: dict[str, Record], requirements: set[str]
) -> list[str]:
    """What R279 asks of the README's section on uses to avoid, and of a short start."""
    names = HEADING.findall(readme)
    if USES_HEADING not in names:
        return [f"the README has no section {USES_HEADING!r}"]
    problems = []
    at = names.index(USES_HEADING)
    if WILL_DO not in names or names.index(WILL_DO) > at:
        problems.append(
            f"the README's section {USES_HEADING!r} comes before its section {WILL_DO!r}"
        )
    if DOCUMENTS not in names or names.index(DOCUMENTS) < at:
        problems.append(f"the README's section {USES_HEADING!r} comes after its list of documents")
    uses = [line for line in section(readme, USES_HEADING).splitlines() if LIST_ITEM.match(line)]
    if not uses:
        problems.append(f"the README's section {USES_HEADING!r} lists no use to avoid")
    for line in uses:
        cited = CITED_ID.findall(line)
        if not set(cited) - OWN_REASONS:
            problems.append(
                f"the use to avoid {line[:60]!r} cites no requirement or record but R279 and DR-286"
            )
        for ident in dict.fromkeys(cited):
            problem = cited_problem(ident, records, requirements)
            if problem:
                problems.append(f"the use to avoid {line[:60]!r} cites {problem}")
    if names and names[0] != WILL_DO:
        start = section(readme, names[0])
        link = start.find(f"](#{slug(USES_HEADING)})")
        step = FIRST_STEP.search(start)
        if link < 0 or (step is not None and step.start() < link):
            problems.append(
                f"the short start, {names[0]!r}, does not link the section {USES_HEADING!r}"
                " before its first step"
            )
    return problems


def table_rows(body: str) -> list[list[str]]:
    lines = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    return [[cell.strip() for cell in line.strip("|").split("|")] for line in lines[2:]]


def crossing_problems(text: str, records: dict[str, Record]) -> list[str]:
    """What R280 asks of the section of how it works on what comes in and goes out."""
    names = HEADING.findall(text)
    if CROSSING not in names:
        return [f"how it works has no section {CROSSING!r}"]
    problems = []
    if INPUTS not in names or names.index(INPUTS) > names.index(CROSSING):
        problems.append(f"the section {CROSSING!r} stands before the section {INPUTS!r}")
    parts = SUBHEADING.split(section(text, CROSSING))
    tables = dict(zip(parts[1::2], parts[2::2], strict=True))
    cited: dict[str, set[str]] = {table: set() for table in TABLES}
    for table in TABLES:
        rows = table_rows(tables.get(table, ""))
        if not rows:
            problems.append(f"the section {CROSSING!r} has no table {table!r}")
        for row in rows:
            if len(row) != 4:
                problems.append(f"the row {row[0]!r} of {table!r} has {len(row)} cells, not 4")
                continue
            thing, _, pinned, cell = row
            if not re.search(r"[A-Za-z]", pinned):
                problems.append(f"the row {thing!r} of {table!r} gives no word on how it is pinned")
            for ident in RECORD_ID.findall(cell):
                problem = cited_problem(ident, records, set())
                if problem:
                    problems.append(f"the row {thing!r} of {table!r} cites {problem}")
                cited[table].add(ident)
    incoming = cited[TOOL_IN] | cited[REPOSITORY_IN]
    for ident, record in records.items():
        if record.open and record.boundary == "incoming" and ident not in incoming:
            problems.append(f"{ident} faces incoming, and neither table of what comes in cites it")
        if record.open and record.boundary == "outgoing" and ident not in cited[GOES_OUT]:
            problems.append(f"{ident} faces outgoing, and the table {GOES_OUT!r} does not cite it")
    return problems


def workflow_input_problems(text: str, root: Path) -> list[str]:
    """Each action, runner image, Python version and file of versions that a workflow of this
    repository names, and the version that such a file holds, is named in the text (R280)."""
    named: dict[str, str] = {}
    for workflow in workflows(root):
        where = workflow.relative_to(root).as_posix()
        for match in WORKFLOW_INPUT.finditer(workflow.read_text(encoding="utf-8")):
            action, runner, versions, version_file = match.groups()
            found = [action, runner] if action or runner else []
            if versions and not versions.startswith("$"):
                found += re.findall(r"[\w.]+", versions)
            if version_file:
                found.append(version_file)
                held = root / version_file
                if held.is_file():
                    found.append(held.read_text(encoding="utf-8").strip())
            for thing in found:
                if thing:
                    named.setdefault(thing, where)
    if not named:
        return ["no workflow names an input, so the check read nothing"]
    return [
        f"{where} names {thing!r}, and the section {CROSSING!r} does not"
        for thing, where in named.items()
        if f"`{thing}`" not in text
    ]


def diagram_identifiers(block: str) -> list[str]:
    """The identifiers of a diagram's nodes, subgraphs and participants: the words that are
    left once its quoted labels, its edges' labels, its shapes and its keywords are taken
    out, and in a sequence diagram what each line names before its first `:`."""
    lines = block.splitlines()
    sequence = bool(lines) and lines[0].strip() == "sequenceDiagram"
    found = []
    for raw in lines[1:]:
        line = re.sub(r'"[^"]*"', "", raw.strip())
        line = re.sub(r"\|[^|]*\|", "", line)
        words = line.split()
        if not words:
            continue
        if sequence:
            if words[0] in ("participant", "actor"):
                found.extend(words[1:2])
            elif words[0] not in SEQUENCE_WORDS:
                head = line.split(":", 1)[0]
                found.extend(part for part in re.split(r"[-<>x)+ ]+", head) if part)
            continue
        if words[0] in FLOW_WORDS:
            continue
        if words[0] == "subgraph":
            found.extend(re.findall(r"^[^\s\[({]+", " ".join(words[1:]))[:1])
            continue
        before = None
        while before != line:
            before, line = line, BRACKETS.sub(" ", line)
        found.extend(word for word in re.split(r"[\s&]+", ARROW.sub(" ", line)) if word)
    return found


def explained_items(text: str, end: int) -> list[str]:
    """The items of the list right after a diagram, each with its continued lines."""
    items: list[str] = []
    for line in text[end:].splitlines()[1:]:
        if not line.strip():
            if items:
                break
            continue
        if line.startswith("- "):
            items.append(line)
        elif items and line.startswith("  "):
            items[-1] += " " + line.strip()
        else:
            break
    return items


def explained_numbers(text: str, end: int) -> list[int]:
    """The numbers that the list right after a diagram explains, in their order."""
    return [
        int(match[1]) for item in explained_items(text, end) if (match := EXPLAINED.match(item))
    ]


def diagram_problems(name: str, text: str) -> list[str]:
    """What R281 asks of each Mermaid diagram on a page."""
    problems = []
    for fence in ANY_MERMAID_FENCE.finditer(text):
        if not fence[0].startswith("```mermaid"):
            line = text.count(chr(10), 0, fence.start()) + 1
            problems.append(
                f"{name}:{line}: a Mermaid block in a fence that the checks do not read"
            )
    for block in MERMAID.finditer(text):
        where = f"{name}:{text.count(chr(10), 0, block.start()) + 1}"
        body = block[1]
        sequence = body.strip().startswith("sequenceDiagram")
        drawn = [int(n) for n in QUOTED_NUMBER.findall(body)]
        if sequence:
            drawn += [int(n) for n in SEQUENCE_NUMBER.findall(body)]
        else:
            unquoted = re.sub(r'"[^"]*"', '""', body)
            for number in BARE_NUMBER.findall(unquoted):
                problems.append(f"{where}: the number {number} stands in a label without quotes")
        explained = explained_numbers(text, block.end())
        for item in explained_items(text, block.end()):
            if not REQUIREMENT_ID.search(item):
                problems.append(f"{where}: the explanation {item[:40]!r} cites no requirement")
        if not drawn:
            problems.append(f"{where}: the diagram numbers none of its parts")
        for number in sorted(set(drawn) - set(explained)):
            problems.append(f"{where}: the number {number} is drawn and not explained below")
        for number in sorted(set(explained) - set(drawn)):
            problems.append(f"{where}: the number {number} is explained and not drawn")
        for number in sorted({n for n in explained if explained.count(n) > 1}):
            problems.append(f"{where}: the number {number} is explained twice")
        every = set(drawn) | set(explained)
        for number in sorted(set(range(1, max(every, default=0) + 1)) - every):
            problems.append(f"{where}: the number {number} is skipped")
        for ident in dict.fromkeys(diagram_identifiers(body)):
            if not IDENTIFIER.fullmatch(ident):
                problems.append(
                    f"{where}: the identifier {ident!r} is not one to three letters or digits"
                )
    return problems


def written_pages(root: Path) -> list[Path]:
    """The Markdown pages that this repository writes."""
    import conventions

    listed = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"], cwd=root, capture_output=True, check=True
    ).stdout.decode("utf-8")
    return [
        root / path
        for path in sorted(listed.split("\0"))
        if path and not conventions.written_by_others(path)
    ]


def page_diagram_problems(root: Path) -> list[str]:
    """Every feature page and how it works hold a diagram, how it works holds its overview in
    its first section, and the README links that page without a fragment (R281)."""
    problems = []
    features = root / "docs" / "features"
    pages = [p for p in sorted(features.glob("*.md")) if p.name != "README.md"]
    if not pages:
        problems.append("docs/features/ holds no feature page")
    how = root / "docs" / "how-it-works.md"
    for page in [*pages, how]:
        if not MERMAID.search(page.read_text(encoding="utf-8")):
            problems.append(f"{page.relative_to(root).as_posix()} holds no Mermaid diagram")
    text = how.read_text(encoding="utf-8")
    names = HEADING.findall(text)
    if not names or not MERMAID.search(section(text, names[0])):
        problems.append("the first section of docs/how-it-works.md holds no diagram")
    if not HOW_IT_WORKS_LINK.search((root / "README.md").read_text(encoding="utf-8")):
        problems.append("the README does not link docs/how-it-works.md without a fragment")
    return problems


def test_the_readme_says_what_the_tool_is_for_and_which_uses_to_avoid() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    problems = readme_uses_problems(readme, decision_records(ROOT), register_ids(ROOT))
    assert not problems, "\n".join(problems)


def test_how_it_works_lists_everything_that_comes_in_and_goes_out() -> None:
    text = (ROOT / "docs" / "how-it-works.md").read_text(encoding="utf-8")
    records = decision_records(ROOT)
    assert records, "no decision record was read, so this test covered nothing"
    problems = crossing_problems(text, records) + workflow_input_problems(
        section(text, CROSSING), ROOT
    )
    assert not problems, "\n".join(problems)


def test_every_diagram_numbers_its_parts_and_explains_them() -> None:
    pages = written_pages(ROOT)
    problems = [
        problem
        for page in pages
        for problem in diagram_problems(
            page.relative_to(ROOT).as_posix(), page.read_text(encoding="utf-8")
        )
    ]
    assert any(MERMAID.search(page.read_text(encoding="utf-8")) for page in pages), (
        "no page holds a Mermaid diagram, so this test covered nothing"
    )
    assert not problems, "\n".join(problems)


def test_each_feature_page_and_how_it_works_hold_a_diagram_and_the_readme_links_it() -> None:
    problems = page_diagram_problems(ROOT)
    assert not problems, "\n".join(problems)


OPEN_RECORDS = {
    "DR-002": Record("outgoing", True),
    "DR-286": Record("outgoing", True),
    "DR-044": Record("incoming", True),
    "DR-041": Record("incoming", True),
    "DR-010": Record("inside", True),
    "DR-009": Record("incoming", False),
}
REQUIREMENTS = {"R3", "R94", "R279"}
USES_SECTION = (
    "## What it is for, and what to avoid using it for\n\n"
    "It estimates what a pull request cost.\n\n"
    "- As a bill (R94, [DR-002](docs/decisions/DR-002-x.md)).\n"
    "- In a session that also works on private repositories (R3).\n\n"
)
README = (
    "# Tool\n\nIntro.\n\n## What it will do\n\nThings.\n\n"
    + USES_SECTION
    + "## Documentation\n\n- [How it works](docs/how-it-works.md)\n"
)


def test_a_readme_with_its_section_on_uses_passes() -> None:
    assert readme_uses_problems(README, OPEN_RECORDS, REQUIREMENTS) == []


def test_a_short_start_that_links_the_uses_before_its_first_step_passes() -> None:
    start = (
        "# Tool\n\nIntro.\n\n## Start here\n\nFirst read [the uses to avoid]"
        "(#what-it-is-for-and-what-to-avoid-using-it-for).\n\n1. Turn it on.\n\n"
    )
    readme = README.replace("# Tool\n\nIntro.\n\n", start)
    assert readme_uses_problems(readme, OPEN_RECORDS, REQUIREMENTS) == []


@pytest.mark.parametrize(
    ("readme", "expected"),
    [
        (README.replace(USES_SECTION, ""), "has no section"),
        (
            README.replace("## What it will do\n\nThings.\n\n" + USES_SECTION, USES_SECTION)
            + "## What it will do\n\nThings.\n",
            "comes before its section 'What it will do'",
        ),
        (
            README.replace(USES_SECTION, "") + USES_SECTION,
            "comes after its list of documents",
        ),
        (
            README.replace("- In a session", "Text: in a session").replace(
                "- As a bill (R94, [DR-002](docs/decisions/DR-002-x.md)).\n", ""
            ),
            "lists no use to avoid",
        ),
        (README.replace("(R3)", ""), "cites no requirement or record"),
        (README.replace("(R3)", "(R279, DR-286)"), "cites no requirement or record"),
        (README.replace("(R3)", "(R7)"), "R7, which the register does not hold"),
        (README.replace("(R3)", "(DR-009)"), "DR-009, which is closed"),
        (README.replace("(R3)", "(DR-999)"), "DR-999, which no record holds"),
        (
            README.replace("# Tool\n\nIntro.\n\n", "# Tool\n\nIntro.\n\n## Start\n\n1. On.\n\n"),
            "does not link the section",
        ),
        (
            README.replace(
                "# Tool\n\nIntro.\n\n",
                "# Tool\n\nIntro.\n\n## Start\n\n```sh\ngit config x\n```\n\n"
                "[Uses](#what-it-is-for-and-what-to-avoid-using-it-for)\n\n",
            ),
            "does not link the section",
        ),
        (
            README.replace(
                "# Tool\n\nIntro.\n\n",
                "# Tool\n\nIntro.\n\n## Start\n\n- Turn it on.\n\n"
                "[Uses](#what-it-is-for-and-what-to-avoid-using-it-for)\n\n",
            ),
            "does not link the section",
        ),
        (
            README.replace(
                "# Tool\n\nIntro.\n\n",
                "# Tool\n\nIntro.\n\n## Start\n\nRun `git config x`, then read "
                "[Uses](#what-it-is-for-and-what-to-avoid-using-it-for).\n\n",
            ),
            "does not link the section",
        ),
        (
            README.replace(
                "- In a session that also works on private repositories (R3).", "* In a session."
            ),
            "cites no requirement or record",
        ),
        (
            README.replace(
                "- In a session that also works on private repositories (R3).", "1. In a session."
            ),
            "cites no requirement or record",
        ),
    ],
)
def test_a_section_on_uses_that_is_missing_out_of_place_or_unsupported_is_reported(
    readme: str, expected: str
) -> None:
    problems = readme_uses_problems(readme, OPEN_RECORDS, REQUIREMENTS)
    assert any(expected in problem for problem in problems), problems


CROSSING_SECTION = (
    "## Inputs and outputs\n\nData.\n\n"
    "## What comes in and what goes out\n\n"
    "### What the tool takes in when it runs\n\n"
    "| What | What crosses | Pinned | Records |\n|---|---|---|---|\n"
    "| Transcripts | Lines | Not pinned: Claude Code writes them | DR-044, DR-010 |\n\n"
    "### What this repository takes in to be built and checked\n\n"
    "| What | What crosses | Pinned | Records |\n|---|---|---|---|\n"
    "| Superpowers | Skills | A commit | DR-041 |\n\n"
    "### What goes out to adopters\n\n"
    "| What | What crosses | Pinned | Records |\n|---|---|---|---|\n"
    "| The comment | A figure | The release's commit | DR-002, DR-286 |\n\n"
    "## Flows\n"
)


def test_a_complete_section_on_what_crosses_passes() -> None:
    assert crossing_problems(CROSSING_SECTION, OPEN_RECORDS) == []


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (CROSSING_SECTION.replace("## What comes in and what goes out", "## Other"), "no section"),
        (CROSSING_SECTION.replace(" DR-041 |", " none |"), "DR-041 faces incoming"),
        (CROSSING_SECTION.replace("DR-002, DR-286", "DR-002"), "DR-286 faces outgoing"),
        (
            CROSSING_SECTION.replace("DR-044, DR-010", "DR-010").replace(
                "DR-002, DR-286", "DR-002, DR-286, DR-044"
            ),
            "DR-044 faces incoming",
        ),
        (CROSSING_SECTION.replace("| A commit |", "|  |"), "no word on how it is pinned"),
        (CROSSING_SECTION.replace("| A commit |", "| - |"), "no word on how it is pinned"),
        (CROSSING_SECTION.replace("DR-010", "DR-009"), "DR-009, which is closed"),
        (CROSSING_SECTION.replace("DR-010", "DR-999"), "DR-999, which no record holds"),
        (
            CROSSING_SECTION.replace("### What goes out to adopters", "### Elsewhere"),
            "has no table 'What goes out to adopters'",
        ),
        (
            CROSSING_SECTION.replace("## Inputs and outputs\n\nData.\n\n", "").replace(
                "## Flows\n", "## Inputs and outputs\n\nData.\n"
            ),
            "stands before the section 'Inputs and outputs'",
        ),
        (CROSSING_SECTION.replace("| Lines |", "| Lines | more |"), "has 5 cells"),
    ],
)
def test_a_record_left_out_of_the_section_or_cited_in_the_wrong_table_is_reported(
    text: str, expected: str
) -> None:
    problems = crossing_problems(text, OPEN_RECORDS)
    assert any(expected in problem for problem in problems), problems


INPUTS_WORKFLOW = (
    "jobs:\n  a:\n    runs-on: ubuntu-latest\n    strategy:\n      matrix:\n"
    '        python-version: ["3.11", "3.x"]\n    steps:\n'
    "      - uses: actions/checkout@0123456789012345678901234567890123456789 # v7\n"
    "      - uses: actions/setup-node@0123456789012345678901234567890123456789 # v7\n"
    "        with:\n          node-version-file: .node-version\n"
)
NAMED = (
    "`actions/checkout`, `actions/setup-node`, `ubuntu-latest`, `3.11`, `3.x`, "
    "`.node-version` holding `24`"
)


def workflow_tree(root: Path, workflow: str) -> Path:
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / ".github" / "workflows" / "ci.yml").write_text(workflow, encoding="utf-8")
    (root / ".node-version").write_text("24\n", encoding="utf-8")
    return root


def test_a_section_that_names_every_input_of_the_workflows_passes(tmp_path: Path) -> None:
    root = workflow_tree(tmp_path, INPUTS_WORKFLOW)
    assert workflow_input_problems(NAMED, root) == []


@pytest.mark.parametrize(
    ("named", "expected"),
    [
        (NAMED.replace("`actions/checkout`, ", ""), "'actions/checkout'"),
        (NAMED.replace("`ubuntu-latest`, ", ""), "'ubuntu-latest'"),
        (NAMED.replace("`3.11`, ", ""), "'3.11'"),
        (NAMED.replace("`.node-version` holding ", ""), "'.node-version'"),
        (NAMED.replace(" holding `24`", ""), "'24'"),
    ],
)
def test_an_input_that_a_workflow_names_and_the_section_does_not_is_reported(
    tmp_path: Path, named: str, expected: str
) -> None:
    root = workflow_tree(tmp_path, INPUTS_WORKFLOW)
    problems = workflow_input_problems(named, root)
    assert any(expected in problem for problem in problems), problems


def test_a_workflow_input_check_that_reads_no_workflow_fails(tmp_path: Path) -> None:
    problems = workflow_input_problems(NAMED, tmp_path)
    assert problems == ["no workflow names an input, so the check read nothing"]


FLOW_PAGE = (
    "# Page\n\n```mermaid\nflowchart LR\n"
    '  subgraph M1["Machine"]\n    T["1) Transcripts"] -->|read| H["2) Capture step"]\n  end\n'
    '  H --> S[("3) Store")] & L{"4) Staged?"}\n```\n\n'
    "- 1) Transcripts: what Claude Code writes (R2).\n"
    "- 2) Capture step: reads them (R3),\n  and keeps counts.\n"
    "- 3) Store: holds them (R47).\n- 4) Staged: a decision (R56).\n\nAfter.\n"
)
SEQUENCE_PAGE = (
    "# Page\n\n```mermaid\nsequenceDiagram\n  participant CC as 1) Claude Code\n"
    "  participant H as 2) Capture hook\n  CC->>H: 3) Stop, with the transcript\n"
    "  Note over H: what follows\n  alt on\n    H-->>CC: 4) Exit 0\n  end\n```\n\n"
    "- 1) Claude Code (R7).\n- 2) The hook (R1).\n- 3) The event (R9).\n- 4) The exit (R30).\n"
)


@pytest.mark.parametrize("page", [FLOW_PAGE, SEQUENCE_PAGE])
def test_a_numbered_and_explained_diagram_passes(page: str) -> None:
    assert diagram_problems("page.md", page) == []


def test_a_page_without_diagrams_has_no_diagram_problem() -> None:
    assert diagram_problems("page.md", "# Page\n\n```sh\necho 1) no\n```\n") == []


@pytest.mark.parametrize(
    ("page", "expected"),
    [
        (FLOW_PAGE.replace("- 4) Staged: a decision (R56).\n", ""), "4 is drawn and not explained"),
        (FLOW_PAGE.replace("- 1) Transcripts", "- 5) Transcripts"), "5 is explained and not drawn"),
        (FLOW_PAGE.replace("- 4) Staged", "- 3) Staged"), "3 is explained twice"),
        (
            FLOW_PAGE.replace('"4) Staged?"', '"5) Staged?"').replace("- 4) Staged", "- 5) Staged"),
            "4 is skipped",
        ),
        (FLOW_PAGE.replace('T["1) Transcripts"]', "T[1) Transcripts]"), "without quotes"),
        (FLOW_PAGE.replace("-->|read|", "-->|1) read|"), "without quotes"),
        (FLOW_PAGE.replace('M1["Machine"]', 'machine["Machine"]'), "'machine'"),
        (FLOW_PAGE.replace('H["2) Capture step"]', 'Hook["2) Capture step"]'), "'Hook'"),
        (FLOW_PAGE.replace("H --> S", "H_1 --> S"), "'H_1'"),
        (
            SEQUENCE_PAGE.replace("participant H as", "participant Hook as")
            .replace("CC->>H", "CC->>Hook")
            .replace("H-->>CC", "Hook-->>CC"),
            "'Hook'",
        ),
        (SEQUENCE_PAGE.replace("3) Stop", "Stop"), "3 is explained and not drawn"),
        (
            "# P\n\n```mermaid\nflowchart LR\n  A --> B\n```\n",
            "numbers none of its parts",
        ),
        (FLOW_PAGE.replace("\n- 1) Transcripts", "\nText.\n- 1) Transcripts"), "not explained"),
        (
            FLOW_PAGE.replace("- 3) Store: holds them (R47).", "- 3) Store: holds them."),
            "cites no requirement",
        ),
        (
            FLOW_PAGE.replace("- 3) Store: holds them (R47).", "- 3) Store (DR-010)."),
            "cites no requirement",
        ),
        (
            FLOW_PAGE.replace("```mermaid", "~~~mermaid").replace("```\n\n- 1)", "~~~\n\n- 1)"),
            "fence",
        ),
        ("# P\n\n- An item\n\n  ```mermaid\n  flowchart LR\n    LongName --> B\n  ```\n", "fence"),
        ("# P\n\n> ```mermaid\n> flowchart LR\n> ```\n", "fence"),
        ("# P\n\n````mermaid\nflowchart LR\n````\n", "fence"),
    ],
)
def test_a_number_left_unexplained_or_explained_but_not_drawn_is_reported(
    page: str, expected: str
) -> None:
    problems = diagram_problems("page.md", page)
    assert any(expected in problem for problem in problems), problems


def synthetic_pages(root: Path, feature: str, how: str, readme: str) -> None:
    (root / "docs" / "features").mkdir(parents=True)
    (root / "docs" / "features" / "README.md").write_text("# Features\n", encoding="utf-8")
    (root / "docs" / "features" / "thing.md").write_text(feature, encoding="utf-8")
    (root / "docs" / "how-it-works.md").write_text(how, encoding="utf-8")
    (root / "README.md").write_text(readme, encoding="utf-8")


HOW_PAGE = "# How\n\n## In one paragraph\n\nText.\n\n" + FLOW_PAGE.split("\n\n", 1)[1]
LINKING_README = "# Tool\n\nSee [how it works](docs/how-it-works.md).\n"


def test_pages_that_hold_their_diagrams_and_a_linking_readme_pass(tmp_path: Path) -> None:
    synthetic_pages(tmp_path, FLOW_PAGE, HOW_PAGE, LINKING_README)
    assert page_diagram_problems(tmp_path) == []


@pytest.mark.parametrize(
    ("feature", "how", "readme", "expected"),
    [
        ("# Thing\n", HOW_PAGE, LINKING_README, "docs/features/thing.md holds no Mermaid"),
        (FLOW_PAGE, "# How\n\n## A\n\nText.\n", LINKING_README, "how-it-works.md holds no"),
        (
            FLOW_PAGE,
            "# How\n\n## In one paragraph\n\nText.\n\n## Later\n\n" + FLOW_PAGE.split("\n\n", 1)[1],
            LINKING_README,
            "first section of docs/how-it-works.md holds no diagram",
        ),
        (FLOW_PAGE, HOW_PAGE, "# Tool\n", "does not link docs/how-it-works.md"),
        (
            FLOW_PAGE,
            HOW_PAGE,
            "# Tool\n\n[how](docs/how-it-works.md#overview)\n",
            "does not link docs/how-it-works.md",
        ),
    ],
)
def test_a_page_without_its_diagram_or_a_readme_without_the_link_is_reported(
    tmp_path: Path, feature: str, how: str, readme: str, expected: str
) -> None:
    synthetic_pages(tmp_path, feature, how, readme)
    problems = page_diagram_problems(tmp_path)
    assert any(expected in problem for problem in problems), problems


def test_the_index_of_the_feature_pages_needs_no_diagram(tmp_path: Path) -> None:
    synthetic_pages(tmp_path, FLOW_PAGE, HOW_PAGE, LINKING_README)
    problems = page_diagram_problems(tmp_path)
    assert not any("features/README.md" in problem for problem in problems)


def test_the_decision_records_are_read_with_their_boundary_and_whether_they_are_open(
    tmp_path: Path,
) -> None:
    folder = tmp_path / "docs" / "decisions"
    folder.mkdir(parents=True)
    fields = "- **Boundary:** {}\n- **Status:** {}\n- **Closed by:** {}\n"
    (folder / "DR-001-a.md").write_text(fields.format("incoming", "accepted", "none"))
    (folder / "DR-002-b.md").write_text(fields.format("outgoing", "closed", "DR-003"))
    (folder / "README.md").write_text("# Records\n")
    assert decision_records(tmp_path) == {
        "DR-001": Record("incoming", True),
        "DR-002": Record("outgoing", False),
    }


def test_a_heading_s_fragment_is_the_one_that_github_gives() -> None:
    assert slug("What it is for, and what to avoid using it for") == (
        "what-it-is-for-and-what-to-avoid-using-it-for"
    )
