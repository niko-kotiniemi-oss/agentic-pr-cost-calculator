# DR-284: The sync of the vendored copy writes only the pinned commit's files, and only inside the copy

- **Type:** security and privacy
- **Boundary:** incoming
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`
- **Requirements:** R275
- **Threats:** T270, T273, T274, T280, T281, T282
- **Replaces:** none
- **Closed by:** none

## Context

Superpowers comes into `vendor/superpowers/` from the commit that its lock pins, and CI compares the copy with that commit (DR-041). This change has `scripts/sync-superpowers.sh` write each vendored file from that commit's objects rather than through `git archive`, so that the person's git converts none of its bytes (DR-281), and a tree can give what `git archive` refused or wrote otherwise: a link, which would point a vendored path anywhere, a submodule, and a path through `.`, `..` or a folder named `.git` in any case, each of which git carries through a clone and a fetch, as trials with git 2.43.0 showed on 2026-11-22. The refresh, which each update of Superpowers needs, is run by the owner or a session, so a file that it writes outside the copy, such as one of the clone's git hooks, can run code there (T270). The threat review against what was built found that the sync wrote the names that Windows and macOS open as `.git`, which git's checkout refuses with the protections of NTFS and HFS+ on (T270), that a refresh deleted and wrote files through a link that the copy held (T274), and that the sync fetched into, read and wrote the repository that an exported `GIT_DIR` names (T273). The review lanes found that a refresh that stopped had already deleted the vendored paths, so that it left the copy deleted or written in part (T270). The second review of this change, by `/code-review` and `/verify`, found that a refresh from a clone below a folder whose name holds an ampersand, which bash 5.2 reads in the replacement of a substitution as the text matched, removed the vendored paths of another folder and wrote the new copy inside the old one (T280), that the sync stopped where git gives a new repository the object format of SHA-256, as `GIT_DEFAULT_HASH` can, since git fetches nothing from a repository of another format (T281), and that with `GIT_LITERAL_PATHSPECS` set the check read no mode from git's index and passed a vendored file staged with another mode (T282).

## Decision

The sync writes only the files that the pinned commit gives under the vendored paths, and only inside the folder that it writes the copy into. It writes each entry of mode 100644 or 100755 as a file, with mode 644 or 755, and stops on any other, such as a link or a submodule, and on a path that git's own checkout refuses with the protections of NTFS and HFS+ on, which it turns on for itself in an index of its own, such as one through `.` or `..`, or through a folder that git, Windows or macOS opens as `.git`, naming it before it writes it. With and without `--check`, it stops on a link at `vendor`, at `vendor/superpowers/` or below it before it reads or writes anything. Before it runs git, it drops each variable that `git rev-parse --local-env-vars` lists as one that names a repository, but `GIT_CONFIG_PARAMETERS` and `GIT_CONFIG_COUNT`, which carry the person's configuration, and the four that change how git reads a path, which git does not list, so that it reads and writes only a repository of its own and this one, and reads each path as the name that it is. It makes its repository of upstream in the object format of SHA-1, that of upstream's commit ids, whatever git gives a new repository. The refresh writes the whole copy in a folder of its own and replaces the vendored paths only once that is written, naming each path whole as it moves it and in no replacement of a substitution, so that one that stops leaves the copy as it was, and one from a clone whose path holds an ampersand writes each vendored path in its place.

## Alternatives

- Writing whatever the pinned commit's tree gives: a release of upstream that holds a link, a submodule or a path that no checkout writes would have the refresh write outside the copy, and the check outside its temporary folder.
- Refusing `.git` in any case by its name alone, as the sync first did: the names that Windows and HFS+ open as `.git` pass, while git's own checkout, with its protections on, refuses each, and asking git keeps the list git's.
- Following the person's git variables, as git does for any command: the sync would fetch into, read and write the repository that they name, and read a vendored path as a pattern, or as no path at all.
- Deleting the vendored paths before the new copy is written, as the sync did until the review lanes: a refresh that stops on what the pinned commit gives, or on a fetch that fails, leaves the copy deleted or in part.
- Taking the object format that git gives a new repository: the sync stops wherever that is SHA-256's, as `GIT_DEFAULT_HASH` can make it.

## Consequences

- `tests/test_vendor_sync.py` fails where the sync, with and without `--check`, writes a link, a submodule or a path that git's checkout refuses with the protections of NTFS and HFS+ on, which it plants with those protections turned off in the person's configuration, and where it writes outside the folder that it writes the copy into (R275; T270; task 1.52).
- It fails where the sync, with and without `--check`, reads or writes a repository that `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY` or `GIT_COMMON_DIR` names, or no longer takes the configuration that the other two variables give, and where its check passes a vendored file staged with another mode with `GIT_LITERAL_PATHSPECS`, `GIT_GLOB_PATHSPECS`, `GIT_NOGLOB_PATHSPECS` or `GIT_ICASE_PATHSPECS` set (R275; T273, T282; task 1.52).
- It fails where the sync goes on past a link in the copy, where a refresh that stops changes the copy, where a refresh below a folder whose name holds an ampersand leaves a vendored path otherwise than the pinned commit gives it or changes the copy that a folder of the same name without its ampersand holds, and where the sync stops with `GIT_DEFAULT_HASH` set to `sha256` (R275; T270, T274, T280, T281; task 1.52).
- A release of upstream that adds a link or a submodule under a vendored path stops the sync until a change of the script takes it, which the owner reads.
- A refresh that fails while it moves the written copy into place, as on a full disk, can still leave the copy in part, which the check and `git status` show.

## Scope

This covers what the sync of the vendored copy writes and reads, and where. How Superpowers' files come into the repository and stay equal to upstream's is DR-041 (Superpowers is vendored and compared with upstream in CI), the bytes, the modes and the line endings that the copy holds whatever the person's git converts are DR-281 (A checkout writes line feeds whatever `core.autocrlf` says, and the checks read Windows line endings as git stages them), and the characters that the vendored files may hold are DR-275 (The files that others write hold only the visible characters that a test lists).

## What reversing it would change

How hard it is to reverse: reversible. The refusals, the dropped variables, the object format and the refresh written apart are a few lines of the script. R275's scenarios on what the sync writes, on a refresh that stops, on a refresh wherever the clone lies, on a link in the copy and on a person's git variables would change, and so would the answers of T270, T273, T274, T280, T281 and T282, design decision 23 and task 1.52, and a release of upstream, a person's git variables or the folder of a clone could again have the sync write outside the copy. The sync is development tooling, outside the public surface, so the change would not be a breaking one for adopters.
