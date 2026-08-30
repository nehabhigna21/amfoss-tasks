## LEVEL 2 — The Two Faces of Whiskey Peak

**Repo:** Terminal-Voyage-User-Edition
**Path:** ~/Terminal-Voyage-User-Edition/GrandLine/Whiskey_Peak/
**My approach**:

 I started by using git branch -a to look through the available branches and found the hidden branch whiskey_peak_investigation. I then switched to it using:
git checkout whiskey_peak_investigation
Once inside the Whiskey Peak directory, I had check for hidden files and directories. This revealed a folder named .baroque_works_cache. I entered that directory and inspected its contents, where I found the unlock.sh script.
I initially went through the script manually using nano instead of simply running the script directly. Inside unlock.sh, I found an expected target hash.

The script generates a hash from the AWAKENING_SIGNATURE using:
INPUT_HASH=$ echo -n "$AWAKENING_SIGNATURE" | sha256sum | awk '{print $1}'
The goal was to make the generated hash match the target hash specified in the script. I used the Level 1 flag as the AWAKENING_SIGNATURE, ran the required command, and obtained the corresponding hash.

After confirming that the generated hash matched the expected value in unlock.sh, I proceeded with the remaining steps defined by the script.
The final part involved decrypting the Level 2 flag. The encrypted value provided by the script had to be decrypted using the Level 1 flag as the password.
The decryption was performed using:
REAL_FLAG=$(echo "$ENCRYPTED_FLAG" | openssl enc -aes-256-cbc -d -a -pbkdf2 -iter 100000 -pass pass:"$AWAKENING_SIGNATURE" 2>/dev/null)

I replaced ENCRYPTED_FLAG with the encrypted value obtained during the previous step and used my Level 1 flag as the AWAKENING_SIGNATURE. After running the command, the Level 2 flag was successfully revealed.
### Result

**Flag:** `BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}`
