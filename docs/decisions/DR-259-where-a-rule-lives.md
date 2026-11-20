# DR-259: Each rule lives in the root `CLAUDE.md` or in the folder file of the folder where its work happens

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-19
- **Requirements:** R127, R228, R254
- **Threats:** T74, T223, T227, T228, T235
- **Replaces:** none
- **Closed by:** none

## Context

Backlog item B-003 asks for a shorter `CLAUDE.md`, with rules that load only for the files that they concern. On 2026-11-19 the owner asked for the root `CLAUDE.md` to hold only the essentials and to point to files in the folders below it for the rest, each following the same principles within its folder, and for reviewers without the project's memory to test what can move without a loss. Claude Code loads a folder's `CLAUDE.md` as project instructions when a file in that folder is opened, though not for every way of reaching a file, so that a rule placed there is in front of an agent for much of the work in that folder and absent elsewhere (A5). The reviews at design found three ways in which a split loses a rule: a rule that governs work outside its folder, such as that a check which examined nothing fails, is absent from that work (T223); a sentence by which the root wins wherever a folder file differs from it voids what the folder file tightens, since every such rule differs from the root (T228); and a limit on the root's length that a test holds, while no rule that steers says what may leave the root, pushes the next needed rule out (T227).

## Decision

A rule stays in the root `CLAUDE.md` if it applies to work in more than one folder or to every task, if breaking it does harm before a check or the owner's review can catch it, or if a test or a record ties it there. Any other rule goes to the `CLAUDE.md` of the folder where its work happens. Two folder files hold such rules: `docs/CLAUDE.md` holds how records are written and closed, the threat model's working rules, the pages that a change updates, the clauses that wait for a change of their own, and how a principle of the guide changes, and `tests/CLAUDE.md` holds the depth of testing.

A folder file adds rules for work on files in its folder, or makes the root's stricter there, and never loosens the root: where one would, the root wins, and the agent tells the owner. Each folder file names the tool on its first line, and says this, with the guide's rank, before its first section (R254). Unless a folder file's text is in front of the agent, the agent reads it before it changes, creates or reviews a file in that folder, and gives it to each review of such a file, so that the root asks for the rules to be present rather than describing when Claude Code loads them, which changes between its releases (T235). The root's last section states this rule, and moving a rule out of the root is among the steps that need the owner's words in the agent's session.

The checks that read the context files read the folder files too. R127's check of the records that a file names reads `tests/CLAUDE.md`, while it still skips the rest of `tests/` (T74), and R228 lets a pull request that changes a principle of the guide change any context file, since the rules on testing, which rest on the guide's concern Testing, are in `tests/CLAUDE.md`.

## Alternatives

- One `CLAUDE.md`, shortened: the owner asked for the rules of one folder's work to load only for that work, and a single file keeps every folder's rules in front of every task, at more than the 100 lines that the owner aims for.
- Rules files under `.claude/rules/`, which load for the paths that they name: they load as folder files do, and one kind of file is simpler to test (R252).
- A folder file for `openspec/`: what a spec's writer needs applies across tasks and stays in the root, so that file would only repeat it.
- The rule held by this record alone: a record describes and never instructs, so the rule would steer nothing, and the next change that met the limits on length would move a rule out to pass them (T227).
- The root winning wherever a folder file differs from it: every rule of a folder file differs from the root, so the root's looser words would void each.

## Consequences

- The rules that the root held before this change and that no context file holds now, and what holds each:
  - the licence's name, which the README and `LICENSE` give;
  - that the tool uses no feature that the oldest supported Python lacks, held by CI's tests on Python 3.11, by ruff's and mypy's settings for that version, and by DR-025;
  - that a major dependency update waits for the owner while minor and patch updates and vulnerability fixes go ahead, held by Renovate's configuration, DR-028 and DR-111, and by the root's rule that an agent never approves an item on the dependency dashboard;
  - that versions are semantic and each release is made from a tag with a bill of materials, held by `releases-and-compatibility`, DR-096, DR-097 and DR-148, with tags and releases the owner's under the root's rule;
  - that OpenSpec's Node packages and the scripts and configuration that develop and check the tool are for development only, held by DR-024;
  - which OpenSpec command creates, explores or revises a change, held by the skills themselves, which the root has an agent use;
  - that nothing merges because an AI reported success, held by the root's rule that an agent never merges a pull request, and by DR-080;
  - that backlog item B-022 brought the pages that it swept to the rule that the specs are the single source, held by that item, which the default branch gives as Done, and by its mapping.
- A rule that moved to a folder file holds there as it held in the root, and an older text that places it in `CLAUDE.md` reads as DR-258 says.
- The threats whose rules moved cite the folder file in their answers.
- Each review lane's brief names the folder files of the folders that its diff touches, and the pull request that brings in the context files maps each rule that left the root to the check or the review that catches a breach of it.

## Scope

This covers where a rule of the context files lives. Which files steer is DR-258 (Only the context files and the files that the root lists steer work here, and everything else describes), the limits on the files' lengths are DR-260 (The root `CLAUDE.md` puts what does harm first, within 60 lines, and holds at most 200 lines), and how their lines are counted is DR-261 (The context files are wrapped at 100 characters, so that their lines are the lines that the limits count).

## What reversing it would change

How hard it is to reverse: reversible. Moving the folder files' rules back into the root is a change to three files and to the checks that read them, R127's and R228's among them, with the answers of T74, T223, T227, T228 and T235 and of the threats whose answers cite a folder file, and the root would pass the length that DR-260 holds it to.
