# Listonomicon 10.2 — Feats

Every feat available in the shipped 10.2 list, with what it actually does after Listo's
rebalances. **Grep this file; don't read it whole.**

```bash
S=~/.claude/skills/listo-build     # or the plugin path

grep -i -A6 "^### Great Weapon Master" "$S/data/listo-10.2-feats.md"   # one feat
grep -i "half-feat" "$S/data/listo-10.2-feats.md"                     # everything granting +1
grep -i -B2 -A6 "short rest" "$S/data/listo-10.2-feats.md"            # by mechanic
```

**Provenance.** Compiled 17 August 2026 against the bundled 10.2 snapshot. Every mod named
here was confirmed present in `listo-10.2-mods.tsv`, and every *file variant* noted was
confirmed in `listo-10.2-manifest.json`. Mechanical detail comes from the mod pages on Nexus,
which describe the mod's **current** version — where Listo pulled an older archive, the
version is stated so you can discount accordingly. Anything not verified is marked
`(unverified)`.

---

## Feat cadence

**Read out of the installed `FeatsUni.json`, not from the docs** — the docs version was wrong
in two ways. See `data/listo-10.2-mcm.md` for the raw config.

- **All classes:** feats at **3, 6, 9, 12, 13, 15, 18** — **seven feats**
- **Fighter and Rogue:** additionally at **11** — eight feats

The live values are `featFrequency: 3`, `alwaysGrantFeatAtLevels: {"13": true}`,
`fighterfeat: 11`, `roguefeat: 11`, `multiclassFeatAtLevel1: false`.

Two corrections this forces:

- **The level 13 feat is universal.** Everyone gets seven, not six.
- **`enableAdvancedSettings` is `false`**, so the `advancedCustomClasses` block that would have
  given **Mesmerist and Artificer** an extra feat at 11 **does not apply**. Only Fighter and
  Rogue get the 11. Mesmerist is not on a special cadence.
- `multiclassFeatAtLevel1: false` — a dip grants no feat for its own level 1.

Delivered by `Universal Feat Every X Level(s) - MCM` (`13193`, archive
`Feat Every x Level(s)-13193-5-0-3-1`). It is now the **only** feat source: Expansion's own
selectors are set to `"None"` in `MCM/Expansion/settings.json`, so its native 14/16/19 feats do
not fire. Because the cadence keys off **class level**, a 3-level dip is feat-neutral — you
collect the dip class's own level-3 feat. This is the arithmetic behind the skill's "assume
multiclassing by default" rule.

> A third config copy, `MCM/FeatsUni/FeatsUni.json`, holds `alwaysGrantFeatAtLevels {"20": true}`
> and nothing else. Two of three files agree on 13; whether **20** also grants a feat is
> `(unverified)` — check the level-up screen.

`(Beta) FeatMaker - MCM` (`23113`) is an authoring tool, not a feat source.

---

## The ability-score cap is gone

**This is the single most important fact in this file.**

`Feats Overhaul` (`15044`) removes the **ability score cap of 20** on feat-granted increases.
Half-feats and ASI can push a stat **past 20** without a Tome or Hag's Hair. It does this by
replacing feat ability selectors with passive selectors (implementation credited to Goonsack).

Consequences for build math:

- The "+4 from Lone Wolf is the only cheap route to 20" framing is **too pessimistic**.
  Stacking half-feats is now a real alternative path to 20 and beyond.
- `Enweaved` is capped at **22** by its own mod text — that cap is specific to Enweaved, not
  a global rule.
- `Resilient` can be taken **multiple times** (different abilities each time).
- **Open question — does the uncap reach Essential Feats?** `references/listo-rules.md` states
  the uncap applies to feat increases generally, with the plain **ASI feat as the exception**.
  But Feats Overhaul's own page recommends `Stackable ASI Feats` (patches only) to "remove the
  ability score cap of 20 for all half feats from those mods [Essential Feats, Planescape] **the
  same way this mod does**" — which reads as Essential Feats needing a separate patch, and
  **that patch mod is not in the 10.2 list**.
  `(unresolved — the two sources are in tension; check a character sheet in-game before
  building a plan that depends on an Essential Feats half-feat crossing 20.)`

---

## Build-selection priorities — use this during creation and every respec

This is the recommendation layer for the mechanical catalogue below. **Do not fill seven feat
slots from a fixed tier list.** At every creation/respec rung, first price the feat against a
class level or dip that supplies the same proficiency, then against a half-feat that completes an
odd score, and finally against the other feats in its build-specific package. A temporary Act I
feat is valid: Withers lets the ladder replace it when the chassis or equipment solves its job.

The audit covers every selectable family documented below and is calibrated for this skill's
two-person Lone Wolf run: two Actions, Bonus Actions, and Reactions per character; expensive long
rests; seven feats; and no spare body to rescue a downed character. The strongest candidates are:

| Priority | Feat | Why the builder must test it |
|---|---|---|
| **Default first comparison** | **Skeleton Crew** | A free, scaling third body at the start of **every combat**, with no action, slot, concentration, or rest cost. This is the only near-universal pick and the best direct repair for duo action economy. Reject it only for a deliberate no-summons concept or if its random body is operationally unacceptable. |
| **Default defensive comparison** | **Resilient (Wisdom or Constitution first)** | Repeatable half-feat, uncapped by Feats Overhaul, and the only feat that adds a save proficiency. In a duo, a failed Hold/Fear save can remove half the party; concentration builds also price Constitution. Never choose it before checking the level-1 class and Lone Wolf save grants for duplication. |
| **Default endurance comparison** | **Durable** | +1 CON, full healing on every short rest, and in-combat regeneration below 60%. It converts the cheap clock into effective HP and is particularly strong early, before healing and camp supplies stabilize. |
| **Weapon-build benchmark** | **Weapon Master** | +1 STR/DEX, all weapon proficiencies, a fighting style, and always-on extra weapon damage scaling to +3. This unusually dense package is the baseline that Fighting Initiate, Martial Adept, and a proficiency dip must beat. Do not take it merely for proficiency if the chassis already grants every weapon actually used. |
| **Melee damage benchmark** | **Savage Attacker** | Price it from the **entire eligible melee/unarmed damage packet**, not the weapon die. It becomes premier on smites, melee Sneak Attack, Manoeuvres, Flourishes, coatings, and item-rider stacks; it is modest on mostly-flat or independent damage. |
| **Shield benchmark** | **Shield Master** | Passive Evasion, +2 DEX saves, flat damage reduction, and a bonus-action Shield Blow. It is exceptionally dense for a shield user and uses Lone Wolf's spare bonus action without consuming a reaction. Do not duplicate Rogue Evasion. |
| **Spell-attack benchmark** | **Spell Sniper** | Stacking spell critical threshold reduction, no low-ground penalty, a cantrip, and damage-die advantage on attack-roll spells (first hit only on multi-hit spells). Particularly strong for crit-supported Eldritch Blast/ray builds; not a default for save-based casters. |
| **Melee-caster benchmark** | **War Magic** | A full basic/weapon-action attack as a bonus action after casting from level 5. This is one of the largest repeatable action-economy gains for casters without Extra Attack; carefully compare it on War Cleric, and reject it for Eldritch Knight, Booming Blade plans, or another non-stacking bonus-action grant. |
| **Short-rest caster benchmark** | **Fey Touched** / **Shadow Touched** | A half-feat plus two slot-free casts **per short rest**. Misty Step is the generally useful mobility winner; Invisibility and a level 1/2 illusion or necromancy spell can be stronger for scouting or a specific spell package. Respect the Essential Feats cap caveat. |
| **Skill/face benchmark** | **Actor**, **Dungeon Delver**, or **Skilled Expert** | Actor is four face expertises plus CHA; Dungeon Delver is two high-value expertises, trap defence, and DEX/WIS; Skilled Expert fills any one proficiency/expertise/stat hole. Two characters must cover the campaign, so explicitly compare one of these when the level-1 map misses a gate. |

### Strong packages, not automatic picks

- **Heavy Armour Master + a level-1 heavy-armour source** is a premier anchor package: a
  STR/CON half-feat and reduction of every damage instance by PB (cap 5). Taking **Heavily
  Armoured** first makes it a two-feat package, so always compare a Fighter or Paragon start.
- **Mage Slayer** is broad spell-save advantage plus PB spell-damage reduction, not merely an
  anti-concentration reaction. It is a top defensive choice when encounter/caster pressure is
  the problem; **Tough** is the generic alternative (+1 CON, +2 CON saves, +2 HP/level).
- **Duellist** is exceptional accuracy (PB), crit range, and +1 DEX for a finesse one-hander,
  but the empty off-hand costs a shield. Treat it as a complete offensive style, not a free
  half-feat. **Deadly Alacrity** can extend the crit package but lost its +1 in Listo.
- **Great Weapon Master** remains good because the crit/kill bonus attack is untouched even when
  All In is unattractive. **Polearm Master + Sentinel** is the control/reaction package; Lone
  Wolf's extra reaction raises its ceiling. Verify weapon overlap before adding Shillelagh.
- **Dual Wielder** is a full package here: non-Light dual wielding, +1 AC, and Two-Weapon Fighting
  Style. It becomes much stronger when the build has two worthwhile weapon riders and enough
  bonus actions; it is not automatically better than a shield.
- **Medium Armour Master** is a strong half-feat on an existing medium-armour chassis: +1 AC,
  no Stealth disadvantage, and PB temporary HP every combat. The familiar vanilla 18-DEX plan is
  gone, so value these actual grants instead. **Light Armor Master** and **Mobile** are the more
  aggressive mobility packages; both can impose disadvantage on opportunity attacks, while
  Light Armor Master also completes STR/DEX and Mobile cannot be slowed.
- **Bow Expert** is an excellent DEX half-feat for bow/crossbow users who exploit special arrows
  or fight at close range. **Sharpshooter** is a terrain/accuracy tool first and a toggleable
  damage feat second; price Listo's PB-scaled penalty rather than vanilla −5/+10 lore.
- **Martial Adept** is two short-rest dice, two Manoeuvres, and +1 STR/DEX. This is efficient on
  a martial that needs control/burst and can exploit attached dice, but Weapon Master is the
  competing always-on package.
- **Battle Medic** can preserve an Action after weapon attacks and is a high-value rescue tool in
  a duo. Take it only when the build actually attacks and owns useful healing spells.
- **Telekinetic**, **Dirty Fighting**, **Charger**, and **Thief's Apprentice** turn spare bonus
  actions or movement into repeatable control/tempo. Lone Wolf makes that resource abundant, but
  non-stacking bonus-action grants and an already-crowded hotbar can erase their value.
- **War Caster** is the clean concentration half-feat; compare it directly with Resilient CON.
  Advantage is usually better at low DC, proficiency scales, and only Resilient grants the save
  proficiency. Opportunity Spell matters only when the build can trigger and exploit it.
- **Elemental Adept** is strong for a build committed to one elemental type because ignoring
  resistance preserves its engine. **Poison Adept** needs its equipment passive to downgrade
  immunity and is therefore a gear package, not a standalone general recommendation.
- **Ritual Caster** is an unusually broad utility half-feat in the Listo patch and has small
  short-rest slot recovery. **Magic Initiate** is better when its cantrips and one added slot are
  specifically part of the engine. Neither should be chosen as vague “more spells.”
- **Meta Magic Adept** (3 points, 2 options) and repeatable **Eldritch Adept** can import a
  build-defining class tool without a dip. Compare the small resource pool or invocation against
  what 2–3 class levels return; do not assume the feat automatically wins because dips are cheap
  in feat cadence.
- **Enweaved** is the fastest one-feat route to 22 casting ability, but it deliberately adds two
  wild-magic liabilities in a list with expanded surges. Offer it as a high-variance player
  choice, never silently optimize into it. **Arcane Chaos** belongs only on a sorcery-point/wild
  surge plan where the guaranteed surge and instability reset are desired.
- **Alert** is still the anti-ambush/initiative pick, but here it is PB rather than +5 on a d10
  initiative die. Value Surprise immunity and Perception; do not copy vanilla “always first feat”
  advice.

### Contextual picks and common opportunity costs

These are not forbidden; they need a named reason that beats the packages above.

| Use only when this exact job exists | Feats |
|---|---|
| Complete an odd score or buy a physical perk that the chassis can exploit | **Athlete**, **Mobile**, **Light Armor Master**, **Medium Armour Master** |
| Buy missing armour/shields without a better level-1 start | **Lightly Armoured**, **Moderately Armoured**, **Heavily Armoured** |
| Add a narrow spell/defence package | **Heaven Touched**, **Hell Touched**, **Nimble Fingers**, **Lucky** |
| Add skill/economy breadth after checking overlap | **Skilled**, **Performer**, **Alchemist**, **Thief's Apprentice** |
| Add a fighting style when Weapon Master or a dip is wasteful | **Fighting Initiate** |
| Solve a specific movement/control plan | **Mobile**, **Light Armor Master**, **Muscular**, **Dirty Fighting**, **Telekinetic**, **Charger** |

**Usually dominated without a special interaction:** plain **ASI** after the primary reaches 20
(it cannot cross 20), **Lightly Armoured** merely as a prerequisite for shields, **Muscular**
when Athletics advantage is the whole grant, and **Lucky** when the run cannot afford frequent
long rests. **Tavern Brawler is not the vanilla autopick**: it lost the half-feat and grants only
PB−1 to unarmed/thrown attack and damage. It can still be correct, but the build must show that
math beating Savage Attacker, Weapon Master, or another half-feat at the rung where it is taken.

### Respec checklist

At each planned respec, record these checks in the working notes (the finished sheet needs only
the resulting picks):

1. Remove any feat whose proficiency, Expertise, movement, or save is now duplicated by the new
   level-1 class, race, subclass, equipment, or partner coverage.
2. Recompute the ability spread around the selected half-feats; do not preserve an odd score from
   the previous cut, and do not use plain ASI to plan above 20.
3. Re-price **Skeleton Crew**, the relevant damage benchmark (**Weapon Master**, **Savage
   Attacker**, **Spell Sniper**, or **War Magic**), one endurance feat, and missing Wisdom/CON save
   coverage even if the prior version omitted them.
4. Check clocks and action collisions: long-rest feats in the supply budget; bonus-action and
   reaction feats against both Lone Wolf actions; non-stacking grants called out below.
5. Name why every contextual feat survives. “Good feat” is insufficient; state the interaction,
   missing proficiency, stat breakpoint, or act-specific problem it solves.

---

## Half-feat index

For this reference, **half-feat** means any feat that also increases an ability score. This
includes `Enweaved` even though it grants +2 rather than the usual +1. The table is the complete
shipped roster: **35 feat families / 40 selectable entries** when the six Magic Initiate variants
are counted separately. Ability choices were swept from the installed feat selectors and passive
boosts in `FeatsOverhaul.pak`, `FeatsOverhaul_ListoPatch.pak`, `Essential_Feats.pak`,
`Enweaved.pak`, and the Dirty Fighting pak.

| Feat | Ability increase | Source / important qualification |
|---|---|---|
| **Actor** | +1 CHA | Feats Overhaul |
| **Alchemist** | +1 CON, INT, WIS, or CHA | Essential Feats; subject to its cap caveat above |
| **Athlete** | +1 STR or DEX | Feats Overhaul |
| **Bow Expert** (renamed Crossbow Expert) | +1 DEX | Feats Overhaul |
| **Dirty Fighting** | +1 STR or DEX | Standalone |
| **Duellist** (renamed Defensive Duellist) | +1 DEX | Feats Overhaul |
| **Dungeon Delver** | +1 DEX or WIS | Feats Overhaul |
| **Durable** | +1 CON | Feats Overhaul |
| **Eldritch Adept** | +1 INT, WIS, or CHA | Essential Feats; repeatable; subject to its cap caveat above |
| **Elemental Adept** | +1 INT, WIS, or CHA | Feats Overhaul; each element uses the same ability selector |
| **Enweaved** | **+2 INT, WIS, or CHA** | Standalone; explicit cap of 22 |
| **Fey Touched** | +1 INT, WIS, or CHA | Essential Feats; subject to its cap caveat above |
| **Fighting Initiate** | +1 STR or DEX | Essential Feats; subject to its cap caveat above |
| **Heaven Touched** | +1 INT, WIS, or CHA | Essential Feats; subject to its cap caveat above |
| **Heavily Armoured** | +1 STR or CON | Feats Overhaul; requires medium-armour proficiency |
| **Heavy Armour Master** | +1 STR or CON | Feats Overhaul; requires heavy-armour proficiency |
| **Hell Touched** | +1 INT, WIS, or CHA | Essential Feats; subject to its cap caveat above |
| **Light Armor Master** | +1 STR or DEX | Essential Feats; subject to its cap caveat above |
| **Lightly Armoured** | +1 STR or DEX | Feats Overhaul |
| **Magic Initiate: Bard** | +1 CHA | Feats Overhaul |
| **Magic Initiate: Cleric** | +1 WIS | Feats Overhaul |
| **Magic Initiate: Druid** | +1 WIS | Feats Overhaul |
| **Magic Initiate: Sorcerer** | +1 CHA | Feats Overhaul |
| **Magic Initiate: Warlock** | +1 CHA | Feats Overhaul |
| **Magic Initiate: Wizard** | +1 INT | Feats Overhaul |
| **Martial Adept** | +1 STR or DEX | Feats Overhaul |
| **Medium Armour Master** | +1 STR or DEX | Feats Overhaul; requires medium-armour proficiency |
| **Meta Magic Adept** | +1 INT, WIS, or CHA | Essential Feats; subject to its cap caveat above |
| **Moderately Armoured** | +1 STR or DEX | Feats Overhaul; requires light-armour proficiency |
| **Nimble Fingers** | +1 DEX | Essential Feats; subject to its cap caveat above |
| **Performer** | +1 DEX or CHA | Feats Overhaul |
| **Resilient** | +1 to any ability | Feats Overhaul; repeatable for different abilities |
| **Ritual Caster** | +1 INT, WIS, or CHA | Feats Overhaul |
| **Shadow Touched** | +1 INT, WIS, or CHA | Essential Feats; subject to its cap caveat above |
| **Skilled** | +1 to any ability | Feats Overhaul |
| **Skilled Expert** | +1 to any ability | Essential Feats; subject to its cap caveat above |
| **Telekinetic** | +1 INT, WIS, or CHA | Essential Feats; subject to its cap caveat above |
| **Tough** | +1 CON | Feats Overhaul |
| **War Caster** | +1 INT, WIS, or CHA | Listo patch selects the 2024 version |
| **Weapon Master** | +1 STR or DEX | Feats Overhaul |

**Not half-feats in the shipped setup:** `Deadly Alacrity` has its +1 removed by the Listo
patch, and `Tavern Brawler` has its +1 STR/CON removed by Feats Overhaul. Plain `ASI` is omitted
because increasing abilities is its entire grant rather than an additional half-feat benefit.

---

## Listo-specific patches to feats

`Feats Overhaul` ships with a **`FeatsOverhaul_ListoPatch`** archive (v1.1.3), confirmed
pulled. Its documented changes:

- **Performer:** gold gain is reduced (the base mod makes performing a real income source;
  Listo's harder economy pulls that back).
- **Ritual Caster:** instead of the toggled in-combat free ritual cast, you **learn all** the
  ritual spells from the list you'd otherwise pick 3 from.
- **Essential Feats — Deadly Alacrity:** the **+1 ability score is removed**.
- **War Caster:** the vanilla feat is renamed plain "War Caster" and uses the **2024**
  features; the duplicate is removed, so there is only **one** War Caster to pick.

Also pulled: `FeatsOverhaul DualWielderPatch` (v1.0.2) and `FeatsOverhaul HitDicePatch`
(v1.0.0). The Dual Wielder patch combines Feats Overhaul's Two-Weapon Fighting Style grant
with the **-3 Attack Roll** version of Dual Wielding Master — which is the variant Listo
pulled (`Dual Wielding Tweaks Reworked (-3 Attack Roll)-1304-2-0-0`).

The **`FeatsOverhaul_GWMPatch` is NOT in the list.** So GWM: All In uses
`CharacterWeaponDamage`, meaning it does **not** apply to melee attacks that don't use weapon
damage (Pommel Strike and similar).

---

## Vanilla feats, as rebalanced

Source: `Feats Overhaul` (`15044`, archive `FeatsOverhaul-15044-1-5-10`), co-authored by
**Ajax** and built for Listonomicon. This mod is the reason vanilla BG3 feat advice is
misleading here.

**Each entry below states the FULL grant, not just what Listo changed** — vanilla baselines
verified against bg3.wiki. This matters because several feats carry a proficiency, save, or
resource that a dip could supply instead, and reading only the changelog hides it. Where Listo
altered something, the vanilla behaviour is noted in parentheses.

**Feats that grant a proficiency or save** — the ones that interact with the dip table in
`references/listo-rules.md`:

| Feat | Grants |
|---|---|
| **Resilient** | A **saving throw proficiency** (repeatable, different ability each time) |
| **Moderately Armoured** | Medium armour **and shields** |
| **Heavily Armoured** | **Heavy armour** |
| **Lightly Armoured** | Light armour — **no shields** |
| **Weapon Master** | **All** weapon proficiencies, plus a fighting style |
| **Alert** | **Perception** proficiency (Listo addition) |
| **Skilled** | 3 skill proficiencies |
| **Actor / Dungeon Delver / Performer** | Expertise in specific skills |

### ASI
Increase one ability by **2**, or two abilities by **1**. No changes in Listo — **and this is
the one ability source still capped at 20**, so it cannot take you from 20 to 22. Everything
else in this section that grants +1 bypasses the cap (with the Essential Feats caveat above).

### Actor
**+1 Charisma** — this is a **half-feat**, which the changelog framing hides. Expertise in
**Persuasion, Deception, Intimidation, and Performance** (vanilla: Deception and Performance
only). If not already proficient, you gain proficiency in those skills too.

### Alert
Initiative bonus is now **your Proficiency Bonus**, not +5. Adds **proficiency in
Perception**. Listo ships `Initiative Variants` (`1247`), which sets initiative to
**d10 + Dex + bonuses** (MCM-configurable) — the nerf is calibrated for a d8–d12 die, not
vanilla's d4. **The optional revert patch that restores vanilla Alert is NOT in the list.**

**Also grants immunity to being Surprised** — a base grant Feats Overhaul had to bug-fix (a
duplicate boost was stopping it working). Easy to overlook and worth real value against the
list's ambush mods (`Hunted - Dynamic Ambushes`, `Sensible Ambushing`).

> Still the intended way to reliably go first, per the docs — just weaker than vanilla.

### Athlete
No changes — but note it **is a half-feat: +1 Strength or Dexterity**, plus the reduced cost to
stand from Prone and improved jumping.

### Charger
- **Weapon Attack:** no longer costs a bonus action; once-per-turn cooldown; damage bonus is
  **double your Proficiency Bonus** (vanilla: flat +5). Tooltip does not show the bonus.
- **Shove:** no longer costs an action.

### Crossbow Expert → renamed **Bow Expert**
Proficiency with **all bows**. No melee disadvantage with **all bows** (vanilla: crossbows
only). Doubles duration of **Gaping Wounds and Hamstrung**. **+2 save DC** on Piercing Shot
and Hamstring Shot. **Half-feat: +1 Dexterity.**

### Defensive Duellist → renamed **Duellist**
13+ Dexterity requirement removed. With a Finesse weapon you're proficient with in your main
hand **and an empty off-hand**: bonus to melee attack rolls equal to **Proficiency Bonus**,
and **critical threshold reduced by 1**. Ships a spell to strip the Versatile property off a
Versatile+Finesse weapon so it qualifies. **Half-feat: +1 Dexterity.**

> Duo note: the empty-off-hand requirement means this competes directly with a shield. In a
> two-person party, read that as a real AC cost.

### Dual Wielder
Full grant: you can use **Two-Weapon Fighting with non-Light weapons** (still not Two-Handed),
you gain **+1 AC while wielding a melee weapon in each hand**, and — Listo's addition —
**Two-Weapon Fighting Style**.

> The **+1 AC** is a base grant the changelog framing hides, and it partly offsets giving up a
> shield. See the Dual Wielding Master entry below for how the two mods interact — Listo pulled
> both plus the bridging patch.

### Dungeon Delver
Base grants, unchanged: **advantage on Perception checks to detect hidden objects and on saving
throws to avoid or resist traps**, plus **resistance to trap damage**. Listo adds **expertise in
Sleight of Hand and Perception**, **+1 to Dexterity saving throws**, and **+1 Dexterity or
Wisdom**.

> Expertise in two skills plus a half-feat makes this a genuine skill-coverage pick, not just an
> anti-trap tax — relevant given the premise that two characters must cover every check in the
> campaign.

### Durable
Base grant, unchanged: **+1 Constitution**, and **regain FULL hit points on every short rest**.
Listo adds: while in combat, if you start your turn below **60% HP**, regain HP equal to
**Proficiency Bonus + Constitution modifier**.

> **Full HP on every short rest is the headline, and it is not a Listo change — it is vanilla,
> and easy to omit.** With two short rests per long rest, and long rests costing 120+ camp
> supplies scaling with camp population, this is one of the strongest answers in the list to the
> duo's rest-economy problem. Listo then bolted **in-combat** regen on top.
>
> The docs call out Durable + Mage Slayer as an anchor/tank package. Both were buffed here.
> Note the Wild Shape caveat: it grants full HP on short rest but **does not** raise Wild Shape
> form HP.

### Elemental Adept
Base grant, unchanged and the actual point of the feat: **your spells and attacks IGNORE
RESISTANCE** to a chosen damage type (Acid, Cold, Lightning, Fire, or Thunder). Listo
**replaces** the "cannot roll a 1 on damage die" clause with a flat **+1 damage** with that
element, and adds **+1 INT, WIS, or CHA**.

> Ignoring resistance is what the feat is for — the rebalance only touched the minor clause. In
> a list where the docs tell you to carry a spread of damage types because encounters punish the
> wrong one, a feat that deletes one resistance entirely is worth more than the +1 suggests.
>
> A **Poison** version exists separately — see `Poison Adept` below — and Poison Adept goes
> further, downgrading **immunity** to resistance when stacked with its equipment passive.

### Great Weapon Master
Two components — **only the second was rebalanced**:
- **Bonus Attack** (unchanged): when a melee weapon attack **lands a critical hit or kills**,
  make another melee weapon attack as a **bonus action** that turn.
- **All In:** damage bonus is **(2 × Proficiency Bonus) − 1** (vanilla: +10); attack penalty is
  **Proficiency Bonus** (vanilla: −5). At level 5 with PB 3: **+5 damage, −3 to hit**. Ratio
  improves from 1.50 at level 1 to 1.83 at 17. Toggleable passive.

> **The Bonus Attack half is untouched and is still excellent** — the nerf landed entirely on
> All In. GWM remains worth taking for the crit/kill bonus attack alone, which is easy to miss
> if you only read the rebalance. It also pairs with the two crit-threshold rings and Deadly
> Alacrity (see `data/listo-10.2-equipment.md`).

### Heavily Armoured
Grants **heavy armour proficiency**, **+1 Strength or Constitution** (vanilla: Strength only),
**plus +1 to saving throws** with the chosen ability.

> The armour proficiency is the point of the feat and is easy to lose sight of. A **Fighter 1**
> or **Paragon 1** level 1 supplies heavy armour for free and **returns this feat**.

### Heavy Armour Master
**Requires heavy armour proficiency** — so it needs Heavily Armoured, or a class that grants
heavy armour, before it does anything. Reduces **all** damage taken by your **Proficiency
Bonus, capped at 5** (vanilla: flat 3, and non-magical only). **+1 Strength or Constitution.**

> Stacking the two armour feats costs two of your seven or eight feats. A heavy-armour class at
> level 1 collapses that to one.

### Lightly Armoured
Grants **light armour proficiency only — no shields.** **+1 STR or DEX**, and Listo adds
**+1 to saving throws** with that ability.

> **Trap.** If you need a shield, this feat does not supply one. It is also the **prerequisite
> for Moderately Armoured**, so a character with no armour proficiency pays two feats to reach
> shields — where a Fighter/Artificer/Paragon level 1 pays none.

### Lucky
No changes. Grants **3 Luck Points**, recharging on a **long rest**, spendable for advantage on
attack rolls, ability checks, and saving throws (or to force an enemy reroll).

> Long-rest resource in a list where long rests cost 120+ camp supplies scaling with camp size.
> Weigh against short-rest alternatives — see the rest-economy premise.

### Mage Slayer
- **Break Concentration:** replaced — enemies within **3m** of you have **disadvantage on
  Concentration saves**.
- **Magic Resistance** (replaces Saving Throw Advantage): advantage on saves against **all**
  spells (vanilla: melee range only), and **reduces all spell damage by your Proficiency
  Bonus**.

### Magic Initiate (all versions)
The 1st-level spell **loses its long-rest cooldown but now costs a spell slot** (still no
upcasting) — and you **gain a 1st-level spell slot** in return. All spells use **your normal
spellcasting ability**, not the chosen class's. **Half-feat: +1 to the spellcasting ability
associated with the chosen class.**

### Martial Adept
Learn **two Manoeuvres** from the Battle Master archetype, fuelled by **2 Superiority Dice**
(vanilla: 1) — **regained on a short OR long rest**. **Half-feat: +1 Strength or Dexterity.**

> **A short-rest resource, and Listo doubled it.** In a duo paying 120+ supplies per long rest,
> a feat that refuels on short rests is worth more than its raw numbers. The manoeuvres
> themselves are also easy to forget — this is not just a dice grant.

### Medium Armour Master
**Requires medium armour proficiency.** While in medium armour: **no Stealth disadvantage**
(base), plus Listo's replacement — flat **+1 AC**, and on entering combat **temp HP equal to
Proficiency Bonus**. (Vanilla's DEX-cap raise from +2 to +3 is **gone**.) **+1 Strength or
Dexterity.**

> Because the DEX-cap raise is gone, the old "medium armour + 18 DEX" optimisation **does not
> work here**. Medium armour now caps DEX contribution at +2, full stop.

### Mobile
Base grant: **+3m (10ft) movement speed** — omitted from most summaries, and the main reason to
take the feat.
- **Evade Opportunity Attack:** **disadvantage on all opportunity attacks against you**
  (vanilla: only avoided provoking from a target you had melee-attacked).
- **Evade Difficult Terrain:** your **movement speed cannot be reduced by any effect** (vanilla:
  Difficult Terrain ignored only after Dashing).

> Both sub-passives were broadened from conditional to unconditional. Combined with the +3m, this
> went from a niche mobility feat to a solid one.

### Moderately Armoured
**Requires light armour proficiency.** Grants **medium armour *and shields***, **+1 STR or
DEX**, and Listo adds **+1 to saving throws** with that ability.

> **This is the feat that buys shields without a dip** — but note the prerequisite: a character
> with no armour proficiency at all needs **Lightly Armoured first**, making shields a two-feat
> purchase. Conversely, a **Fighter 1**, **Artificer 1**, or **Paragon 1** level 1 supplies
> medium armour and shields for free, which *returns this feat* — that trade is in the dip table
> in `references/listo-rules.md`.

### Performer
Expertise in **Performance and Acrobatics**. Performing for NPCs earns significantly more
gold, scaling with Proficiency Bonus — **but the Listo patch reduces this**. **+1 Dexterity
or Charisma** (vanilla: Charisma only).

### Polearm Master
Adds **tridents and javelins** (pikes were always included). Dynamically grants the **Reach**
property to a Versatile polearm wielded two-handed (quarterstaves, spears, tridents) — you
must re-equip the weapon after taking the feat. **Bonus Attack** now includes all damage
riders (Caustic Ring, GWM: All In) and uses your **spellcasting modifier** instead of STR/DEX
if your weapon has a casting-ability override (Pact Weapon, **Shillelagh**).

> **Correction — Shillelagh is NOT permanent.** The Listo docs say it is; the changelog (v9.0.3
> #70) says otherwise, and v10.0 #99 patched the *bug* that made it look permanent. It is a
> **level 1 spell, not a cantrip**, and **must be re-cast after every Long Rest**. It uses your
> **highest** spellcasting modifier, not Wisdom. See `data/classes/druid.md`.
>
> **The weapon lists barely overlap.** Shillelagh covers Club, Quarterstaff, Mace, Morningstar,
> Sickle, Spear, Trident. Polearm Master covers glaives, halberds, pikes, quarterstaves, spears,
> tridents and javelins. **Glaives, halberds and pikes get no Shillelagh; clubs, maces,
> morningstars and sickles get no Polearm Master.** The combination only works on a
> **quarterstaff, spear or trident** — so the spellcasting-modifier interaction is real but
> narrower than it looks.

### Resilient
**+1 to a chosen ability, and proficiency in that ability's saving throws.** Listo makes it
**repeatable** (a different ability each time) and removes the ability cap of 20.

> **The most under-described feat in the file, and the one that matters most for this run.** Save
> proficiencies are otherwise obtainable *only* from your level 1 class and Lone Wolf's +4 — and
> `references/listo-rules.md` puts the ceiling at four distinct saves from those two sources.
> **Resilient breaks that ceiling**, and being repeatable it can break it more than once. It is
> also a half-feat that stacks above 20.
>
> Weigh it against the save-value ordering in `listo-rules.md`: Wisdom > Constitution ≈ Dexterity
> > Charisma > Strength > Intelligence. A duo with no Wisdom save coverage is one Hold Person
> away from losing the fight.

### Ritual Caster
**In Listo, the ListoPatch replaces the base behaviour: you learn ALL the ritual spells from
the list**, rather than picking 3 and getting a once-per-short-rest in-combat free cast.
Base-mod features that remain relevant:
- Ritual spells available include, from `5e Spells`: Ceremony, Commune with Nature, Detect
  Magic, Unseen Servant, Water Walk; from `PF2e Spells`: Ant Haul.
- Two utility cantrips from: Dancing Lights, Friends, Guidance, Light, Mage Hand, Minor
  Illusion, Resistance, Thaumaturgy.
- On a **short rest**, 20% chance to regain a level 1 slot; at level 5 a separate 20% for a
  level 2 slot; at level 12 another 20% for level 3.
- Learning spells from scrolls costs **half** (25 gold per spell level).
- **Half-feat: +1 INT, WIS, or CHA.**

> The short-rest slot recovery is worth more in a duo than it looks — see the rest-economy
> premise.

### Savage Attacker
The installed passive remains `Reroll(MeleeWeaponDamage,20,false)`: on every qualifying melee
attack, **each eligible damage die is rolled twice independently and keeps the higher result**.
This is not limited to the weapon's printed die. It also covers dice attached to that attack by:

- **items and weapon effects** — elemental weapon dice, dips/coatings, and dice-based equipment
  riders;
- **spells** — when their dice are added to the melee hit, most importantly smites; and
- **class features** — melee **Sneak Attack**, Battle Master Manoeuvres, and Blade Flourishes.

Flat damage bonuses have no die to reroll. An independent spell damage roll, separate explosion or
save, surface, condition, and later damage tick is not part of the melee packet merely because the
weapon hit caused it. Thrown weapons are a special case: Savage Attacker can affect the base
thrown-weapon damage die, but not added riders such as Ring of Flinging.

> **Build consequence — count the whole packet.** Savage Attacker gains value with every die
> stacked onto each hit, so it is a major damage feat for smiters, melee Rogues, manoeuvre/Flourish
> users, and item-rider builds. Comparing it only against the base weapon die badly undervalues it;
> compare its expected gain from all eligible dice in the routine attack against the competing
> feat's gain, act by act.

Separately, `Add Unarmed Attacks to Savage Attacker and Savage Attacks` (`2473`) extends these
damage rerolls to **unarmed attacks**, and adds unarmed attacks to the Half-Orc **Savage Attacks**
trait. Do not confuse the feat (reroll every eligible die) with the racial trait (add a weapon die
on a critical hit).

### Sentinel
Three components — **only Vengeance was changed**:
- **Vengeance:** reaction attack when an enemy in melee range attacks an ally. Listo loosens the
  restrictions toward 5e RAW — **you can interrupt all attackers**, not only enemies attacking
  allies — and it now works correctly with Polearm Master to stop enemies **outside** your reach
  (with a small pushback if you have PAM and a polearm).
- **Snare** (unchanged): when you hit with an **Attack of Opportunity**, the target **cannot
  move for the rest of its turn**.
- **Opportunity Advantage** (unchanged): **advantage on Opportunity Attacks**.

> Two-thirds of this feat is untouched and rarely mentioned. **Lone Wolf grants an extra
> Reaction**, so reaction-driven feats like this one, War Caster, and Nimble Fingers are worth
> more here than in a normal party — the skill's premises call out scaling with reaction count.

### Sharpshooter
Two components — **only the second was rebalanced**:
- **Low Ground** (unchanged): your ranged weapon attacks are **not penalised by high-ground
  rules**.
- **All In:** identical treatment to Great Weapon Master — damage bonus
  **(2 × Proficiency Bonus) − 1**, attack penalty **Proficiency Bonus**. Toggleable passive.

> As with GWM, the un-nerfed half still carries the feat. Ignoring high ground is a persistent
> accuracy gain in a game that models elevation everywhere.

### Shield Master
Base grant, unchanged: **+2 to Dexterity saving throws while wielding a shield.**
- **Block:** now a **passive**, not a reaction — same effect as Rogue **Evasion** and **does
  not stack with it**. Correctly halves damage on a failed save (vanilla had a bug where it
  didn't). Also **reduces all damage taken by 1**.
- Unlocks **Shield Blow** as a bonus action while a shield is equipped.
- With **Viconia's Walking Fortress** equipped, Shield Blow also deals **2d4 Force**.
- All Shield Blows use a **hybrid save DC**: higher of (weapon save DC + 2) or spell save DC.

### Skilled
**+1 to any ability** added on top of the three skill proficiencies.

### Spell Sniper
Base grants, unchanged: **learn a cantrip**, and **the number needed to roll a critical hit with
a spell is reduced by 1 — and this effect stacks**. Listo adds: ranged spell attacks **ignore
low-ground penalties**, and **advantage on damage dice**
(roll twice, take highest — same as Savage Attacker) for cantrips and spells that use an
**attack roll**; multi-hit spells (Eldritch Blast, Scorching Ray) benefit on the **first hit
only**. Extra cantrip options with mods present in Listo — from `5e Spells`: Frostbite,
Lightning Lure; from `Homebrew Spells`: Illusionary Dart, Rock Slam, Sonic Blast, Water
Bullet.

> **The stacking crit-threshold reduction is the buried headline.** Spell Sniper explicitly
> stacks with other crit-threshold effects, and Listo ships several: **Deadly Alacrity** (−1),
> **Duellist** (−1), **Critfisher Ring**, and **Ring of Viciousness** (−1). A spell crit build is
> unusually well supported here — see `data/listo-10.2-equipment.md`.

### Tavern Brawler
**Nerfed hard, and the +1 STR/CON is removed entirely.** Adds
**(Proficiency Bonus − 1)** to attack rolls and damage for unarmed, thrown, and improvised
attacks (vanilla: added the Strength modifier a second time). Works in Wild Shape on Honour
rules and in Slayer Form.

> This is the headline "your vanilla knowledge is wrong" feat. Tavern Brawler throwing and
> Monk builds are not what they are elsewhere.

### Tough
Base grant: **hit point maximum increased by 2 per character level** (+40 HP at level 20). Listo
adds **+2 to Constitution saving throws** and **+1 Constitution**.

> Now a half-feat *and* a save booster on top of the HP. Combined with Lone Wolf's +30% max HP
> and halved damage, this is a large effective-HP swing on a character you cannot afford to lose.

### War Caster
Base grant, unchanged and frequently omitted: **advantage on saving throws to maintain
Concentration.**

**Only one War Caster exists in Listo** (the ListoPatch removes the duplicate and uses the
**2024** features). Opportunity Spell usable under more polymorphs and **while invisible**.
The separate mod `War Caster (2014 and UA2)` (`5822`, archive `War Caster-5822-1-15-2`) is
what supplies the 2024/2014 split; the 2024 version gives **+1 ability score**, and the 2014
version allows Polearm Master and Echo Knight interactions.

### Weapon Master
**+1 Strength or Dexterity.** Proficiency in **all weapons** (vanilla: 4 of your choice). Pick a fighting style from
Archery, Duelling, Great Weapon Fighting, Two-Weapon Fighting — **plus the UA styles**, since
`UA Fighting Styles` is in the list. Deals extra weapon damage equal to **half Proficiency
Bonus rounded down** (+1 at level 1, +2 at 9, +3 at 17).

---

## New feats — Essential Feats (`5623`)

Archive pulled: **`Essential Feats-5623-1-0-13`** — the **base file**. The optional **ASI
version is NOT installed**, so these feats give only the ability increases listed below, and
they are **not** exempted from the cap of 20 (see the uncap section).

**Listo patch: Deadly Alacrity's +1 ability score is removed.**

### Alchemist
Grants the **Experimental Alchemy** passive (brew 2 potions instead of 1 — **does not stack**
with Wizard/Artificer sources). Throw a **grenade or water bottle** free once per turn. Throw
**healing potions as a bonus action** once per turn. **+1 CON, INT, WIS, or CHA.**

### Deadly Alacrity
**Critical hit threshold reduced by 1.** On a hit, regain **1m** of movement; **3m** on a
crit or kill. **The +1 ability score is removed by the Listo patch.**

### Eldritch Adept
Learn one **Eldritch Invocation** from the Warlock class (any that doesn't require a Warlock
spell slot). **Can be taken multiple times.** **+1 INT, WIS, or CHA.**

### Fey Touched
Learn **Misty Step** plus a level 1 **divination or enchantment** spell. Both cast **without
a spell slot, once per short rest**. **+1 INT, WIS, or CHA.**

### Fighting Initiate
Learn one **fighting style** from the Fighter class. **+1 Strength or Dexterity.**

### Heaven Touched
Learn **Sanctuary** plus a level 1 **abjuration or transmutation** spell. Both cast without a
slot, **once per short rest**. **+1 INT, WIS, or CHA.**

### Hell Touched
Learn **Hellish Rebuke** plus a harmful level 1 **conjuration or evocation** spell. Both cast
without a slot, **once per short rest**. **+1 INT, WIS, or CHA.**

### Light Armor Master
While in light armour: **+3m movement, +3m jump distance**, and **reactions against you have
disadvantage**. **+1 Strength or Dexterity.**

### Meta Magic Adept
**2 metamagic options** and **3 metamagic points**. **+1 INT, WIS, or CHA.**

### Nimble Fingers
**Expertise in Sleight of Hand.** Reaction to **intercept projectiles** aimed at you and fling
them back — intercepting reduces damage by **1d10 + DEX mod**, returning deals **1d4–3d4
(level-based) + DEX mod**. Works in **Wild Shape**. **+1 Dexterity.**

> Reaction-hungry, which suits Lone Wolf's extra reaction.

### Shadow Touched
Learn **Invisibility** plus a level 1 or 2 **illusion or necromancy** spell. Both cast without
a slot, **once per short rest**; level 1 spells are learned as **level 2 upcasts**.
**+1 INT, WIS, or CHA.**

### Skilled Expert
Gain a **skill proficiency**, **expertise** in a skill, and **+1 to any ability**.

### Telekinetic
Learn **Mage Hand** (no cooldown) and **Telekinetic Shove/Pull** — bonus action, STR save,
hybrid DC, push distance **3 + Proficiency Bonus**. **+1 INT, WIS, or CHA.**

### Thief's Apprentice
Grants a **bonus action on your next turn** when you attack from stealth or kill a target,
plus **Cunning Action: Hide**. **Does not stack** with Fast Hands, Wholeness of Body, or other
bonus-action grants.

### War Magic
After casting a spell or cantrip, make a **basic attack as a bonus action**. The attack deals
**half damage until level 5**; from level 5 it deals full damage and can be **any** attack
(including weapon actions). **Does not work with Booming Blade.** Does **not** stack with
Eldritch Knight's similar feature.

> The docs single this out for melee-casters, especially **Clerics**, who otherwise get
> neither Extra Attack nor War Priest charges.
>
> **Caveat — that framing no longer holds for every domain.** `Cat's Cleric Changes` (`21257`),
> written for Listo, gives **War Domain a real Extra Attack at level 6**. So War Magic is the
> answer for the other 18 domains, not for War. See `data/classes/cleric.md`.

---

## New feats — standalone mods

### Enweaved
`Enweaved Feat` (`13310`, archive `Enweaved-13310-1-1-1`). Designed and requested by Ajax for
Listonomicon.

**+2 to WIS, CHA, or INT, to a cap of 22** — and grants **both wild magic and magic allergy**.
Listo also ships `Wild Magic D100 Table`, `More Wild Magic effects`, and `Increasingly Likely
Wild Magic Surge (Combat Only)`, all of which make the downside considerably livelier.

> The only +2 half-feat in the list. It is the cheapest single-feat route to a 22 casting
> stat, at the price of turning every cast — and being *near* casting — into a gamble.

### Dirty Fighting
`Dirty Fighting Feat` (`14049`, archive `Dirty Fighting Feat-14049-2-01`).

**+1 Strength or Dexterity.** Grants **Dirty Kick**: a bonus action dealing **1d4 + unarmed
modifier** that knocks the target **Off-Balance** — the next attack against them has
**advantage**, and they have **disadvantage on STR and DEX saves**. Counts as an **unarmed
attack** and scales with effects that buff unarmed.

> Docs flag this for sword-and-shield Fighters with a spare bonus action and for melee Rogues
> who want reliable Sneak Attack setup. **Enemy Fighters and Rogues use it from Act 3.**

### Battle Medic
`Battle Medic Feat` (`20428`, archive `Battle Medic-20428-1-2`).

Cast **healing spells as a bonus action after a weapon attack**.

> Strong in a duo, where the healer usually cannot afford to spend a whole turn healing.

### Poison Adept
From `Better Poison Equipment` (`12413`, archive `Better Poison Equipment-12413-3-1`).

A **Poison version of Elemental Adept**. The feat and the equipment passive (`Poison Adept:
Equipment`, on the Poisoner's Robe and Necromancer's Robe) are **separate sources**; holding
**both at once** grants the **Deadly Venom** condition, which downgrades enemy **Poison
Immunity to Poison Resistance** (no further). Does not affect stone/metal constructs or
inanimate objects.

> The docs' worked example — Green Dragonborn Circle of Spores Druid with the feat and the
> Poisoner's Robe — gets it on breath weapon, spore attack, and poison spells.

### Muscular
`Muscular Passive (Feat)` (`13979`, archive `Muscular Passive (Feat)-13979-1` — the **base
file**, not the homebrew optional).

Grants the **Muscular** passive: **advantage on Athletics ability checks and saving throws**.
The stronger optional version (STR increase, 2.5× carry capacity) is **not** the file Listo
pulled.

### Skeleton Crew
`Valkrana's Skeleton Crew - Random Undead and Feat` (`4496`, archive
**`Valkrana's Skeleton Crew Feat-4496-1-29-02`**).

Listo pulled the **feat** variant specifically, not the automatic one — so this is a feat
choice, not something you get for free. Companion mods present: `Valkrana's Skeleton
Emporium - 40 New Animate Dead Options`, `Valkrana's Spellbook - 12 New Necromancy Spells`,
`Valkrana's Undead Encounters`, `Valkrana's Skeletal Challenge`.

Per `references/listo-rules.md`, the feat **spawns a scaling random skeleton ally at the start
of every combat** — no resource, no cast, no concentration.

> **The single best feat in the list for this run.** It is the only feat that directly fixes
> small-party action economy, and it does so every fight rather than once per rest. The skill's
> premises already weight a third body above its raw numbers.

### Arcane Chaos
Archive `ArcaneChaosFeat-14228-1-0-0`, shipped as part of `Wild Magic Subclass - Additional
Spells` (`14228`). A feat delivered by a subclass-spells mod, so it is easy to miss when
grepping mod names for "feat".

Lets you cast **any** spell using **sorcery points**, and **always triggers a wild magic surge**
when you do. This is **broader than the subclass feature of the same name**, which `14228` grants
to the vanilla Wild Magic subclass at level 6 — the feat version is not restricted the same way.

> Pairs with Listo's surge model: risk only accrues **in combat**, ramping **+5 percentage points
> per non-surging cast** (readable in-game as the **`Unstable Magic`** condition). A feat that
> *guarantees* a surge is therefore a deliberate reset as much as a cost. See
> `data/classes/sorcerer.md`.

---

## Fighting styles (feat-adjacent)

Fighting styles matter more than usual because **Weapon Master**, **Fighting Initiate**, and
several dips can all grant one.

### UA Fighting Styles (`19693`, archive `UA Fighting Styles-19693-1-1-0`)
Adds, fully implemented: **Close Quarters Shooter**, **Mariner**, **Interception**,
**Thrown Weapon Fighting**. With modifications: **Tunnel Fighter**. Partially implemented —
each always gives a fixed choice rather than a selection:
- **Superior Technique** → always **Riposte**
- **Druidic Warrior** → always **Guidance and Shillelagh**
- **Blessed Warrior** → always **Guidance and Sacred Flame**

Deliberately not implemented: Blind Fighting, Unarmed Fighting.
**Close Quarters Shooter, Mariner, and Thrown Weapon Fighting are added to the Swords Bard
list.** These styles are also added to **Weapon Master's** options.

> **Druidic Warrior is a cheap route to Shillelagh** for anyone who can take a fighting style.
> But note Shillelagh in Listo is a **level 1 spell requiring a re-cast after every Long Rest**,
> not a permanent cantrip effect (the docs are wrong; see `data/classes/druid.md`), and whether a
> feature-granted Shillelagh **costs a spell slot** is `(unverified)`.

### Protection and Great Weapon Fighting PHB2024 (`18684`)
- **Protection:** now gives **disadvantage on ALL attack rolls** against the protected target
  until the start of your next turn, as long as they stay within **1.5m** of you.
- **Great Weapon Fighting:** sets the **minimum melee weapon damage die result to 3**.

### Unarmored Defence Synergy (`2837`)
Allows Unarmored Defense to compute AC as **10 + WIS + CON (no DEX)** for a **Monk/Barbarian
multiclass** — the two normally overwrite each other.

---

## Racial / class features that behave like feats

- **Githyanki Psionics** (`13920`): psionics are **no longer spells**, so they can be cast
  **while Silenced**.
- **Dragonborn - Stronger Breath Weapon** (`3235`, archive `Dragonborn - Stronger Breath - A`):
  breath weapon gains dice **faster than every 5 levels**; the die can be changed between d4,
  d6, d8, d10, d12 (20 combinations). The **`- A`** suffix is the specific balance variant
  Listo pulled — the mod ships several `(unverified which tier "A" corresponds to)`.

---

## Not in 10.2 — do not recommend

Confirmed **absent** from `listo-10.2-mods.tsv`:

| Thing | ModID | Note |
|---|---|---|
| **Arcanist Feat** | `1087` | **Removed in v9.0.3** (changelog: *"REMOVED Arcanist Feat and Experimental Alchemy as a Feat"*). The canonical doc-lag trap — docs page 4 still describes it in detail (+1 INT, Arcana expertise, a level 1 spell once per short rest). **It is gone.** Use Essential Feats' `-Touched` / `Magic Initiate` / `Eldritch Adept` lines instead. |
| **Experimental Alchemy as a Feat** | `12446` | **Removed in v9.0.3**, same changelog entry. Essential Feats' **Alchemist** covers the same ground — and no two Experimental Alchemy sources stack (feat, Wizard, Artificer all give the same 2 potions). |
| **Stackable ASI Feats** | — | Referenced by Feats Overhaul as the way to uncap Essential Feats' half-feats. Not present, so that uncap does not apply. |
| **FeatsOverhaul_GWMPatch** | — | Not pulled; GWM: All In does not extend to non-weapon-damage melee attacks. |
| **Feats Extra** | — | Referenced by Essential Feats' author as where most of his rebalance ideas live. Not in the list. |
| **Magic Initiate Feats Enhanced** | — | Not present; Magic Initiate spells **cannot be upcast**. |

`Features from DnD 5E Spelljammer` (`13195`) is in the list but adds **backgrounds, goals,
spells, items, and a bestiary — not feats**. Do not treat it as a feat source.

> **Caveat on absence claims.** `listo-10.2-mods.tsv` covers **Nexus mods only**. The manifest
> also carries **8 mod.io archives** and two GitHub downloads (MO2 and its BG3 plugin) that do
> not appear in the TSV — Bloodhunter is the known mod.io class. Every mod listed as absent
> above is a **Nexus** mod, so TSV absence is conclusive for those. For anything else, check
> the manifest's `"Url"` fields before declaring it missing:
> `grep -o -E '"Url":"[^"]{1,120}' data/listo-10.2-manifest.json | sed 's/"Url":"//' | sort -u`
