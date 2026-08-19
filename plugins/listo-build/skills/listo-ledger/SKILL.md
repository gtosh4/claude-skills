---
name: listo-ledger
description: Build or update the Listonomicon pairing ledger — score every candidate chassis on the nine-axis radar, rank every carry × support pairing on coverage plus delivered damage, and render the ledger artifact. Use when comparing many possible duos rather than building one.
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

Each chassis gets **nine axes × three acts**, on `listo-build`'s §5a anchors —
read that section, it is the rubric. Acts map to character levels I 1–10,
II 11–15, III 16–20. Scores are relative to *that act's* encounters, so a
feature that does not scale must fall.

Then the renderer does the rest. Your job is three things and nothing else:

1. **The chassis scores** — nine ints per act, honestly, with the low ones low.
2. **`reach`** — `ranged`, `hybrid` (melee with a real ranged option), `mobile`
   (melee with repeatable mobility), `static` (melee, none).
3. **The prose** — what each chassis is, and why each entry reads the way it does.

## The two numbers, and why not one

**Coverage** is the seven non-damage axes. **Damage coverage** is what the pair
actually delivers, reach-discounted. Score weights them evenly.

Do not be tempted back to a nine-axis total. Across a full field its correlation
with delivered damage is **0.00** — the completeness axes correlate *negatively*
with damage (−0.46) and cancel the damage block's +0.81 exactly. Two pairings
with an identical ST+AoE block can differ by seven points of delivered damage,
and a total cannot see it.

**5 + 0 is worse than 3 + 3.** A pair that wins one fight type and is a passenger
in the other has a dead body in every encounter of the wrong kind. Split
single-target against area only when *neither* half has a dead fight.

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
