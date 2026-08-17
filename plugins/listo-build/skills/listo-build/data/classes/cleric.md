# Listonomicon 10.2 — Cleric

Cleric in Listo is the widest subclass menu in the list: **20 domains**, of which 12 are modded.
The class chassis is close to vanilla — Wisdom casting, prepared spells, Channel Divinity on a
short rest — but three things change the planning math. First, **domain choice, not class level,
decides your armour and weapon proficiencies**, so a Cleric 1 dip is worth wildly different
amounts depending on the domain. Second, `Cat's Cleric Changes` (`21257`) hands **War Domain a
real Extra Attack at level 6** and **Knowledge Domain Magical Secrets at 6 and 10**, which
invalidates the stale docs line that Clerics never get Extra Attack. Third, `Expansion` (`279`)
carries every domain to level 20 — third Channel Divinity charge at 18, and a **repeatable
Divine Intervention at 20**. `Goon's Cleric Overhaul` (`17471`) sits on top as a bug-fix and RAW
layer, and also **removes the free skill proficiencies BG3 wrongly gave a Cleric multiclass**.

**Provenance.** Compiled 17 August 2026 against the bundled 10.2 snapshot. Every domain listed
was confirmed present in `listo-10.2-mods.tsv` **and** in `listo-10.2-manifest.json` (archive
names given). Mechanics come from mod pages / implementation articles on Nexus; vanilla baselines
from bg3.wiki. In every case checked, Listo pulled the mod's **current** version. Anything not
read directly is marked `(unverified)`.

```bash
S=~/.claude/skills/listo-build     # or the plugin path

grep -i -A12 "^### Peace" "$S/data/classes/cleric.md"      # one domain
grep -i "heavy armour" "$S/data/classes/cleric.md"         # domains worth dipping
grep -i "Duo:" "$S/data/classes/cleric.md"                 # duo relevance only
```

---

## At a glance

| | |
|---|---|
| **Primary ability** | Wisdom (spell attacks, save DC, prepared-spell count) |
| **Saves at level 1** | **Wisdom + Charisma** — only granted if Cleric is your **starting** class |
| **Armour proficiency** | Light + Medium + **Shields** from the class; **Heavy armour only from the domain** (see table below) |
| **Weapon proficiency** | Simple weapons, Flails, Morningstars from the class; **Martial weapons only from the domain** |
| **Skills** | 2 from History, Insight, Medicine, Persuasion, Religion — **starting class only**. Goon's fix removes the skills a Cleric *multiclass* used to grant |
| **Resource cadence** | Spell slots: **long rest**. Channel Divinity: **short rest** (1 charge at L2, 2 at L6, 3 at L18). Most modded domain features: **long rest**, usually Wis-modifier uses |
| **Level breakpoints** | **1** domain + saves + armour. **2** Channel Divinity + Turn Undead. **5** Destroy Undead + level-3 spells. **6** second CD charge + domain feature (War: Extra Attack). **8** Divine Strike / Potent Spellcasting. **10** Divine Intervention (once per playthrough). **14** Divine Strike → 2d8. **17** domain capstone. **18** third CD charge. **20** Divine Intervention returns, **once per long rest** |
| **Dip value** | **Very high at 1** for a heavy-armour domain; **1 or 2** for Channel Divinity; **3** is feat-neutral but buys little unless you want a level-3 domain spell pair |
| **Feats** | 3, 6, 9, 12, 15, 18 (Listo cadence — see `listo-10.2-feats.md`), *not* the vanilla 4/8/12 |

---

## Class changes from vanilla

### `Goon's Cleric Overhaul` — `17471`, archive `Goon's Cleric Overhaul-17471-1-0-5-1`

A bug-fix and rules-as-written pass over the whole class. The parts that change decisions:

- **Cleric multiclass no longer grants extra skills.** BG3's progression merge was handing a
  Cleric dip two skill proficiencies it shouldn't have. **A Cleric dip now gives you no skills.**
  Requires Compatibility Framework for this fix.
- **Divine Strike** (all domains, vanilla and modded):
  - The spell variants **only expend the once-per-turn charge on a hit** (mirrors Divine Smite;
    tooltip says "Does not consume a Divine Strike charge" on a miss).
  - Spell variants now **execute weapon functors**, so weapon damage riders apply to them.
  - Damage **scales to 2d8 at Cleric level 14** even without Expansion.
  - Interrupts usable while **Invisible** and under most non-hostile Polymorphs.
  - The `IsDivineStrike` function was extended to cover the custom Divine Strikes from
    **5e Cleric Subclasses Combined** and **Expansion**, so those get the same fixes.
- **Blessed Healer** (Life) now **only heals the caster**, as the tooltip always claimed —
  previously it fired off every healing source on everyone. This is a **nerf** if you were
  relying on the buggy behaviour.
- **Disciple of Life** (Life) re-implemented RAW; Restore Vitality must heal >0 for the bonus to
  apply. An ExtraDescription confirms **Aura of Vitality (Warden of Vitality) works with it**.
- **Destructive Wrath** (Tempest) triggers **when damage is dealt** rather than when the spell is
  cast, so it is no longer wasted on a spell that misses or deals no damage.
- **Blessing of the Trickster** (Trickery): **concentration removed** (RAW).
- **Guided Strike / War God's Blessing** (War) and **Wrath of the Storm** (Tempest): usable while
  Invisible and under more Polymorphs.

### `Cat's Cleric Changes` — `21257`, archive `CCC - Cat's Cleric Changes-21257-1-00`

Written **specifically for Listonomicon**. Two lines, both large:

- **Knowledge Domain gains Magical Secrets at levels 6 and 10.**
- **War Domain gains Extra Attack at level 6.**

> This is the single most important Listo-specific Cleric fact. The docs page still says Clerics
> get "neither Extra Attack nor War Priest extra attack" — **that is stale for War Domain.**

### `Expansion` — `279`, archive `Expansion-279-1-7-3-6` (the level 13–20 mod)

- **Channel Divinity: third charge at level 18.**
- **Divine Intervention at 20**: the feature is granted **again** and is **usable once per long
  rest** (BG3's level-10 version is once per playthrough — Sunder the Heretical / Arm Thy Servant
  / Opulent Revival).
- **Divine Strike 14th-level upgrade** implemented for Tempest, Trickery and War.
- **Optional, MCM-toggled** (default enabled; the player can turn each off in Mod Configuration
  Menu — **ask them what they run**):
  - **Harness Divine Power** (L2): bonus action, spend a Channel Divinity charge to **regain one
    spell slot** of level ≤ half proficiency bonus. Uses: 1 at L2, 2 at L6, 3 at L18, per long rest.
  - **Cantrip Versatility**: swap a cantrip at ASI levels.
  - **Blessed Strikes** (L8): **replaces** Divine Strike *or* Potent Spellcasting — 1d8 radiant
    when a creature takes damage from your **cantrips or weapon attacks**, once per turn. Offered
    as a choice to each subclass.
- **17th-level capstones** for vanilla domains: Improved Reaper (Death), Divine Foreknowledge
  (Knowledge — the 2024 version: bonus action, **advantage on all d20 tests for 1 hour**, once
  per long rest, refreshable with a level 6+ slot), Supreme Healing (Life), Corona of Light
  (Light), Master of Nature (Nature), Stormborn (Tempest), Improved Duplicity (Trickery),
  Avatar of Battle (War).
- Expansion's own "extra feat at 16 and 19" is **not** the Listo cadence; feats come from
  `Universal Feat Every X Level(s)` — see `listo-10.2-feats.md`.

### Spells and other cross-class changes that hit Cleric

- **`5e Spells` (`125`) is installed; Mystra's Spells is NOT.** Several modded domain spell lists
  offer a spell "from 5e Spells **or** Mystra's" — those resolve. Entries listed as
  **Mystra's-only** do **not**: *Ego Whip* (Order, L7) and *Aura of Purity* (Peace, L7) will be
  missing or substituted `(unverified which substitute appears in-game)`.
- **Shillelagh** was reworked list-wide: applies to **Club, Quarterstaff, Mace, Morningstar,
  Sickle, Spear, Trident**, is now a **level 1 spell** (not a cantrip), and per changelog v9.0.3
  **must be re-cast after a Long Rest**; it was **added as a domain spell for Nature Clerics**.
  `(conflict: docs page 4 and listo-10.2-feats.md both describe Shillelagh as a permanent effect;
  the changelog entry is more specific. Verify in-game before planning around uptime.)`
- **The `Arcanist` feat is REMOVED** from the list. The routes to Shillelagh for a non-Nature
  Cleric are now Essential Feats' **Magic Initiate / Eldritch Adept** line or the **Druidic
  Warrior** fighting style from UA Fighting Styles — both documented in `listo-10.2-feats.md`.
- **`War Magic`** (Essential Feats) is the feat the docs single out for Clerics: cast, then swing
  as a bonus action, every turn. See `listo-10.2-feats.md` for the exact wording and the level-5
  half-damage clause.
- **`Multiclass Preferred Casting Ability Fix`** (`10209`) stops a Cleric dip from stealing your
  "Spellcasting Stat" — the classic Sorcerer 19 / Tempest Cleric 1 no longer has Wisdom assigned
  as its casting stat for scrolls and items.
- **Deity choice** is cosmetic. `Gods Extra` (`433`) and `Faithful and Faithless` (`1512`) add
  choices with **no mechanics and no new dialogue**; `Origin Gods SE - MCM` (`20583`) lets you
  reassign companion deities (Shadowheart's is locked). Individual deity mods (Bane `5904`,
  Bhaal `5894`, Myrkul `5906`, Shar `6198`, Jergal `6571`, Silvanus `6591`) restore cut dialogue.
- **Healing is worth more than usual here.** `Hardcore Healing Potions` (`15391`) and
  `No Free NPC Heals` (`12906`) are both installed — see `listo-10.2-equipment.md` and the
  skill's rules file. Long rests cost 120+ camp supplies and scale up.

### `Blessing of the Trickster` (`11566`) is **NOT in 10.2**

The docs page 4 Cleric section still recommends it. **It is absent from both the mod list TSV and
the manifest.** What Trickery actually gets in 10.2 is Goon's version: **BotT without
concentration**. It does **not** apply to extra skills and is **not** usable in dialogue. Plan
Trickery accordingly.

---

## Domains (subclasses)

**20 domains total: 8 vanilla, 12 modded.**

### Heavy armour / martial weapon table (the dip-planning summary)

| Domain | Source | Heavy armour | Martial weapons | Other L1 proficiency |
|---|---|---|---|---|
| Death | vanilla | – | **yes** | – |
| Knowledge | vanilla | – | – | 2 skills at **double** bonus (Arcana/History/Nature/Religion) |
| Life | vanilla | **yes** | – | – |
| Light | vanilla | – | – | – |
| Nature | vanilla | **yes** | – | 1 of Animal Handling / Nature / Survival |
| Tempest | vanilla | **yes** | **yes** | – |
| Trickery | vanilla | – | – | – |
| War | vanilla | **yes** | **yes** | – |
| Arcana | `16007` | – | – | Arcana + **2 wizard cantrips** |
| Forge | `16007` | **yes** | – | Sleight of Hand (stands in for smith's tools) |
| Grave | `16007` | – | – | Spare the Dying as a bonus free cantrip |
| Order | `16007` | **yes** | – | Intimidation **or** Persuasion |
| Peace | `16007` | – | – | Insight / Performance / Persuasion (choose 1) |
| Twilight | `16007` | **yes** | **yes** | – |
| Strength | `9054` | **yes** | – | 1 druid cantrip + 1 of Animal Handling/Athletics/Nature/Survival |
| Zeal | `9089` | **yes** | **yes** | – |
| Inquisition | `8931` | **yes** | **yes** | – |
| Eldritch | `15357` | – | – | any cantrip (free) + any skill, both re-selectable each long rest |
| Night | `15443` | – | – | Darkvision 18m |
| Dream | `21822` | – | – | Mind Sliver as a Wis-based Cleric cantrip |

**Ten domains grant heavy armour:** Life, Nature, Tempest, War, Forge, Order, Twilight, Strength,
Zeal, Inquisition. **Six grant martial weapons:** Death, Tempest, War, Twilight, Zeal,
Inquisition. **Five grant both:** Tempest, War, Twilight, Zeal, Inquisition.

---

### Death
- **Mod:** vanilla (playable base-game domain), extended by `Control Undead for Death Domain Cleric` (`16140`) and `Expansion` (`279`)
- **File pulled:** `Control Undead for Death Domain Cleric-16140-1-0` (mod page shows no newer version)
- **Mechanics:** L1 **Reaper** + domain spells False Life, Ray of Sickness, choice of Bone Chill /
  Bursting Sinew / Toll the Dead. L2 Channel Divinity **Touch of Death**. `16140` adds the
  Oathbreaker **Control Undead** Channel Divinity action to the domain. L8 Divine Strike
  (necrotic; Goon added the missing level-14 map for the crit variant). L17 **Improved Reaper**
  from Expansion — necromancy spells of level 1–5 that target one creature hit **two** creatures
  within 1.5m, with a Passives-tab toggle to switch it off.
- **Proficiency:** martial weapons. **No heavy armour.**
- **Duo:** Control Undead converts an enemy into a third body, which is the one thing a two-person
  party is structurally short of. Costs a Channel Divinity charge, so it competes with Turn Undead.

### Knowledge
- **Mod:** vanilla, buffed by `CCC - Cat's Cleric Changes` (`21257`) and `Expansion` (`279`)
- **Mechanics:** L1 **Blessings of Knowledge** — Command, Sleep, and **double proficiency bonus in
  2 of Arcana/History/Nature/Religion**. L2 Channel Divinity **Knowledge of the Ages**.
  **L6 and L10: Magical Secrets** (from CCC — pick spells from any class list)
  `(the exact pick count and list are not stated on the CCC page — unverified)`.
  L17 **Divine Foreknowledge** (Expansion, 2024 version): bonus action, **advantage on all d20
  tests for 1 hour**, once per long rest, refreshable by spending a level 6+ slot.
- **Proficiency:** none beyond the class. Light/medium armour only.
- **Duo:** Magical Secrets at 6 turns the Cleric into the party's utility answer — Counterspell,
  Haste, Revivify from another list — which matters when there is no third character to cover
  gaps. Divine Foreknowledge at 17 is an hour of advantage on everything.

### Life
- **Mod:** vanilla, heavily patched by `Goon's Cleric Overhaul` (`17471`), capstone from `Expansion`
- **Mechanics:** L1 **Disciple of Life** (healing spells of level 1+ heal an extra 2 + spell level;
  Goon re-implemented RAW and confirmed it works with **Warden of Vitality / Aura of Vitality**),
  domain spells Cure Wounds and Bless. L2 Channel Divinity **Preserve Life**. L6 **Blessed
  Healer** — **now heals only the caster** when you heal others (Goon bug fix; the old behaviour
  was much stronger). L8 Divine Strike (radiant). L17 **Supreme Healing** (Expansion): all healing
  dice roll maximum.
- **Proficiency:** **heavy armour**, no martial weapons.
- **Duo:** the default answer to "we cannot afford to lose either character." Supreme Healing at
  17 plus maximised Cure Wounds/Heal is the strongest sustain in the list, and healing potions are
  nerfed specifically to make this matter.

### Light
- **Mod:** vanilla, capstone from `Expansion`
- **Mechanics:** L1 **Warding Flare** (reaction: impose disadvantage on an attack against you),
  domain spells Light, Burning Hands, Faerie Fire. L2 Channel Divinity **Radiance of the Dawn**.
  L6 Improved Warding Flare (protects allies). L8 **Potent Spellcasting** (add Wis to cantrip
  damage). L17 **Corona of Light** (Expansion): 1-minute aura, enemies in the bright light have
  **disadvantage on saves against fire and radiant spells**.
- **Proficiency:** none beyond the class.
- **Duo:** Warding Flare uses a reaction, and Lone Wolf grants an **extra reaction** — so Light can
  flare twice per round without giving up an opportunity attack or a Shield.

### Nature
- **Mod:** vanilla, capstone from `Expansion`; Shillelagh added as a domain spell by Listo's own patch
- **Mechanics:** L1 **Acolyte of Nature** — Speak with Animals, Animal Friendship, one of Poison
  Spray / Produce Flame / **Shillelagh** / Thorn Whip, plus a skill from Animal Handling / Nature
  / Survival. Listo additionally **makes Shillelagh a Nature Domain spell** (and Shillelagh is now
  a level-1 spell, not a cantrip). L2 Channel Divinity **Charm Animals and Plants**. L8 Divine
  Strike (cold/fire/lightning). L17 **Master of Nature** (Expansion): bonus action to command
  charmed creatures, which Expansion implements as taking control of them like a summon.
- **Proficiency:** **heavy armour** + a nature skill.
- **Duo:** the only domain with **built-in Shillelagh access**, so a Wisdom melee build needs no
  feat tax. Master of Nature is a temporary third body.

### Tempest
- **Mod:** vanilla, patched by `Goon's Cleric Overhaul`, capstone from `Expansion`
- **Mechanics:** L1 **Wrath of the Storm** (reaction damage when hit in melee; Goon fixed
  Polymorph and Blinded interactions), domain spells Thunderwave, Fog Cloud. L2 Channel Divinity
  **Destructive Wrath** — maximise thunder/lightning damage; **Goon moved the trigger to when
  damage is dealt** so it is not wasted, and Listo separately made it stop spamming confirmations
  on AoE. L6 Thunderbolt Strike. L8 Divine Strike (thunder, → 2d8 at 14 via Expansion). L17
  **Stormborn**: flying speed equal to walking speed when not underground or indoors.
- **Proficiency:** **heavy armour + martial weapons.**
- **Duo:** the classic 1-level dip for a Sorcerer — heavy armour, shields, martial weapons and
  maximised lightning, with `Multiclass Preferred Casting Ability Fix` protecting the casting stat.

### Trickery
- **Mod:** vanilla, patched by `Goon's Cleric Overhaul`, capstone from `Expansion`
- **Mechanics:** L1 **Blessing of the Trickster** — advantage on Stealth for a target;
  **concentration removed by Goon**. Domain spells Charm Person, Disguise Self. L2 Channel
  Divinity **Invoke Duplicity** (Goon deliberately left it alone). L8 Divine Strike (poison,
  → 2d8 at 14). L17 **Improved Duplicity** (Expansion): **up to four duplicates**, moved with a
  bonus action.
- **Proficiency:** none beyond the class. This is the weakest chassis of the eight vanilla domains.
- **Duo:** four duplicates at 17 is real action-economy value — enemies spread attacks across
  decoys. Before then Trickery gives a two-person party very little, and **the Listo BotT buff mod
  the docs recommend is not installed**.

### War
- **Mod:** vanilla, buffed by `CCC - Cat's Cleric Changes` (`21257`), patched by Goon, capstone from `Expansion`
- **Mechanics:** L1 **War Priest** — spend a War Priest Charge to attack as a **bonus action**;
  3 charges per long rest, 4 at L5, 5 at L8, 6 at L11. Domain spells Divine Favour, Shield of
  Faith. L2 Channel Divinity **Guided Strike** (+10 to an attack roll; Goon made it work while
  Invisible/Polymorphed). **L6: Extra Attack (CCC)** plus War God's Blessing. L8 Divine Strike
  (weapon's damage type, → 2d8 at 14). L17 **Avatar of Battle** (Expansion): resistance to
  non-magical bludgeoning/piercing/slashing.
- **Proficiency:** **heavy armour + martial weapons.**
- **Duo:** the only domain with true **Extra Attack**, and War Priest stacks on top of it —
  attack, attack, bonus-action attack. With Lone Wolf's extra Action and Bonus Action this is the
  highest raw swing count any Cleric can reach, and it makes War Magic a lower priority here than
  for other domains.

---

### Arcana
- **Mod:** `5e Cleric Subclasses Combined` (`16007`) by Sumradagnoth
- **File pulled:** `ClericSubclasses5eCombined.zip-16007-1-6-2-1` — **v1.6.2.1, the current version**
- **Mechanics:** L1 **Arcane Initiate** — Arcana proficiency + **two wizard cantrips that count as
  Cleric cantrips**. Domain spells: Detect Magic/Magic Missile (1), Magic Weapon/Blur (3),
  Dispel Magic/Counterspell/Magic Circle (5), Arcane Eye/Otiluke's Resilient Sphere (7),
  Planar Binding/Teleportation Circle (9). L2 Channel Divinity **Arcane Abjuration** — turn a
  celestial/elemental/fey/fiend; from L5 it **banishes** creatures at or below a level threshold
  (BG3 has no CR, so it keys off target level: L5 → CR ½, L8 → 1, L11 → 2, L14 → 3, L17 → 4).
  L6 **Spell Breaker** — reimplemented: healing an ally with a level 1+ slot grants them a **bonus
  to saves vs spells equal to the slot level** until their next such save. L8 **Potent
  Spellcasting** — applies to **any** cantrip, not just Cleric ones. L17 **Arcane Mastery**: add a
  6th/7th/8th/9th-level wizard spell as always-prepared domain spells (needs 5e Spells).
- **Proficiency:** none beyond the class.
- **Duo:** the only domain that gives a Cleric **Counterspell** natively — in a two-person party
  there is no wizard to hold that reaction, and Lone Wolf's extra reaction pays for it.

### Forge
- **Mod:** `5e Cleric Subclasses Combined` (`16007`)
- **Mechanics:** L1 **Blessing of the Forge** — after a long rest, touch a creature (target the
  character, not the item) to give armour **+1 AC** or a weapon **+1 attack and damage**; works on
  magical items too, not just nonmagical. Domain spells: Burning Hands/Searing Smite (1),
  Heat Metal/Magic Weapon (3), Elemental Weapon/Protection from Energy (5), Summon Construct/Wall
  of Fire (7), Holy Weapon/Skill Empowerment (9). L2 Channel Divinity **Artisan's Blessing** —
  craft nonmagical weapons/armour/tools under 100gp out of combat, **plus** a reaction that lets
  you or an ally **bypass bludgeoning/piercing/slashing resistance** when attacking with a metal
  weapon or against a metal-armoured target. L6 **Soul of the Forge**: fire resistance and
  **+1 AC in heavy armour**. L8 Divine Strike (fire). L17 **Saint of Forge and Fire**: fire
  immunity, and in heavy armour **resistance to non-magical physical damage**.
- **Proficiency:** **heavy armour** + Sleight of Hand (the mod's stand-in for smith's tools).
- **Duo:** the most durable Cleric on the list — +1 AC on top of heavy armour, then physical
  resistance at 17. The resistance-bypass reaction also fixes the "spread of damage types" problem
  the economy section warns about. Note Listo's 4× merchant prices make Artisan's Blessing's
  crafting slightly less useless than the author assumes.

### Grave
- **Mod:** `5e Cleric Subclasses Combined` (`16007`) — replaced Hav's standalone Grave Domain
- **Mechanics:** L1 **Circle of Mortality** — healing a creature **at 0 HP uses maximum dice**;
  you also learn **Spare the Dying** free (requires 5e Spells), at 30ft range and castable as a
  **bonus action**. L1 **Eyes of the Grave** — detect undead, Wis-modifier uses per long rest; the
  implementation also **reveals hiding undead, blocks them from hiding or turning invisible for 2
  turns, and gives them disadvantage on attacks**. Domain spells: Bane/False Life (1), Wither and
  Bloom/Ray of Enfeeblement (3), Revivify/Vampiric Touch (5), Blight/Death Ward (7), Antilife
  Shell/Raise Dead (9). L2 Channel Divinity **Path to the Grave** — cursed target takes
  **vulnerability to all damage** from the next hit. L6 **Sentinel at Death's Door** — reaction,
  **turn a critical hit against you or an ally into a normal hit**, Wis-modifier uses per long
  rest. L8 Potent Spellcasting. L17 **Keeper of Souls** — enemies dying within 9m heal you or an
  ally (approximates hit dice; unreliable outside combat).
- **Proficiency:** none beyond the class.
- **Duo:** **Sentinel at Death's Door is the best defensive feature in this file for a two-person
  party** — the failure mode is one character getting critically hit and dropping, and this
  deletes that outcome several times per long rest, using a reaction Lone Wolf gives you spare.
  Path to the Grave doubles as a burst-damage enabler for your partner's biggest hit.

### Order
- **Mod:** `5e Cleric Subclasses Combined` (`16007`)
- **Mechanics:** L1 **Voice of Authority** — when you cast a level 1+ spell **targeting an ally**,
  that ally makes **one weapon attack as a reaction**. Implementation: the ally attacks a random
  enemy in range of their active weapon; if you targeted several allies you pick which one reacts,
  and only one does. (v1.6.2.0 was a total rework of this feature; v1.6.2.1 fixed a stats error —
  both are in the pulled build.) Domain spells: Command/Heroism (1), Hold Person/Zone of Truth (3),
  Mass Healing Word/Slow (5), Compulsion/Freedom of Movement/**Ego Whip (Mystra's — not
  installed)** (7), Skill Empowerment/Dominate Person (9). L2 Channel Divinity **Order's Demand** —
  AoE charm on a Wis save, and failures **drop their active weapon**. L6 **Embodiment of the Law**
  — cast an **enchantment spell as a bonus action**, Wis-modifier uses per long rest, controlled by
  a toggle. L8 Divine Strike (psychic). L17 **Order's Wrath** — Divine Strike curses the target;
  the next ally hit deals **+2d8 psychic**. (Cursing is automatic, not a choice.)
- **Proficiency:** **heavy armour** + Intimidation or Persuasion.
- **Duo:** the single best action-economy domain in a two-player run. **Every buff or heal you put
  on your partner buys a free weapon attack from them**, every turn, at no resource cost — that is
  a structural fix for exactly the problem a two-person party has. Order's Wrath at 17 keys off
  "one of your allies hits," which with one partner is entirely reliable.

### Peace
- **Mod:** `5e Cleric Subclasses Combined` (`16007`)
- **Mechanics:** L1 **Emboldening Bond** — bond up to **proficiency-bonus** willing creatures for
  10 minutes; while bonded creatures are within 9m of each other, each may add a **d4 to an attack
  roll, ability check or saving throw once per turn**. Proficiency-bonus uses per long rest.
  L1 **Implement of Peace** — Insight, Performance or Persuasion. Domain spells:
  Heroism/Sanctuary (1), Aid/Warding Bond (3), Beacon of Hope/Motivational Speech (5),
  **Aura of Purity (Mystra's — not installed)**/Otiluke's Resilient Sphere (7), Greater
  Restoration/Dispel Evil and Good (9). L2 Channel Divinity **Balm of Peace** — move your full
  speed without provoking, healing **2d6 + Wis** to each creature you pass within 1.5m.
  L6 **Protective Bond** — when a bonded creature is about to take damage, another bonded creature
  within 9m can use its **reaction to teleport adjacent and take all the damage instead**.
  L8 Potent Spellcasting. L17 **Expansive Bond**: range to 18m, and the interceptor takes the
  damage **with resistance**.
- **Proficiency:** none beyond the class. Light/medium only — the weakest armour of the
  strong domains.
- **Duo:** with exactly two characters the bond is always fully online: **a permanent d4 to every
  attack, check and save on both of you**, plus a damage-redirect that lets the durable character
  eat the hit that would drop the fragile one. At 17 that redirect halves the damage. Note the
  author's caveat that multiple Peace Clerics bonding at once is unsupported — irrelevant for a
  duo unless both players go Peace.

### Twilight
- **Mod:** `5e Cleric Subclasses Combined` (`16007`)
- **Mechanics:** L1 **Eyes of Night** — darkvision 90m, shareable with Wis-modifier allies for an
  hour (once per long rest, or spend any slot to share again). L1 **Vigilant Blessing** — touch a
  creature to give **+3 initiative** on its next roll (implemented as a flat bonus, not advantage).
  Domain spells: Faerie Fire/Sleep (1), Moonbeam/See Invisibility (3), Aura of Vitality/Catnap (5),
  Aura of Life/Greater Invisibility (7), Circle of Power/Mislead (9). L2 Channel Divinity
  **Twilight Sanctuary** — a 9m sphere centred on you for 1 minute; whenever any creature ends its
  turn inside, you grant it **1d6 + Cleric level temporary HP** *or* **end one charm or fright
  effect** on it. The "dim light" is VFX only, but you are immune to overlapping magical darkness
  inside as RAW. L6 **Steps of Night** — bonus action **flight** for 1 minute in dim light or
  darkness, proficiency-bonus uses per long rest. L8 Divine Strike (radiant). L17 **Twilight
  Shroud** — you and allies have **half cover** inside the sanctuary.
- **Proficiency:** **heavy armour + martial weapons.**
- **Duo:** Twilight Sanctuary is a per-round temp-HP tap on both characters for a **single Channel
  Divinity charge that a short rest refunds** — exactly the resource profile a 120-supply long rest
  economy rewards. The charm/fright cleanse covers the crowd-control losses a two-person party
  cannot absorb. Expect UI noise: the end-of-turn effects are implemented as interrupts.

---

### Strength (Rhonas)
- **Mod:** `Amonkhet - Strength Domain - Cleric Subclass` (`9054`), from *Plane Shift: Amonkhet*
- **File pulled:** `RhonasStrengthDomain-9054-1-2-1` — **v1.2.1, the current version**
  (the page also offers a separate level-12-only file; the main archive is the one pulled)
- **Mechanics:** L1 **Bonus Proficiency**: heavy armour. L1 **Acolyte of Strength**: one **druid
  cantrip** + one of Animal Handling / Athletics / Nature / Survival. Domain spells:
  Divine Favour/Shield of Faith (1), Enhance Ability/Protection from Poison (3), **Haste**/
  Protection from Energy (5), Dominate Beast/Stoneskin (7), Destructive Wave/Insect Plague (9).
  L2 Channel Divinity **Feat of Strength**: **+10 to a Strength attack roll, check or save**.
  L2 **Avatar of Battle I**: Enlarge-like transform (no size/weight change) — **+1d4 weapon
  damage, advantage on Strength checks and saves, 3 turns**, 1 charge per long rest.
  L6 Channel Divinity **Rhonas' Blessing**: reaction, **+10** to an ally's Strength roll within 9m.
  L6 **Avatar of Battle II**: adds **resistance to non-magical physical damage** during the
  transform, damage bonus to 1d6. L8 Divine Strike (weapon's type). L10 second Avatar charge.
  L17 **The Avatar of Battle**: permanent resistance to non-magical bludgeoning/piercing/slashing.
- **Proficiency:** **heavy armour**, **no martial weapons** — an odd gap for a Strength domain.
- **Duo:** the only Cleric domain with **Haste on its own list**, and Haste is the strongest
  action-economy spell in the game for a two-person party. `(Whether the L1 druid cantrip can
  still pick Shillelagh is unverified — Listo converted Shillelagh into a level-1 spell, so it may
  no longer appear in a cantrip picker.)`

### Zeal (Hazoret)
- **Mod:** `Amonkhet - Zeal Domain - Cleric Subclass` (`9089`), from *Plane Shift: Amonkhet*
- **File pulled:** `Zeal Domain 1.3.0-9089-1-3-0` — **v1.3.0, the current version.** Compatibility
  Framework and merged progression supported natively; **progression written to level 20**
- **Mechanics:** L1 **Bonus Proficiencies**: **martial weapons and heavy armour**. L1 **Priest of
  Zeal** — a copy of War Priest: when you take the Attack action, make **one weapon attack as a
  bonus action**, **Wis-modifier uses per long rest** (minimum 1). Domain spells: Searing
  Smite/Thunderous Smite (1), Magic Weapon/Shatter (3), **Haste**/Fireball (5), Fire Shield/Freedom
  of Movement (7), Destructive Wave/Flame Strike (9). L2 Channel Divinity **Consuming Fervor** —
  **maximise fire or thunder damage** (Tempest's Destructive Wrath, and Listo separately patched
  it to stop spamming confirmations on AoE casts). L6 **Resounding Strike** — thunder damage pushes
  Large-or-smaller creatures 3m; has a toggle. L8 Divine Strike (weapon's type, magical, 2d8 at 14;
  the mod also fixes the base-game multi-trigger bug). L17 **Blaze of Glory** — once per long rest,
  when an enemy drops you to 0, that attacker takes **5d10 fire + 5d10 thunder**; toggleable passive.
- **Proficiency:** **heavy armour + martial weapons.**
- **Duo:** the best "second martial" Cleric — heavy armour, martial weapons, a bonus-action attack
  from level 1, **Haste and Fireball on the domain list**, and maximised Fireball via Consuming
  Fervor. If your partner is a caster, this is the domain that makes the Cleric the front line
  without giving up spellcasting.

### Inquisition
- **Mod:** `Inquisition Domain Cleric Subclass` (`8931`), from Ghostfire Gaming's *Grim Hollow*
- **File pulled:** `Inquisition Domain Cleric Subclass-8931-1-3` — **v1.3, the current version**
- **Mechanics:** L1 **Bonus Proficiencies**: **martial weapons and heavy armour**. L1 **Witch
  Hunter's Strike** — on a weapon hit, deal **+1d8 force**, or **+2d8 force and gain 2d8 temporary
  HP** if the target is **concentrating on a spell**. **Wis-modifier uses per long rest**;
  increases to 2d8/3d8 at L14. Domain spells: Command/Bane (1), See Invisibility/Silence (3),
  Crusader's Mantle/Remove Curse (5), Arcane Eye/Banishment (7), Dominate Person/Flame Strike (9).
  L2 Channel Divinity **Spell Shield** — bonus action, give a creature within 9m **1d10 + Cleric
  level temp HP**; while it holds those temp HP it has **resistance to spell damage and advantage
  on saves against spells**. L6 **Rebuke Invoker** — reaction when a creature within 18m casts a
  spell: Con save or take **1d8 per slot level + Wis** force damage (half on success), Wis-modifier
  uses per long rest. L8 Divine Strike (force). L17 **Spell Shield on up to five targets**.
- **Proficiency:** **heavy armour + martial weapons.**
- **Caveat from the author:** Witch Hunter's Strike **does not stack with the Divine Strike
  interrupt** — from L8 you must manually use the Divine Strike action instead of a normal attack
  to get both riders on one swing.
- **Duo:** Listo's own changelog flags this as expected top-tier, on par with Life and Tempest.
  Spell Shield is the cleanest answer to enemy casters, and in a two-person party one Channel
  Divinity charge covering your partner is 50% of the team. Rebuke Invoker is a reaction sink for
  Lone Wolf's spare reaction.

### Eldritch
- **Mod:** `Eldritch Domain Cleric Subclass` (`15357`), from *Grim Hollow*
- **File pulled:** `Eldritch Domain Cleric Subclass-15357-1-1` — **v1.1, the current version**
- **Mechanics:** L1 **Unpredictable Inspiration** — **any base-game cantrip free** (does not count
  against known cantrips) **and any skill proficiency**, both swappable each long rest. L1
  **Eldritch Contagion** — when you cast a level 1+ spell at one or more creatures, use a **bonus
  action** to force one target to make a Wis save or suffer a random **Eldritch Effect** for 1
  minute (re-save at end of each of its turns). Only one target can be affected at a time. Domain
  spells: Tasha's Hideous Laughter/Sleep (1), Detect Thoughts/See Invisibility (3), Fear/Slow (5),
  Confusion/Phantasmal Killer (7), Dominate Person/Planar Binding (9). L2 Channel Divinity
  **Prophecy of Doom** — 5m-radius sphere at 27m, **every** creature that fails a Wis save gets a
  random Eldritch Effect. L6 **psychic resistance, advantage on saves vs Charmed and Frightened**,
  and anyone who deals psychic damage to you takes **psychic damage equal to your Cleric level** on
  a failed Wis save. L8 **Potent Spellcasting** (also boosts the free cantrip). L17: creatures
  failing Prophecy of Doom take **10d10 psychic**, once per creature.
- **Eldritch Effects table (1 minute each):** Silenced; 1d8 psychic at the start of its turns;
  falls Prone repeatedly; disadvantage on attacks and Perception; **can move OR act, not both, and
  no reactions**; advantage on its attacks but attacks against it also have advantage; partially
  Blinded past 7m; Frightened.
- **Proficiency:** none beyond the class.
- **Duo:** Prophecy of Doom is the widest crowd control on this list from one Channel Divinity
  charge, and "move or act, not both, no reactions" is an action-economy tax on the enemy — the
  mirror image of what Lone Wolf gives you. The random table makes it unreliable for a specific plan.

### Night
- **Mod:** `Night Domain Cleric Subclass` (`15443`), from *Humblewood*
- **File pulled:** `Night Domain Cleric Subclass-15443-1-1` — **v1.1, the current version**
- **Mechanics:** L1 **Darkvision 18m** (37m at L6; see in magical darkness at L8; **Truesight 37m
  in darkness, once per long rest, at L17**). L1 **Ward of Shadows** — reaction: impose
  **disadvantage** on an attack against you from a creature within 9m (fails against enemies that
  cannot be Blinded); at L6 it also protects **allies**. Domain spells: Sleep/**Veil of Dusk*** (1),
  Darkness/Moonbeam (3), Fear/Fly (5), Greater Invisibility/**Stellar Bodies*** (7), Dispel Good
  and Evil/Seeming (9). L2 Channel Divinity **Invocation of Night** — extinguishes all mundane and
  magical light within 9m (dispels Light, Faerie Fire, Guiding Bolt, Burning, etc.) and Blinds
  enemies that fail a Con save for **rounds equal to your Cleric level**. L8: **Sleep gains +14 HP
  of effect** and sleepers cannot be woken until the start of your next turn — and Sleep makes
  everything within 1.5m a critical hit. L17: 1-minute 9m aura that **Blinds and Frightens** every
  enemy inside, once per long rest.
- **Two new spells** ship with the mod and were added to class lists in v1.1: **Veil of Dusk**
  (level 1, concentration: +1 AC and advantage on Stealth; also on Druid/Warlock lists) and
  **Stellar Bodies** (level 4: two orbiting stars that punish melee attackers with 1d8 radiant
  each, or can be fired for 4d8 radiant + Blind; more stars when upcast, up to 4 at level 9; also
  on Cleric/Druid/Sorcerer/Wizard lists).
- **Proficiency:** none beyond the class.
- **Duo:** Ward of Shadows is the same reaction-defence pattern as Light's Warding Flare, and Lone
  Wolf's extra reaction means it and an opportunity attack both fit in a round. The author pitches
  it as the better Shadowheart subclass than Trickery, which is true in 10.2 given the Trickery
  buff mod was dropped.

### Dream
- **Mod:** `(DTO) Otherworldy Archetypes` (`21822`), Volume 1 of *Daelen's Testament of the
  Otherworldly* — a 12-subclass pack, one per class
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67` (2026-06-17)
- **Mechanics** (from the DTO documentation site): L1 **Deep Slumber** — level 1 spell, action,
  18m range, 2m radius, Wis save: targets sleep until the end of their next turn and wake with
  **Torpor** for 1 turn (creatures immune to Sleep get Torpor immediately). **Torpor: quarter
  movement, no reactions, and only ONE of attack/action/bonus action** — damage breaks it. Upcast
  extends Torpor. L1 **Mind Sliver** as a Wisdom-based Cleric cantrip. Additional spells known:
  Deep Slumber/Dissonant Whispers (1), Calm Emotions/Phantasmal Force (3), Hypnotic Pattern/Fear
  (5), Confusion/Phantasmal Killer (7), Synaptic Static/Dream (9). L2 **Inception** — passive
  toggle: targets of your Int- or Wis-save spells have **disadvantage on their first save**;
  consumes your Channel Divinity when the spell is cast. L6 **Nightmare** — reaction when a nearby
  foe fails a Wis or Int save: **2d10 + level psychic**, Wis-modifier uses per long rest, +1d10 at
  Cleric 11 and 17. L8 **Potent Spellcasting**. L17 **The Third Eye** — psychic damage you deal
  sometimes makes the target **vulnerable to psychic** until the end of your next turn.
- **Proficiency:** none stated — light/medium armour, no martial weapons `(unverified: the DTO
  page lists no bonus proficiencies for the domain)`.
- **Duo:** Torpor is a hard action-economy debuff — a Torpored enemy gets one action instead of
  the action/bonus/reaction suite, which is the same lever Lone Wolf pulls in your favour.
  Inception makes your saving-throw spells land, which matters when there is no second controller
  in the party. **Note the pack recommends 5e Spells specifically for Dream Domain** — 5e Spells
  is installed, so this is satisfied.

---

## Dip value

**Cleric 1 is one of the best dips in the list, but only for the right domain.**

What one level buys:

- **Wisdom and Charisma saving throw proficiencies** — but **only if Cleric is your level 1
  class**. This is the Cleric's single best structural offer: Wis and Cha are the two save types
  that carry the fight-losing effects (Hold Person, Fear, Banishment, Dominate). Starting Cleric
  and then building elsewhere buys both.
- **Light + medium armour and shields** from the class.
- **Heavy armour from the domain** — for **Life, Nature, Tempest, War, Forge, Order, Twilight,
  Strength, Zeal, Inquisition**. This is the reason to dip on a Sorcerer, Warlock or any Dex-light
  caster.
- **Martial weapons from the domain** — **Death, Tempest, War, Twilight, Zeal, Inquisition**.
- **The domain's whole level-1 feature set**, which for several modded domains is substantial:
  Zeal's bonus-action attack, Inquisition's Witch Hunter's Strike, Peace's Emboldening Bond,
  Order's Voice of Authority, Grave's max-healing-at-0-HP, Arcana's two wizard cantrips.
- **Domain spells always prepared**, plus Wisdom-based Cleric spellcasting with a small slot pool.
- **NO skill proficiencies.** Goon's Cleric Overhaul removed the extra skills a Cleric multiclass
  was wrongly granting. Do not plan a dip around picking up Religion or Medicine.

**Cleric 2** adds Channel Divinity (1 charge, **short rest**) and Turn Undead — worth it when the
domain's Channel Divinity is the point (Twilight Sanctuary, Spell Shield, Path to the Grave,
Destructive Wrath, Balm of Peace, Prophecy of Doom, Feat of Strength).

**Cleric 3** is feat-neutral under Listo's cadence (feats at class level 3), and adds the level-3
domain spell pair plus level-2 slots. Rarely the right stopping point unless a specific domain
spell is the goal.

**The classic dips, restated for 10.2:**

| Dip | Buys |
|---|---|
| **Tempest 1** | Heavy armour, shields, martial weapons, maximised lightning/thunder via Channel Divinity at 2 |
| **Life 1** | Heavy armour + Disciple of Life on every heal you cast from any source |
| **War 1** | Heavy armour, martial weapons, **War Priest bonus-action attack (3/long rest)** |
| **Zeal 1** | Heavy armour, martial weapons, **bonus-action attack Wis times/long rest** — strictly a wider offer than War 1 for a dip, since War's Extra Attack needs 6 levels |
| **Order 1** | Heavy armour, and **every buff/heal on your partner grants them a free weapon attack** |
| **Peace 1** | No armour upgrade, but a **permanent d4 on both characters' attacks, checks and saves** |
| **Forge 1** | Heavy armour **+1 AC in it at level 6**, so only pays off as a deeper investment |

> **Watch the casting stat.** `Multiclass Preferred Casting Ability Fix` (`10209`) is installed
> specifically so a Cleric dip does not reassign your character's Spellcasting Stat to Wisdom for
> scrolls, Illithid powers and items. Take advantage of it, but confirm on the character sheet.

---

## Not present

- **`Blessing of the Trickster` (`11566`) — not in the 10.2 list.** Docs page 4 still recommends
  it. Trickery's BotT in 10.2 is Goon's version: **no concentration**, Stealth only, **not usable
  in dialogue**.
- **`Darkness Domain`** — added in an earlier version for Shadowheart, then **REMOVED** (changelog
  items 102 and 103), along with the Shadowheart Darkness Domain patch. Goon's Cleric Overhaul
  still carries load-order instructions referencing it; ignore them.
- **`Ambition Domain` and `Solidarity Domain`** (the other two *Plane Shift: Amonkhet* domains) —
  explicitly **REMOVED** (changelog item 46). Only Strength and Zeal survive.
- **`Vow of Poverty` Cleric subclass** — added, then removed.
- **Standalone Grave Domain (Hav's)** — removed; Grave now comes from `5e Cleric Subclasses
  Combined`.
- **`Mystra's Spells`** — not installed. Domain spells listed as Mystra's-only (Order's *Ego Whip*,
  Peace's *Aura of Purity*) will not appear as written.
- **`Arcanist` feat** — removed from the list; the docs' Shillelagh advice for Clerics is stale.
  Use Essential Feats' Magic Initiate / Eldritch Adept, or the Druidic Warrior fighting style.
- **`Tal'dorei` domains** — the 5e Cleric Subclasses Combined author lists them as planned, not
  shipped. The pack contains exactly six: Arcana, Forge, Grave, Order, Peace, Twilight.
- **`UA6 Invoke Duplicity`** — recommended by both Goon and the BotT author; **not in the list**.
  Trickery's Invoke Duplicity is the vanilla implementation until Expansion's L17 upgrade.
- **`Alternate Origin Subclasses` (`8960`)** *is* installed (archives `AOS - Shadowheart -
  Knowledge 1.0.0` and `AOS - Wyll - Hexblade 1.0.0`) but only changes Shadowheart's **default**
  subclass to Knowledge Domain. It adds no domain and no mechanics; you can still respec normally.
- **`Class Action Enhanced - Voice of the Circle` (`5075`)** is **not a Cleric mod** — Voice of the
  Circle is a class action granted by the **Envoy's Amulet**. Listo pulled variant "A"
  `(unverified which of the mod's 7 cooldown/AoE combinations that is)`.
