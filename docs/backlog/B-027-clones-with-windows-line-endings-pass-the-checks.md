# B-027: Clones with Windows line endings pass the checks

- **Status:** Open to feedback and contributions
- **Last changed:** 2026-11-21
- **Brief:** The repository's tests pass, and its scripts and hooks run, in a clone in which git writes Windows line endings, a carriage return before each line feed, as they do in a clone that writes line feeds alone.
- **Rests on:** R268, R274, DR-274, DR-280
- **Issue:** none
- **Pull requests:** none

## Problem

In a trial on 2026-11-21, a clone of this repository made with `core.autocrlf` on failed 17 tests that passed in a clone made without it. Among them were the checks of single pages, which read each file as the working tree holds it and refuse a carriage return, and the tests that run the session's start hook and `scripts/sync-superpowers.sh`, both of which bash ended with an error, since it read the carriage return at the end of each line as part of the line. The test of characters that R268 adds reads the working tree too, so it fails in such a clone as well (DR-274), and a contributor who works in one cannot run the tests as they are.

## What done looks like

In a clone in which git writes a carriage return before each line feed, the scripts and hooks run, and every test that passes in a clone that writes line feeds alone passes, while a carriage return that git's index holds still fails. If the change sets line endings in the repository's attributes, which DR-280 keeps for such a fix, they still give nothing but line endings (R274).

## Postponed points

None.
