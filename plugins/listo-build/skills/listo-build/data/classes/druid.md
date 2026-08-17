# Listonomicon 10.2 — Druid

Druid is one of the most heavily modified classes in Listo, but almost none of the change is
in the subclass list — it is in the chassis. Every Druid gets **Speak with Animals** always
prepared (and Listo makes it a party-wide AoE lasting until Long Rest), **Find Familiar** as an
always-prepared spell at level 2 plus **Flock of Familiars** from the Druid list, two purpose-built
summon spells (**Summon Beast** at 3, **Conjure Animals** at 5) that produce non-concentration
bodies lasting until Long Rest, and a **Shillelagh** that is no longer a cantrip but a level 1
spell lasting until Long Rest on any of seven weapon types. Wild Shape is a complete ground-up
overhaul. On top of that vanilla ships three circles (Land, Moon, Spores) plus Patch 8's Circle of
the Stars, and mods add seven more. The result is a class that is very good at exactly the thing a
two-person Lone Wolf party is worst at: putting extra bodies on the board.

**Provenance.** Compiled 17 August 2026 against the bundled 10.2 snapshot. Every circle below was
confirmed present in `listo-10.2-mods.tsv` or is vanilla; every file variant was confirmed in
`listo-10.2-manifest.json` (archive names and the installed `.pak` filenames). Mechanics come from
the mod pages, the Listo changelog, and bg3.wiki for vanilla baselines. **The Listo docs stop at
v10.0 and are wrong about Shillelagh** — see below. Anything not read is marked `(unverified)`.

---

## At a glance

| | |
|---|---|
| **Primary ability** | Wisdom (spellcasting, save DC, prepared-spell count = Druid level + WIS mod) |
| **Saves at level 1** | **Intelligence + Wisdom** — only granted if Druid is your *level 1* class |
| **Armour/weapons** | Light + Medium armour, Shields; Clubs, Daggers, Javelins, Maces, Quarterstaves, Scimitars, Sickles, Spears. *(Multiclass in: Light/Medium armour + Shields only.)* |
| **Hit points** | 8 + CON at 1, 5 + CON per level |
| **Skills (pick 2)** | Arcana, Animal Handling, Insight, Medicine, Nature, Perception, Religion, Survival |
| **Resource cadence** | Spell slots: **Long Rest**. Wild Shape charges: **2, Short Rest** (Moon: 2 per Short Rest, bonus action). Stars' Star Maps/Cosmic Omens: Long Rest — **Star Druid Tweaks moves Cosmic Omens to Short Rest**. Shillelagh, Summon Beast, Conjure Animals, Speak with Animals, Longstrider: cast once, **lasts until Long Rest**. |
| **Feats** | 3, 6, 9, 12, 15, 18 (Listo-wide; see `listo-10.2-feats.md`) |
| **Key breakpoints** | **1** Int+Wis saves, Shillelagh, Goodberry, Speak with Animals · **2** Wild Shape + circle + Find Familiar · **3** Summon Beast, Flock of Familiars · **5** Conjure Animals, Wild Strike/Extra Attack · **6** circle tier-2 + Wild Shape CR bump · **9** Moon CR3 forms · **10** Nature's Ward + circle capstone-ish |
| **Dip value** | **Very high at 1 and 2.** See the Dip section. |
| **Level 13–20** | Delivered by the `Expansion Level 13-20` pak (`Expansion.pak`, not a Nexus mod so not in the TSV). Modded circles advertise level 14 features and are built for it; **exact vanilla-circle progression at 13–20 is (unverified)**. |

---

## Class changes from vanilla

### Shillelagh — read this before building anything that uses it

**Both Listo doc pages disagree with each other, and `listo-10.2-feats.md` inherited the wrong
one.** `4-SpellsFeatsClassesItems.md` says Shillelagh "is a permanent effect"; `1-Home.md` and the
changelog say otherwise, and the changelog is newer and more specific. The current behaviour, from
changelog v9.0.3 item 70 (the most recent entry that restates the whole rule):

- **It is a level 1 spell, not a cantrip.** It costs a level 1 spell slot and a prepared-spell slot.
- **It lasts until Long Rest** — it "needs to be re-cast after a Long Rest." It is *not* permanent,
  but it is not the vanilla 10-turn buff either. One cast per adventuring day.
- **Applicable weapons: Club, Quarterstaff, Mace, Morningstar, Sickle, Spear, Trident.**
  (An earlier, v8-era list also had Glaives, Greatclubs, Javelins, Pikes and Warhammers; v9.0.3
  cut it back to the seven above. Halberds were removed even earlier.)
- **Added as a Nature Cleric domain spell and as an option for Oath of Ancients Paladins.**
- v10.0 item 99 fixed "Shillelagh being permanently stuck on gear and not working as intended" —
  i.e. the *bug* that made it look permanent is what got patched out.

Vanilla for contrast (bg3.wiki): cantrip, Bonus Action, **10 turns**, **Quarterstaff or Club only**,
1d8 + spellcasting modifier Bludgeoning, and it swaps Strength for your **highest** spellcasting
modifier on both attack and damage rolls. The stat effect itself is unchanged in Listo as far as the
changelog says; **the exact Listo damage die is (unverified)** — only the weapon list, spell level and
duration are stated. (Related datum: the changelog nerfed *Dryad's* Shillelagh to "2d8+WIS … so twice
as good as normal", which implies normal Listo Shillelagh is still 1d8+WIS.)

Consequences that matter beyond Druid:

- **Highest spellcasting modifier, not Wisdom.** A Druid X / Wizard 1 uses the higher of INT or WIS.
  Watch multiclass dips. Monk's Martial Arts: Dextrous Attacks overrides Shillelagh entirely.
- **Polearm Master overlap is exact.** Listo's PAM grants Reach to a Versatile polearm used
  two-handed — quarterstaves, spears, tridents — and **all three are on the Shillelagh list**, and
  PAM's bonus attack uses your spellcasting modifier when the weapon has a casting-ability override
  like Shillelagh. Glaives, halberds and pikes are *not* on the Shillelagh list, so the WIS-caster
  polearm build is specifically a quarterstaff/spear/trident build. See `listo-10.2-feats.md`
  → Polearm Master (but ignore its "permanent" wording).
- **Non-Druids get it three ways:** `UA Fighting Styles` **Druidic Warrior** (always Guidance +
  Shillelagh), the **Arcanist** feat (any level 1 spell, castable once per short rest — the docs name
  Shillelagh for Clerics and Monks explicitly), and **Magic Initiate: Druid**. Whether a
  feature-granted Shillelagh costs a slot now that it is a level 1 spell is **(unverified)**;
  Arcanist's once-per-short-rest casting sidesteps the question and is the cleanest route.

### Familiars and the third body

`Druid Wild Companion` (`12286`, archive `Druid Wild Companion-12286-1-1`, pak
`DruidWildCompanion_….pak`) grants the **Wild Companion** passive at **Druid level 2**: Find Familiar
becomes an **Always Prepared** spell with the normal Find Familiar cost and rules — explicitly **not**
costing a Wild Shape charge, because the author judged that wrong for BG3's balance. It also adds
**Flock of Familiars** (a 2nd-level Conjuration spell from `5e Spells`, which Listo ships) to the
Druid list at **spell level 3**, i.e. **Druid level 3**.

`Grimoire Familiar` (`17704`) adds a **Flying Grimoire** option to Find Familiar: flight, +1 Arcana to
its summoner within 10 ft, and a psychic-damage INT-save attack. Available to anyone with Find
Familiar, Druids included.

### Animal summons

`Conjure Animals and Summon Beast Spells` (`13458`, archive
`Conjure Animals and Summon Beast Spells-13458-2-2-8.rar`, pak `ConjureAnimals2024_….pak`) adds two
spells built to BG3 conventions rather than tabletop ones — crucially, **they last until Long Rest and
require no Concentration**, unlike the `5e Spells` versions of the same spells (600 turns, *and*
Concentration).

- **Summon Beast** — spell level 2, unlocked at **Druid 3** (Ranger 5, Bard Magical Secrets). One
  "Bestial Spirit": Wolf or Black Bear (Land: Pack Tactics + Maul) or White Raven or Eagle (Sky:
  Flyby + Maul). Upcasting gives **+5 HP, +1 AC, +1 damage per slot level**, and an **Extra Attack at
  every second slot level past 2** (1 extra at slot 4, 2 at slot 6, 3 at slot 8). Its proficiency
  bonus matches the summoner's at time of casting.
- **Conjure Animals** — spell level 3, unlocked at **Druid 5** (Ranger 9, Bard Magical Secrets).
  Twelve options, each with unique abilities: **pairs** of Brown Bears, Dire Wolves, Deep Rothe,
  Giant Badgers, Giant Eagles, Giant Hyenas, Giant Spiders, Panthers; or a **single** Dilophosaurus,
  Giant Boar, Polar Bear, or Sabre-Toothed Tiger. Abilities do not scale on upcast — **upcasting
  conjures more of them**. All count as **Fey**.

Both mods define these spells; **`5e Spells` also defines its own versions and whichever loads later
wins. The resulting load order in Listo is (unverified)** — if you see Concentration on the tooltip
you have the 5e Spells version, and the build assumption below (non-concentration, until Long Rest)
does not hold.

`Automated Summons` (`10922`, `Automated Summons SE.pak`) adds a toggle that hands your summons to
the AI during combat, per-summon opt-out via a "Block Automation" toggle. The toggle appears on your
Tav after toggling the Non-Lethal passive or after a Short Rest. **This is the mod that makes a
summon-heavy Druid actually playable in a two-player run** — it removes the turn-management tax of
running six conjured animals by hand.

### Speak with Animals, Goodberry, Warden of Vitality

- **Speak with Animals** is **Always Prepared for every Druid from level 1** via
  `Druid PHB2024 - Speak With Animals Always-Prepared` (`13098`, pak
  `DruidPHB2024-SpeakAnimals_….pak`, granting the "Druidic: Speak with Animals" feature). Separately,
  Listo makes Speak with Animals an **AoE that lasts until Long Rest**, so one cast covers both
  characters for the day.
- **Longstrider** is likewise AoE and until-Long-Rest (Listo-wide spell change).
- **Goodberry is buffed** per the docs. The old `Actually GOODberry` mod is **not** in the 10.2 Nexus
  list; the buff, if still present, lives in Listo's own `ListoMasterSpells.pak`. **The exact buff is
  (unverified)** — vanilla is 4 berries, each a Bonus Action to consume for 1d4 HP, each also worth 1
  Camp Supply. The camp-supply angle is the one worth checking in game, because Long Rests in this run
  cost 120+ supplies.
- **Warden of Vitality** was added to the Druid list in an older Listo version and is listed by the
  Wild Shape Overhaul as re-castable in Wild Shape, which implies it is still there; **presence in
  10.2 is (unverified)**.

### Wild Shape — `Druid Wild Shape Overhaul` (`1148`)

Archive `DruidWildShapeOverhaul 1148 1.1.2.0`, and **only `DruidWildShapeOverhaul.pak` is installed** —
none of the optional modules (the 5e-2014 charge module, the "Moon progression for all druids"
module) are in the manifest. This is a full replacement, using its own entries separate from vanilla's,
so other mods' Wild Shape edits do not reach it.

What changes:

- **Wild Shape can be used with either a standard or a bonus action, for all Druids** (Moon's bonus
  action is no longer its distinguishing perk).
- **CR progression rebased.** Non-Moon Druids now start at **CR 1/2** and reach **CR 1 at level 6**
  (vanilla: CR 1/4 → CR 1/2 at 6 → CR 1 at 8). Moon still starts at CR 1, CR 2 at 6, CR 3 at 9. Panther
  is available to everyone at level 2; Owlbear is Moon-only at 9.
- **Stats rebuilt.** HP from Hit Dice by CR (CR 1/2 = 3d8 + CON, CR 1 = 4d10 + CON), +1 HD every 2
  levels; AC and the form's attack ability rise at each CR step (all Druids at 6; Moon at 6, 9, 12).
  Ability DCs are 8 + form's proficiency + the relevant modifier.
- **Damage rebased and the vanilla scaling bonus deleted.** Base attacks are 2d4 at CR 1/2, 2d6 at
  CR 1; riders (Prone, Poisoned, Distract, etc.) are 1d8 / 1d10.
- **The level 10 second Extra Attack (Improved Wild Strike) is removed.** One Extra Attack at level
  5 is kept.
- **New forms:** Giant Boar, Giant Hyena, Giant Frog, Venom Spider, Phase Spider, Storm Raven, Giant
  Eagle, Alioramus, Blink Dog, Displacer Beast, Bulette, Dire Raven. Every vanilla form's kit was
  reworked (e.g. Giant Badger loses Claws/Burrow and gains Hamstring, Bloodied Tenacity, Ferocity, and
  a Reckless Multiattack at CR 2).
- **Critter forms** (Cat, Raven, plus many new small forms) are split into their own container, have
  no combat abilities, and **can be cast as a Ritual — free out of combat, no charge spent**.
- **Concentration spells that need re-casting now work in Wild Shape**: Moonbeam, Call Lightning,
  Heat Metal, Sunbeam, Warden of Vitality, Vampiric Touch. Shove works in Wild Shape.
- **Multiclass features now work in Wild Shape with animations**: Action Surge, Second Wind; Reckless
  Attack and the Barbarian rage strikes; Patient Defence, Step of the Wind; **Smite, Lay on Hands and
  all Paladin auras**; Sneak Attack and all Cunning Actions.
- Movement is 40 ft on most forms, 50 ft on some. All forms get skill proficiencies using *your*
  proficiency bonus. Lunar Mend scales to spell level 9 and can be set to 1d8 or 2d8 per slot level
  (choice offered at level 2). There is a toggle to auto-dismiss Wild Shape at the end of combat so a
  Druid main character does not miss dialogue.

> **Caveat.** The mod page says it is built with the `5R Druid` mod in mind and that some of its
> removals are "intended to be replaced with 5R Druid stuff, such as Fount of Moonlight and Primal
> Strike." **`5R Druid` is NOT in Listo 10.2.** So the compensations the author points at are not
> present. Exactly what the main pak removes on its own is **(unverified)** — worth checking Moon's
> level 6 Primal Strike in game before building around it.

---

## Circles (subclasses)

Eleven circles: four vanilla (Land, Moon, Spores, Stars), seven modded.

### Circle of the Land
- **Mod:** vanilla BG3.
- **Mechanics:** Level 2 land-type cantrip + **Natural Recovery** (restore spell slots on a Short
  Rest, charges growing at 2/3/5/7/…); circle spells at 3/5/7/9; **Land's Stride** at 6 (ignore
  Difficult Terrain, advantage against plant effects); **Nature's Ward** at 10.
- **Duo relevance:** Natural Recovery is the only in-combat-day slot refund in the class, and in a
  run where Long Rests cost 120+ camp supplies that is worth more than usual. Weakest circle for
  action economy though — it adds no bodies of its own.

### Circle of the Moon
- **Mod:** vanilla BG3, heavily reshaped by `Druid Wild Shape Overhaul` (`1148`).
- **Mechanics:** Level 2 **Combat Wild Shape** (bonus action, twice per Short Rest) + **Lunar Mend**;
  CR 1 forms at 2, CR 2 at 6, CR 3 at 9 under WSO; **Primal Strike** at 6 (beast attacks count as
  magical — see the 5R caveat above); Wild Shape Extra Attack at 5, **and the level 10 second Extra
  Attack is gone**.
- **Duo relevance:** the tankiest option — Wild Shape is a second HP bar, and with WSO your
  multiclass features (Smite, Sneak Attack, Action Surge, auras) keep working inside it. It does not
  add a body; it makes your one body harder to remove, which matters because losing either character
  usually ends the fight.

### Circle of the Spores
- **Mod:** vanilla BG3, plus `Circle of the Spores Druid Damage Type Options` (`11252`) and
  `Spore Druid Extra Attack` (`4018`).
- **File pulled:** **`Dealer's Choice Variant-11252-1-2.zip`** (pak `SporesDruidUpdate_Container_v1.2.pak`)
  and **`Spore Extra Attack (Single Extra Attack)-4018-2-0-0.zip`** (pak `Val_SporeExtraAttack_OneExtra.pak`).
- **Mechanics:** vanilla base — **Halo of Spores** (Reaction, 1d4 → 1d6 at 6 → 1d8 at 10),
  **Symbiotic Entity** (Wild Shape charge: 4 temp HP per Druid level, +1d6 damage on weapon/unarmed
  attacks, Halo damage doubled), circle spells at 3/5/7/9 (Blindness, Detect Thoughts / Animate Dead,
  Gaseous Form / Blight, Confusion / Cloudkill, Contagion), **Fungal Infestation** at 6 (Reaction,
  4 charges/Long Rest, raises a Fungal Zombie from a corpse until Long Rest), **Spreading Spores** at
  10 (2d8/turn area, does not hit you or allies).
  **Listo changes:** the *Dealer's Choice* variant lets you pick **Acid, Necrotic or Poison
  independently** for Halo of Spores, Symbiotic Entity and Spreading Spores (so a Poison Symbiotic
  Entity alongside a Necrotic Halo is legal), and gives **half damage on a successful Halo of Spores
  save** instead of none. `4018` **replaces Wild Strike at 5 and Improved Wild Strike at 10 with a
  real Extra Attack** — a single Extra Attack, usable outside Wild Shape, which is the whole point
  since Symbiotic Entity does not work in beast form.
- **Interaction note:** `4018` edits CircleOfTheSpores progression at 5 and 10 and `1148` also
  rewrites the level 5/10 Wild Shape attack features. Both ship Compatibility Framework definitions
  and Listo ships CF, so this should resolve; **that it resolves to exactly one Extra Attack is
  (unverified)**.
- **Duo relevance:** the best pure-melee Druid, and it stacks with Shillelagh (WIS to attack and
  damage) plus Symbiotic Entity's temp HP as a damage buffer. Fungal Infestation is four extra bodies
  per Long Rest from corpses — cheap action economy. Cross-reference `listo-10.2-feats.md`: the docs
  call out a Green Dragonborn Spore Druid with the Poison Elemental Adept feat + Poisoner's Robe as a
  build that downgrades enemy poison immunity to resistance.

### Circle of the Stars
- **Mod:** vanilla BG3 (Patch 8), tweaked by `Star Druid Tweaks` (`21637`).
- **File pulled:** `Star Druid Tweaks-21637-v1.zip`, pak `StarDruidTweaks.pak`.
- **Mechanics:** Level 2 Guidance + **Starry Form** (Wild Shape charge): **Archer** (bonus action
  Luminous Arrow, 1d8 + spellcasting mod Radiant → 2d8 at 10), **Chalice** (free 1d8 + WIS heal
  whenever you cast a healing spell with a slot → 2d8 at 10), **Dragon** (Concentration saves treat
  rolls of 9 or lower as 10; bonus action Dazzling Breath 2d6 → 3d6 at 5 → 4d6 at 10). **Star Maps**
  (2/3 at 5/4 at 9) cast Guiding Bolt free. **Cosmic Omen** at 6: after each Long Rest you get Weal or
  Woe, spending charges to add or subtract 1d6 on Attack Rolls or Saving Throws (3 charges, 4 at 9).
  Level 10 **Twinkling Constellations** lets you switch Starry Form once per turn as a free action.
  **Listo changes (`21637`): Dazzling Breath no longer hits allies, and Cosmic Omen charges recharge
  on a Short Rest instead of a Long Rest.**
- **Duo relevance:** **the strongest support circle for this run.** Cosmic Omens on a Short Rest is
  3–4 swings of ±1d6 on attacks or saves *per rest cycle* — in a two-character party where a single
  failed save can end the run, that is a save-or-die insurance policy you can actually afford to
  spend. Dragon form's Concentration floor keeps your one control spell up. Chalice makes every heal
  a double heal, which is exactly the profile you want when there are only two of you.

### Circle of the Sea
- **Mod:** `Circle of the Sea 2024 - Standalone` (`17858`).
- **File pulled:** `Circle of the Sea 2024-17858-1-1-0-3.zip`, pak
  `Circle_of_the_Sea_Standalone_1.1.0.3.pak`. Requires Compatibility Framework (present).
- **Mechanics:** **Level 2** circle spells Fog Cloud, Ray of Frost, Thunderwave; **Wrath of the Sea** —
  a 2m current around you lasting 10 turns; **free on the turn you summon it, then a Bonus Action**
  each later turn to use **Crashing Wave** on a target inside it: CON save or take **Nd6 Cold where
  N = your Wisdom modifier** (min 1d6) and be pushed 5m. **Level 3** Gust of Wind, Shatter. **Level 5**
  Lightning Bolt, Sleet Storm. **Level 6 Aquatic Affinity:** current radius → 4m, and you ignore
  water, electrified water and ice surfaces while it is up. **Level 7** Evard's Black Tentacles, Ice
  Storm. **Level 9** Conjure Elemental, Hold Monster. **Level 10 Stormborn:** while Wrath of the Sea
  is active you can **Fly** your movement distance and gain **Resistance to Cold, Lightning and
  Thunder**. **Level 14 Oceanic Gift:** project Wrath of the Sea onto an ally within 18m using your
  WIS modifier; spend an extra Wild Shape charge to get it on yourself as well.
- **Duo relevance:** the level 14 Oceanic Gift is unusually well-aimed at a two-person party — one
  Wild Shape charge buffs *both* characters with a WIS-scaled bonus-action damage-and-push. The
  built-in forced movement is also the cheapest way to peel something off your partner.

### Circle of Stormchasers
- **Mod:** `Circle of Stormchasers Druid Subclass` (`3584`).
- **File pulled:** `Circle of Stormchasers Druid Subclass-3584-1-5.zip`, pak `CircleofStormchasers.pak`.
- **Mechanics:** Circle spells — **2**: Shocking Grasp, Thaumaturgy, Thunderwave, Fog Cloud; **3**:
  Misty Step, Shatter; **5**: Fly, Lightning Bolt; **7**: Ice Storm, Conjure Minor Elemental; **9**:
  Cone of Cold, Tornado. **Level 2 Storm Shift:** Bonus Action, spend a Wild Shape charge instead of
  transforming — **temp HP equal to 3× your Druid level**, add your **WIS modifier to Lightning,
  Thunder or Cold damage rolls**, immune to Falling damage. Lasts **until Long Rest**; ends early on
  dismissal, another Wild Shape, or being incapacitated. **Level 6 Storm's Reach:** Bonus Action,
  target within 18m makes a DEX save, **d8s equal to your Proficiency Bonus** of Lightning/Thunder/Cold
  (half on save); uses equal to Proficiency Bonus, recharging on Long Rest. *(Its damage table is
  locked at the level 12 value and will not scale past 12.)* **Level 10:** while Storm Shifted your
  Lightning/Thunder/Cold **ignores Resistance and treats Immunity as Resistance**, plus a Flying speed
  equal to your movement and hovering (ignores surfaces and Difficult Terrain). **Level 14:**
  Resistance to Lightning, Thunder or Cold (swappable on a rest), plus one free cast each of Create or
  Destroy Water and Gust of Wind (Bonus Action) and **Chain Lightning** (Action) per Long Rest.
  Comes in Lightning / Thunder / Cold variants.
- **Duo relevance:** the temp-HP number is enormous — **3× Druid level, so 60 temp HP at 20** on a
  buff that lasts all day for one Wild Shape charge. Immunity-to-Resistance at 10 solves the single
  worst problem of an elemental damage build in a party too small to have a second damage type ready.

### Circle of Winter
- **Mod:** `Circle of Winter Druid Subclass` (`15058`).
- **File pulled:** `Circle of Winter Druid Subclass-15058-1-0.zip`, pak `CircleofWinter_….pak`.
  (Listo also ships `Compatibility Framework Patch for havsglimt's Subclasses` (`17062`), which the
  changelog credits with getting Circle of Winter working alongside other mods and multiclassing.)
- **Mechanics:** Circle spells — **2**: Ray of Frost; **3**: Darkness, Snilloc's Snowball Storm
  (a bonus 2nd-level spell the mod adds: 3d6 Cold in a 1.5m sphere, DEX save for half, +1d6 per slot
  above 2nd); **5**: Sleet Storm, Slow; **7**: Fire Shield, Ice Storm; **9**: Cone of Cold, Hold
  Monster. **Level 2 Winter Spirit:** an **Action**, spend a Wild Shape charge — **5 temp HP per Druid
  level**, **add your WIS modifier as bonus Cold damage to every damage-dealing Druid cantrip or
  spell** (not just cold ones), and **+1d6 Cold on melee weapon attacks**. Lasts until Long Rest, until
  the temp HP runs out, or until you Wild Shape again. **Level 6:** Bonus Action each turn while
  Winter Spirit is up — CON save or −3m movement until end of its next turn; plus immunity to slipping
  on ice. **Level 10:** creatures that fail a save against a Cold-damage Druid spell of yours fall
  **Prone** (the Winter Spirit bonus damage does not count as such a spell). **Level 14:** **Immunity
  to Cold**, and melee attackers take Cold damage equal to half your Druid level.
- **Duo relevance:** the mod author explicitly flags the melee rider as a Shillelagh pairing, and it
  is the best of the three "spirit" circles for a caster who also swings: WIS added to *every* damage
  spell and +1d6 on every melee hit off one charge. Prone-on-failed-save at 10 is real crowd control
  from damage you were casting anyway — valuable when you only have two action pools to spend.

### Circle of Dreams
- **Mod:** `Book of Druids - 5e Druid Subclasses (Nexus-Exclusive Version)` (`17722`).
- **File pulled:** `Book of Druids - Nexus Version-17722-1-0-0-9.zip`; the installed pak is
  **`BookOfDruids_NexusVersion 1.0.0.6c.pak`**. Requires Compatibility Framework (present).
- **Mechanics:** the Xanathar's Circle of Dreams. Confirmed from the mod page: a **level 14 "Walker in
  Dreams"** that is "completely different from the source material, due to significant limitations on
  the spells available," and requires a level 20 mod (present); v1.0.0.9 fixed its spell save DC.
  **The levels 2/6/10 features are (unverified) in this pack** — the same author's separate Circle of
  Dreams implementations use Balm of the Summer Court (2, bonus-action ranged heal + temp HP),
  Hearth of Moonlight and Shadow (6, Stealth/Perception aura + always-prepared Invisibility) and
  Hidden Paths (10, bonus-action teleport of self or ally + brief Invisibility), but that text comes
  from a *different* standalone mod (`1844`) and must not be assumed to match this pack.
- **Duo relevance:** if the standard progression holds, ally-targeted bonus-action healing and an
  ally teleport are both two-player-shaped tools; **verify in game before committing**.

### Circle of the Shepherd
- **Mod:** `Book of Druids` (`17722`) — same pack and pak as above.
- **Mechanics:** **Spirit Totems** (the level 2 feature, verified in full from the mod page):
  - **Bear** — allies in the aura gain **temp HP = 5 + your Druid level** when the spirit appears;
    advantage on Strength checks and saves inside it.
  - **Hawk** — advantage on Perception; allies inside can spend a **Reaction to gain advantage on an
    attack roll**.
  - **Flumph** — enemies in the aura cannot be invisible; **when you cast a healing spell, every ally
    in the aura also heals for your Druid level**.
  - **Frog** (homebrew) — allies don't provoke opportunity attacks, advantage on DEX checks and saves.
  - **Wolf** (homebrew) — allies get **+3m/10ft movement** and advantage on attacks against a target
    adjacent to another ally.
  **Mighty Summoner** (level 6 in 5e; level **(unverified)** here) was changed in v1.0.0.9 so that
  **your summons ignore all Resistance to physical damage on unarmed attack rolls** (it does not apply
  to saving throws or lingering effects). **Guardian Spirit and Faithful Summons are (unverified)** —
  not named on the mod page.
- **Duo relevance:** **the circle most directly built for this run.** Every totem is an aura that
  buffs the *other* character, and Mighty Summoner scales whatever you already have on the field —
  Conjure Animals, Find Familiar, Flock of Familiars, Fungal Zombies. With Automated Summons handling
  their turns, this is the closest a two-person party gets to a four-person one.

### Circle of Wildfire
- **Mod:** `Book of Druids` (`17722`) — same pack and pak as above.
- **Mechanics:** **Wildfire Spirit** at level 2, with **Fiery Teleportation** (v1.0.0.9 added
  enemy-only damage; it can teleport **only one ally at a time** — an engine limit the author accepted
  as a balance fix). **You can cast spells through the Wildfire Spirit** (the Tasha's optional
  Enhanced Bond), with some spells excluded because they misbehave (Misty Step is named).
  **Cauterizing Flames must be activated on your turn** rather than as a Reaction, because Reactions
  did not work for it. **Blazing Revival** requires the Wildfire Spirit to activate it on *its* turn,
  not instantly. Circle spells: **2** Burning Hands, Cure Wounds; **3** Flaming Sphere, Scorching Ray;
  **5** Plant Growth, Revivify; **7** Fire Shield, **Warden of Life** (a custom spell — the pack's
  stand-in for 5e's Aura of Life, also added to the Cleric list); **9** Flame Strike, Mass Cure Wounds.
  **Exact levels for Cauterizing Flames / Blazing Revival are (unverified)** (5e puts them at 6 and 14).
- **Duo relevance:** a permanent extra body that also **casts your spells from its position** — that
  is a second point of origin for AoE, which a two-person party otherwise cannot generate. Blazing
  Revival is a self-rez, and in a run where losing either character ends the fight, an automatic
  second life is worth more than its damage numbers.
- **Note:** v1.0.0.5 of the pack added a unique armour for each Druid subclass that lacked one. See
  `listo-10.2-equipment.md` for how Listo distributes gear.

### Circle of Wrath
- **Mod:** `(DTO) Otherworldy Archetypes` (`21822`).
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67.zip`, pak `DaelensTestament_….pak`.
  `5e Spells` recommended (present).
- **Mechanics** (from the author's documentation site, `prizzels.github.io/DTO`, not the Nexus page):
  **Level 2 Aspects of Wrath** — a Wild Shape / Bonus Action feature; choose **two** of **Sunfire,
  Stormstrike, Icespike, Kinetic Blast**. Each grants a scaling cantrip and builds **Wrath stacks**
  (max = your **Wisdom modifier**), each stack giving **+1 spell damage**. **Level 6 Revelations** —
  each aspect gains a revelation spell usable once per Wild Shape; casting it **consumes all Wrath
  stacks** for bonus damage (Consecrate Wrath fire/radiant, Surging Storm lightning/thunder, Rime
  cold/piercing, Fulminate force/bludgeoning). **Level 10 Aspect Mastery** — a third aspect, and
  immunity to that aspect's elemental status effects while channelling it. **Level 14 Eye of the
  Storm** — you start with **3 Wrath stacks**, your elemental immunities extend to **allies within
  9m**, and fading Wrath clears surfaces and clouds within 3m.
- **Duo relevance:** a self-contained scaling damage engine that needs no summons and no gear
  dependency; the level 14 shared immunity plus surface-clearing is genuinely useful when your
  two-body party keeps standing in its own AoE. Advertised as fully featured to level 20 — the
  documentation site stops at 14, so **15–20 is (unverified)**.

---

## Dip value

Only your **level 1** class grants saving throw proficiencies, so a Druid *dip* never gives you
Int + Wis saves — that requires starting Druid. A 3-level dip is feat-neutral under Listo's 3/6/9/12/15/18
cadence.

- **Druid 1 (as a dip):** Light + Medium armour and Shields, **Shillelagh** (level 1 spell — you must
  prepare it and spend a slot, then it lasts until Long Rest), **Goodberry**, and **Speak with Animals
  always prepared**. For any WIS-based character who wants to swing a quarterstaff, spear or trident,
  this one level is the whole gish package. Note it will *raise* your highest spellcasting modifier
  pool — a Wizard dipping Druid still uses INT for Shillelagh if INT is higher.
- **Druid 2 (the real dip):** Wild Shape (a second HP bar under the overhaul, and now usable with a
  standard *or* bonus action), your circle's level 2 feature, and **Find Familiar always prepared**
  via Wild Companion. For a two-person party, "one level of Druid for a permanent extra body" is one
  of the best action-economy trades in the list. Circle of Stormchasers' Storm Shift (3× *Druid* level
  temp HP) and Circle of Winter's Winter Spirit (5× *Druid* level temp HP) scale off Druid level, so
  they are poor dip targets — take those as your main class.
- **Druid 3:** adds Summon Beast and Flock of Familiars. Worth it only if you are building around
  summons.
- **Do not dip Druid for Shillelagh alone** if you can take a fighting style (**Druidic Warrior**) or
  the **Arcanist** feat instead — both reach it without spending a level. See `listo-10.2-feats.md`.

---

## Not present

Confirmed absent from the 10.2 Nexus mod list and/or the installed pak set:

- **`5R Druid` (PHB 2024 Druid)** — recommended by Wild Shape Overhaul for the "full experience"
  (Fount of Moonlight, Primal Strike, the 5R charge economy). **Not installed.** Neither are Wild
  Shape Overhaul's optional modules (5e-2014 charge module, Moon-progression-for-all module).
- **`Spells Enhanced - Shillelagh`** — added in a v6-era update, **no longer in the list**. Shillelagh
  is now handled by Listo's own `ListoMasterSpells.pak`.
- **`Actually GOODberry`** — added in a v3-era update, no longer a separate mod. Any Goodberry buff is
  in Listo's own paks.
- **`Druid Quality of Life`, `Druid Perfection`, `Druid Wildshape Items`, `Druid Wildshape Weapons and
  Gear`, `Granny Druid Rewards`** — all removed in earlier versions.
- **Standalone `Circle of Dreams` (`1844`), `Circle of the Shepherd` (`8515`), `Circle of Wildfire`,
  `Circle of Stars` (havsglimt), `Circle of the Blighted`, `Circle of Blood`, `The Unbroken Circle`** —
  not in the list. Dreams / Shepherd / Wildfire come *only* through the Book of Druids pack, whose
  implementations differ from the standalones.
- **`FoeBane` (`12523`)**, the Druid Grove questline reward, is flagged **optional** by the docs — see
  `listo-10.2-equipment.md`.
