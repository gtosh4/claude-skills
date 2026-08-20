"""Shared scoring for the Listonomicon skills.

Implements ``references/scoring-model.md``. That file is the spec; this is the
only implementation. Renderers import from here and must not reimplement any of
it — three divergent copies is exactly the drift the spec exists to stop.

Everything with special handling FAILS CLOSED: an unrecognised axis kind, ability,
booster or reach raises ``ScoringError`` rather than being skipped. A skipped
booster contributes nothing, so the score lands too low, and a score that is too
low is indistinguishable from an honest one.
"""

import collections


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

# `skl` and `sav` are both DERIVED, and for opposite reasons. Saves are personal: each body rolls
# its own, so the pair is its weakest link. Skills are shared: the host is boosted to the party
# maximum, so the pair is its better half. Neither has a combining operator on the rung — the
# combination happens on the evidence (proficiency sets, skill modifiers) before a rung exists.
KINDS = {"st": "add", "aoe": "add", "dur": "per", "act": "comp",
         "ctrl_s": "comp", "ctrl_a": "comp", "rsc": "comp", "skl": "derived",
         "sav": "derived", "end": "per"}
KIND_MAX = {"add": 10, "comp": 7, "per": 5, "derived": 5}
KINDNAME = {"add": "Additive", "comp": "Complementary", "per": "Personal",
            "derived": "Derived from evidence"}

# Blocks. `act` is in none of them — it caps tempo rather than contributing.
BLOCKS = ("tempo", "resilience", "duration", "utility")
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

# Weaknesses used to be *reported* and never *priced*: `holes` and `flags` were collected into
# the record, printed as chips, and left out of the score entirely. The page could say "idles in
# crowd fights" directly above a rank-1 result the chip had not touched — and in the v5 roster
# every one of the top ten pairings carried a hole while the top chassis was flagged idle in all
# ten. Pairs sharing a primary class were 7% of the field and 24% of the top 25; melee-locked
# pairs 21% and 36%. Every penalty the model owned was over-represented at the top.
#
# Both factors are deliberately modest, because the raw effect is already partly counted: an idle
# body's zero damage is in the crowd sum, and a holed axis is in its block's average. What is NOT
# counted is structural — a fight type fought one body down, and a duo with no third character to
# cover a gap. These price that remainder and nothing more.
IDLE_BODY = 0.85    # per flagged body, on that fight type's term, in that act only
HOLE = 0.95         # per holed axis, on the block that axis belongs to

# ── gates: Skills is DERIVED, like Saves ─────────────────────────────────────
# `Use Highest Modifier in dialogue` reads every party member's total for all eighteen skills and
# boosts the roller to the party maximum, so a gate is cleared if EITHER body clears it. That is a
# max over modifiers, taken BEFORE any rung exists — which is why Skills has no combining operator
# any more. It is also why `hi + lo//2` was wrong: normalised against 7, a pair where one body
# cleared everything scored 0.71 while the host actually rolled at the party maximum.
#
# The bank is vanilla: four charges, each a full reroll (`gates.md`). Two rerolls turn a 45% check
# into 83%, which is what makes the >=90% rung reachable at all.
#
# Only gates with a DC recorded in `gates.md` are here. A gate whose DC is not documented is not
# invented — it is absent, and the rung says so.
# ── the checks the run actually makes ────────────────────────────────────────
# Two classes, and the split is the whole point of the axis.
#
# NAMED gates are telegraphed: you know they are coming, so you can prepare, and the Inspiration
# bank is worth spending. They are also the *weaker* half of the axis, because every one of them
# has a no-check route to the same ability-score reward — the Hag's Hair deal gives the hair and
# costs Mayrina, Araj can simply be killed and looted. What passing buys is the secondary prize
# (Mayrina's life, Araj alive for Unstable Blood), not the +1/+2.
#
# ROUTINE checks are not telegraphed. Traps fire, caches stay hidden and townspeople talk while
# you are wearing whatever build you are wearing. They cannot be prepared for, and that makes them
# the respec-proof half: a rented Withers build clears a named gate and is useless here.
#
# REMOVED, and why:
#   Mirror of Loss  — bg3.wiki documents respeccing into Rogue 11 / Knowledge Cleric 1 for
#                     Religion expertise, passing DC 25, then respeccing back "retaining the
#                     Mirror of Loss stat enhancement". A 100-gold check is not a chassis property.
#   Gauntlet trap   — fabricated. Perception DC 15 appears nowhere in references/gates.md. It was
#                     inflating Act I for 114 of 265 chassis against no source at all.
ROUTINE_DC = {"I": (10, 15), "II": (15, 18), "III": (18, 22)}   # backgrounds.md:104

# One route past a gate. `hi` > `lo` means a band of DCs, not a single check.
#   requires  classes that unlock this route; empty means anyone may take it
#   adv       rolled with advantage
Alt = collections.namedtuple("Alt", "skill lo hi requires adv")
Alt.__new__.__defaults__ = (frozenset(), False)


def _r(act):
    return ROUTINE_DC[act]

GATES = {
    act: [g for g in (
        # named, banked
        ("Hag's Hair", (Alt("Deception", 20, 20),
                        Alt("Intimidation", 15, 15, frozenset({"Fighter", "Barbarian"}), True),
                        Alt("Intimidation", 20, 20)), True) if act == "I" else None,
        ("Free Us", tuple(Alt(sk, 10, 10) for sk in
                          ("Investigation", "Medicine", "Athletics", "Acrobatics")), True)
        if act == "I" else None,
        ("Araj's potion", (Alt("Sleight of Hand", 20, 20),), True) if act == "II" else None,
        # routine, unbanked — the bank is four charges for a whole run and these are constant
        ("Traps and hidden caches", (Alt("Perception", 15, 25),), False),
        ("Secret doors and switches", (Alt("Investigation", 15, 20),), False),
        ("Town dialogue", (Alt("Persuasion", *_r(act)),), False),
    ) if g]
    for act in ("I", "II", "III")
}
GATE_SKILLS = sorted({a.skill for act in GATES.values() for _n, alts, _b in act for a in alts})
# Recorded on chassis but no longer scored. Religion's only gate was the Mirror; the field stays
# valid so the evidence pass does not have to be re-run to drop a column.
RECORDED_SKILLS = sorted(set(GATE_SKILLS) | {"Religion"})
# The routine checks decide every act, so an absent modifier on one of these is not "untrained" —
# it is missing evidence, and `mods.get(sk, -99)` would read it as hopeless. Named-gate skills stay
# optional: a body with neither Deception nor Intimidation genuinely cannot talk to Ethel.
REQUIRED_SKILLS = ("Perception", "Investigation", "Persuasion")

REROLLS = 2         # of the four banked charges, two is what a plan can count on


def _p_clear(mod, dc, rerolls=REROLLS):
    """Probability of clearing `dc` with `mod`, given `rerolls` full rerolls."""
    p = max(0.0, min(1.0, (21 - (dc - mod)) / 20))
    return 1 - (1 - p) ** (rerolls + 1)


def _alt_odds(mod, alt, rerolls):
    """`(sure, p)` for one route. A DC band is scored as the fraction of that band it clears."""
    dcs = range(alt.lo, alt.hi + 1)
    ps = []
    for dc in dcs:
        p = max(0.0, min(1.0, (21 - (dc - mod)) / 20))
        if alt.adv:
            p = 1 - (1 - p) ** 2
        ps.append(1 - (1 - p) ** (rerolls + 1))
    return mod >= alt.hi - 1, sum(ps) / len(ps)


def _gate_odds(mods, act, classes=None):
    """Per-gate `(sure, p)`, taking each gate's best available route.

    `classes` is the body's class set; a route with `requires` is unavailable without it. Passing
    None means "no class information", and every restricted route is then withheld — fail-closed,
    so an unknown body is never credited with the Fighter/Barbarian Intimidation discount.
    """
    out = []
    for _name, alts, banked in GATES.get(act, []):
        rr = REROLLS if banked else 0
        usable = [a for a in alts if not a.requires or (classes and a.requires & classes)]
        odds = [_alt_odds(mods.get(a.skill, -99), a, rr) for a in usable]
        out.append((any(s for s, _ in odds), max(p for _, p in odds)) if odds else (False, 0.0))
    return out


# Rung cut-offs on the pair's MEAN clear probability across the act's checks, plus caps keyed on
# its worst single check.
#
# An `all`-quantifier — "every check at >=90%" — is the natural reading and it was the first one
# implemented. It works over one or two homogeneous named gates and fails over a heterogeneous
# set: the hardest check binds every pair at once, and 72-86% of the field landed on rung 1. The
# axis carried a 2.5 weight and almost no information.
#
# The mean says how much of the act's check load the pair actually handles, which is the question.
# The caps keep what the all-quantifier was protecting: a check nobody can roll is a different
# failure from a check everyone rolls badly, and it must not average away.
#
# Rung 5 is unreachable, deliberately. The best pair in a 34,980-pairing field averages 0.79, and
# Perception against the 15-25 trap band peaks at 0.60 for anyone. **No two-character party covers
# this run's detection load.** That is a fact about Lone Wolf, not a gap in the scale.
SKL_CUTS = ((0.75, 5), (0.65, 4), (0.55, 3), (0.40, 2), (0.25, 1))
SKL_DEAD = 0.10     # a check this bad is one nobody can roll — rung 2 at best
SKL_WEAK = 0.25     # a check this bad still needs a plan — rung 3 at best


def _rung(odds):
    """Per-check `(sure, p)` -> a 0-5 rung."""
    if not odds:
        return 0
    ps = [p for _s, p in odds]
    mean, worst = sum(ps) / len(ps), min(ps)
    rung = next((v for cut, v in SKL_CUTS if mean >= cut), 0)
    if worst < SKL_DEAD:
        return min(rung, 2)
    if worst < SKL_WEAK:
        return min(rung, 3)
    return rung


def derive_skills(mods, act, classes=None):
    """One body's Skills rung. `mods` is `{skill: modifier}`."""
    for sk in mods:
        _require(sk in RECORDED_SKILLS,
                 f"unknown skill {sk!r} — expected one of {RECORDED_SKILLS}")
    return _rung(_gate_odds(mods, act, classes))


# ── damage-type redundancy ───────────────────────────────────────────────────
# Absolute Wrath puts layered resistances on ordinary enemies, and the rubric already caps a
# single body at 4 on `st` for one commonly-resisted type. The PAIR had no such rule: two bodies
# dealing the same resisted type still summed linearly. A duo with one damage type between them
# has no answer at all when that type is resisted, and that is a pair-level fact.
DAMAGE_TYPES = ("acid", "bludgeoning", "cold", "fire", "force", "lightning", "necrotic",
                "piercing", "poison", "psychic", "radiant", "slashing", "thunder")
TYPE_SPREAD = {1: 0.85, 2: 0.93}    # by size of the pair's combined type set; 3+ is unpenalised

# A pair whose only outward answer sits on one body has no answer at all once that body is the one
# down — the case `hi + lo//2` denies exists. Charged when the weaker body brings nothing.
LONE_RESCUE = 0.85

# Two bodies of the same class want the same unique items and the same ability spread. This is a
# coarse proxy for contention the model cannot see properly; it is deliberately small.
SAME_CLASS = 0.95

ABILITIES = ("str", "dex", "con", "int", "wis", "cha")
KEY_SAVES = frozenset(("wis", "con", "dex"))
ALL = ABILITIES
# scope: "self" applies to this body, "pair" applies to both and does not stack.
#
# Three tiers, because a two-way split under-counted the list badly. The first sweep found ten-odd
# real blanket save effects with no id here; every one of them contributed nothing, which is
# indistinguishable from an honest low score on the heaviest-weighted axis in the model.
#
#   blanket=True   applies to EVERY save, always. Buys the rung the table trades a proficiency for.
#   partial=True   applies to a subset of abilities, or costs an action or a limited resource.
#                  **Two partials count as one blanket** — the effect is real but half-covered, and
#                  a body carrying two of them is as protected as one carrying a blanket.
#   neither        documented, priced elsewhere, worth no rung on its own. War Caster is advantage
#                  on *concentration* saves only — marking it blanket silently lifted every
#                  concentration build a rung. Its value is already priced by `concentration` and
#                  the rung-3 cap below.
#
# Advantage against spells and magical effects counts as blanket: in this list almost every save
# that decides a fight comes off a spell or a magical effect, so the condition is nearly always met.
BOOSTERS = {
    # unconditional, every save
    "brutish-durability": {"scope": "self", "blanket": True},   # Fighter 7 — +1d6, no resource
    "aura-of-protection": {"scope": "pair", "blanket": True},   # Paladin 6 — +Cha
    "emboldening-bond":   {"scope": "pair", "blanket": True},   # Cleric Peace — +1d4, both bodies
    "friars-blessing":    {"scope": "pair", "blanket": True},   # Way of the Friar — +1d4, both bodies
    "lunar-champion":     {"scope": "pair", "blanket": True},   # Oath of the Moon 20 — +Cha aura
    "heroic-warrior":     {"scope": "self", "blanket": True},   # Champion — a free reroll every turn
    # advantage against spells and magical effects
    "magic-resistance":   {"scope": "self", "blanket": True},   # Paragon 9
    "spell-resistance":   {"scope": "self", "blanket": True},   # Wizard Abjuration 14
    "magic-awareness":    {"scope": "pair", "blanket": True},   # Wildsurge — PB to both, vs spells
    "rage-of-ginnungagap": {"scope": "self", "blanket": True},  # advantage vs spells while raging
    # a subset of abilities, or a limited resource. `abilities` is what the effect actually covers;
    # ALL means every save. Two partials make a blanket only if together they reach two of the
    # three key saves — see derive_saves. A Barbarian has advantage on Strength saves from Rage and
    # Dexterity saves from Danger Sense, and those two must NOT add up to full coverage, because
    # the saves that decide a duo fight are Wisdom and Constitution and neither touches them.
    "dark-augmentation":  {"scope": "self", "partial": True, "abilities": ("str", "dex", "con")},
    "towering-ego":       {"scope": "self", "partial": True, "abilities": ("wis", "int")},
    "frost-rune":         {"scope": "self", "partial": True, "abilities": ("str", "con")},
    "fanatical-focus":    {"scope": "self", "partial": True, "abilities": ALL},   # Zealot — reroll per Rage
    "gift-of-will":       {"scope": "pair", "partial": True, "abilities": ("wis",)},
    "flash-of-genius":    {"scope": "pair", "partial": True, "abilities": ALL},   # Artificer 7, a reaction
    # found by the tier-1 grants pass. Added conservatively: an effect earns an id only if it
    # applies to a save *category* rather than one named condition. "Advantage against Frightened"
    # and the like stay unregistered on purpose — they are real, and they are worth no rung.
    "indomitable":        {"scope": "self", "partial": True, "abilities": ALL},   # Fighter 9, 1-3/long rest
    "supernatural-defense": {"scope": "self", "partial": True, "abilities": ALL}, # Monster Slayer 7, +1d6 vs prey
    "cosmic-omen":        {"scope": "self", "partial": True, "abilities": ALL},   # Star Druid 6, +-1d6, short rest
    "legendary-resistance": {"scope": "self", "partial": True, "abilities": ALL}, # Paragon 15, auto-succeed
    "soul-of-artifice":   {"scope": "self", "partial": True, "abilities": ALL},   # Artificer 20, +1 all saves
    "danger-sense":       {"scope": "self", "partial": True, "abilities": ("dex",)},  # Barbarian 2
    "bladesong":          {"scope": "self", "partial": True, "abilities": ("con",)},  # Bladesinging 2, +2/3/4
    # real, but priced elsewhere
    "war-caster":         {"scope": "self", "blanket": False},  # concentration saves only
}


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
    if kind == "derived":
        return min(x, y)          # placeholder; both derived axes are written in by saves_pair
                                  # and skills_pair before the record is built
    raise ScoringError(f"unknown axis kind {kind!r}")


def combine(a, b):
    return {ax: combine_axis(a[i], b[i], KINDS[ax]) for i, ax in enumerate(KEYS)}


def norm(ax, value):
    """Combined value -> 0..1 against that axis kind's own maximum."""
    return value / KIND_MAX[KINDS[ax]]


# ── saves are derived from the authored set, never authored directly ─────────
# ── hot-path memoisation ─────────────────────────────────────────────────────
# A body's save block and its derived rung do not depend on the partner, but `score()` recomputes
# both for every pairing: C(150,2) pairs meant 134,100 calls for 150 distinct bodies. Ranking
# enumerated split variants against a pool is the same shape and two orders of magnitude larger,
# so both are cached on their *content*. The functions are pure — same inputs, same result and the
# same raised error — so memoising cannot change behaviour, only cost.
#
# Errors still fail closed: an invalid block raises on the first call and, being uncached, raises
# identically on every later one.
def _saves_block_ok(prof, boosters):
    """Cached validity check on block content. Returns None, or the reason it is invalid."""
    key = (prof, boosters)
    hit = _SAVES_OK_CACHE.get(key, _MISS)
    if hit is not _MISS:
        return hit
    reason = None
    for a in prof:
        if a not in ABILITIES:
            reason = f"unknown ability {a!r} — expected one of {ABILITIES}"
            break
    else:
        if len(set(prof)) != len(prof):
            reason = (f"duplicate ability in prof {list(prof)!r} — record the union after "
                      "de-duplication, so overlapping grants correctly count once")
        else:
            for b in boosters:
                if b not in BOOSTERS:
                    reason = (f"unknown booster {b!r} — add it to BOOSTERS with an "
                              "implemented effect before authoring it")
                    break
    _SAVES_OK_CACHE[key] = reason
    return reason


_SAVES_OK_CACHE = {}
_SAVES_CACHE = {}
_MISS = object()


def _validate_saves_block(block, who, act):
    _require(isinstance(block, dict), f"{who} {act}: saves block must be an object")
    for field in ("prof", "boosters"):
        _require(field in block, f"{who} {act}: saves block missing {field!r}")
    reason = _saves_block_ok(tuple(block["prof"]), tuple(block["boosters"]))
    _require(reason is None, f"{who} {act}: {reason}")


def derive_saves(prof, boosters, concentration):
    """scoring-model.md / ledger-schema.md rung table. Returns 0-5.

    Validates its own inputs: this is a public entry point, and an unrecognised
    ability or booster silently contributing nothing is the one failure mode the
    model cannot detect downstream.
    """
    key = (tuple(prof), tuple(boosters), bool(concentration))
    hit = _SAVES_CACHE.get(key, _MISS)
    if hit is not _MISS:
        return hit
    for a in prof:
        _require(a in ABILITIES,
                 f"unknown ability {a!r} — expected one of {ABILITIES}")
    _require(len(set(prof)) == len(prof), f"duplicate ability in prof {prof!r}")
    for b in boosters:
        _require(b in BOOSTERS, f"unknown booster {b!r}")
    s = set(prof)
    n, nkey = len(s), len(s & KEY_SAVES)
    # Two partials make a blanket — but only if together they reach two of the three key saves.
    # Counting partials alone let two effects that both miss Wisdom and Constitution add up to
    # full coverage, which is exactly backwards: those are the saves a duo actually loses to.
    parts = [b for b in boosters if BOOSTERS[b].get("partial")]
    covered = set().union(*(BOOSTERS[b].get("abilities", ()) for b in parts)) if parts else set()
    blanket = (any(BOOSTERS[b].get("blanket") for b in boosters)
               or (len(parts) >= 2 and len(covered & KEY_SAVES) >= 2))
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
    _SAVES_CACHE[key] = v
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

    # Pair-scope boosters raise both bodies. Non-stacking is per *effect*, not per scope: an Aura
    # of Protection and an Emboldening Bond are different sources and both apply, but two Auras of
    # Protection are one Aura and six wasted levels. So dedupe by id and warn only on a collision.
    shared, seen = [], set()
    for w in ("a", "b"):
        for x in blocks[w]["boosters"]:
            if BOOSTERS[x]["scope"] != "pair":
                continue
            if x in seen:
                warnings.append(
                    f"both {ca['_id']} and {cb['_id']} bring {x}. It does not stack with itself — "
                    "the second is ignored, and the levels that bought it are wasted.")
                continue
            seen.add(x)
            shared.append(x)

    for who, c in (("a", ca), ("b", cb)):
        blk = blocks[who]
        boosters = list(dict.fromkeys(list(blk["boosters"]) + shared))
        out[who] = derive_saves(blk["prof"], boosters, c.get("concentration", False))
    return out["a"], out["b"], warnings


def _classes(split):
    """The set of class names in a split string, for the contention proxy."""
    import re as _re
    out = set()
    for part in split.split("/"):
        part = _re.sub(r"\(.*$", "", part).strip().strip("*").strip()
        m = _re.match(r"^(.+?)\s+\d{1,2}$", part)
        if m:
            out.add(m.group(1).strip())
    return out


def skills_pair(ca, cb, act):
    """The pair's Skills rung for one act, from both bodies' skill modifiers.

    Every remaining check is party-level, so the pair takes the better body on each. Note
    what does NOT transfer: Reliable Talent and Silver Tongue are keyed on *being proficient* and
    stay with the body that owns them, so a rung resting on those is the owner's alone — record
    the owner's modifier without them if the partner is the one rolling.
    """
    ma = (ca.get("skills") or {}).get(act, {})
    mb = (cb.get("skills") or {}).get(act, {})
    for who, m in ((ca["_id"], ma), (cb["_id"], mb)):
        _require(isinstance(m, dict), f"{who} {act}: `skills` must be a modifier map")
        for sk in m:
            _require(sk in RECORDED_SKILLS,
                     f"{who} {act}: unknown skill {sk!r} — expected one of {RECORDED_SKILLS}")
    oa = _gate_odds(ma, act, _classes(ca.get("split", "")))
    ob = _gate_odds(mb, act, _classes(cb.get("split", "")))
    return _rung([(sa or sb, max(pa, pb)) for (sa, pa), (sb, pb) in zip(oa, ob)])


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
    # No role. A chassis is not typed carry-or-support: the model pairs every chassis with every
    # other, so a duo of two damage bodies or two controllers is representable and rankable
    # rather than unsayable.
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
    # Both derived axes need their evidence, and a missing map must RAISE rather than derive 0.
    # `skl` is weighted 2.5; a body silently reading 0 on it is the invisible failure this whole
    # model is built to refuse — too low, and indistinguishable from an honest low score.
    sk = c.get("skills")
    _require(isinstance(sk, dict), f"{cid}: `skills` missing — Skills is derived from check "
                                   f"modifiers, and an absent map would score 0 in silence")
    for act in ACTS:
        _require(act in sk, f"{cid}: `skills` missing act {act}")
        for name, mod in sk[act].items():
            _require(name in RECORDED_SKILLS,
                     f"{cid} {act}: unknown skill {name!r} — expected one of {RECORDED_SKILLS}")
            _require(isinstance(mod, int), f"{cid} {act}: {name} modifier must be an integer")
        for name in REQUIRED_SKILLS:
            _require(name in sk[act],
                     f"{cid} {act}: `skills` has no {name} modifier. Traps, hidden caches, secret "
                     f"doors and town dialogue recur through every act and cannot be respecced "
                     f"for, so they carry the axis — an absent value would be read as hopeless "
                     f"rather than as the evidence gap it is. Record it, even if untrained.")
    ty = c.get("types")
    _require(isinstance(ty, list) and ty,
             f"{cid}: `types` missing — two bodies sharing one damage type have no answer when "
             f"it is resisted, and Absolute Wrath is on")
    for t in ty:
        _require(t in DAMAGE_TYPES, f"{cid}: unknown damage type {t!r}")



# ── presentation order within a pairing ──────────────────────────────────────
def _lead_metrics(ca, cb):
    """Each body's (delivered damage, total axis value), summed across acts.

    Saves are derived per *pairing*, since Aura of Protection is a pair-scope booster, so both
    bodies are resolved together here exactly as they are in the score itself.
    """
    dmg = {"a": 0.0, "b": 0.0}
    tot = {"a": 0.0, "b": 0.0}
    for act in ACTS:
        va, vb, _ = saves_pair(ca, cb, act)
        for who, c, sv in (("a", ca, va), ("b", cb, vb)):
            row = list(c["scores"][act])
            row[SAV_IDX] = sv
            dmg[who] += sum(utilisation(row, c["reach"]))
            tot[who] += sum(row)
    return (dmg["a"], tot["a"]), (dmg["b"], tot["b"])


def lead_order(ca, cb):
    """Which body is presented first. Returns the two bodies, ordered.

    **Higher delivered damage leads**, then higher total axis value, then the id alphabetically.
    A pairing is unordered — the score is symmetric — so without a rule the order would fall out
    of whatever sequence the caller happened to iterate in, and the same duo could render one way
    in the field table and the other in an entry. The damage-first rule also puts the body a
    reader thinks of as carrying the fight on the left, which is what the old carry/support
    partition used to do implicitly.
    """
    (da, oa), (db, ob) = _lead_metrics(ca, cb)
    if (-db, -ob, cb["_id"]) < (-da, -oa, ca["_id"]):
        return cb, ca
    return ca, cb


# ── the score ────────────────────────────────────────────────────────────────
def score(C, a, b):
    """Pair score from a chassis map. Ids are injected as `_id`."""
    return score_bodies(dict(C[a], _id=a), dict(C[b], _id=b))


def score_bodies(ca, cb):
    """Pair score from two body dicts.

    Each needs `_id`, `reach`, `scores` (act -> 10 values, index 8 null),
    `saves` (act -> {prof, boosters}) and optionally `concentration`.
    """
    _require(ca["reach"] in REACH, f"{ca['_id']}: unknown reach {ca['reach']!r}")
    _require(cb["reach"] in REACH, f"{cb['_id']}: unknown reach {cb['reach']!r}")

    ca, cb = lead_order(ca, cb)
    a, b = ca["_id"], cb["_id"]
    ra, rb = ca["reach"], cb["reach"]
    locked = ra in ("static", "mobile") and rb in ("static", "mobile")

    ta = {t for t in (ca.get("types") or [])}
    tb = {t for t in (cb.get("types") or [])}
    for who, ts in ((a, ta), (b, tb)):
        for t in ts:
            _require(t in DAMAGE_TYPES, f"{who}: unknown damage type {t!r}")
    both = ta | tb
    type_spread = TYPE_SPREAD.get(len(both), 1.0) if both else 1.0
    same_class = bool(_classes(ca.get("split", "")) & _classes(cb.get("split", "")))

    rec = {"a": a, "b": b, "acts": {}, "locked": locked, "type_spread": type_spread,
           "types": sorted(both), "same_class": same_class,
           "holes": set(), "flags": set(), "warnings": []}
    tempo_total = nontempo_total = 0.0

    for act in ACTS:
        sa = list(ca["scores"][act])
        sb = list(cb["scores"][act])
        va, vb, warns = saves_pair(ca, cb, act)
        sa[SAV_IDX], sb[SAV_IDX] = va, vb
        rec["warnings"] += warns

        pair = combine(sa, sb)
        pair["skl"] = skills_pair(ca, cb, act)      # derived from modifiers, not from the rungs
        wc, wb = MIX[act]

        ua, ub = utilisation(sa, ra), utilisation(sb, rb)
        if locked:
            ua[0] *= 0.9
            ub[0] *= 0.9
        # Absolute Wrath layers resistances on ordinary enemies. Two bodies dealing the same type
        # have no answer at all when it is resisted, and `add` summed them as if they did.
        if type_spread < 1.0:
            ua[0] *= type_spread; ua[1] *= type_spread
            ub[0] *= type_spread; ub[1] *= type_spread
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

        # A flagged body has nothing worth doing in this fight type, so the pair fights it a body
        # down. Charged against that fight type's term only, in the act it happens in — a body
        # that idles in crowds is fine against a boss and must not be charged for both.
        idle_c = sum(1 for who, u in ((a, ua), (b, ub)) if u[0] < FLAG and wc >= 0.40)
        idle_b = sum(1 for who, u in ((a, ua), (b, ub)) if u[1] < FLAG and wb >= 0.40)
        crowd *= IDLE_BODY ** idle_c
        boss *= IDLE_BODY ** idle_b
        tempo = (wc * crowd + wb * boss) * action_factor(pair["act"])

        rsc_c, rsc_b = FIGHT["rsc"]
        adj = {ax: norm(ax, pair[ax]) for ax in RESILIENCE + DURATION + UTILITY}
        adj["rsc"] *= wc * rsc_c + wb * rsc_b
        # One body carrying all the outward answer is not the same as two carrying half each:
        # when the body that heals is the body that went down, nothing picks it up.
        if min(sa[KEYS.index("rsc")], sb[KEYS.index("rsc")]) == 0:
            adj["rsc"] *= LONE_RESCUE
        # A hole is an axis the PAIR cannot answer — with only two characters there is no third
        # body to cover it, so it is not merely a low average. Charged once per holed axis per
        # act, to the block that axis belongs to, so a pair holed in Act I but not Act III pays
        # for Act I only. Applied to the blocks as well as to the score, because the frontier
        # selects on the blocks and the two must not disagree about how good a pairing is.
        act_holes = {k for k in KEYS if norm(k, pair[k]) <= 0.40}
        hole_f = {grp: HOLE ** len(act_holes & set(axes))
                  for grp, axes in (("tempo", set(TEMPO) | {"act"}),
                                    ("resilience", set(RESILIENCE)),
                                    ("duration", set(DURATION)),
                                    ("utility", set(UTILITY)))}
        tempo *= hole_f["tempo"]
        for ax in adj:
            for grp, axes in (("resilience", RESILIENCE), ("duration", DURATION), ("utility", UTILITY)):
                if ax in axes and ax in act_holes:
                    adj[ax] *= HOLE

        nontempo = (sum(WEIGHTS[ax] * adj[ax] for ax in WEIGHTS)
                    / sum(WEIGHTS.values()))

        # §2's four blocks, kept apart. `nontempo` is their weighted mean and is what the score
        # uses; these are what *selection* runs against, because a pairing that is beaten on one
        # block and wins another is not beaten at all — which a single number cannot say.
        blocks = {
            "tempo": tempo,
            "resilience": (sum(WEIGHTS[ax] * adj[ax] for ax in RESILIENCE)
                           / sum(WEIGHTS[ax] for ax in RESILIENCE)),
            "duration": sum(adj[ax] for ax in DURATION) / len(DURATION),
            "utility": sum(adj[ax] for ax in UTILITY) / len(UTILITY),
        }

        # display: collapse the two control axes to one act-appropriate spoke
        radar = dict(pair)
        radar["ctrl"] = wc * pair["ctrl_a"] + wb * pair["ctrl_s"]

        # `ua`/`ub` follow the record's own presentation order, which lead_order may have
        # swapped relative to the caller's. `u` is keyed by id so a consumer holding its own
        # notion of which body is which can never mis-attribute delivered damage.
        rec["acts"][act] = {"radar": radar, "pair": pair, "ua": ua, "ub": ub,
                            "u": {a: ua, b: ub}, "blocks": blocks,
                            "crowd": crowd, "boss": boss, "tempo": tempo,
                            "nontempo": nontempo,
                            "dmg_crowd": dmg_crowd, "dmg_boss": dmg_boss}
        rec["holes"] |= act_holes
        tempo_total += tempo
        nontempo_total += nontempo

    rec["warnings"] = list(dict.fromkeys(rec["warnings"]))
    rec["tempo"] = tempo_total / len(ACTS)
    rec["nontempo"] = nontempo_total / len(ACTS)
    rec["blocks"] = {b: sum(rec["acts"][a]["blocks"][b] for a in ACTS) / len(ACTS)
                     for b in BLOCKS}
    contention = SAME_CLASS if same_class else 1.0
    rec["score"] = round((50 * rec["tempo"] + 50 * rec["nontempo"]) * contention, 1)
    rec["holes"] = sorted(rec["holes"], key=KEYS.index)
    return rec
