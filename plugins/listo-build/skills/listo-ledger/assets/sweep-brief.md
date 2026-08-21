# Sweep brief — one seed per subclass

Paste this into every sweep agent's prompt, followed by that agent's assignment. It is
self-contained **by design**: the reference files it compresses total ~32k tokens, and an agent
that opens them instead costs more than the whole sweep is worth.

**Everything below is deliberately duplicated** from `axis-rubrics.md`, `scoring-model.md`,
`listo-rules.md` and `listo-build` SKILL.md. That is the one place in this skill where restating
another file is correct, because a sweep agent cannot afford to read them. Do not "fix" it by
replacing these sections with pointers — the pointers cost more than the text. Do re-check it
against those files when they change; `seed_deps` in `seed_index.py` hashes this file precisely so
that an edit here re-seeds what it invalidates.

## Your job

For each subclass you are assigned, emit **one seed record** carrying one or more **builds**. A
build is one line of judgement, not a score — the ledger re-scores every promoted chassis from
scratch later, so do not attempt ten axes here.

**Read only the line ranges named in your assignment** — which include your own classes' sections
*and* every class's `## Dip value` section, the shared set below. Do not open
`listo-build/SKILL.md`, `axis-rubrics.md`, `listo-rules.md`, other parts of other class files, the
manifest, or any `.pak`. Everything else you need is below. If a subclass's entry is genuinely unreadable without more, emit the seed with
`"verdict": "none"` and say so in `why` — do not go hunting.

## Output contract

Return **raw JSON only** — no prose, no fences, no commentary. One object, keyed exactly as your
assignment lists the keys (they are `<class file>/<### heading verbatim>`; copy, never retype).

```json
{"warlock/The Hexblade": {"verdict":"candidate","builds":{
  "front-line": {"chassis":"Hexplate","split":"Warlock 12 (The Hexblade) / Paladin 8 (Oath of Devotion)",
                 "peak":4,"peak_axis":"st","breadth":5,"why":"Cha to attack and damage, short-rest slots feeding smites, aura at Paladin 6."},
  "short-rest": {"chassis":"Curse","split":"Warlock 12 (The Hexblade) / Sorcerer 8 (Draconic Bloodline)",
                 "peak":4,"peak_axis":"ctrl_s","breadth":4,"why":"Same stat, different clock: Chains of Carceri and Quickened blast off pact slots."}}}}
```

| verdict | when | required |
|---|---|---|
| `candidate` | has at least one viable 20-level expression | `builds` |
| `dupe` | its best expression **is** another assigned subclass's body | `dupe_of` `why` |
| `none` | no 20-level split rescues it | `why` |
| `not-a-subclass` | the heading is a table or a note | `why` |

Every build needs `chassis` `split` `niche` (as its key) `peak` `peak_axis` `breadth` `why`.
`why` is **one sentence, 25 words maximum**. Rejections need it more than candidates do.

**Emit no other fields.** `src`, `seed_deps` and `score_deps` are cache stamps written by
`seed_index.py --stamp` after your output is merged; a stamp you invent would mark a judgement as
verified against source you never read.

## The seven niches

**`niche` is a closed set.** It is the key each build sits under, and it must be one of exactly
these seven strings. Anything else is rejected on load, so copy them character for character.

| niche | what a body in it does with its turns | the catch |
|---|---|---|
| `action-economy` | Manufactures turns — summons, Haste, Action Surge, Quickened, or an Action handed to the partner | Summons cost a turn to set up; Haste is concentration and competes with your control spell |
| `lockdown` | Save-or-lose against crowds; area control that composes rather than duplicating | Enemy saves climb +1 per 6 levels, so a static DC decays; single-target-only control falls further as fights crowd |
| `front-line` | Weapon damage into a priority target — smites, Extra Attack, Fighter 11's third attack | Resource-limited burst runs dry in long fights; needs an endurance answer |
| `reaction` | Spends Lone Wolf's **second reaction** — off-turn Sneak Attack, Uncanny Dodge, Riposte, opportunity attacks | Worthless if nothing triggers it; needs a build shaped around being attacked |
| `short-rest` | Runs on the short clock — pact slots, superiority dice, ki, Second Wind | Usually caps spell tier or damage ceiling against a long-rest caster |
| `durability` | Refuses to die — heavy armour, shields, flat reduction, and **self-healing counts here** | Being un-killable does not end fights, and a duo cannot afford a passenger |
| `skills` | Clears gates — Expertise, Guidance, covering checks the partner cannot | Depth saturates at one source; breadth does not. Rarely worth building around, always worth dividing |

**There is no carry/support field.** The ledger pairs every chassis with every other, so a body is
not typed as one or the other — the niche already says what it does with its turns, and whether it
reads as the damage half of a duo depends on the partner, which a seed does not know.

### One build per niche — a subclass is not one chassis

**`builds` is keyed by niche, so a subclass can express more than one body.** A Hexblade is a
Charisma smite frontliner *and* a short-rest blaster; those are different chassis that pair with
different partners, and collapsing them to one loses whichever you did not write down.

But most subclasses have exactly one honest expression, and **a second build must earn itself**:

- **It must differ in the split.** Same levels with a different label is a variant, not a build,
  and is rejected on load.
- **It should differ in at least one of: primary stat, what the body does with its turns, or
  resource clock.** If those three match, you are describing gear or spell choices, which the pair
  sheet decides later — not a chassis.
- **One per niche, three maximum.** Past three you are reflavouring one of the first three.

Write a second build when it is real. Do not manufacture one per niche to look thorough — an
inflated seed file drags weak bodies into the roster through the niche floors.

`chassis` is a ledger id: **one word**, evocative, unique, not the class name unless the class *is*
the identity — Bombard, Volley, Zeal, Chains, Mercy, Hexplate.

## The split

The build's 20-level expression: **one, two or three distinct classes, summing to 20, joined by
`/`.** Each class appears once, carrying its total, **with its subclass in parentheses**.

```
Cleric 14 (Life) / Paladin 6 (Oath of the Ancients)                     two classes
Sorcerer 17 (Storm) / Cleric 1 (Tempest) / Fighter 2 (none)             three, the maximum
Fighter 20 (Battle Master)                                              one class is legal, and rare
```

**Name the subclass for every class in the split.** A reader cannot rebuild `Fighter 2` — Battle
Master, Champion and Eldritch Knight are different dips. If a class is taken below its subclass
level, write `(none)`.

### Dipping is close to free here, and mono-class is the exception

The single largest error in the last sweep was mono-class splits: three quarters of the roster took
one class for all twenty levels. **That was wrong, and the numbers say so** — the multiclass
quarter beat the mono three-quarters by +0.8 on Actions, the axis that caps Tempo, and took a
third more than its share of the frontier.

The reason is arithmetic. **Feats key off character level (3/6/9/12/13/15/18), not class level, so
a dip costs no feats at all.** Nor does it cost save proficiencies: Lone Wolf already grants two
of its own, so the classic Fighter 1 or Sorcerer 1 for Constitution buys nothing here. A dip in
this list costs only what the top of the abandoned class table would have given — and outside a
handful of real capstones, that is very little.

So **the burden of proof runs the other way**: a 20-level single class needs a reason, and the
reason must be a specific late feature worth more than the best three levels available elsewhere.
Paragon has one (Paragon Of Legend at 20 breaks the stat ceiling). Most classes do not.

Read the `## Dip value` sections as a menu you are expected to buy from, not as background.

- **Never more than three classes.** A fourth is a build that has stopped being a chassis.
- **A feature you name must be one the split actually reaches.** If `why` says a body has
  slot-free Counterspell, the split must include the level that grants it. Class files list a
  level against every feature — `L13 Will Over Weave` — and a `## Duo relevance` bullet praising a
  subclass is describing the *whole* subclass, not the three levels you are dipping into. Check
  the level before you cite the feature.
- **Do not record levelling order.** No arrows, and never the same class twice. Which block comes
  first matters enormously to a build, but it is a **pair-sheet** decision — a seed that encodes
  it is claiming precision the sweep does not have. `Rogue 9 (Thief) / Ranger 11 (Gloom Stalker)`, not
  `Rogue 1 -> Ranger 11 -> Rogue 8`.
- **It must sum to 20.** A split that does not has shipped here before, and `--check` refuses it
  rather than letting it through.
- The **level-1 class** owns saving throws and armour; it is a real choice, not a formality.
- Feats land at character **3/6/9/12/13/15/18**, plus **11 for Fighter and Rogue only**. Every
  mod page's own feat table is wrong for this list.
- The primary stat must reach **20 by character 6 and 22 by 18**. One stat, in practice.
- **The subclass you were assigned must take more levels than any other class in the split** — it
  is the dominant class, not the only one. `Cleric 14 (Life) / Paladin 6` is right. `Paladin 14 /
  Cleric 6 (Life)` is a Paladin build and belongs to whoever was assigned Paladin.
  If your subclass has nothing to offer *except* as a 3-level dip under someone else's body,
  **that** is what makes it a `dupe` or a `none`. It is a judgement about the subclass being
  seeded, and says nothing about whether that body should itself dip. It should.

**Two players, Lone Wolf, level cap 20.** Lone Wolf is baseline for every body from level 1:
2 Actions, 2 Bonus Actions, 2 Reactions, **halved damage from all sources**, +4 to two abilities
with save proficiency in both. Score what the chassis adds **above** that floor.

### The other half of the split comes from the shared read set

Your assignment names, besides your own classes, **every class's `## Dip value` section**. Read
all of them. They are the authority on what a partner class sells at each level, and a split you
cannot justify from them is a split you guessed.

This is the one place the read rule opens up, and deliberately: a seed may name up to three
classes, and you were only assigned one of them. Nothing else — not another class's subclass list, not the manifest —
comes with it.

**Inquisitor is unusable past level 2 on the shipped install** — dangling subclass GUID at level 3.
Seed its subclasses `none` unless the split stops at 2, and say the mod needs updating to 2.2.1.

**The split is provisional, and that is expected.** It is a starting hypothesis for the scoring
pass, which revisits it with the full rubric and both classes' complete text in front of it.
Get the majority class and the shape right; do not agonise over whether the dip is 2 or 3.

## `peak`, `peak_axis` and `breadth`

Two numbers, both judged in **Act II** (characters 9–15, 5–6 feats, 8th-level slots) because it is
the richest band — six feats and nearly every run-defining breakpoint. Both rank builds for
promotion and are then discarded; the ledger re-scores every promoted chassis from scratch.

**`peak`** is the highest rung this body reaches on **any single axis**, 0–5, and `peak_axis`
names that axis.

**`breadth`** is **how many of the ten axes reach 3 or better** in Act II, 0–10.

> **Why `breadth` exists.** `peak` is a maximum, and a maximum cannot see the thing a dip buys.
> Fighter 20 and Fighter 11 / Rogue 9 both peak at 5 on `st`; the dip's gain lands on `act` and
> `skl`, which the maximum discards. The last sweep asked for `peak` alone and came back
> three-quarters mono-class — agents optimised the one number they were given, and that number was
> blind to breadth by construction. Write both, and let a wide body show as wide.

Do not inflate `breadth`. A 3 is "does this competently for the act"; most bodies are 0 or 1 on
several axes and a `breadth` above 6 is a claim that needs a split to back it.

Rungs are **act-relative**: a `peak` of 5 means "as good as a body can be at this point in the run", not ever.
A body that is merely competent peaks at 3. Be willing to write 2.

| key | axis | **4 =** | **5 =** |
|---|---|---|---|
| `st` | single-target | **computed, not judged** — ratio to par (48 / 61 / 76): 4 = 1.5–2.0× | 5 = ≥ 2.0× par |
| `aoe` | AoE | **computed, not judged** — ratio to par (22 / 28 / 32): 4 = 2.0–3.0× | 5 = ≥ 3.0× par |
| `dur` | durability | heavy armour + shield + one flat-reduction or halving source | + everything the act's feats stack — Heavy Armour Master, Shield Master Block, Tough |
| `act` | actions | multiattack + bonus-action attack + a third Action, or a multi-body summon set | an Action handed to the **other** body (Haste, Twinned Haste, Commander's Strike) on top of own extra attacks |
| `ctrl_s` | control, single | single-target control costing **no concentration** that does not decay as saves scale | + slot-free hard control on a short-rest clock — Brand of the Sapping Scar, Chains of Carceri |
| `ctrl_a` | control, area | area control costing no concentration, or that does not decay | slot-free **repeatable** area control on a short-rest clock |
| `rsc` | rescue — **outward only** | prevention on the partner, or a no-action aura temp-HPing them each round | prevention **and** restoration **and** no-action outward healing — Twilight Sanctuary + Revivify + Death Ward |
| `skl` | skills | Expertise ×2 + Guidance + all but one of the act's named gates | every named gate cleared |
| `sav` | saves | four+ proficiencies covering Wis/Con/Dex, or a blanket booster | all six, or that coverage **and** a blanket booster |
| `end` | endurance | ~40 units per long-rest cycle — Monk 14 ki, plus healing between fights | **unbounded**: at-will damage with no clock — Sneak Attack, Champion, Crimson Rite |

Two rules that bite:

- **One concentration spell per body.** Control that spends no concentration is worth a full rung
  more than control that does.
- **Self-healing is `dur`, not `rsc`.** Only what a body can aim at its *partner* is rescue. Damage
  redirection (Warding Bond, Protective Bond) **never scores above 1** — in a duo it moves damage
  from one half of the party to the other.

## Traps that have cost points here

- **A flat feature must fall.** Fixed dice with no upcast path decay against Combat Extender's
  **+126% regular and +170% boss HP**. An at-will cone that is 3d10 at character 10 is still 3d10
  at 20 — Eldritch Cone/Line literally stops scaling at 10.
- **`StackId` is a cap.** A summon or brand carrying one *replaces* rather than accumulates.
- **Absolute Wrath is ON** — ordinary enemies carry layered resistances, not just bosses. A body
  locked to one commonly-resisted damage type **caps at 4** on `st` from Act II.
- **Save DCs decay**: bosses gain +1 spell save DC per 7 levels, enemies +1 per 11. Pure save-DC
  control loses a rung by Act III; Disadvantage-on-saves does not.
- **Eldritch Blast is 1d8 per beam here**, not 1d10. Any damage math from outside Listo is
  overstated.
- **Archive versions lag mod pages.** If the class file records drift, trust the class file.
