"""Pages: /haji-umrah/ (hub) and 13 guide pages under it: cara umrah (with a tawaf & sa'ie counter), cara haji (day by day,
with this year's dates from the JAKIM Hijri calendar), niat ihram, talbiah, larangan ihram and rukun/wajib, jenis haji, dam
(with a checker), miqat, wanita haid, badal haji, ziarah Madinah and a packing checklist. Content and sources live in
tools/haji.py; the three widgets are assets/js/haji.js (every widget is pre-rendered, so the page is complete without JS).

Intent split: the monetised www.ilmualam.com already ranks for "doa tawaf & sa'ie" (7-round doa) and "solat jamak qasar
umrah", so these pages cover the rites and link there instead of duplicating it (WWW_*)."""
import json, datetime as dt
import haji as H
import hijri as HJ
import ibadah as I
import plans as P
from pages import e, faq_html, hero, side, meta_line, table, tool_cards, SITE
from pages2 import card
from pages7 import doa_cards
from pages16 import h_item

PUB = "2026-11-15"
HUB = H.HUB
JS = "/assets/js/haji.js"
WWW_TAWAF = "https://www.ilmualam.com/2026/09/doa-tawaf-saie.html"
WWW_JAMAK = "https://www.ilmualam.com/2026/10/solat-jamak-qasar-umrah.html"
TBB_TH = "https://tool.thebukitbesi.com/kalkulator-tabung-haji/"

# (slug, short name for crumbs/links, one-line description for the hub list)
GUIDES = [
    ("cara-umrah", "Cara Umrah", "8 langkah dari miqat hingga tahallul, dengan kaunter tawaf & sa'ie"),
    ("cara-haji", "Cara Haji", "Manasik haji hari demi hari, 8 hingga 13 Zulhijjah, dengan tarikh tahun ini"),
    ("niat-ihram", "Niat Ihram", "Lafaz niat umrah, haji, qiran dan isytirat, solat sunat ihram dan pakaian ihram"),
    ("talbiah", "Talbiah", "Lafaz talbiah Arab, Rumi dan maksud, bila mula dan berhenti"),
    ("larangan-ihram", "Larangan Ihram", "13 larangan ihram lelaki dan wanita dengan dam setiap satu"),
    ("rukun-haji", "Rukun & Wajib Haji", "Rukun haji, wajib haji, rukun umrah dan beza rukun dengan wajib"),
    ("jenis-haji", "Haji Ifrad, Tamattu' & Qiran", "Beza tiga cara mengerjakan haji, dam dan mana yang afdal"),
    ("dam-haji", "Dam Haji & Umrah", "4 jenis dam dan penyemak dam mengikut kesalahan"),
    ("miqat", "Miqat Haji & Umrah", "5 miqat, miqat bagi jemaah Malaysia dan miqat zamani"),
    ("umrah-wanita-haid", "Haji & Umrah Wanita Haid", "Ihram wanita, haid sebelum tawaf, tawaf wada' dan pil penangguh haid"),
    ("badal-haji", "Badal Haji & Umrah", "Hukum, syarat, niat dan siapa yang boleh dibadalkan"),
    ("ziarah-madinah", "Ziarah Madinah", "Masjid Nabawi, Raudhah, salam kepada Rasulullah SAW, Quba dan Baqi'"),
    ("senarai-barang-umrah", "Senarai Barang Umrah & Haji", "Senarai semak dokumen, ihram, ubat dan barang ibadah yang boleh ditanda"),
]
NAME = {s: n for s, n, _ in GUIDES}
ICON = dict(zip(NAME, "🕋 🐪 🤍 📣 🚫 📋 🔀 ⚖️ 📍 🌸 🤝 🕌 🧳".split()))


def url(slug):
    return HUB + slug + "/" if slug else HUB


def a(slug, text=None):
    return f'<a href="/{url(slug)}">{e(text or NAME[slug])}</a>'


def ul(*items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def ref(t):
    return f' <span class="nref">({e(t)})</span>'


def rows(pairs):
    return [[f"<strong>{e(x)}</strong>", e(y)] for x, y in pairs]


dlong = P.dlong


# ---------------- haji dates (this or next season), from the JAKIM Hijri column or the labelled estimate ----------------
def season(day):
    hy = HJ.g2h(day)[0]
    if HJ.h2g(hy, 12, 13)[0] < day:
        hy += 1
    days = [(d, *HJ.h2g(hy, 12, d)) for d in range(8, 14)]
    return hy, days, all(x[2] for x in days)


def dates_table(hy, days, official):
    names = {8: "Hari Tarwiyah", 9: "Hari Arafah (wukuf)", 10: "Aidiladha · melontar Jamrah Aqabah", 11: "Hari Tasyrik 1", 12: "Hari Tasyrik 2 · nafar awal", 13: "Hari Tasyrik 3 · nafar thani"}
    t = table(["Zulhijjah", "Tarikh (Malaysia)", "Amalan"], [[f"<strong>{d} Zulhijjah {hy}H</strong>", e(dlong(g)), e(names[d])] for d, g, _ in days], f"Tarikh haji {hy}H")
    src = ("daripada takwim Hijrah rasmi JAKIM" if official else "anggaran kalendar Hijrah (takwim rasmi JAKIM belum diterbitkan)")
    return t + (f'<p class="note">Tarikh {src}. Tarikh wukuf ditetapkan oleh kerajaan Arab Saudi dan boleh berbeza sehari dengan Malaysia. '
                f'Hari Arafah: <strong data-hu-days="{days[1][1].isoformat()}"></strong> · <a href="/kalendar-hijrah/">Kalendar Hijrah</a></p>')


# ---------------- widgets (assets/js/haji.js) ----------------
def counter_html():
    dots = "".join(f"<li>{i}</li>" for i in range(1, 8))
    return f'''<div class="tool hu-ctr" id="hu-ctr" data-mode="tawaf">
<h3 id="h-ctr">🔄 Kaunter Tawaf & Sa'ie</h3>
<div class="chips2" role="group" aria-label="Pilih ibadah"><button type="button" data-m="tawaf" aria-pressed="true">Tawaf</button><button type="button" data-m="saie" aria-pressed="false">Sa'ie</button></div>
<button class="hu-ctr__btn" type="button" id="hu-btn" aria-describedby="hu-hint"><span class="hu-ctr__n" id="hu-n">0</span><span class="hu-ctr__of">/ 7 pusingan</span></button>
<ol class="hu-ctr__dots" id="hu-dots" aria-hidden="true">{dots}</ol>
<p class="hu-ctr__hint" id="hu-hint" aria-live="polite">Mula di garisan Hajarul Aswad. Tekan butang setiap kali satu pusingan selesai.</p>
<div class="act"><button class="btn2" type="button" id="hu-undo">↶ Undur</button><button class="btn2" type="button" id="hu-reset">⟲ Mula semula</button></div>
<p class="note">Kiraan disimpan dalam pelayar ini sahaja dan bergetar pada setiap pusingan. Jika ragu-ragu bilangan pusingan, ambil bilangan yang lebih sedikit kerana itulah yang yakin.</p>
<noscript><p class="note">Kaunter memerlukan JavaScript.</p></noscript>
</div>'''


def dam_result(key):
    _, label, who, dk, detail = next(x for x in H.LARANGAN if x[0] == key)
    if not dk:
        return f'<div class="sum"><p><strong>Tiada dam</strong>, tetapi berdosa.</p><p>{e(detail)}</p></div>'
    name, how, _ = H.DAM[dk]
    return (f'<div class="sum"><p><strong>{e(name)}</strong> · {e(who)}</p><p>{e(how)}</p><p class="note">{e(detail)}</p>'
            f'<p class="note"><a href="/{url("dam-haji")}#{dk}">Penjelasan {e(name.lower())}</a></p></div>')


def dam_tool():
    opts = "".join(f'<option value="{k}">{e(lbl)}</option>' for k, lbl, *_ in H.LARANGAN)
    outs = "".join(f'<div data-k="{k}"{"" if i == 0 else " hidden"}>{dam_result(k)}</div>' for i, (k, *_) in enumerate(H.LARANGAN))
    return (f'<div class="tool hu-dam" id="hu-dam"><h3 id="h-dam">⚖️ Semak Dam Mengikut Kesalahan</h3>'
            f'<div class="fl"><label for="hu-dsel">Apa yang berlaku?</label><select id="hu-dsel">{opts}</select></div>'
            f'<div id="hu-dout" aria-live="polite">{outs}</div>'
            '<p class="note">Panduan umum mazhab Syafi\'i. Kesilapan kerana lupa atau jahil (selain bercukur, memotong kuku, memburu dan bersetubuh) tidak dikenakan dam; '
            'sahkan kes anda dengan pembimbing ibadah Tabung Haji atau mutawwif.</p></div>')


def checklist_html():
    n = sum(len(items) for _, items in H.CHECKLIST)
    groups = "".join(
        f'<h3>{e(g)}</h3><ul class="hu-chk">' + "".join(
            f'<li><label><input type="checkbox" data-k="{k}"> <span>{e(t)}</span>{f" <small>{e(nt)}</small>" if nt else ""}</label></li>' for k, t, nt in items) + "</ul>"
        for g, items in H.CHECKLIST)
    return (f'<div class="tool hu-list" id="hu-list"><p class="prog" id="hu-cprog" aria-live="polite">0 / {n} siap</p>{groups}'
            '<div class="act"><button class="btn2" type="button" id="hu-creset">⟲ Kosongkan tanda</button><button class="btn2" type="button" id="hu-cprint">🖨 Cetak senarai</button></div>'
            '<p class="note">Tanda disimpan dalam pelayar ini sahaja.</p></div>')


def howto(page_url, name, steps):
    return {"@type": "HowTo", "@id": page_url + "#howto", "name": name, "inLanguage": "ms-MY",
            "step": [{"@type": "HowToStep", "position": i, "name": n, "text": t, "url": f"{page_url}#{sid}"} for i, (sid, n, t) in enumerate(steps, 1)]}


# ---------------- page content ----------------
def content(day):
    hy, days, official = season(day)
    arafah = days[1][1]
    pages = []

    # cara umrah
    steps_html = "".join(f'<li id="{sid}"><strong>{e(n)}.</strong> {e(t)}</li>' for sid, n, t in H.UMRAH_STEPS)
    pages.append(("cara-umrah", dict(
        h1="Cara Umrah Lengkap: 8 Langkah dari Miqat hingga Tahallul",
        title="Cara Umrah Lengkap: Langkah demi Langkah, Niat & Doa",
        desc="Cara buat umrah langkah demi langkah: ihram di miqat, niat, talbiah, tawaf 7 pusingan, solat sunat tawaf, sa'ie dan tahallul, dengan kaunter tawaf & sa'ie.",
        lead="Panduan umrah mengikut mazhab Syafi'i: lima rukun, dua wajib, lapan langkah, doa utama dengan sumber, dan kaunter pusingan untuk dibawa ke Masjidil Haram.",
        box="Umrah ada <strong>5 rukun</strong>: <strong>niat ihram, tawaf, sa'ie, bercukur atau bergunting, dan tertib</strong>, serta 2 wajib: berihram dari miqat dan menjauhi larangan ihram. "
            "Ringkasnya: niat ihram di miqat → talbiah → tawaf 7 pusingan → solat sunat tawaf → sa'ie 7 kali dari Safa ke Marwah → bercukur/bergunting. Umrah biasa selesai dalam 3 hingga 5 jam.",
        sections=[("langkah", "8 Langkah Umrah", f'<ol class="steps">{steps_html}</ol>'),
                  ("kaunter", "Kaunter Tawaf & Sa'ie", counter_html()),
                  ("doa", "Doa dan Bacaan Utama Umrah", doa_cards([H.NIAT["umrah"], H.TALBIAH] + H.TAWAF + H.SAIE) +
                   f'<p class="note">Doa lengkap bagi setiap pusingan tawaf dan sa\'ie: <a href="{WWW_TAWAF}">Doa Tawaf & Sa\'ie 7 Pusingan</a>. Tiada doa khusus yang wajib; berdoalah dengan bahasa sendiri.</p>'),
                  ("syarat", "Syarat Sah Tawaf dan Sa'ie", table(["Tawaf", "Sa'ie"], [
                      ["Suci daripada hadas kecil, hadas besar dan najis", "Dilakukan selepas tawaf yang sah"],
                      ["Menutup aurat", "Bermula di Safa dan berakhir di Marwah"],
                      ["Kaabah di sebelah kiri, bermula dari Hajarul Aswad", "Cukup 7 kali (Safa ke Marwah dikira satu)"],
                      ["Tujuh pusingan dengan yakin, di dalam masjid dan di luar Hijir Ismail", "Melalui keseluruhan jarak antara kedua-dua bukit"]], "Syarat tawaf dan sa'ie") +
                   f'<p class="note">Jika wuduk terbatal ketika tawaf, berwuduk semula dan sambung dari tempat terhenti (pendapat muktamad mazhab Syafi\'i). Solat jamak dan qasar ketika umrah: <a href="{WWW_JAMAK}">hukum dan cara</a>.</p>'),
                  ("rukun", "Rukun dan Wajib Umrah", table(["Rukun umrah", "Keterangan"], rows(H.RUKUN_UMRAH), "Rukun umrah") +
                   table(["Wajib umrah", "Jika ditinggalkan"], rows(H.WAJIB_UMRAH), "Wajib umrah") +
                   f'<p class="note">Rukun yang ditinggalkan menjadikan umrah tidak sah dan tidak boleh diganti dengan dam. Lihat {a("larangan-ihram")} dan {a("dam-haji")}.</p>')],
        faq=[("Apakah rukun umrah?", "Lima: niat ihram, tawaf, sa'ie, bercukur atau bergunting, dan tertib. Wajib umrah pula dua: berihram dari miqat dan menjauhi larangan ihram."),
             ("Berapa lama masa untuk melakukan umrah?", "Kira-kira 3 hingga 5 jam bergantung pada kesesakan: tawaf 45 minit hingga 1.5 jam, sa'ie sekitar 1 jam (kira-kira 3.2 km), selebihnya solat, rehat dan tahallul."),
             ("Adakah wajib berwuduk ketika sa'ie?", "Tidak wajib, tetapi sunat. Wuduk wajib bagi tawaf sahaja."),
             ("Bolehkah melakukan umrah berkali-kali dalam satu perjalanan?", "Boleh menurut mazhab Syafi'i: keluar ke tanah halal (contohnya Tan'im atau Ji'ranah), berniat ihram dan ulang tawaf, sa'ie dan tahallul. Rasulullah SAW menyuruh Aisyah berumrah dari Tan'im (HR Al-Bukhari, no. 1784)."),
             ("Apakah yang perlu dilakukan jika terlupa bilangan pusingan tawaf?", "Ambil bilangan yang lebih sedikit kerana itu yang yakin, dan sempurnakan baki pusingan. Kaunter di atas membantu mengelakkan keraguan.")],
        about=["Umrah", "Cara umrah", "Tawaf", "Sa'ie"],
        nodes=lambda u: [howto(u, "Cara melakukan umrah", H.UMRAH_STEPS)], js=True,
        llms="Cara umrah (mazhab Syafi'i): 5 rukun (niat ihram, tawaf, sa'ie, bercukur, tertib), 2 wajib, 8 langkah, doa tawaf (HR Abu Daud 1892) dan sa'ie (HR Muslim 1218), syarat sah tawaf/sa'ie, kaunter pusingan tawaf & sa'ie.")))

    # cara haji
    G = {d: g for d, g, _ in days}
    WHEN = {1: [8], 2: [9], 3: [9], 4: [10], 5: [11, 12], 6: [13]}  # row index in HAJI_DAYS -> Zulhijjah days it covers (row 3 is the night after Arafah)
    day_rows = []
    for i, (d, n, t, hk) in enumerate(H.HAJI_DAYS):
        when = " – ".join(dlong(G[x]) for x in WHEN.get(i, []))
        if i == 3:
            when = "malam selepas " + when
        day_rows.append([f"<strong>{e(n)}</strong>" + (f"<br><small>{e(when)}</small>" if when else ""), e(t), e(hk)])
    hsteps = [(f"h{i}", n, t) for i, (d, n, t, hk) in enumerate(H.HAJI_DAYS)]
    pages.append(("cara-haji", dict(
        h1=f"Cara Haji Lengkap: Manasik Hari demi Hari ({hy}H)",
        title="Cara Haji Lengkap: Manasik 8–13 Zulhijjah Hari demi Hari",
        desc=f"Cara mengerjakan haji hari demi hari: ihram 8 Zulhijjah, wukuf Arafah, Muzdalifah, melontar jamrah, tawaf ifadah dan tawaf wada', dengan tarikh haji {hy}H.",
        lead="Manasik haji mengikut mazhab Syafi'i dari Hari Tarwiyah hingga tawaf wada', dengan hukum setiap amalan dan tarikh musim haji akan datang.",
        box=f"Haji berlangsung dari <strong>8 hingga 13 Zulhijjah</strong>. Kemuncaknya <strong>wukuf di Arafah pada 9 Zulhijjah</strong> (dijangka {e(dlong(arafah))}), "
            "diikuti bermalam di Muzdalifah, melontar Jamrah Aqabah, bercukur dan tawaf ifadah pada 10 Zulhijjah, serta melontar tiga jamrah dan bermalam di Mina pada hari tasyrik. "
            "“Haji itu Arafah” (HR At-Tirmizi, no. 889): sesiapa terlepas wukuf, terlepas hajinya.",
        sections=[("tarikh", f"Tarikh Haji {hy}H", dates_table(hy, days, official)),
                  ("hari", "Manasik Haji Hari demi Hari", table(["Hari", "Amalan", "Hukum"], day_rows, "Manasik haji hari demi hari") +
                   f'<p class="note">Jadual sebenar mengikut taklimat Tabung Haji atau agensi. Lihat juga {a("jenis-haji")} dan {a("rukun-haji")}.</p>'),
                  ("doa", "Doa dan Zikir Utama Musim Haji", doa_cards([H.NIAT["haji"], H.TALBIAH, H.ARAFAH, ("muzdalifah", "Zikir di Masy'aril Haram (Muzdalifah)", "Q:2:198", "", "", "", "Selepas Subuh 10 Zulhijjah, berzikir dan berdoa menghadap kiblat hingga langit cerah (HR Muslim, no. 1218)."), H.MELONTAR])),
                  ("tahallul", "Tahallul Awal dan Tahallul Thani", table(["", "Syarat", "Yang menjadi halal"], [
                      ["<strong>Tahallul awal</strong>", "Dua daripada tiga: melontar Jamrah Aqabah, bercukur/bergunting, tawaf ifadah (bersama sa'ie jika belum)", "Semua larangan ihram kecuali bersetubuh, bercumbu dan akad nikah"],
                      ["<strong>Tahallul thani</strong>", "Ketiga-tiganya selesai", "Semua larangan ihram"]], "Tahallul awal dan thani"))],
        faq=[("Bilakah haji bermula?", f"Amalan haji bermula pada 8 Zulhijjah dan berakhir pada 12 atau 13 Zulhijjah. Bagi {hy}H, Hari Arafah dijangka pada {dlong(arafah)} mengikut takwim Malaysia; tarikh wukuf ditetapkan oleh Arab Saudi."),
             ("Apakah rukun haji yang paling penting?", "Wukuf di Arafah. Rasulullah SAW bersabda “Haji itu Arafah” (HR At-Tirmizi, no. 889). Rukun lain boleh dilakukan kemudian, tetapi wukuf terikat dengan masanya."),
             ("Apakah beza nafar awal dan nafar thani?", "Nafar awal: meninggalkan Mina pada 12 Zulhijjah sebelum matahari terbenam selepas melontar. Nafar thani: bermalam lagi dan melontar pada 13 Zulhijjah. Kedua-duanya sah (Al-Baqarah 2:203)."),
             ("Berapa biji batu diperlukan untuk melontar?", "49 biji bagi nafar awal (7 pada 10 Zulhijjah + 21 pada 11 dan 12 Zulhijjah) atau 70 biji bagi nafar thani. Ambil sedikit lebih sebagai simpanan."),
             ("Bolehkah mewakilkan lontaran?", "Boleh bagi yang uzur (sakit, warga emas, wanita hamil): wakil melontar untuk dirinya dahulu, kemudian untuk orang yang diwakilkan pada jamrah yang sama.")],
        about=["Haji", "Cara haji", "Wukuf Arafah", "Melontar jamrah"],
        nodes=lambda u: [howto(u, "Cara mengerjakan haji", hsteps)], js=True,
        llms=f"Cara haji hari demi hari (8–13 Zulhijjah) mazhab Syafi'i: ihram, wukuf Arafah (HR At-Tirmizi 889), Muzdalifah, melontar (HR Al-Bukhari 1751), tawaf ifadah, tahallul awal/thani, nafar awal/thani, tawaf wada'; tarikh haji {hy}H daripada takwim JAKIM.")))

    # niat ihram
    pages.append(("niat-ihram", dict(
        h1="Niat Ihram Umrah & Haji: Lafaz Rumi, Arab dan Maksud",
        title="Niat Ihram Umrah & Haji: Lafaz Rumi, Arab & Maksud",
        desc="Lafaz niat ihram umrah, haji ifrad/tamattu', haji qiran dan niat bersyarat (isytirat) dalam tulisan Arab, Rumi dan maksud, serta sunat ihram dan pakaian ihram.",
        lead="Lafaz niat ihram yang diajar dalam kursus haji di Malaysia, solat sunat ihram, sunat sebelum berihram dan pakaian ihram lelaki dan wanita.",
        box="Niat ihram umrah: <strong>“Nawaitul-'umrata wa ahramtu biha lillahi ta'ala”</strong>. Niat ihram haji: <strong>“Nawaitul-hajja wa ahramtu bihi lillahi ta'ala”</strong>. "
            "Niat ialah rukun di dalam hati dan mesti dibuat <strong>sebelum melintasi miqat</strong>; melafazkannya sunat. Selepas niat, terus membaca talbiah.",
        sections=[("lafaz", "Lafaz Niat Ihram", doa_cards([H.NIAT["umrah"], H.NIAT["haji"], H.NIAT["qiran"], H.NIAT["isytirat"]])),
                  ("sunat", "Sunat Sebelum Berihram", doa_cards([H.NIAT_SOLAT_IHRAM]) + ul(
                      "Memotong kuku, mencukur bulu ketiak dan bulu ari, serta merapikan misai.",
                      "Mandi sunat ihram, termasuk wanita haid dan nifas." + ref("HR Muslim, no. 1209 (Asma' binti Umais)"),
                      "Memakai wangian pada badan sebelum niat, bukan pada kain ihram." + ref("HR Al-Bukhari, no. 1539"),
                      "Solat sunat ihram dua rakaat, kemudian berniat dan bertalbiah.")),
                  ("pakaian", "Pakaian Ihram Lelaki dan Wanita", table(["", "Lelaki", "Wanita"], [
                      ["Pakaian", "Dua helai kain tidak berjahit: izar (bawah) dan rida' (atas), sebaik-baiknya putih", "Pakaian biasa yang menutup aurat; tidak wajib putih"],
                      ["Kepala", "Terbuka", "Bertudung"],
                      ["Muka dan tapak tangan", "Boleh ditutup kecuali kepala", "Tidak boleh menutup muka atau memakai sarung tangan" + ref("HR Al-Bukhari, no. 1838")],
                      ["Kaki", "Selipar yang menampakkan buku lali dan belakang kaki", "Boleh berkasut dan berstokin"]], "Pakaian ihram") +
                   f'<p class="note">Selepas niat, semua {a("larangan-ihram")} berkuat kuasa. Miqat bagi jemaah Malaysia: {a("miqat")}.</p>')],
        faq=[("Bilakah niat ihram umrah dibuat?", "Sebelum melintasi miqat. Bagi penerbangan terus ke Jeddah, niat dibuat dalam pesawat apabila anak kapal mengumumkan hampir dengan miqat; pakai ihram sebelum berlepas atau dalam pesawat."),
             ("Adakah niat ihram perlu dilafazkan?", "Niat di dalam hati sudah memadai dan menjadi rukun. Melafazkannya sunat dalam mazhab Syafi'i untuk membantu hati, diikuti talbiah."),
             ("Bagaimana jika terlintas miqat tanpa niat ihram?", "Wajib kembali ke miqat untuk berniat jika mampu sebelum memulakan tawaf; jika tidak kembali, ihramnya sah tetapi wajib dam seekor kambing."),
             ("Bolehkah memakai jam tangan atau tali pinggang semasa ihram?", "Boleh. Larangan bagi lelaki ialah pakaian yang dijahit mengikut bentuk badan seperti baju dan seluar, bukan semua benda yang ada jahitan.")],
        about=["Niat ihram", "Ihram", "Umrah", "Haji"],
        llms="Niat ihram umrah (Nawaitul-'umrata wa ahramtu biha lillahi ta'ala), haji, qiran (asal HR Muslim 1251), isytirat (HR Al-Bukhari 5089; Muslim 1207), solat sunat ihram, sunat sebelum ihram, pakaian ihram lelaki dan wanita (HR Al-Bukhari 1838).")))

    # talbiah
    pages.append(("talbiah", dict(
        h1="Talbiah: Bacaan Labbaikallahumma Labbaik (Rumi, Arab & Maksud)",
        title="Talbiah Haji & Umrah: Rumi, Arab, Maksud & Bila Dibaca",
        desc="Bacaan talbiah Labbaikallahumma labbaik dalam tulisan Arab, Rumi dan maksud, bila mula dan berhenti bertalbiah ketika umrah dan haji, serta hukumnya.",
        lead="Talbiah ialah seruan jemaah yang berihram menyahut panggilan Allah, dengan lafaz yang dibaca Rasulullah SAW sendiri.",
        box="Talbiah: <strong>“Labbaikallahumma labbaik, labbaika la syarika laka labbaik, innal-hamda wan-ni'mata laka wal-mulk, la syarika lak”</strong> (HR Al-Bukhari, no. 1549; Muslim, no. 1184). "
            "Ia <strong>sunat muakkad</strong> dibaca selepas niat ihram hingga <strong>memulakan tawaf</strong> (umrah) atau hingga <strong>mula melontar Jamrah Aqabah</strong> pada 10 Zulhijjah (haji).",
        sections=[("bacaan", "Bacaan Talbiah", doa_cards([H.TALBIAH, H.TALBIAH_DOA])),
                  ("bila", "Bila Mula dan Berhenti Bertalbiah", table(["Ibadah", "Mula", "Berhenti"], [
                      ["Umrah", "Sejurus selepas niat ihram di miqat", "Apabila memulakan tawaf umrah"],
                      ["Haji", "Sejurus selepas niat ihram haji", "Apabila mula melontar Jamrah Aqabah pada 10 Zulhijjah" + ref("HR Al-Bukhari, no. 1685")]], "Waktu talbiah") +
                   ul("Diulang-ulang terutama ketika naik dan turun bukit, bertemu jemaah lain, selepas solat dan pada waktu pagi dan petang.",
                      "Lelaki menguatkan suara; Jibril menyuruh Rasulullah SAW memerintahkan para sahabat meninggikan suara talbiah." + ref("HR Abu Daud, no. 1814; At-Tirmizi, no. 829"),
                      "Wanita membaca dengan suara perlahan yang didengar dirinya.", "Wanita haid dan nifas boleh bertalbiah.")),
                  ("makna", "Makna Talbiah", "<p>“Labbaik” bermaksud “aku menyahut dan aku tetap dalam ketaatan kepada-Mu”. Talbiah menyahut seruan Nabi Ibrahim AS yang diperintah menyeru manusia kepada haji:</p>" +
                   doa_cards([("ayat-22-27", "Al-Hajj 27: seruan haji Nabi Ibrahim", "Q:22:27", "", "", "", "")]))],
        faq=[("Apakah lafaz talbiah yang sahih?", "Labbaikallahumma labbaik, labbaika la syarika laka labbaik, innal-hamda wan-ni'mata laka wal-mulk, la syarika lak (HR Al-Bukhari, no. 1549; Muslim, no. 1184)."),
             ("Apakah hukum talbiah?", "Sunat muakkad dalam mazhab Syafi'i. Ihram tetap sah tanpanya, tetapi meninggalkannya bererti meninggalkan syiar haji dan umrah."),
             ("Bilakah berhenti talbiah ketika umrah?", "Apabila memulakan tawaf umrah (ketika istilam Hajarul Aswad pusingan pertama)."),
             ("Bolehkah wanita membaca talbiah dengan kuat?", "Tidak digalakkan. Wanita membaca perlahan, cukup didengari dirinya sendiri.")],
        about=["Talbiah", "Ihram", "Haji", "Umrah"],
        llms="Talbiah: Labbaikallahumma labbaik... (HR Al-Bukhari 1549; Muslim 1184), sunat muakkad, mula selepas niat ihram, berhenti ketika mula tawaf (umrah) atau melontar Jamrah Aqabah (haji, HR Al-Bukhari 1685); lelaki kuat (HR Abu Daud 1814), wanita perlahan.")))

    # larangan ihram
    lrows = [[e(lbl), e(who), (f'<a href="/{url("dam-haji")}#{dk}">{e(H.DAM[dk][0])}</a>' if dk else "Tiada dam (berdosa, akad tidak sah)"), e(det)] for k, lbl, who, dk, det in H.LARANGAN if k not in ("tamattu", "miqat", "wajib")]
    pages.append(("larangan-ihram", dict(
        h1="Larangan Ihram Lelaki dan Wanita (dengan Dam Setiap Satu)",
        title="Larangan Ihram Haji & Umrah: Senarai Penuh dan Dam",
        desc="Senarai larangan ihram lelaki dan wanita ketika umrah dan haji: pakaian, wangian, rambut, kuku, buruan, nikah dan jimak, dengan dam setiap satu.",
        lead="Perkara yang haram dilakukan selepas berniat ihram hingga tahallul, dengan jenis dam bagi setiap kesalahan dan penyemak dam.",
        box="Selepas berniat ihram, haram: <strong>lelaki</strong> memakai pakaian berjahit dan menutup kepala; <strong>wanita</strong> menutup muka dan memakai sarung tangan; "
            "dan <strong>kedua-duanya</strong> memakai wangian, meminyakkan rambut, memotong rambut atau kuku, memburu, bernikah, bercumbu dan bersetubuh. "
            "Kebanyakannya dikenakan <strong>dam takhyir</strong>: seekor kambing, atau sedekah 3 gantang makanan kepada 6 miskin, atau puasa 3 hari.",
        sections=[("senarai", "Senarai Larangan Ihram", table(["Larangan", "Bagi", "Dam", "Catatan"], lrows, "Larangan ihram")),
                  ("semak", "Penyemak Dam", dam_tool()),
                  ("boleh", "Perkara yang Dibolehkan Ketika Ihram", ul("Mandi, menukar kain ihram dan mencuci kepala dengan perlahan (tanpa sabun berwangi).",
                      "Berteduh di bawah payung, khemah atau bumbung kenderaan.", "Memakai jam tangan, cermin mata, tali pinggang, cincin dan beg.",
                      "Berbekam atau mendapat rawatan, menggaru dengan perlahan.", "Membunuh binatang perosak yang berbahaya." + ref("HR Al-Bukhari, no. 1829")))],
        faq=[("Bolehkah memakai sabun ketika ihram?", "Tidak boleh memakai sabun, syampu atau losyen yang berwangi. Gunakan sabun tanpa pewangi."),
             ("Apakah hukum jika rambut gugur ketika mandi atau berwuduk?", "Tiada dam jika gugur tanpa sengaja. Dam dikenakan jika dipotong atau dicabut dengan sengaja."),
             ("Adakah terlupa atau tidak tahu menghapuskan dam?", "Bagi larangan yang bersifat bersenang-senang (pakaian, wangian, minyak), tiada dam jika lupa atau jahil. Bagi larangan yang bersifat merosakkan (bercukur, memotong kuku, memburu) dam tetap wajib."),
             ("Bolehkah wanita berihram memakai purdah?", "Tidak. Wanita berihram dilarang menutup muka dengan niqab dan memakai sarung tangan (HR Al-Bukhari, no. 1838), tetapi boleh melabuhkan kain dari atas kepala jika ada lelaki ajnabi, tanpa melekat pada muka.")],
        about=["Larangan ihram", "Ihram", "Dam"], js=True,
        llms="Larangan ihram (mazhab Syafi'i): pakaian berjahit dan menutup kepala (lelaki), menutup muka dan sarung tangan (wanita, HR Al-Bukhari 1838), wangian, minyak rambut, rambut, kuku, buruan (Al-Ma'idah 95), pokok Tanah Haram, nikah (HR Muslim 1409), cumbu, jimak; dam bagi setiap satu dan penyemak dam.")))

    # rukun & wajib
    pages.append(("rukun-haji", dict(
        h1="Rukun Haji, Wajib Haji dan Rukun Umrah (Beserta Beza)",
        title="Rukun Haji, Wajib Haji & Rukun Umrah: Senarai dan Beza",
        desc="Senarai 6 rukun haji, 7 wajib haji, 5 rukun umrah dan 2 wajib umrah mengikut mazhab Syafi'i, beza rukun dengan wajib, syarat wajib haji dan perkara sunat haji.",
        lead="Rukun, wajib dan sunat haji dan umrah dalam mazhab Syafi'i, serta akibat jika setiap satu ditinggalkan.",
        box="Rukun haji ada <strong>6</strong>: <strong>niat ihram, wukuf di Arafah, tawaf ifadah, sa'ie, bercukur atau bergunting, dan tertib</strong>. "
            "Rukun umrah ada <strong>5</strong> (sama tetapi tanpa wukuf). <strong>Rukun</strong> yang ditinggalkan menjadikan ibadah tidak sah dan tidak boleh diganti dengan dam; "
            "<strong>wajib</strong> yang ditinggalkan tidak membatalkan haji tetapi wajib dibayar dam.",
        sections=[("rukun-haji", "6 Rukun Haji", table(["Rukun", "Keterangan"], rows(H.RUKUN_HAJI), "Rukun haji")),
                  ("wajib-haji", "Wajib Haji", table(["Wajib", "Jika ditinggalkan"], rows(H.WAJIB_HAJI), "Wajib haji")),
                  ("rukun-umrah", "5 Rukun Umrah dan 2 Wajib Umrah", table(["Rukun umrah", "Keterangan"], rows(H.RUKUN_UMRAH), "Rukun umrah") + table(["Wajib umrah", "Jika ditinggalkan"], rows(H.WAJIB_UMRAH), "Wajib umrah")),
                  ("beza", "Beza Rukun, Wajib dan Sunat", table(["", "Jika ditinggalkan", "Contoh"], [
                      ["<strong>Rukun</strong>", "Haji/umrah tidak sah; mesti dilakukan, tidak boleh diganti dam", "Wukuf, tawaf ifadah, sa'ie"],
                      ["<strong>Wajib</strong>", "Haji sah tetapi berdosa jika sengaja, dan wajib dam", "Bermalam di Muzdalifah, melontar, tawaf wada'"],
                      ["<strong>Sunat</strong>", "Tiada dosa dan tiada dam, cuma terlepas pahala", "Tawaf qudum, talbiah, solat sunat ihram, bermalam di Mina malam 9"]], "Beza rukun, wajib dan sunat")),
                  ("syarat", "Syarat Wajib Haji", table(["Syarat", "Keterangan"], rows(H.SYARAT_WAJIB), "Syarat wajib haji"))],
        faq=[("Berapakah rukun haji?", "Enam dalam mazhab Syafi'i: niat ihram, wukuf di Arafah, tawaf ifadah, sa'ie, bercukur atau bergunting, dan tertib."),
             ("Apakah beza rukun haji dan rukun umrah?", "Rukun umrah sama dengan rukun haji kecuali wukuf di Arafah. Umrah ada 5 rukun, haji ada 6."),
             ("Adakah tawaf wada' rukun haji?", "Bukan. Ia wajib dalam mazhab Syafi'i; jika ditinggalkan, haji sah tetapi wajib dam seekor kambing. Wanita haid dan nifas dikecualikan (HR Al-Bukhari, no. 1755)."),
             ("Apakah yang berlaku jika terlepas wukuf di Arafah?", "Hajinya terlepas. Dia bertahallul dengan amalan umrah (tawaf, sa'ie dan bercukur), wajib mengqada haji pada tahun berikutnya dan membayar dam.")],
        about=["Rukun haji", "Wajib haji", "Rukun umrah"],
        llms="Rukun haji (6): niat ihram, wukuf Arafah, tawaf ifadah, sa'ie, bercukur, tertib. Wajib haji: ihram dari miqat, mabit Muzdalifah dan Mina, melontar, tawaf wada', jauhi larangan ihram. Rukun umrah (5), wajib umrah (2); beza rukun/wajib/sunat; syarat wajib haji.")))

    # jenis haji
    pages.append(("jenis-haji", dict(
        h1="Haji Ifrad, Tamattu' dan Qiran: Beza, Cara dan Dam",
        title="Haji Ifrad, Tamattu' & Qiran: Beza, Cara, Dam dan Afdal",
        desc="Beza haji ifrad, tamattu' dan qiran: cara niat, bila umrah dilakukan, siapa wajib dam dan mana yang afdal mengikut mazhab Syafi'i, dalam satu jadual.",
        lead="Tiga cara menggabungkan haji dan umrah, yang ketiga-tiganya dilakukan oleh para sahabat dalam haji wada' bersama Rasulullah SAW.",
        box="<strong>Ifrad</strong>: haji dahulu, umrah selepasnya, tiada dam. <strong>Tamattu'</strong>: umrah dahulu dalam bulan haji, bertahallul, kemudian ihram haji pada 8 Zulhijjah; wajib dam. "
            "<strong>Qiran</strong>: berniat haji dan umrah serentak; wajib dam. Dalam mazhab Syafi'i yang <strong>paling afdal ialah ifrad</strong> (jika umrah dilakukan pada tahun yang sama), kemudian tamattu', kemudian qiran.",
        sections=[("beza", "Perbandingan Ifrad, Tamattu' dan Qiran", table(["", "Ifrad", "Tamattu'", "Qiran"], [
                      ["Niat", "Haji sahaja dari miqat", "Umrah dari miqat; haji dari Makkah pada 8 Zulhijjah", "Haji dan umrah serentak dari miqat"],
                      ["Umrah", "Selepas selesai haji, dari tanah halal", "Sebelum haji, dalam bulan haji", "Termasuk dalam amalan haji"],
                      ["Tempoh berihram", "Panjang (dari tiba hingga tahallul haji)", "Singkat: bebas antara umrah dan 8 Zulhijjah", "Panjang"],
                      ["Dam", "Tiada", "Wajib: seekor kambing atau puasa 10 hari", "Wajib: sama seperti tamattu'"],
                      ["Keutamaan (Syafi'i)", "Paling afdal", "Kedua", "Ketiga"]], "Beza jenis haji")),
                  ("dalil", "Dalil", doa_cards([("ayat-2-196", "Al-Baqarah 196: haji tamattu' dan damnya", "Q:2:196", "", "", "", "")]) +
                   "<p>Aisyah RA berkata: “Antara kami ada yang berihram untuk umrah, ada yang untuk haji dan umrah, dan ada yang untuk haji sahaja.”" + ref("HR Al-Bukhari, no. 1562; Muslim, no. 1211") + "</p>"),
                  ("syarat", "Syarat Dam Tamattu'", ul("Bukan penduduk Tanah Haram (atau dalam jarak 2 marhalah darinya).", "Umrah dilakukan dalam bulan haji (Syawal hingga Zulhijjah).",
                      "Haji dilakukan pada tahun yang sama.", "Tidak kembali ke miqat untuk berniat ihram haji.") +
                   f'<p class="note">Cara membayar dam: {a("dam-haji")}. Jenis haji jemaah Malaysia ditetapkan dalam kursus dan taklimat Tabung Haji.</p>')],
        faq=[("Jenis haji manakah yang paling afdal?", "Dalam mazhab Syafi'i: ifrad (dengan syarat umrah dilakukan pada tahun yang sama), kemudian tamattu', kemudian qiran. Mazhab Hanbali mengutamakan tamattu'."),
             ("Kenapa ramai jemaah memilih haji tamattu'?", "Kerana tempoh berihram lebih singkat: selepas umrah, jemaah bebas daripada larangan ihram sehingga 8 Zulhijjah. Ini memudahkan jemaah yang tiba awal."),
             ("Apakah dam haji tamattu'?", "Seekor kambing. Jika tidak mampu, berpuasa 10 hari: 3 hari semasa haji dan 7 hari selepas pulang (Al-Baqarah 2:196)."),
             ("Bolehkah menukar haji ifrad kepada tamattu'?", "Isu ini ada perbezaan pendapat ulama. Ikut ketetapan pembimbing ibadah Tabung Haji yang mengetahui keadaan rombongan anda.")],
        about=["Haji ifrad", "Haji tamattu'", "Haji qiran"],
        llms="Haji ifrad (afdal dalam mazhab Syafi'i, tiada dam), tamattu' (umrah dahulu dalam bulan haji, dam kambing atau puasa 10 hari, Al-Baqarah 2:196) dan qiran (serentak, dam); syarat dam tamattu'; dalil HR Al-Bukhari 1562.")))

    # dam
    dam_secs = "".join(f'<section class="dsec" id="{k}" aria-labelledby="h-{k}"><h3 id="h-{k}">{i}. {e(n)}</h3><p><strong>Cara membayar:</strong> {e(how)}</p><p><strong>Dikenakan kerana:</strong> {e(why)}</p></section>'
                       for i, (k, (n, how, why)) in enumerate(H.DAM.items(), 1))
    pages.append(("dam-haji", dict(
        h1="Dam Haji & Umrah: 4 Jenis Dam dan Penyemak Dam",
        title="Dam Haji & Umrah: 4 Jenis Dam, Cara Bayar & Penyemak",
        desc="4 jenis dam haji dan umrah mazhab Syafi'i (tartib taqdir, takhyir taqdir, tartib ta'dil, takhyir ta'dil), cara membayarnya dan penyemak dam ikut kesalahan.",
        lead="Dam ialah denda atau tebusan dalam haji dan umrah. Kenal pasti jenis dam bagi setiap kesalahan, pilihan pembayaran dan di mana ia dibayar.",
        box="Dam terbahagi kepada <strong>4 jenis</strong>: <strong>tartib dan taqdir</strong> (tamattu', qiran, meninggalkan wajib haji: kambing atau puasa 10 hari), "
            "<strong>takhyir dan taqdir</strong> (kebanyakan larangan ihram: kambing, sedekah 3 gantang kepada 6 miskin, atau puasa 3 hari), "
            "<strong>tartib dan ta'dil</strong> (jimak sebelum tahallul awal: unta) dan <strong>takhyir dan ta'dil</strong> (memburu, memotong pokok Tanah Haram). "
            "Sembelihan dan sedekah dam diagihkan kepada fakir miskin <strong>Tanah Haram</strong>.",
        sections=[("semak", "Penyemak Dam", dam_tool()),
                  ("jenis", "4 Jenis Dam", dam_secs),
                  ("istilah", "Maksud Istilah", table(["Istilah", "Maksud"], [
                      ["<strong>Tartib</strong>", "Mesti mengikut susunan: hanya boleh beralih ke pilihan seterusnya jika tidak mampu yang pertama"],
                      ["<strong>Takhyir</strong>", "Boleh memilih mana-mana pilihan walaupun mampu yang pertama"],
                      ["<strong>Taqdir</strong>", "Kadar gantinya telah ditetapkan syarak (contohnya 3 hari puasa)"],
                      ["<strong>Ta'dil</strong>", "Gantinya dinilai mengikut harga semasa (makanan senilai binatang)"]], "Istilah dam")),
                  ("bayar", "Cara dan Tempat Membayar Dam", ul("Sembelihan dan sedekah makanan mesti diagihkan kepada fakir miskin di Tanah Haram Makkah.",
                      "Puasa boleh dilakukan di mana-mana, termasuk di tanah air (7 hari bagi dam tamattu').",
                      "Jemaah haji Malaysia lazimnya membayar dam melalui Tabung Haji atau saluran rasmi yang diiktiraf di Makkah. Elakkan pihak yang tidak dikenali.",
                      f"1 cupak (mud) ≈ {H.MUD_KG} kg makanan asasi; 1 gantang (sa') = 4 cupak ≈ {4 * H.MUD_KG:.1f} kg, sama seperti sukatan <a href=\"/zakat-fitrah/\">zakat fitrah</a>."))],
        faq=[("Apakah dam haji tamattu'?", "Dam tartib dan taqdir: seekor kambing; jika tidak mampu, puasa 3 hari semasa haji dan 7 hari selepas pulang."),
             ("Berapakah dam jika memotong rambut ketika ihram?", "Tiga helai atau lebih: dam takhyir (seekor kambing, atau sedekah 3 gantang kepada 6 miskin, atau puasa 3 hari). Satu helai: secupak makanan; dua helai: dua cupak."),
             ("Bolehkah dam dibayar di Malaysia?", "Sembelihan dan sedekah makanan dam mesti diagihkan di Tanah Haram. Hanya puasa yang boleh dilakukan di tanah air."),
             ("Adakah dam sama dengan korban?", "Tidak. Dam ialah tebusan yang wajib kerana nusuk (tamattu'/qiran) atau kesalahan; korban ialah ibadah sunat pada Aidiladha. Daging dam tidak boleh dimakan oleh orang yang membayarnya.")],
        about=["Dam haji", "Dam umrah", "Larangan ihram"], js=True,
        llms="4 jenis dam (Syafi'i): tartib & taqdir (tamattu', qiran, tinggal wajib haji: kambing / puasa 3+7), takhyir & taqdir (larangan ihram: kambing / 3 gantang kepada 6 miskin / puasa 3 hari), tartib & ta'dil (jimak sebelum tahallul awal: unta), takhyir & ta'dil (buruan, pokok Tanah Haram); dibayar di Tanah Haram.")))

    # miqat
    mrows = [[f"<strong>{e(n)}</strong>", e(now), e(who), e(km)] for n, now, who, km in H.MIQAT]
    pages.append(("miqat", dict(
        h1="Miqat Haji & Umrah: 5 Miqat dan Miqat Jemaah Malaysia",
        title="Miqat Haji & Umrah: 5 Miqat dan Miqat Jemaah Malaysia",
        desc="Lima miqat makani (Zulhulaifah, Juhfah, Qarnul Manazil, Yalamlam, Zat 'Irq), miqat bagi jemaah Malaysia yang ke Jeddah atau Madinah, dan miqat zamani haji.",
        lead="Miqat ialah sempadan tempat dan masa untuk berniat ihram. Kenal pasti miqat anda berdasarkan laluan penerbangan.",
        box="Rasulullah SAW menetapkan <strong>4 miqat</strong>: <strong>Zulhulaifah</strong> (Bir Ali), <strong>Al-Juhfah</strong>, <strong>Qarnul Manazil</strong> dan <strong>Yalamlam</strong> "
            "(HR Al-Bukhari, no. 1524; Muslim, no. 1181), dan <strong>Zat 'Irq</strong> bagi penduduk Iraq (HR Abu Daud, no. 1739). "
            "Jemaah Malaysia yang ke <strong>Madinah dahulu</strong> berniat di Bir Ali; yang terbang <strong>terus ke Jeddah</strong> berniat dalam pesawat sebelum melintasi miqat.",
        sections=[("makani", "5 Miqat Makani (Tempat)", table(["Miqat", "Nama kini", "Bagi", "Jarak ke Makkah"], mrows, "Miqat makani") +
                   '<p class="note">Jarak ialah anggaran jalan raya. Penduduk dalam kawasan antara miqat dan Makkah berniat dari tempat tinggalnya; penduduk Makkah berniat umrah dari tanah halal terdekat seperti Tan\'im (Masjid Aisyah) atau Ji\'ranah.</p>'),
                  ("malaysia", "Miqat bagi Jemaah dari Malaysia", table(["Laluan", "Miqat dan cara"], [
                      ["Terbang ke Madinah dahulu", "Berniat di Zulhulaifah (Masjid Bir Ali) ketika bertolak dari Madinah ke Makkah"],
                      ["Terbang terus ke Jeddah", "Pakai ihram sebelum berlepas atau dalam pesawat, dan berniat apabila anak kapal mengumumkan hampir dengan miqat"],
                      ["Sudah berada di Makkah (umrah kedua)", "Keluar ke tanah halal (Tan'im atau Ji'ranah) untuk berniat"]], "Miqat jemaah Malaysia") +
                   '<p class="note">Ulama berbeza pendapat tentang menjadikan Jeddah sebagai miqat bagi yang terbang. Ikut ketetapan Tabung Haji atau mutawwif; yang paling berhati-hati ialah berniat dalam pesawat sebelum melintasi garisan miqat.</p>'),
                  ("zamani", "Miqat Zamani (Masa)", table(["Ibadah", "Masa berniat"], [
                      ["Haji", "Syawal, Zulkaedah dan 10 malam pertama Zulhijjah (hingga sebelum fajar 10 Zulhijjah)"],
                      ["Umrah", "Sepanjang tahun, kecuali bagi orang yang sedang dalam amalan haji"]], "Miqat zamani") +
                   doa_cards([("ayat-2-197", "Al-Baqarah 197: bulan-bulan haji", "Q:2:197", "", "", "", "")]))],
        faq=[("Di manakah miqat jemaah umrah dari Malaysia?", "Jika ke Madinah dahulu: Bir Ali (Zulhulaifah). Jika terbang terus ke Jeddah: dalam pesawat sebelum melintasi miqat, apabila diumumkan oleh anak kapal."),
             ("Apakah hukum melintasi miqat tanpa ihram?", "Berdosa dan wajib kembali ke miqat untuk berniat sebelum memulakan tawaf. Jika tidak kembali, wajib dam seekor kambing."),
             ("Di manakah miqat bagi umrah kedua ketika di Makkah?", "Di tanah halal terdekat, biasanya Tan'im (Masjid Aisyah, kira-kira 7.5 km dari Masjidil Haram) atau Ji'ranah."),
             ("Bolehkah berniat ihram di KLIA?", "Boleh berniat sebelum miqat dan ihram itu sah, tetapi larangan ihram berkuat kuasa sepanjang perjalanan yang panjang. Ramai memilih memakai ihram di lapangan terbang dan berniat dalam pesawat.")],
        about=["Miqat", "Ihram", "Umrah", "Haji"],
        llms="Miqat makani: Zulhulaifah/Bir Ali, Juhfah/Rabigh, Qarnul Manazil/As-Sail Al-Kabir, Yalamlam, Zat 'Irq (HR Al-Bukhari 1524; Muslim 1181; Abu Daud 1739); jemaah Malaysia: Bir Ali jika dari Madinah, dalam pesawat jika terus ke Jeddah; miqat zamani haji (Al-Baqarah 197); Tan'im bagi penduduk Makkah.")))

    # wanita haid
    pages.append(("umrah-wanita-haid", dict(
        h1="Haji & Umrah Wanita Haid: Hukum, Ihram dan Tawaf",
        title="Umrah & Haji Wanita Haid: Hukum, Ihram, Tawaf & Wada'",
        desc="Umrah dan haji bagi wanita: ihram ketika haid, haid sebelum tawaf, tawaf wada' gugur, pil penangguh haid, aurat ihram wanita dan mahram, dengan dalil hadis.",
        lead="Wanita haid dan nifas boleh melakukan semua amalan haji dan umrah kecuali tawaf, berdasarkan sabda Rasulullah SAW kepada Aisyah RA.",
        box="Wanita haid <strong>boleh berniat ihram</strong>, bertalbiah, wukuf, melontar dan berzikir, tetapi <strong>tidak boleh tawaf sehingga suci</strong> "
            "(HR Al-Bukhari, no. 305; Muslim, no. 1211). Jika haid sebelum tawaf umrah, <strong>kekal dalam ihram</strong> dan tawaf selepas mandi wajib. "
            "<strong>Tawaf wada' gugur</strong> bagi wanita haid atau nifas (HR Al-Bukhari, no. 1755).",
        sections=[("situasi", "Situasi dan Tindakan", table(["Situasi", "Tindakan"], [
                      ["Haid sebelum sampai miqat", "Mandi sunat ihram, berniat ihram seperti biasa dan bertalbiah; jangan masuk masjid untuk tawaf"],
                      ["Haid sebelum tawaf umrah", "Kekal berihram, tunggu suci, mandi wajib, kemudian tawaf, sa'ie dan tahallul"],
                      ["Haid selepas tawaf, sebelum sa'ie", "Teruskan sa'ie dan tahallul; sa'ie tidak mensyaratkan suci"],
                      ["Haid ketika haji sebelum tawaf ifadah", "Teruskan wukuf, Muzdalifah, melontar dan bercukur (tahallul awal); tawaf ifadah selepas suci"],
                      ["Haid ketika hendak pulang", "Tawaf wada' gugur tanpa dam"],
                      ["Masa hampir tamat, belum suci, tawaf belum dibuat", "Rujuk segera pembimbing ibadah atau mutawwif; sebahagian ulama membenarkan tawaf dalam keadaan darurat dengan pendapat tertentu"]], "Situasi wanita haid")),
                  ("ihram", "Ihram dan Aurat Wanita", ul("Pakaian biasa yang menutup aurat; tidak wajib putih, tidak perlu kain ihram khusus.",
                      "Tidak boleh memakai niqab atau sarung tangan." + ref("HR Al-Bukhari, no. 1838"),
                      "Tidak berlari-lari anak ketika tawaf dan sa'ie, dan bertalbiah dengan suara perlahan.",
                      "Tahallul dengan memotong hujung rambut sepanjang hujung jari, bukan bercukur." + ref("HR Abu Daud, no. 1985"))),
                  ("pil", "Pil Penangguh Haid", "<p>Mengambil pil untuk menangguhkan haid supaya dapat menyempurnakan tawaf <strong>harus</strong> menurut ramai ulama, dengan syarat tidak memudaratkan kesihatan. "
                   "Dapatkan nasihat doktor sekurang-kurangnya sebulan sebelum berlepas kerana pil perlu dimulakan lebih awal.</p>"),
                  ("mahram", "Mahram bagi Wanita", "<p>Dalam mazhab Syafi'i, wanita wajib ditemani suami, mahram atau rombongan wanita yang dipercayai bagi haji fardu. "
                   "Syarat pendaftaran mahram bagi jemaah Malaysia ditetapkan oleh Tabung Haji; semak syarat terkini sebelum mendaftar.</p>")],
        faq=[("Bolehkah wanita haid berniat ihram umrah?", "Boleh. Rasulullah SAW menyuruh Asma' binti Umais yang bersalin mandi dan berihram (HR Muslim, no. 1209). Dia hanya tidak boleh tawaf sehingga suci."),
             ("Bolehkah wanita haid melakukan sa'ie?", "Boleh jika tawaf telah dilakukan dalam keadaan suci sebelum haid datang. Sa'ie tidak mensyaratkan suci."),
             ("Adakah wanita haid perlu membayar dam kerana tidak tawaf wada'?", "Tidak. Tawaf wada' gugur bagi wanita haid dan nifas (HR Al-Bukhari, no. 1755; Muslim, no. 1328)."),
             ("Bolehkah wanita haid membaca doa dan zikir di Tanah Haram?", "Boleh: talbiah, zikir, doa dan selawat. Dia tidak boleh masuk masjid, tawaf atau solat, dan dalam mazhab Syafi'i tidak membaca Al-Quran dengan niat tilawah.")],
        about=["Umrah wanita", "Haid", "Tawaf"],
        llms="Haji/umrah wanita haid: boleh semua amalan kecuali tawaf (HR Al-Bukhari 305; Muslim 1211), kekal ihram hingga suci, sa'ie selepas tawaf boleh ketika haid, tawaf wada' gugur (HR Al-Bukhari 1755), larangan niqab/sarung tangan (HR Al-Bukhari 1838), pil penangguh haid harus, tahallul wanita (HR Abu Daud 1985).")))

    # badal haji
    pages.append(("badal-haji", dict(
        h1="Badal Haji & Umrah: Hukum, Syarat dan Lafaz Niat",
        title="Badal Haji & Umrah: Hukum, Syarat, Niat & Siapa Layak",
        desc="Badal haji dan umrah untuk ibu bapa yang meninggal dunia atau uzur: hukum, syarat orang yang membadalkan, lafaz niat badal dan dalil hadis sahih.",
        lead="Mengerjakan haji atau umrah bagi pihak orang yang telah meninggal dunia atau tidak mampu kerana uzur yang berkekalan.",
        box="Badal haji <strong>harus dan sah</strong> bagi orang yang telah <strong>meninggal dunia</strong> atau <strong>uzur berkekalan</strong> (sakit tiada harapan sembuh, terlalu tua), berdasarkan hadis wanita Khath'am "
            "(HR Al-Bukhari, no. 1513; Muslim, no. 1334). <strong>Syarat utama</strong>: orang yang membadalkan <strong>mesti sudah menunaikan haji untuk dirinya sendiri</strong> (HR Abu Daud, no. 1811).",
        sections=[("niat", "Lafaz Niat Badal", doa_cards([H.NIAT["badal-haji"], H.NIAT["badal-umrah"]])),
                  ("syarat", "Syarat Badal Haji", table(["Pihak", "Syarat"], [
                      ["Orang yang dibadalkan", "Telah meninggal dunia dalam keadaan Islam dan wajib haji ke atasnya, atau masih hidup tetapi uzur berkekalan (ma'dhub)"],
                      ["Orang yang membadalkan", "Islam, baligh, berakal, dan sudah menunaikan haji (atau umrah, bagi badal umrah) untuk dirinya sendiri"],
                      ["Belanja", "Haji wajib si mati diambil daripada harta pusakanya sebelum faraid, seperti hutang"],
                      ["Bilangan", "Seorang pembadal bagi seorang yang dibadalkan dalam satu musim haji"]], "Syarat badal haji")),
                  ("dalil", "Dalil Badal Haji", ul(
                      "Seorang wanita Khath'am bertanya: bapanya wajib haji tetapi sudah terlalu tua dan tidak mampu duduk di atas kenderaan, bolehkah dia berhaji untuknya? Baginda menjawab: “Ya.”" + ref("HR Al-Bukhari, no. 1513; Muslim, no. 1334"),
                      "Seorang wanita Juhainah berkata ibunya bernazar haji tetapi meninggal dunia sebelum menunaikannya. Baginda bersabda: “Berhajilah untuknya… tunaikanlah hak Allah, kerana Allah lebih berhak ditunaikan.”" + ref("HR Al-Bukhari, no. 1852"),
                      "Baginda mendengar seorang lelaki bertalbiah untuk Syubrumah lalu bertanya: “Adakah kamu sudah berhaji untuk dirimu?” Dia menjawab belum. Baginda bersabda: “Berhajilah untuk dirimu dahulu, kemudian untuk Syubrumah.”" + ref("HR Abu Daud, no. 1811"))),
                  ("pilih", "Memilih Wakil Badal", ul("Pilih individu atau agensi yang diiktiraf dan boleh memberikan bukti pelaksanaan (nama pembadal, tarikh).",
                      "Pastikan pembadal sudah menunaikan haji sendiri dan memahami manasik.", "Haji badal untuk si mati yang belum wajib haji (tidak berkemampuan semasa hidup) tidak wajib, tetapi harus sebagai sedekah pahala."))],
        faq=[("Siapakah yang boleh dibadalkan haji?", "Orang yang telah meninggal dunia, atau yang masih hidup tetapi uzur berkekalan seperti terlalu tua atau sakit tanpa harapan sembuh. Orang yang sihat dan mampu tidak boleh dibadalkan."),
             ("Bolehkah anak membadalkan haji ibu bapa sebelum menunaikan haji sendiri?", "Tidak dalam mazhab Syafi'i. Dia mesti menunaikan haji untuk dirinya dahulu (HR Abu Daud, no. 1811)."),
             ("Bolehkah lelaki membadalkan haji untuk wanita?", "Boleh, dan sebaliknya, wanita boleh membadalkan untuk lelaki."),
             ("Adakah badal umrah juga dibenarkan?", "Ya, dengan syarat yang sama: si mati atau orang yang uzur berkekalan, dan pembadal sudah menunaikan umrah untuk dirinya.")],
        about=["Badal haji", "Badal umrah", "Haji untuk ibu bapa"],
        llms="Badal haji/umrah: sah bagi yang meninggal atau uzur berkekalan (HR Al-Bukhari 1513; Muslim 1334; Al-Bukhari 1852), pembadal mesti sudah haji untuk diri sendiri (HR Abu Daud 1811), lafaz niat badal, belanja daripada harta pusaka.")))

    # ziarah madinah
    pages.append(("ziarah-madinah", dict(
        h1="Ziarah Madinah: Masjid Nabawi, Raudhah, Quba & Baqi'",
        title="Ziarah Madinah: Adab Masjid Nabawi, Raudhah, Quba & Baqi'",
        desc="Ziarah Madinah: kelebihan solat di Masjid Nabawi, Raudhah, lafaz salam kepada Rasulullah SAW, solat di Masjid Quba dan doa ziarah Baqi', dengan hadis sahih.",
        lead="Ziarah Madinah bukan sebahagian daripada rukun atau wajib haji dan umrah, tetapi amalan mulia yang dilakukan oleh hampir semua jemaah Malaysia.",
        box="Solat di <strong>Masjid Nabawi</strong> lebih baik daripada <strong>1,000 solat</strong> di masjid lain (HR Al-Bukhari, no. 1190). Kawasan antara rumah dan mimbar Baginda ialah <strong>Raudhah</strong>, "
            "satu taman daripada taman-taman syurga (HR Al-Bukhari, no. 1196). Solat di <strong>Masjid Quba</strong> menyamai pahala umrah (HR At-Tirmizi, no. 324; Ibn Majah, no. 1411).",
        sections=[("nabawi", "Masjid Nabawi dan Raudhah", ul(
                      "Niat utama musafir ialah ke Masjid Nabawi: tidak digalakkan bermusafir khusus kecuali ke tiga masjid (Masjidil Haram, Masjid Nabawi, Masjid Al-Aqsa)." + ref("HR Al-Bukhari, no. 1189"),
                      "Masuk dengan kaki kanan dan doa masuk masjid, kemudian solat tahiyatul masjid, sebaik-baiknya di Raudhah jika mudah.",
                      "Kemasukan ke Raudhah kini memerlukan tempahan melalui aplikasi rasmi Nusuk; ikut jadual yang ditetapkan untuk lelaki dan wanita.") +
                   h_item("masuk-masjid")),
                  ("salam", "Salam kepada Rasulullah SAW", doa_cards([H.ZIARAH_SALAM]) + ul(
                      "Sesiapa berselawat kepada Baginda, Allah membalas selawatnya sepuluh kali." + ref("HR Muslim, no. 408"),
                      "Tidak meninggikan suara, tidak menyentuh atau mengusap pagar makam, dan tidak berdoa menghadap makam; doa dipanjatkan kepada Allah menghadap kiblat.")),
                  ("quba", "Masjid Quba", "<p>Masjid pertama yang dibina Rasulullah SAW. Baginda mengunjunginya setiap hari Sabtu, berjalan kaki atau berkenderaan, dan solat dua rakaat" + ref("HR Al-Bukhari, no. 1193") +
                   ". Sesiapa bersuci di rumahnya kemudian datang ke Masjid Quba dan solat di dalamnya, baginya pahala seperti umrah" + ref("HR Ibn Majah, no. 1412") + ".</p>"),
                  ("baqi", "Perkuburan Baqi' dan Uhud", "<p>Rasulullah SAW menziarahi Baqi' dan mendoakan penghuninya. Gunakan doa ziarah kubur:</p>" + h_item("ziarah-kubur") +
                   '<p class="note">Di Uhud, jemaah lazimnya menziarahi makam para syuhada termasuk Hamzah bin Abdul Muttalib dan mengenang peristiwa Perang Uhud. Lihat juga <a href="/kisah-nabi/nabi-muhammad/">kisah Nabi Muhammad SAW</a>.</p>')],
        faq=[("Adakah ziarah Madinah wajib bagi jemaah haji dan umrah?", "Tidak. Ia bukan rukun atau wajib haji/umrah, tetapi sunat dan sangat digalakkan kerana kelebihan solat di Masjid Nabawi."),
             ("Bagaimana cara masuk ke Raudhah?", "Buat tempahan slot melalui aplikasi rasmi Nusuk. Lelaki dan wanita mempunyai waktu yang berasingan."),
             ("Apakah lafaz salam kepada Rasulullah SAW?", "Assalamu 'alaika ya Rasulallah, kemudian salam kepada Abu Bakar dan Umar, seperti amalan Ibn Umar (Al-Muwatta')."),
             ("Adakah solat arba'in (40 waktu) di Masjid Nabawi wajib?", "Tidak wajib dan bukan sebahagian daripada haji. Hadisnya dinilai dhaif oleh ramai ulama hadis; solatlah sebanyak mungkin di sana tanpa membebankan diri.")],
        about=["Ziarah Madinah", "Masjid Nabawi", "Raudhah"],
        llms="Ziarah Madinah: solat di Masjid Nabawi lebih baik daripada 1,000 solat (HR Al-Bukhari 1190), Raudhah taman syurga (HR Al-Bukhari 1196), salam kepada Rasulullah SAW (amalan Ibn Umar), Quba menyamai umrah (HR Ibn Majah 1412), doa ziarah Baqi' (HR Muslim 975); bukan rukun haji/umrah.")))

    # senarai barang
    n_items = sum(len(items) for _, items in H.CHECKLIST)
    pages.append(("senarai-barang-umrah", dict(
        h1="Senarai Barang Umrah & Haji: Senarai Semak yang Boleh Ditanda",
        title="Senarai Barang Umrah & Haji: Senarai Semak Lengkap",
        desc=f"Senarai semak {n_items} barang wajib bawa untuk umrah dan haji: dokumen, ihram lelaki dan wanita, ubat, barang tanpa pewangi dan barang ibadah. Tanda dan cetak.",
        lead="Senarai semak yang boleh ditanda dan dicetak: tanda disimpan dalam telefon anda supaya boleh disambung bila-bila masa sebelum berlepas.",
        box="Barang paling penting untuk umrah: <strong>pasport (sah 6 bulan), visa, sijil vaksin meningitis, kain ihram atau telekung, selipar terbuka (lelaki), ubat peribadi "
            "dan sabun tanpa pewangi</strong> untuk tempoh berihram. Bawa salinan dokumen secara berasingan dan simpan gunting kecil dalam bagasi untuk tahallul.",
        sections=[("senarai", "Senarai Semak Barang", checklist_html()),
                  ("tips", "Tip Mengemas", ul("Bagasi umrah lazimnya dihadkan oleh syarikat penerbangan; semak had berat sebelum membeli barang di Makkah dan Madinah.",
                      "Air zamzam dibawa pulang dalam karton rasmi yang dibeli di lapangan terbang atau disediakan agensi, bukan dalam bagasi biasa.",
                      "Pakai kain ihram di rumah atau lapangan terbang jika terbang terus ke Jeddah, dan bawa ihram dalam beg tangan jika ke Madinah dahulu.",
                      f"Pelajari {a('cara-umrah')} dan {a('larangan-ihram')} sebelum berlepas."))],
        faq=[("Apakah barang wajib dibawa untuk umrah?", "Pasport, visa, sijil vaksin meningitis, tiket, kain ihram (lelaki) atau telekung (wanita), selipar terbuka, ubat peribadi, wang Riyal dan barang kebersihan tanpa pewangi."),
             ("Kenapa perlu sabun tanpa pewangi?", "Memakai wangian ialah larangan ihram yang dikenakan dam. Sabun, syampu dan losyen berwangi termasuk dalam larangan ini."),
             ("Adakah palam elektrik Malaysia boleh digunakan di Arab Saudi?", "Arab Saudi menggunakan palam jenis G (tiga pin seperti Malaysia) dan jenis C, dengan voltan 220–230V. Bawa penyesuai universal untuk berjaga-jaga.")],
        about=["Barang umrah", "Persediaan umrah", "Persediaan haji"], js=True,
        llms=f"Senarai semak {n_items} barang umrah dan haji yang boleh ditanda dan dicetak: dokumen (pasport, visa, vaksin meningitis), pakaian ihram, ubat, barang tanpa pewangi, barang ibadah.")))
    return hy, days, official, pages


def hub_body(day, hy, days, official):
    guides = "".join(f'<li><a href="/{url(s)}"><span class="ti" aria-hidden="true">{ICON[s]}</span><span class="tn">{e(n)}</span><span class="td">{e(d)}</span></a></li>' for s, n, d in GUIDES)
    vir = ul(*(e(t) + ref(s) for t, s in H.VIRTUES))
    return (("tarikh", f"Tarikh Haji {hy}H", dates_table(hy, days, official)),
            ("panduan", "Panduan Haji dan Umrah", f'<ul class="tcards hu-cards">{guides}</ul>'),
            ("beza", "Beza Haji dan Umrah", table(["", "Haji", "Umrah"], [
                ["Hukum", "Rukun Islam kelima; wajib sekali seumur hidup bagi yang mampu", "Wajib sekali seumur hidup dalam mazhab Syafi'i; sunat selebihnya"],
                ["Masa", "8–13 Zulhijjah sahaja", "Bila-bila masa sepanjang tahun"],
                ["Rukun", "6 (termasuk wukuf di Arafah)", "5 (tiada wukuf)"],
                ["Tempoh", "Kira-kira 5 hari amalan; 40–45 hari perjalanan jemaah Malaysia", "3–5 jam amalan; 9–14 hari pakej biasa"],
                ["Tempat", "Makkah, Mina, Arafah, Muzdalifah", "Masjidil Haram (Kaabah, Safa dan Marwah)"],
                ["Pendaftaran di Malaysia", "Melalui Tabung Haji (giliran)", "Melalui agensi umrah berlesen Kementerian Pelancongan"]], "Beza haji dan umrah")),
            ("dalil", "Dalil Kewajipan Haji dan Kelebihannya", doa_cards([("ayat-3-97", "Ali 'Imran 97: kewajipan haji bagi yang mampu", "Q:3:97", "", "", "", "")]) + vir),
            ("daftar", "Mendaftar Haji di Malaysia", ul(
                "Daftar haji melalui akaun Lembaga Tabung Haji (aplikasi THiJARI atau kaunter TH) dengan simpanan minimum yang ditetapkan TH, kemudian tunggu giliran.",
                "Giliran haji Malaysia sangat panjang kerana kuota Arab Saudi; semak anggaran tahun giliran dalam akaun TH anda.",
                f'Rancang simpanan untuk kos haji dengan <a href="{TBB_TH}">Kalkulator Tabung Haji</a>.',
                "Umrah boleh dilakukan bila-bila masa melalui agensi berlesen; pastikan lesen agensi sah sebelum membayar.")))


def build_pages20(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    day = dt.date.fromisoformat(ctx.get("SOLAT_DAY", T))
    hy, days, official, guides = content(day)
    out = []

    def render(slug, d, secs, crumbs, toc_extra=()):
        page_url = SITE + url(slug)
        html_secs = []
        for i, (sid, h, html) in enumerate(secs):
            cls = "dsec hu-print" if 'id="hu-list"' in html else "dsec"
            html_secs.append(f'<section class="{cls}" id="{sid}" aria-labelledby="h-{sid}"><h2 id="h-{sid}">{e(h)}</h2>{html}</section>')
            if i == 0:
                html_secs.append(ad(0))
        others = "".join(f'<li><a href="/{url(s)}">{e(n)}</a></li>' for s, n, _ in GUIDES if s != slug)
        toc = [(sid, h) for sid, h, _ in secs] + [("faq", "Soalan lazim"), ("lain", "Panduan lain")]
        body = hero(e(d["h1"]), e(d["lead"]), crumbs)
        body += f'''<div class="wrap mn"><div class="ct">
<section aria-labelledby="h-jwp"><div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {d["box"]}</p></div>
{meta_line(PUB, P.dlong(dt.date.fromisoformat(PUB)).split(", ")[1])}
{share(page_url, d["title"].split(":")[0] + ":")}
</div></section>
{"".join(html_secs)}
<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim</h2>
{faq_html(d["faq"])}
</section>
<section id="lain" aria-labelledby="h-lain">
<h2 id="h-lain">Panduan Haji & Umrah Lain</h2>
<ul class="rel sts">{"" if not slug else f'<li><a href="/{HUB}">Panduan Haji & Umrah (utama)</a></li>'}{others}</ul>
<p class="note"><a href="/solat-jamak-qasar/">Solat jamak & qasar musafir</a> · <a href="/kalendar-hijrah/">Kalendar Hijrah</a> · <a href="/doa-naik-kenderaan/">Doa naik kenderaan</a> · <a href="/tasbih-digital/">Tasbih digital</a></p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(HUB)}</section>
</div>
{side(toc, HUB)}
</div>'''
        pg = dict(path=url(slug), kind="tool", data=False, arabic=True, published=PUB, modified=PUB, nocache=bool(slug), og="haji-umrah" + (f"-{slug}" if slug else ""),
                  title=d["title"], ogtitle=d["title"].split(":")[0], desc=d["desc"], crumbs=[(n, p) for n, p in crumbs], body=body, faq=d["faq"],
                  about=d["about"], ogcard=(d["title"].split(":")[0], d.get("ogsub", "Panduan mazhab Syafi'i dengan rujukan Al-Quran & hadis")), llms=d["llms"])
        if d.get("js"):
            pg["scripts"] = [JS]
        if d.get("nodes"):
            pg["nodes"] = d["nodes"](page_url)
        if d.get("itemlist"):
            pg["itemlist"] = d["itemlist"]
        return pg

    hub = dict(
        h1="Panduan Haji & Umrah Lengkap (Mazhab Syafi'i)",
        title="Panduan Haji & Umrah: Cara, Niat, Rukun, Dam & Tarikh Haji",
        desc=f"Panduan haji dan umrah lengkap: cara umrah dan haji, niat ihram, talbiah, rukun, larangan ihram, dam, miqat, badal haji dan tarikh haji {hy}H.",
        lead="Semua yang perlu diketahui sebelum menunaikan haji dan umrah, disusun mengikut mazhab Syafi'i dengan rujukan Al-Quran dan hadis, serta alat kaunter tawaf, penyemak dam dan senarai semak barang.",
        box="<strong>Haji</strong> ialah rukun Islam kelima, wajib <strong>sekali seumur hidup</strong> bagi Muslim yang mampu (Ali 'Imran 3:97; HR Muslim, no. 1337), dan hanya dilakukan pada <strong>8–13 Zulhijjah</strong>. "
            "<strong>Umrah</strong> boleh dilakukan bila-bila masa dan wajib sekali seumur hidup dalam mazhab Syafi'i. "
            f"Hari Arafah {hy}H dijangka pada <strong>{e(dlong(days[1][1]))}</strong>.",
        faq=[("Apakah beza haji dan umrah?", "Haji hanya pada 8–13 Zulhijjah dan mempunyai 6 rukun termasuk wukuf di Arafah; umrah boleh dilakukan sepanjang tahun dan mempunyai 5 rukun tanpa wukuf."),
             (f"Bilakah musim haji {hy}H?", f"8 hingga 13 Zulhijjah {hy}H, iaitu {dlong(days[0][1])} hingga {dlong(days[-1][1])} mengikut takwim Malaysia. Hari Arafah: {dlong(days[1][1])}. Tarikh wukuf ditetapkan oleh Arab Saudi."),
             ("Adakah umrah wajib?", "Dalam mazhab Syafi'i, umrah wajib sekali seumur hidup bagi yang mampu, seperti haji (Al-Baqarah 2:196). Mazhab Hanafi dan Maliki berpendapat ia sunat muakkad."),
             ("Bolehkah umrah menggantikan haji?", "Tidak. Haji tetap wajib bagi yang mampu walaupun sudah berumrah berkali-kali. Umrah pada bulan Ramadan menyamai pahala haji (HR Al-Bukhari, no. 1782) tetapi tidak menggugurkan kewajipan haji."),
             ("Bagaimana mendaftar haji di Malaysia?", "Melalui akaun Lembaga Tabung Haji dengan simpanan minimum yang ditetapkan TH, kemudian menunggu giliran yang dimaklumkan dalam akaun anda.")],
        about=["Haji", "Umrah", "Rukun Islam"],
        itemlist=dict(name="Panduan haji dan umrah", items=[{"@type": "ListItem", "position": i, "name": n, "url": SITE + url(s)} for i, (s, n, _) in enumerate(GUIDES, 1)]),
        llms=f"Hub haji & umrah (mazhab Syafi'i): beza haji dan umrah, tarikh haji {hy}H (takwim JAKIM), dalil (Ali 'Imran 97), kelebihan (HR Al-Bukhari 1773, 1521, 1782), pendaftaran Tabung Haji, 13 panduan: cara umrah, cara haji, niat ihram, talbiah, larangan ihram, rukun, jenis haji, dam, miqat, wanita haid, badal, ziarah Madinah, senarai barang.",
        ogsub="Cara umrah & haji, niat ihram, rukun, dam, miqat dan tarikh haji", js=True)
    out.append(render("", hub, hub_body(day, hy, days, official), [("Haji & Umrah", None)]))
    for slug, d in guides:
        out.append(render(slug, d, d["sections"], [("Haji & Umrah", HUB), (NAME[slug], None)]))
    for pg in out:
        assert len(pg["title"]) <= 70 and len(pg["desc"]) <= 160, (pg["path"], len(pg["title"]), len(pg["desc"]))
    return out
