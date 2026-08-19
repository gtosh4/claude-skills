"""Shared scoring for the Listonomicon skills.

Implements ``references/scoring-model.md``. That file is the spec; this is the
only implementation. Renderers import from here and must not reimplement any of
it — three divergent copies is exactly the drift the spec exists to stop.

Everything with special handling FAILS CLOSED: an unrecognised axis kind, ability,
booster or reach raises ``ScoringError`` rather than being skipped. A skipped
booster contributes nothing, so the score lands too low, and a score that is too
low is indistinguishable from an honest one.
"""


class ScoringError(ValueError):
    """An authored value the model cannot score. Never swallow this."""


def _require(cond, msg):
    if not cond:
        raise ScoringError(msg)


# ── axes ─────────────────────────────────────────────────────────────────────
# Order is fixed and shared with every schema. Control is two axes.
KEYS = ["st", "aoe", "dur", "act", "ctrl_s", "ctrl_a", "rsc", "skl", "sav", "end"]
LABELS = ["Single-target", "AoE", "Durability", "Action economy",
          "Control (single)", "Control (area)", "Rescue", "Skills",
          "Saves", "Endurance"]
AXES = ["Single", "AoE", "Durab.", "Actions", "Ctrl-S", "Ctrl-A",
        "Rescue", "Skills", "Saves", "Endur."]
SAV_IDX = KEYS.index("sav")

KINDS = {"st": "add", "aoe": "add", "dur": "per", "act": "comp",
         "ctrl_s": "comp", "ctrl_a": "comp", "rsc": "comp", "skl": "comp",
         "sav": "per", "end": "per"}
KIND_MAX = {"add": 10, "comp": 7, "per": 5}
KINDNAME = {"add": "Additive", "comp": "Complementary", "per": "Personal"}

# Blocks. `act` is in none of them — it caps tempo rather than contributing.
TEMPO = ["st", "aoe", "ctrl_s", "ctrl_a"]
RESILIENCE = ["dur", "sav", "rsc"]
DURATION = ["end"]
UTILITY = ["skl"]

ACTS = ("I", "II", "III")
BANDS = ["3–8", "9–15", "16–20"]
MIX = {"I": (0.70, 0.30), "II": (0.60, 0.40), "III": (0.50, 0.50)}

REACH = {"ranged": (1.00, 1.00), "hybrid": (0.95, 0.95),
         "mobile": (0.95, 1.00), "static": (0.85, 0.90)}
REACH_LABEL = {"ranged": "ranged", "hybrid": "melee + ranged option",
               "mobile": "mobile melee", "static": "static melee"}
ROLES = ("carry", "support")

# Fight-type coefficients (crowd, boss). AoE/ST derived; the rest provisional.
FIGHT = {"aoe": (1.00, 0.25), "st": (0.50, 1.00),
         "ctrl_a": (1.00, 0.20), "ctrl_s": (0.30, 1.00),
         "rsc": (0.50, 1.00)}

# Provisional — see scoring-model.md §8. Tempo axes are not weighted here.
WEIGHTS = {"sav": 3.0, "skl": 2.5, "end": 2.0, "dur": 2.0, "rsc": 1.5}

# Provisional — scoring-model.md §6. Lone Wolf already meets four-body parity,
# so the cap clips a pair below baseline and barely rewards one above it.
ACTION_BASELINE = 4.0
ACTION_FLOOR = 0.75

FLAG = 3.0      # an idle body, in a fight type worth >=40% of the act

ABILITIES = ("str", "dex", "con", "int", "wis", "cha")
KEY_SAVES = frozenset(("wis", "con", "dex"))
# scope: "self" applies to this body, "pair" applies to both and does not stack.
BOOSTERS = {"brutish-durability": {"scope": "self", "blanket": True},
            "war-caster":         {"scope": "self", "blanket": True},
            "aura-of-protection": {"scope": "pair", "blanket": True}}


# ── combining ────────────────────────────────────────────────────────────────
def combine_axis(x, y, kind):
    """Two bodies -> one pair value, on the raw authored 0-5 scale.

    Complementary is uncapped: capping at 5 makes 5+4 and 5+0 identical, which
    reintroduces the saturation that made a plain maximum wrong.
    """
    if kind == "add":
        return x + y
    if kind == "comp":
        return max(x, y) + min(x, y) // 2
    if kind == "per":
        return min(x, y)
    raise ScoringError(f"unknown axis kind {kind!r}")


def combine(a, b):
    return {ax: combine_axis(a[i], b[i], KINDS[ax]) for i, ax in enumerate(KEYS)}


def norm(ax, value):
    """Combined value -> 0..1 against that axis kind's own maximum."""
    return value / KIND_MAX[KINDS[ax]]


# ── saves are derived from the authored set, never authored directly ─────────
def _validate_saves_block(block, who, act):
    _require(isinstance(block, dict), f"{who} {act}: saves block must be an object")
    for field in ("prof", "boosters"):
        _require(field in block, f"{who} {act}: saves block missing {field!r}")
    prof = block["prof"]
    for a in prof:
        _require(a in ABILITIES,
                 f"{who} {act}: unknown ability {a!r} — expected one of {ABILITIES}")
    _require(len(set(prof)) == len(prof),
             f"{who} {act}: duplicate ability in prof {prof!r} — record the union after "
             "de-duplication, so overlapping grants correctly count once")
    for b in block["boosters"]:
        _require(b in BOOSTERS,
                 f"{who} {act}: unknown booster {b!r} — add it to BOOSTERS with an "
                 "implemented effect before authoring it")


def derive_saves(prof, boosters, concentration):
    """scoring-model.md / ledger-schema.md rung table. Returns 0-5.

    Validates its own inputs: this is a public entry point, and an unrecognised
    ability or booster silently contributing nothing is the one failure mode the
    model cannot detect downstream.
    """
    for a in prof:
        _require(a in ABILITIES,
                 f"unknown ability {a!r} — expected one of {ABILITIES}")
    _require(len(set(prof)) == len(prof), f"duplicate ability in prof {prof!r}")
    for b in boosters:
        _require(b in BOOSTERS, f"unknown booster {b!r}")
    s = set(prof)
    n, nkey = len(s), len(s & KEY_SAVES)
    blanket = any(BOOSTERS[b]["blanket"] for b in boosters)
    covers_key = KEY_SAVES <= s

    if n >= 6:
        v = 5
    elif n >= 4 and covers_key and blanket:
        v = 5
    elif (n >= 4 and covers_key) or blanket:
        v = 4
    elif n == 4 and nkey >= 2:
        v = 3
    elif n == 3 and nkey >= 1:
        v = 2
    elif n == 2 and nkey >= 1:
        v = 1
    else:
        v = 0

    # A body holding the pair's one control spell without a Constitution save is
    # structurally fragile regardless of what else it is proficient in.
    if concentration and "con" not in s:
        v = min(v, 3)
    return v


def saves_pair(ca, cb, act):
    """Derive both bodies' saves for one act, applying pair-scope boosters.

    Aura of Protection raises BOTH bodies, so it is applied before the Personal
    `min`. Auras do not stack — a second one is dropped with a named warning.
    """
    warnings = []
    blocks, out = {}, {}
    for who, c in (("a", ca), ("b", cb)):
        blk = c["saves"][act]
        _validate_saves_block(blk, c["_id"], act)
        blocks[who] = blk

    pair_src = [w for w in ("a", "b")
                if any(BOOSTERS[x]["scope"] == "pair" for x in blocks[w]["boosters"])]
    if len(pair_src) > 1:
        warnings.append(
            f"both {ca['_id']} and {cb['_id']} bring a pair-scope booster "
            "(aura-of-protection). Auras do not stack — the second is ignored, and "
            "six levels are being wasted.")
    shared = [x for x in blocks[pair_src[0]]["boosters"]
              if BOOSTERS[x]["scope"] == "pair"] if pair_src else []

    for who, c in (("a", ca), ("b", cb)):
        blk = blocks[who]
        boosters = list(dict.fromkeys(list(blk["boosters"]) + shared))
        out[who] = derive_saves(blk["prof"], boosters, c.get("concentration", False))
    return out["a"], out["b"], warnings


# ── delivered damage ─────────────────────────────────────────────────────────
def utilisation(sc, reach):
    """Damage one body actually delivers, as (crowd, boss).

    The reach discount applies to the single-target term only — that is the
    damage a melee body has to walk to. Area is already priced into the AoE score.
    """
    rc, rp = REACH[reach]
    st, aoe = sc[KEYS.index("st")], sc[KEYS.index("aoe")]
    return [aoe * FIGHT["aoe"][0] + FIGHT["st"][0] * st * rc,
            aoe * FIGHT["aoe"][1] + FIGHT["st"][1] * st * rp]


# Theoretical ceilings, used to put damage and control on a common 0..1 scale.
_DMG_CROWD_MAX = 2 * (5 * FIGHT["aoe"][0] + FIGHT["st"][0] * 5)
_DMG_BOSS_MAX = 2 * (5 * FIGHT["aoe"][1] + FIGHT["st"][1] * 5)
_CTL_CROWD_MAX = KIND_MAX["comp"] * (FIGHT["ctrl_a"][0] + FIGHT["ctrl_s"][0])
_CTL_BOSS_MAX = KIND_MAX["comp"] * (FIGHT["ctrl_a"][1] + FIGHT["ctrl_s"][1])


def action_factor(act_pair):
    """Actions caps tempo rather than adding to it (scoring-model.md §6)."""
    return ACTION_FLOOR + (1.0 - ACTION_FLOOR) * min(1.0, act_pair / ACTION_BASELINE)


# ── validation ───────────────────────────────────────────────────────────────
def validate_chassis(cid, c):
    _require(c.get("role") in ROLES,
             f"{cid}: unknown role {c.get('role')!r} — expected one of {ROLES}")
    _require(c.get("reach") in REACH,
             f"{cid}: unknown reach {c.get('reach')!r} — expected one of {tuple(REACH)}")
    _require("saves" in c, f"{cid}: missing `saves` block — saves is derived, not authored")
    for act in ACTS:
        _require(act in c.get("scores", {}), f"{cid}: scores missing act {act}")
        _require(act in c["saves"], f"{cid}: saves block missing act {act}")
        row = c["scores"][act]
        _require(len(row) == len(KEYS),
                 f"{cid} {act}: scores has {len(row)} entries, expected {len(KEYS)} "
                 f"({', '.join(KEYS)})")
        _require(row[SAV_IDX] is None,
                 f"{cid} {act}: index {SAV_IDX} (saves) must be null — it is derived "
                 "from the `saves` block, never authored")
        for i, v in enumerate(row):
            if i == SAV_IDX:
                continue
            _require(isinstance(v, int) and 0 <= v <= 5,
                     f"{cid} {act}: {KEYS[i]} is {v!r}, expected an integer 0-5")


# ── the score ────────────────────────────────────────────────────────────────
def score(C, a, b):
    """Pair score from a chassis map. Ids are injected as `_id`."""
    return score_bodies(dict(C[a], _id=a), dict(C[b], _id=b))


def score_bodies(ca, cb):
    """Pair score from two body dicts.

    Each needs `_id`, `reach`, `scores` (act -> 10 values, index 8 null),
    `saves` (act -> {prof, boosters}) and optionally `concentration`.
    """
    a, b = ca["_id"], cb["_id"]
    ra, rb = ca["reach"], cb["reach"]
    _require(ra in REACH, f"{a}: unknown reach {ra!r}")
    _require(rb in REACH, f"{b}: unknown reach {rb!r}")
    locked = ra in ("static", "mobile") and rb in ("static", "mobile")

    rec = {"a": a, "b": b, "acts": {}, "locked": locked,
           "holes": set(), "flags": set(), "warnings": []}
    tempo_total = nontempo_total = 0.0

    for act in ACTS:
        sa = list(ca["scores"][act])
        sb = list(cb["scores"][act])
        va, vb, warns = saves_pair(ca, cb, act)
        sa[SAV_IDX], sb[SAV_IDX] = va, vb
        rec["warnings"] += warns

        pair = combine(sa, sb)
        wc, wb = MIX[act]

        ua, ub = utilisation(sa, ra), utilisation(sb, rb)
        if locked:
            ua[0] *= 0.9
            ub[0] *= 0.9
        dmg_crowd, dmg_boss = ua[0] + ub[0], ua[1] + ub[1]
        for who, u in ((a, ua), (b, ub)):
            if u[0] < FLAG and wc >= 0.40: rec["flags"].add((who, "crowd"))
            if u[1] < FLAG and wb >= 0.40: rec["flags"].add((who, "priority"))

        ctl_crowd = (pair["ctrl_a"] * FIGHT["ctrl_a"][0]
                     + pair["ctrl_s"] * FIGHT["ctrl_s"][0])
        ctl_boss = (pair["ctrl_a"] * FIGHT["ctrl_a"][1]
                    + pair["ctrl_s"] * FIGHT["ctrl_s"][1])

        crowd = (dmg_crowd / _DMG_CROWD_MAX + ctl_crowd / _CTL_CROWD_MAX) / 2
        boss = (dmg_boss / _DMG_BOSS_MAX + ctl_boss / _CTL_BOSS_MAX) / 2
        tempo = (wc * crowd + wb * boss) * action_factor(pair["act"])

        rsc_c, rsc_b = FIGHT["rsc"]
        adj = {ax: norm(ax, pair[ax]) for ax in RESILIENCE + DURATION + UTILITY}
        adj["rsc"] *= wc * rsc_c + wb * rsc_b
        nontempo = (sum(WEIGHTS[ax] * adj[ax] for ax in WEIGHTS)
                    / sum(WEIGHTS.values()))

        # display: collapse the two control axes to one act-appropriate spoke
        radar = dict(pair)
        radar["ctrl"] = wc * pair["ctrl_a"] + wb * pair["ctrl_s"]

        rec["acts"][act] = {"radar": radar, "pair": pair, "ua": ua, "ub": ub,
                            "crowd": crowd, "boss": boss, "tempo": tempo,
                            "nontempo": nontempo,
                            "dmg_crowd": dmg_crowd, "dmg_boss": dmg_boss}
        rec["holes"] |= {k for k in KEYS if norm(k, pair[k]) <= 0.40}
        tempo_total += tempo
        nontempo_total += nontempo

    rec["warnings"] = list(dict.fromkeys(rec["warnings"]))
    rec["tempo"] = tempo_total / len(ACTS)
    rec["nontempo"] = nontempo_total / len(ACTS)
    rec["score"] = round(50 * rec["tempo"] + 50 * rec["nontempo"], 1)
    rec["holes"] = sorted(rec["holes"], key=KEYS.index)
    return rec
