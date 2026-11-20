# DR-251: The checks of the documentation compare it with what a machine can read, and a rule about prose goes to review

- **Type:** process
- **Boundary:** inside
- **Reversibility:** reversible
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-17
- **Requirements:** none
- **Threats:** T173, T197, T198, T201
- **Replaces:** none
- **Closed by:** none

## Context

Backlog item B-022 asks that a record say which checks of the documentation stay once the documents cite the specs, and when a rule about prose goes to review instead of a new check, so that those checks do not grow faster than what they protect. The checks of the documentation are tests that read the documents, under `tests/`. They compare the register and the feature pages with the specs, the page on how the tool works with the workflows, the threat model's citations and ratings with what they name, the records' index with the records, the roadmap with the backlog and with the design's risks, and the guide, the glossary, the assumptions and the specs' form with their own rules. B-022 records that they hold the copies' IDs and tables but not their prose, which is why that prose drifted. Whether a page restates a scenario, and whether a citation covers the sentence that it replaces, is a judgement about meaning, which no test can make (T173).

## Decision

Every check of the documentation that the default branch holds when B-022's pull request opens stays, as it is: that pull request changes no file under `tests/` other than the tests of its own script, and a check that fails once a sentence is gone keeps the sentence, so that a check is never weakened in the diff that changes what it checks. Its script, which shows that no clause is lost, is committed with its tests and runs in that pull request, as design decision 19 gives it, and is not a check that CI runs on other pull requests. A rule about prose, such as that a page cites rather than restates, that it says only what no scenario can, or that a citation covers its sentence, is held by review, the four review lanes and the owner's, and not by a new check. A new check of the documentation is added only where it compares a document with a source that a machine reads, such as a spec, a workflow, a record or a file, and where a defect of the kind that it would hold has reached the default branch or a review once, or a threat with a risk of 4 or more rests on it. `CLAUDE.md` steers by this.

## Alternatives

- A check that every Answer of the threat model cites a scenario: it would pass an Answer that cites a scenario and still restates it, and fail one whose holders are rightly a task or a setting that the owner keeps.
- A check that compares each page's sentences with the specs' text: it would find copies word for word and miss every copy reworded, which is how the copies drifted.
- No rule on when a check is added: the checks of the documentation would go on growing with each rule that is written about prose.

## Consequences

- Review reads the swept pages for what the checks cannot, and a review lane that finds a page restating a scenario reports it as a finding.
- A pull request that proposes a new check of the documentation says which source it compares with and which defect, review or threat it rests on.
- A check that the sweep would need to change is changed in a pull request of its own, after the sweep, with the sentence that it reads kept until then.

## Scope

This covers which checks of the documentation stay and when one is added. That the specs are the single source is DR-232, and how the sweep shows that no clause is lost is design decision 19.

## What reversing it would change

How hard it is to reverse: reversible. A later record can add checks of prose or loosen the rule on when a check is added, with no change to the pages themselves.
