# Pricing

The tokens are priced from a dated price table kept in this repository, at the price that applied on the day each call was made.

**Status:** designed, not built yet.

**Spec:** `pricing`

**Requirements:** R14, R15, R16, R61, R17

## Expected behaviour

- **Dated prices.** Every price has an effective date, and each call uses the latest price dated on or before its UTC day. A price change is a new row with a later date, so history is never rewritten (DR-020). The statements of how modifiers combine are dated the same way, so a changed combination reprices nothing earlier.
- **Each token type at its own rate.** Input, output, cache-write and cache-read tokens are priced separately. Cache writes use the rate for their cache lifetime, and where the lifetime is unknown the report gives the range between the two.
- **Modifiers.** Higher rates for long prompts, the inference region's multiplier, rates for speed and service tier, and a per-request rate for server-side tool requests such as web searches, all as the price table states them.
- **Nothing is guessed.** A model, attribute or combination that the price table does not price is counted in tokens, left out of the cost and named by the report.
- **Never fetched.** Prices are read from the table at the tool's own commit. The tool fetches no prices from anywhere, a rule that `project-standards` holds for the whole tool.

## How it is validated

This feature is validated first by its spec's scenarios: each gets an acceptance test before its code, seen to fail for the expected reason (task 1.4). Then come the checks that DR-084 to DR-093 and DR-109 apply to all the tool's code. Beyond those, this feature has its own:

- A test that every price row has its date and its source, and that a pull request cannot change or remove an existing row or add one dated on or before the newest existing one for the same price (task 3.1).
- Tests of each modifier and of their combinations, with property tests that a cost is never negative and adds up across any split of the ledger (task 3.2).

## See also

- `pricing` in `openspec/`, and design decision 4 of `add-pr-cost-calculator`.
