# Listonomicon 10.2 — Backgrounds and the skill map

**Backgrounds are two free skill proficiencies per character, and the build process kept forgetting
them.** In a two-person party that is **four proficiencies across the pair** — the cheapest skill
coverage in the game, bought with no level, no feat and no gold.

**Provenance.** Compiled 18 August 2026. The background list is BG3 vanilla, confirmed against
bg3.wiki. The "no modded backgrounds" finding and the Listo origin patch were read out of the
**installed paks**, not from a mod page — every `.pak` in the installed modlist had its file table
scanned for background data.

---

## The rule that decides the pick

**BG3 does not implement the tabletop "swap a duplicate proficiency" rule.** If your background
grants a skill your class or race already gave you, **the duplicate is simply wasted** — you do
not get to choose a replacement. Confirmed on bg3.wiki.

So a background is chosen for **non-overlap** — and because the class list is *also* a choice, the
two are solved **together in one pass**, not in sequence. A Rogue who wants Urchin's Sleight of
Hand and Stealth should spend its class picks elsewhere; a Rogue that already took both has thrown
Urchin away. See "Building the skill map" below.

---

## The twelve backgrounds

| Background | Skills | Abilities they key off |
|---|---|---|
| **Acolyte** | Insight, Religion | WIS, INT |
| **Charlatan** | Deception, Sleight of Hand | CHA, DEX |
| **Criminal** | Deception, Stealth | CHA, DEX |
| **Entertainer** | Acrobatics, Performance | DEX, CHA |
| **Folk Hero** | Animal Handling, Survival | WIS, WIS |
| **Guild Artisan** | Insight, Persuasion | WIS, CHA |
| **Haunted One** | Medicine, Intimidation | WIS, CHA |
| **Noble** | History, Persuasion | INT, CHA |
| **Outlander** | Athletics, Survival | STR, WIS |
| **Sage** | Arcana, History | INT, INT |
| **Soldier** | Athletics, Intimidation | STR, CHA |
| **Urchin** | Sleight of Hand, Stealth | DEX, DEX |

> **Haunted One is Dark Urge only.** Every other background is available to any character.

**Two backgrounds are ability-concentrated** — Folk Hero (both WIS), Sage (both INT), Urchin (both
DEX) — which makes them efficient on a character whose primary is that ability and poor on anyone
else. **Noble and Guild Artisan are the face pair**; **Acolyte and Sage** are the knowledge-gate
pair, and Sage covers **Arcana + History** on an Intelligence character in one pick.

---

## The eighteen skills, by ability

This is the map. **It is not the score** — see "Weighting" below, because a proficiency the
character cannot actually pass a check with is not coverage.

| Ability | Skills |
|---|---|
| **Strength** | Athletics |
| **Dexterity** | Acrobatics, Sleight of Hand, Stealth |
| **Intelligence** | Arcana, History, Investigation, Nature, Religion |
| **Wisdom** | Animal Handling, Insight, Medicine, Perception, Survival |
| **Charisma** | Deception, Intimidation, Performance, Persuasion |

**Constitution has no skills**, which is why a Constitution-heavy build never contributes here.

---

## Weighting — five skills carry the axis, thirteen are breadth

**Do not score coverage by counting ticks.** Most of the eighteen gate nothing but flavour text.
Five gate **permanent character power or a unique item**, and those five decide the score. Each
is rolled in a specific **act**, against that act's DC, with that act's proficiency bonus — so
score them **where they land**, not at level 20:

| Gate | Skill | Act | DC | What passing buys |
|---|---|---|---|---|
| **Hag's Hair**, keeping Mayrina | **Persuasion** or **Intimidation** | **I**, char ~4–6 | 20 | permanent **+1** to an ability |
| **Mirror of Loss** | **Religion** | **III** | ~20 `(verify)` | permanent **+2** to an ability |
| **Phalar Aluve +3** | **Sleight of Hand**, pickpocket only | **III** | ~20, scales with value | the upgraded sword |
| Traps, hidden caches | **Perception** — **passive**, never rolled | all three | 15–25 | avoided damage and lost loot |
| Secret doors, switches | **Investigation** | all three | 15–20 | routes and caches |

Everything else is **breadth**: it opens dialogue and small XP, and missing it costs nothing
permanent. Deception and Intimidation sit between — they avoid fights, which has real value under
Combat Extender, but nothing permanent hangs on them.

### Score against the DC of the act the check lands in

Proficiency is **+2** at character 1–4, **+3** at 5–8, **+4** at 9–12, **+5** at 13–16, **+6** at
17+. Expertise doubles it. The routine DC band rises with the act, but **not as fast as
proficiency does** — which is why the earliest gate is the hardest one:

| Act | Char | Prof | Routine DC | The gate that lands here |
|---|---|---|---|---|
| **I** | 1–10 | +2 → +4 | 10–15 | **Hag's Hair, DC 20** — an outlier, rolled at prof **+2/+3** |
| **II** | 11–15 | +4 → +5 | 15–18 | none permanent; Shadowfell dialogue clusters at 18 |
| **III** | 16–20 | +6 | 18–22 | **Mirror of Loss** and the **Circus pickpocket**, both ~20 |

**Hag's Hair is the hardest check in the run relative to what is available.** At character 5 a
face with Expertise and a 20 in the ability rolls `+6 + 5 = +11` — 60%. The same character in
Act III rolls **+17**. Anything whose skill power arrives late — **Reliable Talent at Rogue 11**,
Expertise bought at Bard 10 — **is not there when this check happens**, and the reward is
permanent and missable. Score it separately from the Act III gates.

### A proficiency is not a pass — do the arithmetic

The check is `d20 + ability modifier + proficiency`. Against **DC 20**, at Act III proficiency:

| What the character has | Total | Chance |
|---|---|---|
| Expertise **on the primary ability** (20 → +5) | **+17** | 90% |
| Expertise on a neutral ability (10 → +0) | **+12** | 65% |
| Expertise on a **dumped** ability (8 → −1) | **+11** | 60% |
| Proficiency on the **primary** ability | **+11** | 60% |
| Proficiency on a neutral ability | **+6** | 35% |
| Proficiency on a **dumped** ability | **+5** | **30% — this is not coverage** |

**The rule that follows:** a gate is satisfied only by **Expertise**, or by **proficiency on the
character's primary ability**, or by proficiency plus stacked boosts. Plain proficiency on a dump
stat is a tick on the map and a failed check in the game.

**Where this bites hardest is Religion**, because Religion keys off **Intelligence** and almost
nothing in a duo runs Intelligence. A Cleric with Religion on its class list and INT 8 rolls
**+5** against the Mirror of Loss. The pair has "covered" Religion and cannot pass it. Answers,
cheapest first:

- an **Intelligence primary** — Wizard, Artificer, Inquisitor, or the **Intelligence** Blood
  Hunter, which reaches +11 on plain proficiency;
- **Knowledge Domain's Blessings of Knowledge**, which is Expertise in Religion outright;
- a **Bard 3 (Lore)** dip — Expertise ×2, spendable on Religion, from three levels;
- the **Skilled Expert** feat — a proficiency, **an Expertise, and +1 to any ability**, which
  buys the gate outright for one of seven feats.

### The boosts, and which kind of check each one reaches

| Source | Size | At-will? | Reaches |
|---|---|---|---|
| **Guidance** — cantrip, 10 turns, no concentration | **+1d4** (avg +2.5) | **yes** | every rolled check, planned or not |
| **Enhance Ability** — 2nd level, concentration | **advantage** (≈ +3.3, more near the DC) | no | one ability, planned checks |
| **Bardic Inspiration** | +1d6 → +1d12 | no | any check, planned |
| **Reliable Talent** — Rogue 11 | rolls of 9 or lower **count as 10** | **passive** | every proficient check, **from Act II on** |
| **Silver Tongue** — Eloquence Bard 3 | same, on **Persuasion and Deception** | **passive** | those two, **from Act I** |
| Durge origin passive | +1 Intimidation, +1 Deception | passive | those two |

**Where Guidance comes from — and why it is a tiebreaker, not a requirement.** It is free on the
Cleric, Druid and Artificer lists; if either character is one of those, take it and move on.
Everyone else is buying it, and **the price is usually too high**:

- **Blessed Warrior** or **Druidic Warrior** fighting style. This is described everywhere as
  "free" and it is not — it **costs the Fighting Style slot**, and in Listo that slot holds real
  options. **Protection** gives **disadvantage on ALL attack rolls** against an ally who stays
  within 1.5m, until your next turn — in a two-person party where losing either character ends
  the fight, and with Lone Wolf handing out an extra reaction, that is the strongest defensive
  effect available to a martial. **Great Weapon Fighting** sets the minimum melee damage die to
  3, and **Duelling**'s +2 per hit is multiplied by every crit-smite the build lands. **Do not
  trade any of those for a cantrip.** Take Blessed Warrior only when the slot is genuinely idle.
  `(Which classes are offered the UA styles is unverified — Blood Hunter is not, its list is
  hard-coded to the five vanilla styles.)`
- **Magic Initiate** or **Ritual Caster** — one feat of seven, Guidance among the cantrips.

**And weigh it against the bank before paying anything.** Guidance is +2.5 on a single roll. On a
60% check that is worth about ten points of single-roll chance — but with two Inspiration rerolls
that check is already at 94%, so the cantrip is worth a fraction of a point where it matters most.
Its real value is on **unplanned** checks, where you do not want to spend the bank at all.

Three consequences worth planning around:

1. **Guidance is a pair-level property.** Cast it on whoever is talking, before dialogue starts.
   A pair with no Cleric, Druid or Artificer and no fighting style to spend has **no at-will
   bonus at all**, and every unplanned check is 2.5 lower for the whole campaign.
2. **Reliable Talent turns the Act III gates into formalities and does nothing for Act I.** A
   Rogue 11+ with Expertise and any positive modifier has a floor of `10 + 12 + mod` = **22 or
   better** — every Act III DC 20 passes without rolling. It arrives after Hag's Hair.
3. **Passive Perception takes none of them.** It is `10 + WIS + proficiency`, doubled with
   Expertise, and Guidance does not apply. The only way to raise it is Wisdom, proficiency and
   Expertise — so passive Perception belongs on the **high-Wisdom** character, not on whoever
   happened to have a spare pick.

### Inspiration — the bank that turns a marginal check into a passed one

**Backgrounds do a second job, and it is the bigger one.** Fulfilling a background's goals grants
**Inspiration**, and a point is spent to **reroll a failed ability check**. Plan around the bank
rather than around the single roll:

- The pool caps at **4 points** and is **shared across the party** — either character's goal fills
  it, either character can spend it. At 4 you stop gaining, so spend down before a goal cluster.
- It rerolls **ability checks** — dialogue and world skill checks. It does **not** touch saving
  throws, attack rolls, or **passive** checks.
- Because the pool is shared and the goals are per-background, **choose the pair's two backgrounds
  so their goals fire in different content**, not the same content. Two backgrounds that both key
  off the same act's questline fill the bank half as fast as two that split it.
  `(Which goals belong to which background, and when each fires, is not enumerated here — verify
  in game if the pair is relying on an early bank.)`

**What a bank is worth.** With `k` rerolls the chance of clearing a gate is `1 − (1 − p)^(k+1)`:

| Single roll | +1 reroll | +2 rerolls | Full bank of 4 |
|---|---|---|---|
| **5%** — untrained, DC 20 | 10% | 14% | **23%** |
| **10%** | 19% | 27% | **41%** |
| **30%** — proficiency on a dump stat | 51% | 66% | **83%** |
| **40%** | 64% | 78% | **92%** |
| **45%** | 70% | 83% | **95%** |
| **50%** | 75% | 88% | **97%** |
| **60%** — Expertise on a neutral ability | 84% | 94% | **99%** |
| **70%** | 91% | 97% | **99.8%** |

**Two rerolls is the standing assumption** for a critical gate; the full bank is available for the
single most important one. Three consequences, and they reorder the whole axis:

1. **A guaranteed floor is worth much less than it looks.** Reliable Talent and Silver Tongue
   still remove all risk, but a 60% check with two rerolls is 94% — close enough that "guaranteed"
   stops being a build requirement. Do not pay levels for certainty you can bank instead.
2. **Inspiration cannot fix a missing proficiency.** Untrained against a DC 20 is 5–10% a roll;
   the entire bank drags that to 23–41%. **The discriminator is no longer the size of the
   modifier — it is whether any character can roll the check at all.**
3. **Passive Perception is the one gate the bank cannot reach**, because nothing is rolled. That
   makes it the axis's most load-bearing number: it must be bought with Wisdom, proficiency and
   Expertise, on the high-Wisdom character, up front.

### Scoring the axis

Audit the five gates at the act each lands in, then score:

Score each gate at the act it lands in, **with two Inspiration rerolls assumed**:

| Score | The pair |
|---|---|
| **5** | Every rolled gate at **≥90% with two rerolls**, every one of them on a **proficient** character, and **passive Perception 21+** |
| **4** | Every gate has a proficient character, but one needs the **full bank** to clear 90%, or passive Perception is **17–20**, or **Investigation** has no proficient character, or the pair has **no Guidance** for unplanned checks |
| **3** | **No proficient character on Hag's Hair, the Mirror or the pickpocket**, or passive Perception **≤16** |
| **2** | Two gates with no proficient character |
| **1** | Three or more |

**The failure mode this rubric is built to catch** is a gate nobody can roll. A bad modifier is a
few reloads; a missing proficiency is a reward you do not get.

**Audit the five before counting the eighteen.** Breadth only breaks ties.

---

## Modded backgrounds — there are none

Scanned the file table of **every `.pak` in the installed modlist** for background data. Only
three mods carry any, and none of them add a playable background:

| Pak | What it holds | Verdict |
|---|---|---|
| `spjammer_dnd5e_voiced.pak` (Spelljammer 5e) | `Backgrounds/Backgrounds.lsx` — **zero bytes** | Empty, and the mod is `-OPTIONAL_Spelljammer 5e` — **disabled in the profile** |
| `Dark_Urge_All_Origins` | `Backgrounds/Backgrounds.lsx` — an empty `<region>` node | Adds no background; it widens which origins can be the Dark Urge |
| `CommunityLibrary`, `CompatibilityFramework` | Background *tag* dictionaries and handlers | Framework plumbing, not content |

**So the twelve above are the whole pool.** Do not go looking for a modded background list; there
isn't one.

---

## What Listo *did* change: origin skill passives

`ListoPatches.pak` ships `BackgroundPassives.txt`, which gives **each origin character a passive
granting flat skill bonuses** (a bonus to the check, not a proficiency):

| Origin | Passive grants |
|---|---|
| Astarion | Performance +1, Acrobatics +1 |
| Gale | Arcana +1, History +1 |
| Halsin | Nature +1, Medicine +1 |
| Jaheira | History +1, Survival +1 |
| Karlach | Intimidation +1, Religion +1 |
| Lae'zel | Intimidation +1, Perception +1 |
| Minsc | **Intimidation +2, Acrobatics +2** |
| Minthara | Intimidation +1, Religion +1 |
| Shadowheart | Arcana +1, Religion +1 |
| Wyll | Persuasion +1, Investigation +1 |
| **The Dark Urge** | **Intimidation +1, Deception +1** |

**Only the Durge row matters for a custom pair** — a player character is a Tav or a Durge, and the
Durge is the one that carries a skill passive. It is small, but it is free, and it points a Durge
toward the intimidation half of the face role. `(Verified from the shipped pak. Whether the
passive also applies when a Durge respecs is unchecked.)`

---

## Building the skill map — one pass, both characters, at level 1

**Do not fill the map sequentially.** "Class picks first, background last" wastes coverage,
because the class list and the background list overlap heavily and both are *choices*. Solve it
as **one assignment problem across the pair**, at level 1, before either character is made.

**1 · Write down what is fixed.** These are not choices and they constrain everything else:

- **Race grants** — Astral Elf and Wood Elf give Perception; Lizardfolk gives two from a list.
- **Subclass grants** — Way of the Kensei hands over Performance, Way of Mercy gives Insight and
  Medicine, Vengeance Inquisitor gives Expertise in an Intelligence skill.
- **Feat grants already planned** — Alert gives Perception, Dungeon Delver Expertise in Sleight
  of Hand and Perception, Skilled three of anything.

**2 · Reserve the gates.** Assign each to the character with the higher ability modifier for it,
and mark it for Expertise:

| Gate | Skill | Put it on |
|---|---|---|
| Hag's Hair, DC 20 | **Persuasion** (or Intimidation) | the higher Charisma |
| Mirror of Loss | **Religion** | either — but it must exist |
| Circus pickpocket | **Sleight of Hand** | the higher Dexterity |
| Traps, secrets | **Perception**, **Investigation** | split them |

**3 · Count how many picks each character actually has.** Level-1 class list (2–4), the
multiclass node of any dip (usually 1, sometimes 0), college or subclass bonus proficiencies
(Lore gives 3), background (2), and any feat. **A dip taken later in the ladder still grants its
skill immediately when taken** — but plan as if you have it, because the pick is not re-chosen.

**4 · Allocate every slot at once, cheapest source first.** Take a skill from the source that can
*only* give that skill, and leave the flexible sources for last:

- A **class list is narrow** — take from it the skills only that class offers (Religion on a
  Cleric or Blood Hunter, Arcana on a Warlock).
- A **background is fixed in pairs**, so pick the pair whose *both* halves are still unclaimed.
  Sage is two Intelligence skills, Urchin two Dexterity, Folk Hero two Wisdom — those are
  efficient on the right character and half-wasted on the wrong one.
- **Lore's three and Skilled's three are wildcards.** Spend them last, on whatever the first two
  steps could not reach.

**5 · Check for overlap and delete it.** Two characters proficient in the same skill is one pick
thrown away, with two exceptions worth doubling: **Perception**, because it is rolled passively
and often, and **Sleight of Hand** if both will attempt the Circus.

**6 · Audit the five gates, then score** — for each of Hag's Hair, the Mirror of Loss, the Circus
pickpocket, passive Perception and Investigation, write down **who rolls it, at what total, in
which act**. Coverage count does not enter the score; it only breaks ties. See "Weighting" above.

> **Step 2 has a consequence step 4 must honour:** assigning a gate to the character with the
> higher modifier is not enough if that modifier is still too low. **Religion on a Cleric's
> dumped Intelligence is not coverage** — it needs Expertise, an Intelligence primary, or the
> Skilled Expert feat. Check the arithmetic before moving on.

> **Worked shape, and the trap in it.** A Cleric with Religion and Medicine from the class list,
> Sage for Arcana and History; beside a Rogue with Stealth, Sleight of Hand, Investigation and
> Deception from the class list, Perception from the race, Survival from a Ranger dip, and Guild
> Artisan for Insight and Persuasion. Twelve of eighteen, zero overlap — **and it still fails the
> Mirror of Loss**, because the Cleric's Religion sits on a dumped Intelligence at `+6 − 1 = +5`.
> The map looks finished and the gate is not covered. That is the whole reason step 6 exists.

**Cross-reference:** the Skills axis is **complementary**, not threshold — see
`references/listo-rules.md`. Breadth stacks across the pair, depth does not, which is why step 5
matters — but breadth is the tiebreak, not the score. **The five gates are the score.**
