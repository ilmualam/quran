/*! IlmuAlam Quran Tools v1.0 | © ilmualam.com | khatam, hafazan, tasbih, cari ayat. Schedule maths mirror tools/plans.py */
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

/* ---------- waktu solat (maths mirror tools/solat.py) ---------- */
const sw=$("#sw");
if(sw){
  const S=JSON.parse($("#sd").textContent),C=S.c,NM=S.n,rad=x=>x*Math.PI/180,deg=x=>x*180/Math.PI,mod=(x,n)=>(x%n+n)%n;
  function sun(jd){const D=jd-2451545,g=mod(357.529+.98560028*D,360),q=mod(280.459+.98564736*D,360),L=mod(q+1.915*Math.sin(rad(g))+.02*Math.sin(rad(2*g)),360),e=23.439-.00000036*D;
    const ra=mod(deg(Math.atan2(Math.cos(rad(e))*Math.sin(rad(L)),Math.cos(rad(L))))/15,24),decl=deg(Math.asin(Math.sin(rad(e))*Math.sin(rad(L))));let eqt=q/15-ra;eqt=eqt-24*Math.round(eqt/24);return[decl,eqt]}
  function jdn(y,m,d){if(m<=2){y-=1;m+=12}const A=Math.floor(y/100),B=2-A+Math.floor(A/4);return Math.floor(365.25*(y+4716))+Math.floor(30.6001*(m+1))+d+B-1524.5}
  function day(y,m,d,lat,lng){
    const jd=jdn(y,m,d)-lng/(15*24),noon=t=>mod(12-sun(jd+t)[1],24);
    const at=(a,t,ccw)=>{const decl=sun(jd+t)[0];const x=(-Math.sin(rad(a))-Math.sin(rad(decl))*Math.sin(rad(lat)))/(Math.cos(rad(decl))*Math.cos(rad(lat)));const T=deg(Math.acos(Math.max(-1,Math.min(1,x))))/15;return noon(t)+(ccw?-T:T)};
    const asr=t=>{const decl=sun(jd+t)[0];return at(-deg(Math.atan(1/(1+Math.tan(rad(Math.abs(lat-decl)))))),t,false)};
    let f=at(S.fa,5/24,true),sr=at(.833,6/24,true),z=noon(12/24),a=asr(13/24),mg=at(.833,18/24,false),i=at(S.is,18/24,false);
    const adj=S.tz-lng/15;[f,sr,z,a,mg,i]=[f,sr,z,a,mg,i].map(x=>(x+adj)*60);
    const up=x=>Math.ceil(x+1),sub=up(f);return[sub-10,sub,Math.floor(sr),Math.ceil(z+2),up(a),up(mg),up(i)];
  }
  const hm=x=>`${pad(Math.floor(x/60))}:${pad(x%60)}`;
  const qibla=(lat,lng)=>{const p1=rad(lat),p2=rad(21.4225),dl=rad(39.8262-lng);return mod(deg(Math.atan2(Math.sin(dl),Math.cos(p1)*Math.tan(p2)-Math.sin(p1)*Math.cos(dl))),360)};
  const sel=$("#sc"),list=$("#stimes"),tb=$("#smon tbody"),nx=$("#snext"),src=$("#ssrc"),hij=$("#shij"),qb=$("#sqib"),cap=$("#smcap"),dt0=$("#sdate");
  const cache={};let cur=null,avail=null;
  function official(zone,y){
    const k=zone+"-"+y;
    avail=avail||fetch("/assets/data/solat/index.json").then(r=>r.ok?r.json():[]).catch(()=>[]);
    return avail.then(a=>{
      if(!zone||!a.includes(k))return null;
      if(!(k in cache))cache[k]=fetch(`/assets/data/solat/${k}.json`).then(r=>r.ok?r.json():null).catch(()=>null);
      return cache[k];
    });
  }
  const doy=d=>Math.round((new Date(d.getFullYear(),d.getMonth(),d.getDate())-new Date(d.getFullYear(),0,1))/864e5);
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
})();
