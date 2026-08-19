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
| Pair value per axis | by axis kind — **`listo-build/references/scoring-model.md` §4 is authoritative**: additive `a+b` uncapped, complementary `hi + ⌊lo/2⌋` **uncapped**, personal `min` |
| Fight-type terms | crowd and boss terms per `scoring-model.md` §5, MIX-blended 70/30, 60/40, 50/50 by act |
| Reach discount | applied to the **single-target damage term only** — control takes none |
| Melee lock | a further ×0.9 on crowd when neither reach is `ranged`/`hybrid` |
| Tempo cap | `min(capability breadth, action points)` — Actions bounds tempo rather than adding to it |
| Score | the four blocks of `scoring-model.md` §9 |
| Idle-body flags, holes, chips | flag under 3.0 in a fight type worth ≥40% of the act; hole is any pair axis ≤2 |
| The whole field table | **every chassis with every other**, ranked — `C(n,2)` unordered pairs |
| Which pairings become entries | each chassis's **best** partner, ranked, capped at `entry_limit`; a pairing that two chassis both name is kept once |
| Every number in a variation line | from the pairing itself — you write only the clause after it |
| Roster order | by the best score that chassis reaches anywhere |
| Order within a pairing | higher delivered damage first, then higher total axis value, then the id alphabetically — see `scoring-model.md` §10 |

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
  "entry_limit": 12,                        // chassis beyond this fall out, and are named
  "footer":  "Provenance line.",

  "chassis": {
    "Bombard": {                            // key is the id; used for anchors
      "display": "Bombard",                 // optional; shown instead of the key
      "reach":   "hybrid",                  // ranged | hybrid | mobile | static
      "split":   "Blood Hunter 14 / Wizard 6",
      "meta":    "Int 22 · 7 feats",
      "note":    "Prose. What the chassis is and what it gives up.",
      "concentration": false,               // does this body's plan ride a concentration spell?
      "saves": {                            // source of truth for the saves axis — see below
        "I":   {"prof": ["int","wis","dex","con"], "boosters": []},
        "II":  {"prof": ["int","wis","dex","con"], "boosters": []},
        "III": {"prof": ["int","wis","dex","con"], "boosters": []}
      },
      "scores": {                           // 10 per act, in AXIS ORDER; index 8 is null
        "I":   [3,2,3,2,2,1,0,3,null,4],
        "II":  [4,4,3,3,4,2,0,3,null,4],
        "III": [4,4,3,3,4,2,0,3,null,4]
      }
    }
  },

  "entries": {                              // keyed by CHASSIS id, not by pairing
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

**Axis order is fixed** and every `scores` array must have **ten** entries:

    single-target, aoe, durability, actions, control-single, control-area,
    rescue, skills, saves, endurance

Control is **two axes**, split crowd-versus-boss exactly as damage already is — see
`axis-rubrics.md` §5 and §6, and `scoring-model.md` §3. It is the only axis that gained a split;
§7 there records why Rescue, Saves and Durability did not.

## The saves axis is authored as a set, not a number

Index 8 is **derived** and must be authored as `null`. Every other axis is a judgement against
`listo-build/references/axis-rubrics.md`; saves is the one axis whose rubric is written in terms
of *which* abilities are proficient and whether the grants are **disjoint**, so a bare 0–5 cannot
be re-checked from outside. Author the evidence and let the renderer score it.

```jsonc
"saves": {
  "II": {
    "prof":     ["wis","dex","con","cha"],   // the RESULTING set, deduplicated
    "boosters": ["brutish-durability"]        // blanket effects, not proficiencies
  }
}
```

`prof` — lowercase from `str dex con int wis cha`. Record the **union after de-duplication**, which
is what makes the disjointness rule bite: Blood Hunter's `int + dex` on top of a Lone Wolf `int +
dex` pick is two entries, not four. Grants are the **level-1 class** (two, and only the level-1
class), **Lone Wolf's two picks**, each **Resilient**, **Slippery Mind** (Rogue 15, adds `wis`),
and **Diamond Soul** (Monk 14, adds all six).

`boosters` — numeric or advantage effects that apply across saves without granting proficiency:

| id | what | scope |
|---|---|---|
| `brutish-durability` | Fighter 7 — +1d6 to every save, unconditional, no resource | self |
| `war-caster` | advantage on concentration saves only | self |
| `aura-of-protection` | Paladin 6 — +Cha modifier to every save | **pair** |

`concentration` (chassis-level, not per act) — `true` if the body's plan rides a concentration
spell. It reorders the ability weighting: **Con outranks Wis when true**, since a broken
concentration is a lost body one turn later; otherwise the ordering is Wisdom > Constitution ≈
Dexterity > Charisma > Strength > Intelligence.

### How the renderer derives index 8

Rungs follow `axis-rubrics.md` §9. `key` = `{wis, con, dex}`.

| value | test |
|---|---|
| 0 | `len(prof) ≤ 2` and no `key` ability |
| 1 | `len(prof) == 2` and ≥1 `key` |
| 2 | `len(prof) == 3` and ≥1 `key` |
| 3 | `len(prof) == 4` and ≥2 `key` |
| 4 | `len(prof) ≥ 4` covering all of `key`, **or** any blanket booster |
| 5 | all six proficient, **or** rung-4 coverage **and** a blanket booster |

Then: **if `concentration` is true and `con` is not in `prof`, cap the result at 3.** A body that
holds the pair's one control spell without a Constitution save is structurally fragile regardless
of what else it is proficient in.

### Anything with special handling fails closed

**An unknown value is a hard error. Never skipped, never defaulted, never warned-and-continued.**

The failure this prevents is one-directional and invisible. A booster the renderer does not
recognise contributes nothing, so the score comes out **too low** — and a score that is too low is
indistinguishable from an honest one. Nothing downstream can catch it: the field table still
ranks, the entries still render, the chassis just quietly sits a rung below where it belongs.
Every other class of bug in this format announces itself; this one does not.

So the checking is reactive rather than an ongoing tax. You do not have to remember to audit
boosters before every render. You have to fix a crash when you author something new, once.

**Every enum in this format is closed** — `role`, `reach`, `prof` abilities, `boosters` ids, act
keys, axis kinds. Unknown member, raise. Do not add a permissive branch to any of them.

**Before authoring a value with special handling, confirm the renderer implements it.** The
registry in `render_ledger.py` is the authority; the tables in this file mirror it. Adding a
booster is one change that touches the registry, the table above, and a case that exercises it —
if you cannot point at the line that applies the effect, it is not implemented, and authoring the
id is how you find that out at render time instead of after publishing.

**A deliberate drop must be distinguishable from an unrecognised one.** The only sanctioned drop
in this format is a second `aura-of-protection` in one pairing, below. It warns by name and says
what it dropped and why. Nothing else silently discards an authored value.

### `aura-of-protection` is a pair effect

Aura raises **both** bodies, so it cannot be scored inside one body's value. The combiner applies
it to each side *before* taking the `min` for the Personal axis. **Auras do not stack** — a second
`aura-of-protection` in the same pairing is ignored, and the renderer warns rather than double-
counting it. This is the commonest way a pair wastes six levels.

## Errors the renderer raises rather than papering over

These are **fatal, by design** — see "Anything with special handling fails closed". A render that
cannot score something correctly must not produce a number for it.

- a chassis with an unknown `reach`
- a `scores` array that is not **ten** long
- a `scores` array whose index 8 is not `null` — saves is derived, never authored
- a chassis with no `saves` block, or one missing an act
- a `prof` entry outside `str dex con int wis cha`, or a duplicate within one act
- an unknown `boosters` id
- an entry whose chassis survives the `entry_limit` cut but has no prose
- a variation naming a partner the chassis has no pairing with

The last two are the ones that bite. A chassis that rises into the cut needs prose
before the ledger will build, which is what stops the entries and the field
table drifting apart.

## There is no carry/support field

A chassis is **not typed**. The renderer pairs every chassis with every other, so a duo of two
damage bodies or two controllers is representable and rankable rather than unsayable — the old
`product(carries, supports)` could not express one even to show it scoring badly. `C(n,2)` costs
nothing: pairings are derived from the authored ints at roughly 600 bytes and microseconds each.

What a body does with its turns is still visible — in its `note`, its axis values, and the
`niche` its seed sat under. It is just not a partition the model enforces.
