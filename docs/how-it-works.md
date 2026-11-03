# How it works

This page explains the calculator as one product: what goes in, what comes out, how a cost is computed and from where, each flow, and every credential, permission and outside connection it uses. A developer who reads it should know what the tool does, and should treat anything it does that this page leaves out as a defect.

The calculator is designed and not built yet, so this page describes the design in `openspec/changes/add-pr-cost-calculator/`. It changes in the same pull request as what it describes, and `tests/test_documentation.py` checks it against the workflows.

## In one paragraph

A hook in each Claude Code session reads the session's transcript, keeps the token counts of the model calls made from this repository, and holds them in the repository's git directory. Just before the agent commits, it writes the waiting counts into a new ledger file and stages it, so the agent's own commit carries it. When the pull request merges, a GitHub Actions workflow reads the ledger files that the merge added, prices them from the dated price table at the tool's own commit, adds the CI minutes of the pull request's own commits from GitHub's jobs API, and posts one comment. The ledger stays in the repository as the record.

## Parts

| Part | Where it runs | Reads | Writes |
|---|---|---|---|
| Capture hook, one standard-library Python file | The machine running the Claude Code session | The session's and its subagents' transcripts; the hook's input from Claude Code; `.pr-cost.json` in the working tree; `pr-cost.capture` in the person's global git configuration; the repository's git state | Its store in the git common directory; one ledger file per commit under `.pr-cost/ledger/`, staged; nothing else |
| Store | Inside the repository's git common directory (`git rev-parse --git-common-dir`), outside the working tree and shared by its worktrees | Written and read by the hook only | Never committed |
| Ledger files | `.pr-cost/ledger/<YYYY-MM>/<random>.jsonl`, committed with the agent's work | Counts per call, never content | Written once, never changed |
| Configuration | `.pr-cost.json` at the repository root | `enabled` | Changed only by a pull request |
| Price table | `prices/models.json` and `prices/github-actions.json`, at the tool's commit | Dated rates, modifiers and the source of each | A new row per price change, by pull request |
| Report, a reusable workflow and its Python code | A GitHub Actions runner, on the push a merge makes to the default branch | The push event; as git blobs: the ledger files and `.pr-cost.json` before and after the merge, the ledger files of the default branch's first-parent history before it, and the hook file at the merged commit and at its own commit; the price table; GitHub's API | One comment on the merged pull request; its job summary |
| Release workflow | A GitHub Actions runner, on a pushed tag `vMAJOR.MINOR.PATCH` | `pyproject.toml`, `CHANGELOG.md`, the tag's commit | A GitHub release with a CycloneDX bill of materials |

## Inputs and outputs

**Inputs:**

- Claude Code's transcript lines, one JSON object per line: each assistant message's model, `usage` block (input, output, cache-write by lifetime, cache-read tokens), service tier, speed, inference region, server-side tool requests, the tools it called, and the working directory.
- Claude Code's hook input: the hook event, the transcript's path, `cwd`, and for Bash commands the command's text and `tool_use_id`.
- `.pr-cost.json` and the person's `pr-cost.capture` setting.
- The price table at the tool's own commit.
- GitHub: the push event, the pull request that a commit belongs to, the workflow runs and job attempts on the pull request's own commits, and the report's own earlier comment.

**Outputs:**

- Ledger lines: UTC day, model, a SHA-256 hash of the message id in a field whose name ends in `_id`, main agent or subagent, the token counts, the price attributes, and the activity type. Counts of refused calls, of calls read without a stop reason, and of calls with a usage field that capture does not know.
- One comment per merged pull request, and the report's job summary.
- A GitHub release per version tag, with its bill of materials.

## How a cost is computed

For each ledger entry counted, on the entry's UTC day *d*:

```
token cost = input × rate(model, input, d)
           + output × rate(model, output, d)
           + cache write 5 min × rate(model, cache write 5 min, d)
           + cache write 1 h × rate(model, cache write 1 h, d)
           + cache read × rate(model, cache read, d)
           + server-side tool requests × rate(model, request type, d)
```

`rate` is the latest row in `prices/models.json` dated on or before *d*, with every modifier that the table lists for the entry's attributes, combined as the table states: long-prompt rates, where a prompt's length is its input, cache-write and cache-read tokens together; the inference region's multiplier; and the rates for speed and service tier. Where the transcript gave no cache lifetime, the cost is a range between the two lifetimes' rates. An entry whose model, attribute or day has no price is counted in tokens and left out of the cost, and the comment names it.

For each attempt of each job of each counted run:

```
CI cost = ceil(duration in seconds / 60) × rate(runner type, day the job ran)
```

The runs counted are those on the pull request's own commits that no push to the default branch started and that were created before the merge. A job on a runner that `prices/github-actions.json` does not list is counted in minutes and left out of the cost.

```
total = Σ token cost + Σ CI cost
```

The comment splits the token cost by model, by token type and by activity type. Every figure can be recomputed from the ledger, the price table and the jobs API.

## Flows

### Overview

```mermaid
flowchart LR
  subgraph machine["Session's machine"]
    T[Transcripts] --> H[Capture hook]
    H --> S[(Store in the git directory)]
    S -->|before git commit| L[New ledger file, staged]
  end
  L -->|the agent's commit and push| PR[Pull request branch]
  subgraph github["GitHub"]
    PR -->|merge| M[Default branch]
    M -->|push event| R[Report workflow]
    P[Price table at the tool's commit] --> R
    A[REST API: pull requests, runs, jobs] --> R
    R -->|one comment| C[Merged pull request]
  end
```

### Capture during a session

```mermaid
sequenceDiagram
  participant CC as Claude Code
  participant H as Capture hook
  participant G as git directory
  CC->>H: Stop, SubagentStop, StopFailure or SessionEnd, with the transcript path and cwd
  H->>H: Check .pr-cost.json and the person's pr-cost.capture, before starting any program
  H->>G: Note in the store whether this run found both on
  alt either is off
    H->>G: Take back or put back what the store notes; record nothing
  end
  H->>H: Read the transcripts on from where the last run stopped, up to the time budget
  H->>H: Keep calls whose working directory is in this repository, that are over, and that were made while both switches were on
  H->>G: Record each new call once, by the hash of its message id, with its worktree and branch
  H-->>CC: Exit 0, print nothing
```

### A commit

```mermaid
sequenceDiagram
  participant CC as Claude Code
  participant H as Capture hook
  participant W as Worktree and index
  CC->>H: PreToolUse for a Bash command matching Bash(git *)
  H->>H: Record calls that are over, as in capture
  alt the command is a git commit whose branch and contents the hook can tell
    H->>W: Write .pr-cost/ledger/YYYY-MM/random.jsonl and stage it alone
  else anything else
    H->>H: Stage nothing; the calls wait
  end
  CC->>W: Run the command
  CC->>H: PostToolUse or PostToolUseFailure
  alt the checked-out commit holds the file
    H->>H: Note its calls as taken
  else no commit took it
    H->>W: Take the file back; the calls wait for a later commit
  end
```

### A commit that never ran

```mermaid
flowchart TD
  A[Ledger file staged for a command] --> B{Did a post-tool run follow?}
  B -->|yes| C[That run keeps or takes back the file]
  B -->|no: refused, blocked, cancelled or interrupted| D[Any later run in the repository]
  D --> E{Is the command over? Its result, a later call, its agent stopped, or its session ended}
  E -->|yes| F[Take the file back, unless a commit holds it]
  E -->|no| G[Leave it for a later run]
```

### A merge and its report

```mermaid
sequenceDiagram
  participant GH as GitHub
  participant R as Report
  GH->>R: Push to the default branch, made by a merge
  R->>R: Refuse any other event
  R->>R: Check out the tool's own code at job.workflow_sha, without keeping the token
  R->>GH: List pull requests associated with each commit the push adds
  alt the commits belong to exactly one pull request
    R->>R: Read .pr-cost.json before and after; stop if both turn the tool off
    R->>R: Fetch the default branch's history and refs/pull/<n>/head
    R->>R: Read the ledger files the merge adds, as git blobs, within the size bound, holding each line to the ledger format
    R->>R: Read the call ids of the first-parent history's earlier ledger files, so no call counts twice
    R->>R: Compare the hook file at the merged commit with the one at its own commit
    R->>GH: List runs and every job attempt on the pull request's own commits
    R->>R: Price tokens and minutes from the price table
    R->>GH: Post the comment, or update the report's own earlier one
  else none, more than one, or more commits than the call budget allows
    R->>R: Say why, and how many earlier ledger files the push removed or changed, in the job summary; post no comment
  end
```

### A price update

```mermaid
flowchart LR
  A[Anthropic or GitHub publishes a new price] --> B[Pull request adds a row dated after the existing ones]
  B --> C[Review and CI]
  C --> D[Merge]
  D --> E[Next release names the commit]
  E --> F[Adopters update the hook and the workflow pin together]
```

### A release

```mermaid
flowchart TD
  A[Owner pushes tag vMAJOR.MINOR.PATCH] --> Q{Do the tests pass at the tagged commit on the oldest and newest Python, with every expected failure run as an ordinary test?}
  Q -->|no| X[Refuse, publishing nothing]
  Q -->|yes| T{Is the tag v and a semantic version?}
  T -->|no| X
  T -->|yes| B{Is its commit in the default branch's first-parent history?}
  B -->|no| X
  B -->|yes| C{Tag matches pyproject.toml and CHANGELOG.md?}
  C -->|no| X
  C -->|yes| S{Surface manifest changed, or a breaking change listed, without a raised major number and a Breaking section?}
  S -->|yes| X
  S -->|no| D[Write the CycloneDX bill of materials from the tagged tree]
  D -->|fails, misses an action, or a checksum differs| X
  D --> P{Private-reference check on the bill and the release text}
  P -->|match| X
  P -->|clean| E[Publish the GitHub release naming the commit, with the changelog entry and the bill of materials]
```

## Credentials and permissions

**On the session's machine:** none. The hook uses no token, no key and no account. It reads the person's global git configuration for `pr-cost.capture`, and the repository's configuration only to see capture turned off there. It writes only its store inside the git common directory and the ledger file it stages, and touches the index only to stage, take back or put back that one file.

**The report's workflow**, as an adopter calls it, uses the workflow's own `GITHUB_TOKEN` and no other secret. Its caller grants it exactly:

- `contents: read`, to read the ledger files, `.pr-cost.json` and the pull request's commits from git;
- `actions: read`, to list the workflow runs and job attempts on those commits;
- `pull-requests: write`, to post and update its one comment.

It needs no `contents: write`, so a ruleset protecting the default branch needs no exception for it.

**The release workflow**, in this repository only, holds `contents: write` in its release job alone, to create the release and attach the bill of materials, and runs only for a pushed tag.

**This repository's CI** (`.github/workflows/ci.yml`) grants every job `contents: read` and nothing else. Its checkouts keep no credentials, and no job reads a secret. The job that runs the tests clones the whole history rather than one commit, so that the decision records' check can compare the records with what the default branch held before the change. The workflow names that commit in `BASE_COMMIT`: the pull request's base commit, or the commit that a push to the default branch replaced. The check also compares with where HEAD left the default branch, since a pull request's base is the branch that its author chose, and a pull request's run starts again when its base changes, and so when its title or description is edited, since GitHub reports these as one event. The repository is public, so the whole history gives the job nothing that it could not already read.

Each job of each workflow in this repository, with the permissions it is granted. `tests/test_documentation.py` fails when a job is granted anything this table does not give it, or the table gives a job something it is not granted:

| Workflow | Job | Permissions |
|---|---|---|
| `ci.yml` | `python` | `contents: read` |
| `ci.yml` | `openspec` | `contents: read` |
| `ci.yml` | `vendor` | `contents: read` |
| `ci.yml` | `ci` | `contents: read` |

## Connections to the outside world

| From | To | Protocol | Why | Credential |
|---|---|---|---|---|
| Capture hook | Nothing | None | The hook opens no network connection. | None |
| Report | GitHub's REST API, at the host in `GITHUB_API_URL` (`api.github.com` on github.com) | HTTPS | Find the merged pull request, list its runs and jobs, post or update its comment | `GITHUB_TOKEN` |
| Report | GitHub, by git, through `actions/checkout` and `git fetch` | HTTPS | Fetch the tool's own code at its commit, and the adopter's repository to read as data: the default branch's history up to the push's commit and the pull request's head as `refs/pull/<number>/head` | `GITHUB_TOKEN` |
| Release workflow | GitHub's REST API | HTTPS | Create the release and upload the bill of materials | `GITHUB_TOKEN` |

Prices are never fetched: the price table is a file at the tool's commit, changed only by a pull request.

**Developing this repository** also connects to these, none of which ships to adopters:

| From | To | Protocol | Why |
|---|---|---|---|
| CI and cloud sessions | `actions/checkout`, `actions/setup-python` and `actions/setup-node` from GitHub, each pinned to a full commit | HTTPS | Check out the code and install Python and Node on the runner |
| CI and cloud sessions | The Python Package Index | HTTPS | Install the pinned development tools in `requirements-dev.txt` |
| CI and cloud sessions | The npm registry | HTTPS | Install the pinned OpenSpec CLI from `package-lock.json` |
| CI | `github.com/obra/superpowers` | HTTPS, git | Check that `vendor/superpowers/` matches the commit that `UPSTREAM.lock` pins |

## Environment variables

As designed, the hook reads `CLAUDE_PROJECT_DIR`, `HOME`, `XDG_CONFIG_HOME` and `PATH`, and on Windows `HOMEDRIVE`, `HOMEPATH` and `USERPROFILE`. It sets `GIT_NO_LAZY_FETCH=1` and `GIT_TERMINAL_PROMPT=0` for every git command it runs, so that git fetches nothing and asks for no credentials. It ignores the variables that point git at other configuration files or add settings, and reads each run's time from the system's clock in UTC, which no variable sets. The report reads `GITHUB_API_URL`, `GITHUB_TOKEN` and the event that GitHub passes the workflow. Task 5.3 checks this list against the code once it exists.

## What it never does

- Record or publish a prompt, a response, code, a file's contents, a tool's name, a path, a branch name, a user name, a session identifier or a time of day.
- Record the usage of anyone who has not turned capture on for themselves. For them, the store in their own git directory notes only that a run found capture off, and nothing in it leaves that directory.
- Send anything from the session's machine anywhere. The ledger leaves the machine only in the person's own commits, when they push.
- Run, import or install anything from the pull request it reports on.
- Write to the repository, beyond the ledger file staged for the agent's own commit.
- Fetch prices, or contact any service other than GitHub.
