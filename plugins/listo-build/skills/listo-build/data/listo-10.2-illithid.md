# Listonomicon 10.2 — illithid powers (IPO2)

**Illithid Powers Overhaul 2 is live for this run.** It ships in the list flagged `OPTIONAL_` and
is enabled in the MO2 profile; Listo's own docs call it "officially optional due to its
significant strength". Everything below is read from the installed paks, not from the mod pages.

Vanilla illithid knowledge is wrong here in every load-bearing way: powers cost a **resource**,
their numbers **scale with how many you own**, owning them **makes you more fragile**, and the
astral tadpole grants **none of the six powers the wiki lists**.

## What is installed, and what wins

Load order from `profiles/Listonomicon/modsettings.lsx` — later entries override earlier ones:

| # | Mod | What it contributes |
|---|---|---|
| 314 | `IllithidPowersOverhaul` (Nexus 5105) | the whole overhaul — tree, costs, scaling, the `SiaelIPORes` resource |
| 315 | `IllithidPowersOverhaulHalfPotency` | **overrides every resource grant** — halves the charges each power carries |
| 721 | `Illithid Powers_consolidated` (Nexus 16671) | UI only: folds every power into one hotbar container. Changes no cost and no number |
| 178 | `Illithid Emporium` (Nexus 14860) | gear that **reads** power count. Adds no tadpoles |
| — | `Stomp that Tadpole` (17485) | dialogue edit at the Emperor reveal — lets the astral tadpole be refused |
| — | `Tadpole Dialogue Without Resting` (2162) | removes the rest gate on tadpole dialogue. No mechanical change |

**Half Potency is the live balance**, so every charge number in this file is the halved one. The
un-patched IPO2 numbers on the Nexus page are double these and do not apply.

## The economy

**`SiaelIPORes` — illithid charges.** A new action resource, `ReplenishType Rest` (long).

| | |
|---|---|
| **Pool** | `2.5 + 0.5 × powers mastered` — Illithid Persuasion carries 2.5, every power after it 0.5 |
| **Refill** | long rest full; **short rest 50%**; Potion of Greater Restoration 100%, Lesser 50% |
| **Spent by** | every active power, on top of its action cost — 1 to 5 charges, 7 for Ceremorphosis |

So the pool at 5 / 10 / 15 / 20 / 25 powers is **5 / 7.5 / 10 / 12.5 / 15** charges per long rest.
At an average 2 charges a cast that is roughly **2–7 casts per long rest**, or 3–10 with both
short rests taken. Illithid powers are a **long-rest resource that competes with the Action**, not
a free rider on the turn.

**Illithid Mind Rank (IMR) — `⌊powers ÷ 5⌋`, capped at 5.** Nearly every power's numbers scale off
IMR rather than character level, so power count *is* the scaling stat. Rank updates on long rest.

**The tax: `+IMR` bonus physical damage taken, per hit.** `Siael_IllithidMind_1…5` add flat 1–5
Bludgeoning / Piercing / Slashing on every incoming physical hit. It is applied before Lone Wolf's
halving like any other damage, and it is **unconditional** — there is no way to own 25 powers and
not take +5 per physical hit. This is the whole cost of the system and it lands on **Durability**.

**Respec.** `SIAEL_Purifying_Tadpole` (Rare, 100 gp) resets the tree and refunds the tadpoles. One
seeds the tutorial-chest table, so it is available from Act I.

## Supply — finite, party-wide, and back-loaded

One tadpole buys one power **for one character**. **Nothing in the list adds any** — and because
most tadpoles are looted off True Souls, the encounter mods were checked too, not just the illithid
ones. Every installed pak was scanned: **810 paks / 578,672 entries**, of which 440
`TreasureTable` / `Equipment` / `Character` / `Object` stat files and 10,461 scripts, goals and
templates were read. The only tadpole item any mod creates is the Purifying Tadpole above, and the
only mod-added creatures with "Tadpole" in their name are vanilla **tadpoled skeletons**, which
carry nothing lootable. The enabled encounter mods — Encounters Overhaul (+5e Spells, Less XP),
Encounters Enhanced, Dynamic Enemy Encounters, Valkrana's Undead Encounters — add fights, not True
Souls with specimens.

Two live-install caveats fell out of that scan:

- **`OPTIONAL_The Debug Book` ships disabled** (`-` in the profile). It can set tadpole count
  directly and hand out the astral tadpole. If it is ever switched on, supply stops being a
  constraint and every number in this file stops binding.
- **`Topple the Weave` is enabled, and it can delete an illithid build.** Its Unstable Weave surge
  arms itself **only once Volo is dead**; after that, every character that casts a spell gains
  `TTW_WildMagic_UnstableWeave`, roughly one cast in five surges, and 4 of the 121 surge outcomes
  call `Osi.RemoveAllTadpolePowers(caster)` — about **0.7% per spell cast**, compounding across a
  run. Whether the tadpoles are refunded is *(unverified)*. **A build committed to illithid powers
  should keep Volo alive**; a spell-heavy one has the most exposure.

| Act | True Souls | Loot / quest | Total |
|---|---|---|---|
| **I** | 6 — Dror Ragzlin, Edowin, Flind, Gut, Minthara, Nere | 6 — Enclave Library ×1, Crèche infirmary ×3, Raid the Emerald Grove, siding with Nere | **≈12** |
| **II** | 7 — Krizt, Linsella, Malik, Marcus, Merim, Z'rell, Isobel if abducted | 5 — Zhentarim crate ×2, brine pool ×1, Capture Isobel, Ketheric's Relic via Balthazar | **≈12** |
| **III** | 8 — Avery Sonshal, Churg Elvek, Darbonna, Dravo Flymm, Edenosa, Mibbs, windmill mind flayer, Sally Flymm | 18 — Rivington/Wyrm's ×4, Lower City ×7, **Cargo Shipment ×6** near the Steel Watch Foundry, Feed the Mind Flayer | **≈26** |

> **(unverified — bg3.wiki, not pak-confirmed.)** Vanilla placement lives in base-game level files,
> which are not under the mods root, so `lspk.py` cannot check these. Treat the totals as
> approximate and the *shape* as the finding: **half the run's supply lands in Act III**, and
> several Act I/II tadpoles are locked behind mutually exclusive choices (siding with the Absolute,
> siding with Nere, siding with Balthazar, abducting Isobel).

Planning consequence: **the party is tadpole-poor exactly when the powers would matter most.**
Through Act I a duo can fund about 12 powers *between them*; through Act II about 24. Both bodies
at IMR 5 needs 50 and the run does not hold that many.

## The astral gate

Ten of the twenty-five powers carry `NeedsHalfIllithidToUnlock="true"` in `TadpolePowersTree.lsx`.
Half-illithid comes only from the **Astral-Touched Tadpole**, given by the Emperor at the **start of
Act III**. So:

- **IMR is capped at 3 before Act III** — only 15 powers exist to buy, whatever the tadpole count.
- The whole inner ring — Mind Blast, Black Hole, Psionic Dominance, Astral Stillness, Fly, both
  Psykinetic spells, Fracture Psyche, Elevated Mind, Psionic Backlash — is **Act III content**.
- **IPO2 grants none of the six powers the vanilla item grants.** It intercepts
  `TAD_PARTIAL_CEREMORPH` and suppresses them, substituting **Grand Design / Ceremorphosis**.
- **Commune, don't eat.** Eating consumes the item for one character; communing leaves it usable by
  the other, so **both bodies can become half-illithid from the one tadpole**. Eating it is a
  planning error in a duo. *(unverified — vanilla behaviour, bg3.wiki.)*
- **Destroying it** is only offered if nobody has consumed a tadpole at all; `Stomp that Tadpole`
  is the mod that keeps that option live at the reveal.

## The tree

Ring 1 needs only Illithid Persuasion. Ring 2 needs one ring-1 power. Ring 3 needs half-illithid.
Prerequisites inside a ring are loose — every ring-2 node lists a ring-1 *or* a ring-3 parent — so
in practice **any power is one tadpole once its ring is open**.

Costs are `action + charges`. IMR scaling is quoted at rank 0 → rank 5.

### Free with the first tadpole

| Power | Cost | What it does |
|---|---|---|
| **Illithid Persuasion** | — | dialogue option; carries the 2.5-charge pool and the Illithid Mind tax |

### Ring 1 — available from Act I

| Power | Cost | What it does | Axis |
|---|---|---|---|
| **Psionic Overload** | toggle, 1 charge | rider on *everything* offensive, 1d2 → 1d12 by IMR; damages you each turn in combat | single-target |
| **Peace Breaker** (Favourable Beginnings) | passive | **+IMR+1 to the first attack roll and the first Persuasion / Deception / Intimidation check** — +1 at rank 0, +6 at rank 5. Consumed by whichever comes first: the boost is conditioned on `not HasStatus('TAD_PEACE_BREAKER')`, and making an attack or a check applies it. (Rank 5 gives Intimidation only +5 — a typo in the pak, not a rule) | skills |
| **Force Tunnel** | **bonus action** + 6 m movement, 1 charge | dash through a line, pushback 2 m + IMR. No cooldown. Free bonus action with Awakened | control-area |
| **Concentrated Blast** | action, 3 | 1d6 per IMR+1 (1d6 → 6d6), no cooldown | single-target |
| **Transfuse Health** (Life Punction) | action, 1 | steal 20% of an **ally's** remaining HP to heal yourself; +1 target per IMR | durability |

### Ring 2 — available from Act I, one ring-1 power deep

| Power | Cost | What it does | Axis |
|---|---|---|---|
| **Stage Fright** | action, 2 | 1d6 per IMR (half a d6 at rank 0), no cooldown | single-target |
| **Ability Drain** | action | drain an ability score and **gain it yourself**; value capped by IMR; ends with combat | control-single |
| **Luck of the Far Realms** | interrupt, 2 | crit threshold improved by ⌊IMR/2⌋+1 while unused; −2 after firing | single-target |
| **Eldritch Ward** | interrupt, 1 + spell level | **Shield-like**: ±(proficiency + IMR) on the triggering attack or save, plus flat `IMR` damage reduction against AoE, ranged and spells | durability / saves |
| **Displace** | passive | procs when an enemy is pushed, pulled, thrown or teleported — 1d2 → 1d12 | aoe |
| **Repulsor** | action, 2 | push out to 8 m, 1d3 → 5d6, enemies only, no cooldown | control-area |
| **Cull the Weak** | 1–2 charges, once per turn | spreads overkill damage; radius +1 m per IMR; **executes enemies under 2×IMR HP** | aoe |
| **Psychic Fortress** | passive | **Psychic resistance + IMR to Intelligence, Wisdom and Charisma saves** | saves |
| **Shield of Thralls** | action, 2 | shield that explodes for IMR+1 Force, again on a failed **Constitution** save | rescue |
| **Mind Flayer** | toggle | illithid damage applies **Insanity** stacks scaling with the fraction of max HP dealt; stacks improve the crowd-control chance | control-area |

### Ring 3 — inner circle, half-illithid only, Act III

| Power | Cost | What it does | Axis |
|---|---|---|---|
| **Mind Blast** | action, 4, once per turn | 1d8 per IMR+2 (3d8 → 7d8) + spellcasting modifier, cone, **half damage and no stun on a save** | aoe |
| **Black Hole** | action, 5, once per combat | pull, 1d10 per IMR (1d5 → 5d10), Prone on a failed save, Dazed 2 turns regardless | control-area |
| **Psionic Dominance** | action, 4 | **Dominate Person** | control-single |
| **Fracture Psyche** (Imperil) | action, 2 (recast 4) | vulnerability, lasting 1 turn per IMR | single-target |
| **Psionic Backlash** | **reaction**, 2 | counterspell up to level IMR+1, scaling die. No once-per-rest limit any more | control-single |
| **Elevated Mind** (Illithid Expertise) | action, 2 | pick an ability: **Expertise + proficiency in every skill keyed to it**, permanent, recastable to switch | skills |
| **Psykinetic Toss** | action, 3 | telekinesis on creatures only, 1d4 per IMR to the thrown target, gravitational pull at impact | control-single |
| **Psykinetic Pull** | action, 2 (+1 to throw) | pull creatures | control-area |
| **Fly** (Levitate) | action | flight, 4 m per IMR (2 m → 20 m) | actions |
| **Astral Stillness** | passive | **every power costs 1 charge less**; builds stacks equal to each power's printed cost, and every `10 − IMR` stacks the next power is free | actions |

### Granted by the astral tadpole itself

| Power | Cost | What it does |
|---|---|---|
| **Grand Design — Ceremorphosis** | action, **7** | full mind flayer form: +20 max HP, Tentacle Whip replacing unarmed, Extract Brain, a 7d6 Psychic Concentrated Blast that heals you for the damage, and an upgraded Astral Stillness that zeroes most charge costs |

## Interactions that change a build

**Save DC comes from the *last class added*.** Illithid power DCs use the spellcasting ability
modifier of the most recently taken class — taking a level-1 dip switches every illithid DC to that
class's ability. A Wisdom build that dips Fighter last has illithid DCs off nothing. This collides
directly with §3a's multiclass-by-default doctrine and with §4a's respec ladder: **the dip order on
the ladder decides the illithid DC.** Arcane Acuity and Arcane Enchantment do apply.
*(unverified — vanilla rule, bg3.wiki; IPO2 does not appear to change it.)*

**Illithid Emporium gear reads power count.** The Cerebral Citadel armour grants **+1 AC per 5
powers mastered, to +5** (`SIAEL_EMPEROR_AC_1…5`, applied by the mod's Lua at the same 5/10/15/20/25
thresholds as IMR). The rest of the set is ordinary gear: Alien Legacy ring ignores Psychic and Force
resistance, the Paranoia set gives up to +3 spell save DC at close range, the Emperor weapons add
proficiency-bonus damage on Psychic and Force. It arrives through a vendor, not a tadpole.

**Awakened** (the Crèche infirmary passive) makes Force Tunnel free and lets a power be cast with an
Action when the bonus action is gone. **Survival Instinct** (Omeluum) is a toggleable passive here.

**Concentration.** Illithid powers do not take concentration, which is why they read strongly on
Control for a duo holding only two concentration slots — but they take the **Action**, so they
compete with the attack routine rather than with the control spell.

**Chassis differ in what they get out of the same tadpoles**, and that difference — not the size of
the share — is what a score should move for. The two-way table is in `listo-ledger` SKILL.md; the
short version is that a body converts powers well when its Action is cheap, its last-added class
has a real casting stat (that is where power DCs come from), its reactions are idle, and its armour
shrugs off the `+IMR` tax. The passive powers — Psionic Overload, Cull the Weak, Luck of the Far
Realms — are the exception that suits a multiattack martial, because they cost no Action and ride
every attack.

## What vanilla and mod-page knowledge gets wrong here

- **Powers are not free.** Every active one costs charges from a long-rest pool.
- **The astral tadpole grants no powers.** It grants Ceremorphosis and opens the inner ring.
- **Fly is inner-ring** — it cannot be had before Act III.
- **More powers is not strictly better.** The Illithid Mind tax is unconditional.
- **The Nexus page's charge numbers are double the live ones** — the Half Potency patch overrides them.
- **Illithid Powers Consolidated changes nothing mechanical**; it is a hotbar container.
