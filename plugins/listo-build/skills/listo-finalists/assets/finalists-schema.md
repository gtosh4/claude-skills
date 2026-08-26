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
| Pair value per axis | by axis kind — **`listo-build/references/scoring-model.md` §4 is authoritative**: additive `a+b` uncapped, complementary `hi + ⌊lo/2⌋` **uncapped**, personal `min` |
| Tempo, the non-tempo blocks, score | as the ledger — one implementation, in `listo-build/scripts/scoring.py`, which implements `listo-build/references/scoring-model.md` |
| Reach discount, melee lock, idle flags, holes | identical rules to the ledger and the pair sheet |
| Card order and the field table | ranked by score |

## Shape

```jsonc
{
  "title":   "Eleven Built Pairings",    // name the shortlist; no fixed count
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
        "a": {"I": [10 values], "II": [...], "III": [...]},   // index 8 (saves) is null
        "b": {"I": [...],    "II": [...], "III": [...]}
      },

      // ── the five the model reads and --scrape cannot fill ──────────────
      "saves":  {"a": {"I": {"prof": ["wis","con"], "boosters": ["aura-of-protection"]},
                       "II": {...}, "III": {...}}, "b": {...}},
      "concentration": {"a": false, "b": true},
      "types":  {"a": ["cold","radiant"], "b": ["slashing","radiant"]},
      "meta":   {"a": "wis", "b": "cha"},   // primary ability, lowercase
      "skills": {"a": {"I": {"Perception": 9, "Investigation": 5, "Persuasion": -1},
                       "II": {...}, "III": {...}}, "b": {...}}
    }
  }
}
```

## The five fields `--scrape` cannot fill — author all of them

`--scrape` reads the six per-act series and nothing else. The model reads more
than that, and **degrades silently rather than failing** when a field is absent.
Each of these was missing from a rendered page at some point, and each was worth
points:

| field | what reads it | what its absence does |
|---|---|---|
| `saves` | `saves_pair` | required — the render fails without it |
| `concentration` | `derive_saves` | Constitution stops counting double on the body holding a concentration spell |
| `skills` | `skills_pair` | **derives the Skills rung from `{}`, scores 0, and reports `skl` as a hole on every card** |
| `types` | `type_spread`, `gear_key` | the Absolute Wrath damage-type penalty never applies, and contention falls back to the blunt `SAME_CLASS` |
| `meta` | `gear_key` | same fallback — two bodies sharing a primary ability stop being charged for it |

`splits` is read twice: as display text on the card, and — cut at the first
`&middot;` — as the class split behind `same_class`. Keep the classes first.

**`skills` uses `scoring.RECORDED_SKILLS` names, capitalised**, and
`Perception`, `Investigation` and `Persuasion` are required on every body: an
absent modifier on one of those reads as missing evidence, not as untrained.

## `--scrape` nulls the saves index for you

A rendered pair sheet carries the **resolved** saves value at index 8, because
it derived it for that pairing and drew it on the radar. The finalists model
derives saves itself and refuses a pre-filled row — rightly, since a value
derived beside one partner is wrong beside another. `scrape()` nulls index 8 on
import; do the same by hand if you ever transcribe a row.

> **`assets/finalists-v1.json` is stale and will not render.** It predates the
> Control split, so its rows carry **nine** axes rather than ten, and it has no
> `saves` block. Keep it as a record of that run; do not use it as a template.
> `finalists-example.json` is the current shape.

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
