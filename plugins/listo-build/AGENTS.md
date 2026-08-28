# Listonomicon mechanics research

These instructions apply to all work under `plugins/listo-build/`.

## Evidence order

For mechanics research, prefer evidence in this order:

1. The current compiled SQLite database at `/tmp/listonomicon-character-data.sqlite`.
2. The resolved summaries under `skills/listo-build/data/` when they already answer the question.
3. An installed PAK only when the database reports an extraction error, does not extract the
   relevant runtime format, or a compiler result is being audited.
4. `bg3.wiki` for vanilla facts not represented in the installed base-game archives.
5. Mod pages, changelogs, repositories, and other secondary sources only as leads.

The database is primary evidence: it is compiled from the installed BG3 gameplay archives and
all enabled Listonomicon PAKs, records provenance on every row, and puts base and mod definitions
into one effective load order. Do not open or extract PAKs for routine class, race, feat, spell,
passive, status, item, progression, spell-list, root-template, or localization questions.

Never present a mod page or wiki description as proof of what this installation does. Clearly
mark unresolved claims and distinguish database evidence from a wiki fallback.

## Build or refresh the database

The compiler is:

```text
plugins/listo-build/skills/listo-build/scripts/compile_mod_data.py
```

It requires BG3 Forge 0.2.0, and `lupa` to execute Script Extender Lua (without it the runtime
passes are skipped and recorded as `unavailable` in `runtime_lua`, rather than silently omitted).
From the repository root:

```bash
python3 -m venv /tmp/listo-db-venv
/tmp/listo-db-venv/bin/python -m pip install "bg3forge[zstd]==0.2.0" lupa
/tmp/listo-db-venv/bin/python \
  plugins/listo-build/skills/listo-build/scripts/compile_mod_data.py \
  /tmp/listonomicon-character-data.sqlite
```

The default build uses up to 16 worker processes. Override only for resource constraints or
comparison:

```bash
# Low-memory/debug build
/tmp/listo-db-venv/bin/python \
  plugins/listo-build/skills/listo-build/scripts/compile_mod_data.py \
  /tmp/listonomicon-character-data.sqlite --workers 1
```

Default installation paths are:

```text
BG3 Data:  /mnt/mercury/Steam/steamapps/common/Baldurs Gate 3/Data
Listo:     /mnt/mercury/Games/Listonomicon
Profile:   Listonomicon
```

Override them when necessary:

```bash
/tmp/listo-db-venv/bin/python \
  plugins/listo-build/skills/listo-build/scripts/compile_mod_data.py \
  /tmp/listonomicon-character-data.sqlite \
  --game-data "/path/to/Baldurs Gate 3/Data" \
  --install-root "/path/to/Listonomicon" \
  --profile Listonomicon
```

The output is replaced atomically. Rebuild it after changing the BG3 patch level, `modlist.txt`,
`modsettings.lsx`, enabled mod files, or compiler. A successful complete build reports zero
extraction errors. Verify that invariant:

```sql
SELECT status, COUNT(*)
FROM resources
GROUP BY status;
```

`status = 'error'` means the affected resource is not trustworthy until the parser or source is
fixed. Do not silently answer around it.

Extraction results depend on the parser build, which `metadata.parser_version` records. Two
`RootTemplates/_merged.lsf` entries (`Fade's Equipment Distribution AIO`, `VFX Library by
Shivero`) currently fail under bg3forge 0.2.0 with `malformed LSF resource: match offset beyond
output start`; both reproduce outside the compiler and neither holds character-build records.
Compare `parser_version` before concluding that a rebuild regressed.

## Database schema

Start with:

```sql
SELECT key, value FROM metadata ORDER BY key;
SELECT record_type, table_name FROM data_types ORDER BY record_type;
```

Core metadata tables:

| Table | Purpose |
|---|---|
| `metadata` | Build paths, profile, worker count, scope, and load-order semantics |
| `mod_load_order` | Base archives and enabled modules in effective order |
| `resources` | Every indexed PAK entry, extraction status, sizes, source, and provenance |
| `data_types` | Original record type to generated `type_*` table mapping |
| `runtime_config` | Script Extender / MCM JSON, including the loose `SE_CONFIG` files no PAK contains |
| `runtime_lua` | Every mod whose Lua was executed, with status, log, and unimplemented APIs |
| `runtime_mutations` | Every static record a mod rewrote at load, with the field and new value |
| `progression_feats` | Per progression row: static value, runtime value, effective value |
| `class_feat_levels` | One row per class and level: does it grant a feat, and who changed it |

Each generated `type_*` table has the same provenance columns:

```text
source, source_kind, load_order, archive_priority,
module_uuid, module_name, pak_path, entry_path,
format, record_name, record_uuid, using_record, data, raw
```

- `source_kind` is `base_game` or `mod`.
- Higher non-null `load_order` wins.
- `data` is JSON.
- Stats fields are normally direct JSON keys, such as `$.Boosts`.
- LSX/LSF fields are normally under `$.attributes`, such as
  `$.attributes.Level.value`.
- `raw` preserves the original Stats block when applicable.

## Prefer the query helper for routine lookups

`plugins/listo-build/skills/listo-build/scripts/lsdb.py` (stdlib only, read-only) encodes the
load-order, patch-layer and `using_record` semantics below, so routine questions cost one short
command and a compact answer instead of a chain of raw SQL with wide JSON rows:

```bash
L=plugins/listo-build/skills/listo-build/scripts/lsdb.py
$L tables progress                 # which type_* table holds a record type
$L find battlemind                 # where a name appears; --deep searches payloads
$L get Projectile_HellrimeBlast    # EFFECTIVE record: winner, patch layers merged,
                                   #   using-chain resolved with per-field origin,
                                   #   LSX attributes flattened, handles localized
$L get X --all                     # audit view: every definition in effective order
$L loc "potent robe"               # localization handle <-> text
$L feats Mesmerist                 # EFFECTIVE feat levels: runtime overrides applied,
                                   #   with the static LSX cadence and the mod that moved it
$L grants Snowlight --level 3 --expand   # ClassDescription -> progression -> per-level
                                   #   grants, passives and spell lists one line each
```

Values are truncated at 160 chars (`--full` disables; `--db` overrides the default path).

### From a notebook or REPL, import it — do not hand-roll the resolution

`lsdb.py` also imports as a library, which is the supported way to reuse these semantics in
`eval`-style work:

```python
import sys; sys.path.insert(0, "plugins/listo-build/skills/listo-build/scripts")
import lsdb

db  = lsdb.connect()                      # or lsdb.connect(path) / $LSDB_DB
rec = db.record("MAG_CELESTIAL_HASTE")    # EFFECTIVE record; table auto-discovered
rec.get("Boosts")                         # inherited from HASTE, still present
rec.origin("Boosts")                      # 'HASTE' — which parent supplied it
rec.data()                                # plain {field: value}
rec.load_order, rec.source, rec.entry_path, rec.chain, rec.layers, rec.raw
db.records("BOLDSTARE_SUNDERING")         # a name in >1 table: passive AND status
db.sql("SELECT ... FROM type_armor WHERE ...")   # plain dicts, for the rest
```

`record()` **raises** when a name exists in more than one table rather than picking one — the
Mesmerist pattern of passive `BoldStare_X` beside status `BOLDSTARE_X` is the common case, and
matching is case-insensitive. Pass `table=` or use `records()`.

Fall back to raw SQL for anything the helper does not cover, and for verifying its output on
load-bearing claims — but **raw `json_extract` does not resolve inheritance**, and three failure
modes have each produced a wrong published claim:

1. **Inherited fields read as absent.** `json_extract(data,'$.X')` is null when the `using` parent
   supplies `X`. `BOLDSTARE_SUNDERING` declares no `StatusPropertyFlags` and inherits
   `MultiplyEffectsByDuration` from `BOLDSTARE_DISORIENTATION`; reading the child alone turns a
   −3 debuff into −1.
2. **A patch layer naming itself truncates the chain.** A record may have an early row with a
   *foreign* `using` (the real parent) and a later row whose `using` is its own name. Walking only
   the last row's `using` hits the self-reference, stops, and drops every inherited field.
   `MAG_CELESTIAL_HASTE` is the regression case — Gustav row `using "HASTE"`, Honour row
   `using "MAG_CELESTIAL_HASTE"` — and what goes missing is the whole
   `ActionResource(ActionPoint,1,0);AC(2);…` package: the difference between "an inert marker" and
   "full Haste".
3. **Truncated payloads read as complete.** Functor strings run long — `BoldStare_Sundering` is 815
   characters. Printing a slice and concluding a clause is absent is not a negative result. Print
   the length, or split on `;` and print every clause.

## Runtime overrides: what the static tables cannot tell you

A Script Extender mod can rewrite a static record when the game loads, so an LSX or Stats value
is not automatically the effective one. The compiler therefore extracts each mod's Lua, and for
every mod that references `Ext.StaticData` it executes that mod's own scripts in a sandbox
(`lua_harness.py`) against a stubbed `Ext` API, recording each write. The effective value is
consequently evidence produced by the mod itself, not a formula transcribed by hand that would
rot the next time the mod updates.

**Feat cadence is the standing example, and it is not 4/8/12.** `Universal Feat Every X Level`
rewrites `Progression.AllowImprovement` from MCM settings, so the installed profile grants feats
per **class** level at **3, 6, 9, 12, 13, 15, 18**, plus **11 for Fighter and Rogue**. Reading
`type_progression` alone yields the vanilla 4/8/12 and is wrong:

```bash
$L feats Mesmerist          # effective cadence, the static one, and the mod responsible
$L feats                    # every class
```

```sql
-- every place a runtime override changed the answer
SELECT class_name, level, static_grants_feat, grants_feat, overridden_by
FROM class_feat_levels WHERE changed_at_runtime ORDER BY class_name, level;

-- what any mod rewrote, not just feats
SELECT mod_table, record_type, field, count(*) FROM runtime_mutations
GROUP BY mod_table, record_type, field ORDER BY 4 DESC;
```

Check `runtime_lua` before trusting a negative: `status` is `ran`, `skipped_no_static_data`
(the mod never names `Ext.StaticData`, so it cannot mutate a record), `failed`, `timeout`,
`memory_limit`, or `no_entry`. A mod that did not run proves nothing about what it would have
changed, and `missing_api` lists the interfaces it wanted that the sandbox does not implement.
Lua outcomes deliberately do not fail the build — a framework that cannot run under a stubbed
API says nothing about gameplay records — so the counts in the build summary are the signal.

## Find records

Discover the table before guessing its name:

```sql
SELECT record_type, table_name
FROM data_types
WHERE lower(record_type) LIKE '%progress%';
```

Search both internal names and structured data:

```sql
SELECT record_name, source, load_order, entry_path
FROM type_class_description
WHERE lower(record_name) LIKE '%snowlight%'
   OR lower(data) LIKE '%snowlight%';
```

For player-facing text, also search localization:

```sql
SELECT record_name AS handle,
       json_extract(data, '$.text') AS text,
       source,
       load_order
FROM type_localization
WHERE lower(json_extract(data, '$.text')) LIKE '%potent robe%';
```

Use `resources` to locate unsupported runtime files without opening every archive:

```sql
SELECT source, load_order, pak_path, entry_path, kind, status, error
FROM resources
WHERE lower(entry_path) LIKE '%bootstrapserver.lua%';
```

## Resolve load order and inheritance

Never select an arbitrary duplicate. Inspect every definition in ascending load order:

```sql
SELECT record_name, source, source_kind, load_order, using_record, data
FROM type_armor
WHERE record_name = 'MAG_CQCaster_GainArcaneChargeOnDamaged_Robe'
ORDER BY load_order, id;
```

A later definition overrides an earlier definition. Stats records may inherit through
`using_record`. A definition that uses its own name is a patch layer: merge it over the previous
definition of that name, not over itself and not as an inheritance cycle. For a normal
`using_record`, recursively resolve the latest prior definition of that parent, then merge the
child fields over it.

For questions that only need the final unmerged definition, rank rows explicitly:

```sql
WITH ranked AS (
  SELECT *,
         row_number() OVER (
           PARTITION BY record_name
           ORDER BY load_order DESC, id DESC
         ) AS rank
  FROM type_passive_data
  WHERE load_order IS NOT NULL
)
SELECT * FROM ranked WHERE rank = 1;
```

Do not use this shortcut when `using_record` contributes fields needed by the answer.

### `MergedInto` — lists are a UNION, not an override

**A third resolution rule, and the one most likely to produce a false negative.**
Selector lists (`PassiveList`, `SpellList`) may carry a `MergedInto` guid, which adds that
list's entries to the target list instead of replacing it. A list's effective contents are
therefore **the load-order winner plus every list declaring `MergedInto` at its UUID**:

```sql
-- contributors to a list, which resolving by UUID alone never shows
SELECT record_name, record_uuid, source, load_order,
       json_extract(data, '$.attributes.Passives.value') AS passives
FROM type_passive_list
WHERE json_extract(data, '$.attributes.MergedInto.value')
      = '333fb1b0-9398-4ca8-953e-6c0f9a59bbed';
```

**887 of 2,379 spell lists and 20 of 173 passive lists use it**, so reading only the winner
loses roughly a third of the game's list content. This is not a corner case: the Warlock
level-2 invocation list has three contributors (Expansion 13-20, Mizoras Rewards, Pact of the
Shroud), and `ElementalBlast` reaches the Eldritch Adept feat's picker **only** through
Mizoras Rewards' merge. Resolving that list to its winner alone reports, wrongly, that no feat
can select Elemental Blast.

A negative claim about list membership is unproven until the merge contributors are checked.
`lsdb.py grants --expand` and `lsdb_index.py` both resolve the union; raw SQL does not.

## Mining interactions — the synergy index

For "what interacts with what" rather than "what does X do", build the sidecar index. It parses
the functor DSL out of every effective record into a graph, plus a player-reachability closure,
and never touches the compiled DB (which the compiler replaces atomically):

```bash
S=plugins/listo-build/skills/listo-build/scripts
$S/lsdb_index.py                      # ~5 s -> /tmp/listonomicon-synergy.sqlite
```

`lsdb.py` refuses to answer from an index built against a different compiled DB. Then:

```bash
$S/lsdb.py applies BLINDED            # every reachable applier, with save/at-will/clamp tags
$S/lsdb.py reads BLINDED              # everything gated on the condition
$S/lsdb.py chain BLINDED --hops 2     # applier -> reader -> what that applies
$S/lsdb.py origins Glaring_Frost      # which class/subclass/feat/race/item grants it, and at what level
$S/lsdb.py motif broker               # status one feature applies and another reads
$S/lsdb.py motif per-instance         # damage-type payoff x multi-instance delivery
$S/lsdb.py motif no-save              # chance 100 with no saving throw in the gate
$S/lsdb.py motif on-crit              # on-critical payoffs beside crit-threshold sources
$S/lsdb.py motif handoff --status BLINDED   # CROSS-BODY: one character supplies a
                                      #   condition, the other cashes it in
```

### Single-body or cross-body

The graph is **body-agnostic**: an edge joins two features and says nothing about which
character carries them. Three additions make the pair question answerable.

**Side.** Every `APPLIES` edge records who the status lands on — `self`, `ally`, `enemy` or
`unknown` — read from predicate **polarity**, not presence: `not Enemy()` means an ALLY (it is
how `Target_Bless` is written) and `not Ally()` means an enemy. Matching the bare predicate name
gets both backwards and mislabelled 1,326 edges when it was tried.

**Role.** `status_role` says what a condition does to whoever carries it: `atk` grants advantage
to anyone attacking the bearer (BLINDED), `weak` degrades the bearer (POISONED, FRIGHTENED),
`buff` improves it (BLESS, Battlemind Link). Heuristic, from the sign of its own boosts.

**Level budget.** `origin_meta` maps subclass to parent class, so a pair of features is costed:
same class -> the deeper level, different classes -> the sum, feats and races -> free. At or under
twenty it fits **one body**; above it the combination exists **only across two characters**.
"1 body" means they *could* share a character, not that they should.

`motif handoff` walks four channels on that basis, and is generic over any condition:

```text
BLINDED [atk+weak] <- Glaring_Frost [subclass:Snowlight@3] enemy-side at-will save:Constitution
     ATTACKER   Advantage(AttackTarget) — both characters' attack rolls; crit rate follows
     on-crit    ClarifiedMortality  [subclass:GreatOldOne@1]   1 body (4 lv)
     WEAKEN     Disadvantage(AttackRoll) — both characters benefit, no reader needed
     reads      Snowblindness       [subclass:Snowlight@11]    1 body (17 lv)
POISONED [weak] <- Projectile_RayOfSickness_2 [feat:SYR_ShadowTouched] enemy-side at-will
     WEAKEN     Disadvantage(AttackRoll); Disadvantage(AllAbilities)
HASTE [buff] <- Target_Haste [subclass:AbjurationSchool@1] ally-side at-will
     ALLY BUFF  AC(2); ActionResource(ActionPoint,1,0) — lands on the PARTNER
```

Naming a status with `--status` lifts the specificity filter, because a generic spell such as
Bless is reachable from everywhere and would otherwise be hidden.

**What is asserted rather than read.** Only the crit arithmetic under ATTACKER — advantage rolls
twice, so it widens threshold coverage. Say so in any answer that leans on it.

**Where the data runs out.** An aura's targeting is often absent from the record, so the side
comes back `unknown` and the channel prints as `ALLY BUFF?`. Battlemind Link and Emboldening Bond
both land there: they really do buff an ally, and the record does not say so. Confirm those in
game rather than quoting the index.

### Owner-scoped chains are not cross-body

`motif self-chain` is the counterpart to `handoff`, and the distinction is a correctness one.
`HasDamageDoneForType` asks what **this** creature just dealt, inside its own `On*` context, so a
damage-type payoff and the thing dealing the damage must sit on the **same character**:

```text
Radiant  Glaring_Frost [subclass:Snowlight@3] OnDamage
                  <- FriarRetribution [subclass:Friar@3] OnAttacked   SAME BODY ok (6 lv)
```

For this class of chain a level cost above twenty is **IMPOSSIBLE**, not "two bodies" — 46 pairs
in the field are exactly that, and reporting them as a cross-body option would be a false
positive. `per-instance` shares the constraint and now says so; it also filters on
multi-instance delivery, so single-hit feeders such as a retaliation only appear under
`self-chain`.

Rule of thumb: a payoff keyed on **what the owner did** (`HasDamageDoneForType`, `IsCriticalHit`
in an `On*` context) is owner-scoped. A payoff keyed on **the target's state** (a status on the
enemy, `Advantage(AttackTarget)`) is target-side and crosses bodies freely.

Results are ranked by **specificity** (`origin_count`): a record reachable from 40 sources is a
generic spell-list entry, one reachable from 1–2 is a signature feature, and `--max-sources`
bounds it. Items are excluded unless `--include-items`; `--kinds` narrows to
`subclass,class,feat,race`.

**What the index cannot see.** It is a stats-layer graph: runtime Lua, Osiris, level placement
and engine rules (crit doubling, what a condition does beyond its own `Boosts`) are absent, and
`unparsed` holds anything the parser refused — check it before trusting a negative. Origins show
one representative source per record; `lsdb.py origins` lists them all. The closure follows
progressions, feats, races, equip fields, `MergedInto` unions, `SpellContainerID` membership,
`ApplyStatus`, `UnlockSpell` and granted passives — a record it calls unreachable is a claim
about those routes only, not proof a player cannot obtain it.

## Common mechanics queries

### What a subclass grants at a level

1. Find its `ClassDescription` and `ProgressionTableUUID`:

```sql
SELECT record_name,
       json_extract(data, '$.attributes.ProgressionTableUUID.value') AS table_uuid,
       source,
       load_order
FROM type_class_description
WHERE lower(record_name) = 'snowlight'
ORDER BY load_order DESC;
```

2. Follow that UUID into `Progression`:

```sql
WITH subclass AS (
  SELECT json_extract(data, '$.attributes.ProgressionTableUUID.value') AS table_uuid
  FROM type_class_description
  WHERE lower(record_name) = 'snowlight'
  ORDER BY load_order DESC
  LIMIT 1
)
SELECT p.record_name,
       json_extract(p.data, '$.attributes.Level.value') AS level,
       json_extract(p.data, '$.attributes.PassivesAdded.value') AS passives,
       json_extract(p.data, '$.attributes.AddSpells.value') AS spells,
       json_extract(p.data, '$.attributes.Selectors.value') AS selectors,
       p.source,
       p.load_order
FROM type_progression AS p, subclass AS s
WHERE json_extract(p.data, '$.attributes.TableUUID.value') = s.table_uuid
  AND json_extract(p.data, '$.attributes.Level.value') = '3'
ORDER BY p.load_order DESC;
```

3. Follow every passive, selector, spell-list UUID, and spell into its own table. Read
   `Boosts`, `Conditions`, `StatsFunctors`, costs, cooldowns, saves, statuses, and localization;
   the progression row is only the outer grant.

### What a passive or status does

```sql
SELECT record_name,
       json_extract(data, '$.Boosts') AS boosts,
       json_extract(data, '$.Conditions') AS conditions,
       json_extract(data, '$.StatsFunctorContext') AS context,
       json_extract(data, '$.StatsFunctors') AS functors,
       source,
       load_order
FROM type_passive_data
WHERE record_name IN ('Snowborne', 'Glaring_Frost')
ORDER BY record_name, load_order;
```

For statuses, query `type_status_data` and inspect `Boosts`, `StackId`, status type, duration,
conditions, and functors. Follow referenced spells/passives/statuses until the actual effect is
accounted for.

### Items and robes

Start in the Stats tables, not by searching display names alone:

```sql
SELECT record_name,
       using_record,
       json_extract(data, '$.RootTemplate') AS root_template,
       json_extract(data, '$.Rarity') AS rarity,
       json_extract(data, '$.Boosts') AS boosts,
       json_extract(data, '$.PassivesOnEquip') AS passives,
       source,
       load_order
FROM type_armor
WHERE lower(record_name) LIKE '%robe%'
ORDER BY record_name, load_order;
```

Then join `RootTemplate` by `record_uuid = RootTemplate`, read its `DisplayName` and `Description`
handles, and resolve those handles in `type_localization`. Expand `PassivesOnEquip`,
`StatusOnEquip`, unlocked spells, and every referenced status before comparing items. Internal
names containing `Robe` include cosmetics and non-caster equipment; verify equipment slot,
`ArmorType`, proficiency requirements, and effective inherited fields.

### Resource amount and recharge

Query `type_action_resource_definition`, then follow referenced passives and statuses:

```sql
SELECT record_name,
       json_extract(data, '$.attributes.ReplenishType.value') AS replenishes,
       data,
       source,
       load_order
FROM type_action_resource_definition
WHERE lower(record_name) LIKE '%resource%';
```

## When PAK access is still justified

Do not read PAKs merely because a question is consequential; the database already preserves the
installed primary records and provenance. Read a PAK only when one of these is true:

- `resources.status = 'error'` for the relevant entry.
- The mechanic lives in Osiris story, level placement, or another payload indexed but not
  extracted into a `type_*` table. Script Extender Lua no longer qualifies: it is extracted into
  `type_script_extender_lua` (with `raw` holding the source) and executed, so read it from there.
- A whole-pack absence claim needs searching payloads the compiler only indexed.
- The compiler output is internally inconsistent and the source entry is needed to diagnose it.

Use `resources.pak_path` and `resources.entry_path` to target that one entry. Do not scan guessed
archives by filename. The minimal fallback reader is:

```bash
python3 plugins/listo-build/skills/listo-build/scripts/lspk.py \
  "/mnt/mercury/Games/Listonomicon/mods/<mod directory>/<file.pak>" \
  "<entry/path/inside/pak>"
```

Do not extract archives into the repository.

## Reporting a mechanics answer

For consequential claims, report:

- the database build/profile from `metadata`;
- `source`, `source_kind`, `load_order`, `pak_path`, and `entry_path`;
- relevant internal record names and decisive JSON fields/functors;
- how duplicate definitions and `using_record` inheritance were resolved;
- any inference connecting those fields to the conclusion;
- the exact fallback source when the database could not answer it.

Keep “not found” narrower than “does not exist.” State which `type_*` tables, identifiers, and
indexed resource classes were searched. A negative claim about runtime grants is not proven by
searching structured Stats/LSX tables alone.
