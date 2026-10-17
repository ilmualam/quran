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
async function open(p){const pg=await ctx.newPage();const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});await pg.clock.setFixedTime(new Date('2026-10-17T10:00:00'));await pg.goto(B+p,{waitUntil:'networkidle'});pg.errs=errs;return pg}
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
  const py=execSync(`cd ${TOOLS} && python3 -c "import plans as P,datetime as d;s,t=P.khatam_html(${D},${r},d.date(2026,10,17));print(s+t,end='')"`).toString();
  ok(js===py,`khatam D=${D} r=${r} JS==py (${(await pg.$$('#kt tbody tr')).length} rows)`);
}
ok(pg.url().includes('#hari=1'),'hash updated '+pg.url());
await pg.fill('#kd','30');await pg.fill('#kr','0');await pg.dispatchEvent('#kf','input');
await pg.check('#kt input[data-d="1"]');await pg.check('#kt input[data-d="2"]');
ok((await pg.textContent('#kprog')).includes('2 daripada 30'),'progress text');
await pg.reload({waitUntil:'networkidle'});
ok(await pg.isChecked('#kt input[data-d="2"]'),'progress persisted');
const [dl]=await Promise.all([pg.waitForEvent('download'),pg.click('[data-act=ics]')]);
const fs=await import('fs');const p2=await dl.path();const ics=fs.readFileSync(p2,'utf8');
ok(ics.startsWith('BEGIN:VCALENDAR')&&(ics.match(/BEGIN:VEVENT/g)||[]).length===30,'ics 30 events '+dl.suggestedFilename());
ok(pg.errs.length===0,'khatam no errors '+pg.errs);

// hafazan
pg=await open('jadual-hafazan-al-quran/');
ok(await raw('jadual-hafazan-al-quran/','#ht tbody')===await pg.$eval('#ht tbody',e=>e.innerHTML),'hafazan tbody JS == build');
ok(await raw('jadual-hafazan-al-quran/','#hsum')===await pg.$eval('#hsum',e=>e.innerHTML),'hafazan summary JS == build');
for(const [k,o,u,n,w] of [['all','mushaf','page',1,'6j'],['s36','mushaf','ayat',3,'5s'],['j29','pendek','ayat',7,'5j'],['j1','mushaf','page',2,'7'],['all','pendek','ayat',2,'7']]){
  await pg.selectOption('#htg',k);await pg.selectOption('#hu',u);if(u==='ayat')await pg.selectOption('#ho',o);await pg.fill('#hn',String(n));await pg.selectOption('#hw',w);
  const js=await pg.$eval('#hsum',e=>e.innerHTML)+await pg.$eval('#ht tbody',e=>e.innerHTML);
  const py=execSync(`cd ${TOOLS} && python3 -c "import plans as P,datetime as d;s,t=P.hafazan_html('${k}','${o}','${u}',${n},'${w}',d.date(2026,10,17));print(s+t,end='')"`).toString();
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
  await p2.clock.setFixedTime(new Date('2026-10-17T10:00:00'));await p2.goto(B+'waktu-solat/#bandar=kangar',{waitUntil:'networkidle'});
  await p2.waitForFunction(()=>document.querySelector('#ssrc').textContent.includes('e-solat'));
  const want=JSON.parse(mock).prayerTime[16];
  ok((await p2.textContent('#stimes')).includes(want.fajr.slice(0,5))&&(await p2.textContent('#shij')).includes('17 Jamadilawal 1448'),'live e-solat month shown + hijri from JAKIM');
  ok(errs.length===0,'live e-solat no errors '+errs);
  await c2.close();
}

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

// home reader still works from root + reader link from tool page
pg=await open('jadual-khatam-al-quran/');
await pg.click('#kt tbody tr:nth-child(2) a');await pg.waitForSelector('dialog.rd[open]');
await pg.waitForFunction(()=>document.querySelector('#ayat-142'));
ok(pg.url().endsWith('/#surah-2-ayat-142'),'reader opens from khatam link '+pg.url());
await browser.close();
