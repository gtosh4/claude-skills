# Listonomicon 10.2 — Bard

Bard in Listo is the vanilla BG3 chassis — Charisma full caster, d8 hit die, Dex + Cha saves,
Bardic Inspiration on a short-rest clock from level 5 — with four things layered on top: a
bug-fix/QoL overhaul (`Goon's Bard Overhaul`, `17658`), a full 13–20 progression from
`Expansion` (`279`) that adds the d12 Inspiration die, two extra Magical Secrets picks and a
level 20 capstone, an `Automatic Magical Secrets Extender` (`20247`) that silently makes Magical
Secrets pull from *every* class list in the modlist including modded ones, and four extra
Colleges beyond the vanilla four. Listo also changed the Bardic Inspiration spell itself: the AoE
was removed but it now **heals** the single target, scaling with the Inspiration die. The one
thing that breaks outside build advice is `Arcane Acuity Rework` (`14595`) — the Swords Bard
Acuity engine that most published guides are built on does not exist here. **Listo's own docs
have no Bard section at all** (`4-SpellsFeatsClassesItems.md` covers Barbarian, Cleric, Druid,
Fighter, Monk, Paladin, Rogue, Sorcerer — Bard is simply absent), so everything below comes from
the manifest, the changelog, and mod pages.

## At a glance

| | |
|---|---|
| **Primary ability** | Charisma (spell DC and spell attack rolls) |
| **Saves granted at level 1** | **Dexterity + Charisma** — only if Bard is your *first* class |
| **Hit die** | d8 (8 + Con at level 1, 5 + Con on level-up) |
| **Armour / weapons** | Light armour; simple weapons, hand crossbows, rapiers, longswords, shortswords |
| **Skills at level 1** | **Choose 3** from an 18-skill list (essentially every skill except a couple) |
| **Multiclass node (Bard as a later class)** | Light armour, **1** skill, musical-instrument proficiency, an instrument. **No saving throws.** |
| **Bardic Inspiration cadence** | 3 uses at level 1, **long rest only**. At level 5 **Font of Inspiration** moves it to **short *or* long rest** and raises it to 4 uses. |
| **Inspiration die** | d6 → **d8 at 5** → **d10 at 10** → **d12 at 15** (the d12 is from `Expansion`, not vanilla) |
| **Level breakpoints** | **3** College + Expertise ×2 + (Lore/Swords/Valour only) bonus proficiencies · **5** Font of Inspiration + d8 · **6** Countercharm + 2nd College feature · **10** d10 + Expertise ×2 + Magical Secrets ×2 · **14** Magical Secrets ×2 + 14th College feature · **15** d12 · **18** Magical Secrets ×2 · **20** Superior Inspiration |
| **Feat cadence** | Listo grants feats **every 3 levels** (docs page 1), not every 4 — so a 3-level Bard dip is feat-neutral. Cross-ref `data/listo-10.2-feats.md`. |
| **Dip value** | **Bard 3** is one of the strongest three-level dips in the list: a College, **Expertise ×2**, and (Lore) three free skill proficiencies. See "Dip value" below. |

Countercharm (level 6): you and allies within 9 m have Advantage on saves against **Charmed and
Frightened**. Song of Rest (level 2): grants the party the effect of a Short Rest, recharging on
long rest.

## Class changes from vanilla

### Goon's Bard Overhaul (`17658`)
- **File pulled:** `Goon's Bard Overhaul-17658-1-0-1-1-1777631543.zip` (**v1.0.1.1**).
  **The Nexus page now describes v1.1.0.0**, which "polished interrupt implementations with new
  Goon's Library tech" and added Goon's Library 4.23+ / Compatibility Framework / Automatic
  Magical Secrets Extender as declared dependencies. Everything below is on the page for both
  versions; the interrupt polish specifically is v1.1.0.0 and **is not in Listo's build**.
- Must load **after** `Expansion` (the mod page states this explicitly).

**Blade Flourishes (Swords Bard):**
- All three Flourishes gain **Interrupt (reaction) counterparts**.
- The Slashing Flourish interrupt **supports throwing**.
- Interrupts usable while **Invisible**.
- Slashing Flourish (Melee) is now a **Target** spell, not a Zone spell — you pick **two targets
  within melee range in a 360° arc**. Tooltip damage now includes the Bardic Inspiration die.
- Slashing Flourish (Ranged) can no longer hit the same entity twice.
- Mobile Flourish (Melee and Ranged) — you can steer the push direction with cursor position.
- Natively compatible with `Expansion`'s Master's Flourish toggle (tooltip does not live-update).

**Bardic Inspiration / Combat Inspiration:**
- Can no longer be cast on a target that already has a **higher-level** Bardic Inspiration
  condition (stops overwriting a d10 with a d6).
- `Expansion`'s d12 conditions are consumed/removed correctly by interrupts.
- Bardic Attack interacts correctly with the d10 Inspiration die.
- Usable under more non-hostile polymorphs, and while Invisible.

**Cutting Words (Lore Bard) — read this before planning a Lore Bard:**
- Now shows the die value in its description; correctly uses the **d12 at level 15+** instead of
  capping at d10.
- **Cannot be used while Silenced** (checks all Silence conditions, not just `SILENCED`).
- **The Cutting Words condition is now a Charm**, in the `SG_Charmed` status group, and
  **cannot be used on Deafened creatures or creatures immune to Charm.** This is a real
  restriction in a list where undead, constructs and many bosses carry charm immunity — Cutting
  Words is no longer a universal answer.

**Countercharm:** only applies to characters who are **not Deafened**. The instrument is tagged
`AI_UNPREFERRED_TARGET` so enemy AI stops wasting turns attacking it.

**Magical Secrets:** Goon adds "a lot of vanilla spells" to the list, and the page defers to
`Automatic Magical Secrets Extender` for the rest.

### Expansion (`279`) — levels 13–20
- **File pulled:** `Expansion-279-1-7-3-6-1780876532.zip` (**v1.7.3.6**; Nexus is on **1.7.3.10**).
- Adds for the base class: **Bardic Inspiration d12 at 15th**, **Magical Secrets at 14th and
  18th** (2 spells each — the mod page notes these two tranches *specifically require* `5e
  Spells`, which **is** in Listo as mod `125`), and **Superior Inspiration at 20th** (when you
  roll initiative with no Inspiration uses left, you regain one).
- Note on implementation: you gain a **second "Bardic Inspiration" spell entry at 13th level**
  that replaces the old one — this is intentional, not a bug.
- **Magical Inspiration** is offered as an **optional 2nd-level feature** (a creature holding your
  Inspiration die can spend it to add the roll to the damage or healing of a spell it casts). It
  is an MCM/script-extender toggle in Expansion's Bard config. **Whether Listo enables it by
  default is unverified** — check the MCM in-game.
- Per-subclass 14th-level features are listed under each College below.

### Automatic Magical Secrets Extender (`20247`)
- **File pulled:** `AutomaticMagicalSecretsExtender-20247-1-1-2-1768899452.zip` (**v1.1.2**;
  Nexus is on **1.1.3**).
- "Automatically pulls in magical secrets from other class lists. It requires no configuration."
  Covers vanilla spells missing from the base choice list **as well as any added by mods**.
- Practical effect in Listo: Magical Secrets at 10/14/18 draws from `5e Spells` (`125`), the
  Artificer/Mesmerist/Paragon/Inquisitor lists, `Conjure Animals and Summon Beast Spells`
  (`13458` — whose own description calls out "Bard's Magical Secrets"), and everything else the
  list adds. This is the single largest power delta between a Listo Bard and a vanilla one.

### Bard Flourishes Consolidated (`6226`)
- **File pulled:** `Bard Flourishes Consolidated-6226-1-0-1-1706413938.zip` — the **optional
  standalone file**, not the full `Common Actions Consolidated` (which the changelog says is
  **disabled by default**, while "Battle Master Maneuvers, Arcane Archer shots, and **Bard
  Flourishes** are **default enabled**").
- Collapses the **6 Swords Bard Flourishes** into a single hotbar icon. Cosmetic/hotbar only, no
  mechanical change. Known issue: **hotkeys do not work** for abilities inside a roll-up.

### Listo's own spell edits (from `5-ChangeLog.md`)
- **Bardic Inspiration: the AoE effect was removed, but Bardic Inspiration now *heals* the single
  target.** The healing value scales as the Inspiration die improves. This makes Bardic
  Inspiration a bonus-action heal-plus-buff on a short-rest clock — a meaningful change to how
  the class plays, and it stacks with the fact that Bard is one of only three Charisma casters in
  the list with real healing (see `references/listo-rules.md`).
- **Motivational Speech**: better temporary HP, fewer maximum targets.
- Bards were **removed** from the *Mark of Putrefaction* spell list.
- The `5e Spells` mod (`125`) is present, so the Bard spell list itself is wider than vanilla.
- *(Enemy-side only, not player-facing:* Listo's Combat Extender gives **enemy** Swords Bards Trip
  Attack in Act 3, and differentiates enemy Swords / Valour / Lore Bards.*)*

### Supporting mods that change Bard planning
- **Multiclass Preferred Casting Ability Fix** (`10209`) — fixes the vanilla bug where generic
  effects (scrolls, items, illithid powers) use the casting ability of the *last brand-new class*
  you took. With this in, **class order no longer hijacks your scroll/item casting stat**, so a
  Bard can be taken at any point in a multiclass without losing Charisma scaling on scrolls.
- **JWL Discordant Instruments** (`9119`) — converts the Musical Instrument slot into a **Trinket**
  slot with 100+ items. The mod page states it "keeps musical instruments interesting by giving
  **Perform** a unique effect for bards", so instruments remain equippable but now compete with
  real gear. Full trinket list and version caveat: `data/listo-10.2-equipment.md` § "New equipment
  slot".
- **Progression Preview** (`20193`) — shows full class progressions in-game; useful for checking
  what a modded College actually grants at each level before committing.
- Compatibility is patched by **Compatibility Framework Subclass Patches** (`6996`) and
  **Chisfreak's patch** (changelog: explicitly names **College of Tragedy** among the subclasses
  made to work together and with multiclassing).

## Subclasses

Eight Colleges are selectable: the four vanilla ones plus Eloquence, Dance, Tragedy, and
Stormcalling. All four vanilla Colleges also receive a 14th-level feature from `Expansion`.

### College of Lore (vanilla)
- **Mod:** base game; 14th-level feature from `Expansion` (`279`); Cutting Words fixed by Goon's
  Bard Overhaul (`17658`).
- **Mechanics:** **L3** — Cutting Words (reaction, expend Inspiration, subtract the die from an
  enemy attack roll / ability check / damage roll) **plus proficiency in 3 additional skills**.
  **L6** — Magical Secrets: learn 2 non-Bard spells (up to level 3), *four levels earlier than the
  base class gets it*. **L14** (`Expansion`) — **Peerless Skill**: expend Inspiration to add the
  die to your own ability check; implemented as a self-buff you can apply pre-emptively **or
  during dialogue**.
- **Listo caveats:** Cutting Words is now blocked by **Silence**, by **Deafened** targets, and by
  **Charm immunity** (Goon). Peerless Skill's dialogue usability is a direct answer to the
  two-character skill-coverage problem.
- **Duo relevance:** the highest skill-coverage subclass in the game here — 3 free proficiencies
  at L3 on top of Bard's own 3 and Expertise ×4, and a dialogue-usable Inspiration boost at 14.

### College of Swords (vanilla)
- **Mod:** base game; Flourishes reworked by Goon's Bard Overhaul (`17658`) and consolidated by
  `6226`; 14th-level feature from `Expansion` (`279`).
- **Mechanics:** **L3** — Blade Flourish (Defensive / Slashing / Mobile, each in Melee and Ranged
  = the 6 flourishes), a **Fighting Style** (Duelling or Two-Weapon Fighting), and proficiency in
  **medium armour and scimitars**. **L6** — **Extra Attack**. **L14** (`Expansion`) — **Master's
  Flourish**: a Passives-tab toggle letting you roll a **d6 instead of expending an Inspiration
  die** for a Flourish.
- **Listo additions:** `UA Fighting Styles` (`19693`) adds **Close Quarters Shooter, Mariner, and
  Thrown Weapon Fighting to the Swords Bard style list** — so the L3 style choice is wider than
  Duelling/Two-Weapon Fighting (see `data/listo-10.2-feats.md` § "Fighting styles"). Goon's
  rework adds Interrupt versions of all three Flourishes
  (usable while Invisible; the Slashing interrupt supports **throwing** builds).
- **Duo relevance:** the martial Bard. Extra Attack at 6 plus Lone Wolf's extra Action, and the
  Flourish interrupts convert a spare Reaction into damage. **Do not plan it around Arcane
  Acuity** — see below.

### College of Valour (vanilla)
- **Mod:** base game; 14th-level feature from `Expansion` (`279`).
- **Mechanics:** **L3** — Combat Inspiration (Inspiration die can be spent for weapon damage or
  AC) and proficiency in **medium armour, shields, and martial weapons**. **L6** — **Extra
  Attack**. **L14** (`Expansion`) — **Battle Magic**: when you use your Action to cast a Bard
  spell, make **one weapon attack as a bonus action**.
- **Duo relevance:** the only College that hands out **shields plus martial weapons**, so it is
  the cheapest way to make a Charisma caster durable without a Fighter/Paladin dip. Battle Magic
  at 14 is a real action-economy gain on top of Lone Wolf's extra Action.

### College of Glamour (vanilla)
- **Mod:** base game; 14th-level feature from `Expansion` (`279`).
- **Mechanics:** **L3** — Mantle of Inspiration. **L6** — Mantle of Majesty: **Command**.
  **L14** (`Expansion`) — **Unbreakable Majesty**: bonus action, 1 minute; the first time a
  creature tries to attack you each turn it must make a **Charisma save vs your spell save DC** or
  lose the attack; on a success it instead has **disadvantage on saves against your spells next
  turn**. Short or long rest. Implemented through the interrupt/reaction system.
- **Duo relevance:** Unbreakable Majesty is the best single-target aggro-shed in the class, which
  matters in a two-character party where losing one member usually ends the fight — but it does
  not arrive until 14.

### College of Eloquence
- **Mod:** Bard Subclass - College of Eloquence (`4651`)
- **File pulled:** `College of Eloquence-4651-1-03-1702343609.rar` (**v1.03** — current on Nexus).
- **Mechanics:**
  - **L3 Silver Tongue** — treat a d20 of **9 or lower as a 10** on Charisma (Persuasion) and
    Charisma (Deception) checks. **The mod page's own Known Issues list says "Silver Tongue
    feature is not working properly; may be due to Reliable Talent inheritance."** Treat this as
    possibly broken until tested in-game.
  - **L3 Unsettling Words** — bonus action, expend Inspiration, target within 60 ft subtracts the
    rolled die from its **next saving throw** before the start of your next turn. **The die is
    rolled before the status applies, so you see the number first** — you can decide whether it's
    worth committing your control spell.
  - **L6 Unfailing Inspiration** — when a creature adds your Inspiration die to an **attack roll
    or saving throw and fails**, it **regains the die**. For **ability checks** the author could
    not detect success/failure, so it is a flat **50% chance** (d20 of 11+) to regain the die
    regardless of outcome.
  - **L6 Universal Speech** — action, 1 hour, grants **Speak with Animals and Speak with Dead**
    simultaneously. Once per long rest, or spend a spell slot to reuse.
  - **L14 Infectious Inspiration** — you gain **5 Eloquence Charges** (flat, not Charisma-scaled),
    restored on long rest. When an ally within 60 ft **succeeds** on an attack roll or save using
    your Inspiration die, you gain "Host of Inspiration" until the end of your next turn; once per
    turn you may spend a Charge to hand a **free Bardic Inspiration** to a different creature.
    This costs **no bonus action and no Inspiration use**. Because BG3 cannot target during a
    reaction, the hand-off is **delayed to your next turn** rather than being instant — you keep
    your Reaction for Counterspell / opportunity attacks. v1.02 also lets it trigger off ability
    checks when the creature loses the Bardic Persistence d20 roll.
- **Duo relevance:** the strongest *sustained* Inspiration economy in the list. In a two-person
  party the Inspiration die is almost always going into your partner's roll, and Unfailing
  Inspiration means failed rolls cost you nothing. Unsettling Words is a cheap, reliable
  save-debuff that turns a coin-flip Hold Person into a likely one.

### College of Dance
- **Mod:** College of Dance - Bard Subclass PHB2024 (`12558`)
- **File pulled:** `College of Dance - Bard Subclass PHB2024 DnD 5R-12558-3-1-2-1778169191.rar`
  (**v3.1.2** — current on Nexus) **plus** `College of Dance - Level 20 Patch-12558-1-1-1727551405.zip`.
  The Level 20 patch is installed, which **shifts Leading Evasion from level 12 to level 14** and
  enables the level 15 die upgrade.
- **Mechanics:**
  - **L3 Dance Virtuoso** — **Advantage on Performance checks**; gain **Perform Dance** (a
    Performance-style action with six song options plus a silent dance).
  - **L3 Dance of Death: Dextrous Attacks** — your **Unarmed Attacks use Dexterity** for attack
    and damage rolls if Dex > Str.
  - **L3 Dance of Death: Unarmed Damage** — a **toggleable passive** (on by default) that replaces
    your Unarmed Attack with **Bardic Unarmed Attack**, whose damage **scales with your Bardic
    Inspiration die**.
  - **L3 Defensive Footwork / Agile Strikes** — after using Bardic Inspiration in combat, you gain
    **one free Bardic Unarmed Kick Attack** (appears in the **Temporary** section of the hotbar).
  - **L5 / L10 / L15** — unarmed damage die rises to **1d8 / 1d10 / 1d12** (the 1d12 requires the
    Level 20 patch, which Listo has).
  - **L6 Inspiring Movement** — a **Reaction** that buffs an ally; per the mod's changelog it now
    grants **+50% movement speed** (previously a flat +4.5 m), **only targets allies**, and costs
    an "Inspiring Movement Charge" that **refreshes at the end of each of your turns** (so at most
    one per round).
  - **L6 Tandem Footwork** and **L10 Improved Tandem Footwork (increased Initiative bonus)** —
    `(unverified — described only in images on the mod page; the level-10 tier is explicitly an
    initiative bonus increase)`.
  - **L14 Leading Evasion** (L12 without the Level 20 patch; Listo has the patch so **14**) —
    `(unverified — described only in images on the mod page)`.
- **Gear note:** `Corellon's Grace Rework with Corellon's Fist` (`14238`) is in the list and its
  description explicitly states compatibility with College of Dance — a quarterstaff that lets you
  substitute an **unarmed attack** for your weapon attack. Details in
  `data/listo-10.2-equipment.md`.
- **Known quirks from the mod page:** the combat log will show "Negate Strength Modifier" next to
  "Strength Modifier" (cosmetic). If unarmed attacks stop scaling with Dex, equip/unequip a
  weapon. If Bardic Unarmed Attack doesn't appear, toggle the passive off and on.
- **Duo relevance:** the only Bard that is a **Dexterity** martial without needing weapon
  proficiency or Extra Attack — unarmed damage rides the Inspiration die, so the class resource
  and the damage engine scale together. Agile Strikes gives a free attack every time you inspire
  your partner, which is exactly the action-economy shape a two-person party wants. Note it gets
  **no Extra Attack**.

### College of Tragedy
- **Mod:** College of Tragedy Bard Subclass (`15166`)
- **File pulled:** `College of Tragedy Bard Subclass-15166-1-2-1754142787.zip` (**v1.2** — current
  on Nexus). Explicitly named in Chisfreak's compatibility patch (changelog) as made to work with
  other mods and multiclassing.
- **Source:** Tal'Dorei Campaign Setting Reborn.
- **Mechanics:** *(the mod page renders each feature's name as an image; only **Nimbus of Pathos**
  was recoverable from the page text. The bracketed names below are the Tal'Dorei source names
  matched to the level and effect — `(names unverified, effects verified)`.)*
  - **L3 (Poetry in Misery)** — whenever **you or an ally within 9 m rolls a natural 1** on the
    d20 for an **attack roll or saving throw**, you may use your **Reaction** to **regain one
    expended Bardic Inspiration**. The author cut the ability-check trigger (couldn't be
    implemented). The page notes you can potentially regain a charge **every single turn** as long
    as you have your Reaction.
  - **L3 (Sorrowful Fate)** — when you or a visible ally forces a creature to make a saving throw,
    expend an Inspiration to **change that save to a Charisma save**; on a failure the target
    takes **Psychic damage equal to a Bardic Inspiration die**. **Short or long rest.**
    **Implementation caveat from the author: this is NOT an interrupt** — you must **pre-cast it
    on the target before the save is forced**. There is a one-turn grace period.
  - **L6 (Tale of Hubris)** — when a creature scores a **critical hit** on you or an ally within
    18 m, **Reaction + expend Inspiration**: for 1 minute or until it is crit, the **critical hit
    threshold against that creature is reduced by 2** (**by 3 at 14th level**).
  - **L6 (Impending Misfortune)** — take a **+10 bonus** to an attack roll or saving throw; your
    **next** attack roll or save takes **-10**. The penalty clears on a short or long rest if
    unused. Recharges on **short or long rest, or when you are reduced to 0 HP**.
  - **L14 Nimbus of Pathos** — *(requires a past-12 level mod; Listo has `Expansion`)* — Action,
    touch a willing creature. For 1 minute it gains **+4 AC**, **Advantage on attack rolls and
    saving throws**, **+1d10 Radiant** on weapon and spell attack hits, and **-2 to the crit
    threshold against it**. **When the effect ends the creature immediately drops to 0 HP and is
    dying.** Once per long rest. Author's warning: the drop is implemented as **damage**, so
    **do not have Warding Bond active** on the target — the caster of Warding Bond will very
    likely die too.
- **Duo relevance:** a Reaction-hungry subclass in a run where **Lone Wolf grants an extra
  Reaction** — Poetry in Misery and Tale of Hubris can both be live in the same round. Poetry in
  Misery is genuine short-rest-economy relief. Nimbus of Pathos is a one-fight-ending nuke button
  with a lethal downside that is far riskier in a two-person party than in a party of four:
  the "dying" character is 50% of your action economy.

### College of Stormcalling
- **Mod:** (DTO) Otherworldly Archetypes (`21822`) — a 12-subclass pack; the Bard entry is
  **The College of Stormcallers / College of Stormcalling** (the mod page and the author's docs
  use both spellings).
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67 2026-06-17T17-15Z PYJWETtYB.zip`
  (**v1.2.0.67**; the Nexus page currently displays **1.2.0.66**, so Listo's archive is at or
  ahead of the public listing). Changelog: "ADDED (for testing) Otherworldly Archetypes" — it
  entered the list on a **playtesting** footing, so treat it as less battle-tested than the others.
- **Mechanics** (from the author's documentation site, `prizzels.github.io/DTO/`):
  - **L3 Chorus of Thunder** — **Passive Toggle, costs 1 Bardic Inspiration**: your next Thunder
    damage spell forces a **Constitution save** or inflicts **Concussion** for 1 turn.
    **Concussion = knocked prone, cannot take reactions, and limited to one attack, action or
    bonus action.**
  - **L3 Thundercall** — **cantrip**, Action, Constitution save, 18 m: **1d8 Thunder**, half on a
    successful save. **Range increases with your Charisma modifier.**
  - **L3 Additional Spells Known** — **Thunderwave** (1st) and **Shatter** (2nd).
  - **L6 Conductor** — 3rd-level spell, Action, ranged spell attack, 18 m, **Concentration, 10
    turns**: **3d6 Lightning** and **Shocked** for 2 turns. While concentrating you may cast
    **Staccato Lightning** as a **bonus action**. Upcast: +1d6.
  - **L6 Staccato Lightning** — bonus action, ranged spell attack, 18 m: **2d6 Lightning**; if the
    target has an **electrical or concussive status**, add your **Charisma modifier** to the damage.
  - **L14 Electrifying Aria** — 7th-level spell, Action, Dexterity save, 12 m radius: **3d6
    Lightning** and **Electrified** to everything caught in it. **The aria repeats at the start of
    each of the next 10 turns** until you end it. Upcast: +1d6.
    **Electrified:** 1d4 Lightning per turn; **allies** get their **crit threshold reduced by 1**;
    **foes** get their **Constitution save reduced by 1 per remaining turn of duration**.
  - **L14 Finale!** — Action, Constitution save, 18 m radius (**increased by your Charisma
    modifier**): **stuns all nearby Electrified foes** on a failed save and ends the aria.
- **Note:** the DTO docs also describe a Bard **"Warsongs"** feature line (levels 7/10/12/16) —
  that belongs to **Codex of Might and Magic (Volume 2)**, which is **not in Listo**. Do not plan
  around Warsongs.
- **Duo relevance:** the only Bard College in the list that is a genuine **blaster**, and
  Electrifying Aria is an unusual fit for a two-person party: it is a 10-turn persistent AoE that
  simultaneously **buffs your partner's crit rate** and **degrades enemy Constitution saves each
  turn**, then converts into a mass Stun. That's one Action buying an entire fight's worth of
  control — the exact trade a two-character party wants. Concussion at level 3 also denies enemy
  Reactions, which is worth more when there are fewer of you to be reacted at.

## Arcane Acuity — why published Swords Bard guides do not apply

`Arcane Acuity Rework` (`14595`) is installed
(`Arcane Acuity Rework-14595-1-0-0-16-1745258631.rar`). Per `references/listo-rules.md` and
`data/listo-10.2-equipment.md` § "Arcane Acuity", Acuity in Listo is:

- **capped at 3 stacks**
- **gains only 1 stack per trigger**
- **combat-only** — it **cannot be pre-stacked** before a fight
- **triggers on weapon attack rolls**

**What this means for Bard specifically.** The canonical Swords Bard build outside Listo is the
"Acuity lock": Helmet/Hat of Fire Acuity plus **Band of the Mystic Scoundrel**, stack Acuity to
7–10 with a Flourish or Hand Crossbow volley, then cast a save-or-lose spell (Hold Person, Hold
Monster, Command) as a **bonus action** at an inflated spell save DC, usually on turn one and
often pre-buffed out of combat. In Listo:

- The DC bonus tops out at **+3**, not +7 to +10. Your spell save DC is essentially Charisma +
  proficiency, and you must build it the normal way.
- You cannot walk into a fight already stacked, so **turn one is a setup turn** — the Bard has to
  land weapon attacks *first*, which is the opposite of the "open with Hold Monster" pattern.
- Because it triggers on **weapon attack rolls**, Acuity still favours Swords/Valour over a pure
  caster Bard — but as a small, slow bonus, not a build-defining engine.
- **Treat every published Swords Bard guide that mentions Acuity stacking as void here.** If a
  build's damage or control plan depends on a Charisma-caster reaching a DC in the mid-20s by
  turn one, it does not work in this modlist.

The practical replacement for that control ceiling is **Magical Secrets breadth** (the Extender
plus `5e Spells` gives you access to control spells no vanilla Bard can take) and **Eloquence's
Unsettling Words** (a flat, *known-in-advance* subtraction from a single save), not stacked DC.

## Dip value

**Bard 3** (from `references/listo-rules.md`, expanded):
- A **College** — all eight above are available at 3, including Lore's three bonus skill
  proficiencies and Swords' medium armour + scimitars + a Fighting Style.
- **Expertise ×2** at level 3, and **another ×2** at level 10 if you go deep.
- **Jack of All Trades** at level 2 — half proficiency on every non-proficient ability check.
- **Song of Rest** at level 2 — a party-wide short rest effect on a long-rest recharge. In a run
  where long rests cost 120+ camp supplies and short-rest resources are the ones worth having,
  this is a resource in its own right.
- Feat-neutral: Listo's feats land every 3 levels, so a 3-level Bard dip costs no feats.
- Bardic Inspiration at a dip is **long-rest only** — **Font of Inspiration is level 5**, not 3.
  A 3-level dip gets 3 uses per long rest, which is thin. If you want Inspiration as a recurring
  resource, **5 is the real breakpoint**, not 3.

**Bard 1** buys **Dex + Cha saves** (first class only), light armour, **3 skills**, and
Charisma-based full-caster progression. **Bard 2** adds Jack of All Trades and Song of Rest.

**The two-character skill-coverage argument.** Two players must clear every skill check in the
campaign. Bard is the best answer in the list to that problem: 3 skill proficiencies at level 1
(from an 18-skill list), **Jack of All Trades** covering everything you did *not* pick,
**Expertise ×2 at 3 and ×2 more at 10**, **three more proficiencies if you take Lore**, and
Eloquence's Silver Tongue or Lore's dialogue-usable **Peerless Skill** on top. A Bard plus almost
anything covers the campaign; two non-Bards will have holes.

**The Charisma trap still applies.** Bard grants **Charisma** saves at level 1, so pairing Lone
Wolf's +4 with Charisma wastes one of the two grants. See `references/listo-rules.md`
§ "The Charisma trap".

## Not present

- **College of Whispers** — **confirmed removed.** Changelog: added in an earlier version
  ("ADDED College of Whispers Bard"), then **"REMOVED Bard College of Whispers"** in **v9.0.3**.
  Not in the mod TSV, not in the manifest. This is the single most common stale recommendation.
- **College of Creation** — **confirmed removed.** Changelog: "ADDED College of Creation", later
  **"REMOVED College of Creation bards"**. Not in the TSV or manifest. The Eloquence mod page
  still lists Creation in its compatibility config, which is misleading — the mod is gone.
- **College of Spirits** — not in the TSV or manifest. It appears in the Eloquence mod's
  compatibility list and in the Tragedy author's "other mods" list, but **was never installed**.
- **College of Satire / Whispers-style stealth Colleges, Skald, Minstrel, Troubadour** — none
  present; manifest sweep found no matching paks.
- **"Warsongs"** (the DTO Bard feature line at levels 7/10/12/16) — belongs to **Codex of Might
  and Magic Volume 2**, which is **not in the list** (no `Codex`, `Might and Magic`, or
  `Testament` entry in the TSV). Only the Otherworldly Archetypes volume is installed.
- **Common Actions Consolidated** (the non-Bard half of `6226`) — installed but **disabled by
  default**. Only the Bard Flourishes half is on.
- **A Bard section in Listo's own documentation** — `4-SpellsFeatsClassesItems.md` has per-class
  sections for eight classes and **none for Bard**. Do not read that absence as "Bard is
  unchanged"; it is not.
- **`references/listo-rules.md` lists surviving Bard subclasses as "Eloquence, Dance, Tragedy"** —
  that list **omits College of Stormcalling** from `(DTO) Otherworldly Archetypes` (`21822`),
  which is installed. Consider that rules-file line incomplete.

## Unverified / needs in-game confirmation

- Whether **Expansion's optional Magical Inspiration (level 2)** is toggled on in Listo's MCM.
- **Eloquence's Silver Tongue** — the mod page's own Known Issues say it "is not working properly".
- **College of Dance's Tandem Footwork (L6), Improved Tandem Footwork (L10) and Leading Evasion
  (L14)** — the mod page documents these only as images; exact numbers unread.
- Which **Arcane Acuity Rework** file variant (cap-3 vs cap-5) the archive contains — the archive
  name does not disclose it; `references/listo-rules.md` states cap 3.
- Whether the old **"Jack of All Trades Affects Initiative"** tweak (present in an early changelog
  entry) is still active — no matching mod appears in the current manifest, so it would have to be
  inside `Listo Tweaks and Patches`.
