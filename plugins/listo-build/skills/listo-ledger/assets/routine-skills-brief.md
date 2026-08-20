# Routine skills evidence pass

Record three skill modifiers, for three acts, for every chassis in your slice. Nothing else.

## Why these three

The Skills axis used to score five *named* gates. Four of them turned out to be buyable — the
Mirror of Loss can be passed by respeccing at Withers into Rogue 11 / Knowledge Cleric 1 and
respeccing back, and Hag's Hair, Araj's potion and the Mirror all have no-check routes to the same
ability point. What cannot be bought is the untelegraphed half of the run:

| check | skill | DC |
|---|---|---|
| traps and hidden caches | **Perception** | 15–25, every act |
| secret doors and switches | **Investigation** | 15–20, every act |
| routine town dialogue | **Persuasion** | act band: **I 10–15, II 15–18, III 18–22** |

These fire without warning, in whatever build is worn, so they measure the chassis rather than the
wallet. The whole axis now rests on these three numbers.

## What to record

The **finished number this body rolls**: ability modifier + proficiency bonus if proficient +
proficiency bonus again if it has Expertise + any permanent bonus it reliably carries.

**Record all three skills for all three acts, always — even at zero, even untrained.** This is the
one rule that changed. The previous pass let you omit a skill the body had nothing on, and an
absent value is now read as an evidence gap, not as "untrained". Untrained is a real number: the
ability modifier alone, with no proficiency bonus. Write it.

### Proficiency bonus — pinned, do not derive

    Act I: +3        Act II: +4        Act III: +5

Use these exact values. Do not compute them from character level and do not use any other
progression. They are the convention the six already-collected skills were built on, and mixing
conventions is the single failure this pass exists to avoid. (For the record: strict rules would
give Act III +6. The understatement is deliberate, uniform across every chassis, and therefore
does not move any chassis relative to another. Do not "correct" it.)

Expertise doubles the proficiency bonus, so an Expertise skill is `ability + 6 / +8 / +10`.

### Ability modifiers

The primary ability reaches 20 by character 6 (+5) and 22 by character 18 (+6). Everything else is
whatever the build actually allots — a Strength Fighter has no Charisma, and its Persuasion is
negative. **Negative numbers are expected and correct.** Roughly half of these bodies are bad at
two of these three skills; say so.

### Where proficiency and Expertise come from

Check all of these before deciding a body is untrained:

- **class and subclass skill lists** — `data/classes/<class>.md`, level-1 picks and later grants
- **race** — `data/listo-10.2-races.md`; Wood Elf Keen Senses is Perception proficiency
- **background** — `data/listo-10.2-backgrounds.md`
- **feats** — `data/listo-10.2-feats.md`; **Alert grants Perception proficiency** as a Listo
  addition, and Observant grants advantage on Perception to detect hidden objects

Only claim Expertise you can point at. **Rogue Expertise is a level-1 grant, not something a
Rogue 3 dip buys** — this exact error reached four chassis last pass.

**Two corrections to watch, both Listo-specific and both against the vanilla assumption:**

- **Knowledge Domain Expertise cannot reach Investigation here.** `data/classes/cleric.md:153`
  restricts its two double-bonus skills to **Arcana / History / Nature / Religion**. Vanilla
  guides route Investigation Expertise through Knowledge Cleric; that route does not exist in
  this build. An earlier version of this brief said otherwise — it was wrong.
- **Cleric taken as a later class grants no skill picks at all.** `Goon's Cleric Overhaul`
  "removes the free skill proficiencies BG3 wrongly gave a Cleric multiclass"
  (`data/classes/cleric.md:12`). Only a Cleric *first* class gets its starting picks.

### Two things that do not transfer

**Reliable Talent** (Rogue 11) and **Silver Tongue** (Eloquence Bard 3) are keyed on *being
proficient*, and the mod that shares skills across the party copies a flat number rather than a
proficiency. **Do not fold them into the modifier.** Note them in `uncertain` instead.

## Output

Write JSON to the path you are given. One object, keyed by chassis id, nothing else in the file:

```json
{
  "Ossuary": {
    "I":   {"Perception": 8, "Investigation": -1, "Persuasion": 0},
    "II":  {"Perception": 9, "Investigation": -1, "Persuasion": 1},
    "III": {"Perception": 10, "Investigation": -1, "Persuasion": 2},
    "uncertain": ["Death domain grants no skill; Perception is Wis 18 + Alert proficiency"]
  }
}
```

`uncertain` is optional, a list of strings, and belongs on any body where you had to make a call.
Every chassis in your slice must appear. All three acts, all three skills, integers only.
