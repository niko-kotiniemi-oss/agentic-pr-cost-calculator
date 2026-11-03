# git

The assumptions about git: what its commands, options, attributes, locks and configuration do, and how its releases differ. A test may run git, against repositories on the local disk. [The index](README.md) lists every assumption, the most at stake first.

## A10. A repository's worktrees share one git common directory, which recording can use.

- **Rests on it:** R3, R47, R54, R78, R147, R149, R169, T2, T8, T10, T11, T19, T46, T108, T119, T122, DR-011, DR-012, DR-057, DR-174, DR-179, DR-188
- **If it is wrong:** A nested repository's calls, or those of another repository that the session's environment points git at this one for, could be published here (T2), and the environment could move the store or a staged ledger file into another repository (T119), a worktree's calls could be staged in the main worktree's index and carried to its branch (T19, T8), a git command could trip over the store, so that calls are lost or recorded twice (T10, T11), a take-back could not find a worktree that was moved, so that its staged ledger file waits (T10), a git in a linked worktree outside the repository's folder could be the one that runs (T46), or a clone that another user owns would record after all, which the README's section on adopting the tool that task 4.4 writes says it does not (T122).
- **Fact:** A repository's worktrees share one git common directory, which `git rev-parse --git-common-dir` names, while a repository nested inside its folder has its own.
  - **Relied on:** R3, R47, R147, T2, T11, T108, DR-011, DR-057, DR-179
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 and `add-pr-cost-calculator` task 1.1 check it
- **Fact:** git resolves a directory inside a worktree under the repository's folder to that worktree, not to the main worktree around it.
  - **Relied on:** R78, T8, T10, T19, DR-012
  - **Checked:** not yet: `add-pr-cost-calculator` task 1.1 checks it
- **Fact:** A store kept in its own folder in the git common directory changes nothing that git does, so recording never blocks a change of branch or a rebase.
  - **Relied on:** R47, T10, DR-011
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it
- **Fact:** `git worktree move` keeps a linked worktree's folder in the git common directory, so the worktree keeps its name, and refuses to move the main worktree, which has no such folder.
  - **Relied on:** R149, T10, DR-174
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it
- **Fact:** With every variable whose name begins with `GIT_` removed from its environment, among them `GIT_DIR`, `GIT_COMMON_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` and `GIT_CEILING_DIRECTORIES`, git finds a directory's repository, worktree and index from that directory alone.
  - **Relied on:** R147, R169, T2, T119, DR-179, DR-188
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it
- **Fact:** A linked worktree's `.git` file names its folder in the git common directory, where a `commondir` file names the git common directory, relative to that folder, and a `gitdir` file names the worktree's `.git` file, so that the repository's own files list where each of its worktrees is.
  - **Relied on:** R54, T46, DR-188
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it
- **Fact:** A submodule's checkout, and a working tree whose git folder was moved out of it, as `git init --separate-git-dir` does, have a `.git` file that names their git folder, by a relative path in a submodule, and that folder holds no `commondir` file, since it is the git common directory itself.
  - **Relied on:** R54, T46, DR-188
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it
- **Fact:** `git worktree list` takes the main worktree to be the folder that holds the git common directory when that is named `.git`, and otherwise names the common directory itself, even when it runs in that main worktree, as for a submodule or a working tree whose git folder was moved to a folder of another name, and marks it `(bare)` for a bare repository.
  - **Relied on:** R54, T46, DR-188
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it
- **Fact:** git refuses to name the repository of a folder that another user owns, unless a `safe.directory` setting names it, and `git config` there reads no setting of the repository's own, without an error.
  - **Relied on:** R147, T122, DR-179
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it
- **Fact:** git takes a `safe.directory` setting only from the system's configuration, the person's global configuration and the command line's, which the variables `GIT_CONFIG_COUNT` and `GIT_CONFIG_PARAMETERS` add to, never from the repository's own, so with every variable whose name begins with `GIT_` removed, only the system's file, `~/.gitconfig` and the XDG file can name a folder.
  - **Relied on:** R147, T122, DR-188
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.1 checks it

## A11. git 2.43 stands for every later git.

- **Rests on it:** R32, R52, R110, R113, R117, T2, T8, T10, T45, T56, DR-027, DR-037, DR-055, DR-107, DR-130, DR-154
- **If it is wrong:** A later git that changes index locking, intent-to-add index entries, sparse checkouts or option parsing would still pass the floor, and could make the step disturb work or lose calls (T10, T56, T8), while the README's ways to detect, prevent and recover could lose ledger files or a person's changes (T2).
- **Fact:** The design's account, in its risk of a removed ledger file, of the commands that an untracked or intent-to-add ledger file stops, lets run or drops the index entry of, and of what a crash leaves behind, holds in git 2.43 and every later release.
  - **Relied on:** R52, R110, R113, R117, T2, T8, T10, DR-055, DR-130, `openspec/changes/add-pr-cost-calculator/design.md`
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.4 checks it
- **Fact:** The git behaviour that the design relies on holds in git 2.43 and in every later release, so the CI runner's git and git 2.43 stand for what adopters run, and a version check is enough to refuse a git that behaves otherwise. Reading `GIT_NO_LAZY_FETCH` is the exception that A63 records: a plain git 2.43.0 to 2.43.3 or 2.44.0 does not read it.
  - **Relied on:** R32, T8, T10, T45, T56, DR-027, DR-037, DR-107, DR-154
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.4 and `add-pr-cost-calculator` task 6.5 check it in part

## A12. History, refs and tags behave as the checks expect.

- **Rests on it:** R10, R22, R27, R34, R59, R68, R119, R129, R130, T2, T13, T20, T23, T28, T47, T58, T67, T68, T70, T77, DR-015, DR-022, DR-061, DR-068, DR-121, DR-122, DR-127, DR-131, DR-148, DR-153, DR-156
- **If it is wrong:** A removed ledger file could vanish from the history that the report reads (T20, T77), a tag named like the default branch could take its place (T23, T70), and the README's check of a pin could pass a commit that only a fork holds (T58, T28).
- **Fact:** A file or text that a later commit removes stays in git history, and in clones and forks, so a removal hides nothing that was pushed; only rewriting history removes it.
  - **Relied on:** R22, R129, T2, T20, T77, DR-015, DR-121, DR-153
  - **Checked:** not yet: none will, since it is how git keeps history, which the design takes as given
- **Fact:** Every clone that the decision records' check runs in holds `refs/remotes/origin/main`.
  - **Relied on:** R129, R130, T70, DR-121
  - **Checked:** not yet: none will, since the clones that the check runs in are made outside any test, by people and by CI
  - **Handled by:** `tests/test_decisions.py::test_a_clone_of_one_branch_is_told_how_to_fetch_the_default_branch`
- **Fact:** `refs/remotes/origin/main` names the default branch: the default branch is `main` and the remote is `origin`, in this repository's clones and in the clone where the README's pin check runs.
  - **Relied on:** R129, R130, T58, T70, DR-121, DR-156
  - **Checked:** not yet: none will, since the branch's and the remote's names are set outside any test, by this repository's settings and each person's clone
  - **Handled by:** `tests/test_decisions.py::test_a_default_branch_that_cannot_be_found_is_an_error`
- **Fact:** git resolves a short name to a tag before a branch of the same name, with only a warning, so a tag named like the default branch takes its place unless refs are named in full.
  - **Relied on:** R68, R129, T23, T70, DR-061, DR-121
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.3 checks it
- **Fact:** git allows shell characters in tag names.
  - **Relied on:** R27, T68, DR-148
  - **Checked:** not yet: `add-pr-cost-calculator` task 6.3 and `add-pr-cost-calculator` task 6.1 check it
- **Fact:** A tag can be moved to another commit.
  - **Relied on:** R34, T28, DR-022, DR-068, DR-156
  - **Checked:** not yet: none will, since were it wrong the design would only be more careful than it needs to be
- **Fact:** A commit from inside a merged pull request is in the default branch's history, though the branch never had its state; only the first-parent history holds the states the branch had.
  - **Relied on:** R27, T67, DR-122
  - **Checked:** not yet: `add-pr-cost-calculator` task 6.1 checks it
- **Fact:** A revert of a revert brings back the ledger files that the first revert took off the default branch.
  - **Relied on:** R59, R119, T47, DR-131
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.2 checks it
- **Fact:** Two branches that add to one file conflict when they merge.
  - **Relied on:** R10, T13, DR-127
  - **Checked:** not yet: none will, since were it wrong the design would only be more careful than it needs to be
- **Fact:** `git merge-base --is-ancestor <commit> origin/main` succeeds only for a commit that the default branch's history holds, so it fails for a commit that only a fork holds, whether or not the clone holds that commit.
  - **Relied on:** T58, DR-156
  - **Checked:** not yet: none will, since no task plans a test of it; `add-pr-cost-calculator` task 4.4 writes the check into the README

## A21. The git commands that the step runs start no program that the step did not choose, apart from those that git's configuration names.

- **Rests on it:** R54, T15, T19, T46, T112, DR-188
- **If it is wrong:** A program that git starts would run at every capture run, outside the step's own guard (T15, T46), and one that a command's own options start could change the branch before a commit (T19).
- **Fact:** The git commands that the step itself runs start no other program, except programs that git's configuration names, the person's own or the repository's, such as `core.fsmonitor`, which `git status` and `git add` start, or a clean filter that the repository's `info/attributes` assigns, which `git add` starts, so that whoever can write the git common directory can name one.
  - **Relied on:** R54, T15, T46, T112, DR-188
  - **Checked:** not yet: none will, since no task plans a test of it; `add-pr-cost-calculator` task 2.3 checks only how the step finds git
- **Fact:** git's own options and environment variables in a command can make git start another program, such as `git -c diff.external=<program> diff`, `git -c core.hooksPath=<folder> commit` or `GIT_EDITOR=<program> git commit`, and such a program can change the branch before a commit.
  - **Relied on:** T19
  - **Checked:** not yet: none will, since T19's residual accepts the case

## A40. The options of `git commit` mean what capture takes them to mean.

- **Rests on it:** R49, R79, R80, R83, R84, R85, T8, T10, DR-013, DR-034, DR-035, DR-128
- **If it is wrong:** A spelling or an option that git reads otherwise would mean a missed commit (T8), or a staged ledger file that no commit takes, waiting in the index (T10).
- **Fact:** `git commit` is a dry run when any of `--dry-run`, `--short`, `--porcelain`, `--long`, `-z` and `--null`, in any spelling that git accepts, is still in effect once git has read all of its options, and `--short`, `--porcelain` and `--long` are one setting that the `--no-` form of any of them clears.
  - **Relied on:** R79, R80, T8, T10, DR-035, DR-128
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 and `add-pr-cost-calculator` task 4.4 check it
- **Fact:** No option of `git commit` other than those makes it a dry run.
  - **Relied on:** R80, T10, DR-128
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it in part
- **Fact:** git takes options of its own before its subcommand, so a `-C` before `commit` names a folder, while a `-C` after `commit` names a commit whose message the commit reuses.
  - **Relied on:** R49, R79, T8, T10, DR-013, DR-128
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it
- **Fact:** A `git commit` that names paths commits only those paths, and `-a` adds the changes to tracked files.
  - **Relied on:** R83, R84, T8, T10, DR-034, DR-035
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it
- **Fact:** Pathspec magic such as `:(icase)` lets a git command name the ledger folder in another spelling.
  - **Relied on:** R85, T10, DR-035
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it
- **Fact:** `git rm` refuses to remove a newly staged file and fails the command, also when it is given the file's folder, and a `git mv` of the folder moves the staged file away.
  - **Relied on:** R85, T10, DR-035
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it
- **Fact:** A `git commit` with nothing to commit fails, so a staged ledger file alone would turn a commit that ought to fail into one that succeeds.
  - **Relied on:** R84, T10, DR-035
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it

## A41. Only the attributes and settings that capture knows change what git commits of a ledger file.

- **Rests on it:** R50, R86, T8, T10, DR-014, DR-034, DR-129
- **If it is wrong:** A ledger file could fall out of a commit, or a committed one could hold something other than the entries written, which the report then refuses (T8). A file left behind in the working tree would meet the person's git commands (T10).
- **Fact:** `git add --force` stages a file that an ignore rule matches, and `--sparse` stages one that a sparse checkout leaves out; without them git drops or refuses the file.
  - **Relied on:** R50, T8, T10, DR-014, DR-129
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it
- **Fact:** `git check-attr` reads every attribute file that git reads, the repository's `.gitattributes`, its `.git/info/attributes` and the person's own attributes file among them.
  - **Relied on:** R86, T8, T10, DR-034
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it
- **Fact:** A `filter` attribute, as Git LFS sets, or a `working-tree-encoding` makes git commit something other than the file written.
  - **Relied on:** R86, T8, DR-034
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it
- **Fact:** Only a `filter`, a `working-tree-encoding` or a line-ending conversion can make a committed ledger file differ from the file written.
  - **Relied on:** R86, T8, DR-034
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it in part
- **Fact:** git refuses to add a file where `core.safecrlf` is on and line endings would be converted, and a `.pr-cost/** -text` line in the root `.gitattributes` lets it through unless git ranks above it a line that gives `text` another state.
  - **Relied on:** R50, T8, T10, DR-129
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 and `add-pr-cost-calculator` task 4.4 check it

## A42. git's index lock and staging behave as the design expects.

- **Rests on it:** R47, R110, R114, R115, R116, R117, T8, T10, T13, DR-011, DR-013, DR-014, DR-130
- **If it is wrong:** Two commands could interleave their writes to the index, or a take-back could race a commit in a window that the put-back does not watch, so the step could disturb the person's staging (T10, T13). A lock that a crash left would hold a take-back back until someone removes it, while a staged ledger file waits in the index (T10).
- **Fact:** A plain `git commit` holds no index lock while its `prepare-commit-msg` and `commit-msg` hooks run, so a take-back can remove the ledger file from the index after the commit has taken it.
  - **Relied on:** R110, R115, R116, R117, T8, T10, DR-130
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it
- **Fact:** Two git commands that meet in one worktree fail at the index lock: a command that finds `index.lock` held stops rather than waiting.
  - **Relied on:** R114, T10, T13, DR-013, DR-014, DR-130
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.2 checks it
- **Fact:** A held `index.lock` means that another git command is using the index and will release it, so a run that waits for a free index waits only briefly.
  - **Relied on:** R114, R116, T10, DR-130
  - **Checked:** not yet: none will, since a lock that a crash leaves is never released, and `add-pr-cost-calculator` task 2.2 tests only a lock that a command holds
- **Fact:** The object name of an empty file begins `e69de29` under SHA-1, which is git's default hash.
  - **Relied on:** `add-pr-cost-calculator` task 4.4
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.4 checks it in part
- **Fact:** Staged changes make `git rebase` refuse, and a newly staged file follows `git checkout` to another branch and is taken by `git stash`.
  - **Relied on:** R47, T10, DR-011
  - **Checked:** not yet: none will, since were it wrong the design would only be more careful than it needs to be

## A43. Sparse checkouts behave in git 2.43 as the design describes them.

- **Rests on it:** R52, R113, T8, T10, DR-037, DR-055, DR-107
- **If it is wrong:** If git 2.43 crashed, or damaged an index, in other cases than the README names, a later commit could delete ledger files from the branch with their calls (T8, T10), and the README's way to turn the sparse index off could miss a worktree.
- **Fact:** git 2.43 can crash in a cone-mode `git sparse-checkout` command while any intent-to-add index entry exists, and such a crash can leave `info/sparse-checkout.lock`, or with the sparse index, `index.lock`, behind.
  - **Relied on:** R52, R113, T8, T10, DR-037, DR-107
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.4 checks it
- **Fact:** With the sparse index on, or given `--sparse-index`, such a command in git 2.43 can instead exit with success having written a damaged index, so that the next commit deletes files, ledger files among them, from the branch.
  - **Relied on:** R113, T8, T10, DR-037, DR-107
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.4 checks it
- **Fact:** The sparse index is off unless someone turns it on: `git sparse-checkout` does not turn it on unless it is given `--sparse-index`.
  - **Relied on:** R113, T8, T10, DR-037
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.4 checks it
- **Fact:** `git config --worktree` is refused with more than one worktree while `extensions.worktreeConfig` is off, as in a sparse checkout set up by hand.
  - **Relied on:** R113, T8, T10, DR-037
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.4 checks it
- **Fact:** In a sparse checkout that leaves `.pr-cost/` out, a mixed reset can leave a committed ledger file out of both the index and the working tree, as a removal does.
  - **Relied on:** R52, DR-055
  - **Checked:** not yet: `add-pr-cost-calculator` task 4.4 checks it

## A51. git reads a person's configuration from the files that the step reads, by the rules that the step re-implements.

- **Rests on it:** R37, R38, R39, R103, R104, R105, R106, R107, R109, R118, R160, R162, R164, R169, T3, T38, T41, T105, T120, T121, DR-049, DR-050, DR-168, DR-169, DR-183, DR-185, DR-188
- **If it is wrong:** The step and git would disagree about whether a person opted in, so usage would be published without consent, or not at all (T3), and on Windows the step could read another `.gitconfig` than git does (T41). An opt-out written where neither the step nor git's own reading of the key finds it would be ignored, and calls recorded against the person's wish (T3, T38), and a change to a file that git reads the key from, but that the fingerprint does not name, would go unseen between two runs (T105). A folder's opt-out would reach further or less far than the opt-in's pages say (T121), and the README's account of which writes end an interval would be wrong (T120).
- **Fact:** git reads a person's global configuration from `~/.gitconfig` and its file in the XDG configuration folder, reading the XDG file first and `~/.gitconfig` after it, so `~/.gitconfig` decides where both set a key.
  - **Relied on:** R37, R105, T3, T41, DR-183
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it
- **Fact:** git's configuration syntax is as the step re-implements it: section and key names match in any case, a value loses its quotes and any comment after it, the last value in a file decides, and a key in a subsection or in a comment is not the opt-in key.
  - **Relied on:** R38, T3, DR-049, DR-183
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it in part
- **Fact:** git reads `true`, `yes`, `on`, `1` and a key given with no value as true, reads other numbers such as `2` as true too, reads an empty value as false, and refuses a value such as `maybe`.
  - **Relied on:** R106, T3, DR-049
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it
- **Fact:** git reads a relative `XDG_CONFIG_HOME`, and a relative `HOME`, from its current directory, which can be in a repository's folder.
  - **Relied on:** R103, R104, T3, DR-183
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it
- **Fact:** On Windows, git takes the home folder from `HOME`, and only when `HOME` is not set from `HOMEDRIVE` and `HOMEPATH`, where they name a folder that exists and is not Windows' system folder, and otherwise from `USERPROFILE`.
  - **Relied on:** R104, T3, T41, DR-183
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it in part
- **Fact:** The repository's own git configuration, where a person turns capture off for one repository, is in files that the step can find and read itself without running git.
  - **Relied on:** R39, R109, R118, T3, T38, DR-050, DR-168, DR-188
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it in part
- **Fact:** In a repository, git reads the opt-in key from every file and variable that it reads its settings from, among them the files that those include under the conditions that hold there, in this order: the system's file, the person's XDG file, `~/.gitconfig`, the repository's own files and then the variables, each included file where its include stands, and the last value decides. `git config --type=bool --get-all` lists every value in that order, each as `true` only when git reads it as true, exits with an error when one is not a boolean, and exits with an error, listing nothing, when the key is not set.
  - **Relied on:** R160, T3, T38, DR-183
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it
- **Fact:** `git config --show-origin --get-all` names each file that git reads the opt-in key from in a repository, the files that others include among them, and names a value that a variable gives as given on the command line. With `--null`, it ends each origin and each value with a null byte, and names the main worktree's own file by a path relative to that worktree's top level, as `.git/config`.
  - **Relied on:** R107, R160, R162, T3, T105, DR-169, DR-183
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it
- **Fact:** git matches an `includeIf "gitdir:"` condition against the repository's git folder, which for a linked worktree is a folder in its repository's git common directory, so a condition for a folder does not hold in a linked worktree there whose repository lies elsewhere, and a condition that names the folder through a symbolic link holds for a repository there only when `PWD` names, through that link, the top level of the main worktree that git runs in, and does hold when git runs in a repository whose `.git` is a folder and `PWD` names its top level through the link, while one that names the folder's real path holds wherever git runs.
  - **Relied on:** R160, R164, R169, T121, DR-185, DR-188
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it
- **Fact:** `git config --global` writes one of the person's two global configuration files, and git's advice for a repository that another user owns is to add a `safe.directory` line with it.
  - **Relied on:** T120, DR-169
  - **Checked:** not yet: `add-pr-cost-calculator` task 2.4 checks it

## A63. git can be kept offline and from asking for credentials.

- **Rests on it:** R30, R32, R45, R111, T45, T56, T86, DR-027, DR-060, DR-090
- **If it is wrong:** A run in a partial clone would fetch a missing ledger blob over the network, against R30, and could wait on a credential helper or a slow remote until its budget is spent (T45). The source of a plain git 2.43.0 to 2.43.3 or 2.44.0, which the floor admits, names `GIT_NO_LAZY_FETCH` nowhere, so on those releases this happens (T86).
- **Fact:** In a partial clone, git fetches from the remote an object that a command needs and the clone lacks.
  - **Relied on:** R30, R45, R111, T45, DR-060
  - **Checked:** observed: `tests/test_git_lazy_fetch.py`, 2026-11-01, git, version `git version 2.43.0`, build `1:2.43.0-1ubuntu7.3`
- **Fact:** With `GIT_NO_LAZY_FETCH=1`, git fails a command that needs an object that a partial clone lacks, rather than fetching it.
  - **Relied on:** R30, R45, R111, T45, DR-060, DR-090
  - **Checked:** observed: `tests/test_git_lazy_fetch.py`, 2026-11-01, git, version `git version 2.43.0`, build `1:2.43.0-1ubuntu7.3`
- **Fact:** A plain git 2.43.0 to 2.43.3 or 2.44.0, which the step's floor admits, does not read `GIT_NO_LAZY_FETCH`: its source names the variable in no file, while 2.43.4 and 2.44.1 read it in `promisor-remote.c`, and 2.45.0 in `environment.c`, through a name that `environment.h` defines. The links give each release's file in which the later releases read it; that the earlier ones name it in no file rests on the design's context, since one file cannot show what a whole source leaves out.
  - **Relied on:** R32, R111, T45, T56, T86, DR-027, DR-060
  - **Checked:** documented: <https://github.com/git/git/blob/564d0252ca632e0264ed670534a51d18a689ef5d/promisor-remote.c>, <https://github.com/git/git/blob/3526e67d917bcd03f317a058208fa02737654637/promisor-remote.c>, <https://github.com/git/git/blob/efb050becb6bc703f76382e1f1b6273100e6ace3/promisor-remote.c>, <https://github.com/git/git/blob/0d464a4e6a5a19bd8fbea1deae22d48d14dccb01/promisor-remote.c>, <https://github.com/git/git/blob/3c2a3fdc388747b9eaf4a4a4f2035c1c9ddb26d0/promisor-remote.c>, <https://github.com/git/git/blob/1f2e64e22dee75db96b92d526d14003ba59a154e/promisor-remote.c>, <https://github.com/git/git/blob/10dc9846b82b5f4927d57c6bb657a9352121bebf/promisor-remote.c>, <https://github.com/git/git/blob/786a3e4b8d754d2b14b1208b98eeb0a554ef19a8/environment.c>, <https://github.com/git/git/blob/786a3e4b8d754d2b14b1208b98eeb0a554ef19a8/environment.h>, read 2026-11-01
- **Fact:** `GIT_TERMINAL_PROMPT=0` keeps git from prompting on the terminal, as when it asks for HTTP authentication.
  - **Relied on:** R111, T45, DR-060
  - **Checked:** documented: <https://github.com/git/git/blob/564d0252ca632e0264ed670534a51d18a689ef5d/Documentation/git.txt>, read 2026-11-01
