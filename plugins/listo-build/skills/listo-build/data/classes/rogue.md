# Listonomicon 10.2 — Rogue

Rogue in Listo is a **skill and action-economy class that happens to do damage**, not the other
way round. The chassis is close to vanilla — Dex/Int saves, Expertise at 1 and 6, Sneak Attack,
Cunning Action at 2, Uncanny Dodge at 5, Evasion at 7, Reliable Talent at 11 — but three things
change the maths. **Cunning Strike** (`507`) turns Sneak Attack dice into a rider budget from
Rogue 5, so a Rogue can spend damage on Prone/Poison/Disarm/reposition every single turn.
**Goon's Rogue Overhaul** (`17612`) rebuilds Sneak Attack and Uncanny Dodge as interrupts and
fixes the off-turn cases, so Sneak Attack fires on reactions — which matters a great deal when
Lone Wolf hands you a second reaction. And **Book of Rogues** (`19717`) adds five full 5e
subclasses that are featured to level 17, next to the four vanilla ones and a tenth from
`(DTO) Otherworldy Archetypes`. Rogue is also on the **eight-feat cadence** (a feat at 11 that
most classes don't get). The docs' Rogue section is **stale in one concrete way**: it advertises
`Second-Story Work Dexterity Jump`, which is **not in the 10.2 list**.

**Provenance.** Compiled 17 August 2026 against the bundled 10.2 snapshot. Every mod named here
was confirmed in `listo-10.2-mods.tsv`; every *file variant* was confirmed in
`listo-10.2-manifest.json`. Vanilla baselines come from bg3.wiki. Anything not read directly is
marked `(unverified)`.

---

## At a glance

| | |
|---|---|
| **Primary ability** | Dexterity (attacks, AC, Sneak Attack, most Cunning Strike save DCs). Int for Arcane Trickster spells; Cha for Swashbuckler's Dirty Tricks except Sand Toss; Int for Seeker |
| **Saves at level 1** | **Dexterity + Intelligence** — only if Rogue is your *first* class. Dex is the most-rolled save in the game and Int is the classic dump-save hole, so this is one of the better save pairs on offer |
| **Hit points** | 8 + Con at 1, 5 + Con per level (d8) |
| **Armour / weapons** | Light armour; simple weapons, hand crossbows, longswords, rapiers, shortswords. No shields, no medium armour |
| **Skills** | **4 at level 1** — the largest starting pick of any class except Bard. Full list: Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Performance, Persuasion, Sleight of Hand, Stealth |
| **Expertise** | **2 skills at level 1, 2 more at level 6** (4 total). Skills only — not tools |
| **Multiclass entry** | Light armour + **1** skill. No saves, no Expertise-at-1 bonus skills. Rogue-as-dip is much weaker than Rogue-as-first-class |
| **Resource cadence** | Sneak Attack: **once on your turn plus once off-turn** on a reaction attack (Cunning Strike rework), refreshing every round — **no rest clock**. Everything else is at-will (Cunning Action) or a subclass short/long-rest ability. **Rogue is nearly rest-free**, which is worth real money when a long rest costs 120+ supplies |
| **Feats** | **3, 6, 9, 11, 12, 13, 15, 18** — eight, see below |
| **Level breakpoints** | **1** Expertise ×2 + Sneak Attack + Dex/Int saves · **2** Cunning Action (Dash/Disengage/Hide) · **3** subclass + Listo feat · **5** Uncanny Dodge + **Cunning Strike** · **6** Expertise ×2 + feat · **7** Evasion · **9** subclass feature + feat · **11** Reliable Talent + **feat** · **13/17** subclass features (all packs) · **14** Blindsense · **15** Slippery Mind (Wis save proficiency) + feat · **18** Elusive + feat · **20** Stroke of Luck |
| **Dip value** | **3 levels** for a subclass + Cunning Action + 2d6 Sneak Attack, feat-neutral. **5 levels** if you want Cunning Strike. **1 level** is a bad dip unless it's your first class |

---

## Feat cadence

**Rogue is one of only two classes on the eight-feat cadence.**

- All classes: feats at **3, 6, 9, 12, 13, 15, 18** — seven
- **Fighter and Rogue**: additionally at **11** — **eight feats** at level 20. Mesmerist is
  named in the docs but its grant is gated behind `enableAdvancedSettings`, which the install
  sets to `false` — see `data/listo-10.2-mcm.md`

Delivered by `Universal Feat Every X Level(s) - MCM` (`13193`) — see `data/listo-10.2-feats.md`.
The cadence keys off **class level**, so the extra feat only exists if you take **Rogue to 11**,
and a 3-level Rogue dip still collects its own level-3 feat.

Note what this does to the class's shape: vanilla Rogue's feats sit at 4/8/10/12, Listo's at
3/6/9/11/12/13. **Level 11 is now the single biggest Rogue level in the game** — Reliable Talent,
the 6th Sneak Attack die, and a feat all at once. Any plan that stops Rogue at 9 or 10 is
leaving the class's best level on the table.

---

## Class changes from vanilla

### Cunning Strike — `UA6 Cunning Strike and Swashbuckler` (`507`)

- **File pulled:** `Cunning Strike-507-1-6-1-1749372011.zip` — **main file only, version 1.6.1**
  (the current Nexus version). Read the "Not present" section below about the Swashbuckler
  optional file.

Two separate things in one mod.

**Sneak Attack rework (Rogue 1):**
- Sneak Attack can be used **once on your own turn and once off-turn** if you get a reaction
  attack — as in tabletop. With Lone Wolf's extra reaction this is a real second Sneak Attack
  most rounds.
- Sneak Attack used from the action bar **no longer burns the attempt on a miss**.
- The reaction is **no longer blocked by invisibility** or appearance-changing effects.
- The reaction **no longer applies damage riders** at any difficulty (vanilla only got this
  right in Honour mode).
- Where off-turn Sneak Attack can't be implemented, you instead get **two Sneak Attacks on your
  own turn** — specifically with **Commander's Strike**.
- Adds **"Hold Sneak Attack"**: usable when you have an action and reaction but no Sneak Attack
  charge (e.g. Hasted or Action Surged and already used it). It pre-buys the upcoming reaction
  Sneak Attack but **blocks movement, non-actions and Extra Attack** while held.

**Cunning Strike (Rogue 5):** when you deal Sneak Attack damage, forgo dice to add an effect.
Save DC = **8 + Proficiency Bonus + Dexterity modifier**.

| Effect | Cost | What it does |
|---|---|---|
| **Trip** | 1d6 | Large or smaller target: Dex save or **Prone** |
| **Poison** | 1d6 | Con save or **Poisoned 1 minute**, save at end of each of its turns. **Requires a Poisoner's Kit on your person** |
| **Withdraw** | 1d6 | Move up to **half your Speed** immediately after the attack, no Opportunity Attacks |
| **Disarm** | 1d6 | Dex save or drop one held item of your choice. **Toggled OFF by default** — enable it in the Reactions UI |

> The mod page says rings unlocking Cunning Strike early can be found in a Cartilaginous Chest in
> the tutorial. Whether that chest survives Listo's loot edits is **(unverified)**.

### Goon's Rogue Overhaul (`17612`)

- **File pulled:** `Goon's Rogue Overhaul-17612-1-2-2-0-1771175282.zip` — **version 1.2.2.0**.
  **The Nexus page describes version 2.1.0.1.** Listo is pinned behind because 2.1.0.0 requires
  Goon's Library 4.23.0.0+ and Listo ships **Goon's Library 4.9.0.0**. Read the page with that
  discount; the 2.x-only items are listed at the end of this section.

What **is** in 1.2.2.0:

- **Uncanny Dodge** is now an **Interrupt**, not an auto-firing passive. It only triggers from
  being attacked or from an evadable AoE, works under all non-hostile polymorphs, and fixes
  every bug listed on the wiki page. **You now choose when to spend it** — with Lone Wolf's
  second reaction, that is a straight upgrade.
- **Sneak Attack**: damage always matches the weapon's damage type; spell variants only spend a
  charge **on a hit**; the charge is **visible on the hotbar**; interrupts default to **ask**
  rather than fire automatically; **invisible characters can use the interrupts**; per-turn
  cooldowns removed (so a second Sneak Attack charge from any source actually works); Wild Shape
  and Fire Myrmidon can use Sneak Attack interrupts.
- **Dirty Trick: Flick o' the Wrist** now executes weapon functors (damage riders apply) and uses
  a **Dexterity-restricted Maneuver save DC** instead of Spell Save DC; its range matches your
  melee weapon instead of a fixed 1.5 m.
- **Dirty Trick: Sand Toss** uses a Dex-based save DC instead of Spell Save DC; is an unarmed
  attack rather than a weapon attack.
- **Dirty Advantage** no longer falls off when you take a non-attack action; tooltip shows the
  correct **2-turn** duration.
- **Fancy Footwork**'s hidden condition clears at the end of *your* turn, not the target's.
- **Panache** tooltip warnings; disadvantage-removal edge cases fixed.
- **Arcane Trickster** no longer gets 2× level-1 slots at level 10 — it gets **1 level-2 slot**.
- Native support for wesslen's Cunning Strike (`507`); requires **Compatibility Framework**
  (`1933`, present).

**In the Nexus description but NOT in the installed 1.2.2.0** (all arrived in 2.0.0.0+):
the **Rakish Sneak Attack 1:1 5e-RAW rework** (no-advantage Sneak Attack within 2 m with no other
creatures within 5 ft), the Sand Toss change to **static 1 Bludgeoning with no attack roll**, the
Panache **HUMANOID-tag** check, and the fix for **throwing finesse weapons** without a finesse
weapon equipped. Treat Swashbuckler's Rakish Sneak Attack as **vanilla behaviour**.

### Levels 13–20 — `Expansion` (`279`, listed as "Expansion (Bladesinger Only)")

- **File pulled:** `Expansion-279-1-7-3-6-1780876532.zip` (1.7.3.6).

Base Rogue continues: **Sneak Attack dice at 13, 15, 17 and 19** (reaching 10d6), **Blindsense**
at 14, **Slippery Mind** at 15, **Elusive** at 18, **Stroke of Luck** at 20.

- **Blindsense (14):** you are aware of hidden/invisible creatures within 3 m. Implemented via
  script extender — you can attack them but **with disadvantage**, and they lose advantage on you.
- **Slippery Mind (15):** **proficiency in Wisdom saving throws.** Implemented as written. In a
  duo this is the single most valuable non-damage level in the back half — Wis saves are what
  Hold Person, Dominate and fear effects target, and losing one of two characters ends fights.
- **Elusive (18):** no attack roll has advantage against you while you aren't incapacitated. The
  author warns a few homebrew advantage sources may slip through.
- **Stroke of Luck (20):** an interrupt that turns a missed attack into a hit (implemented as
  base roll → 10, +100 bonus), plus a **toggle** that auto-succeeds your next ability check.
  Recharges on a **short rest**. The author calls his own implementation lacklustre.
- **Steady Aim** is an **optional** Expansion feature at level 3 (bonus action, advantage on your
  next attack, speed 0 for the turn). **Listo turns it off** — `optional_features.Rogue: false`
  in the installed `MCM/Expansion/settings.json`. Do not plan around it.

Expansion also adds **13th/17th-level features to Arcane Trickster, Assassin and Thief only**
(detailed under each subclass below). **Swashbuckler gets nothing at 13–20 from Expansion** — it
is a Patch 8 subclass and is absent from Expansion's feature list.

### What did NOT change

- **Second-Story Work is vanilla**: Thief level 3, **resistance to falling damage**. It does *not*
  scale jump distance off Dexterity — see "Not present".
- Expertise, Cunning Action, Evasion, Reliable Talent, saves, proficiencies and the skill list are
  all unmodified.

---

## Subclasses

**Ten subclasses**: four vanilla, five from Book of Rogues, one from Otherworldy Archetypes.

### Thief

- **Mod:** vanilla (Patch 8 base game), bugfixed by Goon's Rogue Overhaul (`17612`); levels 13/17
  from `Expansion` (`279`)
- **Mechanics:**
  - **3 — Fast Hands:** a **second Bonus Action**, usable with any of your bonus actions.
  - **3 — Second-Story Work:** resistance to falling damage. That is all it does in Listo.
  - **9 — Supreme Sneak:** action, become **Invisible**; recharges on **short rest**.
  - **13 — Use Magic Device:** ignore all class, race and level requirements on magic items,
    including branded items. Accounts for `5e Magic Items` items.
  - **17 — Thief's Reflexes:** **two turns in the first round of combat** — normal initiative and
    initiative −10. Implemented via a hotbar toggle plus script extender; the author rates it
    "90–95%" working and warns it **breaks in combats you cannot escape from** and can misbehave
    with **shared turns between allies**.
- **Duo relevance:** the highest-value vanilla pick for two players. A third bonus action (Fast
  Hands + Lone Wolf) is raw action economy, and Thief's Reflexes is effectively a free extra round
  at the start of every fight — but note the shared-turn warning, which is exactly the situation a
  two-player party is in. Fast Hands **does not stack** with the Thief's Apprentice feat.

### Assassin

- **Mod:** vanilla (Patch 8 base game), bugfixed by `17612`; levels 13/17 from `279`
- **Mechanics:**
  - **3 — Assassin's Alacrity:** restore your **Action and Bonus Action** at the start of combat.
  - **3 — Assassinate: Ambush:** any successful attack roll against a **Surprised** creature is a
    **critical hit**.
  - **3 — Assassinate: Initiative:** **advantage** on attack rolls against creatures that haven't
    taken a turn yet.
  - **9 — Infiltration Expertise:** action, change your appearance.
  - **13 — Imposter:** out of combat, copy a creature's appearance **and take on its faction** —
    its allies become yours, yours become hostile. Attacking a faction ally ends it; if that
    target was in combat the attack counts as against a **Surprised** creature, and if it wasn't,
    it becomes "susceptible to becoming surprised" for 10 turns.
  - **17 — Death Strike:** hit a Surprised creature and it makes a **Con save (DC 8 + Dex + PB)**
    or you **double the attack's damage**.
- **Duo relevance:** the alpha-strike pick, and Listo has quietly buffed its enabler — initiative
  is now **d10 + Dex** (`Initiative Variants`, `1247`), so a high-Dex Rogue reliably wins the roll
  and gets the whole first round against creatures that haven't acted. Imposter + Death Strike at
  13/17 is the closest thing in the list to deleting a boss before it acts. The cost is that all
  of it front-loads: against long fights with reinforcements, Assassin contributes least when the
  duo is most at risk.

### Arcane Trickster

- **Mod:** vanilla (Patch 8 base game), bugfixed by `17612`; levels 13/17 from `279`
- **Mechanics:**
  - **3 — Mage Hand Legerdemain:** Mage Hand is **invisible and permanent**. Plus 2 cantrips and
    2 Enchantment/Illusion spells; Int is the casting stat, spell slots on the third-caster table.
  - **9 — Magical Ambush:** while **Hiding**, your targets have **disadvantage** on saves against
    your spells.
  - **10 — one level-2 spell slot** (Goon's fix; vanilla incorrectly gave 2× level-1).
  - **13 — Versatile Trickster:** bonus action, designate a creature within 5 ft of your Mage
    Hand to gain **advantage on attack rolls** against it until end of turn. A temporary spell
    appears on the hotbar when the hand is summoned.
  - **17 — Spell Thief:** reaction when a creature's spell targets or includes you — it saves
    with its casting modifier against your spell save DC, or you **negate the spell against you
    and learn it for 8 hours** while it cannot cast it. **Once per long rest.** Implemented via
    script extender; **AoE, cone and line spells may fail to register the interrupt**.
- **Duo relevance:** the permanent invisible Mage Hand is a third body for levers, buttons and
  distance-pulling that costs nothing per rest — worth more with two characters than four. But
  the spell list is short and Int competes with Dex, and Versatile Trickster is the only feature
  that turns the hand into damage. Take it for the utility, not the casting.

### Swashbuckler

- **Mod:** vanilla (Patch 8 base game), partially bugfixed by `17612` **at 1.2.2.0** — the
  Rakish Sneak Attack RAW rework is **2.x only and therefore absent**
- **Mechanics:**
  - **3 — Rakish Audacity:** **+2 initiative, scaling with Rogue level**. You don't need advantage
    for Sneak Attack while within **1.5 m** of the target with no disadvantage.
  - **3 — Rakish Sneak Attack (Melee/Ranged):** replaces normal Sneak Attack. Usable without
    advantage if **no other combatants are within 2 m of the target**, or if you have an **ally**
    within that range. Per-turn recharge.
  - **3 — Fancy Footwork:** a target you melee attack **can't make Opportunity Attacks against
    you** for the rest of your turn.
  - **4 — Dirty Tricks** (Cha-based except Sand Toss, which is Dex): **Flick o' the Wrist**
    (possible Disarm), **Sand Toss** (possible Blind), **Vicious Mockery** (disadvantage on the
    target's next attack). Goon's fixes to save DCs and range apply.
  - **9 — Panache:** Persuasion check contested by the target's Insight; on a win it takes
    **Panache: Disadvantage**, others who fail become **Charmed**.
  - **13–20:** **nothing.** Expansion does not cover Swashbuckler.
- **Duo relevance:** the only Rogue that gets Sneak Attack **without needing a setup body** — in a
  two-character party there often isn't a second melee to flank with, which is exactly the hole
  Rakish Audacity fills. Cha-based Dirty Tricks also make it the natural Rogue for the party face.
  The catch is the dead back half: no subclass features from 13 to 20, and no `Cunning Strike`
  Swashbuckler variant in the list. If you plan to reach 17+, Thief, Assassin or a Book of Rogues
  subclass all keep growing and this one does not.

---

The five below are all from **Book of Rogues — 5e Rogue Subclasses** (`19717`), file pulled
`Book of Rogues - 5e Rogue Subclasses-19717-1-0-0-3-1773202170.zip` (**1.0.0.3**, current).
Features at **3, 9, 13, 17** — fully featured to 17 with no Expansion dependency.

`Cunning Strike - Book of Rogues Compatibility Patch` (`20687`, file
`Cunning Strike - Book of Rogues Compatibility Patc-20687-1-0-0-0-1768337822.zip`) is installed
and load-ordered below both. It collapses the duplicate Sneak Attack entries down to wesslen's
improved **Sneak Attack (Melee)** and **(Ranged)**, and makes **Wails from the Grave**,
**Insightful Fighting**, **Eye for Weakness** and **Sudden Strike** work with both Sneak Attack
*and* all four Cunning Strike interrupts. **Caveat: the patch was authored against Book of Rogues
1.0.0.2 and Listo ships 1.0.0.3**, whose changelog says it *restructured the level-3 progressions
file*. The patch has not been updated. Its author also says he **did not test the level 17
features**. `(risk — verify the subclass list and level-17 behaviour in-game)`

Book of Rogues also **reworks Uncanny Dodge into a reaction pop-up**, which is a second mod
touching the same feature as Goon's interrupt version. Which implementation wins depends on
Listo's load order, which the manifest does not expose. `(unverified — expect one or the other,
not both)`

### Inquisitive

- **Mod:** Book of Rogues (`19717`)
- **Mechanics:**
  - **3 — Ear for Deceit:** on an Insight check you **cannot roll below 8** on the die.
  - **3 — Eye for Detail:** roll a Perception check to search for hidden and invisible creatures;
    revealing any gives your **next attack against them advantage**.
  - **3 — Insightful Fighting:** roll an Insight check to be able to use **Sneak Attack against
    that target even without advantage**.
  - **9 — Steady Eye:** **advantage on Perception and Investigation checks** (the mod drops 5e's
    "half movement" restriction).
  - **13 — Unerring Eye:** uncover invisible or disguised creatures within 9 m; identified this
    way they **cannot become invisible again** and take a **penalty to attack rolls equal to your
    Proficiency Bonus**. Uses per long rest = **Wisdom modifier (min 1)**.
  - **17 — Eye for Weakness:** while Insightful Fighting applies to a target, your Sneak Attack
    damage against it **increases by 3d6**.
- **Duo relevance:** the strongest single answer to Rogue's structural problem in a two-person
  party — **Insightful Fighting is a repeatable, no-ally-required Sneak Attack enabler**, and it
  scales into a flat +3d6 at 17. Steady Eye plus Reliable Talent plus Expertise makes one
  character cover Perception and Investigation for the whole campaign. Note the Wis dependency on
  Unerring Eye, which a Dex/Con Rogue will not have.

### Mastermind

- **Mod:** Book of Rogues (`19717`)
- **Mechanics:**
  - **3 — Master of Intrigue:** **advantage on Deception and Performance** checks; gain
    **Disguise Self**.
  - **3 — Master of Tactics:** use the **Help action as a Bonus Action**; alternatively spend a
    bonus action to grant an **ally advantage on their next attack**.
  - **9 — Insightful Manipulator:** Insight check against a humanoid's Int, Wis or Cha score; on a
    failure they take a **penalty to saving throws of that ability equal to your Wisdom modifier**.
  - **13 — Misdirection:** when you are the target of an attack while another creature is within
    2 m of you, **reaction** to force the attacker to **choose a different target**.
  - **17 — Soul of Deceit:** **+ Wisdom modifier to Deception checks**, and **immunity to Charmed**.
- **Duo relevance:** Master of Tactics is a bonus-action **Help** — with two characters, picking
  your partner up off the floor without spending your Action is a fight-saving button, and Lone
  Wolf's extra bonus action means you rarely have to choose. Granting advantage as a bonus action
  also feeds a partner who needs it (Paladin smites, big single hits). Misdirection is a
  hard-redirect that only works with a body nearby, which in a duo means your partner — read it as
  "hand the hit to the tankier one". Insightful Manipulator's Wis scaling is a poor fit for a
  Dex build.

### Phantom

- **Mod:** Book of Rogues (`19717`)
- **Mechanics:**
  - **3 — Whispers of the Dead:** once per **short rest**, become **proficient in all skills of a
    chosen ability**.
  - **3 — Wails from the Grave:** after dealing Sneak Attack damage, roll **half your Sneak Attack
    dice** against a second enemy within 9 m of the first. Uses per **long rest** = **Proficiency
    Bonus**.
  - **9 — Tokens of the Departed:** when a creature dies within 9 m, **reaction** to gain a **Soul
    Trinket**, granting **advantage on Constitution and Death saving throws**. Trinkets can be
    consumed to fuel extra Wails from the Grave.
  - **13 — Ghost Walk:** become **ethereal** — unaffected by harmful surfaces, **attacks against
    you have disadvantage**, for 10 minutes / 100 turns or until you end it. Once per long rest,
    or spend a Soul Trinket for another use.
  - **17 — Death's Friend:** Wails from the Grave also **rolls damage against the first creature**
    when you target the second (i.e. full Sneak Attack on both). You gain a Soul Trinket after a
    long rest if you have none.
- **Duo relevance:** the only Rogue subclass in the list that **converts single-target Sneak Attack
  into two-target damage**, which addresses the duo's actual problem — too many enemies, not
  enough turns. Whispers of the Dead is a short-rest, on-demand **all skills of one ability**,
  which is close to a cheat code when two characters must cover every check in the campaign. Ghost
  Walk is a genuine survival cooldown (disadvantage on all attacks against you) and Tokens of the
  Departed turns kills into Con-save advantage — concentration and hard-CC insurance. The Soul
  Trinket economy also **feeds off kills, not rests**, which suits Listo's expensive long rests.
  Note that the compat patch's author explicitly did not test level 17.

### Scout

- **Mod:** Book of Rogues (`19717`)
- **Mechanics:**
  - **3 — Skirmisher:** when an enemy **ends its turn within 2 m of you**, **reaction** to increase
    your movement speed by **half until the end of your next turn**, and you **do not provoke
    opportunity attacks**.
  - **3 — Survivalist:** **Expertise in Nature and Survival.**
  - **9 — Superior Mobility:** **+3 m movement speed.**
  - **13 — Ambush Master:** **+5 to Initiative**; additionally, the **first creature you hit in the
    first round** of combat becomes easier to hit — **attack rolls against it have advantage until
    the start of your next turn**.
  - **17 — Sudden Strike:** if you take the Attack Action, make **one additional attack as a Bonus
    Action**, and that second attack **can benefit from Sneak Attack damage even if you already
    used it this turn** — but **not against the same target**.
- **Duo relevance:** Ambush Master's advantage-marking is a **party-wide** buff, which is worth
  double in a two-person party where one mark covers half the team. It also stacks on top of
  Listo's d10 initiative, and note that Alert is now only **+Proficiency Bonus** (see
  `data/listo-10.2-feats.md`), so a flat **+5** is competitive with the feat and does not cost a
  feat slot. Sudden Strike at 17 is a **second Sneak Attack per turn** on a different target —
  combined with Cunning Strike that is two riders a turn. Survivalist's free Expertise is two
  more skills covered for nothing.

### Soulknife

- **Mod:** Book of Rogues (`19717`)
- **Mechanics:**
  - **3 — Psychic Blades:** manifest blades of psychic energy at the start of your turn in combat
    (they vanish at end of turn; summonable briefly out of combat). Thrown Psychic Blades deal
    **Psychic damage**, not weapon damage.
  - **3 — Psi-Bolstered Knack:** spend **Psionic Energy Dice** to improve skill checks. Implemented
    as a **toggle**, parked next to Metamagic on the hotbar — remember to switch it on and off.
  - **3 — Psychic Whispers:** gain **Detect Thoughts**.
  - **9 — Homing Strikes:** when you **miss** while wielding Psychic Blades, roll a Psionic Energy
    Die and add it to the attack roll; **the die is only spent if the attack then hits**.
  - **9 — Psychic Teleportation:** bonus action, spend a die to throw a Psychic Blade and
    **teleport to where it lands**.
  - **13 — Psychic Veil:** action, become **Invisible**. Once per long rest, or spend a Psionic
    Energy Die for more.
  - **17 — Rend Mind:** when you deal Sneak Attack damage with Psychic Blades, force a **Wisdom
    save (DC 8 + PB + Dex)** or **Stunned for 10 turns**, repeating the save at the end of each of
    its turns. Once per long rest, or spend **three** Psionic Energy Dice.
- **Mechanics not verified:** the **number and size of Psionic Energy Dice** and their recovery
  rate are not stated on the mod page. There is a **Restore Psionic Energy** action (given VFX in
  1.0.0.3), so recovery is an activated ability. `(unverified — check the character sheet)`
- **Duo relevance:** the most self-sufficient Rogue here — its weapon, its accuracy fix, its
  mobility and its invisibility all come from one resource, so it needs no gear and no ally.
  Homing Strikes is a **miss-insurance** mechanic, which matters disproportionately when one
  character's turn is a quarter of the party's whole round. Rend Mind is the only hard **stun** on
  any Rogue in the list. Downside: Psychic damage is one of the more commonly resisted types
  in the late game, and the dice economy is the thing this file could not verify.

---

### Seeker

- **Mod:** `(DTO) Otherworldy Archetypes` (`21822`)
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67 2026-06-17T17-15Z PYJWETtYB.zip` —
  **1.2.0.67, the current Nexus version**
- **Mechanics** (from the author's own documentation site, prizzels.github.io/DTO):
  - **Requirement on every casting feature: a free off-hand and at most Light Armour.**
  - **3 — Conduit of the Weave** (passive/reaction): when a levelled spell is cast within 18 m,
    **reaction** to siphon it for a **Sorcery Point**. Pool = **1 + Intelligence modifier**,
    replenished on a **long rest**.
  - **3 — Arcane Strike** (action, 1 SP, once per turn): a **Sneak Attack that deals Force damage
    even if you would not otherwise qualify** for Sneak Attack.
  - **3 — Auspicious Parry** (reaction, 1 SP): when about to be hit, **take 1 damage instead**.
  - **3 — Arcane Bolts** (action main-hand / **bonus action** off-hand, 1 SP each, 18 m): three
    bolts of **1d4+1 Force** each, and they **hit through Shield**. Dice step up at **7** and
    **13**.
  - **7 — Arcane Strike: Flicker** (2 SP): **teleport up to 9 m** to the target and Arcane Strike.
  - **7 — Arcane Strike: Decoy** (2 SP): Arcane Strike and gain a **Mirror Image (+3 AC)** until
    you are missed; up to **3** at once.
  - **9 — Spell Siphon** (reaction, 12 m, once per **short rest**): **interrupt a spell being cast**
    and absorb it for temporary Sorcery Points equal to your **Intelligence modifier**.
  - **13 — Brilliant Edge** (passive): add your **Intelligence modifier as Force damage** to weapon
    attacks, and your **Force damage pierces Resistance**.
  - **13 — Arcane Strike: Quicken** (3 SP): +3 m movement and an **additional attack for the next
    2 turns**.
  - **13 — Arcane Strike: Disrupt** (3 SP): on hit, target is **Disarmed**, **Silenced** until the
    end of its next turn, and **Stunned if Concentrating**.
  - **17 — Antimagic Shell** (bonus action, once per long rest): **immune to all magical damage and
    untargetable by status effects for 2 turns**.
- **Duo relevance:** the counterspell-shaped Rogue. **Auspicious Parry** is the best single
  survival reaction available to any Rogue in the list — with Lone Wolf's extra reaction you can
  parry and still Uncanny Dodge — and **losing either character usually ends the fight**, so a
  1-damage "no" button is worth more here than its cost suggests. **Spell Siphon** and
  **Disrupt** give a two-person party the enemy-caster answer it otherwise lacks. The costs are
  real: **Int-dependent** (Conduit pool, Spell Siphon, Brilliant Edge) on top of Dex, resource
  income that depends on **enemies casting spells**, and a **free off-hand plus light armour**
  restriction that rules out dual-wielding and shields.

---

## Feat anti-synergies

Cross-reference `data/listo-10.2-feats.md` for full feat text. Three interactions silently do
nothing or less than you expect on a Rogue.

- **Shield Master's Block vs Evasion.** Block is now a **passive** with the **same effect as Rogue
  Evasion, and it does not stack with it.** A Rogue past level 7 who takes Shield Master gets the
  +2 Dex-save bonus, Shield Blow and the flat −1 damage taken, but **Block is dead weight**. Rogue
  can't use shields without a dip anyway, so this mostly bites multiclass builds.
- **Thief's Apprentice vs Fast Hands.** Essential Feats' Thief's Apprentice grants a **bonus
  action after attacking from stealth or killing**, plus Cunning Action: Hide. It **does not
  stack** with Fast Hands. On a Thief the bonus-action half is entirely wasted; on any other Rogue
  it's a real gain, and the Cunning Action: Hide half is redundant with Rogue 2 regardless. Read
  it as a feat for **non-Thief** Rogues and for **non-Rogues** who want Rogue-shaped turns.
- **Alert is weaker than you remember.** Its initiative bonus is now **your Proficiency Bonus**,
  not +5, calibrated for Listo's **d10 + Dex** initiative. Scout's **Ambush Master (+5 at 13)** and
  Swashbuckler's **Rakish Audacity** now compete with the feat directly — don't buy both for the
  same effect.

And one **synergy** worth naming, since the docs call it out explicitly:

- **Dirty Fighting** (`14049`) — +1 Str or Dex, plus **Dirty Kick**: a bonus action for
  1d4 + unarmed modifier that knocks the target **Off-Balance** (next attack against them has
  **advantage**; they have disadvantage on Str and Dex saves). The docs name this as *the*
  reliable Sneak Attack setup for melee Rogues who don't have Swashbuckler's Rakish Audacity or
  Inquisitive's Insightful Fighting. It costs a bonus action, so it competes with Cunning Action —
  but Lone Wolf gives you a second bonus action, and Thief a third. **Enemy Fighters and Rogues
  use Dirty Fighting on you from Act 3.**

---

## Dip value

**Rogue 3 is the standard dip**: a subclass (any of the ten), **Cunning Action: Dash/Disengage/
Hide**, and **2d6 Sneak Attack**. It is **feat-neutral** — the Listo cadence pays a feat at class
level 3, so you collect the Rogue feat you would otherwise have collected elsewhere.

What the dip is actually worth, in order:

1. **Thief 3** — a second Bonus Action. On top of Lone Wolf's extra bonus action this is the
   largest raw action-economy purchase available for three levels in the whole list, and it
   applies to *anything*: off-hand attacks, item bonus actions, War Magic, Cunning Action: Dash
   for triple movement.
2. **Assassin 3** — Action + Bonus Action restored at the start of combat, guaranteed crits on
   Surprised targets, advantage on anything that hasn't acted. Best on a character that already
   wins initiative.
3. **Swashbuckler 3** — Sneak Attack without needing advantage or an adjacent ally, plus scaling
   initiative. The dip that works when there is no second melee body, which in a duo is often.
4. **Inquisitive 3** — Insightful Fighting as a repeatable Sneak Attack enabler for anyone with a
   finesse weapon.
5. **Seeker 3** — Arcane Strike is a Sneak Attack that ignores the Sneak Attack requirements, and
   Auspicious Parry is a survival reaction. Costs Int and a free off-hand.

**Rogue 5** extends the dip to **Uncanny Dodge + Cunning Strike**. Expensive, but Cunning Strike
is the only source in the class of turn-by-turn Prone/Poison/Disarm without spending an action.

**The Expertise argument is about Rogue 1, not the dip.** Only the **first** class grants saving
throw proficiencies, and only a first-class Rogue gets **4 skill proficiencies + 2 Expertise at
level 1**. Multiclassing *into* Rogue gives **light armour and one skill** — no Expertise bonus,
no saves. In a run where **two characters must cover every skill check in the campaign**, Rogue
as the level 1 class is one of the strongest skill packages available, and **Reliable Talent at
11** (minimum roll of 10 on any proficient skill) converts that coverage from "usually" to
"always". Pair it with **Slippery Mind at 15** — Dex + Int + Wis saves on one character — and the
back half of the class earns its levels defensively even when the damage falls off.

---

## Not present

Verified absent from the 10.2 list (TSV and manifest both checked):

- **`Second-Story Work Dexterity Jump` (`6331`)** — **the docs are wrong.** Docs page 4's Rogue
  section still advertises it, but the mod is **not in the TSV, not in the manifest, and never
  appears in the changelog**. Second-Story Work is **vanilla**: resistance to falling damage, not
  Dex-scaled jumping. Do not plan a Thief around Dexterity jump distance.
- **The UA6 Swashbuckler subclass** — mod `507` is titled "UA6 Cunning Strike and Swashbuckler",
  but Swashbuckler is a **separate optional download** (`Swashbuckler-507-1-5-17-….zip`) and
  Listo pulled **only** `Cunning Strike-507-1-6-1-….zip`. There is no **Swashbuckler\*** variant
  (Parrying Stance at 3 instead of 13) and no playtest-6 Swashbuckler. The Swashbuckler you can
  actually pick is the **Patch 8 vanilla** one.
- **`Steady Aim`** — split out of `507` onto its own mod page; that page is not in the list.
  Expansion's optional Steady Aim at level 3 is the only possible source, and whether Listo
  enables it is unverified.
- **Grim Surgeon, Misfortune Bringer, Debonaire** — standalone Rogue subclasses **explicitly
  removed** in the changelog ("REMOVED Grim Surgeon, Misfortune Bringer, Debonaire, Scout,
  Mastermind, and Inquisitive from Rogue") and replaced wholesale by Book of Rogues. Scout,
  Mastermind and Inquisitive came back inside the pack; **these three did not**.
- **Rogue Unleashed / Rogue Unchained / The Ruffian (Strength Rogue) / Justicar** — named in
  Goon's and wesslen's compatibility notes but **none are in the list**. Goon's Ruffian and
  Justicar support code is inert.
- **`(DTO) Codex of Might and Magic`** (Volume 2, which has its own Rogue section) — documented on
  the same DTO site as Seeker, **not in the list**. Ignore its Rogue content.
- **`Alternate Origin Subclasses - Shadowheart and Wyll` (`8960`)** is installed but contains
  **no Rogue content** — it only changes Shadowheart's default Cleric domain and Wyll's default
  Warlock patron.
- **No Rogue-specific gear entries** exist in `data/listo-10.2-equipment.md`; note only that
  **hand crossbow range is reduced** in Listo (they can still be dual wielded) and
  **Crossbow Expert is renamed Bow Expert**.

### Open questions

- **Uncanny Dodge implementation.** Book of Rogues turns it into a **reaction pop-up**; Goon's
  Rogue Overhaul turns it into an **Interrupt**. Both are installed. Load order decides; the
  manifest doesn't say. `(unverified)`
- **Compat patch version drift.** `20687` targets Book of Rogues **1.0.0.2**; Listo ships
  **1.0.0.3**, which restructured the level-3 progressions file. The patch's author also states he
  **did not test the level 17 features**. `(risk)`
- **Soulknife's Psionic Energy Dice** — count, die size and recovery rate not documented anywhere
  readable. `(unverified)`
- **Expansion's optional Steady Aim** at Rogue 3 — enabled or not in Listo's config.
  `(unverified)`
- **Cunning Strike early-unlock rings** in the tutorial Cartilaginous Chest — present in Listo's
  loot or not. `(unverified)`
