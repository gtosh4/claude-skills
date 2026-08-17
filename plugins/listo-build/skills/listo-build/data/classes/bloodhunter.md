# Listonomicon 10.2 — Blood Hunter

> **Provenance: CONFIRMED PRESENT in 10.2. Ships from mod.io, not Nexus — the usual TSV check does not apply.**
>
> Blood Hunter is **absent from `listo-10.2-mods.tsv` by design**: that file lists Nexus mods only.
> Its absence there is *not* evidence it is missing. It was confirmed directly in
> `listo-10.2-manifest.json`:
>
> - Archive: `bloodhunter_860e44bd-5c0a-ad19-g06x.zip`, 17,000,714 bytes, Wabbajack hash `6fMlZusiYiU=`
> - Download URL: `https://g-6715.modapi.io/v1/games/6715/mods/5218924/files/7541860/download`
>   (one of the 8 `modapi.io` archives in the manifest; the other 7 are unrelated)
> - Installs to `mods\[ModIO] Bloodhunter\PAK_FILES\BloodHunter_860e44bd-5c0a-ad19-3553-1f2ec8c8b2ca.pak`
>   (19,041,112 bytes), with a dedicated MO2 separator `mods\Bloodhunter_separator\`
> - Docs page 4 (`4-SpellsFeatsClassesItems.md:117`) lists **Bloodhunter** under *Brand New Classes*,
>   linking `https://mod.io/g/baldursgate3/m/blood-hunter`
>
> **Everything mechanical below was read out of the shipped `.pak` itself**, not from the mod page
> and not from tabletop. The mod.io page is client-side rendered and its API requires a key, so the
> pak was downloaded from the manifest URL, unpacked (LSPK v18, 492 files), and its
> `ClassDescriptions.lsx`, `Progressions.lsx`, `ActionResourceDefinitions.lsx`, `LevelMapValues.lsx`,
> `Lists/*.lsx`, `Stats/Generated/Data/*.txt` and `Localization/English/english.xml` were read
> directly. Facts sourced any other way are labelled inline. Facts I could not settle are marked
> `(unverified)`.
>
> - **Mod:** "Blood Hunter Class" by **LemonSoup** (mod.io publish handle `5218924`), MD5
>   `8993047713a13fcd1735b641e84e7909`, depends on `GustavX`.
> - **Changelog history** (`5-ChangeLog.md`, newest-first): considered but deferred at **v7.0.9**
>   (line 775 — "might get added to Listo if it gets another update to fix various issues and support
>   level 20 properly"); **ADDED at v8** (line 504); **updated at v9.0.3** (line 172). No removal
>   entry exists. It has been in the list continuously since v8.
> - Level 20 support is real: the progression tables in the shipped pak run 1–20 for the base class
>   and all four Orders.

---

## At a glance

| | |
|---|---|
| **Class name (internal)** | `BloodHunter`, UUID `742e494e-b0aa-45a8-9123-ae0ea274c9e4` |
| **Primary ability** | **Dexterity** (`PrimaryAbility=2`) |
| **Spellcasting / DC ability** | **Intelligence** (`SpellCastingAbility=4`) — for *all* Orders, including Profane Soul |
| **Hit die** | **d10** (`BaseHp 10`, `HpPerLevel 6`) |
| **Saves at level 1** | **Intelligence + Dexterity**. No Constitution save. Granted **only** on the level-1 class entry — a Blood Hunter *dip* grants no saves. |
| **Armour** | Light, Medium, **Shields**. No heavy. |
| **Weapons** | Simple **and Martial**. |
| **Skills** | 3 (1 if multiclassing in) from: Acrobatics, Arcana, Athletics, History, Insight, Investigation, Religion, Survival |
| **Caster tier** | **None** for the base class and 3 of 4 Orders. Only **Profane Soul** casts, at roughly one-third Warlock (pact slots, short-rest, INT-based) — see below. |
| **Resource cadence** | **Short rest** for everything that matters: Blood Maledict, Brand, Hybrid Transformation, Mutagen, Aether Walk. **Long rest** only for Adrenaline Burst and Exalted Mutation. `VitalEssence` replenishes **per turn** (10/turn) and is a hidden throttle, not a budget. |
| **Native ASI/feat levels** | 4, 8, 12, 16, 19 — but see *Known issues* re: Listo's feat mod |
| **CC recommended array** | STR 8 / DEX 14 / CON 15 / INT 14 / WIS 12 / CHA 8 |
| **Starting kit** | 2× Shortsword, Light Crossbow, `ARM_BloodHunter` (studded leather), leather boots, silver amulet, 2× healing potion, Revivify scroll, alchemy pouch |
| **Dip value** | **High at 1–3.** See *Dip value* below. |

**Hemocraft die** (`LevelMapValues.lsx`, keyed to class level) — this single die drives Crimson Rite
damage, all self-damage, and several Order features:

| Class level | 1–4 | 5–10 | 11–16 | 17–20 |
|---|---|---|---|---|
| Hemocraft die | 1d4 | 1d6 | 1d8 | 1d10 |

**Base-class level table** (from `Progressions.lsx`, table `2ccbd5e4-…`):

| Lvl | Gains |
|---|---|
| 1 | Hunter's Bane (Adv. on Survival), Hemocraft Magic, **Blood Maledict ×2**, Vital Essence 10, 3 skills, **2 Blood Curses** |
| 2 | **Crimson Rite** (pick 1 rite) + **Fighting Style** (pick 1 of 5) |
| 3 | **Order** (subclass); Blood Maledict → 3 |
| 4 | ASI/feat |
| 5 | **Extra Attack** |
| 6 | **Brand of Castigation** (+1 `Brand` charge); Blood Maledict → 4; +1 Blood Curse |
| 7 | +1 Crimson Rite |
| 8 | ASI/feat |
| 9 | Grim Psychometry (Adv. History), Grim Communion (highlights speakable corpses); Blood Maledict → 5 |
| 10 | **Dark Augmentation**: +1.5 m movement, and add `max(1, INT mod)` to **STR, DEX and CON saves**; +1 Blood Curse |
| 11 | — (Order feature only) |
| 12 | ASI/feat |
| 13 | **Brand of Tethering** (Brand retaliation damage doubled); Blood Maledict → 6 |
| 14 | +1 Crimson Rite (→ all 3), +1 Blood Curse |
| 15 | — (Order feature only) |
| 16 | ASI/feat |
| 17 | Blood Maledict → 7 |
| 18 | +1 Blood Curse (→ 6 total) |
| 19 | ASI/feat |
| 20 | **Sanguine Mastery**: roll Crimson Rite damage dice twice and take the higher; on a crit with a Rite, **regain a Blood Maledict** |

Fighting Style list is fixed at five: Archery, Defense, Dueling, Great Weapon Fighting,
Two-Weapon Fighting.

---

## Crimson Rite and the HP economy

**The single most important correction to the tabletop mental model: in this conversion Crimson Rite
is a one-off up-front payment per weapon per long rest, not a per-attack cost.**

Mechanically (`Spell_Shout.txt` / `Status_BOOST.txt`):

- **Cast:** bonus action + 1 `VitalEssence`. Requires a wielded weapon with the `Dippable` property
  and that the weapon does not already carry that rite.
- **Cost:** applies `ESSENCE_SACRIFICE` to self, which deals **one hemocraft die of magical Necrotic
  damage** to you. At level 1–4 that is 1d4; at 17–20 it is 1d10.
- **Benefit:** applies `CRIMSON_RITE_<TYPE>` to the *weapon*, permanent duration, adding
  **one hemocraft die of that element** to that weapon's hits. Tooltip states it lasts *"until your
  next Long Rest"*. Separate rites can go on main hand, off hand, and (Lycan only) unarmed strikes.
- **Rites available:** Flame (Fire), Frozen (Cold), Storm (Lightning) — pickable at 2, 7, 14.
  Ghostslayer also gets **Rite of the Dawn** (Radiant) free at 3.
- **Anti-cheese clause:** `ESSENCE_SACRIFICE` deals **double dice if you are resistant to Necrotic**.
  This is compensation, not a penalty — the doubling exactly cancels the resistance halving, so
  stacking Necrotic resistance (including Ghostslayer's own Rite of the Dawn) neither reduces nor
  increases the true cost.

**The recurring HP cost is amplified Blood Curses, not the Rite.** Every Blood Curse has an
Amplified variant costing an extra `ESSENCE_SACRIFICE` (one hemocraft die of self Necrotic) on top
of the Blood Maledict charge.

### Duo assessment (2 players, Lone Wolf, cap 20)

Honestly: **the HP economy is much less dangerous here than the tabletop reputation suggests.**

- The Rite cost is paid **once per weapon per long rest** and should always be paid **out of
  combat**. At level 11–16 that is 1d8 off a Lone Wolf'd d10 pool with +30% max HP — noise.
- Listo's healing-potion nerf (limited immediate + delayed heal, see the docs page 4 economy notes)
  therefore does **not** bite the way it would for a per-attack HP class. You are not topping up
  mid-fight to fund your damage.
- The genuinely risky button is **amplifying a Blood Curse while below half HP**. That is a
  deliberate in-combat HP payment for a debuff. With no third body to pick anyone up, the rule of
  thumb is: amplify freely above ~60% HP, never below ~35%.
- **Lone Wolf's "halved damage from all sources" and `ESSENCE_SACRIFICE`:** `(unverified)`. If Listo
  implements Lone Wolf as generic incoming-damage reduction, the self-damage is halved and the cost
  is trivial. If it is implemented as blanket damage *Resistance* — including Necrotic — the mod's
  doubling clause fires and the net cost is unchanged. Either way the outcome is neutral-to-good;
  there is no branch where this gets worse.
- Two counter-currents that actually matter more: **Rite Revival** (Ghostslayer 18) turns the HP
  economy into a free extra life, and **Order of the Lycan's Bloodlust** is the one Order that
  genuinely punishes low HP (see below).

### The short-rest fit is the real duo argument

Every meaningful Blood Hunter resource replenishes on a **short rest**: Blood Maledict, Brand,
Hybrid Transformation, Mutagen, Aether Walk. Long rests in Listo cost 120+ camp supplies scaling
with camp population; short rests are free. A class whose whole kit refills for free between fights
is unusually well matched to this run's supply pressure.

### The action-economy fit

Blood Hunter spends **bonus actions and reactions**, leaving the Action free for attacks:

- Crimson Rite — bonus action, once per weapon per long rest
- Most Blood Curses — bonus action
- Eyeless, Exposure, Fallen Puppet, Soul Eater — **reactions**
- Brand of Castigation — a free interrupt on a Rite hit; its retaliation is also a free interrupt

In a two-body party, off-turn damage and off-turn debuffs are the scarcest resource. This is the
class's strongest structural argument for the run.

---

## Blood Curses

Cast with **`Blood Maledict`** (short rest), 9 m range, bonus action (or reaction for the
interrupt-style ones). Amplifying adds one hemocraft die of self Necrotic damage.

**Critical finding for build planning: almost none of the base curses allow a saving throw.** Of the
eight base curses, only **Binding** rolls (STR save vs your spell DC). The other seven apply
automatically. Corrosion (Mutant) grants a CON save to *end* the effect each turn; MuddledMind's
amplified Silence rider and Howl (Lycan) use CON and WIS saves respectively. **This means a low-INT
Blood Hunter dip still gets full value from the majority of the curse list** — a genuinely unusual
property.

**Bloodless rule:** Undead, Constructs, Elementals, Plants and Oozes cannot be targeted by a curse
**unless it is Amplified** — or unless you are a Ghostslayer with Curse Specialist, which removes
the restriction entirely.

Known curses: 2 at level 1, +1 at 6, 10, 14, 18 → **6 total** (7 for Ghostslayer, which grants an
extra pick at level 3). The eight-curse selection pool:

| Curse | Base effect | Amplified adds |
|---|---|---|
| **The Marked** | Your Crimson Rite attacks against it roll an extra damage die | Next attack against it this turn has Advantage |
| **Bloated Agony** | Disadv. on STR/DEX checks; takes 1d8 Necrotic per attack it makes on its turn | (self-damage only) |
| **The Eyeless** *(reaction)* | −(hemocraft die) penalty to the triggering attack roll | Penalty applies to **all** its attack rolls |
| **Exposure** *(reaction)* | Strip **Resistance** to damage types in an incoming hit | Strips **Immunity** too |
| **The Fallen Puppet** *(reaction, on death)* | Dying creature makes one attack on its allies; cannot move | It can also move up to half speed |
| **Binding** | Cannot move or take Reactions (STR save) | (self-damage only) |
| **The Muddled Mind** | Disadv. on Concentration saves | CON save or **Silenced** |
| **The Anxious** | Advantage on CHA/Intimidation checks against it | Its next WIS save has Disadvantage |

**Exposure is the standout for a duo.** Stripping Resistance (Amplified: Immunity) off a boss as a
reaction, with no save, is the kind of effect that a four-person party gets from a dedicated caster
and a two-person party normally has to go without.

---

## Brand of Castigation (level 6)

- Free interrupt on a hit with a Crimson Rite weapon; costs 1 `Brand` charge (short rest,
  once per short rest), applies `BRAND_OF_CASTIGATION` permanently and `AURA_OF_CASTIGATION` to you.
- Each time the branded creature damages **you or a nearby ally**, you retaliate for damage equal to
  your **Intelligence modifier**, as a free interrupt with no resource cost.
- **Level 13, Brand of Tethering:** that retaliation damage is doubled.
- Each Order replaces `Brand_Castigation` with an upgraded brand at 11 or 15 (see below).

Duo note: "you or a **nearby ally**" is a two-target aura in a two-person party — you cover both
bodies. It is small, constant, free damage, and it is one of the few off-turn effects that keys off
your partner being attacked.

---

## Orders (subclasses)

All four tabletop Orders are implemented, chosen at level 3, with features at **3, 7, 11, 15, 18**.

### Order of the Ghostslayer

- **Mechanics (3):** **Rite of the Dawn** — a fourth Crimson Rite dealing Radiant, plus **Necrotic
  Resistance**, plus an extra hemocraft die of Radiant against Undead. **Curse Specialist**: +1 Blood
  Maledict (4 at level 3, one ahead of every other Order for the whole game) *and* your Blood Curses
  ignore the Bloodless restriction entirely.
- **(7):** **Aether Walk** — become intangible for INT-mod rounds and cast Aether Step; 1 charge per
  short rest, 2 from level 15.
- **(11):** **Brand of Sundering** — Crimson Rite damage against a branded creature rolls **two**
  dice instead of one.
- **(15):** **Blood Curse of the Exorcist** — free a Charmed/Frightened/Possessed creature;
  amplified also grants immunity for 2 turns. +1 Aether Walk.
- **(18):** **Rite Revival** — with an active Crimson Rite, dropping to 0 HP instead restores 1 HP
  and ends all your Rites.
- **Duo relevance:** the strongest pick for this run. Rite Revival is a literal answer to "losing
  either character usually ends the fight"; Curse Specialist front-loads the extra Blood Maledict
  from level 3; the Exorcist curse is a two-body party's only reliable Charm/Fear break.

### Order of the Lycan

- **Mechanics (3):** **Hybrid Transformation** (3/short rest) — while transformed you gain **Feral
  Might** (Adv. on STR checks and STR saves, +1 melee damage rising to +2 at 11 and +3 at 18),
  **Resilient Hide** (Resistance to non-magical B/P/S; +1 AC out of heavy armour), **Predatory
  Strikes** (unarmed strikes at 1d6→1d8 from 11, with a scaling attack bonus, and **they scale off
  DEX if DEX is higher than STR**), an extra unarmed strike as a bonus action, and **Unarmed Crimson
  Rite** (any known Rite can be placed on your fists). Also Heightened Senses (Adv. Perception).
  **Downside — Bloodlust:** while transformed, if you start a turn below half HP you must pass a WIS
  save or lose control and attack the nearest creature.
- **(7):** **Stalker's Prowess** (+4.5 m speed, doubled jump distance); unarmed strikes count as
  magical; +1 transformation.
- **(11):** **Lycan Regeneration** — regain 1 + CON mod HP at the start of each turn while below
  half HP; +1 transformation.
- **(15):** **Brand of the Voracious** — attacks against the branded target have Advantage;
  **Voracious Bloodlust** — Advantage on the Bloodlust save.
- **(18):** **Blood Curse of the Howl** (AoE Frighten, WIS save; amplified doubles the radius to
  18 m) and **unlimited** Hybrid Transformations.
- **Duo relevance:** the highest raw damage and the only Order that is actively dangerous in a
  two-body party. Bloodlust turning your character on your partner is exactly the failure mode this
  run cannot absorb, and it triggers at the moment you are already losing. It is manageable — the
  save has Advantage from 15 and the whole thing is off before then if you stay above half HP — but
  it is a real, structural risk between levels 3 and 14. Note the DEX-scaling unarmed strikes make
  it compatible with the class's DEX-primary design.

### Order of the Mutant

- **Mechanics (3):** **Mutagencraft** — 1 Mutagen charge (short rest), pick **4** formulae from a
  16-entry list. Each mutagen grants a benefit and a **side effect**, both lasting until a short or
  long rest. +1 formula at 7, 11, 15, 18 (→ 8 known); +1 charge at 7 and 15 (→ 3).
- **(7):** **Strange Metabolism** — **immune to Poison damage and the Poisoned condition**.
  **Adrenaline Burst** (1/long rest) — suppress all mutagen side effects for 10 turns.
- **(11):** **Improved Mutagencraft** (Celerity/Potency/Sagacity give +4 instead of +3; Mobility adds
  Paralysis immunity); **Brand of Axiom** — branded creatures cannot benefit from Invisibility or
  illusions.
- **(15):** **Advanced Mutagencraft**; **Blood Curse of Corrosion** (Poisoned, CON save each turn to
  end; amplified deals 4d6 up front and again on each failure).
- **(18):** **Expert Mutagencraft** (+5 ability score from Celerity/Potency/Sagacity);
  **Exalted Mutation** — swap one active mutagen for another, 1/long rest.
- **Notable mutagens:** Celerity (+DEX score), Potency (+STR), Sagacity (+INT), Precision (crit range
  −1), Cruelty (extra attack after any attack, at the cost of Disadv. on INT/WIS/CHA saves),
  Vermillion (+1 Blood Maledict, Disadv. on death saves), Rapidity (+3 m speed, +1.5 m more at 15),
  Reconstruction (regain Proficiency Bonus HP at the start of your turn while below half HP), Aether
  (Flight), plus the elemental/physical resistance-for-vulnerability trades (Embers, Gelid,
  Impermeable, Shielded, Unbreakable).
- **Duo relevance:** the flexible pick and the best fit for gear-dependent planning. **Potency and
  Celerity are effectively +3-to-+5 to a raw ability score at a short-rest cost** — cross-reference
  the ability-score-cap section of `listo-10.2-feats.md`, because Listo removed the cap and that
  changes what these are worth. Strange Metabolism's poison immunity is a large defensive swing
  given the poison package in `listo-10.2-equipment.md`. The side effects are real, though:
  every resistance mutagen hands out a matching **vulnerability**, which in a two-body party is a
  much bigger liability than in a four-body one.

### Order of the Profane Soul

- **Mechanics (3):** **Pact Magic** — Warlock spell list, **cast off Intelligence**, slots refresh on
  **short rest**. Choose a **Patron** from nine (Archfey, Celestial, Fathomless, Fiend, Genie,
  Great Old One, Hexblade, Undead, Undying) — these are Blood-Hunter-specific passives defined in
  this mod, not the Warlock subclasses. Also 2 always-prepared spells and 2 known level-1 spells.
- **Slot progression** (pure Blood Hunter, from the `PactMagic_*` passives): **L3** 1 slot @ spell
  level 1 · **L6** 2 slots @ 1 · **L7** 2 slots @ 2 · **L13** 2 slots @ 3 · **L19** 2 slots @ 4.
  Spells known grow at most levels from 3 to 20. Spell level never exceeds 4.
- **(7):** **Mystic Frenzy** — after casting a cantrip, make a weapon attack as a bonus action.
  **Revealed Arcana** — a patron-specific bonus spell.
- **(11):** **Brand of the Sapping Scar** — branded creatures have Disadvantage on saving throws.
- **(15):** **Unsealed Arcana** — a second patron spell.
- **(18):** **Blood Curse of the Soul Eater** — a reaction on an enemy's death.
- **Patron highlights:** Hexblade (cursing a creature adds your Proficiency Bonus to your next damage
  roll against it), Undying (Rite kills restore a hemocraft die of HP — directly offsets the HP
  economy), Celestial (spend Blood Maledict to heal), Genie (spend Blood Maledict to fly for INT-mod
  turns), Undead (reaction: Necrotic Resistance), Archfey (Rite damage reveals invisible targets),
  Great Old One (crits Frighten in an area), Fiend (reroll 1s and 2s on Rite of the Flame),
  Fathomless (Rite hits slow by 3 m).
- **Duo relevance:** the only Order that adds a caster axis, and the only one that touches the
  duo's real gap — no third body means no dedicated controller. Short-rest slots make it cheap to
  run. **Brand of the Sapping Scar at 11 is the best single boss-fight feature in the class**: blanket
  Disadvantage on saves, delivered by a free interrupt, is exactly what a two-person party needs to
  make its one control spell land. Two caveats: it needs a real Intelligence investment to be worth
  it (spell DCs, unlike most Blood Curses, do matter here), and the spell ceiling of level 4 means
  it never becomes a primary caster.

---

## Dip value

Blood Hunter is an unusually good dip, and Listo's feat cadence (3/6/9/12/15/18, keyed to *class*
level — see `listo-10.2-feats.md`) makes a 3-level dip **feat-neutral**.

- **1 level** — Light + Medium armour, **Shields**, **Martial weapons**, 1 skill, Hunter's Bane, and
  **2 short-rest Blood Curses**. Because most curses have no saving throw, a caster or a
  low-Intelligence martial gets nearly full value from Marked, Bloated Agony, Eyeless, Exposure,
  Fallen Puppet and Anxious. **Gains no saving-throw proficiencies** — the multiclass entry omits
  them, so only take Blood Hunter at level 1 if you want INT+DEX saves.
- **2 levels** — adds a Fighting Style and **Crimson Rite**: a permanent-until-long-rest 1d4 elemental
  rider on a weapon for a one-time 1d4 self-hit and a bonus action. For any martial this is close to
  free damage.
- **3 levels** — adds an Order. Feat-neutral. Ghostslayer gives Rite of the Dawn (a 4th, Radiant rite
  with Necrotic Resistance) and a 4th Blood Maledict for three levels — the highest-value 3-level dip
  in the class. Lycan 3 hands a non-Monk character a real unarmed package that scales off DEX.
- **5 levels** — Extra Attack; redundant if the base class already has it.
- **6 levels** — Brand of Castigation. Probably not worth it as a dip; the Brand only becomes strong
  at 11–13 when the Order upgrade and Tethering land.

**As a base class**, the payoff levels are 10 (Dark Augmentation adding INT to STR/DEX/CON saves is a
large, permanent defensive swing), 11 (Order brand upgrade), 13 (Tethering) and 20 (Sanguine Mastery,
which is both a damage floor and a Blood Maledict engine on crits). Level 11 and 15 are empty on the
base table — if you plan to multiclass out, those are the cheapest levels to skip.

**Ability priority:** DEX primary, then **INT** — Intelligence is not a dump stat here. It drives
Brand of Castigation retaliation damage, Dark Augmentation's save bonus (levels 10+), Aether Walk
duration, and the DCs of Binding / Howl / amplified Muddled Mind and Profane Soul spells. CON third.
STR and CHA are dumpable except on a Lycan who is not using DEX-scaled strikes.

---

## Not present / known issues

Read out of the shipped pak; all of these are real defects in the version Listo ships.

1. **`HardenedSoul` is dead code.** The passive (Advantage on saves vs Charmed and Frightened — the
   tabletop level-14 Blood Hunter feature) is defined in `Passive.txt` and has an icon, but **no
   progression node in the entire mod grants it**. It is unobtainable. Do not plan around it.
2. **Base-class levels 11 and 15 are empty.** Only the Order gives anything at those levels.
3. **Native ASI levels are 4/8/12/16/19**, which is the vanilla cadence, not Listo's 3/6/9/12/15/18.
   Listo's cadence comes from `Universal Feat Every X Level(s) - MCM` (`13193`), whose manifest
   description explicitly claims it "should work for every class and subclass, custom/modded or
   vanilla." Whether it *replaces* or *stacks with* the mod's native entries in 10.2 is
   `(unverified)` — worth checking in-game at Blood Hunter 3 and 4 before committing to a plan that
   depends on feat count.
4. **No Constitution save proficiency** and no Order grants one. Blood Hunter has no native
   Concentration insurance; if a build leans on Profane Soul concentration spells, budget a
   Resilient (Constitution) feat (`listo-10.2-feats.md:323`).
5. **Crimson Rite requires a `Dippable` weapon.** `RequirementConditions` on the Rite spells is
   `not Unarmed() and WieldingWeapon('Dippable')`. Which of Listo's many added and reworked weapons
   (see `listo-10.2-equipment.md`) carry that flag is `(unverified)` — a Blood Hunter can be handed a
   best-in-slot weapon that cannot take a Rite at all. Verify on any weapon you plan a build around.
6. **`Shout_MutagenI_mpermeable` typo** in the level-11 Mutagens spell list (`SpellLists.lsx`, list
   `f5c34205-…`); the correct id is `Shout_Mutagen_Impermeable`. The **Impermeable mutagen is likely
   unpickable at the level 11, 15 and 18 Mutant selections** (it is fine at 3 and 7). `(unverified
   in-game)`.
7. **`Target_Target_BloodCurse_FallenPuppet_Container` typo** in `DefaultValues/Spells.lsx` — the
   auto-suggested curse default is broken. Harmless; you pick curses manually.
8. **Blood Curse of the Soul Eater's tooltip is wrong** — the container description is copy-pasted
   from Blood Curse of the Exorcist ("free its mind and make them immune"), while the passive and the
   spell itself are an on-death life-siphon reaction. Text bug, not a mechanical one.
9. **`WPN_BloodHunter_Longsword`** — a Versatile, **Finesse**, Dippable longsword with its own root
   template — exists in the pak but is **not** in `EQP_CC_BloodHunter`, which hands out two
   shortswords and a light crossbow instead. Press coverage of the mod (ScreenRant) describes a
   finesse longsword as the class's starting weapon, so it appears to have been moved or dropped in
   this build. Where, if anywhere, it is obtainable in 10.2 is `(unverified)`.
10. **Fighting Style list is hard-coded to five vanilla styles.** Any fighting styles Listo adds
    elsewhere will not appear on the Blood Hunter's level-2 pick.
11. **Order of the Lycan's Bloodlust has no opt-out before level 15.** There is a `ShapechangeHybrid`
    toggle, but it only controls whether you visually become a full werewolf; it does not disable the
    save.
12. Assorted display-name typos in the shipped English localisation (e.g. "Mystic **Frency**").
    Cosmetic.

---

## Cross-references

- Feat cadence, the removed ability-score cap, Resilient, Tough, Savage Attacker, Dual Wielder,
  Mobile: `data/listo-10.2-feats.md`
- Attunement/rarity limits, the poison package (relevant to Mutant's Strange Metabolism), weapon
  reworks (relevant to the `Dippable` question): `data/listo-10.2-equipment.md`
- Healing-potion nerf, camp-supply cost of long rests, economy: `data/docs/4-SpellsFeatsClassesItems.md`
  and `data/docs/3-GameBalance.md`
