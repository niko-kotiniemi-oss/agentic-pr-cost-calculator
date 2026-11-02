# DR-048: The opt-in is read only from the person's global git configuration

- **Type:** security and privacy
- **Status:** closed
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R1, R37, R38, R103, R104, R105
- **Threats:** T3, T41
- **Replaces:** none
- **Closed by:** DR-183

## Context

The opt-in has to be the person's own (DR-046). Yet a repository's settings can set environment variables for the hook that point git at another global configuration file or add settings, though Claude Code ignores `HOME` and the `XDG_*` variables there (see the design's context). An included file can lie in a repository's folder, and so can the folder that a relative `XDG_CONFIG_HOME` names, since git reads it from its current directory. On Windows, Python and git can take the home folder from different variables (T41).

## Decision

Capture reads the person's `pr-cost.capture` only from `~/.gitconfig` and git's configuration file in their XDG configuration folder. It follows no include in them, ignores every variable that points git at other configuration files or adds settings, and reads no file from a relative path: it takes `XDG_CONFIG_HOME`, and `HOME`, only when absolute, and on Windows, without an absolute `HOME`, the folder that git uses when `HOME` is not set.

## Alternatives

None were recorded when this was decided.

## Consequences

- No variable that a repository's settings set, no included file and no relative `HOME` or `XDG_CONFIG_HOME` opts anyone in, which task 2.4 tests. By the same rule, a person's own setting kept only in an included file, or in the file that `GIT_CONFIG_GLOBAL` names, does not opt them in either (R37).
- On Windows, with an absolute `HOME`, the step reads the `.gitconfig` that git reads, not the profile folder's (T41).
- A repository's own hooks can still change the person's global configuration, as the threat model's assumptions say (T3's residual).

## Scope

This covers where the opt-in is kept and read from. How capture parses each file, by git's rules (R38), and which of them decides when both set the key, the one that git reads last (R105), are choices of their own that no other record holds, so this record covers them too. Which values turn capture on is DR-049 (The opt-in is read strictly), and what the repository's own git configuration can do is DR-050 (A repository's git configuration can turn capture off, never on).

## What reversing it would change

R37, R103 and R104 in `switch-and-opt-in` would change, with their scenarios, and so would R1 there, where it keeps the person's setting in their global git configuration, and R38 and R105 with their scenarios, which this record covers too. So would the design's decision 6 where it names the files read and how it reads them, the answers of T3 and T41, the `switch-and-opt-in` feature page, `docs/how-it-works.md`'s table of parts, its section on credentials and the variables it lists, the proposal's Impact, the README's section on adopting the tool, which task 4.4 writes, and task 2.4. The opt-in key is part of the public surface, so no longer reading it from either file would be a breaking change for adopters (DR-096). DR-049 and DR-050 would be revisited.
