# Listonomicon 10.2 — Races

Every playable race and subrace added by the shipped 10.2 list, plus the vanilla-changing race
mods. **Grep this file; don't read it whole.**

```bash
S=~/.claude/skills/listo-build     # or the plugin path

grep -i -A8 "^### Lizardfolk" "$S/data/listo-10.2-races.md"     # one race
grep -i "resistance" "$S/data/listo-10.2-races.md"              # by mechanic
grep -i -A6 "^## Removed" "$S/data/listo-10.2-races.md"         # what's gone
```

**Provenance.** Compiled 17 August 2026. Every mod named here was confirmed present in
`listo-10.2-mods.tsv` by ModID. Mechanics come from the mod pages, which describe each mod's
**current** version — Listo may have pulled an older archive. Marked `(unverified)` where not
confirmed.

**The universal rule:** races in BG3 grant **no ability score bonuses** — the +2/+1 is assigned
freely at creation, independent of race. So a race is chosen for its *features*, never its
stats. Several mods below still describe RAW ability bonuses in their text; those are vestigial
and were removed by the authors.

---

## Elemental Power — Playable Genasi (`4741`)

Four subraces, all with **Darkvision** and innate spells that unlock with level.

| Subrace | Resistance | Level 1 | Level 3 | Level 5 |
|---|---|---|---|---|
| **Fire** | Fire | Produce Flame | Burning Hands | Flame Blade |
| **Air** | Lightning | Shocking Grasp | Feather Fall | Levitate |
| **Earth** | — (**ignores difficult terrain**) | Blade Ward | — | Pass Without Trace |
| **Water** | Acid | Acid Splash | `(not captured)` | `(not captured)` |

> Free innate casting on a martial is worth real value in a duo, where you cannot bring a third
> character to cover a gap. **Earth's difficult-terrain immunity** stacks conceptually with the
> **Mobile** feat's rework (movement speed cannot be reduced by any effect).

`Lydia's Heads Patches for Elemental Power Genasi` (`13006`) is cosmetic.

---

## Mordenkainen's Tome of Tieflings (`14885`)

Adds the **six remaining tiefling subraces** from Mordenkainen's Tome of Foes. Every one is a
Charisma-flavoured innate caster on a long-rest clock.

| Subrace | Level 1 | Level 3 | Level 5 |
|---|---|---|---|
| **Baalzebul** | Thaumaturgy | Ray of Sickness (as level 2), 1/long rest | Crown of Madness, 1/long rest |
| **Dispater** | Thaumaturgy | Disguise Self, **at will** | Detect Thoughts, 1/long rest |
| **Fierna** | Friends | Charm Person (as level 2), 1/long rest | Enthrall, 1/long rest |
| **Glasya** | Minor Illusion | `(not captured)` | `(not captured)` |
| **Levistus** | `(not captured)` | `(not captured)` | `(not captured)` |
| **Mammon** | `(not captured)` | `(not captured)` | `(not captured)` |

> The innate spells use **Charisma** and cost no slots — useful on a Charisma primary who wants
> utility without spending prepared spells. Also available on mod.io; Listo pulls the Nexus
> version.

---

## Gith

### Full Roster of Gith — Subrace Framework (`12135`)
Converts vanilla **Githyanki** into a base **"Gith"** race with subraces, retaining tags. This
is the framework the Githzerai mod plugs into.

### Followers of Zerthimon — Githzerai (`3460`)
Re-adds the monastic **Githzerai** as a subrace.

**This version's progression:** Mage Hand, Unshackle Mind and Mental Discipline at **1**;
**Shield** at **3**; **Misty Step** and Bestow Knowledge at **5**; permanent Detect Thoughts and
Insight advantage.

> **Trap:** **no Medium armour or Martial weapon proficiency**, unlike vanilla Githyanki. If you
> were relying on Githyanki's armour proficiency to free a feat, Githzerai does not supply it.

**Githyanki psionics are no longer spells** (`Githyanki Psionics`, `13920`) and can be cast
**while Silenced** — see `data/listo-10.2-feats.md`.

---

## Elves and elf subraces

All three are implemented as **elf subraces**, so they inherit the general elf traits and stay
compatible with elf cosmetic mods.

### Mori's Astral Elves (`7718`)
From Spelljammer. Close to RAW.
- **Astral Fire:** learn one of Dancing Lights, Light, or **Sacred Flame**.
- **Keen Senses:** proficiency in **Perception**.
- **Starlight Step:** **bonus action** teleport up to **9m** to a space you can see. Uses equal
  to your **Proficiency Bonus**, restored on long rest; charges increase at levels **5, 9, 13,
  17**.
- **Astral Trance:** implemented as the vanilla **Astral Knowledge** action rather than RAW.

Ships with `Mori's Astral Elves - Patch 7 Fix` (`13867`). The RAW +2 CHA / +1 DEX was
**removed in v1.1** — Larian moved ASI to class.

> Starlight Step is a **repeatable bonus-action teleport scaling on proficiency** — 3–6 uses per
> long rest. Strong positioning on any build, and it does not compete with a spell slot.

### Astral Half-Elves (`9676`)
A Half-Elf variant of the above, standalone from v2.00. The only mechanical difference:
**Astral Knowledge is swapped for a custom Astral Intuition** granting **advantage on all
Intelligence checks**.

### Playable Shadar-kai (`21382`)
- **Necrotic Resistance.**
- **Blessing of the Raven Queen:** bonus action teleport, **once per long rest**. From level 3,
  you also gain **resistance to ALL damage until your next turn** after using it.
- **Raven Summon:** bonus action, **once per long rest**, summons a personal raven (**Brân**)
  that **levels with you**.
- Not tagged Baldurian; gains other-plane dialogue options. The Raven Queen becomes your deity
  if you play a Cleric. Includes a reusable black/grey dye.

> **Two duo-relevant features in one race.** Resistance to *all* damage for a round is a genuine
> emergency button in a party with no third body to pick anyone up — and it stacks with Lone
> Wolf's halved damage. The raven is a free extra body on a long-rest clock.

### Spirited Seasons — Playable Fey Eladrin (`7037`)
- **Fey Step:** bonus action teleport to a space you can see. Uses equal to **Proficiency
  Bonus**, restored on long rest.
- From level **3**, Fey Step gains a season-based rider:
  - **Autumn** — Charm and teleport to an enemy
  - **Winter** — Frighten and teleport to an enemy
  - **Spring** — swap places with another creature you can see
  - **Summer** — deal fire damage and teleport to an enemy
- **Trance:** from level 3, change your season **once per long rest**.
- Includes four reusable seasonal dyes.

> Same proficiency-scaling teleport economy as Astral Elves, but the level 3 riders add **free
> CC attached to movement** — Winter's Frighten in particular is control that costs no slot and
> no concentration.

---

## Ghastly Ghouls — Playable Undead (`5895`)

Four subraces built from Libris Mortis (3.5e) and homebrew: **Lich, Ghoul, Wight, Mummy**. Each
has its own progression table and gimmick — Ghouls eat corpses, Liches are bound to
Phylacteries, Mummies move organs into Canopic jars, Wights can raise a Half-Wight. All four can
also be played as a **Skeleton**.

**Universal undead passives:**
- **Undead Resistance:** **immune to Poison**, **resistant to Necrotic**, **vulnerable to
  Radiant**.
- **Decayed Constitution:** being inflicted with a Poison status **heals you for 1d10**.
- **Illithid Disguise:** roleplay-only toggle so NPCs don't react to you being a corpse.
- **Toxic Bite** (Ghoul): inflicts **Rot** for 3 turns (1d4 poison/turn); if not healed or saved
  against with a Constitution check, escalates to **Infection** (1d6 poison/turn **plus
  vulnerability to all damage types**), which reapplies itself until cleared.

> ### ⚠ The undead tag is the biggest single build constraint in this file
>
> Your character uses the **vanilla `undead` tag**, which means **most healing spells do not
> work on you**, you are **vulnerable to Radiant**, and you **can be affected by Turn Undead**.
>
> **In a two-player Lone Wolf run this is close to disqualifying unless planned around.** Losing
> either character usually ends the fight, and the standard answer — the other character heals
> you — stops working. If a player wants an undead Tav, the run needs an alternative recovery
> plan: `Necromancy Heals Undead` (`12666`) is in the list and makes **Inflict Wounds, Harm and
> Circle of Death heal undead** instead of damaging them, which is the intended workaround.
> Confirm the other character can supply one of those before greenlighting this.

`Ghastly Ghouls Addon - Banshee Subrace` (`15707`) adds a Banshee-themed ghoul subrace with
custom VFX.

Related mods in the list: `Ghouls Custom Piercings`, `Ghouls Customization Compendium`,
`Jerinski's Masc Gith Heads - for Undead Race` (all cosmetic).

---

## Mordenkainen Presents — Lizardfolk (`22963`)

Faithful adaptation from *Monsters of the Multiverse*. **Mechanically the strongest race
addition in the list.**

- **Bite:** a fanged maw usable for unarmed strikes, dealing **1d6 + Strength modifier**
  slashing.
- **Hungry Jaws:** **bonus action** special Bite attack; on hit, deals normal damage **and
  grants temporary HP equal to your Proficiency Bonus**.
- **Natural Armor:** while **not wearing armour**, base AC is **13 + Dexterity modifier**.
- **Hold Breath:** always active; **immune to Stinking Cloud and certain poison gasses**.
- **Nature's Intuition:** proficiency in **two** of Animal Handling, Medicine, Nature,
  Perception, Stealth, Survival.

Uses Dragonborn jaw/chin assets; extensive customisation.

> Three separate things a build normally pays for: an **unarmed attack that scales on STR**, a
> **bonus-action attack with self-sustaining temp HP**, and **unarmored AC** that competes with
> Barbarian/Monk without needing either class. Note **Tavern Brawler is heavily nerfed** here
> (`data/listo-10.2-feats.md`), so the classic unarmed payoff is smaller than it looks — but
> Hungry Jaws' temp HP is on a **per-turn bonus action**, which is exactly the kind of repeatable
> durability a two-person party wants. Two skill proficiencies also feed the duo's
> "two characters must cover every check" premise.

---

## Vanilla race changes

- **Sunlight Sensitivity - DND 5E** (`20274`) restores **Sunlight Sensitivity to Drow and
  Duergar** — disadvantage on attack rolls and Perception in sunlight. **Avoid both races**
  unless the player specifically wants the drawback.
- **Dragonborn - Stronger Breath Weapon** (`3235`) — breath weapon gains dice faster than every
  5 levels; die configurable between d4/d6/d8/d10/d12. See `data/listo-10.2-feats.md`.
- **Half-Tiefs** (`2538`) and **Half-Tiefs - Flora and Fauna** (`8871`) add tiefling horns and
  tails to all races — **cosmetic only**.
- A large number of head, hair, eye, skintone and scale mods ship in the list. All cosmetic;
  none are listed here.

---

## Removed — do not recommend

**v9.0.3 purged nearly all race mods**, including **Fantastical Multiverse**. **Remixed
Subraces** went in v8; **Satyr** in v7.1.0.

This is the same purge that removed a large batch of subclasses, so intuition about what "should"
be available is unreliable in both directions. **Confirm any race against
`data/listo-10.2-mods.tsv` before recommending it** — and remember the TSV is Nexus-only, so
check the manifest's `"Url"` fields for mod.io content before declaring something absent.
