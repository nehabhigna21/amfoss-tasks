## LEVEL 5 — The Buster Call Timeline Recovery

**Repo:** Terminal-Voyage-User-Edition
**Path:** ~/Terminal-Voyage-User-Edition/GrandLine/ → Enies_Lobby/.cp9_secure_vault/

### Objective

The Buster Call destroyed the current state of the repo , the files needed
now only exist in the past. The task is to walk backward through git history, find the file, run and find the key to get to the next level.

### Approach


git checkout alternate_timeline, get to the branch and find the history in one go, get to the level 5 as required using  git checkout d4e7bf5, the pass to cd Enies_Lobby/.cp9_secure_vault (the target folder), we are going to find script and run python3 poneglyph.py
poneglyph.py wanted the two cipher fragments from Levels 3 and 4
concatenated together as the unlock code:

Enter code : KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnLSwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA=
Prize :
https://github.com/rogueone-x/Laugh-Tale-Merge-War


### Result

PONEGLYPH reassembled into the vault code, which unlocked the URL for the Level 6 repo,the two Little Garden/Water 7 fragments only became useful once combined here.
