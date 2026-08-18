# Listonomicon 10.2 — verified rules and build math

**This file owns the arithmetic and the doctrine.** What *exists* in the list — which classes,
feats and items ship, and what each one does — lives in the compiled data files. Don't
duplicate them here, and don't answer "does X exist" from this file.

| Question | File |
|---|---|
| Does this class/subclass exist, and what does it do? | `data/listo-10.2-classes.md` → `data/classes/<class>.md` |
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

Granted at **class** level 3, 6, 9, 12, 13, 15, 18. Fighters and Rogues also get one at
class level 11.

Feat count = `floor(classA / 3) + floor(classB / 3)`, **plus 1 for each class taken to level 13
or higher**, **plus 1 for each of Fighter or Rogue taken to class level 11 or higher**. The
ceiling at character level N is `floor(N / 3)` plus those bonuses, reached whenever the two
remainders mod 3 sum to less than 3.

> **The level 13 grant is the one most plans miss, and it rewards lopsided splits.** Like the
> rest of the cadence it keys off *class* level, so a **17/3** build collects it and a **10/10**
> build does not. `(The class-level reading follows from how `FeatsUni` applies every other
> level in the list; a level-up screen would confirm it.)`

> **The bare formula undercounts Fighter and Rogue by one** at class level 11+. A pure Fighter 20
> gets **8 feats, not 6** — `floor(20/3) = 6`, plus the level 11 grant, plus the level 13 grant.
> Do not apply the formula without both corrections.
>
> **Fighter 11 is the highest-value single level in the list**: Improved Extra Attack *and* the
> off-cadence feat land together. Rogue 11 is the same shape — Reliable Talent, the 6th Sneak
> Attack die, and the feat.
>
> Note also that `Expansion` grants its own feats at 14/16/19, but `Universal Feat Every X
> Level(s)` **overrides** them — **confirmed**, `feats.BaseClassFeats: "None"` in the installed
> `MCM/Expansion/settings.json`. The class mod pages' feat tables are all wrong for Listo.

Consequences:

- **3-level dips are feat-neutral.** You get the dip class's own level 3 feat.
- **1- and 2-level dips cost a feat outright.**
- Place a dip as a contiguous 3-level block starting right after the main class crosses a
  multiple of 3, and feats still land on 3/6/9/12/13/15/18.

### Cheap dip breakpoints

**Rows are per-level increments, and a dip of size N gives you every row up to N.** A Fighter 2
dip is Fighter 1 *plus* Fighter 2 — Str/Con saves, all armour, shields, Fighting Style, Second
Wind and Action Surge.

Saving throw proficiencies are the ones that force the dip to be your **level 1 class** — they are
unobtainable otherwise, and a respec silently loses them.

| Dip | Buys |
|---|---|
| **Artificer 1** | **Int + Con saves**, medium armour, shields, Sleight of Hand. The multiclass node grants no saves — must be first |
| **Fighter 1** | **Str + Con saves**, **all armour including heavy**, shields, Fighting Style, Second Wind — **only as the level 1 class**. The *multiclass* node grants **light + medium + shields only, no heavy armour and no saves** |
| **Fighter 2** | Action Surge — a third Action alongside Lone Wolf's second |
| **Fighter 11** | Improved Extra Attack **and an off-cadence feat** — the highest-value single level in the list |
| **Warlock 1** | **Wis + Cha saves**, Eldritch Blast, pact slot, patron features. Note the multiclass node grants the *same* proficiencies as level 1, so unlike Fighter 1 or Artificer 1 it **frees no armour feat** |
| **Warlock 2** | **Agonizing Blast** — beams scale on *character* level, so this is a full damage engine for two levels (at 1d8/beam in Listo, not 1d10) |
| **Warlock 3** | Pact boon (Chain = a familiar), 2nd-level pact slots on a short-rest clock, **and a feat** — the strongest action-economy purchase in the list for a duo. Chain familiars get the **Help** action, Magic Resistance and doubled HP from `18881` |
| **Warlock 5** | Pact slots to 3rd level, third invocation |
| **Cleric 1** | **Wis + Cha saves**, a domain, armour depending on domain |
| **Sorcerer 2** | Font of Magic — convert slots to sorcery points and back |
| **Sorcerer 3** | Metamagic; Twinned and Quickened are the ones worth levels |
| **Bard 3** | A College, Expertise ×2, three bonus proficiencies |
| **Rogue 3** | A subclass from Book of Rogues, Expertise, Sneak Attack |
| **Ranger 3 (Beast Master)** | A full animal companion — **`Expansion` moves Companion's Bond from level 5 to 3**, and adds a Panther with your Proficiency Bonus, all-save proficiency and ASIs. A third body for a feat-neutral dip |
| **Paragon 1** | Heavy armour, shields, martial weapons, light/medium armour, simple weapons, two skills, **Con + Cha saves**. A late dip loses **only Skills, Saving Throws and Heavy Armour** — shields, martial weapons, medium armour and all class features still arrive |
| **Paragon 3 (Spellblade)** | Charisma-based melee weapon attacks (Scholar's Armament: CHA for attack *and* damage). A **feat-neutral mid-run dip** for any Charisma character, Hexblade-shaped |

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
| **Paragon 20 capstone** | **+4 to STR/CHA or DEX/CHA** | **caps at 25** — requires pure Paragon 20 |

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
character **5, 10 and 17** — BG3 diverges from tabletop, and the 3rd beam lands at **10, not 11**.
The 4th beam comes from `Expansion` (`279`). This holds regardless of how few Warlock levels you
have, so two Warlock levels still buy a fully-scaling damage engine.

**But the beams are weaker here: Listo nerfed Eldritch Blast to 1d8 per beam in v10.0, down from
1d10**, and Repelling Blast now allows a Strength save. Any damage math taken from outside Listo
is overstated. See `data/classes/warlock.md`.

### Respec

Withers' fee is unchanged by the 4× merchant multiplier. A rebuild **re-derives everything from
class levels** — nothing banks, so you cannot take a level for a feat and then drop back.

It also **re-picks your first class**, and saving throw proficiencies come from the level 1 class
only. This is the single easiest thing to lose silently.

**Trap:** starting as an Oathbreaker Paladin blocks normal respec entirely.

---

## Economy and difficulty

- **Long rest: 120 camp supplies**, rising with camp population and act. Resolved multipliers
  (`Dynamic Camp Supply Cost`): active party member **1.0**, idle follower **0.30**, hireling
  and pet **0.25**, children 0.45; Aylin, Mizora, Tara and the Oathbreaker Knight are overridden
  to **0**. Act multipliers 1.075 / 1.175 / 1.15, rounded to the nearest ten. Camp size drives
  the cost, but an idle body costs under a third of an active one — **recruiting companions is
  not the trap the older note made it**.
- **Short rests are unchanged** — two per long rest. Listo's own docs advise leaning on them.
- **Merchants: 4× buy, ¼ sell.** Withers is a merchant with 50,000 gold that resets each
  conversation.
- **Initiative: d10 + Dex + bonuses** — `InitiativeDie: 10` confirmed in the installed config.
  The docs name Alert as the intended way to reliably go first — and Alert is nerfed to
  Proficiency Bonus here.
- **Surprise:** `Sensible Ambushing` gives a flat **Wisdom save, DC 15**, applying to both
  sides. One more reason Wisdom outranks the other saves.
- **Combat Extender enemy HP** = `Base × (1 + staticBoost + healthPerLevel × playerLevel)`.
  Live values: bosses `0.10 + 0.08/level` → **+170% at 20**; enemies `0.06 + 0.06/level` →
  **+126% at 20**; **allies `0.12 + 0.011/level` → +34%**. Enemies scale with *player* level,
  so there is no out-levelling. The older "+310%/+250%" figure came from a superseded config.
- **Combat Extender's other live scaling:** bosses +1 AC per 9 levels and +1 spell save DC per
  7; enemies +1 AC per 11 and +1 DC per 11; **allies +1 AC static and +1 per 4 levels**;
  attack/save rolls +1 per 20 levels for everyone; **no extra actions and no flat damage boost
  in the normal config**. Enemy lethality comes from kit, not from a damage multiplier.
- **CX is configured by file, not by MCM** — `Use_MCM_Settings` is `false`. Difficulty changes
  are a rename of `CombatExtender.json` to the EASY or HARD variant.
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
  loadout, not a permanent commitment. **Resolved caps: 5 attuned total; 3 Legendary, 5
  VeryRare, 6 Rare, 13 Uncommon** — identical across all five difficulty entries, so difficulty
  does not change them. Items at **Legendary or above auto-require attunement**. Plan against
  five attuned pieces with at most three Legendary. A `relaxed config.json` (6 total, 4
  Legendary) ships but is not live. Full mechanics in `data/listo-10.2-equipment.md`.

---

## Lone Wolf

**Not bundled.** Removed with the note *"Smaller parties are not the intended Listo experience."*
Hand-add **Lone Wolf Feat - SE**; the author recommends load order "somewhere in the middle,
below MCM."

> **In the shipped 10.2 profile the mod is present but `-` disabled**, at the very top of
> `modlist.txt` — enabling it in MO2 is a manual step. It is also the *only* mod in the profile
> with no `BG3MCM/Profiles/Default` entry, so its own defaults stand unless the player edits MCM
> in game.
>
> **For this run it is enabled, in non-feat mode** — the MCM feat requirement is off, so Lone
> Wolf is **always on from level 1 and costs no feat**. Every feat in the cadence below is free
> for the build.

Buffs: extra Action, Bonus Action and Reaction; +30% max HP; **halved damage from all sources**;
doubled carry; and +4 to two abilities with save proficiency in both.

- MCM (v2.3.0.0+) **disables the feat requirement** — this run uses that mode, so all buffs
  apply from level 1 with no feat spent.
- **Still unverified:** whether the +4 caps at 20. Visible on the sheet at character creation —
  check there.
- **Sit This One Out 2 ships disabled** (`-OPTIONAL_Sit This One Out 2` in `modlist.txt`) and is
  **enabled for this run**. Lone Wolf has an explicit exception for it: companions toggled to
  sit out **don't count toward the party cap of 2**. This solves companion quests.

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

**The catalogue is `data/listo-10.2-classes.md` (index) and `data/classes/<class>.md` (detail)** —
156 subclasses across 17 classes, each confirmed against the manifest. Enumerate from there, not
from memory.

Only the facts that feed the tables above are repeated here:

- **Paragon** has **no spell slots** — martial support, not a caster (Spellblade gets cantrips and
  cantrip-like weapon attacks; Nighthawk has one 1/long-rest spell). It is **Charisma-flavoured
  but MAD**: outside Spellblade, weapon attacks still use STR/DEX and Charisma only feeds riders.
  Only **Spellblade** is genuinely single-stat. Taking it at level 1 buys skills, saving throws
  and heavy armour; a **later dip still grants shields, martial weapons, medium armour and all
  class features**. Its **level 20 capstone gives +4 to two abilities capping at 25**, reachable
  only by pure Paragon 20. See `data/classes/paragon.md`.
- **Mesmerist** is a Charisma **half-caster** drawing from the **Bard** list, gaining a new spell
  **every level**. It is on the **standard** cadence — the docs claim it gets the level 11 feat,
  but the installed config gates that behind `enableAdvancedSettings: false`, so it does not.
  The mod's own page says 4/8/12/16/19; Listo's `Universal Feat Every X Level(s)` overrides that
  too, so plan against **3/6/9/12/13/15/18**. Its **max spell level is `(unverified)`** — the mod page never
  states it; 5th is the natural reading of "half-caster" but is not confirmed.
  Its level 2 **Towering Ego** adds the **Charisma modifier to Wisdom saves** (and half to
  Intelligence). Three qualifiers the older notes missed: it is **self-only**, it scales with
  **Charisma rather than class level — so a 2-level dip gets the full effect** — and it **switches
  off entirely while you are under any harmful mind-affecting condition**, making it purely
  preventative. See `data/classes/mesmerist.md`.
- **Mesmerist grants both Dex and Cha saves at level 1** — the two a Charisma build most wants —
  so Lone Wolf's +4 should go on **Constitution + Wisdom**, yielding four proficiencies covering
  the entire top of the save-value ordering. It escapes the Charisma trap rather than falling
  into it.
- **Artificer 1** and **Paragon 1** grant nothing from their multiclass nodes — both must be the
  level 1 class to be worth taking at all.
- **Inquisitor** is Wisdom-based (tagged Cleric and Ranger).
- Charisma casters **with healing**: Bard, Celestial Warlock, Favored Soul Sorcerer.
- **Multiclass Preferred Casting Ability Fix** is in the list — class order no longer hijacks
  your Spellcasting Stat, so you can multiclass in any order.
- **Expansion** (mod 279) supplies level 13–20 progression.

The v9.0.3 purge list and the surviving-subclass catalogue both live in
`data/listo-10.2-classes.md`. **Do not plan from a remembered subclass list** — the old summary
here was wrong in three ways: it missed `(DTO) Otherworldly Archetypes` entirely (12 subclasses,
one per vanilla class), it listed "Arcane Chaos" as a Sorcerer subclass when it is a level-6
feature of vanilla Wild Magic, and it named The Celestial as the only surviving added Warlock
patron when The Psyker also survives.

**⚠ Inquisitor is probably broken past level 2** in 10.2 — Listo pulled the version *before* the
fix for exactly that bug, and no patch is in the manifest. See the index.
