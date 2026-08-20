# Dip catalogue brief — what each class contributes to a split

You are converting prose that already exists into structured data. Every class file carries a
`## Dip value` section written for exactly this question, plus a subclass list with levels against
every feature. Your job is transcription plus judgement, not research.

## What this is for

A base profile is a subclass at twenty levels. A **split** trades some of those levels for another
class. To search that space mechanically we need, per class and per breakpoint, what those levels
buy — so that `Fighter 14 / Rogue 6` can be composed from parts instead of guessed.

**Composed vectors never get published.** They rank candidate splits so that expensive full
scoring is spent on the survivors. So these numbers are **filter-grade**: good enough to order
variants of one subclass against each other, and not claimed to be more.

## The two halves of an entry

**Grants are set-valued and do not add.** Saving throws, armour category, shields. Two grants of
heavy armour is heavy armour. These union or take the best.

**Deltas are additive**, in axis rungs, and are applied with **headroom damping** — a delta of
`+2` on a body already at 4 moves it far less than on a body at 1. Write the delta as *what this
buys a body that does not already have it*; the composition engine handles the damping.

## `as_first` versus `as_dip`

**Only the level-1 class grants saving throws**, and for several classes only the level-1 class
grants the good armour. So every entry has two sides, and exactly one class in a split is first.

```jsonc
"barbarian/1": {
  "as_first": {"grants": {"prof": ["str","con"], "armour": "medium", "shield": true},
               "deltas": {"dur": 2, "st": 1}},
  "as_dip":   {"grants": {"prof": [], "armour": "medium", "shield": true},
               "deltas": {"dur": 1, "st": 1}},
  "requires": null,
  "conflicts": ["rage"],
  "note": "Str + Con saves and the d12 only when first. Rage and armour from any position."
}
```

Read each class's own multiclassing rules — they differ. Paragon withholds heavy armour, saves
*and* skills on a late dip but still grants shields and martial weapons. Wizard grants nothing at
all when multiclassed into. Rogue gives light armour and one skill, no Expertise.

## Subclass parts

A dip usually picks a subclass, and subclasses differ enormously. Emit the class-generic part at
each breakpoint **and** a part per subclass worth taking as a dip:

```jsonc
"rogue/3":        { ... class-generic: Cunning Action, Sneak Attack 2d6 ... },
"rogue/3/Thief":  {"deltas": {"act": 1}, "conflicts": ["bonus-action-attack"],
                   "note": "A second Bonus Action on top of Lone Wolf's."}
```

A subclass part normally carries **deltas only** — the grants come from the class-generic part at
the same level, and a build takes the generic part plus at most one subclass part.

**Exception: a subclass that grants proficiency the base class does not.** Favored Soul's medium
armour and shields, College of Valour's martial package, Armorer's heavy armour at 3. Put those in
a `grants` object on the subclass part, exactly as a generic part does. Do **not** price armour as
a `dur` delta — armour is set-valued, and a delta would double-count against the armour floor.

## Breakpoints

Emit an entry for each level a dip is genuinely taken at — the `## Dip value` section names them.
Typically 1, 2, 3, 5, 6, and sometimes 9, 11 or 12 where a real breakpoint sits. Do not emit an
entry per level; emit them where the class has something to sell.

## `exit` — what the class gives up by stopping short

The other half of a split is the levels the **primary** class no longer has. Emit one exit table
per class, keyed by the level it stops at, as negative deltas relative to its full twenty:

```jsonc
"exit": {"paragon": {"17": {"st": -1},
                     "14": {"st": -1, "act": -1},
                     "11": {"st": -2, "act": -1, "dur": -1}}}
```

This is where a strong capstone shows up. Paragon's own file says the level-20 capstone is
reachable only by pure Paragon 20 and calls the class all-or-nothing in both directions — that
should read as a heavy exit cost. A class with a weak back half should read as a light one.
Use levels **17, 14 and 11** — 11 is the minimum a majority class can hold.

## Fields

- **`requires`** — `null`, or a condition on the rest of the build. `{"primary": "cha"}` means the
  deltas apply in full only on a Charisma body; otherwise they are halved. Use it for stat-gated
  dips such as Spellblade's Charisma-to-attack.
- **`conflicts`** — tags this part competes for. Two parts sharing a tag do not stack; the larger
  applies. Use existing tags where they fit: `extra-attack`, `bonus-action-attack`, `expertise`,
  `heavy-armour`, `sneak-attack`. Invent a new tag only for a genuine non-stacking clash, and say
  what it means in `note`.
- **`note`** — one sentence. What these levels actually buy.

## Axis keys

    st, aoe, dur, act, ctrl_s, ctrl_a, rsc, skl, sav, end

Do **not** write a `sav` delta. Saves are derived from the `prof` grants, never from a rung.

## Read set

Only the line ranges your assignment names: each class's at-a-glance, subclass section and
`## Dip value` section. You need nothing else — not the rubric, not the spell lists.

## Output

Raw JSON, one object. Keys are `<class>/<levels>` and `<class>/<levels>/<subclass>`, plus one
`exit` object holding your classes' exit tables. No prose, no fences.
