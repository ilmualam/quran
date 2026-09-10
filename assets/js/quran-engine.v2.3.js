/* IlmuAlam Quran Engine © 2026 ilmualam.com — v2.3 CWV/INP optimized, legacy HTML compatible */
(()=>{"use strict";
const OWNER="ilmualam.com",VERSION="2.3";
const ALLOW=["ilmualam.com","www.ilmualam.com","ilmualam.blogspot.com","blogger.com","blogspot.com","draft.blogger.com","localhost"];
const host=(location.hostname||"").toLowerCase();
if(!ALLOW.some(d=>host===d||host.endsWith("."+d)))return;

const onReady=fn=>document.readyState==="loading"
?document.addEventListener("DOMContentLoaded",fn,{once:true})
:fn();

onReady(()=>document.querySelectorAll(".ilmq[data-surah]").forEach(init));

function init(root){
  if(!root||root.dataset.ilmqBooted===VERSION)return;
  const surah=parseInt(root.dataset.surah,10);
  if(!Number.isInteger(surah)||surah<1||surah>114)return;
  root.dataset.ilmqBooted=VERSION;

  const $=q=>root.querySelector(q), $$=q=>[...root.querySelectorAll(q)];
  const clean=v=>String(v??"").trim();
  const reduced=matchMedia?.("(prefers-reduced-motion: reduce)")?.matches===true;

  const versesEl=$('[data-bind="verses"]');
  const audio=$('[data-bind="audio"]');
  const playBtn=$('[data-action="playpause"]');
  const barWrap=$('[data-action="seek"]');
  const barFill=barWrap?.querySelector("i")||null;
  const verseLabel=$('[data-bind="currentVerse"]');
  const timeLabel=$('[data-bind="time"]');
  const qariSel=$('[data-bind="qari"]');
  const toastEl=$('[data-bind="toast"]');
  const ayahCountBind=$('[data-bind="ayahCount"]');

  ensureToolbar(root);

  const tabs=$$(".tab[data-tab]");
  const modeBtn=$('[data-action="mode"]');
  const copyChip=$('[data-action="copy"]');
  const shareChip=$('[data-action="share"]');
  const bmChip=$('[data-action="bookmark"]');
  const resumeChip=$('[data-action="resume"]');
  const printChip=$('[data-action="print"]');
  const arabicRange=$('[data-bind="arabicSize"]');
  const transRange=$('[data-bind="translationSize"]');
  const autoScrollChk=$('[data-bind="autoScroll"]');
  const autoNextChk=$('[data-bind="autoNext"]');

  const storeKey=`ilmq_${surah}`;
  const store={
    get(k,d){try{const v=JSON.parse(localStorage.getItem(`${storeKey}:${k}`));return v==null?d:v}catch{return d}},
    set(k,v){try{localStorage.setItem(`${storeKey}:${k}`,JSON.stringify(v))}catch{}}
  };

  let verses=[],idx=0,isReady=false,userPaused=true,tab=store.get("tab","all");
  let activeCard=null,progressRAF=0,lastTimeSecond=-1;

  const pageBaseUrl=()=>{const u=new URL(location.href);u.hash="";return u.toString()};
  const ayahUrl=i=>`${pageBaseUrl()}#ayat-${i+1}`;
  const surahTitle=()=>clean(root.querySelector(".hdr h2,h1,h2")?.textContent)||`Surah ${surah}`;
  const ayahNode=i=>root.querySelector(`#ayat-${i+1}`);

  function toast(message){
    if(!toastEl)return;
    toastEl.textContent=message;
    toastEl.classList.add("on");
    clearTimeout(toastEl._t);
    toastEl._t=setTimeout(()=>toastEl.classList.remove("on"),1500);
  }

  function formatTime(s){
    if(!Number.isFinite(s)||s<0)return"0:00";
    return`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,"0")}`;
  }

  function escapeHTML(v){
    return String(v??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");
  }

  function applyMode(mode){
    if(mode==="auto")root.removeAttribute("data-mode");else root.dataset.mode=mode;
    if(modeBtn){
      modeBtn.textContent=mode==="dark"?"🌙":mode==="light"?"☀️":"🌓";
      modeBtn.setAttribute("aria-label",`Tema: ${mode}`);
      modeBtn.title=`Tema: ${mode}`;
    }
  }

  const fzA=Number(store.get("fzA",30))||30,fzT=Number(store.get("fzT",16))||16;
  root.style.setProperty("--fzA",`${fzA}px`);
  root.style.setProperty("--fzT",`${fzT}px`);
  if(arabicRange)arabicRange.value=String(fzA);
  if(transRange)transRange.value=String(fzT);
  if(autoScrollChk)autoScrollChk.checked=store.get("autoScroll",true);
  if(autoNextChk)autoNextChk.checked=store.get("autoNext",true);
  applyMode(store.get("mode","auto"));

  if(qariSel){
    const names={
      "Mishary Rashid Alafasy":"M. R. Alafasy",
      "Abdul Rahman Al-Sudais":"A. R. Sudais",
      "Mahmoud Khalil Al-Husary":"M. K. Husary",
      "Abdul Basit":"Abdul Basit",
      "Saad Al-Ghamadi":"S. Al-Ghamadi"
    };
    for(const opt of qariSel.options){const t=clean(opt.textContent);if(names[t])opt.textContent=names[t]}
  }

  function setPlayUI(playing){
    if(!playBtn)return;
    playBtn.setAttribute("aria-pressed",playing?"true":"false");
    playBtn.textContent=playing?"⏸":"▶";
    playBtn.setAttribute("aria-label",playing?"Jeda bacaan":"Mainkan bacaan");
  }

  function markPlaying(index,{scroll=false,updateHash=false}={}){
    const card=versesEl?.querySelector(`.v[data-i="${index}"]`);
    if(!card)return;
    if(activeCard!==card){
      activeCard?.classList.remove("playing");
      card.classList.add("playing");
      activeCard=card;
    }
    if(updateHash){
      const target=`#ayat-${index+1}`;
      if(location.hash!==target)history.replaceState(null,"",target);
    }
    if(scroll&&(autoScrollChk?autoScrollChk.checked:store.get("autoScroll",true))){
      card.scrollIntoView({behavior:reduced?"auto":"smooth",block:"center"});
    }
  }

  function formatCopy(index){
    const v=verses[index];if(!v)return"";
    return[
      `${surahTitle()} — Ayat ${index+1}`,v.arabic,
      v.rumi?`Rumi: ${v.rumi}`:"",
      v.ms?`Maksud: ${v.ms}`:"",
      ayahUrl(index),`— ${OWNER}`
    ].filter(Boolean).join("\n");
  }

  async function copyText(text,success="Disalin"){
    if(!text)return;
    try{await navigator.clipboard.writeText(text);toast(`${success} ✓`)}
    catch{
      const ta=document.createElement("textarea");
      ta.value=text;ta.readOnly=true;ta.style.cssText="position:fixed;left:-9999px;top:0";
      document.body.appendChild(ta);ta.select();
      try{document.execCommand("copy");toast(`${success} ✓`)}catch{toast("Gagal menyalin.")}
      ta.remove();
    }
  }

  async function shareAyah(index){
    const v=verses[index];if(!v)return;
    const data={title:`${surahTitle()} Ayat ${index+1}`,text:`${surahTitle()} ayat ${index+1} — ${v.ms||v.rumi||""}`.trim(),url:ayahUrl(index)};
    try{if(navigator.share){await navigator.share(data);return}}catch(e){if(e?.name==="AbortError")return}
    await copyText(data.url,"Pautan ayat disalin");
  }

  const getBookmarks=()=>store.get("bm",[]);
  function toggleBookmark(index){
    const set=new Set(getBookmarks());
    set.has(index)?set.delete(index):set.add(index);
    store.set("bm",[...set].sort((a,b)=>a-b));
    paintBookmarks();
    toast(set.has(index)?"Bookmark ★":"Bookmark dibuang");
  }

  function paintBookmarks(){
    if(!versesEl)return;
    const set=new Set(getBookmarks());
    for(const card of versesEl.querySelectorAll(".v")){
      const i=parseInt(card.dataset.i,10),star=card.querySelector('[data-act="bm"]');
      if(!star)continue;
      const on=set.has(i);
      star.textContent=on?"★":"☆";star.classList.toggle("on",on);
      star.setAttribute("aria-pressed",on?"true":"false");
      star.setAttribute("aria-label",on?`Buang bookmark ayat ${i+1}`:`Bookmark ayat ${i+1}`);
    }
  }

  function applyTab(){
    for(const b of tabs){
      const on=b.dataset.tab===tab;
      b.classList.toggle("active",on);b.setAttribute("aria-selected",on?"true":"false");
    }
    if(!versesEl)return;
    for(const card of versesEl.querySelectorAll(".v")){
      card.querySelector(".arab")?.classList.toggle("hide",!(tab==="all"||tab==="arab"));
      card.querySelector(".rumi")?.classList.toggle("hide",!(tab==="all"||tab==="rumi"));
      card.querySelector(".mal")?.classList.toggle("hide",!(tab==="all"||tab==="ms"));
    }
  }

  function currentAyahText(){
    const v=verses[idx];if(!v)return"";
    const out=[];
    if(tab==="all"||tab==="arab")out.push(v.arabic);
    if((tab==="all"||tab==="rumi")&&v.rumi)out.push(`Rumi: ${v.rumi}`);
    if((tab==="all"||tab==="ms")&&v.ms)out.push(`Maksud: ${v.ms}`);
    out.push(ayahUrl(idx));return out.join("\n");
  }

  function requestedHashIndex(){
    const m=/^#ayat-(\d{1,3})$/i.exec(location.hash||"");
    if(!m)return null;
    const n=parseInt(m[1],10);
    return Number.isInteger(n)&&n>=1?n-1:null;
  }

  async function loadAyah(index,autoplay=false,options={}){
    if(!verses.length)return;
    idx=Math.max(0,Math.min(verses.length-1,index));
    if(verseLabel)verseLabel.textContent=`Ayat ${idx+1}`;
    markPlaying(idx,{scroll:options.scroll??autoplay,updateHash:options.updateHash??autoplay});
    store.set("resume",{idx,t:Date.now()});
    if(!audio)return;

    const qari=qariSel?.value||"Alafasy_128kbps";
    const audioUrl=`https://everyayah.com/data/${encodeURIComponent(qari)}/${String(surah).padStart(3,"0")}${String(idx+1).padStart(3,"0")}.mp3`;
    if(audio.src!==audioUrl){audio.src=audioUrl;audio.load()}
    if(!autoplay){userPaused=true;setPlayUI(false);return}
    try{await audio.play();userPaused=false;setPlayUI(true)}
    catch{userPaused=true;setPlayUI(false);toast("Tekan ▶ untuk mula.")}
  }

  async function togglePlay(){
    if(!isReady||!audio)return;
    if(!audio.src){await loadAyah(idx,true,{scroll:true,updateHash:true});return}
    if(audio.paused){
      try{await audio.play();userPaused=false;setPlayUI(true);markPlaying(idx,{scroll:true,updateHash:true})}
      catch{toast("Tekan ▶ untuk mula.")}
    }else{audio.pause();userPaused=true;setPlayUI(false)}
  }

  function renderVerses(){
    if(!versesEl)return;
    const frag=document.createDocumentFragment(),title=surahTitle();
    for(let i=0;i<verses.length;i++){
      const v=verses[i],n=i+1,card=document.createElement("article");
      card.className="v";card.dataset.i=String(i);card.dataset.ayah=String(n);card.id=`ayat-${n}`;
      card.setAttribute("aria-labelledby",`ayat-label-${surah}-${n}`);
      card.innerHTML=`<div class="top"><a class="no" id="ayat-label-${surah}-${n}" href="#ayat-${n}" aria-label="${escapeHTML(title)} ayat ${n}">${surah}:${n}</a><div class="va" role="group" aria-label="Tindakan ayat ${n}"><button class="vbtn p" type="button" data-act="play" aria-label="Main ayat ${n}">▶</button><button class="vbtn" type="button" data-act="copy" aria-label="Salin ayat ${n}">Copy</button><button class="vbtn" type="button" data-act="share" aria-label="Kongsi ayat ${n}">Share</button><button class="vbtn star" type="button" data-act="bm" aria-label="Bookmark ayat ${n}" aria-pressed="false">☆</button></div></div><div class="arab" lang="ar" dir="rtl">${escapeHTML(v.arabic)}</div>${v.rumi?`<p class="rumi" lang="ms-Latn">${escapeHTML(v.rumi)}</p>`:""}${v.ms?`<p class="mal" lang="ms">${escapeHTML(v.ms)}</p>`:""}`;
      frag.appendChild(card);
    }
    versesEl.replaceChildren(frag);
    activeCard=null;applyTab();paintBookmarks();
    const h=requestedHashIndex();
    if(h!==null&&h<verses.length){
      idx=h;markPlaying(idx);
      requestAnimationFrame(()=>ayahNode(idx)?.scrollIntoView({behavior:reduced?"auto":"smooth",block:"start"}));
    }else markPlaying(idx);
  }

  /* One listener for every verse/card action: keeps long surahs cheap. */
  versesEl?.addEventListener("click",e=>{
    const card=e.target.closest(".v[data-i]");
    if(!card||!versesEl.contains(card))return;
    const i=parseInt(card.dataset.i,10);if(!Number.isInteger(i))return;
    const action=e.target.closest("[data-act]")?.dataset.act;
    if(!action){
      if(!e.target.closest("a"))loadAyah(i,true,{scroll:false,updateHash:true});
      return;
    }
    e.preventDefault();e.stopPropagation();
    if(action==="play"){if(idx!==i||audio?.paused)loadAyah(i,true,{scroll:true,updateHash:true});else togglePlay()}
    else if(action==="copy")copyText(formatCopy(i),"Ayat disalin");
    else if(action==="share")shareAyah(i);
    else if(action==="bm")toggleBookmark(i);
  });

  async function loadSurah(){
    if(!versesEl)return;
    root.setAttribute("aria-busy","true");
    try{
      const url=`https://cdn.jsdelivr.net/gh/ilmualam/quran@main/data-surah/surah-${surah}.json`;
      const res=await fetch(url,{cache:"force-cache",credentials:"omit",mode:"cors"});
      if(!res.ok)throw Error(`HTTP ${res.status}`);
      const data=await res.json();
      if(!Array.isArray(data)||!data.length)throw Error("Data surah kosong");
      verses=data.map(x=>({arabic:clean(x.arabic),rumi:clean(x.rumi),ms:clean(x.translation||x.ms)}));
      if(ayahCountBind)ayahCountBind.textContent=String(verses.length);
      const resume=store.get("resume",null),h=requestedHashIndex(),ri=Number.isInteger(resume?.idx)?resume.idx:0;
      idx=h!==null?Math.min(h,verses.length-1):Math.max(0,Math.min(ri,verses.length-1));
      isReady=true;renderVerses();await loadAyah(idx,false,{scroll:false,updateHash:false});
      root.dataset.seoRendered="true";
      root.dispatchEvent(new CustomEvent("ilmq:ready",{bubbles:true,detail:{surah,ayahCount:verses.length,version:VERSION}}));
    }catch(err){
      versesEl.innerHTML='<div class="loading" role="alert">Ralat memuat data surah. Sila cuba semula.</div>';
      toast("Gagal memuatkan data surah.");
      console.error("[IlmuAlam Quran v2.3]",err);
    }finally{root.removeAttribute("aria-busy")}
  }

  playBtn?.addEventListener("click",togglePlay,{passive:true});
  qariSel?.addEventListener("change",async()=>{if(!isReady)return;const was=audio&&!audio.paused;await loadAyah(idx,!!was,{scroll:false,updateHash:false});toast("Qari ditukar.")});

  function paintProgress(){
    progressRAF=0;
    if(!audio?.duration)return;
    const pct=(audio.currentTime/audio.duration)*100;
    if(barFill)barFill.style.transform=`scaleX(${Math.max(0,Math.min(1,pct/100))})`;
    const sec=Math.floor(audio.currentTime);
    if(timeLabel&&sec!==lastTimeSecond){
      lastTimeSecond=sec;
      timeLabel.textContent=`${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
    }
  }

  if(audio){
    audio.addEventListener("timeupdate",()=>{if(!progressRAF)progressRAF=requestAnimationFrame(paintProgress)},{passive:true});
    audio.addEventListener("play",()=>{userPaused=false;setPlayUI(true);markPlaying(idx,{updateHash:true})},{passive:true});
    audio.addEventListener("pause",()=>{if(userPaused||audio.ended)setPlayUI(false)},{passive:true});
    audio.addEventListener("ended",async()=>{setPlayUI(false);const next=autoNextChk?autoNextChk.checked:store.get("autoNext",true);if(next&&idx+1<verses.length)await loadAyah(idx+1,true,{scroll:true,updateHash:true});else userPaused=true});
  }

  barWrap?.addEventListener("click",e=>{
    if(!audio?.duration)return;
    const r=barWrap.getBoundingClientRect();
    audio.currentTime=(Math.max(0,Math.min(r.width,e.clientX-r.left))/r.width)*audio.duration;
  });

  arabicRange?.addEventListener("input",()=>root.style.setProperty("--fzA",`${arabicRange.value}px`),{passive:true});
  transRange?.addEventListener("input",()=>root.style.setProperty("--fzT",`${transRange.value}px`),{passive:true});
  arabicRange?.addEventListener("change",()=>store.set("fzA",Number(arabicRange.value)));
  transRange?.addEventListener("change",()=>store.set("fzT",Number(transRange.value)));
  autoScrollChk?.addEventListener("change",()=>store.set("autoScroll",autoScrollChk.checked));
  autoNextChk?.addEventListener("change",()=>store.set("autoNext",autoNextChk.checked));
  tabs.forEach(b=>b.addEventListener("click",()=>{tab=b.dataset.tab||"all";store.set("tab",tab);applyTab()}));
  modeBtn?.addEventListener("click",()=>{const cur=store.get("mode","auto"),next=cur==="auto"?"light":cur==="light"?"dark":"auto";store.set("mode",next);applyMode(next)});
  copyChip?.addEventListener("click",()=>copyText(currentAyahText(),"Ayat disalin"));
  shareChip?.addEventListener("click",()=>shareAyah(idx));
  bmChip?.addEventListener("click",()=>toggleBookmark(idx));
  resumeChip?.addEventListener("click",()=>{const r=store.get("resume",null),target=Number.isInteger(r?.idx)?r.idx:0;loadAyah(target,false,{scroll:false,updateHash:true});requestAnimationFrame(()=>ayahNode(target)?.scrollIntoView({behavior:reduced?"auto":"smooth",block:"center"}))});
  printChip?.addEventListener("click",()=>{const old=document.title;document.title=`${surahTitle()} - Arab Rumi Terjemahan | ${OWNER}`;root.classList.add("print-target");print();setTimeout(()=>{root.classList.remove("print-target");document.title=old},400)});

  addEventListener("hashchange",()=>{
    if(!isReady)return;
    const h=requestedHashIndex();if(h===null||h>=verses.length)return;
    idx=h;markPlaying(idx);ayahNode(idx)?.scrollIntoView({behavior:reduced?"auto":"smooth",block:"start"});
  },{passive:true});

  loadSurah();
}

function ensureToolbar(root){
  if(root.querySelector(".tools"))return;
  const anchor=root.querySelector(".player")||root.querySelector('[data-bind="audio"]')?.parentElement||root.querySelector(".set")||root.querySelector('[data-bind="verses"]');
  if(!anchor?.parentNode)return;
  const tools=document.createElement("nav");
  tools.className="tools";
  tools.dataset.ilmqTools="";
  tools.setAttribute("aria-label","Kawalan paparan Al-Quran");
  tools.innerHTML='<div class="tabs" role="tablist" aria-label="Paparan teks"><button class="tab" type="button" role="tab" data-tab="all" aria-selected="true">Semua</button><button class="tab" type="button" role="tab" data-tab="arab" aria-selected="false">Arab</button><button class="tab" type="button" role="tab" data-tab="rumi" aria-selected="false">Rumi</button><button class="tab" type="button" role="tab" data-tab="ms" aria-selected="false">Melayu</button></div><div class="act" role="group" aria-label="Tindakan"><button class="chip" type="button" data-action="copy">Copy</button><button class="chip" type="button" data-action="share">Share</button><button class="chip" type="button" data-action="bookmark" aria-label="Bookmark ayat semasa">★</button><button class="chip" type="button" data-action="resume">Sambung</button><button class="chip" type="button" data-action="print">PDF</button><button class="chip mode" type="button" data-action="mode" aria-label="Tema">🌓</button></div>';
  anchor.parentNode.insertBefore(tools,anchor.nextSibling);
}
})();
