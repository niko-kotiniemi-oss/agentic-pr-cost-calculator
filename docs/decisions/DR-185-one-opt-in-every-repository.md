# DR-185: One opt-in covers every repository that turns the tool on, and a person turns capture off by folder

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-02 and 2026-11-03
- **Requirements:** R1, R160, R164
- **Threats:** T3, T121
- **Replaces:** none
- **Closed by:** none

## Context

Each person turns on capture of their own sessions, with one opt-in that applies in every repository that turns the tool on (DR-046). On 2026-11-02 the owner asked that the global scope of the opt-in be revisited, and that an authorization that the person controls repository by repository be assessed. The change set out the options with what each costs, and the design-stage review of the tool's boundary with its adopters found that each authorization given repository by repository brings a threat of its own. Opting in is a deliberate act of the person's own. A setting that changes what goes into a person's commits, such as the name and email that git writes, is commonly one global setting with exceptions by folder, which git's conditional includes give, while lists of allowed folders, such as git's `safe.directory`, guard against a repository that could run code or read secrets.

## Decision

One opt-in, in the person's global git configuration, covers every repository that turns the tool on, those that adopt it later among them, and the tool keeps no list of the repositories that a person allows. A person turns capture off for a folder with git's own conditional includes, which git's reading of the opt-in finds (DR-183), and for one clone with the repository's own git configuration (DR-050).

## Alternatives

- A required list of the repositories that the person allows, kept in their global configuration, each by the absolute path of its git common directory, matched exactly. It would add a setting of the tool's own: a list kept in dotfiles that a person publishes shows which repositories they work in, an entry outlives the repository that it named and covers another one cloned later at the same path, and a clone at another path needs an entry of its own. It would also change the default, which is a breaking change for adopters once a release exists (DR-096).
- An optional list, under which a person who keeps no list is covered in every repository, as under this decision. It brings the same costs to whoever keeps a list, and since it leaves the default as it is, it can be added later without a breaking change.
- A `true` in the repository's own git configuration as well as the opt-in. `git clone -c`, a repository's own hooks or a steered agent can write that file, and routine commands such as `git push -u` rewrite it, so it could not be part of the fingerprint (DR-169) without ending intervals at those commands, and an opt-out and back there between two runs would go unseen.
- The repository's own git configuration alone, under which something other than the person could opt them in, which DR-050 rules out.
- Taking an include whose file is missing as an opt-out, since capture cannot tell what the file held: in every repository, so that one missing file turns the person's capture off everywhere until it is back, or only where the include's condition holds, which would have capture judge git's conditions itself, a copy of git's matching rules that can drift from them. The owner chose on 2026-11-03 to leave the case to git, as the opt-in's feature page says, with the command that shows whether an opt-out reaches a repository (T121).

## Consequences

- A person who opts in for their own work and then works in another repository that turns the tool on has their counts recorded there, from the next run there that finds both switches on, unless they have turned capture off for its folder, and the ledger file is then part of their commits there (T3's residual).
- The opt-in's feature page, and the README's section that task 4.4 writes, say that one opt-in covers every repository that turns the tool on, with no notice, and how to turn capture off for a folder (R164, DR-182).
- Git matches a folder's conditional include against where a repository's git folder is, so a folder's opt-out does not reach a linked worktree in the folder whose repository lies elsewhere, and one whose condition names the folder through a symbolic link can miss a repository there, which the opt-in's feature page says, with the remedy for each (T121).
- Git reads an include whose file is missing as if it were not there, without a word, so a folder's opt-out whose file is missing, as when a person's synced dotfiles leave it out, leaves capture on in that folder, which the opt-in's feature page says, with the git command that lists, in a repository there, each value of the opt-in and the file that gives it (T121).
- Opting in stays one setting, and no file that a person publishes lists the repositories they work in.

## Scope

This covers which repositories one opt-in covers. Who turns capture on is DR-046 (Each person turns on capture of their own sessions), where the opt-in is read and what git's reading of it can do is DR-183, and what the repository's own git configuration can do is DR-050 (A repository's git configuration can turn capture off, never on).

## What reversing it would change

R1 in `switch-and-opt-in` and R164 in `project-standards` would change, with their scenarios, and a requirement for a list would be added, with negative scenarios: an unlisted repository records nothing, a prefix or a path spelled otherwise matches nothing, and neither an included file nor a variable adds an entry. A record that restates DR-046 would close it, and T3, the design's decision 6, the README's section on adopting the tool, which task 4.4 writes, the opt-in's feature page and task 2.4 would change. A required list would change the default, so once a release exists it would be a breaking change for adopters (DR-096).
