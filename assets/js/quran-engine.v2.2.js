/* IlmuAlam Quran Engine (Enterprise) © 2026 ilmualam.com — v2.2 SEO/UX */
(function () {
  "use strict";

  const OWNER = "ilmualam.com";
  const VERSION = "2.2";
  const ALLOW = ["ilmualam.com","www.ilmualam.com","ilmualam.blogspot.com","blogger.com","blogspot.com","draft.blogger.com","localhost"];
  const host = (location.hostname || "").toLowerCase();
  if (!ALLOW.some((d) => host === d || host.endsWith("." + d))) return;

  const ready = (fn) => document.readyState === "loading"
    ? document.addEventListener("DOMContentLoaded", fn, {once:true})
    : fn();

  ready(() => document.querySelectorAll(".ilmq[data-surah]").forEach(init));

  function init(root){
    if (!root || root.dataset.ilmqBooted === VERSION) return;
    root.dataset.ilmqBooted = VERSION;

    const surah = Number.parseInt(root.getAttribute("data-surah"),10);
    if (!Number.isInteger(surah) || surah < 1 || surah > 114) return;

    const $ = (q) => root.querySelector(q);
    const $$ = (q) => Array.from(root.querySelectorAll(q));
    const clean = (v) => String(v ?? "").trim();

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

    let verses = [], idx = 0, isReady = false, userPaused = true;

    ensureToolbar(root);
    const tabs = $$(".tab[data-tab]");
    const modeBtn = $('[data-action="mode"]');
    const copyChip = $('[data-action="copy"]');
    const shareChip = $('[data-action="share"]');
    const bmChip = $('[data-action="bookmark"]');
    const resumeChip = $('[data-action="resume"]');
    const printChip = $('[data-action="print"]');

    const storeKey = `ilmq_${surah}`;
    const store = {
      get(k,d){ try{ const v=JSON.parse(localStorage.getItem(`${storeKey}:${k}`)); return v==null?d:v; }catch{return d;} },
      set(k,v){ try{ localStorage.setItem(`${storeKey}:${k}`,JSON.stringify(v)); }catch{} }
    };

    let tab = store.get("tab","all");
    const prefersReducedMotion = () => window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches === true;

    function pageBaseUrl(){ const u=new URL(location.href); u.hash=""; return u.toString(); }
    function ayahUrl(i){ return `${pageBaseUrl()}#ayat-${i+1}`; }
    function surahTitle(){ return clean(root.querySelector(".hdr h2, h1, h2")?.textContent) || `Surah ${surah}`; }

    function toast(message){
      if(!toastEl) return;
      toastEl.textContent=message;
      toastEl.classList.add("on");
      clearTimeout(toastEl._t);
      toastEl._t=setTimeout(()=>toastEl.classList.remove("on"),1500);
    }

    function formatTime(seconds){
      if(!Number.isFinite(seconds)||seconds<0) return "0:00";
      const m=Math.floor(seconds/60), s=Math.floor(seconds%60);
      return `${m}:${String(s).padStart(2,"0")}`;
    }

    function escapeHTML(v){
      return String(v??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");
    }

    function applyMode(mode){
      store.set("mode",mode);
      if(mode==="auto") root.removeAttribute("data-mode"); else root.setAttribute("data-mode",mode);
      if(modeBtn){
        modeBtn.textContent=mode==="dark"?"🌙":mode==="light"?"☀️":"🌓";
        modeBtn.setAttribute("aria-label",`Tema: ${mode}`);
        modeBtn.title=`Tema: ${mode}`;
      }
    }
    applyMode(store.get("mode","auto"));

    const fzA=Number(store.get("fzA",30))||30, fzT=Number(store.get("fzT",16))||16;
    root.style.setProperty("--fzA",`${fzA}px`);
    root.style.setProperty("--fzT",`${fzT}px`);

    const arabicRange=$('[data-bind="arabicSize"]');
    const transRange=$('[data-bind="translationSize"]');
    const autoScrollChk=$('[data-bind="autoScroll"]');
    const autoNextChk=$('[data-bind="autoNext"]');
    if(arabicRange) arabicRange.value=String(fzA);
    if(transRange) transRange.value=String(fzT);
    if(autoScrollChk) autoScrollChk.checked=store.get("autoScroll",true);
    if(autoNextChk) autoNextChk.checked=store.get("autoNext",true);

    if(qariSel){
      const shortNames={
        "Mishary Rashid Alafasy":"M. R. Alafasy",
        "Abdul Rahman Al-Sudais":"A. R. Sudais",
        "Mahmoud Khalil Al-Husary":"M. K. Husary",
        "Abdul Basit":"Abdul Basit",
        "Saad Al-Ghamadi":"S. Al-Ghamadi"
      };
      Array.from(qariSel.options).forEach(opt=>{ const t=clean(opt.textContent); if(shortNames[t]) opt.textContent=shortNames[t]; });
    }

    function setPlayUI(playing){
      if(!playBtn) return;
      playBtn.setAttribute("aria-pressed",playing?"true":"false");
      playBtn.textContent=playing?"⏸":"▶";
      playBtn.setAttribute("aria-label",playing?"Jeda bacaan":"Mainkan bacaan");
    }

    function markPlaying(index,{scroll=false,updateHash=false}={}){
      if(!versesEl) return;
      versesEl.querySelectorAll(".v.playing").forEach(n=>n.classList.remove("playing"));
      const card=versesEl.querySelector(`.v[data-i="${index}"]`);
      if(!card) return;
      card.classList.add("playing");
      if(updateHash){ const target=`#ayat-${index+1}`; if(location.hash!==target) history.replaceState(null,"",target); }
      const shouldScroll=scroll&&(autoScrollChk?autoScrollChk.checked:store.get("autoScroll",true));
      if(shouldScroll) card.scrollIntoView({behavior:prefersReducedMotion()?"auto":"smooth",block:"center"});
    }

    function formatCopy(index){
      const v=verses[index]; if(!v) return "";
      return [
        `${surahTitle()} — Ayat ${index+1}`,
        v.arabic,
        v.rumi?`Rumi: ${v.rumi}`:"",
        v.ms?`Maksud: ${v.ms}`:"",
        ayahUrl(index),
        `— ${OWNER}`
      ].filter(Boolean).join("\n");
    }

    async function copyText(text,success="Disalin"){
      if(!text) return;
      try{ await navigator.clipboard.writeText(text); toast(`${success} ✓`); }
      catch{
        const ta=document.createElement("textarea");
        ta.value=text; ta.setAttribute("readonly",""); ta.style.position="fixed"; ta.style.left="-9999px";
        document.body.appendChild(ta); ta.select();
        try{ document.execCommand("copy"); toast(`${success} ✓`); }catch{ toast("Gagal menyalin."); }
        ta.remove();
      }
    }

    async function shareAyah(index){
      const v=verses[index]; if(!v) return;
      const data={title:`${surahTitle()} Ayat ${index+1}`,text:`${surahTitle()} ayat ${index+1} — ${v.ms||v.rumi||""}`.trim(),url:ayahUrl(index)};
      try{ if(navigator.share){ await navigator.share(data); return; } }
      catch(err){ if(err?.name==="AbortError") return; }
      await copyText(data.url,"Pautan ayat disalin");
    }

    function getBookmarks(){ return store.get("bm",[]); }
    function toggleBookmark(index){
      const set=new Set(getBookmarks());
      set.has(index)?set.delete(index):set.add(index);
      store.set("bm",Array.from(set).sort((a,b)=>a-b));
      paintBookmarks(); toast(set.has(index)?"Bookmark ★":"Bookmark dibuang");
    }
    function paintBookmarks(){
      if(!versesEl) return;
      const set=new Set(getBookmarks());
      versesEl.querySelectorAll(".v").forEach(card=>{
        const i=Number.parseInt(card.dataset.i,10), star=card.querySelector('[data-act="bm"]');
        if(!star) return;
        const on=set.has(i); star.textContent=on?"★":"☆"; star.classList.toggle("on",on);
        star.setAttribute("aria-pressed",on?"true":"false");
        star.setAttribute("aria-label",on?`Buang bookmark ayat ${i+1}`:`Bookmark ayat ${i+1}`);
      });
    }

    function applyTab(){
      store.set("tab",tab);
      tabs.forEach(b=>{ const active=b.dataset.tab===tab; b.classList.toggle("active",active); b.setAttribute("aria-selected",active?"true":"false"); });
      if(!versesEl) return;
      versesEl.querySelectorAll(".v").forEach(card=>{
        const a=card.querySelector(".arab"),r=card.querySelector(".rumi"),m=card.querySelector(".mal");
        if(a) a.classList.toggle("hide",!(tab==="all"||tab==="arab"));
        if(r) r.classList.toggle("hide",!(tab==="all"||tab==="rumi"));
        if(m) m.classList.toggle("hide",!(tab==="all"||tab==="ms"));
      });
    }

    function currentAyahText(){
      const v=verses[idx]; if(!v) return "";
      const out=[];
      if(tab==="all"||tab==="arab") out.push(v.arabic);
      if((tab==="all"||tab==="rumi")&&v.rumi) out.push(`Rumi: ${v.rumi}`);
      if((tab==="all"||tab==="ms")&&v.ms) out.push(`Maksud: ${v.ms}`);
      out.push(ayahUrl(idx)); return out.join("\n");
    }

    function requestedHashIndex(){
      const m=/^#ayat-(\d{1,3})$/i.exec(location.hash||"");
      if(!m) return null;
      const n=Number.parseInt(m[1],10);
      return Number.isInteger(n)&&n>=1?n-1:null;
    }

    async function loadAyah(index,autoplay=false,options={}){
      if(!verses.length) return;
      idx=Math.max(0,Math.min(verses.length-1,index));
      if(verseLabel) verseLabel.textContent=`Ayat ${idx+1}`;
      markPlaying(idx,{scroll:options.scroll??autoplay,updateHash:options.updateHash??autoplay});
      store.set("resume",{idx,t:Date.now()});
      if(!audio) return;

      const qari=qariSel?.value||"Alafasy_128kbps";
      const audioUrl=`https://everyayah.com/data/${encodeURIComponent(qari)}/${String(surah).padStart(3,"0")}${String(idx+1).padStart(3,"0")}.mp3`;
      if(audio.src!==audioUrl){ audio.src=audioUrl; audio.load(); }
      if(!autoplay){ userPaused=true; setPlayUI(false); return; }
      try{ await audio.play(); userPaused=false; setPlayUI(true); }
      catch{ userPaused=true; setPlayUI(false); toast("Tekan ▶ untuk mula."); }
    }

    async function togglePlay(){
      if(!isReady||!audio) return;
      if(!audio.src){ await loadAyah(idx,true,{scroll:true,updateHash:true}); return; }
      if(audio.paused){
        try{ await audio.play(); userPaused=false; setPlayUI(true); markPlaying(idx,{scroll:true,updateHash:true}); }
        catch{ toast("Tekan ▶ untuk mula."); }
      }else{ audio.pause(); userPaused=true; setPlayUI(false); }
    }

    function renderVerses(){
      if(!versesEl) return;
      const frag=document.createDocumentFragment();
      verses.forEach((v,i)=>{
        const n=i+1, card=document.createElement("article");
        card.className="v"; card.dataset.i=String(i); card.dataset.ayah=String(n); card.id=`ayat-${n}`;
        card.setAttribute("aria-labelledby",`ayat-label-${surah}-${n}`);
        card.innerHTML=`
          <div class="top">
            <a class="no" id="ayat-label-${surah}-${n}" href="#ayat-${n}" aria-label="${escapeHTML(surahTitle())} ayat ${n}">${surah}:${n}</a>
            <div class="va" role="group" aria-label="Tindakan ayat ${n}">
              <button class="vbtn p" type="button" data-act="play" aria-label="Main ayat ${n}">▶</button>
              <button class="vbtn" type="button" data-act="copy" aria-label="Salin ayat ${n}">Salin</button>
              <button class="vbtn" type="button" data-act="share" aria-label="Kongsi ayat ${n}">Kongsi</button>
              <button class="vbtn star" type="button" data-act="bm" aria-label="Bookmark ayat ${n}" aria-pressed="false">☆</button>
            </div>
          </div>
          <div class="arab" lang="ar" dir="rtl">${escapeHTML(v.arabic)}</div>
          ${v.rumi?`<p class="rumi" lang="ms-Latn">${escapeHTML(v.rumi)}</p>`:""}
          ${v.ms?`<p class="mal" lang="ms">${escapeHTML(v.ms)}</p>`:""}
        `;
        card.addEventListener("click",e=>{ if(e.target.closest("button,a")) return; loadAyah(i,true,{scroll:false,updateHash:true}); });
        card.querySelector('[data-act="play"]')?.addEventListener("click",e=>{ e.stopPropagation(); if(idx!==i||audio?.paused) loadAyah(i,true,{scroll:true,updateHash:true}); else togglePlay(); });
        card.querySelector('[data-act="copy"]')?.addEventListener("click",e=>{ e.stopPropagation(); copyText(formatCopy(i),"Ayat disalin"); });
        card.querySelector('[data-act="share"]')?.addEventListener("click",e=>{ e.stopPropagation(); shareAyah(i); });
        card.querySelector('[data-act="bm"]')?.addEventListener("click",e=>{ e.stopPropagation(); toggleBookmark(i); });
        frag.appendChild(card);
      });
      versesEl.replaceChildren(frag); applyTab(); paintBookmarks();
      const hashIndex=requestedHashIndex();
      if(hashIndex!==null&&hashIndex<verses.length){
        idx=hashIndex; markPlaying(idx);
        requestAnimationFrame(()=>document.getElementById(`ayat-${idx+1}`)?.scrollIntoView({behavior:prefersReducedMotion()?"auto":"smooth",block:"start"}));
      }else markPlaying(idx);
    }

    async function loadSurah(){
      if(!versesEl) return;
      root.setAttribute("aria-busy","true");
      const jsonUrl=`https://cdn.jsdelivr.net/gh/ilmualam/quran@main/data-surah/surah-${surah}.json`;
      try{
        const response=await fetch(jsonUrl,{cache:"force-cache",credentials:"omit",mode:"cors"});
        if(!response.ok) throw new Error(`HTTP ${response.status}`);
        const data=await response.json();
        if(!Array.isArray(data)||!data.length) throw new Error("Data surah kosong");
        verses=data.map(x=>({arabic:clean(x.arabic),rumi:clean(x.rumi),ms:clean(x.translation||x.ms),audio:clean(x.audio)}));
        if(ayahCountBind) ayahCountBind.textContent=String(verses.length);
        const resume=store.get("resume",null), hashIndex=requestedHashIndex();
        const resumeIndex=Number.isInteger(resume?.idx)?resume.idx:0;
        idx=hashIndex!==null?Math.min(hashIndex,verses.length-1):Math.max(0,Math.min(resumeIndex,verses.length-1));
        isReady=true; renderVerses(); await loadAyah(idx,false,{scroll:false,updateHash:false});
        root.dataset.seoRendered="true"; root.removeAttribute("aria-busy");
        root.dispatchEvent(new CustomEvent("ilmq:ready",{bubbles:true,detail:{surah,ayahCount:verses.length,version:VERSION}}));
      }catch(err){
        root.removeAttribute("aria-busy");
        versesEl.innerHTML='<div class="loading" role="alert">Ralat memuat data surah. Sila cuba semula.</div>';
        toast("Gagal memuatkan data surah."); console.error("[IlmuAlam Quran v2.2]",err);
      }
    }

    playBtn?.addEventListener("click",togglePlay);
    qariSel?.addEventListener("change",async()=>{ if(!isReady) return; const wasPlaying=audio&&!audio.paused; await loadAyah(idx,Boolean(wasPlaying),{scroll:false,updateHash:false}); toast("Qari ditukar."); });

    if(audio){
      audio.addEventListener("timeupdate",()=>{ if(!audio.duration) return; const pct=(audio.currentTime/audio.duration)*100; if(barFill) barFill.style.width=`${pct.toFixed(2)}%`; if(timeLabel) timeLabel.textContent=`${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`; });
      audio.addEventListener("play",()=>{ userPaused=false; setPlayUI(true); markPlaying(idx,{updateHash:true}); });
      audio.addEventListener("pause",()=>{ if(userPaused||audio.ended) setPlayUI(false); });
      audio.addEventListener("ended",async()=>{ setPlayUI(false); const nextOn=autoNextChk?autoNextChk.checked:store.get("autoNext",true); if(nextOn&&idx+1<verses.length) await loadAyah(idx+1,true,{scroll:true,updateHash:true}); else userPaused=true; });
    }

    barWrap?.addEventListener("click",e=>{ if(!audio?.duration) return; const rect=barWrap.getBoundingClientRect(),x=Math.max(0,Math.min(rect.width,e.clientX-rect.left)); audio.currentTime=(x/rect.width)*audio.duration; });
    arabicRange?.addEventListener("input",()=>{ root.style.setProperty("--fzA",`${arabicRange.value}px`); store.set("fzA",Number(arabicRange.value)); });
    transRange?.addEventListener("input",()=>{ root.style.setProperty("--fzT",`${transRange.value}px`); store.set("fzT",Number(transRange.value)); });
    autoScrollChk?.addEventListener("change",()=>store.set("autoScroll",autoScrollChk.checked));
    autoNextChk?.addEventListener("change",()=>store.set("autoNext",autoNextChk.checked));
    tabs.forEach(button=>button.addEventListener("click",()=>{ tab=button.dataset.tab||"all"; applyTab(); }));
    modeBtn?.addEventListener("click",()=>{ const current=store.get("mode","auto"),next=current==="auto"?"light":current==="light"?"dark":"auto"; applyMode(next); });
    copyChip?.addEventListener("click",()=>copyText(currentAyahText(),"Ayat disalin"));
    shareChip?.addEventListener("click",()=>shareAyah(idx));
    bmChip?.addEventListener("click",()=>toggleBookmark(idx));
    resumeChip?.addEventListener("click",()=>{ const resume=store.get("resume",null),target=Number.isInteger(resume?.idx)?resume.idx:0; loadAyah(target,false,{scroll:false,updateHash:true}); requestAnimationFrame(()=>document.getElementById(`ayat-${target+1}`)?.scrollIntoView({behavior:prefersReducedMotion()?"auto":"smooth",block:"center"})); });
    printChip?.addEventListener("click",()=>{ const old=document.title; document.title=`${surahTitle()} - Arab Rumi Terjemahan | ${OWNER}`; root.classList.add("print-target"); window.print(); setTimeout(()=>{root.classList.remove("print-target");document.title=old;},400); });
    window.addEventListener("hashchange",()=>{ if(!isReady) return; const hashIndex=requestedHashIndex(); if(hashIndex===null||hashIndex>=verses.length) return; idx=hashIndex; markPlaying(idx); document.getElementById(`ayat-${idx+1}`)?.scrollIntoView({behavior:prefersReducedMotion()?"auto":"smooth",block:"start"}); });

    loadSurah();
  }

  function ensureToolbar(root){
    if(root.querySelector(".tools")) return;
    const anchor=root.querySelector(".player")||root.querySelector('[data-bind="audio"]')?.parentElement||root.querySelector(".set")||root.querySelector('[data-bind="verses"]');
    if(!anchor?.parentNode) return;
    const tools=document.createElement("nav");
    tools.className="tools"; tools.setAttribute("aria-label","Kawalan paparan Al-Quran");
    tools.innerHTML=`
      <div class="tabs" role="tablist" aria-label="Paparan teks">
        <button class="tab" type="button" role="tab" data-tab="all" aria-selected="true">Semua</button>
        <button class="tab" type="button" role="tab" data-tab="arab" aria-selected="false">Arab</button>
        <button class="tab" type="button" role="tab" data-tab="rumi" aria-selected="false">Rumi</button>
        <button class="tab" type="button" role="tab" data-tab="ms" aria-selected="false">Melayu</button>
      </div>
      <div class="act" role="group" aria-label="Tindakan">
        <button class="chip" type="button" data-action="copy">Salin</button>
        <button class="chip" type="button" data-action="share">Kongsi</button>
        <button class="chip" type="button" data-action="bookmark" aria-label="Bookmark ayat semasa">★</button>
        <button class="chip" type="button" data-action="resume">Sambung</button>
        <button class="chip" type="button" data-action="print">PDF</button>
        <button class="chip mode" type="button" data-action="mode" aria-label="Tema">🌓</button>
      </div>`;
    anchor.parentNode.insertBefore(tools,anchor.nextSibling);
  }
})();
