# B-028: A daily check of published prices

- **Status:** Open to feedback and contributions
- **Last changed:** 2026-11-24
- **Brief:** A routine that reads the providers' published prices each day and opens a pull request with the rows that changed, each with its source, so that the price table lags a price change by days, not until someone notices.
- **Rests on:** R14, R287, R288, R289, R294, DR-299
- **Issue:** none
- **Pull requests:** none

## Problem

A price is added a few days after it changes, by hand (DR-299), and an adopter's report prices every call at the rows that its pinned release holds. Nothing notices a published price change, so the table can lag one for as long as no one looks. A routine that read the providers' pages would read text that someone else controls and hold a token that can open pull requests, which no threat of the model covers yet.

## What done looks like

A routine checks the providers' published prices each day and opens a pull request with each changed row, dated the day the price took effect and naming its source, and never merges one. It reads the pages as data, writes nothing but rows and their sources, and its change carries a threat review of its own, which covers the pages it reads, the token it holds and the rows it writes.

## Postponed points

- From the threat review at design of the first pull request of B-007 (boundary 7): the routine that DR-299 names has no item and no threat.
