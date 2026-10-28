"""Pages: /kisah-nabi/ (the 25 prophets named in the Quran, how often each is named, Ulul Azmi, surah named after them) and
/kisah-nabi/<slug>/ x25 (facts, the story point by point with the ayat it rests on, key ayat in full, every ayah that names
the prophet). Counts and ayat come from tools/nabi.py, which reads data-surah/. Static pages: no alat.js."""
import re
import nabi as NB
import plans as P
from pages import e, faq_html, hero, side, meta_line, table, tool_cards, SITE
from pages2 import qref, quran_block, card

HUB = "kisah-nabi/"
PUB = "2026-10-29"
NAMA = NB.title


def refs(rs):
    return ", ".join(qref(s, a) for s, a in rs)


def sname(s):
    return P.NAMES[s - 1]


def kali_txt(n):
    if n["slug"] == "nabi-muhammad":
        return "5 kali (Muhammad 4 kali, Ahmad sekali)"
    return f"{n['kali']} kali dalam {n['ayat']} ayat" if n["kali"] != n["ayat"] else f"{n['kali']} kali"


def key_cards(n):
    out = []
    for s, a in n["key"]:
        ar, ru, tr = quran_block([(s, a)])
        out.append(card(f"ayat-{s}-{a}", f"{sname(s)} {s}:{a}", ar, ru, tr, qref(s, a)))
    return "".join(out)


def hit_list(n):
    """Every ayah naming the prophet, grouped by surah, translation with the Malay name marked."""
    groups = []
    for s in n["surahs"]:
        lis = []
        for s2, a, _ in n["hits"]:
            if s2 != s:
                continue
            tr = n["re"].sub(r"<mark>\1</mark>", e(NB.ayah(s, a)["translation"]))
            lis.append(f'<li><p class="cref"><a href="/#surah-{s}-ayat-{a}">{e(sname(s))} {s}:{a}</a></p><p>{tr}</p></li>')
        cnt = len(lis)
        groups.append(f'<details class="zpx"{" open" if len(n["surahs"]) <= 4 else ""}><summary>{s}. {e(sname(s))} · {cnt} ayat</summary>'
                      f'<ul class="hits">{"".join(lis)}</ul></details>')
    return "".join(groups)


def nav(i):
    p, q = NB.NABI[i - 1] if i else None, NB.NABI[i + 1] if i + 1 < len(NB.NABI) else None
    a = f'<a href="/{HUB}{p["slug"]}/">← {e(NAMA(p))}</a>' if p else "<span></span>"
    b = f'<a href="/{HUB}{q["slug"]}/">{e(NAMA(q))} →</a>' if q else "<span></span>"
    return f'<nav class="nbnav" aria-label="Nabi sebelum dan selepas">{a}{b}</nav>'


def all_links(skip):
    return '<ul class="rel sts">' + "".join(f'<li><a href="/{HUB}{n["slug"]}/">{i}. {e(NAMA(n))}</a></li>'
                                            for i, n in enumerate(NB.NABI, 1) if n["slug"] != skip) + "</ul>"


def person(n, url):
    return {"@type": "Person", "@id": url + "#nabi", "name": NAMA(n), "alternateName": [n["ar"], f"Nabi {n['nama']}"],
            "description": n["gelaran"], "subjectOf": {"@id": url + "#webpage"}}


def build_pages13(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    pages = []
    N = NB.NABI
    top = max(n["kali"] for n in N)

    # ---------------- 25 prophet pages ----------------
    for i, n in enumerate(N):
        url = f"{HUB}{n['slug']}/"
        nm = NAMA(n)
        ns = len(n["surahs"])
        most = max(n["surahs"], key=lambda s: sum(1 for s2, _, _ in n["hits"] if s2 == s))
        facts = [["Nama dalam bahasa Arab", f'<span lang="ar" dir="rtl" class="nar">{e(n["ar"])}</span>'], ["Gelaran", e(n["gelaran"])],
                 ["Diutus kepada", e(n["kaum"])], ["Tempat", e(n["tempat"])], ["Kitab", e(n["kitab"])], ["Mukjizat / keistimewaan", e(n["mukjizat"])],
                 ["Ulul Azmi", "Ya" if n.get("ulul") else "Tidak"], ["Urutan dalam senarai 25 nabi", f"Ke-{i + 1}"],
                 ["Namanya disebut dalam Al-Quran", f"{kali_txt(n)}, dalam {ns} surah"]]
        if n.get("surah"):
            facts.append(["Surah bernama sempena", f'<a href="/#surah-{n["surah"]}">Surah {e(sname(n["surah"]))} ({n["surah"]})</a>'])
        kisah = "".join(f"<li>{e(t)} <span class=\"nref\">({refs(rs)})</span></li>" for t, rs in n["kisah"])
        lead_kisah = n["kisah"][0][0]
        faq = [(f"Berapa kali nama {nm} disebut dalam Al-Quran?",
                f"Nama {nm} disebut {kali_txt(n)}, merentasi {ns} surah. Paling banyak dalam Surah {sname(most)}. "
                "Kiraan ini mengira sebutan nama sahaja (bukan kata ganti atau gelaran), berdasarkan teks Uthmani; sumber lain mungkin berbeza sedikit kerana kaedah kiraan."),
               (f"Apakah mukjizat {nm}?", f"{n['mukjizat']}."),
               (f"Kepada siapa {nm} diutus?", f"{n['kaum']}. Tempat: {n['tempat']}."),
               (f"Apakah pengajaran daripada kisah {nm}?", n["pengajaran"])]
        if n.get("ulul"):
            faq.append((f"Adakah {nm} seorang Ulul Azmi?", f"Ya. {nm} ialah salah seorang daripada lima rasul Ulul Azmi: Nabi Nuh, Nabi Ibrahim, Nabi Musa, Nabi Isa dan Nabi Muhammad SAW (rujuk Al-Ahqaf 46:35, Al-Ahzab 33:7 dan Asy-Syura 42:13)."))
        body = hero(f"{e(nm)} dalam Al-Quran: Kisah, Mukjizat & Ayat",
                    f"Kisah {e(nm)} ringkas berdasarkan ayat Al-Quran, serta senarai lengkap {n['ayat']} ayat yang menyebut namanya.",
                    [("Kisah 25 Nabi", HUB), (nm, None)])
        body += f'''<div class="wrap mn"><div class="ct">
<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {e(nm)} ialah nabi ke-{i + 1} daripada 25 nabi dan rasul yang wajib diketahui. Namanya disebut <strong>{kali_txt(n)}</strong> dalam Al-Quran, merentasi {ns} surah. {e(lead_kisah)} Mukjizat: {e(n["mukjizat"][0].lower() + n["mukjizat"][1:])}.</p></div>
{meta_line(T, TMS)}
{share(SITE + url, f"{nm} dalam Al-Quran: kisah, mukjizat dan ayat:")}
</div>
</section>

<section id="fakta" aria-labelledby="h-fakta">
<h2 id="h-fakta">Fakta {e(nm)}</h2>
{table(["Perkara", "Keterangan"], facts, f"Fakta {nm}")}
</section>

<section id="kisah" aria-labelledby="h-kisah">
<h2 id="h-kisah">Kisah {e(nm)} Mengikut Al-Quran</h2>
<ol class="nkisah">{kisah}</ol>
<p><strong>Pengajaran:</strong> {e(n["pengajaran"])}</p>
<p class="note">Kisah ini diringkaskan terus daripada ayat yang dirujuk; tekan rujukan untuk membaca ayat penuh dengan audio. Untuk huraian lanjut, rujuk kitab tafsir muktabar seperti Tafsir Ibnu Kathir.</p>
</section>

<section class="dsec" id="ayat-pilihan" aria-labelledby="h-ap">
<h2 id="h-ap">Ayat Pilihan</h2>
{key_cards(n)}
</section>
{ad(0)}
<section id="semua-ayat" aria-labelledby="h-sa">
<h2 id="h-sa">Semua {n["ayat"]} Ayat yang Menyebut Nama {e(nm)}</h2>
<p>Disusun mengikut surah. Terjemahan Bahasa Melayu (Abdullah Muhammad Basmeih); tekan rujukan untuk membaca teks Arab dan mendengar audio.</p>
{hit_list(n)}
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: {e(nm)}</h2>
{faq_html(faq)}
</section>

<section id="nabi-lain" aria-labelledby="h-nl">
<h2 id="h-nl">Nabi dan Rasul Lain</h2>
{nav(i)}
{all_links(n["slug"])}
<p class="note"><a href="/{HUB}">Senarai 25 nabi & kiraan sebutan</a> · <a href="{NB.MAIN_ARTICLE}" rel="noopener">Artikel penuh 25 Nabi dan Rasul (garis masa & kuiz) ↗</a> · <a href="/doa-harian/#nabi">Doa para nabi</a></p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(HUB)}</section>
</div>
{side([("fakta", "Fakta"), ("kisah", "Kisah"), ("ayat-pilihan", "Ayat pilihan"), ("semua-ayat", "Semua ayat"), ("faq", "Soalan lazim"), ("nabi-lain", "Nabi lain")], HUB)}
</div>'''
        title = f"{nm} dalam Al-Quran: Kisah, Mukjizat & {n['ayat']} Ayat"
        desc = f"Kisah {nm} ringkas daripada Al-Quran: gelaran, kaum, mukjizat dan pengajaran, serta {n['ayat']} ayat yang menyebut namanya ({kali_txt(n)})."
        if len(desc) > 160:
            desc = f"Kisah {nm} daripada Al-Quran: kaum, mukjizat, pengajaran dan {n['ayat']} ayat yang menyebut namanya."
        pages.append(dict(path=url, kind="ref", data=False, arabic=True, published=PUB, nocache=True,
                          title=title, ogtitle=f"Kisah {nm} dalam Al-Quran", desc=desc,
                          crumbs=[("Kisah 25 Nabi", HUB), (nm, None)], body=body, faq=faq, about=[nm, "Nabi dan rasul", "Kisah nabi"],
                          about_ref=SITE + url + "#nabi", nodes=[person(n, SITE + url)], og="kisah-nabi",
                          ogcard=("Kisah 25 Nabi dalam Al-Quran", "Kisah, mukjizat dan setiap ayat yang menyebut nama 25 nabi dan rasul."),
                          llms=f"{nm}: {n['gelaran']}; diutus kepada {n['kaum']}; mukjizat: {n['mukjizat']}. Disebut {kali_txt(n)} dalam {ns} surah. Senarai semua ayat."))

    # ---------------- hub ----------------
    rows = []
    for i, n in enumerate(N, 1):
        nm = NAMA(n)
        rows.append([str(i), f'<a href="/{HUB}{n["slug"]}/"><strong>{e(nm)}</strong></a>{" ⭐" if n.get("ulul") else ""}',
                     f'<span lang="ar" dir="rtl" class="nar">{e(n["ar"])}</span>', e(n["kaum"]), f'{n["kali"]}', str(len(n["surahs"]))])
    rank = sorted(N, key=lambda n: -n["kali"])
    bars = "".join(f'<li><a href="/{HUB}{n["slug"]}/">{e(NAMA(n))}</a><span class="nbar" style="--w:{max(2, round(n["kali"] / top * 100))}%"></span><span class="nkali">{n["kali"]}</span></li>'
                   for n in rank)
    ulul = [n for n in N if n.get("ulul")]
    named = [n for n in N if n.get("surah")]
    srows = [[f'<a href="/#surah-{n["surah"]}">Surah {e(sname(n["surah"]))}</a>', str(n["surah"]), f'<a href="/{HUB}{n["slug"]}/">{e(NAMA(n))}</a>'] for n in sorted(named, key=lambda n: n["surah"])]
    in21 = sum(1 for n in N if any(s == 21 for s, _, _ in n["hits"]))
    anam = [n["nama"] for n in N if any((s, a) in NB.ANAM for s, a, _ in n["hits"])]
    assert len(anam) == 18, anam
    srows.append(['<a href="/#surah-21">Surah Al-Anbiya\'</a>', "21", f"“Para Nabi”: {in21} nabi disebut namanya, serta Nabi Yunus dengan gelaran Zun-Nun"])
    u1 = quran_block([(46, 35)])
    u2 = quran_block([(33, 7)])
    an = quran_block(NB.ANAM)
    musa, ibr = rank[0], rank[1]
    hfaq = [
        ("Siapakah 25 nabi dan rasul yang wajib diketahui?", "Adam, Idris, Nuh, Hud, Soleh, Ibrahim, Lut, Ismail, Ishak, Yaakub, Yusuf, Ayub, Syuaib, Musa, Harun, Zulkifli, Daud, Sulaiman, Ilyas, Ilyasa', Yunus, Zakaria, Yahya, Isa dan Muhammad SAW. Mereka wajib diketahui kerana nama mereka disebut dalam Al-Quran."),
        ("Nabi manakah yang paling banyak disebut dalam Al-Quran?", f"Nabi Musa AS: namanya disebut {musa['kali']} kali dalam {musa['ayat']} ayat merentasi {len(musa['surahs'])} surah. Diikuti Nabi Ibrahim AS ({ibr['kali']} kali) dan Nabi Nuh AS (43 kali). Nama Nabi Muhammad SAW disebut 4 kali, dan sekali lagi dengan nama Ahmad (As-Saff 61:6)."),
        ("Siapakah Rasul Ulul Azmi?", "Lima rasul yang paling tinggi ketabahan dan keazamannya: Nabi Nuh, Nabi Ibrahim, Nabi Musa, Nabi Isa dan Nabi Muhammad SAW. Istilah Ulul Azmi datang daripada Al-Ahqaf 46:35, dan kelima-lima mereka disebut bersama dalam Al-Ahzab 33:7 dan Asy-Syura 42:13."),
        ("Apakah beza nabi dan rasul?", "Menurut pandangan masyhur, nabi menerima wahyu untuk diamalkan, manakala rasul menerima wahyu dan diperintah menyampaikannya kepada kaum yang diutus kepadanya. Setiap rasul ialah nabi, tetapi bukan setiap nabi ialah rasul."),
        ("Adakah nabi hanya 25 orang?", "Tidak. Allah berfirman ada rasul yang dikisahkan dan ada yang tidak dikisahkan kepada Nabi Muhammad SAW (An-Nisa' 4:164; Ghafir 40:78). 25 orang ini wajib diketahui kerana disebut namanya dalam Al-Quran; jumlah keseluruhan nabi hanya diketahui Allah, walaupun ada riwayat yang menyebut bilangan tertentu."),
        ("Ayat manakah yang menyebut paling banyak nama nabi sekali gus?", "Surah Al-An'am ayat 83 hingga 86 menyebut 18 nama nabi berturut-turut: Ibrahim, Ishak, Yaakub, Nuh, Daud, Sulaiman, Ayub, Yusuf, Musa, Harun, Zakaria, Yahya, Isa, Ilyas, Ismail, Ilyasa', Yunus dan Lut."),
        ("Surah apa yang dinamakan sempena nama nabi?", "Enam surah: Yunus (10), Hud (11), Yusuf (12), Ibrahim (14), Muhammad (47) dan Nuh (71). Surah Al-Anbiya' (21) pula bermaksud “para nabi”."),
    ]
    hbody = hero("Kisah 25 Nabi dalam Al-Quran: Ayat, Mukjizat & Kiraan Sebutan",
                 "Senarai 25 nabi dan rasul yang wajib diketahui, berapa kali setiap nama disebut dalam Al-Quran, dan kisah setiap nabi berdasarkan ayatnya.",
                 [("Kisah 25 Nabi", None)])
    hbody += f'''<div class="wrap mn"><div class="ct">
<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> 25 nabi dan rasul yang wajib diketahui ialah mereka yang <strong>disebut namanya dalam Al-Quran</strong>, bermula dengan <strong>Nabi Adam AS</strong> dan berakhir dengan <strong>Nabi Muhammad SAW</strong>, penutup sekalian nabi. Lima daripada mereka bergelar <strong>Ulul Azmi</strong>: Nuh, Ibrahim, Musa, Isa dan Muhammad SAW. Nabi yang paling banyak disebut ialah <strong>Nabi Musa AS ({musa["kali"]} kali)</strong>.</p></div>
{meta_line(T, TMS)}
{share(SITE + HUB, "25 nabi dan rasul dalam Al-Quran: senarai, kisah dan ayat:")}
</div>
</section>

<section id="senarai" aria-labelledby="h-sen">
<h2 id="h-sen">Senarai 25 Nabi dan Rasul</h2>
{table(["#", "Nabi", "Arab", "Diutus kepada", "Sebutan", "Surah"], rows, "Senarai 25 nabi dan rasul")}
<p class="note">⭐ Ulul Azmi. “Sebutan” = berapa kali nama itu disebut dalam Al-Quran, dikira terus daripada teks Uthmani dalam laman ini (bukan kata ganti atau gelaran). Tekan nama untuk kisah dan semua ayatnya.</p>
</section>

<section id="kiraan" aria-labelledby="h-kir">
<h2 id="h-kir">Nabi yang Paling Banyak Disebut dalam Al-Quran</h2>
<ol class="nbars">{bars}</ol>
<p class="note">Nabi Muhammad SAW disebut 4 kali dengan nama Muhammad dan sekali dengan nama Ahmad (As-Saff 61:6). Baginda lebih banyak diseru dengan gelaran seperti “wahai Nabi” dan “wahai Rasul”, yang tidak dikira di sini.</p>
</section>
{ad(0)}
<section class="dsec" id="ulul-azmi" aria-labelledby="h-ulul">
<h2 id="h-ulul">5 Rasul Ulul Azmi</h2>
<p>{", ".join(f'<a href="/{HUB}{n["slug"]}/">{e(NAMA(n))}</a>' for n in ulul)}.</p>
{card("ayat-46-35", "Al-Ahqaf 46:35: sabar seperti Ulul Azmi", u1[0], u1[1], u1[2], qref(46, 35))}
{card("ayat-33-7", "Al-Ahzab 33:7: perjanjian dengan lima rasul", u2[0], u2[1], u2[2], qref(33, 7))}
</section>

<section class="dsec" id="al-anam" aria-labelledby="h-anam">
<h2 id="h-anam">18 Nabi dalam Empat Ayat (Al-An'am 83–86)</h2>
{card("ayat-6-83", "Al-An'am 6:83–86", an[0], an[1], an[2], f'<a href="/#surah-6-ayat-83">Al-An\'am 6:83–86</a>')}
</section>

<section id="surah" aria-labelledby="h-surah">
<h2 id="h-surah">Surah yang Dinamakan Sempena Nabi</h2>
{table(["Surah", "No.", "Nabi"], srows, "Surah yang dinamakan sempena nabi")}
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: 25 Nabi dan Rasul</h2>
{faq_html(hfaq)}
<p class="note">Baca juga <a href="{NB.MAIN_ARTICLE}" rel="noopener">artikel penuh 25 Nabi dan Rasul dengan garis masa dan kuiz ↗</a>, <a href="/doa-harian/#nabi">doa para nabi</a> dan <a href="/cari-ayat-al-quran/">carian ayat Al-Quran</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(HUB)}</section>
</div>
{side([("senarai", "Senarai 25 nabi"), ("kiraan", "Paling banyak disebut"), ("ulul-azmi", "Ulul Azmi"), ("al-anam", "18 nabi dalam 4 ayat"), ("surah", "Surah nama nabi"), ("faq", "Soalan lazim")], HUB)}
</div>'''
    pages.insert(0, dict(path=HUB, kind="ref", data=False, arabic=True, published=PUB, schema="CollectionPage",
                         title="Kisah 25 Nabi dalam Al-Quran: Ayat, Mukjizat & Kiraan Sebutan", ogtitle="Kisah 25 Nabi dalam Al-Quran",
                         desc="Senarai 25 nabi dan rasul, berapa kali setiap nama disebut dalam Al-Quran (Musa 136 kali), 5 Ulul Azmi, dan kisah setiap nabi dengan ayatnya.",
                         crumbs=[("Kisah 25 Nabi", None)], body=hbody, faq=hfaq, about=["Nabi dan rasul", "Rukun iman", "Ulul Azmi"], og="kisah-nabi",
                         ogcard=("Kisah 25 Nabi dalam Al-Quran", "Kisah, mukjizat dan setiap ayat yang menyebut nama 25 nabi dan rasul."),
                         itemlist=dict(name="25 Nabi dan Rasul", items=[{"@type": "ListItem", "position": i, "name": NAMA(n), "url": f"{SITE}{HUB}{n['slug']}/"} for i, n in enumerate(N, 1)]),
                         llms="25 nabi dan rasul yang disebut dalam Al-Quran, dengan kiraan sebutan nama daripada teks Uthmani: " + ", ".join(f"{n['nama']} {n['kali']}" for n in rank) + ". Ulul Azmi: Nuh, Ibrahim, Musa, Isa, Muhammad SAW (46:35, 33:7, 42:13). 18 nabi dalam Al-An'am 83–86."))
    return pages
