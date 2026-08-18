# Listonomicon 10.2 — Inquisitor

**Mod:** `18318` Inquisitor Class, by **JL935JL**. Archive pulled by Listo 10.2:
**`Inquisitor-18318-2-2-0-1779926434.zip`** (version **2.2.0**), installed as a single pak
`PFInquisitor.pak` under `mods\Inquisitor Class\PAK_FILES\`. No Listo patch or override for
this mod appears anywhere in the 10.2 manifest — it ships as the author published it.

**Provenance.** Compiled 17 August 2026 from the mod's Nexus description, files and changelog
tabs. The Nexus page currently describes **2.2.1** (uploaded 08 Aug 2026); Listo pulled
**2.2.0** (uploaded ~28 May 2026 — see *Known issues*, this matters a great deal). The only
documented change between the two is a bug fix, so the mechanics below should describe the
installed version accurately — but read the *Known issues* section before planning a build
around this class. **This class has no D&D or BG3 baseline**: it is a homebrew adaptation of
the Pathfinder 1e Inquisitor, so nothing here is inferred from 5e. Anything the mod page does
not state is marked `(unverified)`.

A grim divine **half-caster martial** — the mod pitches it as "Paladin-shaped, but for hunting
a specific target." Its niche is single-target focus: **Judgment**, a stance-like buff aimed at
one enemy that you can rewrite mid-fight as a bonus action, and **Monster Lore**, a skill check
that identifies a weakness and loads a scaling bonus-damage die. It is Wisdom-primary, wears
medium armour and a shield, swings martial weapons, gets Extra Attack at 5, and casts from a
bespoke divine/hunter spell list topping out at 5th level. Everything it does — save DCs,
Judgment magnitude, initiative, healing, capstone — keys off Wisdom modifier.

## At a glance

| | |
|---|---|
| **Primary ability** | **Wisdom** (spellcasting; every Judgment and subclass number scales off WIS mod). Secondary: Strength or Dexterity for weapon attacks; Constitution for HP. |
| **Saves at level 1** | **Wisdom + Strength** |
| **Hit points** | 8 + CON at level 1, **5 + CON** per level after (d10-equivalent average, stated as a flat number) |
| **Armour** | Light, Medium, **Shields** |
| **Weapons** | Simple + **Martial** |
| **Skills** | Choose 2 from Arcana, Athletics, History, Investigation, Nature, Perception, Religion, Survival |
| **Caster tier** | **Half-caster.** "Wisdom-based spontaneous caster, following the same spell progression as a Ranger." Slots begin at **level 2**, not level 1. |
| **Max spell level** | **5th**, first slot at character level **17** |
| **Slots at 20 (as listed)** | 2× 1st, 3× 2nd, 3× 3rd, 3× 4th, 2× 5th. The page lists *increments*, and 1st-level slots are never incremented past 2 — one fewer tier of 1st-level slots than a real Ranger. `(possible page omission — unverified)` |
| **Resource cadence** | **Judgment charges restore on SHORT REST** (2 at L1, then +1 at 5/10/15/20 → 6 max). Also restored by Potion of Angelic Slumber, Potion of Angelic Reprieve, Illithid Restoration Pods, and Divine Intervention: Opulent Revival. Spell slots are long-rest. Supreme Judgment (L18) is 1/long rest. |
| **Key breakpoints** | **1** Judgment + saves + martial/shield + deity weapon · **2** spellcasting, Monster Lore, WIS to initiative · **3** subclass + permanent Detect Thoughts · **5** Extra Attack + Sanctified Slayer · **6** Hallowed Blade (Radiant/Necrotic conversion) · **11** two Judgments at once |
| **Dip value** | **High at 1 and 2**, very high at 3. Best Wisdom-save opener in the list that also brings martial weapons and shields. |
| **Feats** | The class's *native* feat levels are 4/8/12/16/19, but Listo overrides feat cadence globally to **3/6/9/12/13/15/18** via `Universal Feat Every X Level(s) - MCM` (`13193`) — see `listo-10.2-feats.md`. Whether that mod's selectors land cleanly on a modded class (and whether the class's own 4/8/12/16/19 selectors survive alongside them, which would be extra feats) is `(unverified — check the level-up screen in-game)`. |

## Class tagging

The mod states this plainly, and it is narrower than it sounds:

> "The Inquisitor is tagged as both a Cleric and a Ranger **for dialogue purposes**."

- **Dialogue:** yes, this is the intended and only claimed effect. You get [CLERIC] and
  [RANGER] dialogue options. Listo ships the **DART Framework** (`17561`, confirmed present in
  `listo-10.2-mods.tsv`), which the author names as the optional dependency that relabels
  those options as **[INQUISITOR]**. So in Listo you should see [INQUISITOR] tags.
- **Spell lists:** **no effect.** The Inquisitor has its own bespoke, hand-written spell list
  (reproduced under *Core mechanics*). It does not draw from the Cleric or Ranger list, does
  not get Cleric cantrips, and does not get a Cleric domain.
- **Multiclass spell-slot progression:** `(unverified)`. The mod never addresses multiclassing.
  A half-caster *should* contribute half its levels to the shared slot table, but modded
  classes routinely fail to register in BG3's multiclass slot maths and instead keep a separate
  pool. **Verify on the character sheet before committing to an Inquisitor/Cleric or
  Inquisitor/Paladin caster split.**
- **Class-restricted gear:** `(unverified, and worth testing early)`. Listo has real
  Cleric-restricted items — JWL Discordant Instruments' holy symbols for Clerics/Paladins,
  Lathander's Armory (`4711`) and Helm's Armory (`6345`) gear (see
  `listo-10.2-equipment.md`). Whether an Inquisitor can equip them depends on whether each
  item checks the **class tag** (in which case the Cleric tag likely satisfies it) or the
  **class UUID / progression** (in which case it will not). The mod author claims the tags are
  for dialogue only, which argues against relying on this. Treat any Cleric-gated item as
  **unavailable until proven otherwise in-game**.
- **Deity selection is enabled** on the class independently of the tagging — that is an
  explicit class feature, not a side effect of the Cleric tag.

## Core mechanics

### Judgment (level 1)

Cast at a single target. Lasts **the whole combat or until the target dies**, and you may
**switch which Judgment is active as a bonus action** — this is the core loop: retune the buff
to the fight in progress. Six options, all scaling off Wisdom modifier (**rounded up**, changed
in 2.1.0):

| Judgment | Effect |
|---|---|
| **Conviction** | Target takes a penalty to saves against you = half your WIS mod |
| **Destruction** | You deal bonus damage to the target = your WIS mod |
| **Justice** | Bonus to all attack rolls against the target = half your WIS mod |
| **Protection** | Target takes a penalty to attack you = half your WIS mod |
| **Purity** | Bonus to all saves against the target = half your WIS mod |
| **Resiliency** | All damage the target deals you is reduced by your WIS mod |
| **Stern Gaze** | Proficiency in Insight and Intimidation; use WIS instead of CHA for Intimidation if higher |

Note **Stern Gaze is a Judgment slot**, not a passive — it costs you your combat buff, but out
of combat it is a free skill package.

Action cost of the initial Judgment cast is not stated on the page `(unverified — switching is
explicitly a bonus action)`. As of 2.0.0 there is **no range limit** on the target.

### Monster Lore (level 2)

Two parts. Passive: **add half your WIS mod (rounded up) to Intelligence-based skill checks you
are proficient in.** Active: **bonus action**, roll a skill check against the target — the skill
depends on creature type — DC **8 + half the target's level**, with **advantage if the target is
Judged**. On a success the next damage you deal that target adds **1d8**, rising to **2d8 at
level 3, 3d8 at level 7, +1d8 every 4 levels thereafter**, and this damage **ignores resistance
and immunity**. Scales with **Inquisitor level, not character level** (2.0.0) — so it does not
grow on a dip.

Unlimited uses, but **once per target per long rest** (Vengeance lifts this). The first time
each round you damage a Judged target you **auto-roll** Monster Lore against it if it has not
been identified yet, so in practice the bonus action is often free.

Skill by creature type: Arcana — Aberrations, Celestials, Constructs, Elementals, Fey, Fiends ·
Nature — Beasts, Monstrosities, Oozes, Plants · History — Dragons, Giants, Humanoids ·
Religion — Undead.

### Deity weapon (character creation)

Deity selection is enabled, and grants **+1 to attack and damage rolls with one specific weapon**
(the deity's 3e favoured weapon), plus that weapon in your starting gear. Selected examples:
Lathander/Selûne → Morningstar; Helm/Kelemvor/Eilistraee → Longsword (Bastard Sword);
Tempus/Garl Glittergold → Battleaxe; Moradin/Laduguer → Warhammer; Mielikki → Scimitar;
Lolth/Mystra/Tymora → Dagger; Bahamut/Tiamat → War Pick; Talos/Gruumsh → Trident;
Yondalla → Shortsword.

**Ilmater (and Bane) instead grant Improved Unarmed Strike: your unarmed strikes follow the
progression of a Monk of your *character* level, including becoming Magical at level 6.** That
is the single most abusable line on the page — it is granted at level 1 and keyed to character
level, not Inquisitor level, so a **1-level dip hands any unarmed build full Monk unarmed
scaling**. Worth verifying in-game before building around it.

Modded-deity support: Bane, Bhaal, Myrkul, Shar are noted as tested with **Deities Restored**
(Koriik) — **not present in the 10.2 list**; Shar's sickles become chakrams only with **Shar's
Chakrams** — also **not in the list**. The Raven Queen entry works via **Playable Shadar-kai**
(`21382`), which **is** in the list.

### Spellcasting (level 2+)

Wisdom-based spontaneous casting on a Ranger-like curve. Number of spells known is not stated
`(unverified)`. Bespoke list:

- **1st:** Bane, Charm Person, Command, Compelled Duel, Disguise Self, Divine Favour, Ensnaring
  Strike, Heroism, Hunter's Mark, Protection from Evil and Good, Shield of Faith
- **2nd:** Calm Emotions, Hold Person, Lesser Restoration, Magic Weapon, **Misty Step**,
  Protection from Poison, See Invisibility, Silence, Spiritual Weapon
- **3rd:** Bestow Curse, Crusader's Mantle, **Counterspell**, Daylight, Elemental Weapon, Fear,
  Remove Curse, Speak with Dead, **Spirit Guardians**
- **4th:** Banishment, Confusion, Death Ward, Guardian of Faith
- **5th:** Contagion, Destructive Wave, Dispel Evil and Good, **Dominate Person**, Greater
  Restoration, **Hold Monster**, Planar Binding

Plus **custom spells**, one per spell level shared by all subclasses and one per level per
subclass — most notably **Consecrate/Desecrate** (1st, 6m aura, ally heal +1/+1 or enemy 1d4
necrotic −1/−1), **Guarding Knowledge** (2nd, identified enemies have disadvantage to hit you
and you have advantage on saves against them), **Judgment Light** (3rd, a 9m burst whose effects
depend on which Judgments are active — the Purity mode heals WIS-mod d8s and grants 3 rounds of
Charm/Fear/Confusion immunity), **Sacred Nimbus** (4th, half damage from enemy spells,
disadvantage on ranged attacks from outside, retaliation damage), and **Bestow Grace** (5th,
target adds your **WIS mod to attack rolls, damage, saves and AC**, or cast on yourself for
True Judgment + immunity to Charm/Compulsion/Fear/Disease/Poison).

2.0.0 added spell support for **Spells Extra** (`11291`, in the list) and Dawnstar's Grimoire /
Telekinetic / Necromancy spell packs `(presence in 10.2 not checked here)`.

### Level progression (base class)

| Lvl | Feature |
|---|---|
| 1 | **Judgment** (2 charges, short rest), deity weapon, WIS+STR saves |
| 2 | **Monster Lore**, **Righteous Vigilance** (add WIS mod to initiative *in addition to* DEX), **Spellcasting** (2× 1st) |
| 3 | **Interrogative Mind** (permanent Detect Thoughts), **Inquisitorial Order** (subclass) + subclass feature |
| 4 | Feat (native) |
| 5 | **Extra Attack**; **Sanctified Slayer** (expend a spell slot → until short rest, Judgment may target additional creatures equal to the slot level); 3rd Judgment charge; 2× 2nd-level slots |
| 6 | **Hallowed Blade** — your weapon may deal **Radiant or Necrotic** instead of its normal damage type |
| 7 | Subclass feature; 3rd 2nd-level slot |
| 8 | Feat (native) |
| 9 | 3rd-level slots |
| 10 | **Supernal Celerity** — at combat start gain **Momentum** equal to the lower of your proficiency bonus or WIS mod `(what a stack of Momentum does is BG3's movement-speed status; exact magnitude unverified)`; 4th Judgment charge |
| 11 | **Second Judgment** — activate **two** different Judgments for one charge, switchable independently |
| 12 | Feat (native) |
| 13 | 4th-level slot |
| 14 | **Exploit Weakness** — crits on a Judged target ignore resistances and the target **cannot regain hit points** for WIS-mod rounds |
| 15 | Subclass feature; 5th Judgment charge |
| 16 | Feat (native) |
| 17 | 5th-level slot (max spell level reached) |
| 18 | **Supreme Judgment** — 1/long rest, functions as **all Judgments at once** on one target; your WIS is treated as 1 higher per Judged target killed since your last long rest |
| 19 | Feat (native) |
| 20 | Subclass capstone; 6th Judgment charge |

## Subclasses

Three, chosen at level 3, with features at **3, 7, 15, 20**.

### Tactics Inquisition

- **Mechanics:** L3 **Shared Judgment** — once per short rest, an ally gains **all** your active
  Judgments, switching in lockstep with yours; it drops if either of you is incapacitated. L3
  **Tempered Champion**, choosing one Judgment upgrade at **3, 9 and 15**, which apply *only to
  the shared ally*: Conviction → target has disadvantage on saves vs the ally's spells;
  Destruction → ally's crits add WIS-mod d6s; Justice → ally's crit threshold drops by
  min(PB, half WIS); Protection → ally gains Displacement, **Blur** from level 11; Purity → ally
  has advantage on saves vs the target's spells; Resiliency → ally gains temp HP = your
  Inquisitor level each turn, plus **physical resistance** while those persist from level 11.
  L7 **Battle Acumen** — **+1 to attack rolls, saves and AC per ally within 9m benefiting from a
  Judgment**, a reaction attack when such an ally crits, and (for a Judgment charge) the ally
  gets Battle Acumen too; Sanctified Slayer now extends Shared Judgment to more allies. L15
  **Blood for the Inquisition** — once per target per round, after a shared ally damages a Judged
  target, a *different* shared ally's next attack has advantage on attack **and damage** and
  **heals for the damage dealt**; Shared Judgment's cooldown drops to **once per combat**. L20
  **Shared Divinity** — share **Supreme Judgment**, and Battle Acumen becomes **+2 per ally** and
  also applies to damage rolls and **spell save DC**. Subclass spells: Saving Grace (1st,
  reaction, spend Shared Judgment to reroll an ally's failed save), Contagious Zeal (2nd,
  +1d4 attack/damage, temp HP, fear immunity, spreads), Flames of the Faithful (3rd, ally's
  weapons +1d8 fire, **1d12 ignoring resistance** if the target is Judged), Vindicator's Shield
  (4th, **+3 AC and saves**, Charm/Compulsion immunity, transferable), Wake of Light (5th).
- **Duo relevance:** Structurally the duo subclass — every feature reads "ally" and you have
  exactly one — but that is also its ceiling: the "per ally within 9m" scaling on Battle Acumen
  caps at **+1** (+2 at level 20) with one partner unless summons count `(unverified)`. Shared
  Judgment doubling Destruction/Justice/Resiliency onto the other player is real, short-rest
  priced, and free once per combat at 15.

### Vengeance Inquisition

- **Mechanics:** L3 **Monster Tactician** — **Expertise** in one Intelligence skill and **double
  your WIS mod** on checks with it. L3 **Divine Scourge** — bypasses the once-per-target limit on
  Monster Lore (recasts need no check and **refund the bonus action**), and marks the target as
  your **Vengeful Quarry**; against a target that is both Judged and your Quarry, each Judgment
  gains the same upgrades Tactics grants its ally, but **for you**: Conviction → disadvantage on
  saves vs your spells, Destruction → crits add WIS-mod d6s, Justice → crit threshold −min(PB,
  half WIS), Protection → Displacement then **Blur** at 11, Purity → advantage on saves vs its
  spells, Resiliency → the first attack against you each round from the Quarry deals **half
  damage**. L7 **Studied Combat** — identifying a creature auto-rolls Investigation; on success
  your **first attack each round has advantage and all damage against it is rolled with
  advantage**; Sanctified Slayer also grants +1 damage and +1 INT-skill per slot spent. L15
  **Inquisitor's Edge** — reaction to contest an incoming attack with Insight (forcing a
  penalised reroll), reaction to reroll a failed save against a Judged enemy, and reaction to
  **teleport to your Quarry when it teleports**. L20 **Third Judgment** — three Judgments per
  charge. Subclass spells: Hunter's Lore (1st), Castigation (2nd, Command: Grovel plus escalating
  1d6 fire+radiant), Righteous Condemnation (3rd, reaction, 4d8 radiant retaliation),
  Mark of Justice (4th, no-save stacking **−1 to all ability scores**), Holy Sword (5th).
- **Duo relevance:** The self-sufficient pick — the highest personal single-target damage and the
  only one whose defensive layer (Insight-contest reroll on attacks *and* saves at 15) is a
  **reaction**, which Lone Wolf's extra Reaction lets you use twice a round.

### Zeal Inquisition

- **Mechanics:** L3 **Crusader's Conviction** — in-combat **fast healing** for half your
  Inquisitor level at end of turn, computed from **both CON and WIS**; at 9 it is your full
  Inquisitor level and adds Lesser Restoration and **cannot be blocked by anti-healing effects**;
  at 15 it becomes **regeneration that persists while incapacitated** and adds Lesser + Greater
  Restoration. L3 **Unyielding Resolve** — a **delayed damage pool** holding up to 25% of your max
  HP: damage goes into the pool and lands at the end of your next turn (overflow hits normally),
  and you gain **+1 to saves per 5 points in the pool**; excess healing at full HP flows into the
  pool, so fast healing can erase damage before you ever take it. L3 **Wrathful Taunt** — Judged
  enemies have **disadvantage attacking anyone but you**. L7 **Ardent Protector** — for WIS-mod
  rounds you **absorb 100% of damage dealt to a linked ally**, falling 25% per 3m of separation;
  Sanctified Slayer adds +10 pool capacity and a 10% crit-negation chance per slot level. L15
  **Guardian's Counterstrike** reaction — a Judged enemy attacking an ally makes a WIS save or the
  attack is negated and it cannot target that ally for WIS-mod rounds (on a success it is immune
  to further uses against that ally); plus, once per short rest, **discharge the pool** as damage
  to all Judged enemies within 18m (CON save halves) while taking 150% yourself. L20 **Deathless
  Zealot** — doubled Unyielding Resolve bonuses below 10%-per-WIS-point health, Force damage
  reflected to anyone hitting a protected ally, and **resistance to all damage while the pool is
  full**. Subclass spells: Blood Armor (1st), Blood Rage (2nd, up to **+10 STR / −5 AC**),
  Deadly Juggernaut (3rd), Resurgent Transformation (4th, auto-triggers below 25% for +4 physical
  stats, DR 5, **Haste** and a heal — then Stunned 2 rounds and 2d4 CON/WIS damage until long
  rest), Iron Body (5th, crit/stun/blind/poison immunity, +6 STR / −6 DEX, halved movement).
- **Duo relevance:** The direct answer to "losing either character usually ends the fight."
  Ardent Protector plus Wrathful Taunt plus fast healing means the other player is very hard to
  kill while you stand next to them. The self-healing is long-rest-free sustain, which matters
  when a long rest costs 120+ supplies.

## Dip value

**Level 1 — strong.** Saving throw proficiencies come only from your level-1 class, and
Inquisitor grants **Wisdom** (the top priority in this skill's ordering) plus **Strength**. That
package is one rung below Cleric's WIS+CHA on the second save, but Inquisitor pays you for it:
**martial weapons, medium armour and shields** at level 1, the deity weapon's +1/+1 (or Monk-rate
unarmed strikes on Ilmater), and **Judgment** — 2 uses restored on a **short rest**, exactly the
resource cadence this run wants. On a low-WIS character the Judgment numbers (half WIS mod)
are near-worthless, but Resiliency/Destruction still key off full WIS mod and Stern Gaze's skill
proficiencies do not scale at all.

**Level 2 — the sweet spot for a Wisdom character.** **Righteous Vigilance stacks WIS mod onto
initiative on top of DEX**, which on a WIS-primary build is a large, permanent, always-on bonus,
and going first is worth more in a two-character party than in a four-character one. Spellcasting
opens here (2× 1st, Hunter's Mark / Shield of Faith / Divine Favour). Monster Lore's damage die
stays 1d8 on a dip, but the passive half-WIS to proficient INT skills does not care about level.

**Level 3 — feat-neutral and adds a subclass.** Listo's 3/6/9/12/13/15/18 cadence means three levels
cost you no feats, and level 3 gives **permanent Detect Thoughts** (Interrogative Mind) plus a
full subclass feature — Vengeance's Expertise + double-WIS on an INT skill is a genuine
skill-monkey package, and Zeal's fast healing + delayed damage pool is a real defensive layer on
a martial chassis.

**Beyond 3**, take it as a main class or not at all: Extra Attack at 5, Hallowed Blade at 6, and
Second Judgment at 11 are what make the class, and Monster Lore's dice scale only with Inquisitor
level.

**On the "Listo lacks Wisdom-primary options" claim — honestly:** Cleric and Druid already exist
and both grant Wisdom save proficiency at level 1, so Inquisitor does not fill a *hole* in the
save department. What it actually adds is a **Wisdom-primary full martial** — martial weapons,
shields, Extra Attack, half-casting — which Cleric only approximates through War/Nature domain
and Druid not at all. If you want a Wisdom SAD frontliner whose defensive numbers rise with the
same stat as its DCs, this is the cleanest option in the list. It is not a reason to prefer WIS
over CHA builds generally.

## Not present / known issues

- **CONFIRMED IN THE INSTALLED PAK: the level 3 progression references a subclass that does not
  exist.** Unpacked `PFInquisitor.pak` from the live install (18 Aug 2026). `meta.lsx` reports
  `Version64` = **2.2.0.0**, so the installed build is 2.2.0 regardless of the filename. The base
  class progression node for **Level 3** lists **four** `SubClass` objects:

  | GUID | Resolves to |
  |---|---|
  | `4dc44aca-29ec-4fe5-8d34-bc58c8d7c269` | TacticsInquisitor |
  | `81e4c08b-ce20-4c3f-bad4-959966432f1c` | VengeanceInquisitor |
  | `e115216d-f6f8-4034-bca5-e06cd1e95dfe` | ZealInquisitor |
  | **`040e41b0-e197-4856-a7c3-f7093ae85f0b`** | **nothing — no ClassDescription anywhere** |

  That GUID occurs **exactly once in the whole pak**, in the reference itself, and in **none** of
  the 2,541 other sub-6 MB paks in the installed modlist — so no Listo patch or other mod defines
  it. **Level 3 is the first level that builds the subclass list**, which is precisely the level
  the upstream bug report names. Treat the dangling reference as the mechanical cause until
  someone levels an Inquisitor past 2 in game and proves otherwise.

- **Listo 10.2 ships version 2.2.0, and 2.2.0 appears to contain a level-up-breaking bug.**
  The 2.2.1 changelog reads: *"Fixed a critical error preventing anyone from leveling up past 2
  (how did no one report this for 72 days)."* The dating lines up exactly: the archive filename's
  trailing timestamp `1779926434` resolves to **28 May 2026**, 2.2.1 was uploaded **8 Aug 2026**,
  and 28 May + 72 days = 8 Aug. **2.2.0 is also absent from the mod's "old files" list**, which is
  what an author does with a version they consider broken. No Inquisitor patch exists anywhere in
  the 10.2 manifest.
  **Treat the installed Inquisitor as unusable past level 2 until proven otherwise.** The cheap
  test is to create an Inquisitor and try to take level 3. If it fails, the fix is to manually
  drop 2.2.1's pak in over the installed one — a single-pak mod with no Listo patch, so the
  swap is low-risk `(the exact scope of the bug — Inquisitors only, or any character in the
  party — is not stated on the page; the wording "anyone" is ambiguous)`.
- **`8931` Inquisition Domain Cleric Subclass is a completely different mod** — Grim Hollow's
  Inquisition Domain, by **havsglimt**, a Cleric domain. Different author, different mod, no
  shared content, no documented interaction beyond both being in the list. Listo's changelog
  mentions a Chizfreak compatibility patch covering Inquisition **Domain**; nothing in the
  changelog touches the Inquisitor **class** beyond "ADDED Inquisitor class."
- **Optional dependencies:** AnimationUnlocker (`16058`) is present, so animations should be
  complete. DART (`17561`) is present, so dialogue tags should read [INQUISITOR]. **Deities
  Restored** and **Shar's Chakrams** are **not** in 10.2 — the modded-deity weapon entries for
  Bane/Bhaal/Myrkul/Shar are unverified in this list, and a Shar Inquisitor gets sickles rather
  than chakrams.
- **Unverified and worth checking in-game:** multiclass spell-slot stacking; whether the class
  satisfies Cleric-restricted gear checks (JWL holy symbols, Lathander's/Helm's Armory — see
  `listo-10.2-equipment.md`); whether Listo's universal feat cadence and the class's native
  4/8/12/16/19 feat selectors both fire; the action cost of casting Judgment; the number of
  spells known per level; the size of a Momentum stack; and whether summons count as "allies"
  for Tactics' Battle Acumen.
- **Respec warning from the author:** versions 1.3.0 and 2.0.0 both demanded "RESPEC OUT OF
  INQUISITOR BEFORE UPDATING." If the class is ever updated mid-run, respec first.
