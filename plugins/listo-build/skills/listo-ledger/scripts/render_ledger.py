#!/usr/bin/env python3
"""Render a Listo pairing ledger from a JSON data file.

    scripts/render_ledger.py ledger.json > out.html
    scripts/render_ledger.py ledger.json -o out.html

Author the CHASSIS SCORES and the PROSE. Everything derived is produced here:
pair combining, tempo and the non-tempo blocks, reach discounts, idle-body
flags, melee lock, holes, the full carry x support field table, the roster order, the
entry list (best partner per carry, ranked) and every number quoted in a
variation line. See assets/ledger-schema.md.

Strings pass through as HTML: inline <b>/<em>/<code> are fine.
"""
import json, sys, os, itertools

HERE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "listo-build", "scripts"))

# The scoring model lives in ONE place: listo-build/scripts/scoring.py, which
# implements listo-build/references/scoring-model.md. Never reimplement it here.
from scoring import (                                       # noqa: E402
    KEYS, LABELS, AXES, KINDS, KINDNAME, KIND_MAX, ACTS, BANDS, MIX, FLAG,
    REACH, REACH_LABEL, SAV_IDX, WEIGHTS, TEMPO, RESILIENCE,
    ScoringError, score, norm, derive_saves, validate_chassis)


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
    head = "".join(f"<th><span>{a}</span></th>" for a in AXES)
    rows = []
    for act in ACTS:
        r = rec["acts"][act]
        rows.append(f'<tr><th>{act}</th>'
                    + "".join(cell(r["pair"][k]) for k in KEYS)
                    + f'<td class="tot">{r["tempo"]*100:.0f}%</td>'
                    + f'<td class="tot">{r["nontempo"]*100:.0f}%</td></tr>')
    return (f'<div class="scroll"><table class="matrix"><thead><tr><th>Act</th>{head}'
            '<th class="tot" title="damage + control, capped by Actions"><span>Tempo</span></th>'
            '<th class="tot" title="resilience, duration, utility"><span>Rest</span></th>'
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
    head = "".join(f"<th><span>{a}</span></th>" for a in AXES)
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
    return f'''<article class="rost" id="r-{key.lower()}">
<header><h3>{disp(key)}<span class="role {ch["role"]}">{ch["role"]}</span></h3>
<p class="chassis">{ch.get("split","")}{meta}</p>
<p class="chassis reachline">reach: <b>{REACH_LABEL[ch["reach"]]}</b></p></header>
{f'<p class="note">{ch["note"]}</p>' if ch.get("note") else ""}
<div class="scroll"><table class="matrix"><thead><tr><th>Act</th>{head}
<th class="tot"><span>Sum</span></th></tr></thead><tbody>{rows}</tbody></table></div></article>'''


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

    carries  = [k for k in C if C[k]["role"] == "carry"]
    supports = [k for k in C if C[k]["role"] == "support"]
    if not carries or not supports:
        sys.exit("need at least one carry and one support")

    field = sorted((score(C, a, b) for a, b in itertools.product(carries, supports)),
                   key=lambda r: -r["score"])
    by_pair = {(r["a"], r["b"]): r for r in field}

    # entries: each carry's best partner, ranked, capped at entry_limit
    best = {}
    for r in field:
        best.setdefault(r["a"], r)
    ranked = sorted(best.values(), key=lambda r: -r["score"])
    limit = d.get("entry_limit", len(ranked))
    kept, cut = ranked[:limit], ranked[limit:]

    prose = d.get("entries", {})
    missing = [r["a"] for r in kept if r["a"] not in prose]
    if missing:
        sys.exit("entry prose missing for: " + ", ".join(missing))

    entries = []
    for i, rec in enumerate(kept, 1):
        e = prose[rec["a"]]
        vars_html = []
        for v in e.get("vars", []):
            if "partner" in v:
                p = v["partner"]
                vr = by_pair.get((rec["a"], p))
                if vr is None:
                    sys.exit(f"entry {rec['a']}: no pairing with {p}")
                vars_html.append(f'<li><b>+ {disp(p)}</b> &mdash; {vr["score"]} &middot; '
                                 f'tempo {vr["tempo"]*100:.0f}% &middot; rest {vr["nontempo"]*100:.0f}%. {v.get("note","")}</li>')
            else:
                vars_html.append(f'<li>{v["text"]}</li>')
        entries.append(f'''<article class="entry">
<header class="ehead">
  <div class="rank">{i:02d}</div>
  <div class="etitle">
    <h3>{e["name"]}</h3>
    <p class="tag">{e.get("tag","")}</p>
    <p class="members"><a href="#r-{rec["a"].lower()}">{disp(rec["a"])}</a>
      <span class="plus">+</span>
      <a href="#r-{rec["b"].lower()}">{disp(rec["b"])}</a></p>
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
  <p><span class="lead">Reads as.</span> {e["verdict"]}</p>
  <p><span class="lead cost">Costs.</span> {e["cost"]}</p>
  <ul class="vars">{"".join(vars_html)}</ul>
</div></article>''')

    cut_line = ""
    if cut:
        names = ", ".join(f'<b>{disp(r["a"])}</b> ({r["score"]})' for r in cut)
        cut_line = (f' {len(kept)} carries make the cut; {names} '
                    f'{"does" if len(cut)==1 else "do"} not, and stay in the field table '
                    f'and the roster.')

    ranked_key = {(r["a"], r["b"]): i for i, r in enumerate(kept, 1)}
    frows = "".join(
        f'<tr class="{"in" if (r["a"], r["b"]) in ranked_key else ""}">'
        f'<th scope="row">'
        + (f'<span class="ent">{ranked_key[(r["a"], r["b"])]:02d}</span>'
           if (r["a"], r["b"]) in ranked_key else "")
        + f'{disp(r["a"])} + {disp(r["b"])}</th>'
        + "".join(f'<td class="v v{min(5, round(sum(r["acts"][a]["pair"][k] for a in ACTS)/3/KIND_MAX[KINDS[k]]*5))}">'
                  f'{sum(r["acts"][a]["pair"][k] for a in ACTS)}</td>' for k in KEYS)
        + "".join(f'<td class="n{" sep" if i == 0 else ""}">{r["acts"][a]["tempo"]*100:.0f}</td>'
                  for i, a in enumerate(ACTS))
        + f'<td class="n dm sep">{r["nontempo"]*100:.0f}</td>'
          f'<td class="n b">{r["score"]}</td></tr>'
        for r in field)

    # roster order is derived, so a chassis added later can never be dropped
    peak = {}
    for r in field:
        peak[r["a"]] = max(peak.get(r["a"], 0), r["score"])
        peak[r["b"]] = max(peak.get(r["b"], 0), r["score"])
    order = (sorted(carries,  key=lambda k: -peak[k])
             + sorted(supports, key=lambda k: -peak[k]))
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
  <h2>{d.get("method",{}).get("h2","Two numbers, each counted once")}</h2>
  <div class="method">{"".join(
      f'<div><b>{c["title"]}</b><p>{c["body"]}</p></div>' for c in d.get("method",{}).get("cards",[]))}
    <div><b>Axis kinds</b><p>How a second source of each axis combines.</p>
      <table class="plain"><tbody>{kindrows}</tbody></table></div>
  </div>
</section>

<section>
  <h2>The full field</h2>
  <p class="sublede">{len(field)} pairings, {len(carries)} carries &times; {len(supports)} supports.
  Axis values summed across acts, then tempo per act. Sorted by score.</p>
  <div class="scroll"><table class="field matrix"><thead><tr><th></th><th>Pairing</th>
    {"".join(f"<th>{a}</th>" for a in AXES)}
    <th title="tempo %, act I">I</th><th title="tempo %, act II">II</th>
    <th title="tempo %, act III">III</th>
    <th title="resilience, duration, utility">Rest</th><th>Score</th></tr></thead>
    <tbody>{frows}</tbody></table></div>
</section>

<section>
  <h2>The entries</h2>
  <p class="sublede">Ranked by score, in the same order as the field table above.
  <b>One entry per carry</b>, headlined by that carry's highest-scoring partner; every other
  partner for the same carry is a variation beneath it rather than an entry of its own.{cut_line}</p>
  {"".join(entries)}
</section>

<section>
  <h2>The roster</h2>
  <p class="sublede">Every chassis, carries first, each ranked by the best score it reaches anywhere
  in the field. Act bands: {" &middot; ".join(f"{a} {b}" for a, b in zip(ACTS, BANDS))}.</p>
  {roster}
</section>

<section>
  <h2>{d.get("caveats",{}).get("h2","What this ledger does not include")}</h2>
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
