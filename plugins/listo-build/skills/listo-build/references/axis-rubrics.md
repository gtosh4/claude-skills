# Listonomicon 10.2 — axis rubrics

What 0–5 means on each of the ten axes, anchored on named content in the installed 10.2
manifest. **Every rung is a checkable configuration.** No rung is defined by comparison to
another chassis — that circularity is what this file exists to remove.

Score a **single body**, per act — **ten values**, since Control is two axes (§5, §6). Never score
a pair here; the pair value is derived. `scoring-model.md` owns how two bodies combine, the
fight-type coefficients, the weights and the score. `listo-build` SKILL.md §5a owns the functional
ladder and what each axis measures. This file owns only **what a 0–5 is**.

## Scoring is act-relative

**A 5 means "as good as a body can be at this point in the run", not "as good as a body can ever
be".** Act I's rung 5 and Act III's rung 5 are different configurations, because Act I has two
feats and 4th-level slots while Act III has seven feats and 9th-level slots.

Scored absolutely, every chassis would read low in Act I and high in Act III, and the act columns
would measure character level instead of chassis quality. They exist to answer *"who is ahead
right now"*, so each act is judged against its own ceiling.

Consequence: **act scores are not comparable across acts.** A 4 in Act I is not weaker than a 4 in
Act III — both mean "near the best available then". Summing the three acts averages a chassis's
standing across the run, which is the intended reading.

### The ladder is the shape; the act table is the threshold

Each axis below carries two things, and they do different jobs:

- the **0–5 ladder** — what *kind* of capability each rung is. Act-invariant.
- the **act table** — what that kind of capability has to *be* in each act to hold the rung. This
  is where the act-relativity actually lives, and it is anchored for **every rung from 2 up**.

Rungs **0 and 1 are act-invariant by construction** — you either have nothing, or you have an
incidental. Nothing about "no armour proficiency" or "an incidental rider" changes between acts,
so those two rungs carry no act row.

**A chassis that acquires a capability and never improves it slides down.** That is not a defect;
it is the direct consequence of "a 5 means as good as a body can be at *this point* in the run".
Score against the act's row, not against what the chassis was worth when it got the feature.

The floor moves too. A martial with no spell list scores 0–1 on both control axes in all three
acts regardless of how far the caster bar rises, so **tightening the upper rungs adds resolution
in the caster band without compressing the martial band.** The two problems are separable.

### What actually drifts, and what does not

Derived from `CombatExtender.json` (numbers in `data/listo-10.2-mcm.md`), read at the end of each
act band — character 8 / 15 / 20:

| | end of I | end of II | end of III |
|---|---|---|---|
| Enemy HP multiplier | ×1.54 | ×1.96 | **×2.26** |
| Boss HP multiplier | ×1.74 | ×2.30 | **×2.70** |
| Enemy AC / boss AC | +0 / +0 | +1 / +1 | +1 / +2 |
| Enemy ability points | +1 | +2 | +3 |
| Boss spell save DC (*their* offence) | +1 | +2 | +2 |
| Our proficiency bonus | +3 | +5 | +6 |
| Our spell save DC | ≈16 | ≈18 | ≈20 |

- **Fixed-magnitude effects decay.** A flat 1d6 rider holds about **two-thirds** of its relative
  value from the end of Act I to the end of Act III (1.54⁄2.26 against ordinary enemies,
  1.74⁄2.70 against bosses). That is a one-rung slide for a body whose contribution is purely flat,
  and it is the main reason a chassis can fall between acts.
- **Scale-invariant effects hold.** Advantage and Disadvantage, Lone Wolf's halving, proportional
  resistance, and attack counts — which ride weapon dice, stat and gear — do not decay.
- The clearest worked case is the **Eldritch Cannon**: 20 HP and a flat 2d8 is excellent at
  character 3 and close to irrelevant by Act II. Read a flat row as *keeps pace*, not as *stopped
  growing*, and a falling row as the build being outrun.
- **Summons decay slowest of all.** Allies scale +34% HP and **+1 AC static plus +1 per 4 levels**,
  so a summon set holds its rung where a flat-statted feature loses one.

> **⚠ Correction — save-DC control does *not* decay, and the old note saying it did was a
> misreading.** `Spell save DC: bosses +1 per 7 levels` is the DC of spells **the enemy casts**;
> it is their offence and belongs on §9 Saves. What resists *our* control is the enemy's saving
> throw, which rises only through `Ability points +1 per 6` and the flat `+1 per 20` on save rolls
> — roughly **+2 to +3** across the whole run, against **+4** on our own DC (proficiency +3, primary
> stat +1). A pure save-DC controller therefore **holds its rung**, and may gain slightly.
>
> Rungs 4–5 on both control axes still sit above rung 2, but on the **concentration** argument
> alone — a duo holds exactly two slots — which is derived and sufficient. Do not restore the
> decay justification.

| band | characters | feats | full-caster tier | what newly lands |
|---|---|---|---|---|
| **I** | **3–8** | **2** | 4th | Extra Attack (class 5), Action Surge (Fighter 2), Fireball / Haste (caster 5), Aura of Protection (Pal 6), Expertise ×2 (Bard/Rogue 3), Twilight Sanctuary (Cleric 2), Brutish Durability (Fighter 7) |
| **II** | **9–15** | **5–6** | **8th** | Eldritch Cone (Warlock 9), Improved Extra Attack + off-cadence feat (Fighter 11), Reliable Talent (Rogue 11), Brand of the Sapping Scar (ProfaneSoul 11), Volley / Whirlwind (Ranger 11), Flurry of Healing and Harm (Monk 11), Chains of Carceri (Warlock 12), Diamond Soul (Monk 14), Slippery Mind (Rogue 15) |
| **III** | **16–20** | **7–8** | 9th | 9th-level slots, Mirror of Loss, Legendary attunement gear, class capstones (17–20) |

> **Where these bands come from.** `CombatExtender.json` → `Level.Bosses.Act` sets `MaxLevel`
> **10 / 16 / 24** for Acts 1/2/3, and **10 and 16 are identical across the EASY, live and HARD
> configs** — only the `Offset` values differ (0/0/0, 0/2/4, 2/3/6). Offset is the difficulty knob;
> MaxLevel is structural. On EASY, where offset is 0, boss level *equals* player level capped at
> MaxLevel, so the cap states the highest player level the designer expects in that act: Act 1 ends
> by 10, Act 2 by 16. Listo's own `3-GameBalance.md` adds that Act 3 encounters "should keep you
> awake beyond level 16+".
>
> **Act II is the richest band, not Act III.** Six feats, 8th-level slots, and almost every
> run-defining class breakpoint (Fighter 11, Rogue 11, ProfaneSoul 11, Ranger 11, Monk 11, Warlock
> 12, Monk 14). Act III adds the 9th tier, Mirror of Loss, Legendary attunement and capstones — real,
> but a narrower delta than the level span suggests.

## Two constraints that apply to every axis

**The axes are not independent — they are funded from one budget.** Feats
(`floor(A/3) + floor(B/3)`, +1 per class reaching 13, +1 for Fighter/Rogue at 11), twenty class
levels, and one primary stat that must hit **20 by character 6 and 22 by 18**. A 5 on any axis
is priced in that act's budget, and in Act I two 5s essentially cannot coexist — there are two
feats. When a body scores 5, check what it gave up; if nothing, the score is wrong.

**Lone Wolf is baseline, not a bonus.** For this run it is enabled in non-feat mode, so every
body already has 2 Actions, 2 Bonus Actions, 2 Reactions, halved damage from all sources, and +4
to *two* abilities with save proficiency in both, **from level 1**. Score what the chassis adds
**above** that floor in every act. (`GOON_LONE_WOLF_STATUS`; +30% max HP is a separate MCM toggle
— if `enableHpMax` is off, effective HP is 2.0× per body rather than 2.6×.)

---

## 1. Single-target

Damage into one priority target per round, with both Lone Wolf Actions spent on it.

| | |
|---|---|
| **0** | A cantrip or one weapon attack per Action, no rider. |
| **1** | One attack per Action with a small per-hit rider, or a character-level-scaling cantrip. |
| **2** | The act's standard multiattack, no rider. |
| **3** | The act's standard multiattack plus a per-hit rider. |
| **4** | The above plus a third attack source every round, or a repeatable burst channel. |
| **5** | The act's maximum attack count, with a rider on every hit **and** a bonus-action attack. |

| rung | I (char 3–8) | II (9–15) | III (16–20) |
|---|---|---|---|
| **2 =** | Extra Attack (class 5) — 2 per Action, 4 per round. A body still on one attack per Action by act's end is rung 0–1 | 2 per Action, no rider. Improved Extra Attack exists now, so this is merely par | 2 per Action with no rider **and** no attuned weapon falls to **1**; par is 3 per Action, or 2 with Legendary attunement |
| **3 =** | Extra Attack + a per-hit rider — Crimson Rite, Divine Smite, Hex, Hunter's Mark, Sneak Attack | The same, but a **flat** rider (1d4/1d6) is now worth two-thirds of its Act I value; a rider that scales with level or dice count (Sneak Attack, Improved Divine Smite at Paladin 11) holds the rung, a flat one slips | 3 per Action with a scaling rider, or 2 per Action with a scaling rider **plus** one damage feat |
| **4 =** | Rung 3 plus a third attack source — Action Surge (Fighter 2), a Thief bonus action, a bonus-action strike | Rung 3 plus Improved Extra Attack (Fighter 11) **or** a repeatable burst channel — Eldritch Smite, Consuming Fervor | Rung 3 plus a 9th-tier burst, or Concentrated Blast / Psionic Overload at IMR 4–5 |
| **5 =** | Extra Attack (class 5) + rider (Crimson Rite, Divine Smite, Hex, Sneak Attack) + a bonus-action strike (War Priest, Martial Arts, Priest of Zeal) | **Improved Extra Attack (Fighter 11)** — 3 per Action, 6 per round — + rider + bonus-action strike | The Act II ceiling plus a damage feat (Great Weapon Master, Sharpshooter, Savage Attacker) and attuned gear |

> Eldritch Blast is **1d8 per beam here, not 1d10** (v10.0 nerf); beams at character 5/10/17, 4th
> from `Expansion`. Any damage math from outside Listo is overstated.
>
> **Absolute Wrath is ON**, so ordinary enemies carry layered resistances, not just bosses. A body
> locked to one commonly-resisted damage type **caps at 4 from Act II** unless it carries a
> resistance strip (Paragon Nighthawk, Circle of Stormchasers 10, School of Death 6), Elemental
> Adept, or a second weapon of another type. Force is least-resisted, then Radiant in Act 2.

## 2. AoE

Damage delivered to a group per round, and how often it is available. Priced against **+126%
enemy HP at 20** — repeatability outranks per-cast size, increasingly so as the run goes on.

| | |
|---|---|
| **0** | Nothing that hits more than one target. |
| **1** | An incidental multi-hit — cleave, a thrown item, a cantrip that catches two. |
| **2** | One levelled AoE per fight out of long-rest slots. |
| **3** | A **repeatable** AoE on an at-will or short-rest clock. |
| **4** | A repeatable AoE **plus** a burst, a maximised burst, or two AoE damage types. |
| **5** | The act's best repeatable AoE delivered twice a round, plus a second damage type or a maximised burst. |

| rung | I (4th tier) | II (8th tier) | III (9th tier) |
|---|---|---|---|
| **2 =** | One Fireball / Shatter / Ice Knife per fight out of long-rest slots | A single 3rd-tier AoE is now background — par is a 4th–5th tier cast (Ice Storm, Cone of Cold) once per fight | 6th-tier and up once per fight (Chain Lightning, Sunburst, Freezing Sphere); a lone Fireball is rung **1** |
| **3 =** | A **repeatable** source — Breath of the Dragon (Monk 3, replaces one attack), a cleave routine, Consuming Fervor's maximised Fireball ×2 per short rest (Cleric 6) | Eldritch Cone (Warlock 9) or Spirit Guardians as moving denial. ⚠ **Eldritch Cone stops scaling at character 10** and so slides to rung 2 in Act III | An at-will weapon AoE (Volley / Whirlwind), or Cull the Weak's overkill spread at IMR 4–5 |
| **4 =** | Repeatable **plus** a slot burst, or two damage types against early resistances | Repeatable plus a 5th–6th tier burst, or a maximised burst on a short-rest clock | The at-will engine plus a 9th-tier burst, **or** the engine plus a second damage type |
| **5 =** | Fireball/Shatter from slots **plus** a repeatable source — Breath of the Dragon (Monk 3, replaces one attack, costs no bonus action) | **Volley/Whirlwind** (Ranger 11 — at-will full weapon damage to every target, no save, no resource) ×2 rounds, or Eldritch Cone (Warlock 9), plus Consuming Fervor's maximised Fireball ×2 per short rest | The Act II at-will engine **plus** a 9th-tier burst and a second damage type against layered resistances |

> **Eldritch Cone / Line does not scale past character 10.** `Zone_EldritchCone` reads
> `LevelMapValue(EldritchZoneDamage)` — 1d10 at 1–4, 2d10 at 5–9, **3d10 from 10, where it ends** —
> and its `SpellSuccess` never checks `AgonizingBlast`. A cone chassis peaks in Act II and **drops a
> rung in Act III** as enemy HP keeps climbing.
>
> Consuming Fervor is `MinimumRollResult(Damage,20)` on Fire **or Thunder**, Channel Divinity, twice
> per short rest at Cleric 6.

## 3. Durability

How hard this body is to remove by damage. Lone Wolf's halved damage is the floor for everyone in
every act, so it earns no rung.

Rank by **mitigation actually applied**, not by armour category — a robe with the right spells
outperforms unoptimised medium armour.

**Self-healing is Durability, not Rescue.** Effective HP however it is bought: AC, hit dice,
resistances, damage reduction, *and* recovery aimed at yourself — Second Wind, Lay on Hands spent
on yourself, temp HP on yourself, Lycan Regeneration (11: 1 + Con each turn below half), Durable's
full-HP short rests. A body that keeps itself up is durable; only what it can aim at its partner
is Rescue. Never score the same feature in both.

| | |
|---|---|
| **0** | No armour proficiency, no AC spell, no defensive feat. |
| **1** | Light armour, no shield; or a robe with **Mage Armour** alone (13 + Dex). |
| **2** | Medium armour and a shield; or a robe with Mage Armour **plus Shield** cast most rounds. |
| **3** | Heavy armour and a shield. |
| **4** | Rung 3 plus one flat-reduction or damage-halving source. |
| **5** | Rung 3 plus everything the act's feat budget can stack on top. |

| rung | I (2 feats) | II (5–6 feats) | III (7–8 feats, 5 attuned) |
|---|---|---|---|
| **2 =** | Medium armour + shield (AC 17–18), or a robe with Mage Armour **plus** Shield cast most rounds — only if the slot budget supports it | The same, but enemy AC/attack scaling has begun; par now includes **one magic AC source** on top | Medium + shield with no magic AC and no attunement falls to **1**; par is medium/heavy + shield + an attuned defensive item |
| **3 =** | Heavy armour + shield (AC 19–20) — reachable only if the level-1 class grants heavy armour proficiency | Heavy + shield **plus** a magic AC source or a resistance | Heavy + shield + attuned defensive gear, or rung 4's mitigation without the armour |
| **4 =** | Rung 3 + **Heavy Armour Master** — one feat, which is half the Act I budget. Class equivalents: Lycan Resilient Hide, Uncanny Dodge, Evasion | Rung 3 + **Shield Master**'s passive Block, or Evasion, or Eldritch Ward at IMR 2+ (flat `IMR` off AoE, ranged and spells) | Rung 3 + two mitigation layers, at least one **proportional** — flat-only mitigation sits a rung below its raw numbers by Act III |
| **5 =** | Heavy armour + shield + **Heavy Armour Master** (all damage −PB, cap 5) — one feat, and only if the level-1 class grants heavy armour. Brutish Durability (Fighter 7) also lands here | + **Shield Master** (Block is a **passive** here: halves damage on a failed Dex save, plus flat −1) and **Tough** → flat −6 after Lone Wolf's halving, plus Evasion-grade AoE mitigation | + Legendary attunement defensive gear (5 attuned, 3 Legendary) |

> **Shield lasts until the start of your next turn**, so it is a once-per-round +5 and **Lone Wolf's
> second reaction buys no extra uptime** — the second cast would overwrite an active buff. It also
> costs a slot every round it is used, so a robe caster is paying for Durability out of **Endurance**.
> Score rung 2 only if the slot budget actually supports casting it most rounds.
>
> Heavy Armour Master needs heavy armour proficiency first — free from a Fighter/Paladin/heavy
> domain at level 1, otherwise **three feats** (Lightly → Moderately → Heavily Armoured), which no
> Act I budget can afford.
>
> Shield Master's Block **does not stack with Rogue Evasion**. A body with both scores 4, not 5.
>
> Class equivalents for rung 4: Lycan Resilient Hide, Uncanny Dodge, Evasion.
>
> **Flat reduction is crowd-facing; proportional is fight-shape neutral.** Heavy Armour Master's
> flat −5 *per hit* is enormous against eight small attacks and nearly irrelevant against one
> 60-damage hit, while Lone Wolf's halving is scale-invariant. Durability is not split into crowd
> and boss axes the way Control is — it is not a capability you choose between on a given turn — so
> **price the mismatch here instead**: a body whose mitigation is purely flat, facing an act whose
> encounters are boss-weighted, sits a rung below where its raw numbers suggest. `scoring-model.md`
> §7 records why this is handled in the rubric rather than the schema.

## 4. Actions

Meaningful things this body makes happen per round **above** Lone Wolf's 2/2/2 floor — which
already matches a four-body party's economy. This axis measures surplus, not sufficiency.

| | |
|---|---|
| **0** | One attack or spell per Action; bonus action and reaction unused. |
| **1** | A recurring bonus-action use. |
| **2** | The act's standard multiattack, or one permanent extra body. |
| **3** | Multiattack plus a recurring bonus-action attack, or a real third body. |
| **4** | The above plus a third Action, or a multi-body summon set. |
| **5** | An Action handed to the **other** body, or the act's largest body count, on top of own extra attacks. |

| rung | I | II | III |
|---|---|---|---|
| **2 =** | Extra Attack (class 5), or one permanent extra body — Find Familiar, Beast Tamer's short-rest familiar, Pact of the Chain | The same. A familiar still counts because **allies scale too** (+34% HP, +1 AC per 4 levels) | 2 per Action or a single familiar is now par at best; a body with neither falls to **1** |
| **3 =** | Multiattack + a recurring bonus-action attack (Martial Arts, War Priest, Priest of Zeal, Thief), or a real third body — Conjure Animals at Druid 5, **non-concentration until long rest** via `13458` | The same, plus a maintained summon set with `Automated Summons` (`10922`) handing turns to the AI | A summon set **plus** a bonus-action attack engine |
| **4 =** | Rung 3 plus a third Action — **Action Surge** (Fighter 2) | Rung 3 plus Action Surge, or a multi-body summon set | Rung 3 plus Action Surge (two charges at Fighter 17), or **Astral Stillness** free casts every `10 − IMR` stacks |
| **5 =** | **Haste** on the partner (caster 5) + Extra Attack + Action Surge; or a summon set — Conjure Animals at Druid 5, made **non-concentration, until long rest** by `13458`, with `Automated Summons` (`10922`) handing their turns to the AI | Improved Extra Attack (Fighter 11) + Haste on the partner + a maintained summon set | + uncapped undead (`Animate Dead++` removes the cap, moves free Animate Dead to 5, extends Undead Thralls to every undead owned) and 9th-tier summons |

> **Priest of Zeal** charges scale with Wisdom — six at Wis 22 — and `PriestOfZealActionPoint` is
> `ReplenishType "Rest"`, i.e. short rest. But each use also requires a `BonusActionPoint`, so the
> per-turn cap is 2 with Lone Wolf; the six is a per-short-rest pool.
>
> A summon's action is worth less than a character's. Score a set as one rung of surplus plus its
> soak value, not as N actions.

## Control is two axes

Control removes enemy action points **temporarily**, exactly as damage removes them permanently —
so it carries the same crowd-versus-boss split damage already has. Score both.

| | crowd | boss |
|---|---|---|
| **permanent** | AoE (§2) | Single-target (§1) |
| **temporary** | **Control (area)** §6 | **Control (single)** §5 |

**The binding rule for both is one concentration spell per character**, so a duo has exactly two
slots between them — which is why control that spends no slot is worth a full rung more than
control that does.

> **Rungs 4–5 sit above rung 2 on the concentration argument alone**, and that is enough: the pair
> holds two slots between them, so control that spends none is strictly additional where control
> that spends one is substitutional.
>
> An earlier version of this note also claimed save-DC control decays across the run. **It does
> not** — see the correction under "What actually drifts". Enemy saving throws rise ~+2 to +3 while
> our DC rises +4. Disadvantage-on-saves is still better than a DC, but because it stacks with the
> DC rather than because the DC rots.
>
> **The pool a caster picks from, by act** (`data/listo-10.2-spells.md`): Wizard 176 / 242 / 260,
> Sorcerer 138 / 182 / 192, Bard 85 / 105 / 122 — plus Magical Secrets at 280 (Bard 10), 376 (14)
> and **415** (18). Ranger 40 / 58 / 68. A chassis with no list scores 0–1 here in every act.

## 5. Control (single)

Removing **one** enemy's turn — the boss answer.

| | |
|---|---|
| **0** | No single-target control. |
| **1** | An incidental rider — Prone from a shove, Repelling Blast (**which now allows a Strength save**). |
| **2** | One single-target concentration control spell off long-rest slots. |
| **3** | That **plus** a repeatable non-concentration rider. |
| **4** | Single-target control that **costs no concentration**, so it never competes with the partner's one slot. |
| **5** | The above plus slot-free hard control on a short-rest clock. |

| rung | I (4th tier) | II (8th tier) | III (9th tier) |
|---|---|---|---|
| **2 =** | Hold Person / Command / Ensnaring Strike off long-rest slots | The 2nd-tier version is background now; par is 5th–8th tier — Hold Monster, Dominate Person, Feeblemind | 6th–9th tier off long-rest slots — Dominate Monster, Power Word Kill. Hold Person alone is rung **1** |
| **3 =** | Rung 2 **plus** a repeatable non-concentration rider — Cunning Strike (Rogue 5), Wrath of the Storm, Mind Sliver's save penalty | Rung 2 plus Hypnotic Stare (Mesmerist 2 — permanent −1 to one enemy's saves, bonus action, no resource) or Vengeance's Divine Scourge | Rung 2 plus a rider from Legendary attunement gear, or illithid Ability Drain |
| **4 =** | Single-target control costing **no concentration** — Command, Hypnotic Stare, a Prone routine that lands every turn | **Brand of the Sapping Scar** (ProfaneSoul 11 — blanket Disadvantage on the branded creature's saves, free interrupt, no concentration) | **Psionic Dominance** (Dominate Person, no concentration) at IMR 4–5, or Blade of Disaster |
| **5 =** | Hold Person (caster 3) / Command **plus** a repeatable rider — Cunning Strike (Prone/Poison/Disarm every turn), Wrath of the Storm | Brand of the Sapping Scar or Divine Scourge, **plus Chains of Carceri** (`Invocations Expanded`, Warlock 12 — Hold Monster, once per short rest, no slot) | **Time Stop** — every enemy loses every action point for its duration, the purest effect on this axis — or Power Word Kill / Dominate Monster off the 9th slot, **plus** a no-concentration rider |

> **Brand of the Sapping Scar is single-target, not area** — `Brand_Castigation` marks one creature.
> Its value is that the Disadvantage is blanket *across that creature's saves* and costs no
> concentration, so it never competes with the partner's one spell.

## 6. Control (area)

Removing **several** enemies' turns — the crowd answer, and the one Listo's added encounters
punish you for lacking.

| | |
|---|---|
| **0** | No area control. |
| **1** | An incidental multi-target effect — difficult terrain, a surface left behind. |
| **2** | One area control spell off long-rest slots. |
| **3** | Repeatable area control, or an area spell **plus** a non-concentration rider. |
| **4** | Area control that **costs no concentration**, so it never competes with the partner's one slot. |
| **5** | Slot-free repeatable area control on a short-rest clock. |

| rung | I (4th tier) | II (8th tier) | III (9th tier) |
|---|---|---|---|
| **2 =** | Hypnotic Pattern / Web / Sleep off long-rest slots | Par is 4th–5th tier — Evard's Black Tentacles, Sleet Storm, Confusion. A lone Web is background | 6th–9th tier — Weird, Psychic Scream, Prismatic Wall, Maze, Incendiary Cloud. Web alone is rung **1** |
| **3 =** | Repeatable area control, or an area spell **plus** a surface or shove routine | Spirit Guardians as moving denial on a repeatable clock, or an area spell plus a non-concentration rider | An area spell plus Black Hole (IMR 4–5: pull, Prone, guaranteed Dazed 2) |
| **4 =** | Area control costing **no concentration** — Grease and other persistent surfaces, Repelling Blast, a shove routine that lands every turn | Mind Flayer's Insanity stacks or Repulsor at IMR 2–3, or an area effect that runs off a short-rest charge rather than concentration | Black Hole, or 9th-tier area control that resolves on cast rather than holding |
| **5 =** | Hypnotic Pattern / Web / Grease (caster 5) plus a surface or shove routine | Evard's Black Tentacles, Sleet Storm, Spirit Guardians as area denial, on a repeatable clock | 9th-tier area control off the new slot **plus** a no-concentration layer under it |

> A chassis carrying only single-target hard control **should fall on this axis as encounters
> crowd**. `data/docs/3-GameBalance.md` — More Enemies in Basic Fights, Encounters Overhaul and
> Vulkrana's all add bodies specifically to compensate for larger parties, and a duo faces the same
> counts.

## 7. Rescue

**Keeping the *other* body functional, or getting it back.** Outward-facing only — recovery aimed
at yourself is **Durability**, and scoring it in both inflates the polygon and breaks the pairing
read. Renamed from "Rescue", which was too close to Endurance and implied healing when the top of
the axis is not healing at all.

Four things count, and they are not equal in a duo:

| form | examples | duo value |
|---|---|---|
| **Prevention** | Death Ward, Sanctuary on the partner | full — stops the loss before it happens |
| **Restoration** | Revivify, Raise Dead, Lesser/Greater Restoration, condition removal | full — a Held partner is 50% of the action economy |
| **Outward healing / temp HP** | Healing Word, Cure Wounds aimed out, Aid, Beacon of Hope, Twilight Sanctuary | full, and Lone Wolf's halved damage **doubles every point** |
| **Damage redirection** | Warding Bond, Peace's Protective Bond, Mesmerist Reflection | **discounted — see below** |

| | |
|---|---|
| **0** | Nothing aimed at the partner. |
| **1** | Damage redirection only. |
| **2** | Outward healing off long-rest slots. |
| **3** | Revival or condition removal available, or repeatable outward healing on a short-rest clock. |
| **4** | **Prevention** on the partner, or a no-action aura that temp-HPs them every round. |
| **5** | Prevention **and** restoration **and** no-action outward healing, on clocks the act can rescue. |

| rung | I | II | III |
|---|---|---|---|
| **2 =** | Healing Word / Cure Wounds aimed outward off long-rest slots | Mass Healing Word or Aura of Vitality — but Aura of Vitality **holds concentration**, so it competes with §5/§6 | 6th-tier and up outward, or a lower-tier heal upcast; a bare Cure Wounds is rung **1** |
| **3 =** | **Revivify** (full caster 5, Artificer 5, Paladin 5) or Lesser Restoration; or repeatable outward healing on a short-rest clock | **Greater Restoration** (5th, caster 9); **Revivify now reaches the Ranger** at spell level 3 (class 9), which removes the "one of us must be Cleric/Paladin/Bard" constraint on pair composition | 9th-tier restoration, Mass Heal, or Legendary rescue gear |
| **4 =** | **Prevention** — Death Ward (4th, caster 7) — or a no-action aura that temp-HPs the partner every round: **Twilight Sanctuary** (Cleric 2), Peace's Emboldening Bond | Rung 4 plus **Flurry of Healing and Harm** (Way of Mercy 11 — every Flurry strike carries a free Hands of Healing outward; Lone Wolf's second bonus action buys two Flurries a round) | Prevention that survives the act's damage, plus a no-action outward source, on a short-rest clock |
| **5 =** | **Twilight Sanctuary** + Revivify (caster 5) + **Death Ward** (4th, caster 7) | + **Greater Restoration** (5th, caster 9) and **Flurry of Healing and Harm** | + 9th-tier restoration off the new slot, Mass Heal, and Legendary gear |

> **Damage redirection is worth far less in a duo than its reputation.** Warding Bond and
> Protective Bond are strong in a four-party because they move damage onto a **spare** body. You
> have no spare — they move it from one half of your party to the other half. Net zero at best,
> actively bad when it lands on the squishier one, and `data/classes/bard.md:298` already warns
> that the Warding Bond caster is the one who dies. **Never score redirection above rung 1 on its
> own.**
>
> **Twinned Spell makes this axis cheap for a Sorcerer.** `data/classes/sorcerer.md:477` calls out
> Twinned Death Ward, Twinned Warding Bond and Twinned Greater Restoration, and a two-person party
> means Twinned covers *everyone*. A Sorcerer 3 dip buys a rung here that costs other chassis six
> levels.
>
> **Short Rest Full Heal is OFF** and Camp Cost is 3, so out-of-combat outward healing counts here
> *and* raises the partner's Endurance. Score the clock, not the burst size.

## 8. Skills

Out-of-combat coverage. Judge against the **named gates that exist in that act**, not a
proficiency count — this axis is the most strongly act-gated of the ten.

**`gates.md` owns the gate list** — every act, DC, cost and reward, and which mods change them.
The rows below name only the gates that are *paid in a skill check*; most gates are not, and what
they buy usually lands on another axis. Do not restate a gate's numbers here.

| | |
|---|---|
| **0** | Two or three skills, no Expertise, and the dump stat sits behind them. |
| **1** | Four or more skills, no Expertise. |
| **2** | Expertise ×1, or a broad list with a real ability behind it. |
| **3** | Expertise ×2 plus Guidance at will. |
| **4** | Expertise ×2, Guidance, and all but one of the act's named gates cleared. |
| **5** | Every named gate in that act cleared. |

| rung | I | II | III |
|---|---|---|---|
| **skill gates** | **Hag's Hair, DC 20** — **Deception or Intimidation**, one per run | **Potion of Everlasting Vigour** — pickpocket Araj (Sleight of Hand); plus passive Perception for hidden content | **Mirror of Loss, Religion DC 25**, and the **pickpocket-only** second Phalar Aluve music box in the Circus (Sleight of Hand) |
| **2 =** | Expertise ×1, or five-plus skills behind a 16+ ability | The same plus Guidance at will — a broad list with no Expertise is now rung 1 | The same; with no answer to a DC 25 a body **cannot exceed 2**, however many proficiencies it holds |
| **3 =** | Expertise ×2 (Bard/Rogue 3) + Guidance | + **Reliable Talent** (Rogue 11) or Lore's Peerless Skill — floor-raising, not just bonus-raising | + **Elevated Mind** (illithid: Expertise *and* proficiency in every skill of one ability, re-selectable) |
| **4 =** | Expertise ×2 + Guidance + **Hag's Hair cleared** on the host body | + a Sleight of Hand body for Araj and passive Perception in the 20s | All but one of the act's named gates — typically the Mirror or the Circus box |
| **5 =** | Expertise ×2 (Bard/Rogue 3) + Guidance + a check that clears DC 20 | + a Sleight of Hand body + passive Perception in the 20s | + an Intelligence skill that clears DC 25, or Forbidden Knowledge spent to bypass it |

> **Persuasion does not open Hag's Hair** — the check is Deception or Intimidation, and Fighters
> and Barbarians get an easier **Intimidation DC 15 with advantage** instead. **Stern Gaze**
> (Inquisitor) lets Intimidation use **Wisdom instead of Charisma**, the only non-Charisma route
> in the list. Vengeance's **Monster Tactician** grants Expertise in an Intelligence skill *and*
> double Wisdom modifier on it, which clears the Mirror's DC 25 outright.

> **The gate rows above assume the host makes the roll.** `Use Highest Modifier in dialogue` and
> `Use Best Sleight of Hand` hand the party-best total to `GetHostCharacter()` only, so a gate
> cleared by the non-host body is not cleared at all. The ability and the proficiency must still
> sit on the *same* body, and the flat bonus does **not** carry proficiency — **Reliable Talent**
> and **Silver Tongue** stay with whichever body owns them. Full mechanics in `gates.md`.

## 9. Saves

This body's own resistance to being removed. Weight the abilities: **Wisdom > Constitution ≈
Dexterity > Charisma > Strength > Intelligence** — and **Constitution takes the top slot on any
body that holds concentration**, since a broken concentration is a lost body one turn later.

| | |
|---|---|
| **0** | Two proficient saves, both low-value (Str, Int), no booster. |
| **1** | Two proficient saves, one of them Wis / Con / Dex. |
| **2** | Three **disjoint** proficient saves including one of Wis / Con / Dex. |
| **3** | Four disjoint proficient saves covering two of Wis / Con / Dex. |
| **4** | Four or more disjoint saves covering **all three** of Wis / Con / Dex, or a blanket booster. |
| **5** | The act's best available blanket coverage on top of a disjoint four. |

Enemy DCs are the one thing that genuinely climbs — **boss spell save DC +1 / +2 / +2** across the
acts — so this is the axis where standing still costs the most.

| rung | I (boss DC +1) | II (+2) | III (+2, and 9th-tier effects) |
|---|---|---|---|
| **2 =** | Three disjoint proficient saves including one of Wis / Con / Dex | The same, but three disjoint with **no booster** is thin against the act's DCs | Three disjoint alone falls to **1**; par is four disjoint or three plus a booster |
| **3 =** | Four disjoint covering two of Wis / Con / Dex | Four disjoint covering two, **plus** a booster or a save-relevant item | Four disjoint covering all three, without a blanket source |
| **4 =** | All three of Wis / Con / Dex covered, **or** a blanket booster — Aura of Protection (Paladin 6), Brutish Durability (Fighter 7) | **Diamond Soul** (Monk 14 — all six proficient) or Slippery Mind (Rogue 15) | Psychic Fortress at IMR 4–5 (+IMR to Int/Wis/Cha saves) on top of a disjoint four |
| **5 =** | Four disjoint (level-1 class pair + Lone Wolf's two) covering Wis/Con/Dex **plus Aura of Protection** or Brutish Durability | Diamond Soul or Slippery Mind on top of a disjoint four | Diamond Soul or a disjoint four **and** a partner's Aura, plus Legendary save gear from the 5-item attunement budget |

> Sources are the **level 1 class only** (two saves, lost silently on respec) and **Lone Wolf's two
> picks**, plus Resilient, which is repeatable. They must be **disjoint** to count — Blood Hunter's
> Int + Dex duplicating a Lone Wolf Int + Dex pick wastes both.
>
> **Auras do not stack**: a second Paladin 6 on the other body buys nothing. This is a *pair*
> effect — record it as a flag, not as this body's own score.
>
> `Sensible Ambushing` makes surprise a flat **DC 15 Wisdom save** applying to both sides — one
> more reason Wisdom leads the ordering.

## 10. Endurance

How many hard fights the body's resource budget covers per long-rest cycle. **Two short rests per
long rest**, so a short-rest pool is spent **three times** per cycle — the initial fill plus two
refreshes, not indefinitely.

This axis drifts least — a clock is a clock at every level — but it does **not** hold still, and the
previous version of this ladder named class levels as rungs (Warlock 11, Paladin 17, Monk 14),
which put every rung above 1 out of reach in Act I and left the axis unable to discriminate there
at all. The ladder below is stated in **shapes**; the class levels moved into the act table where
they belong.

| | |
|---|---|
| **0** | Long-rest resources only, spent by the second hard fight, no at-will fallback. |
| **1** | Long-rest resources that stretch to about three fights, still no short-rest pool. |
| **2** | A **small short-rest pool** on top of slots — refilled twice, so spent three times per cycle. |
| **3** | A large short-rest pool, **or** a long-rest pool covering four to five fights, plus out-of-combat healing. |
| **4** | A short-rest pool that covers a hard fight **on its own**, refilled twice. |
| **5** | **Unbounded** — the damage is at-will with no clock: Rogue Sneak Attack, Champion / Battle Master Fighter, Blood Hunter Crimson Rite. |

| rung | I (char 3–8) | II (9–15) | III (16–20) |
|---|---|---|---|
| **2 =** | Warlock 3–5 (2 pact × 3 = **6 units**), Battle Master's 4 dice × 3 = **12**, or Second Wind + Action Surge | Warlock 11 (3 pact × 3 = **9**); a full caster's ≈14–16 slots is now only rung 1–2 | Paladin 17 ≈ **15 slots**; a full caster's long-rest table alone no longer clears rung 2 |
| **3 =** | Monk 5–8 (6–9 ki × 3 = **18–27**), or slots **plus** Song of Rest (Bard 2) | Bard 15 ≈ **18 slots**, or a short-rest pool plus out-of-combat healing | Cleric 18 ≈ **21 slots** — four to five fights |
| **4 =** | A short-rest pool large enough that one fight does not empty it — Monk 8's ki, Ki-fuelled healing between fights | **Monk 14**: 14 ki × 3 = **42** at 8–10 per hard fight, plus ki healing | **Monk 20**: 21 ki × 3 = **63**; or a short-rest engine plus Illithid charges *not* leaned on |
| **5 =** | At-will damage with no clock — **act-invariant, and that is the point**: it is why martials own this axis in every act | The same | The same |

> **Illithid charges cut against this axis.** `2.5 + 0.5 × powers` per long rest, only half back on
> a short rest — a chassis that funds its tempo from charges is buying Act III damage with Act III
> rests. Score the drop.
>
> **Hit points force more long rests than slots do.** Count out-of-combat healing in this budget:
> ki healing and Song of Rest raise Endurance; a pool that only refreshes on a long rest does not.
>
> **A Paladin 17's own table beats a Warlock 7 dip.** `Paladin 17 / Warlock 3` holds ≈21 units
> against `Paladin 13 / Warlock 7`'s ≈18. Take a short-rest dip for Hex Warrior, Hexblade's Curse
> or a familiar — not for the clock.

---

## Illithid powers across the axes

IPO2 is live (`data/listo-10.2-illithid.md`). Powers **fill** rungs on the axes above; they never
create rungs of their own, and no power is worth a rung in an act it cannot exist in.

**The rungs above are authored illithid-free, and stay that way.** Every body may spend tadpoles,
so a uniform uplift would move every chassis together and mean nothing. What moves a row is
**differential conversion** — a body that turns the same share of the pool into more than its
neighbours do. Score against the **even share**, roughly **IMR 1 / 2 / 4** by act, and ask what
this body gets out of it that another would not: a cheap Action, a real casting stat on the last
class added, an idle reaction, armour that shrugs off the tax, or a missing damage type that
Psychic and Force fill. `listo-ledger` SKILL.md has the full both-ways table.

**What the act allows.** Nothing before the first tadpoles are spent. Only the outer 15 powers
exist before the Astral-Touched Tadpole, so **IMR is capped at 3 through Acts I and II** whatever
the tadpole count; the inner ring and IMR 4–5 arrive in one step at the **start of Act III**. A
duo can fund about 12 powers between both bodies through Act I and about 24 through Act II, so
IMR 1–2 is the realistic Act I holding on the body that gets the share.

**What a charge pool can support.** `2.5 + 0.5 × powers` per long rest, half back per short rest,
against costs of 2–5. Below about IMR 3 an illithid power is a **per-fight burst**, which is rung 2
on AoE and cannot be read as the repeatable rung 3. At IMR 4–5 the pool reaches 12.5–15 and, with
Astral Stillness discounting every cast by 1, it becomes a genuine repeatable engine.

| Axis | What illithid can anchor | Needs |
|---|---|---|
| **Single-target** | Concentrated Blast 6d6 or Stage Fright 5d6 as a third damage source beside the attack routine; Psionic Overload as a rider on every offensive action; Fracture Psyche's vulnerability window | rung 4 at IMR 4+; **rung 3 rider at IMR 2–3** |
| **AoE** | Mind Blast 7d8 in a cone, half on a save; Cull the Weak's overkill spread executing under 2×IMR HP | Act III for Mind Blast; Cull the Weak reaches rung 2–3 in Act II |
| **Durability** | Eldritch Ward's flat `IMR` reduction against AoE, ranged and spells, plus its Shield-like interrupt; Transfuse Health; Cerebral Citadel armour's +1 AC per 5 powers | Ward is rung-worthy from IMR 2; **subtract the `+IMR` physical-damage tax** at every rank |
| **Actions** | Astral Stillness — every power 1 charge cheaper, free casts every `10 − IMR` stacks; Awakened making Force Tunnel free | Act III |
| **Control (single)** | Psionic Dominance = Dominate Person, **no concentration**; Psionic Backlash as a repeatable counterspell to level IMR+1; Ability Drain | Act III. **No-concentration control is the rung-4 clause in §5** |
| **Control (area)** | Black Hole's pull with Prone and guaranteed Dazed 2; Mind Flayer's Insanity stacks; Repulsor | Black Hole is Act III; Repulsor and Mind Flayer are Act I/II rung-2 material |
| **Rescue** | Shield of Thralls outward | thin — illithid is a poor rescue answer at every rank |
| **Skills** | Elevated Mind: Expertise **and** proficiency in every skill of one ability, permanent and re-selectable — a rung on its own; Peace Breaker's +IMR+1 on the first Persuasion, Deception or Intimidation check | Elevated Mind is Act III; Peace Breaker is a **rung-1 to rung-2 lift from Act I** |
| **Saves** | Psychic Fortress: Psychic resistance plus **+IMR to Intelligence, Wisdom and Charisma saves**; Eldritch Ward's interrupt on a failed save | +3 at IMR 3 is a full rung against Listo's inflated DCs |
| **Endurance** | nothing — illithid **costs** Endurance. A build leaning on charges burns a long-rest pool that only half-refills on a short rest | — |

> Two power sources are commonly mis-scored. **Transfuse Health heals only the caster** — it is
> Durability, never Rescue. And **Peace Breaker is consumed by the first attack roll or check**, so
> it is a Skills anchor — a one-shot +6 on an opening check — not a damage one, whatever its
> `RollBonus(Attack)` suggests.

---

## Applying these

1. **Fix the level order first.** Act scores come from where a feature actually lands in the
   levelling ladder, not from the final build. A chassis that defers its Cleric block scores its
   Act I on what it has at character 7, whatever it ends up as.
2. Score each body against **that act's row in the axis table**, ignoring its partner entirely.
   Rungs 0–1 have no act row; every rung from 2 up does, and a capability that was rung 3 in Act I
   is often rung 2 in Act III without anything having changed about the chassis.
3. **Check the budget.** Total the feats and levels the 4s and 5s imply against that act's
   allowance — **2 feats in Act I, 5–6 by Act II, 7–8 by Act III**. If they exceed it, or leave the
   primary below 20-by-6 / 22-by-18, lower a score rather than hand-wave it. Act I is the binding
   band: two feats cannot buy two 5s.
4. Watch what **loses** a rung across acts:
   - anything **flat-magnitude** — a 1d6 rider keeps about two-thirds of its relative value from
     the end of Act I to the end of Act III;
   - **Eldritch Cone** AoE, which stops scaling at character 10 outright;
   - anything locked to **one damage type** once Absolute Wrath's layered resistances appear;
   - a **three-disjoint save set** with no booster, as boss DCs climb;
   - **flat-only mitigation** in a boss-weighted act.

   And what does **not**: Advantage/Disadvantage, proportional mitigation, attack counts, summons
   (allies scale too), at-will damage — and **save-DC control**, which the old version of this list
   wrongly included. See the correction under "What actually drifts".
