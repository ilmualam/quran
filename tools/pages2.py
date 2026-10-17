"""Pages: /waktu-solat/, /doa-harian/, /zikir-pagi-petang/, /belajar-tajwid/ (same page-dict contract as pages.py)."""
import json, os, datetime as dt
import ibadah as I
import solat as SL
import plans as P
from pages import e, faq_html, hero, side, meta_line, table, tool_cards, SITE, MAIN, TBB

_Q = {}


def ayah(s, a):
    if s not in _Q:
        _Q[s] = json.load(open(f"{P.REPO}/data-surah/surah-{s}.json", encoding="utf8"))
    return _Q[s][a - 1]


def qref(s, a):
    return f'<a href="/#surah-{s}-ayat-{a}">{e(P.NAMES[s - 1])} {s}:{a}</a>'


def quran_block(refs):
    """Arabic + Rumi + translation for a list of (s, a) straight from the dataset."""
    ar = " ".join(f'{e(ayah(s, a)["arabic"])} <span class="an">﴿{a}﴾</span>' for s, a in refs)
    ru = " ".join(e(ayah(s, a)["rumi"]) for s, a in refs)
    tr = " ".join(e(ayah(s, a)["translation"]) for s, a in refs)
    return ar, ru, tr


QUL = [(112, a) for a in range(1, 5)], [(113, a) for a in range(1, 6)], [(114, a) for a in range(1, 7)]


def zref(code):
    """'Q2:255', 'Q2:285-286', 'Q112-114' -> list of (s, a) groups."""
    c = code[1:]
    if c == "112-114":
        return list(QUL)
    s, a = c.split(":")
    if "-" in a:
        a1, a2 = map(int, a.split("-"))
        return [[(int(s), x) for x in range(a1, a2 + 1)]]
    return [[(int(s), int(a))]]


def card(id_, title, ar, ru, mn, src, extra="", cat="", q="", counter=None, cls="dw"):
    txt = f"{title}\n\n{ar}\n\n{ru}\n\nMaksud: {mn}\n({src})"
    txt = txt.replace('<span class="an">', "").replace("</span>", "")
    cnt = (f'<button class="zc" type="button" data-id="{id_}" data-n="{counter}" data-t="{e(title)}">0 / {counter}</button>' if counter else "")
    return (f'<article class="{cls}" id="{id_}" data-c="{cat}" data-q="{e(q or title + " " + ru + " " + mn)}" data-txt="{e(txt)}">'
            f'<header class="dh"><h3>{e(title)}</h3>{f"<span class=zn>{counter}×</span>" if counter else ""}</header>'
            f'<p class="dar" lang="ar" dir="rtl">{ar}</p><p class="dru"><em>{ru}</em></p><p class="dmn"><strong>Maksud:</strong> {mn}</p>'
            f'{f"<p class=dnote>{e(extra)}</p>" if extra else ""}<footer class="df"><span class="dsrc">{src}</span>'
            f'<span class="dbtn">{cnt}<button class="btn2 sm" type="button" data-copy>Salin</button></span></footer></article>')


def build_pages2(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    start = dt.date.fromisoformat(T)
    pages = []

    # ======================= WAKTU SOLAT =======================
    kl = next(c for c in SL.CITIES if c[0] == "kuala-lumpur")
    offp = f"{P.REPO}/assets/data/solat/{kl[5]}-{start.year}.json"
    off = json.load(open(offp)) if os.path.exists(offp) else None
    doy = lambda d: (d - dt.date(d.year, 1, 1)).days
    get = (lambda d: off["t"][doy(d)]) if off else (lambda d: SL.solat_day(d.year, d.month, d.day, kl[3], kl[4]))
    tt = get(start)
    times = "".join(f'<li data-i="{i}"><span class="sn">{n}</span><span class="st">{SL.hm(tt[i])}</span></li>' for i, n in enumerate(SL.NAMES))
    rows = []
    import calendar
    dim = calendar.monthrange(start.year, start.month)[1]
    for k in range(1, dim + 1):
        d = dt.date(start.year, start.month, k)
        r = get(d)
        cls = ' class="today"' if k == start.day else ""
        rows.append(f'<tr{cls}><td>{k} {P.BLS[start.month - 1]}</td>' + "".join(f"<td>{SL.hm(x)}</td>" for x in r) + "</tr>")
    src = (f'Sumber: <strong>jadual rasmi JAKIM</strong>, zon {kl[5]} ({e(off["src"])}).' if off else
           f'Sumber: <strong>kiraan anggaran</strong> parameter JAKIM untuk Kuala Lumpur. Boleh berbeza beberapa minit daripada jadual rasmi; semak <a href="https://www.e-solat.gov.my/" rel="noopener">e-solat.gov.my</a>.')
    states = {}
    for c in SL.CITIES:
        states.setdefault(c[2], []).append(c)
    opts = "".join(f'<optgroup label="{e(st)}">' + "".join(f'<option value="{c[0]}"{" selected" if c[0] == "kuala-lumpur" else ""}>{e(c[1])}</option>' for c in cs) + "</optgroup>" for st, cs in states.items())
    HB = ["Muharam", "Safar", "Rabiulawal", "Rabiulakhir", "Jamadilawal", "Jamadilakhir", "Rejab", "Syaaban", "Ramadan", "Syawal", "Zulkaedah", "Zulhijjah"]
    sdata = json.dumps({"api": "https://www.e-solat.gov.my/index.php?r=esolatApi/TakwimSolat&period=month&zone=", "c": SL.CITIES, "n": SL.NAMES, "fa": SL.FAJR, "is": SL.ISHA, "tz": SL.TZ, "hb": HB}, ensure_ascii=False, separators=(",", ":"))
    wfaq = [
        ("Bilakah waktu imsak?", "Imsak ialah 10 minit sebelum masuk waktu Subuh, mengikut amalan jadual JAKIM. Ia waktu berjaga-jaga untuk berhenti makan dan minum ketika berpuasa; puasa sebenarnya bermula apabila masuk waktu Subuh."),
        ("Bila berakhirnya waktu Subuh?", "Waktu Subuh bermula dengan terbit fajar sadiq dan berakhir apabila matahari terbit (Syuruk). Solat Subuh selepas waktu Syuruk dikira qada."),
        ("Bagaimana waktu Zohor dan Asar ditentukan?", "Zohor masuk apabila matahari tergelincir dari tengah langit (zawal). Dalam mazhab Syafi'i, Asar masuk apabila bayang-bayang objek sama panjang dengan objeknya, ditambah panjang bayang semasa zawal."),
        ("Kenapa waktu solat berbeza antara negeri dan zon?", "Waktu solat bergantung pada kedudukan matahari, jadi ia berubah mengikut longitud dan latitud. JAKIM membahagikan Malaysia kepada lebih 50 zon waktu solat; bandar di timur seperti Kota Kinabalu masuk waktu lebih awal berbanding Alor Setar."),
        ("Adakah waktu di laman ini rasmi?", "Jika paparan menyatakan “jadual rasmi JAKIM”, waktu diambil daripada takwim JAKIM bagi zon tersebut. Jika menyatakan “kiraan anggaran”, waktu dikira (Subuh 18°, Isyak 18°, Asar mazhab Syafi'i) yang dikalibrasi dengan jadual rasmi (kebanyakannya dalam lingkungan 2 minit). Untuk kepastian, rujuk e-solat.gov.my."),
        ("Ke arah mana kiblat dari Malaysia?", "Kiblat dari Malaysia menghala ke barat laut: kira-kira 291° hingga 293° dari utara benar bagi bandar di Semenanjung, dan 290° hingga 292° bagi Sabah, Sarawak dan Labuan. Darjah tepat bagi bandar pilihan anda dipaparkan di atas."),
    ]
    body = hero("Waktu Solat Hari Ini: Jadual Ikut Bandar di Malaysia",
                "Pilih bandar atau guna lokasi anda. Waktu Imsak hingga Isyak, kiraan ke solat seterusnya, jadual sebulan dan arah kiblat.",
                [("Alat", "alat/"), ("Waktu Solat", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira" class="sr">Waktu solat</h2>
<form class="frm" id="sf" novalidate>
<div class="fl w2"><label for="sc">Bandar</label><select id="sc">{opts}</select></div>
</form>
<div class="act" id="sact"><button class="btn2" type="button" id="sgeo">📍 Guna lokasi saya</button><button class="btn2" type="button" data-act="link">🔗 Salin pautan</button><button class="btn2" type="button" data-act="print">🖨 Cetak jadual</button></div>
<div id="sw" class="sw">
<p class="sdate"><span id="sdate">{P.dlong(start)} · Kuala Lumpur</span><br><span id="shij" class="shij"></span></p>
<ol class="stimes" id="stimes">{times}</ol>
<p class="snext" id="snext" aria-live="polite">&nbsp;</p>
<p class="ssrc" id="ssrc">{src}</p>
<p class="sqb">🧭 Arah kiblat: <strong id="sqib">{SL.qibla(kl[3], kl[4]):.1f}°</strong> dari utara benar · <a href="{TBB}arah-kiblat/" rel="noopener">Kompas kiblat ↗</a></p>
</div>
<div class="tw" tabindex="0" role="region" aria-label="Jadual waktu solat sebulan"><table class="plan smon" id="smon">
<caption id="smcap">Jadual waktu solat {P.BLN[start.month - 1]} {start.year} – Kuala Lumpur</caption>
<thead><tr><th scope="col">Tarikh</th>{"".join(f'<th scope="col">{n}</th>' for n in SL.NAMES)}</tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp">Waktu Solat Fardu & Tempohnya</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Solat fardu ada lima waktu: <strong>Subuh</strong> (fajar hingga matahari terbit), <strong>Zohor</strong> (matahari tergelincir hingga bayang sama panjang), <strong>Asar</strong> (hingga matahari terbenam), <strong>Maghrib</strong> (terbenam hingga hilang mega merah) dan <strong>Isyak</strong> (hingga terbit fajar). Imsak ialah 10 minit sebelum Subuh. Waktu tepat bergantung pada lokasi, jadi pilih bandar anda di atas.</p></div>
{meta_line(T, TMS)}
{share(SITE + "waktu-solat/", "Waktu solat hari ini ikut bandar di Malaysia:")}
</div>
{table(["Waktu", "Bermula", "Berakhir", "Catatan"], [
    ["<strong>Imsak</strong>", "10 minit sebelum Subuh", "Subuh", "Waktu berjaga-jaga untuk berhenti sahur"],
    ["<strong>Subuh</strong>", "Terbit fajar sadiq", "Matahari terbit (Syuruk)", "2 rakaat"],
    ["<strong>Zohor</strong>", "Matahari tergelincir (zawal)", "Masuk Asar", "4 rakaat; Jumaat bagi lelaki"],
    ["<strong>Asar</strong>", "Bayang sama panjang objek + bayang zawal (Syafi'i)", "Matahari terbenam", "4 rakaat; makruh melewatkan hingga matahari kekuningan"],
    ["<strong>Maghrib</strong>", "Matahari terbenam", "Hilang mega merah (syafaq)", "3 rakaat; waktu berbuka puasa"],
    ["<strong>Isyak</strong>", "Hilang mega merah", "Terbit fajar sadiq", "4 rakaat; waktu pilihan (ikhtiyar) hingga sepertiga malam"],
], "Waktu solat fardu dan tempohnya")}
</section>
{ad(0)}
<section id="kaedah" aria-labelledby="h-kaedah">
<div class="prose">
<h2 id="h-kaedah">Sumber & Kaedah Kiraan</h2>
<ul>
<li><strong>Jadual rasmi:</strong> takwim waktu solat JAKIM bagi setiap zon disegerakkan setiap bulan dan disimpan dalam laman ini, supaya boleh dibuka dengan pantas dan tanpa internet.</li>
<li><strong>Terus daripada e-solat:</strong> jika jadual zon belum disegerakkan, pelayar anda mengambil jadual bulan semasa terus daripada e-solat.gov.my dan menyimpannya untuk kegunaan luar talian.</li>
<li><strong>Kiraan anggaran</strong> (hanya jika kedua-dua sumber rasmi tidak dapat dicapai): Subuh dan Isyak 18° bawah ufuk, Asar mazhab Syafi'i, matahari terbit/terbenam pada −0.833°, UTC+8, dengan ihtiyat. Parameter ini dikalibrasi dengan jadual rasmi JAKIM 2026 bagi 43 zon: 92–98% waktu berada dalam lingkungan 2 minit daripada jadual rasmi.</li>
<li><strong>Lokasi anda</strong> digunakan dalam pelayar sahaja untuk memilih zon terdekat; ia tidak dihantar kepada kami.</li>
<li>Untuk ibadah yang bergantung pada minit tepat (imsak, berbuka), sentiasa semak dengan <a href="https://www.e-solat.gov.my/" rel="noopener">e-solat.gov.my</a> atau pengumuman masjid setempat.</li>
</ul>
</div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Waktu Solat</h2>
{faq_html(wfaq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("waktu-solat/")}</section>
</div>
{side([("kira", "Waktu hari ini"), ("smon", "Jadual sebulan"), ("h-jwp", "Waktu & tempoh"), ("kaedah", "Sumber & kaedah"), ("faq", "Soalan lazim")], "waktu-solat/")}
</div>'''
    pages.append(dict(path="waktu-solat/", kind="tool", data=False, arabic=False,
                      extra_data=f'<script type="application/json" id="sd">{sdata}</script>',
                      title="Waktu Solat Hari Ini Malaysia: Jadual Bulanan Ikut Bandar",
                      ogtitle="Waktu Solat Hari Ini – Ikut Bandar di Malaysia",
                      desc="Waktu solat hari ini untuk 64 bandar di Malaysia: Imsak, Subuh, Zohor, Asar, Maghrib, Isyak, kiraan ke solat seterusnya, jadual sebulan dan arah kiblat.",
                      crumbs=[("Alat", "alat/"), ("Waktu Solat", None)], body=body, faq=wfaq,
                      app=dict(name="Waktu Solat Malaysia", features=["64 bandar di 16 negeri dan wilayah", "Guna lokasi semasa (zon terdekat)", "Kiraan ke waktu solat seterusnya", "Jadual sebulan boleh dicetak", "Arah kiblat dalam darjah", "Berfungsi tanpa internet"]),
                      about=["Waktu solat", "Solat", "Malaysia"],
                      llms="Waktu solat harian dan bulanan bagi 64 bandar di Malaysia (Imsak, Subuh, Syuruk, Zohor, Asar, Maghrib, Isyak), menggunakan jadual rasmi JAKIM bagi zon berkenaan apabila tersedia, terus daripada e-solat.gov.my, atau kiraan anggaran yang dikalibrasi dengan jadual JAKIM (Subuh 18°, Isyak 18°, Asar Syafi'i). Imsak = 10 minit sebelum Subuh. Termasuk arah kiblat (≈291–293° dari Semenanjung, 290–292° dari Sabah/Sarawak)."))

    # ======================= DOA =======================
    dq_cards = {k: [] for k, _ in I.DOA_CAT}
    for s, a, title, cat in I.DOA_QURAN:
        v = ayah(s, a)
        w = v["arabic"].split()
        k = I.doa_start(s, a, w)
        ar = (" ".join(e(x) for x in w[:k]) + " " if k else "") + f'<mark>{" ".join(e(x) for x in w[k:])}</mark>'
        dq_cards[cat].append(card(f"q{s}-{a}", title, ar, e(v["rumi"]), e(v["translation"]), qref(s, a), cat=cat))
    dh = [card(i, t, e(ar), e(r), e(m), e(src), cat="harian") for i, t, ar, r, m, src in I.DOA_HARIAN]
    am = []
    for i, t, refs, note in I.AYAT_AMALAN:
        groups = [[r] for r in refs] if i != "tiga-qul" else list(QUL)
        ar = " ".join(quran_block(g)[0] for g in groups)
        ru = " ".join(quran_block(g)[1] for g in groups)
        tr = " ".join(quran_block(g)[2] for g in groups)
        src = ", ".join(qref(s, a) for s, a in refs) if i != "tiga-qul" else "Surah 112, 113 & 114"
        am.append(card(i, t, ar, ru, tr, src, extra=note, cat="ayat"))
    cats = [("all", "Semua"), ("harian", "Doa Harian")] + list(I.DOA_CAT) + [("ayat", "Ayat Amalan")]
    total = len(dh) + sum(len(v) for v in dq_cards.values()) + len(am)
    dsecs = "".join(f'<section class="dsec" id="{k}" aria-labelledby="h-{k}"><h3 id="h-{k}" class="dsh">{e(n)}</h3>{"".join(dq_cards[k])}</section>' for k, n in I.DOA_CAT)
    dfaq = [
        ("Apakah doa Sapu Jagat?", "Doa Sapu Jagat ialah “Rabbana atina fid-dunya hasanah, wa fil-akhirati hasanah, wa qina 'azaban-nar” (Al-Baqarah 2:201), memohon kebaikan dunia dan akhirat serta perlindungan daripada neraka. Anas RA meriwayatkan bahawa inilah doa yang paling banyak dibaca Rasulullah SAW (HR Al-Bukhari, no. 6389)."),
        ("Bilakah waktu doa paling mustajab?", "Antaranya sepertiga malam terakhir (HR Al-Bukhari, no. 1145), antara azan dan iqamah (HR Abu Daud, no. 521; At-Tirmizi, no. 212), ketika sujud (HR Muslim, no. 482), satu saat pada hari Jumaat (HR Al-Bukhari, no. 935), dan doa orang berpuasa, pemimpin adil serta orang yang dizalimi (HR At-Tirmizi, no. 3598)."),
        ("Apakah doa Nabi Yunus dan kelebihannya?", "“La ilaha illa anta subhanaka inni kuntu minaz-zalimin” (Al-Anbiya' 21:87). Rasulullah SAW bersabda tiada seorang Muslim pun berdoa dengannya dalam sesuatu urusan melainkan Allah memperkenankannya (HR At-Tirmizi, no. 3505)."),
        ("Doa apa untuk ibu bapa yang masih hidup atau telah meninggal?", "“Rabbirhamhuma kama rabbayani saghira” (Al-Isra' 17:24), “Rabbanaghfir li wa liwalidayya” (Ibrahim 14:41) dan doa Nabi Nuh (Nuh 71:28). Ketiga-tiganya boleh dibaca untuk ibu bapa yang masih hidup atau yang telah meninggal dunia."),
        ("Bolehkah berdoa dalam Bahasa Melayu?", "Di luar solat, berdoa dalam apa-apa bahasa dibenarkan, dan doa dengan bahasa yang difahami membantu kehadiran hati. Di dalam solat, ulama mazhab Syafi'i menganjurkan doa dalam bahasa Arab; rujuk guru untuk perincian."),
        ("Adakah teks doa di halaman ini sahih?", "Doa daripada Al-Quran dipaparkan terus daripada teks mushaf Rasm Uthmani yang sama digunakan dalam pembaca. Doa harian daripada hadis disertakan nama kitab dan nombor hadis supaya boleh disemak. Jika menemui kesilapan, sila hubungi kami."),
    ]
    body = hero("Himpunan Doa Harian, Doa Rabbana & Ayat Amalan",
                f"{total} doa dan ayat pilihan dengan teks Arab, Rumi dan maksud: doa harian daripada hadis sahih, doa-doa dalam Al-Quran dan ayat amalan seperti Ayat Kursi.",
                [("Alat", "alat/"), ("Doa Harian", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="cari" class="tool" aria-labelledby="h-cari">
<h2 id="h-cari" class="sr">Cari doa</h2>
<form class="frm one" id="df" role="search" novalidate><div class="fl"><label for="dq">Cari doa (contoh: makan, tidur, ibu bapa, rezeki)</label><input id="dq" type="search" autocomplete="off" enterkeyhint="search" placeholder="Cari doa…"></div></form>
<div class="chips2" id="dcat" role="group" aria-label="Kategori doa">{"".join(f'<button type="button" data-c="{k}" aria-pressed="{"true" if k == "all" else "false"}">{e(n)}</button>' for k, n in cats)}</div>
<p class="cnt" id="dcnt" role="status">{total} doa dan ayat</p>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Doa yang paling banyak dibaca Rasulullah SAW ialah <strong>doa Sapu Jagat</strong>: <em>Rabbana atina fid-dunya hasanah, wa fil-akhirati hasanah, wa qina 'azaban-nar</em> (Al-Baqarah 2:201; HR Al-Bukhari, no. 6389). Halaman ini menghimpunkan doa harian daripada hadis sahih berserta rujukan, {sum(len(v) for v in dq_cards.values())} doa daripada Al-Quran (doa Rabbana dan doa para nabi) serta ayat amalan seperti Ayat Kursi.</p></div>
{meta_line(T, TMS)}
{share(SITE + "doa-harian/", "Himpunan doa harian & doa Rabbana (Arab, Rumi, maksud):")}
</div>
</section>

<section class="dsec" id="harian" aria-labelledby="h-harian"><h2 id="h-harian">🤲 Doa Harian (Daripada Hadis)</h2>{"".join(dh)}</section>
{ad(0)}
<section aria-labelledby="h-quran"><h2 id="h-quran">📖 Doa Dari Al-Quran</h2><p class="note">Bahagian yang ditanda ialah lafaz doa dalam ayat tersebut. Klik rujukan untuk mendengar bacaan qari.</p>{dsecs}</section>

<section class="dsec" id="ayat" aria-labelledby="h-ayat"><h2 id="h-ayat">✨ Ayat Amalan Pilihan</h2>{"".join(am)}</section>

<section id="adab" aria-labelledby="h-adab">
<div class="prose">
<h2 id="h-adab">Adab Berdoa</h2>
<ol class="steps">
<li><strong>Mulakan dengan pujian kepada Allah dan selawat</strong> ke atas Nabi SAW (HR At-Tirmizi, no. 3477).</li>
<li><strong>Yakin doa akan dimakbulkan</strong> dan jangan tergesa-gesa berkata “aku sudah berdoa tetapi tidak dimakbulkan” (HR Al-Bukhari, no. 6340).</li>
<li><strong>Angkat tangan</strong> dan menghadap kiblat jika mampu.</li>
<li><strong>Pilih waktu mustajab:</strong> sepertiga malam terakhir, antara azan dan iqamah, ketika sujud dan hari Jumaat.</li>
<li><strong>Utamakan rezeki yang halal</strong>, kerana makanan yang haram menghalang doa (HR Muslim, no. 1015).</li>
</ol>
</div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Doa</h2>
{faq_html(dfaq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("doa-harian/")}</section>
</div>
{side([("harian", "Doa harian"), ("rabbana", "Doa Rabbana"), ("nabi", "Doa para nabi"), ("keluarga", "Ibu bapa & keluarga"), ("ampun", "Taubat & keampunan"), ("urusan", "Ilmu & urusan"), ("ayat", "Ayat amalan"), ("adab", "Adab berdoa"), ("faq", "Soalan lazim")], "doa-harian/")}
</div>'''
    pages.append(dict(path="doa-harian/", kind="tool", data=False, arabic=True,
                      title="Himpunan Doa Harian & Doa Rabbana (Arab, Rumi, Maksud)",
                      ogtitle="Himpunan Doa Harian, Doa Rabbana & Ayat Amalan",
                      desc=f"{total} doa dan ayat pilihan: doa harian daripada hadis sahih, doa Rabbana dan doa para nabi dari Al-Quran, Ayat Kursi. Arab, Rumi, maksud & rujukan.",
                      crumbs=[("Alat", "alat/"), ("Doa Harian", None)], body=body, faq=dfaq,
                      app=dict(name="Himpunan Doa Harian & Doa Al-Quran", features=["Doa harian dengan rujukan hadis", f"{sum(len(v) for v in dq_cards.values())} doa dari Al-Quran", "Ayat amalan pilihan", "Carian dan kategori", "Salin doa untuk dikongsi"]),
                      about=["Doa", "Dua", "Al-Quran"],
                      llms=f"Himpunan {total} doa: doa harian (bangun tidur, sebelum tidur, makan, tandas, keluar rumah, masjid, pakaian, hujan, musibah, dukacita, bersin) dengan rujukan Al-Bukhari/Muslim/Abu Daud/At-Tirmizi; doa dari Al-Quran termasuk doa Sapu Jagat 2:201, doa Nabi Yunus 21:87, doa ibu bapa 17:24, 14:41, 71:28, doa ilmu 20:114, doa Nabi Musa 20:25–28; ayat amalan (Ayat Kursi, akhir Al-Baqarah, 3 Qul, At-Talaq 2–3)."))

    # ======================= ZIKIR =======================
    def zcards(lst, sec):
        out = []
        for i, t, ar, ru, mn, n, src, note in lst:
            if ar.startswith("Q"):
                groups = zref(ar)
                ar_ = " ".join(quran_block(g)[0] for g in groups)
                ru_ = " ".join(quran_block(g)[1] for g in groups)
                mn_ = " ".join(quran_block(g)[2] for g in groups)
                src_ = e(src) + " · " + ", ".join(qref(g[0][0], g[0][1]) for g in groups)
                out.append(card(i, t, ar_, ru_, mn_, src_, extra=note, counter=n, cls="dw zw"))
            else:
                out.append(card(i, t, e(ar), e(ru), e(mn), e(src), extra=note, counter=n, cls="dw zw"))
        return "".join(out)
    zfaq = [
        ("Bilakah waktu membaca zikir pagi dan petang?", "Zikir pagi dibaca selepas solat Subuh hingga matahari naik, dan zikir petang selepas solat Asar hingga matahari terbenam. Sebahagian ulama meluaskan waktunya: zikir pagi hingga sebelum Zohor dan zikir petang hingga awal malam."),
        ("Apakah beza zikir pagi dengan zikir petang?", "Kebanyakan bacaannya sama. Perbezaan utama ialah lafaz “asbahna” (kami berpagi) ditukar kepada “amsaina” (kami berpetang), dan “hazal-yaum” (hari ini) kepada “hazihil-lailah” (malam ini). Perbezaan setiap zikir dinyatakan di bawah teksnya."),
        ("Apakah Al-Ma'thurat?", "Al-Ma'thurat ialah himpunan zikir pagi dan petang susunan Imam Hasan Al-Banna yang popular di Malaysia. Kebanyakan bacaannya diambil daripada ayat Al-Quran dan hadis yang sama seperti dalam halaman ini."),
        ("Perlukah berwuduk untuk berzikir?", "Tidak wajib. Zikir boleh dibaca dalam apa-apa keadaan, namun berwuduk dan menghadap kiblat adalah adab yang digalakkan."),
        ("Bolehkah wanita haid membaca zikir pagi petang?", "Boleh. Zikir dan doa dibenarkan ketika haid. Bagi ayat Al-Quran seperti Ayat Kursi dan 3 Qul, mazhab Syafi'i membenarkannya jika dibaca dengan niat zikir, bukan niat tilawah."),
        ("Apakah zikir selepas solat fardu?", "Istighfar 3 kali, “Allahumma antas-salam…”, Ayat Kursi, Subhanallah 33, Alhamdulillah 33, Allahu Akbar 33 dan digenapkan 100 dengan tahlil, kemudian 3 Qul dan doa “Allahumma a'inni 'ala zikrik”. Semuanya ada dalam bahagian “Selepas Solat” di atas dengan rujukan hadis."),
    ]
    zsec = lambda id_, h, lst, lead: (f'<section class="zsec" id="{id_}" aria-labelledby="h-{id_}"><div class="zhd"><h2 id="h-{id_}">{h}</h2>'
                                      f'<p class="zprog" aria-live="polite">0 / {len(lst)} selesai hari ini</p><button class="btn2 sm" type="button" data-zreset>⟲ Set semula</button></div>'
                                      f'<p class="note">{lead}</p>{zcards(lst, id_)}</section>')
    body = hero("Zikir Pagi & Petang, Zikir Selepas Solat & Sebelum Tidur",
                "Bacaan lengkap berdasarkan Al-Quran dan hadis sahih: teks Arab, Rumi, maksud, bilangan dan kaunter yang menanda zikir yang selesai hari ini.",
                [("Alat", "alat/"), ("Zikir", None)])
    body += f'''<div class="wrap mn"><div class="ct zk">
<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Zikir pagi dibaca <strong>selepas Subuh hingga matahari naik</strong> dan zikir petang <strong>selepas Asar hingga Maghrib</strong>. Teras zikirnya ialah Ayat Kursi, 3 Qul (3 kali), Sayyidul Istighfar, “Bismillahil-lazi la yadurru” (3 kali), “Raditu billahi rabba” (3 kali) dan “Hasbiyallah” (7 kali), semuanya dengan rujukan hadis di bawah. Ketik butang kiraan pada setiap zikir untuk menanda bacaan anda.</p></div>
{meta_line(T, TMS)}
{share(SITE + "zikir-pagi-petang/", "Zikir pagi & petang lengkap dengan kaunter:")}
</div>
</section>
{zsec("pagi-petang", "🌅 Zikir Pagi & Petang", I.Z_PAGI_PETANG, "Lafaz petang dinyatakan di bawah zikir yang berbeza. Kiraan disimpan dalam pelayar anda dan bermula semula setiap hari.")}
{ad(0)}
{zsec("selepas-solat", "🕌 Zikir Selepas Solat Fardu", I.Z_SOLAT, "Dibaca selepas memberi salam. Untuk kiraan 33·33·33 dengan butang besar, guna <a href=\"/tasbih-digital/\">Tasbih Digital</a>.")}
{zsec("sebelum-tidur", "🌙 Zikir Sebelum Tidur", I.Z_TIDUR, "Amalan Rasulullah SAW sebelum tidur, termasuk tasbih Fatimah (33·33·34).")}
<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Zikir</h2>
{faq_html(zfaq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("zikir-pagi-petang/")}</section>
</div>
{side([("pagi-petang", "Zikir pagi & petang"), ("selepas-solat", "Selepas solat"), ("sebelum-tidur", "Sebelum tidur"), ("faq", "Soalan lazim")], "zikir-pagi-petang/")}
</div>'''
    pages.append(dict(path="zikir-pagi-petang/", kind="tool", data=False, arabic=True,
                      title="Zikir Pagi & Petang Lengkap, Selepas Solat & Sebelum Tidur",
                      ogtitle="Zikir Pagi & Petang Lengkap (Arab, Rumi, Maksud)",
                      desc="Bacaan zikir pagi dan petang lengkap berdasarkan hadis sahih, zikir selepas solat fardu dan sebelum tidur: Arab, Rumi, maksud, bilangan & kaunter harian.",
                      crumbs=[("Alat", "alat/"), ("Zikir Pagi & Petang", None)], body=body, faq=zfaq,
                      app=dict(name="Zikir Pagi & Petang dengan Kaunter", features=["Zikir pagi & petang lengkap dengan rujukan hadis", "Zikir selepas solat fardu", "Zikir sebelum tidur", "Kaunter setiap zikir, set semula harian", "Teks Arab, Rumi dan maksud"]),
                      about=["Zikir", "Dhikr", "Al-Ma'thurat"],
                      llms="Zikir pagi dan petang (Ayat Kursi, 3 Qul ×3, Asbahna – HR Muslim 2723, Allahumma bika asbahna – HR At-Tirmizi 3391, Sayyidul Istighfar – HR Al-Bukhari 6306, Bismillahil-lazi la yadurru ×3 – HR Abu Daud 5088, Raditu billahi rabba ×3 – HR Abu Daud 5072, Hasbiyallah ×7 – HR Abu Daud 5081, Subhanallahi wa bihamdih ×100 – HR Muslim 2692), zikir selepas solat (istighfar ×3, Allahumma antas-salam – HR Muslim 591, tasbih 33·33·33·1 – HR Muslim 597) dan sebelum tidur (Ayat Kursi – HR Al-Bukhari 2311, tasbih 33·33·34)."))

    # ======================= TAJWID =======================
    words = lambda s, a, idx: " ".join(ayah(s, a)["arabic"].split()[i] for i in idx)
    rules = {"izhar": ("Izhar Halqi", "Nun mati atau tanwin bertemu huruf halqum (ء ه ع ح غ خ): dibaca jelas tanpa dengung."),
             "idgham-g": ("Idgham Maal Ghunnah", "Bertemu ي ن م و (يَنْمُو): nun dimasukkan ke huruf berikutnya dengan dengung 2 harakat. Pengecualian: dalam satu kalimah (seperti دُنْيَا) dibaca izhar."),
             "idgham-b": ("Idgham Bila Ghunnah", "Bertemu ل atau ر: nun dimasukkan tanpa dengung."),
             "iqlab": ("Iqlab", "Bertemu ب: nun ditukar kepada bunyi mim dengan dengung 2 harakat."),
             "ikhfa": ("Ikhfa' Haqiqi", "Bertemu salah satu daripada 15 huruf ikhfa': nun disamarkan antara izhar dan idgham dengan dengung 2 harakat."),
             "ikhfa-s": ("Ikhfa' Syafawi", "Mim mati bertemu ب: mim disamarkan dengan dengung."),
             "idgham-m": ("Idgham Mithlain", "Mim mati bertemu م: dimasukkan dengan dengung 2 harakat."),
             "izhar-s": ("Izhar Syafawi", "Mim mati bertemu selain ب dan م: mim dibaca jelas. Lebih jelas lagi apabila bertemu و atau ف.")}
    ex = {}
    for rid, name, s, a, idx, _ in I.TAJWID:
        ex.setdefault(rid, [s, a, words(s, a, idx), P.NAMES[s - 1]])
    tjdata = json.dumps({"halqi": sorted(I.HALQI), "yanmu": sorted(I.YANMU), "lr": sorted(I.LR), "rules": rules, "ex": ex,
                         "q": [[rid, name, words(s, a, idx), P.NAMES[s - 1], s, a, expl] for rid, name, s, a, idx, expl in I.TAJWID]},
                        ensure_ascii=False, separators=(",", ":"))
    excards = {}
    for rid, name, s, a, idx, expl in I.TAJWID:
        excards.setdefault(name, []).append(f'<li><span class="tjw" lang="ar" dir="rtl">{e(words(s, a, idx))}</span><span class="tjr">{qref(s, a)}</span><span class="tje">{e(expl)}</span></li>')
    exl = lambda names: "".join(f'<h3>{e(n)}</h3><ul class="tjl">{"".join(excards[n])}</ul>' for n in names)
    grid = "".join(f'<button type="button" data-h="{h}" aria-pressed="false">{h}</button>' for h in I.HURUF)
    tfaq = [
        ("Apakah hukum belajar tajwid?", "Menurut ulama qiraat seperti Imam Ibn Al-Jazari, membaca Al-Quran dengan tajwid (menyebut huruf dengan betul) adalah wajib bagi setiap orang yang membaca. Mempelajari teori dan istilah tajwid secara terperinci pula ialah fardu kifayah."),
        ("Berapakah hukum nun mati dan tanwin?", "Lima: Izhar Halqi (6 huruf: ء ه ع ح غ خ), Idgham Maal Ghunnah (ي ن م و), Idgham Bila Ghunnah (ل ر), Iqlab (ب) dan Ikhfa' Haqiqi (15 huruf yang selebihnya)."),
        ("Apakah huruf qalqalah?", "Lima huruf: ق ط ب ج د, dihimpunkan dalam “قُطْبُ جَدٍّ” (qutbu jad). Qalqalah sughra apabila huruf itu mati asli di tengah bacaan; qalqalah kubra apabila diwaqafkan di hujung bacaan."),
        ("Berapa harakat mad wajib muttasil dan mad jaiz munfasil?", "Dalam riwayat Hafs melalui Tariq Asy-Syatibiyyah (bacaan lazim di Malaysia), kedua-duanya dibaca 4 atau 5 harakat. Mad asli 2 harakat, mad lazim 6 harakat, dan mad 'aridh lissukun 2, 4 atau 6 harakat."),
        ("Apakah beza alif lam syamsiah dan qamariah?", "Alif lam syamsiah: lam tidak dibaca dan huruf selepasnya bersyaddah (contoh: ٱلشَّمْسِ). Alif lam qamariah: lam dibaca jelas (contoh: ٱلْقَمَرِ). Terdapat 14 huruf bagi setiap satu."),
        ("Bolehkah belajar tajwid sendiri secara online?", "Teori boleh dipelajari sendiri, dan mendengar bacaan qari membantu. Namun sebutan huruf (makhraj) dan sifatnya perlu diperbetulkan secara bertalaqqi dengan guru bertauliah supaya kesilapan tidak menjadi kebiasaan."),
    ]
    body = hero("Belajar Tajwid Al-Quran: Hukum Nun Mati, Mim Mati, Mad & Qalqalah",
                "Panduan tajwid ringkas dengan contoh dari Juz 30 dan Al-Fatihah, pengesan hukum nun dan mim mati, serta kuiz untuk menguji kefahaman.",
                [("Alat", "alat/"), ("Belajar Tajwid", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="pengesan" class="tool" aria-labelledby="h-peng">
<h2 id="h-peng">🔤 Pengesan Hukum Nun Mati, Tanwin & Mim Mati</h2>
<div class="chips2" id="tjmode" role="group" aria-label="Jenis"><button type="button" data-m="nun" aria-pressed="true">Nun mati / Tanwin</button><button type="button" data-m="mim" aria-pressed="false">Mim mati</button></div>
<div id="tj" class="tjg"><div class="tjgrid" id="tjgrid" role="group" aria-label="Huruf selepasnya">{grid}</div>
<div class="tjout" id="tjout" aria-live="polite"><p>Pilih huruf yang datang selepas nun mati atau tanwin untuk melihat hukumnya.</p></div></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp">Apa Itu Tajwid?</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Tajwid ialah ilmu cara menyebut huruf Al-Quran dengan betul: tempat keluar huruf (makhraj), sifat huruf, dengung, panjang pendek (mad) dan hukum pertemuan huruf. Asas yang paling kerap ditemui ialah <strong>5 hukum nun mati dan tanwin</strong>, <strong>3 hukum mim mati</strong>, <strong>qalqalah</strong> dan <strong>mad</strong>.</p></div>
{meta_line(T, TMS)}
{share(SITE + "belajar-tajwid/", "Belajar tajwid: hukum nun mati, mim mati, mad & kuiz:")}
</div>
</section>

<section id="nun-mati" aria-labelledby="h-nun">
<h2 id="h-nun">Hukum Nun Mati & Tanwin</h2>
{table(["Hukum", "Huruf", "Cara bacaan"], [
    ["<strong>Izhar Halqi</strong>", '<span lang="ar" dir="rtl">ء ه ع ح غ خ</span>', "Jelas, tanpa dengung"],
    ["<strong>Idgham Maal Ghunnah</strong>", '<span lang="ar" dir="rtl">ي ن م و</span>', "Dimasukkan dengan dengung 2 harakat"],
    ["<strong>Idgham Bila Ghunnah</strong>", '<span lang="ar" dir="rtl">ل ر</span>', "Dimasukkan tanpa dengung"],
    ["<strong>Iqlab</strong>", '<span lang="ar" dir="rtl">ب</span>', "Ditukar kepada bunyi mim, berdengung"],
    ["<strong>Ikhfa' Haqiqi</strong>", '<span lang="ar" dir="rtl">ت ث ج د ذ ز س ش ص ض ط ظ ف ق ك</span>', "Disamarkan dengan dengung"],
], "Hukum nun mati dan tanwin")}
{exl(["Izhar Halqi", "Idgham Maal Ghunnah", "Idgham Bila Ghunnah", "Iqlab", "Ikhfa' Haqiqi"])}
</section>
{ad(0)}
<section id="mim-mati" aria-labelledby="h-mim">
<h2 id="h-mim">Hukum Mim Mati</h2>
{table(["Hukum", "Huruf", "Cara bacaan"], [
    ["<strong>Ikhfa' Syafawi</strong>", '<span lang="ar" dir="rtl">ب</span>', "Disamarkan dengan dengung"],
    ["<strong>Idgham Mithlain</strong>", '<span lang="ar" dir="rtl">م</span>', "Dimasukkan dengan dengung"],
    ["<strong>Izhar Syafawi</strong>", "Huruf selain ب dan م", "Jelas tanpa dengung"],
], "Hukum mim mati")}
{exl(["Ikhfa' Syafawi", "Idgham Mithlain (Mim)", "Izhar Syafawi"])}
</section>

<section id="qalqalah" aria-labelledby="h-qal">
<h2 id="h-qal">Qalqalah (ق ط ب ج د)</h2>
{exl(["Qalqalah Sughra", "Qalqalah Kubra"])}
</section>

<section id="mad" aria-labelledby="h-mad">
<h2 id="h-mad">Hukum Mad (Panjang Bacaan)</h2>
{table(["Jenis mad", "Harakat", "Sebab"], [
    ["<strong>Mad Asli (Tabi'i)</strong>", "2", "Huruf mad tanpa hamzah atau sukun selepasnya"],
    ["<strong>Mad Wajib Muttasil</strong>", "4 atau 5", "Huruf mad bertemu hamzah dalam satu kalimah"],
    ["<strong>Mad Jaiz Munfasil</strong>", "4 atau 5", "Huruf mad bertemu hamzah pada kalimah berikutnya"],
    ["<strong>Mad 'Aridh Lissukun</strong>", "2, 4 atau 6", "Sukun kerana waqaf selepas huruf mad"],
    ["<strong>Mad Lazim Kalimi Muthaqqal</strong>", "6", "Huruf mad bertemu huruf bersyaddah dalam satu kalimah"],
    ["<strong>Mad Lin</strong>", "2, 4 atau 6", "Wau/ya mati selepas baris atas, ketika waqaf"],
    ["<strong>Mad Silah Sughra</strong>", "2", "Ha dhamir antara dua huruf berbaris"],
    ["<strong>Mad 'Iwadh</strong>", "2", "Waqaf pada tanwin baris atas"],
    ["<strong>Mad Badal</strong>", "2", "Hamzah diikuti huruf mad"],
], "Jenis-jenis mad")}
<p class="note">Harakat mengikut riwayat Hafs, Tariq Asy-Syatibiyyah, yang lazim diajar di Malaysia.</p>
{exl(["Mad Asli (Tabi'i)", "Mad Wajib Muttasil", "Mad Jaiz Munfasil", "Mad 'Aridh Lissukun", "Mad Lazim Kalimi Muthaqqal", "Mad Lin", "Mad Silah Sughra", "Mad 'Iwadh", "Mad Badal"])}
</section>

<section id="lain" aria-labelledby="h-lain">
<h2 id="h-lain">Ghunnah, Alif Lam & Lam Jalalah</h2>
{exl(["Ghunnah Musyaddadah", "Alif Lam Syamsiah", "Alif Lam Qamariah", "Lam Jalalah Tafkhim", "Lam Jalalah Tarqiq"])}
</section>

<section id="kuiz" class="tool" aria-labelledby="h-kuiz">
<h2 id="h-kuiz">📝 Kuiz Tajwid (10 Soalan)</h2>
<div class="qz" id="qz"><p>Kenal pasti hukum tajwid bagi perkataan yang ditunjukkan. Setiap jawapan disertakan penerangan dan pautan audio ayat.</p><button class="btn3" type="button" data-qstart>Mula kuiz</button></div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Tajwid</h2>
{faq_html(tfaq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("belajar-tajwid/")}</section>
</div>
{side([("pengesan", "Pengesan hukum"), ("nun-mati", "Nun mati & tanwin"), ("mim-mati", "Mim mati"), ("qalqalah", "Qalqalah"), ("mad", "Mad"), ("lain", "Ghunnah & alif lam"), ("kuiz", "Kuiz tajwid"), ("faq", "Soalan lazim")], "belajar-tajwid/")}
</div>'''
    pages.append(dict(path="belajar-tajwid/", kind="tool", data=False, arabic=True,
                      extra_data=f'<script type="application/json" id="tjd">{tjdata}</script>',
                      title="Belajar Tajwid Al-Quran: Nun Mati, Mim Mati, Mad & Kuiz",
                      ogtitle="Belajar Tajwid Al-Quran – Hukum, Contoh & Kuiz",
                      desc="Belajar tajwid dengan contoh dari Juz 30: 5 hukum nun mati dan tanwin, 3 hukum mim mati, qalqalah, 9 jenis mad, alif lam, pengesan hukum dan kuiz.",
                      crumbs=[("Alat", "alat/"), ("Belajar Tajwid", None)], body=body, faq=tfaq,
                      app=dict(name="Belajar Tajwid: Pengesan Hukum & Kuiz", features=["Pengesan hukum nun mati, tanwin dan mim mati", "Kuiz tajwid 10 soalan", "Contoh dari Juz 30 dengan audio", "Jadual mad dan harakat"]),
                      about=["Tajwid", "Al-Quran", "Qiraat"],
                      llms="Panduan tajwid: 5 hukum nun mati/tanwin (Izhar Halqi ء ه ع ح غ خ; Idgham Maal Ghunnah ي ن م و; Idgham Bila Ghunnah ل ر; Iqlab ب; Ikhfa' 15 huruf), 3 hukum mim mati (Ikhfa' Syafawi ب, Idgham Mithlain م, Izhar Syafawi), qalqalah ق ط ب ج د (sughra/kubra), mad (asli 2, wajib muttasil 4–5, jaiz munfasil 4–5 riwayat Hafs Tariq Asy-Syatibiyyah, 'aridh 2/4/6, lazim 6), alif lam syamsiah/qamariah, lam jalalah; contoh dari Juz 30 dan Al-Fatihah; pengesan hukum dan kuiz."))
    return pages
