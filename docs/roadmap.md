# Roadmap

What is being built now, what comes next and what is left for later, with what the tool knowingly does not do. The roadmap describes: an item here is not a promise, and it is not a request to start the work. Issues and pull requests are named by number. This page changes in the same pull request as the work that finishes, adds or moves one of its items.

## Now

The tool has no code yet. Its design, the change `add-pr-cost-calculator`, whose [proposal](../openspec/changes/add-pr-cost-calculator/proposal.md) says what it builds, is being made ready for the build by a series of pull requests, in this order:

- **Patterns and anti-patterns.** A page that lists each recognised pattern that the design follows and each anti-pattern that it avoids or knowingly accepts, from an assessment by reviewers of their own, with each anti-pattern found fixed before the build.
- **A risk register.** Each threat rated as if its answer were not built, beside its rating with the answer in place, on a page generated from the threat model, and a further answer for every high or critical risk.
- **Context files and the rules agents follow.** Rules that load only for the files they concern, a shorter `CLAUDE.md`, and rules on how reviews are reported and how files are staged.
- **Two new fields on every record.** Each decision record says which way its boundary faces and how hard it is to reverse.
- **Conventions.** Printable ASCII in everything the project writes, diagrams as code, and naming conventions, each checked in CI.
- **Scope and visual documentation.** Records on what the project takes from elsewhere, a section of the page on how the tool works that lists everything incoming and outgoing, and diagrams in the README and the feature pages.
- **The tool's requirements, corrected before the build.** The design's fixes from the pages above, how the comment shows a cost, with no dollar sign and no tilde outside inline code in the comment or its job summary, so that GitHub shows no amount as a formula or struck through, as issue 18 asks (R21, R97), the prices' rules, and the open points that earlier reviews left.

Then the build itself, in pull requests of its own, by the sections of the change's tasks: verification first, the capture step, pricing, the report, review, releases and compatibility, and integration, in which the tool reports the cost of its own pull requests.

## Next

What follows the first build. Each item says what it rests on.

- **Planned.** A command that lists pull requests' costs and writes each one as a small Markdown file in a folder that the adopter chooses, which reaches the repository through an ordinary pull request, while the report itself still writes nothing (DR-222, DR-016).
- **Planned.** A report that can be run before a pull request merges and shows it as still in progress, where the first version reports only at the merge (DR-223, DR-005).
- **Planned.** Every reader of the specs finds them at any depth, as the test of the specs' form does: issue 19 (R177, T124).
- **Planned.** CI keeps the rewording script's output, so that no one pastes a long output into comments: issue 16 (T94).
- **Planned.** A check, on Windows, of whether a project's Claude Code settings can set the variables that name the home folder, from which the opt-in is read: issue 15 (DR-183, T119).
- **Planned.** A decision on when the marketplace moves to a new major release, so that repositories can move their pins first: issue 23 (DR-204, DR-208).
- **Open to feedback and contributions.** A ledger line whose model the report's price table does not list counted under `unknown`, in tokens and not in cost, instead of being refused: issue 24 (DR-208, T136).

## Later

Work on an item here starts with an issue on which the owner agrees, and some items need a spec, a threat review and the owner's decision first.

- **Planned.** The cost of AI review by an app or a job in CI, which the first version leaves out (DR-004).
- **Open to feedback and contributions.** An organization mode, in which an organization turns its members' capture on and they cannot turn it off. Nothing in the first version rules it out (DR-189).
- **Open to feedback and contributions.** Agents other than Claude Code, such as Gemini or Codex (DR-003).
- **Open to feedback and contributions.** Commands sent through Claude Code's PowerShell tool, which capture does not see (DR-007).
- **Open to feedback and contributions.** GitHub Enterprise Server (DR-006).
- **Open to feedback and contributions.** Repository and CI services other than GitHub, such as GitLab or Gitea (DR-160).

## Known limitations

This is a short list. It gives the limitations of the design that an adopter notices, each with what it means for the figure or for the person. Each feature page lists the rest of its own: [activity types](features/activity-types.md#known-limitations-and-the-roadmap), [CI minutes](features/ci-minutes.md#known-limitations-and-the-roadmap), [the ledger](features/ledger.md#known-limitations-and-the-roadmap), [pricing](features/pricing.md#known-limitations-and-the-roadmap), [project standards](features/project-standards.md#known-limitations-and-the-roadmap), [releases and compatibility](features/releases-and-compatibility.md#known-limitations-and-the-roadmap), [the report comment](features/report-comment.md#known-limitations-and-the-roadmap), [the switch and the opt-in](features/switch-and-opt-in.md#known-limitations-and-the-roadmap) and [usage capture](features/usage-capture.md#known-limitations-and-the-roadmap).

- **Claude Code makes model calls for its own tools, such as WebFetch, that the session's transcript does not hold**: those calls are not counted, so the figure is lower than what the session used.
- **Some calls reach no commit**: calls made after the agent's last commit on a branch, such as pushing and opening the pull request, calls on a branch that gets no later commit, and calls made while no branch is checked out, as during a rebase stopped at a conflict, are in no pull request's figure, and so are calls that wait for a commit that capture does not stage for, such as a `git merge`.
- **A session works from a folder that contains the repository**: its calls are left out, and the comment says that the figure is a lower bound. A project's cloud thread starts in such a folder, so its figure can be far too low.
- **A session whose current directory is in the repository also works on another one, through paths or with a `cd` inside a command**: those calls are recorded and published in this repository, so work on other repositories, private ones above all, belongs in sessions of its own.
- **A pull request is based on another one that was merged by squashing or rebasing**: the later pull request counts the earlier one's CI runs again, unless it is rebased first.
- **A workflow merges a pull request with `GITHUB_TOKEN`**: GitHub starts no workflow for that merge, so the pull request gets no report.
- **A person turns capture on during a session, a session gets no start run, or its first prompt is written before its start run notes its time**: the calls before capture first finds both switches on are left out, such as a session's first turn.
- **A project's cloud thread continues on a machine that cannot be resumed**: the calls that waited for a commit are lost, so committing as the work goes keeps them.
- **With the plugin, one opt-in reaches every repository that turns the tool on where Claude works or commits**: each repository that turns the tool on records the calls made from it, shown in the diff of a commit there, though a thread can commit and push with no one reading that diff.
- **An organization's shared environment, its default environment or its managed settings opt in its members**: a member's usage is published wherever they work in that environment, so the organization tells its members first.
- **A release reaches everyone who added the marketplace, once their account syncs it, with nothing to accept**: a release reaches those people's sessions without a step of theirs, so the README gives the zip first.
- **The account or the repository that serves the marketplace is renamed, and someone else takes the old name**: people who added the marketplace by its old address could get another plugin of the same name.

## Known bugs

None yet, since the tool has no code. Once it has, this section names, by number, the issues that the bug form opens.
