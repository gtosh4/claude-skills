# Research recipes

Commands that work, and the ones that don't. Run these from a scratch directory.

---

## Start with the bundled snapshot

A full capture of **10.2** ships with this skill. Check it before fetching anything.

| Path | What it is |
|---|---|
| `data/listo-10.2-mods.tsv` | 706 Nexus mods as `ModID<TAB>Name` — the fast "does X exist" lookup |
| `data/listo-10.2-manifest.json` | The raw Wabbajack manifest (1.2 MB) |
| `data/docs/*.md` | The four Listo doc pages, raw markdown |
| `scripts/strip.sh` | HTML-to-text helper for Nexus and bg3.wiki pages |

**Never read the manifest or the changelog whole** — they are 1.2 MB and 293 KB. Grep them.

```bash
S=~/.claude/skills/listo-build

# does a class / subclass / feat / race exist in the list?
grep -i -E "eloquence|celestial|skeleton crew" "$S/data/listo-10.2-mods.tsv"

# everything in a category
grep -i -E "warlock|patron|pact" "$S/data/listo-10.2-mods.tsv" | cut -f2

# what a doc page says about a mechanic
grep -n -i -E "attunement|initiative|camp suppl" "$S"/data/docs/*.md
```

The manifest holds what the TSV cannot: **which file variant was pulled**, non-Nexus sources, and
version strings. This matters — it's how you tell the feat version of a mod from the automatic
one, or a full package from a sub-module.

```bash
# which archive was actually downloaded for a mod
grep -o -E '"Name":"[^"]*[Ss]keleton[^"]{0,70}' "$S/data/listo-10.2-manifest.json" | sort -u

# non-Nexus archives (mod.io, GitHub)
grep -o -E '"Url":"[^"]{1,120}' "$S/data/listo-10.2-manifest.json" | sed 's/"Url":"//' | sort -u
```

The snapshot is frozen at 10.2, built 8 July 2026. When the list moves, refresh it using the
sections below and re-check `references/listo-rules.md`.

---

## Nexus Mods blocks WebFetch — use curl

WebFetch returns HTTP 403 on every nexusmods.com page. curl with a browser user-agent works:

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
curl -sS -A "$UA" "https://www.nexusmods.com/baldursgate3/mods/<ID>?tab=description" -o mod.html
```

Pages are ~250–330 KB of HTML. Strip to text with this helper:

```bash
cat > strip.sh <<'EOF'
#!/bin/sh
tr '\n' ' ' < "$1" \
| sed 's/<script[^>]*>/\n@@SCRIPT@@/g; s/<\/script>/\n/g' \
| grep -v '^@@SCRIPT@@' \
| sed 's/</\n</g' \
| sed -n 's/^[^>]*>//p' \
| sed 's/&nbsp;/ /g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g; s/&quot;/"/g; s/&#39;/'"'"'/g' \
| sed 's/^[[:space:]]*//; s/[[:space:]]*$//' \
| grep -v '^$'
EOF
chmod +x strip.sh
./strip.sh mod.html > mod.txt
```

The useful content usually starts after the line `About this mod` or
`Collections containing this mod`. Filter the boilerplate:

```bash
awk '/About this mod/{f=1} f' mod.txt \
  | grep -v -i -E "permission|licen|copyright|translat|donation|credit|upload|asset|log in"
```

Descriptions with heavy letter-spacing render one character per line. Reflow with:

```bash
awk '/Collections containing this mod/{f=1} f' mod.txt | tr -d '\n' | sed 's/  */ /g'
```

**bg3.wiki works with the same curl approach** and is the right source for vanilla mechanics —
feat prerequisites, item effects, proficiency grants.

---

## The manifest is ground truth

The mod list ships as a `.wabbajack` file, which is a zip containing a JSON manifest named
`modlist` (no extension).

**Get the current version through the Wabbajack client**, not Nexus — the Nexus manual download
is stale (stuck at 8.0). The client stores it next to its executable:

```
C:\Wabbajack\<version>\downloaded_mod_lists\Listonomicon_@@_Listonomicon.wabbajack
```

`%LOCALAPPDATA%\Wabbajack\saved_settings\last-loaded-modlist.json` holds the exact path.

The client's **"Can't find game"** error is harmless for this purpose — the descriptor downloads
before the game check runs, so the file is already on disk.

Extract and confirm the version:

```bash
unzip -o -q "<path>.wabbajack" modlist -d ./wj/
tail -c 400 wj/modlist          # version is the last field
```

Pull every Nexus mod as `ModID<TAB>Name`:

```bash
grep -o -E '"ModID":[0-9]+,"Name":"[^"]{1,150}"' wj/modlist \
  | sed 's/"ModID":\([0-9]*\),"Name":"/\1\t/; s/"$//' \
  | sed 's/\\u0027/'"'"'/g' \
  | sort -u -t$'\t' -k2 > listo_mods.tsv
```

Then grep that file for anything you're about to recommend. Non-Nexus archives (mod.io, GitHub)
appear separately:

```bash
grep -o -E '"Url":"[^"]{1,120}' wj/modlist | sed 's/"Url":"//' | sort -u
```

Also useful: which exact file was pulled for a mod, since some mods ship variants (feat version
vs automatic version, main file vs sub-module):

```bash
grep -o -E '"Name":"[^"]*<keyword>[^"]{0,70}' wj/modlist | sort -u
```

---

## Documentation

Raw markdown, far more reliable than the rendered site:

```
https://raw.githubusercontent.com/ajaxxxxxxxx/ajaxxxxxxxx.github.io/main/docs/1listo/1-Home.md
                                                                              /3-GameBalance.md
                                                                              /4-SpellsFeatsClassesItems.md
                                                                              /5-ChangeLog.md
```

**The changelog is newest-first** — a *higher line number* is *older*. When a mod appears as both
ADDED and REMOVED, the one nearer the top of the file wins. Version headers are `## Listonomicon
vX.Y`; find them with `grep -n '^## Listonomicon'`.

**The docs lag the shipped list.** They stop at v10.0 while 10.2 ships. Treat them as a lead, and
confirm anything load-bearing against the manifest.

---

## Dead ends

- `authored-files.wabbajack.org` returns the same 989-byte SPA page for every path, including
  bogus ones. The gallery download URL in `modlists.json` only resolves inside the client.
- `build.wabbajack.org/lists/status/<name>.json` also returns the SPA shell.
- The **Nexus Collection** (slug `wpljdl`) renders its mod list client-side, so curl gets nothing
  useful. It may also be deleted.
- Cahoot's feat rebalance Google Doc, still linked from the docs, returns **410 Gone**.

---

## Repo metadata

`https://raw.githubusercontent.com/Listonomicon-Team/Listonomicon/main/modlists.json` gives the
current version, archive count, install size, and the Nexus Collection id without downloading
anything.
