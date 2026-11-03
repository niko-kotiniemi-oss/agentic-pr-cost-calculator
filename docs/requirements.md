# Requirements

Every requirement the tool must meet, in one list. The specs under `openspec/` hold each requirement's full text and the scenarios that test it; this register is their index, so that what the tool must do can be read in one place. `tests/test_documentation.py` checks that the register and the specs hold the same requirements, each once.

Each requirement has one kind:

- **functional:** what the tool does.
- **behavioural:** how it responds to conditions, failures and inputs it must refuse.
- **non-functional:** a quality it must keep, such as privacy, security, compatibility, or how it is released and documented.

The capability names the spec that holds the requirement. Each capability is one feature, and each requirement is on its capability's page in [`features/`](features/README.md).

| ID | Kind | Capability | Requirement |
|---|---|---|---|
| R1 | behavioural | `switch-and-opt-in` | Capture runs only where the tool is on and the person has opted in |
| R2 | functional | `usage-capture` | Usage is recorded per model call |
| R3 | functional | `usage-capture` | Only calls made from this repository are recorded |
| R4 | non-functional | `ledger` | The ledger holds counts, never content |
| R5 | behavioural | `usage-capture` | Counts are whole numbers |
| R6 | functional | `activity-types` | Each entry carries an activity type |
| R7 | functional | `usage-capture` | Usage reaches the pull request with the agent's commits |
| R8 | behavioural | `usage-capture` | A ledger file is staged only for a commit whose branch and contents the step can tell |
| R9 | behavioural | `usage-capture` | A ledger file that no commit takes is taken back |
| R10 | behavioural | `ledger` | A ledger file is written once |
| R11 | behavioural | `usage-capture` | Runs at the same time keep every note whole |
| R12 | non-functional | `usage-capture` | The capture step is one self-contained file |
| R13 | behavioural | `usage-capture` | Capture never breaks or steers the session |
| R14 | functional | `pricing` | Prices are dated |
| R15 | functional | `pricing` | Every token type is priced at its own rate |
| R16 | functional | `pricing` | Price modifiers are applied |
| R17 | behavioural | `pricing` | An unknown model is reported, not guessed |
| R18 | functional | `ci-minutes` | CI minutes are billed per job, rounded up |
| R19 | functional | `switch-and-opt-in` | One file turns the tool on or off, and a pull request cannot turn off its own report |
| R20 | functional | `report-comment` | A merged pull request gets one report comment |
| R21 | behavioural | `report-comment` | The comment shows only what the report computed |
| R22 | functional | `ledger` | The ledger is the record |
| R23 | behavioural | `report-comment` | The report reads the ledger from git, within bounds |
| R24 | non-functional | `report-comment` | The report runs only trusted code, with the least it needs |
| R25 | non-functional | `releases-and-compatibility` | The tool runs on the oldest supported Python and on every later release |
| R26 | non-functional | `releases-and-compatibility` | The oldest supported Python and major updates change only on the owner's decision |
| R27 | non-functional | `releases-and-compatibility` | Releases are made from a tag that matches the version and the changelog |
| R28 | non-functional | `releases-and-compatibility` | Every release carries a software bill of materials |
| R29 | non-functional | `project-standards` | The documentation names everything the tool does |
| R30 | non-functional | `project-standards` | The tool connects only where its documentation says |
| R31 | non-functional | `project-standards` | Every threat is rated for impact and likelihood |
| R32 | behavioural | `releases-and-compatibility` | The capture step does nothing below its floors |
| R33 | non-functional | `project-standards` | Pull request text carries no private reference |
| R34 | non-functional | `project-standards` | Every pinned action is a commit its repository tagged |
| R35 | behavioural | `report-comment` | Each ledger line is held to the ledger format |
| R36 | behavioural | `switch-and-opt-in` | Capture reads the configuration file only as a regular file within its bound |
| R37 | behavioural | `switch-and-opt-in` | The person's opt-in is read only from their global configuration files |
| R38 | behavioural | `switch-and-opt-in` | The person's opt-in is read by git's rules |
| R39 | behavioural | `switch-and-opt-in` | A repository's own git configuration can turn capture off |
| R40 | behavioural | `switch-and-opt-in` | Consent holds for each recorded call |
| R41 | functional | `usage-capture` | A call is identified by its message id and read from its lines that give a stop reason |
| R42 | functional | `usage-capture` | A call with no stop reason is read from its last line once it is over |
| R43 | functional | `usage-capture` | A call with an unknown usage field is recorded and counted |
| R44 | functional | `usage-capture` | Capture reads only lines that end in a line break, and no one line holds it back |
| R45 | functional | `usage-capture` | Capture reads the branch's ledger files only from git |
| R46 | functional | `usage-capture` | Calls recorded with no branch checked out go only to a commit made the same way |
| R47 | functional | `usage-capture` | Capture keeps what it records inside the git common directory |
| R48 | behavioural | `usage-capture` | A substitution counts as a command before the commit |
| R49 | behavioural | `usage-capture` | A ledger file is staged in the worktree where its commit runs |
| R50 | behavioural | `usage-capture` | A ledger file is added despite ignore rules and sparse checkouts, unless git refuses it |
| R51 | behavioural | `usage-capture` | A run that comes again before the same command stages nothing twice |
| R52 | behavioural | `usage-capture` | A ledger file that a commit takes stays taken |
| R53 | non-functional | `usage-capture` | The capture step's first line names its release |
| R54 | non-functional | `usage-capture` | The capture step starts only git, from an absolute path |
| R55 | behavioural | `usage-capture` | The store is versioned: an earlier version is upgraded, an unknown one left alone |
| R56 | behavioural | `ledger` | The capture step stages only the ledger file it wrote |
| R57 | behavioural | `ledger` | A ledger file is noted before it is written |
| R58 | functional | `ledger` | Only the ledger files that the merge adds are counted |
| R59 | functional | `ledger` | Each call is counted at most once |
| R60 | functional | `ledger` | The job summary says how many ledger files a push without a comment removes or changes |
| R61 | functional | `pricing` | An unpriced attribute or combination is named, not guessed |
| R62 | functional | `ci-minutes` | Every job attempt of the pull request's own runs is counted |
| R63 | functional | `ci-minutes` | Minutes on a runner the price table does not list are counted, not priced |
| R64 | functional | `ci-minutes` | A CI cost missing any run or job is marked incomplete |
| R65 | functional | `report-comment` | A hook file that does not come from the report's commit is named, not quoted |
| R66 | behavioural | `report-comment` | A pull request's ledger files larger in total than the size bound are refused |
| R67 | behavioural | `report-comment` | Ledger files that the default branch already holds are read by capture's rules |
| R68 | non-functional | `report-comment` | The report runs only for the push that a merge makes to the default branch |
| R69 | non-functional | `report-comment` | A push gets a comment only when all its commits belong to one pull request |
| R70 | non-functional | `report-comment` | The report keeps to a call budget and a time limit |
| R71 | non-functional | `releases-and-compatibility` | Versions are semantic, and their numbers say what an adopter must do |
| R72 | non-functional | `releases-and-compatibility` | A release is not published when its bill of materials is missing or fails a check |
| R73 | non-functional | `project-standards` | Each feature's page matches its spec |
| R74 | non-functional | `project-standards` | Each proposal says how its outcome is validated |
| R75 | functional | `usage-capture` | A subagent's calls are read from its own transcript |
| R76 | functional | `usage-capture` | Capture works on the repository that holds the project directory |
| R77 | non-functional | `ledger` | A model name or attribute value the price table does not list is recorded as unknown |
| R78 | functional | `usage-capture` | A call goes only to a commit in its worktree, on the branch it was recorded on |
| R79 | behavioural | `usage-capture` | Only git's commit subcommand counts as a commit |
| R80 | behavioural | `usage-capture` | A commit is a dry run when a dry-run option is left in effect |
| R81 | behavioural | `usage-capture` | A ledger file holds the new calls of its commit's worktree and branch |
| R82 | behavioural | `usage-capture` | Only a top-level commit in the foreground, after nothing but listed commands, takes a ledger file |
| R83 | behavioural | `usage-capture` | No ledger file is staged for a commit that names its paths |
| R84 | behavioural | `usage-capture` | A commit with nothing to commit and no git add, rm or mv before it takes no ledger file |
| R85 | behavioural | `usage-capture` | No ledger file is staged after a removal or move that may reach the ledger folder |
| R86 | behavioural | `usage-capture` | No ledger file is staged where the ledger path has a filter or a working-tree encoding |
| R87 | behavioural | `usage-capture` | A ledger file whose command is refused at a permission prompt or by a permission rule, blocked, cancelled or interrupted is taken back by a later run |
| R88 | behavioural | `usage-capture` | The registered command runs the hook file only when its checksum matches |
| R89 | behavioural | `usage-capture` | The capture step writes only its own words and numbers to standard error |
| R90 | behavioural | `usage-capture` | The capture step finishes within a time budget |
| R91 | functional | `switch-and-opt-in` | Capture reads the configuration in the working tree |
| R92 | functional | `switch-and-opt-in` | A missing or unreadable configuration file neither turns the tool on nor stops the report |
| R93 | functional | `switch-and-opt-in` | A change to the configuration, the hook file, its registration or a workflow is flagged |
| R94 | functional | `report-comment` | The comment says what its figure is and where it comes from |
| R95 | functional | `report-comment` | The comment counts refused calls and calls that may leave the token cost low |
| R96 | functional | `report-comment` | A report run again updates only its own comment |
| R97 | behavioural | `report-comment` | No text from the pull request or the jobs API is quoted |
| R98 | behavioural | `report-comment` | A ledger line naming a model or attribute value that the price table does not list, other than the value unknown, is refused |
| R99 | non-functional | `releases-and-compatibility` | Every copy of the oldest supported Python agrees with its one source |
| R100 | non-functional | `project-standards` | The register matches the specs, and every requirement is on a feature page |
| R101 | non-functional | `project-standards` | Workflows are checked against the documented permissions, actions and images |
| R102 | behavioural | `report-comment` | A refused ledger line is counted as refused, and no line stops the report |
| R103 | behavioural | `switch-and-opt-in` | Only an absolute XDG folder is read |
| R104 | behavioural | `switch-and-opt-in` | Only an absolute home folder is read |
| R105 | behavioural | `switch-and-opt-in` | The home configuration file decides over the XDG one |
| R106 | behavioural | `switch-and-opt-in` | Only some of git's true values turn capture on |
| R107 | behavioural | `switch-and-opt-in` | A run that finds both switches on notes its time and a fingerprint |
| R108 | behavioural | `switch-and-opt-in` | An interval when both switches were on begins and ends at a run |
| R109 | behavioural | `switch-and-opt-in` | An opt-out ends every session's interval and empties the store |
| R110 | behavioural | `switch-and-opt-in` | Ledger files are taken back and put back whatever the switches say |
| R111 | functional | `usage-capture` | The capture step's git commands stay offline |
| R112 | behavioural | `usage-capture` | An unquoted here-document in or before the commit stages nothing |
| R113 | behavioural | `usage-capture` | Only a ledger file that no run has found in a commit is taken back |
| R114 | behavioural | `usage-capture` | A take-back leaves the file for a later run while the index is in use |
| R115 | behavioural | `usage-capture` | Each take-back is noted |
| R116 | behavioural | `usage-capture` | A ledger file that a take-back removed is put back for a commit that holds it |
| R117 | behavioural | `usage-capture` | A put-back is tried once, and in no other case |
| R118 | non-functional | `usage-capture` | Capture reads both switches before it starts any program |
| R119 | functional | `ledger` | The comment says how many ledger files the pull request restores, removes or changes |
| R120 | functional | `ci-minutes` | Runs that the merge's push starts, and runs on other commits, are not counted |
| R121 | functional | `ci-minutes` | The report finds the pull request's runs with the fewest calls it can |
| R122 | non-functional | `releases-and-compatibility` | The public surface is kept in a manifest |
| R123 | non-functional | `releases-and-compatibility` | The release workflow compares the surface manifest with the previous release's |
| R124 | non-functional | `project-standards` | Each decision has a record of its own, in a fixed form |
| R125 | non-functional | `project-standards` | The index lists every record as the record has it |
| R126 | non-functional | `project-standards` | A decision record names only what exists |
| R127 | non-functional | `project-standards` | No document follows a closed record |
| R128 | non-functional | `project-standards` | A decision record holds plain text |
| R129 | non-functional | `project-standards` | An accepted record changes only to be closed |
| R130 | non-functional | `project-standards` | IDs that the default branch holds stay held or retired |
| R131 | non-functional | `project-standards` | A record and the threats it lists name each other |
| R132 | non-functional | `project-standards` | A removed threat's ID is retired, never used again |
| R133 | non-functional | `project-standards` | The records' folder holds only the records and their index |
| R134 | non-functional | `project-standards` | No attribute hides a record's diff |
| R135 | non-functional | `project-standards` | The assumptions the design rests on are written down |
| R136 | non-functional | `project-standards` | The assumptions with the most at stake come first |
| R137 | non-functional | `project-standards` | The specs and pages use the glossary's words |
| R138 | non-functional | `project-standards` | Each term is defined once |
| R139 | non-functional | `project-standards` | Every version reproduces the golden set |
| R140 | non-functional | `project-standards` | Each fact's check can be followed |
| R141 | non-functional | `project-standards` | A golden figure changes only with the spec that gives it |
| R142 | non-functional | `project-standards` | Each ledger format that a release wrote keeps its golden figures |
| R143 | non-functional | `project-standards` | The assumptions give no other web address |
| R144 | behavioural | `switch-and-opt-in` | A call is inside an interval only when the line it answers and its first line are inside it |
| R145 | non-functional | `switch-and-opt-in` | A run that finds a switch off creates no store and notes no session |
| R146 | behavioural | `switch-and-opt-in` | An opt-out leaves committed ledger files to git |
| R147 | functional | `usage-capture` | A call's repository is told by its working directory alone |
| R148 | functional | `usage-capture` | A start run reads no transcript |
| R149 | non-functional | `usage-capture` | The store keeps only what attribution, deduplication and take-backs need |
| R150 | non-functional | `usage-capture` | The store keeps nothing past its retention window |
| R151 | non-functional | `usage-capture` | A store that holds nothing is removed |
| R152 | non-functional | `usage-capture` | The store is readable and writable by its owner alone |
| R153 | behavioural | `usage-capture` | A removed store lets no earlier call be recorded |
| R154 | non-functional | `usage-capture` | Capture keeps no copy of a transcript |
| R155 | functional | `usage-capture` | A ledger file says when calls of its sessions were left out |
| R156 | non-functional | `ledger` | Each ledger file states its format's version, and each version is published with a schema |
| R157 | functional | `report-comment` | The comment says when the ledger files flag calls left out |
| R158 | behavioural | `report-comment` | The report reads each ledger file by the version it states |
| R159 | non-functional | `project-standards` | The documentation says what stays published after an opt-out and what a hash does not hide |
| R160 | behavioural | `switch-and-opt-in` | Git's own reading of the opt-in can turn capture off, never on |
| R161 | behavioural | `switch-and-opt-in` | A run that began before an opt-out leaves nothing after it |
| R162 | behavioural | `switch-and-opt-in` | A change to the files that hold the opt-in is taken as an opt-out |
| R163 | non-functional | `ledger` | Every version of the ledger format names a call by the same id |
| R164 | non-functional | `project-standards` | The documentation says where an opt-in applies |
| R165 | behavioural | `usage-capture` | A call is placed by the line it answers, whichever run read that line |
| R166 | behavioural | `switch-and-opt-in` | A clock that moves back ends the session's intervals |
| R167 | behavioural | `usage-capture` | Capture reads each ledger file by the version that it states |
| R168 | behavioural | `report-comment` | Ledger files that the default branch already holds are read by the version they state |
| R169 | non-functional | `usage-capture` | Git runs without the session's git variables |
| R170 | non-functional | `usage-capture` | A ledger file's note keeps only what a take-back needs |
| R171 | behavioural | `switch-and-opt-in` | A configuration file with a key that the tool does not know, a key given twice or no `enabled` of `true` or `false` is not valid |
| R172 | functional | `switch-and-opt-in` | The report says when the configuration after the merge does not turn the tool on |

IDs are stable: a requirement keeps its ID while it exists, and a new one takes the next free number, so the rows follow the order in which requirements were added rather than the order of the specs. A requirement that a later change removes leaves the table, and its ID is listed below with the change that removed it, never to be used again.

## Retired IDs

None yet. An entry names the ID and the change that removed it, as in "R7, removed by `change-name`".
