/*! IlmuAlam Nama Bayi Islam v1.0 | © ilmualam.com | quran.ilmualam.com/nama-bayi-islam/ | data: /assets/data/nama-bayi.json (tools/nama.py). card() and fullCard() mirror tools/pages17.py */
(()=>{"use strict";
const app=document.getElementById("nbapp");if(!app)return;
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const num=n=>String(n).replace(/\B(?=(\d{3})+(?!\d))/g,",");
const KEY="ilmq:nama-simpan",MAXS=50,PER=30;
const GL={L:"Lelaki",P:"Perempuan",U:"Uniseks"},SRC={n:"Nabi & keluarga",s:"Sahabat & tokoh",u:"Umum"};
const PATTERNS={L:[["m2","Muhammad + 2 nama","Muhammad",2],["a2","Ahmad + 2 nama","Ahmad",2],["m1","Muhammad + 1 nama","Muhammad",1],["x2","2 nama (tanpa awalan)","",2],["x1","1 nama sahaja","",1],["ab","Abdul + Asmaul Husna","",0]],
  P:[["n2","Nur + 2 nama","Nur",2],["n1","Nur + 1 nama","Nur",1],["nl1","Nurul + 1 nama","Nurul",1],["s1","Siti + 1 nama","Siti",1],["x2","2 nama (tanpa awalan)","",2],["x1","1 nama sahaja","",1]]};
// prefixes that are not rows of their own in the data
const EXTRA={Nurul:{n:"Nurul",a:"نُورُ الْ",m:"Cahaya (bagi perkataan selepasnya)"},Siti:{n:"Siti",a:"",m:"Gelaran hormat wanita Melayu (puan)"}};
const ALLAH_ONLY={allah:"Allah",rahman:"Ar-Rahman",ahad:"Al-Ahad",samad:"As-Samad",khaliq:"Al-Khaliq",razzaq:"Ar-Razzaq",razak:"Ar-Razzaq",quddus:"Al-Quddus",jabbar:"Al-Jabbar",mutakabbir:"Al-Mutakabbir",qahhar:"Al-Qahhar",kahhar:"Al-Qahhar",ghaffar:"Al-Ghaffar",gaffar:"Al-Ghaffar",wahhab:"Al-Wahhab",wahab:"Al-Wahhab",muhaimin:"Al-Muhaimin",qayyum:"Al-Qayyum",musawwir:"Al-Musawwir",bari:"Al-Bari'"};
const MAKRUH={yasar:"Yasar",aflah:"Aflah",rabah:"Rabah",najih:"Najih",nafi:"Nafi'",naafi:"Nafi'",barrah:"Barrah"};
const ABD=new Set(["abdul","abd","abdur","abdel","abdil","abdu","abdus","abdurr"]);
const MD={mohd:"Muhammad",md:"Muhammad",mohamad:"Muhammad",mohammad:"Muhammad",mohamed:"Muhammad",muhamad:"Muhammad",mohammed:"Muhammad"};
const BIN=new Set(["bin","binti","bt","bte","bnt","b.","bt.","ibni","ibnu"]);

let toastEl,toastT;
function toast(m){toastEl=toastEl||Object.assign(document.body.appendChild(document.createElement("div")),{className:"toast",role:"status"});toastEl.textContent=m;toastEl.classList.add("on");clearTimeout(toastT);toastT=setTimeout(()=>toastEl.classList.remove("on"),1800)}
function copy(text,msg){
  const ok=()=>toast(msg),fb=()=>{const t=document.createElement("textarea");t.value=text;t.setAttribute("readonly","");t.style.cssText="position:fixed;opacity:0";document.body.appendChild(t);t.select();try{document.execCommand("copy");ok()}catch{}t.remove()};
  if(navigator.clipboard&&isSecureContext)navigator.clipboard.writeText(text).then(ok,fb);else fb();
}
const store={get(){try{const v=JSON.parse(localStorage.getItem(KEY)||"[]");return Array.isArray(v)?[...new Set(v.filter(x=>typeof x==="string"&&x.length<120))].slice(0,MAXS):[]}catch{return[]}},
  set(v){try{localStorage.setItem(KEY,JSON.stringify(v))}catch{}}};

// seeded RNG so a shared settings link reproduces the same 12 names
function rng(seed){let a=seed>>>0;return()=>{a=a+0x6D2B79F5>>>0;let t=a;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296}}
const loose=s=>String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/['’‘`\-\s.]/g,"")
  .replace(/kh/g,"k").replace(/gh/g,"g").replace(/sy|sh/g,"s").replace(/dh|dz|zh/g,"z").replace(/th/g,"t").replace(/q/g,"k")
  .replace(/ee|ie/g,"i").replace(/oo|ou/g,"u").replace(/o/g,"u").replace(/e/g,"i").replace(/y/g,"i").replace(/w/g,"u")
  .replace(/(.)\1+/g,"$1").replace(/([aiu])h$/,"$1");
const akey=a=>String(a).replace(/[ً-ٰٟ]/g,"").replace(/[أإآ]/g,"ا").replace(/\s/g,"");

let D=null,ROWS=[],LIST=[],SN=[],TH={},BYLOW=new Map(),BYLOOSE=new Map(),VAR=new Map(),ABDSET=new Map();
let saved=store.get();
const ready=fetch("/assets/data/nama-bayi.json").then(r=>{if(!r.ok)throw new Error(r.status);return r.json()}).then(j=>{
  D=j;SN=j.sn;TH=j.themes;
  ROWS=j.n.map(x=>({n:x[0],a:x[1],m:x[2],g:x[3],s:x[4],y:x[5],t:x[6],f:x[7],r:x[8],c:x[9],k:x[10],low:x[0].toLowerCase(),lo:loose(x[0]),ak:akey(x[1])}));
  LIST=ROWS.filter(r=>r.f!=="a");
  for(const r of ROWS){
    (BYLOW.get(r.low)||BYLOW.set(r.low,[]).get(r.low)).push(r);
    (BYLOOSE.get(r.lo)||BYLOOSE.set(r.lo,[]).get(r.lo)).push(r);
    if(r.f!=="a"){const k=r.ak+"|"+r.g;(VAR.get(k)||VAR.set(k,[]).get(k)).push(r.n)}
    if(r.f==="b")ABDSET.set(loose(r.n.slice(6)),r);
  }
  return j;
}).catch(()=>{$("#nbln").textContent="Data nama gagal dimuatkan. Semak sambungan internet dan muat semula halaman.";return null});

/* ---------- shared markup (mirror of tools/pages17.py) ---------- */
function refa(r){
  if(r.k)return`<a href="/kisah-nabi/${r.k}/">📜 Kisah Nabi</a>`;
  if(!r.r)return"";const[s,a]=r.r.split(":");
  return`<a href="/#surah-${s}-ayat-${a}" title="Perkataan ini terdapat dalam Al-Quran">📖 ${esc(SN[s-1])} ${s}:${a}${r.c>1?` · ${r.c}×`:""}</a>`;
}
function card(r){
  const th=[...r.t.slice(0,2)].map(t=>`<span>${TH[t]}</span>`).join("");
  const v=(VAR.get(r.ak+"|"+r.g)||[]).filter(x=>x!==r.n).slice(0,4);
  const on=saved.includes(r.n);
  return`<li class="nbc"><button class="nbs" type="button" data-save="${esc(r.n)}" aria-pressed="${on}" aria-label="Simpan ${esc(r.n)}">${on?"♥":"♡"}</button>`+
    `<p class="nbn">${esc(r.n)}</p><p class="nba" lang="ar" dir="rtl">${esc(r.a)}</p><p class="nbm">${esc(r.m)}</p>${v.length?`<p class="nbv">Ejaan lain: ${esc(v.join(", "))}</p>`:""}`+
    `<p class="nbt"><span class="g${r.g}">${GL[r.g]}</span>${r.f==="a"?'<span class="nbaw">Awalan</span>':""}<span>${SRC[r.s]}</span><span>${r.y} suku kata</span>${th}${refa(r)}</p></li>`;
}
function fullCard(parts,father,g){
  const nm=parts.map(p=>p.n).join(" "),on=saved.includes(nm);
  const bin=father?` <span class="nbfb">${g==="P"?"binti":"bin"} ${esc(father)}</span>`:"";
  return`<li class="nbf"><button class="nbs" type="button" data-save="${esc(nm)}" aria-pressed="${on}" aria-label="Simpan ${esc(nm)}">${on?"♥":"♡"}</button>`+
    `<p class="nbff">${esc(nm)}${bin}</p><p class="nba" lang="ar" dir="rtl">${esc(parts.map(p=>p.a).filter(Boolean).join(" "))}</p>`+
    `<p class="nbm">${parts.map(p=>`<b>${esc(p.n)}</b>: ${esc(p.m)}`).join(" · ")}</p></li>`;
}

/* ---------- shortlist ---------- */
function paintSaved(){
  $$(".nbcnt").forEach(x=>x.textContent=saved.length);
  $$("button[data-save]").forEach(b=>{const on=saved.includes(b.dataset.save);b.setAttribute("aria-pressed",on);b.textContent=on?"♥":"♡"});
  const ol=$("#nbsv");
  if(!saved.length){ol.innerHTML='<li class="nbe">Tekan ♡ pada mana-mana nama untuk menyimpannya di sini. Senarai disimpan dalam peranti ini sahaja.</li>';return}
  ol.innerHTML=saved.map((n,i)=>`<li><div><strong>${esc(n)}</strong><span class="nbm">${esc(meaningOf(n))}</span></div><span class="nbsa"><button class="btn2 sm" type="button" data-up="${i}" aria-label="Naikkan ${esc(n)}"${i?"":" disabled"}>↑</button><button class="btn2 sm" type="button" data-rm="${i}" aria-label="Buang ${esc(n)}">✕</button></span></li>`).join("");
}
function meaningOf(full){
  if(!D)return"";
  return full.split(/\s+/).reduce((o,w,i,a)=>{
    if(o.skip){o.skip=false;return o}
    const lw=loose(w);
    if(ABD.has(lw)&&a[i+1]){const r=ABDSET.get(loose(a[i+1]));if(r){o.out.push(r.m.replace(/\s*Antara.*$/,""));o.skip=true;return o}}
    const r=(BYLOW.get(w.toLowerCase())||BYLOOSE.get(lw)||[])[0]||EXTRA[w];
    if(r)o.out.push(`${w}: ${r.m}`);return o;
  },{out:[],skip:false}).out.join(" · ");
}
function toggleSave(n){
  const i=saved.indexOf(n);
  if(i>=0){saved.splice(i,1);toast("Dibuang daripada senarai")}
  else{if(saved.length>=MAXS){toast(`Had ${MAXS} nama dicapai`);return}saved.push(n);toast(`${n} disimpan ♥`)}
  store.set(saved);paintSaved();
}
app.addEventListener("click",e=>{
  const b=e.target.closest("button[data-save]");if(b){toggleSave(b.dataset.save);return}
  const rm=e.target.closest("button[data-rm]");if(rm){saved.splice(+rm.dataset.rm,1);store.set(saved);paintSaved();return}
  const up=e.target.closest("button[data-up]");if(up){const i=+up.dataset.up;if(i>0){[saved[i-1],saved[i]]=[saved[i],saved[i-1]];store.set(saved);paintSaved()}return}
  const sv=e.target.closest("button[data-sv]");if(sv)shortAct(sv.dataset.sv);
});
const shareText=()=>"Senarai nama bayi pilihan kami:\n"+saved.map((n,i)=>`${i+1}. ${n}${meaningOf(n)?` (${meaningOf(n)})`:""}`).join("\n");
const shareLink=()=>location.origin+location.pathname+"#senarai="+encodeURIComponent(saved.join("|"));
function shortAct(a){
  if(a!=="clear"&&!saved.length){toast("Senarai masih kosong");return}
  if(a==="copy")copy(shareText(),"Senarai disalin ✓");
  else if(a==="link")copy(shareLink(),"Pautan disalin ✓ Hantar kepada pasangan anda");
  else if(a==="wa")window.open("https://wa.me/?text="+encodeURIComponent(shareText()+"\n\nLihat & undi: "+shareLink()),"_blank","noopener");
  else if(a==="clear"&&saved.length&&confirm("Kosongkan senarai pendek?")){saved=[];store.set(saved);paintSaved()}
}
function sharedList(){
  const m=/^#senarai=(.+)$/.exec(location.hash);if(!m)return;
  let names=[];try{names=decodeURIComponent(m[1]).split("|").map(s=>s.trim().replace(/[<>"]/g,"")).filter(s=>s&&s.length<120).slice(0,MAXS)}catch{return}
  if(!names.length)return;
  const box=$("#nbsh");
  box.innerHTML=`<div class="box nbshx"><p><strong>Senarai yang dikongsi dengan anda (${names.length} nama):</strong></p><ol>${names.map(n=>`<li><strong>${esc(n)}</strong> <span class="nbm">${esc(meaningOf(n))}</span></li>`).join("")}</ol><button class="btn3" type="button" id="nbshi">♥ Simpan semua ke senarai saya</button></div>`;
  $("#nbshi").addEventListener("click",()=>{for(const n of names)if(!saved.includes(n)&&saved.length<MAXS)saved.push(n);store.set(saved);paintSaved();toast("Disimpan ✓")});
  $("#simpan").scrollIntoView();
}

/* ---------- generator ---------- */
const G={j:$("#nbgj"),c:$("#nbgc"),h:$("#nbgh"),t:$("#nbgt"),s:$("#nbgs"),k:$("#nbgk"),b:$("#nbgb"),x:$("#nbgx"),w:$("#nbgw")};
let seed=0;
function setPatterns(g,keep){
  const cur=keep||G.c.value;
  G.c.innerHTML=PATTERNS[g].map(([v,t])=>`<option value="${v}">${esc(t)}</option>`).join("");
  G.c.value=PATTERNS[g].some(p=>p[0]===cur)?cur:PATTERNS[g][0][0];
}
G.j.addEventListener("change",()=>setPatterns(G.j.value));
function pool(g,{h,t,s},father,all){
  const fl=father?loose(father):"",ed=G.w.checked&&!all;
  return LIST.filter(r=>(ed?r.f==="e"&&r.g===g:(r.g===g||r.g==="U"))&&r.f!=="b"&&!r.n.includes(" ")&&r.lo!==fl&&!["muhammad","ahmad","nur"].includes(r.low)&&
    (!h||r.n[0].toUpperCase()===h)&&(!t||r.t.includes(t))&&(!s||(s==="q"?!!r.r:"ns".includes(r.s))));
}
function rowOf(n,g){return(BYLOW.get(n.toLowerCase())||[]).find(r=>r.g===g||r.g==="U")||EXTRA[n]}
function generate(newSeed){
  if(!D)return;
  const g=G.j.value,pat=PATTERNS[g].find(p=>p[0]===G.c.value)||PATTERNS[g][0],[,label,pre,nparts]=pat;
  const father=G.b.value.trim().split(/\s+/)[0]||"";
  const h=G.x.checked&&father?father[0].toUpperCase():G.h.value,t=G.t.value,s=G.s.value,K=+G.k.value||0;
  if(newSeed!==false)seed=Math.floor(Math.random()*1e9);
  const R=rng(seed),out=[],seen=new Set();
  let total=0,note="";
  if(nparts===0){
    const ab=ROWS.filter(r=>r.f==="b"&&(!h||r.n[6]&&r.n[6].toUpperCase()===h));
    total=ab.length;
    const sh=ab.slice();for(let i=sh.length-1;i>0;i--){const j=Math.floor(R()*(i+1));[sh[i],sh[j]]=[sh[j],sh[i]]}
    for(const r of sh.slice(0,12))out.push([r]);
  }else{
    let A=pool(g,{h,t,s},father),B=pool(g,{h:"",t,s},father);
    if(B.length<12){B=pool(g,{h:"",t:"",s:""},father);note=" (tema/sumber dilonggarkan untuk nama kedua)"}
    if(A.length<4&&G.w.checked){A=pool(g,{h,t,s},father,1);B=pool(g,{h:"",t,s},father,1);if(B.length<12)B=pool(g,{h:"",t:"",s:""},father,1);note=" (pilihan editor terlalu sedikit untuk tetapan ini, semua nama digunakan)"}
    if(A.length&&nparts===2&&K)A=A.filter(r=>r.y<K);
    total=nparts===1?A.filter(r=>!K||r.y<=K).length:A.length*Math.max(0,B.length-1);
    const preRow=pre?rowOf(pre,g):null;
    for(let tries=0;out.length<12&&tries<3000&&A.length;tries++){
      const a=A[Math.floor(R()*A.length)];
      if(nparts===1){if(K&&a.y>K)continue;if(seen.has(a.n))continue;seen.add(a.n);out.push(preRow?[preRow,a]:[a]);continue}
      const b=B[Math.floor(R()*B.length)];
      if(!b||b.ak===a.ak||b.n===a.n||(K&&a.y+b.y>K))continue;
      const k=a.n+" "+b.n;if(seen.has(k))continue;seen.add(k);
      out.push(preRow?[preRow,a,b]:[a,b]);
    }
  }
  $("#nbgr").innerHTML=out.length?out.map(p=>fullCard(p,father,g)).join(""):'<li class="nbe">Tiada nama sepadan. Longgarkan huruf, tema, sumber atau had suku kata.</li>';
  $("#nbgn").textContent=`${label}: ${num(total)} gabungan mungkin dengan tetapan ini${note}`;
  history.replaceState(null,"","#"+new URLSearchParams({j:g,c:pat[0],h:G.h.value,t,s,k:G.k.value,b:father,x:G.x.checked?1:0,w:G.w.checked?1:0,r:seed}).toString());
}
$("#nbgo").addEventListener("click",()=>ready.then(()=>generate()));
$("#nbgf").addEventListener("change",e=>{if(e.target!==G.b)ready.then(()=>generate())});
$("#nbgb").addEventListener("change",()=>ready.then(()=>generate(false)));
$("#nbgl").addEventListener("click",()=>{ready.then(()=>{if(!seed)generate();copy(location.href,"Pautan tetapan disalin ✓")})});
function fromHash(){
  const p=new URLSearchParams(location.hash.slice(1));if(!p.has("j"))return false;
  const g=p.get("j")==="P"?"P":"L";G.j.value=g;setPatterns(g,p.get("c"));
  for(const k of["h","t","s","k"]){const el=G[k];const v=p.get(k)||"";if([...el.options].some(o=>o.value===v))el.value=v}
  G.b.value=(p.get("b")||"").slice(0,40);G.x.checked=p.get("x")==="1";G.w.checked=p.get("w")!=="0";seed=+p.get("r")||0;
  generate(!seed);return true;
}

/* ---------- search & filter ---------- */
const F={q:$("#nblq"),g:$("#nblg"),h:$("#nblh"),e:$("#nble"),s:$("#nbls"),t:$("#nblt"),y:$("#nbly"),o:$("#nblo"),a:$("#nbla")};
let shown=PER,last=[],rseed=1;
function filter(){
  if(!D)return;
  const q=F.q.value.trim().toLowerCase(),ql=loose(q),g=F.g.value,h=F.h.value,en=F.e.value.trim().toLowerCase(),s=F.s.value,t=F.t.value,y=+F.y.value||0,o=F.o.value;
  let res=(F.a.checked?ROWS:LIST).filter(r=>(!g||r.g===g)&&(!h||r.n[0].toUpperCase()===h)&&(!en||r.low.endsWith(en))&&
    (!s||(s==="q"?!!r.r:s==="e"?r.f==="e"||r.f==="b":r.s===s))&&(!t||r.t.includes(t))&&(!y||(y===4?r.y>=4:r.y===y)));
  if(q){
    const sc=r=>r.low===q?0:r.lo===ql?1:r.low.startsWith(q)||r.lo.startsWith(ql)?2:r.low.includes(q)||(ql.length>2&&r.lo.includes(ql))?3:r.m.toLowerCase().includes(q)?4:9;
    res=res.map(r=>[sc(r),r]).filter(x=>x[0]<9).sort((a,b)=>a[0]-b[0]||a[1].low.localeCompare(b[1].low)).map(x=>x[1]);
  }else if(o==="za")res.sort((a,b)=>b.low.localeCompare(a.low));
  else if(o==="pd")res.sort((a,b)=>a.n.length-b.n.length||a.low.localeCompare(b.low));
  else if(o==="rw"){const R=rng(rseed);res=res.map(r=>[R(),r]).sort((a,b)=>a[0]-b[0]).map(x=>x[1])}
  else res.sort((a,b)=>a.low.localeCompare(b.low)||a.g.localeCompare(b.g));
  last=res;shown=PER;draw();
}
function draw(){
  const n=Math.min(shown,last.length);
  $("#nblr").innerHTML=n?last.slice(0,n).map(card).join(""):'<li class="nbe">Tiada nama sepadan. Cuba ejaan lain atau longgarkan tapisan.</li>';
  $("#nbln").textContent=`Memaparkan ${num(n)} daripada ${num(last.length)} nama`;
  $("#nblm").hidden=n>=last.length;
}
let qT;
$("#nblf").addEventListener("input",e=>{clearTimeout(qT);qT=setTimeout(()=>ready.then(filter),e.target===F.q||e.target===F.e?180:0)});
$("#nblf").addEventListener("submit",e=>e.preventDefault());
F.o.addEventListener("change",()=>{rseed=Math.floor(Math.random()*1e9)});
$("#nblm").addEventListener("click",()=>{shown+=PER;draw()});
$$(".nbaz a[data-h]").forEach(a=>a.addEventListener("click",()=>{F.h.value=a.dataset.h;ready.then(filter)}));

/* ---------- name checker ---------- */
function lev(a,b){if(Math.abs(a.length-b.length)>2)return 9;const d=[...Array(b.length+1).keys()];for(let i=1;i<=a.length;i++){let p=d[0];d[0]=i;for(let j=1;j<=b.length;j++){const t=d[j];d[j]=Math.min(d[j]+1,d[j-1]+1,p+(a[i-1]===b[j-1]?0:1));p=t}}return d[b.length]}
function suggest(w){const l=loose(w);return LIST.filter(r=>r.lo[0]===l[0]&&!r.n.includes(" ")).map(r=>[lev(l,r.lo),r]).filter(x=>x[0]<=2).sort((a,b)=>a[0]-b[0]||a[1].n.length-b[1].n.length).slice(0,5).map(x=>x[1].n)}
function check(text){
  const words=text.replace(/[^\p{L}\s'’.-]/gu," ").trim().split(/\s+/).filter(Boolean);
  if(!words.length)return'<p class="note">Taip sekurang-kurangnya satu nama.</p>';
  const bi=words.findIndex(w=>BIN.has(w.toLowerCase()));
  const child=bi>=0?words.slice(0,bi):words,father=bi>=0?words.slice(bi+1):[];
  const items=[];let bad=0,warn=0;
  const joined=child.join("").toLowerCase();
  if(/malik(ul|al)?mul[uo]k|syahansyah|shahanshah|malikulamlak/.test(joined)){bad++;items.push(["bad","Raja segala raja","Nama “raja segala raja” ialah nama paling hina di sisi Allah (HR Al-Bukhari 6205; Muslim 2143). Gantikan nama ini."])}
  for(let i=0;i<child.length;i++){
    const w=child[i],lw=loose(w),low=w.toLowerCase();
    if(ABD.has(lw)){
      const nx=child[i+1];
      if(!nx){warn++;items.push(["warn",w,"“Abdul” bermaksud hamba kepada; ia mesti disambung dengan salah satu Asmaul Husna."]);continue}
      const r=ABDSET.get(loose(nx))||(loose(nx)==="lah"||loose(nx)==="allah"?(BYLOW.get("abdullah")||[])[0]:null);
      if(r){items.push(["ok",`${w} ${nx}`,r.m,r.a]);i++;continue}
      bad++;items.push(["bad",`${w} ${nx}`,`“${nx}” bukan Asmaul Husna. Ulama sepakat melarang nama yang menghambakan diri kepada selain Allah (seperti Abdul Nabi atau Abdul Rasul). Jika ia ejaan lain bagi nama Allah, semak ejaan di halaman Asmaul Husna.`]);i++;continue;
    }
    if(MD[low]){items.push(["warn",w,`Singkatan atau ejaan lain bagi Muhammad. Ejaan penuh “Muhammad” lebih jelas maksudnya (yang sangat terpuji).`]);warn++;continue}
    if(ALLAH_ONLY[lw]||ALLAH_ONLY[low]){bad++;items.push(["bad",w,`${ALLAH_ONLY[lw]||ALLAH_ONLY[low]} ialah nama yang khusus bagi Allah. Gunakan “Abdul ${w}” (hamba kepada ${ALLAH_ONLY[lw]||ALLAH_ONLY[low]}).`]);continue}
    if(MAKRUH[lw]||MAKRUH[low]){warn++;const k=MAKRUH[lw]||MAKRUH[low];
      items.push(["warn",w,k==="Barrah"?"Rasulullah ﷺ menukar nama Barrah (yang sangat baik, memuji diri) kepada Zainab (HR Al-Bukhari 6192).":`${k} termasuk nama yang Rasulullah ﷺ larang (makruh, bukan haram) kerana jawapan “dia tiada” apabila ditanya tentangnya (HR Muslim 2136–2137).`]);continue}
    const rs=BYLOW.get(low)||BYLOOSE.get(lw)||(EXTRA[w[0].toUpperCase()+w.slice(1).toLowerCase()]?[EXTRA[w[0].toUpperCase()+w.slice(1).toLowerCase()]]:null);
    if(rs&&rs.length){
      const r=rs[0],gs=[...new Set(rs.map(x=>GL[x.g]).filter(Boolean))].join("/");
      const sp=r.n&&r.n.toLowerCase()!==low?` Ejaan dalam data: ${r.n}.`:"";
      const aw=r.f==="a"?" Ini awalan nama berganding: maksudnya lengkap bersama perkataan selepasnya.":"";
      const q=r.r?` Perkataan ini terdapat dalam Al-Quran (${SN[r.r.split(":")[0]-1]} ${r.r}).`:"";
      items.push(["ok",w,`${r.m}${gs?` · ${gs}`:""}.${sp}${aw}${q}`,r.a]);
    }else{warn++;const sg=suggest(w);items.push(["unk",w,`Tiada dalam pangkalan data kami. Ini tidak semestinya salah: semak maksud dan ejaan Arabnya dengan guru agama.${sg.length?` Mungkin maksud anda: ${sg.join(", ")}.`:""}`])}
  }
  const full=words.join(" ");
  const sum=bad?`<p class="nbck bad">⛔ ${bad} bahagian perlu ditukar.</p>`:warn?`<p class="nbck warn">⚠️ Tiada larangan jelas, tetapi ${warn} perkara perlu disemak.</p>`:`<p class="nbck ok">✅ Semua bahagian nama dikenal pasti dan maksudnya baik.</p>`;
  const icon={ok:"✅",warn:"⚠️",bad:"⛔",unk:"❓"};
  return sum+`<ul class="nbr">${items.map(([c,w,m,a])=>`<li class="${c}"><strong>${icon[c]} ${esc(w)}</strong>${a?` <span lang="ar" dir="rtl" class="nbta">${esc(a)}</span>`:""}<span>${esc(m)}</span></li>`).join("")}</ul>`+
    (father.length?`<p class="note">Nama bapa (${esc(father.join(" "))}) tidak disemak. ${full.length} aksara termasuk ${esc(words[bi])}.</p>`:`<p class="note">${full.length} aksara.</p>`)+
    `<div class="act"><button class="btn2" type="button" data-save="${esc(child.join(" "))}" aria-pressed="${saved.includes(child.join(" "))}">♡ Simpan nama ini</button></div>`;
}
$("#nbkf").addEventListener("submit",e=>{e.preventDefault();const v=$("#nbkq").value;ready.then(()=>{if(D)$("#nbkr").innerHTML=check(v)})});

/* ---------- start ---------- */
paintSaved();
const route=()=>{if(/^#senarai=/.test(location.hash))sharedList();else if(/^#j=/.test(location.hash))fromHash()};
ready.then(d=>{if(!d)return;paintSaved();route();addEventListener("hashchange",route)});
})();
