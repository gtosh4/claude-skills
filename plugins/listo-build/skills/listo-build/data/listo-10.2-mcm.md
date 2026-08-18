# Listonomicon 10.2 — resolved mod configuration

Every value here was **read out of an installed 10.2 copy**, not inferred from docs or mod
pages. This file replaces the "check MCM in game" and "ask the player" hedges elsewhere in the
skill for the settings it covers.

**Source.** `<Listo>/mods/[CUST] Listonomicon Mod Settings/SE_CONFIG/`, plus the MO2 profile at
`<Listo>/profiles/Listonomicon/modlist.txt`. Install verified as `Version = 10.2` in
`Listonomicon.compiler_settings`, matching the bundled snapshot.

Paths below are relative to `SE_CONFIG/`. `MCM/` is shorthand for
`BG3MCM/Profiles/Default/`.

> **These are the shipped defaults, not the player's live state.** MCM writes player changes to
> `%LOCALAPPDATA%\Larian Studios\Baldur's Gate 3\Script Extender\BG3MCM\Profiles\...`, which
> shadows what ships here. Treat this file as "what Listo intends" and confirm anything
> load-bearing on the player's actual sheet.

---

## Optional mods: what is actually enabled

From `modlist.txt` (`+` enabled, `-` disabled). **91 entries ship disabled.** The ones that
change build planning:

| Mod | State | Consequence |
|---|---|---|
| **Lone Wolf Feat - SE** | ships **DISABLED** — **enabled for this run** | Enabling it in MO2 is a manual step. This run uses **non-feat mode** (MCM feat requirement off), so the buffs apply from level 1 and cost no feat. |
| **OPTIONAL_Sit This One Out 2** | ships **DISABLED** — **enabled for this run** | Without it, recruited companions count against Lone Wolf's party cap of 2. |
| **OPTIONAL_Absolute Wrath** | **ENABLED** | Listo's own docs warn this double-dips with the CX affixes. It is on anyway — enemy gear is more loaded than the base config implies. |
| **OPTIONAL_Grit&Glory - Injuries Exhaustion** | **DISABLED** | No injury/exhaustion layer. Its MCM config exists but is inert. |
| **OPTIONAL_Illithid Powers Overhaul 2** | **DISABLED** | `Illithid Powers Consolidated` is enabled instead. |
| **OPTIONAL_Hit Dice RAW** | DISABLED | Hit dice stay vanilla. |
| **OPTIONAL_FeatMaker**, **EasyCheat**, **The Debug Book** | DISABLED | Not feat sources. |
| **OPTIONAL_Dynamic Difficulty Scaling**, **Advanced Enemy Randomizer**, **Many More Monsters**, **Hunted - Dynamic Ambushes**, **[ModIO] EEncounters & Minibosses**, **Dynamic Enemy Encounters** | DISABLED | Extra-encounter mods are off; the enabled encounter mods are `Encounters Overhaul`, `Encounters Enhanced` and `Valkrana's Undead Encounters`. |
| **Random Equipment Loot** | **not installed at all** | Gear planning is safe. The `REL_SE` MCM config present in `SE_CONFIG` is orphaned. |

---

## Expansion Level 13-20 — `MCM/Expansion/settings.json`

The file the class notes repeatedly call unreadable. Resolved:

```
Levels.MaxLevel                  20
Levels.DisableXPDataModification true
boons.BaseClassEpicBoons         false
boons.CustomClassEpicBoons       false
feats.BaseClassFeats             "None"
feats.CustomClassFeats           "None"
feats.BaseClassFeatSelection     true
misc.ExpansionBladesinger        false
misc.WizardBladesinger           false
misc.Sorcerer11thSubclass        true
```

- **No Epic Boons at 20**, base or modded class. Delete every "Epic Boons may apply" hedge.
- **Expansion grants no feats of its own** — its native 14/16/19 selectors are off, so
  `Universal Feat Every X Level(s)` is the *only* feat source. This confirms what
  `data/classes/fighter.md` guessed.
- **Bladesinger is off in both forms.** Do not propose it.
- `Sorcerer11thSubclass` is **on** — Sorcerer subclasses get their extra subclass feature.

### Per-class optional features (`optional_features`)

| On | Off |
|---|---|
| Barbarian, Bard, Cleric, Druid, Ranger | Fighter, Monk, Paladin, Rogue, Sorcerer, Warlock, **Wizard** |

- **Bard's Magical Inspiration (level 2) is ON.** `data/classes/bard.md` marked this unverified.
- **Wizard's Cantrip Formulas is OFF.** The mod default is on; Listo turns it off. Any wizard
  plan leaning on a cantrip swap is wrong.

### XP curve

`Levels.Level1..Level20+`: 2, 3, 1700, 2250, 4500, 5000, 8500, 9500, 10000, 30000, 20000,
24000, 30000, 30500, 32000, 32000, 33000, 35000, 35000, 50000. Note the **level 10 spike
(30000) and the level 11 dip (20000)** — 10 is the wall, and 11 is cheaper than 10.

---

## Feat cadence — `FeatsUni.json` (and `MCM/FeatsUni.json`, identical)

```
enableMod                true
featFrequency            3
alwaysGrantFeatAtLevels  { "13": true }
fighterfeat              11
roguefeat                11
multiclassFeatAtLevel1   false
enableAdvancedSettings   false
customGrantFeatAtLevels  []
```

**Resolved cadence: 3, 6, 9, 12, 13, 15, 18 for every class — seven feats, not six.** Fighter
and Rogue add **11**, for eight.

Two corrections this forces:

- The **level 13 feat is universal**, not something the older notes captured.
- **`enableAdvancedSettings` is `false`**, so the `advancedCustomClasses` block — which would
  have given Mesmerist and Artificer an extra feat at 11 — **does not apply**. Mesmerist is
  *not* on a special seven-feat cadence; it is on the same cadence as everyone else. Only
  Fighter and Rogue get the 11.
- `multiclassFeatAtLevel1` is false, so a dip grants no feat at its own level 1.

> **One unresolved conflict.** `MCM/FeatsUni/FeatsUni.json` is a third, near-empty copy holding
> `alwaysGrantFeatAtLevels { "20": true }` and nothing else. Two of the three files agree on
> 13; whether 20 also grants one is `(unverified)` — check the level-up screen.

---

## Combat Extender — `CombatExtender.json`

**`MCM/CombatExtender/settings.json` sets `Use_MCM_Settings: false`.** The MCM panel is inert;
the JSON file governs. Never tell a player to change CX in MCM.

Three configs ship — `CombatExtender.json` (normal, live), `EASY CombatExtender.json`,
`HARD CombatExtender.json`. Swapping is a file rename, per the docs.

### HP scaling — the actual numbers

Formula `Base × (1 + StaticBoost + HealthPerLevel × playerLevel)`, keyed off **player** level:

| | Static | Per level | At level 20 |
|---|---|---|---|
| **Bosses** | 0.10 | 0.08 | **×2.70 (+170%)** |
| **Enemies** | 0.06 | 0.06 | **×2.26 (+126%)** |
| **Allies** | 0.12 | 0.011 | ×1.34 (+34%) |

HARD raises bosses to 0.11/level and enemies to 0.08/level; EASY drops them to 0.06 and 0.05.

**The "+310% bosses / +250% enemies" figure in the older notes is wrong for 10.2** — it came
from a superseded config. The direction of the argument survives (enemies scale off player
level, so there is no out-levelling); the magnitude is roughly half what was claimed.

**Your summons and allies scale too**, which the radar guidance previously ignored: `Allies`
gets +34% HP by 20 and **+1 AC static plus +1 per 4 levels**. A summon does not decay as fast
as a flat-statted feature does.

### Other live scaling (normal config)

- **AC:** allies +1 static, +1 per 4 levels. Bosses +1 per 9, enemies +1 per 11.
- **Spell save DC:** bosses +1 per 7 levels, enemies +1 per 11.
- **Ability points:** allies +1 per 5, bosses +1 per 6, enemies +1 per 6.
- **Attack/save rolls:** +1 per 20 levels for everyone — effectively one point, late.
- **Movement:** bosses +2m, enemies +1m.
- **Extra actions:** **none** in the normal config for any category.
- **Damage boosts:** all zero in the normal config. Enemy lethality comes from kit, not from a
  flat damage multiplier.

### Level scaling — the only hard per-act level evidence

```
Level.Characters.Act.1/2/3.MaxLevel = 1        (no scaling of ordinary characters)
Level.Bosses.Act.1  MaxLevel 10  Offset 0
Level.Bosses.Act.2  MaxLevel 16  Offset 2
Level.Bosses.Act.3  MaxLevel 24  Offset 4
```

Bosses are set to *player level + offset*, capped. The Act I cap of 10 and the Act II cap of 16
(binding from player level 14) are the closest thing in the install to a stated expectation of
where the player is per act, and they support the skill's I 1–10 / II 11–15 / III 16–20 bands.
The Act III cap of 24 never binds at cap 20, so Act III bosses are **always player level +4**.

---

## Attunement — `Attunement/config.json`

`rules.uncapAttunementLimit: false`. Caps are **identical across all five difficulty entries**
(EASY, MEDIUM, HARD, HONOUR, Base), so difficulty does not change them:

| | Total attuned | Legendary | VeryRare | Rare | Uncommon |
|---|---|---|---|---|---|
| **Cap** | **5** | 3 | 5 | 6 | 13 |

Per-rarity slot sub-caps: Legendary 2 Armor / 2 Weapons / 2 Accessories; VeryRare 3/3/3;
Rare 4/4/4; Uncommon 6/5/5. Every rarity also has `Attunement Slots: 1`.

`items.attunementRarityThreshold: "Legendary"` — items **at Legendary or above auto-require
attunement**, plus 413 explicit `requiresAttunementOverrides` and 946 `rarityOverrides`.

A `relaxed config.json` also ships (total 6, Legendary 4, VeryRare 6, Rare 7); it is not the
live file.

**Plan gear against five attuned items, at most three of them Legendary.** The old "ask the
player" hedge is only needed if they swapped in the relaxed config.

---

## Long rest cost — `MCM/DynamicCampSupplyCost/settings.json`

```
category_active_party_multiplier   1.00
category_idle_follower_multiplier  0.30
category_hireling_multiplier       0.25
category_pet_multiplier            0.25
category_children                  0.45
category_supernatural_multiplier   0.00
category_unknown_multiplier        0.40
act1/act2/act3_multiplier          1.075 / 1.175 / 1.15
global_multiplier 1.0, round_to_nearest_ten true
```

**This materially corrects the skill's rest-economy claim.** Camp population does drive cost,
but an idle companion is **0.3× an active party member**, a hireling 0.25×, and Aylin, Mizora,
Tara and the Oathbreaker Knight are explicitly overridden to **0**. A two-person active party
that recruits companions does *not* pay a full party's price — it pays roughly a third per
idle body. Short-rest resources are still worth more, but the penalty for recruiting is a
third of what the older note asserted.

---

## Party size — `MCM/ConfigurablePartyLimit/settings.json`

`party_limit: 5`, `inspiration_cap_mode: "Party limit"`. Listo's default is **five**, not four —
consistent with the docs calling 5 "probably the right number for balance". Lone Wolf's cap of
2 is a separate mechanic layered on top.

---

## Smaller settings that touch build math

| Mod | Setting | Effect |
|---|---|---|
| `Initiative Variants` | `InitiativeDie: 10` | Confirms **d10 + Dex**. |
| `Sensible_Ambushing` | `resist_surprise_ability: Wisdom`, `dc: 15`, applies to All | A flat **Wisdom DC 15** to avoid surprise, for both sides. Another reason Wisdom outranks the other saves. |
| `OneDnD_WarMagic` | `improvedExtraAttackFix: true` | Extra Attack interaction fix is on. |
| `5eSpells` | all `remove_spells` tiers `false` | **No 5e or TCoE spell tier is stripped.** `BoomingBladeChange: true`; the RAW variants of Raise Dead, Ritual Spells and Spare the Dying are **off**. |
| `Attunement` | `cast_animation: true`, `cast_animation_combat: false` | Attuning plays an animation out of combat only. |

---

## How to re-read this

```sh
LISTO=/mnt/mercury/Games/Listonomicon
CFG="$LISTO/mods/[CUST] Listonomicon Mod Settings/SE_CONFIG"
ls "$CFG/BG3MCM/Profiles/Default"          # every mod with an MCM profile
grep '^-' "$LISTO/profiles/Listonomicon/modlist.txt" | grep -v _separator   # what's off
```
