# Listonomicon 10.2 — Equipment

Every equipment source in the shipped 10.2 list: what it adds or changes, and where the
notable items come from. **Grep this file; don't read it whole.**

```bash
S=~/.claude/skills/listo-build     # or the plugin path

grep -i -B2 -A4 "shield" "$S/data/listo-10.2-equipment.md"      # by slot
grep -i "Act 1\|tutorial chest" "$S/data/listo-10.2-equipment.md"  # by availability
grep -i -A8 "^## Attunement" "$S/data/listo-10.2-equipment.md"     # the equip constraint
grep -i "upgrade" "$S/data/listo-10.2-equipment.md"                # upgrade paths
```

**Provenance.** Compiled 17 August 2026 against the bundled 10.2 snapshot. Every mod named
here was confirmed present in `listo-10.2-mods.tsv`; file variants were checked in
`listo-10.2-manifest.json` where it mattered. Item effects and drop locations come from the
mod pages on Nexus, which describe each mod's **current** version — Listo may have pulled an
older archive. Treat specific numbers as strong leads, not guarantees, and confirm anything
load-bearing in-game. Unverified claims are marked `(unverified)`.

**Cosmetic-only mods are deliberately excluded** — the list carries a large number of
appearance, dye, hair, and outfit mods with no mechanical effect. This file covers only gear
that changes a build.

---

## The two constraints that govern all gear planning

### Attunement (And Rarity Limits) — `14576`

The reason you cannot simply wear everything you find.

- Items requiring attunement, or falling under a configured **Rarity** limit, are given a
  **UseCost** against a custom Action Resource — the same mechanism as spending an Action.
- The resource is **restored when you unequip** the item (including on being disarmed).
- Out of resource means **you cannot equip the item** until you free one up.
- **No short-rest requirement** to attune — you can swap freely, whenever.
- Limits are configurable **per difficulty setting**, and can be set by slot or in total,
  separately for Rare / VeryRare / Legendary. Items granting Statuses, Passives, or Boosts at
  or above the configured rarity threshold **auto-require attunement**.
- MCM/IMGUI interface; requires ImpUI for the resource icons.

**Listo's shipped caps, read out of `Attunement/config.json` — identical across all five
difficulty entries, so difficulty does not change them:**

| Total attuned | Legendary | VeryRare | Rare | Uncommon |
|---|---|---|---|---|
| **5** | 3 | 5 | 6 | 13 |

Per-rarity slot sub-caps: Legendary 2 Armor / 2 Weapons / 2 Accessories; VeryRare 3/3/3;
Rare 4/4/4; Uncommon 6/5/5. `attunementRarityThreshold` is **Legendary**, so items at Legendary
or above auto-require attunement — plus 413 explicit item overrides and 946 rarity overrides.

> **Plan against five attuned items, at most three Legendary.** A `relaxed config.json` (6 total,
> 4 Legendary) also ships but is not the live file — only ask the player if they swapped it in.
> Full dump in `data/listo-10.2-mcm.md`.

### The economy — from docs page 4

- **4× merchant prices** and reduced sell values; gold accumulates slowly (Poor
  Adventurer-style changes plus custom difficulty settings).
- You will find **far more magic items** than in vanilla, so selling unused gear still funds
  a lot.
- Design intent is **fewer best-in-slot answers** and **more frequent swapping** — plan a kit,
  not a single endgame set.
- Hold a **spread of damage types**; some encounters reward or punish weapon choice.
- **Withers is a merchant** with 50,000 gold that resets each conversation — the trash-dump
  of choice. He carries dyes and camp clothes (moved off normal vendors). Cannot be
  pickpocketed. (`Trade with Withers`, present in list.)

> **`Random Equipment Loot` is NOT in the 10.2 list.** The docs still describe it as an
> optional mod near the bottom of MO2, and the skill's own process step still tells you to ask
> about it — but it is **absent from both `listo-10.2-mods.tsv` and the manifest**, including
> the non-Nexus archives. The v10.0 changelog shows a related mod ("A Human's Random Loot")
> considered and struck out. The changelog's most recent substantive REL entries are from the
> v7.x era, and an older entry records it being removed for incompatibility with too many Listo
> mods.
>
> So: **gear locations in this file are reliable by default.** Still worth one question to the
> player, since a user can add it manually and it would void every location here — but treat
> its presence as the exception, not the expectation.

---

## New equipment slot — JWL Discordant Instruments (`9119`)

Converts the near-useless **Musical Instrument** slot into a **Trinket** slot, with **100+
new items**. Effectively a third ring slot for every character. Requires Script Extender;
distributes via SE, so items appear even on already-looted containers. Enemies equip trinkets
too. Includes class-restricted items (holy symbols for Clerics/Paladins) and keeps **Perform**
meaningful for Bards.

> Free power for both characters in a duo — this slot is otherwise dead weight on a non-Bard.
> Also a dependency: Degreaser's **Rolan's Stolen Spellbook** requires JWL trinkets. Listo also
> pulls a **`Grit and Glory - JWL Discordant Instruments Patch`** — a patch file shipped under
> `Grit and Glory - Injuries Exhaustion and Madness` (`14863`) — so the trinket slot is
> reconciled with the injuries/exhaustion system.

**Version caveat:** Listo pulled **`JWL Discordant Instruments-9119-1-2-0-0`**, an archive from
May 2024. The location table below is from the mod's **current** Nexus page, so later-added
trinkets may not exist in the installed version, and some listed here may have moved. Treat it
as a strong lead, not a guarantee — this is the least version-stable table in this file.

Documented locations (partial list, from the mod page):

| Trinket | Where |
|---|---|
| Annotated Map of the Sword Coast | Most vendors |
| Fashionable Backpack | Most vendors |
| Balance of Harmony | Dowry chest |
| Belt of Primal Recall | Flind |
| Brambleheart Quiver | Arron |
| Triage Kit | Arron |
| Decanter of Endless Mead | Mattis (Act 1) |
| Rope of Mending / Wind Fan | Mattis (Act 2) |
| Shoulder-Mounted Leather Frog, Steel Crowbar | Dammon (Act 1) |
| Portable Whetstone, Soulbound Chain | Dammon (Act 2) |
| Galder's Bubble Pipe | Harpy stash |
| Pole of Collapsing | Filro the Forgotten |
| Witch's Whistle | Hag lair chest (Act 1) |
| Belt of Dwarvenkind | Gekh Coal |
| Candle of Lawful Invocation | Pooldripp the Zealous |
| Docent | Bernard |
| Efficient Quiver | Harper/Gith Quartermaster |
| Shielding Brooch | Gith Quartermaster |
| Houndmaster's Whistle | Gomwick's corpse |
| Hourglass of Distorted Perception | Brewer's Buried Stash |
| Lens of Astute Observation | Family Ring burrow |
| Mourningsteel Obol | Bulette |
| Pearl of Power | Dhourn |
| Professor Orb | The Sparkswall chest |
| Ruby of the Warmage | Xargrim's corpse |
| Badge of the Watch, Harbin's Lucky Die | Sticky Dondo |
| Belt of Frost Giant Strength | Kith'rak Therezzyn |
| Belt of the Raid Leader | Gloomy Fentonson |
| Bowl of Commanding Water | Sorcerous Sundries |
| Cowardly Magic Carpet | Holy Lance Helm chest |
| Eyes of Charming | Popper |
| Handy Haversack | Reithwyn Morgue harper corpse |
| Mimir | Astral Sea potion sack (before Baldur's Gate) |
| Quiver of Elemental Chaos | Lann Tarv |
| Sea Serpent's Pin | Allandra Grey |
| Silver Lycan Charm | Yurgir |
| Thayan Femur | Balthazar |
| Worghide Leather Frog | Prelate Lir'i'c |
| Bag of Holding | Sundries Vault (Elminster) |
| Belt of Forbidden Harmony | House of Hope hidden treasure pile |
| Black Crystal Tablet | Mystic Carrion (purchase) |

---

## Listo's own items — Degreaser 2.0 (`15258`)

`Degreaser 2.0 - new equipment and creature rebalances` is **Ajax's own mod**, split out of
the older all-in-one "Ajax's Degreaser" so that standalone content and Listo-specific patches
are separate. It fills deliberate capability gaps for Listo players — these are the items
most likely to be *designed for* a build here.

Requires Goon's Passive Library, 5e Spells, PF2e Spells, and the Artificer mod (for guns).

| Item | Type | Where |
|---|---|---|
| **Mantle of Ajax** | Cloak | Sold by **Volo**. Ignore enemy acid and poison resistance; gain it yourself. |
| **Shield of Spell Reflection** | Shield | Sold by **Popper**. Flail Snail shell — effectively grants the **Mage Slayer feat**, so Listo's Mage Slayer changes apply to it. |
| **Grand Exchange** | Scimitar (rune) | Alchemist merchant in **Moonrise**. |
| **Swollentoe's Cloak of Protection** | Cloak | **Ironhand gnomes, Act 3** (if still alive). Improved Cloak of Protection. |
| **Jarlaxle's Piwafwi** | Cloak | Lost-and-found of a bar in **Baldur's Gate**. Cloak of Elvenkind-like. |
| **Cloak of Supreme Defenses** | Cloak | **Danthelon's Dancing Axe**. |
| **Moghadam** | Sword | The **Penitent** outside the Murder Tribunal. |
| **Flamepearl's Greataxe** | Greataxe | Dwarf weapon merchant near **Sorcerous Sundries**. Adamantium meteorite. |
| **Resplendent Scimitar** | Scimitar | **Devil's Fee**. Fire + radiant. |
| **Censor of Orcus** | Mace | Sold by **Carrion**. Empowers necromancy. |
| **Galloway's Goggles of True Sight** | Goggles | Dropped by **Grym**. |
| **Gloves of Gecko Grip** | Gloves | **Dammon at the Grove**. |
| **Armor of the Bear** | Armour | Sold by **Aaron**. Undocumented **1/short rest disarm** ability (not on the tooltip). |
| **Adamantine Bow** | Bow | On **mimics**, somewhere underground. |
| **Devilstring Bow** | Bow | Sold by **duergar**. |
| **Sussurstring Bow** | Bow | Workshop of the Sussur-obsessed. |
| **Rolan's Stolen Spellbook** | — | Book merchant near Rolan's Act 3 destination. **Requires JWL trinkets.** |

"And more" — the mod page does not enumerate everything.

Degreaser also adds Combat Extender NPC spells and passives (`NPC_SummonGildedHellsboar`,
`NPC_HellfireOrb`, `NPC_FleshToGold`, `NPC_ParalyzingRay`, `NPC_CircleOfDeath`, and others).
These only fire if assigned in a CX config — they affect what you *face*, not what you wear.

---

## Vanilla items reworked

> **Do not quote vanilla item numbers from memory or from outside sources.** Between
> `Degreaser 2.0`, the `Gear Revised` trio, `Elixirs Revised`, `Hardcore Healing Potions`, and
> the individual item mods below, a large share of vanilla magic items have different numbers
> here. Confirm any specific value before a build leans on it.

### Gear Revised — footwear, rings, shields
Three mods from one author's "Revised" series: `Gear Revised Footwear` (`10893`),
`Gear Revised Rings` (`13925`), `Gear Revised Shields` (`10984`). Reworks and QoL tweaks to
**vanilla** items in those slots — items added, removed, and rebalanced.

> **Only these three of the series are in Listo** (plus `Elixirs Revised` separately). The
> author's Headwear/Amulets/Cloaks/Armors/Clothing/Handwear/Weapons Revised mods are **not**
> in the list — do not assume the whole series applies. The author notes the balance is tuned
> for "high difficulty of combat," which suits Listo.

### Individual vanilla item reworks

| Item | Mod | Change |
|---|---|---|
| **The Blood of Lathander** | `16436` | Mace → **morningstar**. |
| **Markoheshkir** | `15396` | Adds **Radiant and Necrotic** Kereska's Favour variants; fixes vanilla bugs. |
| **Mourning Frost** | `18908` | New spell **Freezing Gust**; unique Ray of Frost variant; **Insidious Cold scales with Spell DC** (and is bug-fixed); immunity to ice slipping; **Arcane Enchantment +1**. |
| **Phalar Aluve** | `2987` | Two music boxes upgrade it to **+2 VeryRare**, then **+3 Legendary**. See upgrade paths. |
| **Duellist's Prerogative** | `17680` | Fixes and buffs. |
| **Sword of the Emperor** | `8700` | Buffed. |
| **Sword of Justice** | `23050` | Can be **upgraded twice**. |
| **Cruel Sting** | `19562` | Buffed. |
| **Wyll's Infernal Rapier** | `14369` | Brought in line with other companion story weapons. |
| **Dark Displacement Gloves** | `8198` | Subtle Swap passive redesigned as an **active ability**. |
| **Corellon's Grace** (quarterstaff) | `14238` | While wielded, you may use an **unarmed attack** in place of your weapon attack. Compatible with College of Dance. Adds **Corellon's Fist**. |
| **Ring of Feywild Sparks** | `15789` | **Removes the Tides of Chaos interaction**; raises baseline Wild Magic Surge chance; fixes a hidden Spell Save DC bonus. Pairs with `Tides of Chaos DnD 5R PHB2024`. |
| **Hr'a'cknir Bracers** | `5653` | `Luminous Hellrider's Belligerent Bracers` — **combines the passives of Hellrider's Pride, Luminous Gloves, and Gloves of Belligerent Skies onto one item**. |
| **Malus Thorm's Glasses** | `6130` | Reworked as **Goggles**, equippable in **Headwear or Cloak** slot; spells switch between over-eyes / forehead / neck. Requires SE. |
| **Bhaalist Armour** | `14890` | **Aura of Murder nerfed** — no longer applies Piercing **vulnerability**; instead melee weapon attacks deal **extra Piercing damage** to the target. Applies to Bhaalist enemies too. |
| **Ring of Exalted Marrow, Circlet of Bones** | `16842` | Ring gains **Control Undead**; new aura grants minions the **Alert feat** and **+Proficiency Bonus to saves**. Zombie Connor lasts until Long Rest; zombies can jump. Circlet of Bones aura matches regular spell range. |
| **Necromancy of Thay rewards** | `18949` | **Tharchiate Withering** goes straight to **Tharchiate Vigour** if you're curse-immune. **Tharchiate Codex: Blessing** now grants **half damage from all sources while you have temp HP** (stacks multiplicatively with resistance); as **undead**, +1 temp HP per turn and ignore damage below 4. **Festin Macabre** trades away Danse Macabre for **Necrotic Resurgence**. |
| **Poison gear** | `12413` | See the Poison package below. |

### The poison package — Better Poison Equipment (`12413`)

Both an equipment mod and a feat source (see `listo-10.2-feats.md` → Poison Adept).

- **NEW — Necromancer's Robe:** grants **Absorb Poison** (a reaction, like Absorb Elements)
  and the **Poison Adept** passive. **Dropped by Balthazar.** An upgrade of the (also
  upgraded) Poisoner's Robe. For **Warlocks, Absorb Poison restores 1 Warlock spell slot**
  instead.
- **NEW — Necromancer's Staff:** grants **Poison Wave** (Cone of Cold range). Viable melee
  weapon: **+1d4 poison damage** and can use **Lacerate** to bleed. Found in the chest in
  **Balthazar's Secret Room, Moonrise Towers** (same room as the Coldbrim Hat).
- **Poisoner's Glove:** new passive **Empowered Poison**.
- **Poisoner's Robe:** Poison Trails scales — **+1d4**, rising to **+1d6 at level 6** and
  **+1d8 at level 11**; also gains **Poison Adept**.
- **Necklace of Elemental Augmentation** and **Ring of Elemental Infusion** now include
  **Poison**.
- **Derivation Cloak:** healing on poisoning an enemy raised from **1d4 to 2d4**.
- **Poisoner's Ring — Virulent Venom rebalanced:** now **once per short rest**; DC scales with
  your **Spellcasting DC** (was fixed 14); targets a **small area** instead of 3 individual
  targets; range **9m → 6m**; duration **10 → 6 turns**.

---

## Arcane Acuity — the item mechanic that breaks published guides

`Arcane Acuity Rework` (`14595`). Per `references/listo-rules.md`, Arcane Acuity is
**capped at 3 stacks, gains 1 per trigger, is combat-only, cannot be pre-stacked**, and
**triggers on weapon attack rolls**.

> Vanilla Arcane Acuity stacking (Hat of Fire Acuity → Band of the Mystic Scoundrel loops) is
> the backbone of most published Swords Bard and Acuity-caster guides. **None of that works
> here.** Treat any build advice from outside Listo that leans on Acuity as void.

## Caster gear is robe-shaped

Per `references/listo-rules.md`: **no mod in the list adds medium armour with caster
benefits.** A caster in this list is wearing a robe, so plan AC from Shield, Mage Armour,
Warding Bond, or a dip that supplies armour proficiency — not from finding better caster
armour later.

Known caster sets and their gates:

- **Better End Game Caster Robe** (`10963`) — Robe of Archmage plus circlet, cloak, gloves,
  boots. **Gilded Chest, Illusion section of the Sorcerous Vault (Act 3).**
- **Robe of Vecna ReAwakened** (`17422`) — multi-act chain: read the **Compendium
  Maleficarum** and **deliberately fail** the Wisdom save, then cast **Extract Divine Undeath
  Essence** on Ketheric's Apostle form (**Act 2**).
- **Psychic Armory** (`14476`) — upgradeable set; **Sussur Bloom** from the **Arcane Tower
  basement**.
- **Bladesong Garment** (`5452`) — **restricted to female slim body types**
  (human/elf/half-elf/tiefling). A hard gate: check the character's body type before planning
  around it.

## Quest-gated items worth planning around

From `references/listo-rules.md`:

- **Potent Robe** (Charisma to cantrip damage) is **Alfira's reward, and she must be alive.**
  The Dark Urge kills her in a scripted scene — the only workaround is **knocking her out in
  Act 1**.
- **Hag's Hair** (+1 to an ability, one per run, Act 1) — a **DC 20** check gets the hair
  *and* saves Mayrina; fail and you must choose one.
- **Mirror of Loss** (Cloister of Sombre Embrace, Act 3) — **+2 to a chosen ability plus a
  separate +1 Charisma, per character**. Requires the **Night Orchid** from behind a breakable
  wall in the Armoury (past a passive check), then a Religion check. Whether it exceeds 20 is
  **unconfirmed**.
- **Tomes and Manuals** — +1 each, stack above 20.

## Named unique items added

Each of these mods is essentially one item — the mod name is the item name.

### Weapons

| Item | Mod | What it is |
|---|---|---|
| **Acheron Blade** | `13531` | From Explorer's Guide to Wildemount. |
| **Celestial Fury** | `14984` | The legendary **katana from Baldur's Gate II**, custom model, lore-based powers. |
| **Dawnbringer** | `23572` | Gilded longsword hilt found in the **Underdark**; bonus action to spring a blade of pure radiance. Has all properties of a **Sun Blade**. |
| **FoeBane** | `12523` | Lore-faithful FoeBane. **Reward in the Druid Grove questline**; upgradeable (see upgrade paths). **Optional mod** per the docs. |
| **Holy Avenger** | `7818` | From the 5e DMG. |
| **Ryujin Jakka** | `16334` | Fiery greatsword for mid/endgame; unique weapon action and a powerful burn. |
| **Sword of the Rising Dawn** | `13491` | Glowing **Finesse longsword**, Lathander-themed. |
| **Ghoul Touch Weaponry** | `15659` | Necrotic weapons with unique models, **plus a shield and monk gloves**. |
| **Way of Shadow Revised - Katanas** | `21534` | Adds **5 katanas**. |
| **More Better Scimitars** | `18033` | Scimitars with more advanced stats. |
| **Some Neat Amazing Crossbows (SNAC)** | `18649` | A pair of **VeryRare hand crossbows** that apply **Wet**, summon puddles, and deal lightning; plus **two Legendary "hand" crossbows** with unique effects. |
| **Wand of Wonder** | `20584` | Gamble-y wand; chaotic effects. |
| **Vera the Alchemist** | `17864` | A full **quest in Act 2 (Shadow-Cursed Lands)** that adds new **flask weapons**. |
| **Steel Watch Armaments** | `13364` | A **legendary weapon and helmet**, city-guard aesthetic. |

### Armour, clothing, and cloaks

| Item | Mod | What it is |
|---|---|---|
| **Bladesong Garment** | `5452` | Opulent clothes **and a weapon**, tuned for a **gish** — explicitly aimed at College of Swords Bard or Bladesinger. |
| **Vest of Investiture** | `13591` | Late-game clothing for **defensively deficient casters**. |
| **Better end game caster Robe** | `10963` | For when the Weave set isn't enough. |
| **Mantle of Holy Light** | `13157` | Unique cloak. Projects an **Orb of Holy Light** protecting from the **Shadow Curse**; **Healing Incense Aura 1/long rest**; **+2 to Death Saving Throws**. |
| **Barbarian of our Heart** | `13929` | **Two armour pieces** built around endurance/tanking, plus an **endgame greataxe** built on bleed. |
| **Ghaikskin Knight Armor** | `14727` | Armour set with hand-modeled helmet. **Tutorial chest as backup**; pieces intended to be found from **Githyanki sources** (author notes this is **untested**). |
| **Garb of the Ghustil** | `20262` | Githyanki-inspired outfit for all vanilla bodies. |
| **Robes and Armor of the Absolute** | `4143` | **Nere's** and **Z'rell's** robes and **The Warden's** armour, added to their loot **and the tutorial chest**. |
| **Gifts of the Absolute** | `11487` | More equipment for players carrying the **Brand of the Absolute**. |
| **Sheltering Steel** | `23041` | A variety of **heavy armours added to Act 1 vendors** — fills the early heavy-armour gap. |
| **Knights and Dames** | `8208` | Armour set. |
| **Harmony Habiliment** | `12650` | Rebuild of the author's earlier **bard** mod. |
| **Illithid Emporium** | `14860` | Improves existing and adds new equipment for **Illithid-focused** characters. |
| **Necrotic Armament and Curios** | `18790` | Options for **necrotic casters** along the journey. |
| **Lost Shipment - Equipment for Clawstep** | `16546` | Chest of armour, boots, camp clothes. Added to the **Player Chest** and the **tutorial chest**. |
| **Extra Gear** | `3483` | New armour and clothing (body-type restrictions — see mod images). |
| **Radiant Threads** | `20546` | Custom dresses. Largely cosmetic. |

### Shields

| Mod | What it adds |
|---|---|
| **Aitze's Shields** (`14756`) | Shields **based on various gods**; from a backpack in the **tutorial chest**. |
| **Extra Shields (Updated)** (`15393`) | **15 custom shields**, in balanced **and OP** versions `(unverified which variant Listo pulled)`. |
| **Shields of the Fallen** (`16412`) | **26 shields** from Lords of the Fallen, various styles. |
| **Lathander's Armory** (`4711`) | Shields, armour, and **books** for **Cleric/Paladin**. |
| **Helm's Armory** (`6345`) | **Shield and longsword** for **Paladin/Cleric**. |
| **Degreaser: Shield of Spell Reflection** | See Degreaser above — grants Mage Slayer. |

> Shields matter disproportionately here — the skill's own pitfall list flags that shield
> proficiency is often unobtainable without a specific feat or dip. Check the proficiency
> before planning around an AC number.

### Headwear, rings, and accessories

| Item | Mod | What it is |
|---|---|---|
| **Hats of Power** | `13337` | More magical hats, sold by the **Sorcerous Sundries** trader. |
| **More Helmets by Guigodead** | `12711` | Helmets. |
| **Corrosive Ring** | `10872` | **Acid build core item** — maximizes acid damage properties, accumulates **Corrosion**, melts enemy armour. |
| **Critfisher Ring** | `13425` | Legendary ring that **greatly reduces critical threshold**. |
| **Ring of Viciousness** | `20932` | Rare ring in **Act 2**; **critical hit threshold −1**. |
| **Weapon Earrings** | `18691` | **16 earrings** based on weapons. |
| **Goggles (with Variants)** | `6130` | See Malus Thorm's Glasses above. |
| **Cloaks of Faerun** | `2811` | Additional cloaks/capes. |
| **More Weapons by Guigodead** | `14913` | **40 new weapons** — Macuahuitl, hook swords, khopesh, daggers, javelins, warhammers — in the **tutorial chest**. |
| **Aitze's Swordtember Weapons** | `14755` | Weapon models from a Swordtember art challenge; **tutorial chest** backpack. |
| **Banite wretched armor** | `19249` | Sarevok armour retexture for Banites. Cosmetic. |
| **MAAM** | `18940` | **Mamzell Amira** now sells scrolls and items at **Sharess' Caress**. |
| **Distinctive Arrows of Slaying** | `20199` | Unique icons per Arrow of Slaying. QoL only. |

> **Two crit-threshold rings exist** (`Critfisher Ring`, `Ring of Viciousness`) plus
> **Deadly Alacrity** and **Duellist** from the feat side. Crit-fishing is unusually well
> supported in this list — worth checking stacking before building around it
> `(unverified whether these stack)`.

---

## Upgrade paths

A handful of items improve through found materials — worth planning around because they turn
an early pickup into an endgame weapon.

| Item | Path |
|---|---|
| **Phalar Aluve** (`2987`) | Music box hidden in the **Shadow-Cursed Lands (Act 2)** → **+2 VeryRare**. Second music box in a part of the **Circus only pickpockets can find (Act 3)** → **+3 Legendary**. **Variant pulled: `PhalarAluveLegendary SynergeticStrikes` v2.8** — not the plain file, so the Synergetic Strikes behaviour applies `(unverified what that variant changes)`. |
| **Psychic Armory** (`14476`) | A scavenger hunt and upgrade path in one. The **Sussur Bloom** from the **basement of the Arcane Tower** is the upgrade material. |
| **FoeBane** (`12523`) | Druid Grove questline reward → upgraded with a **magic scabbard in Act 3 (Jaheira's Basement)**. *(Optional mod.)* |
| **Sword of Justice** (`23050`) | Upgradeable **twice**. |
| **Robe of Vecna ReAwakened** (`17422`) | Upgradeable robe integrated into game events; built-in synergy with **Eye of Vecna, Hand of Vecna, Path of Undeath**, Deathsong, and Dread Overlord. SE not required. |

---

## Legendary artifacts

### The Hand and Eye of Vecna (`12600`, `12601`) — *optional mod*

The docs frame these as the **evil inverse of the Blood of Lathander**, more powerful when one
owner holds both, and carrying real risk — Vecna exerts influence through them and the gods
react badly.

- **Hand of Vecna** — grafts to your **right arm** (visuals). Sets **Strength to 20** if lower.
  Melee spell attacks made with it, and melee weapon attacks with a weapon it holds, deal
  **+2d8 cold**. **8 charges**, spent as an action to cast at **save DC 18**: Finger of Death
  (5), Sleep (1), Slow (2), Dimension Door (3).
- **Eye of Vecna** — grafts to your **right socket** (same visual as the Hag Eye).
  **Truesight** (see in darkness and see invisible to 24m) **+2 Perception**. Action to gain
  **Ring of X-Ray Vision** sight, ended as a bonus action. **8 charges**, save DC 18:
  Clairvoyance (2), Crown of Madness (1), Disintegrate (4), Dominate Monster `(charge cost
  not captured)`.

> A guaranteed **STR 20** from an item is a serious build lever — it frees a Lone Wolf +4 and
> a stat spread from carrying Strength at all. Weigh against the mod being **optional** and
> risk-laden; confirm it is enabled before building on it.

### Path of the Righteous (`16597`) and Path of Undeath (`9164`) — *optional*

Two long-form avatar-upgrade arcs. **Righteous** is the good-guy fantasy: collect relics and
complete quests, rituals, and castings to restore tarnished artifacts. **Undeath** is the
inverse: esoteric rituals leading to dying and rising as a master of undeath. Listo also ships
`Bloodtrail - Path of Undeath Chapter 2`.

> Path of Undeath interacts with the undead-specific clauses on the **Tharchiate Codex** and
> `Necromancy Heals Undead`. If a player is going undead, that whole cluster reinforces.

---

## Consumables and economy

| Mod | Effect |
|---|---|
| **Elixirs Revised** (`10073`) | Elixirs changed substantially — **many now stack or work differently**; read tooltips in-game. **Elixirs of Giant's Strength are now +STR items, not set-to-N potions** — so you **cannot dump STR and drink your way out of it**, and high-STR characters still benefit. |
| **Elixir Rebalance - Giant Strength and Battlemage Only** (`5838`) | Rebalances **Cloud Giant, Hill Giant, and Battlemage** elixirs specifically. |
| **Hardcore Healing Potions** (`15391`) | Healing potions give **limited immediate healing plus a delayed heal**, sharply reducing in-combat value. Explicit design goal: make **healers relevant** rather than "a guy with a good throwing arm." |
| **Wye Fey Potions** (`23323`) | Successor to WiFi Potions: **every party member gets a potion of each tier, linked to the party's total pool**. |
| **Better Potion of Everlasting Vigour** / **Stealable Potion of Everlasting Vigour** | Both in list — improves and makes stealable the +2 STR potion. |
| **Dynamic Camp Supply Cost** | Long rest cost scales with **camp population**, not active party — the mechanic behind the duo's rest-economy problem. |
| **Auto Send Food To Camp** | Food auto-routes to camp chest; MCM-configurable for alcohol and valuable food. |
| **Gold Weights Nothing** | QoL. |

> The healing-potion nerf plus the rest-economy penalty means a duo should weight **in-class
> healing** (and the **Battle Medic** feat) higher than a normal party would.

---

## Firearms vs bows

From docs page 4, implemented via the **Artificer** mod and the **Listo patch/Degreaser**:

- **Firearms** are generally **stronger than the equivalent bow/crossbow** in damage dice, but
  have **significantly reduced range**.
- **Hand crossbows** now have **similarly reduced range** — they can no longer compete with
  bows/crossbows on range, though they can still be **dual wielded**.
- A variety of **magic pistols** exist, from an unreleased mod Jasperthefae permitted Listo to
  use. **Basic and +1 firearms are sold by Dammon and Roah Moonglow in Acts 1 and 2**, with
  others scattered.

> Note the interaction with the feat side: **Crossbow Expert is renamed Bow Expert** and now
> covers **all bows**, and Feats Overhaul's author deliberately buffed bows toward crossbow
> parity. Range is the axis that separates the categories now, not raw damage.

---

## Optional mods that change gear planning

Confirm these before planning specifics:

- **Random Equipment Loot** — **not shipped in 10.2** (see above). If a player has added it
  manually it randomizes ~2,000 items and **voids every location in this file**; the docs also
  suggest dropping the price multiplier from 4× to 3.5× and checking every NPC's trade menu
  when using it.
- **The Hand and Eye of Vecna** — optional.
- **FoeBane** — optional per the docs.
- **Path of the Righteous / Path of Undeath** — optional.
- **Spelljammer** — the Act 3 ship arc; the **ship manifest/deed sold by Popper in the circus**
  is very expensive, so it's a gold sink to plan for. `Features from DnD 5E Spelljammer`
  (`13195`) adds backgrounds, goals, spells, items, and a bestiary.
- **Absolute Wrath**, extra-encounter mods — change the difficulty gear is measured against.
- **Illithid Powers Overhaul 2** (`5105`) — officially optional for being strong; makes
  Illithid powers very powerful in Act 3.
