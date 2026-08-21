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
import concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "listo-build", "scripts"))
import compose as CO                                              # noqa: E402
import seed_index as SI                                           # noqa: E402
from scoring import (KEYS, SAV_IDX, KEY_SAVES, derive_saves,       # noqa: E402
                     derive_skills, score_bodies, _gate_odds_cached)

MIN_PRIMARY = 11          # a majority of twenty; below this the subclass is not the subject
MAX_CLASSES = 3
ACTS = ("I", "II", "III")

# `to_chassis` overwrites both of these before anything is scored — Saves from the proficiency set,
# Skills from the modifier map — so the rungs `compose` produced for them are dead weight in a
# domination test and only block culls that should have happened.
DOM_IDX = [i for i, k in enumerate(KEYS) if k not in ("sav", "skl")]


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


def _saves_key(prof):
    """The only four things `derive_saves` reads off a proficiency set.

    It asks how many abilities are covered, how many of Wisdom / Constitution / Dexterity are
    among them, whether all three are, and whether Constitution is there to lift the
    concentration clamp. Boosters are the other input and are fixed per subclass, so within one
    subclass the save rung is a function of exactly these four numbers — and, since the rung table
    is monotone, a variant behind on all four can never out-save one ahead on them.

    This is what replaced grouping on the proficiency set itself. Equality forbade domination
    between `{str, dex}` and `{int, cha}`, which are set-incomparable and yet plainly ordered here:
    `(2, 1, 0, 0)` against `(2, 0, 0, 0)`.
    """
    s = set(prof)
    return [len(s), len(s & KEY_SAVES), int(KEY_SAVES <= s), int("con" in s)]


def _gates_key(meta):
    """Per-gate clear odds for all three acts — what `skills_pair` actually consumes.

    The pair takes the better body on each check: `(sa or sb, max(pa, pb))` per gate, then one
    rung off the mean. Both are monotone per gate, so domination on this vector is exactly
    domination on the skills axis. Raw modifiers were the key before, and they over-separated —
    a modifier past the top of a DC band buys no odds but still read as a bigger number and
    blocked the cull. The class set is folded in here too, since the gates are class-gated.
    """
    cls = frozenset(meta["classes"])
    sk = meta.get("skills") or {}
    return [x for a in ACTS
            for sure, p in _gate_odds_cached(sk.get(a) or {}, a, cls)
            for x in (int(sure), round(p, 3))]


def dom_key(vec, meta):
    """Every number the pair score reads off one body, in domination order."""
    return [vec[i] for i in DOM_IDX] + _saves_key(meta["prof"]) + _gates_key(meta)


def cull(vs, key):
    """`([(vid, vector, [merged_ids])], n_distinct)` — dedupe and frontier in one pass.

    Domination here is a partial order, not a partition. The previous version ran `CO.frontier`
    inside each exact `(prof, classes)` group, which is sound but blunt: two variants whose
    proficiency sets differ by a single ability could never cull each other however lopsided the
    rest of the comparison was. `dom_key` replaces both grouping columns with numbers the score
    genuinely reads, leaving one side condition that cannot be reduced to a number:

    **classes must be a SUBSET.** `same_class` charges a flat penalty when the pair shares a class,
    so a variant carrying fewer classes is penalised against fewer partners and can win from
    behind on the rungs. Subset domination closes that; it is the one place a set relation is
    still required, and it is the reason the cull stops where it does.

    Deduping on `dom_key` is also exact where the old key was not. `CO.dedupe` collapsed variants
    that composed to the same vector even when their `prof` differed — a documented approximation.
    Proficiency now enters through `_saves_key`, so two variants sharing a key really are
    indistinguishable to the scorer.
    """
    rows, seen = [], {}
    for lab, v, m in vs:
        vid = f"{key}::{lab}"
        k = (tuple(dom_key(v, m)), frozenset(m["classes"]))
        if k in seen:
            rows[seen[k]][2].append(vid)
            continue
        seen[k] = len(rows)
        rows.append((vid, list(v), [], k[0], k[1]))
    # Descending key sum, so a dominator is always seen before anything it dominates and each
    # candidate is tested against the kept frontier rather than the whole set.
    keep = []
    for r in sorted(rows, key=lambda r: -sum(r[3])):
        if any(kc <= r[4] and all(x >= y for x, y in zip(kk, r[3]))
               for _v, _vec, _m, kk, kc in keep):
            continue
        keep.append(r)
    order = {r[0]: i for i, r in enumerate(rows)}          # back to enumeration order
    keep.sort(key=lambda r: order[r[0]])
    return [(r[0], r[1], r[2]) for r in keep], len(rows)


def enumerate_for(key, base, cat, pbc, cls_of, sbc=None):
    """Every composed variant of one subclass, as `[(label, vector, meta)]`."""
    primary = cls_of[key]
    # The subclass half of the exit cost is keyed on this. `key` is `class/Subclass`, and the
    # subclass half is the only place a duo-dead capstone can be priced at nothing.
    primary_subclass = key.split("/", 1)[1] if "/" in key else None
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
                        primary_first=(first is None),
                        primary_subclass=primary_subclass)
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


def pair_value(a, b):
    try:
        return score_bodies(dict(a, _id="a"), dict(b, _id="b"))["score"]
    except Exception:
        return 0.0


# Ranking is `candidates x pool` pair scores and dwarfs everything else: enumerating and deduping
# four subclasses takes 22s, ranking them against an uncapped pool took 33 minutes. The pool is
# identical for every subclass and the subclasses do not see each other, so the loop is
# embarrassingly parallel — the pool is handed to each worker once by the initialiser rather than
# pickled per task, which at a thousand bodies is the difference that matters.
_POOL = None


def _init_worker(pool_ch):
    global _POOL
    _POOL = pool_ch


def stratify(per, cap):
    """`cap` bodies drawn evenly from every subclass's frontier, not from the concatenation.

    A stride over the concatenated frontier hands each subclass slots in proportion to how many
    variants its enumeration happened to produce — an artifact of how many dip breakpoints its
    primary class offers, not of how good a partner it makes. At the old thousand-body cap the
    step was 178 variants, so a subclass with a small frontier contributed one body or none, and
    no candidate was ever scored against it at all.

    Slots a small subclass cannot fill are handed back and shared out again, so the cap is always
    spent. Within a subclass the sample is still a stride over its own frontier.
    """
    keys = sorted(per)
    total = sum(len(per[k][0]) for k in keys)
    if not cap or total <= cap:
        return [v for k in keys for v in per[k][0]]
    avail = {k: len(per[k][0]) for k in keys}
    quota = {k: 0 for k in keys}
    left = cap
    while left:
        hungry = [k for k in keys if quota[k] < avail[k]]
        if not hungry:
            break
        share = max(1, left // len(hungry))
        for k in hungry:
            take = min(share, avail[k] - quota[k], left)
            quota[k] += take
            left -= take
            if not left:
                break
    out = []
    for k in keys:
        d, n = per[k][0], quota[k]
        if not n:
            continue
        step = len(d) / n
        out += [d[int(i * step)] for i in range(n)]
    return out


def _rank_one(task):
    key, cand = task
    ranked = []
    for vid, ch in cand:
        s = sorted((pair_value(ch, pc) for pid, pc in _POOL if pid != vid), reverse=True)
        ranked.append((vid, sum(s[:10]) / max(1, len(s[:10]))))
    ranked.sort(key=lambda t: -t[1])
    return key, ranked


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--limit", type=int, default=2, help="variants kept per subclass")
    ap.add_argument("--only", help="comma-separated subclass keys, for a smoke test")
    ap.add_argument("--pool-cap", type=int, default=5000,
                    help="bodies in the partner pool, drawn evenly from every subclass's "
                         "frontier; 0 = all, which is quadratic and takes hours")
    ap.add_argument("--jobs", type=int, default=0,
                    help="ranking workers; 0 = one per CPU, 1 = in-process")
    ap.add_argument("--ignore-verdicts", action="store_true",
                    help="enumerate every subclass with a base profile, including ones the sweep "
                         "rejected; for smoke tests only, never for a roster")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    doc = json.load(open(os.path.join(ASSETS, "subclass-bases.json")))
    cat = CO.load()
    bases = bases_for_compose(doc)
    inv = SI.inventory()
    cls_of = {f"{c}/{s}": c for c, subs in inv.items() for s in subs}
    keys = [k for k in bases if not a.only or k in a.only.split(",")]

    # The base profiles are keyed by subclass and know nothing about verdicts, so enumerating
    # straight off them resurrects every subclass the sweep already rejected — a `none` whose
    # features cannot be read, a `dupe` whose best body is another seed's, an `inquisitor` whose
    # level-3 subclass GUID dangles on the shipped install. Those variants rank like any other and
    # reach the scoring pass looking exactly like promoted work, which is the same invisible
    # failure the fail-closed doctrine exists to prevent: nothing downstream can tell that a body
    # was never supposed to be here. So the verdicts are read here, and what they drop is named.
    if not a.ignore_verdicts:
        seeds = SI.load(os.path.join(ASSETS, "chassis-seeds.json"))
        cand = {k for k, sd in seeds.items() if sd["verdict"] == "candidate"}
        dropped = [k for k in keys if k not in cand]
        keys = [k for k in keys if k in cand]
        if dropped:
            print(f"skipping {len(dropped)} subclass(es) the sweep did not promote:",
                  file=sys.stderr)
            for k in sorted(dropped):
                sd = seeds.get(k)
                why = f"{sd['verdict']}" if sd else "no seed"
                print(f"  {k} — {why}", file=sys.stderr)
        # A base profile with no seed at all is a real gap, not a rejection: `--check` never saw
        # it, so nobody decided anything about it. Fail rather than silently narrowing the roster.
        missing = [k for k in cand if k not in bases and (not a.only or k in a.only.split(","))]
        if missing:
            sys.exit(f"{len(missing)} promoted subclass(es) have no base profile: "
                     + ", ".join(sorted(missing)[:5]))
    pbc = parts_by_class(cat)
    sbc = subclasses_by_class(cat)

    per = {}
    raw = dist = 0
    for k in keys:
        vs = enumerate_for(k, bases[k], cat, pbc, cls_of, sbc)
        meta = {f"{k}::{lab}": m for lab, _v, m in vs}
        # Dominated variants cannot place above the variant dominating them — see `cull`. Ranking
        # is quadratic, so culling here is the difference between a run and an afternoon: measured
        # on cleric/Forge and wizard/Evocation it drops 14,152 raw to 1,554, half what the
        # `(prof, classes)` grouping kept, and takes a second.
        d, n = cull(vs, k)
        raw += len(vs)
        dist += n
        per[k] = (d, meta)
    front = sum(len(v) for v, _ in per.values())
    print(f"{len(keys)} subclasses -> {raw} raw, {dist} distinct after dedupe, "
          f"{front} on the frontier ({100 * (1 - front / max(1, dist)):.0f}% culled)",
          file=sys.stderr)

    # The pool is not the candidate set and must not scale with it: it stands in for "the space of
    # plausible partners". It is drawn from the frontier — a stride over raw variants spent most of
    # its slots on bodies that were dominated and could never have been anyone's best partner —
    # and it is capped, because ranking is |candidates| x |pool| and an uncapped pool is quadratic
    # in the frontier: at ~86k bodies that is 7.9 billion pair scores, about seven hours on
    # thirty-two cores against five minutes at a thousand. Peeling dominated bodies out of the pool
    # would be exact — a body with ten dominators can never enter anyone's top ten — but measured,
    # it removes nothing: two thirds of the pool is on the first skyline layer and all of it fits
    # in four, because at 36 dimensions with incomparable class and booster sets almost nothing
    # dominates anything. So the cap stands, and `stratify` decides how it is spent.
    pool = stratify(per, a.pool_cap)
    pool_ch = [(vid, to_chassis(v, per[vid.split("::")[0]][1][vid]["prof"],
                                bases[vid.split("::")[0]]["boosters"],
                                bases[vid.split("::")[0]]["concentration"],
                                skills=per[vid.split("::")[0]][1][vid]["skills"],
                                split=vid.split("::", 1)[1],
                                classes=per[vid.split("::")[0]][1][vid]["classes"]))
               for vid, v, _m in pool]
    slots = collections.Counter(vid.split("::")[0] for vid, _c in pool_ch)
    print(f"pool: {len(pool_ch)} bodies from {len(slots)}/{len(per)} subclasses, "
          f"{min(slots.values())}-{max(slots.values())} each", file=sys.stderr)

    tasks = [(k, [(vid, to_chassis(v, meta[vid]["prof"], bases[k]["boosters"],
                                   bases[k]["concentration"], skills=meta[vid]["skills"],
                                   split=vid.split("::", 1)[1],
                                   classes=meta[vid]["classes"])) for vid, v, _m in d])
             for k, (d, meta) in sorted(per.items())]

    jobs = a.jobs if a.jobs > 0 else (os.cpu_count() or 1)
    print(f"ranking {sum(len(c) for _k, c in tasks)} candidates against {len(pool_ch)} bodies "
          f"on {jobs} worker(s)", file=sys.stderr)
    results = {}
    if jobs == 1:
        _init_worker(pool_ch)
        done = (_rank_one(t) for t in tasks)
    else:
        ex = cf.ProcessPoolExecutor(max_workers=jobs, initializer=_init_worker,
                                    initargs=(pool_ch,))
        done = (f.result() for f in cf.as_completed([ex.submit(_rank_one, t) for t in tasks]))
    for i, (k, ranked) in enumerate(done, 1):
        results[k] = ranked
        if i % 20 == 0 or i == len(tasks):
            print(f"  ranked {i}/{len(tasks)}", file=sys.stderr)
    if jobs != 1:
        ex.shutdown()

    out = {}
    for k, (d, meta) in sorted(per.items()):
        kept = CO.pick(results[k], d, a.limit)
        out[k] = [{"id": vid, "value": round(val, 3), "split": vid.split("::", 1)[1],
                   "vector": next(v for x, v, _ in d if x == vid),
                   "meta": {kk: vv for kk, vv in meta[vid].items() if kk != "prof"}}
                  for vid, val in kept]
    if a.out:
        json.dump(out, open(a.out, "w"), indent=2, ensure_ascii=False)
    print(f"kept {sum(len(v) for v in out.values())} variants across {len(out)} subclasses",
          file=sys.stderr)
    return out


if __name__ == "__main__":
    main()
