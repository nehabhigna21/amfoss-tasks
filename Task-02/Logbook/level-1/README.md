## LEVEL 1 — Awakening at Loguetown Reef

**Repo:** `Terminal-Voyage-User-Edition`
**Path:** `~/Terminal-Voyage-User-Edition/GrandLine/Loguetown_Reef/`

### Objective

Somewhere among several sectors of near-identical crates lies the real Devil
Fruit — the rest are Marine-manufactured decoys.

### Approach

```bash
cd Terminal-Voyage-User-Edition/GrandLine/Loguetown_Reef
ls -la
cd sector_A && ls -la && cd ..
cd sector_B && ls -la && cd ..
cd sector_C && ls -la && cd ..
./eat.sh sector_C/devil_fruit_6.txt
```

Went through each sector's contents by hand rather than assuming the first
one was right — the whole point of the level is that every crate *looks*
identical. `sector_C` was the one with a file that stood out (a genuine item
doesn't look manufactured/catalogued the same way decoys do), so I "ate" it
with the provided `eat.sh` script.

### Result

```
*** CRUNCH! ***
The fruit tastes absolutely terrible...
Reality begins to fracture.
Forgotten histories rush into your mind.
You have awakened the legendary...
Gito Gito no Mi
```

**Flag:** `ONE_PIECE{GITO_GITO_NO_AWAKENING}`
