# Evidence brief — skill modifiers and damage types

Every chassis in the ledger is already scored. This pass adds **two fields** to each and changes
no existing value. You are not re-scoring anything.

## Why

Two axes are now **derived from evidence** rather than authored as a rung, for opposite reasons.

**Skills.** `Use Highest Modifier in dialogue` reads every party member's total for all eighteen
skills and boosts the roller to the party maximum. So a gate is cleared if **either** body clears
it — the combination happens on modifiers, before any rung exists. The old operator normalised
against 7, so a pair where one body cleared everything scored 0.71 while the host was actually
rolling at the party maximum and clearing every gate.

**Damage types.** Absolute Wrath layers resistances on ordinary enemies. The rubric already caps a
single body at 4 on `st` for one commonly-resisted type; the pair had no such rule, so two bodies
dealing the same type still summed linearly. A duo with one damage type between them has no answer
at all when that type is resisted.

## What to emit

For each chassis you are assigned, exactly two fields:

```jsonc
"Lectern": {
  "skills": {
    "I":   {"Deception": 6, "Intimidation": 4, "Religion": 3, "Perception": 7,
            "Investigation": 3, "Sleight of Hand": 4, "Athletics": 2},
    "II":  { ... },
    "III": { ... }
  },
  "types": ["bludgeoning", "radiant"]
}
```

### `skills` — the body's own total modifier, per act

The **finished number this body rolls**, not a rung: ability modifier + proficiency bonus +
Expertise if it has it + any permanent item or feature bonus it reliably carries. One entry per
gate skill the body has anything on; omit a skill it has nothing on rather than writing a guess.

Only these gate the run, so only these are read:

    Acrobatics  Athletics  Deception  Intimidation  Investigation
    Medicine  Perception  Persuasion  Sleight of Hand

**Perception, Investigation and Persuasion are mandatory on every body in every act**, including
untrained ones at a negative modifier — they carry the untelegraphed half of the axis and an
absent value reads as an evidence gap. The rest may be omitted when the body has nothing on them.
**Religion is no longer scored**: its only gate was the Mirror of Loss, which is respec-buyable.

Act bands are characters **3–8 / 9–15 / 16–20**. **Proficiency bonus is pinned at +3 / +4 / +5 by
act — use these exact values and do not derive them from character level.** An earlier pass left
this as a range and one agent read it as +2/+3/+4 while the rest used +3/+4/+5, which needed 47
chassis corrected by hand. (Strict rules would give Act III +6; the understatement is deliberate
and uniform, so it moves no chassis relative to another. Do not "correct" it.) The primary stat
reaches 20 by character 6 and 22 by 18. A body that gains Expertise or a
skill grant mid-run should show the jump between acts.

**Two things do not transfer to the partner** and so belong only to the body that owns them:
**Reliable Talent** (Rogue 11) and **Silver Tongue** (Eloquence Bard 3). They are keyed on *being
proficient*, and the mod copies a flat number, not a proficiency. Record them in the owner's
modifier and say so in `uncertain`; do not spread them across the pair.

### `types` — every damage type this body can reliably deliver

From this closed list:

    acid  bludgeoning  cold  fire  force  lightning  necrotic
    piercing  poison  psychic  radiant  slashing  thunder

**Reliably** means its normal routine, not a one-off scroll or a single prepared spell it might
not have taken. A Monk punching is `bludgeoning`; add `radiant` only if the subclass actually
converts. A blaster with real access to two elements records both. Most bodies have one or two;
three or more is a genuinely flexible body and should be rare.

## What the gates are

The rung falls out of these, so it is worth knowing what you are scoring against:

| act | gate | check |
|---|---|---|
| I | Auntie Ethel's Hair | **Deception 20** or **Intimidation 15** |
| I | Free Us (prologue) | **Investigation 10**, **Medicine 10**, **Athletics 10** or **Acrobatics 10** |
| I | Gauntlet trap | **Perception 15** |
| II | Araj's potion | **Sleight of Hand 20** |
| III | Mirror of Loss | **Religion 25** — the hardest single check in the run |

The inspiration bank is vanilla: four charges, each a full reroll. Two rerolls turn a 45% check
into 83%, which is what makes the upper rungs reachable at all.

## Output

Raw JSON, one object keyed by chassis id, containing only `skills`, `types` and optionally
`uncertain`. **Do not emit `scores`, `saves`, `split`, `note` or anything else** — those already
exist and will not be overwritten.
