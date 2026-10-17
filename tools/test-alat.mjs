/* Browser tests for the tool pages: JS output must equal the build-time HTML (tools/plans.py), plus tasbih, search and reader links. */
import { createRequire } from 'module';
const require = createRequire(process.env.PLAYWRIGHT_PATH||'/opt/node-tools/node_modules/');
const TOOLS=new URL('.',import.meta.url).pathname;
const { chromium } = require('playwright');
// usage: python3 -m http.server 8765 &  then  node tools/test-alat.mjs [base-url]
const B=process.argv[2]||'http://localhost:8765/';
const browser=await chromium.launch();
const ctx=await browser.newContext({viewport:{width:390,height:844}});
const ok=(c,m)=>console.log((c?'PASS ':'FAIL ')+m);
async function open(p){const pg=await ctx.newPage();const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});await pg.clock.setFixedTime(new Date('2026-10-17T10:00:00'));await pg.goto(B+p,{waitUntil:'networkidle'});pg.errs=errs;return pg}
// raw pre-rendered html
const raw=async(p,sel)=>{const pg=await ctx.newPage();await pg.route('**/alat.js',r=>r.abort());await pg.goto(B+p);const h=await pg.$eval(sel,e=>e.innerHTML);await pg.close();return h};

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

// home reader still works from root + reader link from tool page
pg=await open('jadual-khatam-al-quran/');
await pg.click('#kt tbody tr:nth-child(2) a');await pg.waitForSelector('dialog.rd[open]');
await pg.waitForFunction(()=>document.querySelector('#ayat-142'));
ok(pg.url().endsWith('/#surah-2-ayat-142'),'reader opens from khatam link '+pg.url());
await browser.close();
