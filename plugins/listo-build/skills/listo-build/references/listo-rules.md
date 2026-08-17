# Listonomicon 10.2 — verified rules and build math

**This file owns the arithmetic and the doctrine.** What *exists* in the list — which classes,
feats and items ship, and what each one does — lives in the compiled data files. Don't
duplicate them here, and don't answer "does X exist" from this file.

| Question | File |
|---|---|
| Does this class/subclass exist, and what does it do? | the Classes section **below**, then `data/listo-10.2-mods.tsv` |
| Does this race exist, and what does it grant? | `data/listo-10.2-races.md` |
| Does this feat exist, and what does it do here? | `data/listo-10.2-feats.md` |
| Does this item exist, where is it, what does it do? | `data/listo-10.2-equipment.md` |
| **How do I count feats, dips, saves and stat targets?** | **this file** |
| How do I search the snapshot / refresh it? | `references/research-recipes.md` |

Everything below was checked against the 10.2 manifest (706 Nexus mods, built 8 July 2026) or
the mod pages themselves. Where something is inferred rather than confirmed, it says so.

---

## Build math

### Ability modifiers

Modifiers change only on **even** scores. 20 and 21 are both +5; 22 is +6; 24 is +7.

**A single +1 is always wasted.** Any plan to raise an ability is two points or none. This kills
most "take a half-feat for the casting stat" advice.

Feat ability increases in Listo **bypass the hard cap of 20** — Feats Overhaul reimplements them
as stacking passives rather than ability selections. The plain **ASI feat is the exception** and
remains capped.

> **Unresolved:** whether the uncap reaches **Essential Feats'** half-feats, or only the vanilla
> feats Feats Overhaul itself rebalances. See the "ability-score cap" section of
> `data/listo-10.2-feats.md` — Listo pulled the base Essential Feats file, not the ASI optional,
> and the patch mod that would extend the uncap is not in the list. **Check a sheet in-game
> before planning a build that needs an Essential Feats half-feat to cross 20.**

Non-feat sources that stack above 20: **Hag's Hair** (+1) and the **Tomes and Manuals** mod
(+1 each). The **Mirror of Loss** gives +2 to a chosen ability *plus* a separate +1 Charisma, per
character — whether it exceeds 20 is **unconfirmed**. Acquisition gates for all three are in
`data/listo-10.2-equipment.md`.

### Feat cadence and count

Granted at **class** level 3, 6, 9, 12, 15, 18. Fighters, Rogues and Mesmerists also get one at
class level 11.

Feat count = `floor(classA / 3) + floor(classB / 3)`. The ceiling at character level N is
`floor(N / 3)`, reached whenever the two remainders mod 3 sum to less than 3.

Consequences:

- **3-level dips are feat-neutral.** You get the dip class's own level 3 feat.
- **1- and 2-level dips cost a feat outright.**
- Place a dip as a contiguous 3-level block starting right after the main class crosses a
  multiple of 3, and feats still land on 3/6/9/12/15/18.

### Cheap dip breakpoints

**Rows are per-level increments, and a dip of size N gives you every row up to N.** A Fighter 2
dip is Fighter 1 *plus* Fighter 2 — Str/Con saves, all armour, shields, Fighting Style, Second
Wind and Action Surge.

Saving throw proficiencies are the ones that force the dip to be your **level 1 class** — they are
unobtainable otherwise, and a respec silently loses them.

| Dip | Buys |
|---|---|
| **Artificer 1** | **Int + Con saves**, medium armour, shields, Sleight of Hand. The multiclass node grants no saves — must be first |
| **Fighter 1** | **Str + Con saves**, all armour, shields, Fighting Style, Second Wind |
| **Fighter 2** | Action Surge — a third Action alongside Lone Wolf's second |
| **Warlock 1** | **Wis + Cha saves**, Eldritch Blast, pact slot, patron features |
| **Warlock 2** | **Agonizing Blast** — beams scale on *character* level, so this is a full damage engine for two levels |
| **Warlock 3** | Pact boon (Chain = a familiar), 2nd-level pact slots on a short-rest clock |
| **Warlock 5** | Pact slots to 3rd level, third invocation |
| **Cleric 1** | **Wis + Cha saves**, a domain, armour depending on domain |
| **Sorcerer 2** | Font of Magic — convert slots to sorcery points and back |
| **Sorcerer 3** | Metamagic; Twinned and Quickened are the ones worth levels |
| **Bard 3** | A College, Expertise ×2, three bonus proficiencies |
| **Rogue 3** | A subclass from Book of Rogues, Expertise, Sneak Attack |
| **Paragon 1** | Heavy armour, shields, martial weapons, **Con + Cha saves** — must be first or it grants none of it |

A **fighting style** can also be bought without a dip — Weapon Master and Fighting Initiate both
grant one, and the list adds UA styles. Check `data/listo-10.2-feats.md` before spending levels
on a style a feat would supply.

### Level 1 saving throw proficiencies

Only your **first** class grants these. Pick it deliberately, and re-pick it on every respec.

| Str | Dex | Con | Int | Wis | Cha |
|---|---|---|---|---|---|
| Barbarian, Fighter, Monk, Ranger | Bard, Monk, Ranger, Rogue, Mesmerist | Barbarian, Fighter, Sorcerer, Artificer, Paragon | Druid, Rogue, Wizard, Artificer | Cleric, Druid, Paladin, Warlock, Wizard | Bard, Cleric, Paladin, Sorcerer, Warlock, Paragon, Mesmerist |

### Lone Wolf's +4 and the first class are one decision

Solve these **jointly**, by enumerating combinations. Deciding the +4 on stat grounds and then
picking a class to fit produces worse builds than considering them together, because both sides
carry more than they appear to.

**Lone Wolf's +4, per ability chosen:**
- Up to **+2 modifier**, and only if the final score lands even — odd wastes half of it
- **Save proficiency** in that ability

**The level 1 class, which is the only class that grants any of this:**
- **Two save proficiencies** — unobtainable later, lost silently on respec
- **Armour, shield and weapon proficiencies** — these can *return a feat*. Fighter 1 or Artificer 1
  supply shields and medium armour, making Moderately Armoured unnecessary
- **Starting skills**, sometimes more than the same class's multiclass node grants
- **Level 1 class features and starting equipment**

**Primary stat targets: 20 by level 6, 22 by level 18.** Those thresholds — +5 then +6 — are the
constraint. How you reach them is open; failing to reach them is not. Primary modifier is spell
save DC, attack rolls and per-hit damage, so never finish a plan below the line.

Sources, and their ceilings:

| Source | Amount | Cap |
|---|---|---|
| Point buy + floating racial | 15 + 2 = **17** at creation | — |
| **Lone Wolf +4** | +4 | stops at 20 |
| ASI feat | +2 | stops at 20 |
| Half-feats (Feats Overhaul) | +1 each | **bypass 20** |
| Mirror of Loss | +2 chosen, +1 Cha | Act 3 |
| Hag's Hair | +1 | Act 1, one per run |
| Tomes and Manuals | +1 each | — |

**Lone Wolf's +4 is the cheapest route to 20, and the only one available at level 1.** Put it on
the primary and you hit 20 immediately with every feat still free.

Reaching 20 without it costs roughly **two feats** — 17 at creation, then the ASI feat (+2) at
level 3 and a half-feat (+1) at 6 — and leaves the primary at +3 through the whole of Act 1. That
is a real price, but it is a *price*, not an impossibility. If four distinct saves plus a better
first-class package is worth two feats and a weak Act 1, the +4 is free to go elsewhere.

Above 20 needs **half-feats or items** — the plain ASI feat is capped, so it cannot take you from
20 to 22. **Enweaved** is the only +2 half-feat in the list and caps at 22; its wild-magic
downside is described in `data/listo-10.2-feats.md`.

Corollary for point buy: if Lone Wolf is taking the primary, buy it to exactly **16** after the
racial bonus. 17 wastes a point against the cap; less than 16 fails to reach it.

**Respec changes when, not whether.** Stats are re-picked on every rebuild, so the second +4, the
point buy and the feats can all be re-cut as items land — but every intermediate build still has
to clear the thresholds.

**Save value ordering**, roughly, for weighing coverage:

> Wisdom (Hold, Dominate, Fear, Hypnotic Pattern) > Constitution (concentration) ≈ Dexterity (AoE)
> > Charisma (Banishment) > Strength > Intelligence

**Ceiling:** four distinct saves, two from each source, and only if the pairs are disjoint.

**The Charisma trap:** seven classes grant Charisma at level 1 (Bard, Cleric, Paladin, Sorcerer,
Warlock, Paragon, Mesmerist). Give Lone Wolf's +4 to Charisma alongside any of them and one grant
is wasted. Escaping that means either a non-Charisma first class — costing a caster level and
breaking the multiple-of-three feat rule — or letting items carry Charisma instead.

**Worked comparison shape** (a Charisma caster, to show the method rather than the answer):

| First class | Lone Wolf +4 | Distinct saves | Also gets |
|---|---|---|---|
| Warlock 1 | Cha + Con | Wis, Cha, Con — 3 | Cha at 20 from level 1, every feat free |
| Warlock 1 | Con + Dex | Wis, Cha, Con, Dex — **4** | Cha needs ~2 feats to hit 20 by level 6, and sits at +3 through Act 1 |
| Fighter 1 | Cha + Wis | Str, Con, Cha, Wis — **4** | Shields and all armour (frees a feat), Fighting Style, Second Wind — but a caster level and the feat cadence |
| Artificer 1 | Cha + Wis | Con, Int, Cha, Wis — **4** | Medium armour and shields (frees a feat), Int/Con saves |

Score each on modifier points gained, number *and quality* of saves, feats freed against feats
spent, caster levels lost, and what the class features add. There is no default answer.

### Spell progression

Full casters unlock a new tier at odd class levels (1, 3, 5, 7, 9, 11, 13, 15, 17). A dip
therefore costs a spell tier at odd character levels and nothing at even ones.

**Cantrip scaling keys off character level, not class level.** Eldritch Blast gains beams at
character 5, 11 and 17 regardless of how few Warlock levels you have — so two Warlock levels buy
a fully-scaling damage engine.

### Respec

Withers' fee is unchanged by the 4× merchant multiplier. A rebuild **re-derives everything from
class levels** — nothing banks, so you cannot take a level for a feat and then drop back.

It also **re-picks your first class**, and saving throw proficiencies come from the level 1 class
only. This is the single easiest thing to lose silently.

**Trap:** starting as an Oathbreaker Paladin blocks normal respec entirely.

---

## Economy and difficulty

- **Long rest: 120 camp supplies**, rising with camp population and act. Supernatural members
  (Aylin, Withers) cost nothing; Astarion is minimal; hirelings very little. Camp size, not
  active party size, drives the cost — so a small party pays full price for half the refuel.
- **Short rests are unchanged** — two per long rest. Listo's own docs advise leaning on them.
- **Merchants: 4× buy, ¼ sell.** Withers is a merchant with 50,000 gold that resets each
  conversation.
- **Initiative: d10 + Dex + bonuses** (Initiative Variants), MCM-configurable. The docs name
  Alert as the intended way to reliably go first — and Alert is nerfed to Proficiency Bonus here.
- **Combat Extender enemy HP** ≈ `Base × (1 + staticBoost + healthPerLevel × playerLevel)`.
  Bosses reach +310% and regular enemies +250% at level 20. Enemies scale with *player* level,
  so there is no out-levelling.
- **Level cap 20.** Most players reach 15+, completionists 18+; 20 needs the optional encounter
  content.
- **Combat Extender** gives enemies mod spells, classes, feats and magic items — the reason
  enemy capability tracks the list rather than vanilla.
- **Absolute Wrath** is optional; Listo's CX config already bakes in curated affixes, so enabling
  it double-dips.
- **Illithid Powers Overhaul 2** is optional and strong; Illithid powers become very powerful in
  Act 3 if the astral tadpole is used.
- **Attunement:** each attuned item consumes an Action Resource, refunded on unequip, with **no
  rest or combat restriction** — so re-attuning is free and unlimited. Treat it as a per-fight
  loadout, not a permanent commitment. Separate caps for total attuned and for
  Rare/VeryRare/Legendary counts, all **MCM-configurable per difficulty**. Because the caps are
  a config value, **ask the player what theirs are set to** before planning a kit. Full
  mechanics in `data/listo-10.2-equipment.md`.

---

## Lone Wolf

**Not bundled.** Removed with the note *"Smaller parties are not the intended Listo experience."*
Hand-add **Lone Wolf Feat - SE**; the author recommends load order "somewhere in the middle,
below MCM."

Buffs: extra Action, Bonus Action and Reaction; +30% max HP; **halved damage from all sources**;
doubled carry; and +4 to two abilities with save proficiency in both.

- MCM (v2.3.0.0+) can **disable the feat requirement**, making it always-on from level 1.
- **Unverified:** whether the ability bonus and save proficiencies still apply in that mode, and
  whether the +4 caps at 20. Both are visible on the sheet at character creation — check there.
- **Sit This One Out 2 is bundled**, and Lone Wolf has an explicit exception for it: companions
  toggled to sit out **don't count toward the party cap of 2**. This solves companion quests.

---

## Races — the one rule that affects the math

**Races grant no ability score bonuses in BG3.** The +2/+1 is assigned freely at creation,
independent of race, so a race never constrains the stat spread — pick it for features.

The catalogue is in **`data/listo-10.2-races.md`**. Two entries change build math enough to flag
here:

- **Ghastly Ghouls (playable undead)** uses the vanilla `undead` tag: **most healing spells do
  not work on you**, you are **vulnerable to Radiant**, and **Turn Undead affects you**. In a duo
  this needs an explicit recovery plan before it is viable.
- **Githzerai** grants **no Medium armour or Martial weapon proficiency**, unlike vanilla
  Githyanki — so it does not return a feat the way Githyanki might.

---

## Classes and subclasses

> **No compiled classes file exists yet** — this section is the reference. Unlike races, feats
> and equipment, classes have not been compiled into a `data/` file, so this list is
> summary-level. **Verify any specific subclass against `data/listo-10.2-mods.tsv` before
> recommending it**, and enumerate from the mods index rather than from this section when
> presenting options.

New classes: **Artificer** (all four subclasses), **Mesmerist**, **Paragon** (Lionheart,
Nighthawk, Prodigy, Regent, Spellblade, Sword Saint), **Inquisitor**, **Bloodhunter** (mod.io,
so it does not appear in the Nexus-only TSV).

Facts that feed the tables above:

- **Paragon** is Charisma-based but has **no spell slots** — martial support, not a caster. Must
  be taken at level 1 or it loses heavy armour, skills and save proficiencies.
- **Mesmerist** is Charisma but a **half-caster** — caps at 5th-level spells. It is also one of
  the three classes on the **seven-feat** cadence. Its level 2 gives a bonus to Wisdom saves
  equal to the Charisma modifier, the best defensive feature on any Cha class here.
- **Artificer 1** and **Paragon 1** grant nothing from their multiclass nodes — both must be the
  level 1 class to be worth taking at all.
- **Inquisitor** is Wisdom-based (tagged Cleric and Ranger).
- Charisma casters **with healing**: Bard, Celestial Warlock, Favored Soul Sorcerer.
- **Multiclass Preferred Casting Ability Fix** is in the list — class order no longer hijacks
  your Spellcasting Stat, so you can multiclass in any order.
- **Expansion** (mod 279) supplies level 13–20 progression.

**v9.0.3 purged**: Whispers Bard; Frozen Sorcery and Spellfire Sorcery; the Sorcerer King,
Undead, Fathomless, Genie and Star Warlock patrons; Hedge Mage and Graviturgy Wizard; Blackguard;
Oath of Zeal/Phoenix/Storm.

**Surviving notable subclasses**: Bard — Eloquence, Dance, Tragedy. Warlock — **The Celestial**
only, plus Pact of the Shroud and 5R Pact of the Chain. Sorcerer — Aberrant Mind, **Favored
Soul**, Draconic (Expanded ancestries), Storm, Shadow, Arcane Chaos. Wizard — Book of Wizards,
Conjuration School Enhanced, School of Death, Hexcraft, Hierophant. Cleric — Circle of the Sea,
Darkness Domain, Death Domain, Cat's Cleric Changes. Druid — Book of Druids. Rogue — Book of
Rogues.
