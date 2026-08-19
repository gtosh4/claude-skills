---
name: listo-ledger
description: Build or update the Listonomicon pairing ledger — score every candidate chassis on the ten-axis radar, rank every possible pairing on tempo, resilience, duration and utility, and render the ledger artifact. Use when comparing many possible duos rather than building one.
---

# Listo pairing ledger

**The ledger answers "which pairings are worth building?"** It is upstream of
`listo-build`: the ledger narrows a roster of chassis to a shortlist, and each
shortlisted pairing then gets a real pair sheet.

**Author JSON. Never write ledger HTML.** `scripts/render_ledger.py` holds the
CSS, the scoring, the field table and every derived number:

```sh
scripts/render_ledger.py ledger.json -o ledger.html
```

`assets/ledger-schema.md` is the shape. `assets/ledger-example.json` is a
working ledger to copy.

## Discovering the roster

**The roster is the one thing this format cannot check.** Everything else fails closed — an
unknown booster raises, a chassis in the cut without prose refuses to build — but a chassis nobody
thought of is simply absent, and the ledger renders happily without it. The sweep closes that hole.

**Ask before you sweep.** If the user named the chassis, score those. If the list is absent or
ambiguous — "compare the good duos", or four names and an "etc." — **ask**, with
`AskUserQuestion`: score the named list as it stands, or sweep the subclass inventory first and
add whatever clears the bar. It is their run and their patience. Do not decide it silently in
either direction.

### The unit is the subclass, and the inventory is derived

```sh
scripts/seed_index.py --list      # the work-list: 157 subclasses across 17 classes
scripts/seed_index.py --check     # every subclass seeded? both directions
scripts/seed_index.py --promote   # every viable build; --limit N to ration instead
```

The work-list comes from `listo-build/data/classes/*.md`, not from a list in this file — the same
reason roster order is derived. Keys are `<class file>/<### heading verbatim>`; copy them from
`--list`, never retype them. `--check` fails on **unseeded** subclasses and on **stale** seeds
whose heading no longer exists, which is what catches a Listo update that renamed something.

Seeds live in `assets/chassis-seeds.json`. `assets/chassis-seeds-example.json` is ten worked rows
covering all four verdicts, two of them carrying a second build — copy it and fill until `--check`
is clean.

| verdict | means | fields |
|---|---|---|
| `candidate` | has at least one viable 20-level expression | `builds` |
| `dupe` | its best expression *is* another seed's body | `dupe_of`, `why` |
| `none` | no 20-level split rescues it | `why` |
| `not-a-subclass` | the heading is a table or a note, not a subclass | `why` |

### A subclass is not one chassis

**A seed is keyed by subclass; the unit of judgement inside it is the `builds` object, keyed by
niche.** A Hexblade is a Charisma smite frontliner *and* a short-rest blaster — different splits,
different partners, different rows in the field table. One seed per subclass would silently keep
whichever the sweep agent happened to write down and lose the other, which is the same class of
invisible loss the sweep exists to prevent.

Keying by niche makes "at most one build per niche" structurally true rather than a rule someone
has to remember. Three guards keep it from inflating, all enforced on load:

- **Two builds must differ in the `split`** — same levels, different label is a variant, and the
  pair sheet decides variants.
- **Three builds maximum.** A fourth is a reflavour of one of the first three.
- **`chassis` ids are unique across every build**, since they become ledger keys and anchors.

Inflation is not a cosmetic problem: extra builds reach the roster through the niche floors below,
so a padded seed file drags weak bodies into the scored set.

### A build is one line of judgement, not a score

Cheap on purpose. Ten axes × three acts is thirty judgements per chassis; you cannot afford that
across 157 subclasses and would throw most of it away. So a build carries exactly one number:

- **`split`** — that build's 20-level expression: **one to three distinct classes summing to 20**,
  joined by `/`, each class appearing once with its total. `--check` parses it and refuses a split
  that misses 20, names a fourth class, repeats a class, or uses arrows — which is how the
  archived v1 roster's 18-level `Shepherd Druid 17 / Cleric 1` would have been caught before it
  was published. **Levelling order is deliberately not recorded**: it moves features between acts
  and therefore matters, but it is the pair sheet's decision, and a seed asserting it would be
  claiming precision the sweep does not have.
- **`peak` / `peak_axis`** — the highest rung this body reaches on any axis, **in Act II**, and
  which axis. Act II because it is the richest band. The number exists to rank for promotion and
  is then discarded — the ledger re-scores every promoted chassis from scratch against
  `listo-build/references/axis-rubrics.md`.
- **No role.** A build is not typed carry-or-support: the ledger pairs every chassis with every
  other, so whether a body reads as the damage half of a duo depends on the partner, which a seed
  does not know. The `niche` it sits under — from `listo-build` §1a — already says what it does
  with its turns.
- **`why`** — one sentence. The rejections need it more than the candidates do; a `none` without
  a reason is indistinguishable from a subclass nobody looked at.

### Score everything viable, then select on real numbers

**By default `--promote` promotes every viable build.** No bar, no cap. A seed's `peak` is a
one-act triage guess that exists to make the *sweep* cheap; the pair score is a real number
derived from thirty authored values per body. Discarding a chassis on the estimate, before the
real number exists, throws away the better instrument to save the cheaper one.

So the cut moves downstream. Score thoroughly, then threshold on the field table — which is
sorted by score, carries every block separately, and flags idle bodies and holes. `entry_limit`
then decides how many pairings earn prose.

**The cost this commits to is linear and it is the only real one:**

```
roster size × chassis scoring    ~5k tokens each — thirty ints, a saves set, prose
C(roster, 2) pairing scores      free, derived from those ints
```

Pairings cost nothing worth counting: roughly 600 bytes and microseconds each, so 130 chassis is
8,385 pairings and about 5MB against a 16MB ceiling. The field table stays exhaustive however
large the roster grows.

### Rationing, when the scoring budget will not stretch

`--limit N` re-imposes a cap, and only then do the floors and the bar apply:

| route | rule |
|---|---|
| **class floor** | every class's best build, whatever its peak |
| **niche floor** | every niche's best build, likewise |
| **bar** | `peak >= 4`, filling whatever the limit leaves |

Floors are **guaranteed slots, not fallbacks**. Rationing on the bar alone would rebuild exactly
the roster that retired the correlation figures — a shortlist selected for being good at
something, which therefore cannot show whether the blocks genuinely trade off. Floors force a
class's honest best into the sample even when that best is a 3, so a rationed roster is
**stratified** rather than a highlight reel.

They are also coarse: a flat class floor gives Cleric's twenty-one domains the same single slot
as Artificer's four. That asymmetry is tolerable when rationing is a budget concession and
indefensible as a default, which is the second reason the default is to score everything.

Ties break by address, so a rationed cut is deterministic. **If the floors alone exceed the
limit, coverage wins** — the roster is the floors and the script says so. And a build can then
miss for two unrelated reasons, which `--promote` reports separately in the `caveats.excluded`
block: *under the bar*, or *at or over the bar, past the roster limit*. Never merge those two —
the second would tell a reader the ledger judged a chassis poor when it did not.

`chassis` names are ledger ids: one word, unique, evocative, and not the class name unless the
class *is* the identity — Bombard, Volley, Zeal, Chains. Loading the seeds file refuses a
duplicate name, since two chassis sharing an id would collide as anchors in the rendered ledger.

### Running the sweep — the brief is the whole trick

157 subclasses is a subagent job. The cost is dominated not by the class files but by **shared
reference material**: `listo-build/SKILL.md`, `axis-rubrics.md` and `listo-rules.md` are ~32k
tokens together, and an agent that opens them pays that toll *per agent*. Seventeen agents reading
freely costs upward of 690k tokens; the same sweep briefed properly costs about 137k at two agents
and 183k at four.

Three rules produce that difference:

1. **`assets/sweep-brief.md` is the agent's only *prose* reference.** It compresses those ~32k
   into ~2.6k — verdicts, split rules, the rung-4/5 anchors for all ten axes, the niche
   vocabulary and the traps. Paste it into every agent prompt.

   It does **not** compress the cross-class material, and an earlier version's attempt to is
   worth recording as a mistake. A seed's split names two classes and an agent is assigned one,
   so it cannot invent what the other sells. A hand-written dip menu covered which class to *dip*
   into at levels 1-6 and said nothing that supports a `Cleric 12 / Fighter 8`. Every agent
   therefore reads all seventeen **`## Dip value`** sections — ~10.6k, authoritative, emitted in
   the assignment by `--assign`. The seed's split stays **provisional**: it is a hypothesis for
   the scoring pass, which revisits it with both classes' full text.
2. **Assignments come from `--assign`, never by hand.**

   ```sh
   scripts/seed_index.py --assign 8
   ```

   It bin-packs the classes by reading cost and prints, per agent, the exact **line ranges** it may
   read — at-a-glance plus the subclass section, ~77k across all seventeen classes against ~148k
   for whole files — and the exact seed keys, verbatim. Keys copied from here cannot be mistyped,
   which is the difference between a clean `--check` and an afternoon of reconciliation.
3. **Batch to 4 agents or fewer.** Everything paid per agent — overhead, the brief, and now the
   ~10.6k shared dip set — dominates, so agent count is the sweep's main dial:

   | agents | total | subclasses each |
   |---:|---:|---:|
   | 2 | ~137k | 78 |
   | 4 | ~183k | 39 |
   | 8 | ~276k | 19 |
   | 17 | ~484k | 9 |

   Four is the balance point: ~39 subclasses and ~30k of reading per agent, which is one
   comfortable pass, at a little over half what eight costs.

Agents return **raw JSON only**, one object of seed records. Merge them into
`assets/chassis-seeds.json`, then `--check`. Anything an agent skipped or mistyped surfaces there
as unseeded or stale, so a bad batch is re-run alone rather than re-running the sweep.

**Do not have agents verify against paks.** A seed is a ranking judgement that gets discarded; pak
reads belong in the ten-axis scoring of the ~30 chassis that actually get promoted, where the
claim is load-bearing.

### Wire the rejects into the ledger

`--promote` prints the non-promoted seeds grouped by reason, formatted for
`caveats.excluded.items`. Paste it. That is what the sweep buys: a reader can see what was
considered and dropped, so the roster's bias is on the page rather than in your head.

Then score the promoted seeds normally. The seed's `peak` has no standing from that point on.

### The seeds file is a cache, and it knows when it is stale

A seed is an expensive judgement that stays valid until something it was derived from changes. So
every seed records what it was derived *from*, and `--check` reports what that invalidates.

**Two stages, two keys, and they go stale independently** — that separation is the point. Editing
`axis-rubrics.md` must not force a 157-subclass re-sweep, and editing the sweep brief must not
force a re-score of every chassis.

| stamp | where | covers | invalidated by |
|---|---|---|---|
| `src` | seed | that subclass's `###` block **plus** its class's at-a-glance section | a Listo update that rewrites the subclass, or the class's headline facts |
| `seed_deps` | seed | `assets/sweep-brief.md` | changing the rules the sweep judged under |
| `score_deps` | **build** | `axis-rubrics.md`, `scoring-model.md`, `gates.md` | changing the rules the *scores* were authored under |

`DEPS` in `seed_index.py` is that registry — add a file to it when a new document starts governing
one of the two stages, exactly as you would add a booster to the renderer's.

`--check` sorts the whole file into five buckets: **unseeded**, **stale** (heading gone),
**drifted** (`src` moved), **rules changed** (`seed_deps` moved) — those four block — plus
**re-score** and **never scored**, which are reported but do not, since a stale score is a
ledger-authoring job rather than a sweep one. A seed that must be re-swept is not also reported as
needing a re-score; the seed comes first.

The workflow after a sweep, and after any later edit:

```sh
scripts/seed_index.py --assign 8              # only what is unseeded, drifted or under old rules
# ... merge the agents' JSON into chassis-seeds.json ...
scripts/seed_index.py --stamp                 # record src + brief hashes on every seed
scripts/seed_index.py --check                 # five buckets; blocks while any of the first four bite
scripts/seed_index.py --promote               # the cut
# ... author ten-axis scores for the promoted builds into ledger.json ...
scripts/seed_index.py --stamp --scored "warlock/The Hexblade:front-line,cleric/Life:durability"
```

**`--assign` reads the cache and hands out only the work that is actually needed.** A Listo update
that touches two class files costs two agents, not eight. `--assign N --all` forces a full
re-sweep when you want one.

`--stamp` fills hashes; it never overwrites a seed's judgement. It is deliberately a separate
command from `--check`, so accepting drift is an act rather than a side effect: if a class file
changed and you decide the seed still holds, you run `--stamp` and that decision is recorded.

### Re-running it

Cheap and idempotent, and after the first sweep it is *incremental*. When Listo updates, `--check`
names every new subclass, every renamed heading and every seed whose source text moved; `--assign`
hands out exactly those. Nothing else in the ledger needs touching.

## What you are scoring

Each chassis gets **ten axes × three acts** — Control is split crowd-versus-boss
exactly as damage already is. Three files own the rules and they do not overlap:
**`listo-build/references/axis-rubrics.md`** gives the content anchors — what a 5
actually *is* in named manifest features, per act; **`listo-build` §5a** gives the
functional ladder (5 Surplus → 0 Absent) and what each axis measures; and
**`listo-build/references/scoring-model.md`** owns how two bodies combine, the
fight-type coefficients, the weights and the score. Read all three before scoring.

The act bands, and why scores are act-relative, are `axis-rubrics.md`'s — including the
`CombatExtender.json` derivation behind them. Read it there rather than trusting a summary.

**Illithid: `scoring-model.md` fixes the allocation, this file expands the judgement.** A ledger
row is scored at the **even share** because a row has no partner yet and only a fixed allocation
keeps rows comparable; the rubric ceilings are authored illithid-free, so what moves a row is how
much better or worse this chassis *converts* that share than its neighbours do. Both of those
rules, and the IMR the share buys per act, live in `scoring-model.md`'s illithid section.

What is here and nowhere else is the both-ways table `axis-rubrics.md` points at:

| Converts well | Converts badly |
|---|---|
| A **cheap Action** — a body whose turn is often a cantrip loses nothing casting a power; the passive powers (Psionic Overload, Cull the Weak, Luck of the Far Realms) cost no Action at all and **scale with attack count** | An **expensive Action** — Fighter 11 gives up six attacks per cast, a Paladin gives up smites |
| A **real casting stat on the last class added** — that is where power DCs come from — and doubly so with Arcane Acuity | **No casting stat**: every save power in the tree is dead, leaving only the no-save half |
| **Spare reactions**: Eldritch Ward and Psionic Backlash are interrupts, and Lone Wolf's second reaction is often idle | Bonus action and both reactions already committed — Force Tunnel and the wards have nowhere to go |
| **At-will damage** chassis: charges are a long-rest pool bolted onto a body with no long-rest clock, so the Endurance cost is small | **Full casters**: charges compete for the rest that slots already force |
| **Armour and AC to spare** — the `+IMR` tax and Psionic Overload's self-damage are cheap here, and the Cerebral Citadel set's +1 AC per 5 powers wants medium-armour proficiency | **Soft bodies** — the tax lands on the half enemy AI already prefers |
| A body **short on damage types** — Psychic and Force answer Absolute Wrath's layered resistances | A body that already carries two damage types |

Record the even-share baseline as a `caveats.assumptions` item, so a reader knows which allocation
the column assumes. A pair sheet may then deviate from it — concentrating the pool lifts one body
and lowers the other — and that is `listo-build` §5a's business, not the ledger's.

Then the renderer does the rest. Your job is three things and nothing else:

1. **The chassis scores** — ten ints per act, honestly, with the low ones low.
   Index 8 (saves) is `null`: author the `saves` set instead and let the renderer derive it.
2. **`reach`** — `ranged`, `hybrid` (melee with a real ranged option), `mobile`
   (melee with repeatable mobility), `static` (melee, none).
3. **The prose** — what each chassis is, and why each entry reads the way it does.

## Why the ledger shows four blocks and no total

The blocks — Tempo, Resilience, Duration, Utility — are `scoring-model.md` §2's, and Actions
capping Tempo rather than joining it is its §6. The ledger only has to obey them; the argument,
the coefficients and the provisional-versus-derived status of every constant are all there.

What is the ledger's own call is **refusing to collapse the blocks into one number**. Two pairings
with an identical damage block can differ by seven points of delivered damage, and a total cannot
see it. The field table therefore ranks by score but shows the blocks beside it, and the entries
quote tempo and non-tempo separately.

`listo-build` SKILL.md's **split rule** — 5 + 0 is worse than 3 + 3 — is the reason the idle-body
flag exists, and the control split means it now catches a passenger on the control side as well as
the damage side.

## Method notes that keep the ledger honest

- **Entries are derived, not chosen.** One per chassis, headlined by its best
  partner, and a pairing two chassis both name is kept once. Hand-picking entries is how the
  entry list and the field table drift apart — the renderer refuses to build if a chassis in the
  cut has no prose.
- **Roster order is derived too.** A hardcoded list silently drops every chassis
  added after it was written; this has already happened once.
- **Variation figures do not exist until render time.** Write the clause, not
  the number.
- **Re-scoring is cheap and should be frequent.** Change the ints, re-render.
  Nothing downstream needs hand-patching.

## Confirm special handling before you author it

Some fields are not plain data — `boosters`, `reach`, `prof` abilities, axis kinds — and the
renderer applies each one through a registry. **Before authoring such a value, confirm the
renderer implements it.** If you cannot point at the line that applies the effect, it is not
implemented.

**The renderer fails on an unrecognised value rather than skipping it, and that is deliberate.**
A dropped booster contributes nothing, so the score lands **too low** — and a score that is too
low is indistinguishable from an honest one. The field table still ranks, the entries still
render, and the chassis just sits a rung below where it belongs, permanently and invisibly. Every
other bug in this format announces itself; this one would not.

Failing closed makes the check reactive instead of a standing tax. You do not audit boosters
before each render. You fix one crash the first time you author something new. Never add a
permissive branch, a default, or a warn-and-continue to any of these — see
`assets/ledger-schema.md`, "Anything with special handling fails closed".

## Verify before you score

Score against the compiled data in `listo-build/data/`, and when a claim is
load-bearing read the pak itself with `listo-build/scripts/lspk.py` — mod pages
and changelogs go stale, installed archives do not.

**The pak-reading traps are `listo-build` SKILL.md's** — `StackId` as a cap, and a passive's real
strength hiding in its conditional `Boosts` — and the decay of flat, non-upcasting features
against Combat Extender's inflated HP is priced in `axis-rubrics.md`, axis by axis. They cost the
ledger points exactly as they cost a sheet points; there is no ledger-specific version of them.

The one this format adds: **check the level arithmetic.** A `split` that does not sum to 20 has
been shipped here before. `seed_index.py` now parses every seed's split and refuses one that
misses 20 or names more than three classes — the ledger renderer still never parses the string,
so this is the only place it is caught.

## Updating a published ledger

Re-render the same JSON and republish to the same artifact URL. When the roster
changes, add the chassis and its prose in one edit — the renderer will tell you
if an entry is now missing, which is the only bookkeeping the format needs.
