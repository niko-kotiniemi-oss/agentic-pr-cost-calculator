# DR-241: Where the guide says the project stands is held true, before the build and at each release

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-10-29 and 2026-11-14
- **Requirements:** R226, R227, R230, R233
- **Threats:** T170, T177, T182
- **Replaces:** none
- **Closed by:** none

## Context

The owner asked on 2026-10-29 that each anti-pattern that the design meets be fixed before the build (DR-231). The guide says, for each principle, where the project stands: followed, knowingly accepted with the record that gives the reason, or a gap with the backlog item that closes it, and a test failed while a gap named an item that was done or dropped. The threat review at design of the guide found that nothing else held what Where we stand says. The first view is written before any code exists, so `Followed.` would read for code that does not exist (T170). Under Security or Privacy, a principle knowingly accepted could name a record that a change rather than the owner decided, and a gap could name an item that no one had agreed to build and still read as handled. With the release check that the first design had for an anti-pattern to fix removed, nothing at a release told adopters of a security or privacy gap, while the README and its known limitations carry none (T177). And nothing held the owner's ask, since the item that closes a gap could leave the roadmap's Now, or a task of the build be ticked, with no test failing (T182).

The threat review at implementation of the guide found that one word lifted that gate: an entry whose Where we stand turned from `Gap.` to `Followed.` in the pull request that ticks a task of the build, while its item stayed under Now, passed every check, since no gap then named an item under Now (T182). The owner chose on 2026-11-14 that an entry leaves `Gap.` only with its item done.

## Decision

Where we stand opens with `Followed.` only while every task that the entry's Held by cites is ticked, and with `Designed.` while one of them is not. Under Security, Privacy, Identity and credentials, and Supply chain and releases, the four concerns that adopters rely on, a principle knowingly accepted names a record that the owner decided, and a gap names an item that is `Planned` or `In progress`. While a gap names an item that the roadmap lists under Now, which holds the items that make the design ready for the build, no task of the build is ticked, and a gap that the owner asked to be closed before the build opens with `Gap. Before the build.` and names such an item. Compared with the base, an entry leaves `Gap.` only while each backlog item that its gap named is `Done` or `Dropped`, so that a gap closes through its item, and not in the pull request whose work it holds back. The release workflow refuses a tag whose guide does not say that its entries were last read for that tag's version, or whose changelog entry leaves out the item of a gap under those four concerns.

## Alternatives

- A release check that refuses every release while the guide names a gap, as the first design had for an anti-pattern to fix: gaps are expected as the tool grows (DR-231), so it would hold back every release once an assessment finds one, while a release whose text names its gaps tells adopters without holding the release back.
- Where we stand left to review alone, as before: no reader could tell a principle designed from one built, and a change's own choice could read as the owner's accepted risk.
- The build held back only by the words `Gap. Before the build.`, which a pull request could drop beside the build's own work.
- An entry that leaves `Gap.` counted as a change of its principle (R228), so that it lands only in a pull request of documents alone, which would still let a gap close while its item stays open.
- A gap's close left to review, which the diff shows, so that the pull request that starts the build could also lift the gap that holds it back.

## Consequences

- Tests fail as R226, R227 and R233 say (tasks 1.28 and 1.30), and the release workflow refuses a tag as R230 says (task 6.1). The test of R233 examines nothing while no base holds the guide.
- Tasks 1.1 to 1.9, 1.13 to 1.15 and 1.21 of `add-pr-cost-calculator`, which no pull request that prepares the build has taken, and every task in a later section, wait for the items under the roadmap's Now that the guide's gaps name.
- A release's changelog entry names the item of each gap that adopters rely on, so that the release's text tells them.
- Whether a principle that is followed is really held, and whether a gap's item really closes it, still rest on review (T170).

## Scope

This covers how what the guide says of where the project stands is held true. The guide's form is DR-231 (A guide by concern says how the project builds, and steers below the specs and `CLAUDE.md`), and how a release is made is DR-148 (Each release is made from a tag).

## What reversing it would change

How hard it is to reverse: reversible. The rules are tests and a step of the release workflow, which one pull request can change, though a release made without them stays as it was published. R226, R227 and R233 in `project-standards` and R230 in `releases-and-compatibility` would change, with their scenarios, and so would design decision 12, tasks 1.28, 1.30 and 6.1, the guide's opening, and the answers of T170, T177 and T182.
