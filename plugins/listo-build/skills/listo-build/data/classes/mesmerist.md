# Listonomicon 10.2 — Mesmerist

The Mesmerist is a **brand-new class** added to Listo by a mod — a conversion of the
Pathfinder 1e class of the same name, not a D&D class and not a reskin of a BG3 class. It is a
**Charisma-based half-caster** drawing from the **Bard** spell list, built around a
bonus-action, no-concentration, single-target **saving-throw debuff** (Hypnotic Stare) and a
melee **Deception-check debuff** (Mesmerist's Feint). Its niche is *locking down one important
enemy* rather than clearing trash: it stacks penalties on a single target so the rest of the
party's control lands, while its own level-2 feature makes it one of the most
mind-control-resistant characters available. It wears light armor, fights with finesse
weapons, and is a full party face.

**Provenance.** Compiled 17 August 2026. ModID **`11854`** — *Mesmerist - Pathfinder 1e Class
Conversion*, confirmed in `listo-10.2-mods.tsv` line 419. Archive pulled per
`listo-10.2-manifest.json`: **`Mesmerist-11854-2-2-3-1779925635.zip`** — **version 2.2.3**,
which is the current release, so the mod page describes the version Listo ships. Mechanics
below come from the mod's description page, its four Articles pages
(`baldursgate3/articles/965`–`968`), its changelog tab, and its comment thread. Requires
**BG3 Script Extender** (an off-site requirement of the mod; Listo ships SE). Anything not
stated by those sources is marked `(unverified)` — **this class has no D&D or BG3 baseline, so
do not fill gaps from 5e or from Pathfinder tabletop.**

---

## At a glance

| | |
|---|---|
| **Primary ability** | **Charisma** (spontaneous caster; also the stat behind Feint via Deception) |
| **Secondary** | **Dexterity** (light armor, finesse weapons, AC) |
| **Saves granted at level 1** | **Dexterity + Charisma** |
| **Hit die** | d8 |
| **Armor** | Light only |
| **Weapons** | Simple weapons, Hand Crossbows, Finesse weapons (Rapiers, Scimitars, Shortswords) |
| **Skills** | Choose **3** from Arcana, Deception, History, Intimidation, Insight, Investigation, Perception, Performance, Persuasion, Sleight of Hand, Stealth |
| **Class tags** | **Bard, Rogue** (relevant for tag-gated dialogue and gear) |
| **Caster tier** | **Half-caster**, explicitly "see Paladin or Ranger". Spells from the **Bard list**. 2 cantrips at 1, +1 at 4, +1 at 10 (4 total). Leveled spells start at **level 2**. |
| **Max spell level** | **5th `(unverified — see below)`.** The mod page never states a cap. It says half-caster slot progression and that level 20 is supported; the standard half-caster table extended to 20 tops out at 5th-level slots at class level 17. Custom spells are only documented for spell levels 1–3, and a commenter describes the class as trading away "higher level casting". |
| **Spells known** | **A new spell every level** (unlike Paladin/Ranger). At each level where a new *spell level* unlocks, you also get **2 custom Pathfinder-converted spells** for free. |
| **Resource cadence** | Hypnotic Stare and Feint are **at-will, no resource**. Subclass resources: Trickster's **Hypnotic Bond** = `3 + Mesmerist level`, **short rest**. Daredevil's **Panache** = 2 at level 3, +1 per odd level, restored by **crit or kill with a one-handed piercing weapon**, otherwise **long rest**. |
| **Key breakpoints** | **2** (Towering Ego + casting), **3** (subclass), **5** (Stare to 2 stacks; 2nd-level spells; Daredevil Extra Attack), **6** (Stare pierces mind-immunity at 50%; Feint −2 attack), **7** (2nd subclass pick; Eyebiter Psychic Inception), **10** (Feint stacking −1 AC; Towering Ego upgrade; 4th cantrip), **11** (Stare to 3 stacks; Phasic Challenge; Tier-3 subclass pick) |
| **Dip value** | **Very high at 2 levels** — see [Dip value](#dip-value). |

---

## Feat cadence

**Corrected against the install.** Mesmerist is on the **standard cadence**: **3, 6, 9, 12, 13,
15, 18** — seven feats, the same as every other class. **It does not get the level 11 feat.**

The docs say twice that it does:

- `data/docs/4-SpellsFeatsClassesItems.md` — "all classes get a feat at 3, 6, 9, 12, 15, and 18;
  **Fighters, Mesmerists, and Rogues** get a feat at 3, 6, 9, **11**, 12, 15, and 18."
- `data/docs/1-Home.md` — "Fighters, Mesmerists, and Rogues get an additional feat at level 11."

**The installed config contradicts both.** `FeatsUni.json` grants the level 11 feat through
`fighterfeat: 11` and `roguefeat: 11` only. Mesmerist's grant lives in the
`advancedCustomClasses` block, which is gated behind `enableAdvancedSettings` — set to
**`false`**. Artificer is in the same block and equally unaffected. See
`data/listo-10.2-mcm.md`.

> `(unverified)` only in the sense that a level-up screen would settle it definitively. The
> config is unambiguous; the docs are the stale side here, as they are on the universal level
> 13 feat they never mention.

**Note the conflict, and that Listo wins.** The mod's own page says "Ability Score Improvement:
At levels 4, 8, and 12 (and 16 and 19), gain a feat" — a five-feat, level-4-cadence class in
isolation. Listo's `Universal Feat Every X Level(s) - MCM` (`13193`) overrides this. Plan
against **3/6/9/12/13/15/18**, not the mod page's numbers. Because the cadence keys off *class
level*, a 3-level Mesmerist dip is feat-neutral.

---

## Core mechanics

Two at-will actions define the class. Neither costs a spell slot, neither needs concentration,
and both are available from **level 1**.

### Hypnotic Stare — level 1, **bonus action**, 9m/30ft

Focus on one enemy and inflict **Mesmeric Gaze**, which is mechanically **identical to
Mental Fatigue** from the base game (a saving-throw penalty). It applies **1 "turn"** (stack)
at level 1, **2 at level 5**, **3 at level 11**.

The stare is **persistent and free**: it lasts until you or the target die, until you move it
to a new target, or until you dismiss it with a hotbar spell. You must be within 9m to *apply*
it, but **once applied you can move any distance away**. Only one target at a time.

This is the class's structural contribution: **a permanent, no-cost, no-concentration −1/−2/−3
to one enemy's saving throws**, which every control spell your partner casts then benefits
from. It is also the input to several subclass features.

- Mesmeric Gaze **does not stack with other Mental Fatigue sources** (there are two in the base
  game). If the partner runs Illithid powers that apply Mental Fatigue, they overlap rather
  than add.
- **Blinded** does not stop it, but reduces it to a flat **25%** chance to work.
- **Immunity list.** Mind-affecting resistance blocks it entirely at low level: **undead with
  Int ≤ 10, Mindflayers, mindless Constructs/Plants/Oozes, the Netherbrain, Intellect
  Devourers, and anything with Int ≤ 2.** At **level 6** these become a flat **50% per turn**
  chance instead of blanket immunity. The **Eyebiter** removes the restriction entirely at
  level 7 (Psychic Inception, 100%). *This is a real Act-3 concern — a large share of late
  content is undead and constructs.*

### Mesmerist's Feint — level 1, **bonus action**, melee

A weapon flourish that makes a **Deception check** against a DC; on success the target is
thrown **Off Balance** and takes a little psychic damage.

- **Level 6:** target also takes **−2 to attack rolls** until the start of your next turn.
- **Level 10:** additionally a **stacking −1 to AC until the end of combat**.

The DC formula (from the Main Class Addendum article) is
**10 + target's level + target's Wisdom save modifier**, modified by:

- **+2** mind-affecting-resistant creatures, **+4** mindless creatures, **+1** Boss-tagged
- **−1** if feinting with a **Light or Finesse** weapon
- **−1/−2/−3** if the target is also under your Hypnotic Stare (equal to its stack count)
- **Advantage** on the Deception check if *you* have advantage on Wisdom saves; **disadvantage**
  if the *target* does; SE compares sources if both
- DC is capped at **60** (since v2.1.0)

Restricted to melee weapons the base Mesmerist is proficient with. **Known UI defect:** because
the check runs in Script Extender, the tooltip **always displays 0% chance of success**
regardless of the real odds — read the combat log instead.

### Consummate Liar — level 2

Bonus to **Deception checks equal to half your Mesmerist level**. Directly feeds Feint's
success rate as well as dialogue.

### Towering Ego — level 2

**This is the defensive feature the skill cares about, and the existing belief is correct but
incomplete.**

- **Bonus to Wisdom saving throws equal to your Charisma modifier.**
- **Bonus to Intelligence saving throws equal to half your Charisma modifier.**
- **At level 10:** the Intelligence bonus becomes the **full** Charisma modifier, **and you
  gain advantage on Charisma saving throws.**

Three qualifications that matter for planning:

1. **Self only.** It is a personal passive, not an aura and not a party buff. Nothing about
   Towering Ego reaches the partner. (The party-facing Wisdom-save effect is the **Trickster's
   Gift of Will** trick — see below.)
2. **It scales with Charisma, not with class level.** A **2-level dip gets the full effect.**
3. **It switches off while you are under a harmful mind-affecting effect** — defined as any
   status in the groups Charmed, Confused, Dominated, Drunk, Fleeing, Frightened, Mad,
   Possessed, Rage, Sleeping. So it is purely **preventative**: it helps you resist the first
   application, and does nothing to help you shake off a Dominate that already landed, or to
   resist a second effect while the first persists. Do not plan on it as a recovery tool.

Even with those caveats, at Cha 20 this is a flat **+5 to Wisdom saves from class level 2**,
which is the top-priority save category for this run and is not otherwise purchasable that
cheaply.

### Spellcasting

Cantrips and leveled spells are drawn from the **Bard list**. 2 cantrips at level 1, a third at
4, a fourth at 10. Leveled casting starts at **level 2** on half-caster slots, but unlike
Paladin/Ranger you **pick a new spell every single level**. At each new *spell level* you are
additionally handed **2 custom Pathfinder conversions for free**. Since **v2.2.3** you are also
**automatically granted Shadow Blade as a 2nd-level spell**.

Custom spells documented on the Articles page:

| Spell lvl | Name | Effect |
|---|---|---|
| 1 | **Doom** | Conc. ≤10 rounds, Wis negates, Fear effect. **−1 to attack rolls, damage rolls, saving throws and skill checks**, multiplied by the slot level if upcast. |
| 1 | **Sensory Overload** | 3 rounds (+1/slot above 1st), Wis negates. Whenever the target fails *any* save it takes **1d8 psychic**, escalating to 2d8/3d8/4d8 as its HP drops below 75%/50%/25%. |
| 2 | **Animus Mine** | Lasts until triggered or long rest. **When you would fail any saving throw**, detonate: **1d4 psychic per Mesmerist level** to the source and **Stun 1 round**, which can interrupt the spell and spare you the save. Wis save halves and negates the stun. |
| 2 | **Psychic Leech** | 10 rounds. Target is **Sickened** (−2 attack, damage, saves, ability and skill checks); while you stand within 3m of it **your Dexterity and Charisma are +2**. Successful Wis save cuts Sickened to 2 rounds and denies you the stat bonus. |
| 3 | **Battlemind Link** | 10 rounds or end of encounter, **no save**, cast on an **ally**. Both of you, while within 3m of each other: **+2 initiative, cannot be Surprised or Threatened, no opportunity attacks provoked, +2 AC, advantage on attack rolls, +2 damage.** |
| 3 | **Synesthesia** | Conc. ≤3 rounds (+1/slot above 3rd), Wis negates. Target gets **−3m movement, −4 AC and Dex saves, flat 20% miss chance, cannot crit**. |
| — | **Phasic Challenge** (class level **11**, 1/long rest) | 10 rounds, Wis negates. **A duel:** you and the target can only damage each other; outsiders catching either of you in an AoE are made immune to it. You gain **+3d8 psychic on weapon attacks** and **−2 crit threshold** (stacks with other crit-threshold reduction). Dismissible early. |

No custom spells are documented above spell level 3, which is the main reason the 5th-level cap
is marked unverified.

---

## Archetypes / subclasses

Chosen at level 3 as **Mesmerist Aspect**. There are **three**. All three share the same
skeleton: a Tier-1 pick at 3, a **Boon** at 4 and 8 (and 16), a signature feature at 5, a
scaling feature at 6, a Tier-1-or-2 pick at 7, and Tier-any picks at 11 (and 15, 19). Levels in
parentheses on the mod page are the beyond-12 ones.

### Aspect of the Trickster — the support/buff archetype

- **Mechanics:**
  - **L3 Mesmerist Trick + Hypnotic Bond.** New resource: **`3 + Mesmerist level` Hypnotic
    Bonds, refreshed on a SHORT rest** — 6 at level 3, 23 at level 20. You **implant** a Trick
    on yourself or an ally at any time; it fires **as a free action** when its trigger
    condition is met. Learn **2 Tier-1 tricks** at level 3. Only **1 implanted at a time** at
    level 3.
  - **L4/L8 (L16) Trickster's Boon** — pick 1 of 4: **Fortifying Tricks** (+1 AC and 1 Damage
    Reduction while a trick is implanted, +1 per 5 class levels, max +5/+5); **Healing Bond**
    (1d8 temp HP per trick activation, +1d8 per 5 levels, max 5d8); **Mocking Machinations**
    (on activation, enemies within 9m of the subject take 1d6 psychic and −1 attack for 1
    round, scaling to 5d6/−5); **Spirited Trick** (on activation, allies within 9m get +1
    attack and +1.5m movement for 1 round, scaling to +5/+7.5m).
  - **L5 Manifold Trick** — 2 implanted at once; **L9** → 3 (L13 → 4, L17 → 5).
  - **L6 Expansive Trick** — target **2 allies** with the same trick while it still counts as
    one implant; **3 at L12** (4 at L18). Costs extra Bonds equal to the trick's Tier.
  - **L7 Vexing Trick** — learn 2 more from Tier 1 or 2. **L11 Masterful Trick** — 1 more from
    any Tier (again at 15, 19).
  - **Tier 1 (L3):** *Astounding Avoidance* (grant Evasion against the triggering Dex-save
    effect); *Mesmeric Mirror* (triggering attack **automatically misses**, plus 3 Mirror Image
    copies for 1 minute); *Reflect Fear* (immune to fear 1d4 rounds and the source must save or
    be Frightened); *Touch Treatment, Minor* (**no trigger, usable any time** — Lesser
    Restoration at 18m range).
  - **Tier 2 (L7):** *Compel Alacrity* (**Haste 2 rounds**, DC 15 Con save to ignore Lethargy);
    *Free in Body* (Freedom of Movement 1 minute); **_Gift of Will_** — *the subject adds the
    Mesmerist's **Charisma modifier + half the Mesmerist's level** to a Wisdom saving throw.
    **Cannot be implanted on yourself.***
  - **Tier 3 (L11):** *Cursed Sanction* (attacker takes **−4 to attacks, saves, ability and
    skill checks for 1 minute**, Wis negates); *Psychosomatic Retribution* (store 2 rounds of
    damage taken, then reflect **150%** of it as psychic to every enemy who dealt it);
    *Touch Treatment, Major* (Lesser + Greater Restoration + fear removal at 18m, no trigger).
- **Duo relevance:** **The strongest of the three for this run.** *Gift of Will* is the only
  feature in the class that hands the **partner** a Wisdom-save bonus — **+Cha mod + half level**
  is roughly **+15 at level 20** on the save category this skill ranks first, and the
  self-exclusion is irrelevant when the Mesmerist already has Towering Ego. Add *Mesmeric
  Mirror* (a guaranteed miss on the partner) and short-rest-refreshing Bonds in a run where
  long rests cost 120+ supplies, and this archetype directly answers both structural problems:
  losing a character, and rest economy.

### Aspect of the Eyebiter — the debuff/damage archetype

- **Mechanics:**
  - **L3 Bold Stare** — every Bold Stare effect rides along on the Hypnotic Stare and applies
    for as long as the Stare persists. Pick 1 from Tier 1 at level 3.
  - **L4/L8 (L16) Eyebiter's Boon** — pick 1 of 4: **Mirror** (every Bold Stare also grants
    *you* the inverse of the penalty it imposes; where no inverse exists, +1 Damage Reduction
    per Tier); **Resistance** (resistance to **physical** damage while Staring → **all** damage
    at L10 → **immunity to all damage at L20**); **Manifold Stare** (Painful Stare becomes 2d8
    usable **twice per turn** → 2d10 three times at L10 → 2d12 **unlimited** at L20, with the
    normal die increases at 12 and 18 still applying); **Vital Pinpoint** (ignore resistance to
    physical damage while Staring → all damage at L10 → **ignore immunity at L20**).
  - **L5 Penetrating Stare** — permanent **Speak with Animals** and **Detect Thoughts**; Stare
    at a corpse for **Speak with Dead**. **L9:** immune to Blindness, see through fog clouds and
    magical darkness. (L13: permanent See Invisibility. L17: **True Seeing** — auto-pass all
    Perception and Survival checks, see through disguises and polymorphs, auto-save against any
    Illusion spell.)
  - **L6 Painful Stare** — **once per turn**, when you damage your Stare target, **+2d6 psychic**.
    **+2d6 at L12** and again at L18 (so 2d6 → 4d6 → 6d6). *Progression was nerfed in v2.2.0.*
  - **L7 Biting Gaze** — 1 more Bold Stare from Tier 1 or 2. **L7 Psychic Inception** — your
    Hypnotic Stare now works on normally-resistant creatures at **100%**. **L11 Masterful
    Gaze** — 1 more from any Tier (again at 15, 19).
  - **Tier 1 (L3):** *Blinding* (Con save each turn or Blinded 1 round); *Disorientation* (the
    Stare's save penalty **also applies to attack and damage rolls**); *Hex* (1d6 force at the
    start of its turn, disadvantage on Dex and Cha saves); *Sundering* (the Stare's save penalty
    **also applies to AC**).
  - **Tier 2 (L7):** *Reflection* (target takes the same damage you do, as Warding Bond,
    converted to psychic); *Restriction* (obscured areas become difficult terrain for it);
    *Sluggishness* (Wis save at start of turn or **Slowed**).
  - **Tier 3 (L11):** *Oscillation* (target has a **50% miss chance against everyone except
    you**); *Sapped Magic* (the Stare's penalty also applies to **the target's spell save DCs**
    and Con saves); *Withering* (target must pass **DC 20 Wis** to cast a spell at you or it
    **fails as though counterspelled**; AoEs that fail leave you untouched).
- **Duo relevance:** The **boss-lockdown** option, and the only archetype that fixes the
  undead/construct immunity hole (**Psychic Inception at 7**). *Sapped Magic* + *Withering* is a
  standing anti-caster package that protects a two-person party with no bodies to spare, and
  *Oscillation* redirects a boss's attacks onto the Mesmerist — who has d8 HP and light armor,
  so pair it with the **Resistance** boon. Note **Mirror + Sundering/Disorientation** turns the
  enemy debuff into a personal AC or attack bonus, making the Eyebiter self-sufficient.

### Aspect of the Daredevil — the melee/skirmisher archetype

- **Mechanics:**
  - **L3 Daredevil's Panache** — new resource. **2 at level 3, +1 at every odd Mesmerist
    level.** Restored by landing a **critical hit or a kill with a one-handed piercing weapon**;
    otherwise **long rest** only. Panache is spent on Stances, or **dedicated** to upgrade
    Feints, or simply **held** — several features check only that you *have* at least N.
  - **L3 Dazzling Feint** — a **toggleable passive** (only 1 active at a time, freely switched)
    that adds an effect to each successful Mesmerist's Feint. Pick 1 from Tier 1 at level 3.
    **Dedicate 3 or 6 Panache for the day** to unlock the **Improved** or **Greater** variants —
    this permanently reduces your available Panache by that amount until you rest.
  - **L4/L8 (L16) Daredevil's Boon** — pick 1 of 4: **Critical Restoration** (1d6 HP on crit or
    kill with a light/one-handed piercing weapon, +1d6 per 5 levels; −2 crit threshold while in
    a Stance); **Grounded Stance** (entering a Stance grants immunity to Prone, Difficult
    Terrain and Surfaces and forced movement for 2 rounds; **Stance cost −1**, improving at 10
    and 20); **Pain Becomes Power** (**+2 attack below 80% HP, +4 below 50%, +6 below 10%**;
    damage bonus = ½ class level; unlocks a **free-action, no-cooldown Feint that costs 25% of
    your max HP**); **Superior Defense** (while **unarmored**, add **Charisma to AC on top of
    Dexterity**; +1 AC and another +1 per 5 Mesmerist levels; +3m movement).
  - **L5 Daredevil's Deeds** — **while you have ≥3 Panache, you gain Extra Attack.** **L9:**
    with ≥5 Panache, **Evasion, Uncanny Dodge, and +1 reaction**. (L13: with ≥4 Panache,
    Expertise in all Dex skills and advantage on Dex saves and checks. L17: with ≥6 Panache,
    **Feint no longer costs a bonus action**.)
  - **L6 Parry and Riposte** — spend **3 Panache** for a **Riposte stance** until your next
    turn: you **automatically Feint against anyone who misses you**. **L12** adds a **Parry
    stance** (3 Panache): **−5 AC**, but all attack-roll damage is reduced by
    **1d20 + Dex mod + Cha mod**, and reducing it to 0 triggers a free riposte with **+3d8
    psychic**. (L18: Daredevil stance combines both and imposes −1d10 − Dex − Cha on attack
    rolls against you.)
  - **L7 Daredevil's Feint** — 1 more Dazzling Feint from Tier 1 or 2. **L11 Masterful Feint** —
    1 more from any Tier; **Tier 3 Feints are once per short rest.**
  - **Tier 1 (L3):** *Blinding Strike* (Con save or Blinded 1 round); *Disengaging Feint* (free
    Disengage; Improved adds free Dash; Greater removes Jump's bonus-action cost); *Fateful
    Feint* (roll damage twice take higher until your next turn; Improved also rerolls natural 1s
    on attacks and saves; **Greater projects it as a 6m aura**); *Pushing Feint* (push 10ft, Dex
    negates).
  - **Tier 2 (L7):** *Critical Feint* (crit threshold −2 / −4 / −6 this turn); *Distracting
    Feint* (Wis save or 25% miss chance / 50% / 50% with disadvantage); *Inspiring Feint*
    (**allies within 9m get +2 attack for 1 round and 5 temp HP**; Improved/Greater extend to
    2/3 rounds with temp HP refreshing each turn).
  - **Tier 3 (L11, 1/short rest):** *Crippling Feint* (**Blinded, Slowed and Silenced 2
    rounds**, Con negates); *Humiliating Feint* (**Disarmed, Prone and Maimed 2 turns**, Dex
    negates); *Overwhelming Feint* (Bleeding, Reverberation and Reeling 2 turns on a failed Con
    save, **plus vulnerability to Psychic and Piercing regardless of the save**).
- **Duo relevance:** The only archetype that solves the **action-economy** problem directly —
  **Extra Attack at 5** (gated on holding 3 Panache) and **+1 reaction at 9**, on top of Lone
  Wolf's extra Action/Bonus Action/Reaction. **Superior Defense** (Cha to AC unarmored) makes
  the Charisma investment do double duty and removes the light-armor ceiling. The catch is
  **Panache economy in a long-rest-expensive run**: outside crits and kills with one-handed
  piercing weapons, Panache only comes back on a **long rest**, and dedicating 3–6 to Improved
  or Greater Feints can drop you below the Extra Attack threshold. Prefer a **rapier** (finesse,
  piercing, one-handed) and see `listo-10.2-equipment.md` for crit-threshold gear.

---

## Dip value

**High, and unusually cheap.** Only the **level-1 class** grants saving-throw proficiencies, so
the level-1 package matters most, but the standout is level **2**.

- **1 level:** Dex + Cha saves, light armor, finesse weapons and hand crossbows, **3** skills
  from a wide list, 2 Bard cantrips, and **Hypnotic Stare** — a permanent bonus-action −1 to
  one enemy's saving throws with no resource cost, which improves every control spell the duo
  casts at that target. Also picks up the **Bard and Rogue class tags**.
- **2 levels — the real dip.** Adds **Towering Ego**: **+Cha modifier to Wisdom saves and +½ Cha
  modifier to Intelligence saves**, permanently, on a feature that **scales with Charisma and
  not with class level**. A Charisma-primary character (Bard, Sorcerer, Warlock, Paladin) pays
  two levels for a flat **+5 to Wisdom saves at Cha 20** — the highest-value save in this run's
  ordering, against Hold Person, Dominate, Fear and Hypnotic Pattern. Also grants Consummate
  Liar (+½ level to Deception) and opens half-caster slots. **Remember the shutoff clause: the
  bonus vanishes while you are under a mind-affecting condition, so it prevents rather than
  cures.**
- **3 levels:** feat-neutral under Listo's cadence (you collect the dip class's level-3 feat),
  and buys a subclass. At 3 the subclass payloads are modest — 2 Tier-1 Tricks and 6 short-rest
  Hypnotic Bonds (Trickster), 1 Tier-1 Bold Stare (Eyebiter), or 2 Panache and 1 Tier-1
  Dazzling Feint (Daredevil). **Gift of Will is Tier 2 and needs Mesmerist 7**, so a 3-dip does
  *not* get the partner-facing Wisdom bonus.
- **Against dipping deep:** half-caster slot progression means Mesmerist levels contribute only
  half to a multiclass slot table, and the class's own damage scaling (Painful Stare, Extra
  Attack, stance tiers) is back-loaded to 5–12.

### The Charisma trap, and why the Mesmerist actually escapes it

Mesmerist grants **Dexterity *and* Charisma** saves at level 1 — the two abilities a
Charisma-finesse build most wants boosted. Lone Wolf's +4 to two abilities **also grants save
proficiency in both**, so pointing it at Dex or Cha wastes the proficiency half of the grant on
a Mesmerist twice over.

The consequence is a good one: put **Lone Wolf's +4 on Constitution and Wisdom**. That yields
**four** save proficiencies (Dex, Cha from the class; Con, Wis from Lone Wolf) covering the
entire top of this skill's save-value ordering, and stacks Con and Wis on top of Towering Ego's
Charisma-scaled Wisdom bonus. Charisma then has to be raised through point buy, half-feats
(see `listo-10.2-feats.md` — **the ability-score cap of 20 is removed** for feat increases),
the Hag's Hair, and the Mirror of Loss.

---

## Not present / known issues

The author states outright that they are "no expert at balance" and expects to rebalance; a
level-15 Honour-mode player in the comments reports the class "feels fairly OP" even with added
difficulty mods. Treat power estimates as provisional.

- **Feint always displays 0% success chance.** The entire Feint check runs in Script Extender,
  so the tooltip cannot show real odds. Read the combat log for your Deception bonus and the DC.
  *(Author-acknowledged, no fix planned.)*
- **Animus Mine damage is wrong.** "1d4 per Mesmerist level" is implemented as **roll 1d4 and
  multiply by level**, not `Xd4` — same average, far higher variance. Author is "looking for
  workarounds".
- **Phasic Challenge and Withering do not block residual AoE effects.** You are immune to the
  spell, but not to a fireball igniting a barrel or to the grease surface it leaves.
- **Eyebiter Blinding/Sluggishness may expire early.** One user reports the Blinded/Slowed
  statuses vanishing at the end of the target's turn rather than persisting; they were running a
  collection pack and never tested standalone, so **a mod conflict is not ruled out**.
  Unresolved on the page. `(unverified — worth testing in-game before building around Blinding.)`
- **Respec cleanliness.** Several statuses and passives (e.g. Daredevil's Extra Attack and
  unarmored AC persisting after respeccing to Eyebiter) failed to clear on respec. **Fixed in
  v2.2.2**, and Listo ships **2.2.3**, so this should not affect a fresh install — but v2.2.0's
  note "if you are an Eyebiter, please respec out of the class before updating" applies if the
  mod is ever updated mid-run.
- **No custom icons.** Every ability, both new action resources, the class and all three
  subclasses reuse existing base-game icons. Cosmetic, but expect visual ambiguity on the
  hotbar.
- **Author's stated not-yet-done list:** Mesmerist-specific items, additional Pathfinder spell
  conversions, and a distinct psychic casting system that would drop verbal/somatic components.
  None of these are in 2.2.3.
- **Max spell level is not stated anywhere on the mod page.** 5th is the reading implied by
  "half-caster progression (see Paladin or Ranger)" plus level-20 support, but custom spells
  stop at spell level 3 and a commenter refers to the class's "lack of higher level casting" as
  its balancing trade-off. `(unverified — confirm on a character sheet before planning a build
  around 4th- or 5th-level Bard spells.)`
- **Listo does not appear to patch this mod.** No Mesmerist-specific patch archive is present in
  `listo-10.2-manifest.json` — only the base `Mesmerist-11854-2-2-3-1779925635.zip`.

### Cross-references

- **Feats** — `listo-10.2-feats.md`. Seven-feat cadence at 3/6/9/12/13/15/18; the level-20
  ability-score cap is removed for feat increases.
- **Equipment** — `listo-10.2-equipment.md`. **Psychic Armory** (`14476`) is the
  Mesmerist-synergy gear breadtrail Listo added alongside the class (changelog: "a gear and
  equipment breadtrail for Mesmerist synergistic items"); it is an upgradeable set whose
  upgrade material is the **Sussur Bloom** from the **Arcane Tower basement**. The mod added a
  "framework for synergy with Psychic Armory" in v2.1.0. If updating an existing save past the
  tutorial, the changelog gives an SE command to grant the starting item:
  `TemplateAddTo("af22db43-e8be-4fc2-b906-1aaf87f199d7", GetHostCharacter(), 1)`.
- **Source material** — the mod links the Pathfinder original at Archives of Nethys. **Do not
  use it as a rules reference**; the BG3 conversion differs substantially.
