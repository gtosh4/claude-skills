# Listonomicon 10.2 — Barbarian

Barbarian in Listo is the vanilla Patch 8 class — d12 hit die, Rage, Unarmoured Defence, four
base-game subclasses — with the rough edges filed off by **Goon's Barbarian Overhaul** (`17654`),
Reckless Attack converted from a reaction to a hotbar toggle by **5e Reckless Attack** (`10924`),
and the level 13–20 progression supplied by **Expansion** (`279`). The class itself is not
rebalanced; the changes are almost entirely bug fixes, RAW corrections and quality-of-life. What
*is* dramatically different is subclass count: **14 subclasses are selectable** (4 base-game plus
10 from mods), where vanilla offers 4. The single most consequential mechanical change for play
is that **Rage can now be entered outside of combat and ending it is free** (no Bonus Action).
The single most important thing that did *not* change: **Rage charges still refresh only on a
Long Rest.** Grep this file; don't read it whole.

```bash
S=~/.claude/skills/listo-build     # or the plugin path

grep -i -A12 "^### Path of the Zealot" "$S/data/classes/barbarian.md"   # one subclass
grep -i "Duo relevance" "$S/data/classes/barbarian.md"                  # scan all verdicts
grep -i -A20 "^## Dip value" "$S/data/classes/barbarian.md"
grep -i -A20 "^## Not present" "$S/data/classes/barbarian.md"
```

**Provenance.** Compiled 17 August 2026. Every mod named here was confirmed present in
`listo-10.2-mods.tsv` by ModID, and the archive Listo actually pulled was read out of
`listo-10.2-manifest.json`. Vanilla baselines come from bg3.wiki. Mechanics come from mod pages
and their implementation articles, which describe each mod's **current** version — where Listo
pulled an older archive that is called out explicitly. Marked `(unverified)` where not confirmed.

---

## At a glance

| | |
|---|---|
| **Primary ability** | **Strength** (attack/damage). **Constitution** is co-primary — it drives HP, Unarmoured Defence AC, *and* the save DC of most modded subclass features (Ginnungagap, Lightning Vessel, Beast, Storm Herald all key off CON). |
| **Saves at level 1** | **Strength + Constitution.** Only granted if Barbarian is your **level 1** class. |
| **Armour** | Light, Medium, **Shields**. No heavy armour (except Revenant, which grants it at 3). Fast Movement and Unarmoured Defence both switch off in heavy armour. |
| **Weapons** | Simple + Martial. |
| **Multiclass-in proficiencies** | Simple + Martial weapons and **Shields only** — *no* armour proficiency is granted by a Barbarian multiclass dip. |
| **Hit points** | 12 + CON at level 1; 7 + CON per level. Highest in the game. |
| **Skills at level 1** | Choose 2 from Animal Handling, Athletics, Intimidation, Nature, Survival, Perception. |
| **Resource cadence** | **Rage charges: 2 / 3 (L3) / 4 (L6) / 5 (L12). Long rest only.** Nothing in Listo moves them to short rest. Count at 17+ `(unverified)`; at **20** Expansion gives you a Rage charge back **every turn** (effectively unlimited). |
| **What Rage does** | +2 damage on melee / improvised / **thrown** attacks (**+3 at L9, +4 at L16** via Expansion — Goon's `17654` is what makes the L16 step apply to *throws*), **Resistance to physical damage**, **Advantage on Strength checks and Strength saves**. Subclasses replace this with their own Rage variant. |
| **Short-rest resources** | Only **Relentless Rage** (L11, 1/short rest, survive a drop to 0 HP). Two subclasses add short-rest cadence: Beast's Bestial Soul (L6) and Ancestral Guardian's Consult the Spirits (L10). |
| **Key breakpoints** | **1** STR/CON saves + Rage + Unarmoured Defence · **2** Reckless Attack (toggle) + Danger Sense · **3** subclass + 3rd Rage · **5** Extra Attack + Fast Movement · **6** subclass feature + 4th Rage · **7** Feral Instinct (+3 Initiative, cannot be Surprised) · **9** Brutal Critical · **10** subclass feature · **11** Relentless Rage · **13/17** Brutal Critical +1 die each (Expansion) · **14** capstone subclass feature (Expansion) · **18** Indomitable Might · **20** Primal Champion (+4 STR/CON, cap 24) + unlimited Rage |
| **Worth a dip?** | **Yes, at 1 or 2.** A level-1 dip is the cheapest STR+CON save package in the game and hands a d12 hit die plus shield proficiency. A **2**-level dip adds toggled Reckless Attack (which in Listo works on **thrown** attacks too) and Danger Sense. **3** buys a subclass and is feat-neutral, but few subclasses pay off at 3 alone — Zealot and Revenant are the exceptions. Past 3 the class wants to be your main. |

---

## Class changes from vanilla

### Goon's Barbarian Overhaul (`17654`)
- **File pulled:** `Goon's Barbarian Overhaul-17654-1-1-3-6-1778076347.zip` (**v1.1.3.6**).
  ⚠️ The Nexus description page documents **v1.2.0.0**, which Listo did **not** pull — 1.2.0.0
  requires Goon's Library 4.14.1.0 and Listo ships `Goon's Library 12834 4.9.0.0`. The
  Aspect-of-the-Beast fixes below (Crocodile surfaces, Honey Badger 50%, Stallion/Dash,
  Tiger, Wolverine hit-only) are **1.2.0.0 content and are therefore NOT in Listo's build.**
  Treat them as absent.

**Present in 1.1.3.6 (verified against Goon's own changelog):**

| Feature | Change |
|---|---|
| **Rage** | **You can Rage outside of combat.** |
| **Rage** | **End Rage no longer costs a Bonus Action** — it is a free cast. |
| **Rage** | Thrown-attack Rage damage now scales to **+4 at level 16** (Expansion covered melee but not throws). |
| **Rage** | Fall damage is no longer *quartered* by Bludgeoning resistance stacking with halved fall damage. |
| **Rage** | Sustaining Rage no longer works by targeting hostiles with non-attack, non-harmful actions. |
| **Rage** | A level 9+ Barbarian can no longer re-apply the same Rage while already Raging. |
| **Rage** | All Rages check for Expansion's **Persistent Rage** before removing the condition, so Rage does not drop the instant combat ends. (Goon's description calls Persistent Rage a *level 15* feature; his changelog calls it *level 14*. Expansion's own feature article lists neither — **exact level unverified**.) |
| **Reckless Attack** | Now works with **all melee and thrown attacks**; usable under non-hostile Polymorph; usable while **Invisible**. Natively compatible with `10924`. |
| **Danger Sense** | Now triggers off the full **Blinded** and **Incapacitated** status groups, not just the two literal conditions. Description corrected: it is **plain Advantage on Dexterity saving throws**, not limited to traps/spells/surfaces. |
| **Brutal Critical** | Now rolls the extra dice for **offhand** and **thrown** critical hits. |
| **Rage: Bear Heart** (Wildheart) | Physical damage resistance is **no longer granted while wearing Heavy Armour**. |
| **Bestial Heart actions** (Wildheart) | Converted from conditional actions into temporary spells unlocked by the Rage condition. |
| **Primal Stampede** (Wildheart) | Deals real **unarmed damage** instead of a flat 1d4; no longer evadable via Evasion / Shield Master: Block. |
| **Tiger's Bloodlust** (Wildheart) | Now executes weapon functors, so **damage riders on your weapon apply**. Tooltip fixed. |
| **Inciting Howl** (Wildheart) | No longer stacks with itself. |
| **Boot of the Giants** (Giant, L5) | Push trajectory can be aimed with the cursor; takes priority over the normal Shove keybind; combat-log DC display fixed. |
| **Wild Magic: Bolt of Light / Dark Tendrils** | Save DC now **scales off the Barbarian's Constitution** instead of a hardcoded DC 12. |
| **Wild Magic: Teleport** | No longer applies to every entity within 18 m. |
| **Wild Magic: Protective Lights** | No longer stripped when a level 9+ Wild Magic Barbarian gains a Rage condition. |
| **Unstable Backlash** (Wild Magic, L10) | Usable under non-hostile Polymorph. |
| **Magic Awareness** (Wild Magic, L3) | Now adds your **Proficiency Bonus to saves against spells** instead of 1d4 to all saves. Aura no longer applies to hostiles; lasts until the **end** of your next turn; stops spamming the combat log. |

> The Wild Magic DC fix is the sleeper here: it turns Bolt of Light and Dark Tendrils from
> flat-DC-12 jokes into scaling CON-based control at level 20.

### 5e Reckless Attack (`10924`)
- **File pulled:** `RecklessAttack5e_NoVFX.zip-10924-1-0-2-1-1731431052.zip` (**v1.0.2.1**, the
  **No-VFX** variant — no red glow while the toggle is on). Current on Nexus.
- Reckless Attack becomes a **hotbar toggle**, not a reaction. You declare it *before* your first
  attack of the turn and it locks in once you swing — you can no longer swing, see the miss, and
  then retroactively invoke it. Unarmed strikes count as melee weapon attacks. The advantage you
  grant enemies and the advantage you gain have **different durations** (RAW).
- Confirmed by the Listo docs (`4-SpellsFeatsClassesItems.md`, Barbarian section) as the one
  class change the wiki bothers to name.

### Expansion (`279`) — level 13–20
- **File pulled:** `Expansion-279-1-7-3-6-1780876532.zip`. This is the **full** mod (the TSV name
  "Expansion (Bladesinger Only)" is the Nexus page title, not the file variant) — its manifest
  description confirms Tasha's optional class features and 13–20 progressions.
- Barbarian gains: **Brutal Critical** 13th and 17th level parts (2 and 3 extra dice),
  **Indomitable Might** (18th — implemented as *reroll a Strength check twice, take the highest*,
  which stacks with Advantage rather than the RAW score-floor), **Primal Champion** (20th: +4 STR
  and +4 CON, maximum raised to **24**, and you regain a Rage charge **every turn**).
- **Optional (Tasha's) features, configurable in MCM:** **Primal Knowledge** (an extra Barbarian
  skill proficiency at 3rd *and* 10th level) and **Instinctive Pounce** (7th — move half your
  speed as part of the Bonus Action you spend to Rage). Primal Knowledge at 3rd level requires
  Improved UI, which Listo ships (`ImpUI_P8_Fork`). **Whether Listo enables these in its shipped
  MCM config is `(unverified)`** — check in-game under Expansion's Barbarian settings.
- Base-subclass 14th-level capstones supplied by Expansion: **Berserker → Retaliation**
  (reaction melee attack when damaged by a creature within 5 ft), **Giant → Demiurgic Colossus**
  (reach +10 ft, choose Large *or* Huge, Mighty Impel works on Large creatures, Elemental Cleaver
  to 2d6), **Wildheart → Bestial Attunement** (a second totem benefit; Bear = enemies within 5 ft
  have disadvantage attacking anyone else, Eagle = flight while raging, Elk/Tiger/Wolf as RAW),
  **Wild Magic → Controlled Surge** (roll the Wild Magic table twice and pick; doubles matched →
  pick anything).
- Also: an extra **feat at 16th and 19th level** for all classes, per the DnD table.

### Unarmored Defence Synergy (`2837`)
- **File pulled:** `Unarmored Defence Synergy-2837-1-0-1696241804.zip`.
- Adds a third Unarmoured Defence formula, **10 + CON + WIS (no DEX)**, available once you have
  *both* the Monk and Barbarian Unarmoured Defence features. The game auto-picks the best of the
  three. It does **not** stack DEX+WIS+CON. Already documented in `listo-10.2-feats.md` — see
  that file, don't restate it here.

### Wild Magic tables (Wild Magic Barbarian only)
Per `4-SpellsFeatsClassesItems.md` and `1-Home.md`, the shared wild magic pool is **220+ effects**
across several mods and it feeds **both** Wild Magic Sorcerers and Wild Magic Barbarians:

| Mod | ID | File pulled |
|---|---|---|
| More Wild Magic effects | `2022` | `MoreWildMagic 1.3.2-2022-1-3-2-...zip` |
| Wild Magic D100 Table | `2967` | `Wild Magic D100-2967-1-1-0-...zip` |
| Goon d100 Wild Magic (TSV lists this ID as "Listonomicon Again") | `15237` | `Goon d100 Wild Magic-15237-4-1-...zip` |
| Homebrew Wild Magic (for Sorcerer and Barbarian) | `20299` | `Homebrew Wild Magic (...)-20299-1-0-4-...zip` (**v1.0.4**, current) |

- **`20299` adds 30 new effects, most of which are Barbarian-eligible** (a few are spell-gated and
  Sorcerer-only). It overwrites nothing vanilla. Listo does **not** ship its optional Playtest file.
- **Increasingly Likely Wild Magic Surge (`9603`) is a Sorcerer mechanic** (+5% surge risk per
  spell cast in combat) — it does not gate the Barbarian, whose surge fires on Rage.
- ⚠️ **Historical caveat:** Listo v3.6 *removed* a patch that had grafted the full Sorcerer wild
  magic table onto Barbarians, on the explicit reasoning that a Barbarian is forced to roll (Rage
  is their core mechanic) whereas a Sorcerer can play around it — "being turned into cheese
  wheels" was cited. The current tables are the general-purpose ones above, which the docs still
  describe as shared. Assume the Barbarian pool is large but **less punishing than the Sorcerer's**.

---

## Subclasses

**14 selectable.** 4 base-game (Patch 8) + 6 from the `15141` pack + 3 standalone + 1 from the DTO
pack. Base-game subclass features land at 3/5/6/8/9/10 (uneven per subclass) plus a 14th-level
capstone from Expansion; every modded subclass here uses the clean **3 / 6 / 10 / 14** cadence.

### Base game (Patch 8) — Berserker
- **Mod:** none (vanilla). Listo touches it only through `17654` and `279`.
- **Mechanics:** L3 Frenzy + Frenzied Strike · L6 Mindless Rage · L10 Intimidating Presence ·
  **L14 Retaliation** (Expansion): reaction melee attack against any creature within 5 ft that
  damages you.
- **Duo relevance:** Retaliation is a *free extra attack per round* off a resource Lone Wolf
  already doubled (you get an extra Reaction). Strong late; the L3–L10 kit is the weakest of the
  base four.

### Base game (Patch 8) — Path of the Giant
- **Mod:** none (vanilla — this shipped with Patch 8; the old standalone Nexus mod Listo used to
  carry is gone and unneeded).
- **Mechanics:** L3 Giant's Rage + Vaprak's Greed + free **Thaumaturgy** · L5 **Boot of the
  Giants** (Goon's fixes the DC display and lets you aim the push) · L6 Elemental Cleaver ·
  L10 Mighty Impel · **L14 Demiurgic Colossus** (Expansion): reach +10 ft, become Large **or
  Huge** by toggle, Mighty Impel affects Large creatures, Elemental Cleaver → 2d6. Expansion also
  doubles Rage's **throw** damage bonus for Giant at 14 (→ +8 at 16).
- **Duo relevance:** the throwing build. With Goon's throw fixes (Reckless Attack applies to
  thrown attacks, Brutal Critical rolls on thrown crits, Rage throw bonus scales to +4/+8) this is
  the best-supported Barbarian damage line in Listo. Huge size at 14 also solves reach in a duo
  where you cannot body-block with four allies.

### Base game (Patch 8) — Path of Wild Magic
- **Mod:** none (vanilla), but heavily modified — see the Wild Magic table section above and
  Goon's DC/Teleport/Protective-Lights fixes.
- **Mechanics:** L3 Rage: Wild Magic + **Magic Awareness** (Goon's: adds **Proficiency Bonus to
  saves vs spells**) · L6 Bolstering Magic (Boon / L1 slot / L2 slot) · L9 Bolstering Magic: L3
  slot · L10 Unstable Backlash · **L14 Controlled Surge** (Expansion): roll twice, choose.
- **Duo relevance:** **Bolstering Magic is the standout in a two-player run** — you hand your
  partner a free spell slot or a d3 attack/check bonus every rest cycle, which is exactly the kind
  of cross-character economy a duo lacks. Magic Awareness with Goon's fix is a real party-wide
  anti-caster aura. Controlled Surge at 14 removes most of the downside variance. Note that the
  wild magic pool is large and *some* effects are penalising.

### Base game (Patch 8) — Wildheart
- **Mod:** none (vanilla). Listo's Goon's Overhaul does more work here than on any other subclass:
  Bear Heart resistance now disabled in Heavy Armour, Bestial Heart actions rebuilt as temporary
  spells, Primal Stampede deals real unarmed damage and is no longer Evasion-dodgeable, Tiger's
  Bloodlust applies weapon damage riders, Inciting Howl no longer self-stacks.
- **Mechanics:** L3 choose a **Bestial Heart** + free **Speak with Animals** · L6 choose an Animal
  Aspect · L8 Land's Stride: Difficult Terrain · L10 second Animal Aspect · **L14 Bestial
  Attunement** (Expansion): a third totem benefit — **Eagle grants flight while raging**, Bear
  makes enemies within 5 ft attack you at disadvantage against everyone else.
- **Duo relevance:** Bear Attunement at 14 is a genuine taunt, which is how you protect the
  squishier half of a two-person party. Eagle flight solves positioning. Note the Goon's
  Aspect-of-the-Beast **bug fixes for Crocodile / Honey Badger / Stallion / Tiger / Wolverine are
  in v1.2.0.0, which Listo did not pull** — those aspects are still buggy in this build.

### Path of the Ancestral Guardian
- **Mod:** 5e Barbarian Subclasses Combined (`15141`)
- **File pulled:** `BarbarianSubclasses5eCombined.zip-15141-1-1-9-1763335722.zip` (**v1.1.9**,
  current on Nexus). Pack requires Community Library (`1333`) and Compatibility Framework (`1933`),
  both present. Uses Script Extender for accuracy.
- **Mechanics:** **L3 Ancestral Protectors** — while raging, the first creature you hit each turn
  has **disadvantage on attacks not aimed at you**, and any creature it *does* hit takes only half
  damage (resistance). RAW. · **L6 Spirit Shield** — reaction, reduce damage to an ally within
  30 ft by **2d6**, rising to 3d6 at 10 and 4d6 at 14. RAW. · **L10 Consult the Spirits** —
  Augury/Clairvoyance are useless in BG3, so replaced with an Ancestral-Spirit reskin of the 5e
  **Arcane Eye** spell, **1/short or long rest** (5e Spells not required). · **L14 Vengeful
  Ancestors** — the attacker takes force damage equal to what Spirit Shield prevented. RAW.
- **Duo relevance:** **the strongest defensive pick in the list for this run.** Spirit Shield is a
  reaction that protects the *other* character, and Lone Wolf gives you a spare Reaction to spend
  on it. Ancestral Protectors is a taunt-with-teeth: it both redirects fire onto the durable body
  and halves what leaks through. Losing either character ends fights — this subclass is built to
  prevent exactly that.

### Path of the Battlerager
- **Mod:** 5e Barbarian Subclasses Combined (`15141`) — same archive as above.
- **Mechanics:** Dwarf-only in RAW; **the restriction is not implemented**, any race can take it.
  **L3 Battlerager Armor** — while **wearing medium metal armour** and raging, Bonus Action for a
  1d4 piercing armour-spike melee attack using STR (it counts as a weapon attack and **inherits
  your mainhand's attack bonus**). The grapple-damage half of the feature needs **Grappling
  Framework, which Listo does NOT ship** — it falls back to dealing the 3 piercing on a **Throw**
  instead. · **L6 Reckless Abandon** — using Reckless Attack while raging grants temp HP equal to
  your CON modifier (min 1). · **L10 Battlerager Charge** — Dash as a Bonus Action while raging. ·
  **L14 Spiked Retribution** — 3 piercing to any creature within 5 ft that hits you in melee.
- **Duo relevance:** weak. Reckless Abandon is a trickle of temp HP and the L14 retaliation is a
  flat 3 damage. The Bonus Action spike attack competes with everything else you want your Bonus
  Action for, and it locks you into medium metal armour — giving up Unarmoured Defence. Skip
  unless you specifically want the medium-armour frame.

### Path of the Beast
- **Mod:** 5e Barbarian Subclasses Combined (`15141`) — same archive.
- **Mechanics:** **L3 Form of the Beast** — pick one natural weapon each time you Rage.
  **Bite** 1d8 piercing, heals you for your Proficiency Bonus once per turn when you damage a
  creature *and you are below half HP*. **Claws** 1d6 slashing, one **extra claw attack** per
  Attack action — requires an **empty hand in both weapon sets** or it won't appear on the hotbar.
  **Tail** 1d8 piercing with **reach**, plus a **reaction: roll a d8 and add it to AC** against an
  attack from within 10 ft. Natural weapons inherit your mainhand's attack bonus. · **L6 Bestial
  Soul** — natural weapons count as magical; pick one of Swim / Climb / Jump on **each short or
  long rest** (BG3 versions: faster in water; Dash through difficult terrain unslowed; longer
  jumps). · **L10 Infectious Fury** — on hitting with a natural weapon while raging, target makes
  a **WIS save (DC 8 + CON + PB)** or you choose: it **uses its reaction to attack another creature
  of your choice**, or takes **2d12 psychic**. Uses = Proficiency Bonus, long rest. · **L14 Call
  the Hunt** — on Rage, up to CON-modifier willing allies gain **+1d6 damage once per turn**; you
  gain **5 temp HP each**. Uses = Proficiency Bonus, long rest.
- **Duo relevance:** **the standout offensive pick for a duo.** Call the Hunt with a two-person
  party gives your partner a permanent +1d6 per turn for the whole rage — and because you only
  have one ally, the temp HP is small but the buff lands where it matters. Infectious Fury's
  "attack an ally" mode is a free extra action stolen from the enemy side, which directly attacks
  the action-economy problem. Claws' extra attack is real DPS but forbids shields and dual-wield,
  which fights the AC you want in a duo. Note the caveat: **an extra Action from Haste starts a new
  Attack action and forfeits the bonus claw attack.**

### Path of the Juggernaut (Critical Role)
- **Mod:** 5e Barbarian Subclasses Combined (`15141`) — same archive.
- **Note:** Listo **removed** the old standalone "Path of the Juggernot" mod in v3.6, reasoning it
  only added grappling and "Listo doesn't use grappling". It came back later as part of Sumra's
  combined pack, and the pack's Juggernaut has **no grapple dependency**. It is present and
  selectable.
- **Mechanics:** **L3 Thunderous Blows** — on a melee hit while raging, **push the target 5 ft**
  (10 ft from level 10); Huge or larger get a STR save at DC 8 + PB + STR. Toggleable off. ·
  **L3 Spirit of the Mountain** — while raging you cannot be knocked **prone** or **moved against
  your will**. · **L6 Demolishing Might** — +1d8 vs constructs, double damage to objects and
  structures. · **L6 Resolute Stance** — a toggle checked at the start of your turn: **attacks
  against you have disadvantage**, you can't be grappled, but **your own attacks have disadvantage**.
  Once you act, it locks in for the turn. · **L10 Hurricane Strike** — reaction after pushing a
  creature 5+ ft: **leap next to it for free** (no movement cost, no opportunity attacks) and it
  makes a STR save or falls **prone**; and any ally within 5 ft of where you pushed it can react
  with a **melee attack**. · **L14 Unstoppable** — while raging, speed can't be reduced and you
  are **immune to Frightened, Paralysed, Prone and Stunned**; if you are hit by one of those, your
  Rage auto-triggers to clear it (Listo/mod toggle, combat only).
- **Duo relevance:** very good, for an unusual reason. **Resolute Stance is the best single-toggle
  survivability tool any Barbarian subclass has** — imposing disadvantage on every attack against
  you, on demand, is how one of two characters tanks an encounter tuned for five. The
  attack-disadvantage cost matters much less when the *other* player is your damage. Hurricane
  Strike also grants your partner a free reaction attack, i.e. it manufactures action economy.
  Unstoppable at 14 is a hard answer to the Stun/Prone lockouts that would otherwise be lethal.

### Path of the Storm Herald
- **Mod:** 5e Barbarian Subclasses Combined (`15141`) — same archive.
- **Mechanics:** **L3 Storm Aura** — 10 ft aura while raging, re-triggerable as a **Bonus Action
  each turn**; pick Desert / Sea / Tundra, changeable on level-up. DC = 8 + PB + **CON**.
  **Desert**: 2 fire damage to all other creatures in the aura → 3 at L5, 4 at L10, 5 at L15,
  **6 at L20**. **Sea**: one creature makes a DEX save for **1d6 lightning** → 2d6 at L10, 3d6 at
  L15, **4d6 at L20** (to trigger it, target an *enemy* with your Rage; target yourself to skip). 
  **Tundra**: **2 temp HP to each creature of your choice** in the aura → 3/4/5/6 on the same
  ladder. · **L6 Storm Soul** — Desert: fire resistance + Burning immunity + ignite an object or
  your own weapon. Sea: lightning resistance + Shocked immunity + faster in water. Tundra: cold
  resistance + freeze a wet surface. · **L10 Shielding Storm** — **every ally in your aura gains
  your Storm Soul resistance.** RAW. · **L14 Raging Storm** — Desert: reaction, fire damage equal
  to half your Barbarian level when a creature in the aura hits you. Sea: reaction, STR save or
  **prone** when you hit a creature in the aura. Tundra: on each aura activation, one creature
  makes a STR save or its **speed drops to 0** (must be cast immediately after Rage, before you
  move or act).
- **Duo relevance:** **Tundra is the duo pick.** Temp HP to your partner every single turn as a
  Bonus Action, scaling to 6/turn at 20, plus cold resistance shared at 10 — that is a sustained
  mitigation stream that costs no rest resource at all, which is exactly what a party that can't
  afford 120-supply long rests needs. Shielding Storm turning one resistance into a party-wide
  resistance is worth more with two bodies than five, since both of you are always in the 10 ft
  aura. Desert/Sea are damage options and are fine, but Tundra solves the actual problem.

### Path of the Zealot
- **Mod:** 5e Barbarian Subclasses Combined (`15141`) — same archive.
- **Mechanics:** **L3 Divine Fury** — while raging, the first creature you hit each turn takes
  **+1d6 + half your Barbarian level** in **necrotic or radiant** (chosen at L3). You also pick a
  **Deity**, which applies both the God tag and the Paladin_God tag ("Unaligned" available). ·
  **L3 Warrior of the Gods** — reimplemented for BG3: when the Zealot is downed or dead, **any
  nearby party member can revive them without consuming a Revivify scroll** (watch for the hotbar
  unlock). · **L6 Fanatical Focus** — **reroll one failed saving throw per Rage** while raging. ·
  **L10 Zealous Presence** — Bonus Action, up to ten creatures within 60 ft gain **advantage on
  attack rolls AND saving throws** until the start of your next turn. **1/long rest.** ·
  **L14 Rage Beyond Death** — while raging, dropping to **1 HP** (the mod's substitute for 0)
  doesn't knock you out; you still make death saves, but you **cannot die until your Rage ends**.
- **Duo relevance:** **the best level-3 dip in this file, and the best "don't lose a character"
  insurance in the class.** Divine Fury at 3 is roughly +1d6+1 per turn immediately and scales with
  *Barbarian* level, so it rewards going deep rather than dipping. Warrior of the Gods directly
  attacks the run's failure mode — your partner can pick you up without spending a scroll.
  Fanatical Focus is a save reroll *every Rage*, not per rest, which is enormous in a duo with
  narrow save coverage. Rage Beyond Death at 14 makes the Zealot functionally unkillable inside a
  Rage. Note **Zealous Presence is 1/long rest** — with 120+ supply long rests, treat it as a
  once-per-boss button.

### Path of Ginnungagap
- **Mod:** Path of Ginnungagap - Barbarian Subclass (`20482`)
- **File pulled:** `Ginnungagap Barbarian-20482-1-0-1-1770141353.zip` (**v1.0.1** — the only
  version on Nexus, so current). Adapted from Dreamfarers' homebrew. Added in Listo per changelog.
- **Mechanics:** **L3 Null Warrior** — while raging, **Advantage on saving throws against spells
  and magical effects**, and a **reaction to downgrade an incoming Critical Hit to a normal hit**,
  **once per Rage**. RAW. · **L6 Magic Syphoning** — while raging, reaction when a creature within
  **18 m** begins casting: make a **Constitution check vs DC 10 + spell level**. On success the
  spell **fails outright**, and your next weapon hit deals **+2× the spell's level** in damage.
  Refreshes only when you spend a Bonus Action to enter a Rage (and only a *successful*
  interrupt consumes it). · **L10 Spell Eater** — **regain 2d6 HP whenever you succeed a saving
  throw against a spell.** (This replaces the homebrew's Dispel-Magic-like feature; the author
  says the original was too janky for BG3.) · **L14 Herald of Ginnungagap** — while raging, on a
  weapon hit force a **CON save** (DC 8 + PB + CON): failure applies **Slow for 10 turns**;
  success still denies the target **Reactions** until the end of its next turn. Saves again at end
  of each of its turns. Uses = Proficiency Bonus, **long rest**.
- **Duo relevance:** **the dedicated anti-caster.** Listo's `3-GameBalance.md` states that goblins,
  fae, Kuo-toa and similar are now "effectively wild magic sorcerers or warlocks with powerful
  patrons" and that many enemies are wild magic barbarians — this modlist is far more caster-dense
  than vanilla, and a counterspell-on-a-CON-check is a direct answer. Null Warrior's
  once-per-Rage crit denial is a survival card in a run where one character dying ends the fight,
  and Spell Eater turns enemy magic into sustain with no rest cost. Advantage on spell saves
  patches the classic Barbarian hole (WIS/CHA saves).

### Path of the Lightning Vessel
- **Mod:** Path of the Lightning Vessel Barbarian (`21050`)
- **File pulled:** `VesselPath-21050-1-2-2-1779334234.zip` (**v1.2.2**, current on Nexus).
- ⚠️ **Listo applies "CD's nerf patch" on top of this mod** (changelog: "Added Lightning Vessel
  Barbarian, with CD's nerf patch"). That patch is **not a Nexus archive and does not appear in
  the manifest** — it ships inside the Wabbajack. **The numbers below are the unmodified mod's;
  Listo's are lower by an unknown amount. `(unverified)` — confirm in game before building around
  the damage.**
- **Mechanics (pre-nerf, from the mod page):** Vessel DC = 8 + PB + **CON**. **L3 Galvanic Heart**
  — Lightning resistance (or **−1d6** further if you already had it), plus three Bonus Action
  powers usable only while raging: **Electrified Chains** (hits deal **+2× CON mod** lightning
  until end of turn and apply *Ensnared*: the target can't move 10 ft without an Athletics check
  vs your passive Athletics, failure = damage again and speed 0); **Fulgurant Strike** (interrupt,
  once/turn, after a melee hit: **+2× CON mod** lightning to the target and everything within
  5 ft on a failed DEX save — **you have advantage on that save**); **Lightning Step** (move half
  speed; a creature you end within 5 ft of takes **2× CON mod** lightning). · **L6 Roaring Crash**
  — on entering Rage, **leap 30 ft**; 10 ft radius, DEX save or **(CON mod)d8** lightning, half on
  success; a creature in your landing square saves at disadvantage and is pushed out. Available
  only on the turn you Rage. · **L10 Lightning Reflexes** — **+CON mod to all Dexterity checks**
  (min +1); **one free Lightning Step per turn** that costs no Bonus Action; Roaring Crash range
  → 60 ft. · **L14 Electric Beast** — all Galvanic Heart damage goes to **3× CON mod**; Chains
  tighten to 1 ft and deny Reactions on a failed check; Fulgurant Strike radius → 15 ft and
  **allies auto-succeed**; Lightning Step becomes **double full movement** and can be spent as a
  **teleport**.
- **Duo relevance:** heavy Bonus Action competition — all three L3 powers want the same Bonus
  Action, and so does Rage itself. It gets much better at **10**, where the free Lightning Step
  breaks the bottleneck and +CON to DEX checks quietly fixes a Barbarian's lockpicking/trap
  problem in a party with no rogue. Roaring Crash is one of the few gap-closers in the class,
  which matters when two characters have to cover a whole battlefield. **Do not commit to this
  subclass on the strength of the listed numbers until the Listo nerf patch is inspected.**

### Path of the Revenant
- **Mod:** (DTO) Otherworldy Archetypes (`21822`) — a 12-subclass pack; Revenant is its only
  Barbarian entry.
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67 2026-06-17T17-15Z PYJWETtYB.zip`
  (**v1.2.0.67**). Note the author's own site documents only up to **1.2.0.65** — Listo's archive
  is **newer than the published changelog**, so two versions of fixes are undocumented.
- **Mechanics:** **L3 Revenant's Rage** (Bonus Action, Rage charge) — ethereal form:
  **resistance to physical damage AND all incoming damage reduced by 2**; you count as **Undead**
  and gain immunity to **Charm, Fear, Poison and Disease** — but **you cannot be healed by any
  means**, and **you cannot end the rage until combat ends**. **Spellcasting is disabled while
  Revenant's Rage is active** (1.2.0.66-era change), but activating it **no longer breaks
  concentration**. · **L3 Ghost Armor** — **proficiency with Heavy Armour, and you can wear it
  while raging.** · **L6 Unyielding** — in heavy armour while raging you cannot be **moved or
  knocked Prone** by enemy spells or actions. · **L6 Haunt** (Bonus Action, WIS save, 9 m) —
  **Frighten** a target 1 turn; while you stay near it, **all damage you take is mirrored onto it
  as necrotic**. One target at a time, lasts until you retarget, the rage ends, or one of you
  dies; **if the Haunted target dies you may recast Haunt for free.** · **L10 Gravemarch** — each
  time your Haunted foe dies you gain **max HP equal to PB + CON mod** and **grow one size
  category** (further stacks give max HP only); each time Haunt is *saved* against, add your Rage
  modifier to its DC until it lands. · **L14 Wraithwalk** — raging in heavy armour makes you
  **immune to Difficult Terrain and most restraints**.
- **Duo relevance:** the most distinctive and the most dangerous. **Damage reduction 2 stacks
  multiplicatively with Lone Wolf's halved damage and physical resistance** — this is by a wide
  margin the tankiest thing in this file against weapon damage. But **"cannot be healed by any
  means" is a hard incompatibility with the duo's other half being a healer**, and "cannot cease
  your rage until combat ends" removes the option to bail out. Haunt's damage-mirroring is
  effectively free offence bolted onto being hit, and Gravemarch snowballs across a long fight.
  The heavy-armour path also means you never care about DEX or Unarmoured Defence — a genuinely
  different stat spread from every other entry here. Treat healing incompatibility as the deciding
  question with your partner.

---

## Dip value

Assume level cap 20, two characters, Lone Wolf. A 3-level dip is feat-neutral.

**Barbarian 1** — the single best value tier.
- **Strength + Constitution saving throw proficiencies** — but *only* if Barbarian is your level 1
  class. This is the argument for starting Barbarian and multiclassing out, not the reverse.
  STR saves stop the grapples/shoves/prone that separate a two-person party; CON saves protect
  concentration and are the most-called save in the game.
- **d12 hit die**, 12 + CON at level 1, and **+30% HP from Lone Wolf on top**.
- **Rage** (2 charges/long rest): **+2 damage** with melee, improvised and **thrown** weapons,
  **Resistance to physical damage**, and **Advantage on Strength checks *and* Strength saving
  throws** — stacking with the STR save proficiency above. In Listo you can now **enter it out of
  combat** and **end it for free**.
- **Unarmoured Defence** — add your **Constitution modifier** to AC while not wearing armour
  (10 + DEX + CON). Free AC for any build not wearing armour.
- **Simple + martial weapons, light and medium armour, shields.**
- ⚠️ **Dipping *into* Barbarian later grants only weapons and shields — no armour, no saves.**

**Barbarian 2** — the best "one more level".
- **Reckless Attack**, and Listo's version is materially better than vanilla's: a **toggle**
  (`10924`) that Goon's extends to **all melee *and thrown* attacks**, usable while **Invisible**
  and under non-hostile Polymorph. For any STR-based attacker this is near-permanent Advantage.
  The cost — enemies get advantage on you — is much cheaper in a duo where Lone Wolf already
  halves incoming damage and you have HP to burn.
- **Danger Sense**: plain **Advantage on Dexterity saving throws** (Goon's corrected the
  description and expanded its condition coverage). This is your AoE-survival stat.

**Barbarian 3** — feat-neutral, buys a subclass and a third Rage charge.
- Only worth it for subclasses that front-load: **Zealot** (Divine Fury damage + free-revive
  insurance), **Revenant** (heavy armour proficiency + DR 2 at level 3), **Ginnungagap**
  (Advantage on spell saves + crit denial). **Ancestral Guardian, Storm Herald, Beast and
  Juggernaut all have their best features at 6, 10 or 14** — take those as a main class.
- Everything else in the class (Extra Attack at 5, Feral Instinct at 7, Relentless Rage at 11,
  the L14 capstones, Primal Champion at 20) argues for going deep, not dipping.

**Beyond 3:** the class has no dead levels between 5 and 14, and Expansion makes 13–20 real
(Brutal Critical scaling, Indomitable Might, and a Primal Champion capstone worth +4/+4 with a
24 stat cap plus effectively infinite Rage). A Barbarian 17 / X 3 split preserves the level 1 saves
and the L14 subclass capstone.

---

## Not present

Things a BG3 or 5e player would reasonably expect, that this build of Listo does **not** have:

- **Barbarian Quality of Life** — removed (changelog v10.x, item 5). Its functionality is not
  replaced; Goon's Overhaul covers a different set of fixes. Goon's 1.1.3.1 notes it stopped
  overriding this mod.
- **Dynamic Wildheart Barbarian** — removed (changelog v10.x, item 6).
- **Feral Wildheart - Barbarian Subclass Rework** — added in an older version, **not in 10.2**.
  (Goon's Overhaul is explicitly incompatible with it, which is presumably why.)
- **The Rage Mage - A Barbarian Spellcaster Subclass** — Goon's ships compatibility code for it,
  but the mod itself is **not in Listo**. There is no spellcasting Barbarian subclass.
- **Grappling Framework** — not in the list. This costs **Battlerager** the grapple half of
  Battlerager Armor (it falls back to a Throw), and was Listo's stated reason for once cutting
  Juggernaut ("Listo doesn't use grappling").
- **DTO Volume 2: Codex of Might and Magic** — only Volume 1 (`21822`) is installed. The
  Barbarian feature **"Ferocious Attacks" (level 6, choose one; additional at 15)** lives in
  Volume 2 and is therefore **absent**.
- **Goon's Barbarian Overhaul v1.2.0.0** — Listo pulled **1.1.3.6**. The Aspect of the Beast bug
  fixes (Crocodile surface detection, Honey Badger 50%-not-55%, Stallion/Dash refresh, Tiger
  rework, Wolverine hit-only Maimed) are **not in this build**, despite what the Nexus page says.
- **The Berserker Set - On The Edge of Death** — removed (changelog item 17), which also stripped
  a set of Combat Extender passives that had been built on it for enemies.
- **A standalone Path of the Giant mod** — unnecessary; Path of the Giant is a **base-game
  Patch 8 subclass** and is fully present, with Expansion supplying its level 14 capstone.
- **Rage on a short rest.** Nothing in the list moves Rage charges off the long rest. Plan around
  5 charges/long rest until level 20.
- **Standalone individual 5e Barbarian subclass mods** — the author decommissioned them in favour
  of the `15141` combined pack. Do not look for separate Zealot/Storm Herald/Beast mod IDs.

---

## Cross-references

- **Feats** — see `data/listo-10.2-feats.md`. Relevant: the docs call out a **Durable + Mage
  Slayer** frontliner (Cleric/Paladin/**Barbarian**/Fighter) as "very formidable… an essential
  anchor and tank"; Durable in Listo carries **proficiency-bonus-scaling damage resistance** and
  Tough carries **+1 CON**. Great Weapon Master and Sharpshooter were reworked (proficiency bonus
  moves from the attack roll to the damage roll). **Tavern Brawler is significantly weaker.**
  Unarmored Defence Synergy (`2837`) is documented there at line ~612.
- **Equipment** — see `data/listo-10.2-equipment.md`. **Barbarian of our Heart** (`13929`) is
  covered there: two endurance/tanking armour pieces plus an endgame bleed greataxe, distributed
  to **Act 3 vendors** by Listo (the manifest pulled that mod's `New Vendor Locations` file).
  Remember Listo enforces an **attunement and magic-item rarity limit**.
- **Races** — see `data/listo-10.2-races.md`.
