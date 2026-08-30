# TASK-01: Git Exercises

All 23 exercises from [Git Exercises](https://gitexercises.fracz.com/) completed
and were verified (`git verify`). Completion screenshot: `completion-screenshot.png`.

Going in, I thought this would be a practice on commands.
It turned into something closer to an archaeology dig through Git's internals
 `reflog`, `fsck`, `bisect`  and honestly `git verify` gave me a reality check.

Below, for each exercise , the objective, the commands I actually used, why
they were right , and where it wasn't smooth,what went wrong
first and how I found my way to the fix.

---

## 1. Getting Started

### Commands Used
```bash
git start
git start master
git verify
```
 `git start` sets up the exercise environment; `git start master` does it explicitly for the warm-up exercise on `master`;
 `git verify` checks thesolution against the server before moving on to the next one.

---

## 2. Commit One File

Two files were present in the working directory,but only one needed committing.

### Commands Used
```bash
git add A.txt
git commit -m "Add A.txt"
git verify
```
 `git add A.txt` stages only that file,leaving the other untouched,and the commit that follows includes just that change.

---

## 3. Commit One File of Two Currently Staged

Both files were already staged, the goal was to commit only one of them.

### Commands Used
```bash
git reset B.txt
git commit -m "Add A.txt"
git verify
```
 `git reset B.txt` unstages it without touching the working directory, so the following commit only includes `A.txt`.

---

## 4. Ignore Them

### Commands Used
```bash
echo "*.exe" > .gitignore
echo "*.o" >> .gitignore
echo "*.jar" >> .gitignore
echo "libraries/" >> .gitignore
git add .gitignore
git commit -m "Add gitignore"
git verify
```
 Adds rules so compiled/binary files and the `libraries/` directory are never tracked, then commits the `.gitignore` itself.

**What went wrong first:** my initial `.gitignore` was created with `touch` completely empty,with no actual ignore rules in it. Verification failed until I realise the file needs content.

---

## 5. Chase Branch

Objective: bring missing work from another branch (`escaped`) into the
current one.

### Commands Used
```bash
git reset --hard escaped
git verify
```
 The current branch had no work of its own yet,so hard-resetting onto  `escaped` was enough to bring it fully up to date.

---

## 6. Merge Conflict

### Commands Used
```bash
git merge another-piece-of-work
# conflict in equation.txt
echo "2 + 3 = 5" > equation.txt
git add equation.txt
git commit -m "Resolve merge conflict"
git verify
```
 The merge left `equation.txt` with conflicting content from both branches;
 resolving it meant writing the correct value by hand,staging it,and completing the merge commit.

---

## 7. Save Your Work

Objective: stash unfinished work, fix an urgent bug, then restore and finish the original work.

### Commands Used
```bash
git stash
sed -i '/THIS IS A BUG/d' bug.txt
git add bug.txt
git commit -m "Fix bug"
git stash pop
echo "Finally, finished it!" >> bug.txt
git add bug.txt program.txt
git commit -m "Finish work"
git verify
```
 `git stash` sets the in-progress changes aside so the working tree is
clean for the urgent fix; `git stash pop` brings them back afterward to
finish.

**What went wrong first:** it took a couple of tries ,I initially stashed the wrong thing and committed at the wrong point, which `git verify` caught. The actual fix was to delete the line marked `THIS IS A BUG` outright, not
just append more text near it.

---

## 8. Change Branch History

Objective: replace a bad commit with the actual fix that exists on another
branch.

### Commands Used
```bash
git switch change-branch-history
git reset --hard HEAD~1
git rebase hot-bugfix
git verify
```
 Dropped the bad commit with `reset --hard HEAD~1`, then rebased onto `hot-bugfix` so its fix replaced it in the history.

**What went wrong first:** I tried `git cherry-pick hot-bugfix` directly, which clearly did not work. Aborting it and using reset + rebase instead worked.
cleanly, since it replays from a shared ancestor rather than a diverged one.

---

## 9. Remove Ignored

### Commands Used
```bash
git rm --cached ignored.txt
git commit -m "Stop tracking ignored.txt"
git verify
```
 `--cached` untracks the file without deleting it on disk, since it's now meant to be covered by `.gitignore` instead.

---

## 10. Case-Sensitive Filename

### Commands Used
```bash
git mv File.txt file.txt
git commit -m "Rename file"
git verify
```
 `git mv` records the rename explicitly, which matters on case-sensitive filesystems where a plain OS-level rename can confuse Git about whether this is an add/delete or a rename.

---

## 11. Fix Typo

### Commands Used
```bash
sed -i 's/wordl/world/' file.txt
git add file.txt
git commit --amend -m "Add Hello world"
git verify
```
The typo was in the most recent commit, so `commit --amend` fixes both the content and the message in place rather than adding a new commit on top.

---

## 12. Forge Date

### Commands Used
```bash
GIT_COMMITTER_DATE="1987-08-21 12:00:00" git commit --amend --no-edit --date="1987-08-21 12:00:00"
git verify
```
A commit actually carries two dates — the author date (`--date`) and the
 committer date (`GIT_COMMITTER_DATE`) and both needed to match the
target date before verification passed.

---

## 13. Fix Old Typo

Objective: fix a typo buried in an older commit, not the most recent one.

### Commands Used
```bash
git rebase -i HEAD~2
# mark the older commit as `edit`
printf "Hello world\nHello world is an excellent program.\n" > file.txt
git add file.txt
git rebase --continue
git verify
```
Interactive rebase pauses at the marked commit, letting it be amended in
place, then `rebase --continue` replays the remaining commits on top of
the correction.

---

## 14. Commit Lost

Objective: recover a commit that's no longer reachable from any branch.

### Commands Used
```bash
git reflog
git fsck --lost-found
for c in $(git fsck --lost-found | awk '/dangling commit/ {print $3}'); do
  git show --no-patch --format="%H %s" $c
done
git reset --hard 2de7a81
git verify
```
`git reflog` tracks where `HEAD` has pointed even after a branch is reset
 away from a commit, and `git fsck --lost-found` surfaces commits that are
 still in the object database but unreachable from any branch. This is
where the task stopped feeling like "using Git" and started feeling like
understanding how it actually stores things.

**What went wrong first:**  Several dangling commits turned up not one
so I had to read each commits message, with `git show --no-patch` to
identify the specific one described in the exercise ("Very important piece of
work") rather than guessing at a hash.
---

## 15. Split Commit

Objective: split one commit containing multiple unrelated changes into
separate commits.

### Commands Used
```bash
git reset HEAD^
git add first.txt
git commit -m "Add first.txt"
git add second.txt
git commit -m "Add secont.txt"
git verify
```
`git reset HEAD^` undo the commit but keeps its changes unstaged in the
 working directory, so each file can be staged and committed separately.

---

## 16. Too Many Commits

Objective: combine several small commits into one clean commit.

### Commands Used
```bash
git rebase -i HEAD~2
# change `pick` to `squash` on the second commit
git verify
```
 `squash` folds a commit into the one before it, combining both diffs into
 a single commit.

---

## 17. Make the File Executable

### Commands Used
```bash
chmod +x script.sh
git add script.sh
git commit --amend --no-edit
git verify
```
 Git tracks the executable bit as part of a file's mode; `chmod` sets it on disk, and re-adding + amending records that mode change in the commit.

---

## 18. Commit Part of Work

Objective: split changes within a single file into two separate commits.

### Commands Used
```bash
git add -p
git commit -m "Task 1"
git add .
git commit -m "Task 2"
git verify
```
`git add -p` walks through the file's changes hunk by hunk, so only some of them get staged —,letting the same file be committed in two logical parts.

---

## 19. Pick Your Features

Objective: apply specific feature commits onto the current branch, resolving
conflicts along the way.

### Commands Used
```bash
git cherry-pick feature-a
git cherry-pick feature-b
git merge --squash feature-c
# resolve program.txt conflicts by hand
git add program.txt
git commit -m "Complete Feature C"
git verify
```
 `cherry-pick` replays individual commits from other branches onto the
 current one. `feature-c` needed several commits combined into one, so
 `merge --squash` handled that, and the resulting conflicts in
`program.txt` were resolved manually before committing.

**What went wrong first:** This was, by far the exercise. I went through several rounds of picking the wrong commits dealing with conflicting merges and rebasing just to fix my own mistakes. It took a lot of time before I finally got to the combination. For the time I actually had to slow down and carefully look at the branch graph instead of just guessing what would work.

---

## 20. Rebase Complex

Objective: move a branch onto a new base while skipping intermediate commits
that shouldn't come along.

### Commands Used
```bash
git rebase --onto your-master issue-555
git verify
```
`rebase --onto <newbase> <upstream>` replays only the commits on the
 current branch that aren't on `issue-555`, directly onto `your-master` 
 skipping the ones in between.

---

## 21. Invalid Order

Objective: swap the order of the last two commits.

### Commands Used
```bash
git rebase -i HEAD~2
# swap the two `pick` lines, save
git verify
```
 Interactive rebase replays commits in the order listed in its todo file;
 reordering the two lines and saving swaps their positions in history.

---

## 22. Find Swearwords

Objective: find every commit that introduced the word *shit* into
`words.txt` or `list.txt` across 100+ generated commits, and replace it with
*flower* ,without leaving the original word visible anywhere in history.

### Commands Used
```bash
git log -S"shit" --oneline -- words.txt list.txt
git rebase -i --root
# mark each matching commit `edit`
# fix the file content, then:
git add words.txt   # or list.txt
git commit --amend --no-edit
git rebase --continue
git verify
```
`git log -S"shit"`(the pickaxe search) finds every commit that added or
removed that string rather than reading through 100 plus commits by
hand. Each one is edited in place during a rebase then
amended.
**What went wrong first:** the challenge of this task two of the
three fixes were wrong and I didn't notice at the time. One commit ended up
adding a line instead of "flower " so the swearword was gone but so
was the intended replacement. Another accidentally overwrote a
unrelated word earlier in the file 'sit' became 'flower' while still
leaving its own target line blank. Both mistakes were invisible to a
`grep` since there was no longer any swearword to search for just words
missing where they shouldn't have been. `git verify` was what actually
caught both by naming the wrong word it found each time. I fixed
them by reentering interactive rebase at the specific commit hash
`git rebase -i <hash>^` checking the exact line number rather than
assuming it was the last one and re-verifying, after each fix.

---

## 23. Find Commit That Introduced a Bug

Objective: the home-screen text (base64-encoded) contains the word
*jackass* somewhere across the last 300 commits. Find the exact first
commit that introduced it.

### Commands Used
```bash
git bisect start HEAD 1.0
git bisect run sh -c "openssl enc -base64 -A -d < home-screen-text.txt | grep -v jackass"
git bisect reset
git push origin <COMMIT_ID>:find-bug
git verify
```
 `git bisect` does a binary search over the commit range of scanning 300 commits one by one.

`bisect run` automates every step. It decodes the base64 content. Uses grep to find the word in each candidate commit.
 `grep -v` gives an exit code: 0 is the word for not found, which we consider good; 1 is the word for found, which we consider bad. That exit code helps bisect narrow the search to the first bad commit, in about eight steps.

This exercise made the earlier ones click into place. It shows clearly why bisect matters when the source of a bug is not obvious.
---

## Screenshot

`completion-screenshot.png` — 23/23 exercises passed.
