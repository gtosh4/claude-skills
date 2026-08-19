# Finalists comparison data format

Author a JSON file; render it. **Never hand-write comparison HTML.**

```sh
scripts/render_finalists.py finalists.json -o out.html
scripts/render_finalists.py finalists.json --scrape sheets/ -o out.html
```

`--scrape` fills `scores` for any pairing that has none, by reading
`data-a1/a2/a3` and `data-b1/b2/b3` out of `sheets/<slug>.html` — the attributes
a rendered pair sheet already carries. It writes them back into the JSON, so it
is a one-time import rather than a build step. **Use it.** Re-typing 54 integers
per pairing out of a sheet is how transcription errors get in.

## What the renderer computes — never author these

| Thing | Rule |
|---|---|
| Pair value per axis | by axis kind — additive capped at 5, threshold `max`, complementary `min(5, hi + ⌊lo/2⌋)`, personal `min` |
| Coverage, damage coverage, score | as the ledger: `cov/105×50 + dmg/28×50` |
| Reach discount, melee lock, idle flags, holes | identical rules to the ledger and the pair sheet |
| Card order and the field table | ranked by score |

## Shape

```jsonc
{
  "title":   "Three Finalists v2",
  "eyebrow": "Listonomicon 10.2 · two players · Lone Wolf",
  "lede":    "What this page is.",
  "facts":   ["11 built pairings", "6 carries"],
  "cards_note": "Sits above the cards.",
  "footer":  "Provenance.",
  "method":  {"h2": "How to read this", "cards": [{"title": "…", "body": "…"}]},

  "pairings": {
    "bombard-fervor": {                     // key must match <slug>.html for --scrape
      "names":  {"a": "Bombard", "b": "Fervor"},
      "reach":  {"a": "hybrid",  "b": "static"},
      "splits": {"a": "Wizard 6 / Blood Hunter 14 · Astral Half-Elf · Urchin",
                 "b": "Cleric 17 / Bard 3 · Zeal · Lizardfolk · Soldier"},
      "url":    "https://…",                // the published pair sheet
      "tagline": "…",                       // lift from the sheet, do not re-write
      "shape":   "…",                       // the sheet's profile headline
      "damage":  "…",                       // the sheet's damage headline
      "scores": {                           // omit and use --scrape
        "a": {"I": [9 ints], "II": [...], "III": [...]},
        "b": {"I": [...],    "II": [...], "III": [...]}
      }
    }
  }
}
```

## Lift the prose, don't rewrite it

`tagline`, `shape` and `damage` should be **the sheet's own words** — its
`.tagline` and its profile and damage `<h2>`s. A card that paraphrases drifts
from the sheet it links to, and the sheet is the authority. Extracting them is
three regexes; do that rather than composing new sentences.

## Per pair, not per chassis

There is deliberately no shared roster here. The same carry appears on several
cards with different numbers, because each sheet built it against a different
partner and spent its feats differently. **Do not average them into one canonical
chassis** — the spread is the finding. Across five Bombard sheets its Act III AoE
ran 2–3 and its Endurance 4–5, and flattening that would have hidden the reason:
Wizard 6 freezes at 3rd-level slots for fourteen levels while enemy HP doubles.

If you want one number per chassis, that is the ledger's job, not this page's.
