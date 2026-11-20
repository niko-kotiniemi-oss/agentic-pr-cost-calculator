# DR-020: Prices come from a dated price table in the repository

- **Type:** architecture
- **Boundary:** incoming
- **Reversibility:** reversible with work
- **Status:** accepted
- **Decided by:** the owner, 2026-10-27
- **Requirements:** R14, R16, R18, R30, R94
- **Threats:** T17, T24, T27, T30
- **Replaces:** none
- **Closed by:** none

## Context

Each cost uses the price in force on the day of its usage (see the proposal), and every number in a report has to be reproducible from the ledger, the price table and the jobs API (see the design's goals). Anthropic's prices carry modifiers beyond the four token rates (see the design's context), and both Anthropic and GitHub publish new prices, so each price has to be kept with the day it took effect.

## Decision

Prices come from a price table kept as data in this repository, `prices/models.json` and `prices/github-actions.json`, which gives every price, and every statement of how a model's modifiers combine, an effective date and its source page. A row is never changed or removed: a price changes only by a pull request that adds a row dated after the newest one for the same price, or for the same model's combination. The report reads the table at the tool's own commit and fetches no price.

## Alternatives

- Fetching prices from an API when the report runs, instead of keeping them in a table in the repository. Anthropic publishes no price API that could replace this.

## Consequences

- A new price counts only once its row is in the table and an adopter pins a commit that holds it. Until then, as the design's risk "[Prices go stale, or a new model appears]" says, a report names the table's date and what it cannot price (DR-124).
- An adopting repository can change a price only by pinning a different tool, which T21 covers.
- A row dated after the newest one but before its pull request merges reprices the days in between, which that pull request's diff shows, with the row's source, for review (T30).
- Since the report fetches no price, it opens no connection to a price service, which could carry its token outside GitHub (T24).

## Scope

This covers where prices come from and how the table changes. That the figure is an estimate at list prices is DR-002 (The figure is an estimate at list prices, not a bill), and which names the hook records is DR-054 (Names the price table does not list are recorded as `unknown`).

## What reversing it would change

R14 in `pricing` would change, with its scenarios, and so would R30's sentences on the report's connections and on prices in `project-standards`, with their scenarios "The report connects only to GitHub" and "Prices are never fetched", and so would the clauses of R16, R18 and R94 that price by the day or name the table's date. So would the design's decision 4, the answers of T17, T24, T27 and T30, the proposal, the README, the `pricing` feature page, `docs/how-it-works.md`, and tasks 3.1 and 3.2. R122 does not list the price table in the public surface (DR-154). DR-054 and DR-124 would be revisited.
