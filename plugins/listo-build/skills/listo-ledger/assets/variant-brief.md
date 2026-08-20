# Variant brief — the second answer for a subclass

You are given bodies that already exist and are already scored. For each, build a **different
twenty-level expression of the same subclass**, then score it in full.

This is not a re-score and not a correction. The existing body stays. You are filling in a corner
of the design space that the first pass missed.

## Why this pass exists

The first pass batched agents by class, and each agent found one good dip per class and applied it
to every subclass of it. The result:

```
Wizard     12 of 16 bodies took Cleric 1        0 of 15 Cleric-1 bodies reach the frontier
Druid       8 of 12 bodies took Cleric 3        every Druid scored exactly 1.0 on skills
Barbarian   6 of 14 bodies took Fighter 3       the best Barbarian in fourteen scored 0.7 on skills
```

A worked example of what was lost. Two bodies, same subclass, same levels, one dip apart:

```
Monk 17 (Ascendant Dragon) / Cleric 3 (Tempest)    a damage body  — built
Monk 17 (Ascendant Dragon) / Cleric 3 (Twilight)   a rescue body  — never built
```

Both are real. The second was found only by comparing against a hand-built document. **That is the
kind of thing you are looking for.**

## The variant axis is partner demand

A body is built to be half of a pair. The question that decides the dip is **what does this body
want its partner to bring** — and therefore what it must bring itself. Same subclass, different
answer, different body.

Four rough shapes. They are deliberately loose; their only job is to make the dip decision more
than once:

| shape | what the body brings | what it demands of a partner |
|---|---|---|
| **specialist** | one axis pushed as high as the act allows | everything else, including its own floor |
| **self-sufficient** | its own skills, saves and endurance; no holes | a free hand — the partner can specialise into anything |
| **enabler** | turns spent raising the partner rather than itself | a partner whose ceiling is worth raising |
| **anchor** | the pair's floor — durability, saves, staying power | the damage |

Pick the shape the existing body **is not**, then choose the dip that serves it.

## What makes a variant real

- **The dip must differ** — a different class, or the same class at a level that changes what it
  buys. `Cleric 1` to `Cleric 3` is a real change (Channel Divinity, a domain); `Fighter 2` to
  `Fighter 3` usually is not.
- **The outcome must differ.** At least one axis moves by two rungs, or the body's best axis
  changes. If you score it and it looks like the existing body, you picked the wrong dip — say so
  in `uncertain` and pick again.
- **Skills are the axis most often left at zero, and the model weights them 2.5.** Two characters
  carry every proficiency the run will ever have. A three-level Rogue or Bard dip buys Expertise
  and costs no feats. That is not the only answer, but it is the one nobody reached for.
- **Do not force it.** If a subclass genuinely has one expression, say so in `uncertain` and emit
  nothing for it. An invented variant is worse than an absent one.

## Read set

1. `listo-build/references/axis-rubrics.md` — the authority on every value. Score against the
   **act table** row for the act, not the ladder headline.
2. `listo-build/references/scoring-model.md`, then `gates.md`, then
   `listo-ledger/assets/ledger-schema.md` for the output shape and the 24-id booster registry.
3. Only the class-file ranges your assignment names, plus every class's `## Dip value` section —
   the authority for the other half of a split.

## Output

One JSON object keyed by a **proposed** chassis name. Names are reconciled centrally afterwards,
so a collision costs nothing — pick something evocative and move on.

```jsonc
"Proposed": {
  "key": "monk/Way of the Ascendant Dragon",   // the subclass, copied from the assignment
  "variant_of": "Wyrmcall",                    // the existing body this is an alternative to
  "shape": "anchor",                           // which of the four you built toward
  "split": "Monk 17 (Way of the Ascendant Dragon) / Cleric 3 (Twilight Domain)",
  "reach": "mobile", "meta": "Wis 22 · 7 feats",
  "note": "One or two sentences: what this body is and what it gives up.",
  "concentration": false,
  "saves": {"I": {...}, "II": {...}, "III": {...}},
  "scores": {"I": [...], "II": [...], "III": [...]},
  "uncertain": []
}
```

Same rules as the first pass: ten values per act in the order `st, aoe, dur, act, ctrl_s, ctrl_a,
rsc, skl, sav, end`; **index 8 always `null`**; `saves.prof` is the character's full resulting set
per act including Lone Wolf's two picks; splits are 1–3 distinct classes summing to 20 with the
assigned subclass taking the most levels and the level-1 class marked `*`.

**Most axes should not move between acts.** Front-loaded bodies fall, back-loaded ones rise, and
the rest stay flat.
