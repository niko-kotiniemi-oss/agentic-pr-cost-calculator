# DR-183: The opt-in is read only from the person's global git configuration, and git's own reading of it can only turn capture off

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R1, R37, R38, R103, R104, R105, R160
- **Threats:** T3, T14, T41, T119
- **Replaces:** DR-048
- **Closed by:** none

## Context

The opt-in has to be the person's own (DR-046). Yet a repository's settings can set environment variables for the hook that point git at another global configuration file or add settings, though Claude Code ignores `HOME` and the `XDG_*` variables there (see the design's context). An included file can lie in a repository's folder, and so can the folder that a relative `XDG_CONFIG_HOME` names, since git reads it from its current directory. On Windows, Python and git can take the home folder from different variables (T41). DR-048 decided that capture reads the opt-in only from the person's two global configuration files, so it also left unread an opt-out that only git finds: one in an included file, one under a condition that holds in a repository, or one in the file that `GIT_CONFIG_GLOBAL` names.

The owner asked on 2026-11-02 that the global scope of the opt-in be revisited, and that an authorization that the person controls repository by repository be assessed. Git already lets a person set a value for some folders and not for others, with conditional includes such as `includeIf "gitdir:~/work/"`. The owner kept one opt-in for every repository (DR-185).

## Decision

Capture reads the person's `pr-cost.capture` only from `~/.gitconfig` and git's configuration file in their XDG configuration folder, as DR-048 decided. It follows no include in them, ignores every variable that points git at other configuration files or adds settings, and reads no file from a relative path: it takes `XDG_CONFIG_HOME`, and `HOME`, only when absolute, and on Windows, without an absolute `HOME`, the folder that git uses when `HOME` is not set. It reads each file by git's rules for its configuration files, and where both files set the key, `~/.gitconfig` decides, since git reads it last.

Once that reading finds both switches on, capture also asks git, twice, for each value of the key that git reads in the repository, from every file and variable that git reads its settings from, the files that they include under the conditions that hold there among them: once in the session's environment, and once without the session's `GIT_` variables (DR-188). It takes the person's capture to be off when either answer does not come within the run's time budget or gives no value or a refusal, when its last value is not true, or when the last value of any one file other than the person's two global configuration files, or of the variables, is not true. What git reads never turns capture on, and no variable that changes which files git reads, or for which repository, hides an opt-out.

## Alternatives

- Keeping DR-048 alone, under which an opt-out that only an included file, a conditional include or the file that `GIT_CONFIG_GLOBAL` names holds goes unseen, so that a person cannot turn capture off for one folder.
- Taking git's own reading alone, the last value that git reads, under which a value that the repository's own configuration or a variable gives after an included file's opt-out would undo it, since git reads those last, and so would the person's own line that turns capture on, below the include.
- Letting git's reading turn capture on as well, which would let a repository's settings opt a person in, through the variables that point git at other files or add settings (T3).
- Asking git only in the session's environment, under which a variable that a repository's settings set, such as `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_NOSYSTEM` or `GIT_DIR`, could keep git from reading the file that holds an opt-out (T119).

## Consequences

- No variable that a repository's settings set, no included file and no relative `HOME` or `XDG_CONFIG_HOME` opts anyone in, which task 2.4 tests. A person's own setting kept only in an included file, or in the file that `GIT_CONFIG_GLOBAL` names, still does not opt them in (R37).
- An opt-out that git finds turns capture off, so a person who has opted in can turn capture off for a folder with git's own conditional includes, wherever the include stands in their file, as the opt-in's feature page and the README's section that task 4.4 writes show (R160, R164), and no value that git reads later undoes it. The variables that a repository's settings set can turn capture off in its sessions, never on, and since git's second reading runs without them, they cannot hide an opt-out in the person's own files, the system's or the repository's (T119).
- A file that the session's environment names for git to read its settings from, such as a named pipe that nothing writes to, can hold up the first reading, which the run stops at its time budget, and capture is then off for that run (T14).
- A value that turns capture off in the system's configuration file turns capture off too, though git reads the person's global files after it: only those two files are left out of the rule for each file's last value, since the step's own reading decides between them (R105).
- One opt-in still covers every repository that turns the tool on, those that adopt it later among them, as the README and the opt-in's feature page say (DR-182, DR-185).
- On Windows, with an absolute `HOME`, the step reads the `.gitconfig` that git reads, not the profile folder's (T41).
- Asking git starts a program twice in every run that finds both switches on, which runs git at its absolute path from a folder that only the system's administrator can write (DR-188).
- Each file that git reads the key from is part of the fingerprint, so a change to one between two runs is taken as an opt-out (DR-169).
- A repository's own hooks can still change the person's global configuration, as the threat model's assumptions say (T3's residual).

## Scope

This covers where the opt-in is kept and read from, and what git's own reading of it can do. How capture parses each file, by git's rules (R38), and which of them decides when both set the key, the one that git reads last (R105), are choices of their own that no other record holds, so this record covers them too, as DR-048 did. Which values turn capture on is DR-049 (The opt-in is read strictly), what the repository's own git configuration can do is DR-050 (A repository's git configuration can turn capture off, never on), and how a change to the files that hold the opt-in is noticed is DR-169 (A change to the files that hold the opt-in is taken as an opt-out).

## What reversing it would change

R37, R103, R104 and R160 in `switch-and-opt-in` would change, with their scenarios, and so would R1 there, where it keeps the person's setting in their global git configuration, and R38 and R105 with their scenarios, which this record covers too. So would the design's decision 6 where it names the files read, how it reads them and what git's reading does, the answers of T3 and T41, the `switch-and-opt-in` feature page, `docs/how-it-works.md`'s table of parts, its section on credentials and the variables it lists, the proposal's Impact, the README's section on adopting the tool, which task 4.4 writes, and task 2.4. The opt-in key is part of the public surface, so no longer reading it from either file would be a breaking change for adopters (DR-096). DR-049, DR-050 and DR-169 would be revisited.
