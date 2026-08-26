#!/usr/bin/env python3
"""Render a Listo finalists comparison from a JSON data file.

    scripts/render_finalists.py finalists.json -o out.html

One card per BUILT PAIRING, each carrying that sheet's own numbers and linking
out to it. Unlike the ledger there is no shared roster: the same chassis is a
different build on every card, because the feats, race and ladder differ by
partner, and that spread is information.

Everything derived is produced here — pair combining, coverage, damage
coverage, reach discounts, idle flags, holes, ranking and the field table.
Author the per-half scores, the prose and the sheet URL.

    scripts/render_finalists.py finalists.json --scrape sheets/
        fills `scores` for any pairing that has none, by reading the
        data-a1/a2/a3 and data-b1/b2/b3 attributes out of <slug>.html.

Strings pass through as HTML.
"""
import json, sys, os, re, html

HERE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "listo-build", "scripts"))

# One implementation of the scoring model, in listo-build/scripts/scoring.py.
from scoring import (                                       # noqa: E402
    KEYS, AXES, ACTS, MIX, FLAG, REACH, KIND_MAX, KINDS, SAV_IDX,
    ScoringError, score_bodies, derive_saves)


def split_classes(display):
    """The bare class split out of a card's display string.

    `splits` carries "Ranger 15 / Monk 3 / Cleric 2 &middot; Wood Elf &middot; Sage" — the race
    and background trail the classes behind a separator, and `scoring._classes` matches
    `^(.+?)\\s+\\d{1,2}$` per "/" segment, so the final class silently fails to parse with them
    attached. Cut at the first separator and hand `score_bodies` the classes only.
    """
    for sep in ("&middot;", "\u00b7"):
        display = display.split(sep)[0]
    return display.strip()


def score(p):
    """Adapter: a finalists pairing is two bodies rather than a chassis map.

    `split`, `types` and `meta` are passed through because the model reads all three and
    silently degrades without them: `split` drives `same_class`, and `types` plus `meta` are
    what `gear_key` needs to reach `CONTEND` instead of falling back to the blunt `SAME_CLASS`.
    A page that omitted them scored every pairing as though no two builds ever competed for an
    item — which is wrong most sharply exactly where it matters, on two bodies sharing a primary
    ability at 4x merchant prices.

    `skills` matters more bluntly still: `skills_pair` derives the Skills rung from per-act
    modifier maps and NOT from the authored rung, so a pairing that passes none derives it from
    `{}`, scores 0, and reports `skl` as a hole. Every page rendered without it flagged a Skills
    hole on every card.
    """
    def body(who):
        b = {"_id": p["names"][who], "reach": p["reach"][who],
             "scores": p["scores"][who], "saves": p["saves"][who],
             "concentration": p.get("concentration", {}).get(who, False),
             "split": split_classes(p.get("splits", {}).get(who, ""))}
        for field in ("types", "meta", "skills"):
            v = p.get(field, {}).get(who)
            if v:
                b[field] = v
        return b
    return score_bodies(body("a"), body("b"))


def scrape(slug, sheetdir):
    """Read the six per-act series straight out of a rendered pair sheet."""
    path = os.path.join(sheetdir, slug + ".html")
    if not os.path.exists(path):
        sys.exit(f"--scrape: no sheet at {path}")
    s = open(path).read()
    def series(letter):
        out = {}
        for i, act in enumerate(ACTS, 1):
            m = re.search(r'data-%s%d="([^"]*)"' % (letter, i), s)
            if not m:
                sys.exit(f"--scrape: {slug} has no data-{letter}{i}")
            row = [int(x) for x in m.group(1).split(",")]
            # A rendered pair sheet carries the RESOLVED saves value at index 8, because it
            # derived it for that pairing and drew it on the radar. The finalists model derives
            # saves itself, from the `saves` blocks, and refuses a row that arrives pre-filled —
            # rightly, since a value derived beside one partner is wrong beside another.
            row[SAV_IDX] = None
            out[act] = row
        return out
    return {"a": series("a"), "b": series("b")}


def cell(v, ax=None):
    """One matrix cell, shaded by where the value sits on THAT AXIS's own range.

    Pair values are uncapped by kind — `scoring.KIND_MAX` puts additive at 10, complementary at
    7 and personal at 5 — so shading them on a flat 0-5 ramp was wrong twice. It ran off the end
    of the palette, because `.v6`-`.v10` are not defined and those cells rendered as bare ink on
    the surface; and it lied about what it showed, because a personal 5 is *maxed* while an
    additive 5 is *half*. Normalising by `KIND_MAX` fixes both at once.

    `ax` is a `scoring.KEYS` name for a pair row, and None for a single body's own row — one
    body tops out at 5 on every axis regardless of the axis's kind, so those shade against 5 and
    are unchanged.

    The cell still prints the raw value; only the shading is normalised.
    """
    denom = KIND_MAX[KINDS[ax]] if ax else 5
    step = 0 if v <= 0 else max(1, min(5, round(5 * v / denom)))
    return f'<td class="v v{step}">{v}</td>'


def _own(p, who, act):
    """A body's own row: index 8 is null, so derive it without the pair aura."""
    vals = list(p["scores"][who][act])
    blk = p["saves"][who][act]
    vals[SAV_IDX] = derive_saves(blk["prof"], blk["boosters"],
                                 p.get("concentration", {}).get(who, False))
    return vals


def matrix(p, rec):
    head = "".join(f"<th><span>{a}</span></th>" for a in AXES)
    body = []
    for who in ("a", "b"):
        nm = p["names"][who]
        for act in ACTS:
            body.append(f'<tr class="ind {who}"><th>{nm if act == "I" else ""} {act}</th>'
                        + "".join(cell(x) for x in _own(p, who, act))
                        + '<td class="tot">—</td></tr>')
    for act in ACTS:
        r = rec["acts"][act]
        body.append(f'<tr class="pairrow"><th>Pair {act}</th>'
                    + "".join(cell(r["pair"][k], k) for k in KEYS)
                    + f'<td class="tot">{r["tempo"]*100:.0f}%</td></tr>')
    return (f'<div class="scroll"><table class="matrix"><thead><tr><th>Series</th>{head}'
            f'<th class="tot"><span>Tempo</span></th></tr></thead><tbody>'
            + "".join(body) + '</tbody></table></div>')


def dmg_table(p, rec):
    rows = []
    for act in ACTS:
        r = rec["acts"][act]
        wc, wb = MIX[act]
        f = lambda u, w: f'<td class="{"crit" if u < FLAG and w >= .40 else ""}">{u:.2f}</td>'
        # By id, not by slot: score_bodies orders a pairing damage-first, which need not match
        # this sheet's authored a/b.
        ua, ub = r["u"][p["names"]["a"]], r["u"][p["names"]["b"]]
        rows.append(f'<tr><th>{act}</th>' + f(ua[0], wc) + f(ua[1], wb)
                    + f(ub[0], wc) + f(ub[1], wb)
                    + f'<td class="mix">{r["tempo"]*100:.0f}%</td></tr>')
    return ('<div class="scroll"><table class="matrix dmg"><thead>'
            f'<tr><th rowspan="2">Act</th><th colspan="2">{p["names"]["a"]}</th>'
            f'<th colspan="2">{p["names"]["b"]}</th><th rowspan="2">Tempo</th></tr>'
            '<tr><th>crowd</th><th>prio</th><th>crowd</th><th>prio</th></tr></thead>'
            '<tbody>' + "".join(rows) + '</tbody></table></div>')


def chips(p, rec):
    out = []
    if rec["locked"]:
        out.append('<span class="chip warn">melee-locked</span>')
    for h in rec["holes"]:
        out.append(f'<span class="chip warn">{AXES[KEYS.index(h)].lower()} hole</span>')
    for who, kind in sorted(rec["flags"]):
        out.append(f'<span class="chip">{who} idles in {kind} fights</span>')
    if not out:
        out.append('<span class="chip ok">no hole, no idle body</span>')
    out.append(f'<span class="chip flat">reach {p["reach"]["a"]} · {p["reach"]["b"]}</span>')
    return "".join(out)


def render(d, sheetdir=None):
    pairs = d["pairings"]
    for slug, p in pairs.items():
        p.setdefault("slug", slug)
        if sheetdir and not p.get("scores"):
            p["scores"] = scrape(slug, sheetdir)
        for f in ("names", "reach", "scores", "url"):
            if f not in p:
                sys.exit(f"pairing {slug}: missing {f!r}")
        for who in ("a", "b"):
            if p["reach"][who] not in REACH:
                sys.exit(f"pairing {slug}: unknown reach {p['reach'][who]!r}")
            if who not in p.get("saves", {}):
                sys.exit(f"pairing {slug}: missing saves block for {who!r} — "
                         "saves is derived, not authored")
            for act in ACTS:
                row = p["scores"][who][act]
                if len(row) != len(KEYS):
                    sys.exit(f"pairing {slug} {who} {act}: scores has {len(row)} entries, "
                             f"expected {len(KEYS)} ({', '.join(KEYS)})")
                if row[SAV_IDX] is not None:
                    sys.exit(f"pairing {slug} {who} {act}: index {SAV_IDX} (saves) must be "
                             "null — it is derived from the saves block")
                if act not in p["saves"][who]:
                    sys.exit(f"pairing {slug} {who}: saves block missing act {act}")

    ranked = sorted(((score(p), p) for p in pairs.values()), key=lambda t: -t[0]["score"])

    cards = []
    for i, (rec, p) in enumerate(ranked, 1):
        splits = "".join(f'<span>{p["splits"][w]}</span>' for w in ("a", "b")
                         if p.get("splits", {}).get(w))
        cards.append(f'''<article class="card" id="{p["slug"]}">
  <header class="ehead">
    <div class="rank">{i:02d}</div>
    <div class="etitle">
      <h3>{p["names"]["a"]} &amp; {p["names"]["b"]}</h3>
      <p class="splits">{splits}</p>
    </div>
    <div class="score"><span class="num">{rec["score"]}</span><span class="lbl">score</span>
      <span class="sub">tempo {rec["tempo"]*100:.0f}% &middot; damage + control, capped by Actions</span>
      <span class="sub">resilience &middot; duration &middot; utility {rec["nontempo"]*100:.0f}%</span></div>
  </header>
  <div class="chips">{chips(p, rec)}</div>
  <p class="lede">{p.get("tagline","")}</p>
  <div class="cols">
    <div class="col"><h4>Profile — both halves, then the pair</h4>{matrix(p, rec)}
      {f'<p class="note">{p["shape"]}</p>' if p.get("shape") else ""}</div>
    <div class="col"><h4>Damage coverage</h4>{dmg_table(p, rec)}
      {f'<p class="note">{p["damage"]}</p>' if p.get("damage") else ""}</div>
  </div>
  <p class="out"><a href="{p["url"]}">Open the full sheet &rarr;</a></p>
</article>''')

    frows = "".join(
        f'<tr><th scope="row"><span class="ent">{i:02d}</span>'
        f'<a href="#{p["slug"]}">{p["names"]["a"]} + {p["names"]["b"]}</a></th>'
        + "".join(cell(rec["acts"]["III"]["pair"][k], k) for k in KEYS)
        + "".join(f'<td class="n{" sep" if n == 0 else ""}">{rec["acts"][a]["tempo"]*100:.0f}</td>' for n, a in enumerate(ACTS))
        + f'<td class="n dm sep">{rec["nontempo"]*100:.0f}</td>' 
          f'<td class="n b">{rec["score"]}</td></tr>' 
        for i, (rec, p) in enumerate(ranked, 1))

    facts = "".join(f"<li>{f}</li>" for f in d.get("facts", []))
    method = "".join(f'<div><b>{c["title"]}</b><p>{c["body"]}</p></div>'
                     for c in d.get("method", {}).get("cards", []))
    css = open(os.path.join(ASSETS, "finalists.css")).read()

    return f'''<title>{d.get("title","Finalists")}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>{css}</style>
<div class="wrap">
<header class="masthead">
  <p class="eyebrow">{d.get("eyebrow","")}</p>
  <h1>{d.get("title","Finalists")}</h1>
  <p class="standfirst">{d.get("lede","")}</p>
  <ul class="facts">{facts}</ul>
</header>

{f"""<section><h2>{d.get("method",{}).get("h2","How to read this")}</h2>
<div class="method">{method}</div></section>""" if method else ""}

<section>
  <h2>The field</h2>
  <p class="sublede">Act III axis values, then coverage per act. Sorted by score.</p>
  <div class="scroll"><table class="field matrix"><thead><tr><th>Pairing</th>
    {"".join(f"<th>{a}</th>" for a in AXES)}
    <th title="tempo %, act I">I</th><th title="tempo %, act II">II</th><th title="tempo %, act III">III</th><th title="resilience, duration, utility">Rest</th><th>Score</th></tr></thead>
    <tbody>{frows}</tbody></table></div>
</section>

<section>
  <h2>The pairings</h2>
  <p class="sublede">{d.get("cards_note","")}</p>
  {"".join(cards)}
</section>

<footer>{d.get("footer","")}</footer>
</div>
'''


def main():
    args = list(sys.argv[1:])
    out = sheetdir = None
    for flag, setter in (("-o", "out"), ("--scrape", "sheetdir")):
        if flag in args:
            i = args.index(flag)
            val = args[i + 1]
            del args[i:i + 2]
            if setter == "out": out = val
            else: sheetdir = val
    if len(args) != 1:
        sys.exit(__doc__)
    d = json.load(open(args[0]))
    doc = render(d, sheetdir)
    if sheetdir:                       # persist what was scraped
        json.dump(d, open(args[0], "w"), indent=1)
    if out:
        open(out, "w").write(doc)
        print(f"wrote {out} ({len(doc)} bytes)", file=sys.stderr)
    else:
        sys.stdout.write(doc)


if __name__ == "__main__":
    main()
