## LEVEL 3 — The Wax Labyrinth of Little Garden

**Repo:** `Terminal-Voyage-User-Edition`
**Path:** `~/Terminal-Voyage-User-Edition/GrandLine/Wax_Jungle/`

### Objective

Hundreds of intercepted Baroque Works reports are scattered through the
jungle, each looking authentic. Only one carries the Level 2 flag in its
broadcast (base64) form — that's the real one.

### Approach

```bash
git checkout little_garden
cd GrandLine/Wax_Jungle
ls    # report_001.log ... report_008.log, sector_alpha/beta/gamma/delta
```

Rather than opening every report by hand, converted the Level 2 flag to its
transmitted (base64) form and searched the whole tree for that exact string:

```bash
echo "BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}" | base64
# QkFST1FVRV9ESUFMe1NQTElUX1RJTUVMSU5FX01JU0RJUkVDVElPTn0K

grep -r "QkFST1FVRV9ESUFMe1NQTElUX1RJTUVMSU5FX01JU0RJUkVDVElPTn0K" .
```

That pointed to a single matching file:

```bash
cat sector_beta/outpost/watchtower/storage/archive/agent_manifest.log
```

### Result

```
SECURITY LOG ACCESS // LEVEL 3 CLEARANCE REQUIRED
STATUS: METALLIC WAX SUIT ACTIVE
...
BAROQUE WORKS EXECUTIVE REPORT
PONEGLYPH_FRAGMENT_I = "KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL"
```

**Cipher fragment obtained:** `PONEGLYPH_FRAGMENT_I`
