# DR-242: The licence is the Fair Core License, with MIT as its future licence

- **Type:** process
- **Status:** accepted
- **Decided by:** the owner, 2026-11-16
- **Requirements:** R28
- **Threats:** none
- **Replaces:** DR-099
- **Closed by:** none

## Context

DR-099 put the repository's own work under the MIT licence. On 2026-11-16 the owner set out a model in which the tool stays free for each person who uses it, updates and new features included, while a paid version adds settings for organizations and other features, both with the same transparency and support, and in which no one else sells the tool. The MIT licence lets anyone sell or bundle the tool, and leaves nothing to sell but support.

The Fair Core License, version 1.0, which Keygen publishes at fcl.dev, grants the use of the software for any purpose other than a Competing Use, which it defines as making the software available to others in a commercial product or service that substitutes for it or offers the same or substantially similar functionality. It forbids moving, changing, disabling or circumventing the software's licence key functionality, and it grants each version under a future licence on the second anniversary of the date that version is made available. Its MIT variant, FCL-1.0-MIT, names MIT as that future licence. The licence is not on the SPDX list.

The repository has been public under MIT since it was created, on 2026-10-20, and has no release yet.

## Decision

The repository's own work is under the Fair Core License, version 1.0, with MIT as its future licence (FCL-1.0-MIT). `LICENSE` holds its text word for word as fcl.dev publishes it, with the notice "Copyright 2026 Niko Kotiniemi", and `pyproject.toml` declares it as `license = "LicenseRef-FCL-1.0-MIT"`.

## Alternatives

- The MIT licence, as DR-099 had it: anyone may sell the tool, and there is nothing to sell but support.
- Open core, with the tool under MIT and the features for organizations in a separate, closed add-on: the free and the paid parts both work, but others may sell the tool, and a second codebase is kept whose source the users of the paid version do not see.
- The Functional Source License, FSL-1.1-MIT: the same grant without the clause on licence keys, so an organization may unlock a paid feature for its own use.
- The Business Source License 1.1: up to four years before its change licence applies, and a grant of use that this repository would have to draft for itself.
- The Elastic License 2.0: it never becomes open source, and it is aimed at hosted services, which the tool is not.
- PolyForm Noncommercial or PolyForm Small Business, with a paid licence beside it: the first leaves out a developer who uses the tool for an employer's work, and the second anyone at a company of 100 people or more, or with a revenue of 1,000,000 USD (2019) or more.
- The AGPL with a paid licence beside it: others may sell the tool under the AGPL's terms, and many companies do not allow the AGPL at all.

## Consequences

- The tool is no longer open source by the Open Source Initiative's definition, since the licence restricts a Competing Use. DR-243 (The tool is fair source, in a public repository) closes DR-114, which said it was.
- Each commit that the repository made public before this record stays available under MIT to whoever holds a copy of it. Each version made available under this licence is also available under MIT from the second anniversary of the day it was made available.
- A contribution is licensed under the repository's licence, as `CONTRIBUTING.md` says. That licence alone does not let the licensor also offer a contribution under other terms, so an outside contribution merges only once its author has agreed to the contributor licence agreement that backlog item B-023 brings (DR-244).
- `tests/test_repository.py` holds that `LICENSE` is the FCL-1.0-MIT text, by the SHA-256 of the text with its notice left blank, that its one notice is this record's word for word, and that `pyproject.toml` declares `LicenseRef-FCL-1.0-MIT`. A changed word of the licence, another or a longer notice, or another declared licence fails it.
- Each release's bill of materials names FCL-1.0-MIT, as the scenario "The bill of materials describes the release" of R28 expects.
- The vendored Superpowers and OpenSpec's generated skills keep the MIT licence that each carries, and the README's section on the licence says so, so that the licence of the repository's own work is not read as theirs.
- The clause on licence keys has nothing to apply to until a feature behind a licence key exists. Such a feature is a new data flow, and perhaps a new trust boundary, in a tool whose hook reads transcripts, so it adds its threats to `docs/threat-model.md` before it is built, as `CLAUDE.md` asks of every change that adds one, and any key that signs licences is a secret that the repository never holds.
- What DR-099's last section named was read again. R28's scenario, `LICENSE`, the licence in `pyproject.toml`, the licence test, the README's opening and its section on the licence, `CONTRIBUTING.md`'s section on the licence and the opening sentence of `CLAUDE.md` change with this record, and the bill of materials that task 6.2 writes names this licence. DR-114 is closed by DR-243, and DR-115 (Outside contributions are welcome), whose contributions came under MIT, by DR-244. DR-116 (The repository carries the usual open-source files) still holds, since its decision is the set of files, which stays the same: its consequence that a test checks `LICENSE` for the MIT licence describes the test as it was, and the test that this record names takes its place. DR-097 (Each release carries a bill of materials), whose scope names DR-099 as the licence that the bill of materials names, still holds, and the licence it names is this record's. Assumption A67 rests on this record instead of DR-099.

## Scope

This covers the licence of the repository's own work. The vendored Superpowers and OpenSpec's generated skills keep their own licences, which the bill of materials lists with their sources (R28). That the tool is fair source rather than open source is DR-243 (The tool is fair source, in a public repository), and whether a contribution may also be offered under other terms is backlog item B-023 (A contributor licence agreement). Where the repository lives is not decided here.

## What reversing it would change

How hard it is to reverse: reversible with work for later versions, and a one-way door for each version already made available, which keeps this licence and becomes available under MIT on its second anniversary, while the copies made under MIT before this record stay under MIT. Going back to MIT, or to another licence, would change what DR-099's last section named, as the consequences above list it, and DR-243 and backlog item B-023 would be revisited. The licence is not part of the public surface, so the release check would not take the change for a breaking one.
