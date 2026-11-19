"""Ramadan 1448H rebuild of the 14 www.ilmualam.com state berbuka posts (/2022/03/waktu-berbuka-puasa-<state>.html, URLs kept).
Each post carries a pre-rendered 30-day table for its first zone (official JAKIM timetable when synced, else the calibrated calculation
from tools/solat.py) and an inline widget that redraws the table for any zone of the state, with a live countdown to berbuka or imsak.
The widget reads assets/data/solat/<ZONE>-<YEAR>.json from quran.ilmualam.com, then GitHub raw, and otherwise calculates in the browser
(solatDay below mirrors assets/js/alat.js and tools/solat.py). The Quran-site state pages point their canonical to these posts.
Run from tools/blog: PYTHONPATH=.. python3 berbuka.py"""
import datetime as dt, json, os
import solat as SL
import ramadan as R
from gen import write, e, table, card as dcard, Q, IMG
from cards import card as img
from batch3 import ul, ref, base

HERE = os.path.dirname(os.path.abspath(__file__))
POSTS_META = json.load(open(f"{HERE}/berbuka-posts.json"))
AREA = {z["jakimCode"]: z["daerah"] for z in json.load(open(f"{R.REPO}/assets/data/solat/zones.json"))}
MOD, MODMS = "2026-11-20", "20 November 2026"
HARI = ["Isnin", "Selasa", "Rabu", "Khamis", "Jumaat", "Sabtu", "Ahad"]
BLN = ["Januari", "Februari", "Mac", "April", "Mei", "Jun", "Julai", "Ogos", "September", "Oktober", "November", "Disember"]
DOA_BERBUKA = "https://www.ilmualam.com/2025/12/doa-berbuka-niat-puasa.html"
NIAT = "https://www.ilmualam.com/2025/12/niat-puasa-ramadan.html"
BATAL = "https://www.ilmualam.com/2020/04/perkara-yang-membatalkan-puasa-ramadhan.html"
QADA = "https://www.ilmualam.com/2025/11/cara-ganti-puasa-qada.html"
AMALAN = "https://www.ilmualam.com/2025/12/ramadan-kelebihan-amalan.html"

# post slug -> (state name, Quran-site state slug used in tools/solat.py ZONES, capital/major town for the FAQ)
STATES = {
    "johor": ("Johor", "johor", "Johor Bahru"), "kedah": ("Kedah", "kedah", "Alor Setar"), "kelantan": ("Kelantan", "kelantan", "Kota Bharu"),
    "kl-putrajaya": ("Kuala Lumpur & Putrajaya", "kuala-lumpur", "Kuala Lumpur"), "melaka": ("Melaka", "melaka", "Bandar Melaka"),
    "negeri-sembilan": ("Negeri Sembilan", "negeri-sembilan", "Seremban"), "pahang": ("Pahang", "pahang", "Kuantan"),
    "penang": ("Pulau Pinang", "pulau-pinang", "George Town"), "perak": ("Perak", "perak", "Ipoh"), "perlis": ("Perlis", "perlis", "Kangar"),
    "sabah": ("Sabah", "sabah", "Kota Kinabalu"), "sarawak": ("Sarawak", "sarawak", "Kuching"), "selangor": ("Selangor", "selangor", "Shah Alam"),
    "terengganu": ("Terengganu", "terengganu", "Kuala Terengganu")}
TITLE_NAME = {"kl-putrajaya": "KL & Putrajaya", "negeri-sembilan": "Negeri Sembilan", "penang": "Pulau Pinang"}

SEASON = R.season(dt.date(2027, 1, 1))  # Ramadan 1448H: official JAKIM Hijri column when synced
START, NDAYS, OFFICIAL = SEASON["start"], SEASON["n"], SEASON["official"]


def hm(m):
    return f"{m // 60:02d}:{m % 60:02d}"


def dms(d):
    return f"{HARI[d.weekday()]}, {d.day} {BLN[d.month - 1]} {d.year}"


def zones_of(qslug, town):
    zs = [z for z in SL.ZONES if z[1] == qslug and (qslug != "kuala-lumpur" or z[0] == "WLY01")]
    home = next((c[5] for c in SL.CITIES if c[1].startswith(town.split()[0]) and c[2].lower().startswith(zs[0][1][:4])), None) \
        or next((c[5] for c in SL.CITIES if c[1] == town), None)
    return sorted(zs, key=lambda z: (z[0] != home, z[0]))  # the capital's zone first: it is the default and the pre-rendered table


def rows(zone):
    out, official_all = [], True
    for i in range(NDAYS):
        d = START + dt.timedelta(i)
        t, off = R.day_times(zone, d)
        official_all &= off
        out.append([f"{i + 1}", f"{d.day} {BLN[d.month - 1][:3]}", HARI[d.weekday()][:3], f"<strong>{hm(t[0])}</strong>", hm(t[1]), f"<strong>{hm(t[5])}</strong>", hm(t[6])])
    return out, official_all


WIDGET_JS = r"""
var D=JSON.parse(document.getElementById('{P}-bz-data').textContent),sel=document.getElementById('{P}-bz'),tb=document.getElementById('{P}-bz-tb'),
cd=document.getElementById('{P}-bz-cd'),src=document.getElementById('{P}-bz-src'),cache={},cur=null;
var pad=function(n){return String(n).padStart(2,'0')},rad=function(x){return x*Math.PI/180},deg=function(x){return x*180/Math.PI},mod=function(x,n){return(x%n+n)%n};
function sun(jd){var D=jd-2451545,g=mod(357.529+.98560028*D,360),q=mod(280.459+.98564736*D,360),L=mod(q+1.915*Math.sin(rad(g))+.02*Math.sin(rad(2*g)),360),e=23.439-.00000036*D;
var ra=mod(deg(Math.atan2(Math.cos(rad(e))*Math.sin(rad(L)),Math.cos(rad(L))))/15,24),decl=deg(Math.asin(Math.sin(rad(e))*Math.sin(rad(L)))),eqt=q/15-ra;eqt=eqt-24*Math.round(eqt/24);return[decl,eqt]}
function jdn(y,m,d){if(m<=2){y-=1;m+=12}var A=Math.floor(y/100),B=2-A+Math.floor(A/4);return Math.floor(365.25*(y+4716))+Math.floor(30.6001*(m+1))+d+B-1524.5}
function solatDay(y,m,d,lat,lng){var jd=jdn(y,m,d)-lng/360,noon=function(t){return mod(12-sun(jd+t)[1],24)};
var at=function(a,t,ccw){var decl=sun(jd+t)[0],x=(-Math.sin(rad(a))-Math.sin(rad(decl))*Math.sin(rad(lat)))/(Math.cos(rad(decl))*Math.cos(rad(lat))),T=deg(Math.acos(Math.max(-1,Math.min(1,x))))/15;return noon(t)+(ccw?-T:T)};
var asr=function(t){var decl=sun(jd+t)[0];return at(-deg(Math.atan(1/(1+Math.tan(rad(Math.abs(lat-decl)))))),t,false)};
var v=[at(18,5/24,true),at(.833,6/24,true),noon(.5),asr(13/24),at(.833,.75,false),at(18,.75,false)],adj=8-lng/15;v=v.map(function(x){return(x+adj)*60});
var up=function(x){return Math.ceil(x+1)},sub=up(v[0]);return[sub-10,sub,Math.floor(v[1]),Math.ceil(v[2]+2),up(v[3]),up(v[4]),up(v[5])]}
function day(i){var s=D.start.split('-');return new Date(+s[0],+s[1]-1,+s[2]+i)}
function doy(d){return Math.round((new Date(d.getFullYear(),d.getMonth(),d.getDate())-new Date(d.getFullYear(),0,1))/864e5)}
function hmx(m){return pad(Math.floor(m/60))+':'+pad(m%60)}
function get(u){return fetch(u).then(function(r){if(!r.ok)throw 0;return r.json()})}
function load(z){var y=day(0).getFullYear(),f=z+'-'+y+'.json';if(cache[f])return cache[f];
cache[f]=get('https://quran.ilmualam.com/assets/data/solat/'+f).catch(function(){return get('https://raw.githubusercontent.com/ilmualam/quran/main/assets/data/solat/'+f)}).catch(function(){return null});return cache[f]}
function times(z,o,d){if(o&&o.t&&o.y===d.getFullYear())return o.t[doy(d)];var c=D.zc[z];return solatDay(d.getFullYear(),d.getMonth()+1,d.getDate(),c[0],c[1])}
function draw(z){load(z).then(function(o){var H=['Ahad','Isnin','Selasa','Rabu','Khamis','Jumaat','Sabtu'],B=['Jan','Feb','Mac','Apr','Mei','Jun','Jul','Ogo','Sep','Okt','Nov','Dis'],h='';
cur={z:z,o:o,t:[]};for(var i=0;i<D.n;i++){var d=day(i),t=times(z,o,d);cur.t.push(t);
h+='<tr><td>'+(i+1)+'</td><td>'+d.getDate()+' '+B[d.getMonth()]+'</td><td>'+H[d.getDay()].slice(0,3)+'</td><td><strong>'+hmx(t[0])+'</strong></td><td>'+hmx(t[1])+'</td><td><strong>'+hmx(t[5])+'</strong></td><td>'+hmx(t[6])+'</td></tr>'}
tb.innerHTML=h;src.textContent=o?'Sumber: jadual rasmi JAKIM (e-solat) zon '+z+'.':'Anggaran kiraan parameter JAKIM untuk zon '+z+' (jadual rasmi '+day(0).getFullYear()+' belum diterbitkan); semak e-solat.gov.my.';tick()})}
function tick(){if(!cur)return;var u=new Date(Date.now()+288e5),now=new Date(u.getUTCFullYear(),u.getUTCMonth(),u.getUTCDate(),u.getUTCHours(),u.getUTCMinutes(),u.getUTCSeconds()),
s0=day(0),end=day(D.n),msg;function left(ms){var x=Math.max(0,Math.floor(ms/1000)),hh=Math.floor(x/3600),mm=Math.floor(x%3600/60),ss=x%60;return(hh?hh+' jam ':'')+mm+' minit '+ss+' saat'}
function at(d,m){return new Date(d.getFullYear(),d.getMonth(),d.getDate(),0,m)}
if(now<at(s0,cur.t[0][0])){var dd=Math.ceil((s0-new Date(now.getFullYear(),now.getMonth(),now.getDate()))/864e5);msg=dd>1?'<strong>'+dd+' hari</strong> lagi ke 1 Ramadan '+D.y+'H (jangkaan '+s0.getDate()+'/'+(s0.getMonth()+1)+'/'+s0.getFullYear()+'). Imsak pertama zon '+cur.z+': <strong>'+hmx(cur.t[0][0])+'</strong>.':'Imsak 1 Ramadan zon '+cur.z+' dalam <strong>'+left(at(s0,cur.t[0][0])-now)+'</strong>.'}
else if(now>=at(day(D.n-1),cur.t[D.n-1][5])){msg='Ramadan '+D.y+'H telah berakhir. Semoga Allah menerima puasa kita.'}
else{var i=Math.floor((new Date(now.getFullYear(),now.getMonth(),now.getDate())-s0)/864e5),t=cur.t[i],d=day(i);
if(now<at(d,t[0]))msg='Imsak hari ini ('+(i+1)+' Ramadan) dalam <strong>'+left(at(d,t[0])-now)+'</strong> · pukul '+hmx(t[0]);
else if(now<at(d,t[5]))msg='Berbuka puasa hari ini ('+(i+1)+' Ramadan) dalam <strong>'+left(at(d,t[5])-now)+'</strong> · Maghrib '+hmx(t[5]);
else{var n=cur.t[i+1],dn=day(i+1);msg=n?'Imsak esok ('+(i+2)+' Ramadan) dalam <strong>'+left(at(dn,n[0])-now)+'</strong> · pukul '+hmx(n[0]):'Hari terakhir Ramadan. Selamat Hari Raya Aidilfitri.'}}
cd.innerHTML=msg}
sel.addEventListener('change',function(){try{localStorage.setItem('ilmx-bz-'+D.state,sel.value)}catch(e){}draw(sel.value)});
try{var sv=localStorage.getItem('ilmx-bz-'+D.state);if(sv&&D.zc[sv])sel.value=sv}catch(e){}
draw(sel.value);setInterval(tick,1000);
"""


def widget(P, slug, name, zs):
    z0 = zs[0][0]
    rws, off = rows(z0)
    opts = "".join(f'<option value="{z[0]}">{z[0]} · {e(AREA.get(z[0], z[2])[:60])}</option>' for z in zs)
    data = {"state": slug, "y": SEASON["y"], "start": START.isoformat(), "n": NDAYS, "zc": {z[0]: [z[3], z[4]] for z in zs}}
    return (f'<div class="{P}-box blue"><label for="{P}-bz"><strong>Pilih zon anda</strong></label><br>'
            f'<select id="{P}-bz" style="width:100%;padding:8px;border-radius:8px;margin:6px 0 10px;font:inherit">{opts}</select>'
            f'<p id="{P}-bz-cd" aria-live="polite" style="margin:0;font-size:1.05rem">Kiraan detik dimuatkan…</p></div>'
            + table(["Ramadan", "Tarikh", "Hari", "Imsak", "Subuh", "Berbuka (Maghrib)", "Isyak"], rws).replace("<tbody>", f'<tbody id="{P}-bz-tb">', 1)
            + f'<p id="{P}-bz-src" class="{P}-meta">{"Sumber: jadual rasmi JAKIM (e-solat) zon " + z0 + "." if off else "Anggaran kiraan parameter JAKIM untuk zon " + z0 + "; semak e-solat.gov.my."}</p>'
            + f'<script type="application/json" id="{P}-bz-data">{json.dumps(data)}</script>')


POSTS = []
for slug, (name, qslug, town) in STATES.items():
    meta = POSTS_META[slug]
    zs = zones_of(qslug, town)
    P = "ilmx-bz"
    tname = TITLE_NAME.get(slug, name)
    rws, off = rows(zs[0][0])
    d1 = START
    first = rws[0]
    n = len(zs)
    zone_word = f"{n} Zon" if n > 1 else "Zon"
    POSTS.append((f"berbuka-{slug}", base(
        ns=P, url=meta["url"], published=meta["published"], pubms=f"{int(meta['published'][8:])} {BLN[int(meta['published'][5:7]) - 1]} {meta['published'][:4]}",
        modified=MOD, modms=MODMS,
        title=f"Waktu Berbuka Puasa & Imsak {tname} 2027: Jadual {zone_word} JAKIM",
        desc=next(d for d in (f"Jadual waktu berbuka puasa dan imsak {name} Ramadan 1448H/2027 untuk {n} zon JAKIM, dengan kiraan detik ke waktu berbuka hari ini, doa berbuka dan niat puasa.",
                              f"Jadual waktu berbuka puasa dan imsak {name} Ramadan 1448H/2027 untuk {n} zon JAKIM, dengan kiraan detik ke waktu berbuka hari ini dan doa berbuka.",
                              f"Waktu berbuka puasa dan imsak {name} Ramadan 1448H/2027, {n} zon JAKIM, dengan kiraan detik ke waktu berbuka hari ini dan doa berbuka.") if len(d) <= 160),
        h1=f"Waktu Berbuka Puasa & Imsak {name} 2027",
        img=img(f"berbuka-{slug}", "Ramadan 1448H", f"Waktu Berbuka {tname}", f"Jadual imsak & berbuka 2027 · {n} zon JAKIM", "ذَهَبَ الظَّمَأُ"),
        alt=f"Jadual waktu berbuka puasa dan imsak {name} 2027", refshort="JAKIM e-solat, Sahih Al-Bukhari, Sunan Abu Daud",
        lead=f"Waktu imsak dan berbuka setiap hari Ramadan 1448H bagi semua zon {name}, dengan kiraan detik yang dikemas kini secara langsung.",
        crumb=("Ramadan", "https://www.ilmualam.com/search/label/Ramadan"), about=[f"Waktu berbuka puasa {name}", "Ramadan 1448H", "Waktu imsak"],
        badges=["Data Rasmi JAKIM" if off else "Kiraan Parameter JAKIM", f"{n} Zon {name}", "Ramadan 1448H"],
        answer=f"Ramadan 1448H dijangka bermula <strong>{dms(d1)}</strong>{' mengikut takwim rasmi JAKIM' if OFFICIAL else ''}, tertakluk kepada pengisytiharan Penyimpan Mohor Besar Raja-Raja selepas rukyah. "
               f"Pada 1 Ramadan, waktu <strong>imsak</strong> bagi zon {zs[0][0]} ({e(AREA.get(zs[0][0], zs[0][2])[:50])}) ialah <strong>{first[3][8:-9]}</strong> dan <strong>berbuka</strong> pada <strong>{first[5][8:-9]}</strong>. "
               f"Pilih zon anda di bawah untuk jadual 30 hari dan kiraan detik ke waktu berbuka.",
        sections=[
            ("jadual", f"Jadual Imsak & Berbuka {name} Ramadan 1448H", widget(P, slug, name, zs)),
            ("zon", f"Zon Waktu Solat {name}",
             table(["Zon", "Kawasan"], [[f"<strong>{z[0]}</strong>", e(AREA.get(z[0], z[2]))] for z in zs])
             + f"<p>Waktu di zon yang berlainan boleh berbeza 1 hingga beberapa minit kerana kedudukan matahari. Gunakan zon kawasan anda, bukan zon ibu negeri.</p>"),
            ("imsak", "Apa Itu Imsak dan Bolehkah Makan Selepasnya?",
             "<p><strong>Imsak</strong> ialah waktu berjaga-jaga kira-kira 10 minit sebelum Subuh. Ia bukan waktu wajib berhenti makan: puasa bermula apabila <strong>masuk waktu Subuh</strong>"
             + ref("Al-Baqarah 2:187") + ". Nabi SAW bersabda: “Makan dan minumlah sehingga Ibn Ummi Maktum melaungkan azan”" + ref("HR Al-Bukhari, no. 1919; Muslim, no. 1092")
             + ". Namun berhenti ketika imsak lebih selamat supaya tidak tersilap masa.</p>"),
            ("sunnah", "Sunnah Ketika Berbuka",
             ul("<strong>Segerakan berbuka</strong> sebaik masuk waktu Maghrib: “Manusia sentiasa dalam kebaikan selagi mereka menyegerakan berbuka”" + ref("HR Al-Bukhari, no. 1957"),
                "Berbuka dengan <strong>kurma basah, kurma kering atau air</strong>" + ref("HR Abu Daud, no. 2356; hasan"),
                "Membaca doa: <em>“Dhahabaz-zama'u wabtallatil-'uruqu wa thabatal-ajru insya-Allah”</em> (telah hilang dahaga, urat-urat telah basah, dan pahala tetap insya-Allah)" + ref("HR Abu Daud, no. 2357; hasan"),
                "Berdoa sebelum berbuka, kerana doa orang berpuasa tidak ditolak" + ref("HR At-Tirmizi, no. 3598"))
             + f'<p>Bacaan lengkap: <a href="{DOA_BERBUKA}">Doa Berbuka Puasa & Niat</a> · <a href="{NIAT}">Niat Puasa Ramadan</a> · <a href="{AMALAN}">30 Amalan Ramadan</a>.</p>'),
            ("tarikh", "Tarikh Penting Ramadan 1448H",
             table(["Perkara", "Tarikh (jangkaan)"], [["1 Ramadan 1448H", dms(d1)], ["Malam pertama tarawih", dms(d1 - dt.timedelta(1))],
                                                    ["10 malam terakhir bermula", dms(d1 + dt.timedelta(19))], ["Hari Raya Aidilfitri (1 Syawal)", dms(d1 + dt.timedelta(NDAYS))]])
             + "<p>Tarikh rasmi ditentukan selepas rukyah hilal dan diumumkan oleh Penyimpan Mohor Besar Raja-Raja.</p>"),
        ],
        faq=[(f"Bilakah 1 Ramadan 2027 di {name}?", f"Dijangka {dms(d1)}, tertakluk kepada pengisytiharan rasmi selepas rukyah. Tarikh ini sama di seluruh Malaysia."),
             (f"Pukul berapa waktu berbuka di {town}?", f"Pada 1 Ramadan, berbuka bagi zon {zs[0][0]} ialah pukul {first[5][8:-9]}. Kad di atas memaparkan waktu bagi setiap hari dan setiap zon {name}."),
             ("Bolehkah makan selepas waktu imsak?", "Boleh sehingga masuk waktu Subuh, kerana imsak hanya waktu berjaga-jaga (HR Al-Bukhari 1919). Berhenti ketika imsak lebih selamat."),
             (f"Kenapa waktu berbuka berbeza antara zon di {name}?", "Kerana kedudukan matahari berbeza mengikut longitud dan latitud. JAKIM membahagikan setiap negeri kepada zon supaya waktu lebih tepat."),
             ("Apakah doa berbuka puasa yang sahih?", "“Dhahabaz-zama'u wabtallatil-'uruqu wa thabatal-ajru insya-Allah” (HR Abu Daud 2357, hasan).")],
        refs=["Jabatan Kemajuan Islam Malaysia (JAKIM), e-solat.gov.my: jadual waktu solat zon.", "Al-Quran: Al-Baqarah 2:187.",
              "Sahih Al-Bukhari, no. 1919, 1957; Sahih Muslim, no. 1092.", "Sunan Abu Daud, no. 2356, 2357; Sunan At-Tirmizi, no. 3598."],
        disclaimer=("Waktu diambil daripada jadual rasmi JAKIM bagi zon yang dipilih. " if off else "Jadual rasmi JAKIM bagi sebahagian zon belum diterbitkan; waktu ialah anggaran kiraan parameter JAKIM dan akan bertukar kepada jadual rasmi secara automatik. ")
                   + "Tarikh Ramadan tertakluk kepada pengisytiharan rasmi.",
        related=[(DOA_BERBUKA, "Doa Berbuka Puasa & Niat", "Bacaan sebelum dan selepas sahur"), (BATAL, "Perkara yang Membatalkan Puasa", "Senarai menurut mazhab Syafi'i"),
                 (QADA, "Cara Ganti Puasa & Fidyah", "Kiraan qada dan bayaran fidyah")],
        js=WIDGET_JS.replace("{P}", P))))


if __name__ == "__main__":
    write(POSTS)
