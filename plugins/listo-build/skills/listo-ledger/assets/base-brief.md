# Tier-1 brief — one base profile per subclass

You score **base profiles**. A base profile is a subclass taken for **all twenty levels, with no
multiclassing**, scored coarsely on the ten axes in **Act II**.

**A base profile is not a recommendation.** Almost none of these bodies should actually be played
mono-class — dips are close to free in this list, because feats key off *character* level
(3/6/9/12/13/15/18) — see below. The mono-20 profile is the **zero-dip
reference point**: the thing every split of this subclass is measured against. Score it as what
the subclass does on its own, not as what you would build.

**You choose no splits.** Nothing here names another class. That decision happens later, against
this profile plus a catalogue of what each dip contributes. Do not speculate about it.

## Read set

1. `listo-build/references/axis-rubrics.md` — **the authority on what each rung means.** Every
   value you write is a claim against a rung in this file. Read it in full.
2. `listo-build/references/scoring-model.md` — how the axes combine and what the blocks are.
3. `listo-build/references/gates.md` — the named gates the `skl` axis is scored against.

Then read **only** the line ranges your assignment names. Those cover your classes' own sections
**and** the spell-access ranges — the mods change caster lists enormously (a Wizard's level-1 pick
pool is **45** against vanilla's 23, and Bard's Magical Secrets is the largest single grant in the
modlist), so `aoe` and both control axes cannot be scored honestly without them. Do not open other class
files, `listo-rules.md`, the manifest, or any `.pak`. You do not need any class's `## Dip value`
section — you are not choosing a split.

All paths are under `/var/home/gordon/claude-skills/plugins/listo-build/skills/`.

## Output contract

Raw JSON only. One object, keyed exactly as your assignment lists the keys.

```json
{"cleric/Life": {
  "verdict": "candidate",
  "scores": [2,2,3,4,2,2,5,1,null,2],
  "prof": ["wis","cha"],
  "armour": "heavy",
  "shield": true,
  "primary": "wis",
  "concentration": true,
  "why": "Rescue ceiling of the list; nothing else on the table clears competent."
}}
```

| verdict | when | required |
|---|---|---|
| `candidate` | the subclass is real and buildable | everything above |
| `dupe` | it **is** another assigned subclass, mechanically | `dupe_of` `why` |
| `none` | nothing verifiable to build on | `why` |
| `not-a-subclass` | the heading is a table or a note | `why` |

**Emit no other fields.** No chassis name, no split, no niche, no peak. Names are assigned later,
centrally, so that they can be checked for collisions across all seventeen classes at once.
`src` and `deps` stamps are written by `seed_index.py --stamp`; inventing one would mark a
judgement as verified against source you never read.

## `scores` — ten values, Act II, in this order

    st, aoe, dur, act, ctrl_s, ctrl_a, rsc, skl, sav, end

**Index 8 (`sav`) is always `null`.** It is derived from `prof` by the renderer. Authoring a
number there is a hard error.

**Act II** is characters 9–15 — 5–6 feats, 8th-level slots. Judge at **character 12–13**, the
middle of the band, so that two people scoring the same subclass land in the same place.
Act II because it is the richest band: almost every run-defining breakpoint lands there.

Rungs are **act-relative**, and `axis-rubrics.md` now separates the two halves of that explicitly:

- the **0–5 ladder** is what *kind* of capability each rung is. Act-invariant.
- the **act table** is what that capability has to *be* in each act to hold the rung. This is
  where act-relativity lives, and it is anchored for **every rung from 2 up**.

**Score against the Act II column of the act table**, not against the ladder's headline and not
against what the feature was worth when the body first got it. Rungs 0 and 1 carry no act row —
they are act-invariant by construction, since "has nothing" and "has an incidental" do not change
between acts.

**Use the whole ladder.** Most subclasses are 0 or 1 on several axes. A Fighter has no `rsc`; a
Wizard has no `end` in the at-will sense. `0` is a real value and means the body does not do this
thing at all. A profile that lives on 3 and 4 was not scored.

## The grants — set-valued, not numbers

These describe what the class gives **at level 1**, because only the level-1 class grants saving
throws and the good armour. They are recorded separately from `scores` precisely because they do
not add — they union.

- **`prof`** — the two saving throws **this class** grants at level 1, lowercase from
  `str dex con int wis cha`. Just this class's two. Do **not** add Lone Wolf's pair, Resilient, or
  anything else; those are composed in later.
- **`armour`** — best category at level 1: `null`, `"light"`, `"medium"`, `"heavy"`.
- **`shield`** — true or false.
- **`primary`** — the ability the build must take to 20 by character 6 and 22 by 18.
- **`concentration`** — true if this subclass's plan rides a concentration spell.

## Lone Wolf is the floor, not a bonus

Both bodies have it from level 1: **2 Actions, 2 Bonus Actions, 2 Reactions, halved damage from
all sources, +4 to two abilities with save proficiency in both.** Score what the subclass adds
**above** that floor. Two Actions is baseline — a body does not earn `act` for having them.

## Rules that decide values and are routinely missed

- **One concentration spell per body.** Control costing no concentration is worth a full rung more.
- **Self-healing is `dur`, not `rsc`.** Rescue is outward only — what this body aims at its
  *partner*. Damage redirection never scores above 1: in a duo it moves damage from one half of
  the party to the other.
- **Absolute Wrath is ON.** A body locked to one commonly-resisted damage type **caps at 4** on
  `st` from Act II.
- **Combat Extender: +126% regular and +170% boss HP.** A flat feature with no upcast path falls
  across the acts. Eldritch Cone/Line stops scaling at character 10.
- **Save DCs decay**: bosses +1 spell save DC per 7 levels, enemies +1 per 11. Pure save-DC
  control loses a rung by Act III; disadvantage-on-saves does not.
- **Eldritch Blast is 1d8 per beam here**, not 1d10.
- **`StackId` is a cap.** A summon or brand carrying one *replaces* rather than accumulates.
- **Archive versions lag mod pages.** If the class file records drift, trust the class file.

## Fail closed

If you cannot justify a value from the rubric and the class text, pick the one you can defend and
list the doubt in an `uncertain` array on that subclass. A feature that scores as nothing is
indistinguishable from an honest low score; the `uncertain` list is what makes that visible.


## The response shape — two maps, one response

You return one object with exactly two top-level keys:

```jsonc
{
  "bases": {
    "ranger/Gloom Stalker": {
      "verdict": "candidate",
      "scores": [2, 3, 2, 3, 2, 1, 2, 4, null, 3],
      "prof": ["str", "dex", "wis", "int"],
      "boosters": [],
      "armour": "medium",
      "shield": true,
      "primary": "dex",
      "concentration": false,
      "why": "…",
      "uncertain": []
    }
  },
  "arrives": {
    "ranger/Gloom Stalker": {"wis": 7, "int": 7}
  }
}
```

`bases` is this brief's contract. `arrives` is `grants-brief.md`'s, and it is returned here rather
than by a second pass because you have already read everything it needs: the grant fields say
**what the body holds at level 20**, and `arrives` says **which of those turn up after level 1**.
Use the ability name for a save, `armour` / `shield` for those, and the booster id for a booster.

Three rules the merger enforces, all for the same reason — a grant nothing applies is an
understated save score, and an understated score reads exactly like an honest one:

- **Every subclass in `bases` needs an entry in `arrives`.** Write `{}` when the subclass adds
  nothing after level 1. Omission is an evidence gap, not a "no".
- **Nothing arrives at level 1.** That is what the base profile's own grant fields already record.
- **`arrives` cannot name a grant the profile does not hold.** It annotates the profile; if a save
  turns up at 7 it is also in `prof`.
