# Assumptions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build task 1.19 of `add-pr-cost-calculator`: the assumptions under `docs/assumptions/`, the move of the threat model's section on assumptions, and `tests/test_assumptions.py`, which holds them.

**Architecture:** The assumptions are Markdown pages with a fixed grammar of one field per line, read by a test that resolves every citation against the register, the threat model, the records and the change's tasks, and that recomputes each assumption's place in the list from the threat model's ratings and the checks of its facts. The checks live in the test file, as the other document checks of this repository do, and each is shown to fail on a synthetic page that plants its defect.

**Tech Stack:** Python 3.11 standard library, pytest, git.

**Spec:** `openspec/changes/add-pr-cost-calculator/specs/project-standards/spec.md` ("The assumptions the design rests on are written down", "Each fact's check can be followed", "The assumptions give no other web address", "The assumptions with the most at stake come first"), design decision 14 and task 1.19 of the same change, DR-162 and DR-163.

## Global Constraints

- The tool supports Python 3.11 and every later release, with the standard library only; tests may use pytest and PyYAML, which `requirements-dev.txt` pins.
- Tests never use the network (DR-090). The git observation runs against a repository on the local disk, over `file://`.
- No test may reach Claude Code, GitHub, a vendor's prices, or adopters and people, so a fact about them is never `tested` alone.
- An observation names the file under `tests/` that reproduces what was seen, the date, and the program, the version that it prints and its build, and never whose work it was seen in. It gives no figure measured on someone's private work.
- Documentation is linked by its address, shown as its text, on a vendor's documentation host that the test lists or as a file at a full commit of a GitHub repository that it lists, by a path with no `.` or `..` segment, with the date it was read, and no page gives a web address anywhere else.
- The pages describe and never steer (`CLAUDE.md`): where one differs from `CLAUDE.md` or a spec, those hold.
- Records keep their words: no file under `docs/decisions/` changes.
- Every number written in the pages, the commit messages or the pull request is computed in the session that writes it.

---

## The grammar the test reads

The index, `docs/assumptions/README.md`:

```markdown
A risk below is rated with the assumption true, since the threat model rates each threat with its answer in place (DR-112).

## The assumptions, most at stake first

- **A1.** Claude Code keeps each session's transcript where the capture step can read it while the session lasts. Impact 3, risk 6. Page: [Claude Code](claude-code.md).
- **A68.** Other agents and review apps will expose their usage later. No threat. Page: [Adopters and people](adopters-and-people.md).

## Retired IDs

None yet. An entry names the ID and the change that removed it, as in "A7, removed by `change-name`".
```

A subject page, one of `claude-code.md`, `github.md`, `git.md`, `python-tools-and-prices.md` and `adopters-and-people.md`. Assumptions are `##` headings; on `python-tools-and-prices.md` they are `###` headings under `## Python`, `## The development tools` and `## Prices`, so that the test knows which facts are about prices:

```markdown
## A63. git can be kept offline and from asking for credentials.

- **Rests on it:** R30, R32, R45, R111, T45, T56, T86, DR-027, DR-060, DR-090
- **If it is wrong:** <what would change, never how to change it>
- **Fact:** In a partial clone, git fetches from the remote an object that a command needs and the clone lacks.
  - **Relied on:** R30, R45, R111, T45, DR-060
  - **Checked:** observed: `tests/test_git_lazy_fetch.py`, 2026-11-01, git, version `git version 2.43.0`, build `1:2.43.0-1ubuntu7.3`
```

`Checked` takes one of four forms:

- `tested: ` one or more collected tests, each as `` `tests/<file>.py::<name>` ``;
- `observed: ` the file under `tests/`, the date, the program, `version` and the text it prints, and `build` and its build;
- `documented: ` one or more links as `<https://...>`, then `read` and the date;
- `not yet: ` text that cites the task that will check it, as `` `add-pr-cost-calculator` task 1.1 ``, or `none will, since` and the reason.

A fact may also give `- **Handled by:**`, indented as its other fields, naming the collected tests that hold the tool's handling of the fact. A threat that rests on an assumption names it among its fields, as T45 does with `- **Assumptions:** A63`.

## Files

- Create: `tests/test_git_lazy_fetch.py`, the file that reproduces the observation that T45's answer rests on.
- Create: `tests/test_assumptions.py`, the parsers, the checks, their synthetic tests and the test of the repository's own pages.
- Create: `docs/assumptions/README.md` and the five subject pages.
- Modify: `docs/threat-model.md`: the section "Assumptions" keeps its heading with a pointer, each threat that rests on an assumption gets its `Assumptions` field, and each "(see Assumptions)" gives way to it.
- Modify: `docs/features/project-standards.md`, whose status and validation say that the assumptions are in place.
- Modify: `openspec/changes/add-pr-cost-calculator/tasks.md`, task 1.19 ticked.

### Task 1: The git observation

**Files:** Create `tests/test_git_lazy_fetch.py`.

- [x] **Step 1:** Write `test_git_no_lazy_fetch_keeps_a_partial_clone_from_fetching`: a repository on the local disk with one ledger blob and `uploadpack.allowFilter` on, a clone of it with `--filter=blob:none --no-checkout` over `file://`, and then, with `GIT_NO_LAZY_FETCH=1`, `git cat-file -s` on the blob fails and the blob stays missing; without it, the same command prints the blob's size. Every git runs with every `GIT_` variable of the caller's environment removed, `GIT_CONFIG_GLOBAL` set to an empty file in the test's folder and `GIT_CONFIG_NOSYSTEM` set, so that no setting of the person running the tests takes part.
- [x] **Step 2:** Write `test_a_variable_that_git_does_not_read_leaves_lazy_fetching_on`, the same clone with a misspelled variable, which fetches the blob: a git that ignores the variable behaves this way, so the first test fails on it.
- [x] **Step 3:** Run `.venv/bin/python -m pytest tests/test_git_lazy_fetch.py -v`. Expected: both pass on this machine's git, whose `git --version` and `dpkg-query -W git` are recorded in the observation.

### Task 2: The checks, test first

**Files:** Create `tests/test_assumptions.py`.

**Interfaces:**
- `problems(root: Path, collected: frozenset[str]) -> tuple[list[str], int]`: every problem of the assumptions under `root`, and how many facts were read.
- `collected_tests(root: Path) -> frozenset[str]`: the node IDs that `pytest --collect-only` lists.

- [x] **Step 1:** Write a synthetic repository fixture: a register with R1 and R2, a threat model with T1 to T3 rated and a retired ID, a record DR-001, a change with task 1.1, a test file, and an index and two subject pages that pass.
- [x] **Step 2:** Write one test per defect of task 1.19's list, each planting it in the passing fixture and asserting that the problems name the assumption, and what it names where the scenario says so: no "Rests on it" or "If it is wrong"; a fact without "Relied on" or "Checked"; a citation of a requirement, a threat, a record, a task, a decision or a path that does not exist; a test that is not collected; a threat and an assumption that do not name each other; a fact about Claude Code, GitHub, prices or adopters and people checked by a test alone; an observation without its file, its date, or its program, version and build; a documented fact that links another host, a GitHub file not at a full commit, link text other than its address, or no date; a path under a home folder or a session identifier on a page or in a file that an observation names, reported by file and line without quoting either; an assumption out of order, on the index and on its page; an index line without the impact or with a rating that differs from the threat model's; an assumption on the index and not on its page, or the reverse, or with another statement; a page that holds no assumption; and the threat model's settings that no fact names, or one named as checked.
- [x] **Step 3:** Write `test_the_assumptions_hold`, which runs the checks on the repository and fails when they read no fact.
- [x] **Step 4:** Run `.venv/bin/python -m pytest tests/test_assumptions.py`. Expected: every test fails, the synthetic ones because the checks do not exist yet, and the repository's because `docs/assumptions/` does not exist.
- [x] **Step 5:** Write the parsers and the checks until the synthetic tests pass. The repository's test still fails.

### Task 3: The pages and the move

**Files:** Create `docs/assumptions/*.md`. Modify `docs/threat-model.md`.

- [x] **Step 1:** Draft each subject page from the specs, the design, the threat model and the records, with the exploration's notes as a starting list: each assumption with what rests on it and what changes if it is wrong, each fact with where it is relied on and its check. A fact is `not yet` unless a test, a reproducing file or a page read on the day holds it.
- [x] **Step 2:** Put each sentence of the threat model's section into an assumption, word for word where it can be, and each sentence that states what the tool does into the spec that holds that behaviour, or leave it where a spec already holds it.
- [x] **Step 3:** List each of the threat model's settings that the owner keeps as a fact that points to its section, `not yet`.
- [x] **Step 4:** Number the assumptions in the order that the test computes, write the index, and give each threat that an assumption names its `Assumptions` field.
- [x] **Step 5:** Run `.venv/bin/python -m pytest tests/test_assumptions.py tests/test_threat_model.py tests/test_decisions.py`. Expected: pass.

### Task 4: Evidence, documentation and checks

- [x] **Step 1:** Run a script, once, that takes each sentence of the section from the default branch's threat model and finds it in the assumptions or the specs, listing every sentence that it does not find word for word; keep its output for the pull request with the reason for each listed change.
- [x] **Step 2:** Update the feature page and tick task 1.19.
- [x] **Step 3:** Run `pytest`, `ruff check .`, `ruff format --check .`, `mypy` and `scripts/verify-openspec.sh`. Expected: each exits 0.
- [x] **Step 4:** Commit by file name and push.

### Task 5: Review

- [x] **Step 1:** In a context separate from the builder's, rate each threat again against what was built, and add the threats that it brings.
- [x] **Step 2:** Run `/simplify`, `/security-review`, `/code-review` and `/verify`, each in its own context; post the findings, their resolutions and the index on the pull request.

### Task 6: The review's fixes

**Files:** Modify `tests/test_assumptions.py`, `tests/test_decisions.py`, `tests/test_git_lazy_fetch.py`, `docs/assumptions/*.md`, `docs/threat-model.md`, the spec of `project-standards` in the change, its design, `docs/requirements.md`, `docs/features/project-standards.md`, DR-162, the record that DR-238 replaced, `docs/decisions/README.md` and `README.md`.

**Interfaces:**
- `problems(root: Path, collected: frozenset[str], marked: frozenset[str] = frozenset()) -> tuple[list[str], int]`: as before, with the collected tests that a mark skips or expects to fail.
- `marked_tests(root: Path) -> frozenset[str]`: the collected tests that a mark skips or expects to fail.

- [x] **Step 1:** Update the change first, for each finding that changes what must hold: the requirements and scenarios of `project-standards`, design decision 14 and its risks, the register's row, the feature page, and DR-162 and the record that DR-238 replaced, which the default branch does not hold yet.
- [x] **Step 2:** Write a failing test for each finding that the checks fix, planting its defect in the passing fixture, and see each fail for the reason that the finding gives, or, where the check was written first, fail once the check's line is removed.
- [x] **Step 3:** Write the checks until the synthetic tests pass. The repository's test then fails on the facts that the new checks read.
- [x] **Step 4:** Fix the pages and the threat model: each fact that stated what the tool does, each threat that rests on an assumption without naming it, the threats that the review found, and the matrix.
- [x] **Step 5:** Run the move's script again, and `pytest`, `ruff check .`, `ruff format --check .`, `mypy` and `scripts/verify-openspec.sh`. Expected: each exits 0.
- [x] **Step 6:** Commit by file name and push.

## Self-review

- Every scenario of the four requirements maps to a test of Task 2 or Task 6, and every defect in task 1.19's list to one of the tests of Task 2's Step 2.
- The defect lists in Task 2 and in the task match word for word where the task names them.
- The plan is executed inline by its author, so its code blocks give the grammar and the interfaces, and the test file holds the code.
