# DR-282: Every tracked path is one that Windows can write

- **Type:** technical
- **Boundary:** outgoing
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-21 and 2026-11-22
- **Requirements:** R277
- **Threats:** T258, T266
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-11-21 that the design not break with Windows line endings, since the project supports Linux, macOS and Windows, and said that leaving a problem that is already known out of the design now is against the intent of the product. Asked on 2026-11-22 whether that covers the paths that Windows cannot write too, the owner said that the guidance to support Linux, macOS and Windows already answers it; this record applies it to those paths. R268 holds every tracked path to printable ASCII but the space and refuses two paths that differ only in case, which a file system that ignores case keeps as one file (T258). Windows refuses more in a file name, among printable ASCII: Microsoft's page on naming files, read on 2026-11-21, gives, besides the slash that separates folders, the angle brackets, the colon, the double quote, the backslash, the vertical bar, the question mark and the asterisk, a name that ends in a space or a dot, and the names that it keeps for devices, such as `CON`, `NUL`, `COM1` and `LPT1`, which it says to avoid before an extension too, as `NUL.txt` and `NUL.tar.gz` are both `NUL`. Its page on the length of a path gives a path 260 characters, from the drive to its final null, and a folder that a program creates 12 fewer, so that a short name still fits in it, unless long paths are turned on. A clone whose files Windows cannot write fails there, a clone of this repository's marketplace, from which a person on Windows installs the plugin, among them, while the diff that adds such a path reads as ordinary and CI on Linux passes it (T266). On 2026-11-21, before this record, the 517 paths that this change's branch tracked held none of those characters or names, and no `~`, and the longest held 85 characters.

The design-stage review of this decision found that Windows can also give a file or a folder a short name in the form of DOS, such as `CLAUDE~1` for `.claude-plugin`, which the naming page says holds a `~`, and that git, with `core.protectNTFS` on, refused only the short names of `.git` in a trial with git 2.43.0 that day. A tracked path such as `CLAUDE~1/marketplace.json` then passes every check and the diff, while in a clone on Windows that keeps short names it would name the root marketplace file (T258).

## Decision

Every tracked path holds none of the characters that Windows refuses in a file name, no `~`, the character that Windows writes in a short name, no part that ends in a dot, and no part that is a name that Windows keeps for a device, `CON`, `PRN`, `AUX`, `NUL`, `COM0` to `COM9`, `LPT0` to `LPT9`, `CONIN$` or `CONOUT$`, alone or before a dot and in any case. A tracked path holds at most 140 characters, so that a clone in a folder whose own path holds up to 100 characters writes each file within the 260 characters that Windows allows a path and each folder within the 248 that it allows a folder that a program creates. The test of characters, which reads every tracked path, fails on each such path and names it with what Windows refuses in it.

## Alternatives

- Leaving such paths to review: a name such as `aux.md` or `CLAUDE~1/marketplace.json` reads as ordinary on Linux and macOS, and nothing in a diff shows that Windows refuses it or reads it as another file.
- Holding paths to letters, digits and a few marks: it would answer the characters, but not the names of devices or the length, and would refuse names that every system writes.
- Refusing only a `~` followed by a digit, as git does for the short names of `.git`: Microsoft's page gives the `~` of a short name but not what follows it, and no tracked path holds a `~` at all.
- A device's name only before its last dot: `aux.tar.gz` would pass, which Windows reads as `AUX`.
- A limit on each part of a path alone, as file systems give: the full path, which Windows limits, could still grow without bound.
- A limit of 150 characters on the tracked path: a file would fit within 260 characters, but a folder of the clone could pass the 248 that Windows allows a folder that a program creates.

## Consequences

- The test of characters fails on a tracked path, of any file, that holds such a character or a `~`, a part that ends in a dot or names a device, or more than 140 characters, naming the path and what Windows refuses in it or its length, and passes a part that only begins with a device's name, such as `console.md` (R277; T258, T266; task 1.55).
- A vendored update that brings such a path fails CI as any change does, and waits for the owner's decision, since a vendored file is never edited.
- A clone in a folder whose own path is longer than 100 characters may still pass Windows' limits, unless long paths are turned on. A contributor picks that folder, while Claude Code picks where it keeps its clone of a marketplace and its copy of the plugin, below the person's home folder, which task 7.2 records (A72).

## Scope

This covers the names and the length of every tracked path. Which other characters a path may hold, and paths and folders that differ only in case, are DR-274 (Everything that this repository writes holds printable ASCII), and the line endings that a checkout writes are DR-281 (A checkout writes line feeds whatever `core.autocrlf` says, and the checks read Windows line endings as git stages them).

## What reversing it would change

How hard it is to reverse: reversible. The check is part of one test. R277 in `project-standards` would change, with its scenarios, and so would the answers of T258 and T266, design decision 23 and task 1.55, and a path that Windows cannot write, or reads as another file, would again pass CI. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
