# GitHub

The assumptions about GitHub: this repository's settings there, and its workflows, events, tokens, API and the way it shows text. No test may reach GitHub (DR-090), so a fact here is documented, or not yet checked, and may name beside its check the test that holds the tool's handling of it. [The index](README.md) lists every assumption, the most at stake first.

## A7. The repository's settings on GitHub are applied, and stay applied, as the threat model's section on the settings the owner keeps lists them.

- **Rests on it:** R27, T28, T33, T35, T37, T61, T62, T64, T67, T68, T76, T100, T132, T133, T142, DR-072, DR-073, DR-074, DR-075, DR-076, DR-077, DR-078, DR-084, DR-089, DR-114, DR-115, DR-119, DR-122, DR-140, DR-141, DR-144, DR-161, DR-203
- **If it is wrong:** Each answer that rests on a setting would fail without any sign: a change could reach `main` without a pull request or `ci`, also from an agent session acting as the owner's account (T62, T64), a release or its tag could change after adopters took it (T67), a workflow that declares no permissions could get a write token (T68), a fork's pull request could run CI before the owner looked at it (T37), two pull requests could take one record's number (T76), a reporter could find no private route (T61), a published release's zip could change after people checked it (T133), and someone could serve another plugin from the address that people added the marketplace by (T142). No test reads a setting on GitHub, so nothing would show that one changed (T100).
- **Fact:** A ruleset that requires branches to be up to date before merging makes a pull request's CI run on what the default branch holds before the pull request merges.
  - **Relied on:** T76, DR-119
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** **Approval for running fork pull request workflows from contributors** is set as the threat model's section on the settings the owner keeps says, and stays so.
  - **Relied on:** T37, T100, DR-078, DR-115, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may read a setting on GitHub
- **Fact:** **The ruleset on `main`** is set as the threat model's section on the settings the owner keeps says, and stays so.
  - **Relied on:** T28, T33, T35, T62, T64, T100, T132, DR-072, DR-084, DR-089, DR-140, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may read a setting on GitHub
- **Fact:** **Branches up to date before merging** is set as the threat model's section on the settings the owner keeps says, and stays so.
  - **Relied on:** T76, T100, DR-119, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may read a setting on GitHub
- **Fact:** **A tag ruleset on every tag** is set as the threat model's section on the settings the owner keeps says, and stays so.
  - **Relied on:** R27, T28, T64, T67, T100, T132, T133, DR-073, DR-122, DR-144, DR-161, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may read a setting on GitHub
- **Fact:** **Immutable releases** is set as the threat model's section on the settings the owner keeps says, and stays so.
  - **Relied on:** T67, T100, T133, DR-074, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may read a setting on GitHub
- **Fact:** **Code-owner review off** is set as the threat model's section on the settings the owner keeps says, and stays so.
  - **Relied on:** T62, T64, T100, DR-075, DR-141, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may read a setting on GitHub
- **Fact:** **Actions' default workflow permissions read-only** is set as the threat model's section on the settings the owner keeps says, and stays so.
  - **Relied on:** T68, T100, DR-076, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may read a setting on GitHub
- **Fact:** **Private vulnerability reporting on** is set as the threat model's section on the settings the owner keeps says, and stays so.
  - **Relied on:** T61, T100, DR-077, DR-114, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may read a setting on GitHub
- **Fact:** **The account's and the repository's names kept** is set as the threat model's section on the settings the owner keeps says, and stays so.
  - **Relied on:** T100, T142, DR-203, `docs/threat-model.md`
  - **Checked:** not yet: none will, since no test may read a setting on GitHub
- **Fact:** GitHub does not let a pull request's author approve it.
  - **Relied on:** T62, T64, DR-075, DR-140, DR-141
  - **Checked:** not yet: none will, since no test may reach GitHub

## A8. Workflows and required checks run when the design expects them to.

- **Rests on it:** R33, R129, T28, T35, T65, T70, T76, DR-043, DR-072, DR-114, DR-119
- **If it is wrong:** A failed, cancelled or skipped job might not block a merge, so the `ci` check would not stand for the jobs before it (T28, T35). A change of a pull request's base, title or body that sends no event, or whose event carries stale text, would go unchecked until the next event (T70, T65).
- **Fact:** A required check that never runs never reports, so a pull request that requires it waits for good.
  - **Relied on:** DR-043, DR-072
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** A job with `if: always()` runs even when a job that it needs has failed, so a last job that fails unless each job it needs succeeded can stand for all of them as the one required check.
  - **Relied on:** T28, T35, DR-043, DR-072
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 1.7 tests only what this repository does with it
- **Fact:** GitHub runs a pull request's CI again when the pull request is pushed to, not when its base branch moves on.
  - **Relied on:** T76, DR-119
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** GitHub reports a change of a pull request's base and an edit of its title or description as one `edited` event, so a workflow that runs on `edited` runs again when the base changes.
  - **Relied on:** R129, T70
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** A pull request's `opened`, `edited`, `reopened` and `synchronize` events carry its current title and body, and a change to the title or body sends one of them.
  - **Relied on:** R33, T65, DR-114
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 1.14 tests only what this repository does with it

## A9. GitHub shows text as the checks expect, and text posted on GitHub is public at once.

- **Rests on it:** R21, R33, R97, R98, R128, R134, R176, R198, R200, T26, T52, T61, T65, T73, T79, T81, T125, T126, T145, T147, T151, DR-044, DR-108, DR-114, DR-115, DR-152, DR-195, DR-213
- **If it is wrong:** Text shown as code could still render as a link, an image or a mention, and a log line could be read as a workflow command (T26, T52). A decision record could read one way to a reviewer and another way to an agent, or be collapsed and merged unread (T73, T79, T81), and a bug report opened without the form would never meet its privacy checkbox (T61, T65). A spec could read one way to its reviewers and another to an agent (T125), and the check of the specs' form could print a line that CI reads as a command (T126). The README's detail could show in full, so that its short start no longer comes first, or stay out of a reader's reach (T145), and if GitHub showed an HTML comment, or a drawn code block's text, as the raw file holds it, the README's test that refuses them would refuse more than it needs to (T151). If GitHub showed the root's README on the repository's page where the `.github` folder holds one, the README's test that refuses such a file would refuse more than it needs to (R198, T147).
- **Fact:** GitHub shows text inside inline code in a comment or a job summary as code, never as a link, an image or a mention.
  - **Relied on:** R21, T26, T52, DR-044
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** GitHub reads a line of a job's log that has the form of a workflow command, such as `::error::`, as a command.
  - **Relied on:** R97, R98, T52, T126, DR-044
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 4.1 tests only what this repository does with it
- **Fact:** GitHub hides an HTML comment when it shows a file.
  - **Relied on:** R128, R176, R200, T73, T125, T151, DR-152, DR-195, DR-213
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** GitHub shows text between dollar signs as a mathematical expression, and text between one or two tildes struck through, in a Markdown file as in a pull request.
  - **Relied on:** R176, R200, T125, T151, DR-195
  - **Checked:** documented: <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions>, <https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax>, read 2026-11-09
- **Fact:** GitHub shows the Markdown inside a `<details>` element collapsed, under its `<summary>`, until a reader clicks to expand it, and open from the start only when the element has the `open` attribute.
  - **Relied on:** R200, T145, DR-213
  - **Checked:** documented: <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections>, read 2026-11-10
- **Fact:** GitHub draws a fenced code block whose language is `mermaid`, `geojson`, `topojson` or `stl` as a diagram, a map or a model, and one whose language is `math` as a mathematical expression.
  - **Relied on:** R200, T151
  - **Checked:** documented: <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams>, <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions>, read 2026-11-11
- **Fact:** GitHub hides a footnote's definition that nothing refers to, and raw HTML that is not an element, such as a processing instruction, a declaration or a CDATA section, as it hides a comment.
  - **Relied on:** R200, T151
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** Where a repository holds a README in its `.github` folder, GitHub shows that one on the repository's page in place of the one at its root.
  - **Relied on:** R198, T147
  - **Checked:** documented: <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes>, read 2026-11-11
- **Fact:** A record kept to the plain-text subset shows on GitHub every word that an agent reads in the raw file.
  - **Relied on:** R128, T73, T79, DR-152
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** A spec kept to the text that DR-195 allows shows on GitHub every word that OpenSpec and an agent read in the raw file.
  - **Relied on:** R176, T125, DR-195
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** Only the `binary`, `diff` and `linguist-generated` attributes, set in the repository's own attribute files, make git show a record's diff as binary or GitHub hide it.
  - **Relied on:** R134, T81, DR-108
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** Text posted on GitHub, such as a pull request's or an issue's, is public the moment it is posted, before any check can read it.
  - **Relied on:** R33, T61, T65, DR-114, DR-115
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** With blank issues turned off, every issue starts from a template, so every bug report meets the form's privacy checkbox.
  - **Relied on:** T61, DR-115
  - **Checked:** not yet: none will, since no test may reach GitHub

## A27. Tags and releases can be protected from change.

- **Rests on it:** R27, R28, R68, R72, R189, T23, T28, T29, T64, T67, T69, T132, T133, T139, DR-061, DR-073, DR-074, DR-097, DR-144, DR-161, DR-209
- **If it is wrong:** An identity with `contents: write`, such as an agent session acting as the owner's account, could publish a release on an unreviewed commit, or change one after adopters took it (T67, T64, T28). A tag named like the default branch could pass the report's check of the event (T23, T29), and the bill of materials could list parts that a release's archive does not hold (T69). A release could be published before its files are attached, or its zip replaced after people checked it (T139, T133).
- **Fact:** A push of a tag has a `github.ref` that begins `refs/tags/`, while its `github.ref_name` is the tag's name alone, so a tag named like the default branch shares the branch's `github.ref_name` but not its `github.ref`.
  - **Relied on:** R68, T23, T29, DR-061
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 4.3 tests only what this repository does with it
- **Fact:** Any identity with `contents: write` can create a release and its tag through the API, with no workflow at all and with a tag of any name.
  - **Relied on:** T64, T67, DR-073, DR-144, DR-161
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** A tag ruleset that covers every tag also governs a tag that GitHub's releases API creates, so an identity with `contents: write` cannot create a release with a new tag without the ruleset's bypass.
  - **Relied on:** R27, T28, T64, T67, T132, T133, DR-073, DR-144, DR-161
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** GitHub's immutable releases stop a published release from changing and its tag from moving.
  - **Relied on:** T67, T133, T139, DR-074
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** GitHub publishes a release when it is created, unless it is created as a draft, and attaches a release's files by calls of their own after that.
  - **Relied on:** R189, T139, DR-209
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 6.3 tests only the order of the workflow's calls, against recorded responses
- **Fact:** GitHub's source archive of a release holds the vendored and generated parts.
  - **Relied on:** R28, R72, T69, DR-097
  - **Checked:** not yet: none will, since no test may reach GitHub

## A18. A merge into the default branch makes one push, and that push starts the adopter's calling workflow.

- **Rests on it:** R19, R27, R58, R62, R68, R69, R93, R120, R129, T19, T20, T21, T22, T23, T50, T67, T68, T70, T88, DR-005, DR-017, DR-018, DR-019, DR-051, DR-061, DR-073, DR-092, DR-121, DR-122, DR-133, DR-147, DR-148, DR-186
- **If it is wrong:** A merge that makes no push, or whose push starts no workflow, would get no report, and nothing would say why (T21, T23). A push that named another commit as the one it replaced would make the report count the wrong ledger files as the merge's own (T19, T20), and a run that a merge starts through another event, created before the merge time, would be counted as the pull request's, so the CI figure would be too high without saying so (T22, T88).
- **Fact:** Every merge into the default branch, by hand, by auto-merge or through a merge queue, makes a push to that branch, and that push starts the adopter's calling workflow.
  - **Relied on:** R19, R58, R68, R69, T19, T21, T23, DR-005, DR-018, DR-061, DR-092, DR-133, DR-147
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** An event that `GITHUB_TOKEN` causes, such as the push of a merge that a workflow makes, creates no new workflow run, apart from `workflow_dispatch`, `repository_dispatch` and some `pull_request` events, so such a merge gets no report.
  - **Relied on:** R68, T50, DR-018
  - **Checked:** documented: <https://github.com/github/docs/blob/33b1f4a6fec2d9b6fd3d374afa56bcd9f0875b57/data/reusables/actions/actions-do-not-trigger-workflows.md>, read 2026-11-01
- **Fact:** The push that a merge makes names, as the commit it replaced, the default branch just before the merge, and its own commit is the default branch just after it.
  - **Relied on:** R19, R58, R129, T19, T20, T70, DR-017, DR-121
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** GitHub creates a workflow run that a merge starts through an event other than its push, such as the pull request's `closed` event, no earlier than the pull request's merge time. Its documentation does not order the two times.
  - **Relied on:** R62, R120, T22, T88, DR-019, DR-147
  - **Checked:** not yet: none will, since none of this repository's own workflows runs on such an event, so its own merges cannot check this
- **Fact:** A push, of a branch or of a tag, runs the workflow files as the pushed commit holds them: a pull request's merge runs the calling workflow as the pull request left it, and a tag runs the release workflow as the tagged commit holds it.
  - **Relied on:** R19, R27, R93, T21, T67, T68, DR-051, DR-073, DR-122, DR-148, DR-186
  - **Checked:** not yet: none will, since no test may reach GitHub

## A19. A reusable workflow runs with its caller's context, and with only the token and the secrets that its caller gives it.

- **Rests on it:** R24, R30, R65, R93, R96, R101, T21, T23, T24, T25, T28, T29, T54, T57, T60, DR-006, DR-016, DR-044, DR-062, DR-063, DR-090, DR-102, DR-117, DR-132, DR-139, DR-186
- **If it is wrong:** The report could run the caller's code instead of its own, with a token that can write (T23), or reach a token or secrets beyond those it declares (T24, T29). If its three permissions were not enough, every adopter's report would fail, and if the API's host could be pointed elsewhere, the token could go there (T24).
- **Fact:** A reusable workflow gets its caller's `GITHUB_TOKEN`, with the permissions that the calling job grants or else the default ones, and the secrets that the caller passes it, all of them with `secrets: inherit`.
  - **Relied on:** R24, T24, T29, DR-063, DR-132
  - **Checked:** documented: <https://github.com/github/docs/blob/33b1f4a6fec2d9b6fd3d374afa56bcd9f0875b57/content/actions/reference/workflows-and-actions/reusing-workflow-configurations.md>, <https://github.com/github/docs/blob/33b1f4a6fec2d9b6fd3d374afa56bcd9f0875b57/content/actions/how-tos/reuse-automations/reuse-workflows.md>, read 2026-11-01
- **Fact:** In a reusable workflow on GitHub.com, `job.workflow_repository` and `job.workflow_sha` name the reusable workflow's own repository and commit, not the caller's, and the caller cannot set them.
  - **Relied on:** R24, R65, T23, T28, T54, T60, DR-006, DR-062, DR-132, DR-139
  - **Checked:** not yet: none will, since no test may reach GitHub, and at `add-pr-cost-calculator` task 7.1 this repository calls its own workflow, so that the caller's repository and commit are the workflow's own
- **Fact:** GitHub Enterprise Server lacks the `job` context values that the report relies on.
  - **Relied on:** DR-006
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** The report's three permissions, `contents: read`, `actions: read` and `pull-requests: write`, are enough for every call it makes: fetching history and `refs/pull/<number>/head`, looking up pull requests, listing runs and job attempts, and posting and updating its comment.
  - **Relied on:** R24, T24, T29, DR-016, DR-063
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** `GITHUB_API_URL` names GitHub's API host, and a calling workflow cannot point it elsewhere.
  - **Relied on:** R30, T24, DR-090
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 1.13 tests only what this repository does with it
- **Fact:** Every workflow in a repository that uses `GITHUB_TOKEN` posts comments under one identity, so a comment's author tells the report's comment from a person's but not from another workflow's.
  - **Relied on:** R93, R96, T21, T25, DR-044, DR-186
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 4.1 tests only what this repository does with it
- **Fact:** GitHub runs workflow files that end in `.yml` or `.yaml`, and a job's token gets the permissions of its own block or, without one, of its workflow's.
  - **Relied on:** R101, T57, DR-102, DR-117
  - **Checked:** not yet: none will, since no test may reach GitHub

## A20. Checkouts and GitHub's hosted runners are what the workflows expect.

- **Rests on it:** R23, R24, R25, R27, T22, T23, T24, T68, DR-019, DR-023, DR-062, DR-067, DR-076
- **If it is wrong:** The report would fail on a runner without a suitable `python3`, and the tools on a runner that is not trustworthy would be exposed to the release job's token and the report's (T68, T23, T24).
- **Fact:** `actions/checkout` fetches one commit unless it is asked for more.
  - **Relied on:** R23, T22, DR-019
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 4.3 tests only what this repository does with it
- **Fact:** The runner that runs the report has a `python3` at or above the supported floor, since the report runs with `python3 -I` and no step installs Python for it.
  - **Relied on:** R24, R25, DR-023, DR-062
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** GitHub's hosted runners, and the `python3` and `git` installed on them, are trustworthy, though nothing pins the runner image.
  - **Relied on:** R24, R27, T23, T24, T68, DR-067, DR-076
  - **Checked:** not yet: none will, since no test may reach GitHub

## A48. A pull request's commits stay findable after every merge method.

- **Rests on it:** R23, R62, R64, R120, R201, T22, T147, DR-019, DR-038, DR-110, DR-215
- **If it is wrong:** A head ref that went missing marks the CI cost incomplete, as designed, but one that named other commits, or runs that named the test merge commit, would make the report count the wrong runs or miss them, without saying so (T22). If git did not fetch a fork's head under this repository's address, the README's test that refuses a pull request's ref would refuse more than it needs to (T147).
- **Fact:** A pull request's head stays fetchable by git as `refs/pull/<number>/head` after the merge, for a pull request from a fork too, and names the pull request's last head.
  - **Relied on:** R23, R62, R64, R120, R201, T22, T147, DR-019, DR-038, DR-110, DR-215
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** Commits that a force-push removed from a pull request are no longer in `refs/pull/<number>/head`, so CI runs on them are not counted.
  - **Relied on:** R62, T22, DR-019
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** A squash merge puts one new commit on the default branch and GitHub's rebase merge always makes new commits, so neither brings to the default branch the commits that CI ran on.
  - **Relied on:** R62, R120, T22, DR-019
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** A `pull_request` run names the pull request's head commit as its head commit, not the test merge commit, so listing each of the pull request's commits finds its runs.
  - **Relied on:** R62, T22, DR-019, DR-038
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request

## A26. Runs for a pull request from a fork get no secrets, and run the code that its author chose.

- **Rests on it:** R27, R34, R68, R201, T37, T58, T63, T95, T147, DR-018, DR-068, DR-078, DR-115, DR-122, DR-156, DR-215
- **If it is wrong:** A secret added later could be read by a fork's pull request (T37), and pull requests from forks would get no report if their merge's push ran elsewhere. If GitHub did not run an action pinned to a commit that only a fork holds, or serve one under this repository's address, the defences against such commits, the README's refusal of a commit's ID among them, would be more than needed (T58, T63, T147), and if it served under a repository's address nothing else that others write, the README's test would refuse more addresses there than it needs to (R201, T147).
- **Fact:** Apart from `GITHUB_TOKEN`, GitHub passes no secrets to a run that a pull request from a fork triggers.
  - **Relied on:** T37, DR-078
  - **Checked:** documented: <https://github.com/github/docs/blob/33b1f4a6fec2d9b6fd3d374afa56bcd9f0875b57/data/reusables/actions/forked-secrets.md>, read 2026-11-01
- **Fact:** A pull request from a fork runs this repository's CI with code that its author chose.
  - **Relied on:** T37, DR-078, DR-115
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** The push that merging a fork's pull request makes belongs to the base repository and runs its workflows there.
  - **Relied on:** R68, DR-018
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** GitHub serves a commit that only a fork holds under the parent repository's address, and resolves a commit id in `uses:` across the fork network, so it runs an action pinned to such a commit.
  - **Relied on:** R27, R34, R201, T58, T63, T95, T147, DR-068, DR-122, DR-156, DR-215
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** GitHub serves under a repository's address what others write there too: an issue, which anyone who can read the repository can open, a pull request from a fork, which its author opens on the original repository, and a comparison of its branch with a fork's.
  - **Relied on:** R201, T147, DR-215
  - **Checked:** documented: <https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue>, <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork>, <https://docs.github.com/en/pull-requests/committing-changes-to-your-project/viewing-and-comparing-commits/comparing-commits>, read 2026-11-11

## A28. GitHub, and this repository's place on it, stay as they are.

- **Rests on it:** R24, R34, T63, T142, T147, T148, DR-062, DR-068, DR-090, DR-092, DR-096, DR-114, DR-118, DR-132, DR-147, DR-157, DR-203
- **If it is wrong:** The check of pins could not tell a tagged commit from one that only a fork holds (T63). A change in GitHub's API would skew the report in adopters' CI while every test passes, and a repository made private or renamed would break the adopters who call its workflow, and would leave the people who added the marketplace, and the README's addresses, on an address that someone else can take (T142, T147, T148).
- **Fact:** CI can read the source of each action and container image that a workflow uses, to list the tags that name a pin.
  - **Relied on:** R34, T63, DR-068
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** GitHub's API keeps the shape that the recorded responses hold, so tests against recordings and one live run, at the merge of the pull request that does `add-pr-cost-calculator` task 7.1, stand for what adopters' CI will meet.
  - **Relied on:** DR-090, DR-092, DR-147
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** This repository stays public, so any repository's workflow can call its reusable workflow and check out its code, and its whole history gives CI nothing it could not already read.
  - **Relied on:** R24, DR-062, DR-114, DR-132, DR-157
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** Renaming this repository would break adopters' references to its reusable workflow, since GitHub's redirect for a renamed repository is taken not to carry `uses:` references.
  - **Relied on:** DR-096, DR-118
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** When an account or a repository on GitHub is renamed, its old address leads to the new one only until someone takes the old name, and then leads to theirs.
  - **Relied on:** T142, T147, T148, DR-203
  - **Checked:** not yet: none will, since no test may reach GitHub

## A35. GitHub enforces the permissions a workflow declares, gives runs from forks a read-only token, and gives a reusable workflow its caller's event, as its documentation says.

- **Rests on it:** R24, R68, T23, T24, T29, T37, DR-005, DR-016, DR-018, DR-061, DR-063, DR-067, DR-078, DR-115, DR-132
- **If it is wrong:** A token could hold more than the report declares, as through an adopter's broad grant (T24, T29), a fork's pull request could write through CI (T37), and the report's own check of the event would read the wrong event, so it could refuse every merge or let another event through (T23).
- **Fact:** GitHub enforces the permissions that a workflow declares, setting each one that it does not declare to `none`, and a reusable workflow can narrow, but not widen, the permissions that its caller passes it.
  - **Relied on:** R24, T24, T29, DR-016, DR-063, DR-132
  - **Checked:** documented: <https://github.com/github/docs/blob/33b1f4a6fec2d9b6fd3d374afa56bcd9f0875b57/data/reusables/actions/github-token-scope-descriptions.md>, <https://github.com/github/docs/blob/33b1f4a6fec2d9b6fd3d374afa56bcd9f0875b57/content/actions/reference/workflows-and-actions/reusing-workflow-configurations.md>, read 2026-11-01
- **Fact:** A workflow run for a pull request from a fork gets a `GITHUB_TOKEN` with read-only permissions.
  - **Relied on:** T37, DR-018, DR-067, DR-078, DR-115
  - **Checked:** documented: <https://github.com/github/docs/blob/33b1f4a6fec2d9b6fd3d374afa56bcd9f0875b57/data/reusables/developer-site/pull_request_forked_repos_link.md>, read 2026-11-01
- **Fact:** A reusable workflow's `github` context is always its caller's, so it names the event that triggered the caller.
  - **Relied on:** R68, T23, T29, DR-005, DR-061, DR-132
  - **Checked:** documented: <https://github.com/github/docs/blob/33b1f4a6fec2d9b6fd3d374afa56bcd9f0875b57/content/actions/reference/workflows-and-actions/reusing-workflow-configurations.md>, read 2026-11-01

## A49. GitHub's lookup of the pull requests associated with a commit behaves as documented: for a commit on the default branch, it gives the merged pull request that introduced the commit.

- **Rests on it:** R69, R70, T19, T88, DR-018, DR-133
- **If it is wrong:** The report's rule that a push whose commits do not all belong to one pull request gets no comment rests on it (T19). If the lookup gave another pull request, or none, a push could be charged to the wrong pull request or lose its comment, while a test that replays GitHub's answer still passes (T19, T88).
- **Fact:** For a commit that the default branch holds, GitHub's "List pull requests associated with a commit" returns the merged pull request that introduced it.
  - **Relied on:** R69, R70, T19, T88, DR-018, DR-133
  - **Checked:** documented: <https://github.com/github/docs/blob/33b1f4a6fec2d9b6fd3d374afa56bcd9f0875b57/src/rest/data/fpt-2022-11-28/commits.json>, read 2026-11-01
- **Fact:** GitHub's lookup of the pull requests associated with a commit finds the pull request for the commits that every merge method puts on the default branch: a merge commit, a squash, a rebase merge and a fast-forward.
  - **Relied on:** R69, T19, DR-133
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** One push to the default branch can merge several pull requests, as a merge queue can, or add commits that belong to no pull request.
  - **Relied on:** R69, T19, DR-133
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 4.1 tests only what this repository does with it

## A50. GitHub's runs and jobs API gives complete, timed listings, within known limits.

- **Rests on it:** R18, R21, R24, R62, R63, R64, R70, R94, R120, R121, T22, T27, T51, DR-015, DR-017, DR-019, DR-020, DR-038, DR-039, DR-044, DR-063, DR-110
- **If it is wrong:** Job attempts after the first, unfinished jobs or listings cut short without a sign would make the CI cost too low, or price it as if whole, while the comment shows it as complete (T22, T51). The call budget would be set against the wrong limits (T51), and once runs expire, a report's CI figures could not be recomputed (T27).
- **Fact:** GitHub lists a repository's runs per commit, or filtered by event and by creation time, and each run names the event and branch that started it, so runs that a push to the default branch started can be told apart.
  - **Relied on:** R62, R120, R121, T22, T51, DR-019, DR-039, DR-110
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** GitHub's jobs API gives each job's start and end times with the default `GITHUB_TOKEN` and `actions: read`, whichever way the pull request merged.
  - **Relied on:** R18, R24, R62, T22, DR-038, DR-063, DR-110
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** The jobs API lists only the latest attempt of each job unless it is asked for all of them, and lists every attempt when asked.
  - **Relied on:** R62, T22, DR-038, DR-110
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request
- **Fact:** The jobs API gives a job that has not finished no end time.
  - **Relied on:** R64, T22, DR-038
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 3.3 tests only what this repository does with it
- **Fact:** GitHub's per-run billable timing cannot be relied on to give the minutes that a run used.
  - **Relied on:** DR-038
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** The jobs API gives each job's runner labels, from which the runner type that the price table is keyed on can be read.
  - **Relied on:** R18, R21, R63, DR-020, DR-038, DR-044
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 3.3 tests only what this repository does with it
- **Fact:** `GITHUB_TOKEN`'s rate limit is 1,000 requests per hour per repository, and every workflow in the repository draws on it.
  - **Relied on:** R70, T51, DR-039
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** A filtered listing of a repository's workflow runs returns at most 1,000 runs.
  - **Relied on:** R121, T22, T51, DR-039
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 3.3 tests only what this repository does with it
- **Fact:** A runs listing that GitHub cut short can be told apart from a whole one.
  - **Relied on:** R64, T22, T51, DR-039, DR-110
  - **Checked:** not yet: none will, since no test may reach GitHub; `add-pr-cost-calculator` task 3.3 tests only what this repository does with it
- **Fact:** GitHub's lists of a pull request's files and commits return at most 3000 files and 250 commits.
  - **Relied on:** R62, T22, DR-017, DR-019
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** GitHub keeps the runs and job timings that a report used listable long enough for the report's CI figures to be recomputed later.
  - **Relied on:** R94, T27, DR-015, DR-020, DR-038
  - **Checked:** not yet: `add-pr-cost-calculator` task 7.1 meets it once, at the merge of that task's own pull request

## A64. GitHub bills job minutes from job times.

- **Rests on it:** R18, R63, T27, DR-002, DR-020, DR-038, DR-110
- **If it is wrong:** The CI figure would differ from what GitHub charges, in one direction in every report (T27).
- **Fact:** GitHub charges each job its duration rounded up to a whole minute, at a rate per minute set by the runner type and the day.
  - **Relied on:** R18, DR-038, DR-110
  - **Checked:** not yet: none will, since no test may reach GitHub
- **Fact:** GitHub bills each job attempt by its duration rounded up to a whole minute, at a published per-minute list rate for its runner type, so job times reproduce the list-rate cost.
  - **Relied on:** R18, R63, T27, DR-002, DR-020, DR-038, DR-110
  - **Checked:** not yet: none will, since no test may reach GitHub's bill; `add-pr-cost-calculator` task 3.3 tests only the arithmetic
