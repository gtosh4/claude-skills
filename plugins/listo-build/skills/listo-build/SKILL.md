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

**Lone Wolf runs in non-feat mode** — the MCM feat requirement is off, so all its buffs apply
from level 1 and **it costs no feat**. All seven feats (3/6/9/12/13/15/18) go to the build.
Lone Wolf Feat and Sit This One Out 2 both ship `-` disabled in the MO2 profile and are enabled
by hand for this run; see `data/listo-10.2-mcm.md` for the rest of the shipped on/off state.

**Absolute Wrath is enabled for this run.** Listo's own docs warn that it double-dips with
Combat Extender's curated affixes; it is on regardless, so **plan against enemies carrying
random affixes on top of the CX ones** — stacked resistances and damage reduction, and death
explosions that disarm. Two consequences for every build: **damage types that are rarely
resisted (Force, and Radiant in Act 2) are worth more than their raw numbers**, and a weapon
that cannot be disarmed, or a character who does not depend on one, is worth more than usual.
Carry resistance-stripping or elixirs for the rest.

What follows from two characters, regardless of what either of them is:

- **Action economy is the structural problem.** Two bodies against encounters tuned for five.
  Anything that adds a third body — summons, familiars, Skeleton Crew — is worth more here than
  its raw numbers suggest.
- **Rest economy is worse than it looks.** Long rest cost keys off *camp population*, not active
  party — but an idle companion costs **0.3×** an active member and a hireling 0.25×, so
  recruiting is a third as expensive as the older note claimed. Short-rest resources are still
  worth more. Resolved multipliers in `data/listo-10.2-mcm.md`.
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

**Do not assume anything about the other character.** Establish what roles it already covers —
damage type, healing, control, face, skills — and design into the gaps. That opens the interview
in §1b: **read it off the partner's sheet if one exists**, ask if it doesn't. The same premises
support a build alongside a martial, a second caster, or anything else.

## Process

### 1. Orient, then interview

**This is a conversation, not a form.** The niche decision eliminates more of the option space
than everything else combined, and it is the one decision the player — not the skill — owns.
Get it right by *showing them the landscape first*, then asking.

#### 1a. Open with a short orientation

Before the first question, spend **one short paragraph** on what this run actually rewards. Not a
lecture — the player should be answering within about 150 words. Cover only:

- The duo's structural problem is **action economy**, so anything adding a body is worth more
  than its numbers.
- Enemy HP is **+126% / +170% by 20** and scales off *player* level, so fights are long and
  there is no out-levelling. Damage that ends fights early is worth more than it looks.
- **Long rests cost 120+ supplies**; short-rest engines refuel for free.
- Vanilla build knowledge is actively wrong here — name the one or two rebalances that bear on
  what they seem to want (Arcane Acuity, Eldritch Blast at 1d8, Alert, Tavern Brawler).

The niche table below is **working material, not output**. Mine it for the option descriptions in
§1b; paste it at the player only if they ask to see the whole landscape at once.

| Niche | What carries it here | The catch |
|---|---|---|
| **Action-economy engine** | **Not only summons.** Bodies: Warlock 3 Chain familiar (Help, Magic Resistance, doubled HP from `18881`), Ranger 3 Beast Master (Expansion moves Companion's Bond to **3**), Summon Beast 5 / Conjure Animals 9 (`13458`), the **Skeleton Crew feat**. Extra actions: **Haste** — the strongest action-economy spell in the list for a duo — **Action Surge** (2 charges from 17), and **Quickened**, the only general exemption from Listo's rule that a bonus-action spell blocks a levelled cast. **Twinned Haste covers 100% of a two-person party for one Metamagic pick** | Summons cost a turn to set up. Haste is **concentration** — it competes with your control spell — and Lethargy costs the target a turn if it drops |
| **Lockdown controller** | Save-or-lose against crowds; area control composes rather than duplicating | Enemy saves climb with **+1 ability point per 6 levels** (bosses and enemies alike), so a static DC decays. Single-target-only CC *falls* further as encounters crowd |
| **Front-line damage** | Smites, Extra Attack, **Fighter 11** (3 attacks *and* an off-cadence feat) | Long fights mean resource-limited burst runs dry; needs a sustain answer |
| **Reaction economy** | Lone Wolf's **second reaction**: Rogue's off-turn Sneak Attack, Uncanny Dodge as an interrupt, Riposte, Opportunity Attacks | Reaction effects are worthless if nothing triggers them — it needs a build shaped around being attacked |
| **Short-rest engine** | Warlock pact slots, Battle Master dice, Monk ki, Second Wind / Action Surge | Usually caps spell tier or damage ceiling relative to a long-rest caster |
| **Durability anchor** | Lone Wolf already gives **halved damage and +30% HP**; heavy armour + shields stack on top. **Self-healing counts here too** — `Durable` refunds full HP on *every* short rest plus in-combat regen below 60%, which is effective HP on the cheap clock | Being un-killable does not end fights, and the duo cannot afford a passenger |
| **Skills and face** | Two characters cover **every** check in the campaign; Expertise is worth double | A **complementary** role — depth saturates at one source, but breadth does not: two characters with different proficiencies cover more gates than one. Rarely worth building *around*, always worth dividing |

#### 1b. Ask in batches, with `AskUserQuestion`

Use the **`AskUserQuestion` tool**, not prose, for anything with a bounded answer. Batch related
questions into one call — up to four questions, each with up to four options.

**Batch one — the two questions that eliminate the most space.** Ask these together, before any
chassis thinking:

1. **What the other character already covers** — `multiSelect: true`, drawn from the niche table.
   Roles and gaps only, never a critique of their build.
2. **What this character should own** — the niche, again from the table, narrowed to the four
   that fit whatever they said about the partner.

> **If the partner already has a sheet, don't ask them to describe it — read it.** Given an
> artifact URL or a file, **fetch it first**, take the coverage straight off the profile radar
> (high scores are what's covered; the falling rows and the `gap`-flagged cells are the brief),
> and turn question 1 into *confirm or correct my read*. It is a faster question and a better
> one: the player is reacting to specifics rather than generating a summary from memory. State
> which rows you read as covered so a wrong read is easy to catch.

**Read the negative space.** In a `multiSelect`, what they *didn't* tick carries as much signal
as what they did — an unticked "healing" means this character has to carry some, whatever niche
they then pick. Say the derived brief back to them in one sentence before moving on, because it
is an inference and it may be wrong.

**On a partner's threshold and complementary axes, the score converts straight into a requirement.** Sustain and
Skills saturate at the party's first real source, so the partner's number tells you exactly how
much this build owes:

| Partner scores | What this build must do |
|---|---|
| **5** | **Solos it.** Build nothing here — every point spent is wasted. |
| **4** | **Optional.** A second source is a luxury. Take it only if it falls out of the chassis for free; never spend a feat or a level on it. |
| **≤ 3** | **Must be covered, non-trivially.** Real levels or a real feat, not a token gesture. A 3 is not "mostly fine" — on a threshold axis it means the party has no reliable answer. |

**Score it per act, not overall.** A partner at Sustain 3/4/4 needs genuine help in Act I and
almost none afterwards, which argues for an early dip rather than a late investment.

This mapping applies to **threshold and complementary** axes. Additive axes always want more regardless of the partner's
number, and personal axes cannot be delegated at all — a partner's Saves score does nothing for
you. The kind labels are in §5a.

**Batch two — the constraints that shape the chassis.** After the niche is fixed. This is a
**menu, not a checklist** — ask only what is still genuinely open, since a comparison or an
earlier answer often settles two of these implicitly. Re-asking a question the conversation has
already answered reads as not listening.

3. **Stat lock.** Gear is 4× merchant price, so most players commit to one primary stat. Frame
   the options as actual stat lines, not abstractions. **Check for a stat clash with the
   partner** — two Charisma builds compete for every Charisma item at 4× prices, which is a real
   cost and belongs in the option description.
4. **Damage expectation.** A pure controller in a two-person party gets overrun. Ask directly
   whether this character must be a damage threat or whether the partner carries it.
5. **Resource clock tolerance.** Short-rest engine, long-rest nova, or a mix — this decides
   half the chassis list on its own.
6. **Melee or ranged**, if the niche hasn't already settled it.

**Batch three — the decisive trade-off.** Once the shortlist exists, ask the *specific* question
the shortlist turns on, with the real candidates as options. That is where §3b's decisive
trade-off belongs, and it is far more useful as a question than as a paragraph.

**"I'd like to compare these options" is an answer, not a stall.** The niche question is exactly
where a player wants the comparison *before* committing, and it is the highest-stakes question
in the interview. When it comes back, go straight to **§3b** — enumerate the options they were
offered as real builds, with the act-by-act shape and the costs — then re-ask with the same
tool. Do not re-pose the original question with the same four options, and do not fall back to
picking for them.

**Writing good options.** This is where the "more detail" lives:

- **Every option description carries a concrete Listo mechanic**, with levels attached. "Summons
  as extra bodies" is a label; "Warlock 3 buys a Chain familiar with Help, Magic Resistance and
  doubled HP, on a short-rest clock" is an option.
- **State the downside in the description.** An option with no stated cost has not been thought
  about, and the player cannot choose against something invisible.
- **Never four flavours of the same answer.** If two options lead to the same chassis, cut one.
- **No "(Recommended)" on preference questions.** Niche, stat lock and playstyle are the
  player's call and have no correct answer. Reserve the recommendation for *build* decisions,
  where §3b's doctrine applies — enumerate, then recommend with the condition that flips it.
- Always leave room for the free-text answer; the option list is a prompt, not a menu.

#### 1c. Confirm the config only where it deviates

Do **not** interview the player about mod settings — `data/listo-10.2-mcm.md` already has them.
Absolute Wrath is **on**; Random Equipment Loot is **not installed**; Grit and Glory is **off**;
Lone Wolf and Sit This One Out 2 are enabled by hand for this run. Ask only whether they have
changed something away from that.

### 2. Verify the option space

**Grep the compiled data files first** — they already did this work and they carry the
mechanics, not just the names:

| Looking for | Grep this |
|---|---|
| Classes, subclasses, progression | `data/listo-10.2-classes.md`, then `data/classes/<class>.md` |
| Races and subraces | `data/listo-10.2-races.md` |
| Feats and fighting styles | `data/listo-10.2-feats.md` |
| Items, slots, attunement, economy | `data/listo-10.2-equipment.md` |
| Any "is this toggle on?" question | `data/listo-10.2-mcm.md` — resolved from the install |

Each has a "not present" section listing what the docs still advertise but the list no longer
ships — check it before recommending anything, because that is where the expensive mistakes
are. Fall back to `data/listo-10.2-mods.tsv` and the manifest for anything the compiled files
don't cover. Do not recommend a class, subclass, race or feat without confirming it's in the
list — v9.0.3 purged a large batch of subclasses and nearly all race mods.

### 3. Work the decisions in this order

Chassis (class + subclass + **dip**) → race → ability spread → feats → equipment. Each constrains
the next. Doing stats before feats produces wasted points, because half-feats complete odd scores.

### 3a. Assume multiclassing by default

**The default shape in Listo is a primary class plus a dip, not a single class.** Feats key off
class level, so a 3-level dip is feat-neutral — you get the dip class's own level 3 feat.
Single-class is a legitimate answer, but it is a *conclusion*, never the starting assumption.

**Do not stop at 17/3.** A 6-level dip is *also* feat-neutral (14/6 = 17/3 = 7 feats), a 2-level
dip is free next to clean blocks (18/2, 15/3/2), and three classes are fine as long as one still
reaches 13. What a bigger dip costs is **primary class levels, not feats** — price those against
what the levels buy. The split table, the exchange rate, and the list of levels that outbid a
feat are in `references/listo-rules.md` § "Splits" and § "What a class level has to beat".

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

### 3b. Enumerate, detail, then hand the choice back

When exploring classes or subclasses, **enumerate before narrowing**. Grep the mods index for
every candidate in scope first — the option space is larger than memory suggests, and v9.0.3
purged enough that intuition is unreliable in both directions.

> **This section is not pinned to step 3.** Pull it forward whenever the player asks to compare
> before choosing — most often at the niche question in §1b, where the options are niches rather
> than chassis. Same structure either way: enumerate, detail, table, dismissed list, decisive
> trade-off, hand back.

Then present **at least six candidates**, each with:

- **What it is** — the concrete mechanics, **with levels attached**. Name the feature, the level
  it lands, the resource it costs and the clock it refreshes on. "Good control" is not an entry;
  "Hypnotic Pattern at 5, one long-rest slot, Wis save against Listo's scaled saves" is.
- **What it looks like at each act** — the build at character 5, 12 and 18. Two candidates that
  read identically at level 5 often diverge completely by 12, and that is usually the real
  choice. Say which act it peaks in.
- **Strengths** — what it does that the alternatives don't.
- **Weaknesses** — stated plainly, including the ones that are disqualifying, and including
  **what it gives up** rather than only what it lacks.
- **What it needs from the partner** — every candidate has a hole; name it, since the duo has
  exactly one other body to fill it.
- **Evaluation** — a verdict sentence saying when this is the right pick.

Follow with a **side-by-side table** across the axes that matter for a duo: damage, control,
healing, durability, resource cadence, skill coverage, and whether a mid-run mistake is
recoverable.

Then list what was **dismissed and why**, one line each, so the user can see the space was
actually covered rather than silently truncated.

Close by naming **the decisive trade-off** — the single axis the choice turns on — and give a
recommendation with the condition that would flip it.

**Then hand the choice back with `AskUserQuestion`.** Do not narrow six candidates to one on the
player's behalf. Put the two or three that survive the trade-off in as options, each described
by the mechanic that distinguishes it, and let them pick. Batch it with whatever secondary
question the answer will raise anyway — race, dip order, or the stat line — so one call
advances the whole design.

**Expand on demand, at any depth.** If they ask about one candidate, go deeper on that one
rather than re-summarising all six: the full progression table, the exact gear that keys off it,
what the level 1 class costs them, what a respec at 12 could still recover. The compiled data
files carry that detail — `data/classes/<class>.md` has per-subclass mechanics, dip value and
gaps for every one of the 156 subclasses.

### 4. Do the math properly

The arithmetic in `references/listo-rules.md` is where most build advice goes wrong. In
particular: modifier thresholds, the feat-count ceiling, and dip placement.

### 5. Deliver as a character sheet

Publish an artifact using `assets/sheet-template.html`. Keep it to **picks and when** — what to
select at each level, the stat spread, the gear targets. Reasoning belongs in conversation, not
on the sheet. State unverified assumptions explicitly rather than smoothing over them.

**A build that needs a mod change is blocked until the change is made, and the sheet has to say
so.** Two exist in this install: **Inquisitor** requires updating its pak to 2.2.1 (the shipped
2.2.0 cannot level past 2), and a **Wisdom-based Blood Hunter** requires the mod.io companion mod
that switches Hemocraft off Intelligence. Name the file, say what replaces it, and mark the build
blocked — never present either as if it works out of the box. And when a mod change moves a
build's primary stat, **re-derive the dip**: a Wisdom Blood Hunter wants Monk's Unarmoured Defence
in a way an Intelligence one never did.

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

**When both characters are being planned together, publish one pair sheet instead** — use
`assets/pair-template.html`. It is the same chassis with the duo-specific structure:

- **One radar with three series** — character A, character B, and a *computed* pair value. The
  combining rule follows the axis kind: additive sums (capped at 5), threshold takes the higher,
  **personal takes the lower**, because a save gap on one character is a party-level gap. Author
  A and B only; never hand-write a pair number.
- **Per-character panes** for ability spread, saves-with-source, and racial kit. Set
  `data-who="a"` / `"b"` — A takes the structure accent, B the highlight accent.
- **A combined "How it plays"** — A's loop, B's loop, then the shared loop. If the third pass is
  just both characters doing their own thing, the pairing is not a pairing.
- **One progression table.** XP is shared, so the levels are shared; both characters' picks sit
  in grouped columns against a single character-level row.
- **Per-character equipment plus a contested table.** Every unique item is assigned to exactly
  one character, with the benefit to the winner and what the loser gives up stated in the row.
  Hag's Hair is one per *run*; the Mirror of Loss is per character.
- **One combined quest-reward table**, with an owner chip per reward.

Theme a pair sheet **once**, on the pair's lead class (highest class level across both).

### 5a. Score the profile radar

The sheet opens with a nine-axis radar, tabbed by act. On `<figure class="profile">` fill
`data-act1`, `data-act2` and `data-act3` — one score set per act — plus `data-bands` for the
character-level range each act covers. **Keep the table rows in sync with the numbers**; the
table is the accessible view and the only thing that survives if the script doesn't run.

Axis order is fixed: **single-target, aoe, durability, actions, control, sustain, skills,
saves, cadence.**

**"Actions" is *action* economy** — bodies, actions and reactions per round. It has nothing to do
with gold. Listo's 4× merchant prices and 120-supply long rests are real constraints and belong
in the gear and cadence prose, but they are **never scored on this chart**. Label the axis
`Actions` on the chart and **Action economy** in the table; never the bare word "Economy", which
in a modlist this expensive reads as money.

**Score 0–5 against what a party needs — a general sense, not a named partner's sheet.** Two-player
Lone Wolf is the *environment* (halved damage, +30% HP, few bodies), so a four-person party's
expectations are the wrong yardstick. But the score must not depend on who the other character
turns out to be, or two sheets from one run can't be read against each other.

| | Anchor |
|---|---|
| **5** | Surplus. Exceeds what the act's encounters demand — this axis wins fights by itself. |
| **4** | Covers this axis alone. Nobody else has to think about it. |
| **3** | Strong. Keeps pace with the act's encounters unaided. |
| **2** | Adequate, but leans on a partner or on consumables. |
| **1** | Thin. A real liability if nobody else covers it. |
| **0** | Absent. |

**Every score is relative to that act's own encounters, and scores are expected to fall.**
Combat Extender scales enemies off *player* level — **bosses reach +170% HP and regular enemies
+126% by 20**, with bosses also gaining +1 AC per 9 levels and +1 spell save DC per 7 — so there
is no out-levelling and no absolute yardstick. A feature that does not scale therefore loses
ground: the Eldritch Cannon's 20 HP and flat 2d8 are excellent at character 3 and nearly
irrelevant by Act 2, and that decline belongs in the numbers. Read a flat row as *keeps pace*,
not as *stopped growing*, and a falling row as the build being outrun.

**Summons are the exception.** CX buffs the `Allies` category too — +34% HP by 20 and **+1 AC
static plus +1 per 4 levels** — so a summon decays far more slowly than a flat-statted feature.
Don't score Actions down as hard as the rest. Numbers in `data/listo-10.2-mcm.md`.

**Score each act separately.** A build that peaks at 20 and a build that peaks at 8 are different
builds, and one polygon cannot say so. Acts map to character levels roughly:

| Act | Char levels |
|---|---|
| I | 1–10 |
| II | 11–15 |
| III | 16–20 |

> These bands are an **estimate**, but the installed CX config supports them: boss level is
> capped at **10 in Act I** and **16 in Act II** (binding from player level 14), while Act III
> bosses are always player level **+4**. Level cap is 20 (`Expansion.Levels.MaxLevel`); most
> players reach 15+ and 20 needs the optional encounter content. Label the bands as approximate
> on the sheet.

What each axis measures, and its **kind** — which decides whether a second source of it is worth
anything to the party:

| Axis | Kind | Scores high when… |
|---|---|---|
| **Single-target** | additive | it kills one priority enemy fast enough that the fight ends before resources do |
| **AoE** | additive | it clears groups. Split from single-target because Listo's encounters lean on numbers, and a build can be excellent at one and absent at the other |
| **Durability** | additive | it survives incoming HP damage. **Effective HP, however it is bought:** AC, hit dice, resistances, damage reduction — *and self-healing*. Durable's full-HP short rests, temp HP on yourself, Second Wind and Lay on Hands spent on yourself all belong here |
| **Actions** | additive | **action economy, not gold, and not just minions** — anything that raises the number of meaningful things the party does per round. Four routes, all scored here: **extra bodies** (summons, familiars, companions, Skeleton Crew), **extra actions on your turn** (Haste, Action Surge, Quickened), **off-turn actions** (Lone Wolf's second reaction, Riposte, off-turn Sneak Attack, interrupts), and **actions handed to your partner** (Twinned Haste, Commander's Strike). **The duo's structural problem, so weight it heavily** |
| **Control** | additive | it reliably removes an enemy's turn — and the CC lands against Listo's inflated saves. Additive because two locked-down enemies are twice as good as one, and area control composes with single-target rather than duplicating it. A build with only single-target CC should *fall* as encounters get more crowded |
| **Sustain** | threshold | it recovers **the other character**: heals aimed outward, raising a downed partner, Greater Restoration and condition removal, temp HP granted to someone else. Not just heal *spells* — but it must be delegatable, or it is Durability |
| **Skills** | **complementary** | it covers out-of-combat checks: expertise, proficiencies, face skills. **Not threshold** — see below, because two characters with different proficiencies cover more of the campaign than either does alone |
| **Saves** | personal | it resists *hard CC*. Distinct from Durability — being Held is a different death than being burst down. Weight Wisdom highest, then Con, then Dex |
| **Cadence** | personal | its resources refresh on **short** rests. Long-rest-only classes score low, because long rests cost 120+ supplies scaling with camp population |

- **Additive** stacks across the party — more is always more.
- **Threshold** saturates at the party's first source. The campaign needs one healer; a second is
  worth far less than the number suggests.
- **Complementary** stacks *only where the two do not overlap*. **Skills is the one axis of this
  kind, and calling it threshold prices it wrong.** Depth does saturate — only one character rolls
  any given check, so a second Persuasion expert adds almost nothing — but **breadth does not**.
  A Rogue with Stealth, Sleight of Hand and Perception beside a Cleric with Religion, Insight and
  Medicine covers more of the campaign's gates than either could alone, and the campaign gates
  content behind *many different* skills.
- **Personal** cannot be delegated at all. A partner's Wisdom save does not stop *you* being Held,
  and their short-rest engine does not refill *your* slots.

**How a complementary axis combines on a pair sheet:** `min(5, higher + floor(lower / 2))`. The
stronger character's coverage stands in full; the weaker one is credited at half, because some of
its proficiencies duplicate ground already covered and some do not. Two characters at 3 and 3
reach **4**, not 5 and not 3 — which is the honest answer for a pair that split the skill list
between them.

**Consequence for planning: the skill map can be divided.** Do not assume one character has to buy
the whole axis. Give the Intelligence character the knowledge gates (Arcana, History, Religion,
Investigation — Religion is the Mirror of Loss gate), give the Dexterity character the physical
ones (Stealth, Sleight of Hand — the Circus pickpocket gate — and Perception), and put the face
skills wherever the Charisma is. **Overlap is the only waste**, so when scoring each half, score
the coverage it *adds*, not the coverage it has.

**Actions is not a summons axis.** A build with no minions at all can score high on it — a
Fighter with Action Surge and a Riposte reaction, or a Sorcerer with Haste and Quickened, is
adding actions per round exactly as a summoner is. If a score here only ever moves when
something is summoned, the axis is being read wrong. Two riders:

- **A multiplier scores on the axis of what it multiplies.** Metamagic is the common case:
  Twinned **Haste** is Actions, Twinned **Hold Person** is Control, Twinned **Death Ward** is
  Durability. Scoring the Metamagic itself on Actions regardless of payload double-counts it
  against the axis the spell already scored on.
- **Discount for concentration.** Haste competes with your control spell, and only one of them
  can be up. An action source that costs concentration in a build that also wants concentration
  for CC is worth materially less than the same effect on a partner or a summon — and if it
  drops, **Lethargy** costs that character their next turn, which out of two bodies is dear.

**Sustain splits by who it targets, and the split decides the axis.** Self-healing is not
delegatable, so scoring it on a threshold axis prices it wrong — a partner's Durable does
nothing for your hit points. Route it by target:

| Recovery aimed at | Axis | Why |
|---|---|---|
| **Yourself** — Durable's full-HP short rests, Second Wind, Fiendish Vigor, self-cast Lay on Hands, temp HP on yourself | **Durability** | It is effective HP bought a different way. Additive, and it makes you harder to remove |
| **The other character** — Healing Word, raising a downed partner, Greater Restoration, Aid, temp HP granted outward | **Sustain** | Genuinely delegatable, so genuinely threshold |

**Count each feature once.** A build with heavy self-healing scores it on Durability and takes
no Sustain credit for it — putting it in both inflates the polygon and breaks the pairing read,
because a partner would see Sustain 4 and correctly conclude they owe nothing, while in fact
nobody can heal them.

> A build that keeps *itself* up but cannot heal its partner should read **high Durability, low
> Sustain**. That is the shape of a self-sufficient martial, and it is exactly the information
> the paired sheet needs.

**So the column never totals, and two sheets are never compared by summed score.** Read the shape
and read the low axes; that is what the chart is for.

**A threshold score is a statement about the whole party, so score it that way.** On a threshold
axis the number says what the *other* character still owes, and the bands are sharp:

| Score | What the partner owes on this axis |
|---|---|
| **5** | Nothing. This build solos the axis. |
| **4** | Optional — worth taking only if it falls out of their chassis free. |
| **≤ 3** | A real investment: levels or a feat. **3 is not "mostly fine"** on a threshold axis. |

Score with that reading in mind, because it is how the paired sheet will be read — see §1b.
It does not apply to additive or personal axes.

**A 4 across the board is a failed evaluation, not a great build.** If nothing scores 1 or 0, look
harder. Then say in one sentence, under the table, what the lowest axis that matters is and what
covers it.

**5 is rare and it is earned.** Reserve it for an axis that ends fights on its own at that point in
the campaign — nine attacks a round with smites, or a Dominate Monster that removes the boss from
its own encounter. Threshold axes reach it least often, and that is information rather than a
defect: you cannot over-invest in Skills the way you can in damage.

**The ceiling still exists at 5.** When a build's real advantage is headroom past what any
encounter demands, say so in prose rather than inflating a number.

## Pitfalls that have bitten before

- **Proposing single-class builds by default.** A 3-level dip is free in feat terms. If the answer
  is single-class, say *why* the dips were rejected.
- **Offering two or three options.** Enumerate from the mods index and present at least six with
  real strengths and weaknesses. Narrowing early hides the good answers.
- **Deciding the niche for them.** Playstyle is the player's call and it eliminates more of the
  option space than anything else. Show the landscape, then ask — don't infer a niche from one
  offhand remark and build three steps past it.
- **Answering in one long monologue.** Chassis, race, stats, feats and gear in a single reply
  gives the player nothing to steer. Ask at each decision that has a real fork.
- **Options that are labels.** "More damage" versus "more control" tells the player nothing they
  didn't already know. Every option names the mechanic, the level and the cost.
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
| `data/listo-10.2-mcm.md` | **Resolved MCM and SE_CONFIG values** read out of an installed copy — Expansion toggles, feat cadence, CX scaling, attunement caps, what ships disabled |
| `data/listo-10.2-mods.tsv` | 706 mods as `ModID<TAB>Name` — grep this to confirm anything exists |
| `data/listo-10.2-manifest.json` | Raw manifest; holds which *file variant* was pulled per mod |
| `data/docs/*.md` | The four Listo doc pages as raw markdown |
| `scripts/strip.sh` | HTML-to-text helper for Nexus and bg3.wiki pages |
| `assets/sheet-template.html` | Character-sheet artifact template, themed |
| `assets/pair-template.html` | Two-character sheet — overlaid radar, shared progression, contested-item table |

The compiled `.md` data files are the **first stop** for "does X exist and what does it do".
They were built from the mods index, the manifest's file variants, and the mod pages themselves,
and they record provenance — anything they mark `(unverified)` needs checking before a build
leans on it. `references/listo-rules.md` owns the **arithmetic and doctrine** only; it
deliberately does not enumerate options.

**Read the warnings at the top of `data/listo-10.2-classes.md` before recommending a class.**
One class ships a version with a known level-up-breaking bug, several mods are pinned behind
their own documentation, and every class mod page's feat table is wrong for Listo.

**Grep the data files, never read them whole** — the manifest is 1.2 MB and the changelog 293 KB.

Everything here is a snapshot of Listonomicon **10.2**, built 8 July 2026, and **checked against
an installed copy on 17 August 2026** (`Version = 10.2` in `Listonomicon.compiler_settings`) —
that pass produced `data/listo-10.2-mcm.md`. If the installed list moves past 10.2, refresh both
before trusting any of it — `references/research-recipes.md` has the commands.
