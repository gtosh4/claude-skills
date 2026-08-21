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

## `exit_levels` — what the class gives up by stopping short

The other half of a split is the levels the **primary** class no longer has.

**Write one row per level, and write what THAT LEVEL grants** — not a running total. Consumption is
cumulative: the cost of capping at P is the sum of every row above P, so the totals take care of
themselves. **A level that grants nothing worth a rung gets no row**, and most levels won't.

```jsonc
"exit_levels": {"paragon": {"20": {"st": -1, "act": -1},   // the all-or-nothing capstone
                            "17": {"st": -1},              // 18 and 19 grant nothing here
                            "12": {"dur": -1}}}
```

Cover levels **12 through 20** — 11 is the minimum a majority class can hold, so nothing below 12
is ever lost. Do not write a row you cannot name a feature for; an absent row is the honest answer
and is much better than a guess, because a spurious rung here does not cost one split, it biases
every split of every subclass of that class.

> The **old** `exit` tables were cumulative-from-20 and banded at 11/14/17 only, with exactly one
> band applying. Two things went wrong with that and both are fixed by the format above. Levels
> snapped down — a primary at 16 paid the 14 band, so shaving one level was charged as three, and
> it is why the ledger holds 161 splits at primary 17 and 14 at primary 14. And re-stating a
> running total across bands is what produced this file's one real bug, where the consumer summed
> the bands it was supposed to choose between. `exit` is still read for any class that has no
> `exit_levels` row yet, so the two can coexist while the tables are rewritten class by class.

## `exit_levels_subclass` — the half that is not generic

Same format, keyed `<class>/<Subclass>`, and **summed on top of the class table**. The class table
carries the generic back half — spell-slot tiers, feats, Empty Body. This one carries what the
subclass alone loses, and it exists because that is the only place a duo question can be asked:

```jsonc
"exit_levels_subclass": {"monk/Way of the Open Hand": {"17": {"st": -1}},   // Quivering Palm
                         "monk/Way of the Friar": {}}                       // Community: nothing
```

Way of the Friar's level-17 Community bonds a second and third ally and is **dead weight in a
duo**; Open Hand's Quivering Palm at the same level is not. A table keyed by class cannot say
both, and until now charged Friar for a capstone it does not want.

**Most classes need no subclass table at all.** Check where the subclass actually finishes: Wizard's
school capstone is at 10, Druid's circle at 10, Bard's College at 14, and those never reach the
levels a split gives up. The six that need one are **Monk, Cleric and Rogue** (17), **Fighter and
Sorcerer** (18), and **Paladin** (the oath capstone at 20).

Note also what this format still cannot say: it speaks only in axis rungs, so it cannot express
losing a *booster*, a proficiency or an armour tier. Oath of the Moon's Lunar Champion at 20 is a
pair-scope save booster, and a Paladin capped at 17 loses it invisibly. Flag any such loss in
`note` rather than trying to spend a rung on it.

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
