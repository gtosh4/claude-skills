# Coldsnap v1 — Winter 13 / Snowlight 3 / Friar 3 / Peace 1

**Druid 13 (Circle of Winter) / Ranger 3 (Snowlight Conclave) / Monk 3 (Way of the Friar) /
Cleric 1 (Peace)**, **Astral Elf** — level 20, Lone Wolf duo. An at-will blind engine: eight **Elemental Blast**
beams a round, natively Cold, each one an independent Constitution save against being Blinded.

Every mechanic marked **[pak]** was read out of the installed archive with
`skills/listo-build/scripts/lspk.py`, not from mod pages or the Listo docs. Four of them contradict
the docs; those are called out where they appear.

---

## The engine

1. **Glaring Frost** (Ranger 3) is a predicate, not a threshold. **[pak]**
   ```
   Glaring_Frost  StatsFunctorContext "OnDamage"
                  Conditions "(HasDamageDoneForType(DamageType.Cold) or HasDamageDoneForType(DamageType.Radiant)) and not Item();"
                  StatsFunctors "IF(not SavingThrow(Ability.Constitution, SourceSpellDC())):ApplyStatus(BLINDED, 100, 2)"
   ```
   No cooldown, no once-per-turn clamp. `HasDamageDoneForType` asks *whether*, never *how much* — so
   a six-point Cold component blinds exactly as well as a sixty-point one. **The whole build is
   built on that sentence.**

2. **Winter Spirit** (Druid 2) attaches that component to everything. **[pak]**
   ```
   WINTER_SPIRIT  Boosts "TemporaryHP(ClassLevel(Druid)*5);
                          CharacterWeaponDamage(1d6,Cold);
                          IF((IsSpell() or IsCantrip()) and HasDamageEffectFlag(DamageFlags.Hit)):
                              DamageBonus(max(0, WisdomModifier),Cold,Magical);
                          IF(ClassLevelHigherOrEqualThan(6,'Druid')):UnlockSpell(Projectile_BlizzardCloud);
                          IF(ClassLevelHigherOrEqualThan(6,'Druid')):StatusImmunity(PRONE_ICE);"
                 RemoveConditions "not HasTemporaryHP() or HasStatus('SG_Polymorph_BeastShape')"
   ```
   **The damage rider carries no class predicate**, though the author uses class gates twice in the
   same field. The shipped tooltip says "a cantrip or a spell"; the Nexus page says "Druid". The
   code and the tooltip agree, so any spell or cantrip qualifies — including one granted by a feat.
   The bonus is **explicitly typed Cold**, which is what makes it a Glaring Frost trigger rather
   than just damage. `data/classes/druid.md` has been corrected.

3. **Elemental Blast** is the vehicle, via **Eldritch Adept** at character 3. **[pak]**
   ```
   ElementalBlast             Boosts "UnlockSpell(Projectile_ElementalBlast);"
   Projectile_HellrimeBlast   using "Projectile_EldritchBlast"
                              SpellContainerID "Projectile_ElementalBlast"
                              SpellProperties "GROUND:SurfaceChange(Freeze);GROUND:SurfaceChange(Douse);
                                               GROUND:CreateSurface(2,2,WaterFrozen);"
                              SpellSuccess "DealDamage(1d8,Cold,Magical);…"
   ```
   It inherits Eldritch Blast wholesale — `AmountOfTargets "LevelMapValue(EldritchBlast)"`, an 18 m
   `TargetRadius`, `Attack(AttackType.RangedSpellAttack)`, `ActionPoint:1` — and overrides the
   damage to **`1d8` Cold**, already patched down from `1d10` by `[cust] MizoraReward_ListoPatch`
   (the mod is literally named `Mizora_Reward_d8_Patch`). Beams scale on **character** level, 4 from
   17. Each beam is its own attack roll, its own damage roll, and therefore **its own Glaring Frost
   save**, and each may pick its own target. With both Lone Wolf Actions that is **eight independent
   blind saves a round, at 18 m, for no resource of any kind.**

   **The engine is live at character 3, not 5.** Hellrime is natively Cold, so it fires Glaring
   Frost on its own — it does not wait for Winter Spirit to supply a Cold component. That deletes
   the two-level gap the previous ladder carried *and* the dependency chain behind it.

   **It also deletes the sheet's largest open risk.** The old vehicle was Spell Sniper's Eldritch
   Blast, whose attack ability rested on an inference from a *missing* class UUID in the feat's
   selector. Elemental Blast arrives through `UnlockSpell` in a passive's `Boosts` field instead,
   so nothing about the build hangs on that reading any more.

   **`Projectile_ElementalBlast` is a container, not a single spell.** `Projectile_HellrimeBlast`
   (Cold), `Projectile_BrimstoneBlast` (Fire) and `Projectile_VitriolicBlast` (Acid) all carry
   `SpellContainerID "Projectile_ElementalBlast"`, and the invocation unlocks the container — so one
   feat buys **three damage types, switchable**. That is what answers the objection the previous
   version of this section raised against a Cold-typed beam:

   | | Cold **resistance** | Cold **immunity** |
   |---|---|---|
   | Hellrime alone | halves everything, since the whole beam is Cold | damage and blind both lost |
   | + `Elemental Adept: Cold` (char 10) | **pierced** — `IgnoreResistance(Cold,Resistant)` | still lost |
   | + switch to Brimstone or Vitriolic | — | `1d8` lands at full weight; only Winter Spirit's rider is immune, so you lose the blind and keep the damage |
   | + Word of Radiance (char 7) | — | the Radiant branch fires the blind anyway |

   **Every beam also lays `CreateSurface(2,2,WaterFrozen)`.** Eight beams a round carpets the field
   in ice. That is free difficult terrain against enemies and a real hazard for the partner, who has
   no `PRONE_ICE` immunity — see the pair sheet.

4. **Armour of Agathys blinds with no saving throw.** Undocumented anywhere. **[pak]**
   ```
   XR_ArmorSetup  OnStatusApplied  Conditions "StatusId('ARMOR_OF_AGATHYS') or …_2 … _6;"
                  StatsFunctors "ApplyStatus(XR_ARMOR_AG_TECH, 100, -1)"
   XR_ARMOR_AG_TECH   Passives "XR_ArmorTest;"
   XR_ArmorTest   OnAttacked  Conditions "IsMeleeAttack() and HasDamageEffectFlag(DamageFlags.Hit) and not SpellTypeIs(SpellType.Throw);"
                  StatsFunctors "ApplyStatus(SWAP, BLINDED, 100, 2)"
   ```
   Granted at **Ranger 3**, alongside Glaring Frost and the always-prepared `Shout_ArmorOfAgathys`.
   While Agathys is up, every melee attacker that hits you is Blinded — **no save, no roll**.

5. **Two retaliation lines**, both of which are Glaring Frost triggers. **[pak]**
   ```
   FriarRetribution  OnAttacked  "IsAttack() and Self(context.Target) and IsHit();"
                     "DealDamage(SWAP, 2*Cause.WisdomModifier, Radiant, Magical)"
   ColdSoul          OnAttacked  "IsMeleeAttack() and HasDamageEffectFlag(DamageFlags.Hit) and not SpellTypeIs(SpellType.Throw);"
                     Boosts "Resistance(Cold, Immune);"
                     "DealDamage(SWAP, (ClassLevel(Druid))/2, Cold, Magical)"
   ```
   One incoming melee hit is a **no-save Blind, a Radiant instance and a Cold instance** — two
   damage types, so resistance on either side does not close the loop. `Interrupt_FriarRetribution`
   covers the Kin the same way, and Lone Wolf grants two reactions.

6. **SlipperyMagic** (Druid 10) stacks a second status on the same damage. **[pak]**
   ```
   SlipperyMagic  OnDamage  Conditions "not Item() and not Self() and not IsMiss() and IsDamageTypeCold()
                             and not IsLastConditionRollSuccess(ConditionRollType.ConditionSavingThrow) and IsSavingThrow();"
                  StatsFunctors "ApplyStatus(PRONE,100,2)"
   ```
   Any Cold damage from a saving throw they failed knocks them Prone — so Ice Storm and Cone of Cold
   land Blind **and** Prone off one cast. It requires an actual save, so beams never trigger it.

**Every DC is `8 + PB + WIS` = 20**, and the blast attack is `PB + WIS` = **+12**. Ranger, Druid,
Cleric and the Ki Save DC all key off Wisdom, so one stat drives the Glaring Frost save, the beam's
attack roll, the reflect magnitude, Unarmoured Defence and Friar's Grace range.

---

## Chassis

| class | levels | subclass | what it is here for |
|---|---|---|---|
| Druid | 13 | Circle of Winter | **Winter Spirit (2)**, Snilloc's (3), Blizzard Cloud (6), Ice Storm (7), Cone of Cold (9), **SlipperyMagic (10)**, **ColdSoul (12)**, top slot tier (13) |
| Ranger | 3 | Snowlight Conclave | **Glaring Frost**, Snowborne, **Armour of Agathys + the no-save blind**, Close Quarters Shooter (2) |
| Monk | 3 | Way of the Friar | Friar's Bond + **Retribution**, Guardian of Light (shield + Unarmoured Defence + concentration advantage), Friar's Grace, Flurry of Blows |
| Cleric | 1 | Peace | **Word of Radiance**, Sacred Flame, always-prepared **Sanctuary** and Heroism, **Emboldening Bond** |

**Druid stops at 13, not 14.** `Expansion.pak`'s Druid 14 row is literally empty — no passive, no
boost, no selector — and Circle of Winter's own table ends at 12. The 20th level is free, and
Cleric 1 is also a full caster level, so the split keeps caster level **15** either way. **[pak]**

**Level-1 class: Ranger** — STR + DEX saves, martial weapons, medium armour, shields. Druid at 1
would give INT + WIS, colliding with Lone Wolf's Wisdom and leaving no Dexterity save.

### Why Peace and not Light

Light's only level-1 feature is **Warding Flare**, which imposes disadvantage on an attack against
you — and this chassis converts *being hit* into a no-save blind, 12 Radiant and 6 Cold. Its own
domain feature fights the engine. Its level-1 domain spells are Burning Hands (no proc) and Faerie
Fire (concentration, and Bond owns the slot). Radiance of the Dawn is at Cleric **2**, out of reach.

Peace pays three ways at Cleric 1:

- **Sanctuary**, always prepared, non-concentration — §7's *Prevention* form, aimed at the partner.
- **Emboldening Bond**, and it scales on **character** level, not Cleric level: **[pak]**
  ```
  EmboldeningBondUnlockScaling  Boosts "…IF(CharacterLevelGreaterThan(16)):UnlockSpell(Target_EmboldeningBond_Expansive,…,,Wisdom)"
  EmboldeningBondScaling        Boosts "IF(CharacterLevelGreaterThan(4,context.Source)):ActionResource(EmboldeningBondUse,1,0); …(8)…(12)…(16)…"
  ```
  A one-level dip at character 20 gets **five charges and the Expansive version**. Both bonded
  characters regain one `BondedEmpowerment` at the start of each turn (`EMBOLDENING_BOND_TICK`,
  `TickType StartTurn`) and spend it on **+1d4 to an attack roll, ability check or saving throw**.
  Note this is **once per turn each**, not the permanent blanket d4 `cleric.md:593` describes.
- A **free skill proficiency** from its level-1 `SelectSkills` — **Insight, Performance or
  Persuasion**, which Light and Twilight do not have at all **[data]**. Take **Persuasion**: it is
  the only route this body has to a proficient face check, and `Cat's Cleric Changes` removes the
  skills a Cleric *multiclass* used to hand out, so the domain pick is the only skill Cleric 1
  grants here.

Grave and Twilight are the runners-up; Twilight Sanctuary would sustain Winter Spirit's temp HP,
but it is a Cleric **2** feature.

---

## Race — Astral Elf

`Mori's Astral Elves` (`7718`), enabled. Read out of
`mods/Mori's Astral Elves/PAK_FILES/MoriAstralElf.pak`. **[pak]**

```
AstralElf_1   PassivesAdded "AstralElf_KeenSenses;AstralElf_StarlightStepChargeGain"
              Boosts        "ActionResource(StarlightStepCharges,1,0)"
              Selectors     "AddSpells(6a6ae2d7-…);SelectSpells(31334043-…,1,0,AstralFire,,,AlwaysPrepared)"
AstralElf_5 / _9 / _13 / _17    PassivesAdded "AstralElf_StarlightStepChargeGain"

Shout_AstralKnowledgeAstralElf_Intelligence
              SpellProperties "ApplyStatus(ASTRAL_KNOWLEDGE_INTELLIGENCE,100,-1)"
```

- **Astral Knowledge → Intelligence.** Duration `-1`, so it does not tick down. Proficiency in
  Arcana, History, Investigation, Nature and Religion. **Most of that is already held** — Ranger 1
  brings Investigation and the Sage background brings Arcana and History — so what it actually
  nets this body is **Religion**, which is the Mirror of Loss, plus Nature. It does **not** move
  the Skills rung: §8 scores Perception, Investigation and Persuasion, and this chassis was
  already proficient in the first two.
- **Keen Senses** — Perception proficiency, **redundant here**: Ranger 1 already grants it, and
  Dungeon Delver's Expertise was never doubling nothing. Recorded for completeness, worth zero.
- **Astral Fire → Light.** The pair's Callous Glow Ring sits on this body and wants an illuminated
  target; having Light here means Coldsnap can light its own target instead of spending the
  partner's Action on it. Sacred Flame is already free from Cleric 1 and Dancing Lights is worse.
- **Starlight Step** — bonus-action 9 m teleport, one charge at each of levels 1, 5, 9, 13, 17 =
  **5 per long rest**. Repositioning that does not cost the Action the beam routine needs.
  (`data/listo-10.2-races.md` says the charges equal Proficiency Bonus. The pak says otherwise.)
- Base elf: **Fey Ancestry**, Darkvision, Elf Weapon Training — the last redundant behind Ranger 1.

**No ability scores.** Listo removed racial ASI, so the `+2 WIS / +1 CON` in the stat table below
is assigned freely at creation and would read the same on any race. Race is bought here purely
for proficiencies.

**Runner-up: Fey Eladrin, and the case is closer than it first looked.**
`Target_FeyStep_Winter` is a bonus action, no slot and no concentration,
`not SavingThrow(Ability.Wisdom, SourceSpellDC())` → `ApplyStatus(FEARED,100,2)` at this build's
DC 20 **[pak]** — the direct answer to *Control (single) stops at 4 because a blinded creature
still acts*, since Frightened stops movement. Against it: only **4** charges (levels 1/5/9), and
it cannot roll the Mirror.

The first draft of this section credited Astral Elf with fixing Coldsnap's Investigation and
Perception. **It does not** — Ranger 1 already held both. What Astral Elf is actually bought for
is **Religion for the Mirror**, five bonus-action teleports, a free Light and Fey Ancestry, none
of which the scoring model prices. Fey Eladrin's Frighten is the only option on the table that
would move a scored axis. The pick stands as Astral Elf, but it stands on utility, not on rungs.

---

## Stats

| source | char | DEX | CON | WIS | AC |
|---|---:|---:|---:|---:|---:|
| point buy 8 / 15 / 15 / 10 / 14 / 8, then racial **+2 WIS / +1 CON** | 1 | 15 | 16 | 16 | — |
| Lone Wolf **+4** (WIS + CON) | 1 | 15 | **20** | **20** | 19 |
| Dungeon Delver | 6 | 15 | 20 | 21 | 19 |
| **Elemental Adept: Cold** | 10 | 15 | 20 | **22** | **20** |
| Durable | 16 | 15 | 21 | 22 | 20 |
| Tough | 19 | 15 | **22** | 22 | 20 |
| *Mirror of Loss* | *III* | *15* | *22* | ***24*** | ***21*** |

AC is Unarmoured Defence plus a shield — `10 + DEX + WIS + 2` — so Wisdom buys armour class here
as well as everything else. Lone Wolf grants **+4 to two abilities and save proficiency in both**,
plus +30% max HP, halved damage from all sources, and a second Action / Bonus Action / Reaction.

**Wisdom over Dexterity, and it is not close on this chassis.** Dexterity buys AC and initiative;
Wisdom buys AC, initiative parity via Alert, the beam's attack roll, the beam's damage, both
save DCs, Retribution's magnitude and Friar's Grace range. Nothing competes.

**Both Constitution half-feats are needed, and neither is wasted.** `20 → 21` moves no modifier
and `21 → 22` moves one, so Durable and Tough are a package that pays at the second of the two —
**+6 from character 19**. Tough is worth taking for the `+2` per character level and the `+2` to
Constitution saves regardless; the ability point is the bonus, not the reason.

**Wisdom 22 needs no picker and no Hag's Hair.** Dungeon Delver and Elemental Adept are both
Feats Overhaul, which delivers ability increases through *passive selectors* rather than the
vanilla ability picker, so both clear the cap of 20 unconditionally. **[pak]** That leaves
Hag's Hair free for the partner — see *The Mirror of Loss*.

**Dexterity stops at 15.** `Skilled Expert` bought the sixteenth point on the previous sheet and
is no longer taken; 14 and 15 are the same modifier, so the cost is one point of AC and the
Expertise on Investigation, which is now uncovered on both bodies.

---

## Fighting style and weapon

**Close Quarters Shooter** at Ranger 2 (UA Fighting Styles): **[pak]**
```
UA_FightingStyle_CloseQuartersShooter
  Boosts "IgnorePointBlankDisadvantage(Ammunition);IgnorePointBlankDisadvantage(Spell);
          RollBonus(RangedOffHandWeaponAttack,1);RollBonus(RangedWeaponAttack,1);
          RollBonus(RangedSpellAttack, 1)"
PassiveLists  AddTo_Ranger  "UA_FightingStyle_CloseQuartersShooter,UA_FightingStyle_DruidicWarrior,
                             UA_FightingStyle_Interception,UA_FightingStyle_Mariner,
                             UA_FightingStyle_ThrownWeaponFighting,UA_FightingStyle_TunnelFighter"
```
**`RollBonus(RangedSpellAttack, 1)` lands on every beam.** Eight a round at level 20 is eight
attack rolls, so this is the largest per-round accuracy source the fighting style slot can buy —
and it is the only one of the ten options that touches a spell attack at all. `AddTo_Ranger`
also settles the `(unverified)` in `data/listo-10.2-feats.md` about whether the UA styles reach
Rangers: they do.

`IgnorePointBlankDisadvantage(Spell)` is the other half, and it matters more than it reads. This
body has no Extra Attack, fights at 18 m and carries the pair's Blind engine; something closing
to melee used to cost the whole routine its accuracy. It now costs nothing.

**The three AC styles are all dead here, and it is worth saying why.** AC is Unarmoured Defence
plus a shield — `10 + Dex + Wis + 2` — so:

| style | why it does nothing |
|---|---|
| **Defence** (vanilla) | `+1 AC` **while wearing armour**. This body wears none, by design |
| **Mariner** | `BoostConditions "not HasHeavyArmor(…) and not HasShieldEquipped(…)"` **[pak]** — the shield is worth 2 AC and carries Guardian of Light, so trading it for 1 is net **−1** |
| **Tunnel Fighter** | genuinely gives `AC(1)` and a third Reaction — but through a **bonus-action stance re-cast every turn** **[pak]**, against a routine that already spends its bonus actions on Friar's Bond and Flurry |

**Druidic Warrior was the previous pick and its case has gone.** It bought Shillelagh locked to
Wisdom, which mattered when the melee fallback was the plan B. The routine is now eight 18 m
beams and a Flurry — **Flurry of Blows is unarmed and never used Shillelagh** — so what
Shillelagh protected was a quarterstaff swing this body takes a handful of times a run.
Guidance is not a reason either: **Druid 1 and Cleric 1 both carry it on the cantrip list**, so
the style was selling a spell the chassis already owns.

**Carry Mourning Frost through Acts I and II, then replace it with Markoheshkir.** Mourning Frost
is assembled in the Underdark and keeps the shield: the installed tweak gives it Arcane
Enchantment +1, Spell-DC Insidious Cold, Heart of Ice's **+1 Cold per damage event**, Freezing
Gust and `PRONE_ICE` immunity. **[database: `MAG_Cold_IncreaseColdDamageOnCast_Staff`]**

Markoheshkir is the Act III upgrade. Its installed Cold attunement reads
`IF(SpellDamageTypeIs(Cold) and IsSpell()):DamageBonus(ProficiencyBonus, Cold, false)`, so at level
20 it adds **+6 Cold to each Hellrime beam**, versus Mourning Frost's +1; both weapons carry the
same +1 spell attack/DC passive. It also applies two Encrusted-with-Frost turns once per attack
and unlocks Ice Storm and Cone of Cold. By then Winter Spirit already supplies ice-slip immunity,
so Mourning Frost's defensive edge is redundant. **[database: Markoheshkir Expanded + AOE Status
Fixer]**

Neither staff is a melee plan. Strength is 8, so a staff swing is unavailable in practice; use
the 18 m beams or Flurry of Blows. **A shield remains mandatory** — Guardian of Light keeps
Unarmoured Defence working and grants advantage on Concentration checks for Friar's Bond.


---

## Feats — seven

Cadence is per **class level**, `featFrequency 3` plus `alwaysGrantFeatAtLevels {"13": true}` →
**3 / 6 / 9 / 12 / 13 / 15 / 18**. **[pak: `MCM/FeatsUni.json`]** Against the progression order
below they land at characters **3, 6, 10, 13, 16, 19, 20**.

| Char | Class rung | Feat | What it buys |
|---|---|---|---|
| 3 | Ranger 3 | **Eldritch Adept → Elemental Blast** | The engine, on the level Glaring Frost arrives. Not the half-feat variant — this one carries no ability increase |
| 6 | Druid 3 | **Dungeon Delver (WIS)** | WIS 21, **Expertise in Perception**, advantage against traps |
| 10 | Monk 3 | **Elemental Adept: Cold** | WIS **22**, `IgnoreResistance(Cold,Resistant)`, and **+1 Cold per damage instance** |
| 13 | Druid 6 | **Alert** | Initiative **+ proficiency bonus**, immunity to being Surprised |
| 16 | Druid 9 | **Durable** | +1 CON, **full hit points on every short rest**, in-combat regeneration below 60% |
| 19 | Druid 12 | **Tough** | +1 CON → **22**, +2 HP per character level, **+2 Constitution saves** |
| 20 | Druid 13 | **Shield Master** | +2 DEX saves, **−1 to all damage taken**, and Block as a *passive* — Rogue Evasion, spending no reaction |

### Elemental Adept was cut on the previous sheet, and the engine change re-priced it

```
ElementalAdept        Selectors "SelectPassives(f6b6e71f-…,1);SelectPassives(97c15ad1-…,1)"
ElementalAdept_Cold   Boosts "IgnoreResistance(Cold,Resistant);
                              IF(HasDamageDoneForType(DamageType.Cold)):DamageBonus(1, Cold)"
```

The old reasoning was *"it pierces resistance but not immunity, and the rider only has to land, not
to be large."* **True while the beam was Force and Cold was a small rider on top. False now.**
Hellrime is `1d8` Cold and Winter Spirit adds `+WIS` Cold, so the entire beam is Cold and Cold
resistance halves all of it. Three grants, all live:

- **`+1 WIS` through a passive selector**, not `SelectAbilities` — so Wisdom **22 guaranteed**, with
  no dependence on the ability-picker question or on Hag's Hair.
- **`IgnoreResistance(Cold, Resistant)`** across the whole engine.
- **`+1 Cold per instance`** — eight beams is **+8 a round**, and it rides the retaliation ticks.

### Notes on the rest

**Alert's Perception proficiency is dead weight** — Dungeon Delver already gives Expertise. What
you are buying is the initiative bonus, now **proficiency bonus** rather than +5 **[data]**, and
**immunity to being Surprised**. The Surprise half is *not* redundant with Battlemind Link, and
the Link is a great deal larger than earlier drafts of this sheet allowed: **[database]**

```
Mesmerist_Target_BattlemindLink  SpellFlags "IsSpell"        — no IsConcentration
                                 UseCosts   "ActionPoint:1;SpellSlotsGroup:1:1:3"
                                 ApplyStatus(MESMERIST_BATTLEMINDLINK,100,10)   — self and target
MESMERIST_BATTLEMINDLINK  AuraRadius   "6"
                          AuraStatuses "TARGET:IF(HasStatus('MESMERIST_BATTLEMINDLINK')):
                                        ApplyStatus(BATTLEMIND_BONUS)"
                          RemoveEvents "OnCombatEnded"
BATTLEMIND_BONUS  Boosts "Initiative(2);DamageBonus(2);AC(2);StatusImmunity(FLANKED);
                          StatusImmunity(SURPRISED);IgnoreLeaveAttackRange();Advantage(AttackRoll)"
```
**[database: `Mesmerist`, load order 431]**

**`Advantage(AttackRoll)` is the load-bearing term, and no earlier description on this sheet
carried it.** It is unconditional advantage on attack rolls, so it lands on **every one of the
eight Hellrime beams**, not merely on beams aimed at a target Glaring Frost has already blinded.
One 3rd-level slot, cast by the partner, buys that plus `AC(2)`, `DamageBonus(2)`, `Initiative(2)`
and immunity to `FLANKED` and `SURPRISED` — **no saving throw and no concentration**, since the
spell's `SpellFlags` is `IsSpell` alone.

**The aura is mutual and doubly gated.** `AuraStatuses` fires on a `TARGET` that itself holds
`MESMERIST_BATTLEMINDLINK`, so both bodies must carry the status *and* each must stand inside the
other's **6 m** `AuraRadius`; step outside and both lose `BATTLEMIND_BONUS` at once. It is also
`RemoveEvents "OnCombatEnded"` on a 10-turn duration, so it is **recast every fight** rather than
pre-buffed — which is exactly why Alert still earns its place: the Link's own
`StatusImmunity(SURPRISED)` only covers rounds where the Link is already up, and an ambush from
`Hunted - Dynamic Ambushes` or `Sensible Ambushing` fires before that. Initiative is
`d10 + Dex + bonuses` from `Initiative Variants` (`1247`).

**Shield Master is swappable for `Mage Slayer`.** Both are last-feat shapes — instantaneous value,
nothing that ramps with level. Shield Master's passive Evasion covers the threat this body is
worst against, since Dexterity is the weakest of its four proficient saves at `+8` and Dexterity is
what large area damage rolls against. Mage Slayer instead gives advantage on saves against **all**
spells and reduces spell damage by the proficiency bonus, but Wisdom is already `+12` and
Constitution `+14`, so it is insurance on rolls that rarely fail — and Fixation's rebuilt feat list
takes Mage Slayer *and* Shield Master, so the swap changes nothing the pair already covers on that
body, where the same grant reaches saves that have no proficiency at all. **If area damage turns out
to be the smaller problem in play, swap them.** The shield is already there: Guardian of Light
keeps Unarmoured Defence working with one equipped, and Monk's own Evasion is a level 7 feature,
so there is no duplication at Monk 3.

### Feats considered and rejected

- **Spell Sniper** carried the engine on the previous sheet and has no job left. Elemental Blast is
  the vehicle and the container already supplies three damage types, so what remains is the crit
  threshold — worth about `+7` a round on a body with no Mortal Reminder to feed — plus damage-die
  advantage on the first beam and the low-ground clause.
- **War Caster.** Friar's Bond is welded on for the whole run, so protecting it looks urgent. But
  **Guardian of Light already grants advantage on Concentration checks**, and Constitution saves
  run `+14`. Nothing left to buy.
- **Resilient.** The feats file calls it the most under-described feat in the list, and it is right
  — but this body already owns the top four saves: Strength and Dexterity from Ranger 1, Wisdom and
  Constitution from Lone Wolf. Only Intelligence and Charisma remain, the bottom of the value
  ordering, and the `+1` would land on a dump stat.
- **Eldritch Adept (Essential) → Devil's Sight**, which the previous sheet took at character 9 to
  make Circle of Winter's **Darkness** one-sided. **Darkness is concentration and Friar's Bond holds
  the only slot from character 10** — the plan was castable for four levels and never again. Not a
  compromise, a contradiction that has been removed.
- **Telekinetic**, and any other push effect: pushing enemies out of melee starves three of the six
  blind sources, which is the same reason **Repelling Blast** is banned.
- **Lucky.** Three points on a **long rest** clock, in a list where long rests cost 120+ supplies.
- **Do not take Agonizing Blast** — `IF(IsEldritchBlastAlike() and IsCharismaModifierPositive())` is
  false at CHA 8. **Do not take Magic Initiate: Warlock for the blast** — it binds Charisma.

---

## The Mirror of Loss

`references/listo-rules.md`: **+2 to a chosen ability against a hard cap of 24, plus a separate +1
Charisma, per character**, behind Religion DC 25 in Act III. Put the +2 on **Wisdom**:

```text
WIS 22 -> 24    Beam damage             +6 -> +7 Cold per beam    (+8 a round)
                Beam attack             +12 -> +13
                Glaring Frost DC        20 -> 21
                Friar's Retribution     12 -> 14 Radiant per incoming hit
                Unarmoured Defence      20 -> 21
```

22 + 2 lands **exactly** on the cap, which is why the WIS climb stops at two half-feats — a
pre-Mirror 23 would be thrown away.

**That is also why Hag's Hair does not belong here.** It would put Wisdom on 23 before the
Mirror and the Mirror's second point would fall off the cap. Spend it on **Fixation's
Constitution 21 → 22** instead, where it buys a modifier that body has no other route to.

**The separate +1 Charisma is dead** — 8 → 9 moves nothing.

**Coldsnap can now roll its own check.** Astral Knowledge supplies the Religion proficiency it
lacked, so the check is `+6` at INT 10, plus Guidance — a Druid and Cleric cantrip — and
Emboldening Bond's `1d4`. Against DC 25 that is `d20 + 2d4 ≥ 19`, about **35%**: enough to try,
not enough to plan on. The 100-gold Withers respec into Religion Expertise stays the certain
route, and Fixation clears its own check separately — the +2 lands on whoever rolled.

---

## Concentration budget

**Friar's Bond holds the only slot, permanently.** That rules out Sleet Storm, Moonbeam, Heroism,
Faerie Fire, Conjure Woodland Beings, Hold Monster — **and Darkness**, which is why the
self-obscurement plan is not on this sheet and Devil's Sight is not among the feats. Accept it —
Bond is a third of the engine and the pair's Rescue floor.

Mitigation: shield + Guardian of Light (advantage) and CON proficiency from Lone Wolf at +11.

**Everything the engine does is concentration-free**: Elemental Blast, Glaring Frost, Winter Spirit,
Armour of Agathys, Retribution, ColdSoul, SlipperyMagic, Blizzard Cloud, Ice Storm, Cone of Cold,
Snilloc's. **Conjure Animals** is made non-concentration until long rest by `13458`, so the summon
set does not compete either.

**Resource budget per fight**, on the rubric's three-fights-per-long-rest arithmetic: ki **4, in
full** (short-rest pool), levelled slots ≈ **5.7** of a caster-15 table, Wild Shape **2** (short
rest) for Winter Spirit re-ups, Emboldening Bond **5** per long rest. The binding constraint is the
8-action / 8-bonus-action budget, not any pool — which is what makes the at-will beam routine the
default and the slots pure surplus.

---

## Spells and cantrips

- **Cleric cantrips:** Word of Radiance, Sacred Flame, Resistance. Guidance is already on
  Guardian of Light. **These are the answer to Cold immunity** — the only Radiant the build can aim.
- **Druid cantrips — four picks, at Druid 1, 4 and 10**, plus Ray of Frost free from the circle at
  Druid 2. Thorn Whip and Produce Flame at Druid 1; then two that are worth naming, because both
  do something the beams cannot:
  - **Moonflare** (Druid 4) — `Projectile_Moonflare`, 18 m, ranged spell attack,
    `DealDamage(LevelMapValue(D8Cantrip),Radiant)` and `ApplyStatus(GLITTERING_LIGHT,100,2)`
    **[pak]**. It is the only **Radiant** attack cantrip on the Druid list, so it fires Glaring
    Frost's Radiant branch at range where Word of Radiance is a 3 m self-centred burst — *and* it
    illuminates the target the Callous Glow Ring needs. Winter Spirit's `+Wis` Cold rider lands on
    top, so one Moonflare hit carries **both** Glaring Frost predicates at once.
  - **Frostbite** (Druid 10) — `Target_Frostbite`, 18 m,
    `SpellRoll "not SavingThrow(Ability.Constitution, SourceSpellDC())"`, Cold **[pak]**. It is an
    at-will **saving throw** that deals Cold, which is exactly what `SlipperyMagic` requires and
    exactly what the beams can never supply. It lands on the level SlipperyMagic does.

  All of them carry Winter Spirit's Cold rider, so all of them proc.
- **Circle spells, always prepared:** Ray of Frost (2), Darkness *(unusable — concentration)* +
  Snilloc's Snowball Storm (3),
  Sleet Storm + Slow (5), Fire Shield + Ice Storm (7), Cone of Cold + Hold Monster (9).
- **Peace domain, always prepared:** Sanctuary, Heroism.
- **Druid list:** Healing Word and Lesser Restoration for the Rescue floor; Greater Restoration from
  5th-level slots; Conjure Animals for the Actions axis.

---

## Progression order

**Re-derived level by level. No respec is needed** — the per-level optimum is monotone, so every
level is a forward pick. Characters 1–5 are locked (no Withers yet) and happen to already be
right.

**Every locked pick is in the `Choose` column.** A feat is not the only thing a level asks you
for — a fighting style, a conclave, a circle, a domain and its skill, and every cantrip and
half-caster spell *known* are all respec-only. They are listed here rather than left implicit,
because the sheet is a build order and a level with an unspent selector is a level not yet
finished.

| Char | Take | Choose | What lands | Feat |
|---|---|---|---|---|
| 1 | Ranger 1 | <b>3 skills</b> → Perception, Investigation, Survival · <b>Favoured Enemy</b> → <b>Beast Tamer</b> (Find Familiar, once per short rest) · <b>Natural Explorer</b> → <b>Deft Explorer</b>, Canny on <b>Investigation</b> | Str + Dex saves, martial weapons, medium armour, shields. <b>Ranger must be first</b> | — |
| 2 | Ranger 2 | <b>Fighting style</b> → <b>Close Quarters Shooter</b> · <b>2 Ranger spells known</b> → Longstrider, Cure Wounds | <code>RollBonus(RangedSpellAttack, 1)</code> on every beam, and no point-blank disadvantage | — |
| 3 ★ | Ranger 3 | <b>Conclave</b> → <b>Snowlight</b> · <b>+1 Ranger spell known</b> → Ensnaring Strike · feat | Glaring Frost, Snowborne, and always-prepared Armour of Agathys with its undocumented no-save Blind hook. <b>The beam engine is live on this level</b> | **Eldritch Adept → Elemental Blast** |
| 4 | Druid 1 | <b>2 Druid cantrips</b> → Thorn Whip, Produce Flame | Wild Shape charges, 1st-level slots | — |
| 5 ★ | Druid 2 | <b>Circle</b> → <b>Circle of Winter</b> | <b>Winter Spirit</b>. The beams pick up <code>+Wis Cold</code> on top of their own, and 65 temporary hit points arrive. Ray of Frost arrives free as a circle spell | — |
| 6 | Druid 3 | feat | <b>Snilloc's Snowball Storm</b> — the first area cold, so the first <em>area</em> Blind. <b>Three levels earlier than the previous ladder</b> | **Dungeon Delver** |
| 7 ★ | <b>Cleric 1 (Peace)</b> | <b>Domain</b> → <b>Peace</b> · <b>Peace's level-1 skill</b> (Insight / Performance / Persuasion) → <b>Persuasion</b> · <b>3 Cleric cantrips</b> → Word of Radiance, Sacred Flame, Resistance | <b>Word of Radiance</b> fires Glaring Frost's Radiant branch, so the Blind engine keeps running against Cold-immune enemies. <b>Emboldening Bond</b> (+1d4 to every save on <em>both</em> characters), always-prepared Sanctuary | — |
| 8 | Monk 1 | — | Unarmoured Defence (10 + Dex + Wis), Martial Arts | — |
| 9 | Monk 2 | — | Uncanny Metabolism, Patient Defence, Step of the Wind | — |
| 10 ★ | Monk 3 | <b>Way</b> → <b>Way of the Friar</b> · feat | Friar's Bond + Retribution, Guardian of Light (a shield without losing Unarmoured Defence, and advantage on Concentration) | **Elemental Adept: Cold** |
| 11 | Druid 4 | <b>3rd Druid cantrip</b> → <b>Moonflare</b> | 2nd-level slots deepen | — |
| 12 | Druid 5 | — | 3rd-level slots, <b>Conjure Animals</b> — a third body, non-concentration until long rest | — |
| 13 | Druid 6 | feat | Blizzard Cloud, and Winter Spirit's <code>PRONE_ICE</code> immunity gate opens — this body stops slipping on its own ice | **Alert** |
| 14 | Druid 7 | — | 4th-level slots, <b>Ice Storm</b> — save-for-half, so it damages every target and therefore Blinds every target | — |
| 15 | Druid 8 | — | — | — |
| 16 | Druid 9 | feat | 5th-level slots, <b>Cone of Cold</b> | **Durable** |
| 17 | Druid 10 | <b>4th Druid cantrip</b> → <b>Frostbite</b> | <b>SlipperyMagic</b> — Prone on any failed saving throw against your Cold | — |
| 18 | Druid 11 | — | 6th-level slots. <b>The fourth beam lands at character 17</b>, not here | — |
| 19 | Druid 12 | feat | <b>ColdSoul</b> — immunity to Cold, and every melee attacker takes half your Druid level in Cold | **Tough** |
| 20 | Druid 13 | feat | 7th-level slots. Circle of Winter has nothing left to give | **Shield Master** |
| *III* | — | ***Mirror of Loss* → Wisdom** — `22 → 24`, on the cap | Beam damage, beam attack, Glaring Frost's DC, Retribution and Unarmoured Defence all move together | — |

**Two picks on character 1 are not free.** `Deft Explorer`'s **Canny** is a straight Expertise on
one already-proficient skill **[data]** — put it on Investigation, and it is now **priced into
§8** and the pair sheet's gate table. `Beast Tamer` is a Find Familiar on a short-rest clock — a
third body on the axis this pair is thinnest on — and stays under *Open decisions*, because
moving Actions cascades into three pair sheets and the finalists board.

**What is *not* a locked choice, and so is not in the column.** Druid and Cleric spells are
**prepared**, not known — swappable at every level-up and after every long rest, so the Spells
section below is a loadout, not a selector. Wild Shape forms are automatic from Druid level.
Feats have their own column because the pair sheets already carry one.

**The engine is live at character 3** — Glaring Frost and a natively Cold beam on the same level.
Winter Spirit at character 5 makes it bigger; it is no longer what switches it on.

### The two changes against the previous ladder

**Cleric 1 moves from character 20 to character 7.** It was previously live for one level out of
twenty. It carries two things this pair needs early and neither of them scales with Cleric level:

- **Emboldening Bond** — a *pair*-scope **+1d4 to every saving throw on both characters**. It is
  a registered blanket booster in `scoring.py`, and moving it into Acts I and II lifts the Saves
  rung on **both** bodies. Saves is the highest-weighted axis in the model.
- **Word of Radiance** — an area **Radiant** cantrip. Glaring Frost's predicate is
  `HasDamageDoneForType(DamageType.Cold) or HasDamageDoneForType(DamageType.Radiant)`, so this
  is a Blind that works on Cold-immune enemies, arriving in Act I rather than never.

**Druid 3 moves from character 9 to character 6** — Snilloc's Snowball Storm is the first *area*
Cold, so the first area Blind, and Darkness is the self-obscurement plan. The second feat comes
with it, two levels early.

**What it costs:** Monk 3 slips from 8 to 10, so Friar's Bond is two levels later, and the four
Druid feats each land about one level later. Against a pair-wide save booster running for
thirteen extra levels, that is not close.

---

## Gear — notable options by act

Bold entries are the default pair allocation. Alternatives are real swaps, not a second
simultaneous loadout.

| Slot | Act I | Act II | Act III |
|---|---|---|---|
| **Main hand** | **Mourning Frost** once its three Underdark pieces are assembled; Melf's First Staff is the earlier +1 attack/DC bridge | **Mourning Frost** — +1 attack/DC, +1 Cold, Spell-DC Insidious Cold, Freezing Gust, ice immunity | **Markoheshkir** on Cold attunement — +1 attack/DC and **+PB Cold per Cold-spell damage event**; keep Mourning Frost as the Insidious Cold swap |
| **Off-hand** | Any +1 shield; Safeguard Shield is +1 all saves, but Fixation's rebuilt chassis carries a shield too, so the only copy is contested | **Guardian of Light** from Friar 3 — preserves Unarmoured Defence and gives Concentration advantage | **Guardian of Light**; no normal shield beats protecting the permanent Friar's Bond slot |
| **Ranged stat stick** | No engine piece; Bow of Awareness is +1 initiative and uncontested — Fixation carries no weapon | **Bow of Awareness**; Fixation's engine is Eldritch Blast with a shield in the off-hand, so it never wants a bow | **The Dead Shot** for its unconditional global critical-threshold −1; Hellrider Longbow is the initiative/Perception swap |
| **Body** | Chain Shirt through character 7, then **The Graceful Cloth** at Monk 1 for +2 Dexterity and the resulting +1 AC | **Robe of Exquisite Focus** for +1 spell DC; Graceful Cloth is the +1 AC/Dex-save swap | **Vest of Investiture** for +2 AC, physical resistance and regeneration; Robe of the Weave trades that defence for +1 spell attack/DC |
| **Head** | Haste Helm for opening movement; Shadespell Circlet is the conditional DC option | **Fistbreaker Helm** for +1 spell DC and +1 initiative; Coldbrim Hat adds two Frost turns only once per turn | **Hood of the Weave** for +2 spell attack/DC; Mask of Soul Perception trades the DC for +2 attack and initiative |
| **Cloak** | Cloak of Spell Focus (+1 DC) or Arcane Exercise (+1 spell attack) from Cloaks of Faerûn's common pool | Cloak of Spell Focus; Cloak of Protection is the +1 AC/all-saves defensive swap | **Cloak of the Weave** for +1 spell attack/DC and Absorb Elements |
| **Gloves** | **Winter's Clutches** from Lady Esther or the Myconid reward — two Frost turns per Cold attack | **Winter's Clutches**; each Hellrime beam is an independent attack, so AOE Status Fixer's placeholder clears between beams | **Winter's Clutches**; Markoheshkir adds another two Frost turns once per attack |
| **Boots** | Hoarfrost Boots only until Mourning Frost is assembled, then **Boots of Stormy Clamour** | **Boots of Stormy Clamour** — Blind and Frost applications feed two Reverberation once per attack; Winter Spirit supplies ice immunity from character 13 | **Boots of Stormy Clamour**; Fixation gets the pair's ice-proof footwear |
| **Amulet** | **Necklace of Elemental Augmentation** from Crèche Y'llek; Amulet of Misty Step before the crèche | **Necklace of Elemental Augmentation** | **Necklace of Elemental Augmentation**; Amulet of the Devout is the +2 DC control swap |
| **Rings** | Crusher's Ring / Ring of Protection as uncommitted utility; no Act I ring is part of the engine | **Snowburst Ring + Callous Glow Ring** — ice around every Cold target, plus 2 Radiant per illuminated damage event for Glaring Frost's alternate branch | **Snowburst + Callous Glow**; Coruscation is the attack-debuff swap when Cold immunity is not in the encounter |
| **Trinket** | Pearl of Power from Dhourn; Professor Orb is the skill swap | Lens of Astute Observation (+3 Investigation) or Hourglass of Distorted Perception (three-turn Haste, once/short rest) if Fixation is not using it | **Codex of the Arcanes** from Lorroakan — +3 spell attacks and +3 spell save DC; it also grants Cone of Cold, Flame Strike and Blade Barrier |

### Decisive installed implementations

- **The necklace is settled, not an open test.** Its final passive is an `OnDamage`
  `DamageBonus(max(1,SpellCastingAbilityModifier))` gated by a native elemental cantrip damage
  type. Hellrime is natively Cold and every beam is a damage event, so this is **Wisdom per beam**.
  **[database: Homebrew Spells, load order 247]**
- **Winter's Clutches remains a multi-beam item.** AOE Status Fixer holds a placeholder until one
  attack resolves, converts it to two real Frost turns, then removes the placeholder. Hellrime's
  beams are independent attacks. Coldbrim's `DO_NOT_REMOVE` placeholder is instead once per turn.
  **[database + indexed runtime Lua fallback]**
- **Fixation, not Coldsnap, owns the ice-proof boots, and Battlemind Link is why it is not
  optional.** Mourning Frost covers Coldsnap in Act I; Winter Spirit supplies personal
  `PRONE_ICE` immunity from character 13. Fixation, unarmoured on the rebuilt chassis, has
  neither — and `MESMERIST_BATTLEMINDLINK`'s `AuraRadius "6"` **[database: `Mesmerist`, load order
  431]** keeps it standing inside the beams' `WaterFrozen` carpet for the whole fight, because
  `Advantage(AttackRoll)` from `BATTLEMIND_BONUS` stops the moment either body leaves the 6 m aura.

Do not wear Icebite Robe merely to complete the visual set. Ring of Elemental Infusion is also a
melee follow-up rider and has no place in the two-Action beam routine.

---

## Scores

Rubric: `skills/listo-build/references/axis-rubrics.md`. §1 and §2 are computed against par
(single-target **60 / 87 / 123**, AoE **48 / 65 / 82**), both sides carrying the per-instance gear
constant `k` = **+3 / +5 / +8**; §3 is computed; the rest read against the act tables.

**Re-derived against the finished feat list.** Three inputs moved: `Elemental Adept: Cold` adds
**+1 Cold to every damage instance** from character 10, the Mirror's Wisdom 24 puts **+7** rather
than +6 of Winter Spirit rider on each beam in Act III, and dropping `Skilled Expert` leaves
Dexterity at 15, so Act II's AC reads **20** rather than 21.

**Re-derived a second time against the checkpoints.** Three more inputs moved: ki is the Monk
level, so the Act I checkpoint (character 8, Monk 1) has **2**, not 4 — a Flurry every other
round; the Act II checkpoint (character 15) is **Druid 8**, so the strongest credited area cast
is **Ice Storm**, not Cone of Cold, which arrives at character 16; and §2's beam share now takes
the rubric's `0.65/0.775` attack-roll-area correction — the same term the partner's sheet has
always carried, because par's area damage is save-for-half and a beam that misses deals nothing.
The blind's advantage stays on §1 only: spread beams open on fresh, un-blinded targets.

> **This table is the body scored alone, with no accuracy multiplier.** The pair sheets apply one
> for Glaring Frost's own routine Blind — `pair-schema.md` tier 1, save-gated, `1.19` — times this
> body's **attack-roll share**, because Friar's Retribution is Radiant and ColdSoul is Cold and
> neither is an attack roll, times the first-instance lag against a fresh target:
>
> | act | attack rolls | share | lag | `mult.st` |
> |---|---|---:|---:|---:|
> | **I** | 4 beams (38) + Flurry (5.5) of 47.5 | 91.6% | 5/6 | **1.15** |
> | **II** | 6 beams (69) + Flurry (13) of 87 | 94.3% | 7/8 | **1.16** |
> | **III** | 8 beams (100) + Flurry (13) of 121 | 93.4% | 9/10 | **1.16** |
>
> Single-target then reads **3 / 4 / 5** there. Both tables are the same arithmetic; only the
> multiplier differs, and it belongs on the pair surface because par cannot answer it.
> The earlier sheets carried a flat `1.14` above prose claiming an 84% attack-roll share, which
> was true of neither the old raws nor the new ones.

| axis | I | II | III |
|---|---|---|---|
| Single-target | **2** | 3 | **4** |
| AoE | 2 | **5** | **5** |
| Durability | 4 | **5** | **5** |
| Actions | 2 | 3 | 3 |
| Control (single) | 4 | 4 | 4 |
| Control (area) | 3 | 4 | 4 |
| Rescue | 4 | 4 | 4 |
| Skills | 2 | 3 | 4 |
| Saves | 4 | 4 | 4 |
| Endurance | 4 | 4 | 4 |

**§1 Single-target.** Both Actions on one target. Beams are `LevelMapValue(EldritchBlast)` — 2 per
Action at char 8, 3 at 15, 4 at 20. Ki is the Monk level: **2 at the Act I checkpoint** (Monk 1 at
character 8), 4 from Monk 3 — so Act I supports a Flurry every other round, the later acts one a
round.

| | beams | Flurry | Retribution | ColdSoul | raw | inst | with `k` | ratio | rung |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **I** (char 8, WIS 21) | 4 × 9.5 = 38 | 5.5 | 4 | — | 47.5 | 5.4 | 64 | 1.06 | **2** |
| **II** (char 15, WIS 22) | 6 × **11.5** = 69 | 13 | 5 | — | **87** | 8.4 | 129 | 1.48 | **3** |
| **III** (char 20, WIS 24) | 8 × **12.5** = 100 | 13 | 5 | 3 | **121** | 10.8 | 207 | 1.69 | **4** |

A beam is `1d8` Cold (4.5), plus Winter Spirit's `+Wis` Cold rider, plus **Elemental Adept's `+1`
per instance** from character 10: `4.5 + 6 + 1` in Act II and `4.5 + 7 + 1` in Act III. Friar's
Retribution is **Radiant** and collects nothing from Elemental Adept; ColdSoul is Cold and does.
**Flurry is left flat** — whether an unarmed strike picks up Winter Spirit's
`CharacterWeaponDamage(1d6,Cold)` is still the open item below, and if it does, both later acts
gain another two points of raw.

`h` cancels — par rolls attacks and so does every beam. **Retaliation is discounted to the boss
rate here**: §3's constants put a boss at **one** attack a round, and a blinded boss swings at
disadvantage, so Retribution and ColdSoul land about 0.42 times a round rather than every round.
That is the honest number for a single-target axis; §2 below counts them at the crowd rate, which
is why the same two features are worth three times as much there.

**§2 AoE.** Beams spread across four targets, one Action on a slot spell about 70% of rounds, and
retaliation discounted to ~2 procs because blinded enemies attack at disadvantage and miss. At the
Act II checkpoint Coldsnap is **Druid 8**, not Druid 9 — Cone of Cold arrives at character 16 — so
**Ice Storm** (Druid 7, character 14) is the strongest credited four-target cast: `2d8 + 4d6` (23)
plus Winter Spirit's `+6` rider plus Elemental Adept's `+1` is `30` per target,
`4 × 30 × 0.7 = 84`. The beam share then takes the rubric's `0.65/0.775` attack-roll-area
correction (`× corr` below), because par's area damage is save-for-half and a beam that misses
deals nothing; the blind's advantage is credited on §1 only.

| | beams | slot spell | retaliation | raw | inst | with `k` | × corr | ratio | rung |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **I** | 4 × 9.5 = 38 | none — Druid 2 | 15 | 53 | 5.5 | 70 | 0.884 | **1.28** | **2** |
| **II** | 3 × **11.5** = 34.5 | Ice Storm × 0.7 = **84** | 24 | **142.5** | 7.8 | 182 | 0.961 | **2.68** | **5** |
| **III** | 4 × **12.5** = 50 | Cone of Cold × 0.7 = **123** | 31 | **204** | 9.8 | 282 | 0.960 | **3.31** | **5** |

Both slot spells move for the same two reasons the beams do: their dice carry Winter Spirit's
rider at `+6` then `+7`, and Elemental Adept adds a point per target instance. Act I falls to
rung 2 under the correction — four bare beams against par's two Fireballs. Act II clears the
rung-5 line by `0.03`, and it leans on Winter Spirit's rider landing on a save spell — the same
Hit-flag reading the open items already carry; if that reading fails, the act reads `2.44` and
rung 4. Act III clears with room. Snilloc's and Sleet Storm remain the cheaper tactical casts, but
the axis credits the strongest available four-target routine rather than averaging weaker
alternatives into it.

**§3 Durability.** `pool ratio × 0.65/p_hit`, with Lone Wolf's +30% HP and halving excluded as
universal to every chassis in the ledger.

| | HP | temp HP | pool ÷ par | AC | 0.65/p_hit | flat | ratio | rung |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **I** | 87 | 28 | 115/65 = 1.77 | 19 | 1.18 | — | 2.09 | **4** |
| **II** | 157 | 69 | 226/115 = 1.97 | **20** | 1.30 | — | 2.55 | **5** |
| **III** | **267** | 86 | **353**/160 = 2.21 | 21 | 1.44 | Shield Master **−1** | 3.36 | **5** |

Act III's hit points move because **Durable at 16 and Tough at 19 take Constitution to 22** — an
extra point of modifier across all twenty levels — on top of Tough's own +2 a level. Act II's AC
falls a point because Dexterity stops at 15.

Winter Spirit's `ClassLevel(Druid)*5` is doing most of that — 65 temp HP at Druid 13 on top of
Friar's Bond topping the pool up every turn. **Both act-III 5s are contingent on Winter Spirit
being up**, and it is the thing an unlucky opening round removes.

**Control (single) 4** in every act: Blind that costs no concentration and repeats every round is
the rung-4 clause, and Agathys' no-save version is stronger than the anchors. It stops at 4 because
a blinded creature still acts — this is not hard control.

**Control (area) 3 / 4 / 4**: the same argument at four targets, held to 3 in Act I because two
beams is a two-target blind. Rung 5 needs 9th-tier area control and the build tops out at 7th.

**Rescue 4**: Friar's Bond temp-HPs the Kin every turn for no action — the rung-4 clause verbatim —
plus Sanctuary as Prevention and Greater Restoration from Act II. Rung 5's Act II anchor also wants
Flurry of Healing and Harm, which is Way of Mercy.

**Endurance 4**: the output is at-will with no clock, which is the rung-5 shape, discounted to 4 by
the rubric's own Warlock ruling — there is a real slot pool here and it is worth naming.

> **Skills, derived rather than judged.** `scoring.py`'s `derive_skills` on this body's own
> modifiers — Perception `+11/+16/+18` (Dungeon Delver's Expertise), Investigation `+6/+10/+12`
> (**Deft Explorer's Canny, now priced**), Persuasion `+2/+4/+5`, plus the untrained
> Sleight of Hand `+2` that keeps Araj from reading as unrollable — gives the **2 / 3 / 4** the
> table carries. What the axis actually reports is a pair value, computed on the *evidence*
> rather than on these rungs: with Expertise on both Perception and Investigation the pair reads
> **5 / 5 / 5** — double Expertise on a Wisdom body is what finally clears the 15–25 trap band's
> mean, which no proficiency-only pair does.

> **The race moves no rung either.** Ranger 1 already carried Perception and Investigation, so
> Astral Knowledge and Keen Senses both land on proficiencies the chassis held. The only skill
> they add is **Religion**, and `axis-rubrics.md` §8 excludes the Mirror from scoring outright
> because it is rentable at Withers for 100 gold.

---

## Known weaknesses

- **The loop suppresses itself.** Blinded enemies attack at disadvantage, so they hit less, so they
  proc Retribution, ColdSoul and the Agathys blind less. Every retaliation number above is
  discounted for this and should stay discounted.
- **Cold immunity switches the *blind* off, not the damage.** Every trigger but Friar's
  Retribution is Cold. Two answers now: switch the beam container to **Brimstone** or
  **Vitriolic**, which keeps the `1d8` at full weight and loses only the rider, and **Word of
  Radiance / Sacred Flame** for the Radiant branch of Glaring Frost. Cold *resistance* is no
  longer a problem at all from character 10 — `Elemental Adept: Cold` pierces it. The pair's
  off-type cover is **Force**, not Psychic: Fixation's rebuilt chassis is **Mesmerist 12 (Aspect of
  the Eyebiter) / Sorcerer 6 (Draconic Bloodline — Amethyst) / Warlock 2 (Hexblade)**, and Amethyst
  routes Elemental Affinity to Force **[database: Draconic Bloodline Expanded, load order 408 —
  `ElementalAffinity_Damage`]**, so its eight Eldritch Blast beams are `1d8` Force with Charisma
  riders. The Psychic `Projectile_IllusionaryDart` **[database: Homebrew Spells, load order 247]**
  survives on that sheet only as an off-type fallback, so Force immunity, not Psychic immunity,
  is the case where both bodies need a third type.
- **Investigation Expertise is covered, and it is now priced.** `Skilled Expert` left both sheets,
  but `Deft Explorer`'s Canny — a locked character-1 pick — is double proficiency on Investigation
  **[data]**, so it reads `+6/+10/+12` across the acts. The §8 rungs above and the pair sheet's
  gate table are derived with it; it is the single input that lifts the pair's Skills to 5/5/5.
- **The ice is a liability for the partner, and Battlemind Link's 6 m leash makes it structural.**
  Every beam lays `CreateSurface(2,2,WaterFrozen)` and this body is immune to `PRONE_ICE` from
  Druid 6; Fixation is not, and no feat in the list grants that immunity. The two facts now
  interact: the pair's accuracy runs through `MESMERIST_BATTLEMINDLINK`'s `AuraRadius "6"`
  **[database: `Mesmerist`, load order 431]**, whose `Advantage(AttackRoll)` only pays while each
  body stands inside the other's 6 m aura — so **holding the bonus live pulls Fixation into the
  ice carpet this body is generating**, eight surfaces a round. Mitigation is already routed in the
  gear table: the pair's `PRONE_ICE`-immune footwear goes to **Fixation** in every act it is not
  needed here, which is from the moment Mourning Frost's own ice immunity covers Coldsnap and
  permanently once Winter Spirit's `StatusImmunity(PRONE_ICE)` gate opens at character 13. The
  residual tension is the Act I window before Mourning Frost is assembled — when Coldsnap is
  wearing the ice-proof boots itself — and any round Fixation swaps them for another effect. Then
  the choice is Fixation prone or the pair's attack-roll advantage dropped for a turn. See the
  pair sheet.
- **Blind is a CON save** at DC 20. Brutes and undead pass it, and a blinded caster still casts —
  BG3's Blindness only imposes attack disadvantage and grants advantage against.
- **No Extra Attack anywhere, and the melee fallback is now genuinely bad.** Dropping Druidic
  Warrior for Close Quarters Shooter leaves the quarterstaff on Strength 8. What answers a body
  in melee is Flurry of Blows, `IgnorePointBlankDisadvantage(Spell)` keeping the beams at full
  accuracy, and Armour of Agathys blinding whatever hit you — not the weapon.
- **Persuasion is CHA 8.** Peace's level-1 skill pick buys proficiency, which is `+5` at level 20
  against Act III checks reaching DC 25–30 — enough to stop the body being a liability in a
  dialogue, not enough to be the face. The pair must still cover every social gate.
- **Winter Spirit is a single point of failure.** Lose the temp HP and the beam loses 6 damage
  *and* its blind trigger simultaneously. Re-upping costs an Action and a Wild Shape charge, and
  there are two per short rest.

---

## Open decisions and unverified items

- **One character-1 pick is still unpriced against the rungs.** Canny on Investigation and
  Peace's Persuasion are now folded into §8's derivation (**2 / 3 / 4** alone, **5 / 5 / 5** on
  the pair sheet). **Favoured Enemy → Beast Tamer** is not: Find Familiar once per short rest is
  a third body, and §4 Actions is this body's weakest axis at 2 / 3 / 3. **Re-derive §4 before
  the next ledger publish** — the cascade is three pair sheets and the finalists board, which is
  why it is not folded in here.
- **`~~Eldritch Blast's attack ability~~` — closed.** The previous sheet's largest open risk was
  whether Spell Sniper's class-UUID-free selector resolved the cantrip to Wisdom. Elemental Blast
  is granted through `UnlockSpell` in a passive's `Boosts` field instead, so the inference is no
  longer load-bearing. **Still read the tooltip at character 3** — it should say **+12** at level
  20, not `−1`.
- `(unverified)` **Whether `Elemental Adept: Cold`'s `+1 Cold` applies per beam or per cast.**
  The boost reads `IF(HasDamageDoneForType(DamageType.Cold)):DamageBonus(1, Cold)` **[pak]**, and
  each beam is its own damage roll, so per beam is the expectation — but it is the same shape as
  the Elemental Affinity question on the partner's sheet, and worth one tooltip check. Nothing
  else depends on it; the resistance-piercing half is unconditional.
- **`(unverified)` Winter Spirit versus Armour of Agathys.** Both key off the same temporary HP
  pool. With 65 temp HP standing, Agathys' smaller grant may not apply — in which case its *status*
  may still apply and the no-save blind still works, or it may not. The opposite outcome is also
  possible and better: `HasTemporaryHP()` staying true could keep Agathys up all fight instead of
  two hits. Vanilla `ARMOR_OF_AGATHYS` is base-game and not readable under the mods root. Five
  minutes in game settles it.
- **`(unverified)` Whether unarmed strikes take `CharacterWeaponDamage(1d6,Cold)`.** If they do,
  every Flurry strike is another Glaring Frost save and §1 rises. Excluded from the scores above.
- **`(unverified)` Whether the Winter Spirit rider applies per beam.** Agonizing Blast is the same
  construction — an IF-gated `DamageBonus` boost — and is known to pay per beam, which is the basis
  for the assumption. If it pays once per cast, beams fall to `1d8` and only the first carries the
  Cold trigger; §1 drops to roughly 2 / 2 / 3 and the build needs rethinking.
- **`(unverified)` Whether the elf base traits inherit.** `MoriAstralElf` is a subrace —
  its progression adds only Keen Senses and the Starlight Step charges, and never re-lists
  Darkvision, Fey Ancestry or Elf Weapon Training, so it is relying on the parent Elf table.
  That table is base-game and not readable under the mods root. Character creation shows the
  proficiency list before you commit; confirm there. Astral Knowledge, Keen Senses, Astral Fire
  and Starlight Step are all in the mod's own pak and are not at issue.
- **The author's intent was Druid-only.** The Winter Spirit rider's missing class predicate is a
  bug, not a design. A Circle of Winter update that closes it removes the Wisdom rider from every
  beam, but **does not switch the engine off**: Hellrime is natively Cold and still fires Glaring
  Frost. Damage falls; the Blind loop survives.
- **Two Eldritch Adept feats coexist** — `SYR_EldritchAdept` (Essential, +1 ability, vanilla
  invocations only) and `EldritchAdept` (Mizora, no ability, the Level 2 list). Different names,
  different UUIDs, neither overrides the other. `listo-10.2-feats.md` calls the load-order winner
  unresolved; it is not a contest. **[pak]**
- **Listo's 1d8 nerf does reach the elemental blast variants** — `[cust] MizoraReward_ListoPatch`
  redefines Hellrime, Brimstone and Vitriolic at `1d8`. `classes/warlock.md` marks this unverified;
  it is settled. **[pak]**
