/* IlmuAlam Quran Engine (Enterprise) © 2026 ilmualam.com — v2.0 */
(function () {
  "use strict";

  const OWNER = "ilmualam.com";
  const ALLOW = ["ilmualam.com", "www.ilmualam.com", "ilmualam.blogspot.com", "blogger.com", "blogspot.com", "draft.blogger.com"];
  const host = (location.hostname || "").toLowerCase();
  const okHost = ALLOW.some(d => host === d || host.endsWith("." + d));
  if (!okHost) return;

  function boot() { document.querySelectorAll(".ilmq[data-surah]").forEach(init); }

  function init(root) {
    const surah = parseInt(root.getAttribute("data-surah"), 10);
    if (!surah || surah < 1 || surah > 114) return;

    const $ = (q) => root.querySelector(q);
    const $$ = (q) => Array.from(root.querySelectorAll(q));

    let versesEl = $('[data-bind="verses"]');
    let audio = $('[data-bind="audio"]');
    let playBtn = $('[data-action="playpause"]');
    let barWrap = $('[data-action="seek"]');
    let barFill = barWrap ? barWrap.querySelector("i") : null;
    let verseLabel = $('[data-bind="currentVerse"]');
    let timeLabel = $('[data-bind="time"]');
    let qariSel = $('[data-bind="qari"]');
    let toastEl = $('[data-bind="toast"]');
    let ayahCountBind = $('[data-bind="ayahCount"]');
    let revelationBind = $('[data-bind="revelation"]');

    let verses = [];
    let idx = 0;
    let ready = false;
    let userPaused = true;

    // ---- Toolbar injection (tabs + action chips) — reuses .tools/.tabs/.tab/.act/.chip,
    // classes already shipped in quran.min.css, just never wired up by the JSON-fetch engine ----
    ensureToolRow(root);
    const tabs = $$(".tab");
    const modeBtn = $('[data-action="mode"]');
    const copyChip = $('[data-action="copy"]');
    const shareChip = $('[data-action="share"]');
    const bmChip = $('[data-action="bookmark"]');
    const resumeChip = $('[data-action="resume"]');

    const storeKey = `ilmq_${surah}`;
    const store = {
      get(k, d) { try { const v = JSON.parse(localStorage.getItem(`${storeKey}:${k}`)); return v === null || v === undefined ? d : v; } catch { return d; } },
      set(k, v) { try { localStorage.setItem(`${storeKey}:${k}`, JSON.stringify(v)); } catch {} }
    };

    let tab = store.get("tab", "all"); // all | arab | rumi | ms

    // ---- Theme mode — data-mode attribute matches :where(.ilmq[data-mode="dark"]) already in CSS ----
    function applyMode(mode) {
      store.set("mode", mode);
      if (mode === "auto") root.removeAttribute("data-mode");
      else root.setAttribute("data-mode", mode);
      if (modeBtn) modeBtn.textContent = mode === "dark" ? "🌙" : mode === "light" ? "☀️" : "🌓";
    }
    applyMode(store.get("mode", "auto"));

    // ---- Font size vars — FIX: single source of truth, always stored as raw number,
    // always written to CSS with px. CSS now reads var(--fzT) directly (no calc*1px double-unit bug). ----
    const fzA = store.get("fzA", 30);
    const fzT = store.get("fzT", 16);
    root.style.setProperty("--fzA", `${fzA}px`);
    root.style.setProperty("--fzT", `${fzT}px`);

    const arabicRange = $('[data-bind="arabicSize"]');
    const transRange = $('[data-bind="translationSize"]');
    const autoScrollChk = $('[data-bind="autoScroll"]');
    const autoNextChk = $('[data-bind="autoNext"]');
    if (arabicRange) arabicRange.value = fzA;
    if (transRange) transRange.value = fzT;
    if (autoScrollChk) autoScrollChk.checked = store.get("autoScroll", true);
    if (autoNextChk) autoNextChk.checked = store.get("autoNext", true);

    if (qariSel) {
      const map = {
        "Mishary Rashid Alafasy": "M. R. Alafasy",
        "Abdul Rahman Al-Sudais": "A. R. Sudais",
        "Mahmoud Khalil Al-Husary": "M. K. Husary",
        "Abdul Basit": "Abdul Basit",
        "Saad Al-Ghamadi": "S. Al-Ghamadi"
      };
      Array.from(qariSel.options).forEach(opt => {
        const t = opt.textContent.trim();
        if (map[t]) opt.textContent = map[t];
      });
    }

    const toast = (m) => {
      if (!toastEl) return;
      toastEl.textContent = m;
      toastEl.classList.add("on");
      clearTimeout(toastEl._t);
      toastEl._t = setTimeout(() => toastEl.classList.remove("on"), 1400);
    };

    const formatTime = (s) => {
      if (!isFinite(s) || s < 0) return "0:00";
      const m = Math.floor(s / 60), sec = Math.floor(s % 60);
      return `${m}:${String(sec).padStart(2, "0")}`;
    };

    const setPlayUI = (playing) => {
      if (!playBtn) return;
      playBtn.setAttribute("aria-pressed", playing ? "true" : "false");
      playBtn.innerHTML = playing ? "⏸" : "▶️";
    };

    const markPlaying = (index) => {
      if (!versesEl) return;
      versesEl.querySelectorAll(".v.playing").forEach(n => n.classList.remove("playing"));
      const card = versesEl.querySelector(`.v[data-i="${index}"]`);
      if (card) {
        card.classList.add("playing");
        const sc = autoScrollChk ? autoScrollChk.checked : store.get("autoScroll", true);
        if (sc) card.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    };

    function escapeHTML(s) {
      return String(s || "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
    }

    function formatCopy(i) {
      const v = verses[i];
      return `Surah ${surah}:${i + 1}\n${v.arabic}\nRumi: ${v.rumi}\nMaksud: ${v.ms}\n— ${OWNER}`;
    }

    async function copyText(text) {
      try { await navigator.clipboard.writeText(text); toast("Disalin ✅"); }
      catch {
        const ta = document.createElement("textarea");
        ta.value = text; ta.style.position = "fixed"; ta.style.left = "-9999px";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); toast("Disalin ✅"); } catch { toast("Gagal salin."); }
        ta.remove();
      }
    }

    // ---- Bookmarks ----
    function getBookmarks() { return store.get("bm", []); }
    function toggleBookmark(i) {
      const list = new Set(getBookmarks());
      if (list.has(i)) list.delete(i); else list.add(i);
      store.set("bm", Array.from(list).sort((a, b) => a - b));
      paintBookmarks();
      toast(list.has(i) ? "Bookmark ★" : "Bookmark dibuang");
    }
    function paintBookmarks() {
      const list = new Set(getBookmarks());
      versesEl.querySelectorAll(".v").forEach(card => {
        const i = parseInt(card.dataset.i, 10);
        const star = card.querySelector('[data-act="bm"]');
        if (!star) return;
        star.textContent = list.has(i) ? "★" : "☆";
        star.classList.toggle("on", list.has(i));
      });
    }

    // ---- Tab filter — classList only, never .style.display (R6) ----
    function applyTab() {
      store.set("tab", tab);
      tabs.forEach(b => b.classList.toggle("active", b.dataset.tab === tab));
      tabs.forEach(b => b.setAttribute("aria-selected", b.dataset.tab === tab ? "true" : "false"));
      versesEl.querySelectorAll(".v").forEach(card => {
        const a = card.querySelector(".arab");
        const r = card.querySelector(".rumi");
        const m = card.querySelector(".mal");
        if (a) a.classList.toggle("hide", !(tab === "all" || tab === "arab"));
        if (r) r.classList.toggle("hide", !(tab === "all" || tab === "rumi"));
        if (m) m.classList.toggle("hide", !(tab === "all" || tab === "ms"));
      });
    }

    function currentAyahText() {
      const v = verses[idx];
      if (!v) return "";
      const parts = [];
      if (tab === "all" || tab === "arab") parts.push(v.arabic);
      if (tab === "all" || tab === "rumi") parts.push(`Rumi: ${v.rumi}`);
      if (tab === "all" || tab === "ms") parts.push(`Maksud: ${v.ms}`);
      return parts.join("\n");
    }

    async function loadAyah(index, autoplay) {
      idx = Math.max(0, Math.min(verses.length - 1, index));
      if (verseLabel) verseLabel.textContent = `Ayat ${idx + 1}`;
      markPlaying(idx);
      store.set("resume", { idx, t: Date.now() });

      if (audio) {
        const qari = qariSel ? qariSel.value : "Alafasy_128kbps";
        audio.src = `https://everyayah.com/data/${qari}/${String(surah).padStart(3, "0")}${String(idx + 1).padStart(3, "0")}.mp3`;
        audio.load();
        if (autoplay) {
          try { await audio.play(); userPaused = false; setPlayUI(true); }
          catch { userPaused = true; setPlayUI(false); }
        } else { userPaused = true; setPlayUI(false); }
      }
    }

    async function togglePlay() {
      if (!ready || !audio) return;
      if (!audio.src) return loadAyah(idx, true);
      if (audio.paused) { try { await audio.play(); userPaused = false; setPlayUI(true); } catch { toast("Klik ▶️ untuk mula."); } }
      else { audio.pause(); userPaused = true; setPlayUI(false); }
    }

    function renderVerses() {
      if (!versesEl) return;
      const frag = document.createDocumentFragment();
      verses.forEach((v, i) => {
        const card = document.createElement("article");
        card.className = "v";
        card.dataset.i = String(i);
        card.innerHTML = `
          <div class="top">
            <div class="no">${surah}:${i + 1}</div>
            <div class="va">
              <button class="vbtn p" type="button" data-act="play">Play</button>
              <button class="vbtn" type="button" data-act="copy">Copy</button>
              <button class="vbtn star" type="button" data-act="bm" aria-label="Bookmark ayat">☆</button>
            </div>
          </div>
          <div class="arab">${v.arabic}</div>
          <p class="rumi"><strong>Rumi:</strong> ${escapeHTML(v.rumi)}</p>
          <p class="mal"><strong>Maksud:</strong> ${escapeHTML(v.ms)}</p>
        `;
        card.addEventListener("click", (e) => { if (!e.target?.dataset?.act) loadAyah(i, true); });
        card.querySelector('[data-act="play"]').addEventListener("click", (e) => {
          e.stopPropagation();
          if (idx !== i) loadAyah(i, true); else togglePlay();
        });
        card.querySelector('[data-act="copy"]').addEventListener("click", (e) => {
          e.stopPropagation(); copyText(formatCopy(i));
        });
        card.querySelector('[data-act="bm"]').addEventListener("click", (e) => {
          e.stopPropagation(); toggleBookmark(i);
        });
        frag.appendChild(card);
      });
      versesEl.innerHTML = "";
      versesEl.appendChild(frag);
      applyTab();
      markPlaying(idx);
      paintBookmarks();
    }

    async function loadSurah() {
      const jsonUrl = `https://cdn.jsdelivr.net/gh/ilmualam/quran@main/data-surah/surah-${surah}.json`;
      let dataSurah;
      try {
        const response = await fetch(jsonUrl, { cache: "no-store" });
        if (!response.ok) throw new Error("Gagal HTTP " + response.status);
        dataSurah = await response.json();
      } catch (err) {
        if (versesEl) versesEl.innerHTML = `<div class="loading">❌ Ralat memuat data surah-${surah}.json. Sila refresh.</div>`;
        toast("Gagal memuatkan data surah.");
        return;
      }

      verses = dataSurah.map((x) => ({ arabic: x.arabic || "", ms: x.translation || x.ms || "", rumi: x.rumi || "" }));
      if (ayahCountBind) ayahCountBind.textContent = String(verses.length);
      if (revelationBind && !revelationBind.textContent.trim()) revelationBind.textContent = "Makkiyyah";

      ready = true;
      renderVerses();
      const res = store.get("resume", null);
      const startIdx = res?.idx >= 0 ? Math.min(res.idx, verses.length - 1) : 0;
      await loadAyah(startIdx, false);
    }

    // ---- Events ----
    playBtn?.addEventListener("click", togglePlay);
    qariSel?.addEventListener("change", async () => { if (ready) { const wasPlaying = audio && !audio.paused; await loadAyah(idx, !!wasPlaying); toast("Qari ditukar."); } });

    if (audio) {
      audio.addEventListener("timeupdate", () => {
        if (!audio.duration) return;
        const pct = (audio.currentTime / audio.duration) * 100;
        if (barFill) barFill.style.width = pct.toFixed(2) + "%";
        if (timeLabel) timeLabel.textContent = `${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
      });
      audio.addEventListener("play", () => { setPlayUI(true); markPlaying(idx); });
      audio.addEventListener("pause", () => { if (userPaused) setPlayUI(false); });
      audio.addEventListener("ended", async () => {
        setPlayUI(false);
        const nextOn = autoNextChk ? autoNextChk.checked : store.get("autoNext", true);
        if (nextOn && idx + 1 < verses.length) await loadAyah(idx + 1, true);
        else userPaused = true;
      });
    }

    barWrap?.addEventListener("click", (e) => {
      if (!audio || !audio.duration) return;
      const rect = barWrap.getBoundingClientRect();
      const x = Math.max(0, Math.min(rect.width, e.clientX - rect.left));
      audio.currentTime = (x / rect.width) * audio.duration;
    });

    // FIX: both sliders now write the SAME contract the CSS expects — full px string, no double-unit calc.
    arabicRange?.addEventListener("input", () => { root.style.setProperty("--fzA", `${arabicRange.value}px`); store.set("fzA", arabicRange.value); });
    transRange?.addEventListener("input", () => { root.style.setProperty("--fzT", `${transRange.value}px`); store.set("fzT", transRange.value); });
    autoScrollChk?.addEventListener("change", () => store.set("autoScroll", !!autoScrollChk.checked));
    autoNextChk?.addEventListener("change", () => store.set("autoNext", !!autoNextChk.checked));

    tabs.forEach(b => b.addEventListener("click", () => { tab = b.dataset.tab; applyTab(); }));
    modeBtn?.addEventListener("click", () => {
      const cur = store.get("mode", "auto");
      const next = cur === "auto" ? "dark" : cur === "dark" ? "light" : "auto";
      applyMode(next); toast("Mod: " + next);
    });
    copyChip?.addEventListener("click", () => copyText(currentAyahText() || formatCopy(idx)));
    shareChip?.addEventListener("click", async () => {
      const text = formatCopy(idx);
      const url = location.href.split("#")[0] + `#ayah-${surah}-${idx + 1}`;
      try {
        if (navigator.share) { await navigator.share({ title: `Surah ${surah}:${idx + 1}`, text, url }); toast("Dikongsi ✅"); }
        else { await copyText(url); toast("Pautan disalin ✅"); }
      } catch { /* user cancelled */ }
    });
    bmChip?.addEventListener("click", () => toggleBookmark(idx));
    resumeChip?.addEventListener("click", async () => {
      const res = store.get("resume", null);
      if (res?.idx >= 0) { await loadAyah(res.idx, false); toast("Sambung ayat terakhir."); }
      else toast("Tiada rekod sambung.");
    });

    window.addEventListener("hashchange", () => {
      const h = (location.hash || "").replace("#", "");
      const m = h.match(/^ayah-(\d+)-(\d+)$/);
      if (!m) return;
      const s = parseInt(m[1], 10), a = parseInt(m[2], 10);
      if (s === surah && a >= 1 && a <= verses.length) loadAyah(a - 1, false);
    });

    loadSurah();
  }

  // ---- Injects the tab row + action-chip row once per instance ----
  // Reuses .tools/.tabs/.tab/.act/.chip — these selectors already exist in quran.min.css.
  function ensureToolRow(root) {
    if (root.querySelector(".tools")) return;
    const row = document.createElement("div");
    row.className = "tools";
    row.innerHTML = `
      <div class="tabs" role="tablist" aria-label="Paparan">
        <button class="tab" data-tab="all" aria-selected="true" type="button">Semua</button>
        <button class="tab" data-tab="arab" aria-selected="false" type="button">Arab</button>
        <button class="tab" data-tab="rumi" aria-selected="false" type="button">Rumi</button>
        <button class="tab" data-tab="ms" aria-selected="false" type="button">Melayu</button>
      </div>
      <div class="act" aria-label="Tindakan">
        <button class="chip" data-action="mode" type="button" title="Tukar mod">🌓</button>
        <button class="chip" data-action="resume" type="button" title="Sambung ayat terakhir">⏯</button>
        <button class="chip" data-action="bookmark" type="button" title="Bookmark ayat semasa">★</button>
        <button class="chip" data-action="copy" type="button" title="Salin ayat semasa">⎘</button>
        <button class="chip" data-action="share" type="button" title="Kongsi ayat semasa">✆</button>
      </div>
    `;
    const after = root.querySelector(".player");
    if (after) after.insertAdjacentElement("afterend", row);
    else root.insertAdjacentElement("afterbegin", row);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", () => setTimeout(boot, 300));
  else setTimeout(boot, 300);
})();
