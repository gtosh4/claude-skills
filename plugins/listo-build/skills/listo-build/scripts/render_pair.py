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

sys.path.insert(0, HERE)

# One implementation of the scoring model: scripts/scoring.py, which implements
# references/scoring-model.md. Never restate its constants here.
import scoring as S                                          # noqa: E402
from scoring import ScoringError, derive_saves, SAV_IDX      # noqa: E402

AXES = list(S.AXES)
LABELS = list(S.LABELS)
# `derived` axes are not combined on the rung — scoring.py builds them from the evidence.
# On a pair sheet they still need a display operator: saves is the weakest link, skills the
# better half.
_KIND = {"add": "additive", "comp": "complementary", "per": "personal"}
_DERIVED = {"sav": "personal", "skl": "shared"}
KINDS = [_DERIVED[k] if S.KINDS[k] == "derived" else _KIND[S.KINDS[k]] for k in S.KEYS]
BANDS = list(S.BANDS)
REACH = dict(S.REACH)
REACH_LABEL = {"ranged": "ranged", "hybrid": "hybrid",
               "mobile": "mobile melee", "static": "static melee"}
MIX = [S.MIX[a] for a in S.ACTS]
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


# Ability, buy, Lone Wolf, feats, other — then Final and Mod. An eighth entry inserts a
# `Mirror` column before Final, for the one Act III reward that permanently moves a stat and
# raises its cap to 24. It is display only: `axis-rubrics.md` rule 1 keeps every named reward
# out of the scored rows, and the `derived` block reads the pre-Mirror figures.
_ABILITY_COLS = ["Buy", "LW", "Feat", "Other"]


def abilities(ab):
    extra = ["Mirror"] if ab and len(ab[0]) == len(_ABILITY_COLS) + 4 else []
    cols = _ABILITY_COLS + extra + ["Final", "Mod"]
    head = "<thead><tr><th>Ability</th>%s</tr></thead>" % "".join(
        '<th class="num%s">%s</th>' % (" final" if c == "Final" else "", c) for c in cols)
    body = []
    for r in ab:
        # Final is always the second-to-last entry, whether or not a Mirror column is present.
        final_at = len(r) - 3
        cells = ['<td class="ability">%s</td>' % r[0]]
        for i, v in enumerate(r[1:]):
            cls = "num mono final" if i == final_at else "num mono"
            if extra and i == final_at - 1:
                cls += " mirror"
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


def _slots(acts):
    """The action budget as it was authored. Every slot is an attack, a cast or filler."""
    bits = [("%g attack" % acts.get("attacks", 0), acts.get("attacks", 0)),
            ("%g cast" % acts.get("spells", 0), acts.get("spells", 0)),
            ("%g filler" % acts.get("filler", 0), acts.get("filler", 0))]
    return " &middot; ".join(b for b, n in bits if n)


def _dmg_working(t, block, axis):
    """raw + gear = scored, over par — and what the raw was made of."""
    if not t["inst"]:
        return '<span class="faint">no delivery on this axis</span>'
    riders = [r["name"] for r in block.get("riders", []) if r.get(axis, 0)]
    made = (' <span class="faint">incl. %s</span>' % ", ".join(riders)) if riders else ""
    mult = (' &times; <b>%g</b> <span class="faint">%s</span>'
            % (t["mult"], t["why"])) if t["mult"] != 1.0 else ""
    return ('raw <b>%.1f</b> + gear <b>%.1f</b> <span class="faint">(%g inst &times; k%g)</span>%s '
            '= <b>%.1f</b> &divide; par %g%s'
            % (t["raw"], t["gear"], t["inst"], t["k"], mult, t["scored"], t["par"], made))


def _ehp_working(e):
    layers = ["&times;%.2f %s" % (1 / v, w) for w, v in e["prop"]]
    layers += ["&minus;%g %s" % (v, w) for w, v in e["flat"]]
    mit = (" &middot; " + ", ".join(layers)) if layers else ""
    crowd, boss = e["fights"]
    if abs(crowd["ratio"] - boss["ratio"]) < 5e-3:
        # Nothing here splits the two fight shapes, and saying so is more use than printing the
        # same number twice: the blend only does work when a flat layer is in play.
        fights = ('crowd = boss <span class="faint">&mdash; no mitigation layer to split '
                  'them</span>')
    else:
        fights = " &middot; ".join(
            '%s <b>%.2f</b> <span class="faint">&times;%g</span>%s'
            % (f["fight"], f["ratio"], f["weight"],
               ' <span class="cap">capped</span>' if f["capped"] else "")
            for f in (crowd, boss))
    return ('pool <b>%.2f</b> <span class="faint">(%g &divide; %g)</span> &middot; AC %g '
            '&rarr; p_hit %.2f <b>&times;%.2f</b>%s<br>%s'
            % (e["pool_ratio"], e["pool"], e["par_pool"], e["ac"], e["p_hit"], e["acc"],
               mit, fights))


def _derived_notes():
    """Why the three rungs above are arithmetic, in the terms the constants are actually in."""
    return (
        '<p class="r-note"><b>Three of the ten axes are computed, not judged.</b> '
        '<b>Single-target</b> and <b>AoE</b> are damage per round over that act&rsquo;s par '
        '&mdash; %s and %s &mdash; par being a reference body with Extra Attack and a mundane '
        'weapon, against two Fireball-equivalents a fight on four targets. <b>Effective HP</b> '
        'is this body&rsquo;s pool, AC and mitigation over par&rsquo;s medium armour and shield '
        'at AC %d. Every ratio and rung above is derived from the inputs by '
        '<code>scoring.py</code>; a ratio that disagreed with the rung in the profile table '
        'would refuse to render.</p>'
        '<p class="r-note"><b>The gear constant <code>k</code> is per damage instance</b> '
        '&mdash; %s by act &mdash; and it lands on par&rsquo;s four instances too, so a body '
        'that delivers like par is unmoved by it. Four attacks collect it four times and one big '
        'spell collects it once, which is why instance count is stated rather than inferred. No '
        'named item ever enters: a rented capability is not a chassis property.</p>'
        '<p class="r-note"><b>Durability is blended over two fight shapes</b>, because flat '
        'reduction is worth several times more against a crowd than against a boss. The crowd '
        'and boss ratios carry that act&rsquo;s weights &mdash; %s &mdash; and the flat term is '
        'capped at &times;%g: against Act I&rsquo;s crowd hit of %g an uncapped aura reads as '
        'four times par, which is a fact about small numbers rather than about the body. '
        '<b>Self-healing counts here</b>, not as Rescue &mdash; only what a body can aim at its '
        '<em>partner</em> is Rescue, and nothing is ever scored in both.</p>'
        % (" / ".join("%g" % S.PAR["st"][a] for a in S.ACTS),
           " / ".join("%g" % S.PAR["aoe"][a] for a in S.ACTS),
           S.PAR_AC,
           " / ".join("+%g" % S.GEAR[a] for a in S.ACTS),
           " &middot; ".join("%d/%d" % (c * 100, b * 100) for c, b in (S.MIX[a] for a in S.ACTS)),
           S.MIT_CAP, S.TYPICAL_HIT["I"][0]))


def derived(d, names):
    """The three computed axes, worked.

    Nothing here is authored except the inputs — the action split, the raws and their instance
    counts, the pool, the AC and the mitigation layers. Every ratio and every rung comes out of
    `scoring.py`, and a rung disagreeing with the one the profile table claims is a hard failure:
    two numbers for the same axis is exactly the drift this block exists to end.
    """
    dv = d.get("derived")
    if not dv:
        return ""
    scores = d["profile"]["scores"]
    idx = {"st": S.ST_IDX, "aoe": S.AOE_IDX, "dur": S.DUR_IDX}
    splits = d.get("splits", {})
    panes = []
    for who in ("a", "b"):
        body = dv.get(who)
        if not body:
            sys.exit("derived: no block for %s — author both bodies or omit the section" % who)
        trs = []
        for i, act in enumerate(S.ACTS):
            blk = body.get(act)
            if not blk:
                sys.exit("derived %s: act %s is missing" % (names[who], act))
            for f in ("damage", "dur"):
                if f not in blk:
                    sys.exit("derived %s act %s: missing %r" % (names[who], act, f))
            try:
                t = S.damage_terms(blk["damage"], act, names[who])
                e = S.derive_ehp(blk["dur"], act, names[who])
            except ScoringError as err:
                sys.exit("derived: %s" % err)

            for ax, rung in (("st", t["st"]["rung"]), ("aoe", t["aoe"]["rung"]),
                             ("dur", e["rung"])):
                claimed = scores[who][i][idx[ax]]
                if rung != claimed:
                    sys.exit("derived %s act %s: the working gives %s rung %d, the profile "
                             "table claims %d. One of the two is wrong — fix the inputs or fix "
                             "the score, but the sheet may not carry both."
                             % (names[who], act, ax, rung, claimed))

            rows = [("Single-target", _dmg_working(t["st"], blk["damage"], "st"),
                     t["st"]["ratio"], t["st"]["rung"]),
                    ("AoE", _dmg_working(t["aoe"], blk["damage"], "aoe"),
                     t["aoe"]["ratio"], t["aoe"]["rung"]),
                    ("Effective HP", _ehp_working(e), e["ratio"], e["rung"])]
            for j, (label, work, ratio, rung) in enumerate(rows):
                head = ('<td class="act" rowspan="%d">Act %s<span class="budget">%s</span></td>'
                        % (len(rows), act, _slots(blk["damage"].get("actions") or {}))) if not j else ""
                trs.append('<tr>%s<td class="metric">%s</td><td class="work">%s</td>'
                           '<td class="u"><b>%.2f</b>&times;</td><td class="w">%d</td></tr>'
                           % (head, label, work, ratio, rung))
        note = ('<p class="r-note">%s</p>' % body["note"]) if body.get("note") else ""
        panes.append('<div class="wk" data-who="%s"><div class="pane-head">'
                     '<span class="pane-name">%s</span><span class="pane-sub">%s</span></div>'
                     '<div class="scroller"><table><thead><tr><th>Act</th><th>Metric</th>'
                     '<th>Working</th><th class="u">Ratio</th><th class="w">Rung</th></tr>'
                     '</thead><tbody>%s</tbody></table></div>%s</div>'
                     % (who, names[who], splits.get(who, DASH), "\n".join(trs), note))

    notes = "".join('<p class="r-note">%s</p>' % n for n in dv.get("notes", []))
    return ('<h3>%s</h3>%s<div class="r-notes">%s%s</div>'
            % (dv.get("h3", "Where the damage and durability rungs come from"),
               "".join(panes), _derived_notes(), notes))

def profile(d, names):
    p = d.get("profile", {})
    sc = p["scores"]
    axes = p.get("axes", AXES)
    kinds = p.get("kinds", KINDS)
    labels = p.get("labels", LABELS)
    reads = p.get("reads") or [DASH] * len(axes)
    for nm, seq in (("axes", axes), ("kinds", kinds), ("labels", labels), ("reads", reads)):
        if len(seq) != len(S.KEYS):
            sys.exit("profile: %s has %d entries, expected %d (%s)"
                     % (nm, len(seq), len(S.KEYS), ", ".join(S.KEYS)))
    # Radar collapse, scoring-model.md §10: control-single/control-area blend by the act's
    # fight mix, and damage does the same. Ten rows stay in the table; the chart draws eight.
    # `"collapse": false` in the JSON turns it off; a string overrides the groups.
    collapse = p.get("collapse", "%d+%d:Damage,%d+%d:Control"
                     % (S.AOE_IDX, S.ST_IDX, S.KEYS.index("ctrl_a"), S.KEYS.index("ctrl_s")))
    attrs = ['data-names="%s,%s"' % (names["a"], names["b"]),
             'data-axes="%s"' % ",".join(axes),
             'data-kinds="%s"' % ",".join(kinds),
             'data-bands="%s"' % ",".join(p.get("bands", BANDS)),
             'data-need="%s"' % ",".join(str(S.NEED[k]) for k in S.KEYS)]
    if collapse:
        attrs.append('data-collapse="%s"' % collapse)
    saves = p.get("saves")
    if saves is None:
        sys.exit("profile: missing `saves` block — saves is derived, not authored")
    conc = p.get("concentration", {})
    # The authored saves cell is null; the table reads these resolved rows, not `sc`.
    resolved = {"a": [], "b": []}
    for who in ("a", "b"):
        for act in (1, 2, 3):
            row = list(sc[who][act - 1])
            if len(row) != len(S.KEYS):
                sys.exit("profile %s act %d: %d axis values, expected %d (%s)"
                         % (who, act, len(row), len(S.KEYS), ", ".join(S.KEYS)))
            if row[SAV_IDX] is not None:
                sys.exit("profile %s act %d: index %d (saves) must be null — it is "
                         "derived from the `saves` block" % (who, act, SAV_IDX))
            blk = saves[who][S.ACTS[act - 1]]
            row[SAV_IDX] = derive_saves(blk["prof"], blk["boosters"],
                                        conc.get(who, False))
            resolved[who].append(row)
            attrs.append('data-%s%d="%s"' % (
                who, act, ",".join(str(v) for v in row)))
    trs = []
    for i, label in enumerate(labels):
        cells = []
        for act in (1, 2, 3):
            cells.append('<td class="sc a%d"><span class="va">%s</span> '
                         '<span class="vb">%s</span> <b class="pv"></b></td>'
                         % (act, resolved["a"][act - 1][i], resolved["b"][act - 1][i]))
        trs.append('<tr><td>%s</td><td class="kind">%s</td>%s<td>%s</td></tr>'
                   % (label, kinds[i].capitalize(), "".join(cells), reads[i]))
    notes = "\n".join('<p class="r-note">%s</p>' % n for n in p.get("notes", []))
    return """  <section>
    <div class="eyebrow"><span>Profile</span><span>0&ndash;5 each &middot; pair value computed</span></div>
    <h2>%s</h2>
    <figure class="profile" style="margin:0" %s>
      <div class="p-chart">
      <div class="radar">
        <div class="r-tabs" role="tablist" aria-label="Act">
          <button class="r-tab" type="button" role="tab" data-act="1">Act I</button>
          <button class="r-tab" type="button" role="tab" data-act="2">Act II</button>
          <button class="r-tab" type="button" role="tab" data-act="3">Act III</button>
        </div>
        <p class="r-band"></p>
        <p class="r-legend"></p>
      </div>
      <p class="r-key">
        Each cell reads <span class="va">A</span> <span class="vb">B</span> <b class="pv">pair</b>.
        <strong>Additive</strong> axes sum, uncapped. <strong>Complementary</strong> axes take the
        higher plus half the lower &mdash; one source is enough, a second is discounted.
        <strong>Personal</strong> axes take the <em>lower</em>; they cannot be delegated.
        <strong>Shared</strong> axes take the <em>higher</em> &mdash; only one body rolls the check.
<b>The outer ring is the party these encounters are tuned for.</b>
        <code>axis-rubrics.md</code> §1 fixes the unit: par is one <em>reference body</em> and rung 2
        is par. Throughput scales with the party's <em>actions</em>, not its headcount &mdash; a
        five-seat party has one Action each and none of a planned duo's optimisation pressure, so it
        is priced at <b>four actions of ordinary play</b>, or <b>8</b> rung-units of Single-target or
        AoE. Coverage does not scale at all: that party fields one healer and a backup, so parity is
        <b>5</b> on a complementary axis, <b>4</b> on a personal one (nobody can lend you a Wisdom
        save) and <b>4</b> on Skills. All three series
        plot against that parity line, so the pair polygon is the pair's <em>share of a five-stack</em>
        and anything past the outer ring is surplus. The chart folds
        <strong>Single-target with AoE</strong> and <strong>Control (single) with Control (area)</strong>,
        each blended by that act&rsquo;s crowd/priority mix &mdash; eight spokes drawn, all ten rows kept.
      </p>
      </div>
      <div class="p-main">
        <div class="r-table"><table>
          <thead><tr><th>Axis</th><th>Kind</th>
            <th class="sc a1">I</th><th class="sc a2">II</th><th class="sc a3">III</th>
            <th>Reads as</th></tr></thead>
          <tbody>%s</tbody>
        </table></div>
      </div>
      <div class="r-notes">%s</div>
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
                # scoring.py owns FLAG; it moved 3.0 -> 1.25 and this copy did not follow.
                idle = " u-idle" if u[who][k] < S.FLAG and w >= 0.40 else ""
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
    combos = ['<div class="ck"><span class="ck-head">%s</span><p>%s</p></div>' % (c[0], c[1])
              for c in p.get("combos", [])]
    # Combos share the row rather than each taking a full-width box with a 66ch line in it.
    stack = ['<div class="combos">%s</div>' % "\n".join(combos)] if combos else []
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


_EATEN = ("<b>Eaten by %s.</b> That consumes the item, so <b>%s</b> never becomes half-illithid, "
          "and no inner-ring power is available to it at any point in the run.")

ASTRAL = {
    "commune": "<b>Communed with, not eaten.</b> Eating the Astral-Touched Tadpole consumes it for "
               "one character; communing leaves it usable by the other, so <b>both bodies become "
               "half-illithid off the one tadpole</b> and both inner rings open. Eating it in a duo "
               "is a planning error. <em>(unverified — vanilla behaviour, bg3.wiki.)</em>",
    # %s twice: the name of the body that ate it, then the name of the one that did not.
    "a": _EATEN, "b": _EATEN,
    "none": "<b>Refused.</b> Neither body becomes half-illithid, so the inner ring never opens and "
            "IMR is capped at 3 for the whole run. <code>Stomp that Tadpole</code> is what keeps "
            "the refusal available at the Emperor reveal.",
}


def illithid(d, names):
    """The tadpole allotment. IMR, the charge pool, the tax and the supply check are computed —
    author the picks and who gets the astral tadpole."""
    il = d.get("illithid")
    if not il:
        return None
    astral = il.get("astral", "none")
    if astral not in ASTRAL:
        sys.exit("illithid: astral must be one of %s" % ", ".join(ASTRAL))
    half = {"a": astral in ("commune", "a"), "b": astral in ("commune", "b")}
    picks = il.get("picks", {})
    try:
        plan = {w: S.illithid_plan(picks.get(w, {}), half[w]) for w in ("a", "b")}
    except ScoringError as e:
        sys.exit("illithid %s" % e)

    panes = []
    for w in ("a", "b"):
        appetite = S.illithid_appetite(plan[w])
        blocks = []
        for i, act in enumerate(S.ACTS):
            added = picks.get(w, {}).get(act, [])
            if not added:
                continue
            lis = []
            if not i or not plan[w][i - 1]["powers"]:
                lis.append('<li><b>Illithid Persuasion</b> %s <span class="tag">first tadpole</span> '
                           'carries the %s-charge pool and the Illithid Mind tax. Not a power for '
                           'IMR.</li>' % (DASH, S.POOL_BASE))
            for key in added:
                p = S.POWERS[key]
                lis.append('<li><b>%s</b> %s <span class="tag">%s</span> <span class="ring">ring %d</span> '
                           '<span class="cost">%s</span></li>'
                           % (p.name, DASH, S.AXES[S.KEYS.index(p.axis)], p.ring, p.cost))
            blocks.append("<h3>Act %s %s IMR %d, %.1f charges</h3><ul class=\"kit\">%s</ul>"
                          % (act, DASH, plan[w][i]["imr"], plan[w][i]["pool"], "\n".join(lis)))
        if not blocks:
            blocks = ['<ul class="kit"><li><b>No tadpoles.</b> This body spends none of the pool, '
                      'carries no Illithid Mind tax, and scores nothing illithid on any axis.</li></ul>']
        panes.append('<div class="pane" data-who="%s">%s</div>'
                     % (w, pane(names[w], "appetite: <b>%s</b>" % appetite, "\n".join(blocks))))

    trs, cum = [], 0
    for i, act in enumerate(S.ACTS):
        cum += S.SUPPLY[act]
        spent = plan["a"][i]["tadpoles"] + plan["b"][i]["tadpoles"]
        spare = cum - spent
        if spare < 0:
            sys.exit("illithid: act %s spends %d tadpoles against a supply of about %d — "
                     "the run does not hold that many" % (act, spent, cum))
        cells = []
        for w in ("a", "b"):
            r = plan[w][i]
            cells.append('<td class="num mono%s">%d</td><td class="num mono imr">%d</td>'
                         '<td class="num mono">%.1f</td><td class="num mono tax">%s</td>'
                         % (" split" if w == "b" else "", r["powers"], r["imr"], r["pool"],
                            ("+%d" % r["tax"]) if r["tax"] else DASH))
        trs.append('<tr><td class="act">%s</td>%s<td class="num mono split">%d</td>'
                   '<td class="num mono">%d</td><td class="num mono spare">%d</td></tr>'
                   % (act, "".join(cells), spent, cum, spare))

    notes = ['<p class="r-note">Every figure above is computed from the picks. '
             '<b>IMR</b> = &lfloor;powers &divide; 5&rfloor;, capped at 5, and it is what the '
             'powers’ numbers scale off &mdash; not character level. <b>Charges</b> = '
             '%s + %s &times; powers per long rest, <b>half back on a short rest</b>, against '
             'costs of 1&ndash;5 a cast. <b>Tax</b> is <code>+IMR</code> flat physical damage on '
             'every incoming hit, unconditional. Illithid Persuasion is the first tadpole and does '
             'not count toward IMR. <b>Supply</b> is the party total by that act &mdash; '
             '%s &middot; %s &middot; %s, cumulative &mdash; and it is '
             '<em>approximate</em>: vanilla tadpole placement is not pak-confirmed, and several '
             'Act I/II tadpoles sit behind mutually exclusive choices.</p>'
             % (S.POOL_BASE, S.POOL_PER_POWER,
                *("%s&nbsp;%d" % (a, S.SUPPLY[a]) for a in S.ACTS)),
             '<p class="note"><b>Astral-Touched Tadpole.</b> %s</p>'
             % (ASTRAL[astral] % (names[astral], names["b" if astral == "a" else "a"])
                if astral in ("a", "b") else ASTRAL[astral])]
    if any(plan[w][-1]["powers"] for w in ("a", "b")):
        notes.append('<p class="note"><b>Keep Volo alive.</b> <code>Topple the Weave</code> is '
                     'enabled, and its Unstable Weave surge arms itself only once Volo is dead. '
                     'After that roughly one spell cast in five surges and 4 of the 121 outcomes '
                     'call <code>RemoveAllTadpolePowers</code> &mdash; about <b>0.7% per cast</b>, '
                     'compounding. This plan is deleted by it. Whether the tadpoles are refunded is '
                     '<em>(unverified)</em>.</p>')
        notes.append('<p class="note"><b>The dip order sets the illithid save DC.</b> Power DCs '
                     'use the spellcasting modifier of the <em>last class added</em>, so a level-1 '
                     'dip taken late silently rewrites every save-based power on that body. Check '
                     'it against the respec ladder before spending on anything that asks for a '
                     'save. <em>(unverified — vanilla rule; IPO2 does not appear to change it.)</em></p>')
    notes += ['<p class="note">%s</p>' % n for n in il.get("notes", [])]

    intro = '<div class="prose"><p>%s</p></div>' % il["intro"] if il.get("intro") else ""
    return """  <section>
    <div class="eyebrow"><span>Illithid plan</span><span>One shared pool &middot; IPO2 + Half Potency</span></div>
    <h2>%s</h2>
    %s
    <div class="duo">%s</div>
    <div class="phase">Allotment &mdash; what each act's holding costs and buys</div>
    <div class="ill scroller"><table>
      <thead>
        <tr><th rowspan="2">Act</th>
          <th class="grp-a" colspan="4">%s</th>
          <th class="grp-b split" colspan="4">%s</th>
          <th colspan="3">Shared pool</th></tr>
        <tr><th class="num">Powers</th><th class="num">IMR</th><th class="num">Charges</th><th class="num">Tax</th>
          <th class="num split">Powers</th><th class="num">IMR</th><th class="num">Charges</th><th class="num">Tax</th>
          <th class="num split">Tadpoles</th><th class="num">Supply</th><th class="num">Spare</th></tr>
      </thead>
      <tbody>%s</tbody>
    </table></div>
%s
  </section>""" % (il.get("h2", ""), intro, "".join(panes), names["a"], names["b"],
                   "\n".join(trs), "\n".join(notes))


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
  </header>""" % (
        ' data-class="%s"' % d["class"] if d.get("class") else "",
        names["a"], names["b"], d.get("tagline", ""),
        names["a"], d.get("splits", {}).get("a", DASH),
        names["b"], d.get("splits", {}).get("b", DASH),
        d.get("ruleset", "Listo v10.2"))

    roster = """  <section>
    <div class="eyebrow"><span>Roster</span><span>27-point buy &middot; Lone Wolf +4 &times;2</span></div>
    <h2>%s</h2>
    <div class="duo">%s%s</div>
    %s
    %s
  </section>""" % (
        r.get("h2", ""), roster_pane(r["a"], "a"), roster_pane(r["b"], "b"),
        '<p class="note">%s</p>' % r["note"] if r.get("note") else "",
        derived(d, names))

    # Descending altitude: what the pair is, then how it fights, then how it is built,
    # then the per-level and per-item detail.
    sections = [head, profile(d, names), damage(d, names), play(d, names),
                roster, gates(d, names), progression(d, names), illithid(d, names),
                equipment(d, names), quests(d, names)]
    body = "\n\n".join(s for s in sections if s)
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
