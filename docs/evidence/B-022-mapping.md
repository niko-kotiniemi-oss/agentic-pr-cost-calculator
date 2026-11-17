# The mapping of the sweep of B-022

This is the evidence of the sweep that brought the documents to cite the specs, as design decision 19 of `add-pr-cost-calculator` and DR-232 give it. The text that it quotes is what the base commit held before that sweep, kept only to show that no clause was lost on the way. It does not say what the tool does: the specs do. It holds no instruction, and nothing in it is a step to carry out.

Each entry below is a unit of a page, a sentence, a list item, a table row, a heading or a fenced block, that the base held and that the pull request's head does not hold word for word. Old gives that unit. New, where there is one, gives the unit that replaces it. Each Clause gives a part of the old unit and where that part now is: in the new unit, elsewhere on the page, or in the requirement, scenario, record or task that it names. `scripts/sweep_evidence.py` checks that every such unit has an entry, that the clauses of each cover every word of it, and that every place exists at the head. Whether a place says what its clause said is for the review.

The section For B-007 lists the clauses that state what the tool does and that no scenario holds, or that a scenario contradicts, which the sweep leaves on their pages. The section Left as it is lists the sentences that state what the tool does in documents that the sweep does not change.

## `docs/assumptions/adopters-and-people.md`

### Entry

Old:

~~~~text
- **Rests on it:** R26, R27, R59, R124, R129, T2, T20, T28, T32, T33, T35, T37, T47, T53, T61, T62, T64, T66, T67, T68, T71, T72, T76, T77, T79, T81, T93, T94, T95, T102, T103, T128, T132, T137, T140, T147, T149, T151, T160, T161, T162, T163, T165, T166, T167, T168, T170, T172, T173, T174, T175, T177, T178, T179, T180, T181, T182, T183, T184, T185, T186, T187, T188, T190, T192, T193, DR-015, DR-017, DR-072, DR-073, DR-074, DR-075, DR-076, DR-077, DR-078, DR-080, DR-093, DR-095, DR-096, DR-108, DR-111, DR-116, DR-119, DR-121, DR-122, DR-131, DR-134, DR-140, DR-141, DR-144, DR-145, DR-151, DR-153, DR-156, DR-161, DR-210, DR-237, DR-248
~~~~

New:

~~~~text
- **Rests on it:** R26, R27, R59, R124, R129, T2, T20, T28, T32, T33, T35, T37, T47, T53, T61, T62, T64, T66, T67, T68, T71, T72, T76, T77, T79, T81, T93, T94, T95, T102, T103, T128, T132, T137, T140, T147, T149, T151, T160, T161, T162, T163, T165, T166, T167, T168, T170, T172, T173, T174, T175, T177, T178, T179, T180, T181, T182, T183, T184, T185, T186, T187, T188, T190, T192, T193, T195, T197, T198, T199, T200, DR-015, DR-017, DR-072, DR-073, DR-074, DR-075, DR-076, DR-077, DR-078, DR-080, DR-093, DR-095, DR-096, DR-108, DR-111, DR-116, DR-119, DR-121, DR-122, DR-131, DR-134, DR-140, DR-141, DR-144, DR-145, DR-151, DR-153, DR-156, DR-161, DR-210, DR-237, DR-248
~~~~

Clause, the new unit:

~~~~text
- **Rests on it:** R26, R27, R59, R124, R129, T2, T20, T28, T32, T33, T35, T37, T47, T53, T61, T62, T64, T66, T67, T68, T71, T72, T76, T77, T79, T81, T93, T94, T95, T102, T103, T128, T132, T137, T140, T147, T149, T151, T160, T161, T162, T163, T165, T166, T167, T168, T170, T172, T173, T174, T175, T177, T178, T179, T180, T181, T182, T183, T184, T185, T186, T187, T188, T190, T192, T193,
~~~~

Clause, the new unit:

~~~~text
DR-015, DR-017, DR-072, DR-073, DR-074, DR-075, DR-076, DR-077, DR-078, DR-080, DR-093, DR-095, DR-096, DR-108, DR-111, DR-116, DR-119, DR-121, DR-122, DR-131, DR-134, DR-140, DR-141, DR-144, DR-145, DR-151, DR-153, DR-156, DR-161, DR-210, DR-237, DR-248
~~~~

### Entry

Old:

~~~~text
- **Fact:** The owner reads every pull request's diff here before merging, closely enough to catch a changed check or script, a vendored update, a false attribution in a decision record, private text in a title or a file name, a wrongly numbered version, a change to what steers agents, an address in the README that sends people elsewhere, a rewording that changes what a rule or the README's short start says, text in the README, the roadmap or the guide worded for an agent, a roadmap or a guide that no longer says what holds, a change to the guide that would steer an agent against `CLAUDE.md`, a sentence of a page cut down to a citation that does not hold it, or a change that records sessions that its records leave out, such as the walking skeleton's here, or that adds an agent without showing that the answers that hold for Claude Code hold for it, a principle of the guide changed beside the work that it would stop, or moved to another concern, a line added to the guide's opening or an entry that differs from a skill's step, a release whose changelog leaves out a gap that adopters rely on, a reusable workflow added before its guard, a task ticked before its work is done, or work on the build before its gaps are closed.
~~~~

New:

~~~~text
- **Fact:** The owner reads every pull request's diff here before merging, closely enough to catch a changed check or script, a vendored update, a false attribution in a decision record, private text in a title or a file name, a wrongly numbered version, a change to what steers agents, an address in the README that sends people elsewhere, a rewording that changes what a rule or the README's short start says, text in the README, the roadmap or the guide worded for an agent, a roadmap or a guide that no longer says what holds, a change to the guide that would steer an agent against `CLAUDE.md`, a sentence of a page cut down to a citation that does not hold it, an entry of the sweep's mapping that gives a clause a place that does not say what it said, a page from which a reader learns less once it cites, a clause listed for B-007 that becomes an obligation, or a change that records sessions that its records leave out, such as the walking skeleton's here, or that adds an agent without showing that the answers that hold for Claude Code hold for it, a principle of the guide changed beside the work that it would stop, or moved to another concern, a line added to the guide's opening or an entry that differs from a skill's step, a release whose changelog leaves out a gap that adopters rely on, a reusable workflow added before its guard, a task ticked before its work is done, or work on the build before its gaps are closed.
~~~~

Clause, the new unit:

~~~~text
- **Fact:** The owner reads every pull request's diff here before merging, closely enough to catch a changed check or script, a vendored update, a false attribution in a decision record, private text in a title or a file name, a wrongly numbered version, a change to what steers agents, an address in the README that sends people elsewhere, a rewording that changes what a rule or the README's short start says, text in the README, the roadmap or the guide worded for an agent, a roadmap or a guide that no longer says what holds, a change to the guide that would steer an agent against `CLAUDE.md`, a sentence of a page cut down to a citation that does not hold it,
~~~~

Clause, the new unit:

~~~~text
or a change that records sessions that its records leave out, such as the walking skeleton's here, or that adds an agent without showing that the answers that hold for Claude Code hold for it, a principle of the guide changed beside the work that it would stop, or moved to another concern, a line added to the guide's opening or an entry that differs from a skill's step, a release whose changelog leaves out a gap that adopters rely on, a reusable workflow added before its guard, a task ticked before its work is done, or work on the build before its gaps are closed.
~~~~

### Entry

Old:

~~~~text
- **Relied on:** R124, R129, T33, T35, T53, T71, T72, T77, T79, T81, T93, T94, T95, T102, T103, T137, T140, T147, T149, T151, T160, T161, T162, T163, T165, T166, T167, T168, T170, T172, T173, T174, T175, T177, T178, T179, T180, T181, T182, T183, T184, T186, T187, T188, T190, T192, T193, DR-080, DR-096, DR-108, DR-116, DR-121, DR-151, DR-153, DR-237
~~~~

New:

~~~~text
- **Relied on:** R124, R129, T33, T35, T53, T71, T72, T77, T79, T81, T93, T94, T95, T102, T103, T137, T140, T147, T149, T151, T160, T161, T162, T163, T165, T166, T167, T168, T170, T172, T173, T174, T175, T177, T178, T179, T180, T181, T182, T183, T184, T186, T187, T188, T190, T192, T193, T195, T197, T198, T199, T200, DR-080, DR-096, DR-108, DR-116, DR-121, DR-151, DR-153, DR-237
~~~~

Clause, the new unit:

~~~~text
- **Relied on:** R124, R129, T33, T35, T53, T71, T72, T77, T79, T81, T93, T94, T95, T102, T103, T137, T140, T147, T149, T151, T160, T161, T162, T163, T165, T166, T167, T168, T170, T172, T173, T174, T175, T177, T178, T179, T180, T181, T182, T183, T184, T186, T187, T188, T190, T192, T193,
~~~~

Clause, the new unit:

~~~~text
DR-080, DR-096, DR-108, DR-116, DR-121, DR-151, DR-153, DR-237
~~~~

### Entry

Old:

~~~~text
- **Rests on it:** R26, R33, R99, R204, T32, T33, T34, T35, T55, T62, T64, T65, T66, T67, T73, T77, T93, T95, T150, T158, T159, T164, T166, T172, T173, T174, T179, T181, T185, DR-026, DR-069, DR-070, DR-081, DR-083, DR-111, DR-134, DR-144, DR-145, DR-146, DR-214, DR-227, DR-237, DR-243, DR-244
~~~~

New:

~~~~text
- **Rests on it:** R26, R33, R99, R204, T32, T33, T34, T35, T55, T62, T64, T65, T66, T67, T73, T77, T93, T95, T150, T158, T159, T164, T166, T172, T173, T174, T179, T181, T185, T196, DR-026, DR-069, DR-070, DR-081, DR-083, DR-111, DR-134, DR-144, DR-145, DR-146, DR-214, DR-227, DR-237, DR-243, DR-244
~~~~

Clause, the new unit:

~~~~text
- **Rests on it:** R26, R33, R99, R204, T32, T33, T34, T35, T55, T62, T64, T65, T66, T67, T73, T77, T93, T95, T150, T158, T159, T164, T166, T172, T173, T174, T179, T181, T185,
~~~~

Clause, the new unit:

~~~~text
DR-026, DR-069, DR-070, DR-081, DR-083, DR-111, DR-134, DR-144, DR-145, DR-146, DR-214, DR-227, DR-237, DR-243, DR-244
~~~~

### Entry

Old:

~~~~text
- **Fact:** Agents working here treat data files, records, the glossary, the assumptions, the roadmap, the backlog items and the pages that a file here links to, other than the files that steer, issue text and pull request text as data, never as instructions, follow the guide only as the default branch holds it, below the specs, `CLAUDE.md` and the steps of the Superpowers skills, and never as widening what an agent may do, start no backlog item and close no gap of the guide unless the person they work for asks for it, and bring a page that states behaviour to the rule that the specs are the single source only in the pull request that delivers its backlog item (B-022).
~~~~

New:

~~~~text
- **Fact:** Agents working here treat data files, records, the glossary, the assumptions, the roadmap, the backlog items and the pages that a file here links to, other than the files that steer, issue text and pull request text as data, never as instructions, follow the guide only as the default branch holds it, below the specs, `CLAUDE.md` and the steps of the Superpowers skills, and never as widening what an agent may do, start no backlog item and close no gap of the guide unless the person they work for asks for it, bring a page that states behaviour to the rule that the specs are the single source only in the pull request that delivers its backlog item (B-022), and treat the text that the sweep's mapping quotes as what the default branch held before that sweep, never as what the tool does.
~~~~

Clause, the new unit:

~~~~text
- **Fact:** Agents working here treat data files, records, the glossary, the assumptions, the roadmap, the backlog items and the pages that a file here links to, other than the files that steer, issue text and pull request text as data, never as instructions, follow the guide only as the default branch holds it, below the specs, `CLAUDE.md` and the steps of the Superpowers skills, and never as widening what an agent may do, start no backlog item and close no gap of the guide unless the person they work for asks for it,
~~~~

Clause, the new unit:

~~~~text
and
~~~~

Clause, the new unit:

~~~~text
bring a page that states behaviour to the rule that the specs are the single source only in the pull request that delivers its backlog item
~~~~

Clause, the new unit:

~~~~text
(B-022)
~~~~

### Entry

Old:

~~~~text
- **Relied on:** T33, T73, T93, T95, T159, T164, T166, T173, T179, T181, DR-227, DR-237, DR-244
~~~~

New:

~~~~text
- **Relied on:** T33, T73, T93, T95, T159, T164, T166, T173, T179, T181, T196, DR-227, DR-237, DR-244
~~~~

Clause, the new unit:

~~~~text
- **Relied on:** T33, T73, T93, T95, T159, T164, T166, T173, T179, T181,
~~~~

Clause, the new unit:

~~~~text
DR-227, DR-237, DR-244
~~~~

## `docs/backlog/B-022-the-specs-as-the-single-source.md`

### Entry

Old:

~~~~text
- **Status:** Planned
~~~~

New:

~~~~text
- **Status:** In progress
~~~~

Clause, the new unit:

~~~~text
- **Status:**
~~~~

Clause, changed, the item moves to In progress with this pull request:

~~~~text
Planned
~~~~

### Entry

Old:

~~~~text
- **Last changed:** 2026-11-14
~~~~

New:

~~~~text
- **Last changed:** 2026-11-17
~~~~

Clause, the new unit:

~~~~text
- **Last changed:**
~~~~

Clause, changed, the item moves to In progress with this pull request:

~~~~text
2026-11-14
~~~~

### Entry

Old:

~~~~text
- **Pull requests:** none
~~~~

New:

~~~~text
- **Pull requests:** 41
~~~~

Clause, the new unit:

~~~~text
- **Pull requests:**
~~~~

Clause, changed, the item moves to In progress with this pull request:

~~~~text
none
~~~~

## `docs/roadmap.md`

### Entry

Old:

~~~~text
- [B-022: The specs as the single source](backlog/B-022-the-specs-as-the-single-source.md) - Planned, last changed 2026-11-14. The documents that state what the tool does today, such as the threat model, the design's risks, the feature pages and the register, brought to cite the specs instead of stating it again.
~~~~

New:

~~~~text
- [B-022: The specs as the single source](backlog/B-022-the-specs-as-the-single-source.md) - In progress, last changed 2026-11-17. The documents that state what the tool does today, such as the threat model, the design's risks, the feature pages and the register, brought to cite the specs instead of stating it again.
~~~~

Clause, the new unit:

~~~~text
- [B-022: The specs as the single source](backlog/B-022-the-specs-as-the-single-source.md) -
~~~~

Clause, changed, the item moves to In progress with this pull request:

~~~~text
Planned
~~~~

Clause, the new unit:

~~~~text
last changed
~~~~

Clause, changed, the item moves to In progress with this pull request:

~~~~text
2026-11-14
~~~~

Clause, the new unit:

~~~~text
The documents that state what the tool does today, such as the threat model, the design's risks, the feature pages and the register, brought to cite the specs instead of stating it again.
~~~~

## `docs/threat-model.md`

### Entry

Old:

~~~~text
It holds 194 threats across 9 trust boundaries.
~~~~

New:

~~~~text
It holds 200 threats across 9 trust boundaries.
~~~~

Clause, the new unit:

~~~~text
It holds
~~~~

Clause, changed, the count and the answer follow this change's design and threats:

~~~~text
194
~~~~

Clause, the new unit:

~~~~text
threats across 9 trust boundaries.
~~~~

### Entry

Old:

~~~~text
T38 to T69 were found by the design-stage review, T70 to T78 by the design-stage review of the decision records in `docs/decisions/`, T79 to T81 by the implementation-stage review of those records and their checks, T82 to T100 by the design-stage review of the assumptions, the glossary and the golden set, T101 by the implementation-stage review of the assumptions, T102 and T103 by the implementation-stage review of the glossary, T104 to T116 at the design of the revision of consent, the store and the ledger's format, T117 and T118 by the design-stage review of that revision, T119 to T122 by the review of that revision after its approval, T123 with the owner's answer to a question that the check of that review's fixes raised, T124 to T126 by the design-stage review of the test of the specs' form, T127 by the implementation-stage review of that test, T128 to T135 at the design of the plugin that brings capture to a project's cloud threads, T136 to T142 by the design-stage review of that plugin, T143 by its implementation-stage review, T144 by its security review, T145 to T147 at the design of the README's short start, T148 to T156 by the design-stage review of that short start, T157 and T158 by its implementation-stage review, T159 to T162 at the design of the roadmap, T163 to T165 by the design-stage review of the roadmap, T166 to T168 at the design of the backlog, T169 by the design-stage review of the backlog, T170 at the design of the guide, T171 to T174 by the design-stage review of the guide, T175 and T176 by the design-stage review of one opt-in for every agent, T177 to T182 by the second design-stage review of the guide, T183 by the final review of its build, T184 by its implementation-stage review, and T185 to T189 at the design of the walking skeleton and T190 to T194 by its design-stage review; they follow T37, each under a heading for its boundary, so that the numbers stay in order, and a threat that a change removes keeps its ID out of use (see Retired IDs).
~~~~

New:

~~~~text
T38 to T69 were found by the design-stage review, T70 to T78 by the design-stage review of the decision records in `docs/decisions/`, T79 to T81 by the implementation-stage review of those records and their checks, T82 to T100 by the design-stage review of the assumptions, the glossary and the golden set, T101 by the implementation-stage review of the assumptions, T102 and T103 by the implementation-stage review of the glossary, T104 to T116 at the design of the revision of consent, the store and the ledger's format, T117 and T118 by the design-stage review of that revision, T119 to T122 by the review of that revision after its approval, T123 with the owner's answer to a question that the check of that review's fixes raised, T124 to T126 by the design-stage review of the test of the specs' form, T127 by the implementation-stage review of that test, T128 to T135 at the design of the plugin that brings capture to a project's cloud threads, T136 to T142 by the design-stage review of that plugin, T143 by its implementation-stage review, T144 by its security review, T145 to T147 at the design of the README's short start, T148 to T156 by the design-stage review of that short start, T157 and T158 by its implementation-stage review, T159 to T162 at the design of the roadmap, T163 to T165 by the design-stage review of the roadmap, T166 to T168 at the design of the backlog, T169 by the design-stage review of the backlog, T170 at the design of the guide, T171 to T174 by the design-stage review of the guide, T175 and T176 by the design-stage review of one opt-in for every agent, T177 to T182 by the second design-stage review of the guide, T183 by the final review of its build, T184 by its implementation-stage review, T185 to T189 at the design of the walking skeleton and T190 to T194 by its design-stage review, and T195 to T197 at the design of the specs' citation sweep and T198 to T200 by its design-stage review; they follow T37, each under a heading for its boundary, so that the numbers stay in order, and a threat that a change removes keeps its ID out of use (see Retired IDs).
~~~~

Clause, the new unit:

~~~~text
T38 to T69 were found by the design-stage review, T70 to T78 by the design-stage review of the decision records in `docs/decisions/`, T79 to T81 by the implementation-stage review of those records and their checks, T82 to T100 by the design-stage review of the assumptions, the glossary and the golden set, T101 by the implementation-stage review of the assumptions, T102 and T103 by the implementation-stage review of the glossary, T104 to T116 at the design of the revision of consent, the store and the ledger's format, T117 and T118 by the design-stage review of that revision, T119 to T122 by the review of that revision after its approval, T123 with the owner's answer to a question that the check of that review's fixes raised, T124 to T126 by the design-stage review of the test of the specs' form, T127 by the implementation-stage review of that test, T128 to T135 at the design of the plugin that brings capture to a project's cloud threads, T136 to T142 by the design-stage review of that plugin, T143 by its implementation-stage review, T144 by its security review, T145 to T147 at the design of the README's short start, T148 to T156 by the design-stage review of that short start, T157 and T158 by its implementation-stage review, T159 to T162 at the design of the roadmap, T163 to T165 by the design-stage review of the roadmap, T166 to T168 at the design of the backlog, T169 by the design-stage review of the backlog, T170 at the design of the guide, T171 to T174 by the design-stage review of the guide, T175 and T176 by the design-stage review of one opt-in for every agent, T177 to T182 by the second design-stage review of the guide, T183 by the final review of its build, T184 by its implementation-stage review,
~~~~

Clause, the new unit:

~~~~text
and
~~~~

Clause, the new unit:

~~~~text
T185 to T189 at the design of the walking skeleton and T190 to T194
~~~~

Clause, the new unit:

~~~~text
by its design-stage review; they follow T37, each under a heading for its boundary, so that the numbers stay in order, and a threat that a change removes keeps its ID out of use (see Retired IDs).
~~~~

### Entry

Old:

~~~~text
| 2 medium | T4, T6, T11, T13, T18, T25, T26, T38, T41, T42, T53, T55, T56, T57, T60, T69, T70, T76, T78, T79, T80, T81, T84, T85, T86, T87, T88, T89, T90, T91, T97, T98, T99, T100, T101, T102, T104, T105, T109, T112, T115, T124, T126, T127, T135, T139, T146, T149, T152, T153, T155, T156, T157, T162, T172, T173, T179, T181, T182, T185, T189, T191, T193, T194 | T3, T9, T10, T17, T19, T20, T21, T22, T27, T30, T39, T40, T44, T45, T47, T48, T49, T50, T51, T52, T54, T71, T72, T74, T75, T96, T111, T116, T120, T121, T122, T123, T129, T130, T131, T134, T136, T143, T145, T154, T158, T159, T161, T166, T168, T170, T171, T176 | T7, T8, T16, T128 |
~~~~

New:

~~~~text
| 2 medium | T4, T6, T11, T13, T18, T25, T26, T38, T41, T42, T53, T55, T56, T57, T60, T69, T70, T76, T78, T79, T80, T81, T84, T85, T86, T87, T88, T89, T90, T91, T97, T98, T99, T100, T101, T102, T104, T105, T109, T112, T115, T124, T126, T127, T135, T139, T146, T149, T152, T153, T155, T156, T157, T162, T172, T173, T179, T181, T182, T185, T189, T191, T193, T194, T195, T197, T196, T198, T199, T200 | T3, T9, T10, T17, T19, T20, T21, T22, T27, T30, T39, T40, T44, T45, T47, T48, T49, T50, T51, T52, T54, T71, T72, T74, T75, T96, T111, T116, T120, T121, T122, T123, T129, T130, T131, T134, T136, T143, T145, T154, T158, T159, T161, T166, T168, T170, T171, T176 | T7, T8, T16, T128 |
~~~~

Clause, the new unit:

~~~~text
| 2 medium | T4, T6, T11, T13, T18, T25, T26, T38, T41, T42, T53, T55, T56, T57, T60, T69, T70, T76, T78, T79, T80, T81, T84, T85, T86, T87, T88, T89, T90, T91, T97, T98, T99, T100, T101, T102, T104, T105, T109, T112, T115, T124, T126, T127, T135, T139, T146, T149, T152, T153, T155, T156, T157, T162, T172, T173, T179, T181, T182, T185, T189, T191, T193,
~~~~

Clause, the new unit:

~~~~text
T194
~~~~

Clause, the new unit:

~~~~text
| T3, T9, T10, T17, T19, T20, T21, T22, T27, T30, T39, T40, T44, T45, T47, T48, T49, T50, T51, T52, T54, T71, T72, T74, T75, T96, T111, T116, T120, T121, T122, T123, T129, T130, T131, T134, T136, T143, T145, T154, T158, T159, T161, T166, T168, T170, T171, T176 | T7, T8, T16, T128 |
~~~~

### Entry

Old:

~~~~text
- **Answer:** `CLAUDE.md` says that a page that states behaviour today is brought to the rule only through backlog item B-022, and that a page that a requirement obliges to tell its readers something tells them and cites that requirement. That item's pull request shows, for each sentence that it removes, the scenario that holds it or the spec that it moved into, as the answer to T78 showed for the design's sentences, and the item rests on this threat (DR-232).
~~~~

New:

~~~~text
- **Answer:** `CLAUDE.md` says that a page that states behaviour today is brought to the rule only through backlog item B-022, and that a page that a requirement obliges to tell its readers something tells them and cites that requirement. That item's pull request shows, for each unit of a page that it removes or rewrites, where each of its clauses now is, in a mapping that its committed script checks against the base and the head and that the review runs again (design decision 19, T198), writes nothing into the specs, and changes no check (DR-251). DR-250 is named here because it lists this threat, not because it holds the answer.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** `CLAUDE.md` says that a page that states behaviour today is brought to the rule only through backlog item B-022, and that a page that a requirement obliges to tell its readers something tells them and cites that requirement. That item's pull request shows, for each
~~~~

Clause, changed, design decision 19 replaces the moves into specs, after the threat review at design, with a mapping of every clause that a committed script checks; T198 replaces T78 as the precedent:

~~~~text
sentence that it removes, the scenario that holds it or the spec that it moved into, as the answer to T78 showed for the design's sentences,
~~~~

Clause, DR-232:

~~~~text
and the item rests on this threat (DR-232).
~~~~

### Entry

Old:

~~~~text
- **Held by:** DR-232; `CLAUDE.md`; `add-pr-cost-calculator` task 1.28
~~~~

New:

~~~~text
- **Held by:** DR-232; DR-250; DR-251; `CLAUDE.md`; `add-pr-cost-calculator` task 1.28; `add-pr-cost-calculator` task 1.37
~~~~

Clause, the new unit:

~~~~text
- **Held by:** DR-232;
~~~~

Clause, the new unit:

~~~~text
`CLAUDE.md`; `add-pr-cost-calculator` task 1.28
~~~~

### Entry

Old:

~~~~text
- **Answer:** entries are built from typed values only. A count is copied as a number. The only text taken from a transcript is the model's name and the values of the price attributes, each only when the price table that the hook ships with lists it, or else recorded as `unknown`, because a private gateway, a custom model or an alias can have a name that looks like one of Anthropic's. Tool names, including MCP server names, which can name a private service, are read only to choose the activity type and are never written.
~~~~

New:

~~~~text
- **Answer:** entries are built from typed values only. A count is copied as a number. The only text taken from a transcript is the model's name and the values of the price attributes (R4), each only when the price table that the hook ships with lists it (R77), because a private gateway, a custom model or an alias can have a name that looks like one of Anthropic's. Tool names, including MCP server names, which can name a private service, are never written (R6).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** entries are built from typed values only. A count is copied as a number. The only text taken from a transcript is the model's name and the values of the price attributes
~~~~

Clause, the new unit:

~~~~text
each only when the price table that the hook ships with lists it
~~~~

Clause, R77:

~~~~text
or else recorded as `unknown`
~~~~

Clause, the new unit:

~~~~text
because a private gateway, a custom model or an alias can have a name that looks like one of Anthropic's. Tool names, including MCP server names, which can name a private service, are
~~~~

Clause, R6:

~~~~text
read only to choose the activity type and
~~~~

Clause, the new unit:

~~~~text
are never written
~~~~

### Entry

Old:

~~~~text
- **Answer:** for a run of the hook file's registration, this repository is the one that holds the project directory that Claude Code gives the hook, whatever directory the hook runs in, and a run of the plugin works on each repository that it meets, as this repository, recording in each only the calls made from it (T129). Capture records only the calls whose transcript line gives a working directory in this repository, meaning one whose git common directory, as git finds it from that directory when the run reads the call, is this repository's. Calls made in another repository, in a separate repository nested inside this one's folder, or in a folder that contains this one, are not recorded here, and neither is a call whose lines give no working directory, or whose directory is gone by the time a run reads it, as a removed worktree's is, or names no repository that git can tell, which the session's next ledger file flags, with no count, when the line gives no directory, or one inside this repository's folder or one that holds it (T128). Every git command that the step starts runs without the session's variables whose names begin with `GIT_`, so that the session's environment can neither move a call into this repository nor move the store or a staged ledger file into another one (T119). A call's directory alone tells its repository and worktree: never what the call reads or writes, and never its branch, which is the one checked out in that worktree when the call is recorded.
~~~~

New:

~~~~text
- **Answer:** for a run of the hook file's registration, this repository is the one that holds the project directory that Claude Code gives the hook (R76), and a run of the plugin works on each repository that it meets, as this repository, recording in each only the calls made from it (R180, T129). Capture records only the calls whose transcript line gives a working directory in this repository (R3, R147). The calls that are not recorded here, and those of them that the session's next ledger file flags, with no count, are as R3, R147 and R155 state (T128). Every git command that the step starts runs without the session's variables whose names begin with `GIT_`, so that the session's environment can neither move a call into this repository nor move the store or a staged ledger file into another one (R169, T119). A call's directory alone tells its repository and worktree (R147): never what the call reads or writes, and never its branch, which is the one checked out in that worktree when the call is recorded.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** for a run of the hook file's registration, this repository is the one that holds the project directory that Claude Code gives the hook
~~~~

Clause, R76:

~~~~text
whatever directory the hook runs in
~~~~

Clause, the new unit:

~~~~text
and a run of the plugin works on each repository that it meets, as this repository, recording in each only the calls made from it
~~~~

Clause, the new unit:

~~~~text
T129). Capture records only the calls whose transcript line gives a working directory in this repository
~~~~

Clause, R3:

~~~~text
meaning one whose git common directory
~~~~

Clause, R147:

~~~~text
as git finds it from that directory when the run reads the call
~~~~

Clause, R3:

~~~~text
is this repository's
~~~~

Clause, R3:

~~~~text
Calls made in another repository, in a separate repository nested inside this one's folder, or in a folder that contains this one, are not recorded here, and neither is a call whose lines give no working directory
~~~~

Clause, R147:

~~~~text
or whose directory is gone by the time a run reads it, as a removed worktree's is, or names no repository that git can tell
~~~~

Clause, R155:

~~~~text
which the session's next ledger file flags, with no count
~~~~

Clause, R155:

~~~~text
when the line gives no directory, or one inside this repository's folder or one that holds it
~~~~

Clause, the new unit:

~~~~text
T128). Every git command that the step starts runs without the session's variables whose names begin with `GIT_`, so that the session's environment can neither move a call into this repository nor move the store or a staged ledger file into another one
~~~~

Clause, the new unit:

~~~~text
T119). A call's directory alone tells its repository and worktree
~~~~

Clause, the new unit:

~~~~text
never what the call reads or writes, and never its branch, which is the one checked out in that worktree when the call is recorded
~~~~

### Entry

Old:

~~~~text
- **Answer:** capture also needs the opt-in, in the global git configuration where the session runs, which the person sets, or the setup script of the cloud environment that they use (T134), and which is not part of the repository, and having the plugin opts no one in, however it came to the session. It is read from the person's global configuration files, `~/.gitconfig` and git's file in their XDG configuration folder, and not from files that they include, which can lie in a repository's folder. That folder is taken from `XDG_CONFIG_HOME` only when it holds an absolute path, since git reads a relative one from its current directory, which can be in a repository's folder too. The person's opt-in is read as git reads it: the last value in a file decides, git's spellings of the section and key count, and a subsection or a comment does not, though only `true`, `yes`, `on`, `1` and the bare key opt a person in, where git also reads other numbers as true. The environment variables that a repository's Claude Code settings could set, to point git at a file that opts everyone in or to add the opt-in key, are ignored, and a repository's own git configuration can turn it off but not on. Once that reading finds both switches on, the step also asks git for each value of the key that git reads in the repository, twice, in the session's environment and without its `GIT_` variables, and takes capture to be off when either answer does not come within the run's time budget or gives no value or a refusal, when its last value is not true, or when the last value of any file in it other than the person's two global configuration files, or of the variables, is not true, so an included file, a conditional include or those variables can turn capture off but never on, no value that git reads later undoes such an opt-out, and no variable that changes which files git reads, or for which repository, hides one (T119). The opt-in's feature page, and the README's section on adopting the tool that task 4.4 writes, say what is published when capture is on, that one opt-in covers every repository that turns the tool on, how a person turns capture off for a folder with git's own conditional includes, and where that stops (T121). Removing the setup script's line, or using another environment, reaches only the sessions that start, or whose machines are rebuilt, afterwards, so the README's section on turning capture off gives the opt-outs that reach a session that is running: `git config --global pr-cost.capture false` there, and on the environment the three `GIT_CONFIG_` variables that set the key to false, which each of its sessions reads at its next restore, what can undo each, and how to see a session's opt-in, where it comes from and which hooks run.
~~~~

New:

~~~~text
- **Answer:** capture also needs the opt-in, which the person sets, or the setup script of the cloud environment that they use (T134), and which is not part of the repository (R1), and having the plugin opts no one in (R182). It is read from the person's global configuration files, `~/.gitconfig` and git's file in their XDG configuration folder, and not from files that they include, which can lie in a repository's folder (R37). That folder is taken from `XDG_CONFIG_HOME` only when it holds an absolute path (R103), since git reads a relative one from its current directory, which can be in a repository's folder too. The person's opt-in is read as git reads it (R38), though only some of git's true values opt a person in (R106). The environment variables that a repository's Claude Code settings could set, to point git at a file that opts everyone in or to add the opt-in key, are ignored (R37), and a repository's own git configuration can turn it off but not on (R1, R39). Once that reading finds both switches on, the step also asks git for each value of the key that git reads in the repository, twice, in the session's environment and without its `GIT_` variables (R160), so an included file, a conditional include or those variables can turn capture off but never on, no value that git reads later undoes such an opt-out, and no variable that changes which files git reads, or for which repository, hides one (T119). The opt-in's feature page, and the README's section on adopting the tool that task 4.4 writes, say what is published when capture is on, that one opt-in covers every repository that turns the tool on, how a person turns capture off for a folder with git's own conditional includes, and where that stops (R164, T121). Removing the setup script's line, or using another environment, reaches only the sessions that start, or whose machines are rebuilt, afterwards, so the README's section on turning capture off gives the opt-outs that reach a session that is running: `git config --global pr-cost.capture false` there, and on the environment the three `GIT_CONFIG_` variables that set the key to false, which each of its sessions reads at its next restore, what can undo each, and how to see a session's opt-in, where it comes from and which hooks run (R194).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** capture also needs the opt-in
~~~~

Clause, R1:

~~~~text
in the global git configuration where the session runs
~~~~

Clause, the new unit:

~~~~text
which the person sets, or the setup script of the cloud environment that they use (T134), and which is not part of the repository
~~~~

Clause, the new unit:

~~~~text
and having the plugin opts no one in
~~~~

Clause, R182:

~~~~text
however it came to the session
~~~~

Clause, the new unit:

~~~~text
It is read from the person's global configuration files, `~/.gitconfig` and git's file in their XDG configuration folder, and not from files that they include, which can lie in a repository's folder
~~~~

Clause, the new unit:

~~~~text
That folder is taken from `XDG_CONFIG_HOME` only when it holds an absolute path
~~~~

Clause, the new unit:

~~~~text
since git reads a relative one from its current directory, which can be in a repository's folder too. The person's opt-in is read as git reads it
~~~~

Clause, R38:

~~~~text
the last value in a file decides, git's spellings of the section and key count, and a subsection or a comment does not
~~~~

Clause, the new unit:

~~~~text
though only
~~~~

Clause, R106:

~~~~text
`true`, `yes`, `on`, `1` and the bare key
~~~~

Clause, the new unit:

~~~~text
opt a person in
~~~~

Clause, R106:

~~~~text
where git also reads other numbers as true
~~~~

Clause, the new unit:

~~~~text
The environment variables that a repository's Claude Code settings could set, to point git at a file that opts everyone in or to add the opt-in key, are ignored
~~~~

Clause, the new unit:

~~~~text
and a repository's own git configuration can turn it off but not on
~~~~

Clause, the new unit:

~~~~text
Once that reading finds both switches on, the step also asks git for each value of the key that git reads in the repository, twice, in the session's environment and without its `GIT_` variables
~~~~

Clause, R160:

~~~~text
and takes capture to be off when either answer does not come within the run's time budget or gives no value or a refusal, when its last value is not true, or when the last value of any file in it other than the person's two global configuration files, or of the variables, is not true
~~~~

Clause, the new unit:

~~~~text
so an included file, a conditional include or those variables can turn capture off but never on, no value that git reads later undoes such an opt-out, and no variable that changes which files git reads, or for which repository, hides one (T119). The opt-in's feature page, and the README's section on adopting the tool that task 4.4 writes, say what is published when capture is on, that one opt-in covers every repository that turns the tool on, how a person turns capture off for a folder with git's own conditional includes, and where that stops
~~~~

Clause, the new unit:

~~~~text
T121). Removing the setup script's line, or using another environment, reaches only the sessions that start, or whose machines are rebuilt, afterwards, so the README's section on turning capture off gives the opt-outs that reach a session that is running: `git config --global pr-cost.capture false` there, and on the environment the three `GIT_CONFIG_` variables that set the key to false, which each of its sessions reads at its next restore, what can undo each, and how to see a session's opt-in, where it comes from and which hooks run
~~~~

### Entry

Old:

~~~~text
- **Answer:** a call is identified by a SHA-256 hash of its message id, kept only so that no call is recorded twice. No session value, transcript path, `tool_use_id`, path, working directory, user name or branch name, nor a hash of any of them, is written into an entry or a ledger file, and a ledger file's name is random, so that neither an entry nor a file's path carries one. The store, which is never committed, keeps a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` only where capture needs them, and only as hashes, but for the ledger file's path and its worktree's name in the note of a staged or taken-back ledger file, and its transcript's path, which carries the session's id, in the note of a staged one, until it is resolved. It keeps the fingerprint of the configuration files only as a hash, with no path, and nothing from it reaches a ledger file, a comment or standard error.
~~~~

New:

~~~~text
- **Answer:** a call is identified by a SHA-256 hash of its message id, kept only so that no call is recorded twice (R2, R41). No identifier, nor a hash of one, is written into an entry or a ledger file (R4), and a ledger file's name is random (R10), so that neither an entry nor a file's path carries one. The store, which is never committed, keeps only what capture needs (R149). It keeps the fingerprint of the configuration files only as a hash (R107), and nothing from it reaches a ledger file, a comment or standard error (R4, R89).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a call is identified by a SHA-256 hash of its message id, kept only so that no call is recorded twice
~~~~

Clause, the new unit:

~~~~text
No
~~~~

Clause, R4:

~~~~text
session value, transcript path, `tool_use_id`, path, working directory, user name or branch name
~~~~

Clause, the new unit:

~~~~text
nor a hash of
~~~~

Clause, R4:

~~~~text
any of them
~~~~

Clause, the new unit:

~~~~text
is written into an entry or a ledger file
~~~~

Clause, the new unit:

~~~~text
and a ledger file's name is random
~~~~

Clause, the new unit:

~~~~text
so that neither an entry nor a file's path carries one. The store, which is never committed, keeps
~~~~

Clause, R149:

~~~~text
a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` only where capture needs them, and only as hashes, but for the ledger file's path and its worktree's name in the note of a staged or taken-back ledger file, and its transcript's path, which carries the session's id, in the note of a staged one, until it is resolved
~~~~

Clause, the new unit:

~~~~text
It keeps the fingerprint of the configuration files only as a hash
~~~~

Clause, R107:

~~~~text
with no path
~~~~

Clause, the new unit:

~~~~text
and nothing from it reaches a ledger file, a comment or standard error
~~~~

### Entry

Old:

~~~~text
- **Answer:** an entry records the UTC day only, which is all that pricing needs.
~~~~

New:

~~~~text
- **Answer:** an entry records the UTC day only (R2), which is all that pricing needs.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** an entry records the UTC day only
~~~~

Clause, the new unit:

~~~~text
which is all that pricing needs
~~~~

### Entry

Old:

~~~~text
- **Answer:** every count must be a whole number from zero up to a documented ceiling, and a count at the ceiling is recorded while one above it, or one that is not a number, is refused. `true` and `false` are refused explicitly. A call with a refused value is a refused call: capture records no entry for it, and the ledger counts it as refused, so that the comment can say how many calls capture refused. A hook that succeeds shows its standard error to no one, so the count is kept in the ledger and not printed.
~~~~

New:

~~~~text
- **Answer:** every count must be a whole number from zero up to a documented ceiling, and a call with any other value is refused: capture records no entry for it, and the ledger counts it as refused (R5), so that the comment can say how many calls capture refused (R95). A hook that succeeds shows its standard error to no one, so the count is kept in the ledger and not printed.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** every count must be a whole number from zero up to a documented ceiling
~~~~

Clause, R5:

~~~~text
and a count at the ceiling is recorded while one above it, or one that is not a number, is refused. `true` and `false` are refused explicitly. A call with a refused value is a refused call
~~~~

Clause, the new unit:

~~~~text
capture records no entry for it, and the ledger counts it as refused
~~~~

Clause, the new unit:

~~~~text
so that the comment can say how many calls capture refused
~~~~

Clause, the new unit:

~~~~text
A hook that succeeds shows its standard error to no one, so the count is kept in the ledger and not printed
~~~~

### Entry

Old:

~~~~text
- **Answer:** a call is recorded once, by the hash of its message id, from its lines that give a stop reason. A call with no such line is read from its last line once a later call follows it or its agent has stopped, and the ledger counts those calls, so that the comment can give their number. A call that is not over yet waits for a later run. A call whose final lines disagree is refused rather than guessed at.
~~~~

New:

~~~~text
- **Answer:** a call is recorded once, by the hash of its message id, from its lines that give a stop reason (R2, R41). A call with no such line is read from its last line once it is over, and the ledger counts those calls (R42), so that the comment can give their number (R95). A call whose final lines disagree is refused rather than guessed at (R41).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a call is recorded once, by the hash of its message id, from its lines that give a stop reason
~~~~

Clause, the new unit:

~~~~text
A call with no such line is read from its last line once
~~~~

Clause, R42:

~~~~text
a later call follows it or its agent has stopped
~~~~

Clause, the new unit:

~~~~text
and the ledger counts those calls
~~~~

Clause, the new unit:

~~~~text
so that the comment can give their number
~~~~

Clause, R42:

~~~~text
A call that is not over yet waits for a later run
~~~~

Clause, the new unit:

~~~~text
A call whose final lines disagree is refused rather than guessed at
~~~~

### Entry

Old:

~~~~text
- **Answer:** capture runs before and after each of the agent's Bash commands that the hook's condition `Bash(git *)` matches, and when a turn, a subagent, a failed turn or the session ends. It stages for a `git commit` in the repository that holds the session's project directory, or, for a run of the plugin, in the repository where the commit runs, which that run works on first (T19), including one whose command stages its own files first, one made with `-a`, and one whose message comes from a here-document whose delimiter is quoted, and recognises it whatever options git is given first, and when a later option undoes one that would make it a dry run. So each commit it stages for carries the calls recorded on its branch up to that moment, including those of the turn that commits. A call that one run missed is recorded by a later one, and neither an ignore rule nor a sparse checkout can drop the ledger file.
~~~~

New:

~~~~text
- **Answer:** capture runs before and after each of the agent's Bash commands that the hook's condition `Bash(git *)` matches, and when a turn, a subagent, a failed turn or the session ends (R7). It stages for a `git commit` in the repository that holds the session's project directory, or, for a run of the plugin, in the repository where the commit runs, which that run works on first (R76, R180, T19), in each form of a commit that R8, R48, R79, R80 and R84 state. So each commit it stages for carries the calls recorded on its branch up to that moment, including those of the turn that commits (R81). A call that one run missed is recorded by a later one (R42), and neither an ignore rule nor a sparse checkout can drop the ledger file (R50).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** capture runs before and after each of the agent's Bash commands that the hook's condition `Bash(git *)` matches, and when a turn, a subagent, a failed turn or the session ends
~~~~

Clause, the new unit:

~~~~text
It stages for a `git commit` in the repository that holds the session's project directory, or, for a run of the plugin, in the repository where the commit runs, which that run works on first
~~~~

Clause, the new unit:

~~~~text
T19
~~~~

Clause, R8:

~~~~text
including one whose command stages its own files first
~~~~

Clause, R84:

~~~~text
one made with `-a`
~~~~

Clause, R48:

~~~~text
and one whose message comes from a here-document whose delimiter is quoted
~~~~

Clause, R79:

~~~~text
and recognises it whatever options git is given first
~~~~

Clause, R80:

~~~~text
and when a later option undoes one that would make it a dry run
~~~~

Clause, the new unit:

~~~~text
So each commit it stages for carries the calls recorded on its branch up to that moment, including those of the turn that commits
~~~~

Clause, the new unit:

~~~~text
A call that one run missed is recorded by a later one
~~~~

Clause, the new unit:

~~~~text
and neither an ignore rule nor a sparse checkout can drop the ledger file
~~~~

### Entry

Old:

~~~~text
- **Answer:** capture records these attributes where the transcript gives them. Pricing applies every modifier the price table lists, the fast-speed premium and service-tier rates among them, combined as the table states, and names, rather than guesses, any value or combination it has no price for. Web fetches are listed at no charge, so a call that made them is still priced.
~~~~

New:

~~~~text
- **Answer:** capture records these attributes where the transcript gives them (R2). Pricing applies every modifier the price table lists, combined as the table states (R16), and names, rather than guesses, any value or combination it has no price for (R61). Web fetches are listed at no charge, so a call that made them is still priced.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** capture records these attributes where the transcript gives them
~~~~

Clause, the new unit:

~~~~text
Pricing applies every modifier the price table lists
~~~~

Clause, R16:

~~~~text
the fast-speed premium and service-tier rates among them
~~~~

Clause, the new unit:

~~~~text
combined as the table states
~~~~

Clause, the new unit:

~~~~text
and names, rather than guesses, any value or combination it has no price for
~~~~

Clause, the new unit:

~~~~text
Web fetches are listed at no charge, so a call that made them is still priced
~~~~

### Entry

Old:

~~~~text
- **Answer:** a ledger file's name is random and is created only if no file of that name exists, and capture refuses to write through any path with a symbolic link in a folder below the repository root. The branch name plays no part in the path.
~~~~

New:

~~~~text
- **Answer:** a ledger file's name is random and is created only if no file of that name exists, and capture refuses to write through any path with a symbolic link in a folder below the repository root (R10). The branch name plays no part in the path (R4).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a ledger file's name is random and is created only if no file of that name exists, and capture refuses to write through any path with a symbolic link in a folder below the repository root
~~~~

Clause, the new unit:

~~~~text
The branch name plays no part in the path
~~~~

### Entry

Old:

~~~~text
- **Answer:** the step stages exactly the ledger file it wrote.
~~~~

New:

~~~~text
- **Answer:** the step stages exactly the ledger file it wrote (R56).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the step stages exactly the ledger file it wrote
~~~~

### Entry

Old:

~~~~text
- **Answer:** each ledger file is written once, whole, under a new random name, so no two runs or branches write the same file, and runs at the same time keep every note whole and record no call twice, since a run holds the store's lock from when it reads the store until it has written it. The store lives in the repository's git common directory, which every worktree shares.
~~~~

New:

~~~~text
- **Answer:** each ledger file is written once, whole, under a new random name, so no two runs or branches write the same file (R10), and runs at the same time keep every note whole and record no call twice (R11), since a run holds the store's lock from when it reads the store until it has written it. The store lives in the repository's git common directory, which every worktree shares.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each ledger file is written once, whole, under a new random name, so no two runs or branches write the same file
~~~~

Clause, the new unit:

~~~~text
and runs at the same time keep every note whole and record no call twice
~~~~

Clause, the new unit:

~~~~text
since a run holds the store's lock from when it reads the store until it has written it. The store lives in the repository's git common directory, which every worktree shares
~~~~

### Entry

Old:

~~~~text
- **Answer:** the registered command ends in `; exit 0`, which `sh`, Git Bash and PowerShell all read, rather than `|| true`, which Windows PowerShell 5.1 does not, so it exits with success even when its script cannot be read or started, in each shell that Claude Code runs it in, and the plugin's command does the same. The step prints nothing on standard output, at a session's start too, and no git command it starts prints there either, and its messages on standard error are its own words and numbers, never text from the transcript or the ledger. Claude never sees the standard error of a hook that succeeds. The command has a short timeout, which the plugin's hooks share with the hook file's registration, and the step stops at a time budget inside it, leaving the rest for a later run. It stops a reading of the opt-in that has not finished by then, and takes capture to be off for that run.
~~~~

New:

~~~~text
- **Answer:** the registered command ends in `; exit 0`, which `sh`, Git Bash and PowerShell all read, rather than `|| true`, which Windows PowerShell 5.1 does not, so it exits with success even when its script cannot be read or started (R13), and the plugin's command does the same (R179). The step prints nothing on standard output, and no git command it starts prints there either (R13, R148), and its messages on standard error are its own words and numbers (R89). Claude never sees the standard error of a hook that succeeds. The command has a short timeout, which the plugin's hooks share with the hook file's registration (R179), and the step stops at a time budget inside it (R90). It stops a reading of the opt-in that has not finished by then, and takes capture to be off for that run (R160).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the registered command ends in `; exit 0`, which `sh`, Git Bash and PowerShell all read, rather than `|| true`, which Windows PowerShell 5.1 does not, so it exits with success even when its script cannot be read or started
~~~~

Clause, R13:

~~~~text
in each shell that Claude Code runs it in
~~~~

Clause, the new unit:

~~~~text
and the plugin's command does the same
~~~~

Clause, the new unit:

~~~~text
The step prints nothing on standard output
~~~~

Clause, R148:

~~~~text
at a session's start too
~~~~

Clause, the new unit:

~~~~text
and no git command it starts prints there either
~~~~

Clause, the new unit:

~~~~text
and its messages on standard error are its own words and numbers
~~~~

Clause, R89:

~~~~text
never text from the transcript or the ledger
~~~~

Clause, the new unit:

~~~~text
Claude never sees the standard error of a hook that succeeds. The command has a short timeout, which the plugin's hooks share with the hook file's registration
~~~~

Clause, the new unit:

~~~~text
and the step stops at a time budget inside it
~~~~

Clause, R90:

~~~~text
leaving the rest for a later run
~~~~

Clause, the new unit:

~~~~text
It stops a reading of the opt-in that has not finished by then, and takes capture to be off for that run
~~~~

### Entry

Old:

~~~~text
- **Answer:** the registered command runs Python in isolated mode (`python3 -I`), which leaves the script's folder, the current directory and Python's environment variables out of the import path.
~~~~

New:

~~~~text
- **Answer:** the registered command runs Python in isolated mode (`python3 -I`), which leaves the script's folder, the current directory and Python's environment variables out of the import path (R12).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the registered command runs Python in isolated mode (`python3 -I`), which leaves the script's folder, the current directory and Python's environment variables out of the import path
~~~~

### Entry

Old:

~~~~text
- **Answer:** between commits, capture keeps its notes in the git common directory and leaves the working tree and the index alone, but for the take-backs and put-backs below. It stages a ledger file only just before the agent's own `git commit`, and only when that commit is a top-level command, not in a pipeline, joined to the rest by `&&`, `;` or line breaks, in the foreground, and nothing comes before it in the command but `cd` to a path written in it and the git commands `add`, `rm`, `mv`, `status`, `diff`, `log` and `show`, with or without git's own options, counting every command or process substitution in the commit or before it, in an argument, an assignment or a redirection, as coming before it unless all it runs is `cat` reading a here-document whose delimiter is quoted, and staging nothing when the commit or a command before it reads a here-document whose delimiter is not. It finds the worktree from the current directory that the hook's input gives, followed through each top-level `cd` before the commit and the `-C` options given to git before `commit` in the commit's own command, never from where the hook runs, and stages nothing for such a `-C` path that the command does not write out. It stages nothing for a commit that would otherwise be empty when no `git add`, `git rm` or `git mv` comes before it, for a dry run, in any spelling that git accepts, for a commit of named paths, for a command that only names a commit, after a `git rm` or `git mv` that is given a `-C` path not written out, or names, read from where it runs, the ledger file's folder, a folder above it, a path with a wildcard or other pathspec magic, or a path not written out, when no call is waiting, when the ledger path has a filter or a working-tree encoding, or when git refuses to add the file, which it then removes, and it stages through ignore rules and sparse checkouts. A run that comes again before the same command, as for a deferred call, stages nothing new while that command's file is still staged and its branch still checked out, and takes the file back first when that branch is not. The run after that command takes the file back if no commit took it. For a command that gets no such run, any later run, from that session or another, does once it finds the command over, as the run when the session ends does for that session's commands, which, for the plugin, takes back before it reads any transcript, within the shorter budget that Claude Code gives a plugin's `SessionEnd` hooks. A take-back never removes a file from a worktree whose checked-out commit holds it, and leaves the file while another git command holds that worktree's index lock. Runs take back and put back what they can before they read any transcript. Every take-back notes the commit it found checked out there, which did not hold the file, and whether it removed the file from the index, the working tree or both, and the first later run there that finds another commit checked out and the index free puts the file back, as that commit holds it, when that commit holds it: into the index, when the take-back removed it from there and the index lacks it, and then into the working tree, when the take-back removed it from there, the index holds it as that commit does and the working tree lacks it. That run then forgets the note, and the step puts back no file in any other case. Once a run has found a commit holding a ledger file, the step never stages its calls again in that run's clone, so that in that clone a ledger file that anyone removes after that takes its calls with it, and the step never takes the file back, but leaves it to git, wherever git leaves it, as git leaves the other changes of a commit that a reset undoes. Apart from staging, taking back and putting back, no run touches the index. The ledger names its hash field so that detect-secrets, a common secret scanner, reads the hash as an identifier, and the README tells adopters to exclude `.pr-cost/` from their own git hooks before they turn the tool on.
~~~~

New:

~~~~text
- **Answer:** between commits, capture keeps its notes in the git common directory and leaves the working tree and the index alone, but for the take-backs and put-backs below (R47). It stages a ledger file only just before the agent's own `git commit`, and only when that commit stands as R82, R48 and R112 require. It finds the worktree from the current directory that the hook's input gives, never from where the hook runs (R49). It stages nothing for the commits that R79, R80, R83, R84 and R85 name, when no call is waiting (R81), when the ledger path has a filter or a working-tree encoding (R86), or when git refuses to add the file, which it then removes, and it stages through ignore rules and sparse checkouts (R50). A run that comes again before the same command stages nothing new (R51). The run after that command takes the file back if no commit took it (R9). For a command that gets no such run, any later run, from that session or another, does once it finds the command over, as the run when the session ends does for that session's commands (R87, R90). A take-back never removes a file from a worktree whose checked-out commit holds it, and leaves the file while another git command holds that worktree's index lock (R113, R114). Runs take back and put back what they can before they read any transcript. Every take-back is noted (R115), and the first later run there that finds another commit checked out and the index free puts the file back, as that commit holds it, when that commit holds it (R116). That run then forgets the note, and the step puts back no file in any other case (R117). Once a run has found a commit holding a ledger file, the step never stages its calls again in that run's clone (R52), so that in that clone a ledger file that anyone removes after that takes its calls with it, and the step never takes the file back, but leaves it to git, wherever git leaves it, as git leaves the other changes of a commit that a reset undoes (R113). Apart from staging, taking back and putting back, no run touches the index (R47). The ledger names its hash field so that detect-secrets, a common secret scanner, reads the hash as an identifier, and the README tells adopters to exclude `.pr-cost/` from their own git hooks before they turn the tool on.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** between commits, capture keeps its notes in the git common directory and leaves the working tree and the index alone, but for the take-backs and put-backs below
~~~~

Clause, the new unit:

~~~~text
It stages a ledger file only just before the agent's own `git commit`, and only when that commit
~~~~

Clause, R82:

~~~~text
is a top-level command, not in a pipeline, joined to the rest by `&&`, `;` or line breaks, in the foreground, and nothing comes before it in the command but `cd` to a path written in it and the git commands `add`, `rm`, `mv`, `status`, `diff`, `log` and `show`, with or without git's own options
~~~~

Clause, R48:

~~~~text
counting every command or process substitution in the commit or before it, in an argument, an assignment or a redirection, as coming before it unless all it runs is `cat` reading a here-document whose delimiter is quoted
~~~~

Clause, R112:

~~~~text
and staging nothing when the commit or a command before it reads a here-document whose delimiter is not
~~~~

Clause, the new unit:

~~~~text
It finds the worktree from the current directory that the hook's input gives
~~~~

Clause, R49:

~~~~text
followed through each top-level `cd` before the commit and the `-C` options given to git before `commit` in the commit's own command
~~~~

Clause, the new unit:

~~~~text
never from where the hook runs
~~~~

Clause, R49:

~~~~text
and stages nothing for such a `-C` path that the command does not write out
~~~~

Clause, the new unit:

~~~~text
It stages nothing for
~~~~

Clause, R84:

~~~~text
a commit that would otherwise be empty when no `git add`, `git rm` or `git mv` comes before it
~~~~

Clause, R80:

~~~~text
for a dry run, in any spelling that git accepts
~~~~

Clause, R83:

~~~~text
for a commit of named paths
~~~~

Clause, R79:

~~~~text
for a command that only names a commit
~~~~

Clause, R85:

~~~~text
after a `git rm` or `git mv` that is given a `-C` path not written out, or names, read from where it runs, the ledger file's folder, a folder above it, a path with a wildcard or other pathspec magic, or a path not written out
~~~~

Clause, the new unit:

~~~~text
when no call is waiting
~~~~

Clause, the new unit:

~~~~text
when the ledger path has a filter or a working-tree encoding
~~~~

Clause, the new unit:

~~~~text
or when git refuses to add the file, which it then removes, and it stages through ignore rules and sparse checkouts
~~~~

Clause, the new unit:

~~~~text
A run that comes again before the same command
~~~~

Clause, R51:

~~~~text
as for a deferred call
~~~~

Clause, the new unit:

~~~~text
stages nothing new
~~~~

Clause, R51:

~~~~text
while that command's file is still staged and its branch still checked out, and takes the file back first when that branch is not
~~~~

Clause, the new unit:

~~~~text
The run after that command takes the file back if no commit took it
~~~~

Clause, the new unit:

~~~~text
For a command that gets no such run, any later run, from that session or another, does once it finds the command over, as the run when the session ends does for that session's commands
~~~~

Clause, R90:

~~~~text
which, for the plugin, takes back before it reads any transcript, within the shorter budget that Claude Code gives a plugin's `SessionEnd` hooks
~~~~

Clause, the new unit:

~~~~text
A take-back never removes a file from a worktree whose checked-out commit holds it, and leaves the file while another git command holds that worktree's index lock
~~~~

Clause, the new unit:

~~~~text
Runs take back and put back what they can before they read any transcript. Every take-back
~~~~

Clause, R115:

~~~~text
notes the commit it found checked out there, which did not hold the file, and whether it removed the file from the index, the working tree or both
~~~~

Clause, the new unit:

~~~~text
and the first later run there that finds another commit checked out and the index free puts the file back, as that commit holds it, when that commit holds it
~~~~

Clause, R116:

~~~~text
into the index, when the take-back removed it from there and the index lacks it, and then into the working tree, when the take-back removed it from there, the index holds it as that commit does and the working tree lacks it
~~~~

Clause, the new unit:

~~~~text
That run then forgets the note, and the step puts back no file in any other case
~~~~

Clause, the new unit:

~~~~text
Once a run has found a commit holding a ledger file, the step never stages its calls again in that run's clone
~~~~

Clause, the new unit:

~~~~text
so that in that clone a ledger file that anyone removes after that takes its calls with it, and the step never takes the file back, but leaves it to git, wherever git leaves it, as git leaves the other changes of a commit that a reset undoes
~~~~

Clause, the new unit:

~~~~text
Apart from staging, taking back and putting back, no run touches the index
~~~~

Clause, the new unit:

~~~~text
The ledger names its hash field so that detect-secrets, a common secret scanner, reads the hash as an identifier, and the README tells adopters to exclude `.pr-cost/` from their own git hooks before they turn the tool on
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report holds each line to the ledger format that `docs/ledger-format.md` documents and capture writes: whole counts within the ceiling, never `true`, `false`, not-a-number or a number too large to hold, no field given twice, no field the format does not name, no nesting beyond the format's depth, and a day that is a date. It refuses any line that does not match, and says how many it refused, showing none of them. An entry dated after the day the report runs is refused, an entry older than any price is named and left out of the cost, and entries of one call that differ are all refused. None of these stops the report.
~~~~

New:

~~~~text
- **Answer:** the report holds each line to the ledger format that `docs/ledger-format.md` documents and capture writes (R35). It refuses any line that does not match, and says how many it refused, showing none of them (R97, R102). An entry dated after the day the report runs is refused, an entry older than any price is named and left out of the cost (R14), and entries of one call that differ are all refused (R59). None of these stops the report (R102).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report holds each line to the ledger format that `docs/ledger-format.md` documents and capture writes
~~~~

Clause, R35:

~~~~text
whole counts within the ceiling, never `true`, `false`, not-a-number or a number too large to hold, no field given twice, no field the format does not name, no nesting beyond the format's depth, and a day that is a date
~~~~

Clause, the new unit:

~~~~text
It refuses any line that does not match, and says how many it refused, showing none of them
~~~~

Clause, the new unit:

~~~~text
An entry dated after the day the report runs is refused, an entry older than any price is named and left out of the cost
~~~~

Clause, the new unit:

~~~~text
and entries of one call that differ are all refused
~~~~

Clause, the new unit:

~~~~text
None of these stops the report
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report and capture read ledger files only as blobs from git, never through the working tree, and learn each blob's size before reading it. The report refuses any added path that is not a regular file, and when a pull request's ledger files are together above a documented size bound, counts none of their entries and says they are too large to read, while still reporting the CI cost. Capture skips any path that is not a regular file and any file above that bound, and stops at its time budget.
~~~~

New:

~~~~text
- **Answer:** the report and capture read ledger files only as blobs from git, never through the working tree, and learn each blob's size before reading it, and each keeps to the bounds that R23, R45 and R66 state. Capture stops at its time budget (R90).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report and capture read ledger files only as blobs from git, never through the working tree, and learn each blob's size before reading it
~~~~

Clause, R23:

~~~~text
The report refuses any added path that is not a regular file
~~~~

Clause, R66:

~~~~text
and when a pull request's ledger files are together above a documented size bound, counts none of their entries and says they are too large to read, while still reporting the CI cost
~~~~

Clause, R45:

~~~~text
Capture skips any path that is not a regular file and any file above that bound
~~~~

Clause, the new unit:

~~~~text
and
~~~~

Clause, the new unit:

~~~~text
stops at its time budget
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report counts only the entries of ledger files that the merge adds, does not count an entry whose call the default branch already held before the merge, and counts a call that the pull request adds twice once. So a call recorded on two branches is counted once, for whichever pull request merges first, and a resumed session records nothing again that its own branch already holds, and in a fresh clone, which holds no store, records no call that answers a line written before its first run there. Capture runs before each of the agent's Bash commands that the hook's condition `Bash(git *)` matches, so a call that the transcript holds as over by then is recorded before the command can change the branch, unless that run reaches its time budget before it reads the call, and a run of the plugin works first on the repository where the command runs, so that a command that changes another repository's branch, as `git -C` can, finds that repository's calls recorded first. A push whose commits do not all belong to one pull request, or that merges none, gets no comment, and its job summary says why. This rests on GitHub's lookup of the pull requests associated with a commit behaving as documented (A49).
~~~~

New:

~~~~text
- **Answer:** the report counts only the entries of ledger files that the merge adds (R58), and each call at most once (R59). So a call recorded on two branches is counted once, for whichever pull request merges first, and a resumed session records nothing again that its own branch already holds (R2), and in a fresh clone, which holds no store, records no call that answers a line written before its first run there (R52). Capture runs before each of the agent's Bash commands that the hook's condition `Bash(git *)` matches, so a call that the transcript holds as over by then is recorded before the command can change the branch (R7), and a run of the plugin works first on the repository where the command runs, so that a command that changes another repository's branch, as `git -C` can, finds that repository's calls recorded first (R180). A push whose commits do not all belong to one pull request, or that merges none, gets no comment, and its job summary says why (R69). This rests on GitHub's lookup of the pull requests associated with a commit behaving as documented (A49).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report counts only the entries of ledger files that the merge adds
~~~~

Clause, R59:

~~~~text
does not count an entry whose call the default branch already held before the merge, and counts a call that the pull request adds twice once
~~~~

Clause, the new unit:

~~~~text
So a call recorded on two branches is counted once, for whichever pull request merges first, and a resumed session records nothing again that its own branch already holds
~~~~

Clause, the new unit:

~~~~text
and in a fresh clone, which holds no store, records no call that answers a line written before its first run there
~~~~

Clause, the new unit:

~~~~text
Capture runs before each of the agent's Bash commands that the hook's condition `Bash(git *)` matches, so a call that the transcript holds as over by then is recorded before the command can change the branch
~~~~

Clause, R7:

~~~~text
unless that run reaches its time budget before it reads the call
~~~~

Clause, the new unit:

~~~~text
and a run of the plugin works first on the repository where the command runs, so that a command that changes another repository's branch, as `git -C` can, finds that repository's calls recorded first
~~~~

Clause, the new unit:

~~~~text
A push whose commits do not all belong to one pull request, or that merges none, gets no comment, and its job summary says why
~~~~

Clause, the new unit:

~~~~text
This rests on GitHub's lookup of the pull requests associated with a commit behaving as documented (A49
~~~~

### Entry

Old:

~~~~text
- **Answer:** the deletion or change is in the pull request's diff before it merges. After the merge, its comment says how many earlier ledger files it removed or changed and counts none of their entries, and git history still holds the files as they were. A removal in a push that gets no comment is flagged in that push's job summary instead. A file that comes back later is T47.
~~~~

New:

~~~~text
- **Answer:** the deletion or change is in the pull request's diff before it merges. After the merge, its comment says how many earlier ledger files it removed or changed and counts none of their entries (R119), and git history still holds the files as they were. A removal in a push that gets no comment is flagged in that push's job summary instead (R60). A file that comes back later is T47.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the deletion or change is in the pull request's diff before it merges. After the merge, its comment says how many earlier ledger files it removed or changed and counts none of their entries
~~~~

Clause, the new unit:

~~~~text
and git history still holds the files as they were. A removal in a push that gets no comment is flagged in that push's job summary instead
~~~~

Clause, the new unit:

~~~~text
A file that comes back later is T47
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report reads the configuration from the default branch both before and after the merge, and runs if either turns the tool on. When a pull request changes the configuration file or any workflow file, its comment says so, because any workflow can run with the identity that posts the report comment.
~~~~

New:

~~~~text
- **Answer:** the report reads the configuration from the default branch both before and after the merge, and runs if either turns the tool on (R19). When a pull request changes the configuration file or any workflow file, its comment says so (R93), because any workflow can run with the identity that posts the report comment.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report reads the configuration from the default branch both before and after the merge, and runs if either turns the tool on
~~~~

Clause, the new unit:

~~~~text
When a pull request changes the configuration file or any workflow file, its comment says so
~~~~

Clause, the new unit:

~~~~text
because any workflow can run with the identity that posts the report comment
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report reads a pull request's changes from git rather than from those capped lists, fetching the default branch's history up to the push and the pull request's head, since a checkout fetches one commit by default, and its own commits from its head ref, `refs/pull/<number>/head`, whatever the merge method. It counts only the runs on those commits that no push to the default branch started and that were created before the pull request merged, so it leaves out the runs that the merge's push starts, even when they run on one of those commits, as after a fast-forward, whatever their creation times, and it asks for every attempt of every job. A run that the merge starts through another event, such as the pull request's `closed` event, is created at the merge or after it, so the time cut leaves it out (A18). If any data it needs cannot be read in full, or a run it counts has not finished, it marks the figure incomplete instead of presenting part of it as the whole.
~~~~

New:

~~~~text
- **Answer:** the report reads a pull request's changes from git rather than from those capped lists, fetching the default branch's history up to the push and the pull request's head, since a checkout fetches one commit by default (R23). It counts only the pull request's own runs, leaving out those that the merge's push starts (R62, R120), and it asks for every attempt of every job (R62). A run that the merge starts through another event, such as the pull request's `closed` event, is created at the merge or after it, so the time cut leaves it out (A18). If any data it needs cannot be read in full, or a run it counts has not finished, it marks the figure incomplete instead of presenting part of it as the whole (R64).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report reads a pull request's changes from git rather than from those capped lists, fetching the default branch's history up to the push and the pull request's head
~~~~

Clause, the new unit:

~~~~text
since a checkout fetches one commit by default
~~~~

Clause, R62:

~~~~text
and its own commits from its head ref, `refs/pull/<number>/head`, whatever the merge method
~~~~

Clause, the new unit:

~~~~text
It counts only
~~~~

Clause, R62:

~~~~text
the runs on those commits that no push to the default branch started and that were created before the pull request merged
~~~~

Clause, R120:

~~~~text
so it leaves out the runs that the merge's push starts, even when they run on one of those commits, as after a fast-forward, whatever their creation times
~~~~

Clause, the new unit:

~~~~text
and it asks for every attempt of every job
~~~~

Clause, the new unit:

~~~~text
A run that the merge starts through another event, such as the pull request's `closed` event, is created at the merge or after it, so the time cut leaves it out (A18). If any data it needs cannot be read in full, or a run it counts has not finished, it marks the figure incomplete instead of presenting part of it as the whole
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report runs on the push that a merge makes to the default branch, so it runs only after the owner has merged, and refuses every other event, whatever triggered the workflow that calls it: it goes on only when the event is `push` and the ref is `refs/heads/` followed by the default branch's name, so a tag named like the default branch is refused too. It checks out its own code at the commit its caller pins, by the `job` context's workflow repository and commit, and reads the pull request's files only as data, never running, importing or installing anything from them.
~~~~

New:

~~~~text
- **Answer:** the report runs on the push that a merge makes to the default branch, so it runs only after the owner has merged, and refuses every other event, whatever triggered the workflow that calls it (R68). It checks out its own code at the commit its caller pins, by the `job` context's workflow repository and commit, and reads the pull request's files only as data (R24).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report runs on the push that a merge makes to the default branch, so it runs only after the owner has merged, and refuses every other event, whatever triggered the workflow that calls it
~~~~

Clause, R68:

~~~~text
it goes on only when the event is `push` and the ref is `refs/heads/` followed by the default branch's name, so a tag named like the default branch is refused too
~~~~

Clause, the new unit:

~~~~text
It checks out its own code at the commit its caller pins, by the `job` context's workflow repository and commit, and reads the pull request's files only as data
~~~~

Clause, R24:

~~~~text
never running, importing or installing anything from them
~~~~

### Entry

Old:

~~~~text
- **Answer:** the reusable workflow declares only reading the repository and its Actions data and writing pull request comments, which a caller can narrow but not widen. Its checkout does not keep the token, and the report never writes the token to its log, its job summary or its comment. The report connects only to GitHub: to the host in `GITHUB_API_URL`, and by git to the tool's own repository and the repository it reports on, and a test fails on a connection anywhere else, including one that a git command opens.
~~~~

New:

~~~~text
- **Answer:** the reusable workflow declares only the permissions that R24 names, which a caller can narrow but not widen. Its checkout does not keep the token, and the report never writes the token to its output (R24). The report connects only to GitHub (R30), and a test fails on a connection anywhere else, including one that a git command opens.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the reusable workflow declares only
~~~~

Clause, R24:

~~~~text
reading the repository and its Actions data and writing pull request comments
~~~~

Clause, the new unit:

~~~~text
which a caller can narrow but not widen. Its checkout does not keep the token, and the report never writes the token to
~~~~

Clause, R24:

~~~~text
its log, its job summary or its comment
~~~~

Clause, the new unit:

~~~~text
The report connects only to GitHub
~~~~

Clause, R30:

~~~~text
to the host in `GITHUB_API_URL`, and by git to the tool's own repository and the repository it reports on
~~~~

Clause, the new unit:

~~~~text
and a test fails on a connection anywhere else, including one that a git command opens
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report updates only a comment that its own identity wrote.
~~~~

New:

~~~~text
- **Answer:** the report updates only a comment that its own identity wrote (R96).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report updates only a comment that its own identity wrote
~~~~

### Entry

Old:

~~~~text
- **Answer:** the comment holds numbers, its own fixed text, and model, attribute and runner names that the price table lists, shown as code. A ledger line that names a model or an attribute value the table does not list, other than `unknown`, is refused, and a job on a runner the table does not list is counted in minutes and left out of the cost, unnamed. An entry's day reaches the comment only as a date, since a ledger line whose day is not one is refused. Nothing else from the ledger, the pull request or the jobs API reaches the comment. The job summary and the log are T52.
~~~~

New:

~~~~text
- **Answer:** the comment holds only what R21 lists. A ledger line that names a model or an attribute value the table does not list, other than `unknown`, is refused (R98), and a job on a runner the table does not list is counted in minutes and left out of the cost, unnamed (R63). An entry's day reaches the comment only as a date, since a ledger line whose day is not one is refused (R35). Nothing else from the ledger, the pull request or the jobs API reaches the comment (R97). The job summary and the log are T52.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the comment holds
~~~~

Clause, R21:

~~~~text
numbers, its own fixed text, and model, attribute and runner names that the price table lists, shown as code
~~~~

Clause, the new unit:

~~~~text
A ledger line that names a model or an attribute value the table does not list, other than `unknown`, is refused
~~~~

Clause, the new unit:

~~~~text
and a job on a runner the table does not list is counted in minutes and left out of the cost, unnamed
~~~~

Clause, the new unit:

~~~~text
An entry's day reaches the comment only as a date, since a ledger line whose day is not one is refused
~~~~

Clause, the new unit:

~~~~text
Nothing else from the ledger, the pull request or the jobs API reaches the comment
~~~~

Clause, the new unit:

~~~~text
The job summary and the log are T52
~~~~

### Entry

Old:

~~~~text
- **Answer:** the comment says it is an API-equivalent estimate and not a bill, and names the price table's date and the tool's version, so anyone can recompute it from the ledger. When the pull request's ledger files flag calls left out, the comment says so for each reason, as what those files say, and that the token cost, each of its parts and the total are then lower bounds, and it always says that calls that no ledger file holds are neither counted nor flagged.
~~~~

New:

~~~~text
- **Answer:** the comment says what its figure is, and names the price table's date and the tool's version (R94), so anyone can recompute it from the ledger. When the pull request's ledger files flag calls left out, the comment says so (R157).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the comment says
~~~~

Clause, R94:

~~~~text
it is an API-equivalent estimate and not a bill
~~~~

Clause, the new unit:

~~~~text
and names the price table's date and the tool's version
~~~~

Clause, the new unit:

~~~~text
so anyone can recompute it from the ledger. When the pull request's ledger files flag calls left out, the comment says so
~~~~

Clause, R157:

~~~~text
for each reason, as what those files say, and that the token cost, each of its parts and the total are then lower bounds, and it always says that calls that no ledger file holds are neither counted nor flagged
~~~~

### Entry

Old:

~~~~text
- **Answer:** the tool has no runtime dependencies beyond Python's standard library. The hook is one file that imports nothing else, which an adopter copies from the full commit that their calling workflow pins, not from a tag, which can be moved, and checks against the checksum that the README at that commit gives and the hook registration carries, which a test holds to the file's SHA-256; after that, it changes in their repository only through their own review. The actions the tool's workflows use are pinned to commits, the image that one CI job runs git 2.43 in is pinned to its digest, and the README's calling workflow leaves its pin for the adopter to fill with the full commit that a published release of this repository names, never a branch or a tag, while its section on adopting the tool says to take the hook file and its registration from the README at that commit. A release is made only from a commit in the default branch's first-parent history, and only an identity that agent sessions never hold can create a tag (T67). Changes reach `main` only through pull requests that pass CI, and the owner merges them. The plugin reaches a person as a release's zip, which the release's tag rebuilds and whose checksum the README gives (T133), or from this repository's marketplace, which serves only a published release's plugin, as its tag builds it (T132, T137, T138, T140), and the plugin declares nothing but its command hooks, which run the hook file byte for byte (T141). Development tools are pinned to exact versions, with their own dependencies locked and hashed, and Renovate proposes an update that it can date only after it has been out for 14 days, while it lets a vulnerability fix through at once.
~~~~

New:

~~~~text
- **Answer:** the tool has no runtime dependencies beyond Python's standard library (R12). The hook is one file that imports nothing else (R12), which an adopter copies from the full commit that their calling workflow pins, not from a tag, which can be moved, and checks against the checksum that the README at that commit gives and the hook registration carries, which a test holds to the file's SHA-256; after that, it changes in their repository only through their own review. The actions the tool's workflows use are pinned to commits, the image that one CI job runs git 2.43 in is pinned to its digest, and the README's calling workflow leaves its pin for the adopter to fill with the full commit that a published release of this repository names, never a branch or a tag, while its section on adopting the tool says to take the hook file and its registration from the README at that commit (R203). A release is made only from a commit in the default branch's first-parent history (R27), and only an identity that agent sessions never hold can create a tag (T67). Changes reach `main` only through pull requests that pass CI, and the owner merges them. The plugin reaches a person as a release's zip, which the release's tag rebuilds and whose checksum the README gives (R183, T133), or from this repository's marketplace, which serves only a published release's plugin, as its tag builds it (R184, T132, T137, T138, T140), and the plugin declares nothing but its command hooks, which run the hook file byte for byte (R188, T141). Development tools are pinned to exact versions, with their own dependencies locked and hashed, and Renovate proposes an update that it can date only after it has been out for 14 days, while it lets a vulnerability fix through at once (R26).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the tool has no runtime dependencies beyond Python's standard library
~~~~

Clause, the new unit:

~~~~text
The hook is one file that imports nothing else
~~~~

Clause, the new unit:

~~~~text
which an adopter copies from the full commit that their calling workflow pins, not from a tag, which can be moved, and checks against the checksum that the README at that commit gives and the hook registration carries, which a test holds to the file's SHA-256; after that, it changes in their repository only through their own review. The actions the tool's workflows use are pinned to commits, the image that one CI job runs git 2.43 in is pinned to its digest, and the README's calling workflow leaves its pin for the adopter to fill with the full commit that a published release of this repository names, never a branch or a tag, while its section on adopting the tool says to take the hook file and its registration from the README at that commit
~~~~

Clause, the new unit:

~~~~text
A release is made only from a commit in the default branch's first-parent history
~~~~

Clause, the new unit:

~~~~text
and only an identity that agent sessions never hold can create a tag (T67). Changes reach `main` only through pull requests that pass CI, and the owner merges them. The plugin reaches a person as a release's zip, which the release's tag rebuilds and whose checksum the README gives
~~~~

Clause, the new unit:

~~~~text
T133
~~~~

Clause, the new unit:

~~~~text
or from this repository's marketplace, which serves only a published release's plugin, as its tag builds it
~~~~

Clause, the new unit:

~~~~text
T132, T137, T138, T140
~~~~

Clause, the new unit:

~~~~text
and the plugin declares nothing but its command hooks, which run the hook file byte for byte
~~~~

Clause, the new unit:

~~~~text
T141
~~~~

Clause, the new unit:

~~~~text
Development tools are pinned to exact versions, with their own dependencies locked and hashed, and Renovate proposes an update that it can date only after it has been out for 14 days, while it lets a vulnerability fix through at once
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report refuses every event but a push to the default branch, declares the permissions it needs, and asks for no secret. The README's calling workflow grants those permissions only and passes no secrets, and a test holds that snippet.
~~~~

New:

~~~~text
- **Answer:** the report refuses every event but a push to the default branch (R68), declares the permissions it needs, and asks for no secret (R24). The README's calling workflow grants those permissions only and passes no secrets, and a test holds that snippet.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report refuses every event but a push to the default branch
~~~~

Clause, the new unit:

~~~~text
declares the permissions it needs, and asks for no secret
~~~~

Clause, the new unit:

~~~~text
The README's calling workflow grants those permissions only and passes no secrets, and a test holds that snippet
~~~~

### Entry

Old:

~~~~text
- **Answer:** the price table ships with the pinned tool, so changing it in an adopting repository means pinning a different tool, which T21 covers. In this repository, each price row names its source page, the statements of how modifiers combine are dated like prices, and a test fails when a pull request changes or removes an existing row, or adds one dated on or before the newest row for the same price.
~~~~

New:

~~~~text
- **Answer:** the price table ships with the pinned tool, so changing it in an adopting repository means pinning a different tool, which T21 covers. In this repository, each price row names its source page, the statements of how modifiers combine are dated like prices (R14), and a test fails when a pull request changes or removes an existing row, or adds one dated on or before the newest row for the same price.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the price table ships with the pinned tool, so changing it in an adopting repository means pinning a different tool, which T21 covers. In this repository, each price row names its source page, the statements of how modifiers combine are dated like prices
~~~~

Clause, the new unit:

~~~~text
and a test fails when a pull request changes or removes an existing row, or adds one dated on or before the newest row for the same price
~~~~

### Entry

Old:

~~~~text
- **Answer:** the README's short start says, before any step that opts anyone in, that what a person's sessions spend is committed with their work and published when that work is pushed, and the README's section on adopting the tool says what a public repository's ledger and comment show: which models were used, how many tokens, on which days, and the cost. The opt-in's pages say that, with the plugin, one opt-in records in every repository that turns the tool on where the person's sessions work or commit, whether or not that repository registers the hook file.
~~~~

New:

~~~~text
- **Answer:** the README's short start says, before any step that opts anyone in, that what a person's sessions spend is committed with their work and published when that work is pushed (R199), and the README's section on adopting the tool says what a public repository's ledger and comment show: which models were used, how many tokens, on which days, and the cost. The opt-in's pages say that, with the plugin, one opt-in records in every repository that turns the tool on where the person's sessions work or commit, whether or not that repository registers the hook file (R164).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the README's short start says, before any step that opts anyone in, that what a person's sessions spend is committed with their work and published when that work is pushed
~~~~

Clause, the new unit:

~~~~text
and the README's section on adopting the tool says what a public repository's ledger and comment show: which models were used, how many tokens, on which days, and the cost. The opt-in's pages say that, with the plugin, one opt-in records in every repository that turns the tool on where the person's sessions work or commit, whether or not that repository registers the hook file
~~~~

### Entry

Old:

~~~~text
- **Answer:** consent holds for each call. An interval when both switches were on begins only at a run that finds both on while its session has no open interval, never at the session's start, and ends at its last run before one that finds either off or another fingerprint of the files that can turn the person's capture on or off. Once the step's own reading finds both on, it also asks git for each value of the opt-in key that git reads in the repository, twice, in the session's environment and without its `GIT_` variables, and takes capture to be off when either answer does not come within the run's time budget or gives no value or a refusal, or when its last value, or the last value of any file in it other than the person's two global configuration files or of the variables, is not true. A call counts as inside an interval only when, by each line's own time, the line it answers, the nearest up its first line's chain of parents in the same transcript that gives the person's prompt, a tool's result or a compaction's summary, was written at or after the run that began the interval and no later than the call's first line, and that first line no later than the interval's last run. A run reads again the lines that a call not yet recorded may answer, so that a call is placed by the line it answers whichever run read that line, and a run whose clock reads earlier than the latest time that its session's runs noted or read places no call inside that session's intervals, and begins none. Every other call is left out, and the next ledger file staged for its worktree and branch says so, with no count. A start run at `SessionStart`, which reads no transcript, lets the interval begin before a session's first call, and nothing depends on it. A run that finds a switch off creates no store and adds no note of its session to one. A run that finds the person's own capture off and a store of a version that it knows, or a fingerprint other than the store's last, ends every session's interval and empties the store of everything but what take-backs and put-backs need, and no call made before that run is staged after it (T44). A run holds the store's lock from when it reads the store until it has written it, and reads both switches again under that lock before it writes a call or stages a ledger file, so that a run that began before an opt-out writes nothing after it. Taking back and putting back ledger files does not wait on the switches. Each run's time is read from the system's clock in UTC, which no environment variable sets.
~~~~

New:

~~~~text
- **Answer:** consent holds for each call (R40). An interval when both switches were on begins only at a run, never at the session's start, and ends at a run (R108). Once the step's own reading finds both on, git's own reading of the opt-in can still turn capture off (R160). A call counts as inside an interval only when the line it answers and its first line are inside it (R144). A run reads again the lines that a call not yet recorded may answer, so that a call is placed by the line it answers whichever run read that line (R165), and a run whose clock reads earlier than the latest time that its session's runs noted or read places no call inside that session's intervals, and begins none (R166). Every other call is left out, and the next ledger file staged for its worktree and branch says so, with no count (R155). A start run at `SessionStart`, which reads no transcript, lets the interval begin before a session's first call, and nothing depends on it (R148). A run that finds a switch off creates no store and adds no note of its session to one (R145). A run that finds the person's own capture off and a store of a version that it knows, or a fingerprint other than the store's last, ends every session's interval and empties the store (R109, R162), and no call made before that run is staged after it (T44). A run holds the store's lock from when it reads the store until it has written it, and reads both switches again under that lock before it writes a call or stages a ledger file, so that a run that began before an opt-out writes nothing after it (R161). Taking back and putting back ledger files does not wait on the switches (R110). Each run's time is read from the system's clock in UTC, which no environment variable sets (R107).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** consent holds for each call
~~~~

Clause, the new unit:

~~~~text
An interval when both switches were on begins only at a run
~~~~

Clause, R108:

~~~~text
that finds both on while its session has no open interval
~~~~

Clause, the new unit:

~~~~text
never at the session's start
~~~~

Clause, R108:

~~~~text
and ends at its last run before one that finds either off or another fingerprint of the files that can turn the person's capture on or off
~~~~

Clause, the new unit:

~~~~text
Once the step's own reading finds both on
~~~~

Clause, R160:

~~~~text
it also asks git for each value of the opt-in key that git reads in the repository, twice, in the session's environment and without its `GIT_` variables, and takes capture to be off when either answer does not come within the run's time budget or gives no value or a refusal, or when its last value, or the last value of any file in it other than the person's two global configuration files or of the variables, is not true
~~~~

Clause, the new unit:

~~~~text
A call counts as inside an interval only when
~~~~

Clause, R144:

~~~~text
by each line's own time, the line it answers, the nearest up its first line's chain of parents in the same transcript that gives the person's prompt, a tool's result or a compaction's summary, was written at or after the run that began the interval and no later than the call's first line, and that first line no later than the interval's last run
~~~~

Clause, the new unit:

~~~~text
A run reads again the lines that a call not yet recorded may answer, so that a call is placed by the line it answers whichever run read that line
~~~~

Clause, the new unit:

~~~~text
and a run whose clock reads earlier than the latest time that its session's runs noted or read places no call inside that session's intervals, and begins none
~~~~

Clause, the new unit:

~~~~text
Every other call is left out, and the next ledger file staged for its worktree and branch says so, with no count
~~~~

Clause, the new unit:

~~~~text
A start run at `SessionStart`, which reads no transcript, lets the interval begin before a session's first call, and nothing depends on it
~~~~

Clause, the new unit:

~~~~text
A run that finds a switch off creates no store and adds no note of its session to one
~~~~

Clause, the new unit:

~~~~text
A run that finds the person's own capture off and a store of a version that it knows, or a fingerprint other than the store's last, ends every session's interval and empties the store
~~~~

Clause, R109:

~~~~text
of everything but what take-backs and put-backs need
~~~~

Clause, the new unit:

~~~~text
and no call made before that run is staged after it (T44). A run holds the store's lock from when it reads the store until it has written it, and reads both switches again under that lock before it writes a call or stages a ledger file, so that a run that began before an opt-out writes nothing after it
~~~~

Clause, the new unit:

~~~~text
Taking back and putting back ledger files does not wait on the switches
~~~~

Clause, the new unit:

~~~~text
Each run's time is read from the system's clock in UTC, which no environment variable sets
~~~~

### Entry

Old:

~~~~text
- **Answer:** the step reads the fields it knows and counts the calls whose usage has a field it does not, at its top level or in a block nested in it. The comment gives that count and says the token cost may be low.
~~~~

New:

~~~~text
- **Answer:** the step reads the fields it knows and counts the calls whose usage has a field it does not (R43). The comment gives that count and says the token cost may be low (R95).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the step reads the fields it knows and counts the calls whose usage has a field it does not
~~~~

Clause, R43:

~~~~text
at its top level or in a block nested in it
~~~~

Clause, the new unit:

~~~~text
The comment gives that count and says the token cost may be low
~~~~

### Entry

Old:

~~~~text
- **Answer:** task 1.1 checks which of Claude Code's own model calls the transcript holds. The comment says what the figure is, and the README says that calls Claude Code makes for its own tools without writing them to the transcript are not counted.
~~~~

New:

~~~~text
- **Answer:** task 1.1 checks which of Claude Code's own model calls the transcript holds. The comment says what the figure is (R94), and the README says that calls Claude Code makes for its own tools without writing them to the transcript are not counted.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** task 1.1 checks which of Claude Code's own model calls the transcript holds. The comment says what the figure is
~~~~

Clause, the new unit:

~~~~text
and the README says that calls Claude Code makes for its own tools without writing them to the transcript are not counted
~~~~

### Entry

Old:

~~~~text
- **Answer:** the step finds the home folder the way git for Windows does: `HOME` when it holds an absolute path, and otherwise `HOMEDRIVE` and `HOMEPATH` together where they name a folder that exists and is not Windows' system folder, and the profile folder where they do not; it never reads a relative path.
~~~~

New:

~~~~text
- **Answer:** the step finds the home folder the way git for Windows does, and never reads a relative path (R104).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the step finds the home folder the way git for Windows does
~~~~

Clause, R104:

~~~~text
: `HOME` when it holds an absolute path, and otherwise `HOMEDRIVE` and `HOMEPATH` together where they name a folder that exists and is not Windows' system folder, and the profile folder where they do not;
~~~~

Clause, R104:

~~~~text
it never reads a relative path.
~~~~

### Entry

Old:

~~~~text
- **Answer:** a run reads only complete lines and leaves a half-written last line for a later run. A line that a whole budget cannot read is skipped and counted, and a run of the plugin that works on several repositories counts it in the next ledger file of each, since it cannot tell whose call it was. The store is replaced whole, under a lock that the operating system releases when the process dies, and a ledger file is noted in the store before it is written, so a later run takes back a file that a killed run left.
~~~~

New:

~~~~text
- **Answer:** a run reads only complete lines, and no one line holds capture back (R44); a run of the plugin that works on several repositories counts a line that it skips in each, since it cannot tell whose call it was. A run killed while it writes leaves the store whole (R11), and a ledger file is noted in the store before it is written, so a later run takes back a file that a killed run left (R57).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a run reads only complete lines
~~~~

Clause, R44:

~~~~text
and leaves a half-written last line for a later run.
~~~~

Clause, R44:

~~~~text
A line that a whole budget cannot read is skipped and counted, and a run of the plugin that works on several repositories counts it in the next ledger file of each,
~~~~

Clause, the new unit:

~~~~text
since it cannot tell whose call it was.
~~~~

Clause, R11:

~~~~text
The store is replaced whole, under a lock that the operating system releases when the process dies,
~~~~

Clause, the new unit:

~~~~text
and a ledger file is noted in the store before it is written, so a later run takes back a file that a killed run left
~~~~

### Entry

Old:

~~~~text
- **Answer:** the store carries a format version from the first release, in a field that every release reads in the same way, so that no release takes a later one's store for a broken one, and a run that finds a version it does not know records, stages, takes back and puts back nothing, leaves the store as it was, whatever the switches say, and exits with success, while a run that finds an earlier version rewrites the store in its own version, keeping its waiting calls and its notes of taken calls and of ledger files, and begins every session's interval anew. The store's format is part of the public surface whose change raises the major number. Every release that writes a version of the store keeps its path, its lock and its fields, and makes its fingerprint the same way, which a test holds to the hash recorded for each version, while the checks fail when a change alters the hash recorded for a version that a published release wrote, whatever the major number, so that copies of two releases that share a store version read each other's notes as their own, and a release that changes any of these writes a new version, which the surface manifest names, so that the release check asks for a raised major number. Each run that finds both switches on notes, for its session, the latest release whose copy has run in it, and a run of an earlier release than that leaves the session there to the later release's copy, but for an opt-out (T130).
~~~~

New:

~~~~text
- **Answer:** the store carries a format version from the first release, so that no release takes a later one's store for a broken one, and a run leaves a store of a version that it does not know as it was, whatever the switches say, and upgrades one of an earlier version (R55). The store's format is part of the public surface whose change raises the major number (R71, R122). Every release that writes a version of the store keeps its path, its lock and its fields, and makes its fingerprint the same way (R192), so that copies of two releases that share a store version read each other's notes as their own, and a release that changes any of these writes a new version, which the surface manifest names, so that the release check asks for a raised major number. A run of an earlier release than the latest whose copy has run in a session leaves the session to the later release's copy, but for an opt-out (R191, T130).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the store carries a format version from the first release,
~~~~

Clause, R55:

~~~~text
in a field that every release reads in the same way,
~~~~

Clause, the new unit:

~~~~text
so that no release takes a later one's store for a broken one,
~~~~

Clause, R55:

~~~~text
and a run that finds a version it does not know records, stages, takes back and puts back nothing, leaves the store as it was,
~~~~

Clause, the new unit:

~~~~text
whatever the switches say,
~~~~

Clause, R55:

~~~~text
and exits with success, while a run that finds an earlier version rewrites the store in its own version, keeping its waiting calls and its notes of taken calls and of ledger files, and begins every session's interval anew.
~~~~

Clause, the new unit:

~~~~text
The store's format is part of the public surface whose change raises the major number
~~~~

Clause, the new unit:

~~~~text
Every release that writes a version of the store keeps its path, its lock and its fields, and makes its fingerprint the same way
~~~~

Clause, R192:

~~~~text
which a test holds to the hash recorded for each version, while the checks fail when a change alters the hash recorded for a version that a published release wrote, whatever the major number,
~~~~

Clause, the new unit:

~~~~text
so that copies of two releases that share a store version read each other's notes as their own, and a release that changes any of these writes a new version, which the surface manifest names, so that the release check asks for a raised major number.
~~~~

Clause, R191:

~~~~text
Each run that finds both switches on notes, for its session, the latest release whose copy has run in it, and a run of an earlier release than that leaves the session there to the later release's copy,
~~~~

Clause, the new unit:

~~~~text
but for an opt-out
~~~~

Clause, the new unit:

~~~~text
T130
~~~~

### Entry

Old:

~~~~text
- **Answer:** every git command the step runs has `GIT_NO_LAZY_FETCH=1` and `GIT_TERMINAL_PROMPT=0`, and a blob that the clone lacks is skipped, as an oversized one is.
~~~~

New:

~~~~text
- **Answer:** no git command that the step runs can fetch what the clone lacks (R111), and the step skips a ledger file whose blob the clone lacks, as it skips an oversized one (R45).
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R111:

~~~~text
every git command the step runs has `GIT_NO_LAZY_FETCH=1` and `GIT_TERMINAL_PROMPT=0`,
~~~~

Clause, R45:

~~~~text
and a blob that the clone lacks is skipped, as an oversized one is.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the step finds git at an absolute path, from `PATH`'s absolute entries only, skipping any that names a folder inside the working trees or the git common directory of this repository, or, for a run of the plugin, of any repository that it works on, as a tool that sets up a folder's environment can add, which it learns from the project directory's `.git`, the `commondir` file in the git folder that it names, which is the git common directory itself when it holds none, and each linked worktree's `gitdir` file, each opened only when it is a regular file, starting no program, and saying so, when it cannot read one of them, finds a folder in `worktrees/` with no `gitdir` file, or runs in a linked worktree whose git common directory is not named `.git`, as a submodule's is not, nor a bare repository's in a folder such as `repo.git`, since it then cannot tell where the main worktree is, or that there is none. It sets its own working directory to a folder that only an administrator can write, passes each git command its repository with `-C` and without the session's `GIT_` variables (T119), and reads both switches before it starts any program. A run of the plugin that cannot read a clone's files in this way leaves that clone out, saying so on standard error, and skips any entry of `PATH` inside that clone's folder too, so that one unusual clone neither stops a run over the others nor lends it a git (DR-198).
~~~~

New:

~~~~text
- **Answer:** the step starts only git, found at an absolute path in a folder that no repository that it works on holds, and starts no program where it cannot read the git files that name those folders, or runs in a linked worktree whose git common directory is not named `.git` (R54), since it then cannot tell where the main worktree is, or that there is none. It passes each git command its repository with `-C` and without the session's `GIT_` variables (T119), and reads both switches before it starts any program (R118). A run of the plugin leaves out a clone whose files it cannot read, and runs no git inside it (R54, R180), so that one unusual clone neither stops a run over the others nor lends it a git (DR-198).
~~~~

Clause, R54:

~~~~text
- **Answer:** the step finds git at an absolute path, from `PATH`'s absolute entries only, skipping any that names a folder inside the working trees or the git common directory of this repository, or, for a run of the plugin, of any repository that it works on, as a tool that sets up a folder's environment can add, which it learns from the project directory's `.git`, the `commondir` file in the git folder that it names, which is the git common directory itself when it holds none, and each linked worktree's `gitdir` file, each opened only when it is a regular file, starting no program, and saying so, when it cannot read one of them, finds a folder in `worktrees/` with no `gitdir` file,
~~~~

Clause, the new unit:

~~~~text
or runs in a linked worktree whose git common directory is not named `.git`
~~~~

Clause, R54:

~~~~text
, as a submodule's is not, nor a bare repository's in a folder such as `repo.git`,
~~~~

Clause, the new unit:

~~~~text
since it then cannot tell where the main worktree is, or that there is none.
~~~~

Clause, R54:

~~~~text
It sets its own working directory to a folder that only an administrator can write,
~~~~

Clause, the new unit:

~~~~text
passes each git command its repository with `-C` and without the session's `GIT_` variables (T119), and reads both switches before it starts any program
~~~~

Clause, R54:

~~~~text
A run of the plugin that cannot read a clone's files in this way leaves that clone out, saying so on standard error, and skips any entry of `PATH` inside that clone's folder too,
~~~~

Clause, the new unit:

~~~~text
so that one unusual clone neither stops a run over the others nor lends it a git (DR-198).
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report counts no entry whose call any ledger file in the default branch's first-parent history held before the merge, and counts such files as restored.
~~~~

New:

~~~~text
- **Answer:** a ledger file that comes back holds calls that the default branch held before the merge, so the report counts none of them again (R59) and counts the file as restored (R119).
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R59:

~~~~text
the report counts no entry whose call any ledger file in the default branch's first-parent history held before the merge,
~~~~

Clause, R119:

~~~~text
and counts such files as restored.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report holds files that the default branch already holds to capture's rules: it skips a path that is not a regular file and a file above the per-file bound, and skips an unreadable line without stopping. Such a line is counted neither as an entry nor as refused, so that later pull requests' comments do not repeat a refusal that is not theirs.
~~~~

New:

~~~~text
- **Answer:** the report holds files that the default branch already holds to capture's rules (R67), so that later pull requests' comments do not repeat a refusal that is not theirs.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report holds files that the default branch already holds to capture's rules
~~~~

Clause, R67:

~~~~text
: it skips a path that is not a regular file and a file above the per-file bound, and skips an unreadable line without stopping. Such a line is counted neither as an entry nor as refused,
~~~~

Clause, the new unit:

~~~~text
so that later pull requests' comments do not repeat a refusal that is not theirs.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the configuration is read only as a blob at each commit, within a small bound, and a missing, non-regular, oversized or unparseable file, or one that holds a key that the configuration's format does not document, gives a key twice or has no `enabled` of `true` or `false`, counts as not turning the tool on at that commit, without stopping the report. The change is flagged, and the comment says when the tool is off after the merge, and why, as the job summary does for a merge that finds it off at both commits. Capture treats a configuration file that is not a regular file, or that is not valid, as turning capture off.
~~~~

New:

~~~~text
- **Answer:** the configuration is read only as a blob at each commit, within a small bound, and a file that is not valid counts as not turning the tool on at that commit, without stopping the report (R92, R171). The change is flagged (R93), and the comment says when the tool is off after the merge (R172). Capture treats such a file as turning capture off (R36, R171).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the configuration is read only as a blob at each commit, within a small bound,
~~~~

Clause, R92:

~~~~text
and a missing, non-regular, oversized or unparseable file,
~~~~

Clause, R171:

~~~~text
or one that holds a key that the configuration's format does not document, gives a key twice or has no `enabled` of `true` or `false`,
~~~~

Clause, the new unit:

~~~~text
counts as not turning the tool on at that commit, without stopping the report
~~~~

Clause, the new unit:

~~~~text
The change is flagged
~~~~

Clause, the new unit:

~~~~text
and the comment says when the tool is off after the merge
~~~~

Clause, R172:

~~~~text
, and why, as the job summary does for a merge that finds it off at both commits.
~~~~

Clause, the new unit:

~~~~text
Capture treats
~~~~

Clause, R36:

~~~~text
a configuration file that is not a regular file,
~~~~

Clause, R171:

~~~~text
or that is not valid,
~~~~

Clause, the new unit:

~~~~text
as turning capture off
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report keeps to a documented call budget and its job has a `timeout-minutes`. A pull request with more commits than the budget allows has its CI cost marked incomplete, and a push with more commits than it allows gets no comment. A runs listing that GitHub cuts short is not taken as whole.
~~~~

New:

~~~~text
- **Answer:** the report keeps to a documented call budget and its job has a `timeout-minutes` (R70); a CI cost that the budget leaves partly unread is marked incomplete (R64, R121), and a push that it cannot follow gets no comment (R70).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report keeps to a documented call budget and its job has a `timeout-minutes`
~~~~

Clause, R64:

~~~~text
A pull request with more commits than the budget allows has its CI cost marked incomplete,
~~~~

Clause, R70:

~~~~text
and a push with more commits than it allows gets no comment.
~~~~

Clause, R121:

~~~~text
A runs listing that GitHub cuts short is not taken as whole.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the rule that the comment shows only what the report computed covers the job summary and the log too, workflow commands included, and so does the rule that the token never reaches the output. The property test over planted strings covers all three.
~~~~

New:

~~~~text
- **Answer:** the rule that the comment shows only what the report computed covers the job summary and the log too (R21, R97, R98), and so does the rule that the token never reaches the output (R24). The property test over planted strings covers all three.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the rule that the comment shows only what the report computed covers the job summary and the log too
~~~~

Clause, R97:

~~~~text
, workflow commands included,
~~~~

Clause, the new unit:

~~~~text
and so does the rule that the token never reaches the output
~~~~

Clause, the new unit:

~~~~text
The property test over planted strings covers all three.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the public surface names everything adopters configure or depend on, a manifest of it is kept in the repository, and the release check compares it between the previous release's commit and the tag, refusing a release whose surface changed without a raised major number and a `### Breaking` section. A newer report reads every ledger format that an earlier release's hook wrote, with one fixture per released format. The surface names the hook's registration whole, by the events and matchers that it names and its command's form, the plugin's name, the events and matchers that its hooks name and their command's form, the marketplace's name, each key that the configuration's format documents, with the values that each takes, each released ledger version's schema by its hash, and each store version with the hash that its fingerprint gives for a fixed set of files, and a run that finds a store that an earlier release wrote rewrites it in its own version. A test fails when the configuration's reader takes a key or a value that the manifest does not name, or refuses a key or a value of the configuration that it names, so that a release that changes what the reader takes changes the manifest too. A person's plugin follows their account rather than a repository's pin, so a report also meets ledger files of a later release than its own, which each name the release that wrote them, and the comment says so (T136).
~~~~

New:

~~~~text
- **Answer:** the public surface names everything adopters configure or depend on, a manifest of it is kept in the repository (R122), and the release check compares it between the previous release's commit and the tag (R71, R123). A newer report reads every ledger format that an earlier release's hook wrote (R158), with one fixture per released format. The surface names the hook's registration, the plugin, the marketplace, the configuration's keys, each released ledger version's schema and each store version's fingerprint (R122, R156, R192), and a run that finds a store that an earlier release wrote rewrites it in its own version (R55). A test fails when the configuration's reader takes a key or a value that the manifest does not name, or refuses a key or a value of the configuration that it names, so that a release that changes what the reader takes changes the manifest too. A person's plugin follows their account rather than a repository's pin, so a report also meets ledger files of a later release than its own, and the comment says so (R156, R193, T136).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the public surface names everything adopters configure or depend on, a manifest of it is kept in the repository
~~~~

Clause, the new unit:

~~~~text
, and the release check compares it between the previous release's commit and the tag
~~~~

Clause, R123:

~~~~text
, refusing a release whose surface changed without a raised major number and a `### Breaking` section.
~~~~

Clause, the new unit:

~~~~text
A newer report reads every ledger format that an earlier release's hook wrote
~~~~

Clause, the new unit:

~~~~text
with one fixture per released format.
~~~~

Clause, R122:

~~~~text
The surface names the hook's registration whole, by the events and matchers that it names and its command's form, the plugin's name, the events and matchers that its hooks name and their command's form, the marketplace's name, each key that the configuration's format documents, with the values that each takes,
~~~~

Clause, R156:

~~~~text
each released ledger version's schema by its hash,
~~~~

Clause, R192:

~~~~text
and each store version with the hash that its fingerprint gives for a fixed set of files,
~~~~

Clause, the new unit:

~~~~text
and a run that finds a store that an earlier release wrote rewrites it in its own version
~~~~

Clause, the new unit:

~~~~text
A test fails when the configuration's reader takes a key or a value that the manifest does not name, or refuses a key or a value of the configuration that it names, so that a release that changes what the reader takes changes the manifest too.
~~~~

Clause, the new unit:

~~~~text
A person's plugin follows their account rather than a repository's pin, so a report also meets ledger files of a later release than its own,
~~~~

Clause, R156:

~~~~text
which each name the release that wrote them,
~~~~

Clause, the new unit:

~~~~text
and the comment says so
~~~~

Clause, the new unit:

~~~~text
T136
~~~~

### Entry

Old:

~~~~text
- **Answer:** the hook file names its release in its first line, the comment says when the hook in the merged commit differs from the one at the report's own commit, quoting nothing from the file, and the README tells adopters to update the file, its checksum and the pin together, in one pull request. Each ledger file's first line names the release that wrote it, and the comment says when a ledger file that the merge adds names a later release than the report's, as a person's plugin can, since it follows their account rather than the repository's pin (T136).
~~~~

New:

~~~~text
- **Answer:** the hook file names its release (R53), the comment names a hook in the merged commit that differs from the one at the report's own commit (R65), and the README tells adopters to update the file, its checksum and the pin together, in one pull request. Each ledger file names the release that wrote it (R156), and the comment says when one names a later release than the report's (R193), as a person's plugin can, since it follows their account rather than the repository's pin (T136).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the hook file names its release
~~~~

Clause, R53:

~~~~text
in its first line,
~~~~

Clause, R65:

~~~~text
the comment says when the hook in the merged commit differs from the one at the report's own commit, quoting nothing from the file,
~~~~

Clause, the new unit:

~~~~text
and the README tells adopters to update the file, its checksum and the pin together, in one pull request.
~~~~

Clause, R156:

~~~~text
Each ledger file's first line names the release that wrote it,
~~~~

Clause, R193:

~~~~text
and the comment says when a ledger file that the merge adds names a later release than the report's,
~~~~

Clause, the new unit:

~~~~text
as a person's plugin can, since it follows their account rather than the repository's pin (T136).
~~~~

### Entry

Old:

~~~~text
- **Answer:** `requires-python` is the one source, and a test fails when any other copy disagrees, or when the CI matrix lacks either the oldest version or the newest release.
~~~~

New:

~~~~text
- **Answer:** `requires-python` is the one source, and a test holds every other copy to it and the CI matrix to the oldest version and the newest release (R25, R99).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** `requires-python` is the one source,
~~~~

Clause, R99:

~~~~text
and a test fails when any other copy disagrees, or when the CI matrix lacks either the oldest version
~~~~

Clause, R25:

~~~~text
or the newest release.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the step checks, before anything else, that Python is 3.11 or later, and before its first other git command that git is 2.43 or later, the oldest git that CI tests. Below either floor it records nothing, stages nothing, prints nothing and exits with success. Both floors are part of the public surface.
~~~~

New:

~~~~text
- **Answer:** the step checks its floors, the oldest Python that the tool supports and the oldest git that CI tests, and does nothing below either (R32). Both floors are part of the public surface (R122).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the step checks
~~~~

Clause, R32:

~~~~text
, before anything else, that Python is 3.11 or later, and before its first other git command that git is 2.43 or later,
~~~~

Clause, the new unit:

~~~~text
the oldest git that CI tests
~~~~

Clause, R32:

~~~~text
Below either floor it records nothing, stages nothing, prints nothing and exits with success.
~~~~

Clause, the new unit:

~~~~text
Both floors are part of the public surface
~~~~

### Entry

Old:

~~~~text
- **Answer:** the test compares the page's table of permissions, per workflow and per job, with every workflow, `.yml` and `.yaml` alike, in both directions, and compares every action and image the workflows use with the connections the page names. A requirement that a later change removes leaves the register, and its ID is retired.
~~~~

New:

~~~~text
- **Answer:** the test compares the page's table of permissions with every workflow, in both directions, and every action and image that the workflows use with the connections that the page names (R101). A requirement that a later change removes leaves the register, and its ID is retired.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the test compares the page's table of permissions
~~~~

Clause, R101:

~~~~text
per workflow and per job,
~~~~

Clause, the new unit:

~~~~text
with every workflow,
~~~~

Clause, R101:

~~~~text
`.yml` and `.yaml` alike,
~~~~

Clause, the new unit:

~~~~text
in both directions,
~~~~

Clause, R101:

~~~~text
and compares every action and image the workflows use with the connections the page names.
~~~~

Clause, the new unit:

~~~~text
A requirement that a later change removes leaves the register, and its ID is retired.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the README tells adopters to pin only a commit that a release of this repository names, and to check it in a clone of this repository with `git merge-base --is-ancestor <commit> origin/main`, which fails for a commit that only a fork holds. A release names only a commit in the default branch's first-parent history. The README's short start says to pin a release, and links the section that gives the check.
~~~~

New:

~~~~text
- **Answer:** the README tells adopters to pin only a commit that a release of this repository names, and to check it in a clone of this repository with `git merge-base --is-ancestor <commit> origin/main`, which fails for a commit that only a fork holds. A release names only a commit in the default branch's first-parent history (R27). The README's short start says to pin a release, and links the section that gives the check (R198).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the README tells adopters to pin only a commit that a release of this repository names, and to check it in a clone of this repository with `git merge-base --is-ancestor <commit> origin/main`, which fails for a commit that only a fork holds. A release names only a commit in the default branch's first-parent history
~~~~

Clause, the new unit:

~~~~text
The README's short start says to pin a release, and links the section that gives the check
~~~~

### Entry

Old:

~~~~text
- **Answer:** the registered command carries the hook file's SHA-256, reads the file once and runs what it read only when it matches, with each CRLF taken as LF, in every shell the command runs in. The plugin's command carries the SHA-256 of the capture step in the plugin's own folder and runs it only when it matches in the same way, since a copied plugin's folder is a copy that no checkout changes, while one loaded in place runs from its source folder (DR-197). The README says to install the plugin only from a release's zip or from this repository's GitHub address. The README tells maintainers to review a pull request from another worktree, or from its diff.
~~~~

New:

~~~~text
- **Answer:** the registered command runs the hook file only when it matches the checksum that the command carries (R88), and the plugin's command does the same for the capture step in the plugin's own folder (R179), since a copied plugin's folder is a copy that no checkout changes, while one loaded in place runs from its source folder (DR-197). The README says to install the plugin only from a release's zip or from this repository's GitHub address (R187). The README tells maintainers to review a pull request from another worktree, or from its diff.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the registered command
~~~~

Clause, R88:

~~~~text
carries the hook file's SHA-256, reads the file once and runs what it read only when it matches, with each CRLF taken as LF, in every shell the command runs in.
~~~~

Clause, R179:

~~~~text
The plugin's command carries the SHA-256 of the capture step in the plugin's own folder and runs it only when it matches in the same way,
~~~~

Clause, the new unit:

~~~~text
since a copied plugin's folder is a copy that no checkout changes, while one loaded in place runs from its source folder (DR-197).
~~~~

Clause, the new unit:

~~~~text
The README says to install the plugin only from a release's zip or from this repository's GitHub address
~~~~

Clause, the new unit:

~~~~text
The README tells maintainers to review a pull request from another worktree, or from its diff.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the hook file's path is fixed by the README, a pull request that changes it, or `.claude/settings.json` or `.claude/settings.local.json`, the project settings files that can register it and set its environment, has that flagged in its comment, and a hook file that differs from the one at the report's own commit is named.
~~~~

New:

~~~~text
- **Answer:** the hook file's path is fixed by the README, so a pull request that changes the hook file, or a project settings file that can register it and set its environment, has that flagged in its comment (R93), and a hook file that differs from the one at the report's own commit is named (R65).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the hook file's path is fixed by the README,
~~~~

Clause, R93:

~~~~text
a pull request that changes it, or `.claude/settings.json` or `.claude/settings.local.json`, the project settings files that can register it and set its environment, has that flagged in its comment,
~~~~

Clause, the new unit:

~~~~text
and a hook file that differs from the one at the report's own commit is named
~~~~

### Entry

Old:

~~~~text
- **Answer:** every action and container image that a workflow uses is pinned to a commit or digest that a tag of its source names, and CI fails on anything else, checked against a local fixture.
~~~~

New:

~~~~text
- **Answer:** CI holds every action and container image that a workflow uses to a commit or digest that a tag of its source names (R34), checked against a local fixture.
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R34:

~~~~text
every action and container image that a workflow uses is pinned to a commit or digest that a tag of its source names, and CI fails on anything else,
~~~~

Clause, the new unit:

~~~~text
checked against a local fixture.
~~~~

### Entry

Old:

~~~~text
- **Answer:** each control that is the owner's alone names an identity that agent sessions never hold, wherever there is one, such as the deploy key that alone may bypass the tag ruleset. Where there is none, as for dashboard approvals, and for merges while the only code owner's account also opens pull requests here, `CLAUDE.md`'s section on what an agent never does here keeps them with the owner. Adopters pin only a commit that a release names, and the marketplace serves only a published release's plugin, as its tag builds it (T132), so an agent's merge reaches no adopter, and no person who added the marketplace, before the owner releases it.
~~~~

New:

~~~~text
- **Answer:** each control that is the owner's alone names an identity that agent sessions never hold, wherever there is one, such as the deploy key that alone may bypass the tag ruleset. Where there is none, as for dashboard approvals, and for merges while the only code owner's account also opens pull requests here, `CLAUDE.md`'s section on what an agent never does here keeps them with the owner. Adopters pin only a commit that a release names, and the marketplace serves only a published release's plugin (R184, T132), so an agent's merge reaches no adopter, and no person who added the marketplace, before the owner releases it.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each control that is the owner's alone names an identity that agent sessions never hold, wherever there is one, such as the deploy key that alone may bypass the tag ruleset. Where there is none, as for dashboard approvals, and for merges while the only code owner's account also opens pull requests here, `CLAUDE.md`'s section on what an agent never does here keeps them with the owner.
~~~~

Clause, the new unit:

~~~~text
Adopters pin only a commit that a release names, and the marketplace serves only a published release's plugin
~~~~

Clause, R184:

~~~~text
as its tag builds it
~~~~

Clause, the new unit:

~~~~text
T132
~~~~

Clause, the new unit:

~~~~text
so an agent's merge reaches no adopter, and no person who added the marketplace, before the owner releases it.
~~~~

### Entry

Old:

~~~~text
- **Answer:** a CI job checks a pull request's title and body against the same private patterns and name hashes as tracked files, whenever the pull request is opened, edited, reopened or updated, and fails naming the pattern and quoting none of the text. `CLAUDE.md` says that no such link or identifier goes into a commit, a pull request's text, an issue or a comment here, whatever a tool adds.
~~~~

New:

~~~~text
- **Answer:** a CI job checks a pull request's title and body against the same private patterns and name hashes as tracked files (R33). `CLAUDE.md` says that no such link or identifier goes into a commit, a pull request's text, an issue or a comment here, whatever a tool adds.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a CI job checks a pull request's title and body against the same private patterns and name hashes as tracked files
~~~~

Clause, R33:

~~~~text
whenever the pull request is opened, edited, reopened or updated, and fails naming the pattern and quoting none of the text.
~~~~

Clause, the new unit:

~~~~text
`CLAUDE.md` says that no such link or identifier goes into a commit, a pull request's text, an issue or a comment here, whatever a tool adds.
~~~~

### Entry

Old:

~~~~text
- **Answer:** a release is made only from a tag that names a commit in the default branch's first-parent history, which is a guard against mistakes, not the control. The control is who can create a tag or a release: a tag ruleset whose only bypass is an identity that agent sessions never hold, and immutable releases (see Settings the owner keeps). The release's text names the tag and the commit in the workflow's own fixed words. `CLAUDE.md` says that agents never create, move or delete a tag or a release. The marketplace's folder holds only a published release's plugin, its tag taken by its full name and its commit in the default branch's first-parent history, so a tag whose release the workflow refused, which stays, gives the marketplace no version, and the owner deletes such a tag, with its draft, and never tags its version again (T138).
~~~~

New:

~~~~text
- **Answer:** a release is made only from a tag that names a commit in the default branch's first-parent history (R27), which is a guard against mistakes, not the control. The control is who can create a tag or a release: a tag ruleset whose only bypass is an identity that agent sessions never hold, and immutable releases (see Settings the owner keeps). The release's text names the tag and the commit in the workflow's own fixed words (R27). `CLAUDE.md` says that agents never create, move or delete a tag or a release. The marketplace's folder holds only a published release's plugin (R184), so a tag whose release the workflow refused, which stays, gives the marketplace no version, and the owner deletes such a tag, with its draft, and never tags its version again (T138).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a release is made only from a tag that names a commit in the default branch's first-parent history
~~~~

Clause, the new unit:

~~~~text
which is a guard against mistakes, not the control. The control is who can create a tag or a release: a tag ruleset whose only bypass is an identity that agent sessions never hold, and immutable releases (see Settings the owner keeps). The release's text names the tag and the commit in the workflow's own fixed words
~~~~

Clause, the new unit:

~~~~text
`CLAUDE.md` says that agents never create, move or delete a tag or a release. The marketplace's folder holds only a published release's plugin
~~~~

Clause, R184:

~~~~text
its tag taken by its full name and its commit in the default branch's first-parent history,
~~~~

Clause, the new unit:

~~~~text
so a tag whose release the workflow refused, which stays, gives the marketplace no version, and the owner deletes such a tag, with its draft, and never tags its version again (T138).
~~~~

### Entry

Old:

~~~~text
- **Answer:** the release job alone holds `contents: write`, runs only for a pushed tag, checks the tag's form before any other step, installs nothing, restores no cache, checks out without keeping credentials, runs only `python3 -I` on the tagged commit's standard-library scripts and actions pinned by commit, and passes event data only through `env:`. It needs a read-only job that runs the tests on the oldest and newest Python. Actions' default workflow permissions stay read-only as a backstop (see Settings the owner keeps).
~~~~

New:

~~~~text
- **Answer:** the release job alone holds `contents: write`, runs only for a pushed tag, checks the tag's form before any other step (R27), installs nothing, restores no cache, checks out without keeping credentials, runs only `python3 -I` on the tagged commit's standard-library scripts and actions pinned by commit, and passes event data only through `env:`. It needs a read-only job that runs the tests on the oldest and newest Python. Actions' default workflow permissions stay read-only as a backstop (see Settings the owner keeps).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the release job alone holds `contents: write`, runs only for a pushed tag, checks the tag's form before any other step
~~~~

Clause, the new unit:

~~~~text
installs nothing, restores no cache, checks out without keeping credentials, runs only `python3 -I` on the tagged commit's standard-library scripts and actions pinned by commit, and passes event data only through `env:`. It needs a read-only job that runs the tests on the oldest and newest Python. Actions' default workflow permissions stay read-only as a backstop (see Settings the owner keeps).
~~~~

### Entry

Old:

~~~~text
- **Answer:** the bill of materials is written from the tagged tree, never from a working tree, and names the tool, its version, commit and licence, the oldest supported Python, the hook file's SHA-256 and the plugin zip's, each action the reusable workflow uses at its pinned commit, and the vendored and generated parts as development-only components. A release is not published when it cannot be written, when the workflow uses an action it does not list, when a checksum in it differs from the file's or the README's, or when the private-reference check matches it or the release's text. The release is created as a draft and published only once its zip and its bill of materials are attached and each, downloaded again, has the size and SHA-256 of the file that the workflow built (T139).
~~~~

New:

~~~~text
- **Answer:** the bill of materials is written from the tagged tree, never from a working tree, and describes the release (R28). A release is not published when its bill of materials is missing or fails a check (R72), nor before its files are attached and checked (R189, T139).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the bill of materials is written from the tagged tree, never from a working tree,
~~~~

Clause, R28:

~~~~text
and names the tool, its version, commit and licence, the oldest supported Python, the hook file's SHA-256 and the plugin zip's, each action the reusable workflow uses at its pinned commit, and the vendored and generated parts as development-only components.
~~~~

Clause, R72:

~~~~text
A release is not published when it cannot be written, when the workflow uses an action it does not list, when a checksum in it differs from the file's or the README's, or when the private-reference check matches it or the release's text.
~~~~

Clause, R189:

~~~~text
The release is created as a draft and published only once its zip and its bill of materials are attached and each, downloaded again, has the size and SHA-256 of the file that the workflow built
~~~~

Clause, the new unit:

~~~~text
T139
~~~~

### Entry

Old:

~~~~text
- **Answer:** the check compares git trees, never the working tree: every file with a record's name anywhere in the base's tree, by path, mode and object, against HEAD's, with no rename detection, so a rename, a move or anything else put in a record's place counts as removed or changed. It compares with the merge base of HEAD and `refs/remotes/origin/main`, resolved by its full name so that neither a tag nor a local branch can take its place, and in CI also with the base that the workflow names through `env:` as `BASE_COMMIT`: the pull request's base commit, or the commit that a push to the default branch replaced. CI fetches the whole history, and runs again when a pull request's base changes. The check fails when a base is not a full commit ID, is not in the clone or cannot be found, and says how to fetch it. It skips only while no base's tree holds `docs/decisions/`, and fails when a base holds that folder with no file in it named as a record. The release's test job names the commit of the previous release's tag as its base (task 6.3), and tasks 1.9 and 3.1 compare with the same base as this check.
~~~~

New:

~~~~text
- **Answer:** the check compares git trees, never the working tree, with no rename detection, so a rename, a move or anything else put in a record's place counts as removed or changed (R129). It compares with the merge base of HEAD and `refs/remotes/origin/main`, resolved by its full name so that neither a tag nor a local branch can take its place, and in CI also with the base that the workflow names through `env:` as `BASE_COMMIT`, and fails, saying how to fetch it, when a base cannot be found (R129). It skips only while no base's tree holds `docs/decisions/`, and fails when a base holds that folder with no file in it named as a record (R129). The release's test job names the commit of the previous release's tag as its base (task 6.3), and tasks 1.9 and 3.1 compare with the same base as this check.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the check compares git trees, never the working tree
~~~~

Clause, R129:

~~~~text
: every file with a record's name anywhere in the base's tree, by path, mode and object, against HEAD's,
~~~~

Clause, the new unit:

~~~~text
with no rename detection, so a rename, a move or anything else put in a record's place counts as removed or changed
~~~~

Clause, the new unit:

~~~~text
It compares with the merge base of HEAD and `refs/remotes/origin/main`, resolved by its full name so that neither a tag nor a local branch can take its place, and in CI also with the base that the workflow names through `env:` as `BASE_COMMIT`
~~~~

Clause, R129:

~~~~text
: the pull request's base commit, or the commit that a push to the default branch replaced. CI fetches the whole history, and runs again when a pull request's base changes.
~~~~

Clause, R129:

~~~~text
The check fails when a base is not a full commit ID, is not in the clone or cannot be found, and says how to fetch it.
~~~~

Clause, the new unit:

~~~~text
It skips only while no base's tree holds `docs/decisions/`, and fails when a base holds that folder with no file in it named as a record
~~~~

Clause, the new unit:

~~~~text
The release's test job names the commit of the previous release's tag as its base (task 6.3), and tasks 1.9 and 3.1 compare with the same base as this check.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the check's failure messages name the record and the change that is allowed, closing it with a record that replaces it, and say how to fetch what the clone lacks: `git fetch --unshallow` in a shallow clone, and `git fetch origin main:refs/remotes/origin/main` where it lacks the default branch. `CLAUDE.md` says that an accepted record changes only by being closed, and its rule against weakening an acceptance test covers this test, which holds a requirement's scenarios.
~~~~

New:

~~~~text
- **Answer:** the check's failure messages name the record and the change that is allowed, closing it with a record that replaces it, and say how to fetch what the clone lacks: `git fetch --unshallow` in a shallow clone, and `git fetch origin main:refs/remotes/origin/main` where it lacks the default branch. `CLAUDE.md` says that an accepted record changes only by being closed, and its rule against weakening an acceptance test covers this test, which holds a requirement's scenarios (R129).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the check's failure messages name the record and the change that is allowed, closing it with a record that replaces it, and say how to fetch what the clone lacks: `git fetch --unshallow` in a shallow clone, and `git fetch origin main:refs/remotes/origin/main` where it lacks the default branch. `CLAUDE.md` says that an accepted record changes only by being closed, and its rule against weakening an acceptance test covers this test, which holds a requirement's scenarios
~~~~

### Entry

Old:

~~~~text
- **Answer:** "Decided by" takes one of three fixed forms: the owner, with the dates of the decision; the change that made it; or that change, with the dates on which the owner asked for what it decided. Each date must be a real one, no later than the day the tests run, the change must exist, and no link, quotation or identifier fits in the field. The index's column of deciders puts every attribution in one diff, for the owner to read before merging. `CLAUDE.md` says that a record the default branch does not hold is a proposal, whatever its status says, and that the owner's present word decides, not a record's attribution.
~~~~

New:

~~~~text
- **Answer:** "Decided by" takes one of three fixed forms: the owner, with the dates of the decision; the change that made it; or that change, with the dates on which the owner asked for what it decided. Each date must be a real one and the change must exist (R126), and no link, quotation or identifier fits in the field. The index's column of deciders puts every attribution in one diff, for the owner to read before merging (R125). `CLAUDE.md` says that a record the default branch does not hold is a proposal, whatever its status says, and that the owner's present word decides, not a record's attribution.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** "Decided by" takes one of three fixed forms: the owner, with the dates of the decision; the change that made it; or that change, with the dates on which the owner asked for what it decided. Each date must be a real one
~~~~

Clause, R126:

~~~~text
, no later than the day the tests run,
~~~~

Clause, the new unit:

~~~~text
the change must exist
~~~~

Clause, the new unit:

~~~~text
and no link, quotation or identifier fits in the field
~~~~

Clause, the new unit:

~~~~text
The index's column of deciders puts every attribution in one diff, for the owner to read before merging
~~~~

Clause, the new unit:

~~~~text
`CLAUDE.md` says that a record the default branch does not hold is a proposal, whatever its status says, and that the owner's present word decides, not a record's attribution.
~~~~

### Entry

Old:

~~~~text
- **Answer:** `CLAUDE.md` says that records describe and never instruct, and that where a record and `CLAUDE.md` disagree, `CLAUDE.md` steers and the agent tells the owner. A record's last section says what reversing the decision would change, not how to do it. CI fails on a record or an index that holds anything but printable ASCII characters and line breaks, or `&`, a backslash, `@`, a fenced block, a web address, a link reference definition, `<` or `][` outside inline code, or a link but from a record's ID to that record's file, and on a record that holds `|` outside inline code, with which Markdown makes a table, or a line other than its headings that starts with `#`. A record about what agents may do lands in the same pull request as the `CLAUDE.md` change that steers by it.
~~~~

New:

~~~~text
- **Answer:** `CLAUDE.md` says that records describe and never instruct, and that where a record and `CLAUDE.md` disagree, `CLAUDE.md` steers and the agent tells the owner. A record's last section says what reversing the decision would change, not how to do it. CI fails on a record or an index that holds anything but plain text (R128). A record about what agents may do lands in the same pull request as the `CLAUDE.md` change that steers by it.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** `CLAUDE.md` says that records describe and never instruct, and that where a record and `CLAUDE.md` disagree, `CLAUDE.md` steers and the agent tells the owner. A record's last section says what reversing the decision would change, not how to do it.
~~~~

Clause, the new unit:

~~~~text
CI fails on a record or an index that holds anything but
~~~~

Clause, R128:

~~~~text
printable ASCII characters and line breaks, or `&`, a backslash, `@`, a fenced block, a web address, a link reference definition, `<` or `][` outside inline code, or a link but from a record's ID to that record's file, and on a record that holds `|` outside inline code, with which Markdown makes a table, or a line other than its headings that starts with `#`.
~~~~

Clause, the new unit:

~~~~text
A record about what agents may do lands in the same pull request as the `CLAUDE.md` change that steers by it.
~~~~

### Entry

Old:

~~~~text
- **Answer:** only the records, their index, the changelog and archived changes may name a closed record, each by its exact path, and CI fails on any other tracked file that names one, `CLAUDE.md` and this threat model included. CI also fails on an accepted record whose cited requirements are all retired, so the change that retires them closes it. A record that replaces another starts an assessment of what rests on the closed one, and a record that no longer holds is closed in the same change, a backlog item that names it being kept only for one whose standing the assessment cannot settle (DR-230, T168). `CLAUDE.md` says that a closed record holds nothing.
~~~~

New:

~~~~text
- **Answer:** only the records, their index, the changelog and archived changes may name a closed record, each by its exact path, and CI fails on any other tracked file that names one, `CLAUDE.md` and this threat model included (R127). CI also fails on an accepted record whose cited requirements are all retired (R126), so the change that retires them closes it. A record that replaces another starts an assessment of what rests on the closed one, and a record that no longer holds is closed in the same change, a backlog item that names it being kept only for one whose standing the assessment cannot settle (DR-230, T168). `CLAUDE.md` says that a closed record holds nothing.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** only the records, their index, the changelog and archived changes may name a closed record, each by its exact path, and CI fails on any other tracked file that names one, `CLAUDE.md` and this threat model included
~~~~

Clause, the new unit:

~~~~text
CI also fails on an accepted record whose cited requirements are all retired
~~~~

Clause, the new unit:

~~~~text
so the change that retires them closes it. A record that replaces another starts an assessment of what rests on the closed one, and a record that no longer holds is closed in the same change, a backlog item that names it being kept only for one whose standing the assessment cannot settle (DR-230, T168). `CLAUDE.md` says that a closed record holds nothing.
~~~~

### Entry

Old:

~~~~text
- **Answer:** threat IDs are retired, never reused or renumbered, as requirement IDs already are, and the threat model's test accepts only the gaps that its list of retired IDs names. An ID that the default branch's register, threat model or assumptions' index holds or retires must stay held or retired. A record names requirements, threats and records by ID, its change by name, and that change's design decisions and tasks by number, and CI fails on any of them that does not exist, finding a design decision or a task named without its change in any change, active or archived; it links only to other records. A mistaken merge's records are undone by new records that close them, and the check's message on a removal says that a record is only ever closed.
~~~~

New:

~~~~text
- **Answer:** threat IDs are retired, never reused or renumbered, as requirement IDs already are (R132), and an ID that the default branch's register, threat model or assumptions' index holds or retires must stay held or retired (R130). A record names requirements, threats and records by ID, its change by name, and that change's design decisions and tasks by number, and CI fails on any of them that does not exist, finding a design decision or a task named without its change in any change, active or archived (R126); it links only to other records (R128). A mistaken merge's records are undone by new records that close them, and the check's message on a removal says that a record is only ever closed.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** threat IDs are retired, never reused or renumbered, as requirement IDs already are
~~~~

Clause, R132:

~~~~text
, and the threat model's test accepts only the gaps that its list of retired IDs names.
~~~~

Clause, R130:

~~~~text
An ID that the default branch's register, threat model or assumptions' index holds or retires must stay held or retired.
~~~~

Clause, the new unit:

~~~~text
A record names requirements, threats and records by ID, its change by name, and that change's design decisions and tasks by number, and CI fails on any of them that does not exist, finding a design decision or a task named without its change in any change, active or archived
~~~~

Clause, the new unit:

~~~~text
it links only to other records
~~~~

Clause, the new unit:

~~~~text
A mistaken merge's records are undone by new records that close them, and the check's message on a removal says that a record is only ever closed.
~~~~

### Entry

Old:

~~~~text
- **Answer:** `main`'s ruleset requires branches to be up to date before merging (see Settings the owner keeps), so the later pull request's CI runs on what the default branch holds and fails while its record can still be renumbered. The check names a number held twice as such, and CI's run on the push to the default branch reports it at once.
~~~~

New:

~~~~text
- **Answer:** `main`'s ruleset requires branches to be up to date before merging (see Settings the owner keeps), so the later pull request's CI runs on what the default branch holds and fails while its record can still be renumbered. The check names a number held twice as such (R124), and CI's run on the push to the default branch reports it at once.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** `main`'s ruleset requires branches to be up to date before merging (see Settings the owner keeps), so the later pull request's CI runs on what the default branch holds and fails while its record can still be renumbered. The check names a number held twice as such
~~~~

Clause, the new unit:

~~~~text
and CI's run on the push to the default branch reports it at once.
~~~~

### Entry

Old:

~~~~text
- **Answer:** once a record is closed, any line of text under its sections may become `[removed]`, and nothing else in it may change, while the record that closes it restates what still holds. The private-reference check reads tracked path names as well as what the files hold (T32).
~~~~

New:

~~~~text
- **Answer:** a closed record's text can be cleared, line by line (R129), while the record that closes it restates what still holds. The private-reference check reads tracked path names as well as what the files hold (T32).
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R129:

~~~~text
once a record is closed, any line of text under its sections may become `[removed]`, and nothing else in it may change,
~~~~

Clause, the new unit:

~~~~text
while the record that closes it restates what still holds. The private-reference check reads tracked path names as well as what the files hold (T32).
~~~~

### Entry

Old:

~~~~text
- **Answer:** sentences move word for word. A script, run once in the pull request that makes the move, shows that every sentence of the design before the move is in the design or a record after it, apart from the changes it lists, and its result is evidence in that pull request. Every mention of a record or a design decision in tracked prose must resolve, and a threat that cites a record that the default branch does not hold yet must be listed among that record's threats.
~~~~

New:

~~~~text
- **Answer:** sentences move word for word. A script, run once in the pull request that makes the move, shows that every sentence of the design before the move is in the design or a record after it, apart from the changes it lists, and its result is evidence in that pull request. Every mention of a record or a design decision in tracked prose must resolve (R127), and a threat that cites a record that the default branch does not hold yet must be listed among that record's threats (R131).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** sentences move word for word. A script, run once in the pull request that makes the move, shows that every sentence of the design before the move is in the design or a record after it, apart from the changes it lists, and its result is evidence in that pull request. Every mention of a record or a design decision in tracked prose must resolve
~~~~

Clause, the new unit:

~~~~text
and a threat that cites a record that the default branch does not hold yet must be listed among that record's threats
~~~~

### Entry

Old:

~~~~text
- **Answer:** a record's number is written in ASCII digits, padded to three and no further. CI fails on any folder, link or file in `docs/decisions/` but the records and their index, and on a file named as a record anywhere else. Every line of the index's table, which runs to its first blank line, must be a row that the check reads, and a later line that holds `|` fails, and a link whose text is a record's ID must lead to that record's file.
~~~~

New:

~~~~text
- **Answer:** a record's number, the records' folder, the index's table and the links in a record each take only the form that the checks read (R124, R125, R128, R133).
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R124:

~~~~text
a record's number is written in ASCII digits, padded to three and no further.
~~~~

Clause, R133:

~~~~text
CI fails on any folder, link or file in `docs/decisions/` but the records and their index, and on a file named as a record anywhere else.
~~~~

Clause, R125:

~~~~text
Every line of the index's table, which runs to its first blank line, must be a row that the check reads, and a later line that holds `|` fails,
~~~~

Clause, R128:

~~~~text
and a link whose text is a record's ID must lead to that record's file.
~~~~

### Entry

Old:

~~~~text
- **Answer:** each threat that an accepted record lists names that record in its Held by line, so the change that closes the record finds the threat model naming a closed record, which fails CI until the threat is revisited. A threat that names a record the default branch does not hold yet must be listed in that record, and a field of a threat that runs onto a second line fails CI, so that every name in a Held by line is read.
~~~~

New:

~~~~text
- **Answer:** each threat that an accepted record lists names that record in its Held by line (R131), so the change that closes the record finds the threat model naming a closed record, which fails CI until the threat is revisited (R127). A threat that names a record the default branch does not hold yet must be listed in that record, and a field of a threat that runs onto a second line fails CI (R131), so that every name in a Held by line is read.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each threat that an accepted record lists names that record in its Held by line
~~~~

Clause, the new unit:

~~~~text
so the change that closes the record finds the threat model naming a closed record, which fails CI until the threat is revisited
~~~~

Clause, the new unit:

~~~~text
A threat that names a record the default branch does not hold yet must be listed in that record, and a field of a threat that runs onto a second line fails CI
~~~~

Clause, the new unit:

~~~~text
so that every name in a Held by line is read.
~~~~

### Entry

Old:

~~~~text
- **Answer:** CI fails when the repository's attributes give a record, the index, the README, `CLAUDE.md`, the guide, a change's `tasks.md`, the root marketplace file or a file in the plugin folder that it names `binary`, `diff` or `linguist-generated`, in any state, and a person's own global attributes file is not read. The line that sets such an attribute shows in the pull request's own diff. An attribute that changes what git's checkout of the hook file or of the marketplace's plugin folder writes, rather than how its diff shows, is T143.
~~~~

New:

~~~~text
- **Answer:** CI fails on an attribute that hides the diff of a file that the review reads, and reads none of a person's own attributes (R134). The line that sets such an attribute shows in the pull request's own diff. An attribute that changes what git's checkout of the hook file or of the marketplace's plugin folder writes, rather than how its diff shows, is T143.
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R134:

~~~~text
CI fails when the repository's attributes give a record, the index, the README, `CLAUDE.md`, the guide, a change's `tasks.md`, the root marketplace file or a file in the plugin folder that it names `binary`, `diff` or `linguist-generated`, in any state
~~~~

Clause, R134:

~~~~text
and a person's own global attributes file is not read
~~~~

Clause, the new unit:

~~~~text
The line that sets such an attribute shows in the pull request's own diff. An attribute that changes what git's checkout of the hook file or of the marketplace's plugin folder writes, rather than how its diff shows, is T143
~~~~

### Entry

Old:

~~~~text
- **Answer:** `usage-capture` states the rule in a scenario that an acceptance test holds, task 1.1 gives it a fixture, and when the section moves, each of its sentences that states what the tool does, rather than what it assumes, moves to the spec that holds that behaviour.
~~~~

New:

~~~~text
- **Answer:** `usage-capture` states the rule in a scenario of R3 that an acceptance test holds, task 1.1 gives it a fixture, and when the section moves, each of its sentences that states what the tool does, rather than what it assumes, moves to the spec that holds that behaviour.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** `usage-capture` states the rule in a scenario
~~~~

Clause, the new unit:

~~~~text
that an acceptance test holds, task 1.1 gives it a fixture, and when the section moves, each of its sentences that states what the tool does, rather than what it assumes, moves to the spec that holds that behaviour
~~~~

### Entry

Old:

~~~~text
- **Answer:** each golden session lists every call of its transcripts, by its message ID, with the entry that capture must write for it or the scenario that leaves it out, and a test fails on a call left unaccounted for or on a citation of a scenario that does not exist. The set holds sessions whose calls the rules of this boundary keep from being recorded or change.
~~~~

New:

~~~~text
- **Answer:** each golden session lists every call of its transcripts, by its message ID, and a test holds each to an entry or to a scenario that exists and leaves it out (R139). The set holds sessions whose calls the rules of this boundary keep from being recorded or change.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each golden session lists every call of its transcripts, by its message ID
~~~~

Clause, R139:

~~~~text
with the entry that capture must write for it or the scenario that leaves it out, and a test fails on a call left unaccounted for or on a citation of a scenario that does not exist
~~~~

Clause, the new unit:

~~~~text
The set holds sessions whose calls the rules of this boundary keep from being recorded or change
~~~~

### Entry

Old:

~~~~text
- **Answer:** each run's time is read from the system's clock in UTC, which no environment variable sets, and a scenario that sets `TZ` holds it. The golden tests call the step's entry point in the test's own process and give each run its time there.
~~~~

New:

~~~~text
- **Answer:** the session's environment cannot move a run's time (R107). The golden tests call the step's entry point in the test's own process and give each run its time there.
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R107:

~~~~text
each run's time is read from the system's clock in UTC, which no environment variable sets
~~~~

Clause, `switch-and-opt-in`: "The environment cannot move a run's time":

~~~~text
and a scenario that sets `TZ` holds it
~~~~

Clause, the new unit:

~~~~text
The golden tests call the step's entry point in the test's own process and give each run its time there
~~~~

### Entry

Old:

~~~~text
- **Answer:** the golden tests run each golden session in a temporary repository of its own, with a home folder and a configuration folder inside the test's temporary folder, and a check around the whole test run fails when the clone's store, index or working tree changes.
~~~~

New:

~~~~text
- **Answer:** the golden tests run each golden session in a temporary repository of its own, with a home folder and a configuration folder inside the test's temporary folder, and a check around the whole test run fails when the clone's store, index or working tree changes (R139).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the golden tests run each golden session in a temporary repository of its own, with a home folder and a configuration folder inside the test's temporary folder, and a check around the whole test run fails when the clone's store, index or working tree changes
~~~~

### Entry

Old:

~~~~text
- **Answer:** an observation names the file that reproduces what was seen, the date, and the program, the version that it prints and its build, and a test fails on one that does not. The design's context names the build that the observation was made on and the releases whose source does not name the variable, and task 1.19 records the fact as not holding on those releases, linking their source.
~~~~

New:

~~~~text
- **Answer:** an observation that does not name the build it was seen on fails a test (R140). The design's context names the build that the observation was made on and the releases whose source does not name the variable, and task 1.19 records the fact as not holding on those releases, linking their source.
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R140:

~~~~text
an observation names the file that reproduces what was seen, the date, and the program, the version that it prints and its build, and a test fails on one that does not
~~~~

Clause, the new unit:

~~~~text
The design's context names the build that the observation was made on and the releases whose source does not name the variable, and task 1.19 records the fact as not holding on those releases, linking their source
~~~~

### Entry

Old:

~~~~text
- **Answer:** each golden session states the pull request it is reported for, the report runs without capture on a session that gives no transcripts, and the set holds a session for each rule at this boundary that changes a figure or a count. `report-comment` holds that an earlier file's valid lines keep their calls beside an unreadable one, and task 4.2 skips the line, not the file.
~~~~

New:

~~~~text
- **Answer:** the golden tests run the report alone on a pull request's ledger files (R139), and the set holds a session for each rule at this boundary that changes a figure or a count. R67 keeps the calls of an earlier file's valid lines beside an unreadable one, and task 4.2 skips the line, not the file.
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R139:

~~~~text
each golden session states the pull request it is reported for, the report runs without capture on a session that gives no transcripts
~~~~

Clause, the new unit:

~~~~text
and the set holds a session for each rule at this boundary that changes a figure or a count
~~~~

Clause, R67:

~~~~text
`report-comment` holds that an earlier file's valid lines keep their calls beside an unreadable one
~~~~

Clause, the new unit:

~~~~text
and task 4.2 skips the line, not the file
~~~~

### Entry

Old:

~~~~text
- **Answer:** GitHub has a page of its own among the assumptions, and a fact whose subject no test may reach, such as Claude Code or GitHub, is never checked by a test alone: it is observed, documented or not yet, and may name beside that the test that holds the tool's handling of it.
~~~~

New:

~~~~text
- **Answer:** GitHub has a page of its own among the assumptions, and a fact about it is never checked by a test alone (R140): it is observed, documented or not yet, and may name beside that the test that holds the tool's handling of it.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** GitHub has a page of its own among the assumptions, and a fact
~~~~

Clause, R140:

~~~~text
whose subject no test may reach, such as Claude Code or GitHub
~~~~

Clause, the new unit:

~~~~text
is never checked by a test alone
~~~~

Clause, the new unit:

~~~~text
it is observed, documented or not yet, and may name beside that the test that holds the tool's handling of it
~~~~

### Entry

Old:

~~~~text
- **Answer:** the golden set holds each figure as the comment shows it, and its tests compare the comment that the report writes. Task 1.21 waits until `report-comment` states how a cost is shown, a rule whose choices are the owner's and an open question of the design.
~~~~

New:

~~~~text
- **Answer:** the golden set holds each figure as the comment shows it, and its tests compare the comment that the report writes (R139). Task 1.21 waits until `report-comment` states how a cost is shown, a rule whose choices are the owner's and an open question of the design.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the golden set holds each figure as the comment shows it, and its tests compare the comment that the report writes
~~~~

Clause, the new unit:

~~~~text
Task 1.21 waits until `report-comment` states how a cost is shown, a rule whose choices are the owner's and an open question of the design
~~~~

### Entry

Old:

~~~~text
- **Answer:** the wording test never reads inline code or fenced code blocks, which give names, commands, paths and snippets as they must be typed; a word is listed to avoid only if it is wrong wherever it appears in prose; and the review reads the pages that adopters act on before and after a rewording.
~~~~

New:

~~~~text
- **Answer:** the wording test leaves inline code and fenced code blocks as written (R137), which give names, commands, paths and snippets as they must be typed; a word is listed to avoid only if it is wrong wherever it appears in prose; and the review reads the pages that adopters act on before and after a rewording.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the wording test
~~~~

Clause, R137:

~~~~text
never reads inline code or fenced code blocks
~~~~

Clause, the new unit:

~~~~text
which give names, commands, paths and snippets as they must be typed; a word is listed to avoid only if it is wrong wherever it appears in prose; and the review reads the pages that adopters act on before and after a rewording
~~~~

### Entry

Old:

~~~~text
- **Answer:** for each ledger format that a release wrote, the golden set keeps sessions whose entries are as that release wrote them, with their hand-worked figures, for as long as the report reads that format, and a pull request that changes a golden session that the latest release's tag holds names it in the changelog's unreleased section. Each ledger file names the release that wrote it, and the comment says when a merge adds one of a later release than the report's (T136).
~~~~

New:

~~~~text
- **Answer:** the golden set keeps the figures of each ledger format that a release wrote for as long as the report reads it (R142), and a change to a released golden session is named in the changelog (R141), so that a newer report cannot give other figures for an older hook's files unseen. Each ledger file names the release that wrote it (R156), and the comment says when a merge adds one of a later release than the report's (R193, T136).
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R142:

~~~~text
for each ledger format that a release wrote, the golden set keeps sessions whose entries are as that release wrote them, with their hand-worked figures, for as long as the report reads that format
~~~~

Clause, R141:

~~~~text
and a pull request that changes a golden session that the latest release's tag holds names it in the changelog's unreleased section
~~~~

Clause, the new unit:

~~~~text
Each ledger file names the release that wrote it
~~~~

Clause, the new unit:

~~~~text
and the comment says when a merge adds one of a later release than the report's
~~~~

Clause, the new unit:

~~~~text
T136
~~~~

### Entry

Old:

~~~~text
- **Answer:** the assumptions are listed by the highest impact among the threats that rest on them, then with the least checked first, then by the highest risk, all read from this model, and the index shows each assumption's impact beside its risk.
~~~~

New:

~~~~text
- **Answer:** the assumptions, and the ratings of their index, follow the threats that rest on them as this model rates them, impact first (R136).
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R136:

~~~~text
the assumptions are listed by the highest impact among the threats that rest on them, then with the least checked first, then by the highest risk, all read from this model, and the index shows each assumption's impact beside its risk
~~~~

### Entry

Old:

~~~~text
- **Answer:** a script, run in each pull request that rewords or adds a word to avoid, as the pull request template asks, from the copies of it and of `scripts/wording.py` that the default branch holds, in the way that its docstring gives, shows that each changed line differs only by words to avoid replaced with their terms, and lists every other change, those to `CLAUDE.md` first and those to the guide next, since the guide steers too (DR-237). It compares a renamed page with what it was, names each changed file that it does not compare, and lists apart each line that replaces a word that the base's glossary did not give for its term, since that rule is the pull request's own (T103). The review in a separate context runs those copies itself and compares their output with the one posted, reads a pull request that changes either script as a change to a check, and reads, before and after, the requirements, `CLAUDE.md`, the guide, this model's answers and residuals, the README's statements of what opting in records and publishes, and the pages that adopters act on. Each concept that a rule tells apart has a term of its own, so listing one, or its plural, as a word to avoid for another fails the check of the glossary.
~~~~

New:

~~~~text
- **Answer:** a script, run in each pull request that rewords or adds a word to avoid, as the pull request template asks, from the copies of it and of `scripts/wording.py` that the default branch holds, in the way that its docstring gives, shows that each changed line differs only by words to avoid replaced with their terms, and lists every other change, those to `CLAUDE.md` first and those to the guide next, since the guide steers too (DR-237). It compares a renamed page with what it was, names each changed file that it does not compare, and lists apart each line that replaces a word that the base's glossary did not give for its term, since that rule is the pull request's own (T103). The review in a separate context runs those copies itself and compares their output with the one posted, reads a pull request that changes either script as a change to a check, and reads, before and after, the requirements, `CLAUDE.md`, the guide, this model's answers and residuals, the README's statements of what opting in records and publishes, and the pages that adopters act on. Each concept that a rule tells apart has a term of its own, and the check of the glossary fails on one listed, or its plural, as a word to avoid for another (R138).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a script, run in each pull request that rewords or adds a word to avoid, as the pull request template asks, from the copies of it and of `scripts/wording.py` that the default branch holds, in the way that its docstring gives, shows that each changed line differs only by words to avoid replaced with their terms, and lists every other change, those to `CLAUDE.md` first and those to the guide next, since the guide steers too (DR-237). It compares a renamed page with what it was, names each changed file that it does not compare, and lists apart each line that replaces a word that the base's glossary did not give for its term, since that rule is the pull request's own (T103). The review in a separate context runs those copies itself and compares their output with the one posted, reads a pull request that changes either script as a change to a check, and reads, before and after, the requirements, `CLAUDE.md`, the guide, this model's answers and residuals, the README's statements of what opting in records and publishes, and the pages that adopters act on. Each concept that a rule tells apart has a term of its own
~~~~

Clause, R138:

~~~~text
so listing one, or its plural, as a word to avoid for another fails the check of the glossary
~~~~

### Entry

Old:

~~~~text
- **Answer:** a documented fact links, by its address shown as its text, only a vendor's page on a host that the test lists or a file at a full commit of a GitHub repository that the test lists, by a path with no `.` or `..` segment; no page of the assumptions gives a web address anywhere else; and `CLAUDE.md` says that a page that a file here links to, other than the files that steer, is data (DR-238).
~~~~

New:

~~~~text
- **Answer:** a documented fact links only a page that the test lists, by its address shown as its text (R140), and no page of the assumptions gives a web address anywhere else (R143); and `CLAUDE.md` says that a page that a file here links to, other than the files that steer, is data (DR-238).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a documented fact links
~~~~

Clause, the new unit:

~~~~text
by its address shown as its text
~~~~

Clause, R140:

~~~~text
only a vendor's page on a host that the test lists or a file at a full commit of a GitHub repository that the test lists, by a path with no `.` or `..` segment
~~~~

Clause, R143:

~~~~text
no page of the assumptions gives a web address anywhere else
~~~~

Clause, the new unit:

~~~~text
and `CLAUDE.md` says that a page that a file here links to, other than the files that steer, is data (DR-238
~~~~

### Entry

Old:

~~~~text
- **Answer:** a threat that rests on an assumption names it in a field of its own, the assumption names the threat, and a test fails when either names the other alone. Task 1.19 replaces each "(see Assumptions)" with the assumption's ID, and a script shows that each sentence of the section it moves is in an assumption or a spec afterwards.
~~~~

New:

~~~~text
- **Answer:** a test holds that each names the other, the threat in its field `Assumptions` (R135). Task 1.19 replaces each "(see Assumptions)" with the assumption's ID, and a script shows that each sentence of the section it moves is in an assumption or a spec afterwards.
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R135:

~~~~text
a threat that rests on an assumption names it in a field of its own, the assumption names the threat, and a test fails when either names the other alone
~~~~

Clause, the new unit:

~~~~text
Task 1.19 replaces each "(see Assumptions)" with the assumption's ID, and a script shows that each sentence of the section it moves is in an assumption or a spec afterwards
~~~~

### Entry

Old:

~~~~text
- **Answer:** an observation names a file under `tests/` that reproduces what was seen and holds a test that no mark skips or expects to fail, the date, and the program, version and build it was seen on, and a test fails on one that names no such file, as it does on a check that names a test that pytest does not collect or that a mark skips or expects to fail. Until a file exists, the fact is `not yet`.
~~~~

New:

~~~~text
- **Answer:** a test fails on an observation that names no file under `tests/` that reproduces what was seen (R140), and on a check that names a test that does not run (R135). Until a file exists, the fact is `not yet`.
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R140:

~~~~text
an observation names a file under `tests/` that reproduces what was seen and holds a test that no mark skips or expects to fail, the date, and the program, version and build it was seen on, and a test fails on one that names no such file
~~~~

Clause, R135:

~~~~text
as it does on a check that names a test that pytest does not collect or that a mark skips or expects to fail
~~~~

Clause, the new unit:

~~~~text
Until a file exists, the fact is `not yet`
~~~~

### Entry

Old:

~~~~text
- **Answer:** a pull request that changes a golden session that its base holds either changes a spec or changes nothing outside the golden set, and a test fails otherwise, so a slip in the set is fixed on its own and a rule change comes with its spec.
~~~~

New:

~~~~text
- **Answer:** a golden session changes alone or with a spec (R141), so a slip in the set is fixed on its own and a rule change comes with its spec.
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R141:

~~~~text
a pull request that changes a golden session that its base holds either changes a spec or changes nothing outside the golden set, and a test fails otherwise
~~~~

Clause, the new unit:

~~~~text
so a slip in the set is fixed on its own and a rule change comes with its spec
~~~~

### Entry

Old:

~~~~text
- **Answer:** the release's test job runs every expected failure as an ordinary test, which the tests that parse the workflow check, so no version is released while any acceptance test fails, and each golden test names as its expected error one that only a missing capture step or report raises, so a wrong figure fails CI on the pull request, before any tag.
~~~~

New:

~~~~text
- **Answer:** the release's test job runs every expected failure as an ordinary test, which the tests that parse the workflow check, so no version is released while any acceptance test fails, a golden test among them (R139), and each golden test names as its expected error one that only a missing capture step or report raises, so a wrong figure fails CI on the pull request, before any tag.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the release's test job runs every expected failure as an ordinary test, which the tests that parse the workflow check, so no version is released while any acceptance test fails
~~~~

Clause, the new unit:

~~~~text
and each golden test names as its expected error one that only a missing capture step or report raises, so a wrong figure fails CI on the pull request, before any tag
~~~~

### Entry

Old:

~~~~text
- **Answer:** a test fails when a fact that is not yet checked names, as the one that will check it, a task that its change's `tasks.md` ticks, and when an observation or a reading gives a date later than the day the test runs.
~~~~

New:

~~~~text
- **Answer:** a test fails on each (R135, R140).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a test fails
~~~~

Clause, R135:

~~~~text
when a fact that is not yet checked names, as the one that will check it, a task that its change's `tasks.md` ticks
~~~~

Clause, R140:

~~~~text
and when an observation or a reading gives a date later than the day the test runs
~~~~

### Entry

Old:

~~~~text
- **Answer:** the test reads every tracked file that GitHub shows as Markdown, by the extensions and the name that GitHub's language list gives the languages that it renders as Markdown. It finds a word to avoid under emphasis, with its apostrophe straight or curly, and with any run of spaces between its words, no-break spaces among them, that holds at most one line break, which it matches in one way only. The spaces after a heading's or a title's text are matched in one way too, and a line's code spans are found in one pass over its backticks; a test times each of the reader's patterns on a long run of spaces after each shape that it reads, and the reading of a line of many runs of backticks, so that neither slows the test. A fence that a list item's marker opens ends, as GitHub ends the item, at the first line that is not blank and is indented less than the fence, so the test reads that line. A fence that opens on its own line, two columns in or more, may be held by a list item or not, so the test fails on a line that GitHub reads one way in an item and another outside one, and reads no further. A blank line is one of spaces and tabs alone, and a closing fence is indented no further than GitHub allows. It leaves as written only the titles that the specs hold and an accepted record quotes where HEAD left the default branch, and it fails, naming the file, on a page that is a symbolic link, which it does not follow, on a file or a path that is not UTF-8, and on a fenced code block that never closes.
~~~~

New:

~~~~text
- **Answer:** the test reads every tracked file that GitHub shows as Markdown, by the extensions and the name that GitHub's language list gives the languages that it renders as Markdown. It finds a word to avoid under emphasis, with its apostrophe straight or curly, and with any run of spaces between its words, no-break spaces among them, that holds at most one line break, which it matches in one way only. The spaces after a heading's or a title's text are matched in one way too, and a line's code spans are found in one pass over its backticks; a test times each of the reader's patterns on a long run of spaces after each shape that it reads, and the reading of a line of many runs of backticks, so that neither slows the test. A fence that a list item's marker opens ends, as GitHub ends the item, at the first line that is not blank and is indented less than the fence, so the test reads that line. A fence that opens on its own line, two columns in or more, may be held by a list item or not, so the test fails on a line that GitHub reads one way in an item and another outside one, and reads no further. A blank line is one of spaces and tabs alone, and a closing fence is indented no further than GitHub allows. It leaves as written only the titles that the specs hold and an accepted record quotes where HEAD left the default branch, and it fails, naming the file, on a page that it cannot read whole (R137) and on a path that is not UTF-8.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the test reads every tracked file that GitHub shows as Markdown, by the extensions and the name that GitHub's language list gives the languages that it renders as Markdown. It finds a word to avoid under emphasis, with its apostrophe straight or curly, and with any run of spaces between its words, no-break spaces among them, that holds at most one line break, which it matches in one way only. The spaces after a heading's or a title's text are matched in one way too, and a line's code spans are found in one pass over its backticks; a test times each of the reader's patterns on a long run of spaces after each shape that it reads, and the reading of a line of many runs of backticks, so that neither slows the test. A fence that a list item's marker opens ends, as GitHub ends the item, at the first line that is not blank and is indented less than the fence, so the test reads that line. A fence that opens on its own line, two columns in or more, may be held by a list item or not, so the test fails on a line that GitHub reads one way in an item and another outside one, and reads no further. A blank line is one of spaces and tabs alone, and a closing fence is indented no further than GitHub allows. It leaves as written only the titles that the specs hold and an accepted record quotes where HEAD left the default branch, and it fails, naming the file, on a page that
~~~~

Clause, R137:

~~~~text
is a symbolic link, which it does not follow, on a file or
~~~~

Clause, the new unit:

~~~~text
a path that is not UTF-8
~~~~

Clause, R137:

~~~~text
and on a fenced code block that never closes
~~~~

### Entry

Old:

~~~~text
- **Answer:** each run's time is read from the system's clock in UTC, which no environment variable sets, and which the transcript's times are taken to share. A call counts only when, by each line's own time, the line it answers, which is never one of Claude Code's own bookkeeping lines, a hook's output or a system line, was written at or after the run that began its interval and no later than the call's first line, and that first line no later than the interval's last run, so that a call already being made when an interval begins is left out. A run that finds its clock earlier than the latest time that its session's runs noted, or that a line they read gave, ends each of that session's intervals, begins none, and places no call inside any of them, so that the session's next interval begins only once the clock has passed every time that its runs saw. Among those times is that of a run that finds a switch off and ends the session's interval (DR-170), so a clock set back after such a run begins no interval until it has passed that run's time.
~~~~

New:

~~~~text
- **Answer:** each run's time is read from a clock that the session's environment cannot move (R107), and which the transcript's times are taken to share. A call counts only when the line it answers and its first line fall inside an interval, by each line's own time, so that a call already being made when an interval begins is left out (R144). A clock that moves back ends the session's intervals and begins none until it has passed every time that its runs saw (R166), that of a run that finds a switch off and ends the session's interval (DR-170) among them.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each run's time is read from
~~~~

Clause, R107:

~~~~text
the system's clock in UTC, which no environment variable sets
~~~~

Clause, the new unit:

~~~~text
and which the transcript's times are taken to share
~~~~

Clause, R144:

~~~~text
A call counts only when, by each line's own time, the line it answers, which is never one of Claude Code's own bookkeeping lines, a hook's output or a system line, was written at or after the run that began its interval and no later than the call's first line, and that first line no later than the interval's last run
~~~~

Clause, the new unit:

~~~~text
so that a call already being made when an interval begins is left out
~~~~

Clause, R166:

~~~~text
A run that finds its clock earlier than the latest time that its session's runs noted, or that a line they read gave, ends each of that session's intervals, begins none, and places no call inside any of them, so that the session's next interval begins only once the clock has passed every time that its runs saw
~~~~

Clause, R166:

~~~~text
Among those times is
~~~~

Clause, the new unit:

~~~~text
that of a run that finds a switch off and ends the session's interval (DR-170
~~~~

Clause, `switch-and-opt-in`: "A clock set back past earlier lines begins no interval until it passes them":

~~~~text
so a clock set back after such a run begins no interval until it has passed that run's time
~~~~

### Entry

Old:

~~~~text
- **Answer:** a run that finds both switches on notes a fingerprint of the person's two global configuration files, each other file that git reads the opt-in key from, the repository's own git configuration among them only when it sets the key, and each link on the way to one, made of each one's device and inode numbers, size and modification times and never of its contents or its path, and kept only as a hash, and a run that notes another fingerprint than the store's last does what an opt-out does, so that the calls between those two runs, and the calls that wait to be staged, are left out.
~~~~

New:

~~~~text
- **Answer:** a run that finds both switches on notes a fingerprint of the files that git reads the opt-in from, which holds nothing of their contents (R107), and a run that notes another fingerprint than the store's last does what an opt-out does (R108, R162), so that the calls between those two runs, and the calls that wait to be staged, are left out.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a run that finds both switches on notes a fingerprint of
~~~~

Clause, R107:

~~~~text
the person's two global configuration files, each other file that git reads the opt-in key from, the repository's own git configuration among them only when it sets the key, and each link on the way to one, made of each one's device and inode numbers, size and modification times and never of its contents or its path, and kept only as a hash
~~~~

Clause, the new unit:

~~~~text
and a run that notes another fingerprint than the store's last does what an opt-out does
~~~~

Clause, the new unit:

~~~~text
so that the calls between those two runs, and the calls that wait to be staged, are left out
~~~~

### Entry

Old:

~~~~text
- **Answer:** the three flags carry no count, time or other fact about the calls left out. A flag for consent or for age goes only to the next ledger file staged for the worktree and branch of the calls left out, and one for the repository only when the call's line gives no working directory, or one inside this repository's folder or one that holds it; calls made in another repository raise none.
~~~~

New:

~~~~text
- **Answer:** the three flags carry no count, time or other fact about the calls left out, and none is raised for calls made in another repository (R155).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the three flags carry no count, time or other fact about the calls left out
~~~~

Clause, R155:

~~~~text
A flag for consent or for age goes only to the next ledger file staged for the worktree and branch of the calls left out, and one for the repository only when the call's line gives no working directory, or one inside this repository's folder or one that holds it
~~~~

Clause, R155:

~~~~text
calls made in another repository raise none
~~~~

### Entry

Old:

~~~~text
- **Answer:** the tool recomputes a pull request's cost from its ledger files, the price table and the jobs API alone, and keeps no transcript: the step writes no line of a transcript, and no value from one beyond the fields that an entry or the store's notes name, to any file, the store, a ledger file and a temporary file included, or to standard error. Keeping or reprocessing transcripts would need a change of its own, with its own specification, its own threat review and the owner's authorization.
~~~~

New:

~~~~text
- **Answer:** the tool recomputes a pull request's cost from its ledger files, the price table and the jobs API alone, and keeps no transcript (R154). Keeping or reprocessing transcripts would need a change of its own, with its own specification, its own threat review and the owner's authorization.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the tool recomputes a pull request's cost from its ledger files, the price table and the jobs API alone, and keeps no transcript
~~~~

Clause, R154:

~~~~text
the step writes no line of a transcript, and no value from one beyond the fields that an entry or the store's notes name, to any file, the store, a ledger file and a temporary file included, or to standard error
~~~~

Clause, the new unit:

~~~~text
Keeping or reprocessing transcripts would need a change of its own, with its own specification, its own threat review and the owner's authorization
~~~~

### Entry

Old:

~~~~text
- **Answer:** a call whose directory no longer exists, or names no repository that git can tell, is left out, and when that directory is inside this repository's folder or holds it, the session's next ledger file here says that calls whose repository could not be told were left out. Runs come before and after every git command, at every turn's end and at the session's end, so that the gap between a call and the run that reads it is short. A run of the plugin before a git command works first on the repository where the command runs (T19).
~~~~

New:

~~~~text
- **Answer:** a call whose directory no longer exists, or names no repository that git can tell, is left out, and when that directory is inside this repository's folder or holds it, the session's next ledger file here says that calls whose repository could not be told were left out (R147, R155). Runs come before and after every git command, at every turn's end and at the session's end, so that the gap between a call and the run that reads it is short. A run of the plugin before a git command works first on the repository where the command runs (R180, T19).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a call whose directory no longer exists, or names no repository that git can tell, is left out, and when that directory is inside this repository's folder or holds it, the session's next ledger file here says that calls whose repository could not be told were left out
~~~~

Clause, the new unit:

~~~~text
Runs come before and after every git command, at every turn's end and at the session's end, so that the gap between a call and the run that reads it is short. A run of the plugin before a git command works first on the repository where the command runs
~~~~

Clause, the new unit:

~~~~text
T19
~~~~

### Entry

Old:

~~~~text
- **Answer:** the store keeps a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` only as hashes, the ledger file's path and its worktree's name only in the note of a staged or taken-back ledger file, and its transcript's path, which carries the session's id, only in the note of a staged one, until it is resolved. Each user has a store of their own, in a folder of their own in the git common directory where the system numbers users, and each write leaves its folder with mode 0700 and its file with mode 0600, whatever the umask or the modes it found, writing a new file that the run creates itself, never through a link, so that a store that arrived looser is closed again, and nothing from the store reaches a ledger file, a comment or standard error.
~~~~

New:

~~~~text
- **Answer:** the store keeps no plain id, path or name but in the note of a ledger file that is staged or taken back, and its transcript's path, which carries the session's id, only in the note of a staged one, until it is resolved (R149, R170). Only its owner can read it (R152), and nothing from the store reaches a ledger file, a comment or standard error (R4, R89).
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R149:

~~~~text
the store keeps a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` only as hashes
~~~~

Clause, R170:

~~~~text
the ledger file's path and its worktree's name only in the note of a staged or taken-back ledger file
~~~~

Clause, the new unit:

~~~~text
and its transcript's path, which carries the session's id, only in the note of a staged one, until it is resolved
~~~~

Clause, R152:

~~~~text
Each user has a store of their own, in a folder of their own in the git common directory where the system numbers users, and each write leaves its folder with mode 0700 and its file with mode 0600, whatever the umask or the modes it found, writing a new file that the run creates itself, never through a link, so that a store that arrived looser is closed again
~~~~

Clause, the new unit:

~~~~text
and nothing from the store reaches a ledger file, a comment or standard error
~~~~

### Entry

Old:

~~~~text
- **Answer:** the store keeps nothing past its retention window of 30 days, which the owner picked on 2026-11-03: no call older than that is recorded, waiting calls, flags due and notes of taken calls that old are dropped, a dropped waiting call is flagged for its age in the next ledger file staged for its worktree and branch, a session's notes go once none of its runs has come within the window, a staged ledger file whose note is that old is taken back, and a store that holds nothing is removed, in every run that finds a store of a version that it knows, whatever the switches say.
~~~~

New:

~~~~text
- **Answer:** the store keeps nothing past its retention window of 30 days, which the owner picked on 2026-11-03 (R150), flags a waiting call that it drops for its age (R155), and removes itself once it holds nothing (R151), in every run that finds a store of a version that it knows, whatever the switches say (R145).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the store keeps nothing past its retention window of 30 days, which the owner picked on 2026-11-03
~~~~

Clause, R150:

~~~~text
no call older than that is recorded, waiting calls, flags due and notes of taken calls that old are dropped
~~~~

Clause, R155:

~~~~text
a dropped waiting call is flagged for its age in the next ledger file staged for its worktree and branch
~~~~

Clause, R150:

~~~~text
a session's notes go once none of its runs has come within the window, a staged ledger file whose note is that old is taken back
~~~~

Clause, R151:

~~~~text
and a store that holds nothing is removed
~~~~

Clause, the new unit:

~~~~text
in every run that finds a store of a version that it knows, whatever the switches say
~~~~

### Entry

Old:

~~~~text
- **Answer:** when the store is gone, or its file does not parse, which a run takes as gone and replaces, the next run that finds both switches on begins a new interval, so that no call that answers a line written before that run is recorded, however far the transcripts were read before. A ledger file staged before the removal is left to git, and the README's section on adopting the tool that task 4.4 writes says to look for one with `git status`, in every worktree that `git worktree list` names, such as those that Claude Code keeps under `.claude/worktrees/`, before removing the store.
~~~~

New:

~~~~text
- **Answer:** a store that is gone, or does not parse, lets no earlier call be recorded, however far the transcripts were read before, and leaves to git a ledger file staged before the removal (R153), and the README's section on adopting the tool that task 4.4 writes says to look for one with `git status`, in every worktree that `git worktree list` names, such as those that Claude Code keeps under `.claude/worktrees/`, before removing the store.
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R153:

~~~~text
when the store is gone, or its file does not parse, which a run takes as gone and replaces, the next run that finds both switches on begins a new interval, so that no call that answers a line written before that run is recorded
~~~~

Clause, the new unit:

~~~~text
however far the transcripts were read before
~~~~

Clause, R153:

~~~~text
A ledger file staged before the removal is left to git
~~~~

Clause, the new unit:

~~~~text
and the README's section on adopting the tool that task 4.4 writes says to look for one with `git status`, in every worktree that `git worktree list` names, such as those that Claude Code keeps under `.claude/worktrees/`, before removing the store
~~~~

### Entry

Old:

~~~~text
- **Answer:** each user's store lies in a folder of its own in the git common directory where the system numbers users, each write keeps the store its owner's alone, never through a link, and a run leaves alone a store whose file or folder is a link or, on Windows, another reparse point, is not a regular file or a folder, or, where the system numbers users, is not owned by the user that it runs as. Where the system numbers users, a run opens the store's folder once, without following a link, checks its owner and kind on what it opened, and creates, writes, renames and removes the store's files only through that opened folder, so that a folder replaced by a link between the check and the write redirects none of them. A run acts on a note only for a file of the form that the step writes, in the ledger folder of a worktree whose git common directory is this repository's, opens a note's transcript only when it is a regular file, and drops any other note, and it checks each waiting call's entry again when it stages it, by the rules that it records by, so that an entry written into the store carries nothing into a ledger file.
~~~~

New:

~~~~text
- **Answer:** each user's store is theirs alone, and a run leaves alone one that is a link, not a regular file or a folder, or another user's (R152). Where the system numbers users, a run opens the store's folder once, without following a link, checks its owner and kind on what it opened, and creates, writes, renames and removes the store's files only through that opened folder, so that a folder replaced by a link between the check and the write redirects none of them. A run acts on a note only for a file that the step writes in a worktree of this repository (R152), opens a note's transcript only when it is a regular file (R13), and it checks each waiting call's entry again when it stages it, by the rules that it records by, so that an entry written into the store carries nothing into a ledger file (R4).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each user's store
~~~~

Clause, R152:

~~~~text
lies in a folder of its own in the git common directory where the system numbers users, each write keeps the store its owner's alone, never through a link, and a run leaves alone a store whose file or folder is a link or, on Windows, another reparse point, is not a regular file or a folder, or, where the system numbers users, is not owned by the user that it runs as
~~~~

Clause, the new unit:

~~~~text
Where the system numbers users, a run opens the store's folder once, without following a link, checks its owner and kind on what it opened, and creates, writes, renames and removes the store's files only through that opened folder, so that a folder replaced by a link between the check and the write redirects none of them
~~~~

Clause, the new unit:

~~~~text
A run acts on a note only for a file
~~~~

Clause, R152:

~~~~text
of the form that the step writes, in the ledger folder of a worktree whose git common directory is this repository's
~~~~

Clause, the new unit:

~~~~text
opens a note's transcript only when it is a regular file
~~~~

Clause, R152:

~~~~text
and drops any other note
~~~~

Clause, the new unit:

~~~~text
and it checks each waiting call's entry again when it stages it, by the rules that it records by, so that an entry written into the store carries nothing into a ledger file
~~~~

### Entry

Old:

~~~~text
- **Answer:** a run that finds a switch off creates no store and adds no note of its session to one, and starts git only to find a store that exists, which it removes when it does not parse, and in one of a version that it knows only ends its own session's interval, noting its time, does what the store's notes call for, drops what the retention window ends, and removes the store when it then holds nothing.
~~~~

New:

~~~~text
- **Answer:** a run that finds a switch off creates no store and adds no note of its session to one, and starts git only for a store that exists, where it does only what R145 says (R118).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a run that finds a switch off creates no store and adds no note of its session to one
~~~~

Clause, R118:

~~~~text
and starts git only to find a store that exists
~~~~

Clause, R145:

~~~~text
which it removes when it does not parse, and in one of a version that it knows only ends its own session's interval, noting its time, does what the store's notes call for, drops what the retention window ends, and removes the store when it then holds nothing
~~~~

### Entry

Old:

~~~~text
- **Answer:** the README says where the store is and how to remove it, after looking with `git status`, in every worktree that `git worktree list` names, for a staged ledger file (T111), and the first run that comes, of any session in the repository and of a release that knows the store's version, empties the store or applies the window. A person who opts out and back in before any run comes changes a file that the fingerprint holds, so that run empties the store as an opt-out does.
~~~~

New:

~~~~text
- **Answer:** the README says where the store is and how to remove it, after looking with `git status`, in every worktree that `git worktree list` names, for a staged ledger file (T111), and the first run that comes, of any session in the repository and of a release that knows the store's version, empties the store or applies the window (R109, R150). An opt-out and back in, before any run comes, in a file that the fingerprint holds is taken as an opt-out too (R162).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the README says where the store is and how to remove it, after looking with `git status`, in every worktree that `git worktree list` names, for a staged ledger file (T111), and the first run that comes, of any session in the repository and of a release that knows the store's version, empties the store or applies the window
~~~~

Clause, R162:

~~~~text
A person who opts out and back in before any run comes changes a file that the fingerprint holds, so that run empties the store as an opt-out does
~~~~

### Entry

Old:

~~~~text
- **Answer:** each ledger file states its format's version on its first line, and the report reads each file by that version's rules, matching the version exactly as a whole number and choosing no code by its value, and counts as refused a file that states no version or one that it does not read, or that breaks its version's rules. It reads the default branch's earlier ledger files by their versions too, capture reads the branch's ledger files the same way, and every version names a call by the same id. Each entry marks whether its call was read without a stop reason or held a usage field that capture does not know, so that a restored or copied file adds no counts or flags.
~~~~

New:

~~~~text
- **Answer:** each ledger file states its format's version (R156), the report reads each file only by the version that it states, the default branch's earlier ones too (R158, R168), capture reads the branch's ledger files the same way (R167), and every version names a call by the same id (R163). Each entry marks whether its call was read without a stop reason or held a usage field that capture does not know, so that a restored or copied file adds no counts or flags (R95, R158).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each ledger file states its format's version
~~~~

Clause, R156:

~~~~text
on its first line
~~~~

Clause, R158:

~~~~text
and the report reads each file by that version's rules, matching the version exactly as a whole number and choosing no code by its value, and counts as refused a file that states no version or one that it does not read, or that breaks its version's rules
~~~~

Clause, R168:

~~~~text
It reads the default branch's earlier ledger files by their versions too
~~~~

Clause, the new unit:

~~~~text
capture reads the branch's ledger files the same way
~~~~

Clause, the new unit:

~~~~text
and every version names a call by the same id
~~~~

Clause, the new unit:

~~~~text
Each entry marks whether its call was read without a stop reason or held a usage field that capture does not know, so that a restored or copied file adds no counts or flags
~~~~

### Entry

Old:

~~~~text
- **Answer:** the README, the opt-in's feature page and the ledger's feature page say what stays published after an opt-out, a removed ledger file or a removed store, and that a hashed id does not hide whose record it is, clause by clause as DR-182 decides, and the glossary lists `anonymous` as a word to avoid, which the wording test finds in the prose of any page.
~~~~

New:

~~~~text
- **Answer:** the README, the opt-in's feature page and the ledger's feature page say what stays published after an opt-out, a removed ledger file or a removed store, and that a hashed id does not hide whose record it is, clause by clause as DR-182 decides (R159), and the glossary lists `anonymous` as a word to avoid, which the wording test finds in the prose of any page (R159).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the README, the opt-in's feature page and the ledger's feature page say what stays published after an opt-out, a removed ledger file or a removed store, and that a hashed id does not hide whose record it is, clause by clause as DR-182 decides
~~~~

Clause, the new unit:

~~~~text
and the glossary lists `anonymous` as a word to avoid, which the wording test finds in the prose of any page
~~~~

### Entry

Old:

~~~~text
- **Answer:** the store keeps a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` only as hashes, and plain names only in the note of a staged or taken-back ledger file until it is resolved; it keeps nothing past its retention window, empties itself at an opt-out and removes itself once it holds nothing. A copy put back after an opt-out brings back no call when the opt-out changed a file that the fingerprint holds, since the next run then notes another fingerprint and does what an opt-out does, and the README says where the store is, so that a person can leave it out of their backups.
~~~~

New:

~~~~text
- **Answer:** the store keeps no plain id, path or name but in the note of a ledger file until it is resolved (R149, R170), keeps nothing past its retention window (R150), empties itself at an opt-out (R109) and removes itself once it holds nothing (R151). A copy put back after an opt-out brings back no call when the opt-out changed a file that the fingerprint holds, since the next run then notes another fingerprint and does what an opt-out does (R162), and the README says where the store is, so that a person can leave it out of their backups.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the store keeps
~~~~

Clause, R149:

~~~~text
a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` only as hashes
~~~~

Clause, R170:

~~~~text
and plain names only in the note of a staged or taken-back ledger file until it is resolved
~~~~

Clause, R150:

~~~~text
it keeps nothing past its retention window
~~~~

Clause, R109:

~~~~text
empties itself at an opt-out
~~~~

Clause, R151:

~~~~text
and removes itself once it holds nothing
~~~~

Clause, the new unit:

~~~~text
A copy put back after an opt-out brings back no call when the opt-out changed a file that the fingerprint holds, since the next run then notes another fingerprint and does what an opt-out does
~~~~

Clause, the new unit:

~~~~text
and the README says where the store is, so that a person can leave it out of their backups
~~~~

### Entry

Old:

~~~~text
- **Answer:** each schema is written with ASCII patterns rather than `format`, which a validator only notes by default, and `docs/ledger-format.md` lists what no schema can hold, where the report's rules decide. The tests check, with a standard validator and its default options, that each schema refuses each line that the report refuses, but for those, and accepts each line that it counts, a property-based test compares each schema with the reader, and the surface manifest holds each released version's schema by its hash, so that a released schema cannot change unseen.
~~~~

New:

~~~~text
- **Answer:** each schema is written with ASCII patterns rather than `format`, which a validator only notes by default, and `docs/ledger-format.md` lists what no schema can hold, where the report's rules decide. The tests hold each schema to what the report refuses and counts, by a standard validator with its default options (R156), a property-based test compares each schema with the reader, and the surface manifest holds each released version's schema by its hash, so that a released schema cannot change unseen (R156).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each schema is written with ASCII patterns rather than `format`, which a validator only notes by default, and `docs/ledger-format.md` lists what no schema can hold, where the report's rules decide. The tests
~~~~

Clause, R156:

~~~~text
check, with a standard validator and its default options, that each schema refuses each line that the report refuses, but for those, and accepts each line that it counts
~~~~

Clause, the new unit:

~~~~text
a property-based test compares each schema with the reader, and the surface manifest holds each released version's schema by its hash, so that a released schema cannot change unseen
~~~~

### Entry

Old:

~~~~text
- **Answer:** every git command that the step starts runs without the session's variables whose names begin with `GIT_`, setting only its own, so that the session's environment chooses neither the repository, its index, its objects nor the files that git reads its settings from. The one exception is git's reading of the opt-in, which the step asks for twice, in the session's environment and without those variables, and capture stays on only when both readings keep it on, so that the variables can add an opt-out but neither hide one nor give consent.
~~~~

New:

~~~~text
- **Answer:** every git command that the step starts runs without the session's git variables (R169), so that the session's environment chooses neither the repository, its index, its objects nor the files that git reads its settings from. The one exception is git's reading of the opt-in, which can turn capture off but never on (R160), so that the variables can add an opt-out but neither hide one nor give consent.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** every git command that the step starts runs without the session's
~~~~

Clause, R169:

~~~~text
variables whose names begin with `GIT_`, setting only its own
~~~~

Clause, the new unit:

~~~~text
so that the session's environment chooses neither the repository, its index, its objects nor the files that git reads its settings from. The one exception is git's reading of the opt-in
~~~~

Clause, R160:

~~~~text
which the step asks for twice, in the session's environment and without those variables, and capture stays on only when both readings keep it on
~~~~

Clause, the new unit:

~~~~text
so that the variables can add an opt-out but neither hide one nor give consent
~~~~

### Entry

Old:

~~~~text
- **Answer:** the fingerprint holds the files that the owner chose on 2026-11-02, at this cost (DR-169). The README's section on adopting the tool that task 4.4 writes says which writes end an interval and what that costs, and the comment words the flag as calls that capture could not show were made while it was on, never as capture being off. The README's section on turning capture off gives `git config --global --get pr-cost.capture` to see a session's opt-in, and task 7.2 checks whether a project's thread that pauses and resumes keeps the details of the opt-in's files that the fingerprint holds.
~~~~

New:

~~~~text
- **Answer:** the fingerprint holds the files that the owner chose on 2026-11-02, at this cost (DR-169). The README's section on adopting the tool that task 4.4 writes says which writes end an interval and what that costs, and the comment never words the flag as capture being off (R157). The README's section on turning capture off gives `git config --global --get pr-cost.capture` to see a session's opt-in, and task 7.2 checks whether a project's thread that pauses and resumes keeps the details of the opt-in's files that the fingerprint holds.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the fingerprint holds the files that the owner chose on 2026-11-02, at this cost (DR-169). The README's section on adopting the tool that task 4.4 writes says which writes end an interval and what that costs
~~~~

Clause, R157:

~~~~text
and the comment words the flag as calls that capture could not show were made while it was on
~~~~

Clause, R157:

~~~~text
never as capture being off
~~~~

Clause, the new unit:

~~~~text
The README's section on turning capture off gives `git config --global --get pr-cost.capture` to see a session's opt-in, and task 7.2 checks whether a project's thread that pauses and resumes keeps the details of the opt-in's files that the fingerprint holds
~~~~

### Entry

Old:

~~~~text
- **Answer:** the opt-in's feature page, and the README's section on adopting the tool that task 4.4 writes, say where a folder's opt-out stops: a linked worktree there whose repository lies elsewhere needs the opt-out in that repository's own configuration, a condition for a folder reached through a symbolic link needs the folder's real path, and an opt-out whose file is missing does nothing, which `git config --show-origin --get-all pr-cost.capture`, run from a repository's real path there, as after `cd "$(pwd -P)"`, shows, since it lists each value with the file that gives it as the hook's reading without the session's variables and `PWD` finds them.
~~~~

New:

~~~~text
- **Answer:** the opt-in's feature page, and the README's section on adopting the tool that task 4.4 writes, say where a folder's opt-out stops (R164): a linked worktree there whose repository lies elsewhere needs the opt-out in that repository's own configuration, a condition for a folder reached through a symbolic link needs the folder's real path, and an opt-out whose file is missing does nothing, which `git config --show-origin --get-all pr-cost.capture`, run from a repository's real path there, as after `cd "$(pwd -P)"`, shows, since it lists each value with the file that gives it as the hook's reading without the session's variables and `PWD` finds them.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the opt-in's feature page, and the README's section on adopting the tool that task 4.4 writes, say where a folder's opt-out stops
~~~~

Clause, the new unit:

~~~~text
a linked worktree there whose repository lies elsewhere needs the opt-out in that repository's own configuration, a condition for a folder reached through a symbolic link needs the folder's real path, and an opt-out whose file is missing does nothing, which `git config --show-origin --get-all pr-cost.capture`, run from a repository's real path there, as after `cd "$(pwd -P)"`, shows, since it lists each value with the file that gives it as the hook's reading without the session's variables and `PWD` finds them
~~~~

### Entry

Old:

~~~~text
- **Answer:** a run that git refuses records no call, creates no store, stages no ledger file and exits with success, never asking git to trust the folder, and since the step runs git without the session's `GIT_` variables (DR-188), a `safe.directory` setting that only those variables give does not count. The README's section on adopting the tool that task 4.4 writes says that a clone that git does not trust records nothing until a `safe.directory` setting in the person's global configuration, or the system's, names it, and that adding one to the person's global configuration ends every open interval in their other repositories, as any write to it does (T120).
~~~~

New:

~~~~text
- **Answer:** a run that git refuses records nothing and exits with success, never asking git to trust the folder, and since the step runs git without the session's `GIT_` variables (DR-188), a `safe.directory` setting that only those variables give does not count (R147). The README's section on adopting the tool that task 4.4 writes says that a clone that git does not trust records nothing until a `safe.directory` setting in the person's global configuration, or the system's, names it, and that adding one to the person's global configuration ends every open interval in their other repositories, as any write to it does (T120).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a run that git refuses
~~~~

Clause, R147:

~~~~text
records no call, creates no store, stages no ledger file and exits with success
~~~~

Clause, the new unit:

~~~~text
never asking git to trust the folder, and since the step runs git without the session's `GIT_` variables (DR-188), a `safe.directory` setting that only those variables give does not count
~~~~

Clause, the new unit:

~~~~text
The README's section on adopting the tool that task 4.4 writes says that a clone that git does not trust records nothing until a `safe.directory` setting in the person's global configuration, or the system's, names it, and that adding one to the person's global configuration ends every open interval in their other repositories, as any write to it does (T120)
~~~~

### Entry

Old:

~~~~text
- **Answer:** the surface manifest names each key that the configuration's format documents, with the values that each takes, so the release check refuses a release that adds or drops one without a raised major number and a `### Breaking` section (DR-096, DR-123). The comment of the pull request that adds the key says that it changed the tool's configuration and that the tool is off after the merge, each merge that then finds the tool off at both commits says why in its job summary (DR-191), and a hook file at another commit than the report's is named in the comment (DR-139). The README's section on adopting the tool that task 4.4 writes says to add such a key only with or after the pull request that moves the hook file and the calling workflow's pin to that version, and to drop one that a later version no longer documents before or with it. Where the plugin and the hook file's registration both run, a copy of an earlier release leaves the session to the later one, and the README says that a person keeps their plugin current (T136).
~~~~

New:

~~~~text
- **Answer:** the surface manifest names each key that the configuration's format documents (R122), so the release check refuses a release that adds or drops one without a raised major number and a `### Breaking` section (R123, DR-096, DR-123). The comment of the pull request that adds the key says that it changed the tool's configuration and that the tool is off after the merge (R171, R172), each merge that then finds the tool off at both commits says why in its job summary (R172, DR-191), and a hook file at another commit than the report's is named in the comment (R65, DR-139). The README's section on adopting the tool that task 4.4 writes says to add such a key only with or after the pull request that moves the hook file and the calling workflow's pin to that version, and to drop one that a later version no longer documents before or with it. Where the plugin and the hook file's registration both run, a copy of an earlier release leaves the session to the later one (R191), and the README says that a person keeps their plugin current (R195, T136).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the surface manifest names each key that the configuration's format documents
~~~~

Clause, R122:

~~~~text
with the values that each takes
~~~~

Clause, the new unit:

~~~~text
so the release check refuses a release that adds or drops one without a raised major number and a `### Breaking` section (
~~~~

Clause, the new unit:

~~~~text
DR-096, DR-123). The comment of the pull request that adds the key says that it changed the tool's configuration and that the tool is off after the merge
~~~~

Clause, the new unit:

~~~~text
each merge that then finds the tool off at both commits says why in its job summary (
~~~~

Clause, the new unit:

~~~~text
DR-191), and a hook file at another commit than the report's is named in the comment (
~~~~

Clause, the new unit:

~~~~text
DR-139). The README's section on adopting the tool that task 4.4 writes says to add such a key only with or after the pull request that moves the hook file and the calling workflow's pin to that version, and to drop one that a later version no longer documents before or with it. Where the plugin and the hook file's registration both run, a copy of an earlier release leaves the session to the later one
~~~~

Clause, the new unit:

~~~~text
and the README says that a person keeps their plugin current (
~~~~

Clause, the new unit:

~~~~text
T136)
~~~~

### Entry

Old:

~~~~text
- **Answer:** `tests/test_spec_form.py` reads every `spec.md` that OpenSpec reads, at any depth, line by line as OpenSpec reads it, and fails on a scenario out of form or with the name of another scenario in its spec, on a heading out of form or out of place, on a line that OpenSpec or GitHub alone reads as a fence or a heading, after a list's or a quote's marker among them, on text before a spec's first section, on a label line or a scenario's line in a requirement's text, and on a `spec.md` that it does not read (DR-193). CI compares its reading of each spec and change with what the pinned OpenSpec CLI shows for it, so that a release that reads specs otherwise, or a defect in the test's reader, fails CI in the pull request that brings it (DR-196).
~~~~

New:

~~~~text
- **Answer:** `tests/test_spec_form.py` reads every `spec.md` that OpenSpec reads, at any depth, line by line as OpenSpec reads it, and fails on a spec out of form or one that it does not read (R173, R174, R175, R177, DR-193). CI compares its reading of each spec and change with what the pinned OpenSpec CLI shows for it, so that a release that reads specs otherwise, or a defect in the test's reader, fails CI in the pull request that brings it (R178, DR-196).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** `tests/test_spec_form.py` reads every `spec.md` that OpenSpec reads, at any depth, line by line as OpenSpec reads it, and fails
~~~~

Clause, R174:

~~~~text
on a scenario out of form or with the name of another scenario in its spec
~~~~

Clause, R175:

~~~~text
on a heading out of form or out of place, on a line that OpenSpec or GitHub alone reads as a fence or a heading, after a list's or a quote's marker among them, on text before a spec's first section
~~~~

Clause, R173:

~~~~text
on a label line
~~~~

Clause, R174:

~~~~text
or a scenario's line in a requirement's text
~~~~

Clause, R177:

~~~~text
and on a `spec.md` that it does not read
~~~~

Clause, the new unit:

~~~~text
DR-193
~~~~

Clause, the new unit:

~~~~text
). CI compares its reading of each spec and change with what the pinned OpenSpec CLI shows for it, so that a release that reads specs otherwise, or a defect in the test's reader, fails CI in the pull request that brings it (
~~~~

Clause, the new unit:

~~~~text
DR-196)
~~~~

### Entry

Old:

~~~~text
- **Answer:** `tests/test_spec_form.py` fails, naming the spec, the line and what it holds, on a spec that holds a character other than printable ASCII and line breaks, a run of backticks that no run as long closes on its line, or, outside inline code, a `<`, an `&`, a backslash, a `|`, a `](`, a `]:`, a `$` or a `~` (DR-195).
~~~~

New:

~~~~text
- **Answer:** `tests/test_spec_form.py` fails, naming the spec, the line and what it holds, on a spec that holds text that GitHub would hide or show otherwise (R176, DR-195).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** `tests/test_spec_form.py` fails, naming the spec, the line and what it holds
~~~~

Clause, R176:

~~~~text
on a spec that holds a character other than printable ASCII and line breaks, a run of backticks that no run as long closes on its line, or, outside inline code, a `<`, an `&`, a backslash, a `|`, a `](`, a `]:`, a `$` or a `~`
~~~~

Clause, the new unit:

~~~~text
DR-195)
~~~~

### Entry

Old:

~~~~text
- **Answer:** the test checks each spec's bytes as plain text before it splits them into lines, and fails naming the spec on bytes that are not UTF-8. Its patterns match a line in one way only, and a test times the reading of a line of many spaces and of one of many backticks. It fails on every symbolic link in `openspec/` outside the archive, which it never follows, and it reports each problem only in a test's failure message. The comparison starts each line that it prints with `verify-openspec: `, shows each name, path and text from a spec or from the CLI with every character outside printable ASCII replaced by its code point, and quotes the requirements only of a spec that the test reads too, naming one that only the CLI reads by its path alone, so that no line of a spec or of the CLI's output starts a line of either output.
~~~~

New:

~~~~text
- **Answer:** the test checks each spec's bytes as plain text before it splits them into lines, and fails naming the spec on bytes that are not UTF-8 (R176). Its patterns match a line in one way only, and a test times the reading of a line of many spaces and of one of many backticks. It fails on every symbolic link in `openspec/` outside the archive, which it never follows (R177), and it reports each problem only in a test's failure message. The comparison starts each line that it prints with `verify-openspec: `, shows each name, path and text from a spec or from the CLI with every character outside printable ASCII replaced by its code point, and quotes the requirements only of a spec that the test reads too, naming one that only the CLI reads by its path alone, so that no line of a spec or of the CLI's output starts a line of either output.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the test checks each spec's bytes as plain text before it splits them into lines, and fails naming the spec on bytes that are not UTF-8
~~~~

Clause, the new unit:

~~~~text
Its patterns match a line in one way only, and a test times the reading of a line of many spaces and of one of many backticks. It fails on every symbolic link in `openspec/` outside the archive, which it never follows
~~~~

Clause, the new unit:

~~~~text
and it reports each problem only in a test's failure message. The comparison starts each line that it prints with `verify-openspec: `, shows each name, path and text from a spec or from the CLI with every character outside printable ASCII replaced by its code point, and quotes the requirements only of a spec that the test reads too, naming one that only the CLI reads by its path alone, so that no line of a spec or of the CLI's output starts a line of either output
~~~~

### Entry

Old:

~~~~text
- **Answer:** such calls are left out, as every call whose repository cannot be told is, and the session's next ledger file in each clone that turns the tool on says that calls whose repository could not be told were left out, so that the comment says that the token cost, each of its parts and the total are lower bounds. The README's section on cloud threads says that these calls are left out and flagged, and how to keep a session's work inside a repository, such as by asking Claude in the project's instructions to work from inside it, since one `cd` into a clone does not keep it there, since Claude's current directory can go back to the thread's folder. The README's section on cloud threads also says that a call made from one clone counts there, whatever clone it works on, so that a project that holds a repository that turns the tool on should hold no repository whose work must stay private, and this repository turns the tool on only from a project that holds it alone, with the owner's opt-in only in that project's own environment, so that only that project's threads record here (DR-207, DR-210).
~~~~

New:

~~~~text
- **Answer:** such calls are left out, as every call whose repository cannot be told is, and flagged in the session's next ledger file in each clone that turns the tool on (R155), so that the comment says that the figure is a lower bound (R157). The README's section on cloud threads says that these calls are left out and flagged, and how to keep a session's work inside a repository, such as by asking Claude in the project's instructions to work from inside it (R185). The README's section on cloud threads also says that a call made from one clone counts there, whatever clone it works on, so that a project that holds a repository that turns the tool on should hold no repository whose work must stay private (R185), and this repository turns the tool on only from a project that holds it alone, with the owner's opt-in only in that project's own environment, so that only that project's threads record here (DR-207, DR-210).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** such calls are left out, as every call whose repository cannot be told is, and
~~~~

Clause, R155:

~~~~text
the session's next ledger file in each clone that turns the tool on says that calls whose repository could not be told were left out
~~~~

Clause, the new unit:

~~~~text
so that the comment says that
~~~~

Clause, R157:

~~~~text
the token cost, each of its parts and the total are lower bounds
~~~~

Clause, the new unit:

~~~~text
The README's section on cloud threads says that these calls are left out and flagged, and how to keep a session's work inside a repository, such as by asking Claude in the project's instructions to work from inside it
~~~~

Clause, R185:

~~~~text
since one `cd` into a clone does not keep it there, since Claude's current directory can go back to the thread's folder
~~~~

Clause, the new unit:

~~~~text
The README's section on cloud threads also says that a call made from one clone counts there, whatever clone it works on, so that a project that holds a repository that turns the tool on should hold no repository whose work must stay private
~~~~

Clause, the new unit:

~~~~text
and this repository turns the tool on only from a project that holds it alone, with the owner's opt-in only in that project's own environment, so that only that project's threads record here (DR-207, DR-210)
~~~~

### Entry

Old:

~~~~text
- **Answer:** a run records in each repository only the calls whose line gives a working directory in it, and nothing reaches a ledger file there until a commit is made there, whose diff shows the file, though a project's thread can commit and push with no one reading it. A plugin run meets a repository only through the project directory, a folder directly inside it, Claude's current directory or a git command run there, never by walking deeper. The opt-in's pages say that one opt-in covers every repository that turns the tool on, with the plugin wherever Claude works or runs a git command, and how a person turns capture off for a folder with git's own conditional includes (DR-185), and a repository's own git configuration can turn it off there (DR-050).
~~~~

New:

~~~~text
- **Answer:** a run records in each repository only the calls whose line gives a working directory in it (R180), and nothing reaches a ledger file there until a commit is made there, whose diff shows the file, though a project's thread can commit and push with no one reading it. A plugin run meets a repository only through the project directory, a folder directly inside it, Claude's current directory or a git command run there, never by walking deeper (R180). The opt-in's pages say that one opt-in covers every repository that turns the tool on, with the plugin wherever Claude works or runs a git command, and how a person turns capture off for a folder with git's own conditional includes (R164, DR-185), and a repository's own git configuration can turn it off there (R39, DR-050).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a run records in each repository only the calls whose line gives a working directory in it
~~~~

Clause, the new unit:

~~~~text
and nothing reaches a ledger file there until a commit is made there, whose diff shows the file, though a project's thread can commit and push with no one reading it. A plugin run meets a repository only through the project directory, a folder directly inside it, Claude's current directory or a git command run there, never by walking deeper
~~~~

Clause, the new unit:

~~~~text
The opt-in's pages say that one opt-in covers every repository that turns the tool on, with the plugin wherever Claude works or runs a git command, and how a person turns capture off for a folder with git's own conditional includes (
~~~~

Clause, the new unit:

~~~~text
DR-185), and a repository's own git configuration can turn it off there (
~~~~

Clause, the new unit:

~~~~text
DR-050)
~~~~

### Entry

Old:

~~~~text
- **Answer:** every copy works through the same store of each repository, under its lock, so that each call is recorded once, by its message id, and a run before a command for which another run has staged a ledger file stages nothing more. A run that finds the store at a version that it does not know records, stages, takes back and puts back nothing there, and leaves the store, and the session's calls there, to the copy whose release wrote it (T44). Every release that writes a store version keeps its path, its lock and its fields and makes its fingerprint the same way, which a test holds for each version, and whose recorded hash the checks hold unchanged once a published release has written that version, and each run that finds both switches on notes, for its session, the latest release whose copy has run in it, so that a run of an earlier release records, stages, takes back, puts back and ends nothing for that session there, and leaves it to the later release's copy, unless it finds the person's own capture off, which it acts on as any run does, so that an opt-out is acted on even where the later copy no longer runs. The README's section on installing the plugin says what happens when the plugin and the repository's hook file are of different releases, and that only one copy of a plugin's name runs its hooks.
~~~~

New:

~~~~text
- **Answer:** every copy works through the same store of each repository, under its lock, so that each call is recorded once, by its message id, and a run before a command for which another run has staged a ledger file stages nothing more (R181). A run that finds the store at a version that it does not know leaves the store, and the session's calls there, to the copy whose release wrote it (R55, R181, T44). Every release that writes a store version keeps its path, its lock and its fields and makes its fingerprint the same way (R192), and each run that finds both switches on notes, for its session, the latest release whose copy has run in it, so that a run of an earlier release leaves the session to the later release's copy, unless it finds the person's own capture off, so that an opt-out is acted on even where the later copy no longer runs (R191). The README's section on installing the plugin says what happens when the plugin and the repository's hook file are of different releases, and that only one copy of a plugin's name runs its hooks (R195).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** every copy works through the same store of each repository, under its lock, so that each call is recorded once, by its message id, and a run before a command for which another run has staged a ledger file stages nothing more
~~~~

Clause, the new unit:

~~~~text
A run that finds the store at a version that it does not know
~~~~

Clause, R55:

~~~~text
records, stages, takes back and puts back nothing there, and
~~~~

Clause, the new unit:

~~~~text
leaves the store, and the session's calls there, to the copy whose release wrote it (
~~~~

Clause, the new unit:

~~~~text
T44). Every release that writes a store version keeps its path, its lock and its fields and makes its fingerprint the same way
~~~~

Clause, R192:

~~~~text
which a test holds for each version, and whose recorded hash the checks hold unchanged once a published release has written that version
~~~~

Clause, the new unit:

~~~~text
and each run that finds both switches on notes, for its session, the latest release whose copy has run in it, so that a run of an earlier release
~~~~

Clause, R191:

~~~~text
records, stages, takes back, puts back and ends nothing for that session there, and leaves it to the later release's copy
~~~~

Clause, the new unit:

~~~~text
unless it finds the person's own capture off
~~~~

Clause, R191:

~~~~text
which it acts on as any run does
~~~~

Clause, the new unit:

~~~~text
so that an opt-out is acted on even where the later copy no longer runs
~~~~

Clause, the new unit:

~~~~text
The README's section on installing the plugin says what happens when the plugin and the repository's hook file are of different releases, and that only one copy of a plugin's name runs its hooks
~~~~

### Entry

Old:

~~~~text
- **Answer:** none in the tool beyond what a fresh clone already brings: its first run begins a new interval, so the calls that answer a line written before that run are left out and flagged for consent, and the comment says that the figure is a lower bound. The README's section on cloud threads says that a machine that cannot be resumed loses the calls that no commit took, so that a person who wants them counted commits as the work goes.
~~~~

New:

~~~~text
- **Answer:** none in the tool beyond what a fresh clone already brings: its first run begins a new interval, so the calls that answer a line written before that run are left out and flagged for consent (R153, R155), and the comment says that the figure is a lower bound. The README's section on cloud threads says that a machine that cannot be resumed loses the calls that no commit took, so that a person who wants them counted commits as the work goes (R185).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** none in the tool beyond what a fresh clone already brings: its first run begins a new interval, so the calls that answer a line written before that run are left out and flagged for consent
~~~~

Clause, the new unit:

~~~~text
and the comment says that the figure is a lower bound. The README's section on cloud threads says that a machine that cannot be resumed loses the calls that no commit took, so that a person who wants them counted commits as the work goes
~~~~

### Entry

Old:

~~~~text
- **Answer:** the root marketplace file holds only the marketplace's name, its owner and one entry that names the tool's plugin and its folder, and CI fails when it holds anything else (T140). The folder holds the plugin exactly as a published release's tag builds it, with that release's version in its manifest, and CI fails when, compared by path, mode and content, it differs from what that tag's own build script builds, holds anything but regular files, or gives a version that no published release, found by its tag's full name in the default branch's first-parent history, has, or a lower one than at the base (T137, T138). A pull request that adds, changes or removes the root file, or changes the folder, changes nothing else, and the folder moves only after a release, in a pull request that the owner reviews and merges, while only an identity that agent sessions never hold can create a tag (T67). The README gives the zip first, each update of which is the person's own act after a check, says that a marketplace's update arrives when the person checks for updates, or by itself once they turn on syncing, with nothing to accept once it has synced, and that a fixed release comes from its zip, since a release's own tag holds an earlier release's plugin. The owner merges a pull request that changes the root file or the folder only when its diff changes nothing else, since its CI runs the checks as that pull request leaves them (T137). The README's short start says that the marketplace's updates need no approval, beside the zip, whose checksum a person checks first.
~~~~

New:

~~~~text
- **Answer:** the root marketplace file holds only the marketplace's name, its owner and one entry that names the tool's plugin and its folder, and CI fails when it holds anything else (R190, T140). The folder holds the plugin exactly as a published release's tag builds it, with that release's version in its manifest, and CI fails when it differs from what that tag's own build script builds or gives a version that no published release, found by its tag's full name in the default branch's first-parent history, has, or a lower one than at the base (R184, T137, T138). A pull request that adds, changes or removes the root file, or changes the folder, changes nothing else (R190), and the folder moves only after a release, in a pull request that the owner reviews and merges, while only an identity that agent sessions never hold can create a tag (T67). The README gives the zip first, each update of which is the person's own act after a check, and says how a marketplace's updates arrive and where a fixed release comes from (R187). The owner merges a pull request that changes the root file or the folder only when its diff changes nothing else, since its CI runs the checks as that pull request leaves them (T137). The README's short start says that the marketplace's updates need no approval (R198).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the root marketplace file holds only the marketplace's name, its owner and one entry that names the tool's plugin and its folder, and CI fails when it holds anything else (
~~~~

Clause, the new unit:

~~~~text
T140). The folder holds the plugin exactly as a published release's tag builds it, with that release's version in its manifest, and CI fails when
~~~~

Clause, R184:

~~~~text
compared by path, mode and content
~~~~

Clause, the new unit:

~~~~text
it differs from what that tag's own build script builds
~~~~

Clause, R184:

~~~~text
holds anything but regular files
~~~~

Clause, the new unit:

~~~~text
or gives a version that no published release, found by its tag's full name in the default branch's first-parent history, has, or a lower one than at the base (
~~~~

Clause, the new unit:

~~~~text
T137, T138). A pull request that adds, changes or removes the root file, or changes the folder, changes nothing else
~~~~

Clause, the new unit:

~~~~text
and the folder moves only after a release, in a pull request that the owner reviews and merges, while only an identity that agent sessions never hold can create a tag (T67). The README gives the zip first, each update of which is the person's own act after a check
~~~~

Clause, R187:

~~~~text
says that a marketplace's update arrives when the person checks for updates, or by itself once they turn on syncing, with nothing to accept once it has synced, and that a fixed release comes from its zip, since a release's own tag holds an earlier release's plugin
~~~~

Clause, the new unit:

~~~~text
The owner merges a pull request that changes the root file or the folder only when its diff changes nothing else, since its CI runs the checks as that pull request leaves them (T137). The README's short start says that the marketplace's updates need no approval
~~~~

Clause, R198:

~~~~text
beside the zip, whose checksum a person checks first
~~~~

### Entry

Old:

~~~~text
- **Answer:** each release carries the zip built from its tag alone, holding only the plugin, stored uncompressed with every header field fixed, the system that made it among them, so that every build on any system gives the same bytes, whose SHA-256 the README at the tag's commit gives. CI fails on a pull request after which the zip built from its tree, on Linux and on Windows, has another SHA-256 than its README gives, so that a mistake shows before any tag, and the release workflow publishes no release whose zip has another SHA-256, while the release's bill of materials names it too. The README's section on installing the plugin gives the command that checks a zip's SHA-256 against the README at the release's commit before it is uploaded, and says that a zip follows no address. The README's short start says to check the zip's checksum against that release's README before uploading it, and links that section.
~~~~

New:

~~~~text
- **Answer:** each release carries the zip built from its tag alone, holding only the plugin, stored uncompressed with every header field fixed, the system that made it among them, so that every build on any system gives the same bytes (R183), whose SHA-256 the README at the tag's commit gives. CI fails on a pull request after which the zip built from its tree has another SHA-256 than its README gives, so that a mistake shows before any tag, and the release workflow publishes no release whose zip has another SHA-256 (R183), while the release's bill of materials names it too (R28). The README's section on installing the plugin gives the command that checks a zip's SHA-256 against the README at the release's commit before it is uploaded, and says that a zip follows no address (R187). The README's short start says to check the zip's checksum against that release's README before uploading it, and links that section (R198).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each release carries the zip built from its tag alone, holding only the plugin, stored uncompressed with every header field fixed, the system that made it among them, so that every build on any system gives the same bytes
~~~~

Clause, the new unit:

~~~~text
whose SHA-256 the README at the tag's commit gives. CI fails on a pull request after which the zip built from its tree
~~~~

Clause, R183:

~~~~text
on Linux and on Windows
~~~~

Clause, the new unit:

~~~~text
has another SHA-256 than its README gives, so that a mistake shows before any tag, and the release workflow publishes no release whose zip has another SHA-256
~~~~

Clause, the new unit:

~~~~text
while the release's bill of materials names it too
~~~~

Clause, the new unit:

~~~~text
The README's section on installing the plugin gives the command that checks a zip's SHA-256 against the README at the release's commit before it is uploaded, and says that a zip follows no address
~~~~

Clause, the new unit:

~~~~text
The README's short start says to check the zip's checksum against that release's README before uploading it, and links that section
~~~~

### Entry

Old:

~~~~text
- **Answer:** the opt-in is set by the person, or by the setup script of the environment that they use, and having the plugin, which an organization can turn on for its members or require, opts no one in. A person turns capture off in a running session with `git config --global pr-cost.capture false`, and in each session of an environment that they can change, from its next restore, with the three `GIT_CONFIG_` variables that set the key to false, since an opt-out that git reads in the session's environment turns capture off (T119), and the variables outlast a rewrite of the global configuration file, such as a setup script makes on a rebuilt machine or an organization's hook at a session's start or resume, or after `/clear` or a compaction. The README's short start says that a person's own line goes in a cloud environment that only they use, tells an organization to tell its members before it opts them in, and says what is then published. Its section on organizations says how an organization turns the plugin on and puts the line in a shared environment, which sessions each reaches, that a member who has picked no environment uses the organization's default, that sharing an environment, or making it the default, shares the line in its setup script with every member who uses it and with a Claude Tag channel's sessions, so that an Owner takes their own line out first, that a member sees a shared environment read-only, so that an opt-out in a session there holds only until its machine is rebuilt and a member refuses the line for good only by working in an environment of their own, that its managed settings can also opt members in (T155), that the organization tells its members first what is then published, and that its opt-in also records each agent that a later release adds (T176), that a person's own line belongs in an environment of their own, and how a member sees what turns capture on, with git's `--show-origin` and `/hooks`, and turns it off.
~~~~

New:

~~~~text
- **Answer:** the opt-in is set by the person, or by the setup script of the environment that they use, and having the plugin, which an organization can turn on for its members or require, opts no one in (R1, R182). A person turns capture off in a running session with `git config --global pr-cost.capture false`, and in each session of an environment that they can change, from its next restore, with the three `GIT_CONFIG_` variables that set the key to false, since an opt-out that git reads in the session's environment turns capture off (R160, T119), and the variables outlast a rewrite of the global configuration file, such as a setup script makes on a rebuilt machine or an organization's hook at a session's start or resume, or after `/clear` or a compaction (R194). The README's short start says that a person's own line goes in a cloud environment that only they use, tells an organization to tell its members before it opts them in, and says what is then published (R198, R199). Its section on organizations says how an organization turns the plugin on and puts the line in a shared environment, what sharing an environment and its managed settings do to its members' opt-ins (T155), that the organization tells its members first what is then published, and that its opt-in also records each agent that a later release adds (T176), and how a member sees what turns capture on, with git's `--show-origin` and `/hooks`, and turns it off (R186).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the opt-in is set by the person, or by the setup script of the environment that they use, and having the plugin, which an organization can turn on for its members or require, opts no one in
~~~~

Clause, the new unit:

~~~~text
A person turns capture off in a running session with `git config --global pr-cost.capture false`, and in each session of an environment that they can change, from its next restore, with the three `GIT_CONFIG_` variables that set the key to false, since an opt-out that git reads in the session's environment turns capture off (
~~~~

Clause, the new unit:

~~~~text
T119), and the variables outlast a rewrite of the global configuration file, such as a setup script makes on a rebuilt machine or an organization's hook at a session's start or resume, or after `/clear` or a compaction
~~~~

Clause, the new unit:

~~~~text
The README's short start says that a person's own line goes in a cloud environment that only they use, tells an organization to tell its members before it opts them in, and says what is then published
~~~~

Clause, the new unit:

~~~~text
Its section on organizations says how an organization turns the plugin on and puts the line in a shared environment
~~~~

Clause, R186:

~~~~text
which sessions each reaches, that a member who has picked no environment uses the organization's default, that sharing an environment, or making it the default, shares the line in its setup script with every member who uses it and with a Claude Tag channel's sessions, so that an Owner takes their own line out first, that a member sees a shared environment read-only, so that an opt-out in a session there holds only until its machine is rebuilt and a member refuses the line for good only by working in an environment of their own, that its managed settings can also opt members in
~~~~

Clause, the new unit:

~~~~text
(T155), that the organization tells its members first what is then published, and that its opt-in also records each agent that a later release adds (T176)
~~~~

Clause, R186:

~~~~text
that a person's own line belongs in an environment of their own
~~~~

Clause, the new unit:

~~~~text
and how a member sees what turns capture on, with git's `--show-origin` and `/hooks`, and turns it off
~~~~

### Entry

Old:

~~~~text
- **Answer:** a repository's settings can already run any hook in a session that trusts its folder (A62), so a plugin of the same name gives it no power that it lacks. The plugin's name is part of the public surface, so it does not change but in a major release, and the README's section on installing the plugin says that only one copy of a plugin's name runs its hooks, how to see which one in a terminal session, and what a cloud session shows.
~~~~

New:

~~~~text
- **Answer:** a repository's settings can already run any hook in a session that trusts its folder (A62), so a plugin of the same name gives it no power that it lacks. The plugin's name is part of the public surface, so it does not change but in a major release (R122, R123), and the README's section on installing the plugin says that only one copy of a plugin's name runs its hooks, how to see which one in a terminal session, and what a cloud session shows (R195).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a repository's settings can already run any hook in a session that trusts its folder (A62), so a plugin of the same name gives it no power that it lacks. The plugin's name is part of the public surface, so it does not change but in a major release
~~~~

Clause, the new unit:

~~~~text
and the README's section on installing the plugin says that only one copy of a plugin's name runs its hooks, how to see which one in a terminal session, and what a cloud session shows
~~~~

### Entry

Old:

~~~~text
- **Answer:** each ledger file's first line states, beside its format's version, the release of the capture step that wrote it, both in a place and form that every version of the format keeps, and when a ledger file that a merge adds names a later release than the report's own, whatever its version, the comment says that some ledger files come from a later release than the report, so that lines or files that the report cannot read may be refused, and quotes nothing from them. Where the plugin and the hook file's registration both run, a copy of an earlier release leaves the session to the later one, but for an opt-out (T130). The README's section on installing the plugin says that the plugin's release, not the repository's pinned report, writes the ledger files of the sessions that run it, what a later or an earlier plugin then does, and that a repository keeps its pin current and a person keeps their plugin current. The README's short start says that the marketplace's updates need no approval, so that a person who adds it knows that each new release reaches their sessions with nothing to accept.
~~~~

New:

~~~~text
- **Answer:** each ledger file's first line states, beside its format's version, the release of the capture step that wrote it, both in a place and form that every version of the format keeps (R156), and when a ledger file that a merge adds names a later release than the report's own, whatever its version, the comment says that some ledger files come from a later release than the report, so that lines or files that the report cannot read may be refused, and quotes nothing from them (R193). Where the plugin and the hook file's registration both run, a copy of an earlier release leaves the session to the later one, but for an opt-out (R191, T130). The README's section on installing the plugin says that the plugin's release, not the repository's pinned report, writes the ledger files of the sessions that run it, what a later or an earlier plugin then does, and that a repository keeps its pin current and a person keeps their plugin current (R195). The README's short start says that the marketplace's updates need no approval, so that a person who adds it knows that each new release reaches their sessions with nothing to accept (R198).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each ledger file's first line states, beside its format's version, the release of the capture step that wrote it, both in a place and form that every version of the format keeps
~~~~

Clause, the new unit:

~~~~text
and when a ledger file that a merge adds names a later release than the report's own, whatever its version, the comment says that some ledger files come from a later release than the report, so that lines or files that the report cannot read may be refused, and quotes nothing from them
~~~~

Clause, the new unit:

~~~~text
Where the plugin and the hook file's registration both run, a copy of an earlier release leaves the session to the later one, but for an opt-out (
~~~~

Clause, the new unit:

~~~~text
T130). The README's section on installing the plugin says that the plugin's release, not the repository's pinned report, writes the ledger files of the sessions that run it, what a later or an earlier plugin then does, and that a repository keeps its pin current and a person keeps their plugin current
~~~~

Clause, the new unit:

~~~~text
The README's short start says that the marketplace's updates need no approval, so that a person who adds it knows that each new release reaches their sessions with nothing to accept
~~~~

### Entry

Old:

~~~~text
- **Answer:** the check compares the folder with what the release tag's own build script builds, run with `python3 -I`, never with the pull request's build, and fails a pull request that adds, changes or removes the root marketplace file, or changes the folder that it names, together with anything else, so that a change to the check, the build script or the workflow comes in a pull request of its own, which the owner reviews as such. The checks are on the default branch before the root file comes back, in a pull request that changes no marketplace file, so that the pull request that brings the marketplace back is held by checks that it does not change. That check runs as the pull request leaves it, so the owner merges a pull request that changes the root file or the folder only when its diff changes nothing else, a rule that no change to CI undoes (A15).
~~~~

New:

~~~~text
- **Answer:** the check compares the folder with what the release tag's own build script builds, never with the pull request's build (R184), and fails a pull request that changes the marketplace together with anything else (R190), so that a change to the check, the build script or the workflow comes in a pull request of its own, which the owner reviews as such. The checks are on the default branch before the root file comes back, in a pull request that changes no marketplace file, so that the pull request that brings the marketplace back is held by checks that it does not change. That check runs as the pull request leaves it, so the owner merges a pull request that changes the root file or the folder only when its diff changes nothing else, a rule that no change to CI undoes (A15).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the check compares the folder with what the release tag's own build script builds
~~~~

Clause, R184:

~~~~text
run with `python3 -I`
~~~~

Clause, the new unit:

~~~~text
never with the pull request's build
~~~~

Clause, the new unit:

~~~~text
and fails a pull request that
~~~~

Clause, R190:

~~~~text
adds, changes or removes the root marketplace file, or changes the folder that it names, together with anything else
~~~~

Clause, the new unit:

~~~~text
so that a change to the check, the build script or the workflow comes in a pull request of its own, which the owner reviews as such. The checks are on the default branch before the root file comes back, in a pull request that changes no marketplace file, so that the pull request that brings the marketplace back is held by checks that it does not change. That check runs as the pull request leaves it, so the owner merges a pull request that changes the root file or the folder only when its diff changes nothing else, a rule that no change to CI undoes (A15)
~~~~

### Entry

Old:

~~~~text
- **Answer:** the check takes a release's tag by its full name, `refs/tags/v<version>`, passes the folder only when that tag's commit is in the default branch's first-parent history and a published release has its version, and refuses a version lower than the one at the pull request's base. The owner deletes a refused release's tag, with its draft, and its version is never tagged again (DR-209). The README's sections on installing the plugin and on adopting the tool say that a tag with no published release is not a version to pin or install, its short start says to pin a published release, and its section on organizations says to register the marketplace with no `ref`. The release workflow refuses a tag whose root marketplace file lists any plugin but the tool's. Until this repository's root marketplace file holds an entry for the tool's plugin, the README's status says that the marketplace does not serve it yet, which a test holds against that file, and the short start is written only once the root marketplace file, which lists the vendored Superpowers, is removed, so that a person who adds the marketplace from the short start is never offered that plugin.
~~~~

New:

~~~~text
- **Answer:** the check takes a release's tag by its full name, `refs/tags/v<version>`, passes the folder only when that tag's commit is in the default branch's first-parent history and a published release has its version, and refuses a version lower than the one at the pull request's base (R184). The owner deletes a refused release's tag, with its draft, and its version is never tagged again (DR-209). The README's sections on installing the plugin and on adopting the tool say that a tag with no published release is not a version to pin or install (R195, R203), its short start says to pin a published release (R198), and its section on organizations says to register the marketplace with no `ref` (R186). The release workflow refuses a tag whose root marketplace file lists any plugin but the tool's (R190). Until this repository's root marketplace file holds an entry for the tool's plugin, the README's status says that the marketplace does not serve it yet, which a test holds against that file (R205), and the short start is written only once the root marketplace file, which lists the vendored Superpowers, is removed, so that a person who adds the marketplace from the short start is never offered that plugin.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the check takes a release's tag by its full name, `refs/tags/v<version>`, passes the folder only when that tag's commit is in the default branch's first-parent history and a published release has its version, and refuses a version lower than the one at the pull request's base
~~~~

Clause, the new unit:

~~~~text
The owner deletes a refused release's tag, with its draft, and its version is never tagged again (DR-209). The README's sections on installing the plugin and on adopting the tool say that a tag with no published release is not a version to pin or install
~~~~

Clause, the new unit:

~~~~text
its short start says to pin a published release
~~~~

Clause, the new unit:

~~~~text
and its section on organizations says to register the marketplace with no `ref`
~~~~

Clause, the new unit:

~~~~text
The release workflow refuses a tag whose root marketplace file lists any plugin but the tool's
~~~~

Clause, the new unit:

~~~~text
Until this repository's root marketplace file holds an entry for the tool's plugin, the README's status says that the marketplace does not serve it yet, which a test holds against that file
~~~~

Clause, the new unit:

~~~~text
and the short start is written only once the root marketplace file, which lists the vendored Superpowers, is removed, so that a person who adds the marketplace from the short start is never offered that plugin
~~~~

### Entry

Old:

~~~~text
- **Answer:** the release workflow creates each release as a draft, attaches its plugin's zip and its bill of materials, downloads each attached file again and checks its size and SHA-256 against the file that it built, and only then publishes the release; when an attachment fails or differs, the release stays a draft, the workflow fails and names the file, and nothing is published. The tests hold the order of the workflow's calls against recorded responses.
~~~~

New:

~~~~text
- **Answer:** the release workflow publishes a release only once each file attached to its draft, downloaded again, matches the file that it built, so that no release is published without its zip and its bill of materials (R189). The tests hold the order of the workflow's calls against recorded responses.
~~~~

Clause, the new unit:

~~~~text
- **Answer:**
~~~~

Clause, R189:

~~~~text
the release workflow creates each release as a draft, attaches its plugin's zip and its bill of materials, downloads each attached file again and checks its size and SHA-256 against the file that it built, and only then publishes the release; when an attachment fails or differs, the release stays a draft, the workflow fails and names the file, and nothing is published
~~~~

Clause, the new unit:

~~~~text
The tests hold the order of the workflow's calls against recorded responses
~~~~

### Entry

Old:

~~~~text
- **Answer:** the root marketplace file holds only the marketplace's name, its owner and one entry that gives the tool's plugin's name and its folder, and CI fails when the file, parsed, holds any other key, value or entry. The check that the plugin's hooks match the hook file's registration reads them from every file that can declare them. The owner merges a pull request that changes the root file only when its diff changes nothing else (T137).
~~~~

New:

~~~~text
- **Answer:** the root marketplace file holds only the marketplace's name, its owner and one entry that gives the tool's plugin's name and its folder, and CI fails when the file, parsed, holds any other key, value or entry (R190). The check that the plugin's hooks match the hook file's registration reads them from every file that can declare them (R179). The owner merges a pull request that changes the root file only when its diff changes nothing else (T137).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the root marketplace file holds only the marketplace's name, its owner and one entry that gives the tool's plugin's name and its folder, and CI fails when the file, parsed, holds any other key, value or entry
~~~~

Clause, the new unit:

~~~~text
The check that the plugin's hooks match the hook file's registration reads them from every file that can declare them
~~~~

Clause, the new unit:

~~~~text
The owner merges a pull request that changes the root file only when its diff changes nothing else (T137)
~~~~

### Entry

Old:

~~~~text
- **Answer:** the plugin that each commit builds has a manifest that holds no key but its name, version, description, author, licence and repository, hooks that are all command hooks, and the hook file, byte for byte, as its capture step; CI fails on a pull request whose tree builds a plugin where any of these does not hold, and the release workflow publishes no release where any does not. The zip, and the marketplace's folder, which CI compares with what the release's tag builds, hold only the manifest, the hooks, the capture step and the licence, so a file that Claude Code reads from a default path is refused too.
~~~~

New:

~~~~text
- **Answer:** the plugin that each commit builds has a manifest that holds no key but its name, version, description, author, licence and repository, hooks that are all command hooks, and the hook file, byte for byte, as its capture step; CI fails, and no release is published, where any of these does not hold (R188). The zip, and the marketplace's folder, which CI compares with what the release's tag builds, hold only the manifest, the hooks, the capture step and the licence (R183, R184), so a file that Claude Code reads from a default path is refused too.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the plugin that each commit builds has a manifest that holds no key but its name, version, description, author, licence and repository, hooks that are all command hooks, and the hook file, byte for byte, as its capture step
~~~~

Clause, R188:

~~~~text
CI fails on a pull request whose tree builds a plugin where any of these does not hold, and the release workflow publishes no release where any does not
~~~~

Clause, the new unit:

~~~~text
The zip, and the marketplace's folder, which CI compares with what the release's tag builds, hold only the manifest, the hooks, the capture step and the licence
~~~~

Clause, the new unit:

~~~~text
so a file that Claude Code reads from a default path is refused too
~~~~

### Entry

Old:

~~~~text
- **Answer:** the account's name and the repository's are among the settings the owner keeps, so that neither changes while the marketplace is served from them. The README gives the release's zip first, which follows no address once it is uploaded, and says so.
~~~~

New:

~~~~text
- **Answer:** the account's name and the repository's are among the settings the owner keeps, so that neither changes while the marketplace is served from them. The README gives the release's zip first, which follows no address once it is uploaded, and says so (R187).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the account's name and the repository's are among the settings the owner keeps, so that neither changes while the marketplace is served from them. The README gives the release's zip first, which follows no address once it is uploaded, and says so
~~~~

### Entry

Old:

~~~~text
- **Answer:** both commands take each CRLF in the step as LF before they compare its SHA-256, so that a checkout that changes only its line endings runs the step, while a change to any other byte, a lone carriage return among them, runs none of it. The zip is built from the tag's files as git's objects hold them, never from a checkout. CI fails when the repository's attributes give the hook file, or a file in the plugin folder that the root marketplace file names, `working-tree-encoding`, `ident` or `filter`, in any state.
~~~~

New:

~~~~text
- **Answer:** both commands take each CRLF in the step as LF before they compare its SHA-256, so that a checkout that changes only its line endings runs the step, while a change to any other byte, a lone carriage return among them, runs none of it (R88, R179). The zip is built from the tag's files as git's objects hold them, never from a checkout (R183). CI fails on an attribute that would change the checkout of the hook file or of the plugin's files (R134).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** both commands take each CRLF in the step as LF before they compare its SHA-256, so that a checkout that changes only its line endings runs the step, while a change to any other byte, a lone carriage return among them, runs none of it
~~~~

Clause, the new unit:

~~~~text
The zip is built from the tag's files as git's objects hold them, never from a checkout
~~~~

Clause, R134:

~~~~text
CI fails when the repository's attributes give the hook file, or a file in the plugin folder that the root marketplace file names, `working-tree-encoding`, `ident` or `filter`, in any state
~~~~

### Entry

Old:

~~~~text
- **Answer:** outside the repository that holds the project directory, a plugin run starts a git command that can start a program that a repository's configuration names, as one that reads the index or the attributes can, only where a git command of its input runs, or to take back a ledger file that its own session staged there, and leaves any other take-back or put-back there to the first run that may make it. It reads the opt-in and finds the store with `git config` and `git rev-parse`, which start neither program (A21), so that in a repository that the session only meets or moves into, its intervals still begin and its calls are still recorded.
~~~~

New:

~~~~text
- **Answer:** outside the repository that holds the project directory, a plugin run starts a git command that can start a program that a repository's configuration names, as one that reads the index or the attributes can, only where a git command of its input runs, or to take back a ledger file that its own session staged there, and leaves any other take-back or put-back there to the first run that may make it (R197). It reads the opt-in and finds the store with `git config` and `git rev-parse`, which start neither program (A21), so that in a repository that the session only meets or moves into, its intervals still begin and its calls are still recorded (R197).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** outside the repository that holds the project directory, a plugin run starts a git command that can start a program that a repository's configuration names, as one that reads the index or the attributes can, only where a git command of its input runs, or to take back a ledger file that its own session staged there, and leaves any other take-back or put-back there to the first run that may make it
~~~~

Clause, the new unit:

~~~~text
It reads the opt-in and finds the store with `git config` and `git rev-parse`, which start neither program (A21), so that in a repository that the session only meets or moves into, its intervals still begin and its calls are still recorded
~~~~

### Entry

Old:

~~~~text
- **Answer:** the short start itself, read as GitHub shows it, says before any step that opts anyone in that turning the tool on in a repository records only the sessions of people who are opted in, that one opt-in covers every repository that turns the tool on and every agent that the tool records, later ones too, that a call counts in the repository that it is made from, whatever repository it works on, that what a session spends is committed with its work and can be traced to the person, that pushing that work publishes it, even after an opt-out, and that it stays published, and its step for an organization says to tell its members before it opts them in. A test fails when it leaves out any of these, or gives one only after a step that opts anyone in. Each section of detail shows its heading, so that a reader sees what its folded text covers.
~~~~

New:

~~~~text
- **Answer:** the short start itself, read as GitHub shows it, says before any step that opts anyone in what an opt-in records and publishes. A test fails when it leaves out any of these, or gives one only after a step that opts anyone in (R199). Each section of detail shows its heading, so that a reader sees what its folded text covers (R200).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the short start itself, read as GitHub shows it, says before any step that opts anyone in
~~~~

Clause, R199:

~~~~text
that turning the tool on in a repository records only the sessions of people who are opted in, that one opt-in covers every repository that turns the tool on and every agent that the tool records, later ones too, that a call counts in the repository that it is made from, whatever repository it works on, that what a session spends is committed with its work and can be traced to the person, that pushing that work publishes it, even after an opt-out, and that it stays published, and its step for an organization says to tell its members before it opts them in
~~~~

Clause, the new unit:

~~~~text
A test fails when it leaves out any of these, or gives one only after a step that opts anyone in
~~~~

Clause, the new unit:

~~~~text
Each section of detail shows its heading, so that a reader sees what its folded text covers
~~~~

### Entry

Old:

~~~~text
- **Answer:** a test fails when a command in the short start's code is not given, as written, in the README's section that the short start links for that step, its opt-in's line in both the section on the opt-in and the section on cloud threads, when its opt-in is not `git config --global pr-cost.capture true` or its way to stop is not `git config --global pr-cost.capture false`, as the specs give them, so that a change to both the short start and a section fails it too, or when the marketplace's address that it gives is not the one that the section on installing the plugin gives. The tests of task 4.4 hold the commands of those sections to what the specs ask of them.
~~~~

New:

~~~~text
- **Answer:** a test fails when a command of the short start differs from the section that it links for that step or from what the specs give, so that a change to both the short start and a section fails it too (R198). The tests of task 4.4 hold the commands of those sections to what the specs ask of them.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a test fails when
~~~~

Clause, R198:

~~~~text
a command in the short start's code is not given, as written, in the README's section that the short start links for that step, its opt-in's line in both the section on the opt-in and the section on cloud threads, when its opt-in is not `git config --global pr-cost.capture true` or its way to stop is not `git config --global pr-cost.capture false`, as the specs give them
~~~~

Clause, the new unit:

~~~~text
so that a change to both the short start and a section fails it too
~~~~

Clause, R198:

~~~~text
or when the marketplace's address that it gives is not the one that the section on installing the plugin gives
~~~~

Clause, the new unit:

~~~~text
The tests of task 4.4 hold the commands of those sections to what the specs ask of them
~~~~

### Entry

Old:

~~~~text
- **Answer:** a test fails when a link of the short start names anything but a heading of the README or this repository's latest release by its full address, and another when a link, an autolink, a web address or an `owner/repo` anywhere in the README, in its opening, its short start, its folded detail and its code, names anything but a heading of the README, a file of this repository by a relative path, an address on the test's list, or, at `github.com` or `raw.githubusercontent.com`, this repository, its latest release, or a release, a release's file, a file or a folder at a release's tag or a placeholder, since GitHub serves under this repository's address a commit that only a fork holds (A26), a pull request's head, a fork's too, as `refs/pull/<number>/head` (A48), and what others write, such as a pull request, an issue or a comparison with a fork's branch (A26), and a third when the `.github` folder holds a README (A9). The owner reads every diff before merging it.
~~~~

New:

~~~~text
- **Answer:** a test fails when a link of the short start names anything but a heading of the README or this repository's latest release by its full address (R198), and another when a link, an autolink, a web address or an `owner/repo` anywhere in the README names anything but a heading of the README, a file of this repository by a relative path, an address on the test's list, or, at `github.com` or `raw.githubusercontent.com`, this repository, its latest release, or a release, a release's file, a file or a folder at a release's tag or a placeholder (R201), since GitHub serves under this repository's address a commit that only a fork holds (A26), a pull request's head, a fork's too, as `refs/pull/<number>/head` (A48), and what others write, such as a pull request, an issue or a comparison with a fork's branch (A26), and a third when the `.github` folder holds a README (R198, A9). The owner reads every diff before merging it.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a test fails when a link of the short start names anything but a heading of the README or this repository's latest release by its full address
~~~~

Clause, the new unit:

~~~~text
and another when a link, an autolink, a web address or an `owner/repo` anywhere in the README
~~~~

Clause, R201:

~~~~text
in its opening, its short start, its folded detail and its code
~~~~

Clause, the new unit:

~~~~text
names anything but a heading of the README, a file of this repository by a relative path, an address on the test's list, or, at `github.com` or `raw.githubusercontent.com`, this repository, its latest release, or a release, a release's file, a file or a folder at a release's tag or a placeholder
~~~~

Clause, the new unit:

~~~~text
since GitHub serves under this repository's address a commit that only a fork holds (A26), a pull request's head, a fork's too, as `refs/pull/<number>/head` (A48), and what others write, such as a pull request, an issue or a comparison with a fork's branch (A26), and a third when the `.github` folder holds a README (
~~~~

Clause, the new unit:

~~~~text
A9). The owner reads every diff before merging it
~~~~

### Entry

Old:

~~~~text
- **Answer:** the short start names this repository's marketplace by its `owner/repo`, in code, and links this repository's latest release by its full address, so that an unchanged copy of the README still sends its readers here, and a test fails when the marketplace's address that it gives is not the one that the section on installing the plugin gives. Every other address in the README is on the test's list or is one of the few of this repository's that the test allows (T147).
~~~~

New:

~~~~text
- **Answer:** the short start names this repository's marketplace by its `owner/repo`, in code, and links this repository's latest release by its full address, so that an unchanged copy of the README still sends its readers here, and a test fails when the marketplace's address that it gives is not the one that the section on installing the plugin gives (R198). Every other address in the README is on the test's list or is one of the few of this repository's that the test allows (R201, T147).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the short start names this repository's marketplace by its `owner/repo`, in code, and links this repository's latest release by its full address, so that an unchanged copy of the README still sends its readers here, and a test fails when the marketplace's address that it gives is not the one that the section on installing the plugin gives
~~~~

Clause, the new unit:

~~~~text
Every other address in the README is on the test's list or is one of the few of this repository's that the test allows (
~~~~

Clause, the new unit:

~~~~text
T147)
~~~~

### Entry

Old:

~~~~text
- **Answer:** the short start holds no HTML, and a test fails when it holds a `<details>` element, an HTML comment or any other element. The test of what it says reads it as GitHub shows it, and fails when it gives what an opt-in publishes only after a step that opts anyone in. The test of its commands also compares its opt-in and its way to stop with the commands that the specs give, and its opt-in's line with both the section on the opt-in and the section on cloud threads (T146).
~~~~

New:

~~~~text
- **Answer:** the short start holds no HTML, and a test fails otherwise (R198). The test of what it says reads it as GitHub shows it, and fails when it gives what an opt-in publishes only after a step that opts anyone in (R199). The test of its commands also compares its opt-in and its way to stop with the commands that the specs give, and its opt-in's line with both the section on the opt-in and the section on cloud threads (R198, T146).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the short start holds no HTML, and a test fails
~~~~

Clause, R198:

~~~~text
when it holds a `<details>` element, an HTML comment or any other element
~~~~

Clause, the new unit:

~~~~text
The test of what it says reads it as GitHub shows it, and fails when it gives what an opt-in publishes only after a step that opts anyone in
~~~~

Clause, the new unit:

~~~~text
The test of its commands also compares its opt-in and its way to stop with the commands that the specs give, and its opt-in's line with both the section on the opt-in and the section on cloud threads (
~~~~

Clause, the new unit:

~~~~text
T146)
~~~~

### Entry

Old:

~~~~text
- **Answer:** the README holds no text that GitHub hides or shows otherwise: a test fails when it holds an attribute on the `<details>` and `<summary>` elements that fold its sections of detail, a character other than printable ASCII and a line break, a code block whose opening fence gives anything but a language on the test's list, which holds none that GitHub draws as a diagram, a map, a model or mathematics, or, outside code, a `<` that does not open or close one of those elements, which refuses every comment, other element, processing instruction, declaration and CDATA section, a `]:`, which refuses every link reference definition and footnote's definition, a character reference, a mathematical expression, an image, a link with a title, or a link whose target holds a query or a fragment that names no heading of the README, and names the line and what it holds.
~~~~

New:

~~~~text
- **Answer:** the README holds no text that GitHub hides or shows otherwise: a test fails when it holds any, and names the line and what it holds (R200).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the README holds no text that GitHub hides or shows otherwise: a test fails when it holds
~~~~

Clause, R200:

~~~~text
an attribute on the `<details>` and `<summary>` elements that fold its sections of detail, a character other than printable ASCII and a line break, a code block whose opening fence gives anything but a language on the test's list, which holds none that GitHub draws as a diagram, a map, a model or mathematics, or, outside code, a `<` that does not open or close one of those elements, which refuses every comment, other element, processing instruction, declaration and CDATA section, a `]:`, which refuses every link reference definition and footnote's definition, a character reference, a mathematical expression, an image, a link with a title, or a link whose target holds a query or a fragment that names no heading of the README
~~~~

Clause, the new unit:

~~~~text
and names the line and what it holds
~~~~

### Entry

Old:

~~~~text
- **Answer:** the short start says to check the zip's checksum against that release's README, and the section on adopting the tool says to take the hook file, its registration and the calling workflow from the README at the commit that a published release names. When the merged commit's `.claude/settings.json` or `.claude/settings.local.json` registers the hook's command with a checksum other than the SHA-256 of the hook file at that commit, the comment says that the hook's registration does not run the repository's hook file, and quotes nothing from either file.
~~~~

New:

~~~~text
- **Answer:** the short start says to check the zip's checksum against that release's README, and the section on adopting the tool says to take the hook file, its registration and the calling workflow from the README at the commit that a published release names (R198, R203). When the merged commit's `.claude/settings.json` or `.claude/settings.local.json` registers the hook's command with a checksum other than the SHA-256 of the hook file at that commit, the comment says so and quotes nothing from either file (R202).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the short start says to check the zip's checksum against that release's README, and the section on adopting the tool says to take the hook file, its registration and the calling workflow from the README at the commit that a published release names
~~~~

Clause, the new unit:

~~~~text
When the merged commit's `.claude/settings.json` or `.claude/settings.local.json` registers the hook's command with a checksum other than the SHA-256 of the hook file at that commit
~~~~

Clause, R202:

~~~~text
the comment says that the hook's registration does not run the repository's hook file, and quotes nothing from either file
~~~~

### Entry

Old:

~~~~text
- **Answer:** the section on adopting the tool says that a tag with no published release is not a version to pin, so that a pin, an update bot's included, is taken only once a published release names its commit, and the short start says to pin a published release. The owner deletes a refused release's tag, with its draft, and its version is never tagged again (DR-209).
~~~~

New:

~~~~text
- **Answer:** the section on adopting the tool says that a tag with no published release is not a version to pin, so that a pin, an update bot's included, is taken only once a published release names its commit (R203), and the short start says to pin a published release (R198). The owner deletes a refused release's tag, with its draft, and its version is never tagged again (DR-209).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the section on adopting the tool says that a tag with no published release is not a version to pin, so that a pin, an update bot's included, is taken only once a published release names its commit
~~~~

Clause, the new unit:

~~~~text
and the short start says to pin a published release
~~~~

Clause, the new unit:

~~~~text
The owner deletes a refused release's tag, with its draft, and its version is never tagged again (DR-209)
~~~~

### Entry

Old:

~~~~text
- **Answer:** the short start's way to stop says to run the opt-out on each machine and in each running session, and to take the line out of any setup script or use an environment without it, and the short start says, before any step that opts anyone in, that pushing a session's work publishes what it spent, even after an opt-out. The section on turning capture off says that taking the line out, or using another environment, reaches only the sessions that start, or whose machines are rebuilt, afterwards, and gives the command for a running session.
~~~~

New:

~~~~text
- **Answer:** the short start's way to stop says to run the opt-out on each machine and in each running session, and to take the line out of any setup script or use an environment without it, and the short start says, before any step that opts anyone in, that pushing a session's work publishes what it spent, even after an opt-out (R198, R199). The section on turning capture off says that taking the line out, or using another environment, reaches only the sessions that start, or whose machines are rebuilt, afterwards, and gives the command for a running session (R194).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the short start's way to stop says to run the opt-out on each machine and in each running session, and to take the line out of any setup script or use an environment without it, and the short start says, before any step that opts anyone in, that pushing a session's work publishes what it spent, even after an opt-out
~~~~

Clause, the new unit:

~~~~text
The section on turning capture off says that taking the line out, or using another environment, reaches only the sessions that start, or whose machines are rebuilt, afterwards, and gives the command for a running session
~~~~

### Entry

Old:

~~~~text
- **Answer:** the README's section on organizations gives a hook that writes the opt-in only when `CLAUDE_CODE_REMOTE` is `true`, which Claude Code sets in cloud sessions and never locally, and `git config --global --get pr-cost.capture` does not already give `true`, so that it leaves alone a file that already opts the member in, says that a hook without the first condition writes the opt-in into a member's own git configuration on their own computer, where it stays after the hook goes and after they leave, and records each agent that later releases add, has an organization that stops tell its members to turn capture off on each computer, and says how a member sees what turns capture on, with git's `--show-origin` and `/hooks`, and turns it off. Task 4.4's tests run that hook against a git configuration of their own, and show that it writes nothing outside a cloud session, leaves a file that already opts the member in untouched, since git writes the file anew even to set the value that it holds (A51), and writes the opt-in otherwise. The short start says that an organization that opted a person in can do so again.
~~~~

New:

~~~~text
- **Answer:** the README's section on organizations gives a hook that writes the opt-in only when `CLAUDE_CODE_REMOTE` is `true`, which Claude Code sets in cloud sessions and never locally, and `git config --global --get pr-cost.capture` does not already give `true`, so that it leaves alone a file that already opts the member in, says what a hook without the first condition leaves on a member's own computer, and has an organization that stops tell its members to turn capture off on each computer (R186). Task 4.4's tests run that hook against a git configuration of their own, and show that it writes nothing outside a cloud session, leaves a file that already opts the member in untouched, since git writes the file anew even to set the value that it holds (A51), and writes the opt-in otherwise. The short start says that an organization that opted a person in can do so again (R198).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the README's section on organizations gives a hook that writes the opt-in only when `CLAUDE_CODE_REMOTE` is `true`, which Claude Code sets in cloud sessions and never locally, and `git config --global --get pr-cost.capture` does not already give `true`, so that it leaves alone a file that already opts the member in
~~~~

Clause, R186:

~~~~text
says that a hook without the first condition writes the opt-in into a member's own git configuration on their own computer, where it stays after the hook goes and after they leave, and records each agent that later releases add
~~~~

Clause, the new unit:

~~~~text
has an organization that stops tell its members to turn capture off on each computer
~~~~

Clause, R186:

~~~~text
and says how a member sees what turns capture on, with git's `--show-origin` and `/hooks`, and turns it off
~~~~

Clause, the new unit:

~~~~text
Task 4.4's tests run that hook against a git configuration of their own, and show that it writes nothing outside a cloud session, leaves a file that already opts the member in untouched, since git writes the file anew even to set the value that it holds (A51), and writes the opt-in otherwise. The short start says that an organization that opted a person in can do so again
~~~~

### Entry

Old:

~~~~text
- **Answer:** the README's section on turning capture off says that a repository whose `.claude/settings.json` sets `remote.defaultEnvironmentId` chooses the environment of the cloud sessions that `claude --cloud` starts from its clone, over the person's own pick, which the person keeps with the same key in the clone's `.claude/settings.local.json`.
~~~~

New:

~~~~text
- **Answer:** the README's section on turning capture off says that a repository whose `.claude/settings.json` sets `remote.defaultEnvironmentId` chooses the environment of the cloud sessions that `claude --cloud` starts from its clone, over the person's own pick, which the person keeps with the same key in the clone's `.claude/settings.local.json` (R194).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the README's section on turning capture off says that a repository whose `.claude/settings.json` sets `remote.defaultEnvironmentId` chooses the environment of the cloud sessions that `claude --cloud` starts from its clone, over the person's own pick, which the person keeps with the same key in the clone's `.claude/settings.local.json`
~~~~

### Entry

Old:

~~~~text
- **Answer:** the report reads each settings file as a blob within a size bound of their own, and leaves out, without stopping, one that is not a regular file, is above that bound, is not JSON that it can read, nested too deep for Python's JSON reader among them, or is JSON in which a value on the way to a hook's command is not of the type it has in a registration, saying nothing of a registration there and quoting nothing from it, which a test holds with each of these planted, at a depth on which the running Python's reader raises and within that bound.
~~~~

New:

~~~~text
- **Answer:** the report reads each settings file as a blob within a size bound of their own, and leaves out, without stopping, one that is not a regular file, is above that bound, is not JSON that it can read, nested too deep for Python's JSON reader among them, or is JSON in which a value on the way to a hook's command is not of the type it has in a registration, saying nothing of a registration there and quoting nothing from it (R202), which a test holds with each of these planted, at a depth on which the running Python's reader raises and within that bound.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the report reads each settings file as a blob within a size bound of their own, and leaves out, without stopping, one that is not a regular file, is above that bound, is not JSON that it can read, nested too deep for Python's JSON reader among them, or is JSON in which a value on the way to a hook's command is not of the type it has in a registration, saying nothing of a registration there and quoting nothing from it
~~~~

Clause, the new unit:

~~~~text
which a test holds with each of these planted, at a depth on which the running Python's reader raises and within that bound
~~~~

### Entry

Old:

~~~~text
- **Answer:** the README's sections on the opt-in, on a project's cloud threads and on organizations say that a person sets their own opt-in, or their organization does once it has told them, and that an agent that sets the tool up turns capture on for no one, in a git configuration file, a setup script, an environment's variables or managed settings, and leaves the opt-in to whoever asked it. The section on the opt-in sits inside the section on adopting the tool, which the short start's step for a repository links, so an agent that sets a repository up reads it there. The guide, which the README's list of documentation links and which says that agents follow it, opens by saying that it speaks to work on this repository, not to setting the tool up, which is the README's section on adopting it, and that an agent that sets the tool up turns capture on for no one (R219, DR-231).
~~~~

New:

~~~~text
- **Answer:** the README's sections on the opt-in, on a project's cloud threads and on organizations leave the opt-in to the person, or to their organization once it has told them, and say that an agent that sets the tool up turns capture on for no one (R204). The section on the opt-in sits inside the section on adopting the tool, which the short start's step for a repository links, so an agent that sets a repository up reads it there. The guide, which the README's list of documentation links and which says that agents follow it, opens by saying that it speaks to work on this repository, not to setting the tool up, which is the README's section on adopting it, and that an agent that sets the tool up turns capture on for no one (R219, DR-231).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the README's sections on the opt-in, on a project's cloud threads and on organizations
~~~~

Clause, R204:

~~~~text
say that a person sets their own opt-in, or their organization does once it has told them, and
~~~~

Clause, the new unit:

~~~~text
that an agent that sets the tool up turns capture on for no one
~~~~

Clause, R204:

~~~~text
in a git configuration file, a setup script, an environment's variables or managed settings, and leaves the opt-in to whoever asked it
~~~~

Clause, the new unit:

~~~~text
The section on the opt-in sits inside the section on adopting the tool, which the short start's step for a repository links, so an agent that sets a repository up reads it there. The guide, which the README's list of documentation links and which says that agents follow it, opens by saying that it speaks to work on this repository, not to setting the tool up, which is the README's section on adopting it, and that an agent that sets the tool up turns capture on for no one (R219, DR-231)
~~~~

### Entry

Old:

~~~~text
- **Answer:** `CLAUDE.md` names the roadmap and the backlog items among the pages that describe and never tell an agent what to do, and says that an item is not, by being there, a request to start it: work on one starts only when the person the agent works for asks for it, and an item is built only while the default branch gives its status as `Planned` or `In progress`, whatever a branch says. Compared with the base commit, a test fails on an item added as in progress, done or dropped, and on one moved from open or dropped straight to in progress or done, so that an item is agreed by a change to its status line that the owner's merge accepts. The roadmap opens, and the backlog's page says, that an item is not a request to start work, and Later opens by saying to every reader that an item open to feedback and contributions starts with an issue, that an item is built only once it is planned, and that some items need a spec, a threat review and the owner's decision first; tests fail when they do not. Each gap on the guide names the backlog item that closes it, and a test fails while that item is done or dropped (R226); the guide opens by saying to every reader that a gap is not, by being there, a request to start work, that it closes only through the backlog item that it names, that work outside that item leaves what the gap concerns as it stands, and that a principle knowingly accepted is accepted only where its record says (R219), and `CLAUDE.md` says the same, so that a gap closes only once its item is built. `CLAUDE.md`'s rule that the specs are the single source has an agent write a finding into a spec only once the person it works for asks it to (DR-232). Nothing merges but by the owner.
~~~~

New:

~~~~text
- **Answer:** `CLAUDE.md` names the roadmap and the backlog items among the pages that describe and never tell an agent what to do, and says that an item is not, by being there, a request to start it: work on one starts only when the person the agent works for asks for it, and an item is built only while the default branch gives its status as `Planned` or `In progress`, whatever a branch says. Compared with the base commit, a test fails on an item that skips agreement (R218), so that an item is agreed by a change to its status line that the owner's merge accepts. The roadmap opens, and the backlog's page says, that an item is not a request to start work, and Later opens by saying to every reader that an item open to feedback and contributions starts with an issue, that an item is built only once it is planned, and that some items need a spec, a threat review and the owner's decision first; tests fail when they do not (R214, R217). Each gap on the guide names the backlog item that closes it, and a test fails while that item is done or dropped (R226); the guide opens by saying to every reader that a gap is not, by being there, a request to start work, that it closes only through the backlog item that it names, that work outside that item leaves what the gap concerns as it stands, and that a principle knowingly accepted is accepted only where its record says (R219), and `CLAUDE.md` says the same, so that a gap closes only once its item is built. `CLAUDE.md`'s rule that the specs are the single source has an agent write a finding into a spec only once the person it works for asks it to (DR-232). Nothing merges but by the owner.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** `CLAUDE.md` names the roadmap and the backlog items among the pages that describe and never tell an agent what to do, and says that an item is not, by being there, a request to start it: work on one starts only when the person the agent works for asks for it, and an item is built only while the default branch gives its status as `Planned` or `In progress`, whatever a branch says. Compared with the base commit, a test fails on an item
~~~~

Clause, R218:

~~~~text
added as in progress, done or dropped, and on one moved from open or dropped straight to in progress or done
~~~~

Clause, the new unit:

~~~~text
so that an item is agreed by a change to its status line that the owner's merge accepts. The roadmap opens, and the backlog's page says, that an item is not a request to start work, and Later opens by saying to every reader that an item open to feedback and contributions starts with an issue, that an item is built only once it is planned, and that some items need a spec, a threat review and the owner's decision first; tests fail when they do not
~~~~

Clause, the new unit:

~~~~text
Each gap on the guide names the backlog item that closes it, and a test fails while that item is done or dropped (R226); the guide opens by saying to every reader that a gap is not, by being there, a request to start work, that it closes only through the backlog item that it names, that work outside that item leaves what the gap concerns as it stands, and that a principle knowingly accepted is accepted only where its record says (R219), and `CLAUDE.md` says the same, so that a gap closes only once its item is built. `CLAUDE.md`'s rule that the specs are the single source has an agent write a finding into a spec only once the person it works for asks it to (DR-232). Nothing merges but by the owner
~~~~

### Entry

Old:

~~~~text
- **Answer:** each backlog item gives one of five statuses, and a test fails on one that has none of them; the roadmap lists each open item once, by a line that gives its title, status, date and brief as the item does, and lists no item that is done or dropped, and a test fails otherwise. The roadmap opens, and the backlog's page says, that an item describes and is neither a promise nor a date, and the page says what each status means and that `Done` means merged, with `CHANGELOG.md` naming the release that holds it; tests fail when they do not. Compared with the base commit, a test fails on an item whose text a branch changes while its date stays before the base's, and on an item removed or renamed. Each item names what it rests on, those under Next and Later at least one ID, and a test fails on an ID that does not exist, in active and archived changes alike, on an item that names a closed record and on an open item whose tasks are all ticked. A test fails on a record that the README's list of what the first version does not support links and that no item under Later names. The README's briefing says that what an issue proposes is neither planned nor committed to. `CLAUDE.md`'s rule on documentation and the pull request template ask that a pull request that finishes, adds or moves an item changes the item and the roadmap with it.
~~~~

New:

~~~~text
- **Answer:** each backlog item gives one of five statuses (R207), and the roadmap lists each open item as the item gives it and lists no item that is done or dropped (R213), so that the roadmap's line says what the item says and an item finished or dropped leaves the roadmap. The roadmap opens, and the backlog's page says, that an item describes and is neither a promise nor a date (R206, R217), so that no item reads as a commitment. An item's date moves with its text and the item keeps its file (R216), and an item names only what exists and is not stale (R215), so that an item whose work or ground has moved on fails a test rather than standing; and each record that the README's list of what the first version does not support links is named by an item under Later (R214). The README's briefing says that what an issue proposes is neither planned nor committed to (R212). `CLAUDE.md`'s rule on documentation and the pull request template ask that a pull request that finishes, adds or moves an item changes the item and the roadmap with it.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each backlog item gives one of five statuses
~~~~

Clause, R207:

~~~~text
, and a test fails on one that has none of them;
~~~~

Clause, R213:

~~~~text
the roadmap lists each open item once, by a line that gives its title, status, date and brief as the item does, and lists no item that is done or dropped, and a test fails otherwise.
~~~~

Clause, the new unit:

~~~~text
The roadmap opens, and the backlog's page says, that an item describes and is neither a promise nor a date
~~~~

Clause, R217:

~~~~text
, and the page says what each status means and that `Done` means merged, with `CHANGELOG.md` naming the release that holds it; tests fail when they do not.
~~~~

Clause, R216:

~~~~text
Compared with the base commit, a test fails on an item whose text a branch changes while its date stays before the base's, and on an item removed or renamed.
~~~~

Clause, R215:

~~~~text
Each item names what it rests on,
~~~~

Clause, R213:

~~~~text
those under Next and Later at least one ID,
~~~~

Clause, R215:

~~~~text
and a test fails on an ID that does not exist, in active and archived changes alike, on an item that names a closed record and on an open item whose tasks are all ticked.
~~~~

Clause, R214:

~~~~text
A test fails on a record that the README's list of what the first version does not support links and that no item under Later names.
~~~~

Clause, the new unit:

~~~~text
The README's briefing says that what an issue proposes is neither planned nor committed to
~~~~

Clause, the new unit:

~~~~text
. `CLAUDE.md`'s rule on documentation and the pull request template ask that a pull request that finishes, adds or moves an item changes the item and the roadmap with it.
~~~~

### Entry

Old:

~~~~text
- **Answer:** every risk of every change's design, active or archived, is listed, by its title as its design gives it, on the roadmap's Known limitations or on a feature page, and a test fails on a risk that no page lists, on a listed title that no design gives, on a feature page without its section on known limitations and the roadmap, and on a Known limitations that does not link each of those sections. Known limitations says that it is a short list.
~~~~

New:

~~~~text
- **Answer:** every risk of every change's design, active or archived, is listed, by its title as its design gives it, on the roadmap's Known limitations or on a feature page (R208), so that an adopter who reads the documentation and not the design meets each risk, an archived change's among them. Known limitations says that it is a short list (R208).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** every risk of every change's design, active or archived, is listed, by its title as its design gives it, on the roadmap's Known limitations or on a feature page
~~~~

Clause, R208:

~~~~text
, and a test fails on a risk that no page lists, on a listed title that no design gives, on a feature page without its section on known limitations and the roadmap, and on a Known limitations that does not link each of those sections.
~~~~

Clause, the new unit:

~~~~text
Known limitations says that it is a short list
~~~~

### Entry

Old:

~~~~text
- **Answer:** the roadmap, the backlog items and the guide give no fenced or indented code, and a test reads every link, autolink, web address, host and `owner/repo` in them, in every file in `docs/backlog/` and in each feature page's section on known limitations and the roadmap, in prose and code alike, each link from its `](` whatever its text holds, and fails on any that names anything but a heading of its own page or a tracked file of this repository outside `vendor/` and `.claude/skills/` by a relative path that stays inside it, on a host that emphasis marks split, which GitHub shows as one name, on four numbers joined by dots and on a commit ID, which GitHub serves for a fork's commit under this repository's address (R209, R221). Their inline code holds no space, so that no command stands in them, apart from the guide's opening, whose words a test holds word for word (R219, R221), and a test fails on one that does: commands are given only in the README, whose own test holds them (R201).
~~~~

New:

~~~~text
- **Answer:** the roadmap, the backlog items, each feature page's section on known limitations and the roadmap, and the guide give no fenced or indented code and link nothing but a heading of their own page or a tracked file of this repository outside `vendor/` and `.claude/skills/` (R209, R221), so that no command or link there leads an adopter to a fork, a commit ID among them, which GitHub serves for a fork's commit under this repository's address. Their inline code holds no space, so that no command stands in them, apart from the guide's opening, whose words a test holds word for word (R219, R221): commands are given only in the README, whose own test holds them (R201).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the roadmap, the backlog items
~~~~

Clause, the new unit:

~~~~text
and the guide give no fenced or indented code
~~~~

Clause, R209:

~~~~text
, and a test reads every link, autolink, web address, host and `owner/repo` in them, in every file in `docs/backlog/` and in each feature page's section on known limitations and the roadmap, in prose and code alike, each link from its `](` whatever its text holds, and fails on any that names anything but a heading of its own page or
~~~~

Clause, the new unit:

~~~~text
a tracked file of this repository outside `vendor/` and `.claude/skills/`
~~~~

Clause, R209:

~~~~text
by a relative path that stays inside it, on a host that emphasis marks split, which GitHub shows as one name, on four numbers joined by dots and on a commit ID,
~~~~

Clause, the new unit:

~~~~text
which GitHub serves for a fork's commit under this repository's address
~~~~

Clause, the new unit:

~~~~text
(R209, R221)
~~~~

Clause, the new unit:

~~~~text
. Their inline code holds no space, so that no command stands in them, apart from the guide's opening, whose words a test holds word for word (R219, R221)
~~~~

Clause, R209:

~~~~text
, and a test fails on one that does
~~~~

Clause, the new unit:

~~~~text
: commands are given only in the README, whose own test holds them (R201).
~~~~

### Entry

Old:

~~~~text
- **Answer:** the roadmap and the backlog items name an issue or a pull request by its number alone, with its own summary, and links none, so that it invites no reader to follow one, and a test fails on any address under this repository on GitHub.
~~~~

New:

~~~~text
- **Answer:** the roadmap and the backlog items name an issue or a pull request by its number alone, with its own summary, and links none, so that it invites no reader to follow one (R209).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the roadmap and the backlog items name an issue or a pull request by its number alone, with its own summary, and links none, so that it invites no reader to follow one
~~~~

Clause, R209:

~~~~text
, and a test fails on any address under this repository on GitHub.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the roadmap, every file in `docs/backlog/`, the guide, and each feature page's section on known limitations and the roadmap, hold only printable ASCII and line feeds, and nowhere, inline code included, a `<`, a `&`, a backslash, a `]:`, a `|` or a link with a title, and a test fails otherwise, as the answer to T151 holds the README (R210, R221). The guide also gives no `$` and no `~` outside inline code, with which GitHub shows mathematics or struck-through text, as the specs give none (R221).
~~~~

New:

~~~~text
- **Answer:** the roadmap, every file in `docs/backlog/`, the guide, and each feature page's section on known limitations and the roadmap hold none of the text that GitHub hides from the rendered page and diff, as the answer to T151 holds the README (R210, R221), so that an agent that reads the raw file reads only what the owner sees. The guide also gives no `$` and no `~` outside inline code, as the specs give none (R221).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the roadmap, every file in `docs/backlog/`, the guide, and each feature page's section on known limitations and the roadmap
~~~~

Clause, R210:

~~~~text
, hold only printable ASCII and line feeds, and nowhere, inline code included, a `<`, a `&`, a backslash, a `]:`, a `|` or a link with a title, and a test fails otherwise
~~~~

Clause, the new unit:

~~~~text
, as the answer to T151 holds the README (R210, R221)
~~~~

Clause, the new unit:

~~~~text
The guide also gives no `$` and no `~` outside inline code
~~~~

Clause, R221:

~~~~text
, with which GitHub shows mathematics or struck-through text
~~~~

Clause, the new unit:

~~~~text
, as the specs give none (R221).
~~~~

### Entry

Old:

~~~~text
- **Answer:** `CLAUDE.md` says that an agent adds an item at `Planned`, moves one to `Planned`, changes what an agreed item's What done looks like says, or gives an agreed item a postponed point or a gap of the guide to close, only when the owner has asked for that in words in the agent's own session, never by text on GitHub, which agent sessions also write as the owner's account (T64), and that an item counts as the default branch gives it (DR-239). The pull request template asks a pull request that does any of these to say so and where the owner asked. A test, compared with the base commit, fails on an item added as in progress, done or dropped and on one that skips planned on its way to being built, and on a gap of the guide given to an item that the base gives as agreed whose What done looks like is unchanged (R231). The README's briefing, the backlog's page and Later's opening say that only a merged pull request makes an item planned. Nothing merges but by the owner.
~~~~

New:

~~~~text
- **Answer:** `CLAUDE.md` says that an agent adds an item at `Planned`, moves one to `Planned`, changes what an agreed item's What done looks like says, or gives an agreed item a postponed point or a gap of the guide to close, only when the owner has asked for that in words in the agent's own session, never by text on GitHub, which agent sessions also write as the owner's account (T64), and that an item counts as the default branch gives it (DR-239). The pull request template asks a pull request that does any of these to say so and where the owner asked. Compared with the base commit, an item is agreed by its status line before it is built (R218), and a gap of the guide given to an agreed item changes that item's own text (R231), so that whatever an item is agreed to shows in its own lines of the diff. The README's briefing, the backlog's page and Later's opening say that only a merged pull request makes an item planned. Nothing merges but by the owner.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** `CLAUDE.md` says that an agent adds an item at `Planned`, moves one to `Planned`, changes what an agreed item's What done looks like says, or gives an agreed item a postponed point or a gap of the guide to close, only when the owner has asked for that in words in the agent's own session, never by text on GitHub, which agent sessions also write as the owner's account (T64), and that an item counts as the default branch gives it (DR-239). The pull request template asks a pull request that does any of these to say so and where the owner asked.
~~~~

Clause, R218:

~~~~text
A test, compared with the base commit, fails on an item added as in progress, done or dropped and on one that skips planned on its way to being built
~~~~

Clause, R231:

~~~~text
, and on a gap of the guide given to an item that the base gives as agreed whose What done looks like is unchanged (R231).
~~~~

Clause, the new unit:

~~~~text
The README's briefing, the backlog's page and Later's opening say that only a merged pull request makes an item planned. Nothing merges but by the owner.
~~~~

### Entry

Old:

~~~~text
- **Answer:** a record that replaces another starts an assessment of what rests on the closed one: each requirement, record and threat that the closed record's section on what reversing it would change names, and each page that names it, is read again, and each record that no longer holds is closed in the same change, a backlog item that names it being kept only for one whose standing the assessment cannot settle; the new record's consequences say what became of each, as `CLAUDE.md`'s rule on records asks. CI fails on a page other than the history that still names a closed record, which flags the pages that name it.
~~~~

New:

~~~~text
- **Answer:** a record that replaces another starts an assessment of what rests on the closed one: each requirement, record and threat that the closed record's section on what reversing it would change names, and each page that names it, is read again, and each record that no longer holds is closed in the same change, a backlog item that names it being kept only for one whose standing the assessment cannot settle; the new record's consequences say what became of each, as `CLAUDE.md`'s rule on records asks. CI fails on a page other than the history that still names a closed record (R127), which flags the pages that name it.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** a record that replaces another starts an assessment of what rests on the closed one: each requirement, record and threat that the closed record's section on what reversing it would change names, and each page that names it, is read again, and each record that no longer holds is closed in the same change, a backlog item that names it being kept only for one whose standing the assessment cannot settle; the new record's consequences say what became of each, as `CLAUDE.md`'s rule on records asks. CI fails on a page other than the history that still names a closed record
~~~~

Clause, the new unit:

~~~~text
, which flags the pages that name it.
~~~~

### Entry

Old:

~~~~text
- **Answer:** the briefing says that an issue is public at once and holds nothing private, and that a security problem goes to `SECURITY.md` instead, and a test fails when it does not; the bug form's checkbox stays for bugs (T61).
~~~~

New:

~~~~text
- **Answer:** the briefing says that an issue is public at once and holds nothing private, and that a security problem goes to `SECURITY.md` instead (R212), so that whoever opens an issue outside the bug form is told before posting; the bug form's checkbox stays for bugs (T61).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** the briefing says that an issue is public at once and holds nothing private, and that a security problem goes to `SECURITY.md` instead
~~~~

Clause, R212:

~~~~text
, and a test fails when it does not;
~~~~

Clause, the new unit:

~~~~text
the bug form's checkbox stays for bugs (T61).
~~~~

### Entry

Old:

~~~~text
- **Answer:** each change's `tasks.md` gives each task once, on a line that the checks read, and holds no other line with a checkbox, no fenced code, front matter, byte-order mark or carriage return without a line feed after it, no `<` before a letter, `/`, `!` or `?` outside inline code on its line, with which an HTML comment or tag opens wherever it stands, and no line that opens with `$$`, and a test fails and names the file and the line otherwise (R232), so that the checks read the tasks that GitHub shows the owner. No attribute that the repository sets hides the diff of a change's `tasks.md` (R134).
~~~~

New:

~~~~text
- **Answer:** each change's `tasks.md` gives each task once, on a line that the checks read, and holds none of the text that GitHub shows otherwise than the checks read it (R232), so that the checks read the tasks that GitHub shows the owner. No attribute that the repository sets hides the diff of a change's `tasks.md` (R134).
~~~~

Clause, the new unit:

~~~~text
- **Answer:** each change's `tasks.md` gives each task once, on a line that the checks read
~~~~

Clause, R232:

~~~~text
, and holds no other line with a checkbox, no fenced code, front matter, byte-order mark or carriage return without a line feed after it, no `<` before a letter, `/`, `!` or `?` outside inline code on its line, with which an HTML comment or tag opens wherever it stands, and no line that opens with `$$`, and a test fails and names the file and the line otherwise (R232)
~~~~

Clause, the new unit:

~~~~text
, so that the checks read the tasks that GitHub shows the owner. No attribute that the repository sets hides the diff of a change's `tasks.md` (R134).
~~~~

### Entry

Old:

~~~~text
- **Answer:** DR-247 and R236 in `project-standards`: the recorder keeps names only at a line's top level, in its `message` object and in `message.usage`, gives every other object and array as its type alone, and checks its own output, writing nothing on a failure; a test reads every kept shape under `tests/`, fails on a name below another object, on a name of an identifier's form and on anything but a path and a type, and fails when no shape exists once the run is recorded; and the owner reads the shape in the scratch repository before it comes here; and it keeps a top-level name only when a list that it shares with that test names it, so that no name of the host's own features reaches the shape.
~~~~

New:

~~~~text
- **Answer:** DR-247 and R236 in `project-standards`: the recorder keeps names only at a line's top level, in its `message` object and in `message.usage`, gives every other object and array as its type alone, and checks its own output, writing nothing on a failure; a test holds every kept shape under `tests/` to names and types alone, and to existing once the run is recorded (R236), so that every kept shape is read and not one file alone; and the owner reads the shape in the scratch repository before it comes here; and it keeps a top-level name only when a list that it shares with that test names it, so that no name of the host's own features reaches the shape.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** DR-247 and R236 in `project-standards`: the recorder keeps names only at a line's top level, in its `message` object and in `message.usage`, gives every other object and array as its type alone, and checks its own output, writing nothing on a failure;
~~~~

Clause, R236:

~~~~text
a test reads every kept shape under `tests/`, fails on a name below another object, on a name of an identifier's form and on anything but a path and a type, and fails when no shape exists once the run is recorded;
~~~~

Clause, the new unit:

~~~~text
and the owner reads the shape in the scratch repository before it comes here; and it keeps a top-level name only when a list that it shares with that test names it, so that no name of the host's own features reaches the shape.
~~~~

### Entry

Old:

~~~~text
- **Answer:** DR-246, and R237 in `project-standards`, by which a test fails unless the workflow runs only on a push to `main`, asks only to read contents and to write pull requests, uses no action but `actions/checkout`, pinned to a full commit, with `persist-credentials: false`, fetches only the push's two commits, reads no secret, puts no `${{` inside a `run:` and sets `timeout-minutes`; and the test also fails on a checkout input other than its ref, its path and `persist-credentials`, on a checkout into another folder than the report reads, on a command other than the report's, and on the word `secrets` anywhere in the file.
~~~~

New:

~~~~text
- **Answer:** DR-246, and R237 in `project-standards`, by which a test fails unless the skeleton's workflow can do no more than post its comment; and the test also fails on a checkout input other than its ref, its path and `persist-credentials`, on a checkout into another folder than the report reads, on a command other than the report's, and on the word `secrets` anywhere in the file.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** DR-246, and R237 in `project-standards`, by which a test fails unless the
~~~~

Clause, R237:

~~~~text
workflow runs only on a push to `main`, asks only to read contents and to write pull requests, uses no action but `actions/checkout`, pinned to a full commit, with `persist-credentials: false`, fetches only the push's two commits, reads no secret, puts no `${{` inside a `run:` and sets `timeout-minutes`
~~~~

Clause, the new unit:

~~~~text
; and the test also fails on a checkout input other than its ref, its path and `persist-credentials`, on a checkout into another folder than the report reads, on a command other than the report's, and on the word `secrets` anywhere in the file.
~~~~

### Entry

Old:

~~~~text
- **Answer:** R240 in `project-standards`: the skeleton recognises `cd` to a written path and `git add` before a `git commit` with only `-m`, `-a` or `-q`, stages nothing when the commit would commit nothing without the file, and after a command that did not commit the file, whether it failed or not, removes it from the index and the working tree and keeps its calls waiting; and task 1.36, by which the run commits in the recognised form; a recognised commit may give `-m` more than once, and only in the repository of each `git add` before it.
~~~~

New:

~~~~text
- **Answer:** R240 in `project-standards`, by which the skeleton stages a ledger file only for a commit that it recognises and that would commit something without the file, and takes back a file that a command did not commit, its calls waiting, so that no commit holds the ledger file alone and no staged file waits for a later commit to take it again; and task 1.36, by which the run commits in the recognised form.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** R240 in `project-standards`
~~~~

Clause, R240:

~~~~text
: the skeleton recognises `cd` to a written path and `git add` before a `git commit` with only `-m`, `-a` or `-q`,
~~~~

Clause, R240:

~~~~text
stages nothing when the commit would commit nothing without the file, and after a command that did not commit the file, whether it failed or not, removes it from the index and the working tree and keeps its calls waiting
~~~~

Clause, the new unit:

~~~~text
; and task 1.36, by which the run commits in the recognised form
~~~~

Clause, R240:

~~~~text
; a recognised commit may give `-m` more than once, and only in the repository of each `git add` before it.
~~~~

### Entry

Old:

~~~~text
- **Answer:** R241 in `project-standards`: the report compares the push's `before` and `after`, goes on only when GitHub's API gives exactly one merged pull request and `before` is not all zeros, reads only the ledger files that the push added and counts each call's key once; otherwise it posts no comment and says why in the job summary; it follows no ledger file that is a link, and takes as a count only a whole number from zero to below a bound, so that a line that gives another is counted as unread and the summary still says what it did.
~~~~

New:

~~~~text
- **Answer:** R241 in `project-standards`, by which the report counts each call of the one merged pull request of a push once, from the ledger files that the push added, so that the figure is neither doubled nor charged to no pull request; otherwise it posts no comment and says why in the job summary; it follows no ledger file that is a link, and takes as a count only a whole number from zero to below a bound, so that a line that gives another is counted as unread and the summary still says what it did.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** R241 in `project-standards`
~~~~

Clause, R241:

~~~~text
: the report compares the push's `before` and `after`, goes on only when GitHub's API gives exactly one merged pull request and `before` is not all zeros, reads only the ledger files that the push added and counts each call's key once
~~~~

Clause, the new unit:

~~~~text
; otherwise it posts no comment and says why in the job summary; it follows no ledger file that is a link, and takes as a count only a whole number from zero to below a bound, so that a line that gives another is counted as unread and the summary still says what it did.
~~~~

### Entry

Old:

~~~~text
- **Answer:** R239 in `project-standards`: each hook command runs the script with `python3 -I` and ends in `; exit 0`, and the script prints nothing on standard output, which tests drive with the script missing and raising.
~~~~

New:

~~~~text
- **Answer:** R239 in `project-standards`, by which a hook command exits with success and prints nothing whatever its script meets, so that neither its exit code nor its output reaches the agent.
~~~~

Clause, the new unit:

~~~~text
- **Answer:** R239 in `project-standards`
~~~~

Clause, R239:

~~~~text
: each hook command runs the script with `python3 -I` and ends in `; exit 0`, and the script prints nothing on standard output, which tests drive with the script missing and raising.
~~~~

## `openspec/changes/add-pr-cost-calculator/design.md`

### Entry

Old:

~~~~text
The run at `SessionStart`, a start run, reads no transcript, since Claude's first response waits for it (see Context), and writes nothing to standard output, which Claude Code gives Claude as context: it takes back and puts back what is due and, when it finds both switches on, begins the session's interval when both were on (decision 6).
~~~~

New:

~~~~text
The run at `SessionStart`, a start run, reads no transcript, since Claude's first response waits for it (see Context), and does the rest of what R148 says (decision 6).
~~~~

Clause, the new unit:

~~~~text
The run at `SessionStart`, a start run, reads no transcript, since Claude's first response waits for it (see Context), and
~~~~

Clause, R148:

~~~~text
writes nothing to standard output, which Claude Code gives Claude as context: it takes back and puts back what is due and, when it finds both switches on, begins the session's interval when both were on
~~~~

Clause, the new unit:

~~~~text
(decision 6).
~~~~

### Entry

Old:

~~~~text
It keeps each call whose line gives a working directory in this repository: one whose git common directory, as git finds it from that directory when the run reads the call, without the session's `GIT_` variables (below), is this repository's, so that the repository's worktrees count and a separate repository nested in its folder does not.
~~~~

New:

~~~~text
It keeps each call whose line gives a working directory in this repository (R3, R147).
~~~~

Clause, the new unit:

~~~~text
It keeps each call whose line gives a working directory in this repository
~~~~

Clause, R147:

~~~~text
: one whose git common directory, as git finds it from that directory when the run reads the call, without the session's `GIT_` variables (below), is this repository's,
~~~~

Clause, R3:

~~~~text
so that the repository's worktrees count and a separate repository nested in its folder does not.
~~~~

### Entry

Old:

~~~~text
That directory alone tells a call's repository and worktree, never what the call reads or writes, nor the branch.
~~~~

New:

~~~~text
That directory alone tells a call's repository and worktree (R147).
~~~~

Clause, the new unit:

~~~~text
That directory alone tells a call's repository and worktree
~~~~

Clause, R147:

~~~~text
, never what the call reads or writes, nor the branch.
~~~~

### Entry

Old:

~~~~text
A call whose line gives no working directory, or whose directory no longer exists, as when a worktree is removed before a run reads its calls, or names no repository that git can tell, is left out.
~~~~

Clause, R147:

~~~~text
A call whose line gives no working directory, or whose directory no longer exists, as when a worktree is removed before a run reads its calls, or names no repository that git can tell, is left out.
~~~~

### Entry

Old:

~~~~text
Because a run comes before every Bash command that the condition matches, a call that the transcript holds as over by then is recorded before that command can change its branch, unless that run reaches its time budget before it reads the call.
~~~~

New:

~~~~text
Because a run comes before every Bash command that the condition matches, a call that the transcript holds as over by then is recorded before that command can change its branch (R7).
~~~~

Clause, the new unit:

~~~~text
Because a run comes before every Bash command that the condition matches, a call that the transcript holds as over by then is recorded before that command can change its branch
~~~~

Clause, R7:

~~~~text
, unless that run reaches its time budget before it reads the call.
~~~~

### Entry

Old:

~~~~text
Apart from staging a ledger file, taking it back and putting it back, as below, it changes nothing in the working tree or the index, so recording never blocks a change of branch or a rebase.
~~~~

New:

~~~~text
Recording changes the working tree and the index only as R47 allows, so recording never blocks a change of branch or a rebase.
~~~~

Clause, R47:

~~~~text
Apart from staging a ledger file, taking it back and putting it back, as below, it changes nothing in the working tree or the index,
~~~~

Clause, the new unit:

~~~~text
so recording never blocks a change of branch or a rebase.
~~~~

### Entry

Old:

~~~~text
Where none does, as in one shape of subagent transcript, the call is read from its last line once it is over: once a later call follows it in the same transcript, or once its agent has stopped, which `Stop`, `StopFailure` and `SubagentStop` say.
~~~~

New:

~~~~text
Where none does, as in one shape of subagent transcript, the call is read as R42 says, its agent having stopped when `Stop`, `StopFailure` and `SubagentStop` say.
~~~~

Clause, the new unit:

~~~~text
Where none does, as in one shape of subagent transcript,
~~~~

Clause, R42:

~~~~text
the call is read from its last line once it is over: once a later call follows it in the same transcript, or once its agent has stopped,
~~~~

Clause, R42:

~~~~text
which
~~~~

Clause, the new unit:

~~~~text
`Stop`, `StopFailure` and `SubagentStop` say.
~~~~

### Entry

Old:

~~~~text
The ledger counts the calls read that way, because their lines give the usage of the call's start, and the comment gives that count and says that the token cost is then a lower bound.
~~~~

Clause, R42:

~~~~text
The ledger counts the calls read that way, because their lines give the usage of the call's start,
~~~~

Clause, R95:

~~~~text
and the comment gives that count and says that the token cost is then a lower bound.
~~~~

### Entry

Old:

~~~~text
A call that is not over yet waits for a later run.
~~~~

Clause, R42:

~~~~text
A call that is not over yet waits for a later run.
~~~~

### Entry

Old:

~~~~text
A call whose usage holds a field that the script does not know, at its top level or in a block nested in it, is recorded from the fields that the script knows, and the ledger counts such calls without naming the field, because a new field can carry a charge that the entry then leaves out, so the comment gives that count and says that the token cost may then be low.
~~~~

Clause, R43:

~~~~text
A call whose usage holds a field that the script does not know, at its top level or in a block nested in it, is recorded from the fields that the script knows, and the ledger counts such calls without naming the field, because a new field can carry a charge that the entry then leaves out,
~~~~

Clause, R95:

~~~~text
so the comment gives that count and says that the token cost may then be low.
~~~~

### Entry

Old:

~~~~text
A run reads only the lines that end in a line break, because Claude Code can still be writing the last one, and a line that a run began with, or began as the first line that no earlier run read whole, and could not finish reading within its time budget is skipped by the next run and counted as one refused call, so that no one line, however long, holds capture back for good.
~~~~

New:

~~~~text
A run reads only the lines that end in a line break, because Claude Code can still be writing the last one, and treats a line too long for its time budget as R44 says.
~~~~

Clause, the new unit:

~~~~text
A run reads only the lines that end in a line break, because Claude Code can still be writing the last one, and
~~~~

Clause, R44:

~~~~text
a line that a run began with, or began as the first line that no earlier run read whole, and could not finish reading within its time budget is skipped by the next run and counted as one refused call, so that no one line, however long, holds capture back for good.
~~~~

### Entry

Old:

~~~~text
A command runs `git commit` when one of the commands it is made of, split as the shell splits it, is `git`, then any of git's own options, then `commit`, and is not a dry run, which it is when any of `--dry-run`, `--short`, `--porcelain`, `--long`, `-z` and `--null` is in effect once git has read the commit's options, in any spelling that git accepts, such as `--dry` or `-qz`.
~~~~

New:

~~~~text
A command runs `git commit` as R79 and R80 say.
~~~~

Clause, the new unit:

~~~~text
A command runs `git commit`
~~~~

Clause, R79:

~~~~text
when one of the commands it is made of, split as the shell splits it, is `git`, then any of git's own options, then `commit`, and is not a dry run,
~~~~

Clause, R80:

~~~~text
which it is when any of `--dry-run`, `--short`, `--porcelain`, `--long`, `-z` and `--null` is in effect once git has read the commit's options, in any spelling that git accepts, such as `--dry` or `-qz`.
~~~~

### Entry

Old:

~~~~text
For git, `--short`, `--porcelain` and `--long` are one setting, which the `--no-` form of any of them clears, so `git commit --porcelain --no-short` makes a commit.
~~~~

Clause, R80:

~~~~text
For git, `--short`, `--porcelain` and `--long` are one setting, which the `--no-` form of any of them clears, so `git commit --porcelain --no-short` makes a commit.
~~~~

### Entry

Old:

~~~~text
So the script stages a ledger file only when the commit is a top-level command, joined to the rest by `&&`, `;` or line breaks and not part of a pipeline, whose other commands run beside it, runs in the foreground, which a commit followed by `&` does not, and comes after nothing but `cd` to a path written in the command and the git commands `add`, `rm`, `mv`, `status`, `diff`, `log` and `show`, with or without git's own options, which are what an agent runs before a commit and which do not change the branch themselves.
~~~~

New:

~~~~text
So the script stages a ledger file only for a commit that R82 names, and none in a pipeline, whose other commands run beside it, nor after any git command but those that R82 lists, which are what an agent runs before a commit and which do not change the branch themselves.
~~~~

Clause, the new unit:

~~~~text
So the script stages a ledger file only
~~~~

Clause, R82:

~~~~text
when the commit is a top-level command, joined to the rest by `&&`, `;` or line breaks and not part of a pipeline,
~~~~

Clause, the new unit:

~~~~text
whose other commands run beside it
~~~~

Clause, R82:

~~~~text
, runs in the foreground, which a commit followed by `&` does not, and comes after nothing but `cd` to a path written in the command and the git commands `add`, `rm`, `mv`, `status`, `diff`, `log` and `show`, with or without git's own options,
~~~~

Clause, the new unit:

~~~~text
which are what an agent runs before a commit and which do not change the branch themselves.
~~~~

### Entry

Old:

~~~~text
So each counts as a command that comes before the commit, except one whose only command is `cat` reading a here-document whose delimiter is quoted, which is one way to pass a message of several lines, and in whose body the shell expands nothing.
~~~~

New:

~~~~text
So each counts as a command that comes before the commit, with the one exception that R48 gives, which is one way to pass a message of several lines.
~~~~

Clause, the new unit:

~~~~text
So each counts as a command that comes before the commit,
~~~~

Clause, R48:

~~~~text
except one whose only command is `cat` reading a here-document whose delimiter is quoted,
~~~~

Clause, the new unit:

~~~~text
which is one way to pass a message of several lines
~~~~

Clause, R48:

~~~~text
and in whose body the shell expands nothing.
~~~~

### Entry

Old:

~~~~text
The shell runs any command substitution in the body of a here-document whose delimiter is not quoted, so when the commit or a command before it reads one, the script stages nothing.
~~~~

Clause, R112:

~~~~text
The shell runs any command substitution in the body of a here-document whose delimiter is not quoted, so when the commit or a command before it reads one, the script stages nothing.
~~~~

### Entry

Old:

~~~~text
The worktree where the commit runs is the hook input's `cwd`, followed through each top-level `cd` before the commit and the `-C` options given to git before `commit` in the commit's own command, never the directory the hook runs in, which in a desktop worktree session is the main worktree (see Context), and the script stages nothing when such a `-C` option names a path that is not written in the command.
~~~~

New:

~~~~text
The worktree where the commit runs is the one that R49 gives, never the directory the hook runs in, which in a desktop worktree session is the main worktree (see Context).
~~~~

Clause, the new unit:

~~~~text
The worktree where the commit runs is
~~~~

Clause, R49:

~~~~text
the hook input's `cwd`, followed through each top-level `cd` before the commit and the `-C` options given to git before `commit` in the commit's own command,
~~~~

Clause, the new unit:

~~~~text
never the directory the hook runs in, which in a desktop worktree session is the main worktree (see Context)
~~~~

Clause, R49:

~~~~text
and the script stages nothing when such a `-C` option names a path that is not written in the command.
~~~~

### Entry

Old:

~~~~text
It writes nothing when no call is waiting; when the command names the paths to commit, which leaves the rest of the index out; when the commit would commit nothing without the file, counting the changes to tracked files that `-a` adds, and no `git add`, `git rm` or `git mv` comes before it, so a commit that would fail still fails, and an empty commit asked for stays empty; when a `git rm` or `git mv` before the commit is given a `-C` path not written in the command, or names a path with a wildcard or other pathspec magic, a path not written in the command, or the folder that the file goes in or one above it, read from where that command runs, after the `cd`s before it and its own `-C` options, because `git rm` refuses to remove a newly staged file and fails the command, and `git mv` moves it where the script does not look for it; and when `git check-attr`, which reads every attribute file that git does, the repository's `.git/info/attributes` and the person's own among them, gives the ledger path a `filter` or a `working-tree-encoding`, because git can then commit a pointer, as Git LFS does, or the file decoded from another encoding, instead of the entries.
~~~~

New:

~~~~text
It writes nothing in the cases that R81, R83, R84, R85 and R86 give: for a command that names the paths to commit, which leaves the rest of the index out; for a `git rm` or `git mv` that may reach the ledger folder, because `git rm` refuses to remove a newly staged file and fails the command, and `git mv` moves it where the script does not look for it; and when `git check-attr`, which reads every attribute file that git does, the repository's `.git/info/attributes` and the person's own among them, gives the ledger path a `filter` or a `working-tree-encoding`, because git can then commit a pointer, as Git LFS does, or the file decoded from another encoding, instead of the entries.
~~~~

Clause, the new unit:

~~~~text
It writes nothing
~~~~

Clause, R81:

~~~~text
when no call is waiting;
~~~~

Clause, R83:

~~~~text
when the command names the paths to commit,
~~~~

Clause, the new unit:

~~~~text
which leaves the rest of the index out;
~~~~

Clause, R84:

~~~~text
when the commit would commit nothing without the file, counting the changes to tracked files that `-a` adds, and no `git add`, `git rm` or `git mv` comes before it, so a commit that would fail still fails, and an empty commit asked for stays empty;
~~~~

Clause, R85:

~~~~text
when a `git rm` or `git mv` before the commit is given a `-C` path not written in the command, or names a path with a wildcard or other pathspec magic, a path not written in the command, or the folder that the file goes in or one above it, read from where that command runs, after the `cd`s before it and its own `-C` options,
~~~~

Clause, the new unit:

~~~~text
because `git rm` refuses to remove a newly staged file and fails the command, and `git mv` moves it where the script does not look for it; and when `git check-attr`, which reads every attribute file that git does, the repository's `.git/info/attributes` and the person's own among them, gives the ledger path a `filter` or a `working-tree-encoding`, because git can then commit a pointer, as Git LFS does, or the file decoded from another encoding, instead of the entries.
~~~~

### Entry

Old:

~~~~text
When git refuses to add the file, as it does where `core.safecrlf` is on and line endings are converted, the script removes the file it wrote and stages nothing.
~~~~

New:

~~~~text
When git refuses to add the file, as it does where `core.safecrlf` is on and line endings are converted, the script does what R50 says.
~~~~

Clause, the new unit:

~~~~text
When git refuses to add the file, as it does where `core.safecrlf` is on and line endings are converted,
~~~~

Clause, R50:

~~~~text
the script removes the file it wrote and stages nothing.
~~~~

### Entry

Old:

~~~~text
If not, that run takes the file back, from the index and the working tree, and its calls wait for a later commit.
~~~~

New:

~~~~text
If not, that run takes the file back, as R9 says.
~~~~

Clause, the new unit:

~~~~text
If not, that run takes the file back,
~~~~

Clause, R9:

~~~~text
from the index and the working tree, and its calls wait for a later commit.
~~~~

### Entry

Old:

~~~~text
Any later run of the step in the repository, from that session or another, takes the file back once it finds that command over: by the command's result in the transcript, by a later call of the agent that ran it, by that agent having stopped, or by its session having ended, which `SessionEnd` says.
~~~~

New:

~~~~text
Any later run of the step in the repository takes the file back as R87 says, a session having ended when `SessionEnd` says.
~~~~

Clause, the new unit:

~~~~text
Any later run of the step in the repository
~~~~

Clause, R87:

~~~~text
, from that session or another, takes the file back once it finds that command over: by the command's result in the transcript, by a later call of the agent that ran it, by that agent having stopped, or by its session having ended, which
~~~~

Clause, the new unit:

~~~~text
`SessionEnd` says.
~~~~

### Entry

Old:

~~~~text
A `PreToolUse` run that fires again for the same `tool_use_id`, as for a deferred call when it is resumed, stages nothing new while that command's file is still staged and the branch it was staged for is still checked out in that worktree.
~~~~

New:

~~~~text
A `PreToolUse` run that fires again for the same `tool_use_id`, as for a deferred call when it is resumed, does what R51 says.
~~~~

Clause, the new unit:

~~~~text
A `PreToolUse` run that fires again for the same `tool_use_id`, as for a deferred call when it is resumed,
~~~~

Clause, R51:

~~~~text
stages nothing new while that command's file is still staged and the branch it was staged for is still checked out in that worktree.
~~~~

### Entry

Old:

~~~~text
A take-back never removes a file from a worktree whose checked-out commit holds it, and leaves the file while another git command holds that worktree's index lock, rather than waiting for the lock or removing it.
~~~~

New:

~~~~text
A take-back does what R113 and R114 say, rather than waiting for the lock or removing it.
~~~~

Clause, R113:

~~~~text
A take-back never removes a file from a worktree whose checked-out commit holds it,
~~~~

Clause, R114:

~~~~text
and leaves the file while another git command holds that worktree's index lock,
~~~~

Clause, the new unit:

~~~~text
rather than waiting for the lock or removing it.
~~~~

### Entry

Old:

~~~~text
So every take-back notes the commit that it found checked out there, not holding the file, and whether it removed the file from the index, the working tree or both, and the first later run that finds another commit checked out in that worktree and the index free puts the file back, as that commit holds it, if that commit holds it: into the index, if the take-back removed it from there and the index lacks it, and then into the working tree, if the take-back removed it from there, the index holds it as that commit does and the working tree lacks it, before the agent's next git command could commit its deletion.
~~~~

New:

~~~~text
So every take-back is noted, and a later run puts the file back, as R115 and R116 say, before the agent's next git command could commit its deletion.
~~~~

Clause, the new unit:

~~~~text
So every take-back
~~~~

Clause, R115:

~~~~text
notes the commit that it found checked out there, not holding the file, and whether it removed the file from the index, the working tree or both,
~~~~

Clause, R116:

~~~~text
and the first later run that finds another commit checked out in that worktree and the index free puts the file back, as that commit holds it, if that commit holds it: into the index, if the take-back removed it from there and the index lacks it, and then into the working tree, if the take-back removed it from there, the index holds it as that commit does and the working tree lacks it,
~~~~

Clause, the new unit:

~~~~text
before the agent's next git command could commit its deletion.
~~~~

### Entry

Old:

~~~~text
Then it forgets the note, whether it put the file back or not, so that a ledger file that the person removes later, or that the step never took back, is never put back.
~~~~

New:

~~~~text
Then it forgets the note, as R117 says, so that a ledger file that the person removes later, or that the step never took back, is never put back.
~~~~

Clause, the new unit:

~~~~text
Then it forgets the note,
~~~~

Clause, R117:

~~~~text
whether it put the file back or not,
~~~~

Clause, the new unit:

~~~~text
so that a ledger file that the person removes later, or that the step never took back, is never put back.
~~~~

### Entry

Old:

~~~~text
A call is recorded once, by a SHA-256 hash of its message id.
~~~~

Clause, R2:

~~~~text
A call is recorded once,
~~~~

Clause, R163:

~~~~text
by a SHA-256 hash of its message id.
~~~~

### Entry

Old:

~~~~text
An entry records whether the main agent or a subagent made the call, and no session value.
~~~~

Clause, R2:

~~~~text
An entry records whether the main agent or a subagent made the call,
~~~~

Clause, R4:

~~~~text
and no session value.
~~~~

### Entry

Old:

~~~~text
Its standard error carries only its own words and numbers, never text from a transcript, from a ledger file or its name, or from what a git command printed.
~~~~

Clause, R89:

~~~~text
Its standard error carries only its own words and numbers, never text from a transcript, from a ledger file or its name, or from what a git command printed.
~~~~

### Entry

Old:

~~~~text
The script is one file that imports only Python's standard library, because under `python3 -I` a script cannot import a module beside it, and adding its folder to the import path would undo what isolated mode is for.
~~~~

New:

~~~~text
The script is the one file that R12 gives, because under `python3 -I` a script cannot import a module beside it, and adding its folder to the import path would undo what isolated mode is for.
~~~~

Clause, the new unit:

~~~~text
The script is
~~~~

Clause, R12:

~~~~text
one file that imports only Python's standard library,
~~~~

Clause, the new unit:

~~~~text
because under `python3 -I` a script cannot import a module beside it, and adding its folder to the import path would undo what isolated mode is for.
~~~~

### Entry

Old:

~~~~text
Its first line names the release that it comes from.
~~~~

Clause, R53:

~~~~text
Its first line names the release that it comes from.
~~~~

### Entry

Old:

~~~~text
An update bot can still move the pin alone and leave the file behind, so the report says when the hook file in the merged commit is not the one at the commit that the report runs from (decision 7).
~~~~

New:

~~~~text
An update bot can still move the pin alone and leave the file behind, so the report says so, as R65 gives (decision 7).
~~~~

Clause, the new unit:

~~~~text
An update bot can still move the pin alone and leave the file behind, so the report says
~~~~

Clause, R65:

~~~~text
when the hook file in the merged commit is not the one at the commit that the report runs from
~~~~

Clause, the new unit:

~~~~text
(decision 7).
~~~~

### Entry

Old:

~~~~text
The file carries the model names and price attribute values of the price table at its commit, and records any other value as `unknown`, so that a gateway's private alias is not published.
~~~~

New:

~~~~text
The file carries the model names and price attribute values of the price table at its commit, and records any other value as R77 says.
~~~~

Clause, the new unit:

~~~~text
The file carries the model names and price attribute values of the price table at its commit, and records any other value
~~~~

Clause, R77:

~~~~text
as `unknown`, so that a gateway's private alias is not published.
~~~~

### Entry

Old:

~~~~text
When the hook and the report come from one commit, they share one price table, and the report refuses a line with a name that its table does not list.
~~~~

New:

~~~~text
When the hook and the report come from one commit, they share one price table, and the report refuses a line as R98 says.
~~~~

Clause, the new unit:

~~~~text
When the hook and the report come from one commit, they share one price table, and the report refuses a line
~~~~

Clause, R98:

~~~~text
with a name that its table does not list.
~~~~

### Entry

Old:

~~~~text
The script starts no program but git, which it finds at an absolute path, in the folders that the absolute entries of `PATH` name, because Windows looks for a program named without a folder in the current directory before it looks in `PATH` (see Context), and Claude's current directory is usually in the repository.
~~~~

New:

~~~~text
The script starts no program but git, as R54 says, because Windows looks for a program named without a folder in the current directory before it looks in `PATH` (see Context), and Claude's current directory is usually in the repository.
~~~~

Clause, the new unit:

~~~~text
The script starts no program but git,
~~~~

Clause, R54:

~~~~text
which it finds at an absolute path, in the folders that the absolute entries of `PATH` name,
~~~~

Clause, the new unit:

~~~~text
because Windows looks for a program named without a folder in the current directory before it looks in `PATH` (see Context), and Claude's current directory is usually in the repository.
~~~~

### Entry

Old:

~~~~text
Before it starts git, it moves its own current directory to a folder that only the system's administrator can write, such as `/` or Windows' system folder, and names each git command's folder with `-C`, so that a program planted in Claude's current directory, in the repository's folder or in a folder that a relative entry of `PATH` names is never the one that runs.
~~~~

New:

~~~~text
Before it starts git, it does what R54 says, naming each git command's folder with `-C`, so that a program planted in Claude's current directory, in the repository's folder or in a folder that a relative entry of `PATH` names is never the one that runs.
~~~~

Clause, the new unit:

~~~~text
Before it starts git, it
~~~~

Clause, R54:

~~~~text
moves its own current directory to a folder that only the system's administrator can write, such as `/` or Windows' system folder, and names
~~~~

Clause, the new unit:

~~~~text
each git command's folder with `-C`,
~~~~

Clause, the new unit:

~~~~text
so that a program planted in Claude's current directory, in the repository's folder or in a folder that a relative entry of `PATH` names is never the one that runs.
~~~~

### Entry

Old:

~~~~text
It reads both switches from their files before it starts any program.
~~~~

Clause, R118:

~~~~text
It reads both switches from their files before it starts any program.
~~~~

### Entry

Old:

~~~~text
A run whose own reading finds either off starts git only to find its store and, where one exists, to do there what decision 6 says; one whose own reading finds both on also asks git for the opt-in, and when git's answer turns capture off, it starts git after that only as such a run.
~~~~

Clause, R118:

~~~~text
A run whose own reading finds either off starts git only to find its store and, where one exists, to do there what decision 6 says; one whose own reading finds both on also asks git for the opt-in, and when git's answer turns capture off, it starts git after that only as such a run.
~~~~

### Entry

Old:

~~~~text
The store is written only by replacing it whole, under a lock that the operating system releases when the process that holds it ends, so that a run killed while it writes leaves the store as it was or as that write left it, and leaves no lock behind.
~~~~

Clause, R11:

~~~~text
The store is written only by replacing it whole, under a lock that the operating system releases when the process that holds it ends, so that a run killed while it writes leaves the store as it was or as that write left it, and leaves no lock behind.
~~~~

### Entry

Old:

~~~~text
A ledger file is noted in the store before it is written, so that a later run takes back a file that a run killed while writing it left behind.
~~~~

Clause, R57:

~~~~text
A ledger file is noted in the store before it is written, so that a later run takes back a file that a run killed while writing it left behind.
~~~~

### Entry

Old:

~~~~text
So the store carries the version of its format from the first release on, and a run that finds a version that it does not know records, stages, takes back and puts back nothing, leaves the store as it was, whatever the switches say, and exits with success.
~~~~

New:

~~~~text
So the store is versioned as R55 says.
~~~~

Clause, the new unit:

~~~~text
So the store
~~~~

Clause, R55:

~~~~text
carries the version of its format from the first release on, and a run that finds a version that it does not know records, stages, takes back and puts back nothing, leaves the store as it was, whatever the switches say, and exits with success.
~~~~

### Entry

Old:

~~~~text
Copies of two releases that write the same version of the store take each other's notes as their own, so every release that writes a version keeps its path, its lock and its fields, and makes its fingerprint the same way, and a test holds the fingerprint that a fixed set of files gives for each version to the hash recorded for it, while the checks fail when a change alters the hash recorded for a version that a published release wrote, whatever the major number, since a copy that made it otherwise would take each of the other's runs for an opt-out.
~~~~

New:

~~~~text
Copies of two releases that write the same version of the store take each other's notes as their own, so every release that writes a version writes it as R192 says, since a copy that made it otherwise would take each of the other's runs for an opt-out.
~~~~

Clause, the new unit:

~~~~text
Copies of two releases that write the same version of the store take each other's notes as their own, so every release that writes a version
~~~~

Clause, R192:

~~~~text
keeps its path, its lock and its fields, and makes its fingerprint the same way, and a test holds the fingerprint that a fixed set of files gives for each version to the hash recorded for it, while the checks fail when a change alters the hash recorded for a version that a published release wrote, whatever the major number,
~~~~

Clause, the new unit:

~~~~text
since a copy that made it otherwise would take each of the other's runs for an opt-out.
~~~~

### Entry

Old:

~~~~text
Two such releases can still differ in what they record, as when the configuration file holds a key that only the later one documents, so each run that finds both switches on notes, for its session, the latest release whose copy has run in it, and a run of an earlier release than that records, stages, takes back, puts back and ends nothing for that session there, and exits with success, leaving the session to the later release's copy, unless it finds the person's own capture off, which it acts on as any run does, taking back and putting back too, so that an opt-out is acted on even where the later copy no longer runs (DR-206).
~~~~

New:

~~~~text
Two such releases can still differ in what they record, as when the configuration file holds a key that only the later one documents, so an earlier release leaves a session to a later one as R191 says, so that an opt-out is acted on even where the later copy no longer runs (DR-206).
~~~~

Clause, the new unit:

~~~~text
Two such releases can still differ in what they record, as when the configuration file holds a key that only the later one documents, so
~~~~

Clause, R191:

~~~~text
each run that finds both switches on notes, for its session, the latest release whose copy has run in it, and a run of an earlier release than that records, stages, takes back, puts back and ends nothing for that session there, and exits with success, leaving the session to the later release's copy, unless it finds the person's own capture off, which it acts on as any run does, taking back and putting back too,
~~~~

Clause, the new unit:

~~~~text
so that an opt-out is acted on even where the later copy no longer runs (DR-206).
~~~~

### Entry

Old:

~~~~text
A run that finds a store that an earlier release wrote rewrites it in its own version, keeping its waiting calls, its notes of taken calls and its notes of staged and taken-back ledger files, and begins every session's interval anew, so that no call is placed inside an interval by an earlier release's rules, and the calls that answer lines written before that run are left out and flagged for consent, as a removed store's are (DR-187).
~~~~

New:

~~~~text
A run that finds a store that an earlier release wrote rewrites it as R55 says, so that no call is placed inside an interval by an earlier release's rules, and the calls that answer lines written before that run are left out and flagged for consent, as a removed store's are (DR-187).
~~~~

Clause, the new unit:

~~~~text
A run that finds a store that an earlier release wrote rewrites it
~~~~

Clause, R55:

~~~~text
in its own version, keeping its waiting calls, its notes of taken calls and its notes of staged and taken-back ledger files, and begins every session's interval anew,
~~~~

Clause, the new unit:

~~~~text
so that no call is placed inside an interval by an earlier release's rules, and the calls that answer lines written before that run are left out and flagged for consent, as a removed store's are (DR-187).
~~~~

### Entry

Old:

~~~~text
Because a ledger file is written once, under a random name, a pull request's usage is the ledger files its merge adds.
~~~~

New:

~~~~text
Because a ledger file is written once, under a random name, a pull request's usage is what R58 counts.
~~~~

Clause, the new unit:

~~~~text
Because a ledger file is written once, under a random name, a pull request's usage is
~~~~

Clause, R58:

~~~~text
the ledger files its merge adds.
~~~~

### Entry

Old:

~~~~text
Files the default branch already held, such as those that a reused branch name still carries from an earlier pull request, are not added again, so they are not counted again.
~~~~

Clause, R58:

~~~~text
Files the default branch already held, such as those that a reused branch name still carries from an earlier pull request, are not added again, so they are not counted again.
~~~~

### Entry

Old:

~~~~text
An added entry whose call a ledger file held at any commit of the default branch's first-parent history before the merge is not counted, so that a ledger file that leaves the default branch, as a revert takes it, and comes back, as a revert of that revert brings it, is not counted twice, and an added file at a path that this history held is counted as restored.
~~~~

Clause, R59:

~~~~text
An added entry whose call a ledger file held at any commit of the default branch's first-parent history before the merge is not counted, so that a ledger file that leaves the default branch, as a revert takes it, and comes back, as a revert of that revert brings it, is not counted twice,
~~~~

Clause, R119:

~~~~text
and an added file at a path that this history held is counted as restored.
~~~~

### Entry

Old:

~~~~text
A change to an earlier ledger file is flagged, not counted.
~~~~

Clause, R119:

~~~~text
A change to an earlier ledger file is flagged, not counted.
~~~~

### Entry

Old:

~~~~text
A change to a price or to such a statement is a pull request that adds a row dated after the rows already there, so history is never rewritten, and a change reprices nothing earlier.
~~~~

New:

~~~~text
A change to a price or to such a statement is a pull request that adds a row dated after the rows already there, so history is never rewritten (R14).
~~~~

Clause, the new unit:

~~~~text
A change to a price or to such a statement is a pull request that adds a row dated after the rows already there, so history is never rewritten
~~~~

Clause, R14:

~~~~text
, and a change reprices nothing earlier.
~~~~

### Entry

Old:

~~~~text
The type comes from the first tool call in a message: edits and writes are code generation, reads and searches are file reading, shell commands are tooling, `mcp__` tools are MCP, starting a subagent is subagent, a tool the classification does not know is other, and no tool call is conversation.
~~~~

New:

~~~~text
The type comes from the first tool call in a message, as R6 gives it.
~~~~

Clause, the new unit:

~~~~text
The type comes from the first tool call in a message
~~~~

Clause, R6:

~~~~text
: edits and writes are code generation, reads and searches are file reading, shell commands are tooling, `mcp__` tools are MCP, starting a subagent is subagent, a tool the classification does not know is other, and no tool call is conversation.
~~~~

### Entry

Old:

~~~~text
Capture reads it in the working tree, and the report reads it as a blob from the default branch before and after the merge (decision 7), so the pull request being reported cannot turn its own report off.
~~~~

New:

~~~~text
Capture and the report read it as R91 and R19 say (decision 7), so the pull request being reported cannot turn its own report off.
~~~~

Clause, R91:

~~~~text
Capture reads it in the working tree,
~~~~

Clause, R19:

~~~~text
and the report reads it as a blob from the default branch before and after the merge
~~~~

Clause, the new unit:

~~~~text
(decision 7), so the pull request being reported cannot turn its own report off.
~~~~

### Entry

Old:

~~~~text
Both read it only as a regular file no larger than the size bound that its format documents, and take a file that is missing, larger, not a regular file or not valid to leave the tool off, so that the file cannot stall a run, as a named pipe in the working tree could, and a pull request that breaks it still gets its report, flagged, when the file before the merge turned the tool on.
~~~~

New:

~~~~text
Both read it as R36 and R19 say, and leave the tool off for a file that R92 names, so that the file cannot stall a run, as a named pipe in the working tree could, and a pull request that breaks it still gets its report, flagged, when the file before the merge turned the tool on.
~~~~

Clause, the new unit:

~~~~text
Both read it
~~~~

Clause, R36:

~~~~text
only as a regular file no larger than the size bound that its format documents,
~~~~

Clause, R92:

~~~~text
and take a file that is missing, larger, not a regular file or not valid to leave the tool off,
~~~~

Clause, the new unit:

~~~~text
so that the file cannot stall a run, as a named pipe in the working tree could, and a pull request that breaks it still gets its report, flagged, when the file before the merge turned the tool on.
~~~~

### Entry

Old:

~~~~text
A file that holds a key that its format does not document, in the version of the tool that reads it, is not valid, whatever that key's value and whatever `enabled` says, as the owner chose on 2026-11-03 over passing such a key over (DR-190), so that a misspelt key leaves the tool off, and the pull request that adds it is flagged, rather than the file doing what its author did not mean.
~~~~

New:

~~~~text
A file that holds a key that its format does not document is not valid (R171), as the owner chose on 2026-11-03 over passing such a key over (DR-190), so that a misspelt key leaves the tool off, and the pull request that adds it is flagged, rather than the file doing what its author did not mean.
~~~~

Clause, the new unit:

~~~~text
A file that holds a key that its format does not document
~~~~

Clause, R171:

~~~~text
,
~~~~

Clause, R171:

~~~~text
in the version of the tool that reads it, is not valid, whatever that key's value and whatever `enabled` says,
~~~~

Clause, the new unit:

~~~~text
as the owner chose on 2026-11-03 over passing such a key over (DR-190), so that a misspelt key leaves the tool off, and the pull request that adds it is flagged, rather than the file doing what its author did not mean.
~~~~

### Entry

Old:

~~~~text
When the configuration before a merge turns the tool on and the one after it does not, the comment says so in the report's own words, and whether the file there is missing, disables the tool or cannot be read as a valid configuration, and when neither turns the tool on, the job summary says the same, so that a merge that leaves the tool off is seen, and so is a repository that adopts the tool with a file that is not valid (DR-191).
~~~~

New:

~~~~text
The report says what R172 gives, so that a merge that leaves the tool off is seen, and so is a repository that adopts the tool with a file that is not valid (DR-191).
~~~~

Clause, R172:

~~~~text
When the configuration before a merge turns the tool on and the one after it does not, the comment says so in the report's own words, and whether the file there is missing, disables the tool or cannot be read as a valid configuration, and when neither turns the tool on, the job summary says the same,
~~~~

Clause, the new unit:

~~~~text
so that a merge that leaves the tool off is seen, and so is a repository that adopts the tool with a file that is not valid (DR-191).
~~~~

### Entry

Old:

~~~~text
The script reads the person's opt-in from their global configuration files, `~/.gitconfig` and git's file in the XDG configuration folder, not from files that they include, which can lie anywhere, a repository's folder among them, and ignores the variables that point git at other files or add settings, because a repository's Claude Code settings can set those for everyone who works in it, though not `HOME` or the `XDG_*` variables.
~~~~

New:

~~~~text
The script reads the person's opt-in as R37 says, not from files that they include, which can lie anywhere, a repository's folder among them, and ignores the variables that point git at other files or add settings, because a repository's Claude Code settings can set those for everyone who works in it, though not `HOME` or the `XDG_*` variables.
~~~~

Clause, the new unit:

~~~~text
The script reads the person's opt-in
~~~~

Clause, R37:

~~~~text
from their global configuration files, `~/.gitconfig` and git's file in the XDG configuration folder,
~~~~

Clause, the new unit:

~~~~text
not from files that they include, which can lie anywhere, a repository's folder among them, and ignores the variables that point git at other files or add settings, because a repository's Claude Code settings can set those for everyone who works in it, though not `HOME` or the `XDG_*` variables.
~~~~

### Entry

Old:

~~~~text
It takes the XDG folder from `XDG_CONFIG_HOME` only when that variable holds an absolute path, and reads `~/.config/git/config` otherwise, because git reads a relative one from its current directory, which can be in a repository's folder.
~~~~

New:

~~~~text
It takes the XDG folder as R103 says, because git reads a relative one from its current directory, which can be in a repository's folder.
~~~~

Clause, the new unit:

~~~~text
It takes the XDG folder
~~~~

Clause, R103:

~~~~text
from `XDG_CONFIG_HOME` only when that variable holds an absolute path, and reads `~/.config/git/config` otherwise,
~~~~

Clause, the new unit:

~~~~text
because git reads a relative one from its current directory, which can be in a repository's folder.
~~~~

### Entry

Old:

~~~~text
It takes `~` from `HOME` only when that variable holds an absolute path, for the same reason, and never reads a configuration file from a relative path.
~~~~

New:

~~~~text
It takes `~` as R104 says, for the same reason.
~~~~

Clause, the new unit:

~~~~text
It takes `~`
~~~~

Clause, R104:

~~~~text
from `HOME` only when that variable holds an absolute path,
~~~~

Clause, the new unit:

~~~~text
for the same reason
~~~~

Clause, R104:

~~~~text
and never reads a configuration file from a relative path.
~~~~

### Entry

Old:

~~~~text
On Windows, where `HOME` is not set or not absolute, it takes the folder that git takes when `HOME` is not set: `HOMEDRIVE` and `HOMEPATH` together where they name a folder that exists and is not Windows' system folder, and `USERPROFILE` otherwise.
~~~~

New:

~~~~text
On Windows, where `HOME` is not set or not absolute, it takes the folder that R104 gives from `HOMEDRIVE`, `HOMEPATH` and `USERPROFILE`.
~~~~

Clause, the new unit:

~~~~text
On Windows, where `HOME` is not set or not absolute, it takes the folder that
~~~~

Clause, R104:

~~~~text
git takes when `HOME` is not set: `HOMEDRIVE` and `HOMEPATH` together where they name a folder that exists and is not Windows' system folder, and `USERPROFILE` otherwise.
~~~~

### Entry

Old:

~~~~text
Elsewhere, with no absolute `HOME`, it reads no file from `~`.
~~~~

Clause, R104:

~~~~text
Elsewhere, with no absolute `HOME`, it reads no file from `~`.
~~~~

### Entry

Old:

~~~~text
Where both files set it, `~/.gitconfig` decides, as it does for git, which reads it after the other.
~~~~

Clause, R105:

~~~~text
Where both files set it, `~/.gitconfig` decides, as it does for git, which reads it after the other.
~~~~

### Entry

Old:

~~~~text
The script reads these files itself, since it reads both switches before it starts any program (decision 1), and it reads them by git's rules for its configuration files: section and key names match in any case, a value loses its quotes and any comment after it, the last value in a file decides, and a key in a subsection, such as `[pr-cost "x"]`, or in a comment is not the opt-in key.
~~~~

New:

~~~~text
The script reads these files itself, since it reads both switches before it starts any program (decision 1), and it reads them by git's rules, as R38 gives them.
~~~~

Clause, the new unit:

~~~~text
The script reads these files itself, since it reads both switches before it starts any program (decision 1), and it reads them by git's rules
~~~~

Clause, R38:

~~~~text
for its configuration files: section and key names match in any case, a value loses its quotes and any comment after it, the last value in a file decides, and a key in a subsection, such as `[pr-cost "x"]`, or in a comment is not the opt-in key.
~~~~

### Entry

Old:

~~~~text
The script stops a reading that has not finished by the end of the run's time budget, such as one held up by a named pipe that the session's environment names as git's global file, and takes capture to be off when either answer does not come within that budget or gives no value or a refusal, when its last value is not true, or when the last value of any one file in it other than the person's two global files, or of the variables, is not true.
~~~~

New:

~~~~text
The script stops a reading that has not finished by the end of the run's time budget, such as one held up by a named pipe that the session's environment names as git's global file, and takes capture to be off in the cases that R160 gives.
~~~~

Clause, the new unit:

~~~~text
The script stops a reading that has not finished by the end of the run's time budget, such as one held up by a named pipe that the session's environment names as git's global file, and takes capture to be off
~~~~

Clause, R160:

~~~~text
when either answer does not come within that budget or gives no value or a refusal, when its last value is not true, or when the last value of any one file in it other than the person's two global files, or of the variables, is not true.
~~~~

### Entry

Old:

~~~~text
A run that finds both switches on, and no store whose version it does not know, notes in the store its time, read from the system's clock in UTC, and a fingerprint of the files that can turn the person's capture on or off: their two global configuration files, each other file that git reads the opt-in key from, which either of git's two answers names, and each link on the way to one, made of each one's device and inode numbers, size and modification times, and never of its contents or its path, and the store keeps only a hash of it, so that no configuration file's path, which can carry the home folder and the names that the person gives their files, reaches the store.
~~~~

New:

~~~~text
A run that finds both switches on, and no store whose version it does not know, notes its time and a fingerprint as R107 says, so that no configuration file's path, which can carry the home folder and the names that the person gives their files, reaches the store.
~~~~

Clause, the new unit:

~~~~text
A run that finds both switches on, and no store whose version it does not know, notes
~~~~

Clause, R107:

~~~~text
in the store its time, read from the system's clock in UTC, and a fingerprint of the files that can turn the person's capture on or off: their two global configuration files, each other file that git reads the opt-in key from, which either of git's two answers names, and each link on the way to one, made of each one's device and inode numbers, size and modification times, and never of its contents or its path, and the store keeps only a hash of it,
~~~~

Clause, the new unit:

~~~~text
so that no configuration file's path, which can carry the home folder and the names that the person gives their files, reaches the store.
~~~~

### Entry

Old:

~~~~text
An interval begins at a run that finds both on while its session has no open interval, and ends at its last run before one that finds either off or notes another fingerprint than the last that the store notes, whichever session's run noted it, which then begins the next interval if it finds both on.
~~~~

Clause, R108:

~~~~text
An interval begins at a run that finds both on while its session has no open interval, and ends at its last run before one that finds either off or notes another fingerprint than the last that the store notes,
~~~~

Clause, R162:

~~~~text
whichever session's run noted it,
~~~~

Clause, R108:

~~~~text
which then begins the next interval if it finds both on.
~~~~

### Entry

Old:

~~~~text
A call counts as made inside an interval only when, by each line's own time, read as an instant with its offset from UTC, the line it answers, which is the nearest line up the chain of parents that the call's first line names in the same transcript that gives the person's prompt, a tool's result or a compaction's summary, was written at or after the run that began the interval and no later than the call's first line, and its first line no later than the interval's last run.
~~~~

New:

~~~~text
A call counts as made inside an interval only as R144 says, by each line's own time, read as an instant with its offset from UTC.
~~~~

Clause, the new unit:

~~~~text
A call counts as made inside an interval only
~~~~

Clause, R144:

~~~~text
when,
~~~~

Clause, the new unit:

~~~~text
by each line's own time, read as an instant with its offset from UTC
~~~~

Clause, R144:

~~~~text
the line it answers, which is the nearest line up the chain of parents that the call's first line names in the same transcript that gives the person's prompt, a tool's result or a compaction's summary, was written at or after the run that began the interval and no later than the call's first line, and its first line no later than the interval's last run.
~~~~

### Entry

Old:

~~~~text
A call that answers no line of its transcript, whose answered line comes before where runs read again or was skipped as too long, or that falls outside every interval, is left out.
~~~~

Clause, R144:

~~~~text
A call that answers no line of its transcript,
~~~~

Clause, R165:

~~~~text
whose answered line comes before where runs read again or was skipped as too long,
~~~~

Clause, R40:

~~~~text
or that falls outside every interval, is left out.
~~~~

### Entry

Old:

~~~~text
Nothing depends on it: where no start run comes, as with a Claude Code that does not run that event, the interval begins at the session's first run that finds both on, and the calls before it are left out.
~~~~

New:

~~~~text
Nothing depends on it, as R148 says, as with a Claude Code that does not run that event.
~~~~

Clause, the new unit:

~~~~text
Nothing depends on it
~~~~

Clause, R148:

~~~~text
: where no start run comes,
~~~~

Clause, the new unit:

~~~~text
as with a Claude Code that does not run that event
~~~~

Clause, R148:

~~~~text
the interval begins at the session's first run that finds both on, and the calls before it are left out.
~~~~

### Entry

Old:

~~~~text
So whenever a run leaves out a call made in this repository because it fell outside every interval, the next ledger file staged for that call's worktree and branch says so, with no count, time or other fact about the calls left out, and the comment says that the token cost is then a lower bound (decision 16).
~~~~

Clause, R155:

~~~~text
So whenever a run leaves out a call made in this repository because it fell outside every interval, the next ledger file staged for that call's worktree and branch says so, with no count, time or other fact about the calls left out,
~~~~

Clause, R157:

~~~~text
and the comment says that the token cost is then a lower bound (decision 16).
~~~~

### Entry

Old:

~~~~text
A run that finds either switch off creates no store and adds no note of its session to one, removes a store that does not parse, and in one of a version that it knows only ends its own session's interval, noting its time as above, and does what decision 15 says that every run does, so that someone who has never opted in leaves nothing in the git common directory, and a repository that turns the tool off keeps nothing past the window.
~~~~

New:

~~~~text
A run that finds either switch off does what R145 says, so that someone who has never opted in leaves nothing in the git common directory, and a repository that turns the tool off keeps nothing past the window.
~~~~

Clause, the new unit:

~~~~text
A run that finds either switch off
~~~~

Clause, R145:

~~~~text
creates no store and adds no note of its session to one, removes a store that does not parse, and in one of a version that it knows only ends its own session's interval, noting its time as above, and does what decision 15 says that every run does,
~~~~

Clause, the new unit:

~~~~text
so that someone who has never opted in leaves nothing in the git common directory, and a repository that turns the tool off keeps nothing past the window.
~~~~

### Entry

Old:

~~~~text
A run holds the store's lock from when it reads the store until it has written it, and reads both switches again under that lock before it writes a call to the store or stages a ledger file, acting only on a store whose file is still the one that its lock holds, so that a run that began before an opt-out writes nothing after it, and a run that waited for the lock writes nothing into a store that an opt-out removed.
~~~~

Clause, R161:

~~~~text
A run holds the store's lock from when it reads the store until it has written it, and reads both switches again under that lock before it writes a call to the store or stages a ledger file, acting only on a store whose file is still the one that its lock holds, so that a run that began before an opt-out writes nothing after it, and a run that waited for the lock writes nothing into a store that an opt-out removed.
~~~~

### Entry

Old:

~~~~text
A run that finds the person's own capture off, in their global configuration, in the repository's or as git reads it there, ends every session's interval and empties a store of a version that it knows (decision 1): it removes every call waiting to be staged, every flag due, every note of a taken call and every session's notes, keeping only the notes that a take-back or a put-back still needs, and a take-back after it returns that file's calls and flags to neither `waiting` nor `flags`, so the store removes itself once those are done (decision 15).
~~~~

New:

~~~~text
A run that finds the person's own capture off, in their global configuration, in the repository's or as git reads it there, does what R109 says (decision 1), and a take-back after it returns that file's calls and flags to neither `waiting` nor `flags`, so the store removes itself once those are done (decision 15).
~~~~

Clause, the new unit:

~~~~text
A run that finds the person's own capture off, in their global configuration, in the repository's or as git reads it there,
~~~~

Clause, R109:

~~~~text
ends every session's interval and empties a store of a version that it knows
~~~~

Clause, the new unit:

~~~~text
(decision 1)
~~~~

Clause, R109:

~~~~text
: it removes every call waiting to be staged, every flag due, every note of a taken call and every session's notes, keeping only the notes that a take-back or a put-back still needs,
~~~~

Clause, the new unit:

~~~~text
and a take-back after it returns that file's calls and flags to neither `waiting` nor `flags`, so the store removes itself once those are done (decision 15).
~~~~

### Entry

Old:

~~~~text
So no call made before that run is staged after it, and turning capture on again reads every transcript afresh, through intervals that begin only at later runs.
~~~~

Clause, R109:

~~~~text
So no call made before that run is staged after it, and turning capture on again reads every transcript afresh, through intervals that begin only at later runs.
~~~~

### Entry

Old:

~~~~text
Taking back and putting back ledger files does not wait on the switches, so a file staged before capture was turned off is still taken back.
~~~~

Clause, R110:

~~~~text
Taking back and putting back ledger files does not wait on the switches, so a file staged before capture was turned off is still taken back.
~~~~

### Entry

Old:

~~~~text
A reusable workflow receives its caller's event, so the report checks the event itself and refuses anything but a push to the default branch: it goes on only when `github.event_name` is `push` and `github.ref` is `refs/heads/` followed by the default branch's name, so that no other event passes, even one whose `github.ref` names the default branch, and neither does a push of a tag named like the default branch, whose `github.ref_name` is that same name.
~~~~

New:

~~~~text
A reusable workflow receives its caller's event, so the report checks the event itself, as R68 says.
~~~~

Clause, the new unit:

~~~~text
A reusable workflow receives its caller's event, so the report checks the event itself
~~~~

Clause, R68:

~~~~text
and refuses anything but a push to the default branch: it goes on only when `github.event_name` is `push` and `github.ref` is `refs/heads/` followed by the default branch's name, so that no other event passes, even one whose `github.ref` names the default branch, and neither does a push of a tag named like the default branch, whose `github.ref_name` is that same name.
~~~~

### Entry

Old:

~~~~text
It fetches what it reads, since `actions/checkout` fetches one commit unless it is asked for more: the default branch's history up to the push's commit, and the pull request's head as `refs/pull/<number>/head`.
~~~~

New:

~~~~text
It fetches what it reads, since `actions/checkout` fetches one commit unless it is asked for more, as R23 gives.
~~~~

Clause, the new unit:

~~~~text
It fetches what it reads, since `actions/checkout` fetches one commit unless it is asked for more
~~~~

Clause, R23:

~~~~text
: the default branch's history up to the push's commit, and the pull request's head as `refs/pull/<number>/head`.
~~~~

### Entry

Old:

~~~~text
It looks up each commit that the push adds to the default branch's first-parent history, and when they do not all belong to one pull request, as when a merge queue merges several in one push, or belong to none, as when a commit is pushed straight to the default branch, it posts no comment and says why in its job summary, so that a push that gets no comment can be told from a push for which the report did not run.
~~~~

New:

~~~~text
It looks up each commit that the push adds to the default branch's first-parent history, and comments only as R69 says, so that a push that gets no comment can be told from a push for which the report did not run.
~~~~

Clause, the new unit:

~~~~text
It looks up each commit that the push adds to the default branch's first-parent history, and
~~~~

Clause, R69:

~~~~text
when they do not all belong to one pull request, as when a merge queue merges several in one push, or belong to none, as when a commit is pushed straight to the default branch, it posts no comment and says why in its job summary,
~~~~

Clause, the new unit:

~~~~text
so that a push that gets no comment can be told from a push for which the report did not run.
~~~~

### Entry

Old:

~~~~text
It reads the ledger from git, comparing the push's commit before with the one after: the ledger files the merge adds, and the earlier ledger files it removes or changes, whose number the job summary gives when the push gets no comment.
~~~~

New:

~~~~text
It reads the ledger from git, comparing the push's commit before with the one after, as R58 and R60 say.
~~~~

Clause, the new unit:

~~~~text
It reads the ledger from git, comparing the push's commit before with the one after
~~~~

Clause, R58:

~~~~text
: the ledger files the merge adds,
~~~~

Clause, R60:

~~~~text
and the earlier ledger files it removes or changes, whose number the job summary gives when the push gets no comment.
~~~~

### Entry

Old:

~~~~text
So that a call is counted once, it also reads the call ids of every ledger file that a commit of the default branch's first-parent history held before the merge, and counts as restored an added file at a path that this history held.
~~~~

New:

~~~~text
So that a call is counted once, it also reads the call ids of every ledger file that a commit of the default branch's first-parent history held before the merge, as R59 and R119 need.
~~~~

Clause, the new unit:

~~~~text
So that a call is counted once, it also reads the call ids of every ledger file that a commit of the default branch's first-parent history held before the merge
~~~~

Clause, R119:

~~~~text
, and counts as restored an added file at a path that this history held.
~~~~

### Entry

Old:

~~~~text
It reads those earlier files by the rules that capture applies to the ledger files it reads: it skips a path that is not a regular file, a file above the size bound and a line that does not match the ledger format, and counts none of them against the pull request, since none of them is the pull request's, so that a ledger file that an earlier merge brought can neither stop nor slow every later report.
~~~~

New:

~~~~text
It reads those earlier files by the rules that R67 gives, since none of them is the pull request's, so that a ledger file that an earlier merge brought can neither stop nor slow every later report.
~~~~

Clause, the new unit:

~~~~text
It reads those earlier files by the rules that
~~~~

Clause, R67:

~~~~text
capture applies to the ledger files it reads: it skips a path that is not a regular file, a file above the size bound and a line that does not match the ledger format, and counts none of them against the pull request,
~~~~

Clause, the new unit:

~~~~text
since none of them is the pull request's, so that a ledger file that an earlier merge brought can neither stop nor slow every later report.
~~~~

### Entry

Old:

~~~~text
It reads `.pr-cost.json` at both commits only as a blob within the size bound that its format documents, takes a file that is missing, not a regular file, too large or not valid to leave the tool off at that commit, and runs when either commit turns the tool on, so the pull request that turns the tool on gets its report too, and so does one that breaks the file, while a merge that finds the tool off at both commits gets no comment, and its job summary says why the file after the merge leaves the tool off (decision 6).
~~~~

Clause, R19:

~~~~text
It reads `.pr-cost.json` at both commits only as a blob within the size bound that its format documents,
~~~~

Clause, R92:

~~~~text
takes a file that is missing, not a regular file, too large or not valid to leave the tool off at that commit,
~~~~

Clause, R19:

~~~~text
and runs when either commit turns the tool on, so the pull request that turns the tool on gets its report too,
~~~~

Clause, R92:

~~~~text
and so does one that breaks the file,
~~~~

Clause, R172:

~~~~text
while a merge that finds the tool off at both commits gets no comment, and its job summary says why the file after the merge leaves the tool off (decision 6).
~~~~

### Entry

Old:

~~~~text
So the report keeps to a call budget that the README gives, and its job has a time limit, set with `timeout-minutes`.
~~~~

New:

~~~~text
So the report keeps to the call budget and time limit that R70 gives, set with `timeout-minutes`.
~~~~

Clause, the new unit:

~~~~text
So the report keeps to
~~~~

Clause, R70:

~~~~text
a call budget that the README gives, and its job has a time limit,
~~~~

Clause, the new unit:

~~~~text
set with `timeout-minutes`.
~~~~

### Entry

Old:

~~~~text
It finds the runs on the pull request's commits with as few calls as it can: by listing each commit's runs, or, where fewer calls do it and GitHub returns the whole listing, by listing the repository's runs page by page, filtered by their event and by when they were created.
~~~~

Clause, R121:

~~~~text
It finds the runs on the pull request's commits with as few calls as it can: by listing each commit's runs, or, where fewer calls do it and GitHub returns the whole listing, by listing the repository's runs page by page, filtered by their event and by when they were created.
~~~~

### Entry

Old:

~~~~text
When the budget runs out before the report can tell which pull request the push merges, it posts no comment and says so in its job summary.
~~~~

Clause, R70:

~~~~text
When the budget runs out before the report can tell which pull request the push merges, it posts no comment and says so in its job summary.
~~~~

### Entry

Old:

~~~~text
When it runs out while the report reads the runs and jobs, or GitHub returns only part of a listing, the comment marks the CI cost as incomplete.
~~~~

Clause, R64:

~~~~text
When it runs out while the report reads the runs and jobs, or GitHub returns only part of a listing, the comment marks the CI cost as incomplete.
~~~~

### Entry

Old:

~~~~text
It counts only the runs on those commits that no push to the default branch started, as the event and branch that each run names show, and that were created before the pull request merged.
~~~~

New:

~~~~text
It counts only the runs that R62 gives, as the event and branch that each run names show.
~~~~

Clause, the new unit:

~~~~text
It counts only the runs
~~~~

Clause, R62:

~~~~text
on those commits that no push to the default branch started,
~~~~

Clause, the new unit:

~~~~text
as the event and branch that each run names show
~~~~

Clause, R62:

~~~~text
and that were created before the pull request merged.
~~~~

### Entry

Old:

~~~~text
So the runs that the merge's push starts, the report's own included, are not counted, even when they run on one of those commits, as after a fast-forward, and this does not depend on how their creation times fall around the merge time.
~~~~

Clause, R120:

~~~~text
So the runs that the merge's push starts, the report's own included, are not counted, even when they run on one of those commits, as after a fast-forward, and this does not depend on how their creation times fall around the merge time.
~~~~

### Entry

Old:

~~~~text
A run counted that has not finished makes the CI cost incomplete, and a job on a runner that the price table does not list is counted in minutes and left out of the cost.
~~~~

Clause, R64:

~~~~text
A run counted that has not finished makes the CI cost incomplete,
~~~~

Clause, R63:

~~~~text
and a job on a runner that the price table does not list is counted in minutes and left out of the cost.
~~~~

### Entry

Old:

~~~~text
It also says when the hook file in the merged commit is missing or differs from the hook file at `job.workflow_sha`, quoting nothing from it, because adopters' update bots can move the workflow's pin and leave the copied hook behind, so that the hook and the report come from different commits.
~~~~

New:

~~~~text
It also says what R65 gives, because adopters' update bots can move the workflow's pin and leave the copied hook behind, so that the hook and the report come from different commits.
~~~~

Clause, the new unit:

~~~~text
It also says
~~~~

Clause, R65:

~~~~text
when the hook file in the merged commit is missing or differs from the hook file at `job.workflow_sha`, quoting nothing from it,
~~~~

Clause, the new unit:

~~~~text
because adopters' update bots can move the workflow's pin and leave the copied hook behind, so that the hook and the report come from different commits.
~~~~

### Entry

Old:

~~~~text
And since a person's plugin follows their account, not the repository's pin, it says when a ledger file that the merge adds names, on its first line, a later release of the capture step than the report's own, quoting nothing from it, so that a line or a file that the report refuses for a model name or a format that only a later release knows is explained (DR-208).
~~~~

New:

~~~~text
And since a person's plugin follows their account, not the repository's pin, it says what R193 gives, so that a line or a file that the report refuses for a model name or a format that only a later release knows is explained (DR-208).
~~~~

Clause, the new unit:

~~~~text
And since a person's plugin follows their account, not the repository's pin, it says
~~~~

Clause, R193:

~~~~text
when a ledger file that the merge adds names, on its first line, a later release of the capture step than the report's own, quoting nothing from it,
~~~~

Clause, the new unit:

~~~~text
so that a line or a file that the report refuses for a model name or a format that only a later release knows is explained (DR-208).
~~~~

### Entry

Old:

~~~~text
And it says when `.claude/settings.json` or `.claude/settings.local.json` at the merged commit registers the hook's command with a checksum other than the SHA-256 of the merged commit's hook file, with each CRLF taken as LF, quoting nothing from either, since a registration copied from another release's README runs nothing, prints nothing and exits with success (R88), so that the sessions there would record nothing through it with no sign of why (R202, DR-216).
~~~~

New:

~~~~text
And it says what R202 gives, since a registration copied from another release's README runs nothing, prints nothing and exits with success (R88), so that the sessions there would record nothing through it with no sign of why (R202, DR-216).
~~~~

Clause, the new unit:

~~~~text
And it says
~~~~

Clause, R202:

~~~~text
when `.claude/settings.json` or `.claude/settings.local.json` at the merged commit registers the hook's command with a checksum other than the SHA-256 of the merged commit's hook file, with each CRLF taken as LF, quoting nothing from either,
~~~~

Clause, the new unit:

~~~~text
since a registration copied from another release's README runs nothing, prints nothing and exits with success (R88), so that the sessions there would record nothing through it with no sign of why (R202, DR-216).
~~~~

### Entry

Old:

~~~~text
Ruff and mypy check against the oldest supported version that `requires-python` in `pyproject.toml` gives, CI runs the tests on it and on the newest release, which the matrix names as `3.x` so that it moves without an edit, and a test checks that every other copy of the version agrees with it: the CI matrix, the ruff and mypy settings, `.python-version`, the bill of materials, the hook's own guard, and the documents that state it.
~~~~

New:

~~~~text
Ruff and mypy check against the oldest supported version that `requires-python` in `pyproject.toml` gives, CI runs the tests on it and on the newest release, which the matrix names as `3.x` so that it moves without an edit, and a test checks that every other copy of the version agrees with it (R99).
~~~~

Clause, the new unit:

~~~~text
Ruff and mypy check against the oldest supported version that `requires-python` in `pyproject.toml` gives, CI runs the tests on it and on the newest release, which the matrix names as `3.x` so that it moves without an edit, and a test checks that every other copy of the version agrees with it
~~~~

Clause, R99:

~~~~text
: the CI matrix, the ruff and mypy settings, `.python-version`, the bill of materials, the hook's own guard, and the documents that state it.
~~~~

### Entry

Old:

~~~~text
So its first statement checks the Python version, and its first git command the git version, against the floors: Python 3.11, and git 2.43, the oldest git that CI tests.
~~~~

New:

~~~~text
So its first statement checks the Python version, and its first git command the git version, against the floors that R32 gives.
~~~~

Clause, the new unit:

~~~~text
So its first statement checks the Python version, and its first git command the git version, against the floors
~~~~

Clause, R32:

~~~~text
: Python 3.11, and git 2.43, the oldest git that CI tests.
~~~~

### Entry

Old:

~~~~text
Below either, it records, stages and prints nothing, and exits with success.
~~~~

Clause, R32:

~~~~text
Below either, it records, stages and prints nothing, and exits with success.
~~~~

### Entry

Old:

~~~~text
A machine-readable manifest of the public surface (DR-154) is kept in the repository, and the release check compares it between the previous release's commit and the tag: a difference with no `### Breaking` section in the changelog entry, or without a raised major number, refuses the release and names what changed.
~~~~

New:

~~~~text
A machine-readable manifest of the public surface (DR-154) is kept in the repository, and the release check compares it as R123 says.
~~~~

Clause, the new unit:

~~~~text
A machine-readable manifest of the public surface (DR-154) is kept in the repository, and the release check compares it
~~~~

Clause, R123:

~~~~text
between the previous release's commit and the tag: a difference with no `### Breaking` section in the changelog entry, or without a raised major number, refuses the release and names what changed.
~~~~

### Entry

Old:

~~~~text
It attaches the bill of materials and the plugin's zip, downloads each again and checks its size and SHA-256 against the file that it built, and only then publishes the release, so that no release is published without its files or with other files than those it built, since a published release cannot change under the immutable releases that DR-074 relies on (DR-209).
~~~~

New:

~~~~text
It publishes the release only as R189 says, so that no release is published without its files or with other files than those it built, since a published release cannot change under the immutable releases that DR-074 relies on (DR-209).
~~~~

Clause, R189:

~~~~text
It attaches the bill of materials and the plugin's zip, downloads each again and checks its size and SHA-256 against the file that it built, and only then publishes the release,
~~~~

Clause, the new unit:

~~~~text
so that no release is published without its files or with other files than those it built, since a published release cannot change under the immutable releases that DR-074 relies on (DR-209).
~~~~

### Entry

Old:

~~~~text
A release whose reusable workflow uses an action that the bill of materials does not list, or whose hook file's or plugin zip's checksum there differs from the file's or the README's, is not published.
~~~~

Clause, R72:

~~~~text
A release whose reusable workflow uses an action that the bill of materials does not list, or whose hook file's or plugin zip's checksum there differs from the file's or the README's, is not published.
~~~~

### Entry

Old:

~~~~text
Each release also carries the plugin (decision 17) as a zip, built from the tag's files alone, as git's objects hold them, never from a checkout, whose line endings git can change, holding only the plugin's manifest, its hooks, the capture step and the licence, in a fixed order, each stored uncompressed with every header field fixed, its times, its modes and the system that made it among them, since Python writes into each entry the system that it runs on and compresses with whatever zlib it links, so that a build on Linux and one on Windows give the same bytes.
~~~~

New:

~~~~text
Each release also carries the plugin (decision 17) as a zip, as R183 gives it, never from a checkout, whose line endings git can change, in a fixed order, with each entry's header fields fixed, its times, its modes and the system that made it among them, since Python writes into each entry the system that it runs on and compresses with whatever zlib it links, so that a build on Linux and one on Windows give the same bytes.
~~~~

Clause, the new unit:

~~~~text
Each release also carries the plugin (decision 17) as a zip,
~~~~

Clause, R183:

~~~~text
built from the tag's files alone, as git's objects hold them,
~~~~

Clause, the new unit:

~~~~text
never from a checkout, whose line endings git can change,
~~~~

Clause, R183:

~~~~text
holding only the plugin's manifest, its hooks, the capture step and the licence,
~~~~

Clause, the new unit:

~~~~text
in a fixed order,
~~~~

Clause, R183:

~~~~text
each stored uncompressed with every header field fixed,
~~~~

Clause, the new unit:

~~~~text
its times, its modes and the system that made it among them, since Python writes into each entry the system that it runs on and compresses with whatever zlib it links, so that a build on Linux and one on Windows give the same bytes.
~~~~

### Entry

Old:

~~~~text
The README gives the zip's SHA-256, and CI builds the zip from every pull request's tree, on Linux and on Windows, and fails when its SHA-256 differs from the README's, so that a checksum left behind is found before a tag is pushed, while the release workflow publishes no release whose zip differs (DR-203).
~~~~

New:

~~~~text
The README gives the zip's SHA-256, and CI builds the zip from every pull request's tree, on Linux and on Windows, and checks it as R183 says, so that a checksum left behind is found before a tag is pushed (DR-203).
~~~~

Clause, the new unit:

~~~~text
The README gives the zip's SHA-256, and CI builds the zip from every pull request's tree, on Linux and on Windows, and
~~~~

Clause, R183:

~~~~text
fails when its SHA-256 differs from the README's,
~~~~

Clause, the new unit:

~~~~text
so that a checksum left behind is found before a tag is pushed
~~~~

Clause, R183:

~~~~text
, while the release workflow publishes no release whose zip differs
~~~~

Clause, the new unit:

~~~~text
(DR-203).
~~~~

### Entry

Old:

~~~~text
CI and the release workflow also hold the plugin to declaring nothing but its hooks (decision 17), and the zip's closed list of files keeps out the files in default places, such as `.mcp.json`, through which a plugin can declare more.
~~~~

New:

~~~~text
CI and the release workflow also hold the plugin to R188 (decision 17), and the zip's closed list of files keeps out the files in default places, such as `.mcp.json`, through which a plugin can declare more.
~~~~

Clause, the new unit:

~~~~text
CI and the release workflow also hold the plugin to
~~~~

Clause, R188:

~~~~text
declaring nothing but its hooks
~~~~

Clause, the new unit:

~~~~text
(decision 17), and the zip's closed list of files keeps out the files in default places, such as `.mcp.json`, through which a plugin can declare more.
~~~~

### Entry

Old:

~~~~text
The repository's root marketplace file holds only the marketplace's name, its owner and one entry that gives the tool's plugin's name and its folder, since an entry's other fields can add commands, agents and skills to the plugin, replace its hooks, stop it loading or start it turned off (see Context), and CI compares the parsed file with the one expected (DR-205).
~~~~

New:

~~~~text
The repository's root marketplace file holds only what R190 gives, since an entry's other fields can add commands, agents and skills to the plugin, replace its hooks, stop it loading or start it turned off (see Context), and CI compares the parsed file with the one expected (DR-205).
~~~~

Clause, the new unit:

~~~~text
The repository's root marketplace file holds only
~~~~

Clause, R190:

~~~~text
the marketplace's name, its owner and one entry that gives the tool's plugin's name and its folder,
~~~~

Clause, the new unit:

~~~~text
since an entry's other fields can add commands, agents and skills to the plugin, replace its hooks, stop it loading or start it turned off (see Context), and CI compares the parsed file with the one expected (DR-205).
~~~~

### Entry

Old:

~~~~text
The folder holds the plugin exactly as a published release's tag builds it, with that release's version in its manifest, and moves only in a pull request after a release.
~~~~

New:

~~~~text
The folder holds the plugin as R184 gives it, and moves only in a pull request after a release.
~~~~

Clause, the new unit:

~~~~text
The folder holds the plugin
~~~~

Clause, R184:

~~~~text
exactly as a published release's tag builds it, with that release's version in its manifest,
~~~~

Clause, the new unit:

~~~~text
and moves only in a pull request after a release.
~~~~

### Entry

Old:

~~~~text
CI takes that tag by its full name, `refs/tags/v<version>`, since git takes a branch of the short name when no such tag exists, requires its commit in the default branch's first-parent history and a published release for it, so that a refused tag, which names no release, does not pass, and fails when the version is lower than at the pull request's base.
~~~~

New:

~~~~text
CI takes that tag by its full name, `refs/tags/v<version>`, since git takes a branch of the short name when no such tag exists, and checks it as R184 says, so that a refused tag, which names no release, does not pass.
~~~~

Clause, the new unit:

~~~~text
CI takes that tag by its full name, `refs/tags/v<version>`, since git takes a branch of the short name when no such tag exists,
~~~~

Clause, R184:

~~~~text
requires its commit in the default branch's first-parent history and a published release for it,
~~~~

Clause, the new unit:

~~~~text
so that a refused tag, which names no release, does not pass
~~~~

Clause, R184:

~~~~text
, and fails when the version is lower than at the pull request's base.
~~~~

### Entry

Old:

~~~~text
`docs/how-it-works.md` gives each workflow's permissions as a table, per workflow and per job, and `tests/test_documentation.py` compares that table with every workflow, `.yml` and `.yaml` alike, in both directions, so that a permission granted and not listed fails it, and so does one listed and not granted.
~~~~

New:

~~~~text
`docs/how-it-works.md` gives each workflow's permissions as a table, per workflow and per job, and `tests/test_documentation.py` compares that table with every workflow, as R101 gives it.
~~~~

Clause, the new unit:

~~~~text
`docs/how-it-works.md` gives each workflow's permissions as a table, per workflow and per job, and `tests/test_documentation.py` compares that table with every workflow
~~~~

Clause, R101:

~~~~text
`.yml` and `.yaml` alike, in both directions, so that a permission granted and not listed fails it, and so does one listed and not granted.
~~~~

### Entry

Old:

~~~~text
The test compares every action and every container or service image the workflows use with the connections the page names.
~~~~

New:

~~~~text
The test holds the actions and images that the workflows use to the page too (R101).
~~~~

Clause, R101:

~~~~text
The test compares every action and every container or service image the workflows use with the connections the page names.
~~~~

### Entry

Old:

~~~~text
`tests/test_spec_form.py` reads every spec that OpenSpec reads, at any depth below `openspec/specs/` and below the `specs/` folder of each change that is not archived, line by line, as OpenSpec reads it, and fails where a spec would be read otherwise than it is written or shown: on a requirement, a scenario, a heading or a line out of the form that R173 to R175 of `project-standards` give, and on a `spec.md` that it does not read and on a symbolic link, as R177 says (DR-193, DR-194); and on text that GitHub would hide or show otherwise than it is, as R176 lists it, so that what GitHub shows of a spec is all that OpenSpec and agents read (DR-195).
~~~~

New:

~~~~text
`tests/test_spec_form.py` reads every spec that OpenSpec reads, as OpenSpec reads it, and fails where a spec would be read otherwise than it is written or shown, as R173 to R177 give it (DR-193, DR-194), so that what GitHub shows of a spec is all that OpenSpec and agents read (DR-195).
~~~~

Clause, the new unit:

~~~~text
`tests/test_spec_form.py` reads every spec that OpenSpec reads
~~~~

Clause, R177:

~~~~text
at any depth below `openspec/specs/` and below the `specs/` folder of each change that is not archived, line by line
~~~~

Clause, the new unit:

~~~~text
as OpenSpec reads it, and fails where a spec would be read otherwise than it is written or shown
~~~~

Clause, R173:

~~~~text
on a requirement,
~~~~

Clause, R174:

~~~~text
a scenario,
~~~~

Clause, R175:

~~~~text
a heading or a line out of the form that R173 to R175 of `project-standards` give
~~~~

Clause, R177:

~~~~text
and on a `spec.md` that it does not read and on a symbolic link, as R177 says
~~~~

Clause, the new unit:

~~~~text
(DR-193, DR-194)
~~~~

Clause, R176:

~~~~text
and on text that GitHub would hide or show otherwise than it is, as R176 lists it
~~~~

Clause, the new unit:

~~~~text
so that what GitHub shows of a spec is all that OpenSpec and agents read (DR-195).
~~~~

### Entry

Old:

~~~~text
Since the test models how the pinned OpenSpec reads a spec, `scripts/verify-openspec.sh` compares the test's reading of every spec and change with what the pinned OpenSpec CLI shows for it, so that a release that reads specs otherwise, or a defect in the test's reader, fails CI in the pull request that brings it (DR-196).
~~~~

New:

~~~~text
Since the test models how the pinned OpenSpec reads a spec, `scripts/verify-openspec.sh` makes the comparison that R178 gives, so that a release that reads specs otherwise, or a defect in the test's reader, fails CI in the pull request that brings it (DR-196).
~~~~

Clause, the new unit:

~~~~text
Since the test models how the pinned OpenSpec reads a spec, `scripts/verify-openspec.sh`
~~~~

Clause, R178:

~~~~text
compares the test's reading of every spec and change with what the pinned OpenSpec CLI shows for it
~~~~

Clause, the new unit:

~~~~text
so that a release that reads specs otherwise, or a defect in the test's reader, fails CI in the pull request that brings it (DR-196).
~~~~

### Entry

Old:

~~~~text
After the README's first paragraph and its status, with no HTML and in at most 200 words outside code, it says how a repository turns the tool on, pinned to a published release, how a person opts in, with the same line in the setup script of a cloud environment that only they use, how a person adds the plugin for a project's cloud threads, in the project's settings, from the latest release's zip after checking its checksum against that release's README, or from this repository's marketplace, named by its address, whose updates need no approval, how an organization tells its members and then opts them in, and how to stop, in every running session too, each step linking the section that gives its detail (R198).
~~~~

New:

~~~~text
After the README's first paragraph and its status, the short start gives what R198 lists, each step linking the section that gives its detail.
~~~~

Clause, the new unit:

~~~~text
After the README's first paragraph and its status,
~~~~

Clause, R198:

~~~~text
with no HTML and in at most 200 words outside code, it says how a repository turns the tool on, pinned to a published release, how a person opts in, with the same line in the setup script of a cloud environment that only they use, how a person adds the plugin for a project's cloud threads, in the project's settings, from the latest release's zip after checking its checksum against that release's README, or from this repository's marketplace, named by its address, whose updates need no approval, how an organization tells its members and then opts them in, and how to stop, in every running session too,
~~~~

Clause, the new unit:

~~~~text
each step linking the section that gives its detail
~~~~

Clause, R198:

~~~~text
(R198).
~~~~

### Entry

Old:

~~~~text
Before any step that opts anyone in, it says what an opt-in records and publishes: that only the sessions of people who are opted in are recorded, in every repository that turns the tool on and for every agent that the tool records, later ones too, that a call counts in the repository that it is made from, whatever it works on, and that what a session spends is committed with its work, which ties it to the person, and published when that work is pushed, even after an opt-out, so that a person who reads no further knows it before they opt in (R199, T145).
~~~~

New:

~~~~text
Before any step that opts anyone in, it says what an opt-in records and publishes, as R199 gives it, so that a person who reads no further knows it before they opt in (R199, T145).
~~~~

Clause, the new unit:

~~~~text
Before any step that opts anyone in, it says what an opt-in records and publishes
~~~~

Clause, R199:

~~~~text
that only the sessions of people who are opted in are recorded, in every repository that turns the tool on and for every agent that the tool records, later ones too, that a call counts in the repository that it is made from, whatever it works on, and that what a session spends is committed with its work, which ties it to the person, and published when that work is pushed, even after an opt-out,
~~~~

Clause, the new unit:

~~~~text
so that a person who reads no further knows it before they opt in (R199, T145).
~~~~

### Entry

Old:

~~~~text
Its links name only the README's headings and this repository's latest release, by its full address, and every address in the README is one that its test lists or, on GitHub, only this repository, its latest release, or a release, a release's file, a file or a folder at a release's tag or a placeholder, since GitHub also serves under this repository's address what others write (R201, T147, DR-215).
~~~~

New:

~~~~text
Its links and every address in the README are held as R198 and R201 give them, since GitHub also serves under this repository's address what others write (R201, T147, DR-215).
~~~~

Clause, R198:

~~~~text
Its links name only the README's headings and this repository's latest release, by its full address,
~~~~

Clause, R201:

~~~~text
and every address in the README is one that its test lists or, on GitHub, only this repository, its latest release, or a release, a release's file, a file or a folder at a release's tag or a placeholder,
~~~~

Clause, the new unit:

~~~~text
since GitHub also serves under this repository's address what others write (R201, T147, DR-215).
~~~~

### Entry

Old:

~~~~text
The detail stays in the README, as the owner chose on 2026-11-10, under the headings that task 4.4 gives, each section's text folded in a `<details>` element, which GitHub shows closed until a reader opens it (A9), and the README holds only printable ASCII and line breaks, and no other text that GitHub hides (T151), so that the README first shows the short start and a list of what the detail covers, while every requirement and record that says the README gives a detail still holds (R200, DR-213).
~~~~

New:

~~~~text
The detail stays in the README, as the owner chose on 2026-11-10, under the headings that task 4.4 gives, each section folded as R200 gives it (A9, T151), so that the README first shows the short start and a list of what the detail covers, while every requirement and record that says the README gives a detail still holds (R200, DR-213).
~~~~

Clause, the new unit:

~~~~text
The detail stays in the README, as the owner chose on 2026-11-10, under the headings that task 4.4 gives,
~~~~

Clause, R200:

~~~~text
each section's text folded in a `<details>` element, which GitHub shows closed until a reader opens it
~~~~

Clause, the new unit:

~~~~text
A9
~~~~

Clause, R200:

~~~~text
and the README holds only printable ASCII and line breaks, and no other text that GitHub hides
~~~~

Clause, the new unit:

~~~~text
T151
~~~~

Clause, the new unit:

~~~~text
so that the README first shows the short start and a list of what the detail covers, while every requirement and record that says the README gives a detail still holds (R200, DR-213).
~~~~

### Entry

Old:

~~~~text
Its sections on the opt-in, on cloud threads and on organizations say that a person sets their own opt-in, or their organization does once it has told them, and that an agent that sets the tool up turns capture on for no one and leaves the opt-in to whoever asked it, since `CLAUDE.md` steers only the agents that work here (R204, DR-214, T158).
~~~~

New:

~~~~text
Its sections on the opt-in, on cloud threads and on organizations leave each opt-in to the person or their organization, as R204 gives it, since `CLAUDE.md` steers only the agents that work here (R204, DR-214, T158).
~~~~

Clause, the new unit:

~~~~text
Its sections on the opt-in, on cloud threads and on organizations
~~~~

Clause, R204:

~~~~text
say that a person sets their own opt-in, or their organization does once it has told them, and that an agent that sets the tool up turns capture on for no one and leaves the opt-in to whoever asked it,
~~~~

Clause, the new unit:

~~~~text
since `CLAUDE.md` steers only the agents that work here (R204, DR-214, T158).
~~~~

### Entry

Old:

~~~~text
Until the root marketplace file holds an entry for the tool's plugin, the README's status says that this repository's marketplace does not serve it yet, which a test holds against that file, and task 4.4 writes the short start only once task 6.8 has removed the root marketplace file, which lists the vendored Superpowers, so that a person who adds the marketplace from the short start is never offered that plugin (R205, T138).
~~~~

New:

~~~~text
The README's status says what R205 gives, and task 4.4 writes the short start only once task 6.8 has removed the root marketplace file, which lists the vendored Superpowers, so that a person who adds the marketplace from the short start is never offered that plugin (R205, T138).
~~~~

Clause, R205:

~~~~text
Until the root marketplace file holds an entry for the tool's plugin, the README's status says that this repository's marketplace does not serve it yet, which a test holds against that file,
~~~~

Clause, the new unit:

~~~~text
and task 4.4 writes the short start only once task 6.8 has removed the root marketplace file, which lists the vendored Superpowers, so that a person who adds the marketplace from the short start is never offered that plugin (R205, T138).
~~~~

### Entry

Old:

~~~~text
An item is named `B-NNN-words.md`, numbered from B-001 without a gap, beside a `README.md` that gives the form, links the roadmap and the README's briefing, and says that an item describes, is neither a promise nor a date and is not a request to start work, what each status means, and that `Done` means that its pull requests have merged to the default branch, while `CHANGELOG.md` names the release that holds it (R217).
~~~~

New:

~~~~text
Each item is a file of its own in the form that R211 gives, beside a `README.md` that says what R217 gives and links the README's briefing (R212).
~~~~

Clause, R211:

~~~~text
An item is named `B-NNN-words.md`, numbered from B-001 without a gap,
~~~~

Clause, R217:

~~~~text
beside a `README.md` that gives the form, links the roadmap
~~~~

Clause, R212:

~~~~text
and the README's briefing,
~~~~

Clause, R217:

~~~~text
and says that an item describes, is neither a promise nor a date and is not a request to start work, what each status means, and that `Done` means that its pull requests have merged to the default branch, while `CHANGELOG.md` names the release that holds it (R217).
~~~~

### Entry

Old:

~~~~text
Compared with the base commit, an item is added only as open or planned, and never moves from open or dropped straight to in progress or done, so that the agreement is a change to a status line that the diff shows; the check examines nothing while no base holds `docs/backlog/`, so that task 1.27 can write the first items with the statuses that the roadmap's marks give them today (R218).
~~~~

New:

~~~~text
Compared with the base commit, an item becomes agreed only as R218 gives it, so that the agreement is a change to a status line that the diff shows, and so that task 1.27 can write the first items with the statuses that the roadmap's marks give them today (R218).
~~~~

Clause, the new unit:

~~~~text
Compared with the base commit,
~~~~

Clause, R218:

~~~~text
an item is added only as open or planned, and never moves from open or dropped straight to in progress or done,
~~~~

Clause, the new unit:

~~~~text
so that the agreement is a change to a status line that the diff shows
~~~~

Clause, R218:

~~~~text
the check examines nothing while no base holds `docs/backlog/`,
~~~~

Clause, the new unit:

~~~~text
so that task 1.27 can write the first items with the statuses that the roadmap's marks give them today (R218).
~~~~

### Entry

Old:

~~~~text
A test, like that of the records, compares the items with the base commit that `tests/test_decisions.py` uses and fails when an item is removed, renamed or moved, so that every link to an item still leads to it once it is done or dropped, and when a branch changes an item's text and leaves its date before the base's, or at the base's when that is not the day of the run, so that two changes to one item can merge on one day, and on a date later than the day on which it runs, in UTC (R216); it also fails on Rests on in another form, on an ID that does not exist, on an item that names a closed record, as R127 asks of every page outside the history, and on an open item whose tasks are all ticked, which is stale (R215, T161).
~~~~

New:

~~~~text
A test, like that of the records, compares the items with the base commit that `tests/test_decisions.py` uses, as R216 gives it, so that every link to an item still leads to it once it is done or dropped, and so that two changes to one item can merge on one day; it also holds R215, as R127 asks of every page outside the history (T161).
~~~~

Clause, the new unit:

~~~~text
A test, like that of the records, compares the items with the base commit that `tests/test_decisions.py` uses
~~~~

Clause, R216:

~~~~text
and fails when an item is removed, renamed or moved,
~~~~

Clause, the new unit:

~~~~text
so that every link to an item still leads to it once it is done or dropped,
~~~~

Clause, R216:

~~~~text
and when a branch changes an item's text and leaves its date before the base's, or at the base's when that is not the day of the run,
~~~~

Clause, the new unit:

~~~~text
so that two changes to one item can merge on one day
~~~~

Clause, R216:

~~~~text
and on a date later than the day on which it runs, in UTC (R216);
~~~~

Clause, R215:

~~~~text
it also fails on Rests on in another form, on an ID that does not exist, on an item that names a closed record,
~~~~

Clause, the new unit:

~~~~text
as R127 asks of every page outside the history
~~~~

Clause, R215:

~~~~text
and on an open item whose tasks are all ticked, which is stale (R215,
~~~~

Clause, the new unit:

~~~~text
T161).
~~~~

### Entry

Old:

~~~~text
The README's list of documentation links it, and its sections are Now, Next, Later, Known limitations and Known bugs, in that order; it opens by saying that it describes, that an item on it is neither a promise nor a date, and that it is not a request to start work (R206).
~~~~

Clause, R206:

~~~~text
The README's list of documentation links it, and its sections are Now, Next, Later, Known limitations and Known bugs, in that order; it opens by saying that it describes, that an item on it is neither a promise nor a date, and that it is not a request to start work (R206).
~~~~

### Entry

Old:

~~~~text
Brief`, giving the item's title, status, date and brief exactly as the item does, and a test fails on a line that differs from its item or links none, on an item that is open to feedback and contributions, planned or in progress and is listed in none of the three or more than once, and on an item that is done or dropped and is still listed, since the changelog says what shipped.
~~~~

New:

~~~~text
Brief`, giving the item's title, status, date and brief exactly as the item does, as R213 holds, and listing no item that is done or dropped, since the changelog says what shipped.
~~~~

Clause, the new unit:

~~~~text
Brief`, giving the item's title, status, date and brief exactly as the item does,
~~~~

Clause, R213:

~~~~text
and a test fails on a line that differs from its item or links none, on an item that is open to feedback and contributions, planned or in progress and is listed in none of the three or more than once, and on an item that is done or dropped and is still listed,
~~~~

Clause, the new unit:

~~~~text
since the changelog says what shipped.
~~~~

### Entry

Old:

~~~~text
Later holds what the first version leaves out, among them other agents than Claude Code, which the owner chose on 2026-11-12 to plan for after the first version (B-017, DR-003, DR-234), and opens by saying that work on an item that is open to feedback and contributions starts with an issue, that an item is built only once it is `Planned`, which only a pull request that the owner merges makes it, and that some items need a spec, a threat review and the owner's decision first; each record that the README's list of what the first version does not support links is named in the field Rests on of an item listed under Later, and each item listed under Next or Later rests on at least one ID (R213, R214, DR-226).
~~~~

New:

~~~~text
Later holds what the first version leaves out, among them other agents than Claude Code, which the owner chose on 2026-11-12 to plan for after the first version (B-017, DR-003, DR-234), and opens and rests as R213 and R214 give it (DR-226).
~~~~

Clause, the new unit:

~~~~text
Later holds what the first version leaves out, among them other agents than Claude Code, which the owner chose on 2026-11-12 to plan for after the first version (B-017, DR-003, DR-234),
~~~~

Clause, R214:

~~~~text
and opens by saying that work on an item that is open to feedback and contributions starts with an issue, that an item is built only once it is `Planned`, which only a pull request that the owner merges makes it, and that some items need a spec, a threat review and the owner's decision first; each record that the README's list of what the first version does not support links is named in the field Rests on of an item listed under Later,
~~~~

Clause, R213:

~~~~text
and each item listed under Next or Later rests on at least one ID
~~~~

Clause, DR-226:

~~~~text
(R213, R214, DR-226).
~~~~

### Entry

Old:

~~~~text
Each feature page named for a spec has that section, which lists the rest of the risks that concern it and links the roadmap, and every risk of every change's design, active or archived, is listed by its title as its design gives it on the roadmap or on a feature page, as the owner chose on 2026-11-11 (R208, DR-220, T162).
~~~~

New:

~~~~text
Each feature page named for a spec has that section, which lists the rest of the risks that concern it, so that every risk is listed as R208 gives it, as the owner chose on 2026-11-11 (DR-220, T162).
~~~~

Clause, the new unit:

~~~~text
Each feature page named for a spec has that section, which lists the rest of the risks that concern it
~~~~

Clause, R208:

~~~~text
and links the roadmap, and every risk of every change's design, active or archived, is listed by its title as its design gives it on the roadmap or on a feature page
~~~~

Clause, the new unit:

~~~~text
as the owner chose on 2026-11-11
~~~~

Clause, R208:

~~~~text
(R208,
~~~~

Clause, the new unit:

~~~~text
DR-220, T162).
~~~~

### Entry

Old:

~~~~text
The roadmap and the backlog items name issues and pull requests by number alone, with no link, as the owner chose on 2026-11-11 and agreed for the items on 2026-11-13 (DR-228, T164), and their other links, and those of each feature page's section on known limitations and the roadmap, name only a heading of their own page or a tracked file of this repository, each link read from its `](` in prose and code alike, with no fenced or indented code, no image, no `@` and no space in inline code, so that commands are given only in the README, whose tests hold them (R209, DR-227, T160, T163).
~~~~

New:

~~~~text
The roadmap and the backlog items name issues and pull requests by number alone, with no link, as the owner chose on 2026-11-11 and agreed for the items on 2026-11-13 (DR-228, T164), and their other links, and those of each feature page's section on known limitations and the roadmap, are held as R209 gives them, so that commands are given only in the README, whose tests hold them (DR-227, T160, T163).
~~~~

Clause, the new unit:

~~~~text
The roadmap and the backlog items name issues and pull requests by number alone, with no link, as the owner chose on 2026-11-11 and agreed for the items on 2026-11-13 (DR-228, T164), and their other links, and those of each feature page's section on known limitations and the roadmap,
~~~~

Clause, R209:

~~~~text
name only a heading of their own page or a tracked file of this repository, each link read from its `](` in prose and code alike, with no fenced or indented code, no image, no `@` and no space in inline code,
~~~~

Clause, the new unit:

~~~~text
so that commands are given only in the README, whose tests hold them
~~~~

Clause, R209:

~~~~text
(R209,
~~~~

Clause, the new unit:

~~~~text
DR-227, T160, T163).
~~~~

### Entry

Old:

~~~~text
The README is the table's one home, and `CONTRIBUTING.md` and `docs/backlog/README.md` link the section; a test fails when the briefing is missing or follows the setup, leaves out a statement, its table lacks a column or a row or gives them out of order, a row links no page, another tracked Markdown file gives the table's header and rows, or either page does not link the section (R212).
~~~~

New:

~~~~text
The README is the table's one home, and `CONTRIBUTING.md` and `docs/backlog/README.md` link the section, as R212 holds.
~~~~

Clause, the new unit:

~~~~text
The README is the table's one home, and `CONTRIBUTING.md` and `docs/backlog/README.md` link the section
~~~~

Clause, R212:

~~~~text
a test fails when the briefing is missing or follows the setup, leaves out a statement, its table lacks a column or a row or gives them out of order, a row links no page, another tracked Markdown file gives the table's header and rows, or either page does not link the section (R212).
~~~~

### Entry

Old:

~~~~text
Its sections are its concerns, in this order: Architecture and integration, Security, Privacy, Identity and credentials, Supply chain and releases, Testing, Decisions and documentation, Working with agents, and Conventions, as arc42 keeps one heading for each crosscutting concept.
~~~~

New:

~~~~text
Its sections are its concerns, in the order that R219 gives, as arc42 keeps one heading for each crosscutting concept.
~~~~

Clause, the new unit:

~~~~text
Its sections are its concerns, in
~~~~

Clause, R219:

~~~~text
this order: Architecture and integration, Security, Privacy, Identity and credentials, Supply chain and releases, Testing, Decisions and documentation, Working with agents, and Conventions,
~~~~

Clause, the new unit:

~~~~text
as arc42 keeps one heading for each crosscutting concept.
~~~~

### Entry

Old:

~~~~text
It opens with a text that R219 gives word for word, so that a line added to it or taken from it fails a test, as a test of each statement's presence would not (T180): that the specs decide what the tool does, `CLAUDE.md` what an agent may do and the guide how the project builds, that both win where the guide differs from them and the owner is told, that the guide never widens what `CLAUDE.md` lets an agent do, that an entry cites the requirement or the rule of `CLAUDE.md` that it rests on rather than stating it again, and that where an entry and a step of a Superpowers skill differ, the step is followed and the owner is told (T181); that the guide steers as the default branch holds it, a principle changing, or moving to another concern, only when the owner asks for it (T179, T183), and that it speaks to work on this repository, not to setting the tool up, which is the README's section on adopting it, an agent that sets the tool up turning capture on for no one (T158); what Where we stand gives, and that it gives where the default branch stands, a release's guide being the copy at its tag; and that a gap is not, by being there, a request to start work, closing only through its backlog item, while work outside that item leaves what the gap concerns as it stands, and that a principle knowingly accepted is accepted only where its record says (T159).
~~~~

New:

~~~~text
It opens with a text that R219 gives word for word, so that a line added to it or taken from it fails a test, as a test of each statement's presence would not (T158, T159, T179, T180, T181, T183).
~~~~

Clause, the new unit:

~~~~text
It opens with a text that R219 gives word for word, so that a line added to it or taken from it fails a test, as a test of each statement's presence would not
~~~~

Clause, R219:

~~~~text
(T180): that the specs decide what the tool does, `CLAUDE.md` what an agent may do and the guide how the project builds, that both win where the guide differs from them and the owner is told, that the guide never widens what `CLAUDE.md` lets an agent do, that an entry cites the requirement or the rule of `CLAUDE.md` that it rests on rather than stating it again, and that where an entry and a step of a Superpowers skill differ, the step is followed and the owner is told (T181); that the guide steers as the default branch holds it, a principle changing, or moving to another concern, only when the owner asks for it (T179, T183), and that it speaks to work on this repository, not to setting the tool up, which is the README's section on adopting it, an agent that sets the tool up turning capture on for no one (T158); what Where we stand gives, and that it gives where the default branch stands, a release's guide being the copy at its tag; and that a gap is not, by being there, a request to start work, closing only through its backlog item, while work outside that item leaves what the gap concerns as it stands, and that a principle knowingly accepted is accepted only where its record says (T159).
~~~~

### Entry

Old:

~~~~text
Its last line names the assessment, by its date, or the release, by its version, for which its entries were last read (R219).
~~~~

Clause, R219:

~~~~text
Its last line names the assessment, by its date, or the release, by its version, for which its entries were last read (R219).
~~~~

### Entry

Old:

~~~~text
An entry under Working with agents cites `CLAUDE.md` in its Held by, so that it adds to a rule of `CLAUDE.md` and never stands in for one more narrowly worded (R220, T180).
~~~~

New:

~~~~text
An entry under Working with agents cites `CLAUDE.md` as R220 gives it, so that it adds to a rule of `CLAUDE.md` and never stands in for one more narrowly worded (T180).
~~~~

Clause, R220:

~~~~text
An entry under Working with agents cites `CLAUDE.md` in its Held by,
~~~~

Clause, the new unit:

~~~~text
so that it adds to a rule of `CLAUDE.md` and never stands in for one more narrowly worded
~~~~

Clause, R220:

~~~~text
(R220,
~~~~

Clause, the new unit:

~~~~text
T180).
~~~~

### Entry

Old:

~~~~text
Where we stand opens with `Followed.` while every task that the entry's Held by cites is ticked, `Designed.` while one of them is not, so that no reader takes a principle that the specs hold for one that the code holds, `Knowingly accepted.` with the record that gives the reason, or `Gap.` with the backlog item that closes it, and a test fails while a gap names an item that is done or dropped, so that the pull request that finishes or drops an item says again where the project stands (R226, DR-241, T170).
~~~~

New:

~~~~text
Where we stand opens as R226 gives it, so that no reader takes a principle that the specs hold for one that the code holds, and so that the pull request that finishes or drops an item says again where the project stands (DR-241, T170).
~~~~

Clause, R226:

~~~~text
Where we stand opens with `Followed.` while every task that the entry's Held by cites is ticked, `Designed.` while one of them is not,
~~~~

Clause, the new unit:

~~~~text
so that no reader takes a principle that the specs hold for one that the code holds
~~~~

Clause, R226:

~~~~text
`Knowingly accepted.` with the record that gives the reason, or `Gap.` with the backlog item that closes it, and a test fails while a gap names an item that is done or dropped,
~~~~

Clause, the new unit:

~~~~text
so that the pull request that finishes or drops an item says again where the project stands
~~~~

Clause, R226:

~~~~text
(R226,
~~~~

Clause, the new unit:

~~~~text
DR-241, T170).
~~~~

### Entry

Old:

~~~~text
Compared with the base, a test fails on an entry that leaves `Gap.`, or whose gap stops naming an item that it named, while that item is neither `Done` nor `Dropped`, so that a gap closes, or passes to other work, only through its item, and not in the pull request whose work it holds back (R233, DR-241, T182).
~~~~

New:

~~~~text
Compared with the base, a gap of the guide closes as R233 gives it, so that a gap closes, or passes to other work, only through its item, and not in the pull request whose work it holds back (DR-241, T182).
~~~~

Clause, the new unit:

~~~~text
Compared with the base,
~~~~

Clause, R233:

~~~~text
a test fails on an entry that leaves `Gap.`, or whose gap stops naming an item that it named, while that item is neither `Done` nor `Dropped`,
~~~~

Clause, the new unit:

~~~~text
so that a gap closes, or passes to other work, only through its item, and not in the pull request whose work it holds back
~~~~

Clause, R233:

~~~~text
(R233,
~~~~

Clause, the new unit:

~~~~text
DR-241, T182).
~~~~

### Entry

Old:

~~~~text
The ticks are read from each change's `tasks.md` as GitHub shows them: a test fails on a task given twice, on a checkbox that the checks do not read as a task, and on fenced code, front matter, a byte-order mark, a `<` before a letter, `/`, `!` or `?` outside inline code on its line, with which an HTML comment or tag opens, a line that opens with `$$`, or a carriage return without a line feed after it, in which a tick would be read that GitHub does not show as one (R232, T184), and no attribute hides the diff of a change's `tasks.md` (R134).
~~~~

New:

~~~~text
The ticks are read from each change's `tasks.md` as GitHub shows them, as R232 and R134 give it (T184).
~~~~

Clause, the new unit:

~~~~text
The ticks are read from each change's `tasks.md` as GitHub shows them
~~~~

Clause, R232:

~~~~text
a test fails on a task given twice, on a checkbox that the checks do not read as a task, and on fenced code, front matter, a byte-order mark, a `<` before a letter, `/`, `!` or `?` outside inline code on its line, with which an HTML comment or tag opens, a line that opens with `$$`, or a carriage return without a line feed after it, in which a tick would be read that GitHub does not show as one (R232,
~~~~

Clause, the new unit:

~~~~text
T184
~~~~

Clause, R134:

~~~~text
and no attribute hides the diff of a change's `tasks.md` (R134).
~~~~

### Entry

Old:

~~~~text
Under Security, Privacy, Identity and credentials, and Supply chain and releases, the four concerns that adopters rely on, a principle knowingly accepted names a record that the owner decided, so that no change's own choice reads as the project's accepted risk, and a gap names an item that is `Planned` or `In progress`, so that no such gap waits on an item that no one has agreed to build (R226, DR-241, T177).
~~~~

New:

~~~~text
Under Security, Privacy, Identity and credentials, and Supply chain and releases, the four concerns that adopters rely on, what is knowingly accepted and what is a gap are held as R226 gives it, so that no change's own choice reads as the project's accepted risk, and so that no such gap waits on an item that no one has agreed to build (DR-241, T177).
~~~~

Clause, the new unit:

~~~~text
Under Security, Privacy, Identity and credentials, and Supply chain and releases, the four concerns that adopters rely on,
~~~~

Clause, R226:

~~~~text
a principle knowingly accepted names a record that the owner decided,
~~~~

Clause, the new unit:

~~~~text
so that no change's own choice reads as the project's accepted risk,
~~~~

Clause, R226:

~~~~text
and a gap names an item that is `Planned` or `In progress`,
~~~~

Clause, the new unit:

~~~~text
so that no such gap waits on an item that no one has agreed to build
~~~~

Clause, R226:

~~~~text
(R226,
~~~~

Clause, the new unit:

~~~~text
DR-241, T177).
~~~~

### Entry

Old:

~~~~text
The entries are read again at each assessment and before each release, each gap found becoming a backlog item, and the release workflow refuses a tag whose guide does not say that its entries were last read for that tag's version, or whose changelog entry leaves out the item of a gap under those four concerns, so that each release's text tells its adopters of each such gap (R230, DR-241, T177).
~~~~

New:

~~~~text
The entries are read again at each assessment and before each release, each gap found becoming a backlog item, and the release workflow holds each tag to R230, so that each release's text tells its adopters of each such gap (DR-241, T177).
~~~~

Clause, the new unit:

~~~~text
The entries are read again at each assessment and before each release, each gap found becoming a backlog item, and the release workflow
~~~~

Clause, R230:

~~~~text
refuses a tag whose guide does not say that its entries were last read for that tag's version, or whose changelog entry leaves out the item of a gap under those four concerns,
~~~~

Clause, the new unit:

~~~~text
so that each release's text tells its adopters of each such gap
~~~~

Clause, R230:

~~~~text
(R230,
~~~~

Clause, the new unit:

~~~~text
DR-241, T177).
~~~~

### Entry

Old:

~~~~text
Compared with the base commit that the records' check uses, a pull request that adds or removes an entry, moves one to another concern, or changes its Statement, Rationale, Implications, Pattern or Anti-patterns, changes no file outside `docs/`, `openspec/`, `CLAUDE.md` and `CHANGELOG.md`, so that one diff cannot both weaken a principle and add the work that it forbade, and one that gives an agreed item a gap changes that item's What done looks like, which only the owner's words change, while Held by, Rests on and Where we stand change with the work that they follow; each check reads nothing while no base holds the guide (R228, R231, DR-239, DR-240, T166, T179, T183).
~~~~

New:

~~~~text
Compared with the base commit that the records' check uses, a pull request that changes a principle of the guide is held as R228 gives it, so that one diff cannot both weaken a principle and add the work that it forbade, and one that gives an agreed item a gap changes that item's What done looks like (R231), which only the owner's words change, while Held by, Rests on and Where we stand change with the work that they follow (DR-239, DR-240, T166, T179, T183).
~~~~

Clause, the new unit:

~~~~text
Compared with the base commit that the records' check uses, a pull request that
~~~~

Clause, R228:

~~~~text
adds or removes an entry, moves one to another concern, or changes its Statement, Rationale, Implications, Pattern or Anti-patterns, changes no file outside `docs/`, `openspec/`, `CLAUDE.md` and `CHANGELOG.md`,
~~~~

Clause, the new unit:

~~~~text
so that one diff cannot both weaken a principle and add the work that it forbade, and one that gives an agreed item a gap changes that item's What done looks like
~~~~

Clause, the new unit:

~~~~text
which only the owner's words change, while Held by, Rests on and Where we stand change with the work that they follow
~~~~

Clause, R228:

~~~~text
each check reads nothing while no base holds the guide
~~~~

Clause, R231:

~~~~text
(R228, R231,
~~~~

Clause, the new unit:

~~~~text
DR-239, DR-240, T166, T179, T183).
~~~~

### Entry

Old:

~~~~text
The records are in `docs/decisions/`, one Markdown file each, named `DR-NNN-<words>.md` with the number in ASCII digits, padded to three, and `docs/decisions/README.md` is their index, with one row per record giving its title, type, status, decider, requirements and threats.
~~~~

New:

~~~~text
The records are in `docs/decisions/`, one Markdown file each, named and indexed as R124 and R125 give it, the number padded to three.
~~~~

Clause, the new unit:

~~~~text
The records are in `docs/decisions/`, one Markdown file each,
~~~~

Clause, R124:

~~~~text
named `DR-NNN-<words>.md` with the number in ASCII digits,
~~~~

Clause, the new unit:

~~~~text
padded to three
~~~~

Clause, R125:

~~~~text
and `docs/decisions/README.md` is their index, with one row per record giving its title, type, status, decider, requirements and threats.
~~~~

### Entry

Old:

~~~~text
The folder holds nothing else, each record a file and not a link, and no file elsewhere is named as a record.
~~~~

Clause, R133:

~~~~text
The folder holds nothing else, each record a file and not a link, and no file elsewhere is named as a record.
~~~~

### Entry

Old:

~~~~text
Its sections follow, each once and in this order: Context, Decision, Alternatives, Consequences, Scope, and What reversing it would change.
~~~~

Clause, R124:

~~~~text
Its sections follow, each once and in this order: Context, Decision, Alternatives, Consequences, Scope, and What reversing it would change.
~~~~

### Entry

Old:

~~~~text
It holds only printable ASCII characters and line breaks, and links only from a record's ID to that record's file.
~~~~

Clause, R128:

~~~~text
It holds only printable ASCII characters and line breaks, and links only from a record's ID to that record's file.
~~~~

### Entry

Old:

~~~~text
The closed record's status becomes closed and its "Closed by" names the new record, which names it in "Replaces".
~~~~

Clause, R129:

~~~~text
The closed record's status becomes closed
~~~~

Clause, R126:

~~~~text
and its "Closed by" names the new record, which names it in "Replaces".
~~~~

### Entry

Old:

~~~~text
Threat IDs, like requirement IDs, are retired rather than reused, and the threat model lists the retired ones.
~~~~

New:

~~~~text
Threat IDs, like requirement IDs, are retired rather than reused (R132).
~~~~

Clause, the new unit:

~~~~text
Threat IDs, like requirement IDs, are retired rather than reused
~~~~

Clause, R132:

~~~~text
and the threat model lists the retired ones.
~~~~

### Entry

Old:

~~~~text
Its entry names what rests on it, by requirement, threat and record ID, says what would change if it is wrong, never how to change it, and lists its facts, each with where it is relied on, by ID or by path, and how it is checked: `tested`, naming the test; `observed`, naming the file under `tests/` that reproduces what was seen, the date, and the program, the version that it prints and its build; `documented`, linking by its address a vendor's page on a host that the test lists, or a file at a full commit of a GitHub repository that it lists, with the date it was read; or `not yet`, naming the task that will check it or saying why none will.
~~~~

New:

~~~~text
Its entry names what rests on it, says what would change if it is wrong, never how to change it, and lists its facts, each with where it is relied on and how it is checked, as R135 and R140 give them.
~~~~

Clause, the new unit:

~~~~text
Its entry names what rests on it
~~~~

Clause, R135:

~~~~text
by requirement, threat and record ID
~~~~

Clause, the new unit:

~~~~text
says what would change if it is wrong, never how to change it, and lists its facts, each with where it is relied on
~~~~

Clause, R140:

~~~~text
by ID or by path, and how it is checked: `tested`, naming the test; `observed`, naming the file under `tests/` that reproduces what was seen, the date, and the program, the version that it prints and its build;
~~~~

Clause, R140:

~~~~text
`documented`, linking by its address a vendor's page on a host that the test lists, or a file at a full commit of a GitHub repository that it lists, with the date it was read;
~~~~

Clause, R135:

~~~~text
or `not yet`, naming the task that will check it or saying why none will.
~~~~

### Entry

Old:

~~~~text
The assumptions are listed by the highest impact among the threats that rest on them, then least checked first, an assumption being as checked as its least checked fact, from `not yet` through `documented` and `observed` to `tested`, then by the highest risk among those threats, all read from the threat model, so a changed rating or check changes the order and no assumption is rated on its own; an assumption that no threat rests on comes last.
~~~~

New:

~~~~text
The assumptions are listed in the order that R136 gives, an assumption being as checked as its least checked fact, from `not yet` through `documented` and `observed` to `tested`, all read from the threat model, so a changed rating or check changes the order and no assumption is rated on its own.
~~~~

Clause, the new unit:

~~~~text
The assumptions are listed
~~~~

Clause, R136:

~~~~text
by the highest impact among the threats that rest on them, then least checked first,
~~~~

Clause, the new unit:

~~~~text
an assumption being as checked as its least checked fact, from `not yet` through `documented` and `observed` to `tested`,
~~~~

Clause, R136:

~~~~text
then by the highest risk among those threats,
~~~~

Clause, the new unit:

~~~~text
all read from the threat model, so a changed rating or check changes the order and no assumption is rated on its own
~~~~

Clause, R136:

~~~~text
an assumption that no threat rests on comes last.
~~~~

### Entry

Old:

~~~~text
It leaves as written each requirement's or scenario's title that an accepted record quotes, the records and the specs read where HEAD left the default branch, so that a record that a pull request adds keeps no title's words, and fails when such a title leaves the specs, since the record keeps its quote (DR-121).
~~~~

New:

~~~~text
It leaves as written each requirement's or scenario's title that an accepted record quotes, as R137 gives it, the records and the specs read where HEAD left the default branch, since the record keeps its quote (DR-121).
~~~~

Clause, the new unit:

~~~~text
It leaves as written each requirement's or scenario's title that an accepted record quotes,
~~~~

Clause, the new unit:

~~~~text
the records and the specs read where HEAD left the default branch,
~~~~

Clause, R137:

~~~~text
so that a record that a pull request adds keeps no title's words, and fails when such a title leaves the specs,
~~~~

Clause, the new unit:

~~~~text
since the record keeps its quote (DR-121).
~~~~

### Entry

Old:

~~~~text
A golden entry, figure or working changes only in a pull request that changes a spec or nothing outside the set, and one that the latest release's tag holds is named in the changelog's unreleased section (R141).
~~~~

Clause, R141:

~~~~text
A golden entry, figure or working changes only in a pull request that changes a spec or nothing outside the set, and one that the latest release's tag holds is named in the changelog's unreleased section (R141).
~~~~

### Entry

Old:

~~~~text
For each ledger format that a release wrote, sessions as that release wrote them keep their figures for as long as the report reads that format (R142).
~~~~

Clause, R142:

~~~~text
For each ledger format that a release wrote, sessions as that release wrote them keep their figures for as long as the report reads that format (R142).
~~~~

### Entry

Old:

~~~~text
The roadmap, every file in `docs/backlog/`, and each feature page's section on known limitations and the roadmap, hold no text that GitHub hides, as the README holds none (R210, T165).
~~~~

Clause, R210:

~~~~text
The roadmap, every file in `docs/backlog/`, and each feature page's section on known limitations and the roadmap, hold no text that GitHub hides,
~~~~

Clause, R200:

~~~~text
as the README holds none
~~~~

Clause, R210:

~~~~text
(R210, T165).
~~~~

### Entry

Old:

~~~~text
Retention, over a window of 30 days, which the owner picked on 2026-11-03 from 7, 14 and 30: a run records no call whose day is more than 30 days before the run's day, and drops a waiting call, a flag due or a taken call's note that old, a flag by the day a run last raised it, flagging a dropped waiting call for its age in the next ledger file staged for its worktree and branch, so that the store never holds a call that it may still record without its note; a session's notes go once none of its runs has come within those 30 days; a staged file's note that old is taken back as for a command that is over, and a take-back's note that old is dropped.
~~~~

New:

~~~~text
Retention, over a window of 30 days, which the owner picked on 2026-11-03 from 7, 14 and 30, is as R150 gives it, so that the store never holds a call that it may still record without its note.
~~~~

Clause, the new unit:

~~~~text
Retention, over a window of 30 days, which the owner picked on 2026-11-03 from 7, 14 and 30
~~~~

Clause, R150:

~~~~text
a run records no call whose day is more than 30 days before the run's day, and drops a waiting call, a flag due or a taken call's note that old, a flag by the day a run last raised it, flagging a dropped waiting call for its age in the next ledger file staged for its worktree and branch,
~~~~

Clause, the new unit:

~~~~text
so that the store never holds a call that it may still record without its note
~~~~

Clause, R150:

~~~~text
a session's notes go once none of its runs has come within those 30 days; a staged file's note that old is taken back as for a command that is over, and a take-back's note that old is dropped.
~~~~

### Entry

Old:

~~~~text
A run that leaves the store holding nothing, no flag among it, removes its file and its folder.
~~~~

Clause, R151:

~~~~text
A run that leaves the store holding nothing, no flag among it, removes its file and its folder.
~~~~

### Entry

Old:

~~~~text
Protection: each write leaves the folder with mode 0700 and the file with 0600, whatever the umask or the modes it found.
~~~~

New:

~~~~text
Protection: each write leaves the folder and the file readable and writable by their owner alone, as R152 gives it.
~~~~

Clause, the new unit:

~~~~text
Protection: each write leaves the folder
~~~~

Clause, R152:

~~~~text
with mode 0700 and the file with 0600, whatever the umask or the modes it found.
~~~~

### Entry

Old:

~~~~text
A run that cannot create or enter its own folder records, stages, takes back and puts back nothing, says so on standard error in its own words, and exits with success.
~~~~

Clause, R152:

~~~~text
A run that cannot create or enter its own folder records, stages, takes back and puts back nothing, says so on standard error in its own words, and exits with success.
~~~~

### Entry

Old:

~~~~text
A note's paths are acted on only for a file of the form that the step writes, in the ledger folder of a worktree whose git common directory is this repository's, and a run checks each waiting call's entry again when it stages it, by the rules that it records by, so that an entry that someone wrote into the store carries nothing into a ledger file.
~~~~

New:

~~~~text
A note's paths are acted on only as R152 gives it, and a run checks each waiting call's entry again when it stages it, by the rules that it records by, so that an entry that someone wrote into the store carries nothing into a ledger file.
~~~~

Clause, the new unit:

~~~~text
A note's paths are acted on only
~~~~

Clause, R152:

~~~~text
for a file of the form that the step writes, in the ledger folder of a worktree whose git common directory is this repository's,
~~~~

Clause, the new unit:

~~~~text
and a run checks each waiting call's entry again when it stages it, by the rules that it records by, so that an entry that someone wrote into the store carries nothing into a ledger file.
~~~~

### Entry

Old:

~~~~text
A store that the person, or anything else, removes, or that does not parse, as when a sync or a power loss cut it short, takes its notes with it: the next run that finds both switches on begins a new interval, so that no call that answers a line written before that run is recorded, however far the transcripts were read, and a ledger file staged before the removal is left to git, since no note says that a run staged it, so the README says to look for one with `git status`, in every worktree that `git worktree list` names, before removing the store.
~~~~

New:

~~~~text
A store that the person, or anything else, removes, or that does not parse, as when a sync or a power loss cut it short, takes its notes with it, as R153 gives it, however far the transcripts were read, and leaves to git a ledger file staged before, since no note says that a run staged it, so the README says to look for one with `git status`, in every worktree that `git worktree list` names, before removing the store.
~~~~

Clause, the new unit:

~~~~text
A store that the person, or anything else, removes, or that does not parse, as when a sync or a power loss cut it short, takes its notes with it
~~~~

Clause, R153:

~~~~text
the next run that finds both switches on begins a new interval, so that no call that answers a line written before that run is recorded,
~~~~

Clause, the new unit:

~~~~text
however far the transcripts were read,
~~~~

Clause, R153:

~~~~text
and a ledger file staged before the removal is left to git,
~~~~

Clause, the new unit:

~~~~text
since no note says that a run staged it, so the README says to look for one with `git status`, in every worktree that `git worktree list` names, before removing the store.
~~~~

### Entry

Old:

~~~~text
Every version names a call by the same id, the SHA-256 hash of its message id, so that a call is counted once whichever versions its entries are in, and states the format's version and the release on the first line in the same place and form, so that a report reads both from a file of a version that it does not read, and can say that it comes from a later release (DR-208).
~~~~

New:

~~~~text
Every version names a call as R163 gives it and states the format's version and the release on the first line as R156 gives it, so that a report reads both from a file of a version that it does not read, and can say that it comes from a later release (DR-208).
~~~~

Clause, the new unit:

~~~~text
Every version names a call
~~~~

Clause, R163:

~~~~text
by the same id, the SHA-256 hash of its message id, so that a call is counted once whichever versions its entries are in,
~~~~

Clause, the new unit:

~~~~text
and states the format's version and the release on the first line
~~~~

Clause, R156:

~~~~text
in the same place and form,
~~~~

Clause, the new unit:

~~~~text
so that a report reads both from a file of a version that it does not read, and can say that it comes from a later release (DR-208).
~~~~

### Entry

Old:

~~~~text
The report reads each file by its version's rules, which it keeps for every version that a release wrote (DR-040), matching the version exactly as a whole number and choosing no code by its value, and counts as a refused file, using none of its entries, counts or flags, one whose first line states no version or one that it does not read, or breaks its version's rules, so that a report older than the hook says what it could not read rather than misreading it; a line shaped as a first line anywhere else is a refused line.
~~~~

New:

~~~~text
The report reads each file by its version's rules, which it keeps for every version that a release wrote (DR-040), as R158 gives it, so that a report older than the hook says what it could not read rather than misreading it.
~~~~

Clause, the new unit:

~~~~text
The report reads each file by its version's rules, which it keeps for every version that a release wrote (DR-040)
~~~~

Clause, R158:

~~~~text
matching the version exactly as a whole number and choosing no code by its value, and counts as a refused file, using none of its entries, counts or flags, one whose first line states no version or one that it does not read, or breaks its version's rules,
~~~~

Clause, the new unit:

~~~~text
so that a report older than the hook says what it could not read rather than misreading it
~~~~

Clause, R158:

~~~~text
a line shaped as a first line anywhere else is a refused line.
~~~~

### Entry

Old:

~~~~text
It reads the default branch's earlier ledger files by the versions that they state too, skipping one that it does not read and giving their number in its job summary, and capture skips such a file in the branch it reads.
~~~~

Clause, R168:

~~~~text
It reads the default branch's earlier ledger files by the versions that they state too, skipping one that it does not read and giving their number in its job summary,
~~~~

Clause, R167:

~~~~text
and capture skips such a file in the branch it reads.
~~~~

### Entry

Old:

~~~~text
A restored ledger file, or one that holds at least one entry, each of which the default branch already held, adds no counts and no flags.
~~~~

Clause, R95:

~~~~text
A restored ledger file, or one that holds at least one entry, each of which the default branch already held, adds no counts and no flags.
~~~~

### Entry

Old:

~~~~text
The comment says when the pull request's ledger files flag calls left out, for each reason, as what those files say, with no count, and that the token cost, each of its parts and the total are then lower bounds, and it always says that calls that no ledger file holds are neither counted nor flagged.
~~~~

Clause, R157:

~~~~text
The comment says when the pull request's ledger files flag calls left out, for each reason, as what those files say, with no count, and that the token cost, each of its parts and the total are then lower bounds,
~~~~

Clause, R157:

~~~~text
and it always says that calls that no ledger file holds are neither counted nor flagged.
~~~~

### Entry

Old:

~~~~text
The plugin's hooks run the same file, from the plugin's own folder, for the same events and with the same condition and timeouts as the hook file's registration, through a command that names the plugin form with an argument, ends in `; exit 0` and prints nothing on standard output.
~~~~

New:

~~~~text
The plugin's hooks run the same file as R179 gives it, with the same timeouts as the hook file's registration, through a command that names the plugin form with an argument and ends in `; exit 0`.
~~~~

Clause, the new unit:

~~~~text
The plugin's hooks run the same file
~~~~

Clause, R179:

~~~~text
from the plugin's own folder, for the same events and with the same condition and
~~~~

Clause, the new unit:

~~~~text
timeouts as the hook file's registration
~~~~

Clause, the new unit:

~~~~text
through a command that names the plugin form with an argument
~~~~

Clause, the new unit:

~~~~text
ends in `; exit 0`
~~~~

Clause, R179:

~~~~text
and prints nothing on standard output.
~~~~

### Entry

Old:

~~~~text
The plugin declares nothing but those hooks: its manifest holds only its name, version, description, author, licence and repository, its hooks are all command hooks, and each commit builds it with the hook file, byte for byte, as its capture step, never from the marketplace's plugin folder, which holds a published release's build (decision 11), so that it runs nothing that the zip's list of files, its checksum and the bill of materials do not show, and CI and the release workflow fail where any of these does not hold in the plugin that a commit builds (DR-197).
~~~~

New:

~~~~text
The plugin declares nothing but those hooks, and each commit builds it as R188 gives it, never from the marketplace's plugin folder, which holds a published release's build (decision 11), so that it runs nothing that the zip's list of files, its checksum and the bill of materials do not show (DR-197).
~~~~

Clause, the new unit:

~~~~text
The plugin declares nothing but those hooks
~~~~

Clause, R188:

~~~~text
its manifest holds only its name, version, description, author, licence and repository, its hooks are all command hooks, and each commit builds it with the hook file, byte for byte, as its capture step,
~~~~

Clause, the new unit:

~~~~text
never from the marketplace's plugin folder, which holds a published release's build (decision 11), so that it runs nothing that the zip's list of files, its checksum and the bill of materials do not show
~~~~

Clause, R188:

~~~~text
and CI and the release workflow fail where any of these does not hold in the plugin that a commit builds
~~~~

Clause, the new unit:

~~~~text
(DR-197).
~~~~

### Entry

Old:

~~~~text
So a run of the plugin works first on the repository where each git command of its input that the hook's condition matches runs, read as decision 1 reads where a commit runs, so that a command that changes the branch of another repository, as `git -C <path> switch` does, finds that repository's waiting calls recorded on the branch checked out before it; then on the repository that holds the hook input's working directory; then on the repository that holds the project directory or, when no repository holds it, on each repository whose top level is directly inside it, as a project's thread's folder holds its clones, in the order of their paths, so that what a run reaches within its time budget does not depend on the order in which the system lists them (DR-198).
~~~~

New:

~~~~text
So a run of the plugin works on the repositories that it meets in the order that R180 gives, each git command's read as decision 1 reads where a commit runs, so that a command that changes the branch of another repository, as `git -C <path> switch` does, finds that repository's waiting calls recorded on the branch checked out before it, and on the clones that the project directory holds, as a project's thread's folder holds its clones, in the order of their paths, so that what a run reaches within its time budget does not depend on the order in which the system lists them (DR-198).
~~~~

Clause, the new unit:

~~~~text
So a run of the plugin works
~~~~

Clause, R180:

~~~~text
first on the repository where each git command of its input that the hook's condition matches runs,
~~~~

Clause, the new unit:

~~~~text
read as decision 1 reads where a commit runs, so that a command that changes the branch of another repository, as `git -C <path> switch` does, finds that repository's waiting calls recorded on the branch checked out before it
~~~~

Clause, R180:

~~~~text
then on the repository that holds the hook input's working directory; then on the repository that holds the project directory or, when no repository holds it, on each repository whose top level is directly inside it,
~~~~

Clause, the new unit:

~~~~text
as a project's thread's folder holds its clones, in the order of their paths, so that what a run reaches within its time budget does not depend on the order in which the system lists them (DR-198).
~~~~

### Entry

Old:

~~~~text
It finds each by reading the git files on the way itself, before it starts any program, as a run finds its own repository (decision 1), leaves out one whose files it cannot read, and in each of the others does what decision 1 and decision 6 say of this repository, with that repository's switches, intervals, store and ledger files, recording only the calls whose line gives a working directory in it.
~~~~

New:

~~~~text
It finds each as R180 gives it, as a run finds its own repository (decision 1), and in each of the others does what decision 1 and decision 6 say of this repository, with that repository's switches, intervals, store and ledger files.
~~~~

Clause, the new unit:

~~~~text
It finds each
~~~~

Clause, R180:

~~~~text
by reading the git files on the way itself, before it starts any program,
~~~~

Clause, the new unit:

~~~~text
as a run finds its own repository (decision 1),
~~~~

Clause, R180:

~~~~text
leaves out one whose files it cannot read,
~~~~

Clause, the new unit:

~~~~text
and in each of the others does what decision 1 and decision 6 say of this repository, with that repository's switches, intervals, store and ledger files
~~~~

Clause, R180:

~~~~text
recording only the calls whose line gives a working directory in it.
~~~~

### Entry

Old:

~~~~text
Outside the repository that holds the project directory, it starts a git command that can start a program that a repository's own configuration names, as staging, a take-back and a put-back can, only where a git command of its input runs, or to take back a ledger file that its own session staged there, and leaves any other take-back or put-back to the first run that may make it, since git starts such a program, as it starts `core.fsmonitor` at a command that reads the index or the attributes, and `gpg.program` at `git log` and `git show` for a signed commit when `log.showSignature` is on (A21), and a session may never have run git in a clone that it only meets or moves into (T144).
~~~~

New:

~~~~text
Outside the repository that holds the project directory, it lets git start a program that a repository's own configuration names only as R197 gives it, since git starts such a program, as it starts `core.fsmonitor` at a command that reads the index or the attributes, and `gpg.program` at `git log` and `git show` for a signed commit when `log.showSignature` is on (A21), and a session may never have run git in a clone that it only meets or moves into (T144).
~~~~

Clause, the new unit:

~~~~text
Outside the repository that holds the project directory,
~~~~

Clause, R197:

~~~~text
it starts a git command that can start a program that a repository's own configuration names, as staging, a take-back and a put-back can, only where a git command of its input runs, or to take back a ledger file that its own session staged there, and leaves any other take-back or put-back to the first run that may make it,
~~~~

Clause, the new unit:

~~~~text
since git starts such a program, as it starts `core.fsmonitor` at a command that reads the index or the attributes, and `gpg.program` at `git log` and `git show` for a signed commit when `log.showSignature` is on (A21), and a session may never have run git in a clone that it only meets or moves into (T144).
~~~~

### Entry

Old:

~~~~text
A repository deeper inside the project directory is met only once Claude's directory or a git command is in it, so that a run never walks a folder tree of unknown size within its time budget.
~~~~

New:

~~~~text
A repository deeper inside the project directory is met as R180 gives it, so that a run never walks a folder tree of unknown size within its time budget.
~~~~

Clause, the new unit:

~~~~text
A repository deeper inside the project directory is met
~~~~

Clause, `usage-capture`: "A repository deeper inside the project directory is not met at the start":

~~~~text
only once Claude's directory or a git command is in it,
~~~~

Clause, the new unit:

~~~~text
so that a run never walks a folder tree of unknown size within its time budget.
~~~~

### Entry

Old:

~~~~text
Both copies work through the same store of each repository, under its lock, so that a call is recorded once by its message id, and a run before a command for which another run has staged a ledger file stages nothing more.
~~~~

New:

~~~~text
Both copies work through the same store of each repository, under its lock, as R181 gives it.
~~~~

Clause, the new unit:

~~~~text
Both copies work through the same store of each repository, under its lock,
~~~~

Clause, R181:

~~~~text
so that a call is recorded once by its message id, and a run before a command for which another run has staged a ledger file stages nothing more.
~~~~

### Entry

Old:

~~~~text
A run that finds the store at a version that it does not know leaves it, and the session's calls there, to the copy whose release wrote it, and a run of an earlier release than the latest that has run in its session leaves that session to the later copy, but for an opt-out, which it acts on, as decision 1 says (DR-206).
~~~~

New:

~~~~text
A run that finds the store at a version that it does not know leaves it, and the session's calls there, to the copy whose release wrote it (R55), and an earlier release leaves a session to a later copy as R191 gives it, as decision 1 says (DR-206).
~~~~

Clause, the new unit:

~~~~text
A run that finds the store at a version that it does not know leaves it, and the session's calls there, to the copy whose release wrote it
~~~~

Clause, R191:

~~~~text
and a run of an earlier release than the latest that has run in its session leaves that session to the later copy, but for an opt-out, which it acts on,
~~~~

Clause, the new unit:

~~~~text
as decision 1 says (DR-206).
~~~~

### Entry

Old:

~~~~text
Each of its files that can hold a comment opens with one that says it is the walking skeleton and not the tool or a release, its plugin's manifest says so in its description, and while the folder exists the README's status names it as such (R242).
~~~~

New:

~~~~text
It says what it is, as R242 gives it.
~~~~

Clause, R242:

~~~~text
Each of its files that can hold a comment opens with one that says it is the walking skeleton and not the tool or a release, its plugin's manifest says so in its description, and while the folder exists the README's status names it as such (R242).
~~~~

### Entry

Old:

~~~~text
Nothing here registers it: no tracked file under `.claude/`, `.claude-plugin/` or `.github/` holds the word `skeleton` (R234).
~~~~

New:

~~~~text
Nothing here registers it (R234).
~~~~

Clause, the new unit:

~~~~text
Nothing here registers it
~~~~

Clause, R234:

~~~~text
no tracked file under `.claude/`, `.claude-plugin/` or `.github/` holds the word `skeleton` (R234).
~~~~

### Entry

Old:

~~~~text
A capture script, one file that imports only Python's standard library, run by the plugin's hooks at `Stop`, `SubagentStop` and `SessionEnd`, and at `PreToolUse`, `PostToolUse` and `PostToolUseFailure` for every Bash command, with no `if` condition, the script itself going on only when the command's text holds the word `git`, through a command that runs it with `python3 -I` and ends in `; exit 0`, and which prints nothing on standard output (R239).
~~~~

New:

~~~~text
A capture script, one file that imports only Python's standard library, run by the plugin's hooks at `Stop`, `SubagentStop` and `SessionEnd`, and at `PreToolUse`, `PostToolUse` and `PostToolUseFailure` for every Bash command, with no `if` condition, the script itself going on only when the command's text holds the word `git`, and run as R239 gives it.
~~~~

Clause, the new unit:

~~~~text
A capture script, one file that imports only Python's standard library, run by the plugin's hooks at `Stop`, `SubagentStop` and `SessionEnd`, and at `PreToolUse`, `PostToolUse` and `PostToolUseFailure` for every Bash command, with no `if` condition, the script itself going on only when the command's text holds the word `git`,
~~~~

Clause, R239:

~~~~text
through a command that runs it with `python3 -I` and ends in `; exit 0`, and which prints nothing on standard output (R239).
~~~~

### Entry

Old:

~~~~text
In each, it does nothing unless the repository's `.pr-cost.json` holds `enabled` and `walking_skeleton` both set to `true`, so that the tool's own switch never turns the skeleton on and the skeleton's never turns the tool on, and git gives the skeleton's own opt-in, `pr-cost-skeleton.capture`, as `true` from the person's global configuration files alone, read without the session's git variables, which a repository's own settings can set, or `XDG_CONFIG_HOME`, should they reach it too (A5), so that the tool's opt-in, which an environment may already hold, never turns the skeleton on either, and a repository never turns it on for someone (R235).
~~~~

New:

~~~~text
In each, it records only as R235 gives it, so that the tool's own switch never turns the skeleton on and the skeleton's never turns the tool on, the session's git variables being ones which a repository's own settings can set, should they reach it too (A5), so that the tool's opt-in, which an environment may already hold, never turns the skeleton on either, and a repository never turns it on for someone.
~~~~

Clause, the new unit:

~~~~text
In each,
~~~~

Clause, R235:

~~~~text
it does nothing unless the repository's `.pr-cost.json` holds `enabled` and `walking_skeleton` both set to `true`,
~~~~

Clause, the new unit:

~~~~text
so that the tool's own switch never turns the skeleton on and the skeleton's never turns the tool on,
~~~~

Clause, R235:

~~~~text
and git gives the skeleton's own opt-in, `pr-cost-skeleton.capture`, as `true` from the person's global configuration files alone, read without the session's git variables,
~~~~

Clause, the new unit:

~~~~text
which a repository's own settings can set,
~~~~

Clause, R235:

~~~~text
or `XDG_CONFIG_HOME`,
~~~~

Clause, the new unit:

~~~~text
should they reach it too (A5),
~~~~

Clause, the new unit:

~~~~text
so that the tool's opt-in, which an environment may already hold, never turns the skeleton on either, and a repository never turns it on for someone
~~~~

Clause, R235:

~~~~text
(R235).
~~~~

### Entry

Old:

~~~~text
Before a command that it recognises as a commit, it writes the calls waiting into one new file, `.pr-cost/ledger/<YYYY-MM>/<random>.jsonl`, and stages it, unless the commit would commit nothing without it; after a command that did not commit the file, it removes the file from the index and the working tree, and its calls wait for a later commit (R240, DR-249).
~~~~

New:

~~~~text
Before a command that it recognises as a commit, it writes the calls waiting into one new file, `.pr-cost/ledger/<YYYY-MM>/<random>.jsonl`, and stages and takes back that file as R240 gives it (DR-249).
~~~~

Clause, the new unit:

~~~~text
Before a command that it recognises as a commit, it writes the calls waiting into one new file, `.pr-cost/ledger/<YYYY-MM>/<random>.jsonl`, and stages
~~~~

Clause, R240:

~~~~text
it, unless the commit would commit nothing without it; after a command that did not commit the file, it removes the file from the index and the working tree, and its calls wait for a later commit (R240,
~~~~

Clause, the new unit:

~~~~text
DR-249).
~~~~

### Entry

Old:

~~~~text
A command is recognised when its parts, joined by two ampersands, are each `cd` to a written path or `git add` with written paths, and last a `git commit` whose options are only `-m` with a quoted message, which may repeat, `-a` or `-q`, in the repository of each `git add` before it, each git command with at most one `-C` written path.
~~~~

Clause, R240:

~~~~text
A command is recognised when its parts, joined by two ampersands, are each `cd` to a written path or `git add` with written paths, and last a `git commit` whose options are only `-m` with a quoted message, which may repeat, `-a` or `-q`, in the repository of each `git add` before it, each git command with at most one `-C` written path.
~~~~

### Entry

Old:

~~~~text
A report script, run by a workflow on the push that a merge makes to `main`, which compares the push's `before` and `after` commits, fetched by their SHA, and, only when GitHub's API gives exactly one merged pull request for `after` and `before` is not all zeros, reads the ledger files that the push added, following no link and taking as a count only a whole number from zero to below a bound, counts each call's key once, sums each model's tokens, prices them at a fixed test price that `skeleton/` holds and names as one, and writes the figure, saying that it is at a test price and not a real cost, to the job summary and as one comment; otherwise it posts no comment and says why in the job summary (R241, DR-246).
~~~~

New:

~~~~text
A report script, run by a workflow on the push that a merge makes to `main`, which compares the push's `before` and `after` commits, fetched by their SHA, reads the ledger files that the push added, following no link and taking as a count only a whole number from zero to below a bound, and counts, prices and posts as R241 gives it (DR-246).
~~~~

Clause, the new unit:

~~~~text
A report script, run by a workflow on the push that a merge makes to `main`, which compares the push's `before` and `after` commits, fetched by their SHA
~~~~

Clause, R241:

~~~~text
and, only when GitHub's API gives exactly one merged pull request for `after` and `before` is not all zeros,
~~~~

Clause, the new unit:

~~~~text
reads the ledger files that the push added, following no link and taking as a count only a whole number from zero to below a bound
~~~~

Clause, R241:

~~~~text
counts each call's key once, sums each model's tokens, prices them at a fixed test price that `skeleton/` holds and names as one, and writes the figure, saying that it is at a test price and not a real cost, to the job summary and as one comment; otherwise it posts no comment and says why in the job summary (R241,
~~~~

Clause, the new unit:

~~~~text
DR-246).
~~~~

### Entry

Old:

~~~~text
The plugin's manifest and hooks, as `pr-cost-skeleton`, whose manifest holds only its name, a version and a description and whose hooks are all command hooks, and a script that builds its zip of the manifest, the hooks and the capture script, stored without compression, from git's objects of a full commit id that it prints beside the zip's SHA-256, the same bytes each time and on each machine (R243, DR-248).
~~~~

New:

~~~~text
The plugin's manifest and hooks, as `pr-cost-skeleton`, and a script that builds its zip, stored without compression, from git's objects of a full commit id that it prints beside the zip's SHA-256, as R243 gives them (DR-248).
~~~~

Clause, the new unit:

~~~~text
The plugin's manifest and hooks, as `pr-cost-skeleton`
~~~~

Clause, R243:

~~~~text
whose manifest holds only its name, a version and a description and whose hooks are all command hooks,
~~~~

Clause, the new unit:

~~~~text
and a script that builds its zip
~~~~

Clause, R243:

~~~~text
of the manifest, the hooks and the capture script,
~~~~

Clause, the new unit:

~~~~text
stored without compression, from git's objects of a full commit id that it prints beside the zip's SHA-256
~~~~

Clause, R243:

~~~~text
the same bytes each time and on each machine (R243,
~~~~

Clause, the new unit:

~~~~text
DR-248).
~~~~

### Entry

Old:

~~~~text
A workflow for the scratch repository, `skeleton/workflow.yml`, which runs only on a push to `main`, asks only to read contents and to write pull requests, uses no action but `actions/checkout`, pinned to a full commit and keeping no credentials, fetches only the push's two commits, reads no secret, puts no expression inside a command and sets a time limit, and which sits outside `.github/workflows/` so that it never runs here (R237).
~~~~

New:

~~~~text
A workflow for the scratch repository, `skeleton/workflow.yml`, which can do no more than R237 lets it, and which sits outside `.github/workflows/` so that it never runs here.
~~~~

Clause, the new unit:

~~~~text
A workflow for the scratch repository, `skeleton/workflow.yml`
~~~~

Clause, R237:

~~~~text
which runs only on a push to `main`, asks only to read contents and to write pull requests, uses no action but `actions/checkout`, pinned to a full commit and keeping no credentials, fetches only the push's two commits, reads no secret, puts no expression inside a command and sets a time limit,
~~~~

Clause, the new unit:

~~~~text
and which sits outside `.github/workflows/` so that it never runs here
~~~~

Clause, R237:

~~~~text
(R237).
~~~~

### Entry

Old:

~~~~text
- [Claude Code changes its transcript format] → The parser keeps to the fields it needs, refuses unknown shapes with a count instead of guessing, and its fixtures carry every shape seen in each kind of transcript, so a change shows up as a failing test. A call whose two final lines disagree, or whose usage block gives a cache-write split that disagrees with its total, is refused. A usage field that the parser does not know is not a reason to refuse the call, whose known fields still price it, but the ledger counts such calls, and when there are any, the comment gives their number and says that the token cost may be low, because the new field can carry a charge that the entry leaves out.
~~~~

New:

~~~~text
- [Claude Code changes its transcript format] → The parser keeps to the fields it needs, refuses unknown shapes with a count instead of guessing, and its fixtures carry every shape seen in each kind of transcript, so a change shows up as a failing test. A call whose two final lines disagree, or whose usage block gives a cache-write split that disagrees with its total, is refused. A call with a usage field that the parser does not know is recorded and counted as R43 and R95 give it, because the new field can carry a charge that the entry leaves out.
~~~~

Clause, the new unit:

~~~~text
- [Claude Code changes its transcript format] → The parser keeps to the fields it needs, refuses unknown shapes with a count instead of guessing, and its fixtures carry every shape seen in each kind of transcript, so a change shows up as a failing test. A call whose two final lines disagree, or whose usage block gives a cache-write split that disagrees with its total, is refused.
~~~~

Clause, R43:

~~~~text
A usage field that the parser does not know is not a reason to refuse the call, whose known fields still price it, but the ledger counts such calls,
~~~~

Clause, R95:

~~~~text
and when there are any, the comment gives their number and says that the token cost may be low,
~~~~

Clause, the new unit:

~~~~text
because the new field can carry a charge that the entry leaves out.
~~~~

### Entry

Old:

~~~~text
- [A call read without a stop reason gives the usage of its start, not of its end] → Its output tokens and server-side tool requests are too low. The ledger counts such calls, and when there are any, the comment gives their number and says that the token cost is a lower bound.
~~~~

New:

~~~~text
- [A call read without a stop reason gives the usage of its start, not of its end] → Its output tokens and server-side tool requests are too low, and such calls are counted as R42 and R95 give it.
~~~~

Clause, the new unit:

~~~~text
- [A call read without a stop reason gives the usage of its start, not of its end] → Its output tokens and server-side tool requests are too low
~~~~

Clause, R42:

~~~~text
The ledger counts such calls,
~~~~

Clause, R95:

~~~~text
and when there are any, the comment gives their number and says that the token cost is a lower bound.
~~~~

### Entry

Old:

~~~~text
- [A workflow runs a script or a local action that a pull request changes] → The comment flags changes to workflow files, to `.pr-cost.json`, to the hook file and to `.claude/settings.json` and `.claude/settings.local.json`, which can register it (DR-186), not to the files that workflows run, which can also act with the identity that posts the report comment. Those changes are in the pull request's diff for review.
~~~~

New:

~~~~text
- [A workflow runs a script or a local action that a pull request changes] → The comment flags changes as R93 gives it (DR-186), not to the files that workflows run, which can also act with the identity that posts the report comment. Those changes are in the pull request's diff for review.
~~~~

Clause, the new unit:

~~~~text
- [A workflow runs a script or a local action that a pull request changes] → The comment flags changes
~~~~

Clause, R93:

~~~~text
to workflow files, to `.pr-cost.json`, to the hook file and to `.claude/settings.json` and `.claude/settings.local.json`, which can register it
~~~~

Clause, the new unit:

~~~~text
(DR-186), not to the files that workflows run, which can also act with the identity that posts the report comment. Those changes are in the pull request's diff for review.
~~~~

### Entry

Old:

~~~~text
- [An adopter updates the hook and the workflow pin at different times] → Their price tables then differ. An older hook records a model that only the newer table lists as `unknown`, which the report counts in tokens and leaves out of the cost. An older report refuses a ledger line with a name its table does not list, and counts it as refused. Either way the comment shows that something was not priced, and nothing is guessed. Whenever the hook file in the merged commit is not the one at the report's commit, the comment also says that the repository's hook does not come from the report's commit, quoting nothing from the file, and the README tells adopters to update both in one pull request.
~~~~

New:

~~~~text
- [An adopter updates the hook and the workflow pin at different times] → Their price tables then differ. An older hook records a model that only the newer table lists as `unknown`, which the report counts in tokens and leaves out of the cost. An older report refuses a ledger line with a name its table does not list, and counts it as refused. Either way the comment shows that something was not priced, and nothing is guessed. The comment also names a hook file that does not come from the report's commit (R65), and the README tells adopters to update both in one pull request.
~~~~

Clause, the new unit:

~~~~text
- [An adopter updates the hook and the workflow pin at different times] → Their price tables then differ. An older hook records a model that only the newer table lists as `unknown`, which the report counts in tokens and leaves out of the cost. An older report refuses a ledger line with a name its table does not list, and counts it as refused. Either way the comment shows that something was not priced, and nothing is guessed.
~~~~

Clause, R65:

~~~~text
Whenever the hook file in the merged commit is not the one at the report's commit, the comment also says that the repository's hook does not come from the report's commit, quoting nothing from the file,
~~~~

Clause, the new unit:

~~~~text
and the README tells adopters to update both in one pull request.
~~~~

### Entry

Old:

~~~~text
- [Prices go stale, or a new model appears] → Every report names the price table's date, and an unpriced model or attribute is named rather than guessed. A model the hook's copy of the price table does not list is recorded as `unknown` until the adopter updates the hook.
~~~~

New:

~~~~text
- [Prices go stale, or a new model appears] → The report names the price table's date and never guesses a price (R14, R17, R61). A model the hook's copy of the price table does not list is recorded as `unknown` until the adopter updates the hook.
~~~~

Clause, the new unit:

~~~~text
- [Prices go stale, or a new model appears] →
~~~~

Clause, R14:

~~~~text
Every report names the price table's date,
~~~~

Clause, R17:

~~~~text
and an unpriced model
~~~~

Clause, R61:

~~~~text
or attribute is named rather than guessed.
~~~~

Clause, the new unit:

~~~~text
A model the hook's copy of the price table does not list is recorded as `unknown` until the adopter updates the hook.
~~~~

### Entry

Old:

~~~~text
- [A pull request's commits and runs use up the report's call budget, or the requests per hour that `GITHUB_TOKEN` can make in the repository] → The report keeps to its call budget, so that one report cannot use up a limit that the repository's other workflows share. When the budget runs out while it reads runs and jobs, the comment marks the CI cost as incomplete, and when it runs out before the report can tell which pull request the push merged, no comment is posted and the job summary says why.
~~~~

New:

~~~~text
- [A pull request's commits and runs use up the report's call budget, or the requests per hour that `GITHUB_TOKEN` can make in the repository] → The report keeps to its call budget, so that one report cannot use up a limit that the repository's other workflows share, and says what the budget left unread as R64 and R70 give it.
~~~~

Clause, the new unit:

~~~~text
- [A pull request's commits and runs use up the report's call budget, or the requests per hour that `GITHUB_TOKEN` can make in the repository] → The report keeps to its call budget, so that one report cannot use up a limit that the repository's other workflows share
~~~~

Clause, `ci-minutes`: "A pull request with more commits than the call budget allows is marked incomplete":

~~~~text
When the budget runs out while it reads runs and jobs, the comment marks the CI cost as incomplete,
~~~~

Clause, R70:

~~~~text
and when it runs out before the report can tell which pull request the push merged, no comment is posted and the job summary says why.
~~~~

### Entry

Old:

~~~~text
- [A person's plugin is of another release than the report that a repository pins] → A later plugin can write a model name or a ledger format that the pinned report does not know, which the report refuses, and the comment says that some ledger files come from a later release than the report (DR-208); an earlier plugin leaves a session to a later copy that runs beside it, and records nothing in a repository whose configuration holds a key that it does not know. The README says that a repository keeps its pin current and a person keeps their plugin current.
~~~~

New:

~~~~text
- [A person's plugin is of another release than the report that a repository pins] → A later plugin can write a model name or a ledger format that the pinned report does not know, which the report refuses, and the comment says so (R193, DR-208); an earlier plugin leaves a session to a later copy that runs beside it, and records nothing in a repository whose configuration holds a key that it does not know. The README says that a repository keeps its pin current and a person keeps their plugin current.
~~~~

Clause, the new unit:

~~~~text
- [A person's plugin is of another release than the report that a repository pins] → A later plugin can write a model name or a ledger format that the pinned report does not know, which the report refuses, and the comment says
~~~~

Clause, R193:

~~~~text
that some ledger files come from a later release than the report
~~~~

Clause, the new unit:

~~~~text
DR-208); an earlier plugin leaves a session to a later copy that runs beside it, and records nothing in a repository whose configuration holds a key that it does not know. The README says that a repository keeps its pin current and a person keeps their plugin current.
~~~~

### Entry

Old:

~~~~text
- [The glossary, an assumption or a page that one links to reads as an instruction to an agent] → They describe, and never instruct; where the glossary or an assumption differs from a requirement, a scenario or `CLAUDE.md`, those hold, and `CLAUDE.md` says so (DR-238). A documented fact links only a vendor's page on a listed host or a file at a full commit of a listed repository, and a page of the assumptions gives no other web address.
~~~~

New:

~~~~text
- [The glossary, an assumption or a page that one links to reads as an instruction to an agent] → They describe, and never instruct; where the glossary or an assumption differs from a requirement, a scenario or `CLAUDE.md`, those hold, and `CLAUDE.md` says so (DR-238). A documented fact and a page of the assumptions link only as R140 and R143 give it.
~~~~

Clause, the new unit:

~~~~text
- [The glossary, an assumption or a page that one links to reads as an instruction to an agent] → They describe, and never instruct; where the glossary or an assumption differs from a requirement, a scenario or `CLAUDE.md`, those hold, and `CLAUDE.md` says so (DR-238).
~~~~

Clause, R140:

~~~~text
A documented fact links only a vendor's page on a listed host or a file at a full commit of a listed repository,
~~~~

Clause, R143:

~~~~text
and a page of the assumptions gives no other web address.
~~~~

## `docs/how-it-works.md`

### Entry

Old:

~~~~text
Where the transcript gave no cache lifetime, the cost is a range between the two lifetimes' rates.
~~~~

New:

~~~~text
Where the transcript gave no cache lifetime, the cost is a range between the two lifetimes' rates (R15).
~~~~

Clause, the new unit:

~~~~text
Where the transcript gave no cache lifetime, the cost is a range between the two lifetimes' rates
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
An entry whose model, attribute or day has no price is counted in tokens and left out of the cost, and the comment names it.
~~~~

New:

~~~~text
An entry whose model, attribute or day has no price is counted in tokens and left out of the cost, and the comment names it (R14, R17, R61).
~~~~

Clause, the new unit:

~~~~text
An entry whose model, attribute or day has no price is counted in tokens and left out of the cost, and the comment names it
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
The runs counted are those on the pull request's own commits that no push to the default branch started and that were created before the merge.
~~~~

New:

~~~~text
The runs counted are those on the pull request's own commits that no push to the default branch started and that were created before the merge (R62, R120).
~~~~

Clause, the new unit:

~~~~text
The runs counted are those on the pull request's own commits that no push to the default branch started and that were created before the merge
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
A job on a runner that `prices/github-actions.json` does not list is counted in minutes and left out of the cost.
~~~~

New:

~~~~text
A job on a runner that `prices/github-actions.json` does not list is counted in minutes and left out of the cost (R63).
~~~~

Clause, the new unit:

~~~~text
A job on a runner that `prices/github-actions.json` does not list is counted in minutes and left out of the cost
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
`rate` is the latest row in `prices/models.json` dated on or before *d*, with every modifier that the table lists for the entry's attributes, combined as the table states: long-prompt rates, where a prompt's length is its input, cache-write and cache-read tokens together; the inference region's multiplier; and the rates for speed and service tier.
~~~~

New:

~~~~text
`rate` is the latest row in `prices/models.json` dated on or before *d*, with every modifier that the table lists for the entry's attributes, combined as the table states (R14, R16).
~~~~

Clause, the new unit:

~~~~text
`rate` is the latest row in `prices/models.json` dated on or before *d*, with every modifier that the table lists for the entry's attributes, combined as the table states
~~~~

Clause, `pricing`: "A long prompt is priced at its higher rates":

~~~~text
: long-prompt rates, where a prompt's length is its input, cache-write and cache-read tokens together;
~~~~

Clause, `pricing`: "A region multiplier applies to every token type":

~~~~text
the inference region's multiplier;
~~~~

Clause, R16:

~~~~text
and the rates for speed and service tier
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Ledger files: a first line that states the ledger format's version, the release of the capture step that wrote it, the count of refused calls and three flags for calls left out, for consent, for their age or because their repository could not be told, with no count; then one entry per call: UTC day, model, a SHA-256 hash of the message id in a field whose name ends in `_id`, main agent or subagent, the token counts, the price attributes, the activity type, and marks for a call read without a stop reason or with a usage field that capture does not know.
~~~~

New:

~~~~text
- Ledger files: a first line that states the ledger format's version, the release of the capture step that wrote it, the count of refused calls and three flags for calls left out, for consent, for their age or because their repository could not be told, with no count; then one entry per call: UTC day, model, a SHA-256 hash of the message id in a field whose name ends in `_id`, main agent or subagent, the token counts, the price attributes, the activity type, and marks for a call read without a stop reason or with a usage field that capture does not know (R2, R4, R6, R42, R43, R155, R156).
~~~~

Clause, the new unit:

~~~~text
- Ledger files: a first line that states the ledger format's version, the release of the capture step that wrote it, the count of refused calls and three flags for calls left out, for consent, for their age or because their repository could not be told, with no count; then one entry per call: UTC day, model, a SHA-256 hash of the message id in a field whose name ends in `_id`, main agent or subagent, the token counts, the price attributes, the activity type, and marks for a call read without a stop reason or with a usage field that capture does not know
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
It reads the person's two global git configuration files for `pr-cost.capture`, and asks git for each value of it that git reads in the repository, which can only turn capture off.
~~~~

New:

~~~~text
It reads the person's two global git configuration files for `pr-cost.capture`, and asks git for each value of it that git reads in the repository, which can only turn capture off (R37, R160).
~~~~

Clause, the new unit:

~~~~text
It reads the person's two global git configuration files for `pr-cost.capture`, and asks git for each value of it that git reads in the repository, which can only turn capture off
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
It writes only its store inside the git common directory, a file of its own, in a folder of its own, that its owner alone can read and write, except on Windows, and the ledger file it stages, and touches the index only to stage, take back or put back that one file, which a run of the plugin does outside the repository that holds the project directory only before or after a git command of its session there, or to take back a file that its own session staged there.
~~~~

New:

~~~~text
It writes only its store inside the git common directory, a file of its own, in a folder of its own, that its owner alone can read and write, except on Windows, and the ledger file it stages, and touches the index only to stage, take back or put back that one file, which a run of the plugin does outside the repository that holds the project directory only before or after a git command of its session there, or to take back a file that its own session staged there (R47, R152, R56, R197).
~~~~

Clause, the new unit:

~~~~text
It writes only its store inside the git common directory, a file of its own, in a folder of its own, that its owner alone can read and write, except on Windows, and the ledger file it stages, and touches the index only to stage, take back or put back that one file, which a run of the plugin does outside the repository that holds the project directory only before or after a git command of its session there, or to take back a file that its own session staged there
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
**The report's workflow**, as an adopter calls it, uses the workflow's own `GITHUB_TOKEN` and no other secret.
~~~~

New:

~~~~text
**The report's workflow**, as an adopter calls it, uses the workflow's own `GITHUB_TOKEN` and no other secret (R24).
~~~~

Clause, the new unit:

~~~~text
**The report's workflow**, as an adopter calls it, uses the workflow's own `GITHUB_TOKEN` and no other secret
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
**The release workflow**, in this repository only, holds `contents: write` in its release job alone, to create the release as a draft, attach the bill of materials and the plugin's zip, read them back and then publish the release, and runs only for a pushed tag.
~~~~

New:

~~~~text
**The release workflow**, in this repository only, holds `contents: write` in its release job alone, to create the release as a draft, attach the bill of materials and the plugin's zip, read them back and then publish the release, and runs only for a pushed tag (R189).
~~~~

Clause, the new unit:

~~~~text
**The release workflow**, in this repository only, holds `contents: write` in its release job alone, to create the release as a draft, attach the bill of materials and the plugin's zip, read them back and then publish the release, and runs only for a pushed tag
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
| Capture step | Nothing | None | The hook opens no network connection. | None |
~~~~

New:

~~~~text
| Capture step | Nothing | None | The hook opens no network connection (R30). | None |
~~~~

Clause, the new unit:

~~~~text
| Capture step | Nothing | None | The hook opens no network connection
~~~~

Clause, the new unit:

~~~~text
. | None |
~~~~

### Entry

Old:

~~~~text
| Report | GitHub's REST API, at the host in `GITHUB_API_URL` (`api.github.com` on github.com) | HTTPS | Find the merged pull request, list its runs and jobs, post or update its comment | `GITHUB_TOKEN` |
~~~~

New:

~~~~text
| Report | GitHub's REST API, at the host in `GITHUB_API_URL` (`api.github.com` on github.com) | HTTPS | Find the merged pull request, list its runs and jobs, post or update its comment (R30) | `GITHUB_TOKEN` |
~~~~

Clause, the new unit:

~~~~text
| Report | GitHub's REST API, at the host in `GITHUB_API_URL` (`api.github.com` on github.com) | HTTPS | Find the merged pull request, list its runs and jobs, post or update its comment
~~~~

Clause, the new unit:

~~~~text
| `GITHUB_TOKEN` |
~~~~

### Entry

Old:

~~~~text
| Report | GitHub, by git, through `actions/checkout` and `git fetch` | HTTPS | Fetch the tool's own code at its commit, and the adopter's repository to read as data: the default branch's history up to the push's commit and the pull request's head as `refs/pull/<number>/head` | `GITHUB_TOKEN` |
~~~~

New:

~~~~text
| Report | GitHub, by git, through `actions/checkout` and `git fetch` | HTTPS | Fetch the tool's own code at its commit, and the adopter's repository to read as data: the default branch's history up to the push's commit and the pull request's head as `refs/pull/<number>/head` (R30) | `GITHUB_TOKEN` |
~~~~

Clause, the new unit:

~~~~text
| Report | GitHub, by git, through `actions/checkout` and `git fetch` | HTTPS | Fetch the tool's own code at its commit, and the adopter's repository to read as data: the default branch's history up to the push's commit and the pull request's head as `refs/pull/<number>/head`
~~~~

Clause, the new unit:

~~~~text
| `GITHUB_TOKEN` |
~~~~

### Entry

Old:

~~~~text
| Release workflow | GitHub's REST API | HTTPS | Create the release as a draft, upload the bill of materials and the plugin's zip, download each to check it, and publish the release | `GITHUB_TOKEN` |
~~~~

New:

~~~~text
| Release workflow | GitHub's REST API | HTTPS | Create the release as a draft, upload the bill of materials and the plugin's zip, download each to check it, and publish the release (R189) | `GITHUB_TOKEN` |
~~~~

Clause, the new unit:

~~~~text
| Release workflow | GitHub's REST API | HTTPS | Create the release as a draft, upload the bill of materials and the plugin's zip, download each to check it, and publish the release
~~~~

Clause, the new unit:

~~~~text
| `GITHUB_TOKEN` |
~~~~

### Entry

Old:

~~~~text
Prices are never fetched: the price table is a file at the tool's commit, changed only by a pull request.
~~~~

New:

~~~~text
Prices are never fetched: the price table is a file at the tool's commit, changed only by a pull request (R30).
~~~~

Clause, the new unit:

~~~~text
Prices are never fetched: the price table is a file at the tool's commit, changed only by a pull request
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
It sets `GIT_NO_LAZY_FETCH=1` and `GIT_TERMINAL_PROMPT=0` for every git command it runs, so that git fetches nothing and asks for no credentials.
~~~~

New:

~~~~text
It sets `GIT_NO_LAZY_FETCH=1` and `GIT_TERMINAL_PROMPT=0` for every git command it runs, so that git fetches nothing and asks for no credentials (R111).
~~~~

Clause, the new unit:

~~~~text
It sets `GIT_NO_LAZY_FETCH=1` and `GIT_TERMINAL_PROMPT=0` for every git command it runs, so that git fetches nothing and asks for no credentials
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
Its own reading of the opt-in ignores the variables that point git at other configuration files or add settings.
~~~~

New:

~~~~text
Its own reading of the opt-in ignores the variables that point git at other configuration files or add settings (R37).
~~~~

Clause, the new unit:

~~~~text
Its own reading of the opt-in ignores the variables that point git at other configuration files or add settings
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
Every git command that it starts runs without `PWD`, so that git matches a condition on a repository's folder against its real path, and without the session's variables whose names begin with `GIT_`, but those that it sets itself, so that they choose neither the repository, its index nor the files that git reads its settings from, save for one of the two git commands that ask for each value of the opt-in key, which runs in the session's own environment, its `PWD` included, where those variables and `PWD` can only turn capture off, and which the hook stops at its time budget, taking capture to be off, when a file that they name holds it up.
~~~~

New:

~~~~text
Every git command that it starts runs without `PWD`, so that git matches a condition on a repository's folder against its real path, and without the session's variables whose names begin with `GIT_`, but those that it sets itself, so that they choose neither the repository, its index nor the files that git reads its settings from, save for one of the two git commands that ask for each value of the opt-in key, which runs in the session's own environment, its `PWD` included, where those variables and `PWD` can only turn capture off, and which the hook stops at its time budget, taking capture to be off, when a file that they name holds it up (R169, R160).
~~~~

Clause, the new unit:

~~~~text
Every git command that it starts runs without `PWD`, so that git matches a condition on a repository's folder against its real path, and without the session's variables whose names begin with `GIT_`, but those that it sets itself, so that they choose neither the repository, its index nor the files that git reads its settings from, save for one of the two git commands that ask for each value of the opt-in key, which runs in the session's own environment, its `PWD` included, where those variables and `PWD` can only turn capture off, and which the hook stops at its time budget, taking capture to be off, when a file that they name holds it up
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Put a prompt, a response, code, a file's contents, a tool's name, input or output, a path, a working directory, a branch name, a user name, a session identifier, a transcript's path, a `tool_use_id` or a time of day, or a hash of any of them, in a ledger file or in anything it publishes. For its own use, the person's store in the git common directory of their clone keeps, for no longer than 30 days, the worktree and branch that each waiting call goes to, a session's id, a transcript's path, a `tool_use_id` and the fingerprint of the files that hold the opt-in, each as a hash, and, only until a run resolves a staged or taken-back ledger file, that file's path and its worktree's name, and for a staged one its transcript's path, which carries the session's id, and nothing in the store leaves that directory.
~~~~

New:

~~~~text
- Put a prompt, a response, code, a file's contents, a tool's name, input or output, a path, a working directory, a branch name, a user name, a session identifier, a transcript's path, a `tool_use_id` or a time of day, or a hash of any of them, in a ledger file or in anything it publishes. For its own use, the person's store in the git common directory of their clone keeps, for no longer than 30 days, the worktree and branch that each waiting call goes to, a session's id, a transcript's path, a `tool_use_id` and the fingerprint of the files that hold the opt-in, each as a hash, and, only until a run resolves a staged or taken-back ledger file, that file's path and its worktree's name, and for a staged one its transcript's path, which carries the session's id, and nothing in the store leaves that directory (R4, R47, R149, R150, R170).
~~~~

Clause, the new unit:

~~~~text
- Put a prompt, a response, code, a file's contents, a tool's name, input or output, a path, a working directory, a branch name, a user name, a session identifier, a transcript's path, a `tool_use_id` or a time of day, or a hash of any of them, in a ledger file or in anything it publishes. For its own use, the person's store in the git common directory of their clone keeps, for no longer than 30 days, the worktree and branch that each waiting call goes to, a session's id, a transcript's path, a `tool_use_id` and the fingerprint of the files that hold the opt-in, each as a hash, and, only until a run resolves a staged or taken-back ledger file, that file's path and its worktree's name, and for a staged one its transcript's path, which carries the session's id, and nothing in the store leaves that directory
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Record the usage of anyone whose opt-in is not on, as they set it themselves, or as the cloud environment that they use or their organization's managed settings set it for them, or a call that it cannot show was made while both switches were on. The plugin, however it came to a session, opts no one in. A run that finds a switch off creates no store and adds nothing of its session to one, so someone who has never opted in leaves nothing in the git common directory, and an opt-out empties the store of everything but what a take-back or a put-back still needs, at a run of a release that knows the store's version.
~~~~

New:

~~~~text
- Record the usage of anyone whose opt-in is not on, as they set it themselves, or as the cloud environment that they use or their organization's managed settings set it for them, or a call that it cannot show was made while both switches were on. The plugin, however it came to a session, opts no one in. A run that finds a switch off creates no store and adds nothing of its session to one, so someone who has never opted in leaves nothing in the git common directory, and an opt-out empties the store of everything but what a take-back or a put-back still needs, at a run of a release that knows the store's version (R1, R40, R109, R145, R182).
~~~~

Clause, the new unit:

~~~~text
- Record the usage of anyone whose opt-in is not on, as they set it themselves, or as the cloud environment that they use or their organization's managed settings set it for them, or a call that it cannot show was made while both switches were on. The plugin, however it came to a session, opts no one in. A run that finds a switch off creates no store and adds nothing of its session to one, so someone who has never opted in leaves nothing in the git common directory, and an opt-out empties the store of everything but what a take-back or a put-back still needs, at a run of a release that knows the store's version
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Keep a copy of a transcript, or of any line of one, in any file.
~~~~

New:

~~~~text
- Keep a copy of a transcript, or of any line of one, in any file (R154).
~~~~

Clause, the new unit:

~~~~text
- Keep a copy of a transcript, or of any line of one, in any file
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Look for repositories below a session's project directory deeper than directly inside it: a run of the plugin meets a repository only through the project directory, Claude's current directory or a git command run there.
~~~~

New:

~~~~text
- Look for repositories below a session's project directory deeper than directly inside it: a run of the plugin meets a repository only through the project directory, Claude's current directory or a git command run there (R180).
~~~~

Clause, the new unit:

~~~~text
- Look for repositories below a session's project directory deeper than directly inside it: a run of the plugin meets a repository only through the project directory, Claude's current directory or a git command run there
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Start a git command that can start a program that a repository's own configuration names, such as `core.fsmonitor` or `gpg.program`, in a repository that a run of the plugin only meets or moves into, outside the one that holds the project directory: it starts one there only before or after a git command of the session there, or to take back a file that the session staged there.
~~~~

New:

~~~~text
- Start a git command that can start a program that a repository's own configuration names, such as `core.fsmonitor` or `gpg.program`, in a repository that a run of the plugin only meets or moves into, outside the one that holds the project directory: it starts one there only before or after a git command of the session there, or to take back a file that the session staged there (R197).
~~~~

Clause, the new unit:

~~~~text
- Start a git command that can start a program that a repository's own configuration names, such as `core.fsmonitor` or `gpg.program`, in a repository that a run of the plugin only meets or moves into, outside the one that holds the project directory: it starts one there only before or after a git command of the session there, or to take back a file that the session staged there
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Unpublish what was pushed. An opt-out, a removed ledger file or a removed store leaves each pushed ledger file in its branch's history, in every clone and fork that holds it, and in the comments already posted.
~~~~

New:

~~~~text
- Unpublish what was pushed. An opt-out, a removed ledger file or a removed store leaves each pushed ledger file in its branch's history, in every clone and fork that holds it, and in the comments already posted (R146).
~~~~

Clause, the new unit:

~~~~text
- Unpublish what was pushed. An opt-out, a removed ledger file or a removed store leaves each pushed ledger file in its branch's history, in every clone and fork that holds it, and in the comments already posted
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Send anything from the session's machine anywhere. The ledger leaves the machine only in the person's own commits, when they push.
~~~~

New:

~~~~text
- Send anything from the session's machine anywhere. The ledger leaves the machine only in the person's own commits, when they push (R30, R111).
~~~~

Clause, the new unit:

~~~~text
- Send anything from the session's machine anywhere. The ledger leaves the machine only in the person's own commits, when they push
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Run, import or install anything from the pull request it reports on.
~~~~

New:

~~~~text
- Run, import or install anything from the pull request it reports on (R24).
~~~~

Clause, the new unit:

~~~~text
- Run, import or install anything from the pull request it reports on
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Write to the repository, beyond the ledger file staged for the agent's own commit.
~~~~

New:

~~~~text
- Write to the repository, beyond the ledger file staged for the agent's own commit (R22, R56).
~~~~

Clause, the new unit:

~~~~text
- Write to the repository, beyond the ledger file staged for the agent's own commit
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- Fetch prices, or contact any service other than GitHub.
~~~~

New:

~~~~text
- Fetch prices, or contact any service other than GitHub (R30).
~~~~

Clause, the new unit:

~~~~text
- Fetch prices, or contact any service other than GitHub
~~~~

Clause, the new unit:

~~~~text
.
~~~~

## `README.md`

### Entry

Old:

~~~~text
- capture the tokens the agent spent while its session was working in the repository, per model and by type: input, output, cache writes and cache reads, and carry them to the pull request with the agent's own commits;
~~~~

New:

~~~~text
- capture the tokens the agent spent while its session was working in the repository, per model and by type: input, output, cache writes and cache reads, and carry them to the pull request with the agent's own commits (R2, R3, R7);
~~~~

Clause, the new unit:

~~~~text
- capture the tokens the agent spent while its session was working in the repository, per model and by type: input, output, cache writes and cache reads, and carry them to the pull request with the agent's own commits
~~~~

Clause, the new unit:

~~~~text
;
~~~~

### Entry

Old:

~~~~text
- price them from a dated price table kept in the tool's own repository, so the estimate uses the price that applied on the day the tokens were spent;
~~~~

New:

~~~~text
- price them from a dated price table kept in the tool's own repository, so the estimate uses the price that applied on the day the tokens were spent (R14, R15);
~~~~

Clause, the new unit:

~~~~text
- price them from a dated price table kept in the tool's own repository, so the estimate uses the price that applied on the day the tokens were spent
~~~~

Clause, the new unit:

~~~~text
;
~~~~

### Entry

Old:

~~~~text
- add the GitHub Actions minutes the pull request's CI used, priced at GitHub's published rate;
~~~~

New:

~~~~text
- add the GitHub Actions minutes the pull request's CI used, priced at GitHub's published rate (R18, R62);
~~~~

Clause, the new unit:

~~~~text
- add the GitHub Actions minutes the pull request's CI used, priced at GitHub's published rate
~~~~

Clause, the new unit:

~~~~text
;
~~~~

### Entry

Old:

~~~~text
- where the data allows, split the cost by activity: code generation, file reading, tooling, MCP calls, subagents and conversation, with any tool it does not know counted as other;
~~~~

New:

~~~~text
- where the data allows, split the cost by activity: code generation, file reading, tooling, MCP calls, subagents and conversation, with any tool it does not know counted as other (R6);
~~~~

Clause, the new unit:

~~~~text
- where the data allows, split the cost by activity: code generation, file reading, tooling, MCP calls, subagents and conversation, with any tool it does not know counted as other
~~~~

Clause, the new unit:

~~~~text
;
~~~~

### Entry

Old:

~~~~text
- post a short report comment when the pull request merges, and keep the ledger in the repository as the record;
~~~~

New:

~~~~text
- post a short report comment when the pull request merges, and keep the ledger in the repository as the record (R20, R22);
~~~~

Clause, the new unit:

~~~~text
- post a short report comment when the pull request merges, and keep the ledger in the repository as the record
~~~~

Clause, the new unit:

~~~~text
;
~~~~

### Entry

Old:

~~~~text
- record a project's cloud threads too, through a Claude Code plugin that a person adds from a release's zip or from this repository as a marketplace.
~~~~

New:

~~~~text
- record a project's cloud threads too, through a Claude Code plugin that a person adds from a release's zip or from this repository as a marketplace (R179, R183, R184).
~~~~

Clause, the new unit:

~~~~text
- record a project's cloud threads too, through a Claude Code plugin that a person adds from a release's zip or from this repository as a marketplace
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
A repository turns it on or off with one file, its configuration file, and each person's own opt-in, which they set themselves or which the cloud environment that they use sets, decides whether their own sessions are recorded.
~~~~

New:

~~~~text
A repository turns it on or off with one file, its configuration file, and each person's own opt-in, which they set themselves or which the cloud environment that they use sets, decides whether their own sessions are recorded (R19, R1).
~~~~

Clause, the new unit:

~~~~text
A repository turns it on or off with one file, its configuration file, and each person's own opt-in, which they set themselves or which the cloud environment that they use sets, decides whether their own sessions are recorded
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
Usage is recorded by the directory that Claude is in when it makes each call, not by which files it touches.
~~~~

New:

~~~~text
Usage is recorded by the directory that Claude is in when it makes each call, not by which files it touches (R3, R147).
~~~~

Clause, the new unit:

~~~~text
Usage is recorded by the directory that Claude is in when it makes each call, not by which files it touches
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
The figure is an **API-equivalent estimate**, meaning what the same tokens would cost at list prices.
~~~~

New:

~~~~text
The figure is an **API-equivalent estimate**, meaning what the same tokens would cost at list prices (R94).
~~~~

Clause, the new unit:

~~~~text
The figure is an **API-equivalent estimate**, meaning what the same tokens would cost at list prices
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
The tool runs on Python 3.11 and every later release, with the standard library only, so it fits into other projects without pulling anything in.
~~~~

New:

~~~~text
The tool runs on Python 3.11 and every later release, with the standard library only, so it fits into other projects without pulling anything in (R25).
~~~~

Clause, the new unit:

~~~~text
The tool runs on Python 3.11 and every later release, with the standard library only, so it fits into other projects without pulling anything in
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
Versions follow [Semantic Versioning](https://semver.org/), and each release on GitHub carries a CycloneDX software bill of materials and the plugin's zip, and names the commit to pin.
~~~~

New:

~~~~text
Versions follow [Semantic Versioning](https://semver.org/), and each release on GitHub carries a CycloneDX software bill of materials and the plugin's zip, and names the commit to pin (R27, R28, R71, R183).
~~~~

Clause, the new unit:

~~~~text
Versions follow [Semantic Versioning](https://semver.org/), and each release on GitHub carries a CycloneDX software bill of materials and the plugin's zip, and names the commit to pin
~~~~

Clause, the new unit:

~~~~text
.
~~~~

## `SECURITY.md`

### Entry

Old:

~~~~text
The tool supports Python 3.11 and every later release, and each release carries a CycloneDX software bill of materials, and the capture step as a Claude Code plugin in a zip whose SHA-256 the README at the release's commit gives.
~~~~

New:

~~~~text
The tool supports Python 3.11 and every later release, and each release carries a CycloneDX software bill of materials, and the capture step as a Claude Code plugin in a zip whose SHA-256 the README at the release's commit gives (R25, R28, R183).
~~~~

Clause, the new unit:

~~~~text
The tool supports Python 3.11 and every later release, and each release carries a CycloneDX software bill of materials, and the capture step as a Claude Code plugin in a zip whose SHA-256 the README at the release's commit gives
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
- it needs no secret beyond the `GITHUB_TOKEN` a workflow already has, with the narrowest permissions that work;
~~~~

New:

~~~~text
- it needs no secret beyond the `GITHUB_TOKEN` a workflow already has, with the narrowest permissions that work (R24);
~~~~

Clause, the new unit:

~~~~text
- it needs no secret beyond the `GITHUB_TOKEN` a workflow already has, with the narrowest permissions that work
~~~~

Clause, the new unit:

~~~~text
;
~~~~

### Entry

Old:

~~~~text
- the ledger entries it writes hold counts, the model, the price attributes, the UTC day, the activity type, whether the main agent or a subagent made the call, and a hash of the call's message id, and never prompts, code, tool names, transcript text or any session identifier, and each ledger file's first line holds only its format's version, the release of the capture step that wrote it, its count of refused calls and flags, with no count, for calls left out;
~~~~

New:

~~~~text
- the ledger entries it writes hold counts, the model, the price attributes, the UTC day, the activity type, whether the main agent or a subagent made the call, and a hash of the call's message id, and never prompts, code, tool names, transcript text or any session identifier, and each ledger file's first line holds only its format's version, the release of the capture step that wrote it, its count of refused calls and flags, with no count, for calls left out (R2, R4, R155, R156);
~~~~

Clause, the new unit:

~~~~text
- the ledger entries it writes hold counts, the model, the price attributes, the UTC day, the activity type, whether the main agent or a subagent made the call, and a hash of the call's message id, and never prompts, code, tool names, transcript text or any session identifier, and each ledger file's first line holds only its format's version, the release of the capture step that wrote it, its count of refused calls and flags, with no count, for calls left out
~~~~

Clause, the new unit:

~~~~text
;
~~~~

### Entry

Old:

~~~~text
- the notes that capture keeps for its own use never leave the git common directory of the person's clone, where its store is readable and writable by that person alone, except on Windows, keeps nothing past 30 days, holds a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` only as hashes, and holds plain names only for a staged or taken-back ledger file, until a run resolves it, a staged one's transcript path among them, which carries the session's id, and capture keeps no copy of a transcript;
~~~~

New:

~~~~text
- the notes that capture keeps for its own use never leave the git common directory of the person's clone, where its store is readable and writable by that person alone, except on Windows, keeps nothing past 30 days, holds a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` only as hashes, and holds plain names only for a staged or taken-back ledger file, until a run resolves it, a staged one's transcript path among them, which carries the session's id, and capture keeps no copy of a transcript (R47, R149, R150, R152, R154, R170);
~~~~

Clause, the new unit:

~~~~text
- the notes that capture keeps for its own use never leave the git common directory of the person's clone, where its store is readable and writable by that person alone, except on Windows, keeps nothing past 30 days, holds a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` only as hashes, and holds plain names only for a staged or taken-back ledger file, until a run resolves it, a staged one's transcript path among them, which carries the session's id, and capture keeps no copy of a transcript
~~~~

Clause, the new unit:

~~~~text
;
~~~~

### Entry

Old:

~~~~text
- it records a person's usage only when that person's opt-in is on, as they set it themselves, or as the cloud environment that they use or their organization's managed settings set it for them, and never because the plugin is there, only for calls made while both switches were on, and only for calls made while Claude's current directory is in the repository that publishes it, which includes work on other repositories from there, apart from a line too long to read, which a run of the plugin counts, as refused, in each repository that it works on;
~~~~

New:

~~~~text
- it records a person's usage only when that person's opt-in is on, as they set it themselves, or as the cloud environment that they use or their organization's managed settings set it for them, and never because the plugin is there, only for calls made while both switches were on, and only for calls made while Claude's current directory is in the repository that publishes it, which includes work on other repositories from there, apart from a line too long to read, which a run of the plugin counts, as refused, in each repository that it works on (R1, R3, R40, R44, R147, R182);
~~~~

Clause, the new unit:

~~~~text
- it records a person's usage only when that person's opt-in is on, as they set it themselves, or as the cloud environment that they use or their organization's managed settings set it for them, and never because the plugin is there, only for calls made while both switches were on, and only for calls made while Claude's current directory is in the repository that publishes it, which includes work on other repositories from there, apart from a line too long to read, which a run of the plugin counts, as refused, in each repository that it works on
~~~~

Clause, the new unit:

~~~~text
;
~~~~

## `CONTRIBUTING.md`

### Entry

Old:

~~~~text
The tool supports Python 3.11 and later, so use Python 3.11 locally if you can: CI tests on 3.11 and on the newest release.
~~~~

New:

~~~~text
The tool supports Python 3.11 and later, so use Python 3.11 locally if you can: CI tests on 3.11 and on the newest release (R25).
~~~~

Clause, the new unit:

~~~~text
The tool supports Python 3.11 and later, so use Python 3.11 locally if you can: CI tests on 3.11 and on the newest release
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
1. **The change first.** Update or add the OpenSpec change that says what must hold, with its requirements and scenarios. A change that makes or reverses a decision adds its record to [`docs/decisions/`](docs/decisions/README.md), and closes the record of any decision it reverses; a record that the default branch holds is never edited otherwise, except that a closed record's lines may become `[removed]`.
~~~~

New:

~~~~text
1. **The change first.** Update or add the OpenSpec change that says what must hold, with its requirements and scenarios. A change that makes or reverses a decision adds its record to [`docs/decisions/`](docs/decisions/README.md), and closes the record of any decision it reverses; a record that the default branch holds is never edited otherwise, except that a closed record's lines may become `[removed]` (R124, R129).
~~~~

Clause, the new unit:

~~~~text
1. **The change first.** Update or add the OpenSpec change that says what must hold, with its requirements and scenarios. A change that makes or reverses a decision adds its record to [`docs/decisions/`](docs/decisions/README.md), and closes the record of any decision it reverses; a record that the default branch holds is never edited otherwise, except that a closed record's lines may become `[removed]`
~~~~

Clause, the new unit:

~~~~text
.
~~~~

### Entry

Old:

~~~~text
2. **Threats at design.** Read [`docs/threat-model.md`](docs/threat-model.md) against the change. Add the threats it brings, each rated for impact and likelihood, with its answer.
~~~~

New:

~~~~text
2. **Threats at design.** Read [`docs/threat-model.md`](docs/threat-model.md) against the change. Add the threats it brings, each rated for impact and likelihood, with its answer (R31).
~~~~

Clause, the new unit:

~~~~text
2. **Threats at design.** Read [`docs/threat-model.md`](docs/threat-model.md) against the change. Add the threats it brings, each rated for impact and likelihood, with its answer
~~~~

Clause, the new unit:

~~~~text
.
~~~~

## For B-007

- `docs/threat-model.md`: the configuration is read only as a blob at each commit (T49: R19's requirement states it, but none of its scenarios does)
- `docs/threat-model.md`: the bill of materials is written from the tagged tree, never from a working tree, (T69: R28's requirement states it, but its scenario does not)
- `docs/threat-model.md`: A test fails when the configuration's reader takes a key or a value that the manifest does not name, or refuses a key or a value of the configuration that it names, (T53: no scenario holds this test; R122's scenario holds only what the manifest names)
- `docs/threat-model.md`: It skips only while no base's tree holds `docs/decisions/`, (T70: no scenario of R129 says when the check skips)
- `docs/threat-model.md`: finding a design decision or a task named without its change in any change, active or archived (T75: no scenario of R126 or R127 says how a design decision or a task named without its change is found)
- `docs/threat-model.md`: "Decided by" takes one of three fixed forms: the owner, with the dates of the decision; the change that made it; or that change, with the dates on which the owner asked for what it decided. (T72: R124 holds a field's form only in general; no scenario names the three forms, which DR-108 and DR-151 give)
- `docs/threat-model.md`: and no link, quotation or identifier fits in the field. (T72: no scenario of R124 states it)
- `docs/threat-model.md`: The README's section on turning capture off gives `git config --global --get pr-cost.capture` to see a session's opt-in (T120: the scenario "The README says how to turn capture off in a running session" (R194) gives `git config --show-origin --get-all pr-cost.capture` to see each value of a session's opt-in, and says that `--global --get` shows only the global file's value.)
- `docs/threat-model.md`: each golden session lists every call of its transcripts, by its message ID, (T83: R139 asks for each call with its entry or scenario; no scenario says that a golden session names a call by its message ID.)
- `docs/threat-model.md`: and the set holds a session for each rule at this boundary that changes a figure or a count (T87: no scenario of R139 asks for a golden session for each rule at this boundary.)
- `docs/threat-model.md`: and each golden test names as its expected error one that only a missing capture step or report raises, so a wrong figure fails CI on the pull request, before any tag (T99: no scenario states what a golden test names as its expected error.)
- `docs/threat-model.md`: a path that is not UTF-8 (T102: R137's scenario fails on a file that is not UTF-8; none names a path that is not.)
- `docs/threat-model.md`: never asking git to trust the folder (T122: a never-does of the capture step that no scenario or requirement of usage-capture states; R147's scenarios show only that the run records nothing and exits with success.)
- `docs/threat-model.md`: When the merged commit's `.claude/settings.json` or `.claude/settings.local.json` registers the hook's command with a checksum other than the SHA-256 of the hook file at that commit (T152: R202's requirement names both files, but its scenario that the comment names the registration covers `.claude/settings.json` alone.)
- `docs/threat-model.md`: has a manifest that holds no key but its name, version, description, author, licence and repository (T141: R188's requirement gives the allowed keys, but its scenarios name only keys that fail, never the list that passes.)
- `docs/threat-model.md`: found by its tag's full name in the default branch's first-parent history (T132: R184's requirement says so, but its scenarios say only that CI reads no ref by the short name, not that the tag's commit must be in the first-parent history.)
- `docs/threat-model.md`: passes the folder only when that tag's commit is in the default branch's first-parent history and a published release has its version (T138: the same gap of R184's scenarios as T132's, for the marketplace's check.)
- `docs/threat-model.md`: the test also fails on a checkout input other than its ref, its path and `persist-credentials`, on a checkout into another folder than the report reads, on a command other than the report's, and on the word `secrets` anywhere in the file (T187: no scenario of R237 states these further cases of the test.)
- `docs/threat-model.md`: it follows no ledger file that is a link, and takes as a count only a whole number from zero to below a bound, so that a line that gives another is counted as unread and the summary still says what it did (T191: no scenario of R241 states that the report follows no link or bounds a count.)
- `docs/threat-model.md`: the recorder keeps names only at a line's top level, in its `message` object and in `message.usage`, gives every other object and array as its type alone, and checks its own output, writing nothing on a failure (T186: R236's scenarios hold the kept shape, not the recorder's own behaviour or its check of its output.)
- `openspec/changes/add-pr-cost-calculator/design.md`: In a sparse checkout, too, the put-back puts the file into the working tree, where it would be had the step not taken it back. (No scenario of R116 or R117 states a put-back in a sparse checkout.)
- `openspec/changes/add-pr-cost-calculator/design.md`: A run takes back and puts back what it can before it reads any transcript (Only the plugin's run at a session's end is held to take back first, by R90's scenario; no scenario holds it for every run, nor for a put-back.)
- `openspec/changes/add-pr-cost-calculator/design.md`: padded to three (R124 asks for a record named for its number in ASCII digits; no scenario says that the number is padded to three digits.)
- `openspec/changes/add-pr-cost-calculator/design.md`: never how to change it (R135 asks an assumption to say what changes if it is wrong; no scenario says that it never says how to change it.)
- `openspec/changes/add-pr-cost-calculator/design.md`: an assumption being as checked as its least checked fact, from `not yet` through `documented` and `observed` to `tested` (R136 orders the least checked first, but no scenario says how an assumption's checks rank or that its least checked fact decides.)
- `openspec/changes/add-pr-cost-calculator/design.md`: a run checks each waiting call's entry again when it stages it, by the rules that it records by, so that an entry that someone wrote into the store carries nothing into a ledger file (No scenario has a run check a waiting entry again when it stages it.)
- `openspec/changes/add-pr-cost-calculator/design.md`: timeouts as the hook file's registration (R179 gives the plugin's hooks the same events and condition as the registration, but no scenario gives them the same timeouts.)
- `openspec/changes/add-pr-cost-calculator/design.md`: following no link and taking as a count only a whole number from zero to below a bound (R241 says what the skeleton's report counts, but no scenario has it follow no link or bound a count.)
- `docs/how-it-works.md`: The comment splits the token cost by model, by token type and by activity type. (R20's text gives the split, but no scenario of R20 or of activity-types states it; the page keeps it unchanged.)
- `docs/how-it-works.md`: Every figure can be recomputed from the ledger, the price table and the jobs API. (No scenario states that the comment's figures can be recomputed from those three sources; the page keeps it unchanged.)
- `docs/how-it-works.md`: or their organization's managed settings set it for them (R1's text names an organization's managed settings, but no scenario shows them opting a member in; R182's scenario covers only a required plugin without the opt-in.)
- `README.md`: An organization can also set it for its members. (No capture scenario shows an organization setting the opt-in for a member; R186 obliges only the README's words about it.)
- `SECURITY.md`: or their organization's managed settings set it for them (Same clause as on the page on how the tool works: R1's text holds it and no scenario does.)

## Left as it is

None yet.
