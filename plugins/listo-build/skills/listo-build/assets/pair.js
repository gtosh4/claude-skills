/* Builds the pair profile radar from the data attributes on
   <figure class="profile">, wires the act tabs, and writes the computed pair
   value into each table row's .pv span.

   Three series per act: A, B, and the pair. The pair is never authored —
   it is derived from data-kinds:

     additive   min(5, a + b)
     threshold  max(a, b)
     personal   min(a, b)

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
  function at(u, v) {
    v = Math.max(0, Math.min(MAX, isFinite(v) ? v : 0));
    return [CX + u[0] * STEP * v, CY + u[1] * STEP * v];
  }
  function poly(U, get) {
    return U.map(function (u, i) {
      var p = at(u, get(i));
      return p[0].toFixed(1) + "," + p[1].toFixed(1);
    }).join(" ");
  }
  function combine(kind, a, b) {
    if (kind === "threshold") return Math.max(a, b);
    if (kind === "personal") return Math.min(a, b);
    /* complementary: the stronger half's coverage stands in full, the weaker half
       is credited at half, because some of it duplicates ground already covered. */
    if (kind === "complementary") {
      return Math.min(MAX, Math.max(a, b) + Math.floor(Math.min(a, b) / 2));
    }
    return Math.min(MAX, a + b);
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

    var U = axes.map(function (_, i) {
      var a = (-90 + i * 360 / axes.length) * Math.PI / 180;
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
      t.textContent = axes[i];
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

      shapeA.setAttribute("points", poly(U, function (i) { return s.a[i]; }));
      shapeB.setAttribute("points", poly(U, function (i) { return s.b[i]; }));
      shapeP.setAttribute("points", poly(U, function (i) { return s.p[i]; }));

      while (dots.firstChild) dots.removeChild(dots.firstChild);
      U.forEach(function (u, i) {
        var pa = at(u, s.a[i]), pb = at(u, s.b[i]);
        dots.appendChild(el("circle", { "class": "r-dot-a", r: 3.4, cx: pa[0].toFixed(1), cy: pa[1].toFixed(1) }));
        dots.appendChild(el("circle", { "class": "r-dot-b", r: 3.4, cx: pb[0].toFixed(1), cy: pb[1].toFixed(1) }));
      });

      caption.textContent = "Act " + ROMAN[n - 1] + " pair profile, scored 0 to 5: " +
        axes.map(function (ax, i) {
          return ax + " — " + names[0] + " " + s.a[i] + ", " + (names[1] || "B") + " " + s.b[i] +
                 ", pair " + s.p[i];
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
