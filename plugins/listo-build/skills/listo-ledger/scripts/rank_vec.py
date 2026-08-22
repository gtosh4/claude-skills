#!/usr/bin/env python3
"""Array-vectorised pair scoring for the split search — the same score, computed all at once.

`score_bodies` costs ~120us and the search asks for it |frontier| x |pool| times: at 88,987
candidates against a 5,000-body pool that is 445 million calls, and the measured cost was 55
minutes on thirty-two cores. The arithmetic per call is tiny; the fifty-five minutes are Python
overhead. This restates the same computation as elementwise operations over a `(candidates, pool)`
block: the same sweep ranks in **5 minutes on one core**, and the whole script drops from ~60
minutes to 398 seconds, emitting a byte-identical `variants.json`.

One core, deliberately. The other thirty-one are idle and the chunks are independent, so a process
pool over them is there for the taking if five minutes ever stops being short enough.

**This is a second implementation of the scoring model, and `scoring.py` line 4 forbids exactly
that.** It cannot be the only one: the renderers need the whole record — per-act radars, blocks,
holes, flags, warnings, delivered damage per body — and this computes a scalar. So `score_bodies`
stays, this stays, and two things keep them from drifting apart. Neither is optional:

  * **No authored number is retyped.** Every constant — weights, cut-offs, fight coefficients,
    rung tables — is imported from `scoring.py`. What is restated here is control flow, not the
    model. A change to a coefficient reaches this file for free; a change to the *shape* of the
    model does not, and that is what the guard below is for.
  * **`--verify` cross-checks against `score_bodies` itself** on a random sample of the run's own
    bodies and aborts on any mismatch. There is no scoring test in the tree, so this is the only
    thing standing between a restated `min` and a silently wrong roster. It has already earned its
    place once — see `_nsum`.

Three branches of `score_bodies` are dead on this path and are asserted rather than implemented:
`to_chassis` emits no `types` (so `type_spread` is 1.0) and no `redirect` (so `redirect_pair` is
the identity), and `lead_order` only decides which body is presented first — the score is
symmetric, and only the score is read here. `_rung` reads only the probabilities, never the `sure`
flags, so those are not carried either.
"""
import collections
import numpy as np

import scoring as S

# Axis positions. KEYS order is fixed and shared with every schema, so unpacking it is safe.
I_ST, I_AOE, I_DUR, I_ACT, I_CS, I_CA, I_RSC, I_SKL, I_SAV, I_END = range(len(S.KEYS))
DIV = [float(S.KIND_MAX[S.KINDS[k]]) for k in S.KEYS]
# Insertion order of WEIGHTS, so the weighted sum accumulates in the same order `score_bodies` does.
W_AX = list(S.WEIGHTS)
W_SUM = sum(S.WEIGHTS.values())
PAIR_SCOPE = frozenset(k for k, v in S.BOOSTERS.items() if v["scope"] == "pair")

# Candidates per block. At a 5,000-body pool this is ~1.3M pairs, and the widest intermediate —
# the per-gate odds, which carry a third axis — stays around 50MB.
CHUNK = 256

Feat = collections.namedtuple(
    "Feat", "n rung rc rp locked cls sig pm savtab gidx parr ids")


def _require(cond, msg):
    if not cond:
        raise S.ScoringError(msg)


def build(bodies):
    """Per-body feature arrays. `bodies` are chassis dicts carrying a real `_id`.

    Everything the pair score reads off ONE body is precomputed here, including the two things
    that look like they need the partner:

      * **Saves.** `saves_pair` hands each body the union of both bodies' pair-scope boosters, and
        a body already holds its own — so its rung is a function of its own block and of the
        PARTNER'S pair-scope set alone. There are seven such boosters and only a handful of
        combinations occur, so the rung is tabulated over (own block) x (partner's pair mask) and
        the pair score becomes a gather.
      * **Skills.** `_gate_odds` folds the class-gated routes in per body, and `_rung` reads only
        the probabilities. So one vector of per-gate odds per body per act is all the pair needs.

    Both tables are built over DISTINCT signatures rather than over bodies: 89k bodies share a few
    hundred save blocks and skill maps between them.
    """
    n = len(bodies)
    rung = np.zeros((n, len(S.ACTS), len(S.KEYS)), np.int16)
    rc = np.zeros(n)
    rp = np.zeros(n)
    locked = np.zeros(n, bool)

    sigs, sig_of = [], {}                 # distinct (prof, boosters, concentration)
    masks, mask_of = [], {}               # distinct partner-side pair-scope sets
    sig = np.zeros((n, len(S.ACTS)), np.int32)
    pm = np.zeros((n, len(S.ACTS)), np.int32)
    gs = [([], {}) for _ in S.ACTS]       # distinct (skill map, classes) per act
    gidx = np.zeros((n, len(S.ACTS)), np.int32)
    cls_bit, cls = {}, np.zeros(n, np.int64)

    for bi, c in enumerate(bodies):
        _require(c["reach"] in S.REACH, f"{c['_id']}: unknown reach {c['reach']!r}")
        _require(not c.get("types"), f"{c['_id']}: `types` is set; this path assumes none")
        _require(not c.get("redirect"), f"{c['_id']}: `redirect` is set; this path assumes none")
        rc[bi], rp[bi] = S.REACH[c["reach"]]
        locked[bi] = c["reach"] in ("static", "mobile")
        conc = bool(c.get("concentration", False))
        split_classes = S._classes(c.get("split", ""))
        for name in split_classes:
            if name not in cls_bit:
                cls_bit[name] = 1 << len(cls_bit)
            cls[bi] |= cls_bit[name]
        for ai, act in enumerate(S.ACTS):
            row = c["scores"][act]
            _require(len(row) == len(S.KEYS), f"{c['_id']} {act}: scores has {len(row)} entries")
            rung[bi, ai] = [0 if v is None else v for v in row]

            blk = c["saves"][act]
            S._validate_saves_block(blk, c["_id"], act)
            k = (tuple(blk["prof"]), tuple(blk["boosters"]), conc)
            if k not in sig_of:
                sig_of[k] = len(sigs)
                sigs.append(k)
            sig[bi, ai] = sig_of[k]
            mk = frozenset(x for x in blk["boosters"] if x in PAIR_SCOPE)
            if mk not in mask_of:
                mask_of[mk] = len(masks)
                masks.append(mk)
            pm[bi, ai] = mask_of[mk]

            mods = (c.get("skills") or {}).get(act, {})
            bad = S._skills_block_bad(tuple(sorted(mods)))
            _require(bad is None, f"{c['_id']} {act}: unknown skill {bad!r}")
            gk = (tuple(sorted(mods.items())), tuple(sorted(split_classes)))
            store, seen = gs[ai]
            if gk not in seen:
                seen[gk] = len(store)
                store.append(S._gate_odds_cached(mods, act, split_classes))
            gidx[bi, ai] = seen[gk]

    # (own block) x (partner's pair-scope set) -> rung. `derive_saves` is set-semantic, so the
    # union may be taken in any order; it is taken in the body's own order to match `saves_pair`.
    savtab = np.zeros((len(sigs), len(masks)), np.int16)
    for si, (prof, boos, conc) in enumerate(sigs):
        for mi, mk in enumerate(masks):
            extra = [x for x in sorted(mk) if x not in boos]
            savtab[si, mi] = S.derive_saves(prof, list(boos) + extra, conc)

    # Per-act odds tables. Acts have different gate counts (5 / 4 / 3), so they stay separate.
    parr = [np.array([[p for _sure, p in row] for row in store], np.float64)
            for store, _seen in gs]

    ids = np.array([c["_id"] for c in bodies], dtype=object)
    return Feat(n, rung, rc, rp, locked, cls, sig, pm, savtab, gidx, parr, ids)


def _nsum(terms):
    """`sum(terms)` reproduced bit-for-bit — which is not the same as adding them up.

    CPython's `sum` has run **Neumaier compensated summation** over floats since 3.12, and
    `scoring.py` sums Python floats. `ndarray.sum` and a plain running total do not: on four gate
    odds, `0.0 + 0.5 + 0.525 + 0.575` is 1.6 compensated and 1.5999999999999999 uncompensated.
    `SKL_CUTS` tests `mean >= 0.40`, so that last bit decides a rung and a rung is 0.76 of a pair
    score. This was six disagreements in four thousand sampled pairs before it was carried here.

    Sequences are 3-10 long, so the compensation costs nothing worth measuring.
    """
    it = iter(terms)
    s = next(it) + 0.0                  # `0.0 + x` is exact, so the first term needs no correction
    c = np.zeros_like(s)
    for x in it:
        t = s + x
        c = c + np.where(np.abs(s) >= np.abs(x), (s - t) + x, (x - t) + s)
        s = t
    return s + c


def _last_axis(a):
    return (a[..., g] for g in range(a.shape[-1]))


def _skl_rung(pm_):
    """`_rung` over the pair's per-gate odds. `sure` is not read by `_rung`, so it is not carried."""
    mean = _nsum(_last_axis(pm_)) / pm_.shape[-1]
    worst = pm_.min(-1)
    r = np.zeros(mean.shape, np.int16)
    for cut, v in S.SKL_CUTS[::-1]:          # ascending cut, so the highest reached rung survives
        r = np.where(mean >= cut, np.int16(v), r)
    r = np.where(worst < S.SKL_DEAD, np.minimum(r, np.int16(2)),
                 np.where(worst < S.SKL_WEAK, np.minimum(r, np.int16(3)), r))
    return r


def score_block(F, ci, pi):
    """`(len(ci), len(pi))` pair scores — `score_bodies(...)["score"]` for every combination."""
    tempo_t = None
    non_t = None
    for ai, act in enumerate(S.ACTS):
        A = F.rung[ci, ai].astype(np.int32)          # (c, 10)
        B = F.rung[pi, ai].astype(np.int32)          # (p, 10)
        av = [A[:, k][:, None] for k in range(len(S.KEYS))]
        bv = [B[:, k][None, :] for k in range(len(S.KEYS))]

        def comp(x, y):
            return np.maximum(x, y) + np.minimum(x, y) // 2

        sav_a = F.savtab[F.sig[ci, ai][:, None], F.pm[pi, ai][None, :]]
        sav_b = F.savtab[F.sig[pi, ai][None, :], F.pm[ci, ai][:, None]]

        pa = F.parr[ai][F.gidx[ci, ai]]              # (c, G)
        pb = F.parr[ai][F.gidx[pi, ai]]              # (p, G)
        p_skl = _skl_rung(np.maximum(pa[:, None, :], pb[None, :, :]))

        p_st = av[I_ST] + bv[I_ST]
        p_aoe = av[I_AOE] + bv[I_AOE]
        p_dur = np.minimum(av[I_DUR], bv[I_DUR])
        p_end = np.minimum(av[I_END], bv[I_END])
        p_act = comp(av[I_ACT], bv[I_ACT])
        p_cs = comp(av[I_CS], bv[I_CS])
        p_ca = comp(av[I_CA], bv[I_CA])
        p_rsc = comp(av[I_RSC], bv[I_RSC])
        p_sav = np.minimum(sav_a, sav_b)

        wc, wb = S.MIX[act]
        fa_c, fa_b = S.FIGHT["aoe"]
        fs_c, fs_b = S.FIGHT["st"]
        ua0 = av[I_AOE] * fa_c + fs_c * av[I_ST] * F.rc[ci][:, None]
        ua1 = av[I_AOE] * fa_b + fs_b * av[I_ST] * F.rp[ci][:, None]
        ub0 = bv[I_AOE] * fa_c + fs_c * bv[I_ST] * F.rc[pi][None, :]
        ub1 = bv[I_AOE] * fa_b + fs_b * bv[I_ST] * F.rp[pi][None, :]
        lock = F.locked[ci][:, None] & F.locked[pi][None, :]
        ua0 = np.where(lock, ua0 * 0.9, ua0)
        ub0 = np.where(lock, ub0 * 0.9, ub0)

        dmg_crowd = ua0 + ub0
        dmg_boss = ua1 + ub1
        ctl_crowd = p_ca * S.FIGHT["ctrl_a"][0] + p_cs * S.FIGHT["ctrl_s"][0]
        ctl_boss = p_ca * S.FIGHT["ctrl_a"][1] + p_cs * S.FIGHT["ctrl_s"][1]
        crowd = (dmg_crowd / S._DMG_CROWD_MAX + ctl_crowd / S._CTL_CROWD_MAX) / 2
        boss = (dmg_boss / S._DMG_BOSS_MAX + ctl_boss / S._CTL_BOSS_MAX) / 2

        # A flagged body idles in that fight type, so the pair fights it a body down — charged on
        # that term only, and only in an act where the term is worth >=40%.
        if wc >= 0.40:
            idle_c = (ua0 < S.FLAG).astype(np.int32) + (ub0 < S.FLAG).astype(np.int32)
            crowd = crowd * S.IDLE_BODY ** idle_c
        if wb >= 0.40:
            idle_b = (ua1 < S.FLAG).astype(np.int32) + (ub1 < S.FLAG).astype(np.int32)
            boss = boss * S.IDLE_BODY ** idle_b

        af = S.ACTION_FLOOR + (1.0 - S.ACTION_FLOOR) * np.minimum(1.0, p_act / S.ACTION_BASELINE)
        tempo = (wc * crowd + wb * boss) * af

        adj_dur = p_dur / DIV[I_DUR]
        adj_sav = p_sav / DIV[I_SAV]
        adj_rsc = p_rsc / DIV[I_RSC]
        adj_end = p_end / DIV[I_END]
        adj_skl = p_skl / DIV[I_SKL]
        adj_rsc = adj_rsc * (wc * S.FIGHT["rsc"][0] + wb * S.FIGHT["rsc"][1])
        lone = np.minimum(av[I_RSC], bv[I_RSC]) == 0
        adj_rsc = np.where(lone, adj_rsc * S.LONE_RESCUE, adj_rsc)

        # A hole is an axis the PAIR cannot answer, charged to that axis's block, in this act only.
        h = {}
        for i, v in ((I_ST, p_st), (I_AOE, p_aoe), (I_DUR, p_dur), (I_ACT, p_act),
                     (I_CS, p_cs), (I_CA, p_ca), (I_RSC, p_rsc), (I_SKL, p_skl),
                     (I_SAV, p_sav), (I_END, p_end)):
            h[i] = v / DIV[i] <= 0.40
        n_tempo = sum(h[i].astype(np.int32) for i in (I_ST, I_AOE, I_CS, I_CA, I_ACT))
        tempo = tempo * S.HOLE ** n_tempo
        adj_dur = np.where(h[I_DUR], adj_dur * S.HOLE, adj_dur)
        adj_sav = np.where(h[I_SAV], adj_sav * S.HOLE, adj_sav)
        adj_rsc = np.where(h[I_RSC], adj_rsc * S.HOLE, adj_rsc)
        adj_end = np.where(h[I_END], adj_end * S.HOLE, adj_end)
        adj_skl = np.where(h[I_SKL], adj_skl * S.HOLE, adj_skl)

        adj = {"dur": adj_dur, "sav": adj_sav, "rsc": adj_rsc, "end": adj_end, "skl": adj_skl}
        nontempo = _nsum(S.WEIGHTS[ax] * adj[ax] for ax in W_AX) / W_SUM

        tempo_t = tempo if tempo_t is None else tempo_t + tempo
        non_t = nontempo if non_t is None else non_t + nontempo

    n = len(S.ACTS)
    same = (F.cls[ci][:, None] & F.cls[pi][None, :]) != 0
    sc = (50 * (tempo_t / n) + 50 * (non_t / n)) * np.where(same, S.SAME_CLASS, 1.0)
    return np.round(sc, 1)


def rank(F, ci, pi, top=10, chunk=CHUNK, progress=None):
    """`[(index_into_ci, value)]` — each candidate's mean over its `top` best partners.

    A candidate that is also in the pool must not partner with itself, which is the one place the
    block is not a plain outer product. Its own column is driven to -inf rather than dropped, so
    every row keeps the same width and the block stays rectangular.
    """
    _require(len(pi) > top, f"pool of {len(pi)} is not larger than top-{top}")
    order = {v: i for i, v in enumerate(F.ids[pi])}
    self_col = np.array([order.get(v, -1) for v in F.ids[ci]], np.int64)
    out = []
    for s in range(0, len(ci), chunk):
        M = score_block(F, ci[s:s + chunk], pi)
        col = self_col[s:s + chunk]
        hit = np.nonzero(col >= 0)[0]
        if len(hit):
            M[hit, col[hit]] = -np.inf
        # Descending top-`top`, then summed in that order, so the mean accumulates exactly as the
        # scalar path's `sum(sorted(...)[:top])` does. Exactness matters here for the same reason
        # it does in `_nsum`: composed rungs are coarse integers, so ranked values tie often, and a
        # last-bit disagreement reorders ties that `CO.pick` then selects from.
        part = -np.partition(-M, top - 1, axis=1)[:, :top]
        part = -np.sort(-part, axis=1)
        out += [(s + i, float(v)) for i, v in enumerate(_nsum(_last_axis(part)) / top)]
        if progress:
            progress(min(s + chunk, len(ci)), len(ci))
    return out


def verify(F, bodies, n, seed=0):
    """Cross-check `score_block` against `score_bodies` on `n` random pairs.

    Returns `[(i, j, vectorised, reference)]` for every disagreement. The vectorised path is a
    second implementation of a model whose own docstring forbids second implementations, and
    nothing else in the tree scores anything, so this is the whole guard.
    """
    rng = np.random.default_rng(seed)
    ii = rng.integers(0, F.n, n)
    jj = rng.integers(0, F.n, n)
    # `score_block` is an outer product, so the sampled pairs are its diagonal. Taken in blocks:
    # the wasted off-diagonal work is bounded by the block size and the code stays the code under
    # test, rather than a special-cased variant of it that could differ from what the run uses.
    got = np.concatenate([np.diagonal(score_block(F, ii[s:s + 128], jj[s:s + 128]))
                          for s in range(0, n, 128)])
    bad = []
    for k in range(n):
        want = S.score_bodies(dict(bodies[int(ii[k])]), dict(bodies[int(jj[k])]))["score"]
        if float(got[k]) != float(want):
            bad.append((int(ii[k]), int(jj[k]), float(got[k]), float(want)))
    return bad
