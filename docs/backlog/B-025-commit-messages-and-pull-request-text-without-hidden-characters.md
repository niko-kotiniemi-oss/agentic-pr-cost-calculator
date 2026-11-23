# B-025: Commit messages and pull request text without hidden characters

- **Status:** Open to feedback and contributions
- **Last changed:** 2026-11-21
- **Brief:** A check that holds the messages of the commits that a pull request adds, and its title and body, to characters that a reader can see, as the files that this repository writes are held.
- **Rests on:** T251, DR-274, task 1.9 of `add-pr-cost-calculator`, task 1.14 of `add-pr-cost-calculator`
- **Issue:** none
- **Pull requests:** none

## Problem

A session reads commit messages through git and a pull request's text through GitHub's tools, and a merge commit can carry a pull request's title into the default branch's history. R268 holds every file that this repository writes to printable ASCII and line feeds, but a commit message and a pull request's text are not files, so no check reads their characters (T251, DR-274). A character that a reader cannot see, or one that changes the order in which text is shown, could reach a session and the owner's review unseen.

## What done looks like

A pull request whose commit messages, title or body hold a character that a reader cannot see, or one that changes the order in which text is shown, fails CI before it merges, and the failure names each such character by its code point, never by the character itself. The change has its own threat model first, since people outside the project write pull requests too: which characters the rule allows, and how it reads the text that tasks 1.9 and 1.14 read for private references.

## Postponed points

- From the threat review at design of pull request 59 (its point D4): a check of the characters in commit messages and pull request text, which T251's residual names and which tasks 1.9 and 1.14 could take when they are built.
