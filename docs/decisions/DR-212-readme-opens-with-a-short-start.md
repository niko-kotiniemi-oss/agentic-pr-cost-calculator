# DR-212: The README opens with a short start

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-10
- **Requirements:** R198, R199, R205
- **Threats:** T2, T31, T58, T132, T133, T134, T136, T138, T145, T146, T147, T148, T149, T152, T154
- **Replaces:** none
- **Closed by:** none

## Context

The README is where adopters start. The change asks it to say a great deal before a person sets the tool up: how a repository adopts the tool, with its calling workflow, its hook file and their checks, what an opt-in records and publishes and where it applies, how to install the plugin, and what holds for a project's cloud threads, for organizations and for turning capture off (R159, R164, R185 to R187, R194 to R196, task 4.4). On 2026-11-10 the owner asked that the README give a very concise instruction for a person and for an organization, so that setting the tool up does not look daunting. The design-stage review of that opening, on 2026-11-10, found that a person who follows it alone needs it to say what an opt-in publishes before they opt in, that a call counts in the repository it is made from, that stopping reaches each running session, whose cloud environment takes the opt-in's line, which repository's release and marketplace to use, and what a zip's checksum is checked against (T145, T148, T152, T154).

## Decision

The README opens, after its first paragraph and its status, with a short start that holds no HTML and at most 200 words outside code, counted as the runs of letters or digits, with any apostrophe or hyphen inside them, that are left once its heading, its code blocks, its inline code and each link's brackets and target are taken out. Before any step that opts anyone in, it says that the tool records only the sessions of people who are opted in, that one opt-in covers every repository that turns the tool on, later ones too, that a call counts in the repository it is made from, whatever it works on, and that what a session spends is committed with its work, can be traced to the person, is published when that work is pushed, even after an opt-out, and stays published. It says how a repository turns the tool on, pinned to a published release; how a person opts in on each machine, and in the setup script of a cloud environment that only they use; that a project's cloud threads also need the plugin, added in the project's settings, from the latest release's zip after checking its checksum against that release's README, or from this repository's marketplace, named by its address, whose updates need no approval; that an organization tells its members, then turns the plugin on and opts them in; and how to stop, on each machine and in each running session, and in a setup script or with another environment, which an organization can undo. Each step links the section of the README that gives its detail, and its links name only the README's headings and this repository's latest release, by its full address. Until this repository's root marketplace file holds an entry for the tool's plugin, the README's status says that this repository's marketplace does not serve it yet.

## Alternatives

- A short start that gives the steps alone, which would leave a person who reads no further to opt in without knowing what an opt-in publishes (T145).
- What an opt-in publishes said after the steps, as the first draft had it, which a person who stops reading at the step that opts them in would not reach.
- No limit on the short start's length, which would let it grow back into the detail with each change that adds a step.
- No short start, with every step given where its detail is, which is the README as the change had it before.

## Consequences

- Tests hold the short start's place, its length by the rule above, that it holds no HTML, what it says an opt-in records and publishes and that it says so before any step that opts anyone in, its commands against those of the sections that it links and against the specs, the marketplace's address against the section on installing the plugin, and its links (R198, R199; T145, T146, T147, T149).
- The short start names the checks that keep a person safe and links the sections that give them: the zip's checksum against the release's own README before the zip is uploaded (T133, T152), a published release to pin (T58), that the marketplace's updates need no approval (T132, T136), and an organization telling its members before it opts them in (T134). It says that what a session spends is committed and published, while the section on adopting the tool says what a public repository's ledger and comment show (T31), and that a call counts in the repository it is made from (T2).
- It names this repository's marketplace and latest release by their addresses, so that an unchanged copy of the README elsewhere still sends its readers here (T148), and its way to stop names each running session and says that a push after an opt-out still publishes (T154).
- What the short start leaves out, such as that a hashed id does not hide whose record it is, stays in the sections of detail, which a person may not open (T145).

## Scope

This covers the README's opening. Where the README's detail lives, and how it shows, is DR-213 (The README keeps its detail, folded below its short start), which addresses the README may give is DR-215 (The README gives no address outside this repository but those that its test lists), and what the detail says is in the requirements that the context names.

## What reversing it would change

R198 and R199 in `project-standards` would change, with their scenarios, and so would design decision 12, task 4.4, the answers of T2, T31, T58, T132 to T134, T136, T145 to T149, T152 and T154, the proposal's "What Changes", the glossary's short start and the feature page for `project-standards`. DR-213 and DR-215 would be revisited.
