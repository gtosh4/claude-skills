---
name: listo-build
description: Plan a Baldur's Gate 3 character build for the Listonomicon modlist, for a two-player Lone Wolf run, and publish it as a character-sheet artifact. Use whenever the user asks about Listo/Listonomicon builds, classes, subclasses, races, feats, stat spreads, gear, or quest rewards. Assumes two players and Lone Wolf but makes no assumption about the other character. Verifies every option against the installed 10.2 manifest rather than the published docs, which are stale.
---

# Listonomicon build planning

Listo changes enough of BG3 that vanilla build knowledge is actively misleading. The job is
to plan against **what actually ships**, not what the documentation or the wider BG3 community
says.

## The one rule that matters most

**The published changelog lags the shipped list.** The docs site stops at v10.0; the Wabbajack
gallery ships **10.2**. Several things the docs still describe have been removed — the Arcanist
Feat is the canonical example. Anything load-bearing gets checked against the manifest.

`references/research-recipes.md` has the commands to pull and search the manifest.
`references/listo-rules.md` has the verified ruleset facts — read it before doing any math.

## Fixed premises

Every build planned with this skill is for the **same run**: two players, Lone Wolf active, level
cap 20. Treat these as given rather than questions.

What follows from two characters, regardless of what either of them is:

- **Action economy is the structural problem.** Two bodies against encounters tuned for five.
  Anything that adds a third body — summons, familiars, Skeleton Crew — is worth more here than
  its raw numbers suggest.
- **Rest economy is worse than it looks.** Long rest cost keys off *camp population*, not active
  party, so recruiting companions means paying a full party's 120+ supplies to refuel two
  characters. Short-rest resources are correspondingly more valuable.
- **Losing either character usually ends the fight.** There is no third body to pick anyone up.
  Weight survivability and hard-CC resistance above what a normal party would.
- **Two characters cover every skill check in the campaign.** Expertise and skill proficiencies
  are worth more than usual.
- **Lone Wolf gives an extra Action, Bonus Action and Reaction.** Design turns around having two
  of each, and look for effects that scale with reaction count.
- **Lone Wolf's +4 to two abilities also grants save proficiency in both**, and the level 1 class
  grants two more plus armour, shields, skills and features. **Solve those together, by
  enumerating combinations** — not by fixing the +4 first and fitting a class around it. Hold the
  primary to **20 by level 6 and 22 by level 18**; the +4 is the cheapest way there but not the
  only one, and any alternative costs roughly two feats. See the joint-optimisation section in
  `references/listo-rules.md`.
- Companion quests are solved by **Sit This One Out 2** — see `references/listo-rules.md`.

**Do not assume anything about the other character.** Ask what roles it already covers — damage
type, healing, control, face, skills — and design into the gaps. The same premises support a
build alongside a martial, a second caster, or anything else.

## Process

### 1. Establish the remaining constraints

Ask:

- **What the other character covers.** Roles and gaps only, not a build critique.
- **Stat lock.** Gear is expensive (4× merchant prices), so most players commit to one primary
  stat. Establish it early; it eliminates most of the option space.
- **Damage expectation.** A pure controller in a two-person party gets overrun. Ask directly
  whether they need to be a damage threat, or whether the other character carries that.
- **Lone Wolf MCM config.** Is the feat requirement disabled? Does the ability bonus still apply?
  This decides whether +4 and save proficiencies exist at all, and it is visible on the sheet at
  character creation.
- **Optional mods.** Absolute Wrath, Random Equipment Loot, extra encounters. Random Equipment
  Loot in particular voids all gear planning.

### 2. Verify the option space

**Grep the compiled data files first** — they already did this work and they carry the
mechanics, not just the names:

| Looking for | Grep this |
|---|---|
| Classes, subclasses, progression | `data/listo-10.2-classes.md`, then `data/classes/<class>.md` |
| Races and subraces | `data/listo-10.2-races.md` |
| Feats and fighting styles | `data/listo-10.2-feats.md` |
| Items, slots, attunement, economy | `data/listo-10.2-equipment.md` |

Each has a "not present" section listing what the docs still advertise but the list no longer
ships — check it before recommending anything, because that is where the expensive mistakes
are. Fall back to `data/listo-10.2-mods.tsv` and the manifest for anything the compiled files
don't cover. Do not recommend a class, subclass, race or feat without confirming it's in the
list — v9.0.3 purged a large batch of subclasses and nearly all race mods.

### 3. Work the decisions in this order

Chassis (class + subclass + **dip**) → race → ability spread → feats → equipment. Each constrains
the next. Doing stats before feats produces wasted points, because half-feats complete odd scores.

### 3a. Assume multiclassing by default

**The default shape in Listo is a primary class plus a 3-level dip, not a single class.** Feats
key off class level, so a 3-level dip is feat-neutral — you get the dip class's own level 3 feat.
Single-class is a legitimate answer, but it is a *conclusion*, never the starting assumption.

Generate candidates as **(primary subclass × dip)** pairs where the dip fills a gap the primary
cannot. A dip is worth proposing when it buys one of:

- **A saving throw proficiency** — only the level 1 class grants these, so the dip may need to go
  *first*. This often decides build order on its own.
- **An armour or shield proficiency** the primary lacks.
- **A resource on a different clock** — short-rest slots against a long-rest primary.
- **A scaling effect that keys off character level**, which a tiny dip buys in full. Eldritch
  Blast beams are the standard example: two Warlock levels give a fully-scaling damage engine.
- **A whole role** the primary has no access to — healing, summons, Counterspell.

`references/listo-rules.md` has the dip-size math and the cheap breakpoints table.

### 3b. Present options, not a recommendation

When exploring classes or subclasses, **enumerate before narrowing**. Grep the mods index for
every candidate in scope first — the option space is larger than memory suggests, and v9.0.3
purged enough that intuition is unreliable in both directions.

Then present **at least six candidates**, each with:

- **What it is** — the concrete mechanics, with levels attached. Not vibes.
- **Strengths** — what it does that the alternatives don't.
- **Weaknesses** — stated plainly, including the ones that are disqualifying.
- **Evaluation** — a verdict sentence saying when this is the right pick.

Follow with a **side-by-side table** across the axes that matter for a duo: damage, control,
healing, durability, resource cadence, skill coverage, and whether a mid-run mistake is
recoverable.

Then list what was **dismissed and why**, one line each, so the user can see the space was
actually covered rather than silently truncated.

Close by naming **the decisive trade-off** — the single axis the choice turns on — and give a
recommendation with the condition that would flip it.

### 4. Do the math properly

The arithmetic in `references/listo-rules.md` is where most build advice goes wrong. In
particular: modifier thresholds, the feat-count ceiling, and dip placement.

### 5. Deliver as a character sheet

Publish an artifact using `assets/sheet-template.html`. Keep it to **picks and when** — what to
select at each level, the stat spread, the gear targets. Reasoning belongs in conversation, not
on the sheet. State unverified assumptions explicitly rather than smoothing over them.

**Set `data-class` on the `.sheet` element to the build's primary class** — the one with the
highest class level. A 9/3 Sorcerer/Warlock is `data-class="sorcerer"`. This themes the sheet
for that class. One of:

```
barbarian bard cleric druid fighter monk paladin ranger rogue sorcerer
warlock wizard artificer mesmerist paragon inquisitor bloodhunter
```

Omit the attribute for the neutral default. Do not hand-edit the palette — the themes vary by
hue alone over a shared chassis so that two sheets from the same run look like a matched pair,
and picking colours by hand breaks that.

> Both characters in a run get their own sheet. If the two builds share a primary class, they
> will theme identically — that is correct, not a bug. Distinguish them by name in the wordmark.

### 5a. Score the profile radar

The sheet opens with a nine-axis radar, tabbed by act. On `<figure class="profile">` fill
`data-act1`, `data-act2` and `data-act3` — one score set per act — plus `data-bands` for the
character-level range each act covers. **Keep the table rows in sync with the numbers**; the
table is the accessible view and the only thing that survives if the script doesn't run.

Axis order is fixed: **single-target, aoe, durability, economy, control, sustain, skills,
saves, cadence.**

**Score 0–4 against what a party needs — a general sense, not a named partner's sheet.** Two-player
Lone Wolf is the *environment* (halved damage, +30% HP, few bodies), so a four-person party's
expectations are the wrong yardstick. But the score must not depend on who the other character
turns out to be, or two sheets from one run can't be read against each other.

| | Anchor |
|---|---|
| **4** | Covers this axis alone. Nobody else has to think about it. |
| **3** | Strong. Needs no help in normal fights. |
| **2** | Adequate, but leans on a partner or on consumables. |
| **1** | Thin. A real liability if nobody else covers it. |
| **0** | Absent. |

**Score each act separately.** A build that peaks at 20 and a build that peaks at 8 are different
builds, and one polygon cannot say so. Acts map to character levels roughly:

| Act | Char levels |
|---|---|
| I | 1–10 |
| II | 11–15 |
| III | 16–20 |

> These bands are an **estimate**, not a verified figure. The only per-act level numbers in the
> docs are boss-scaling caps from the v3.0/v3.2.1 changelog, long superseded, and the XP curve now
> comes from Expansion 13-20 and is MCM-editable. Level cap is 20; most players reach 15+ and 20
> needs the optional encounter content. Label the bands as approximate on the sheet.

What each axis measures, and its **kind** — which decides whether a second source of it is worth
anything to the party:

| Axis | Kind | Scores high when… |
|---|---|---|
| **Single-target** | additive | it kills one priority enemy fast enough that the fight ends before resources do |
| **AoE** | additive | it clears groups. Split from single-target because Listo's encounters lean on numbers, and a build can be excellent at one and absent at the other |
| **Durability** | additive | it survives incoming HP damage: AC, HP, resistances, damage reduction |
| **Economy** | additive | it adds bodies, actions or reactions — summons, familiars, Skeleton Crew, Action Surge, extra reactions. **The duo's structural problem, so weight it heavily** |
| **Control** | threshold | it reliably removes an enemy's turn — and the CC lands against Listo's inflated saves |
| **Sustain** | threshold | it recovers between and during fights: heals, self-healing, Durable's full-HP short rests, temp HP. Not just heal *spells* |
| **Skills** | threshold | it covers out-of-combat checks: expertise, proficiencies, face skills |
| **Saves** | personal | it resists *hard CC*. Distinct from Durability — being Held is a different death than being burst down. Weight Wisdom highest, then Con, then Dex |
| **Cadence** | personal | its resources refresh on **short** rests. Long-rest-only classes score low, because long rests cost 120+ supplies scaling with camp population |

- **Additive** stacks across the party — more is always more.
- **Threshold** saturates at the party's first source. The campaign needs one face and one
  lockdown; a second is worth far less than the number suggests.
- **Personal** cannot be delegated at all. A partner's Wisdom save does not stop *you* being Held,
  and their short-rest engine does not refill *your* slots.

**So the column never totals, and two sheets are never compared by summed score.** Read the shape
and read the low axes; that is what the chart is for.

**A 4 across the board is a failed evaluation, not a great build.** If nothing scores 1 or 0, look
harder. Then say in one sentence, under the table, what the lowest axis that matters is and what
covers it.

**Beware the ceiling.** 4 means "as much as a party needs", so everything above it is clipped —
two builds both scoring Control 4 can differ by Hold Monster versus Hold Monster plus Wall of
Force plus Dominate Monster. When a build's real advantage is headroom past 4, the chart cannot
show it; say so in prose instead of inflating a number.

## Pitfalls that have bitten before

- **Proposing single-class builds by default.** A 3-level dip is free in feat terms. If the answer
  is single-class, say *why* the dips were rejected.
- **Offering two or three options.** Enumerate from the mods index and present at least six with
  real strengths and weaknesses. Narrowing early hides the good answers.
- **Recommending from vanilla knowledge.** Tavern Brawler, Great Weapon Master, Sharpshooter,
  Alert, Tough, Durable and Arcane Acuity all work differently here. Arcane Acuity in particular
  invalidates most published Bard guides.
- **Assuming a single +1 helps.** Odd ability scores give nothing. It's two points or none.
- **Forgetting the first class is re-picked on respec.** Saving throw proficiencies come from
  the level 1 class only, and a rebuild silently loses them.
- **Treating the docs as current.** See above.
- **Ignoring where a proficiency comes from.** Shields, in particular, are often unobtainable
  without a specific feat or dip — check before assuming an AC number.
- **Planning gear without checking attunement.** Listo caps how much you can wear at once.

## Reference files

| Path | Contents |
|---|---|
| `references/listo-rules.md` | Verified ruleset facts and all build math |
| `references/research-recipes.md` | How to search the bundled snapshot; how to refresh it |
| `data/listo-10.2-classes.md` | Index of all 17 classes and 156 subclasses; saves, caster tier, cadence |
| `data/classes/<class>.md` | One file per class — every subclass's mechanics, dip value, gaps |
| `data/listo-10.2-races.md` | Every race and subrace, with the traits each grants |
| `data/listo-10.2-feats.md` | Every feat and fighting style, with Listo's rebalances |
| `data/listo-10.2-equipment.md` | Items, slots, attunement, upgrade paths, drop locations |
| `data/listo-10.2-mods.tsv` | 706 mods as `ModID<TAB>Name` — grep this to confirm anything exists |
| `data/listo-10.2-manifest.json` | Raw manifest; holds which *file variant* was pulled per mod |
| `data/docs/*.md` | The four Listo doc pages as raw markdown |
| `scripts/strip.sh` | HTML-to-text helper for Nexus and bg3.wiki pages |
| `assets/sheet-template.html` | Character-sheet artifact template, themed |

The compiled `.md` data files are the **first stop** for "does X exist and what does it do".
They were built from the mods index, the manifest's file variants, and the mod pages themselves,
and they record provenance — anything they mark `(unverified)` needs checking before a build
leans on it. `references/listo-rules.md` owns the **arithmetic and doctrine** only; it
deliberately does not enumerate options.

**Read the warnings at the top of `data/listo-10.2-classes.md` before recommending a class.**
One class ships a version with a known level-up-breaking bug, several mods are pinned behind
their own documentation, and every class mod page's feat table is wrong for Listo.

**Grep the data files, never read them whole** — the manifest is 1.2 MB and the changelog 293 KB.

Everything here is a snapshot of Listonomicon **10.2**, built 8 July 2026. If the installed list
has moved, refresh the snapshot before trusting any of it — `references/research-recipes.md` has
the commands.
