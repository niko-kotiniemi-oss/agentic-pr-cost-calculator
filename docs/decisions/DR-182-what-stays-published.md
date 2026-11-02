# DR-182: The documentation says what stays published, and that a hash does not hide whose record it is

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R146, R159, R164
- **Threats:** T3, T4, T116
- **Replaces:** none
- **Closed by:** none

## Context

A ledger file that a commit holds is published once it is pushed, and an opt-out, a removed ledger file or a removed store changes nothing that was pushed: the file stays in its branch's history, in every clone and fork that holds it, and in the report comments already posted. An entry's call id is a hash of the call's message id (DR-136), which a reader could take for anonymity, though the commit that adds the ledger file names its author and whoever holds the transcript can match each hash. The owner asked on 2026-11-02 that the documentation say so clearly and imply no anonymity. One opt-in, in the person's global configuration, covers every repository that turns the tool on (DR-046), and the owner asked the same day that the global scope of the opt-in be revisited.

## Decision

The README and the opt-in's feature page say that what is pushed stays published, whatever the person does later, that a ledger file in a commit not yet pushed is published by that commit's push, opt-out or not, that a force-push that drops a commit does not remove what GitHub keeps for the pull requests that referenced it, and that a hashed id does not hide whose record it is, with the reasons. They also say that one opt-in covers every repository that turns the tool on, those that adopt it later among them, and that none says so when it does, that a repository's own git configuration that turns capture off holds only in that clone, and how a person turns capture off for a folder with git's own conditional includes (DR-183), and where that stops (DR-185). The glossary lists `anonymous` as a word to avoid, so that the wording test fails on a page whose prose uses it (DR-164).

## Alternatives

- Calling the ledger pseudonymous, a word that adopters may not know, and which still suggests more than a commit's author line leaves hidden.
- Leaving it to the reviews, which can miss a page that calls the ledger anonymous.

## Consequences

- A page that needs to say that something is not anonymous words it otherwise, as the glossary asks of every word to avoid.
- An adopter learns before opting in that an opt-out unpublishes nothing, and that the opt-in reaches every repository that turns the tool on (T3).

## Scope

This covers what the documentation says about what stays published and what a hash hides. What capture leaves in committed files at an opt-out is DR-171, and the hash in each entry is DR-136 (Only a hash of a call's message id is kept).

## What reversing it would change

R159 and R164 in `project-standards` and R146 in `switch-and-opt-in` would change, with their scenarios, and so would the design's decisions 6 and 16, the README and the opt-in's feature page that task 4.4 writes, the glossary, T3's and T4's residuals and T116. No format would change, so the change would not be a breaking one for adopters.
