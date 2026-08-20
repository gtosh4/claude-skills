# Correction pass — grants at level 20

The tier-1 base profiles are scored and good. One field group in them was specified wrongly and
needs redoing: **the grants**. Nothing else about the profiles changes, and you are not rescoring
anything.

## What was wrong

A base profile is a subclass taken for **all twenty levels**. The original contract asked for the
saving throws and armour the class grants **at level 1**, on the reasoning that only a level-1
class grants saves. That is true of *classes* and false of *subclasses* — and a mono-20 body's
level-1 class is itself, so it holds everything it ever gains.

Three tier-1 agents independently reported the same consequence. Examples they named:

- `ranger/Gloom Stalker` — **Iron Mind** at 7 grants Wisdom *and* Intelligence saves
- `fighter/Samurai` — **Elegant Courtier** at 7 grants a third save proficiency
- `rogue/*` — **Slippery Mind** at 15 adds Wisdom; `monk/*` — **Diamond Soul** at 14 adds all six
- `bard/College of Valour`, `bard/College of Swords` — medium armour and shields at 3
- `artificer/Armorer` — heavy armour at 3
- `fighter/Brute` — **Brutish Durability**, a registry booster the record had no field for at all

The saves axis is *derived* from these fields, so an understated grant is an understated score on
the heaviest-weighted axis in the model, and it is invisible downstream.

## Your job

For each subclass you are assigned, emit the four grant fields **as the body holds them at level
20**, plus the level each non-level-1 grant arrives at.

```json
{"ranger/Gloom Stalker": {
  "prof": ["str", "dex", "wis", "int"],
  "boosters": [],
  "armour": "medium",
  "shield": true,
  "arrives": {"wis": 7, "int": 7}
}}
```

- **`prof`** — every saving throw proficiency at 20, deduplicated, lowercase from
  `str dex con int wis cha`. The class's level-1 pair **plus** anything the subclass adds later.
  Do **not** add Lone Wolf's pair or Resilient; those belong to the character, not the subclass.
- **`boosters`** — ids from the registry table below. An effect with **no id** goes in
  `uncertain`, never into the nearest-looking id: an unrecognised booster contributes nothing,
  which is indistinguishable from an honest low score.
- **`armour`** — best category reached by 20: `null`, `"light"`, `"medium"`, `"heavy"`.
- **`shield`** — true if the body has shield proficiency at 20.
- **`arrives`** — `{grant: level}` for everything **not** granted at level 1. Use the ability name
  for a save, `"armour"` / `"shield"` for those, and the booster id for a booster. Omit it if the
  subclass adds nothing after level 1. This is what a later pass needs to know whether a dip
  reaches the grant.

Return raw JSON, one object keyed exactly as your assignment lists the keys. No prose, no fences.
**Emit no other fields** — no scores, no split, no chassis name.

## The booster registry — these ids and no others

| id | what | scope |
|---|---|---|
| `brutish-durability` | Fighter 7 — +1d6 to every save | self |
| `aura-of-protection` | Paladin 6 — +Cha to every save | pair |
| `emboldening-bond` | Cleric Peace — +1d4 to every save, both bodies | pair |
| `friars-blessing` | Way of the Friar — +1d4 to every save, both bonded | pair |
| `lunar-champion` | Oath of the Moon 20 — +Cha to all saves in an aura | pair |
| `heroic-warrior` | Champion — a free reroll on a failed save, every turn | self |
| `magic-resistance` | Paragon 9 — advantage vs spells and magical effects | self |
| `spell-resistance` | Wizard Abjuration 14 — advantage vs spells | self |
| `magic-awareness` | Wildsurge — proficiency bonus to both bodies' saves vs spells | pair |
| `rage-of-ginnungagap` | advantage on all saves vs spells while raging | self |
| `dark-augmentation` | Blood Hunter — +Int to Str, Dex and Con saves | self |
| `towering-ego` | Mesmerist 2 — +Cha to Wis saves, +half Cha to Int | self |
| `frost-rune` | Rune Knight — +2 to Str and Con saves | self |
| `fanatical-focus` | Zealot — one reroll per Rage | self |
| `gift-of-will` | Trickster — +Cha and half level to the partner's Wis saves | pair |
| `flash-of-genius` | Artificer 7 — +Int to an ally's save, costs a reaction | pair |
| `war-caster` | advantage on concentration saves only | self |

## Read set

Only the class-file line ranges your assignment names. You are answering a narrow, factual
question — which proficiencies and which named effects — so you do not need the rubric, the
scoring model or the spell lists.
