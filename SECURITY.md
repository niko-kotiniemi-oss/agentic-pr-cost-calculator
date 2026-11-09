# Security policy

## Reporting a vulnerability

Please report vulnerabilities privately through GitHub: open this repository's **Security** tab and choose **Report a vulnerability**. Do not open a public issue for a security problem.

We aim to acknowledge a report within a week and will tell you what we decide to do about it.

## Supported versions

There is no release yet. Once there is, fixes go to the latest release only. The tool supports Python 3.11 and every later release, and each release carries a CycloneDX software bill of materials.

## What this tool handles

The tool will read token-usage records and GitHub Actions job data, and it will write one comment on the pull request it measures. The ledger files it reads are committed with the pull requests that add them. It is designed so that:

- it needs no secret beyond the `GITHUB_TOKEN` a workflow already has, with the narrowest permissions that work;
- the ledger entries it writes hold counts, the model, the price attributes, the UTC day, the activity type, whether the main agent or a subagent made the call, and a hash of the call's message id, and never prompts, code, tool names, transcript text or any session identifier, and each ledger file's first line holds only its format's version, its count of refused calls and flags, with no count, for calls left out;
- the notes that capture keeps for its own use never leave the git common directory of the person's clone, where its store is readable and writable by that person alone, except on Windows, keeps nothing past 30 days, holds a session's id, a transcript's path, a worktree, a branch and a `tool_use_id` only as hashes, and holds plain names only for a staged or taken-back ledger file, until a run resolves it, a staged one's transcript path among them, which carries the session's id, and capture keeps no copy of a transcript;
- it records a person's usage only when that person has turned capture on for themselves, only for calls made while both switches were on, and only for calls made while Claude's current directory is in the repository that publishes it, which includes work on other repositories from there;
- its tests use synthetic fixtures only, never real usage data.

A change that would break any of these is a security issue.

The threats the design answers, and how each is held, are in [`docs/threat-model.md`](docs/threat-model.md).
