# Listonomicon 10.2 — Classes and Subclasses

**Index and summary. Full detail lives in `data/classes/<class>.md`** — one file per class, with
every subclass's mechanics, level breakpoints, dip value, and what is *not* present.

**156 subclasses across 17 classes.** Grep this file to pick a class; open the class file to
plan with it.

```bash
S=~/.claude/skills/listo-build     # or the plugin path

grep -i -A3 "^| \*\*Cleric" "$S/data/listo-10.2-classes.md"    # one class at a glance
grep -i "short rest" "$S/data/classes/"*.md                    # by resource cadence
grep -i -B2 -A6 "Dream Domain" "$S/data/classes/cleric.md"     # one subclass
grep -il "heavy armour" "$S/data/classes/"*.md                 # which classes grant what
```

**Provenance.** Compiled 17 August 2026 by 17 parallel research passes, one per class. Every
subclass was confirmed present in `listo-10.2-mods.tsv` and/or as an installed `.pak` path in
`listo-10.2-manifest.json`. Mechanics come from mod pages, and where a page was unusable, from
the mod's own source or shipped data (Artificer from the author's GitHub at the matching tag;
Blood Hunter by unpacking the shipped `.pak`). Anything unconfirmed is marked `(unverified)` in
the class file.

---

## Read this before recommending anything

### ⚠ Inquisitor is probably broken

Listo pulled `Inquisitor-18318-**2-2-0**`. Nexus is on **2.2.1**, whose sole changelog entry is
*"Fixed a critical error preventing anyone from leveling up past 2."* Dating corroborates: the
archive resolves to 28 May 2026, 2.2.1 shipped 8 Aug 2026, and the author's stated 72-day gap
matches exactly. **No patch exists in the manifest.** Treat the class as unusable past level 2
until tested in-game. It passes every "does it exist" check, which is exactly why it is
dangerous.

### ⚠ Mod pages' feat tables are all wrong for Listo

`Universal Feat Every X Level(s)` (`13193`) overrides every class mod's own cadence. Paragon's
page says 4/8/12/16/19; Mesmerist's says the same; `Expansion` grants its own at 14/16/19; Blood
Hunter has native ASIs at 4/8/12/16/19. **All are overridden.** Plan against **3/6/9/12/15/18**,
plus **11** for Fighter, Rogue and Mesmerist. Whether any of them *stack* rather than replace is
`(unverified)` and worth one in-game check.

### ⚠ Archive versions lag mod pages, sometimes deliberately

Several mods are pinned behind their documentation because newer versions need a newer Goon's
Library than Listo ships (4.9.0.0). The mod page therefore describes features **not in this
build**. Worst offenders: Goon's Rogue Overhaul (1.2.2.0 vs 2.1.0.1 — two majors), Goon's
Barbarian (1.1.3.6 vs 1.2.0.0), Goon's Bard (1.0.1.1 vs 1.1.0.0), Eldritch Knight Plus (5.2 vs
5.3), Expansion (1.7.3.6 vs 1.7.3.10). Each class file records its own drift.

### The docs name three mods that are not installed

`Blessing of the Trickster` (`11566`), `Second-Story Work Dexterity Jump` (`6331`) and
`Experimental Alchemy as a Feat` (`12446`) are all described in the Listo docs and are **absent
from both the index and the manifest**. Verify before repeating a doc claim.

---

## The roster

| Class | Subs | Level-1 saves | Caster | Feats | Opens or dips? |
|---|---:|---|---|---:|---|
| **[Barbarian](classes/barbarian.md)** | 14 | Str + Con | — | 6 | Rage is **long-rest only** — the binding constraint here |
| **[Bard](classes/bard.md)** | 8 | Dex + Cha | Full | 6 | **Dip 3** — College, Expertise ×2, 3 proficiencies |
| **[Cleric](classes/cleric.md)** | **20** | Wis + Cha | Full | 6 | **Open 1** — armour comes from the *domain*, not the class |
| **[Druid](classes/druid.md)** | 11 | Int + Wis | Full | 6 | Summons are the argument; non-concentration, until long rest |
| **[Fighter](classes/fighter.md)** | 14 | Str + Con | 1/3 (EK) | **7** | **Open 1** for heavy armour + saves; **dip 2** for Action Surge; **11** is the best single level in the list |
| **[Monk](classes/monk.md)** | 11 | Str + Dex | — | 6 | Ki on short rest; **WIS is now the primary stat** |
| **[Paladin](classes/paladin.md)** | 9 | Wis + Cha | Half | 6 | Auras hit both characters. **Oathbreaker blocks respec** |
| **[Ranger](classes/ranger.md)** | 11 | Str + Dex | Half | 6 | **Dip 3** — Beast Master companion moved to level 3 by Expansion |
| **[Rogue](classes/rogue.md)** | 10 | Dex + Int | 1/3 (AT) | **7** | **Dip 3** — subclass, Expertise, Sneak Attack. **11** is huge |
| **[Sorcerer](classes/sorcerer.md)** | 7 | Con + Cha | Full | 6 | **Dip 2** Font of Magic, **3** Metamagic (Twinned, Quickened) |
| **[Warlock](classes/warlock.md)** | 6 | Wis + Cha | Pact | 6 | **The default dip.** Short-rest slots; 1/2/3/5 all buy something |
| **[Wizard](classes/wizard.md)** | 15 | Int + Wis | Full | 6 | Necromancy answers action economy; robe-shaped defensively |
| **[Artificer](classes/artificer.md)** | 4 | Int + Con | Half | 6 | **Open 1** — the multiclass node grants far less. Firearms framework |
| **[Mesmerist](classes/mesmerist.md)** | 3 | Dex + Cha | Half | **7** | **Dip 2** — Towering Ego scales on CHA, not class level |
| **[Paragon](classes/paragon.md)** | 6 | Con + Cha | None | 6 | **Open 1** for saves/skills/heavy armour; a late dip still gives the rest |
| **[Inquisitor](classes/inquisitor.md)** | 3 | **Wis + Str** | Half | 6 | ⚠ **likely broken past level 2** |
| **[Blood Hunter](classes/bloodhunter.md)** | 4 | Int + Dex | — * | 6 | Everything on short rest. **No CON save.** mod.io, not Nexus |

\* Profane Soul only: short-rest INT pact slots, capped at spell level 4.

---

## Saving throws by level 1 class

Only your **first** class grants these, and a respec silently re-picks them. Ordered by the
save-value ranking in `references/listo-rules.md` — Wisdom > Constitution ≈ Dexterity >
Charisma > Strength > Intelligence.

| Save | Granted by |
|---|---|
| **Wisdom** | Cleric, Druid, Paladin, Warlock, Wizard, **Inquisitor** |
| **Constitution** | Barbarian, Fighter, Sorcerer, Artificer, Paragon |
| **Dexterity** | Bard, Monk, Ranger, Rogue, Mesmerist, Blood Hunter |
| **Charisma** | Bard, Cleric, Paladin, Sorcerer, Warlock, Paragon, Mesmerist |
| **Strength** | Barbarian, Fighter, Monk, Ranger, **Inquisitor** |
| **Intelligence** | Druid, Rogue, Wizard, Artificer, Blood Hunter |

**The Charisma trap:** seven classes grant Charisma at level 1. Putting Lone Wolf's +4 on
Charisma alongside any of them wastes a grant. **Mesmerist escapes it** by granting Dex + Cha —
the two a Charisma build most wants — leaving the +4 free for **Con + Wis** and yielding four
proficiencies across the top of the ordering.

**Blood Hunter grants no Constitution save**, unusually for a d10 martial — relevant given
concentration and the duo's low tolerance for losing a character.

---

## Rest cadence — the duo's real axis

Long rests cost 120+ camp supplies scaling with **camp population**, so a two-person party pays
full price for half the refuel. Short-rest classes are worth more here than their raw numbers.

| Refreshes on short rest | Long rest only |
|---|---|
| **Warlock** pact slots — the headline | **Barbarian** Rage — nothing in 706 mods moves it |
| **Monk** ki, and every Way prices in ki | **Wizard / Sorcerer / Cleric / Druid / Bard** slots |
| **Blood Hunter** — everything | **Paladin** spell slots (Channel Oath varies by oath) |
| **Fighter** Second Wind, Action Surge | **Lucky**, most feat resources |
| **Cleric** Channel Divinity (Twilight especially) | |
| **Druid** Circle of the Stars via `Star Druid Tweaks` | |
| **Wizard** Signature Spells at 20 (short *and* long) | |
| **Ritual Caster** feat — 20% slot recovery per short rest | |

---

## `(DTO) Otherworldly Archetypes` — the biggest gap in the old notes

Mod `21822` ships **12 subclasses, one per vanilla class**, and `references/listo-rules.md`
never mentioned it. Added in v9.0.3 "for testing", pulled at `1.2.0.67` while the author's own
docs site only covers `1.2.0.65` — so two versions of changes are undocumented upstream.

| Class | Subclass | Class | Subclass |
|---|---|---|---|
| Barbarian | Path of the Revenant | Paladin | Oath of Illumination |
| Bard | College of Stormcalling | Ranger | Conclave of the Dawnstriders |
| Cleric | Dream Domain | Rogue | Seeker |
| Druid | Circle of Wrath | Sorcerer | Wretched Soul |
| Fighter | Chronoknight | Warlock | The Psyker |
| Monk | Way of the Friar | Wizard | School of Bombardment |

Two carry real drawbacks worth reading before picking: **Path of the Revenant cannot be healed
by any means while raging** (and the rage cannot be ended early), and **The Psyker drains max
HP**. No Artificer content.

---

## Cross-cutting mods that change many classes at once

- **`Expansion` (`279`)** — level 13–20 for every base class, and far more besides. Its Tasha's
  optional features are **on by default**. It moves Beast Master's Companion's Bond to level 3,
  adds Magical Secrets tranches at 14 and 18, restores Divine Intervention at 20, and supplies
  Spell Mastery and Signature Spells. **Do not judge it by its name.**
- **Goon's overhauls** — Barbarian, Bard, Cleric, Paladin, Rogue, Wizard. All pinned behind
  their pages by the Goon's Library version Listo ships.
- **`Universal Feat Every X Level(s)` (`13193`)** — overrides every class's native feat cadence.
- **`Cat's Cleric Changes` (`21257`)** — written for Listo; gives **War Domain a real Extra
  Attack at 6**, which breaks the docs' "Clerics never get Extra Attack" framing.

---

## Purged in v9.0.3 — do not recommend

Confirmed absent from the index and manifest by the relevant class pass:

| Class | Removed |
|---|---|
| Bard | Whispers |
| Sorcerer | Frozen Sorcery, Spellfire Sorcery |
| Warlock | Sorcerer King, Undead, Fathomless, Genie, Star |
| Wizard | Hedge Mage, Graviturgy |
| Paladin | Blackguard, Oath of Zeal, Oath of Phoenix, Oath of Storm |

Two false positives to avoid: **`Amonkhet - Zeal Domain` (`9089`) is a Cleric domain**, not the
purged Oath of Zeal; and **`Inquisition Domain` (`8931`) is a Cleric domain** unrelated to the
`Inquisitor` class (`18318`).

Also not installed despite appearances: **UA6 Swashbuckler** (only the Cunning Strike file was
pulled — the Swashbuckler you can pick is Larian's, and it gets **no 13–20 features**), and
**Way of the Drunken Master** (two installed mods still ship features for it, which reads as
evidence it exists).

---

## Things that are vanilla, not mods

Easy to miscredit, and each one wasted research time somewhere:

**Bladesinging** (Wizard), **Swarmkeeper** (Ranger), **Hexblade** (Warlock), **Path of the
Giant** (Barbarian), **Swashbuckler** (Rogue) — all shipped by Larian in Patch 8. Companion
mods that touch them (`Remove Swarmkeeper VFX`, `Way of Shadow Revised - Katanas`) are cosmetic
or standalone and are **not** the subclass.
