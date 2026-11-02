# DR-169: A change to a file that can turn capture off ends the interval

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02
- **Requirements:** R107, R108
- **Threats:** T38, T105
- **Replaces:** none
- **Closed by:** none

## Context

Runs bound the intervals when both switches were on (DR-168), and the step cannot see a switch change between two runs. A person who turns capture off and on again between two runs would, if each run looked only at the switches, have the calls made while capture was off recorded (T38). The person's opt-in is read from their two global git configuration files, and the repository's own git configuration can turn it off (DR-048 and DR-050).

## Decision

A run that finds both switches on notes, beside its time, a fingerprint of each file that can turn the person's capture on or off: their two global configuration files and the repository's own git configuration. A file's fingerprint is made of its identity, size and modification times, never of its contents, and a missing file has a fingerprint of its own. A run that notes another fingerprint than the interval's last run noted ends that interval at that last run, and begins the next one if it finds both switches on.

## Alternatives

- Fingerprinting the person's two global files alone, which would not see capture turned off and on again in the repository's own git configuration, though it would not end the interval at the routine commands that write that file, such as `git push -u`.
- A hash of each file's contents, which would end fewer intervals for changes that leave the switches as they were, but would keep in the store a value computed from the person's configuration.
- No fingerprint, which would record the calls made while capture was off whenever it was turned on again before the next run.

## Consequences

- Any change to those files between two runs ends the interval, at the cost of the calls between those runs, a routine `git push -u` or `git config` in the repository included, as the design's risks say.
- A change that keeps a file's identity, size and modification times, as a rewrite in place within the time resolution of a coarse file system, is not seen, so the calls between the runs around it are recorded (T105).
- The store holds no value computed from a configuration file's contents.

## Scope

This covers how a run tells that the files that hold the opt-in have changed. How intervals bound consent is DR-168, and where the opt-in is read is DR-048 (The opt-in is read only from the person's global git configuration) and DR-050 (A repository's git configuration can turn capture off, never on).

## What reversing it would change

R107 and R108 in `switch-and-opt-in` would change, with their scenarios, and so would the design's decisions 6 and 15 and their risks, T38's answer, T105, and tasks 1.1 and 2.4. The fingerprints are in the store, whose format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
