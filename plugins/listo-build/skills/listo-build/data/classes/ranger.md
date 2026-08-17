# Listonomicon 10.2 — Ranger

Ranger in Listo is the base-game class plus three additions: `Expansion` (`279`) bolts on the
13–20 progression *and* the Tasha's optional features (Favored Foe, Deft Explorer, Primal
Awareness, Martial Versatility, Nature's Veil) as extra picks inside the existing Favoured
Enemy / Natural Explorer / Hide in Plain Sight selections; `5e Ranger Subclasses Combined`
(`15037`) adds five RAW conclaves; and two standalone conclaves (`14258`, `21822`) round the
list out to **eleven** subclasses. The class's Listo-specific character comes from two things
that are not in the Ranger's own files at all: **Hunter's Mark is a cast-once, re-apply-forever
bonus action** (`20688`), which removes the single biggest per-fight tax on the class; and the
**ranged-weapon rebalance** — Crossbow Expert renamed **Bow Expert** covering all bows, plus
firearms and hand crossbows traded range for damage — which quietly makes the plain longbow the
Ranger's range weapon and makes melee-adjacent bow play legal. For a two-person Lone Wolf run
the headline is bodies: Beast Master's companion, the Drakewarden's drake, and the
Ranger-accessible **Summon Beast (5) / Conjure Animals (9)** from `13458` are the cheapest
third, fourth and fifth actors in the game.

---

## At a glance

| | |
|---|---|
| **Primary ability** | **Dexterity** (or Strength) for attacks; **Wisdom** for spell save DC, spell attacks, and several feature scalings (Fey Wanderer's Otherworldly Glamour, Hunter's Sense uses, Misty Wanderer uses, Valkyrie leap distance, Foe Slayer) |
| **Saving throws (level 1 only)** | **Strength + Dexterity** — the only class in the game granting that pair. Note it is a *bad* pair defensively: no WIS/CON save proficiency. |
| **Hit points** | 10 + CON at level 1; 6 + CON per level |
| **Armour / weapons** | Simple + martial weapons, light + medium armour, **shields**. (Ranger Knight favoured enemy adds **heavy armour** proficiency.) |
| **Skills** | Choose **3** at level 1 from Animal Handling, Athletics, Insight, Investigation, Nature, Perception, Stealth, Survival. Multiclass entry grants **1**. Favoured Enemy picks add a 4th (Investigation / Arcana / History / Religion); Natural Explorer's Urban Tracker adds Sleight of Hand. |
| **Spellcasting** | Wisdom, half-caster (slots at ½ rate), **all known spells are always prepared**. Spells known: 2 at level 2, 7 by level 11. |
| **Resource cadence** | **Short rest:** Ranger's Companion re-summon, Umbral Shroud, Detect Portal, Ethereal Step, Magic-User's Nemesis, Slayer's Prey re-designation. **Long rest:** most PB-limited features (Favored Foe marks, Nature's Veil, Tireless, Hunter's Sense, Misty Wanderer, Reflexive Resistance, Swarming Dispersal), Drake Companion, Drake's Breath, Fey Reinforcements, Writhing Currents. **Per turn:** the damage riders (Colossus Slayer, Dreadful Strikes, Piercing Thorns, Slayer's Prey, Planar Warrior, swarm attack). |
| **Key breakpoints** | **1** — saves, Favoured Enemy + Natural Explorer (Favored Foe / Deft Explorer live in these lists). **2** — Fighting Style + Spellcasting. **3** — conclave **+ a Listo feat**. **5** — Extra Attack, Summon Beast. **9** — Conjure Animals. **10** — Hide in Plain Sight *or* Nature's Veil. **11** — capstone-ish conclave feature (Volley, Stalker's Flurry, Mighty Swarm, Drake's Breath, Distant Strike, Divine Flurry). **14** — Vanish (Hide as a bonus action). **15** — the second big conclave feature. **18** — Feral Senses. **20** — Foe Slayer. |
| **Dip value** | **1** = STR+DEX saves, martial/medium/shield, a 4th skill proficiency. **2** = + Archery style and half-caster entry. **3** = + a full conclave *and* the level-3 feat (feat-neutral dip). See "Dip value" below. |

---

## Class changes from vanilla

**Levels 13–20 — `Expansion` (`279`), archive `Expansion-279-1-7-3-6`**
- Base class: **Vanish** (14, Hide as a bonus action; the "can't be tracked" half is not
  implemented), **Feral Senses** (18, no disadvantage attacking creatures you can't see, plus
  awareness of invisible creatures within 30 ft), **Foe Slayer** (20, once per turn add your
  **Wisdom modifier** to an attack roll *or* damage roll against a favoured enemy —
  implemented as an interrupt).
- Subclass extensions: Beast Master **Share Spells** (15); Gloom Stalker spells at 13/17
  (Greater Invisibility, Seeming) + **Shadowy Dodge** (15); Hunter **Superior Hunter's
  Defense** (15 — choose Evasion, Stand Against the Tide, or Uncanny Dodge); Swarmkeeper
  spells at 13/17 (Arcane Eye, Insect Plague) + **Swarming Dispersal** (15).
- Expansion also grants feats at 16 and 19 by default, but Listo overrides feat cadence to
  every 3 class levels — see `data/listo-10.2-feats.md`.
- **Epic Boons at 20** are an Expansion MCM option; whether Listo enables them is
  **(unverified)**.

**Tasha's optional features — on by default, MCM-configurable per class.** The mod author
implemented them as *additional options inside the existing selection lists*, not as forced
replacements:
- **Favored Foe** (level 1, appears among the Favoured Enemy options): on hit you may mark the
  target for 1 minute; **it uses your concentration**. First hit each turn on the marked
  creature deals **+1d4**, rising to **1d6 at 6** and **1d8 at 14**. Uses = **proficiency
  bonus** per long rest. A Beast Master's Panther companion also benefits from it.
- **Deft Explorer** (level 1, among Natural Explorer options): **Canny** — double proficiency
  bonus (expertise) on one chosen skill, delivered through a spell container on the hotbar
  rather than a character-sheet pick, and only skills you are already proficient in are
  selectable. **Roving** (6) +5 ft speed plus climb/swim speed. **Tireless** (10) — action for
  `1d8 + WIS` temp HP, PB uses per long rest.
- **Primal Awareness** (3): grants **Speak with Animals** and **Commune with Nature** free
  (the rest of the RAW spell list is not implemented).
- **Martial Versatility** (4/8/12/16/19): swap one known fighting style for another.
- **Nature's Veil** (10, offered alongside Hide in Plain Sight): **bonus action invisibility**
  until the start of your next turn, PB uses per long rest.

> Favored Foe vs Hunter's Mark: both are concentration in Listo's build (see below), so they
> compete. Favored Foe scales to 1d8 and is free; Hunter's Mark is 1d6, costs a slot once, and
> in Listo re-targets for free forever. Hunter's Mark also drives Swarmkeeper's Prey's Scent
> and Dawnstrider's Pursuit of Valor, so those two conclaves want Mark, not Foe.

**Hunter's Mark reworked — `Spells Reworked - Hex and Hunter's Mark` (`20688`), archive
`Hex and Hunter's Mark-20688-1-0-0`**
- Casting Hunter's Mark applies a **self-buff lasting until Long Rest** (or death) that grants
  a temporary **Mark Quarry** ability on the hotbar. Mark Quarry re-applies the debuff to a new
  target as a **bonus action with no spell slot**, one target at a time.
- Works while **Wild Shaped**; can be cast while **Invisible or Hiding without breaking stealth
  or starting combat** (a Stealth check still applies).
- **Marked targets cannot turn Invisible and have Disadvantage on Stealth checks.**
- Mark Quarry's damage bonus correctly applies to **unarmed attacks**.
- Upcasting to 9th level supported.
- **Version caveat:** Listo pulled **1.0.0**. The Nexus page now describes **1.1.0**, which
  added an optional non-concentration variant (10-turn debuff instead) and fixed the
  Stealth-disadvantage rider. **In 10.2 the debuff still requires concentration**, and the
  Stealth-disadvantage line may not actually work.

**Spell list edits (from the Listo changelog)**
- **Removed from Rangers:** Shade Shield (the necromancy Shield clone), Mark of Putrefaction,
  Sigil of Mortality (the last is noted as non-functional anyway).
- **Added:** upcastable **Elemental Weapon** for Druids and Rangers.
- **`Conjure Animals and Summon Beast Spells` (`13458`)** — Rangers get **Summon Beast at
  ranger level 5** and **Conjure Animals at ranger level 9**. Summon Beast is one durable
  Bestial Spirit (Wolf/Black Bear land, White Raven/Eagle sky) that gains +5 HP, +1 AC and +1
  damage per slot level and an extra attack at slot levels 4/6/8; Conjure Animals gives 12
  options (pairs of Brown Bears, Dire Wolves, Deep Rothe, Giant Badgers, Giant Eagles, Giant
  Hyenas, Giant Spiders, Panthers; single Dilophosaurus, Giant Boar, Polar Bear, Saber-Toothed
  Tiger), all flagged as Fey, with upcasting increasing quantity.

**Fighting styles — `UA Fighting Styles` (`19693`)** adds Close Quarters Shooter, Tunnel
Fighter, Mariner, Interception, Thrown Weapon Fighting, Superior Technique (always Riposte),
Druidic Warrior (always Guidance + Shillelagh) and Blessed Warrior (always Guidance + Sacred
Flame). Blind Fighting and Unarmed Fighting are deliberately not implemented. **Which of these
appear on the Ranger's level-2 list is (unverified)** — the mod page only states explicitly
that Close Quarters Shooter, Mariner and Thrown Weapon Fighting were added to the Swords Bard
list. Vanilla Ranger styles (Archery, Defence, Duelling, Two-Weapon Fighting) are unchanged;
`Fighting Initiate` from Essential Feats is another route to a style (`data/listo-10.2-feats.md`).

**Removed from earlier Listo versions (as of v9.0.3, so absent in 10.2):** the **Displacer
Beast** Ranger companion and the **Stargazer** conclave.

---

## Conclaves (subclasses)

Eleven total: four base-game, five from the combined pack, two standalone.

### Beast Master *(base game + `Expansion`)*
- **Mod:** base game; extended by `Expansion` (`279`)
- **Mechanics:** L3 **Ranger's Companion** (Bear, Boar, Dire Raven, Wolf, Wolf Spider —
  recharges on short rest). `Expansion` **moves Companion's Bond from level 5 to level 3**
  (companion adds your **proficiency bonus to its AC and damage**) and adds a **Panther**
  companion built to the RAW Companion's Bond: it uses **your** proficiency bonus, gains
  **proficiency in all saving throws**, gains a hit die per ranger level, gains **Ability Score
  Improvements when you do**, has Perception proficiency and Stealth expertise, and can take
  **Dash/Disengage/Help as a bonus action** via Exceptional Training (L7). The Panther also
  benefits from **Favored Foe**, and scales visually (75% size <7, normal <11, +25% at 11+).
  L11 **Bestial Fury** (extra attack for all companions). L15 **Share Spells** — a self-targeted
  spell also affects the companion within 30 ft.
- **Duo relevance:** the strongest pick in this file for a two-person party. A third body that
  scales off your proficiency bonus, saves like a PC, and can Help (revive/advantage) as a
  bonus action is worth far more than its damage line. Share Spells at 15 lets one Longstrider
  / Haste / defensive buff cover two actors.

### Gloom Stalker *(base game + `Expansion`)*
- **Mod:** base game; extended by `Expansion` (`279`)
- **Mechanics:** L3 **Dread Ambusher** (+3 initiative; first turn of combat +3 m speed and one
  extra weapon attack dealing +1d8), **Umbral Shroud** (invisible while obscured, short rest),
  **Superior Darkvision** 24 m, Disguise Self always prepared. L5 Misty Step. L7 **Iron Mind**
  (**Wisdom and Intelligence saving throw proficiency**). L9 Fear. L11 **Stalker's Flurry**
  (free re-attack on a miss). L13/17 Greater Invisibility, Seeming. L15 **Shadowy Dodge**
  (reaction: impose disadvantage on an attack that doesn't already have advantage — the
  implementation resolves after you know the roll, an engine limitation).
- **Duo relevance:** Iron Mind at 7 patches the Ranger's worst structural weakness (no WIS save
  proficiency) without spending Resilient. Dread Ambusher plus a +3 initiative in a party of two
  is a real "delete one enemy before it acts" tool, and Shadowy Dodge converts Lone Wolf's
  extra reaction into survivability.

### Hunter *(base game + `Expansion`)*
- **Mod:** base game; extended by `Expansion` (`279`)
- **Mechanics:** L3 **Hunter's Prey** — Colossus Slayer (+1d8 once per turn vs a damaged
  target), Giant Killer (reaction melee attack when a Large+ creature attacks you), or Horde
  Breaker (two adjacent targets in succession, melee or ranged). L7 **Defensive Tactics** —
  Escape the Horde (disadvantage on OAs against you), Steel Will (advantage vs Frightened), or
  Multiattack Defence (−4 to an enemy's follow-up attacks on you). L11 **Volley** / **Whirlwind
  Attack**. L15 **Superior Hunter's Defense** — Evasion, Stand Against the Tide (reaction:
  force a missing melee attacker to repeat the attack on another creature; refunds the reaction
  if the AI won't comply), or Uncanny Dodge.
- **Duo relevance:** Volley is the only AoE in the class's base kit and matters when two
  characters have to clear adds. Multiattack Defence and Uncanny Dodge are pure "don't lose a
  character" value. Note the Listo changelog's "removed blanket Colossus Slayer" refers to
  **enemy** CX rangers, not the player feature.

### Swarmkeeper *(base game, Patch 8 + `Expansion`)*
- **Mod:** base game (Larian Patch 8). `Remove Swarmkeeper VFX` (`16056`, archive
  `No Swarmkeeper VFX-16056-1-0`) is shipped to suppress the out-of-combat swarm animation
  (Writhing Tide and the attack animations still show). Extended by `Expansion` (`279`).
- **Mechanics:** L3 **Prey's Scent** (swarm deals extra damage to **Hunter's Mark**ed
  creatures) and **Gathered Swarm** — pick Cloud of Jellyfish (Lightning / Shock), Flurry of
  Moths (Psychic / Blind) or Legion of Bees (Piercing / knock back 5 m), changeable on level
  up; once per round after you attack, the swarm either deals **1d6**, applies its status, or
  **teleports you**. Spells: Mage Hand + Faerie Fire (3), Web (5), Gaseous Form (9). L7
  **Writhing Tide** — 3 charges (4 at L9), flight 9 m and immunity to surfaces. L11 **Mighty
  Swarm** — swarm attack becomes **1d8**, the status option gains a rider, and the teleport
  option also **raises your AC for the round**. L13/17 Arcane Eye, Insect Plague. L15
  **Swarming Dispersal** — reaction for resistance to an instance of damage plus a teleport
  (the teleport is deferred to your next turn, like Archfey Misty Escape); PB uses per long rest.
- **Duo relevance:** the free per-round reposition is the answer to being focused when there is
  no third body to peel. Blind (Moths) is a strong single-target lockdown for a party that
  can't afford to eat a boss turn. Wants Hunter's Mark up permanently — which Listo's rework
  makes trivial.

### Drakewarden
- **Mod:** 5e Ranger Subclasses Combined (`15037`)
- **File pulled:** `RangerSubclasses5eCombined.zip-15037-2-0-1-1` (matches the current Nexus
  version 2.0.1.1)
- **Mechanics:** L3 **Draconic Gift** (Thaumaturgy cantrip; Tongue of Dragons is replaced by
  **Speak with Animals**) and **Drake Companion** — action to summon, choose a damage type from
  its Draconic Essence; **once per long rest free, or expend a 1st+ slot to re-summon**. Bite
  is +3+PB to hit for 1d6+PB piercing; **Infused Strikes** adds **1d6 of the drake's essence
  type when any creature within 30 ft that it can see hits with a weapon attack**. The drake
  auto-resummons on level-up to update its statblock, and acts on its own like other Ranger
  summons. L7 **Bond of Fang and Scale** — drake grows wings and Medium size, its bite gains
  +1d6 and counts as magical, **you gain resistance to its essence damage type**, and while
  within 10 ft of a non-hovering drake you ignore difficult terrain and most surfaces
  (the mod's stand-in for the mount rules). L11 **Drake's Breath** — 30 ft cone, DEX save vs
  your spell DC, **8d6** (10d6 at 15), once per long rest or by spending a 3rd+ slot. L15
  **Perfected Bond** — bite +2d6 total, Large drake, drake can shift to a wisp form for
  navigation, and **Reflexive Resistance**: reaction to give yourself *or* the drake resistance
  to an instance of damage, **PB uses per long rest**.
- **Duo relevance:** the other "third body" conclave, and mechanically the more offensive one —
  Infused Strikes buffs **your partner's** attacks too, not just yours. Reflexive Resistance is
  a second life-saving reaction, which Lone Wolf's bonus reaction makes affordable. Caveat from
  the author: **you may need to start a new playthrough** when taking this subclass, or the
  drake animates incorrectly.

### Fey Wanderer
- **Mod:** 5e Ranger Subclasses Combined (`15037`)
- **File pulled:** `RangerSubclasses5eCombined.zip-15037-2-0-1-1`
- **Mechanics:** L3 **Dreadful Strikes** (+1d4 psychic once per turn on a weapon hit, **1d6 at
  11**), **Otherworldly Glamour** (**add your Wisdom modifier to every Charisma check**, min
  +1, plus proficiency in Deception, Performance or Persuasion), spells Charm Person (3),
  Misty Step (5), Dispel Magic + Counterspell (9), Dimension Door (13), Mislead (17, from
  `5e Spells`). L7 **Beguiling Twist** — advantage on saves vs charm/fear, and when you *or* a
  visible creature within 120 ft succeeds on a charm/fear save, reaction to force a WIS save on
  another creature or charm/frighten it for 1 minute. L11 **Fey Reinforcements** — free
  **Summon Fey** (first cast per long rest costs no slot; a toggle adds non-concentration
  variants with a 1-minute duration). L15 **Misty Wanderer** — free Misty Step **WIS-modifier
  times per long rest**, and each Misty Step can bring one willing creature within 5 ft.
- **Duo relevance:** the best answer to "two characters must cover every skill check." WIS to
  *all* Charisma checks turns the Ranger into the party face without CHA investment — which
  matters enormously when the other player is not a CHA class. Misty Wanderer's passenger clause
  repositions **both** party members, and Summon Fey is a third body from 11.
  Implementation notes: the author says leave Beguiling Twist's interrupts alone, and Misty
  Wanderer only resolves reliably in **turn-based mode**.

### Horizon Walker
- **Mod:** 5e Ranger Subclasses Combined (`15037`)
- **File pulled:** `RangerSubclasses5eCombined.zip-15037-2-0-1-1`
- **Mechanics:** L3 **Planar Warrior** — bonus action to mark a creature within 30 ft; your
  next hit on it this turn converts **all** the attack's damage to Force and adds **+1d8**
  (**2d8 at 11**). Resistances, immunities and item damage riders convert correctly; the
  combat log display is cosmetically wrong. **Detect Portal** is re-implemented as an action
  granting **advantage on Perception for 1 minute**, once per short/long rest. Spells:
  Protection from Evil and Good (3), Misty Step (5), Haste (9), Banishment (13), Teleportation
  Circle (17). L7 **Ethereal Step** — bonus action, a custom Etherealness that gives you one
  turn of immunity in which you cannot interact with anything; **use it in turn-based mode or
  you waste it**. L11 **Distant Strike** — teleport 10 ft before each attack of the Attack
  action, and if you attack two different creatures you get **a third attack against a third
  creature**. L15 **Spectral Defense** — reaction for resistance to all of an attack's damage.
- **Duo relevance:** force-damage conversion is the cleanest answer to Listo's resistance-heavy
  enemy design ("hold onto a variety of weapons for damage types" — docs page 4); Horizon
  Walker just deletes the problem. Distant Strike is a genuine extra attack whenever there are
  three enemies, which is most fights a duo is losing.

### Monster Slayer
- **Mod:** 5e Ranger Subclasses Combined (`15037`)
- **File pulled:** `RangerSubclasses5eCombined.zip-15037-2-0-1-1`
- **Mechanics:** L3 **Slayer's Prey** — bonus action to designate a target within 60 ft; the
  first hit each turn on it deals **+1d6**; lasts until short/long rest or until you re-designate
  (**no concentration**). **Hunter's Sense** — an action, **WIS-modifier uses per long rest**;
  in this implementation it does not just reveal resistances, it makes your next hit before the
  end of your next turn **bypass all resistances and immunities** of your Slayer's Prey target.
  Spells: Protection from Evil and Good (3), Zone of Truth (5), Magic Circle (9), Banishment
  (13), Hold Monster (17). L7 **Supernatural Defense** — **+1d6 on every saving throw** forced
  by your prey (static passive). L11 **Magic-User's Nemesis** — reaction to force a WIS save on
  a creature casting a spell or teleporting within 60 ft; on a failure the spell/teleport is
  wasted. Once per short/long rest. L15 **Slayer's Counter** — reaction to attack your prey
  when it forces a save on you; on a hit **your save automatically succeeds** (the attack roll
  happens inside the interrupt and won't appear in the combat log).
- **Duo relevance:** the boss-killer pick, and the only conclave whose damage rider does **not**
  use concentration, so it stacks with Hunter's Mark. A free counterspell-equivalent that works
  on *any* caster and an auto-succeed save against the boss's control spell are exactly the two
  things that stop a duo wipe.

### Primeval Guardian (UA)
- **Mod:** 5e Ranger Subclasses Combined (`15037`)
- **File pulled:** `RangerSubclasses5eCombined.zip-15037-2-0-1-1`
- **Mechanics:** L3 **Guardian Soul** — bonus action to enter tree form until you end it or are
  incapacitated: **size Large, reach +5 ft, speed drops to 5 ft**, and you gain **temp HP equal
  to half your ranger level at the start of each turn**. **Piercing Thorns** — +1d6 piercing
  once per turn on a weapon hit (**turn-based mode only**, and keep the second interrupt off
  "Ask"). Spells: Entangle (3), Enhance Ability (5), Conjure Animals (9, needs `5e Spells`),
  **Grasping Vine** replacing Giant Insect (13), Insect Plague (17). L7 **Ancient Fortitude** —
  while in guardian form, **+2 max and current HP per ranger level**. L11 **Rooted Defense** —
  ground within 30 ft is difficult terrain for enemies while in form. L15 **Guardian Aura** —
  allies starting their turn within 30 ft **and below half HP** regain **half your ranger level**
  in HP; no effect on undead or constructs.
- **Duo relevance:** the only Ranger that is a tank/healer. At level 20 that's +40 max HP in
  form, 10 temp HP per turn, and 10 HP per turn to a hurt partner — passive healing that costs
  no action and no camp supplies, which is exactly the resource a duo runs short of. The
  **5-ft movement speed** is the price, and it is a steep one; it pairs with a bow, not a
  charge. Cosmetic caveat: the form is VFX-based and misbehaves with model-replacing effects
  and in cutscenes.

### Snowlight Conclave
- **Mod:** Snowlight Conclave Ranger (`14258`)
- **File pulled:** `Snowlight Conclave Ranger-14258-v2-10` (v2.10, the current Nexus version;
  needs Compatibility Framework ≥ 2.5.6.8, which Listo ships as `1933`; supports 13–20 via
  `Expansion`)
- **Mechanics:** Subclass spells Armour of Agathys (3), Blindness (5), Blinding Smite (9),
  Greater Invisibility (13), Cone of Cold (17). L3 **Snowborne** — **Cold resistance**, cannot
  be knocked prone by ice. L3 **Glaring Frost** — whenever you deal **Cold or Radiant** damage
  to a creature it makes a **CON save vs your spell save DC or is Blinded for 2 turns**. L7
  **Behind the Sun** — **+2 AC and +2 to Dexterity saving throws while in sunlight**. L11
  **Snow Blindness** — creatures you have Blinded take **1d6 Radiant whenever they take an
  Action, Bonus Action, or Reaction, and again at the end of their turn**. L15 **Snowborn
  Anthelion** — Glaring Frost also forces the CON save on **everything within 3 m** of the
  creature you damaged. No level-20 feature is described.
- **Duo relevance:** the hardest control conclave in the list. Blind is a full attack shutdown
  in BG3, Glaring Frost fires off any Cold or Radiant source (arrows, Blinding Smite, a radiant
  weapon), and Snow Blindness turns mass blindness into passive AoE damage that punishes every
  action an enemy takes. For two characters trying not to be outnumbered, blinding a room is
  worth more than any of the damage riders above. Needs a Cold/Radiant damage source to
  function — this is the conclave that most wants specific gear.

### Conclave of the Dawnstriders
- **Mod:** (DTO) Otherworldy Archetypes (`21822`) — Daelen's Testament of the Otherworldly
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67` (full progression to level 20)
- **Mechanics:** L3 **Herald of the Sun** — two toggleable passives: **Radiant** (weapon attacks
  deal Radiant and illuminate the target) or **Fire** (weapon attacks deal Fire and inflict
  Burning). L3 **Valkyrie** — an Action attack, range 9 m, leap distance scales with your
  **Wisdom modifier**: you ignore opportunity attacks, **gain an Extra Attack on landing**, and
  if you land within 2 m of an enemy, attacks against you have **Disadvantage** until the start
  of your next turn. Spells: Divine Favour (3), Aid (5), Daylight (9), Wall of Fire (13), Dawn
  (17). L7 **Zeal** — each attack grants 1 stack (2 with a two-handed weapon); at **7 stacks**
  Zeal ends and you gain an **Extra Attack**. L11 **Divine Flurry** — Action + Bonus Action +
  a 3rd-level slot: anchor in place for **5 Extra Attacks** with the **critical threshold
  reduced by 2** (−1 more per upcast); afterwards you are **Faded** (−2 attack rolls per stack)
  until the end of your next turn, cleared by gaining Zeal. Flurry attacks don't build Zeal.
  L15 **Pursuit of Valor** — killing a creature affected by **Hunter's Mark** gives you a free
  **Valkyrie**.
- **Duo relevance:** the highest raw damage ceiling of the eleven, and it converts Listo's free
  re-targeting Hunter's Mark into mobility (kill the marked target → free Valkyrie → re-mark as
  a bonus action → attack). Herald of the Sun is also a clean fix for physical resistance.
  The Faded window is a real cost in a party with no third body to cover a weak turn — Divine
  Flurry is a burst button for the turn that ends a fight, not a rotation.
  Note the mod author explicitly **swapped Zeal and Valkyrie** in 1.2.0.66 to discourage
  universal martial Zeal dipping — in 10.2 the level-3 pick is **Valkyrie**, not Zeal.

---

## Ranged weapons in Listo

The full detail lives in `data/listo-10.2-feats.md` and `data/listo-10.2-equipment.md`. What it
means for a Ranger:

- **Bow Expert (renamed Crossbow Expert) is the Ranger's feat.** It grants proficiency with
  **all bows**, removes **melee disadvantage with all bows** (vanilla: crossbows only), doubles
  the duration of **Gaping Wounds and Hamstrung**, adds **+2 save DC to Piercing Shot and
  Hamstring Shot**, and is a **half-feat (+1 DEX)**. Practical effect: a longbow Ranger no
  longer has to disengage or kite. In a two-person party where one character is usually in
  melee, this is what lets the Ranger stand next to the partner and keep shooting — which is
  also what makes melee-adjacent conclaves (Primeval Guardian at 5 ft speed, Dawnstrider
  landing Valkyrie inside 2 m, Drakewarden staying within 10 ft of the drake) function with a
  bow rather than forcing a weapon swap.
- **Sharpshooter's un-nerfed half is the one that matters.** Only **All In** was rebalanced
  (damage `(2 × PB) − 1`, attack penalty `PB`); the **Low Ground** component still **ignores
  high-ground penalties entirely**. In a game that models elevation everywhere, that is a
  persistent accuracy gain for a ranged Ranger regardless of whether you ever toggle All In.
- **Firearms out-damage bows per die but lose badly on range.** Basic and +1 firearms are sold
  by Dammon and Roah Moonglow in Acts 1–2. They are a legitimate Ranger weapon if you fight
  close, but they give up the one advantage a Ranger has in a duo: opening from outside the
  enemy's reach.
- **Hand crossbows had their range cut too.** They can still be **dual wielded**, so they remain
  the Two-Weapon Fighting / offhand-attack route, and `Some Neat Amazing Crossbows` (`18649`)
  adds two VeryRare hand crossbows (apply **Wet**, summon puddles, lightning) and two
  Legendary ones. But hand crossbows can no longer be the "safe" ranged option.
- **Net effect:** **range is now the axis that separates bow from gun**, not damage. The Ranger
  is the class best positioned to exploit that — Archery style (+2 to hit), Sharpshooter's high
  ground immunity, and Bow Expert's no-melee-disadvantage together make a longbow good at every
  distance, which no other weapon category is in 10.2.
- Bow-relevant gear from `data/listo-10.2-equipment.md`: **Adamantine Bow** (on mimics,
  underground), **Devilstring Bow** (duergar vendor), **Sussurstring Bow** (Sussur workshop).
  The **Titanstring Bow** line was reworked and the legendary version was explicitly nerfed
  "as not to completely out-class rangers."

---

## Dip value

- **Ranger 1** — the cheapest source of **Strength + Dexterity save proficiency** in the game,
  and it only works as the **level-1 class**. Also martial weapons, medium armour, shields, a
  4th skill proficiency, and a Favoured Enemy pick that can be a straight skill proficiency
  (Investigation / Arcana / History + heavy armour / Religion + Sacred Flame) or **Beast Tamer's
  Find Familiar once per short rest** — another cheap extra body. **Favored Foe** is available
  here as a concentration-based 1d4 damage rider even at one level.
- **Ranger 2** — adds **Archery (+2 to ranged attack rolls)** or Defence/Duelling/Two-Weapon,
  plus half-caster entry with two always-prepared spells. A very cheap fighting style for a
  ranged build that doesn't want Fighter.
- **Ranger 3** — a full conclave *and* the level-3 feat. Under Listo's every-3-class-levels
  cadence this dip is **feat-neutral**. The three that pay off hardest at exactly 3:
  **Beast Master** (companion **with Companion's Bond already at level 3** thanks to
  `Expansion` — a PB-scaled third body for three levels), **Gloom Stalker** (+3 initiative and
  a first-round extra attack with +1d8), and **Monster Slayer** (a no-concentration +1d6 rider
  that recharges on a short rest).
- **Ranger 5** — Extra Attack plus **Summon Beast**. Rarely correct as a dip unless the other
  class has no Extra Attack of its own.
- **Against dipping out of Ranger:** the 11/14/15/18/20 features (Stalker's Flurry, Volley,
  Vanish, the L15 conclave features, Feral Senses, Foe Slayer) are all back-loaded, and the
  L15 features are uniformly reaction-based — which is where Lone Wolf's **extra reaction**
  turns them from once-a-turn into twice. A duo Ranger has a stronger case for going deep than
  most classes do.
- **The Inquisitor class (`18318`) is tagged as both Cleric and Ranger** for dialogue purposes
  and uses the **Ranger spell-slot progression** as a WIS-based spontaneous caster. That
  overlap means Ranger-flavoured dialogue is available without playing a Ranger. Its own
  mechanics are documented elsewhere.

---

## Not present

- **Stargazer** conclave — removed in Listo v9.0.3.
- **Displacer Beast** as a Ranger companion — removed in Listo v9.0.3.
- **Beast and Bow** (Ranger-focused equipment) and **Ranger Leather Armour** — both removed in
  earlier versions; neither appears in the 10.2 mod list.
- **The 5e Ranger Subclasses Combined pack does not include Swarmkeeper or Gloom Stalker** —
  the pack is exactly Drakewarden, Fey Wanderer, Horizon Walker, Monster Slayer and Primeval
  Guardian. Swarmkeeper is the base-game Patch 8 subclass.
- **Codex of Might and Magic** (DTO Volume 2) — **not in Listo 10.2**. Its Ranger features
  (**Endless Hunt**: Hunter's Mark at will without concentration; **Cull the Hunted**: a free
  opportunity attack when your Marked foe becomes severely injured) are **not available**.
- **The non-concentration Hunter's Mark variant** from `Spells Reworked` v1.1.0 — Listo pulled
  v1.0.0, so Hunter's Mark still uses concentration.
- Ranger appears heavily in **Combat Extender** as an enemy archetype (Act 3 dopplegangers,
  assassins and Murder Tribunal cultists are largely rangers/rogues; enemy rangers gain
  Improved Critical by Act 3 and better mobility). That affects what you face, not what you
  build.

---

## Verification notes

- Every subclass above is confirmed present via the 10.2 Nexus mod list, the Wabbajack manifest,
  or (for the four base-game conclaves) the `Expansion` progression table that extends them.
- Marked **(unverified)**: whether Listo enables Expansion's **Epic Boons** at 20; which
  fighting styles from `UA Fighting Styles` are actually offered to Rangers; whether the
  Stealth-disadvantage rider on Hunter's Mark works in the 1.0.0 archive Listo pulled.
- Sources: mod pages and implementation articles for `15037` (articles 1298/1300/1301/1303/1577),
  `279` (article 684), `14258`, `21822` + the DTO documentation site, `20688`, `13458`, `19693`,
  `16056`; bg3.wiki for vanilla Ranger, Hunter, Beast Master, Gloom Stalker and Swarmkeeper
  baselines; Listo docs pages 4 and 5 for the class/changelog history.
