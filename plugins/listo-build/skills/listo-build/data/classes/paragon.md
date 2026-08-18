# Listonomicon 10.2 — Paragon

The Paragon (`23169`, *The Paragon* by CatDude55) is a **brand-new full 1–20 class**, not a
base-game class and not a reskin — it is an implementation of Kingstarman's homebrew. It is a
**Charisma-based martial-support** class: a d10 heavy-armour front-liner whose entire resource
economy is **Willpower Dice**, a small pool that **recharges on a short rest** and is spent to
augment weapon attacks (Blade Skills), buff allies, and shore up its own defence. It has a
Charisma "spellcasting stat" for save DCs but **no spell slots and no spell list** — the one
subclass that casts anything casts cantrips. Its signature trick is turning **Help** and
**Distract** into bonus actions attached to weapon attacks, which makes it the only class in the
list built specifically around pulling a *second* character forward. In a two-person Lone Wolf
run that is close to a design brief.

**Provenance.** Compiled 17 August 2026. Mod present in `listo-10.2-mods.tsv` as
`23169  The Paragon`. Archive pulled by 10.2: **`Paragon-23169-1-01-1780878080.zip`**, FileID
`123121`, **version 1.01**, 21,140,731 bytes. The Nexus page's current version is **also 1.01**
(uploaded 08 June 2026, original upload 05 June 2026) — **no version drift; the page describes
exactly what Listo ships.** This is a very new mod (Listo changelog: "Official release of
Paragon!", earlier "ADDED (playtesting) Paragon"), so expect the author to change it: he states
a plan for **16 subclasses total, 10 by end of 2026**, plus a companion item mod *Valor and
Virtue* which is **not in the 10.2 list**.

**Everything below comes from the mod page.** This class has no D&D or BG3 baseline — nothing
here is inferred from 5e. Anything not stated on the page is marked `(unverified)`.

---

## At a glance

| | |
|---|---|
| **Primary ability** | **Charisma** — but see the MAD warning below; only Spellblade is single-stat |
| **Hit points** | **10 + CON** at level 1, **6 + CON** per level after (a d10 class) |
| **Saves granted at level 1** | **Constitution + Charisma** |
| **Armour** | Light, **Medium**, **Heavy** |
| **Shields** | **Yes** |
| **Weapons** | Simple **and Martial** |
| **Skills at level 1** | **Two** of Athletics, History, Investigation, Insight, Medicine, Survival, Intimidation, Persuasion |
| **Starting gear** | Longsword, Shield, Half Plate (medium, 15 AC) |
| **Caster tier** | **None.** No spell slots, no spell list. "Spellcasting stat is Charisma" exists to set save DCs. Spellblade gets **cantrips only**; Nighthawk gets one 1/long-rest spell |
| **Resource cadence** | **Willpower Dice — short rest.** Count = Proficiency Bonus (2 at 1, 3 at 5, 4 at 9, 5 at 13, 6 at 17). Size 1d4 → **1d6 at 5** → **1d8 at 11** → **1d10 at 17** |
| **Long-rest resources** | Only the capstone-ish ones: Legendary Resistance (15), Beyond All Limits (18), each subclass's level-17 finisher, Nighthawk's Protection from Evil and Good |
| **Extra Attack** | **Level 5** (three attacks for 3 turns at 18) |
| **Subclass** | **Level 3** ("Heroic Title"), further features at **6, 9, 13, 17** |
| **Feats** | Mod page shows 4/8/12/16/19 — **overridden in Listo.** See feat cadence note |
| **Key breakpoints** | **1** (armour + saves), **2** (Fighting Style + Actions Speak Louder), **3** (subclass), **5** (Extra Attack + d6 + Taunting/Feinting Blade), **7** (Those Who Help Others), **11** (Tag Team Maneuver + d8), **18** (Beyond All Limits), **20** (+4/+4 capstone) |
| **Dip value** | **Very high at 1 (opener only) and at 3 (feat-neutral, works from any position).** See Dip value |
| **Requirements, all present in 10.2** | `5e Spells` (`125`), `AnimationUnlocker` (`16058`) |
| **Supported mods, both present** | `DART` (`17561`) — dialogue tags; `UA Fighting Styles` (`19693`) — **widens the level-2 style menu** |

### Feat cadence — the mod page is wrong for Listo

The Paragon page lists feats at **4, 8, 12, 16, 19** (vanilla cadence). Listo overrides this
globally with `Universal Feat Every X Level(s) - MCM` (`13193`): **feats at 3, 6, 9, 12, 13, 15, 18
for all classes**, with an extra at 11 for **Fighter and Rogue only** — Paragon is
**not** on that list, so a Paragon character gets **six** feats, not seven. See
`data/listo-10.2-feats.md`. `(unverified whether the class's own 4/8/12/16/19 feat entries are
removed by the universal mod or stack on top of it — check the level-up screen at 4)`.

---

## The level-1-or-nothing rule — **partly corrected**

The skill's premise ("must be taken at level 1 or it grants none of that") is **too strong**.
The mod page states exactly one sentence on this:

> **Multiclassing-** Multiclassing into Paragon will not give new Skills, Saving Throw
> proficiencies, or proficiency in Heavy Armor.

So the multiclass node withholds **three** things:

| Lost on a late Paragon level | Still granted on a late Paragon level |
|---|---|
| **Constitution + Charisma saves** (unobtainable from any later class, lost silently on respec) | **Shields** `(unverified — not excluded by the mod text)` |
| **Heavy armour** | **Martial weapons** `(unverified — not excluded)` |
| **The two starting skills** | **Light and medium armour** `(unverified — not excluded)` |
| | All class features: Willpower Dice, Blade Skills, Distract, Fighting Style, subclass, Extra Attack |

**Correction to `references/listo-rules.md`.** The dip table row currently reads
*"Paragon 1 | Heavy armour, shields, martial weapons, Con + Cha saves — must be first or it
grants none of it."* The "none of it" is wrong: a late Paragon dip still gives **shields,
martial weapons and medium armour** — it loses **heavy armour, both saves and the skills**.
That distinction matters, because a mid-run Paragon 3 dip is still a real package (see below);
only the *armour-and-saves* half is level-1-exclusive.

The practical rule is unchanged in shape but narrower in force:

- **Want Con + Cha saves or heavy armour from Paragon → Paragon must be your class at level 1.**
- **Want Willpower Dice, a Heroic Title, Actions Speak Louder or a Fighting Style → any position
  works.**

---

## The Charisma trap, sharpened

Paragon grants **Con + Cha** saves at level 1, and Charisma is its named primary. Lone Wolf
grants **+4 to two abilities with save proficiency in both** (`references/listo-rules.md`), and
the level 1 class is the only other source of save proficiencies — ceiling four distinct saves.
Put Lone Wolf's +4 on Charisma next to a Paragon 1 and **one of the four grants is burned on a
duplicate**, leaving three distinct saves.

What makes this sharper for Paragon than for the other six Charisma-save classes:

- **Paragon must be the level 1 class to be worth opening with at all** (heavy armour + saves),
  so you cannot dodge the collision by reordering classes the way a Sorcerer or Warlock can.
- **Paragon is not actually single-stat.** Weapon attacks use **Strength or Dexterity** for every
  subclass except Spellblade. Charisma feeds the *riders*: Feinting Blade's AC reduction
  (½ PB + CHA), Lionheart's Banner Charges and Yellow Banner AC (= CHA mod), Regent's Oberon's
  Favor stacks (= CHA mod), Nighthawk's Scorching Rebuke damage (= CHA mod), Sword Saint's
  initiative bonus, A Hero's Renown, and — `(unverified, the page never states the DC formula)` —
  the save DCs on Forceful/Taunting/Feinting Blade and Fairy's Curse, which is called "your Spell
  Save DC". So a typical Paragon wants **STR/DEX + CON + CHA**: three stats, one Lone Wolf pair.
- Consequence: the +4 pair on **STR/DEX + CON** or **STR/DEX + WIS** is often better than putting
  it on Charisma, because Charisma at 16 still functions (the riders scale gently) while the
  attack stat at 16 does not. That is the opposite of the advice for a Charisma *caster*.
- **The exception is Spellblade**, whose Scholar's Armament makes the main-hand weapon use
  **Charisma for attack and damage rolls**. A Spellblade is genuinely single-stat and *does* want
  the +4 on Charisma — accepting the wasted Cha-save duplicate — or wants Charisma carried by
  items instead (see `data/listo-10.2-equipment.md`, Mirror of Loss and the Charisma items).

Practical spreads to enumerate, jointly with the +4 (never decide these separately):

| Opener | Lone Wolf +4 pair | Distinct saves | Note |
|---|---|---|---|
| Paragon 1 | **STR (or DEX) + WIS** | Con, Cha, Str/Dex, **Wis — 4** | Best save spread; Wisdom is the highest-value save per `listo-rules.md`. Charisma must come from point buy + items |
| Paragon 1 | **CHA + WIS** | Con, Cha, Wis — **3** | One grant wasted. Only correct for **Spellblade**, where Cha is the attack stat |
| Paragon 1 | **STR/DEX + CON** | Con, Cha, Str/Dex — **3** | Wastes the Con duplicate too — avoid; Paragon already gives Con |

---

## Core mechanics

### Willpower Dice — the whole engine

A pool equal to your **Proficiency Bonus**, **restored on short rest**, spent one at a time.
In a run where a long rest costs 120+ camp supplies scaling with camp population, a martial
whose entire kit runs on a short-rest pool is structurally cheap to operate — this is the single
biggest economy argument for the class. The dice are also *reactive*: several features **refund**
them (Prodigy on a nearby natural 20, Regent on a nearby natural 1, Sword Saint on your own
natural 20), and level 7's Those Who Help Others **does not expend** one at all.

### Level-by-level

| Lvl | Feature |
|---|---|
| **1** | **Humble Origins** — add CHA mod to Insight checks. **Paragon's Help** — a compatibility copy of Help; every Paragon feature referring to "Help" means this one. **Distract** — Action, melee, applies Distracted so the next attack roll against the target has **Advantage**. **Blade Skills** — usable after a weapon or unarmed attack, cost a Willpower Die, add a roll of it to damage, plus a rider. Start with **Forceful Blade** (STR save or pushed 6m) and **Graceful Blade** (+3m movement and Disengage) |
| **2** | **Fighting Style** — Archery, Dueling, Great Weapon Fighting, Two-Weapon Fighting; **plus** Close Quarters Shooter, Tunnel Fighter, Mariner, Interception, Superior Technique because `UA Fighting Styles` is installed. **Actions Speak Louder** — after hitting with a weapon or unarmed attack, **Help and Distract become Bonus Actions**, and Distract also deals a Willpower Die of damage |
| **3** | **Heroic Title** (subclass) |
| **5** | **Extra Attack.** Willpower Dice → **d6**, pool → 3. **Taunting Blade** (WIS save or Disadvantage attacking anyone but you). **Feinting Blade** (WIS save or **AC reduced by ½ PB + CHA mod** until the start of their next turn) |
| **7** | **Those Who Help Others** — once per turn, when hit by an attack or when you fail a save, add a roll of your Willpower Die to that AC or that save. **Does not expend the die.** Effectively a free, every-turn defensive reroll |
| **10** | **Words of Affirmation** — Actions Speak Louder's Help and Distract reach **9m (30ft)**, and Help also grants the ally **+4.5m (15ft) movement**. **A Hero's Renown** — add a Willpower Die roll to any Charisma check |
| **11** | **Tag Team Maneuver** — when you Help an ally via Actions Speak Louder, **they make a weapon or unarmed attack as a Reaction**. Willpower Dice → **d8** |
| **13** | Pool → 5 |
| **14** | **Determined Mind** — immune to Charmed and Frightened |
| **15** | **Legendary Resistance** — auto-succeed one failed save, 1/long rest |
| **17** | Willpower Dice → **d10**, pool → **6** |
| **18** | **Beyond All Limits** — Bonus Action, 1/long rest. For 3 turns: movement doubled, **regain all Willpower Dice at the start of each turn**, and **3 attacks per Action** |
| **19** | Feat (Listo cadence: 18) |
| **20** | **Paragon Of Legend** — **+4 STR/CHA or +4 DEX/CHA, capping at 25** |

### Three things that specifically matter for a duo

1. **Actions Speak Louder + Lone Wolf's extra Bonus Action** = up to **two** Help/Distract
   applications per turn from level 2, gated only on landing a weapon hit first. Distract hands
   your partner **Advantage** on their next roll and does damage on top.
2. **Tag Team Maneuver (11)** hands your partner a **free weapon attack on their Reaction**, every
   time you Help them. Lone Wolf gives each character an *extra* Reaction, so the partner can
   take the Tag Team attack **and** still hold a normal Reaction (opportunity attack, Riposte,
   Counterspell). In a two-person party there is exactly one ally to point this at, which means
   none of the targeting value is diluted the way it would be in a four-person party — this is
   the rare "party support" feature that is *better* in a duo, not worse.
3. **Paragon's Help at 9m from level 10** `(unverified whether the compatibility copy retains
   vanilla Help's ability to raise a downed ally — the page does not say)`. If it does, it is a
   **bonus-action ranged pick-up** in a run where losing either character usually ends the fight.
   Verify this in-game before building the plan around it.

---

## Subclasses

**Six, confirmed** — the manifest description, the mod page, and the level tables all agree:
Lionheart, Nighthawk, Prodigy, Regent, Spellblade, Sword Saint. All six get features at **3, 6,
9, 13, 17**. The author plans more later; **only these six exist in the 1.01 archive Listo ships**.

### Lionheart
- **Mechanics:** **L3 Banner Lord** — a *separate* pool of **Banner Charges = CHA modifier**,
  spent as an **Action** to raise a banner; **banners count as attacks for Extra Attack**, so
  post-5 you can banner *and* swing. **Red Banner**: an ally within 9m makes a Reaction attack
  with +1 Willpower Die damage. **Blue Banner**: allies within 18m Reaction-dash to you, free of
  movement and opportunity attacks. **Yellow Banner**: an ally gets **+CHA mod AC for 2 turns**.
  Plus **Knight's Training** (one extra skill proficiency). **L6 Unwavering Standard — Banner
  Charges move from long rest to short rest.** **L9 Vanguard's Charge** — after your first turn
  in combat, attacks against you have **Disadvantage** until your next turn; **Improved Banners**
  — Red can carry Forceful (DC 12 + ½ level) or Graceful Blade, Blue grants allies one use of
  Those Who Help Others at 1d4, Yellow buffs **your** AC as well. **L13 Vanguard's Glory** —
  opportunity attack when an enemy *enters* your melee range (not just when it leaves).
  **L17 Legendary Banner** — Action, 1/long rest, free of charges: an ally gets doubled movement,
  +CHA AC, and a **free attack every turn** for CHA-mod turns.
- **Duo relevance:** the strongest of the six for this run. Red Banner is a second Tag Team on a
  different resource, Yellow is transferable AC for the squishier half of the pair, and L6 puts
  the whole package on the short-rest clock. L9's blanket Disadvantage-on-attacks-against-you is
  a genuine anchor effect.

### Nighthawk
- **Mechanics:** **L3 Searing Blade** — a Blade Skill dealing Fire damage that forces a CON save;
  on a fail the target **loses all resistances for 3 turns**. **Vigilant Aegis** — your Help also
  grants **Protection from Evil and Good** for 2 turns; plus one free cast per long rest.
  **Superior Darkvision** 24m. **L6 Supernatural Dampening** — a resistance-stripped creature
  **cannot regain hit points**, has Disadvantage on spell attacks, and is treated as **in
  sunlight**. **L9 Iron Filings** — your Fire damage applies a **stacking** 1d4 Fire per turn;
  **Scorching Rebuke** — Reaction, CHA-mod Fire damage to whoever hits you. **L13 Bird Cage** —
  Fire damage forces a CHA save or 1d10 Fire at end of turn for 3 turns unless the target stays
  within 6m of you. **L17 Strike Out Against The Night** — 1/long rest, +7d10 Fire, **automatic
  critical** if the target's resistances are stripped.
- **Duo relevance:** the debuff subclass. Resistance-strip plus no-healing plus treated-as-sunlit
  is a two-character answer to the list's tankier bosses and to undead — and it makes your
  partner's damage type stop mattering. Bird Cage punishes anything that tries to disengage from
  the front-liner, which is where a duo bleeds tempo.

### Prodigy
- **Mechanics:** **L3 Sheer Will** — Bonus Action, one Willpower Die: temp HP = die + CHA mod,
  and **while you hold those temp HP you take 1 less damage from every source** (2 at Paragon 9,
  3 at 17). **Competitive Streak** — regain a Willpower Die whenever someone *other than you*
  nearby rolls a natural 20 on an attack or save. **Innate Mastery** — **+1 to attack and damage
  with weapons**, rising to +2 at 9 and **+3 at 17**. **Natural Talent** — one extra skill.
  **L6 Brilliance** — Sheer Will also grants an ally within 9m temp HP (no damage reduction).
  **L9 Willful Blade** — first weapon hit each turn deals +1 Willpower Die. **L13 Training From
  Hell** — **resistance to non-magical bludgeoning, piercing and slashing**. **L17 Echo of the
  Soul** — 1/long rest, DEX save, 6d10 Radiant + 1d10 per nearby ally (max +5d10), half on save,
  and nearby enemies make a WIS save or are Frightened.
- **Duo relevance:** the durability pick, and it stacks multiplicatively with Lone Wolf's halved
  damage — flat "-3 damage from all sources" is worth far more when the incoming number has
  already been halved, and physical resistance stacks on top of that again at 13. Competitive
  Streak refunds off your *partner's* crits, so a crit-fishing partner (see the crit-threshold
  rings in `data/listo-10.2-equipment.md`) actively feeds your resource pool. Note Echo of the
  Soul's ally-count scaling is nearly dead in a duo: +1d10, not +5d10.

### Regent
- **Mechanics:** **L3 Shifting Court** — alternate Help and Distract that cost a Willpower Die,
  **swap your position with the target's**, and grant **Oberon's Favor stacks = CHA mod**.
  **Fickle Fortune** — regain a Willpower Die when a nearby creature rolls a natural 1.
  **Oberon's Favor** — weapon attacks deal +1 Willpower Die **Psychic**; one stack consumed per
  weapon attack. **L6 Strike Of The Butterflies** — while empowered by Oberon's Favor, **crit
  threshold −½ PB** (−1, then **−2 at L9**, **−3 at L17**). **L9 Fairy's Curse** — a crit on an
  empowered attack forces a CHA save vs your Spell Save DC or the target is **Cursed: half
  movement, no Bonus Actions, no Reactions**. **L13 Eternal Bloom** — +1 stack at the start of
  each of your turns. **L17 Butterfly Tempest** — 1/long rest, teleport-strike **5 targets** for
  6d10 Psychic each, then regain CHA-mod stacks.
- **Duo relevance:** the position-swap is the answer to the duo's worst failure mode — your
  partner caught alone in the middle of a pack. Swapping Help/Distract pulls them out and puts
  the armoured character in, on a **Bonus Action** once Actions Speak Louder is online. Fairy's
  Curse stripping an enemy's Reactions and Bonus Actions is the class's best action-economy
  denial, which is the structural axis of this run. Crit threshold −3 stacks (in principle) with
  `Critfisher Ring` and `Ring of Viciousness` — `(unverified whether these stack; the equipment
  file flags the same question)`.

### Spellblade — **the exception the skill suspected, but not a caster**
- **Mechanics:** **L3 Spell Sword** — pick **2** of ten elemental Focuses, +1 more at 6, 9, 13
  and 17 (**6 total**). Each Focus grants a **cantrip** plus a **Spell Sword attack**; these
  attacks are **treated as cantrips and work with Extra Attack**. **Scholar's Armament** —
  enchant your **main-hand melee weapon**: damage becomes magical, it cannot be disarmed or
  removed from inventory, and it **uses Charisma for its attack and damage rolls**. **Arcane
  Knowhow** — **expertise** in Arcana. **Arcane Style** — cosmetic Bladesinger animations.
  **L6 Arcane Surge** — spend a Willpower Die to cast Spell Sword attacks **at your current
  level** rather than as level 1. **L9 Magic Resistance** — Advantage on saves vs spells and
  magical effects. **L13 Will Over Weave** — Reaction + Willpower Die to force an enemy caster's
  INT save or **their spell fails entirely** (a Counterspell that costs no slot). **L17 Beloved
  By Mana** — resistance to spell damage; your spells and Spell Sword attacks get **−1 crit
  threshold and Advantage on damage rolls**.
- The Focuses: Acidity (Acid Splash / Corrosive Smash, 1d6+CHA Acid, applies Acid), Frost (Ray of
  Frost / Freezing Pierce, 1d8+CHA Cold), Fire (Firebolt / Blazing Blade, 1d10+CHA Fire), Force
  (Sword Burst / Slashing Blades, 1d6+CHA Force, hits enemies around the target), Lightning
  (Shocking Grasp / Shocking Slash, 1d8+CHA Lightning, **Advantage vs metal armour**), Necrosis
  (Toll the Dead / Ringing Strike, 1d12+CHA Necrotic, only 1d8 at full health), Poison (Poison
  Spray / Envenomed Strike, 1d12+CHA Poison), Psionics (Mind Sliver / Inner Feint, 1d6+CHA
  Psychic), Radiance (Sacred Flame / Luminous Blade, 1d8+CHA Radiant), Thunder (Thunderclap /
  Shattering Slam, 1d6+CHA Thunder, hits enemies around the target).
- **Verdict on the "no spell slots" belief: it holds.** Spellblade gets **cantrips and
  cantrip-like weapon attacks only** — no slots, no prepared list, no upcasting beyond Arcane
  Surge's level scaling. Nighthawk's one Protection from Evil and Good per long rest is the
  class's only true spell.
- **Duo relevance:** the only genuinely single-stat build, and the only one that makes Charisma
  the attack stat — which is what resolves the Charisma trap in its favour rather than against
  it. **Will Over Weave at 13 is slot-free Counterspell on a short-rest die**, which a duo with
  no dedicated caster otherwise has no access to. Damage-type flexibility (six Focuses by 17)
  covers the resistance gaps a two-character party cannot cover with gear alone. Cross-reference
  **Potent Robe** in `data/listo-10.2-equipment.md` — it adds Charisma to cantrip damage, and
  Spell Sword attacks are "considered cantrips" `(unverified whether Potent Robe actually fires
  on them; if it does it is a large, cheap damage add, but the robe is Alfira's reward and she
  must be kept alive)`.

### Sword Saint
- **Mechanics:** **L3 Disciple of Steel and Strategy** — regain a Willpower Die on **your own**
  natural 20 attack roll. **Wisdom of Water** — whenever you spend a Willpower Die you may cast
  **Falling Rain**: a **free-action** melee weapon attack using 1d4 in place of the weapon's
  damage dice. **L6 Wisdom of Fire** — each weapon attack grants a stack of **Fanning the
  Flames** (+1 Fire damage on melee weapons and +1 temp HP per stack; stacks clear at the start
  of your turn). **L9 Wisdom of Earth** — **Blindsight**, darkvision, immune to Blinded.
  **L13 Wisdom of Wind** — each weapon attack grants a stacking +3m movement for the turn, and
  add **CHA mod to Initiative**. **L17 Wisdom of Void** — 1/long rest, spend **6 Willpower Dice**
  to enter **Nirvana** for the rest of the turn: **every attack roll counts as a natural 20**,
  and weapon attacks deal +1d10 Slashing.
- **Duo relevance:** the pure-throughput pick and the one that most rewards Lone Wolf's extra
  Action, because Falling Rain is a **free action** riding on every Willpower Die you already
  spend — more Actions means more Blade Skills means more free attacks. Note the L17 finisher
  wants **6 dice**, which is exactly the level-17 pool, so it is realistically once per short
  rest at best and pairs with **Beyond All Limits** at 18 (which refills the pool every turn) for
  one enormous auto-crit round. CHA to Initiative matters more in a duo, where going first
  decides whether you get to set the front line at all.

---

## Dip value

**Paragon 1 as the opener — very strong, and it returns feats.**
It grants **Con + Cha saves, heavy armour, shields, martial weapons, two skills**, plus Distract,
two Blade Skills and **2 short-rest Willpower Dice**. Against `data/listo-10.2-feats.md`:

- **Moderately Armoured** (medium armour **and shields**) — **returned**.
- **Heavily Armoured** (heavy armour, +1 STR or CON, +1 to saves with it) — **returned**.
- **Lightly Armoured** is the stated prerequisite for Moderately Armoured, so a character with no
  armour proficiency pays that too — **a third feat returned** in the worst case.
  `(unverified whether Heavily Armoured additionally requires Moderately Armoured in Listo; the
  feats file does not state a prerequisite for it.)`
- It also **unlocks Heavy Armour Master**, which the feats file notes does nothing without heavy
  armour proficiency, and which in Listo reduces **all** damage by PB (capped 5).

**Quantified: Paragon 1 returns 2 feats, or 3 if the character would otherwise have started from
zero armour proficiency — out of six.** That is a third to a half of the character's entire feat
budget recovered by a single level, on top of two save proficiencies that no later level can buy.

**Paragon 3 as a mid-run dip — feat-neutral and still worth it.** Listo's 3/6/9/12/13/15/18 cadence
keys off class level, so a 3-level block costs no feat. Paragon 3 taken *after* level 1 still
delivers **Fighting Style** (with the UA styles), **Actions Speak Louder**, a full **Heroic
Title**, **shields and martial weapons**, and 2 Willpower Dice — losing only heavy armour, the
saves and the skills. Two specific cases:

- **Spellblade 3 on a Charisma character** is the standout: Scholar's Armament converts a
  main-hand weapon to **Charisma attack and damage**, which turns any Charisma caster into a
  functional melee threat without a second stat. Effectively a Hexblade-shaped dip that no other
  class in the list provides.
- **Lionheart 3** on a support character buys the Banner suite outright (though Banner Charges
  stay on the long-rest clock until Paragon **6**, which is the level that makes them worth it —
  a 6-level commitment, not a dip).

**Paragon 5** buys Extra Attack, but only matters on a character that does not already have it.

**Against dipping *out* of Paragon.** The back half is heavily loaded — Tag Team Maneuver at 11,
d10 dice and 6 of them at 17, Beyond All Limits at 18, and the **level 20 capstone Paragon Of
Legend (+4 to two stats, cap 25)**. With this run's level cap at exactly 20, that capstone is
reachable **only by pure Paragon 20**, and it is the single largest stat source in the file —
larger than Lone Wolf's +4, and it **breaks the 20 ceiling that Lone Wolf and the ASI feat both
stop at** (compare the source table in `references/listo-rules.md`). Any dip out of Paragon
costs that capstone. Treat Paragon as **all-or-nothing in both directions**: it wants to be your
level 1 class *and* it wants to be all 20 levels.

---

## Verdict on the four prior beliefs

| Belief | Verdict |
|---|---|
| Subclasses are Lionheart, Nighthawk, Prodigy, Regent, Spellblade, Sword Saint | **Confirmed** — exactly six, all present in the 1.01 archive |
| Charisma-based with **no spell slots** | **Confirmed.** Spellblade is cantrips-only; Nighthawk has one 1/long-rest spell. No slots anywhere. But see the MAD warning — Charisma is the *stat*, not the attack stat, outside Spellblade |
| Heavy armour, shields, martial weapons, Con + Cha saves at level 1 | **Confirmed** verbatim, plus light/medium armour, simple weapons and two skills |
| Must be level 1 **or it grants none of that** | **Corrected.** The multiclass node withholds only **skills, saving throws and heavy armour**. Shields, martial weapons, medium armour and every class feature still arrive `(the "still granted" half is inference from what the mod text does *not* exclude — verify at a level-up screen)` |

---

## Not present / known issues

- **No version drift.** Listo pulled 1.01 and 1.01 is current on Nexus as of this compile. The
  1.01 changelog is almost entirely tooltip rewording plus removal of a misused `IsAttack` tag;
  the one gameplay change is that **Scholar's Armament now requires an equipped melee weapon**
  and reads "main-hand melee weapon" rather than "right-hand weapon".
- **Zero reported bugs on the Nexus page** at compile time (Bugs tab: 0, Posts: 33,
  Endorsements: 27). That is a *very* small sample — this mod is ~10 weeks old and was added to
  Listo for playtesting before its official release. Treat unusual interactions as untested.
- **The companion item mod `Valor and Virtue` is not in the 10.2 list.** The author describes it
  as a GraphicFade-style item mod designed to complement Paragon. Do not plan around Paragon-
  specific gear; the class has none.
- **Only 6 of a planned 16 subclasses exist.** A future Listo update may add more; the six above
  are what 10.2 ships.
- **Save DC formula is never stated** on the mod page for Blade Skills. Fairy's Curse says "your
  Spell Save DC", and Lionheart's banner-triggered Forceful Blade uses a fixed "DC 12 + half your
  level", which implies the two are *different* formulas. `(unverified — confirm the Blade Skill
  DCs on a tooltip in-game before building around Feinting/Taunting Blade as reliable control.)`
- **`Paragon's Help` is a compatibility copy of Help**, not Help itself. Whether it triggers
  effects keyed to vanilla Help (including raising a downed ally, and any item or feat that keys
  off Help) is **unverified** and is the most load-bearing unknown in this file for a duo.
- **Interaction with `Universal Feat Every X Level(s)`** — the mod's own 4/8/12/16/19 feat entries
  versus Listo's 3/6/9/12/13/15/18 cadence is `(unverified)`. If they stack, Paragon quietly becomes
  the most feat-rich class in the list; if they do not, it gets the standard six.
- **`DART` support** (`17561`) means the class has dialogue tags wired up — flavour reactivity,
  no mechanical effect on a build.
