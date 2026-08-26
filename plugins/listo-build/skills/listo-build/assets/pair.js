/* Builds the pair profile radar from the data attributes on
   <figure class="profile">, wires the act tabs, and writes the computed pair
   value into each table row's .pv span.

   Three series per act: A, B, and the pair. The pair is never authored —
   it is derived from data-kinds:

     additive       a + b        (uncapped; max 10)
     complementary  hi + floor(lo / 2)  (uncapped; max 7)
     personal       min(a, b)    (max 5)
     shared         max(a, b)    (max 5)

   Every series — A, B and pair — plots against data-need, the parity line for that
   axis (scoring.py NEED): four actions of ordinary un-Lone-Wolfed play. The rings therefore read as
   20/40/60/80/100% of a five-stack, and the outer ring is "keeping up", not
   "theoretical maximum". Values past parity clip, which is intended.

   The radar also COLLAPSES spokes for legibility, per scoring-model.md s10:
   data-collapse="1+0:Damage,5+4:Control" blends the crowd member (first index)
   and the priority member (second) by the act's own fight mix. The table keeps
   all ten rows — the collapse is presentation, never source.

   The pair value is NOT capped at 5 any more: capping made 5+4 and 5+0 read
   identically, which is the saturation that made a plain maximum wrong. Each
   spoke is therefore plotted as a PERCENT OF ITS OWN ACHIEVABLE MAXIMUM, so a
   personal axis at 5 and a complementary axis at 7 both reach the outer ring.
   See listo-build/references/scoring-model.md.

   If this never runs, the chart stays hidden (.profile:not(.ready) .radar),
   the .pv spans stay empty, and the table still carries both characters'
   numbers for all three acts — the chart is the summary, the table is the
   record. */
(function () {
  var CX = 130, CY = 100, STEP = 12.8, MAX = 5, LR = 76, NS = "http://www.w3.org/2000/svg";
  var ROMAN = ["I", "II", "III"];

  function el(name, attrs) {
    var e = document.createElementNS(NS, name);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }
  function nums(attr) {
    if (!attr) return null;
    var a = attr.split(",").map(function (n) { return parseFloat(n.trim()); });
    return a.every(function (n) { return isFinite(n); }) ? a : null;
  }
  var KIND_MAX = { additive: 10, complementary: 7, personal: 5, shared: 5 };
  /* Fallback parity line per kind, used only if data-need is absent. The renderer emits
     scoring.py's NEED: what the party Listo tunes for actually delivers — four actions of
     ordinary, un-Lone-Wolfed play. See scoring.py "display calibration". */
  var KIND_NEED = { additive: 8, complementary: 5, personal: 4, shared: 4 };
  /* act fight mix (crowd, priority) — the same weights the damage table uses. */
  var MIX = [[0.70, 0.30], [0.60, 0.40], [0.50, 0.50]];
  function kindMax(kind) { return KIND_MAX[kind] || MAX; }
  function kindNeed(kind) { return KIND_NEED[kind] || MAX; }
  /* v is plotted as a fraction of `full`, scaled onto the 0..MAX grid. */
  function at(u, v, full) {
    full = full || MAX;
    v = Math.max(0, Math.min(full, isFinite(v) ? v : 0)) / full * MAX;
    return [CX + u[0] * STEP * v, CY + u[1] * STEP * v];
  }
  function poly(U, get, full) {
    return U.map(function (u, i) {
      var p = at(u, get(i), full ? full(i) : MAX);
      return p[0].toFixed(1) + "," + p[1].toFixed(1);
    }).join(" ");
  }
  function combine(kind, a, b) {
    if (kind === "personal") return Math.min(a, b);
    /* complementary: the stronger half's coverage stands in full, the weaker half
       is credited at half, because some of it duplicates ground already covered. */
    if (kind === "complementary") {
      return Math.max(a, b) + Math.floor(Math.min(a, b) / 2);
    }
    if (kind === "additive") return a + b;
    /* shared: the pair rolls its better half, so the weaker one adds nothing. */
    if (kind === "shared") return Math.max(a, b);
    throw new Error("unknown axis kind: " + kind);
  }

  Array.prototype.forEach.call(document.querySelectorAll(".profile"), function (fig) {
    var axes = (fig.getAttribute("data-axes") || "").split(",")
      .map(function (s) { return s.trim(); }).filter(Boolean);
    var kinds = (fig.getAttribute("data-kinds") || "").split(",")
      .map(function (s) { return s.trim().toLowerCase(); });
    var names = (fig.getAttribute("data-names") || "A,B").split(",")
      .map(function (s) { return s.trim(); });
    var bands = (fig.getAttribute("data-bands") || "").split(",")
      .map(function (s) { return s.trim(); });
    var need = nums(fig.getAttribute("data-need"));

    /* Display collapse. Each group is "crowdIndex+priorityIndex:Label"; the two
       members leave the chart and one blended spoke takes the crowd member's slot. */
    var groups = (fig.getAttribute("data-collapse") || "").split(",")
      .map(function (g) { return g.trim(); }).filter(Boolean)
      .map(function (g) {
        var bits = g.split(":"), ix = bits[0].split("+");
        return { c: parseInt(ix[0], 10), p: parseInt(ix[1], 10), label: bits[1] || "" };
      });
    var folded = {};   /* axis index -> the group it belongs to, or null if it leads one */
    groups.forEach(function (g) { folded[g.c] = g; folded[g.p] = null; });

    function set(prefix) {
      return [1, 2, 3].map(function (n) {
        var s = nums(fig.getAttribute("data-" + prefix + n));
        return (s && s.length === axes.length) ? s : null;
      });
    }
    var A = set("a"), B = set("b");
    var box = fig.querySelector(".radar");
    if (axes.length < 3 || !box) return;

    var acts = [0, 1, 2].map(function (i) {
      if (!A[i] || !B[i]) return null;
      return {
        a: A[i], b: B[i],
        p: axes.map(function (_, k) { return combine(kinds[k], A[i][k], B[i][k]); })
      };
    });
    if (!acts.some(Boolean)) return;

    /* the spokes actually drawn: collapsed groups in place, everything else as-is. */
    var disp = [];
    axes.forEach(function (ax, i) {
      var g = folded[i];
      if (g === null) return;                       /* folded into its group's spoke */
      /* a group's two members share a parity line by construction — st/aoe both 10,
         the two control axes both 5 — so either member's value is the group's. */
      if (g) disp.push({ label: g.label || ax, kind: kinds[g.c], g: g,
                         need: need ? need[g.c] : kindNeed(kinds[g.c]) });
      else disp.push({ label: ax, kind: kinds[i], i: i,
                       need: need ? need[i] : kindNeed(kinds[i]) });
    });
    function fold(vec, act) {
      var w = MIX[act];
      return disp.map(function (d) {
        return d.g ? w[0] * vec[d.g.c] + w[1] * vec[d.g.p] : vec[d.i];
      });
    }
    acts.forEach(function (s, i) {
      if (!s) return;
      s.da = fold(s.a, i); s.db = fold(s.b, i); s.dp = fold(s.p, i);
    });

    var U = disp.map(function (_, i) {
      var a = (-90 + i * 360 / disp.length) * Math.PI / 180;
      return [Math.cos(a), Math.sin(a)];
    });

    var svg = el("svg", { viewBox: "0 0 260 200", role: "img" });
    var caption = el("title", {});
    svg.appendChild(caption);

    [1, 2, 3, 4, 5].forEach(function (v) {
      svg.appendChild(el("polygon", {
        "class": "r-ring" + (v === MAX ? " outer" : ""),
        points: poly(U, function () { return v; })
      }));
    });
    U.forEach(function (u) {
      var p = at(u, MAX);
      svg.appendChild(el("line", {
        "class": "r-spoke", x1: CX, y1: CY, x2: p[0].toFixed(1), y2: p[1].toFixed(1)
      }));
    });

    var shapeA = el("polygon", { "class": "r-a", points: "" });
    var shapeB = el("polygon", { "class": "r-b", points: "" });
    var shapeP = el("polygon", { "class": "r-pair", points: "" });
    var dots = el("g", {});
    svg.appendChild(shapeA);
    svg.appendChild(shapeB);
    svg.appendChild(shapeP);   /* pair drawn last so the dashed edge stays readable */
    svg.appendChild(dots);

    U.forEach(function (u, i) {
      var t = el("text", {
        "class": "r-label",
        x: (CX + u[0] * LR).toFixed(1),
        y: (CY + u[1] * LR + (u[1] < -0.5 ? -1 : u[1] > 0.5 ? 7 : 3)).toFixed(1),
        "text-anchor": u[0] > 0.2 ? "start" : u[0] < -0.2 ? "end" : "middle"
      });
      t.textContent = disp[i].label;
      svg.appendChild(t);
    });

    var band = fig.querySelector(".r-band");
    box.insertBefore(svg, band || null);

    var legend = fig.querySelector(".r-legend");
    if (legend) {
      legend.innerHTML =
        '<span class="lg-a"><i></i>' + names[0] + '</span>' +
        '<span class="lg-b"><i></i>' + (names[1] || "B") + '</span>' +
        '<span class="lg-p"><i></i>Pair</span>';
    }

    var rows = Array.prototype.slice.call(fig.querySelectorAll(".r-table tbody tr"));
    var tabs = Array.prototype.slice.call(fig.querySelectorAll(".r-tab"));

    function show(n) {
      var s = acts[n - 1];
      if (!s) return;

      /* All three series share one denominator per spoke: the PARITY line — what a
         five-person party, the size Listo tunes encounters for, delivers on that axis.
         Two earlier schemes were both wrong. Bodies on a 0..5 grid with the pair on the
         kind ceiling made the scales silently incomparable (an additive pair of 7 and a
         body of 3.5 both landed at 70%, so the pair line sat ON the bodies). Everything
         on the kind ceiling fixed that but left the outer ring meaning "two maxed bodies",
         a theoretical sum nothing is measured against. Parity is a real demand line, so a
         reading of 80% means four fifths of a five-stack — and clipping past it is right,
         because surplus is surplus. */
      var full = function (i) { return disp[i].need; };
      shapeA.setAttribute("points", poly(U, function (i) { return s.da[i]; }, full));
      shapeB.setAttribute("points", poly(U, function (i) { return s.db[i]; }, full));
      shapeP.setAttribute("points", poly(U, function (i) { return s.dp[i]; }, full));

      while (dots.firstChild) dots.removeChild(dots.firstChild);
      U.forEach(function (u, i) {
        var pa = at(u, s.da[i], full(i)), pb = at(u, s.db[i], full(i));
        dots.appendChild(el("circle", { "class": "r-dot-a", r: 3.4, cx: pa[0].toFixed(1), cy: pa[1].toFixed(1) }));
        dots.appendChild(el("circle", { "class": "r-dot-b", r: 3.4, cx: pb[0].toFixed(1), cy: pb[1].toFixed(1) }));
      });

      caption.textContent = "Act " + ROMAN[n - 1] + " pair profile, scored 0 to 5: " +
        disp.map(function (d, i) {
          var r = function (v) { return Math.round(v * 10) / 10; };
          return d.label + " — " + names[0] + " " + r(s.da[i]) + ", " +
                 (names[1] || "B") + " " + r(s.db[i]) + ", pair " + r(s.dp[i]);
        }).join("; ");

      if (band) {
        band.textContent = "Act " + ROMAN[n - 1] +
          (bands[n - 1] ? " · char " + bands[n - 1] + " · approximate" : "");
      }

      rows.forEach(function (tr, i) {
        Array.prototype.forEach.call(tr.querySelectorAll("td.sc"), function (td) {
          var pv = td.querySelector(".pv");
          if (!pv) return;
          var act = td.classList.contains("a1") ? 1 : td.classList.contains("a2") ? 2 : 3;
          var src = acts[act - 1];
          pv.textContent = (src && i < axes.length) ? src.p[i] : "";
        });
      });

      tabs.forEach(function (b) {
        var on = b.getAttribute("data-act") === String(n);
        b.setAttribute("aria-selected", on ? "true" : "false");
        b.tabIndex = on ? 0 : -1;
      });
      Array.prototype.forEach.call(fig.querySelectorAll(".a1, .a2, .a3"), function (c) {
        c.classList.toggle("on", c.classList.contains("a" + n));
      });
    }

    tabs.forEach(function (b, i) {
      var n = parseInt(b.getAttribute("data-act"), 10);
      if (!acts[n - 1]) { b.disabled = true; return; }
      b.addEventListener("click", function () { show(n); });
      b.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var k = i;
        do { k = ((k + d) % tabs.length + tabs.length) % tabs.length; }
        while (tabs[k].disabled && k !== i);
        tabs[k].focus();
        show(parseInt(tabs[k].getAttribute("data-act"), 10));
      });
    });

    show(acts[2] ? 3 : acts[1] ? 2 : 1);
    fig.classList.add("ready");
  });
})();
