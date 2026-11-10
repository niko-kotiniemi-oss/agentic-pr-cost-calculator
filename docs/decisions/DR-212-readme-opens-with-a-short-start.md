# DR-212: The README opens with a short start

- **Type:** process
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-10
- **Requirements:** R198, R199
- **Threats:** T31, T58, T133, T134, T145, T146, T147
- **Replaces:** none
- **Closed by:** none

## Context

The README is where adopters start. The change asks it to say a great deal before a person sets the tool up: how a repository adopts the tool, with its calling workflow, its hook file and their checks, what an opt-in records and publishes and where it applies, how to install the plugin, and what holds for a project's cloud threads, for organizations and for turning capture off (R159, R164, R185 to R187, R194 to R196, task 4.4). On 2026-11-10 the owner asked that the README give a very concise instruction for a person and for an organization, so that setting the tool up does not look daunting.

## Decision

The README opens, after its first paragraph and its status, with a short start of at most 200 words outside code: how a repository turns the tool on, pinned to a release; how a person opts in, with the same line in a cloud environment's setup script, and adds the plugin for a project's cloud threads, from a release's zip after checking its checksum or from the marketplace; how an organization opts its members in; and how to stop, each step linking the section of the README that gives its detail. It says that turning the tool on in a repository records no one's sessions by itself, that only the sessions of people who are opted in are recorded, that one opt-in covers every repository that turns the tool on, later ones too, that what a session spends is committed with its work under its author's name, published when that work is pushed and still published after an opt-out, and that an organization tells its members before it opts them in.

## Alternatives

- A short start that gives the steps alone, which would leave a person who reads no further to opt in without knowing what an opt-in publishes (T145).
- No limit on the short start's length, which would let it grow back into the detail with each change that adds a step.
- No short start, with every step given where its detail is, which is the README as the change had it before.

## Consequences

- Tests hold the short start's place and length, what it says an opt-in records and publishes, its commands against those of the sections that it links, and its links to this repository (R198, R199; T145, T146, T147).
- The short start names the checks that keep a person safe and links the sections that give them: the zip's checksum before the zip is uploaded (T133), a release to pin (T58), and an organization telling its members before it opts them in (T134), and it says what an adopter's repository publishes (T31).
- What the short start leaves out, such as that a hashed id does not hide whose record it is, stays in the sections of detail, which a person may not open (T145).

## Scope

This covers the README's opening. Where the README's detail lives, and how it shows, is DR-213 (The README keeps its detail, folded below its short start), and what that detail says is in the requirements that the context names.

## What reversing it would change

R198 and R199 in `project-standards` would change, with their scenarios, and so would design decision 12, task 4.4, the answers of T31, T58, T133, T134 and T145 to T147, the proposal's "What Changes", the glossary's short start and the feature page for `project-standards`. DR-213 would be revisited.
