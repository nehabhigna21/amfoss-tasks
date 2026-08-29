## LEVEL 6 — The Great Merge War at Laugh Tale

**Repo:** [`Laugh-Tale-Merge-War`](https://github.com/rogueone-x/Laugh-Tale-Merge-War)
**Path:** `~/Laugh-Tale-Merge-War/`

### Objective

Two conflicting timelines (branches) both claim to hold the true history.
Neither one alone has the complete Pirate King's Password — it only exists
by merging both and resolving what conflicts between them.

### Approach

```bash
git clone https://github.com/rogueone-x/Laugh-Tale-Merge-War
cd Laugh-Tale-Merge-War
git branch -a
git merge origin/pirate_king_path
```

First merge attempt failed immediately — Git didn't know who I was:

```
Committer identity unknown
*** Please tell me who you are.
```

Fixed with:
```bash
git config --global user.email "nehabhigna@gmail.com"
git config user.name "nehabhigna21"
git merge origin/pirate_king_path
```

That produced real conflicts in both treasure files:
```
Auto-merging treasure/key_part_1.txt
CONFLICT (content): Merge conflict in treasure/key_part_1.txt
Auto-merging treasure/key_part_2.txt
CONFLICT (content): Merge conflict in treasure/key_part_2.txt
```

Resolved each by hand, keeping the correct half of the password from each
conflicting version rather than just picking one side wholesale:

```bash
cd treasure
nano key_part_1.txt
nano key_part_2.txt
git add .
git commit -m "key_part"
```

### The script name typo (an honest confession)

Ran the verification script and it didn't exist — misread the filename
twice before actually reading it correctly:

```
$ ./vicory.sh
-bash: ./vicory.sh: No such file or directory
$ ./ victory.sh
-bash: ./: Is a directory
$ ./victory.sh
```

(It's `victory.sh`, not `vicory.sh` — and no space after `./`.)

### Result

```
====================================
 Verifying Timeline Integrity
====================================

Enter the Pirate King's Password: TheGrandLineRemembers
Timeline Integrity ............. OK
Merge Conflict .................. Resolved
Repository ...................... Restored
History .......................... Preserved

====================================================

        THE ONE PIECE HAS BEEN FOUND
```

Returning to the main Terminal Voyage script with that password unlocked the
final reward:

```
FLAG{The_Grand_Line_Remembers_Your_Commit}

REWARD UNLOCKED
Title: Pirate King of Git
Badge: Keeper of History
```
