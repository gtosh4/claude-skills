# Listonomicon 10.2 — Paladin

Paladin in Listo is close to vanilla in *chassis* and far from vanilla in *reach*. The class
itself gets no overhaul-scale rewrite: Charisma half-caster, all armour, Wisdom + Charisma
saves, Channel Oath on a short rest. What changes is the surrounding frame — auras are pushed
from 3m to **9m base / 15m improved** for every oath (Listo's own patch), the level cap runs to
**20** via `Expansion` (`279`), the concentration requirement is stripped off the three smites
that carried it, Goon's overhaul fixes a pile of smite/aura bugs and makes Improved Divine Smite
a toggle, and **Oathbreaker is rebuilt into a distinct necrotic subclass** that trades Divine
Smite away entirely for Unholy Smite. Nine oaths are selectable (five vanilla, four modded), and
one of them — Oathbreaker — can be taken at character creation, which is the single most
dangerous option in this file.

---

## At a glance

| | |
|---|---|
| **Primary ability** | **Charisma** — spells, Aura of Protection, Channel Oath DCs, most oath scaling. **Strength or Dexterity** for weapon attacks; **Constitution** for HP and concentration. |
| **Saving throws granted at level 1** | **Wisdom + Charisma** (vanilla, unaltered in Listo). Only granted if Paladin is your **level 1** class. |
| **Armour / weapon proficiencies (level 1 class)** | Simple + Martial weapons; **Light, Medium and Heavy armour**; **Shields**. |
| **Proficiencies if multiclassed *into*** | Simple + Martial weapons; **Light and Medium armour**; Shields. **No Heavy armour, no save proficiencies.** |
| **Spellcasting** | Half-caster. Prepared spells = **Paladin level + CHA mod** (min 1), swappable out of combat. Slots restore on **long rest**. |
| **Channel Oath** | **1 charge**, restores on **short rest**. Each oath grants a level 1 option and (usually) more at level 3. |
| **Lay on Hands** | **3 charges** at level 1, **+1 at level 4**, **+1 at level 10** (5 total). Restores on **long rest**. |
| **Divine Sense** | Advantage on attack rolls vs celestials/fiends/undead. **Short rest**. |
| **Feats (Listo cadence)** | **3, 6, 9, 12, 13, 15, 18** — seven total, keyed off *class* level. See `listo-10.2-feats.md`. |
| **Level breakpoints** | **1** oath + Channel Oath + Lay on Hands + Divine Sense + heavy armour/saves · **2** spellcasting + Divine Smite · **3** oath features + oath spells (+ Listo feat) · **5** Extra Attack · **6** **Aura of Protection** (+CHA to saves, you and allies) · **7** oath aura · **9/13/17** oath spells · **10** Aura of Courage (frightened immunity) · **11** Improved Divine Smite · **14** Cleansing Touch (from `Expansion`) · **15** oath feature · **18** aura radius upgrade · **20** oath capstone |
| **Dip value** | **Very high at 1** (heavy armour + Wis/Cha saves — *only* if it is your level 1 class), **high at 2** (Divine Smite on any slot from any class), **high at 6** (Aura of Protection is a party-wide save buff). See "Dip value" below. |

---

## The Oathbreaker respec trap

**Verified.** `Start with Oathbreaker Unlocked` (`12052`, archive
`Start with Oathbreaker Unlocked-12052-1-1725803151.zip`) is in the list and lets you pick
**Oathbreaker in character creation**. Its own mod page states, in the author's words, that the
mod *"DOES NOT give Oathbreakers the ability to respec"* and tells you to "make sure you're
committed to an Oathbreaker character and have your build planned out before you select this
subclass." bg3.wiki confirms the underlying engine behaviour: **"Withers will not respec a
Paladin who has the Oathbreaker subclass. Restoring their original Oath will enable the respec
service again."**

The Listo docs say the same and add the escape hatches: *"as a limitation of BG3, this will
block you from normal respec and require you to use console commands or deal with the Oathbreaker
Knight."*

Why this is a trap and not a nuisance, for this run specifically:

- **Only your level 1 class grants saving throw proficiencies.** A respec re-picks level 1 from
  scratch. If a build depends on Wisdom + Charisma saves (Paladin's pair — the two best save
  categories in the game for a front-liner, since Wisdom gates most control effects and Charisma
  gates banishment), that dependency is locked in at creation and can only be re-rolled by a
  respec. Being unable to respec means being unable to fix a wrong level 1 pick — you are
  committed for the entire run.
- The mitigation the mod page recommends — the `Respec Spell` mod — **is not in Listo 10.2**
  (grepped the TSV; absent). Neither is `Appearance Edit Enhanced`, which older changelog entries
  mention as a free-respec route but which no longer appears in the 10.2 mod list.
- That leaves two routes, both with costs: **the Oathbreaker Knight** (in vanilla he charges
  1000gp for the first oath restoration, 2000gp for the second, 10,000gp thereafter — and Listo
  runs merchant prices at ×4 buy / ¼ sell, so gold is genuinely scarce) or **Script Extender
  console commands**, which is an out-of-game fix. `Combat Console Commands` (`9282`) is in the
  list but is a combat-debug tool, not a respec tool.
- Note the asymmetry: the Knight route restores *an oath you broke*. If you **started** as an
  Oathbreaker you never had one. That the Knight can still be used to take on an oath and thereby
  re-enable Withers is Listo's documented claim, **not something confirmed on the mod page**
  — treat "start as Oathbreaker, later convert to a normal oath via the Knight" as
  **(unverified)** and do not plan a build around it.

**Planning rule:** if you want to *play* an Oathbreaker, the safe path is to take a normal oath
at level 1 and break it in play (which is reversible, costs gold, and keeps Withers available
until you actually convert). Only pick Oathbreaker in character creation if the build is final
— stats, race, and level 1 class all settled — because you will not get a second look at any of
them.

`Minthara Oathbreaker Dialog` (`17578`, `Minthara Oathbreaker Dialog-17578-1-0-0-1`) restores a
hidden conversation with Minthara for a character who is or becomes an Oathbreaker. Pure
roleplay; no mechanical effect.

---

## Class changes from vanilla

**Level cap 20** — `Expansion` (`279`), archive `Expansion-279-1-7-3-6-1780876532.zip`
(**v1.7.3.6**; the Nexus page is on **v1.7.3.10**, so Listo is four patches behind). Paladin
additions from this mod:

- **Cleansing Touch** at 14th level.
- **Harness Divine Power** (optional, 2nd) and **Martial Versatility** (optional, 4th) — these
  are Tasha's *optional* features gated behind an MCM toggle. **Listo turns them OFF**:
  `optional_features.Paladin: false` in the installed `MCM/Expansion/settings.json`. Neither is
  available — resolved, see `data/listo-10.2-mcm.md`.
- Per-oath 13th/17th oath spells plus 15th and 20th level features (listed under each oath below).
- The **v1.7.3.7** fix "added inability to use the 18th level Paladin's Aura of spells if you're
  already under their effects" is **not** in Listo's build (it pulled 1.7.3.6), so that stacking
  quirk is presumably still live at 18.
- `Expansion`'s own feat schedule is irrelevant here — Listo overrides feat cadence globally with
  `Universal Feat Every X Level(s) - MCM` (`13193`) to **3/6/9/12/13/15/18**. See
  `listo-10.2-feats.md`.

**Aura radius — every paladin, every oath.** Listo changelog (v6.1.0, item 22): *"All Paladins in
Listo should now have a 9m aura radius and a 15m improved aura radius (meaning vanilla and modded
subclasses are all covered by the improvement)."* Vanilla is 3m (Listo's own words: "vanilla
range is 3m!"). This is delivered by a Listo-internal patch — the old `Increase Paladin Aura
Range` and `Visual Paladin Auras` mods were both removed and are **not** in the 10.2 TSV.
Caveat: the "all modded subclasses are covered" claim dates from v6.1.0, well before Oath of the
Moon (v10.0) and Otherworldly Archetypes were added, so coverage of those two is **(unverified)**.

**Smites no longer require concentration.** Docs: *"Smites that once required concentration should
not anymore."* Scope, checked against bg3.wiki:

| Smite | Concentration in vanilla BG3? |
|---|---|
| **Searing Smite** | **Yes** — affected by this change |
| **Wrathful Smite** | **Yes** — affected |
| **Branding Smite** | **Yes** — affected |
| Blinding Smite | No (Larian already dropped it) |
| Thunderous Smite | No |
| Divine Smite / Improved Divine Smite | No (not spells with duration) |

So the change covers exactly **three** vanilla smites — but those three are the ones that
previously competed with holding a real concentration spell. Delivery mechanism: Listo's
**internal master spell patcher**, not a Nexus mod — the standalone `Non-Concentration Smites`
mod (and `Quickened Oaths`) were **removed in v9.0.3** as *"redundant with Listo's master spell
patcher."* Because the patcher is a Listo file rather than a listed mod, this is
**doc-verified, not manifest-verified**. Modded smites are handled per-mod (e.g. Oath of the
Moon's Lunar Smite is de-concentrated by its own author).

**`Goon's Paladin Overhaul` (`17535`)** — archive `Goon's Paladin Overhaul-17535-1-1-0-0-1781095388.zip`
(**v1.1.0.0**, current). This is a bug-fix/QoL layer, not a rewrite. Listo also pulls the mod's
**optional file** `No Divine Smite for Oathbreakers-17535-1-0-3-7-1767852139.zip` (v1.0.3.7) —
see Oathbreaker below. Requires `Goon's Library` 4.6.0.0+, which Listo pulls at 4.9.0.0.

- *Divine Smite:* targets that are both Fiend **and** Undead no longer take double damage from
  spell variants; the +1d8 vs Fiends/Undead now shows correctly in the tooltip as conditional
  damage; interrupt tooltips carry damage lists; Honour-ruleset damage-rider bools fixed;
  animations fixed for base and 3rd+ upcasts under Honour rules.
- *Divine Smite interrupts:* now default to **ask** instead of auto-firing (important — this is
  the setting that stops you dumping slots on trash), can trigger from **throwing melee weapons**,
  and can be used while **Invisible**.
- *Improved Divine Smite (11):* now a **toggleable passive**, and the bonus damage also applies
  when throwing melee weapons.
- *Aura of Hate (Oathbreaker, 7):* extra damage now works with **all** melee attacks and with
  thrown melee weapons; the aura now buffs only **non-hostile** fiends and undead (in vanilla it
  also buffed enemy fiends/undead standing in it).
- *Oath of the Crown* finally gets its own unique smite-preparation VFX.
- Under the hood it rewrites the `IsDivineSmite` and `IsSmiteSpells` functions so that modded
  smites (Unholy Smite, Lunar Smite, Eldritch Smite from Mizora's Rewards, etc.) correctly count
  as smites for restricted smite reactions and for Dazing Smite.

**Oathbreaker is a different subclass in Listo** (details in its own section below).

**Oath of the Ancients** gained **Shillelagh** as an option (changelog: Shillelagh's weapon list
widened to Club, Quarterstaff, Mace, Morningstar, Sickle, Spear, Trident; it is now a level 1
spell that must be re-cast after a long rest, and it is *"an option for Oath of Ancients
Paladins"*).

**Oath of the Crown** gained a niche via a **Royal Decree cantrip** added from mod.io (changelog:
*"ADDED (ModIO) Royal Decree Cantrip (creating a niche for Oath of Crown)"*). Not a Nexus mod, so
not in the TSV; mechanics **(unverified)**.

**Enemy paladins are dangerous.** Combat Extender gives NPC paladins act-scaled boosts: Heavy
Armour Master in Act 3, Improved Critical by Act 3, better Extra Attack access in Act 3, war
magic (cast + attack) by Act 3, improved saving throws and healing in Act 3, shield-shove, and
*"Paladins smite more and smite harder."* Enemy paladins are also differentiated by oath. Assume
any humanoid paladin-flavoured enemy in Act 2–3 hits far harder than the vanilla equivalent.

---

## Oaths (subclasses)

Nine selectable oaths. Five vanilla (all still present), four added by mods.

### Oath of Devotion
- **Mod:** vanilla (`Expansion` `279` supplies 13–20)
- **File pulled:** `Expansion-279-1-7-3-6-1780876532.zip`
- **Mechanics:** vanilla 1–12 (Holy Rebuke / Sacred Weapon Channel Oath, Aura of Devotion at 7 —
  charm immunity). `Expansion` adds **oath spells at 13 and 17**, **Purity of Spirit at 15** and
  **Holy Nimbus at 20**. Listo's global aura patch puts the aura at 9m / 15m improved.
- **Duo relevance:** Aura of Devotion's charm immunity covers your partner too at 9m, which
  matters against the list's revamped enemy casters. Otherwise the plain, safe pick.

### Oath of the Ancients
- **Mod:** vanilla (`Expansion` `279` supplies 13–20)
- **File pulled:** `Expansion-279-1-7-3-6-1780876532.zip`
- **Mechanics:** vanilla 1–12 (Nature's Wrath / Turn the Faithless, **Aura of Warding at 7** —
  resistance to spell damage for you and nearby allies). `Expansion` adds **oath spells at 13 and
  17**, **Undying Sentinel at 15** and **Elder Champion at 20**. Listo additionally offers
  **Shillelagh** to this oath, and Shillelagh in Listo is buffed, permanent-until-long-rest, and
  applies to a wide weapon list.
- **Duo relevance:** **the strongest defensive aura in the class for a two-person party.** Aura
  of Warding at 9m gives *both* characters resistance to spell damage, which is the damage type
  the run's revamped enemy casters lean on hardest. Combined with Aura of Protection at 6, a
  level 7 Ancients paladin is carrying the other character's survivability.

### Oath of Vengeance
- **Mod:** vanilla (`Expansion` `279` supplies 13–20)
- **File pulled:** `Expansion-279-1-7-3-6-1780876532.zip`
- **Mechanics:** vanilla 1–12 (Abjure Enemy / Vow of Enmity, subclass feature at 7).
  `Expansion` adds **oath spells at 13 and 17**, **Soul of Vengeance at 15** and **Avenging Angel
  at 20**.
- **Duo relevance:** the damage oath. Vow of Enmity is single-target advantage on a short-rest
  Channel Oath charge — with Lone Wolf's extra Action you get more attacks per turn to spend that
  advantage on than a normal party member would.

### Oath of the Crown
- **Mod:** vanilla (`Expansion` `279` supplies 13–20; Goon's overhaul fixes its VFX; Royal Decree
  cantrip from mod.io)
- **File pulled:** `Expansion-279-1-7-3-6-1780876532.zip`
- **Mechanics:** vanilla 1–12. `Expansion` adds **oath spells at 13 and 17**, **Unyielding Saint
  at 15** and **Exalted Champion at 20**. Goon's overhaul gives it its own smite-preparation VFX
  (cosmetic). Listo adds a **Royal Decree cantrip** from mod.io — mechanics **(unverified)**.
- **Duo relevance:** Crown's Channel Oath is a taunt-and-tank package, which is exactly the shape
  a Lone Wolf duo wants: force attacks onto the character holding Aura of Protection and heavy
  armour, keep them off the squishier partner.

### Oathbreaker
- **Mod:** vanilla base, then rebuilt by `Unholy Smite for Oathbreakers` (`15366`),
  `Improved Unholy Smite for Oathbreakers` (`12916`), `Goon's Paladin Overhaul`'s optional
  **No Divine Smite for Oathbreakers** file (`17535`), and `Expansion` (`279`) for 13–20.
  Selectable at character creation via `Start with Oathbreaker Unlocked` (`12052`).
- **Files pulled:** `Unholy Smite for Oathbreakers-15366-4-3-3-1762065818.rar` (v4.3.3, current) ·
  `Improved Unholy Smite-12916-2-2-1765261400.rar` (v2.2, current) ·
  `No Divine Smite for Oathbreakers-17535-1-0-3-7-1767852139.zip` (optional file, v1.0.3.7) ·
  `Start with Oathbreaker Unlocked-12052-1-1725803151.zip` (v1, current)
- **Mechanics:**
  - **Level 1:** Spiteful Suffering — target takes `1d4 + CHA mod` **Necrotic** per turn and
    attack rolls against it have advantage.
  - **Level 2:** **Unholy Smite replaces Divine Smite.** Damage scaling mirrors Divine Smite
    exactly (author's words), upcastable to **spell slot level 9** so it works at level 20. The
    Divine Smite *removal* is real and shipped: Listo pulls Goon's `No Divine Smite for
    Oathbreakers` optional file, and the changelog records *"Replaced 'No Divine Smite for
    Oathbreakers' (standalone mod) with Goon's version made for his paladin overhaul."*
    **Practical consequence: an Oathbreaker's smite damage is entirely Necrotic, never Radiant.**
    That is a straight downgrade against the shadow-cursed and undead enemies of Act 2, and an
    upgrade against very little.
  - **Level 3:** Control Undead, Dreadful Aspect; oath spells Hellish Rebuke, Inflict Wounds.
  - **Level 5:** oath spells Crown of Madness, Darkness.
  - **Level 7:** **Aura of Hate** — you and nearby **fiends and undead** get bonus melee damage
    equal to your CHA modifier. Goon's overhaul extends this to **all** melee attacks and to
    **thrown melee weapons**, and restricts the buff to **non-hostile** fiends/undead.
  - **Level 9:** oath spells Bestow Curse, Animate Dead.
  - **Level 11:** **Improved Unholy Smite** replaces Improved Divine Smite — **+1d8 Necrotic**
    instead of Radiant on melee hits. (Mod page note: the level-up screen visually shows both;
    you only actually get the Unholy version.)
  - **Level 13/17:** oath spells (`Expansion`). **Level 15: Supernatural Resistance** —
    `Expansion` specifically tuned this to grant resistance to bludgeoning/slashing/piercing from
    **non-magical** weapons. **Level 20: Dread Lord.**
  - Listo also added **Vampiric Touch** to the Oathbreaker spell list (changelog).
- **Duo relevance:** **Aura of Hate does not help a normal partner.** It buffs "you and nearby
  fiends and undead" — a human/elf/tiefling co-op partner gets nothing from it. It *does* buff a
  partner playing a **Ghastly Ghouls playable undead** (`5895`, see `listo-10.2-races.md`), which
  is the one race pairing that turns Oathbreaker's level 7 aura into a genuine duo aura. Note the
  same races file's warning that the undead tag breaks most healing — an Oathbreaker's Lay on
  Hands would not fix an undead partner either. Weigh this against Oath of the Ancients, whose
  level 7 aura helps any partner unconditionally.

### Oath of Conquest
- **Mod:** `Oath of Conquest - Paladin Subclass` (`13147`), by Luma
- **File pulled:** `Oath of Conquest 1.2.0-13147-1-2-0-1730591136.zip` (**v1.2.0**, current)
- **Mechanics:** Xanathar's Guide implementation, "as close to rules as written as I could get
  it", with progression **to level 20 built into the mod** (no cap mod needed for the features
  themselves).
  - **Level 1 Channel Oath — Conqueror's Retort:** when a creature **misses you** with an attack
    roll in melee range, spend Channel Oath to retaliate with a melee weapon attack; the attacker
    must succeed a **Wisdom save** or be **Frightened for 3 turns** (repeat save at end of each of
    its turns).
  - **Level 3 Channel Oath — Conquering Presence:** Action; every creature of your choice you can
    see within 30 ft makes a Wisdom save or is Frightened for 1 minute (repeat save each turn).
    **Guided Strike:** **+10 to an attack roll**, chosen *after* seeing the roll.
  - **Oath spells:** 3 Armour of Agathys, Command · 5 Hold Person, Spiritual Weapon · 9 Bestow
    Curse, Fear · 13 Dominate Beast, Stoneskin · 17 Cloudkill, Dominate Person.
  - **Level 7 Aura of Conquest:** frightened creatures take **psychic damage equal to half your
    paladin level** if they start their turn in the aura. **The speed-reduction-to-0 half of this
    aura does nothing** — the author states BG3's Frightened condition works differently and the
    clause is left in only in case a mod reimplements it; no such mod is in Listo (`Goon's
    Condition and Surface Overhaul` `17320` does not touch Frightened). Radius 10 ft → 30 ft at
    18 per the mod, but Listo's global patch nominally normalises paladin auras to 9m/15m.
  - **Level 15 Scornful Rebuke:** any creature that **hits** you takes psychic damage equal to
    your **CHA modifier** (min 1). Toggleable.
  - **Level 20 Invincible Conqueror:** Action, 1 minute — **resistance to all damage**, **one
    extra attack** on the Attack action, and **crit on 19–20**. Once per long rest.
  - **Implementation warning:** *"You are tagged as **Oath of Vengeance** — all oathbreaking rules
    and dialogue for Vengeance will apply."* Plan roleplay around Vengeance's break triggers, not
    Conquest's tenets.
  - **History note:** Conquest was previously removed from Listo (*"It's out of date, and the
    up-to-date versions block other Paladin subclasses from working"*) and later re-added at
    "Luma's latest and greatest". The version in 10.2 is the current one and coexists with the
    other oaths.
- **Duo relevance:** the best **capstone** in the list for a Lone Wolf duo — resistance to *all*
  damage plus an extra attack plus 19–20 crits on the character who is also carrying Aura of
  Protection. Guided Strike (+10 after seeing the roll) is a short-rest-recharging guarantee on
  the one attack that must land, which matters more in a duo where a single missed control effect
  can lose the fight. The Frightened-based damage aura is only as good as your ability to land
  Wisdom saves.

### Oath of the Bleak Walkers
- **Mod:** `Oath of the Bleak Walkers Paladin Subclass` (`6598`), also by Luma
- **File pulled:** `Oath of the Bleak Walkers Paladin Subclass-6598-1-4-1715793922.zip`
  (**v1.4**, current)
- **Mechanics:** homebrew "evil paladin without oathbreaking", inspired by Pillars of Eternity;
  features go to **level 20** in the mod. Feature *names* on the mod page are images, so the names
  below come from the prose and changelog; the mechanics are quoted from the description text.
  - **Level 1:** **Expertise in Intimidation** (a real skill payoff for the high Charisma you
    already need). **Channel Oath — No Quarter:** Action; deal weapon damage to one target and
    force it plus enemies within 3m into a **Strength save** or be knocked back 3m and **Prone**.
  - **Oath spells:** 3 Inflict Wounds, Command · 5 Crown of Madness, Darkness · 9 Bestow Curse,
    Fear · 13 Blight, Phantasmal Killer · 17 Dominate Person, **Artistry of War** (the author
    deliberately gave a wizard-scroll-only spell to this oath).
  - **Level 3 Channel Oath — Black Flames:** **Bonus Action**; next attack deals **+1d10 Fire +
    1d10 Necrotic**, or **flat 10 Fire + 10 Necrotic if you have Advantage** on the roll. Target
    becomes **Sickened** — HP reduced by its level + 1, and **disadvantage on Constitution saves**.
    Lasts 1 minute or until you hit. Stacks with Divine Smite on the same hit.
  - **Level 3 Channel Oath — (Death's Maw):** Action; **whenever you defeat an enemy**, enemies
    within 2m make a **Wisdom save** or are Frightened until the start of their next turn; and
    while you stand **within 2m of a corpse**, all damage you take is reduced by your
    **Proficiency Bonus**. **Lasts until your next long rest.**
  - **Level 7 aura:** 3m (9m at 18 per the mod; Listo's global patch nominally 9m/15m). **You and
    nearby allies reduce the roll needed to crit by 1, and it stacks** with other crit-range
    effects.
  - **Level 15:** Black Flames upgrades to **2d10 Fire + 2d10 Necrotic** (or flat 20 + 20 with
    Advantage) and adds **1d10 Necrotic per round for 3 rounds**.
  - **Level 20 — Avatar of Bleak War:** Action, 1 minute — resistance to **slashing, bludgeoning
    and piercing**, every attack deals **+1d10 Necrotic**, and enemies starting their turn in
    melee range make a **Wisdom save** or are Frightened. Once per long rest.
  - Ships a subclass dye (tutorial chest + vendors). Black Flames VFX will not render on
    **scimitars** (game-file limitation). VFX comes from `VFX Library by Shivero` (`3888`), which
    is in the list. The mod **removed its Oath Framework files in v1.2**, so it does not use
    `Oath Framework`; its oathbreaking behaviour is **(unverified)**.
- **Duo relevance:** the **level 7 aura is the standout for a duo** — a stacking crit-range
  reduction that applies to *both* characters, which compounds with the crit-range gear the list
  is full of and with a partner who makes many attacks (Lone Wolf's extra Action). Death's Maw's
  proficiency-bonus flat damage reduction while near a corpse is a cheap, long-lasting tank
  buff that pairs naturally with the Durable + Mage Slayer anchor package the docs recommend.
  Expertise in Intimidation also lets one character monopolise the Charisma skill spread.

### Oath of the Moon (Selûne-inspired)
- **Mod:** `Oath of the Moon - Paladin Subclass. Selune-inspired oath.` (`19534`)
- **File pulled:** `Oath of the Moon 19534 2.0 2026-06-17T19-13Z 5eYi6PheW.zip` (**v2.0**, current)
- **Added in Listo v10.0**, together with *"2 patches from CatDude55 fixing Mizora's Rewards and
  Moon Paladins"* — those patches are Listo-internal files, not Nexus mods. Optional dependency
  `Dialogue and Reactivity Tags (DART) Framework` (`17561`) is present, so the custom dialogue
  should work.
- **Mechanics:**
  - **Oath spells:** 1 Guidance · 3 Faerie Fire, Sanctuary, **Lunar Smite** · 5 Moonbeam, Warding
    Bond · 9 Remove Curse, Spirit Guardians · 13 Dimension Door, **Fount of Moonlight** · 17 Hold
    Monster, Mass Cure Wounds. The author states **Lunar Smite is de-concentrated in this
    version**.
  - **Level 1 Channel Oath — Full Moon:** Bonus Action; hostiles within **9m** make a **Wisdom
    save** or are **Blinded and Slowed for 2 turns**. Plus the Guidance cantrip.
  - **Level 3:** **Superior Darkvision.** **Channel Oath — Punish the Wicked:** Bonus Action;
    teleport next to an enemy (free repositioning, enemy-target only). **Channel Oath — Divine
    Guardian:** Action; you or an ally take **half incoming damage for 10 turns**, and it
    **stacks with resistance** and with the level 7 aura.
  - **Level 7 — Aura of Moonlight:** reduces **all** incoming damage to allies in the aura by
    your **Charisma modifier**, stacking with resistance. 3m → 9m at 18 per the mod (Listo's
    global aura patch may raise this; **unverified for a v10.0-era subclass**).
  - **Level 15 — Silvered Rebuke:** creatures that **miss** an attack roll against you make a
    Wisdom save or take radiant damage equal to **character level + CHA modifier**. Toggleable
    (the author added the toggle for fights against radiant-retort enemies).
  - **Level 20 — Lunar Champion:** Bonus Action, 10 turns — **you gain one extra Reaction**; all
    non-enemies within 18m gain a bonus to **all saving throws equal to your CHA modifier** and
    temporary Freedom of Movement; enemies within 3m save vs Wisdom each turn or gain
    **Vulnerability to Radiant**.
  - New spell **Fount of Moonlight** (5e 2024, level 4): 6m light, **resistance to Radiant**,
    melee attacks deal **+2d6 Radiant** for 10 turns, and a reaction to Blind an attacker within
    18m. Upcastable to 9th.
  - **Warnings from the author:** *"Oath breaking events are all based on Devotion Paladin"* — you
    inherit Devotion's break triggers and restoration dialogue. Searing Smite and Lunar Smite lack
    the glowing ground effect when preparing. Uninstalling mid-run requires disposing of the
    starting armour manually. Anyone updating from 1.0 to 2.0 must respec first — irrelevant for
    a fresh 10.2 install, which ships 2.0.
- **Duo relevance:** **the most duo-tuned oath in the list, by a wide margin.** Aura of Moonlight
  is flat damage reduction equal to CHA mod on *every* hit either character takes, stacking with
  resistance — and Divine Guardian is a Channel Oath (short rest!) that halves all damage on the
  *other* character for 10 turns. That is a targeted "keep my partner alive" button, and losing
  either character usually ends the fight. Lunar Champion at 20 adds a party-wide CHA-mod bonus
  to **all saving throws** stacked on top of Aura of Protection, plus an extra Reaction on top of
  Lone Wolf's extra Reaction. Compare directly against Ancients (spell-damage resistance) and
  decide by damage type profile.

### Oath of Illumination
- **Mod:** `(DTO) Otherworldy Archetypes` (`21822`) — Daelen's Testament of the Otherworldly, a
  12-subclass pack (one per vanilla class)
- **File pulled:** `Otherworldly Archetypes 21822 1.2.0.67 2026-06-17T17-15Z PYJWETtYB.zip`
  (**v1.2.0.67**, current or newer than the page's headline version)
- **Mechanics:** **mostly (unverified).** The Nexus description gives only the pitch —
  *"Empowered by Lathander's light, you eschew traditions for brilliant beams of radiant energy
  and smite your foes from a distance"* — and states the whole pack is **fully featured to level
  20**. The only concrete feature name recoverable from the mod's changelog is **Aura of
  Brilliance** (entries describe removing its body glow and toning down its ground effect). No
  level-by-level breakdown is published on the Nexus page; there is no separate detail page for
  it in the mod's own link set. The pack notes `Mystra's Spells` or `5E Spells` are strongly
  recommended — `5e Spells` (`125`) is in Listo.
  - Listo added the pack **"for testing"** in v9.0.3 and it is still present in 10.2.
- **Duo relevance:** a **ranged radiant** paladin is a genuinely different shape from every other
  oath here, and radiant is the right damage type for Act 2. But with no verifiable feature list,
  do not build a duo plan around it without confirming in-game first. Treat as experimental.

### Supporting library

**`Oath Framework` (`6493`)**, archive `Oath Framework-6493-1-2-1-1714869665.zip` (**v1.2.1**,
current), loads just after Community Library. It is an **API**, not player-facing content: it
lets custom paladin mods implement their own oathbreaking triggers and, notably, **redemption
events that regain your oath without paying the Oathbreaker Knight**. Nothing in the 10.2
paladin set is confirmed to use it — Bleak Walkers explicitly **removed** its Oath Framework files
in v1.2, Conquest piggybacks on Vengeance's oathbreaking, and Moon piggybacks on Devotion's.
Whether Oath of Illumination uses it is **(unverified)**. Do not count on a free redemption path.

---

## Dip value

- **Paladin 1 as your level 1 class** is the highest-value single level in the class, and it is
  **not repeatable by dipping later**: heavy armour proficiency and the **Wisdom + Charisma save
  proficiencies** only come from the level 1 class. Multiclassing *into* Paladin gives Light and
  Medium armour and shields only. Everything else in this file is downstream of that one
  irreversible choice — see the respec trap section.
- **Paladin 2** is the classic dip: **Divine Smite**, which converts *any* spell slot from *any*
  class into burst weapon damage, plus half-caster spellcasting and Lay on Hands. Under Listo's
  feat cadence (3/6/9/12/13/15/18, keyed to class level) a **3-level** dip is feat-neutral — you
  collect the dip class's own level 3 feat — so **Paladin 3** (oath features, oath spells, second
  Channel Oath option) is usually the better-shaped dip than Paladin 2.
- **Paladin 6** buys **Aura of Protection**: +CHA modifier to saving throws for you *and* your
  partner, at Listo's 9m radius rather than vanilla's 3m. In a duo where a single failed save can
  end the fight, this is the strongest six levels of defence available to a Charisma character,
  and it stacks with the extra save bonuses Oath of the Moon hands out at 20.
- **Paladin 7** adds the oath aura, which for Ancients (spell-damage resistance), Moon (flat
  damage reduction) and Bleak Walkers (party crit range) is a second party-wide effect. If either
  character is going Paladin at all, 7 is the natural stopping point before committing further.
- **Against dipping out:** Extra Attack at 5, Improved Divine Smite at 11 and the level 20
  capstones (Invincible Conqueror, Lunar Champion, Avatar of Bleak War) are all real, and a
  level-20 cap means a monoclass paladin actually reaches its capstone. In a duo the capstones
  are unusually valuable because they buff the character who is already the anchor.
- **Charisma is not wasted** on a paladin dip in a duo — it feeds Aura of Protection, oath DCs,
  Aura of Hate / Scornful Rebuke / Silvered Rebuke damage, *and* the party's dialogue checks,
  which one of two characters has to carry.

---

## Not present

Confirmed absent from the 10.2 mod TSV and manifest. All four of the first group were removed in
**v9.0.3**:

- **Blackguard — A Homebrew Dark Paladin Class.** Changelog v9.0.3: *"REMOVED Blackguard. Play an
  Oathbreaker or Bleakwalker."* No Blackguard entry in the TSV or manifest. Goon's Paladin
  Overhaul still contains dormant Blackguard compatibility code (Profane Smite / Improved Profane
  Smite support), which is harmless but will make search hits look like it is present — it is not.
- **Oath of Zeal.** Removed v9.0.3. (`Amonkhet - Zeal Domain - Cleric Subclass` (`9089`) *is*
  present — that is a **Cleric** domain, not the paladin oath. Do not confuse them.)
- **Oath of the Phoenix.** Removed v9.0.3.
- **Oath of the Storm.** Removed v9.0.3.
- **Oath of Redemption.** Removed earlier (*"console spam from outdated code plus bugs"*).
- **Quickened Oaths** and **Non-Concentration Smites** (standalone mods). Removed v9.0.3 as
  *"redundant with Listo's master spell patcher."* The *effects* survive; the mods do not.
- **Unholy Oathbreakers.** Superseded by `Unholy Smite for Oathbreakers` + `Improved Unholy Smite
  for Oathbreakers`.
- **No Divine Smite for Oathbreakers** as a standalone mod. Superseded by the optional file inside
  `Goon's Paladin Overhaul` (which *is* pulled — the effect is live).
- **Visual Paladin Auras** / **Paladin Visual Aura** / **Increase Paladin Aura Range.** All
  removed; the 9m/15m radii now come from a Listo-internal patch, and there is no in-game aura
  visualisation.
- **Respec Spell** and **Appearance Edit Enhanced.** Neither is in 10.2 — this is what makes the
  Oathbreaker respec block bite.
- **Oath of Treachery**, **Oath of the Watchers**, **Oath of Glory**: never in the list.

---

## Cross-references

- **Feats** — `data/listo-10.2-feats.md`. Read the **Durable** entry (full HP on every short rest
  plus Listo's in-combat regen below 60% HP) and **Mage Slayer**; the docs name Durable + Mage
  Slayer on a Paladin as an anchor/tank package. Note the ability-score cap of 20 is removed by
  `Feats Overhaul` (`15044`), which matters for a Charisma-scaling aura.
- **Equipment** — `data/listo-10.2-equipment.md`. `Lathander's Armory` (`4711`, shields/armour/
  books for Cleric/Paladin) and `Helm's Armory` (`6345`, shield and longsword for Paladin/Cleric)
  are both in the list and covered there, as are The Blood of Lathander (converted to a
  morningstar) and Sword of the Rising Dawn.
- **Races** — `data/listo-10.2-races.md`. Relevant to Oathbreaker: `Ghastly Ghouls — Playable
  Undead` (`5895`) is the only way a *partner* benefits from Aura of Hate, but the undead tag
  blocks most healing.

## Verification notes

- Every oath above is confirmed present via the TSV **and** a manifest archive entry (except the
  four vanilla oaths, which are base-game content reached through `Expansion`).
- Every modded paladin mod Listo pulls is at the **current Nexus version** except `Expansion`
  (`279`), which is at **1.7.3.6** against a current **1.7.3.10**.
- Items marked **(unverified)** are: Listo's aura-radius patch coverage of Oath of the Moon and
  Oath of Illumination; whether `Expansion`'s Harness Divine Power / Martial Versatility optional
  features are enabled in Listo's MCM config; Royal Decree cantrip mechanics; Oath of Illumination's
  feature list beyond "Aura of Brilliance"; Bleak Walkers' oathbreaking triggers; and whether the
  Oathbreaker Knight can grant an oath to a character who *started* as an Oathbreaker.
