# Listonomicon 10.2 — spells and spell-list access

Compiled from two sources, joined:

- **The installed paks** — every modded number was read out of `Public/*/Lists/SpellLists.lsx`,
  `Progressions.lsx` and `Feats.lsx` inside the LSPK archives under the Mod Organizer install,
  with enabled/disabled state taken from `profiles/Listonomicon/modlist.txt`.
- **bg3.wiki** — the base-game lists, which are **not** available from the mods root (Larian's
  `Shared.pak` is not under it). `List of <class> spells` on bg3.wiki is the vanilla baseline the
  mods merge into.

The join cross-validates: vanilla Wizard has **16** cantrips, the paks add **23**, and the
re-declared Listo list holds exactly **39**. Every cantrip pool below reconciles the same way.
See `references/research-recipes.md` and `scripts/lspk.py`.

This file answers one question: **what spells can a given character actually reach, and by which
route.** It does not document what each spell does — for that, read the spell in game or on
bg3.wiki.

---

## Why this matters more here than in vanilla

Listo installs **eight spell packs** whose contents are merged directly into the vanilla class
lists. **445 distinct spells** are injected into pre-existing class lists this way, on top of
everything the base game and the class mods already carry. The practical consequences:

- A **full caster's pick list roughly doubles or triples.** At spell level 6 the Wizard chooses
  from **215** spells against vanilla's 102; by level 9 it is **260**. The Sorcerer goes 78 → 165
  → **192**.
- **Magical Secrets is the single largest access grant in the modlist.** The Bard's level-18
  tranche picks from a **415-spell** pool.
- **Cantrip lists roughly doubled or better.** Wizard 16 → **39**, Sorcerer 15 → **42**,
  Warlock 10 → **34**, Druid 6 → **26**.
- The **Magic Initiate feats read from those same expanded lists**, so a one-feat dip into a
  spell list is worth far more than the vanilla feat suggests.
- **Which casters benefit is not the obvious answer.** *Prepared* casters (Cleric, Druid, Paladin)
  receive their whole list automatically, so every spell added is a free capability with no
  opportunity cost — the Druid's list slightly more than doubles, 56 → **117**. *Known* casters
  (Sorcerer, Bard, Ranger, Warlock) still pick a fixed number, so a bigger list buys **better
  picks, not more of them**. Only the **Wizard** converts list growth directly into breadth,
  because scroll transcription has no cap.

---

## How spell access is wired (read this before trusting any list)

**Merge, not replace.** Mods extend a vanilla list by declaring a `SpellList` node with a
`MergedInto` attribute pointing at the vanilla list's UUID. The game unions everything that names
the same target. A second, older idiom is re-declaring a node with the *same UUID* and a leading
`;` in the `Spells` string — also additive. Both are in use here.

**Load order matters only for empty overrides.** Because merges are additive, load order rarely
decides anything — with one live exception, below.

**⚠ `Valkrana's Spellbook Limited Lists` is enabled and it wins.** In `modlist.txt` the Limited
Lists variant sits *above* `Valkranas Spellbook` (higher MO2 priority = loaded later), and it
declares **139 zero-spell lists** that blank Valkrana's merges out of **Cleric, Druid, Paladin,
Ranger, Mesmerist and Artificer**. The 17 Valkrana necromancy spells therefore reach **Wizard,
Sorcerer, Warlock, Bard, Eldritch Knight and Arcane Trickster** normally, and reach Cleric/Druid
only through the two dedicated lists the Limited variant keeps: **Death domain Cleric** and
**Circle of Spores Druid**. Do not plan a Valkrana spell on a Life Cleric.

**⚠ `OPTIONAL_Spelljammer 5e @` is DISABLED.** It ships in the install but is unticked in the
profile, so Air Bubble and the rest of its scroll-list entries are **not** available. Every count
in this file already excludes it. (`OPTIONAL_Valkranas Skeletal Challenge +` is likewise off.)

**Spell List Customization Framework (`21017`) is installed with exactly one rule active.**
`SE_CONFIG/MikeshardmindSpellListFramework/user_settings.json` sets
`active_user_rules: ["examples.BladeCantrips"]`. That rule reads:

> **BladeCantrips** — `has_any: Booming Blade, Sparking Blade, Green-Flame Blade → add: all of
> them`, then `prefer` collapses the duplicate implementations down to one.

So **any class whose cantrip list contains one blade cantrip gets all three.** That is Wizard,
Sorcerer, Warlock, and anything that borrows those lists (Magic Initiate, Pact of the Tome,
Hierophant). A second rulegroup, **MindSliver** (which would collapse the three competing Mind
Sliver implementations), is present in the rules file but **not in `active_user_rules` — it is
off**.

**⚠ Duplicate spells are real and visible.** Several spells ship in two implementations that both
land in the same list — `Foresight`, `Feeblemind`, `Mind Blank`, `Regenerate`, `Power Word: Kill`
and `Dominate Monster` each appear twice in the Bard/Sorcerer/Wizard level-9 pools (one entry from
`5e Spells`, one from `AdvancedTabletopSpells`, the latter usually prefixed **ATT** in the tooltip).
They are not identical — check the tooltip numbers before picking, and expect the pick lists to
look padded.

---

## The spell packs, and what each one is for

| Mod | ID | Role | Distinct spells it places into class lists |
|---|---|---|---|
| **`5e Spells`** | `125` | The backbone. Implements the tabletop spells BG3 omitted, and merges them into every vanilla class list at every level | **287** |
| **`ListoPFSpells`** (PF2e Spells Updated and Reduced) | `15367` | Re-declares the **level 7–9 pick lists** and Magical Secrets with a much larger roster | 352 placed (33 its own) |
| **`Spells Extra - DND 5E Library`** | `11291` | Library of lists for *other* mods to consume — see the warning below | 283 placed (41 its own) |
| **`Homebrew Spells`** | `473` | 38 new elemental/force spells and cantrips, merged broadly into arcane lists | **38** |
| **`AdvancedTabletopSpells`** | `14429` | The **level 7–9 tabletop capstones** — Wish, Time Stop, Shapechange, Meteor Swarm, Gate, Prismatic Wall, Weird, Psychic Scream | **45** |
| **`Valkrana's Spellbook`** | `1258` | 17 necromancy spells — **restricted by the Limited Lists variant, see above** | 17 |
| **`Spells of Exandria`** | `18441` | Dunamancy — Gift of Alacrity, Fortune's Favour, Magnify Gravity, Gravity Sinkhole, Temporal Shunt, Tether Essence, Reality Break, Dark Star | **14** |
| **`[ModIO] Mystra's Homebrew Spells`** | mod.io | Small utility/weapon-conjuration set — Ghost Walk, Summon Moonblade, Force Weapon, Illusory Weapon, Moonflare, Macabre Explosion | **14** |
| **`Dispel Magic`** | `23` in list | Injects Dispel Magic and the level-3 utility block into **every** level-3 list (Cleric, Paladin, Druid, Bard, Sorcerer, Wizard, all Warlock patrons) | 261 placed |
| **`Life Drain Spell`** | `18702` | Larloch's Minor Drain, merged into every arcane cantrip and Warlock list | 1 |
| **`Telekinetic Thrust`** | `15423` | One cantrip, but it **re-declares the whole Wizard / Sorcerer / Warlock cantrip lists** — which is why those three are the only cantrip pools this file can state as absolute totals | 1 |
| **`Listo Master Spells Patch`** | Listo-authored | Highest-priority patch. Owns the **Artificer** lists outright and carries targeted fixes (Hypnotic Gaze, Holy Rebuke, Motivational Speech) | 183 placed |
| **`Conjure Animals and Summon Beast Spells`** | `13458` | Adds the summon spells to Druid/Ranger/Bard-Secrets lists | 2 |
| **`Hierophant - 5e Spells Compatibility`** | `7859` optional file | Feeds the Hierophant's combined Wizard+Cleric list | **81** |

> **⚠ `Spells Extra - DND 5E Library` is a library, not a feature.** It ships 214 spell lists with
> names like *"Cleric Knowledge Domain Enhanced Wizard SLevel 1"*, *"Cleric War Domain Enhanced
> Paladin SLevel 1"*, *"Monk Way of Shadow Enhanced SLevel 5"* and the eight *"Spell Savant
> Enhanced"* school lists. **None of them is referenced by any installed progression.** They exist
> for dependent mods to point at. In 10.2 the only ones actually wired are the **Hierophant**
> lists. Do not promise a player that Knowledge Domain grants wizard spells — it does not.
> The same applies to Community Library's `Bard Magical Secrets (5e)` and `Warlock OneDnD` lists:
> defined, unreferenced.

---

## Cantrip pools

Vanilla counts from bg3.wiki; totals measured from the paks (`Telekinetic Thrust` re-declares the
three arcane lists in full and `Listo Master Spells Patch` re-declares the Druid's, so these are
absolute).

| List | Vanilla | Added | Total | Notable additions |
|---|---|---|---|---|
| **Wizard** | 16 | +23 | **39** | Green-Flame Blade, Sparking Blade (Booming Blade is already vanilla), Mind Sliver, Sword Burst, Lightning Lure, Frostbite, Infestation, Control Flames, Mold Earth, Shape Water, Gust, Sapping Sting, Larloch's Minor Drain, TK Thrust, Prestidigitation, Thunderclap, Ice Weapon, Illusionary Dart, Rock Slam, Shadow Lash, Water Bullet, Electric Arc |
| **Sorcerer** | 15 | +27 | **42** | The same arcane set plus Force Bolt, Toll the Dead, Fists of Fire, Stone Forming, Burn, Freeze, Impact, Decaying Touch |
| **Warlock** | 10 | +24 | **34** | The full blade trio, Mind Sliver, Magic Stone, Shadow Lash, Sword Burst, Lightning Lure, Prestidigitation, Shape Water, Bursting Sinew, plus the Homebrew elemental set |
| **Druid** | 6 | +21, **−1** | **26** | Druidcraft, Primal Savagery, Magic Stone, Create Bonfire, Frostbite, Infestation, Control Flames, Mold Earth, Shape Water, Gust, Thunderclap, Moonflare, plus 9 Homebrew elemental cantrips |
| **Bard** | 8 | +4 | **12** | Thunderclap, Prestidigitation, Illusionary Dart, Thunder Note |
| **Cleric** | 9 | +3 | **12** | **Word of Radiance**, Spare the Dying, Moonflare |

> **⚠ Shillelagh is no longer a Druid cantrip.** bg3.wiki lists it among the Druid's six vanilla
> cantrips; it is **absent** from Listo's 26-entry cantrip list and present in the Druid's
> **level-1 spell** pool instead. That is the hard confirmation of the warning already in
> `data/classes/druid.md` — in Listo you prepare Shillelagh and spend a slot on it, and it then
> lasts until long rest. Any published Druid guide that treats it as an at-will cantrip is
> describing a different game.

> **The blade cantrips are the headline.** Green-Flame Blade and Booming Blade scale on
> **character level**, land on a **weapon attack**, and are the cheapest way to make an Int- or
> Cha-caster contribute in melee. Booming Blade is already on the vanilla Wizard/Sorcerer/Warlock
> cantrip lists; the mods add Green-Flame Blade and Sparking Blade, and the active SLCF
> **BladeCantrips** rule guarantees you get the whole set rather than whichever implementation
> loaded last. This also means **Magic Initiate (Wizard/Sorcerer/Warlock) on a martial buys a
> scaling melee cantrip** — see the feats section.

---

## List sizes, vanilla vs Listo

BG3 stores two shapes of spell list, and the mods respect the distinction — which is why the two
tables below are counted differently. It is worth understanding before reading them.

- **Known casters** (Wizard, Sorcerer, Bard, Ranger, Warlock) get one **cumulative** list per tier:
  the "spell level 3" list contains every level-1, -2 and -3 spell they may pick. Verified — the
  additions at each tier are a strict superset of the tier below.
- **Prepared casters** (Cleric, Druid, Paladin) get one **per-tier** list and receive *all* of it
  automatically. Verified — the additions at each tier are disjoint from the tier below.

### Known casters — the cumulative pick pool

Read as `vanilla + modlist = pool you choose from`.

| Class | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 |
|---|---|---|---|---|---|---|---|---|---|
| **Wizard** | 23+22=**45** | 48+53=**101** | 67+79=**146** | 81+95=**176** | 90+108=**198** | 102+113=**215** | **226** | **242** | **260** |
| **Sorcerer** | 18+17=**35** | 39+43=**82** | 53+63=**116** | 63+75=**138** | 71+82=**153** | 78+87=**165** | **176** | **182** | **192** |
| **Bard** | 15+9=**24** | 31+22=**53** | 39+34=**73** | 44+41=**85** | 50+47=**97** | 52+51=**103** | **105** | — | **122** |
| **Ranger** | 10+11=**21** | 17+23=**40** | 22+36=**58** | — | **68** | — | — | — | — |

Levels 7–9 (and Ranger 4–5, Paladin 4–5) do not exist in vanilla BG3 at all — `Expansion Level
13-20` creates those pick lists, and `ListoPFSpells` then re-declares them at roughly double the
size. Those cells are measured totals rather than sums. **`Expansion` is what makes levels 13–20
exist; PF2e Spells is what makes them interesting.**

### Prepared casters — per tier, and the whole list

Read as `vanilla + modlist = the tier you get for free`.

| Class | L1 | L2 | L3 | L4 | L5 | L6 | **Whole list** |
|---|---|---|---|---|---|---|---|
| **Druid** | 14+15=**29** | 13+13=**26** | 6+14=**20** | 11+8=**19** | 7+7=**14** | 5+4=**9** | 56 + 61 = **117** |
| **Cleric** | 11+5=**16** | 11+8=**19** | 12+10=**22** | 4+4=**8** | 7+5=**12** | 6+5=**11** | 51 + 37 = **88** |
| **Paladin** | 11+5=**16** | 5+8=**13** | 7+7=**14** | 0+3=**3** | 0+5=**5** | — | 23 + 28 = **51** |

**The Druid is the quiet winner of the whole modlist.** Its list slightly more than doubles, every
addition is free (prepared caster), and the growth is front-loaded at exactly the levels a
three-level Druid dip reaches.

### The half-casters and Warlock

| Class | Shape | Additions |
|---|---|---|
| **Warlock** (per patron) | cumulative, per patron | +5 / +5 / +26 / +5 / +43 at spell levels 1–5 |
| **Artificer** | patch-owned, absolute | 23 / 36 / 36 / 32 / 39 entries at spell levels 1–5, plus a 76-entry scroll list |
| **Mesmerist** | absolute | 17 / 36 / 49 |
| **Inquisitor** | absolute | 20 / 37 / 58 / 72 / 93 |

> **⚠ Dispel Magic does not exist in the base game.** bg3.wiki has no Dispel Magic on any class
> list (only the Cleric's level-5 *Dispel Evil and Good*). The `Dispel Magic` mod adds it and
> re-declares the **spell-level-3 list of every caster in the game** to carry it — Cleric, Paladin,
> Druid, Ranger, Bard, Sorcerer, Wizard, Eldritch Knight and all Warlock patrons. It is included in
> the "+" columns above. Practical read: **every caster in Listo can strip a buff or a summon at
> spell level 3**, which is not true in vanilla BG3 and changes what enemy concentration is worth.

---

## Per-class notes

### Wizard — the biggest beneficiary, twice over

- **Pick pools: 45 at spell level 1 (vanilla 23), 146 at 3 (vanilla 67), 215 at 6 (vanilla 102),
  then 226 / 242 / 260 at 7–9.** Levels 7–9 are the
  `Expansion` + `ListoPFSpells` stack; the level-1–6 additions are `5e Spells` (45 at L3 alone),
  `Homebrew Spells` (16), `Spells of Exandria` (5) and Valkrana (8).
- **The tabletop capstones only exist here and on Sorcerer.** `AdvancedTabletopSpells` puts
  **Wish, Time Stop, Shapechange, Meteor Swarm, Gate, Prismatic Wall, Weird, Psychic Scream,
  Invulnerability, Mass Polymorph, Blade of Disaster, Antimagic Field, Maze, Horrid Wilting,
  Illusory Dragon, Sunburst, Draconic Transformation, Prismatic Spray** into the level-9 pool.
  This is a real argument for taking Wizard to 17+ that does not exist in vanilla BG3.
- **Scroll transcription is the multiplier.** Wizard is the only class that converts a dropped
  scroll into a permanent list entry, and the modlist's scroll drop tables now carry the modded
  spells too. A Wizard's *effective* list is the union of the pick pool and everything the
  campaign drops — see `data/classes/wizard.md` § "Dipping into Wizard".
- **Dunamancy is present.** `Spells of Exandria` merges **Gift of Alacrity** (a permanent +1d8
  initiative that lasts until long rest), **Fortune's Favour**, **Magnify Gravity**, **Immovable
  Object**, **Gravity Sinkhole**, **Temporal Shunt**, **Tether Essence**, **Gravity Fissure**,
  **Reality Break** and **Dark Star**. Gift of Alacrity at level 3 is the cheapest initiative
  purchase in the file, and in a two-person party going first is worth more than in a four-person
  one.
- **Bladesinger reads a 39-cantrip list.** Green-Flame Blade on a Bladesinger is the modded
  version of the standard trick and it is available from level 1.
- **Hierophant is the one wired cross-list subclass** — see the cross-class section.

### Sorcerer — same pools, fewer picks, but Metamagic on top

- **176 / 182 / 192** at levels 7/8/9, and **+82 at level 5**. Nearly everything the Wizard gets,
  including Wish, Time Stop, Meteor Swarm, Gate and Blade of Disaster.
- **Chaos Bolt** is in the list (`5e Spells`), which matters for Wild Magic.
- The real note is structural: the list went **78 → 165 → 192** but the *known-spells* count did
  not move. A bigger pool on a fixed 13-known chassis means **better picks, not more of them**, and
  swapping a known spell still needs a respec. Contrast the Wizard, whose scroll transcription
  turns list growth directly into breadth, and the Druid, who simply receives its whole list.
- **Twinned Spell now has far more targets worth twinning**, including Gift of Alacrity (via
  Magical Secrets or a Wizard partner), Ashardalon's Stride, Spirit Shroud and Tenser's
  Transformation.

### Bard — Magical Secrets is the largest single grant in the modlist

| Tranche | Level | Pool size |
|---|---|---|
| Lore's **Additional Magical Secrets** | Bard 6 | **221** |
| **Magical Secrets** | Bard 10 | **280** |
| **Magical Secrets** (`Expansion`) | Bard 14 | **376** |
| **Magical Secrets** (`Expansion`) | Bard 18 | **415** |

- Those pools are the **whole cross-class arcane and divine roster** — Wizard, Cleric, Druid,
  Sorcerer and Warlock spells side by side, plus every mod pack's contribution. A Lore Bard at 6
  is choosing two spells from 221 options.
- `Automatic Magical Secrets Extender` (`20247`) is installed on top of this and pulls in
  further class lists at runtime; it is a Script Extender mod so its effect is not visible in the
  pak files. See `data/classes/bard.md`.
- **The Bard's own list grew too** — +50 by level 6, 122 at level 9, including **Glibness**,
  **Power Word: Heal**, **Power Word: Fortify**, **Psychic Scream**, **Mass Polymorph**,
  **Etherealness**, **Motivational Speech**, **Heroes' Feast** and **Mass Healing Word**.
- **In a two-person party this is the whole argument for a Bard.** One Magical Secrets pick can
  cover the gap the other character leaves — Revivify, Counterspell, Haste, Spirit Guardians or
  Aura of Vitality — without either player respeccing.

### Ranger — quietly the largest proportional gain of any half-caster

- **Level-5 pool is 68 spells, stated as a total** (`Expansion` 32 → `ListoPFSpells` 49, plus
  `5e Spells` 29). Vanilla BG3 Ranger has a famously thin list; this is a different class.
- Standouts merged in: **Zephyr Strike**, **Absorb Elements**, **Ashardalon's Stride**,
  **Summon Fey**, **Summon Elemental**, **Steel Wind Strike**, **Swift Quiver**, **Conjure Volley**,
  **Guardian of Nature**, **Healing Spirit**, **Greater Restoration**, **Revivify**, **Searing
  Smite**, **Elemental Weapon**, **Flame Arrows**, **Beast Bond**, **Nondetection**.
- **Revivify on a Ranger at spell level 3** is the fact worth remembering for a duo — it removes
  the "one of us must be a Cleric/Paladin/Bard" constraint.

### Druid — list slightly more than doubles, and it is all free

- **56 vanilla spells → 117.** Per tier: 29 / 26 / 20 / 19 / 14 / 9. A prepared caster receives
  every one of them, so this is the largest *usable* list gain in the modlist — the Wizard's pool
  is bigger but the Wizard must still pick from it.
- **+15 at spell level 1** is the largest level-1 gain of any class: **Absorb Elements**, **Beast
  Bond**, **Detect Magic**, **Earth Tremor**, **Protection from Evil and Good**, **Snare**,
  **Shillelagh** (list-level, see the Shillelagh warning in `data/classes/druid.md`), plus five
  Homebrew elemental spells.
- Level 2–3 add **Flock of Familiars**, **Healing Spirit**, **Summon Beast**, **Conjure Animals**,
  **Aura of Vitality**, **Elemental Weapon**, **Revivify**, **Warding Wind**, **Wither and Bloom**.
- Level 5 adds **Maelstrom**, **Cone of Cold**, **Antilife Shell**, **Commune with Nature**.
- Above spell level 4 the additions dry up (+4 to +7 per tier). The Druid's high end is Wild Shape
  and circle features, not the spell list — but the growth is concentrated at exactly the tiers a
  **two- or three-level Druid dip** reaches, which is the practical read.
- **Shillelagh moved from cantrip to level-1 spell** — see the cantrip table warning.
- **The Limited Lists override strips Valkrana from Druid** except Circle of Spores.

### Cleric — the smallest absolute gain of any full caster

- **51 vanilla spells → 88.** Per tier: 16 / 19 / 22 / 8 / 12 / 11. That is +37 against the
  Wizard's +113 and the Druid's +61, out of 445 injected overall — but it is still a **72%**
  increase, and because Cleric is a prepared caster **all of it is free**.
- What did land is genuinely good: **Ceremony**, **Detect Evil and Good**, **Zone of Truth**,
  **Gentle Repose**, **Borrowed Knowledge**, **Find Traps**, **Aura of Vitality**, **Life
  Transference**, **Motivational Speech**, **Spirit Shroud**, **Water Walk**, **Aura of Life**,
  **Holy Weapon**, **Raise Dead**, **Dawn**, **Sunbeam**, **True Seeing**, and the level-3 block
  `Dispel Magic` injects everywhere.
- **Domain lists are where the Cleric's variety lives**, not the base list — `Goon's Cleric
  Overhaul` and the domain mods carry that, documented per-domain in `data/classes/cleric.md`.
- Planning consequence: **a Cleric dip is still bought for armour, Channel Divinity and the domain
  package.** The list grew, but it grew least, and the spells that arrived are utility rather than
  the fight-winners — the Cleric's ceiling is unchanged while the Wizard's tripled.
- Note the **level-4 tier is the thinnest in the game**: 4 vanilla + 4 modded = **8 spells**.

### Paladin — the smallest list in the game, roughly doubled

- **23 vanilla spells → 51.** Per tier: 16 / 13 / 14 / 3 / 5. Proportionally the biggest jump of
  any prepared caster, from the smallest base; in absolute terms still the shortest list in the
  file. Notables: **Ceremony**, **Detect Evil and Good**, **Warding Bond**,
  **Prayer of Healing**, **Gentle Repose**, **Zone of Truth**, **Force Weapon**, **Aura of
  Vitality**, **Crusader's Mantle**, **Blinding Smite**, **Blind Faith**, plus `Expansion`'s
  per-oath level 4–5 pairs (Ancients → Ice Storm/Stoneskin/Commune with Nature/Wall of Stone;
  Vengeance → Banishment/Dimension Door/Hold Monster/Far Step; Crown → Circle of Power/Dominate
  Person; Devotion → Freedom of Movement/Guardian of Faith/Flame Strike/Greater Restoration;
  Oathbreaker → Blight/Confusion/Contagion/Dominate Person).
- Divine Smite spends *any* slot, so **the Paladin's own list has never been the point** — but note
  that a Paladin/Sorcerer or Paladin/Warlock still converts the partner list's slots into smites.

### Warlock — patron lists grew, and the invocations grew more

- Patron lists gain **+26 at spell level 3 and +43 at level 5** each for Archfey / Fiend / Great
  Old One. Notables: **Shadow of Moil**, **Synaptic Static**, **Far Step**, **Mislead**,
  **Raulothim's Psychic Lance**, **Negative Energy Flood**, **Summon Aberration: Beholderkin**,
  **Summon Shadowspawn**, **Summon Fey**, **Spirit Shroud**, **Planar Binding**, **Teleportation
  Circle**, **Enemies Abound**, **Intellect Fortress**.
- **Mystic Arcanum is where the ceiling moved**: the 9th-level Arcanum pool gains **Foresight,
  Gate, Shapechange, Weird, Psychic Scream, Power Word: Kill and Blade of Disaster**. One
  free 9th-level spell per long rest, chosen from that set, on a class whose *other* slots refuel
  on short rests.
- **Pact of the Tome gets 18 Book of Shadows cantrips** from `5e Spells` — Druidcraft, Word of
  Radiance, Spare the Dying, Primal Savagery, Magic Stone, Mind Sliver, the blade cantrips, and the
  utility set — cast at will and off any list. For a duo this is the cheapest source of
  out-of-combat utility coverage in the game.
- **Book of Ancient Secrets** (from `Spells Extra`) adds 3 further ritual entries.
- **34-cantrip Warlock list** including all three blade cantrips means a Hexblade or Pact of the
  Blade warlock has a scaling melee cantrip without spending a feat.

### Artificer — hand-built by the Listo patch, and the only class whose list is fully enumerable

- `Listo Master Spells Patch` **owns the Artificer lists outright** (23 / 36 / 36 / 32 / 39 entries
  at spell levels 1–5, plus a 76-entry scroll list), assembled from `Artificer class and all
  subclasses`, `Artificer 5e Spells Addon` and `ListoPFSpells`. The four subclass lists (Alchemist,
  Armorer, Artillerist, Battle Smith at 3/5/9/13/17) are likewise patch-owned.
- Because the patch re-declares them, these are the **actual full lists**, not deltas — the cantrip
  list is 36 entries including **Booming Blade, Green-Flame Blade, Guidance, Magic Stone, Thorn
  Whip, Lightning Lure, TK Thrust** and the Dawnstar/Homebrew elemental set.
- Level-3 and up carry **Counterspell, Haste, Fly, Revivify, Intellect Fortress, Glyph of Warding,
  Elemental Weapon, Flame Arrows, Ashardalon's Stride, Freedom of Movement, Stoneskin, Greater
  Restoration, Skill Empowerment, Wall of Stone, Temporal Shunt** and **Shadow Blade / Flame Blade**.
- **Revivify + Counterspell + Haste on a half-caster that also opens with Int+Con saves** is the
  reason Artificer keeps showing up in duo planning. See `data/classes/artificer.md`.

### Eldritch Knight (Fighter) and Arcane Trickster (Rogue)

- **Eldritch Knight**: +10 at spell level 1, +22 at 2, and **+65 at 4** once `Expansion` opens the
  full abjuration/evocation table (Fireball, Counterspell, Banishment, Fire Shield, Wall of Fire,
  Stoneskin, Ice Storm, Lightning Bolt, Shield). `5e Spells` adds **Absorb Elements, Aganazzar's
  Scorcher, Rime's Binding Ice, Snilloc's Snowball Storm, Minute Meteors, Storm Sphere, Vitriolic
  Sphere, Warding Wind, Intellect Fortress**, and `Listo Master Spells Patch` adds **Shadow Blade
  and Flame Blade**.
- **Arcane Trickster**: +12 at spell level 2 and **+35 by 4**, including **Shadow Blade** (the
  single best Arcane Trickster spell — a finesse-adjacent psychic weapon that pairs with Sneak
  Attack), **Nathair's Mischief**, **Mind Whip**, **Raulothim's Psychic Lance**, **Enemies Abound**,
  and `Expansion`'s enchantment/illusion table at 3–4 (Hypnotic Pattern, Fear, Hold Person,
  Greater Invisibility, Phantasmal Killer).
- Both gain a **16–17 entry Valkrana scroll list** — these two are among the classes the Limited
  Lists override *keeps*.

### Mesmerist, Inquisitor, Paragon, Blood Hunter, Monk, Barbarian

- **Mesmerist** carries its own list: **17 / 36 / 49** entries at spell levels 1–3 (full totals).
  It is a Charisma half-caster reading a control-heavy list — Bane, Bless, Command, Compelled Duel,
  Dissonant Whispers, Hold Person, Hypnotic Pattern, Fear, Counterspell, Slow, Shadow Blade,
  Intellect Fortress, Tasha's Mind Whip, Motivational Speech.
- **Inquisitor** carries a Wisdom list of **20 / 37 / 58 / 72 / 93** entries (full totals) that
  mixes Paladin, Ranger and Cleric material with the Dawnstar blood/telekinesis set — Hunter's Mark,
  Divine Favour, Shield of Faith, Misty Step, Spiritual Weapon, Hold Person, Counterspell,
  Crusader's Mantle, Banishment, Death Ward, Guardian of Faith, Contagion, Destructive Wave,
  Dominate Person, Greater Restoration, Hold Monster. **This is the widest half-caster list in the
  modlist.**
- **Paragon** and **Blood Hunter** are not spell-list classes. Paragon's two list entries are
  Distract and Paragon's Help; Blood Hunter's are the **8 Blood Curses** and the **16/17/20-entry
  Mutagen tables** at Order of the Mutant 3/7/11. Blood Hunter's *Profane Soul* order reads a
  Warlock-shaped list of **8 / 19 / 27 / 35 / 31** entries.
- **Monk** gains nothing list-wise except Four Elements, whose level-17 table `Expansion` fills
  with 21 entries (Breath of Winter, River of Hungry Flame, Eternal Mountain Defense, Wave of
  Rolling Earth, Fist of Unbroken Air). `Warrior of the Elements` replaces that subclass by
  default — see `data/classes/monk.md`. Way of Shadow's Shadow Arts is a fixed grant, not a list.
- **Barbarian has no spell access at all.** The only progression entries that touch a spell list
  are two single-spell grants at level 10 (Ancestral Protector, Zealous Presence) from
  `5e Barbarian Subclasses Combined`. The *"Barbarian Primal Sentry"* lists in `Spells Extra`
  are unreferenced library content. A Barbarian who wants spells buys them with a feat
  (`-Touched`, Magic Initiate, Ritual Caster) or a three-level dip.
- **Base Fighter, Rogue and Monk likewise have no list** — their access is the Eldritch Knight and
  Arcane Trickster subclasses above, or the same feat/dip routes.

---

## Cross-class access routes, ranked

**1. Bard Magical Secrets — 221 / 280 / 376 / 415 at Bard 6 (Lore) / 10 / 14 / 18.**
Nothing else in the modlist comes close. Two spells per tranche, from every list at once.

**2. Wizard scroll transcription.** Unbounded rather than large: any Wizard scroll the campaign
drops becomes a permanent list entry, and the drop tables now include modded spells. A Wizard 2
dip on an Int character (Eldritch Knight, Arcane Trickster, Artificer) buys the *ability to keep
growing*, which no other route does. `data/classes/wizard.md` prices this out.

**3. Hierophant (Wizard subclass, `7859`).** The only cross-list subclass actually wired in 10.2.
Its **Combined** list runs 79 / 95 / 109 / 124 / 134 / 145 / **158** entries at spell levels 3–9 —
a merged Wizard + Cleric list on one Intelligence stat, with a 15-cantrip combined cantrip list
(Sacred Flame and Word of Radiance alongside the arcane set). Plus fixed always-prepared grants:
Guiding Bolt, Lesser Restoration, Mass Healing Word, Guardian of Faith, Greater Restoration,
Spirit Guardians, Flame Strike, Harm, and Raise Dead as a ritual at 10.

**4. Warlock Pact of the Tome.** 18 at-will Book of Shadows cantrips drawn from across the
Druid, Cleric and arcane cantrip lists, for one pact choice at Warlock 3.

**5. Magic Initiate feats.** See the table below — the pools these read are the *modded* class
lists, which is why they are worth more here than the feat text suggests.

**6. Multiclassing.** Unremarkable mechanically, but note that in Listo a **3-level dip is
feat-neutral** (feats land at class level 3/6/9/12/13/15/18), so buying a whole new spell list
costs three levels and no feats. Sorcerer 3, Warlock 3, Bard 3 and Wizard 2/3 are all in range.

---

## Feats that grant spell-list access

Read from `Feats.lsx` in `Cahoots Feats Overhaul` (+ its Listo patch) and `Essential Feats`.
`data/listo-10.2-feats.md` has the rest of each feat's mechanics — this table is only about
*which pool* it reads.

| Feat | Reads | Picks | Pool as installed |
|---|---|---|---|
| **Magic Initiate: Wizard** | Wizard cantrips + Wizard L1 | 2 cantrips + 1 spell | **39 cantrips** (incl. all three blade cantrips, Mind Sliver, Toll the Dead) / L1 pool +22 (Absorb Elements, Gift of Alacrity, Magnify Gravity, Catapult, Cause Fear, Snare, Unseen Servant) |
| **Magic Initiate: Sorcerer** | Sorcerer cantrips + Sorcerer L1 | 2 + 1 | **42 cantrips** / +17 (Absorb Elements, Chaos Bolt, Grease, Catapult, Caustic Brew) |
| **Magic Initiate: Warlock** | Warlock cantrips + Warlock L1 | 2 + 1 | **34 cantrips incl. Eldritch Blast and the blade trio** / +2 |
| **Magic Initiate: Druid** | Druid cantrips + Druid L1 | 2 + 1 | **26 cantrips** (Primal Savagery, Magic Stone, Thorn Whip) / +15 (Absorb Elements, Shillelagh, Beast Bond, Protection from Evil and Good) |
| **Magic Initiate: Bard** | Bard cantrips + Bard L1 | 2 + 1 | +4 cantrips / +9 |
| **Magic Initiate: Cleric** | Cleric cantrips + Cleric L1 | 2 + 1 | +3 cantrips (**Word of Radiance**) / +5 (Ceremony, Detect Evil and Good, Detect Magic) |
| **Ritual Caster** | Ritual list + Ritual cantrips | **all rituals** + 2 cantrips | **14 rituals**: Ant Haul, Ceremony, Commune with Nature, Detect Magic, Detect Thoughts, Disguise Self, Feather Fall, Find Familiar, Jump, Longstrider, Speak with Animals, Speak with Dead, Unseen Servant, Water Walk. **8 cantrips**: Dancing Lights, Friends, Guidance, Light, Mage Hand, Minor Illusion, Resistance, Thaumaturgy |
| **Spell Sniper** | Attack-cantrip list | 1 cantrip | **13**: Chill Touch, **Eldritch Blast**, Fire Bolt, Frostbite, Illusionary Dart, Lightning Lure, Ray of Frost, Rock Slam, Starry Wisp, Shocking Grasp, Sonic Blast, Thorn Whip, Water Bullet |
| **Fey Touched** | Divination/Enchantment L1 | Misty Step + 1 | **13**: Animal Friendship, Bane, Bless, Charm Person, Command, Compelled Duel, Dissonant Whispers, Heroism, **Hex**, Hideous Laughter, **Hunter's Mark**, Sleep, Speak with Animals |
| **Heaven Touched** | Abjuration/Transmutation L1 | Sanctuary + 1 | **11**: **Armor of Agathys**, Create/Destroy Water, Expeditious Retreat, Feather Fall, **Goodberry**, Jump, **Longstrider**, **Mage Armor**, Protection from Evil and Good, **Shield**, Shield of Faith |
| **Hell Touched** | Harmful Conjuration/Evocation L1 | Hellish Rebuke + 1 | **14**: Arms of Hadar, Burning Hands, **Chromatic Orb**, Ensnaring Strike, Entangle, **Faerie Fire**, Fog Cloud, **Grease**, **Guiding Bolt**, Hail of Thorns, **Ice Knife**, **Magic Missile**, Thunderwave, **Witch Bolt** |
| **Shadow Touched** | Illusion/Necromancy L1+2 | Invisibility + 1 | **11**: Blindness, **Blur**, Disguise Self, False Life (upcast 2), Inflict Wounds (2), **Mirror Image**, Phantasmal Force, Ray of Enfeeblement, Ray of Sickness (2), **Shadow Blade**, **Silence** |

**Notes that change how you pick these:**

- **Ritual Caster is the outlier.** Listo's patch replaces "pick 3" with **learn all 14**, and adds
  **Find Familiar** to the list. One feat buys a permanent extra body plus Speak with Dead, Detect
  Thoughts, Disguise Self, Longstrider and Feather Fall as free out-of-combat casts, on any
  character. In a two-person party the third body matters more than the spells.
- **The `-Touched` feats are the cheapest way onto a *different* list.** Heaven Touched grants
  **Shield** to a character with no arcane list at all; Shadow Touched grants **Shadow Blade** and
  **Mirror Image**; Hell Touched grants **Magic Missile** and **Witch Bolt**. Each is a half-feat
  (+1 INT/WIS/CHA) and casts on a **short-rest** clock, which in a 120-supply-per-long-rest run is
  the clock that counts.
- **Fey Touched carries Hex and Hunter's Mark**, so it is also a concentration-damage rider for a
  martial with no caster level at all.
- **Magic Initiate uses your own spellcasting ability, not the chosen class's** (Listo change), and
  the level-1 spell **costs a slot instead of having a cooldown, with a level-1 slot granted in
  return.** The cantrips are the durable half of the feat — which is why the blade cantrips in the
  Wizard/Sorcerer/Warlock pools are the pick that actually scales.
- **Magic Initiate spells cannot be upcast** — `Magic Initiate Feats Enhanced` is **not** in the
  list.
- **`Arcanist` is gone** (removed in v9.0.3). Do not plan around it; see
  `data/listo-10.2-feats.md`.

---

## Scroll lists

Scroll lists control what can drop and, for a Wizard, what can be transcribed. The modlist extends
them for every class: Artificer 76 entries (patch-owned, full total), Wizard/Bard/Sorcerer/Ranger/
Druid/Cleric/Paladin/Warlock and both Eldritch Knight and Arcane Trickster all receive the
Valkrana set (16–19 entries) and the `5e Spells` roster. `Hierophant` carries its own combined
scroll list.

Practical read: **scroll drops in Act II–III now include modded spells**, so a Wizard's library
grows past its own pick list, and any character with `Ritual Caster` (half-price scribing) or
`Spell List Customization Framework`-touched cantrips benefits from the wider tables.

---

## Not present / explicitly off

| Thing | Status |
|---|---|
| **`OPTIONAL_Spelljammer 5e @`** | Installed but **unticked in the profile**. Its spells and scroll-list entries are unavailable. |
| **`OPTIONAL_Valkranas Skeletal Challenge +`** | Off. |
| **Valkrana spells on Cleric / Druid / Paladin / Ranger / Mesmerist / Artificer** | **Blocked** by `Valkrana's Spellbook Limited Lists`, except Death-domain Cleric and Circle-of-Spores Druid. |
| **`Spells Extra` "Enhanced" and "Savant" lists** | Defined but **unreferenced** — Knowledge Domain does *not* get wizard spells, War Domain does *not* get the paladin list, Way of Shadow does *not* get a necromancy list, Arcane Trickster does *not* get the enchantment expansion. Only the Hierophant lists are wired. |
| **Community Library `Bard Magical Secrets (5e)` / `Warlock OneDnD` lists** | Defined but unreferenced. The live Magical Secrets pools are the ones in the Bard table above. |
| **SLCF `MindSliver` dedupe rule** | Present in the rules file, **not in `active_user_rules`** — the three Mind Sliver implementations are not collapsed. |
| **`Magic Initiate Feats Enhanced`** | Not in the list; Magic Initiate spells cannot be upcast. |
| **`Arcanist` feat** | Removed in v9.0.3. |

---

## Unverified / worth confirming in game

- `(unverified)` The **vanilla halves** of the size tables come from bg3.wiki's `List of <class>
  spells` pages, not from Larian's paks (which are not under the mods root). The wiki tracks the
  current patch and reconciled exactly against every list a mod re-declares in full, so treat it
  as sound — but a wiki page is one step further from ground truth than a pak is.
- `(unverified)` Whether the **duplicate implementations** (Foresight, Feeblemind, Mind Blank,
  Regenerate, Power Word: Kill, Dominate Monster) both appear in the level-up UI or whether the
  game silently collapses them. They are distinct stat entries, so expect both.
- `(unverified)` What `Automatic Magical Secrets Extender` adds on top of the 415-spell pool at
  Bard 18 — it operates at runtime through Script Extender and leaves no pak evidence.
- `(unverified)` Whether the Listo `Ritual Caster` patch's "learn all" behaviour covers all 14
  entries or only the 3-pick selector's subset; the patch declares a `SelectSpells(...,2,0,...)`
  for cantrips but the ritual selector's arity was not resolvable from the feat node alone.
- `(unverified)` Whether **Blood Hunter's Profane Soul** patron list stacks correctly with a real
  Warlock level — the mod never addresses multiclassing (see `data/classes/bloodhunter.md`).

---

## How this file was built

**The vanilla baseline comes from bg3.wiki.** Larian's `Shared.pak` is not under the mods root, so
the base-game lists cannot be read the same way. The wiki generates its `List of <class> spells`
tables from a Cargo store; **arbitrary Cargo queries are blocked** (`permissiondenied`), so parse
the rendered table instead:

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"
curl -sS -A "$UA" -o Cleric.html "https://bg3.wiki/wiki/List_of_Cleric_spells"
# one <table class="wikitable sortable">; column 1 = name, column 2 = level ("C" for cantrip)
python3 - <<'EOF'
import re
h = open("Cleric.html", encoding="utf-8").read()
t = h.split('class="wikitable sortable"', 1)[1].split("</table>", 1)[0]
for r in re.findall(r'<tr>(.*?)</tr>', t, re.S):
    c = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)]
    if len(c) > 1 and c[0] != "Name": print(c[1], c[0])
EOF
```

Page titles are `List of <Class> spells` — `<Class>_Spells` 404s. `action=parse&prop=wikitext`
returns only the `{{Spell table}}` transclusion, not the rows.

```bash
# every pak that declares spell lists (86 of 810 in 10.2)
python3 scripts/lspk.py "<mod>/PAK_FILES/<x>.pak" | grep SpellLists.lsx

# the two injection idioms: MergedInto=<vanilla uuid>, or a same-UUID re-declaration
python3 scripts/lspk.py "<pak>" "Public/<Mod>/Lists/SpellLists.lsx" \
  | grep -o 'id="\(UUID\|MergedInto\|Name\|Comment\|Spells\)"[^/]*'

# what consumes a list — class/subclass progressions and feats
python3 scripts/lspk.py "<pak>" "Public/<Mod>/Progressions/Progressions.lsx" | grep -E 'AddSpells|SelectSpells'
python3 scripts/lspk.py "<pak>" "Public/<Mod>/Feats/Feats.lsx"               | grep -E 'AddSpells|SelectSpells'

# enabled/disabled state — MO2 lists highest priority FIRST; "-" means unticked
grep -E "^[+-]" /mnt/mercury/Games/Listonomicon/profiles/Listonomicon/modlist.txt
```

**A list is only live if a progression or feat selector names its UUID.** That single check is what
separates the Hierophant's combined list (real) from the twenty-odd "Enhanced" lists in
`Spells Extra` (library shelfware). Run it before promising a player any cross-class access.

**Sanity check any refresh by reconciling the two sources.** Every list a mod re-declares in full
must equal `vanilla + additions`: Wizard cantrips 16 + 23 = 39 ✓, Sorcerer 15 + 27 = 42 ✓,
Warlock 10 + 24 = 34 ✓. The one place it did *not* reconcile — Druid 6 + 21 = 27 against a measured
26 — was the finding that **Shillelagh was moved out of the cantrip list**. A mismatch is a
result, not an error; chase it before adjusting a number.

> **Note on `scripts/lspk.py`:** some paks in this modlist (e.g. `Spell List Customization
> Framework`) use **zstd (compression method 3)**. The reader handles it as of this pass, but the
> branch needs the `zstandard` package — without it you get
> `RuntimeError: entry is zstd-compressed; pip install zstandard` instead of a silent failure.
