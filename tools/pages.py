"""Content + structured data for every page except the home page (tools/page.html).
Each page = body HTML (rendered at build time, complete without JavaScript) + JSON-LD @graph + FAQ.
build.py wraps them in tools/layout.html."""
import json, html, datetime as dt
from surahs import S
import plans as P

SITE = "https://quran.ilmualam.com/"
MAIN = "https://www.ilmualam.com/"
TBB = "https://tool.thebukitbesi.com/"


def e(s):
    return html.escape(str(s), quote=True)


def arab(s, a, words=4):
    t = json.load(open(f"{P.REPO}/data-surah/surah-{s}.json", encoding="utf8"))[a - 1]["arabic"]
    w = [x for x in t.replace("۞", " ").split() if x not in ("ۘ", "ۖ", "ۗ", "ۚ", "ۛ", "ۙ")]
    return " ".join(w[:words]) + (" …" if len(w) > words else "")


def ayat(s, a):
    return json.load(open(f"{P.REPO}/data-surah/surah-{s}.json", encoding="utf8"))[a - 1]


TOOLS = [
    ("waktu-solat/", "🕌", "Waktu Solat Hari Ini", "Waktu solat 64 bandar di Malaysia, kiraan ke solat seterusnya, jadual sebulan dan arah kiblat."),
    ("asmaul-husna/", "✨", "Asmaul Husna", "99 nama Allah dengan maksud, ayat Al-Quran, kad hafalan, kuiz dan penjejak hafalan."),
    ("zakat-pendapatan/", "💼", "Zakat Pendapatan", "Kalkulator zakat gaji: kaedah kasar vs bersih, nisab negeri, potongan bulanan dan kos sebenar selepas rebat cukai."),
    ("zakat-simpanan/", "🏦", "Zakat Simpanan & ASB", "Zakat wang simpanan, ASB, Tabung Haji dan simpanan tetap: baki terendah, nisab negeri dan tarikh haul."),
    ("zakat-emas/", "🥇", "Zakat Emas", "Zakat emas simpanan dan perhiasan ikut ketulenan dan had uruf 15 negeri."),
    ("zakat-perniagaan/", "🏪", "Zakat Perniagaan", "Zakat perniagaan kaedah modal kerja: aset semasa, liabiliti dan pemilikan Muslim."),
    ("faraid/", "⚖️", "Kalkulator Faraid", "Bahagian harta pusaka setiap waris mengikut mazhab Syafi'i, waris terhalang dan Baitulmal."),
    ("zakat-fitrah/", "🌾", "Zakat Fitrah", "Kadar zakat fitrah semua negeri, kalkulator keluarga, berat beras dan tarikh bayaran Ramadan akan datang."),
    ("solat-jamak-qasar/", "🚗", "Solat Jamak & Qasar", "Kalkulator musafir 2 marhalah, waktu jamak hari ini di destinasi, niat dan cara setiap gabungan solat."),
    ("solat-sunat/", "🌙", "Solat Sunat", "Taubat, dhuha, hajat, jenazah, witir, istikharah, tahajjud & tarawih: cara, niat, doa dan waktu hari ini."),
    ("kalendar-hijrah/", "🗓", "Kalendar Hijrah", "Tarikh Hijrah hari ini rasmi JAKIM, puasa sunat, hari kebesaran Islam, penukar tarikh dan umur Hijrah."),
    ("tahlil-ringkas/", "🤲", "Tahlil Ringkas", "Bacaan tahlil lengkap dengan nama arwah, doa ikut lelaki/perempuan, audio, buku cetak dan mod majlis."),
    ("cari-masjid/", "📍", "Cari Masjid & Surau", "Masjid dan surau terdekat dari lokasi anda atau ikut 60 zon JAKIM, dengan arah dan waktu solat hari ini."),
    ("waktu-berbuka-puasa/", "🌙", "Waktu Berbuka Puasa & Imsak", "Jadual imsakiyah Ramadan semua zon JAKIM, kiraan detik ke berbuka, penanda puasa dan peringatan kalendar."),
    ("belajar-solat/", "🧎", "Cara Solat Lengkap", "Panduan solat fardu langkah demi langkah dengan bacaan Arab, Rumi dan maksud, rukun solat dan kalkulator qada."),
    ("doa-harian/", "🤲", "Himpunan Doa Harian", "Doa harian daripada hadis, doa Rabbana dan doa para nabi dari Al-Quran, serta ayat amalan."),
    ("zikir-pagi-petang/", "🌅", "Zikir Pagi & Petang", "Zikir pagi petang, selepas solat dan sebelum tidur dengan kaunter dan rujukan hadis."),
    ("belajar-tajwid/", "📘", "Belajar Tajwid", "Hukum nun mati, mim mati, mad dan qalqalah dengan contoh audio, pengesan hukum dan kuiz."),
    ("belajar-mengaji/", "🔤", "Belajar Mengaji", "29 huruf hijaiyah dengan makhraj, bentuk sambung dan baris, kuiz huruf dan senarai semak kemajuan."),
    ("belajar-iqra/", "📗", "Belajar Iqra' 1–6", "Latihan Iqra' interaktif tanpa had: baris, mad, tanwin, sukun, qalqalah, alif lam, sabdu dan ayat Juz 30."),
    ("jadual-khatam-al-quran/", "📅", "Jadual Khatam Al-Quran", "Kira berapa muka surat sehari dan jana jadual khatam 30 hari, Ramadan, 7 hari atau tempoh sendiri."),
    ("jadual-hafazan-al-quran/", "🧠", "Jadual Hafazan Al-Quran", "Rancang hafazan Juz 30, Al-Mulk, Yasin atau 30 juzuk dan dapatkan tarikh tamat."),
    ("tasbih-digital/", "📿", "Tasbih Digital", "Kira zikir dan tasbih selepas solat (33·33·33) dengan getaran dan kiraan tersimpan."),
    ("cari-ayat-al-quran/", "🔎", "Cari Ayat Al-Quran", "Cari 6,236 ayat mengikut kata kunci, topik atau nombor ayat dalam terjemahan Melayu."),
    ("senarai-juzuk-al-quran/", "📚", "Senarai 30 Juzuk Al-Quran", "Surah dan ayat permulaan setiap juz, muka surat, ayat sajdah dan 7 manzil."),
    ("", "📖", "Baca Al-Quran Online", "114 surah dengan teks Arab, Rumi, terjemahan Melayu dan audio 5 qari."),
]

TBB_TOOLS = [
    ("arah-kiblat/", "Arah Kiblat"), ("kalkulator-zakat-pendapatan/", "Kalkulator Zakat Pendapatan"),
    ("kalkulator-zakat-emas/", "Kalkulator Zakat Emas"), ("kalkulator-faraid/", "Kalkulator Faraid"),
    ("kalkulator-fidyah/", "Kalkulator Fidyah"), ("kalkulator-iddah/", "Kalkulator Iddah"),
    ("kalkulator-tabung-haji/", "Kalkulator Tabung Haji"), ("kalkulator-mas-kahwin/", "Kalkulator Mas Kahwin"),
]


def tool_cards(skip=None, cls="tcards"):
    li = "".join(f'<li><a href="/{p}"><span class="ti" aria-hidden="true">{i}</span><span class="tn">{e(n)}</span><span class="td">{e(d)}</span></a></li>'
                 for p, i, n, d in TOOLS if p != skip)
    return f'<ul class="{cls}">{li}</ul>'


def faq_html(faq):
    return "\n".join(f'<details class="q"><summary><h3>{e(q)}</h3></summary><div class="an"><p>{e(a)}</p></div></details>' for q, a in faq)


def crumbs(items):
    """items: [(name, path or None)]"""
    out = ['<a href="/">Al-Quran Online</a>']
    for n, p in items:
        out.append(f'<a href="/{p}">{e(n)}</a>' if p is not None else f'<span aria-current="page">{e(n)}</span>')
    return '<nav class="crumb" aria-label="Laluan">' + " › ".join(out) + "</nav>"


def hero(h1, lead, items, extra=""):
    return (f'<div class="hero sm"><div class="wrap">{crumbs(items)}<h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div></div>')


def side(toc, skip):
    lis = "".join(f'<li><a href="#{a}">{e(n)}</a></li>' for a, n in toc)
    others = "".join(f'<li><a href="/{p}">{i} {e(n)}</a></li>' for p, i, n, d in TOOLS if p != skip)
    return (f'<aside class="side" aria-label="Pautan pantas"><nav aria-label="Dalam halaman ini"><span class="sh">Dalam halaman ini</span><ol>{lis}</ol></nav>'
            f'<div class="sb"><span class="sh">Alat lain</span><ul class="one">{others}</ul></div></aside>')


def meta_line(today, todayms):
    return (f'<p class="meta2">Dikemas kini: <time datetime="{today}">{todayms}</time> · Disediakan oleh pasukan editorial '
            f'<a href="/tentang-kami/">The Ilmu Alam</a> · <a href="/tentang-kami/#semakan">Cara kami menyemak</a></p>')


def table(head, rows, label, cls=""):
    th = "".join(f'<th scope="col">{h}</th>' for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<div class="tw" tabindex="0" role="region" aria-label="{e(label)}"><table class="{cls}"><thead><tr>{th}</tr></thead>'
            f'<tbody>{tr}</tbody></table></div>')


def sref(s, a=None):
    n = P.NAMES[s - 1]
    return f'<a href="/#surah-{s}' + (f'-ayat-{a}">{e(n)} {s}:{a}</a>' if a else f'">{e(n)}</a>')


def src_list(items):
    return '<ul class="src">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


# ======================================================================================
def build_pages(ctx):
    """ctx: TODAY (iso), TODAYMS, share(url, text), ad(i). Returns list of page dicts."""
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    start = dt.date.fromisoformat(T)
    share, ad = ctx["share"], ctx["ad"]
    pages = []

    # ---------------- khatam ----------------
    ks, kt = P.khatam_html(30, 0, start)
    quick = []
    for D in (3, 7, 10, 15, 20, 29, 30, 40, 60, 90, 180, 365):
        rows, juz, _ = P.khatam(D, 0)
        b, x = 604 // D, 604 % D
        per = f"{30 // D} juzuk" if juz else (f"{b}" if x == 0 else f"{b}–{b + 1}")
        quick.append([f"<strong>{D} hari</strong>", per + ("" if juz else " muka surat"), P.r1(604 / D), P.r1(604 / D / 5)])
    manz = []
    M = [P.gid(*x) for x in P.META["manzil"]] + [P.TOTAL + 1]
    HARI7 = ["Jumaat", "Sabtu", "Ahad", "Isnin", "Selasa", "Rabu", "Khamis"]
    for i in range(7):
        s1, _ = P.sa(M[i]); s2, _ = P.sa(M[i + 1] - 1)
        p1, p2 = P.page_of(M[i]), P.page_of(M[i + 1] - 1)
        manz.append([f"<strong>{i + 1}</strong>", HARI7[i], f"{sref(s1)} – {e(P.NAMES[s2 - 1])}", f"{p1}–{p2}", str(p2 - p1 + 1)])
    kfaq = [
        ("Berapa muka surat sehari untuk khatam Al-Quran dalam sebulan?",
         "Untuk khatam dalam 30 hari, baca 1 juzuk sehari, iaitu kira-kira 20 muka surat Mushaf Madinah (604 muka surat). Jika dibahagikan kepada 5 waktu solat fardu, ia hanya kira-kira 4 muka surat selepas setiap solat."),
        ("Bagaimana hendak khatam Al-Quran dalam Ramadan yang 29 hari?",
         "Baca 20 hingga 21 muka surat sehari (purata 20.8). Jadual 29 hari di atas membahagikan 604 muka surat kepada 24 hari bacaan 21 muka surat dan 5 hari bacaan 20 muka surat, lalu menunjukkan surah dan ayat mula serta tamat bagi setiap hari."),
        ("Berapa lama masa untuk membaca satu juzuk?",
         "Anggaran kasar ialah 30 hingga 45 minit bagi bacaan sederhana. Bacaan laju (hadr) lebih singkat dan bacaan tartil lebih lama. Cara terbaik ialah mengukur masa bacaan satu muka surat anda sendiri, kemudian darabkan dengan bilangan muka surat sehari dalam jadual."),
        ("Berapa kerap Rasulullah SAW menganjurkan umatnya khatam Al-Quran?",
         "Dalam hadis Abdullah bin 'Amr, Rasulullah SAW bersabda: “Bacalah (khatamkan) Al-Quran dalam sebulan”, kemudian membenarkan sehingga tujuh hari (riwayat Al-Bukhari no. 5054 dan Muslim no. 1159). Dalam riwayat Abu Daud (no. 1394) dan At-Tirmizi (no. 2949) disebut bahawa orang yang khatam kurang daripada tiga hari tidak dapat memahaminya."),
        ("Saya tertinggal beberapa hari. Bolehkah jadual dikira semula?",
         "Boleh. Isi ruangan “Sudah baca sehingga muka surat” dengan muka surat terakhir yang anda baca dan tetapkan baki hari. Alat ini membahagikan semula baki muka surat secara sama rata dan mengemas kini tarikh khatam."),
        ("Adakah jadual ini sesuai untuk mushaf yang saya gunakan?",
         "Nombor muka surat mengikut Mushaf Madinah 15 baris (604 muka surat), susun atur yang digunakan oleh kebanyakan mushaf Rasm Uthmani di Malaysia. Jika mushaf anda berbeza, ikut lajur surah dan ayat kerana rujukan surah:ayat adalah sama dalam semua mushaf."),
        ("Bolehkah saya dapat peringatan bacaan setiap hari?",
         "Boleh. Tekan “Simpan ke kalendar (.ics)” untuk memuat turun jadual sebagai acara harian, kemudian buka fail itu dengan Google Calendar, Kalendar iPhone atau Outlook. Anda juga boleh menanda hari yang selesai; tanda itu disimpan dalam pelayar anda."),
    ]
    body = hero("Jadual Khatam Al-Quran: Kira Berapa Muka Surat Sehari",
                "Tetapkan tempoh dan tarikh mula. Jadual harian dengan muka surat, surah dan ayat dijana serta-merta, berdasarkan Mushaf Madinah 604 muka surat.",
                [("Alat", "alat/"), ("Jadual Khatam", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira">📅 Kalkulator Khatam Al-Quran</h2>
<form class="frm" id="kf" novalidate>
<div class="fl"><label for="kd">Khatam dalam (hari)</label><input id="kd" name="hari" type="number" inputmode="numeric" min="1" max="1000" value="30"></div>
<div class="fl w2"><label for="ks">Tarikh mula</label><input id="ks" name="mula" type="date" value="{T}"></div>
<div class="fl"><label for="kr">Sudah baca sehingga muka surat</label><input id="kr" name="dibaca" type="number" inputmode="numeric" min="0" max="603" value="0"><small>0 jika baru bermula</small></div>
</form>
<div class="kpre chips2" role="group" aria-label="Tempoh popular">{"".join(f'<button type="button" data-v="{v}" aria-pressed="{"true" if v == 30 else "false"}">{l}</button>' for v, l in [(7, "7 hari"), (15, "15 hari"), (29, "Ramadan 29"), (30, "30 hari"), (60, "60 hari"), (365, "Setahun")])}</div>
<div class="sum" id="ksum" aria-live="polite">{ks}</div>
<p class="prog" id="kprog" aria-live="polite"></p>
<div class="act" id="kact"><button class="btn2" type="button" data-act="ics">📆 Simpan ke kalendar (.ics)</button><button class="btn2" type="button" data-act="link">🔗 Salin pautan jadual</button><button class="btn2" type="button" data-act="print">🖨 Cetak / PDF</button></div>
<div class="tw" tabindex="0" role="region" aria-label="Jadual khatam harian"><table class="plan" id="kt">
<colgroup><col style="width:64px"><col style="width:124px"><col style="width:104px"><col><col><col style="width:52px"></colgroup>
<thead><tr><th scope="col">Hari</th><th scope="col">Tarikh</th><th scope="col">Muka surat</th><th scope="col">Mula</th><th scope="col">Tamat</th><th scope="col">✓</th></tr></thead>
<tbody>{kt}</tbody></table></div>
<p class="note">Klik nama surah pada lajur “Mula” untuk terus membaca dan mendengar ayat itu dalam pembaca Al-Quran.</p>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp">Berapa Muka Surat Sehari Untuk Khatam Al-Quran?</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Untuk khatam Al-Quran dalam 30 hari, baca <strong>1 juzuk sehari (kira-kira 20 muka surat)</strong>. Jika dibahagikan kepada 5 waktu solat fardu, ia hanya <strong>4 muka surat selepas setiap solat</strong>. Untuk Ramadan 29 hari, baca 20–21 muka surat sehari; untuk khatam seminggu, baca kira-kira 86 muka surat (4–5 juzuk) sehari.</p></div>
{meta_line(T, TMS)}
{share(SITE + "jadual-khatam-al-quran/", "Jadual khatam Al-Quran – kira berapa muka surat sehari:")}
</div>
{table(["Tempoh", "Bacaan sehari", "Purata muka surat/hari", "Muka surat selepas setiap solat"], quick, "Jadual pantas berapa muka surat sehari mengikut tempoh khatam")}
<p class="note">Berdasarkan 604 muka surat Mushaf Madinah. Bagi tempoh yang membahagi 30 dengan tepat (contohnya 30, 15, 10 hari), jadual mengikut sempadan juzuk.</p>
</section>
{ad(0)}
<section id="cara" aria-labelledby="h-cara">
<div class="prose">
<h2 id="h-cara">Cara Khatam Al-Quran Dalam Sebulan (Termasuk Ramadan)</h2>
<ol class="steps">
<li><strong>Tetapkan tempoh</strong> (contohnya 30 hari, atau 29 hari bagi Ramadan) dan tarikh mula dalam kalkulator di atas.</li>
<li><strong>Pecahkan mengikut waktu solat.</strong> 20 muka surat sehari menjadi 4 muka surat selepas setiap solat fardu, kira-kira 10 minit setiap kali bagi bacaan sederhana.</li>
<li><strong>Simpan ke kalendar</strong> supaya anda menerima peringatan bacaan setiap hari, atau cetak jadual dan selitkan dalam mushaf.</li>
<li><strong>Tanda hari yang selesai</strong> (lajur ✓). Jika tertinggal, masukkan muka surat terakhir yang dibaca untuk mengira semula baki.</li>
<li><strong>Dengar sambil membaca.</strong> Klik rujukan surah untuk membuka ayat dalam pembaca dan ikut bacaan qari bagi memperbetulkan sebutan.</li>
</ol>
</div>
</section>

<section id="manzil" aria-labelledby="h-manzil">
<div class="prose">
<h2 id="h-manzil">Khatam Dalam 7 Hari: Kaedah 7 Manzil</h2>
<p>Sebahagian sahabat dan salafussoleh mengkhatamkan Al-Quran setiap minggu dengan membahagikannya kepada tujuh bahagian yang dipanggil <em>manzil</em> (atau <em>hizb</em>). Permulaan setiap manzil diingati dengan singkatan <strong>“fami bisyauqin”</strong> (ف م ي ب ش و ق): Al-Fatihah, Al-Ma'idah, Yunus, Bani Isra'il (Al-Isra'), Asy-Syu'ara', Wa As-Saffat dan Qaf.</p>
</div>
{table(["Manzil", "Cadangan hari", "Surah", "Muka surat", "Bilangan muka surat"], manz, "Tujuh manzil Al-Quran untuk khatam seminggu")}
<p class="note">Cadangan hari bermula Jumaat hanyalah contoh. Manzil tidak sama panjang; gunakan kalkulator di atas dengan 7 hari jika mahu bacaan harian yang sama rata.</p>
</section>

<section id="dalil" aria-labelledby="h-dalil">
<div class="prose">
<h2 id="h-dalil">Berapa Lama Tempoh Khatam Yang Dianjurkan?</h2>
<p>Abdullah bin 'Amr RA meminta untuk membaca lebih banyak, lalu Rasulullah SAW bersabda:</p>
<blockquote class="ayah" style="margin-inline:0"><p>“Bacalah (khatamkan) Al-Quran dalam sebulan.” … “Bacalah dalam tujuh hari dan jangan kurang daripada itu.”</p><p><cite>— Riwayat Al-Bukhari (no. 5054) dan Muslim (no. 1159)</cite></p></blockquote>
<p>Dalam riwayat lain disebut: <em>“Tidak memahami (Al-Quran) orang yang membacanya kurang daripada tiga hari”</em> (riwayat Abu Daud, no. 1394; At-Tirmizi, no. 2949). Ulama memahami hadis-hadis ini sebagai panduan supaya bacaan disertai kefahaman dan tadabbur, bukan semata-mata mengejar bilangan khatam. Konsistensi lebih utama: sedikit tetapi berterusan.</p>
<p>Rasulullah SAW juga menjelaskan ganjaran setiap huruf: satu huruf dibalas dengan satu kebaikan, dan satu kebaikan digandakan sepuluh kali (riwayat At-Tirmizi, no. 2910).</p>
</div>
</section>

<section id="kaedah" aria-labelledby="h-kaedah">
<div class="prose">
<h2 id="h-kaedah">Bagaimana Jadual Ini Dikira</h2>
<ul>
<li><strong>Susun atur:</strong> Mushaf Madinah 15 baris, 604 muka surat, 30 juzuk. Permulaan setiap muka surat dipetakan kepada surah dan ayat (data Tanzil melalui pakej sumber terbuka <a href="https://github.com/quran-center/quran-meta" rel="noopener">quran-meta</a>, lesen MIT).</li>
<li><strong>Tempoh yang membahagi 30</strong> (1, 2, 3, 5, 6, 10, 15, 30 hari): setiap hari bermula tepat pada awal juzuk.</li>
<li><strong>Tempoh lain atau bacaan disambung:</strong> baki muka surat dibahagi sama rata; hari-hari awal menerima satu muka surat tambahan jika ada baki.</li>
<li>Semua kiraan berlaku dalam pelayar anda. Tiada data dihantar ke pelayan.</li>
</ul>
</div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Jadual Khatam Al-Quran</h2>
{faq_html(kfaq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel">
<h2 id="h-rel">Alat Al-Quran Lain</h2>
{tool_cards("jadual-khatam-al-quran/")}
</section>
</div>
{side([("kira", "Kalkulator khatam"), ("h-jwp", "Muka surat sehari"), ("cara", "Cara khatam sebulan"), ("manzil", "7 manzil"), ("dalil", "Tempoh dianjurkan"), ("faq", "Soalan lazim")], "jadual-khatam-al-quran/")}
</div>'''
    pages.append(dict(
        path="jadual-khatam-al-quran/", kind="tool", data=True, arabic=False,
        title="Jadual Khatam Al-Quran 30 Hari & Ramadan (Kalkulator Percuma)",
        ogtitle="Jadual Khatam Al-Quran: Berapa Muka Surat Sehari?",
        desc="Jana jadual khatam Al-Quran ikut tempoh anda: 30 hari (1 juzuk sehari), Ramadan 29 hari, 7 atau 60 hari. Lihat muka surat, surah & ayat setiap hari.",
        crumbs=[("Alat", "alat/"), ("Jadual Khatam Al-Quran", None)], body=body, faq=kfaq,
        app=dict(name="Kalkulator Jadual Khatam Al-Quran", features=["Jadual harian ikut tempoh (1–1000 hari)", "Sempadan juzuk automatik", "Sambung bacaan dari mana-mana muka surat", "Simpan ke kalendar (.ics)", "Tanda hari selesai", "Cetak / PDF"]),
        about=["Khatam Al-Quran", "Juz (Al-Quran)", "Ramadan"],
        llms="Kalkulator jadual khatam Al-Quran: masukkan bilangan hari, tarikh mula dan muka surat terakhir dibaca; hasilnya jadual harian (muka surat, surah:ayat mula dan tamat) berdasarkan Mushaf Madinah 604 muka surat. Khatam 30 hari = 1 juzuk (≈20 muka surat) sehari = ≈4 muka surat selepas setiap solat fardu; Ramadan 29 hari = 20–21 muka surat sehari; 7 hari = 86–87 muka surat sehari.",
    ))

    # ---------------- hafazan ----------------
    hs, ht = P.hafazan_html("j30", "pendek", "ayat", 5, "7", start)
    opts = []
    groups = [("Popular", [k for k, _, _ in P.TARGETS if not (k.startswith("j") and k not in ("j28", "j29", "j30"))]),
              ("Mengikut juzuk", [f"j{n}" for n in range(1, 28)])]
    for g, keys in groups:
        opts.append(f'<optgroup label="{g}">' + "".join(f'<option value="{k}"{" selected" if k == "j30" else ""}>{e(P.TMAP[k][0])}</option>' for k in keys) + "</optgroup>")
    est = []
    for k in ("s67", "s36", "s18", "j30", "j29", "all"):
        lab, segs = P.TMAP[k]
        tot = sum(a2 - a1 + 1 for _, a1, a2 in segs)
        row = [f"<strong>{e(lab)}</strong>", P.num(tot)]
        for n in (3, 5, 10):
            d = -(-tot // n)
            row.append(f"{P.num(d)} hari")
        est.append(row)
    hfaq = [
        ("Berapa lama masa untuk menghafal Juz 30?",
         "Juz 30 mempunyai 564 ayat dalam 37 surah. Pada kadar 3 ayat sehari ia mengambil 188 hari, pada 5 ayat sehari 113 hari (kira-kira 4 bulan) dan pada 10 ayat sehari 57 hari, tidak termasuk hari rehat atau murajaah."),
        ("Berapa lama untuk menghafal seluruh Al-Quran?",
         "Dengan kadar 1 muka surat sehari, 604 muka surat Mushaf Madinah memerlukan 604 sesi, iaitu kira-kira 1 tahun 8 bulan jika menghafal setiap hari, atau kira-kira 2 tahun pada 6 hari seminggu. Pada kadar 2 muka surat sehari, ia memerlukan 302 sesi."),
        ("Kenapa ramai mula menghafal dari surah pendek (An-Nas ke belakang)?",
         "Surah-surah Juz 30 pendek, kerap dibaca dalam solat dan cepat memberi rasa pencapaian. Pilih susunan “Surah pendek dahulu” supaya jadual bermula dari An-Nas dan bergerak ke An-Naba'. Bagi juzuk lain, susunan mushaf lebih lazim."),
        ("Berapa ayat sehari yang sesuai untuk dihafal?",
         "Tiada satu angka untuk semua orang. Mulakan dengan kadar kecil (contohnya 1 hingga 3 ayat atau separuh muka surat), dan tambah hanya apabila hafazan lama kekal kukuh. Kekuatan hafazan bergantung pada murajaah yang konsisten, bukan kelajuan."),
        ("Apakah murajaah dan bagaimana menjadualkannya?",
         "Murajaah ialah mengulang hafazan lama supaya tidak lupa. Kaedah lazim: hafaz bahagian baharu, ulang bahagian beberapa hari lepas setiap hari, dan ulang hafazan lama secara bergilir mengikut juzuk. Gunakan pilihan hari hafazan (contohnya 5 atau 6 hari seminggu) dan khaskan hari selebihnya untuk murajaah."),
        ("Adakah alat ini menggantikan guru tahfiz?",
         "Tidak. Alat ini hanya merancang jadual. Bacaan dan sebutan perlu diperdengarkan (talaqqi) kepada guru bertauliah supaya kesilapan tajwid tidak turut dihafal."),
    ]
    body = hero("Jadual Hafazan Al-Quran: Rancang Hafal Juz 30, Yasin & 30 Juzuk",
                "Pilih sasaran hafazan dan kadar sehari. Dapatkan tarikh tamat serta jadual sesi demi sesi yang boleh dicetak atau disimpan ke kalendar.",
                [("Alat", "alat/"), ("Jadual Hafazan", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira">🧠 Perancang Hafazan Al-Quran</h2>
<form class="frm" id="hf" novalidate>
<div class="fl w2"><label for="htg">Sasaran hafazan</label><select id="htg" name="sasaran">{"".join(opts)}</select></div>
<div class="fl"><label for="ho">Susunan</label><select id="ho" name="susunan"><option value="pendek" selected>Surah pendek dahulu</option><option value="mushaf">Ikut susunan mushaf</option></select></div>
<div class="fl"><label for="hn">Kadar sehari</label><input id="hn" name="kadar" type="number" inputmode="numeric" min="1" max="50" value="5"></div>
<div class="fl"><label for="hu">Unit</label><select id="hu" name="unit"><option value="ayat" selected>Ayat</option><option value="page">Muka surat</option></select></div>
<div class="fl"><label for="hw">Hari hafazan</label><select id="hw" name="hari">{"".join(f'<option value="{k}"{" selected" if k == "7" else ""}>{e(v[0])}</option>' for k, v in P.WEEK.items())}</select></div>
<div class="fl"><label for="hs">Tarikh mula</label><input id="hs" name="mula" type="date" value="{T}"></div>
</form>
<div class="sum" id="hsum" aria-live="polite">{hs}</div>
<div class="act" id="hact"><button class="btn2" type="button" data-act="ics">📆 Simpan ke kalendar (.ics)</button><button class="btn2" type="button" data-act="link">🔗 Salin pautan</button><button class="btn2" type="button" data-act="print">🖨 Cetak / PDF</button></div>
<div class="tw" tabindex="0" role="region" aria-label="Jadual hafazan"><table class="plan" id="ht">
<colgroup><col style="width:64px"><col style="width:124px"><col><col style="width:64px"></colgroup>
<thead><tr><th scope="col">Sesi</th><th scope="col">Tarikh</th><th scope="col">Hafazan baharu</th><th scope="col">Ayat</th></tr></thead>
<tbody>{ht}</tbody></table></div>
<p class="note">Unit “muka surat” mengikut Mushaf Madinah (604 muka surat) dan sentiasa mengikut susunan mushaf. Klik rujukan untuk mendengar bacaan qari bagi ayat tersebut.</p>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp">Berapa Lama Untuk Menghafal Juz 30 dan Al-Quran?</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Pada kadar <strong>5 ayat sehari, Juz 30 (564 ayat) mengambil 113 hari</strong>, kira-kira 4 bulan. Surah Al-Mulk (30 ayat) mengambil 6 hari dan Surah Yasin (83 ayat) 17 hari. Seluruh Al-Quran pada <strong>1 muka surat sehari mengambil 604 hari</strong> (kira-kira 1 tahun 8 bulan), tidak termasuk hari murajaah.</p></div>
{meta_line(T, TMS)}
{share(SITE + "jadual-hafazan-al-quran/", "Rancang hafazan Al-Quran – Juz 30, Yasin, Al-Mulk:")}
</div>
{table(["Sasaran", "Ayat", "3 ayat/hari", "5 ayat/hari", "10 ayat/hari"], est, "Anggaran tempoh hafazan mengikut kadar ayat sehari")}
<p class="note">Bilangan sesi hafazan berturut-turut. Tambah hari rehat dan murajaah mengikut jadual anda.</p>
</section>
{ad(0)}
<section id="cara" aria-labelledby="h-cara">
<div class="prose">
<h2 id="h-cara">Cara Menghafal Al-Quran Dengan Konsisten</h2>
<ol class="steps">
<li><strong>Betulkan bacaan dahulu.</strong> Dengar bacaan qari ayat demi ayat (klik rujukan dalam jadual) dan perdengarkan kepada guru sebelum mula menghafal.</li>
<li><strong>Hafaz sedikit, ulang banyak.</strong> Baca ayat baharu berulang kali sambil melihat mushaf, kemudian tanpa melihat, sehingga lancar.</li>
<li><strong>Sambung ayat.</strong> Sebelum menambah ayat baharu, baca semula ayat-ayat sebelumnya supaya sambungan antara ayat kukuh.</li>
<li><strong>Murajaah setiap hari.</strong> Ulang hafazan beberapa hari lepas, dan pusingkan hafazan lama mengikut juzuk.</li>
<li><strong>Baca dalam solat.</strong> Gunakan surah yang baru dihafal dalam solat sunat dan fardu untuk menguatkan ingatan.</li>
</ol>
<p>Rasulullah SAW bersabda: <em>“Sebaik-baik kamu ialah orang yang mempelajari Al-Quran dan mengajarkannya”</em> (riwayat Al-Bukhari, no. 5027). Baginda juga mengingatkan supaya hafazan sentiasa dijaga kerana ia lebih cepat terlepas berbanding unta yang terlepas daripada ikatannya (riwayat Al-Bukhari, no. 5033; Muslim, no. 791).</p>
</div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Hafazan Al-Quran</h2>
{faq_html(hfaq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel">
<h2 id="h-rel">Alat Al-Quran Lain</h2>
{tool_cards("jadual-hafazan-al-quran/")}
</section>
</div>
{side([("kira", "Perancang hafazan"), ("h-jwp", "Tempoh hafazan"), ("cara", "Cara menghafal"), ("faq", "Soalan lazim")], "jadual-hafazan-al-quran/")}
</div>'''
    pages.append(dict(
        path="jadual-hafazan-al-quran/", kind="tool", data=True, arabic=False,
        title="Jadual Hafazan Al-Quran: Rancang Hafal Juz 30, Yasin & Al-Mulk",
        ogtitle="Jadual Hafazan Al-Quran – Juz 30, Yasin & 30 Juzuk",
        desc="Rancang hafazan Al-Quran ikut kemampuan: pilih Juz 30, Al-Mulk, Yasin atau 30 juzuk, tetapkan ayat sehari dan dapatkan tarikh tamat serta jadual harian.",
        crumbs=[("Alat", "alat/"), ("Jadual Hafazan Al-Quran", None)], body=body, faq=hfaq,
        app=dict(name="Perancang Jadual Hafazan Al-Quran", features=["Sasaran: Juz 1–30, seluruh Al-Quran, Yasin, Al-Mulk, Al-Kahfi dan lain-lain", "Kadar ikut ayat atau muka surat", "Susunan surah pendek dahulu", "Hari hafazan 5, 6 atau 7 hari seminggu", "Simpan ke kalendar (.ics)"]),
        about=["Hafazan Al-Quran", "Tahfiz", "Juz Amma"],
        llms="Perancang jadual hafazan Al-Quran: pilih sasaran (Juz 1–30, seluruh Al-Quran, Al-Mulk, Yasin, Al-Kahfi, Al-Waqi'ah, Ar-Rahman, As-Sajdah, Al-Baqarah), kadar ayat atau muka surat sehari, susunan dan hari hafazan seminggu; hasilnya tarikh tamat dan jadual setiap sesi. Juz 30 = 564 ayat: 113 hari pada 5 ayat sehari, 57 hari pada 10 ayat sehari. Seluruh Al-Quran pada 1 muka surat sehari = 604 sesi.",
    ))

    # ---------------- tasbih ----------------
    Z = {
        "SUB": ("سُبْحَانَ ٱللَّٰهِ", "Subhanallah", "Maha Suci Allah"),
        "HAM": ("ٱلْحَمْدُ لِلَّٰهِ", "Alhamdulillah", "Segala puji bagi Allah"),
        "AKB": ("ٱللَّٰهُ أَكْبَرُ", "Allahu Akbar", "Allah Maha Besar"),
        "TAM": ("لَا إِلَٰهَ إِلَّا ٱللَّٰهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ ٱلْمُلْكُ وَلَهُ ٱلْحَمْدُ وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ",
                "La ilaha illallahu wahdahu la syarika lah, lahul mulku wa lahul hamdu wa huwa 'ala kulli syai'in qadir",
                "Tiada tuhan melainkan Allah, Yang Esa, tiada sekutu bagi-Nya. Bagi-Nya kerajaan dan bagi-Nya segala puji, dan Dia Maha Berkuasa atas segala sesuatu"),
        "IST": ("أَسْتَغْفِرُ ٱللَّٰهَ", "Astaghfirullah", "Aku memohon ampun kepada Allah"),
        "SEL": ("ٱللَّٰهُمَّ صَلِّ عَلَىٰ سَيِّدِنَا مُحَمَّدٍ", "Allahumma solli 'ala Sayyidina Muhammad", "Ya Allah, limpahkanlah selawat ke atas junjungan kami Nabi Muhammad"),
        "TAH": ("لَا إِلَٰهَ إِلَّا ٱللَّٰهُ", "La ilaha illallah", "Tiada tuhan melainkan Allah"),
        "SWB": ("سُبْحَانَ ٱللَّٰهِ وَبِحَمْدِهِ", "Subhanallahi wa bihamdih", "Maha Suci Allah dan segala puji bagi-Nya"),
        "HAW": ("لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِٱللَّٰهِ", "La hawla wa la quwwata illa billah", "Tiada daya dan kekuatan melainkan dengan (pertolongan) Allah"),
    }
    def zs(*pairs):
        return [dict(a=Z[k][0], r=Z[k][1], m=Z[k][2], n=n) for k, n in pairs]
    PRE = [
        ("solat", "Selepas solat (33·33·33·1)", zs(("SUB", 33), ("HAM", 33), ("AKB", 33), ("TAM", 1)), "HR Muslim, no. 597"),
        ("sub", "Subhanallah 33", zs(("SUB", 33)), "HR Muslim, no. 597"),
        ("ham", "Alhamdulillah 33", zs(("HAM", 33)), "HR Muslim, no. 597"),
        ("akb", "Allahu Akbar 33", zs(("AKB", 33)), "HR Muslim, no. 597"),
        ("ist", "Istighfar 100", zs(("IST", 100)), "HR Muslim, no. 2702"),
        ("swb", "Subhanallahi wa bihamdih 100", zs(("SWB", 100)), "HR Al-Bukhari, no. 6405; Muslim, no. 2691"),
        ("sel", "Selawat 100", zs(("SEL", 100)), "Galakan selawat: HR Muslim, no. 408"),
        ("tah", "La ilaha illallah 100", zs(("TAH", 100)), "Zikir tahlil"),
        ("haw", "La hawla wa la quwwata 100", zs(("HAW", 100)), "HR Al-Bukhari, no. 4205; Muslim, no. 2704"),
        ("bebas", "Bebas (sasaran sendiri)", zs(("SUB", 33)), ""),
    ]
    zd = {k: dict(l=l, s=s) for k, l, s, _ in PRE}
    zd["bebas"]["s"] = [dict(a="ذِكْرُ ٱللَّٰهِ", r="Zikir pilihan anda", m="Tetapkan sasaran sendiri di bawah", n=0)]
    first = PRE[0][2][0]
    tz_rows = [[f"<strong>{e(l)}</strong>", " → ".join(f"{e(x['r'])} ×{x['n']}" for x in s), e(src)] for k, l, s, src in PRE if k not in ("bebas", "sub", "ham", "akb")]
    tfaq = [
        ("Berapa kali tasbih selepas solat fardu?",
         "Subhanallah 33 kali, Alhamdulillah 33 kali dan Allahu Akbar 33 kali (jumlah 99), kemudian digenapkan menjadi 100 dengan La ilaha illallahu wahdahu la syarika lah, lahul mulku wa lahul hamdu wa huwa 'ala kulli syai'in qadir. Rasulullah SAW menyebut dosa orang yang mengamalkannya diampunkan walaupun sebanyak buih di lautan (riwayat Muslim, no. 597)."),
        ("Apakah hukum menggunakan tasbih digital atau aplikasi untuk berzikir?",
         "Harus. Alat pengira seperti biji tasbih, pengira digital atau aplikasi hanyalah wasilah untuk mengira bilangan zikir, dan majoriti ulama mengharuskannya. Yang penting ialah lafaz zikir dan kehadiran hati."),
        ("Mana lebih afdal: kira zikir dengan jari atau tasbih?",
         "Mengira dengan jari, terutamanya jari tangan kanan, ialah sunnah. Abdullah bin 'Amr RA melihat Rasulullah SAW menghitung tasbih dengan tangan kanannya (riwayat Abu Daud, no. 1502), dan baginda menyuruh para wanita mengira dengan hujung jari kerana jari akan ditanya dan diminta berkata-kata (riwayat Abu Daud, no. 1501; At-Tirmizi, no. 3583). Tasbih digital memudahkan kiraan yang banyak."),
        ("Adakah kiraan zikir saya disimpan?",
         "Ya, dalam pelayar anda sahaja (localStorage). Kiraan semasa, jumlah hari ini dan jumlah keseluruhan kekal walaupun halaman ditutup. Tiada data dihantar kepada kami."),
        ("Bolehkah tasbih digital ini digunakan tanpa internet?",
         "Boleh. Selepas lawatan pertama, halaman ini disimpan oleh service worker dan boleh dibuka tanpa sambungan internet. Anda juga boleh memasangnya ke skrin utama telefon melalui butang Install atau menu pelayar."),
        ("Zikir apa yang baik diamalkan 100 kali sehari?",
         "Antaranya Subhanallahi wa bihamdih 100 kali sehari, yang menghapuskan dosa walaupun sebanyak buih di lautan (riwayat Al-Bukhari, no. 6405; Muslim, no. 2691), dan istighfar, kerana Rasulullah SAW sendiri beristighfar 100 kali sehari (riwayat Muslim, no. 2702)."),
    ]
    C = 339.29  # 2*pi*54
    body = hero("Tasbih Digital Online: Kira Zikir & Tasbih Selepas Solat",
                "Ketik butang besar untuk mengira. Getaran pada setiap kiraan, peralihan automatik 33·33·33·1 dan kiraan disimpan dalam telefon anda.",
                [("Alat", "alat/"), ("Tasbih Digital", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool tz" aria-labelledby="h-kira">
<h2 id="h-kira" class="sr">Tasbih digital</h2>
<div class="chips2" id="tpre" role="group" aria-label="Pilih zikir">{"".join(f'<button type="button" data-p="{k}" aria-pressed="{"true" if k == "solat" else "false"}">{e(l)}</button>' for k, l, s, _ in PRE)}</div>
<div id="tz" class="tzw">
<p class="tar" id="tar" lang="ar" dir="rtl">{first["a"]}</p>
<p class="trm" id="trm">{e(first["r"])}</p>
<p class="tmn" id="tmn">{e(first["m"])}</p>
<button class="tbtn" id="tbtn" type="button" aria-label="Kira {e(first['r'])}. Kiraan 0 daripada 33">
<svg viewBox="0 0 120 120" width="240" height="240" aria-hidden="true"><circle cx="60" cy="60" r="54" class="trk"/><circle id="tring" cx="60" cy="60" r="54" class="tpr" style="stroke-dasharray:{C};stroke-dashoffset:{C}"/></svg>
<span class="tnum"><span id="tcnt">0</span><span class="ttgt" id="ttgt">/ 33</span></span>
</button>
<p class="tstep" id="tstep" aria-live="polite">Langkah 1 daripada 4</p>
<div class="fl tcustom" id="tcustom" hidden><label for="tn">Sasaran kiraan</label><input id="tn" type="number" inputmode="numeric" min="1" max="100000" value="33"></div>
<div class="act tact"><button class="btn2" id="tundo" type="button">↶ Tolak 1</button><button class="btn2" id="treset" type="button">⟲ Set semula</button><button class="btn2" id="tvib" type="button" aria-pressed="true">📳 Getar</button><button class="btn2" id="twake" type="button" aria-pressed="false">☀️ Skrin kekal hidup</button></div>
<dl class="tstat"><div><dt>Hari ini</dt><dd id="tday">0</dd></div><div><dt>Jumlah keseluruhan</dt><dd id="tall">0</dd></div></dl>
</div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp">Bacaan Tasbih Selepas Solat Fardu</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Selepas solat fardu, baca <strong>Subhanallah 33 kali, Alhamdulillah 33 kali dan Allahu Akbar 33 kali</strong>, kemudian genapkan 100 dengan <em>La ilaha illallahu wahdahu la syarika lah, lahul mulku wa lahul hamdu wa huwa 'ala kulli syai'in qadir</em>. Rasulullah SAW menyebut dosa pengamalnya diampunkan walaupun sebanyak buih di lautan (riwayat Muslim, no. 597).</p></div>
{meta_line(T, TMS)}
{share(SITE + "tasbih-digital/", "Tasbih digital percuma – kira zikir di telefon:")}
<figure class="ayah" style="margin-inline:0">
<p class="a" lang="ar" dir="rtl">{Z["TAM"][0]}</p>
<figcaption><p>{e(Z["TAM"][1])}</p><p>“{e(Z["TAM"][2])}.”</p></figcaption>
</figure>
</div>
</section>
{ad(0)}
<section id="senarai" aria-labelledby="h-senarai">
<h2 id="h-senarai">Zikir Dalam Tasbih Digital Ini & Dalilnya</h2>
{table(["Zikir", "Bacaan dan bilangan", "Rujukan"], tz_rows, "Senarai zikir dan rujukan hadis")}
</section>

<section id="cara" aria-labelledby="h-cara">
<div class="prose">
<h2 id="h-cara">Cara Menggunakan Tasbih Digital</h2>
<ol class="steps">
<li><strong>Pilih zikir</strong> di atas. Pilihan “Selepas solat” beralih sendiri dari Subhanallah ke Alhamdulillah, Allahu Akbar dan tahlil.</li>
<li><strong>Ketik butang bulat</strong> (atau tekan Enter/Space pada papan kekunci). Telefon bergetar sedikit pada setiap kiraan dan lebih panjang apabila sasaran dicapai.</li>
<li><strong>Tersilap tekan?</strong> Gunakan “Tolak 1”. “Set semula” memulakan pusingan baharu tanpa memadam jumlah hari ini.</li>
<li><strong>Zikir panjang:</strong> hidupkan “Skrin kekal hidup” supaya skrin tidak gelap ketika berzikir.</li>
<li><strong>Pasang ke skrin utama</strong> (butang Install atau menu pelayar) untuk membukanya seperti aplikasi, termasuk tanpa internet.</li>
</ol>
</div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Tasbih & Zikir</h2>
{faq_html(tfaq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel">
<h2 id="h-rel">Alat Al-Quran Lain</h2>
{tool_cards("tasbih-digital/")}
</section>
</div>
{side([("kira", "Tasbih digital"), ("h-jwp", "Tasbih selepas solat"), ("senarai", "Zikir & dalil"), ("cara", "Cara guna"), ("faq", "Soalan lazim")], "tasbih-digital/")}
</div>'''
    pages.append(dict(
        path="tasbih-digital/", kind="tool", data=False, arabic=True,
        extra_data=f'<script type="application/json" id="zd">{json.dumps(zd, ensure_ascii=False, separators=(",", ":"))}</script>',
        title="Tasbih Digital Online: Kira Zikir & Tasbih Selepas Solat",
        ogtitle="Tasbih Digital Online – Kira Zikir 33·33·33",
        desc="Tasbih digital percuma untuk kira zikir di telefon: Subhanallah, Alhamdulillah, Allahu Akbar 33 kali, istighfar & selawat 100 kali. Getar, kiraan disimpan.",
        crumbs=[("Alat", "alat/"), ("Tasbih Digital", None)], body=body, faq=tfaq,
        app=dict(name="Tasbih Digital Online", features=["Tasbih selepas solat 33·33·33·1 automatik", "Istighfar, selawat dan zikir 100 kali", "Sasaran kiraan sendiri", "Getaran pada setiap kiraan", "Kiraan harian disimpan", "Skrin kekal hidup", "Berfungsi tanpa internet"]),
        about=["Tasbih", "Zikir", "Dhikr"],
        llms="Tasbih digital (pengira zikir) dalam pelayar: tasbih selepas solat (Subhanallah 33, Alhamdulillah 33, Allahu Akbar 33, kemudian tahlil 1 = 100; HR Muslim 597), istighfar 100 (HR Muslim 2702), Subhanallahi wa bihamdih 100 (HR Al-Bukhari 6405, Muslim 2691), selawat 100, dan sasaran sendiri. Getaran, kiraan disimpan dalam localStorage, berfungsi tanpa internet.",
    ))

    # ---------------- cari ayat ----------------
    TOPICS = [
        ("sabar", "Ayat Al-Quran Tentang Sabar & Ujian", [(2, 153), (2, 286), (94, 5), (94, 6)]),
        ("rezeki", "Ayat Al-Quran Tentang Rezeki & Tawakal", [(65, 3), (11, 6)]),
        ("ibu-bapa", "Ayat Al-Quran Tentang Ibu Bapa", [(17, 23), (17, 24), (31, 14)]),
        ("taubat", "Ayat Al-Quran Tentang Taubat & Keampunan", [(39, 53), (66, 8)]),
        ("doa", "Ayat Al-Quran Tentang Doa", [(2, 186), (40, 60), (2, 201)]),
        ("syukur", "Ayat Al-Quran Tentang Syukur & Ketenangan Hati", [(14, 7), (13, 28), (2, 152)]),
        ("keluarga", "Ayat Al-Quran Tentang Suami Isteri & Keluarga", [(30, 21), (25, 74)]),
        ("solat", "Ayat Al-Quran Tentang Solat", [(29, 45), (2, 45)]),
        ("ilmu", "Ayat Al-Quran Tentang Ilmu", [(20, 114), (96, 1), (58, 11)]),
        ("al-quran", "Ayat Tentang Kelebihan Al-Quran", [(17, 82), (54, 17), (35, 29)]),
    ]
    tsec = []
    for slug, h, refs in TOPICS:
        cards = []
        for s, a in refs:
            v = ayat(s, a)
            cards.append(f'<li><p class="cref"><a href="/#surah-{s}-ayat-{a}">{e(P.NAMES[s - 1])} {s}:{a}</a></p>'
                         f'<p class="car" lang="ar" dir="rtl">{e(v["arabic"])}</p><p>{e(v["translation"])}</p></li>')
        tsec.append(f'<section id="{slug}" aria-labelledby="h-{slug}"><h3 id="h-{slug}">{e(h)}</h3><ul class="hits">{"".join(cards)}</ul></section>')
    chips = [("sabar", "Sabar"), ("rezeki", "Rezeki"), ("ibu bapa", "Ibu bapa"), ("ampun", "Ampun"), ("doa", "Doa"), ("syukur", "Syukur"),
             ("sembahyang", "Solat (sembahyang)"), ("syurga", "Syurga"), ("isteri", "Isteri"), ("2:255", "Ayat Kursi 2:255")]
    cfaq = [
        ("Bagaimana cara mencari ayat Al-Quran mengikut topik?",
         "Taip kata kunci dalam Bahasa Melayu, contohnya “sabar”, “rezeki” atau “ibu bapa”. Alat ini menyemak terjemahan Melayu bagi kesemua 6,236 ayat dan memaparkan setiap ayat yang mengandungi semua perkataan yang ditaip, berserta pautan untuk membaca dan mendengar ayat tersebut."),
        ("Bagaimana mencari ayat menggunakan nombor surah dan ayat?",
         "Taip nombor surah dan ayat dipisahkan dengan titik bertindih atau ruang, contohnya 2:255 untuk Ayat Kursi atau 36 12 untuk Surah Yasin ayat 12."),
        ("Kenapa carian “solat” memberi sedikit hasil?",
         "Terjemahan yang digunakan memakai istilah lama seperti “sembahyang” bagi solat. Cuba sinonim atau ejaan lain: sembahyang, ampun atau taubat, zakat, syurga, neraka, rezeki."),
        ("Ayat Kursi ialah surah dan ayat ke berapa?",
         "Ayat Kursi ialah Surah Al-Baqarah ayat 255, di dalam Juz 3. Taip 2:255 dalam kotak carian untuk memaparkannya."),
        ("Terjemahan Al-Quran mana yang digunakan?",
         "Terjemahan Bahasa Melayu Abdullah Muhammad Basmeih, sebagaimana diterbitkan oleh AlQuran Cloud, yang sama digunakan dalam pembaca Al-Quran di laman ini. Terjemahan ialah kefahaman makna; rujuk tafsir muktabar untuk huraian lanjut."),
        ("Bolehkah saya mencari dalam teks Arab?",
         "Buat masa ini carian dibuat pada terjemahan Bahasa Melayu. Selepas menemui ayat, klik “Baca & dengar” untuk melihat teks Arab, bacaan Rumi dan mendengar audio qari."),
    ]
    body = hero("Cari Ayat Al-Quran Ikut Kata Kunci & Topik",
                "Cari dalam terjemahan Bahasa Melayu bagi 6,236 ayat: taip kata kunci seperti sabar, rezeki atau ibu bapa, atau nombor ayat seperti 2:255.",
                [("Alat", "alat/"), ("Cari Ayat", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira" class="sr">Carian ayat Al-Quran</h2>
<form class="frm one" id="cf" role="search" novalidate>
<div class="fl"><label for="cq">Kata kunci atau nombor ayat</label><input id="cq" type="search" inputmode="search" autocomplete="off" enterkeyhint="search" placeholder="Contoh: sabar, rezeki, 2:255"></div>
</form>
<div class="chips2" role="group" aria-label="Carian popular">{"".join(f'<button type="button" data-q="{e(q)}">{e(l)}</button>' for q, l in chips)}</div>
<p class="cnt" id="cstat" role="status"></p>
<ol class="hits" id="cres"></ol>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp">Cara Mencari Ayat Al-Quran Dengan Pantas</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Taip satu atau dua kata kunci Bahasa Melayu (contohnya <em>sabar</em> atau <em>ibu bapa</em>) untuk mencari dalam terjemahan kesemua 6,236 ayat, atau taip <em>surah:ayat</em> (contohnya <strong>2:255</strong> untuk Ayat Kursi). Terjemahan ini memakai istilah lama, jadi cuba juga <em>sembahyang</em> bagi solat.</p></div>
{meta_line(T, TMS)}
{share(SITE + "cari-ayat-al-quran/", "Cari ayat Al-Quran ikut topik dalam Bahasa Melayu:")}
</div>
</section>
{ad(0)}
<section id="topik" aria-labelledby="h-topik">
<h2 id="h-topik">Ayat Al-Quran Mengikut Topik Popular</h2>
<p>Teks Arab dan terjemahan di bawah diambil terus daripada data Al-Quran yang sama digunakan dalam pembaca. Klik rujukan untuk mendengar bacaan qari.</p>
{"".join(tsec)}
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Mencari Ayat Al-Quran</h2>
{faq_html(cfaq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel">
<h2 id="h-rel">Alat Al-Quran Lain</h2>
{tool_cards("cari-ayat-al-quran/")}
</section>
</div>
{side([("kira", "Carian ayat"), ("h-jwp", "Cara mencari")] + [(s, h.replace("Ayat Al-Quran Tentang ", "").replace("Ayat Tentang ", "")) for s, h, _ in TOPICS] + [("faq", "Soalan lazim")], "cari-ayat-al-quran/")}
</div>'''
    pages.append(dict(
        path="cari-ayat-al-quran/", kind="tool", data=True, arabic=True,
        title="Cari Ayat Al-Quran Ikut Kata Kunci & Topik (Bahasa Melayu)",
        ogtitle="Cari Ayat Al-Quran Ikut Topik – Terjemahan Melayu",
        desc="Cari ayat Al-Quran ikut kata kunci atau topik (sabar, rezeki, ibu bapa, taubat) dalam terjemahan Melayu 6,236 ayat, atau ikut nombor ayat. Terus baca & dengar.",
        crumbs=[("Alat", "alat/"), ("Cari Ayat Al-Quran", None)], body=body, faq=cfaq,
        app=dict(name="Carian Ayat Al-Quran (Bahasa Melayu)", features=["Carian kata kunci dalam terjemahan 6,236 ayat", "Carian ikut surah:ayat", "Topik popular: sabar, rezeki, ibu bapa, taubat, doa", "Pautan terus ke bacaan dan audio ayat"]),
        about=["Al-Quran", "Terjemahan Al-Quran Bahasa Melayu"],
        llms="Carian ayat Al-Quran dalam terjemahan Bahasa Melayu (Abdullah Muhammad Basmeih) bagi 6,236 ayat, mengikut kata kunci atau rujukan surah:ayat (contoh 2:255 Ayat Kursi). Halaman ini juga menyenaraikan ayat mengikut topik: sabar (2:153, 2:286, 94:5–6), rezeki (65:3, 11:6), ibu bapa (17:23–24, 31:14), taubat (39:53, 66:8), doa (2:186, 40:60, 2:201), syukur (14:7, 13:28, 2:152), keluarga (30:21, 25:74), solat (29:45, 2:45), ilmu (20:114, 96:1, 58:11), kelebihan Al-Quran (17:82, 54:17, 35:29).",
    ))

    # ---------------- juzuk ----------------
    jrows, counts = [], []
    for j in range(1, 31):
        g1, g2 = P.JS[j - 1], P.JS[j] - 1
        (s1, a1), (s2, a2) = P.sa(g1), P.sa(g2)
        p1, p2 = P.page_of(g1), P.page_of(g2)
        n = g2 - g1 + 1
        counts.append(n)
        sur = e(P.NAMES[s1 - 1]) if s1 == s2 else f"{e(P.NAMES[s1 - 1])} – {e(P.NAMES[s2 - 1])} ({s2 - s1 + 1} surah)"
        jrows.append([f'<strong id="juz-{j}">Juz {j}</strong>',
                      f'<a href="/#surah-{s1}-ayat-{a1}">{e(P.NAMES[s1 - 1])} {s1}:{a1}</a><span class="jar" lang="ar" dir="rtl">{e(arab(s1, a1, 3))}</span>',
                      f"{e(P.NAMES[s2 - 1])} {s2}:{a2}", f"{p1}–{p2}", P.num(n), sur])
    jmax, jmin = counts.index(max(counts)) + 1, counts.index(min(counts)) + 1
    sj = []
    for i, (s, a) in enumerate(P.META["sajda"], 1):
        g = P.gid(s, a)
        j = max(k for k in range(1, 31) if P.JS[k - 1] <= g)
        note = {(38, 24): "Sajdah syukur menurut mazhab Syafi'i (bukan sajdah tilawah); sajdah tilawah menurut mazhab Hanafi",
                (22, 77): "Sajdah kedua Surah Al-Hajj: sajdah tilawah menurut mazhab Syafi'i, tidak menurut mazhab Hanafi"}.get((s, a), "Sajdah tilawah")
        sj.append([str(i), sref(s, a), f"Juz {j}", f"{P.page_of(g)}", e(note)])
    jfaq = [
        ("Juz 30 bermula dengan surah apa?",
         f"Juz 30 (Juz 'Amma) bermula dengan Surah An-Naba' ayat 1 dan berakhir dengan Surah An-Nas. Ia mengandungi 37 surah, 564 ayat, pada muka surat 582 hingga 604 Mushaf Madinah."),
        ("Berapa juzuk dalam Al-Quran dan berapa muka surat setiap juz?",
         "Al-Quran mempunyai 30 juzuk, 114 surah dan 6,236 ayat (kiraan Kufah, riwayat Hafs). Dalam Mushaf Madinah 604 muka surat, setiap juz kira-kira 20 muka surat; Juz 1 ialah 21 muka surat dan Juz 30 ialah 23 muka surat."),
        ("Surah Yasin terletak dalam juz berapa?",
         "Surah Yasin bermula dalam Juz 22 (ayat 1 hingga 27) dan bersambung ke Juz 23 (ayat 28 hingga 83)."),
        ("Surah Al-Kahfi terletak dalam juz berapa?",
         "Surah Al-Kahfi bermula dalam Juz 15 (ayat 1 hingga 74) dan bersambung ke Juz 16 (ayat 75 hingga 110)."),
        ("Berapa banyak ayat sajdah dalam Al-Quran?",
         "Terdapat 15 tempat sajdah dalam mushaf. Menurut mazhab Syafi'i, 14 daripadanya ialah sajdah tilawah, manakala Surah Sad ayat 24 ialah sajdah syukur yang tidak dilakukan dalam solat."),
        ("Juz mana yang mempunyai ayat paling banyak?",
         f"Juz {jmax} mempunyai ayat paling banyak ({P.num(max(counts))} ayat) kerana surah-surahnya pendek, manakala Juz {jmin} mempunyai paling sedikit ({min(counts)} ayat). Panjang setiap juz hampir sama dari segi muka surat, iaitu kira-kira 20 muka surat."),
        ("Apakah itu manzil dalam Al-Quran?",
         "Manzil ialah pembahagian Al-Quran kepada 7 bahagian untuk khatam dalam seminggu, bermula di Al-Fatihah, Al-Ma'idah, Yunus, Al-Isra', Asy-Syu'ara', As-Saffat dan Qaf (singkatan “fami bisyauqin”)."),
    ]
    j30 = "".join(f'<li><a href="/#surah-{s}">{s}. {e(P.NAMES[s - 1])}</a></li>' for s in range(78, 115))
    body = hero("Senarai 30 Juzuk Al-Quran: Surah & Ayat Permulaan Setiap Juz",
                "Rujukan lengkap 30 juz: surah dan ayat mula serta tamat, muka surat Mushaf Madinah, bilangan ayat, 15 ayat sajdah dan 7 manzil.",
                [("Alat", "alat/"), ("Senarai Juzuk", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Al-Quran dibahagikan kepada <strong>30 juzuk</strong> yang hampir sama panjang (kira-kira 20 muka surat setiap satu). Juz 1 bermula dengan Surah Al-Fatihah, <strong>Juz 30 bermula dengan Surah An-Naba' ayat 1</strong> dan berakhir dengan Surah An-Nas. Setiap juz dibahagi kepada 2 hizb dan 8 rubu' (suku hizb).</p></div>
{meta_line(T, TMS)}
{share(SITE + "senarai-juzuk-al-quran/", "Senarai 30 juzuk Al-Quran – surah & ayat mula setiap juz:")}
</div>
</section>

<section id="senarai" aria-labelledby="h-senarai">
<h2 id="h-senarai">📚 Jadual 30 Juzuk Al-Quran</h2>
{table(["Juz", "Mula", "Tamat", "Muka surat", "Ayat", "Surah"], jrows, "Senarai 30 juzuk Al-Quran", "jz")}
<p class="note">Muka surat mengikut Mushaf Madinah 15 baris (604 muka surat). Klik rujukan “Mula” untuk membaca dan mendengar juz tersebut. Gunakan <a href="/jadual-khatam-al-quran/">Jadual Khatam</a> untuk membahagikan juzuk mengikut hari.</p>
</section>
{ad(0)}
<section id="juz-30-surah" aria-labelledby="h-j30">
<h2 id="h-j30">Senarai 37 Surah Dalam Juz 30 (Juz 'Amma)</h2>
<ol class="j30">{j30}</ol>
</section>

<section id="sajdah" aria-labelledby="h-sajdah">
<div class="prose">
<h2 id="h-sajdah">15 Ayat Sajdah Dalam Al-Quran</h2>
<p>Apabila membaca atau mendengar ayat sajdah, disunatkan sujud tilawah. Dalam mazhab Syafi'i, sajdah tilawah berjumlah 14; Surah Sad ayat 24 dikira sajdah syukur yang dilakukan di luar solat.</p>
</div>
{table(["No.", "Surah:ayat", "Juz", "Muka surat", "Catatan"], sj, "Senarai 15 ayat sajdah", "")}
</section>

<section id="manzil" aria-labelledby="h-manzil">
<div class="prose">
<h2 id="h-manzil">7 Manzil Untuk Khatam Seminggu</h2>
<p>Permulaan manzil: <strong>Al-Fatihah (1), Al-Ma'idah (5), Yunus (10), Al-Isra' (17), Asy-Syu'ara' (26), As-Saffat (37) dan Qaf (50)</strong>, diingati dengan singkatan “fami bisyauqin”. Jadual muka surat lengkap ada dalam <a href="/jadual-khatam-al-quran/#manzil">Jadual Khatam</a>.</p>
</div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Juzuk Al-Quran</h2>
{faq_html(jfaq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel">
<h2 id="h-rel">Alat Al-Quran Lain</h2>
{tool_cards("senarai-juzuk-al-quran/")}
</section>
</div>
{side([("senarai", "Jadual 30 juzuk"), ("juz-30-surah", "Surah Juz 30"), ("sajdah", "15 ayat sajdah"), ("manzil", "7 manzil"), ("faq", "Soalan lazim")], "senarai-juzuk-al-quran/")}
</div>'''
    jitems = [{"@type": "ListItem", "position": j, "name": f"Juz {j}", "url": f"{SITE}senarai-juzuk-al-quran/#juz-{j}"} for j in range(1, 31)]
    pages.append(dict(
        path="senarai-juzuk-al-quran/", kind="ref", data=False, arabic=True,
        title="Senarai 30 Juzuk Al-Quran: Surah & Ayat Mula Setiap Juz",
        ogtitle="Senarai 30 Juzuk Al-Quran – Surah & Ayat Setiap Juz",
        desc="Senarai lengkap 30 juzuk Al-Quran: surah dan ayat permulaan serta penamat setiap juz, muka surat Mushaf Madinah, bilangan ayat, 15 ayat sajdah dan 7 manzil.",
        crumbs=[("Alat", "alat/"), ("Senarai 30 Juzuk Al-Quran", None)], body=body, faq=jfaq,
        itemlist=dict(name="30 Juzuk Al-Quran", items=jitems),
        about=["Juz (Al-Quran)", "Sujud tilawah", "Al-Quran"],
        llms="Senarai 30 juzuk Al-Quran dengan surah:ayat mula dan tamat, muka surat Mushaf Madinah dan bilangan ayat. Juz 30 bermula An-Naba' 78:1, 37 surah, 564 ayat, muka surat 582–604. Yasin: Juz 22 (ayat 1–27) dan Juz 23 (28–83). Al-Kahfi: Juz 15 (1–74) dan Juz 16 (75–110). 15 tempat sajdah; mazhab Syafi'i: 14 sajdah tilawah, Sad 38:24 sajdah syukur. 7 manzil bermula 1, 5, 10, 17, 26, 37, 50.",
    ))

    # ---------------- alat hub ----------------
    body = hero("Alat Al-Quran & Islamik Percuma",
                "Alat ringkas untuk membaca, mengkhatam, menghafal dan berzikir. Semuanya percuma, tanpa daftar akaun, dan berfungsi di telefon walaupun tanpa internet.",
                [("Alat", None)])
    tbb = "".join(f'<li><a href="{TBB}{p}" rel="noopener">{e(n)} ↗</a></li>' for p, n in TBB_TOOLS)
    body += f'''<div class="wrap mn pg1"><div class="ct">
<section aria-labelledby="h-alat">
<h2 id="h-alat">Alat Al-Quran</h2>
{tool_cards(None, "tcards big")}
{meta_line(T, TMS)}
</section>
<section aria-labelledby="h-kenapa">
<div class="prose">
<h2 id="h-kenapa">Kenapa Alat Ini Berbeza</h2>
<ul>
<li><strong>Dikira daripada data sebenar mushaf:</strong> muka surat, juzuk dan ayat dipetakan kepada Mushaf Madinah 604 muka surat, bukan anggaran purata.</li>
<li><strong>Bersambung terus ke bacaan:</strong> setiap rujukan surah dan ayat membuka pembaca dengan teks Arab, Rumi, terjemahan dan audio 5 qari.</li>
<li><strong>Privasi:</strong> tiada akaun dan tiada borang. Kiraan tasbih dan tanda khatam disimpan dalam pelayar anda sendiri.</li>
<li><strong>Ringan dan pantas:</strong> tanpa aplikasi berat; pasang ke skrin utama dan guna tanpa internet.</li>
</ul>
</div>
</section>
{ad(0)}
<section aria-labelledby="h-lain">
<div class="prose">
<h2 id="h-lain">Kalkulator Islamik Lain</h2>
<p>Untuk zakat, faraid, fidyah dan kompas kiblat, gunakan kalkulator rakan kami di The Bukit Besi Tools:</p>
</div>
<ul class="rel">{tbb}</ul>
</section>
</div></div>'''
    pages.append(dict(
        path="alat/", kind="hub", data=False, arabic=False,
        title="Alat Al-Quran & Islamik Percuma: Ramadan, Solat, Iqra', Tajwid",
        ogtitle="Alat Al-Quran & Islamik Percuma",
        desc="Alat Al-Quran & Islamik percuma: waktu berbuka puasa, waktu solat, cara solat, belajar mengaji, Iqra', tajwid, jadual khatam, hafazan dan tasbih. Tanpa akaun.",
        crumbs=[("Alat", None)], body=body, faq=[],
        itemlist=dict(name="Alat Al-Quran", items=[{"@type": "ListItem", "position": i + 1, "name": n, "url": SITE + p} for i, (p, _, n, _) in enumerate(TOOLS)]),
        about=["Al-Quran"], schema="CollectionPage",
        llms="Direktori alat Al-Quran dan Islamik percuma: waktu berbuka puasa dan imsak Ramadan, waktu solat, cara solat, belajar mengaji (huruf hijaiyah), latihan Iqra' 1–6, belajar tajwid, doa, zikir, jadual khatam, jadual hafazan, tasbih digital, carian ayat dan senarai 30 juzuk.",
    ))

    # ---------------- tentang ----------------
    body = hero("Tentang Al-Quran Online", "Siapa kami, sumber data yang kami gunakan dan bagaimana setiap halaman disemak.", [("Tentang Kami", None)])
    body += f'''<div class="wrap mn pg1"><div class="ct prose">
{meta_line(T, TMS)}
<h2 id="siapa">Siapa Kami</h2>
<p><strong>Al-Quran Online</strong> (quran.ilmualam.com) ialah projek <a href="{MAIN}">The Ilmu Alam</a>, laman ilmu Islam berbahasa Melayu yang menerbitkan artikel surah, doa, zikir dan panduan ibadah sejak 2020. Laman ini dibina dan diselenggara oleh pasukan editorial yang sama di Malaysia.</p>
<p>Moto kami: <em>Ilmu Tanpa Sempadan, Amal Tanpa Batasan, Akhirat Jua Pengakhiran.</em></p>

<h2 id="misi">Misi</h2>
<p>Memudahkan setiap Muslim penutur Bahasa Melayu membaca, mendengar, memahami dan menghafal Al-Quran di mana-mana peranti, secara percuma, tanpa akaun, dan tanpa aplikasi berat. Laman ini dibina supaya pantas dibuka walaupun dengan talian perlahan, dan boleh digunakan tanpa internet selepas lawatan pertama.</p>

<h2 id="kandungan">Apa Yang Ada Di Laman Ini</h2>
<ul>
<li><a href="/">Pembaca Al-Quran</a>: 114 surah, 6,236 ayat, teks Arab, bacaan Rumi, terjemahan Bahasa Melayu dan audio 5 qari.</li>
<li><a href="/jadual-khatam-al-quran/">Jadual Khatam</a>, <a href="/jadual-hafazan-al-quran/">Jadual Hafazan</a>, <a href="/tasbih-digital/">Tasbih Digital</a>, <a href="/cari-ayat-al-quran/">Cari Ayat</a> dan <a href="/senarai-juzuk-al-quran/">Senarai 30 Juzuk</a>.</li>
<li>Artikel huraian setiap surah di <a href="{MAIN}">ilmualam.com</a>.</li>
</ul>

<h2 id="sumber">Sumber Data</h2>
<div class="tw" tabindex="0" role="region" aria-label="Sumber data"><table>
<thead><tr><th scope="col">Data</th><th scope="col">Sumber</th></tr></thead>
<tbody>
<tr><td>Teks Arab (Rasm Uthmani) dan terjemahan Melayu</td><td>Teks Uthmani dan terjemahan Abdullah Muhammad Basmeih, sebagaimana diterbitkan oleh <a href="https://alquran.cloud/" rel="noopener">AlQuran Cloud</a></td></tr>
<tr><td>Audio bacaan ayat demi ayat</td><td><a href="https://everyayah.com/" rel="noopener">EveryAyah.com</a> (Alafasy, As-Sudais, Al-Husary, Abdul Basit, Al-Ghamadi)</td></tr>
<tr><td>Sempadan muka surat, juzuk, sajdah dan manzil</td><td>Data Tanzil bagi Mushaf Madinah melalui <a href="https://github.com/quran-center/quran-meta" rel="noopener">quran-meta</a> (lesen MIT)</td></tr>
<tr><td>Fon Arab</td><td><a href="https://www.amirifont.org/" rel="noopener">Amiri</a> oleh Khaled Hosny (SIL Open Font License 1.1)</td></tr>
<tr><td>Hadis yang dipetik</td><td>Kitab hadis muktabar dengan nombor hadis dinyatakan (Al-Bukhari, Muslim, Abu Daud, At-Tirmizi)</td></tr>
</tbody></table></div>

<h2 id="semakan">Cara Kami Menyemak Kandungan</h2>
<ol class="steps">
<li><strong>Data dahulu.</strong> Jumlah ayat setiap surah disemak secara automatik setiap kali laman dibina; binaan gagal jika jumlah bukan 6,236 ayat.</li>
<li><strong>Kiraan diuji.</strong> Jadual khatam dan hafazan dikira dengan dua pelaksanaan berasingan (semasa binaan dan dalam pelayar) dan diuji supaya hasilnya sama.</li>
<li><strong>Dalil berrujukan.</strong> Setiap hadis yang dipetik disertakan nama kitab dan nombor hadis supaya pembaca boleh menyemak sendiri.</li>
<li><strong>Bukan fatwa.</strong> Bagi isu yang ada khilaf, kami nyatakan pandangan mazhab Syafi'i sebagai amalan majoriti di Malaysia, dan menyarankan rujukan kepada mufti negeri atau JAKIM.</li>
<li><strong>Pembetulan.</strong> Laporan kesilapan disemak dan dibetulkan; tarikh “Dikemas kini” pada halaman berkenaan diubah.</li>
</ol>

<h2 id="dana">Pembiayaan & Iklan</h2>
<p>Laman ini percuma. Kos penyelenggaraan mungkin ditampung oleh iklan Google AdSense. Iklan tidak sekali-kali dipaparkan di dalam paparan ayat Al-Quran, dan pengiklan tidak mempengaruhi kandungan. Lihat <a href="/dasar-privasi.html">Dasar Privasi</a> dan <a href="/terma-penggunaan/">Terma Penggunaan</a>.</p>

<h2 id="kod">Sumber Terbuka</h2>
<p>Kod laman ini terbuka di <a href="https://github.com/ilmualam/quran" rel="noopener">GitHub</a>. Anda boleh menyemak cara data dipaparkan dan dikira.</p>

<h2 id="hubungi">Hubungi Kami</h2>
<p>Jumpa kesilapan teks, terjemahan atau kiraan? Ada cadangan alat baharu? <a href="/hubungi-kami/">Hubungi kami</a>.</p>
</div></div>'''
    pages.append(dict(path="tentang-kami/", kind="info", schema="AboutPage", data=False, arabic=False,
                      title="Tentang Kami – Al-Quran Online oleh The Ilmu Alam",
                      ogtitle="Tentang Al-Quran Online (Ilmu Alam)",
                      desc="Kenali Al-Quran Online oleh The Ilmu Alam: misi, sumber teks dan terjemahan, audio qari, cara kami menyemak kandungan dan dasar pembetulan.",
                      crumbs=[("Tentang Kami", None)], body=body, faq=[], about=["The Ilmu Alam"],
                      llms="Tentang laman: projek The Ilmu Alam (ilmualam.com, sejak 2020), sumber data (AlQuran Cloud, EveryAyah.com, Tanzil/quran-meta, Amiri), proses semakan dan dasar pembetulan."))

    # ---------------- hubungi ----------------
    body = hero("Hubungi Kami", "Laporkan kesilapan, cadangkan alat baharu atau bertanya tentang kerjasama.", [("Hubungi Kami", None)])
    body += f'''<div class="wrap mn pg1"><div class="ct prose">
{meta_line(T, TMS)}
<div class="box"><p><strong>Cara paling cepat:</strong> gunakan <a href="{MAIN}p/contact.html">borang hubungi di ilmualam.com</a>. Borang itu meliputi laman Al-Quran Online ini juga.</p></div>
<p><a class="btn3" href="{MAIN}p/contact.html">✉️ Buka borang hubungi</a></p>

<h2 id="kesilapan">Laporkan Kesilapan Teks, Terjemahan atau Audio</h2>
<p>Kami amat menghargai laporan kesilapan kerana ia melibatkan kalam Allah. Sertakan:</p>
<ul>
<li>pautan halaman atau rujukan ayat (contohnya <code>quran.ilmualam.com/#surah-36-ayat-12</code> atau 36:12);</li>
<li>apa yang salah (teks Arab, Rumi, terjemahan, audio atau kiraan jadual);</li>
<li>sumber rujukan jika ada (contohnya mushaf bercetak yang disahkan).</li>
</ul>
<p>Laporan yang disahkan akan dibetulkan dan tarikh “Dikemas kini” halaman berkenaan diubah. Lihat <a href="/tentang-kami/#semakan">cara kami menyemak kandungan</a>.</p>

<h2 id="cadangan">Cadangkan Alat Baharu</h2>
<p>Beritahu kami alat Al-Quran atau ibadah yang anda perlukan dan untuk siapa (diri sendiri, anak-anak, kelas tahfiz, surau). Cadangan yang paling banyak diminta akan dibina dahulu.</p>

<h2 id="kerjasama">Kerjasama, Masjid & Sekolah</h2>
<p>Masjid, surau, sekolah dan kelas tahfiz dipersilakan berkongsi pautan laman ini. Untuk kerjasama kandungan atau pengiklanan, gunakan borang yang sama. Iklan tidak dipaparkan di dalam paparan ayat Al-Quran.</p>

<h2 id="sosial">Media Sosial</h2>
<ul>
<li><a href="https://www.facebook.com/ilmualam" rel="noopener me">Facebook: Ilmu Alam</a></li>
<li><a href="https://twitter.com/ilmualam" rel="noopener me">X: @ilmualam</a></li>
<li><a href="https://www.youtube.com/@theilmualam" rel="noopener me">YouTube: @theilmualam</a></li>
<li><a href="https://ilmualam.bsky.social/" rel="noopener me">Bluesky: ilmualam.bsky.social</a></li>
</ul>

<h2 id="sebelum">Sebelum Menghubungi</h2>
<p>Banyak soalan sudah dijawab dalam <a href="/#faq">Soalan Lazim</a>. Untuk persoalan hukum peribadi, sila rujuk mufti negeri, JAKIM atau asatizah bertauliah kerana kami tidak mengeluarkan fatwa.</p>
</div></div>'''
    pages.append(dict(path="hubungi-kami/", kind="info", schema="ContactPage", data=False, arabic=False,
                      title="Hubungi Kami – Al-Quran Online (The Ilmu Alam)",
                      ogtitle="Hubungi Al-Quran Online (Ilmu Alam)",
                      desc="Hubungi Al-Quran Online oleh The Ilmu Alam untuk melaporkan kesilapan teks, terjemahan atau audio, mencadangkan alat baharu, atau kerjasama.",
                      crumbs=[("Hubungi Kami", None)], body=body, faq=[], about=["The Ilmu Alam"],
                      llms="Hubungi: borang di ilmualam.com/p/contact.html untuk laporan kesilapan, cadangan alat dan kerjasama."))

    # ---------------- terma ----------------
    body = hero("Terma Penggunaan & Penafian", "Syarat menggunakan Al-Quran Online dan alat-alatnya.", [("Terma Penggunaan", None)])
    body += f'''<div class="wrap mn pg1"><div class="ct prose">
<p class="meta2">Berkuat kuasa: <time datetime="{T}">{TMS}</time> · Terpakai bagi quran.ilmualam.com, dikendalikan oleh <a href="{MAIN}">The Ilmu Alam</a>.</p>
<div class="box"><p><strong>Ringkasan:</strong> Laman ini percuma untuk kegunaan peribadi, pendidikan dan ibadah. Sentiasa rujuk mushaf bercetak yang disahkan untuk kepastian teks. Kandungan hukum ialah maklumat umum, bukan fatwa. Hasil kalkulator ialah panduan perancangan.</p></div>

<h2 id="penerimaan">1. Penerimaan Terma</h2>
<p>Dengan menggunakan laman ini, anda bersetuju dengan terma ini dan <a href="/dasar-privasi.html">Dasar Privasi</a> kami. Jika tidak bersetuju, sila hentikan penggunaan.</p>

<h2 id="penggunaan">2. Penggunaan Yang Dibenarkan</h2>
<ul>
<li>Membaca, mendengar, mencetak jadual dan berkongsi pautan untuk tujuan peribadi, keluarga, pendidikan, masjid dan surau.</li>
<li>Memaut ke mana-mana halaman, termasuk pautan terus ke ayat (contohnya <code>/#surah-36-ayat-1</code>).</li>
<li>Tidak dibenarkan: menyalin kandungan artikel atau halaman secara pukal ke laman lain, mengubah teks Al-Quran, menggunakan laman ini untuk tujuan yang menghina agama, atau mengganggu operasi laman (contohnya permintaan automatik berlebihan).</li>
</ul>

<h2 id="quran">3. Teks Al-Quran, Rumi, Terjemahan & Audio</h2>
<ul>
<li>Teks Arab, terjemahan dan audio dipaparkan seadanya daripada sumber yang dinyatakan dalam halaman <a href="/tentang-kami/#sumber">Tentang Kami</a>. Kami berusaha memastikan ketepatan, namun sentiasa rujuk mushaf bercetak yang disahkan oleh pihak berkuasa agama.</li>
<li>Bacaan Rumi ialah alat bantu sebutan sahaja dan tidak menggantikan pembelajaran tajwid secara bertalaqqi dengan guru.</li>
<li>Terjemahan ialah kefahaman makna dan bukan Al-Quran itu sendiri.</li>
<li>Hak cipta terjemahan, audio dan fon kekal milik pemilik masing-masing.</li>
</ul>

<h2 id="alat">4. Alat & Kalkulator</h2>
<p>Jadual khatam, jadual hafazan, kiraan tasbih dan carian ayat disediakan sebagai panduan. Nombor muka surat mengikut Mushaf Madinah 604 muka surat dan mungkin berbeza dengan cetakan lain. Kiraan disimpan dalam pelayar anda dan boleh hilang jika data pelayar dikosongkan.</p>

<h2 id="penafian">5. Penafian</h2>
<ul>
<li>Kandungan berkaitan hukum ialah maklumat umum untuk pendidikan dan <strong>bukan fatwa</strong>. Untuk keputusan bagi keadaan peribadi, rujuk mufti negeri, JAKIM atau asatizah bertauliah.</li>
<li>Laman ini disediakan “seadanya” tanpa sebarang jaminan, termasuk jaminan bahawa ia sentiasa tersedia atau bebas daripada kesilapan.</li>
<li>Kami tidak bertanggungjawab atas sebarang kerugian akibat penggunaan laman ini, atau gangguan perkhidmatan pihak ketiga seperti audio.</li>
</ul>

<h2 id="harta">6. Harta Intelek</h2>
<p>Reka bentuk, teks asal dan susun atur laman ini © The Ilmu Alam. Kod sumber laman tersedia di <a href="https://github.com/ilmualam/quran" rel="noopener">GitHub</a> di bawah lesen MIT kecuali dinyatakan sebaliknya. Al-Quran ialah kalam Allah; hak cipta terjemahan, audio dan fon kekal milik pemilik masing-masing.</p>

<h2 id="luar">7. Pautan Luar & Iklan</h2>
<p>Laman ini mengandungi pautan ke laman lain (contohnya ilmualam.com dan The Bukit Besi Tools) dan mungkin memaparkan iklan Google AdSense. Kami tidak bertanggungjawab atas kandungan laman luar. Iklan tidak dipaparkan di dalam paparan ayat Al-Quran.</p>

<h2 id="undang">8. Undang-undang</h2>
<p>Terma ini ditadbir oleh undang-undang Malaysia.</p>

<h2 id="perubahan">9. Perubahan Terma</h2>
<p>Terma ini mungkin dikemas kini dari semasa ke semasa; tarikh berkuat kuasa di atas akan diubah. Penggunaan berterusan selepas perubahan bermakna anda menerima terma baharu.</p>

<h2 id="hubungi">10. Hubungi</h2>
<p>Pertanyaan tentang terma ini: <a href="/hubungi-kami/">Hubungi Kami</a>.</p>
</div></div>'''
    pages.append(dict(path="terma-penggunaan/", kind="info", data=False, arabic=False,
                      title="Terma Penggunaan & Penafian – Al-Quran Online",
                      ogtitle="Terma Penggunaan & Penafian – Al-Quran Online",
                      desc="Terma penggunaan dan penafian Al-Quran Online (quran.ilmualam.com): penggunaan dibenarkan, ketepatan teks dan terjemahan, alat kalkulator, bukan fatwa.",
                      crumbs=[("Terma Penggunaan", None)], body=body, faq=[], about=["Terma penggunaan"],
                      llms="Terma penggunaan dan penafian: kegunaan peribadi/pendidikan, rujuk mushaf bercetak, kandungan hukum bukan fatwa, undang-undang Malaysia."))
    return pages
