# Listonomicon 10.2 — Fighter

Fighter is the least-changed *chassis* in Listo and the most-expanded *subclass list*. The base
class is vanilla BG3 — Second Wind, Fighting Style, Action Surge, Extra Attack, Indomitable —
with levels 13–20 supplied by **Expansion** (`279`): a second Action Surge charge at 17, a
second and third Indomitable at 13 and 17, and a **fourth attack at 20**. Argelia's
`Fighter - OneDnD - PHB2024 Changes` is **not** in the list, so there is no PHB2024 rework of
Second Wind or Tactical Mind. What Listo does instead is bolt on **fourteen** subclasses and
rebuild Eldritch Knight almost from the ground up. Combined with the eight-feat cadence and
Action Surge stacking on Lone Wolf's bonus Action, Fighter is the strongest *primary* martial in
the list and the single most-recommended *dip*.

MO2 groups these under a `Fighter_separator`; every mod below was confirmed installed by tracing
its `.pak` destination in the 10.2 manifest, not just its presence in the download list.

---

## At a glance

| | |
|---|---|
| **Primary ability** | Strength or Dexterity. **Intelligence** additionally for Eldritch Knight, Arcane Archer and Psi Warrior; **Constitution** for Rune Knight save DCs |
| **Saves at level 1** | **Strength + Constitution** — only if Fighter is your **level 1** class |
| **Armour / weapons (level 1 class)** | Light, Medium, **Heavy**, Shields; Simple + Martial weapons |
| **Armour / weapons (multiclass node)** | Light, Medium, Shields, Simple + Martial — **no Heavy armour, no saves.** A Fighter dip taken *after* level 1 does not grant heavy armour |
| **Hit dice** | d10 (10 + CON at level 1, 6 + CON thereafter) |
| **Skills** | Choose 2 from Acrobatics, Animal Handling, Athletics, History, Insight, Intimidation, Perception, Survival |
| **Second Wind** | Level 1. `1d10 + Fighter level` HP, **recharges on short rest** |
| **Action Surge** | Level 2. One extra Action. **Recharges on short rest.** **Two charges from level 17** (Expansion), still only once per turn |
| **Indomitable** | Level 9, reroll a failed save. **Long rest.** 2 uses at 13, 3 at 17 (Expansion) |
| **Extra Attack** | 2 attacks at 5, 3 at 11, **4 at 20** (Expansion "Extra Attack 20th Level part") |
| **Key breakpoints** | **1** saves + armour + Fighting Style + Second Wind · **2** Action Surge · **3** subclass + feat · **5** Extra Attack · **11** Improved Extra Attack **and** the bonus feat · **17** second Action Surge · **20** fourth attack |
| **Dip value** | Highest in the list. See [Dip value](#dip-value) |

---

## Feat cadence

**Fighter is one of only two classes on the eight-feat cadence.**

> Feats land at Fighter level **3, 6, 9, 11, 12, 13, 15, 18** — eight feats over 20 levels.
> Every other class gets seven (3, 6, 9, 12, 13, 15, 18). The exceptions are **Fighter and
> Rogue**, which get the extra one at **11**.

Source: `Universal Feat Every X Level` (installed, confirmed in the manifest), which replaced the
older `Feat Every X Levels`. Listo's changelog states it explicitly: *"It also restores the
advantage of Fighters and Rogues: They gain a unique, extra feat at level 11 each (ignore what
the book says)."* The docs' FAQ repeats it and adds Mesmerist — **but the installed
`FeatsUni.json` sets `enableAdvancedSettings: false`, so the Mesmerist entry never applies.
Fighter and Rogue only.** The universal 13 is also live and the docs miss it; see
`data/listo-10.2-mcm.md`.

Consequences for planning:

- **Fighter 11 is the highest-value single level in the list for a feat-hungry build.** It pays
  Improved Extra Attack (3 attacks) *and* an off-cadence feat in the same level-up.
- Expansion's own extra feats at **14, 16 and 19** do **not** apply — **confirmed**, not guessed:
  `MCM/Expansion/settings.json` sets `feats.BaseClassFeats: "None"`. A pure Fighter 20 gets
  **eight** feats, not eleven.
- The standard feat arithmetic in `references/listo-rules.md` **undercounts Fighter by one** at
  Fighter level 11 or higher, on top of the universal level 13 grant.
- Because the bonus feat sits at 11 and not on a multiple of 3, a **Fighter 11 base + 9-level
  second class** is feat-optimal.

Cross-reference `data/listo-10.2-feats.md` for what to spend them on. The Fighter-relevant ones
documented there and *not* restated here: **Martial Adept** (2 superiority dice, short-rest
refresh), **Weapon Master**, **Fighting Initiate**, **Dirty Fighting** (the docs specifically
recommend it for sword-and-board Fighters with a spare bonus action), **Polearm Master**,
**Durable + Mageslayer** (the docs' named Fighter tank package), and the **UA Fighting Styles** /
**Protection and Great Weapon Fighting PHB2024** style pools.

---

## Class changes from vanilla

Very little touches the base chassis. What does:

- **Expansion (`279`, archive `Expansion-279-1-7-3-6`)** supplies all of 13–20:
  - **Action Surge, 17th-level part** — two uses between short rests, once per turn. Implemented
    by making base Action Surge per-turn with a hidden short-rest resource.
  - **Indomitable, 13th and 17th-level parts** — 2 uses at 13, 3 at 17, long rest.
  - **Extra Attack, 20th-level part** — the fourth attack.
  - **Martial Versatility (optional, 4/8/12/16/19)** — swap a fighting style. **Listo turns it
    off**: `MCM/Expansion/settings.json` has `optional_features.Fighter: false`. Resolved from
    the install — see `data/listo-10.2-mcm.md`.
- **Feat cadence** replaced as described above.
- **UA Fighting Styles (`19693`)** and **Protection and Great Weapon Fighting PHB2024 (`18684`)**
  widen and rebalance the level 1 Fighting Style pick. Both are already documented in
  `data/listo-10.2-feats.md` — don't restate; do remember that Fighter picks from that expanded
  pool at level 1, and Champion and Brute each pick a **second** style later.
- **Hotbar consolidation.** `Battle Master Manoeuvres Consolidated` (`16879`) and
  `Arcane Shots Consolidated` (`17011`) fold all manoeuvres / arcane shots into container buttons
  (melee and ranged containers for manoeuvres; one for shots). Both are **enabled by default** in
  Listo's Consolidated separator. The manoeuvre containers unlock from **any** superiority die
  source, including the Martial Adept feat — so a non-Battle Master who takes Martial Adept still
  gets the tidy container.
- **Enemy Fighters got the same toys.** NPC Overhaul and Combat Extender give Action Surge,
  Second Wind, Heavy Armour Master, Trip Attack and Menacing Attack to enemy Fighters, and Listo
  patched the AI so it can't chain the same manoeuvre twice in one turn. Relevant only as threat
  assessment, not build planning.
- **Removed:** a "Fighters get a taunt at level 3" mod, and the **Guardian** fighter subclass —
  both added and then removed in earlier versions. Neither is in 10.2.

---

## Subclasses

Fourteen. Four vanilla (two of them heavily modded), seven from one pack, three standalone.

### Battle Master
- **Mod:** vanilla BG3 + `Expansion` (`279`); UI from `Battle Master Manoeuvres Consolidated` (`16879`)
- **File pulled:** `Battle Master Manoeuvres Consolidated-16879-1-0-3` (latest)
- **Mechanics:** 4 superiority **d8** and 3 manoeuvres at 3; +1 die and +2 manoeuvres at 7; **d10**
  and +2 manoeuvres at 10. Dice **recharge on short rest**. Save DC = 8 + proficiency + STR or DEX,
  whichever is higher. Expansion adds **Relentless** at 15 (regain 1 die on initiative if you have
  none) and **Improved Combat Superiority** at 18 (**d12**).
- **Duo relevance:** the only Fighter subclass whose entire kit runs on the **short-rest** clock,
  which is the clock that matters when a long rest costs 120+ supplies. Commander's Strike also
  hands your partner an off-turn attack — genuine action-economy value in a two-body party.

### Champion
- **Mod:** `Champion fighter PHB 2024` (`14957`) + `Expansion` (`279`)
- **File pulled:** `Champion_PHB2024-14957-2-0-0-1` — the **plain** main file, not the
  `Champion_PHB2024_5e` variant. That means you do **not** get vanilla Remarkable Athlete at 7.
  2.0.0.1 is the current version.
- **Mechanics:**
  - **3 — Improved Critical:** crit on 19–20.
  - **3 — Remarkable Athlete (2024):** implemented as **advantage on Athletics** and a flat **+3 to
    initiative rolls** (the mod's stand-in for advantage on initiative), plus RAW free movement of
    half your Speed immediately after a crit, without provoking.
  - **7 — Additional Fighting Style.**
  - **10 — Heroic Warrior:** two interrupts, one on attack rolls and one on saving throws, letting
    you **reroll and keep the new result** — attack-roll behaviour like Elven Accuracy but without
    the advantage requirement, save behaviour like Indomitable. **Once per turn**, no other cost.
  - **15 — Superior Critical** (Expansion): crit on **18–20**.
  - **18 — Survivor** (Expansion): regain **5 + CON** HP at the start of each turn while at or
    below half HP. The Champion mod's own **Defy Death** adds advantage on death saves.
- **Duo relevance:** an 18–20 crit range plus a free reroll every turn is the best crit-fishing
  platform in the list, and it stacks with **Deadly Alacrity**'s crit-threshold reduction from
  `data/listo-10.2-feats.md`. Heroic Warrior's save-reroll is also a second Indomitable that
  costs nothing and recharges every turn — meaningful when losing one of two characters ends the
  fight.

### Eldritch Knight
- **Mods:** `Eldritch Knight Plus` (`11807`) + three of its add-ons, `OneDnD - Eldritch Knight -
  War Magic and Improved War Magic PHB 2024` (`12070`) + its level-5 patch,
  `Eldritch Knight Spellcasting Modifier UI BUGFIX` (`11966`), `Expansion` (`279`)
- **Files pulled:**
  - `Eldritch Knight Plus - Level 20 Version-11807-5-2` → `Eldritch Knight Plus - Lvl20 ver.pak`
  - `EKP Add-on 1 - Extra Cantrip at Lvl4-11807-3-0`
  - `EKP Add-on 2 - Potent Cantrips at lvl12-11807-3-0`
  - `EKP Add-on 7 - No Empowered Cantrips-11807-5-2`
  - `DnD 5R War Magic and Improved War Magic-12070-5-0-0` (latest)
  - `War Magic at Lvl 5 Patch-12070-1-0`
  - `EK Spellcasting Mod UI BUGFIX-11966-1-0`
  - **Version drift:** EK Plus is on **5.2**; the Nexus page now documents **5.3**, which adds
    cantrip replacement on level-up, moves the level-20 bonus spell slot to 19, and gives **two**
    new spells at 13. **None of those apply here.** The add-on **numbering** on the current page
    also no longer matches the 3.0-era files Listo pulled — Add-on 2 today means "Eldritch Strike
    to 8 + Potent Cantrips at 10", but the archive Listo has is literally named
    *Potent Cantrips at lvl12*, and Listo's changelog confirms the intent: *"the optional files for
    a bonus cantrip at 4th level, potent cantrips at 12th level, and removing the 'Empowered
    Cantrips' passive."*
- **Mechanics** (vanilla features still apply; this is what the mods add or move):
  - **All spell-school restrictions removed at every level.** You pick from the **full Wizard
    list**, not just Abjuration and Evocation — for new spells *and* replacements.
  - **4** — +1 cantrip known (Add-on 1).
  - **5** — +1 spell known. **Battlemage Casting**: your ranged spell attacks can be cast as
    **melee** spell attacks when threatened; toggleable, auto-added to the hotbar.
  - **5** — **War Magic arrives at 5 instead of 7** (level-5 patch), in its **PHB2024** form:
    *exchange one of your attacks to cast a cantrip*, in either order. Once per turn — **but
    Action Surge resets the counter and lets you do it again.**
  - **6** — +1 level 1 slot, +1 cantrip known.
  - **8** — **nothing.** Empowered Cantrips is **removed** by Add-on 7 (Listo's deliberate balance
    call now that Booming Blade is base-game).
  - **9** — +1 spell known, +1 level 2 slot.
  - **10** — Eldritch Strike (vanilla).
  - **11** — **level 3 spells unlock two levels early**: +1 level 3 slot and **+2** spells known.
  - **12** — +1 level 3 slot, +1 spell known. **Improved War Magic** (PHB2024): *exchange two of
    your attacks to cast a levelled spell*. Also once per turn, also reset by Action Surge.
    **Potent Cantrips** (Add-on 2) — exact BG3 implementation `(unverified)`.
  - **13–20** (Expansion): full spell progression, with **any** Wizard spell selectable at 14 and
    20; **Arcane Charge** at 15 (teleport 9m before or after your Action Surge action);
    **Improved War Magic** at 18 in its *vanilla* form (cast a spell with your Action, then a
    weapon attack as a bonus action). This is a **separate passive** from the 12070 version, which
    ships its new War Magic as new passives rather than overwriting the old ones — so an EK 18+
    may hold both. Whether they usefully stack is `(unverified)`.
  - **Attack accounting under the new War Magic:** your Action is worth **3 attacks** (4 with the
    level-20 fourth attack). A weapon attack costs 1, **any** cantrip costs 1 (including Booming
    Blade), a levelled spell costs 2. Bonus actions are not counted, so Misty Step mid-sequence is
    free. Spend your base Action's attacks *first*, then Action Surge (which resets to 3 and
    re-enables the War Magic cantrip and spell), then any Haste action last.
  - The `11966` bugfix corrects the Spellbook/level-up UI showing the wrong spellcasting modifier.
    Cosmetic only.
- **The docs' two claims, checked:**
  - *"Eldritch Knights in general are improved with better flow between mixing spells, cantrips,
    and extra attack"* — **verified.** PHB2024 War Magic at 5, Improved War Magic at 12, Battlemage
    Casting, and the removed school restrictions all do exactly this.
  - *"Eldritch Knight weapon bonds are permanent… you no longer need to redo your bond every
    morning"* — **cannot be verified in 10.2.** The mod that provided it, `Permanent Weapon Bond`,
    was added back in Listonomicon **v1.0** and **no longer appears anywhere in the 10.2
    manifest** — no archive, no `.pak`, no mod folder, and the string "Bond" does not occur in the
    manifest at all. None of the EK mods Listo *does* pull mentions bond persistence. It may have
    been absorbed into Ajax's DeGreaser (whose contents can't be inspected from the manifest), or
    it may have been dropped silently. **Treat the docs' claim as stale and confirm in-game before
    building around it.** `(unverified)`
  - **Essential Feats' War Magic feat does NOT stack** with the Eldritch Knight feature. The docs
    call this out directly; see `data/listo-10.2-feats.md`. Do not take that feat on an EK.
- **Duo relevance:** the only Fighter that converts Action Surge into *two* spells per turn.
  Action Surge resets the War Magic counter, so an Action Surge turn is Attack+Attack+Cantrip
  **then** Spell+Attack — and Lone Wolf's extra Action is a third pass on top of that. Also the
  natural home for the **Arcanist Feat** (the docs single out Shield of Faith on an EK as
  "basically a free +2 AC" for someone with no other access to it).

### Arcane Archer
- **Mod:** vanilla BG3 (Patch 8) + `Expansion` (`279`); UI from `Arcane Shots Consolidated` (`17011`)
- **File pulled:** `Arcane Shots Consolidated-17011-1-0-0` (latest)
- **Mechanics:** at 3, Arcana + Nature proficiency, one cantrip from Guidance / Light / True
  Strike, **4 Arcane Arrows** and **3 Arcane Shots**; +3 arrows and +1 shot at both 7 and 10;
  Curving Shot and Magic Arrow at 7. **Arcane Arrows recharge on short rest.** Expansion adds
  **Ever-Ready Shot** at 15 (regain a use on initiative if you have none) and **Arcane Shot
  Improved** at 18 (**+2d6** of each shot's own damage type, plus an extra shot option).
- **Duo relevance:** short-rest resource, and the changelog notes Lae'zel's default stats were
  retuned to support Eldritch Knight / Psi Warrior / **Arcane Archer** if you are running her as
  the second body. Rider effects (Banishing, Grasping, Enfeebling) are how a two-person party
  removes a threat it cannot out-damage.

### Banneret (Purple Dragon Knight, 2014)
- **Mod:** `5e Fighter Subclasses Combined` (`15060`)
- **File pulled:** `FighterSubclasses5eCombined.zip-15060-1-1-9-2` (latest)
- **Mechanics:** **3 — Rallying Cry:** using Second Wind also heals up to **three allies within
  18m for your Fighter level** (a hotbar action appears after Second Wind). **7 — Royal Envoy:**
  Persuasion proficiency + **doubled proficiency on Persuasion checks**, and a second skill if you
  already had it. **10 — Inspiring Surge:** using Action Surge lets one ally within 18m spend
  their **reaction** to make a weapon attack — **two allies at 18**. Note the ally attacks with
  whatever weapon is active and **must already be in range**. **15 — Bulwark:** when you use
  Indomitable on an INT/WIS/CHA save, an ally who fails the same kind of save before your next
  turn can reroll too.
- **Duo relevance:** **the sharpest action-economy subclass in a two-player run.** Inspiring Surge
  turns your Action Surge into your partner's extra attack, so a single Action Surge produces
  action for both characters — and with Lone Wolf you already have a spare Action to spend before
  you even reach for it. Rallying Cry and Bulwark both scale to *party size*, which normally
  punishes a duo, but the healing is per-ally at full Fighter level and Bulwark only ever needed
  one target anyway. Requires your level-20 unlock mod to name its features `Indomitable_2` /
  `Indomitable_3` — **Expansion does**, and Bulwark is written against exactly that.

### Brute (UA)
- **Mod:** `5e Fighter Subclasses Combined` (`15060`)
- **Mechanics:** **3 — Brute Force:** every damaging hit with a weapon you're proficient with adds
  **1d4**, rising to **1d6 at 10**, **1d8 at 16**, **1d10 at 20**. Works with the dual-wielding
  toggle on, with Tavern Brawler improvised weapons, and with most pseudo-weapons like Beast
  Barbarian claws. **7 — Brutish Durability:** add **1d6 to every saving throw**; on death saves,
  reaching 20+ triggers a hidden roll that heals you 1 HP to mimic a critical success.
  **10 — Additional Fighting Style. 15 — Devastating Critical:** crits add damage equal to your
  **Fighter level**. **18 — Survivor:** 5 + CON HP at the start of each turn while below half HP
  and above 0.
- **Duo relevance:** flat, unconditional, resource-free. **+1d6 on every save** is the strongest
  passive defence available to a Fighter and directly attacks the run's failure mode — one
  character losing a save and the fight ending. Pairs with the Resilient feat's save
  proficiencies rather than competing with them.

### Cavalier
- **Mod:** `5e Fighter Subclasses Combined` (`15060`)
- **Mechanics:** **3 — Bonus Proficiency** (Animal Handling, History, Insight, Performance or
  Persuasion). **3 — Born to the Saddle:** no mounts in BG3, so reimplemented as **25% less
  falling damage** and **+9m speed on the first turn of combat**. **3 — Unwavering Mark:** hitting
  with a melee weapon marks the target until the end of your next turn; while within 1.5m of you
  a marked creature has **disadvantage on any attack that isn't against you**, and if it damages
  anyone else you get a **bonus-action attack with advantage dealing +half your Fighter level**.
  Uses = STR modifier, long rest. Toggleable. **7 — Warding Maneuver:** reaction, **+1d8 AC**
  against one attack on you or an ally within 1.5m, and **resistance** to that attack's damage if
  it still hits. Uses = CON modifier, long rest. **10 — Hold the Line:** enemies provoke an
  opportunity attack when they move 1.5m+ **within your reach** (not just leaving it), and a hit
  sets their speed to **0**. **15 — Ferocious Charger:** a granted charge ability; your next
  attack after it forces a STR save (DC 8 + prof + STR) or **prone**. **18 — Vigilant Defender:**
  a **special extra reaction on every other creature's turn**, usable only for opportunity attacks
  and not on a turn you spend your normal reaction.
- **Duo relevance:** the dedicated protector. Warding Maneuver is the cleanest "my partner does
  not die" button in the class, and Unwavering Mark forcibly redirects attention onto the durable
  half of a two-person party. Vigilant Defender at 18 multiplies reactions in a party that has
  very few bodies to generate them — and it scales with **Polearm Master** reach (see the feats
  file).

### Psi Warrior
- **Mod:** `5e Fighter Subclasses Combined` (`15060`)
- **Mechanics:** **3 — Psionic Energy dice**, count = **twice your proficiency bonus**, size **d6
  → d8 at 5 → d10 at 11 → d12 at 17**. All restored on long rest; **regain one as a bonus action,
  once per short rest**. They fuel: **Protective Field** (reaction, reduce damage to you or an ally
  within 9m by the die + INT), **Psionic Strike** (once per turn, +die + INT force damage on a hit
  — toggle it on), and **Telekinetic Movement** (free once per short rest, then costs a die;
  limited to 9m centred on *you* because of BG3's throw system). **7 — Telekinetic Adept:**
  **Psi-Powered Leap** (bonus action, flying speed = twice walking, free once per short rest then
  costs a die) and **Telekinetic Thrust** (after Psionic Strike damage, STR save vs 8 + prof + INT
  or prone/pushed 3m — cast as a follow-up hotbar action, and you click a spot to push *away
  from*). **10 — Guarded Mind:** psychic resistance, and spend a die to end charm/fright at the
  start of your turn. **15 — Bulwark of Force:** bonus action, **half cover** to up to INT-modifier
  creatures for 1 minute; free once per long rest, then costs a die. **18 — Telekinetic Master:**
  cast **Telekinesis** with INT, and make a **weapon attack as a bonus action** on every turn you
  concentrate on it.
- **Duo relevance:** Protective Field is damage mitigation you can spend on the *other* character,
  from range, on their turn — one of very few ways a Fighter protects a partner who is out of
  position. Die count scales on proficiency bonus, so it grows to **12 dice** at level 17+, and the
  bonus-action refresh means it partially runs on the short-rest clock. Note Listo moved the
  standalone `Telekinetic Thrust` cantrip on enemies to Act 2 and restricted it to Eldritch
  Knights, so the player-side Psi Warrior version is unaffected.

### Rune Knight
- **Mod:** `5e Fighter Subclasses Combined` (`15060`)
- **Mechanics:** **3 — Bonus Proficiency**, reimplemented as **Sleight of Hand**. **3 — Rune
  Carver:** know **2 runes**, rising to **3 at 7**, **4 at 10**, **5 at 15**; you may swap one on
  each level-up. Inscribe by casting the rune on yourself once, which unlocks its passive and its
  invocation. **Rune save DC uses CONSTITUTION**, not Intelligence — the level-up UI displays an
  INT-based DC and that display is wrong. Runes: **Cloud** (Sleight of Hand/Deception advantage;
  reaction to redirect an attack to a random other creature within 9m), **Fire** (doubled tool
  proficiency; +2d6 fire and STR save or restrained with 2d6/turn), **Frost** (Animal
  Handling/Intimidation advantage; **+2 to all STR and CON checks and saves for 10 minutes**),
  **Stone** (Insight advantage, **36m darkvision**; reaction to charm-stupor a creature ending its
  turn within 9m), **Hill** (7+) (poison resistance and save advantage; **resistance to
  bludgeoning, piercing and slashing for 1 minute**), **Storm** (7+) (Arcana advantage, can't be
  surprised; a 1-minute prophetic state granting reactions that impose advantage or disadvantage
  on attack rolls and saves within 18m, plus two castable spells for ability checks).
  Each invocation is **once per short rest**. **3 — Giant's Might:** bonus action, become **Large**,
  advantage on STR checks and saves, and **+1d6** once per turn on a weapon or unarmed hit
  (toggleable so you can time it). Uses = proficiency bonus, long rest. **7 — Runic Shield:**
  reaction, force an attacker who hit an ally within 18m to **reroll**; uses = proficiency bonus,
  long rest. **10 — Great Stature:** Giant's Might damage to **1d8**; +10% height, same size
  category. **15 — Master of Runes:** **every rune invocable twice**, and they refresh on a
  **short** rest. **18 — Runic Juggernaut:** Giant's Might to **1d10**, size can go **Huge**, and
  **+1.5m reach**; stacks with Enlarge if you cast Giant's Might first.
- **Duo relevance:** the widest toolbox in the class, and almost all of it is on the **short-rest**
  clock — decisively so from 15, when every rune fires twice per short rest. Cloud Rune and Runic
  Shield are both "the other character does not take that hit". Storm Rune's advantage/disadvantage
  reactions are party-wide force multipliers in a party where there are only two turns to buff.
  Note the historical `Rune Knight QoL tweak` mod (inscriptions surviving rests) is **not** in
  10.2; the combined mod's own v1.1.6.1 fixed *"some rune inscriptions not lasting beyond long
  rest"*, so inscription persistence is `(partly unverified — confirm in-game)`.

### Samurai
- **Mod:** `5e Fighter Subclasses Combined` (`15060`)
- **Mechanics:** **3 — Bonus Proficiency** (History, Insight, Performance or Persuasion; must
  choose a skill). **3 — Fighting Spirit:** bonus action, **advantage on all weapon attack rolls
  this turn** plus **5 temp HP** (**10 at 10**, **15 at 15**). **Three uses, long rest.**
  **7 — Elegant Courtier:** add your **WIS modifier to Persuasion checks**, and **choose a
  saving throw proficiency** at level-up (WIS, or INT/CHA if you already have WIS).
  **10 — Tireless Spirit:** regain one Fighting Spirit use on initiative if you have none.
  **15 — Rapid Strike:** when you have advantage on an attack, an interrupt lets you **give up the
  advantage for an extra weapon attack** against the same target, once per turn. **18 — Strength
  Before Death:** taking lethal damage spends your **reaction** to grant a **full extra turn at 1
  HP with all action resources restored**, during which you cannot be dropped to 0; damage taken
  gives a death-save failure (two on a crit), three failures kills you instantly. Long rest.
- **Duo relevance:** **Elegant Courtier at 7 is a third saving-throw proficiency** — and
  `references/listo-rules.md` treats save proficiencies as otherwise obtainable *only* from your
  level 1 class, Lone Wolf, and the Resilient feat. That alone justifies the subclass. Strength
  Before Death is a free "the fight does not end here" at 18, which is the exact failure mode of a
  two-person party.

### Sharpshooter (UA)
- **Mod:** `5e Fighter Subclasses Combined` (`15060`)
- **Mechanics:** **3 — Steady Aim:** bonus action, aim at a target; until end of turn your ranged
  attacks with that weapon ignore **high-ground rules** (BG3's stand-in for cover) and deal
  **+2 + half your Fighter level** on each hit against it. **Three uses, short or long rest.**
  **7 — Careful Eyes:** Search as a **bonus action** (Perception vs Stealth to reveal hiding, not
  invisible, enemies) + Perception, Investigation or Survival proficiency. **10 — Close-Quarters
  Shooting:** no disadvantage on ranged attacks within 1.5m, and a creature you hit at that range
  **can't take reactions** for the rest of the turn. **15 — Rapid Strike:** forgo advantage on an
  attack to make an extra weapon attack **as a bonus action** — a different, snappier
  implementation than the Samurai's. **18 — Snap Shot:** one **extra ranged attack** as part of
  the Attack action on your first turn of combat.
- **Mind the naming:** this is a **subclass** with no relationship to the **Sharpshooter feat**,
  which Listo rebalances separately (proficiency bonus to damage instead of to attack — see
  `data/listo-10.2-feats.md`). They combine, but don't confuse them.
- **Duo relevance:** Steady Aim refreshes on **short rest**, and Snap Shot plus Action Surge on
  turn one is a very large opening burst — the mod author literally writes *"Action surge and
  enjoy the carnage."* Thrown weapons do **not** count as ranged weapons for Steady Aim or Rapid
  Strike.

### Echo Knight
- **Mod:** `Echo Knight Fighter Subclass` (`3939`), with the **RAW Progression** optional file
  and `Object Character Support`
- **Files pulled:** `Echo Knight-3939-1-5-7` → both `DEchoKnight.pak` **and**
  `DEchoKnightRAW.pak`, plus `Object Character Support`. Nexus is on **1.5.8** (opportunity-attack
  avoidance fix, transformation compatibility) — minor drift.
- **Mechanics:** **3 — Manifest Echo:** bonus action, summon an echo within ~4.5m. **AC 14 +
  proficiency bonus, 1 HP**, immune to all conditions, uses your save bonuses, occupies its space,
  **flies** (so it ignores surfaces and never provokes). Lasts until destroyed, dismissed, replaced,
  or you're incapacitated; destroyed if it ends your turn more than 9m away. You command its
  movement freely; the echo shares your movement pool and your initiative. **Bonus action to swap
  places** at a cost of 4.5m of movement, at any range — with a "Reserve Movement" toggle that
  holds back exactly enough movement so you never lose the swap. Attacks from the Attack action may
  originate from the echo's space, via either **Control Echo** (instantly swap, you're invulnerable
  and surface-immune while swapped) or **Attack Near Echo** (stay put, melee attacks reach targets
  near the echo — passive toggle or free action). Opportunity attacks trigger around the echo but
  are made from your position. **3 — Unleash Incarnation:** one extra melee attack from the echo's
  position **per Attack action taken that turn** — so regular **plus Haste plus Action Surge** —
  and the extras may be taken together at the end of the turn. Uses = **CON modifier** (min 1),
  long rest, unlocked by a free action so you don't burn charges by accident.
  **With the RAW file Listo installs: 7 — nothing** (Echo Avatar is deliberately not implemented),
  **10 — Shadow Martyr** (reaction, teleport the echo next to a targeted ally and take the attack
  for them; once per **short or long** rest; technically resolves as a critical miss on the
  original target), **15 — Reclaim Potential** (when an echo is destroyed by damage, gain
  **2d6 + CON** temp HP if you have none; uses = CON modifier, long rest).
  **18 — Legion of One is NOT implemented** — the author calls it out of scope. Fighter 18–20 as an
  Echo Knight gets nothing from the subclass.
- **Feat interactions the author flags:** **Sentinel** (its opportunity-attack lockdown works from
  the echo, "highly recommended") and the **2014 War Caster** (cast instead of the echo's
  opportunity attack) — Listo ships `War Caster (2014 and UA2)`, and the feats file confirms the
  2014 branch is what enables the Echo Knight interaction.
- **Duo relevance:** the closest thing to a third body. The echo threatens a second zone,
  generates opportunity attacks 9m away from you, and Unleash Incarnation converts **Action Surge
  into an additional free melee attack** rather than just an extra Action. Shadow Martyr is a
  short-rest "eat the attack aimed at my partner". The catch: Legion of One never arrives, so a
  Fighter 20 Echo Knight is spending its last three levels on Expansion's generic features only.

### Purple Dragon Knight (2024 UA)
- **Mod:** `2024 Purple Dragon Knight (UA) - Fighter Subclass` (`15607`)
- **File pulled:** `PurpleDragonKnight2024-15607-2-0` (latest)
- **Mechanics:** **3 — Knightly Envoy:** implemented as **Speak with Animals 1/day**.
  **3 — Purple Dragon Companion:** summon an amethyst dragon hatchling **1/day**; it persists until
  it dies, **shares your initiative**, acts independently (no bonus action needed to command it),
  and grows in size and stat block as you level. **Resummon the same day by expending your daily
  use of Second Wind, or by taking a short rest.** A hover toggle avoids ground surfaces but blocks
  attacking. **7 — Dragon Rider:** dragon becomes Medium and can fly-carry you; **Gravity Breath**
  becomes a 9m cone with +2d6 force on a failed save and gains **4/day** uses; **Shared Second
  Wind** — your Second Wind also heals the dragon **1d6 + your Fighter level** and restores one
  Gravity Breath. **10 — Rallying Surge:** using **Action Surge** lets up to **three allies within
  9m** spend a **reaction** to either **Advance** (one weapon attack, at a random enemy in range —
  or a Rend if it's the dragon) or **Retreat** (move half speed toward you without provoking).
  **11 —** the dragon gains a **Change Shape** mote form for traversal. **15 — Amethyst Pinnacle:**
  dragon becomes Large, speed and fly speed 12m, can hover while attacking and while carrying you,
  Gravity Breath 5/day, and **Tandem Attack** — forgo one of your attacks for a dragon Rend, or two
  for a Gravity Breath. **18 — Enduring Commander:** you and the dragon gain **resistance to force
  and psychic**.
- **Practical warning from the author:** the dragon uses custom Osiris scripting and animations.
  **You very likely need a new playthrough** for the dragon not to break, the model periodically
  resets (a visible blink to a mote and back — expected), and pathfinding indoors is awkward at
  full size.
- **Duo relevance:** the strongest raw action-economy subclass on paper for a two-person party.
  The dragon is a **third combatant sharing your initiative**, and **Rallying Surge** turns Action
  Surge into up to three reaction-attacks — in a duo that means your partner *and* the dragon both
  act off your surge. Shared Second Wind stacks a heal onto a short-rest resource. Weigh that
  against the stability caveats and the fact that camp-supply cost scales with camp population.

### Chronoknight
- **Mod:** `(DTO) Otherworldy Archetypes` (`21822`), Daelen's Testament of the Otherworldly
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67` →
  `DaelensTestament_c714f127-6475-4e82-1816-3922fc220bee.pak`. Added to Listo **"for testing"** per
  the changelog — treat as the least battle-tested option in this file.
- **Mechanics** (from the official DTO reference site; the Nexus page only lists names):
  - **3 — Timeless Knowledge:** gain **Sorcery Points equal to 1 + your Intelligence modifier** per
    long rest.
  - **3 — Borrowed Time:** costs a sorcery point, range 18m. **Grant an Action to any entity you
    choose, including yourself.** On their next turn they become **Desynchronized** for 2 turns:
    only a single attack, action **or** bonus action, half movement, disadvantage on Concentration
    checks, with an Intelligence save at end of turn to resync early. **You cannot benefit from
    Action Surge and Borrowed Time in the same turn.**
  - **7 — Alacrity:** **+1 Reaction point per turn**, and **+Intelligence modifier to Initiative**.
  - **10 — Rewind:** reaction, once per **short rest** — when you or a nearby ally is about to fail
    a saving throw, they succeed instead.
  - **15 — Continuity:** advantage on INT saves; **Stunned and Lethargic become Desynchronized**
    instead.
  - **18 — Chronobreak:** bonus action, once per long rest — **Borrowed Time on yourself and all
    allies within 9m.**
- **Duo relevance:** this subclass is *about* the run's central problem. Borrowed Time hands your
  partner an entire extra Action at the cost of a debuffed following turn — and in a two-person
  party there is exactly one obvious recipient. Alacrity's extra Reaction stacks on top of Lone
  Wolf's. Rewind is a short-rest save-save. The hard constraint: **Borrowed Time and Action Surge
  are mutually exclusive on the same turn**, so a Chronoknight is choosing between the class's
  signature feature and the subclass's — plan to alternate turns rather than stack them.

---

## Dip value

**Fighter is the most commonly recommended dip in Listonomicon, and the reason is arithmetic, not
flavour.**

**Fighter 1 — must be your level 1 class:**
- **Strength + Constitution saving throw proficiencies.** These are obtainable *only* from the
  level 1 class (plus Lone Wolf's +4 and the repeatable Resilient feat). A respec that reorders
  your classes silently loses them. CON saves in particular protect Concentration on anything you
  multiclass into.
- **All armour including Heavy, plus Shields** — but only at level 1. Taken as a later multiclass,
  Fighter grants Light, Medium and Shields **only**; the heavy armour proficiency does not come
  through the multiclass node.
- **Simple and Martial weapon proficiency.**
- **A Fighting Style** — from the widened pool of `UA Fighting Styles` and
  `Protection and Great Weapon Fighting PHB2024`. Archery, Defence, Duelling, Interception,
  Thrown Weapon Fighting and Druidic Warrior (free Shillelagh, which Listo makes permanent) are all
  live options at character level 1.
- **Second Wind** — `1d10 + Fighter level` self-heal on a **short rest**, and it never scales
  badly because the cost is one bonus action.

**Fighter 2 — Action Surge:**
- **A third Action.** With **Lone Wolf granting a second Action, Bonus Action and Reaction**,
  Fighter 2 makes a three-Action turn the baseline for any character in this run, and Haste makes
  it four. There is no other two-level investment in the list that does this.
- It **recharges on a short rest**, which is the resource clock that actually matters when a long
  rest costs 120+ camp supplies scaling with camp population.
- Every "cast a big spell then also swing" and "burst the boss before it acts" plan in a duo runs
  through this level.
- For an **Eldritch Knight** specifically, Action Surge also **resets the PHB2024 War Magic
  counter**, so the surge Action can carry a second cantrip or a second levelled spell.
- **Exception:** a **Chronoknight** cannot use Action Surge and Borrowed Time in the same turn.

**Fighter 3 — feat-neutral, and the cheapest way to buy a subclass:**
- A 3-level dip costs no feats at all: the dip class grants its own level 3 feat. So Fighter 3
  is Fighter 1 + Fighter 2 + a full subclass tier 1 **for free**, feat-wise. Battle Master's
  4 short-rest superiority dice and 3 manoeuvres, or Echo Knight's Manifest Echo + Unleash
  Incarnation, are both reachable this way.

**Deeper stopping points if Fighter is the main class:** **5** (Extra Attack), **11** (three
attacks **and** the off-cadence bonus feat — the highest-value single level-up in the list),
**17** (second Action Surge charge), **20** (fourth attack).

---

## Not present

Confirmed **absent** from the 10.2 manifest — do not recommend, and correct the user if they ask:

- **`Fighter - OneDnD - PHB2024 Changes` (Argelia).** Not in the list. There is no PHB2024 rework
  of the base Fighter — Second Wind is one short-rest use at all levels, and there is no Tactical
  Mind / Tactical Shift / Tactical Master. Only the *Champion* and *Eldritch Knight War Magic*
  PHB2024 mods are installed.
- **`Permanent Weapon Bond`.** Added in Listonomicon v1.0, gone by 10.2 — the string "Bond" does
  not appear anywhere in the manifest. The docs page still claims permanent Eldritch Knight weapon
  bonds; that claim is unsupported by anything installed. `(unverified — see Eldritch Knight)`
- **`War Magic Enhanced`** and **EK Plus Add-ons 3–6** (cantrips as a bonus action, Eldritch Strike
  moved to 8, Potent Cantrips at 10, War Magic moved without the OneDnD rework). Listo pulled the
  OneDnD War Magic line instead, and the two are explicitly incompatible.
- **The `12070` "Level 20 Progression Patch"**, which would move Improved War Magic to 18. Not
  pulled, so the PHB2024 Improved War Magic lands at **Eldritch Knight 12**.
- **`Champion_PHB2024_5e`** (the variant that keeps vanilla Remarkable Athlete at level 7).
- **Guardian**, a Fighter subclass, added in an earlier version and since removed.
- **"Fighters get a taunt at level 3"**, removed by Ajax as "breaking everything".
- **Legion of One** (Echo Knight 18) — never implemented by the mod at all.
- **Echo Avatar** (Echo Knight 7) — deliberately not implemented; with Listo's RAW progression file
  that level is empty.
- **`Rune Knight QoL tweak`** (inscriptions surviving rests) as a standalone mod.
- **`Alternate Origin Subclasses - Shadowheart and Wyll` (`8960`) contains no Fighter content.**
  Listo pulled `AOS - Shadowheart - Knowledge` and `AOS - Wyll - Hexblade`; the changelog shows the
  Wyll Hexblade change was later struck through. Lae'zel's *starting stats* were retuned to support
  Eldritch Knight / Psi Warrior / Arcane Archer, but her subclass was not changed.
- **`(DTO) Otherworldy Archetypes` (`21822`) contributes exactly one Fighter subclass** —
  Chronoknight. The other eleven belong to other classes.

---

## Load-order and stacking notes

- **`OneDnD - Eldritch Knight - War Magic` patches the Polearm Master bonus-attack entry**
  (its changelog lists a *"tweak for Polearm Clout for compatibility"* at v2.2). **Cahoot's Feats
  Overhaul must load AFTER it**, or Feats Overhaul's Polearm Master rework — reach on versatile
  polearms, damage riders on the bonus attack, spellcasting-modifier override — loses the conflict.
  Listo ships both `Cahoots Feats Overhaul` and `Cahoots Feats Overhaul Listo Patch`. The MO2
  profile is now readable: the **Listo Patch sits near the top of `modlist.txt` (highest
  priority)**, while base `Cahoots Feats Overhaul` sits *below* the Eldritch Knight War Magic
  mods. Whether that satisfies the requirement, or whether the in-game pak order in
  `modsettings.lsx` is what actually decides it, is still `(unverified)` — but the ordering is
  no longer unreadable. See `data/listo-10.2-mcm.md` for how to check.
- **Essential Feats' War Magic feat does not stack with Eldritch Knight's War Magic.** Stated
  directly in the Listo docs.
- **Expansion's Improved War Magic (18) and the OneDnD Improved War Magic (12) are separate
  passives.** The 12070 mod deliberately does not overwrite the base-game passives (the "replace
  base-game War Magic" file is an *optional* it does not ship by default here). Whether an Eldritch
  Knight 18+ can use both in one turn is `(unverified)`.
- **`Battle Master Manoeuvres Consolidated` must load after `Basic Weapon Actions Consolidated`**
  per its author. Listo keeps the Consolidated mods in their own separator with Battle Master
  manoeuvres, Arcane Archer shots and Bard flourishes **enabled by default** and the basic-weapon
  and common-action ones disabled — which satisfies this trivially.
- **Listo's `OneDnD_WarMagic` MCM profile — resolved.** It holds exactly two keys:
  `improvedExtraAttackFix: true` and `debugToggle: false`. Nothing else is tuned, so the mod
  page's defaults stand.
- **Champion, Expansion, load order:** the Champion mod must load *after* Expansion for Superior
  Critical (15) and Survivor (18) to resolve. Assume Listo does this; not independently verified.
