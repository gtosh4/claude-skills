#!/usr/bin/env python3
"""lsdb — compact query CLI for the compiled Listonomicon character database.

Encodes the evidence semantics from plugins/listo-build/AGENTS.md so routine
questions cost one short command instead of a chain of raw SQL round trips:

  lsdb.py tables [PATTERN]            which type_* table holds a record type
  lsdb.py find TERM [--deep]          where a name (or payload, --deep) appears
  lsdb.py get NAME [--all] [--full]   the EFFECTIVE record: load-order winner,
                                      same-name patch layers merged, the
                                      using_record chain resolved, LSX
                                      attributes flattened, handles localized
  lsdb.py loc TERM                    localization: handle -> text, text -> handle
  lsdb.py grants NAME [--level N] [--expand]
                                      ClassDescription -> ProgressionTableUUID ->
                                      per-level grants, optionally expanding
                                      passives and spell lists one line each

Output is deliberately terse (values truncated at --trunc, default 160 chars;
--full disables).

It also imports as a library, which is the supported way to reuse the load-order,
patch-layer and using_record semantics from a notebook or REPL instead of
hand-rolling SQL:

    import sys; sys.path.insert(0, "plugins/listo-build/skills/listo-build/scripts")
    import lsdb

    db  = lsdb.connect()                    # or lsdb.connect(path)
    rec = db.record("MAG_CELESTIAL_HASTE")  # table auto-discovered
    rec["Boosts"]                           # inherited from HASTE, still present
    rec.origin("Boosts")                    # 'HASTE' — which parent supplied it
    rec.load_order, rec.source, rec.chain
    db.sql("SELECT ... FROM type_armor WHERE ...")   # plain dicts, for the rest

Prefer `db.record(...)` over `json_extract(data,'$.Field')`. A field supplied by a
`using` parent is simply absent from the child row, and a patch layer whose `using`
names itself will silently truncate a hand-rolled inheritance walk — the failure
that made `MAG_CELESTIAL_HASTE` read as having no Boosts at all when it inherits
the whole Haste package.
"""

import argparse
import os
import json
import re
import sqlite3
import sys
from typing import NamedTuple

DB_DEFAULT = "/tmp/listonomicon-character-data.sqlite"

# Fields worth reading first, in the order a mechanics question wants them.
LEAD = [
    "Level", "SpellType", "DamageType", "Damage", "UseCosts", "Cooldown",
    "Boosts", "BoostConditions", "Conditions", "StatsFunctorContext",
    "StatsFunctors", "SpellRoll", "SpellSuccess", "SpellFail",
    "SpellProperties", "AmountOfTargets", "TargetRadius", "AreaRadius",
    "TooltipDamageList", "Properties", "StackId", "StackType",
    "StatusPropertyFlags", "TickType", "OnApplyFunctors", "OnRemoveFunctors",
    "AuraRadius", "AuraStatuses", "PassivesAdded", "PassivesRemoved",
    "AddSpells", "Selectors", "ProgressionTableUUID", "ReplenishType",
    "RootTemplate", "Rarity", "PassivesOnEquip", "StatusOnEquip", "Slot",
    "ArmorType", "Spells", "DisplayName", "Description",
]
LEAD_RANK = {k: i for i, k in enumerate(LEAD)}

HANDLE_RE = re.compile(r"^h[0-9a-g]{30,};?\d*$")
UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def clip(s, n):
    s = str(s).replace("\n", " ")
    return s if n <= 0 or len(s) <= n else s[: n - 1] + "…"


def parse_data(row):
    """data JSON -> flat field dict. LSX rows flatten attributes; stats are flat."""
    try:
        d = json.loads(row["data"]) if row["data"] else {}
    except (TypeError, ValueError):
        return {}
    if isinstance(d, dict) and isinstance(d.get("attributes"), dict):
        out = {}
        for k, v in d["attributes"].items():
            out[k] = v.get("value") if isinstance(v, dict) else v
        kids = d.get("children")
        if kids:
            out["children"] = f"{len(kids)} child node(s)"
        return out
    return d if isinstance(d, dict) else {}


class Record(NamedTuple):
    """One record's EFFECTIVE fields, with provenance and per-field origin.

    `rec.get("Boosts")` reads a field; `rec.origin("Boosts")` names the `using`
    parent that supplied it, or None when this record supplies it directly — the
    distinction raw `json_extract` on the child row cannot make. `rec.data()`
    flattens to plain {field: value}.
    """

    name: str
    table: str
    fields: dict            # {field: (value, origin_or_None)}
    row: sqlite3.Row
    layers: list
    chain: list

    def get(self, field, default=None):
        got = self.fields.get(field)
        return default if got is None else got[0]

    def origin(self, field):
        got = self.fields.get(field)
        return None if got is None else got[1]

    def data(self):
        """Plain {field: value}, origins dropped. (`_asdict` is the tuple's own.)"""
        return {k: v for k, (v, _o) in self.fields.items()}

    @property
    def source(self):
        return self.row["source"]

    @property
    def load_order(self):
        return self.row["load_order"]

    @property
    def entry_path(self):
        return self.row["entry_path"]

    @property
    def raw(self):
        """The original Stats block, where the table carries one."""
        return self.row["raw"] if "raw" in self.row.keys() else None

    def __repr__(self):
        # The generated repr would dump `fields` and the whole sqlite3.Row, which
        # is unusable in a notebook. Everything below is recoverable via the attrs.
        return (f"<Record {self.table}::{self.name} load={self.load_order} "
                f"fields={len(self.fields)} using={'->'.join(self.chain) or '—'}>")


class Db:
    def __init__(self, path):
        self.cx = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        self.cx.row_factory = sqlite3.Row
        self._loc = {}

    def type_tables(self, pattern=None):
        q = "SELECT record_type, table_name FROM data_types ORDER BY record_type"
        rows = self.cx.execute(q).fetchall()
        if pattern:
            p = pattern.lower()
            rows = [r for r in rows
                    if p in r["record_type"].lower() or p in r["table_name"].lower()]
        return rows

    def rows_named(self, table, name):
        """All definitions of NAME in TABLE, ascending effective order."""
        return self.cx.execute(
            f"SELECT * FROM {table} WHERE lower(record_name)=? "
            f"ORDER BY COALESCE(load_order,-1), id", (name.lower(),)).fetchall()

    def effective(self, table, name, _seen=None):
        """The effective definition of NAME per AGENTS.md load-order semantics.

        Returns (fields, final_row, layers, chain) or None.
        - same-name `using` = patch layer: merged over the previous definition
        - other later definitions replace wholesale
        - a foreign `using_record` parent is resolved recursively and the child
          merges over it; `chain` lists parent names; inherited fields are
          tagged in fields as (value, origin)
        """
        rows = self.rows_named(table, name)
        if not rows:
            return None
        cur, layers = None, []
        for r in rows:
            f = parse_data(r)
            u = (r["using_record"] or "").lower()
            if cur is not None and u == (r["record_name"] or "").lower():
                cur.update(f)                       # patch layer
                layers.append(r)
            else:
                cur, layers = dict(f), [r]          # fresh definition
        final = layers[-1]
        fields = {k: (v, None) for k, v in cur.items()}
        chain = []
        parent = (layers[0]["using_record"] or "")
        seen = _seen or {name.lower()}
        if parent and parent.lower() not in seen and len(seen) < 8:
            seen.add(parent.lower())
            up = self.effective(table, parent, seen)
            if up:
                pf, _pr, _pl, pchain = up
                chain = [parent] + pchain
                merged = {k: (v, o or parent) for k, (v, o) in pf.items()}
                merged.update(fields)
                fields = merged
        return fields, final, layers, chain

    def localize(self, handle):
        h = handle.split(";")[0]
        if h in self._loc:
            return self._loc[h]
        r = self.cx.execute(
            "SELECT json_extract(data,'$.text') t FROM type_localization "
            "WHERE record_name=? ORDER BY COALESCE(load_order,-1) DESC, id DESC "
            "LIMIT 1", (h,)).fetchone()
        self._loc[h] = r["t"] if r else None
        return self._loc[h]

    # ── library surface ─────────────────────────────────────────────────────

    def tables_with(self, name):
        """Every type_* table holding a record of this exact name."""
        return [r["table_name"] for r in self.type_tables()
                if self.rows_named(r["table_name"], name)]

    def record(self, name, table=None):
        """The EFFECTIVE Record, or None. Table auto-discovered when omitted.

        Prefer this over `json_extract(data,'$.Field')`: it merges same-name patch
        layers and resolves the `using` chain, so a field the parent supplies is
        present and attributed rather than silently missing.

        Name matching is case-insensitive, so a name can land in more than one
        table — the Mesmerist pattern of passive `BoldStare_X` beside status
        `BOLDSTARE_X` is the common case. That is ambiguous, not a tie to break,
        so it raises: pass `table=` or use `records()`. Returning either one
        silently is how a status' Boosts get reported as absent.
        """
        if table is None:
            found = self.tables_with(name)
            if len(found) > 1:
                raise LookupError(
                    f"{name!r} exists in {len(found)} tables: {', '.join(found)}. "
                    f"Pass table= to choose, or use records() for all of them.")
            if not found:
                return None
            table = found[0]
        hit = self.effective(table, name)
        if not hit:
            return None
        fields, final, layers, chain = hit
        return Record(final["record_name"], table, fields, final, layers, chain)

    def records(self, name):
        """Every table's effective Record for this name, in type_tables order."""
        out = []
        for t in self.tables_with(name):
            hit = self.effective(t, name)
            if hit:
                fields, final, layers, chain = hit
                out.append(Record(final["record_name"], t, fields, final, layers, chain))
        return out

    def sql(self, query, *params):
        """Raw query -> list of plain dicts, for what the helpers do not cover."""
        return [dict(r) for r in self.cx.execute(query, params).fetchall()]


def connect(path=None):
    """Open the compiled database read-only for library use.

        import lsdb
        db  = lsdb.connect()
        rec = db.record("MAG_CELESTIAL_HASTE")
        rec.get("Boosts"), rec.origin("Boosts")   # inherited value, and 'HASTE'
    """
    return Db(path or os.environ.get("LSDB_DB") or DB_DEFAULT)


def provenance(row):
    lo = row["load_order"]
    return f"{row['source']} · load {lo if lo is not None else '—'} · {row['entry_path']}"


def print_effective(db, table, name, args):
    hit = db.effective(table, name)
    if not hit:
        return False
    fields, final, layers, chain = hit
    print(f"== {table} :: {final['record_name']}")
    print(f"   {provenance(final)}")
    if len(layers) > 1:
        print(f"   patch layers: {len(layers)} "
              f"({', '.join(l['source'] for l in layers)})")
    if chain:
        print(f"   using: {' -> '.join(chain)}")
    n = 0 if args.full else args.trunc
    for k in sorted(fields, key=lambda k: (LEAD_RANK.get(k, 999), k)):
        v, origin = fields[k]
        if v in (None, ""):
            continue
        line = f"   {k} = {clip(v, n)}"
        if isinstance(v, str) and HANDLE_RE.match(v.strip()):
            txt = db.localize(v.strip())
            if txt:
                line += f'   "{clip(txt, 90)}"'
        if origin:
            line += f"   <- {origin}"
        print(line)
    return True


def cmd_tables(db, args):
    for r in db.type_tables(args.pattern):
        print(f"{r['record_type']:32} {r['table_name']}")


def cmd_find(db, args):
    term = f"%{args.term.lower()}%"
    tables = [args.table] if args.table else [r["table_name"] for r in db.type_tables()]
    skip_deep = {"type_localization", "type_voice_bark_data"}
    total = 0
    for t in tables:
        cond, params = "lower(record_name) LIKE ?", [term]
        if args.deep and (t not in skip_deep or args.table):
            cond, params = f"({cond} OR lower(data) LIKE ?)", [term, term]
        try:
            rows = db.cx.execute(
                f"SELECT record_name, COUNT(*) n, MAX(COALESCE(load_order,-1)) lo "
                f"FROM {t} WHERE {cond} GROUP BY lower(record_name) "
                f"ORDER BY 3 DESC LIMIT ?", params + [args.limit]).fetchall()
        except sqlite3.Error:
            continue
        for r in rows:
            w = db.cx.execute(
                f"SELECT source FROM {t} WHERE lower(record_name)=? "
                f"ORDER BY COALESCE(load_order,-1) DESC, id DESC LIMIT 1",
                ((r["record_name"] or "").lower(),)).fetchone()
            marks = f" ×{r['n']}" if r["n"] > 1 else ""
            print(f"{t:28} {r['record_name']:44} {w['source']} · load {r['lo']}{marks}")
            total += 1
    if not total:
        print(f"no record_name match for {args.term!r}"
              + ("" if args.deep else " (try --deep for payload search, or `loc`)"))


def cmd_get(db, args):
    tables = [args.table] if args.table else db.tables_with(args.name)
    if not tables:
        print(f"{args.name!r} not found by exact name in any type table — try `find`")
        sys.exit(1)
    for t in tables:
        if args.all:
            rows = db.rows_named(t, args.name)
            print(f"== {t} :: {rows[-1]['record_name']} — all definitions, effective order")
            for r in rows:
                u = f" using {r['using_record']}" if r["using_record"] else ""
                print(f"   load {str(r['load_order'] or '—'):>4} · {r['source']}{u} · {r['entry_path']}")
        else:
            print_effective(db, t, args.name, args)


def cmd_loc(db, args):
    if HANDLE_RE.match(args.term.strip()):
        txt = db.localize(args.term.strip())
        print(txt if txt is not None else "handle not found")
        return
    rows = db.cx.execute(
        "SELECT record_name h, json_extract(data,'$.text') t, source, "
        "MAX(COALESCE(load_order,-1)) lo FROM type_localization "
        "WHERE lower(json_extract(data,'$.text')) LIKE ? "
        "GROUP BY record_name ORDER BY lo DESC LIMIT ?",
        (f"%{args.term.lower()}%", args.limit)).fetchall()
    for r in rows:
        print(f"{r['h']}  {clip(r['t'], args.trunc)}  ({r['source']})")
    if not rows:
        print(f"no localization text matches {args.term!r}")


def _expand_passive(db, name, trunc):
    hit = db.effective("type_passive_data", name)
    if not hit:
        return f"      {name}: (no passive_data record)"
    fields = {k: v for k, (v, _o) in hit[0].items()}
    bits = [f"{k}={fields[k]}" for k in
            ("Boosts", "Conditions", "StatsFunctorContext", "StatsFunctors")
            if fields.get(k)]
    return f"      {name}: {clip('; '.join(bits) or '(no functors)', trunc)}"


def _list_contents(db, table, field, uuid, seen=None):
    """A list's effective contents: the load-order winner UNION every list that
    declares `MergedInto` at it.

    `MergedInto` is a union, not an override — 887 of 2,379 spell lists use it, so
    reading only the winner silently loses a third of the game's list content.
    """
    seen = seen if seen is not None else set()
    if uuid in seen:
        return [], 0
    seen.add(uuid)
    out, contributors = [], 0
    r = db.cx.execute(
        f"SELECT data FROM {table} WHERE record_uuid=? "
        f"ORDER BY COALESCE(load_order,-1) DESC, id DESC LIMIT 1", (uuid,)).fetchone()
    if r:
        out += [x.strip() for x in re.split(r"[;,]", str(parse_data(r).get(field) or ""))
                if x.strip()]
    for c in db.cx.execute(
            f"SELECT DISTINCT record_uuid FROM {table} "
            f"WHERE json_extract(data,'$.attributes.MergedInto.value')=?", (uuid,)):
        sub, subc = _list_contents(db, table, field, c["record_uuid"], seen)
        out += sub
        contributors += 1 + subc
    return out, contributors


def _expand_spell_list(db, uuid, trunc):
    names, merged = _list_contents(db, "type_spell_list", "Spells", uuid)
    if not names:
        pnames, pmerged = _list_contents(db, "type_passive_list", "Passives", uuid)
        if pnames:
            names, merged = pnames, pmerged
        else:
            return f"      list {uuid}: (not found)"
    tail = f"  (+{merged} merged list(s))" if merged else ""
    return f"      list {uuid[:8]}…: {clip(','.join(dict.fromkeys(names)), trunc)}{tail}"


def cmd_grants(db, args):
    hit = db.effective("type_class_description", args.name)
    if not hit:
        print(f"no ClassDescription named {args.name!r} — try `find {args.name}`")
        sys.exit(1)
    fields, final, _l, _c = hit
    uuid = (fields.get("ProgressionTableUUID") or (None,))[0]
    print(f"== {final['record_name']} — {provenance(final)}")
    if not uuid:
        print("   no ProgressionTableUUID on the effective record")
        sys.exit(1)
    rows = db.cx.execute(
        "SELECT * FROM type_progression "
        "WHERE json_extract(data,'$.attributes.TableUUID.value')=? "
        "ORDER BY COALESCE(load_order,-1), id", (uuid,)).fetchall()
    latest = {}
    for r in rows:                      # per-uuid override: last wins
        latest[r["record_uuid"] or r["id"]] = r
    by_level = {}
    for r in latest.values():
        f = parse_data(r)
        lvl = int(f.get("Level") or 0)
        if args.level and lvl != args.level:
            continue
        by_level.setdefault(lvl, []).append((f, r))
    n = 0 if args.full else args.trunc
    for lvl in sorted(by_level):
        for f, r in by_level[lvl]:
            mc = " [multiclass]" if str(f.get("IsMulticlass")) == "true" else ""
            print(f"-- level {lvl}{mc}  ({r['source']} · load {r['load_order']})")
            for k in ("PassivesAdded", "PassivesRemoved", "Boosts",
                      "AddSpells", "Selectors", "AllowImprovement"):
                if f.get(k):
                    print(f"   {k} = {clip(f[k], n)}")
            if args.expand:
                for p in re.split(r"[;,]", f.get("PassivesAdded") or ""):
                    if p.strip():
                        print(_expand_passive(db, p.strip(), n))
                blob = (f.get("AddSpells") or "") + ";" + (f.get("Selectors") or "")
                for u in UUID_RE.findall(blob):
                    print(_expand_spell_list(db, u, n))
    if not by_level:
        print("   no progression rows"
              + (f" at level {args.level}" if args.level else ""))


# ── synergy sidecar (built by lsdb_index.py) ────────────────────────────────
SIDE_DEFAULT = "/tmp/listonomicon-synergy.sqlite"

# Which origin kinds a synergy question is about. Items are excluded by default:
# 3,307 of them dominate every join and the question is usually about the body.
DEFAULT_KINDS = ("subclass", "class", "feat", "race")


def open_side(args):
    """Open the sidecar, refusing a stale index rather than answering from it."""
    try:
        sx = sqlite3.connect(f"file:{args.side}?mode=ro", uri=True)
        sx.row_factory = sqlite3.Row
        meta = {r["key"]: r["value"] for r in sx.execute("SELECT key, value FROM meta")}
    except sqlite3.Error:
        sys.exit(f"no synergy index at {args.side} — build it with:\n"
                 f"  lsdb_index.py --db {args.db} --out {args.side}")
    try:
        st = os.stat(args.db)
        stale = (meta.get("source_size") != str(st.st_size)
                 or meta.get("source_mtime") != str(int(st.st_mtime)))
    except OSError:
        stale = True
    if stale and not args.stale_ok:
        sys.exit(f"synergy index is STALE: built {meta.get('built_at')} against a "
                 f"different {args.db}.\nRe-run lsdb_index.py, or pass --stale-ok "
                 f"to query it anyway.")
    # One representative origin per record: the most specific wins. A record can be
    # reachable several ways; `origins` keeps them all and this view picks one.
    sx.executescript("""
      CREATE TEMP VIEW best_origin AS
      SELECT tbl, nm, kind, label, level FROM (
        SELECT tbl, lower(name) nm, kind, label, level,
               row_number() OVER (PARTITION BY tbl, lower(name) ORDER BY
                 CASE kind WHEN 'subclass' THEN 1 WHEN 'class' THEN 2
                           WHEN 'feat' THEN 3 WHEN 'race' THEN 4 ELSE 5 END,
                 label) rn
        FROM origins) WHERE rn = 1;
    """)
    return sx, meta


def kind_filter(args):
    kinds = tuple(k.strip() for k in (args.kinds or ",".join(DEFAULT_KINDS)).split(","))
    if getattr(args, "include_items", False):
        kinds += ("item",)
    return kinds


def orig_str(row, prefix=""):
    k, l, lv = row[prefix + "kind"], row[prefix + "label"], row[prefix + "level"]
    return f"[{k}:{l}" + (f"@{lv}" if lv else "") + "]"


LEVEL_CAP = 20


def parent_classes(sx):
    return {r["label"]: r["parent_class"]
            for r in sx.execute("SELECT label, parent_class FROM origin_meta")}


def budget(pc, a, b):
    """Can these two origins sit on ONE twenty-level body?

    Feats and races cost no class levels (a feat is one of seven slots, a race is
    free), so they never force a split. Two features of the same SUBCLASS cost the
    deeper of the two; of different classes, the sum. Above twenty levels the
    combination exists only across two characters — which is precisely the
    question a pair sheet asks and a single-chassis ledger cannot.

    Two *different subclasses of the same class* are mutually exclusive: BG3
    grants one subclass per class, so no number of levels buys both Oath of
    Conquest and Oathbreaker. Costing that as `max()` — as though they were
    siblings on one body — reports an impossible combination as the cheapest
    kind of single body, which is the most misleading verdict this function
    can return.

    Returns (levels, verdict) where verdict is "one", "two" or "exclusive".
    """
    def cost(kind, label, lv):
        if kind in ("feat", "race", "item"):
            return None, None, 0
        try:
            n = int(lv)
        except (TypeError, ValueError):
            n = 1
        parent = pc.get(label, label)
        return parent, (label if kind == "subclass" else None), n

    ca, sa, na = cost(*a)
    cb, sb, nb = cost(*b)
    if ca is None or cb is None:
        return na + nb, "one" if na + nb <= LEVEL_CAP else "two"
    if ca != cb:
        total = na + nb
        return total, "one" if total <= LEVEL_CAP else "two"
    if sa and sb and sa != sb:
        return max(na, nb), "exclusive"
    total = max(na, nb)
    return total, "one" if total <= LEVEL_CAP else "two"


def cmd_applies(db, args):
    sx, _m = open_side(args)
    ph = ",".join("?" * len(kind_filter(args)))
    rows = sx.execute(f"""
      SELECT e.src, e.tbl, e.chance, e.save, e.gated, e.target, e.detail,
             o.kind, o.label, o.level, a.at_will, a.clamped, a.context, a.cooldown
      FROM edges e
      JOIN best_origin o ON o.tbl = e.tbl AND o.nm = lower(e.src)
      LEFT JOIN annot a ON a.tbl = e.tbl AND lower(a.name) = lower(e.src)
      WHERE e.kind = ? AND upper(e.dst) = upper(?) AND o.kind IN ({ph})
      ORDER BY a.at_will DESC, e.save IS NOT NULL, o.kind, e.src
      LIMIT ?""", ["REMOVES" if args.removes else "APPLIES", args.status]
                     + list(kind_filter(args)) + [args.limit]).fetchall()
    for r in rows:
        tags = []
        if r["save"]:
            tags.append(f"save:{r['save']}")
        elif r["chance"] == 100:
            tags.append("NO-SAVE")
        if r["at_will"]:
            tags.append("at-will")
        if r["clamped"]:
            tags.append("clamped")
        if r["cooldown"]:
            tags.append(r["cooldown"])
        if r["context"]:
            tags.append(r["context"])
        if r["target"]:
            tags.append(f"->{r['target']}")
        print(f"{r['src']:38} {orig_str(r):34} {' '.join(tags)}")
    if not rows:
        print(f"nothing reachable applies {args.status!r} "
              f"(kinds: {','.join(kind_filter(args))})")


def status_tokens(sx, status):
    """The query token plus every status group it belongs to, widest last.

    Applying BLINDED also puts the target in `SG_Blinded` and `SG_Condition`, so
    a reader of either fires. Querying the bare status alone understates its
    consumers badly — which is how "only one thing in the install reads Blind"
    survived as long as it did.
    """
    rows = sx.execute(
        "SELECT e.dst grp, (SELECT count(*) FROM edges g "
        "        WHERE g.kind='INGROUP' AND upper(g.dst)=upper(e.dst)) members "
        "FROM edges e WHERE e.kind='INGROUP' AND upper(e.src)=upper(?) "
        "GROUP BY upper(e.dst) ORDER BY members", (status,)).fetchall()
    return [(status, None)] + [(r["grp"], r["members"]) for r in rows]


def cmd_reads(db, args):
    sx, _m = open_side(args)
    kinds = list(kind_filter(args))
    ph = ",".join("?" * len(kinds))
    shown = 0
    for token, members in status_tokens(sx, args.status):
        rows = sx.execute(f"""
          SELECT e.src, e.tbl, e.target, e.field, o.kind, o.label, o.level,
                 a.at_will, a.context
          FROM edges e
          JOIN best_origin o ON o.tbl = e.tbl AND o.nm = lower(e.src)
          LEFT JOIN annot a ON a.tbl = e.tbl AND lower(a.name) = lower(e.src)
          WHERE e.kind = 'READS' AND upper(e.dst) = upper(?) AND o.kind IN ({ph})
          ORDER BY e.target = 'neg', o.kind, e.src LIMIT ?""",
          [token] + kinds + [args.limit]).fetchall()
        if not rows:
            continue
        if members is not None:
            print(f"-- via group {token} ({members} member statuses)")
        for r in rows:
            pol = "requires" if r["target"] == "pos" else "requires NOT"
            print(f"{r['src']:38} {orig_str(r):34} {pol} · {r['field']}"
                  + (f" · {r['context']}" if r["context"] else ""))
        shown += len(rows)
    if not shown:
        print(f"nothing reachable reads {args.status!r} or any group it belongs to")


def cmd_origins(db, args):
    sx, _m = open_side(args)
    rows = sx.execute(
        "SELECT tbl, kind, label, level FROM origins WHERE lower(name)=lower(?) "
        "ORDER BY CASE kind WHEN 'subclass' THEN 1 WHEN 'class' THEN 2 "
        "WHEN 'feat' THEN 3 WHEN 'race' THEN 4 ELSE 5 END, label LIMIT ?",
        (args.name, args.limit)).fetchall()
    for r in rows:
        print(f"{r['kind']:9} {r['label']:32} {r['tbl']}"
              + (f" @level {r['level']}" if r["level"] else ""))
    if not rows:
        print(f"{args.name!r} is not reachable from any player class, subclass, "
              f"feat, race or item — monster/NPC/cut content, or an evidence gap")


def cmd_chain(db, args):
    """Walk the graph outward from a status: who applies it, who reads it, and
    what those readers apply in turn — the shape a synergy loop actually has."""
    sx, _m = open_side(args)
    kinds = kind_filter(args)
    ph = ",".join("?" * len(kinds))
    # Status spelling is not consistent in the installed content: `SG_Blinded`
    # and `SG_BLINDED` both occur. Comparisons therefore case-fold, while the
    # stored token stays verbatim so provenance survives.
    seen, frontier = set(), [args.status]
    for hop in range(args.hops):
        nxt = []
        for st in frontier:
            if st.upper() in seen:
                continue
            seen.add(st.upper())
            ap = sx.execute(f"""
              SELECT e.src, o.kind, o.label, o.level, a.at_will, e.save, e.chance
              FROM edges e JOIN best_origin o ON o.tbl=e.tbl AND o.nm=lower(e.src)
              LEFT JOIN annot a ON a.tbl=e.tbl AND lower(a.name)=lower(e.src)
              WHERE e.kind='APPLIES' AND upper(e.dst)=upper(?) AND o.kind IN ({ph})
              ORDER BY a.at_will DESC LIMIT 4""", [st] + list(kinds)).fetchall()
            rd = sx.execute(f"""
              SELECT e.src, e.tbl, o.kind, o.label, o.level
              FROM edges e JOIN best_origin o ON o.tbl=e.tbl AND o.nm=lower(e.src)
              WHERE e.kind='READS' AND upper(e.dst)=upper(?) AND e.target='pos'
                AND o.kind IN ({ph}) LIMIT 4""", [st] + list(kinds)).fetchall()
            print(f"{'  ' * hop}{st}")
            for r in ap:
                gate = f"save:{r['save']}" if r["save"] else (
                    "NO-SAVE" if r["chance"] == 100 else "")
                print(f"{'  ' * hop}  <- applied by {r['src']} {orig_str(r)} "
                      f"{'at-will ' if r['at_will'] else ''}{gate}")
            for r in rd:
                print(f"{'  ' * hop}  -> read by    {r['src']} {orig_str(r)}")
                for nx in sx.execute(
                        "SELECT DISTINCT dst FROM edges WHERE kind='APPLIES' "
                        "AND tbl=? AND lower(src)=lower(?) LIMIT 3",
                        (r["tbl"], r["src"])).fetchall():
                    nxt.append(nx["dst"])
        frontier = nxt


MOTIFS = ("broker", "per-instance", "self-chain", "no-save", "on-crit", "handoff")


def cmd_motif(db, args):
    sx, _m = open_side(args)
    kinds = kind_filter(args)
    ph = ",".join("?" * len(kinds))
    n = args.limit

    if args.name == "broker":
        # A status one feature applies and a DIFFERENT feature reads: the shape of
        # every "my condition turns on your payoff" pairing.
        #
        # Two things make the output readable rather than a dump:
        #   SPECIFICITY — `origin_count` says how many sources reach a record. A
        #     pair of signature features (n=1 each) is the interesting case;
        #     ranking by name put ANIMATEDEAD_ZONE first and buried everything.
        #   PAIR DEDUPE — one row per (applier, reader), not per status. Bardic
        #     Inspiration alone has six status variants that are the same finding.
        # The specificity filter also runs BEFORE the join, in the CTEs, which is
        # what keeps this a few seconds instead of a minute.
        rows = sx.execute(f"""
          WITH ap AS (
            SELECT e.dst, e.src, e.tbl, e.save, e.chance FROM edges e
            JOIN origin_count c ON c.tbl=e.tbl AND c.name=lower(e.src) AND c.n<=?
            WHERE e.kind='APPLIES'),
          rd AS (
            SELECT e.dst, e.src, e.tbl FROM edges e
            JOIN origin_count c ON c.tbl=e.tbl AND c.name=lower(e.src) AND c.n<=?
            WHERE e.kind='READS' AND e.target='pos')
          SELECT group_concat(DISTINCT ap.dst) statuses, COUNT(DISTINCT ap.dst) nst,
                 ap.src applier, oa.kind akind, oa.label alabel, oa.level alevel,
                 rd.src reader, ob.kind rkind, ob.label rlabel, ob.level rlevel,
                 MAX(aa.at_will) at_will, MIN(ap.save IS NULL) nosave,
                 ca.n an, cb.n rn
          FROM ap
          JOIN rd ON rd.dst=ap.dst AND lower(rd.src)<>lower(ap.src)
          JOIN best_origin oa ON oa.tbl=ap.tbl AND oa.nm=lower(ap.src)
          JOIN best_origin ob ON ob.tbl=rd.tbl AND ob.nm=lower(rd.src)
          JOIN origin_count ca ON ca.tbl=ap.tbl AND ca.name=lower(ap.src)
          JOIN origin_count cb ON cb.tbl=rd.tbl AND cb.name=lower(rd.src)
          LEFT JOIN annot aa ON aa.tbl=ap.tbl AND lower(aa.name)=lower(ap.src)
          WHERE oa.kind IN ({ph}) AND ob.kind IN ({ph}) AND oa.label <> ob.label
          GROUP BY lower(ap.src), lower(rd.src)
          ORDER BY (ca.n + cb.n), MAX(aa.at_will) DESC LIMIT ?""",
          [args.max_sources, args.max_sources] + list(kinds) * 2 + [n]).fetchall()
        for r in rows:
            st = clip(r["statuses"], 40) + (f" (+{r['nst'] - 1} variants)"
                                            if r["nst"] > 1 else "")
            tags = ("at-will " if r["at_will"] else "") + ("NO-SAVE" if r["nosave"] else "save")
            print(f"{r['applier']:32} {orig_str(r,'a'):28} -> {r['reader']:32} "
                  f"{orig_str(r,'r'):28} {tags:14} {st}")

    elif args.name == "per-instance":
        # A damage-type predicate (payoff per damage instance) crossed with a
        # multi-instance source of that type. Winter Spirit x Elemental Blast.
        rows = sx.execute(f"""
          SELECT p.dst type, p.src payoff, op.kind pkind, op.label plabel,
                 op.level plevel, d.src delivery, od.kind dkind, od.label dlabel,
                 od.level dlevel, ad.instances
          FROM edges p
          JOIN best_origin op ON op.tbl=p.tbl AND op.nm=lower(p.src)
          JOIN edges d ON d.kind='DEALS' AND d.dst=p.dst AND lower(d.src)<>lower(p.src)
          JOIN best_origin od ON od.tbl=d.tbl AND od.nm=lower(d.src)
          JOIN annot ad ON ad.tbl=d.tbl AND lower(ad.name)=lower(d.src) AND ad.multi=1
          WHERE p.kind='PREDICATE' AND op.kind IN ({ph}) AND od.kind IN ({ph})
            AND op.label <> od.label
          GROUP BY p.dst, lower(p.src), lower(d.src)
          ORDER BY (SELECT n FROM origin_count WHERE tbl=p.tbl AND name=lower(p.src))
                 + (SELECT n FROM origin_count WHERE tbl=d.tbl AND name=lower(d.src)),
                 p.dst LIMIT ?""", list(kinds) * 2 + [n]).fetchall()
        print("# SAME BODY REQUIRED: a damage-type predicate fires in its OWNER's "
              "On* context,\n#   so the payoff and the delivery must be the same "
              "character. See `self-chain`\n#   for the feasibility check.")
        for r in rows:
            print(f"{r['type']:10} payoff {r['payoff']:28} {orig_str(r,'p'):30} "
                  f"x {r['delivery']:26} {orig_str(r,'d'):26} "
                  f"instances={clip(r['instances'], 28)}")

    elif args.name == "self-chain":
        # SAME-BODY BY CONSTRUCTION, and that is the point of having it separate.
        #
        # `HasDamageDoneForType` asks what THIS creature just dealt, inside its own
        # `On*` context, so a damage-type payoff and the thing dealing the damage
        # must sit on the SAME character. For this motif a level cost above twenty
        # is therefore not "two bodies" — it is IMPOSSIBLE, and reporting it as a
        # cross-body option would be a false positive.
        #
        # Unlike `per-instance` there is no multi-instance filter: a single-hit
        # retaliation like Friar's Retribution feeds a predicate exactly as well as
        # an eight-beam cantrip, it just feeds it once.
        pc = parent_classes(sx)
        want = (args.type or "").capitalize()
        rows = sx.execute(f"""
          SELECT p.dst type, p.src payoff, op.kind pkind, op.label plabel,
                 op.level plevel, d.src source, od.kind dkind, od.label dlabel,
                 od.level dlevel, ap.context pctx, ad.context dctx,
                 cp.n pn, cd.n dn
          FROM edges p
          JOIN best_origin op ON op.tbl=p.tbl AND op.nm=lower(p.src)
          JOIN origin_count cp ON cp.tbl=p.tbl AND cp.name=lower(p.src) AND cp.n<=?
          LEFT JOIN annot ap ON ap.tbl=p.tbl AND lower(ap.name)=lower(p.src)
          JOIN edges d ON d.kind='DEALS' AND d.dst=p.dst
                      AND lower(d.src)<>lower(p.src)
          JOIN best_origin od ON od.tbl=d.tbl AND od.nm=lower(d.src)
          JOIN origin_count cd ON cd.tbl=d.tbl AND cd.name=lower(d.src) AND cd.n<=?
          LEFT JOIN annot ad ON ad.tbl=d.tbl AND lower(ad.name)=lower(d.src)
          WHERE p.kind='PREDICATE' AND op.kind IN ({ph}) AND od.kind IN ({ph})
            AND (?='' OR p.dst=?) AND ap.context LIKE 'On%'
          GROUP BY p.dst, lower(p.src), lower(d.src)
          ORDER BY (cp.n + cd.n), p.dst LIMIT ?""",
          [args.max_sources, args.max_sources] + list(kinds) * 2
          + [want, want, n]).fetchall()
        if not rows:
            print("no same-body damage-type chain found"
                  + (f" for {want}" if want else ""))
        for r in rows:
            total, verdict = budget(pc, (r["pkind"], r["plabel"], r["plevel"]),
                                    (r["dkind"], r["dlabel"], r["dlevel"]))
            fit = {"one": f"SAME BODY ok ({total} lv)",
                   "two": f"IMPOSSIBLE ({total} lv > {LEVEL_CAP})",
                   "exclusive": "IMPOSSIBLE (one subclass per class)"}[verdict]
            print(f"{r['type']:9} {r['payoff']:26} {orig_str(r,'p'):26} "
                  f"{(r['pctx'] or '?'):11} <- {r['source']:26} "
                  f"{orig_str(r,'d'):26} {(r['dctx'] or 'spell/item'):11} {fit}")

    elif args.name == "no-save":
        # chance=100 with no SavingThrow anywhere in the gate: control that cannot
        # be resisted, which is worth more than its damage ever is.
        rows = sx.execute(f"""
          SELECT e.src, e.dst, e.target, o.kind, o.label, o.level, a.at_will,
                 a.clamped, a.context, e.detail
          FROM edges e
          JOIN best_origin o ON o.tbl=e.tbl AND o.nm=lower(e.src)
          LEFT JOIN annot a ON a.tbl=e.tbl AND lower(a.name)=lower(e.src)
          WHERE e.kind='APPLIES' AND e.chance=100 AND e.save IS NULL
            AND (e.target IS NULL OR e.target='SWAP') AND o.kind IN ({ph})
            AND e.dst IN (SELECT dst FROM edges WHERE kind='READS')
          GROUP BY lower(e.src), e.dst
          ORDER BY a.at_will DESC,
                 (SELECT n FROM origin_count WHERE tbl=e.tbl AND name=lower(e.src)),
                 e.src LIMIT ?""",
          list(kinds) + [n]).fetchall()
        for r in rows:
            print(f"{r['dst']:26} {r['src']:30} {orig_str(r):32} "
                  f"{'at-will ' if r['at_will'] else ''}"
                  f"{'clamped ' if r['clamped'] else ''}{r['context'] or ''}")

    elif args.name == "handoff":
        # THE CROSS-BODY CHANNELS, which is a different question from `broker`.
        #
        # `broker` finds feature-to-feature status handoffs and says nothing about
        # which character carries which end. This walks the four ways one character
        # hands value to the other, using the `side` of the APPLIES edge (who the
        # status lands on) and `status_role` (what it does to whoever carries it):
        #
        #   ATTACKER   condition on the ENEMY granting Advantage(AttackTarget) —
        #              every attacker collects, so accuracy and crit payoffs follow
        #   WEAKEN     condition on the ENEMY degrading its own rolls or actions —
        #              both characters benefit passively, no reader required
        #   READ       some other feature is gated on the condition being present
        #   ALLY       buff applied to an ALLY: the partner is the beneficiary
        #              (657 ally-targeted spells and 334 ally auras use this)
        #
        # Every step is an extracted edge except the crit arithmetic under
        # ATTACKER, which is the ENGINE fact that advantage rolls twice. `budget`
        # then says whether the two ends fit one twenty-level body or need two.
        pc = parent_classes(sx)
        want = args.status or ""
        # Naming a status is a targeted question. The specificity filter exists to
        # rank a broad sweep; applied here it would hide Bless, which is generic
        # precisely because every support class gets it.
        maxsrc = 9999 if want else args.max_sources
        conds = sx.execute(f"""
          SELECT ap.dst status, ap.src applier, ap.side, ap.save, ap.chance,
                 oa.kind akind, oa.label alabel, oa.level alevel,
                 aa.at_will, ca.n an,
                 COALESCE(sr.atk,0) atk, COALESCE(sr.weak,0) weak,
                 COALESCE(sr.buff,0) buff
          FROM edges ap
          JOIN best_origin oa ON oa.tbl=ap.tbl AND oa.nm=lower(ap.src)
          JOIN origin_count ca ON ca.tbl=ap.tbl AND ca.name=lower(ap.src) AND ca.n<=?
          LEFT JOIN annot aa ON aa.tbl=ap.tbl AND lower(aa.name)=lower(ap.src)
          LEFT JOIN status_role sr ON upper(sr.name)=upper(ap.dst)
          WHERE ap.kind='APPLIES' AND ap.side IN ('enemy','ally','unknown')
            AND oa.kind IN ({ph}) AND (?='' OR upper(ap.dst)=upper(?))
            AND (COALESCE(sr.atk,0)+COALESCE(sr.weak,0)+COALESCE(sr.buff,0)) > 0
          GROUP BY ap.dst, lower(ap.src)
          ORDER BY ca.n, aa.at_will DESC, ap.dst LIMIT ?""",
          [maxsrc] + list(kinds) + [want, want, n]).fetchall()
        if not conds:
            print(f"no cross-body channel found"
                  + (f" for {want}" if want else "") + f" (kinds: {','.join(kinds)})")

        def consumers(kind_sql, role, lim=4):
            return [dict(r, role=role) for r in sx.execute(f"""
              SELECT DISTINCT e.src, o.kind, o.label, o.level, c.n
              FROM edges e
              JOIN best_origin o ON o.tbl=e.tbl AND o.nm=lower(e.src)
              JOIN origin_count c ON c.tbl=e.tbl AND c.name=lower(e.src) AND c.n<=?
              WHERE {kind_sql} AND o.kind IN ({ph})
              ORDER BY c.n LIMIT ?""",
              [args.max_sources] + list(kinds) + [lim]).fetchall()]


        for c in conds:
            gate = (f"save:{c['save']}" if c["save"] else
                    "NO-SAVE" if c["chance"] == 100 else "gated")
            tags = "+".join(t for t, on in (("atk", c["atk"]), ("weak", c["weak"]),
                                            ("buff", c["buff"])) if on)
            print(f"{c['status']} [{tags}] <- {c['applier']} {orig_str(c,'a')} "
                  f"{c['side']}-side {'at-will ' if c['at_will'] else ''}{gate}")

            def emit(rows, label):
                for p in rows:
                    total, verdict = budget(pc, (c["akind"], c["alabel"], c["alevel"]),
                                            (p["kind"], p["label"], p["level"]))
                    # "exclusive" is a genuine cross-body REQUIREMENT, not a
                    # failure: the two ends cannot share a body at any level, so
                    # the pairing is the only way to have both.
                    fit = {"one": f"1 body ({total} lv)",
                           "two": f"2 BODIES ({total} lv)",
                           "exclusive": "2 BODIES (one subclass per class)"}[verdict]
                    lb = f"[{p['kind']}:{p['label']}" + (f"@{p['level']}" if p["level"] else "") + "]"
                    print(f"     {label:14} {p['src']:32} {lb:34} {fit}")

            if c["atk"] and c["side"] in ("enemy", "unknown"):
                print("     ATTACKER       Advantage(AttackTarget) — both characters' "
                      "attack rolls; crit rate follows (engine fact)")
                emit(consumers("e.kind='FLAG' AND e.dst LIKE 'IsCritical%'",
                               "on-crit"), "on-crit")
                emit(consumers("e.kind='MODIFIES' AND "
                               "e.dst='ReduceCriticalAttackThreshold'", "crit-thr"),
                     "crit-thr")
            if c["weak"] and c["side"] in ("enemy", "unknown"):
                degr = sx.execute(
                    "SELECT DISTINCT dst, detail FROM edges WHERE tbl='type_status_data'"
                    " AND src=? AND kind='MODIFIES' LIMIT 4", (c["status"],)).fetchall()
                print("     WEAKEN         " + "; ".join(
                    f"{d['dst']}({clip(d['detail'], 24)})" for d in degr)
                    + " — both characters benefit, no reader needed")
            if c["buff"] and c["side"] in ("ally", "unknown"):
                boosts = sx.execute(
                    "SELECT DISTINCT dst, detail FROM edges WHERE tbl='type_status_data'"
                    " AND src=? AND kind IN ('MODIFIES','RESIST') LIMIT 4",
                    (c["status"],)).fetchall()
                # An aura's targeting often is not stated in the record, so the
                # side comes back `unknown`. Say so rather than claiming the
                # partner gets it: Battlemind Link and Emboldening Bond both land
                # here, and both really do buff an ally, but the DATA does not say.
                sure = c["side"] == "ally"
                print(f"     {'ALLY BUFF' if sure else 'ALLY BUFF?':14} " + "; ".join(
                    f"{b['dst']}({clip(b['detail'], 24)})" for b in boosts)
                    + (" — lands on the PARTNER" if sure else
                       " — buff, targeting UNRESOLVED in the record; confirm it reaches an ally"))
            emit(consumers(f"e.kind='READS' AND e.target='pos' AND e.dst="
                           f"'{c['status'].replace(chr(39), '')}'", "reads"), "reads")

    elif args.name == "on-crit":
        # Not a pairwise join: any threshold source combines with any on-crit
        # payoff, so the useful answer is the two lists side by side.
        print("== fires on a critical hit")
        for r in sx.execute(f"""
          SELECT DISTINCT e.src, o.kind, o.label, o.level, a.context
          FROM edges e JOIN best_origin o ON o.tbl=e.tbl AND o.nm=lower(e.src)
          LEFT JOIN annot a ON a.tbl=e.tbl AND lower(a.name)=lower(e.src)
          WHERE e.kind='FLAG' AND (e.dst LIKE 'IsCritical%' OR e.dst='DamageFlags.Critical')
            AND o.kind IN ({ph}) ORDER BY o.kind, e.src LIMIT ?""",
          list(kinds) + [n]).fetchall():
            print(f"   {r['src']:34} {orig_str(r):32} {r['context'] or ''}")
        print("== lowers the critical threshold")
        for r in sx.execute(f"""
          SELECT DISTINCT e.src, e.detail, o.kind, o.label, o.level
          FROM edges e JOIN best_origin o ON o.tbl=e.tbl AND o.nm=lower(e.src)
          WHERE e.kind='MODIFIES' AND e.dst='ReduceCriticalAttackThreshold'
            AND o.kind IN ({ph}) ORDER BY o.kind, e.src LIMIT ?""",
          list(kinds) + [n]).fetchall():
            print(f"   {r['src']:34} {orig_str(r):32} -{r['detail']}")


def cmd_feats(db, args):
    """Effective feat levels, with runtime overrides applied.

    Feat cadence is not a static fact in this install: a Script Extender mod
    rewrites `Progression.AllowImprovement` when the game loads. The compiler
    runs those mods in a sandbox and records what they wrote, so this reports
    the effective cadence and names the mod responsible — reading the LSX
    tables alone gives the wrong answer.
    """
    try:
        rows = db.cx.execute(
            "SELECT class_name, level, grants_feat, static_grants_feat, "
            "       changed_at_runtime, overridden_by "
            "FROM class_feat_levels "
            "WHERE level BETWEEN 2 AND ? AND (? = '' OR lower(class_name) = lower(?)) "
            "ORDER BY class_name, level",
            (args.max_level, args.name or "", args.name or ""),
        ).fetchall()
    except sqlite3.OperationalError:
        sys.exit(
            "this database has no class_feat_levels view — it predates runtime-override\n"
            "support. Rebuild it with compile_mod_data.py."
        )
    if not rows:
        target = f" for {args.name!r}" if args.name else ""
        print(f"no progression rows{target}")
        return

    by_class = {}
    for row in rows:
        by_class.setdefault(row["class_name"], []).append(row)

    for class_name, entries in by_class.items():
        effective = [str(r["level"]) for r in entries if r["grants_feat"]]
        static = [str(r["level"]) for r in entries if r["static_grants_feat"]]
        moved = [r for r in entries if r["changed_at_runtime"]]
        source = next(
            (r["overridden_by"] for r in moved if r["overridden_by"]), None
        )
        print(f"{class_name:22} {','.join(effective) or '(none)'}")
        if args.static or moved:
            print(f"{'':22} static LSX: {','.join(static) or '(none)'}")
            if source:
                print(f"{'':22} rewritten at runtime by {source}")


def main():
    ap = argparse.ArgumentParser(prog="lsdb.py", description=__doc__.splitlines()[0])
    ap.add_argument("--db", default=DB_DEFAULT)
    ap.add_argument("--trunc", type=int, default=160, help="value truncation (0 = off)")
    ap.add_argument("--full", action="store_true", help="never truncate values")
    ap.add_argument("--side", default=SIDE_DEFAULT,
                    help="synergy index built by lsdb_index.py")
    ap.add_argument("--stale-ok", action="store_true",
                    help="query a synergy index built against a different DB")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("tables", help="list record type -> table")
    p.add_argument("pattern", nargs="?")

    p = sub.add_parser("find", help="where does a name appear")
    p.add_argument("term")
    p.add_argument("--table")
    p.add_argument("--deep", action="store_true", help="also search data payloads")
    p.add_argument("--limit", type=int, default=8, help="rows per table")

    p = sub.add_parser("get", help="effective record, inheritance resolved")
    p.add_argument("name")
    p.add_argument("--table")
    p.add_argument("--all", action="store_true", help="audit every definition instead")

    p = sub.add_parser("loc", help="localization handle <-> text")
    p.add_argument("term")
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("grants", help="what a class/subclass grants per level")
    p.add_argument("name")
    p.add_argument("--level", type=int)
    p.add_argument("--expand", action="store_true",
                   help="one-line expansion of passives and spell lists")

    def synargs(p, status=True):
        p.add_argument("status" if status else "name")
        p.add_argument("--kinds", help=f"origin kinds, default {','.join(DEFAULT_KINDS)}")
        p.add_argument("--include-items", action="store_true")
        p.add_argument("--max-sources", type=int, default=3,
                       help="skip records reachable from more than N sources — "
                            "high counts mean generic spell-list entries, not "
                            "signature features")
        p.add_argument("--limit", type=int, default=20)
        return p

    synargs(sub.add_parser("applies", help="what reachable thing applies a status")) \
        .add_argument("--removes", action="store_true", help="removals instead")
    synargs(sub.add_parser("reads", help="what reachable thing reads a status"))
    synargs(sub.add_parser("chain", help="walk applier/reader hops from a status")) \
        .add_argument("--hops", type=int, default=2)

    p = sub.add_parser("origins", help="how a record is reachable by a player")
    p.add_argument("name")
    p.add_argument("--limit", type=int, default=20)

    p = synargs(sub.add_parser("motif", help=f"canned synergy joins: {', '.join(MOTIFS)}"),
                status=False)
    p.add_argument("--status", default="",
                   help="handoff: restrict to one condition, e.g. --status BLINDED")
    p.add_argument("--type", default="",
                   help="self-chain: restrict to one damage type, e.g. --type Radiant")

    p = sub.add_parser("feats", help="effective feat levels, runtime overrides applied")
    p.add_argument("name", nargs="?", help="class name; omit for every class")
    p.add_argument("--max-level", type=int, default=20)
    p.add_argument("--static", action="store_true",
                   help="show the static LSX cadence beside the effective one")

    args = ap.parse_args()
    if args.cmd == "motif" and args.name not in MOTIFS:
        sys.exit(f"unknown motif {args.name!r} — expected one of {', '.join(MOTIFS)}")
    db = Db(args.db)
    {"tables": cmd_tables, "find": cmd_find, "get": cmd_get, "loc": cmd_loc,
     "grants": cmd_grants, "applies": cmd_applies, "reads": cmd_reads,
     "chain": cmd_chain, "origins": cmd_origins, "feats": cmd_feats,
     "motif": cmd_motif}[args.cmd](db, args)


if __name__ == "__main__":
    main()
