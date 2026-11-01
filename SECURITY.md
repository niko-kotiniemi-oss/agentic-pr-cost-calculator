# Security policy

## Reporting a vulnerability

Please report vulnerabilities privately through GitHub: open this repository's **Security** tab and choose **Report a vulnerability**. Do not open a public issue for a security problem.

We aim to acknowledge a report within a week and will tell you what we decide to do about it.

## Supported versions

There is no release yet. Once there is, fixes go to the latest release only. The tool supports Python 3.11 and every later release, and each release carries a CycloneDX software bill of materials.

## What this tool handles

The tool will read token-usage records and GitHub Actions job data, and it will write one comment on the pull request it measures. The ledger files it reads are committed with the pull requests that add them. It is designed so that:

- it needs no secret beyond the `GITHUB_TOKEN` a workflow already has, with the narrowest permissions that work;
- it records counts, the model, the price attributes, the UTC day, the activity type, whether the main agent or a subagent made the call, and a hash of the call's message id, and never prompts, code, tool names, transcript text or any session identifier;
- it records a person's usage only when that person has turned capture on for themselves, and only for calls made while their session's working directory is in the repository that publishes it, which includes work that session does on other repositories from there;
- its tests use synthetic fixtures only, never real usage data.

A change that would break any of these is a security issue.

The threats the design answers, and how each is held, are in [`docs/threat-model.md`](docs/threat-model.md).
