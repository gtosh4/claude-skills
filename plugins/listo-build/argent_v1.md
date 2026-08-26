# Argent v1 — Moon 14 / Champion 3 / Hexblade 3

**Paladin 14 (Oath of the Moon) / Fighter 3 (Champion) / Warlock 3 (The Hexblade)** — level 20,
Lone Wolf duo partner for **Lectern v2**. A Charisma greatsword that converts Lectern's mass
Blindness into critical hits and smites, and pays for the smites on a short-rest clock.

Every mechanic marked **[pak]** was read out of the installed Listonomicon 10.2 archive with
`skills/listo-build/scripts/lspk.py`. **[data]** is confirmed in the repository's compiled 10.2
snapshot. Vanilla mechanics whose base-game paks are not under the mods root are named as such.

---

## The paired engine

1. **Lectern supplies the advantage; Argent converts it to criticals.** Glaring Frost and
   Snowborn Anthelion turn Lectern's Cold/Radiant into two-turn Blind, and attacks against a
   blinded creature have Advantage. Argent never buys an advantage source of its own — no Vow of
   Enmity, no Reckless Attack — and spends the whole budget on **crit threshold** and **per-hit
   riders** instead.

   With Champion's Improved Critical **and** Hexblade's Curse both at 19, Advantage gives
   `1 − (18/20)² = 19%` per swing. Across 5.2 swings that is **0.99 criticals a round**.

2. **Great Weapon Master's bonus attack is untouched by Listo's rebalance. [data]** The nerf
   landed entirely on All In; the *"on a critical hit or kill, make another melee weapon attack
   as a bonus action"* half is vanilla. At a 19% crit rate that fires **57% of rounds** before
   kills are counted.

   > **Leave All In toggled off.** At PB 6 it is +11 damage for −6 to hit. Against AC 22 at +15
   > with Advantage, hit rate falls `0.91 → 0.64` for a 35% bigger hit: `0.64 × 42 = 26.9`
   > against `0.91 × 31 = 28.2`. Net negative, and it costs Improved Divine Smite procs too.

3. **Savage Attacker is the highest-value feat on this chassis, because the melee packet is the
   fattest in the list. [data]** The installed passive is `Reroll(MeleeWeaponDamage,20,false)` —
   every eligible die rerolled, keep higher, **on every attack**, not once per turn — and it is
   not limited to the weapon die: it covers **smite dice** explicitly.

   | die | plain | +GWF | +GWF +Savage Attacker |
   |---|---|---|---|
   | d6 (greatsword) | 3.50 | 4.00 | **4.61** |
   | d8 (Divine Smite) | 4.50 | — | **5.81** |

   On a smited critical the packet is `8d6 + 12d8` after doubling — twenty rerolled dice.

4. **Pact of the Blade solves the MAD, and Hexblade's Curse pays for itself. [data]**
   Pact of the Blade *"summons or binds a weapon; it uses your Spellcasting Ability instead of
   Str/Dex"* — and unlike 5e's Hex Warrior it has no Two-Handed restriction, so it binds a
   greatsword to Charisma. Hexblade's Curse adds **+PB damage** against the cursed target, drops
   its crit threshold to 19, and heals on the kill, for one bonus action per short rest.

5. **Two pact slots per short rest are two extra Divine Smites per fight.** Warlock slots fuel
   Divine Smite, and they refill twice per long-rest cycle. In a pack where a long rest costs
   120+ supplies and Listo allows only two short rests, that is the whole Endurance argument.

---

## What the Listo patch actually ships — read this before trusting the mod page

`[cust] MoonOath_ListoPatch` overrides the Oath of the Moon mod's own values. **Both of the
oath's headline defensive features are cut.** **[pak]**

```text
AURA_OF_MOONLIGHT                                    (Listo patch)
  AuraRadius  "3"
  Boosts "DamageReduction(Bludgeoning,Flat, Cause.CharismaModifier/2);
          DamageReduction(Piercing,Flat, Cause.CharismaModifier/2);
          DamageReduction(Slashing,Flat, Cause.CharismaModifier/2);"

MOONOATH_SILVEREDREBUKE_DAMAGE                       (Listo patch)
  OnApplyRoll    "not SavingThrow(Ability.Wisdom, SourceSpellDC())"
  OnApplySuccess "DealDamage(2*Cause.CharismaModifier, Radiant,Magical)"
```

| | base mod | **as installed** |
|---|---|---|
| Aura of Moonlight | CHA mod, **all** damage types | **½ CHA mod, Bludgeoning / Piercing / Slashing only** — 3 at CHA 22 |
| Aura radius | 3m, 9m at 18 | **3m** until the `_2` tier |
| Silvered Rebuke | `Level + CHA mod` = 26 at 20 | **`2 × CHA mod`** = 12 |

Three consequences, and they decided this build:

- **Heavy Armour Master is the bigger mitigation layer, not the aura.** PB capped at 5, *all*
  damage, magical included, and Listo's version also grants +1 STR or CON. **[data]**
- **The aura is a 3m tether.** Lectern collects it only while standing adjacent. It is real —
  see the eHP working — but it is not a party-wide blanket.
- **Silvered Rebuke is not worth three Paladin levels at 12 damage a proc.** That is why this
  build stops the oath at 14 and spends the rest elsewhere. A Paladin 17 variant was scored and
  lost.

Two features the patch leaves intact and this build does lean on: **Full Moon** — Bonus Action
plus one Channel Oath, **9m**, Wisdom save or Blinded 2 turns **[pak]** — a second save axis
beside Lectern's Constitution-save blind; and **Fount of Moonlight**.

```text
Shout_MoonOath_FountOfMoonlight
  Level "4"   UseCosts "ActionPoint:1;SpellSlotsGroup:1:1:4;"
  SpellFlags "...;IsConcentration;IsSpell"     AuraRadius "18"
MoonOath_FountOfMoonlight_Radiant
  Properties "IsHidden;OncePerAttack"   StatsFunctorContext "OnAttack"
  Conditions "IsMeleeAttack() and not IsMiss();"
  StatsFunctors "DealDamage(2d6, Radiant,Magical)"
```

**+2d6 Radiant on every melee hit for ten turns, on one 4th-level slot** — the best per-hit
rider available at any price, and the reason the oath goes to 13. It is **concentration**, and
it is the only concentration this build holds.

> **`(unverified)` Savage Attacker probably does not touch it.** Fount of Moonlight and Improved
> Divine Smite are separate `OnAttack` functors, not dice folded into the weapon packet, and the
> feat's own scope note excludes *"an independent spell damage roll … not part of the melee packet
> merely because the weapon hit caused it."* Every number below assumes **no** reroll and **no**
> crit-doubling on those two. If they do double, this build is stronger than scored.

**Fount of Moonlight and Spirit Guardians compete.** Both are concentration; the oath grants
Spirit Guardians at Paladin 9. Fount for a boss, Spirit Guardians for a crowd — and Spirit
Guardians is this body's **only** area damage in the entire run.

---

## Per-hit riders, priced per level spent

The currency of this chassis. This table is why the oath stops at 14 and why Warlock is the dip.

| rider | per hit | levels | per level |
|---|---|---|---|
| **Fount of Moonlight** (Paladin 13) | 2d6 = **7.0** | 2 | **3.50** |
| **Hexblade's Curse** (Warlock 3) | +PB = **6.0** | 3 | **2.00** |
| Crimson Rite (Blood Hunter 2) | 1d4 = 2.5 | 2 | 1.25 |
| **Improved Divine Smite** (Paladin 11) | 1d8 = **4.5** | 4 | **1.13** |
| Rage damage (Barbarian 9) | +3 flat | 9 | 0.33 |

Improved Divine Smite is not the stopping point; it is what you pass through on the way to Fount
of Moonlight, and Paladin 12 and 13 each carry a feat on top.

---

## Chassis

| class | levels | subclass | what it is here for |
|---|---|---|---|
| Paladin | 14 | **Oath of the Moon** | Extra Attack (5), Aura of Protection (6), Aura of Moonlight (7), Spirit Guardians (9), Improved Divine Smite (11), **Fount of Moonlight (13)**, Full Moon / Punish the Wicked / Divine Guardian (3) |
| Warlock | 3 | **The Hexblade** | **Pact of the Blade** (Charisma greatsword), Hexblade's Curse, **2 pact slots per short rest**, Eldritch Blast, 2 invocations |
| Fighter | 3 | **Champion** | Action Surge, **Improved Critical (19)**, a second Fighting Style, Second Wind |

**Level-1 class: Paladin.** Wisdom + Charisma saves and heavy armour. Both are lost if Paladin is
not first — and **the Fighter multiclass node grants neither heavy armour nor saves** **[data]**,
so opening Fighter buys nothing this build cannot get from Paladin 1.

Paladin stops at 14 because 15 buys a 12-damage Silvered Rebuke and 17 buys Hold Monster and Mass
Cure Wounds — three levels for one boss-fight spell, against three levels that buy a per-hit
rider, a crit range and a short-rest resource. Warlock stops at 3 because Pact of the Blade's own
Extra Attack duplicates Paladin 5.

---

## Stats — two lines and one respec

**The build swings Strength for the whole of Act I and Charisma from Warlock 3 onward.** Respec
re-picks the ability spread, the Lone Wolf pair and the class order, so the level-1 line does not
have to be a prefix of the level-20 one. Before Warlock 3 there is no way to put Charisma on a
greatsword; keeping Strength until then is free damage.

| | **Act I — Strength line** | **Acts II–III — Charisma line** |
|---|---|---|
| Lone Wolf +4 | **STR + CON** | **CHA + CON** |
| STR / CHA / CON | 20 / 14 / 20 | 10 / 20→22 / 20 |
| Save proficiencies | Str, Con, **Wis, Cha** — 4 disjoint | Wis, Cha, Con — **3 disjoint** (Cha duplicated) |
| Aura of Moonlight | 1 | 2 → **3** |
| Spell save DC at PB 6 | — | **20** |
| Weapon ability | Strength | **Charisma**, via Pact of the Blade |

**Charisma to 22:** 16 at creation → Lone Wolf **+4** → 20 → **Mirror of Loss +2** → 22 (Act III;
the Mirror also grants a separate +1 Charisma, so 23 is reachable). Buy Charisma to exactly 16
after the racial bonus on the rebuild — 17 wastes a point against Lone Wolf's cap of 20.

**The Charisma tax, stated exactly.** Lone Wolf's +4 pair has to cover the attack stat. On
Strength that pair is STR + CON and Paladin 1's Wis + Cha completes **four disjoint saves for
free**. On Charisma the attack stat duplicates a save the class already granted, so you choose
between four disjoint saves and Constitution 20 — not both. This build takes **Constitution 20**
and buys the fourth save back with **Resilient (Dexterity)** at Paladin 13.

**The Potion of Everlasting Vigour is dead weight here. [pak]** `Better Potion of Everlasting
Vigour` reads *"Permanently increase the **Strength** of everyone in your party and camp by 2"* —
Strength only, party-wide, and this body is Charisma by the time it lands in Act II. It is free,
so it costs nothing; it is simply an argument for a route this build did not take.

**Hag's Hair must go on Charisma or Constitution — never Strength.** It is Act I, one per run,
permanent, and it **survives respec**, so a point placed on the Act I Strength line is stranded
forever. This is the single irreversible decision in the ladder.

---

## Weapon, armour and fighting styles

**Greatsword, two-handed, no shield.** `2d6`, and Listo's **Great Weapon Fighting (PHB2024)**
sets the minimum die result to **3** **[data]**, which is worth more than vanilla's reroll-1s-and-2s
and stacks with Savage Attacker: `3.50 → 4.00 → 4.61` per die.

Two Fighting Styles: **Great Weapon Fighting** at Paladin 2, **Defence** at Fighter 1.

**Heavy armour throughout** — plate, no Dexterity contribution, AC 18 base rising to 21 with Act
III enchantment. Giving up a shield is what a two-handed weapon costs; Heavy Armour Master is
what buys it back.

---

## Feats — seven

Cadence is per **class level**: Paladin 3, 6, 9, 12, 13 (five) + Warlock 3 (one) + Fighter 3 (one).

1. **Savage Attacker** — see above. The single highest-value feat on this chassis.
2. **Great Weapon Master** — for the bonus attack on crit or kill. All In stays off.
3. **Heavy Armour Master** — PB capped at 5, all damage, magical included, **+1 STR or CON**.
   Requires heavy armour proficiency, which Paladin 1 supplies. **[data]**
4. **Resilient (Dexterity)** — the fourth disjoint save, and the one covering the third of the
   three key abilities. Personal axis; Lectern cannot cover it.
5. **Alert** — going second in a duo is how a fight is lost before it starts.
6. **Skilled Expert** — a proficiency, an Expertise and +1 Charisma, for one feat. This is what
   makes Argent the party face; Lectern sits at Skills 3 all run.
7. **Tough** — free. More rounds of the engine running.

`Arcanist` is **removed** from Listo. Do not plan around it.

---

## Invocations — two, at Warlock 2

- **Agonizing Blast** — Eldritch Blast is the only ranged attack this body owns.
- **Beguiling Influence** (Deception + Persuasion) *or* **Leaps and Bounds** (Acrobatics +
  Athletics). Deception is the **Hag's Hair** gate and it is a Charisma check, which no other
  member of this pair can pass — take Beguiling Influence unless the hair is already banked.

---

## Progression ladder

Holdings at each character level, not a purchase order. **Rung 12 is a respec.**

| char | hold | what comes online |
|---|---|---|
| 1–2 | Paladin 1–2 | Wis + Cha saves, heavy armour, **Great Weapon Fighting**, Divine Smite |
| 3 | Paladin 3 | oath: **Full Moon**, Punish the Wicked, Divine Guardian, Lunar Smite · feat **Savage Attacker** |
| 4–5 | Paladin 5 | **Extra Attack** — four swings a round under Lone Wolf |
| 6–7 | Paladin 7 | **Aura of Protection**, **Aura of Moonlight** · feat **Great Weapon Master** |
| 8–9 | Paladin 9 | **Spirit Guardians** — the only area damage in the build · feat **Heavy Armour Master** |
| 10–11 | Paladin 9 / Warlock 2 | Hexblade's Curse, Eldritch Blast, invocations. **Two martially dead levels — this is the real price of the plan** |
| **12** | Paladin 9 / **Warlock 3** | **Pact of the Blade. RESPEC: re-pick the spread as Charisma-primary, Lone Wolf to Cha + Con.** feat **Skilled Expert** |
| 13–15 | Paladin 9 / Warlock 3 / **Fighter 3** | **Action Surge**, **Improved Critical (19)**, Defence, Second Wind · feat **Tough** |
| 16–17 | Paladin 11 | **Improved Divine Smite** |
| 18–19 | Paladin 13 | **Fount of Moonlight** · feats **Alert**, **Resilient (Dexterity)** |
| 20 | Paladin 14 | Cleansing Touch |

**Take Warlock last in the rebuild order at rung 12.** Illithid power save DCs key off the
spellcasting modifier of the **last class added**; with Warlock last that is Charisma 20–22. If
Fighter ends up last, every save-based power on this body reads off nothing.

Act III's scored row is the **character 20** configuration. Fount of Moonlight does not land until
19, so the first half of Act III runs a materially thinner routine than the table below.

---

## Scores

Rubric: `skills/listo-build/references/axis-rubrics.md`; §1–§3 computed by `scripts/scoring.py`
against par (single-target **60 / 87 / 123**, AoE **48 / 65 / 82**, eHP pool **65 / 115 / 160**),
with the act's per-instance gear constant on both sides.

| axis | I | II | III |
|---|---|---|---|
| Single-target | 4 | **5** | **5** |
| AoE | **0** | 2 | 2 |
| Durability | 4 | **5** | **5** |
| Actions | 1 | 2 | 2 |
| Control (single) | 2 | 3 | 3 |
| Control (area) | 3 | 3 | 3 |
| Rescue | 3 | 4 | 4 |
| Skills | 2 | 3 | 3 |
| Saves | 4 | 3 | 4 |
| Endurance | 3 | 4 | 4 |

### Single-target, worked

`mult.st = 1.19`. Lectern's blind is **tier 1** — save-gated — and `pair-schema.md` names
Snowlight's blind engine as the exemplar. Tier 2's 1.35 is for a no-save, no-concentration source
and does not apply. Effectively all of this body's raw is attack rolls, so it takes the full tier.

| act | routine | raw | inst | +gear | ×1.19 | /par | rung |
|---|---|---|---|---|---|---|---|
| **I** | Paladin 7, **Strength 20**. 4 swings + 0.4 GWM. `2d6 GWF+SA 9.22 + 5`. Smites 2.33/fight | 74.7 | 4.40 | 87.9 | **104.6** | 1.74 | **4** |
| **II** | Paladin 9 / Warlock 3, **Charisma 20**. `9.22 + 5 + 6 Curse`; crit 19 → 4.6 swings. 3 paladin smites **+ 2 pact** | 122.9 | 4.60 | 145.9 | **173.6** | 2.00 | **5** |
| **III** | Full chassis, **Charisma 22**. `9.22 + 6 + 4.5 ImpDS + 7 Fount + 6 Curse = 32.72` × 5.2 swings; crit dice 9.1; smites 22.2 | 201.5 | 5.20 | 243.1 | **289.3** | 2.35 | **5** |

Act III's 5.2 swings: 4 from Extra Attack under two Actions, +0.7 for the GWM bonus attack at a
19% crit rate, +0.5 for one Action Surge amortised over four rounds.

### AoE, worked

Spirit Guardians only, at `3d8` upcast to 4th, Wisdom save for half (×0.71), about 3.5 enemies.

| act | raw | inst | +gear | /par | rung |
|---|---|---|---|---|---|
| I | 0 | 0 | 0 | 0.00 | **0** |
| II | 33.6 | 3.50 | 51.1 | 0.79 | 2 |
| III | 40.0 | 3.50 | 68.0 | 0.83 | 2 |

No accuracy multiplier: it is a saving throw, not an attack roll.

### Durability, worked

`pool ÷ par × accuracy × flat-mitigation`, blended on each act's crowd/boss mix. **The aura is
authored at roughly 0.7 of its nominal value** because the Listo patch restricts it to
Bludgeoning / Piercing / Slashing.

| act | pool | AC | acc | flat | crowd | boss | eHP | ratio | rung |
|---|---|---|---|---|---|---|---|---|---|
| I | 93 | 18 | ×1.08 | aura 1 | `5.4−1` ×1.23 | `16.3−1` ×1.07 | **119** | 1.83 | **4** |
| II | 148 | 20 | ×1.30 | HAM 4 + aura 1 | `9.6−5` ×2.09 | `28.8−5` ×1.21 | **334** | 2.90 | **5** |
| III | 252 | 21 | ×1.44 | HAM 5 + aura 2 | `13.3−7` ×2.11 | `40.0−7` ×1.21 | **605** | 3.78 | **5** |

Pool is `10 + 16×6` on d10 hit dice plus `3×5` on Warlock's d8, plus Constitution 20 across 20
levels — **221** at level 20 — plus **Lay on Hands spent on yourself** (70 per long rest ÷ 3
fights = 23) and **Second Wind** (8.5, short rest). Lay on Hands aimed at Lectern is Rescue and is
counted there instead; nothing is scored on both.

Flat reduction is multiplicative against small hits, which is why the crowd column runs at ×2.1
while the boss column sits at ×1.21. **Heavy Armour Master is doing most of that work.**

### The rest

**Saves 4 / 3 / 4.** Act I is the Strength line's four disjoint (Str, Con, Wis, Cha) plus Aura of
Protection. Act II drops to three when the respec puts Lone Wolf on Cha + Con and Charisma
duplicates Paladin's own grant. Resilient (Dexterity) at rung 18–19 restores four, and covers
Dexterity — the one of Wis/Con/Dex the Strength line never had.

**Endurance 3 / 4 / 4.** Act I is long-rest smite slots and nothing else. From Warlock 3 the body
adds two pact slots that refill on **both** short rests — six extra smites per long-rest cycle —
plus Second Wind and at-will Eldritch Blast.

**Skills 2 / 3 / 3.** Two Paladin proficiencies until the respec; Charisma 22 plus Skilled Expert
plus an invocation makes this the party face from Act II.

**Rescue 3 / 4 / 4** — Lay on Hands aimed outward, **Warding Bond** (the only Paladin route to it
in the list is this oath **[pak]**), and **Divine Guardian**, a Channel Oath that halves all
damage to Lectern for ten turns. Lectern already reads Rescue 4, so this is surplus rather than a
requirement.

---

## Known weaknesses

- **AoE is 0 in Act I and 2 thereafter, and that is the pairing's real hole.** Lectern's own Act I
  AoE is 1. Neither body clears an Act I crowd with damage — the pair controls it (Full Moon on a
  Wisdom save, Lectern's blind on a Constitution save) and then kills things one at a time. Slow,
  and it is 70% of Act I's encounters.
- **Two dead levels at characters 10–11.** Warlock 1–2 give this body nothing martial, and they
  land in the middle of Act II.
- **One concentration slot, and Fount of Moonlight owns it.** No Spirit Guardians while it is up,
  and no Haste, Warding Bond upkeep aside.
- **The aura is a 3m tether.** Lectern only collects the damage reduction standing adjacent, which
  is not where a Word of Radiance body always wants to be.
- **Blind suppresses its own supply.** Blinded enemies attack at disadvantage, so they hit Lectern
  less, so Lectern's Retribution fires less. Full Moon makes this worse. The pair trades
  Retribution uptime for a second save axis.
- **No shield, ever.** Two-handed weapon. AC caps around 21.
- **Charisma save duplication** costs a proficiency for six levels until Resilient lands.

---

## Open decisions and unverified items

- **`(unverified)` Whether Savage Attacker rerolls Fount of Moonlight and Improved Divine Smite.**
  Both are separate `OnAttack` functors. Scored as **no**. Check whether a reroll animation fires
  on those dice in game.
- **`(unverified)` Whether Hexblade's Curse and Champion's Improved Critical stack**, or both
  simply set the threshold to 19. Scored as **no stack**. If they stack, crit range is 18–20 and
  every damage figure here rises.
- **`(unverified)` Whether Great Weapon Fighting's minimum-3 applies before or after Savage
  Attacker's reroll.** Identical result for a d6 either way; stated for completeness.
- **`(unverified)` Whether Listo's global aura patch reaches Oath of the Moon.** The `_2` status
  at 9m exists in the patch pak **[pak]**, keyed to the oath's own level-18 tier, which this build
  does not reach. Assume **3m all run**.
- **Fount of Moonlight vs Spirit Guardians** is a per-fight call, not a build decision. Rule 3
  scores the slot on both axes because it is fungible.
- **Hag's Hair.** DC 20 Deception or Intimidation, rolled in Act I, and both are Charisma checks
  on a pair whose other half is Wisdom-based. On the Act I Strength line at Charisma 14 this is a
  bad roll even with two Inspiration rerolls. Either bank Beguiling Influence early or accept it.
- **Illithid: this body takes none.** The pair plan concentrates the pool on Lectern, which
  carries the `+IMR` physical tax better and whose Wisdom 22 drives the best power DCs in the pair.
