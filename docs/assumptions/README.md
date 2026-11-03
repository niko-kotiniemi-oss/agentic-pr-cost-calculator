# Assumptions

What the specs, the design, the [threat model](../threat-model.md) and the decision records assume about what lies outside the tool's own code: Claude Code, GitHub, git, Python, the development tools of this repository, the prices that the tool applies, and the adopters and people who use and keep the tool. A page per subject holds each assumption in full: what rests on it, by requirement, threat and record ID, what would change if it were wrong, and its facts, each with where it is relied on and how it is checked. A threat that rests on an assumption names it in its field `Assumptions`, and the assumption names the threat. `tests/test_assumptions.py` checks that each citation resolves, that each check takes one of the forms below, and the order of the list.

These pages describe and never steer: where one differs from `CLAUDE.md` or a spec, `CLAUDE.md` or the spec holds.

A fact is checked in one of four ways:

- `tested`: a test that pytest collects, and that no mark skips or expects to fail, holds it, named as `` `tests/<file>.py::<name>` ``.
- `observed`: a file under `tests/` holds such a test, which reproduces what was seen, and the fact gives that file, the date, and the program, the version that it prints and its build.
- `documented`: the vendor's documentation says it. The fact links each page by its address, on a documentation host that the test lists or as a file at a full commit of a GitHub repository that it lists, and gives the day the pages were read. No page gives a web address anywhere else.
- `not yet`: nothing checks it yet, and the fact names the task, still to be done, that will, or says why none will.

Tests never use the network (DR-090), so no test may reach Claude Code, GitHub, a vendor's prices, or adopters and people, and a fact about them is never `tested` alone. Such a fact may name, beside its check, the test that holds the tool's handling of it.

The list puts first the assumptions behind the threats of highest impact, then, among those, the least checked, an assumption being as checked as its least checked fact, from `not yet` through `documented` and `observed` to `tested`, then those behind the highest risk. The assumptions that no threat rests on come last, and each page keeps the list's order within each of its sections. Impact and risk are read from the threat model, so a changed rating or check changes the order. A risk below is rated with the assumption true, since the threat model rates each threat with its answer in place (DR-112).

## The assumptions, most at stake first

- **A1.** Claude Code keeps each session's transcript where the capture step can read it while the session lasts. Impact 3, risk 6. Page: [Claude Code](claude-code.md).
- **A2.** A transcript line gives its call's model, usage, time and current directory, in fields whose meaning stays put. Impact 3, risk 6. Page: [Claude Code](claude-code.md).
- **A3.** Hooks get enough time to finish, and every adopter's Claude Code has the hook events and the condition that the tool registers. Impact 3, risk 6. Page: [Claude Code](claude-code.md).
- **A4.** A hook's input gives the directories, the paths and the command text that capture needs, and a hook that exits with success and prints nothing steers nothing. Impact 3, risk 6. Page: [Claude Code](claude-code.md).
- **A5.** What a session loads comes from its settings and the branch it starts on, and a project's settings cannot set `HOME` or the `XDG_*` variables. Impact 3, risk 6. Page: [Claude Code](claude-code.md).
- **A6.** The agent runs git in forms that capture recognises, and acts on GitHub as the owner's own account. Impact 3, risk 6. Page: [Claude Code](claude-code.md).
- **A7.** The repository's settings on GitHub are applied, and stay applied, as the threat model's section on the settings the owner keeps lists them. Impact 3, risk 6. Page: [GitHub](github.md).
- **A8.** Workflows and required checks run when the design expects them to. Impact 3, risk 6. Page: [GitHub](github.md).
- **A9.** GitHub shows text as the checks expect, and text posted on GitHub is public at once. Impact 3, risk 6. Page: [GitHub](github.md).
- **A10.** A repository's worktrees share one git common directory, which recording can use. Impact 3, risk 6. Page: [git](git.md).
- **A11.** git 2.43 stands for every later git. Impact 3, risk 6. Page: [git](git.md).
- **A12.** History, refs and tags behave as the checks expect. Impact 3, risk 6. Page: [git](git.md).
- **A13.** Adopters' git setup leaves the ledger alone. Impact 3, risk 6. Page: [Adopters and people](adopters-and-people.md).
- **A14.** People who opt in know what it publishes, and keep other work apart. Impact 3, risk 6. Page: [Adopters and people](adopters-and-people.md).
- **A15.** The owner merges, reads every diff and keeps the settings. Impact 3, risk 6. Page: [Adopters and people](adopters-and-people.md).
- **A16.** Agents follow the repository's rules. Impact 3, risk 6. Page: [Adopters and people](adopters-and-people.md).
- **A17.** People report bugs and vulnerabilities through the right channel. Impact 3, risk 6. Page: [Adopters and people](adopters-and-people.md).
- **A54.** The clock of the machine that runs a session agrees with its transcripts and with the runner's day. Impact 3, risk 6. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A18.** A merge into the default branch makes one push, and that push starts the adopter's calling workflow. Impact 3, risk 4. Page: [GitHub](github.md).
- **A19.** A reusable workflow runs with its caller's context, and with only the token and the secrets that its caller gives it. Impact 3, risk 4. Page: [GitHub](github.md).
- **A20.** Checkouts and GitHub's hosted runners are what the workflows expect. Impact 3, risk 4. Page: [GitHub](github.md).
- **A21.** The git commands that the step runs start no program that the step did not choose, apart from those that git's configuration names. Impact 3, risk 4. Page: [git](git.md).
- **A22.** The test tools can do what the testing decision records ask of them. Impact 3, risk 4. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A23.** Adopters pin released commits, and update the hook and the pin together. Impact 3, risk 4. Page: [Adopters and people](adopters-and-people.md).
- **A24.** The machine running a session, and the programs that a hook starts on it, are the person's own. Impact 3, risk 4. Page: [Adopters and people](adopters-and-people.md).
- **A57.** The reviews and the planned tests get done. Impact 3, risk 4. Page: [Adopters and people](adopters-and-people.md).
- **A33.** Model names and list prices mean what the report says they mean. Impact 3, risk 4. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A25.** Claude Code keeps the hook registrations it read at session start. Impact 3, risk 3. Page: [Claude Code](claude-code.md).
- **A26.** Runs for a pull request from a fork get no secrets, and run the code that its author chose. Impact 3, risk 3. Page: [GitHub](github.md).
- **A27.** Tags and releases can be protected from change. Impact 3, risk 3. Page: [GitHub](github.md).
- **A28.** GitHub, and this repository's place on it, stay as they are. Impact 3, risk 3. Page: [GitHub](github.md).
- **A29.** Python's isolated mode and its start-up behave as the hook expects. Impact 3, risk 3. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A30.** Renovate proposes updates as it is configured to, and its wait catches bad releases. Impact 3, risk 3. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A31.** Upstream releases and lock files are what they claim to be. Impact 3, risk 3. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A32.** OpenSpec behaves as the checks expect. Impact 3, risk 3. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A34.** Maintainers review a pull request without checking out its branch where a session runs. Impact 3, risk 3. Page: [Adopters and people](adopters-and-people.md).
- **A35.** GitHub enforces the permissions a workflow declares, gives runs from forks a read-only token, and gives a reusable workflow its caller's event, as its documentation says. Impact 3, risk 3. Page: [GitHub](github.md).
- **A36.** Claude Code writes a call as lines that share one message id, with the call's final usage on each line that gives its stop reason. Impact 2, risk 6. Page: [Claude Code](claude-code.md).
- **A37.** Claude Code only appends whole lines to a transcript, soon after each call. Impact 2, risk 6. Page: [Claude Code](claude-code.md).
- **A38.** A subagent's calls are in a transcript of their own, and the transcripts leave out only the calls that Claude Code makes for its own tools. Impact 2, risk 6. Page: [Claude Code](claude-code.md).
- **A39.** Claude Code's hooks behave as its documentation describes. Impact 2, risk 6. Page: [Claude Code](claude-code.md).
- **A40.** The options of `git commit` mean what capture takes them to mean. Impact 2, risk 6. Page: [git](git.md).
- **A41.** Only the attributes and settings that capture knows change what git commits of a ledger file. Impact 2, risk 6. Page: [git](git.md).
- **A42.** git's index lock and staging behave as the design expects. Impact 2, risk 6. Page: [git](git.md).
- **A43.** Sparse checkouts behave in git 2.43 as the design describes them. Impact 2, risk 6. Page: [git](git.md).
- **A44.** Teams want each pull request's cost, and read it as an estimate. Impact 2, risk 6. Page: [Adopters and people](adopters-and-people.md).
- **A45.** Adopters merge into the default branch by hand, after CI, having read the diff, and never rewrite that branch's history. Impact 2, risk 6. Page: [Adopters and people](adopters-and-people.md).
- **A46.** Sessions commit through Bash, and little else changes the branch while a session works. Impact 2, risk 6. Page: [Adopters and people](adopters-and-people.md).
- **A47.** Ledger files stay small, and their commits are rarely undone. Impact 2, risk 6. Page: [Adopters and people](adopters-and-people.md).
- **A48.** A pull request's commits stay findable after every merge method. Impact 2, risk 4. Page: [GitHub](github.md).
- **A49.** GitHub's lookup of the pull requests associated with a commit behaves as documented: for a commit on the default branch, it gives the merged pull request that introduced the commit. Impact 2, risk 4. Page: [GitHub](github.md).
- **A50.** GitHub's runs and jobs API gives complete, timed listings, within known limits. Impact 2, risk 4. Page: [GitHub](github.md).
- **A51.** git reads a person's configuration from the files that the step reads, by the rules that the step re-implements. Impact 2, risk 4. Page: [git](git.md).
- **A52.** Python's JSON reader and digit matching behave at their edges as the step and the checks expect. Impact 2, risk 4. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A53.** Files, locks and random names behave alike on every system where a repository's git common directory lives. Impact 2, risk 4. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A55.** Anthropic prices each token type at its own rate for each model. Impact 2, risk 4. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A56.** Only the facts that the ledger records set a call's price, and prices change rarely and from a given day. Impact 2, risk 4. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A58.** Someone reads the report comments and job summaries, and keeps the prices current. Impact 2, risk 4. Page: [Adopters and people](adopters-and-people.md).
- **A64.** GitHub bills job minutes from job times. Impact 2, risk 4. Page: [GitHub](github.md).
- **A59.** The development tools support Python 3.11, and report code that needs a newer Python. Impact 2, risk 2. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A60.** Adopters' machines and runners meet the floors, and their policies allow the workflow. Impact 2, risk 2. Page: [Adopters and people](adopters-and-people.md).
- **A61.** A session that starts in a repository's folder runs the hooks that the repository's settings register, once the folder is trusted, unless it is a cloud thread of a project or a cloud session with several repositories. Impact 2, risk 6. Page: [Claude Code](claude-code.md).
- **A62.** A repository opened in Claude Code can already run any hook its own settings register, including one that changes a person's git configuration. Impact 2, risk 4. Page: [Claude Code](claude-code.md).
- **A63.** git can be kept offline and from asking for credentials. Impact 2, risk 4. Page: [git](git.md).
- **A65.** Telemetry stays off where its switches say. Impact 1, risk 2. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A66.** Later Pythons keep what the tool uses, on every system that adopters use, and each version gets security fixes until its end of life. No threat. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A67.** The licences allow what is kept here. No threat. Page: [Python, the development tools and prices](python-tools-and-prices.md).
- **A68.** Other agents and review apps will expose their usage later. No threat. Page: [Adopters and people](adopters-and-people.md).

## Retired IDs

IDs are stable: an assumption keeps its ID while it exists, and a new one takes the next free number. An assumption that a later change removes leaves the list above, and its ID is listed here with the change that removed it, never to be used again.

None yet. An entry names the ID and the change that removed it, as in "A7, removed by `change-name`".
