# DR-169: A change to the files that hold the opt-in is taken as an opt-out

- **Type:** security and privacy
- **Status:** accepted
- **Decided by:** the owner, 2026-11-02
- **Requirements:** R107, R108, R162
- **Threats:** T38, T105, T117, T120
- **Replaces:** none
- **Closed by:** none

## Context

Runs bound the intervals when both switches were on (DR-168), and the step cannot see a switch change between two runs. A person who turns capture off and on again between two runs would, if each run looked only at the switches, have the calls made while capture was off recorded (T38). The person's opt-in is read from their two global git configuration files, and git's own reading of it, from every file that git reads the key from, can turn it off (DR-183), as can the repository's own git configuration (DR-050), which routine commands such as `git push -u` write. A run cannot tell what a change between two runs was, so calls recorded before an opt-out and back that no run saw would still wait in the store to be staged. On 2026-11-02 the owner kept the files that this record names, rather than every file that git reads its settings from or the two global files alone.

## Decision

A run that finds both switches on notes, beside its time, a fingerprint of the files that can turn the person's capture on or off: their two global configuration files, each other file that git reads the opt-in key from, which either of git's two readings of it names (DR-183), the repository's own git configuration among them only when it sets the key, and each link on the way to one. A file's fingerprint is made of its device and inode numbers, size and modification times, never of its contents or its path, a missing file has a fingerprint of its own, and the store keeps only a hash of the whole. A run that notes another fingerprint than the last that the store notes first does what an opt-out does (DR-171), since a change that it cannot read may have been an opt-out and back, and so ends every session's interval and empties the store, and then begins the next interval if it finds both switches on.

## Alternatives

- Fingerprinting the person's two global files alone, which would not see capture turned off and on again in a file that git reads the key from, such as one that a conditional include names.
- Fingerprinting every file that git reads its settings from, the repository's own configuration among them whatever it sets, which would also see an opt-out and back in an included file that set no opt-in key at the last run, but would end the interval at the routine commands that write the repository's configuration, such as `git push -u`.
- Only ending the interval at a change, which would leave the calls recorded before an opt-out and back waiting to be staged.
- A hash of each file's contents, which would end fewer intervals for changes that leave the switches as they were, but would keep in the store a value computed from the person's configuration.
- No fingerprint, which would record the calls made while capture was off whenever it was turned on again before the next run.

## Consequences

- Any change to those files between two runs ends every interval and drops the calls waiting to be staged, at the cost of those calls and of the calls between those runs, as the design's risks say. A routine command that writes the repository's own git configuration, such as `git push -u`, ends no interval unless that configuration sets the opt-in key, while a routine write to a global file, such as `git config --global user.email` or the `safe.directory` line that git's own advice adds, ends every interval and raises the flag for consent (T120).
- A change that keeps a file's device and inode numbers, size and modification times, as a rewrite in place within the time resolution of a coarse file system, is not seen, and nor is an opt-out and back in an included file, or in the repository's own git configuration, that set no opt-in key at the last run, so the calls between the runs around it are recorded (T105), as the README's section that task 4.4 writes says.
- A copy of the store that a backup or a sync puts back after an opt-out brings back no call when the opt-out changed a file that the fingerprint holds, since the next run notes another fingerprint (T117).
- The store holds no value computed from a configuration file's contents, and no configuration file's path.

## Scope

This covers how a run tells that the files that hold the opt-in have changed, and what it does then. How intervals bound consent is DR-168, what an opt-out does is DR-171 (An opt-out empties the store), and where the opt-in is read is DR-183 (The opt-in is read only from the person's global git configuration, and git's own reading of it can only turn capture off) and DR-050 (A repository's git configuration can turn capture off, never on).

## What reversing it would change

R107, R108 and R162 in `switch-and-opt-in` would change, with their scenarios, and so would the design's decisions 6 and 15 and their risks, T38's answer, T105, T117, and tasks 1.1 and 2.4. The fingerprints are in the store, whose format is part of the public surface, so the change would be a breaking one for adopters (DR-096).
