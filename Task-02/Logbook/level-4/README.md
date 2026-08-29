## LEVEL 4 — The Camouflaged Blueprints of Water 7

**Repo:** `Terminal-Voyage-User-Edition`
**Path:** `~/Terminal-Voyage-User-Edition/GrandLine/Water_7/galley_la_company/`

### Objective

The Sea Train blueprints have been stripped of any identifying name or
extension — the file has to be judged by what it actually *is*, not what
it's called.

### Approach

```bash
git checkout canonical-timeline
cd GrandLine/Water_7/galley_la_company
ls
# puffing_tom_blueprints
```

A file with no extension, so asked `file` what it actually was instead of
guessing:

```bash
file puffing_tom_blueprints
# gzip compressed data, was "step2_blueprints.tar", ...
```

Renamed it to match reality and unpacked it, checking its type again at each
step since the disguise was layered:

```bash
mv puffing_tom_blueprints puffing_tom_blueprints.gz
gunzip puffing_tom_blueprints.gz
file puffing_tom_blueprints
# now: a tar archive

tar -xf puffing_tom_blueprints
# produced step1_blueprints.zip

unzip step1_blueprints.zip   # (had to `sudo apt install unzip` first)
cd blueprints_extracted
cat secret_link.txt
```

### Result

Three layers of disguise (gzip → tar → zip) peeled back using `file` at each
step rather than assuming the extension, ending in `blueprints_extracted/secret_link.txt`:

```
PONEGLYPH_FRAGMENT_II="SwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA="
```
