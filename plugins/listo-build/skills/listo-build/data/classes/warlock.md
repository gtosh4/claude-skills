# Listonomicon 10.2 — Warlock

Warlock is the default dip in this list because everything it gives you arrives in the first
two or three levels and then keeps scaling off **character** level. Warlock 1 is one of only
three classes that grant **Wisdom + Charisma** saves at level 1 (Cleric and Paladin are the
others), and it hands you Eldritch
Blast; Warlock 2 adds **Agonizing Blast**, at which point you own a ranged cantrip that gains
beams at character level 5, 10 and 17 no matter how few Warlock levels you ever take. Warlock 3
adds a pact boon and a **feat** (Listo's cadence is class levels 3/6/9/12/13/15/18, so a 3-level
dip is feat-neutral) — and it is the only class whose spell slots come back on a **short rest**,
which in a run where a long rest costs 120+ camp supplies is the resource cadence that matters.
Listo has not left the class alone: **Eldritch Blast is 1d8 per beam here, not 1d10**, Repelling
Blast now allows a Strength save, and Mizora's Rewards' Eldritch Blast riders were nerfed to
your spell save DC minus 2.

**Provenance.** Compiled 17 August 2026 against the bundled 10.2 snapshot. Every mod named was
confirmed in `listo-10.2-mods.tsv`; every file variant was confirmed in
`listo-10.2-manifest.json`. Vanilla baselines are from bg3.wiki (Patch 8). Listo's own deltas
are from `data/docs/5-ChangeLog.md`. Anything not read is marked `(unverified)`.

Cross-references, not restated here: feats in `data/listo-10.2-feats.md`, gear in
`data/listo-10.2-equipment.md`, dip/save/stat arithmetic in `references/listo-rules.md`.

---

## At a glance

| | |
|---|---|
| **Primary ability** | Charisma (spell attacks, save DC, Agonizing Blast damage) |
| **Secondary** | Constitution (concentration, HP), Dexterity (AC) |
| **Saves granted at level 1** | **Wisdom + Charisma** — only from the level 1 class; a respec that re-picks first class silently loses them |
| **Hit points** | 8 + Con at level 1, 5 + Con on level up |
| **Equipment proficiencies** | Simple weapons, Light armour. **Identical on the multiclass node** — a Warlock dip returns no armour feat |
| **Skills (choose 2, level 1 only)** | Arcana, Deception, History, Intimidation, Investigation, Nature, Religion |
| **Resource cadence** | **Pact slots refresh on a SHORT rest.** Very few slots, always cast at the highest level you have. **1** slot at Warlock 1, **2** from Warlock 2, **3** from Warlock 11. Two short rests per long rest in Listo |
| **Slot level** | Always upcast to max: 1st at Warlock 1–2, **2nd at 3–4**, **3rd at 5–6**, 4th at 7–8, 5th at 9+ |
| **Spells** | Always prepared, few known. Cantrips 2 / 3 at WL4 / 4 at WL10 |
| **Key breakpoints** | **1** (saves + EB + patron), **2** (Agonizing Blast), **3** (pact boon + 2nd-level slots + feat), **5** (3rd-level slots, 3rd invocation, Deepened Pact), 11 (Mystic Arcanum 6th), 13/15/17 (Arcanum 7th/8th/9th), 20 (Eldritch Master) |
| **Dip value** | **Highest in the list.** See the section below |
| **Not touched by Goon's overhauls** | There is no `Goon's Warlock Overhaul` in the TSV — Barbarian, Bard, Cleric, Paladin, Rogue, Wizard and Slayer have one; Warlock does not |

### Listo's own changes to the class

From `5-ChangeLog.md` v10.0 (item 38) — **these are current in 10.2**:

- **Eldritch Blast base damage reduced to 1d8 per beam, from 1d10.**
- **Repelling Blast now allows a Strength saving throw** (vanilla is automatic).

Older, still in force:

- **Mizora's Rewards blast riders are nerfed.** v7.0.8 set their DC to `spell save DC − 4`;
  v7.0.9 walked that back to **`spell save DC − 2`**, except **Deteriorating Blast** and
  **Bewitching Blast** at **`− 3`**. **Lance of Lethargy gained a Constitution save.** Effects
  that lasted longer than 3 turns were cut to 2–3.
- **Eldritch Glaive** (Mizora's Rewards) requires you to already have a source of **Extra
  Attack** before its bonus-action glaive attack is available.
- Enemy warlocks are a distinct CX category with GOO/Archfey/Fiend variants, and enemies that
  had Repelling Blast were given **Grasp of Hadar** instead.
- **Spell Sniper** is reworked (advantage on the damage die for attack-roll spells) but
  deliberately **only applies to the first hit** so it does not run away with Eldritch Blast.
  Full text in `listo-10.2-feats.md`.

### Levels 13–20

Supplied by **Expansion Level 13-20 (Configurable)** (`279`), archive
`Expansion-279-1-7-3-6-1780876532.zip` (**v1.7.3.6**).

> **TSV/manifest naming trap:** the manifest's cached metadata for `279` still reads
> *"Expansion (Bladesinger Only)", v0.0.26*, and that stale name is what landed in the TSV.
> The **archive** Listo actually pulls is the full v1.7.3.6 Expansion mod (237 MB). Do not
> conclude from the TSV that Listo has no 13–20 progression.

Warlock gets: **Mystic Arcanum at 13, 15 and 17** (7th, 8th, 9th level spells),
**optional Eldritch Invocations at 15 and 18**, and **Eldritch Master at 20**.
The extra invocations Expansion adds at 15/18 are **Chains of Carceri, Master of Myriad Forms,
Shroud of Shadow, Visions of Distant Realms, Witch Sight and Eldritch Sight**.

> Expansion **v1.7.3.9** (newer than the archive Listo pulled) *removed* Eldritch Sight, Master
> of Myriad Forms and Visions of Distant Realms, handing them to 5e Spells. **In Listo 10.2 all
> six are still present**, because Listo is on 1.7.3.6. The Nexus page describes the newer
> behaviour — discount it.

Patron 14th-level features from Expansion: **Fiend → Hurl Through Hell**, **Great Old One →
Create Thrall**, **Hexblade → Master of Hexes**. **Archfey is not listed** — it appears to get
no 14th-level feature from Expansion `(unverified whether another mod fills the gap)`.

### Eldritch Blast beam scaling — correct this number

`references/listo-rules.md` says beams at character **5, 11 and 17**. That is the tabletop
progression. What is actually verifiable:

- **2 beams at character level 5** — bg3.wiki, vanilla.
- **3 beams at character level 10** — bg3.wiki, vanilla. **BG3 uses 10, not 11.**
- **4 beams at character level 17** — Expansion's changelog contains *"Fixed Eldritch Blast
  being able to fire 5 beams at 17th level"* and *"Fixed Eldritch Blast at 17th being limited to
  targeting a single creature with each beam"*, so Expansion is the source of the fourth beam.
- No mod in the list was found that moves the third beam from 10 to 11.

**Treat the progression as 5 / 10 / 17.** `(The 10-vs-11 question is worth one glance at a
level-10 sheet in game; everything else here is confirmed.)` The load-bearing claim is
unaffected: **beams key off character level, so two Warlock levels buy the whole engine.**

---

## Dip value — level by level

Rows are cumulative. A dip of size N gives you every row up to N.

### Warlock 1

- **Wisdom + Charisma saving throw proficiencies.** Only the level 1 class grants saves. This is
  the reason to put Warlock first rather than bolt it on. Wisdom is the highest-value save in
  the game (Hold, Dominate, Fear, Hypnotic Pattern); Charisma covers Banishment.
- **Eldritch Blast** (and one other cantrip): 1d8 Force, 18 m, attack roll, scales on character
  level.
- 2 spells known, always prepared. **1 pact slot**, refreshed on a short rest.
- **Patron features** — the level 1 subclass package (see Patrons below). Choosing the patron
  here is free; you are not obliged to ever take Warlock 2.
- Light armour + simple weapons. **The multiclass node grants exactly the same proficiencies**,
  so unlike Fighter 1 or Artificer 1 this does **not** free up an armour feat.
- **Charisma trap:** Warlock is one of seven classes granting a Charisma save at level 1. Giving
  Lone Wolf's +4 to Charisma alongside Warlock 1 wastes one of the two grants. See
  `listo-rules.md`.

### Warlock 2

- **Two Eldritch Invocations.** **Agonizing Blast** is the one that makes the dip: add your
  Charisma modifier to *each beam* of Eldritch Blast. At 4 beams and Cha 22 that is +24 damage
  per cast on top of 4d8, from two class levels.
- Second invocation is free choice. Strong non-slot picks: **Devil's Sight** (see through
  magical darkness to 24 m — pairs with the Darkness spell), **Armour of Shadows** (Mage Armour
  at will, relevant if you have no armour proficiency to spare), **Repelling Blast** (now with
  a Strength save), **Beguiling Influence** (Deception + Persuasion proficiency),
  **Fiendish Vigour** (False Life at will).
- 2nd pact slot. 3 spells known.
- **Cost:** stopping at 2 breaks the 3-level feat block. A 1- or 2-level dip costs a feat
  outright.

### Warlock 3

- **Pact boon** — Blade, Chain, Tome, or **Shroud** (mod `6001`).
- **Pact slots become 2nd level.** Everything you cast is upcast to 2nd automatically.
- **A feat**, because Listo's cadence is class level 3. **This makes Warlock 3 feat-neutral and
  the natural dip size.**
- **Pact of the Chain is the duo pick.** It grants Find Familiar with Imp and Quasit options,
  and in a two-player Lone Wolf run a third body on the initiative order is worth more than the
  familiar's stat block suggests. With `18881` installed the familiars are substantially
  rebuilt (below).
- 4 spells known, now up to 2nd level.

### Warlock 5

- **Pact slots become 3rd level**, still on the short-rest clock. Two 3rd-level slots that come
  back twice per long rest is more raw casting per adventuring day than a level 5 full caster
  gets from its long-rest slots.
- **Third Eldritch Invocation.** Level-5 invocations unlock: Mire the Mind, Sign of Ill Omen,
  and — with the invocation mods — Cloak of Flies, Tomb of Levistus, Maddening Hex, Undying
  Servitude, Investment of the Chain Master, Gift of the Ever-Living Ones, Ascendant Step,
  Eldritch Glaive, Eldritch Smite, Spider Shape, Thieves' Bane.
- **Deepened Pact:** Blade → **Extra Attack** with the pact weapon; Chain → **familiar gains
  Extra Attack**; Tome → Animate Dead / Haste / *(list truncated on the wiki page)*;
  Shroud → Eldritch Shroud becomes continuously active until you are hit.
- Cantrips 3 (from Warlock 4), 6 spells known.
- **Cost:** five levels off the main class, and it breaks the multiple-of-three feat block
  unless the main class is also sitting on a multiple of 3.

### Beyond 5, if Warlock is the main class

11 → **Mystic Arcanum** (a free 6th-level spell, once per long rest) and a **third pact slot**.
13 / 15 / 17 → Arcanum 7th / 8th / 9th via Expansion. 20 → **Eldritch Master**
`(text of Listo's implementation unverified; 5e's version restores all pact slots once per long
rest)`.

---

## Patrons (subclasses)

Six are available. Four vanilla, two modded.

### The Archfey
- **Mod:** vanilla (Larian)
- **Mechanics:** Level 1 **Fey Presence**; expanded spells at 1/3/5/7/9 (Faerie Fire, Sleep;
  Calm Emotions, Phantasmal Force; …). Level 6 **Misty Escape**. Level 10 **Beguiling
  Defences**.
- **Duo relevance:** Fey Presence is an AoE charm/fear on a short rest — real crowd control from
  a level 1 dip, and crowd control is how a two-person party survives being outnumbered.

### The Fiend
- **Mod:** vanilla (Larian)
- **Mechanics:** Level 1 **Dark One's Blessing** (temp HP on kill); expanded spells from 1
  (Burning Hands, Command). Level 6 **Dark One's Own Luck**. Level 10 **Fiendish Resilience**.
  Level 14 **Hurl Through Hell** (Expansion `279`).
- **Duo relevance:** the best *defensive* level 1 patron. Dark One's Own Luck at 6 is a
  free re-roll; Fiendish Resilience is a rest-scaled resistance. Losing a character usually ends
  the fight, so survivability on the Charisma caster is worth more than on a four-person team.

### The Great Old One
- **Mod:** vanilla (Larian)
- **Mechanics:** Level 1 **Mortal Reminder** (crit → fear); expanded spells from 1 (Dissonant
  Whispers, Tasha's Hideous Laughter). Level 6 **Entropic Ward**. Level 10 **Thought Shield:
  Psychic Resistance / Psychic Reflection**. Level 14 **Create Thrall** (Expansion `279`).
- **Duo relevance:** Mortal Reminder triggers on crits, and Eldritch Blast makes several attack
  rolls per turn, so it fires far more often on a blaster than the description implies.

### The Hexblade
- **Mod:** vanilla (Larian, **Patch 8**) — *not* a mod, despite what old build guides assume
- **Mechanics:** Level 1 **Hex Warrior**, **Bind Hexed Weapon**, **Hexblade's Curse**; expanded
  spells from 1 (Shield, Wrathful Smite). Level 6 **Accursed Spectre**. Level 10 **Armour of
  Hexes**. Level 14 **Master of Hexes** (Expansion `279`).
- **Duo relevance:** the only patron that makes Warlock 1 a *melee* dip — Hex Warrior puts
  Charisma on a weapon at level 1, without waiting for Pact of the Blade at 3. Note that
  Mizora's Rewards modifies **Hexblade's Pact** alongside Pact of the Blade (below), and that
  Hexblade's Curse counts as a "curse" for **Maddening Hex** / **Relentless Hex**.
- Listo once changed Wyll's default subclass to Hexblade and **reverted it** (changelog v9.0.3,
  struck through). The manifest still pulls `AOS - Wyll - Hexblade 1.0.0-8960-...`, so the
  download exists; whether the .pak is enabled in the shipped profile is `(unverified)`.

### The Celestial
- **Mod:** The Celestial - Warlock Subclass (`11561`)
- **File pulled:** `The Celestial 1.3.0-11561-1-3-0-1764640280.zip` — v1.3.0, the current
  version
- **Mechanics** (author states "rules as written" from Xanathar's, progression to 20):
  - **Level 1 — Bonus Cantrips:** **Light** and **Sacred Flame**, free, not counted against
    cantrips known. *A free saving-throw radiant cantrip on a Warlock 1 dip — the answer to
    high-AC targets that Eldritch Blast's attack roll struggles with.*
  - **Level 1 — Healing Light:** a pool of **1 + Warlock level d6**. **Bonus action**, heal one
    creature within 60 ft, spending up to **Charisma modifier** dice at once. **Pool refreshes
    on a long rest** (not short).
  - **Level 1 — Expanded spell list**, added as you level: **Cure Wounds, Guiding Bolt** (WL1);
    Flaming Sphere, Lesser Restoration (WL3); Daylight, **Revivify** (WL5); Guardian of Faith,
    Wall of Fire (WL7); Flame Strike, Greater Restoration (WL9).
  - **Level 6 — Radiant Soul:** resistance to Radiant; add **Charisma modifier** to one radiant
    or fire damage roll per spell. Implemented as an interrupt, once per spell.
  - **Level 10 — Celestial Resistance:** after a **short or long** rest, temp HP = Warlock level
    + Cha mod for you, and half Warlock level + Cha mod for up to five creatures. Out of combat
    only.
  - **Level 14 — Searing Vengeance:** once per long rest, triggers **on being downed** (the
    author's deviation from RAW), heal to half max HP, 2d8 + Cha radiant to enemies within 30 ft
    and blind them. Toggleable.
- **Duo relevance:** **one of only three Charisma casters with healing** (with Bard and Favored
  Soul Sorcerer). In a duo where losing either character ends the fight, a **bonus-action** heal
  that does not spend a spell slot is the single most valuable thing on this list — it stacks
  with an Action *and* Lone Wolf's extra Action in the same turn. **Revivify at Warlock 5** on a
  short-rest slot is the other half of that argument. Caveat: Healing Light is on the **long
  rest** clock, so it is a per-day budget, not a per-fight one.
- **Dependencies, all present:** Compatibility Framework (`1933`), Community Library (`1333`),
  Spells Extra - DND 5E Library (`11291`), and the author-recommended **Warlock Spell List
  Fixer** (`11239`).

### The Psyker
- **Mod:** (DTO) Otherworldy Archetypes (`21822`) — one of 12 subclasses in the pack
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67 2026-06-17T17-15Z PYJWETtYB.zip`
- **Added:** v9.0.3, changelog item 118 — *"ADDED (for testing) Otherworldly Archetypes."*
  **The "for testing" wording is the author's; treat this patron as less settled than the rest.**
- **Mechanics** (from the author's own reference site, `prizzels.github.io/DTO/`):
  - **Level 1 — Warp Wielder** (passive toggle): Eldritch Blast damage applies **Warp** for 2
    turns. Further blasts or detonations reduce the remaining duration by 1.
  - **Warp (status):** when it ends it **detonates for 1d10 Force in a 3 m radius**, +1d10 at
    **levels 5, 11 and 17**.
  - **Level 1 — Perils of the Warp** (passive): each Warped blast or detonation **reduces your
    maximum hit points by 1d4 per turn of remaining duration** (1d6/1d8/1d10 at 5/11/17), and
    exposes you to random consequences at the start of each turn.
  - **Level 1** also grants **Eldritch Blast** as an additional spell known.
  - **Level 6 — Soul Rupture:** a killing blast reduces Perils duration by 2.
  - **Level 10 — Gellar's Field:** bonus action, **once per short rest** — negates Perils and
    blocks its return for 2 turns; Psychic resistance and advantage on mental saves while up.
    Free if it triggers in response to Perils.
  - **Level 14 — Chaos Rift:** action, 5th-level, 18 m range, 6 m radius — Warps all foes and
    can inflict Burning, Banished, Paralyzed, Frozen, Force Vulnerability, Confusion, Phantasmal
    Killer, Knockback, Frighten.
- **Duo relevance:** **avoid as a dip.** The max-HP drain is self-inflicted and scales with
  character level, the mitigation is a level 10 feature, and in a two-person party there is no
  third body to cover a caster who is bleeding max HP. As a main class it is an AoE blaster, but
  it trades exactly the resource a duo cannot spare.
- **Interaction not verified:** whether Warp detonations count as "Eldritch Blast" for
  Agonizing Blast or for Mizora's `IsEldritchBlastAlike()` rider system. `(unverified)`

---

## Pact boons

Chosen at Warlock 3; upgraded by **Deepened Pact** at Warlock 5.

| Boon | Source | Level 3 | Deepened Pact (WL5) |
|---|---|---|---|
| **Pact of the Blade** | vanilla | Summon or Bind a weapon; it uses your **Spellcasting Ability** instead of Str/Dex | **Extra Attack** with the pact weapon |
| **Pact of the Chain** | vanilla (+ `18881`) | **Find Familiar** with Imp and Quasit options | Familiar gains **Extra Attack** |
| **Pact of the Tome** | vanilla | Book of Shadows: **Guidance, Vicious Mockery, Thorn Whip** | Animate Dead, Haste, … `(full list truncated on the wiki page)` |
| **Pact of the Shroud** | **`6001`** | **Eldritch Shroud** reaction | Shroud becomes continuously active until hit |

### Pact of the Shroud (`6001`)
- **File pulled:** `Pact of the Shroud-6001-1-2-0-0-1746418262.zip` — v1.2.0.0, current
- **Eldritch Shroud** (reaction, when attacked): base AC becomes **10 + Cha mod + Proficiency
  Bonus** until the start of your next turn. Dex, equipment, spells and class features stack
  **on top**. Uses = **Proficiency Bonus**, and **all uses refresh on a short rest**, same clock
  as pact slots.
- Does **not** stack with other base-AC replacements (Unarmoured Defence, Mage Armour, Barkskin)
  — the highest base applies.
- **Deepened Pact at WL5:** the shroud is **always on, in and out of combat, until you are hit**;
  then it reverts to a reaction until a short rest.
- **Three invocations** ship with it. Engine limits mean **you can take them without the boon**,
  in which case you get one Eldritch Shroud charge usable only to fuel them:
  - **Shroud of Safe Passage:** no armour and no shield → **Disengage or Hide as a bonus
    action**.
  - **Veil of Shadows** (7th): using Eldritch Shroud imposes **disadvantage on attacks against
    you**; and you can spend a bonus action + a Shroud charge to **teleport between shadows**,
    arriving **invisible** until your next turn (no armour).
  - **Shroud the Soul** (12th): no armour or shield → spend a Shroud charge as a **Reaction to
    turn a failed saving throw into a success**, once per combat.
- **Duo relevance:** at Cha 22 and PB +6 that is base AC 26 before Dex or items, on a
  short-rest-refreshing reaction — but it costs the **Reaction**, which Lone Wolf already gives
  you a second of. The armour/shield restriction is the real cost. **Shroud the Soul is the
  headline for a duo**: a guaranteed save once per combat is a hard counter to the single
  Hold/Dominate that would otherwise end the run.

### DnD 5R Pact of the Chain (`18881`)
- **File pulled:** `DnD 5R Pact of the Chain-18881-3-3-1764123813.rar` — v3.3, current
- **Command Familiar** (Pact of the Chain only): trade **one of your attacks** to grant the
  familiar an **extra attack that costs the familiar's Reaction** rather than its normal cost.
  With Extra Attack you lose one attack and keep the rest; without it, it consumes your Action.
- **Imp and Quasit rebuilt to PHB2024:** now **level 2**, **12 m movement** (was 9), **Superior
  Darkvision**, **Magic Resistance** (advantage on saves vs spells and magical effects),
  **Tiny** (fits through holes). Imp **21 HP**, damage **1d6+3 piercing + 2d6 poison**,
  proficient in Stealth/Deception/Insight. Quasit **25 HP**, guaranteed **Poisoned for 1 turn**
  on hit, proficient in Stealth, **immune to Poison damage** (was only the condition).
  **Resistance to non-magical physical damage was removed** in exchange for the HP.
- **Two new familiars:** **Skeleton** (PHB2024 statblock, level 2, shortsword + shortbow;
  Undead — vulnerable to Bludgeoning, immune to Poison/Poisoned/Exhaustion/Bleeding/Dazed/
  Suffocating, **cannot be healed by normal means**) and **Sphinx of Wonder** (flies, Radiant
  Claws, Tiny).
- **All Chain familiars gain Help, Throw and Improvised Weapon actions.**
- Author-declared compatibility with **Mizora's Rewards** and **Invocations Expanded** (load
  those first).
- **Duo relevance:** this is the mod that makes the Warlock 3 dip a **party-size** decision
  rather than a damage decision. **Help** on every familiar means a third body that can hand
  either player advantage every round without spending a player action. Magic Resistance plus
  doubled HP means the familiar survives long enough to matter, and **Command Familiar** turns
  a martial's spare attack into a familiar attack. At Warlock 5 the familiar gets Extra Attack
  on top.

---

## Invocations

Base game gives you 2 at Warlock 2, then +1 each at 5, 7, 9 and 12 (six total by 12), plus
Expansion's optional picks at 15 and 18. Three mods add to the pool, and they are explicitly
compatible with each other.

### Invocations Expanded — Patch 8 Update (`15872`)
**File pulled:** `Invocations Expanded 1.7-15872-1-7-1775654229.zip`. A community update of
WinterBrick's original; the page's notes describe up to v1.5 while the archive is 1.7.

> The mod ships **two variants — "Normal" (leveled progression) and "Fully Unlocked" (all
> invocations from level 2)**. Which one Listo enables is **`(unverified)`** — the archive is a
> single zip and the manifest does not disambiguate. Assume **Normal** unless a sheet says
> otherwise.

Adds (level prerequisite in brackets):

- **[1] Eldritch Spear** — Eldritch Blast range ×1.5 *(tooltip does not update)*
- **[1] Eldritch Mind** — advantage on Con saves for concentration
- **[1] Grasp of Hadar** — Eldritch Blast pulls the target 15 ft toward you
- **[1] Lance of Lethargy** — Eldritch Blast reduces movement by 10 ft *(Listo added a Con save)*
- **[1] Eldritch Smite** — spend pact slots for extra damage with pact weapons
- **[1] Improved Pact Weapon** — scaling enchantment (**+1 at 1–6, +2 at 7–11, +3 at 12**) and
  ranged pact weapons
- **[1] Investment of the Chain Master** — familiar gets temp HP = Warlock level, uses **your
  spell save DC**, 60 ft fly speed, and you can Reaction it damage resistance
- **[1] Gift of the Ever Living Ones** — healing on you is **maximised** while your Chain
  familiar is within 60 ft
- **[5] Ascendant Step** — Fly once per long rest, no slot
- **[5] Undying Servitude** — cast Animate Dead with a pact slot
- **[5] Cloak of Flies** — bonus-action damage aura, once per short rest
- **[5] Tomb of Levistus** — reaction for temp HP, incapacitated until end of next turn, once
  per short rest
- **[5] Maddening Hex** — bonus action, detonate a Hex/Curse for damage in an area
- **[7] Relentless Hex** — bonus action, teleport in front of a Hex'd/Cursed target
- **[7] Ghostly Gaze** — Darkvision + See Invisible for 10 min, once per short rest
- **[7] Trickster's Escape** — Freedom of Movement once per short rest, no slot
- **[7] Gift of the Protectors** — once per long rest, drop to 1 HP instead of 0
- **[12] Chains of Carceri** — Hold Monster once per short rest, no slot
- **[12] Shroud of Shadow** — Invisibility once per short rest, no slot
- Fixes **Mire the Mind**, **Sign of Ill Omen** and **Lifedrinker** (the last now works with
  ranged weapons), and broadens base **Pact of the Blade**'s summonable weapon types.
- **Known issue:** Grasp of Hadar and Repelling Blast can both be toggled on; the one selected
  last wins. Keep one active.

### Mizora's Rewards — More Warlock Invocations (`17046`)
**File pulled:** `Mixora's Rewards-17046-1-0-0-10-1758856875.zip` (the typo is in the archive
name). **31 new invocations**, 13 from 5e and 18 adapted from 3e, plus one feat.

> **Read Listo's nerfs above before quoting any of this.** Save DCs on the blast riders are
> `your spell save DC − 2` (`− 3` for Deteriorating and Bewitching), durations capped at 2–3
> turns, and Eldritch Glaive's bonus attack requires an existing Extra Attack source.

Highlights:

- **Elemental Blast [2]** — unlocks **Brimstone (fire)**, **Hellrime (ice)** and **Vitriolic
  (acid)** Eldritch Blast variants that **fully benefit from Agonizing Blast, Eldritch Spear
  etc.** This is the damage-type flexibility answer to a resistant enemy.
- **Eldritch Cone / Eldritch Line [9]** — AoE Eldritch Blast, 9 m cone or 18 m line, **1d10 per
  beam you would normally fire**, Dex save for half, still benefits from blast enhancements.
- **Eldritch Doom [12]** — once per long rest, blasts explode for their damage in 6 m.
- **Eldritch Glaive [5]** — a Force glaive whose attacks **count as Eldritch Blast**; bonus
  action extra attack **(Listo: requires an existing Extra Attack source)**. Needs Blade or
  Hexblade.
- **Rider blasts [2]:** Beshadowed (darkness cloud), Deteriorating (physical vulnerability),
  Frightful (Wis save → Frightened 2), Sickening (Con save → Poisoned 2), Hammer (auto-crit vs
  objects/inorganic); **[7]** Bewitching (Wis save → Confused); **[9]** Enervating Shadow (Str
  drain vs obscured targets).
- **Investment of the Chain Master [5]** — this mod's version: familiar flies, uses **your**
  Proficiency Bonus, **+HP = level × Cha mod**, unarmed attacks count as magical, bonus action
  to give it an extra attack, Reaction to grant it resistance.
- **Gift of the Ever-Living Ones [5]**, **Eldritch Smite [5]** (explicitly **stacks with Divine
  Smite** if one is an action and the other an interrupt), **Maddening Hex [5]**,
  **Relentless Hex [7]**, **Trickster's Escape [7]**, **Gift of the Protectors [9]**,
  **Aspect of the Moon [2]** (Tome), **Cloak of Flies [2]**, **Eldritch Mind [2]**,
  **Grasp of Hadar [2]**, **Lance of Lethargy [2]**, **Dragon Ward [2]**, **Leaps and Bounds
  [2]** (Acrobatics + Athletics proficiency), **Spider Shape [5]**, **Thieves' Bane [5]**,
  **Voidsense [7]**, **Baleful Plague [9]**.
- **Modifies vanilla:** **Pact of the Blade** and **Hexblade's Pact** behave like Eldritch
  Knight's Weapon Bond (throwable pact weapons); Agonizing Blast, Repelling Blast and Eldritch
  Spear are rewired to `IsEldritchBlastAlike()` so they apply to every blast variant.
- **Overwrites `Projectile_EldritchBlast`** to implement Grasp of Hadar — the author warns that
  other mods altering Eldritch Blast may not be fully compatible. Listo also alters Eldritch
  Blast (1d8 base). `(Whether Listo's 1d8 applies to Mizora's elemental variants is
  unverified.)`
- **It also adds a feat named "Eldritch Adept"** granting any one **2nd-level** invocation. See
  the conflict note below.

### Warlock Spell List Fixer (`11239`)
**File pulled:** `Warlock Spell List Fixer-11239-1-00-06-1777306046.zip`. Not an invocation mod
— it sweeps modded spells (5e Spells `125`, Valkrana's, Xara's) into **modded warlock
subclasses' spell lists**, which they otherwise miss because of how Larian handles warlock spell
lists. **This is what makes The Celestial and The Psyker see the list's expanded spell pool.**
Vanilla patrons already get them. Load near the bottom.

### Eldritch Adept — two mods claim this feat name

`listo-10.2-feats.md` documents **Essential Feats' (`5623`) Eldritch Adept**: learn one Eldritch
Invocation (any that doesn't require a Warlock spell slot), **+1 INT/WIS/CHA**, and **can be
taken multiple times**. **Mizora's Rewards also adds an "Eldritch Adept"** limited to one
**2nd-level** invocation with no ability bonus. Which one wins in Listo's load order is
`(unverified)` — but the feats file is the compiled reference and describes the Essential Feats
version, so plan against that and expect the 2nd-level restriction to be the pessimistic case.

**Why this matters:** a non-Warlock can buy **Agonizing Blast** (a 2nd-level invocation, no slot
required) with a feat — but Eldritch Blast itself comes from **Magic Initiate: Warlock** or
**Spell Sniper**, not from Eldritch Adept. A Sorcerer or Bard taking Magic Initiate: Warlock
plus Eldritch Adept gets the blast engine with **zero** Warlock levels and **no** Wis/Cha saves.
Compare that against Warlock 2 (which costs a feat) or Warlock 3 (which does not).

---

## Not present

**Purged in v9.0.3** (changelog item 57: *"REMOVED The Sorcerer King, The Undead, The
Fathooomless, The Genie, and The Star patrons from Warlocks"*). None of these appear in
`listo-10.2-mods.tsv`. **Do not recommend them:**

- **The Sorcerer King** — added v7.0.11, removed v9.0.3
- **The Undead** — added v4.x, removed v9.0.3
- **The Fathomless** — added v5.1, removed v9.0.3 (its Dawn's-Water spell-list patch went too)
- **The Genie** — added v5.1, removed v9.0.3
- **The Star** — added v6.2, removed v9.0.3

Also gone, from earlier releases:

- **The Archmage Patron** — added v7.2, removed v8.0.1
- **Otherworldy Boons** (mod.io) — added, then **removed** (changelog: *"REMOVED Otherworldy
  Boons (Mod.io)"*); not in the TSV
- **Pact and Power** (Warlock gear mod) — added in an early release, not in the 10.2 TSV
- **True Darkness** — not in the 10.2 TSV, so the tabletop Darkness-cheese interaction it
  enabled is **not** available; plan Devil's Sight + Darkness against vanilla Darkness rules
- **Intelligent Warlock** — was an optional mod in an older release; not in the 10.2 TSV
- **Pacts as Invocations / OneDnD Pact of the Blade** — recommended by `18881`'s author, **not
  in the list**. Pact boons remain a **one-time choice at Warlock 3**, not invocation picks
- **Eldritch Blast Overhaul** — Mizora's Rewards declares compatibility with it; **not in the
  list**
- **Hexblade as a mod** — there is no Hexblade patron mod in the TSV because **Hexblade is
  vanilla in Patch 8**. `Alternate Origin Subclasses` (`8960`) lists Celestial, Dread Overlord,
  First Vampire, Undead and Undying Light as *modded* patron options for Wyll; **only The
  Celestial exists in Listo**, so the rest of that list is inert

**Not a Warlock mod, despite the name:** `If Fate Chose Differently - Wyll Pact Points Overhaul`
(`22731`, archive `If Fate Chose Differently - Wyll Pact Overhaul-22731-1-0-0-9-...`) is a
**narrative** mod — dialogue, a Shadowheart-style approval-points system, and overhauled Act 2/3
scenes around Wyll breaking his pact. It changes **no** class mechanics. Also
`Hexcraft` (`10196`) is a **Wizard** subclass, and `Eldritch Domain` (`15357`) is a **Cleric**
subclass — neither is a Warlock option.
