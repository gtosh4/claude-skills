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
| Whole damage-coverage table | from `profile.scores` (ST, AoE) + `damage.reach` |
| Idle-body flags (`u-idle`) | character under 3.0 in a fight type worth ≥40% of that act |
| Melee lock | applied, and its callout emitted, when neither reach is `ranged`/`hybrid` |
| Axis names, kinds, order, act bands | fixed; override with `profile.axes` / `.kinds` / `.labels` / `.bands` only if a sheet genuinely differs |
| Gate grade | `bad` when `owner` is `none`, else `ok` — set `grade` (`ok`\|`mid`\|`bad`) to override |

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

  "profile": {
    "h2": "...",
    "scores": {                       // 9 axes, fixed order: single, aoe, durability, actions,
      "a": [[...9], [...9], [...9]],  // control, sustain, skills, saves, endurance — one array per act
      "b": [[...9], [...9], [...9]]
    },
    "reads": ["—", "— B carries every crowd", ...9],   // "Reads as" column, optional
    "notes": ["..."]                  // r-notes under the table
  },

  "damage": {
    "h2": "...",
    "reach": {"a": "hybrid", "b": "static"},   // ranged | hybrid | mobile | static
    "notes": ["..."]                           // extra callouts; the reach line and melee lock are automatic
  },

  "gates": {
    "h2": "...",
    "rows": [{"gate": "Hag's Hair", "skill": "Persuasion", "act": "I", "dc": "20",
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

  "quests": {
    "h2": "...",
    "rows": [{"act": 1, "reward": "...", "source": "...", "gate": "...", "to": "b", "win": true}]
  }
}
```

Scoring rules for the axes and the damage arithmetic live in `SKILL.md` §5a–§5b,
the gate arithmetic in `data/listo-10.2-backgrounds.md`. This file is the wire
format only.
