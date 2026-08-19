#!/usr/bin/env python3
"""Render a Listo pair sheet from a JSON data file.

    scripts/render_pair.py pair.json > out.html
    scripts/render_pair.py pair.json -o out.html

The CSS, the JS, the section scaffolding, the pair radar values and the whole
damage-coverage table are produced here — author only the JSON. See
assets/pair-schema.md for the shape.

Strings pass through as HTML: inline <b>/<em> are fine.
"""
import json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")

AXES = ["Single", "AoE", "Durab.", "Actions", "Control",
        "Sustain", "Skills", "Saves", "Endur."]
LABELS = ["Single-target", "AoE", "Durability", "Action economy", "Control",
          "Sustain", "Skills", "Saves", "Endurance"]
KINDS = ["additive", "additive", "additive", "additive", "additive",
         "threshold", "complementary", "personal", "personal"]
BANDS = ["1–10", "11–15", "16–20"]

# reach class -> (crowd multiplier, priority multiplier)
REACH = {"ranged": (1.00, 1.00), "hybrid": (0.95, 0.95),
         "mobile": (0.95, 1.00), "static": (0.85, 0.90)}
REACH_LABEL = {"ranged": "ranged", "hybrid": "hybrid",
               "mobile": "mobile melee", "static": "static melee"}
MIX = [(0.70, 0.30), (0.60, 0.40), (0.50, 0.50)]
DASH = "—"


def rows(x):
    """Accept [[k, v], ...] or ['plain', ...] for kit lists."""
    out = []
    for r in x or []:
        if isinstance(r, str):
            out.append("<li>%s</li>" % r)
        else:
            out.append("<li><b>%s</b> %s %s</li>" % (r[0], DASH, r[1]))
    return "\n".join(out)


def pane(name, sub, body):
    return ('<div class="pane-head"><span class="pane-name">%s</span>'
            '<span class="pane-sub">%s</span></div>'
            '<div class="pane-body">%s</div>' % (name, sub, body))


def abilities(ab):
    head = ('<thead><tr><th>Ability</th><th class="num">Buy</th>'
            '<th class="num">LW</th><th class="num">Feat</th>'
            '<th class="num">Other</th><th class="num final">Final</th>'
            '<th class="num">Mod</th></tr></thead>')
    body = []
    for r in ab:
        cells = ['<td class="ability">%s</td>' % r[0]]
        for i, v in enumerate(r[1:]):
            cls = "num mono final" if i == 4 else "num mono"
            cells.append('<td class="%s">%s</td>' % (cls, v))
        body.append("<tr>%s</tr>" % "".join(cells))
    return "<table>%s<tbody>%s</tbody></table>" % (head, "\n".join(body))


def roster_pane(c, who):
    parts = [abilities(c["abilities"]),
             "<h3>Saves</h3>", '<ul class="kit">%s</ul>' % rows(c.get("saves"))]
    race = c.get("race")
    if race:
        parts += ["<h3>Race %s %s</h3>" % (DASH, race["name"]),
                  '<ul class="kit">%s</ul>' % rows(race.get("traits"))]
    sk = c.get("skills")
    if sk:
        parts += ["<h3>Skill map %s background: %s</h3>" % (DASH, sk.get("background", DASH)),
                  '<ul class="kit">%s</ul>' % rows(sk.get("items"))]
    return '<div class="pane" data-who="%s">%s</div>' % (
        who, pane(c["name"], c.get("sub", DASH), "\n".join(parts)))


def profile(d, names):
    p = d.get("profile", {})
    sc = p["scores"]
    axes = p.get("axes", AXES)
    kinds = p.get("kinds", KINDS)
    labels = p.get("labels", LABELS)
    reads = p.get("reads") or [DASH] * len(axes)
    attrs = ['data-names="%s,%s"' % (names["a"], names["b"]),
             'data-axes="%s"' % ",".join(axes),
             'data-kinds="%s"' % ",".join(kinds),
             'data-bands="%s"' % ",".join(p.get("bands", BANDS))]
    for who in ("a", "b"):
        for act in (1, 2, 3):
            attrs.append('data-%s%d="%s"' % (
                who, act, ",".join(str(v) for v in sc[who][act - 1])))
    trs = []
    for i, label in enumerate(labels):
        cells = []
        for act in (1, 2, 3):
            cells.append('<td class="sc a%d"><span class="va">%s</span> '
                         '<span class="vb">%s</span> <b class="pv"></b></td>'
                         % (act, sc["a"][act - 1][i], sc["b"][act - 1][i]))
        trs.append('<tr><td>%s</td><td class="kind">%s</td>%s<td>%s</td></tr>'
                   % (label, kinds[i].capitalize(), "".join(cells), reads[i]))
    notes = "\n".join('<p class="r-note">%s</p>' % n for n in p.get("notes", []))
    return """  <section>
    <div class="eyebrow"><span>Profile</span><span>0&ndash;5 each &middot; pair value computed</span></div>
    <h2>%s</h2>
    <figure class="profile" style="margin:0" %s>
      <div class="radar">
        <div class="r-tabs" role="tablist" aria-label="Act">
          <button class="r-tab" type="button" role="tab" data-act="1">Act I</button>
          <button class="r-tab" type="button" role="tab" data-act="2">Act II</button>
          <button class="r-tab" type="button" role="tab" data-act="3">Act III</button>
        </div>
        <p class="r-band"></p>
        <p class="r-legend"></p>
      </div>
      <div>
        <div class="r-table"><table>
          <thead><tr><th>Axis</th><th>Kind</th>
            <th class="sc a1">I</th><th class="sc a2">II</th><th class="sc a3">III</th>
            <th>Reads as</th></tr></thead>
          <tbody>%s</tbody>
        </table></div>
        <p class="r-note">
          Each cell reads <span class="va">A</span> <span class="vb">B</span> <b class="pv">pair</b>.
          <strong>Additive</strong> axes sum (capped at 5). <strong>Threshold</strong> axes take the
          higher. <strong>Complementary</strong> axes take the higher plus half the lower.
          <strong>Personal</strong> axes take the <em>lower</em> &mdash; they cannot be delegated.
        </p>
%s
      </div>
    </figure>
  </section>""" % (p.get("h2", ""), "\n            ".join(attrs), "\n".join(trs), notes)


def damage(d, names):
    """Compute the whole coverage table from the radar scores and reach."""
    dm = d.get("damage", {})
    sc = d["profile"]["scores"]
    reach = dm.get("reach", {"a": "ranged", "b": "ranged"})
    lock = not any(reach[w] in ("ranged", "hybrid") for w in ("a", "b"))
    trs = []
    for act in (1, 2, 3):
        wc, wp = MIX[act - 1]
        u = {}
        for who in ("a", "b"):
            st, aoe = sc[who][act - 1][0], sc[who][act - 1][1]
            rc, rp = REACH[reach[who]]
            crowd = (aoe + 0.5 * st * rc) * (0.9 if lock else 1.0)
            u[who] = (crowd, st * rp + 0.25 * aoe)
        pc = u["a"][0] + u["b"][0]
        pp = u["a"][1] + u["b"][1]
        cells = []
        for who in ("a", "b"):
            for k, w in ((0, wc), (1, wp)):
                idle = " u-idle" if u[who][k] < 3.0 and w >= 0.40 else ""
                cells.append('<td class="u%s"><b>%.1f</b></td>' % (idle, u[who][k]))
        trs.append('<tr><td class="act">%s</td><td class="mix">%d / %d</td>%s'
                   '<td class="u"><b>%.1f</b></td><td class="u"><b>%.1f</b></td>'
                   '<td class="w">%.1f</td></tr>'
                   % (["I", "II", "III"][act - 1], wc * 100, wp * 100,
                      "".join(cells), pc, pp, wc * pc + wp * pp))
    notes = ['<p class="r-note">Reach &mdash; %s <span class="reach">%s</span>, '
             '%s <span class="reach">%s</span>. The discount lands on the single-target term only. '
             '<span class="reach">ranged</span> 1.00 &middot; <span class="reach">hybrid</span> 0.95 '
             '&middot; <span class="reach">mobile</span> 0.95 crowd, 1.00 priority &middot; '
             '<span class="reach">static</span> 0.85 crowd, 0.90 priority.</p>'
             % (names["a"], REACH_LABEL[reach["a"]], names["b"], REACH_LABEL[reach["b"]])]
    if lock:
        notes.append('<p class="note"><b>Melee lock.</b> Neither body answers at range, so every '
                     'crowd figure above carries a further &times;0.9. Anything that kites, flies or '
                     'holds a ledge is fought entirely on its terms.</p>')
    notes += ['<p class="note">%s</p>' % n for n in dm.get("notes", [])]
    return """  <section>
    <div class="eyebrow"><span>Damage coverage</span><span>What the pair delivers, not what the axes cap at</span></div>
    <h2>%s</h2>
    <div class="dmg"><table>
      <thead><tr><th>Act</th><th>Fight mix</th>
        <th style="text-align:right">%s crowd</th><th style="text-align:right">%s priority</th>
        <th style="text-align:right">%s crowd</th><th style="text-align:right">%s priority</th>
        <th style="text-align:right">Pair crowd</th><th style="text-align:right">Pair priority</th>
        <th style="text-align:right">Weighted</th></tr></thead>
      <tbody>%s</tbody>
    </table></div>
%s
  </section>""" % (dm.get("h2", ""), names["a"], names["a"], names["b"], names["b"],
                   "\n".join(trs), "\n".join(notes))


def who_chip(w, names):
    label = {"either": "either", "both": "Both", "none": "nobody"}.get(w) or names[w]
    return '<span class="who" data-who="%s">%s</span>' % (
        "either" if w in ("either", "both", "none") else w, label)


def gates(d, names):
    g = d.get("gates", {})
    trs = []
    for r in g.get("rows", []):
        owner = r.get("owner", "none")
        grade = r.get("grade") or ("bad" if owner == "none" else "ok")
        cls = ' class="fail"' if owner == "none" else ""
        trs.append('<tr%s><td class="gate">%s</td><td>%s</td><td>%s</td><td>%s</td>'
                   '<td>%s</td><td class="mod g-%s"><b>%s</b><span class="pc">%s</span></td>'
                   '<td>%s</td></tr>'
                   % (cls, r["gate"], r["skill"], r.get("act", DASH), r.get("dc", DASH),
                      who_chip(owner, names), grade, r["mod"], r.get("pc", ""),
                      r.get("source", DASH)))
    return """  <section>
    <div class="eyebrow"><span>Gate audit</span><span>Five gates &middot; two Inspiration rerolls assumed</span></div>
    <h2>%s</h2>
    <div class="gt"><table>
      <thead><tr><th>Gate</th><th>Skill</th><th>Act</th><th>DC</th><th>Rolled by</th><th>Modifier</th><th>Source</th></tr></thead>
      <tbody>%s</tbody>
    </table></div>
%s
  </section>""" % (g.get("h2", ""), "\n".join(trs),
                   '<p class="r-note">%s</p>' % g["note"] if g.get("note") else "")


def play(d, names):
    p = d.get("play", {})
    cards = [('<div class="card" data-who="a"><span class="lvl">%s %s the turn</span><p>%s</p></div>'
              % (names["a"], DASH, p.get("a", DASH))),
             ('<div class="card" data-who="b"><span class="lvl">%s %s the turn</span><p>%s</p></div>'
              % (names["b"], DASH, p.get("b", DASH))),
             ('<div class="card" data-who="pair"><span class="lvl">Together</span><p>%s</p></div>'
              % p.get("pair", DASH))]
    stack = ['<div class="ck"><span class="ck-head">%s</span><p>%s</p></div>' % (c[0], c[1])
             for c in p.get("combos", [])]
    if p.get("failure"):
        stack.append('<p class="note"><b>Failure mode:</b> %s</p>' % p["failure"])
    return """  <section>
    <div class="eyebrow"><span>How it plays</span><span>Two loops, then the shared one</span></div>
    <h2>%s</h2>
    <div class="prose"><p>%s</p></div>
    <div class="cards">%s</div>
    <div class="stack">%s</div>
  </section>""" % (p.get("h2", ""), p.get("intro", ""), "\n".join(cards), "\n".join(stack))


def progression(d, names):
    p = d.get("prog", {})
    trs = []
    for r in p.get("rows", []):
        flag = r.get("flag")
        a, b = r.get("a", [DASH] * 3), r.get("b", [DASH] * 3)
        trs.append('<tr%s><td class="num mono">%s</td>'
                   '<td class="mono">%s</td><td>%s</td><td class="mono">%s</td>'
                   '<td class="mono split">%s</td><td>%s</td><td class="mono">%s</td></tr>'
                   % (' class="%s"' % flag if flag else "", r["lvl"],
                      a[0], a[1], a[2], b[0], b[1], b[2]))
    ck = p.get("checkpoint")
    ckhtml = ('<div class="ck"><span class="ck-head">%s</span><p>%s</p></div>'
              % (ck.get("head", "Respec checkpoint"), ck["text"])) if ck else ""
    return """  <section>
    <div class="eyebrow"><span>Progression</span><span>Shared XP &middot; character levels 1&ndash;20</span></div>
    <h2>%s</h2>
    <div class="scroller"><table>
      <thead>
        <tr><th class="num" rowspan="2">Lvl</th>
          <th class="grp-a" colspan="3">%s</th>
          <th class="grp-b split" colspan="3">%s</th></tr>
        <tr><th>Take</th><th>Pick</th><th>Feat</th>
          <th class="split">Take</th><th>Pick</th><th>Feat</th></tr>
      </thead>
      <tbody>%s</tbody>
    </table></div>
    %s
  </section>""" % (p.get("h2", ""), names["a"], names["b"], "\n".join(trs), ckhtml)


def kit_table(items):
    trs = ['<tr><td>%s</td><td%s>%s</td><td class="num mono">%s</td></tr>'
           % (r[0], ' class="win"' if len(r) > 3 and r[3] else "", r[1], r[2])
           for r in items]
    return ('<table><thead><tr><th>Slot</th><th>Target</th><th class="num">Act</th></tr></thead>'
            '<tbody>%s</tbody></table>' % "\n".join(trs))


def equipment(d, names):
    g = d.get("gear", {})
    panes = "".join(
        '<div class="pane" data-who="%s">%s</div>'
        % (w, pane(names[w], "Target kit by act", kit_table(g.get(w, []))))
        for w in ("a", "b"))
    trs = []
    for r in g.get("contested", []):
        trs.append('<tr><td class="num mono">%s</td><td class="mono%s">%s</td><td>%s</td>'
                   '<td>%s</td><td>%s</td></tr>'
                   % (r.get("act", DASH), " win" if r.get("win") else "", r["item"],
                      who_chip(r["to"], names), r.get("why", DASH), r.get("gives_up", DASH)))
    note = '<p class="note">%s</p>' % g["note"] if g.get("note") else ""
    return """  <section>
    <div class="eyebrow"><span>Equipment</span><span>4&times; buy &middot; &frac14; sell &middot; 5 attuned each</span></div>
    <h2>%s</h2>
    <div class="duo">%s</div>
    <div class="phase">Contested &mdash; one owner each</div>
    <div class="scroller"><table>
      <thead><tr><th class="num">Act</th><th>Item</th><th>Goes to</th><th>Why</th><th>What the other gives up</th></tr></thead>
      <tbody>%s</tbody>
    </table></div>
    %s
  </section>""" % (g.get("h2", ""), panes, "\n".join(trs), note)


def quests(d, names):
    q = d.get("quests", {})
    trs = ['<tr><td class="num mono">%s</td><td class="mono%s">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
           % (r.get("act", DASH), " win" if r.get("win") else "", r["reward"],
              r.get("source", DASH), r.get("gate", DASH), who_chip(r.get("to", "either"), names))
           for r in q.get("rows", [])]
    return """  <section>
    <div class="eyebrow"><span>Quest rewards</span><span>What gates each one</span></div>
    <h2>%s</h2>
    <div class="scroller"><table>
      <thead><tr><th class="num">Act</th><th>Reward</th><th>Source</th><th>Gate</th><th>Goes to</th></tr></thead>
      <tbody>%s</tbody>
    </table></div>
  </section>""" % (q.get("h2", ""), "\n".join(trs))


def render(d):
    names = {"a": d["roster"]["a"]["name"], "b": d["roster"]["b"]["name"]}
    css = open(os.path.join(ASSETS, "pair.css")).read()
    js = open(os.path.join(ASSETS, "pair.js")).read()
    r = d["roster"]
    head = """<div class="sheet"%s>

  <header class="titleblock">
    <div class="titleblock-main">
      <h1 class="wordmark">%s <span class="amp">&amp;</span> <span class="dim">%s</span></h1>
      <p class="tagline">%s</p>
    </div>
    <div class="fields">
      <div class="field"><span class="field-key">Party</span><span class="field-val">2 &middot; Lone Wolf</span></div>
      <div class="field"><span class="field-key">%s &mdash; Split</span><span class="field-val">%s</span></div>
      <div class="field"><span class="field-key">%s &mdash; Split</span><span class="field-val">%s</span></div>
      <div class="field"><span class="field-key">Ruleset</span><span class="field-val">%s</span></div>
    </div>
  </header>

  <section>
    <div class="eyebrow"><span>Roster</span><span>27-point buy &middot; Lone Wolf +4 &times;2</span></div>
    <h2>%s</h2>
    <div class="duo">%s%s</div>
    %s
  </section>""" % (
        ' data-class="%s"' % d["class"] if d.get("class") else "",
        names["a"], names["b"], d.get("tagline", ""),
        names["a"], d.get("splits", {}).get("a", DASH),
        names["b"], d.get("splits", {}).get("b", DASH),
        d.get("ruleset", "Listo v10.2"),
        r.get("h2", ""), roster_pane(r["a"], "a"), roster_pane(r["b"], "b"),
        '<p class="note">%s</p>' % r["note"] if r.get("note") else "")

    body = "\n\n".join([head, profile(d, names), damage(d, names), gates(d, names),
                        play(d, names), progression(d, names), equipment(d, names),
                        quests(d, names)])
    return """<title>%s</title>
<style>
%s</style>

%s

  <footer>
    <span>Listonomicon v10.2 &middot; Combat Extender</span>
    <span>Party of 2 &middot; Lone Wolf &middot; shared XP</span>
  </footer>

</div>

<script>
%s</script>
""" % (d.get("title", "%s & %s" % (names["a"], names["b"])), css, body, js)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    out = None
    if "-o" in args:
        i = args.index("-o")
        out = args[i + 1]
        del args[i:i + 2]
    data = json.load(open(args[0]))
    html = render(data)
    if out:
        open(out, "w").write(html)
        sys.stderr.write("%s  %d bytes\n" % (out, len(html)))
    else:
        sys.stdout.write(html)
