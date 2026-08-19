# Pairing ledger data format

Author a JSON file; render it. **Never hand-write ledger HTML** — it is ~175KB,
and every number in it is derived from about 200 lines of chassis scores.

```sh
scripts/render_ledger.py ledger.json -o ledger.html
```

`assets/ledger-example.json` is a filled-in ledger — copy it and overwrite.
Every string is emitted as HTML, so inline `<b>`, `<em>` and `<code>` work.

## What the renderer computes — never author these

| Thing | Rule |
|---|---|
| Pair value per axis | by axis kind: additive `min(5, a+b)`, threshold `max`, complementary `min(5, hi + ⌊lo/2⌋)`, personal `min` |
| Coverage | the seven non-damage axes, per act and summed — 105 across the run |
| Damage coverage | `crowd = AoE + 0.5·ST·reach_c`, `priority = ST·reach_p + 0.25·AoE`, weighted 70/30, 60/40, 50/50 by act |
| Reach discount | applied to the **single-target term only** |
| Melee lock | a further ×0.9 on crowd when neither reach is `ranged`/`hybrid` |
| Score | `cov/105×50 + dmg/28×50` |
| Idle-body flags, holes, chips | flag under 3.0 in a fight type worth ≥40% of the act; hole is any pair axis ≤2 |
| The whole field table | every carry × every support, ranked |
| Which pairings become entries | each carry's **best** partner, ranked, capped at `entry_limit` |
| Every number in a variation line | from the pairing itself — you write only the clause after it |
| Roster order | carries then supports, each by the best score that chassis reaches anywhere |

**This list is the point of the format.** Hand-written variation figures were the
single largest source of stale numbers in the previous ledger: a re-score moved
135 pairings and left 27 quoted figures behind. Here they cannot go stale,
because they do not exist until render time.

## Shape

```jsonc
{
  "title":   "Listo Pairing Ledger",       // browser tab / artifact name
  "eyebrow": "Listonomicon 10.2 · two-player Lone Wolf",
  "lede":    "One paragraph on what the ledger is for.",
  "facts":   ["26 chassis", "level cap 20"],   // mono chips under the standfirst
  "entry_limit": 12,                        // carries beyond this fall out, and are named
  "footer":  "Provenance line.",

  "chassis": {
    "Bombard": {                            // key is the id; used for anchors
      "display": "Bombard",                 // optional; shown instead of the key
      "role":    "carry",                   // carry | support
      "reach":   "hybrid",                  // ranged | hybrid | mobile | static
      "split":   "Blood Hunter 14 / Wizard 6",
      "meta":    "Int 22 · 7 feats",
      "note":    "Prose. What the chassis is and what it gives up.",
      "scores": {                           // 9 ints per act, in AXIS ORDER
        "I":   [3,2,3,2,2,0,3,3,4],
        "II":  [4,4,3,3,4,0,3,4,4],
        "III": [4,4,3,3,4,0,3,4,4]
      }
    }
  },

  "entries": {                              // keyed by CARRY id, not by pairing
    "Bombard": {
      "name":    "Bombard & Fervor",
      "tag":     "caster blood hunter + weapon-cleric support",
      "verdict": "Reads as. …",
      "cost":    "Costs. …",
      "vars": [
        {"partner": "Chains", "note": "Hold Monster on a short-rest clock."},
        {"text": "<b>Wisdom variant</b>: free prose, no numbers attached."}
      ]
    }
  },

  "method":  {"h2": "…", "cards": [{"title": "Coverage", "body": "…"}]},
  "caveats": {"h2": "…",
    "excluded":    {"summary": "Excluded chassis, and why", "items": ["…"], "lead": "optional trailing paragraph"},
    "settled":     {"summary": "Settled by reading the installed paks", "items": ["…"]},
    "assumptions": {"summary": "Assumptions that would still move numbers", "items": ["…"]}
  }
}
```

**Axis order is fixed** and every `scores` array must have nine entries:

    single-target, aoe, durability, actions, control, sustain, skills, saves, endurance

## Errors the renderer raises rather than papering over

- a chassis with an unknown `reach`
- a `scores` array that is not nine long
- an entry whose carry survives the `entry_limit` cut but has no prose
- a variation naming a partner the carry has no pairing with

The last two are the ones that bite. A carry that rises into the cut needs prose
before the ledger will build, which is what stops the entries and the field
table drifting apart.
