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

> **§1 and §2 are the exception.** The two damage axes are computed as a ratio to a fixed reference
> body, so their act scores *are* comparable and a declining row means the chassis is being outrun.
> Everything below applies to §3 through §10.

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
  and it is the main reason a chassis can fall between acts. **On §1 and §2 this is already in the
  ratio** — par carries the HP multiplier, so a flat rider slides on its own. Apply the rule of
  thumb only to §3 through §10.
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
levels, and one primary stat that must hit **20 by character 6 and 22 by 18**. (`Feats Overhaul`
removes the 20 cap on every feat-granted increase except the plain ASI, so 22 is reached by
stacking half-feats — `Enweaved` is merely the only **+2** one, and it offers WIS, CHA or INT
alone.) A 5 on any axis
is priced in that act's budget, and in Act I two 5s essentially cannot coexist — there are two
feats. When a body scores 5, check what it gave up; if nothing, the score is wrong.

**Lone Wolf is baseline, not a bonus.** For this run it is enabled in non-feat mode, so every
body already has 2 Actions, 2 Bonus Actions, 2 Reactions, halved damage from all sources, and +4
to *two* abilities with save proficiency in both, **from level 1**. Score what the chassis adds
**above** that floor in every act. (`GOON_LONE_WOLF_STATUS`; +30% max HP is a separate MCM toggle
— if `enableHpMax` is off, effective HP is 2.0× per body rather than 2.6×.)

---

## The two damage axes are computed, not judged

§1 and §2 are **ratios to a fixed reference body**, not configuration checklists. The old ladders
counted components — multiattack, rider, bonus-action strike — as if each were worth the same. They
are not: Improved Extra Attack adds about half a body's damage, Hex adds under a tenth of it by
Act III, and the old rungs scored both as one step. Worse, a level-gated rider (Monk's Martial Arts
die at 1/5/11/17, Rogue's Sneak Attack die every two levels) is invisible to a checklist, so a
split that stops one level short of a breakpoint paid no price.

### Constants

| | value | note |
|---|---|---|
| hard fight | **4 rounds** | |
| hit chance `h` | **0.65** | a **convention, not a measurement**. Enemy AC is not recoverable from the manifest: `Character.txt` declares `Armor` for only 245 of 1,548 entries and carries no `Equipment` field at all, so real AC lives in root-template gear. `h` cancels between chassis and par wherever both roll attacks, which is why the convention is safe. |
| save-fail chance `s` | **0.55** | act-invariant — our DC rises +4 across the run against +2 to +3 on enemy saves |
| save-for-half multiplier | `s + (1−s)/2` = **0.775** | |
| AoE targets | **4** | act-invariant. `scoring-model.md` §5's crowd/boss coefficients already carry fight shape; scaling target count here as well would double-count it. |

### Par

Par is the act's **reference body**: Extra Attack, two attacks per Action, no rider, no damage
feat, a mundane 2d6 weapon, primary at the act's required score. Its configuration never improves.
What changes is the enemy.

| | I (char 8) | II (char 15) | III (char 20) |
|---|---|---|---|
| attacks per round (Lone Wolf ×2 Actions) | 4 | 4 | 4 |
| attack stat / damage per hit | 20 / 12 | 20 / 12 | 22 / 13 |
| enemy HP multiplier | ×1.54 | ×1.96 | ×2.26 |
| **par — single-target** | **48** | **61** | **76** |
| **par — AoE** | **22** | **28** | **32** |

Single-target par is `attacks × damage per hit`, multiplied by that act's enemy HP relative to
Act I's.

> **The row is the ATTACK stat, which for a third of the roster is not the chassis's primary.**
> A Monk's Wisdom drives AC, the Ki Save DC and its Way's scaling while **Dexterity** rolls the
> attack; the same split runs through Paladin (Cha/Str), Inquisitor (Wis/Str), Mesmerist (Cha/Dex),
> Artificer outside Battle Smith (Int/Dex) and Paragon outside Spellblade (Cha/Str). Score the
> damage off the stat that rolls it. Reading the primary here charges a body a modifier it does
> not actually lose — Lone Wolf's +4 lands on **two** abilities, so both stats reach 20 at level
> 1, and a body that puts its 22 on the attack stat is at par on the modifier and ahead on the
> attack count. The exceptions run the other way and are worth knowing: **Way of the Astral Self**
> and **Battle Smith** put attack *and* damage on the caster stat, and **Shillelagh** does it for
> a Druid's club or quarterstaff. AoE par is one **Fireball** (8d6) per fight on four targets, save for half, spread over
the fight — `28 × 0.775 × 4 ÷ 4 = 22` — scaled the same way.

Damage is carried **raw**, before `h`. Multiply by `h` only where a chassis resolves differently
from par: a save-based single-target effect takes `0.775/0.65`, an attack-roll AoE takes
`0.65/0.775`.

> **§1 and §2 are comparable across acts. No other axis is.** The unit is pace against Act I's
> baseline, so a frozen chassis reads 2 / 1 / 1 and that decline is real information — it is being
> outrun. The act-relative rule at the top of this file still governs §3 through §10.

### Four rules

1. **No items.** Mundane weapons, no attunement, no Legendary. A rented capability is not a chassis
   property — the same objection that removed the Mirror of Loss from §8.
2. **Lone Wolf floor economy only** — 2 Actions and 2 Bonus Actions. **Exclude Action Surge,
   summons and extra bodies.** Those are §4, and `scoring-model.md` §6 applies Actions as a *cap* on
   deployable tempo; counting them here as well scores them twice.
3. **One configuration.** Score the build as actually played, never the union of its options.
   Mutually exclusive picks — which Friar Blessing, Kensei versus unarmed, the single concentration
   slot — must be chosen before scoring and named in the chassis note.
4. **Resistance is a multiplier, not a cap.** Absolute Wrath is on. A body locked to one commonly
   resisted damage type multiplies by **0.5** on the share of encounters that resist it — assume
   **half** from Act II — unless it carries a resistance strip, Elemental Adept, or a second damage
   type. Force is least resisted, then Radiant in Act 2.

### Spending resources

**Three hard fights per long-rest cycle, four rounds each — twelve combat rounds.** The constant is
§10's own arithmetic: two short rests per long rest, so a short-rest pool is spent three times per
cycle.

What one fight has to spend:

| resource | refresh | available per fight |
|---|---|---|
| ki, pact slots, Channel Divinity, superiority dice | short rest | **the full pool** |
| levelled spell slots, Second Wind, anything once per long rest | long rest | **pool ÷ 3** |
| illithid charges — `2.5 + 0.5 × powers`, half back on a short rest | mixed | **2 × pool ÷ 3** |
| once per battle (Cleansing Wave) | per fight | the full allowance |

```
spend per fight  = min(available per fight, what four rounds of actions can consume)
damage per round = at-will damage + (spend per fight × damage per unit) / 4
```

**The action cap usually binds before the pool does.** A Monk 12 holds 12 ki, but two Flurries a
round across four rounds consumes 8 — the constraint is bonus actions, not ki. A full caster holds
far more slots than 2 Actions × 4 rounds can cast. Compute both and take the smaller.

Where a strong *configuration* still scores a rung lower is the other direction, when the pool
binds first: **a Monk 5 has 5 ki against the 8 that double Flurry wants**, so it delivers about
six attacks a round, not eight.

> **Do not key the fight count to the body's own §10 rung.** An earlier draft did, and it inverts:
> two chassis holding the same twenty slots would amortize differently because one of them has
> out-of-combat healing, and the *worse*-supplied body would book the larger per-fight burst.
> Endurance asks whether the pool covers the run. §1 and §2 ask what the pool yields per round. Same
> pool, two different questions, one shared constant — and no circular reference between the axes.

**One pool, one axis.** A slot spent on Fireball is not available for Hold Monster or Death Ward.
Rule 3 applies: name the split in the chassis note. Absent a note the default is **half the levelled
slots to damage**, half to §5/§6/§7. A damage effect that holds concentration — Spirit Guardians —
occupies one of the pair's two slots, so §5/§6 may not also claim it.

---

## 1. Single-target

Damage into one priority target per round, with both Lone Wolf Actions spent on it.

`ratio = damage per round ÷ single-target par`

| rung | ratio | reads as |
|---|---|---|
| **0** | < 0.5 | not a damage body |
| **1** | 0.5 – 0.8 | being outrun |
| **2** | 0.8 – 1.15 | par |
| **3** | 1.15 – 1.5 | ahead |
| **4** | 1.5 – 2.0 | a damage chassis |
| **5** | ≥ 2.0 | the act's ceiling |

Worked anchors, raw damage per round over par:

| configuration | I (par 48) | II (par 61) | III (par 76) |
|---|---|---|---|
| Extra Attack, no rider | 48 → 1.00 → **2** | 48 → 0.79 → **1** | 52 → 0.68 → **1** |
| Extra Attack + flat 1d6 rider (Hex, Crimson Rite) | 62 → 1.29 → **3** | 62 → 1.02 → **2** | 66 → 0.87 → **2** |
| Improved Extra Attack (Fighter 11), no rider | — | 72 → 1.18 → **3** | 78 → 1.03 → **2** |
| Sneak Attack ×2 (turn + one reaction) + 4 attacks | 59 → 1.23 → **3** | 80 → 1.31 → **3** | 112 → 1.47 → **3** |
| Monk: Extra Attack + double Flurry, Martial Arts die | 45 → 0.94 → **2** | 76 → 1.25 → **3** | 84 → 1.11 → **2** |
| Improved Extra Attack + scaling rider + 2 bonus strikes | — | 124 → 2.03 → **5** | 132 → 1.74 → **4** |

> **Improved Extra Attack almost exactly cancels the run's HP inflation.** +50% attacks against
> +47% enemy HP from Act I to Act III. Fighter 11's signature feature buys *pace*, not advantage —
> which is why a bare Fighter 11 reads 2, not 5. It still outscores an equivalent two-attack body
> in every act, which is the ordering that matters.

> **A flat rider decays and the arithmetic shows it** — 1d6 on four attacks is 1.29× par in Act I
> and 0.87× in Act III with nothing having changed. Do not also apply a hand-written decay rule;
> that would charge for it twice. Riders that scale with level or dice count (Sneak Attack,
> Improved Divine Smite) hold their ratio.

> **Cantrips scale on character level, not class level.** Eldritch Blast is **1d8 per beam here,
> not 1d10** (v10.0 nerf), with beams at **character** 5/10/17 and a fourth from `Expansion`;
> Booming Blade and Green-Flame Blade likewise (`data/listo-10.2-spells.md:142`). **A two-level
> Warlock dip on a character-20 body fires four full beams** — 4 × (1d8 + Cha) × 2 Actions ≈ 60
> raw, or 0.79× par, from two levels. Magic Initiate buys a martial a character-level-scaling melee
> rider for one feat. Configuration ladders could not see any of this; ratios must.

## 2. AoE

Damage delivered to a group per round, and how often it is available. Same unit as §1, against a
par of one Fireball per fight on four targets.

`ratio = damage per round across all targets ÷ AoE par`

The bands are **wider than §1's** because at-will area damage delivered twice a round outruns a
once-per-fight burst by far more than any single-target engine outruns another.

| rung | ratio |
|---|---|
| **0** | < 0.35 |
| **1** | 0.35 – 0.7 |
| **2** | 0.7 – 1.3 |
| **3** | 1.3 – 2.0 |
| **4** | 2.0 – 3.0 |
| **5** | ≥ 3.0 |

Worked anchors:

| configuration | I (par 22) | II (par 28) | III (par 32) |
|---|---|---|---|
| an incidental cleave or two-target cantrip | 8 → 0.36 → **1** | 8 → 0.29 → **0** | 9 → 0.28 → **0** |
| one Fireball (8d6) per fight | 22 → 1.00 → **2** | 22 → 0.79 → **2** | 22 → 0.69 → **1** |
| one Cone of Cold (8d8) per fight | — | 28 → 1.00 → **2** | 28 → 0.88 → **2** |
| one Chain Lightning (10d8) per fight | — | — | 35 → 1.09 → **2** |
| Spirit Guardians, at-will while concentration holds | — | 42 → 1.50 → **3** | 42 → 1.31 → **3** |
| Volley / Whirlwind (Ranger 11), ×2 Actions | — | 49 → 1.75 → **3** | 55 → 1.72 → **3** |
| Breath of the Dragon (Monk 3), ×2, net of the replaced attack | 41 → 1.86 → **3** | — | — |
| Consuming Fervor: maximised Fireball ×2 per short rest | 74 → 3.4 → **5** | 74 → 2.6 → **4** | 74 → 2.3 → **4** |
| Eldritch Cone (Warlock 9), at-will, ×2 Actions | — | 102 → 3.6 → **5** | 102 → 3.2 → **5** |

> **The old note that Eldritch Cone "drops a rung in Act III" was wrong, and the arithmetic is why.**
> `Zone_EldritchCone` reads `LevelMapValue(EldritchZoneDamage)` — 1d10 at 1–4, 2d10 at 5–9, **3d10
> from 10, where it ends** — and its `SpellSuccess` never checks `AgonizingBlast`, so the effect is
> frozen at 16.5 average from character 10. It **does** decay: 3.6× par to 3.2×. It does not decay
> across a band, because at-will four-target save-for-half damage twice a round is the strongest
> area engine in the list and a 14% slide does not touch that. Record the decay; do not invent a
> rung drop.

> **Repeatability outranks per-cast size, and the amortization is where it shows.** A 9th-tier
> burst spread over four rounds is a fifth of its headline number. This is the same principle the
> axis always claimed; it is now arithmetic rather than assertion.

> Consuming Fervor is `MinimumRollResult(Damage,20)` on Fire **or Thunder**, Channel Divinity, twice
> per short rest at Cleric 6 — effectively a maximised 8d6.

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

**Not authored.** This axis is derived from `skills` — the finished modifier a body rolls on each
check, per act — and `scoring.py` owns the arithmetic. There is no 0–5 judgement to make here.
Record the modifiers; the rung falls out.

### What it measures, and why it changed

It used to score the run's **named gates**: Hag's Hair, the Araj pickpocket, the Mirror of Loss.
That was the wrong target, for two independent reasons.

**The named gates are buyable.** Withers charges 100 gold and sits in the Dank Crypt from Act I.
bg3.wiki documents respeccing into Rogue 11 / Knowledge Cleric 1 for Religion Expertise, passing
the Mirror at DC 25, then respeccing back *"retaining the Mirror of Loss stat enhancement"*. A
check any chassis can rent its way past is not a chassis property, so **the Mirror is no longer
scored at all**.

**The named gates are also bypassable.** Each has a no-check route to the same ability point —
taking Ethel's deal yields the hair and costs only Mayrina, and Araj can simply be killed and
looted. Passing buys the *secondary* prize, not the +1 or +2.

What survives both objections is the untelegraphed half of the run, scored every act:

| check | skill | DC |
|---|---|---|
| traps and hidden caches | **Perception** | 15–25 |
| secret doors and switches | **Investigation** | 15–20 |
| routine town dialogue | **Persuasion** | **I** 10–15, **II** 15–18, **III** 18–22 |

These fire without warning, in whatever build is worn. Nothing prepares for them, so they measure
the chassis. Hag's Hair and the Araj pickpocket are still scored alongside them, at lower weight
in practice because they are one check each against three recurring ones.

### How the rung is computed

Each check takes the pair's **better body** — `Use Highest Modifier in dialogue` puts the host on
the party-best skill total, `Use Best Sleight of Hand` does the same for pickpocket and trap
disarm, and either character can walk into a trap. Nothing here is personal.

**Inspiration applies to the named gates only.** Traps roll automatically with no prompt, so there
is nothing to spend a charge on, and four charges do not stretch across a run of town dialogue.

The rung is then the **mean clear probability** across the act's checks, capped by its worst:

| mean | rung |  | cap |
|---|---|---|---|
| ≥ 0.75 | **5** |  | worst check < 0.10 → rung ≤ **2** |
| ≥ 0.65 | **4** |  | worst check < 0.25 → rung ≤ **3** |
| ≥ 0.55 | **3** |  | |
| ≥ 0.40 | **2** |  | |
| ≥ 0.25 | **1** |  | |
| below | **0** |  | |

The mean asks how much of the act's check load the pair handles. The caps preserve what an
`all`-quantifier was protecting: **a check nobody can roll is a different failure from a check
everyone rolls badly**, and it must not average away.

> **Rung 5 is unreachable, and that is the finding.** The best pair in a 34,980-pairing field
> averages **0.79**, and Perception against the 15–25 trap band peaks at **0.60** for anyone in the
> roster. A two-character Lone Wolf party cannot cover this run's detection load. Expect a good
> duo at 3–4 in Act I and 1–2 by Act III, and read a 4 as excellent rather than adequate.

**Two faces are worth less than a face and a scout.** Charisma covers town dialogue and Hag's
Hair; Wisdom and Intelligence cover traps, caches and doors. Because every check takes the better
body, a duplicate contributes almost nothing — disjoint-class pairs average 6.80 across the three
acts against 5.70 for pairs sharing a class.

> **Persuasion does not open Hag's Hair** — the check is Deception or Intimidation, and Fighters
> and Barbarians get an easier **Intimidation DC 15 with advantage** instead. **Stern Gaze**
> (Inquisitor) lets Intimidation use **Wisdom instead of Charisma**, the only non-Charisma route
> in the list. Vengeance's **Monster Tactician** grants Expertise in an Intelligence skill *and*
> double Wisdom modifier on it — put it on **Investigation** and it is the strongest answer in the
> roster to secret doors and switches. It used to be described here as the clean answer to the
> Mirror of Loss; the Mirror is no longer scored, and the feature only ever reached that DC on a
> body with the Intelligence to back it.

> **Dialogue checks assume the host makes the roll.** `Use Highest Modifier in dialogue` and
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
| **1** | Two or more proficient saves, one of them Wis / Con / Dex. |
| **2** | Three or more **disjoint** proficient saves including one of Wis / Con / Dex. |
| **3** | Four or more disjoint proficient saves covering two of Wis / Con / Dex. |
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
   is often rung 2 in Act III without anything having changed about the chassis. **§1 and §2 are
   computed instead** — take the ratio to that act's par and read the band.
3. **Check the budget.** Total the feats and levels the 4s and 5s imply against that act's
   allowance — **2 feats in Act I, 5–6 by Act II, 7–8 by Act III**. If they exceed it, or leave the
   primary below 20-by-6 / 22-by-18, lower a score rather than hand-wave it. Act I is the binding
   band: two feats cannot buy two 5s.
4. Watch what **loses** a rung across acts:
   - a **three-disjoint save set** with no booster, as boss DCs climb;
   - **flat-only mitigation** in a boss-weighted act.

   And what does **not**: Advantage/Disadvantage, proportional mitigation, summons (allies scale
   too) — and **save-DC control**, which the old version of this list wrongly included. See the
   correction under "What actually drifts".

   **Do not apply any of this to §1 or §2.** Flat-magnitude decay, Eldritch Cone's frozen scaling
   and Absolute Wrath's resistances are all priced inside the ratio already; applying a rule of
   thumb on top charges for them twice.
