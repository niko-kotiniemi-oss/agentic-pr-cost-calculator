# DR-261: The context files are wrapped at 100 characters, so that their lines are the lines that the limits count

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-19
- **Requirements:** R253
- **Threats:** T94
- **Replaces:** none
- **Closed by:** none

## Context

The owner's limits on the root `CLAUDE.md` count lines (DR-260), and a count of lines means something only with a width. The repository writes one paragraph per line, so that the root, before this change, held 98 lines, the longest of them 1,506 characters, and 232 lines once wrapped at 100 characters, the width that `.editorconfig` gives Python files. A limit that counted the file's own lines would let one line hold a section, while a limit that counted wrapped lines would differ from the line numbers that GitHub shows, which are the ones that the owner reads. And `scripts/rewording.py`, which lists for the owner what a rewording changes, compares a file line by line, so that a reworded paragraph that reflows in a wrapped file would show as many changed lines, among which a change of meaning can hide (T94).

## Decision

Every context file is wrapped at 100 characters in the file itself, so that the line numbers that GitHub shows are the ones that the limits count, every line counted, blank ones included. A test fails on a line of a context file longer than 100 characters (R253). `scripts/rewording.py` compares the context files paragraph by paragraph, joining the wrapped lines of a paragraph or of a list's item first, so that a reworded paragraph that reflows shows as the words that changed, and it lists the changes to the context files first, as the files that steer.

## Alternatives

- Lines counted as the file holds them, one paragraph each: a root of a few long lines would meet any limit and say no less.
- Lines counted by a test after wrapping, with the files left one paragraph per line: the count would differ from what GitHub shows, so that the owner could not see in the file where its line 60 falls.
- A width other than 100 characters: the repository already gives 100 to Python, and a wider line is harder to read in a diff shown side by side.

## Consequences

- The context files differ from the rest of the repository, which writes one paragraph per line.
- A search for a phrase in a context file misses it where a line break falls inside the phrase.
- A rule that a change rewords in a context file reflows its paragraph, and the rewording script's comparison by paragraph shows the words that changed.

## Scope

This covers how the context files' lines are counted and compared. The limits are DR-260 (The root `CLAUDE.md` puts what does harm first, within 60 lines, and holds at most 200 lines), and where a rule lives is DR-259 (Each rule lives in the root `CLAUDE.md` or in the folder file of the folder where its work happens).

## What reversing it would change

How hard it is to reverse: reversible. Joining each paragraph of the context files back into one line is mechanical, and the limits, the test of the lines' width, R253 and the comparison by paragraph in `scripts/rewording.py` would change with it, with the answer of T94.
