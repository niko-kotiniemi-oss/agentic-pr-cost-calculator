# DR-281: Every checkout holds line feeds, and the checks read Windows line endings as git stages them

- **Type:** technical
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-21
- **Requirements:** R176, R210, R255, R268, R269, R272, R274, R276
- **Threats:** T143, T251, T256
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-11-21 that the design not break with Windows line endings, since the project supports Linux, macOS and Windows. Git writes a carriage return before each line feed in a checkout where `core.autocrlf` is `true`, and an editor on Windows can save a file so. The repository tracked no attributes file, so each clone's line endings were left to the person's git, and the checks of single pages read each file as the working tree holds it, several of them refusing a carriage return before a line feed, as the test of characters of R268 would. In a trial with git 2.43.0 on 2026-11-21, a clone of this change's branch made with `core.autocrlf` set to `true` failed 17 of the 2773 tests, all of which passed in a clone made without it: tests of the checks of the backlog, the roadmap, the context files, the guide, the specs' form and the threat model, the test that runs the session's start hook, and the tests that run `scripts/sync-superpowers.sh`, which bash ended with an error, since it read the carriage return at the end of each line as part of the line. With one line of attributes that gave every file `text=auto` and `eol=lf`, such a clone held line feeds alone and passed every test. When each file that the repository writes, but its shell scripts, was then saved with a carriage return before each line feed and left unstaged, 10 tests failed, in the checks of the backlog, the roadmap, the context files, the guide, the specs' form and the threat model, though git would commit each such file with line feeds alone. `.editorconfig` asks editors for line feeds (DR-116), but not every editor reads it.

## Decision

One line of the repository's attributes gives every tracked file `text=auto` and `eol=lf`, so that git writes line feeds in every checkout, whatever `core.autocrlf` says, and stages each file that it reads as text with line feeds alone. Each check that reads a file of this repository from the working tree takes each carriage return right before a line feed as a line feed, as git does when it stages a text file, through one function that the checks share, in every file but a script, a file whose name ends in `.sh` or that starts with `#!`, which bash or the system reads with the carriage return as part of its line. The test of characters still fails on a carriage return that git's index holds, on one that no line feed follows, and on any in a script. A job of CI runs the tests again on a working tree in which each file that the repository writes, but its scripts, holds a carriage return before each line feed.

## Alternatives

- Leaving line endings to each person's git, as the repository did: a clone made with `core.autocrlf` set to `true` fails the tests, and its hook and scripts do not run.
- Taking each carriage return before a line feed as a line feed in the checks alone, with no attributes: the checks would pass in such a clone, but the hook and the scripts would still not run there.
- Giving every file `-text`, so that git never changes line endings: a clone would hold what the repository's objects hold, but a file that an editor saves with carriage returns would be committed with them, and fail only once the test of characters reads git's index.
- Giving every file `text` rather than `text=auto`: git would take every file as text, an image or a PDF that a record lets in among them, and change its bytes wherever they read as a carriage return and a line feed.
- Holding carriage returns in the files that git stores: each check, and each checksum of a file, would read two forms of every file, and a diff that changes only line endings shows each line as changed.

## Consequences

- The repository tracks a `.gitattributes` whose one line gives every file `text=auto` and `eol=lf`, and a test fails, naming the file and what its attributes give, when the attributes do not give a tracked file both, while R274's test of attributes still refuses any attribute but `text` and `eol` (R274, R276; task 1.54).
- A clone made with `core.autocrlf` set to `true` holds what git's index holds, the hooks that `.claude/settings.json` registers among it, so that the session's start hook and the scripts run there and every test passes (R276; T256; task 1.54).
- The checks of single pages, the test of characters and the test of the files that others write read the working tree through the shared function, and the scenarios of R176, R210, R255, R268, R269 and R272 that named a carriage return name one that no line feed follows, or one that git's index holds. A test that planted a carriage return before a line feed to show that a check fails plants one that no line feed follows instead, as those scenarios now give it, and the change that builds it says which (R276; T251; task 1.54).
- CI runs the tests again on a working tree whose own files, but its scripts, hold Windows line endings, so that a check which reads a file in another way fails there (R276; task 1.54).
- A check that reads what git holds rather than the working tree, such as the comparison of each record with the default branch, reads no carriage return as a line feed: one that a commit holds is still a change, and the test of characters refuses it (T251).
- A script that an editor saves with Windows line endings does not run in bash, which reads each carriage return as part of its line. The test of characters names it with the reason, and git commits it with line feeds alone, so CI and every other clone are not affected.
- A clone of this repository's marketplace holds the plugin's capture step with line feeds too, whatever `core.autocrlf` says; the plugin's command still takes each CRLF as LF, so that a person's own attributes, such as a `.git/info/attributes` that gives `eol=crlf`, change nothing that it runs (R276; T143; DR-211).

## Scope

This covers the line endings of every checkout of this repository and how its checks read them. The characters that a file may hold are DR-274 (Everything that this repository writes holds printable ASCII) and DR-275 (The files that others write hold only the visible characters that a test lists), the attributes that the repository may set are DR-280 (The repository's attributes set nothing but line endings, and are read as git holds them), and how the tool's command reads the hook file and the plugin's capture step is DR-211 (The capture step runs only when its checksum matches, with each CRLF taken as LF). The line endings of the files that the tool writes in an adopter's repository, such as a ledger file, are not covered here.

## What reversing it would change

How hard it is to reverse: reversible. The attributes are one line, and the reading one function that the checks share. R276 in `project-standards` would change, with its scenarios, and so would the scenarios of R176, R210, R255, R268, R269, R272 and R274 that name a carriage return, the answers of T251 and T256, design decision 23 and task 1.54, and a clone made with `core.autocrlf` set to `true` would fail the tests again, with its hook and scripts not running. Nothing that adopters configure or depend on changes, so the change would not be a breaking one for adopters.
