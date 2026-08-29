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
(`d4e7bf5`, labeled "Level 5: Vault Sealed") — a point "before the cannons
fired" — and checked that out directly to reach the untouched files still
sitting in `Enies_Lobby/.cp9_secure_vault`.

`poneglyph.py` wanted the two cipher fragments from Levels 3 and 4
concatenated together as the unlock code:

```
Enter code : KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnLSwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA=
Prize :
https://github.com/rogueone-x/Laugh-Tale-Merge-War
```

### Result

`PONEGLYPH_FRAGMENT_I` + `PONEGLYPH_FRAGMENT_II` reassembled into the vault
code, which unlocked the URL for the Level 6 repo — the two Little
Garden/Water 7 fragments only became useful once combined here.
