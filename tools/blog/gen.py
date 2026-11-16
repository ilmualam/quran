"""Builds the 3 pilot refresh posts for www.ilmualam.com (Blogger HTML, self-contained like the 2026 posts):
one shared namespaced stylesheet (assets/blog/post.css, linked from the post), JSON-LD (Article + FAQPage + BreadcrumbList), copy buttons, and for hutang puasa a fidyah
calculator. Quranic text comes from the quran repo's data-surah/, doa text from tools/ibadah.py (already verified)."""
import json, html, os, re, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO + "/tools")
import ibadah as I

OUT = os.path.dirname(os.path.abspath(__file__)) + "/out"
os.makedirs(OUT, exist_ok=True)
MOD = "2026-11-15"
MODMS = "15 November 2026"
IMG = "https://quran.ilmualam.com/assets/blog/"
NS = "ilmx"  # every post shares this class namespace and assets/blog/post.css
CSSV = "1"  # bump when CSS changes so browsers fetch the new file
Q = "https://quran.ilmualam.com/"
e = lambda s: html.escape(str(s), quote=True)
Z = {z[0]: z for z in I.Z_PAGI_PETANG}


def ayah(s, a):
    return json.load(open(f"{REPO}/data-surah/surah-{s}.json", encoding="utf8"))[a - 1]


CSS = """
.{P}{all:initial;display:block;box-sizing:border-box;font-family:-apple-system,'Inter',Roboto,sans-serif;font-size:16px;line-height:1.7;color:#1a1a1a;background:#fff;max-width:min(768px,100%);margin:0 auto;padding:10px}
.{P} *{box-sizing:border-box}
.{P} p{margin:0 0 1rem}
.{P} a{color:#1f7a3c;text-decoration:underline;text-underline-offset:2px}
.{P} h2{font-size:1.35rem;font-weight:800;color:#0c3808;margin:2rem 0 .8rem;line-height:1.3;scroll-margin-top:70px}
.{P} h3{font-size:1.1rem;font-weight:700;color:#1f7a3c;margin:1.3rem 0 .5rem}
.{P} strong{color:#0c3808}
.{P} ul,.{P} ol{padding-left:1.3rem;margin:0 0 1rem}
.{P} li{margin:0 0 .5rem}
.{P} img{display:block;width:100%;height:auto;border-radius:12px;margin:0 0 1rem;aspect-ratio:16/9;object-fit:cover}
.{P}-hero{background:linear-gradient(135deg,#0c3808,#1f7a3c);color:#fff;border-radius:14px;padding:22px 18px;margin:0 0 1rem}
.{P}-hero h2{color:#fff;margin:.4rem 0 .5rem;font-size:1.45rem}
.{P}-hero p{color:#e3f3e6;margin:0;font-size:.95rem}
.{P}-badges{display:flex;flex-wrap:wrap;gap:6px}
.{P}-badge{font-size:.75rem;font-weight:700;padding:3px 10px;border-radius:999px;background:rgba(255,255,255,.16);color:#fff}
.{P}-meta{font-size:.82rem;color:#5b6b60;margin:0 0 1rem;padding:8px 12px;border-left:3px solid #c9a227;background:#fbf8ee;border-radius:6px}
.{P}-answer{background:#effaf2;border:1px solid #bfe3c9;border-left:5px solid #1f7a3c;border-radius:12px;padding:14px 16px;margin:0 0 1.2rem}
.{P}-answer p{margin:0}
.{P}-toc{background:#f6f8f6;border:1px solid #e1e8e3;border-radius:12px;padding:12px 16px;margin:0 0 1rem;font-size:.92rem}
.{P}-toc strong{display:block;margin-bottom:4px}
.{P}-toc ol{margin:0}
.{P}-card{border:1px solid #e1e8e3;border-radius:14px;padding:14px 16px;margin:0 0 1rem;background:#fff;box-shadow:0 1px 3px rgba(12,56,8,.06)}
.{P}-card h3{margin-top:0}
.{P}-ar{font-family:'Amiri','Traditional Arabic','Scheherazade New',serif;font-size:1.7rem;line-height:2.2;direction:rtl;text-align:right;color:#0c3808;margin:.3rem 0 .6rem}
.{P}-ru{font-style:italic;color:#38503f;margin:0 0 .5rem}
.{P}-mn{margin:0 0 .5rem}
.{P}-src{font-size:.82rem;color:#5b6b60;display:flex;flex-wrap:wrap;gap:8px;justify-content:space-between;align-items:center;border-top:1px dashed #d5ded8;padding-top:8px;margin-top:6px}
.{P}-btn{font:inherit;font-size:.82rem;font-weight:700;border:1px solid #bfe3c9;background:#effaf2;color:#0c3808;border-radius:8px;padding:6px 12px;cursor:pointer}
.{P}-tw{overflow-x:auto;margin:0 0 1rem;border:1px solid #e1e8e3;border-radius:12px}
.{P} table{border-collapse:collapse;width:100%;font-size:.9rem;min-width:520px}
.{P} th{background:#0c3808;color:#fff;text-align:left;padding:9px 10px;font-weight:700}
.{P} td{padding:9px 10px;border-top:1px solid #e1e8e3;vertical-align:top}
.{P} tr:nth-child(even) td{background:#f8fbf9}
.{P}-box{border-radius:12px;padding:12px 16px;margin:0 0 1rem;font-size:.95rem}
.{P}-box.amber{background:#fff8e6;border:1px solid #f0d9a0}
.{P}-box.blue{background:#eef5fd;border:1px solid #c7dcf5}
.{P}-calc{border:2px solid #1f7a3c;border-radius:14px;padding:16px;margin:0 0 1.2rem;background:#f8fcf9}
.{P}-calc h3{margin-top:0}
.{P}-grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));margin:0 0 10px}
.{P}-grid label{display:block;font-weight:700;font-size:.85rem;margin-bottom:3px}
.{P}-grid input{width:100%;height:44px;border:1px solid #c8d6cc;border-radius:10px;padding:0 10px;font:inherit;background:#fff}
.{P}-out{background:#0c3808;color:#fff;border-radius:12px;padding:12px 14px;font-size:.95rem}
.{P}-out strong{color:#ffe27a}
.{P}-faq details{border:1px solid #e1e8e3;border-radius:12px;margin:0 0 8px;background:#fff}
.{P}-faq summary{cursor:pointer;font-weight:700;padding:12px 14px;color:#0c3808;list-style:none}
.{P}-faq summary::-webkit-details-marker{display:none}
.{P}-faq summary::after{content:'+';float:right;font-weight:800;color:#1f7a3c}
.{P}-faq details[open] summary::after{content:'–'}
.{P}-faq details>p{padding:0 14px 12px;margin:0}
.{P}-refs{font-size:.85rem;color:#38503f}
.{P}-cta{display:block;background:#effaf2;border:1px solid #bfe3c9;border-radius:12px;padding:12px 14px;margin:0 0 1rem;text-decoration:none!important;color:#0c3808!important;font-weight:700}
.{P}-cta span{display:block;font-weight:400;font-size:.88rem;color:#38503f}
"""

JS = """<script>(function(){var w=document.querySelector('.{P}');if(!w)return;w.addEventListener('click',function(ev){var b=ev.target.closest('[data-copy]');if(!b)return;var c=b.closest('.{P}-card');var t=[].map.call(c.querySelectorAll('h3,.{P}-ar,.{P}-ru,.{P}-mn,.{P}-src span'),function(n){return n.innerText.trim()}).join('\\n\\n')+'\\n\\n'+location.href.split('#')[0];
navigator.clipboard&&navigator.clipboard.writeText(t).then(function(){b.textContent='✓ Disalin';setTimeout(function(){b.textContent='Salin'},1600)})});{EXTRA}})();</script>"""


def card(P, title, ar, ru, mn, src, note=""):
    return (f'<div class="{P}-card"><h3>{e(title)}</h3><p class="{P}-ar" lang="ar" dir="rtl">{ar}</p>'
            + (f'<p class="{P}-ru">{e(ru)}</p>' if ru else "")
            + f'<p class="{P}-mn"><strong>Maksud:</strong> {mn}</p>'
            + (f'<p class="{P}-ru" style="font-style:normal">{note}</p>' if note else "")
            + f'<div class="{P}-src"><span>{src}</span><button class="{P}-btn" type="button" data-copy>Salin</button></div></div>')


def qcard(P, title, s, a1, a2, src=""):
    vs = [ayah(s, a) for a in range(a1, a2 + 1)]
    ar = " ".join(f'{e(v["arabic"])} ﴿{v["id"]}﴾' for v in vs)
    mn = " ".join(e(v["translation"]) for v in vs)
    ref = f'Surah {["Al-Fatihah"][0] if s == 1 else ""}'.strip()
    return card(P, title, ar, "", mn, src)


def table(head, rows):
    return ('<div class="TW"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")


def build(p):
    P = p["ns"]
    toc = "".join(f'<li><a href="#{P}-{sid}">{e(h)}</a></li>' for sid, h, _ in p["sections"])
    secs = "".join(f'<h2 id="{P}-{sid}">{e(h)}</h2>{body}' for sid, h, body in p["sections"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
    refs = "".join(f"<li>{r}</li>" for r in p["refs"])
    badges = "".join(f'<span class="{P}-badge">{e(b)}</span>' for b in p["badges"])
    related = "".join(f'<a class="{P}-cta" href="{u}">{e(t)}<span>{e(d)}</span></a>' for u, t, d in p["related"])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": p["title"][:110], "description": p["desc"], "image": [IMG + p["img"]],
         "datePublished": p["published"], "dateModified": p.get("modified", MOD), "inLanguage": "ms-MY", "mainEntityOfPage": p["url"],
         "author": {"@type": "Organization", "name": "The Ilmu Alam", "url": "https://www.ilmualam.com/"},
         "publisher": {"@type": "Organization", "name": "The Ilmu Alam", "url": "https://www.ilmualam.com/"},
         "about": [{"@type": "Thing", "name": a} for a in p["about"]]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ilmu Alam", "item": "https://www.ilmualam.com/"},
            {"@type": "ListItem", "position": 2, "name": p["crumb"][0], "item": p["crumb"][1]},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": p["url"]}]}]}
    body = f'''<div class="{P}">
<img src="{IMG}{p["img"]}" alt="{e(p["alt"])}" width="1200" height="675" title="{e(p["title"])}">
<div class="{P}-hero"><h2>{e(p["h1"])}</h2><p>{e(p["lead"])}</p><div class="{P}-badges">{badges}</div></div>
<p class="{P}-meta">✍️ Disediakan oleh <strong>Pasukan Editorial The Ilmu Alam</strong> · Dikemas kini {p.get("modms", MODMS)} (asal {p["pubms"]}) · Rujukan: {p["refshort"]}</p>
<div class="{P}-answer"><p><strong>Jawapan ringkas:</strong> {p["answer"]}</p></div>
<nav class="{P}-toc" aria-label="Isi kandungan"><strong>Isi kandungan</strong><ol>{toc}<li><a href="#{P}-faq">Soalan lazim</a></li></ol></nav>
{secs}
<h2 id="{P}-faq">Soalan Lazim</h2><div class="{P}-faq">{faq}</div>
<h2 id="{P}-rujukan">Rujukan</h2><ol class="{P}-refs">{refs}</ol>
<div class="{P}-box blue"><strong>Nota:</strong> {p["disclaimer"]}</div>
<h2 id="{P}-lagi">Baca &amp; Guna Juga</h2>{related}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{JS.replace("{P}", P).replace("{EXTRA}", p.get("js", ""))}
</div>'''
    body = body.replace('class="TW"', f'class="{P}-tw"').replace(P, NS)
    # one shared, cached stylesheet instead of an inline <style>: the body then opens with the headline and lead, so Blogger's
    # auto-snippet (feeds, related posts) is readable text, not CSS. A body <link> blocks rendering of what follows, so no flash.
    return f'<link rel="stylesheet" href="{IMG}post.css?v={CSSV}">\n' + body


def write_css():
    """assets/blog/post.css, served from quran.ilmualam.com (Cloudflare) and shared by every refreshed post."""
    open(f"{REPO}/assets/blog/post.css", "w", encoding="utf8").write(CSS.replace("{P}", NS).strip() + "\n")


# ============================ POST 1: hutang puasa ============================
P1 = "ilmx-hp"
niat_qada = ("نَوَيْتُ صَوْمَ غَدٍ عَنْ قَضَاءِ فَرْضِ شَهْرِ رَمَضَانَ لِلّٰهِ تَعَالَى", "Nawaitu sauma ghadin 'an qada'i fardhi syahri Ramadhana lillahi ta'ala.",
             "Sahaja aku berpuasa esok hari bagi menggantikan (qada) puasa fardu bulan Ramadan kerana Allah Taala.")
calc = f'''<div class="{P1}-calc" id="{P1}-calc"><h3>🧮 Kalkulator Qada &amp; Fidyah Puasa</h3>
<div class="{P1}-grid">
<div><label for="{P1}-d">Bilangan hari puasa tertinggal</label><input id="{P1}-d" type="number" min="0" inputmode="numeric" value="10"></div>
<div><label for="{P1}-y">Berapa Ramadan berlalu sebelum qada?</label><input id="{P1}-y" type="number" min="0" inputmode="numeric" value="2"></div>
<div><label for="{P1}-r">Kadar fidyah sehari negeri anda (RM)</label><input id="{P1}-r" type="number" min="0" step="0.05" inputmode="decimal" placeholder="semak kadar negeri"></div>
</div>
<div class="{P1}-out" id="{P1}-o" aria-live="polite">Isi maklumat di atas.</div>
<p style="font-size:.82rem;color:#5b6b60;margin:.6rem 0 0">Kiraan mengikut pendapat muktamad mazhab Syafi'i: fidyah 1 cupak (mud, ≈0.65 kg makanan asasi) bagi setiap hari, digandakan mengikut bilangan Ramadan yang berlalu tanpa qada tanpa uzur. Kadar dalam ringgit ditetapkan oleh majlis agama negeri; semak laman rasmi majlis agama atau pusat zakat negeri anda.</p></div>'''
calc_js = (f"var d=document.getElementById('{P1}-d'),y=document.getElementById('{P1}-y'),r=document.getElementById('{P1}-r'),o=document.getElementById('{P1}-o');"
           "function f(){var D=Math.max(0,parseInt(d.value)||0),Y=Math.max(0,parseInt(y.value)||0),R=parseFloat(r.value);var m=D*Y;"
           "var s='Wajib qada: <strong>'+D+' hari</strong> puasa.';"
           "if(Y<1){s+=' Belum melepasi Ramadan seterusnya, jadi <strong>tiada fidyah</strong>: segerakan qada.'}"
           "else{s+=' Fidyah: <strong>'+m+' cupak</strong> (≈'+(m*0.65).toFixed(1)+' kg beras) = '+D+' hari × '+Y+' tahun.';"
           "if(R>0)s+=' Anggaran wang: <strong>RM'+(m*R).toFixed(2)+'</strong>.';else s+=' Masukkan kadar negeri untuk anggaran ringgit.'}"
           "o.innerHTML=s}[d,y,r].forEach(function(i){i.addEventListener('input',f)});f();")
POST1 = dict(
    ns=P1, url="https://www.ilmualam.com/2018/01/bagaimana-cara-membayar-hutang-puasa.html", published="2018-01-13", pubms="13 Januari 2018",
    title="Cara Bayar Hutang Puasa Bertahun-tahun: Qada, Fidyah & Kalkulator",
    desc="Cara membayar hutang puasa Ramadan yang tertinggal bertahun-tahun menurut mazhab Syafi'i: qada, fidyah berganda, niat qada, situasi khas dan kalkulator fidyah.",
    h1="Cara Bayar Hutang Puasa Bertahun-tahun (Qada & Fidyah)", img="hutang-puasa-qada-fidyah.webp",
    alt="Cara bayar hutang puasa bertahun-tahun: qada dan fidyah mengikut mazhab Syafi'i",
    lead="Panduan lengkap qada puasa yang tertinggal lama: bila fidyah wajib, kenapa ia berganda, niat qada dan cara menyusun jadual, dengan kalkulator.",
    badges=["Mazhab Syafi'i", "Dalil Al-Quran & Hadis", "Kalkulator Fidyah", "Dikemas kini 2026"],
    refshort="Al-Quran, Sahih Al-Bukhari & Muslim, Al-Fiqh Al-Manhaji",
    crumb=("Hukum", "https://www.ilmualam.com/search/label/Hukum"), about=["Qada puasa", "Fidyah", "Puasa Ramadan"],
    answer="Hutang puasa Ramadan <strong>tidak gugur</strong> walaupun sudah bertahun-tahun: setiap hari yang tertinggal <strong>wajib diqada</strong>. "
           "Jika qada dilewatkan melepasi Ramadan berikutnya <strong>tanpa uzur</strong>, mazhab Syafi'i mewajibkan <strong>fidyah 1 cupak makanan asasi bagi setiap hari, "
           "digandakan mengikut bilangan tahun</strong> yang berlalu. Qada dan fidyah kedua-duanya wajib; fidyah tidak menggantikan qada bagi orang yang masih mampu berpuasa.",
    sections=[
        ("hukum", "Hukum Qada Puasa yang Tertinggal",
         "<p>Puasa Ramadan yang ditinggalkan, sama ada kerana haid, nifas, sakit, musafir atau tanpa uzur, menjadi hutang yang wajib diganti pada hari lain. Allah berfirman:</p>"
         + qcard(P1, "Al-Baqarah 2:184", 2, 184, 184, "Surah Al-Baqarah, ayat 184")
         + "<p>Aisyah RA menceritakan bahawa dia mempunyai hutang puasa Ramadan dan tidak dapat menggantinya kecuali pada bulan Syaaban <em>(HR Al-Bukhari, no. 1950; Muslim, no. 1146)</em>. "
           "Ini menunjukkan qada boleh ditangguhkan hingga sebelum Ramadan berikutnya, tetapi tidak melepasinya tanpa sebab.</p>"
           "<p>Wanita yang haid diperintahkan menqada puasa tetapi tidak menqada solat <em>(HR Muslim, no. 335)</em>.</p>"),
        ("fidyah", "Bila Fidyah Wajib dan Kenapa Ia Berganda",
         table(["Situasi", "Qada", "Fidyah"], [
             ["Uzur berterusan (sakit, hamil) hingga masuk Ramadan berikutnya", "Wajib", "Tiada"],
             ["Melewatkan qada melepasi Ramadan berikutnya <strong>tanpa uzur</strong>", "Wajib", "1 cupak sehari bagi setiap tahun lewat"],
             ["Tua atau sakit tiada harapan sembuh (tidak mampu berpuasa)", "Tidak", "1 cupak sehari (ganti puasa)"],
             ["Hamil / menyusu, bimbang keselamatan <strong>anak</strong> sahaja", "Wajib", "1 cupak sehari"],
             ["Hamil / menyusu, bimbang keselamatan <strong>diri</strong>", "Wajib", "Tiada"],
             ["Meninggal dunia dengan hutang puasa yang sempat diqada", "Wali boleh berpuasa untuknya", "Atau fidyah daripada harta pusaka"]])
         + f'<div class="{P1}-box amber"><strong>Fidyah berganda:</strong> menurut pendapat muktamad mazhab Syafi\'i, fidyah bertambah setiap kali Ramadan berlalu tanpa qada. '
           "Contoh: 5 hari tertinggal dan dilewatkan 3 Ramadan = 5 × 3 = <strong>15 cupak</strong>, dan 5 hari puasa tetap wajib diqada.</div>"
           "<p>Orang yang benar-benar tidak tahu hukum kerana baru memeluk Islam atau jauh daripada ilmu agama dimaafkan daripada fidyah lewat menurut ulama Syafi'i, "
           "tetapi qada tetap wajib. Jika ragu tentang keadaan anda, rujuk pejabat agama Islam daerah.</p>"
           "<p>Bagi waris si mati, Rasulullah SAW bersabda: “Sesiapa yang meninggal dunia dan dia mempunyai hutang puasa, walinya berpuasa untuknya” <em>(HR Al-Bukhari, no. 1952; Muslim, no. 1147)</em>.</p>"),
        ("kalkulator", "Kalkulator Qada & Fidyah", calc),
        ("contoh", "Contoh Kiraan Sebenar",
         table(["Keadaan", "Qada", "Fidyah"], [
             ["Aminah haid 7 hari setiap Ramadan, tidak pernah qada selama 5 tahun kerana lalai", "35 hari", "Ramadan 1: 7 hari × 4 tahun lewat = 28; Ramadan 2: 7 × 3 = 21; Ramadan 3: 7 × 2 = 14; Ramadan 4: 7 × 1 = 7; Ramadan 5: belum lewat = 0. Jumlah <strong>70 cupak</strong>"],
             ["Ali musafir 4 hari, qada pada bulan Syaaban sebelum Ramadan berikutnya", "4 hari", "Tiada (belum melepasi Ramadan berikutnya)"],
             ["Siti hamil dan menyusu dua tahun berturut-turut, bimbang keselamatan anak, 30 hari setahun", "60 hari", "60 cupak kerana bimbangkan anak; tambahan fidyah lewat hanya jika qada ditangguh tanpa uzur selepas uzurnya tamat"]])
         + "<p>Perhatikan contoh pertama: setiap tahun dikira berasingan kerana setiap Ramadan mempunyai tempoh lewatnya sendiri. Kalkulator di atas sesuai untuk hutang satu Ramadan; untuk beberapa Ramadan, kira setiap tahun berasingan dan jumlahkan.</p>"),
        ("cara", "Cara Membayar Hutang Puasa Bertahun-tahun",
         "<ol><li><strong>Kira bilangan hari.</strong> Jika tidak ingat dengan tepat, ambil anggaran yang paling diyakini (ghalabah az-zhann) dan cenderung kepada yang lebih banyak untuk berhati-hati. "
         "Bagi wanita, anggarkan purata hari haid setiap Ramadan × bilangan tahun.</li>"
         "<li><strong>Bayar fidyah segera</strong> (jika wajib) kepada fakir miskin atau melalui pusat zakat negeri. Fidyah boleh dibayar sekaligus dan tidak perlu menunggu qada selesai.</li>"
         "<li><strong>Susun jadual qada.</strong> Contohnya setiap Isnin dan Khamis: 2 hari seminggu menyelesaikan 30 hari dalam kira-kira 15 minggu. Elakkan hari yang haram berpuasa (dua hari raya dan hari tasyrik).</li>"
         "<li><strong>Berniat pada waktu malam</strong> sebelum fajar bagi setiap hari qada, kerana puasa wajib mesti diniatkan pada malamnya <em>(HR Abu Daud, no. 2454; An-Nasa'i, no. 2331)</em>.</li>"
         "<li><strong>Catat kemajuan</strong> sehingga selesai; hutang yang belum diqada ketika meninggal dunia menjadi tanggungan waris.</li></ol>"
         + card(P1, "Lafaz Niat Puasa Qada Ramadan", e(niat_qada[0]), niat_qada[1], e(niat_qada[2]),
                "Lafaz lazim mazhab Syafi'i; niat di dalam hati pada waktu malam ialah wajib, melafazkannya sunat")
         + "<p>Puasa qada yang dibuat pada hari Isnin atau Khamis tetap sah sebagai qada. Sebahagian ulama Syafi'i berpendapat pahala sunat hari tersebut juga diperoleh, "
           "tetapi niat utama mestilah qada.</p>"),
    ],
    faq=[("Adakah hutang puasa terhapus jika sudah lama?", "Tidak. Hutang puasa Ramadan tidak gugur dengan berlalunya masa. Ia wajib diqada, dan jika dilewatkan tanpa uzur melepasi Ramadan berikutnya, fidyah juga wajib mengikut mazhab Syafi'i."),
         ("Berapa fidyah bagi hutang puasa 3 tahun?", "Fidyah ialah 1 cupak makanan asasi bagi setiap hari bagi setiap tahun lewat. Contoh: 10 hari dilewatkan 3 Ramadan = 30 cupak (kira-kira 19.5 kg beras), selain wajib qada 10 hari."),
         ("Bolehkah bayar fidyah sahaja tanpa qada?", "Tidak bagi orang yang masih mampu berpuasa. Fidyah sahaja hanya untuk orang tua atau pesakit yang tiada harapan sembuh."),
         ("Bolehkah qada puasa digabungkan dengan puasa sunat Isnin Khamis?", "Boleh, dan qadanya sah. Sebahagian ulama Syafi'i berpendapat pahala sunat turut diperoleh, dengan syarat niat utamanya ialah qada."),
         ("Bagaimana jika tidak ingat berapa hari puasa yang tertinggal?", "Ambil anggaran yang paling diyakini dan lebihkan sedikit untuk berhati-hati, kemudian qada mengikut bilangan itu.")],
    refs=["Al-Quran: Al-Baqarah 2:184–185.", "Sahih Al-Bukhari, no. 1950, 1952; Sahih Muslim, no. 335, 1146, 1147.", "Sunan Abu Daud, no. 2454; Sunan An-Nasa'i, no. 2331.",
          "Al-Fiqh Al-Manhaji 'ala Mazhab Al-Imam Asy-Syafi'i, bab puasa.", "Kadar fidyah: majlis agama Islam / pusat zakat negeri masing-masing."],
    disclaimer="Panduan umum mengikut mazhab Syafi'i. Untuk kes khusus (contohnya sakit berpanjangan atau hutang si mati), rujuk pejabat mufti atau pejabat agama Islam negeri anda.",
    related=[("https://www.ilmualam.com/2025/11/cara-ganti-puasa-qada.html", "Cara Ganti Puasa (Qada') & Kiraan Fidyah", "Panduan asas qada puasa Ramadan"),
             ("https://www.ilmualam.com/2026/04/cara-solat-qada.html", "Cara Solat Qada & Niat Ganti Solat Tertinggal", "Qada solat bertahun-tahun dengan kalkulator hutang solat"),
             (Q + "kalendar-hijrah/", "Kalendar Hijrah & Puasa Sunat", "Hari Isnin, Khamis dan hari yang haram berpuasa ikut takwim JAKIM"),
             (Q + "zakat-fitrah/", "Kadar Zakat Fitrah Semua Negeri", "Kadar terkini dan kalkulator keluarga")],
    js=calc_js)

# ============================ POST 2: Al-Fatihah ============================
P2 = "ilmx-fth"
POST2 = dict(
    ns=P2, url="https://www.ilmualam.com/2018/02/11-hikmah-dan-keutamaan-membaca-surah.html", published="2018-02-04", pubms="4 Februari 2018",
    title="Kelebihan Surah Al-Fatihah: 7 Fadhilat Sahih & Status Amalan Popular",
    desc="Kelebihan Surah Al-Fatihah daripada hadis sahih: surah paling agung, Ummul Quran, ruqyah dan rukun solat, serta status amalan popular yang tiada asas.",
    h1="Kelebihan Surah Al-Fatihah: 7 Fadhilat Sahih", img="kelebihan-surah-al-fatihah.webp",
    alt="Kelebihan Surah Al-Fatihah: tujuh fadhilat daripada hadis sahih",
    lead="Fadhilat Al-Fatihah yang thabit dalam hadis sahih, nama-namanya, hukumnya dalam solat, dan penilaian jujur terhadap amalan yang tersebar di media sosial.",
    badges=["Hadis Sahih", "7 Fadhilat", "Mazhab Syafi'i", "Dikemas kini 2026"],
    refshort="Sahih Al-Bukhari, Sahih Muslim, Sunan At-Tirmizi",
    crumb=("Al-Quran", "https://www.ilmualam.com/search/label/Al-Quran"), about=["Surah Al-Fatihah", "Kelebihan surah"],
    answer="Surah Al-Fatihah ialah <strong>surah paling agung dalam Al-Quran</strong> <em>(HR Al-Bukhari, no. 4474)</em>, digelar <strong>Ummul Quran</strong> dan "
           "<strong>As-Sab'ul Mathani</strong>, menjadi <strong>rukun setiap rakaat solat</strong> <em>(HR Al-Bukhari, no. 756)</em>, dan pernah digunakan para sahabat sebagai "
           "<strong>ruqyah</strong> yang dibenarkan Nabi SAW <em>(HR Al-Bukhari, no. 5007)</em>. Dakwaan seperti “pahala dua pertiga Al-Quran” pula tiada asas yang sahih.",
    sections=[
        ("bacaan", "Bacaan Surah Al-Fatihah (Arab & Maksud)",
         qcard(P2, "Surah Al-Fatihah (1:1–7)", 1, 1, 7, f'Teks Uthmani &amp; terjemahan Abdullah Basmeih · <a href="{Q}surah-al-fatihah/">Rumi &amp; audio di Al-Quran Online</a>')),
        ("fadhilat", "7 Kelebihan Surah Al-Fatihah daripada Hadis Sahih",
         "<ol>"
         "<li><strong>Surah paling agung dalam Al-Quran.</strong> Nabi SAW memberitahu Abu Sa'id bin Al-Mu'alla bahawa Al-Fatihah ialah surah teragung, “As-Sab'ul Mathani dan Al-Quran yang agung yang diberikan kepadaku.” <em>(HR Al-Bukhari, no. 4474)</em></li>"
         "<li><strong>Tiada tandingannya dalam kitab terdahulu.</strong> Allah tidak menurunkan dalam Taurat, Injil, Zabur mahupun Al-Quran surah yang menyamainya. <em>(HR At-Tirmizi, no. 2875; sahih)</em></li>"
         "<li><strong>Salah satu daripada dua cahaya.</strong> Malaikat memberitahu Nabi SAW tentang dua cahaya yang tidak diberikan kepada nabi sebelumnya: Al-Fatihah dan penutup Surah Al-Baqarah; setiap hurufnya yang dibaca pasti diberikan. <em>(HR Muslim, no. 806)</em></li>"
         "<li><strong>Dialog dengan Allah dalam solat.</strong> Dalam hadis qudsi, Allah membahagikan Al-Fatihah antara-Nya dan hamba-Nya, dan menjawab setiap ayat yang dibaca. <em>(HR Muslim, no. 395)</em></li>"
         "<li><strong>Rukun solat.</strong> “Tiada solat bagi sesiapa yang tidak membaca Fatihatul Kitab.” <em>(HR Al-Bukhari, no. 756; Muslim, no. 394)</em></li>"
         "<li><strong>Ruqyah yang diiktiraf.</strong> Seorang sahabat membaca Al-Fatihah ke atas ketua kabilah yang disengat lalu dia sembuh; Nabi SAW bertanya, “Bagaimana kamu tahu ia ruqyah?” <em>(HR Al-Bukhari, no. 5007; Muslim, no. 2201)</em></li>"
         "<li><strong>Ibu kepada Al-Quran.</strong> Al-Fatihah disebut Ummul Quran, Ummul Kitab dan As-Sab'ul Mathani. <em>(HR Al-Bukhari, no. 4704)</em></li></ol>"),
        ("intipati", "Intipati Al-Fatihah Ayat demi Ayat",
         "<ul><li><strong>Ayat 1–2:</strong> memulakan dengan nama Allah dan memuji-Nya sebagai Rabb seluruh alam: asas tauhid rububiyyah.</li>"
         "<li><strong>Ayat 3:</strong> Ar-Rahman Ar-Rahim, sifat rahmat yang meliputi semua makhluk dan rahmat khusus untuk orang beriman.</li>"
         "<li><strong>Ayat 4:</strong> Allah Pemilik hari pembalasan; mengingatkan bahawa setiap amal akan dihisab.</li>"
         "<li><strong>Ayat 5:</strong> “Hanya kepada-Mu kami menyembah dan hanya kepada-Mu kami memohon pertolongan”: inti tauhid uluhiyyah dan tawakal. Dalam hadis qudsi, Allah berfirman ayat ini antara-Nya dan hamba-Nya <em>(HR Muslim, no. 395)</em>.</li>"
         "<li><strong>Ayat 6–7:</strong> doa paling penting seorang hamba, memohon jalan yang lurus: jalan orang yang diberi nikmat, bukan jalan yang dimurkai atau yang sesat.</li></ul>"
         "<p>Kerana itu ulama menyebut seluruh Al-Quran ialah huraian kepada Al-Fatihah: pujian, akidah, ibadah, kisah umat terdahulu dan petunjuk hidup bermula di sini.</p>"),
        ("nama", "Nama-nama Surah Al-Fatihah",
         table(["Nama", "Maksud", "Sebab"], [
             ["Al-Fatihah", "Pembukaan", "Pembuka mushaf dan bacaan solat"],
             ["Ummul Quran / Ummul Kitab", "Ibu Al-Quran", "Merangkumi intipati Al-Quran: tauhid, ibadah, janji dan petunjuk"],
             ["As-Sab'ul Mathani", "Tujuh yang diulang-ulang", "Tujuh ayat yang dibaca berulang dalam setiap rakaat"],
             ["Ar-Ruqyah", "Jampi / penawar", "Berdasarkan hadis Abu Sa'id (HR Al-Bukhari, no. 5007)"],
             ["Al-Hamd", "Pujian", "Dimulakan dengan Alhamdulillah"]])),
        ("solat", "Al-Fatihah dalam Solat (Mazhab Syafi'i)",
         "<ul><li>Wajib dibaca dalam <strong>setiap rakaat</strong>, oleh imam, makmum dan orang yang solat sendirian.</li>"
         "<li><strong>Bismillah ialah ayat pertama</strong> Al-Fatihah dalam mazhab Syafi'i dan wajib dibaca.</li>"
         "<li>Wajib membaca semua 14 sabdunya dan menjaga tertib serta makhraj huruf; kesalahan yang mengubah makna membatalkan bacaan.</li>"
         "<li>Sunat mengucapkan “Amin” selepasnya; sesiapa yang aminnya bertepatan dengan amin malaikat, diampunkan dosanya yang lalu <em>(HR Al-Bukhari, no. 780)</em>.</li></ul>"
         f'<p>Untuk memperbetulkan bacaan, lihat <a href="{Q}belajar-tajwid/">Belajar Tajwid</a> dan <a href="{Q}belajar-solat/">cara solat langkah demi langkah</a>.</p>'),
        ("status", "Amalan Popular & Statusnya",
         table(["Dakwaan yang tersebar", "Status"], [
             ["Membaca Al-Fatihah menyamai pahala dua pertiga Al-Quran", "Tiada asas sahih. Yang sahih ialah Al-Ikhlas menyamai sepertiga Al-Quran (HR Al-Bukhari, no. 5013)."],
             ["Setiap ayat Al-Fatihah menutup satu pintu neraka", "Tidak ditemui dalam kitab hadis yang muktabar."],
             ["Membaca Al-Fatihah 41 kali untuk hajat", "Amalan ijazah sebahagian guru, bukan daripada hadis. Boleh dibaca sebagai zikir dan wasilah doa tanpa beriktikad fadhilat khusus."],
             ["Membaca Al-Fatihah sebagai ruqyah untuk yang sakit", "Sahih (HR Al-Bukhari, no. 5007), disertai doa dan ikhtiar perubatan."]])
         + f'<div class="{P2}-box amber">Kelebihan Al-Fatihah yang sahih sudah cukup besar. Menyebarkan fadhilat palsu atas nama Nabi SAW berdosa, berdasarkan hadis “Sesiapa berdusta atas namaku dengan sengaja, maka sediakanlah tempatnya dalam neraka” <em>(HR Al-Bukhari, no. 110)</em>.</div>'),
    ],
    faq=[("Apakah kelebihan Surah Al-Fatihah?", "Ia surah paling agung dalam Al-Quran (HR Al-Bukhari 4474), digelar Ummul Quran dan As-Sab'ul Mathani, rukun setiap rakaat solat, salah satu daripada dua cahaya (HR Muslim 806) dan diiktiraf sebagai ruqyah (HR Al-Bukhari 5007)."),
         ("Kenapa Al-Fatihah dipanggil Ummul Quran?", "Kerana ia merangkumi intipati seluruh Al-Quran: pujian dan tauhid kepada Allah, hari pembalasan, ibadah, permohonan pertolongan dan petunjuk jalan yang lurus."),
         ("Adakah Bismillah sebahagian daripada Al-Fatihah?", "Ya dalam mazhab Syafi'i: Bismillah ialah ayat pertama Al-Fatihah dan wajib dibaca dalam solat."),
         ("Adakah benar membaca Al-Fatihah menyamai dua pertiga Al-Quran?", "Tiada hadis sahih tentangnya. Yang sahih ialah Surah Al-Ikhlas menyamai sepertiga Al-Quran (HR Al-Bukhari 5013)."),
         ("Bolehkah Al-Fatihah dibaca untuk mengubati penyakit?", "Boleh. Para sahabat membacanya sebagai ruqyah dan Nabi SAW membenarkannya (HR Al-Bukhari 5007), dengan tetap berikhtiar mendapatkan rawatan perubatan.")],
    refs=["Sahih Al-Bukhari, no. 110, 756, 780, 4474, 4704, 5007, 5013.", "Sahih Muslim, no. 394, 395, 806, 2201.", "Sunan At-Tirmizi, no. 2875.",
          "Teks Al-Quran: rasm Uthmani; terjemahan Abdullah Muhammad Basmeih."],
    disclaimer="Rumi hanyalah alat bantu; belajar bacaan Al-Fatihah dengan guru bertauliah kerana kesalahan bacaan boleh menjejaskan sahnya solat.",
    related=[(Q + "surah-al-fatihah/", "Surah Al-Fatihah: Rumi, Maksud & Audio", "Bacaan penuh dengan audio 5 qari"),
             ("https://www.ilmualam.com/2020/01/kelebihan-surah-yasin-dan-fadhilat.html", "Kelebihan Surah Yasin", "Fadhilat dengan status hadis"),
             (Q + "belajar-tajwid/", "Belajar Tajwid", "Hukum nun mati, mim mati dan mad dengan contoh audio")])

# ============================ POST 3: Doa Al-Afiyah ============================
P3 = "ilmx-afy"
af = Z["afiah"]; afb = Z["afini"]
POST3 = dict(
    ns=P3, url="https://www.ilmualam.com/2020/07/doa-al-afiyah-ringkas-tapi-power.html", published="2020-07-08", pubms="8 Julai 2020",
    title="Doa Al-Afiyah: Bacaan Arab, Rumi, Maksud & Kelebihan (Hadis Sahih)",
    desc="Doa Al-Afiyah yang diamalkan Rasulullah SAW pagi dan petang, dengan tulisan Arab, Rumi, maksud, maksud afiyah, empat lafaz doa afiyah dan kelebihannya.",
    h1="Doa Al-Afiyah: Bacaan Penuh & Kelebihannya", img="doa-al-afiyah-ilustrasi.webp",
    alt="Doa Al-Afiyah memohon keselamatan di dunia dan akhirat",
    lead="Doa memohon afiyah yang tidak pernah ditinggalkan Rasulullah SAW pada waktu pagi dan petang, dengan empat lafaz daripada hadis dan cara mengamalkannya.",
    badges=["Hadis Sahih", "Zikir Pagi & Petang", "Arab · Rumi · Maksud", "Dikemas kini 2026"],
    refshort="Sunan Abu Daud, Sunan At-Tirmizi, Sahih Muslim",
    crumb=("Doa", "https://www.ilmualam.com/search/label/Doa"), about=["Doa Al-Afiyah", "Zikir pagi petang"],
    answer=f"Doa Al-Afiyah ialah <strong>“{e(af[3].split('.')[0])}…”</strong>: memohon keampunan dan keselamatan dalam agama, dunia, keluarga dan harta. "
           "Ibn Umar RA meriwayatkan Rasulullah SAW <strong>tidak pernah meninggalkannya pada waktu pagi dan petang</strong> <em>(HR Abu Daud, no. 5074)</em>. "
           "Baginda juga bersabda, tiada yang dikurniakan selepas keyakinan yang lebih baik daripada afiyah <em>(HR At-Tirmizi, no. 3558)</em>.",
    sections=[
        ("bacaan", "Bacaan Doa Al-Afiyah (Pagi & Petang)",
         card(P3, af[1], e(af[2]), af[3], e(af[4]), "HR Abu Daud, no. 5074; Ibn Majah, no. 3871 (sahih)", "Dibaca sekali pada waktu pagi dan sekali pada waktu petang.")),
        ("maksud", "Apakah Maksud Afiyah?",
         "<p><strong>Afiyah</strong> bermaksud dipelihara oleh Allah daripada segala keburukan: penyakit, musibah, fitnah, dosa dan azab, di dunia dan di akhirat. "
         "Ia lebih luas daripada “sihat”: seseorang boleh sihat tubuh tetapi tidak selamat agamanya. Sebab itu doa ini menyebut empat perkara: "
         "<strong>agama, dunia, keluarga dan harta</strong>, serta perlindungan dari enam arah.</p>"
         "<p>Ungkapan “sihat wal afiat” yang biasa kita ucapkan berasal daripada makna ini.</p>"),
        ("lafaz", "4 Lafaz Doa Afiyah daripada Hadis",
         card(P3, "1. Doa ringkas memohon afiyah", "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَافِيَةَ", "Allahumma inni as'alukal-'afiyah.", "Ya Allah, sesungguhnya aku memohon afiyah kepada-Mu.",
              "HR At-Tirmizi, no. 3514: Nabi SAW mengajar bapa saudaranya Al-Abbas: “Mintalah afiyah kepada Allah.”")
         + card(P3, "2. Afiyah tubuh, pendengaran dan penglihatan (3×)", e(afb[2]), afb[3], e(afb[4]), "HR Abu Daud, no. 5090 (hasan)", "Dibaca tiga kali pada waktu pagi dan petang.")
         + card(P3, "3. Doa Lailatul Qadar (memohon kemaafan)", "اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي", "Allahumma innaka 'afuwwun tuhibbul-'afwa fa'fu 'anni.",
                "Ya Allah, sesungguhnya Engkau Maha Pemaaf, Engkau suka memaafkan, maka maafkanlah aku.", "HR At-Tirmizi, no. 3513 (sahih)",
                "Tambahan “karim” selepas 'afuwwun yang popular tidak terdapat dalam riwayat yang sahih.")
         + card(P3, "4. Doa lengkap yang diajar kepada orang yang baru memeluk Islam", "اللَّهُمَّ اغْفِرْ لِي وَارْحَمْنِي وَاهْدِنِي وَعَافِنِي وَارْزُقْنِي",
                "Allahummaghfir li warhamni wahdini wa 'afini warzuqni.", "Ya Allah, ampunilah aku, rahmatilah aku, berilah aku petunjuk, kurniakanlah aku afiyah dan berilah aku rezeki.",
                "HR Muslim, no. 2697")),
        ("kelebihan", "Kelebihan Doa Al-Afiyah",
         "<ul><li>Amalan tetap Rasulullah SAW setiap pagi dan petang <em>(HR Abu Daud, no. 5074)</em>.</li>"
         "<li>“Mohonlah kepada Allah keampunan dan afiyah, kerana tiada seorang pun dikurniakan sesuatu selepas keyakinan yang lebih baik daripada afiyah.” <em>(HR At-Tirmizi, no. 3558)</em></li>"
         "<li>Ketika Al-Abbas meminta doa yang patut dimohon, Nabi SAW berulang kali menjawab: mintalah afiyah, di dunia dan akhirat <em>(HR At-Tirmizi, no. 3514)</em>.</li>"
         "<li>Satu doa merangkumi perlindungan agama, kesihatan, keluarga, harta dan keselamatan diri.</li></ul>"),
        ("silap", "Kesilapan Biasa ketika Mengamalkan Doa Afiyah",
         table(["Kesilapan", "Yang betul"], [
             ["Menganggap afiyah hanya bermaksud sihat tubuh badan", "Afiyah merangkumi keselamatan agama, dunia, keluarga dan harta, serta keampunan di akhirat"],
             ["Menambah “karim” dalam doa Lailatul Qadar dan menyangkanya lafaz hadis", "Lafaz sahih: Allahumma innaka 'afuwwun tuhibbul-'afwa fa'fu 'anni (HR At-Tirmizi, no. 3513)"],
             ["Hanya membaca ketika sakit", "Rasulullah SAW membacanya setiap pagi dan petang ketika sihat (HR Abu Daud, no. 5074)"],
             ["Berdoa tanpa memahami maksud", "Fahami setiap bahagian: agama, dunia, keluarga, harta dan perlindungan enam arah"]])
         + "<p>Doa afiyah juga sesuai dibaca untuk ahli keluarga yang sakit atau sedang bermusafir, dengan menggantikan kata ganti (contohnya “'afihi”, sihatkanlah dia) ketika berdoa dengan bahasa sendiri.</p>"),
        ("amal", "Cara Mengamalkan",
         "<ol><li>Baca selepas solat Subuh (zikir pagi) dan selepas Asar atau Maghrib (zikir petang).</li>"
         "<li>Fahami maksudnya dan hadirkan hajat: kesihatan keluarga, keselamatan perjalanan, keberkatan rezeki.</li>"
         "<li>Gabungkan dengan zikir pagi dan petang yang lain dan istighfar.</li></ol>"
         f'<p>Gunakan <a href="{Q}zikir-pagi-petang/">kaunter Zikir Pagi &amp; Petang</a> untuk menanda bacaan harian anda; doa ini termasuk dalam senarai.</p>'),
    ],
    faq=[("Apakah doa Al-Afiyah?", "Allahumma inni as'alukal-'afwa wal-'afiyah fid-dunya wal-akhirah… (HR Abu Daud 5074): memohon keampunan dan keselamatan dalam agama, dunia, keluarga dan harta, serta perlindungan dari semua arah."),
         ("Bilakah doa Al-Afiyah dibaca?", "Pada waktu pagi dan petang. Rasulullah SAW tidak pernah meninggalkannya pada kedua-dua waktu itu (HR Abu Daud 5074)."),
         ("Apakah maksud afiyah?", "Dipelihara oleh Allah daripada segala keburukan, sama ada penyakit, musibah, fitnah atau dosa, di dunia dan akhirat. Ia lebih luas daripada kesihatan tubuh."),
         ("Adakah lafaz “Allahumma innaka 'afuwwun karim” sahih?", "Riwayat sahih dalam At-Tirmizi (3513) tanpa perkataan “karim”. Lafaz yang sahih: Allahumma innaka 'afuwwun tuhibbul-'afwa fa'fu 'anni.")],
    refs=["Sunan Abu Daud, no. 5074, 5090.", "Sunan At-Tirmizi, no. 3513, 3514, 3558.", "Sunan Ibn Majah, no. 3871.", "Sahih Muslim, no. 2697.",
          "Imam An-Nawawi, Al-Azkar, bab zikir pagi dan petang."],
    disclaimer="Rumi ialah alat bantu sebutan; rujuk guru untuk sebutan Arab yang tepat.",
    related=[(Q + "zikir-pagi-petang/", "Zikir Pagi & Petang (dengan Kaunter)", "Senarai lengkap dengan rujukan hadis"),
             (Q + "doa-harian/", "Himpunan Doa Harian", "Doa daripada hadis dan Al-Quran dengan rujukan"),
             (Q + "doa-orang-sakit/", "Doa Orang Sakit", "Doa ketika sakit dan menziarahi pesakit")])

def write(items):
    """items: [(slug, post dict)] -> out/<slug>.html + out/<slug>.json; prints a size/word report."""
    write_css()
    for slug, p in items:
        h = build(p)
        open(f"{OUT}/{slug}.html", "w", encoding="utf8").write(h)
        json.dump({k: p[k] for k in ("url", "title", "desc", "img", "alt", "published")}, open(f"{OUT}/{slug}.json", "w"), ensure_ascii=False, indent=1)
        t = re.sub(r"<style.*?</style>|<script.*?</script>|<link[^>]*>", " ", h, flags=re.S); t = re.sub(r"<[^>]+>", " ", t)
        assert len(p["title"]) <= 70 and len(p["desc"]) <= 160, (slug, len(p["title"]), len(p["desc"]))
        print(slug, "words", len(t.split()), "| html KB", round(len(h) / 1024, 1), "| title", len(p["title"]), "| desc", len(p["desc"]))


PILOT = [("hutang-puasa", POST1), ("al-fatihah", POST2), ("doa-al-afiyah", POST3)]
if __name__ == "__main__":
    write(PILOT)
