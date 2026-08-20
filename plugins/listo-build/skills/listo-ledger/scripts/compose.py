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
import json, os, sys, itertools, functools

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "listo-build", "scripts"))
from scoring import (KEYS, SAV_IDX, ACTS, RECORDED_SKILLS,   # noqa: E402
                     derive_saves, derive_skills)

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


def fold_subclass(cat, pids):
    """Fold a subclass's rows at or below the dip's level into one `(grants, deltas, conflicts)`.

    A dip at level N gets everything the subclass has handed over by N, not only the row written
    at exactly N. Taking the row at N alone dropped Cleric 2 (Tempest)'s heavy armour — that grant
    lives on the level-1 row — and made Cleric 2 (Light) inexpressible outright, because Light had
    a row at 1 and none at 2.

    The operator on deltas is **MAX per axis, not sum**: the tables are written cumulatively —
    `wizard/2/Abjuration` is `dur 1`, `/6` is `dur 2`, `/11` is `dur 3` — so summing would charge
    the same Arcane Ward three times. Grants union forward, since only the shallowest row carries
    the domain's armour and the deeper rows do not repeat it.
    """
    grants = {"prof": set(), "armour": None, "shield": False, "skills": 0, "expertise": 0}
    deltas, conflicts, lists = {}, [], []
    for pid in pids:
        g, d, meta = _part(cat, pid, False)
        if g.get("skills") or g.get("expertise"):
            lists.append(g.get("skill_list"))
        grants["prof"] |= set(g.get("prof", []))
        if ARMOUR[g.get("armour")] > ARMOUR[grants["armour"]]:
            grants["armour"] = g.get("armour")
        grants["shield"] = grants["shield"] or bool(g.get("shield"))
        grants["skills"] += g.get("skills", 0)
        grants["expertise"] += g.get("expertise", 0)
        for k, x in d.items():
            deltas[k] = max(deltas.get(k, 0), x) if x >= 0 else min(deltas.get(k, 0), x)
        conflicts += meta.get("conflicts") or []
    grants["prof"] = sorted(grants["prof"])
    # One unrestricted row makes the whole fold unrestricted; otherwise the lists union.
    if lists and None not in lists:
        grants["skill_list"] = sorted({s for lst in lists for s in lst})
    return grants, deltas, {"conflicts": list(dict.fromkeys(conflicts)), "requires": None}


def compose(cat, base, parts, primary=None, primary_levels=20, concentration=False,
            primary_first=True, primary_ability=None):
    """`base` is the primary subclass's own 20-level vector + grants; `parts` are the dips.

    Each part is `(part_id, is_first)`, where `part_id` may also be a **tuple of ids** — a
    subclass's rows at every level up to the dip's, folded by `fold_subclass`.

    Returns `(vector, prof, picks)`. `picks` is the proficiency budget the dips buy, as
    `{"skills": [(class, n, allowed_or_None)], "expertise": [(allowed_or_None, n)]}` — per
    source, because a class may only spend its picks on its own list. `compose_skills` turns
    that into a modifier map.

    **Exactly one class in a build is the level-1 class**, and
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
    picks = {"skills": [], "expertise": []}
    for pid, first in parts:
        if isinstance(pid, (tuple, list)):
            grants, deltas, meta = fold_subclass(cat, pid)
            cls = pid[0].split("/")[0]
        else:
            grants, deltas, meta = _part(cat, pid, first)
            cls = pid.split("/")[0]
        # A grant may name its own list — Knowledge's double proficiency is four Intelligence
        # skills, not "any two" — otherwise the picks fall back to the class's level-1 list.
        if grants.get("skills"):
            picks["skills"].append((cls, grants["skills"], grants.get("skill_list")))
        if grants.get("expertise"):
            picks["expertise"].append((grants.get("skill_list"), grants["expertise"]))
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
    # The rows are written CUMULATIVELY from 20 — bard 17 is `rsc -2`, 14 is `rsc -2` again plus
    # more, 11 is `rsc -3` — so exactly ONE row applies, the deepest band the level falls into.
    # The old loop walked the keys downward taking every `primary_levels <= lvl` row, which both
    # summed the bands and read them backwards: Monk 14 paid the 17 row on top of its own and
    # came out at `st 0` instead of 1, biasing the whole search against low-primary splits.
    if primary and primary_levels < 20:
        table = cat["parts"].get("exit", {}).get(primary.lower().replace(" ", ""), {})
        bands = [lvl for lvl in sorted(int(x) for x in table) if lvl <= primary_levels]
        if bands:
            pending.append(table[str(bands[-1])])

    for d in pending + list(tagged.values()):
        for k, x in d.items():
            if k == "skl":
                continue    # Skills is DERIVED from modifiers by `compose_skills`, like Saves.
            v[k] = v[k] + x

    v["dur"] = max(v["dur"], ARMOUR_DUR[armour] + (1 if shield else 0))
    out = [max(0, min(5, round(v[k]))) for k in KEYS]
    out[SAV_IDX] = derive_saves(sorted(prof), [], concentration)
    return out, sorted(prof), picks


# ── the Skills axis, which the search used to be blind to ────────────────────
# `skills_pair` scores off MODIFIERS, not off the composed rung, so a variant handed no `skills`
# map contributed nothing to the axis and every split in the search tied on it. Skills carries
# weight 2.5 of 11 — 23% of the non-tempo half — and the variant brief calls it "the axis most
# often left at zero", so the filter was tying on exactly the thing it was meant to separate.
#
# What follows is FILTER-GRADE like every other number here, and deliberately crude about
# abilities: the primary is +5/+5/+6 by act and everything else is +0. What it is NOT crude about
# is REACHABILITY — which skills a split may spend its picks on. That is the part that decides the
# axis, because no background and no race grants Investigation and most class lists do not either.
SKILL_ABILITY = {
    "Acrobatics": "dex", "Athletics": "str", "Deception": "cha", "Intimidation": "cha",
    "Investigation": "int", "Medicine": "wis", "Perception": "wis", "Persuasion": "cha",
    "Religion": "int", "Sleight of Hand": "dex",
}
PROF_BY_ACT = {"I": 3, "II": 4, "III": 5}
PRIMARY_MOD = {"I": 5, "II": 5, "III": 6}
BEAM = 12
_SKILLS_CACHE = {}


def _mods(prof, expert, primary_ability, act):
    """The modifier map a set of proficiencies produces, for one act."""
    pb = PROF_BY_ACT[act]
    out = {}
    for sk in RECORDED_SKILLS:
        if sk not in SKILL_ABILITY:
            continue
        mod = PRIMARY_MOD[act] if SKILL_ABILITY[sk] == primary_ability else 0
        if sk in prof:
            mod += pb * (2 if sk in expert else 1)
        out[sk] = mod
    return out


@functools.lru_cache(maxsize=None)
def _skl_value(prof, expert, primary_ability, classes):
    return sum(derive_skills(_mods(prof, expert, primary_ability, a), a, classes) for a in ACTS)


def compose_skills(cat, budgets, primary_ability, classes, expertise=()):
    """A per-act skill modifier map for a composed split.

    `budgets` is `[(class_name, n_picks, allowed_or_None), ...]` — picks default to that class's
    own level-1 list, and a part may narrow them further (Knowledge Domain's double proficiency
    is Arcana/History/Nature/Religion only, not "any two skills"). `expertise` is the same shape
    without the class. A background pair and the race's Perception are added on top, because
    every body has both, and the pair is enumerated rather than assumed.
    """
    lists = cat.get("skill_lists", {})
    scored = frozenset(SKILL_ABILITY)
    classes = frozenset(classes)
    if isinstance(expertise, int):
        expertise = ((None, expertise),) if expertise else ()
    exp_budget = tuple((frozenset(a) & scored if a else scored, n) for a, n in expertise if n > 0)

    key = (id(cat), tuple(map(tuple, ((b[0], b[1], tuple(b[2]) if len(b) > 2 and b[2] else None)
                                      for b in budgets))),
           primary_ability, classes, exp_budget)
    if key in _SKILLS_CACHE:                      # 6.7k variants, a few dozen distinct budgets
        return _SKILLS_CACHE[key]

    left = []
    for entry in budgets:
        cls, n = entry[0], entry[1]
        allowed = entry[2] if len(entry) > 2 else None
        if n <= 0:
            continue
        pool = frozenset(allowed) if allowed else frozenset(lists.get(cls, ()))
        left.append((cls, n, pool & scored))
    left = tuple(left)

    best = None
    for _bg, pair in sorted(cat.get("backgrounds", {}).items()):
        start = frozenset({s for s in pair if s in scored}
                          | {s for s in cat.get("race_skills", []) if s in scored})
        # A BEAM, not a greedy walk. Investigation sits on a dumped Intelligence, so on its own
        # it buys nothing and only pays once Expertise lands on the same skill. A step-best
        # chooser never takes the first half of that pair, and so never reaches the second —
        # which loses the one skill most dips are actually bought for.
        beam = [(start, frozenset(), left, exp_budget)]
        for _step in range(sum(n for _c, n, _a in left) + sum(n for _a, n in exp_budget)):
            nxt = {}
            for prof, expert, rem, erem in beam:
                for i, (c, n, pool) in enumerate(rem):
                    for sk in pool - prof:
                        r = rem[:i] + ((c, n - 1, pool),) + rem[i + 1:]
                        nxt[(prof | {sk}, expert, tuple(x for x in r if x[1] > 0), erem)] = None
                for i, (pool, n) in enumerate(erem):
                    for sk in (prof & pool) - expert:
                        e = erem[:i] + ((pool, n - 1),) + erem[i + 1:]
                        nxt[(prof, expert | {sk}, rem,
                             tuple(x for x in e if x[1] > 0))] = None
            if not nxt:
                break
            # The tie-break is not decoration. `nxt` is keyed by tuples of frozensets, and
            # frozenset iteration order varies with PYTHONHASHSEED, so sorting on the rung alone
            # resolves ties differently every run — two runs of the same enumeration disagreed on
            # the distinct-variant count by 60. Order the names too and the search is reproducible.
            beam = sorted(nxt, key=lambda s: (-_skl_value(s[0], s[1], primary_ability, classes),
                                              sorted(s[0]), sorted(s[1])))[:BEAM]
        for prof, expert, _rem, _erem in beam:
            val = _skl_value(prof, expert, primary_ability, classes)
            if best is None or val > best[0]:
                best = (val, prof, expert)
    out = ({a: {} for a in ACTS} if best is None
           else {a: _mods(best[1], best[2], primary_ability, a) for a in ACTS})
    _SKILLS_CACHE[key] = out
    return out


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
