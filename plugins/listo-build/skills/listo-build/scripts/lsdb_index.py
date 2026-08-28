#!/usr/bin/env python3
"""lsdb_index — build the synergy sidecar for the compiled Listonomicon database.

Parses the Stats/LSX functor DSL out of every LOAD-ORDER-EFFECTIVE record into a
queryable graph, so "which pairs of things reference each other" becomes a join
instead of thousands of LIKE scans and JSON reads.

Writes a SEPARATE database (default /tmp/listonomicon-synergy.sqlite) and never
mutates the compiled one: AGENTS.md's compiler replaces that file atomically, so
anything written into it is lost on the next build. The sidecar records the source
build stamp and `lsdb` refuses to answer from a stale index.

    lsdb_index.py [--db COMPILED] [--out SIDECAR] [--verbose]

Tables written:
  effective  one row per (table, record_name): the winner, patch layers merged,
             `using_record` chain resolved, curated fields as JSON
  edges      typed references: APPLIES/REMOVES/READS/DEALS/PREDICATE/MODIFIES/
             IMMUNITY/RESIST/UNLOCKS/GRANTS/LIST
  annot      per-record cost and clamp facts: trigger context, cooldown, stack id,
             instance count, self-clamped, at-will
  origins    player-reachability closure: record -> class/subclass/race/feat/item
  unparsed   fail-loud bucket for functors the parser did not understand

Stats-layer only. Runtime Lua, Osiris and engine rules (crit doubling, what BLINDED
does to a roll beyond its own Boosts) are not in these records; see AGENTS.md.
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import time

DB_DEFAULT = "/tmp/listonomicon-character-data.sqlite"
OUT_DEFAULT = "/tmp/listonomicon-synergy.sqlite"

# Tables carrying mechanics worth parsing into edges.
EDGE_TABLES = ["type_passive_data", "type_status_data", "type_spell_data",
               "type_interrupt_data", "type_armor", "type_weapon", "type_object"]
# Extra tables needed to seed and expand player reachability.
SEED_TABLES = ["type_class_description", "type_race", "type_feat",
               "type_progression", "type_passive_list", "type_spell_list"]

# Only these fields are carried into `effective`, which bounds memory and disk:
# the whole payload is already in the compiled DB and `lsdb get` reads it there.
FUNCTOR_FIELDS = {
    "StatsFunctors", "OnApplyFunctors", "OnRemoveFunctors", "OnTickFunctors",
    "SpellSuccess", "SpellFail", "SpellProperties", "Success", "Failure",
    "AuraStatuses", "StatusOnEquip", "ExtraProperties",
}
COND_FIELDS = {
    "Conditions", "BoostConditions", "TargetConditions", "RemoveConditions",
    "SpellRoll", "ItemConditions", "InterruptConditions",
}
BOOST_FIELDS = {"Boosts", "PassivesOnEquip", "Passives", "PassivesAdded"}
LIST_FIELDS = {"Spells", "AddSpells", "Selectors", "PassivesRemoved"}
META_FIELDS = {
    "StatsFunctorContext", "TickType", "Cooldown", "StackId", "StackType",
    "UseCosts", "AmountOfTargets", "StatusPropertyFlags", "Level", "DamageType",
    "SpellContainerID", "ProgressionTableUUID", "Name", "ParentGuid", "UUID",
    "TableUUID", "IsMulticlass", "DisplayName", "RootTemplate", "Slot",
    "MergedInto", "StatusGroups",
}
KEEP = FUNCTOR_FIELDS | COND_FIELDS | BOOST_FIELDS | LIST_FIELDS | META_FIELDS

# ApplyStatus(SELF, X, …) — only SELF/SWAP occur in practice, but the full
# vocabulary is cheap to accept and misreading a prefix as a status name would
# silently invent records.
TARGETS = {"SELF", "SWAP", "CAUSE", "TARGET", "OWNER", "SOURCE", "OBSERVER",
           "OBSERVER_OBSERVER", "ENTITY"}

DAMAGE_TYPES = {"Acid", "Bludgeoning", "Cold", "Fire", "Force", "Lightning",
                "Necrotic", "Piercing", "Poison", "Psychic", "Radiant",
                "Slashing", "Thunder"}

# Boost calls that change how a roll or a resource resolves. Kept explicit: an
# unrecognised boost goes to `unparsed` rather than being dropped.
MODIFY_BOOSTS = {
    "Advantage", "Disadvantage", "RollBonus", "AC", "ACOverrideFormula",
    "Initiative", "DamageBonus", "DamageReduction", "CharacterWeaponDamage",
    "ReduceCriticalAttackThreshold", "CriticalHit", "IgnoreResistance",
    "TemporaryHP", "ActionResource", "ActionResourceMultiplier", "Ability",
    "AbilityOverrideMinimum", "ProficiencyBonus", "ProficiencyBonusOverride",
    "SpellSaveDC", "UnlockSpellVariant", "MinimumRollResult", "JumpMaxDistance",
    "IncreaseMaxHP", "WeaponDamage", "WeaponAttackRollAbilityOverride",
    "MonkWeaponDamageDiceOverride", "Attribute", "Lootable", "DarkvisionRange",
    "DarkvisionRangeMin", "DarkvisionRangeOverride", "Detach", "GameplayLight",
    "HalveWeaponDamage", "IgnorePointBlankDisadvantage", "IgnoreLeaveAttackRange",
    "IgnoreSurfaceCover", "Invisibility", "Invulnerable", "Reroll",
    "SavingThrow", "AbilityFailedSavingThrow", "SightRangeOverride", "SpellResistance", "UnarmedMagicalProperty",
    "WeaponEnchantment", "WeaponProperty", "CanSeeThrough", "CanShootThrough",
    "CanWalkThrough", "ConcentrationIgnoreDamage", "CriticalHitExtraDice",
    "DodgeAttackRoll", "FallDamageMultiplier", "Movement", "MovementSpeedLimit",
    "ObjectSize", "ObjectSizeOverride", "ScaleMultiplier", "SourceAdvantageOnAttack",
    "SourceAllyAdvantageOnAttack", "SummonLifelinkModifier", "UseBoosts",
    "VoicebarkAttitude", "PhysicalForceRangeBonus", "SpellDamageTypeOverride",
}
SKIP_BOOSTS = {"UnlockSpell", "StatusImmunity", "Resistance", "Proficiency",
               "ProficiencyBonus", "Tag", "CannotHarmCauseEntity", "Attribute"}


# ── paren-aware parsing ──────────────────────────────────────────────────────
def split_top(s, sep=";"):
    """Split on `sep` at bracket/paren depth 0, respecting quotes.

    Brackets count as depth: `CastOffhand[A;B]` is ONE item, and splitting inside
    it strands `B)]` fragments that no parser can read.
    """
    out, depth, buf, q = [], 0, [], None
    for ch in s:
        if q:
            buf.append(ch)
            if ch == q:
                q = None
            continue
        if ch in "'\"":
            q = ch
            buf.append(ch)
            continue
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        if ch == sep and depth == 0:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    out.append("".join(buf))
    return [x.strip() for x in out if x.strip()]


def unwrap_if(s):
    """`IF(cond):body` (possibly nested) -> (list of conditions, body)."""
    conds = []
    while True:
        m = re.match(r"^\s*IF\s*\(", s)
        if not m:
            return conds, s.strip()
        depth, i = 0, m.end() - 1
        for j in range(i, len(s)):
            if s[j] == "(":
                depth += 1
            elif s[j] == ")":
                depth -= 1
                if depth == 0:
                    conds.append(s[i + 1:j])
                    rest = s[j + 1:].lstrip()
                    s = rest[1:] if rest.startswith(":") else rest
                    break
        else:
            return conds, s.strip()


def parse_call(s):
    """`Name(a,b,c)` -> (Name, [args]); bare `Name` -> (Name, [])."""
    m = re.match(r"^([A-Za-z_][\w]*)\s*\((.*)\)\s*$", s, re.S)
    if not m:
        return (s.strip(), []) if re.match(r"^[A-Za-z_][\w]*$", s.strip()) else (None, [])
    return m.group(1), split_top(m.group(2), ",")


def strip_q(s):
    return s.strip().strip("'\"").strip()


def split_names(text):
    """Split a name list on BOTH `;` and `,`.

    These fields mix separators — `PassivesAdded` is
    `"Snowborne; Glaring_Frost; XR_ArmorSetup"` while a spell list's `Spells`
    uses `;` and some selectors use `,`. Splitting on one only is a SILENT
    failure: it yields a single bogus mega-name that joins to nothing.
    """
    out = []
    for part in split_top(text or "", ";"):
        out.extend(strip_q(x) for x in split_top(part, ","))
    return [x for x in out if x]


def normalize_functor(item):
    """Flatten one functor item into parseable bodies.

    Two shapes the raw DSL uses that a bare `Name(args)` match cannot see:
      `CastOffhand[GROUND:DealDamage(...)]`  bracket group, possibly multi-item
      `AI_ONLY:ApplyStatus(...)`             ALLCAPS context prefix
    `IF(...)` is untouched: its prefix is followed by `(`, never `:`.
    """
    item = item.strip()
    m = re.match(r"^(\w+)\[(.*)\]$", item, re.S)
    if m:
        out = []
        for inner in split_top(m.group(2)):
            out.extend(normalize_functor(inner))
        return out
    m = re.match(r"^([A-Za-z][A-Za-z0-9_]*)\s*:\s*(.+)$", item, re.S)
    if m:
        return normalize_functor(m.group(2))
    return [item] if item else []


def find_predicates(text):
    """Damage-type predicates in a condition string -> set of type names."""
    out = set()
    for m in re.finditer(r"HasDamageDoneForType\s*\(\s*DamageType\.(\w+)", text):
        out.add(m.group(1))
    for m in re.finditer(r"MainDamageTypeIs\s*\(\s*DamageType\.(\w+)", text):
        out.add(m.group(1))
    for m in re.finditer(r"SpellDamageTypeIs\s*\(\s*(?:DamageType\.)?(\w+)", text):
        out.add(m.group(1))
    for m in re.finditer(r"IsDamageType(\w+)\s*\(", text):
        out.add(m.group(1))
    return {t for t in out if t in DAMAGE_TYPES}


def find_status_reads(text):
    """(status, negated) pairs read by a condition string.

    Identifiers are mixed case: status *groups* are `SG_Incapacitated`, not
    `SG_INCAPACITATED`, so an upper-only character class silently truncates
    every group read to `SG_I` and makes group consumers unfindable.

    `HasAnyStatus({'A','B'}, ...)` reads each name in its first braced set;
    matching only the single-status predicates misses it entirely.
    """
    out = []
    for m in re.finditer(
        r"(not\s+)?(?:HasStatus|StatusId)\s*\(\s*['\"]?([A-Za-z0-9_]+)", text
    ):
        out.append((m.group(2), bool(m.group(1))))
    for m in re.finditer(r"(not\s+)?HasAnyStatus\s*\(\s*\{([^}]*)\}", text):
        for nm in re.findall(r"['\"]([A-Za-z0-9_]+)['\"]", m.group(2)):
            out.append((nm, bool(m.group(1))))
    return out


def save_ability(text):
    m = re.search(r"SavingThrow\s*\(\s*Ability\.(\w+)", text)
    return m.group(1) if m else None


# Condition predicates worth joining on. A whitelist, because `Is\w+(` also
# matches dozens of one-off scenario checks that would bury the useful ones.
FLAGS = {
    "IsCriticalHit", "IsCritical", "IsMeleeAttack", "IsRangedAttack",
    "IsMeleeWeaponAttack", "IsRangedWeaponAttack", "IsMeleeSpellAttack",
    "IsRangedSpellAttack", "IsWeaponAttack", "IsUnarmedAttack", "IsAttack",
    "IsSpell", "IsCantrip", "IsHit", "IsMiss", "IsConcentrating",
    "IsMovementSpell", "IsThrownWeaponAttack", "IsSavingThrow",
}


def find_flags(text):
    """Whitelisted condition flags, plus HasDamageEffectFlag(DamageFlags.X)."""
    out = {m.group(1) for m in re.finditer(r"\b(Is[A-Z]\w+)\s*\(", text)} & FLAGS
    for m in re.finditer(r"HasDamageEffectFlag\s*\(\s*DamageFlags\.(\w+)", text):
        out.add(f"DamageFlags.{m.group(1)}")
    return out


# ── effective-record resolution (same semantics as lsdb.get) ─────────────────
def parse_data(blob):
    try:
        d = json.loads(blob) if blob else {}
    except (TypeError, ValueError):
        return {}
    if isinstance(d, dict) and isinstance(d.get("attributes"), dict):
        return {k: (v.get("value") if isinstance(v, dict) else v)
                for k, v in d["attributes"].items()}
    return d if isinstance(d, dict) else {}


# Identity differs by record family, and getting it wrong corrupts data silently.
# Stats records (passive/status/spell/armor…) are identified by NAME, and a later
# same-name definition patches or replaces them. LSX nodes below are identified by
# UUID: a Progression table has one row per level all sharing the class name, so
# name-keying would merge twenty levels into one record.
UUID_KEYED = {"type_progression", "type_spell_list", "type_passive_list",
              "type_class_description", "type_race", "type_feat"}


def build_uuid_keyed(cx, table, verbose=False):
    """Latest definition per record_uuid. No patch/parent semantics: LSX nodes
    are replaced wholesale by a later module, never merged field-wise."""
    out = {}
    for r in cx.execute(
            f"SELECT record_name, record_uuid, source, source_kind, load_order, "
            f"entry_path, data FROM {table} "
            f"ORDER BY record_uuid, COALESCE(load_order,-1), id"):
        key = r["record_uuid"] or f"__noid_{len(out)}"
        out[key] = ({k: v for k, v in parse_data(r["data"]).items() if k in KEEP},
                    {"name": r["record_name"] or key, "uuid": r["record_uuid"],
                     "parent": None, "source": r["source"],
                     "source_kind": r["source_kind"], "load_order": r["load_order"],
                     "entry_path": r["entry_path"], "layers": 1}, [])
    if verbose:
        print(f"  {table}: {len(out)} effective records (uuid-keyed)", file=sys.stderr)
    return out


def build_effective(cx, table, verbose=False):
    """One scan -> {lower(name): (fields, meta)} with patch layers merged.

    Same rules as AGENTS.md and `lsdb get`: ascending load order; a definition
    whose `using_record` is its own name is a patch layer merged over the previous
    one; anything else replaces. Foreign parents are resolved in a second pass.
    """
    rows = cx.execute(
        f"SELECT record_name, record_uuid, using_record, source, source_kind, "
        f"load_order, entry_path, data FROM {table} "
        f"WHERE record_name IS NOT NULL "
        f"ORDER BY lower(record_name), COALESCE(load_order,-1), id")
    merged, cur_key, cur, meta, layers = {}, None, None, None, 0
    for r in rows:
        key = r["record_name"].lower()
        if key != cur_key:
            if cur_key is not None:
                merged[cur_key] = (cur, dict(meta, layers=layers))
            cur_key, cur, layers = key, {}, 0
            meta = {"name": r["record_name"], "uuid": r["record_uuid"],
                    "parent": None, "source": r["source"],
                    "source_kind": r["source_kind"], "load_order": r["load_order"],
                    "entry_path": r["entry_path"]}
        f = {k: v for k, v in parse_data(r["data"]).items() if k in KEEP}
        u = (r["using_record"] or "")
        if cur and u.lower() == key:
            cur.update(f)                       # patch layer
            layers += 1
        else:
            cur, layers = dict(f), 1            # fresh definition
            meta["parent"] = u or None
        meta.update({"source": r["source"], "source_kind": r["source_kind"],
                     "load_order": r["load_order"], "entry_path": r["entry_path"],
                     "uuid": r["record_uuid"] or meta["uuid"]})
    if cur_key is not None:
        merged[cur_key] = (cur, dict(meta, layers=layers))

    resolved, chains = {}, {}

    def resolve(key, seen):
        if key in resolved:
            return resolved[key], chains[key]
        if key not in merged or key in seen or len(seen) > 8:
            return {}, []
        seen.add(key)
        fields, meta = merged[key]
        parent = (meta.get("parent") or "").lower()
        if parent and parent in merged:
            pf, pchain = resolve(parent, seen)
            out = dict(pf)
            out.update(fields)
            chain = [merged[parent][1]["name"]] + pchain
        else:
            out, chain = dict(fields), []
        resolved[key], chains[key] = out, chain
        return out, chain

    for key in list(merged):
        resolve(key, set())
    if verbose:
        print(f"  {table}: {len(merged)} effective records", file=sys.stderr)
    return {k: (resolved[k], merged[k][1], chains[k]) for k in merged}


# ── edge extraction ─────────────────────────────────────────────────────────
def _polarity(text, name):
    """(has_positive, has_negated) for a predicate such as Ally / Enemy / Party."""
    pos = neg = False
    for m in re.finditer(r"(not\s+)?\b" + name + r"\s*\(", text or ""):
        if m.group(1):
            neg = True
        else:
            pos = True
    return pos, neg


def side_from_conditions(text):
    """'ally' | 'enemy' | None, reading predicate POLARITY rather than presence."""
    if not text:
        return None
    ally_pos, ally_neg = _polarity(text, "Ally")
    party_pos, _party_neg = _polarity(text, "Party")
    enemy_pos, enemy_neg = _polarity(text, "Enemy")
    if ally_pos or party_pos:
        return "ally"
    if enemy_pos:
        return "enemy"
    if enemy_neg:            # `not Enemy()` — the commonest way to say "an ally"
        return "ally"
    if ally_neg:
        return "enemy"
    return None


class Extractor:
    def __init__(self):
        self.edges, self.annot, self.unparsed = [], [], []
        self._hint = None

    def bad(self, tbl, name, field, snippet, reason):
        self.unparsed.append((tbl, name, field, snippet[:200], reason))

    def edge(self, kind, tbl, src, dst, detail="", chance=None, save=None,
             gated=0, target=None, field=None, side=None):
        self.edges.append((kind, tbl, src, str(dst), str(detail), chance, save,
                           gated, target, field, side))

    def side_of(self, cond_text, target_prefix):
        """Who the status lands on: self, ally, or enemy.

        This is the datum that makes a cross-body question answerable. A condition
        on the ENEMY is collected by whoever attacks it, a buff on an ALLY is
        collected by the partner, and a SELF buff is collected by nobody else.

        POLARITY IS THE WHOLE GAME HERE. `Target_Bless` reads
        `Character() and not Dead() and not Enemy()` and `not Enemy()` means ALLY;
        a retaliation robe reads `not Ally()` and means ENEMY. Matching the bare
        predicate name gets both exactly backwards, which silently mislabels the
        channel a pair sheet is asking about.
        """
        t = (target_prefix or "").upper()
        side = side_from_conditions(cond_text)
        if side:
            return side
        if t == "SELF":
            return "self"
        if t == "SWAP":
            return "enemy"        # retaliation: swaps to the creature that hit you
        return self._hint or "unknown"

    def functor_list(self, tbl, name, field, text):
        """A `;`-separated functor list: ApplyStatus / RemoveStatus / DealDamage.

        Items carry context prefixes (`GROUND:`, `AI_ONLY:`) and bracket groups
        (`CastOffhand[…]`); `normalize_functor` flattens both before parsing.
        """
        for raw in split_top(text):
          for item in normalize_functor(raw):
            conds, body = unwrap_if(item)
            cond_text = " and ".join(conds)
            gated = 1 if conds else 0
            sv = save_ability(cond_text) if conds else None
            for t in find_predicates(cond_text):
                self.edge("PREDICATE", tbl, name, t, "functor gate", field=field)
            for fl in find_flags(cond_text):
                self.edge("FLAG", tbl, name, fl, "functor gate", field=field)
            for st, neg in find_status_reads(cond_text):
                self.edge("READS", tbl, name, st, "functor gate",
                          gated=1, target="neg" if neg else "pos", field=field)
            fn, args = parse_call(body)
            if not fn:
                if body:
                    self.bad(tbl, name, field, body, "unparsed functor")
                continue
            base = fn.split(":")[-1]
            if base in ("ApplyStatus", "ApplyStatusOnTurn", "RemoveStatus"):
                if not args:
                    self.bad(tbl, name, field, body, f"{base} with no args")
                    continue
                a0 = strip_q(args[0]).upper()
                tgt = a0 if a0 in TARGETS else None
                status = strip_q(args[1]) if tgt and len(args) > 1 else strip_q(args[0])
                chance = None
                for a in args[2:] if tgt else args[1:]:
                    if re.match(r"^\d+$", a.strip()):
                        chance = int(a.strip())
                        break
                kind = "REMOVES" if base == "RemoveStatus" else "APPLIES"
                self.edge(kind, tbl, name, status.upper(), cond_text[:200],
                          chance=chance, save=sv, gated=gated, target=tgt,
                          field=field, side=self.side_of(cond_text, tgt))
            elif base == "DealDamage":
                dt = next((strip_q(a) for a in args if strip_q(a) in DAMAGE_TYPES), None)
                dice = args[1] if (tgt_is_target(args) and len(args) > 1) else (args[0] if args else "")
                if dt:
                    self.edge("DEALS", tbl, name, dt, strip_q(dice)[:60],
                              save=sv, gated=gated, field=field)
            elif base in ("CreateSurface", "SurfaceChange"):
                self.edge("SURFACE", tbl, name, strip_q(args[-1]) if args else "?",
                          base, gated=gated, field=field)
            elif base in ("CreateExplosion", "UseSpell", "UseSpellAsTarget",
                          "CastSpell", "UseAttack"):
                # "this triggers that spell", which is how an on-crit or on-hit
                # payoff usually reaches its real effect: Mortal Reminder is a
                # passive whose functor is CreateExplosion(Projectile_...), and
                # the Frightened status lives on the spell, two hops away.
                a0 = strip_q(args[0]).upper() if args else ""
                spell = (strip_q(args[1]) if a0 in TARGETS and len(args) > 1
                         else (strip_q(args[0]) if args else "?"))
                self.edge("CASTS", tbl, name, spell, base, gated=gated, field=field)
            else:
                # Parsed cleanly but not a synergy primitive — kept, not dropped,
                # so a motif that later needs it can find it.
                self.edge("OTHER", tbl, name, base, ",".join(map(strip_q, args))[:60],
                          gated=gated, field=field)

    def cond_text(self, tbl, name, field, text):
        for t in find_predicates(text):
            self.edge("PREDICATE", tbl, name, t, field, field=field)
        for fl in find_flags(text):
            self.edge("FLAG", tbl, name, fl, field, field=field)
        for st, neg in find_status_reads(text):
            self.edge("READS", tbl, name, st, field,
                      target="neg" if neg else "pos", field=field)
        sv = save_ability(text)
        if sv:
            self.edge("MODIFIES", tbl, name, f"SavingThrow.{sv}", "roll gate", field=field)

    def boost_list(self, tbl, name, field, text, plain_names=False):
        for item in split_top(text):
            conds, body = unwrap_if(item)
            cond_text = " and ".join(conds)
            gated = 1 if conds else 0
            for t in find_predicates(cond_text):
                self.edge("PREDICATE", tbl, name, t, "boost gate", field=field)
            for fl in find_flags(cond_text):
                self.edge("FLAG", tbl, name, fl, "boost gate", field=field)
            for st, neg in find_status_reads(cond_text):
                self.edge("READS", tbl, name, st, "boost gate",
                          target="neg" if neg else "pos", field=field)
            if plain_names:
                for nm in split_top(body, ","):
                    nm = strip_q(nm)
                    if nm:
                        kind = "GRANTS" if field != "StatusOnEquip" else "APPLIES"
                        self.edge(kind, tbl, name, nm, field, gated=gated, field=field)
                continue
            fn, args = parse_call(body)
            if not fn:
                if body:
                    self.bad(tbl, name, field, body, "unparsed boost")
                continue
            a = [strip_q(x) for x in args]
            if fn == "UnlockSpell":
                self.edge("UNLOCKS", tbl, name, a[0] if a else "?", "",
                          gated=gated, field=field)
            elif fn == "StatusImmunity":
                self.edge("IMMUNITY", tbl, name, (a[0] if a else "?").upper(), "",
                          gated=gated, field=field)
            elif fn == "Resistance":
                self.edge("RESIST", tbl, name, a[0] if a else "?",
                          a[1] if len(a) > 1 else "", gated=gated, field=field)
            elif fn in MODIFY_BOOSTS:
                self.edge("MODIFIES", tbl, name, fn, ",".join(a)[:80],
                          gated=gated, field=field)
                if fn in ("DamageBonus", "CharacterWeaponDamage", "WeaponDamage"):
                    for x in a:
                        if x in DAMAGE_TYPES:
                            self.edge("DEALS", tbl, name, x, f"{fn} rider",
                                      gated=gated, field=field)
            elif fn in SKIP_BOOSTS or fn.startswith("Unlock"):
                pass
            else:
                self.edge("OTHER", tbl, name, fn, ",".join(a)[:60],
                          gated=gated, field=field)

    def record(self, tbl, name, fields):
        start = len(self.edges)          # only this record's own edges below
        # Record-level side hint, overridden per functor by an explicit gate. Same
        # polarity rule: `not Enemy()` is an ally, `not Ally()` is an enemy.
        tc = " ".join(str(fields.get(k) or "") for k in
                      ("TargetConditions", "Conditions", "BoostConditions"))
        ctx = str(fields.get("StatsFunctorContext") or "")
        self._hint = side_from_conditions(tc)
        if not self._hint and ctx.startswith(("OnDamage", "OnAttack")):
            self._hint = "enemy"        # the thing you hit, or that hit you
        for f, v in fields.items():
            if not isinstance(v, str) or not v.strip():
                continue
            if f in FUNCTOR_FIELDS:
                self.functor_list(tbl, name, f, v)
            elif f in COND_FIELDS:
                self.cond_text(tbl, name, f, v)
            elif f in BOOST_FIELDS:
                self.boost_list(tbl, name, f, v,
                                plain_names=f in ("PassivesOnEquip", "Passives",
                                                  "PassivesAdded"))
        # annotations: what it costs to keep this running. LSX values are
        # occasionally lists, so every one is coerced before it is matched.
        def s(*keys):
            for k in keys:
                v = fields.get(k)
                if v:
                    return v if isinstance(v, str) else ",".join(map(str, v)) \
                        if isinstance(v, list) else str(v)
            return ""
        # A status belongs to status groups, and a reader of the group fires on
        # every member. Without this edge a condition looks like it has almost no
        # consumers: BLINDED itself is read once in the whole install, while
        # `SG_Blinded` is read by Hypnotic Stare, Blindsense and others.
        for grp in split_names(s("StatusGroups")):
            self.edge("INGROUP", tbl, name, grp, "StatusGroups",
                      field="StatusGroups")
        ctx, cooldown, inst = s("StatsFunctorContext", "TickType"), s("Cooldown"), s("AmountOfTargets")
        mine = self.edges[start:]
        applied = {e[3] for e in mine if e[0] == "APPLIES"}
        neg_reads = {e[3] for e in mine if e[0] == "READS" and e[8] == "neg"}
        clamped = 1 if applied & neg_reads else 0
        at_will = 1 if not cooldown and not clamped else 0
        multi = 1 if ("LevelMapValue" in inst or re.match(r"^\s*[2-9]", inst)) else 0
        self.annot.append((tbl, name, ctx, cooldown, s("StackId"),
                           s("UseCosts"), inst, multi, clamped, at_will))


def tgt_is_target(args):
    return bool(args) and strip_q(args[0]).upper() in TARGETS


# ── reachability ────────────────────────────────────────────────────────────
UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def build_origins(eff, ex, verbose=False):
    """Player-reachability closure: record -> {(kind, label, level)}.

    Seeds are the things a player actually picks: class and subclass progression
    tables, race progressions, feats, and equippable items. Everything else in the
    9,592 passives is monster, NPC or cut content, and filtering it out is what
    makes a synergy query readable.
    """
    # Keyed (tbl, name, kind, label) -> EARLIEST level. A class spell list is
    # referenced by every level row that can select from it, so keeping one tag
    # per (source, level) multiplied the table sixfold and answered a question
    # nobody asks. "Available from level N" is the useful fact.
    origins = {}
    by_record = {}          # (tbl, lower name) -> {(kind, label)} for propagation

    def tag(tbl, name, kind, label, level=None):
        nm = name.lower()
        key = (tbl, nm, kind, label)
        try:
            lv = int(level) if level not in (None, "") else None
        except (TypeError, ValueError):
            lv = None
        if key in origins:
            cur = origins[key]
            if lv is not None and (cur is None or lv < cur):
                origins[key] = lv
            return False
        origins[key] = lv
        by_record.setdefault((tbl, nm), set()).add((kind, label))
        return True

    # progression rows by TableUUID
    prog_by_table = {}
    for _k, (f, m, _c) in eff.get("type_progression", {}).items():
        tu = f.get("TableUUID")
        if tu:
            prog_by_table.setdefault(tu, []).append((f, m))
    # `MergedInto` is the THIRD resolution rule, beside load order and
    # `using_record`, and it is a UNION rather than an override: a list declaring
    # `MergedInto = <target>` adds its entries to that target instead of replacing
    # it. 887 of 2,379 spell lists use it, so resolving a list to its single
    # load-order winner silently loses a third of the game's list content — that
    # is how `ElementalBlast` looked unreachable when it is a normal feat pick.
    def list_index(recs, field):
        own, merged = {}, {}
        for uuid, (f, m, _c) in recs.items():
            own[uuid] = f.get(field) or ""
            tgt = f.get("MergedInto")
            if tgt:
                merged.setdefault(tgt, []).append(uuid)
        return own, merged

    def list_contents(uuid, idx, seen=None):
        own, merged = idx
        seen = seen if seen is not None else set()
        if uuid in seen:
            return []
        seen.add(uuid)
        out = split_names(own.get(uuid))
        for c in merged.get(uuid, []):
            out += list_contents(c, idx, seen)
        return out

    spell_idx = list_index(eff.get("type_spell_list", {}), "Spells")
    passive_idx = list_index(eff.get("type_passive_list", {}), "Passives")

    def seed_progression(uuid, kind, label):
        for f, _m in prog_by_table.get(uuid, []):
            lvl = f.get("Level")
            for nm in split_names(f.get("PassivesAdded")):
                if strip_q(nm):
                    tag("type_passive_data", strip_q(nm), kind, label, lvl)
            blob = (f.get("AddSpells") or "") + ";" + (f.get("Selectors") or "")
            for u in UUID_RE.findall(blob):
                for sp in list_contents(u, spell_idx):
                    tag("type_spell_data", sp, kind, label, lvl)
                for pv in list_contents(u, passive_idx):
                    tag("type_passive_data", pv, kind, label, lvl)

    for _k, (f, m, _c) in eff.get("type_class_description", {}).items():
        nm = f.get("Name") or m["name"]
        kind = "subclass" if f.get("ParentGuid") else "class"
        if f.get("ProgressionTableUUID"):
            seed_progression(f["ProgressionTableUUID"], kind, nm)
    for _k, (f, m, _c) in eff.get("type_race", {}).items():
        if f.get("ProgressionTableUUID"):
            seed_progression(f["ProgressionTableUUID"], "race", f.get("Name") or m["name"])
    for _k, (f, m, _c) in eff.get("type_feat", {}).items():
        label = f.get("Name") or m["name"]
        for nm in split_names(f.get("PassivesAdded")):
            if strip_q(nm):
                tag("type_passive_data", strip_q(nm), "feat", label)
        for u in UUID_RE.findall(f.get("Selectors") or ""):
            for pv in list_contents(u, passive_idx):
                tag("type_passive_data", pv, "feat", label)
            for sp in list_contents(u, spell_idx):
                tag("type_spell_data", sp, "feat", label)
    for tbl in ("type_armor", "type_weapon", "type_object"):
        for _k, (f, m, _c) in eff.get(tbl, {}).items():
            if f.get("PassivesOnEquip") or f.get("StatusOnEquip") or f.get("Boosts"):
                tag(tbl, m["name"], "item", m["name"])

    # Spell containers: unlocking `Projectile_ElementalBlast` makes every spell
    # declaring `SpellContainerID` at it castable, so a member inherits its
    # container's reachability. Without this the beam that a feat actually grants
    # looks unreachable while the container looks like a dead end.
    contained = {}
    for _k, (f, m, _c) in eff.get("type_spell_data", {}).items():
        cid = f.get("SpellContainerID")
        if cid:
            contained.setdefault(cid.lower(), []).append(m["name"])

    # BFS along the edges that actually grant a player something
    by_src = {}
    for kind, tbl, src, dst, *_rest in ex.edges:
        if kind in ("APPLIES", "GRANTS", "UNLOCKS", "CASTS"):
            by_src.setdefault((tbl, src.lower()), []).append((kind, dst))
    dst_table = {"APPLIES": "type_status_data", "GRANTS": "type_passive_data",
                 "UNLOCKS": "type_spell_data", "CASTS": "type_spell_data"}
    frontier = list(by_record)
    depth = 0
    while frontier and depth < 6:
        nxt = []
        for key in frontier:
            srcs = list(by_record.get(key, ()))
            targets = [(dst_table[k], d) for k, d in by_src.get(key, [])]
            if key[0] == "type_spell_data":
                targets += [("type_spell_data", m) for m in contained.get(key[1], [])]
            for tbl2, dst in targets:
                lv = min((origins[(key[0], key[1], k, lb)] for k, lb in srcs
                          if origins.get((key[0], key[1], k, lb)) is not None),
                         default=None)
                for k, lb in srcs:
                    if tag(tbl2, dst, k, lb, lv):
                        nxt.append((tbl2, dst.lower()))
        frontier, depth = list(dict.fromkeys(nxt)), depth + 1
    if verbose:
        print(f"  origins: {len(by_record)} records reachable, {len(origins)} tags", file=sys.stderr)
    return origins, by_record


# ── main ────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(prog="lsdb_index.py",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--db", default=DB_DEFAULT)
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    t0 = time.time()
    cx = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    cx.row_factory = sqlite3.Row

    eff = {}
    for t in EDGE_TABLES + SEED_TABLES:
        try:
            eff[t] = (build_uuid_keyed(cx, t, args.verbose) if t in UUID_KEYED
                      else build_effective(cx, t, args.verbose))
        except sqlite3.Error as e:
            print(f"skip {t}: {e}", file=sys.stderr)

    ex = Extractor()
    for t in EDGE_TABLES:
        for _k, (fields, meta, _chain) in eff.get(t, {}).items():
            ex.record(t, meta["name"], fields)
    if args.verbose:
        print(f"  edges: {len(ex.edges)}  unparsed: {len(ex.unparsed)}", file=sys.stderr)

    origins, by_record = build_origins(eff, ex, args.verbose)

    tmp = args.out + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    out = sqlite3.connect(tmp)
    out.executescript("""
      PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF;
      CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
      CREATE TABLE effective(tbl TEXT, name TEXT, uuid TEXT, source TEXT,
        source_kind TEXT, load_order INT, entry_path TEXT, layers INT,
        chain TEXT, fields TEXT);
      CREATE TABLE edges(kind TEXT, tbl TEXT, src TEXT, dst TEXT, detail TEXT,
        chance INT, save TEXT, gated INT, target TEXT, field TEXT, side TEXT);
      CREATE TABLE annot(tbl TEXT, name TEXT, context TEXT, cooldown TEXT,
        stackid TEXT, usecosts TEXT, instances TEXT, multi INT, clamped INT,
        at_will INT);
      CREATE TABLE origins(tbl TEXT, name TEXT, kind TEXT, label TEXT, level TEXT);
      CREATE TABLE unparsed(tbl TEXT, name TEXT, field TEXT, snippet TEXT,
        reason TEXT);
    """)
    for t, recs in eff.items():
        out.executemany(
            "INSERT INTO effective VALUES (?,?,?,?,?,?,?,?,?,?)",
            [(t, m["name"], m["uuid"], m["source"], m["source_kind"],
              m["load_order"], m["entry_path"], m["layers"], ",".join(ch),
              json.dumps(f, separators=(",", ":")))
             for _k, (f, m, ch) in recs.items()])
    out.executemany("INSERT INTO edges VALUES (?,?,?,?,?,?,?,?,?,?,?)", ex.edges)
    out.executemany("INSERT INTO annot VALUES (?,?,?,?,?,?,?,?,?,?)", ex.annot)
    out.executemany("INSERT INTO unparsed VALUES (?,?,?,?,?)", ex.unparsed)
    out.executemany("INSERT INTO origins VALUES (?,?,?,?,?)",
                    [(tbl, nm, k, lb, str(lv) if lv is not None else None)
                     for (tbl, nm, k, lb), lv in origins.items()])

    st = os.stat(args.db)
    build = cx.execute("SELECT value FROM metadata WHERE key LIKE '%build%' "
                       "OR key LIKE '%profile%' LIMIT 1").fetchone()
    out.executemany("INSERT INTO meta VALUES (?,?)", [
        ("source_db", os.path.abspath(args.db)),
        ("source_size", str(st.st_size)),
        ("source_mtime", str(int(st.st_mtime))),
        ("source_stamp", build["value"] if build else ""),
        ("built_at", time.strftime("%Y-%m-%dT%H:%M:%S")),
        ("edges", str(len(ex.edges))), ("unparsed", str(len(ex.unparsed))),
        ("origins", str(len(origins))),
    ])
    # What a status does to WHOEVER CARRIES IT, which is what separates one
    # cross-body channel from another:
    #   atk   grants advantage to anyone attacking the bearer  (BLINDED)
    #   weak  degrades the bearer's own rolls or actions        (POISONED, FRIGHTENED)
    #   buff  improves the bearer                              (BLESS, Battlemind Link)
    # A status can be several at once, and the classification is a heuristic over
    # its own boosts — the sign of a numeric argument decides buff from weaken.
    out.execute("CREATE TABLE status_role(name TEXT, atk INT, weak INT, buff INT)")
    role = {}
    for kind, tbl, src, dst, detail, *_ in ex.edges:
        if tbl != "type_status_data" or kind not in ("MODIFIES", "RESIST"):
            continue
        # `AI_HELPER_*` statuses are the engine's own AI scoring hints. Their
        # boosts are fabricated to tell the AI roughly how good a spell is —
        # Sacred Weapon applies AI_HELPER_BUFF_LARGE, which claims AC(3) and
        # Advantage the spell does not grant. Classifying them as channels
        # reports effects that do not exist.
        if src.upper().startswith("AI_HELPER"):
            continue
        r = role.setdefault(src.upper(), {"atk": 0, "weak": 0, "buff": 0})
        d = detail or ""
        neg = bool(re.search(r"-\s*\d", d))
        if dst == "SourceAdvantageOnAttack" or (dst == "Advantage" and "AttackTarget" in d):
            r["atk"] = 1
        elif dst == "Disadvantage" or dst == "ActionResourceBlock" or dst == "Incapacitated":
            r["weak"] = 1
        elif neg:
            r["weak"] = 1
        elif kind == "RESIST" or dst in (
                "Advantage", "AC", "RollBonus", "DamageBonus", "Initiative",
                "TemporaryHP", "ActionResource", "IncreaseMaxHP", "Ability",
                "ProficiencyBonus", "Invulnerable", "SpellSaveDC", "CriticalHit",
                "ReduceCriticalAttackThreshold", "MinimumRollResult", "Reroll"):
            r["buff"] = 1
    out.executemany("INSERT INTO status_role VALUES (?,?,?,?)",
                    [(k, v["atk"], v["weak"], v["buff"]) for k, v in role.items()])
    out.execute("CREATE INDEX status_role_name ON status_role(name)")
    # How many distinct sources reach a record. This is the specificity signal a
    # synergy query ranks on: a passive reachable from 40 places is a generic
    # spell-list entry, one reachable from 1-2 is a signature feature, and it is
    # the signature pairs that are worth a human's attention.
    out.execute("CREATE TABLE origin_count(tbl TEXT, name TEXT, n INT)")
    out.executemany("INSERT INTO origin_count VALUES (?,?,?)",
                    [(tbl, nm, len({lb for _k, lb in srcs}))
                     for (tbl, nm), srcs in by_record.items()])
    out.execute("CREATE INDEX origin_count_name ON origin_count(tbl, name)")
    # Which class a subclass belongs to, so a consumer can ask the only question
    # that separates a one-body combo from a two-body one: does the pair fit in
    # twenty levels? Snowlight@3 + GreatOldOne@1 is 4 levels and fits; Snowlight@11
    # + Mesmerist@11 is 22 and is CROSS-BODY ONLY.
    cd = eff.get("type_class_description", {})
    by_uuid = {m["uuid"]: (f, m) for _k, (f, m, _c) in cd.items() if m.get("uuid")}
    out.execute("CREATE TABLE origin_meta(label TEXT, kind TEXT, parent_class TEXT)")
    rows = []
    for _k, (f, m, _c) in cd.items():
        nm = f.get("Name") or m["name"]
        pg = f.get("ParentGuid")
        if pg and pg in by_uuid:
            pf, pm = by_uuid[pg]
            rows.append((nm, "subclass", pf.get("Name") or pm["name"]))
        else:
            rows.append((nm, "class", nm))
    out.executemany("INSERT INTO origin_meta VALUES (?,?,?)", rows)
    out.execute("CREATE INDEX origin_meta_label ON origin_meta(label)")
    out.executescript("""
      CREATE INDEX edges_dst ON edges(dst, kind);
      CREATE INDEX edges_src ON edges(src, kind);
      CREATE INDEX edges_kind ON edges(kind);
      CREATE INDEX annot_name ON annot(name);
      CREATE INDEX origins_name ON origins(name);
      -- `origins.name` is lowercased while `edges.src` keeps display case, so a
      -- global join is `origins.name = lower(edges.src)` and needs both columns
      -- indexed together; without this a roster-wide ranking degrades to a scan.
      CREATE INDEX origins_reach ON origins(tbl, name, kind);
      CREATE INDEX origins_kind ON origins(kind, label);
      CREATE INDEX effective_name ON effective(name);
    """)
    out.commit()
    out.close()
    os.replace(tmp, args.out)

    n_unp = len(ex.unparsed)
    rate = 100.0 * n_unp / max(1, len(ex.edges) + n_unp)
    print(f"{args.out}: {len(ex.edges)} edges · "
          f"{sum(len(v) for v in eff.values())} effective records · "
          f"{len(origins)} origin tags · "
          f"{n_unp} unparsed ({rate:.2f}%) · {time.time() - t0:.1f}s")
    if rate > 5:
        print("WARNING: unparsed rate above 5% — inspect the `unparsed` table "
              "before trusting motif output", file=sys.stderr)


if __name__ == "__main__":
    main()
