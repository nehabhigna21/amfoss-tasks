# TASK-02: Prologue — The Logbook of the Grand Line

A One Piece-themed terminal adventure across two repos:

- [`Terminal-Voyage-User-Edition`](https://github.com/rogueone-x/Terminal-Voyage-User-Edition) — Levels 1–5
- [`Laugh-Tale-Merge-War`](https://github.com/rogueone-x/Laugh-Tale-Merge-War) — Level 6, the finale

Each level's writeup and screenshots live in `Logbook/level-1` through
`Logbook/level-6`.

## Approach

Every level followed roughly the same loop: explore the filesystem/git
branches for the level, find whatever's hidden or disguised, decode/decrypt
it, and use the result to unlock the next step. The tools changed level to
level — plain file navigation, `sha256sum` + `openssl` for the vault, `base64`
+ `grep` for the decoy reports, `file`/`gunzip`/`tar`/`unzip` for the
disguised blueprint, `git log`/`checkout` for walking backward through
history, and finally a real `git merge` conflict for the ending.

Level 5 has a writeup below but no screenshot — see its README for why.

## Levels

| Level | Location | Theme |
|---|---|---|
| 1 | Loguetown Reef | find the real Devil Fruit among decoys |
| 2 | Whiskey Peak | decrypt a vault script using the Level 1 flag |
| 3 | Little Garden (Wax Jungle) | find the one authentic report among decoys |
| 4 | Water 7 | identify and unpack a disguised, renamed blueprint file |
| 5 | Buster Call / Enies Lobby | walk backward through git history to recover the past |
| 6 | Laugh Tale | resolve a real merge conflict to reconstruct the password |
