# Pairing ledger data format

Author a JSON file; render it. **Never hand-write ledger HTML** — it is ~175KB,
and every number in it is derived from about 200 lines of chassis scores.

```sh
scripts/render_ledger.py ledger.json -o ledger.html
```

`assets/ledger-example.json` is a filled-in ledger — copy it and overwrite.
Every string is emitted as HTML, so inline `<b>`, `<em>` and `<code>` work.

## What the renderer computes — never author these

| Thing | Rule |
|---|---|
| Pair value per axis | by axis kind — **`listo-build/references/scoring-model.md` §4 is authoritative**: additive `a+b` uncapped, complementary `hi + ⌊lo/2⌋` **uncapped**, personal `min` |
| Fight-type terms | crowd and boss terms per `scoring-model.md` §5, MIX-blended 70/30, 60/40, 50/50 by act |
| Reach discount | applied to the **single-target damage term only** — control takes none |
| Melee lock | a further ×0.9 on crowd when neither reach is `ranged`/`hybrid` |
| Tempo cap | `min(capability breadth, action points)` — Actions bounds tempo rather than adding to it |
| Score | the four blocks of `scoring-model.md` §9 |
| Idle-body flags, holes, chips | flag under 3.0 in a fight type worth ≥40% of the act; hole is any pair axis ≤2 |
| The whole field table | **every chassis with every other**, ranked — `C(n,2)` unordered pairs |
| Which pairings become entries | each chassis's **best** partner, ranked, capped at `entry_limit`; a pairing that two chassis both name is kept once |
| Which pairings the field table lists | the **whole frontier**, always, then the highest-scoring dominated pairings up to `field_limit`; the number omitted is stated |
| Every number in a variation line | from the pairing itself — you write only the clause after it |
| Roster order | by the best score that chassis reaches anywhere |
| Order within a pairing | higher delivered damage first, then higher total axis value, then the id alphabetically — see `scoring-model.md` §10 |
| The pairing's heading | `<lead> & <partner>`, from the selection — an authored `name` that disagrees is a **hard error**, not an override |

**This list is the point of the format.** Hand-written variation figures were the
single largest source of stale numbers in the previous ledger: a re-score moved
135 pairings and left 27 quoted figures behind. Here they cannot go stale,
because they do not exist until render time.

## Shape

```jsonc
{
  "title":   "Listo Pairing Ledger",       // browser tab / artifact name
  "eyebrow": "Listonomicon 10.2 · two-player Lone Wolf",
  "lede":    "One paragraph on what the ledger is for.",
  "facts":   ["26 chassis", "level cap 20"],   // mono chips under the standfirst
  "entry_limit": 12,                        // chassis beyond this fall out, and are named
  "field_limit": 500,                       // field-table rows; the frontier is always kept
  "footer":  "Provenance line.",

  "chassis": {
    "Bombard": {                            // key is the id; used for anchors
      "display": "Bombard",                 // optional; shown instead of the key
      "reach":   "hybrid",                  // ranged | hybrid | mobile | static
      "split":   "Blood Hunter 14 (Order of the Profane Soul) / Wizard 6 (Evocation)",
      "meta":    "Int 22 · 7 feats",
      "note":     "Prose. What the chassis is and what it gives up.",
      "strength": "Why it is worth playing *in this run* — two bodies, Lone Wolf, Listo's inflated encounters.",
      "wants":    "What it needs from the other half of the duo, stated as a capability, not a class.",
      "concentration": false,               // does this body's plan ride a concentration spell?
      "saves": {                            // source of truth for the saves axis — see below
        "I":   {"prof": ["int","wis","dex","con"], "boosters": []},
        "II":  {"prof": ["int","wis","dex","con"], "boosters": []},
        "III": {"prof": ["int","wis","dex","con"], "boosters": []}
      },
      "scores": {                           // 10 per act, in AXIS ORDER; index 8 is null
        "I":   [3,2,3,2,2,1,0,3,null,4],
        "II":  [4,4,3,3,4,2,0,3,null,4],
        "III": [4,4,3,3,4,2,0,3,null,4]
      }
    }
  },

  "entries": {                              // keyed by CHASSIS id, not by pairing
    "Bombard": {
      "name":    "Bombard & Fervor",   // must match the computed pairing exactly, or the render fails
      "tag":     "caster blood hunter + weapon-cleric support",
      "verdict": "Reads as. …",
      "cost":    "Costs. …",
      "vars": [
        {"partner": "Chains", "note": "Hold Monster on a short-rest clock."},
        {"text": "<b>Wisdom variant</b>: free prose, no numbers attached."}
      ]
    }
  },

  "method":  {"h2": "…", "cards": [{"title": "Coverage", "body": "…"}]},
  "caveats": {"h2": "…",
    "excluded":    {"summary": "Excluded chassis, and why", "items": ["…"], "lead": "optional trailing paragraph"},
    "settled":     {"summary": "Settled by reading the installed paks", "items": ["…"]},
    "assumptions": {"summary": "Assumptions that would still move numbers", "items": ["…"]}
  }
}
```

### `note`, `strength` and `wants` do different jobs — write all three

The score matrix says *how much*; it cannot say *why you would pick this body* or *who it needs
beside it*. Those are the two questions a roster card exists to answer, and neither is derivable
from ten integers.

| field | answers | keep it to |
|---|---|---|
| `note` | what the body **is**, and what it gave up to be that | 1–2 sentences |
| `strength` | what makes it strong **for this scenario** — two characters, Lone Wolf's doubled economy and halved damage, Absolute Wrath's resistances, a 120-supply long rest | 1–2 sentences |
| `wants` | what it needs from **the other half of the duo** | 1 sentence |

**`strength` must be scenario-specific.** "Good damage" is not an answer — a four-body party would
say the same. What earns the line is the thing that is true *here*: a second Action doubling a
bonus-action engine, an aura that covers a party of two entirely, a short-rest clock against
expensive long rests, a damage type that sidesteps layered resistances.

**`wants` names a capability, not a class.** "Wants a Cleric" is unusable — every duo can respec.
"Wants a body that holds the pair's one concentration slot, because this one never will" tells a
reader which half of the field to look in. Where the split rule bites — 5 + 0 is worse than 3 + 3 —
say which axis is at 0 and needs covering.

**Axis order is fixed** and every `scores` array must have **ten** entries:

    single-target, aoe, durability, actions, control-single, control-area,
    rescue, skills, saves, endurance

Control is **two axes**, split crowd-versus-boss exactly as damage already is — see
`axis-rubrics.md` §5 and §6, and `scoring-model.md` §3. It is the only axis that gained a split;
§7 there records why Rescue, Saves and Durability did not.

## Everything addressable has a stable id

| target | id | linked from |
|---|---|---|
| section | `method` `field` `entries` `roster` `caveats` | its own `<h2>` |
| entry | `e-<chassis, lowercased>` | its `<h3>`, its rank number, and the entry chip in the field table |
| roster card | `r-<chassis, lowercased>` | its `<h3>` and the members line on every entry |

**Section ids are authored, never slugged from the heading text.** The method and caveats headings
are configurable in the ledger data, so an id derived from prose would change the moment somebody
reworded a title and would silently break every link anyone had saved.

Headings are themselves the anchor rather than carrying a separate marker, so the link target is
the thing being read. The `#` sigil appears on hover only.

## The field table shows tempo and rest per act

Both halves of the score move between acts, so both are broken out. Rest was originally a single
averaged column, which was an inconsistency rather than a decision: measured across the field, a
pairing's rest varies **7.2pp** between its best and worst act at the median against tempo's
**8.2pp**, and 70% of pairings move at least 5pp. The averaged column hid that — most visibly on
Skills, which can swing a full rung between Act I and Act III.

Column headers carry `title=` help generated from `KEYS` / `LABELS` / `KINDS` / `KIND_MAX`, so a
tooltip cannot drift from the arithmetic it describes. Do not hand-write axis tooltips.

## `vars` always swaps the partner, never the headliner

An entry exists to be about one chassis — the one it headlines — so a variant keeps that body and
replaces the **partner**. `{"partner": "Coda"}` on the `Dawnblind & Silvercrit` entry means
*Dawnblind beside Coda*, with Silvercrit leaving.

The renderer used to print this as a bare `+ Coda`, which left the reader to guess which half of
the heading was being swapped out. It now names the body going out and the body coming in:
**"Silvercrit &rarr; Coda"**. The retained chassis is the heading's other half and is not
repeated. Nothing changes in the authored data — only the rendering — but two authoring
mistakes are now hard errors rather than confusing output:

| authored | why it fails |
|---|---|
| `{"partner": "<the current partner>"}` | a variant that swaps in the body already there says nothing |
| `{"partner": "<the headlining chassis>"}` | the headliner never leaves; pairing it with itself is not a pairing |

A free-form alternative uses `{"text": "<b>Heading</b>: …"}` instead and is rendered verbatim.

## The skills axis is authored as modifiers, not a number

Index 7 is **derived** too, from `skills` — a modifier map per act. Same reason as saves: the
rubric is written in terms of which checks a pair can actually clear, and a bare 0–5 cannot be
re-checked from outside.

```jsonc
"skills": {
  "II": {"Perception": 9, "Investigation": -1, "Persuasion": 4, "Deception": 8}
}
```

Each value is the **finished number the body rolls** — ability modifier + proficiency bonus +
Expertise + reliable permanent bonuses. **Proficiency bonus is pinned at +3 / +4 / +5 by act**;
do not derive it from character level.

**Three skills are mandatory in every act, even at a negative modifier:**

    Perception      traps and hidden caches, DC 15–25
    Investigation   secret doors and switches, DC 15–20
    Persuasion      routine town dialogue, DC 10–15 / 15–18 / 18–22 by act

These carry the axis because they are the checks that **cannot be prepared for**. Everything
telegraphed can be bought: Withers charges 100 gold, and bg3.wiki documents respeccing into
Rogue 11 / Knowledge Cleric 1 to pass the Mirror of Loss at DC 25, then respeccing back
*"retaining the Mirror of Loss stat enhancement"*. A check any chassis can rent its way past
measures the wallet. **An absent value for one of these three is an evidence gap, not "untrained",
and the renderer raises rather than reading it as hopeless.**

The named gates — Hag's Hair on Deception or Intimidation, Free Us, the Araj pickpocket on Sleight
of Hand — may be omitted when the body genuinely has nothing on them, because there absence *is*
the answer. They are also the weaker half: each has a no-check route to the same ability point, so
passing buys the secondary prize rather than the +1 or +2. **Religion is no longer read at all.**

Rerolls are credited on the named gates only. Traps roll automatically with no prompt, so there is
nothing to spend Inspiration on, and four charges do not stretch across a run of town dialogue.

## The saves axis is authored as a set, not a number

Index 8 is **derived** and must be authored as `null`. Every other axis is a judgement against
`listo-build/references/axis-rubrics.md`; saves is the one axis whose rubric is written in terms
of *which* abilities are proficient and whether the grants are **disjoint**, so a bare 0–5 cannot
be re-checked from outside. Author the evidence and let the renderer score it.

```jsonc
"saves": {
  "II": {
    "prof":     ["wis","dex","con","cha"],   // the RESULTING set, deduplicated
    "boosters": ["brutish-durability"]        // blanket effects, not proficiencies
  }
}
```

`prof` — lowercase from `str dex con int wis cha`. Record the **union after de-duplication**, which
is what makes the disjointness rule bite: Blood Hunter's `int + dex` on top of a Lone Wolf `int +
dex` pick is two entries, not four. Grants are the **level-1 class** (two, and only the level-1
class), **Lone Wolf's two picks**, each **Resilient**, **Slippery Mind** (Rogue 15, adds `wis`),
and **Diamond Soul** (Monk 14, adds all six).

`boosters` — numeric or advantage effects that apply across saves without granting proficiency.
Three tiers: **blanket** buys the rung the table trades a proficiency for; **partial** covers only
part of the save set or costs a resource, and **two partials count as one blanket — but only if
together they cover at least two of Wisdom, Constitution and Dexterity**, since those are the
saves a duo actually loses to; the third tier
is documented but buys no rung on its own.

Advantage against *spells and magical effects* counts as blanket — in this list almost every save
that decides a fight comes off one, so the condition is nearly always met.

| id | what | scope | tier |
|---|---|---|---|
| `brutish-durability` | Fighter 7 — +1d6 to every save, unconditional, no resource | self | blanket |
| `aura-of-protection` | Paladin 6 — +Cha modifier to every save | **pair** | blanket |
| `emboldening-bond` | Cleric Peace — +1d4 to every save, on both bodies | **pair** | blanket |
| `friars-blessing` | Way of the Friar — +1d4 to every save, on both bonded bodies | **pair** | blanket |
| `lunar-champion` | Oath of the Moon 20 — +Cha to all saves in an aura | **pair** | blanket |
| `heroic-warrior` | Champion — a free reroll on a failed save, every turn | self | blanket |
| `magic-resistance` | Paragon 9 — advantage on saves vs spells and magical effects | self | blanket |
| `spell-resistance` | Wizard Abjuration 14 — advantage on saves vs spells | self | blanket |
| `magic-awareness` | Wildsurge — proficiency bonus to **both** bodies' saves vs spells | **pair** | blanket |
| `rage-of-ginnungagap` | advantage on all saves vs spells while raging | self | blanket |
| `dark-augmentation` | Blood Hunter 2 — +Int modifier to Str, Dex and Con saves | self | partial |
| `towering-ego` | Mesmerist 2 — +Cha to Wis saves, +half Cha to Int saves | self | partial |
| `frost-rune` | Rune Knight — +2 to Str and Con saves | self | partial |
| `fanatical-focus` | Zealot — one reroll on a failed save per Rage | self | partial |
| `gift-of-will` | Trickster — +Cha and half level to the **partner's** Wisdom saves | **pair** | partial |
| `flash-of-genius` | Artificer 7 — +Int to an ally's save, costs a reaction | **pair** | partial |
| `indomitable` | Fighter 9 — reroll a failed save, 1–3 per long rest | self | partial |
| `supernatural-defense` | Monster Slayer 7 — +1d6 on every save your prey forces | self | partial |
| `cosmic-omen` | Star Druid 6 — ±1d6 on a save, recharging on a short rest in Listo | self | partial |
| `legendary-resistance` | Paragon 15 — automatically succeed a save | self | partial |
| `soul-of-artifice` | Artificer 20 — +1 to every save while holding an infused item | self | partial |
| `danger-sense` | Barbarian 2 — advantage on Dexterity saves, unconditional | self | partial |
| `bladesong` | Bladesinging 2 — +2/+3/+4 to Constitution saves | self | partial |
| `war-caster` | advantage on concentration saves only | self | no rung |

`war-caster` stays a legal id because it is worth recording; its value is already priced by
`concentration` and the rung-3 cap. It is keyed to the **effect**, not the feat — Way of the
Friar's Guardian of Light grants the same thing and takes the same id.

`concentration` (chassis-level, not per act) — `true` if the body's plan rides a concentration
spell. It reorders the ability weighting: **Con outranks Wis when true**, since a broken
concentration is a lost body one turn later; otherwise the ordering is Wisdom > Constitution ≈
Dexterity > Charisma > Strength > Intelligence.

### How the renderer derives index 8

Rungs follow `axis-rubrics.md` §9. `key` = `{wis, con, dex}`.

| value | test |
|---|---|
| 0 | `len(prof) ≤ 2` and no `key` ability |
| 1 | `len(prof) == 2` and ≥1 `key` |
| 2 | `len(prof) == 3` and ≥1 `key` |
| 3 | `len(prof) == 4` and ≥2 `key` |
| 4 | `len(prof) ≥ 4` covering all of `key`, **or** any blanket booster |
| 5 | all six proficient, **or** rung-4 coverage **and** a blanket booster |

Then: **if `concentration` is true and `con` is not in `prof`, cap the result at 3.** A body that
holds the pair's one control spell without a Constitution save is structurally fragile regardless
of what else it is proficient in.

### Anything with special handling fails closed

**An unknown value is a hard error. Never skipped, never defaulted, never warned-and-continued.**

The failure this prevents is one-directional and invisible. A booster the renderer does not
recognise contributes nothing, so the score comes out **too low** — and a score that is too low is
indistinguishable from an honest one. Nothing downstream can catch it: the field table still
ranks, the entries still render, the chassis just quietly sits a rung below where it belongs.
Every other class of bug in this format announces itself; this one does not.

So the checking is reactive rather than an ongoing tax. You do not have to remember to audit
boosters before every render. You have to fix a crash when you author something new, once.

**Every enum in this format is closed** — `role`, `reach`, `prof` abilities, `boosters` ids,
`redirect` ids, act keys, axis kinds. Unknown member, raise. Do not add a permissive branch to any of them.

**Before authoring a value with special handling, confirm the renderer implements it.** The
registry in `render_ledger.py` is the authority; the tables in this file mirror it. Adding a
booster is one change that touches the registry, the table above, and a case that exercises it —
if you cannot point at the line that applies the effect, it is not implemented, and authoring the
id is how you find that out at render time instead of after publishing.

**A deliberate drop must be distinguishable from an unrecognised one.** The only sanctioned drop
in this format is a repeated pair-scope booster in one pairing, below. It warns by name and says
what it dropped and why. Nothing else silently discards an authored value.

### Pair-scope boosters raise both bodies

A `pair` booster cannot be scored inside one body's value: it applies to both, so the combiner
applies it to each side *before* taking the `min` for the Personal axis.

**Non-stacking is per effect, not per scope.** An Aura of Protection and an Emboldening Bond are
different sources and both apply. Two Auras of Protection are one Aura — the second is ignored, the
renderer warns by name, and the levels that bought it are wasted. That is the commonest way a pair
throws away six levels, and it is now checked for every pair-scope id rather than only for Aura.

### Redirection raises the pair's floor

`dur` is Personal — the pair is its weaker body, because that is the one that dies. Everything the
tougher body carries above that minimum is discarded. **Redirection is the one effect that argues
with the operator**: a body that can take damage aimed at its partner converts durability it was
not using into floor the pair does not have.

```jsonc
"redirect": {
  "I":   [],                    // the bond is not online yet
  "II":  ["warding-bond"],
  "III": ["expansive-bond"]     // Peace 17 — and now it lands at resistance
}
```

Optional, and **absent means no bond** — unlike `skills`, most bodies genuinely have none and the
empty case has to stay cheap to author. A *present* block must state every act, because a bond
arrives at a level.

| id | what | tier |
|---|---|---|
| `warding-bond` | Peace Cleric 3 · Battle Smith 5 · Oath of the Moon 5 · Favored Soul (Peace) at Sorcerer 3 · Bard Magical Secrets 14/18 | 1 |
| `protective-bond` | Cleric Peace 6 — reaction, teleport adjacent, take **all** of it instead | 1 |
| `expansive-bond` | Cleric Peace 17 — 18m, and the interceptor takes it **with resistance** | 2 |

**Paladin access is per-oath, not class-wide.** `listo-10.2-spells.md` names Warding Bond among the
notables the expanded Paladin list gained, which would have made all 15 Paladin chassis carriers.
It does not: a sweep of all 810 paks found the only Paladin route is **Oath of the Moon's** own
list, `Target_Moonbeam;Target_WardingBond`, granted by the `MoonOath` progression at 5. No base
Paladin progression references a list containing the spell. Author it on Moon Paladins only.

Three near-misses that look like access and are not, each verified inert: the "Cleric War Domain
Enhanced Paladin SLevel 2" list (`Spells Extra`) contains the spell but **no progression references
it**; the five `5e Spells` lists carrying it have zero references anywhere in the load; and the BG3
Community Library's Bard Magical Secrets SLevel 5–9 lists are superseded by the merged
`ListoPFSpells` pool. Knowledge Cleric's `BardMagicalSecrets` selectors at 6 and 10 draw from lists
that do not contain it. Wish (`ATT_WISH_SPELLS_2`) does grant it, off a 9th-level slot.

**Twinned Spell is irrelevant here**, whatever the class docs imply. `Target_WardingBond_UCL`
(Utut's Core Library, the base every copy inherits) gates targeting on `not Self()`, and its
`RequirementConditions` refuse the cast outright while the caster already holds `WARDING_BOND` or
`WARDING_BOND_CASTER` — one bond per caster, ever. In a duo the partner is the only legal target
and there is no second one for Twinned to reach. Twinned genuinely doubles Cure Wounds, Death Ward
and Greater Restoration, because those can be aimed at the caster; this one it cannot help.

**Mesmerist Reflection is not on this list**, though it reads like it should be and is literally
built out of Warding Bond — `EYEBITER_WARDING_BOND` in `BoldStares.txt` is `using "WARDING_BOND"`.
The bond goes on **self**, and its source is the *stared enemy*: `RedirectDamage(1,Psychic,true)`
reflects damage onto the thing you are staring at. `Target_EndHypnoticStare` clears it with
`RemoveStatus(SELF,EYEBITER_WARDING_BOND)`, which fixes the direction beyond doubt, and nothing in
the pak applies a status to an ally. The Eyebiter Mirror boon is real but is **self** durability —
`BOLDSTARE_MIRROR_GENERAL` boosts `DamageReduction(All,Flat,1)` — so it belongs in that body's
authored `dur` rung, not here. A body cannot share a floor it only has itself.

Only the **tougher** body's bond counts. The carrier is the one eating the damage, and a bond
running the other way lowers the floor it was meant to raise. It splits the surplus — the gap is
what it has spare and it keeps half, rounding down at tier 1 and up at tier 2:

```
tank 5 + partner 2   ->  3   (tier 1)      4  (tier 2)
tank 3 + partner 2   ->  2                 3
tank 5 + partner 5   ->  5                 5      nothing spare to move
```

So the transfer scales with how much tougher the carrier actually is: a rung-3 body compensates for
half of what a rung-5 body does, and a body whose partner is already its equal transfers nothing.
**The maximum never rises.** This relocates durability; it cannot manufacture it.

This does **not** touch `rsc`. `axis-rubrics.md` caps redirection at rung 1 there and is right to —
a bond does not pick up a body that already went down. That cap prices it as *rescue*; this prices
it as *transfer*, which is a different question about a different axis.

## Errors the renderer raises rather than papering over

These are **fatal, by design** — see "Anything with special handling fails closed". A render that
cannot score something correctly must not produce a number for it.

- a chassis with an unknown `reach`
- a `scores` array that is not **ten** long
- a `scores` array whose index 8 is not `null` — saves is derived, never authored
- a chassis with no `saves` block, or one missing an act
- a `prof` entry outside `str dex con int wis cha`, or a duplicate within one act
- an unknown `boosters` id
- an unknown `redirect` id, or a `redirect` block that is present but missing an act
- an entry whose chassis survives the `entry_limit` cut but has no prose
- a variation naming a partner the chassis has no pairing with
- **an entry whose `name` disagrees with the pairing selection actually made**

That last one is newer than the others and was added after it bit. The heading used to print the
authored `name` while the members line beside it printed the *computed* pair, so the two could
disagree silently. When a selection rule changed — capping how many entries one chassis may
partner — eleven entries kept a heading and a body of prose written about the partner they no
longer had, sitting above numbers computed from a different pairing. Prose about the wrong
pairing is worse than no prose, so the heading is derived and a contradicting `name` stops the
render.

The last two are the ones that bite. A chassis that rises into the cut needs prose
before the ledger will build, which is what stops the entries and the field
table drifting apart.

## There is no carry/support field

A chassis is **not typed**. The renderer pairs every chassis with every other, so a duo of two
damage bodies or two controllers is representable and rankable rather than unsayable — the old
`product(carries, supports)` could not express one even to show it scoring badly. `C(n,2)` costs
nothing: pairings are derived from the authored ints at roughly 600 bytes and microseconds each.

What a body does with its turns is still visible — in its `note`, its axis values, and the
`niche` its seed sat under. It is just not a partition the model enforces.
