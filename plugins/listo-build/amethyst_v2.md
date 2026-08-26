# Amethyst v2 — Force Draconic 11 / Great Old One 3 / Tragedy 6

**Sorcerer 11 (Force Draconic Bloodline) / Warlock 3 (Great Old One) / Bard 6
(College of Tragedy)** — level 20, Lone Wolf duo partner for Lectern v2. A ranged Force chassis
that converts Lectern's Blind into a critical-hit engine, converts those criticals into area
Frighten, and uses Tragedy Bard to turn attacks on Lectern into retaliation windows.

This is the synergy-first alternative to Force Draconic Sorcerer 17 / Warlock 3. Bard 6 gives up
native 7th–9th-level spells and six Sorcery Points for **Sorrowful Fate**, **Tale of Hubris**,
Expertise, Font of Inspiration and a third short rest. The exchange is only correct if the pair
interactions below work in game.

Every mechanic marked **[pak]** was read from the installed Listonomicon 10.2 archive. Mechanics
marked **[data]** are confirmed in the repository's compiled 10.2 class snapshot. Vanilla
mechanics whose base-game paks are unavailable are named as such.

---

## The paired engine

1. **Lectern creates advantage without Amethyst's concentration.** Glaring Frost and Snowborn
   Anthelion turn Lectern's Cold/Radiant damage into two-turn Blind. Attacks against a blinded
   target have Advantage, so Amethyst gets the input a critical-fisher needs while keeping its
   own concentration free for Haste, control or terrain.

2. **Eldritch Blast converts Advantage into critical volume.** At character 17 it fires four
   beams; Lone Wolf supplies two Actions, so the resource-free floor is **eight attack rolls**.
   With Advantage, the chance of at least one natural 20 is:

   | crit range | per beam | at least one across 8 | across 12 with Quickened |
   |---|---:|---:|---:|
   | 20 | 9.75% | **56%** | **71%** |
   | 19–20 | 19% | **82%** | **92%** |
   | 18–20 | 27.75% | **93%** | **98%** |
   | 17–20 | 36% | **97%** | **99.5%** |

3. **Mortal Reminder converts the critical into a second save axis.** Great Old One's level-1
   passive makes the target and nearby enemies save against **Frightened** when Amethyst lands a
   critical. Lectern attacks CON with Blind; Mortal Reminder attacks WIS with Fear. The pair is
   therefore not asking the same defence twice.

4. **Tale of Hubris turns an enemy critical into Amethyst's critical. [pak]** At Bard 6, when a
   creature critically hits Amethyst or Lectern within range, Amethyst may spend a Reaction and
   Bardic Inspiration to mark that creature for ten turns:
   ```
   Interrupt_TaleOfHubris
     Conditions  RollCritical.Success and (Self(Target) or Ally(Target))
     Cost        ReactionActionPoint:1;BardicInspiration:1

   TaleOfHubrisCrit
     Boosts      IF(HasStatus('TALE_OF_HUBRIS_AURA',context.Target)):
                   ReduceCriticalAttackThreshold(2)
   ```
   The aura removes itself when its owner is critically hit. One enemy critical on Lectern can
   therefore produce **both** halves of the counterattack: Friar's Bond reflects Radiant and
   attempts to Blind it, while Tale of Hubris opens an 18–20 critical window for Amethyst's
   advantaged volley.

5. **Sorrowful Fate changes the save ability, not merely the number. [pak]** At Tragedy 3,
   Amethyst targets **itself or an ally** with a two-turn, once-per-short-rest status. The
   recipient's next saving-throw spell gains variants that replace STR, CON, DEX, INT or WIS with
   **CHA**:
   ```
   SORROWFUL_FATE_D8
     Boosts "UnlockSpellVariant(IsSavingThrow(),
              ModifySpellRoll('Constitution','Charisma'), ...); ..."
     RemoveConditions "HasStringInSpellRoll('SavingThrow')"
     RemoveEvents     "OnSpellCast"
   ```
   Apply it to **Lectern** before damaging a high-CON brute. If Glaring Frost is recognized as
   Lectern's next saving-throw spell, its CON save becomes CHA and a failed save also takes 1d8
   Psychic. This is the build's most important unverified interaction: the pak proves the variant,
   but not that a passive `OnDamage` save consumes it.

6. **Grasp of Hadar rebuilds the cluster.** Each EB beam can pull its target 4.5 m. Use the early
   beams to pull separated enemies toward the blinded target or into Lectern's 3 m Anthelion /
   Word of Radiance footprint; spend the remaining beams on the now-controlled cluster. Toggle to
   Repelling Blast when the correct answer is distance instead.

7. **Friar's Bond makes Amethyst a remote detonation point.** When Amethyst is hit, Lectern can
   spend either Lone Wolf Reaction to deal Radiant damage at the attacker. Because Lectern is the
   source, that damage feeds Glaring Frost and Anthelion around Amethyst's position. The pair can
   cover two clusters without standing together.

The loop in one line:

```text
enemy crits Lectern → Bond Radiant tries to Blind + Hubris marks 18–20
                   → Amethyst fires advantaged EB → crit → area Fear
                   → Grasp compacts survivors → Lectern detonates the cluster again
```

---

## Chassis

| class | levels | subclass | what it is here for |
|---|---:|---|---|
| Sorcerer | **11** | **Force Draconic** | CON saves, Metamagic, Haste/Counterspell, Force Elemental Affinity, Draconic Resilience, flight |
| Warlock | **3** | **Great Old One** | Eldritch Blast, Agonizing Blast, Grasp of Hadar, Mortal Reminder, Chain familiar, short-rest slots, feat |
| Bard | **6** | **College of Tragedy** | Sorrowful Fate, Tale of Hubris, Expertise, Font of Inspiration, Song of Rest, Countercharm, two feats |

**Level-1 class: Sorcerer** — CON + CHA saves. Concentration is load-bearing on Haste and control,
and a late Sorcerer level does not grant the save proficiencies.

### Why Sorcerer stops at 11

Sorcerer 11 retains the whole mid-game Draconic package: Elemental Affinity at 6, Wings at 11,
sixth-level Sorcerer spells and eleven Sorcery Points. Levels 12–17 would add three feat
breakpoints, more points, 7th–9th-level spells and the fifth Metamagic at 17. Bard 6 replaces that
with a second control axis, the face role, another short rest and the two pair triggers above.

This is expensive. A character with ninth-level slots but no seventh- through ninth-level spell
known is not a ninth-level caster in practice; those slots mostly upcast lower-tier spells. If
Sorrowful Fate does not modify Glaring Frost, take the clean **Sorcerer 17 / Warlock 3** version
instead.

### Why Great Old One, not Hexblade

Force Draconic does not supply the critical-triggered fear that Aberrant Mind does, so GOO is not
duplicating anything. Mortal Reminder is the payoff for the entire Blind/critical engine.
Hexblade would add boss damage and a 19–20 range against one cursed target, but no conversion from
critical to area control. Spell Sniper, Tale of Hubris and the crit rings already supply the
threshold reductions.

### Why Tragedy, not the other seven colleges

- **Eloquence 6** subtracts a visible d8 from the next save, but leaves Glaring Frost aimed at
  CON. Strong, less transformative.
- **Lore 6** buys skills and two level-3 Magical Secrets. Sorcerer already reaches the obvious
  Haste/Counterspell package.
- **Swords / Valour 6** buy Extra Attack, which loses to four EB beams per Action.
- **Glamour 6** adds Command control that overlaps Lectern rather than enabling it.
- **Dance 6** is a Dexterity/unarmed engine with the wrong action payload.
- **Stormcalling 6** adds a CON-save Thunder engine and concentration competition.
- **Tragedy 6** alone changes Lectern's save ability and makes enemy criticals feed Amethyst's
  critical engine.

---

## Force Draconic ancestry — the damage hinge

Take **Amethyst**, **Cobalt**, or **Eyrie Force** ancestry; all three bind Elemental Affinity to
Force. The expanded ancestry roster and Force association are confirmed in the installed 10.2
class snapshot **[data]**. Amethyst grants Magic Missile and is the clean thematic choice.

At CHA 22, ordinary Agonizing Blast is:

```text
4 × (1d8 + 6) = 42 per cast
2 Actions      = 84 per round
Quickened      = 126 for the nova round
```

**Resolved in game: Force Elemental Affinity adds CHA to every beam, and it stacks with Agonizing
Blast.** Observed at CHA 20 — a beam rolled 5 and dealt **15**, with both Agonizing Blast and
Elemental Affinity named in the log, on every beam of the cast. The question was whether Affinity
applied per beam, once per cast, or not at all because EB was learned from Warlock:

| Force Affinity behavior | one EB | two Actions | + Quickened |
|---|---:|---:|---:|
| ~~no EB interaction~~ | ~~42~~ | ~~84~~ | ~~126~~ |
| ~~+CHA once per cast~~ | ~~48~~ | ~~96~~ | ~~144~~ |
| **+CHA to every beam — confirmed** | **66** | **132** | **198** |

So a beam at CHA 22 is `1d8 + 6 + 6`, and the resource-free floor is **132 raw a round**.
These are raw, before accuracy and gear. Potent Robe may add another CHA modifier to each beam;
that is a separate equipment interaction and must be tested under Listo's gear rebalance.

---

## Stats and saves

Recommended creation line, **after** the freely assigned racial +2/+1:

| STR | DEX | CON | INT | WIS | CHA |
|---:|---:|---:|---:|---:|---:|
| 8 | **16** | **14** | 8 | 10 | **17** |

Put Lone Wolf's +4 on **DEX + WIS**:

| final source | char | DEX | WIS | CHA |
|---|---:|---:|---:|---:|
| creation | 1 | 16 | 10 | 17 |
| Lone Wolf | 1 | **20** | **14** | 17 |
| Actor | 4 | 20 | 14 | **18** |
| Ability Improvement | 6 | 20 | 14 | **20** |
| War Caster | 9 | 20 | 14 | **21** |
| Ritual Caster | 12 | 20 | 14 | **22** |
| *Mirror of Loss* | *16+* | *20* | *14* | ***24*** |

This avoids the Charisma trap. Sorcerer already grants CHA-save proficiency, so spending Lone
Wolf's +4 on CHA would duplicate it. DEX + WIS instead yields four disjoint saves:

- **CON + CHA** — Sorcerer opener
- **DEX + WIS** — Lone Wolf

**The climb to 22 costs two dedicated picks, not three.** War Caster and Ritual Caster are both
half-feats (`+1 INT, WIS, or CHA`) and both were being taken for their own sake, so they carry
the last two points for free. Only Actor and the plain ASI are bought for the stat, and Actor
pays for itself in Expertise. See the feat section for why `Enweaved` is no longer on this line.

**CHA 22 lands at char 12**, inside the Act II band and before the char-15 scoring level, so no
act is scored at a lower modifier than the old `Enweaved` line gave.

### Why the climb cannot be shortened

The obvious economy is to build to 21 and let the Mirror of Loss finish the job — it gives +2 to
a chosen ability *plus* a separate +1 CHA against a cap of 24, so 21 + 3 = 24 exactly, wasting
nothing, where 22 + 3 spills a point.

**It costs a rung.** Act II single-target reads `1.54× par against a rung-4 line of 1.50` — one
CHA point *is* the whole margin. Agonizing Blast and Elemental Affinity both key off Charisma,
so 22 → 21 costs between 6.6 and 13.2 raw depending on the beam-to-dart split, and the ratio
lands at 1.39–1.47 either way: **rung 3**. The Mirror arrives in Act III; the score is taken at
char 15. The feats have to get there alone.

### The slack that does exist: Hag's Hair

**Hag's Hair is Act I, is already assigned to Amethyst, and stacks past 20.** It used to be
picked for CHA 17 → 18 — but **Actor does that at char 4 now**, so the Hair lands later and buys
**20 → 21**, a step the plain ASI cannot reach. *Take it after the char-6 ASI*, so the ASI does
18 → 20 at full value and the Hair does the step past 20.

With it the body sits at 23 before the Mirror and caps at the same 24, which makes **Ritual
Caster's `+1` surplus in actual play**. The line above keeps it because a quest reward behind a
DC 20 check is not a chassis property — the same rule that bars the Mirror bars the Hair. At the
table, the char-12 pick is free the moment the Hag is dealt with, and so is char 18:

| in play, with Hag's Hair | CHA |
|---|---:|
| creation | 17 |
| Actor, char 4 | 18 |
| Ability Improvement, char 6 | 20 |
| **Hag's Hair**, Act I, taken after char 6 | **21** |
| War Caster, char 9 | **22** |
| *char 12 and char 18 free* | — |
| *Mirror of Loss, Act III* | ***24*** |

Two open picks. **Alert** for the list's ambush mods, a second **Resilient**, or **Metamagic
Adept** — whose Essential-Feats cap caveat does not bite when it is taken for the metamagic
rather than for the point.

**Spell save DC / spell attack at 20:** `8 + PB 6 + CHA 6 = DC 20`, `+12` attack before gear —
**DC 21 and `+13` with the Mirror of Loss**, the one source that raises an ability's cap past 22,
to 24.

---

## Race

**Recommended: Astral Half-Elf.** `Astral_Intuition  Boosts "Advantage(Ability, Intelligence);"`
at level 1, permanent **[pak]** — Advantage on all Intelligence checks, patching the dumped
knowledge stat. Starlight Step is a 9 m Bonus Action teleport with one charge at each of levels
1, 5, 9, 13, 17 — **five per long rest, not Proficiency Bonus** **[pak]**. The build has two Bonus
Actions and can afford a positioning button that does not spend a slot.

**The shield question is settled: it inherits.** `Races.lsx` gives the subrace
`ParentGuid "45f4ac10-3c89-4fb2-b37d-f973bb9110c0"` — vanilla Half-Elf — and the mod grants no
proficiencies of its own **[pak]**. **All 810 installed paks were listed and every
`Progressions.lsx` inside them read; none references that GUID**, so nothing in Listo overrides
Half-Elf **[pak]**. Vanilla Half-Elf carries Light armour, **Shields**, spears/pikes/halberds/
glaives, Darkvision and Fey Ancestry (`https://bg3.wiki/wiki/Half-Elf` — vanilla fallback, the
base-game paks are not under the mods root). Draconic Resilience is gated on *not wearing
armour* and a shield is not armour: *"Draconic Resilience works while wearing a Shield"*
(`https://bg3.wiki/wiki/Draconic_Resilience`). **So a shield works beside Potent Robe and
Draconic Resilience — take one.** `(unverified)`: subrace inheritance itself is inferred from the
mod's omission rather than read, so confirm the proficiency list in character creation.

**Alternative: Shadar-kai.** Its once-per-long-rest teleport grants all-damage resistance for a
round from level 3, and its scaling raven is another body. Chain already supplies a familiar, so
this is the survival choice rather than the action-economy choice.

---

## Feats — six

The final split has Sorcerer 3/6/9, Warlock 3 and Bard 3/6.

1. **Actor (CHA)** — char 4. +1 CHA, Expertise in **Persuasion, Deception, Intimidation** and
   **Performance**, with proficiency in any not already held. This is what makes the Act-I Hag's
   Hair check real rather than cosmetic.
2. **Ability Improvement (CHA +2)** — char 6, 18 → 20. The plain ASI is the one ability source
   still capped at 20, so it does this step and nothing above it.
3. **War Caster (CHA)** — char 9, 20 → **21**. Concentration insurance for Twinned Haste and
   control; Sorcerer already supplies CON proficiency, this supplies Advantage. Moved six levels
   earlier than the old line had it, because the concentration it protects is live from Act II.
4. **Ritual Caster (CHA)** — char 12, 21 → **22**. Listo's version has you *learn all* rituals
   rather than toggling one, and it was already wanted for the slot recovery beside Song of Rest.
5. **Spell Sniper** — char 15. Spell critical threshold −1, explicitly stacks; ignores low
   ground; rolls spell/cantrip damage dice with Advantage, though Listo limits that damage rider
   to the first hit.
6. **Open** — char 18. **Alert** if Amethyst must consistently act before Lectern to place
   Sorrowful Fate or Haste; a second **Resilient** otherwise, since it is repeatable on a
   different ability and this body already holds four save proficiencies.

### Why `Enweaved` is off the line

It is the list's only **+2** half-feat and it was the obvious route from 20 to 22. It also grants
**wild magic and magic allergy**, and Listo ships `Wild Magic D100 Table`, `More Wild Magic
effects` and `Increasingly Likely Wild Magic Surge (Combat Only)` on top of it. This is the body
that casts most in the pair — two Actions plus Quickened — *and* the body holding Twinned Haste
concentration. A surge here is not a novelty; it is the concentration check the whole pair is
standing on.

Dropping it costs nothing, because two feats on the old line were not pulling their weight:

- **Skilled Expert** was bought for one thing — Expertise in Intimidation for Hag's Hair. **Actor
  grants that same Expertise plus three more.** Skilled Expert's only unique gift was a skill
  proficiency, spent on Perception, which the pair's gate table gives to **Lectern**.
- **War Caster is a half-feat.** The old line took it at char 15 and never counted the `+1`.

There is a second reason to prefer this line. `data/listo-10.2-feats.md` flags an **unresolved**
question over whether Feats Overhaul's removal of the ability-score cap reaches **Essential
Feats** half-feats — Feats Overhaul's own page recommends a patch mod to uncap them "the same way
this mod does", and that patch is not in the 10.2 list. Skilled Expert, Shadow Touched,
Telekinetic and the Touched feats are all Essential Feats, so **any of them doing the 21 → 22
step rests on the unresolved reading**. Actor, War Caster and Ritual Caster are Feats Overhaul or
Listo-patched, and the plain ASI stops at 20 by design.

**Deadly Alacrity is still not automatic** — see below.

**Deadly Alacrity is not automatic.** It reduces the critical threshold by one, but Listo removed
its +1 ability score. With Spell Sniper plus Critfisher Ring, another threshold feat is usually
over-investment: once the first critical has triggered Mortal Reminder, extra criticals in the
same cluster have diminishing control value.

---

## Skills and background

**Background: Charlatan** — Deception + Sleight of Hand.

Solve the map without overlaps:

| source | picks |
|---|---|
| Charlatan | Deception, Sleight of Hand |
| Sorcerer 1 | Intimidation, Persuasion |
| Actor (char 4) | **Persuasion, Deception, Intimidation Expertise**; Performance proficiency |
| Bard multiclass skill | Insight |
| Bard 3 Expertise | **Sleight of Hand**, **Insight** — re-pointed; Actor already covers Deception |

This gives the pair:

- an Act-I face for the DC 20 Hag check;
- Expertise on routine dialogue and pickpocketing;
- DEX 20 behind Sleight of Hand;
- Perception and Insight on non-dumped abilities.

**Religion is covered from Act III, by the illithid plan rather than by the skill map.**
`Elevated Mind` grants Expertise *and* proficiency in every Intelligence skill, permanently and
re-selectably, on the body whose Astral Intuition already grants Advantage on all Intelligence
checks. INT 8 becomes `−1 + 12 = +11 rolled with Advantage`, which clears the Mirror of Loss at
DC 25 about **58% cold and 92% on two banked rerolls**. That is two tadpoles and no charges, no
IMR and no `+IMR` tax — the cheapest thing on the sheet.

Before Act III, and if the illithid plan is dropped, the two fallbacks stand. bg3.wiki documents
a **100-gold respec at Withers** into Rogue 11 / Knowledge Cleric 1 for Religion Expertise: pass
the DC, respec back, *"retaining the Mirror of Loss stat enhancement"*. The other route skips the
roll entirely — **sacrificing knowledge of the Necromancy of Thay** gives a guaranteed +2, at the
cost of Forbidden Knowledge's +1 to Wisdom saves and ability checks.

**Why it is worth the trouble.** The Mirror is +2 to one ability *plus* a separate +1 Charisma,
**per character**, and it is the only source that raises an ability's cap to **24**. Amethyst
takes CHA 22 → **24**; the +1 CHA rider is then lost to the cap, which is the right trade because
+7 beats anything the +1 could buy elsewhere. Lectern takes WIS 22 → 24 off its own copy.

None of this enters any score. `axis-rubrics.md`'s first rule is that a rented capability is
never a chassis property, and the Mirror of Loss is the case that rule was written against.

---

## Invocations and pact

Warlock 2:

- **Agonizing Blast** — CHA modifier on every EB beam. Mandatory.
- **Grasp of Hadar** — pull one target toward Amethyst; use beam-by-beam to build Anthelion
  clusters. Keep Repelling Blast available through a later feat only if testing shows the pull
  cannot be toggled cleanly.

Warlock 3:

- **Pact of the Chain** — Imp or Quasit with Help, Magic Resistance and the rebuilt 10.2 stat
  block. It is a third body, scout and source of Advantage when Lectern's Blind misses.

Do not take Pact of the Blade. This body makes four attacks per EB Action and is designed around
range; a pact weapon adds a weaker mode rather than a new role.

---

## Metamagic

- **Twinned Spell** at Sorcerer 2 — Twinned Haste covers 100% of a two-character party.
- **Quickened Spell** at Sorcerer 3 — converts one of Lone Wolf's Bonus Actions into a third EB
  or levelled spell. In Listo it is also the general exemption from the bonus-action spell rule.
- **Seeking Spell** or **Empowered Spell** at Sorcerer 10 — Seeking protects a decisive attack
  spell when Blind is unavailable; Empowered is better for high-dice AoE. EB already gains
  Advantage from Lectern, so Empowered is the broader pick.

Quickened costs three Sorcery Points. Sorcerer 11 owns eleven, so it supports three Quickened
rounds before conversion. Do not model the third EB as the at-will floor.

---

## Spells

### Warlock

- **Eldritch Blast** — primary damage and positioning tool.
- **Hex** — boss damage when Haste/control is not the better concentration use. At four beams it
  adds 4d6 per cast, 8d6 across the two-Action floor.
- Prefer utility that upcasts well from the two short-rest level-2 pact slots. The pact slots are
  also conversion fuel only when the spell they would cast is less valuable.

### Sorcerer

- **Shield**, **Magic Missile** (free from Amethyst ancestry), Misty Step.
- **Haste**, Counterspell, Fear, Fireball or a Force/rarely-resisted alternative.
- Banishment / Polymorph or another non-CON answer.
- Sixth-level choice should be a fight-changing spell rather than a damage payload that merely
  duplicates EB.

### Bard

- Utility and non-concentration buttons first: Healing Word, Longstrider, Enhance Ability,
  Lesser Restoration, See Invisibility where available.
- Do not fill the known list with concentration spells that compete with Haste.
- Bard 6 does **not** reach ordinary Magical Secrets; only Lore would receive them here.

### Concentration budget

Amethyst has one concentration slot and three real claims on it:

1. **Twinned Haste** — default for tempo; every cast covers the whole party.
2. **Hex** — priority-target damage when the fight is safe enough that more damage beats more
   Actions.
3. **Control** — when removing turns is better than multiplying them.

Lectern's Blind/Fear setup costs Amethyst no concentration. That is the pairing's central
advantage: the control engine remains live underneath whichever of the three modes Amethyst
selects.

---

## Equipment targets

1. **Critfisher Ring [pak]** — the shipped passive is
   `ReduceCriticalAttackThreshold(3)`. This is enough beside Blind to make Mortal Reminder nearly
   deterministic; assign it to Amethyst.
2. **Ring of Viciousness [pak]** — `ReduceCriticalAttackThreshold(1)`. Use before Critfisher or
   when the second ring slot is genuinely free; both together are probably excess.
3. **Potent Robe** — likely adds CHA to every EB beam while preserving Draconic Resilience.
   Keep Alfira alive. Verify the per-beam interaction under the installed gear rebalance.
4. **A shield.** Astral Half-Elf inherits Half-Elf shield proficiency and Draconic Resilience is a
   base-AC replacement that works with shields — see *Race*. Both halves are now evidenced.
5. Spell-attack/DC and concentration equipment after the engine pieces. Do not sacrifice a large
   accuracy bonus for a crit reduction: a wider critical range does nothing on a miss.

The base-game critical items — The Dead Shot, Knife of the Undermountain King, Bloodthirst,
Sarevok's helm and conditional cowls — are not assumed here. Base-game paks are unavailable to
the mod archive reader and Listo installs gear rebalances; verify each tooltip before assigning
an attunement slot.

---

## Progression ladder

This is a ladder of strongest holdings, not a no-respec purchase order.

| char | holding | what changes |
|---:|---|---|
| 1 | Sorcerer 1 | CON/CHA saves, Draconic Resilience, Amethyst ancestry |
| 2–3 | Sorcerer 1 / Warlock 1–2 | EB, GOO Mortal Reminder, then Agonizing + Grasp |
| 4 | Sorcerer 1 / Warlock 3 | Chain familiar; feat 1 — **Actor**, CHA 18 |
| 5 | Sorcerer 2 / Warlock 3 | Twinned Spell; two-beam EB |
| 6 | Sorcerer 3 / Warlock 3 | Quickened Spell; feat 2 — **ASI**, CHA 20 |
| 7–8 | Sorcerer 4–5 / Warlock 3 | spell progression, then Haste/Counterspell |
| 9 | Sorcerer 6 / Warlock 3 | **Force Elemental Affinity**; feat 3 — **War Caster**, CHA 21 |
| 10–11 | Sorcerer 7–8 / Warlock 3 | spell tier — no feat lands here |
| 12 | **Sorcerer 6 / Warlock 3 / Tragedy 3** | **respec:** Sorrowful Fate + Expertise; retain Affinity; feat 4 — **Ritual Caster**, **CHA 22** |
| 13–17 | Sorcerer 7–11 / Warlock 3 / Tragedy 3 | rebuild Sorcerer spell tier; Wings at 17; feat 5 at 15 — **Spell Sniper**. **Mirror of Loss from 16** takes CHA to **24** |
| 18 | **Sorcerer 9 / Warlock 3 / Tragedy 6** | **respec:** Tale of Hubris, Font, Countercharm, Song-rest engine; feat 6 — **open** (Alert, or a second Resilient) |
| 19–20 | Sorcerer 10–11 / Warlock 3 / Tragedy 6 | third Metamagic, Wings, sixth-level spells |

At every respec, keep **Sorcerer first**. Starting Bard or Warlock silently replaces CON saves.

The ladder deliberately delays Bard 6 until 18. Before Tale of Hubris exists, Sorcerer spell
tier and Force Affinity outbid generic Bard levels. Sorrowful Fate arrives at 12 because it is a
whole new answer to Lectern's high-CON matchup and costs no Affinity tier at that rung.

---

## How it plays

### Default crowd turn

1. Lectern opens with Cold/Radiant and attempts Blind.
2. Amethyst targets the blinded cluster with EB, pulling outliers inward with Grasp.
3. Split beams after the first critical so Mortal Reminder can threaten a second cluster.
4. Keep the Chain familiar on Help, scouting or finishing duties rather than trading it away.

### High-CON target

1. Amethyst applies Sorrowful Fate to Lectern before the engagement or before Lectern's next
   trigger spell.
2. Lectern deals Cold/Radiant; test whether the save variant appears and changes Glaring Frost to
   CHA.
3. If Blind lands, Amethyst makes the advantaged critical volley.
4. If it does not, use ordinary Sorcerer control against the target's weaker save rather than
   repeating a bad CON contest.

### Enemy critical on Lectern

1. Accept the attack if it is not lethal; Retribution wants the hit.
2. Amethyst spends a Reaction + Inspiration on Tale of Hubris.
3. Lectern's Bond reaction deals Radiant and attempts Blind around the attacker.
4. Amethyst focuses the marked target until the first critical consumes Hubris and triggers
   Mortal Reminder.

### Boss turn

- Twinned Haste when the extra Actions will survive the concentration risk.
- Hex when the boss is controlled and damage is the only remaining problem.
- Quickened EB only when a third volley changes the round; Sorcery Points are not the floor.
- Counterspell save-based enemy actions that do not feed Lectern's Retribution.

---

## Resource budget

- **EB / Mortal Reminder / Grasp:** at will.
- **Pact slots:** 2 level-2 slots × four rest segments after Song of Rest = **8 casts** per long
  cycle, assuming the ordinary two short rests plus the Bard rest.
- **Bardic Inspiration:** 4d8 at Bard 5+, refreshing on each short rest; up to **16 uses** across
  the same four segments if all rests are taken.
- **Sorrowful Fate:** once per short rest; up to **4 uses** per long cycle.
- **Sorcery Points:** 11 long-rest points, plus spell-slot conversion. Quickened costs 3.
- **Sorcerer/Bard spell slots:** full-caster level 17 for slots, but spells known stop at
  Sorcerer 6th / Bard 3rd.

Song of Rest also refreshes Lectern's ki and Channel Divinity. Its value is pair-wide, not merely
four extra Inspiration uses.

---

## Provisional profile

These are planning estimates, not a replacement for a scored routine. Force Affinity is now
tested and Single-target III is settled at **5**; Sorrowful Fate is still load-bearing, so the
Control rungs remain provisional.

| axis | I | II | III |
|---|---:|---:|---:|
| Single-target | 3 | 4 | **5** |
| AoE | 2 | 3 | 3–4 |
| Durability | 3 | 3 | 3 |
| Actions | 4 | 4 | 4 |
| Control (single) | 3 | 4 | **4 ?** |
| Control (area) | 3 | 4 | 4 |
| Rescue | 2 | 3 | 3 |
| Skills | 4 | 4 | 4 |
| Saves | 4 | 4 | 4 |
| Endurance | 3 | 3 | 3–4 |

The pair division is deliberate: Lectern owns durability, rescue, repeatable control and
endurance; Amethyst owns priority damage, face, Counterspell, Haste and forced positioning. The
shared loop raises Control-area beyond what either body does alone.

---

## Known weaknesses

- **One unverified interaction still carries the ceiling:** Sorrowful Fate on Glaring Frost.
  Force Affinity per EB beam is **confirmed in game**.
- **No native 7th–9th-level spells.** Full-caster slots do not replace spells known.
- **The build is soft by duo standards.** Lone Wolf halves damage, but d6 hit dice, clothing and
  enemy preference for the softer body still matter.
- **Mortal Reminder does nothing to critical-immune enemies**, and many bosses resist Fear.
- **Blind partly suppresses Lectern's own reflect rate.** Once enemies attack at Disadvantage,
  fewer attacks hit and feed Bond.
- **Tale of Hubris is reactive.** It needs the enemy to crit first and consumes both a Reaction
  and Inspiration.
- **Sorrowful Fate is once per short rest**, lasts two turns, and is consumed by the recipient's
  next saving-throw spell. Do not let Lectern spend it on a low-value save before the intended
  target.
- **Concentration is crowded.** Haste, Hex and control cannot coexist.
- **Gear concentration is real.** Critfisher and Potent Robe are build-defining assignments, and
  Listo's attunement cap prevents wearing every attractive crit item.

---

## Open decisions and required tests

1. ~~**Force Affinity × Eldritch Blast.**~~ **Done — it adds +CHA to every beam**, stacking with
   Agonizing Blast. A beam rolling 5 dealt 15 at CHA 20, both riders named in the log.
2. **Sorrowful Fate × Glaring Frost.** Apply Sorrowful Fate to Lectern, deal Cold/Radiant through
   Lectern, and inspect whether the target rolls CHA instead of CON. Also verify which trigger
   consumes the two-turn status.
3. **Potent Robe × EB under gear rebalance.** Confirm +CHA on every beam and whether it stacks
   with Agonizing and Affinity.
4. **Crit stacking.** Confirm Spell Sniper, Critfisher and Tale of Hubris stack and observe the
   displayed critical threshold. Do not equip Ring of Viciousness by default unless it changes
   a real breakpoint.
5. **~~Astral Half-Elf shield proficiency~~ — resolved.** No enabled pak overrides Half-Elf across
   all 810 archives, and vanilla Half-Elf grants Shields. See *Race*. Only the generic
   subrace-inheritance caveat remains; character creation shows it before you commit.
6. **Ritual Caster versus Alert.** If the slot recovery works on the additional Song of Rest,
   Ritual Caster is the endurance engine; otherwise take Alert.

**Fallback rule:** test 1 passed, so the Aberrant Mind 11 / Hexblade 3 / Tragedy 6 branch is
dead and the damage ceiling stands. Only test 2 is still live: if Sorrowful Fate does not modify
Glaring Frost, return the six Bard levels to Sorcerer and play Force Draconic 17 / GOO 3 — the
Bard block would then be buying Tale of Hubris and a third short rest alone, which is not worth
7th–9th-level spells.
