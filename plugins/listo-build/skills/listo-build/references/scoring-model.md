# Listonomicon scoring model

How authored axis values become a pair score. **This file owns the aggregation**; it does not own
what a 0–5 means (that is `axis-rubrics.md`) or what each axis measures (that is `listo-build`
SKILL.md §5a). Renderers implement this file and must not invent rules of their own.

Status: **structure settled, constants provisional.** Every coefficient and weight below is marked
either *derived* (falls out of a game mechanic) or *provisional* (needs calibration against a
re-authored roster). Do not treat provisional numbers as evidence.

## 1. The currency is action points

An action point buys **one** of damage, control, or rescue. That single fact organises the whole
model, because it means those axes cannot be summed as though they happened simultaneously.

| axis | what it does to action points |
|---|---|
| **Actions** | your **supply** of them |
| **Single-target / AoE** | spends yours to remove enemy APs **permanently** — the enemy is dead |
| **Control (single / area)** | spends yours to remove enemy APs **temporarily** |
| **Rescue** | spends yours to restore your own supply |
| **Durability / Saves** | how resistant your supply is to removal |
| **Endurance** | how long your supply lasts across fights |
| **Skills** | outside the economy entirely |

**The pair's job is to remove enemy action points faster than they remove yours.**

This dissolves the old coverage-versus-damage split, which was arbitrary because "coverage"
bundled things that compete for actions (control, rescue) with things that are free and always on
(durability, saves, endurance). Those do not belong on the same side of a ratio.

## 2. Four blocks

| block | axes | what it answers |
|---|---|---|
| **Tempo** | single-target, aoe, control-single, control-area | how fast you remove enemy APs |
| **Resilience** | durability, saves, rescue | how hard your APs are to remove |
| **Duration** | endurance | how many fights your supply covers |
| **Utility** | skills | out-of-combat coverage |

**Rescue sits in Resilience, not Tempo**, even though it spends an action. Its action cost is
already priced by the rubric: the Rescue ladder is ordered *by tempo cost, inverted* — rung 2 is
healing off long-rest slots (costs an action every time), rung 5 is healing that rides the attack
routine and costs none. Scoring it as Tempo would double-count what the rungs already say. The
same holds for Control's rung 4, which is specifically the control that costs no concentration and
no action.

## 3. The enemy-AP-removal square

Damage and control are the same mechanism at different permanence, and both are fight-type shaped:

| | crowd | boss |
|---|---|---|
| **permanent** | AoE | Single-target |
| **temporary** | Control (area) | Control (single) |

Damage was already split this way and control never was, for no principled reason. Splitting
control completes the square and is the only axis that gains a split — see §7.

## 4. Combining two bodies

Operators run on the **raw authored 0–5 integers**, before any normalisation. Complementary's
`⌊lo/2⌋` is only meaningful in the units the rubric was authored in.

| kind | rule | axes | why |
|---|---|---|---|
| **Additive** | `a + b`, uncapped | single-target, aoe | both bodies genuinely both deal damage; delivered through `U()` below |
| **Complementary** | `hi + ⌊lo/2⌋`, **no cap** (natural max 7) | control-single, control-area, actions, rescue, skills | one is enough, two is better |
| **Personal** | `min(a, b)` | durability, saves, endurance | you fail at the level of your worse half |

**No cap on complementary** is *derived*: capping at 5 makes `5+4` and `5+0` identical, which
reintroduces exactly the saturation that made a plain maximum wrong. A pair must be able to exceed
what one body achieves alone, or the operator contradicts its own justification.

**Personal is derived too.** BG3 has no taunt — enemy AI selects by softness, so the weaker half is
targeted *more*, and with Enemy Critical Hits ON it eats the crits. For Endurance, you long-rest
when *either* half runs dry, at Camp Cost 3.

Control combines **complementary, not additive**, because the pair holds exactly two concentration
slots. That bound is why control costing no concentration is worth a full rung more.

## 5. Fight-type coefficients

Applied *after* combining, to produce a crowd term and a boss term.

| axis | crowd | boss | status |
|---|---|---|---|
| AoE | 1.0 | 0.25 | derived — already in `U()` |
| Single-target | 0.5 | 1.0 | derived — already in `U()` |
| Control (area) | 1.0 | 0.2 | provisional, mirrors AoE |
| Control (single) | 0.3 | 1.0 | provisional, mirrors single-target |
| Rescue | 0.5 | 1.0 | provisional — you go down in long fights, and boss fights are the long ones |

**Reach discounts apply to the single-target damage term only** — that is the damage a melee body
has to walk to. Control is overwhelmingly ranged and takes no reach discount. A further ×0.9 on
crowd when neither body is `ranged` or `hybrid`.

Crowd and boss terms blend by act, weighting crowd more early:

| act | crowd | boss |
|---|---|---|
| I | 0.70 | 0.30 |
| II | 0.60 | 0.40 |
| III | 0.50 | 0.50 |

## 6. Actions is a cap, not a peer

`deployable tempo = min(capability breadth, action points)`

Actions does not add to tempo — it **bounds how much of your tempo you can spend per round**.
Scoring it as a peer axis double-counts, because a capability you cannot afford to deploy delivers
nothing.

**The cap mostly punishes, rarely rewards, and that is correct.** Lone Wolf gives each body 2
Actions, 2 Bonus Actions and 2 Reactions, so the duo already has a four-body party's economy —
which is what Listo is tuned against. With four Actions a round against four tempo cells, the cap
seldom binds from above. Its real work is clipping a pair whose action economy is *below* that
baseline. This is the same "surplus, not sufficiency" reading §5a now carries.

> **Provisional.** The shape is settled — clipping below baseline, saturating above — but the exact
> functional form and the definition of "capability breadth" need calibration against a re-authored
> roster. Do not tune this against the current chassis values; they were authored under the old
> model and against a curated shortlist.

## 7. Only Control splits

Checked per axis rather than assumed:

- **Rescue** — in a *duo* there is no area-versus-single distinction; Twilight Sanctuary and
  Healing Word both reach the same one other body. The fight-type dependence is about *need*, which
  the §5 coefficient handles.
- **Saves** — the threat profile differs by fight type but your proficiency set does not.
- **Actions, Endurance, Skills** — not fight-type shaped.
- **Durability** — *is* quietly fight-type shaped: Heavy Armour Master's flat −5 per hit is enormous
  against eight small attacks and nearly irrelevant against one 60-damage hit, while Lone Wolf's
  halving is scale-invariant. **Handled in the rubric, not the schema** — rungs distinguish flat
  from proportional mitigation. Splitting it starts the slide toward splitting everything, and
  unlike control it is not a capability you choose between on a given turn.

## 8. Weights

Applied after each axis is normalised to its own maximum (`personal` → 5, `complementary` → 7), so
that caps no longer double as weights.

| axis | w | status |
|---|---|---|
| **Saves** | 3.0 | a failed save removes 2 Actions, 2 Bonus and 2 Reactions — half the party — in encounters tuned for a 25% loss, and half DR does nothing against it |
| **Skills** | 2.5 | two characters carry every proficiency and Expertise the run will have, and primary-stat coverage is halved on top |
| **Endurance** | 2.0 | the one axis Lone Wolf makes *worse* — four bodies' actions burning two bodies' slots |
| **Durability** | 2.0 | at parity once `enableHpMax` is off, with no taunt and doubled loss-cost |
| **Rescue** | 1.5 | nice-to-have rather than required, but half DR doubles every point healed |

All **provisional**. Tempo axes are not weighted here — they are aggregated through §5 and §6.

## 9. Score

```
normalise    each combined axis value ÷ its kind's maximum        → 0–1
tempo        crowd/boss terms, MIX-blended, capped by Actions     → 0–1 against an observed ceiling
resilience   weighted mean of durability, saves, rescue           → 0–1
duration     endurance                                            → 0–1
utility      skills                                               → 0–1
```

Tempo and the non-tempo blocks weigh **evenly, 50/50** — *provisional, and deliberately neutral*.
The earlier attempt to move it rested on a correlation computed across the curated 26-chassis
roster, which is a shortlist rather than a sample of build space, so it could not show whether
coverage and damage genuinely trade off. **Recompute it once the roster is re-authored from
scratch**, which is the first point the data will not be selected on the outcome.

Two things to carry into that decision. At +126% regular and +170% boss HP, kills are slow enough
that enemy turns happen regardless, which pushes work onto resilience rather than tempo. And
tempo's *defensive* value lives in the crowd term, not the boss term — a boss acts whether you took
40% or 60% off it — so if crowd clear deserves a premium, the act blend in §5 is the honest place
for it, not the global split.

## 10. Display collapses; source data does not

Source keeps the full granularity. Presentation collapses it so a radar stays readable.

| surface | shape |
|---|---|
| **Source** | ten values per act |
| **Radar** | nine spokes — control-single and control-area blend by the act's crowd/boss weighting, exactly as the damage pair already does |
| **Tables** | may expose all ten |
| **Idle-body flag** | computed on the uncollapsed values, so it now catches "no answer to crowds" on the **control** side as well as the damage side |

Every spoke plots **percent of that axis's achievable maximum**, so all nine are visually
commensurable despite personal capping at 5 and complementary at 7.

## 11. What is derived and what is not

**Derived** — traceable to a game mechanic or an installed config, safe to rely on:
no cap on complementary; personal for durability/saves/endurance; complementary for control
(two concentration slots); Actions as a cap (Lone Wolf's 2/2/2 meets four-body parity); Rescue in
Resilience (action cost already in the rungs); the AoE and single-target coefficients.

**Provisional** — reasoned but uncalibrated, and every one of them should be revisited against a
re-authored roster: all four weights, the control and rescue coefficients, the tempo cap's
functional form, and the 50/50 split.
