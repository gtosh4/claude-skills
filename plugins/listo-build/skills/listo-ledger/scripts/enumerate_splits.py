#!/usr/bin/env python3
"""Enumerate every split a subclass can express, compose each, and rank them.

The split is the most consequential thing the pipeline decides, and until now an agent guessed it
two subclasses at a time. This searches the space instead: primary class from 11 to 20 levels,
the remainder spent on catalogued dip breakpoints, one class marked level-1, composed from parts
and ranked by pair value against the pool of everything enumerated.

Composed vectors are FILTER-GRADE and are never published. They decide which splits are worth
spending real scoring on; tier 2 re-derives every number from the rubric.

    scripts/enumerate_splits.py --limit 2 -o variants.json
"""
import json, os, sys, itertools, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "listo-build", "scripts"))
import compose as CO                                              # noqa: E402
import seed_index as SI                                           # noqa: E402
from scoring import (KEYS, SAV_IDX, derive_saves, derive_skills,   # noqa: E402
                     score_bodies)

MIN_PRIMARY = 11          # a majority of twenty; below this the subclass is not the subject
MAX_CLASSES = 3


def bases_for_compose(doc):
    """Turn the tier-1 records into what `compose` wants, including the not-first fallbacks."""
    arrives = doc.get("arrives", {})
    out = {}
    for k, b in doc["bases"].items():
        if b["verdict"] != "candidate":
            continue
        late = arrives.get(k, {})
        prof_late = [a for a in b["prof"] if a in late]      # kept when this class is not first
        armour_late = b["armour"] if "armour" in late else None
        out[k] = {"vector": [x if x is not None else 0 for x in b["scores"]],
                  "prof": b["prof"], "prof_late": prof_late,
                  "armour": b["armour"], "armour_late": armour_late,
                  "shield": b["shield"], "concentration": b["concentration"],
                  "boosters": b["boosters"]}
    return out


def parts_by_class(cat):
    """`{class: {levels: [part_id, ...]}}` — generic parts and their subclass alternatives."""
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    for pid in cat["parts"]:
        if pid == "exit":
            continue
        bits = pid.split("/")
        cls, lv = bits[0], int(bits[1])
        out[cls][lv].append(pid)
    return out


def subclasses_by_class(cat):
    """`{class: {subclass: [part_id, ...]}}`, so a dip can take every row at or below its level."""
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    for pid in cat["parts"]:
        if pid == "exit":
            continue
        bits = pid.split("/")
        if len(bits) == 3:
            out[bits[0]][bits[2]].append(pid)
    return out


def dip_sets(pbc, primary, remainder, sbc=None):
    """Every legal way to spend `remainder` levels on at most two other classes.

    A subclass is offered when it has ANY row at or below the dip's level, and it brings all of
    them. Requiring a row at exactly `remainder` dropped the level-1 grants off every deeper dip
    and made Cleric 2 (Light) — a domain whose entire payload is its level-2 Channel Divinity —
    impossible to express.
    """
    sbc = sbc or {}
    if remainder == 0:
        yield ()
        return
    others = [c for c in pbc if c != primary]
    for c in others:
        for lv in pbc[c]:
            if lv == remainder:
                for pid in pbc[c][lv]:
                    if len(pid.split("/")) == 2:          # generic part
                        yield ((c, lv, pid, None),)
                        for sub, pids in sorted(sbc.get(c, {}).items()):
                            chain = tuple(p for p in pids if int(p.split("/")[1]) <= lv)
                            if chain:
                                yield ((c, lv, pid, (sub, chain)),)
    for ca, cb in itertools.combinations(others, 2):
        for la in pbc[ca]:
            lb = remainder - la
            if lb <= 0 or lb not in pbc[cb]:
                continue
            ga = [p for p in pbc[ca][la] if len(p.split("/")) == 2]
            gb = [p for p in pbc[cb][lb] if len(p.split("/")) == 2]
            for pa in ga:
                for pb in gb:
                    yield ((ca, la, pa, None), (cb, lb, pb, None))


def _picks(cat, pid, first):
    """How many skill proficiencies one generic part hands over, and how much Expertise."""
    p = cat["parts"].get(pid) or {}
    side = p.get("as_first" if first else "as_dip", {})
    g = side.get("grants", {})
    return g.get("skills", 0), g.get("expertise", 0)


def enumerate_for(key, base, cat, pbc, cls_of, sbc=None):
    """Every composed variant of one subclass, as `[(label, vector, meta)]`."""
    primary = cls_of[key]
    out = []
    for p in range(MIN_PRIMARY, 21):
        for dips in dip_sets(pbc, primary, 20 - p, sbc):
            if len(dips) + 1 > MAX_CLASSES:
                continue
            firsts = [None] + [d[0] for d in dips]        # primary first, or a dip class first
            for first in firsts:
                parts = []
                for c, lv, gen, sub in dips:
                    parts.append((gen, first == c))
                    if sub:
                        parts.append((sub[1], False))     # every row the subclass has by `lv`
                try:
                    # `requires` gates on the body's primary ABILITY, not its class. A Hexblade
                    # dip is transformative on a Charisma body and near-worthless on a Strength
                    # one, and that is the main thing stopping a three-class split from being
                    # good at everything for free.
                    vec, prof, picked = CO.compose(
                        cat, base, parts, primary=primary,
                        primary_ability=base.get("primary"), primary_levels=p,
                        concentration=base.get("concentration", False),
                        primary_first=(first is None))
                except Exception:
                    continue
                # Skills, which the search could not see at all until now. Each class may only
                # spend its picks on its own level-1 list, so the budget is per class, not a
                # total — and `compose` already collected what every dip part hands over. Only
                # the primary's own level-1 picks have to be added here, since it is not a part.
                pn, pe = _picks(cat, f"{primary}/1", first is None)
                budgets = [(primary, pn, None)] + picked["skills"]
                expertise = ([(None, pe)] if pe else []) + picked["expertise"]
                skills = CO.compose_skills(cat, budgets, base.get("primary"),
                                           {primary.title()} | {c.title() for c, *_ in dips},
                                           expertise)
                bits = [f"{primary.title()} {p}"] + [
                    f"{c.title()} {lv}" + (f" ({s[0]})" if s else "") for c, lv, _g, s in dips]
                label = " / ".join(bits) + ("" if first is None else f"  [{first.title()} first]")
                out.append((label, vec, {"primary": primary, "primary_levels": p,
                                         "dips": [(c, lv, g, s[0] if s else None)
                                                  for c, lv, g, s in dips],
                                         "first": first or primary, "prof": prof,
                                         "skills": skills,
                                         "classes": sorted({primary.title()}
                                                           | {c.title() for c, *_ in dips})}))
    return out


def to_chassis(vec, prof, boosters, concentration, reach="hybrid", skills=None, split="",
               classes=()):
    """A composed variant in the shape `score_bodies` wants.

    `skills` is not optional in practice: `skills_pair` scores off modifiers, so a body handed
    none contributes nothing to an axis carrying 23% of the non-tempo half.
    """
    sc = list(vec)
    sc[SAV_IDX] = None
    skills = skills or {a: {} for a in ("I", "II", "III")}
    cls = set(classes)
    per_act = {}
    for a in ("I", "II", "III"):
        row = list(sc)
        row[KEYS.index("skl")] = derive_skills(skills.get(a, {}), a, cls)
        per_act[a] = row
    return {"_id": "v", "reach": reach, "concentration": concentration, "split": split,
            "skills": skills,
            "scores": per_act,
            "saves": {a: {"prof": list(prof), "boosters": list(boosters)}
                      for a in ("I", "II", "III")}}


def _skl_key(meta):
    """The skill map flattened, so `dedupe` can tell two otherwise identical vectors apart."""
    sk = meta.get("skills") or {}
    return [sk.get(a, {}).get(s, 0) for a in ("I", "II", "III") for s in sorted(CO.SKILL_ABILITY)]


def pair_value(a, b):
    try:
        return score_bodies(dict(a, _id="a"), dict(b, _id="b"))["score"]
    except Exception:
        return 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--limit", type=int, default=2, help="variants kept per subclass")
    ap.add_argument("--only", help="comma-separated subclass keys, for a smoke test")
    ap.add_argument("--pool-cap", type=int, default=0, help="0 = use every distinct variant")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    doc = json.load(open(os.path.join(ASSETS, "subclass-bases.json")))
    cat = CO.load()
    bases = bases_for_compose(doc)
    inv = SI.inventory()
    cls_of = {f"{c}/{s}": c for c, subs in inv.items() for s in subs}
    keys = [k for k in bases if not a.only or k in a.only.split(",")]
    pbc = parts_by_class(cat)
    sbc = subclasses_by_class(cat)

    per, allv = {}, []
    for k in keys:
        vs = enumerate_for(k, bases[k], cat, pbc, cls_of, sbc)
        # Two variants are only indistinguishable if their SKILL modifiers match too — the pair
        # score reads those directly, not the composed rung.
        d = CO.dedupe([(f"{k}::{lab}", v + _skl_key(m)) for lab, v, m in vs])
        d = [(vid, vec[:len(KEYS)], merged) for vid, vec, merged in d]
        meta = {f"{k}::{lab}": m for lab, _v, m in vs}
        per[k] = (d, meta)
        allv += d
    print(f"{len(keys)} subclasses -> {sum(len(v) for v, _ in per.values())} distinct variants "
          f"(from {sum(1 for k in per for _ in per[k][0])} kept after dedupe)", file=sys.stderr)

    # A prefix is every variant of the first subclass and none of the rest, which is not a pool.
    # Stride-sample instead, so a cap still spans the whole enumerated space.
    if a.pool_cap and len(allv) > a.pool_cap:
        step = len(allv) / a.pool_cap
        pool = [allv[int(i * step)] for i in range(a.pool_cap)]
    else:
        pool = allv
    pool_ch = [(vid, to_chassis(v, per[vid.split("::")[0]][1][vid]["prof"],
                                bases[vid.split("::")[0]]["boosters"],
                                bases[vid.split("::")[0]]["concentration"],
                                skills=per[vid.split("::")[0]][1][vid]["skills"],
                                split=vid.split("::", 1)[1],
                                classes=per[vid.split("::")[0]][1][vid]["classes"]))
               for vid, v, _m in pool]
    print(f"pool: {len(pool_ch)} bodies", file=sys.stderr)

    out = {}
    for i, (k, (d, meta)) in enumerate(sorted(per.items()), 1):
        cand = [(vid, to_chassis(v, meta[vid]["prof"], bases[k]["boosters"],
                                 bases[k]["concentration"], skills=meta[vid]["skills"],
                                 split=vid.split("::", 1)[1],
                                 classes=meta[vid]["classes"])) for vid, v, _m in d]
        ranked = []
        for vid, ch in cand:
            s = sorted((pair_value(ch, pc) for pid, pc in pool_ch if pid != vid), reverse=True)
            ranked.append((vid, sum(s[:10]) / max(1, len(s[:10]))))
        ranked.sort(key=lambda t: -t[1])
        kept = CO.pick(ranked, d, a.limit)
        out[k] = [{"id": vid, "value": round(val, 3), "split": vid.split("::", 1)[1],
                   "vector": next(v for x, v, _ in d if x == vid),
                   "meta": {kk: vv for kk, vv in meta[vid].items() if kk != "prof"}}
                  for vid, val in kept]
        if i % 20 == 0:
            print(f"  ranked {i}/{len(per)}", file=sys.stderr)
    if a.out:
        json.dump(out, open(a.out, "w"), indent=2, ensure_ascii=False)
    print(f"kept {sum(len(v) for v in out.values())} variants across {len(out)} subclasses",
          file=sys.stderr)
    return out


if __name__ == "__main__":
    main()
