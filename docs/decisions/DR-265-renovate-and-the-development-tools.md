# DR-265: Renovate proposes no newer development Python, merges nothing on its own, and notes how an update of OpenSpec or Superpowers is refreshed

- **Type:** technical
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-19
- **Requirements:** R259, R260, R261
- **Threats:** T34, T35, T66, T231
- **Replaces:** none
- **Closed by:** none

## Context

Backlog item B-003 asks for Renovate's configuration to keep the Python that the project develops on at the oldest supported release (DR-134), and to say that an update of OpenSpec or Superpowers has its generated files refreshed on its branch once its diff has been read. `.python-version` holds that release, and a test already fails a pull request that raises it alone, since every copy of the oldest supported Python must agree with the one that `pyproject.toml` requires, so that each newer release that Renovate proposed there would be a pull request that cannot pass. An update of OpenSpec or of the vendored Superpowers brings files that steer agent sessions, the generated `openspec-*` skills or the vendored skills and hook scripts, and its pull request at first changes only the pin, so that those files are refreshed on its branch after the owner has read that diff. A session on the branch would load and run them with the session's credentials before the owner has read them (T34, T35, T66), and a refresh made in such a session would run the new version, since `scripts/verify-openspec.sh` runs the pinned OpenSpec to write its skills again. The threat review at design also found that nothing kept a change to Renovate's configuration from letting it merge its own pull requests once the `ci` check passes, since the ruleset on `main` requires a pull request and that check but no approval (DR-072, DR-141, T231).

## Decision

Renovate's configuration has one package rule that matches the `pyenv` manager alone, which reads `.python-version`, and turns its updates off, and no other rule turns updates off (R259), so that Renovate proposes no newer development Python while CI still tests the newest release beside the oldest. The configuration sets `automerge` to nothing but `false`, at any depth, and extends no preset named for it, so that every update waits for the owner's merge (R260). A package rule that matches OpenSpec's npm package and Superpowers' repository by name gives each pull request that updates either a note: the owner reads its diff first; its generated or vendored files are then refreshed on its branch from a working tree outside any agent session's folder, and the owner reads the refreshed diff before merging; and no agent session starts on the branch before the owner has read its diff (R261). The root `CLAUDE.md` says that an agent refreshes such a branch's vendored or generated files only from a working tree outside its session's folder, so that the branch's context files and skills do not load into the session and its hooks do not run there.

## Alternatives

- CI that refreshes the generated or vendored files and commits them to the update's branch: workflow tokens are read-only but for releases and the report's comment (DR-067), and a job that pushed would run the update's code with a token that can write.
- Renovate left to propose each newer Python, closed by hand: each would be a pull request that fails, which someone must read to close.
- A rule that turns off more, by a package's name, a file or an update type: it could silence updates that should come, which the test refuses.
- Merging left to the ruleset alone: the ruleset requires no approval, so an update set to merge itself would wait only for `ci`.

## Consequences

- DR-145 still holds: a session starts on a dependency-update branch only once the owner has reviewed its diff, and the note repeats it on the pull request that the owner reads.
- DR-111 and DR-028 still hold: a major update waits for the owner's approval on the dependency dashboard, and minor and patch updates and vulnerability fixes are proposed as before.
- An update of OpenSpec or Superpowers is refreshed by running `scripts/verify-openspec.sh` or `scripts/sync-superpowers.sh` on its branch in a working tree outside any agent session's folder, and the refreshed files reach the pull request in a push that the owner reads before merging.
- A test reads Renovate's configuration for each of the three rules.

## Scope

This covers what Renovate proposes and merges, and how an update of OpenSpec or Superpowers is refreshed. When a session may start on a dependency-update branch is DR-145 (A session starts on a dependency-update branch only after the owner reviews its diff), and when the oldest supported Python rises is DR-134 (The oldest supported Python rises only near its end of life or for a security fix).

## What reversing it would change

How hard it is to reverse: reversible. The three rules are lines of `renovate.json`, held by R259 to R261 and their tests, beside a sentence of the root `CLAUDE.md`, and the answers of T34, T35, T66 and T231 would change.
