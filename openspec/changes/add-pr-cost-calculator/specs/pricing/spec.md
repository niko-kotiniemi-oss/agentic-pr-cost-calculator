## Purpose

Keep a dated price table for model tokens and CI runners, and turn recorded token usage into an API-equivalent cost, using the prices and modifiers that applied on the day the usage happened, and never guessing a price that the price table does not hold.

## ADDED Requirements

### Requirement: Prices are dated

The price table SHALL give each price, and each statement of how modifiers combine, an effective date. A cost SHALL use, for each ledger entry or CI job, the latest price, and the latest statement of how modifiers combine, whose effective date is on or before the UTC day the usage happened, so that a row added later reprices nothing earlier. An entry whose day has no price yet SHALL be left out of the cost and named, and an entry dated after the day the report runs SHALL be refused.

#### Scenario: A price change applies from its date

- **WHEN** a model's output price changes on a date and a pull request has calls the day before and the day after
- **THEN** the earlier calls are priced at the old price and the later ones at the new price

#### Scenario: Usage before any known price is named, not priced

- **WHEN** an entry's day falls before the earliest effective date for its model
- **THEN** that entry is left out of the cost, and the report names its model and its day

#### Scenario: An entry from the future is refused

- **WHEN** an entry's day is after the day the report runs
- **THEN** the entry is refused, and counted as refused

#### Scenario: A changed combination reprices nothing earlier

- **WHEN** the price table adds a statement of how two modifiers combine for a model, dated after the statement before it, and a pull request has calls with both modifiers on the day before that date and on that date
- **THEN** the earlier calls are priced as the earlier statement says, and the later ones as the new one says

#### Scenario: Every price in the table has an effective date

- **WHEN** the price table is read
- **THEN** every price in it, and every statement of how modifiers combine, has an effective date

### Requirement: Every token type is priced at its own rate

Input, output, cache-write and cache-read tokens SHALL each be priced at their own rate. Cache writes SHALL use the rate for their cache lifetime. When the source does not give the lifetime, the cost SHALL show the range between the two lifetimes' prices.

#### Scenario: A call's cost is the sum of its token types

- **WHEN** an entry has input, output, five-minute cache-write and cache-read tokens
- **THEN** its cost is each count times its own rate, summed

#### Scenario: An unknown lifetime gives a range

- **WHEN** an entry's cache writes do not say their lifetime
- **THEN** the cost is reported as a low and a high figure

### Requirement: Price modifiers are applied

A call SHALL be priced with every modifier the price table lists for its model and day: higher rates for a prompt above a length, where a model has them; a multiplier for its inference region; rates for its speed and its service tier; and a per-request rate for server-side tool requests, such as web searches. A prompt's length SHALL count its input, cache-write and cache-read tokens. Modifiers SHALL combine as the price table's statement for the call's model and day says.

#### Scenario: A long prompt is priced at its higher rates

- **WHEN** a model has higher rates above a prompt length, and a call's input, cache-write and cache-read tokens together exceed that length
- **THEN** that call is priced at the higher rates

#### Scenario: A region multiplier applies to every token type

- **WHEN** a call's entry gives an inference region for which the price table gives a multiplier
- **THEN** each of that call's token costs is multiplied by it

#### Scenario: Web searches are priced per search

- **WHEN** a call's entry gives server-side web searches
- **THEN** they are priced at the table's per-search rate, in addition to the call's tokens

#### Scenario: Web fetches add nothing beyond their tokens

- **WHEN** a call's entry gives server-side web fetches, which the price table lists at no charge
- **THEN** the call is priced, and its cost is that of its tokens alone

#### Scenario: A fast speed is priced at its premium rates

- **WHEN** a call's entry gives a speed for which the price table gives premium rates, as it does for fast mode
- **THEN** each of that call's token types is priced at that speed's rate

#### Scenario: A service tier is priced at its own rates

- **WHEN** a call's entry gives a service tier for which the price table gives rates
- **THEN** each of that call's token types is priced at that tier's rate

#### Scenario: Modifiers combine as the price table states

- **WHEN** a call's prompt is above its model's long-prompt length, the call's entry gives an inference region that has a multiplier and a fast speed, and the price table states how those modifiers combine for its model and day
- **THEN** the call's cost is what that statement gives

### Requirement: An unpriced attribute or combination is named, not guessed

A call with a recorded attribute whose value the price table does not price, or with a combination of attributes the table does not state, SHALL be counted in tokens, left out of the cost and named, as an unknown model is.

#### Scenario: An unpriced attribute is named, not guessed

- **WHEN** a call's entry gives a speed for which the price table has no rate
- **THEN** the report shows that call's tokens, leaves it out of the cost, and names the model and that speed

#### Scenario: A combination the price table does not state is named, not guessed

- **WHEN** a call's entry gives attributes that call for two modifiers whose combination the price table does not state for its model and day
- **THEN** the report shows that call's tokens, leaves it out of the cost, and names the model and those attributes

### Requirement: An unknown model is reported, not guessed

A ledger entry whose model is `unknown`, because the capture step's price table did not list it, or whose model has no price, SHALL be counted in tokens and left out of the cost. The report SHALL name the model, or say that it is unknown, and say that its cost is missing.

#### Scenario: A new model has no price yet

- **WHEN** a pull request's ledger files hold calls recorded with the model `unknown`, because the capture step's price table did not list their model
- **THEN** the report shows those calls' tokens, and says that their model is unknown and their cost is missing
