# Fixation v2 — Eyebiter 12 / Amethyst Draconic 6 / Hexblade 2

**Mesmerist 12 (Aspect of the Eyebiter) / Sorcerer 6 (Draconic Bloodline — Amethyst) / Warlock 2
(The Hexblade)**, **Astral Half-Elf** — level 20, Lone Wolf duo partner for **Coldsnap v1**. A
Charisma beam caster: eight Eldritch Blast beams a round, each one four stacked Charisma riders
deep, and each one carrying **two independent saving throws** — a Wisdom save against Frightened
and a Constitution save against Poisoned.

Every mechanic marked **[database]** was resolved out of the compiled 10.2 snapshot
(`/tmp/listonomicon-character-data.sqlite`, profile `Listonomicon`, bg3forge 0.2.0), with
`source`, `load_order` and the decisive field named. **[wiki]** is bg3.wiki, used only for vanilla
Larian content whose base-game paks are not under the mods root.

**This is v2, and the chassis changed.** v1 was Eyebiter 13 / **Deep** Draconic 6 / **Great Old
One** 1, running **Psychic Illusionary Dart** beams and fishing for criticals to fire Mortal
Reminder. Three findings retired that shape; they are recorded in *What changed from v1* at the
end.

---

## The paired engine

1. **The partner supplies advantage — and so, it turns out, does this body.** Coldsnap's Glaring
   Frost blinds on a Constitution save from every Cold or Radiant instance, and attacks against a
   blinded creature have Advantage. But **Battlemind Link is a second, unconditional source**, and
   v1 under-read it. **[database: `Mesmerist`, load 431]**

   ```
   Mesmerist_Target_BattlemindLink  SpellFlags "IsSpell"          <- NOT concentration
     UseCosts "ActionPoint:1;SpellSlotsGroup:1:1:3"
     SpellProperties "ApplyStatus(SELF,MESMERIST_BATTLEMINDLINK,100,10);ApplyStatus(…,100,10)"
   MESMERIST_BATTLEMINDLINK  AuraRadius "6"   RemoveEvents "OnCombatEnded"
     AuraStatuses "TARGET:IF(HasStatus('MESMERIST_BATTLEMINDLINK')):ApplyStatus(BATTLEMIND_BONUS)"
   BATTLEMIND_BONUS  Boosts "Initiative(2);DamageBonus(2);AC(2);StatusImmunity(FLANKED);
                             StatusImmunity(SURPRISED);IgnoreLeaveAttackRange();Advantage(AttackRoll)"
   ```

   `Advantage(AttackRoll)`, on **both** bodies, for one 3rd-level slot, with no saving throw and no
   concentration — conditional only on the two characters standing inside a mutual **6 m** aura.
   v1's ladder listed this passive as "+2 AC, +2 damage, +2 initiative" and priced the pair's
   accuracy at the save-gated tier. `scoring.py`'s own `ACCURACY` registry already carries
   `battlemind-link` at **tier 2** (`x1.35`); v1 authored tier 1 (`x1.19`) against it. From
   character 12 this sheet takes the tier it was always entitled to.

   The 6 m leash is the cost, and it is a real one — see *Known weaknesses* §3.

2. **The beam is Eldritch Blast, and four separate riders land on every one of them.**

   ```
   Projectile_EldritchBlast   [Listo Master Spells Patch, load 755 — the load-order winner]
     SpellSuccess "DealDamage(1d8,Force,Magical);IF(HasStatus('REPELLING_BLAST_TRIGGER',…)):Force(4.5,…)"
     AmountOfTargets "LevelMapValue(EldritchBlast)"   TargetRadius "18"
     SpellRoll "Attack(AttackType.RangedSpellAttack)"   UseCosts "ActionPoint:1"
     SpellFlags "…;IsSpell;…"
   ```

   `LevelMapValue(EldritchBlast)` keys off **character** level: `1` at 1-4, `2` at 5-9, `3` at
   10-16, `4` at 17-20. **[database: `EldritchBlast` level map, Expansion Level 13-20 load 321]**
   Under Lone Wolf's second Action that is **2 / 4 / 6 / 8** beams a round across the run.

   | Rider | The gate it actually carries | Act III |
   |---|---|---|
   | Eldritch Blast | `DealDamage(1d8,Force,Magical)` | 4.5 |
   | **Potent Robe** | `MAG_CharismaCaster_CantripBooster_Passive` → `IF(IsCantrip() and not IsWeaponAttack()):DamageBonus(max(1,CharismaModifier))` **[Homebrew Spells, load 247 — the winning layer]** | +7 |
   | **Agonizing Blast** | `IF(IsEldritchBlastAlike() and IsCharismaModifierPositive()):DamageBonus(CharismaModifier)` **[Mizoras Rewards, load 416]** | +7 |
   | **Elemental Affinity (Force)** | `ELEMENTALAFFINITY_FORCE_EXTRA_DAMAGE_TECHNICAL` → `IF(IsSpell() and IsDamageTypeForce()):DamageBonus(max(0, CharismaModifier))` **[Draconic Bloodline Expanded, load 408]** | +7 |
   | **Hexblade's Curse** | `IF(HasStatus('HEXBLADES_CURSE',context.Target,context.Source)):DamageBonus(ProficiencyBonus)` **[Base Game: GustavX.pak, load 3]** | +6 |
   | | **per beam, cursed target** | **31.5** |
   | | uncursed | 25.5 |
   | *(Battlemind Link `DamageBonus(2)`)* | *real, but a pair-flat rider this ledger prices nowhere on either body* | *(+2)* |

   **8 beams = 252 a round on the cursed target**, against v1's 148.

3. **Amethyst is why the third Charisma rider exists.** Elemental Affinity binds to a damage type
   through a two-hop chain, and only the last hop carries the boost:

   ```
   DraconicAncestry_Amethyst   Boosts "UnlockSpell(Projectile_MagicMissile,AddChildren,…,Charisma)"
   ElementalAffinity_Damage    StatsFunctorContext "OnCreate"
     IF(HasPassive('DraconicAncestry_Amethyst') or …_Force or …_Cobalt):
         ApplyStatus(ELEMENTALAFFINITY_FORCE_EXTRA_DAMAGE_TECHNICAL,100,-1)
   ```

   Three ancestries map to **Force**: **Amethyst, Force, Cobalt**. `Draconic Bloodline Expanded`
   (load 408) **owns** the selectable ancestry list `c69c33a2-671c-46e1-a92c-656fe64ed447` with
   **37 entries**, beating base game's 10 — so all three are genuinely pickable. **[database]** The
   full ancestry → type map is now recorded in `data/classes/sorcerer.md`.

   The three tie on affinity and differ only in the free spell, so the free spell decides it:
   Amethyst → `Projectile_MagicMissile`, Force → `Shout_Shield_Sorcerer`, Cobalt →
   `Zone_Thunderwave`. **Amethyst wins twice over** — the sheet wanted Magic Missile as a Sorcerer 1
   pick anyway, so it frees a spell known, *and* Magic Missile is Force, which makes it the second
   engine below.

4. **Every beam carries two saving throws, from character 5.**

   ```
   FrightfulBlast  [Listo Tweaks and Patches, load 741, using AgonizingBlast]
     Conditions "IsEldritchBlastAlike() and HasDamageEffectFlag(DamageFlags.Hit)"  <- AgonizingBlast
     StatsFunctorContext "OnAttack"                                               <- AgonizingBlast
     StatsFunctors "IF(not SavingThrow(Ability.Wisdom,(SourceSpellDC()-2),
                       AdvantageOnFrightened(),DisadvantageOnFrightened())):ApplyStatus(FRIGHTENED,100,2)"
   SickeningBlast  [same source and layer]
     StatsFunctors "IF(not SavingThrow(Ability.Constitution,(SourceSpellDC()-2),
                       AdvantageOnPoisoned())):ApplyStatus(POISONED,100,2)"
   FRIGHTENED  Boosts "Disadvantage(AllAbilities);Disadvantage(AttackRoll);ActionResourceBlock(Movement)"
   POISONED    Boosts "Disadvantage(AttackRoll);Disadvantage(AllAbilities)"
   ```

   **Per hit, not per critical.** No cooldown and no once-per-turn clamp, and that is deliberate:
   `docs/5-ChangeLog.md:720` nerfs the DC by 2 explicitly *because* the rider "can be fired off 3+
   times every turn and force multiple saving throws per hit". Different `StackId`s and different
   abilities, so both land off the same beam.

   **And the pair debuffs both abilities.** This is the correction that made Sickening the right
   third pick: **[database: `Mesmerist`, load 431]**

   ```
   MESMERIST_HYPNOTIC_STARE  Boosts "RollBonus(SavingThrow,-1,Intelligence);
                                     RollBonus(SavingThrow,-1,Wisdom);RollBonus(SavingThrow,-1,Charisma)"   x3
   BOLDSTARE_SAPPEDMAGIC     Boosts "RollBonus(SavingThrow,-1,Constitution);SpellSaveDC(-1)"                x3
   ```

   On the Stare target at Mesmerist 11+, Wisdom is at **−3** from the base Stare and Constitution at
   **−3** from Sapped Magic. Both riders therefore land at effective DC **22** against a nominal 21:

   | Rider | Save | DC | target penalty | effective |
   |---|---|---|---|---|
   | Frightful Blast | Wisdom | 21 − 2 = 19 | −3 base Stare | **22** |
   | Sickening Blast | Constitution | 21 − 2 = 19 | −3 Sapped Magic | **22** |

   Against a typical Act III +5 save that is a **75%** failure rate per beam. Eight beams on one
   target is `1 − 0.25⁸` — the boss is Frightened *and* Poisoned essentially every round. Eight
   beams spread over eight targets is **~6 debilitated enemies a round**, each for two turns.

   Frightened's `ActionResourceBlock(Movement)` is the load-bearing half for a two-body party with
   no third character: a Frightened enemy cannot close, and a Poisoned one that does swings at
   disadvantage.

5. **The second engine is Magic Missile, and Amethyst hands it over free.** **[database]**

   ```
   Projectile_MagicMissile     Level "1"  SpellProperties "DealDamage(1d4+1,Force,Magical)"
                               AmountOfTargets "3"   TargetRadius "18"
   Projectile_MagicMissile_6                         AmountOfTargets "8"
   ```

   **Each dart is its own damage instance and its own target, and the type is Force** — so every
   dart takes Elemental Affinity's `+Cha`, and every dart into the cursed target takes Hexblade's
   Curse's `+PB`. It is not a cantrip, so Potent Robe does not reach it.

   At a 6th-level slot in Act III: **8 darts × (3.5 + 7) = 84 spread across up to 8 targets, with
   no attack roll and no saving throw** — or **8 × 16.5 = 132** if every dart goes into the cursed
   boss. That is this sheet's answer to a high-AC target, heavy cover, or anything that would make
   eight attack rolls unreliable, and v1 had no such button at all.

---

## Why Hexblade, and why the patron slot came free

Great Old One's Mortal Reminder is `ClarifiedMortality` — `Conditions "IsCritical()"` →
`CreateExplosion(Projectile_ClarifiedMortality)`, a 3 m Wisdom save applying
`CLARIFIED_MORTALITY`, which is **`using FRIGHTENED` with `StackId FRIGHTENED`**. **[database: Base
Game: Shared.pak, load 4]** Same stack as Frightful Blast, so it can never stack with it, and it
needs a critical this sheet no longer fishes for. The patron slot was therefore free, and all six
installed patrons were re-costed at Warlock 1-2 (level 6 features are out of reach):

| Patron | Level 1, as installed | Verdict |
|---|---|---|
| **Hexblade** GustavX 3 | `HexWarrior` = `Proficiency(MediumArmor);Proficiency(Shields);Proficiency(MartialWeapons);UnlockSpell(Shout_Hexblade_Bind)`. `HexbladesCurse` = `DamageBonus(ProficiencyBonus)` + `ReduceCriticalAttackThreshold(1)` vs the cursed target | **take** — +48 raw a round, −1 threshold, and shields from character 1 |
| Archfey Shared 4 | `Shout_FeyPresence_Container` → `Shout_FeyPresence_Frightened` = `ApplyStatus(FRIGHTENED,100,2)`, `ActionPoint:1`, `OncePerShortRest` | redundant — the same status this sheet applies per beam, here for a full Action once a short rest |
| Fiend Shared 4 | `DarkOnesBlessing`, `Conditions "HasHPLessThan(1) and Enemy() and Character()"` → `TemporaryHP(CharismaModifier+ClassLevel(Warlock))` | 9 temp HP a kill at Charisma 24 / Warlock 2. Real, small, and this body is already `Resistance(All)` behind Lone Wolf's halving |
| Great Old One Shared 4 | `ClarifiedMortality`, above | **drop** — same `StackId`, and crit-gated |
| Psyker Otherworldly Archetypes 343 | `WarpMagic`, `Conditions "…IsCantrip() and (SpellId('Projectile_EldritchBlast') or …)"` → `ApplyStatus(WARP,…)` **and `ApplyStatus(SELF,PERILSOFWARP,100,1)`**; `PERILSOFWARP` = `IncreaseMaxHP(-LevelMapValue(Perils))`, `StackType Additive` | **actively harmful** — self max-HP reduction, additive, **per beam**. Eight stacks a round. `WARP` has no boosts of its own; it feeds `SoulRupture` at Warlock 6, unreachable |
| The Celestial The Celestial 415 | `LHB_TheCelestial_HealingLight` — no `Boosts`, no `StatsFunctors`, no `Conditions` at load 415. Grants `Target_Light;Target_SacredFlame` | nothing — Coldsnap already carries both |

The curse itself: **[database: Base Game: GustavX.pak, load 3]**

```
Target_HexbladesCurse  UseCosts "BonusActionPoint:1"   TargetRadius "18"
                       SpellProperties "ApplyStatus(HEXBLADES_CURSE,100,10)"
                       Cooldown "OncePerShortRest"   SpellFlags "IsHarmful"
```

**Bonus action, 18 m, ten turns, once per short rest, and not concentration.** This body has two
Bonus Actions and only the Hypnotic Stare to spend them on, so the curse is free. It goes on the
same creature as the Stare — Painful Stare, Sundering's −2 AC, Sapped Magic's −3 Constitution — one
designated victim carrying every debuff on the sheet.

`HexWarrior` also **retires v1's largest unverified claim**: v1 spent a whole section inferring that
Astral Half-Elf inherits shield proficiency from vanilla Half-Elf, with Shield Master hanging off
the inference. Hexblade grants `Proficiency(Shields)` outright, at character 1. Do not equip the
medium armour — Draconic Resilience is conditioned on wearing none.

---

## Why Eyebiter and not Trickster

Unchanged from v1, and the case got stronger. The Eyebiter wins on three axes the pair needs.

| | Eyebiter | Trickster |
|---|---|---|
| Durability | **Resistance boon: physical <10, all damage 10–19, Invulnerable at 20** | Fortifying Tricks: +3 AC / +3 flat DR at this depth |
| The pair's save axis | **Sapped Magic** puts the Stare's penalty on **Constitution** — Coldsnap's Glaring Frost *and* this sheet's Sickening Blast | nothing touches Constitution |
| Cold-immune enemies | **Blinding**: Constitution save every turn or Blinded, at-will, no Cold involved | — |
| Act III undead/constructs | **Psychic Inception at 7** — the Stare works at 100% on mind-immune creatures | blocked, then 50% from Mesmerist 6 |
| What it gives up | outward condition-stripping; Haste on the partner via Compel Alacrity | — |

```
EyebiterBoonResistance  Conditions "StatusId('MESMERIST_HYPNOTIC_STARE_OWNER')"
  ClassLevel < 10   EYEBITERBOONPHYSICALRESISTANCE  Resistance(Slashing/Piercing/Bludgeoning)
  ClassLevel 10-19  EYEBITERBOONALLRESISTANCE       Boosts "Resistance(All,Resistant)"
  ClassLevel 20     EYEBITERBOONIMMUNITY            Boosts "Invulnerable()"
```

The condition is a Stare being up, and the Stare is free, permanent, bonus-action and needs no
concentration, so in practice the resistance is always on. Losing Compel Alacrity costs
Haste-on-the-partner; **Sorcerer 2's Twinned metamagic buys it back** for one pick.

**Mesmerist 12, not 13.** Mesmerist 13's only grant is permanent See Invisibility plus a spell
known, and dropping it is what pays for Warlock 2 — see *Chassis*.

---

## Chassis

| Piece | Levels | What it is bought for |
|---|---|---|
| **Mesmerist 12 (Eyebiter)** | 12 | Hypnotic Stare, three Bold Stares, two Boons, Painful Stare `3d10 ×3`, Psychic Inception, Towering Ego, Battlemind Link, Sapped Magic |
| **Sorcerer 6 (Draconic — Amethyst)** | 6 | **Elemental Affinity (Force)** = `+Cha` per beam. Draconic Resilience = AC 13 unarmoured + 6 HP. Font of Magic, Twinned, Fireball, Haste, **free Magic Missile** |
| **Warlock 2 (Hexblade)** | 2 | **Hexblade's Curse**, shield proficiency, Eldritch Blast, **two free invocations**, two short-rest pact slots |

**Feat count: 6.** `class_feat_levels` gives Mesmerist, Sorcerer and Warlock the identical
per-class-level cadence **3 / 6 / 9 / 12 / 13 / 15 / 18** **[database]** — so Mesmerist 12 → 4,
Sorcerer 6 → 2, Warlock 2 → 0.

### The level-split argument, since it is the whole sheet

| Split | Feats | Free invocations | Total picks |
|---|---|---|---|
| v1: Mesmerist 13 / Sorc 6 / Warlock 1 | 7, two of them spent on Eldritch Adept | 0 | 7 |
| **v2: Mesmerist 12 / Sorc 6 / Warlock 2** | **6** | **2** | **8** |
| Mesmerist 11 / Sorc 6 / Warlock 3 | 6 | 2 | 8, and −16.5 raw a round |
| Mesmerist 12 / Sorc 3 / Warlock 5 | 6 | 3 | 9, and no Twinned Haste, no Fireball, no Elemental Affinity |

**Warlock 2 costs Mesmerist 13 and buys two invocations free.** Every gate that matters survives:

| Feature | Gate | At Mesmerist 12 |
|---|---|---|
| Painful Stare `3d10` | `MorePainfulStare` `Level12: 3d10` | yes |
| Painful Stare ×3 a turn | `PAINFULSTARE_3DPR`, Mesmerist ≥10 | yes |
| Resistance to all damage | `EyebiterBoonResistance`, `ClassLevel 10-19` | yes |
| Sapped Magic ×3 | Bold Stare tier 3, Mesmerist 11 | yes |
| Battlemind Link / Manifold Stare | Mesmerist 9 / 8 | yes |
| Multiclass caster level | `floor(12 × 0.5) + 6` | **12 — unchanged.** 6th-level slots, upcast Doom −6 |

`MulticlassSpellcasterModifier` is **0.5** for Mesmerist, **1.0** for Sorcerer and **null** for
Warlock **[database]** — Pact Magic is a separate pool, which is exactly why Warlock levels past 2
are so expensive here. Warlock 5 would need three levels out of Sorcerer (losing Twinned Haste,
the pair's only Haste, plus Fireball) or out of Mesmerist (losing `Resistance(All)`, the Durability
rung, and the Sapped Magic that makes Sickening Blast land) — to save **one** feat.

**Mesmerist must be the level 1 class in the final build.** Saving-throw proficiencies come only
from there.

### Invocations — three, and the routing is forced

| Invocation | In Essential Feats `ae25190d` | In Warlock L2 / Mizora `333fb1b0` |
|---|---|---|
| **Agonizing Blast** | **yes** | yes |
| **Frightful Blast** | no | yes, via Mizora `MergedInto` |
| **Sickening Blast** | no | yes, via Mizora `MergedInto` |

`ae25190d` has **no merge contributors** and holds eight entries. **[database]** So Frightful and
Sickening can only come from a real invocation slot; Agonizing is the one of the three reachable
through the half-feat. Hence:

- **Warlock 2** → **Frightful Blast + Sickening Blast**
- **`SYR_EldritchAdept`** → **Agonizing Blast**, and it carries
  `SelectAbilities(6d64a5f2…,1,1)` whose ability list is `Intelligence, Wisdom, Charisma` — **a free
  ability point the other routing does not get.**

Two distinct Eldritch Adept feats coexist, different UUIDs, neither overriding the other, both
`CanBeTakenMultipleTimes` and neither carrying `Requirements`: `SYR_EldritchAdept` (Essential Feats,
load 256) and `EldritchAdept` (Mizoras Rewards, load 416). **[database]** This resolves the
`(unverified)` question v1 carried at `data/classes/warlock.md:541`.

**Repelling Blast and Grasp of Hadar are not options.** The load-order-winning
`Projectile_EldritchBlast` (Listo Master Spells Patch, load 755) gates the push on
`HasStatus('REPELLING_BLAST_TRIGGER',context.Source)`, and **no record anywhere in the install
defines that status** — the single DB-wide reference is that one spell line. The `RepellingBlast`
passive applies `PASSIVE_REPELLING_BLAST` instead, a base-game status whose `Boosts` is `None`, and
`GraspOfHadar` is `using RepellingBlast` with no boosts of its own, so it inherits the dead chain.
`Properties = IsToggled;ToggledDefaultOn` means it still looks live in the hotbar. **Confirmed
non-functional in game.** It would be a one-line fix if the pack repairs it.

**Eldritch Mind is not an option either.** It is `using WarCaster_Bonuses` and its only boost is the
inherited `Advantage(Concentration)` **[Mizoras Rewards, load 416]** — a strict subset of the War
Caster feat, which also carries the reaction passive and the ability picker.

---

## Race — Astral Half-Elf, on narrowed grounds

`Astral Half-Elves` (`9676`), enabled. **[database: load 440]**

```
AstralHalfElf  Level 1   PassivesAdded "Astral_Intuition;AstralElfHE_StarlightStepChargeGain"
                         Boosts "ActionResource(StarlightStepCharges_HE,1,0)"
                         Selectors "AddSpells(…);SelectSpells(…,1,0,AstralFire,,,AlwaysPrepared)"
               Levels 5 / 9 / 13 / 17   PassivesAdded "AstralElfHE_StarlightStepChargeGain"
Astral_Intuition   Boosts "Advantage(Ability, Intelligence)"
Target_MistyStep_AstralHalfElf_StarlightStep
                   UseCosts "BonusActionPoint:1;StarlightStepCharges_HE:1"   radius 9 m, no slot
Races.lsx  AstralHalfElf  ParentGuid "45f4ac10-3c89-4fb2-b37d-f973bb9110c0"   <- vanilla Half-Elf
```

**All 56 selectable races were re-costed once Hexblade made shields free**, and the finding is that
**no race moves a scored axis on this chassis**: `derive_saves` returns **4** with or without a
hypothetical Halfling-Luck or Gnome-Cunning booster, and `derive_skills` reads flat modifiers only,
so advantage is unpriced. The pick is therefore decided on unpriced utility.

What is worth nothing here, and must be discounted rather than listed: any ability-score bonus
(Listo grants none — see *Stats*); shield, armour and weapon proficiency (Hexblade covers shields,
the body wears no armour by design and swings nothing at Strength 8); Darkvision (Penetrating Stare
at Mesmerist 9 grants blindness immunity and sight through magical darkness); Perception and
Investigation proficiency (Coldsnap holds both and the Skills axis takes the better half).

**What Astral Half-Elf is bought for, in order:**

1. **Five slot-free bonus-action 9 m teleports per long rest** — one charge at each of levels 1, 5,
   9, 13, 17. This is the highest-frequency unpriced utility on offer and it is exactly what the
   6 m Battlemind leash and Coldsnap's `WaterFrozen` carpet demand: repositioning that does not
   spend the Action the beam routine needs.
2. **`Advantage(Ability, Intelligence)`**, permanent, from level 1. **Narrowed**: this is no longer
   bought for the Mirror of Loss, because the character-5 respec plan already routes Religion
   Expertise through Withers. It is bought for routine Arcana, History, Investigation and Nature.
3. **Astral Fire → Light**, free, which frees a cantrip pick.
4. **Fey Ancestry**, inherited — advantage on saves against Charmed. Real cover, because Towering
   Ego switches off once a harmful mind-affecting effect has already landed.

**The runner-up, and why my own Battlemind finding killed it.** **Strongheart Halfling** was the
only candidate that touched the engine: `Halfling_Lucky` = `Reroll(Attack,1,true);
Reroll(SkillCheck,1,true);Reroll(RawAbility,1,true);Reroll(SavingThrow,1,true)` **[Base Game:
Shared.pak, load 4]**, plus `Halfling_StoutResilience` = `Resistance(Poison,Resistant);Tag(POISONED_ADV)`.
Eight attack rolls a round looks like a lot of reroll surface — but `BATTLEMIND_BONUS` grants
unconditional `Advantage(AttackRoll)` from character 12, and with advantage the *kept* die is a 1
only when both dice are: **0.25% instead of 5%.** The attack clause is nearly dead on this chassis
specifically. Its save and skill clauses are real and are the reason it places second.

| Also considered | The record | Verdict |
|---|---|---|
| **Shadar-kai** load 447 | `ShadarKai_NecroticResistance`; `Target_BlessingRavenQueen` (`BonusActionPoint:1`, `OncePerRest`, 18 m, applies one turn of resistance to thirteen damage types); `Target_ShadarKaiRaven` (`BonusActionPoint:1`, `OncePerRest`, summons `RavenCompanion_ShadarKai` until long rest) | third body plus a panic teleport, and the duo has no third body — but `LevelOverride = -1` on the raven template is `(unverified)`, so its Act III survivability is unproven |
| **Rock Gnome** Shared 4 | `Gnome_Cunning` = `Advantage(SavingThrow, Intelligence);Advantage(SavingThrow, Wisdom);Advantage(SavingThrow, Charisma)` | strongest pure-save race, and it covers the two abilities Towering Ego only flat-boosts. 7.5 m movement on an ice field is the cost |
| **Fey Eladrin** load 442 | `Target_FeyStep_Winter`, bonus action, no slot, `not SavingThrow(Ability.Wisdom,SourceSpellDC())` → `FEARED` 2 turns, four charges | redundant now — this sheet Frightens per beam |

**Actively excluded.** **Drow** and **Duergar** carry `SunlightSensitivity` (effective layer:
`Better (SO much better) Dwarves`, load 446), which imposes attack-roll disadvantage — aimed
straight at an eight-roll engine — and their Darkness casts remove the illumination Coldsnap's
Callous Glow Ring needs. Every **playable undead** presentation (`Ghouls_Undead_Passive`, Playable
Undead Race, load 437) carries **Radiant vulnerability**, which is a poor idea beside a partner
whose retaliation lines deal Radiant.

**No ability scores from any race** — see *Stats*.

---

## Stats

Races in Listo grant **no ability score bonuses**; the +2/+1 is assigned freely at creation
**[data]**, so nothing in this table depends on the race pick.

| | Buy | Racial | Lone Wolf | Feats | Mirror | **Final** | Mod |
|---|---|---|---|---|---|---|---|
| STR | 8 | — | — | — | — | **8** | −1 |
| DEX | 14 | — | — | — | — | **14** | +2 |
| CON | 14 | **+1** | **+4** | +1 Durable · +1 Tough | **+2** | **23** | **+6** |
| INT | 10 | — | — | — | — | **10** | +0 |
| WIS | 10 | — | — | — | — | **10** | +0 |
| CHA | 15 | +2 | **+4** | +1 Eldritch Adept · +1 War Caster `(picker)` | **+1** | **24** | **+7** |

27-point buy: `0 + 7 + 7 + 2 + 2 + 9`. Racial assignment: **+2 Charisma, +1 Constitution.**

### Two picker points, and what the second one actually buys

v1 had one ability-picker feat and recorded the consequence at its line 290: *"Constitution 22 is
off the table: reaching it needed the Mirror's +2 spare, which only happens with two picker-based
Charisma points, and there is one."* **There are now two** — `SYR_EldritchAdept` and War Caster use
the identical ability list `Intelligence, Wisdom, Charisma` (`6d64a5f2` and `771b7e52`, both
`SelectAbilities(…,1,1)`) **[database]**.

**Picker reads base scores:**

| | v1, one picker point | v2, two picker points |
|---|---|---|
| CHA base | 17 `+1 WC` = 18 | 17 `+1 EA` `+1 WC` = **19** |
| + Lone Wolf +4 | 22 (+6) | 23 (+6) — *no gain here* |
| Mirror, optional +1 CHA | dead at the cap | 23 → **24** (+7) |
| Mirror, +2 | spent: CHA 22 → 24 | **free → CON 21 → 23** (+6) |
| Hag's Hair +1, pair-shared | CON 21 → 22 (+6) | CON 23 → **24** (+7) |
| **Finish** | CHA 24 / CON 22 | **CHA 24 / CON 24** |

Charisma lands on 24 in both columns — 22 and 23 are the same modifier and the cap is 24 regardless.
What the second point buys is **the Mirror's `+2`, freed for Constitution**: +1 modifier without
Hag's Hair, +2 with it. That is roughly +20 to +40 max hit points before Lone Wolf's +30%, and +1 to
+2 on every Constitution and concentration save.

**Picker reads boosted scores:** both points are refused on Charisma (21 from character 1), and
INT/WIS 10 → 11 moves no modifier. Everything reverts to v1's numbers. **The swap is free upside
with no downside branch.**

`GOON_LONE_WOLF_CHARISMA_STATUS` carries `Boosts "Ability(Charisma,4);ProficiencyBonus(SavingThrow,Charisma)"`
— two arguments, no maximum — so Lone Wolf's `+4` does reach 21. **[pak]**
`references/listo-rules.md:217` records this as *"stops at 20"*; that row is wrong.

### Why the racial +1 goes to Constitution, not Dexterity

**Dexterity 15 and 14 are the same modifier.** On Constitution the point turns `14 + 4 = 18` into
`15 + 4 = 19`, which is the odd number **Durable's +1 lands on** — `19 → 20`, `+4 → +5`, at
character 8. Tough's `+1` then takes 20 → 21 with no modifier behind it; that is unavoidable with
two Constitution half-feats on one sheet, and it is the right way round, because Durable is the
earlier pick. Tough is bought for `+2` per character level and `+2` to Constitution saves regardless.

> **Hag's Hair belongs on this body, and the case is stronger than in v1.** With the Mirror's `+2`
> on Constitution the score reads 23, so Hag's Hair takes it to **24** — a modifier, not a wasted
> point. Coldsnap's Wisdom is already pinned at the Mirror cap of 24, so its `+1` would be thrown
> away there. **[pair decision]**

**Spell save DC = 8 + 6 + 7 = 21** post-Mirror; **20** pre-Mirror at Charisma 22; **19** in the
refused-picker branch through Acts I-II.

### Saves at 20

| Save | Total | Source |
|---|---|---|
| **CHA** | **+13**, advantage | Mesmerist 1 · advantage from Towering Ego at Mesmerist 10 |
| **CON** | **+15, advantage on concentration** | Lone Wolf proficiency · Constitution 23 · Tough +2 · War Caster |
| DEX | **+10** | Mesmerist 1 · Shield Master +2 while a shield is equipped |
| WIS | +7 | Towering Ego — flat +Cha, not proficiency |
| INT | +7 | Towering Ego, full Charisma from Mesmerist 10 |
| STR | **−1** | uncovered, and nothing on the sheet closes it |

`derive_saves(("dex","cha","con"), ("towering-ego","emboldening-bond"))` = **4**.

> **Mage Slayer covers the holes where they matter.** From character 20 it grants advantage on
> saving throws against **every spell** — not melee range only, as in vanilla — and reduces all
> spell damage by the proficiency bonus, `−6` a hit. **[data]** Its anti-concentration half is dead
> weight: the aura is 3 m and this body fights at 18 m.

> **Towering Ego is preventative only.** It switches off while you are already under a harmful
> mind-affecting effect, so the Wisdom and Intelligence rows are not recovery. **[data]**

---

## Feats — six

| Char | Feat | What it buys |
|---|---|---|
| **5** | **`SYR_EldritchAdept` → Agonizing Blast** | The second Charisma rider on every beam, `+1` CHA from the picker, and **the picker test itself at character 5** |
| 8 | **Durable** | `+1 CON → 20`, **full hit points on every short rest**, in-combat regeneration below 60% |
| 11 | **Tough** | **+2 Constitution saves**, +2 HP per character level (+40). Its `+1 CON` lands on 21 |
| 15 | **Shield Master** | +2 Dexterity saves, **−1 to all damage taken**, and Block as a **passive** — the Rogue Evasion effect, spending no reaction |
| **18** | **War Caster** | Second `+1` CHA picker, and advantage on concentration saves exactly when concentration starts mattering — Haste arrives at character 17 |
| 20 | **Mage Slayer** | **Advantage on saves against all spells**, all spell damage reduced by the proficiency bonus |

Feats land on Mesmerist class levels 3 / 6 / 9 / 12 and Sorcerer 3 / 6, which the ladder below puts
at characters 5 / 8 / 11 / 20 and 15 / 18.

**Shield Master no longer depends on an inference.** `HexWarrior` grants `Proficiency(Shields)` at
character 1, so v1's `(unverified)` subrace-inheritance caveat no longer gates a feat.

### Five feats v1 carried, and why they are gone

- **`Spell Sniper` and `Deadly Alacrity`.** Both were bought purely for crit threshold, and the
  threshold existed only to fire Mortal Reminder — v1's own line 83 said so. With Frightened
  arriving per hit, the crit package has no job. `SYR_Feat_DeadlyAlacrity_Passive` is
  `ReduceCriticalAttackThreshold(1)` and nothing else **[Essential Feats, load 256]**; Spell
  Sniper's extra cantrip and `SpellSniper_Empowered` first-hit damage reroll are worth about `1.3`
  a round.

  Cashing them moves the threshold from `r = 8` to `r = 6` — Dreamweaver's unconditional `−2` and
  Ring of Critfishing's `−3` survive in gear, and Hexblade's Curse adds `−1` back on the priority
  target. **Crits only double the `1d8`**: `Eyebiter_MorePainfulStare` fires
  `DealDamage(LevelMapValue(MorePainfulStare),Psychic)` from `StatsFunctors` on `OnDamage`, a
  separate instance that never doubled. The whole cost is `8 × (0.64 − 0.51) × 4.5 ≈ 4.7`, plus
  ~1.3, against an Act III raw of 301.5.
- **`Eldritch Adept → Agonizing Blast` as a bare feat.** Still taken, but as the *half*-feat
  version, which carries an ability point the Mizora version does not.
- **`Actor`.** Four Charisma Expertises and a guaranteed route past Charisma 20. Cut because the
  stat line reaches 24 in both picker branches, and because Mage Slayer and Shield Master each
  answer a structural problem the face does not.
- **`Skeleton Crew`.** Cut on an in-game observation that it does not fire reliably, not on a
  costing. If it works, it is the first feat back and Durable is what it displaces.

**The face is proficiency-only, and that is the price.** Persuasion runs `+7 mod + 6 proficiency
= +13`, against Act III checks reaching DC 25–30. Deception is fine on its own — **Consummate Liar**
adds half the Mesmerist level, so `+19` in Act III — so lean on Deception wherever the dialogue
offers both. Intimidation and Performance have no proficiency. Coldsnap is Charisma 8, so there is
no second face.

---

## The two Eyebiter Boons — Mesmerist 4 and 8

| Boon | At Mesmerist 12 | |
|---|---|---|
| **Resistance** | Resistance to **all damage** while a Stare is up | **take** |
| **Manifold Stare** | Painful Stare becomes `3d10`, **three times a turn** = 49.5 a round | **take** |
| Vital Pinpoint | Ignore resistance to all damage; ignore immunity only at Mesmerist 20 | skip — Magic Missile and the Dart cover the resistance table |
| Mirror | Marker passive only. Each Stare independently checks `HasPassive('EyebiterBoonMirror')` and applies the **inverse** to self, at the same 1/2/3 magnitude: Sundering → `AC(1)`, Sapped Magic → `RollBonus(SavingThrow,1,Constitution);SpellSaveDC(1)`, Disorientation → `RollBonus(Attack,1);CharacterWeaponDamage(1)`, Hex → `Advantage(SavingThrow, Dexterity)` **plus `RegainHitPoints(1d6)` every turn**, Restriction → double movement, Blinding/Reflection/Oscillation/Withering → `DamageReduction(All,Flat,1)` × 1/2/3. Only Sluggishness has no mirror | **live contender** — on this sheet's own three Stares it pays **+3 AC, +3 Constitution saves, +3 spell save DC and flat 1**. See below |

`MorePainfulStare` level map: `6-9: 2d8 · 10-11: 2d10 · 12-17: 3d10 · 18-19: 4d10 · 20: 4d12`.
**[database: `Mesmerist`, load 431]** At Mesmerist 12 it sits at `3d10` and stops there.
`Eyebiter_MorePainfulStare` requires the Manifold boon's `EYEBITER_NORMALPAINFULSTARE_BLOCKER` and
gates the per-turn count: `PAINFULSTARE_2DPR` below Mesmerist 10, **`PAINFULSTARE_3DPR` at
Mesmerist 10-19**.

> **Correction to v1.** Its Act II damage block authored Painful Stare as `2d10 × 2 = 22` at
> Mesmerist 10. The class-level gate is `≥10` for **three** procs, so the correct figure is
> `2d10 × 3 = 33`. This sheet uses 33.

### Mirror against Resistance — the one real contest for slot two

Mesmerist 12 opens exactly **two** boon slots, at Mesmerist 4 and 8; the third is Mesmerist 16 and
out of reach. Slot one is not a choice: `Eyebiter_MorePainfulStare`'s conditions include
`HasStatus('EYEBITER_NORMALPAINFULSTARE_BLOCKER',context.Source)`, a status only
`EyebiterBoonPainfulStare` applies, so without Manifold Stare the 49.5 a round does not fire at
all. That leaves Mirror and Resistance competing for slot two.

On this sheet's own Stares — Blinding, Sundering, Sapped Magic — Mirror pays **+3 AC** (Sundering),
**+3 Constitution saves and +3 spell save DC** (Sapped Magic), and **flat 1** damage reduction
(Blinding). No re-picking required. Durability, run through `derive_ehp` on the authored pools:

| Slot two | Act II | Act III |
|---|---|---|
| **Resistance** — `Resistance(All,Resistant)`, AC 20 | ratio 3.922, **rung 5** | ratio 4.331, **rung 5** |
| **Mirror** — AC 23, flat 2 total | ratio 3.376, **rung 5** | ratio 3.274, **rung 5** |

**Neither moves the rung**, so Durability cannot decide it. Resistance is the better pure
mitigation — a proportional halving does not decay as hits grow from `(9.6, 28.8)` to
`(13.3, 40.0)`, whereas AC and flat reduction do. Mirror buys three things Resistance cannot:

- **+3 spell save DC**, against an engine that rolls **two saving throws on every one of eight
  beams** — Frightful Blast at `SourceSpellDC()-2` and Sickening Blast at `SourceSpellDC()`. The
  `-2` on Frightful is exactly cancelled. This is the largest single DC swing available to the body.
- **+3 Constitution saves**, which is concentration on Doom and on Haste.
- **+3 AC**, which `derive_ehp` prices as `p_hit` 0.50 → 0.35.

**Mirror's ceiling is set by which Stares you pick, and the general damage reduction is
`StackType = Additive` with fixed magnitudes** — Blinding 1, Reflection 2, Oscillation 3,
Withering 3 — while the Sundering, Sapped Magic and Disorientation mirrors carry their **own**
`StackId`s and therefore add on top rather than compete. Re-picking the Stares changes the answer:

| Stares, with Mirror in slot two | AC | flat | Act III ratio | rung | DC gain |
|---|---|---|---|---|---|
| Blinding · Sundering · Sapped Magic *(this sheet)* | 23 | 2 | 3.274 | 5 | +3 |
| Sundering · Reflection · Sapped Magic | 23 | 3 | 3.483 | 5 | +3 |
| **Sundering · Reflection · Withering** | 23 | **6** | **4.403** | 5 | — |
| Disorientation · Sluggishness · Sapped Magic | 20 | 1 | 2.166 | **4** | +3 |
| *Resistance instead of Mirror* | *20* | *1* | *4.331* | *5* | *—* |

So Mirror **can** beat Resistance outright — 4.403 against 4.331 — but only on
Sundering · Reflection · Withering, which abandons both of this body's pair assets: Blinding's
at-will Constitution-save Blind, and Sapped Magic's −3 to the Constitution save Coldsnap's Glaring
Frost tests. It gains Withering's `Interrupt_BoldStare_WitheringCounterspell` in exchange.

Two Stares that look attractive for Mirror are not:

- **Disorientation.** Its mirror is `RollBonus(Attack,1);CharacterWeaponDamage(1)`, which the mod's
  own article renders as "a bonus to your attack and damage rolls" — with no mention of weapons.
  That description is accurate for the weapon-carrying Mesmerist the class ships for. Neither half
  reaches *this* body, and the attack half is the surer of the two:

  **The attack half is worth `0.0`.** `RollBonus(Attack,…)` *is* the umbrella predicate — 428 of 459
  uses in the install are ungated and only 16 are weapon-gated, and `KIRA_Test_Wand_Passive`
  **[load 205]** gates it positively on `IF(IsSpell() and SpellDamageTypeIs(DamageType.Fire))`, so
  it certainly reaches a ranged spell attack. It simply has nothing left to buy. Act III spell
  attack is `PB 6 + Charisma 7 + 10 from gear = +23`, and every beam already rolls with Advantage
  from Battlemind Link, so `p_hit` against AC 25 is **0.997**. Three more is **`+0.0` raw a round
  across eight beams**. Accuracy on this body is saturated; only Spellmight's `−5` ever makes it
  matter.

  **The damage half is `CharacterWeaponDamage`, which needs a weapon attack.** Of 345 records using
  it, **91 gate it behind a positive `IsWeaponAttack` predicate and none behind `not
  IsWeaponAttack()`**; the single cantrip-gated use in the whole install is `EmpoweredCantrips`
  **[Eldritch Knight Plus Base, load 380]**, and that clause is
  `IF(IsCantrip() and SpellId('Target_BoomingBlade_ClassSpell'))` — Booming Blade, the one cantrip
  that swings a weapon. The same record's other branch is
  `IF(IsCantrip() and not IsWeaponAttack()):DamageBonus(…)`, the same author drawing the same line.
  Eldritch Blast is `Attack(AttackType.RangedSpellAttack)` and never a weapon attack, so this is
  `0` too. **Confirmed in game:** the Mirror off Disorientation adds to Eldritch Blast's attack roll
  and **not** to its damage. So the split is settled — `RollBonus(Attack)` reaches a spell attack,
  `CharacterWeaponDamage` does not, and this Stare's mirror is worth nothing to this body on either
  half.
- **Sluggishness.** It has **no mirror rider at all** — `MES_SLOW` removes a
  `BOLDSTARE_SLUGGISHNESS_BUFF` that **no record in the install defines**, so that branch is dead.
  Its self-Haste is separately real; see the Stare table below.

**This sheet keeps Resistance**, on two grounds. Sapped Magic arrives at **character 19**, so
Mirror's DC half is live for two levels of twenty; and the one Stare set that beats Resistance
costs the Blind engine. If the run will spend real time at 19–20, or the Blind is redundant beside
Coldsnap's Glaring Frost, Mirror on Sundering · Reflection · Withering is the better pick and the
swap costs a respec. Recorded as a lever, not a default.

> **Both boons cannot be had.** Taking Resistance *and* Mirror means dropping Manifold Stare, which
> is not flavour: `Eyebiter_PainfulStare` then applies `PAINFULSTAREDAMAGE_12` = `DealDamage(3d6,
> Psychic,Magical)` = **10.5 once per turn** behind `PAINFULSTAREIMMUNE`, against Manifold's
> **49.5**. That is **−39 st_raw a round** in Act III and −22.5 in Act II — no rung moves, both
> stay 5, but it is the worst trade on the sheet.


---

## The three Bold Stares — Mesmerist 3, 7 and 11

| Pick | Tier | At 3 Stare stacks |
|---|---|---|
| **Blinding** | 1 | `OnApplyRoll "not SavingThrow(Ability.Constitution, SourceSpellDC())"`, `TickType "StartTurn"` — a Constitution save every turn or Blinded, at will |
| **Sundering** | 1 | `BOLDSTARE_SUNDERING` = `AC(-1)`, scaled ×3 → **−3 AC** |
| **Sapped Magic** | 3 | `BOLDSTARE_SAPPEDMAGIC` = `RollBonus(SavingThrow,-1,Constitution);SpellSaveDC(-1)`, scaled ×3 → **−3 each** |
| Disorientation | 1 | `BOLDSTARE_DISORIENTATION` = `RollBonus(Attack,-1);DamageBonus(-1)`, scaled ×3 → **−3 to hit and −3 damage**. Not taken, but it is the one whose mirror buffs *weapon* damage, which this body does not use |
| Sluggishness | — | `OnApplyRoll "not SavingThrow(Ability.Wisdom, SourceSpellDC())"`, `TickType "StartTurn"` → `ApplyStatus(MES_SLOW)` **and `ApplyStatus(SELF, MAG_CELESTIAL_HASTE_MESMER)`**. Biting Gaze or Masterful Gaze only — it is **not** in the Mesmerist 3 list |

**Sluggishness grants full Haste, every turn, with no Lethargy — and it is the best Biting Gaze
pick on the sheet.** `MAG_CELESTIAL_HASTE_MESMER` carries `using MAG_CELESTIAL_HASTE`, and the
correctly-merged chain is:

```
Boosts           = ActionResource(Movement,9,0);AC(2);ActionResource(ActionPoint,1,0);Advantage(SavingThrow, Dexterity)
OnRemoveFunctors = RemoveStatus(HASTE_ATTACK)          <- no HASTE_LETHARGY
DisplayName      = "Celestial Haste"
StackId          = HASTE   StackPriority 10
```

**Confirmed in game: three Actions, one more than the baseline two.** `ActionResource(ActionPoint,1,0)`
is the extra Action, and for this body an Action is one Eldritch Blast — four beams from character 17.

> **Correction, and the resolution bug behind it.** An earlier pass reported Celestial Haste as
> carrying "no Boosts at all", i.e. the bare `HASTE_ATTACK` token. That was wrong.
> `MAG_CELESTIAL_HASTE` has **two** rows: `Public/GustavDev/…/Status_BOOST.txt` with `using "HASTE"`
> — the real parent, which is where the Boosts come from — and `Public/Honour/…/Status_BOOST.txt`
> with `using "MAG_CELESTIAL_HASTE"`, a **patch layer naming itself**. Resolving by taking the last
> row's `using` sees the self-reference, skips inheritance, and loses the entire boost package.
> `AGENTS.md` states the rule: a definition that uses its own name is a patch layer, to be merged
> over the previous definition of that name — the foreign `using` on the *earlier* row is still the
> parent. **[database: Base Game: Gustav.pak, load 2]**

The Gustav layer is what makes it "Celestial": it sets `data "OnRemoveFunctors" ""`, blanking
`HASTE`'s `ApplyStatus(HASTE_LETHARGY,100,1)`. The tooltip still reads "When the condition ends,
the creature becomes Lethargic" because the Description handle is inherited boilerplate from the
shared Haste text — **the functors do not apply Lethargy**. Worth one in-game confirmation.

**The gate is effectively free.** `BOLDSTARE_SLUGGISHNESS` rolls
`not SavingThrow(Ability.Wisdom, SourceSpellDC())` on apply and again every `StartTurn`, and the
**base Stare already applies `RollBonus(SavingThrow,-1,Wisdom)` ×3** — the Stare debuffs the exact
save Sluggishness tests. Against an Act III spell save DC around 27, a target with a +6 Wisdom save
sits at +3 and needs a 24: it fails **every turn**.

| Effect of the third Action | Act II | Act III |
|---|---|---|
| `st_raw` | 162 → **226** | 301.5 → **428** (456 with Phalar Aluve) |
| Single-target rung | 5 → 5 | 5 → 5 |
| Durability, AC 20 → 22 | ratio 3.922 → **4.902** | 4.331 → **5.414** |

No rung moves — Single-target and Durability are both saturated — but this is **+64 to +126 raw a
round plus two AC, Advantage on Dexterity saves and doubled movement**, and the movement half
directly answers the 6 m Battlemind leash that the boots row exists to manage.

**It also frees the trinket.** The Hourglass of Distorted Perception is
`JWL_DiscordantInstruments_Hourglass` → `UnlockSpell(JWL_Shout_Haste_Trinket)` →
`ApplyStatus(HASTE,100,3)` **[Discordant Instruments, load 221]**. That is plain `HASTE`: same
`StackId HASTE` at the same `StackPriority 10`, so it can **never stack** with Celestial Haste, and
it carries the Lethargy that Celestial Haste drops. A once-per-short-rest three-turn Haste is
strictly worse than a free one every turn. Spend the Act II and Act III trinket slot elsewhere.

The one real cost: Sluggishness is the single Stare with **no Mirror rider** — `MES_SLOW` removes a
`BOLDSTARE_SLUGGISHNESS_BUFF` that no record in the install defines — so it and the Mirror boon pull
against each other. With Blinding · Sluggishness · Sapped Magic, Mirror pays only flat 1 plus the
Sapped Magic buff, which further favours keeping Resistance in slot two.

Six statuses in the install touch `HASTE_ATTACK`; `MAG_CELESTIAL_HASTE` is reachable outside the
class from **The Victory** longbow (`Shout_MAG_Victory_Longbow_Haste`, displayed "Celestial Haste",
Action, 5 turns), the heel-click boots (`Shout_MOD_Vax_Haste`, **Bonus Action**, 10 turns
**[Spells of Exandria, load 254]**), `Shout_MOD_TashaHaste` **[load 250]**,
`PsiSentry_Health50Buff` under 51% HP **[Psychic Armory, load 432]**, "No Escape" gloves on Rage
**[load 209]**, and the Celestial shields from character 7 **[load 206]**.


**Why every one of these is ×3 — and the trap in reading it.** The magnitude comes from
`MultiplyEffectsByDuration`, which turns the duration argument into a multiplier, and the Stare
statuses are applied at duration 1/2/3 by Mesmerist class level (3 from Mesmerist 11). The flag
does **not** appear on most of these records directly: `BOLDSTARE_SUNDERING` and
`BOLDSTARE_SAPPEDMAGIC` both carry `using BOLDSTARE_DISORIENTATION`, and the buff side likewise
chains through `using BOLDSTARE_DISORIENTATION_BUFF`, so the flag is **inherited**. Reading
`$.StatusPropertyFlags` off the child record alone returns null and makes every one of them look
like a plain 3-turn timer. Resolve the `using` chain — `lsdb.py get` does; raw `json_extract` does
not. `StackType` is `Additive` throughout, so two mirrorable Stares contribute twice.
**[database: `Mesmerist`, load 431]**

So the base Stare is **−3 on Intelligence, Wisdom and Charisma saves** at Mesmerist 11, Sapped
Magic adds **−3 on Constitution and −3 spell save DC**, and Sundering **−3 AC**. The Constitution
line is the partnership one: it is what lowers the save Coldsnap's Glaring Frost tests.
**Sapped Magic arrives at character 19**, so that half of the synergy is late Act III.

### Mind Sanctuary — the other route to a third cast, and it is real

`Target_TAD_MindSanctuary` is an **illithid power**, and this install re-costs it. Base game gives
`Cooldown "OncePerRest"` with `AreaRadius "3"`, summoning a ground entity that carries
`TAD_MIND_SANCTUARY_AURA` **[Base Game: Shared.pak, load 4]**. **Illithid Powers Consolidated**
rewrites the cost to `ActionPoint:1;MindSanctuary_Resource:1`, a `ReplenishType "Rest"` resource —
the identical pattern it gives Black Hole (`ActionPoint:1;BlackHole_Resource:1`)
**[database: Illithid Powers Consolidated, load 726]**. Black Hole is in `scoring.py`'s power
registry and **Mind Sanctuary is not**: 25 powers are modelled and this is absent, so nothing on
the ledger prices it.

**What it actually does is narrower than the tooltip.** `TAD_MIND_SANCTUARY` carries
`ActionResourceConsumeMultiplier(ActionPoint,0,0);ActionResourceConsumeMultiplier(BonusActionPoint,0,0)`,
which reads like free actions, but the work is done by the passive it grants: `TAD_MindSanctuary`
is gated on `MindSanctuaryCheck()` and fires
`IF(OnCast and not HasActionResource('ActionPoint',…) and HasActionResource('BonusActionPoint',…))`
— it spends the **Bonus Action once the Action is gone**. And `TAD_MIND_SANCTUARY_DRAINED`
("You cannot benefit more from Mind Sanctuary this turn", `StackId TAD_MIND_SANCTUARY`,
`StackType Overwrite`, `TickType EndTurn`) caps it at **once per turn**. So the effect is: *inside
the circle, once a turn, cast an Action-cost spell with your Bonus Action.*

For this body that is exactly **one extra Eldritch Blast** — `UseCosts "ActionPoint:1"`, four beams
from character 17. Priced against the authored Act III block:

| | st_raw | rung |
|---|---|---|
| as built (two casts) | 301.5 | 5 |
| + a third cast at 31.5 a beam | **428** | 5 |
| + a third cast at 38.5 (with Phalar Aluve) | **456** | 5 |

**+126 to +154 raw a round, and no rung moves** — Single-target has been saturated since Act II.
Four real costs, and the third is the one that kills it as a default:

1. The Bonus Action is not free on turn one: `Mesmerist_Target_HypnoticStare` costs
   `BonusActionPoint:1`, and every rider on this sheet is gated on
   `HasStatus('MESMERIST_HYPNOTIC_STARE')`. From turn two the Stare persists and the Bonus Action
   is genuinely spare.
2. Placing it costs an **Action**, so the cast turn loses four beams and it breaks even on turn two.
3. **`AuraRadius "3"`.** Battlemind Link is a 6 m aura and Coldsnap's ice carpet wants this body
   mobile; a 3 m circle pins it. This is the same leash problem the boots row already flags, halved.
4. `AuraStatuses = IF(Character()):ApplyStatus(TAD_MIND_SANCTUARY,100,-1)` — **any** Character, so
   enemies standing in it get the same benefit, and the spell is flagged `IsHarmful`.

With one use per long rest it is a **boss-fight button, not a routine**: cast it on the opening turn
of a fight the pair intends to stand still for, and take roughly four extra beams a turn thereafter.
Whether it appears in this install's selectable illithid tree is **(unverified)** — that lives in
Osiris and UI data, not in the `type_*` tables — but a mod assigning it an Action cost and a
per-rest resource is only meaningful if a player can pick it.


---

## Progression ladder

**Warlock-first, with one respec at character 5.** The reason is specific: Agonizing Blast cannot
attach to Illusionary Dart — `IsEldritchBlastAlike()` excludes it — so a Mesmerist-first ladder
carries a dead engine and, if the feat comes early, a dead feat for four levels. Opening on Warlock
puts Eldritch Blast, the curse and shield proficiency on the sheet at character 1.

| Char | Take | Choose | What lands | Feat |
|---|---|---|---|---|
| 1 ★ | **Warlock 1** | <b>Patron</b> → <b>Hexblade</b> · <b>2 skills</b> · <b>2 cantrips</b> → <b>Eldritch Blast</b> + Light · <b>2 spells known</b> | <b>Hexblade's Curse</b>, <b>HexWarrior</b> (shields, medium armour, martial weapons), one pact slot. 2 beams a round at 6.5 each | — |
| 2 | Warlock 2 | <b>2 invocations</b> → <b>Agonizing Blast</b> + <b>Frightful Blast</b> | Beams to <b>11.5</b> each and a Wisdom save on every one. <b>23 a round at character 2</b> | — |
| 3 | Warlock 3 | <b>Pact Boon</b> (any — it is discarded at 5) · spell · feat | Pact slots to 2nd level | **Durable** |
| 4 | Warlock 4 | cantrip · spell | — | — |
| 5 ★ | **respec → Mesmerist 3 / Warlock 2** | <b>Mesmerist first</b> for Dex + Cha saves · <b>3 skills</b> → Persuasion, Perception, Insight · <b>2 Bard cantrips</b> → Illusionary Dart + one spare · <b>Subclass</b> → <b>Aspect of the Eyebiter</b> · <b>Bold Stare</b> → <b>Blinding</b> · <b>invocations</b> → <b>Frightful</b> + <b>Sickening</b> · feat | <b>All three riders live.</b> 4 beams at 12.5 = <b>50 a round</b>, each carrying a Wisdom save and a Constitution save. Hypnotic Stare, Doom | **`SYR_EldritchAdept` → Agonizing Blast** |
| 6 | Mesmerist 4 | <b>Eyebiter's Boon</b> → <b>Resistance</b> · cantrip · spell | Physical resistance on top of Lone Wolf's halving is <b>quarter damage</b> from every weapon in Act I | — |
| 7 | Mesmerist 5 | spell, plus <b>2 free Pathfinder spells</b> for the new tier | Stare <b>2 stacks</b>, Penetrating Stare, 2nd-level spells | — |
| 8 | Mesmerist 6 | spell · feat | <b>Painful Stare</b>, Feint −2 attack, mind-immunity 50% | **Durable** |
| 9 | Mesmerist 7 | <b>Biting Gaze</b> → <b>Sluggishness</b> · spell | The Stare target rolls a Wisdom save each turn against the Stare's own <b>−3 Wisdom</b> penalty; on a fail it is Slowed and Fixation gains <b>Celestial Haste</b> — a <b>third Action</b>, +2 AC, Advantage on Dexterity saves, doubled movement, <b>no Lethargy</b>. Confirmed in game. <b>Psychic Inception</b> | — |
| 10 | Mesmerist 8 | <b>Eyebiter's Boon 2</b> → <b>Manifold Stare</b> · spell | Painful Stare twice a turn. <b>Beams 4 → 6</b> at character 10 | — |
| 11 | Mesmerist 9 | spell · feat | <b>Battlemind Link</b> — +2 AC, +2 damage, +2 initiative and <b>Advantage on attack rolls</b> on <em>both</em> bodies, no save, no concentration, 6 m aura | **Tough** |
| 12 ★ | Mesmerist 10 | cantrip · spell | <b>Resistance → all damage</b> while a Stare is up. Towering Ego to full Charisma on Int and Wis, advantage on Charisma saves. Painful Stare <b>three times a turn</b> | — |
| 13 | Sorcerer 1 | <b>Bloodline</b> → <b>Draconic</b> · <b>Ancestry</b> → <b>Amethyst</b> (Force; <b>Magic Missile free</b>) · <b>4 cantrips</b> · <b>2 spells known</b> → <b>Shield</b> + one | Draconic Resilience — unarmoured AC 13, +1 HP per Sorcerer level | — |
| 14 | Sorcerer 2 | <b>Metamagic ×2</b> → <b>Twinned</b> + <b>Quickened</b> · spell | Font of Magic. Both metamagics land here, not at Sorcerer 3 | — |
| 15 | Sorcerer 3 | <b>3rd Metamagic</b> → <b>Careful</b> · spell · feat | Careful is what keeps Fireball off the partner | **Shield Master** |
| 16 | Sorcerer 4 | <b>5th cantrip</b> · spell | — | — |
| 17 ★ | Sorcerer 5 | <b>spell</b> → <b>Haste</b> | 3rd-level slots. <b>Twinned Haste covers both characters for one pick.</b> <b>Beams 6 → 8</b> | — |
| 18 | Sorcerer 6 | <b>spell</b> → <b>Fireball</b> · feat | <b>Elemental Affinity (Force)</b> — the third Charisma rider on every beam and every Magic Missile dart | **War Caster** |
| 19 | Mesmerist 11 | <b>Masterful Gaze</b> → <b>Sapped Magic</b> · spell | Stare <b>3 stacks</b>. −3 to the target's Constitution saves and spell save DC | — |
| 20 | Mesmerist 12 | spell · feat | Painful Stare → <b>3d10, three times a turn</b> — 49.5 a round | **Mage Slayer** |
| *III* | — | ***Mirror of Loss* → +1 CHA to 24, +2 CON to 23** | Beam damage, both save DCs and the hit-point pool move together | — |

★ = the five levels that change what the body is.

### The respec, and what it costs

**Characters 1-4 run 23 a round instead of 9**, and Frightful Blast is live from character 2 rather
than character 6. Against that: no Hypnotic Stare and no Eyebiter Resistance boon in early Act I,
and **Wisdom + Charisma saves instead of Dexterity + Charisma** until the respec — Warlock 1's
progression carries `ProficiencyBonus(SavingThrow,Wisdom);ProficiencyBonus(SavingThrow,Charisma)`
**[database]**, and multiclass save proficiencies come only from the level-1 class, so the respec is
what restores the Dexterity save.

**No scored rung moves**: the Act I checkpoint is character 8, after the respec. This is real-play
quality, bought for 100 gold. It needs Withers, who is reachable from the Dank Crypt in the
Overgrown Ruins — a character 3-4 area. If he is not available yet, stay Warlock and respec when he
is; nothing downstream changes.

The pre-respec invocation picks are deliberately greedy (Agonizing + Frightful, for damage), because
the respec re-picks them as Frightful + Sickening with Agonizing moving to the half-feat.

### Two orderings worth stating

- **Mesmerist runs 5 → 10 unbroken before any Sorcerer level.** Every Mesmerist level in that band
  beats every Sorcerer level below the sixth, which pulls Painful Stare to character 8, Manifold to
  10, Battlemind Link to 11 and Resistance-to-all-damage to 12.
- **The Sorcerer block cannot be greedy.** Sorcerer 1-5 buy an unarmoured AC, Font of Magic, three
  metamagics and Haste; **they are a down payment on Elemental Affinity**, the only level in the
  block that changes the beam. So it runs unbroken and finishes on character 18. Sapped Magic is
  what that costs — Mesmerist 11 cannot come earlier without pushing Affinity past the start of
  Act III.

---

## Concentration budget

**Doom through Acts I-II, Twinned Haste from character 17.** The engine itself needs no
concentration: Hypnotic Stare, all three Bold Stares, Painful Stare, Hexblade's Curse and
Battlemind Link are all free of it. That matters because Coldsnap's concentration is welded to
Friar's Bond for the whole run.

**Doom is a level-1 spell, and that is the finding.** **[database: `Mesmerist`, load 431]**

```
Mesmerist_Target_Doom  Level "1"   SpellFlags "IsConcentration;IsSpell;IsHarmful"
                       SpellProperties "ApplyStatus(MESMERIST_DOOM,100,SpellPowerLevel)"
MESMERIST_DOOM  Boosts "RollBonus(Attack,-1);RollBonus(SavingThrow,-1);
                        RollBonus(SkillCheck,-1);CharacterWeaponDamage(-1)"
                StatusPropertyFlags "…FreezeDuration;MultiplyEffectsByDuration;…"
```

The duration is `SpellPowerLevel` and `MultiplyEffectsByDuration` turns that into magnitude, so the
penalty is **−1 per slot level to attacks, every saving throw, every skill check and weapon
damage**. `FreezeDuration` means it does not tick down. `−3` at a 3rd-level slot, **`−6` at a 6th**,
which multiclass caster level 12 reaches.

It is available from **character 5**, and `−N` to every saving throw is a direct multiplier on
Frightful Blast, Sickening Blast *and* Coldsnap's Glaring Frost.

| Candidate | Cost | Verdict |
|---|---|---|
| **Doom, upcast** | slot, concentration | **default from character 5.** −6 to attacks, all saves, all skill checks at a 6th-level slot |
| **Twinned Haste** | 3 sorcery points, concentration | **default from character 17.** `HASTE` = `ActionResource(Movement,9,0);AC(2);ActionResource(ActionPoint,1,0);Advantage(SavingThrow,Dexterity)` — a **full Action**, on both bodies for one metamagic pick |
| **Hypnotic Pattern** | 3rd, 9 m radius, concentration | the crowd answer this duo has no other route to |
| Slow | 3rd, concentration | −2 AC and Dexterity saves, halved speed, area |
| Synesthesia | 3rd, concentration | −4 AC and Dex saves, 20% miss, cannot crit. Boss tool |

Haste and Doom compete for one slot from character 17. Haste usually wins; Doom wins where the
fight is long or the enemy's own accuracy is the threat.

---

## Area buttons

Not purely beam splitting, and one of them is free.

| Button | Level | Cost | Role |
|---|---|---|---|
| **Beam splitting** | — | at-will | the default. 8 beams over 4+ targets, each with two saving throws |
| **Magic Missile** | 1-6, **free from Amethyst** | slot | `DealDamage(1d4+1,Force,Magical)` per dart, `AmountOfTargets` 3 → **8** at 6th. **No attack roll, no saving throw.** Each dart takes Elemental Affinity `+Cha` and, on the cursed target, the curse's `+PB` — 84 spread, or 132 into one boss |
| **Fireball** | 3-6, Sorcerer 6 / char 18 | slot | the scored default: `8d6`, Dexterity save for half, upcast through 6th. Careful metamagic keeps it off the partner |
| **Hypnotic Pattern** | 3rd, 9 m | slot + concentration | area incapacitate; competes with Doom and Haste |
| `Target_ValkranaCorpseGrenade` | 2nd, 4.5 m | slot | `DealDamage(2d12,Necrotic,Magical);DealDamage(1d12,Piercing)`, **no concentration**, and a second damage type. From the Valkrana's Spellbook merge into the Mesmerist list **[load 244]** |

Fireball out-raws Magic Missile across four targets at save-for-half, so it stays the scored
default. **Magic Missile is the reliability button** — the press against high AC, heavy cover, or
anything that makes eight attack rolls a bad bet.

---

## Cantrips — twelve

Mesmerist 4 (Mesmerist 1, 1, 4, 10) + Sorcerer 5 (Sorcerer 1 ×4, +1 at Sorcerer 4) + Warlock 3
(Eldritch Blast plus one at Warlock 1, one at Warlock 4 — retained through the respec as Warlock 2's
two).

**Eldritch Blast** (the Force engine) · **Illusionary Dart** (Psychic fallback) · **Light** —
supplied free by Astral Fire, so the pick it was using is spare · **Friends**, **Minor Illusion**,
**Mage Hand**, **Bone Chill**, **Blade Ward**, **Ray of Frost**, **Fire Bolt**, **Vicious Mockery**,
and **Thunderclap** — an area Constitution save in a damage type nothing else here deals.

**The Dart's role inverted, and it is worth being explicit.** In v1 it was the engine at 18.5 a
beam; here it is the off-type press at `4.5 + 7` Potent Robe = **11.5**, or 17.5 into the cursed
target. Elemental Affinity keys off Force now, so it does not reach the Dart. **The trade runs the
right way**: Psychic resistance and immunity are common in Act III — constructs, undead — and Force
resistance is rare, so the main engine sits on the better type and the fallback on the worse one.
If a genuine off-type *engine* is ever needed, `ElementalBlast` is in the same level-2 list and
would give Cold, Fire and Acid variants at `4.5 + 7 + 7 + 6 = 24.5` — but it costs a second
Eldritch Adept feat displacing Shield Master or Mage Slayer, and Hellrime duplicates Coldsnap.

Penetrating Stare at Mesmerist 9 sees through magical darkness, so this body never needs its own
Light to fight — only the partner does.

---

## Gear — notable options by act

**Ring of Critfishing is not an Act II item**: the installed treasure tables put it in the tutorial
chest and on Popper in Act III, with no fair-route Act II copy. The table assumes no tutorial-chest
shopping, so Ring of Viciousness carries Act II and Critfishing replaces it in Act III.

**Dreamweaver needs no in-game spell test.** Its final passive carries unconditional
`ReduceCriticalAttackThreshold(2)`; only the bonus-attack functor is gated by
`AttackedWithPassiveSourceWeapon()`, so the threshold reaches Eldritch Blast. **[database: Psychic
Armory, load 432]**

**Phalar Aluve, upgraded, is a fifth Charisma rider and it beats the crit weapons by an order of
magnitude.** `MAG_HighestCaster_CantripBooster_Passive` reads
`IF(IsSpell() and IsMeleeAttack() or IsCantrip() or IsDivineSmite()):DamageBonus(max(1,SpellCastingAbilityModifier))`;
`and` binds tighter than `or`, so the bare `IsCantrip()` clause fires on its own, and all three of
this body's classes carry `SpellCastingAbility = 6`, so the modifier resolves to Charisma whichever
one is casting. `HexWarrior` covers `Proficiency(MartialWeapons)` from character 1 and a longsword
is one-handed, so the shield stays. **[database: Phalar Aluve - Legendary, load 192; Mesmerist,
load 431]**

The main hand is not free — it is what pays for crit threshold — so the comparison is marginal, not
gross. Ring of Critfishing alone is `ReduceCriticalAttackThreshold(3)` **[database: Critfisher
Ring, load 219]** and Hexblade's Curse adds another, so Dreamweaver's `-2` only moves the beams
from 16+ to 14+. Every beam already rolls with advantage, so that is 43.8% to 57.7% crit, and a
critical doubles dice rather than flat riders — 4.5 of a 38.5 beam. The marginal weapon is worth
**5.0 raw a round**; the fifth rider is worth **56.0**. Even crediting a Spellmight die to the crit
side it is 10.1 against 56.0. The same fact that retired the crit package — Frightful Blast fires
per hit, not per crit — retires the crit weapon one slot later.

The rider is **tier-gated and does not exist on the sword as found**: base `UND_SwordInStone` has
`PassivesOnEquip = None`, and only `UND_SwordInStoneV2`/`V3` carry the booster. The upgrade is a
crafting combination, `OBJ_MusicBox_PhalarAluve_v2` plus the sword, and `ItemCombos.txt` is indexed
but not extracted, so this one is read from the archive **[pak: PhalarAluveLegendary.pak,
Public/PhalarAluveLegendary/Stats/Generated/ItemCombos.txt]**. The boxes sit in
`SCL_InterrogationTable_Hidden_Chest` and `Legendary_Trident_Treasure` **[database:
type_treasure_table, load 192]**, which puts the fifth rider in **Act II**, not Act III.

It is **priced nowhere**. Act II `st_raw` would run 198 rather than 162 and Act III 357.5 rather
than 301.5, both already above the rung-5 ceiling, so the scores are unchanged and the derived
baseline stays on gear the build is committed to holding. It does not rescue the Act I branch
either: the V2 upgrade cannot exist before Act II.

| Slot | Act I | Act II | Act III |
|---|---|---|---|
| **Main hand** | **Astral Echo** for the non-disarmable upgrade path; The Spellsparkler is the raw beam-damage alternative | **Phalar Aluve V2** — a fifth Charisma rider on every beam, worth an order of magnitude more than threshold here; Voidpiercer is the crit-shape alternative at −1 | **Phalar Aluve V3** — the fifth rider, a once-per-short-rest slot restoration and a light source Callous Glow wants lit; Dreamweaver is the crit-shape alternative at −2 and non-disarmable, Rhapsody the +3 attack/damage/DC swap after three Scarlet Remittance stacks |
| **Off-hand** | **Safeguard Shield** for +1 all saves; any +1 shield is the cheap bridge. **Live from character 1 now — `HexWarrior`** | **Ketheric's Shield** for +1 spell attack/DC; Sentinel Shield is the initiative swap | **Ketheric's Shield** remains the offensive default; Viconia's Walking Fortress is the spell-defence swap |
| **Body** | **Psion's Ward** from the Armory chain; Spidersilk Armour is the concentration-defence alternative. Armour is legal here — Draconic Resilience is not live until character 13 | **Potent Robe** — Charisma per cantrip damage event and renewable Charisma temporary HP | **Robe of Archmage** — casting modifier per cantrip event, +2 spell attack/DC, +2 AC and spell resistance; Potent Robe is the renewable-temp-HP swap |
| **Head** | Diadem of the Watcher / Shadespell Circlet | Diadem of the Watcher | **Diadem of Arcane Mastery** — +2 spell attack/DC |
| **Cloak** | Cloak of Arcane Exercise (+1 spell attack) or Spell Focus (+1 DC) | **Cloak of Arcane Potency** — +1 spell attack/DC | **Cloak of Archmage** — +1 spell attack/DC and Warding Echo |
| **Gloves** | **Gloves of Dexterity** — Dexterity 14→18, +1 attacks and +2 AC | **Gloves of Dexterity**; the AC matters until the all-damage Resistance boon is established | **Gloves of Archmage** for +2 spell attacks; Spellmight adds 1d8 per beam at −5 to hit |
| **Boots** | **Disintegrating Night Walkers** or Hoarfrost Boots — `PRONE_ICE` immunity is **mandatory**, and more so now: the 6 m Battlemind aura holds this body inside Coldsnap's ice carpet | **Disintegrating Night Walkers** | **Boots of Archmage** — +1 AC and `PRONE_ICE`/grease immunity |
| **Amulet** | Amulet of Misty Step; **Psychic Spark is now a real option** — the Magic Missile side-grade on a body whose darts are Force-scaled | **Spineshudder Amulet** — two Reverberation per ranged spell attack | **Spineshudder Amulet**; Amulet of the Devout trades Reverberation for +2 Stare DC |
| **Rings** | **Ring of Protection + flex** | **Ring of Viciousness + Coruscation Ring** | **Ring of Critfishing + Coruscation**; Ring of Feywild Sparks is the +1 DC swap. Callous Glow stays on Coldsnap |
| **Trinket** | Docent or Professor Orb | **Hourglass of Distorted Perception** — three-turn Haste once per short rest, no concentration status, and it covers the whole gap to character 17 | **Book of Many Spells** — +2 spell attacks |

Spineshudder is confirmed against the installed AOE Status Fixer: each ranged spell attack gets a
placeholder that runtime Lua converts to two Reverberation. Eldritch Blast's beams are independent
attacks, so one four-beam cast reaches the five-stack Prone check **and lowers the target's
Constitution save — which now feeds Sickening Blast as well as Coldsnap's Glaring Frost.**
**[database + indexed runtime Lua]**

**Attunement check.** Five attuned items, three Legendary. The Act III default spends two Legendary
slots on **Dreamweaver and Ring of Critfishing**; Book of Many Spells and the Archmage set are Very
Rare.

**Do not use the Resonance Stone.** Steeped in Bliss doubles Psychic, which is now only the
fallback cantrip, and it grants Advantage on physical saves — directly helping enemies pass
Coldsnap's Constitution Blind, this sheet's Blinding Stare **and Sickening Blast**. It is strictly
worse for v2 than it was for v1.

---

## Scores

Ten axes, per act, on the pair-sheet rubric. Single-target, AoE and Durability are **derived** by
`scoring.py` from the damage and effective-HP blocks in `coldsnap-fixation-pair.json`, not authored.

| Axis | I | II | III | v1 |
|---|---|---|---|---|
| Single-target | **4** | **5** | **5** | 1 / 4 / 5 |
| AoE | **2** | **4** | **5** | 1 / 3 / 4 |
| Durability | 4 | 5 | 5 | 4 / 5 / 5 |
| Actions | 2 | 4 | 4 | 2 / 4 / 4 |
| Control — single | **5** | 5 | 5 | 4 / 5 / 5 |
| Control — area | **3** | **4** | **5** | 1 / 3 / 4 |
| Rescue | 1 | 1 | 2 | 1 / 1 / 2 |
| Skills | 3 | 2 | 2 | 3 / 2 / 2 |
| Saves | derived (4) | derived | derived | — |
| Endurance | 4 | 5 | 5 | 4 / 5 / 5 |

**Six cells moved, and every one of them is early.** The engine used to complete at character 17,
when Elemental Affinity arrived and Spell Sniper made the crit-fear reliable. It now completes at
character 5.

### Single-target, worked

| | Act I (char 8) | Act II (char 15) | Act III (char 20) |
|---|---|---|---|
| Build | Mesmerist 6 / Warlock 2 | Mesmerist 10 / Sorc 3 / Warlock 2 | Mesmerist 12 / Sorc 6 / Warlock 2 |
| Beams a round | 4 | 6 | 8 |
| Damage a beam, cursed | **13.5** | **21.5** | **31.5** |
| Beam total | 54 | 129 | 252 |
| Painful Stare | 7 | **33** (`2d10 ×3`) | **49.5** (`3d10 ×3`) |
| **st_raw** | **61** | **162** | **301.5** |
| Instances | 5 | 9 | 11 |
| `+ GEAR × instances` | 76 | 207 | 389.5 |
| Accuracy `mult` | ×1.19 | **×1.35** | **×1.35** |
| Ratio to par | **1.507** | **3.212** | **4.275** |
| **Rung** | **4** | **5** | **5** |

Act I takes tier 1 (`blind-engine`, ×1.19) because Battlemind Link is character 12. Acts II and III
take **tier 2** (`battlemind-link`, ×1.35) — unconditional advantage inside 6 m, no save, no
concentration, which is what `scoring.py`'s `ACCURACY` registry already assigns it. Effectively the
whole raw is a ranged spell attack roll or a Painful Stare riding one, so it collects the full tier.

**Act I sits 0.5% above the rung-4 line, and two open questions each drop it to 3.** See *Open
decisions*: if Hexblade's Curse turns out not to reach a spell beam, `st_raw` is 49 → ratio 1.269 →
**rung 3**; if the ability picker refuses Charisma, `st_raw` is 57 → 1.428 → **rung 3**. Acts II and
III hold at 5 in both branches (2.747 and 3.748 on the curse branch).

### AoE, worked

| | Act I | Act II | Act III |
|---|---:|---:|---:|
| Beam portion | 4 beams × 10.5 = 42 | 4.95 × 16.5 = 81.7 | 6.1 × 25.5 = 155.6 |
| Slot spell | none credited | Cold Snap at 4th, caster level 8 | Fireball, averaged over 4th-6th |
| **aoe_raw** | **42** | **106.9** | **220.1** |
| Instances | 4.0 | 6.35 | 8.0 |
| Ratio to par | **0.944** | **2.349** | **3.787** |
| **Rung** | **2** | **4** | **5** |

Beams are priced **uncursed** on this axis — the curse is one target and this is the spread routine.
The `mult` blends the rubric's `0.65/0.775` attack-roll-area correction with Battlemind Link's
×1.35 over the beam share only; the slot spell takes neither.

Act II is caster level **8**, not v1's 9, because Sorcerer 3 rather than 4 sits at character 15 —
so the slot table caps at 4th level and the area cast rate falls to 0.35 a round. The beams more
than cover it.

### Durability, worked

```
HP  8 + 11x4.5 (Mesmerist) + 6x3.5 (Sorcerer) + 2x4.5 (Warlock)
      + 6 (Draconic Resilience) + 40 (Tough) + 120 (Constitution 23)   = 253
AC  13 (Draconic Resilience, unarmoured) + 2 Dex + 1 Potent Robe
      + 2 Battlemind Link + 2 shield (HexWarrior)                      = 20
```

Pools **80 / 176 / 253**, ratios **1.895 / 3.922 / 4.331**, rungs **4 / 5 / 5** — unchanged from v1
despite Sorcerer arriving later, because the Mirror's `+2` on Constitution adds 20 hit points that
v1 could not buy. **Lone Wolf's +30% and its universal halving are excluded on both sides of the
ratio**, as for every chassis in the ledger.

What the rung actually rests on, in order: **Eyebiter Resistance** (physical from character 6, all
damage from character 12 — halving the hit doubles the ratio); Lone Wolf's halving underneath it;
the shield from **character 1** now rather than 5; Potent Robe's per-turn Charisma temporary HP;
Battlemind Link's +2 AC and Flanked/Surprised immunity; Constitution **+15 with advantage**, so
concentration effectively does not break; **Durable**'s full hit points on every short rest, which
matters most in Act I where the rung is weakest; **Shield Master**'s flat −1 and passive Evasion;
**Mage Slayer**'s −6 per instance of spell damage.

### The rest

**Actions 2/4/4.** Twinned Haste is live from character 17, and `HASTE` grants a full
`ActionResource(ActionPoint,1,0)` — a third Action on both bodies. The Hourglass of Distorted
Perception covers Act II.

**Control — single 5/5/5, up from 4 in Act I.** At character 8 this body already puts **two
independent saving throws on every one of four beams** — Wisdom at DC 15 and Constitution at DC 15
— plus an at-will Constitution-save Blind every turn from the Blinding Bold Stare, plus Doom. By
Act III it is a permanent, free, no-concentration `−3` to a boss's Intelligence, Wisdom, Charisma
*and* Constitution saves, its spell save DC and its AC, with two per-beam riders landing at
effective DC 22 and Doom at `−6`. Authored axes stop at 5.

**Control — area 3/4/5, up from 1/3/4.** This is the largest structural change on the sheet. v1's
area control was Mortal Reminder: crit-gated, a 3 m bubble, one turn. v2's is per-hit, arbitrarily
distributed, two turns — 4 targets in Act I, 6 in Act II, **8 in Act III, ~6 of them debilitated a
round**, and Frightened blocks movement outright.

**Rescue 1/1/2.** Nothing outward. Taking Eyebiter over Trickster gave up Touch Treatment, and the
partner reads Rescue 4 — a deliberate zero.

**Skills 3/2/2.** Proficiency without Expertise anywhere: Persuasion, Perception and Insight from
Mesmerist 1, Deception and Sleight of Hand from Charlatan, Consummate Liar's half-Mesmerist-level on
Deception (`floor(12/2) = 6`, unchanged from Mesmerist 13), and Astral Intuition's advantage on
every Intelligence check.

| act | Persuasion | Deception | Perception | Investigation |
|---|---:|---:|---:|---:|
| **I** (char 8) | +9 | **+11** | +3 | +3 <span class="faint">adv</span> |
| **II** (char 15) | +11 | **+16** | +5 | +3 <span class="faint">adv</span> |
| **III** (char 20) | +13 | **+19** | +6 | +3 <span class="faint">adv</span> |

Deception carries the body and clears Hag's Hair at DC 20. Beside Coldsnap's double Expertise the
pair reads **5 / 5 / 5**.

**Endurance 4/5/5.** The damage engine is at-will cantrips with no resource behind it, and the
Stares cost nothing. The clocks are sorcery points, two short-rest pact slots, one 3rd-level slot a
fight for Battlemind Link, and Hexblade's Curse once per short rest — none of which carries the
routine.

---

## Known weaknesses

1. **Act I sits on a boundary.** 1.507 against a rung-4 line of 1.5. Two unresolved questions each
   put it back to 3 — Hexblade's Curse reaching a spell beam, and the ability picker. Both are
   settled by observation inside the first five character levels, which is the point of putting
   them there.

2. **Everything keys off Charisma.** Four of the five beam riders are Charisma or Charisma-derived,
   so a refused picker costs `−3` a beam and `−24` a round through Acts I-II, where v1's exposure
   was `−2` a beam. The Mirror closes it from Act III either way.

3. **The 6 m Battlemind leash, and the ice.** The pair's accuracy tier now depends on both bodies
   standing inside a 6 m aura, and Coldsnap lays `CreateSurface(2,2,WaterFrozen)` on every beam hit
   — eight surfaces a round. This body has no `PRONE_ICE` immunity of its own. The gear table
   routes ice-proof boots through all three acts and Starlight Step gives five slot-free
   repositions, but the tension is real and is a **new** cost that v1 did not carry.

4. **The Stare dependency, not the AC.** The durability rung rests on the Resistance boon, which is
   conditional on a Stare being up, and a Stare cannot be *applied* beyond 9 m — though it persists
   at any range once applied.

5. **Hexblade's Curse is one target per short rest.** The single-target row is priced on the cursed
   figure because a boss is the single-target case, but against a second priority target in the same
   fight the beam drops to 25.5.

6. **Strength saves stay uncovered.** `−1`, and Mage Slayer only covers the magical case.

7. **The face is proficiency-only.** Persuasion `+13` post-Mirror against Act III checks reaching
   DC 30, and the partner is Charisma 8.

---

## Open decisions and unverified items

- `(unverified)` **`IsEldritchBlastAlike()` is engine-side.** Zero definitions across every `type_*`
  table, `type_script_extender_lua` and `type_script_extender_config`; only Mizora and Listo
  passives call it. **[database]** The entire rider suite — Agonizing, Frightful, Sickening — rides
  on it. **One observation settles it: does Agonizing Blast add Charisma to a beam?**
- `(unverified)` **Whether Hexblade's Curse's `DamageBonus(ProficiencyBonus)` reaches a spell
  beam.** The passive carries no weapon gate, which is the whole basis for reading it as per-beam.
  If it does not, the Act I rung falls to 3 and Act III `st_raw` falls `301.5 → 253.5`, ratio
  `4.275 → 3.748`, rung unchanged at 5. **Check the damage tooltip on a cursed target at character
  1.**
- `(unverified)` **Whether the ability picker measures the base score or the boosted one.**
  `SelectAbilities` greys out anything at 20; Lone Wolf's `+4` is a status boost, so the base is 17
  and the total is 21. **[pak]** Open the picker at character 5 — Charisma offered means the sheet
  runs at 22 from character 5, 23 from 18, and the Mirror's `+2` goes to Constitution; refused means
  21 until the Mirror and Constitution stays 21.
- `(unverified)` **Whether four `DamageBonus` boosts stack on one damage roll.** v1 already staked
  18.5 a beam on two of them stacking. Fire one **uncursed** beam and read the roll: expect
  `1d8 + 21` at Charisma 24.
- `(unverified)` **Whether Elemental Affinity's `DamageBonus` applies per beam or once per cast.**
  Magic Missile's per-dart precedent argues per instance. If once per cast, Act III `st_raw` falls
  `301.5 → 252.5` and the rung holds at 5.
- `(unverified)` **Whether Lone Wolf's halving and the Eyebiter Resistance boon multiply or share a
  cap.** The durability rung assumes they multiply.
- **Battlemind Link's radius is 6 m, not 3.** The mod page says 3; `MESMERIST_BATTLEMINDLINK
  AuraRadius "6"` **[database, load 431]**. `scoring.py`'s `ACCURACY` comment also says 3 m and
  should be corrected — the tier is right, the radius in the comment is not.
- **Repelling Blast and Grasp of Hadar are broken** — see *Invocations*. Confirmed in game. If the
  pack ever repairs the `REPELLING_BLAST_TRIGGER` name mismatch, Repelling becomes a live pick with
  no other change to this sheet.
- **Warlock 3 for a Pact Boon is feat-neutral and was costed.** Mesmerist 11 / Sorcerer 6 /
  Warlock 3 gives the same six feats, drops Painful Stare from `3d10` to `2d10` (`49.5 → 33`, Act
  III ratio `4.275 → 4.094`, **rung unchanged at 5**), and buys a Pact Boon plus 2nd-level pact
  slots. Only **Chain** has an argument — the duo has no third body — and the invocation that makes
  a familiar survive Act III (`IotCM` / `InvestmentOfTheChainMaster`) needs a slot Warlock 3 does
  not grant. Recorded as the cheapest available lever if the run turns out to be losing fights to
  action economy rather than damage.
- **Race is settled: Astral Half-Elf**, on mobility and Intelligence checks rather than shields.
  Nothing downstream keys off the race any more — the `(unverified)` subrace-inheritance question
  now touches only Fey Ancestry, and no number on this sheet depends on it. **Strongheart Halfling**
  is the recorded runner-up and **Shadar-kai** the option to revisit if the duo's missing third body
  becomes the binding problem.

---

## What changed from v1, and why

| | v1 | v2 |
|---|---|---|
| Split | Eyebiter 13 / **Deep** Draconic 6 / **GOO** 1 | Eyebiter **12** / **Amethyst** Draconic 6 / **Hexblade 2** |
| Engine | Illusionary Dart, **Psychic**, 18.5 a beam | Eldritch Blast, **Force**, **31.5** a beam cursed |
| Fear | Mortal Reminder — **crit-gated**, 3 m, 1 turn, ~75% a round | **Frightful Blast — per hit**, any distribution, 2 turns, effective DC 22 |
| Second rider | — | **Sickening Blast**, Constitution, effective DC 22 under Sapped Magic |
| Feats | 7, two on crit threshold | **6**, one on Agonizing Blast with an ability point attached |
| Engine complete | character 17 | **character 5** |
| Guaranteed damage | none | **Magic Missile**, free from Amethyst, per-dart Force scaling |
| Accuracy tier | ×1.19 | **×1.35** — Battlemind Link's `Advantage(AttackRoll)` was under-read |

Three findings drove it. **Frightful Blast is per hit rather than per critical**, which retired the
entire crit package and with it Great Old One. **Amethyst binds Elemental Affinity to Force**,
which put the doubler back on Eldritch Blast and made the Sorcerer block pay again. And
**`BATTLEMIND_BONUS` grants `Advantage(AttackRoll)` in a 6 m aura**, which was worth a full accuracy
tier the sheet had not been claiming — at the cost of a leash it now has to manage.
