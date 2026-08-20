#!/usr/bin/env python3
"""Compose a chassis vector from parts, to FILTER splits — never to publish a number.

The split is the sweep's most consequential output and the stage that picks it cannot
evaluate it. Composition makes the choice searchable: enumerate every split the catalogue
can express, compose an estimate, keep the non-dominated ones, and spend real scoring only
on those. See listo-ledger/SKILL.md, "Searching the split space".

Composition is deliberately coarse and has three known error modes, all documented in
assets/dip-catalogue.json: position (only the level-1 class grants saves and good armour),
saturation (Extra Attack and bonus actions do not stack), and stat conditionality. It is
tuned to OVER-admit, because a filter's only fatal error is dropping a real candidate.
"""
import json, os, sys, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "listo-build", "scripts"))
from scoring import KEYS, SAV_IDX, derive_saves            # noqa: E402

ARMOUR = {None: 0, "light": 1, "medium": 2, "heavy": 3}
# Filter-grade only. Durability is authored against the rubric at scoring time; this is just
# enough to stop an unarmoured body reading like an armoured one during the search.
ARMOUR_DUR = {0: 0, 1: 1, 2: 2, 3: 3}


def load(path=None):
    return json.load(open(path or os.path.join(ASSETS, "dip-catalogue.json")))


def _part(cat, pid, first):
    p = cat["parts"].get(pid)
    if p is None:
        raise KeyError(f"no catalogue part {pid!r}")
    if "as_first" in p or "as_dip" in p:
        side = p["as_first"] if first else p["as_dip"]
        return side.get("grants", {}), dict(side.get("deltas", {})), p
    # A subclass part is normally deltas only — its grants come from the generic part at the same
    # level. But some subclasses genuinely hand out proficiency the base class does not: Favored
    # Soul's medium armour and shields, College of Valour's martial package, Armorer's heavy
    # armour. Those are set-valued like any other grant, so they are honoured here rather than
    # being smuggled in as a durability delta, which would double-count against the armour floor.
    return p.get("grants", {}), dict(p.get("deltas", {})), p


def compose(cat, base, parts, primary=None, primary_levels=20, concentration=False,
            primary_first=True, primary_ability=None):
    """`base` is the primary subclass's own 20-level vector + grants; `parts` are the dips.

    Each part is `(part_id, is_first)`. **Exactly one class in a build is the level-1 class**, and
    it is the only one that grants saving throws. When the primary is not first it keeps only the
    proficiencies its *subclass* hands out later — Slippery Mind at 15, Diamond Soul at 14, Iron
    Mind at 7 — and loses the class's own level-1 pair. `base["prof_late"]` carries that subset,
    from the `arrives` map the grants pass produced. Armour is treated the same way.
    """
    v = {k: base["vector"][i] for i, k in enumerate(KEYS)}
    if primary_first:
        prof = set(base.get("prof", []))
        armour = ARMOUR[base.get("armour")]
    else:
        prof = set(base.get("prof_late", []))
        armour = ARMOUR[base.get("armour_late")]
    shield = bool(base.get("shield"))

    firsts = [p for p, f in parts if f]
    if len(firsts) > 1:
        raise ValueError(f"two classes marked level-1: {firsts}")

    # Deltas, grouped by conflict tag so competing sources do not stack.
    pending, tagged = [], {}
    for pid, first in parts:
        grants, deltas, meta = _part(cat, pid, first)
        prof |= set(grants.get("prof", []))
        armour = max(armour, ARMOUR[grants.get("armour")])
        shield = shield or bool(grants.get("shield"))
        if meta.get("requires") and primary_ability:
            want = meta["requires"].get("primary")
            if want and want != primary_ability:
                deltas = {k: x / 2 for k, x in deltas.items()}   # stat gate unmet: halved
        for tag in meta.get("conflicts") or []:
            best = tagged.get(tag)
            if best is None or sum(deltas.values()) > sum(best.values()):
                tagged[tag] = deltas
            deltas = None
            break
        if deltas is not None:
            pending.append(deltas)

    # Exit cost: the primary stopped short of 20 and lost the top of its own table.
    if primary and primary_levels < 20:
        table = cat["parts"].get("exit", {}).get(primary.lower().replace(" ", ""), {})
        for lvl in sorted((int(x) for x in table), reverse=True):
            if primary_levels <= lvl:
                pending.append(table[str(lvl)])

    for d in pending + list(tagged.values()):
        for k, x in d.items():
            v[k] = v[k] + x

    v["dur"] = max(v["dur"], ARMOUR_DUR[armour] + (1 if shield else 0))
    out = [max(0, min(5, round(v[k]))) for k in KEYS]
    out[SAV_IDX] = derive_saves(sorted(prof), [], concentration)
    return out, sorted(prof)


def dominates(a, b):
    return all(x >= y for x, y in zip(a, b)) and any(x > y for x, y in zip(a, b))


def frontier(vectors):
    """Indices of the non-dominated vectors. Ten-axis and weight-free, so it over-admits."""
    keep = []
    for i, v in enumerate(vectors):
        if any(dominates(vectors[j], v) for j in range(len(vectors)) if j != i):
            continue
        if any(vectors[j] == v for j in keep):
            continue
        keep.append(i)
    return keep


def dedupe(variants):
    """Collapse variants that compose to the same vector.

    Two variants with an identical composed vector are indistinguishable to the filter — it
    ranks on pair value, and pair value is a function of the vector alone. So scoring both is
    wasted, and pairing both is wasted quadratically: the pool is every distinct variant, and
    the ranking step is |variants| x |pool|.

    Measured on a simulated enumeration, 31% of variants collapse. That is 31% off the candidate
    count *and* off the pool, so roughly half the pairing work.

    `variants` is `[(id, vector), ...]`. Returns `[(id, vector, [merged_ids])]`, keeping the
    first id seen as the representative so the result is deterministic.
    """
    out, seen = [], {}
    for vid, vec in variants:
        key = tuple(vec)
        if key in seen:
            out[seen[key]][2].append(vid)
            continue
        seen[key] = len(out)
        out.append((vid, list(vec), []))
    return out


def pool_rank(variants, pool, score_pair, k=10):
    """Rank variants by the mean of their `k` best pair scores against `pool`.

    This is the selection criterion, and it is deliberately not a hand-weighted formula. The
    combiner already prices the three axis kinds correctly — measured, dropping an axis two rungs
    costs 2.57 on a personal axis, 2.27 on an additive one and 1.51 on a complementary one,
    because a partner can cover a complementary hole and cannot cover a personal one. It also
    prices *rarity*: an axis the pool is short of costs more to lack, with no rarity table.

    `score_pair(va, vb) -> float`. Returns `[(id, value)]`, best first.
    """
    out = []
    for vid, vec, _merged in variants:
        s = sorted((score_pair(vec, p) for pid, p, _m in pool if pid != vid), reverse=True)
        out.append((vid, sum(s[:k]) / max(1, len(s[:k]))))
    return sorted(out, key=lambda t: -t[1])


def pick(ranked, variants, limit, eps=1):
    """Top `limit` by value, skipping any variant eps-dominated by one already picked.

    Value order alone can spend every slot on the same shape. The guard is deliberately weak —
    a variant is dropped only if another already-picked one beats it by `eps` on *every* axis,
    which in ten dimensions is rare and means "strictly the same body, but worse".
    """
    vecs = {vid: vec for vid, vec, _ in variants}
    kept = []
    for vid, val in ranked:
        v = vecs[vid]
        if any(all(vecs[o][i] >= v[i] + eps for i in range(len(v))) for o, _ in kept):
            continue
        kept.append((vid, val))
        if len(kept) >= limit:
            break
    return kept
