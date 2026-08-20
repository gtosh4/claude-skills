# Tier-2 brief — choose the split, then score the body

For each subclass you are assigned you do two things: **pick its best twenty-level expression**,
then **score that body in full** — ten axes across three acts. Your output is the ledger's data.

## What you are given

Your assignment carries, per subclass, its **base profile**: the same subclass taken mono-20 and
scored in Act II by an earlier pass. That is the zero-dip reference point. Your split has to be
worth more than it, and the profile tells you where the body is already strong and where it is
empty.

## Read set

1. `listo-build/references/axis-rubrics.md` — **the authority on every value you write.** Each
   axis has a 0–5 ladder (what kind of capability a rung is) and an **act table** (what it must be
   in each act to hold that rung). Score against the act column, not the ladder headline.
2. `listo-build/references/scoring-model.md` — how the axes combine.
3. `listo-build/references/gates.md` — the named gates `skl` is scored against.
4. `listo-ledger/assets/ledger-schema.md` — output shape, the saves block, the booster registry.
5. `listo-ledger/assets/dip-catalogue.json` — **reference prose only.** Its `note` fields say what
   each class's levels buy and are worth reading for the split decision. **Ignore its numbers** —
   the delta scales are inconsistent between classes and must not be arithmetic you rely on.

Then only the class-file ranges your assignment names, which include every class's
`## Dip value` section — the authority for justifying the other half of a split.

## Part one — the split

**One to three distinct classes summing to 20, joined by ` / `, each with its subclass in
parentheses.** Your assigned subclass must take **more levels than any other class**.

```
Cleric 14 (Life) / Paladin 6 (Oath of Devotion)
Sorcerer 17 (Storm) / Cleric 1 (Tempest) / Fighter 2 (none)
```

Write `(none)` where a class is taken below its subclass level. **Mark the level-1 class with an
asterisk** — `Fighter 1* / Wizard 19 (Evocation)` — because only the level-1 class grants saving
throws and, for several classes, the good armour. If you do not mark one, the majority class is
assumed to be first.

**Dipping is close to free here.** Feats key off *character* level (3/6/9/12/13/15/18), so a
three-level dip costs no feats. Lone Wolf already grants two save proficiencies, so the classic
Fighter 1 for Constitution buys nothing. A dip costs only what the top of the abandoned class
table would have given — and outside a few real capstones, that is very little. **A mono-20 split
needs a specific reason**: name the late feature that beats the best three levels available
elsewhere.

**A feature you name must be one the split actually reaches.** Class files put a level on every
feature (`L13 Will Over Weave`); a `## Duo relevance` bullet praises the *whole* subclass, not the
three levels you are dipping into. This has shipped wrong before.

**One or two builds per subclass.** A second only if it is a genuinely different body — different
primary stat, different thing done with the turns, or a different resource clock. Two splits with
the same shape are one build.

## Part two — score the body

```jsonc
"Mercy": {
  "key": "cleric/Life",
  "split": "Cleric 14 (Life) / Paladin 6 (Oath of Devotion)",
  "reach": "static",
  "meta": "Wis 22 · 7 feats",
  "note": "One or two sentences: what the body is and what it gives up.",
  "concentration": true,
  "saves": {
    "I":   {"prof": ["wis","cha"], "boosters": []},
    "II":  {"prof": ["wis","cha","con","dex"], "boosters": ["aura-of-protection"]},
    "III": {"prof": ["wis","cha","con","dex"], "boosters": ["aura-of-protection"]}
  },
  "scores": {
    "I":   [1,2,3,2,1,2,4,1,null,2],
    "II":  [2,2,4,2,2,2,5,1,null,2],
    "III": [2,3,4,3,2,3,5,1,null,3]
  },
  "uncertain": ["anything you had to guess — omit if empty"]
}
```

The key is a **one-word, evocative chassis id**, unique — it becomes the ledger's identifier.
`key` is the subclass it came from.

**`scores`** — ten values per act, order `st, aoe, dur, act, ctrl_s, ctrl_a, rsc, skl, sav, end`.
**Index 8 is always `null`** — saves derive from the `saves` block.

**`saves.prof`** — the **resulting** set for that act, deduplicated: the level-1 class's two, plus
**Lone Wolf's two picks**, plus Resilient feats, Slippery Mind (Rogue 15), Diamond Soul (Monk 14),
Iron Mind (Gloom Stalker 7), Elegant Courtier (Samurai 7). Unlike the base profiles, this *is* the
character's full set.

**`saves.boosters`** — ids from `ledger-schema.md`'s registry, which now has 24. An effect with no
id goes in `uncertain`, never into the nearest-looking id.

Acts: **I** = characters 3–8, **II** = 9–15, **III** = 16–20.

## Act-relative scoring — where the last run went wrong

A 5 in Act I means "as good as a body can be at character 8", not "as good as a body ever gets".
**Most axes should not move between acts.** A body with Extra Attack and a rider is "the act's
standard multiattack plus a rider" at 8 and still that at 18 — a 3 in every act. It has not got
worse; the world moved with it.

The previous run produced **883 rises and 34 falls**. That is not what the run looks like; it is
what an absolute ladder looks like. Movement should be roughly symmetric:

- **Front-loaded bodies must fall.** Gloom Stalker, Assassin, Paladin 6's aura — anything whose
  plan is online by character 8 and then only gets bigger numbers. A 4 in Act I becoming a 3 in
  Act III is normal and correct.
- **Back-loaded bodies rise**: Fighter 11, Warlock 12, Monk 14, Rogue 15.
- **Flat features fall hard** — fixed dice with no upcast path against +126%/+170% HP.
- Everything else stays flat.

## Rules that decide values and are routinely missed

- **Lone Wolf is the floor**: 2 Actions, 2 Bonus, 2 Reactions, halved damage, +4 to two abilities
  with save proficiency in both. Score what the chassis adds **above** it.
- **One concentration spell per body.** Control costing none is worth a full rung more.
- **Self-healing is `dur`, not `rsc`.** Rescue is outward only. Damage redirection never exceeds 1.
- **Absolute Wrath is ON** — a body locked to one commonly-resisted damage type caps at 4 on `st`
  from Act II.
- **Save DCs decay**: bosses +1 per 7 levels, enemies +1 per 11. Pure save-DC control loses a rung
  by Act III; disadvantage-on-saves does not.
- **Eldritch Blast is 1d8 per beam here.** **`StackId` is a cap** — a summon carrying one replaces
  rather than accumulates.
- **Endurance counts at-will damage.** A body whose damage has no clock rates high regardless of
  slots — that is why Warlock sits above other casters and below martials.
- **Use the whole ladder.** `0` is a real value. Most bodies are 0 or 1 on several axes.
