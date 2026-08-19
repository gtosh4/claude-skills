---
name: listo-finalists
description: Compare a shortlist of fully-built Listonomicon pair sheets side by side — one card per pairing, each carrying its own sheet's numbers and linking out to it. Use after the sheets exist, to decide which duo to actually play.
---

# Listo finalists comparison

**Three skills, one pipeline.** `listo-ledger` narrows a roster of chassis to a
shortlist. `listo-build` turns each shortlisted pairing into a real pair sheet.
This skill compares the finished sheets and hands back a decision.

The distinction that matters: the ledger scores **chassis**, this page scores
**builds**. By the time a sheet exists the pairing has a ladder, a stat spread,
a race, a background, gear and a gate audit — and those choices move the numbers.
A sheet's scores are the authority; the ledger's were the estimate.

The shortlist is however many pairings the user asked to compare — two, three,
eleven. Nothing here assumes a count; title the page after the field it holds.

**Author JSON. Never write comparison HTML.**

```sh
scripts/render_finalists.py finalists.json --scrape sheets/ -o out.html
```

`assets/finalists-schema.md` is the shape. `assets/finalists-example.json` is a
working comparison of eleven pairings.

## Method

1. **Publish the sheets first.** Each card links to one, and a card without a
   live URL is worse than no card.
2. **Import the scores with `--scrape`**, pointing at the directory of rendered
   sheets. It reads the `data-a1…b3` attributes the sheets already carry and
   writes them into the JSON. Do not re-type them.
3. **Lift the prose from each sheet** — its tagline and its two headline `<h2>`s.
   Rewriting them lets the card drift from the page it links to.
4. **Render, then read the reorder.** The interesting output is not the ranking;
   it is which pairings moved against the ledger's estimate, and why.

## Read the disagreements, they are the product

When a sheet disagrees with the ledger, the sheet is usually right and the
*reason* is usually general. Two that have already come out of this:

- **Five independent builds of the same carry all cut its AoE**, for the same
  reason — a six-level caster dip freezes at 3rd-level slots for fourteen levels
  while enemy HP roughly doubles. Flat payload AoE must fall; the ledger had it
  rising.
- **A level budget that does not exist.** Two features needing class levels 11
  and 5 cannot both be online in Act II, because that is sixteen levels. The
  ledger scored the pair as though both were.

Both are cases where building the thing exposed an arithmetic error that
estimating it could not. Feed them back into the ledger's chassis scores.

## Keep the spread

The same carry will appear on several cards with different numbers. **That is
correct.** Do not average them into one canonical chassis to make the page
tidier — the variation records how much the partner changes the build, which is
the one thing a per-chassis ledger cannot show. If a single number per chassis
is wanted, re-score the ledger.

## When the field is one-sided

If one support partners most of the field, say so plainly rather than drafting a
weaker one for variety. In the run this format was built for, four supports owned
the entire top twenty of a 135-pairing field, and twelve consecutive ranks passed
without a new one. That concentration is a finding about the modlist, and hiding
it behind an artificially diverse shortlist would have misrepresented the ledger.
