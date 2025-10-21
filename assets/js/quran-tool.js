(function(){
  "use strict";

  // ====== CONFIG ======
  const CFG = {
    siteName: "ilmualam.com",
    defaultSurah: 1,
    defaultAyah: 1,
    defaultTranslation: "en.sahih", // Saheeh International (AlQuran Cloud code)
    defaultReciter: "ar.alafasy",   // Mishary Alafasy (CDN folder code)
    apiLang: "en",                  // for names
    storageKey: "qa-bookmarks-v1",
    cacheTTLms: 5*60*1000           // 5 min micro-cache in sessionStorage
  };

  // AlQuran Cloud + Islamic Network CDN
  const ENDPOINTS = {
    surahList: "https://api.alquran.cloud/v1/surah",
    juzList:   "https://api.alquran.cloud/v1/juz",
    // verse set: edition can be "quran-uthmani" for Arabic; translations like "en.sahih"
    verses:    (surah, edition) => `https://api.alquran.cloud/v1/surah/${surah}/${edition}`,
    singleAyah:(surah, ayah, edition) => `https://api.alquran.cloud/v1/ayah/${surah}:${ayah}/${edition}`,
    translationsList: "https://api.alquran.cloud/v1/edition?format=text&type=translation",
    // Audio CDN (per ayah): https://cdn.islamic.network/quran/audio/128/ar.alafasy/{ayahNumber}.mp3
    audioAyah: (globalAyahNumber, reciter="ar.alafasy", bitrate=128) =>
      `https://cdn.islamic.network/quran/audio/${bitrate}/${reciter}/${globalAyahNumber}.mp3`
  };

  // Quran Foundation (optional future swap):
  // const ENDPOINTS = { ... see https://api-docs.quran.foundation ... }  // :contentReference[oaicite:3]{index=3}

  // ====== UTIL ======
  const $ = sel => document.querySelector(sel);
  const state = {
    surahs: [], juz: [],
    currentSurah: CFG.defaultSurah,
    currentAyah: CFG.defaultAyah,
    currentTranslation: CFG.defaultTranslation,
    currentReciter: CFG.defaultReciter,
    versesArabic: null,
    versesTrans: null,
    continuous: false
  };

  function cacheGet(key){
    try{
      const raw = sessionStorage.getItem(key);
      if(!raw) return null;
      const obj = JSON.parse(raw);
      if(Date.now()-obj.t > CFG.cacheTTLms) return null;
      return obj.v;
    }catch(_){ return null; }
  }
  function cacheSet(key, value){
    try{ sessionStorage.setItem(key, JSON.stringify({t:Date.now(), v:value})); }catch(_){}
  }
  async function getJSON(url){
    const hit = cacheGet(url); if(hit) return hit;
    const r = await fetch(url); if(!r.ok) throw new Error("Network");
    const j = await r.json(); cacheSet(url, j); return j;
  }
  function showStatus(msg){ $("#qa-status").textContent = msg; setTimeout(()=>$("#qa-status").textContent="", 2000); }

  // ====== LOADERS ======
  async function loadMeta(){
    const [s, t] = await Promise.all([
      getJSON(ENDPOINTS.surahList),
      getJSON(ENDPOINTS.translationsList)
    ]);
    state.surahs = s.data; // [{number, englishName, name, ayahs, ...}]
    // Keep only popular translations (you can expand)
    const popular = ["en.sahih","ms.basmeih","id.indonesian","ur.jalandhry"];
    const tr = t.data.filter(e => popular.includes(`${e.language}.${e.identifier}`) || popular.includes(e.identifier));
    const selectTr = $("#qa-translation");
    const seen = new Set();
    tr.forEach(e=>{
      // Normalize code like "en.sahih"
      const code = e.identifier.includes(".") ? e.identifier : `${e.language}.${e.identifier}`;
      if(seen.has(code)) return; seen.add(code);
      const opt = document.createElement("option");
      opt.value = code;
      opt.textContent = `${e.language.toUpperCase()} — ${e.englishName}`;
      selectTr.appendChild(opt);
    });
    selectTr.value = CFG.defaultTranslation;

    // Reciters (CDN folders); keep a small curated list for reliability
    const reciters = [
      {id:"ar.alafasy", name:"Mishary Rashid Alafasy"},
      {id:"ar.husary",  name:"Mahmoud Khalil Al-Husary"},
      {id:"ar.minshawi",name:"Muhammad Siddiq Al-Minshawi"}
    ];
    const rSel = $("#qa-reciter");
    reciters.forEach(r=>{
      const o = document.createElement("option");
      o.value = r.id; o.textContent = r.name; rSel.appendChild(o);
    });
    rSel.value = CFG.defaultReciter;

    // Fill Surah list
    const sSel = $("#qa-surah");
    s.data.forEach(x=>{
      const o = document.createElement("option");
      o.value = x.number;
      o.textContent = `${x.number}. ${x.englishName} (${x.name})`;
      sSel.appendChild(o);
    });

    // Juz (1-30)
    const jSel = $("#qa-juz");
    for(let i=1;i<=30;i++){
      const o = document.createElement("option");
      o.value = i; o.textContent = `Juz ${i}`;
      jSel.appendChild(o);
    }
  }

  async function loadSurah(surahNo){
    const [ar, tr] = await Promise.all([
      getJSON(ENDPOINTS.verses(surahNo, "quran-uthmani")),
      getJSON(ENDPOINTS.verses(surahNo, state.currentTranslation))
    ]);
    state.versesArabic = ar.data.ayahs;
    state.versesTrans = tr.data.ayahs;
    // fill ayah selector
    const aSel = $("#qa-ayah");
    aSel.innerHTML = "";
    for(let i=1;i<=state.versesArabic.length;i++){
      const o = document.createElement("option");
      o.value = i; o.textContent = `Ayah ${i}`;
      aSel.appendChild(o);
    }
    $("#qa-title").textContent = surahTitle(surahNo);
  }

  function surahTitle(n){
    const s = state.surahs.find(x=>x.number==n);
    return s ? `${s.number}. ${s.englishName} — ${s.name}` : `Surah ${n}`;
  }

  function setHash(surah, ayah){
    location.hash = `#/surah/${surah}/${ayah}`;
  }

  function parseHash(){
    const m = location.hash.match(/#\/surah\/(\d+)\/(\d+)/);
    if(m){ return {s: +m[1], a: +m[2]}; }
    return null;
  }

  function globalAyahNumber(surah, ayah){
    // sum of ayahs before this surah + ayah; use cached surah list
    let total=0;
    for(const s of state.surahs){
      if(s.number < surah) total += s.numberOfAyahs || s.ayahs || 0;
    }
    return total + ayah;
  }

  function renderAyah(){
    const i = state.currentAyah-1;
    const ar = state.versesArabic?.[i]; const tr = state.versesTrans?.[i];
    $("#qa-ar").textContent = ar ? ar.text : "";
    $("#qa-tr").textContent = tr ? tr.text : "";
    $("#qa-ayah").value = state.currentAyah;
    $("#qa-title").textContent = surahTitle(state.currentSurah) + ` — Ayah ${state.currentAyah}`;
    setHash(state.currentSurah, state.currentAyah);

    // load audio
    const g = globalAyahNumber(state.currentSurah, state.currentAyah);
    const url = ENDPOINTS.audioAyah(g, state.currentReciter, 128);
    const audio = $("#qa-audio");
    if(audio.src !== url){ audio.src = url; }
  }

  async function goto(surah, ayah){
    if(surah !== state.currentSurah){
      state.currentSurah = surah;
      await loadSurah(surah);
    }
    state.currentAyah = Math.max(1, Math.min(ayah, state.versesArabic.length));
    renderAyah();
  }

  // ====== EVENTS ======
  document.addEventListener("DOMContentLoaded", async ()=>{
    await loadMeta();

    // Deep link or default
    const hash = parseHash();
    const s0 = hash?.s || CFG.defaultSurah;
    const a0 = hash?.a || CFG.defaultAyah;
    $("#qa-surah").value = s0;
    await loadSurah(s0);
    await goto(s0, a0);

    // Listeners
    $("#qa-surah").addEventListener("change", async (e)=>{ await goto(+e.target.value, 1); });
    $("#qa-ayah").addEventListener("change", async (e)=>{ await goto(state.currentSurah, +e.target.value); });
    $("#qa-juz").addEventListener("change", async (e)=>{
      const j = +e.target.value;
      // Map simple Juz -> first surah/ayah of that Juz via minimal table
      // Lightweight mapping: known starting points from AlQuran Cloud
      const JMAP = {
        1:[1,1],2:[2,142],3:[2,253],4:[3,93],5:[4,24],6:[4,148],7:[5,82],8:[6,111],9:[7,88],10:[8,41],
        11:[9,93],12:[11,6],13:[12,53],14:[15,1],15:[17,1],16:[18,75],17:[21,1],18:[23,1],19:[25,21],20:[27,56],
        21:[29,46],22:[33,31],23:[36,28],24:[39,32],25:[41,47],26:[46,1],27:[51,31],28:[58,1],29:[67,1],30:[78,1]
      };
      const [s,a] = JMAP[j]; await goto(s,a);
    });
    $("#qa-translation").addEventListener("change", async (e)=>{
      state.currentTranslation = e.target.value;
      await loadSurah(state.currentSurah);
      renderAyah();
    });
    $("#qa-reciter").addEventListener("change", (e)=>{ state.currentReciter = e.target.value; renderAyah(); });
    $("#qa-prev, #qa-prev-ayah").forEach?null:(
      document.querySelectorAll("#qa-prev,#qa-prev-ayah").forEach(btn=>btn.addEventListener("click", async ()=>{
        if(state.currentAyah>1){ await goto(state.currentSurah, state.currentAyah-1); }
        else if(state.currentSurah>1){ await goto(state.currentSurah-1, 1); }
      }))
    );
    document.querySelectorAll("#qa-next,#qa-next-ayah").forEach(btn=>btn.addEventListener("click", async ()=>{
      if(state.currentAyah < state.versesArabic.length){ await goto(state.currentSurah, state.currentAyah+1); }
      else if(state.currentSurah < state.surahs.length){ await goto(state.currentSurah+1, 1); }
    }));
    $("#qa-copy").addEventListener("click", async ()=>{
      const s = `${$("#qa-ar").textContent}\n\n${$("#qa-tr").textContent}\n(${surahTitle(state.currentSurah)}:${state.currentAyah})`;
      try{ await navigator.clipboard.writeText(s); showStatus("Disalin."); }catch(_){ showStatus("Gagal salin."); }
    });
    $("#qa-share").addEventListener("click", async ()=>{
      const url = location.href;
      try{
        await navigator.share({title: "Al-Qur’an Online", text: surahTitle(state.currentSurah)+` Ayah ${state.currentAyah}`, url});
      }catch(_){
        try{ await navigator.clipboard.writeText(url); showStatus("Pautan disalin."); }catch(_){}
      }
    });
    $("#qa-bookmark").addEventListener("click", ()=>{
      const k = CFG.storageKey;
      const v = { s: state.currentSurah, a: state.currentAyah, t: Date.now() };
      localStorage.setItem(k, JSON.stringify(v));
      showStatus("Disimpan.");
    });
    $("#qa-auto").addEventListener("change", (e)=>{ state.continuous = e.target.checked; });
    $("#qa-audio").addEventListener("ended", async ()=>{
      if(state.continuous){
        if(state.currentAyah < state.versesArabic.length){ await goto(state.currentSurah, state.currentAyah+1); $("#qa-audio").play(); }
      }
    });
    document.addEventListener("keydown", async (ev)=>{
      if(ev.target && ["INPUT","SELECT","TEXTAREA"].includes(ev.target.tagName)) return;
      if(ev.key==="ArrowLeft"){ ev.preventDefault(); document.getElementById("qa-prev-ayah").click(); }
      if(ev.key==="ArrowRight"){ ev.preventDefault(); document.getElementById("qa-next-ayah").click(); }
      if(ev.code==="Space"){ ev.preventDefault(); const a=$("#qa-audio"); a.paused?a.play():a.pause(); }
    });
    $("#qa-search").addEventListener("input", (e)=>{
      const q = e.target.value.toLowerCase().trim();
      const sSel = $("#qa-surah");
      sSel.innerHTML="";
      state.surahs
        .filter(s=>{
          const nn = (s.englishName||"").toLowerCase();
          const ar = (s.name||"").toLowerCase();
          return !q || nn.includes(q) || ar.includes(q) || (""+s.number).startsWith(q);
        })
        .forEach(s=>{
          const o=document.createElement("option");
          o.value=s.number; o.textContent=`${s.number}. ${s.englishName} (${s.name})`;
          sSel.appendChild(o);
        });
    });

    // JSON-LD inject (tool + FAQ)
    const jsonld = {
      "@context":"https://schema.org",
      "@graph":[
        {
          "@type":"WebApplication",
          "name":"Al-Qur’an Online — ilmualam.com",
          "url":location.href.split('#')[0],
          "applicationCategory":"Religion,Education",
          "operatingSystem":"All",
          "inLanguage":["ar","en","ms"],
          "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
          "featureList":[
            "Baca mengikut surah/juz",
            "Audio qari (streaming)",
            "Salin & kongsi ayat",
            "Penanda (bookmark)",
            "Pintasan papan kekunci",
            "Terjemahan boleh tukar"
          ],
          "publisher":{"@type":"Organization","name":"ilmualam.com"}
        },
        {
          "@type":"FAQPage",
          "mainEntity":[
            {"@type":"Question","name":"Adakah teks Qur’an ini sahih?","acceptedAnswer":{"@type":"Answer","text":"Teks & struktur ayat berpandukan projek Tanzil (CC BY 3.0) dan edisi AlQuran Cloud; kami tidak mengubah teks."}},
            {"@type":"Question","name":"Bolehkah saya dengar bacaan qari berbeza?","acceptedAnswer":{"@type":"Answer","text":"Ya. Pilih qari; audio distrim dari CDN Islamic Network yang pantas."}},
            {"@type":"Question","name":"Bolehkah saya kongsikan ayat tertentu?","acceptedAnswer":{"@type":"Answer","text":"Ya. Butang “Kongsi” menjana pautan dengan hash seperti #/surah/2/255."}},
            {"@type":"Question","name":"Bagaimana penanda (bookmark) berfungsi?","acceptedAnswer":{"@type":"Answer","text":"Bookmark disimpan dalam pelayar (localStorage). Padam cache untuk membuangnya."}}
          ]
        }
      ]
    };
    document.getElementById("qa-jsonld").textContent = JSON.stringify(jsonld);
  });
})();
