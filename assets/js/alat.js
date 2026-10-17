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
})();
