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

It requires BG3 Forge 0.2.0. From the repository root:

```bash
python3 -m venv /tmp/listo-db-venv
/tmp/listo-db-venv/bin/python -m pip install "bg3forge[zstd]==0.2.0"
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
- The mechanic lives in Lua, Osiris story, level placement, or another payload indexed but not
  extracted into a `type_*` table.
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
