# Listonomicon 10.2 — verified rules and build math

Everything here was checked against the 10.2 manifest (706 Nexus mods, built 8 July 2026) or the
mod pages themselves. Where something is inferred rather than confirmed, it says so.

---

## Build math

### Ability modifiers

Modifiers change only on **even** scores. 20 and 21 are both +5; 22 is +6; 24 is +7.

**A single +1 is always wasted.** Any plan to raise an ability is two points or none. This kills
most "take a half-feat for the casting stat" advice.

Feat ability increases in Listo **bypass the hard cap of 20**. Feats Overhaul reimplements them
as stacking passives rather than ability selections:

> "any ability score increase you get from feats (except the actual ASI feat …) can now stack
> with other bonuses to increase your ability above 20"

The plain **ASI feat is the exception** and remains capped. **Resilient** can be taken multiple
times. **Enweaved** gives +2 to Int/Wis/Cha but caps at 22 and carries wild magic *and* magic
allergy — bad on a concentration build.

Non-feat sources that stack above 20 (per Listo docs): **Hag's Hair** (+1) and the **Tomes and
Manuals** mod (+1 each). The **Mirror of Loss** gives +2 to a chosen ability *plus* a separate +1
Charisma, per character — whether it exceeds 20 is **unconfirmed**.

### Feats

Granted at **class** level 3, 6, 9, 12, 15, 18. Fighters, Rogues and Mesmerists also get one at
class level 11. Mod: Universal Feat Every X Level(s) - MCM.

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
20 to 22.

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
  Alert as the intended way to reliably go first.
- **Combat Extender enemy HP** ≈ `Base × (1 + staticBoost + healthPerLevel × playerLevel)`.
  Bosses reach +310% and regular enemies +250% at level 20. Enemies scale with *player* level,
  so there is no out-levelling.
- **Level cap 20.** Most players reach 15+, completionists 18+; 20 needs the optional encounter
  content.
- **Attunement (And Rarity Limits):** each attuned item consumes an Action Resource, refunded on
  unequip. **No rest or combat restriction**, so re-attuning is free and unlimited — treat it as
  a per-fight loadout. Separate caps for total attuned and for Rare/Very Rare/Legendary counts.
  The MCM panel browses every item above Common rarity and previews any piece for 30 seconds.

---

## Feats that differ from vanilla

| Feat | Listo behaviour |
|---|---|
| **Alert** | Proficiency Bonus to initiative (not +5), plus Perception proficiency. The revert patch is **not** in the list |
| **Tough** | Vanilla +2 HP/level **plus** +1 Con and **+2 to Constitution saves** |
| **Durable** | +1 Con; in-combat regen of Prof Bonus + Con mod when starting a turn below 60% HP |
| **Mage Slayer** | **Advantage on saves against all spells**, spell damage reduced by Prof Bonus, enemies within 3m have disadvantage on concentration saves |
| **GWM / Sharpshooter** | Trade Prof Bonus on the attack roll for Prof Bonus on damage (not −5/+10) |
| **Tavern Brawler** | Significantly nerfed |
| **Moderately Armoured** | Medium Armour **and Shields**, +1 Str/Dex, +1 to saves with that ability |
| **Lightly Armoured** | Light armour only — **grants no shields** |
| **Medium Armour Master** | Flat +1 AC in medium armour and temp HP = Prof Bonus at combat start (no longer raises the Dex cap) |
| **Actor** | Expertise in Persuasion, Deception, Intimidation *and* Performance |
| **Skilled** | +1 to **any** ability |
| **Ritual Caster** | Listo patch: learn *all* ritual spells from the list |
| **Deadly Alacrity** | Listo patch **removes its +1 ability score** |
| **Arcane Acuity** | Capped at 3 stacks, 1 per trigger, combat-only, no pre-stacking — and triggers on **weapon attack rolls**. Invalidates most published Bard guides |
| **Arcanist / Experimental Alchemy** | **Removed in v9.0.3** despite still being in the docs |

**Essential Feats** adds: Fey Touched, Shadow Touched, Heaven Touched, Hell Touched, Meta Magic
Adept, Eldritch Adept, Telekinetic, Alchemist, Skilled Expert, Fighting Initiate, Light Armor
Master, Nimble Fingers, Thief's Apprentice, Deadly Alacrity, War Magic. Nearly all carry +1 to
Int/Wis/Cha; War Magic and Thief's Apprentice do not.

**Skeleton Crew** (Valkrana's, feat version) spawns a scaling random skeleton ally at the start
of **every combat**. The only feat that fixes small-party action economy.

---

## Classes and subclasses

New classes: **Artificer** (all four), **Mesmerist**, **Paragon** (Lionheart, Nighthawk, Prodigy,
Regent, Spellblade, Sword Saint), **Inquisitor**, **Bloodhunter**.

- **Paragon** is Charisma-based but has **no spell slots** — martial support, not a caster. Must
  be taken at level 1 or it loses heavy armour, skills and save proficiencies.
- **Mesmerist** is Charisma but a **half-caster** — caps at 5th-level spells. Its level 2 gives a
  bonus to Wisdom saves equal to the Charisma modifier, the best defensive feature on any Cha
  class here.
- **Inquisitor** is Wisdom-based (tagged Cleric and Ranger).

**v9.0.3 purged**: Whispers Bard; Frozen Sorcery and Spellfire Sorcery; the Sorcerer King,
Undead, Fathomless, Genie and Star Warlock patrons; Hedge Mage and Graviturgy Wizard; Blackguard;
Oath of Zeal/Phoenix/Storm.

**Surviving notable subclasses**: Bard — Eloquence, Dance, Tragedy. Warlock — **The Celestial**
only, plus Pact of the Shroud and 5R Pact of the Chain. Sorcerer — Aberrant Mind, **Favored
Soul**, Draconic (Expanded ancestries), Storm, Shadow, Arcane Chaos. Wizard — Book of Wizards,
Conjuration School Enhanced, School of Death, Hexcraft, Hierophant. Cleric — Circle of the Sea,
Darkness Domain, Death Domain, Cat's Cleric Changes. Druid — Book of Druids. Rogue — Book of
Rogues.

Charisma casters **with healing**: Bard, Celestial Warlock, Favored Soul Sorcerer.

---

## Races

**v9.0.3 purged nearly all race mods**, including Fantastical Multiverse. Remixed Subraces went
in v8; Satyr in v7.1.0.

Surviving additions: **Elemental Power (Genasi)** — Fire/Air/Earth/Water, each with Darkvision, a
resistance, and innate spells at 1/3/5. **Mordenkainen's Tome of Tieflings** — Baalzebul,
Dispater, Fierna, Glasya, Levistus, Mammon. **Full Roster of Gith (FROG)** + **Followers of
Zerthimon** — Githyanki and Githzerai as subraces. **Ghastly Ghouls** playable undead + Banshee
subrace. **Mordenkainen Presents - Lizardfolk**.

- **Sunlight Sensitivity - DND 5E** adds it back to **Drow and Duergar**. Avoid both.
- **Githzerai** (this version): Mage Hand, Unshackle Mind and Mental Discipline at 1; **Shield**
  at 3; **Misty Step** and Bestow Knowledge at 5; permanent Detect Thoughts and Insight
  advantage. **No ability bonuses**, and **no Medium armour or Martial weapon proficiency**.
- Races grant no ability score bonuses in BG3 — assign +2/+1 freely.

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

## Equipment

Caster gear in this list is **robe-shaped**; no mod adds medium armour with caster benefits.

- **Better End Game Caster Robe** — Robe of Archmage plus circlet, cloak, gloves, boots. Gilded
  Chest, Illusion section of the Sorcerous Vault (Act 3).
- **Robe of Vecna ReAwakened** — multi-act chain. Read the Compendium Maleficarum and **fail** the
  Wisdom save, then cast Extract Divine Undeath Essence on Ketheric's Apostle form (Act 2).
- **Psychic Armory** — upgradeable set; Sussur Bloom from the Arcane Tower basement.
- **JWL Discordant Instruments** — converts the Musical Instrument slot into a **Trinket slot**
  with 100+ items, distributed retroactively. Effectively a free extra magic item slot.
- **Phalar Aluve - Legendary** — music box in the Shadow-Cursed Lands (Act 2), second in a
  pickpocket-only part of the Circus (Act 3).
- **FoeBane** — Druid Grove questline (optional mod); scabbard in Jaheira's basement (Act 3).
- **Bladesong Garment** — female slim body types only (human/elf/half-elf/tiefling).
- **Random Equipment Loot** (optional) near-fully randomises distribution — voids all gear
  planning. Check whether it's on.

### Quest gates worth knowing

- **Potent Robe** (Charisma to cantrip damage) is **Alfira's reward and she must be alive**. Dark
  Urge kills her in a scripted scene; the only workaround is knocking her out in Act 1.
- **Hag's Hair** — a DC 20 check gets the hair *and* saves Mayrina; fail and you choose one.
- **Mirror of Loss** (Cloister of Sombre Embrace, Act 3) — needs the Night Orchid from behind a
  breakable wall in the Armoury past a passive check, then a Religion check.

---

## Other included mods worth remembering

- **Multiclass Preferred Casting Ability Fix** — class order no longer hijacks your Spellcasting
  Stat, so you can multiclass in any order.
- **Expansion** (mod 279) supplies level 13–20 progression; gallery tags include "Level 20 Cap".
- **Combat Extender** gives enemies mod spells, classes, feats and magic items.
- **Absolute Wrath** is optional; Listo's CX config already bakes in curated affixes, so enabling
  it double-dips.
- **Degreaser 2.0**, **Gear Revised** (rings/footwear/shields), **Elixirs Revised**, **Healing
  Potions Hardcore** all rebalance vanilla items — verify vanilla item numbers before relying on
  them.
