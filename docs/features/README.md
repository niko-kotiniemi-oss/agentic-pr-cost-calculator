# Features

What the tool consists of, one page per feature, from the side of the person who uses it. Each feature is one spec under `openspec/`, and its page is named for that spec. Each page says what the feature does, how it is expected to behave, which requirements in [`../requirements.md`](../requirements.md) it holds, and how it is validated. How the features fit together as one tool is in [`../how-it-works.md`](../how-it-works.md).

The tool is designed and not built yet, so each page describes the behaviour the specs require. A page changes in the same pull request as the feature it describes.

| Feature | What it does |
|---|---|
| [Turning it on, and personal opt-in](switch-and-opt-in.md) | A repository turns the tool on with one file; each person's opt-in, which they, their cloud environment or their organization set, decides whether their own sessions are recorded. |
| [Usage capture](usage-capture.md) | Records each model call's token counts during a Claude Code session and commits them with the agent's work. |
| [Activity types](activity-types.md) | Labels each call as code generation, file reading, tooling, MCP, subagent, conversation or other. |
| [The ledger](ledger.md) | The small files that carry the counts to the pull request and stay as its record. |
| [Pricing](pricing.md) | Prices the tokens from a dated table, by token type and with the price modifiers. |
| [CI minutes](ci-minutes.md) | Adds the GitHub Actions minutes that the pull request's own commits used. |
| [The report comment](report-comment.md) | Posts one comment with the cost when the pull request merges. |
| [Releases and compatibility](releases-and-compatibility.md) | Which Python versions the tool runs on, and how versions are released. |
| [Standards for the whole tool](project-standards.md) | What holds for the whole tool: documentation, connections, rated threats, pull request text and pinned actions. |
