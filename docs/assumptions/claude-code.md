# Claude Code

The assumptions about Claude Code: what its transcripts hold, when its hooks run and what they receive, and what a session loads. No test may reach Claude Code (DR-090), so a fact here is documented, with the page that says it, or not yet checked. [The index](README.md) lists every assumption, the most at stake first, and says how a fact is checked.

## A1. Claude Code keeps each session's transcript where the capture step can read it while the session lasts.

- **Rests on it:** R2, R7, R52, R87, T2, T8, T10, T19, DR-003, DR-008, DR-010, DR-014, DR-033, DR-053, DR-055, DR-110, DR-172, DR-184
- **If it is wrong:** If the transcript were kept elsewhere or in another form, capture would find nothing it can read, and no usage would reach a pull request (T8). If a transcript moved, or lost its earlier calls, at a resume or a change of worktree, a later run would miss a command's result, so a staged ledger file would wait (T10), or would record again calls that the branch holds (T19).
- **Fact:** Claude Code writes each session's transcript as JSON lines, one JSON object per line, in a file on the machine that runs the session.
  - **Relied on:** R2, T8, DR-003, DR-110, DR-172
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A cloud session's machine is thrown away when the session ends, and the transcript goes with it.
  - **Relied on:** R7, T8, DR-008, DR-010, DR-172
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Reading transcripts after a session has ended is slow for a long pull request, and needs access that a CI job does not have.
  - **Relied on:** R7, DR-172
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A transcript stays at the path the capture step noted, so a later run in the same repository, from that session or another, can still read it there.
  - **Relied on:** R87, T10, DR-014, DR-053
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A session resumed in a fresh clone of its branch, at the same path, still has its earlier calls in its transcript, with the same message ids.
  - **Relied on:** R2, R52, T2, T19, DR-033, DR-055, DR-184
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code moves a session's transcript when the session enters or leaves a worktree, so the path each run of that session receives is where the transcript is now.
  - **Relied on:** R87, T10, DR-014, DR-053
  - **Checked:** not yet: none will, since no test may reach Claude Code

## A2. A transcript line gives its call's model, usage, time and current directory, in fields whose meaning stays put.

- **Rests on it:** R2, R3, R6, R14, R15, R16, R40, R41, R43, R61, R76, R77, R78, R94, R95, R108, R109, R144, R147, R165, T1, T2, T5, T6, T7, T9, T10, T17, T27, T38, T39, T82, T104, T108, DR-002, DR-003, DR-012, DR-029, DR-032, DR-033, DR-052, DR-057, DR-092, DR-110, DR-135, DR-155, DR-168, DR-172, DR-179
- **If it is wrong:** Calls would be refused, priced wrongly or under-counted, and the comment would show it only as a count, if at all (T39, T9, T27). A line's time out of step with the step's clock would place calls in or out of an interval when both switches were on (T38), and a line that named another directory, or none, would sort calls to the wrong repository, so work in another one could be published here (T2, T82).
- **Fact:** Each assistant line in a transcript carries the model's name and a usage block with input, output, cache-write and cache-read token counts.
  - **Relied on:** R2, R15, T6, T39, DR-003, DR-033, DR-110, DR-172
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A call's cache-write tokens are split into two lifetimes, five minutes and one hour, where the transcript gives the split.
  - **Relied on:** R2, R15, T39, DR-155
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A call's usage gives its service tier, speed, inference region and server-side tool requests, under field names the capture step can know in advance.
  - **Relied on:** R2, R16, R61, R77, T9
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A call whose line gives no price attribute is billed at the standard rate, so an attribute that is not recorded adds nothing to the call's cost.
  - **Relied on:** R16, R61, T9
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** The usage a transcript holds for a call is the usage the provider bills for it.
  - **Relied on:** R2, R94, R95, T9, T27, DR-002, DR-032
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code adds fields to a call's usage over time, at its top level or nested in it, before the capture step knows them.
  - **Relied on:** R43, R95, T39, DR-135
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** The usage fields the capture step knows keep their meaning in later versions, and a field it does not know can only add to a call's cost.
  - **Relied on:** R43, R95, T39, DR-135
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** The transcript shapes that the synthetic fixtures copy are the ones that Claude Code writes.
  - **Relied on:** DR-003, DR-092, DR-172
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.1 checks it in part
- **Fact:** Every transcript line carries a timestamp, with its offset, in a form the capture step can read.
  - **Relied on:** R2, R14, R40, R108, T5, T38, DR-052, DR-168
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A line's timestamp is the time its call was made, on a correct clock that is the same clock the capture step reads when it runs.
  - **Relied on:** R40, R108, R109, T17, T38, DR-052, DR-168
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** The line that a call answers, the nearest up the chain of parents that the call's first line names that gives the person's prompt, a tool's result or a compaction's summary, is in the same transcript, and was written, by its timestamp, no later than the call's first line.
  - **Relied on:** R144, R165, T38, T104, DR-168
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code marks the transcript lines that it writes for its own bookkeeping, those that give a hook's output and its system lines, so that a run can tell them from the person's prompt, a tool's result and a compaction's summary.
  - **Relied on:** R144, T38, T104, DR-168
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code's transcripts name each line's working directory, Claude's current directory at the time of the call, and write a call's usage on its lines, the final usage on a line that gives its stop reason wherever such a line is written.
  - **Relied on:** R3, R41, R76, R78, R147, T2, T7, T10, T82, T108, DR-012, DR-057, DR-179
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code keeps a `cd` from one command to the next only while it stays inside the project directory and the directories added to the session, resets it after a command that leaves them, and never keeps one for a subagent.
  - **Relied on:** R3, T2, DR-057
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** The branch that a transcript line names can differ from the branch that is checked out when its call is made.
  - **Relied on:** R78, DR-012
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Each tool call in a transcript names its tool, the names of the edit, write, read, search, shell and subagent tools are known in advance, and an MCP tool can be recognised from its name.
  - **Relied on:** R6, T1, DR-029
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A call's lines come in the order of its content blocks, so the first tool named on its lines is the first tool the call invoked.
  - **Relied on:** R6, DR-029
  - **Checked:** not yet: none will, since no test may reach Claude Code

## A3. Hooks get enough time to finish, and every adopter's Claude Code has the hook events and the condition that the tool registers.

- **Rests on it:** R7, R10, R11, R13, R44, R87, R90, T8, T10, T13, T14, T19, T42, DR-014, DR-030, DR-036, DR-127, DR-172
- **If it is wrong:** Runs cut short would leave calls unrecorded, stores torn and ledger files staged, for the design's whole-file writes and take-backs to absorb (T42, T8, T10), and a run that blocked its command would stall the agent (T14). A Claude Code that lacks an event or the condition would skip it, and calls would wait or never be recorded, with nothing to say why (T8).
- **Fact:** Claude Code runs the hooks that match an event in parallel.
  - **Relied on:** R10, R11, T13, DR-036, DR-127
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** A command hook's default timeout is 600 seconds on `PreToolUse`, `PostToolUse` and `Stop`, and a `PreToolUse` command hook that times out does not block the tool call unless it sets `onFailure` to `block`.
  - **Relied on:** R13, R90, T14, T42, DR-036
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** `SessionEnd` hooks share a budget of 1.5 seconds, which Claude Code raises to match a longer `timeout` that the settings give a hook, up to 60 seconds.
  - **Relied on:** R87, R90, T8, T10, DR-014
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** One run's time budget is enough to read a session's transcripts to their end.
  - **Relied on:** R44, R90, T8, T19, T42, DR-172
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.5 checks it in part, at the fixtures' scale
- **Fact:** Every adopter's Claude Code supports all the hook events that the tool registers, and the `if` field.
  - **Relied on:** R7, T8, DR-030, DR-172
  - **Checked:** not yet: none will, since no test may reach Claude Code

## A4. A hook's input gives the directories, the paths and the command text that capture needs, and a hook that exits with success and prints nothing steers nothing.

- **Rests on it:** R3, R13, R43, R49, R51, R54, R55, R76, R82, R89, T2, T6, T8, T10, T14, T39, T44, T46, DR-007, DR-013, DR-031, DR-057, DR-128, DR-135, DR-187, DR-188
- **If it is wrong:** Capture could stage a ledger file in the wrong worktree, where no commit takes it, or fail to match a later run to its command, so ledger files wait or are staged twice (T10, T8). If a quiet success could still steer the agent, or a failure could stop the session, the hook could stall or redirect the agent's work (T14), and if the project directory named another folder, calls could be judged against the wrong repository (T2).
- **Fact:** A hook's input gives as `cwd` the directory Claude is working in: a worktree's root after Claude enters the worktree, and the new directory after Claude runs `cd`.
  - **Relied on:** R49, T10, DR-013
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** A hook's input gives the transcript's path, and a `PreToolUse` input gives the Bash command's text, as the command will run, and the call's `tool_use_id`.
  - **Relied on:** R51, R82, T8, T10, DR-013, DR-128
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude never sees the standard error of a hook that exits 0.
  - **Relied on:** R89, T14, DR-031
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** No one sees the standard error of a hook that succeeds, so only the ledger and the comment can show what the step refused or did not know.
  - **Relied on:** R43, R89, T6, T39, DR-031, DR-135
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A hook that exits with success and prints nothing on standard output does not steer the agent, while exit 2, or JSON on standard output, can block a call or send Claude back to work. A hook that fails otherwise lets the command and the session go on, unless it sets `onFailure` to `block`.
  - **Relied on:** R13, T14, DR-031
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** A command hook runs in the current directory, or, where that no longer exists, in the first that still exists of the directory the session started in, the project root, the home directory and the system's temporary directory.
  - **Relied on:** R54, R76, T46, DR-188
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** Claude Code gives each hook `${CLAUDE_PROJECT_DIR}`, the project root where the session started, which stays put when Claude enters a worktree.
  - **Relied on:** R3, R55, R76, T2, T44, DR-057, DR-187
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** Claude Code runs a hook's command with `sh -c` on macOS and Linux, in Git Bash on Windows, or in PowerShell where Git Bash is not installed, and in a PowerShell command rewrites `${CLAUDE_PROJECT_DIR}` into PowerShell's `${env:NAME}` form.
  - **Relied on:** R13, T14, DR-007, DR-031
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01

## A5. What a session loads comes from its settings and the branch it starts on, and a project's settings cannot set `HOME` or the `XDG_*` variables.

- **Rests on it:** R1, R37, R93, R103, R104, R160, R169, T3, T33, T34, T35, T36, T41, T60, T66, T119, DR-022, DR-041, DR-046, DR-050, DR-071, DR-081, DR-082, DR-093, DR-115, DR-126, DR-142, DR-143, DR-145, DR-183, DR-186, DR-188
- **If it is wrong:** If a project's settings could set `HOME` or the `XDG_*` variables, a repository could point both the step's reading of the opt-in and git's at configuration files of its own, to opt every contributor in or to hide an opt-out, so their usage would be published without their consent (T3, T119). If a session loaded more from its branch than the rules expect, the rules that keep sessions off untrusted branches would not be enough (T34, T35, T66), and if the vendored skills did not load, agents would build without them unless they read their files (T35).
- **Fact:** Environment variables that a repository's `.claude/settings.json` sets reach every process Claude Code starts, hooks included.
  - **Relied on:** R37, R160, R169, T3, T36, T119, DR-071, DR-183, DR-188
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code applies a repository's `.claude/settings.local.json` over its `.claude/settings.json`, hooks and environment variables among what it can set, and keeps it out of git only when Claude Code itself writes the file, so a repository can track one, which then needs the folder's trust as the other does.
  - **Relied on:** R93, T60, T119, DR-186, DR-188
  - **Checked:** documented: <https://code.claude.com/docs/en/settings>, read 2026-11-03
- **Fact:** Claude Code does not let a project's settings set `HOME` or the `XDG_*` variables, as its documentation says.
  - **Relied on:** R1, R37, R103, R104, T3, T41, T119, DR-046, DR-050, DR-183
  - **Checked:** documented: <https://code.claude.com/docs/en/settings-reference>, read 2026-11-01
- **Fact:** `/clear` and compaction rerun the session-start hooks from the working tree, so a branch checked out during a session acts like one the session started on.
  - **Relied on:** T34, T35, DR-081, DR-142
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A session loads `CLAUDE.md`, skills, settings and hooks from the branch it starts on, and its start-up hooks run with the session's credentials, in a cloud session installing the development tools with the owner's account.
  - **Relied on:** T34, T35, T66, DR-081, DR-115, DR-126, DR-145
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** `.claude/settings.json` makes Claude Code load the vendored Superpowers skills into every session here, and a session started outside the repository does not have them.
  - **Relied on:** T33, T35, DR-082, DR-142, DR-143
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A Claude Code plugin does not install itself in a fresh session, and a repository's own session-start hook can install one for everyone.
  - **Relied on:** DR-022, DR-041
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** `/simplify`, `/security-review`, `/code-review` and `/verify` are commands that a session here can run, in a context separate from the one that built the change.
  - **Relied on:** DR-093
  - **Checked:** not yet: `add-pr-cost-calculator` task 5.1 checks it, by running them

## A6. The agent runs git in forms that capture recognises, and acts on GitHub as the owner's own account.

- **Rests on it:** R7, R26, R33, R48, R52, R56, R79, R80, R82, R87, R112, T8, T10, T19, T32, T62, T64, T65, DR-007, DR-010, DR-013, DR-014, DR-030, DR-034, DR-035, DR-055, DR-070, DR-111, DR-128, DR-140, DR-141, DR-144
- **If it is wrong:** Commits made in other forms, through a wrapper, an alias, another tool or a person, would get no ledger file, so their calls would wait for a later commit or reach none (T8), and a change of branch made that way would send calls to the next branch (T19). If an agent could not read back and remove a link that a tool adds, private references would reach the public repository (T32, T65), and if agent sessions had an identity of their own, rulesets could hold what only `CLAUDE.md` holds today (T64).
- **Fact:** Claude Code applies the aliases and functions of the person's shell start-up file to every Bash command, so git run through one of them does not match the hook's condition.
  - **Relied on:** R7, R82, T8, T19, DR-030
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** The agent's Bash command runs in a shell that reads it as a POSIX shell does: quoting, here-documents, substitutions, `&&`, `;`, `||`, pipes, `&`, subshells and groups.
  - **Relied on:** R48, R79, R82, R112, T8, T10, DR-034, DR-128
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code's PowerShell tool is on by default on Windows for claude.ai and Console accounts, always on there without Git Bash, and can be turned on elsewhere, and hooks registered for Bash never run for its commands.
  - **Relied on:** R7, T8, T19, DR-007
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** The agent itself makes the pull request's commits, through the Bash tool, with a command whose text runs `git commit`.
  - **Relied on:** R7, R82, T8, DR-010, DR-013, DR-128
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude writes its commits in forms that capture recognises: `git` as a top-level command in the foreground, not behind a wrapper, an alias or another command's output.
  - **Relied on:** R82, T8, T10, T19, DR-013, DR-030, DR-034
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** An agent that finds an unfamiliar `.pr-cost/` file staged, in its status or in its commit leaves it alone, and does not unstage, delete or clean it up.
  - **Relied on:** R52, R56, R87, T8, T10, DR-013, DR-014, DR-035, DR-055
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Agent sessions act on GitHub as the owner's own account, so GitHub cannot tell an agent's approval, merge, tag or settings change from the owner's.
  - **Relied on:** R26, T62, T64, DR-111, DR-140, DR-141, DR-144
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Tools that Claude Code sessions use can add a link to a Claude session, or an identifier from one, to a commit or a pull request's text.
  - **Relied on:** R33, T32, T65, DR-070
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** An agent can read back the text it posted and remove such a link before it does harm.
  - **Relied on:** R33, T32, T65, DR-070
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.9 and `add-pr-cost-calculator` task 1.14 check it in part
- **Fact:** The shell splits a Bash command's text into its separate commands by rules that the text alone shows.
  - **Relied on:** R79, R80, T8, T10, DR-128
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it

## A25. Claude Code keeps the hook registrations it read at session start.

- **Rests on it:** R88, T59, DR-022, DR-058
- **If it is wrong:** A branch checked out during a session could change the registered command and the checksum that it carries, so that branch's hook file would run with the session's credentials, and T59's answer would not hold (T59). Claude Code's documentation says that it normally picks up direct edits to hooks in settings files, as a checkout that changes `.claude/settings.json` may be taken to be.
- **Fact:** Claude Code keeps the hook registrations it read at session start, so a hook file that a checkout changes is compared with the checksum the session started with (T59).
  - **Relied on:** R88, T59, DR-022, DR-058
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.1 checks it
- **Fact:** Claude Code normally picks up direct edits to hooks in settings files through its file watcher.
  - **Relied on:** T59
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01

## A36. Claude Code writes a call as lines that share one message id, with the call's final usage on each line that gives its stop reason.

- **Rests on it:** R2, R4, R11, R41, R42, R59, R95, T4, T7, T19, T27, DR-032, DR-033, DR-053, DR-131, DR-136
- **If it is wrong:** A call could be counted more than once, merged with another, read from partial usage or refused, and the figure would drift with no clear warning (T7, T19). If message ids could be guessed, or were held by others, a public entry could be linked to a session or a person (T4).
- **Fact:** Claude Code can write one call over several transcript lines that share its message id, and the earlier lines can give partial usage.
  - **Relied on:** R41, T7, DR-033
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Every line of a call that gives a stop reason gives the same final usage.
  - **Relied on:** R41, T7, DR-032, DR-033
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Every call's lines follow one of three shapes: every line gives a stop reason, only the last line does, or no line does.
  - **Relied on:** R41, R42, R95, T7, DR-032, DR-033
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** The lines of a call that give no stop reason only ever under-count it, never over-count it.
  - **Relied on:** R42, R95, T7, T27, DR-032
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** What the lines of a call with no stop reason leave out is small enough to accept.
  - **Relied on:** R95, T7, DR-032
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A call is over once a later call follows it in the same transcript, or once its agent has stopped, because the lines of different calls do not interleave.
  - **Relied on:** R42, T7, DR-032, DR-033
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A message id belongs to one call only: every line that carries it is part of that call.
  - **Relied on:** R2, R41, R59, T7, T19, DR-033, DR-131, DR-136
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A call that appears in more than one transcript carries the same message id, the same usage and the same facts in each.
  - **Relied on:** R11, R59, T7, T19, DR-033, DR-131
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Message ids are neither public nor guessable, so the SHA-256 hash of one links a public ledger entry to nothing for anyone who does not hold the transcript.
  - **Relied on:** R2, R4, T4, DR-053, DR-136
  - **Checked:** not yet: none will, since no test may reach Claude Code

## A37. Claude Code only appends whole lines to a transcript, soon after each call.

- **Rests on it:** R7, R44, R108, T7, T8, T19, T42, DR-168, DR-172
- **If it is wrong:** A run that reads on from where the last one stopped would skip, repeat or misread calls, or read a call from a partial line (T42, T7). A long lag would carry calls made just before a commit to the next commit or to none (T8), and calls made before a change of branch to the next branch (T19).
- **Fact:** Claude Code only appends whole lines to a transcript and never rewrites or cuts earlier ones, so a run can read on from where the last one stopped.
  - **Relied on:** R44, R108, T7, T42, DR-168, DR-172
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code ends every finished transcript line with a line break, so a line without one is still being written.
  - **Relied on:** R44, T7, T42, DR-172
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code writes the transcript asynchronously, so the transcript can lag behind the conversation.
  - **Relied on:** R44, T42, DR-172
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** A finished call's lines are on disk by a later run of the capture step, though not always by the time the hooks that follow the call run.
  - **Relied on:** R7, R44, T8, T19, DR-172
  - **Checked:** not yet: none will, since no test may reach Claude Code

## A38. A subagent's calls are in a transcript of their own, and the transcripts leave out only the calls that Claude Code makes for its own tools.

- **Rests on it:** R2, R3, R11, R75, R78, R94, T8, T13, T40, DR-004, DR-012, DR-057, DR-138, DR-172
- **If it is wrong:** Calls that capture cannot find, or cannot tell from the main agent's, would be missing from the figure or counted under the wrong agent (T8). If the calls missing from the figure were more, or cost more, than those of Claude Code's own tools, the figure would be lower than the comment says by more than it suggests (T40).
- **Fact:** Claude Code writes a subagent's calls to a transcript of its own, in a `subagents/` folder under the session's, marked so that they can be told from the main agent's calls.
  - **Relied on:** R2, R75, T8, DR-138
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code creates its worktrees under `.claude/worktrees/` inside the repository's folder, and a subagent may work in one of them.
  - **Relied on:** R3, R11, R78, T13, DR-012, DR-057
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A line's working directory still exists when capture runs, except a worktree that Claude Code removes when a subagent finishes without changes.
  - **Relied on:** R78, T8, DR-012
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A review that runs inside a session, such as `/code-review` or `/security-review`, writes its calls, and those of the subagents it starts, to that session's transcripts.
  - **Relied on:** R94, DR-004
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code makes some model calls for its own tools, such as its WebFetch tool's, without writing them to the transcript.
  - **Relied on:** R94, T40, DR-172
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.1 checks it
- **Fact:** The only model calls Claude Code leaves out of the transcript are those its own tools make.
  - **Relied on:** R94, T40, DR-172
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.1 checks it in part
- **Fact:** The model calls that Claude Code makes for its own tools are a small part of a session's cost.
  - **Relied on:** R94, T40, DR-172
  - **Checked:** not yet: none will, since no test may reach Claude Code

## A39. Claude Code's hooks behave as its documentation describes.

- **Rests on it:** R7, R9, R42, R49, R51, R75, R82, R87, R113, R116, R148, T8, T10, T19, T38, DR-013, DR-014, DR-030, DR-034, DR-138, DR-172
- **If it is wrong:** Runs that came at other moments, or not at all, would leave calls waiting for a later run, so they could reach no commit (T8), and a ledger file staged for a commit that was refused at a permission prompt or by a permission rule, blocked, cancelled or failed could stay staged while the person's git commands meet it (T10). A condition that matched fewer git commands would miss commits and changes of branch, so calls would wait or go to the wrong branch (T19).
- **Fact:** `Stop` runs when the main agent finishes responding, `SessionEnd` runs when a session ends, as when the person exits or runs `/clear`, and `PostToolUse` or `PostToolUseFailure` runs after each Bash call that ran.
  - **Relied on:** R7, R87, T8, T10, DR-014, DR-172
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** `SessionStart` runs when a session starts, is resumed or forked, and when it is cleared or compacted. At a session's start its hooks run in the background while the person can already type, Claude's first response waits for them, and a prompt sent meanwhile reaches Claude only once they have finished, what such a hook prints on standard output becomes context for Claude, and it cannot block the session.
  - **Relied on:** R148, T38, DR-172
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-02
- **Fact:** In an interactive session, the first prompt is written to the transcript after the start run has noted its time, unless the person sends it the moment the session starts, while a session whose first prompt is given before it starts, as with `claude -p`, the Agent SDK or a cloud session, may write it before.
  - **Relied on:** R148, T38, DR-172
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** `StopFailure` runs instead of `Stop` when a turn ends in an API error.
  - **Relied on:** R7, T8, DR-172
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** `SubagentStop` runs whenever a subagent finishes, including the agents Claude Code runs for its own features, and names the subagent's own transcript as `agent_transcript_path`.
  - **Relied on:** R42, R75, T8, DR-138, DR-172
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** `PreToolUse` runs, and finishes, before a Bash command starts and before any permission prompt.
  - **Relied on:** R7, R49, T10, T19, DR-013
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** A `Bash(git *)` condition is checked against each command a Bash input is made of, `$()` included, matches git only as Claude wrote it, and lets the hook run when Claude Code cannot tell what the input runs. On any other event, a hook with a condition never runs.
  - **Relied on:** R7, T8, T19, DR-030
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** A Bash call refused at a permission prompt or by a rule, blocked by another hook, or cancelled while it runs gets no `PostToolUse` or `PostToolUseFailure` run, and an interrupt runs no `Stop`.
  - **Relied on:** R9, R87, T10, DR-014
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** Claude Code writes a result into the transcript for a Bash command that was refused at a permission prompt or by a permission rule, blocked or cancelled.
  - **Relied on:** R87, T10, DR-014
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.1 checks it
- **Fact:** A blocked call's reason comes back to Claude as the call's error, and a cancelled call's result carries the interruption message.
  - **Relied on:** R87, T10, DR-014
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
- **Fact:** `PreToolUse` runs again, with the same `tool_use_id`, when a call that another hook deferred is resumed.
  - **Relied on:** R51, T10, DR-013
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** When another hook's deferral of a call ends the Claude Code process, a session-end run follows and can take back the ledger file staged for that call.
  - **Relied on:** R87, T10, DR-014
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.1 checks it
- **Fact:** A Bash command that the agent runs in the background returns its result at once, while the command still runs.
  - **Relied on:** R82, T8, DR-034
  - **Checked:** not yet: none will, since no test may reach Claude Code
- **Fact:** Claude Code moves a command that reaches its timeout to the background, and returns its result while the command still runs.
  - **Relied on:** R113, R116, T10
  - **Checked:** not yet: none will, since no test may reach Claude Code

## A61. A session that starts in a repository's folder runs the hooks that the repository's settings register, once the folder is trusted, unless it is a cloud thread of a project or a cloud session with several repositories.

- **Rests on it:** R7, T8, DR-126, DR-172
- **If it is wrong:** The calls of a session that starts in the repository's trusted folder and runs none of its hooks are never recorded, and the comment shows less than was used, with nothing to say why (T8).
- **Fact:** A cloud session with one repository, outside a project's threads, reads that repository's `.claude/settings.json`, since the file is part of the clone and the session starts inside it.
  - **Relied on:** R7, T8, DR-172
  - **Checked:** documented: <https://code.claude.com/docs/en/settings>, read 2026-11-01
- **Fact:** In a cloud thread of a project, none of a repository's `.claude/settings.json` hooks, permission rules or `env` apply, and a cloud session with several repositories reads only the `enabledPlugins` and `extraKnownMarketplaces` keys of each repository's file.
  - **Relied on:** R7, T8, DR-126, DR-172, `add-pr-cost-calculator` task 7.1
  - **Checked:** documented: <https://code.claude.com/docs/en/settings>, read 2026-11-01
- **Fact:** An interactive session holds back the hooks of every settings file until the person accepts the folder's workspace trust dialog, while a `-p` or SDK session treats the folder as trusted.
  - **Relied on:** R7, T8, DR-172
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01

## A62. A repository opened in Claude Code can already run any hook its own settings register, including one that changes a person's git configuration.

- **Rests on it:** R1, R37, R39, T3, T84, T112, DR-046, DR-050, DR-183
- **If it is wrong:** If a repository could not already run such a hook, the capture step's own hook would ask a person for trust that they had not given, and T3's residual would need an answer instead (T3). While it holds, the capture step adds no trust beyond that.
- **Fact:** Claude Code runs a command hook with the person's full user permissions, so that it can change any file their account can.
  - **Relied on:** R1, R37, R39, T3, T84, T112, DR-046, DR-050, DR-183
  - **Checked:** documented: <https://code.claude.com/docs/en/hooks>, read 2026-11-01
