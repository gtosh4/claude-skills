#!/usr/bin/env python3
"""What a published score actually depends on, per chassis.

`DEPS["score"]` covers the rules a score was authored under — the brief, the rubric, the model,
the gates. It does not cover the *body*. A seed's `src` is the closest thing the pipeline had, and
it covers one subclass plus its class's at-a-glance section: exactly right for a seed, which is a
judgement about one subclass, and wrong for a score, which is a judgement about a two- or
three-class body. Edit the Wizard file and every `… / Wizard 6 (Evocation)` chassis in the ledger
keeps a score that reads as current and was derived from text that no longer exists.

So a scoring result records the digest of every source it was actually derived from:

    judgment_rules  the brief, rubric, model and gates          — DEPS["score"]
    schema          the output contract and closed registries   — ledger-schema.md
    body_sources    every class's at-a-glance and every named subclass block, per class
    compiled_data   the spell-access sections for the classes involved
    pak_evidence    installed-pak excerpts a published judgement leans on, when there are any

and, kept deliberately apart from those:

    selection_provenance   the base profile and catalogue parts that *selected* this split

The separation is the whole point. A moved base profile or dip part means the search might now
choose a different body; it does not mean the score of the body already published is false. Score
validity is `(address, deps)`; selection provenance is audited by enumeration, which decides
whether a *new* body needs scoring at all.

    scripts/score_deps.py "cleric/Tempest:lockdown" "Cleric 14 (Tempest) / Sorcerer 6 (Storm Sorcery)"
"""
import json, os, re, sys, argparse, hashlib

HERE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
BUILD  = os.path.join(os.path.dirname(os.path.dirname(HERE)), "listo-build")
DATA   = os.path.join(BUILD, "data")
sys.path.insert(0, HERE)
import seed_index as SI                                        # noqa: E402

SCHEMA  = os.path.join(ASSETS, "ledger-schema.md")
SPELLS  = os.path.join(DATA, "listo-10.2-spells.md")
BASES   = os.path.join(ASSETS, "subclass-bases.json")
CATALOG = os.path.join(ASSETS, "dip-catalogue.json")

_SEG = re.compile(r"^(.+?)\s+(\d{1,2})(?:\s*\((.*)\))?$")

# A split writes the subclass the way the game displays it; a class file writes the heading the
# way the file is organised. "Cleric 14 (Zeal Domain)" and "### Zeal (Hazoret)" are the same
# subclass. These are the words a display name adds and a heading drops, and they are stripped
# only from the *end* of a multi-word name — `Order` and `Way` are real headings on their own.
GENERIC = ("domain", "school", "circle", "college", "path", "oath", "way",
           "patron", "bloodline", "conclave", "archetype", "aspect")


class DepsError(Exception):
    pass


def _require(cond, msg):
    if not cond:
        raise DepsError(msg)


def _digest(text):
    return hashlib.sha256(text.encode() if isinstance(text, str) else text).hexdigest()[:12]


def _norm(s):
    """Padded, punctuation-free lowercase, so containment tests land on whole words."""
    return " " + re.sub(r"[^a-z0-9]+", " ", s.lower()).strip() + " "


def split_parts(text):
    """`[(class key, levels, subclass display name or None), ...]` from a split string.

    `seed_index.parse_split` drops the parenthetical, because a seed only needs the level
    arithmetic. A dependency record needs the parenthetical: it is what says *which* `###` block
    of the secondary class this body was derived from.
    """
    out = []
    for seg in text.split("/"):
        seg = seg.strip()
        if not seg:
            continue
        m = _SEG.match(seg)
        _require(m, f"cannot read a `<class> <levels> (<subclass>)` part from {seg!r}")
        cls = m.group(1).strip().lower().replace(" ", "")
        sub = (m.group(3) or "").strip()
        out.append((cls, int(m.group(2)), None if sub.lower() in ("", "none") else sub))
    _require(out, f"split names no classes: {text!r}")
    return out


def resolve_subclass(cls, display, inv):
    """The `###` heading a split's parenthetical names, or `None` if nothing matches uniquely.

    Tried in order: the same name; a heading that contains the display name, which covers the
    decorated headings (`Base game (Patch 8) — Berserker`); the display name containing a
    heading, which covers the expanded ones (`School of Divination` against `### Divination`);
    then the same two again with a trailing generic word stripped. An ambiguous match returns
    `None` exactly as a missing one does — guessing between two subclasses is worse than saying
    the record could not be built.
    """
    subs = inv.get(cls, [])
    names = [display]
    words = display.split()
    if len(words) > 1 and words[-1].lower().strip("()") in GENERIC:
        names.append(" ".join(words[:-1]))
    for name in names:
        p = _norm(name)
        for pick in ([s for s in subs if _norm(s) == p],
                     [s for s in subs if p.strip() and p in _norm(s)],
                     [s for s in subs if _norm(s).strip() and _norm(s) in p]):
            if len(pick) == 1:
                return pick[0]
            if len(pick) > 1:
                return None
    return None


def body_sources(split, inv=None):
    """`({source id: digest}, [unresolved, ...])` for every class the body is built from.

    Each class contributes its at-a-glance block — the class-level facts every split of it
    depends on — and, where the split names one, that subclass's `###` block. Source ids are
    `<class>.md#<section>`, not line ranges: a range moves when unrelated text above it is
    edited, and a score that goes stale because a paragraph moved is a false alarm the pipeline
    would learn to ignore.
    """
    inv = inv if inv is not None else SI.inventory()
    out, unresolved = {}, []
    for cls, _levels, display in split_parts(split):
        if cls not in inv:
            unresolved.append(f"{cls}: no class file")
            continue
        glance, blocks = SI.sections(cls)
        out[f"{cls}.md#at-a-glance"] = _digest(glance)
        if display is None:
            continue
        head = resolve_subclass(cls, display, inv)
        if head is None:
            unresolved.append(f"{cls}: cannot resolve subclass {display!r} to a `###` heading")
            continue
        out[f"{cls}.md#{head}"] = _digest(blocks[head])
    return out, unresolved


def spell_sections():
    """`{class: text}` from the compiled spell file's `## Per-class notes`.

    Its `###` children are `<Class> — <headline>`, so the class is the leading word or two.
    """
    with open(SPELLS) as fh:
        lines = fh.read().split("\n")
    lo = hi = None
    for i, l in enumerate(lines):
        if l.startswith("## "):
            if lo is None and "per-class" in l.lower():
                lo = i
            elif lo is not None and hi is None:
                hi = i
    _require(lo is not None, f"{os.path.basename(SPELLS)}: no `## Per-class notes` section")
    out, head, body = {}, None, []
    for l in lines[lo + 1:hi or len(lines)]:
        if l.startswith("### "):
            if head:
                out[head] = "\n".join(body)
            head = re.split(r"\s+[—-]\s+", l[4:].strip())[0].strip().lower().replace(" ", "")
            body = []
        elif head:
            body.append(l)
    if head:
        out[head] = "\n".join(body)
    return out


def compiled_data(split):
    """Spell-access digests for the classes in the body, keyed `<file>:<class>`.

    Only the classes involved. The whole spell corpus is a dependency of nothing: a Wizard note
    changing has no bearing on a Fighter/Rogue, and hashing the file whole would rescore the
    roster every time one class's list moved.
    """
    per = spell_sections()
    return {f"{os.path.basename(SPELLS)}:{cls}": _digest(per[cls])
            for cls, _lv, _sub in split_parts(split) if cls in per}


def selection_provenance(split, inv=None):
    """The structural records that *selected* this split, hashed apart from the score's own deps.

    `subclass_base` is the base profile of each subclass in the body; `dip_parts` is every
    catalogue part the search could have bought for these classes at these levels. Moving either
    can change which body is chosen. Neither says anything about whether the chosen body was
    scored correctly, which is why this is not part of `deps`.
    """
    inv = inv if inv is not None else SI.inventory()
    with open(BASES) as fh:
        bases = json.load(fh).get("bases", {})
    with open(CATALOG) as fh:
        parts = json.load(fh).get("parts", {})
    base_h, dips = {}, {}
    for cls, levels, display in split_parts(split):
        if display is not None:
            head = resolve_subclass(cls, display, inv)
            key = f"{cls}/{head}" if head else None
            if key in bases:
                base_h[key] = _digest(json.dumps(bases[key], sort_keys=True))
        for pid, rec in parts.items():
            bits = pid.split("/")
            if bits[0] == cls and bits[1].isdigit() and int(bits[1]) <= levels:
                dips[pid] = _digest(json.dumps(rec, sort_keys=True))
    return {"subclass_base": base_h, "dip_parts": dips}


def deps_for(address, split, pak_evidence=(), inv=None):
    """The complete dependency document for one chassis's score.

    Raises rather than returning a partial record. A dependency set that quietly omits the
    secondary class it could not resolve is worse than no dependency set at all: it would make
    every later staleness check pass for the wrong reason.
    """
    inv = inv if inv is not None else SI.inventory()
    src, unresolved = body_sources(split, inv)
    _require(not unresolved,
             f"{address}: cannot build a dependency record — " + "; ".join(unresolved))
    with open(SCHEMA, "rb") as fh:
        schema = _digest(fh.read())
    return {"format": 1,
            "address": address,
            "split": split,
            "deps": {"judgment_rules": SI.deps_hash("score"),
                     "schema": schema,
                     "body_sources": src,
                     "compiled_data": compiled_data(split),
                     "pak_evidence": sorted(pak_evidence)},
            "selection_provenance": selection_provenance(split, inv)}


def stale(recorded, current):
    """Which dependency keys moved between two `deps` objects. Empty means the result is valid.

    A key that disappeared counts as moved: the body no longer reads a source it was derived
    from, which is a change of exactly the kind this record exists to catch.
    """
    moved = []
    for field in ("judgment_rules", "schema"):
        if recorded.get(field) != current.get(field):
            moved.append(field)
    for field in ("body_sources", "compiled_data"):
        old, new = recorded.get(field) or {}, current.get(field) or {}
        moved += sorted(f"{field}:{k}" for k in set(old) | set(new) if old.get(k) != new.get(k))
    if sorted(recorded.get("pak_evidence") or []) != sorted(current.get("pak_evidence") or []):
        moved.append("pak_evidence")
    return moved


def audit_ledger(path):
    """Every published chassis whose dependency record cannot be built, and why.

    Failing to resolve a split's subclass is not a bookkeeping problem. It means the body claims
    levels in something the class files do not describe — a heading that was renamed, or a
    subclass the modlist removed — and a chassis nobody can trace to a source is the same
    invisible defect the fail-closed doctrine exists to refuse.
    """
    with open(path) as fh:
        chassis = json.load(fh).get("chassis", {})
    inv, bad = SI.inventory(), []
    for cid, c in chassis.items():
        try:
            deps_for(cid, c.get("split", ""), inv=inv)
        except (DepsError, SI.SeedError) as e:
            bad.append((cid, c.get("split", ""), str(e).split("— ", 1)[-1]))
    return len(chassis), bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("address", nargs="?",
                    help="build address, `<class>/<subclass heading>:<niche>`")
    ap.add_argument("split", nargs="?", help="the body's 20-level split, exactly as published")
    ap.add_argument("--pak", action="append", default=[],
                    help="a pak excerpt this judgement leans on; repeatable")
    ap.add_argument("--ledger", metavar="PATH",
                    help="instead of one address: report every chassis in this ledger whose "
                         "dependency record cannot be built")
    a = ap.parse_args()
    if a.ledger:
        total, bad = audit_ledger(a.ledger)
        for cid, split, why in bad:
            print(f"{cid}: {why}\n  {split}", file=sys.stderr)
        print(f"{total} chassis, {len(bad)} without a traceable source set", file=sys.stderr)
        sys.exit(1 if bad else 0)
    if not (a.address and a.split):
        ap.error("give an address and a split, or --ledger PATH")
    try:
        json.dump(deps_for(a.address, a.split, a.pak), sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    except (DepsError, SI.SeedError) as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
