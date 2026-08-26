# Stormglass v1 — Champion 3 / Great Old One 3 / Stormchaser 3 / Snowlight 11

**Fighter 3 (Champion) / Warlock 3 (Great Old One) / Druid 3 (Circle of
Stormchasers) / Ranger 11 (Snowlight Conclave)** — level 20, Lone Wolf duo. A ranged Cold
control chassis that fires Wisdom-based Hellrime Blast, adds both WIS and CHA to every beam,
turns every hit into a Blind save, and turns its unusually frequent critical hits into area Fear.

Every mechanic marked **[pak]** was read directly from the installed Listonomicon 10.2 archive.
Mechanics marked **[data]** are confirmed in the repository's compiled class snapshot. The generic
spellcasting-ability interaction and sequencing between beams remain **[in-game test]** items.

---

## The engine

1. **Elemental Blast supplies Hellrime without needing ordinary Eldritch Blast. [pak]**
   Warlock 2 selects Elemental Blast and Agonizing Blast as its two invocations:
   ```text
   ElementalBlast
     Boosts "UnlockSpell(Projectile_ElementalBlast);"

   Projectile_ElementalBlast
     ContainerSpells "Projectile_HellrimeBlast;Projectile_BrimstoneBlast;
                      Projectile_VitriolicBlast;"

   Projectile_HellrimeBlast
     using "Projectile_EldritchBlast"
     SpellSuccess "DealDamage(1d10,Cold,Magical); ..."
     DamageType "Cold"
   ```
   The elemental container is a level-0 spell with an Action cost. Hellrime inherits Eldritch
   Blast's character-level projectile scaling, reaching four beams at character 17. Although the
   elemental spell record above contains `1d10`, Listo's Eldritch Blast-alike rebalance governs
   the inherited variant in play: score Hellrime at **1d8 Cold per beam**, not 1d10.

2. **Ranger being the last newly introduced class makes the passive-granted spell use WIS.
   [pak + in-game test]** Elemental Blast uses bare `UnlockSpell(...)`; it supplies no casting-
   ability override. Generic/passive-granted spells use the casting ability of the most recently
   introduced class. Introduce Fighter, Warlock and Druid before Ranger, then never introduce a
   fifth class: Hellrime should use **WIS** for its attack roll and source spell DC. Continuing to
   level an already introduced class does not change that order.

3. **Agonizing Blast recognizes Hellrime but remains CHA-based. [pak]**
   ```text
   AgonizingBlast
     Boosts "IF(IsEldritchBlastAlike() and IsCharismaModifierPositive()):
             DamageBonus(CharismaModifier);"
   ```
   Mizora's `IsEldritchBlastAlike()` helper explicitly contains
   `Projectile_HellrimeBlast`. The attack can therefore use WIS while every beam adds the
   positive **CHA** modifier to damage.

4. **Storm Shift adds WIS to every Hellrime beam. [pak]** Stormchasers 2 spends a Bonus Action
   and one Wild Shape charge to apply `STORM_SHIFTER` indefinitely:
   ```text
   STORM_SHIFTER
     Passives "StormShifter;EyeOfTheStorm"
     Boosts   "TemporaryHP(ClassLevel(Druid)*3); ..."

   StormShifter
     Boosts "IF(MainDamageTypeIs(DamageType.Cold)):
             DamageBonus(max(0, WisdomModifier)); ..."
   ```
   There is no Druid-spell requirement and no once-per-spell or once-per-turn limiter. Each
   Hellrime projectile has Cold as its main damage type, so each receives **+WIS**. Storm Shift
   ends on dismissal, another Wild Shape, or incapacitation.

5. **Glaring Frost converts every hit into control. [pak]**
   ```text
   Glaring_Frost
     StatsFunctorContext "OnDamage"
     Conditions "(HasDamageDoneForType(Cold) or HasDamageDoneForType(Radiant))
                 and not Item();"
     StatsFunctors "IF(not SavingThrow(Ability.Constitution, SourceSpellDC())):
                   ApplyStatus(BLINDED,100,2)"
   ```
   Each damaging beam is a separate projectile and damage event, so every hit should force its
   own CON save. At Ranger 11, **Snow Blindness** then makes a creature Stormglass blinded take
   1d6 Radiant when it spends an Action, Bonus Action or Reaction, plus an end-of-turn tick.

6. **Champion and Great Old One convert beam count into area Fear.** Champion 3 crits on 19–20;
   Spell Sniper lowers that to **18–20**. Great Old One's Mortal Reminder makes the critical
   target and nearby enemies save or become Frightened. Blind supplies Advantage against the
   target, so a successful early Glaring Frost makes the later beams still more likely to crit.

7. **Action Surge supplies the burst volley.** Lone Wolf provides two Actions, hence two
   four-beam casts. Fighter 2 adds one short-rest Action Surge for a third cast:
   ```text
   normal round       2 casts =  8 beams
   Action Surge round 3 casts = 12 beams
   ```

The loop in one line:

```text
Hellrime hit → 1d8 + WIS + CHA Cold → Glaring Frost CON save → Blind
             → later beams gain Advantage → 18–20 crit → Mortal Reminder area Fear
             → blinded creature spends resources → Snow Blindness Radiant ticks
```

---

## Chassis

| class | levels | subclass | what it is here for |
|---|---:|---|---|
| Fighter | **3** | **Champion** | CON saves and heavy armour from the opener, Action Surge, 19–20 criticals, +3 initiative, Fighting Style, feat |
| Warlock | **3** | **Great Old One** | Elemental Blast, Agonizing Blast, Mortal Reminder, pact boon, two short-rest level-2 slots, feat |
| Druid | **3** | **Circle of Stormchasers** | Storm Shift's per-beam WIS rider, Wild Shape charges, WIS casting, level-2 spells, feat |
| Ranger | **11** | **Snowlight Conclave** | Glaring Frost, Snowborne, Extra Attack, Behind the Sun, Snow Blindness, Armour of Agathys, feat ×3 |

**Level-1 class: Fighter.** This supplies STR + CON saving-throw proficiency, heavy armour,
shields, martial weapons and a d10 opener. Lone Wolf can then grant WIS + CHA proficiency without
duplicating either save, producing four disjoint proficient saves.

### Why Ranger stops at 11

Snow Blindness is the last feature needed for the single-target engine. Ranger 15's Snowborn
Anthelion would make every beam an area Blind attempt, but four more Ranger levels do not fit
beside all three multipliers. This version exchanges Anthelion for Storm Shift, Mortal Reminder
and Action Surge: much stronger single-target damage and crit-driven area Fear, but less reliable
area Blind.

### Why each dip is exactly three

Listo grants feats by **class level** at 3 / 6 / 9 / 12 / 13 / 15 / 18. Each three-level block is
therefore feat-neutral:

- Warlock 2 already supplies both essential invocations; 3 adds a feat, pact boon and level-2
  pact slots.
- Druid 2 already supplies Storm Shift; 3 adds a feat and level-2 Druid spells.
- Fighter 2 already supplies Action Surge; 3 adds Champion and a feat.

Putting the last three levels into an existing class is weaker for this engine. Ranger 14 buys
two feats, Greater Invisibility and Vanish; Druid 6 buys one feat, third-level spells and Storm's
Reach; Warlock 6 buys one feat, a third invocation and Entropic Ward. Champion 3 instead buys a
feat, a permanent crit reduction, +3 initiative and an entire extra four-beam cast per short rest.

---

## Class introduction and progression

The **introduction order is mechanical**, not cosmetic:

| character | take | result |
|---:|---|---|
| 1–3 | Fighter 1–3 | CON saves, heavy armour, Action Surge, Champion, first feat |
| 4–6 | Warlock 1–3 | GOO, Elemental + Agonizing Blast, pact boon, feat |
| 7–9 | Druid 1–3 | Storm Shift, level-2 Druid spells, feat |
| 10–20 | Ranger 1–11 | Ranger becomes the generic casting ability; Glaring Frost at 12, Extra Attack at 14, Snow Blindness at 20 |

This conservative order delays Glaring Frost badly. For actual play, respec at the relevant
breakpoints rather than level in that exact sequence:

1. Play Ranger early so Glaring Frost arrives at character 3.
2. Add the desired dips while levelling normally.
3. Once the multiclass body matters, respec and introduce **Fighter → Warlock → Druid → Ranger**,
   then distribute later levels freely among those already introduced classes.

After the respec, Ranger remains the most recently introduced class even if the final five
levels are taken in Fighter, Warlock or Druid.

---

## Stats and saves

A defensive point-buy line after freely assigned racial bonuses:

| STR | DEX | CON | INT | WIS | CHA |
|---:|---:|---:|---:|---:|---:|
| 8 | **12** | **16** | 8 | **16** | **14** |

Put Lone Wolf's +4 on **WIS + CHA**:

| source | char | CON | WIS | CHA |
|---|---:|---:|---:|---:|
| creation | 1 | 16 | 16 | 14 |
| Lone Wolf | 1 | 16 | 20 | 18 |
| Elemental Adept | 3 | 16 | 21 | 18 |
| Dungeon Delver | 6 | 16 | **22** | 18 |
| Actor | 9 | 16 | 22 | 19 |
| War Caster | 12 | 16 | 22 | **20** |
| *Mirror of Loss* | *16+* | *16* | ***24*** | *21* |

Baseline level-20 numbers before gear:

```text
Hellrime attack       +12 = PB 6 + WIS 6        Mirror: +13
Hellrime/Glaring DC    20 = 8 + PB 6 + WIS 6    Mirror:  21
Agonizing rider        +5 = CHA 20              Mirror:  +5 (21 is an odd point)
Storm Shift rider      +6 = WIS 22              Mirror:  +7
one beam              1d8 + 11 Cold             Mirror: 1d8 + 12
```

This deliberately uses **Feats Overhaul half-feats** to cross WIS 20 instead of Enweaved.
Enweaved spends one selection on a bare +2 and adds wild-magic liabilities; two +1 feats reach the
same 22 while carrying Elemental Adept's resistance bypass and Dungeon Delver's expertise. The
plain ASI feat remains capped at 20.

**Every half-feat on this line is a Feats Overhaul or Listo-patched one, and that is not an
accident.** `data/listo-10.2-feats.md` flags an *unresolved* question over whether the removal of
the ability-score cap reaches **Essential Feats** half-feats — Feats Overhaul's own page
recommends a patch mod to uncap them "the same way this mod does", and that patch is not in the
10.2 list. Anything from Essential Feats doing a step **above 20** rests on the unresolved
reading. Elemental Adept, Dungeon Delver, Actor and War Caster are all clear of it.

**Do not push WIS past 22 with feats.** The Mirror of Loss adds +2 against a hard cap of **24**,
so 22 + 2 lands exactly on the ceiling and wastes nothing — while a third WIS half-feat would buy
a 23 that the Mirror then throws away. 22 is the right stopping point, not a compromise.

### Why the Mirror's +2 goes to Wisdom

**WIS is the only stat on this body that pays three ways.** It rolls the Hellrime attack, it sets
the Glaring Frost save DC — which is the entire control engine — and Storm Shift adds it to every
beam as damage. Charisma pays once, through Agonizing Blast. So `+1 WIS` is worth roughly three
times `+1 CHA` here, and the Mirror's +2 belongs on Wisdom in every act it exists.

The Mirror's **separate +1 Charisma** then lands on 20 → 21 and moves no modifier. That is fine:
it is free, and it is the answer to the "last point of Agonizing damage is expensive" line under
Weaknesses — the point costs nothing once the Mirror is in reach.

At CON 16, level 20 and before item bonuses, concentration saves are **+9** from CON 3 + PB 6.
War Caster adds Advantage. Lone Wolf halves incoming damage before the usual concentration DC is
derived, so most hits remain at DC 10; +9 passes those automatically. A 30-damage hit becomes 15
damage and therefore only DC 10, while even a post-mitigation 40-damage hit is DC 20 at Advantage.

CON 14 would lose roughly **26 displayed HP after Lone Wolf's +30% multiplier** compared with this
line, before accounting for the value of halved damage, and would lower every concentration save
by one. It is not worth the two point-buy points saved on a four-class concentration caster.

**Save proficiencies:** STR + CON from Fighter; WIS + CHA from Lone Wolf. Heavy armour makes
dumping DEX defensible, while Champion's +3 initiative largely repairs its initiative cost.

---

## Feats — five, and one spare

Cadence: Fighter 3, Warlock 3, Druid 3, Ranger 3/6/9 — six selections, landing at characters
**3, 6, 9, 12, 15, 18**.

1. **Elemental Adept: Cold (WIS)** — char 3. WIS 20 → 21, ignores Cold resistance and adds +1 Cold
   damage per beam. The resistance clause is the real prize.
2. **Dungeon Delver (WIS)** — char 6. WIS 21 → **22**, Expertise in Sleight of Hand and Perception,
   Advantage finding hidden objects and resisting traps, and resistance to trap damage.
3. **Actor (CHA)** — char 9. CHA 18 → 19, plus Expertise in Persuasion, Deception, Intimidation
   **and Performance**. This makes Stormglass the duo's face without spending another ability
   score.
4. **War Caster (2024; choose CHA)** — char 12. CHA 19 → **20**, and Advantage on concentration
   saves. The installed pak restricts its +1 selector to INT, WIS or CHA, so it cannot raise CON.
5. **Spell Sniper** — char 15. Stacks with Champion for an 18–20 spell-critical range, ignores
   low-ground penalties, and gives Advantage on the first attack-spell damage roll.
6. **Spare** — char 18. See below.

Do **not** spend a feat on Eldritch Adept here: Warlock already supplies both invocations.

### Performer is cut, and that is where the spare comes from

The previous line took **Actor and Performer**, then let War Caster's `+1` make a dead CHA 21 —
the feat's own entry admitted "the odd point does not change the modifier". Two observations
collapse that:

- **Actor already grants Performance Expertise.** Performer's only unique contribution was
  Expertise in *Acrobatics*, which gates nothing in this run.
- **War Caster is a half-feat.** Letting its `+1` do CHA 19 → 20 is the same point Performer was
  bought for, at no extra cost.

Same Wisdom and Charisma at every act boundary — WIS 22 / CHA 18 in Act I, WIS 22 / CHA 20 from
char 12 — so **no scored number moves**. One selection comes back.

### What to do with the spare

It lands at char 18, so it only ever affects Act III. Nothing available there moves a rung —
Tough's retroactive HP arrives too late to lift Act I Durability, which is the rung that actually
binds. The best use is therefore to **retire this chassis's own stated request**:

- **Resilient (DEX)** — Stormglass's four disjoint proficiencies are STR / CON / WIS / CHA, and
  Dexterity is the one category they never cover. Adding it takes the derived saves rung from
  **4 to 5**. The pair value does not move, because saves is a personal axis and reads the weaker
  half — but it stops the build depending on a partner's aura for its own worst save category.
- **Alert** or a second **Elemental Adept** are the alternatives, and neither changes a number.

### One more selection, if you are willing to bet on the Mirror

The Mirror's free `+1 CHA` could do the 19 → 20 step itself, freeing **War Caster** as well. The
cost is running Acts I and II at CHA 19 rather than 20 — about 6 raw a round in Act II, which
leaves single-target at `1.91× par` against a rung-5 line of 1.8 and moves nothing. The risk is
that it stakes a permanent point of Agonizing damage on a **DC 25** check landing. Take it only
if the Religion answer is already secured.

---

## Pact boon, fighting style and equipment posture

**Pact of the Chain** is the default boon. An Imp or Quasit is a third body in a two-character
party and does not compete with Stormglass's Actions. Tome is the utility alternative. Blade has
no role on a character whose Action is worth four Hellrime beams.

**Fighter Fighting Style: Defence** if wearing armour; **Archery does not affect spell attacks**.
Heavy armour plus shield is the default posture. Hellrime has somatic and verbal components but
BG3 does not impose tabletop free-hand component handling, so the shield does not block it.

**Heavy armour has no Strength requirement in BG3.** Unlike tabletop 5e, plate neither requires
STR 15 nor applies a movement penalty for failing that threshold. STR 8 only reduces carrying
capacity and jumping; Lone Wolf doubles carrying capacity, so armour weight is manageable. Keep
spare gear and consumable stock on the partner or in camp rather than raising a dead attack stat.

Equipment effects worth testing around the engine:

- **Mourning Frost:** Insidious Cold / Chilled support and +1 Arcane Enchantment in Listo.
- **Potent Robe:** whether its CHA cantrip rider applies to each elemental beam under the installed
  rebalance.
- **Necklace of Elemental Augmentation:** whether it adds the active WIS casting modifier per
  Hellrime beam.
- Critical-threshold rings stack with Champion and Spell Sniper, though 18–20 is already enough
  for Mortal Reminder reliability.

Attunement and armour requirements may prevent wearing every attractive caster item together;
the chassis does not assume any one item.

---

## Spells and resources

### Warlock

Two level-2 pact slots, refreshing on a short rest. Good low-CHA or no-save choices include
Armour of Agathys, Hex, Darkness and Misty Step where available. **Hex** adds 1d6 Necrotic per
beam, but costs concentration and a Bonus Action; it improves damage without creating another
Glaring Frost trigger.

### Druid

Prepare **Create or Destroy Water**. Wet doubles Cold damage and is the largest multiplier the
body can self-supply, though spending an Action to establish it is usually worse than having the
partner throw water or cast it. Healing Word, Longstrider and utility spells cover the duo floor.

Storm Shift costs one of the Druid's two Wild Shape charges and one Bonus Action, then lasts until
Long Rest. At Druid 3 it supplies **9 temporary HP**. Do not Wild Shape afterward.

### Ranger

Snowlight supplies Armour of Agathys at Ranger 3. It is non-concentration and adds another Cold
Glaring Frost trigger when a melee attacker hits. Ranger 11 reaches third-level Ranger spells;
take Revivify and the required rescue/utility package.

The concentration slot is tactical rather than structural. Hex is the damage choice; control or
support may be worth more in a two-person fight.

---

## Damage and critical math

At WIS 22 / CHA 20 with Elemental Adept, before accuracy and equipment:

```text
one beam             1d8 + 6 WIS + 5 CHA + 1 = 1d8 + 12
one four-beam cast   4d8 + 48                = 66 average
normal Lone Wolf     8d8 + 96                = 132 average
Action Surge nova   12d8 + 144               = 198 average
```

At CHA 22, add 1 per beam: 70 / 140 / 210 respectively. Against **Wet**, the Cold packet is
doubled after bonuses.

Critical probability before Advantage:

| crit range | one beam | ≥1 crit in 4 beams | ≥1 in 8 | ≥1 in 12 |
|---|---:|---:|---:|---:|
| 20 | 5% | 18.5% | 33.7% | 46.0% |
| Champion 19–20 | 10% | 34.4% | 57.0% | 71.8% |
| Champion + Spell Sniper 18–20 | **15%** | **47.8%** | **72.8%** | **85.8%** |

With Advantage and an 18–20 range, one beam crits 27.75% of the time; four beams contain at least
one critical **72.7%** of the time. The engine therefore wants the first successful Blind early in
the volley, after which Mortal Reminder becomes close to automatic.

---

## Combat routine

### Standing setup

1. Storm Shift after each Long Rest; it costs one Bonus Action and lasts indefinitely.
2. Keep the Chain familiar summoned.
3. Cast Armour of Agathys before fights where melee contact is likely.

### Ordinary round

1. First Hellrime cast focuses the priority target until Glaring Frost lands.
2. Second cast exploits Advantage against the blinded target or spreads beams to blind several
   enemies individually.
3. Mortal Reminder from the first critical controls the surrounding cluster on the WIS-save axis.
4. Preserve Bonus Actions for Hex movement, Healing Word, Misty Step or consumables.

### Nova round

1. Apply Wet through the partner when possible.
2. Hellrime twice from Lone Wolf Actions.
3. Action Surge and Hellrime a third time.
4. Twelve beams force repeated Glaring Frost saves and have an 85.8% pre-Advantage chance of at
   least one Mortal Reminder critical at 18–20.

---

## Provisional profile

Rubric: `skills/listo-build/references/axis-rubrics.md`. These are chassis scores, not a pair
total. The two damage axes are ratios against the rubric's **60 / 87 / 123** single-target par and
**48 / 65 / 82** area par, including its per-instance gear constant. Everything else is judged
act-relative. The profile remains provisional until the WIS casting, per-beam Glaring Frost and
same-cast Blind sequencing checks pass.

The assumed act-end bodies are:

```text
I    Ranger 3 / Warlock 3 / Druid 2
II   Fighter 3 / Warlock 3 / Druid 3 / Ranger 6  (respec; Ranger introduced last)
III  Fighter 3 / Warlock 3 / Druid 3 / Ranger 11
```

| axis | I | II | III |
|---|---:|---:|---:|
| Single-target | 3 | 3 | **4** |
| AoE | 3 | 3 | **4** |
| Durability | 3 | 3 | 3 |
| Actions | 2 | 3 | 3 |
| Control (single) | **4 ?** | **4 ?** | **4 ?** |
| Control (area) | 3 ? | **4 ?** | **4 ?** |
| Rescue | 2 | 2 | 1 |
| Skills | 3 | 3 | 3 |
| Saves | 3 | 3 | 3 |
| Endurance | **4** | **4** | **4** |

**Damage derivation.** This uses the resource-free two-Action Hellrime routine, without Hex, Wet,
Action Surge or named equipment. The rubric excludes Action Surge from damage because it is
scored under Actions. Act I has two beams per cast at WIS 22 / CHA 18; Act II has three at WIS 22
/ CHA 20; Act III has four. Each beam is a separate gear instance:

```text
I     4 × (1d8 + 6 WIS + 4 CHA + 1 Adept + k3) = 74   → 1.23 ST / 1.54 AoE
II    6 × (1d8 + 6 WIS + 5 CHA + 1 Adept + k5) = 129  → 1.48 ST / 1.98 AoE
III   8 × (1d8 + 6 WIS + 5 CHA + 1 Adept + k8) = 196  → 1.59 ST / 2.39 AoE
```

Splitting beams among enemies is a tactical targeting choice, so the same at-will pool qualifies
on AoE. Wet is deliberately omitted because Stormglass cannot establish it without consuming one
of the Actions being measured.

**Durability 3** is heavy armour and shield from Act II onward, CON 16, Storm Shift temporary HP
and Second Wind, but no proportional mitigation above the shared Lone Wolf floor. Act I lacks the
Fighter opener and uses medium armour and shield; its comparable HP pool keeps it on the same rung.

**Actions 2 / 3 / 3** is the Chain familiar in Act I, then familiar plus one short-rest Action
Surge after the respec. It does not receive damage-axis credit a second time. **Endurance 4** is
the Warlock-default at-will engine: Hellrime, Agonizing Blast, Glaring Frost and Mortal Reminder
need no slots, while pact slots and Wild Shape remain meaningful finite support pools.

**Control is the principal uncertainty.** Repeated no-concentration Blind attempts justify
single-control 4 if Glaring Frost fires independently per beam. Beam spreading plus crit-driven
Mortal Reminder supports area 3 in Act I and 4 once six to eight beams and the 18–20 critical
range are live. Failure of the per-beam or same-cast sequencing tests lowers the affected control
axis by one rung.

**Skills 3** is derived from the actual modifier shape, not eyeballed: Act I already has
Perception and Sleight of Hand Expertise from Dungeon Delver; Actor adds Persuasion Expertise in
Act II, but INT 8 leaves Investigation at −1 throughout. **Saves 3** is likewise derived. Act I's
Ranger opener plus Lone Wolf covers STR / DEX / WIS / CHA; the Act II respec changes that to STR /
CON / WIS / CHA. Both are four disjoint proficiencies covering two of the three key saves, and War
Caster's concentration-only Advantage is not a blanket save booster. Rescue falls because
low-tier Druid healing, Lesser Restoration and Ranger Revivify do not scale into Act III's rescue
benchmarks.

The profile's clearest partner request is therefore **Investigation, high-tier outward rescue and
Dexterity-save coverage**. Stormglass already supplies priority damage, crowd damage and both
forms of no-concentration control.

---

## Strengths

- Fully assembled control, damage and critical engine in one character.
- Resource-free floor of eight Cold beams every round.
- Blind attacks CON while Mortal Reminder attacks WIS.
- WIS governs attack accuracy, Glaring Frost DC and one complete damage modifier.
- Short-rest Action Surge and pact slots match Listo's expensive long-rest economy.
- Fighter opener plus Lone Wolf produces STR / CON / WIS / CHA save proficiency.
- Heavy armour, shield, Snowborne Cold resistance and Lone Wolf damage halving make a durable
  ranged caster.
- Four independent level-3 blocks produce six feats despite four-class multiclassing.

## Weaknesses

- **No Snowborn Anthelion.** Area Blind must come from spreading beams; Mortal Reminder is the
  primary area-control conversion.
- The body wants both WIS and CHA. WIS is primary and pays three ways; CHA pays once. The last
  point of Agonizing damage used to be expensive — the Mirror of Loss's free `+1 CHA` now covers
  it, so the cost is a DC 25 Religion check rather than a feat.
- Cold immunity still beats Elemental Adept; only Stormchasers 10 downgrades immunity, and this
  split cannot reach it.
- Wet requires setup and can create dangerous electrified/frozen surfaces for the partner.
- Mortal Reminder depends on attack rolls and criticals; Glaring Frost depends on damage landing
  and a CON save.
- Incapacitation removes Storm Shift and consumes another Wild Shape charge and Bonus Action to
  restore it.

---

## Required in-game checks

1. **Generic casting ability:** after introducing Fighter → Warlock → Druid → Ranger, verify
   Hellrime displays `PB + WIS` to hit rather than `PB + CHA`.
2. **Per-beam Glaring Frost:** confirm four separate Glaring Frost saves appear in the combat log
   when all four Hellrime beams damage one target.
3. **In-cast sequencing:** determine whether Blind from an early beam grants Advantage to later
   beams selected as part of the same cast.
4. **Storm Shift rider:** the pak has no limiter and conclusively qualifies Hellrime by main Cold
   type; confirm the combat log shows +WIS on every beam under the full load order.
5. **Mortal Reminder DC:** record whether the GOO feature retains a CHA-based Warlock DC or follows
   the active generic WIS casting ability.
6. **Item riders:** test Potent Robe, Mourning Frost and Necklace of Elemental Augmentation one at
   a time before incorporating any into score arithmetic.

Until checks 1 and 2 pass, treat Stormglass as a pak-supported hypothesis rather than a finished
in-game build. Check 4 is strongly resolved by the installed data; it remains listed only to catch
load-order overwrites.
