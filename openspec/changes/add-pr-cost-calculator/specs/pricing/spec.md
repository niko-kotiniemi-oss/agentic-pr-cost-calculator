## Purpose

Keep a dated price table for model tokens and CI runners, and turn recorded token usage into an API-equivalent cost, using the prices and modifiers that applied on the day the usage happened, and never guessing a price that the price table does not hold.

## ADDED Requirements

### Requirement: Prices are dated

The price table SHALL give each price, and each statement of how modifiers combine, an effective date. A cost SHALL use, for each ledger entry or CI job, the latest price, and the latest statement of how modifiers combine, whose effective date is on or before the UTC day the usage happened, so that a later row reprices nothing before its date. An entry whose day has no price yet SHALL be left out of the cost and named, and an entry dated after the day the report runs SHALL be refused.

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

A ledger entry whose model is `unknown`, because the capture step's price table did not list it, SHALL be counted in tokens and left out of the cost. The report SHALL name the model, or say that it is unknown, and say that its cost is missing.

#### Scenario: A new model has no price yet

- **WHEN** a pull request's ledger files hold calls recorded with the model `unknown`, because the capture step's price table did not list their model
- **THEN** the report shows those calls' tokens, and says that their model is unknown and their cost is missing

### Requirement: A model that the price table lists without a price is counted under its name

The price table SHALL be able to list a model with no price, such as a self-hosted one, in a row that names its provider and effective date as any row does, so that capture records its name and the report counts its tokens under that name, leaves it out of the cost and says that it has no price, which the comment tells apart from an unknown model and from usage before a model's first price (see "Prices are dated").

#### Scenario: A listed model with no price is counted under its name

- **WHEN** a pull request's ledger files hold calls of a model that the price table lists with no price
- **THEN** the report shows those calls' tokens under the model's name, says that the model has no price, and leaves them out of the cost without calling the model unknown

#### Scenario: A price added later for a model listed with no price applies from its date

- **WHEN** the price table lists a model with no price from one date, and adds a priced row for the same provider and model with a later effective date
- **THEN** calls before the later date are counted with no price, and calls on or after it are priced

### Requirement: The price table states one currency

The model price table and the runner price table SHALL each state the one currency of all their prices, by its ISO 4217 code, the same in both, and the report SHALL write each cost in it. The tool's checks SHALL fail on a table that states no currency or more than one, and on two tables that state different currencies.

#### Scenario: Every cost is in the table's currency

- **WHEN** the price table states its currency as `USD`
- **THEN** every cost that the comment and the job summary show is written with `USD`

#### Scenario: A table without one currency fails the checks

- **WHEN** a price table states no currency, or states more than one
- **THEN** the checks fail, naming the table

#### Scenario: Two tables in different currencies fail the checks

- **WHEN** the model price table states `USD` and the runner price table states another currency
- **THEN** the checks fail, naming both tables

### Requirement: A call is priced by its provider and its model

Each price row SHALL name its provider, such as Anthropic's API, Amazon Bedrock or Google Vertex AI, and a model listed under more than one SHALL mark one as its default. A call SHALL be priced by the row of its entry's provider and model, or, when its provider is `unknown`, of its model's only or default provider, which the comment's detail SHALL say was taken from the table. An entry whose provider and model no row names SHALL be counted in tokens, left out of the cost and named.

#### Scenario: Two providers of one model are priced apart

- **WHEN** the price table gives one model different rates for two providers, and a pull request has a call of that model through each
- **THEN** each call is priced at its own provider's rate

#### Scenario: An unknown provider is priced at the model's default provider and said so

- **WHEN** a call's entry gives the provider `unknown` and a model that the price table lists under two providers, one marked as its default
- **THEN** the call is priced at the default provider's rates, and the comment's detail names that provider and says that it was taken from the price table, not from the call

#### Scenario: A provider and model that no row names are named, not guessed

- **WHEN** a call's entry gives a provider and a model that the price table lists, but no row for that pair
- **THEN** the report shows that call's tokens, leaves it out of the cost, and names the provider and the model

#### Scenario: A model listed under two providers with no default fails the checks

- **WHEN** a price table lists one model under two providers and marks neither, or both, as its default
- **THEN** the checks fail, naming the model

### Requirement: The price table states the day it was last checked

The price table SHALL state the UTC day on which its rows were last checked against their sources, which the comment SHALL give as the price table's date, and when a priced call's day is after that date the brief summary SHALL say that prices may have changed since then.

#### Scenario: A call after the table's date is flagged

- **WHEN** the price table was last checked on one day and a pull request has a priced call on a later day
- **THEN** the comment gives the day it was checked as the price table's date, and the brief summary says that prices may have changed since then

#### Scenario: A table that states no checked day fails the checks

- **WHEN** a price table states no day on which it was last checked, or one after the day the checks run
- **THEN** the checks fail, naming the table
