# Listonomicon 10.2 — gates

**A gate is a one-time, missable acquisition that permanently changes what a body can do.**
Hitting one is worth more than most level-ups, and every one of them is lost for the run if the
act moves on without it.

This file is the single definition of the gate list. `axis-rubrics.md` §8 scores the Skills axis
against it; `listo-rules.md` lists the subset that raises an ability score. Neither restates the
gates — if a gate's act, cost or reward is wrong anywhere, it is wrong **here** and fixed here.

**Gates are not a Skills-axis topic.** Only five of them are paid in skill checks. The rest are
paid in gold, saving throws, or a quest decision — and what they buy lands on Saves, Durability,
Actions and Endurance far more often than on Skills. Skills is the axis that *buys* gates; it is
not the axis most of them *feed*.

---

## How a skill gate is actually cleared here

Three modlist mechanics change the arithmetic before any DC is rolled. Confirm all three before
scoring a gate as cleared or missed.

### The party's best modifier is used, and the host rolls it

**`Use Highest Modifier in dialogue`** (`Mods/uhm/ScriptExtender/Lua/Server/USM.lua`) hooks
`DialogStarted`, reads every party member's total for all eighteen skills through
`HasSkill(CHARACTER, STRING, out INTEGER)`, and boosts the roller up to the party maximum with a
`Skill(X, 1)` status stacked by `MultiplyEffectsByDuration`.

**`Use Best Sleight of Hand`** (`Mods/BestLockpicking/…/BestLockpicking.lua`) does the same on
`RequestCanLockpick`, `RequestCanDisarmTrap` and `RequestPickpocket`.

Three consequences, all load-bearing:

- **`HasSkill` is a per-character query.** The maximum is taken over each body's *finished* total.
  The ability modifier and the proficiency still have to sit on the **same body** — you cannot
  pair one PC's Charisma with the other's Persuasion proficiency.
- **The buff always lands on `Osi.GetHostCharacter()`.** In two-player co-op the non-host gets
  nothing. **Route every gate check through the host.**
- **It is a flat number, not a grant of proficiency.** Anything keyed on *being proficient* does
  not transfer — most importantly **Reliable Talent** (Rogue 11) and **Silver Tongue**
  (Eloquence Bard 3), which stay properties of the body that owns them.

> **This is why Skills stays complementary rather than personal, but the reason has changed.**
> It is no longer "two bodies cover more gates than one" — it is that one body's coverage is
> readable by the host, so a pair scores nearer its *better* half than its average. The `comp`
> operator (`hi + lo//2`) may now understate that. Left alone pending calibration; see
> `scoring-model.md` §11.

### The inspiration bank is vanilla

**No `Inspiration Uncapped` in the profile.** Four charges, each a full reroll. The
reroll table in `data/listo-10.2-backgrounds.md` applies unchanged — a 45% roll becomes 83% on
two rerolls, which is what turns most of these DCs from a gamble into a plan.

### Pickpocket and lockpick DCs are vanilla

**Neither `Improved Pickpocketing` nor `Configurable Pickpocketing` is in the profile**, despite
both appearing in other mods' compatibility notes. `Auto Lockpicking` is installed and automates
the rolls; it does not change them.

**The Mod Organizer profile is the whole load order.** The game's own `Mods/` folder is empty, so
nothing loads outside it — checked directly, not inferred. Earlier it held loose paks including
`improved_pickpocketing` and `inspirationsuncapped`, which would have changed both the pickpocket
DCs and the inspiration bank; they have been removed and were never part of Listo.

---

## Act I

| Gate | Cost | Buys | Axis |
|---|---|---|---|
| **Auntie Ethel's Hair** | **Deception or Intimidation, DC 20** — Fighters and Barbarians instead get **Intimidation DC 15 with advantage** | **+1 to a chosen ability**, above 20 | any |
| **Awakened** (Zaith'isk, Crèche Y'llek) | **three saving throws**; each failure is a permanent **−2 to INT, WIS, CON** respectively | **Force Tunnel becomes free**, and a power can be cast **with an Action once the bonus action is gone** | **Actions** |
| **Survival Instinct** | complete *Help Omeluum investigate the parasite* in the Underdark | a unique illithid power outside the tree — infuse a creature with psionic force, healing it at 0 HP. Toggleable under IPO2 | Rescue |
| **Forbidden Knowledge** (*Necromancy of Thay*) | none — turn all three pages; **no save has to be passed** | **+1 Wisdom saving throws and +1 ability checks**, plus Speak with Dead 1/long rest | Saves, Skills |
| **Silvanus' Blessing** | Emerald Grove | **proficiency in Nature and Animal Handling** | Skills |
| **Loviatar's Love** | submit to Abdirak and perform well | **+2 attack rolls and Wisdom saves at ≤30% HP** | Tempo, Saves |
| **BOOOAL's Benediction** | a **Persuasion** check, or sacrifice a companion | advantage on attacks against Bleeding targets | Tempo |
| **Instrument proficiency** | **Performance** check, helping Alfira | instrument proficiency (Bards already have it) | Skills |
| **Volo's Ersatz Eye** | tell Volo about the tadpole, accept the surgery | permanent **See Invisibility** | Utility |
| **Paid the Price** | accept Ethel's deal at the teahouse | **+1 Intimidation, disadvantage on Perception**, disadvantage attacking hags | Skills — mixed |
| **Free Us** (prologue) | **Investigation 10 → Medicine 10 (advantage)**, or raw **Strength 10**, or raw **Dexterity 10** | nothing yet — see below | — |

### Notes

**Hag's Hair is Deception or Intimidation. Persuasion is not an option.** The DC 20 check buys the
hair *and* Mayrina; simply taking the deal gives the hair and costs Mayrina. **Failing one check
makes the other unavailable**, so there is exactly one attempt. `Auntie Ethel Always Surrenders`
is installed and guarantees she surrenders rather than dying first, which removes the usual way
this gate is lost. **Stern Gaze** (Inquisitor) lets Intimidation run off Wisdom — the only
non-Charisma route in the list, and worth more now that Intimidation is one of only two.

**Awakened is the largest Actions gate in the run** and it is paid in saving throws, not skills.
Failing costs permanent ability score. The saves are easier with the player character in the
device rather than Lae'zel. `Sword of the Emperor Enhanced` gives Raulothim's Psychic Lance extra
behaviour for a body that has Awakened or Partial Ceremorphosis.

> **Vanilla says Awakened makes every illithid power a bonus action. Under IPO2 it does not.**
> Powers cost an **Action** here and therefore compete with the attack routine, so what Awakened
> actually buys is the escape from that competition — read the effect off
> `data/listo-10.2-illithid.md`, which is compiled from the installed paks. That file wins over
> any vanilla description of an illithid feature, including this one.

**Forbidden Knowledge is free.** No check is required — the saving throws associated with turning
the pages can all be failed. A flat +1 to every ability check for nothing is the cheapest Skills
rung in the run. It has one cost: **spending it is the no-check route past the Mirror of Loss**
(Act III), so a body cannot keep both.

**Free Us in the prologue, then do not cripple it.** All four routes are DC 10 and two need no
skill at all. Freeing it is the only irrecoverable step — Us must survive the prologue to appear
in Act II. The follow-up "mutilate the brain" option is a **trap**: it is a Dexterity DC 15, and
**failing turns Us and every other Intellect Devourer hostile**, while *passing* applies the
permanent **Lobotomised** condition — Intelligence 12 → 8 and movement 9m → 6m, which the Act II
summon keeps. Take *Spare the creature*. Payoff is in Act II, below.

---

## Act II

| Gate | Cost | Buys | Axis |
|---|---|---|---|
| **Potion of Everlasting Vigour** | **pickpocket Araj Oblodra** at Moonrise, or loot her corpse | **+2 to a chosen ability**, above 20 | any |
| **Summon Us** | free Us from the Morgue cage in the Mind Flayer Colony (requires the prologue step) | a **55 HP ally, once per short rest**, resistant to physical and Necrotic | **Actions** |
| **Githzerai Mind Barrier** | Waking Mind into the Mind-Archive Interface, then purge or consume the mind | **advantage on Intelligence saving throws** | Saves |
| **Improved Bardic Inspiration** | speak to Alfira at Moonrise as a **Bard** | one extra **1d12** Bardic Inspiration per long rest | Rescue |
| **Arabella's Shadow Entangle** | tell Arabella her parents' fate | entangle an Undead or Shadow creature | Control |

### Notes

**Act II is no longer the empty band.** `axis-rubrics.md` used to record "no unique named gate"
here. Two installed mods change that:

- **`Stealable Potion of Everlasting Vigour`** puts the potion in Araj Oblodra's inventory, so it
  no longer requires Astarion — who is not in the party under Lone Wolf. Pickpocket or corpse.
- **`Better Potion of Everlasting Vigour`** makes it **+2 to a chosen ability** instead of fixed
  Strength (`Story/RawFiles/Goals/BetterPotionOfEverlastingVigour.txt`, via
  `MOO_POTION_BLOODOPTION_ASTARION`).

Together that is a **Mirror-of-Loss-grade reward landing in Act II**, and the only route to it in
a two-Tav run is Sleight of Hand or violence.

**Summon Us is an Actions gate priced in short rests.** Once per short rest, not per long — which
matters given Short Rest Full Heal is off and the party leans on short rests anyway.

---

## Act III

| Gate | Cost | Buys | Axis |
|---|---|---|---|
| **Anointed in Splendour** | **gold** at the Stormshore Tabernacle, scaling with level and difficulty; **per character** | **+2 to all saving throws** | **Saves** |
| **The Tharchiate Codex: Blessing** | Ramazith's Tower vault puzzle — **first reader only** | 20 temp HP per long rest, **and 50% damage reduction from all sources while holding any temporary HP** | **Durability** |
| **Mirror of Loss** | **Religion DC 25**, *or* sacrifice knowledge of the *Necromancy of Thay* for a guaranteed result with no check | **+2 to a chosen ability** (raises to 24), optionally **+1 Charisma** | any |
| **Sweet Stone Features** | **5000 gold** to Boney at the Circus — **one statue for the whole party** | **+1d4 to attack rolls and saving throws** | Saves, Tempo |
| **Phalar Aluve +3** | **Sleight of Hand**, pickpocket-only, in the Circus — needs the Act II music box first | the sword upgraded to Legendary | Tempo |
| **Danse Macabre** | *Tharchiate Codex*, then the last page of *Necromancy of Thay*, **DC 20 Wisdom save** | 4 ghouls; −5 Constitution, removable with Remove Curse | Actions |
| **Partial Ceremorphosis** | **commune** with the Astral-Touched Tadpole from the Emperor — do *not* eat it | **Grand Design / Ceremorphosis**, and unlocks the ten inner-ring powers, which still cost charges | Actions |
| **Slayer Knowledge** | rescue Volo at the Steel Watch Foundry, read the guidebook | advantage against Slayer abilities | Saves |
| **Unstable Blood** | give Araj blood in Act II, help her again in Act III | flammable blood | Tempo |

### Notes

**The Tharchiate blessing is the largest Durability gate in the run**, and only because of an
installed mod. `Tharchiate Ascendency` adds the hidden passive `Siael_CursedTome_Thresh`, which
fires on `OnCreate;OnDamaged;OnStatusApplied;OnStatusRemoved;OnTurn` and applies
`SIAEL_CURSEDTOME` under `IF(HasTemporaryHP())` — and that status carries
`Boosts "DamageReduction(All,Half)"`.

The vanilla passive gives 20 temp HP on long rest and is spent, but the condition is *any*
temporary HP from *any* source. **Inspiring Leader refreshes temp HP every short rest**, so this
is maintainable rather than once-per-rest. **Only the first character to read the Codex gets it**
— one of the two bodies, never both.

> `(unverified)` Whether a second `DamageReduction(All,Half)` composes multiplicatively with Lone
> Wolf's own 50% is not confirmed from data. The mod author claims multiplicative stacking with
> *resistance*, which is not the same claim. Do not score a body at 75% total reduction until this
> is tested in game.

**The astral tadpole is the one gate a duo can hit twice.** Eating it consumes the item for one
body; **communing leaves it usable by the other**, so both can become half-illithid from the single
tadpole. Eating it is a planning error here. IPO2 also **suppresses the six powers the vanilla item
grants** — it intercepts `TAD_PARTIAL_CEREMORPH` and substitutes Ceremorphosis — so there is **no
tier-1 refund and no free Fly**; Fly is an inner-ring power that still has to be bought. `Stomp
that Tadpole` keeps the refuse option available at the reveal even after eating tadpoles, behind a
DC 14 Constitution check. Full tree, charge costs and the `NeedsHalfIllithidToUnlock` list are in
`data/listo-10.2-illithid.md`.

**Mirror of Loss is DC 25 Religion, not 20.** `data/listo-10.2-backgrounds.md` carried `~20
(verify)`; the check is 25. Three things follow: it is a genuinely hard gate even at Act III
proficiency; **there is a no-check route** — sacrificing knowledge of the *Necromancy of Thay*
gives a guaranteed +2, at the cost of Forbidden Knowledge from Act I; and the buff **raises a
score to 24**, not merely above 20.

**The Mirror is per character, and it is not scored.** bg3.wiki: *"Each character, including
hirelings, may obtain bonuses from the mirror independently"* — one attempt each, and the +2 lands
on whoever rolled, so a single strong Religion body clears it for itself alone. That would make it
the only personal check in the run. It is nonetheless **excluded from the Skills axis**, because
it is trivially bought: the same source documents respeccing at Withers into **Rogue 11 / Knowledge
Cleric 1** for Religion Expertise and Guidance, passing, then respeccing back *"retaining the
Mirror of Loss stat enhancement"*. Withers is recruitable from the Dank Crypt and charges 100 gold.
A check any chassis can rent its way past measures the wallet, not the chassis.

**The same test disqualifies less than it first appears.** Hag's Hair is not rentable — the
dialogue fires on Ethel's surrender at the end of her fight, so a rented build has to win that
fight. What weakens the named gates instead is that **each has a no-check route to the same
ability point**: taking Ethel's deal yields the hair and costs Mayrina, and Araj can be killed and
looted. Passing buys the secondary prize — Mayrina alive, Araj alive for *Unstable Blood* — not
the +1 or +2. The durable half of the axis is the untelegraphed one: **traps and hidden caches
(Perception 15–25), secret doors and switches (Investigation 15–20), and routine town dialogue at
the act's own DC band**, none of which can be prepared for and none of which announce themselves.

**Anointed in Splendour is per character and Sweet Stone Features is not.** Both bodies can be
anointed; only one can be the statue. +2 to all saves for gold is the cheapest Saves rung in the
run and should be assumed for both bodies unless the run is broke.

---

## Gates that are not available to this run

Record these so nobody scores them.

| Gate | Why not |
|---|---|
| **Dryad's Blessing / Love Protects** (Zethino's love test, Act III Circus) | `Zethino Love Test Buff Fix` is installed and repairs the broken vanilla script, but its goal requires `DB_CompanionCanPartner` and a romance flag. **Two Tavs cannot satisfy it.** |
| **Consumed Shadow Weave** | Gale as an origin only. |
| **Vampire Ascendant**, **Vampire** | Astarion only, or a romanced Astarion. |
| **Slayer Form**, **Father's Gift** (Power Word Kill) | Dark Urge origin only. `Father's Gift Improved` is installed and converts the one-time Power Word Kill to a long-rest recharge — relevant **only** on a Dark Urge run. |
| **Improved Bardic Inspiration** | requires a Bard in the pair. Listed in Act II above; excluded otherwise. |

---

## Modded changes to gates, in one place

Every entry below is confirmed by reading the installed pak, not the mod page.

| Mod | What it changes |
|---|---|
| `Use Highest Modifier in dialogue` | dialogue checks roll at the party-best skill total, applied to the **host** |
| `Use Best Sleight of Hand` | lockpick, disarm trap and pickpocket do the same |
| `Stealable Potion of Everlasting Vigour` | potion added to Araj Oblodra's inventory |
| `Better Potion of Everlasting Vigour` | potion grants **+2 to a chosen ability** rather than Strength |
| `Auntie Ethel Always Surrenders` | Ethel always surrenders before dying, so the Hag's Hair dialogue cannot be skipped by overkill |
| `Tharchiate Ascendency` | Codex blessing adds **50% damage reduction while holding temporary HP** |
| `Permanent Passives` | **Loviatar's Love, Githzerai Mind Barrier and Sweet Stone Features are no longer lost on death**; Volo's Ersatz Eye becomes a toggle. The rest of its changes are cosmetic. |
| `Eye Deal` | Volo's Ersatz Eye and Paid the Price can coexist on one body — vanilla makes them exclusive |
| `Zethino Love Test Buff Fix` | repairs the vanilla script; unreachable here, see above |
| `Auto Lockpicking` | automates lockpick rolls; does not change DCs |
| `Phalar Aluve - Legendary` (`2987`) | adds the two-music-box upgrade path that creates the Act III pickpocket gate |
| `Illithid Powers Overhaul 2` + `Half Potency` | rewrites what Awakened and the astral tadpole deliver — see `data/listo-10.2-illithid.md`, which owns every illithid number |
| `Stomp that Tadpole` | keeps *refuse the astral tadpole* available after eating tadpoles, behind a **DC 14 Constitution check** |

**The three "no longer lost on death" fixes matter more than they look.** At this difficulty a
body goes down regularly, and in vanilla those three conditions evaporate the first time it
happens. Score them as held for the rest of the run.

---

## Provenance

- **Read from installed paks** with `scripts/lspk.py`: every mod behaviour above, the
  `Siael_CursedTome_Thresh` damage reduction, the two "use best modifier" scripts, the Better
  Potion Osiris goal, the Permanent Passives stat overrides, the Zethino goal conditions.
- **bg3.wiki**: the vanilla gate list, DCs and rewards. **Base-game paks are not under the Mod
  Organizer root**, so vanilla numbers cannot be confirmed the same way — treat every vanilla DC
  here as wiki-sourced. **The illithid gates are the exception**: vanilla descriptions of Awakened,
  the astral tadpole and Survival Instinct are wrong under IPO2, so those rows follow
  `data/listo-10.2-illithid.md`, which is compiled from the paks.
- **The Mod Organizer profile is the complete load order.** `profiles/Listonomicon/modlist.txt`
  holds 747 enabled mods, and the game's own `Mods/` folder is empty — so nothing loads outside it.
- **Listo's own docs**: the Phalar Aluve music-box upgrade path, from
  `data/docs/4-SpellsFeatsClassesItems.md`.
