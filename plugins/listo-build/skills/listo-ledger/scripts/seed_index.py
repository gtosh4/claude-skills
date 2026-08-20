#!/usr/bin/env python3
"""Chassis discovery: the mechanical half.

The roster is authored, but *what it must cover* is not a judgement call — it is
every subclass in `listo-build/data/classes/*.md`. This script reads that
inventory, diffs it against the seeds file, and applies the promotion bar.

    scripts/seed_index.py --list                  # the inventory, from the data
    scripts/seed_index.py --check                 # diff seeds against it
    scripts/seed_index.py --promote               # every viable build (--limit N to ration)
    scripts/seed_index.py --assign 8              # split the sweep across N agents

Seeds default to `assets/chassis-seeds.json`. `--check` and `--promote` exit
non-zero on any gap, because an unseeded subclass is invisible exactly the way a
dropped booster is: nothing downstream can tell it apart from a considered one.

The judgement — the split, the niche, the peak — is the sweep's job, and lives in
the seeds file. See SKILL.md, "Discovering the roster".
"""
import json, sys, os, re, argparse, collections, hashlib

HERE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
CLASSES = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                       "listo-build", "data", "classes")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "listo-build", "scripts"))
from scoring import KEYS, SAV_IDX, BOOSTERS                 # noqa: E402

# The niche vocabulary is listo-build SKILL.md §1a's table. Closed, like every
# other enum in this format.
NICHES = ("action-economy", "lockdown", "front-line", "reaction",
          "short-rest", "durability", "skills")
VERDICTS = ("candidate", "dupe", "none", "not-a-subclass")

# A subclass may express more than one chassis, but only one per niche — and past three
# the fourth is a reflavour of one of the first three rather than a distinct body.
MAX_BUILDS = 3

# By default every viable build is scored. Selection happens *downstream*, on real pair scores,
# because that is strictly better information than `peak` — a coarse single-act triage number
# whose only job was to rank seeds cheaply when scoring everything was unaffordable.
#
# `--limit` re-imposes rationing when the scoring budget demands it, and only then do the floors
# and the bar matter: scoring is ~5k tokens per chassis, linear, and it is the only real cost.
# Pairings are derived from the authored ints and cost nothing worth counting.
BAR = 4
ROSTER_LIMIT = None


# A split is one to three distinct classes summing to twenty, written with `/` only:
# `Cleric 14 / Paladin 6`. **Levelling order is not recorded here.** Which block comes first
# matters enormously to a build, but it is a pair-sheet decision, and a seed that encodes it is
# claiming precision the sweep does not have. So a class appears once, carrying its total.
MAX_CLASSES = 3
TOTAL_LEVELS = 20
_SEG = re.compile(r"^\s*(.+?)\s+(\d{1,2})\s*$")


def parse_split(text):
    """`{class: levels}` from a split string, or raise. Parts split on `/`.

    Trailing parentheticals are dropped: `Wizard 6 (Evocation)` is six levels of Wizard.
    """
    _require(isinstance(text, str) and text.strip(), "split must be a non-empty string")
    _require("->" not in text and "\u2192" not in text,
             f"split uses arrow notation: {text!r}. Levelling order belongs to the pair sheet, "
             "not the seed — write each class once with its total, joined by `/`")
    out = collections.OrderedDict()
    for seg in text.split("/"):
        # The parenthetical is the subclass and always trails the level, so strip from the first
        # `(` to the end of the segment rather than matching balanced pairs — subclass names in
        # this list nest their own brackets (`Zeal (Hazoret)`, `Wild Magic (vanilla)`).
        seg = re.sub(r"\(.*$", "", seg).strip().strip(",")
        if not seg:
            continue
        m = _SEG.match(seg)
        _require(m, f"cannot read a `<class> <levels>` part from {seg!r}")
        cls, n = m.group(1).strip(), int(m.group(2))
        _require(cls not in out,
                 f"{cls!r} appears twice in {text!r} — give each class one part carrying its "
                 "total; the order the levels were taken in is the pair sheet's business")
        out[cls] = n
    _require(out, "split names no classes")
    return out


def check_split(text, where):
    levels = parse_split(text)
    total = sum(levels.values())
    _require(total == TOTAL_LEVELS,
             f"{where}: split totals {total}, not {TOTAL_LEVELS} — {text!r}")
    _require(len(levels) <= MAX_CLASSES,
             f"{where}: split names {len(levels)} classes, at most {MAX_CLASSES} — {text!r}")
    return levels


class SeedError(Exception):
    pass


def _require(cond, msg):
    if not cond:
        raise SeedError(msg)


# ── the inventory ────────────────────────────────────────────────────────────
def inventory():
    """Every subclass heading in the class files, as {class: [heading, ...]}.

    One `## ...subclass...` section per class file; its `###` children are the
    subclasses. Headings are taken verbatim apart from markdown emphasis, so the
    keys stay stable when prose around them changes.
    """
    out = {}
    for path in sorted(os.listdir(CLASSES)):
        if not path.endswith(".md"):
            continue
        cls, inside, subs = path[:-3], False, []
        for line in open(os.path.join(CLASSES, path)):
            if line.startswith("## "):
                inside = "subclass" in line.lower()
            elif inside and line.startswith("### "):
                subs.append(re.sub(r"\s+", " ", line[4:].replace("*", "")).strip())
        _require(subs, f"{path}: no `## ...subclass...` section with `###` entries")
        out[cls] = subs
    _require(out, f"no class files under {CLASSES}")
    return out


def ranges(cls):
    """The two line ranges a sweep agent may read: at-a-glance, and the subclass section.

    Whole class files are ~148k tokens across the seventeen; these two sections are ~77k. The
    rest is provenance, load-order notes and dip tables the brief already carries.
    """
    lines = open(os.path.join(CLASSES, cls + ".md")).read().split("\n")
    spans, open_at, label = {}, None, None
    for i, l in enumerate(lines):
        if l.startswith("## "):
            if open_at is not None:
                spans[label] = (open_at + 1, i)
            low = l.lower()
            label = ("subs" if "subclass" in low else
                     "glance" if "at a glance" in low and "glance" not in spans else None)
            open_at = i if label else None
    if open_at is not None:
        spans[label] = (open_at + 1, len(lines))
    _require("subs" in spans, f"{cls}: no subclass section")
    cost = sum(len(l) + 1 for lo, hi in spans.values() for l in lines[lo - 1:hi]) // 4
    return spans, cost


REFS = os.path.join(os.path.dirname(os.path.dirname(HERE)), "listo-build", "references")
DATA = os.path.dirname(CLASSES)

# Two stages, two dependency sets. Seeding is a judgement about a subclass under the sweep
# brief's rules; scoring is a judgement about a build under the rubric's rules. They go stale
# independently — editing axis-rubrics.md must not force a re-sweep, and editing the brief must
# not force a re-score. Add a file here when a new document starts governing one of them.
DEPS = {
    "base":  [os.path.join(ASSETS, "base-brief.md"),
              os.path.join(DATA, "listo-10.2-spells.md"),
              os.path.join(REFS, "axis-rubrics.md"),
              os.path.join(REFS, "scoring-model.md"),
              os.path.join(REFS, "gates.md")],
    "seed":  [os.path.join(ASSETS, "sweep-brief.md")],
    "score": [os.path.join(ASSETS, "scoring-brief.md"),
              os.path.join(REFS, "axis-rubrics.md"),
              os.path.join(REFS, "scoring-model.md"),
              os.path.join(REFS, "gates.md")],
}


def digests(cls):
    """`{subclass: hash}` over exactly the text a sweep agent was shown for it.

    The seed is a cached judgement, and this is its cache key: the subclass's own `###` block
    plus that class's at-a-glance section, which carries the class-level facts every split in
    the file depends on. Editing one subclass therefore invalidates one seed, and editing
    at-a-glance invalidates that class's seeds — nothing wider.
    """
    lines = open(os.path.join(CLASSES, cls + ".md")).read().split("\n")
    spans, _ = ranges(cls)
    glance = "\n".join(lines[spans["glance"][0] - 1:spans["glance"][1]]) if "glance" in spans else ""
    lo, hi = spans["subs"]
    out, head, body = {}, None, []
    for line in lines[lo - 1:hi]:
        if line.startswith("### "):
            if head:
                out[head] = "\n".join(body)
            head, body = re.sub(r"\s+", " ", line[4:].replace("*", "")).strip(), []
        elif head:
            body.append(line)
    if head:
        out[head] = "\n".join(body)
    return {k: hashlib.sha256((glance + "\0" + v).encode()).hexdigest()[:12]
            for k, v in out.items()}


def deps_hash(stage):
    h = hashlib.sha256()
    for path in DEPS[stage]:
        _require(os.path.exists(path),
                 f"missing {os.path.relpath(path)} — it is part of the {stage} cache key")
        h.update(open(path, "rb").read())
    return h.hexdigest()[:12]


def audit(inv, seeds):
    """What actually needs redoing, and at which stage.

    A seed is a cached judgement. It is valid while the three things it was derived from are
    unchanged: the subclass's own text, the class's at-a-glance facts (together, `src`), and the
    sweep brief (`seed_deps`). Scores are a *second* cached judgement over the same build,
    derived from the rubric and the scoring model (`score_deps`), and they go stale on their own
    schedule — which is the point of keeping the two keys apart.

    Returns the five buckets and the fresh `src` map.
    """
    src = {cls: digests(cls) for cls in inv}
    want = {f"{cls}/{sub}": src[cls].get(sub) for cls, subs in inv.items() for sub in subs}
    seed_h, score_h = deps_hash("seed"), deps_hash("score")

    unseeded = sorted(k for k in want if k not in seeds)
    stale    = sorted(k for k in seeds if k not in want)
    drifted  = sorted(k for k, h in want.items()
                      if k in seeds and seeds[k].get("src") != h)
    rules    = sorted(k for k in seeds if k in want and seeds[k].get("seed_deps") != seed_h)
    unscored, rescore = [], []
    for addr, b in builds(seeds).items():
        if b["key"] in drifted or b["key"] in rules:
            continue                       # the seed itself must be redone first
        if not b.get("score_deps"):
            unscored.append(addr)
        elif b["score_deps"] != score_h:
            rescore.append(addr)
    return dict(unseeded=unseeded, stale=stale, drifted=drifted, rules=rules,
                unscored=sorted(unscored), rescore=sorted(rescore), want=want)


def dip_ranges():
    """Every class's `## Dip value` section — the shared read set for a sweep.

    A seed's split names two classes, and an agent assigned one of them cannot invent what the
    other sells. These sections are the authority on that, ~10.6k across the seventeen, and every
    sweep agent reads all of them. A hand-compressed menu in the brief was cheaper and wrong: it
    covered which class to *dip* into, at levels 1-6, and said nothing that supports a 12/8.
    """
    out = {}
    for path in sorted(os.listdir(CLASSES)):
        if not path.endswith(".md"):
            continue
        cls = path[:-3]
        lines = open(os.path.join(CLASSES, path)).read().split("\n")
        start = end = None
        for i, l in enumerate(lines):
            if l.startswith("## "):
                if start is None and "dip" in l.lower():
                    start = i
                elif start is not None and end is None:
                    end = i
        _require(start is not None, f"{cls}: no `## Dip value` section")
        out[cls] = (start + 1, end or len(lines))
    return out


def batches(inv, n):
    """Bin-pack classes into n agents by reading cost, largest first, least-loaded bin."""
    _require(0 < n <= len(inv), f"batch count must be 1-{len(inv)}, got {n}")
    sized = sorted(((ranges(c)[1], c) for c in inv), reverse=True)
    bins = [[] for _ in range(n)]
    load = [0] * n
    for cost, cls in sized:
        i = load.index(min(load))
        bins[i].append(cls)
        load[i] += cost
    return [b for b in bins if b]


def keys(inv):
    return [f"{cls}/{sub}" for cls, subs in inv.items() for sub in subs]


# ── tier 1: subclass base profiles ───────────────────────────────────────────
# A base profile is the subclass at all twenty levels with no multiclassing, scored coarsely on
# the ten axes in Act II. It is the zero-dip reference point every split of that subclass is
# measured against — not a recommendation to play it mono.
#
# Grants are recorded apart from `scores` because they do not add, they union: only the level-1
# class gives saving throws and the good armour, so composition has to know which class was first.
ABILITIES = ("str", "dex", "con", "int", "wis", "cha")
ARMOUR = (None, "light", "medium", "heavy")
BASE_DEPS = "base"


def load_bases(path):
    """Validate a tier-1 bases file and return `{key: record}`."""
    with open(path) as fh:
        d = json.load(fh)
    bases = d.get("bases")
    load_bases.doc = d
    _require(isinstance(bases, dict), f"{path}: no `bases` object")
    for k, b in bases.items():
        v = b.get("verdict")
        _require(v in VERDICTS, f"{k}: unknown verdict {v!r} — expected one of {VERDICTS}")
        if v == "dupe":
            _require(b.get("dupe_of") in bases, f"{k}: dupe_of {b.get('dupe_of')!r} is not a key")
        if v != "candidate":
            _require(b.get("why"), f"{k}: verdict {v!r} needs a `why`")
            continue
        sc = b.get("scores")
        _require(isinstance(sc, list) and len(sc) == len(KEYS),
                 f"{k}: `scores` must be {len(KEYS)} values, got {sc!r}")
        _require(sc[SAV_IDX] is None,
                 f"{k}: scores[{SAV_IDX}] must be null — saves are derived from `prof`, never authored")
        for i, x in enumerate(sc):
            if i == SAV_IDX:
                continue
            _require(isinstance(x, int) and 0 <= x <= 5,
                     f"{k}: {KEYS[i]} is {x!r}, expected an integer 0-5")
        prof = b.get("prof")
        _require(isinstance(prof, list), f"{k}: `prof` must be a list")
        for a in prof:
            _require(a in ABILITIES, f"{k}: unknown ability {a!r} — expected one of {ABILITIES}")
        _require(len(set(prof)) == len(prof), f"{k}: duplicate ability in prof {prof!r}")
        bo = b.get("boosters")
        _require(isinstance(bo, list), f"{k}: `boosters` must be a list (empty is fine)")
        for x in bo:
            _require(x in BOOSTERS,
                     f"{k}: unknown booster {x!r} — add it to BOOSTERS with an implemented "
                     "effect before authoring it, or put the effect in `uncertain`")
        _require(len(set(bo)) == len(bo), f"{k}: duplicate booster in {bo!r}")
        _require(b.get("armour", "MISSING") in ARMOUR,
                 f"{k}: armour {b.get('armour')!r} — expected one of {ARMOUR}")
        _require(isinstance(b.get("shield"), bool), f"{k}: `shield` must be true or false")
        _require(b.get("primary") in ABILITIES,
                 f"{k}: primary {b.get('primary')!r} — expected one of {ABILITIES}")
        _require(isinstance(b.get("concentration"), bool),
                 f"{k}: `concentration` must be true or false")
        _require(b.get("why"), f"{k}: candidate needs a `why`")
        for f in ("chassis", "split", "niche", "peak", "peak_axis", "breadth"):
            _require(f not in b,
                     f"{k}: `{f}` is not a tier-1 field. Splits, names and niches are decided "
                     "after enumeration, not here")
    return bases


def audit_bases(inv, bases):
    """Which base profiles need redoing. Same cache contract as the seeds, one stage."""
    src = {cls: digests(cls) for cls in inv}
    want = {f"{cls}/{sub}": src[cls].get(sub) for cls, subs in inv.items() for sub in subs}
    dep = deps_hash(BASE_DEPS)
    return dict(
        unseeded=sorted(k for k in want if k not in bases),
        stale=sorted(k for k in bases if k not in want),
        drifted=sorted(k for k, h in want.items() if k in bases and bases[k].get("src") != h),
        rules=sorted(k for k in bases if k in want and bases[k].get("base_deps") != dep),
        want=want)


# ── the seeds file ───────────────────────────────────────────────────────────
def load(path):
    with open(path) as fh:
        d = json.load(fh)
    seeds = d.get("seeds")
    load.doc = d
    _require(isinstance(seeds, dict), f"{path}: no `seeds` object")
    for k, s in seeds.items():
        v = s.get("verdict")
        _require(v in VERDICTS, f"{k}: unknown verdict {v!r} — expected one of {VERDICTS}")
        if v == "candidate":
            b = s.get("builds")
            _require(isinstance(b, dict) and b, f"{k}: candidate needs a `builds` object keyed by niche")
            _require(len(b) <= MAX_BUILDS,
                     f"{k}: {len(b)} builds, cap is {MAX_BUILDS} — a fourth is reflavouring, not a chassis")
            for niche, bd in b.items():
                w = f"{k}:{niche}"
                _require(niche in NICHES, f"{w}: unknown niche — expected one of {NICHES}")
                for f in ("chassis", "split", "peak", "peak_axis", "breadth", "why"):
                    _require(bd.get(f) is not None, f"{w}: build missing `{f}`")
                check_split(bd["split"], w)
                _require(bd["peak_axis"] in KEYS,
                         f"{w}: unknown peak_axis {bd['peak_axis']!r} — expected one of {tuple(KEYS)}")
                _require(isinstance(bd["peak"], int) and 0 <= bd["peak"] <= 5,
                         f"{w}: peak is {bd['peak']!r}, expected an integer 0-5")
                # `peak` is a maximum, and a maximum cannot see what a dip buys — a wide body and a
                # narrow one with the same best axis are indistinguishable to it. `breadth` counts
                # the axes at 3 or better, so the two are separable at promotion time.
                _require(isinstance(bd["breadth"], int) and 0 <= bd["breadth"] <= len(KEYS),
                         f"{w}: breadth is {bd['breadth']!r}, expected an integer 0-{len(KEYS)}")
                _require(bd["breadth"] == 0 or bd["peak"] >= 3,
                         f"{w}: breadth {bd['breadth']} claims an axis at 3+, but peak is "
                         f"{bd['peak']} — the highest axis cannot be below the ones counted under it")
            splits = collections.Counter(bd["split"] for bd in b.values())
            same = [x for x, c in splits.items() if c > 1]
            _require(not same, f"{k}: builds must differ in the split, not only the label: " + "; ".join(same))
        elif v == "dupe":
            _require(s.get("dupe_of") in seeds, f"{k}: dupe_of {s.get('dupe_of')!r} is not a seed key")
            _require(s.get("why"), f"{k}: verdict 'dupe' needs a `why`")
        else:
            _require(s.get("why"), f"{k}: verdict {v!r} needs a `why`")
    names = collections.Counter(bd["chassis"] for s in seeds.values()
                                if s["verdict"] == "candidate" for bd in s["builds"].values())
    dupes = [n for n, c in names.items() if c > 1]
    _require(not dupes, "chassis names must be unique (they are ledger ids): " + ", ".join(dupes))
    return seeds


def builds(seeds):
    """Every candidate build, addressed `<class>/<subclass>:<niche>`.

    The seed is per subclass because that is what the inventory can check; the *unit of
    promotion* is the build, because one subclass often has more than one honest expression
    and they land in different niches.
    """
    return {f"{k}:{niche}": dict(bd, key=k, niche=niche, cls=k.split("/")[0])
            for k, s in seeds.items() if s["verdict"] == "candidate"
            for niche, bd in s["builds"].items()}


# ── the bar ──────────────────────────────────────────────────────────────────
def promote(seeds, limit=ROSTER_LIMIT):
    """Which builds make the scored roster, and why.

    With no `limit` — the default — every viable build is promoted. Nothing is filtered on
    `peak`, because `peak` is a one-act triage guess and the pair score is a real number: it is
    better to score thoroughly and threshold afterwards than to discard a chassis on the estimate
    that was only ever there to make the sweep cheap.

    With a `limit`, floors come first and the bar fills what is left. The floors are the point:
    rationing on the bar alone re-creates the roster that is selected for being good at
    something, which is what retired the correlation figures.
    """
    cand = builds(seeds)
    _require(cand, "no candidate builds to promote")

    if limit is None:
        # Thorough: every viable build is scored, and the cut is made later against pair scores.
        return {a: "viable" for a in cand}, cand

    # Rank on peak first, then breadth: a maximum cannot separate a wide body from a narrow one
    # that happens to share its best axis, and breadth is exactly what a multiclass split buys.
    rank = lambda a: (-cand[a]["peak"], -cand[a]["breadth"], a)
    best = lambda group: min(group, key=rank)
    reasons = {}

    # Floors are guaranteed slots, not fallbacks: every class and every niche gets its honest
    # best whatever its peak. There is no role floor — a chassis is not typed carry-or-support,
    # and the renderer pairs every chassis with every other.
    for field, label in (("cls", "class floor"), ("niche", "niche floor")):
        groups = collections.defaultdict(list)
        for a, b in cand.items():
            groups[b[field]].append(a)
        for g in groups.values():
            if not any(a in reasons for a in g):
                reasons[best(g)] = label

    if len(reasons) > limit:
        print(f"# {len(reasons)} floors exceed the limit of {limit}; coverage wins, "
              f"the roster is the floors alone", file=sys.stderr)
        return reasons, cand

    rest = sorted((a for a in cand if a not in reasons), key=rank)
    for a in rest[:limit - len(reasons)]:
        if cand[a]["peak"] >= BAR:
            reasons[a] = "bar"
    return reasons, cand


# ── output ───────────────────────────────────────────────────────────────────
SPELLS = os.path.join(os.path.dirname(CLASSES), "listo-10.2-spells.md")


def spell_ranges():
    """`(framing_span, {class: span})` over listo-10.2-spells.md.

    Spell access is the single biggest thing the mods change for a caster — Wizard's level-1 pick
    pool is 45 against vanilla's 23 — so a subclass cannot be scored on aoe or control without it.
    One `### heading` can cover several classes ("Mesmerist, Inquisitor, Paragon, ..."), so a
    class is matched by name anywhere in the heading rather than by position.
    """
    lines = open(SPELLS).read().split("\n")
    heads = [(i, l[4:].strip()) for i, l in enumerate(lines) if l.startswith("### ")]
    sec2 = [i for i, l in enumerate(lines) if l.startswith("## ")]
    framing = None
    for i in sec2:
        if "how spell access is wired" in lines[i].lower():
            nxt = next((j for j in sec2 if j > i + 3), len(lines))
            framing = (i + 1, nxt)
    _require(framing, "listo-10.2-spells.md: no `## How spell access is wired` section")
    out = {}
    for cls in inventory():
        want = cls.replace("bloodhunter", "blood hunter")
        for n, (i, text) in enumerate(heads):
            if want in text.lower():
                end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
                out.setdefault(cls, (i + 1, end))
    return framing, out


def base_assignments(inv, n, bases=None):
    """N tier-1 agent assignments. No shared dip read set: tier 1 chooses no splits."""
    todo = set(keys(inv))
    if bases is not None:
        rep = audit_bases(inv, bases)
        todo = set(rep["unseeded"]) | set(rep["drifted"]) | set(rep["rules"])
    out = []
    for i, group in enumerate(batches({c: s for c, s in inv.items()
                                       if any(f"{c}/{x}" in todo for x in s)} or inv, n), 1):
        lines, total = [], 0
        for cls in group:
            spans, cost = ranges(cls)
            total += cost
            picked = [x for x in inv[cls] if f"{cls}/{x}" in todo]
            if not picked:
                continue
            r = "  ".join(f"{k} {v[0]}-{v[1]}" for k, v in spans.items())
            lines.append(f"Read ONLY these ranges of listo-build/data/classes/{cls}.md: {r}")
            lines.append(f"Profile these {len(picked)} keys, verbatim:")
            lines += [f"  {cls}/{x}" for x in picked]
            lines.append("")
        fr, sp = spell_ranges()
        lines.append("Spell access — read these too; the mods change caster lists enormously:")
        lines.append(f"  listo-build/data/listo-10.2-spells.md  how-access-works {fr[0]}-{fr[1]}")
        for cls in group:
            if cls in sp:
                lines.append(f"  listo-build/data/listo-10.2-spells.md  {cls} {sp[cls][0]}-{sp[cls][1]}")
        lines.append("")
        n_keys = sum(1 for cls in group for x in inv[cls] if f"{cls}/{x}" in todo)
        out.append(f"## tier-1 agent {i}/{n} — {', '.join(group)} "
                   f"({n_keys} subclasses, ~{total} tok of class text)\n\n" + "\n".join(lines))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--list", action="store_true", help="print the subclass inventory")
    ap.add_argument("--check", action="store_true", help="diff the seeds against it")
    ap.add_argument("--promote", action="store_true", help="apply the floors and the bar")
    ap.add_argument("--limit", type=int, default=ROSTER_LIMIT,
                    help="with --promote: ration the roster to N builds (floors first, then the "
                         "bar). Omit to score every viable build and select downstream.")
    ap.add_argument("--assign", type=int, metavar="N",
                    help="split the work into N sweep-agent assignments and print them")
    ap.add_argument("--all", action="store_true",
                    help="with --assign: re-sweep everything, not only what is stale")
    ap.add_argument("--stamp", action="store_true",
                    help="record current source and brief hashes on every seed (run after merging a sweep)")
    ap.add_argument("--scored", metavar="ADDR,ADDR|@FILE|all",
                    help="with --stamp: mark these build addresses scored under the current rubric. "
                         "Subclass headings contain commas, so pass `@path` to read one address per "
                         "line, or `all` for the whole promoted roster")
    ap.add_argument("--seeds", default=os.path.join(ASSETS, "chassis-seeds.json"))
    ap.add_argument("--bases", action="store_true",
                    help="operate on the tier-1 base profiles in assets/subclass-bases.json "
                         "rather than the legacy sweep seeds")
    ap.add_argument("--bases-file", default=os.path.join(ASSETS, "subclass-bases.json"))
    a = ap.parse_args()

    if a.bases:
        inv = inventory()
        have = (load_bases(a.bases_file)
                if os.path.exists(a.bases_file) else {})
        if a.assign:
            for blk in base_assignments(inv, a.assign, None if a.all else have):
                print(blk)
            return
        rep = audit_bases(inv, have)
        if a.stamp:
            src, dep = {c: digests(c) for c in inv}, deps_hash(BASE_DEPS)
            for k, b in have.items():
                cls, sub = k.split("/", 1)
                if sub in src.get(cls, {}):
                    b["src"], b["base_deps"] = src[cls][sub], dep
            doc = load_bases.doc
            with open(a.bases_file, "w") as fh:
                json.dump(doc, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
            print(f"stamped {len(have)} base profiles", file=sys.stderr)
            return
        n_cand = sum(1 for b in have.values() if b["verdict"] == "candidate")
        print(f"{len(have)} base profiles, {len(rep['want'])} subclasses; {n_cand} candidate")
        bad = False
        for label in ("unseeded", "stale", "drifted", "rules"):
            if rep[label]:
                bad = True
                print(f"{label} ({len(rep[label])}): " + ", ".join(rep[label][:8])
                      + (" ..." if len(rep[label]) > 8 else ""), file=sys.stderr)
        print("base profiles cover every subclass and are current" if not bad
              else "the tier-1 pass is not current", file=sys.stderr)
        sys.exit(1 if bad else 0)

    if not (a.list or a.check or a.promote or a.assign or a.stamp):
        ap.error("pick one of --list, --check, --promote, --assign, --stamp")

    try:
        inv = inventory()
        if a.list:
            for cls, subs in inv.items():
                print(f"{cls} ({len(subs)})")
                for s in subs:
                    print(f"  {s}")
            print(f"\n{sum(len(s) for s in inv.values())} subclasses across {len(inv)} classes")
            return

        if a.assign:
            todo = set(keys(inv))
            if not a.all and os.path.exists(a.seeds):
                rep = audit(inv, load(a.seeds))
                todo = set(rep["unseeded"]) | set(rep["drifted"]) | set(rep["rules"])
                if not todo:
                    print("# nothing to sweep — every seed is current", file=sys.stderr)
                    return
                print(f"# {len(todo)} of {len(keys(inv))} subclasses need a seed; "
                      f"the rest are cached\n")
            dips = dip_ranges()
            dip_cost = sum(
                sum(len(l) + 1 for l in
                    open(os.path.join(CLASSES, c + ".md")).read().split("\n")[lo - 1:hi]) // 4
                for c, (lo, hi) in dips.items())
            shared = ("Shared read set — EVERY agent reads all of these. They are what a split's\n"
                      "second class must be justified from:\n"
                      + "".join(f"  listo-build/data/classes/{c}.md  dip value {lo}-{hi}\n"
                               for c, (lo, hi) in dips.items()))
            work = {c: [x for x in subs if f"{c}/{x}" in todo] for c, subs in inv.items()}
            work = {c: subs for c, subs in work.items() if subs}
            n = min(a.assign, len(work))
            total = 0
            for i, group in enumerate(batches(work, n), 1):
                cost = sum(ranges(c)[1] for c in group)
                total += cost
                print(f"## agent {i}/{n} — {', '.join(group)} "
                      f"({sum(len(work[c]) for c in group)} subclasses, "
                      f"~{cost + dip_cost} tok incl. the shared set)\n")
                print(shared)
                for cls in group:
                    spans, _ = ranges(cls)
                    where = "  ".join(f"{k} {lo}-{hi}" for k, (lo, hi) in sorted(spans.items()))
                    print(f"Read ONLY these ranges of "
                          f"listo-build/data/classes/{cls}.md: {where}")
                    print(f"Seed these {len(work[cls])} keys, verbatim:")
                    for sub in work[cls]:
                        print(f"  {cls}/{sub}")
                    print()
            print(f"# {total} tok of per-agent reading plus {dip_cost} tok of shared dip "
                  f"sections each: {total + dip_cost * n} tok across {n} agents")
            return

        seeds = load(a.seeds)
        rep = audit(inv, seeds)

        if a.stamp:
            doc, now = load.doc, deps_hash("seed")
            for k, sd in seeds.items():
                if k in rep["want"]:
                    sd["src"], sd["seed_deps"] = rep["want"][k], now
            if a.scored:
                score_h, cand = deps_hash("score"), builds(seeds)
                # A build address ends in `:<niche>` but *starts* with a subclass heading, and
                # several of those carry commas. So a comma-joined list cannot address every
                # build in the inventory; `@file` and `all` can.
                if a.scored == "all":
                    addrs = sorted(promote(seeds)[1])
                elif a.scored.startswith("@"):
                    addrs = [l.strip() for l in open(a.scored[1:]) if l.strip()]
                else:
                    addrs = a.scored.split(",")
                for addr in addrs:
                    _require(addr in cand, f"--scored: {addr!r} is not a build address")
                    k, niche = addr.rsplit(":", 1)
                    seeds[k]["builds"][niche]["score_deps"] = score_h
            with open(a.seeds, "w") as fh:
                json.dump(doc, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
            print(f"stamped {len(seeds)} seeds"
                  + (f", {len(addrs)} builds scored" if a.scored else ""),
                  file=sys.stderr)
            return

        blocking = rep["unseeded"] + rep["stale"] + rep["drifted"] + rep["rules"]
        if a.check or blocking:
            for label, ks in (("unseeded", rep["unseeded"]),
                              ("stale (no such subclass)", rep["stale"]),
                              ("drifted (source text changed)", rep["drifted"]),
                              ("rules changed (re-seed under the current brief)", rep["rules"])):
                for k in ks:
                    print(f"{label}: {k}", file=sys.stderr)
            counts = collections.Counter(x["verdict"] for x in seeds.values())
            print(f"{len(seeds)} seeds, {len(keys(inv))} subclasses; "
                  + ", ".join(f"{v} {n}" for n, v in sorted(counts.items())), file=sys.stderr)
            if rep["rescore"]:
                print(f"re-score ({len(rep['rescore'])}, the rubric or scoring model moved): "
                      + ", ".join(rep["rescore"]), file=sys.stderr)
            if rep["unscored"]:
                print(f"never scored ({len(rep['unscored'])}): "
                      + ", ".join(rep["unscored"]), file=sys.stderr)
            if blocking:
                sys.exit(f"{len(rep['unseeded'])} unseeded, {len(rep['stale'])} stale, "
                         f"{len(rep['drifted'])} drifted, {len(rep['rules'])} under old rules "
                         f"— the sweep is not current")
            if a.check:
                print("seeds cover every subclass and are current", file=sys.stderr)
                return

        a_limit = a.limit
        reasons, cand = promote(seeds, a_limit)
        print(f"# {len(reasons)} of {len(cand)} builds promoted, from "
              f"{sum(1 for x in seeds.values() if x['verdict'] == 'candidate')} candidate subclasses\n")
        for a in sorted(reasons, key=lambda a: (-cand[a]["peak"], a)):
            b = cand[a]
            print(f'{b["chassis"]:14} {b["peak"]} {b["peak_axis"]:8} '
                  f'{b["niche"]:15} {reasons[a]:12} {b["split"]}  [{a}]')
        print("\n# not promoted, grouped for caveats.excluded\n")
        groups = collections.defaultdict(list)
        for a, b in cand.items():
            if a not in reasons:
                # A build can miss for two different reasons and they must not be conflated:
                # too weak, or strong enough but past the roster limit. Reporting the second as
                # the first would tell a reader the ledger judged it poor when it did not.
                why = ("under the bar" if b["peak"] < BAR else
                       f"at or over the bar, past the roster limit of {a_limit}") \
                    if a_limit is not None else "not viable"
                groups[f'{b["niche"]}, {why}'].append(f'{b["chassis"]} ({b["peak"]})')
        for k, s in seeds.items():
            if s["verdict"] == "dupe":
                groups[f'same chassis as {s["dupe_of"]}'].append(k)
            elif s["verdict"] == "none":
                groups["no viable 20-level expression"].append(k)
        for g, items in sorted(groups.items()):
            print(f'- <b>{g}</b> ({len(items)}): {", ".join(sorted(items))}')
    except (SeedError, FileNotFoundError, json.JSONDecodeError) as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
