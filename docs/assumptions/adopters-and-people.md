# Adopters and people

The assumptions about the teams that adopt the tool, the people who opt in, and the people who keep this repository: the owner, the agents that work here and its contributors. No test may reach what adopters and people do (DR-090). [The index](README.md) lists every assumption, the most at stake first.

## A13. Adopters' git setup leaves the ledger alone.

- **Rests on it:** R50, R86, T8, T10, T43, DR-034, DR-035, DR-037, DR-129, DR-136
- **If it is wrong:** A git hook that refuses the ledger file would fail the agent's whole commit, and push agents toward `--no-verify` (T43, T10). A filter, an encoding or the sparse index on the ledger path would keep calls from reaching a commit, or let git delete ledger files from the branch (T8, T10).
- **Fact:** Adopters leave `.pr-cost/` out of their own git hooks, such as secret scanners, so that no git hook refuses a ledger file.
  - **Relied on:** T10, T43, DR-035, DR-136
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Secret scanners in adopters' git hooks behave like detect-secrets with its default plugins and filters, which read a hash in a field whose name ends in `_id` as an identifier, not a secret.
  - **Relied on:** T10, T43, DR-136
  - **Checked:** not yet: none will, since no test may reach the scanners that adopters run; `add-pr-cost-calculator` task 1.2 checks detect-secrets alone
- **Fact:** Agents in adopting repositories stop at a failing git hook instead of retrying with `--no-verify` or changing the git hook's configuration.
  - **Relied on:** T10, T43, DR-136
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters give the ledger path no filter, such as Git LFS, and no working-tree encoding, and add a `.pr-cost/** -text` line to `.gitattributes` where git's `core.safecrlf` is on.
  - **Relied on:** R50, R86, T8, DR-034, DR-129
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters keep git's sparse index off in every worktree while the tool is on, and give no command `--sparse-index`.
  - **Relied on:** R50, T8, T10, DR-037, DR-129
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A14. People who opt in know what it publishes, and keep other work apart.

- **Rests on it:** R1, R2, R3, R4, R37, R52, R108, R146, R155, R159, R164, R186, R194, R198, R199, T2, T3, T4, T5, T31, T38, T106, T111, T114, T116, T117, T129, T134, T145, T154, T155, T156, T171, T176, DR-045, DR-050, DR-052, DR-053, DR-055, DR-057, DR-136, DR-138, DR-168, DR-171, DR-182, DR-183, DR-200, DR-201, DR-202, DR-212, DR-213, DR-235
- **If it is wrong:** Work on another repository, private ones included, would be published here (T2), the ledger would reveal more about a person than they expected (T31, T3, T4, T5), a person who opts in during a session would have its calls up to the next run left out, so that its count is too low (T38), and a person who keeps the store in their backups, or puts back a copy of it after an opt-out, would keep its notes there, or bring back calls to be staged (T117). A person whose opt-in is not where the step reads it, or does not outlive a cloud session, would have nothing recorded. A person who opts in from the README's short start alone would not know what only its folded detail says (T145). A person who stops would stay recorded in the running sessions where they did not run the opt-out (T154), a member's own computer would keep an organization's opt-in after the organization stopped (T155), and a clone whose settings choose another environment would run a person's cloud sessions where its setup script opts them in (T156), and a person, or an organization's member, who was not told that one opt-in records each agent that a later release adds would have that agent's calls published too (T171, T176).
- **Fact:** People who opt in start each session in the repository, and keep work on other repositories, private ones above all, in sessions of their own.
  - **Relied on:** R3, T2, DR-057
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** A person who removes a ledger file for privacy deletes the file as well, so that a later `git add` cannot commit it again.
  - **Relied on:** R52, T2, DR-055
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** People who opt in know what the ledger publishes about them, and accept that a public repository shows, for each call, its UTC day, model, counts, price attributes, activity type, whether the main agent or a subagent made it, and a hash of its message id.
  - **Relied on:** R1, R4, T3, T4, T5, T31, DR-045, DR-052, DR-053, DR-136, DR-138, DR-202
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** People opt in before they start a session.
  - **Relied on:** R108, T38, DR-168
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** People who opt in read what the README says stays published after an opt-out, what a flag for calls left out says, that one opt-in covers every repository that turns the tool on, and where the store is, how to keep it out of backups and syncs, and how to remove it.
  - **Relied on:** R146, R155, R159, R164, T3, T106, T111, T114, T116, T117, T129, T134, DR-171, DR-182, DR-200
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** People who set the tool up from the README's short start read what it says an opt-in records and publishes before they opt in, or opt their members in.
  - **Relied on:** R199, T145, T171, DR-212, DR-213
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** A person who stops runs the opt-out on each machine and in each session that is running, as the README's short start says.
  - **Relied on:** R198, R199, T154
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** An organization that puts the opt-in's line in a shared environment's setup script tells its members first what it publishes, the agents that later releases add among them, as the README asks.
  - **Relied on:** R186, T134, T176, DR-202, DR-235
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** An organization that opts its members in through its managed settings uses the hook that the README gives, which writes the opt-in only in cloud sessions, and an Owner takes their own line out of an environment before sharing it or making it the default.
  - **Relied on:** R186, T134, T155
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** A person whose cloud sessions must not run in an environment that opts them in keeps their own pick of environment in a clone whose settings choose another, as the README says.
  - **Relied on:** R194, T156
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** People write their opt-in directly in `~/.gitconfig` or in git's file in their XDG configuration folder, not in a file that those include and not through an environment variable.
  - **Relied on:** R37, DR-183
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Each person keeps a global git configuration that outlives the session, or, in a cloud environment, a setup script that writes the opt-in into each new session's.
  - **Relied on:** R1, DR-050, DR-183, DR-201, DR-202
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Commit times in git already show when someone worked, so a ledger entry's UTC day discloses nothing new.
  - **Relied on:** R2, T5, DR-052
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A15. The owner merges, reads every diff and keeps the settings.

- **Rests on it:** R26, R27, R59, R124, R129, T2, T20, T28, T32, T33, T35, T37, T47, T53, T61, T62, T64, T66, T67, T68, T71, T72, T76, T77, T79, T81, T93, T94, T95, T102, T103, T128, T132, T137, T140, T147, T149, T151, T160, T161, T162, T163, T165, T166, T167, T168, T170, T172, T173, T174, T175, T177, T178, T179, T180, T181, T182, T183, T184, DR-015, DR-017, DR-072, DR-073, DR-074, DR-075, DR-076, DR-077, DR-078, DR-080, DR-093, DR-095, DR-096, DR-108, DR-111, DR-116, DR-119, DR-121, DR-122, DR-131, DR-134, DR-140, DR-141, DR-144, DR-145, DR-151, DR-153, DR-156, DR-161, DR-210, DR-237
- **If it is wrong:** An agent's mistaken or steered merge, a weakened check, a false attribution or private text could reach `main` unnoticed (T64, T72, T71, T77, T33), as could a change to the marketplace together with the check that holds it, or a root marketplace file that adds to the plugin (T132, T137, T140), a setting missing from what the threat model lists would let its answer fail without any sign (T62, T67), the owner's opt-in set where a session reaches this clone beside another repository's would publish counts of that repository's work here (T2, T32, T128), a roadmap that no longer says what holds, or that lists a link, a command or wording that leads elsewhere, could mislead contributors and adopters (T160, T161, T162, T163, T165), as could a guide whose principle, source or view of where the project stands no longer holds (T170), the change that adds an agent could record it under every existing opt-in without the answers that hold for Claude Code (T175), the walking skeleton could record people outside the opt-in, or record here before this repository's own capture is turned on (T172, T174), a page cut down to citations could lose what no scenario holds (T173), a release could ship a gap that adopters rely on without telling them (T177), a workflow merged here before its guard could be called from another repository (T178), a principle of the guide could be weakened beside the work that it forbade, or the guide's opening bent (T179, T180), an entry could drop a skill's step (T181), the build could start before the gaps that the owner asked closed first (T182), an entry moved out of a concern that adopters rely on could leave the owner's rules behind (T183), a task ticked before its work is done could open a gate that rests on the tasks (T184), and reviews and fixes would queue behind one person (T66).
- **Fact:** Only the owner merges pull requests here. Agent sessions, which act on GitHub as the owner's own account, never merge one, although the ruleset on `main` would let any of them merge a pull request that passes `ci`.
  - **Relied on:** R27, T28, T33, T35, T62, T64, T71, T72, DR-080, DR-122, DR-141, DR-156
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** No agent session can read or use the deploy key that alone may bypass the tag ruleset; the key is kept on the owner's own machine.
  - **Relied on:** T28, T64, T67, DR-073, DR-144, DR-161
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** The owner keeps the GitHub settings that the threat model lists under "Settings the owner keeps", among them approval for outside contributors' workflow runs, and approves those runs.
  - **Relied on:** T28, T33, T35, T37, T61, T62, T64, T67, T68, T76, DR-072, DR-073, DR-074, DR-075, DR-076, DR-077, DR-078, DR-119, DR-140, DR-141, DR-161
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** The owner reads every pull request's diff here before merging, closely enough to catch a changed check or script, a vendored update, a false attribution in a decision record, private text in a title or a file name, a wrongly numbered version, a change to what steers agents, an address in the README that sends people elsewhere, a rewording that changes what a rule or the README's short start says, text in the README, the roadmap or the guide worded for an agent, a roadmap or a guide that no longer says what holds, a change to the guide that would steer an agent against `CLAUDE.md`, a sentence of a page cut down to a citation that does not hold it, or a change that records sessions that its records leave out, such as the walking skeleton's here, or that adds an agent without showing that the answers that hold for Claude Code hold for it, a principle of the guide changed beside the work that it would stop, or moved to another concern, a line added to the guide's opening or an entry that differs from a skill's step, a release whose changelog leaves out a gap that adopters rely on, a reusable workflow added before its guard, a task ticked before its work is done, or work on the build before its gaps are closed.
  - **Relied on:** R124, R129, T33, T35, T53, T71, T72, T77, T79, T81, T93, T94, T95, T102, T103, T137, T140, T147, T149, T151, T160, T161, T162, T163, T165, T166, T167, T168, T170, T172, T173, T174, T175, T177, T178, T179, T180, T181, T182, T183, T184, DR-080, DR-096, DR-108, DR-116, DR-121, DR-151, DR-153, DR-237
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** The owner has time for every review, approval and report that waits on them: the reviews of each change, approving major updates, reviewing a dependency update's diff before any session uses it, deciding when the oldest Python rises, and acknowledging a security report within a week.
  - **Relied on:** R26, T35, T64, T66, DR-077, DR-093, DR-095, DR-111, DR-134, DR-145
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** The default branch's history is never rewritten.
  - **Relied on:** R59, R129, T20, T47, T71, T77, DR-015, DR-017, DR-121, DR-131, DR-153
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** **A pull request that changes the marketplace merged only alone** is kept as the threat model's section on the settings the owner keeps says.
  - **Relied on:** T132, T137, T140, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** **The owner's opt-in only in the environment of this repository's own project** is kept as the threat model's section on the settings the owner keeps says.
  - **Relied on:** T2, T32, T128, DR-210, `docs/threat-model.md`
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 checks it

## A16. Agents follow the repository's rules.

- **Rests on it:** R26, R33, R99, R204, T32, T33, T34, T35, T55, T62, T64, T65, T66, T67, T73, T77, T93, T95, T150, T158, T159, T164, T166, T172, T173, T174, T179, T181, DR-026, DR-069, DR-070, DR-081, DR-083, DR-111, DR-114, DR-115, DR-134, DR-144, DR-145, DR-146, DR-214, DR-227, DR-237
- **If it is wrong:** A dashboard approval, a changed setting or a tag made by an agent would count as the owner's decision (T64, T67), text that anyone can write could steer an agent with the owner's credentials (T33, T73), an untrusted branch's hooks could run with credentials that can push here (T34, T66), private references could reach public text (T32, T65), and an agent that followed the README's short start could opt the owner in where their sessions reach another repository beside this one (T150), an adopter's agent that set the tool up from the README could opt in the person who asked it (T158), an agent that read the roadmap or a gap on the guide could start an item that nobody asked for, or take the text of an issue that it names as an instruction (T159, T164), an agent could cut a page down to citations that do not hold its clauses (T173), an agent could set the opt-in for the walking skeleton's run (T172, T174), and an agent could follow a principle of the guide that its own branch rewrote, or drop a skill's step where an entry differs from it (T179, T181).
- **Fact:** Agent sessions never create, move or delete a tag or a release, never approve an item on Renovate's dependency dashboard, and never change a repository setting, a ruleset or a secret; only the owner does these, and only the owner decides when the oldest supported Python rises.
  - **Relied on:** R26, T62, T64, T67, DR-111, DR-134, DR-144
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Agents working here treat data files, records, the glossary, the assumptions, the roadmap, the backlog items and the pages that a file here links to, other than the files that steer, issue text and pull request text as data, never as instructions, follow the guide only as the default branch holds it, below the specs, `CLAUDE.md` and the steps of the Superpowers skills, and never as widening what an agent may do, start no backlog item and close no gap of the guide unless the person they work for asks for it, and bring a page that states behaviour to the rule that the specs are the single source only in the pull request that delivers its backlog item (B-022).
  - **Relied on:** T33, T73, T93, T95, T159, T164, T166, T173, T179, T181, DR-115, DR-227, DR-237
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Agents never start a session on, or check out, an unmerged branch that someone outside the project wrote, or a dependency-update branch before the owner has reviewed its diff.
  - **Relied on:** T34, T35, T66, DR-081, DR-145
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Agents never turn capture on for anyone, the owner included, and a test that needs the opt-in sets it only in a git configuration of the test's own, as `CLAUDE.md` says.
  - **Relied on:** T150, T172, T174, DR-214
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** An agent that sets the tool up in another repository reads the README's sections on the opt-in, on cloud threads and on organizations, and turns capture on for no one, as they say.
  - **Relied on:** R204, T158, DR-214
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Everyone who writes text here keeps private references, session links and session identifiers out of it, including the ones that the private-reference check does not know, and removes a link that a tool adds.
  - **Relied on:** R33, T32, T65, T77, DR-069, DR-070, DR-114
  - **Checked:** not yet: none will, since no check can know every private reference; `add-pr-cost-calculator` task 1.9 and `add-pr-cost-calculator` task 1.14 apply the known patterns to commits and pull request text
- **Fact:** Whoever writes a figure in prose, a commit message or pull request text computes it in the same session rather than recalling it.
  - **Relied on:** DR-083
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Whoever corrects a claim searches for its other copies, since no check holds that rule as a whole.
  - **Relied on:** R99, T55, DR-026, DR-146
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A17. People report bugs and vulnerabilities through the right channel.

- **Rests on it:** T61, T169, DR-069, DR-077, DR-114, DR-115, DR-116, DR-229
- **If it is wrong:** Private text, or a vulnerability before its fix, would be published in an issue (T61).
- **Fact:** People who report a bug heed the bug-report form's privacy warning, and file bugs through that form rather than through the feature-request template, which has no privacy checkbox.
  - **Relied on:** T61, T169, DR-069, DR-114, DR-115, DR-116, DR-229
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** People who find a vulnerability report it through the repository's private vulnerability reporting, not in a public issue.
  - **Relied on:** T61, DR-077
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A23. Adopters pin released commits, and update the hook and the pin together.

- **Rests on it:** R17, R24, R27, R28, R65, R71, R77, R88, R93, R98, R122, R123, R183, R203, T24, T28, T29, T53, T54, T58, T60, T64, T67, T69, T123, T133, T136, T148, T152, T153, DR-020, DR-022, DR-040, DR-054, DR-063, DR-065, DR-072, DR-073, DR-096, DR-097, DR-122, DR-123, DR-124, DR-132, DR-133, DR-139, DR-144, DR-149, DR-154, DR-156, DR-190, DR-203, DR-206, DR-208, DR-211, DR-217
- **If it is wrong:** A commit that no release vouched for, or one that only a fork holds, would run as the tool in the adopter's CI and on their machines (T58, T28, T64), a hook and a report from different commits would disagree on models and prices (T54), and an adopter who gives the report more than it needs, or relies on what the public surface leaves out, could be harmed or broken by an ordinary update (T24, T29, T53). A key that only some versions of the tool document would turn off the hook or the report that does not know it (T123). A zip that is not a release's would run as the tool's plugin in the sessions of a person who uploaded it unchecked (T133), as would the plugin of a copy of the README that a person followed (T148). A registration copied from another commit's README than the pinned one's would run nothing, as the comment then says (T152), and a refused release's tag that an update bot proposes would run as the tool (T153). A person's plugin far from a repository's pinned report would have more of its ledger lines refused, or would record nothing where the configuration file holds a key newer than it (T136).
- **Fact:** Adopters pin only a full commit that a published release of this repository names, an update bot's pin included, and check it with `git merge-base --is-ancestor`.
  - **Relied on:** R27, R203, T28, T58, T64, T67, T153, DR-022, DR-072, DR-073, DR-122, DR-144, DR-156, DR-217
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters take the hook file, its registration and the calling workflow from the README at the commit that their calling workflow pins, keep the hook file at the path that the README gives, and check it against the checksum that the README at that commit gives.
  - **Relied on:** R65, R88, R93, R203, T28, T60, T152, DR-022, DR-065, DR-211
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** A person who uploads the plugin's zip checks its SHA-256 against the README at the release's commit first, as the README asks.
  - **Relied on:** R183, T133, DR-203
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** People take the marketplace and the plugin's zip from this repository, by the addresses that the README gives, not from a copy of the README elsewhere.
  - **Relied on:** T148
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters update the hook file, its checksum and the workflow's pin together, in one pull request, so the hook's model names and the report's prices stay in step.
  - **Relied on:** R17, R65, R77, R98, T54, T123, DR-022, DR-054, DR-139, DR-190
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** A person keeps their plugin current, and a repository its pin, as the README asks, so that the release of a person's plugin and that of a repository's report seldom differ for long.
  - **Relied on:** T136, DR-206, DR-208
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** When the hook and the pin drift apart, the pin moves first: update bots that follow tags can propose a new pin but cannot change the copied hook file, and adopters update the pin more readily than the hook.
  - **Relied on:** R65, T53, T54, DR-022, DR-040, DR-139
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters take new releases soon after new models are priced, so the price tables in their hook and their report stay current.
  - **Relied on:** R17, R77, DR-020, DR-054, DR-124, DR-156
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters call the report through the README's calling workflow as given: on a push to the default branch, granting only the permissions it lists and passing no secrets.
  - **Relied on:** R24, T24, T29, DR-063, DR-132
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters' update bots treat minor and patch releases as safe and let them through, so the version number tells adopters what they must act on.
  - **Relied on:** R71, R123, T53, T123, DR-096, DR-123, DR-149, DR-154
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters run supply-chain checks that read a CycloneDX bill of materials.
  - **Relied on:** R28, T69, DR-097
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters depend on nothing outside the public surface that DR-154 lists: not on the comment's wording, the job summary's wording, the bill of materials or the version numbering itself.
  - **Relied on:** R71, R122, T53, DR-123, DR-124, DR-133, DR-154
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A24. The machine running a session, and the programs that a hook starts on it, are the person's own.

- **Rests on it:** R1, R12, R13, R32, R54, R152, T3, T15, T46, T56, T107, T109, T112, DR-027, DR-031, DR-125, DR-176, DR-183, DR-188, DR-202
- **If it is wrong:** On a shared machine one person's opt-in would record everyone who uses it (T3), and a program planted where the step or git looks for one would run as part of it with the person's rights (T46, T15). A machine without a working `python3` or `git` would record nothing and say nothing (T56). The capture step does not defend against a compromised machine.
- **Fact:** The machine running a session belongs to the person running it.
  - **Relied on:** R1, R54, R152, T3, T46, T107, T109, T112, DR-176, DR-183, DR-188, DR-202
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** On Windows, a program started by a bare name, such as `git`, is looked for first in the starting program's folder and in the current directory, and only then in the system's folders and the folders that `PATH` names.
  - **Relied on:** R54, T46, DR-188
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.3 checks it
- **Fact:** `/`, and Windows' system folder, can be written only by the system's administrator.
  - **Relied on:** R54, T46, DR-188
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Every machine that runs a session has a working `python3`, and a `git` in a folder that an absolute entry of `PATH` names.
  - **Relied on:** R13, R32, R54, T56, DR-027, DR-031, DR-188
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** The `python3` that the registered command starts, and the `git` found through the absolute entries of `PATH`, are the person's own programs, not ones that a repository's content put there.
  - **Relied on:** R12, R54, T15, T46, DR-125, DR-188
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A57. The reviews and the planned tests get done.

- **Rests on it:** R29, R31, R73, R74, R100, R101, R124, T57, T74, T75, T78, T80, T83, T90, T94, T96, T97, T98, T101, T103, T146, T149, DR-084, DR-085, DR-090, DR-091, DR-093, DR-094, DR-095, DR-098, DR-102, DR-103, DR-108, DR-112, DR-117, DR-120, DR-121, DR-147, DR-150, DR-158, DR-159
- **If it is wrong:** Stale citations would look like controls, and the threats that the code brings would be missed (T78, T80, T75), the matrix would show less risk than the built tool carries, a record could stay accepted after a change altered what it describes (T74), and the tool could do what its documentation leaves out (T57).
- **Fact:** Reviews in a context separate from the builder's happen on every change, at design and before merge, and they find what tests cannot: missing threats, citations that no longer say what holds the answer, records that misstate their sources, and IDs whose meaning changed.
  - **Relied on:** R31, R74, T74, T75, T78, T80, T83, T90, T94, T96, T97, T98, T101, T103, T146, T149, DR-085, DR-093, DR-095, DR-108, DR-120, DR-150, DR-158, DR-159
  - **Checked:** not yet: none will, since no test can show what a review misses; `add-pr-cost-calculator` task 5.1 and `add-pr-cost-calculator` task 5.2 run the reviews
- **Fact:** Every answer in the threat model gets built as specified, and the tests that the likelihood ratings count on get written. Until then each rating judges a design, not code.
  - **Relied on:** R31, DR-084, DR-094, DR-112
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.4 and `add-pr-cost-calculator` task 5.2 check it in part
- **Fact:** Every change that adopters would notice gets a line under `## [Unreleased]` in `CHANGELOG.md`.
  - **Relied on:** DR-098
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Whoever changes the tool documents, in the same pull request, what the documentation checks cannot see, such as a flow that a page leaves out.
  - **Relied on:** R73, R100, R101, T57, DR-103, DR-117
  - **Checked:** not yet: none will, since no check can see a flow that a page leaves out; `add-pr-cost-calculator` task 5.3 checks network calls and environment variables only
- **Fact:** A change that makes or reverses a decision adds its decision record in the same pull request.
  - **Relied on:** R124, T74, DR-108, DR-121
  - **Checked:** not yet: none will, since no check can tell that a change made a decision; `add-pr-cost-calculator` task 5.2 revisits the threat model against what was built
- **Fact:** The owner turns the tool on here, with their own opt-in, before the pull request that does `add-pr-cost-calculator` task 7.1 merges, so that its merge exercises the whole tool on real data: the hook records that pull request's work, and the merge's push runs the report, the only contact with GitHub's real API.
  - **Relied on:** DR-090, DR-147
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 checks it, at the merge of that task's own pull request
- **Fact:** A check can find every network call and every environment variable that the tool's code reads.
  - **Relied on:** R29, R101, T57, DR-102, DR-117
  - **Checked:** not yet: `add-pr-cost-calculator` task 5.3 checks it in part, against planted cases
- **Fact:** Every defect found can be reproduced by a test before it is fixed.
  - **Relied on:** DR-091
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A34. Maintainers review a pull request without checking out its branch where a session runs.

- **Rests on it:** R88, T59, DR-022, DR-211
- **If it is wrong:** The checksum would keep a changed hook file from running, but capture would stop for the rest of that session, and if Claude Code read its hook registrations again, the branch's code would run with the session's credentials (T59).
- **Fact:** Maintainers review a pull request from another worktree or from its diff, and never check out its branch in a worktree where a session runs.
  - **Relied on:** R88, T59, DR-022, DR-211
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A44. Teams want each pull request's cost, and read it as an estimate.

- **Rests on it:** R20, R90, R94, T16, T27, DR-001, DR-002, DR-066, DR-110
- **If it is wrong:** Fewer people would adopt the tool, and where the figure is used to charge or pay, a hand-edited ledger would do real harm (T16) and readers would misread what they pay (T27).
- **Fact:** Teams that build pull requests with AI coding agents want to know what each pull request cost.
  - **Relied on:** R20, DR-001
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** An API-equivalent estimate at list prices is useful, also to teams that pay through subscription plans or have CI minutes included in their plan.
  - **Relied on:** R94, DR-002
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Readers treat the figure as an estimate, not a bill, and nobody uses it to charge or pay, so few people have a reason to edit a ledger file by hand.
  - **Relied on:** R94, T16, T27, DR-002, DR-066
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Nothing else already adds up a pull request's model tokens and CI minutes.
  - **Relied on:** R20, DR-001, DR-110
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters accept the delay that capture adds to a session.
  - **Relied on:** R90
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A45. Adopters merge into the default branch by hand, after CI, having read the diff, and never rewrite that branch's history.

- **Rests on it:** R20, R58, R59, R62, R64, R67, R68, R93, R96, T16, T20, T21, T22, T47, T50, DR-005, DR-015, DR-017, DR-018, DR-019, DR-039, DR-051, DR-061, DR-066, DR-110, DR-131, DR-186
- **If it is wrong:** Merges made by a workflow would get no report (T50), a stacked pull request's CI cost would count its base's runs again (T22), and a hand-edited ledger or a repointed workflow would change the reported cost unnoticed (T16, T21). A rewrite of the default branch's history could erase earlier ledger files, so that a returning call is counted again (T47, T20).
- **Fact:** Adopters' pull requests merge into the default branch. A pull request closed without merging, or merged into another branch as in a stack, needs no report of its own.
  - **Relied on:** R20, R58, R68, DR-005, DR-017, DR-018, DR-061
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters merge pull requests themselves rather than through a workflow that uses `GITHUB_TOKEN`, or they know that such merges go unreported.
  - **Relied on:** R68, T50, DR-018
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters rebase a pull request that was based on one merged by squashing or rebasing before they merge it.
  - **Relied on:** R62, T22, DR-019
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** By the time the report runs, the pull request's CI runs have finished, and none is left waiting for approval.
  - **Relied on:** R64, R96, T22, DR-039, DR-110
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** In an adopting repository, whoever merges reads the pull request's diff before merging, its ledger files and workflow changes included.
  - **Relied on:** R93, T16, T21, DR-051, DR-066, DR-186
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Nobody rewrites the default branch's history, so its first-parent history before a merge holds every earlier ledger file.
  - **Relied on:** R59, R67, T20, T47, DR-015, DR-017, DR-131
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A46. Sessions commit through Bash, and little else changes the branch while a session works.

- **Rests on it:** R7, R8, R51, R78, R81, T8, T10, T19, DR-007, DR-010, DR-012, DR-013, DR-014, DR-034
- **If it is wrong:** No usage would reach the pull requests of people who commit through another tool or by hand (T8), and calls recorded on one branch could travel with a commit on another, so that one branch's usage is published with another pull request (T19, T10).
- **Fact:** Few sessions make commits or change branches through Claude Code's PowerShell tool.
  - **Relied on:** R7, T8, T19, DR-007
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** The agent makes the pull request's commits through its Bash tool, the last of them after the work whose usage should count.
  - **Relied on:** R7, R8, T8, DR-010, DR-013
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** While a session works, only the agent's own matched git commands change the branch or stage files in its worktree: the person makes no change of branch and no commit in their own terminal, also not while a permission prompt waits, and no other session commits in the repository.
  - **Relied on:** R8, R51, R78, R81, T8, T10, T19, DR-012, DR-013, DR-014, DR-034
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A47. Ledger files stay small, and their commits are rarely undone.

- **Rests on it:** R22, R52, R67, R70, R113, T8, T42, T48, DR-011, DR-015, DR-039, DR-055, DR-092, DR-127, DR-131, DR-184
- **If it is wrong:** In a busy, long-lived repository the report would reach its time limit and post nothing, and capture would spend its budget on old ledger files (T48, T42). Teams that rework their history often would lose much of their usage from reports (T8).
- **Fact:** Adopters' histories, ledger folders and stores stay small enough that capture reads them within its time budget and the report within its time limit.
  - **Relied on:** R22, R67, R70, T42, T48, DR-011, DR-015, DR-039, DR-092, DR-131
  - **Checked:** not yet: none will, since no test may reach adopters' repositories; `add-pr-cost-calculator` task 4.5 measures the time at the fixtures' scale
- **Fact:** Adopters accept a ledger folder that grows with every agent commit and stays in the repository for good; none wants the report without the record.
  - **Relied on:** R22, DR-015, DR-127
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Reverting, resetting or splitting a commit that holds a ledger file is rare in adopters' work.
  - **Relied on:** R52, R113, T8, DR-055, DR-184
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A58. Someone reads the report comments and job summaries, and keeps the prices current.

- **Rests on it:** R14, R16, R17, R93, R172, T21, T30, T49, T60, T123, DR-020, DR-051, DR-065, DR-124, DR-156, DR-186, DR-191
- **If it is wrong:** A changed switch, hook file or workflow, or a tool that a merge leaves off, would go unnoticed after the merge, and so would the reason that a merge with the tool off at both commits gets no comment (T21, T49, T60, T123), and a wrong or missing price row would leave the figure low or stale for as long as the table lags (T30).
- **Fact:** Someone reads the report's comment on each merged pull request and acts on its flags, such as a changed switch, hook file or workflow, and on its word that a merge leaves the tool off.
  - **Relied on:** R93, R172, T21, T49, T60, T123, DR-051, DR-065, DR-186, DR-191
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Someone who expects a report comment on a merged pull request and finds none opens the run's job summary, which says why.
  - **Relied on:** R172, T21, T49, T123, DR-191
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Each price row is right when it merges: whoever adds it copies the price from its source page, and the review of its diff catches a mistake.
  - **Relied on:** R14, R16, T30, DR-020
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Someone keeps the price table current, adding rows when providers change prices or release models, and releases the tool so that adopters can take the new rows.
  - **Relied on:** R14, R17, DR-020, DR-124, DR-156
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A60. Adopters' machines and runners meet the floors, and their policies allow the workflow.

- **Rests on it:** R25, R26, R32, R122, T56, DR-023, DR-024, DR-025, DR-027, DR-132, DR-134, DR-157
- **If it is wrong:** Sessions on a machine below either floor, and reports on a runner without a suitable Python, would record or post nothing, and the comments would read as facts about the work (T56). An adopter whose organisation allows only listed workflows would have to allow this repository first.
- **Fact:** The machines where people run Claude Code with the tool have `python3` 3.11 or later and git 2.43 or later.
  - **Relied on:** R25, R32, T56, DR-023, DR-025, DR-027, DR-134
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Python is common and well supported, so a tool written in it is open to the most adopters.
  - **Relied on:** DR-024
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Developers update a major component such as Python only when they must, so each rise of the oldest supported Python leaves out adopters who cannot follow it.
  - **Relied on:** R26, DR-134
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** The runner that an adopter's calling workflow chooses has what the report needs, such as a `python3` of 3.11 or later.
  - **Relied on:** R25, DR-023, DR-025, DR-027
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** Adopters' GitHub Actions policies let their workflows call a reusable workflow from this public repository.
  - **Relied on:** R122, DR-132, DR-157
  - **Checked:** not yet: none will, since no test may reach what adopters and people do

## A68. Other agents and review apps will expose their usage later.

- **Rests on it:** R20, R94, DR-003, DR-004, DR-234
- **If it is wrong:** A planned agent that gives no call's token counts could not be recorded at all, one whose usage fits no ledger format of the tool's could be added only with a change to the ledger format, a breaking change for adopters, and the cost of review by an app or a job in CI would stay out of the figure for good.
- **Fact:** Other agents, such as GitHub Copilot, Codex or Gemini, give each call's model and token counts where a later change can read them, as Claude Code's transcripts do, though for none of them is this known yet.
  - **Relied on:** DR-003, DR-234
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
- **Fact:** The usage of review apps and of review jobs in CI will become readable somewhere, so that a later change can add their cost.
  - **Relied on:** R20, R94, DR-004
  - **Checked:** not yet: none will, since no test may reach what adopters and people do
