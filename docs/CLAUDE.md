# CLAUDE.md: Agentic PR cost calculator, the documentation
These rules add to this repository's root `CLAUDE.md` for work on files under `docs/`, and wherever
the root sends you here, or make its rules stricter there. They never loosen it: where one would,
the root wins, so tell the owner. Unless the root's text is in front of you, read it first. Every
page under `docs/` but this file describes and never tells you what to do, apart from the guide,
`docs/patterns.md`, which steers below the root and this file.
## Decision records
`docs/decisions/README.md` gives a record's form and lists every record.
- A record that the default branch holds changes only by being closed by the record that replaces
  it, which restates whatever still holds, and once closed, only by having lines of its text
  replaced by `[removed]`. Only two exceptions hold: the change that brings a field that DR-268
  names adds it to every record and changes nothing else, and a number held twice is mended as
  DR-269 gives.
- A record covers one topic, and says how hard it is to reverse in the first sentence of its section
  on what reversing it would change, until records gain a field for it. A record that closes another
  says in its consequences what became of each record, requirement and threat that rests on the
  closed one (DR-230).
- When the owner asked for an outcome and the change chose how, a record's decider is the change, as
  the owner asked, with the dates (DR-151).
- Write a record in the third person and the present tense: it describes what was decided, and never
  addresses a reader.
## The threat model
Read its section How it was built before you change it: each threat follows its method.
- A change that adds an input, a trust boundary, a permission or a data flow adds its threats and
  their answers there.
- The two reviews that the root asks for work this way. At design, each reviewer reads the design
  and the specs in a context of its own, finds the threats that are missing and rates their
  likelihood, and its findings change the design where they need to. Before the merge, the review
  rates each threat again against what was built, and adds the threats that it brings (DR-095).
- Rate every threat for impact and likelihood, each from 1 to 3 as the method defines them, give its
  risk as their product, and place it in the risk matrix. Rate it raw too, as if its answer were not
  built, and give a threat whose risk with its answer in place is high or critical a further answer,
  as the method gives them (DR-254, DR-255).
- `tests/test_threat_model.py` checks that every citation resolves; whether a citation still says
  what holds the answer is for you and the review to check.
- After changing the threat model, run `python3 -I scripts/risk_register.py`, which writes the risk
  register again (DR-256).
## The pages that a change updates
In the same pull request as what it describes, a change updates the requirement's row in
`docs/requirements.md`, its feature page in `docs/features/`, `docs/how-it-works.md` for any change
to a flow, an input, an output, a credential, a permission or a connection, and the backlog item and
`docs/roadmap.md` for a change that finishes, adds or moves an item (DR-103, DR-225).
`tests/test_documentation.py` checks what a machine can; the rule it serves is that the tool does
nothing that its documentation leaves out.
## Clauses that wait for a change of their own
- The root gives the route of a clause that the mapping of B-022, `docs/evidence/B-022-mapping.md`,
  lists for B-007. A sentence that states what the tool does in a document that the sweep left as it
  is, such as the glossary or an assumption, is brought to the rule that the specs are the single
  source only by a change of its own that the owner asks for (DR-252).
- The mapping describes: the text that it quotes is what the default branch held before the sweep,
  kept as its evidence, and never says what the tool does or what to build.
## The guide and the backlog
- Read the guide's opening before you change the guide. A principle that the owner asks you to add,
  remove, change or move to another concern goes in a pull request that changes nothing outside
  `docs/`, `openspec/`, `CLAUDE.md`, `tests/CLAUDE.md` and `CHANGELOG.md`. An entry cites the rule
  that it rests on, and never states it again. A principle knowingly accepted is accepted only where
  its record says.
- `docs/backlog/README.md` gives an item's form and its statuses.
