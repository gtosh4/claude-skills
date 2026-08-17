# Listonomicon 10.2 — Monk

**Lead with this: the classic Tavern Brawler Monk does not exist in Listo.** Tavern Brawler no
longer grants +1 STR/CON and no longer adds the Strength modifier a second time — it adds only
**(Proficiency Bonus − 1)** to unarmed/thrown/improvised attack *and* damage rolls
(`data/listo-10.2-feats.md`). Elixirs of Giant's Strength are **+STR items, not set-to-N
potions** (`data/listo-10.2-equipment.md`), so "dump STR, drink, punch" is dead twice over. What
replaces it is a **Wisdom-forward Monk**: `Monk 5e Adjustments` (`1411`) moves Stunning Strike
and Open Hand Technique off the Maneuver DC (10 + STR/DEX) and onto the **Ki Save DC
(8 + Proficiency Bonus + WIS)**, so Wisdom now drives AC, save DCs, and several subclasses'
scaling at once. Listo also ships **eleven** Ways, and `Warrior of the Elements` (`18406`)
quietly rewrites the **base class** for every Monk: Martial Arts starts at **1d6**, not 1d4.

```bash
S=~/.claude/skills/listo-build     # or the plugin path

grep -i -A12 "^### Way of the Kensei" "$S/data/classes/monk.md"   # one Way
grep -i "short rest" "$S/data/classes/monk.md"                    # resource cadence
grep -i -A6 "^## Not present" "$S/data/classes/monk.md"           # what's gone
```

**Provenance.** Compiled 17 August 2026 against the bundled 10.2 snapshot. Every mod named here
was confirmed present in `listo-10.2-mods.tsv` by ModID, and the archive actually pulled was
checked in `listo-10.2-manifest.json`. Subclass mechanics come from the mod authors' own
implementation write-ups (Nexus articles for `15907`, the DTO site for `21822`), which describe
each mod's **current** version — where Listo pulled an older archive the gap is stated. Vanilla
baselines come from bg3.wiki. Anything not read directly is marked `(unverified)`.

---

## At a glance

| | |
|---|---|
| **Primary ability** | **Wisdom** first in Listo, then DEX (or STR). WIS drives Unarmoured Defence AC *and* the Ki Save DC that Stunning Strike / Open Hand Technique now use. |
| **Saving throws at level 1** | **Strength + Dexterity** — only granted if Monk is your **level 1** class. |
| **Proficiencies** | Simple weapons, Shortswords. No armour, no shields (exception: **Way of the Friar** grants shield proficiency and lets you keep Unarmoured Defence with one equipped). Skills: choose 2 of History, Insight, Religion, Acrobatics, Stealth, Athletics. |
| **Resource** | **Ki Points**, **recharged on a short rest**. BG3 grants Ki = monk level + 1 (2 at L1 → 13 at L12; L13–20 values `(unverified)`). |
| **Martial Arts die** | **1d6 at 1, 1d8 at 5, 1d10 at 11, 1d12 at 17** — PHB2024 scaling, imposed on *all* Monks by `Warrior of the Elements` (`18406`). Vanilla was 1d4 / 1d6 (L4) / 1d8 (L9). |
| **Feat levels** | **3, 6, 9, 12, 15, 18** (class level), from `Universal Feat Every X Level(s)` — see `data/listo-10.2-feats.md`. Not the vanilla 4/8/12. |
| **Breakpoints** | **1** Unarmoured Defence + Martial Arts + Flurry of Blows · **2** Unarmoured Movement, Patient Defence, Step of the Wind, **Uncanny Metabolism** (Listo addition) · **3** subclass + Deflect Missiles · **5** Extra Attack + Stunning Strike · **6** Ki-Empowered Strikes (unarmed counts as magical) + subclass feature · **7** Evasion + Stillness of Mind · **9/11** subclass features · **14** Diamond Soul · **18** Empty Body · **20** Perfect Self |
| **Dip value** | High at **1** (free 10+DEX+WIS AC on any unarmoured character, plus a bonus-action unarmed strike). High at **3** (feat-neutral, full subclass, Deflect Missiles). Low at 2. |

---

## Class changes from vanilla

### `Monk 5e Adjustments` (`1411`)
Archive pulled: `Monk 5e Adjustments-1411-3-4-2-1769760109.zip` — the **main file, v3.4.2**,
installed as `mods\Monk 5e Adjustments\PAK_FILES\Monk 5e Adjustments.pak`. This is the current
Nexus version. Note: the author's own guidance is to use the **"No Tasha"** variant when
`Expansion` is also loaded, because both add Tasha's optional features. **Listo pulled the main
file anyway.** Whether that duplicates Ki-Fueled Attack / Quickened Healing / Focused Aim, or
whether Listo disabled Expansion's Monk optional features via MCM, is **`(unverified)`** — the
`Expansion\settings.json` in `[CUST] Listonomicon Mod Settings` is an inlined 1,398-byte file
whose contents are not in the manifest.

**Save DC change — the important one.** Stunning Strike, Open Hand Technique (Topple / Push) and
Intoxicating Strike all use the **Ki Save DC = 8 + Proficiency Bonus + WIS** instead of the
vanilla Maneuver Save DC (10 + STR or DEX). For multiclassed characters the Ki Save DC always
uses **Wisdom**, never the "primary casting ability".

Other changes:
- **Unarmed Strike unlocked as a level 1 Monk action** — you can make unarmed attacks with the
  Attack action *while holding a weapon*. This is the QoL change the Listo docs call out.
- **Attack of Opportunity: Unarmed** — toggleable passive making your OA an unarmed strike even
  with a weapon equipped.
- **Flurry of Blows: Double Strike** — splits Flurry into "First Strike" / "Second Strike" so
  you can hit two different targets. Open Hand gets split versions of all three Open Hand
  Technique attacks.
- **Stunning Strike (Passive)** — toggleable; applies the stun after any landed melee hit
  (still 1 ki per attempt). Mutually exclusive with Intoxicating Strike (Passive).
- **Slow Fall** reduces fall damage by **5 × Monk level** (not by half) and grants prone
  immunity on landing.
- Tasha's optionals: **Ki-Fueled Attack** (L3 — spend 1+ ki as part of your Action, get a bonus
  action unarmed or monk-weapon attack), **Quickened Healing** (L4 — Action, 2 ki, heal Martial
  Arts die + Proficiency Bonus), **Focused Aim** (L5 — on a miss, spend 1–3 ki for +2 attack
  each). Ki-Fueled Attack only triggers off abilities that cost **both an Action and ki**, plus
  the mod's own Stunning Strike / Focused Aim / Intoxicating Strike passives.

Also installed: **`Open Hand - Compact Buttons`** (`Open Hand - Compact Buttons-1411-1-0-4`), an
optional file from the same mod page that collapses Open Hand's six Flurry buttons into two
expandable hotbar buttons.

### `Warrior of the Elements Monk PHB2024` (`18406`) — base-class effects
Archive pulled: `Warrior of the Elements Monk PHB2024-18406-2-2-1-1769574366.rar` = **v2.2.1**.
Nexus current is **2.3.0**, which only adds a "Beckon Air" action to Elementalism — the
base-class changes below have been in the mod since 1.0.

- **Martial Arts die rescaled to PHB2024 for all Monks:** **1d6 / 1d8 (L5) / 1d10 (L11) /
  1d12 (L17)**.
- **Uncanny Metabolism at level 2 for all Monks** (PHB2024 feature). The mod page does not spell
  out its BG3 implementation — treat "regain all Ki + heal on initiative once per long rest" as
  `(unverified)`.

> Load order caveat: `modsettings.lsx` is inlined in the .wabbajack and unreadable from the
> manifest, so which mod wins on the Martial Arts progression is **`(unverified)`**. Check the
> die on a level 1 character sheet before committing to damage math.

### `Expansion Level 13-20` (`279`)
Archive pulled: `Expansion-279-1-7-3-6-1780876532.zip`, installed as
`mods\Expansion Level 13-20\PAK_FILES\Expansion.pak`. This is Listo's level-20 backbone and the
source of the XP curve.

Monk progression it adds:
- **13** Tongue of the Sun and Moon
- **14** Diamond Soul — Expansion grants proficiency in **all** saving throws, not just STR/DEX
  (author's words: "cursed multiclassing"). Unarmoured Movement increase.
- **15** Timeless Body — Expansion adds "always gain **full** hit points and Ki points from long
  resting".
- **18** Empty Body. Unarmoured Movement increase.
- **20** Perfect Self
- Optional (Tasha's, MCM-gated): Dedicated Weapon (2), Ki-Fueled Attack (3), Quickened Healing
  (4), Focused Aim (5).
- Subclass capstones: **Open Hand → Quivering Palm (17)**, **Shadow → Opportunist (17)**,
  **Four Elements → Disciple of the Elements (13–20)**.
- It also removed "the limitation preventing Monks from making more than one bonus action
  attack when making multiple attacks as part of the Attack action."

### Feats and items that specifically touch Monk
Do not restate these here — grep the referenced files.
- **`Add Unarmed Attacks to Savage Attacker and Savage Attacks`** (`2473`). **Both** archives are
  installed (`Savage_Attacker_Unarmed.pak` and `Savage_Attacks_Unarmed.pak`), so Savage
  Attacker's damage reroll covers unarmed strikes and the Half-Orc Savage Attacks trait does too.
  See `data/listo-10.2-feats.md`.
- **`Unarmored Defence Synergy`** (`2837`, archive `Unarmored Defence Synergy-2837-1-0`). Adds a
  **third** Unarmoured Defence option for a **Monk/Barbarian multiclass**: **10 + WIS + CON, no
  DEX, no shield**. The best of the three is picked automatically; no respec needed. It does
  **not** give 10 + DEX + WIS + CON.
- **Tavern Brawler**, **Dirty Fighting** (unarmed-scaling bonus-action kick), **Savage Attacker**,
  **Druidic Warrior** / **Arcanist** / Essential Feats "Initiate" feats (cheap routes to
  **Shillelagh**) — all in `data/listo-10.2-feats.md`.
- **Corellon's Grace** (`14238`) — quarterstaff that lets you substitute an **unarmed attack**
  for its weapon attack; adds Corellon's Fist. **Ghoul Touch Weaponry** (`15659`) includes monk
  gloves. **Way of Shadow Revised - Katanas** (`21534`) adds 5 katanas. All in
  `data/listo-10.2-equipment.md`.
- **Lizardfolk** (`22963`) — 1d6 + STR bite usable as an unarmed strike, bonus-action Hungry Jaws
  granting temp HP, and 13 + DEX natural armour. See `data/listo-10.2-races.md`.

---

## Ways (subclasses)

Eleven Ways: the three vanilla ones, the six in Sumradagnoth's combined pack, `Warrior of the
Elements`, and `Way of the Friar` from the DTO archetype pack.

### Way of the Open Hand *(vanilla)*
- **Mod:** base game; level 13–20 from `Expansion Level 13-20` (`279`)
- **Mechanics:** Open Hand Technique riders on Flurry of Blows (Topple / Push / Stagger) —
  in Listo these use the **Ki Save DC (8 + PB + WIS)**, not the Maneuver DC (`1411`). Wholeness
  of Body, Tranquility, Quivering Palm at **17** (added by Expansion). `Open Hand - Compact
  Buttons` collapses the six Flurry variants into two hotbar buttons; `1411` also adds split
  First/Second Strike versions of all three techniques so you can spread them across targets.
- **Duo relevance:** Topple and Push are free control on every Flurry, and they now scale off the
  stat you already want. In a two-character party, control that costs no extra action is worth
  more than raw damage.

### Way of Shadow *(vanilla)*
- **Mod:** base game; level 13–20 from `Expansion Level 13-20` (`279`)
- **Mechanics:** Shadow Arts (Hide / Pass Without Trace / Darkness) for ki, Shadow Step,
  Cloak of Shadows, **Opportunist at 17** (added by Expansion).
- **Duo relevance:** the two-person party has no dedicated scout; Shadow Arts covers stealth,
  repositioning and party-wide Pass Without Trace off one resource pool that refills on a short
  rest. Note `Way of Shadow Revised` itself is **not** in Listo — only its katana add-on.

### Way of the Four Elements *(vanilla)*
- **Mod:** base game; level 13–20 from `Expansion Level 13-20` (`279`) — Disciple of the Elements
  continues 13–20
- **Mechanics:** vanilla elemental disciplines paid for in ki. Expansion fixed "Four Elements
  Monk not being able to switch out disciplines after 17th level".
- **Duo relevance:** superseded in almost every respect by Warrior of the Elements below, which
  is a separate subclass rather than a replacement. Pick it only for the vanilla discipline list.

---

### Way of the Ascendant Dragon
- **Mod:** `5e Monk Subclasses Combined` (`15907`)
- **File pulled:** `MonkSubclasses5eCombined.zip-15907-1-0-5-4-1770553234.zip` — **v1.0.5.4**,
  current on Nexus
- **Mechanics:**
  - **3 — Draconic Disciple:** Draconic Presence is a toggle that auto-activates in dialogue and
    grants **Advantage** on a Charisma check; once it turns a failure into a success it's spent
    until long rest. Draconic Strike changes unarmed damage to acid/cold/fire/lightning/poison
    via a set of toggles that retune **every** elemental ability in the subclass at once.
  - **3 — Breath of the Dragon:** replace one attack of the Attack action with a 20-ft cone or
    30-ft × 5-ft line; DEX save vs **Ki Save DC**, **two Martial Arts dice** on a fail, half on a
    success. **Three dice at 11.** Uses = proficiency bonus, long rest; beyond that, **2 ki** per
    use.
  - **6 — Wings Unfurled:** with the toggle on, Step of the Wind grants **flight** for the turn.
    Uses = proficiency bonus per long rest.
  - **11 — Aspect of the Wyrm:** bonus action, 10-ft aura, 1 minute. Either **Frightful Presence**
    (bonus action to force a WIS save; the implementation blocks movement *toward* you only,
    not all movement) or **Resistance** to the chosen element for you *and allies in the aura*.
    Once per long rest, then **3 ki**.
  - **17 — Ascendant Aspect:** Augment Breath (**1 ki** to upcast the breath to a 60-ft cone /
    90-ft line and **four** Martial Arts dice — appears as upcasts on the ability); Blindsight
    10 ft, **which requires `Tasha's Fighting Styles RAW` to be loaded — that mod is not in the
    10.2 TSV, so treat Blindsight as non-functional `(unverified)`**; Explosive Fury, an
    interrupt dealing 3d10 of your chosen element to any number of creatures in the aura on a
    failed DEX save.
- **Duo relevance:** the only Way here that hands the *other* character a defensive buff —
  Aspect of the Wyrm's resistance aura covers allies. Breath of the Dragon is also real AoE from
  a class that normally has none, without spending your Bonus Action.

### Way of the Astral Self
- **Mod:** `5e Monk Subclasses Combined` (`15907`)
- **File pulled:** same archive, **v1.0.5.4**. Requires Script Extender for the Wisdom-based
  attack conversion.
- **Mechanics:**
  - **3 — Arms of the Astral Self:** bonus action + **1 ki**; creatures within 10 ft take **two
    Martial Arts dice** force damage on a failed DEX save. For **10 minutes** you may use
    **WIS in place of STR** for Strength checks and saves, attack with the spectral arms at
    **+5 ft reach**, and — the headline — the arms' unarmed strikes use **WIS for attack and
    damage rolls**, dealing **force** damage. A hotbar toggle switches between astral and normal
    unarmed attacks.
  - **6 — Visage of the Astral Self:** bonus action + **1 ki** (or folded into the Arms bonus
    action). Darkvision 120 ft including magical darkness; advantage on Insight and Intimidation.
  - **11 — Body of the Astral Self:** automatic when Arms + Visage are both up. **Deflect Energy**
    — reaction reducing acid/cold/fire/force/lightning/thunder damage by **1d10 + WIS**.
    **Empowered Arms** — toggle, +1 Martial Arts die once per turn on an arms hit.
  - **17 — Awakened Astral Self:** bonus action, **5 ki**, 10 minutes: **+2 AC** and **three
    attacks** instead of two when all are made with the astral arms.
- **Duo relevance:** **the single-stat Monk.** WIS covers attack, damage, AC, and Ki Save DC, so
  DEX and STR can both stay low and points go into CON. Deflect Energy is a per-round reaction
  mitigation, and Lone Wolf grants an extra Reaction — this Way is the best user of that extra
  reaction in the class.

### Way of the Kensei
- **Mod:** `5e Monk Subclasses Combined` (`15907`)
- **File pulled:** same archive, **v1.0.5.4** (the last two patch releases were Kensei bug fixes)
- **Mechanics:**
  - **3 — Path of the Kensei:** choose one melee and one ranged weapon type (any simple/martial
    without heavy or special; longbow allowed). You gain proficiency and they become **monk
    weapons for you**. Another weapon type at **6, 11, and 17**.
    **Agile Parry** — make an unarmed strike as part of the Attack action while holding a melee
    kensei weapon for **+2 AC** until the start of your next turn.
    **Kensei's Shot** — bonus action; ranged kensei hits deal **+1d4** for the turn.
    Way of the Brush is replaced with **Performance proficiency**.
  - **6 — One with the Blade:** kensei weapons count as **magical**; **Deft Strike** — a toggle
    that spends **1 ki** to add a Martial Arts die to the first hit while it's on (once per turn;
    stacks with interrupts like Sneak Attack).
  - **11 — Sharpen the Blade:** bonus action, up to **3 ki**, granting the touched kensei weapon
    **+X to attack and damage** for 1 minute. Targets your **active weapon set** and the hand
    picked by a hotbar toggle. **No effect on a weapon that already has an enchantment bonus.**
  - **17 — Unerring Accuracy:** reroll one missed monk-weapon attack per turn.
- **Duo relevance:** the Way that makes Monk a *weapon* character, which matters because Listo's
  weapon pool is enormous and its unarmed pool is not. Agile Parry's +2 AC is on nearly every
  turn for free. Damage bonuses do **not** show on weapon tooltips — read the combat log.

### Way of the Long Death
- **Mod:** `5e Monk Subclasses Combined` (`15907`)
- **File pulled:** same archive, **v1.0.5.4**
- **Mechanics:**
  - **3 — Touch of Death:** reduce a creature within 5 ft to 0 HP → **temp HP = WIS + monk level**
    (min 1).
  - **6 — Hour of Reaping:** Action; every creature within 30 ft that can see you makes a WIS save
    or is **frightened** until the end of your next turn. Implemented so it blocks movement
    *toward you* only, not all movement.
  - **11 — Mastery of Death:** toggleable; when reduced to 0 HP, spend **1 ki** (no action) to
    drop to **1 HP instead**.
  - **17 — Touch of the Long Death:** Action; spend **1–10 ki** for **2d10 necrotic per ki** on a
    failed CON save, half on a success. Delivered as a container of one spell per ki amount.
- **Duo relevance:** **Mastery of Death is the strongest single line in this file for a two-person
  Lone Wolf run.** Losing either character usually ends the fight; this converts that loss into
  1 ki, repeatably, from a pool that refills on a short rest. Touch of Death's temp HP stacks the
  same insurance on every kill.

### Way of Mercy
- **Mod:** `5e Monk Subclasses Combined` (`15907`)
- **File pulled:** same archive, **v1.0.5.4**
- **Mechanics:**
  - **3 — Implements of Mercy:** proficiency in **Insight and Medicine**.
  - **3 — Hands of Healing:** Action, **1 ki**, heal **Martial Arts die + WIS**. When you Flurry,
    you may replace **one** unarmed strike with this **for free**.
  - **3 — Hands of Harm:** **1 ki** on an unarmed hit for **Martial Arts die + WIS necrotic**,
    once per turn.
  - **6 — Physician's Touch:** Hands of Healing also ends one of blinded / deafened / paralysed /
    poisoned / stunned — and if you choose disease, it removes **all** diseases. Hands of Harm
    additionally **poisons** (toggle).
  - **11 — Flurry of Healing and Harm:** Flurry can replace **every** strike with free Hands of
    Healing, and Hands of Harm becomes **free** on Flurry strikes (still once per turn).
  - **17 — Hand of Ultimate Mercy:** Action, **5 ki**, **resurrect** a corpse for **4d10 + WIS**
    HP with blinded/deafened/paralysed/poisoned/stunned cleared. Once per long rest. The
    implementation **drops the 24-hour limit**.
- **Duo relevance:** the strongest fit for a duo with no healer. From 11 this is a full-power
  heal on your **Action** with Flurry as the vehicle, costing nothing but the ki you already
  regenerate on short rests — and Hand of Ultimate Mercy is a free in-combat rez every long rest,
  which is a whole failure mode removed from a two-character party.

### Way of the Sun Soul
- **Mod:** `5e Monk Subclasses Combined` (`15907`)
- **File pulled:** same archive, **v1.0.5.4**
- **Mechanics:**
  - **3 — Radiant Sun Bolt:** a 30-ft **ranged spell attack** using **DEX** for attack and damage,
    dealing **radiant** damage on the **Martial Arts die**. Usable for any attack of the Attack
    action once you have Extra Attack; after an initial Sun Bolt, spend **1 ki** to fire twice
    more as a **bonus action**. Author's warning: tooltips and combat log look wrong because it's
    a ranged spell attack driven by an unusual ability — cosmetic.
  - **6 — Searing Arc Strike:** after the Attack action, **2 ki** to cast **Burning Hands** as a
    bonus action; each extra ki upcasts it by one level, capped at **half your monk level** total.
  - **11 — Searing Sunburst:** Action; 20-ft radius at up to 150 ft, CON save or **2d6 radiant**,
    **+2d6 per ki up to 3**. Total cover blocks the save entirely.
  - **17 — Sun Shield:** permanent bright light 30 ft; reaction on being hit in melee to deal
    **5 + WIS radiant**.
- **Duo relevance:** the only Way that turns a Monk into a genuine **ranged** character without
  giving up the class. In a duo, having one character who can contribute at range without moving
  is a real answer to the action-economy problem. Note this Way scales on **DEX**, not WIS —
  it is the odd one out in a Listo Monk lineup and does not benefit from the Ki Save DC change.

### Warrior of the Elements *(PHB2024 rework of Four Elements)*
- **Mod:** `Warrior of the Elements Monk PHB2024 DnD 5R` (`18406`)
- **File pulled:** `Warrior of the Elements Monk PHB2024-18406-2-2-1-1769574366.rar` = **v2.2.1**.
  **Nexus is on 2.3.0**, which adds only a "Beckon Air" action to Elementalism — everything
  below is present in 2.2.1.
- **Mechanics:** a **separate subclass**; it does not replace vanilla Four Elements.
  - **3 — Elementalism and Elemental Attunement:** attune to **acid, cold, fire, lightning or
    thunder**. Elemental Strikes can be set to **replace your default unarmed attack**, which
    also makes your **Attacks of Opportunity** use the extended range, elemental damage, and the
    push/pull rider. Every Monk attack that's compatible can be converted to the chosen element.
    Elementalism itself is explicitly **not RAW** — it's the author's interpretation.
  - **6 — Elemental Burst**, **11 — Stride of the Elements**, **17 — Elemental Epitome**
    (Destructive Strides, Elemental Resistance, Empowered Strikes). The mod page defers the
    numbers to in-game screenshots, so specific values are **`(unverified)`**.
  - v2.1 fixed "all offensive monk abilities not scaling with Wisdom spellcasting modifier when
    multiclassing" — so this Way is WIS-scaled.
- **Duo relevance:** on-hit **push/pull on your opportunity attacks** is control you get for free
  on the enemy's turn, which is the cheapest action economy in the game for a two-person party.
  Damage-type selection also answers Listo's resistant enemies without swapping gear.

### Way of the Friar
- **Mod:** `(DTO) Otherworldy Archetypes` (`21822`)
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67 2026-06-17T17-15Z PYJWETtYB.zip` —
  **v1.2.0.67**, current on Nexus. Mechanics below are from the author's own reference site
  (prizzels.github.io/DTO), not the Nexus blurb.
- **Mechanics:**
  - **3 — Friar's Bond:** Bonus action, **1 ki**, range **12 m**, **Concentration**. Designate an
    ally as your Kin. You **and** your Kin gain **temporary HP equal to your WIS modifier at the
    start of each turn**. Four **Blessing variants** to choose from:
    - *Friar's Blessing* — **+1d4 to attack rolls and saving throws**
    - *Friar's Valor* — **+1d4 radiant** on weapon attacks
    - *Friar's Retribution* — **twice your WIS modifier in radiant damage** back at any attacker
    - *Friar's Faith* — **+1 AC** and **resistance to psychic, necrotic and radiant** while you
      have temporary HP
  - **3 — Friar's Grace:** Bonus action, **no ki cost**, base range 9 m **scaling with WIS** —
    teleport to a space beside your Kin. Unlocked by casting Friar's Bond.
  - **3 — Guardian of Light:** **shield proficiency**, and while a shield is equipped you get
    **advantage on Concentration checks** and **still benefit from Unarmoured Defence**.
    **Guidance** always prepared.
  - **6 — Staff Mastery:** with a quarterstaff equipped, attacks gain **Reach (2.5 m)**, +1 m at
    11 and again at 17.
  - **6 — Guiding Strike:** bonus action, **2 ki** — staff hit that illuminates the target and
    grants **advantage on attacks against it** until the start of your next turn.
  - **6 — Pacifying Sweep:** Action, **2 ki** — hits all foes in an arc, **knocks back 3 m** on
    hit; WIS save or **Pacified for 2 turns** (cannot take actions unless damaged).
  - **9 — Cleansing Wave:** Action, **3 ki**, 9 m 75° cone — cures you and allies of Poison,
    Blind, Paralysis, Disease, Charm, Petrify, Stun and Curse. **Once per battle.**
  - **11 — Shared Resolve:** bond a **second** ally, and gain additional temp HP per turn.
  - **17 — Community:** bond a **third** ally.
- **Duo relevance:** **this Way is built for exactly this run.** With two characters, Friar's Bond
  covers the *entire party* from level 3 — Shared Resolve and Community are dead weight for you,
  but the level 3 package alone is per-turn temp HP on both characters, a free-teleport repositioning
  tool to your partner, a shield you're allowed to wear, and Guiding Strike handing your partner
  advantage. Friar's Retribution scales on WIS, the stat the rest of the class already wants.

---

## Building a Monk in Listo

**Stats.** Wisdom is the primary ability, not a tertiary one. It sets Unarmoured Defence AC, the
**Ki Save DC (8 + PB + WIS)** that Stunning Strike and Open Hand Technique now use, and the
scaling on Astral Self, Friar, Long Death, Mercy and Warrior of the Elements. The classic
"STR 8, drink an elixir, take Tavern Brawler" spread is gone: Tavern Brawler no longer touches
your ability scores and gives a flat **(PB − 1)**, and Elixirs of Giant's Strength only *add* to
whatever STR you already have.

Two workable spreads:
- **WIS/DEX** — the default. DEX for attack rolls and the second half of Unarmoured Defence.
  Works with every Way.
- **WIS-only** — **Way of the Astral Self** from level 3 puts attack, damage, AC and save DC all
  on WIS. DEX and STR can be left low and the points banked in CON, which matters more here
  because Lone Wolf multiplies max HP.

**Tavern Brawler is still takeable, just not build-defining.** (PB − 1) is **+5 to attack and
damage** at level 17+ on every unarmed strike including every Flurry attack — respectable, but no
longer the reason to be a Monk. See `data/listo-10.2-feats.md` before pricing it.

**What actually carries damage now:**
- **Attack volume.** Flurry of Blows, plus Ki-Fueled Attack turning any Action+ki ability into
  another bonus-action strike, plus `1411` unlocking unarmed strikes **while armed**. Lone Wolf's
  extra Bonus Action doubles the value of everything on that budget.
- **Savage Attacker.** `2473` extends the reroll to unarmed strikes, and Monk makes more
  individual attack rolls per round than any other class — the reroll is worth more here than
  anywhere else.
- **Weapons, via Kensei.** Listo's weapon pool is far deeper than its unarmed pool. Kensei makes
  arbitrary weapons into monk weapons and adds Sharpen the Blade's +3.
- **Shillelagh, via a feat.** The Listo docs explicitly suggest Monks take `Arcanist` or an
  Essential Feats "Initiate" feat to get **Shillelagh** without a Druid dip; Listo buffs it
  substantially and extends it to a wide weapon list. Whether it overrides Martial Arts' DEX
  substitution on a quarterstaff is **`(unverified)`** — test in-game before building on it.
- **Lizardfolk's bite** (`22963`): 1d6 + **STR** slashing usable for unarmed strikes, plus a
  bonus-action Hungry Jaws granting temp HP. This is the one place where STR still buys unarmed
  damage — see `data/listo-10.2-races.md`.

**Ki is your real budget, and it is cheap.** Ki refreshes on a **short rest**, while long rests
cost 120+ camp supplies scaling with camp population. Every Way above prices its good abilities
in ki. In practice this makes Monk one of the least rest-hungry characters in the list.

**Multiclass notes.** Monk/Barbarian is uniquely supported: `Unarmored Defence Synergy` (`2837`)
adds a **10 + WIS + CON** unarmoured AC option so a STR/CON Barbarian-Monk isn't forced into
medium armour. If you go this route, take **Monk at level 1** for the STR + DEX saves, or Barbarian
at 1 for STR + CON — you only get one set.

---

## Dip value

- **Monk 1** — the strongest single level for any unarmoured character: **Unarmoured Defence
  (10 + DEX + WIS)**, Martial Arts (bonus-action unarmed strike after an Attack), and Flurry of
  Blows. If taken at character level 1 it also grants **STR + DEX** save proficiency, which is
  the better half of the save table for avoiding hard control.
- **Monk 2** — Unarmoured Movement, Patient Defence, Step of the Wind, and **Uncanny Metabolism**
  from `18406`. Rarely worth stopping here.
- **Monk 3** — the standard dip. **Feat-neutral** under Listo's 3/6/9/12/15/18 cadence, gets you a
  full subclass entry, and Deflect Missiles. The best 3-level payloads for a duo are **Way of the
  Friar** (per-turn temp HP for both characters, shield proficiency, free teleport to your
  partner) and **Way of Mercy** (free healing folded into Flurry).
- **Monk 5** — Extra Attack plus Stunning Strike. Expensive as a dip, and Extra Attack does not
  stack with another class's, so this is only for characters where Monk is the main class.
- **Deep Monk** — the payoff levels are **11** (subclass tier-3: Astral Body, Long Death's Mastery
  of Death, Mercy's free Flurry healing) and **17** (all six pack capstones plus Quivering Palm /
  Opportunist from Expansion). Level cap 20 makes both reachable.

---

## Not present

- **Way of the Drunken Master.** Removed. Listo's changelog shows it was added, then all
  individual Monk subclass mods were removed and replaced with `5e Monk Subclasses Combined`,
  which does **not** include Drunken Master. Neither the TSV nor the manifest contains it.
  Residual references survive in two installed mods and do nothing on their own: `Monk 5e
  Adjustments` still ships Drunken Technique: Double Strike and the Intoxicating Strike passive,
  and `Expansion` still grants Intoxicated Frenzy at 17 to a subclass that isn't there.
- **`Stone and Steel - Expanded Monk Strikes`.** Explicitly REMOVED in the changelog.
- **`Alternate Monk Complete`.** REMOVED; `Monk 5e Adjustments` replaced it.
- **`Way of Shadow Revised`** (the subclass). Only its katana add-on (`21534`) is in the list, and
  that add-on is **fully standalone and adds weapons only** — it does not change Way of Shadow.
- **`Drunken Humming`** (`20345`) is **cosmetic/audio only** — "Tav & friends can drunkenly hum the
  main theme of the game". It is not a Drunken Master implementation.
- **`Tasha's Fighting Styles RAW`.** Not in the 10.2 list, which means Ascendant Dragon's level 17
  **Blindsight** has no supporting implementation.
- **`OneDnD Monk's Discipline` / `OneDnD Martial Arts`.** Not in the list, so `18406`'s optional
  compatibility patch is irrelevant.
- **Monk-specific parts of `Level 13-20 Extended`** were disabled long ago; `Expansion Level 13-20`
  (`279`) is the sole level 13–20 source.
