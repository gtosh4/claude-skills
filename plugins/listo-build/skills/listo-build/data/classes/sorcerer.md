# Listonomicon 10.2 — Sorcerer

Sorcerer in Listo is the vanilla BG3 chassis — Charisma full caster, d6 hit die, Con + Cha saves,
spells always prepared, sorcery points as a second currency — with three layers on top: a full
13–20 progression from `Expansion` (`279`) that adds a **fifth Metamagic pick at 17** and
**Sorcerous Restoration at 20**; `Metamagic Extended` (shipped as Listo's own patched build,
`MMExtended Patched`) which adds **Empowered, Seeking and Transmuted** to the Metamagic menu; and
**three extra bloodlines** (Aberrant Mind, Favored Soul, Wretched Soul) plus a **27-ancestry
expansion** to Draconic. The headline change is Wild Magic, which is rebuilt from four stacked
mods into a **ramping in-combat risk meter** rather than a flat 5% roll — see the Wild Magic
section, which is the most important part of this file. Listo's own docs page 4 has a Sorcerer
section, but **two of the three mods it names are no longer the ones shipping**: `Tides of Chaos
Recharge` (`11625`) has been replaced by `Tides of Chaos DnD 5R PHB2024` (`15760`), and
`Metamagic Extended` (`405`) is present only as a repackaged community patch hosted on Listo's
own Nexus page (`8976`), so neither ModID appears in `listo-10.2-mods.tsv`.

**Provenance.** Compiled 17 August 2026 against the bundled 10.2 snapshot. Every mod named here
was confirmed present in `listo-10.2-mods.tsv` **or** in `listo-10.2-manifest.json` (three
Sorcerer-relevant paks ship without a TSV row — see "Mods that are installed but absent from the
TSV"). Vanilla baselines come from bg3.wiki. Mechanical detail comes from mod pages, which
describe each mod's **current** version; where Listo pulled an older archive the date is given.
Anything not read is marked `(unverified)`.

---

## At a glance

| | |
|---|---|
| **Primary ability** | Charisma (spell DC, spell attack rolls) |
| **Saves granted at level 1** | **Constitution + Charisma** — only if Sorcerer is your *first* class |
| **Hit die** | d6 (6 + Con at level 1, 4 + Con on level-up) — the joint-lowest in the game |
| **Armour / weapons** | **No armour, no shields.** Daggers, Quarterstaves, Light Crossbows |
| **Skills at level 1** | **Choose 2** from Arcana, Deception, Insight, Intimidation, Persuasion, Religion |
| **Multiclass node (Sorcerer as a later class)** | **Nothing.** bg3.wiki: "No additional proficiencies are granted when multiclassing into Sorcerer." No saves, no armour, no skills |
| **Spells** | **Always prepared**, but a fixed small *known* list — **4 cantrips / 2 spells** at level 1, **5 / 5** at 4, **6 / 11** at 10, **6 / 13** at 12. Swapping known spells requires a respec |
| **Sorcery points** | **= Sorcerer class level**, from level 2 (2 at L2 … 12 at L12 … 20 at L20). **Long rest only** until `Expansion`'s **Sorcerous Restoration at 20** |
| **Font of Magic** (L2) | Create Spell Slot (points → slot) and Create Sorcery Points (slot → points), both bonus actions |
| **Metamagic picks** | **2 at level 2**, +1 at **3**, +1 at **10**, **+1 at 17** (`Expansion`). Five total at cap. `Meta Magic Adept` feat adds **2 more options + 3 points** — see `data/listo-10.2-feats.md` |
| **Spell slot ceiling** | 6th level at 11 in vanilla; `Expansion` carries 7th/8th/9th through 13–20 |
| **Level breakpoints** | **1** subclass + saves · **2** Font of Magic + 2 Metamagic · **3** 3rd Metamagic · **5** 3rd-level slots (Fireball/Haste), `Expansion` optional **Magical Guidance** · **6** subclass feature (and Arcane Chaos for Wild Magic) · **10** 4th Metamagic · **11** subclass feature + 6th-level slots · **17** 5th Metamagic · **18** subclass capstone (Draconic Presence / Umbral Form / Wind Soul) · **20** Sorcerous Restoration |
| **Feat cadence** | Listo grants feats every **3 levels** (`Universal Feat Every X Level(s) - MCM`, `13193`) — **a 3-level Sorcerer dip is feat-neutral.** Cross-ref `data/listo-10.2-feats.md` |
| **Dip value** | **Sorcerer 2** for Font of Magic, **Sorcerer 3** for Metamagic. Both are strong; **Sorcerer 1 is nearly worthless as a later class** because the multiclass node grants nothing |

**The Charisma trap applies in full.** Sorcerer grants **Charisma** at level 1, so putting Lone
Wolf's +4 on Charisma wastes one of the two grants. Con + Cha is also the *narrowest* pair a
level-1 class can give — it collides with Lone Wolf on Charisma **and** with the single most
common Lone Wolf pick (Constitution, for concentration). Sorcerer-first is the worst save-coverage
opener among the Charisma casters. See `references/listo-rules.md` § "The Charisma trap".

---

## Wild Magic in Listo

Vanilla BG3 Wild Magic: each **level 1 or higher** spell you cast rolls a flat **5%** chance of a
surge, off a **20-effect** table. **Tides of Chaos** (level 1) is once per long rest, grants
Advantage on your next Attack Roll / Ability Check / Saving Throw, and raises the next surge
check to **50%**; the condition is consumed the moment a Wild Magic check is rolled.

Listo replaces almost all of that. **Four mods stack**, and the resulting model is:

### The surge risk meter

`Increasingly Likely Wild Magic Surge` (`9603`, archive
`Increasingly Likely Wild Magic Surge-9603-1-0-0-0`, pak `Increasingly Likely Wild Magic
Surge.pak`) **plus its Combat Only addon** (pak `ILWMS Combat Only Addon.pak`) — **both are
installed**, in two separate mod folders.

- The chance starts at **1/20 (5%)** and rises **+1/20 (+5 percentage points) per spell cast
  that does not surge**: 5% → 10% → 15% → … → **20/20 (100%)**.
- The running chance is visible in-game as the **`Unstable Magic`** condition. **Read that
  condition before committing a big turn** — it is the whole risk model in one tooltip.
- The meter **resets to 5% on a successful activation** (i.e. when a surge actually fires).
- **The Combat Only addon means the meter only advances in combat.** Out-of-combat Healing Word,
  Longstrider, Feather Fall, Mage Hand and so on cost you nothing. Listo's docs page 4 states
  this and it verifies against the shipped pak.
- The mod page: **"This mod is only for Sorcerer. It does not affect Wild Magic Barbarian."**
  Whether it also drives the wild magic inflicted by the `Enweaved` feat is `(unverified)`.
- ILWMS works by replacing the `StatsFunctors` field of the `WildMagic` passive, so it is
  **incompatible with any other mod that changes surge chance** — which is why the vanilla Ring
  of Feywild Sparks had to be reworked (below).

### Tides of Chaos

`Tides of Chaos DnD 5R PHB2024 - Wild Magic Sorcerer` (`15760`, archive `Tides of Chaos DnD 5R
PHB2024-15760-2-0`, v2.0, 18 Apr 2025). **This is the mod shipping in 10.2 — not `Tides of Chaos
Recharge` (`11625`), which the docs still name and which is not in the manifest.**

- Tides of Chaos **guarantees a Wild Magic surge** after activation (it no longer merely sets the
  chance to 50%).
- Its cooldown is **once per long rest** …
- … **but is reset every time you trigger a Wild Magic surge.** This is what the docs mean by
  "wild magic surges will restore Tides of Chaos" — you can loop it many times per adventuring
  day.
- The mod rewrites all tooltip and error text to match, so **the in-game descriptions are
  trustworthy here.**

**The loop, stated plainly:** use Tides of Chaos → your next spell surges (guaranteed) → the surge
refunds Tides of Chaos → the `Unstable Magic` meter resets to 5% → repeat. You can also decline to
start the loop entirely: leave Tides of Chaos alone and you are on the 5%-per-cast ramp only. The
docs' phrasing — "you can avoid starting the wild magic risk slide by avoiding using Tides of
Chaos, but that would be boring" — is accurate.

> **Interaction caveat `(unverified)`.** ILWMS's own page says *Tides of Chaos sets the chance to
> 50% unless it is already higher*, and lists `True Tides of Chaos` (the mod `15760` is
> explicitly modelled on) as **incompatible**. `15760` says ToC **guarantees** a surge. Both are
> installed. Which behaviour wins depends on Listo's load order, which the manifest does not
> expose. Assume "guaranteed" (it matches Listo's own documentation) but confirm on the tooltip
> in-game before building a turn around it.

### The effect table

Four effect mods stack. All are patched to coexist by `d100 Wild Magic Tables Patched`
(pak `Wild Magic D100 Patches.pak`, sourced from Listo's own `Listonomicon Again` page, `15237`),
which is what keeps the sorcerer and barbarian tables from colliding.

| Mod | ModID | Archive | Adds |
|---|---|---|---|
| *(vanilla)* | — | — | 20 effects |
| `Wild Magic D100 Table` | `2967` | `Wild Magic D100-2967-1-1-0` | **80** effects. **Wild Magic Sorcerer only.** Includes *Fireball centred on yourself*, *polymorphed into a wheel of cheese*, *Banished for 2 turns*, *summon a hostile Spectator*, *Confused for 3 turns*, and *Incapacitated this turn* — alongside genuinely strong rolls like *next spell attack deals maximum damage* |
| `More Wild Magic effects` | `2022` | `MoreWildMagic 1.3.2-2022-1-3-2` (v1.3.2, Sep 2023) | ~15 effects — 7 shared with Barbarian (Raise Dead, Mass Swap, Resurrection, Dance Party, Forcefield, Mind Sanctuary, free 5th-level Magic Missile), 8 Sorcerer-only (Blink, Portent die, Aura of Truth, transform into an Intellect Devourer, predetermined roll, Polymorph Self, Grease, Music) |
| `Homebrew Wild Magic (for Sorcerer and Barbarian)` | `20299` | `…-20299-1-0-4` (Jan 2026) | **30** effects, most shared with Barbarian. Author's own warning: "Some of these effects can be rather penalising." **Main file only** — the Playtest optional file is not installed |

Effective table size is therefore roughly **145**, not the "220+" the changelog once claimed —
that figure predates the removal of `Home Brew Over 100 Wild Magic Effects` (removed in v10.0) and
`[Mod.io] 60 Wild Magic Effects`.

### The Volo trigger

`Topple the Weave - The Death of Volothamp Geddarm` (`4030`, archive `Topple the Weave-4030-1-1`,
pak `ToppleTheWeave.pak`). Script Extender based.

**If Volo dies for any reason, the Weave unravels and every spellcaster — yours, allies',
enemies' — is inflicted with a variation of Wild Magic that procs 100% of the time.** On top of
the surge, there is a high chance of one of: a **permanent** damage-type change on a damaging
spell (not shown in the tooltip); 1–1000 gold appearing or up to 100 gold vanishing; your turn
immediately ending; your equipped item being unequipped; a random status; a random projectile
fired at you; a random explosion centred on you; **your character immediately dying**; all
cooldowns reset; a random surface or pool under your feet; **your Tadpole powers lost**; you
forget the spell you just cast; all your summons dispelled.

> **Duo relevance: keep Volo alive.** With two characters and Lone Wolf, "your character
> immediately dies" as a possible outcome of *any* cast, on *both* players, is a run-ending
> mechanic rather than a comedy one. This is the single highest-stakes NPC in the list for a
> caster duo.

### Gear interaction

`Ring of Feywild Sparks Rework` (`15789`, archive `Ring of Feywild Sparks Rework-15789-1-0`) —
by the same author as `15760`, and installed specifically because ILWMS and `15760` break the
vanilla ring. Vanilla: guarantees a surge while Tides of Chaos is active, plus a **hidden** +1
Spell Save DC. In Listo: the **Tides of Chaos interaction is removed**, the **baseline surge
chance while the ring is equipped rises from 5% to 20%**, and the **+1 Spell Save DC is
unhidden**. Cross-ref `data/listo-10.2-equipment.md` (line entry for Ring of Feywild Sparks).

> Note the ring now raises the **baseline** — the floor of the ILWMS ramp — so a ring-wearing
> Wild Magic Sorcerer starts each combat at 20% and climbs from there `(unverified — whether the
> ramp adds to 20% or the ring merely sets a one-time floor was not readable from either page)`.

### Other wild-magic sources

- **`Enweaved` feat (`13310`)** — +2 to INT/WIS/CHA capped at 22, and inflicts **both wild magic
  and magic allergy**. Full entry in `data/listo-10.2-feats.md`; the feats file explicitly notes
  the surge mods above are what make its downside real.
- **`Arcane Chaos` feat** (archive `ArcaneChaosFeat-14228-1-0-0`, shipped as an optional file of
  `14228`) — the feats file marks its effect `(unverified)`; **it is now verified.** The Nexus
  files tab: *"Arcane Chaos as feat, allows you cast **any** spell using sorcery points instead
  of spell slots and triggers wild magic."* Note **"any spell"** — broader than the Wild Magic
  subclass's own level-6 version, which is limited to subclass spells.
- Enemies. Listo's encounter work gives wild magic and **Controlled Chaos** to kuo-toa casters,
  mephits, and select fey; **Lorroakan can force *you* to risk a surge rather than risking one
  himself.** Being *near* enemy casting matters if you carry Enweaved's magic allergy.

---

## Metamagic

**Vanilla picks:** Careful (1 pt), Distant (1), Extended (1), Twinned (1 per slot level; cantrips
1) at level 2+; Heightened (3), Quickened (3), Subtle (1) at level 3+.

**`Expansion` adds a fifth Metamagic selection at level 17.**

### Metamagic Extended

**Installed as `MMExtended Patched`** — pak `MetamagicExtended.pak`, pulled from archive
`MMExtended Patched-8976-1-0` (22 Nov 2024) on **Listo's own Nexus page (`8976`)**, not from mod
`405`. This is why `405` does not appear in the TSV. The repackage exists because a community
patch was needed to fix Transmuted Spell (changelog: *"Fixed the 'Transmute Spell' metamagic in
Metamagic Extended, thanks to a community patch"*).

Only the **main** pak is installed. The three options it adds:

| Metamagic | Cost | Effect |
|---|---|---|
| **Empowered Spell** | **1** sorcery point | Rolls spell **damage dice with Advantage**. Combines with other Metamagics. Best on high-dice-count spells — Magic Missile, Scorching Ray, Fireball, Acid Arrow |
| **Seeking Spell** | **2** sorcery points | **Advantage on spell attack rolls**. Combines with other Metamagics. For Scorching Ray, Guiding Bolt, Chromatic Orb |
| **Transmuted Spell** | **1** sorcery point | **Changes the damage type** of an elemental spell to one you pick |

**How to use Transmuted Spell** (this is the bit that confuses people, and Listo's docs call it
out): **activate the metamagic first, then pick an element from the pop-up that appears.** The
new options live in the **Metamagic section of your hotbar — expand that section or you will not
see them.**

**Not installed:** the `Metamagic Extended Plus` add-on. That means **Tripled Spell, Twinning
Unlimited, Detached Spell, Expanded Spell, Maximized Spell and the 2-point Quickened Spell are
all absent.** Quickened costs the full **3** points here.

### The bonus-action rule

Listo enables tabletop's bonus-action casting rule: **you cannot combine a spell that takes a
bonus action with a levelled spell cast in the same turn, unless you have Quickened Metamagic or
another mechanic that overcomes it** (changelog, Combat Extender / rules settings). This makes
**Quickened Spell materially more valuable in Listo than in vanilla** — it is not just an extra
cast, it is the only general-purpose exemption from the rule.

> **Duo relevance.** With two characters, **Twinned Spell hits 100% of the party** — Haste,
> Greater Invisibility, Hold Person, Fly, Polymorph, Blur, Death Ward all become party-wide for
> one Metamagic pick. In a four-person party Twinned is a niche pick; in a duo it is the single
> best Metamagic in the list. **Quickened** is second: Lone Wolf already grants an extra Action,
> and Quickened converts a Bonus Action into a second levelled cast on top of that, so a Sorcerer
> can realistically land three spells in a turn. Take **Twinned + Quickened first**; Careful,
> Distant, Extended and Subtle are filler by comparison. Note Quickened is a **level 3** option,
> which is exactly why Sorcerer 3 is the dip breakpoint rather than Sorcerer 2.

---

## Class changes from vanilla

### `Expansion` — levels 13–20 (`279`, archive `Expansion-279-1-7-3-6`)

Class features added:

- **Magical Guidance** — optional, **level 5**. (Spend a sorcery point to reroll a failed ability
  check; exact Listo implementation `(unverified)`.)
- **Metamagic** — one additional selection at **level 17**.
- **Sorcerous Restoration** — **level 20**. (5e: regain sorcery points on a short rest. Exact
  BG3 numbers `(unverified)`.)

Subclass features added at **18**: **Draconic Presence** (Draconic Bloodline), **Umbral Form**
(Shadow Magic), **Wind Soul** (Storm Sorcery). **Wild Magic Sorcerer gets no 13–20 subclass
feature from Expansion** — it is the one vanilla bloodline that stops at 11.

`Expansion` also exposes an MCM toggle, **"Sorcerer Subclasses 14th Level Feature"**, which moves
the level-11 subclass feature (Draconic Wings / Controlled Chaos / Storm's Fury / Shadow Walk)
back to level 14 as tabletop has it. **The mod default is disabled.**

**The installed profile sets `misc.Sorcerer11thSubclass: true`** — a non-default value, so Listo
changed something here. The key name is ambiguous: read as "subclass feature at 11", the feature
stays at **11**; read as the toggle's internal name, it moves to **14**. `(unverified — confirm
at level 11.)` This is the one Expansion setting the install does not settle; everything else in
`MCM/Expansion/settings.json` is unambiguous and recorded in `data/listo-10.2-mcm.md`.

Note also **`optional_features.Sorcerer: false`** — Expansion's Sorcerer optional features are
off.

### `Multiclass Preferred Casting Ability Fix` (`10209`)

In the list. Multiclassing no longer reassigns your Spellcasting Stat to the newest class's
ability, so a Sorcerer X / Cleric 1 keeps **Charisma** as the stat that drives scrolls, Illithid
powers and stat-scaling items. **You can multiclass in any order.** The classic Sorcerer /
Tempest Cleric 1 lightning dip works as intended here.

### Feats and stat caps

- Feats at **3, 6, 9, 12, 13, 15, 18** (`13193`). A 3-level Sorcerer dip costs no feats.
- **`Feats Overhaul` (`15044`) removes the ability-score cap of 20 on feat-granted increases** —
  a Sorcerer can push Charisma past 20 on half-feats alone. See `data/listo-10.2-feats.md`, which
  also flags an unresolved question about whether the uncap reaches Essential Feats' half-feats.
- **`Meta Magic Adept`** (Essential Feats): **2 metamagic options + 3 metamagic points**, plus
  **+1 INT/WIS/CHA**. A non-Sorcerer route to Twinned or Quickened, and a way for a Sorcerer to
  get a sixth and seventh option.

### Spell pool

`5e Spells` (`125`), `PF2e Spells` (Listo's patched fork), `Homebrew Spells`, `Spells Extra`,
Mystra's Spells and Valkrana's Spellbook all add to class lists, and several add to Sorcerer's.
Listo has also **pruned** Sorcerer access in places — the changelog records removing Shade Shield,
Mark of Putrefaction and Sigil of Mortality from Sorcerers specifically. Enemy casters draw from
the same expanded pools.

### No Goon overhaul

Listo ships Goon's Overhauls for Barbarian, Bard, Cleric, Paladin, Rogue, Wizard and the Slayer.
**There is no Goon's Sorcerer Overhaul** — the Sorcerer chassis itself is unmodified apart from
Expansion and Metamagic Extended.

---

## Bloodlines (subclasses)

Seven playable, and one Metamagic-adjacent note. All confirmed present.

### Draconic Bloodline (vanilla) + Draconic Bloodline Expanded

- **Mod:** `Draconic Bloodline Expanded` (`13563`); cosmetics from `P4 Draconic Bloodline`
  (`11998`) and `Draconic Scales - Color Expansion` (`10686`)
- **File pulled:** `Draconic Bloodline Expanded-13563-1-0` (v1.0, 2 Nov 2024), pak
  `DraconicBloodlinesExpanded.pak`; `P4 Draconic Bloodline-11998-1-0-0-0`, pak
  `P4_Draconic_Bloodline_….pak`
- **Mechanics:**
  - Vanilla: **L1** Draconic Resilience (unarmoured AC 13, +1 HP per Sorcerer level) + choose an
    ancestry (a damage type and a free spell). **L6** Elemental Affinity — add your **Charisma
    modifier** to damage of your ancestry's type, and spend 1 sorcery point for Resistance to it.
    **L11** Draconic Wings (flight). **L18** Draconic Presence (`Expansion`).
  - `13563` adds **27 new ancestries** on top of the vanilla 10, each with a granted spell and a
    damage type:
    - **5e**: Shadow (Arms of Hadar / **Necrotic**), Dracolich (Hex / Poison), Hallow (Sanctuary /
      **Radiant**), Deep (Dissonant Whispers / **Psychic**), Moonstone (Faerie Fire / **Radiant**),
      Solar (Searing Smite / Fire), Lunar (Ice Knife / Cold)
    - **Gem**: Amethyst (Magic Missile / **Force**), Crystal (Charm Person / **Radiant**), Emerald
      (Entangle / **Psychic**), Sapphire (Thunderous Smite / Thunder), Topaz (Inflict Wounds /
      **Necrotic**)
    - **New metallics**: Steel (Disguise Self / Acid), Mercury (Guiding Bolt / **Radiant**)
    - **New chromatics**: Grey (Hail of Thorns / **Piercing**), Pink (Create or Destroy Water /
      **Psychic**), Yellow (Longstrider / **Bludgeoning**), Orange (Hellish Rebuke / Fire), Purple
      (Bane / Fire), Brown (Chromatic Orb — Acid only / Acid)
    - **Ferrous**: Iron (Command / Fire), Chromium (Chromatic Orb — Cold only / Cold), Cobalt
      (Thunderwave / **Force**), Tungsten (Compelled Duel / **Bludgeoning**), Nickel (Hunter's
      Mark / Acid)
    - **Eyrie**: Force (Shield / **Force**), Prismatic (Color Spray / Fire)
  - **`P4 Draconic Bloodline` is cosmetic only** — it adds scale colours to character creation for
    dragonborn and non-dragonborn. Despite the name, it grants no mechanics. Listo's docs imply
    otherwise by listing it under Sorcerer; do not plan around it.
- **Duo relevance:** the reason this mod matters is **Elemental Affinity now reaches damage types
  that had no Charisma-scaling route before** — **Force** (Amethyst, Cobalt, Eyrie Force: Magic
  Missile, Eldritch Blast, Disintegrate, and almost nothing resists it), **Radiant**, **Necrotic**
  and **Psychic**. An Amethyst Sorcerer adding Cha mod to every Magic Missile dart is the
  single highest-floor damage build the expansion enables, and Force resistance is rare enough
  that it holds up across all three Acts. Draconic is also the only bloodline that fixes the d6
  hit die (+1 HP/level) and the no-armour problem (AC 13 base), which matters more when losing
  one of two characters ends the fight.

### Wild Magic (vanilla) + Wild Magic Subclass - Additional Spells

- **Mod:** `Wild Magic Subclass - Additional Spells` (`14228`) — plus the whole surge stack
  documented above
- **File pulled:** `WildMagicSpells-14228-1-0-1` (v1.0.1, 5 Dec 2025), pak `WildMagicSpells.pak`;
  **and separately** the optional `ArcaneChaosFeat-14228-1-0-0`, pak `ArcaneChaosFeat.pak`, in
  its own mod folder
- **Mechanics:**
  - Vanilla: **L1** Wild Magic (surge chance per levelled cast) + Tides of Chaos. **L6** Bend Luck
    — reaction, 2 sorcery points, roll 1d4 and apply it as a bonus **or penalty** to any visible
    creature's attack roll, ability check or saving throw. **L11** Controlled Chaos — **induce a Wild Magic Surge on a
    nearby spellcaster** (including enemy casters). **No 13–20 subclass feature** — `Expansion` does not cover Wild Magic Sorcerer.
  - `14228` adds a **subclass spell list**, which vanilla Wild Magic lacks entirely:
    **L1** Tasha's Hideous Laughter, Color Spray · **L2** Mirror Image, Misty Step ·
    **L3** Blink, Hypnotic Pattern · **L4** Confusion, Polymorph · **L5** Telekinesis,
    Dominate Person
  - `14228` adds **Arcane Chaos at level 6** — a toggleable passive letting you cast **those
    subclass spells** with **sorcery points equal to the spell's level** instead of a slot.
    **Spells cast this way always trigger a Wild Magic Surge.**
  - The **Arcane Chaos feat** (separate pak) extends the same trade to **any** spell.
- **Duo relevance:** the risk math is inverted relative to a four-person party. A surge that
  Banishes you for two turns, Confuses you for three, polymorphs you into a wheel of cheese or
  drops a Fireball on your own head removes **half the party** — and losing either character
  usually ends the fight. Against that: **Bend Luck is one of the best reactions in the game for
  a duo**, because a ±1d4 swing applied to the enemy's save against your partner's Hold Person,
  or to a boss's attack roll against your low-AC caster, is exactly the kind of single-roll
  intervention a two-person party lives and dies on — and Lone Wolf grants an extra reaction to
  spend on it. Play Wild Magic as **Bend Luck first, chaos second**: leave Tides of Chaos alone in
  fights you cannot afford to lose, and only start the loop when a surge landing badly would be
  survivable. The `Unstable Magic` tooltip is your gauge.

### Storm Sorcery (vanilla)

- **Mod:** none — vanilla, with `Expansion` (`279`) supplying the capstone
- **Mechanics:** **L1** Tempestuous Magic — after casting a level 1+ spell, **fly 9 m as a bonus
  action** without provoking opportunity attacks. **L6** Heart of the Storm — Lightning/Thunder
  spells deal (Sorcerer level ÷ 2) of that type to all enemies within 6 m, plus Resistance to
  Lightning and Thunder. **L11** **Storm's Fury** — reaction: when struck by a melee
  attack, deal Lightning damage to the attacker and possibly push them back. **L18** **Wind Soul**
  (`Expansion`).
- **Duo relevance:** the mobility is the point — a two-person party has no front line, and a
  bonus-action disengage-and-fly every turn keeps your caster out of melee for free. Note the
  bonus-action conflict rule above: Tempestuous Magic competes with Quickened Spell for the same
  Bonus Action. The classic **Storm Sorcerer + Tempest Cleric 1** lightning stack works here
  because `Multiclass Preferred Casting Ability Fix` keeps Charisma as the spellcasting stat.

### Shadow Magic (vanilla) + Shadow Magic Expanded - Umbral Form

- **Mod:** `Shadow Magic Expanded - Umbral Form` (`15855`)
- **File pulled:** `Shadow Magic Expanded - Umbral Form-15855-1-0` (archive timestamp
  **2025-04-18 00:44 UTC**, which matches the **"Umbral Form - Level 18"** main file, not the
  Level 12 alternative), pak `Shadow Magic Expanded.pak`
- **Mechanics:**
  - Vanilla (Patch 8): **L1** Eyes of the Dark (24 m darkvision) + Strength of the Grave (on
    reaching 0 HP, regain 1 instead of going down). **L3** Darkness, plus a special
    Eyes-of-the-Dark Darkness you can see through. **L6** Hound of Ill Omen (short-rest recharge).
    **L11** Shadow Walk — teleport into shadow; your next spell that turn gets **Distant Spell
    free**.
  - `15855` adds **Umbral Form at 18**: spend **6 sorcery points** as a **Bonus Action** to become
    shadow — **Resistance to all damage except Force and Radiant**, for **10 turns**, ending early
    if you are Incapacitated, die, or dismiss it (there is a **toggle in your passives** to
    dismiss). Requires a level-20 mod, which Listo has.
  - **Redundancy flag:** `Expansion` (`279`) *also* lists **Umbral Form (18th Level)** for Shadow
    Magic, and its changelog records adding it. Two mods therefore ship the same feature at the
    same level. Whether they conflict, stack, or one simply overwrites the other is
    `(unverified)` — check for a duplicate passive at level 18.
- **Duo relevance:** **Strength of the Grave at level 1** is a free "do not go down" for a party
  that cannot afford anyone going down, and it triggers on a d6-hit-die body. That alone makes
  Shadow Magic the most survivable Sorcerer opener. Umbral Form at 18 is effectively a second set
  of hit points for the last two Acts. Note that **True Darkness is not installed** (see "Not
  present") — the darkness-cheese builds published for Shadow Sorcerers do not work here.

### Aberrant Mind

- **Mod:** `Aberrant Mind Sorcerer Subclass` (`3901`)
- **File pulled:** `Aberrant Mind Sorcerer Subclass-3901-2-1` (v2.1, 2 Aug 2025), pak
  `AberrantMind_e79f6d0c-….pak`. Compatibility handled by `Compatibility Framework Subclass
  Patches` (`6996`, Chisfreak's patch, named in the changelog for exactly this mod).
- **Mechanics:**
  - **Psionic Spells** (L1, expanding): **L1** Mind Sliver, Arms of Hadar, Dissonant Whispers ·
    **L3** Calm Emotions, Detect Thoughts · **L5** Hunger of Hadar, Fear · **L7** Evard's Black
    Tentacles, **Summon Beholderkin** · **L9** Dominate Person, Telekinesis. These do **not**
    count against spells known.
  - **L1** also: on a **Critical Hit**, the target and nearby enemies make a **Wisdom save or are
    Frightened** until the end of their next turn; plus a Telepathic Speech feature (a renamed
    copy of the Great Old One Warlock's).
  - **L6 Psionic Sorcery** — cast any Psionic Spell by spending **sorcery points equal to its
    level** instead of a slot, and **with no verbal or somatic components**. Implemented as a
    toggleable passive that adds a duplicate set of spells to the right of your hotbar; upgraded
    versions appear at 7 and 9.
  - **L6 Psionic Defenses** — **Resistance to Psychic damage** and **Advantage on saves against
    Charmed and Frightened**.
  - **L11 Revelation in Flesh** — bonus action, spend sorcery points (1 each) to gain, until long
    rest: **Aberrant Flight** (9 m flying speed, hover, ignore surfaces and difficult terrain),
    **Aberrant Scrutiny** (32 m darkvision, see invisible within 18 m), **Aberrant Slithering**
    (squeeze through small openings, immune to Throw and Shove attempts, 2 m of movement to escape
    restraint or grapple). Casting one removes the bonus-action cost for one round so you can
    stack all three.
  - **L15 Warping Implosion** — Action, teleport up to 18 m; creatures within 5 m of your
    departure point make a **Strength save** or take **3d10 Force** and are pulled to where you
    were (half damage, no pull, on a success). Once per long rest, **or spend 5 sorcery points**
    to reuse. Requires a level-13+ mod, which Listo has.
  - Also ships a recoloured starter robe and a subclass dye (tutorial chest and various vendors).
- **Duo relevance:** the strongest *utility* bloodline for two players. **Advantage on Charm and
  Frighten saves plus Psychic resistance at level 6** patches two of the three effects most likely
  to take a character out of a fight, and a duo has no third body to break a Dominate. Psionic
  Sorcery's **no verbal or somatic components** means you can cast the whole Psionic list while
  **Silenced** — without spending a Metamagic pick on Subtle Spell, freeing that slot for Twinned.
  Summon Beholderkin at L7 is a genuine third body on the field.

### Favored Soul

- **Mod:** `Favored Soul - Sorcerer Subclass` (`9369`) — Unearthed Arcana 3 implementation
- **File pulled:** `Favored Soul 1.4.0-9369-1-4-0` (v1.4.0, 22 Oct 2025), pak `Favored Soul.pak`.
  Native Compatibility Framework and merged-progression support; non-vanilla spells come from the
  author's `Spells Extra` library, which Listo ships.
- **Mechanics:**
  - **L1 Chosen of the Gods** — pick a **Cleric Domain**; you learn that domain's spells at
    Sorcerer **1, 3, 5, 7 and 9**, they do **not** count against spells known, and they count as
    **Sorcerer spells for you** (so they run off **Charisma** and are eligible for Metamagic).
    **14 domains**: Arcana, Death, Forge, Grave, Knowledge, **Life**, Light, Nature, Order, Peace,
    Tempest, Trickery, Twilight, War.
    - **Life**: Bless, Cure Wounds / Lesser Restoration, Spiritual Weapon / Beacon of Hope,
      Revivify / Death Ward, Guardian of Faith / **Mass Cure Wounds, Raise Dead**
    - **Peace**: Heroism, Sanctuary / Aid, **Warding Bond** / Beacon of Hope, Daylight / Aura of
      Purity, Otiluke's Resilient Sphere / **Greater Restoration, Mass Cure Wounds**
    - **Tempest**: Fog Cloud, Thunderwave / Gust of Wind, Shatter / Call Lightning, Sleet Storm /
      Freedom of Movement, Ice Storm / Destructive Wave, Insect Plague
    - **Light**: Burning Hands, Faerie Fire / Flaming Sphere, Scorching Ray / Daylight,
      **Fireball** / Guardian of Faith, Wall of Fire / Dispel Evil and Good, Flame Strike
    - (Arcana, Death, Forge, Grave, Knowledge, Nature, Order, Trickery, Twilight and War lists are
      on the mod page; all follow the same 2-spells-per-tier shape.)
  - **L1 Bonus Proficiencies** — **light armour, medium armour, shields, and simple weapons.**
  - **L6 Extra Attack.**
  - **L11 Divine Wings** — bonus-action flight (implemented as Draconic Wings, moved to 11 to
    match Larian's compression).
  - **L15 Unearthly Recovery** — bonus action while below half HP, regain **half your maximum hit
    points**. Once per long rest. (The author substituted this for Power of the Chosen, which
    would not work.)
  - Carries the **Cleric tag for dialogue**.
- **Duo relevance:** **the pivotal bloodline for this run.** It is one of only **three Charisma
  casters with healing** in the list (with Bard and Celestial Warlock — see
  `references/listo-rules.md`), and unlike either of them it gets its healing **at level 1**,
  **off the Cleric list**, **as Sorcerer spells**, meaning **Metamagic applies**. **Twinned
  Cure Wounds, Twinned Death Ward, Twinned Warding Bond and Twinned Greater Restoration cover
  100% of a two-person party for one Metamagic pick.** Raise Dead and Revivify on the *Sorcerer*
  chassis solves the duo's worst failure mode — one character down means the other is alone. On
  top of that it fixes the class's two structural weaknesses at level 1 (**medium armour and
  shields** on a no-armour class, saving you a feat and roughly 4–5 AC) and adds **Extra Attack at
  6**. If you want one Sorcerer in a two-player Lone Wolf run and are not committed to the chaos,
  Favored Soul with **Life** or **Peace** is the default answer.

### Wretched Soul

- **Mod:** `(DTO) Otherworldly Archetypes` (`21822`) — a 12-subclass pack, one per class; the
  Sorcerer entry is **Wretched Soul**
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67 2026-06-17T17-15Z ….zip` (v1.2.0.67),
  pak `DaelensTestament_c714f127-….pak`. Added "for testing" per the changelog.
- **Mechanics:** *"Your soul is tainted by sinister energies which manifest as wither and decay, a
  corruption so dark and twisted that it eludes all defense."* Necrotic/damage-over-time themed,
  **fully featured to level 20**. What could be verified from the mod's version history:
  - **Wither** and **Decay** are stacking conditions it applies (they no longer affect objects and
    items as of 1.2.0.67).
  - **Epidemic** — a **toggleable passive**, **3d6 damage** and **1 sorcery point per
    activation**; Decay and Wither **detonate independently**.
  - **Metamagic: Vile Affliction** — a **subclass-specific Metamagic**, **2 sorcery points**,
    grants "piercing effects" for **10 turns** after casting. (The tagline's "eludes all defense"
    suggests this is the damage-bypass mechanism.)
  - **Feature names, levels, and the full progression are `(unverified)`** — the Nexus page carries
    only a one-line pitch and images; there is no written feature list, and the linked "Daelen's
    Testament of the Otherworldly" resource resolves to a Korean translation page (`21824`), not a
    spec. The author strongly recommends `Mystra's Spells` or `5E Spells` for this subclass
    specifically; Listo has both.
- **Duo relevance:** unassessable without the feature list. Its resource is sorcery points on a
  toggle rather than slots, which is duo-friendly (no long-rest pressure at 120+ camp supplies),
  but treat it as **untested content** — Listo's own changelog says it was added for testing, and
  `references/listo-rules.md` omits it from the surviving-subclass list entirely.

> **Correction to `references/listo-rules.md`.** That file lists the surviving Sorcerer
> subclasses as *"Aberrant Mind, Favored Soul, Draconic (Expanded ancestries), Storm, Shadow,
> Arcane Chaos."* Two errors: **Arcane Chaos is not a subclass** — it is the level-6 feature that
> `14228` grants to the vanilla **Wild Magic** subclass (plus a separate feat) — and **Wretched
> Soul is missing** from the list. The correct set is Draconic, Wild Magic, Storm, Shadow,
> Aberrant Mind, Favored Soul, Wretched Soul.

---

## Dip value

**Sorcerer 1** is close to worthless as a *later* class: the multiclass node grants **no
proficiencies at all** — no saves, no armour, no skills, no weapons. It buys a subclass's level-1
feature and Charisma-based casting progression, nothing else. Take Sorcerer 1 only for a specific
subclass feature (Draconic Resilience's AC 13, Shadow Magic's Strength of the Grave, Favored
Soul's **medium armour + shields**) or if Sorcerer is your **first** class, where it does grant
Con + Cha saves.

**Sorcerer 2 — Font of Magic.** Create Spell Slot and Create Sorcery Points, both bonus actions,
converting in **both directions**. Two sorcery points. In practice this is a **spell-slot battery
for another caster class**: a Warlock or Paladin can turn short-rest or unspent slots into points
and back, and any class that runs out of top-tier slots mid-fight gains a conversion route. Two
levels, feat-neutral only in combination with a third.

**Sorcerer 3 — Metamagic.** Two Metamagic options at 2 and a third at 3, and **the level-3 tier is
where Quickened and Heightened unlock.** Three sorcery points. **This is the dip worth taking**:
- **Twinned Spell** (available at 2) makes any single-target buff or control spell cover **the
  entire party** when the party is two people. Haste, Greater Invisibility, Fly, Death Ward,
  Polymorph, Hold Person, Blur — all party-wide for 1 point per slot level.
- **Quickened Spell** (level 3, 3 points) converts an Action spell to a Bonus Action. Alongside
  Lone Wolf's extra Action, and given Listo's rule that a bonus-action spell blocks a levelled
  cast **unless you have Quickened**, this is the only reliable route to three casts in a turn.
- **A 3-level dip is feat-neutral** under Listo's every-3-levels feat cadence — you collect the
  dip class's own level-3 feat, so Sorcerer 3 costs nothing in feats.
- Sorcery points scale off **Sorcerer class level only** (3 points at a 3-dip), so the dip gives
  you the *tools* cheaply but not the *fuel*. Pair a Sorcerer 3 dip with a class that has slots to
  convert.

**Sorcerer 1 as your first class** buys **Con + Cha saves** — the narrowest useful pair, and the
one most likely to collide with Lone Wolf's +4. Prefer a different level-1 class if you are
building a Sorcerer and want four distinct save proficiencies across the duo; see the worked
comparison in `references/listo-rules.md`.

---

## Not present

- **Frozen Sorcery and Spellfire Sorcery** — **confirmed removed.** Changelog v9.0.3, entry 56:
  *"REMOVED Frozen Sorcery and Spellfire Sorcery."* Both had been added earlier (Frozen Soul
  Sorcerer in v6, Spellfire Sorcery in v7.2). Neither is in the TSV or the manifest. The Aberrant
  Mind author's own "check out my other mods" banner still advertises Frozen Sorcery, Pyromancer,
  Arcanist, Lunar Sorcery, Clockwork Soul and Wretched Bloodline — **none of those are installed**;
  that banner is the most common source of stale Sorcerer recommendations for this list.
- **Divine Soul Sorcerer** — the changelog records "UPDATED Divine Soul Sorcerer" in an old
  version, but it is **not in the 10.2 TSV or manifest**. `Favored Soul` (`9369`) is the divine
  Sorcerer that ships. Do not plan a Divine Soul build.
- **Clockwork Soul, Lunar Sorcery, Giant Soul, Pyromancer, Wretched Bloodline, Runechild,
  Arcanist (as a subclass)** — none present; TSV and manifest sweeps found no matching entries.
- **`Tides of Chaos Recharge` (`11625`)** — named in Listo's docs page 4, **not installed.** Its
  function is supplied by `Tides of Chaos DnD 5R PHB2024` (`15760`), which additionally makes the
  activation a **guaranteed** surge and puts ToC on a long-rest cooldown.
- **`Metamagic Extended` as mod `405`** — installed, but as `MMExtended Patched` from Listo's own
  page (`8976`). Grepping the TSV for `405` or for "Metamagic" finds nothing; grep the **manifest**
  for `MetamagicExtended.pak`.
- **`Metamagic Extended Plus`** — the add-on is **not** installed. No **Tripled Spell**, **Twinning
  Unlimited**, **Detached Spell**, **Expanded Spell**, **Maximized Spell**, or **2-point
  Quickened**.
- **`True Darkness`** — **not in the TSV or the manifest.** An old changelog entry says it "makes
  shadow sorcerers and warlocks much more powerful by enabling the recreation of tabletop darkness
  cheese." **That mod is gone.** Do not build a Shadow Sorcerer around darkness stacking.
- **`Home Brew Over 100 Wild Magic Effects`** — **removed in v10.0** (changelog entry 4).
  **`[Mod.io] 60 Wild Magic Effects`** — removed earlier. The changelog's "220+ wild magic effects"
  claim is stale; the shipped table is roughly **145**.
- **`Wild Magic Cantrips` / `Wild Magic Smite` / `Wacky Wild Magic` / `Instruments of Controlled
  Chaos`** — recommended on the surge mods' own pages, none installed.
- **`Tasha's Sorcerer Items`** — removed in v7.0.x; not in the list.
- **`Mystic` class** — added in an old version ("acts like a sorcerer, a monk, or an INT
  paladin"), **not in the 10.2 TSV.** It is not an option.
- **The `Playtest` optional file of `Homebrew Wild Magic`** — main file only; the author warns
  against saving with the playtest file installed.
- **The Level 12 variant of `Shadow Magic Expanded`** — Listo pulled the **Level 18** file.
  Umbral Form is a level 18 feature here, not level 12.

---

## Mods that are installed but absent from the TSV

Grep the **manifest**, not the TSV, for these three:

| What | Where it actually comes from | Pak |
|---|---|---|
| Metamagic Extended | `MMExtended Patched-8976-1-0` (Listonomicon's own Nexus page, `8976`) | `MetamagicExtended.pak` |
| d100 wild magic cross-table patch | `Goon d100 Wild Magic-15237-4-1` (`Listonomicon Again`, `15237`) | `Wild Magic D100 Patches.pak` |
| Arcane Chaos **feat** | optional file of `Wild Magic Subclass - Additional Spells` (`14228`) | `ArcaneChaosFeat.pak` |

---

## Unverified / needs in-game confirmation

- **Which Tides of Chaos behaviour wins** when ILWMS (`9603`, "ToC sets chance to 50%") and
  `15760` ("ToC guarantees a surge") are both loaded. ILWMS lists the mod `15760` is modelled on
  as incompatible. The tooltip after `15760`'s text rewrite should settle it.
- **Whether the Ring of Feywild Sparks' 20% baseline is a floor the ILWMS ramp adds to, or a
  static replacement.**
- **Whether ILWMS's ramp applies to `Enweaved`-granted wild magic**, or only to the Wild Magic
  Sorcerer passive. ILWMS says "only for Sorcerer"; Enweaved grants the condition to anyone.
- **Whether `misc.Sorcerer11thSubclass: true` means the subclass feature sits at 11 or at 14.**
  The value is read from the install and is non-default; only the key's meaning is unclear.
  Confirm at level 11.
- **`Expansion`'s Magical Guidance (optional, L5) and Sorcerous Restoration (L20)** — present per
  the feature list; exact BG3 implementations and numbers not read.
- **Whether `Shadow Magic Expanded`'s Umbral Form and `Expansion`'s Umbral Form conflict,
  duplicate, or one overwrites the other** — both target Shadow Magic at level 18.
- **Wretched Soul's full progression** — only Wither/Decay, Epidemic and the Vile Affliction
  Metamagic could be recovered, and only from the mod's version history.
- **Whether Metamagic Extended's Script Extender dependency is satisfied** — Listo ships the
  Script Extender, and the changelog records a working Transmute fix, so this is very likely fine.
