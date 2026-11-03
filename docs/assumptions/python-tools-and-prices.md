# Python, the development tools and prices

The assumptions about Python, about the development tools of this repository, and about the prices that the tool applies. A test may run Python and the development tools, but no test may reach a vendor's prices (DR-090). [The index](README.md) lists every assumption, the most at stake first.

## Python

### A54. The clock of the machine that runs a session agrees with its transcripts and with the runner's day.

- **Rests on it:** R14, R40, R144, R150, T2, T10, T17, T38, T104, T110, DR-044, DR-052, DR-168, DR-175
- **If it is wrong:** Calls near an opt-in or an opt-out would be kept or withheld wrongly (T38, T104), and entries from a machine whose clock runs ahead would be refused as dated after the report's day (T17). A clock that disagreed with the transcripts' times would also move the retention window (T110), so that a note could be dropped while its call can still be recorded, letting a removed ledger file's calls reach the branch again (T2), or a staged ledger file be taken back while its command still runs (T10).
- **Fact:** The clock of the machine that runs a session agrees with the times in its transcripts, and with the day on the runner where the report runs.
  - **Relied on:** R14, R40, R144, R150, T2, T10, T17, T38, T104, T110, DR-044, DR-052, DR-168, DR-175
  - **Checked:** not yet: none will, since the clocks are those of people's machines and GitHub's runners, which no test reads

### A29. Python's isolated mode and its start-up behave as the hook expects.

- **Rests on it:** R12, R13, R32, T14, T15, T28, T56, T68, DR-022, DR-023, DR-027, DR-031, DR-062, DR-125, DR-188
- **If it is wrong:** A module planted beside the hook would run inside it with the person's rights (T15), as it would in the report and the release job (T28, T68). An older Python could print an error where R32 says that it prints nothing (T56), though the command's `; exit 0` would still end it with success (T14).
- **Fact:** `python3 -I` keeps the script's own folder, the current directory and Python's environment variables out of what decides the hook's imports. Without it, Python puts a script's own folder first on its import path.
  - **Relied on:** R12, T15, T28, T68, DR-022, DR-023, DR-062, DR-125, DR-188
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.3 checks it
- **Fact:** Python exits with status 2 when it cannot start as asked, such as for an option it does not know or a script it cannot open.
  - **Relied on:** R13, T14, DR-031
  - **Checked:** not yet: none will, since the registered command's `; exit 0` ends it with success whatever Python returns, which `add-pr-cost-calculator` task 2.3 checks
- **Fact:** Python reads and compiles a whole file before it runs the file's first statement, so a version check at the top is reached only if the file uses no syntax that the older Python lacks.
  - **Relied on:** R32, T56, DR-027
  - **Checked:** not yet: `add-pr-cost-calculator` task 6.5 checks it

### A52. Python's JSON reader and digit matching behave at their edges as the step and the checks expect.

- **Rests on it:** R5, R35, R102, R124, T6, T17, T79, DR-108, DR-109
- **If it is wrong:** A value that is not finite, a boolean read as a count or a line nested too deep could get past the step, or stop the report, where R35 and R102 require a refusal (T17, T6). A decision record numbered in digits from other scripts could pass where only ASCII digits are meant (T79).
- **Fact:** Python's JSON reader turns `NaN`, `Infinity`, `-Infinity` and `1e999` into numbers that are not finite, and turns `true` and `false` into values that pass a check for a whole number.
  - **Relied on:** R5, R35, T6, T17, DR-109
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 and `add-pr-cost-calculator` task 4.2 check it
- **Fact:** Python's JSON reader refuses to read a whole number thousands of digits long.
  - **Relied on:** R35, T17
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.2 checks it
- **Fact:** Python's JSON reader keeps the last of two values given for one field, and raises no error.
  - **Relied on:** R35, T17
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.2 checks it
- **Fact:** Python's JSON reader raises a RecursionError on very deep nesting, and a RecursionError is not a ValueError.
  - **Relied on:** R35, R102, T17
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.2 checks it
- **Fact:** Python's digit matching accepts digits from other scripts as well as ASCII ones: `\d`, `int()` and `str.isdigit()` all do.
  - **Relied on:** R124, T79, DR-108
  - **Checked:** not yet: none will, since were it wrong the check of decision records would only be more careful than it needs to be
  - **Handled by:** `tests/test_decisions.py::test_a_file_not_named_as_a_record_is_reported`

### A53. Files, locks and random names behave alike on every system where a repository's git common directory lives.

- **Rests on it:** R8, R10, R11, R58, R107, R108, R119, R152, R162, T11, T13, T42, T47, T105, T109, T112, T117, T120, DR-017, DR-036, DR-127, DR-169, DR-176
- **If it is wrong:** Two runs could interleave their notes or both record one call, and a killed run could leave a torn store or a lock that stops later runs (T13, T42). A ledger write could leave the repository through a directory junction (T11), and two branches could add one ledger path, so that their merge conflicts or one pull request's usage is read as another's (T13, T47), and a file system that gives an unchanged file other numbers would end every interval at each run that sees it, with a flag for consent (T120).
- **Fact:** The operating system releases a file lock when the process holding it ends, even when that process is killed, on every system and filesystem where a repository's git common directory lives.
  - **Relied on:** R11, T13, T42, DR-036
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 and `add-pr-cost-calculator` task 2.2 check it
- **Fact:** Replacing a file whole with a new one is a single step, so a run killed during the write leaves either the old file or the new one.
  - **Relied on:** R11, T42, DR-036
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it
- **Fact:** A symbolic link is the only way that a folder on a ledger file's path can lead outside the repository.
  - **Relied on:** R10, T11, DR-127
  - **Checked:** not yet: none will, since no task plans a test of it; `add-pr-cost-calculator` task 2.2 plants a symbolic link only
- **Fact:** Random ledger file names never repeat, across clones, branches and machines.
  - **Relied on:** R10, R58, R119, T13, T47, DR-017, DR-127
  - **Checked:** not yet: none will, since no test can draw the names that every clone will draw
- **Fact:** Random ledger file names never collide across every branch and clone that will ever merge, so creating a file only where none of that name exists is enough.
  - **Relied on:** R8, R10, T13, DR-017, DR-127
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it
- **Fact:** Writing a file changes its size or its modification time, or puts a file of another identity in its place, on every file system where a person's git configuration lives, at a resolution fine enough to tell apart two writes that a run comes between.
  - **Relied on:** R107, R108, R162, T105, T117, DR-169
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it in part, on the file systems that CI runs on
- **Fact:** A file that nothing writes keeps its device and inode numbers, size and modification times from one run to the next, on every file system where a person's git configuration lives.
  - **Relied on:** R107, T120, DR-169
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it in part, on the file systems that CI runs on
- **Fact:** On Linux and macOS, a folder created with mode 0700 and a file with mode 0600 can be read only by their owner and an administrator, and Python's standard library can create them so, whatever the umask, without following a symbolic link.
  - **Relied on:** R152, T109, T112, DR-176
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it
- **Fact:** On Windows, `os.lstat` follows neither a symbolic link nor a directory junction, and sets the reparse-point bit of `st_file_attributes` for each.
  - **Relied on:** R152, T112, DR-176
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it

### A66. Later Pythons keep what the tool uses, on every system that adopters use, and each version gets security fixes until its end of life.

- **Rests on it:** R12, R25, R26, DR-023, DR-025, DR-111, DR-134
- **If it is wrong:** A later Python, or another system, that drops or changes what the tool uses would break capture for the adopters who meet it first, and the command's `; exit 0` would hide it. A changed schedule would move when the oldest supported Python should rise.
- **Fact:** Every Python release after 3.11 keeps the standard-library modules and behaviours that the tool uses.
  - **Relied on:** R25, DR-023, DR-025
  - **Checked:** not yet: none will, since no test can run a Python that is not released yet; the CI job that `add-pr-cost-calculator` task 1.11 set up runs the tests on the newest release in every pull request
- **Fact:** The standard library offers what the hook needs on every operating system that adopters use, Windows included.
  - **Relied on:** R12, R25, DR-023, DR-111
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.3 and `add-pr-cost-calculator` task 2.4 check it in part
- **Fact:** A Python version gets security fixes until the end of life that its release schedule sets: 3.10 until October 2026, when it reached its end of life, and 3.11 until about October 2027.
  - **Relied on:** R25, R26, DR-025, DR-134
  - **Checked:** documented: <https://github.com/python/peps/blob/48eba77cd527ac5ac82dd1e092b0430361484a50/peps/pep-0619.rst>, <https://github.com/python/peps/blob/48eba77cd527ac5ac82dd1e092b0430361484a50/peps/pep-0664.rst>, read 2026-11-01

## The development tools

### A22. The test tools can do what the testing decision records ask of them.

- **Rests on it:** T4, T10, T43, T52, DR-024, DR-084, DR-086, DR-087, DR-088, DR-092, DR-098, DR-136
- **If it is wrong:** A secret scanner that refuses a ledger file would fail the agent's commit and push it toward `--no-verify` (T10, T43). Expected failures, coverage, mutation or property tests that cannot do what the decision records ask would leave CI green without meaning it, and weaken the answers to T4 and T52.
- **Fact:** detect-secrets, with its default plugins and filters, raises no finding on a hexadecimal hash whose key ends in `_id`, though it flags such a hash elsewhere.
  - **Relied on:** T10, T43, DR-136
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.2 checks it
- **Fact:** pytest's `xfail` with `strict=True` and the expected error passes a test that fails with that error, and fails a test that passes early or fails for another reason.
  - **Relied on:** DR-084
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.4 checks it
- **Fact:** coverage.py can measure 100% branch coverage of the tool's code, the hook included when a test runs it as `python3 -I` in a process of its own.
  - **Relied on:** DR-086, DR-092
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.5 checks it
- **Fact:** mutmut's gate, which fails CI on a surviving mutant, runs in a time that CI can afford.
  - **Relied on:** DR-087
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.5 checks it in part
- **Fact:** Hypothesis can run derandomised, so that a run repeats exactly, and its property test over planted strings would find any path by which one reaches an output.
  - **Relied on:** T4, T52, DR-088
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.6 checks it in part
- **Fact:** A release tool that writes the changelog from commit messages needs a Node or Go program.
  - **Relied on:** DR-024, DR-098
  - **Checked:** not yet: none will, since it is a reason that DR-098 gives, not something the tool does

### A30. Renovate proposes updates as it is configured to, and its wait catches bad releases.

- **Rests on it:** R26, T28, T35, T64, T66, DR-028, DR-041, DR-111, DR-145
- **If it is wrong:** Updates and vulnerability fixes would stop, arrive before anyone could find a problem in them, or open without the owner's approval (T28, T64, T66), and a malicious release that stays unnoticed past the wait would be proposed like any other, with the owner's review of its diff as the last defence (T35).
- **Fact:** Renovate is installed on the repository and runs.
  - **Relied on:** R26, T28, DR-028, DR-111, DR-145
  - **Checked:** not yet: none will, since Renovate runs on GitHub, which no test may reach
- **Fact:** Renovate waits 14 days after a release before it proposes an update that it can date, and proposes at once an update that it cannot date.
  - **Relied on:** R26, T28, T66, DR-028
  - **Checked:** not yet: none will, since Renovate runs on GitHub, which no test may reach
- **Fact:** Renovate holds a major update on its dependency dashboard, and opens no pull request for it until the owner approves it there.
  - **Relied on:** R26, T64, DR-111
  - **Checked:** not yet: none will, since Renovate runs on GitHub, which no test may reach
- **Fact:** Renovate proposes a fix for a known vulnerability at once, even a major one, without the wait and without approval, once it learns of the vulnerability.
  - **Relied on:** R26, T28, DR-028, DR-111
  - **Checked:** not yet: none will, since Renovate runs on GitHub, which no test may reach
- **Fact:** Each update arrives as a pull request on a branch of its own, and an update of the vendored Superpowers moves the lock's commit and tag together.
  - **Relied on:** T35, T66, DR-041, DR-145
  - **Checked:** not yet: none will, since Renovate runs on GitHub, which no test may reach
  - **Handled by:** `tests/test_repository.py::test_renovate_reads_the_vendored_lock`
- **Fact:** A compromised release is found, and withdrawn, within the 14 days that Renovate waits.
  - **Relied on:** R26, T28, T66, DR-028
  - **Checked:** not yet: none will, since it is about what other people find in their releases, which no test may reach

### A31. Upstream releases and lock files are what they claim to be.

- **Rests on it:** R26, R34, T28, T35, T63, T66, DR-041, DR-042, DR-068, DR-111, DR-126, DR-142
- **If it is wrong:** Code could come in through a pin, a lock or an install that passes every check, and run with the owner's credentials in sessions and CI (T28, T35, T63, T66). Only the owner's review of the diff would stop it.
- **Fact:** A release tag in an upstream repository marks a release that its maintainers published honestly, so a pin that such a tag names can be trusted.
  - **Relied on:** R34, T28, T35, T63, DR-041, DR-068, DR-142
  - **Checked:** not yet: none will, since no test can tell an honest release from another; `add-pr-cost-calculator` task 1.15 checks that each pin names a tagged commit
- **Fact:** The upstream Superpowers repository stays reachable, and its release tag is not moved or removed.
  - **Relied on:** T35, DR-041
  - **Checked:** not yet: none will, since no test may reach GitHub, though CI's comparison of the vendored tree with upstream fails where it does not hold
- **Fact:** Dependencies drop support for older systems only in major versions.
  - **Relied on:** R26, DR-111
  - **Checked:** not yet: none will, since it is about what other projects release, though CI's job on Python 3.11 fails where an update drops that version
- **Fact:** `npm ci` installs exactly the versions that `package-lock.json` holds.
  - **Relied on:** T35, T66, DR-042, DR-126
  - **Checked:** not yet: none will, since no task plans a test of it
- **Fact:** pip with `--require-hashes` installs only what the lock lists, at the listed hashes, while a dependency that no lock holds resolves to its newest release at every install.
  - **Relied on:** T28, T66, DR-042, DR-126
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.8 checks it

### A32. OpenSpec behaves as the checks expect.

- **Rests on it:** R73, R74, R100, T35, DR-024, DR-042, DR-079, DR-105, DR-113, DR-143
- **If it is wrong:** The check of the generated skills could fail with no hand edit made, or pass while a person's settings shaped the skills that agents load (T35), and the documentation checks could fail with nothing wrong in the documents.
- **Fact:** OpenSpec's pinned command-line tool writes the same skills every time it runs, whatever a person's own OpenSpec settings.
  - **Relied on:** T35, DR-042, DR-143
  - **Checked:** not yet: none will, since CI's regeneration of the skills shows only that they match in CI, not under a person's own settings
- **Fact:** OpenSpec keeps the file layout that the documentation checks read.
  - **Relied on:** R73, R74, R100, DR-079
  - **Checked:** not yet: none will, since it is about OpenSpec's later releases, though the documentation checks fail where it does not hold
- **Fact:** OpenSpec asks that each requirement state one behaviour in 500 characters or fewer, measured on its trimmed lines that are not blank, and its validator reports a longer text only as information, even with `--strict`, and only for the main specs.
  - **Relied on:** DR-105, DR-113
  - **Checked:** not yet: none will, since it is about how OpenSpec's later releases treat the limit
- **Fact:** Node is needed only for the OpenSpec command-line tool.
  - **Relied on:** DR-024, DR-042
  - **Checked:** not yet: none will, since no task plans a test of it

### A59. The development tools support Python 3.11, and report code that needs a newer Python.

- **Rests on it:** R25, T55, T56, DR-025, DR-026
- **If it is wrong:** A development tool's update that drops Python 3.11 would force a choice between the tool's floor and its test tools (T56), and code that needs a newer Python, or a newer Python that breaks the tool, could ship unseen (T55).
- **Fact:** The development tools keep supporting Python 3.11.
  - **Relied on:** R25, T56, DR-025
  - **Checked:** not yet: none will, since installing the tools needs the network, which no test uses; the CI job that `add-pr-cost-calculator` task 1.11 set up installs them on Python 3.11 in every pull request
- **Fact:** `actions/setup-python` reads the matrix entry `3.x` as the newest Python release.
  - **Relied on:** R25, T55, DR-026
  - **Checked:** not yet: none will, since it holds on GitHub's runners, which no test may reach
- **Fact:** ruff and mypy, set to Python 3.11, report any code that needs a newer Python.
  - **Relied on:** R25, DR-025
  - **Checked:** not yet: none will, since no task plans a test of it; `add-pr-cost-calculator` task 1.5's branch coverage narrows what it leaves

### A65. Telemetry stays off where its switches say.

- **Rests on it:** T36, DR-071
- **If it is wrong:** Usage statistics, or a sign that a skill was used, would leave sessions and CI despite the switches (T36).
- **Fact:** OpenSpec sends no usage statistics when `DO_NOT_TRACK` is set.
  - **Relied on:** T36, DR-071
  - **Checked:** not yet: none will, since no test may use the network to see what OpenSpec sends
- **Fact:** Superpowers sends nothing about its use when `SUPERPOWERS_DISABLE_TELEMETRY` is set.
  - **Relied on:** T36, DR-071
  - **Checked:** not yet: none will, since no test may use the network to see what Superpowers sends

### A67. The licences allow what is kept here.

- **Rests on it:** R28, DR-099
- **If it is wrong:** A contribution's licence could be disputed, and the repository would hold files that it may not redistribute as they stand.
- **Fact:** A sentence in `CONTRIBUTING.md` is enough to license each contribution under MIT.
  - **Relied on:** R28, DR-099
  - **Checked:** not yet: none will, since it is a question of law, which no test can settle
- **Fact:** The licences of the vendored Superpowers and of OpenSpec, whose generated skills are kept here, allow them to be redistributed in this repository.
  - **Relied on:** R28, DR-099
  - **Checked:** not yet: none will, since it is a question of law, which no test can settle

## Prices

### A33. Model names and list prices mean what the report says they mean.

- **Rests on it:** R17, R77, R94, R98, T1, T27, DR-002, DR-054
- **If it is wrong:** Every call whose model's name differs from the table's would be recorded as `unknown`, counted in tokens and never priced (T1), and a reader on a subscription plan could take the figure for money spent (T27).
- **Fact:** Transcripts name models as the price table does, with names that begin with `claude-`; only a private gateway, a custom model or an alias gives another name.
  - **Relied on:** R17, R77, R98, T1, DR-054
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** What the tokens and minutes would cost at list prices is a meaningful figure for readers, whatever an adopter is actually billed.
  - **Relied on:** R94, T27, DR-002
  - **Checked:** not yet: none will, since no test may reach a vendor's prices

### A55. Anthropic prices each token type at its own rate for each model.

- **Rests on it:** R2, R15, R16, R61, T9, DR-002, DR-020, DR-124, DR-155
- **If it is wrong:** A call billed in a way that the price table cannot express would be priced wrongly without notice (T9), and the cost would be off by however far the billed units differ from the recorded ones.
- **Fact:** Anthropic prices input, output, cache-write and cache-read tokens each at a rate of its own for each model.
  - **Relied on:** R15, DR-020
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** Cache writes come in exactly two lifetimes, five minutes and one hour, each with a rate of its own.
  - **Relied on:** R15, DR-155
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** Some models charge higher rates for a long prompt, and a prompt's length for that purpose counts its input, cache-write and cache-read tokens together.
  - **Relied on:** R16, T9, DR-020, DR-124
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** A multiplier for US-only inference applies to every token type, and fast mode and service tiers have rates of their own.
  - **Relied on:** R16, R61, T9, DR-020, DR-124
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** A web search costs a fee per search on top of its tokens, and a web fetch costs nothing beyond its tokens.
  - **Relied on:** R16, T9, DR-124
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** Reasoning tokens are part of the output tokens and are priced the same.
  - **Relied on:** R15
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** The token counts in a transcript's usage are the units that Anthropic's API bills.
  - **Relied on:** R2, R15, DR-002
  - **Checked:** not yet: none will, since no test may reach a vendor's prices

### A56. Only the facts that the ledger records set a call's price, and prices change rarely and from a given day.

- **Rests on it:** R4, R14, R16, R17, R43, R61, R95, T5, T9, T30, T39, DR-020, DR-045, DR-052, DR-124, DR-135
- **If it is wrong:** A price that depends on anything else could not be computed from the ledger (T9), a known field that starts to carry another charge would be priced at its old meaning (T39), and prices that change often, or at another hour than a day's start, would leave the table stale or a day's calls at the wrong rate (T30, T5).
- **Fact:** Nothing besides a call's token counts, model, price attributes and UTC day changes its price.
  - **Relied on:** R4, R16, R61, T9, DR-045, DR-124
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** A new kind of charge arrives as a new field in a call's usage, never as a new meaning of a field that capture already knows.
  - **Relied on:** R43, R95, T9, T39, DR-135
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** A price changes only between UTC days, so a call's UTC day is all that pricing needs to know of its time.
  - **Relied on:** R14, T5, DR-020, DR-052
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** Anthropic publishes no price API that the report could read instead of a table.
  - **Relied on:** R14, DR-020
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
- **Fact:** Anthropic and GitHub publish their price changes with the day each takes effect, and seldom enough that a table kept by hand stays current.
  - **Relied on:** R14, R17, T30, DR-020, DR-124
  - **Checked:** not yet: none will, since no test may reach a vendor's prices
