# B-007: The tool's requirements, corrected before the build

- **Status:** Planned
- **Last changed:** 2026-11-14
- **Brief:** The change's requirements, corrected with what the items above find, before any of them is built. It also settles how the comment shows a cost, the prices' rules, a ledger and a price table that fit more than one provider, and the points that earlier reviews left open.
- **Rests on:** R18, R21, R97, R122, B-001, B-002, DR-234
- **Issue:** 18
- **Pull requests:** none

## Problem

None of the change's requirements is built yet, so a fix made to them now costs a revision, while one made after the build costs code, tests and a release. The assessment of patterns, the risk register and earlier reviews each leave points that change what the tool must do.

## What done looks like

The change is revised before it is built. It takes the design fixes from the assessment of patterns and anti-patterns (B-001) and the further answers to high risks from the risk register (B-002). The ledger entry and the price table can name an agent and a provider, so that the change that adds an agent need not also change a ledger format that a release wrote, which the public surface holds (R122, DR-234). A fork records nothing until its owner turns the tool on there. The comment shows, by default, a brief summary of each model's tokens and price, with the detail on request, in a small block that a program can also read, and no dollar sign and no tilde outside inline code in the comment or its job summary, so that GitHub shows no amount as a formula or struck through, as issue 18 asks (R21, R97). The rounding of CI minutes is settled (R18), and so are the prices' rules: when a price is added, models with no price, and the price table's currency. The ledger's day field is named so that it says UTC, and the tool keeps, prints and sends no text of a transcript and reads no secret.

## Postponed points

- From the reviews of pull request 7: whether calls whose transcript lines give no working directory are counted; the oldest git that the tool supports, or a check that git reads its setting against lazy fetching; T16 and the marking of generated files; T68's allowance for each file written, and the tests of task 6.3.
- From the assessment of 2026-11-12, with the owner's answers that day: GitHub's code scanning for Python in its default setup, a repository setting that the owner turns on, with a record that names the owner as its decider and says that a private repository would need a paid product, where deterministic checks such as Semgrep, Bandit, Ruff and pip-audit would take its place; the vendor check run with the base commit's script; and a step in the README that verifies a release's attestation.
- From earlier reviews: the sentence on prices in R30, R57 against R113, the points stated only in scenarios of R13, R20, R25 and R69, the requirement ranges, R81 and R109, the residual risk of T4, the Python command on Windows, a security advisory for every security fix, and the copies of the oldest Python that its test does not read.
