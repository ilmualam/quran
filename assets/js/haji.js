/* Haji & Umrah widgets (/haji-umrah/*): tawaf & sa'ie counter, dam checker, packing checklist, days to Arafah.
   Every widget is pre-rendered by tools/pages20.py; this only adds behaviour. State stays in localStorage. */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode: keep in memory only */ } }
  };

  // ---- days to Arafah ----
  var now = new Date(), today = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());
  [].forEach.call(document.querySelectorAll("[data-hu-days]"), function (el) {
    var p = el.getAttribute("data-hu-days").split("-"), n = Math.round((Date.UTC(+p[0], p[1] - 1, +p[2]) - today) / 864e5);
    el.textContent = n > 1 ? n + " hari lagi" : n === 1 ? "esok" : n === 0 ? "hari ini" : "telah berlalu";
  });

  // ---- tawaf & sa'ie counter ----
  var ctr = $("hu-ctr");
  if (ctr) {
    var KEY = "hu-ctr", st = store.get(KEY, { m: "tawaf", tawaf: 0, saie: 0 });
    var btn = $("hu-btn"), num = $("hu-n"), hint = $("hu-hint"), dots = $("hu-dots").children;
    var chips = ctr.querySelectorAll("[data-m]");
    var hintOf = function (m, n) {
      if (m === "tawaf") {
        if (n === 0) return "Mula di garisan Hajarul Aswad, Kaabah di sebelah kiri. Isyarat dan bertakbir, kemudian tekan butang apabila kembali ke garisan.";
        if (n === 7) return "Tawaf selesai. Seterusnya: tutup bahu kanan, solat sunat tawaf 2 rakaat dan minum air zamzam.";
        return "Pusingan " + n + " selesai. Seterusnya pusingan " + (n + 1) + (n < 3 ? " (lelaki: berlari-lari anak)" : "") + ". Isyarat dan bertakbir di garisan Hajarul Aswad.";
      }
      if (n === 0) return "Mula di Safa: baca Al-Baqarah 158, menghadap Kaabah dan berzikir, kemudian berjalan ke Marwah.";
      if (n === 7) return "Sa'ie selesai di Marwah. Seterusnya: bercukur atau bergunting (tahallul).";
      var at = n % 2 ? "Marwah" : "Safa", to = n % 2 ? "Safa" : "Marwah";
      return "Pusingan " + n + " selesai di " + at + ". Berzikir dan berdoa, kemudian pusingan " + (n + 1) + ": " + at + " → " + to + ".";
    };
    var draw = function () {
      var m = st.m, n = st[m];
      ctr.setAttribute("data-mode", m);
      num.textContent = n;
      hint.textContent = hintOf(m, n);
      btn.disabled = n >= 7;
      btn.setAttribute("aria-label", "Tanda pusingan selesai: " + n + " daripada 7 " + (m === "tawaf" ? "tawaf" : "sa'ie"));
      for (var i = 0; i < dots.length; i++) dots[i].className = i < n ? "on" : "";
      for (var j = 0; j < chips.length; j++) chips[j].setAttribute("aria-pressed", chips[j].getAttribute("data-m") === m ? "true" : "false");
      store.set(KEY, st);
    };
    var buzz = function (ms) { if (navigator.vibrate) navigator.vibrate(ms); };
    btn.addEventListener("click", function () { if (st[st.m] < 7) { st[st.m]++; buzz(st[st.m] === 7 ? [80, 60, 80] : 40); draw(); } });
    $("hu-undo").addEventListener("click", function () { if (st[st.m] > 0) { st[st.m]--; draw(); } });
    $("hu-reset").addEventListener("click", function () { st[st.m] = 0; draw(); });
    for (var c = 0; c < chips.length; c++) chips[c].addEventListener("click", function () { st.m = this.getAttribute("data-m"); draw(); });
    draw();
  }

  // ---- dam checker ----
  var sel = $("hu-dsel");
  if (sel) {
    var outs = $("hu-dout").children;
    var show = function () { for (var i = 0; i < outs.length; i++) outs[i].hidden = outs[i].getAttribute("data-k") !== sel.value; };
    sel.addEventListener("change", show);
    show();
  }

  // ---- packing checklist ----
  var list = $("hu-list");
  if (list) {
    var CK = "hu-list", ticks = store.get(CK, {}), boxes = list.querySelectorAll("input[data-k]"), prog = $("hu-cprog");
    var count = function () {
      var n = 0;
      for (var i = 0; i < boxes.length; i++) if (boxes[i].checked) n++;
      prog.textContent = n + " / " + boxes.length + " siap" + (n === boxes.length ? " ✓ Semua sudah disediakan" : "");
    };
    for (var i = 0; i < boxes.length; i++) {
      boxes[i].checked = !!ticks[boxes[i].getAttribute("data-k")];
      boxes[i].addEventListener("change", function () {
        var k = this.getAttribute("data-k");
        if (this.checked) ticks[k] = 1; else delete ticks[k];
        store.set(CK, ticks);
        count();
      });
    }
    $("hu-creset").addEventListener("click", function () {
      ticks = {};
      store.set(CK, ticks);
      for (var i = 0; i < boxes.length; i++) boxes[i].checked = false;
      count();
    });
    $("hu-cprint").addEventListener("click", function () { window.print(); });
    count();
  }
})();
