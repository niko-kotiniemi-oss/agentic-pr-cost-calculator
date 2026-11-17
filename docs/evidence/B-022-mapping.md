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

## For B-007

None yet.

## Left as it is

None yet.
