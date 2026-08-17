# Listonomicon 10.2 — Wizard

Listo ships the Wizard essentially **un-nerfed and heavily extended**: all nine base-game
schools (including **Bladesinging**, which Larian added in Patch 8), plus six modded schools,
plus `Expansion Level 13-20` carrying every one of them to level 20 with real 5e capstones —
**Spell Mastery at 18** (a 1st- and a 2nd-level spell cast at will, *Shield* and *Mage Armour*
among the options) and **Signature Spells at 20** (two 3rd-level spells free once per short
rest). Nothing in the list changes the Wizard chassis itself: d6 hit die, no armour
proficiency, Int/Wis saves, Arcane Recovery on a long-rest cadence, scroll transcription as the
class's private gold sink. For a two-person Lone Wolf run that makes Wizard the **highest-
ceiling and lowest-floor** pick in the list — the widest spell access and the best summon
support (`Animate Dead++` removes the undead cap outright), attached to the squishiest body,
refuelled off the most expensive rest type.

**Provenance.** Compiled 17 August 2026 against the bundled 10.2 snapshot. Every school named
here was confirmed present in `listo-10.2-mods.tsv` **and** as an installed `.pak` in
`listo-10.2-manifest.json`. Vanilla baselines come from bg3.wiki. Expansion's level 13-20
mechanics were read out of the mod's **public source** (`github.com/Celestro/Expansion`,
`Progressions.lsx` / `Passive_Expansion.txt` / `MCM_blueprint.json`) — that source tracks the
current Nexus build **1.7.3.10**, while Listo pulled **1.7.3.6**; differences are flagged where
they matter. Anything not read from a source is marked `(unverified)`.

---

## At a glance

| | |
|---|---|
| **Primary ability** | **Intelligence** (spellcasting, spell DC, spell attack) |
| **Secondary** | **Constitution** (HP + concentration), **Dexterity** (AC — there is no armour) |
| **Saves granted at level 1** | **Intelligence + Wisdom** — the best save pair in the game for a caster (Wis covers the hold/charm/fear line). Only your level-1 class grants saves; **multiclassing *into* Wizard grants no proficiencies at all** |
| **Hit die** | **d6** — 6 + Con at level 1, 4 + Con thereafter. Lowest in the game |
| **Armour** | **None.** Weapons: daggers, quarterstaves, light crossbows. Bladesinging (school at level 2) is the only in-class source of light armour |
| **Skills** | Choose 2 from Arcana, History, Investigation, Insight, Medicine, Religion |
| **Spell slots** | Full caster. Expansion adds a **7th-level slot at 13, 8th at 15, 9th at 17, a 5th at 18, a 6th at 19, a 7th at 20** |
| **Arcane Recovery** | Charges = **ceil(wizard level / 2)**; spend an Action out of combat to buy back slots (2 charges → L2 slot, 3 → L3, 4 → L4, 5 → L5; **nothing above 5th**). Refreshes on **long rest only**. Expansion adds a charge at **13, 15, 17 and 19** (→ 10 at level 19) |
| **Key breakpoints** | **2** school; **5** L3 slots (Fireball/Counterspell/Haste/Animate Dead); **6** school feature; **10** school capstone; **11** L6 slots; **13-17** L7/8/9 slots via Expansion; **18 Spell Mastery**; **20 Signature Spells** |
| **Feats** | 3, 6, 9, 12, 15, 18 (see `listo-10.2-feats.md` — cadence is class-level based, so a 3-level dip is feat-neutral) |
| **Dip value** | **Low-to-moderate.** No proficiencies on multiclass in; the good stuff (Spell Mastery, Signature Spells, ward/summon scaling) is all deep. The exception is **Wizard 2 → Bladesinging** for light armour + Bladesong, see *Dip value* below |

---

## Class changes from vanilla

### The chassis is untouched
No mod in the list rewrites Wizard's core: hit die, proficiencies, Arcane Recovery's
formula/cadence, and prepared-caster mechanics are all as bg3.wiki describes. Plan AC and
concentration from **Shield, Mage Armour, Warding Bond, Blur, Mirror Image, gear and a dip** —
`listo-10.2-equipment.md` confirms **no mod in the list adds medium armour with caster
benefits**.

### `Expansion Level 13-20 (Configurable)` (`279`) — the biggest change
**Archive pulled:** `Expansion-279-1-7-3-6-1780876532.zip` → installs as
`mods\Expansion Level 13-20\PAK_FILES\Expansion.pak`. Requires Script Extender + MCM (both in
the list). Nexus's current main file is **1.7.3.10**; Listo is on **1.7.3.6**.

> **Manifest trap.** The TSV row for `279` reads *"Expansion (Bladesinger Only)"* and the
> manifest's `State.Version` says `0.0.26`. That is **stale cached Nexus mod metadata**, not
> the file that was pulled. The same staleness shows on other rows (Hierophant records `1.3.0`
> for a `1.6.0` archive; DTO records `1.1.0.60` for a `1.2.0.67` archive). There is exactly
> **one** archive from mod `279` in the manifest and it is the **main Expansion file**. The
> separate *"Bladesinger"* optional file on Nexus (v2.1.0.0, a standalone duplicate subclass)
> was **not** pulled.

Wizard class progression 13-20, read from `Progressions.lsx`:

| Level | Gained |
|---|---|
| 13 | +1 **7th-level** slot, +1 Arcane Recovery charge |
| 14 | — (school features land here) |
| 15 | +1 **8th-level** slot, +1 Arcane Recovery charge |
| 16 | Ability Score Improvement flag `(see note)` |
| 17 | +1 **9th-level** slot, +1 Arcane Recovery charge |
| 18 | **Spell Mastery** + 1 extra 5th-level slot |
| 19 | ASI flag `(see note)`, +1 6th-level slot, +1 Arcane Recovery charge |
| 20 | **Signature Spells** (choose 2), +1 7th-level slot |

- **Spell Mastery (18).** Choose **one 1st-level and one 2nd-level spell you know**; each
  becomes a free at-will cast (implemented as `Shout_SpellMastery_*` unlocks). A toggle lets
  you re-pick after each long rest, or keep your picks. The option list includes **Shield,
  Mage Armour, Magic Missile, Absorb Elements, Feather Fall, Find Familiar, Misty Step, Blur,
  Mirror Image, Invisibility, Hold Person, Web, Darkness, Enlarge/Reduce, Magic Weapon,
  Flaming Sphere** and ~60 more. **At-will Shield on a d6 caster is the single best defensive
  breakpoint the class reaches.**
- **Signature Spells (20).** Pick **2** from a fixed 32-spell list; each is cast free (with
  Intelligence) and refreshes on **short *and* long rest** — i.e. once per short rest each.
  List: Animate Dead, Ashardalon's Stride, Bestow Curse, Blink, Catnap, **Counterspell**,
  Enemies Abound, Erupting Earth, Fear, Feign Death, **Fireball**, Flame Arrows, **Fly**,
  Gaseous Form, Glyph of Warding, **Haste**, **Hypnotic Pattern**, Intellect Fortress, Life
  Transference, **Lightning Bolt**, Minute Meteors, Nondetection, Protection from Energy,
  Remove Curse, Sleet Storm, **Slow**, Speak with Dead, Spirit Shroud, Stinking Cloud, Summon
  Shadowspawn, Thunder Step, Vampiric Touch.
- **Cantrip Formulas (optional feature, MCM default ON).** Swap one known Wizard cantrip for
  another on level-up.
- **MCM note.** Expansion's shipped defaults are: Wizard optional features **on**, *Expansion's
  Bladesinger* **off**, *Song of Victory at 12th* **off**. But Listo ships its own
  `SE_CONFIG\BG3MCM\Profiles\Default\Expansion\settings.json`, whose values are **not readable
  from the manifest** — `(unverified)`. **Check MCM in game before relying on any of these,
  including the ASI-at-16/19 flags**, which sit alongside Listo's own feat cadence from
  `Universal Feat Every X Level(s)` (3/6/9/12/15/18 — see `listo-10.2-feats.md`).

### `Goon's Wizard Overhaul` (`17659`)
**Archive pulled:** `Goon's Wizard Overhaul-17659-1-0-2-3-1768157025.zip` (**main file only** —
the optional *"Bladesinger War Magic"* file was **not** pulled). Despite the name it is a small
bug-fix mod, not a rebalance:

- **Bladesinging:** Bladesong weapon animations no longer leak onto other characters.
- **Divination:** the referenced-but-missing `Divination_Ally_Downed` passive behind the
  *Prophecy: Delivering Alms* Expert Divination prophecy now exists and works.
- **Improved Minor Illusion:** the self-referencing infinite tooltip loop is fixed.
- *Not in Listo:* the optional file that would give Bladesingers **War Magic** at 6 alongside
  Extra Attack. Goon notes it is "not needed if using Expansion with the Bladesinger config
  option enabled" — which is off by default.

### `Arcane Recovery - Spell Balance Intent and Flavor` (`19623`) — a **spell** mod, not the class feature
**Archive pulled:** `Arcane Recovery-19623-1-03-01-1777352918.zip` (current). The name is the
mod series, not the Wizard feature; **it does not touch Arcane Recovery**. It sits *below*
Listo's own spell tweaks in priority. What it changes that a Wizard cares about:

- **Globe of Invulnerability** — rebuilt to 5e: Self, Concentration 1 min, immobile barrier
  that nullifies spells of 5th level or lower cast from outside; +1 blocked level per slot
  above 6th.
- **Dimension Door** — engine-max range, ignores line of sight, upcast support 7th+. (Listo
  separately makes Dimension Door a **Bonus Action**.)
- **Glyph of Warding** — permanent duration, cannot be cast in combat, upcast support 7th+.
- **Greater Invisibility** — no stealth checks to stay invisible when acting; acting instead
  updates your last-known position.
- **Banishment** — adds the missing "native to another plane → banished permanently if you hold
  concentration the full duration".
- **Shadow Blade / Bone Chill** — the mod restores Chill Touch's name and reworks Shadow Blade,
  but **Listo explicitly overrode the Shadow Blade change** (changelog: *"overwrite to remove
  Arcane Recovery from changing the spell"*).

### Scroll learning — the Wizard's private gold sink
Vanilla rules still apply: a Wizard may permanently copy any **Wizard-list** scroll for the
scroll **plus 50 gp per spell level**, provided you have a slot of that level (multiclass slots
count). Every base school **halves the copy cost of its own school to 25 gp/level**. The
expensive half is acquiring scrolls at all — Listo runs **4× buy / ¼ sell**, and v10.0 removed
*Secret Scrolls*. Note `Cahoot` redistributed **more 7th+ level spell scrolls** around the game
(changelog v7.x), which matters once Expansion gives you 7th-9th slots.

### Spell pool
The Wizard list is much wider than vanilla: `5e Spells` (`125`), `AdvancedTabletopSpells`
(`14429`), `Spells Extra - DND 5E Library` (`11291`), `Valkrana's Spellbook — 12 New Necromancy
Spells` (`1258`), `Conjure Animals and Summon Beast Spells` (`13458`), all reconciled by
`Spell List Customization Framework` (`21017`). Listo's v8 changelog trimmed several modded
spells back off the Wizard list (Shade Shield, Mark of Putrefaction, Sigil of Mortality).

---

## Schools (subclasses)

**Fifteen** are available: nine base-game, six modded. All base-game schools grant **Savant**
at level 2 (halved scroll-copy cost for that school) in addition to what is listed.

### Abjuration
- **Mod:** vanilla, extended by `Expansion` (`279`)
- **Mechanics:** **L2** *Arcane Ward* — casting an Abjuration spell charges the ward by the
  spell's level, cap **2× wizard level**; the ward eats damage 1-for-1 and loses 1 charge per
  hit; resets to *wizard level* on long rest. **L6** *Projected Ward* — spend the ward to
  absorb damage for a nearby ally (reaction, −1 charge). **L10** *Improved Abjuration* — the
  ward gains **wizard level** charges on every **short rest**. **L14 (Expansion)** *Spell
  Resistance* — **resistance to spell damage and advantage on all saving throws against spells
  and cantrips** (read from `Passive_Expansion.txt`).
- **Duo relevance:** the only school that fixes the Wizard's own fragility, and Projected Ward
  is one of very few ways to spend your Lone Wolf extra **Reaction** on keeping the *other*
  character alive. Improved Abjuration turns short rests into a real defensive resource, which
  matters when long rests cost 120+ supplies. Spell Resistance at 14 is close to a save-or-die
  insurance policy.

### Bladesinging
- **Mod:** **vanilla — added by Larian in Patch 8** (bg3.wiki: *"Released as part of Patch 8 in
  2025"*), extended to 20 by `Expansion` (`279`)
- **File pulled:** `Expansion-279-1-7-3-6-1780876532.zip` (main Expansion; the standalone
  *Bladesinger* optional file was not pulled and is not needed)
- **Mechanics:** **L2** *Training in War and Song* — proficiency in **light armour**,
  **Performance**, and daggers/longswords/rapiers/scimitars/shortswords/sickles; *Bladesong
  Power* 2/long rest. **Bladesong**: **+2 AC, +2 Constitution saving throws**, +3 m movement,
  advantage on Acrobatics; **no medium/heavy armour and no shield**, and you must be wielding
  one of the listed weapons. **L5** 3 uses, bonus → **+3**. **L6** *Extra Attack*. **L9** 4
  uses, bonus → **+4**. **L10** *Song of Defence* — expend a spell slot while Bladesinging to
  subtract 5 damage per slot level. **L11/13/15/17 (Expansion)** Song of Defence scales to
  6th/7th/8th/9th-level slots. **L14 (Expansion)** *Song of Victory* — **+Intelligence modifier
  to weapon damage while Bladesong is active** (`SongOfVictory` boost, `Passive_Expansion.txt`).
- **MCM switches (Expansion defaults, Listo's profile unverified):** *Expansion's Bladesinger*
  (**off** — replaces Larian's flat AC bonus with Expansion's original Intelligence-scaled
  version) and *Song of Victory at 12th instead of 14th* (**off**).
- **Duo relevance:** the answer to "a Wizard in a robe is the squishiest thing in the list".
  **+4 AC and +4 to Con saves** from a class feature, stacked on light armour, is the largest
  single concentration-protection package available to a full caster — and it comes with Extra
  Attack for turns where you would rather not burn a slot. The cost is that shields are locked
  out and Bladesong is a **long-rest** resource (2-4 uses), which is exactly the resource Listo
  taxes hardest.

### Conjuration
- **Mod:** vanilla + **`Conjuration School Enhanced`** (`20498`), archive `Conjuration Wizard
  Enchanced-20498-1-0-0-3-1768239708.zip` (current 1.0.0.3), pak `ConjurationEnchanced.pak`
- **Mechanics (vanilla):** **L2** *Minor Conjuration: Create Water* (short-rest recharge).
  **L6** *Benign Transposition* (long-rest recharge). **L10** *Focused Conjuration* — **damage
  cannot break your concentration on a Conjuration spell**.
- **Mechanics (mod, from the mod page):** **L3** *Minor Conjuration* is replaced with a
  bonus-action item conjurer — create Alchemist's Fire, a small healing potion, acid vial,
  caustic bulb, grease bottle, holy water, oil flask, spiked bulb, void bulb, slime bulb,
  **thieves' tools**, or a smokepowder bomb; items last **10 turns**; the damaging ones scale
  (**+1 die at levels 5, 10 and 15**; acid and holy water start at 2d6). **L6** *Ultimate
  Transposition* — Benign Transposition gains **18 m range** and can **swap with an enemy** on
  a failed Wisdom save vs your spell DC. **L6** additionally: **choose two Conjuration spells
  from any spell list**.
  `(Note: the mod page places its features at 3 and 6 while vanilla places them at 2 and 6 —
  whether the level-2 slot is replaced or supplemented is unverified.)`
- **Duo relevance:** the strongest *structural* pick. **Focused Conjuration at 10 makes your
  summons unkillable-by-interruption** — with two bodies against five-body encounters, the
  thing that loses you fights is a concentration break dropping your third and fourth
  combatants. Ultimate Transposition is also a free "extract the other player from a bad spot"
  button, and off-list conjuration picks reach into the druid/cleric summon pool.

### Divination
- **Mod:** vanilla, bug-fixed by `Goon's Wizard Overhaul` (`17659`)
- **Mechanics:** **L2** *Portent* — two random Portent dice after each long rest; spend a
  **reaction** to replace an attack roll or saving throw made near you with a Portent die.
  **L6** *Expert Divination* — a third die, plus **Prophecies on short rest** that refund spent
  dice (Goon's mod fixes the missing `Divination_Ally_Downed` prophecy). **L10** *Third Eye:
  Darkvision* and *See Invisibility*, both usable simultaneously.
- **Duo relevance:** Portent is a reaction, and Lone Wolf gives you a **second reaction** — the
  dice are effectively a pool of guaranteed enemy-save-failures or guaranteed enemy misses.
  With only two characters, converting one boss save into a failure is often the whole fight.
  Expert Divination's short-rest refunds fit Listo's long-rest tax better than most.
- `Expansion's changelog adds Greater Portent at 14 (see "Uncertain" below).`

### Enchantment
- **Mod:** vanilla + **`Hypnotic Gaze Breaks Concentration`** (`22655`)
- **Mechanics:** **L2** *Hypnotic Gaze* — charm + incapacitate one creature, maintainable each
  turn (long-rest recharge). **L6** *Instinctive Charm* — charm an enemy attacking you so it
  retargets. **L10** *Split Enchantment* — Enchantment spells that target 1 creature target 2.
- **Listo change:** `22655` makes **Hypnotic Gaze break the target's Concentration** when
  applied, per tabletop. The mod page is explicit that it does **not** break yours.
- **Duo relevance:** single-target lockdown plus a concentration-strip is a two-for-one against
  enemy casters, and Split Enchantment doubles Hold Person / Dominate at exactly the level
  encounters start fielding pairs of dangerous bodies. Instinctive Charm is another use for the
  spare Lone Wolf reaction. Weakness: Listo enemies are far more save-capable than vanilla and
  bosses have magic resistance (see `3-GameBalance.md`).

### Evocation
- **Mod:** vanilla, extended by `Expansion` (`279`)
- **Mechanics:** **L2** *Sculpt Spells* — allies **automatically succeed** their saves against
  your Evocation spells and take no damage. **L6** *Potent Cantrip* — cantrips deal half damage
  on a successful save. **L10** *Empowered Evocation* — add **Intelligence modifier** to damage
  rolls of Evocation spells. **L14 (Expansion)** *Overchannel* — an interrupt that maximises
  the damage of an Evocation spell of level **1-5**, with **necrotic backlash of 2d12 / 1d12**
  (`Interrupt_Overchannel`, read from `Passive_Expansion.txt`).
- **Duo relevance:** the safe default. Sculpt Spells matters more with two characters than with
  four, because in a two-body party your partner is *always* inside your own fireball. Highest
  raw damage per slot in the class, and the least dependent on enemy saves.

### Illusion
- **Mod:** vanilla, bug-fixed by `Goon's Wizard Overhaul` (`17659`)
- **Mechanics:** **L2** *Improved Minor Illusion* — cast Minor Illusion as a **bonus action**
  (Goon fixes its self-referencing tooltip). **L6** *See Invisibility* (short-rest recharge).
  **L10** *Illusory Self* — interpose an illusory duplicate to **make one attack miss**.
- **Duo relevance:** the thinnest of the base schools here. Illusory Self is a genuine "don't
  die" button on a d6 chassis, but a once-per-rest miss is a small return next to Arcane Ward or
  Bladesong, and Listo's enemy overhaul makes Minor Illusion's pull far less reliable than in
  vanilla.

### Necromancy
- **Mod:** vanilla, plus **`Animate Dead Plus Plus`** (`642`), **`Undead Thralls Fix`**
  (`15033`), **`Necromancy Heals Undead`** (`12666`), `Valkrana's Spellbook` (`1258`),
  `Valkrana's Skeleton Emporium` (`5808`), `Valkrana's Skeleton Crew` (`4496`)
- **Mechanics (vanilla):** **L2** *Grim Harvest* — on killing with a spell, heal 2× the slot
  level (3× for a Necromancy spell; not from undead/constructs). **L6** *Undead Thralls* —
  free Animate Dead, **one extra corpse**, and your undead gain **+wizard-level HP and your
  proficiency bonus to damage**. **L10** *Inured to Undeath* — **necrotic resistance** and your
  **hit-point maximum cannot be reduced**.
- **Mechanics (Animate Dead++, from the mod page):** Animate Dead supports **5th-level and
  higher upcasting with two additional undead per slot**; the **cap on how many undead you can
  have is removed entirely** ("as many undead as your spell slots allow"); no corpse required
  by default (toggle); Skeletal Wizard added as an upcast option; **undead benefit from short
  rests** and can be healed by ordinary healing; Undead Thralls' HP/damage bonuses now apply to
  **all** of the necromancer's undead, not just Animate Dead's; and the **free Animate Dead
  arrives at level 5 instead of 6**. `Undead Thralls Fix` repairs the additional-undead grant,
  which is broken in the base game.
- **Duo relevance:** **the single best answer to the action-economy problem in the entire
  list.** Two players against encounters tuned for five is solved most directly by fielding
  four to eight extra bodies, and Listo's necromancy stack is built to allow exactly that,
  scaling with the 7th-9th level slots Expansion hands out. Inured to Undeath also blanks the
  max-HP-reduction effects Listo's undead-heavy Act 2 leans on. Costs: heavy turn-time, and the
  bodies are long-rest-bound (though `Necromancy Heals Undead` lets Inflict Wounds/Harm/Circle
  of Death top them up mid-fight).
- `Expansion's changelog adds Command Undead at 14 (see "Uncertain" below). The standalone
  Command Undead mod is NOT in the 10.2 list.`

### Transmutation
- **Mod:** vanilla
- **Mechanics:** **L2** *Experimental Alchemy* — brew **two** alchemical solutions instead of
  one on a DC 15 Medicine check. **L6** *Transmuter's Stone* — one at a time, re-made after
  casting a Transmutation spell of 1st level or higher or a long rest; variants grant
  **Constitution save proficiency**, darkvision 18 m, +3 m movement, or a damage resistance.
  **L10** *Shapechanger* — turn into a flying blue jay.
- **Duo relevance:** the Constitution-save Transmuter's Stone is the cheapest concentration
  insurance in the class, and it can be handed to **the other player** — one of very few
  cross-character buffs a Wizard can just leave equipped. Note **Experimental Alchemy does not
  stack** with the Artificer's or any feat source (`4-SpellsFeatsClassesItems.md`), and the
  feat version was **removed in v9.0.3** (see `listo-10.2-feats.md`).

---

### War Magic
- **Mod:** `Book of Wizards - 5e Wizard Subclasses (Nexus Version)` (`18653`)
- **File pulled:** `Book of Wizards - Nexus and Expansion Version-18653-1-0-0-5-1761596222.zip`
  → `BookOfWizards_NexusVersion.pak`. **This is the current version (1.0.0.5)** and it is the
  variant built for **`5e Spells` + Advanced Tabletop Spells + `Expansion`** — all three are in
  the list, so spell selection past level 12 works. (Nexus lists `Expansion` as a requirement
  "only if you play past level 12".)
- **Mechanics:** Xanathar's War Magic, adapted. Confirmed from the mod page: the level-2 and
  level-6 features have **optional homebrew variants you enable as toggleable passives**;
  **Dispel Magic does not exist in BG3, so War Magic's dispel-flavoured feature uses Remove
  Curse instead**; the level-14 *Deflecting Shroud* had its **range shrunk to affect all
  targets within the radius** rather than three chosen targets within 18 m.
  `(The per-level feature table on the mod page is images-only; the specific numbers for Arcane
  Deflection / Tactical Wit / Power Surge / Durable Magic are unverified.)`
- **Duo relevance:** the gish-flavoured caster that is **not** Bladesinging — War Magic's
  identity is a reaction-based AC/save spike plus initiative, which pairs with the extra Lone
  Wolf reaction. Verify the actual numbers in the character sheet before building around it.

### Order of Scribes
- **Mod:** `Book of Wizards - 5e Wizard Subclasses (Nexus Version)` (`18653`) — same pak
- **Mechanics:** Tasha's Order of Scribes, heavily homebrewed to work without Script Extender.
  Confirmed from the mod page and changelog: you summon a **Spectral Mind** and **can cast
  spells through it**; spell-type transmutation is replaced by **Formulaic Attunement** —
  spells of your attuned damage type **ignore resistance to that type and deal a little extra
  damage**, and **attunement cannot be changed during combat** (v1.0.0.4 added the *physical*
  damage types, v1.0.0.5 fixed their boosts). The **level-10** feature is a once-per-long-rest
  stripped-down **Arcane Battery** (free casting of one spell). **Level 14** *One With The
  Word* prevents damage **once per long rest, only while your Spectral Mind is summoned**.
  `(Levels for Wizardly Quill / Awakened Spellbook and the exact Formulaic Attunement bonus are
  unverified — the tables on the mod page are images.)`
- **Duo relevance:** Formulaic Attunement is the list's cleanest answer to **resistance**,
  which Listo's Combat Extender hands out liberally to bosses — and a caster who can ignore it
  keeps working in fights where a mono-element Evoker stalls. The Spectral Mind is also a
  **remote casting position**, which is a real survivability tool when there is no third body
  to body-block for you.

### Hexcraft
- **Mod:** `Hexcraft - Wizard Subclass` (`10196`)
- **File pulled:** `Hexcraft - Wizard Subclass-10196-2-01-1731426557.zip` (current 2.01, main
  file; the level-12 patch was not pulled). Requires **Compatibility Framework** and
  **Expansion** — both present.
- **Mechanics (all from the mod page):** **L2** you may **copy Warlock spells into your
  spellbook** from scrolls and other spellbooks and they count as Wizard spells; one of the
  spells you learn each level **must** be from the Warlock list. **L2** also: learn **two
  Eldritch Invocations** from the Warlock list, **+1 more at 6, 10 and 14** — any invocation,
  unrestricted by pact (**taking a pact invocation does not grant the pact**, and invocations
  **cannot be changed** once picked). **L6** finishing a **ritual** cast grants temporary hit
  points equal to *ritual spell level + wizard level*. **L10** **immunity to all
  emotion-altering conditions** (charm/fear line). **L14** *Heart of Darkness* — when you kill
  with a 1st-level-or-higher Wizard spell, **spend a reaction to regain a spell slot one level
  below the spell's base level, max 5th**; uses = **Intelligence modifier**, refreshed on long
  rest.
- **Duo relevance:** the **slot-economy** school, which is the thing that most limits a Wizard
  in a 120-supply-per-long-rest game. It also stacks unusually well with two documented Listo
  facts: **Ritual Caster in Listo teaches you *every* ritual on the list** (`listo-10.2-feats.md`)
  — feeding Hexcraft's level-6 temp-HP engine constantly — and invocation access can buy
  Agonising Blast/Devil's Sight-tier passives on an Intelligence chassis. Level-10 charm/fear
  immunity is worth a great deal when losing either character ends the run.

### Hierophant
- **Mod:** `Hierophant - Wizard Subclass` (`7859`)
- **Files pulled:** `Hierophant 1.6.0-7859-1-6-0-1763655792.zip` **and** the optional
  `Hierophant - 5e Spells Compatibility 1.6.0` — both current, both installed as paks. Its
  dependencies `Spells Extra - DND 5E Library` (`11291`) and `AdvancedTabletopSpells` (`14429`)
  are present. Has **native progression to 20** without Expansion, and carries the **Cleric tag
  for dialogue**.
- **Mechanics (from the mod page's implementation notes):** **L2** *Divine Scribe* — one
  **Cleric cantrip**, plus always-prepared spells at fixed levels: **Guiding Bolt (2), Lesser
  Restoration (3), Mass Healing Word (5), Guardian of Faith (7), Greater Restoration (9)** —
  all count as Wizard spells for you. **L2** *Erudite Remedy* — a pool of **d6 equal to your
  wizard level**; as a **bonus action** heal a creature within 18 m for the dice spent, and the
  target gains **one damage resistance of your choice per die spent** until the start of your
  next turn (choose from the 10 elemental types). Dice spendable at once: **1 at L2, +1 every
  2 levels** (2 at 4 … 9 at 18). Refreshes on **long rest**. **L5** *Cantrip Formulas* (swap a
  cantrip on level-up) and *Divine Arcana*, implemented as spell-list additions: **Sacred Flame,
  Word of Radiance** cantrips and **Inflict Wounds, Spirit Guardians, Flame Strike, Harm**.
  **L6** *Turn the Otherworldly* — 9 m Wisdom save vs your DC to turn Celestials, Fiends or
  Undead for 1 minute; **short-rest** recharge. **L10** *Miracleworker* — **Dispel Evil and
  Good, Planar Binding and Raise Dead** added, each as a **ritual**. **L14** *Warding
  Rejuvenation* — a manual cast on a **downed companion** within 30 m: heal **4d6 + your
  Intelligence modifier**; short- or long-rest recharge.
- **Duo relevance:** **the healer answer for a party with no cleric.** In a two-person run the
  fight-ending event is one character going down, and Hierophant is the only Wizard that both
  **raises a downed ally** (L14, and Raise Dead at 10) and hands out **on-demand elemental
  resistance** as a bonus action — resistance you can pre-apply to *the other player* before a
  known damage type lands. Spirit Guardians on an Intelligence caster is a real damage floor,
  and Turn the Otherworldly is short-rest.

### School of Death
- **Mod:** `School of Death - Wizard Subclass` (`20302`)
- **File pulled:** `School of Death - Wizard Subclass-20302-1-00-00-1766630817.zip` (current
  1.00.00) → `School of Death.pak`
- **Mechanics (from the mod page):** **L2** *Reaper* — your **necromancy cantrips that target
  one creature target an additional creature** (the page recommends `Animate Dead++` for Reaper
  fixes — it is in the list). **L6** *Inescapable Destruction* — **your damage ignores necrotic
  resistance**; *Touch of Death* — when you damage a creature with a spell you may spend **two
  Arcane Recovery charges** to add **5 + twice your wizard level** necrotic damage. **L10**
  *Negative Energy Infusion* — once per turn, **+1d8 necrotic** on a spell attack hit, rising
  to **2d8 at 14**. **L14** *Improved Reaper* — 1st-to-5th-level necromancy spells that target
  one creature target an additional creature within ~2 m; **explicitly requires `Expansion`**,
  which Listo has.
- **Duo relevance:** the highest sustained single-target damage of the schools here, and the
  only one that turns **Arcane Recovery charges into damage** — a meaningful trade when the
  slots those charges buy back are long-rest slots anyway. Doubling necrotic cantrips scales
  with cantrip-boosting gear, and ignoring necrotic resistance covers this list's most commonly
  resisted damage type. It gives **no defensive layer at all**, so pair it with Bladesong-tier
  gear or a dip.

### School of Bombardment
- **Mod:** `(DTO) Otherworldy Archetypes` (`21822`)
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67 2026-06-17T17-15Z PYJWETtYB.zip`
  (current 1.2.0.67) → `DaelensTestament_c714f127-6475-4e82-1816-3922fc220bee.pak`. The pack's
  twelve subclasses cover every class and are **fully featured to level 20**; the Wizard entry
  is School of Bombardment. `5e Spells` (present) is recommended by the author.
- **Mechanics:** *"Rather than be limited by incantations, you discover a method to transform
  your magic energy into ordnance and lay siege to your foes from afar."* **The per-level
  feature list is published only as images on the mod page and the mod.io mirror is
  JavaScript-gated — every mechanic is `(unverified)`.** Read it in the level-up screen before
  committing.
- **Duo relevance:** unknown until verified. Flagged here so the skill knows a **twelfth
  Wizard-usable school exists** rather than silently omitting it.

---

## Dip value

**Dipping *into* Wizard.**

- **Wizard 1** — no armour, no weapon, no skill proficiencies (multiclassing into Wizard grants
  **nothing**), no saving throws. You get Int-based spellcasting, 3 cantrips, and **Arcane
  Recovery with 1 charge**, plus the **ability to transcribe Wizard scrolls** — which is the
  real reason to do it, since it converts Listo's abundant scroll drops into a permanent,
  slot-castable library on any Int-primary character (Eldritch Knight, Arcane Trickster,
  Artificer). Weak on its own.
- **Wizard 2 → Bladesinging** — **the one dip worth planning around.** Two levels buy **light
  armour proficiency, Performance, six martial-adjacent weapon proficiencies, and Bladesong
  (+2 AC, +2 Constitution saves, +3 m movement, advantage on Acrobatics, 2/long rest)**. For
  any Intelligence-based character that would otherwise be in a robe, that is the cheapest AC
  **and concentration** package in the list — and per `listo-10.2-equipment.md`, better caster
  armour is never going to arrive. Costs: no shields while singing, and you must hold one of
  the listed weapons.
- **Wizard 2 → Abjuration** is much weaker as a dip than it looks: Arcane Ward resets to
  *wizard level* and caps at *2× wizard level*, so at Wizard 2 it is a 4-point shield.
- **Wizard 3** is feat-neutral (feats key off class level, 3/6/9/12/15/18) but buys only
  2nd-level slots.

**Dipping *out of* Wizard.** Expensive. You give up caster level 1-for-1, and Listo's Wizard
payoffs are back-loaded — **Spell Mastery at 18** and **Signature Spells at 20** are the two
largest power spikes in the class and both sit past the point where any dip has to be repaid.
The defensible exceptions are cases where the dip fixes the chassis: **Cleric 1** or
**Fighter 1** for armour and shields (taken at *character* level 1 if you also want the saves
and heavy armour), or **Warlock 2** for short-rest slots — worth weighing precisely because
Wizard slots refuel only on the **120+ supply** long rest, while Warlock's refuel on short
rests. Remember **only the level-1 class grants saving throw proficiencies**, so taking Wizard
at level 1 is what buys the Int/Wis pair.

---

## Not present

- **Hedge Mage** — **removed in v9.0.3** (changelog #58: *"REMOVED Hedge Mage and Graviturgy
  from Wizard"*; the earlier v6-era entry reads *"REMOVED Hedge Mage because Havs's mods don't
  play well together"*). Confirmed absent from the 10.2 TSV and manifest.
- **Graviturgy Magic** — **removed in v9.0.3**, same entry. Absent from the TSV and manifest.
  *(Only `Compatibility Framework Patch for havsglimt's Subclasses` (`17062`) survives as an
  orphaned patch — it is not a subclass source.)*
- **Chronurgy Magic, Lore Mastery, Theurgy** — never in the list; no changelog entry, no TSV row.
- **Valkrana's Necrobroker** (wizard subclass, linked from School of Death's page) — not in the
  list.
- **The standalone Expansion "Bladesinger" mod** — the optional file exists on Nexus but was
  **not** pulled, and is not needed: Bladesinging is a base-game subclass in Patch 8. If you saw
  a second Bladesinger subclass in an older Listo, that was the pre-Patch-8 mod, removed in
  **v5.0** (*"REMOVED subclass mods that now have official subclasses"*).
- **Goon's "Bladesinger War Magic"** optional file — not pulled; Bladesingers do **not** get War
  Magic at 6.
- **Command Undead** (standalone mod) — not in the list.
- **Arcanist Feat** and **Experimental Alchemy as a Feat** — removed in v9.0.3; see
  `listo-10.2-feats.md`. The docs page still describes the Arcanist Feat; it is gone.
- **More Wizard RP Items** — removed. **Wands and Weave - Wizard Equipment** is not in the 10.2
  TSV. **Secret Scrolls** was removed in v10.0.

### Uncertain — verify in game

- **Durable Summons (Conjuration 14), Greater Portent (Divination 14), Command Undead
  (Necromancy 14).** Expansion's Nexus changelog says these were added in **1.7.1.0** (the first
  two) and **~1.4.x** (the third) — both **before** the 1.7.3.6 archive Listo pulled — but they
  are **absent from the author's public GitHub source** for the current build (no entry in
  `Progressions.lsx` or `Passive_Expansion.txt`). Either the repo lags the released paks or the
  features were dropped. **Treat as probable but unconfirmed.**
- **Listo's Expansion MCM profile.** Listo ships
  `SE_CONFIG\BG3MCM\Profiles\Default\Expansion\settings.json`, whose contents are not readable
  from the manifest. That file governs Cantrip Formulas, the Expansion-Bladesinger swap, Song
  of Victory's level, **Epic Boons at 20**, and Expansion's own extra-feat settings — so the
  ASI flags at 16/19 in Expansion's progression table may or may not be live alongside Listo's
  3/6/9/12/15/18 cadence.
- **School of Bombardment's entire feature set** (see above).
- **Book of Wizards' per-level tables** for War Magic and Order of Scribes (images only).
- **Whether scroll transcription cost is modified** by any Listo patch — the 50 gp/level
  (25 gp/level with the matching Savant) figures are vanilla; the **4× merchant markup on
  buying the scrolls themselves is confirmed** (`3-GameBalance.md`).

---

## Cross-references, not restated here

- **Feats** — `listo-10.2-feats.md`. Wizard-relevant highlights already documented there:
  **Ritual Caster** teaches **all** rituals rather than 3 (via the Feats Overhaul ListoPatch);
  **Spell Sniper** grants a free cantrip plus a **stacking −1 crit threshold** and advantage on
  damage dice for attack-roll spells (first hit only); **Magic Initiate** spells cost a slot but
  grant a 1st-level slot and use **your** spellcasting ability; the **ability-score cap of 20 is
  gone** for feat-granted increases.
- **Equipment** — `listo-10.2-equipment.md`. **Caster gear is robe-shaped**; **Arcane Acuity is
  capped at 3 stacks, combat-only and triggers on weapon attacks**, which voids every published
  Acuity-caster guide; `Bladesong Garment` (`5452`) is gish gear **restricted to female slim
  body types**; the **Potent Robe** requires Alfira alive.
- **Rest and economy** — `references/listo-rules.md` and `3-GameBalance.md`: 120+ supplies per
  long rest scaling with **camp population**, merchants at **4× buy / ¼ sell**.
