# DR-282: Every tracked path is one that Windows can write

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-21
- **Requirements:** R277
- **Threats:** T266
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-11-21 that the design not break on Windows, since the project supports Linux, macOS and Windows, and that a platform problem that is already known go into the design now rather than into a later item. R268 holds every tracked path to printable ASCII but the space and refuses two paths that differ only in case, which a file system that ignores case keeps as one file (T258). Windows refuses more in a file name, among printable ASCII: the angle brackets, the colon, the double quote, the backslash, the vertical bar, the question mark and the asterisk, a name that ends in a dot, and the names that it keeps for devices, such as `CON`, `NUL`, `COM1` and `LPT1`, alone or before an extension. It also limits a full path, from the drive on, to 260 characters unless long paths are turned on. A clone whose files Windows cannot write fails there, a clone of this repository's marketplace, from which a person on Windows installs the plugin, among them, while the diff that adds such a path reads as ordinary and CI on Linux passes it (T266). On 2026-11-21, before this record, the 517 paths that this change's branch tracked held none of those characters or names, and the longest held 85 characters.

## Decision

Every tracked path holds none of the characters that Windows refuses in a file name, no part that ends in a dot, and no part that is a name that Windows keeps for a device, `CON`, `PRN`, `AUX`, `NUL`, `COM0` to `COM9`, `LPT0` to `LPT9`, `CONIN$` or `CONOUT$`, alone or before an extension and in any case. A tracked path holds at most 150 characters, so that a clone in a folder whose own path holds up to 100 characters stays within the 260 characters that Windows allows a full path. The test of characters, which reads every tracked path, fails on each such path and names it with what Windows refuses in it.

## Alternatives

- Leaving such paths to review: a name such as `aux.md` reads as ordinary on Linux and macOS, and nothing in a diff shows that Windows refuses it.
- Holding paths to letters, digits and a few marks: it would answer the characters, but not the names of devices or the length, and would refuse names that every system writes.
- A limit on each part of a path alone, as file systems give: the full path, which Windows limits, could still grow without bound.
- A limit of 260 characters on the tracked path: the folder that holds a clone counts toward Windows' limit, so such a path would fail in any folder.

## Consequences

- The test of characters fails on a tracked path, of any file, that holds such a character, a part that ends in a dot or names a device, or more than 150 characters, naming the path and what Windows refuses in it or its length, and passes a part that only begins with a device's name, such as `console.md` (R277; T266; task 1.55).
- A vendored update that brings such a path fails CI as any change does, and waits for the owner's decision, since a vendored file is never edited.
- A clone in a folder whose own path is longer than 100 characters may still pass Windows' limit, unless long paths are turned on, which rests on the person's choice of folder.

## Scope

This covers the names and the length of every tracked path. Which other characters a path may hold, and two paths that differ only in case, are DR-274 (Everything that this repository writes holds printable ASCII), and the line endings that a checkout writes are DR-281 (Every checkout holds line feeds, and the checks read Windows line endings as git stages them).

## What reversing it would change

How hard it is to reverse: reversible. The check is part of one test. R277 in `project-standards` would change, with its scenarios, and so would the answer of T266, design decision 23 and task 1.55, and a path that Windows cannot write would again pass CI. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
