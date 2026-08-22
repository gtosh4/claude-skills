# Lectern v2 — Snowlight 15 / Friar 3 / Light 2

**Ranger 15 (Snowlight Conclave) / Monk 3 (Way of the Friar) / Cleric 2 (Light)** — level 20,
Lone Wolf duo. A control chassis that converts *being attacked* into mass Blindness, then taxes
every action the blinded enemy takes.

Every mechanic marked **[pak]** was read out of the installed archive with
`skills/listo-build/scripts/lspk.py`, not from mod pages or the Listo docs.

---

## The engine

1. **Friar's Bond**, Retribution blessing, up permanently. **[pak]**
   ```
   FriarRetribution   StatsFunctorContext "OnAttacked"
                      Conditions "IsAttack() and Self(context.Target) and IsHit();"
                      StatsFunctors "DealDamage(SWAP, 2*Cause.WisdomModifier, Radiant, Magical)"
   ```
   `SWAP` makes **you** the source. No ki, no reaction, **no cooldown** — every attack that hits
   you reflects `2 × WIS` Radiant. At WIS 22 that is **12 per incoming hit**, credited to you.

   `Interrupt_FriarRetribution` covers your Kin: reaction, `DealDamage(OBSERVER_SOURCE, 2*WIS,
   Radiant, Magical)` when a bonded ally is hit. Lone Wolf grants two reactions, so two more
   procs a round.

2. **Glaring Frost** turns each instance into a save. **[pak]**
   ```
   Glaring_Frost  StatsFunctorContext "OnDamage"
                  Conditions "(HasDamageDoneForType(Cold) or HasDamageDoneForType(Radiant)) and not Item();"
                  StatsFunctors "IF(not SavingThrow(Ability.Constitution, SourceSpellDC())):ApplyStatus(BLINDED, 100, 2)"
   ```
   `Item()` is a **target** predicate — "the target is not a crate." Confirmed by contrast: every
   other `Item()` in these paks sits in `TargetConditions` / `AoEConditions` beside `not Dead()`
   and `not Self()`, and when the same authors want a source-side check they use a different
   function, `not AnyEntityIsItem()` (five uses in `Interrupt.txt`). **Weapon and item-borne
   Cold/Radiant trigger Glaring Frost normally.**

3. **Snow Blindness** (Ranger 11) taxes the blinded. **[pak]**
   ```
   Snowblindness  StatsFunctorContext "OnStatusApply"  Conditions "StatusId('BLINDED');"
                  StatsFunctors "ApplyStatus(Snowblind, 100, 2);"
   Snowblind_DMG  StatsFunctorContext "OnCast"
                  Conditions "(HasUseCosts('ActionPoint') or HasUseCosts('BonusActionPoint') or HasUseCosts('ReactionActionPoint'));"
                  StatsFunctors "DealDamage(SELF, 1d6, Radiant, Magical);"
   ```
   1d6 Radiant per Action, Bonus Action *and* Reaction the blinded creature spends, plus an
   end-of-turn tick. That damage is dealt by the blinded creature to itself, so it does **not**
   re-proc Glaring Frost — no loop.

4. **Snowborn Anthelion** (Ranger 15) makes every proc an area effect. **[pak]**
   ```
   Projectile_Anthelion_Explosion
     ExplodeRadius 3
     SpellRoll "not SavingThrow(Ability.Constitution, SourceSpellDC())"
     SpellSuccess "ApplyStatus(BLINDED, 100, 2);"
     TargetConditions "not Item() and not Self() and not Ally() and not Dead()"
   ```
   A real CON save and a real 2-turn Blind in 3 m, **excluding self and allies**. Every Cold or
   Radiant instance you deal now blankets a cluster.

5. **Cleric 2 (Light)** supplies the proactive trigger the loop otherwise lacks — Retribution is
   `OnAttacked`, so round one it is cold. **Word of Radiance** is an at-will AoE Radiant cantrip
   around you; each enemy it damages eats a Glaring Frost save *and* an Anthelion detonation, on
   your turn, on demand, for no resource. **Radiance of the Dawn** (Channel Divinity, short rest)
   is the same chain at a larger radius, and being save-for-half it deals damage — and therefore
   triggers — on every target regardless of their save.

**Every DC in the build is `8 + PB + WIS`** — Ranger, Cleric and the Ki Save DC all key off
Wisdom, so one stat drives the Glaring Frost save, the Anthelion save, the reflect damage,
Unarmoured Defence and Friar's Grace range.

---

## Chassis

| class | levels | subclass | what it is here for |
|---|---|---|---|
| Ranger | 15 | Snowlight Conclave | Glaring Frost (3), Extra Attack (5), Snow Blindness (11), **Snowborn Anthelion (15)** |
| Monk | 3 | Way of the Friar | Friar's Bond + **Retribution**, Guardian of Light (shield + Unarmoured Defence + concentration advantage), Friar's Grace, Deflect Missiles |
| Cleric | 2 | Light | Word of Radiance, Radiance of the Dawn, Sacred Flame |

Monk stops at 3: Monk 5's Extra Attack duplicates Ranger 5, and Monk 3 already delivers the whole
engine feat-neutrally. Ranger stops at 15 because Anthelion is the last thing that multiplies the
gimmick — 16 and 17 buy Cone of Cold and 5th-level slots, the live alternative to this Cleric dip
(see *Open decisions*).

**Level-1 class: Ranger** — STR + DEX saves, 3 skills, martial weapons, medium armour, shields.

---

## Stats

WIS 22 route: **16** after the racial bonus at creation → Lone Wolf **+4** → 20 → **Enweaved**
half-feat +2 → **22** (Enweaved's own cap).

Lone Wolf grants **+4 to two abilities and save proficiency in both**, plus +30% max HP, halved
damage from all sources, and a second Action / Bonus Action / Reaction.

| | **Line B — recommended** | Line A |
|---|---|---|
| DEX / WIS / CON | 16 / 22 / **20** | **20** / 22 / 14–16 |
| Lone Wolf +4 | WIS + **CON** | WIS + DEX |
| Save profs | STR, DEX, WIS, CON — **4 disjoint, all three key saves** → rung **4** | STR, DEX, WIS — 3 disjoint → rung **2** |
| Bond concentration | CON proficient, CON 20 → **+11, with advantage** | no CON prof; shield advantage only |
| AC (Unarmoured + shield) | 21 | 23 |
| Initiative | +3 | +5 |
| Weapon | Shillelagh trident (WIS) | rapier (DEX) |
| Fighting style | **Druidic Warrior** | **Duelling** |
| Extra feats needed | none | War Caster *or* Resilient (CON) |

Line B trades 2 AC and 2 initiative for a save rung, CON-proficient concentration on the ability
the whole build depends on, a much larger HP pool, and ~1.5 feats (DEX 20 without Lone Wolf costs
the ASI feat plus a half-feat). **Lone Wolf already halves all incoming damage, and Retribution
wants attacks to land** — AC is the cheapest thing here to give up. Fix the initiative gap with
`Alert`, not with DEX.

Per-hit damage is a wash either way: Shillelagh trident is 1d8 + 6 at +12; rapier + Duelling is
1d8 + 5 + 2 at +11. Hit-weighted, 45.2 vs 46.0 a round.

---

## Fighting style and weapon

**Line B — Druidic Warrior** (UA Fighting Styles; confirmed on the Ranger list **[pak]**):
```
PassiveList  Name "AddTo_Ranger"
  Passives "...,UA_FightingStyle_DruidicWarrior,..."
UA_FightingStyle_DruidicWarrior
  Boosts "UnlockSpell(Shout_Shillelagh,,,,Wisdom);UnlockSpell(Target_Guidance,,,,Charisma)"
```
Shillelagh **hard-locked to Wisdom**, no feat, no Druid dip. In Listo it is a **level 1 spell**,
not a cantrip: costs a slot and a prepared slot, lasts **until Long Rest**.

**Use a trident.** Listo's Shillelagh list is Club / Quarterstaff / Mace / Morningstar / Sickle /
Spear / Trident. Trident and Morningstar are **martial**, so they are not monk weapons, so Monk's
Martial Arts *Dextrous Attacks* cannot contest the ability override. The five simple weapons on
that list all can — and the data files disagree about whether it wins (`druid.md:68` says Dextrous
Attacks overrides Shillelagh outright; `monk.md:435` calls it `(unverified)`). Dodge the question
rather than test it. Trident is versatile, so one-handed alongside the shield.

**A shield is mandatory** — Guardian of Light keeps Unarmoured Defence working with one equipped
and grants **advantage on Concentration checks**, the second half of protecting Bond.

---

## Feats — seven

Cadence is per **class level**, 3 / 6 / 9 / 12 / 13 / 15 / 18: Ranger 3, 6, 9, 12, 13, 15 (six) +
Monk 3 (one). Cleric 2 contributes none.

1. **Enweaved** — +2 WIS, the only route from 20 to 22. Mandatory.
2. **Alert** — the one unaddressed weakness is going second.
3. **Savage Attacker** — `2473` extends the reroll to unarmed strikes; you make a lot of rolls.
4. **Magic Initiate: Druid** — 2 druid cantrips + 1 L1. Take **Frostbite** (Cold, CON save) and
   **Moonflare** (Radiant) for two at-will triggers at range, where Word of Radiance cannot reach.
5. **Tough** — more HP is more rounds of the engine running.
6–7. Free. `Dungeon Delver` / `Performer` carry +1 DEX or WIS plus real expertise, and a
two-person party needs the skills. On **Line A**, one of these is spent on War Caster or
Resilient (CON) instead.

`Arcanist` is **removed** from Listo — do not plan around it, whatever `monk.md:433` says.

---

## Concentration budget

Friar's Bond holds the **only** concentration slot, permanently. That rules out Hunter's Mark,
Blinding Smite, Greater Invisibility, Conjure Animals and Elemental Weapon. Accept it — Bond is
the engine.

Mitigation: shield + Guardian of Light (advantage) and, on Line B, CON proficiency at +11.

Free control that costs no concentration: **Favored Foe** (bonus action, no slot), Glaring Frost,
Anthelion, Snow Blindness.

---

## Spells and cantrips

- **Cleric cantrips:** Word of Radiance, Sacred Flame *(ranged single-target Radiant proc for when
  nothing is in melee)*. Guidance is already free from Guardian of Light.
- **Snowlight subclass spells:** Armour of Agathys (3), Blindness (5), Blinding Smite (9),
  Greater Invisibility (13) — the last two are concentration and therefore dead.
- **Ranger:** Revivify reaches the Ranger at spell level 3 (class 9); take it. Cure Wounds and
  Lesser Restoration for the Rescue floor.

---

## Progression order

| char | take | unlocks |
|---|---|---|
| 1–3 | Ranger 1–3 | saves, fighting style, **Glaring Frost**, feat |
| 4–6 | Monk 1–3 | Unarmoured Defence, **Friar's Bond + Retribution**, shield, feat |
| 7–8 | Ranger 4–5 | **Extra Attack** — four attacks a round with Lone Wolf |
| 9–14 | Ranger 6–11 | Behind the Sun (7), Revivify (9), **Snow Blindness** (11) |
| 15–16 | Cleric 1–2 | **Word of Radiance**, **Radiance of the Dawn** |
| 17–20 | Ranger 12–15 | **Snowborn Anthelion** (15) |

Both halves of the core loop are online by character 6. Swap the Cleric block earlier if Act I
feels thin on area damage — it costs Anthelion nothing, only delays it within Act III.

---

## Scores

Rubric: `skills/listo-build/references/axis-rubrics.md`. §1 and §2 computed against par
(single-target 48 / 61 / 76, AoE 22 / 28 / 32); the rest act-relative.

| axis | I | II | III |
|---|---|---|---|
| Single-target | 2 | 2 | 2 |
| AoE | 1 | 2 | **4** |
| Durability | 4 | 3 | 3 |
| Actions | 3 | 3 | 3 |
| Control (single) | 3 | 4 | 4 |
| Control (area) | 2 | 3 | **4** |
| Rescue | 4 | 4 | 4 |
| Skills | 3 | 3 | 3 |
| Saves | **4** | **4** | **4** |
| Endurance | 4 | **5** | **5** |

*Single III:* 42 (4 × 1d8+WIS) + Favored Foe 4.5 + Flurry amortised 8 + Snowblind ticks ~7 +
reflect on the boss ~12 ≈ 74 vs par 76 → 0.97 → rung 2.

*AoE III:* reflect ~50 × 0.75 (Act II+ Radiant resistance) = 38, plus Snow Blindness at near-total
blind uptime, 4 × 10.5 × 0.75 = 31 ≈ 69 vs par 32 → 2.1 → rung 4.

Endurance is 5 because **the entire control engine costs nothing** — no slot, no ki, no action,
no reaction. Saves is 4 on Line B only.

---

## Known weaknesses

- **Single-target is flat 2 in every act.** This never threatens a boss on damage.
- **Blind is a CON save.** Brutes and undead resist it, and a blinded caster still casts —
  Blindness in BG3 only imposes attack disadvantage and grants advantage against.
- **AoE is thin until Cleric 2 lands**, and only peaks at Ranger 15.
- **Retribution fires on `IsAttack() and IsHit()` only.** Enemy spells and save-based damage feed
  it nothing.
- **The loop partly suppresses itself** — blinded enemies attack at disadvantage, so they hit you
  less, so they proc Retribution less.
- **Warding Flare is anti-synergistic.** Disadvantage on an attack against you is a hit you did
  not convert into 12 Radiant and a blind save. Spend it on genuinely dangerous attacks only.

---

## Open decisions and unverified items

- **Cleric 2 (Light) vs Ranger 16–17.** Ranger 17 buys **Cone of Cold** (8d6 Cold, ranged, no
  concentration, 5th-level slot) plus 5th-level slots. Every other trigger in this build is
  melee-range, Word of Radiance included, so Cone of Cold covers the one gap the Cleric dip does
  not. It is close. This document takes the Cleric.
- **Shillelagh's damage die in Listo** is `(unverified)`; the changelog's Dryad comparison implies
  1d8 + WIS.
- **Whether Dextrous Attacks overrides Shillelagh** is `(unverified)` and the data files
  contradict each other. The trident sidesteps it.
- **Whether Word of Radiance is save-negates or save-for-half** in Listo's implementation is
  `(unverified)` — its stats entry was not locatable in the installed paks. 5e default is
  save-negates, meaning a successful CON save yields no damage and therefore no proc.
- **`FriarValor`'s level map** reads 1d4 (1–8) / 1d6 (9–16) / 1d8 (17+) **[pak]**; whether it keys
  off Monk level or character level is `(unverified)`. Irrelevant while Retribution is chosen.
- **`Snowborn_Anthelion`'s condition has an operator-precedence quirk** — `Radiant or (Cold and
  not Item)`, since `and` binds tighter. Harmless given `Item()` is target-side, but it is what
  ships.
