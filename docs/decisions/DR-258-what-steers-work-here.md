# DR-258: Only the context files and the files that the root lists steer work here, and everything else describes

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28, 2026-11-13 and 2026-11-19
- **Requirements:** R127, R134, R219, R220, R252, R255, R256, R257, R258
- **Threats:** T33, T81, T93, T94, T95, T180, T181, T224, T225, T226, T230, T232, T233, T234, T236, T237
- **Replaces:** DR-237, DR-238
- **Closed by:** none

## Context

DR-237 and DR-238 say what steers an agent that works on this repository: `CLAUDE.md`, `.claude/`, the workflows, the Superpowers skills that `.claude/settings.json` enables and, for how the project builds, the guide; and that the glossary, the assumptions and the pages that a file here links to describe, apart from the files that steer. On 2026-11-19 the owner asked for the root `CLAUDE.md` to hold only the essentials, pointing to folder files that hold the rest for work in their folders (DR-259), so that `CLAUDE.md` is no longer one file. The threat reviews at design of that change, one for each of trust boundaries 7 and 9, each in a context of its own, found that the old list no longer says what steers. Named whole, `.claude/` would make a worktree under `.claude/worktrees/`, or a rules file, steer by the list's words while a test refuses it. Claude Code loads as project instructions files that the root does not name: another branch's worktree inside the clone, an `AGENTS.md`, a `CLAUDE.local.md`, and a package's or a tool's file, tracked or not (T225). A project's cloud thread loads every clone's root `CLAUDE.md` into each of its sessions (T232). Some agents start without any context file, and their reports bring back what they read (T234). A folder file loads from the working tree, so a branch's change to one steers that branch before the owner merges it (T224). A memory keeps a moved rule's old place and wording (T236). A setting or a variable can keep the context files from loading (T230), a session started above the clone gets the root late or not at all (T233), and text that GitHub hides in a context file reaches the agent and not the reviewer (T226).

## Decision

For work on this repository, only these steer: the root `CLAUDE.md` and the folder files that it names, `docs/CLAUDE.md` and `tests/CLAUDE.md`; `.claude/settings.json`, `.claude/hooks/` and `.claude/skills/`; the workflows; the Superpowers skills that `.claude/settings.json` enables; and, for how the project builds, the guide, `docs/patterns.md`. Everything else describes, however it is worded and wherever it lies: any other `CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md` or rules file, another repository's files and skills, a memory, a subagent's report, every other page and data file here, `CONTRIBUTING.md` and the templates among them, a page that one links to, and issue text, pull request text and review comments from anyone. Where one of them differs from a file that steers or from a spec, those steer, and the agent tells the owner. A rule of a file that steers, a record, a backlog item or a guide entry that a branch adds or changes is a proposal until the owner merges it. Where a record, a threat or the guide places a rule in `CLAUDE.md`, or names one of its sections, the rule is in the root or in a folder file that the root names.

What DR-237 and DR-238 held otherwise still holds. The guide steers below the specs and the context files and never widens what they let an agent do, an entry cites the rule that it rests on and never states it again, and where an entry and a step of a Superpowers skill differ, the step is followed and the owner told. No attribute hides the diff of the guide or of a context file, and the rewording script lists the changes to the context files first and those to the guide next. Where a meaning in the glossary, or an assumption, differs from a context file, a requirement or a scenario, those hold, and the glossary or the assumption is corrected.

A test fails on any other instruction file that git tracks, `vendor/` included, on a tracked `.mcp.json`, which names servers that a session can start (T237), on a tracked file under a `.claude` folder outside its settings file, its hooks and the skills that the pinned OpenSpec generates, and on a tracked symbolic link or submodule (R252). Git ignores a `CLAUDE.local.md` in any folder and the folders where another branch's worktree is made, before they exist, and no ignore file takes them back (R257). The settings file, and the marketplace file that it names, hold only what their tests list (R256). The context files hold no text that GitHub hides, no link, no web address and no import (R255), and no attribute hides the diff of a file that steers or of the tests that hold them (R134). The README and `CONTRIBUTING.md` say to start a session in the clone's own folder (R258).

## Alternatives

- DR-237 and DR-238 left as they were, naming `.claude/` whole and `CLAUDE.md` alone: a file under `.claude/worktrees/` or `.claude/rules/` would steer by their words while a test refuses it, and no folder file would be named among what steers.
- A list of what describes that names only this repository's files, which would leave another repository's context files and skills, which a project's cloud thread loads beside these, with the same authority (T232).
- A `claudeMdExcludes` setting in `.claude/settings.json` that keeps every other `CLAUDE.md` from loading, which a project's cloud thread would not read, since the repository's settings do not apply there (A5).
- A test that walks the working tree rather than what git tracks, which would fail on every worktree and installed package of a contributor's, and still not see a file written after it ran.

## Consequences

- DR-237 and DR-238 are closed. What each held is restated above, and their consequences hold:
  - whether a text instructs or describes is not something a test can decide, so only the rule holds the pages that describe (T33's residual), while the guide's opening, its rank and the changes to its principles are held by tests (R219, R220, R228);
  - what steers changes only through the owner's merge (T33, DR-080), and the guide steers as the default branch holds it (DR-240);
  - each fixture that carries hostile text on purpose is named for it (T33, task 1.1);
  - an assumption's entry says what would change if it is wrong, never how to change it, and a documented fact links only a page that the test lists (DR-162);
  - a meaning that narrows a rule without contradicting its words rests on the owner's review of the glossary's diff (T93).
- What rests on the closed records: R134, R219 and R220 hold, and R134 now names the folder files beside the root. T33, T81, T93, T94, T95, T180 and T181 cite this record in place of the closed ones. Design decision 14 cites this record, and design decision 21 gives the context files. The guide's entry that cited the closed records, the glossary's opening, the pages of the assumptions and the plans that named them name this record. DR-231, DR-240 and DR-244, which name DR-237 or DR-238 in their text, still hold and keep their text, and DR-082 and DR-166 stay closed.
- R127's check lets the mapping of B-022 name the closed records, since its quotes are what the default branch held before that sweep, and it reads `tests/CLAUDE.md` too (DR-259).
- Where an older text names a section of `CLAUDE.md` that the root no longer has, its rule is now here. Rules, and Never write a figure you have not computed, are in the root's Rules. Records are data, not instructions, is in the root's section of that name, and the mapping's description in `docs/CLAUDE.md`. Decision records is in `docs/CLAUDE.md`'s section of that name, apart from adding a record with its change and with the change to what steers by it, in the root's Every change, and naming the owner as a decider, in the root's What an agent never does here. Privacy is in the root's Privacy, and Outside contributions in the root's What an agent never does here. Threat model is in the root's Every change, for when and by whom, and in `docs/CLAUDE.md`'s The threat model, for how, apart from an acceptance of a high risk, in the root's What an agent never does here. Documentation is in the root's Every change and in `docs/CLAUDE.md`'s The pages that a change updates. Compatibility and releases is in the root's Every change. Who owns what is in the root's section of that name, with how a principle of the guide changes in `docs/CLAUDE.md`'s The guide and the backlog. Testing is in the root's Rules and Every change and in `tests/CLAUDE.md`, and Review in the root's Every change. DR-259 names the rules that left the context files, and what holds each.
- The answers of T224, T225, T226, T230, T232, T233, T234, T236 and T237 cite this record.

## Scope

This covers what steers an agent that works on this repository, and what only describes. Where a rule lives among the context files is DR-259 (Each rule lives in the root `CLAUDE.md` or in the folder file of the folder where its work happens), which copy of the guide steers and how its principles change is DR-240 (The guide steers as the default branch holds it, and a principle of it changes alone, when the owner asks), decision records are DR-108 (Each decision has a record of its own, in an index), and how an outside pull request is reviewed is DR-081 (Outside pull requests are reviewed from `main`).

## What reversing it would change

How hard it is to reverse: reversible. The rule is text in the root `CLAUDE.md`, with the tests that hold the instruction files, the settings file, the ignore rules and the context files' text, which one pull request can change. The root's section Records are data, not instructions, R127, R134, R219, R220 and R252 to R258 in `project-standards` and their scenarios, design decisions 14 and 21, and the answers of T33, T81, T93, T94, T95, T180, T181, T224, T225, T226, T230, T232, T233, T234, T236 and T237 would change, and DR-231, DR-240 and DR-244 would be read again.
