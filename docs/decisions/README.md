# Decision records

Each decision about what the tool is, how it works and how it is built has a record of its own here, so that each can be reversed or replaced on its own. A record holds one choice: why it was made, what else was considered, what follows from it, what it covers, and what reversing it would change. Its fields say what kind of decision it is, whether it still holds, who decided it, and the requirements of `docs/requirements.md` and the threats of `docs/threat-model.md` that it shapes.

A record that the default branch holds is accepted, and from then on it changes only by being closed, by a record that replaces it, after which lines of its text may become `[removed]`. Design decision 13 of `add-pr-cost-calculator` describes the form and the checks that `tests/test_decisions.py` holds. Within a record, the design, the proposal and the tasks named without a change are those of the change that added the record.

| Record | Decision | Type | Status | Decided by | Requirements | Threats |
|---|---|---|---|---|---|---|
| [DR-001](DR-001-who-the-tool-is-for.md) | The tool is for teams that build pull requests with AI coding agents | scope | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 | R20 | none |
| [DR-002](DR-002-an-estimate-not-a-bill.md) | The figure is an estimate at list prices, not a bill | scope | accepted | the change `add-pr-cost-calculator` | R94 | T16, T27 |
| [DR-003](DR-003-claude-code-only.md) | Claude Code is the only agent `add-pr-cost-calculator` captures | scope | accepted | the owner, 2026-10-27 | R7, R13, R76 | none |
| [DR-004](DR-004-code-review-cost-later.md) | The cost of AI review by an app or a job in CI is left to a later change | scope | accepted | the owner, 2026-10-18 and 2026-10-27 | R20, R94 | none |
| [DR-005](DR-005-report-at-merge-only.md) | The report runs once, at merge | scope | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 | R20, R68 | T23, T29 |
| [DR-006](DR-006-github-com-only.md) | GitHub.com only, not GitHub Enterprise Server | scope | accepted | the change `add-pr-cost-calculator` | none | T23 |
| [DR-007](DR-007-powershell-tool-out-of-scope.md) | Commands sent through the PowerShell tool are out of scope | scope | accepted | the owner, 2026-10-27 | R7 | T8, T19 |
| [DR-008](DR-008-no-outside-service.md) | Capture uses no service outside GitHub and the repository | architecture | accepted | the change `add-pr-cost-calculator` | R30 | T24 |
| [DR-009](DR-009-capture-through-hooks.md) | Capture reads the transcripts through hooks while the session runs | architecture | closed | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 | R7, R13, R44, R90 | T8, T14, T40, T42 |
| [DR-010](DR-010-usage-in-the-agents-commits.md) | Usage travels inside the agent's own commits | architecture | accepted | the change `add-pr-cost-calculator` | R7 | T8, T10, T16 |
| [DR-011](DR-011-calls-wait-in-the-git-directory.md) | Recorded calls wait in the git directory | architecture | accepted | the change `add-pr-cost-calculator` | R11, R47 | T10, T13, T38, T42, T44 |
| [DR-012](DR-012-calls-stay-on-their-branch.md) | A call goes only to a commit in its worktree, on its branch | architecture | accepted | the change `add-pr-cost-calculator` | R3, R46, R78, R81 | T8, T10, T19 |
| [DR-013](DR-013-staged-just-before-the-commit.md) | A ledger file is staged just before a commit that capture can follow | architecture | accepted | the change `add-pr-cost-calculator` | R8, R49, R51 | T8, T10 |
| [DR-014](DR-014-unused-ledger-files-taken-back.md) | A ledger file that no commit took is taken back | architecture | accepted | the change `add-pr-cost-calculator` | R9, R51, R57, R87, R110, R113, R114 | T8, T10, T19, T38, T42 |
| [DR-015](DR-015-ledger-is-the-record.md) | The ledger stays in the repository as the record | architecture | accepted | the owner, 2026-10-18 | R22 | T20 |
| [DR-016](DR-016-report-writes-nothing.md) | The report writes nothing to the repository | architecture | accepted | the owner, 2026-10-18 | R22, R24 | T24 |
| [DR-017](DR-017-usage-is-what-the-merge-adds.md) | A pull request's usage is the ledger files its merge adds | architecture | accepted | the change `add-pr-cost-calculator` | R58, R119 | T19, T20, T22 |
| [DR-018](DR-018-report-runs-on-the-merge-push.md) | The report runs on the push that a merge makes to the default branch | architecture | accepted | the change `add-pr-cost-calculator` | R68 | T23, T50 |
| [DR-019](DR-019-ci-from-the-pull-requests-commits.md) | CI minutes come from the runs on the pull request's own commits | architecture | accepted | the change `add-pr-cost-calculator` | R23, R62, R120 | T22 |
| [DR-020](DR-020-dated-price-table.md) | Prices come from a dated price table in the repository | architecture | accepted | the owner, 2026-10-27 | R14, R16, R18, R30, R94 | T17, T24, T27, T30 |
| [DR-021](DR-021-one-file-switch.md) | One file, `.pr-cost.json`, turns the tool on or off | architecture | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 | R1, R19, R36, R91 | T49 |
| [DR-022](DR-022-hook-is-a-copied-file.md) | Adopters copy the hook file from a pinned commit | architecture | accepted | the change `add-pr-cost-calculator` | R12, R53, R72, R88 | T28, T54, T59, T60, T69 |
| [DR-023](DR-023-standard-library-only.md) | The hook and the report use Python's standard library only | technical | accepted | the change `add-pr-cost-calculator` | R12, R25 | T28 |
| [DR-024](DR-024-python-and-markdown.md) | The tool, its release and its documentation are Python and Markdown | technical | accepted | the owner, 2026-10-20 and 2026-10-27 | none | none |
| [DR-025](DR-025-oldest-python-3-11.md) | The oldest supported Python is 3.11 | technical | accepted | the owner, 2026-10-20 | R25, R32 | T56 |
| [DR-026](DR-026-one-source-for-the-python-floor.md) | `requires-python` is the one source of the oldest supported Python | technical | accepted | the change `add-pr-cost-calculator` | R99 | T55 |
| [DR-027](DR-027-hook-checks-its-floors.md) | The hook checks its Python and git versions first | technical | accepted | the change `add-pr-cost-calculator` | R32, R99, R110 | T56 |
| [DR-028](DR-028-renovate-policy.md) | Renovate waits 14 days, and proposes vulnerability fixes at once | technical | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 and 2026-10-20 | R26 | T28 |
| [DR-029](DR-029-activity-from-tool-names.md) | Activity types come from tool names, which are never recorded | technical | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 | R4, R6 | T1 |
| [DR-030](DR-030-bash-hooks-only-for-git.md) | The Bash hooks run only for commands that run git | technical | accepted | the change `add-pr-cost-calculator` | R7 | T8, T19 |
| [DR-031](DR-031-command-ends-in-exit-0.md) | The registered command ends in `; exit 0` | technical | accepted | the change `add-pr-cost-calculator` | R13 | T14 |
| [DR-032](DR-032-call-with-no-stop-reason.md) | A call with no stop reason is read from its last line, as a lower bound | technical | accepted | the change `add-pr-cost-calculator` | R42, R95 | T7, T8 |
| [DR-033](DR-033-one-record-per-call.md) | A call is identified by its message id | technical | accepted | the change `add-pr-cost-calculator` | R2, R41 | T7 |
| [DR-034](DR-034-stage-only-what-it-can-tell.md) | Capture stages only for a commit whose branch and contents it can tell | technical | accepted | the change `add-pr-cost-calculator` | R8, R48, R49, R82, R83, R86, R112 | T8, T10, T19 |
| [DR-035](DR-035-commit-unchanged.md) | Capture never changes what the agent's commit would do | technical | accepted | the change `add-pr-cost-calculator` | R56, R84, R85 | T10, T12 |
| [DR-036](DR-036-store-written-whole.md) | The store is replaced whole, under a lock | technical | accepted | the change `add-pr-cost-calculator` | R11 | T13, T42 |
| [DR-037](DR-037-sparse-index-off.md) | Adopters keep git's sparse index off | technical | accepted | the owner, 2026-10-20 | none | T8, T10 |
| [DR-038](DR-038-minutes-from-job-times.md) | CI minutes come from job times, rounded up per job | technical | accepted | the change `add-pr-cost-calculator` | R18, R62 | T22 |
| [DR-039](DR-039-call-budget-and-time-limit.md) | The report keeps to a call budget and a time limit | technical | accepted | the change `add-pr-cost-calculator` | R64, R70 | T51 |
| [DR-040](DR-040-old-ledger-formats-read.md) | A newer report reads every earlier ledger format | technical | accepted | the change `add-pr-cost-calculator` | none | T53 |
| [DR-041](DR-041-superpowers-vendored.md) | Superpowers is vendored and compared with upstream in CI | technical | accepted | the change `add-pr-cost-calculator` | none | T35 |
| [DR-042](DR-042-openspec-pinned.md) | OpenSpec is pinned and its skills are regenerated in CI | technical | accepted | the change `add-pr-cost-calculator` | none | T35, T66 |
| [DR-043](DR-043-one-aggregate-ci-job.md) | CI ends in one aggregate `ci` job | technical | accepted | the change `add-pr-cost-calculator` | R25 | none |
| [DR-044](DR-044-inputs-are-untrusted.md) | Everything that crosses into the tool is untrusted | security and privacy | accepted | the change `add-pr-cost-calculator` | R5, R14, R21, R23, R24, R35, R36, R45, R66, R67, R89, R92, R96, R97, R98, R102 | T6, T14, T17, T18, T23, T25, T26, T48, T49, T52 |
| [DR-045](DR-045-counts-never-content.md) | Ledger entries hold counts, never content | security and privacy | accepted | the change `add-pr-cost-calculator` | R4 | T1, T4, T31 |
| [DR-046](DR-046-personal-opt-in.md) | Each person turns on capture of their own sessions | security and privacy | accepted | the owner, 2026-10-18 | R1 | T3 |
| [DR-047](DR-047-consent-per-call.md) | Consent holds for each recorded call | security and privacy | closed | the change `add-pr-cost-calculator` | R40, R107, R108, R109, R118 | T38, T46 |
| [DR-048](DR-048-opt-in-from-global-config.md) | The opt-in is read only from the person's global git configuration | security and privacy | closed | the change `add-pr-cost-calculator` | R1, R37, R38, R103, R104, R105 | T3, T41 |
| [DR-049](DR-049-opt-in-read-strictly.md) | The opt-in is read strictly | security and privacy | accepted | the change `add-pr-cost-calculator` | R106 | T3 |
| [DR-050](DR-050-repository-can-only-opt-out.md) | A repository's git configuration can turn capture off, never on | security and privacy | accepted | the change `add-pr-cost-calculator` | R1, R39, R109 | T3 |
| [DR-051](DR-051-report-cannot-be-turned-off-by-its-pull-request.md) | A pull request cannot turn off its own report | security and privacy | accepted | the change `add-pr-cost-calculator` | R19, R92 | T21, T49 |
| [DR-052](DR-052-day-not-time.md) | An entry records the UTC day of a call, not its time | security and privacy | accepted | the change `add-pr-cost-calculator` | R2, R4 | T5 |
| [DR-053](DR-053-no-session-value.md) | An entry records no session value | security and privacy | accepted | the change `add-pr-cost-calculator` | R2, R4 | T4 |
| [DR-054](DR-054-unlisted-names-unknown.md) | Names the price table does not list are recorded as `unknown` | security and privacy | accepted | the change `add-pr-cost-calculator` | R17, R77, R98 | T1 |
| [DR-055](DR-055-committed-calls-never-restaged.md) | Calls of a ledger file found in a commit are never staged again | security and privacy | accepted | the owner, 2026-10-19 | R52, R81, R110, R113, R117 | T2, T8, T10 |
| [DR-056](DR-056-no-history-check.md) | Capture does not read the branch's history | security and privacy | closed | the owner, 2026-10-19 | R2, R45, R52, R81 | T2, T19 |
| [DR-057](DR-057-calls-by-working-directory.md) | Calls are kept by the session's working directory | security and privacy | accepted | the change `add-pr-cost-calculator` | R3 | T2 |
| [DR-058](DR-058-checksum-before-running.md) | The hook file runs only when its checksum matches | security and privacy | accepted | the change `add-pr-cost-calculator` | R88, R122 | T59 |
| [DR-059](DR-059-only-git-from-a-safe-folder.md) | The hook starts only git, by absolute path, from a safe folder | security and privacy | closed | the change `add-pr-cost-calculator` | R54, R118 | T46 |
| [DR-060](DR-060-hook-offline.md) | The hook opens no network connection | security and privacy | accepted | the change `add-pr-cost-calculator` | R30, R45, R111 | T45 |
| [DR-061](DR-061-report-only-on-default-branch-push.md) | The report runs only for a push to the default branch | security and privacy | accepted | the change `add-pr-cost-calculator` | R68 | T23, T29 |
| [DR-062](DR-062-report-runs-its-own-code.md) | The report runs its own pinned code | security and privacy | accepted | the change `add-pr-cost-calculator` | R24 | T23, T28, T30 |
| [DR-063](DR-063-least-privilege-caller.md) | The calling workflow grants only what the report needs | security and privacy | accepted | the change `add-pr-cost-calculator` | R24 | T24, T29 |
| [DR-064](DR-064-report-flags-risky-changes.md) | The report flags changes to the switch, the hook and the workflows | security and privacy | closed | the change `add-pr-cost-calculator` | R93 | T21, T25, T30, T49, T60 |
| [DR-065](DR-065-fixed-hook-path.md) | The hook's path is fixed, not a setting | security and privacy | accepted | the change `add-pr-cost-calculator` | R65, R93 | T60 |
| [DR-066](DR-066-hand-edited-ledger-accepted.md) | A ledger edited by hand is an accepted risk | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T16 |
| [DR-067](DR-067-read-only-workflows.md) | Workflow tokens are read-only, except for releases and the report's comment | security and privacy | accepted | the change `add-pr-cost-calculator` | R27 | T37, T68 |
| [DR-068](DR-068-actions-pinned-to-tagged-commits.md) | Every action is pinned to a commit that its repository tagged | security and privacy | accepted | the change `add-pr-cost-calculator` | R34 | T28, T63 |
| [DR-069](DR-069-no-private-data.md) | The public repository holds no private data | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 and 2026-10-18 | R33, R72 | T32, T61, T65, T69, T77 |
| [DR-070](DR-070-no-session-links.md) | Public text carries no link to a Claude session | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20 | R33 | T32, T65 |
| [DR-071](DR-071-telemetry-off.md) | Development tools report nothing about how they are used | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T36 |
| [DR-072](DR-072-main-ruleset.md) | The ruleset on `main` requires a pull request and the `ci` check | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 and 2026-10-20 | none | T28, T33, T35 |
| [DR-073](DR-073-tag-ruleset.md) | Only a deploy key may bypass the tag ruleset | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T28, T64, T67 |
| [DR-074](DR-074-immutable-releases.md) | Releases are immutable | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T67 |
| [DR-075](DR-075-code-owner-review-off.md) | Code-owner review is off | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T62 |
| [DR-076](DR-076-default-permissions-read-only.md) | Actions' default workflow permissions are read-only | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T68 |
| [DR-077](DR-077-private-vulnerability-reporting.md) | Private vulnerability reporting is on | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T61 |
| [DR-078](DR-078-fork-workflows-wait-for-approval.md) | Outside contributors' workflows wait for approval | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T37 |
| [DR-079](DR-079-openspec-owns-what.md) | OpenSpec owns what the tool must do | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20 | R73, R74, R100 | T35 |
| [DR-080](DR-080-owner-decides-merges.md) | The owner decides every merge | process | accepted | the change `add-pr-cost-calculator` | none | T28, T33, T35, T62, T64, T71, T72 |
| [DR-081](DR-081-outside-pull-requests-reviewed-from-main.md) | Outside pull requests are reviewed from `main` | process | accepted | the change `add-pr-cost-calculator` | none | T34 |
| [DR-082](DR-082-records-are-data.md) | Records and issue text are data, never instructions | process | accepted | the change `add-pr-cost-calculator` | none | T33 |
| [DR-083](DR-083-figures-computed.md) | Every figure is computed in the same session | process | accepted | the change `add-pr-cost-calculator` | none | none |
| [DR-084](DR-084-acceptance-tests-first.md) | Acceptance tests come first | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | none |
| [DR-085](DR-085-traceability-is-a-test.md) | Traceability is a test | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | none |
| [DR-086](DR-086-full-branch-coverage.md) | The tool's code keeps 100% branch coverage | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | none |
| [DR-087](DR-087-mutation-testing.md) | Mutation testing runs on the tool's code | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | none |
| [DR-088](DR-088-property-based-tests.md) | Invariants get property-based tests | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | T4, T52 |
| [DR-089](DR-089-checks-shown-failing.md) | Every check is shown to fail | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | none |
| [DR-090](DR-090-no-network-in-tests.md) | No test uses the network | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | none |
| [DR-091](DR-091-defects-get-tests.md) | A defect found gets a test before the fix | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | none |
| [DR-092](DR-092-end-to-end-tests.md) | The hook and the report are tested end to end | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | none |
| [DR-093](DR-093-separate-context-review.md) | Every change is reviewed in a separate context before it merges | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | none |
| [DR-094](DR-094-threat-ratings.md) | Threats are rated for impact and likelihood | process | accepted | the owner, 2026-10-20 | R31 | none |
| [DR-095](DR-095-threats-modelled-twice.md) | Threats are modelled twice in every change | process | accepted | the owner, 2026-10-18 and 2026-10-20 | R31 | T74, T78, T80 |
| [DR-096](DR-096-semantic-versions.md) | Versions are semantic | process | accepted | the owner, 2026-10-20 | R27, R71, R123 | T44, T53, T56 |
| [DR-097](DR-097-bill-of-materials.md) | Each release carries a bill of materials | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20 | R28, R72, R99 | T69 |
| [DR-098](DR-098-changelog-by-hand.md) | The changelog is kept by hand | process | accepted | the change `add-pr-cost-calculator` | none | none |
| [DR-099](DR-099-mit-licence.md) | The licence is MIT | process | accepted | the owner, 2026-10-17 | R28 | none |
| [DR-100](DR-100-requirements-register.md) | A register lists every requirement with its kind | process | accepted | the owner, 2026-10-20 | R29, R73, R100, R130 | none |
| [DR-101](DR-101-feature-pages.md) | Each feature has a page | process | accepted | the owner, 2026-10-20 and 2026-10-25 | R29, R73, R100 | none |
| [DR-102](DR-102-how-it-works-page.md) | A page explains how the tool works as a whole | process | accepted | the owner, 2026-10-20 | R29, R101 | T57 |
| [DR-103](DR-103-documentation-in-the-same-pull-request.md) | Documentation changes in the same pull request as what it describes | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20 | R73, R100, R101 | none |
| [DR-104](DR-104-one-spec-per-feature.md) | Each feature is one spec | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-25 | R73 | none |
| [DR-105](DR-105-one-behaviour-per-requirement.md) | Each requirement states one behaviour | process | accepted | the change `add-pr-cost-calculator` | none | none |
| [DR-106](DR-106-stable-requirement-ids.md) | Requirement IDs are stable and never reused | process | accepted | the change `add-pr-cost-calculator` | R126, R130 | T57, T75 |
| [DR-107](DR-107-proposal-reviews-stopped.md) | The proposal's reviews stopped after the twenty-fifth | process | accepted | the owner, 2026-10-20 | none | T2, T8, T10 |
| [DR-108](DR-108-decision-records.md) | Each decision has a record of its own, in an index | process | accepted | the owner, 2026-10-26 | R124, R125, R126, R127, R133, R134 | T72, T73, T74, T76, T78, T79, T81 |
| [DR-109](DR-109-positive-and-negative-tests.md) | Unit tests are positive and negative, at every boundary | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 | none | none |
| [DR-110](DR-110-ci-minutes-counted.md) | The cost counts CI minutes as well as model tokens | scope | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 | R14, R18, R20, R21, R24, R62, R63, R64, R66, R69, R94, R97, R120, R121 | T18, T22, T24, T26, T51 |
| [DR-111](DR-111-major-updates-wait.md) | Major updates wait for the owner's approval | technical | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20 | R26 | T64 |
| [DR-112](DR-112-likelihood-with-the-answer-in-place.md) | Likelihood is rated with the answer in place | process | accepted | the change `add-pr-cost-calculator` | none | none |
| [DR-113](DR-113-requirements-500-characters.md) | Each requirement is 500 characters or fewer | process | accepted | the owner, 2026-10-26 | none | none |
| [DR-114](DR-114-open-source.md) | The tool is open source, in a public repository | scope | accepted | the owner, 2026-10-17 | none | T32, T61, T65 |
| [DR-115](DR-115-outside-contributions-welcome.md) | Outside contributions are welcome | process | accepted | the owner, 2026-10-18 | none | T33, T34, T37, T61 |
| [DR-116](DR-116-open-source-files.md) | The repository carries the usual open-source files | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20 | none | T61, T62 |
| [DR-117](DR-117-nothing-undocumented.md) | The tool does nothing its documentation leaves out | scope | accepted | the owner, 2026-10-20 | R29, R30, R101 | T57 |
| [DR-118](DR-118-tool-name.md) | The tool is named `agentic-pr-cost-calculator` | scope | accepted | the owner, 2026-10-17 | none | none |
| [DR-119](DR-119-up-to-date-before-merging.md) | Pull requests merge only when up to date with the default branch | process | accepted | the change `add-pr-cost-calculator` | none | T76 |
| [DR-120](DR-120-threat-ids-retired.md) | Threat IDs are retired, never renumbered | process | accepted | the change `add-pr-cost-calculator` | R130, R132 | T75 |
| [DR-121](DR-121-records-closed-not-edited.md) | A record is never edited once accepted, only closed by a record that replaces it | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-26 | R126, R127, R129, R130 | T70, T71, T74, T75, T76, T77, T80 |
| [DR-122](DR-122-release-tags-on-first-parent-history.md) | A release tag names a commit in the default branch's first-parent history | security and privacy | accepted | the change `add-pr-cost-calculator` | R27 | T28, T58, T67 |
| [DR-123](DR-123-public-surface-manifest.md) | The release check compares a manifest of the public surface | technical | accepted | the change `add-pr-cost-calculator` | R71, R122, R123 | T53 |
| [DR-124](DR-124-unpriced-never-guessed.md) | What the price table does not price is named, never guessed | technical | accepted | the change `add-pr-cost-calculator` | R14, R17, R20, R61, R63 | T9, T17, T26, T27 |
| [DR-125](DR-125-hook-in-isolated-mode.md) | The hook runs in Python's isolated mode | security and privacy | accepted | the change `add-pr-cost-calculator` | R12 | T15, T28 |
| [DR-126](DR-126-development-dependencies-hash-locked.md) | Development dependencies are locked with hashes | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T28, T66 |
| [DR-127](DR-127-ledger-file-written-once.md) | Each commit's usage goes in a new file, written once | architecture | accepted | the change `add-pr-cost-calculator` | R8, R10 | T4, T11, T13 |
| [DR-128](DR-128-what-counts-as-a-commit.md) | Only git's commit subcommand counts as a commit, and a dry run does not | technical | accepted | the change `add-pr-cost-calculator` | R79, R80 | T8, T10 |
| [DR-129](DR-129-ledger-file-added-despite-ignore-rules.md) | A ledger file is added despite ignore rules and sparse checkouts | technical | accepted | the change `add-pr-cost-calculator` | R50 | T8, T10 |
| [DR-130](DR-130-take-back-undone-once.md) | A taken-back ledger file is put back once, when its commit holds it | technical | accepted | the change `add-pr-cost-calculator` | R110, R115, R116, R117 | T2, T8, T10, T38 |
| [DR-131](DR-131-call-counted-once-in-history.md) | A call counts at most once in the default branch's history | technical | accepted | the change `add-pr-cost-calculator` | R59, R67, R119 | T17, T19, T47, T48 |
| [DR-132](DR-132-report-is-a-reusable-workflow.md) | The report is a reusable workflow that adopters call | architecture | accepted | the change `add-pr-cost-calculator` | R122 | T24, T29 |
| [DR-133](DR-133-one-pull-request-per-comment.md) | A push gets a comment only when all its commits belong to one pull request | technical | accepted | the change `add-pr-cost-calculator` | R60, R69 | T19, T20 |
| [DR-134](DR-134-when-the-oldest-python-rises.md) | The oldest supported Python rises only near its end of life or for a security fix | technical | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-20 and 2026-10-27 | R26 | none |
| [DR-135](DR-135-unknown-usage-fields-counted.md) | A call with an unknown usage field is counted from the fields capture knows | technical | accepted | the change `add-pr-cost-calculator` | R43, R95 | T39 |
| [DR-136](DR-136-only-a-hash-of-the-message-id.md) | Only a hash of a call's message id is kept | security and privacy | accepted | the change `add-pr-cost-calculator` | R2, R4 | T4, T43 |
| [DR-137](DR-137-store-format-versioned.md) | The store states its format's version | technical | closed | the change `add-pr-cost-calculator` | R55 | T44 |
| [DR-138](DR-138-main-agent-or-subagent.md) | An entry records whether the main agent or a subagent made its call | technical | accepted | the change `add-pr-cost-calculator` | R2, R75 | none |
| [DR-139](DR-139-hook-not-the-reports-own.md) | The report names a hook that is not the report's own | security and privacy | accepted | the change `add-pr-cost-calculator` | R65 | T54, T60 |
| [DR-140](DR-140-no-bypass-actor.md) | The ruleset on `main` has no bypass actor | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 and 2026-10-20 | none | T28, T33, T35, T62, T64 |
| [DR-141](DR-141-no-approvals-required.md) | The ruleset on `main` requires no approvals | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 and 2026-10-20 | none | T62, T64 |
| [DR-142](DR-142-superpowers-owns-how.md) | Superpowers owns how the tool is built | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-18 and 2026-10-20 | none | T35 |
| [DR-143](DR-143-skills-used-as-written.md) | Skills are used as written, never from memory | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-25 | none | none |
| [DR-144](DR-144-tags-releases-settings-stay-with-the-owner.md) | Tags, releases, settings, rulesets and secrets stay with the owner | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T62, T64, T67 |
| [DR-145](DR-145-dependency-update-branches.md) | A session starts on a dependency-update branch only after the owner reviews its diff | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T35, T66 |
| [DR-146](DR-146-corrections-search-other-copies.md) | A correction counts as made once the claim's other copies are searched for | process | accepted | the change `add-pr-cost-calculator` | none | none |
| [DR-147](DR-147-tool-on-in-its-own-repository.md) | The tool is turned on in its own repository | process | accepted | the change `add-pr-cost-calculator` | none | none |
| [DR-148](DR-148-releases-from-tags.md) | Each release is made from a tag | process | accepted | the owner, 2026-10-20 | R27, R123 | T67, T68 |
| [DR-149](DR-149-version-and-changelog-entries.md) | `pyproject.toml` holds the version, and the changelog has one entry per release | process | accepted | the change `add-pr-cost-calculator` | R27, R71, R123 | T53 |
| [DR-150](DR-150-proposals-say-how-validated.md) | Each proposal says how its capabilities are validated | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-25 | R74 | none |
| [DR-151](DR-151-three-forms-of-decider.md) | A record's decider takes one of three forms | process | accepted | the change `add-pr-cost-calculator` | R124, R126 | T72 |
| [DR-152](DR-152-records-are-plain-text.md) | A record is plain text and links only to other records | security and privacy | accepted | the change `add-pr-cost-calculator` | R128 | T73, T75, T79 |
| [DR-153](DR-153-closed-record-text-removed.md) | A closed record's lines may be replaced by `[removed]` | security and privacy | accepted | the change `add-pr-cost-calculator` | R129 | T77 |
| [DR-154](DR-154-the-public-surface.md) | The public surface is what adopters configure or depend on | technical | accepted | the change `add-pr-cost-calculator` | R71, R122 | T44, T53, T56 |
| [DR-155](DR-155-unknown-cache-lifetime-priced-as-a-range.md) | A cache write of unknown lifetime is priced as a range | technical | accepted | the change `add-pr-cost-calculator` | R15 | none |
| [DR-156](DR-156-adopters-pin-a-released-commit.md) | Adopters pin the commit that a release names | security and privacy | accepted | the change `add-pr-cost-calculator` | none | T28, T58, T64 |
| [DR-157](DR-157-a-component-other-repositories-take-in.md) | The tool is a component that other repositories take in | scope | accepted | the owner, 2026-10-20 | R71, R122 | T28 |
| [DR-158](DR-158-how-a-record-names-things.md) | A record names other things by ID, number or path, and its change by name | process | accepted | the change `add-pr-cost-calculator` | R126, R127 | T75 |
| [DR-159](DR-159-records-and-threats-name-each-other.md) | A record and the threats it lists name each other | process | accepted | the change `add-pr-cost-calculator` | R131 | T78, T80 |
| [DR-160](DR-160-github-only.md) | GitHub is the only repository and CI service `add-pr-cost-calculator` supports | scope | accepted | the owner, 2026-10-27 | R30 | T24 |
| [DR-161](DR-161-tag-ruleset-on-every-tag.md) | The tag ruleset covers every tag | security and privacy | accepted | the owner, 2026-10-27 | none | T28, T67 |
| [DR-162](DR-162-assumptions-written-down.md) | The design's assumptions are written down, each with what rests on it and how it is checked | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28 | R135, R140, R143 | T32, T82, T86, T88, T95, T96, T97, T100, T101 |
| [DR-163](DR-163-assumptions-grouped-most-at-stake-first.md) | The assumptions are grouped, and listed with the most at stake first | process | accepted | the owner, 2026-10-28 | R136 | T92 |
| [DR-164](DR-164-a-glossary-and-its-test.md) | A glossary sets the words that the specs and pages use, and a test holds them | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28 | R137, R138 | T90, T94 |
| [DR-165](DR-165-a-golden-set.md) | A golden set of hand-worked sessions holds the tool's figures | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28 | R139, R141, R142 | T83, T84, T85, T87, T89, T91, T98 |
| [DR-166](DR-166-glossary-and-assumptions-describe.md) | The glossary, the assumptions and the pages they link to describe, and never steer | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28 | none | T33, T93, T95 |
| [DR-167](DR-167-release-needs-every-acceptance-test.md) | A release needs every acceptance test to pass | process | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-28 | R139 | T99 |
| [DR-168](DR-168-consent-inside-intervals-runs-bound.md) | Consent holds for each call, inside intervals that runs begin and end | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02 | R40, R108, R109, R144, R165, R166 | T38, T104 |
| [DR-169](DR-169-config-change-ends-interval.md) | A change to the files that hold the opt-in is taken as an opt-out | security and privacy | accepted | the owner, 2026-11-02 | R107, R108, R162 | T38, T105, T117, T120 |
| [DR-170](DR-170-switch-off-creates-no-store.md) | A run that finds a switch off creates no store | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02 | R118, R145 | T38, T46, T113 |
| [DR-171](DR-171-opt-out-empties-store.md) | An opt-out empties the store | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02 | R109, R146, R161 | T38, T114 |
| [DR-172](DR-172-hooks-and-a-start-run.md) | Capture reads the transcripts through hooks while the session runs, and a start run reads none | architecture | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-10-17 and 2026-11-02 | R7, R13, R44, R90, R148 | T8, T14, T38, T40, T42 |
| [DR-173](DR-173-operational-metadata-local-only.md) | Capture keeps operational metadata on the person's machine only where it needs it, and never publishes it | security and privacy | accepted | the owner, 2026-11-02 | R4, R89, R149 | T4, T109 |
| [DR-174](DR-174-store-ids-as-hashes.md) | The store keeps ids as hashes, and plain paths only while a ledger file needs them | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02 | R149 | T4, T10, T109 |
| [DR-175](DR-175-store-retention-window.md) | The store keeps nothing past a retention window of 30 days, and removes itself when empty | security and privacy | accepted | the owner, 2026-11-02 and 2026-11-03 | R150, R151 | T110, T114 |
| [DR-176](DR-176-store-owner-only.md) | The store is its owner's alone, and capture leaves alone a store that it cannot trust | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02 | R152 | T109, T112 |
| [DR-177](DR-177-removed-store-records-nothing-earlier.md) | A removed store lets no earlier call be recorded, and leaves staged ledger files to git | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02 | R153 | T10, T111 |
| [DR-178](DR-178-no-transcript-kept.md) | Capture keeps no transcript, and reprocessing transcripts is a change of its own | scope | accepted | the owner, 2026-11-02 | R154 | T107 |
| [DR-179](DR-179-unattributable-calls-left-out.md) | A call whose repository cannot be told is left out | security and privacy | accepted | the owner, 2026-11-02 | R3, R147 | T2, T108, T122 |
| [DR-180](DR-180-left-out-calls-flagged.md) | A ledger file flags calls left out, with no count | technical | accepted | the owner, 2026-11-02 | R155, R157 | T16, T27, T106 |
| [DR-181](DR-181-ledger-format-versioned.md) | Each ledger file states its format's version, and each version has a published schema | technical | accepted | the owner, 2026-11-02 | R156, R158, R163, R167, R168 | T16, T115, T118 |
| [DR-182](DR-182-what-stays-published.md) | The documentation says what stays published, and that a hash does not hide whose record it is | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02 | R146, R159, R164 | T3, T4, T116 |
| [DR-183](DR-183-opt-in-from-global-config-git-turns-off-only.md) | The opt-in is read only from the person's global git configuration, and git's own reading of it can only turn capture off | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02 | R1, R37, R38, R103, R104, R105, R160 | T3, T14, T41, T119 |
| [DR-184](DR-184-no-history-check.md) | Capture does not read the branch's history | security and privacy | accepted | the owner, 2026-10-19 | R2, R45, R52, R81, R153 | T2, T19 |
| [DR-185](DR-185-one-opt-in-every-repository.md) | One opt-in covers every repository that turns the tool on, and a person turns capture off by folder | security and privacy | accepted | the owner, 2026-11-02 and 2026-11-03 | R1, R160, R164 | T3, T121 |
| [DR-186](DR-186-report-flags-registration-too.md) | The report flags changes to the switch, the hook, its registration and the workflows | security and privacy | accepted | the change `add-pr-cost-calculator` | R93 | T21, T25, T30, T49, T60 |
| [DR-187](DR-187-store-version-upgraded-or-left-alone.md) | The store states its format's version, a later release upgrades an earlier one, and an unknown one is left alone | technical | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02 | R55, R107, R109, R145, R148, R150, R153 | T44 |
| [DR-188](DR-188-only-git-without-session-git-variables.md) | The hook starts only git, by absolute path, from a safe folder, without the session's git variables | security and privacy | accepted | the change `add-pr-cost-calculator`, as the owner asked on 2026-11-02 | R54, R118, R147, R160, R169 | T2, T46, T119, T121, T122 |
| [DR-189](DR-189-organization-mode-later.md) | An organization mode, in which capture cannot be turned off, is left to a later change | scope | accepted | the owner, 2026-11-03 | R1, R37, R160 | none |
| [DR-190](DR-190-unknown-configuration-key-not-valid.md) | A configuration file with a key that the tool does not know is not valid | technical | accepted | the owner, 2026-11-03 | R92, R122, R171 | T49, T123 |
| [DR-191](DR-191-report-says-when-tool-left-off.md) | The report says when a merge leaves the tool off | technical | accepted | the change `add-pr-cost-calculator` | R172 | T49, T123 |
| [DR-192](DR-192-key-twice-or-enabled-not-boolean-not-valid.md) | A configuration file that gives a key twice, or no `enabled` of `true` or `false`, is not valid | technical | accepted | the change `add-pr-cost-calculator` | R92, R171 | T49 |
