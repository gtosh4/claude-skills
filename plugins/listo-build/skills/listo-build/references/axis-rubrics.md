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

| ceiling | I | II | III |
|---|---|---|---|
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

| ceiling | I | II | III |
|---|---|---|---|
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

| ceiling | I | II | III |
|---|---|---|---|
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

| ceiling | I | II | III |
|---|---|---|---|
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

> Combat Extender gives bosses **+1 spell save DC per 7 levels** and enemies +1 per 11, so save-DC
> control decays across the run while Disadvantage-on-saves does not. That gap is why rungs 4–5 sit
> above rung 2 on both ladders, and why a pure save-DC controller **loses a rung between Act II and
> Act III**.

## 5. Control (single)

Removing **one** enemy's turn — the boss answer.

| | |
|---|---|
| **0** | No single-target control. |
| **1** | An incidental rider — Prone from a shove, Repelling Blast (**which now allows a Strength save**). |
| **2** | One single-target concentration control spell off long-rest slots. |
| **3** | That **plus** a repeatable non-concentration rider. |
| **4** | Single-target control that costs no concentration and does not decay as enemy saves scale. |
| **5** | The above plus slot-free hard control on a short-rest clock. |

| ceiling | I | II | III |
|---|---|---|---|
| **5 =** | Hold Person (caster 3) / Command **plus** a repeatable rider — Cunning Strike (Prone/Poison/Disarm every turn), Wrath of the Storm | **Brand of the Sapping Scar** (ProfaneSoul 11 — blanket Disadvantage on the branded creature's saves, free interrupt, no concentration) or Vengeance's Divine Scourge, **plus Chains of Carceri** (`Invocations Expanded`, Warlock 12 — Hold Monster, once per short rest, no slot) | + 9th-tier single-target control off the new slot (Power Word Kill, Dominate Monster) and riders from Legendary attunement gear |

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
| **4** | Area control that costs no concentration, or that does not decay as enemy saves scale. |
| **5** | Slot-free repeatable area control on a short-rest clock. |

| ceiling | I | II | III |
|---|---|---|---|
| **5 =** | Hypnotic Pattern / Web / Grease (caster 5) plus a surface or shove routine | Evard's Black Tentacles, Sleet Storm, Spirit Guardians as area denial, on a repeatable clock | + 9th-tier area control off the new slot |

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

| ceiling | I | II | III |
|---|---|---|---|
| **5 =** | **Twilight Sanctuary** (Cleric 2 — 9m sphere, 1d6 + Cleric level temp HP to everyone ending turn inside, **or** end one charm/fright; one Channel Divinity, short-rest refresh) + Revivify (caster 5) + **Death Ward** (4th, caster 7) | + **Greater Restoration** (5th, caster 9) and **Flurry of Healing and Harm** (Way of Mercy 11 — every Flurry strike carries a free Hands of Healing outward; Lone Wolf's second bonus action buys two Flurries a round) | + 9th-tier restoration off the new slot, Mass Heal, and Legendary gear |

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
proficiency count — this axis is the most strongly act-gated of the nine.

| | |
|---|---|
| **0** | Two or three skills, no Expertise, and the dump stat sits behind them. |
| **1** | Four or more skills, no Expertise. |
| **2** | Expertise ×1, or a broad list with a real ability behind it. |
| **3** | Expertise ×2 plus Guidance at will. |
| **4** | Expertise ×2, Guidance, and all but one of the act's named gates cleared. |
| **5** | Every named gate in that act cleared. |

| ceiling | I | II | III |
|---|---|---|---|
| **gates** | **Hag's Hair, DC 20** (one per run) | passive Perception for hidden content; no unique named gate | **Mirror of Loss** (+2 chosen, +1 Cha — needs an Intelligence skill), and the **pickpocket-only** second Phalar Aluve music box in the Circus (Sleight of Hand) |
| **5 =** | Expertise ×2 (Bard/Rogue 3) + Guidance + a check that clears DC 20 | + passive Perception in the 20s | + a Sleight of Hand body **and** an Intelligence skill |

> **Stern Gaze** (Inquisitor) lets Intimidation use **Wisdom instead of Charisma** — the only
> non-Charisma route to Hag's Hair in the list. Vengeance's **Monster Tactician** grants Expertise
> in an Intelligence skill *and* double Wisdom modifier on it, which buys Mirror of Loss outright.

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

| ceiling | I | II | III |
|---|---|---|---|
| **5 =** | Four disjoint (level-1 class pair + Lone Wolf's two) covering Wis/Con/Dex **plus Aura of Protection** (Paladin 6: +Cha mod to every save **on both characters**, 9m) or Brutish Durability (Fighter 7: +1d6 to **every** save, unconditional, no resource) | **Diamond Soul** (Monk 14 — all six proficient) or Slippery Mind (Rogue 15) on top of a disjoint four | Diamond Soul or a disjoint four **and** a partner's Aura, plus Legendary save gear from the 5-item attunement budget |

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

This is the most act-stable axis: a clock is a clock at every level, so the rungs move least.

| | |
|---|---|
| **0** | Long-rest slots only, 4–5 per hard fight, no at-will fallback — roughly two fights. |
| **1** | Warlock 3 / 5 / 7: 2 pact slots × 3 = **6 units** per cycle. |
| **2** | Warlock 11+: 3 pact slots × 3 = **9**; or Bard 15 ≈ **18 slots** at 4–5 per fight. |
| **3** | Paladin 17 ≈ **15 slots**, Cleric 18 ≈ **21** — four to five fights. |
| **4** | Monk 14: 14 ki × 3 = **42** at 8–10 per hard fight, **plus** ki healing between fights. |
| **5** | **Unbounded** — the damage is at-will with no clock: Rogue Sneak Attack, Champion / Battle Master Fighter, Blood Hunter Crimson Rite. |

> **Hit points force more long rests than slots do.** Count out-of-combat healing in this budget:
> ki healing and Song of Rest raise Endurance; a pool that only refreshes on a long rest does not.
>
> **A Paladin 17's own table beats a Warlock 7 dip.** `Paladin 17 / Warlock 3` holds ≈21 units
> against `Paladin 13 / Warlock 7`'s ≈18. Take a short-rest dip for Hex Warrior, Hexblade's Curse
> or a familiar — not for the clock.

---

## Applying these

1. **Fix the level order first.** Act scores come from where a feature actually lands in the
   levelling ladder, not from the final build. A chassis that defers its Cleric block scores its
   Act I on what it has at character 7, whatever it ends up as.
2. Score each body against the act's own ceiling row, ignoring its partner entirely.
3. **Check the budget.** Total the feats and levels the 4s and 5s imply against that act's
   allowance — **2 feats in Act I, 5–6 by Act II, 7–8 by Act III**. If they exceed it, or leave the
   primary below 20-by-6 / 22-by-18, lower a score rather than hand-wave it. Act I is the binding
   band: two feats cannot buy two 5s.
4. Watch the axes that **lose** a rung across acts: pure save-DC control (enemy DCs climb),
   Eldritch Cone AoE (stops scaling at character 10), and anything locked to one damage type once
   Absolute Wrath's layered resistances appear.
