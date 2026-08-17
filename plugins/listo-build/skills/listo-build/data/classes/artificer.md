# Listonomicon 10.2 — Artificer

Artificer is a **brand-new class added by a mod** (`1779`, *Artificer class and all subclasses*).
There is no vanilla BG3 baseline for it, so every mechanic in this file was read out of the mod's
own data files — nothing is inferred from tabletop 5e. It is an **Intelligence half-caster** with
d8 hit dice, medium armour and shields, a per-long-rest **Infusion** economy that manufactures
magic items out of thin air, and four subclasses, two of which put a **permanent extra body** on
the field. For this run it matters three times over: it is the best *level-1 opener* in the list
(Int + Con saves, medium armour, shields, Sleight of Hand, all for one level), it is the mod that
**defines the Firearms weapon group** that every gun in Listo hangs off, and it is one of the
non-stacking sources of **Experimental Alchemy**.

**Provenance**
| | |
|---|---|
| ModID | `1779` — "Artificer class and all subclasses" |
| Archive pulled by Listo 10.2 | `Artificer-1779-2-22-0-1729427695.zip` → **v2.22.0**, uploaded 2024-10-20 |
| Second archive pulled | `Artificer 5e Spells Addon-1779-2-4-1694983974.zip` → **addon v2.4**, 2023-09-17 |
| Data read from | `github.com/Kidel/BG3_Artificer` at **tag `2.22.0`** — the repo's last commit is 2024-10-20T09:14:28Z, exactly matching the archive, so main == the shipped build |
| Listo overrides | `Listo Tweaks and Patches`, `Listo Master Spells Patch`, `Degreaser 2.0` (`15258`) — **opaque `.pak`s, not inspectable from the manifest.** Where Listo is known to have changed something it is called out below. |

The 5e Spells Addon **overrides the base spell lists** (same list UUIDs) — verified. Its
`SpellLists.lsx` last changed 2023-09-17, the same day as the v2.4 archive, so the addon content
read here is what Listo ships.

---

## At a glance

| | |
|---|---|
| **Primary / casting ability** | **Intelligence** (`PrimaryAbility 4`, `SpellCastingAbility 4`) |
| **Hit dice** | d8 (`BaseHp 8`, `HpPerLevel 5`) |
| **Saves granted at level 1** | **Intelligence + Constitution** — *only if Artificer is your level-1 class* |
| **Armour / shields** | Light armour, **Medium armour, Shields** |
| **Weapons** | Simple weapons, hand crossbows, light crossbows, **Firearms, Slings** |
| **Free skill proficiency** | **Sleight of Hand** (granted outright, not a pick) → **Expertise at Artificer 6** |
| **Skill picks (level 1 only)** | 2 from Arcana, History, Investigation, Perception, Medicine, Nature |
| **Spellcasting** | **Half-caster.** `MulticlassSpellcasterModifier = 0.5`. Prepared caster (`MustPrepareSpells true`) drawing from the whole Artificer list, cleric-style |
| **Slot progression** | 2 L1 @1 · 3 @3 · 4 @4 · 2 L2 @5 · 3 L2 @7 · 2 L3 @9 · 3 L3 @11 · 1 L4 @13 · 2 L4 @15 · 3 L4 + 1 L5 @17 · 2 L5 @19 → **4 / 3 / 3 / 3 / 2** at level 20 |
| **Cantrips** | 2 @1, +1 @10, +1 @14, +1 @18 (5 total), **plus** Magical Tinkering's 3 always-prepared |
| **Resource cadence** | Infusion Slots replenish on **long rest** (`ReplenishType "Rest"`). Most infusions are also `OncePerRest`. Elixirs and Arcane Jolt are long-rest. The Right Tool for the Job and the Homunculus are **short rest** |
| **ASI/feat levels in the base mod** | 4, 8, 12, 16, 19 — **overridden by Listo's universal feat cadence** (3/6/9/12/15/18); see Feats below |
| **Key breakpoints** | **1** (saves + armour + Firearms), **2** (Infusions), **3** (subclass), **5** (L2 slots; Extra Attack for Armorer/Battle Smith), **6** (SoH Expertise, 3rd infusion slot), **7** (Flash of Genius), **10** (Replicate Magic Item unlocks; +1 infusions become +2), **11** (Spell-Storing Item), **20** (Soul of Artifice) |
| **Dip value** | **Top tier at 1.** Good at 2 (Infusions). Weak at 3 (subclass features are back-loaded) |

**Dialogue tag:** Artificer has no dialogue tag of its own and **registers as "Wizard" in
dialogue checks** — the mod's own `ClassDescriptions.lsx` carries the Wizard tag GUID with a
`TODO` comment, and the Nexus page lists it under Known Issues.

---

## Dip value — why Artificer 1 is a premium opener

The mod ships **two separate level-1 progression nodes** for the same class. Which one you get
depends entirely on whether Artificer is your **first** class. Verbatim from `Progressions.lsx`:

**Level-1 node (Artificer is your starting class):**
```
ProficiencyBonus(SavingThrow,Intelligence); ProficiencyBonus(SavingThrow,Constitution);
ProficiencyBonus(Skill,SleightOfHand); Proficiency(SimpleWeapons); Proficiency(HandCrossbows);
Proficiency(LightCrossbows); Proficiency(LightArmor); Proficiency(MediumArmor);
Proficiency(Shields); Proficiency(Firearms); Proficiency(Slings); ActionResource(SpellSlot,2,1)
+ SelectSkills(2 from Arcana/History/Investigation/Perception/Medicine/Nature)
```

**Multiclass node (`IsMulticlass = true`, i.e. Artificer taken at level 2+):**
```
ProficiencyBonus(Skill,SleightOfHand); Proficiency(LightArmor); Proficiency(MediumArmor);
Proficiency(Shields); Proficiency(Firearms); Proficiency(Slings)
```

**The delta — what you forfeit by not opening with Artificer:**

| | Artificer as level 1 | Artificer as a later multiclass |
|---|---|---|
| Intelligence save proficiency | **yes** | **no** |
| Constitution save proficiency | **yes** | **no** |
| Simple weapons, hand/light crossbows | yes | **no** |
| 2 skill proficiencies | yes | **no** |
| 2 level-1 spell slots as a flat boost | yes | no (slots come from the 0.5 multiclass modifier instead) |
| Light + **Medium armour**, **Shields** | yes | **yes** |
| **Sleight of Hand** proficiency | yes | **yes** |
| **Firearms + Slings** proficiency | yes | **yes** |
| Magical Tinkering, Experimental Alchemy, 2 cantrips, full L1 spell list | yes | **yes** |

So the build-math note is **confirmed and slightly understated**: the multiclass node grants no
saving throws *and* no weapon proficiencies *and* no skills. **Int + Con is the single best save
pair in the game** — Con for concentration, Int for the mind-affecting saves that end a two-person
party — and Artificer is one of very few level-1 classes that hands you both at once.

Cross-references:
- `listo-10.2-feats.md` already prices this out: **Moderately Armoured** (medium armour + shields)
  requires **Lightly Armoured** first, so shields cost a character with no armour proficiency
  **two of their six feats**. An Artificer 1 opener returns both. The feats file names
  "Fighter 1, Artificer 1, or Paragon 1" as the three classes that do this.
- Unlike Fighter 1, Artificer 1 also brings **Int + Con saves** (Fighter gives Str + Con),
  **Sleight of Hand**, **Firearms proficiency**, half-caster slot progression that keeps
  contributing when you multiclass, and Experimental Alchemy.

**Artificer 2 as a two-level dip** adds 2 Infusion Slots and **4 known infusions** from the level-1
pool — including Enhanced Weapon (+1 attack/damage on any weapon), Enhanced Defense (+1 AC),
Enhanced Arcane Focus (+1 spell attack and spell save DC), and the Homunculus (a free extra body).
For a Lone Wolf pair short on gear that is a large amount of permanent stat for two levels.

**Warning — half-caster rounding.** The class carries a level-1 passive, **Rounded Up Spellcaster
Level** (`Passive_ArtificerExtraSlots`), that exists because BG3's `MulticlassSpellcasterModifier`
can only round *down*. It hands back the missing slot when your Artificer level is odd. The
mod's own README states this **works only with core-game spellcasters** — pairing Artificer with a
*modded* caster class may lose the rounding-up. `(unverified against Listo's modded classes.)`
The README also notes the extra slots **do not appear on the level-up screen**; they show up once
you return to the field.

---

## Infusions

Unlocked at **Artificer 2** (`UnlockedInfusionSlots`). Two independent tracks:

**Infusion Slots** (the per-long-rest currency, `ReplenishType "Rest"`):
2 at L2 → 3 at L6 → 4 at L10 → 5 at L14 → **6 at L18**.

**Infusions known** (permanent picks from an expanding pool):
4 at L2 → 6 at L6 → 8 at L10 → 10 at L14 → **12 at L18**.

Almost every infusion costs **1 Action + 1 Infusion Slot** and is `OncePerRest`. Infusions applied
to *allies'* gear are delivered through a hidden 30 m technical aura (`AURA_OF_ARTIFICER`) that the
class carries from level 1 — this is plumbing, not a player-facing feature, but it is why an
infusion put on a companion's armour keeps working.

### The pool, by unlock level

**Available from L2** (pick 4 of these 7):

| Infusion | Effect |
|---|---|
| **Enhanced Defense** | +1 AC to a piece of armour **or a shield**. **+2 at Artificer 10.** |
| **Enhanced Weapon** | Target weapon becomes **magical** and gains +1 attack/damage. **+2 at Artificer 10.** |
| **Enhanced Arcane Focus** | Target creature gains **+1 spell attack rolls and +1 spell save DC**. **+2 at Artificer 10.** Implemented as a buff on the creature, since BG3 has no spellcasting focus. |
| **Radiant Weapon** | Weapon becomes magical, +1 attack/damage, sheds bright light. |
| **Repeating Shot** | **Crossbow or Firearm** only. +1 attack/damage on ranged attacks; with an empty main-hand ranged slot it generates its own magic ammunition and lets you **attack two targets once per turn**. At Artificer 10 that attack **no longer costs a Bonus Action.** |
| **Homunculus Servant** | Summons a permanent servant — **Cat** (Meow/distract), **Crab** (Crippling Pinch, slow), **Frog** (Bufotoxin), **Rat** (Infectious Bite), **Raven** (Blind), **Spider** (poison bite). Cooldown is **OncePerShortRest**. |
| **Bag of Holding** | Infinite carry capacity, ignores weight. Does not function in the Astral Plane. Spending **2 slots** on it opens a one-way gate to the Astral Plane and kills the wearer — deliberate, per the README. |

**Added at L6:**

| Infusion | Effect |
|---|---|
| **Create Spell Slot** | **Bonus Action** + 1 Infusion Slot → one spell slot. `OncePerRest`. |
| **Returning Weapon** | +1 attack/damage; thrown weapon returns to hand immediately. |
| **Resistant Armor** | Resistance to a chosen damage type — **all ten**: Acid, Cold, Fire, Force, Lightning, Necrotic, Poison, Psychic, Radiant, Thunder. |
| **Boots of the Winding Path** | **+3 m movement and the wearer does not provoke Opportunity Attacks.** Deliberately reworked away from Misty Step by the mod authors. |

**Added at L10 — Replicate Magic Item.** One infusion pick that unlocks a container of five
**VeryRare** items. Each replica costs an Infusion Slot and **vanishes at long rest**:

| Replica | Boosts (read from `Armor.txt`) |
|---|---|
| **Amulet of Greater Health** | `AbilityOverrideMinimum(Constitution, 20)` + **Advantage on Constitution saving throws** |
| **Gloves of Hill Giant Strength** | `AbilityOverrideMinimum(Strength, 20)` + **+1 Strength saves** |
| **Circlet of Mind Reading** | Detect Thoughts, **Counterspell** (with its own resource passive), Advantage on **Wisdom and Constitution** saves |
| **Flying Boots** | **Fly 1/short rest**, +3 m movement, +2 Acrobatics, +2 Athletics |
| **Ring of the Undead Servant** | Create Undead 1/short rest, Necrotic resistance |

> **This is the single biggest reason to run Artificer deep in this list.** Gear costs 4× to buy.
> A CON-20 floor with advantage on CON saves, remade free after every long rest, is a concentration
> platform you would otherwise have to find. Note it is a **level-10 unlock** — plan it as a main
> class, not a dip.

**Added at L14 — Arcane Propulsion Armor.** Wearer moves faster, gains a once-per-turn Force
blast / area attack, and **all weapon attacks deal additional Force damage.**

---

## Subclasses

Chosen at **Artificer 3**. The mod ships exactly **four** — confirmed from
`ClassDescriptions.lsx` (`Alchemist`, `Armorer`, `Artillerist`, `BattleSmith`) and from the mod's
own summary line: *"Adds the Artificer class and all its subclasses to the game: Alchemist,
Armorer, Artillerist and Battle Smith."* No Listo mod adds a fifth.

All four gain always-prepared spells at 3/5/9/13/17. Only **Alchemist** has extra nodes at 6 and 10.

### Alchemist

- **L3 — Experimental Elixirs.** Produce randomly-effected elixirs; **2 charges per long rest.**
  You can make **additional elixirs by expending a spell slot.** Unconsumed elixirs vanish at long
  rest. Always-prepared: Healing Word, Ray of Sickness.
- **L5 — Alchemical Savant.** Add your **Intelligence modifier (min +1)** to one roll of a spell
  that either restores hit points or deals **acid, fire, necrotic, or poison** damage.
  Always-prepared: Flaming Sphere, Melf's Acid Arrow.
- **L6 — Elixir charges rise to 4 per long rest.**
- **L9 — Restorative Reagents.** Anyone drinking your experimental elixir also gains **2d6
  temporary HP**; you may cast **Lesser Restoration free and unprepared**. Always-prepared:
  Gaseous Form, Mass Healing Word.
- **L10 — Alchemical Mastery.** Upgrade of the base class's Alchemical Adept: spend **Salvaged
  Elements** to craft **rare ingredients** for the in-game Alchemy system. Per the README this is a
  deliberate mod-authored replacement for 5e's Chemical Mastery slot.
- **L13 —** Blight, Death Ward.
- **L15 — Chemical Mastery + elixir charges rise to 6.** Once per long rest cast **Greater
  Restoration and Heal free**; **resistance to Poison and Acid damage and immunity to being
  poisoned.**
- **L17 —** Cloudkill, Revivify.

> **Duo relevance:** the only subclass that pays for itself in **camp supplies** — free Heal,
> Greater Restoration, Lesser Restoration and 6 elixirs per rest directly offsets the 120+ supply
> cost of long-resting, and it stacks with the crafting economy the class already opens.

### Armorer

- **L3 — Arcane Armor.** Grants **Heavy Armour proficiency** (Larian-Ranger-style substitution;
  the 5e version had no BG3 equivalent) and two switchable models, each a `OncePerShortRest` shout:
  - **Guardian** — grants **Thunder Gauntlets**, which count as simple melee weapons while your
    hands are empty.
  - **Infiltrator** — grants **Lightning Launcher**, which counts as a ranged weapon while your
    hands are empty (there is also a Chest-Mounted variant).
  Always-prepared: Magic Missile, Thunderwave.
- **L5 — Extra Attack.** Always-prepared: Mirror Image, Shatter.
- **L9 — Perfected Armor.** Model-dependent. **Guardian:** reaction when a creature attacks a
  nearby ally — Strength save vs your spell save DC, **pulls the creature 6 m toward you and deals
  damage.** **Infiltrator:** anything hit by your Lightning Launcher glimmers until your next turn,
  taking **disadvantage on attack rolls** and **+1d6 lightning** from your attacks. Always-prepared:
  Hypnotic Pattern, Lightning Bolt. *The tooltip explicitly warns "Rebuild after levelup".*
- **L13 —** Fire Shield, Greater Invisibility.
- **L15 — Perfected Armor MkII.** Guardian's reaction now **also deals damage**; Lightning Launcher
  deals **+1d6** and grants you **advantage** against the target.
- **L17 —** Arcane Gate, Blade Barrier.

> **Duo relevance:** the tankiest artificer — heavy armour, Extra Attack at 5, and a **reaction
> that yanks an attacker off your partner**. Lone Wolf's extra Reaction means you can use the
> Guardian pull and still keep a normal reaction in reserve.

### Artillerist

- **L3 — Eldritch Cannon.** A summoned cannon in either a **Small turret** or **Tiny handheld**
  form (the handheld version is itself a Firearm item). Modes: **Flamethrower**, **Force Ballista**,
  **Protector**. The summon spell is built `using "Target_RangersCompanion"` — same casting shape as
  Ranger's Companion, i.e. resummonable without a daily charge. Always-prepared: Shield, Thunderwave.
- **L5 — Arcane Firearm.** **Add 1d8 to one damage roll whenever you cast a spell.** Implemented as
  a self-buff rather than a focus item, since BG3 has no spellcasting focus. Always-prepared:
  Scorching Ray, Shatter.
- **L9 — Explosive Cannon.** All cannon damage rolls **+1d8**, and you can **detonate** the cannon
  (destroying it) forcing a Dexterity save on everything in range. Always-prepared: Fireball,
  Gust of Wind.
- **L13 —** Ice Storm, Wall of Fire.
- **L15 — Fortified Position.** **Summon two cannons with a single action.**
- **L17 —** Cone of Cold, Blade Barrier.

> **Duo relevance:** the strongest action-economy pick in the class. **+1d8 on every spell** from
> level 5 is a flat damage floor, and by 15 you are fielding **two independent cannons** — with a
> Homunculus infusion that is a four-body party out of two characters.

### Battle Smith

- **L3 — Steel Defender + Battle Ready.** **Battle Ready:** when attacking with a **magical**
  weapon you use **Intelligence for attack and damage rolls** instead of Str/Dex — and since
  Enhanced Weapon *makes a weapon magical*, the class self-supplies the prerequisite. Also grants
  **Martial Weapon proficiency**. The **Steel Defender** is summoned via the same
  `Target_RangersCompanion` template; it has a **Deflect Attack** ability that imposes disadvantage
  on an attack aimed at someone other than itself. Always-prepared: Heroism, Shield.
- **L5 — Extra Attack.** Always-prepared: Branding Smite, Warding Bond.
- **L9 — Arcane Jolt.** On hitting with a magic weapon attack, deal an extra **2d6 Force** or
  **heal 2d6** to a creature or construct you can see. Uses per long rest =
  **Intelligence modifier + Proficiency Bonus** (read from the passive's own condition formula).
  Always-prepared: Aura of Vitality, Conjure Barrage.
- **L13 —** Death Ward, Fire Shield.
- **L15 — Improved Defender.** Arcane Jolt damage **and** healing rise to **4d6**; whenever the
  Steel Defender uses Deflect Attack, **the attacker takes Force damage.**
- **L17 —** Banishing Smite, Mass Cure Wounds.

**Battle Smith gear (from the Nexus page, not from the data files):** endgame gear is sold by
**the Dragonborn girl in the Act 3 blacksmith shop**; the **Steel Watcher blueprints** are sold by
**the kid vendor in the Merchants' Guild**. The mod's loca confirms both a **Steel Watcher
Schematics** item ("Gondian Auto-Guard") that upgrades the Defender into a smaller Steel Watcher,
and a **Steel Defender Overdrive** armour that grants the Defender **Extra Attack, a damage bonus
and new abilities**.

> **Duo relevance:** the *single-character* answer to a two-person party — INT drives everything
> (attack, damage, saves, spell DC, Arcane Jolt uses), Extra Attack at 5, a permanent third body
> that can **impose disadvantage on attacks aimed at your partner**, and Arcane Jolt doubling as
> off-turn healing that costs no spell slot.

---

## Spell list

Prepared caster with the **whole list available to prepare** (`AddSpells` on each level-up node
with no `AlwaysPrepared` flag), like a cleric — you never pick "spells known".

**With the 5e Spells Addon that Listo ships** (`v2.4`, which overrides the base lists):

- **Cantrips:** Acid Splash, **Booming Blade**, Create Bonfire, Dancing Lights, Fire Bolt,
  Frostbite, **Green-Flame Blade**, Guidance, Light, Lightning Lure, Mage Hand, **Magic Stone**,
  Mending, Poison Spray, Prestidigitation, Ray of Frost, Resistance, Shocking Grasp,
  Spare the Dying, Sword Burst, Thorn Whip, Thunderclap
- **L1:** Catapult, Cure Wounds, Absorb Elements, Detect Magic, Disguise Self, Expeditious Retreat,
  Faerie Fire, False Life, Feather Fall, Grease, Jump, Longstrider, Ray of Sickness, Sanctuary,
  Snare, Tasha's Caustic Brew
- **L2:** Aid, Arcane Lock, Blur, Continual Flame, Darkvision, Enhance Ability, Enlarge/Reduce,
  Heat Metal, Invisibility, Kinetic Jaunt, Lesser Restoration, Magic Weapon, Protection from Poison,
  See Invisibility, Vortex Warp, Web
- **L3:** Ashardalon's Stride, Blink, Catnap, Create Food and Water, **Counterspell**, Elemental
  Weapon, Flame Arrows, Fly, Glyph of Warding, **Haste**, Intellect Fortress, Protection from
  Energy, **Revivify**, Water Walk
- **L4:** Arcane Eye, Freedom of Movement, Otiluke's Resilient Sphere, Stoneskin
- **L5:** Greater Restoration, Skill Empowerment, Wall of Stone

Without the addon the base lists are smaller (no Booming Blade / Green-Flame Blade / Magic Stone /
Catapult / Vortex Warp / Intellect Fortress / Ashardalon's Stride / Skill Empowerment / Glyph of
Warding, etc.) — but **Listo pulls the addon**, so the list above is the one in play.

**Listo widens it further.** The changelog records, in effect: *"ADDED spells from all spell mods in
Listo as options for Artificers!"*, graviturgy Wizard spells added to Artificer, Dawnstar's
Telekinetic spells added to Artificer, and **Shadow Blade and Flame Blade** added to Artificer,
Arcane Trickster and Eldritch Knight. The exact final list lives inside `Listo Master Spells Patch`
and **cannot be read from the manifest** — treat the Artificer spell list as **substantially larger
than the addon list above**, and check in-game before committing to a specific spell.
`(the specific additions are verified from the changelog; the full merged list is unverified.)`

---

## Base-class features not covered above

| Level | Feature | What it does |
|---|---|---|
| 1 | **Magical Tinkering** | Grants **Mending, Light and Minor Illusion** as always-prepared cantrips |
| 1 | **Experimental Alchemy** | See below |
| 3 | **The Right Tool for the Job** | Action, `OncePerShortRest` — conjure **thieves' tools, a trap disarming kit, or a shovel** |
| 6 | **Sleight of Hand Expertise** | Proficiency **and Expertise** in Sleight of Hand |
| 7 | **Flash of Genius** | **Reaction:** add a bonus to an ability check or saving throw made by you **or a creature you can see** |
| 10 | **Magic Item Adept** | +1 damage when you attack or cast a spell **while holding a magical weapon**; also unlocks **Alchemical Adept / Salvage Elements** — extract elements from corpses and medium objects to craft combat consumables |
| 11 | **Spell-Storing Item** | Action — create **Intelligence-modifier** scrolls per long rest from spells you know. Scrolls vanish at long rest, but you can make **different** ones and **hand them to your partner** (the README calls this out explicitly: let the martial cast Heat Metal or Web) |
| 14 | **Magic Item Savant** | Another +1 damage on the same condition, **and you ignore all class and race requirements on items** (core-game items only) |
| 18 | **Magic Item Master** | **+2** damage on the same condition (the three stack toward +4 per the README) |
| 20 | **Soul of Artifice** | **+1 to all saving throws** while holding a magic or infused weapon; while you possess a replicated magic item, if reduced to 0 HP but not killed outright you may **reaction to drop to 1 HP instead** |

> The Magic Item Adept/Savant/Master line and Soul of Artifice all key off **holding a magical
> weapon** — which Enhanced Weapon or Radiant Weapon supplies on demand. That also satisfies Battle
> Smith's Battle Ready. Never plan an Artificer without at least one weapon-magicking infusion.

---

## Experimental Alchemy

`ExperimentalAlchemy` is a **vanilla BG3 passive** (Transmutation Wizard level 2: brew **two**
solutions instead of one on a successful **Medicine** check). The Artificer mod grants it at
**Artificer level 1** — and, importantly, **on both the level-1 node and the multiclass node**, so
a late Artificer dip still delivers it.

**Sources do not stack.** Wizard + Artificer + Essential Feats' **Alchemist** feat all produce the
same 2 potions. Take **one** and spend the rest of your budget elsewhere.

See `listo-10.2-feats.md`:
- Essential Feats' **Alchemist** grants Experimental Alchemy plus a free grenade/water-bottle throw
  once per turn — that is the feat-shaped route.
- The standalone **Experimental Alchemy as a Feat** (`12446`) was **REMOVED in v9.0.3**, along with
  the Arcanist Feat. Docs page 4 still describes it; the docs are stale.

Alchemist subclass's **Alchemical Mastery** (L10) and the base class's **Alchemical Adept /
Salvage Elements** (L10) are *separate* systems from Experimental Alchemy and do stack with it.

---

## Firearms

**Artificer is the framework mod for guns in Listo 10.2.** There is no ATF / Firearms mod in the
10.2 list — the manifest contains no archive matching `Firearm`, `ATF`, `Musket` or `Blunderbus`.
An older changelog entry describing ATF-style **reloading** is therefore **superseded and does not
apply to 10.2**. Degreaser 2.0 (`15258`) lists the Artificer mod as a hard requirement "for guns to
work" (see `listo-10.2-equipment.md`).

**What Artificer contributes:**

1. **The `Firearms` proficiency group and weapon group itself.** Every gun in the list — the mod's
   own, Degreaser's, and Jasperthefae's unreleased magic-pistol pack — is defined against it.
2. **`Proficiency(Firearms)` and `Proficiency(Slings)` at Artificer 1 — on *both* the level-1 and
   the multiclass node.** A one-level Artificer dip is the cheapest documented route to firearm
   proficiency in the list. `listo-10.2-feats.md` records **no Gunner feat**; the Listo changelog
   mentions revising a Gunner feat that "should provide proficiency with firearms and correctly
   remove the point blank shot penalty", but that entry is from **v4.1** and the feat does not
   appear in the compiled 10.2 feats reference. `(unverified — confirm in-game before planning a
   non-Artificer gun build.)`
3. **Two base firearms**, as shipped by the mod (Listo then rebalances them — see below):
   - **Artillerist Pistol** — built on the hand crossbow: **1d10 piercing**, WeaponRange 15 m,
     damage range 30 m, properties Ammunition / Loading / **Light**, Rare, ~800 gp.
   - **Artificer Rifle (musket)** — built on the light crossbow: **1d12 piercing**, WeaponRange
     18 m, damage range 35 m, Ammunition / Loading / **Two-handed**, Rare, ~1600 gp.
   Both unlock **Mobile Shooting** on equip. The **Artillerist's handheld Eldritch Cannon** is
   itself a firearm item.
4. **Repeating Shot**, the only infusion written to name firearms: +1 attack/damage, self-generating
   ammunition, **two targets once per turn**, and **no Bonus Action cost at Artificer 10.**

**What Listo changes on top** (from the changelog, all pre-10.2 and still standing):
- All Artificer firearms were moved into the **Slings / MartialRangedWeapon** proficiency group so
  the feat and item ecosystem recognises them (this is why Artificer grants `Proficiency(Slings)`).
- Artificer firearms **receive identical benefits from any feats, abilities, or magic items that
  affect ranged combat**, and can **apply oils and poisons**.
- Firearms have **better damage but reduced range** than the equivalent bow/crossbow.
- The **pistol and musket were added to more vendors, ensuring Act 1/2/3 access.**

For the actual gun list, vendors (**Dammon and Roah Moonglow, Acts 1 and 2**), and the
firearms-vs-bows range trade, see the **"Firearms vs bows"** section of
`listo-10.2-equipment.md` — not restated here.

---

## Feats

Listo replaces the mod's own ASI levels (4/8/12/16/19) with `Universal Feat Every X Level(s) - MCM`
(`13193`): **feats at 3, 6, 9, 12, 15, 18** for all classes, with a seventh at **11** for
**Fighter, Rogue and Mesmerist only**. Artificer gets the standard six. Because the cadence keys off
**class level**, a 3-level Artificer dip is **feat-neutral**. See `listo-10.2-feats.md` for the full
cadence and the ability-score-cap removal.

> **Conflict on record.** A **v7.0.10** changelog entry reads *"UPDATED Universal Feats to grant a
> bonus feat at level 13, and a bonus 11th level feat for Artificers."* The **current** docs page 4
> lists no such exception (only Fighter/Mesmerist/Rogue at 11), and the compiled feats reference
> calls the cadence "unchanged in 10.2". Treat the Artificer-specific bonus feat as
> **superseded / `(unverified)`** and confirm on the level-up screen if it matters to a plan.

---

## Not present

- **No fifth subclass.** The mod ships exactly four. **`21822` "(DTO) Otherworldy Archetypes"
  contains no Artificer content** — verified from its Nexus page: 12 subclasses, one each for the
  12 *vanilla* classes (Stormcallers, Path of the Revenant, Dream Domain, Circle of Wrath,
  Chronoknight, Way of the Friar, Oath of Illumination, Conclave of the Dawnstriders, Seeker,
  Wretched Soul, The Psyker, School of Bombardment).
- **No dedicated Artificer patch mod** in the TSV. The only Artificer-adjacent entries are
  `15258 Degreaser 2.0` (requires Artificer for guns), and the alchemy-flavoured
  `22487 Mogris's Disciple` and `17864 Vera The Alchemist` — neither touches the class.
- **No ATF / Firearms mod**, so **no firearm reloading mechanic**.
- **No Artificer dialogue tag** — the class reads as **Wizard** in dialogue. The mod lists this
  as a known unfixed issue.
- **No armour-model visual change** for Armorer — the README states Armor Models are unchanged
  cosmetically; only the mechanical package differs.
- **No Armorer "armour as spellcasting focus"** — BG3 has no focus system, so the mod substituted
  Heavy Armour proficiency instead.

## Explicitly unverified

- The contents of `Listo Tweaks and Patches`, `Listo Master Spells Patch` and `Degreaser 2.0` are
  **opaque `.pak` archives**. Everything attributed to Listo above comes from the changelog or docs,
  not from reading the patch data. **Final firearm damage dice and ranges in-game will be Listo's
  rebalanced values, not the mod-shipped numbers quoted here.**
- The final merged Artificer spell list after Listo's spell-mod additions.
- Whether a **Gunner** feat exists in 10.2.
- Whether Artificer receives a bonus feat at 11 or 13.
- Whether the half-caster **round-up** passive works with Listo's *modded* caster classes (the
  README limits it to core-game spellcasters).
- Exact turn-cost/cooldown of the Eldritch Cannon and Steel Defender summons — both inherit
  `Target_RangersCompanion`, which implies Ranger's-Companion casting shape, but no explicit
  `UseCosts` or `Cooldown` is set on either entry.
