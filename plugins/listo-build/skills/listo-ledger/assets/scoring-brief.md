# Chassis scoring brief

You score a batch of **chassis** for a two-player Lone Wolf Baldur's Gate 3 ledger. Your output
is JSON, one object per chassis, merged straight into `ledger.json` and rendered.

## Read set — in this order, in full

1. `listo-build/references/scoring-model.md` — how the axes combine and what the blocks are
2. `listo-build/references/axis-rubrics.md` — **the authority on what each rung means.** Every
   value you write is a claim against a rung in this file.
3. `listo-build/references/gates.md` — the named gates the `skl` axis is scored against
4. `listo-ledger/assets/ledger-schema.md` — the output shape, the saves block, the closed enums

All four are under `/var/home/gordon/claude-skills/plugins/listo-build/skills/`.

Then read **only** the class-file line ranges your assignment names. Do not open other class
files, `listo-rules.md`, `listo-build/SKILL.md`, the manifest, or any `.pak`.

## What you emit

For each chassis in your assignment, one object keyed by its `chassis` id:

```json
"Bombard": {
  "reach": "hybrid",
  "split": "Blood Hunter 14 (Order of the Profane Soul) / Wizard 6 (Evocation)",
  "meta":  "Int 22 · 7 feats",
  "note":     "One or two sentences: what the body is and what it gives up.",
  "strength": "One or two sentences: why it is strong FOR THIS RUN — two bodies, Lone Wolf, Listo's encounters.",
  "wants":    "One sentence: what it needs from the other half of the duo, as a capability not a class.",
  "concentration": false,
  "types": ["slashing","radiant"],
  "saves": {
    "I":   {"prof": ["int","dex"], "boosters": []},
    "II":  {"prof": ["int","dex","con","wis"], "boosters": []},
    "III": {"prof": ["int","dex","con","wis"], "boosters": []}
  },
  "scores": {
    "I":   [3,2,3,2,2,1,0,3,null,4],
    "II":  [4,4,3,3,4,2,0,3,null,4],
    "III": [4,4,3,3,4,2,0,3,null,4]
  },
  "uncertain": ["anything you had to guess, one line each — omit if empty"]
}
```

Keep the `split` **exactly** as your assignment gives it, parenthesised subclasses and all, unless
the class text proves it wrong; if you change it, say so in `uncertain`. Splits are 1–3 distinct
classes summing to 20, joined by ` / `, each class named once with its total and its subclass in
parentheses. No arrows, no repeated class. The parentheticals are what lets a reader rebuild the
body — never strip them.

### `note`, `strength` and `wants` — all three are required

Ten integers say *how much*. They cannot say why you would pick this body, or who it needs beside
it, and those are the two questions the roster card exists to answer.

- **`note`** — what the body is, and what it gave up. 1–2 sentences.
- **`strength`** — what makes it strong **in this scenario specifically**: two characters, Lone
  Wolf's 2 Actions / 2 Bonus Actions / 2 Reactions and halved damage, Absolute Wrath's layered
  resistances, +126% enemy HP, a long rest costing 120+ supplies. "Good damage" is not an answer —
  a four-body party would say the same. Name the thing that is only true *here*: a second Action
  doubling a bonus-action engine, an aura that covers the whole party because the party is two, a
  short-rest clock against expensive long rests, a damage type nothing resists.
- **`wants`** — what it needs from the **other** body, phrased as a capability, never a class.
  "Wants a Cleric" is unusable; every duo can respec. "Wants a body that will hold the pair's one
  concentration slot, because this one never can" is usable. Where an axis sits at 0, say so —
  `listo-build`'s split rule is that 5 + 0 is worse than 3 + 3, so a hole is what the partner is for.

### `scores` — ten values per act, in this order

    st, aoe, dur, act, ctrl_s, ctrl_a, rsc, skl, sav, end

**Index 8 (`sav`) is always `null`.** It is derived from the `saves` block by the renderer;
authoring a number there is a hard error. See `ledger-schema.md`, "The saves axis is authored as
a set, not a number", for `prof`, `boosters` and which features grant what.

Acts: **I** = characters 3–8, **II** = 9–15, **III** = 16–20.

### Act-relative means the ladder re-baselines, and this is where the last run went wrong

A 5 in Act I means "as good as a body can be at character 8", **not** "as good as a body ever
gets". Act I's rung 5 and Act III's rung 5 are different configurations, because Act I has two
feats and 4th-level slots while Act III has seven feats and 9th. `axis-rubrics.md` carries a
per-act ceiling row under every axis table — read the row for the act you are scoring, not the
axis table's headline.

**The consequence people miss: most axes should not move at all.** A body whose heavy armour,
save set or rescue kit does not improve holds its rung; it has not got worse, the world moved with
it. Only a body whose *standing relative to its peers* changes should move.

**`st` and `aoe` are the exception and are meant to move.** Both are now computed as a ratio to a
fixed par that carries the act's enemy-HP multiplier (`axis-rubrics.md`, "The two damage axes are
computed, not judged"). Extra Attack plus a flat 1d6 rider is 1.29× par in Act I and 0.87× in
Act III — **3 / 2 / 2** — because a flat rider genuinely is being outrun. Do not flatten those
rows to match the other eight.

The last scoring run produced **883 rises and 34 falls** across 150 chassis. That is not what the
run looks like; it is what an absolute ladder looks like. Movement is meant to be roughly
symmetric:

- Bodies that **front-load** must fall: Gloom Stalker, Assassin, Paladin 6's aura, anything whose
  whole plan is online by character 8 and then only gets bigger numbers. A 4 in Act I becoming a 3
  in Act III is a normal, correct thing to write.
- Bodies that **back-load** rise: Fighter 11, Warlock 12, Monk 14, Rogue 15.
- Bodies with a **flat feature** fall hard — fixed dice with no upcast path against +126%/+170% HP.
- Everything else stays flat.

Before you write a chassis's three acts, ask: *is this body better than its contemporaries in Act
III than it was in Act I?* If the honest answer is "no, it just has bigger numbers, like everyone
else", write the same value three times.

### `types` — required, and easy to forget

The damage types this body routinely deals, from the closed set: `acid bludgeoning cold fire force
lightning necrotic piercing poison psychic radiant slashing thunder`. One to three entries is
normal. **The renderer raises if it is missing** — Absolute Wrath means two bodies sharing a single
damage type have no answer when it is resisted, and that is a pair property the renderer can only
compute if both bodies declare what they deal.

### `reach`

One of `ranged` `hybrid` `mobile` `static`. Closed enum; an unknown value is a hard render error.

### `meta`

The primary stat at its Act III value, **the attack stat too whenever it differs**, and the feat
count. `Wis 22 · Dex 20 · 7 feats`. One stat is right only when one stat does both jobs —
`Int 22 · 7 feats` for a Wizard, or for a Battle Smith, where Intelligence rolls the attack.

A third of the last roster named a caster stat and nothing else on a body that swings a weapon:
Monk (Wis primary, **Dex** attacks), Paladin (Cha/Str), Inquisitor (Wis/Str), Mesmerist (Cha/Dex),
Artificer outside Battle Smith (Int/Dex), Paragon outside Spellblade (Cha/Str), and War, Tempest
or Swords bodies under a Cleric or Bard. `meta` is display-only and changes no score, which is
exactly the problem — it is the line a reader checks the damage arithmetic against, and a record
reading `Wis 22` alone gets read as a +4 attack modifier when the body has +5 or +6. That misread
is worth a full rung on `st`. Lone Wolf's +4 lands on **two** abilities, so both stats are at 20
from level 1; say which one carries the 22.

## Lone Wolf is the floor, not a bonus

Both bodies have Lone Wolf from level 1: **2 Actions, 2 Bonus Actions, 2 Reactions, halved damage
from all sources, +4 to two abilities with save proficiency in both**. Score what the chassis adds
**above** that floor. Two Actions is baseline — a chassis does not earn `act` for having them.

The Lone Wolf save proficiencies are two of the entries in `prof`, and they are **deduplicated**
against the level-1 class's two: a Blood Hunter's `int + dex` under a Lone Wolf `int + dex` pick
is two entries, not four.

## Rules that decide values, and are routinely missed

- **One concentration spell per body.** Control that spends no concentration is worth a full rung
  more than control that does.
- **Self-healing is `dur`, not `rsc`.** Rescue is outward only — what this body aims at its
  *partner*. Damage redirection (Warding Bond, Protective Bond) **never scores above 1**: in a duo
  it moves damage from one half of the party to the other.
- **Absolute Wrath is ON.** Ordinary enemies carry layered resistances. A body locked to one
  commonly-resisted damage type **caps at 4** on `st` from Act II.
- **Combat Extender: +126% regular and +170% boss HP.** A flat feature with no upcast path *falls*
  across the acts. Eldritch Cone/Line stops scaling at character 10.
- **Save DCs decay**: bosses +1 spell save DC per 7 levels, enemies +1 per 11. Pure save-DC
  control loses a rung by Act III. Disadvantage-on-saves does not.
- **Eldritch Blast is 1d8 per beam here**, not 1d10.
- **`StackId` is a cap.** A summon or brand carrying one *replaces* rather than accumulates.
- Feats land at **class** level **3/6/9/12/13/15/18**, plus **11 for Fighter and Rogue only** — so the
  budget is `floor(A/3) + floor(B/3) + ...`, **+1 per class reaching 13**. `20`, `17/3` and `14/3/3`
  all pay 7; a split where **no class reaches 13** pays 6 (`11/6/3`, `12/8`). Count it, do not assume 7.
- The primary stat reaches **20 by character 6, 22 by 18**.

## Calibration — use the whole ladder

A batch where everything lands on 3 and 4 is a batch that was not scored. **Be willing to write
0, 1 and 2.** Most chassis are 0 on most axes: a Fighter has no `rsc`, a Cleric has no `end` in
the Sneak-Attack sense. `end` is the long-rest budget axis — at-will damage with no clock is 5,
and a body that runs out of resources in two fights is 1.

`0` is a real value and means the body does not do this thing at all. Write it.

## Fail closed

If you cannot justify a value from the rubric and the class text, **do not guess silently** — pick
the value you can defend and list the doubt in `uncertain`. A booster or feature the renderer does
not recognise scores as nothing, which is indistinguishable from an honest low score; the
`uncertain` list is what makes that visible.

**Do not invent `boosters` ids.** `ledger-schema.md` carries the full table — seventeen ids across
three tiers, expanded after the last run found ten real blanket save effects with no id. Read that
table before you decide a feature is unrepresentable. If a feature genuinely deserves an id and is
not on the list, put it in `uncertain` rather than reaching for the nearest one.
