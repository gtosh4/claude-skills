# Pair sheet data format

Author a JSON file; render it. Never hand-write pair-sheet HTML — it is ~90KB
per sheet, and about two thirds of that is CSS, JS and scaffolding that
`scripts/render_pair.py` already holds.

```sh
scripts/render_pair.py pair.json -o sheet.html
```

`assets/pair-example.json` is a filled-in skeleton — copy it and overwrite the
values. Every string is emitted as HTML, so inline `<b>`, `<em>` and
`<span class="tag">` work. Use `—` for an empty cell.

## What the renderer computes — do not author these

| Thing | Rule |
|---|---|
| Pair radar value per axis | from `profile.scores`, by axis kind, at view time in the page's JS |
| Whole delivered-damage table | from `profile.scores` (ST, AoE) + `damage.reach` |
| Saves (index 8) | derived from `profile.saves` — authored as `null` |
| Idle-body flags (`u-idle`) | character under 1.25 in a fight type worth ≥40% of that act |
| Melee lock | applied, and its callout emitted, when neither reach is `ranged`/`hybrid` |
| Axis names, kinds, order, act bands | fixed; override with `profile.axes` / `.kinds` / `.labels` / `.bands` only if a sheet genuinely differs |
| Gate grade | `bad` when `owner` is `none`, else `ok` — set `grade` (`ok`\|`mid`\|`bad`) to override |
| Single-target, AoE and Durability ratios and rungs | from `derived` — par tables, the gear constant and the ladders are `scoring.py`'s |
| Illithid IMR, charges, tax, appetite | from `illithid.picks` — `⌊powers ÷ 5⌋` capped at 5, `2.5 + 0.5 × powers`, `+IMR` |
| Tadpoles spent, supply, spare | `powers + 1` per body (the first tadpole buys Persuasion); supply is 12 / 24 / 50 cumulative |

## Shape

```jsonc
{
  "title": "Bombard & Chains",        // browser tab / artifact name
  "class": "paladin",                 // theme = PAIR's lead class; omit for neutral
  "tagline": "...",
  "splits": {"a": "Cleric 17 / Fighter 3", "b": "..."},

  "roster": {
    "h2": "...", "note": "...",       // note = the check-at-creation callout, optional
    "a": {
      "name": "Bombard",
      "sub": "Cleric 17 / Fighter 3 · Light · <b>Wood Elf</b> · Sage",
      "abilities": [["STR", 8, "—", "—", "—", 8, "−1"], ...6 rows],  // ability, buy, LW, feat, other, final, mod
      "saves":  [["From level-1 class", "Wis, Cha ..."], ...],       // [bold lead, text] or a plain string
      "race":   {"name": "Wood Elf", "traits": [["Fleet of Foot", "..."]]},
      "skills": {"background": "Sage", "items": [["Class", "..."]]}
    },
    "b": { ...same... }
  },

  "derived": {                        // omit the block and the section does not render
    "h3": "...",
    "a": {
      "I": {
        "damage": {                   // the ledger's own damage block, same wire format
          "actions": {"attacks": 7, "spells": 1, "filler": 0},   // must sum to 8
          "bonus": {"used": [{"src": "Staccato Lightning", "n": 4}]},
          "pools": [{"name": "Channel Oath", "refresh": "short", "size": 1, "spent": 1}],
          "slots": {"caster_level": 5, "pool": 9, "to_damage": 0.6},
          "riders": [{"name": "Unholy Smite", "st": 6.7, "aoe": 0,
                      "single_axis_reason": "a smite rides one melee hit"}],
          "st_raw": 63, "st_instances": 3.5,     // damage per ROUND, and separate rolls per round
          "aoe_raw": 24, "aoe_instances": 3.0,
          "mult": {"st": 1.35, "why": "Spiteful Suffering (routine advantage)"}
        },
        "dur": {"pool": 93, "ac": 19,            // pool = max HP + temp HP + self-healing in-fight
                "prop": [["Bear Heart rage", 0.5]],        // MULTIPLIES the hit — 0.5, never 2
                "flat": [["Heavy Armour Master", 5]]}      // SUBTRACTED from it
      },
      "II": {...}, "III": {...},
      "note": "where the pool and the AC come from"
    },
    "b": {...},
    "notes": ["..."]
  },

  "profile": {
    "h2": "...",
    "scores": {                       // 10 axes, fixed order: single, aoe, durability, actions,
      "a": [[...10], [...10], [...10]],  // control-single, control-area, rescue, skills, saves,
      "b": [[...10], [...10], [...10]]   // endurance — one array per act; saves index 8 is null
    },
    "reads": ["—", "— B carries every crowd", ...10],  // "Reads as" column, optional
    "notes": ["..."],                 // r-notes under the table
    "concentration": {"a": false, "b": true},          // does this body hold a concentration spell?
    "saves": {                        // source of truth for the saves axis
      "a": {"I": {"prof": ["wis","dex"], "boosters": []}, "II": {...}, "III": {...}},
      "b": {"I": {"prof": ["wis","cha","con","dex"], "boosters": ["aura-of-protection"]}, ...}
    }
  },

  "damage": {
    "h2": "...",
    "reach": {"a": "hybrid", "b": "static"},   // ranged | hybrid | mobile | static
    "notes": ["..."]                           // extra callouts; the reach line and melee lock are automatic
  },

  "gates": {
    "h2": "...",
    "rows": [{"gate": "Hag's Hair", "skill": "Deception", "act": "I", "dc": "20",
              "owner": "a",                    // a | b | either | none  — none renders the row as a failure
              "mod": "+8", "pc": "45% cold · 83% on two rerolls", "source": "—"}],
    "note": "..."
  },

  "play": {
    "h2": "...", "intro": "...",
    "a": "A's turn", "b": "B's turn", "pair": "the interaction neither half has alone",
    "combos": [["Combo — name it", "trigger, effect, level it comes online"]],
    "failure": "..."
  },

  "prog": {
    "h2": "...",
    "rows": [{"lvl": 1, "flag": "milestone",   // milestone | respec | dead — omit for a plain row
              "a": ["Cleric 1", "Saves, skills", "—"],   // take, pick, feat
              "b": ["Monk 1", "...", "—"]}],
    "checkpoint": {"text": "..."}
  },

  "gear": {
    "h2": "...",
    "a": [["Weapon", "Target", 1, true], ["Armour", "—", "—"]],  // slot, target, act, win?
    "b": [...],
    "contested": [{"act": 1, "item": "Hag's Hair", "to": "a",    // a | b | both | either
                   "why": "...", "gives_up": "...", "win": true}],
    "note": "..."
  },

  "illithid": {                         // omit the block entirely for a pair that takes none
    "h2": "...", "intro": "...",
    "astral": "commune",                // commune | a | b | none — commune makes BOTH bodies
                                        // half-illithid off the one tadpole, so both inner rings open
    "picks": {                          // what each act ADDS, by scoring.py's POWERS keys.
      "a": {"I": ["psionic-overload", "cull-the-weak"], "II": [...], "III": [...]},
      "b": {"III": ["elevated-mind"]}
    },
    "notes": ["..."]
  },

  "quests": {
    "h2": "...",
    "rows": [{"act": 1, "reward": "...", "source": "...", "gate": "...", "to": "b", "win": true}]
  }
}
```

## The `derived` block, in particular

**Three of the ten axes are arithmetic, and this is where the arithmetic goes.**
`st`, `aoe` and `dur` are ratios to a fixed reference body (`axis-rubrics.md`
§1–§3), so the sheet authors the *inputs* — the action split, the raws, the
instance counts, the pool, the AC and the mitigation layers — and
`scripts/scoring.py` produces every ratio and every rung.

**A rung that disagrees with `profile.scores` refuses to render.** That is the
whole point of the block: before it existed the working lived in prose, and a
sheet could claim rung 5 above a derivation that gave 4 with nothing to catch
it. Fix the inputs or fix the score — the sheet may not carry both.

`damage` is the **same wire format the ledger uses**, so a chassis already in
`ledger-v7.json` can be lifted straight across. It fails closed on action-slots
that do not sum to 8, a short-rest pool underspent without a reason, a
levelled-slot body with no declared damage split, a raw with no instance count,
and a rider feeding one damage axis with no reason given.

**`mult` is how a pair sheet re-scores a chassis its partner changes.** The
ledger scores each body alone; a duo does not. Routine advantage is ×1.35 and
lands *after* the gear constant, because the rider rides the same roll. It
requires a `why`, because an accuracy correction is the one term par cannot
answer and so the one term that may never be applied silently. **A ledger
record may not carry one** — `validate_chassis` refuses it, for the reason rule
1 refuses named items: a buff a chassis only has beside one specific partner is
not a property of that chassis.

Most accuracy sources in this install are **target-side or ally-side**, which
is what makes them a pair effect at all: Blindness grants advantage to everyone
attacking the blinded creature, Spiteful Suffering marks a target, Battlemind
Link buffs the ally it is cast on. One body supplies them and *both* collect.
Reckless Attack is the exception that proves it — self-side and melee-only, and
already priced inside that chassis's own `st_raw`, so a sheet that also declares
a `mult` for it is charging advantage twice.

**Bounds.** `0.65 ≤ mult ≤ 1.35` — advantage and its mirror, straight from
`axis-rubrics.md`'s constants table. The rubric prices nothing outside that
pair. Keys are `st`, `aoe` and `why`; a misspelt axis is refused rather than
ignored, because ignoring it would apply nothing and score as though the
correction had been honest.

**Two tiers, in `scoring.ACCURACY`.** What an effect costs to keep up is most of
what it is worth:

| tier | what earns it | worth |
|---|---|---|
| **2** | no save, no concentration, encounter duration — Battlemind Link (Mesmerist 9), Nimbus of Pathos | **1.35** |
| **1** | save-gated or resource-gated — Snowlight's blind engine, Spiteful Suffering, Vow of Enmity, Feinting Blade | **1.19** |

Tier 2 is `1 − (1−h)² ÷ h` at `h = 0.65`. Tier 1 is `1 + 0.35 × s` at the
rubric's act-invariant `s = 0.55`: a save-gated effect delivers the advantage
only on the share of targets that fail it.

**A tier is a ceiling, not a value to copy.** The rubric applies the multiplier
to the **attack-roll portion of the raw only**, and most bodies are hybrids —
Snowlight's own §1 routine mixes weapon attacks with Snowblind ticks,
Retribution and Armour of Agathys, none of which is an attack roll. A body whose
raw is 60% attack rolls under a tier-1 source authors `1 + 0.6 × 0.19 = 1.11`
and says so in `why`. Authoring the bare tier over-credits every hybrid in the
roster, and the difference is a rung: Amethyst's Act III single-target reads
1.86 (rung **5**) at a flat 1.19 and 1.73 (rung **4**) at a 60% share.

**`dur.pool` counts self-healing, and only self-healing.** Second Wind, Lay on
Hands spent on yourself, temp HP on yourself, Durable's short rests. What a
body can aim at its *partner* is Rescue and is scored there; nothing is ever
scored in both.

## The illithid block, in particular

**Author the picks; nothing else.** `scripts/scoring.py` holds the 25-power tree with each
power's ring, axis and cost, and `render_pair.py` derives every number from the list. It
fails closed on an unknown power key, a ring-2 pick with no ring-1 power under it, an
inner-ring pick before Act III or on a body that never became half-illithid, a power picked
twice, a pre-astral holding above the 15 buyable outer powers, and a plan whose two halves
spend more tadpoles than the act supplies.

**Illithid Persuasion is never authored.** The first tadpole grants it; it carries the
2.5-charge base and the Illithid Mind tax hook but counts zero toward IMR. So a body listing
*n* powers holds *n* powers and has spent *n + 1* tadpoles, and the renderer emits the
Persuasion line itself in whichever act the body first takes anything.

**The block does not move the radar — you do.** `profile.scores` is still authored, and
`SKILL.md` §5a is explicit that a pair sheet scores the plan it authors rather than the
ledger's even share. Author the illithid block and the axis cells it earns in the same pass,
and say in a `profile.notes` entry which cells moved and why; a sheet whose prose claims an
illithid carry while both score columns sit at baseline is the inconsistency the §5a rule
exists to catch.

Scoring rules for the axes and the damage arithmetic live in `SKILL.md` §5a–§5b,
the gate arithmetic in `data/listo-10.2-backgrounds.md`. This file is the wire
format only.
