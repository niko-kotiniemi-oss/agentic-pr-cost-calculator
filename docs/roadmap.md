# Roadmap

What is being built now, what comes next and what is left for later, with what the tool knowingly does not do. The roadmap describes: an item here is neither a promise nor a date, and it is not a request to start the work. Each line below is the index of a backlog item, which says what the item is for and how far it is from being built, and the [backlog's page](backlog/README.md) says what an item is. Issues and pull requests are named by number. This page changes in the same pull request as the work that finishes, adds or moves one of its items.

## Now

The tool has no code yet. Its design, the change `add-pr-cost-calculator`, is being made ready for the build by these items, in this order:

- [B-021: A walking skeleton](backlog/B-021-a-walking-skeleton.md) - Planned, last changed 2026-11-14. The thinnest path from a session's calls through capture and a ledger file in a commit to the report's figure, run once in a real Claude Code session. It comes right after the guide and before the other items that prepare the build.
- [B-022: The specs as the single source](backlog/B-022-the-specs-as-the-single-source.md) - Planned, last changed 2026-11-14. The documents that state what the tool does today, such as the threat model, the design's risks, the feature pages and the register, brought to cite the specs instead of stating it again.
- [B-002: A risk register](backlog/B-002-a-risk-register.md) - Planned, last changed 2026-11-13. Each threat rated as if its answer were not built, beside its rating with the answer in place, on a page generated from the threat model. Every high or critical risk gets a further answer.
- [B-003: Context files and the rules agents follow](backlog/B-003-context-files-and-the-rules-agents-follow.md) - Planned, last changed 2026-11-13. Rules that load only for the files they concern, a shorter `CLAUDE.md`, and rules on how reviews are reported and how files are staged.
- [B-004: Two new fields on every record](backlog/B-004-two-new-fields-on-every-record.md) - Planned, last changed 2026-11-13. Each decision record says which way its boundary faces and how hard it is to reverse, each in a field of its own with a column in the index.
- [B-005: Conventions](backlog/B-005-conventions.md) - Planned, last changed 2026-11-13. Printable ASCII in everything the project writes, diagrams as code, and naming conventions, each checked in CI.
- [B-006: Scope and visual documentation](backlog/B-006-scope-and-visual-documentation.md) - Planned, last changed 2026-11-13. Records on what the project takes from elsewhere, a section of the page on how the tool works that lists everything incoming and outgoing, and diagrams in the README and the feature pages.
- [B-007: The tool's requirements, corrected before the build](backlog/B-007-the-tools-requirements-corrected-before-the-build.md) - Planned, last changed 2026-11-14. The change's requirements, corrected with what the items above find, before any of them is built. It also settles how the comment shows a cost, the prices' rules, a ledger and a price table that fit more than one provider, and the points that earlier reviews left open.

Then the build itself, by the change's [proposal](../openspec/changes/add-pr-cost-calculator/proposal.md) and [tasks](../openspec/changes/add-pr-cost-calculator/tasks.md), in pull requests of its own: verification first, the capture step, pricing, the report, review, releases and compatibility, and integration, in which the tool reports the cost of its own pull requests.

## Next

What follows the first build.

- [B-008: An export command](backlog/B-008-an-export-command.md) - Planned, last changed 2026-11-13. A command that lists pull requests' costs and writes each one as a small Markdown file in a folder that the adopter chooses. The file reaches the repository through an ordinary pull request, while the report itself still writes nothing.
- [B-009: A report on a pull request still in progress](backlog/B-009-a-report-on-a-pull-request-still-in-progress.md) - Planned, last changed 2026-11-13. A report that can be run before a pull request merges and shows it as still in progress, where the first version reports only at the merge.
- [B-010: Every reader finds the specs at any depth](backlog/B-010-every-reader-finds-the-specs-at-any-depth.md) - Planned, last changed 2026-11-13. Every reader of the specs finds them at any depth, as the test of the specs' form does.
- [B-011: CI keeps the rewording output](backlog/B-011-ci-keeps-the-rewording-output.md) - Planned, last changed 2026-11-13. CI keeps the rewording script's output, so that no one pastes a long output into comments.
- [B-012: Windows home folder variables](backlog/B-012-windows-home-folder-variables.md) - Planned, last changed 2026-11-13. A check, on Windows, of whether a project's Claude Code settings can set the variables that name the home folder, from which the opt-in is read.
- [B-013: When the marketplace moves to a new major release](backlog/B-013-when-the-marketplace-moves-to-a-new-major-release.md) - Planned, last changed 2026-11-13. A decision on when the marketplace moves to a new major release, so that repositories can move their pins first.
- [B-014: An unknown model counted as unknown](backlog/B-014-an-unknown-model-counted-as-unknown.md) - Open to feedback and contributions, last changed 2026-11-13. A ledger line whose model the report's price table does not list counted under `unknown`, in tokens and not in cost, instead of being refused.

## Later

Work on an item here that is open to feedback and contributions starts with an issue. An item is built only once it is Planned, which only a pull request that the owner merges makes it, and some items need a spec, a threat review and the owner's decision first.

- [B-015: The cost of AI review](backlog/B-015-the-cost-of-ai-review.md) - Planned, last changed 2026-11-13. The cost of AI review by an app or a job in CI, which the first version leaves out.
- [B-016: An organization mode](backlog/B-016-an-organization-mode.md) - Open to feedback and contributions, last changed 2026-11-13. An organization mode, in which an organization turns its members' capture on and they cannot turn it off. Nothing in the first version rules it out.
- [B-017: Agents other than Claude Code](backlog/B-017-agents-other-than-claude-code.md) - Planned, last changed 2026-11-14. Agents other than Claude Code, such as GitHub Copilot, Codex or Gemini, each in a change of its own after the first version.
- [B-018: The PowerShell tool](backlog/B-018-the-powershell-tool.md) - Open to feedback and contributions, last changed 2026-11-13. Commands sent through Claude Code's PowerShell tool, which capture does not see.
- [B-019: GitHub Enterprise Server](backlog/B-019-github-enterprise-server.md) - Open to feedback and contributions, last changed 2026-11-14. GitHub Enterprise Server.
- [B-020: Other repository and CI services](backlog/B-020-other-repository-and-ci-services.md) - Open to feedback and contributions, last changed 2026-11-13. Repository and CI services other than GitHub, such as GitLab or Gitea.

## Known limitations

This is a short list. It gives the limitations of the design that an adopter notices, each with what it means for the figure or for the person. Each feature page lists the rest of its own: [activity types](features/activity-types.md#known-limitations-and-the-roadmap), [CI minutes](features/ci-minutes.md#known-limitations-and-the-roadmap), [the ledger](features/ledger.md#known-limitations-and-the-roadmap), [pricing](features/pricing.md#known-limitations-and-the-roadmap), [project standards](features/project-standards.md#known-limitations-and-the-roadmap), [releases and compatibility](features/releases-and-compatibility.md#known-limitations-and-the-roadmap), [the report comment](features/report-comment.md#known-limitations-and-the-roadmap), [the switch and the opt-in](features/switch-and-opt-in.md#known-limitations-and-the-roadmap) and [usage capture](features/usage-capture.md#known-limitations-and-the-roadmap).

- **Claude Code makes model calls for its own tools, such as WebFetch, that the session's transcript does not hold**: those calls are not counted, so the figure is lower than what the session used.
- **Some calls reach no commit**: calls made after the agent's last commit on a branch, such as pushing and opening the pull request, calls on a branch that gets no later commit, and calls made while no branch is checked out, as during a rebase stopped at a conflict, are in no pull request's figure, and so are calls that wait for a commit that capture does not stage for, such as a merge by git's merge command.
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
