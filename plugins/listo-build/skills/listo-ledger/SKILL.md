---
name: listo-ledger
description: Build or update the Listonomicon pairing ledger — score every candidate chassis on the ten-axis radar, rank every carry × support pairing on tempo, resilience, duration and utility, and render the ledger artifact. Use when comparing many possible duos rather than building one.
---

# Listo pairing ledger

**The ledger answers "which pairings are worth building?"** It is upstream of
`listo-build`: the ledger narrows a roster of chassis to a shortlist, and each
shortlisted pairing then gets a real pair sheet.

**Author JSON. Never write ledger HTML.** `scripts/render_ledger.py` holds the
CSS, the scoring, the field table and every derived number:

```sh
scripts/render_ledger.py ledger.json -o ledger.html
```

`assets/ledger-schema.md` is the shape. `assets/ledger-example.json` is a
working ledger to copy.

## What you are scoring

Each chassis gets **ten axes × three acts** — Control is split crowd-versus-boss
exactly as damage already is. Three files own the rules and they do not overlap:
**`listo-build/references/axis-rubrics.md`** gives the content anchors — what a 5
actually *is* in named manifest features, per act; **`listo-build` §5a** gives the
functional ladder (5 Surplus → 0 Absent) and what each axis measures; and
**`listo-build/references/scoring-model.md`** owns how two bodies combine, the
fight-type coefficients, the weights and the score. Read all three before scoring.

Acts map to character levels **I 3–8, II 9–15, III 16–20**. Scores are relative to
*that act's* encounters, so a feature that does not scale must fall — and **Act II
is the richest band**, holding six feats, 8th-level slots and nearly every
run-defining class breakpoint.

**Score illithid at the even share, and only where the chassis converts it unusually well.**
IPO2 is live, tadpoles are open to every chassis, and how much a body gets is a *pairing* decision
— so the ledger needs one allocation every row is scored against, or the numbers stop being
comparable. Use the **even share**: half the party pool per body, which is the only allocation
consistent across every pairing in the ledger, and lands at roughly **IMR 1 in Act I, 2 in Act II,
4 in Act III**.

**Then move a row only for differential fit.** The rubric ceilings in
`listo-build/references/axis-rubrics.md` are authored illithid-free, so a chassis that converts
powers averagely gains nothing — folding a flat uplift into every row would just inflate the whole
ledger. What earns a rung is a chassis that converts *better than its neighbours* do, and what
costs one is a chassis that converts worse:

| Converts well | Converts badly |
|---|---|
| A **cheap Action** — a body whose turn is often a cantrip loses nothing casting a power; the passive powers (Psionic Overload, Cull the Weak, Luck of the Far Realms) cost no Action at all and **scale with attack count** | An **expensive Action** — Fighter 11 gives up six attacks per cast, a Paladin gives up smites |
| A **real casting stat on the last class added** — that is where power DCs come from — and doubly so with Arcane Acuity | **No casting stat**: every save power in the tree is dead, leaving only the no-save half |
| **Spare reactions**: Eldritch Ward and Psionic Backlash are interrupts, and Lone Wolf's second reaction is often idle | Bonus action and both reactions already committed — Force Tunnel and the wards have nowhere to go |
| **At-will damage** chassis: charges are a long-rest pool bolted onto a body with no long-rest clock, so the Endurance cost is small | **Full casters**: charges compete for the rest that slots already force |
| **Armour and AC to spare** — the `+IMR` tax and Psionic Overload's self-damage are cheap here, and the Cerebral Citadel set's +1 AC per 5 powers wants medium-armour proficiency | **Soft bodies** — the tax lands on the half enemy AI already prefers |
| A body **short on damage types** — Psychic and Force answer Absolute Wrath's layered resistances | A body that already carries two damage types |

Record the even-share baseline as a `caveats.assumptions` item, so a reader knows which allocation
the column assumes. A pair sheet may then deviate from it — concentrating the pool lifts one body
and lowers the other — and that is `listo-build` §5a's business, not the ledger's.

Then the renderer does the rest. Your job is three things and nothing else:

1. **The chassis scores** — ten ints per act, honestly, with the low ones low.
   Index 8 (saves) is `null`: author the `saves` set instead and let the renderer derive it.
2. **`reach`** — `ranged`, `hybrid` (melee with a real ranged option), `mobile`
   (melee with repeatable mobility), `static` (melee, none).
3. **The prose** — what each chassis is, and why each entry reads the way it does.

## Four blocks, and why not one total

The unifying currency is the **action point**: one buys one of damage, control or
rescue. The pair's job is to remove enemy action points faster than they remove
yours. `scoring-model.md` has the full argument; the shape is:

| block | axes | answers |
|---|---|---|
| **Tempo** | single-target, aoe, control-single, control-area | how fast you remove enemy APs |
| **Resilience** | durability, saves, rescue | how hard yours are to remove |
| **Duration** | endurance | how many fights your supply covers |
| **Utility** | skills | out-of-combat coverage |

**Actions is none of these — it caps Tempo** rather than adding to it. A capability
you cannot afford to deploy delivers nothing.

Do not collapse these to one total. Two pairings with an identical damage block can
differ by seven points of delivered damage, and a total cannot see it.

> **The old −0.46 / +0.81 / 0.00 correlation figures have been retired.** They were
> computed across the curated 26-chassis roster, which is a shortlist selected for
> being good at *something*, not a sample of build space — so they cannot show
> whether the blocks genuinely trade off. Recompute them once the roster is
> re-authored, which is the first point the data is not selected on the outcome.

**5 + 0 is worse than 3 + 3.** A pair that wins one fight type and is a passenger
in the other has a dead body in every encounter of the wrong kind — and the control
split now catches that on the control side too, not just the damage side.

## Method notes that keep the ledger honest

- **Entries are derived, not chosen.** One per carry, headlined by its best
  partner. Hand-picking entries is how the entry list and the field table drift
  apart — the renderer refuses to build if a carry in the cut has no prose.
- **Roster order is derived too.** A hardcoded list silently drops every chassis
  added after it was written; this has already happened once.
- **Variation figures do not exist until render time.** Write the clause, not
  the number.
- **Re-scoring is cheap and should be frequent.** Change the ints, re-render.
  Nothing downstream needs hand-patching.

## Confirm special handling before you author it

Some fields are not plain data — `boosters`, `reach`, `prof` abilities, axis kinds — and the
renderer applies each one through a registry. **Before authoring such a value, confirm the
renderer implements it.** If you cannot point at the line that applies the effect, it is not
implemented.

**The renderer fails on an unrecognised value rather than skipping it, and that is deliberate.**
A dropped booster contributes nothing, so the score lands **too low** — and a score that is too
low is indistinguishable from an honest one. The field table still ranks, the entries still
render, and the chassis just sits a rung below where it belongs, permanently and invisibly. Every
other bug in this format announces itself; this one would not.

Failing closed makes the check reactive instead of a standing tax. You do not audit boosters
before each render. You fix one crash the first time you author something new. Never add a
permissive branch, a default, or a warn-and-continue to any of these — see
`assets/ledger-schema.md`, "Anything with special handling fails closed".

## Verify before you score

Score against the compiled data in `listo-build/data/`, and when a claim is
load-bearing read the pak itself with `listo-build/scripts/lspk.py` — mod pages
and changelogs go stale, installed archives do not. The traps that have actually
cost points here:

- **`StackId` is a cap.** A summon or brand carrying one *replaces* rather than
  accumulates — the difference between Actions 5 and Actions 3.
- **A flat feature must fall.** Anything with fixed dice and no upcast path
  decays against Combat Extender's +126% regular and +170% boss HP. An at-will
  cone that is 3d10 at character 10 is still 3d10 at 20.
- **Conditional `Boosts` scale.** Charges gated behind `Wisdom >= 14/16/18/…`
  mean a Wis 22 build has six and a Wis 14 build has two.
- **Check the level arithmetic.** A split that does not sum to 20 has been
  shipped here before.

## Updating a published ledger

Re-render the same JSON and republish to the same artifact URL. When the roster
changes, add the chassis and its prose in one edit — the renderer will tell you
if an entry is now missing, which is the only bookkeeping the format needs.
