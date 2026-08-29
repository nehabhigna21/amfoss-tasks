## LEVEL 5 — The Buster Call Timeline Recovery

**Repo:** `Terminal-Voyage-User-Edition`
**Path:** `~/Terminal-Voyage-User-Edition/GrandLine/` → `Enies_Lobby/.cp9_secure_vault/`

### Objective

The Buster Call destroyed the present state of the repo — the files needed
now only exist in the past. The task is to walk backward through git history
to a moment before the "bombardment" and recover them from there.

### Approach

```bash
git checkout alternate_timeline
git log --oneline
git checkout d4e7bf5
cd Enies_Lobby/.cp9_secure_vault
python3 poneglyph.py
```

Rather than working on the current state of the branch, checked out
`alternate_timeline` and used `git log` to find a specific earlier commit
(`d4e7bf5`) — a point "before the cannons fired" — and checked that out
directly to reach the untouched files still sitting in `Enies_Lobby`.

### Note on this level's documentation

I don't have a screenshot for this one — this writeup is reconstructed from
my actual shell history rather than a captured image. I'd rather say that
plainly than fake a screenshot or pretend a level was skipped.
