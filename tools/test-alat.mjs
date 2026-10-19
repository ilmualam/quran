/* Browser tests for the tool pages: JS output must equal the build-time HTML (tools/plans.py), plus tasbih, search and reader links. */
import { createRequire } from 'module';
const require = createRequire(process.env.PLAYWRIGHT_PATH||'/opt/node-tools/node_modules/');
const TOOLS=new URL('.',import.meta.url).pathname;
const { chromium } = require('playwright');
// usage: python3 -m http.server 8765 &  then  node tools/test-alat.mjs [base-url]
const B=process.argv[2]||'http://localhost:8765/';
const browser=await chromium.launch();
const ctx=await browser.newContext({viewport:{width:390,height:844}});
await ctx.route('https://www.e-solat.gov.my/**',r=>r.fulfill({status:200,contentType:'application/json',body:'{}'}));
const ok=(c,m)=>console.log((c?'PASS ':'FAIL ')+m);
async function open(p){const pg=await ctx.newPage();const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});await pg.clock.setFixedTime(new Date('2026-10-18T10:00:00'));await pg.goto(B+p,{waitUntil:'networkidle'});pg.errs=errs;return pg}
// raw pre-rendered html
const rawCtx=await browser.newContext({javaScriptEnabled:false});
const raw=async(p,sel)=>{const pg=await rawCtx.newPage();await pg.goto(B+p);const h=await pg.$eval(sel,e=>e.innerHTML);await pg.close();return h};

// khatam
let pg=await open('jadual-khatam-al-quran/');
ok(await raw('jadual-khatam-al-quran/','#kt tbody')===await pg.$eval('#kt tbody',e=>e.innerHTML),'khatam tbody JS == build');
ok(await raw('jadual-khatam-al-quran/','#ksum')===await pg.$eval('#ksum',e=>e.innerHTML),'khatam summary JS == build');
// compare JS vs python for other combos
const {execSync}=await import('child_process');
for(const [D,r] of [[29,0],[7,0],[15,0],[365,0],[30,100],[3,600],[1,0]]){
  await pg.fill('#kd',String(D));await pg.fill('#kr',String(r));await pg.dispatchEvent('#kf','input');
  const js=await pg.$eval('#ksum',e=>e.innerHTML)+await pg.$eval('#kt tbody',e=>e.innerHTML);
  const py=execSync(`cd ${TOOLS} && python3 -c "import plans as P,datetime as d;s,t=P.khatam_html(${D},${r},d.date(2026,10,18));print(s+t,end='')"`).toString();
  ok(js===py,`khatam D=${D} r=${r} JS==py (${(await pg.$$('#kt tbody tr')).length} rows)`);
}
ok(pg.url().includes('#hari=1'),'hash updated '+pg.url());
await pg.fill('#kd','30');await pg.fill('#kr','0');await pg.dispatchEvent('#kf','input');
await pg.check('#kt input[data-d="1"]');await pg.check('#kt input[data-d="2"]');
ok((await pg.textContent('#kprog')).includes('2 daripada 30'),'progress text');
await pg.reload({waitUntil:'networkidle'});
ok(await pg.isChecked('#kt input[data-d="2"]'),'progress persisted');
const [dl]=await Promise.all([pg.waitForEvent('download'),pg.click('[data-act=ics]')]);
const fs=await import('fs');globalThis.fs=fs;const p2=await dl.path();const ics=fs.readFileSync(p2,'utf8');
ok(ics.startsWith('BEGIN:VCALENDAR')&&(ics.match(/BEGIN:VEVENT/g)||[]).length===30,'ics 30 events '+dl.suggestedFilename());
ok(pg.errs.length===0,'khatam no errors '+pg.errs);

// hafazan
pg=await open('jadual-hafazan-al-quran/');
ok(await raw('jadual-hafazan-al-quran/','#ht tbody')===await pg.$eval('#ht tbody',e=>e.innerHTML),'hafazan tbody JS == build');
ok(await raw('jadual-hafazan-al-quran/','#hsum')===await pg.$eval('#hsum',e=>e.innerHTML),'hafazan summary JS == build');
for(const [k,o,u,n,w] of [['all','mushaf','page',1,'6j'],['s36','mushaf','ayat',3,'5s'],['j29','pendek','ayat',7,'5j'],['j1','mushaf','page',2,'7'],['all','pendek','ayat',2,'7']]){
  await pg.selectOption('#htg',k);await pg.selectOption('#hu',u);if(u==='ayat')await pg.selectOption('#ho',o);await pg.fill('#hn',String(n));await pg.selectOption('#hw',w);
  const js=await pg.$eval('#hsum',e=>e.innerHTML)+await pg.$eval('#ht tbody',e=>e.innerHTML);
  const py=execSync(`cd ${TOOLS} && python3 -c "import plans as P,datetime as d;s,t=P.hafazan_html('${k}','${o}','${u}',${n},'${w}',d.date(2026,10,18));print(s+t,end='')"`).toString();
  ok(js===py,`hafazan ${k} ${o} ${u} ${n} ${w} JS==py`);
}
ok(pg.errs.length===0,'hafazan no errors '+pg.errs);

// tasbih
pg=await open('tasbih-digital/');
for(let i=0;i<33;i++)await pg.click('#tbtn');
ok((await pg.textContent('#trm'))==='Alhamdulillah'&&(await pg.textContent('#tcnt'))==='0','tasbih advances after 33');
await pg.click('#tbtn');await pg.click('#tundo');
ok((await pg.textContent('#tday'))==='33','tasbih day total after undo');
await pg.click('#tpre button[data-p=bebas]');await pg.fill('#tn','5');for(let i=0;i<5;i++)await pg.click('#tbtn');
ok((await pg.textContent('#tcnt'))==='5'&&(await pg.textContent('#ttgt'))==='/ 5','tasbih custom target');
await pg.reload({waitUntil:'networkidle'});
ok((await pg.textContent('#tcnt'))==='5','tasbih persisted');
ok(pg.errs.length===0,'tasbih no errors '+pg.errs);

// cari
pg=await open('cari-ayat-al-quran/');
await pg.fill('#cq','sabar');await pg.waitForFunction(()=>document.querySelectorAll('#cres li').length>0);
ok(/Ditemui \d+ ayat/.test(await pg.textContent('#cstat')),'search sabar: '+await pg.textContent('#cstat'));
await pg.fill('#cq','2:255');await pg.waitForFunction(()=>document.querySelector('#cstat').textContent.includes('255'));
ok((await pg.textContent('#cres')).includes('Al-Baqarah 2:255'),'search ref 2:255');
await pg.fill('#cq','ibu bapa');await pg.waitForTimeout(500);
ok(/Ditemui/.test(await pg.textContent('#cstat')),'search multi-word: '+await pg.textContent('#cstat'));
await pg.fill('#cq','xyzqq');await pg.waitForTimeout(500);ok((await pg.textContent('#cstat')).startsWith('Tiada'),'no result msg');
ok(pg.errs.length===0,'cari no errors '+pg.errs);

// waktu solat: build == JS for KL today, and JS == Python for other cities/dates
pg=await open('waktu-solat/');
ok(await raw('waktu-solat/','#stimes')===await pg.$eval('#stimes',e=>{const c=e.cloneNode(true);c.querySelectorAll('.nx').forEach(x=>x.removeAttribute('class'));return c.innerHTML}),'solat times JS == build');
ok(await raw('waktu-solat/','#smon tbody')===await pg.$eval('#smon tbody',e=>e.innerHTML),'solat month JS == build');
ok(/lagi|esok/.test(await pg.textContent('#snext')),'solat countdown: '+await pg.textContent('#snext'));
for(const slug of ['kota-kinabalu','kangar','johor-bahru','kuching','gua-musang']){
  await pg.selectOption('#sc',slug);await pg.waitForFunction(s=>document.querySelector('#sdate').textContent.length>0&&location.hash.includes(s),slug);
  await pg.waitForTimeout(150);
  const official=!(await pg.textContent('#ssrc')).includes('kiraan anggaran');
  if(official){ok(true,`solat ${slug}: official data shown`);continue}
  const js=await pg.$$eval('#smon tbody tr',rs=>rs.map(r=>[...r.cells].slice(1).map(c=>c.textContent).join(' ')));
  const py=execSync(`cd ${TOOLS} && python3 -c "import solat as S;c=[c for c in S.CITIES if c[0]=='${slug}'][0];print('\\n'.join(' '.join(S.hm(x) for x in S.solat_day(2026,10,d,c[3],c[4])) for d in range(1,32)))"`).toString().trim().split('\n');
  ok(JSON.stringify(js)===JSON.stringify(py),`solat ${slug} October JS == Python`);
}
ok(pg.errs.length===0,'solat no errors '+pg.errs);

// live e-solat layer (synced index hidden): a mocked month must replace the calculation and be labelled official
{
  const c2=await browser.newContext({viewport:{width:390,height:844}});
  const mock=execSync(`cd ${TOOLS} && python3 -c "
import json,solat as S
M=['Jan','Feb','Mac','Apr','Mei','Jun','Jul','Ogo','Sep','Okt','Nov','Dis']
f=lambda x:'%02d:%02d:00'%(x//60,x%60)
out=[]
for d in range(1,32):
  t=[x+3 for x in S.solat_day(2026,10,d,6.441,100.198)]
  out.append(dict(hijri='1448-05-%02d'%d,date='%02d-Okt-2026'%d,imsak=f(t[0]),fajr=f(t[1]),syuruk=f(t[2]),dhuhr=f(t[3]),asr=f(t[4]),maghrib=f(t[5]),isha=f(t[6])))
print(json.dumps(dict(prayerTime=out,status='OK!')))"`).toString();
  await c2.route('**/assets/data/solat/index.json',r=>r.fulfill({status:200,contentType:'application/json',body:'[]'}));  // no synced file -> live layer
  await c2.route('https://www.e-solat.gov.my/**',r=>r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:mock}));
  const p2=await c2.newPage();const errs=[];p2.on('pageerror',e=>errs.push(e.message));
  await p2.clock.setFixedTime(new Date('2026-10-18T10:00:00'));await p2.goto(B+'waktu-solat/#bandar=kangar',{waitUntil:'networkidle'});
  await p2.waitForFunction(()=>document.querySelector('#ssrc').textContent.includes('e-solat'));
  const want=JSON.parse(mock).prayerTime[17];
  ok((await p2.textContent('#stimes')).includes(want.fajr.slice(0,5))&&(await p2.textContent('#shij')).includes('18 Jamadilawal 1448'),'live e-solat month shown + hijri from JAKIM');
  ok(errs.length===0,'live e-solat no errors '+errs);
  await c2.close();
}

// state pages: build == JS for today, month and all-zones tables; clicking a zone switches the timetable
for(const st of ['sabah','perlis']){
  pg=await open(`waktu-solat/${st}/`);
  const strip=e=>{const c=e.cloneNode(true);c.querySelectorAll('.nx').forEach(x=>x.removeAttribute('class'));return c.innerHTML};
  ok(await raw(`waktu-solat/${st}/`,'#stimes')===await pg.$eval('#stimes',strip),`state ${st}: times JS == build`);
  ok(await raw(`waktu-solat/${st}/`,'#smon tbody')===await pg.$eval('#smon tbody',e=>e.innerHTML),`state ${st}: month JS == build`);
  ok(await raw(`waktu-solat/${st}/`,'#szt tbody')===await pg.$eval('#szt tbody',e=>e.innerHTML),`state ${st}: all-zones JS == build`);
  ok(pg.errs.length===0,`state ${st}: no errors `+pg.errs);
}
await pg.goto(B+'waktu-solat/sabah/',{waitUntil:'networkidle'});
const z2=await pg.$$eval('#szt a[data-zone]',a=>a.map(x=>x.dataset.zone)[1]);
await pg.click(`#szt a[data-zone="${z2}"]`);await pg.waitForTimeout(200);
ok((await pg.textContent('#sdate')).includes(z2)&&pg.url().includes('bandar='+z2),'state zone click switches timetable to '+z2);

// doa
pg=await open('doa-harian/');
await pg.fill('#dq','makan');await pg.waitForTimeout(100);
ok(/Menunjukkan [1-9]/.test(await pg.textContent('#dcnt')),'doa search: '+await pg.textContent('#dcnt'));
await pg.fill('#dq','');await pg.click('#dcat button[data-c=keluarga]');
ok(await pg.isVisible('#q17-24')&&!(await pg.isVisible('#bangun-tidur')),'doa category filter');
ok(await pg.$eval('#q2-201',e=>e.querySelector('.dar').textContent.split(/\s+/)[3]===e.querySelector('mark').textContent.split(/\s+/)[0]),'doa highlight starts at Rabbana (word 4 of 2:201)');
ok(pg.errs.length===0,'doa no errors '+pg.errs);

// zikir
pg=await open('zikir-pagi-petang/');
for(let i=0;i<3;i++)await pg.click('#bismillah .zc');
ok((await pg.textContent('#bismillah .zc')).includes('Selesai'),'zikir counter completes at 3');
await pg.reload({waitUntil:'networkidle'});
ok((await pg.textContent('#bismillah .zc')).includes('Selesai')&&(await pg.textContent('#pagi-petang .zprog')).startsWith('1 /'),'zikir persisted + progress');
ok(pg.errs.length===0,'zikir no errors '+pg.errs);

// tajwid
pg=await open('belajar-tajwid/');
await pg.click('#tjgrid button[data-h="ب"]');ok((await pg.textContent('#tjout')).includes('Iqlab'),'tajwid nun+ba = iqlab');
await pg.click('#tjgrid button[data-h="ع"]');ok((await pg.textContent('#tjout')).includes('Izhar Halqi'),'tajwid nun+ain = izhar');
await pg.click('#tjgrid button[data-h="ر"]');ok((await pg.textContent('#tjout')).includes('Bila Ghunnah'),'tajwid nun+ra = idgham bila ghunnah');
await pg.click('#tjgrid button[data-h="ك"]');ok((await pg.textContent('#tjout')).includes('Ikhfa'),'tajwid nun+kaf = ikhfa');
await pg.click('#tjmode button[data-m=mim]');await pg.click('#tjgrid button[data-h="م"]');ok((await pg.textContent('#tjout')).includes('Mithlain'),'tajwid mim+mim = idgham mithlain');
await pg.click('#qz [data-qstart]');
for(let i=0;i<10;i++){await pg.click('#qz button[data-a] >> nth=0');await pg.click('#qz [data-next]')}
ok(/Markah anda: \d+ \/ 10/.test(await pg.textContent('#qz')),'tajwid quiz completes: '+(await pg.textContent('.qzs')));
ok(pg.errs.length===0,'tajwid no errors '+pg.errs);

// waktu berbuka puasa: build == JS, JS == Python for another zone, tracker, .ics, official upgrade
pg=await open('waktu-berbuka-puasa/');
ok(await raw('waktu-berbuka-puasa/','#rmt tbody')===await pg.$eval('#rmt tbody',e=>e.innerHTML),'ramadan table JS == build');
ok(await raw('waktu-berbuka-puasa/','#rtd')===await pg.$eval('#rtd',e=>e.innerHTML),'ramadan today strip JS == build');
ok(await raw('waktu-berbuka-puasa/','#rph')===await pg.$eval('#rph',e=>e.innerHTML),'ramadan phase JS == build');
ok((await pg.$$('#rmt tbody tr')).length>=29,'ramadan rows '+(await pg.$$('#rmt tbody tr')).length);
ok(/Maghrib hari ini|Berbuka|Imsak/.test(await pg.textContent('#rcd')),'ramadan countdown: '+await pg.textContent('#rcd'));
await pg.selectOption('#rz','SBH07');await pg.waitForFunction(()=>location.hash.includes('SBH07'));await pg.waitForTimeout(150);
{
  const js=await pg.$eval('#rmt tbody',e=>e.innerHTML);
  const py=execSync(`cd ${TOOLS} && python3 -c "import ramadan as R,pages4 as F,datetime as d;t=d.date(2026,10,18);s=R.season(t);rows,_=R.timetable('SBH07',s);print(''.join(F.r_row(k,x,v,s,t) for k,x,v in rows),end='')"`).toString();
  ok(js===py,'ramadan SBH07 JS == Python');
}
await pg.check('#rmt input[data-r="1"]');await pg.check('#rmt input[data-r="2"]');
ok((await pg.textContent('#rprog')).includes('2 daripada'),'ramadan tracker text: '+await pg.textContent('#rprog'));
await pg.reload({waitUntil:'networkidle'});
ok(await pg.isChecked('#rmt input[data-r="2"]')&&(await pg.inputValue('#rz'))==='SBH07','ramadan tracker + zone persisted');
for(const [k,n] of [['b',30],['bi',60]]){
  const [dl]=await Promise.all([pg.waitForEvent('download'),pg.click(`#ract button[data-ics="${k}"]`)]);
  const ics=fs.readFileSync(await dl.path(),'utf8'),rows=(await pg.$$('#rmt tbody tr')).length;
  const mg=(await pg.textContent('#rmt tbody tr:first-child td:nth-child(7)')).split(':').map(Number),hh=String(mg[0]-8).padStart(2,'0')+String(mg[1]).padStart(2,'0');
  ok((ics.match(/BEGIN:VEVENT/g)||[]).length===rows*n/30&&ics.includes('VALARM')&&new RegExp(`DTSTART:\\d{8}T${hh}00Z`).test(ics),`ramadan ics ${k}: ${rows*n/30} events, berbuka in UTC `+dl.suggestedFilename());
}
ok(pg.errs.length===0,'ramadan no errors '+pg.errs);
// official JAKIM file for the Ramadan year replaces the calculation and is labelled
{
  const c2=await browser.newContext({viewport:{width:390,height:844}});
  const data=execSync(`cd ${TOOLS} && python3 -c "
import json,datetime as d,solat as S
y=2027;n=(d.date(y,12,31)-d.date(y,1,1)).days+1
t=[[x+3 for x in S.solat_day(y,(d.date(y,1,1)+d.timedelta(i)).month,(d.date(y,1,1)+d.timedelta(i)).day,3.139,101.687)] for i in range(n)]
print(json.dumps(dict(z='WLY01',y=y,src='JAKIM e-solat',t=t,h=['']*n)))"`).toString();
  await c2.route('**/assets/data/solat/index.json',r=>r.fulfill({status:200,contentType:'application/json',body:'["WLY01-2027"]'}));
  await c2.route('**/assets/data/solat/WLY01-2027.json',r=>r.fulfill({status:200,contentType:'application/json',body:data}));
  const p2=await c2.newPage();await p2.clock.setFixedTime(new Date('2026-10-18T10:00:00'));
  await p2.goto(B+'waktu-berbuka-puasa/#zon=WLY01',{waitUntil:'networkidle'});
  await p2.waitForFunction(()=>document.querySelector('#rsrc').textContent.includes('jadual rasmi'));
  const want=JSON.parse(data).t[(new Date(2027,1,8)-new Date(2027,0,1))/864e5][5];
  ok((await p2.textContent('#rmt tbody tr:first-child td:nth-child(7)'))===String(Math.floor(want/60)).padStart(2,'0')+':'+String(want%60).padStart(2,'0'),'ramadan official file replaces calculation');
  await c2.close();
}
for(const st of ['perlis','sabah']){
  pg=await open(`waktu-berbuka-puasa/${st}/`);
  ok(await raw(`waktu-berbuka-puasa/${st}/`,'#rmt tbody')===await pg.$eval('#rmt tbody',e=>e.innerHTML),`ramadan ${st}: table JS == build`);
  ok(pg.errs.length===0,`ramadan ${st}: no errors `+pg.errs);
}
{const z2=await pg.$$eval('#szt a[data-zone]',a=>a.map(x=>x.dataset.zone)[2]);await pg.click(`#szt a[data-zone="${z2}"]`);await pg.waitForTimeout(150);
 ok((await pg.textContent('#rcap')).includes(z2)&&pg.url().includes('zon='+z2),'ramadan state zone click switches to '+z2);}

// belajar solat: step player and qada calculator
pg=await open('belajar-solat/');
ok(await raw('belajar-solat/','#spc')===await pg.$eval('#spc',e=>e.innerHTML),'solat step card JS == build');
ok(await raw('belajar-solat/','#spl')===await pg.$eval('#spl',e=>e.innerHTML),'solat step list JS == build');
ok(await raw('belajar-solat/','#qsum')===await pg.$eval('#qsum',e=>e.innerHTML),'qada summary JS == build');
for(const [w,r] of [['subuh',2],['maghrib',3],['isyak',4]]){
  await pg.click(`#spw button[data-w=${w}]`);
  const n=+execSync(`cd ${TOOLS} && python3 -c "import ibadah2 as I;print(len(I.solat_steps(${r},'${w}'=='subuh')))"`).toString();
  ok((await pg.$$('#spl li')).length===n&&(await pg.textContent('#spc .spn')).includes(`Langkah 1 / ${n}`),`solat ${w}: ${n} steps`);
}
for(let i=0;i<5;i++)await pg.click('#spnext');
ok((await pg.textContent('#spc .spn')).includes('Langkah 6 /')&&pg.url().includes('langkah=6'),'solat next x5 -> step 6 '+pg.url());
const qunut=await pg.$$eval('#spl button',b=>b.map(x=>x.textContent));
await pg.click('#spw button[data-w=subuh]');ok((await pg.$$eval('#spl button',b=>b.some(x=>x.textContent.startsWith('Doa Qunut')))),'subuh has qunut');
ok(!qunut.some(x=>x.startsWith('Doa Qunut')),'isyak has no qunut');
await pg.click('#sprm');ok(await pg.$eval('#spc',e=>e.classList.contains('nr')),'rumi toggle hides rumi');
await pg.fill('#qy','2');await pg.fill('#qm','6');await pg.selectOption('#qs','2');
ok((await pg.textContent('#qsum')).includes('4,550 solat fardu')&&(await pg.textContent('#qsum')).includes('455 hari'),'qada 2y6m, 2 sets: '+await pg.textContent('#qsum'));
ok(pg.errs.length===0,'solat no errors '+pg.errs);

// belajar iqra'
pg=await open('belajar-iqra/');
ok(await raw('belajar-iqra/','#iqg')===await pg.$eval('#iqg',e=>e.innerHTML),'iqra level 1 grid JS == build');
for(const L of [2,3,4,5]){await pg.click(`#iql button[data-l="${L}"]`);await pg.click('#iqgen');
  const ok2=await pg.$$eval('#iqg .iqi',b=>b.length===12&&b.every(x=>/[ء-ي]/.test(x.querySelector('.iqa').textContent)&&/^[a-z'ḥ-]+$/.test(x.querySelector('.iqr').textContent)));
  ok(ok2,`iqra level ${L}: 12 items with arabic + rumi (${await pg.$eval('#iqg .iqi .iqr',e=>e.textContent)})`)}
await pg.click('#iql button[data-l="6"]');ok((await pg.$$('#iqg .iqi.w')).length===4,'iqra 6: 4 ayat');
await pg.click('#iqdone');await pg.click('#iqrm');ok(await pg.$eval('#iqg',e=>e.classList.contains('show')),'iqra rumi toggle');
await pg.reload({waitUntil:'networkidle'});ok((await pg.textContent('#iqprog')).includes('Iqra\' 6')&&(await pg.getAttribute('#iql button[data-l="6"]','aria-pressed'))==='true','iqra progress + level persisted');
ok(pg.errs.length===0,'iqra no errors '+pg.errs);

// belajar mengaji
pg=await open('belajar-mengaji/');
await pg.click('#hjg button[data-i="1"]');ok((await pg.textContent('#hjd')).includes('Ba')&&(await pg.textContent('#hjd')).includes('Asy-Syafatan'),'mengaji ba detail');
await pg.click('#hjg button[data-i="9"]');ok((await pg.textContent('#hjd')).includes('tidak bersambung'),'mengaji ra non-connector note');
for(const m of ['nama','huruf','bentuk','makhraj']){
  await pg.click(`#hqm button[data-m=${m}]`);await pg.click('#hqz [data-hq]');
  for(let i=0;i<10;i++){await pg.click('#hqz button[data-k] >> nth=0');await pg.click('#hqz [data-next]')}
  ok(/Markah anda: \d+ \/ 10/.test(await pg.textContent('#hqz')),`mengaji quiz ${m} completes`);
}
ok(await raw('belajar-mengaji/','#msp')===await pg.$eval('#msp',e=>e.innerHTML),'mengaji checklist JS == build');
await pg.check('#msl input[data-m=huruf]');await pg.reload({waitUntil:'networkidle'});
ok(await pg.isChecked('#msl input[data-m=huruf]')&&(await pg.textContent('#msp')).startsWith('1 /'),'mengaji checklist persisted');
ok(pg.errs.length===0,'mengaji no errors '+pg.errs);

// cari masjid: zone page times JS == build, JSON-LD (Place, Mosque list, BreadcrumbList), nearest search with mocked GPS + Overpass
{
  const fs2=await import('fs');
  const slug=fs2.readdirSync(TOOLS+'../cari-masjid/').find(f=>f.startsWith('sgr01-'));
  pg=await open(`cari-masjid/${slug}/`);
  const strip=e=>{const c=e.cloneNode(true);c.querySelectorAll('.nx').forEach(x=>x.removeAttribute('class'));return c.innerHTML};
  ok(await raw(`cari-masjid/${slug}/`,'#mtimes')===await pg.$eval('#mtimes',strip),'masjid zone: times JS == build');
  ok(/lagi|esok/.test(await pg.textContent('#mnext')),'masjid zone countdown: '+await pg.textContent('#mnext'));
  const g=JSON.parse(await pg.$eval('script[type="application/ld+json"]',s=>s.textContent))['@graph'],types=g.map(n=>n['@type']);
  ok(['Place','BreadcrumbList','FAQPage','CollectionPage'].every(t=>types.includes(t)),'masjid zone JSON-LD: '+types.join(','));
  ok(g.find(n=>n['@type']==='BreadcrumbList').itemListElement.length===3,'masjid zone breadcrumb 3 levels');
  if(fs2.existsSync(TOOLS+'../assets/data/masjid/SGR01.json')){
    const il=g.find(n=>n['@type']==='ItemList');
    ok(il&&il.itemListElement.length>0&&il.itemListElement.every(x=>['Mosque','PlaceOfWorship'].includes(x.item['@type'])&&x.item.geo.latitude),'masjid zone ItemList of Mosque/PlaceOfWorship ('+(il?il.itemListElement.length:0)+')');
    ok((await pg.$$('#senarai .mq')).length>0&&(await pg.textContent('#senarai .osm')).includes('OpenStreetMap'),'masjid zone list + OSM credit');
  }
  ok(await pg.$eval(`#kira a[href^="/waktu-solat/selangor/"]`,a=>a.getAttribute('href'))==='/waktu-solat/selangor/#bandar=SGR01','masjid zone links to prayer-times tool');
  ok(pg.errs.length===0,'masjid zone no errors '+pg.errs);
  const c3=await browser.newContext({viewport:{width:390,height:844},geolocation:{latitude:3.0738,longitude:101.5183},permissions:['geolocation']});
  const el=(id,n,la,lo,t={})=>({type:'node',id,lat:la,lon:lo,tags:{amenity:'place_of_worship',religion:'muslim',...(n?{name:n}:{}),...t}});
  const body=JSON.stringify({elements:[el(1,'Surau Al-Ikhlas',3.080,101.520),el(2,'Masjid Sultan Salahuddin Abdul Aziz Shah',3.0786,101.5206,{'addr:street':'Persiaran Masjid','addr:city':'Shah Alam'}),
    el(3,'Masjid Sultan Salahuddin Abdul Aziz Shah',3.0787,101.5206),el(4,'',3.074,101.519),{type:'way',id:5,center:{lat:3.090,lon:101.530},tags:{building:'mosque',name:'Masjid Bulatan <Seksyen 7>'}},
    el(6,'Musolla Stesen',3.070,101.515),el(7,'Tempat Solat Pasar',3.060,101.500)]});
  let hits=0;
  await c3.route('https://overpass-api.de/**',r=>{hits++;r.fulfill({status:504,body:'busy'})});  // first endpoint down -> mirror
  await c3.route('https://overpass.kumi.systems/**',r=>r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body}));
  await c3.route('https://www.e-solat.gov.my/**',r=>r.fulfill({status:200,contentType:'application/json',body:'{}'}));
  const p3=await c3.newPage();const errs=[];p3.on('pageerror',e=>errs.push(e.message));
  await p3.goto(B+'cari-masjid/',{waitUntil:'networkidle'});
  await p3.click('#mgeo');await p3.waitForSelector('#mres li');
  const names=await p3.$$eval('#mres .mqn',a=>a.map(x=>x.textContent));
  ok(hits>0&&names.length===5&&names[0]==='Musolla Stesen'&&names[1]==='Masjid Sultan Salahuddin Abdul Aziz Shah','near me: mirror used, deduped, nearest first: '+names.join(' | '));
  ok(await p3.$eval('#mres',e=>!e.querySelector('script,b')&&e.textContent.includes('<Seksyen 7>')),'near me: names escaped');
  ok(JSON.stringify(await p3.$$eval('#mres .mk',a=>a.map(x=>x.className)))===JSON.stringify(['mk s','mk m','mk s','mk m','mk t']),'near me: masjid/surau kinds');
  ok((await p3.textContent('#mstat')).includes('SGR01')&&await p3.$eval('#mstat a[href^="/cari-masjid/sgr01-"]',a=>!!a),'near me: zone detected + linked');
  ok(errs.length===0,'near me no errors '+errs);
  await c3.close();
}

// kalendar hijrah: build == JS for today; JS hijri engine == tools/hijri.py over 1950-2080; converter, age, haul, .ics
{
  pg=await open('kalendar-hijrah/');
  for(const s of ['#hbig','#har','#hmas','#hmag','#hmt','#hgrid','#hev tbody','#hsl','#hgo','#hho'])
    ok(await raw('kalendar-hijrah/',s)===await pg.$eval(s,e=>e.innerHTML),`hijri ${s} JS == build`);
  const ds=[];for(let t=Date.UTC(1950,0,1);t<Date.UTC(2080,0,1);t+=37*864e5)ds.push(new Date(t).toISOString().slice(0,10));
  ds.push('2026-01-01','2027-12-31','2028-01-10','2026-06-15','2026-06-16','2027-02-07','2027-02-08','2027-03-09','2027-03-10','2027-12-31','2028-01-01');
  const js=await pg.evaluate(ds=>ds.map(s=>{const[y,m,d]=s.split('-').map(Number);const p=document.createElement('p');return s}),ds);
  fs.writeFileSync('/tmp/hj-dates.json',JSON.stringify(ds));
  const py=JSON.parse(execSync(`cd ${TOOLS} && python3 -c "import json,datetime as d,hijri as H;print(json.dumps([list(H.g2h(d.date.fromisoformat(s))) for s in json.load(open('/tmp/hj-dates.json'))]))"`).toString());
  await pg.fill('#hg',ds[0]);
  const jsv=[];for(const s of ds){await pg.fill('#hg',s);jsv.push(await pg.textContent('#hgo'))}
  const pyv=ds.map((s,i)=>{const h=py[i];return `${s} = ${h[2]} ${['Muharam','Safar','Rabiulawal','Rabiulakhir','Jamadilawal','Jamadilakhir','Rejab','Syaaban','Ramadan','Syawal','Zulkaedah','Zulhijjah'][h[1]-1]} ${h[0]} H${h[3]?'':' (anggaran)'}`});
  const bad=ds.filter((s,i)=>jsv[i]!==pyv[i]);
  ok(bad.length===0,`hijri g2h JS == Python on ${ds.length} dates `+bad.slice(0,3));
  ok(jsv[ds.indexOf('2027-02-08')].includes('1 Ramadan 1448 H')&&!jsv[ds.indexOf('2027-02-08')].includes('anggaran'),'2027-02-08 = 1 Ramadan 1448 (official)');
  await pg.selectOption('#hhd','1');await pg.selectOption('#hhm','10');await pg.fill('#hhy','1448');
  ok((await pg.textContent('#hho')).includes('Rabu, 10 Mac 2027'),'1 Syawal 1448 -> '+await pg.textContent('#hho'));
  await pg.selectOption('#hhd','30');await pg.selectOption('#hhm','9');
  ok(/hanya ada 29 hari|Mac 2027/.test(await pg.textContent('#hho')),'30 Ramadan handled: '+await pg.textContent('#hho'));
  for(const [y,m] of [[2026,11],[2027,2],[2030,3]]){
    while(true){const t=await pg.textContent('#hmt');const want=['Januari','Februari','Mac','April','Mei','Jun','Julai','Ogos','September','Oktober','November','Disember'][m-1]+' '+y;if(t.startsWith(want))break;await pg.click('#hnext')}
    const pyg=execSync(`cd ${TOOLS} && python3 -c "import hijri as H,datetime as d;print(H.grid_html(${y},${m},d.date(2026,10,18)),end='')"`).toString();
    ok(pyg===await pg.$eval('#hgrid',e=>e.innerHTML),`hijri grid ${y}-${m} JS == Python`);
  }
  ok(await pg.$$eval('#hgrid .hc.ma',a=>a.length)>0,'grid marks sunat days');
  await pg.fill('#hlahir','1990-05-01');ok(/tahun Hijrah/.test(await pg.textContent('#hlo')),'hijri age: '+(await pg.textContent('#hlo')).slice(0,90));
  await pg.fill('#hhaul','2026-01-01');ok(/Haul cukup pada/.test(await pg.textContent('#hho2')),'haul: '+(await pg.textContent('#hho2')).slice(0,90));
  const [dl2]=await Promise.all([pg.waitForEvent('download'),pg.click('#hics')]);
  const ics2=fs.readFileSync(await dl2.path(),'utf8');ok((ics2.match(/BEGIN:VEVENT/g)||[]).length>20&&ics2.includes('Aidilfitri'),'hijri .ics events: '+(ics2.match(/BEGIN:VEVENT/g)||[]).length);
  ok(pg.errs.length===0,'hijri no errors '+pg.errs);
  ok(jsv[ds.indexOf('2026-01-01')].includes('11 Rejab 1447 H')&&!jsv[ds.indexOf('2026-01-01')].includes('anggaran'),'edge month kept official: '+jsv[ds.indexOf('2026-01-01')]);
  // a visitor in New York at 10:00 local = 22:00 in Malaysia: Malaysian day, already past Maghrib
  const c4=await browser.newContext({timezoneId:'America/New_York'});const p4=await c4.newPage();await p4.clock.setFixedTime(new Date('2026-10-18T14:00:00Z'));
  await p4.goto(B+'kalendar-hijrah/',{waitUntil:'networkidle'});
  ok((await p4.textContent('#hmas')).startsWith('Ahad, 18 Oktober 2026')&&(await p4.textContent('#hmag')).startsWith('Sudah masuk malam 8 Jamadilawal'),'hijri uses Malaysian time abroad: '+await p4.textContent('#hmag'));
  await c4.close();
}
// tahlil: personalisation, pronoun switch, shared link, view, counter, majlis mode
{
  pg=await open('tahlil-ringkas/');
  ok(await pg.$$eval('#tls li.tls',a=>a.length)>=25,'tahlil steps: '+await pg.$$eval('#tls li.tls',a=>a.length));
  ok((await pg.getAttribute('#fatihah1 button[data-play]','data-play'))==='1:1 1:2 1:3 1:4 1:5 1:6 1:7','tahlil audio refs');
  await pg.fill('#tln','Ahmad');await pg.fill('#tlb','Ismail');
  ok((await pg.textContent('#tlh')).includes('roh Allahyarham Ahmad bin Ismail: Al-Fatihah'),'hadiah personalised');
  await pg.selectOption('#tlj','p');
  ok((await pg.textContent('#tlda')).includes('لَهَا')&&(await pg.textContent('#tlh')).includes('Allahyarhamah Ahmad binti Ismail'),'pronoun switched to perempuan');
  await pg.selectOption('#tlj','ll');ok((await pg.textContent('#tldr')).includes('lahum'),'pronoun ramai');
  const py=execSync(`cd ${TOOLS} && python3 -c "import tahlil as T;print(T.hadiah('l','Ahmad','Ismail'),end='')"`).toString();
  await pg.selectOption('#tlj','l');ok((await pg.textContent('#tlh'))===py,'hadiah JS == Python');
  await pg.goto(B+'tahlil-ringkas/#nama=Siti&j=p&t=2025-03-01',{waitUntil:'networkidle'});await pg.reload({waitUntil:'networkidle'});
  ok((await pg.textContent('#tlcn'))==='Allahyarhamah Siti'&&/Haul seterusnya/.test(await pg.textContent('#tlhaul')),'shared link loads name + haul: '+await pg.textContent('#tlhaul'));
  await pg.click('#tlv button[data-v=ar]');ok(!(await pg.isVisible('#kursi .dru'))&&await pg.isVisible('#kursi .dar')&&await pg.isVisible('#hadiah .dmn'),'view Arab only');
  await pg.click('#tlv button[data-v=""]');
  for(let i=0;i<7;i++)await pg.click('#irhamna .zc');ok((await pg.textContent('#irhamna .zc')).includes('Selesai'),'irhamna counter 7');
  await pg.click('#tlbig');ok(await pg.evaluate(()=>document.body.classList.contains('tlbig'))&&(await pg.$$eval('#tls li.tls',a=>a.filter(x=>getComputedStyle(x).display!=='none').length))===1,'majlis mode shows one reading');
  await pg.keyboard.press('ArrowRight');ok((await pg.textContent('#tlpos')).startsWith('2 /'),'majlis next');
  await pg.keyboard.press('Escape');ok(!(await pg.evaluate(()=>document.body.classList.contains('tlbig'))),'majlis exit');
  ok(pg.errs.length===0,'tahlil no errors '+pg.errs);
}

// header: hamburger menu (popover), site search, footer subscribe form
pg=await open('belajar-iqra/');
await pg.click('.mnb');ok(await pg.isVisible('#menu a[href="/waktu-berbuka-puasa/"]'),'hamburger opens full menu');
ok(await pg.$eval('#menu a[href="/belajar-iqra/"]',a=>a.getAttribute('aria-current'))==='page','menu marks current page');
await pg.keyboard.press('Escape');ok(!(await pg.isVisible('#menu')),'Esc closes menu');
await pg.keyboard.press('Control+k');await pg.fill('#srq','yasin');await pg.waitForSelector('#srr li');
ok((await pg.textContent('#srr li:first-child strong'))==='Surah Yasin (36)','search: yasin -> Surah Yasin first');
await pg.fill('#srq','berbuka johor');await pg.waitForTimeout(150);
ok((await pg.textContent('#srr li:first-child strong')).includes('Johor'),'search: berbuka johor -> state page');
await pg.keyboard.press('Enter');await pg.waitForURL(/waktu-berbuka-puasa\/johor\//);ok(true,'search Enter navigates to first result');
ok((await pg.getAttribute('footer .fi-form','action')).startsWith('https://api.follow.it/'),'footer subscribe form');
ok(pg.errs.length===0,'header no errors '+pg.errs);

// home reader still works from root + reader link from tool page
pg=await open('jadual-khatam-al-quran/');
await pg.click('#kt tbody tr:nth-child(2) a');await pg.waitForSelector('dialog.rd[open]');
await pg.waitForFunction(()=>document.querySelector('#ayat-142'));
ok(pg.url().endsWith('/#surah-2-ayat-142'),'reader opens from khatam link '+pg.url());
await browser.close();
