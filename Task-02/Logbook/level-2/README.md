## LEVEL 2 — The Two Faces of Whiskey Peak

**Repo:** `Terminal-Voyage-User-Edition`
**Path:** `~/Terminal-Voyage-User-Edition/GrandLine/Whiskey_Peak/`

### Objective

Beneath the visible island is a hidden communications cache holding an
intercepted Baroque Works transmission. It needs the Level 1 flag to unlock.

### Approach

```bash
git checkout whiskey_peak_investigation
cd GrandLine/Whiskey_Peak
ls -a          # reveals the hidden .baroque_works_cache/
cd .baroque_works_cache
nano unlock_vault.sh
```

Reading `unlock_vault.sh` showed it needed a SHA-256 hash of the Level 1
flag as a signature check:

```bash
echo -n "ONE_PIECE{GITO_GITO_NO_AWAKENING}" | sha256sum | awk '{print $1}'
```

Which produced the matching signature and unlocked the next stage of the
script, printing:

```
[SIGNATURE MATCH] Devil Fruit aura detected. Bypassing proxy firewall...
[SUCCESS] Decrypting Baroque transmission streams...
```

The script then held an AES-encrypted payload, decryptable with the same
flag as the passphrase:

```bash
echo "U2FsdGVkX18eGXT7fCm/5zmZmejGVicPYQQLji9cigHrIyxzalWleyVW+k3X6rBlS3baMgfv0DVe24ILF5v+rw==" \
  | openssl enc -aes-256-cbc -d -a -pbkdf2 -iter 100000 -pass pass:"ONE_PIECE{GITO_GITO_NO_AWAKENING}"
```

### Result

**Flag:** `BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}`
