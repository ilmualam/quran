/*! IlmuAlam Quran Home v3.0 | © ilmualam.com | dependency-free, delegated events, chunked rendering */
(()=>{"use strict";
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const store={
  get(k,d){try{const v=localStorage.getItem("ilmq:"+k);return v==null?d:JSON.parse(v)}catch{return d}},
  set(k,v){try{localStorage.setItem("ilmq:"+k,JSON.stringify(v))}catch{}}
};
const reduced=matchMedia("(prefers-reduced-motion: reduce)").matches;
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const norm=s=>String(s).toLowerCase().replace(/[\s\-'’`‘.]/g,"");
const QARI=[["Alafasy_128kbps","Mishary Alafasy"],["Abdurrahmaan_As-Sudais_192kbps","Abdul Rahman As-Sudais"],["Husary_128kbps","Mahmoud Al-Husary"],["Abdul_Basit_Murattal_192kbps","Abdul Basit"],["Ghamadi_40kbps","Saad Al-Ghamadi"]];
let toastEl,toastT;
function toast(m){
  toastEl=toastEl||Object.assign(document.body.appendChild(document.createElement("div")),{className:"toast",role:"status"});
  toastEl.textContent=m;toastEl.classList.add("on");clearTimeout(toastT);toastT=setTimeout(()=>toastEl.classList.remove("on"),1800);
}

/* ---------- theme ---------- */
const root=document.documentElement,themeBtn=$("#theme");
const icon={auto:"🌓",light:"☀️",dark:"🌙"};
function setTheme(t,save){
  t==="auto"?root.removeAttribute("data-theme"):root.setAttribute("data-theme",t);
  if(themeBtn){themeBtn.textContent=icon[t];themeBtn.setAttribute("aria-label","Tema: "+({auto:"automatik",light:"cerah",dark:"gelap"}[t]))}
  if(save)store.set("theme",t);
}
setTheme(store.get("theme","auto"));
themeBtn?.addEventListener("click",()=>{const c=store.get("theme","auto");setTheme(c==="auto"?"light":c==="light"?"dark":"auto",true)});

/* ---------- surah list ---------- */
const grid=$("#grid"),cards=$$(".sc",grid),search=$("#q"),count=$("#cnt"),none=$("#none");
let filter="all",timer=0;
const POP=new Set((grid?.dataset.pop||"").split(",").map(Number));
function applyFilter(){
  const q=norm(search?.value||"");let shown=0;
  for(const c of cards){
    const n=+c.dataset.n,t=c.dataset.t;
    const ok=(filter==="all"||(filter==="makki"&&t==="k")||(filter==="madani"&&t==="d")||(filter==="juz30"&&n>=78)||(filter==="pop"&&POP.has(n)))&&(!q||c.dataset.q.includes(q));
    if(c.hidden===ok){c.hidden=!ok}
    if(ok)shown++;
  }
  if(count)count.textContent=shown===cards.length?"Menunjukkan semua 114 surah":`Menunjukkan ${shown} daripada 114 surah`;
  if(none)none.hidden=shown>0;
}
search?.addEventListener("input",()=>{clearTimeout(timer);timer=setTimeout(applyFilter,90)});
$(".chips")?.addEventListener("click",e=>{
  const b=e.target.closest("button[data-f]");if(!b)return;
  filter=b.dataset.f;$$(".chips button").forEach(x=>x.setAttribute("aria-pressed",x===b?"true":"false"));applyFilter();
});

/* ---------- reader ---------- */
let dlg,verses=[],cur=0,sNo=0,audio,pushed=false,autoNext=store.get("auto",true),view=store.get("view","all"),prevTitle=document.title,loadId=0,renderToken=0;
const info=n=>{const c=cards[n-1];return c&&{n,ar:c.dataset.ar,name:c.dataset.name,mean:c.dataset.mean,ayat:+c.dataset.ayat,meta:c.dataset.meta}};
const baseUrl=()=>location.origin+location.pathname;
const ayahLink=(s,a)=>`${baseUrl()}#surah-${s}-ayat-${a}`;

function build(){
  dlg=document.createElement("dialog");dlg.className="rd";dlg.setAttribute("aria-labelledby","rt");
  dlg.innerHTML=`<div class="rb"><div class="rbr"><button class="ib" type="button" data-a="close" aria-label="Tutup pembaca">✕</button><button class="pp" type="button" data-a="play" aria-label="Mainkan bacaan">▶</button><div class="rt"><h2 id="rt"></h2><p id="rs"></p></div><button class="ib" type="button" data-a="prev" aria-label="Surah sebelum">‹</button><button class="ib" type="button" data-a="next" aria-label="Surah seterusnya">›</button></div>
<div class="rc">
<select id="qs" aria-label="Pilih qari">${QARI.map(q=>`<option value="${q[0]}">${q[1]}</option>`).join("")}</select>
<div class="seg" role="group" aria-label="Paparan teks">${[["all","Semua"],["ar","Arab"],["rumi","Rumi"],["ms","Melayu"]].map(v=>`<button type="button" data-v="${v[0]}" aria-pressed="false">${v[1]}</button>`).join("")}</div>
<label>Saiz <input id="fz" type="range" min="24" max="60" step="2" aria-label="Saiz tulisan Arab"></label>
<label><input id="an" type="checkbox"> Ayat seterusnya</label></div></div>
<div class="rv" id="rv" tabindex="-1" aria-live="polite"></div>`;
  document.body.appendChild(dlg);
  const qs=$("#qs",dlg),fz=$("#fz",dlg),an=$("#an",dlg);
  qs.value=store.get("qari","Alafasy_128kbps");
  fz.value=store.get("fz",34);dlg.style.setProperty("--fzA",fz.value+"px");
  an.checked=autoNext;setView(view);
  qs.addEventListener("change",()=>{store.set("qari",qs.value);if(audio&&!audio.paused)play(cur)});
  fz.addEventListener("input",()=>{dlg.style.setProperty("--fzA",fz.value+"px");store.set("fz",+fz.value)},{passive:true});
  an.addEventListener("change",()=>{autoNext=an.checked;store.set("auto",autoNext)});
  dlg.addEventListener("click",onClick);
  dlg.addEventListener("close",onClose);
}
function setView(v){
  view=v;dlg.dataset.v=v;store.set("view",v);
  $$(".seg button",dlg).forEach(b=>b.setAttribute("aria-pressed",b.dataset.v===v?"true":"false"));
}
const bms=()=>new Set(store.get("bm",[]));
function onClick(e){
  const t=e.target.closest("[data-a],[data-v],[data-k]");if(!t)return;
  if(t.dataset.v)return setView(t.dataset.v);
  const a=t.dataset.a;
  if(a==="close")return closeReader();
  if(a==="prev"||a==="next"){const n=sNo+(a==="next"?1:-1);if(n>=1&&n<=114){history.replaceState(null,"","#surah-"+n);openSurah(n)}return}
  if(a==="play")return togglePlay();
  const card=t.closest(".ay");if(!card)return;
  const i=+card.dataset.i,k=t.dataset.k;
  if(k==="play")return play(i);
  if(k==="copy"){const v=verses[i],text=`${info(sNo).name} (${sNo}:${i+1})\n${v.arabic}\n${v.rumi?"Rumi: "+v.rumi+"\n":""}Maksud: ${v.translation}\n${ayahLink(sNo,i+1)}\n— ilmualam.com`;return copy(text,"Ayat disalin ✓")}
  if(k==="share"){const d={title:`${info(sNo).name} ayat ${i+1}`,text:verses[i].translation,url:ayahLink(sNo,i+1)};if(navigator.share)return navigator.share(d).catch(()=>{});return copy(d.url,"Pautan ayat disalin ✓")}
  if(k==="bm"){const s=bms(),id=sNo+":"+(i+1);s.has(id)?s.delete(id):s.add(id);store.set("bm",[...s]);t.setAttribute("aria-pressed",s.has(id));t.textContent=s.has(id)?"★":"☆";toast(s.has(id)?"Ditanda ★":"Tanda dibuang");remember(i)}
}
async function copy(text,msg){
  try{await navigator.clipboard.writeText(text)}
  catch{const ta=Object.assign(document.createElement("textarea"),{value:text});ta.style.cssText="position:fixed;opacity:0";document.body.appendChild(ta);ta.select();try{document.execCommand("copy")}catch{}ta.remove()}
  toast(msg);
}
function remember(i){store.set("last",{s:sNo,a:i+1});showResume()}

async function openSurah(n,ayat){
  if(!info(n))return;
  if(!dlg)build();
  const id=++loadId;stopAudio();
  sNo=n;const m=info(n);
  $("#rt",dlg).textContent=`${n}. ${m.name} · ${m.ar}`;
  $("#rs",dlg).textContent=`${m.mean} · ${m.ayat} ayat · ${m.meta}`;
  $('[data-a="prev"]',dlg).disabled=n===1;$('[data-a="next"]',dlg).disabled=n===114;
  const rv=$("#rv",dlg);rv.innerHTML='<p class="rm">Memuatkan surah…</p>';
  if(!dlg.open){prevTitle=document.title;dlg.showModal()}
  document.title=`Surah ${m.name} (${n}) – Baca Al-Quran Online | Ilmu Alam`;
  dlg.scrollTop=0;
  try{
    const r=await fetch(`data-surah/surah-${n}.json`);if(!r.ok)throw 0;
    const d=await r.json();if(id!==loadId)return;
    verses=d;cur=Math.max(0,Math.min(d.length-1,(ayat||1)-1));
    render(rv,m,ayat);
  }catch{if(id===loadId)rv.innerHTML=`<p class="rm" role="alert">Surah tidak dapat dimuatkan. Semak sambungan internet anda, kemudian <a href="#surah-${n}" data-retry>cuba lagi</a>.</p>`}
}
function ayHTML(v,i,marks){
  const n=i+1,on=marks.has(sNo+":"+n);
  return `<article class="ay" id="ayat-${n}" data-i="${i}"><div class="ah"><a class="no" href="#surah-${sNo}-ayat-${n}" aria-label="Pautan ayat ${n}">${sNo}:${n}</a><div class="ac" role="group" aria-label="Tindakan ayat ${n}"><button type="button" data-k="play" aria-label="Main ayat ${n}">▶</button><button type="button" class="t" data-k="copy" aria-label="Salin ayat ${n}">Salin</button><button type="button" class="t" data-k="share" aria-label="Kongsi ayat ${n}">Kongsi</button><button type="button" data-k="bm" aria-pressed="${on}" aria-label="Tanda ayat ${n}">${on?"★":"☆"}</button></div></div><p class="ar" lang="ar" dir="rtl">${esc(v.arabic)}</p>${v.rumi?`<p class="ru" lang="ms">${esc(v.rumi)}</p>`:""}<p class="ms" lang="ms">${esc(v.translation)}</p></article>`;
}
function render(rv,m,ayat){
  const token=++renderToken,marks=bms(),CH=30;
  rv.innerHTML=(sNo!==1&&sNo!==9?'<p class="bs" lang="ar" dir="rtl">بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</p>':"")+'<div id="av"></div>';
  const av=$("#av",rv);let at=0;
  const goTo=ayat&&ayat>1?ayat:0;
  (function chunk(){
    if(token!==renderToken)return;
    const end=Math.min(verses.length,at+CH);let h="";
    for(;at<end;at++)h+=ayHTML(verses[at],at,marks);
    av.insertAdjacentHTML("beforeend",h);
    if(goTo&&at>=goTo&&!chunk.done){chunk.done=1;requestAnimationFrame(()=>{const el=$("#ayat-"+goTo,dlg);if(el){el.scrollIntoView({block:"start"});mark(goTo-1)}})}
    if(at<verses.length)setTimeout(chunk,0);
    else av.insertAdjacentHTML("afterend",`<div class="rf">${sNo>1?`<a class="btn ghost" style="color:var(--lk);border-color:var(--bd)" href="#surah-${sNo-1}">‹ ${esc(info(sNo-1).name)}</a>`:"<span></span>"}${sNo<114?`<a class="btn ghost" style="color:var(--lk);border-color:var(--bd)" href="#surah-${sNo+1}">${esc(info(sNo+1).name)} ›</a>`:""}</div>`);
  })();
}
function mark(i){
  $$(".ay.on",dlg).forEach(x=>x.classList.remove("on"));
  const el=$("#ayat-"+(i+1),dlg);el?.classList.add("on");return el;
}

/* ---------- audio ---------- */
function ensureAudio(){
  if(audio)return audio;
  audio=new Audio();audio.preload="none";
  audio.addEventListener("ended",()=>{if(autoNext&&cur+1<verses.length)play(cur+1);else setPP(false)});
  audio.addEventListener("pause",()=>setPP(false));
  audio.addEventListener("playing",()=>setPP(true));
  audio.addEventListener("error",()=>{setPP(false);toast("Audio tidak dapat dimainkan.")});
  return audio;
}
function setPP(on){const b=dlg&&$('[data-a="play"]',dlg);if(b){b.textContent=on?"⏸":"▶";b.setAttribute("aria-label",on?"Jeda bacaan":"Mainkan bacaan")}}
function stopAudio(){if(audio){audio.pause();audio.removeAttribute("src");audio.load()}setPP(false)}
function play(i){
  if(i<0||i>=verses.length)return;
  cur=i;const a=ensureAudio(),q=$("#qs",dlg).value;
  a.src=`https://everyayah.com/data/${q}/${String(sNo).padStart(3,"0")}${String(i+1).padStart(3,"0")}.mp3`;
  const el=mark(i);
  if(el&&store.get("scroll",true))el.scrollIntoView({block:"center",behavior:reduced?"auto":"smooth"});
  a.play().catch(()=>toast("Tekan ▶ untuk mula."));
  remember(i);
  if("mediaSession" in navigator){try{navigator.mediaSession.metadata=new MediaMetadata({title:`${info(sNo).name} · Ayat ${i+1}`,artist:$("#qs",dlg).selectedOptions[0].textContent,album:"Al-Quran Online – ilmualam.com"})}catch{}}
}
function togglePlay(){
  if(!audio||!audio.src){return play(cur)}
  audio.paused?audio.play().catch(()=>{}):audio.pause();
}

/* ---------- routing ---------- */
const RE=/^#surah-(\d{1,3})(?:-ayat-(\d{1,3}))?$/;
function route(initial){
  const m=RE.exec(location.hash);
  if(!m){if(dlg?.open){pushed=false;dlg.close()}return}
  const n=+m[1];if(n<1||n>114)return;
  if(!initial&&!dlg?.open)pushed=true;
  openSurah(n,m[2]?+m[2]:0);
}
function closeReader(){
  if(pushed&&RE.test(location.hash)){history.back()}else dlg.close();
}
function onClose(){
  stopAudio();document.title=prevTitle;
  if(RE.test(location.hash))history.replaceState(null,"",location.pathname+location.search);
  pushed=false;
}
addEventListener("hashchange",()=>route(false));
document.addEventListener("click",e=>{const r=e.target.closest("[data-retry]");if(r){e.preventDefault();route(false)}});

/* ---------- resume ---------- */
function showResume(){
  const el=$("#resume"),l=store.get("last",null);
  if(!el||!l||!info(l.s))return;
  el.innerHTML=`📌 Sambung bacaan: <a href="#surah-${l.s}-ayat-${l.a}">${esc(info(l.s).name)} ayat ${l.a}</a>`;
}
showResume();
applyFilter();
if(RE.test(location.hash))route(true);
})();
