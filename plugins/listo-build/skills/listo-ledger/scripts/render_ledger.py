#!/usr/bin/env python3
"""Render a Listo pairing ledger from a JSON data file.

    scripts/render_ledger.py ledger.json > out.html
    scripts/render_ledger.py ledger.json -o out.html

Author the CHASSIS SCORES and the PROSE. Everything derived is produced here:
pair combining, tempo and the non-tempo blocks, reach discounts, idle-body
flags, melee lock, holes, every chassis against every other, the frontier and the
field table drawn from it, the roster order, the entry list (best partner per
chassis, ranked) and every number quoted in a variation line.
See assets/ledger-schema.md.

Strings pass through as HTML: inline <b>/<em>/<code> are fine.
"""
import json, sys, os, re, itertools, collections

HERE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "listo-build", "scripts"))

# The scoring model lives in ONE place: listo-build/scripts/scoring.py, which
# implements listo-build/references/scoring-model.md. Never reimplement it here.
from scoring import (BLOCKS,                                       # noqa: E402
    KEYS, LABELS, AXES, KINDS, KINDNAME, KIND_MAX, ACTS, BANDS, MIX, FLAG,
    REACH, REACH_LABEL, SAV_IDX, WEIGHTS, TEMPO, RESILIENCE,
    ScoringError, score, norm, derive_saves, validate_chassis)


# ── column help ──────────────────────────────────────────────────────────────
# Built from the model's own metadata so a tooltip cannot drift from the arithmetic it describes.
# "Rest" in particular was printed in three places and defined in none.
_AXIS_WHAT = {
    "st":     "Damage aimed at one target.",
    "aoe":    "Damage that reaches several targets at once.",
    "dur":    "Staying upright under fire — hit points, armour, resistances.",
    "act":    "Turns, bonus actions and reactions. Caps tempo rather than adding to it: a pair "
              "cannot deliver more than it has actions to deliver.",
    "ctrl_s": "Locking down one dangerous creature.",
    "ctrl_a": "Shutting down a group at once.",
    "rsc":    "Healing, revives, and getting a downed body back on its feet.",
    "skl":    "The checks the run makes without warning: traps and caches (Perception 15-25), "
              "secret doors (Investigation 15-20), town dialogue (Persuasion, at the act's band). "
              "Rung 5 is unreachable — no two-body party covers the detection load.",
    "sav":    "Resisting what would disable you. Each body rolls its own, so a proficiency on one "
              "does nothing for the other.",
    "end":    "Lasting between rests — spell slots, charges, short-rest recovery.",
}
_KIND_HOW = {
    "add":     "the two bodies sum",
    "comp":    "higher + half the lower",
    "per":     "the pair takes the LOWER of the two",
    "derived": "derived from recorded evidence, never authored",
}


def axis_help(k):
    """Tooltip text for one axis key."""
    i = KEYS.index(k)
    return (f"{LABELS[i]} — {_AXIS_WHAT[k]} "
            f"{KINDNAME[KINDS[k]]}: {_KIND_HOW[KINDS[k]]}, cap {KIND_MAX[KINDS[k]]}.")


def axis_th(a, span=True, rowspan=1):
    """A header cell for the axis displayed as `a`, carrying its tooltip."""
    k = KEYS[AXES.index(a)]
    inner = f"<span>{a}</span>" if span else a
    rs = f' rowspan="{rowspan}"' if rowspan > 1 else ""
    return f'<th{rs} title="{axis_help(k)}">{inner}</th>'


def h2(slug, text):
    """A section heading that is its own anchor.

    The id is authored, not slugged from the text: the method and caveats headings are
    configurable in the ledger data, and an id derived from prose would change the moment
    somebody reworded a title, silently breaking every link anyone had saved.
    """
    return f'<h2 id="{slug}"><a class="anchor" href="#{slug}">{text}</a></h2>'


def act_subheads():
    """The act row under the Tempo and Rest group headers.

    The first column of each group carries `sep` so its vertical rule lines up with the one the
    body puts on the matching `td`, and the cells are right-aligned to the same 9px as `td.n` —
    without that the numbers and their headings sit 4px apart and read as misaligned.
    """
    return "".join(f'<th class="sub{" sep" if i == 0 else ""}">{a}</th>'
                   for _grp in range(2) for i, a in enumerate(ACTS))


REST_HELP = ("Rest — everything that is not tempo, as a weighted percentage: resilience "
             "(durability, saves, rescue), duration (endurance) and utility (skills). "
             "Tempo and Rest are weighted 50/50 in the score.")
TEMPO_HELP = ("Tempo — damage and control actually delivered, capped by action economy and "
              "discounted for reach, idle bodies and holes.")
SCORE_HELP = ("Score — 50 x tempo + 50 x rest, averaged across the three acts, then multiplied "
              "by a contention factor when both bodies share a class.")


# ── fragments ────────────────────────────────────────────────────────────────
def cell(v):
    return f'<td class="v v{v}">{v}</td>'


def chips(rec, disp):
    out = []
    if rec["locked"]:
        out.append('<span class="chip warn">melee-locked · both bodies must close</span>')
    for h in rec["holes"]:
        out.append(f'<span class="chip warn">{LABELS[KEYS.index(h)].lower()} hole</span>')
    for who, kind in sorted(rec["flags"]):
        out.append(f'<span class="chip">{disp(who)} idles in {kind} fights</span>')
    if not out:
        out.append('<span class="chip ok">no idle body, no hole</span>')
    return "".join(out)


def radar_table(rec):
    head = "".join(axis_th(a) for a in AXES)
    rows = []
    for act in ACTS:
        r = rec["acts"][act]
        rows.append(f'<tr><th>{act}</th>'
                    + "".join(cell(r["pair"][k]) for k in KEYS)
                    + f'<td class="tot">{r["tempo"]*100:.0f}%</td>'
                    + f'<td class="tot">{r["nontempo"]*100:.0f}%</td></tr>')
    return (f'<div class="scroll"><table class="matrix"><thead><tr><th>Act</th>{head}'
            f'<th class="tot" title="{TEMPO_HELP}"><span>Tempo</span></th>'
            f'<th class="tot" title="{REST_HELP}"><span>Rest</span></th>'
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def dmg_table(rec, disp):
    rows = []
    for act in ACTS:
        r = rec["acts"][act]
        wc, wb = MIX[act]
        f = lambda u, w: f'<td class="{"crit" if u < FLAG and w >= .40 else ""}">{u:.2f}</td>'
        rows.append(f'<tr><th>{act}</th>' + f(r["ua"][0], wc) + f(r["ua"][1], wb)
                    + f(r["ub"][0], wc) + f(r["ub"][1], wb)
                    + f'<td class="mix">{r["tempo"]*100:.0f}%</td></tr>')
    A, B = disp(rec["a"]), disp(rec["b"])
    return ('<div class="scroll"><table class="matrix dmg"><thead>'
            f'<tr><th rowspan="2">Act</th><th colspan="2">{A}</th>'
            f'<th colspan="2">{B}</th><th rowspan="2">Tempo</th></tr>'
            '<tr><th>crowd</th><th>prio</th><th>crowd</th><th>prio</th></tr></thead>'
            '<tbody>' + "".join(rows) + '</tbody></table></div>')


def roster_block(key, ch, disp):
    head = "".join(axis_th(a) for a in AXES)
    rows = []
    for act in ACTS:
        vals = list(ch["scores"][act])
        blk = ch["saves"][act]
        vals[SAV_IDX] = derive_saves(blk["prof"], blk["boosters"],
                                     ch.get("concentration", False))
        rows.append(f'<tr><th>{act}</th>' + "".join(cell(v) for v in vals)
                    + f'<td class="tot">{sum(vals)}</td></tr>')
    rows = "".join(rows)
    meta = f'<span class="dot">·</span>{ch["meta"]}' if ch.get("meta") else ""
    # A split carries its subclasses as parentheticals — `Warlock 17 (The Hexblade)`. They are the
    # part a reader actually needs to rebuild the body, so they are kept, just set back from the
    # class and level that carry the arithmetic.
    split = re.sub(r"\(([^)]*)\)", r'<span class="sub">\1</span>', ch.get("split", ""))
    return f'''<article class="rost" id="r-{key.lower()}">
<header><h3><a class="anchor" href="#r-{key.lower()}">{disp(key)}</a></h3>
<p class="chassis">{split}{meta}</p>
<p class="chassis reachline">reach: <b>{REACH_LABEL[ch["reach"]]}</b></p></header>
{f'<p class="note">{ch["note"]}</p>' if ch.get("note") else ""}
{f'<p class="note lede-strength"><b>Strong because</b> {ch["strength"]}</p>' if ch.get("strength") else ""}
{f'<p class="note lede-wants"><b>Wants a partner who</b> {ch["wants"]}</p>' if ch.get("wants") else ""}
<div class="scroll"><table class="matrix"><thead><tr><th>Act</th>{head}
<th class="tot"><span>Sum</span></th></tr></thead><tbody>{rows}</tbody></table></div></article>'''


def frontier(field):
    """Indices of the pairings no other pairing beats on all four blocks.

    Selection has to run on the blocks, not the score. The whole argument for four blocks is
    that a total cannot see a pairing that trades damage for resilience — so cutting by score
    would discard exactly what the model was built to preserve. A pairing survives here if it is
    best at *something*.

    Sorted by the first block descending, so a candidate can only be dominated by one already
    kept; a final pass clears the ties that ordering alone cannot.
    """
    order = sorted(range(len(field)), key=lambda i: -field[i]["blocks"][BLOCKS[0]])
    kept = []
    for i in order:
        p = field[i]["blocks"]
        if not any(all(field[j]["blocks"][b] >= p[b] for b in BLOCKS)
                   and any(field[j]["blocks"][b] > p[b] for b in BLOCKS) for j in kept):
            kept.append(i)
    return [i for i in kept
            if not any(all(field[j]["blocks"][b] >= field[i]["blocks"][b] for b in BLOCKS)
                       and any(field[j]["blocks"][b] > field[i]["blocks"][b] for b in BLOCKS)
                       for j in kept if j != i)]


def _delabel(text, label):
    """Strip a leading `Reads as.` / `Costs.` from authored prose.

    The template supplies the label, and the house pattern asks authors to open with it too, so
    both conventions are in the wild and the two together render it twice. The label belongs to
    the template — it is styled, and it must not depend on what an author happened to type.
    """
    t = (text or "").lstrip()
    low = t.lower()
    for opener in (label.lower() + ".", label.lower()):
        if low.startswith(opener):
            return t[len(opener):].lstrip()
    return t


def details(block, open_=False):
    if not block or not block.get("items"):
        return ""
    items = "".join(f"<li>{i}</li>" for i in block["items"])
    lead = f'<p class="lead">{block["lead"]}</p>' if block.get("lead") else ""
    return (f'<details{" open" if open_ else ""}><summary>{block["summary"]}</summary>'
            f'<ul>{items}</ul>{lead}</details>')


# ── build ────────────────────────────────────────────────────────────────────
def render(d):
    C = d["chassis"]
    for k, ch in C.items():
        ch.setdefault("display", k)
        validate_chassis(k, ch)
    disp = lambda k: C[k]["display"]

    if len(C) < 2:
        sys.exit("need at least two chassis to form a pairing")

    # Every unordered pair. The pair score is symmetric — combine() is add/comp/per, all
    # order-independent — so (a, b) and (b, a) are one row, not two.
    field = sorted((score(C, a, b) for a, b in itertools.combinations(C, 2)),
                   key=lambda r: -r["score"])
    by_pair = {(r["a"], r["b"]): r for r in field}

    # Selection: the Pareto frontier over the four blocks. Everything else stays in the field
    # table as the audit trail — it is dominated, not deleted.
    front_idx = set(frontier(field))
    front = [field[i] for i in sorted(front_idx, key=lambda i: -field[i]["score"])]
    front_pairs = {(r["a"], r["b"]) for r in front}
    relevant = {k for r in front for k in (r["a"], r["b"])}

    # entries: each chassis's best partner, ranked, capped at entry_limit. Both sides of a
    # pairing count, since neither is privileged as "the carry" any more — so an entry records
    # *which* chassis it headlines (`me`) separately from the record's own a/b labels.
    # A body with no weak axis is the universal best partner by construction: three axes combine
    # as min() and five as hi + lo//2, so a partner who is decent everywhere never subtracts. The
    # consequence is that "each chassis's best partner" converges on ONE body and every entry
    # shares it — Kinship and Lunar did it in v3, Cloister in v4, Lectern here at 262 of 264.
    # That fact is worth stating once, not printing twenty times, so a partner is capped.
    cap = d.get("entry_partner_cap", 3)
    ranked_all = {}
    for r in front:
        for me, other in ((r["a"], r["b"]), (r["b"], r["a"])):
            ranked_all.setdefault(me, []).append((r["score"], other, r))
    best, used = {}, collections.Counter()
    for me in sorted(ranked_all, key=lambda m: -max(x[0] for x in ranked_all[m])):
        for _s, other, r in sorted(ranked_all[me], key=lambda t: -t[0]):
            if used[other] >= cap:
                continue
            best[me] = (me, other, r)
            used[other] += 1
            break

    # When two chassis are each other's best partner they would otherwise headline the identical
    # pairing twice. Keep the first and let the second appear as that entry's partner instead.
    ranked, seen = [], set()
    for ent in sorted(best.values(), key=lambda t: -t[2]["score"]):
        pair_id = (ent[2]["a"], ent[2]["b"])
        if pair_id in seen:
            continue
        seen.add(pair_id)
        ranked.append(ent)

    limit = d.get("entry_limit", len(ranked))
    kept, cut = ranked[:limit], ranked[limit:]

    prose = d.get("entries", {})
    missing = sorted({me for me, _, _ in kept if me not in prose})
    if missing:
        sys.exit("entry prose missing for: " + ", ".join(missing))

    # The pairing NAME is derived, not authored. It used to be printed from `name` while the
    # members line beside it was computed, so the two could disagree — and once a selection rule
    # changed, every heading kept pointing at the partner the prose had been written for while
    # the numbers underneath came from a different pairing. That is precisely the staleness this
    # format exists to prevent, so the heading is computed and a `name` that contradicts it is a
    # hard error rather than a silent override: prose written about the wrong partner is worse
    # than no prose.
    stale = []
    for me, other, _rec in kept:
        want = {disp(me), disp(other)}
        got = {p.strip() for p in prose[me].get("name", "").replace("&amp;", "&").split("&")}
        if prose[me].get("name") and got != want:
            stale.append(f"{me}: prose names {prose[me]['name']!r}, selection paired it with {disp(other)}")
    if stale:
        sys.exit("entry prose is stale — written for a different partner:\n  " + "\n  ".join(stale))

    entries = []
    for i, (me, other, rec) in enumerate(kept, 1):
        e = prose[me]
        vars_html = []
        for v in e.get("vars", []):
            if "partner" in v:
                p = v["partner"]
                # A variant always swaps the PARTNER and keeps the chassis this entry headlines,
                # because the entry exists to be about that chassis. Rendering it as a bare
                # "+ Coda" left the reader to guess which half of the heading was leaving, so the
                # line names the body going out and the body coming in: "Silvercrit -> Coda".
                # The retained chassis is the heading's other half and is not repeated.
                if p == other:
                    sys.exit(f"entry {me}: variant names {p}, which is already the partner")
                if p == me:
                    sys.exit(f"entry {me}: variant names the chassis the entry headlines")
                # by_pair holds one direction per unordered pair; look both ways.
                vr = by_pair.get((me, p)) or by_pair.get((p, me))
                if vr is None:
                    sys.exit(f"entry {me}: no pairing with {p}")
                vars_html.append(
                    f'<li><b>{disp(other)} &rarr; {disp(p)}</b> &mdash; {vr["score"]} &middot; '
                    f'tempo {vr["tempo"]*100:.0f}% &middot; '
                    f'rest {vr["nontempo"]*100:.0f}%. {v.get("note","")}</li>')
            else:
                vars_html.append(f'<li>{v["text"]}</li>')
        entries.append(f'''<article class="entry" id="e-{me.lower()}">
<header class="ehead">
  <div class="rank"><a href="#e-{me.lower()}" title="Link to this entry">{i:02d}</a></div>
  <div class="etitle">
    <h3><a class="anchor" href="#e-{me.lower()}">{disp(me)} &amp; {disp(other)}</a></h3>
    <p class="tag">{e.get("tag","")}</p>
    <p class="members"><a href="#r-{me.lower()}">{disp(me)}</a>
      <span class="plus">+</span>
      <a href="#r-{other.lower()}">{disp(other)}</a></p>
  </div>
  <div class="score"><span class="num">{rec["score"]}</span><span class="lbl">rank score</span>
    <span class="sub">tempo {rec["tempo"]*100:.0f}% &middot; damage + control, capped by Actions</span>
    <span class="sub">resilience &middot; duration &middot; utility {rec["nontempo"]*100:.0f}%</span></div>
</header>
<div class="chips">{chips(rec, disp)}</div>
<div class="cols">
  <div class="col"><h4>Pair profile</h4>{radar_table(rec)}</div>
  <div class="col"><h4>Delivered damage</h4>{dmg_table(rec, disp)}</div>
</div>
<div class="prose">
  <p><span class="lead">Reads as.</span> {_delabel(e["verdict"], "Reads as")}</p>
  <p><span class="lead cost">Costs.</span> {_delabel(e["cost"], "Costs")}</p>
  <ul class="vars">{"".join(vars_html)}</ul>
</div></article>''')

    cut_line = ""
    if cut:
        names = ", ".join(f'<b>{disp(me)}</b> ({r["score"]})' for me, _, r in cut)
        cut_line = (f' {len(kept)} chassis make the cut; {names} '
                    f'{"does" if len(cut)==1 else "do"} not, and stay in the roster.')

    ranked_key = {(r["a"], r["b"]): (i, me) for i, (me, _, r) in enumerate(kept, 1)}

    # The field table is the audit trail, not the whole cartesian product: C(150,2) is 11,175 rows
    # and about 5MB of HTML that nobody reads. Every frontier pairing is always shown — those are
    # the ones selection acted on — and the remainder is filled with the highest-scoring dominated
    # pairings up to `field_limit`. What was dropped is stated, never silently truncated.
    flimit = d.get("field_limit", 500)
    shown = [r for r in field if (r["a"], r["b"]) in front_pairs]
    if len(shown) < flimit:
        shown += [r for r in field if (r["a"], r["b"]) not in front_pairs][:flimit - len(shown)]
    shown.sort(key=lambda r: -r["score"])
    dropped = len(field) - len(shown)

    frows = "".join(
        f'<tr class="{"in" if (r["a"], r["b"]) in ranked_key else ""}'
        f'{" front" if (r["a"], r["b"]) in front_pairs else ""}">'
        f'<th scope="row">'
        + (f'<a class="ent" href="#e-{ranked_key[(r["a"], r["b"])][1].lower()}"'
           f' title="Jump to entry {ranked_key[(r["a"], r["b"])][0]:02d}">'
           f'{ranked_key[(r["a"], r["b"])][0]:02d}</a>'
           if (r["a"], r["b"]) in ranked_key else "")
        + f'{disp(r["a"])} + {disp(r["b"])}</th>'
        + "".join(f'<td class="v v{min(5, round(sum(r["acts"][a]["pair"][k] for a in ACTS)/3/KIND_MAX[KINDS[k]]*5))}">'
                  f'{sum(r["acts"][a]["pair"][k] for a in ACTS)}</td>' for k in KEYS)
        + "".join(f'<td class="n{" sep" if i == 0 else ""}">{r["acts"][a]["tempo"]*100:.0f}</td>'
                  for i, a in enumerate(ACTS))
        # Rest is shown per act for the same reason tempo is: it moves. Across the field it
        # varies 7.2pp between a pairing's best and worst act at the median, against tempo's
        # 8.5pp, and 70% of pairings move at least 5pp. A single averaged column hid that —
        # most visibly on Skills, which swings a whole rung between Act I and Act III.
        + "".join(f'<td class="n dm{" sep" if i == 0 else ""}">'
                  f'{r["acts"][a]["nontempo"]*100:.0f}</td>'
                  for i, a in enumerate(ACTS))
        + f'<td class="n b">{r["score"]}</td></tr>'
        for r in shown)

    # roster order is derived, so a chassis added later can never be dropped
    peak = {}
    for r in field:
        peak[r["a"]] = max(peak.get(r["a"], 0), r["score"])
        peak[r["b"]] = max(peak.get(r["b"], 0), r["score"])
    order = sorted(C, key=lambda k: (k not in relevant, -peak.get(k, 0)))
    roster = "".join(roster_block(k, C[k], disp) for k in order)

    kindrows = "".join(f"<tr><td>{LABELS[i]}</td><td>{KINDNAME[KINDS[k]]}</td></tr>"
                       for i, k in enumerate(KEYS))
    facts = "".join(f"<li>{f}</li>" for f in d.get("facts", []))
    css = open(os.path.join(ASSETS, "ledger.css")).read()

    return f'''<title>{d.get("title","Pairing ledger")}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>{css}</style>
<div class="wrap">
<header class="masthead">
  <p class="eyebrow">{d.get("eyebrow","")}</p>
  <h1>{d.get("title","Pairing ledger")}</h1>
  <p class="standfirst">{d.get("lede","")}</p>
  <ul class="facts">{facts}</ul>
</header>

<section>
  {h2("method", d.get("method",{}).get("h2","Two numbers, each counted once"))}
  <div class="method">{"".join(
      f'<div><b>{c["title"]}</b><p>{c["body"]}</p></div>' for c in d.get("method",{}).get("cards",[]))}
    <div><b>Axis kinds</b><p>How a second source of each axis combines.</p>
      <table class="plain"><tbody>{kindrows}</tbody></table></div>
  </div>
</section>

<section>
  {h2("field", "The field")}
  <p class="sublede">Every one of the {len(C)} chassis was paired with every other &mdash;
  <b>{len(field)}</b> pairings scored. Axis values summed across acts, then tempo and rest
  <em>per act</em>, sorted by score. <b>{len(front)}</b> sit on the four-block frontier (marked), meaning nothing beats them
  on tempo, resilience, duration <em>and</em> utility at once; those are the ones selection acted
  on, and all of them are here.{f" The remaining rows are the highest-scoring dominated pairings; <b>{dropped}</b> further pairings were scored and are not listed." if dropped else ""}</p>
  <div class="scroll"><table class="field matrix"><thead>
    <tr><th rowspan="2" title="The two chassis, higher delivered damage first. A marked row sits on the four-block frontier: nothing beats it on tempo, resilience, duration and utility at once.">Pairing</th>
    {"".join(axis_th(a, span=False, rowspan=2) for a in AXES)}
    <th colspan="3" class="grp sep" title="{TEMPO_HELP}">Tempo</th>
    <th colspan="3" class="grp sep" title="{REST_HELP}">Rest</th>
    <th rowspan="2" title="{SCORE_HELP}">Score</th></tr>
    <tr>{act_subheads()}</tr></thead>
    <tbody>{frows}</tbody></table></div>
</section>

<section>
  {h2("entries", "The entries")}
  <p class="sublede">Ranked by score. <b>One entry per chassis</b>, headlined by its
  highest-scoring available partner &mdash; <b>no body may partner more than {cap} entries</b>,
  because the model makes a well-rounded chassis the best partner for almost everything and
  without a cap one body takes every row. That is a real property of the roster and it is stated
  here rather than printed twenty times. Every other partner for
  the same chassis is a variation beneath it rather than an entry of its own.{cut_line}</p>
  {"".join(entries)}
</section>

<section>
  {h2("roster", "The roster")}
  <p class="sublede">Every chassis, the {len(relevant)} that reach the frontier first, then those
  whose every pairing is dominated. Each ranked by the best score it reaches anywhere in the field. Act bands: {" &middot; ".join(f"{a} {b}" for a, b in zip(ACTS, BANDS))}.</p>
  {roster}
</section>

<section>
  {h2("caveats", d.get("caveats",{}).get("h2","What this ledger does not include"))}
  {details(d.get("caveats",{}).get("excluded"), True)}
  {details(d.get("caveats",{}).get("settled"), True)}
  {details(d.get("caveats",{}).get("assumptions"))}
</section>

<footer>{d.get("footer","")}</footer>
</div>
'''


def main():
    args = [a for a in sys.argv[1:]]
    out = None
    if "-o" in args:
        i = args.index("-o")
        out = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1:
        sys.exit(__doc__)
    doc = render(json.load(open(args[0])))
    if out:
        open(out, "w").write(doc)
        print(f"wrote {out} ({len(doc)} bytes)", file=sys.stderr)
    else:
        sys.stdout.write(doc)


if __name__ == "__main__":
    main()
