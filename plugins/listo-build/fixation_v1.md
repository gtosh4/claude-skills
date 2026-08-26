# Fixation v1 — Eyebiter 13 / Deep Draconic 6 / Great Old One 1

**Mesmerist 13 (Aspect of the Eyebiter) / Sorcerer 6 (Draconic Bloodline — Deep) / Warlock 1
(The Great Old One)**, **Astral Half-Elf** — level 20, Lone Wolf duo partner for **Coldsnap v1**. A Charisma beam
caster that converts a partner's routine Blind into criticals, criticals into area Fear, and
carries a permanent no-concentration debuff aura on one enemy for the whole fight.

Every mechanic marked **[pak]** was read out of the installed Listonomicon 10.2 archive with
`skills/listo-build/scripts/lspk.py`. **[data]** is confirmed in the repository's compiled 10.2
snapshot. **[wiki]** is bg3.wiki, used only for vanilla Larian content whose base-game paks are
not under the mods root.

---

## The paired engine

1. **The partner supplies the advantage; Fixation converts it to criticals.** Coldsnap's
   Glaring Frost blinds on a Constitution save from every Cold or Radiant instance, and attacks
   against a blinded creature have Advantage. Fixation buys **no advantage source of its own**
   and spends the whole budget on **crit threshold** and **per-beam riders** instead — the same
   shape as Argent, moved off a greatsword and onto a cantrip.

2. **The beam count is not a Warlock feature.** `Projectile_IllusionaryDart` is a **Bard-list
   cantrip** — `Homebrew Spells`, merged into spell list `61f79a30-2cac-4a7a-b5fe-50c89d307dd6`,
   which is the list Mesmerist draws from. **[pak]**

   ```
   Projectile_IllusionaryDart  Level "0"  SpellSchool "Illusion"  TargetRadius "18"
     AmountOfTargets "LevelMapValue(EldritchBlast)"
     SpellRoll     "Attack(AttackType.RangedSpellAttack)"
     SpellSuccess  "DealDamage(1d8,Psychic,Magical)"
     UseCosts      "ActionPoint:1"
   ```

   It reads the **same level map as Eldritch Blast**, which keys off **character** level, not
   class level: beams at character **5, 10 and 17**. **[data]** Under Lone Wolf's second Action
   that is **2 / 4 / 6 / 8** beams a round across the run. All sixteen Homebrew cantrips were
   checked; **Illusionary Dart is the only multi-projectile one**.

3. **Two cantrips at exactly the same number, in two damage types.** Absolute Wrath stacks
   random resistance affixes on top of Combat Extender's curated ones, so a single-type beam
   engine is a liability.

   | | Illusionary Dart | Eldritch Blast |
   |---|---|---|
   | Type | **Psychic** | **Force** |
   | Base | 1d8 | 1d8 — Listo nerfed it from 1d10 **[data]** |
   | Range | 18 m | 18 m |
   | Beams | `LevelMapValue(EldritchBlast)` | same map |
   | +Cha | Potent Robe | Potent Robe |
   | +Cha again | **Elemental Affinity (Deep)** | — *(no Agonizing Blast)* |
   | Battlemind Link | +2 | +2 |
   | **Per beam at 20** | **18.5** | **11.5** |

   Switch on the target's resistance table. This is what replaces the Eyebiter's **Vital
   Pinpoint** boon, which would have cost a boon slot for a narrower answer.

   **The Force beam is a fallback, not a second engine, and it is not worth a feat.**
   Elemental Affinity keys off the *ancestry's* damage type, so on Deep it feeds the Dart
   and never the Blast; closing that gap costs `Eldritch Adept → Agonizing Blast`, a whole
   feat spent on a button you press only when Psychic is resisted. It is not needed: against
   a Psychic-resistant target the Dart halves to **9.25**, so a bare Eldritch Blast at
   **11.5** is still the better press — and against Psychic *immunity* it is the only one.
   Warlock 1 was bought for Mortal Reminder regardless.

4. **Criticals feed Mortal Reminder.** Great Old One Warlock 1: on a critical hit, every enemy
   within **3 m** must make a Wisdom saving throw or be **Frightened** for one turn, with **no
   per-turn limit**. **[wiki]** In BG3 Frightened means the target **cannot move** and has
   disadvantage on attacks and ability checks — for a duo with no third body, better than Blind,
   which still lets an enemy close and swing.

   Under the partner's Blind, `p = 1 − (1 − r/20)²` per beam:

   | Threshold source | r | p per beam | ≥1 crit per round (8 beams) |
   |---|---|---|---|
   | Spell Sniper | 2 (19–20) | 19.0% | 81.5% |
   | + Deadly Alacrity | 3 (18–20) | 27.8% | **92.6%** |
   | + Ring of Viciousness | 4 (17–20) | 36.0% | **97.5%** |
   | + installed Critfisher instead (threshold −3) | 6 (15–20) | 51.0% | **99.7%** |
   | + Dreamweaver (threshold −2, if it reaches spells) | 8 (13–20) | 64.0% | **99.97%** |

   The crit's own damage is small — only the `1d8` doubles, `+4.5`, because flat riders do not.
   **The criticals exist to fire Mortal Reminder**, not to add damage.

---

## Why Eyebiter and not Trickster

Both were costed. The Eyebiter wins on three axes the pair actually needs.

| | Eyebiter | Trickster |
|---|---|---|
| Durability | **Resistance boon: physical <10, all damage 10–19, Invulnerable at 20** **[pak]** | Fortifying Tricks: +3 AC / +3 flat DR at this depth |
| Coldsnap's save axis | **Sapped Magic** extends the Stare's penalty to **Constitution** and the target's spell DC | nothing touches Constitution |
| Cold-immune enemies | **Blinding**: Con save every turn or Blinded, at-will, no Cold involved | — |
| Act III undead/constructs | **Psychic Inception at 7** — Stare works at 100% on mind-immune creatures | blocked, then 50% from Mesmerist 6 |
| What it gives up | outward condition-stripping; **Haste on the partner** via Compel Alacrity | — |

```
EyebiterBoonResistance  Conditions "StatusId('MESMERIST_HYPNOTIC_STARE_OWNER')"
  ClassLevel < 10   EYEBITERBOONPHYSICALRESISTANCE  Resistance(Slashing/Piercing/Bludgeoning)
  ClassLevel 10-19  EYEBITERBOONALLRESISTANCE       Boosts "Resistance(All,Resistant)"
  ClassLevel 20     EYEBITERBOONIMMUNITY            Boosts "Invulnerable()"
```

The condition is **a Stare being up**, and the Stare is free, permanent, bonus-action and needs
no concentration. In practice the resistance is always on. **[pak]**

Losing Trickster's **Compel Alacrity** costs Haste-on-the-partner; **Sorcerer 2's Twinned
metamagic buys it back** and covers both bodies for one pick.

---

## Chassis

| Piece | Levels | What it is bought for |
|---|---|---|
| **Mesmerist 13 (Eyebiter)** | 13 | Hypnotic Stare, three Bold Stares, two Boons, Painful Stare, Psychic Inception, Towering Ego, Battlemind Link. Level 13 is the **5-feat rung** |
| **Sorcerer 6 (Draconic — Deep)** | 6 | **Elemental Affinity (Psychic)** = +Cha per beam. Draconic Resilience = AC 13 unarmoured + 6 HP. Font of Magic, Twinned, Fireball, Haste |
| **Warlock 1 (Great Old One)** | 1 | **Mortal Reminder**, Eldritch Blast, 2 cantrips, one short-rest pact slot |

Feat count: `floor(13/3) + floor(6/3) + floor(1/3) = 6`, **plus the universal level-13 grant on
Mesmerist = 7**. **[data]** Mesmerist is on the standard 3/6/9/12/13/15/18 cadence — the docs
claim a level-11 feat but `FeatsUni.json` grants it through `fighterfeat` and `roguefeat` only,
and the Mesmerist entry sits behind `enableAdvancedSettings: false`. **[data]**

**Mesmerist must be the level 1 class.** Saving-throw proficiencies come only from there.

---

## Race — Astral Half-Elf

`Astral Half-Elves` (`9676`), enabled. **[pak]**

```
AstralHalfElf  Level 1   PassivesAdded "Astral_Intuition;AstralElfHE_StarlightStepChargeGain"
                         Selectors "AddSpells(2b98b3c6-…);SelectSpells(d4c114c3-…,1,0,AstralFire,,,AlwaysPrepared)"
               Levels 5 / 9 / 13 / 17   PassivesAdded "AstralElfHE_StarlightStepChargeGain"
Astral_Intuition   Boosts "Advantage(Ability, Intelligence);"
Races.lsx  AstralHalfElf  ParentGuid "45f4ac10-3c89-4fb2-b37d-f973bb9110c0"    ← vanilla Half-Elf
```

Four grants, in order of what they are worth on this chassis.

1. **Shield proficiency, inherited from Half-Elf.** **AC 18 → 20.** Draconic Resilience is
   conditioned on not wearing *armour*, and a shield is not armour, so the unarmoured formula
   keeps working. It costs nothing: the engine is two cantrips at 18 m, BG3 enforces no free
   hand for casting, and Potent Robe is a body slot that never contends with an off-hand.
2. **`Advantage(Ability, Intelligence)`**, permanent, from level 1. This is the Mirror of Loss
   answer, and it is the one thing no feat in the list can buy. It also carries every Arcana,
   History, Investigation and Nature check for the whole run.
3. **Starlight Step** — bonus-action 9 m teleport, a charge at each of levels 1, 5, 9, 13, 17 =
   **5 per long rest**. A disengage on a body with two Bonus Actions and only the Stare to spend
   them on.
4. **Fey Ancestry** — advantage on saving throws against being Charmed. Real cover, because
   **Towering Ego switches off once a harmful mind-affecting effect has already landed**; Fey
   Ancestry works on the save that decides whether it lands.

**Astral Fire → Light**, which frees the cantrip pick the list below was spending on it. Light
armour proficiency is redundant behind Mesmerist 1, and the spear/pike/halberd/glaive
proficiencies are dead at Strength 8. **No ability scores** — see *Stats*.

### Provenance for the shield, which is the load-bearing claim

- **The mod grants no proficiencies itself.** `Public/Astral Half-Elf/Races/Races.lsx` carries no
  boost or proficiency node, and the level-1 progression adds only `Astral_Intuition` and the
  charge-gain passive. Everything else rides on the parent race. **[pak]**
- **No enabled pak overrides Half-Elf.** All **810** installed paks were listed and every
  `Progressions.lsx` inside them was read; none references `45f4ac10-3c89-4fb2-b37d-f973bb9110c0`.
  Zero hits, so vanilla Half-Elf stands unmodified in this install. **[pak]**
- **What vanilla Half-Elf grants is a `[wiki]` fallback** — base-game paks are not under the mods
  root. Darkvision, Fey Ancestry, Light armour, **Shields**, and spears/pikes/halberds/glaives:
  `https://bg3.wiki/wiki/Half-Elf`.
- **Draconic Resilience survives a shield** — *"Draconic Resilience works while wearing a
  Shield"*, `https://bg3.wiki/wiki/Draconic_Resilience`. Sorcerer is vanilla here and Listo
  records no override (`classes/sorcerer.md:301`). **[wiki + data]**
- `(unverified)` **Subrace inheritance itself.** That a subrace picks up its parent's grants is
  inferred from the mod omitting them, not read. Character creation lists the proficiencies
  before you commit; confirm the shield there, and if it is absent the AC line reverts to 18 and
  nothing else on this sheet moves.

---

## Stats

Races in Listo grant **no ability score bonuses** — the +2/+1 is assigned freely at creation
**[data]**, so nothing in this table depends on the race pick. Proficiencies still do: the shield
in the AC line comes from **Astral Half-Elf**, above.

| | Buy | Racial | Lone Wolf | Feats | **Final** | Mod |
|---|---|---|---|---|---|---|
| STR | 8 | — | — | — | **8** | −1 |
| DEX | 14 | — | — | — | **14** | +2 |
| CON | 14 | **+1** | **+4** | +1 Durable · +1 Tough | **21** | **+5** |
| INT | 10 | — | — | — | **10** | +0 |
| WIS | 10 | — | — | — | **10** | +0 |
| CHA | 15 | +2 | **+4** | +1 War Caster `(picker)` | **22** | **+6** |

27-point buy: `0 + 7 + 7 + 2 + 2 + 9`. Racial assignment: **+2 Charisma, +1 Constitution.**

**Lone Wolf +4 on Charisma and Constitution.** Charisma reaches **21 at level 1** with no ASI
feat spent, and Constitution picks up the save proficiency that guards concentration.

### Why the racial +1 goes to Constitution, not Dexterity

**Dexterity 15 and Dexterity 14 are the same modifier.** The point was doing nothing there. On
Constitution it turns `14 + 4 = 18` into `15 + 4 = 19`, which is the odd number **Durable's +1
lands on** — `19 → 20`, `+4 → **+5**`, at character 7. That is +20 hit points, +1 to every
Constitution save, and it costs nothing at all.

**Tough's +1 is then the wasted one**, taking 20 → 21 with no modifier behind it. That is
unavoidable once two Constitution half-feats are on the same sheet, and it is the right way round:
Durable is the earlier pick, so the even score arrives at character 7 instead of 10. Tough is
bought for `+2` per character level and `+2` to Constitution saves regardless — the ability point
was never the reason.

> **Constitution 21 is the one place Hag's Hair is not wasted.** `+1` takes it to **22**, `+5 → +6`
> — another 20 hit points before Lone Wolf's multiplier and another point on every concentration
> save. It is one per run and shared with the partner, so it is a **pair decision**: Coldsnap's
> Wisdom cannot use it (22 plus the Mirror already lands exactly on the cap of 24, so a 23 would
> throw the Mirror's second point away), but Coldsnap's own Constitution 21 wants it for the same
> reason this sheet does.

Constitution sits at 19 for characters 1–6, before Durable.

### Two half-feats, and only one of them is guaranteed

**There are two mechanisms in this modlist, and they behave differently.** Feats Overhaul
delivers its ability increases as a *passive boost*; Essential Feats and the Listo War Caster
patch deliver theirs through the vanilla *ability picker*, which greys out anything already at
20. **[pak]**

```
Actor        PassivesAdded "Actor"   (no Selectors)
             Boosts "…;Ability(Charisma,1)"                          <- boost, no maximum arg
Tough        PassivesAdded "Tough"   (no Selectors)
             Boosts "IncreaseMaxHP(Level*2);RollBonus(SavingThrow,2,Constitution);Ability(Constitution,1)"
WarCaster    Selectors "SelectAbilities(771b7e52-…,1,1,DWE_WarCaster_UA2_ASI)"   <- picker
SYR_EldritchAdept
             Selectors "SelectAbilities(6d64a5f2-…,1,1);SelectPassives(…)"       <- picker
```

| Grant | Mechanism | Clears 20? |
|---|---|---|
| **Durable +1 CON** | Feats Overhaul boost | not at issue — 19 → 20 is under the cap |
| **Tough +1 CON** | Feats Overhaul boost | lands on 20 → 21 and is **wasted**; the feat is bought for the other two grants |
| **War Caster +1 CHA** | Listo patch, `SelectAbilities` | `(unverified)` — see below |

**Lone Wolf's +4 is itself a boost, and it does reach 21.**
`GOON_LONE_WOLF_CHARISMA_STATUS` carries
`Boosts "Ability(Charisma,4);ProficiencyBonus(SavingThrow,Charisma)"` — two arguments, no
maximum. **[pak]** `references/listo-rules.md:217` records this as *"stops at 20"*; that row is
wrong.

So Charisma opens at **21**, and whether War Caster lifts it to 22 turns on a question the paks
cannot settle: does the picker measure the **base** score (17, so the point lands) or the
**boosted** one (21, so it is refused)? That is exactly the unresolved caveat at
`data/listo-10.2-feats.md:72-79`.

> **This is why War Caster sits at character 3.** It is the earliest slot on the sheet, and
> opening its ability picker answers the question at character 3 instead of character 14 — while
> there is still a whole run in which to spend the answer.

> **The damage arithmetic on this sheet runs on Charisma 22.** If the picker refuses, every beam
> loses 2 damage until the Mirror lands in Act III — Act III raw goes `197.5 → 165.5` and the
> spell save DC goes `20 → 19`. **Post-Mirror the sheet is Charisma 24 either way**, which is the
> point of the routing below.

**Spell save DC = 8 + 6 + 6 = 20** before gear, **19** if the picker refuses, **21** from the
Mirror.

### The Mirror of Loss

**+2 to a chosen ability, raising it as high as 24, plus a separate optional +1 Charisma, per
character** — Religion DC 25 in Act III **[data]**. The check is **per character and the +2 lands
on whoever rolled**, so Fixation must clear it for itself. It does, twice over: Astral Intuition
gives permanent advantage on the roll, and the pair respecs at Withers into Religion Expertise,
rolls, and respecs back **retaining the enhancement** **[data]**. No feat is spent on it.

**Both grants go on Charisma, and the result is the same in both branches:**

| | Picker reads base | Picker reads boosted |
|---|---|---|
| Pre-Mirror | 17 `+1 WC` = 18, `+4 LW` = **22** (+6) from character 3 | **21** (+5) through Act II |
| Mirror | **+2 → 24** (+7); the optional +1 is dead at the cap | **+2 and +1 → 24** (+7) |
| Constitution | **21** (+5) | **21** (+5) |

**Charisma 24 and Constitution 21 whichever way it falls.** The picker decides only *when* the
sheet reaches +6, not where it finishes. Constitution 22 is off the table: reaching it needed the
Mirror's +2 spare, which only happens with two picker-based Charisma points, and there is one.

### Saves at 20

| Save | Total | Source |
|---|---|---|
| **CHA** | +12 (**+13** at Charisma 24), **advantage** | Mesmerist level 1 · advantage from Towering Ego at Mesmerist 10 |
| **CON** | **+13, advantage on concentration** | Lone Wolf proficiency · Constitution 20 · Tough +2 · War Caster |
| DEX | **+10** | Mesmerist level 1 · **Shield Master** +2 while a shield is equipped |
| WIS | +6 | **Towering Ego** — flat +Cha, not proficiency |
| INT | +6 | Towering Ego, full Charisma from Mesmerist 10 |
| STR | **−1** | uncovered, and nothing on the sheet closes it |

**Five of six covered, four of them disjoint from Coldsnap's Str/Dex/Wis/Con.** Blindness
immunity arrives at Mesmerist 9 via Penetrating Stare. **[pak]**

> **Mage Slayer covers the holes where they actually matter.** From character 20 it grants
> **advantage on saving throws against every spell** — not melee range only, as in vanilla —
> and **reduces all spell damage by the proficiency bonus**, so `−6` a hit at level 20.
> **[data]** Strength, Wisdom and Intelligence stay uncovered against non-magical effects;
> against magical ones the whole row moves. Its anti-concentration half is dead weight here:
> the disadvantage aura is 3 m and this body fights at 18 m.

> **Towering Ego switches off while you are already under a harmful mind-affecting effect.**
> It is preventative only — it does not help you shake a Dominate that has landed. Do not read
> the Wis and Int rows as recovery. **[data]**

---

## Feats — seven

| Char | Feat | What it buys |
|---|---|---|
| 3 | **War Caster** | `+1 CHA → 22` **if the picker allows it** — and the earliest slot on the sheet, so the answer arrives at character 3. Advantage on concentration saving throws, which starts earning at 14 |
| 7 | **Durable** | `+1 CON → 20`, **full hit points on every short rest**, and in-combat regeneration below 60%. The feats file calls it strongest early, before healing and camp supplies stabilise **[data]** |
| 10 | **Tough** | **+2 Constitution saves**, +2 HP per character level (+40). Its `+1 CON` lands on 21 and is wasted — see *Stats* |
| 14 | **Shield Master** | +2 Dexterity saves, **−1 to all damage taken**, and Block is now a **passive** — the same effect as Rogue Evasion, spending no reaction. Shield Blow as a bonus action **[data]** |
| 17 | **Spell Sniper** | Crit threshold **−1 and it stacks**, an extra cantrip, no low-ground penalty on ranged spell attacks **[data]** |
| 19 | **Deadly Alacrity** | Crit threshold **−1 → 18–20**. Its +1 ability score is removed by the Listo patch **[data]** |
| 20 | **Mage Slayer** | **Advantage on saves against all spells**, and all spell damage reduced by the proficiency bonus **[data]** |

Spell Sniper's damage-die advantage applies to **the first hit only** on multi-hit spells
**[data]** — worth about `+1.3` a round, not `+10`. The feat is bought for the crit threshold,
and it waits until 17 because the threshold is only worth anything under the partner's Blind,
which is not reliably up in Act I.

**Shield Master needs the shield, which the race supplies.** Astral Half-Elf inherits shield
proficiency from Half-Elf, and Draconic Resilience keeps working behind it — see *Race*. If that
inheritance turns out to be wrong at character creation, this feat has nothing to attach to and
should become **`Mobile`** — `+3 m` speed, disadvantage on every opportunity attack against you,
and `StatusImmunity(SG_DifficultTerrain)` so the partner's ice fields stop costing movement
**[pak]**. It does **not** stop the slip: `PRONE_ICE` immunity is a Winter Spirit boost and is
personal to Coldsnap from Druid 6, so this body wants the boots that carry
`MAG_Frost_IceSurfaceProneImmunity_Boots_Passive` **[pak]**.

### Four feats this sheet used to carry, and why they are gone

- **`Eldritch Adept → Agonizing Blast`.** It never touched the engine. Elemental Affinity keys
  off the ancestry's damage type, so the Dart is already doubled; Agonizing Blast was buying
  parity on the *fallback* beam. See *The paired engine*.
- **`Actor`.** Four Charisma Expertises and the only *guaranteed* route past Charisma 20. Cut
  because the stat line reaches 24 without it in both picker branches, and because the three
  feats that replaced it — a third body, a damage floor and blanket spell-save advantage — each
  answer a structural problem the pair has and the face does not.
- **`Skeleton Crew`.** A free scaling body at the start of every combat is the textbook repair
  for duo action economy, and on paper it was the best pick on the sheet. **Cut on an
  in-game observation that it is not firing reliably** — not on a costing. If it turns out to
  work, it is the first feat back, and `Durable` is what it displaces.
- **`Skilled Expert` and `Resilient (Strength)`.** Skilled Expert existed only to put Expertise
  on Religion for the Mirror, which Astral Intuition and a 100-gold respec now cover for free.
  Resilient was the replacement, and it lost to Mage Slayer: a single Strength save proficiency
  is narrower than advantage on every spell save in the game.

**The face is proficiency-only, and that is the price.** Persuasion runs `+6 mod + 6 proficiency
= +12`, reaching **+13** once the Mirror lands, against Act III checks that reach DC 25–30.
Deception is fine on its own — **Consummate Liar** adds half the Mesmerist level, so `+19` in Act
III — so lean on Deception wherever the dialogue offers both. Intimidation and Performance have
no proficiency at all. Coldsnap is Charisma 8, so there is no second face in the pair.

---

## The two Eyebiter Boons — Mesmerist 4 and 8

| Boon | At Mesmerist 13 | |
|---|---|---|
| **Resistance** | Resistance to **all damage** while a Stare is up | **take** |
| **Manifold Stare** | Painful Stare becomes **3d10, three times per turn** = 49.5 a round | **take** |
| Vital Pinpoint | Ignore resistance to all damage; ignore **immunity** only at Mesmerist 20 | skip — the Force beam covers it |
| Mirror | Inverse of each Bold Stare penalty to self (+3 AC off Sundering) | skip — worse than Resistance |

`MorePainfulStare` level map: `6-9: 2d8 · 10-11: 2d10 · 12-17: 3d10 · 18-19: 4d10 · 20: 4d12`.
**[pak]** At Mesmerist 13 it sits at **3d10** and stops there. Base Painful Stare without the
boon is `4d6` **once** per turn — the boon is worth `49.5 − 14 = +35.5` a round.

---

## The three Bold Stares — Mesmerist 3, 7 and 11

| Pick | Tier | At 3 Stare stacks |
|---|---|---|
| **Blinding** | 1 | `OnApplyRoll "not SavingThrow(Ability.Constitution, SourceSpellDC())"`, `TickType "StartTurn"` — **a Constitution save every turn or Blinded**, at DC 20, at will **[pak]** |
| **Sundering** | 1 | The Stare's penalty also applies to AC → **−3 AC** **[pak]** |
| **Sapped Magic** | 3 | The penalty also applies to **the target's Constitution saves and spell save DC** → **−3 both** **[pak]** |

```
MESMERIST_HYPNOTIC_STARE
  Boosts "RollBonus(SavingThrow,-1,Intelligence);RollBonus(SavingThrow,-1,Wisdom);
          RollBonus(SavingThrow,-1,Charisma)"
  StackId "MAG_PSYCHIC_MENTAL_FATIGUE"
  StatusPropertyFlags "…MultiplyEffectsByDuration;FreezeDuration"
BOLDSTARE_SAPPEDMAGIC  Boosts "RollBonus(SavingThrow,-1,Constitution);SpellSaveDC(-1)"   ×3
```

**The base Stare debuffs Intelligence, Wisdom and Charisma only.** It does nothing for Glaring
Frost, which is a **Constitution** save. **Sapped Magic is the pick that makes the pairing work,
and it arrives at character 18.** That is the honest shape of this partnership: the deep synergy
is Act III.

---

## Progression ladder

**Re-derived level by level, and it needs no respec.** The per-level optimum turns out to be
monotone — every level is a forward pick, nothing is ever taken and dropped. Characters 1–5 are
locked anyway (no Withers yet), and 6–20 happen not to want one.

**Every locked pick is in the `Choose` column.** This chassis asks for far more than feats: a
subclass, **three Bold Stares**, **two Eyebiter's Boons**, a patron, a bloodline *and* an
ancestry, **three Metamagics**, twelve cantrips and a spell known at almost every level. All of
them are respec-only. The `Choose` column is the build order; `What lands` is what the level
gives you whether you pick or not.

| Char | Take | Choose | What lands | Feat |
|---|---|---|---|---|
| 1 ★ | Mesmerist 1 | <b>3 skills</b> → Persuasion, Perception, Insight · <b>2 Bard cantrips</b> → <b>Illusionary Dart</b> + one spare (Light is free from Astral Fire) | <b>Dex + Cha saves</b>, light armour, finesse. Hypnotic Stare, Feint. <b>Mesmerist must be first</b> | — |
| 2 | Mesmerist 2 | <b>1 spell known</b> — and one at every Mesmerist level after this | <b>Towering Ego</b>, Consummate Liar, half-caster slots begin | — |
| 3 | Mesmerist 3 | <b>Subclass</b> → <b>Aspect of the Eyebiter</b> · <b>Bold Stare (Tier 1)</b> → <b>Blinding</b> · spell · feat | A Constitution save every turn with no Cold in it | **War Caster** |
| 4 | Mesmerist 4 | <b>Eyebiter's Boon</b> → <b>Resistance</b> · <b>3rd cantrip</b> · spell | Physical resistance stacked on Lone Wolf's halving is <b>quarter damage</b> from every weapon in Act I | — |
| 5 ★ | <b>Warlock 1</b> | <b>Patron</b> → <b>The Great Old One</b> · <b>Eldritch Blast + 1 cantrip</b> · <b>2 spells known</b> | <b>Mortal Reminder</b> — and the beam count doubles on this level, so the crit rate goes to <b>34% a round</b> the moment it arrives. One short-rest pact slot | — |
| 6 | Mesmerist 5 | <b>spell</b>, plus <b>2 free Pathfinder spells</b> for the new tier | Stare <b>2 stacks</b>, Penetrating Stare, 2nd-level spells | — |
| 7 | Mesmerist 6 | spell · feat | <b>Painful Stare 2d6</b>, Feint −2 attack, mind-immunity 50% | **Durable** |
| 8 | Mesmerist 7 | <b>Biting Gaze</b> (Tier 1 or 2) → <b>Sundering</b> · spell | −2 AC on the Stare target, which both characters attack. <b>Psychic Inception</b> — the Stare works at 100% on mind-immune creatures, before the Shadow-Cursed Lands | — |
| 9 | Mesmerist 8 | <b>Eyebiter's Boon 2</b> → <b>Manifold Stare</b> · spell | Painful Stare twice a turn | — |
| 10 | Mesmerist 9 | spell · feat | <b>Battlemind Link</b> always known (+2 AC, +2 damage per instance, +2 initiative on <em>both</em> bodies, no save, no concentration). Immune to Blindness, sees through fog and magical darkness. <b>Beams 2 → 3</b> | **Tough** |
| 11 ★ | Mesmerist 10 | <b>4th cantrip</b> · spell | <b>Resistance → all damage</b> while a Stare is up. Towering Ego to full Charisma on Intelligence, advantage on Charisma saves | — |
| 12 | Sorcerer 1 | <b>Bloodline</b> → <b>Draconic</b> · <b>Ancestry</b> → <b>Deep</b> (Psychic; Dissonant Whispers free) · <b>4 Sorcerer cantrips</b> · <b>2 spells known</b> → <b>Shield</b>, <b>Magic Missile</b> | Draconic Resilience — unarmoured AC 13, +1 HP per level | — |
| 13 | Sorcerer 2 | <b>Metamagic ×2</b> → <b>Twinned</b> + <b>Quickened</b> · spell | Font of Magic. <b>Both metamagics land here, not at Sorcerer 3</b> | — |
| 14 | Sorcerer 3 | <b>3rd Metamagic</b> → <b>Careful</b> · spell · feat | Sorcery points deepen; Careful is what keeps Fireball off the partner | **Shield Master** |
| 15 | Sorcerer 4 | <b>5th Sorcerer cantrip</b> · spell | — | — |
| 16 | Sorcerer 5 | <b>spell</b> → <b>Haste</b> | 3rd-level slots. Twinned Haste covers both characters for one pick | — |
| 17 ★ | Sorcerer 6 | <b>spell</b> → <b>Fireball</b> · feat (Spell Sniper adds the 12th cantrip) | <b>Elemental Affinity (Psychic)</b> — +Charisma to every psychic beam. <b>Beams 3 → 4</b>, so the doubler and the fourth beam land together | **Spell Sniper** |
| 18 | Mesmerist 11 | <b>Masterful Gaze</b> (any tier) → <b>Sapped Magic</b> · spell | Stare <b>3 stacks</b>. −3 to the target's Constitution saves and spell save DC. Phasic Challenge | — |
| 19 | Mesmerist 12 | spell · feat | Painful Stare → <b>3d10, three times a turn</b> — 49.5 a round | **Deadly Alacrity** |
| 20 | Mesmerist 13 | spell · feat | Permanent See Invisibility | **Mage Slayer** |
| *III* | — | ***Mirror of Loss* → Charisma** — `+2` to 24, and the separate `+1` where the picker refused | Beam damage, spell save DC and every Charisma check move together | — |

★ = the four levels that change what the body is.

**Two corrections the choice column forced.**

- **Metamagic is 2 at Sorcerer 2 and 1 at Sorcerer 3, not 2 at Sorcerer 3.** `Expansion.pak`
  carries exactly one Metamagic selector,
  `SelectPassives(c3506532-…,1,Metamagic)` at level 17 **[pak]**; levels 1–12 are vanilla and
  base-game paks are not under the mods root, so the cadence is the wiki's — **2 at 2, +1 at 3,
  +1 at 10, +1 at 17** — and `data/classes/sorcerer.md:39` records the same
  (`https://bg3.wiki/wiki/Sorcerer`, **[wiki fallback + data]**). Twinned and Quickened therefore
  arrive one level earlier than this sheet used to say, and Sorcerer 3 has a third pick that was
  never spent.
- **Fireball and Haste cannot both be taken at Sorcerer 5.** Spells known run 2 / 3 / 4 / 5 / 6 / 7
  across Sorcerer 1–6 **[data]** — one new spell a level. Haste is the one that matters for
  Twinned, so it goes at Sorcerer 5 and Fireball follows at Sorcerer 6. **No rung moves**: the Act
  II checkpoint is character 15, which is Sorcerer 4 and has neither, and the Act III checkpoint
  is character 20, which has both.

### Why Warlock 1 is character 5 and not character 8

**The beam count doubles on that exact level.** Mortal Reminder fires on a critical hit, and the
crit rate is `1 − (1 − r/20)ⁿ` across `n` beams. Spell Sniper does not arrive until 17, so the
threshold here is a bare natural 20 and `p` per beam under the partner's Blind is `9.75%`: at
character 4 that is two beams and a **19%** chance of a crit per round; at character 5 it is
four beams and **34%**. Buying it one level later than it becomes good, rather than three
levels after, is free. The threshold feats then take the same four beams to **81%** at 17 and
**93%** at 19.

### Why Mesmerist runs to 10 before any Sorcerer level

Every Mesmerist level from 5 to 10 beats every Sorcerer level below the sixth, so greedy is
correct through character 11. It pulls four things forward by six levels each against the
previous ladder: **Painful Stare to 7, Manifold Stare to 9, Battlemind Link to 10, and
Resistance-to-all-damage to 11.**

### The Sorcerer block is the one thing that cannot be greedy

Sorcerer 1 through 5 buy almost nothing on their own — an unarmoured AC that ties the light
armour it replaces, Font of Magic, one metamagic, and then Fireball. **They are a down payment
on Elemental Affinity**, which is the only level in the block that changes the damage. So it is
bought as an unbroken run, and the run is timed to **finish exactly on character 17**, where the
fourth beam lands. The doubler and the beam arrive together.

**Sapped Magic is what that costs.** Mesmerist 11 cannot come before the block without pushing
Elemental Affinity past the start of Act III, so the pair's own synergy stays at character 18.

---

## Concentration budget

Nothing in the core loop needs it. Hypnotic Stare, all three Bold Stares, Painful Stare and
Battlemind Link are free and permanent. That matters because Coldsnap's concentration is welded
to Friar's Bond for the whole run — Fixation is the only body in the pair with a free slot.

| Candidate | Cost | Verdict |
|---|---|---|
| **Twinned Haste** | 3 sorcery points, concentration | **Default.** Covers **both** characters for one metamagic pick — four Actions a round for the pair |
| **Doom, upcast** | slot, concentration | The penalty **multiplies by slot level**: a 6th-level slot is **−6 to attacks, damage, saves and skill checks**. Multiclass caster level `floor(13/2) + 6 = 12` reaches 6th **[data]** |
| Synesthesia | 3rd, concentration | −4 AC and Dex saves, 20% miss, cannot crit. Boss tool |

Haste and Doom compete for one slot. Haste usually wins; Doom wins where the fight is long and
the enemy's own accuracy is the threat.

---

## Cantrips — twelve

Mesmerist 4 (Mesmerist 1, 1, 4, 10) + Sorcerer **5** (Sorcerer 1 ×4, +1 at Sorcerer 4) +
Warlock 2 (Eldritch Blast and one other) + Spell Sniper 1 **[data]**. The previous count of
eleven read Sorcerer's as four and missed the level-4 pick.

**Illusionary Dart** (Psychic engine) · **Eldritch Blast** (Force engine) · **Light** — the
partner's Callous Glow Ring needs an illuminated target; **Astral Fire supplies this one free**,
so the pick it was using is spare, and Coldsnap carries its own copy for the rounds where lighting
its own target beats spending an Action here ·
**Friends**, **Minor Illusion**, **Mage Hand**, **Bone Chill**, **Blade Ward**, **Ray of
Frost**, **Fire Bolt**, **Vicious Mockery** — and **one Bard slot still open**, because Astral
Fire supplies Light for free. Listo's Bard list is twelve entries **[data]**; what is left worth
taking is **Thunderclap** — an area Constitution save in a damage type nothing else here
deals — or **Thunder Note**.

Penetrating Stare at Mesmerist 9 sees through magical darkness, so Fixation never needs its own
Light to fight — only the partner does.

---

## Gear — full beam-caster audit

The installed paks change the answer materially. **Critfisher Ring is threshold −3**, not an
unspecified small reduction, and **Cloaks of Faerûn** supplies another global threshold −1.
Consequently Fixation does not need to spend every slot on critical range: Critfisher plus Spell
Sniper already makes Mortal Reminder routine, and Dreamweaver / Deadly Alacrity push it well past
that point. Use the remaining slots for accuracy, per-beam damage and control.

**Potent Robe remains the Act II core**, but it is not the final word. The installed **Better End
Game Caster Robe** pak places the **Robe of the Archmage** set in the Illusion wing's gilded chest
in Sorcerous Vault. Its robe has the same spellcasting-modifier rider on every cantrip instance,
then adds Arcane Enchantment, +2 AC and spell resistance; in Act III it is the offensive upgrade.
Potent Robe remains the durability swap because its Charisma temporary HP refreshes every turn.
Do not wear Psychic Armory's chestpiece over either robe.

| Slot | Target | Why it belongs here |
|---|---|---|
| **Main hand** | **Astral Echo → Voidpiercer → Dreamweaver** | Carry the rapier as a casting stat stick. Voidpiercer's `Mesmerist_Causality_Passive` has unconditional `ReduceCriticalAttackThreshold(1)`; Dreamweaver upgrades it to **2**. The bonus attack is weapon-only, but the threshold has no weapon predicate, so verify once that it reaches spell attacks. Non-disarmable is unusually valuable against Absolute Wrath explosions. **Rhapsody** is the higher-output swap when disarm is not a threat: three Scarlet Remittance stacks add +3 to attacks, damage and save DC, including each beam. **[pak/wiki fallback]** |
| **Off hand** | **Ketheric's Shield** | +1 spell attack and save DC while preserving the AC and Shield Master package. **Sentinel Shield** is the initiative swap. These are vanilla fallbacks: the enabled Revised Shields pak does not override either record. |
| **Ranged stat stick** | **Bow of Awareness → Hellrider Longbow** | Initiative is more useful than another over-cap crit source. **The Dead Shot** is a global threshold −1 swap if Dreamweaver fails the spell-attack test, but it is redundant once the installed Critfisher is equipped. **[wiki fallback; no enabled override found]** |
| **Body** | **Potent Robe → Robe of the Archmage** | Potent Robe adds Charisma to every cantrip instance and renewable temp HP. The installed endgame robe repeats the casting-modifier cantrip rider and adds `MAG_ArcaneEnchantment_Passive`, +2 AC and spell resistance; use Potent when the temp HP matters more. **[pak]** |
| **Head** | **Birthright only while below CHA 22 → Hood of the Weave** | Birthright / Hat of Charisma is +2 Charisma capped at 22, so it is dead once Fixation reaches 22 and cannot help the Act III CHA 24 plan. Hood of the Weave's +2 spell attack/DC is the final target; Mask of Soul Perception trades DC for +2 attack and initiative. The Archmage circlet is the set fallback (+1 attack/DC, magical durability and See Invisibility). **[pak/wiki fallback]** |
| **Boots** | **Mindwalkers → Treads of Psychic Stride** | Psychic Stride fires `OnDamage` whenever one damage event deals **5+ Psychic**, granting 1 turn of Momentum. A fully ridden Illusionary Dart beam always clears the threshold, so the four independent beams should fill the five-turn Momentum cap rapidly. The passive is not `OncePerAttack`; **verify multi-beam stacking in game**. Treads also add Eclipsing Penumbra, a once-per-rest teleport/control field. **[pak]** |
| **Cloak** | **Cloak of the Weave / Cloak of Arcane Potency** | +1 spell attack and DC improves every beam and every Stare. **Psion's Shroud** is the defensive-control swap: a Stared attacker saves Con DC 17 or is Dazed for 2 turns, and its upgraded field punishes enemies when Fixation is immobilised. **Bhaalist Cloak** gives global threshold −1 and Force-resistance bypass, but Critfisher makes the threshold redundant and the bypass helps only Eldritch Blast. **[pak/wiki fallback]** |
| **Gloves** | **Spellmight Gloves / Archmage Gloves** | Spellmight adds `1d8` to every spell-attack beam at −5 to hit; use it into reliable Blind/Advantage and high hit chance. The installed Archmage Gloves give +2 to melee and ranged spell attacks with no penalty, the endurance default. **Quickspell Gloves** add one whole cantrip as a bonus action once per short rest and are the burst swap; **Gemini Gloves add only one extra projectile**, not another four-beam cast. Astral Grasp is a control swap whose once/short-rest rider is consumed by the first beam. **[pak/wiki fallback]** |
| **Amulet** | **Spineshudder Amulet** | Every ranged spell-attack hit inflicts 2 Reverberation. Illusionary Dart therefore reaches the five-stack prone check during one cast and continues stripping physical saves for the partner. The enabled mod paks do not override the vanilla passive. Amulet of the Devout (+2 DC) is the pure Stare/control swap. **[wiki fallback; override search]** |
| **Rings** | **Critfisher Ring + flex** | The installed ring is unconditional `ReduceCriticalAttackThreshold(3)` and is the only mandatory ring. Slot two is **Callous Glow** (+2 Radiant per beam against an illuminated target), **Coruscation** (Radiating Orb control), or Ring of Viciousness (another −1) only when a partner owns the damage/control rings. Ring of Mental Inhibition and Braindrain Gloves collide with the Stare's `MAG_PSYCHIC_MENTAL_FATIGUE` StackId and are not defaults. **[pak/wiki fallback]** |
| **Trinket** | **Book of Many Spells → Book of the Arcane Codex** | JWL's otherwise-free instrument slot is real gear. The installed Book of Many Spells grants +2 spell attacks; the legendary Arcane Codex grants +3 spell attacks and +3 spell save DC. **Guardian Emblem** is the crit alternative (global threshold −1 plus immunity to incoming crits), but it is redundant beside Critfisher. **[pak]** |

The Psychic Armory scavenger hunt begins in Act I; its clue book points to Mindwalkers, Glittering
Gloves, the base rapier and their upgrade materials, while the **Padma Blossom** in the Arcane
Tower chain upgrades the set. Continue the weapon path through Voidpiercer and Dreamweaver, but
treat the other Armory slots as swaps rather than a mandatory set. **[pak]**

**Attunement check.** The live cap is five attuned items and three Legendary items. Do not try to
wear Dreamweaver, Critfisher, Bhaalist Cloak, Guardian Emblem, Arcane Codex and every upgraded
Armory piece simultaneously. The default spends its Legendary budget on **Dreamweaver,
Critfisher and Arcane Codex**; use the accuracy/DC cloak, Spineshudder and a non-Legendary flex
ring around them. If an Armory upgrade is explicitly tagged for attunement in game, drop the
least important defensive piece first rather than the beam riders.

**Do not use the Resonance Stone as the default Psychic amplifier.** Steeped in Bliss doubles the
Dart against creatures without immunity, but it also grants Advantage on physical saves. That
directly helps enemies pass Coldsnap's Constitution-save Blind and Fixation's own Blinding Stare.
It is a resistance-table swap only, for fights where doubling Psychic outweighs breaking the
pair's Blind engine.

---

## Scores

Ten axes, per act, on the pair-sheet rubric.

| Axis | I | II | III |
|---|---|---|---|
| Single-target | **1** | **5** | **5** |
| AoE | **1** | **4** | **4** |
| Durability | 4 | 5 | 5 |
| Actions | 2 | 4 | 4 |
| Control — single | 4 | 5 | 6 |
| Control — area | 1 | 3 | 4 |
| Rescue | 1 | 1 | 2 |
| Skills | **3** | **2** | **2** |
| Saves | derived | derived | derived |
| Endurance | 4 | 5 | 5 |

### Single-target, worked

| | Act I | Act II | Act III |
|---|---|---|---|
| Beams a round | 4 | 6 | 8 |
| Damage a beam | 4.5 | 16.5 | 18.5 |
| Cantrip total | 18 | 99 | 148 |
| Painful Stare | 7 (`2d6`) | 18 (`2d8` ×2) | **49.5** (`3d10` ×3) |
| **Raw** | **25** | **117** | **197.5** |
| Accuracy multiplier | ×1.19 | ×1.19 | ×1.19 |
| **Delivered** | **47.6** | **186.8** | **339.7** |
| Par | 60 | 87 | 123 |
| **Rung** | **1** | **5** | **5** |

Accuracy takes the **tier-1** multiplier — the partner's blind engine is save-gated, so `1.19`,
not tier 2's `1.35`. Effectively the whole raw is ranged spell attack rolls or a Painful Stare
riding one, so it takes the full tier.

### AoE, worked

The old row counted one Fireball and ignored that both beam cantrips may split their targets. That
was inconsistent with Coldsnap's area row and with the rubric's explicit “a beam is an instance”
rule. The revised ladder also moves Sorcerer 5 to character 16, so **Fireball is not available at
the Act II checkpoint**.

| | Act I | Act II | Act III |
|---|---:|---:|---:|
| Beam action | 2 beams × 2 Actions | 3 beams × remaining Actions | 4 beams × remaining Actions |
| Slot spell | none credited | **Cold Snap**, upcast through 5th | **Fireball**, averaged over the damage share of the 4th–6th-level slots |
| Raw / instances | 18 / 4.0 | 125.2 / 6.4 | 177.4 / 8.0 |
| With `k`, then attack-roll correction | 25 | 139 | 215 |
| Ratio to par | 0.52 | 2.14 | 2.63 |
| **Rung** | **1** | **4** | **4** |

**Act I — spread the beams.** Four bare `1d8` beams are `18` raw and four instances. After Act I's
`k = 3` and the rubric's `0.65/0.775` correction for attack-roll area damage, that is `25` against
par `48`. Animus Mine is a reactive 1 m burst and does not beat the standing beam routine.

**Act II — Cold Snap plus beam filler.** At character 15 Fixation is Mesmerist 10 / Sorcerer 4 /
Warlock 1: caster level 9 with 5th-level slots, but only 2nd-level Sorcerer spells known. The
installed Homebrew spell `Target_ColdSnap` is the best clean fit: 18 m range, 2 m radius,
Constitution save for half, `3d8` Cold plus `1d8` per upcast and an ice surface. At 5th it is
`6d8`. Allocating 35% of the 14-slot table to damage supports about 0.41 area casts a round; beam
filler occupies the other Actions. Only the beam portion takes the attack-roll correction.

**Act III — Fireball plus beam filler.** Fireball arrives at character 17 and can upcast through
6th. Allocating 30% of the caster-12 table to damage supports 0.475 casts a round; spending the
highest applicable slots averages about `9.7d6` per cast. The other 1.525 Actions are four-beam
casts. The result is **2.63× par, just below the 2.65 rung-5 line**, so it stays rung 4.

Flash Freeze (`7d8` Cold at 6th, cone), Aether Lance (`11d4` Force at 6th, no listed save) and
Cold Snap (`7d8` at 6th, 2 m radius) are useful resistance/control alternatives. Fire Cyclone and
Minute Meteors can outperform one cast over time, but both take the concentration slot from
Twinned Haste or Doom and therefore do not carry the default damage row. Mortal Reminder remains
area *control*, not area damage.

### Durability, worked

```
HP  8 + 12×4.5 (Mesm) + 6×3.5 (Sorc) + 4.5 (Warlock)
      + 6 (Draconic Resilience) + 40 (Tough) + 100 (Con 21)  = 233
AC  13 (Draconic Resilience, unarmoured) + 2 Dex + 1 Potent Robe + 2 Battlemind Link
      + 2 shield (Half-Elf proficiency)                                             = 20
```

**Lone Wolf's +30% is not in that figure and must not be.** It is excluded on both sides of the
§3 ratio as universal to every chassis in the ledger, exactly as the partner's sheet excludes it.
The pair sheets used to fold it into Acts II and III and leave it out of Act I — `303` where the
line above now reads `233` — which read as a durability climb this chassis does not have. **The
rungs do not move**: at the corrected pools the ratios are `1.94 / 4.19 / 3.99` against a rung-5
line of `2.40`, so Acts II and III were never close to the boundary.

Dexterity 14 and 15 give the same `+2`, so moving the racial point to Constitution costs the AC
nothing and buys 20 hit points.

AC 20 puts a robe caster level with a heavy-armour-and-shield body. It is still not what the
rung rests on:

- **Lone Wolf halves all damage**, doubling everything below it. It is **outside** the §3 ratio on
  both sides, because every chassis in the ledger has it — so it is real effective HP that the
  rung deliberately cannot see
- **The shield**, from character 1 — `p_hit` 0.60 → 0.50 at level 20
- **Eyebiter Resistance**, physical from character 4, **all damage from character 11** — Mesmerist
  10, which the ladder puts at character 11, not 17. It is the largest single term in the rung:
  halving the hit doubles the ratio, taking Act III from `2.00` to `3.99`
- **Potent Robe**: temporary HP equal to Charisma every turn
- **Battlemind Link**: +2 AC, immune to Flanked and Surprised, provokes no opportunity attacks
- **Constitution +13 with advantage** — concentration effectively does not break
- **Durable** from character 7: **full hit points on every short rest** — the cheap clock, on a
  chassis whose entire damage engine is at-will — plus regeneration below 60% inside the fight.
  Neither is in the pool below, and both matter most in Act I where the rung is weakest
- **Shield Master** from character 14: **−1 to every instance of damage taken**, and Block as a
  *passive* — the Rogue Evasion effect on failed Dexterity saves, spending no reaction, on a
  body whose two reactions were otherwise idle. The flat `−1` **is** in the pair sheets' §3 from
  Act II, and it moves no rung — Acts II and III were already at the ceiling **[data]**
- **Mage Slayer** from character 20: **−6 to every instance of spell damage**, on top of the
  halving and the resistance **[data]**

### The rest

> **The shield moves no rung, and the arithmetic is worth showing.** Run through §3 with the
> pair sheet's own authored pools:
>
> | act | pool ratio | AC | `p_hit` | resistance | ratio | rung |
> |---|---:|---:|---:|---:|---:|---:|
> | **I** | 1.26 (82 ÷ 65) | 15 → **17** | 0.75 → **0.65** | ×1.54 physical only | 1.68 → **1.94** | **4**, unchanged |
> | **II** | 1.63 (**188** ÷ 115) | 18 → **20** | 0.60 → **0.50** | ×1.82, plus Shield Master **−1** | **4.19** | **5** |
> | **III** | 1.46 (**233** ÷ 160) | 18 → **20** | 0.60 → **0.50** | ×2 all damage, plus **−1** | **3.99** | **5** |
>
> Act I clears 1.6 comfortably and never approaches the 2.4 rung-5 line — the Act I pool is small
> and the boon is physical-only until Mesmerist 10. Acts II and III were already at the ceiling.
> **Durability stays 4 / 5 / 5**; the two AC points are real eHP that the rung bands are too
> coarse to show.

**Actions 2/4/4.** Twinned Haste gives the pair four Actions a round for one metamagic pick and
three sorcery points. **It is live from character 16**, not 13 — Twinned is one of the two
metamagics at Sorcerer 2, but Haste is a 3rd-level spell and waits for Sorcerer 5.

**Control, single 4/5/6.** A permanent, free, no-concentration `−3` to a boss's Intelligence,
Wisdom and Charisma saves, its Constitution saves, its spell save DC and its AC — plus a
Constitution-save Blind every turn — plus Doom at `−6` on a 6th-level slot. This is the axis the
chassis is actually for.

**Control, area 1/3/4.** Mortal Reminder from character 8, near-certain from character 19.

**Rescue 1/1/2.** Nothing outward. Taking Eyebiter over Trickster gave up Touch Treatment, and
the partner reads Rescue 4 — which the rubric puts at *optional*, so this is a deliberate zero,
not an oversight.

**Skills 3/2/2 — rescored, and it fell two rungs.** The old `4/5/6` was built on Actor's four
Expertises and Skilled Expert's Religion, and the 6 was out of range for the axis besides
(`KIND_MAX` is 5 for a shared axis). What is left is **proficiency without Expertise anywhere**:
Persuasion, Perception and Insight from Mesmerist 1, Deception and Sleight of Hand from Charlatan,
Consummate Liar's half-Mesmerist-level on Deception, and **Astral Intuition's advantage on every
Intelligence check** — worth roughly `+3.3`, which is close to an Expertise this sheet did not pay
for. `scoring.py`'s `derive_skills` on the finished modifiers gives **3 / 2 / 2**:

| act | Persuasion | Deception | Perception | Investigation |
|---|---:|---:|---:|---:|
| **I** (char 8) | +9 | **+12** | +3 | +3 <span class="faint">adv</span> |
| **II** (char 15) | +11 | **+16** | +5 | +3 <span class="faint">adv</span> |
| **III** (char 20) | +13 | **+19** | +6 | +3 <span class="faint">adv</span> |

Deception carries the body — it is proficiency plus Consummate Liar, and it is what clears Hag's
Hair at DC 20. Everything else is a flat proficiency against DC bands that climb faster than the
proficiency bonus does. **The pair value is what the sheets report**, and it is computed on the
evidence rather than on these rungs: beside Coldsnap the pair reads **4 / 4 / 4**.

**Endurance 4/5/5.** The entire damage engine is **at-will cantrips with no resource behind
them**, and Hypnotic Stare, the Bold Stares and Painful Stare cost nothing at all. Sorcery
points and the pact slot are the only clocks, and neither carries the routine.

---

## Known weaknesses

1. **Act I is a hole.** 47.6 delivered against par 60 — rung 1. Before Potent Robe and Elemental
   Affinity, the beams are bare `1d8`. In Act I this body is a controller and a face, and the
   partner carries the fight. This is the direct cost of buying Sorcerer 6 and an Act II robe.

2. **AoE is narrow rather than absent.** Distributed beams plus the damage share of the slot pool
   reach rung 4 from Act II, but the build has no at-will true area spell and Act III sits only
   `0.02` below rung 5. Psychic resistance also removes the preferred beam type from the mix.

3. **Two Charisma stat lines if the partner is also Charisma.** Against Coldsnap (Wisdom) there
   is no contention at all. Against a Charisma carry, every Charisma item is contested at 4×
   merchant prices.

4. **The Stare dependency, not the AC.** The shield takes AC to **20** and Shield Master puts a
   passive Evasion and a flat `−1` under it, so AC is no longer the exposure. What is: the
   durability rung rests on the Resistance boon, which is conditional on a Stare being up —
   and a Stare cannot be applied to a target more than 9 m away, though it persists at any
   range once applied.

5. **~~Religion is bought with the last feat~~ — closed by the race.** Astral Intuition gives
   advantage on the check permanently, so the last feat no longer has to be spent on it. See the
   feat table.

6. **Strength saves are uncovered and stay uncovered.** `Resilient (Strength)` lost the last
   feat slot to Mage Slayer, which buys advantage on every *spell* save instead. Against a
   non-magical Strength effect this body has `−1` and nothing else.

7. **The face is proficiency-only.** Dropping Actor costs four Expertises and leaves Persuasion
   at `+13` post-Mirror against Act III checks reaching DC 30. Deception carries what it can
   via Consummate Liar; Intimidation and Performance are not proficient at all, and the
   partner is Charisma 8.

8. **Charisma 22 before Act III is `(unverified)`.** It rests on War Caster's ability picker
   clearing 20, which the paks cannot settle. If it refuses, the whole of Acts I and II run a
   modifier light. The Mirror closes it either way — but only from Act III.

---

## Open decisions and unverified items

- `(unverified)` **Whether Elemental Affinity's `DamageBonus` applies per beam or once per
  cast.** The pak reads
  `IF(IsSpell() and IsDamageTypePsychic()):DamageBonus(max(0, CharismaModifier))` **[pak]**,
  and BG3's Magic Missile precedent says per instance. **If it is once per cast instead, Act II
  and Act III single-target both fall a full rung** — this is the single largest load-bearing
  inference on the sheet.
- `(unverified)` **Whether Lone Wolf's halved damage and the Eyebiter Resistance boon multiply
  or share a cap.** The durability rung assumes they multiply.
- `(unverified)` **Whether the ability picker used by War Caster measures the base score or
  the boosted one.** `SelectAbilities` greys out anything at 20; Lone Wolf's `+4` is a status
  boost, so the base is 17 and the total is 21. **[pak]** Open its picker at character 3 —
  Charisma offered means the sheet runs at 22 from character 3, refused means 21 until the
  Mirror. Nothing else on the sheet depends on it.
- `(unverified)` **Shield proficiency by subrace inheritance**, which `Shield Master` now
  depends on as well as the AC line. Confirm it at character creation; if it is absent, AC
  reverts to 18 and the character-14 feat becomes `Mobile`.
- **Battlemind Link's radius.** The mod page says 3 m; `MESMERIST_BATTLEMINDLINK AuraRadius "6"`
  **[pak]**. The pak wins, and 6 m is the difference between a usable pair buff and a melee-only
  one.
- **Only one ring slot is locked.** The installed Critfisher Ring is crit threshold **−3**;
  Dreamweaver and the two threshold feats make Ring of Viciousness overkill in Act III. The
  second slot is a pair-dependent damage/control flex. Callous Glow belongs on Coldsnap in that
  pairing because its Radiant instance preserves Glaring Frost against Cold immunity, not because
  it would fail to add damage to Fixation.
- **Race is settled: Astral Half-Elf**, and one thing downstream now keys off it — the shield
  proficiency in the AC line. The `(unverified)` subrace-inheritance caveat is in the race
  section. Darkvision is redundant from Mesmerist 9 either way.
