/*! IlmuAlam Quran Tools v1.1 | © ilmualam.com | khatam, hafazan, tasbih, cari ayat, solat, solat sunat, jamak & qasar, zakat fitrah, zakat pendapatan, simpanan, emas, perniagaan, faraid, asmaul husna, masjid, kalendar Hijrah, tahlil, Ramadan, Iqra', mengaji. Schedule maths mirror tools/plans.py */
(()=>{"use strict";
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const store={
  get(k,d){try{const v=localStorage.getItem("ilmq:"+k);return v==null?d:JSON.parse(v)}catch{return d}},
  set(k,v){try{localStorage.setItem("ilmq:"+k,JSON.stringify(v))}catch{}}
};
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
let toastEl,toastT;
function toast(m){
  toastEl=toastEl||Object.assign(document.body.appendChild(document.createElement("div")),{className:"toast",role:"status"});
  toastEl.textContent=m;toastEl.classList.add("on");clearTimeout(toastT);toastT=setTimeout(()=>toastEl.classList.remove("on"),1800);
}
function copy(text,msg){
  const ok=()=>toast(msg);
  if(navigator.clipboard&&isSecureContext)navigator.clipboard.writeText(text).then(ok,()=>fallback());else fallback();
  function fallback(){const t=document.createElement("textarea");t.value=text;t.setAttribute("readonly","");t.style.cssText="position:fixed;opacity:0";document.body.appendChild(t);t.select();try{document.execCommand("copy");ok()}catch{}t.remove()}
}

/* ---------- shared data + date helpers (same strings as plans.py) ---------- */
const Q=JSON.parse($("#qd")?.textContent||"null");
const HARI=["Ahad","Isnin","Selasa","Rabu","Khamis","Jumaat","Sabtu"];
const BLN=["Januari","Februari","Mac","April","Mei","Jun","Julai","Ogos","September","Oktober","November","Disember"];
const BLS=["Jan","Feb","Mac","Apr","Mei","Jun","Jul","Ogo","Sep","Okt","Nov","Dis"];
const pad=n=>String(n).padStart(2,"0");
const iso=d=>`${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
const parseD=s=>{const m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(s||"");if(!m)return null;const d=new Date(+m[1],m[2]-1,+m[3]);return isNaN(d)?null:d};
const addD=(d,n)=>new Date(d.getFullYear(),d.getMonth(),d.getDate()+n);
const today=()=>{const n=new Date();return new Date(n.getFullYear(),n.getMonth(),n.getDate())};
const dshort=d=>`${HARI[d.getDay()]}, ${d.getDate()} ${BLS[d.getMonth()]}`;
const dlong=d=>`${HARI[d.getDay()]}, ${d.getDate()} ${BLN[d.getMonth()]} ${d.getFullYear()}`;
const r1=x=>(Math.floor(x*10+.5)/10).toFixed(1);
const num=n=>String(n).replace(/\B(?=(\d{3})+(?!\d))/g,",");
const clamp=(v,a,b,d)=>{v=parseInt(v,10);return Number.isFinite(v)?Math.min(b,Math.max(a,v)):d};
const readHash=()=>Object.fromEntries(new URLSearchParams(location.hash.slice(1)));
const writeHash=o=>history.replaceState(null,"","#"+new URLSearchParams(o).toString());

let NAMES,OFF,TOTAL,PS,JS,NP=604;
if(Q){
  NAMES=Q.n;OFF=[0];for(const c of Q.c)OFF.push(OFF[OFF.length-1]+c);TOTAL=OFF[114];
  PS=[...Q.p,TOTAL+1];JS=[...Q.j,TOTAL+1];
}
const gid=(s,a)=>OFF[s-1]+a;
function sa(g){let s=1;while(OFF[s]<g)s++;return[s,g-OFF[s-1]]}
function pageOf(g){let lo=0,hi=NP-1;while(lo<hi){const m=(lo+hi+1)>>1;if(PS[m]<=g)lo=m;else hi=m-1}return lo+1}
const ref=g=>{const[s,a]=sa(g);return`${NAMES[s-1]} ${s}:${a}`};

function toolbar(root,{ics,file}){
  root.addEventListener("click",e=>{
    const b=e.target.closest("button[data-act]");if(!b)return;
    if(b.dataset.act==="link")copy(location.href,"Pautan jadual disalin ✓");
    else if(b.dataset.act==="print")print();
    else if(b.dataset.act==="ics"&&ics){
      const blob=new Blob([ics()],{type:"text/calendar;charset=utf-8"}),a=document.createElement("a");
      a.href=URL.createObjectURL(blob);a.download=file();document.body.appendChild(a);a.click();
      setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1000);toast("Fail kalendar dimuat turun ✓");
    }
  });
}
const icsEsc=s=>String(s).replace(/[\\;,]/g,m=>"\\"+m);
function icsCal(events){
  const st=new Date().toISOString().replace(/[-:]/g,"").replace(/\.\d+/,"");
  const L=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Ilmu Alam//Al-Quran Online//MS","CALSCALE:GREGORIAN"];
  events.forEach((e,i)=>{const d=iso(e.d).replace(/-/g,""),n=iso(addD(e.d,1)).replace(/-/g,"");
    L.push("BEGIN:VEVENT",`UID:${d}-${i}-${Math.random().toString(36).slice(2)}@quran.ilmualam.com`,`DTSTAMP:${st}`,`DTSTART;VALUE=DATE:${d}`,`DTEND;VALUE=DATE:${n}`,`SUMMARY:${icsEsc(e.t)}`,`DESCRIPTION:${icsEsc(e.x)}`,"END:VEVENT")});
  L.push("END:VCALENDAR");return L.join("\r\n");
}
function setIf(el,html){if(el&&el.innerHTML!==html)el.innerHTML=html}

/* ---------- jadual khatam ---------- */
const kf=$("#kf");
if(kf&&Q){
  const kd=$("#kd"),ks=$("#ks"),kr=$("#kr"),sum=$("#ksum"),tb=$("#kt tbody"),prog=$("#kprog");
  function khatam(D,r){
    const R=NP-r;D=Math.max(1,Math.min(D,R));
    if(r===0&&30%D===0){const k=30/D;return[Array.from({length:D},(_,i)=>[JS[i*k],JS[(i+1)*k]-1]),true,D]}
    const base=Math.floor(R/D),extra=R%D,out=[];let p=r;
    for(let i=0;i<D;i++){const n=base+(i<extra?1:0);out.push([PS[p],PS[p+n]-1]);p+=n}
    return[out,false,D];
  }
  let cur=null;
  function render(){
    const r=clamp(kr.value,0,NP-1,0),start=parseD(ks.value)||today();
    let D=clamp(kd.value,1,1000,30);
    const[rows,juz,DD]=khatam(D,r);D=DD;const R=NP-r;
    const trs=rows.map(([g1,g2],i)=>{
      const p1=pageOf(g1),p2=pageOf(g2),[s,a]=sa(g1),pg=p1===p2?String(p1):`${p1}–${p2}`;
      return`<tr><td>${i+1}</td><td>${dshort(addD(start,i))}</td><td>${pg}</td><td><a href="/#surah-${s}-ayat-${a}">${ref(g1)}</a></td><td>${ref(g2)}</td><td><input type="checkbox" data-d="${i+1}" aria-label="Hari ${i+1} selesai"></td></tr>`;
    }).join("");
    let per;
    if(juz)per=`${30/D} juzuk sehari`;else{const b=Math.floor(R/D),x=R%D;per=x===0?`${b} muka surat sehari`:`${b}–${b+1} muka surat sehari`}
    const left=r?` (baki ${R} muka surat)`:"";
    setIf(sum,`<p><strong>Baca ${per}</strong> untuk khatam dalam ${D} hari${left}: purata <strong>${r1(R/D)} muka surat sehari</strong>, atau kira-kira ${r1(R/D/5)} muka surat selepas setiap solat fardu.</p><p>Tarikh khatam: <strong>${dlong(addD(start,D-1))}</strong></p>`);
    setIf(tb,trs);
    cur={rows,D,start,sig:`${D}|${r}|${iso(start)}`};
    const done=store.get("khatam",null),set=new Set(done&&done.sig===cur.sig?done.d:[]);
    $$("input[data-d]",tb).forEach(c=>c.checked=set.has(+c.dataset.d));
    showProg(set.size);
    $$(".kpre button").forEach(b=>b.setAttribute("aria-pressed",String(+b.dataset.v===D)));
  }
  function showProg(n){if(prog)prog.textContent=n?`✓ ${n} daripada ${cur.D} hari selesai${n===cur.D?" — Alhamdulillah, khatam!":""}`:""}
  function update(){render();writeHash({hari:kd.value,mula:ks.value,dibaca:kr.value})}
  const h=readHash();
  kd.value=clamp(h.hari,1,1000,+kd.value||30);kr.value=clamp(h.dibaca,0,NP-1,0);ks.value=parseD(h.mula)?h.mula:iso(today());
  render();
  kf.addEventListener("input",update);kf.addEventListener("submit",e=>{e.preventDefault();update()});
  $(".kpre")?.addEventListener("click",e=>{const b=e.target.closest("button[data-v]");if(b){kd.value=b.dataset.v;update()}});
  tb.addEventListener("change",e=>{
    const c=e.target.closest("input[data-d]");if(!c)return;
    const d=$$("input[data-d]",tb).filter(x=>x.checked).map(x=>+x.dataset.d);
    store.set("khatam",{sig:cur.sig,d});showProg(d.length);
  });
  toolbar($("#kact"),{file:()=>`jadual-khatam-${cur.D}-hari.ics`,ics:()=>icsCal(cur.rows.map(([g1,g2],i)=>{
    const p1=pageOf(g1),p2=pageOf(g2);
    return{d:addD(cur.start,i),t:`Khatam Al-Quran – Hari ${i+1}: muka surat ${p1}–${p2}`,x:`Mula ${ref(g1)}, tamat ${ref(g2)}. ${location.href}`};
  }))});
}

/* ---------- jadual hafazan ---------- */
const hf=$("#hf");
if(hf&&Q){
  const T=Object.fromEntries(Q.t.map(([k,l,s])=>[k,[l,s]])),W=Q.w,MAX=Q.m;
  const el=id=>$("#"+id),sum=el("hsum"),tb=$("#ht tbody");
  function hafazan(key,order,unit,n,week,start){
    let[lab,segs]=T[key];
    if(order==="pendek"&&unit==="ayat")segs=[...segs].reverse();
    const items=[];
    for(const[s,a1,a2]of segs)for(let a=a1;a<=a2;a++){
      const g=gid(s,a),last=items[items.length-1];
      if(unit==="page"&&last&&pageOf(last[last.length-1])===pageOf(g)&&last[last.length-1]===g-1)last.push(g);else items.push([g]);
    }
    const sessions=[];for(let i=0;i<items.length;i+=n)sessions.push(items.slice(i,i+n).flat());
    const days=W[week][1],dates=[];let d=start;
    for(const _ of sessions){while(!days.includes(d.getDay()))d=addD(d,1);dates.push(d);d=addD(d,1)}
    return[lab,sessions,dates,items.reduce((t,x)=>t+x.length,0)];
  }
  function label(gs){
    const parts=[];let i=0;
    while(i<gs.length){
      const[s,a]=sa(gs[i]);let j=i;
      while(j+1<gs.length&&gs[j+1]===gs[j]+1&&sa(gs[j+1])[0]===s)j++;
      const b=sa(gs[j])[1];parts.push(a===b?`${NAMES[s-1]} ${a}`:`${NAMES[s-1]} ${a}–${b}`);i=j+1;
    }
    return parts.join(", ");
  }
  let cur=null;
  function render(){
    const key=T[el("htg").value]?el("htg").value:"j30",unit=el("hu").value==="page"?"page":"ayat",order=el("ho").value==="mushaf"?"mushaf":"pendek";
    const n=clamp(el("hn").value,1,unit==="page"?20:50,unit==="page"?1:5),week=W[el("hw").value]?el("hw").value:"7",start=parseD(el("hs").value)||today();
    el("ho").disabled=unit==="page";
    const[lab,sessions,dates,tot]=hafazan(key,order,unit,n,week,start);
    let trs=sessions.slice(0,MAX).map((gs,i)=>{const[s,a]=sa(gs[0]);return`<tr><td>${i+1}</td><td>${dshort(dates[i])}</td><td><a href="/#surah-${s}-ayat-${a}">${label(gs)}</a></td><td>${gs.length}</td></tr>`}).join("");
    if(sessions.length>MAX)trs+=`<tr><td colspan="4">… dan ${num(sessions.length-MAX)} sesi lagi. Cetak atau salin pautan untuk simpan rancangan ini.</td></tr>`;
    const end=dates[dates.length-1],weeks=Math.ceil((Math.round((end-start)/864e5)+1)/7),u=unit==="ayat"?"ayat":"muka surat";
    setIf(sum,`<p><strong>${lab}</strong> (${num(tot)} ayat) pada kadar ${n} ${u} sehari, ${W[week][0]}: <strong>${num(sessions.length)} sesi hafazan</strong>, dijangka tamat pada <strong>${dlong(end)}</strong> (kira-kira ${weeks} minggu).</p>`);
    setIf(tb,trs);
    cur={sessions,dates,lab};
  }
  function update(){render();writeHash({sasaran:el("htg").value,susunan:el("ho").value,unit:el("hu").value,kadar:el("hn").value,hari:el("hw").value,mula:el("hs").value})}
  const h=readHash();
  if(T[h.sasaran])el("htg").value=h.sasaran;
  if(h.susunan==="mushaf"||h.susunan==="pendek")el("ho").value=h.susunan;
  if(h.unit==="page"||h.unit==="ayat")el("hu").value=h.unit;
  if(h.kadar)el("hn").value=clamp(h.kadar,1,50,5);
  if(W[h.hari])el("hw").value=h.hari;
  el("hs").value=parseD(h.mula)?h.mula:iso(today());
  render();
  hf.addEventListener("input",update);hf.addEventListener("change",update);hf.addEventListener("submit",e=>{e.preventDefault();update()});
  toolbar($("#hact"),{file:()=>"jadual-hafazan.ics",ics:()=>icsCal(cur.sessions.map((gs,i)=>({d:cur.dates[i],t:`Hafazan sesi ${i+1}: ${label(gs)}`,x:`${cur.lab} – ${gs.length} ayat. ${location.href}`})))});
}

/* ---------- tasbih digital ---------- */
const tz=$("#tz");
if(tz){
  const Z=JSON.parse($("#zd").textContent),btn=$("#tbtn"),cnt=$("#tcnt"),tgt=$("#ttgt"),ring=$("#tring"),ar=$("#tar"),rm=$("#trm"),mn=$("#tmn"),day=$("#tday"),all=$("#tall"),step=$("#tstep"),custom=$("#tcustom");
  const C=2*Math.PI*54;
  const st=Object.assign({p:"solat",i:0,c:0,custom:33,vib:true,days:{},all:0},store.get("tasbih",{}));
  const todayKey=()=>iso(today());
  const seq=()=>st.p==="bebas"?[{...Z.bebas.s[0],n:st.custom}]:(Z[st.p]||Z.solat).s;
  function save(){store.set("tasbih",st)}
  function paint(){
    const s=seq(),z=s[Math.min(st.i,s.length-1)];
    cnt.textContent=st.c;tgt.textContent=z.n?`/ ${z.n}`:"";
    ar.textContent=z.a;rm.textContent=z.r;mn.textContent=z.m;
    ring.style.strokeDashoffset=z.n?String(C*(1-Math.min(st.c,z.n)/z.n)):String(C);
    step.textContent=s.length>1?`Langkah ${Math.min(st.i,s.length-1)+1} daripada ${s.length}`:"";
    day.textContent=num(st.days[todayKey()]||0);all.textContent=num(st.all);
    $$("#tpre button").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.p===st.p)));
    custom.hidden=st.p!=="bebas";
    btn.setAttribute("aria-label",`Kira ${z.r}. Kiraan ${st.c}${z.n?" daripada "+z.n:""}`);
  }
  function vib(ms){if(st.vib&&navigator.vibrate)try{navigator.vibrate(ms)}catch{}}
  function tap(){
    const s=seq(),z=s[Math.min(st.i,s.length-1)];
    st.c++;st.all++;const k=todayKey();st.days={[k]:(st.days[k]||0)+1};
    if(z.n&&st.c>=z.n){
      if(st.i+1<s.length){st.i++;st.c=0;vib([60,40,60]);toast("Seterusnya: "+s[st.i].r)}
      else{vib([120,60,120]);toast(st.c===z.n?"Selesai ✓ Alhamdulillah":"Melebihi sasaran")}
    }else vib(12);
    save();paint();
  }
  btn.addEventListener("click",tap);
  $("#tpre").addEventListener("click",e=>{const b=e.target.closest("button[data-p]");if(!b)return;st.p=b.dataset.p;st.i=0;st.c=0;save();paint()});
  $("#tundo").addEventListener("click",()=>{if(st.c>0){st.c--;st.all=Math.max(0,st.all-1);const k=todayKey();st.days[k]=Math.max(0,(st.days[k]||0)-1)}else if(st.i>0){st.i--;st.c=seq()[st.i].n-1}save();paint()});
  $("#treset").addEventListener("click",()=>{st.i=0;st.c=0;save();paint();toast("Kiraan diset semula")});
  const vb=$("#tvib");vb.setAttribute("aria-pressed",String(st.vib));
  vb.addEventListener("click",()=>{st.vib=!st.vib;vb.setAttribute("aria-pressed",String(st.vib));save();toast(st.vib?"Getaran dihidupkan":"Getaran dimatikan")});
  $("#tn").value=st.custom;
  $("#tn").addEventListener("input",e=>{st.custom=clamp(e.target.value,1,100000,33);save();paint()});
  let lock=null;const wl=$("#twake");
  if(!("wakeLock" in navigator))wl.hidden=true;
  wl.addEventListener("click",async()=>{
    if(lock){lock.release();lock=null;wl.setAttribute("aria-pressed","false");return}
    try{lock=await navigator.wakeLock.request("screen");wl.setAttribute("aria-pressed","true");lock.addEventListener("release",()=>{lock=null;wl.setAttribute("aria-pressed","false")})}catch{toast("Tidak disokong oleh pelayar ini")}
  });
  paint();
}

/* ---------- cari ayat ---------- */
const cf=$("#cf");
if(cf&&Q){
  const q=$("#cq"),out=$("#cres"),stat=$("#cstat");let idx=null,loading=null,last="",shown=50;
  const fold=s=>s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[’‘`]/g,"'");
  function load(){
    if(idx)return Promise.resolve(idx);
    if(!loading){stat.textContent="Memuatkan terjemahan 6,236 ayat…";loading=fetch("/assets/data/terjemahan-ms.json").then(r=>{if(!r.ok)throw 0;return r.json()}).then(d=>{idx=d.map(s=>s.map(t=>[t,fold(t)]));return idx}).catch(()=>{loading=null;stat.textContent="Gagal memuatkan data. Semak sambungan internet dan cuba lagi.";throw 0})}
    return loading;
  }
  function card(s,a,t,terms){
    let h=esc(t);
    for(const w of terms){if(w.length<2)continue;h=h.replace(new RegExp("("+w.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+")","gi"),"<mark>$1</mark>")}
    return`<li><p class="cref"><a href="/#surah-${s}-ayat-${a}">${esc(NAMES[s-1])} ${s}:${a}</a></p><p>${h}</p><p class="cgo"><a href="/#surah-${s}-ayat-${a}">Baca &amp; dengar ayat ini ›</a></p></li>`;
  }
  function run(more){
    const v=q.value.trim();
    if(!more)shown=50;
    writeHash(v?{q:v}:{});
    if(!v){out.innerHTML="";stat.textContent="";return}
    const m=/^(\d{1,3})\s*[: ]\s*(\d{1,3})$/.exec(v);
    load().then(d=>{
      if(m){const s=+m[1],a=+m[2];
        if(s>=1&&s<=114&&a>=1&&a<=d[s-1].length){stat.textContent=`Surah ${NAMES[s-1]}, ayat ${a}`;out.innerHTML=card(s,a,d[s-1][a-1][0],[])}
        else{stat.textContent="Rujukan ayat tidak wujud. Contoh betul: 2:255 atau 36 12.";out.innerHTML=""}
        return}
      const terms=fold(v).split(/\s+/).filter(Boolean),hits=[];
      d.forEach((sur,i)=>sur.forEach(([t,f],j)=>{if(terms.every(w=>f.includes(w)))hits.push([i+1,j+1,t])}));
      stat.textContent=hits.length?`Ditemui ${num(hits.length)} ayat mengandungi “${v}”${hits.length>shown?` (menunjukkan ${shown} pertama)`:""}`:`Tiada ayat mengandungi “${v}”. Cuba perkataan lain atau ejaan lain (contoh: sembahyang/solat).`;
      out.innerHTML=hits.slice(0,shown).map(([s,a,t])=>card(s,a,t,terms.map(w=>esc(w)))).join("")+(hits.length>shown?`<li class="cmore"><button class="btn2" type="button" data-more>Tunjuk 50 lagi</button></li>`:"");
    }).catch(()=>{});
  }
  let t=0;
  q.addEventListener("focus",()=>load().catch(()=>{}),{once:true});
  q.addEventListener("input",()=>{clearTimeout(t);t=setTimeout(()=>run(false),220)});
  cf.addEventListener("submit",e=>{e.preventDefault();run(false)});
  out.addEventListener("click",e=>{if(e.target.closest("[data-more]")){shown+=50;run(true)}});
  $$("[data-q]").forEach(b=>b.addEventListener("click",()=>{q.value=b.dataset.q;run(false);q.scrollIntoView({block:"start"})}));
  const h=readHash();if(h.q){q.value=h.q;run(false)}
}
/* ---------- doa: filter, search, copy ---------- */
const df=$("#df");
if(df){
  const items=$$(".dw"),q=$("#dq"),cnt=$("#dcnt");let cat="all";
  const fold=s=>s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"");
  function apply(){
    const v=fold(q.value.trim());let n=0;
    for(const it of items){const ok=(cat==="all"||it.dataset.c===cat)&&(!v||fold(it.dataset.q).includes(v));if(it.hidden===ok)it.hidden=!ok;if(ok)n++}
    $$(".dsec").forEach(s=>{s.hidden=!$$(".dw",s).some(x=>!x.hidden)});
    cnt.textContent=n===items.length?`${n} doa dan ayat`:`Menunjukkan ${n} daripada ${items.length}`;
  }
  q.addEventListener("input",apply);df.addEventListener("submit",e=>{e.preventDefault();apply()});
  $("#dcat").addEventListener("click",e=>{const b=e.target.closest("button[data-c]");if(!b)return;cat=b.dataset.c;$$("#dcat button").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));apply()});
}
document.addEventListener("click",e=>{
  const b=e.target.closest("button[data-copy]");if(!b)return;
  const c=b.closest("[data-txt]");if(!c)return;
  copy(`${c.dataset.txt}\n\n${location.origin+location.pathname}#${c.id}`,"Disalin ✓");
});

/* ---------- zikir: per-item counters, reset daily ---------- */
const zk=$(".zk");
if(zk){
  const key="zikir:"+iso(today());let st=store.get(key,{});
  function paint(){
    $$(".zc").forEach(b=>{const n=+b.dataset.n,c=Math.min(st[b.dataset.id]||0,n);b.textContent=c>=n?"✓ Selesai":`${c} / ${n}`;b.classList.toggle("done",c>=n);b.setAttribute("aria-label",`Kira ${b.dataset.t}: ${c} daripada ${n}`)});
    $$(".zsec").forEach(s=>{const bs=$$(".zc",s),d=bs.filter(b=>(st[b.dataset.id]||0)>=+b.dataset.n).length,p=$(".zprog",s);if(p)p.textContent=`${d} / ${bs.length} selesai hari ini`});
  }
  document.addEventListener("click",e=>{
    const b=e.target.closest(".zc");
    if(b){const n=+b.dataset.n,c=(st[b.dataset.id]||0);if(c<n){st[b.dataset.id]=c+1;if(navigator.vibrate)try{navigator.vibrate(c+1>=n?[60,40,60]:10)}catch{}}store.set(key,st);paint();return}
    const r=e.target.closest("[data-zreset]");
    if(r){$$(".zc",r.closest(".zsec")).forEach(x=>delete st[x.dataset.id]);store.set(key,st);paint();toast("Kiraan diset semula")}
  });
  try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&k.startsWith("ilmq:zikir:")&&k!=="ilmq:"+key)localStorage.removeItem(k)}}catch{}
  paint();
}

/* ---------- tajwid: nun/mim analyser + quiz ---------- */
const tj=$("#tj");
if(tj){
  const T=JSON.parse($("#tjd").textContent),out=$("#tjout");let mode="nun";
  const rule=(m,h)=>m==="nun"?(T.halqi.includes(h)?"izhar":T.yanmu.includes(h)?"idgham-g":T.lr.includes(h)?"idgham-b":h==="ب"?"iqlab":"ikhfa"):(h==="ب"?"ikhfa-s":h==="م"?"idgham-m":"izhar-s");
  function show(h){
    const r=T.rules[rule(mode,h)],x=T.ex[rule(mode,h)];
    out.innerHTML=`<p class="tjh">${mode==="nun"?"Nun mati / tanwin":"Mim mati"} + <span lang="ar" dir="rtl">${h}</span> → <strong>${r[0]}</strong></p><p>${r[1]}</p>${x?`<p class="tjx">Contoh: <span class="tjw" lang="ar" dir="rtl">${x[2]}</span> <a href="/#surah-${x[0]}-ayat-${x[1]}">${x[3]} ${x[0]}:${x[1]} ›</a></p>`:""}`;
  }
  $("#tjmode").addEventListener("click",e=>{const b=e.target.closest("button[data-m]");if(!b)return;mode=b.dataset.m;$$("#tjmode button").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));out.innerHTML=`<p>Pilih huruf selepas ${mode==="nun"?"nun mati atau tanwin":"mim mati"}.</p>`});
  $("#tjgrid").addEventListener("click",e=>{const b=e.target.closest("button[data-h]");if(b){$$("#tjgrid button").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));show(b.dataset.h)}});
  // quiz
  const qz=$("#qz");let qs=[],qi=0,score=0;
  const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
  function ask(){
    if(qi>=qs.length){qz.innerHTML=`<p class="qzs">Markah anda: <strong>${score} / ${qs.length}</strong> ${score===qs.length?"— Masya-Allah, sempurna!":score>=qs.length*.7?"— Bagus!":"— Ulang kaji jadual di atas dan cuba lagi."}</p><button class="btn3" type="button" data-qstart>Cuba lagi</button>`;return}
    const q=qs[qi],names=[...new Set(T.q.map(x=>x[1]))].filter(n=>n!==q[1]),opts=shuffle([q[1],...shuffle(names).slice(0,3)]);
    qz.innerHTML=`<p class="qzn">Soalan ${qi+1} daripada ${qs.length} · Markah ${score}</p><p class="qzw" lang="ar" dir="rtl">${q[2]}</p><p class="qzr">${q[3]} ${q[4]}:${q[5]}</p><div class="qzo">${opts.map(o=>`<button class="btn2" type="button" data-a="${o}">${o}</button>`).join("")}</div><p class="qzf" aria-live="polite"></p>`;
  }
  qz.addEventListener("click",e=>{
    if(e.target.closest("[data-qstart]")){qs=shuffle([...T.q]).slice(0,10);qi=0;score=0;ask();return}
    const b=e.target.closest("button[data-a]");if(!b||b.disabled)return;
    const q=qs[qi],ok=b.dataset.a===q[1];if(ok)score++;
    $$("button[data-a]",qz).forEach(x=>{x.disabled=true;if(x.dataset.a===q[1])x.classList.add("ok");else if(x===b)x.classList.add("no")});
    $(".qzf",qz).innerHTML=`${ok?"✓ Betul.":"✗ Jawapan: <strong>"+q[1]+"</strong>."} ${q[6]} <a href="/#surah-${q[4]}-ayat-${q[5]}">Dengar ayat ›</a><br><button class="btn2" type="button" data-next>Seterusnya ›</button>`;
  });
  qz.addEventListener("click",e=>{if(e.target.closest("[data-next]")){qi++;ask()}});
}

/* ---------- prayer-time maths (mirror tools/solat.py) + official JAKIM files: shared by waktu solat and Ramadan ---------- */
const rad=x=>x*Math.PI/180,deg=x=>x*180/Math.PI,mod=(x,n)=>(x%n+n)%n;
function sun(jd){const D=jd-2451545,g=mod(357.529+.98560028*D,360),q=mod(280.459+.98564736*D,360),L=mod(q+1.915*Math.sin(rad(g))+.02*Math.sin(rad(2*g)),360),e=23.439-.00000036*D;
  const ra=mod(deg(Math.atan2(Math.cos(rad(e))*Math.sin(rad(L)),Math.cos(rad(L))))/15,24),decl=deg(Math.asin(Math.sin(rad(e))*Math.sin(rad(L))));let eqt=q/15-ra;eqt=eqt-24*Math.round(eqt/24);return[decl,eqt]}
function jdn(y,m,d){if(m<=2){y-=1;m+=12}const A=Math.floor(y/100),B=2-A+Math.floor(A/4);return Math.floor(365.25*(y+4716))+Math.floor(30.6001*(m+1))+d+B-1524.5}
function solatDay(y,m,d,lat,lng,fa=18,is=18,tz=8){
  const jd=jdn(y,m,d)-lng/(15*24),noon=t=>mod(12-sun(jd+t)[1],24);
  const at=(a,t,ccw)=>{const decl=sun(jd+t)[0];const x=(-Math.sin(rad(a))-Math.sin(rad(decl))*Math.sin(rad(lat)))/(Math.cos(rad(decl))*Math.cos(rad(lat)));const T=deg(Math.acos(Math.max(-1,Math.min(1,x))))/15;return noon(t)+(ccw?-T:T)};
  const asr=t=>{const decl=sun(jd+t)[0];return at(-deg(Math.atan(1/(1+Math.tan(rad(Math.abs(lat-decl)))))),t,false)};
  let f=at(fa,5/24,true),sr=at(.833,6/24,true),z=noon(12/24),a=asr(13/24),mg=at(.833,18/24,false),i=at(is,18/24,false);
  const adj=tz-lng/15;[f,sr,z,a,mg,i]=[f,sr,z,a,mg,i].map(x=>(x+adj)*60);
  const up=x=>Math.ceil(x+1),sub=up(f);return[sub-10,sub,Math.floor(sr),Math.ceil(z+2),up(a),up(mg),up(i)];
}
const hm=x=>`${pad(Math.floor(x/60))}:${pad(x%60)}`;
const qibla=(lat,lng)=>{const p1=rad(lat),p2=rad(21.4225),dl=rad(39.8262-lng);return mod(deg(Math.atan2(Math.sin(dl),Math.cos(p1)*Math.tan(p2)-Math.sin(p1)*Math.cos(dl))),360)};
const doy=d=>Math.round((new Date(d.getFullYear(),d.getMonth(),d.getDate())-new Date(d.getFullYear(),0,1))/864e5);
const offCache={};let offIdx=null;
function official(zone,y){
  const k=zone+"-"+y;
  offIdx=offIdx||fetch("/assets/data/solat/index.json").then(r=>r.ok?r.json():[]).catch(()=>[]);
  return offIdx.then(a=>{
    if(!zone||!a.includes(k))return null;
    if(!(k in offCache))offCache[k]=fetch(`/assets/data/solat/${k}.json`).then(r=>r.ok?r.json():null).catch(()=>null);
    return offCache[k];
  });
}

/* ---------- hijri calendar (mirror tools/hijri.py): JAKIM's official months, tabular calendar + offset outside them ---------- */
const HJ=JSON.parse(($("#hd")||$("#tdat")||$("#zfd")||$("#zsdat"))?.textContent||"null");
const dnum=d=>Math.round(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())/864e5);
const dfrom=n=>{const u=new Date(n*864e5);return new Date(u.getUTCFullYear(),u.getUTCMonth(),u.getUTCDate())};
const HE=-492148,tabH2d=(y,m,d)=>d+Math.ceil(29.5*(m-1))+(y-1)*354+Math.floor((3+11*y)/30)+HE-1;
function tabD2h(n){const y=Math.floor((30*(n-HE)+10646)/10631),m=Math.min(12,Math.ceil((n-(29+tabH2d(y,1,1)))/29.5)+1);return[y,m,n-tabH2d(y,m,1)+1]}
function g2h(d){const n=dnum(d);for(const[y,m,s,l]of HJ.m)if(n>=s&&n<s+l)return[y,m,n-s+1,true];return[...tabD2h(n-HJ.off),false]}
// month rows: [hy, hm, start day, length, full]; a month cut by the end of the synced data has only its synced days (full 0)
function hMonthLen(y,m){const[ny,nm]=m===12?[y+1,1]:[y,m+1],tab=tabH2d(ny,nm,1)-tabH2d(y,m,1),r=HJ.m.find(x=>x[0]===y&&x[1]===m);return r?(r[4]?[r[3],true]:[Math.max(r[3],tab),false]):[tab,false]}
function h2g(y,m,d){const r=HJ.m.find(x=>x[0]===y&&x[1]===m);return r?[dfrom(r[2]+d-1),!!r[4]||d<=r[3]]:[dfrom(tabH2d(y,m,d)+HJ.off),false]}
// the Hijri pages follow Malaysian time (UTC+8) whatever the device's time zone, like the JAKIM timetable they read
const mytNow=()=>new Date(Date.now()+288e5),mytDay=()=>{const u=mytNow();return new Date(u.getUTCFullYear(),u.getUTCMonth(),u.getUTCDate())};
const hstr=h=>`${h[2]} ${HJ.bh[h[1]-1]} ${h[0]} H`;
function hEvents(d,n){
  const hy=g2h(d)[0],out=[];
  for(const y of[hy,hy+1,hy+2])for(const[k,m,dd,name,note]of HJ.ev){const[g,o]=h2g(y,m,dd);if(g>=d)out.push([k,name,note,[y,m,dd],g,o])}
  return out.sort((a,b)=>a[4]-b[4]).slice(0,n);
}
function hMarks(d){
  const[,hm,hd]=g2h(d),m=[],wd=d.getDay();
  if((hm===10&&hd===1)||(hm===12&&hd>=10&&hd<=13))m.push("h");
  else if(hm===9)m.push("r");
  else if((hm===12&&hd===9)||(hm===1&&(hd===9||hd===10))||(hd>=13&&hd<=15))m.push("a");
  else if(hm===10&&hd>=2)m.push("s");
  if((wd===1||wd===4)&&!m.includes("h")&&!m.includes("r"))m.push("w");
  if(HJ.ev.some(([,em,ed])=>em===hm&&ed===hd))m.push("e");
  return m;
}

/* ---------- waktu solat ---------- */
const sw=$("#sw");
if(sw){
  const S=JSON.parse($("#sd").textContent),C=S.c,NM=S.n,day=(y,m,d,lat,lng)=>solatDay(y,m,d,lat,lng,S.fa,S.is,S.tz);
  const sel=$("#sc"),list=$("#stimes"),tb=$("#smon tbody"),nx=$("#snext"),src=$("#ssrc"),hij=$("#shij"),qb=$("#sqib"),cap=$("#smcap"),dt0=$("#sdate");
  let cur=null;
  // JAKIM e-solat answers browsers directly; imsak is derived as Subuh - 10 because some zones (PLS01) publish it equal to Subuh (as the ilmualam.com widget does); cached per zone and month for offline use
  const MON={jan:0,feb:1,mar:2,mac:2,apr:3,may:4,mei:4,jun:5,jul:6,aug:7,ogo:7,sep:8,oct:9,okt:9,nov:10,dec:11,dis:11};
  const mn=v=>{const[h,m]=String(v).split(":");return +h*60+ +m};
  function live(zone,y,m){
    if(!zone)return Promise.resolve(null);
    const key=`esolat:${zone}-${y}-${m}`,hit=store.get(key,null);if(hit)return Promise.resolve(hit);
    const ac=new AbortController();setTimeout(()=>ac.abort(),8000);
    return fetch(`${S.api}${zone}`,{signal:ac.signal}).then(r=>r.ok?r.json():null).then(d=>{
      const out={t:[],h:[]},dim=new Date(y,m+1,0).getDate();
      for(const p of (d&&d.prayerTime)||[]){const[dd,mm,yy]=p.date.split("-");if(+yy!==y||MON[mm.toLowerCase().slice(0,3)]!==m)continue;
        const f=mn(p.fajr);out.t[+dd-1]=[f-10,f,mn(p.syuruk),mn(p.dhuhr),mn(p.asr),mn(p.maghrib),mn(p.isha)];out.h[+dd-1]=p.hijri||""}
      const ok=out.t.length===dim&&out.t.every(t=>t&&t[1]>=240&&t[1]<=400&&t.every((x,k)=>!k||x>t[k-1]));
      if(!ok)return null;store.set(key,out);return out;
    }).catch(()=>null);
  }
  let seq=0;
  function draw(loc,get,hijri,label){
    const d=today(),y=d.getFullYear(),m=d.getMonth(),t=get(d);cur={loc,t};
    setIf(list,NM.map((n,i)=>`<li data-i="${i}"><span class="sn">${n}</span><span class="st">${hm(t[i])}</span></li>`).join(""));
    setIf(dt0,`${dlong(d)} · ${esc(loc.name)}`);
    setIf(src,label?`Sumber: <strong>jadual rasmi JAKIM</strong>, ${label}.`:`Sumber: <strong>kiraan anggaran</strong> parameter JAKIM untuk ${esc(loc.name)}. Boleh berbeza beberapa minit daripada jadual rasmi; semak <a href="https://www.e-solat.gov.my/" rel="noopener">e-solat.gov.my</a>.`);
    let rows="";const dim=new Date(y,m+1,0).getDate();
    for(let k=1;k<=dim;k++){const r=get(new Date(y,m,k));rows+=`<tr${k===d.getDate()?' class="today"':""}><td>${k} ${BLS[m]}</td>${r.map(x=>`<td>${hm(x)}</td>`).join("")}</tr>`}
    setIf(tb,rows);setIf(cap,`Jadual waktu solat ${BLN[m]} ${y} – ${esc(loc.name)}`);
    setIf(qb,`${qibla(loc.lat,loc.lng).toFixed(1)}°`);
    if(hij){const h=hijri&&hijri(d);let s="";
      if(h){const[hy,hmn,hd]=h.split("-").map(Number);s=`${hd} ${S.hb[hmn-1]} ${hy} H`}
      else{try{s=new Intl.DateTimeFormat("ms-MY-u-ca-islamic-umalqura",{day:"numeric",month:"long",year:"numeric"}).format(d)+" (anggaran)"}catch{}}
      hij.textContent=s}
    tick();
  }
  async function render(loc){
    const my=++seq,d=today(),y=d.getFullYear(),m=d.getMonth();
    // calculated times first (identical to the build-time HTML), upgraded in place when official data arrives
    draw(loc,dd=>day(dd.getFullYear(),dd.getMonth()+1,dd.getDate(),loc.lat,loc.lng),null,"");
    const off=await official(loc.zone,y);if(my!==seq)return;
    if(off)return draw(loc,dd=>off.t[doy(dd)],dd=>off.h[doy(dd)],`zon ${loc.zone} (${esc(off.src)})`);
    const lv=await live(loc.zone,y,m);if(my!==seq||!lv)return;
    draw(loc,dd=>lv.t[dd.getDate()-1],dd=>lv.h[dd.getDate()-1],`zon ${loc.zone} (e-solat.gov.my)`);
  }
  function tick(){
    if(!cur)return;const n=new Date(),mins=n.getHours()*60+n.getMinutes(),t=cur.t;
    let i=[1,3,4,5,6].find(k=>t[k]>mins);
    $$("li",list).forEach(li=>li.classList.toggle("nx",+li.dataset.i===i));
    if(i===undefined){nx.textContent="Waktu seterusnya: Subuh esok";return}
    const left=t[i]-mins,h=Math.floor(left/60),mm=left%60;
    nx.textContent=`Waktu seterusnya: ${NM[i]} ${hm(t[i])} · lagi ${h?h+" jam ":""}${mm} minit`;
  }
  setInterval(tick,20000);
  const byslug=s=>{const c=C.find(x=>x[0]===s);return c&&{slug:c[0],name:c[1],lat:c[3],lng:c[4],zone:c[5]}};
  const DEF=S.def||"kuala-lumpur",KEY=S.key||"solat";
  function pick(slug,save){const l=byslug(slug)||byslug(DEF);sel.value=l.slug;if(save){store.set(KEY,l.slug);writeHash({bandar:l.slug})}render(l)}
  sel.addEventListener("change",()=>pick(sel.value,true));
  $("#sgeo").addEventListener("click",()=>{
    if(!navigator.geolocation)return toast("Lokasi tidak disokong");
    navigator.geolocation.getCurrentPosition(p=>{
      const{latitude:la,longitude:lo}=p.coords;let best=null,bd=1e9;
      for(const c of C){const dd=(c[3]-la)**2+((c[4]-lo)*Math.cos(rad(la)))**2;if(dd<bd){bd=dd;best=c}}
      const near=Math.sqrt(bd)*111<40;
      render({slug:"",name:near?`${best[1]} (lokasi anda)`:`Lokasi anda (${la.toFixed(2)}, ${lo.toFixed(2)})`,lat:la,lng:lo,zone:near?best[5]:""});
      toast(near?`Zon terdekat: ${best[1]}`:"Waktu dikira untuk koordinat anda");
    },()=>toast("Kebenaran lokasi ditolak"),{timeout:10000,maximumAge:6e5});
  });
  toolbar($("#sact"),{});
  const h=readHash();pick(byslug(h.bandar)?h.bandar:store.get(KEY,DEF),false);
  // state pages: today's official times for every zone in the state (build-time values, refreshed for today's date)
  const zt=$("#szt");
  if(zt){zt.addEventListener("click",e=>{const a=e.target.closest("a[data-zone]");if(!a)return;e.preventDefault();pick(a.dataset.zone,true);$("#kira").scrollIntoView({block:"start"})});const d=today(),y=d.getFullYear();
    $$("tr[data-z]",zt).forEach(async tr=>{const o=await official(tr.dataset.z,y);if(!o)return;const t=o.t[doy(d)];
      $$("td[data-k]",tr).forEach(td=>{const v=hm(t[+td.dataset.k]);if(td.textContent!==v)td.textContent=v})});
    const zd=$("#sztd");if(zd)setIf(zd,dlong(d));
  }
}
function saveFile(text,file){
  const blob=new Blob([text],{type:"text/calendar;charset=utf-8"}),a=document.createElement("a");
  a.href=URL.createObjectURL(blob);a.download=file;document.body.appendChild(a);a.click();
  setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1000);toast("Fail kalendar dimuat turun ✓");
}
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
// the device's own Arabic voice, when it has one (never a network service)
const speech={v:null,init(cb){const s=window.speechSynthesis;if(!s)return;const f=()=>{this.v=s.getVoices().find(v=>/^ar([-_]|$)/i.test(v.lang))||null;cb&&cb(!!this.v)};f();s.addEventListener?.("voiceschanged",f)},
  say(t){const s=window.speechSynthesis;if(!s||!this.v)return;s.cancel();const u=new SpeechSynthesisUtterance(t);u.voice=this.v;u.lang=this.v.lang;u.rate=.7;s.speak(u)}};

/* ---------- cari masjid: zone prayer times + nearest mosques from OpenStreetMap (Overpass; same rules as tools/masjid.py) ---------- */
const mdEl=$("#md");
if(mdEl){
  const D=JSON.parse(mdEl.textContent),NM=D.n,mt=$("#mtimes");
  if(mt&&D.z){
    // the build-time HTML shows the build date; redraw for today from the synced JAKIM file (else the calibrated calculation)
    const md=$("#mdate"),rest=md.textContent.split(" · ").slice(1).join(" · ");let t=null;
    const tick=()=>{
      if(!t)return;const n=new Date(),mins=n.getHours()*60+n.getMinutes(),i=[1,3,4,5,6].find(k=>t[k]>mins);
      $$("li",mt).forEach(li=>li.classList.toggle("nx",+li.dataset.i===i));
      if(i===undefined){$("#mnext").textContent="Waktu seterusnya: Subuh esok";return}
      const left=t[i]-mins,h=Math.floor(left/60);$("#mnext").textContent=`Waktu seterusnya: ${NM[i]} ${hm(t[i])} · lagi ${h?h+" jam ":""}${left%60} minit`;
    };
    const d=today();
    official(D.z,d.getFullYear()).then(o=>{
      t=o?o.t[doy(d)]:solatDay(d.getFullYear(),d.getMonth()+1,d.getDate(),D.lat,D.lng);
      setIf(mt,NM.map((n,i)=>`<li data-i="${i}"><span class="sn">${n}</span><span class="st">${hm(t[i])}</span></li>`).join(""));
      md.textContent=`${dlong(d)} · ${rest}`;
      if(!o){const s=$("#msrc strong");if(s)s.textContent=`kiraan anggaran parameter JAKIM, zon ${D.z}`}
      tick();
    });
    setInterval(tick,20000);
  }
  const btn=$("#mgeo"),res=$("#mres"),stat=$("#mstat");
  const SUR=/\b(surau|musolla|musalla|musholla|musolah|mushola|madrasah|madrasatul)\b/i,MAS=/\b(masjid|mosque|jami|jamek)\b/i,KIND={m:"Masjid",s:"Surau",t:"Tempat solat"};
  const kindOf=(n,tg)=>SUR.test(n)?"s":MAS.test(n)||tg.building==="mosque"?"m":"t";
  const km=(a,b,c,d)=>{const h=Math.sin(rad(c-a)/2)**2+Math.cos(rad(a))*Math.cos(rad(c))*Math.sin(rad(d-b)/2)**2;return 12742*Math.asin(Math.sqrt(h))};
  const kmf=x=>x<1?`${Math.round(x*1000)} m`:`${x.toFixed(1).replace(".",",")} km`;
  const sp=s=>String(s||"").trim().replace(/\s+/g," ");
  const EP=["https://overpass-api.de/api/interpreter","https://overpass.kumi.systems/api/interpreter"];
  async function ask(q){
    for(const u of EP){
      const ac=new AbortController(),tm=setTimeout(()=>ac.abort(),25000);
      try{const r=await fetch(u,{method:"POST",body:"data="+encodeURIComponent(q),headers:{"Content-Type":"application/x-www-form-urlencoded"},signal:ac.signal});if(r.ok)return(await r.json()).elements||[]}catch{}finally{clearTimeout(tm)}
    }
    throw new Error("overpass");
  }
  async function near(la,lo){
    for(const r of[3000,10000,25000]){
      stat.textContent=`Mencari masjid dan surau dalam lingkungan ${r/1000} km…`;
      const f=`(around:${r},${la.toFixed(5)},${lo.toFixed(5)})`,out=[];
      for(const el of await ask(`[out:json][timeout:25];(nwr["amenity"="place_of_worship"]["religion"="muslim"]${f};nwr["building"="mosque"]${f};);out center tags qt;`)){
        const tg=el.tags||{},n=sp(tg.name||tg["name:ms"]||tg["name:en"]),lat=el.lat??el.center?.lat,lng=el.lon??el.center?.lon;
        if(!n||lat==null||out.some(o=>o.n.toLowerCase()===n.toLowerCase()&&km(o.lat,o.lng,lat,lng)<.15))continue;
        const addr=[sp([tg["addr:housenumber"],tg["addr:street"]].filter(Boolean).join(" ")),sp(tg["addr:place"]||tg["addr:suburb"]),sp([tg["addr:postcode"],tg["addr:city"]].filter(Boolean).join(" "))].filter(Boolean).join(", ");
        out.push({n,k:kindOf(n,tg),lat,lng,d:km(la,lo,lat,lng),ref:`${el.type}/${el.id}`,addr,a:tg.wheelchair==="yes"});
      }
      if(out.length>=5||r===25000)return{r,out:out.sort((a,b)=>a.d-b.d).slice(0,25)};
    }
  }
  const li=m=>`<li class="mq" data-lat="${m.lat}" data-lng="${m.lng}"><span class="mk ${m.k}">${KIND[m.k]}</span><strong class="mqn">${esc(m.n)}</strong><span class="mqd">${kmf(m.d)} dari lokasi anda${m.a?" · ♿ akses OKU":""}</span>${m.addr?`<span class="mqa">${esc(m.addr)}</span>`:""}<span class="mql"><a href="https://www.google.com/maps/dir/?api=1&amp;destination=${m.lat.toFixed(6)},${m.lng.toFixed(6)}" rel="noopener nofollow">Arah</a> · <a href="https://www.openstreetmap.org/${m.ref}" rel="noopener">Peta OSM</a></span></li>`;
  function zoneAt(la,lo){let best=null,bd=1e9;for(const a of D.an){const x=km(la,lo,a[1],a[2]);if(x<bd){bd=x;best=a[0]}}return bd<60?best:null}
  btn.addEventListener("click",()=>{
    if(!navigator.geolocation)return toast("Lokasi tidak disokong");
    btn.disabled=true;stat.textContent="Mendapatkan lokasi anda…";
    navigator.geolocation.getCurrentPosition(async p=>{
      const{latitude:la,longitude:lo}=p.coords,z=zoneAt(la,lo);
      const zt=z?` Zon waktu solat anda: ${z===D.z?`<strong>${z}</strong> (halaman ini)`:`<a href="${D.zs[z][0]}">${z} · ${esc(D.zs[z][1])}</a>`}.`:"";
      try{
        const{r,out}=await near(la,lo);
        setIf(res,out.map(li).join(""));
        stat.innerHTML=(out.length?`${out.length} tempat solat terdekat dalam ${r/1000} km, disusun mengikut jarak garis lurus.`:`Tiada masjid atau surau dipetakan dalam ${r/1000} km.`)+zt+` © <a href="https://www.openstreetmap.org/copyright" rel="noopener">penyumbang OpenStreetMap</a>`;
      }catch{stat.innerHTML="Carian OpenStreetMap tidak berjaya buat masa ini. Cuba lagi sebentar"+(mt?", atau lihat senarai zon di bawah.":".")+zt}
      btn.disabled=false;
    },()=>{btn.disabled=false;stat.textContent="Kebenaran lokasi ditolak. Benarkan lokasi dalam tetapan pelayar, atau pilih zon anda di bawah.";toast("Kebenaran lokasi ditolak")},{timeout:15000,maximumAge:3e5,enableHighAccuracy:true});
  });
}

/* ---------- kalendar hijrah (HTML mirrors tools/pages6.py + tools/hijri.py) ---------- */
const hgEl=$("#hgrid");
if(hgEl&&HJ){
  const AD=s=>String(s).replace(/\d/g,c=>"٠١٢٣٤٥٦٧٨٩"[c]),BHA=["مُحَرَّم","صَفَر","رَبِيعُ الأَوَّل","رَبِيعُ الآخِر","جُمَادَى الأُولَى","جُمَادَى الآخِرَة","رَجَب","شَعْبَان","رَمَضَان","شَوَّال","ذُو القَعْدَة","ذُو الحِجَّة"];
  const BH=HJ.bh;
  function gridHtml(y,mo,td){
    const first=new Date(y,mo,1),nd=new Date(y,mo+1,0).getDate();
    let s=["Ahd","Isn","Sel","Rab","Kha","Jum","Sab"].map(x=>`<span class="hw">${x}</span>`).join("")+'<span class="hc x"></span>'.repeat(first.getDay());
    for(let k=1;k<=nd;k++){const d=new Date(y,mo,k),[,hm,hd,o]=g2h(d),mk=hMarks(d);
      const cls=["hc",...mk.map(x=>"m"+x),...(iso(d)===iso(td)?["td"]:[])].join(" ");
      s+=`<span class="${cls}" data-d="${iso(d)}"><b>${k}</b><i>${hd}${o?"":"*"}</i>${hd===1||k===1?`<span class="hm">${BH[hm-1]}</span>`:""}</span>`}
    return s;
  }
  function monTitle(y,mo){
    const a=g2h(new Date(y,mo,1)),b=g2h(new Date(y,mo+1,0));
    const span=a[0]===b[0]&&a[1]===b[1]?`${BH[a[1]-1]} ${a[0]} H`:a[0]===b[0]?`${BH[a[1]-1]} – ${BH[b[1]-1]} ${b[0]} H`:`${BH[a[1]-1]} ${a[0]} – ${BH[b[1]-1]} ${b[0]} H`;
    return`${BLN[mo]} ${y} · ${span}`;
  }
  const evRows=d=>hEvents(d,12).map(([k,name,note,h,g,o])=>{const n=Math.round((g-d)/864e5);
    return`<tr data-k="${k}"><td><strong>${name}</strong><span class="za">${note}</span></td><td>${hstr(h)}</td><td>${dlong(g)}${o?"":"*"}</td><td>${n===0?"Hari ini":`lagi ${n} hari`}</td></tr>`}).join("");
  function sunatList(d){
    const out=[];
    for(let i=0;i<60&&out.length<6;i++){const x=addD(d,i);if(!hMarks(x).includes("a"))continue;const h=g2h(x);
      const why=h[1]===12&&h[2]===9?"Hari Arafah":h[1]===1&&h[2]===9?"Tasu'a":h[1]===1&&h[2]===10?"Asyura":"Ayyamul Bidh";
      out.push(`<li><strong>${dshort(x)}</strong> · ${hstr(h)} · ${why}</li>`)}
    return out.join("");
  }
  const zs=$("#hz");let cy,cm,zone=store.get("hijri-zone",HJ.def);if(!HJ.zc[zone])zone=HJ.def;zs.value=zone;
  async function drawToday(){
    const d=mytDay(),h=g2h(d),nh=g2h(addD(d,1)),o=await official(zone,d.getFullYear()),z=HJ.zc[zone];
    const t=o?o.t[doy(d)]:solatDay(d.getFullYear(),d.getMonth()+1,d.getDate(),z[0],z[1]),u=mytNow(),mins=u.getUTCHours()*60+u.getUTCMinutes();
    setIf($("#hbig"),hstr(h));setIf($("#hans"),hstr(h));setIf($("#har"),`${AD(h[2])} ${BHA[h[1]-1]} ${AD(h[0])} هـ`);
    setIf($("#hmas"),`${dlong(d)} · ${h[3]?"takwim rasmi JAKIM":"anggaran kiraan (takwim JAKIM belum tersedia)"}`);
    setIf($("#hmag"),mins>=t[5]?`Sudah masuk malam ${nh[2]} ${BH[nh[1]-1]} (selepas Maghrib ${hm(t[5])}, zon ${zone}).`:`Hari Hijrah bermula waktu Maghrib: selepas ${hm(t[5])} (zon ${zone}) masuk malam ${nh[2]} ${BH[nh[1]-1]}.`);
  }
  const drawGrid=()=>{setIf(hgEl,gridHtml(cy,cm,mytDay()));setIf($("#hmt"),monTitle(cy,cm))};
  function goto(y,m,save){const d=new Date(y,m,1);cy=d.getFullYear();cm=d.getMonth();drawGrid();if(save)writeHash({bulan:`${cy}-${pad(cm+1)}`})}
  $("#hprev").addEventListener("click",()=>goto(cy,cm-1,true));$("#hnext").addEventListener("click",()=>goto(cy,cm+1,true));
  $("#htod").addEventListener("click",()=>{const d=mytDay();goto(d.getFullYear(),d.getMonth(),false);history.replaceState(null,"",location.pathname)});
  zs.addEventListener("change",()=>{zone=zs.value;store.set("hijri-zone",zone);drawToday()});
  // converter
  const hg=$("#hg"),hhd=$("#hhd"),hhm=$("#hhm"),hhy=$("#hhy");
  const conv1=()=>{const d=parseD(hg.value);if(!d)return;const h=g2h(d);setIf($("#hgo"),`${iso(d)} = <strong>${hstr(h)}</strong>${h[3]?"":" (anggaran)"}`)};
  const conv2=()=>{const y=clamp(hhy.value,1,1600,0),m=+hhm.value,d=+hhd.value;if(!y)return;const[ln]=hMonthLen(y,m);
    if(d>ln)return setIf($("#hho"),`${BH[m-1]} ${y} H hanya ada ${ln} hari.`);const[g,o]=h2g(y,m,d);setIf($("#hho"),`${hstr([y,m,d])} = <strong>${dlong(g)}</strong>${o?"":" (anggaran)"}`)};
  hg.addEventListener("input",conv1);[hhd,hhm,hhy].forEach(x=>x.addEventListener("input",conv2));
  // Hijri age, next Hijri birthday, zakat haul
  const nextH=(m,dd,from)=>{for(let y=g2h(from)[0];;y++){const[g]=h2g(y,m,Math.min(dd,hMonthLen(y,m)[0]));if(g>=from)return[g,y]}};
  $("#hlahir").addEventListener("input",e=>{const b=parseD(e.target.value),t=mytDay();if(!b||b>t)return;
    const hb=g2h(b),ht=g2h(t),ah=ht[0]-hb[0]-((ht[1]<hb[1]||(ht[1]===hb[1]&&ht[2]<hb[2]))?1:0);
    const am=t.getFullYear()-b.getFullYear()-((t.getMonth()<b.getMonth()||(t.getMonth()===b.getMonth()&&t.getDate()<b.getDate()))?1:0);
    const[g,y]=nextH(hb[1],hb[2],t),n=Math.round((g-t)/864e5);
    setIf($("#hlo"),`<p>Tarikh lahir Hijrah: <strong>${hstr(hb)}</strong>${hb[3]?"":" (anggaran)"}.</p><p>Umur: <strong>${ah} tahun Hijrah</strong> (${am} tahun Masihi).</p><p>Hari lahir Hijrah seterusnya (${hb[2]} ${BH[hb[1]-1]} ${y} H): <strong>${dlong(g)}</strong>${n?`, lagi ${n} hari`:", hari ini"}.</p>`)});
  $("#hhaul").addEventListener("input",e=>{const s=parseD(e.target.value);if(!s)return;const h=g2h(s),y=h[0]+1,[g,o]=h2g(y,h[1],Math.min(h[2],hMonthLen(y,h[1])[0])),n=Math.round((g-mytDay())/864e5);
    setIf($("#hho2"),`<p>Mula: ${hstr(h)}. Haul cukup pada <strong>${dlong(g)}</strong> (${hstr(g2h(g))})${o?"":", anggaran"}, ${Math.round((g-s)/864e5)} hari kemudian${n>0?`, lagi ${n} hari`:n===0?", iaitu hari ini":""}.</p>`)});
  $("#hics").addEventListener("click",()=>{
    const d=mytDay(),ev=hEvents(d,24).map(([,name,note,h,g])=>({d:g,t:name,x:`${hstr(h)}. ${note}`}));
    for(let i=0;i<366;i++){const x=addD(d,i),h=g2h(x);if(h[2]>=13&&h[2]<=15&&!(h[1]===12&&h[2]===13)&&h[1]!==9)ev.push({d:x,t:`Puasa sunat Ayyamul Bidh (${h[2]} ${BH[h[1]-1]})`,x:"Sunat berpuasa 13, 14 dan 15 setiap bulan Hijrah."})}
    saveFile(icsCal(ev.sort((a,b)=>a.d-b.d)),`kalendar-hijrah-${d.getFullYear()}.ics`);
  });
  toolbar($("#hact"),{});
  const d0=mytDay(),hb=readHash().bulan&&/^(\d{4})-(\d{2})$/.exec(readHash().bulan);
  if(hb)goto(+hb[1],+hb[2]-1,false);else goto(d0.getFullYear(),d0.getMonth(),false);
  setIf($("#hev tbody"),evRows(d0));setIf($("#hsl"),sunatList(d0));
  if(hg.value!==iso(d0)){hg.value=iso(d0);conv1();const h=g2h(d0);hhd.value=h[2];hhm.value=h[1];hhy.value=h[0];conv2()}
  drawToday();setInterval(drawToday,60000);
}

/* ---------- tahlil ringkas: name + pronoun of the deceased, haul, view, audio, print, majlis mode (texts mirror tools/tahlil.py) ---------- */
const tlEl=$("#tls");
if(tlEl&&HJ){
  const TD=HJ,sec=$("#bacaan"),nm=$("#tln"),bp=$("#tlb"),jj=$("#tlj"),td=$("#tld");
  function hadiah(j,nama,bapa){
    const[t,b]=TD.gel[j];
    const who=j==="ll"||j==="pp"?`roh-roh ${nama.trim()||"ahli keluarga kami"} yang telah kembali ke rahmatullah`
      :"roh "+[t,nama.trim()||"[nama arwah]",bapa.trim()?`${b} ${bapa.trim()}`:""].filter(Boolean).join(" ");
    return`Ke hadrat Nabi Muhammad SAW, keluarga dan sahabat baginda, para nabi dan rasul, para wali dan ulama, kedua ibu bapa kami, seluruh muslimin dan muslimat, dan khususnya kepada ${who}: Al-Fatihah.`;
  }
  function update(save){
    const j=TD.doa[jj.value]?jj.value:"l",n=nm.value,b=bp.value,[t,bb]=TD.gel[j],[ar,ru,mn]=TD.doa[j];
    $("#tlh").textContent=hadiah(j,n,b);$("#tlda").textContent=ar;$("#tldr").textContent=ru;$("#tldm").textContent=mn;
    $("#tlcn").textContent=j==="ll"||j==="pp"?(n.trim()||"Arwah ahli keluarga kami"):[t,n.trim()||"[nama arwah]",b.trim()?`${bb} ${b.trim()}`:""].filter(Boolean).join(" ");
    const doaLi=$("#doa");doaLi.dataset.txt=`Doa untuk arwah\n\n${ar}\n\n${ru}\n\n${mn}`;
    const d=parseD(td.value),hl=$("#tlhaul");
    if(d&&d<=mytDay()){
      const h=g2h(d),now=mytDay();let y=g2h(now)[0]-1,g;
      do{y++;g=h2g(y,h[1],Math.min(h[2],hMonthLen(y,h[1])[0]))[0]}while(g<now);
      const left=Math.round((g-now)/864e5);
      hl.innerHTML=`Meninggal: <strong>${hstr(h)}</strong>${h[3]?"":" (anggaran)"} (jika selepas Maghrib, tarikh Hijrahnya sehari kemudian). Haul seterusnya: <strong>${dlong(g)}</strong>, ${h[2]} ${TD.bh[h[1]-1]} ${y} H${left?`, lagi ${left} hari`:", hari ini"}.`;
      $("#tlcd").textContent=`${dlong(d)} · ${hstr(h)}`;
    }else{hl.textContent="Masukkan tarikh meninggal untuk tarikh Hijrah dan tarikh haul arwah.";$("#tlcd").textContent=""}
    if(save)store.set("tahlil",{n,b,j,t:td.value});
  }
  const h0=readHash(),s0=h0.nama!=null||h0.j?{n:h0.nama||"",b:h0.bapa||"",j:h0.j||"l",t:h0.t||""}:store.get("tahlil",{n:"",b:"",j:"l",t:""});
  nm.value=s0.n||"";bp.value=s0.b||"";jj.value=TD.doa[s0.j]?s0.j:"l";td.value=parseD(s0.t)?s0.t:"";
  $("#tlf").addEventListener("input",()=>update(true));update(false);
  $("#tlshare").addEventListener("click",()=>{
    const o={nama:nm.value.trim(),j:jj.value};if(bp.value.trim())o.bapa=bp.value.trim();if(td.value)o.t=td.value;
    const url=`${location.origin}${location.pathname}#${new URLSearchParams(o)}`,txt=`Bacaan tahlil untuk ${$("#tlcn").textContent}:`;
    if(navigator.share)navigator.share({title:"Tahlil Ringkas",text:txt,url}).catch(()=>{});else copy(`${txt} ${url}`,"Pautan tahlil disalin ✓");
  });
  // view + font size
  const views=["","ar-ru","ar","ru"];let v=store.get("tahlil-v","");if(!views.includes(v))v="";
  const setV=x=>{v=x;views.forEach(k=>k&&sec.classList.toggle("v-"+k,k===v));$$("#tlv button").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.v===v)));store.set("tahlil-v",v)};
  $("#tlv").addEventListener("click",e=>{const b=e.target.closest("button[data-v]");if(b)setV(b.dataset.v)});setV(v);
  let fs=clamp(store.get("tahlil-fs",0),-2,4,0);const setFs=()=>{sec.style.setProperty("--tlz",String(1+fs*.15));store.set("tahlil-fs",fs)};setFs();
  $("#tlact").addEventListener("click",e=>{const b=e.target.closest("button[data-fs]");if(b){fs=clamp(fs+ +b.dataset.fs,-2,4,0);setFs()}});
  $("#tlprint").addEventListener("click",()=>print());
  // audio: EveryAyah, one ayah after another
  const au=new Audio();let queue=[],playing=null;
  const stopA=()=>{au.pause();queue=[];if(playing)playing.textContent="▶ Dengar";playing=null;$("#tlplay").textContent="▶ Dengar semua ayat"};
  const next=()=>{const r=queue.shift();if(!r)return stopA();const[s,a]=r.split(":");au.src=`https://everyayah.com/data/Alafasy_128kbps/${pad3(s)}${pad3(a)}.mp3`;au.play().catch(stopA)};
  const pad3=x=>String(x).padStart(3,"0");
  au.addEventListener("ended",next);au.addEventListener("error",()=>{toast("Audio tidak dapat dimainkan");stopA()});
  tlEl.addEventListener("click",e=>{const b=e.target.closest("button[data-play]");if(!b)return;const was=playing===b;stopA();if(was)return;playing=b;b.textContent="■ Henti";queue=b.dataset.play.split(" ");next()});
  $("#tlplay").addEventListener("click",e=>{if(queue.length||!au.paused){stopA();return}stopA();queue=$$("button[data-play]",tlEl).flatMap(b=>b.dataset.play.split(" "));e.currentTarget.textContent="■ Henti audio";next()});
  // majlis mode: one reading at a time, large text, screen kept on
  const items=$$("li.tls",tlEl),nav=$("#tlnav");let idx=0,lock=null,big=false;
  const show=i=>{idx=Math.max(0,Math.min(items.length-1,i));items.forEach((li,k)=>li.classList.toggle("on",k===idx));$("#tlpos").textContent=`${idx+1} / ${items.length}`;window.scrollTo(0,0)};
  async function setBig(on){
    big=on;document.body.classList.toggle("tlbig",on);nav.hidden=!on;
    if(on){show(idx);try{lock=await navigator.wakeLock?.request("screen")}catch{}try{await document.documentElement.requestFullscreen?.()}catch{}}
    else{items.forEach(li=>li.classList.remove("on"));lock?.release?.();lock=null;if(document.fullscreenElement)document.exitFullscreen?.().catch(()=>{});items[idx]?.scrollIntoView({block:"start"})}
  }
  $("#tlbig").addEventListener("click",()=>setBig(true));
  nav.addEventListener("click",e=>{const b=e.target.closest("button[data-nav]");if(!b)return;const n=+b.dataset.nav;n?show(idx+n):setBig(false)});
  tlEl.addEventListener("click",e=>{if(big&&!e.target.closest("button,a"))show(idx+1)});
  document.addEventListener("keydown",e=>{if(!big)return;if(["ArrowRight","ArrowDown","PageDown"," "].includes(e.key)){e.preventDefault();show(idx+1)}else if(["ArrowLeft","ArrowUp","PageUp"].includes(e.key)){e.preventDefault();show(idx-1)}else if(e.key==="Escape")setBig(false)});
  document.addEventListener("fullscreenchange",()=>{if(big&&!document.fullscreenElement)setBig(false)});
}

/* ---------- waktu berbuka puasa: imsakiyah Ramadan (rows mirror tools/pages4.py r_row) ---------- */
const rdEl=$("#rd");
if(rdEl){
  const D=JSON.parse(rdEl.textContent),Z=D.z,start=parseD(D.start),N=D.n,KEY="puasa:"+D.y;
  const sel=$("#rz"),tb=$("#rmt tbody"),cap=$("#rcap"),src=$("#rsrc"),ph=$("#rph"),cd=$("#rcd"),td=$("#rtd"),tdl=$("#rtdl"),zl=$("#rzl"),prog=$("#rprog");
  const days=Array.from({length:N},(_,i)=>addD(start,i));
  const zone=c=>{const z=Z.find(x=>x[0]===c);return z&&{code:z[0],area:z[2],lat:z[3],lng:z[4]}};
  const calc=(z,d)=>solatDay(d.getFullYear(),d.getMonth()+1,d.getDate(),z.lat,z.lng,D.fa,D.is,D.tz);
  const dur=t=>{const m=t[5]-t[1];return`${Math.floor(m/60)}j ${pad(m%60)}m`};
  const dayN=d=>Math.round((d-start)/864e5);
  let cur=null,seq=0;
  function row(k,d,t,now){
    const star=k>=21&&k%2?' <span class="lq" title="Malam ganjil 10 terakhir">★</span>':"",mark=k===30&&!D.off?"*":"";
    return`<tr data-d="${k}"${iso(d)===iso(now)?' class="today"':""}><td>${k}${mark}${star}</td><td>${dshort(d)}</td>${[0,1,3,4].map(i=>`<td>${hm(t[i])}</td>`).join("")}<td><strong>${hm(t[5])}</strong></td><td>${hm(t[6])}</td><td>${dur(t)}</td><td><input type="checkbox" data-r="${k}" aria-label="Puasa hari ke-${k} selesai"></td></tr>`;
  }
  function srcText(nOff,code){
    if(nOff===N)return`Sumber: <strong>jadual rasmi JAKIM</strong>, zon ${code}.`;
    if(!nOff)return`Sumber: <strong>kiraan anggaran</strong> parameter JAKIM bagi zon ${code} (biasanya dalam lingkungan 1–2 minit). Jadual rasmi JAKIM menggantikannya secara automatik sebaik sahaja diterbitkan.`;
    return`Sumber: <strong>jadual rasmi JAKIM</strong> bagi ${nOff} hari, selebihnya kiraan anggaran, zon ${code}.`;
  }
  function phase(now){
    const k=dayN(now);
    if(k<0)return`🌙 Ramadan ${D.y}H ${D.off?"bermula":"dijangka bermula"} <strong>${dlong(start)}</strong> · lagi ${-k} hari`;
    if(k<N)return`🌙 Hari ke-${k+1} Ramadan ${D.y}H · ${dlong(now)}`;
    return`🌙 Ramadan ${D.y}H telah berakhir. Selamat Hari Raya Aidilfitri, maaf zahir dan batin.`;
  }
  const marks=()=>new Set(store.get(KEY,[]));
  function paintTrack(){
    const st=marks(),past=days.filter(d=>d<today()).length,miss=days.slice(0,past).filter((_,i)=>!st.has(i+1)).length;
    $$("input[data-r]",tb).forEach(c=>c.checked=st.has(+c.dataset.r));
    prog.textContent=st.size||past?`✓ ${st.size} daripada ${N} hari puasa ditanda${miss?` · ${miss} hari lepas belum ditanda (semak jika perlu qada)`:""}`:"";
  }
  async function render(z){
    const my=++seq,now=today(),years=[...new Set([...days,now,addD(now,1)].map(d=>d.getFullYear()))];
    const draw=offs=>{
      const get=d=>{const o=offs[d.getFullYear()];return o?o.t[doy(d)]:calc(z,d)},rows=days.map(get),t=get(now);
      cur={z,rows,get};
      setIf(tb,days.map((d,i)=>row(i+1,d,rows[i],now)).join(""));
      setIf(cap,`Jadual imsakiyah Ramadan ${D.y}H (${start.getFullYear()}) – ${esc(z.code+" · "+z.area)}`);
      setIf(src,srcText(days.filter(d=>offs[d.getFullYear()]).length,z.code));
      setIf(zl,esc(z.code+" · "+z.area));setIf(tdl,`Hari ini, ${dlong(now)}`);setIf(ph,phase(now));
      setIf(td,[[0,"Imsak"],[1,"Subuh"],[5,"Maghrib"],[6,"Isyak"]].map(([i,n])=>`<li><span>${n}</span><strong>${hm(t[i])}</strong></li>`).join(""));
      paintTrack();tick();
    };
    draw({});
    const got=await Promise.all(years.map(y=>official(z.code,y)));if(my!==seq)return;
    const offs={};years.forEach((y,i)=>{if(got[i])offs[y]=got[i]});
    if(Object.keys(offs).length)draw(offs);
  }
  const fmt=s=>{const h=Math.floor(s/3600),m=Math.floor(s%3600/60);return`${h?h+"j ":""}${pad(m)}m ${pad(s%60)}s`};
  function tick(){
    if(!cur)return;
    const n=new Date(),now=today(),sec=Math.floor((n-now)/1000),t=cur.get(now),k=dayN(now);let x;
    if(k>=0&&k<N){
      if(sec<t[0]*60)x=`⏳ Imsak (sahur berakhir) ${hm(t[0])} · lagi ${fmt(t[0]*60-sec)}`;
      else if(sec<t[5]*60)x=`🍽 Berbuka puasa ${hm(t[5])} · lagi ${fmt(t[5]*60-sec)}`;
      else x=k+1<N?`✅ Selamat berbuka! Imsak esok ${hm(cur.rows[k+1][0])}`:"✅ Selamat berbuka! Hari terakhir Ramadan; Aidilfitri bergantung pada rukyah malam ini.";
    }else if(sec<t[5]*60)x=`Maghrib hari ini ${hm(t[5])} · lagi ${fmt(t[5]*60-sec)} (puasa sunat)`;
    else x=`Maghrib hari ini ${hm(t[5])} · imsak esok ${hm(cur.get(addD(now,1))[0])}`;
    if(cd.textContent!==x)cd.textContent=x;
  }
  setInterval(tick,1000);
  function ics(imsak){
    const st=new Date().toISOString().replace(/[-:]/g,"").replace(/\.\d+/,""),z=cur.z.code;
    const at=(d,m)=>new Date(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate(),0,m-D.tz*60)).toISOString().replace(/[-:]/g,"").replace(/\.\d+/,"");
    const L=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Ilmu Alam//Al-Quran Online//MS","CALSCALE:GREGORIAN",`X-WR-CALNAME:${icsEsc(`Ramadan ${D.y}H – ${z}`)}`];
    const ev=(id,d,m,len,sum,desc,alarm)=>L.push("BEGIN:VEVENT",`UID:${iso(d)}-${id}-${z}@quran.ilmualam.com`,`DTSTAMP:${st}`,`DTSTART:${at(d,m)}`,`DURATION:PT${len}M`,
      `SUMMARY:${icsEsc(sum)}`,`DESCRIPTION:${icsEsc(desc)}`,"BEGIN:VALARM","ACTION:DISPLAY",`DESCRIPTION:${icsEsc(sum)}`,`TRIGGER:-PT${alarm}M`,"END:VALARM","END:VEVENT");
    days.forEach((d,i)=>{const t=cur.rows[i];
      if(imsak)ev("imsak",d,t[0],10,`Imsak ${hm(t[0])} – ${i+1} Ramadan`,`Sahur berakhir. Subuh ${hm(t[1])}. Zon ${z}.`,30);
      ev("berbuka",d,t[5],20,`Berbuka puasa ${hm(t[5])} – ${i+1} Ramadan`,`Maghrib zon ${z}. Doa: Zahabaz-zama'u wabtallatil-'uruqu wa thabatal-ajru insya-Allah. ${location.origin+location.pathname}`,10)});
    L.push("END:VCALENDAR");return L.join("\r\n");
  }
  function pick(c,save){const z=zone(c)||zone(D.def);sel.value=z.code;if(save){store.set(D.key,z.code);writeHash({zon:z.code})}render(z)}
  sel.addEventListener("change",()=>pick(sel.value,true));
  tb.addEventListener("change",e=>{const c=e.target.closest("input[data-r]");if(!c)return;const st=marks();c.checked?st.add(+c.dataset.r):st.delete(+c.dataset.r);store.set(KEY,[...st].sort((a,b)=>a-b));paintTrack()});
  toolbar($("#ract"),{});
  $("#ract").addEventListener("click",e=>{const b=e.target.closest("button[data-ics]");if(b&&cur)saveFile(ics(b.dataset.ics==="bi"),`ramadan-${D.y}-${cur.z.code}${b.dataset.ics==="bi"?"-imsak":""}.ics`)});
  $("#rgeo").addEventListener("click",()=>{
    if(!navigator.geolocation)return toast("Lokasi tidak disokong");
    navigator.geolocation.getCurrentPosition(p=>{const{latitude:la,longitude:lo}=p.coords;let best=Z[0],bd=1e9;
      for(const c of Z){const dd=(c[3]-la)**2+((c[4]-lo)*Math.cos(rad(la)))**2;if(dd<bd){bd=dd;best=c}}
      pick(best[0],true);toast(`Zon terdekat: ${best[0]}`)},()=>toast("Kebenaran lokasi ditolak"),{timeout:10000,maximumAge:6e5});
  });
  const zt=$("#szt");
  if(zt)zt.addEventListener("click",e=>{const a=e.target.closest("a[data-zone]");if(!a)return;e.preventDefault();pick(a.dataset.zone,true);$("#kira").scrollIntoView({block:"start"})});
  const h=readHash();pick(zone(h.zon)?h.zon:store.get(D.key,D.def),false);
}

/* ---------- belajar solat: step-by-step guide (cards mirror tools/pages4.py sp_card) ---------- */
const spdEl=$("#spd");
if(spdEl){
  const D=JSON.parse(spdEl.textContent),c=$("#spc"),l=$("#spl"),pv=$("#spprev"),nx=$("#spnext"),pp=$("#spp");
  // /belajar-solat/ (fardu) and the /solat-sunat/ pages share this player; a sunat page names its default prayer and storage key
  let w=D.def||"subuh",i=0;const SK=D.key||"solat-w";spdEl._sp={D,show:()=>show(false)};
  function card(){
    const[sid,r]=D.s[w][i];let[t,how,ar,ru,mn,src]=D.b[sid];if(sid==="niat"||sid==="j-niat")[ar,ru,mn]=D.w[w].niat;else if(sid==="niat2")[ar,ru,mn]=D.w[w].niat2;
    return`<p class="spn">${typeof r==="string"?r:`${D.w[w].u||"Rakaat"} ${r} daripada ${D.w[w].r}`} · Langkah ${i+1} / ${D.s[w].length}</p><h3 class="spt">${t}</h3><p class="spd">${how}</p><p class="dar" lang="ar" dir="rtl">${ar}</p><p class="dru"><em>${ru}</em></p><p class="dmn"><strong>Maksud:</strong> ${mn}</p><p class="dsrc">${src}</p>`;
  }
  const list=()=>D.s[w].map(([sid,r],k)=>`<li><button type="button" data-i="${k}"${k===i?' aria-current="step"':""}>${D.b[sid][0]} <small>${typeof r==="string"?r:"R"+r}</small></button></li>`).join("");
  function show(save){
    const N=D.s[w].length;i=Math.max(0,Math.min(N-1,i));
    setIf(c,card());setIf(l,list());pp.max=N;pp.value=i+1;pv.disabled=i===0;nx.textContent=i===N-1?"Ulang dari awal ⟲":"Seterusnya ›";
    $$("#spw button").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.w===w)));
    if(save){store.set(SK,w);writeHash({solat:w,langkah:i+1})}
  }
  nx.addEventListener("click",()=>{i=i===D.s[w].length-1?0:i+1;show(true);c.scrollIntoView({block:"nearest"})});
  pv.addEventListener("click",()=>{i--;show(true)});
  $("#spw").addEventListener("click",e=>{const b=e.target.closest("button[data-w]");if(!b)return;w=b.dataset.w;i=0;show(true)});
  l.addEventListener("click",e=>{const b=e.target.closest("button[data-i]");if(!b)return;i=+b.dataset.i;show(true);c.scrollIntoView({block:"nearest"})});
  for(const[id,cls]of[["#sprm","nr"],["#spmn","nm"]]){
    const b=$(id),set=off=>{b.setAttribute("aria-pressed",String(!off));c.classList.toggle(cls,off)};
    set(store.get("solat-"+cls,false));
    b.addEventListener("click",()=>{const off=!c.classList.contains(cls);store.set("solat-"+cls,off);set(off)});
  }
  $("#panduan").addEventListener("keydown",e=>{if(e.key==="ArrowRight")nx.click();else if(e.key==="ArrowLeft"&&!pv.disabled)pv.click()});
  $$("#panduan .act").forEach(a=>toolbar(a,{}));
  const h=readHash(),sw0=store.get(SK,w);
  if(D.w[h.solat]){w=h.solat;i=clamp(h.langkah,1,99,1)-1}else if(D.w[sw0])w=sw0;
  show(false);
}
/* ---------- solat sunat: today's sunat windows for a zone (mirror tools/pages7.py sw_card), jenazah pronouns, hajat text, tarawih counter ---------- */
const swEl=$("#sw2"),swdEl=$("#swd");
if(swEl&&swdEl){
  const SD=JSON.parse(swdEl.textContent),kind=swEl.dataset.k,zs=$("#swz"),out=$("#swo");
  const hmx=x=>hm(((x%1440)+1440)%1440),dur=m=>`${Math.floor(m/60)} jam ${m%60} minit`;
  const msk=()=>{const u=new Date(Date.now()+288e5);return new Date(u.getUTCFullYear(),u.getUTCMonth(),u.getUTCDate())};
  async function times(z,d){const o=await official(z,d.getFullYear()),c=SD.zc[z];return o?o.t[doy(d)]:solatDay(d.getFullYear(),d.getMonth()+1,d.getDate(),c[0],c[1])}
  function swCard(t,tn,z,d){
    const rows=[];
    if(kind==="dhuha"||kind==="hub")rows.push(["Dhuha bermula",hmx(t[2]+20),`kira-kira 20 minit selepas syuruk (${hmx(t[2])}), apabila matahari naik setinggi tombak`],
      ["Dhuha paling afdal",hmx(t[2]+Math.floor((t[5]-t[2])/4)),"suku siang, ketika panas mula terasa"],["Dhuha berakhir",hmx(t[3]),"sebelum masuk Zohor; elakkan beberapa minit sebelumnya (istiwa')"]);
    if(kind==="tahajjud"||kind==="witir"||kind==="hub"){
      const night=tn[1]+1440-t[5],last=tn[1]+1440-Math.floor(night/3);
      if(kind==="witir")rows.push(["Witir bermula",hmx(t[6]),"selepas solat Isyak"]);
      if(kind==="tahajjud")rows.push(["Malam bermula",hmx(t[5]),"Maghrib"],["Separuh malam",hmx(t[5]+Math.floor(night/2)),`malam ini ${dur(night)}`]);
      rows.push(["Sepertiga malam terakhir",hmx(last),"waktu paling afdal untuk tahajjud, doa dan witir"],["Berakhir",hmx(tn[1]),"masuk waktu Subuh esok"]);
    }
    if(kind==="jamak")rows.push(["Jamak taqdim Zohor + Asar",`${hmx(t[3])}–${hmx(t[4])}`,"kedua-duanya dalam waktu Zohor"],["Jamak takhir Zohor + Asar",`${hmx(t[4])}–${hmx(t[5])}`,"dalam waktu Asar; niat takhir dibuat semasa waktu Zohor"],
      ["Jamak taqdim Maghrib + Isyak",`${hmx(t[5])}–${hmx(t[6])}`,"kedua-duanya dalam waktu Maghrib"],["Jamak takhir Maghrib + Isyak",`${hmx(t[6])}–${hmx(tn[1])}`,"dalam waktu Isyak hingga sebelum Subuh esok"],["Subuh",hmx(t[1]),"tidak boleh dijamak atau diqasar"]);
    if(kind==="hub")rows.push(["Dilarang: selepas Subuh",`${hmx(t[1])}–${hmx(t[2]+20)}`,"selepas solat Subuh hingga matahari naik"],["Dilarang: istiwa'",`sebelum ${hmx(t[3])}`,"beberapa minit sebelum Zohor, ketika matahari tegak"],
      ["Dilarang: selepas Asar",`${hmx(t[4])}–${hmx(t[5])}`,"selepas solat Asar hingga matahari terbenam"]);
    return`<p class="swh">${dlong(d)} · zon ${z}</p><ul class="swr">${rows.map(([a,b,c])=>`<li><span class="swl">${a}</span><strong>${b}</strong><em>${c}</em></li>`).join("")}</ul>`;
  }
  let z=kind==="jamak"?SD.def:store.get("sunat-zone",SD.def);if(!SD.zc[z])z=SD.def;zs.value=z;
  async function draw(){const d=msk(),[t,tn]=await Promise.all([times(z,d),times(z,addD(d,1))]);setIf(out,swCard(t,tn,z,d))}
  zs.addEventListener("change",()=>{z=zs.value;if(kind!=="jamak")store.set("sunat-zone",z);draw()});
  swEl._zone=v=>{if(SD.zc[v]&&v!==z){z=v;zs.value=v;draw()}};draw();
}
const spX=$("#spd")?._sp;
if(spX&&spX.D.jz){
  const D=spX.D,jj=$("#jj");
  const setJ=k=>{const v=D.jz[k]||D.jz.l;D.w.jenazah.niat=v.niat;[2,3,4].forEach((n,x)=>{D.b["j-t3"][n]=v.t3[x];D.b["j-t4"][n]=v.t4[x]});$$("#niat .dar,#niat .dru,#niat .dmn").forEach((el,x)=>{el.innerHTML=x===2?`<strong>Maksud:</strong> ${v.niat[2]}`:x===1?`<em>${v.niat[1]}</em>`:v.niat[0]});spX.show()};
  jj.value=store.get("jenazah-j","l");if(!D.jz[jj.value])jj.value="l";setJ(jj.value);
  jj.addEventListener("change",()=>{store.set("jenazah-j",jj.value);setJ(jj.value)});
}
const hjIn=$("#hjin");
if(hjIn){const put=()=>{const v=hjIn.value.trim();$$(".shm").forEach(m=>m.textContent=v?`(${v})`:"(urusan ini)")};hjIn.addEventListener("input",put)}
const trw=$("#trw");
if(trw){
  const key="tarawih:"+iso(today());let st=Object.assign({n:20,c:0},store.get(key,{}));
  const paint=()=>{const S=st.n/2;$$("#trn button").forEach(b=>b.setAttribute("aria-pressed",String(+b.dataset.n===st.n)));
    $("#trs").textContent=st.c>=S?`✓ ${st.n} rakaat tarawih selesai. Teruskan dengan witir (3 rakaat: 2 + 1).`:`Salam ke-${st.c+1} daripada ${S} · rakaat ${st.c*2+1}–${st.c*2+2}${st.c===S/2?" · separuh, rehat sebentar":""}`;
    $("#trb").disabled=st.c>=S;store.set(key,st)};
  $("#trn").addEventListener("click",e=>{const b=e.target.closest("button[data-n]");if(b){st.n=+b.dataset.n;st.c=Math.min(st.c,st.n/2);paint()}});
  $("#trb").addEventListener("click",()=>{st.c++;if(navigator.vibrate)try{navigator.vibrate(20)}catch{}paint()});
  $("#tru").addEventListener("click",()=>{st.c=Math.max(0,st.c-1);paint()});$("#trr").addEventListener("click",()=>{st.c=0;paint()});
  try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&k.startsWith("ilmq:tarawih:")&&k!=="ilmq:"+key)localStorage.removeItem(k)}}catch{}
  paint();
}
/* ---------- jamak & qasar: musafir calculator (verdict mirrors tools/pages8.py verdict_html) ---------- */
const jmdEl=$("#jmd");
if(jmdEl){
  const J=JSON.parse(jmdEl.textContent),fr=$("#jfrom"),to=$("#jto"),t1=$("#jt1"),t2=$("#jt2"),out=$("#jout");
  const byName=n=>J.tw.find(t=>t[0].toLowerCase()===String(n).trim().toLowerCase());
  const km=(a,b,c,d)=>{const h=Math.sin(rad(c-a)/2)**2+Math.cos(rad(a))*Math.cos(rad(c))*Math.sin(rad(d-b)/2)**2;return 12742*Math.asin(Math.sqrt(h))};
  function jVerdict(a,b,stay){
    const k=Math.floor(km(a[2],a[3],b[2],b[3])+.5);let head,cls,why;
    if(k>=J.mh){head="✅ Layak jamak &amp; qasar";cls="ok";why=`Jarak garis lurus ${a[0]} → ${b[0]} ialah ${k} km, melebihi 2 marhalah (≈${J.mh} km). Jarak jalan biasanya lebih jauh lagi.`}
    else if(k>=J.mb){head="⚠️ Semak jarak jalan";cls="mb";why=`Jarak garis lurus ${k} km. Jarak jalan biasanya 20–40% lebih jauh; jika laluan anda ${J.mh} km atau lebih, anda layak.`}
    else{head="❌ Belum mencapai 2 marhalah";cls="no";why=`Jarak garis lurus ${k} km; jarak jalan jarang mencecah ${J.mh} km. Solatlah penuh pada waktunya.`}
    let s=`<p class="jvh ${cls}">${head}</p><p>${why} <a href="https://www.google.com/maps/dir/?api=1&amp;origin=${a[2]},${a[3]}&amp;destination=${b[2]},${b[3]}" rel="noopener nofollow">Semak jarak jalan di Google Maps ↗</a></p>`;
    if(stay){const full=Math.round((stay[1]-stay[0])/864e5)-1;
      if(full<-1)s+="<p>Tarikh pulang mesti selepas tarikh tiba.</p>";
      else if(full>=4)s+=`<p>Tinggal <strong>${full} hari penuh</strong> (tidak termasuk hari tiba dan hari pulang): anda dikira bermukim sebaik tiba di ${b[0]}; jamak dan qasar hanya semasa perjalanan pergi dan pulang.</p>`;
      else s+=`<p>Tinggal <strong>${Math.max(full,0)} hari penuh</strong> (kurang daripada 4): boleh jamak dan qasar sepanjang berada di ${b[0]} hingga pulang.</p>`}
    return s+`<p class="note">Waktu jamak di bawah mengikut zon destinasi, ${b[4]}.</p>`;
  }
  function run(save){
    const a=byName(fr.value),b=byName(to.value);
    if(!a||!b)return setIf(out,`<p>Pilih bandar daripada senarai (${J.tw.length} bandar di Malaysia).</p>`);
    const d1=parseD(t1.value),d2=parseD(t2.value);
    setIf(out,jVerdict(a,b,d1&&d2?[d1,d2]:null));
    swEl?._zone?.(b[4]);
    if(save){const o={dari:a[0],ke:b[0]};if(d1)o.tiba=t1.value;if(d2)o.pulang=t2.value;writeHash(o)}
  }
  $("#jmf").addEventListener("input",()=>run(true));$("#jmf").addEventListener("change",()=>run(true));
  $("#jgeo").addEventListener("click",()=>{
    if(!navigator.geolocation)return toast("Lokasi tidak disokong");
    navigator.geolocation.getCurrentPosition(p=>{const{latitude:la,longitude:lo}=p.coords;let best=J.tw[0],bd=1e9;
      for(const t of J.tw){const x=km(la,lo,t[2],t[3]);if(x<bd){bd=x;best=t}}
      fr.value=best[0];run(true);toast(`Bandar terdekat: ${best[0]}`)},()=>toast("Kebenaran lokasi ditolak"),{timeout:10000,maximumAge:6e5});
  });
  const h=readHash();if(byName(h.dari))fr.value=byName(h.dari)[0];if(byName(h.ke))to.value=byName(h.ke)[0];if(parseD(h.tiba))t1.value=h.tiba;if(parseD(h.pulang))t2.value=h.pulang;
  if(h.dari||h.ke||h.tiba)run(false);
}
/* ---------- zakat fitrah: household total and the coming Ramadan's payment timeline (mirror tools/pages9.py) ---------- */
const zfdEl=$("#zfd");
if(zfdEl&&HJ){
  const Z=JSON.parse(zfdEl.textContent),st=$("#zfs"),ti=$("#zft"),na=$("#zfa"),nk=$("#zfk"),out=$("#zfo");
  const rm=x=>{const[s,d]=x.toFixed(2).split(".");return`RM${s.replace(/\B(?=(\d{3})+(?!\d))/g,",")}.${d}`};
  function zfResult(s,t,n){const r=Z.r[s],k=Math.min(t,r.length-1);
    return`<p class="zft">${rm(r[k]*n)}</p><p>${n} orang × ${rm(r[k])} (${esc(Z.t[k])}, ${esc(Z.n[s])}). Jika dibayar dengan beras: <strong>${(Z.g*n).toFixed(1)} kg</strong> (${n} gantang Baghdad).</p>`}
  function zfTimeline(d){
    let hy=g2h(d)[0],y=[hy,hy+1].find(x=>h2g(x,10,1)[0]>=d)??hy+1;
    const[r1,o1]=h2g(y,9,1),[eid]=h2g(y,10,1),last=addD(eid,-1),n=Math.round((r1-d)/864e5);
    const rows=[["Harus (boleh) dibayar",`${dlong(r1)} hingga sebelum Maghrib ${dlong(last)}`,"sepanjang Ramadan; ramai membayar awal"],["Wajib",`Maghrib ${dlong(last)}`,"masuk 1 Syawal: setiap Muslim yang hidup ketika itu wajib dizakatkan"],
      ["Paling afdal",`Pagi ${dlong(eid)}`,"selepas Subuh hingga sebelum solat sunat Aidilfitri"],["Makruh",`${dlong(eid)}, selepas solat raya`,"hingga terbenam matahari 1 Syawal"],["Haram (wajib qada)",`Selepas Maghrib ${dlong(eid)}`,"melewatkan tanpa uzur berdosa dan wajib diqada"]];
    return`<p class="swh">Ramadan ${y} H ${o1?"bermula":"dijangka bermula"} ${dlong(r1)}${n>0?` · lagi ${n} hari`:""}</p><ul class="swr">${rows.map(([a,b,c])=>`<li><span class="swl">${a}</span><strong>${b}</strong><em>${c}</em></li>`).join("")}</ul>`;
  }
  const tierOpts=s=>Z.r[s].map((r,i)=>`<option value="${i}">${esc(Z.t[i])}: ${rm(r)}</option>`).join("");
  function run(save){
    const s=Z.r[st.value]?st.value:"selangor",t=clamp(ti.value,0,2,0),n=clamp(na.value,0,50,0)+clamp(nk.value,0,50,0);
    setIf(out,n?zfResult(s,t,n):"<p>Masukkan bilangan ahli keluarga.</p>");
    if(save)store.set("zakat-fitrah",{s,t,a:na.value,k:nk.value});
  }
  st.addEventListener("change",()=>{const t=ti.value;setIf(ti,tierOpts(st.value));ti.value=String(Math.min(+t,Z.r[st.value].length-1));run(true)});
  $("#zff").addEventListener("input",e=>{if(e.target!==st)run(true)});
  const sv=store.get("zakat-fitrah",null);
  if(sv&&Z.r[sv.s]){st.value=sv.s;setIf(ti,tierOpts(sv.s));ti.value=String(Math.min(sv.t,Z.r[sv.s].length-1));na.value=sv.a;nk.value=sv.k;run(false)}
  const u=new Date(Date.now()+288e5);setIf($("#zfl"),zfTimeline(new Date(u.getUTCFullYear(),u.getUTCMonth(),u.getUTCDate())));
}

/* ---------- zakat pendapatan: gross vs net, state nisab, tax rebate (mirror tools/pages10.py) ---------- */
const zpEl=$("#zpdat");
if(zpEl){
  const Z=JSON.parse(zpEl.textContent),f=$("#zpf"),out=$("#zpr"),F={};
  ["s","m","g","el","b","o","d","ni","ai","nk","ak","ib","kw","lt","ns","au","rl"].forEach(k=>F[k]=$("#zp"+k));
  const r2=x=>Math.floor(x*100+.5)/100;
  const rm=x=>{const[a,b]=x.toFixed(2).split(".");return`RM${a.replace(/\B(?=(\d{3})+(?!\d))/g,",")}.${b}`};
  const nv=(el,mx=1e9)=>{const v=parseFloat(el.value);return Number.isFinite(v)?Math.min(mx,Math.max(0,v)):0};
  function tax(ci){let t=0,lo=0;for(const[hi,r]of Z.bd){if(ci>lo)t+=(Math.min(ci,hi)-lo)*r;lo=hi}if(ci<=35000)t-=400;return Math.max(0,t)}
  function zpCalc(i){
    const wages=12*(i.g+i.el)+i.b,total=wages+i.o,kwsp=wages*i.kw/100;
    const ded=i.d+i.ni*i.ai+i.nk*i.ak+i.ib+kwsp+i.lt,relief=i.rl!=null?i.rl:9000+Math.min(kwsp,4000)+2000*i.nk;
    const tx=r2(tax(Math.max(0,total-relief))),o={total:r2(total),kwsp:r2(kwsp),relief:r2(relief),tax:tx};
    for(const[m,base]of[["kasar",total],["bersih",Math.max(0,total-ded)]]){
      const ok=base>=i.ns&&base>0,z=ok?r2(base*.025):0,rb=Math.min(z,tx);
      o[m]={ded:r2(m==="kasar"?0:ded),base:r2(base),ok,z,mo:r2(z/12),rb,cost:r2(z-rb)};
    }
    return o;
  }
  function zpResult(i){
    const c=zpCalc(i),m=c[i.m],nm={kasar:"kaedah kasar",bersih:"kaedah bersih (dengan tolakan)"};
    let head;
    if(m.ok)head=`<p class="jvh ok">✅ Wajib zakat pendapatan (${nm[i.m]})</p><p class="zft">${rm(m.z)} <small>setahun</small></p>`+
      `<p>Potongan gaji: <strong>${rm(m.mo)} sebulan</strong> × 12. `+(m.rb>0?`Zakat ini ditolak terus daripada cukai pendapatan (rebat ${rm(m.rb)}), jadi <strong>kos sebenar anda ${rm(m.cost)}</strong>.`:"Tiada cukai untuk ditolak, jadi tiada rebat cukai.")+"</p>";
    else head=`<p class="jvh no">❌ Belum cukup nisab (${nm[i.m]})</p><p>Pendapatan dikira ${rm(m.base)} kurang daripada nisab ${rm(i.ns)}. Zakat pendapatan belum wajib; bersedekah tetap digalakkan.</p>`;
    const K=c.kasar,B=c.bersih,yn=v=>v?"Ya":"Tidak",st=x=>`<strong>${x}</strong>`;
    const rows=[["Jumlah pendapatan setahun",rm(c.total),rm(c.total)],["Tolakan","–",rm(B.ded)],["Pendapatan dikira",rm(K.base),rm(B.base)],["Cukup nisab?",yn(K.ok),yn(B.ok)],
      [st("Zakat setahun (2.5%)"),st(rm(K.z)),st(rm(B.z))],["Sebulan",rm(K.mo),rm(B.mo)],["Rebat cukai daripada zakat",rm(K.rb),rm(B.rb)],[st("Kos sebenar zakat"),st(rm(K.cost)),st(rm(B.cost))]];
    const ci=c.total-c.relief;
    return head+`<div class="tw"><table class="zpt"><thead><tr><th scope="col">Perkara</th><th scope="col">Kasar</th><th scope="col">Bersih</th></tr></thead><tbody>${rows.map(([a,b,d])=>`<tr><th scope="row">${a}</th><td>${b}</td><td>${d}</td></tr>`).join("")}</tbody></table></div>`+
      `<p class="note">Anggaran cukai sebelum zakat: <strong>${rm(c.tax)}</strong> (pendapatan bercukai ${rm(Math.max(0,ci))} selepas pelepasan ${rm(c.relief)}, kadar YA2025${ci<=35000?", termasuk rebat diri RM400":""}). KWSP pekerja: ${rm(c.kwsp)}.</p>`;
  }
  let rlEdited=false;
  const inputs=()=>({s:F.s.value,m:F.m.value==="bersih"?"bersih":"kasar",g:nv(F.g),el:nv(F.el),b:nv(F.b),o:nv(F.o),d:nv(F.d),ni:clamp(F.ni.value,0,4,0),ai:nv(F.ai),nk:clamp(F.nk.value,0,30,0),ak:nv(F.ak),
    ib:nv(F.ib),kw:nv(F.kw,30),lt:nv(F.lt),ns:nv(F.ns),rl:rlEdited?nv(F.rl):null});
  const pressP=()=>$$("#zpp button").forEach(b=>{const p=Z.p[b.dataset.p];b.setAttribute("aria-pressed",String(nv(F.d)===p[0]&&nv(F.ai)===p[1]&&nv(F.ak)===p[2]))});
  const applyP=k=>{const p=Z.p[k];[F.d.value,F.ai.value,F.ak.value]=p.map(String);pressP()};
  const nisabOf=s=>Z.n[s]??Math.round(Z.g*(nv(F.au)||Z.au));
  function run(save){
    const i=inputs();
    if(!rlEdited){const c=zpCalc(i);F.rl.value=String(c.relief)}
    setIf(out,zpResult(i));
    if(save){const v={};for(const k in F)v[k]=F[k].value;v.rlu=rlEdited;store.set("zakat-pendapatan",v)}
  }
  f.addEventListener("input",e=>{
    const t=e.target;
    if(t===F.rl)rlEdited=true;
    if(t===F.au)F.ns.value=String(Math.round(Z.g*nv(F.au)));
    if(t===F.s){F.ns.value=String(nisabOf(F.s.value));applyP(F.s.value==="selangor"?"lzs":"asas")}
    if(t===F.d||t===F.ai||t===F.ak)pressP();
    run(true);
  });
  $("#zpp").addEventListener("click",e=>{const b=e.target.closest("button[data-p]");if(b){applyP(b.dataset.p);run(true)}});
  $("#kira .act").addEventListener("click",e=>{
    const b=e.target.closest("button[data-act]");if(!b)return;
    if(b.dataset.act==="copy")copy(out.innerText.replace(/\n{2,}/g,"\n")+"\n"+location.href,"Keputusan disalin ✓");
    else if(b.dataset.act==="reset"){const D=Z.def;for(const k in D)if(F[k]&&D[k]!=null)F[k].value=String(D[k]);F.au.value=String(Z.au);rlEdited=false;pressP();run(true)}
  });
  const sv=store.get("zakat-pendapatan",null);
  if(sv&&typeof sv==="object"){for(const k in F)if(sv[k]!=null)F[k].value=sv[k];rlEdited=!!sv.rlu;pressP();run(false)}
}

/* ---------- zakat simpanan, emas, perniagaan (mirror tools/pages11.py) ---------- */
const zkEl=$("#zsdat")||$("#zedat")||$("#zbdat");
if(zkEl){
  const Z=JSON.parse(zkEl.textContent),r2=x=>Math.floor(x*100+.5)/100;
  const n2=x=>{const[a,b]=x.toFixed(2).split(".");return`${a.replace(/\B(?=(\d{3})+(?!\d))/g,",")}.${b}`};
  const rm=x=>"RM"+n2(r2(x)),gram=x=>n2(r2(x))+" g",num=x=>x.toFixed(2).replace(/\.?0+$/,"");
  const nv=(el,mx=1e9)=>{const v=parseFloat(el.value);return Number.isFinite(v)?Math.min(mx,Math.max(0,v)):0};
  const RATES={h:[.025,"2.5% (tahun Hijrah)"],m:[.02577,"2.577% (tahun Masihi)"]};
  const verdict=(ok,t,z,x)=>ok?`<p class="jvh ok">✅ Wajib ${t}</p><p class="zft">${rm(z)}</p>${x}`:`<p class="jvh no">❌ Belum wajib ${t}</p>${x}`;
  const sumA=a=>a.reduce((s,x)=>s+x,0);
  // persist every field of the form; restore before the first run
  function wire(form,key,run,act){
    form.addEventListener("input",e=>{run(e.target);const v={};$$("input,select",form).forEach(x=>v[x.id]=x.type==="checkbox"?x.checked:x.value);store.set(key,v)});
    act.addEventListener("click",e=>{const b=e.target.closest("button[data-act]");if(!b)return;
      if(b.dataset.act==="copy")copy($(".jv",form).innerText.replace(/\n{2,}/g,"\n")+"\n"+location.href,"Keputusan disalin ✓");
      else if(b.dataset.act==="reset"){form.reset();store.set(key,null);run(null)}});
    const sv=store.get(key,null);
    if(sv&&typeof sv==="object"){for(const id in sv){const x=document.getElementById(id);if(x&&form.contains(x)){if(x.type==="checkbox")x.checked=!!sv[id];else x.value=sv[id]}}run(null)}
  }
  const nisabWire=(st,ns,au,t)=>{if(t===au)ns.value=String(Math.round(Z.g*nv(au)));if(t===st)ns.value=String(Z.n[st.value]??Math.round(Z.g*(nv(au)||Z.au)))};
  if(zkEl.id==="zsdat"){
    const f=$("#zsf"),out=$("#zsr"),ho=$("#zsho");
    function zsResult(i){
      const[rate,rl]=RATES[i.hy],total=sumA(i.b)+(i.dv?sumA(i.d):0);
      if(total<=0)return"<p>Masukkan baki terendah simpanan anda.</p>";
      const ok=total>=i.ns,z=ok?r2(total*rate):0;
      const extra=ok?`<p>${rl} × ${rm(total)}. Zakat simpanan juga layak rebat cukai pendapatan (Seksyen 6A(3)).</p>`:`<p>Jumlah dikira ${rm(total)} kurang daripada nisab ${rm(i.ns)}.</p>`;
      const tr=Z.acc.map((a,k)=>i.b[k]||i.d[k]?`<tr><th scope="row">${a}</th><td data-l="Baki terendah">${rm(i.b[k])}</td><td data-l="Dividen/hibah">${i.dv?rm(i.d[k]):"–"}</td><td data-l="Dikira">${rm(i.b[k]+(i.dv?i.d[k]:0))}</td></tr>`:"").join("");
      return verdict(ok,"zakat simpanan",z,extra)+`<div class="tw"><table class="zpt rt"><thead><tr><th scope="col">Akaun</th><th scope="col">Baki terendah</th><th scope="col">Dividen/hibah</th><th scope="col">Dikira</th></tr></thead><tbody>${tr}<tr><th scope="row"><strong>Jumlah</strong></th><td></td><td></td><td data-l="Dikira"><strong>${rm(total)}</strong></td></tr></tbody></table></div>`;
    }
    const inp=()=>({hy:$("#zsh").value==="m"?"m":"h",b:Z.acc.map((_,k)=>nv($("#zsb"+k))),d:Z.acc.map((_,k)=>nv($("#zsd"+k))),dv:$("#zsdv").checked,ns:nv($("#zsn"))});
    function haul(){
      const s=parseD($("#zsmula").value);if(!s){setIf(ho,"");return}
      let g,o=true;
      if($("#zsh").value==="m")g=new Date(s.getFullYear()+1,s.getMonth(),s.getDate());
      else{const h=g2h(s),y=h[0]+1;[g,o]=h2g(y,h[1],Math.min(h[2],hMonthLen(y,h[1])[0]))}
      const n=Math.round((g-mytDay())/864e5);
      setIf(ho,`<p>Haul cukup pada <strong>${dlong(g)}</strong> (${hstr(g2h(g))})${o?"":", anggaran"}${n>0?`, lagi ${n} hari`:n===0?", iaitu hari ini":", sudah berlalu"}.</p>`);
    }
    const run=t=>{nisabWire($("#zss"),$("#zsn"),$("#zsau"),t);setIf(out,zsResult(inp()));haul()};
    zkEl._calc=zsResult;wire(f,"zakat-simpanan",run,$("#zsact"));
  }else if(zkEl.id==="zedat"){
    const f=$("#zef"),out=$("#zer");
    function zeResult(i){
      const[rate,rl]=RATES[i.hy];
      if(sumA(i.g)<=0)return"<p>Masukkan berat emas anda.</p>";
      const u=Z.u[i.s],kept=i.g[0]*i.k[0]/1000+i.g[2]*i.k[2]/1000,exg=u?Math.max(0,i.g[1]-u):i.g[1],exp=exg*i.k[1]/1000,tot=kept+exp;
      const ok=tot>0&&(tot>=Z.g||(u>0&&exg>0)),val=r2(tot*i.au),z=ok?r2(val*rate):0;
      const un=u?`uruf ${Z.nm[i.s]} ${u} g`:`${Z.nm[i.s]} tiada uruf`;
      const extra=ok?`<p>${gram(tot)} emas tulen × RM${num(i.au)}/g = ${rm(val)} × ${rl}.</p>`:`<p>Emas dikira ${gram(tot)} tulen, kurang daripada nisab ${Z.g} g; emas dipakai tidak melebihi ${un}.</p>`;
      const rows=[["Emas simpanan (jongkong, syiling, akaun emas)",0,i.g[0]*i.k[0]/1000],[`Perhiasan dipakai (${un})`,1,exp],["Perhiasan tidak dipakai / disimpan",2,i.g[2]*i.k[2]/1000]];
      const tr=rows.map(([a,k,c])=>i.g[k]?`<tr><th scope="row">${a}</th><td data-l="Berat">${gram(i.g[k])}</td><td data-l="Ketulenan">${i.k[k]}</td><td data-l="Dikira (tulen)">${gram(c)}</td></tr>`:"").join("");
      return verdict(ok,"zakat emas",z,extra)+`<div class="tw"><table class="zpt rt"><thead><tr><th scope="col">Jenis</th><th scope="col">Berat</th><th scope="col">Ketulenan</th><th scope="col">Dikira (tulen)</th></tr></thead><tbody>${tr}<tr><th scope="row"><strong>Jumlah</strong></th><td></td><td></td><td data-l="Dikira (tulen)"><strong>${gram(tot)}</strong></td></tr></tbody></table></div>`;
    }
    const inp=()=>({s:Z.u[$("#zes").value]!=null?$("#zes").value:"selangor",hy:$("#zeh").value==="m"?"m":"h",au:nv($("#zeau")),g:[0,1,2].map(k=>nv($("#zeg"+k))),k:[0,1,2].map(k=>clamp($("#zek"+k).value,1,999,999))});
    const run=()=>setIf(out,zeResult(inp()));
    zkEl._calc=zeResult;wire(f,"zakat-emas",run,$("#zeact"));
  }else{
    const f=$("#zbf"),out=$("#zbr");
    function zbResult(i){
      const[rate,rl]=RATES[i.hy],aset=i.t+i.st+i.p+i.a,base0=Math.max(0,aset-i.l-i.x),base=base0*i.m/100;
      if(aset<=0)return"<p>Masukkan aset semasa perniagaan anda.</p>";
      const ok=base>=i.ns&&base>0,z=ok?r2(base*rate):0;
      const extra=ok?`<p>${rl} × ${rm(base)} (modal kerja bersih bahagian Muslim).</p>`:`<p>Modal kerja bersih ${rm(base)} kurang daripada nisab ${rm(i.ns)}.</p>`;
      const rows=[["Jumlah aset semasa",rm(aset)],["Tolak liabiliti semasa",rm(i.l)],["Tolak pelarasan",rm(i.x)],["Modal kerja bersih",rm(base0)],[`Bahagian pemilikan Muslim (${num(i.m)}%)`,rm(base)],["<strong>Zakat perniagaan</strong>",`<strong>${rm(z)}</strong>`]];
      return verdict(ok,"zakat perniagaan",z,extra)+`<div class="tw"><table class="zpt"><tbody>${rows.map(([a,b])=>`<tr><th scope="row">${a}</th><td>${b}</td></tr>`).join("")}</tbody></table></div>`;
    }
    const inp=()=>({hy:$("#zbh").value==="m"?"m":"h",t:nv($("#zbt")),st:nv($("#zbst")),p:nv($("#zbp")),a:nv($("#zba")),l:nv($("#zbl")),x:nv($("#zbx")),m:nv($("#zbm"),100),ns:nv($("#zbn"))});
    const run=t=>{nisabWire($("#zbs"),$("#zbn"),$("#zbau"),t);setIf(out,zbResult(inp()))};
    zkEl._calc=zbResult;wire(f,"zakat-perniagaan",run,$("#zbact"));
  }
}

/* ---------- faraid (mirror tools/faraid.py): Shafi'i, fractions and integer sen ---------- */
const frdEl=$("#frdat");
if(frdEl){
  const D=JSON.parse(frdEl.textContent),KEYS=D.h.map(x=>x[0]),LABEL={},MAXN={};D.h.forEach(([k,l,m])=>{LABEL[k]=l;MAXN[k]=m});
  const SHORT=D.sh,CHAIN=D.ch,NOTES=D.nt;
  const gcd=(a,b)=>{a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b]}return a};
  const F=(n,d=1)=>{if(d<0){n=-n;d=-d}const g=gcd(n,d)||1;return[n/g,d/g]};
  const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]),mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),div=(a,b)=>F(a[0]*b[1],a[1]*b[0]);
  const gt=(a,b)=>a[0]*b[1]>b[0]*a[1],Z=[0,1],ONE=[1,1],sum=v=>v.reduce(add,Z),isZ=a=>a[0]===0;
  const lcm=(a,b)=>a/gcd(a,b)*b;
  function faraid(h,radd){
    const n={};for(const k of KEYS){const v=parseInt(h[k],10);n[k]=Math.max(0,Math.min(MAXN[k],Number.isFinite(v)?v:0))}
    const ex={},block=(k,r)=>{if(n[k]&&!(k in ex))ex[k]=r},live=k=>n[k]>0&&!(k in ex);
    const desc=n.al+n.ap+n.cl+n.cp>0;
    if(n.al){block("cl","al");block("cp","al")}else if(n.ap>=2&&!n.cl)block("cp","ap2");
    if(n.bp)block("dt","bp");
    if(n.ib){block("ni","ib");block("nb","ib")}
    if(n.bp)block("nb","bp");
    for(const k of["sil","sip"])for(const b of["al","ap","cl","cp","bp","dt"])if(live(b))block(k,b);
    for(const k of["skl","skp","sbl","sbp"])for(const b of["al","cl","bp"])if(live(b))block(k,b);
    if(live("dt")&&["skl","skp","sbl","sbp"].some(live))return{rows:[],ex:[],bm:Z,base:0,aul:0,note:"",bad:true};
    const fdesc=live("ap")||live("cp"),ag={skp_ag:live("skp")&&!n.skl&&fdesc};
    for(const k of["sbl","sbp"]){if(live("skl"))block(k,"skl");else if(ag.skp_ag)block(k,"skp_ag")}
    if(live("sbp")&&n.skp>=2&&!n.sbl)block("sbp","skp2");
    ag.sbp_ag=live("sbp")&&!n.sbl&&fdesc;
    for(let i=8;i<CHAIN.length;i++){const k=CHAIN[i];for(const b of CHAIN.slice(0,i))if(b in ag?ag[b]:live(b)){block(k,b);break}}
    const fard={},asab={},basis={};
    const sibs=n.skl+n.skp+n.sbl+n.sbp+n.sil+n.sip;let spouse=Z,note="";
    if(live("su"))fard.su=spouse=desc?F(1,4):F(1,2);
    if(live("is"))fard.is=spouse=desc?F(1,8):F(1,4);
    if(live("ib")){
      if(desc||sibs>=2)fard.ib=F(1,6);
      else if(live("bp")&&!isZ(spouse)){fard.ib=div(sub(ONE,spouse),F(3));note="umar";basis.ib="1/3 baki ('umariyyatain)"}
      else fard.ib=F(1,3);
    }
    for(const k of["bp","dt"])if(live(k)){
      if(live("al")||live("cl"))fard[k]=F(1,6);
      else if(desc){fard[k]=F(1,6);asab[k]=1;basis[k]="1/6 + asabah"}
      else asab[k]=1;
    }
    const gm=["ni","nb"].filter(live);for(const k of gm)fard[k]=F(1,6*gm.length);
    if(live("ap")){if(live("al")){asab.al=2;asab.ap=1}else fard.ap=n.ap===1?F(1,2):F(2,3)}else if(live("al"))asab.al=2;
    if(live("cp")){if(live("cl")){asab.cl=2;asab.cp=1}else if(!n.ap)fard.cp=n.cp===1?F(1,2):F(2,3);else{fard.cp=F(1,6);basis.cp="1/6 (takmilah 2/3)"}}
    else if(live("cl"))asab.cl=2;
    const ut=live("sil")||live("sip")?n.sil+n.sip:0;
    const mus=ut>=2&&live("skl")&&live("su")&&(live("ib")||gm.length>0)&&!desc&&!live("bp")&&!live("dt");
    if(ut){
      const share=ut===1?F(1,6):F(1,3),heads=ut+(mus?n.skl+n.skp:0);
      for(const k of mus?["sil","sip","skl","skp"]:["sil","sip"])if(live(k)){fard[k]=mul(share,F(n[k],heads));if(mus)basis[k]="1/3 dikongsi sama rata (musytarakah)"}
      if(mus)note="mus";
    }
    if(!mus){
      if(live("skl")){asab.skl=2;if(live("skp"))asab.skp=1}
      else if(live("skp")){if(ag.skp_ag){asab.skp=1;basis.skp="Asabah ma'al ghair"}else fard.skp=n.skp===1?F(1,2):F(2,3)}
      if(live("sbl")){asab.sbl=2;if(live("sbp"))asab.sbp=1}
      else if(live("sbp")){
        if(ag.sbp_ag){asab.sbp=1;basis.sbp="Asabah ma'al ghair"}
        else if(n.skp===1&&live("skp")){fard.sbp=F(1,6);basis.sbp="1/6 (takmilah 2/3)"}
        else fard.sbp=n.sbp===1?F(1,2):F(2,3);
      }
    }
    for(const k of CHAIN.slice(8))if(live(k))asab[k]=1;
    const fk=Object.keys(fard),base=fk.length?fk.map(k=>fard[k][1]).reduce(lcm,1):1,tot=sum(fk.map(k=>fard[k]));
    const aul=gt(tot,ONE)?mul(tot,F(base))[0]:0;
    const share={};for(const k of fk)share[k]=gt(tot,ONE)?div(fard[k],tot):fard[k];
    const rest=gt(tot,ONE)?Z:sub(ONE,tot);let bm=Z;
    if(!isZ(rest)){
      const ak=Object.keys(asab);
      if(ak.length){const w=ak.reduce((s,k)=>s+asab[k]*n[k],0);for(const k of ak)share[k]=add(share[k]||Z,mul(rest,F(asab[k]*n[k],w)))}
      else{
        const pool=fk.filter(k=>k!=="su"&&k!=="is");
        if(radd&&pool.length){const pt=sum(pool.map(k=>fard[k]));for(const k of pool)share[k]=add(share[k],div(mul(rest,fard[k]),pt));note=note||"radd"}
        else bm=rest;
      }
    }
    const rows=[],mixed=new Set(Object.values(asab)).size>1;
    for(const k of KEYS)if(live(k)){
      let b;
      if(k in basis)b=basis[k];
      else if(k in asab)b=k in fard?"Fardh + asabah":"Asabah"+(mixed?" (lelaki 2 : perempuan 1)":"");
      else if((k==="ni"||k==="nb")&&gm.length===2)b="1/6 dikongsi";
      else if((k==="sil"||k==="sip")&&ut>1)b="1/3 dikongsi";
      else b="Fardh"+(n[k]>1?" dikongsi":"");
      rows.push([k,n[k],share[k]||Z,b]);
    }
    return{rows,ex:KEYS.filter(k=>k in ex).map(k=>[k,n[k],ex[k]]),bm,base:fk.length?base:0,aul,note,bad:false};
  }
  const fmtSen=s=>`RM${Math.floor(s/100).toString().replace(/\B(?=(\d{3})+(?!\d))/g,",")}.${String(s%100).padStart(2,"0")}`;
  const part=(e,f,c=1)=>{const num=e*f[0],den=f[1]*c;return Math.floor((2*num+den)/(2*den))};
  const pct=f=>{const h=Math.floor((20000*f[0]+f[1])/(2*f[1]));return`${Math.floor(h/100)}.${String(h%100).padStart(2,"0")}%`};
  const frs=f=>f[1]!==1?`${f[0]}/${f[1]}`:String(f[0]);
  function faraidHtml(h,e,radd){
    const r=faraid(h,radd);
    if(r.bad)return'<p class="jvh mb">⚠️ Kes datuk bersama saudara seibu sebapa/sebapa</p><p>Pembahagian datuk bersama adik-beradik (muqasamah) mempunyai kaedah khas dan khilaf ulama. Kalkulator ini tidak mengiranya; sila rujuk Mahkamah Syariah atau Pejabat Pusaka Kecil.</p>';
    if(!r.rows.length&&!r.ex.length)return`<p class="jvh no">Tiada waris dipilih</p><p>Jika tiada waris langsung, keseluruhan harta (${fmtSen(e)}) diserahkan kepada Baitulmal.</p>`;
    let out=`<p class="frs">Harta untuk dibahagi: <strong>${fmtSen(e)}</strong>`;
    if(r.base)out+=` · Asal masalah <strong>${r.base}</strong>`+(r.aul?`, <strong>'aul kepada ${r.aul}</strong>`:"");
    out+="</p>";
    if(r.note)out+=`<p class="note">${NOTES[r.note]}</p>`;
    let tr="";
    for(const[k,c,sh,b]of r.rows)tr+=`<tr><th scope="row">${LABEL[k]}${c>1?` × ${c}`:""}</th><td data-l="Bahagian">${frs(sh)}<small>${b}</small></td><td data-l="%">${pct(sh)}</td><td data-l="Seorang">${fmtSen(part(e,sh,c))}</td><td data-l="Jumlah">${fmtSen(part(e,sh))}</td></tr>`;
    if(!isZ(r.bm))tr+=`<tr><th scope="row">Baitulmal</th><td data-l="Bahagian">${frs(r.bm)}<small>Baki tanpa asabah</small></td><td data-l="%">${pct(r.bm)}</td><td data-l="Seorang">–</td><td data-l="Jumlah">${fmtSen(part(e,r.bm))}</td></tr>`;
    out+=`<div class="tw"><table class="frt rt"><thead><tr><th scope="col">Waris</th><th scope="col">Bahagian</th><th scope="col">%</th><th scope="col">Seorang</th><th scope="col">Jumlah</th></tr></thead><tbody>${tr}</tbody></table></div>`;
    if(r.ex.length)out+='<p class="frh">Terhalang (mahjub)</p><ul class="frx">'+r.ex.map(([k,c,w])=>`<li><strong>${LABEL[k]}${c>1?` × ${c}`:""}</strong>: terhalang oleh ${SHORT[w]}</li>`).join("")+"</ul>";
    return out;
  }
  const estate=(g,d,f,w)=>{const net=Math.max(0,g-d-f),ww=Math.min(w,Math.floor(net/3));return[net-ww,ww]};
  const fm=$("#frf"),out=$("#frr"),est=$("#fre");
  const toSen=el=>{const v=parseFloat(el.value);return Number.isFinite(v)&&v>0?Math.round(Math.min(v,1e8)*100):0};
  function read(){
    const sx=$("#frsx").value,h={};
    for(const k of KEYS){const el=$("#fr-"+k);if(!el||el.closest("[hidden]"))continue;h[k]=el.type==="checkbox"?(el.checked?1:0):el.value}
    if(sx==="l")h.su=0;else h.is=0;
    return h;
  }
  function run(save){
    const male=$("#frsx").value==="l";$("#frw-su").hidden=male;$("#frw-is").hidden=!male;
    const[e,w]=estate(toSen($("#frg")),toSen($("#frdb")),toSen($("#frfu")),toSen($("#frws")));
    setIf(est,`Harta bersih selepas hutang, kos jenazah${w?` dan wasiat ${fmtSen(w)}`:" dan wasiat"}: <strong>${fmtSen(e)}</strong>`);
    setIf(out,faraidHtml(read(),e,$("#frrd").checked));
    if(save){const v={};$$("input,select",fm).forEach(x=>v[x.id]=x.type==="checkbox"?x.checked:x.value);store.set("faraid",v)}
  }
  frdEl._calc=(h,e,radd)=>faraidHtml(h,e,radd);
  fm.addEventListener("input",()=>run(true));
  $("#fract").addEventListener("click",ev=>{const b=ev.target.closest("button[data-act]");if(!b)return;
    if(b.dataset.act==="copy")copy(out.innerText.replace(/\n{2,}/g,"\n")+"\n"+location.href,"Keputusan disalin ✓");
    else if(b.dataset.act==="reset"){fm.reset();run(true)}});
  const sv=store.get("faraid",null);
  if(sv&&typeof sv==="object"){for(const id in sv){const x=document.getElementById(id);if(x&&fm.contains(x)){if(x.type==="checkbox")x.checked=!!sv[id];else x.value=sv[id]}}run(false)}
}

/* ---------- asmaul husna: name of the day, search, memorised ticks, flashcards, quiz ---------- */
const asdEl=$("#asd");
if(asdEl){
  const N=JSON.parse(asdEl.textContent).n,list=$("#anl"),q=$("#anq"),prog=$("#anp");
  const u=new Date(Date.now()+288e5),d0=new Date(u.getUTCFullYear(),u.getUTCMonth(),u.getUTCDate()),t=doy(d0)%99;
  $("#anda").textContent=N[t][0];$("#andr").textContent=`${t+1}. ${N[t][1]}`;$("#andm").textContent=N[t][2];
  $("#and .swl").textContent=`Nama hari ini · ${dlong(d0)}`;
  let got=new Set(store.get("asmaul",[]));
  const paint=()=>{$$("input[data-n]",list).forEach(c=>{c.checked=got.has(+c.dataset.n);c.closest(".anc").classList.toggle("done",c.checked)});prog.textContent=`${got.size} / 99 dihafal${got.size===99?" · Masya-Allah, lengkap!":""}`};
  list.addEventListener("change",e=>{const c=e.target.closest("input[data-n]");if(!c)return;c.checked?got.add(+c.dataset.n):got.delete(+c.dataset.n);store.set("asmaul",[...got].sort((a,b)=>a-b));paint()});
  q.addEventListener("input",()=>{const v=q.value.trim().toLowerCase();$$(".anc",list).forEach(li=>li.hidden=!!v&&!li.dataset.q.includes(v)&&li.querySelector(".ann").textContent!==v)});
  paint();speech.init();
  // flashcards
  let k=t,show=false;const kd=$("#ankd");
  const drawK=()=>{const[ar,ru,mn]=N[k];kd.innerHTML=`<span class="ann">${k+1} / 99</span><span class="ana" lang="ar" dir="rtl">${esc(ar)}</span>${show?`<span class="anr">${esc(ru)}</span><span class="anm">${esc(mn)}</span>`:'<span class="note">Tekan untuk lihat maksud</span>'}`;$('#ankad [data-k="0"]').textContent=show?"Sembunyi maksud":"Tunjuk maksud"};
  $("#ankad").addEventListener("click",e=>{const b=e.target.closest("[data-k]");if(!b)return;const a=b.dataset.k;
    if(a==="r"){k=Math.floor(Math.random()*99);show=false}else if(a==="s")speech.say(N[k][0]);else if(a==="0")show=!show;else{k=(k+ +a+99)%99;show=false}drawK()});
  kd.addEventListener("click",()=>{show=!show;drawK()});kd.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();show=!show;drawK()}});
  // quiz: arabic -> meaning, 10 questions
  const qz=$("#anqz");let qs=[],qi=0,score=0;
  const ask=()=>{
    if(qi>=qs.length){const b=Math.max(store.get("asmaul-best",0),score);store.set("asmaul-best",b);
      qz.innerHTML=`<p class="qzs">Markah anda: <strong>${score} / ${qs.length}</strong></p><p class="note">Markah terbaik: ${b} / 10</p><button class="btn3" type="button" data-aq>Cuba lagi</button>`;return}
    const i=qs[qi],opts=shuffle([i,...shuffle([...Array(99).keys()].filter(x=>x!==i)).slice(0,3)]);qz.dataset.o=opts.join(",");
    qz.innerHTML=`<p class="qzn">Soalan ${qi+1} daripada ${qs.length} · Markah ${score}</p><p class="qzw" lang="ar" dir="rtl">${esc(N[i][0])}</p><p class="qzr">Apakah maksud nama ini?</p><div class="qzo">${opts.map(o=>`<button class="btn2" type="button" data-o="${o}">${esc(N[o][2])}</button>`).join("")}</div><p class="qzf" aria-live="polite"></p>`};
  qz.addEventListener("click",e=>{
    if(e.target.closest("[data-aq]")){qs=shuffle([...Array(99).keys()]).slice(0,10);qi=0;score=0;ask();return}
    if(e.target.closest("[data-next]")){qi++;ask();return}
    const b=e.target.closest("button[data-o]");if(!b||b.disabled)return;const i=qs[qi],ok=+b.dataset.o===i;if(ok)score++;
    $$("button[data-o]",qz).forEach(x=>{x.disabled=true;if(+x.dataset.o===i)x.classList.add("ok");else if(x===b)x.classList.add("no")});
    $(".qzf",qz).innerHTML=`${ok?"✓ Betul.":"✗ Jawapan:"} <strong>${esc(N[i][1])}</strong>: ${esc(N[i][2])}<br><button class="btn2" type="button" data-next>Seterusnya ›</button>`});
  $("#anmode").addEventListener("click",e=>{const b=e.target.closest("button[data-m]");if(!b)return;const m=b.dataset.m;
    $$("#anmode button").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));$("#anlist").hidden=m!=="senarai";$("#ankad").hidden=m!=="kad";$("#ankuiz").hidden=m!=="kuiz";
    if(m==="kad")drawK();if(m==="kuiz"&&!qs.length)qz.innerHTML='<p>10 soalan rawak: pilih maksud bagi setiap nama.</p><button class="btn3" type="button" data-aq>Mula kuiz</button>'});
  toolbar($("#kira > .act"),{});
}

const qf=$("#qf");
if(qf){
  const qsum=$("#qsum");
  const run=()=>{
    const y=clamp($("#qy").value,0,80,0),m=clamp($("#qm").value,0,11,0),d=clamp($("#qd").value,0,29,0),s=clamp($("#qs").value,1,5,1),days=y*365+m*30+d;
    if(days<=0)return setIf(qsum,"<p>Masukkan tempoh solat fardu yang tertinggal.</p>");
    const fd=Math.ceil(days/s);
    setIf(qsum,`<p><strong>${num(days*5)} solat fardu</strong> perlu diqada (${num(days)} hari × 5 waktu), iaitu ${num(days*17)} rakaat.</p><p>Dengan ${s} set qada sehari (setiap set = Subuh, Zohor, Asar, Maghrib, Isyak), selesai dalam <strong>${num(fd)} hari</strong> (≈ ${r1(fd/30)} bulan): <strong>${dlong(addD(today(),fd-1))}</strong>.</p>`);
  };
  qf.addEventListener("input",run);qf.addEventListener("change",run);qf.addEventListener("submit",e=>{e.preventDefault();run()});run();
}

/* ---------- belajar iqra': drills generated per level (level 1 default mirrors tools/pages4.py iq_items) ---------- */
const iqEl=$("#iqd-data");
if(iqEl){
  const D=JSON.parse(iqEl.textContent),g=$("#iqg"),desc=$("#iqd"),rm=$("#iqrm"),tts=$("#iqtts"),done=$("#iqdone"),prog=$("#iqprog");
  const F="َ",V={a:F,i:"ِ",u:"ُ"},SK="ْ",SD="ّ",TN={a:"ًا",i:"ٍ",u:"ٌ"};
  const H=D.h.filter(h=>h[0]!=="ا"&&h[0]!=="ء"),has=s=>h=>s.includes(h[0]);
  const QAM=H.filter(has("بغحجكوخفعقيمه")),SYM=H.filter(has("تثدذرزسشصضطظلن")),QAL=H.filter(has(D.qal));
  const pk=a=>a[Math.floor(Math.random()*a.length)],rnd=p=>Math.random()<p;
  const vr=(h,v)=>h[2]+(v==="a"&&h[3]?"o":v);
  let L=1,speak=false,st=store.get("iqra",{d:[],n:0});
  function syl(h,v,last){
    let ar=h[0]+V[v],ru=vr(h,v);
    if(L>=4&&last&&rnd(.35)){ar=h[0]+TN[v];ru+="n"}
    else if(L>=2&&rnd(.3)&&!(last&&L>=4)){ar+=v==="a"?"ا":v==="i"?"ي":"و";ru+=ru.slice(-1)}
    else if(L>=4&&!last&&rnd(.4)){const c=rnd(.5)?pk(QAL):pk(H);ar+=c[0]+SK;ru+=c[2]}
    return[ar,ru];
  }
  function word(){
    const n=L===1?1+Math.floor(Math.random()*3):2+Math.floor(Math.random()*2);let ar="",ru=[],k=0;
    if(L===5){
      const p=Math.random();
      if(p<.34){ar="اَلْ";ru.push("al")}
      else if(p<.67){const h=pk(SYM);ar="اَل"+h[0]+SD+F;ru.push("a"+h[2],vr(h,"a"));k=1}
      else{const h1=pk(H),h=pk(H);ar=h1[0]+F+h[0]+SD+F;ru.push(vr(h1,"a")+h[2],vr(h,"a"));k=1}
    }
    for(;k<n;k++){
      const last=k===n-1,v=L<3?"a":L===5&&last?"u":pk(["a","a","i","u"]),h=L===5&&!k?pk(QAM):pk(H);
      const[a,r]=L===5?[h[0]+V[v],vr(h,v)]:syl(h,v,last);ar+=a;ru.push(r);
    }
    return[ar,ru.join("-")];
  }
  const item=(ar,ru,wide)=>`<li><button type="button" class="iqi${wide?" w":""}"><span class="iqa" lang="ar" dir="rtl">${ar}</span><span class="iqr">${esc(ru)}</span></button></li>`;
  function gen(count){
    if(L===6)setIf(g,shuffle([...D.q6]).slice(0,4).map(q=>item(esc(q[2]),`${q[3]} · ${q[4]}`,true)).join(""));
    else setIf(g,Array.from({length:12},()=>item(...word(),false)).join(""));
    if(count){st.n++;store.set("iqra",st)}paint();
  }
  function paint(){
    const lv=D.lv[L-1];setIf(desc,`<strong>${esc(lv[2])}.</strong> ${esc(lv[3])}`);
    $$("#iql button").forEach(b=>b.setAttribute("aria-pressed",String(+b.dataset.l===L)));
    done.setAttribute("aria-pressed",String(st.d.includes(L)));done.textContent=st.d.includes(L)?"✓ Tahap ini selesai":"✓ Tanda tahap selesai";
    prog.textContent=`Tahap selesai: ${st.d.length} / 6${st.d.length?" ("+[...st.d].sort().map(x=>"Iqra' "+x).join(", ")+")":""} · ${st.n} latihan dijana`;
  }
  $("#iql").addEventListener("click",e=>{const b=e.target.closest("button[data-l]");if(!b)return;L=+b.dataset.l;store.set("iqra-l",L);gen(false)});
  $("#iqgen").addEventListener("click",()=>gen(true));
  rm.addEventListener("click",()=>{const on=!g.classList.contains("show");g.classList.toggle("show",on);rm.setAttribute("aria-pressed",String(on))});
  done.addEventListener("click",()=>{st.d=st.d.includes(L)?st.d.filter(x=>x!==L):[...st.d,L];store.set("iqra",st);paint();if(st.d.includes(L))toast(`Iqra' ${L} ditanda selesai ✓`)});
  g.addEventListener("click",e=>{const b=e.target.closest(".iqi");if(!b)return;b.classList.toggle("on");if(speak)speech.say($(".iqa",b).textContent)});
  speech.init(ok=>{tts.hidden=!ok});
  tts.addEventListener("click",()=>{speak=!speak;tts.setAttribute("aria-pressed",String(speak));if(speak)toast("Ketik kotak untuk mendengar")});
  tts.setAttribute("aria-pressed","false");
  const l0=clamp(store.get("iqra-l",1),1,6,1);if(l0!==1){L=l0;gen(false)}else paint();
}

/* ---------- belajar mengaji: huruf hijaiyah explorer, quiz, progress checklist ---------- */
const hjEl=$("#hjdata");
if(hjEl){
  const D=JSON.parse(hjEl.textContent),H=D.h,MK=Object.fromEntries(D.mk),out=$("#hjd"),ZW="‍";
  const forms=h=>h[0]==="ء"?["ء","ء","ء","ء"]:h[4]?[h[0],h[0]+ZW,ZW+h[0]+ZW,ZW+h[0]]:[h[0],h[0],ZW+h[0],ZW+h[0]];
  function variants(h){
    if(h[0]==="ا")return[["أَ","a"],["إِ","i"],["أُ","u"],["آ","aa (mad)"]];
    const c=h[0],r=h[2],o=h[3]?"o":"a",v=[[c+"َ",r+o],[c+"ِ",r+"i"],[c+"ُ",r+"u"],[c+(c==="ء"?"ً":"ًا"),r+o+"n"],[c+"ٍ",r+"in"],[c+"ٌ",r+"un"]];
    if(c!=="ء")v.push(["اَ"+c+"ْ","a"+r],["اَ"+c+"َّ","a"+r+"-"+r+o]);
    return v;
  }
  function show(i){
    const h=H[i],f=forms(h);
    out.innerHTML=`<div class="hjt"><span class="hjb" lang="ar">${h[0]}</span><div><p class="hjh"><strong>${esc(h[1])}</strong> · huruf ke-${i+1} daripada ${H.length}</p><p>Makhraj: <strong>${esc(MK[h[5]])}</strong></p><p class="note">${esc(h[6])}</p></div></div>`+
      `<p class="hjfh">Bentuk tulisan</p><ul class="hjf">${["Tunggal","Awal","Tengah","Akhir"].map((n,k)=>`<li><span lang="ar">${f[k]}</span>${n}</li>`).join("")}</ul>`+
      `<p class="hjfh">Bacaan dengan baris${speech.v?" (ketik untuk dengar)":""}</p><ul class="hjv">${variants(h).map(([a,r])=>`<li><button type="button" class="iqi on" data-say="${a}"><span class="iqa" lang="ar" dir="rtl">${a}</span><span class="iqr">${esc(r)}</span></button></li>`).join("")}</ul>`+
      (h[4]?"":`<p class="note">${h[0]==="ء"?"Hamzah boleh ditulis bersendirian atau di atas alif, wau dan ya (أ ؤ ئ).":"Huruf ini tidak bersambung dengan huruf selepasnya."}</p>`);
  }
  speech.init();
  $("#hjg").addEventListener("click",e=>{const b=e.target.closest("button[data-i]");if(!b)return;$$("#hjg button").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));show(+b.dataset.i);speech.say(H[+b.dataset.i][0]);out.scrollIntoView({block:"nearest",behavior:"smooth"})});
  out.addEventListener("click",e=>{const b=e.target.closest("[data-say]");if(b)speech.say(b.dataset.say)});
  // quiz
  const qz=$("#hqz");let mode="nama",qs=[],qi=0,score=0;
  const ans=h=>mode==="nama"?h[1]:mode==="makhraj"?MK[h[5]]:h[0];
  const ask=()=>{
    if(qi>=qs.length){const best=store.get("hijaiyah-best",{}),b=Math.max(best[mode]||0,score);best[mode]=b;store.set("hijaiyah-best",best);
      qz.innerHTML=`<p class="qzs">Markah anda: <strong>${score} / ${qs.length}</strong> ${score===qs.length?"— Masya-Allah, sempurna!":score>=qs.length*.7?"— Bagus!":"— Ulang kaji grid huruf di atas dan cuba lagi."}</p><p class="note">Markah terbaik (jenis ini): ${b} / ${qs.length}</p><button class="btn3" type="button" data-hq>Cuba lagi</button>`;return}
    const h=qs[qi],ar=mode==="huruf"||mode==="bentuk",pool=mode==="makhraj"?D.mk.map(m=>m[1]):[...new Set(H.map(ans))];
    const opts=shuffle([ans(h),...shuffle(pool.filter(x=>x!==ans(h))).slice(0,3)]);
    const q=mode==="huruf"?`<p class="qzw hq">${esc(h[1])}</p><p class="qzr">Huruf manakah ini?</p>`:mode==="bentuk"?`<p class="qzw" lang="ar" dir="rtl">${forms(h)[2]}</p><p class="qzr">Bentuk tengah huruf apa?</p>`:`<p class="qzw" lang="ar" dir="rtl">${h[0]}</p><p class="qzr">${mode==="nama"?"Apakah nama huruf ini?":"Dari kawasan makhraj manakah huruf ini?"}</p>`;
    qz.innerHTML=`<p class="qzn">Soalan ${qi+1} daripada ${qs.length} · Markah ${score}</p>${q}<div class="qzo">${opts.map((o,k)=>`<button class="btn2${ar?" qar":""}" type="button" data-k="${k}"${ar?' lang="ar"':""}>${esc(o)}</button>`).join("")}</div><p class="qzf" aria-live="polite"></p>`;
    qz.dataset.opts=JSON.stringify(opts);
  };
  $("#hqm").addEventListener("click",e=>{const b=e.target.closest("button[data-m]");if(!b)return;mode=b.dataset.m;$$("#hqm button").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));qs=[];qz.innerHTML=`<p>10 soalan rawak. Markah terbaik bagi setiap jenis kuiz disimpan dalam pelayar anda.</p><button class="btn3" type="button" data-hq>Mula kuiz</button>`});
  qz.addEventListener("click",e=>{
    if(e.target.closest("[data-hq]")){qs=shuffle([...H]).slice(0,10);qi=0;score=0;ask();return}
    if(e.target.closest("[data-next]")){qi++;ask();return}
    const b=e.target.closest("button[data-k]");if(!b||b.disabled)return;
    const opts=JSON.parse(qz.dataset.opts),h=qs[qi],right=ans(h),ok=opts[+b.dataset.k]===right;if(ok)score++;
    $$("button[data-k]",qz).forEach(x=>{x.disabled=true;if(opts[+x.dataset.k]===right)x.classList.add("ok");else if(x===b)x.classList.add("no")});
    $(".qzf",qz).innerHTML=`${ok?"✓ Betul.":`✗ Jawapan: <strong>${esc(right)}</strong>.`} ${esc(h[1])} (${h[0]}): ${esc(h[6])}<br><button class="btn2" type="button" data-next>Seterusnya ›</button>`;
  });
  // checklist
  const ml=$("#msl"),msp=$("#msp");
  const paintM=()=>{const st=store.get("mengaji",{}),cs=$$("input[data-m]",ml);let k=0;cs.forEach(c=>{c.checked=!!st[c.dataset.m];if(c.checked)k++});msp.textContent=`${k} / ${cs.length} selesai${k===cs.length?" — Alhamdulillah! Teruskan dengan khatam Al-Quran.":""}`};
  ml.addEventListener("change",e=>{const c=e.target.closest("input[data-m]");if(!c)return;const st=store.get("mengaji",{});if(c.checked)st[c.dataset.m]=1;else delete st[c.dataset.m];store.set("mengaji",st);paintM()});
  paintM();
}
})();
