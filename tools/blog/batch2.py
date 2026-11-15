"""Batch 2 (surah & ayat): 10 refreshed www.ilmualam.com posts, plus 5 duplicate posts merged into them (MERGES).
Hadith gradings match the Quran site (tools/pages15.py SURAH) so the two sites never contradict each other.
Run from tools/blog: PYTHONPATH=.. python3 batch2.py"""
import json
import ibadah as I
from gen import build, card, qcard, table, write, e, Q, OUT
from cards import card as img

H = {d[0]: d for d in I.DOA_HARIAN}
ZP = {z[0]: z for z in I.Z_PAGI_PETANG}
W = "https://www.ilmualam.com/"
YASIN = W + "2020/01/kelebihan-surah-yasin-dan-fadhilat.html"
DHUHA = W + "2017/12/bagaimana-surah-ad-dhuha-boleh-mengubah.html"
RUQYAH = W + "2020/02/tanda-tanda-gangguan-jin-sihir.html"
IKHLAS = W + "2018/02/ini-lah-9-waktu-yang-dianjurkan-membaca.html"
YUNUS = W + "2018/02/doa-nabi-yunus-amalkan-agar-bebas-dari.html"
SERIBU = W + "2020/01/kelebihan-ayat-seribu-dinar.html"
WAQIAH = W + "2018/02/amalan-wirid-membaca-surat-waqiah-3-x.html"
BACA_YASIN = W + "2020/05/surah-yassin.html"


def ul(*items, ordered=False):
    tag = "ol" if ordered else "ul"
    return f"<{tag}>" + "".join(f"<li>{x}</li>" for x in items) + f"</{tag}>"


def ref(t):
    return f" <em>({t})</em>"


def hd(P, key, note=""):
    _, t, ar, ru, mn, src = H[key]
    return card(P, t, e(ar), ru, e(mn), e(src), note)


def zp(P, key, note=""):
    i, t, ar, ru, mn, n, src, nt = ZP[key]
    return card(P, t, e(ar), ru, e(mn), e(src), note or nt)


def grade(rows):
    """[(claim, source, status)] -> table with a coloured status column."""
    return table(["Fadhilat yang disebut", "Sumber", "Status"], [[e(c), e(s), st] for c, s, st in rows])


SAHIH, HASAN, DHAIF = "✅ Sahih", "✅ Hasan", "⚠️ Dhaif"


def base(**k):
    k.setdefault("badges", ["Teks Al-Quran Uthmani", "Status Hadis Dinyatakan", "Dikemas kini 2026"])
    k.setdefault("disclaimer", "Hadis dhaif disebut bersama statusnya. Ulama membenarkan beramal dengan hadis dhaif dalam fadhilat amal dengan syarat ia tidak terlalu lemah dan tidak diyakini sebagai sabda Nabi SAW yang pasti.")
    return k


POSTS = []

# 1 ---------------------------------------------------------------- Yasin
P = "ilmx-ys"
POSTS.append(("kelebihan-yasin", base(
    ns=P, url=YASIN, published="2020-01-10", pubms="10 Januari 2020",
    title="Kelebihan Surah Yasin: Fadhilat, Status Hadis & Ayat 58",
    desc="Kelebihan Surah Yasin dengan status setiap hadis, kandungan 83 ayat, amalan membaca Yasin di Malaysia dan maksud ayat 58 (Salamun qaulan min rabbir rahim).",
    h1="Kelebihan Surah Yasin & Status Hadisnya", img=img("kelebihan-surah-yasin", "Kelebihan Surah", "Kelebihan Surah Yasin", "Fadhilat, status hadis dan maksud ayat 58", "سُورَةُ يٰسٓ"),
    alt="Kelebihan Surah Yasin dan status hadisnya", refshort="Sunan At-Tirmizi, Abu Daud, Sahih Ibn Hibban",
    lead="Fadhilat Surah Yasin yang sering disebut, dinilai satu per satu mengikut status hadisnya, kandungan surah, amalan di Malaysia dan maksud ayat 58.",
    crumb=("Al-Quran", W + "search/label/Al-Quran"), about=["Surah Yasin", "Kelebihan surah"],
    answer="Surah Yasin (surah ke-36, 83 ayat) ialah surah Makkiyyah tentang kerasulan, tanda kekuasaan Allah dan hari kebangkitan. Hadis yang menyebutnya “hati Al-Quran” <em>(HR At-Tirmizi, no. 2887)</em> "
           "dinilai <strong>dhaif</strong> oleh ramai ulama hadis, dan hadis membacanya kepada orang yang hampir meninggal <em>(HR Abu Daud, no. 3121)</em> diperselisihkan statusnya. "
           "Membaca Yasin tetap <strong>berpahala besar</strong> seperti membaca mana-mana surah: setiap huruf satu kebaikan <em>(HR At-Tirmizi, no. 2910)</em>.",
    sections=[
        ("kandungan", "Kandungan Surah Yasin",
         table(["Ayat", "Tema"], [["1–12", "Sumpah dengan Al-Quran, kebenaran risalah Nabi Muhammad SAW, orang yang menolak peringatan"],
                                  ["13–32", "Kisah penduduk sebuah negeri (ashab al-qaryah), tiga utusan dan lelaki yang datang dari hujung kota"],
                                  ["33–50", "Tanda kekuasaan Allah: bumi yang mati dihidupkan, malam dan siang, matahari dan bulan, bahtera"],
                                  ["51–68", "Tiupan sangkakala, kebangkitan, nikmat ahli syurga dan kehinaan orang yang berdosa"],
                                  ["69–83", "Al-Quran bukan syair, nikmat binatang ternakan, dan bukti kebangkitan: “Kun fayakun”"]])
         + f'<p>Bacaan penuh 83 ayat dengan Rumi dan audio: <a href="{BACA_YASIN}">Surah Yasin Rumi & Jawi</a> atau <a href="{Q}surah-yasin/">Surah Yasin di Al-Quran Online</a>.</p>'),
        ("fadhilat", "Fadhilat Surah Yasin dan Status Hadisnya",
         grade([("Yasin ialah hati Al-Quran", "HR At-Tirmizi, no. 2887; At-Tirmizi sendiri menyebutnya gharib", DHAIF),
                ("Bacakan Yasin kepada orang yang hampir meninggal dunia", "HR Abu Daud, no. 3121; Ibn Majah, no. 1448; disahihkan Ibn Hibban, didhaifkan ramai ulama", DHAIF),
                ("Sesiapa membaca Yasin pada malam hari kerana mencari reda Allah, diampunkan dosanya", "HR Ibn Hibban, no. 2574; sanadnya diperselisihkan", DHAIF),
                ("Setiap huruf Al-Quran yang dibaca diberi satu kebaikan, dan satu kebaikan digandakan sepuluh", "HR At-Tirmizi, no. 2910", SAHIH)])
         + f'<div class="{P}-box amber">Kesimpulan: tiada hadis sahih yang menyebut fadhilat khusus Surah Yasin, tetapi ganjaran membaca Al-Quran secara umum sangat besar. Amalan membaca Yasin pada malam Jumaat dan majlis tahlil di Malaysia <strong>harus</strong>, '
           "asalkan tidak diyakini sebagai kewajipan atau sunnah khusus daripada Nabi SAW.</div>"),
        ("ayat58", "Yasin Ayat 58: Maksud dan Amalan Hajat",
         qcard(P, "Yasin 36:58", 36, 58, 58, "Surah Yasin, ayat 58")
         + "<p>Ayat ini menggambarkan <strong>salam penghormatan daripada Allah</strong> kepada ahli syurga. Ia sering diamalkan secara berulang untuk memohon hajat dan ketenangan. "
           "Amalan ini berasal daripada ijazah sebahagian guru, <strong>bukan daripada hadis</strong>; ia boleh dibaca sebagai zikir dan wasilah doa, tanpa beriktikad bilangan atau fadhilat tertentu ditetapkan oleh Nabi SAW.</p>"),
        ("pilihan", "Ayat-ayat Pilihan dan Pengajarannya",
         qcard(P, "Yasin 36:12: setiap amal dicatat", 36, 12, 12, "Surah Yasin, ayat 12")
         + "<p>Ayat 12 mengingatkan bahawa bukan sahaja amal yang dicatat, tetapi juga <strong>kesan</strong> yang ditinggalkan: ilmu yang diajar, sedekah jariah dan contoh yang diikuti orang lain.</p>"
         + qcard(P, "Yasin 36:65: mulut dikunci, anggota bersaksi", 36, 65, 65, "Surah Yasin, ayat 65")
         + "<p>Pada hari kiamat, mulut tidak lagi dapat berdalih; tangan dan kaki menjadi saksi. Ayat ini mendidik kita menjaga anggota daripada maksiat walaupun tiada siapa melihat.</p>"
         + qcard(P, "Yasin 36:82: Kun fayakun", 36, 82, 82, "Surah Yasin, ayat 82")
         + "<p>Apabila Allah menghendaki sesuatu, Dia hanya berfirman “Jadilah!”, maka jadilah ia. Ayat ini menenangkan orang yang berdoa: tiada hajat yang terlalu sukar bagi Allah.</p>"
         + table(["Ayat", "Pengajaran ringkas"], [["20–27", "Lelaki dari hujung kota berani menyampaikan kebenaran; selepas syahid dia berharap kaumnya mengetahui keampunan yang diterimanya"],
                                                  ["38–40", "Matahari, bulan, malam dan siang beredar mengikut ketetapan: tanda keteraturan ciptaan"],
                                                  ["77–79", "Manusia yang dicipta daripada setitis air menjadi pembantah; Allah yang mencipta kali pertama mampu menghidupkan semula"]])),
        ("amalan", "Amalan Membaca Yasin di Malaysia",
         table(["Amalan", "Hukum"], [["Membaca Yasin pada malam Jumaat", "Harus; malam Jumaat ialah malam yang mulia untuk ibadah. Surah Al-Kahfi pula ada hadis khusus untuk hari Jumaat."],
                                    ["Membaca Yasin dalam majlis tahlil", "Harus menurut pandangan ulama Syafi'i yang membolehkan pahala bacaan dihadiahkan"],
                                    ["Membaca Yasin di sisi orang yang nazak", "Diamalkan ramai ulama Syafi'i berdasarkan HR Abu Daud 3121 walaupun statusnya diperselisihkan"],
                                    ["Mewajibkan Yasin atau menganggap ibadah lain tidak sah tanpanya", "Tidak betul"]])
         + f'<p>Untuk tahlil lengkap dengan nama arwah, guna <a href="{Q}tahlil-ringkas/">Tahlil Ringkas</a>.</p>'),
    ],
    faq=[("Apakah kelebihan Surah Yasin?", "Membacanya berpahala seperti membaca Al-Quran secara umum, setiap huruf satu kebaikan (HR At-Tirmizi 2910). Hadis yang menyebut fadhilat khusus Yasin, seperti “hati Al-Quran”, dinilai dhaif oleh ramai ulama hadis."),
         ("Adakah hadis Yasin hati Al-Quran sahih?", "Tidak. Ia riwayat At-Tirmizi (2887) yang dinilai gharib oleh At-Tirmizi sendiri dan dhaif oleh ramai ulama hadis."),
         ("Apakah maksud Yasin ayat 58?", "“(Mereka diberi ucapan) salam daripada Tuhan Yang Maha Pengasih.” Ia salam penghormatan Allah kepada ahli syurga."),
         ("Bolehkah membaca Yasin pada malam Jumaat?", "Boleh dan berpahala. Tiada hadis sahih yang mengkhususkannya, maka jangan menganggapnya kewajipan. Surah Al-Kahfi pula ada hadis khusus untuk hari Jumaat.")],
    refs=["Sunan At-Tirmizi, no. 2887, 2910.", "Sunan Abu Daud, no. 3121; Sunan Ibn Majah, no. 1448.", "Sahih Ibn Hibban, no. 2574.", "Teks Al-Quran: rasm Uthmani; terjemahan Abdullah Muhammad Basmeih."],
    related=[(BACA_YASIN, "Surah Yasin Rumi & Jawi", "Bacaan penuh 83 ayat dengan audio"), (Q + "surah-yasin/", "Surah Yasin di Al-Quran Online", "Arab, Rumi, terjemahan dan audio 5 qari"),
             (Q + "tahlil-ringkas/", "Tahlil Ringkas", "Bacaan tahlil dengan nama arwah")])))

# 2 ---------------------------------------------------------------- Al-Insyirah
P = "ilmx-in"
POSTS.append(("al-insyirah", base(
    ns=P, url=W + "2018/01/subhanallah-inilah-8-kelebihan.html", published="2018-01-30", pubms="30 Januari 2018",
    title="Surah Al-Insyirah: Maksud, Tafsir Ringkas & Pengajaran",
    desc="Surah Al-Insyirah (Alam Nasyrah): teks Arab dan maksud, tafsir ringkas setiap ayat, makna “bersama kesulitan ada kemudahan” dan status kelebihan yang tersebar.",
    h1="Surah Al-Insyirah: Maksud & Pengajaran", img=img("surah-al-insyirah", "Tadabbur Surah", "Surah Al-Insyirah", "Bersama kesulitan ada kemudahan: tafsir ringkas & pengajaran", "أَلَمْ نَشْرَحْ"),
    alt="Surah Al-Insyirah: maksud, tafsir ringkas dan pengajaran", refshort="Al-Quran, tafsir muktabar",
    lead="Surah lapan ayat yang diturunkan untuk melapangkan dada Rasulullah SAW. Maksud setiap ayat, makna janji kemudahan, dan cara menjadikannya bekal ketika susah.",
    crumb=("Al-Quran", W + "search/label/Al-Quran"), about=["Surah Al-Insyirah", "Tafsir"],
    answer="Surah Al-Insyirah (Alam Nasyrah) ialah surah ke-94, 8 ayat, Makkiyyah. Allah mengingatkan Rasulullah SAW tentang dada yang dilapangkan dan beban yang diangkat, lalu berjanji dua kali: "
           "<strong>“Sesungguhnya bersama kesulitan ada kemudahan”</strong> (ayat 5–6). Tiada hadis sahih tentang fadhilat khusus surah ini; kelebihannya ialah pada <strong>maknanya</strong>, yang menjadi penenang ketika susah.",
    sections=[
        ("bacaan", "Bacaan Surah Al-Insyirah", qcard(P, "Surah Al-Insyirah (94:1–8)", 94, 1, 8, f'Teks Uthmani &amp; terjemahan Abdullah Basmeih · <a href="{Q}surah-al-insyirah/">Rumi &amp; audio</a>')),
        ("tafsir", "Tafsir Ringkas Ayat demi Ayat",
         table(["Ayat", "Maksud ringkas"], [["1–3", "Allah melapangkan dada Nabi SAW untuk menerima wahyu dan mengangkat beban yang memberatkan belakangnya"],
                                            ["4", "Allah meninggikan sebutan nama Baginda: disebut dalam azan, iqamah, syahadah dan tahiyat"],
                                            ["5–6", "Janji diulang dua kali: bersama setiap kesulitan ada kemudahan"],
                                            ["7–8", "Apabila selesai satu urusan, teruskan dengan ibadah dan usaha lain, dan hanya kepada Allah berharap"]])
         + "<p>Ulama menjelaskan “al-'usr” (kesulitan) disebut dengan alif lam pada kedua-dua ayat, menunjukkan kesulitan yang sama, manakala “yusra” (kemudahan) disebut tanpa alif lam, menunjukkan kemudahan yang berbeza. "
           "Dari sini lahir ungkapan masyhur “satu kesulitan tidak akan mengalahkan dua kemudahan”, yang diriwayatkan daripada sahabat dan tabi'in; riwayatnya secara marfu' kepada Nabi SAW dinilai dhaif.</p>"),
        ("pengajaran", "Pengajaran untuk Kehidupan",
         ul("Setiap kesusahan bersifat sementara; kemudahan datang <strong>bersama</strong> kesulitan, bukan hanya selepasnya.",
            "Ingat nikmat yang sudah Allah berikan sebelum mengeluh tentang yang belum ada.",
            "Jangan berehat dalam kelalaian: selesai kerja dunia, teruskan dengan ibadah; selesai satu ibadah, mulakan yang lain.",
            "Letakkan harapan sepenuhnya kepada Allah, bukan kepada manusia.")),
        ("status", "Status “Kelebihan” yang Tersebar",
         table(["Dakwaan", "Status"], [["Membaca Al-Insyirah melapangkan dada dan menghilangkan kesedihan", "Maknanya benar berdasarkan isi surah; tiada hadis khusus tentang bilangan bacaan"],
                                       ["Membaca 7, 41 atau 100 kali untuk rezeki atau hajat tertentu", "Tiada asas daripada hadis; amalan sesetengah guru"],
                                       ["Dibaca dalam solat sunat", "Boleh seperti surah lain; tiada sunnah khusus"]])
         + f'<p>Doa ketika resah yang sahih: lihat <a href="{Q}doa-hilangkan-resah/">doa hilangkan resah</a>.</p>'),
    ],
    faq=[("Apakah maksud surah Al-Insyirah?", "Allah melapangkan dada Nabi SAW, mengangkat bebannya, meninggikan namanya, dan berjanji bahawa bersama kesulitan ada kemudahan; maka teruslah berusaha dan berharap kepada Allah."),
         ("Berapa ayat surah Al-Insyirah?", "Lapan ayat. Ia surah ke-94 dalam Al-Quran dan tergolong dalam Juz 'Amma."),
         ("Apakah maksud fa inna ma'al 'usri yusra?", "“Maka sesungguhnya bersama kesulitan ada kemudahan.” Janji ini diulang dua kali dalam ayat 5 dan 6."),
         ("Adakah kelebihan khusus membaca surah Al-Insyirah?", "Tiada hadis sahih tentang fadhilat khusus. Kelebihannya terletak pada maknanya yang menenangkan dan mendorong untuk terus berusaha.")],
    refs=["Al-Quran: Al-Insyirah 94:1–8.", "Tafsir Ibn Kathir dan Tafsir Al-Qurtubi, Surah Al-Insyirah.", "Teks Al-Quran: rasm Uthmani; terjemahan Abdullah Muhammad Basmeih."],
    related=[(Q + "surah-al-insyirah/", "Surah Al-Insyirah di Al-Quran Online", "Arab, Rumi, terjemahan dan audio"), (DHUHA, "Surah Ad-Dhuha untuk Hati yang Gundah", "Asbabun nuzul dan pengajaran"),
             (Q + "doa-hilangkan-resah/", "Doa Hilangkan Resah", "Doa sahih ketika gelisah dan bersedih")])))

# 3 ---------------------------------------------------------------- Al-Ikhlas: 9 waktu
P = "ilmx-ik"
POSTS.append(("waktu-al-ikhlas", base(
    ns=P, url=IKHLAS, published="2019-12-18", pubms="18 Disember 2019",
    title="9 Waktu Membaca Surah Al-Ikhlas Menurut Sunnah (Dengan Dalil)",
    desc="Bilakah sunat membaca Surah Al-Ikhlas: sebelum tidur, pagi dan petang, selepas solat, dalam solat sunat Subuh, witir, tawaf dan ruqyah, dengan hadis sahih.",
    h1="9 Waktu Membaca Surah Al-Ikhlas Menurut Sunnah", img=img("waktu-membaca-al-ikhlas", "Amalan Sunnah", "9 Waktu Membaca Surah Al-Ikhlas", "Setiap waktu dengan dalil hadis sahih", "سُورَةُ الْإِخْلَاصِ"),
    alt="Waktu-waktu membaca Surah Al-Ikhlas menurut sunnah", refshort="Sahih Al-Bukhari & Muslim, Sunan Abu Daud & At-Tirmizi",
    lead="Surah yang menyamai sepertiga Al-Quran, dan sembilan waktu Rasulullah SAW membacanya, masing-masing dengan dalil.",
    crumb=("Al-Quran", W + "search/label/Al-Quran"), about=["Surah Al-Ikhlas", "Amalan sunnah"],
    answer="Surah Al-Ikhlas <strong>menyamai sepertiga Al-Quran</strong> <em>(HR Al-Bukhari, no. 5013; Muslim, no. 811)</em>. Rasulullah SAW membacanya <strong>sebelum tidur, pagi dan petang, selepas solat fardu, "
           "dalam solat sunat sebelum Subuh, dalam witir, selepas tawaf dan ketika meruqyah diri</strong>. Ini sembilan waktu yang thabit dalam hadis.",
    sections=[
        ("bacaan", "Bacaan Surah Al-Ikhlas", qcard(P, "Surah Al-Ikhlas (112:1–4)", 112, 1, 4, f'<a href="{Q}surah-al-ikhlas/">Rumi &amp; audio</a>')),
        ("tafsir", "Asbabun Nuzul dan Tafsir Ringkas",
         "<p>Diriwayatkan bahawa golongan musyrikin meminta Nabi SAW menerangkan “keturunan” Tuhannya, lalu Allah menurunkan surah ini" + ref("HR At-Tirmizi, no. 3364; dinilai hasan oleh sebahagian ulama") + ".</p>"
         + table(["Ayat", "Maksud", "Inti tauhid"], [["1", "Katakanlah: Dialah Allah Yang Maha Esa", "Allah satu pada zat, sifat dan perbuatan-Nya"],
                                                     ["2", "Allah tempat bergantung segala sesuatu (As-Samad)", "Semua makhluk berhajat kepada-Nya; Dia tidak berhajat kepada sesiapa"],
                                                     ["3", "Dia tidak beranak dan tidak diperanakkan", "Menolak kepercayaan bahawa Tuhan mempunyai anak atau asal-usul"],
                                                     ["4", "Dan tiada sesuatu pun yang setara dengan-Nya", "Tiada yang menyerupai Allah dalam apa jua bentuk"]])
         + "<p>Surah ini juga dinamakan <strong>At-Tauhid</strong>, <strong>Al-Asas</strong> dan <strong>Al-Ma'rifah</strong> oleh sebahagian ulama kerana ia merumuskan asas akidah.</p>"),
        ("waktu", "9 Waktu Membaca Al-Ikhlas",
         table(["#", "Waktu", "Cara", "Dalil"], [
             ["1", "Sebelum tidur", "Baca 3 Qul, tiup ke tapak tangan, sapu badan (3 kali)", "HR Al-Bukhari, no. 5017"],
             ["2", "Pagi dan petang", "Baca 3 Qul tiga kali", "HR Abu Daud, no. 5082; At-Tirmizi, no. 3575"],
             ["3", "Selepas setiap solat fardu", "Baca Al-Ikhlas, Al-Falaq dan An-Nas", "HR Abu Daud, no. 1523"],
             ["4", "Rakaat kedua solat sunat sebelum Subuh", "Rakaat pertama Al-Kafirun, kedua Al-Ikhlas", "HR Muslim, no. 726"],
             ["5", "Solat sunat selepas Maghrib", "Al-Kafirun dan Al-Ikhlas", "HR At-Tirmizi, no. 431"],
             ["6", "Rakaat terakhir solat witir", "Al-Ikhlas, Al-Falaq dan An-Nas", "HR Abu Daud, no. 1424; At-Tirmizi, no. 463"],
             ["7", "Solat sunat tawaf", "Al-Kafirun dan Al-Ikhlas", "HR Muslim, no. 1218"],
             ["8", "Ketika sakit (ruqyah diri)", "Baca 3 Qul, tiup ke tapak tangan dan sapu badan", "HR Al-Bukhari, no. 5016; Muslim, no. 2192"],
             ["9", "Bila-bila masa", "Berpahala menyamai sepertiga Al-Quran", "HR Al-Bukhari, no. 5013"]])
         + f'<p>Senarai zikir lengkap dengan kaunter: <a href="{Q}zikir-pagi-petang/">Zikir Pagi & Petang</a> dan <a href="{Q}doa-sebelum-tidur/">Amalan Sebelum Tidur</a>.</p>'),
        ("kelebihan", "Kelebihan Surah Al-Ikhlas",
         ul("<strong>Sepertiga Al-Quran.</strong> “Demi yang jiwaku di tangan-Nya, sesungguhnya ia menyamai sepertiga Al-Quran.”" + ref("HR Al-Bukhari, no. 5013"),
            "<strong>Cinta kepadanya membawa ke syurga.</strong> Seorang sahabat sentiasa membacanya dalam solat kerana mencintainya; Nabi SAW bersabda: “Kecintaanmu kepadanya memasukkan kamu ke syurga.”" + ref("HR Al-Bukhari, no. 774 (ta'liq); At-Tirmizi, no. 2901"),
            "<strong>Dicintai Allah.</strong> Seorang imam yang sentiasa menutup bacaannya dengan Al-Ikhlas kerana ia sifat Ar-Rahman; Nabi SAW bersabda: “Khabarkan kepadanya bahawa Allah mencintainya.”" + ref("HR Al-Bukhari, no. 7375; Muslim, no. 813"),
            "Membaca 10 kali dibina istana di syurga: diriwayatkan oleh Ahmad, <strong>sanadnya dhaif</strong>; boleh diamalkan sebagai fadhilat tanpa diyakini pasti.")
         + "<p>Membaca Al-Ikhlas tiga kali tidak menggantikan kewajipan khatam atau membaca Al-Quran; “menyamai sepertiga” ialah dari segi pahala dan kandungan tauhid, bukan pengganti bacaan.</p>"),
    ],
    faq=[("Bilakah waktu sunat membaca Surah Al-Ikhlas?", "Sebelum tidur, pagi dan petang, selepas solat fardu, dalam solat sunat Subuh dan Maghrib, witir, solat sunat tawaf dan ketika meruqyah diri, setiap satu dengan dalil hadis."),
         ("Adakah membaca Al-Ikhlas 3 kali sama dengan khatam Al-Quran?", "Dari segi pahala, Al-Ikhlas menyamai sepertiga Al-Quran (HR Al-Bukhari 5013), tetapi ia tidak menggantikan bacaan dan tadabbur seluruh Al-Quran."),
         ("Kenapa Al-Ikhlas menyamai sepertiga Al-Quran?", "Ulama menjelaskan Al-Quran mengandungi tiga tema besar: hukum, kisah dan tauhid. Al-Ikhlas merangkumi tauhid sepenuhnya."),
         ("Berapa kali membaca Al-Ikhlas sebelum tidur?", "Tiga Qul dibaca, ditiup ke tapak tangan dan disapu ke badan, diulang tiga kali (HR Al-Bukhari 5017).")],
    refs=["Sahih Al-Bukhari, no. 774, 5013, 5016, 5017, 7375.", "Sahih Muslim, no. 726, 811, 813, 1218, 2192.", "Sunan Abu Daud, no. 1424, 1523, 5082; Sunan At-Tirmizi, no. 431, 463, 2901, 3575."],
    related=[(Q + "surah-al-ikhlas/", "Surah Al-Ikhlas di Al-Quran Online", "Arab, Rumi, terjemahan dan audio"), (Q + "zikir-pagi-petang/", "Zikir Pagi & Petang", "Dengan kaunter dan rujukan hadis"),
             (RUQYAH, "Ruqyah Syar'iyyah", "Ayat dan doa pendinding daripada sunnah")])))

# 4 ---------------------------------------------------------------- Ad-Dhuha (3 posts merged)
P = "ilmx-dh"
POSTS.append(("ad-dhuha", base(
    ns=P, url=DHUHA, published="2017-12-04", pubms="4 Disember 2017",
    title="Surah Ad-Dhuha: Maksud, Asbabun Nuzul & Penawar Hati yang Gundah",
    desc="Surah Ad-Dhuha: teks Arab dan maksud, asbabun nuzul ketika wahyu terhenti, tafsir ringkas, pengajaran untuk hati yang gundah dan status amalan yang tersebar.",
    h1="Surah Ad-Dhuha: Penawar Hati yang Gundah", img=img("surah-ad-dhuha", "Tadabbur Surah", "Surah Ad-Dhuha", "Asbabun nuzul, maksud dan pengajaran untuk hati yang gundah", "وَالضُّحَىٰ"),
    alt="Surah Ad-Dhuha: maksud, asbabun nuzul dan pengajaran", refshort="Sahih Al-Bukhari & Muslim, tafsir muktabar",
    lead="Surah yang diturunkan ketika Rasulullah SAW berasa ditinggalkan. Kisah turunnya, maksud 11 ayatnya, dan cara menjadikannya penawar ketika jiwa resah.",
    crumb=("Al-Quran", W + "search/label/Al-Quran"), about=["Surah Ad-Dhuha", "Tafsir", "Ketenangan jiwa"],
    answer="Surah Ad-Dhuha (surah ke-93, 11 ayat) turun ketika wahyu terhenti beberapa hari dan seorang wanita mengejek bahawa Nabi SAW telah ditinggalkan <em>(HR Al-Bukhari, no. 4950; Muslim, no. 1797)</em>. "
           "Allah menjawab: <strong>“Tuhanmu tidak meninggalkanmu dan tidak membencimu”</strong>, mengingatkan nikmat yang lalu, dan memerintahkan berbuat baik kepada anak yatim dan peminta. "
           "Ia surah yang sangat sesuai dibaca dan ditadabbur ketika jiwa resah.",
    sections=[
        ("bacaan", "Bacaan Surah Ad-Dhuha", qcard(P, "Surah Ad-Dhuha (93:1–11)", 93, 1, 11, f'<a href="{Q}surah-ad-duha/">Rumi &amp; audio</a>')),
        ("nuzul", "Asbabun Nuzul: Ketika Wahyu Terhenti",
         "<p>Jundub bin Sufyan RA meriwayatkan: Rasulullah SAW sakit lalu tidak bangun (untuk qiamullail) satu atau dua malam. Seorang wanita datang dan berkata, “Wahai Muhammad, aku lihat syaitanmu telah meninggalkanmu.” "
         "Lalu Allah menurunkan: “Demi waktu dhuha, dan demi malam apabila sunyi, Tuhanmu tidak meninggalkanmu dan tidak membencimu.”" + ref("HR Al-Bukhari, no. 4950; Muslim, no. 1797") + "</p>"),
        ("tafsir", "Maksud dan Pengajaran Setiap Bahagian",
         table(["Ayat", "Maksud", "Pengajaran"], [
             ["1–3", "Sumpah dengan waktu dhuha dan malam; Allah tidak meninggalkan Nabi-Nya", "Kesunyian dan ujian bukan tanda Allah membenci kita"],
             ["4–5", "Akhirat lebih baik daripada dunia; Allah akan memberi sehingga engkau reda", "Fokus kepada pengakhiran; pemberian Allah datang pada waktunya"],
             ["6–8", "Bukankah Dia mendapatimu yatim lalu melindungi, bingung lalu memberi petunjuk, kekurangan lalu mencukupkan?", "Ingat nikmat yang lalu untuk yakin dengan pertolongan akan datang"],
             ["9–10", "Jangan berlaku keras kepada anak yatim dan jangan mengherdik peminta", "Syukur dibuktikan dengan berbuat baik kepada yang lemah"],
             ["11", "Dan nikmat Tuhanmu, hendaklah engkau sebut-sebutkan", "Ceritakan nikmat sebagai syukur, bukan untuk berbangga"]])),
        ("pasangan", "Ad-Dhuha dan Al-Insyirah: Dua Surah Berpasangan",
         "<p>Ad-Dhuha (surah ke-93) dan Al-Insyirah (surah ke-94) diturunkan dalam suasana yang sama dan saling melengkapi. Ad-Dhuha menegaskan bahawa Allah <strong>tidak meninggalkan</strong> Nabi-Nya "
         "dan mengingatkan nikmat yang lalu; Al-Insyirah pula menyambung dengan nikmat dada yang dilapangkan dan janji “bersama kesulitan ada kemudahan”. Membaca kedua-duanya bersama memberi gambaran lengkap: "
         f'Allah tidak meninggalkan kita, dan setiap kesulitan ada kemudahannya. Baca juga <a href="{W}2018/01/subhanallah-inilah-8-kelebihan.html">Surah Al-Insyirah</a>.</p>'),
        ("doa", "Doa Sahih Ketika Sedih dan Gundah", hd(P, "dukacita", "Doa yang sering dibaca Rasulullah SAW; baca selepas mentadabbur Ad-Dhuha.")),
        ("penawar", "Ad-Dhuha Sebagai Penawar Hati",
         ul("Baca perlahan-lahan dan fahami maksudnya, terutama ayat 3 dan 5, ketika berasa ditinggalkan atau putus asa.",
            "Senaraikan tiga nikmat yang Allah pernah berikan semasa susah (mengikut ayat 6–8).", "Lakukan satu kebaikan kepada anak yatim atau orang yang meminta (ayat 9–10).",
            "Jika gundah berpanjangan hingga mengganggu tidur, makan atau kerja, dapatkan juga bantuan kaunselor atau doktor; ikhtiar perubatan tidak bercanggah dengan tawakal.")
         + f'<div class="{P}-box amber"><strong>Status amalan yang tersebar:</strong> dakwaan bahawa membaca 11 ayat Ad-Dhuha “merawat jiwa kacau” dengan bilangan tertentu tiada asas daripada hadis. '
           "Manfaatnya datang daripada tadabbur makna, zikir dan doa, bukan formula bilangan.</div>"
         + f'<p>Ramai juga membaca Ad-Dhuha dalam rakaat kedua <a href="{Q}solat-sunat/solat-dhuha/">solat sunat Dhuha</a>; ini amalan masyarakat, dan surah lain juga sah.</p>'),
    ],
    faq=[("Apakah asbabun nuzul Surah Ad-Dhuha?", "Wahyu terhenti beberapa hari ketika Nabi SAW sakit, lalu seorang wanita mengejek bahawa Baginda telah ditinggalkan. Allah menurunkan Ad-Dhuha sebagai jawapan (HR Al-Bukhari 4950; Muslim 1797)."),
         ("Berapa ayat Surah Ad-Dhuha?", "Sebelas ayat. Ia surah ke-93, Makkiyyah, dalam Juz 'Amma."),
         ("Adakah Surah Ad-Dhuha boleh menghilangkan kesedihan?", "Maknanya sangat menenangkan kerana Allah menegaskan Dia tidak meninggalkan hamba-Nya. Tiada hadis tentang bilangan bacaan khusus; manfaatnya melalui tadabbur, zikir dan doa."),
         ("Adakah wajib membaca Ad-Dhuha dalam solat Dhuha?", "Tidak. Ia amalan masyarakat; solat Dhuha sah dengan mana-mana surah.")],
    refs=["Sahih Al-Bukhari, no. 4950; Sahih Muslim, no. 1797.", "Tafsir Ibn Kathir, Surah Ad-Dhuha.", "Teks Al-Quran: rasm Uthmani; terjemahan Abdullah Muhammad Basmeih."],
    related=[(Q + "surah-ad-duha/", "Surah Ad-Dhuha di Al-Quran Online", "Arab, Rumi, terjemahan dan audio"), (Q + "solat-sunat/solat-dhuha/", "Solat Dhuha: Cara & Waktu Hari Ini", "Niat, doa dan waktu ikut zon JAKIM"),
             (W + "2018/01/subhanallah-inilah-8-kelebihan.html", "Surah Al-Insyirah", "Bersama kesulitan ada kemudahan")])))

# 5 ---------------------------------------------------------------- Al-Waqiah & rezeki
P = "ilmx-wq"
POSTS.append(("al-waqiah", base(
    ns=P, url=WAQIAH, published="2018-02-03", pubms="3 Februari 2018",
    title="Surah Al-Waqiah & Rezeki: Status Hadis dan Amalan yang Betul",
    desc="Benarkah membaca Surah Al-Waqiah setiap malam menjauhkan kefakiran? Status hadisnya, kandungan surah dan amalan pembuka rezeki yang thabit dalam Al-Quran.",
    h1="Surah Al-Waqiah & Rezeki: Status dan Amalan Sahih", img=img("surah-al-waqiah-rezeki", "Kelebihan Surah", "Surah Al-Waqiah & Rezeki", "Status hadis dan amalan pembuka rezeki yang sahih", "سُورَةُ الْوَاقِعَةِ"),
    alt="Surah Al-Waqiah dan rezeki: status hadis dan amalan yang betul", refshort="Al-Quran, Sahih Al-Bukhari, Sunan At-Tirmizi, Syu'ab Al-Iman",
    lead="Penilaian jujur terhadap amalan Al-Waqiah untuk rezeki, kandungan surah tentang tiga golongan manusia, dan sebab-sebab rezeki yang disebut dengan jelas dalam Al-Quran.",
    crumb=("Amalan", W + "search/label/Amalan"), about=["Surah Al-Waqiah", "Rezeki"],
    answer="Hadis “sesiapa membaca Surah Al-Waqiah setiap malam tidak akan ditimpa kefakiran” diriwayatkan oleh Ibn As-Sunni dan Al-Baihaqi, dan <strong>dinilai dhaif oleh ramai ulama hadis</strong>; "
           "sebahagian ulama membenarkan beramal dengannya sebagai fadhilat. Amalan “3 kali sehari” pula <strong>tiada asas</strong>. Pembuka rezeki yang <strong>thabit</strong> ialah takwa, istighfar, "
           "tawakal, silaturahim dan sedekah.",
    sections=[
        ("status", "Status Hadis Al-Waqiah dan Kefakiran",
         grade([("Sesiapa membaca Surah Al-Waqiah setiap malam tidak akan ditimpa kefakiran", "Ibn As-Sunni; Al-Baihaqi dalam Syu'ab Al-Iman (daripada Ibn Mas'ud)", DHAIF),
                ("Membaca 3 kali sehari, atau 41 kali, untuk rezeki melimpah", "Tiada sumber hadis", "❌ Tiada asas")])
         + "<p>Membaca Al-Waqiah setiap malam tetap baik kerana ia bacaan Al-Quran yang berpahala dan mengingatkan tentang akhirat. Yang perlu dielakkan ialah meyakininya sebagai “formula” rezeki atau menetapkan bilangan atas nama sunnah.</p>"),
        ("kandungan", "Kandungan Surah Al-Waqiah",
         qcard(P, "Al-Waqiah 56:1–3", 56, 1, 3, f'<a href="{Q}surah-al-waqiah/">Bacaan penuh 96 ayat, Rumi &amp; audio</a>')
         + table(["Ayat", "Tema"], [["1–12", "Kiamat pasti berlaku; manusia terbahagi kepada tiga golongan"], ["13–40", "As-Sabiqun (yang terdahulu) dan Ashab Al-Yamin (golongan kanan) serta nikmat syurga"],
                                    ["41–56", "Ashab Asy-Syimal (golongan kiri) dan azab mereka"], ["57–74", "Bukti kekuasaan Allah: penciptaan manusia, tanaman, air dan api"],
                                    ["75–82", "Kemuliaan Al-Quran: tidak menyentuhnya kecuali yang disucikan"], ["83–96", "Saat sakaratul maut dan nasib ketiga-tiga golongan"]])),
        ("rezeki", "Pembuka Rezeki yang Thabit",
         table(["Amalan", "Dalil"], [["Takwa dan tawakal", "Ath-Thalaq 65:2–3; “Jika kamu bertawakal dengan sebenar-benarnya, kamu diberi rezeki seperti burung” (HR At-Tirmizi, no. 2344)"],
                                     ["Istighfar", "Nuh 71:10–12: istighfar menurunkan hujan, harta dan anak"], ["Silaturahim", "“Sesiapa ingin dilapangkan rezeki… hubungkanlah silaturahim” (HR Al-Bukhari, no. 5986)"],
                                     ["Sedekah", "“Sedekah tidak mengurangkan harta” (HR Muslim, no. 2588)"], ["Syukur", "Ibrahim 14:7: jika bersyukur, nikmat ditambah"],
                                     ["Berusaha dengan halal", "“Tiada makanan yang lebih baik daripada hasil usaha tangan sendiri” (HR Al-Bukhari, no. 2072)"]])
         + qcard(P, "Nuh 71:10–12: istighfar dan rezeki", 71, 10, 12, "Surah Nuh, ayat 10–12")),
    ],
    faq=[("Adakah hadis Al-Waqiah menjauhkan kefakiran sahih?", "Ia diriwayatkan oleh Ibn As-Sunni dan Al-Baihaqi dan dinilai dhaif oleh ramai ulama hadis. Sebahagian ulama membenarkan beramal dengannya sebagai fadhilat tanpa meyakininya pasti."),
         ("Bilakah waktu membaca Surah Al-Waqiah?", "Masyarakat biasa membacanya selepas Maghrib atau Isyak. Tiada waktu khusus yang ditetapkan oleh hadis sahih."),
         ("Apakah amalan pembuka rezeki yang sahih?", "Takwa dan tawakal (Ath-Thalaq 65:2–3), istighfar (Nuh 71:10–12), silaturahim (HR Al-Bukhari 5986), sedekah (HR Muslim 2588) dan syukur (Ibrahim 14:7)."),
         ("Berapa ayat Surah Al-Waqiah?", "96 ayat. Ia surah ke-56, Makkiyyah, dalam Juz 27.")],
    refs=["Al-Quran: Al-Waqiah 56; Ath-Thalaq 65:2–3; Nuh 71:10–12; Ibrahim 14:7.", "Sahih Al-Bukhari, no. 2072, 5986; Sahih Muslim, no. 2588; Sunan At-Tirmizi, no. 2344.",
          "Al-Baihaqi, Syu'ab Al-Iman; Ibn As-Sunni, 'Amal Al-Yaum wa Al-Lailah."],
    related=[(Q + "surah-al-waqiah/", "Surah Al-Waqiah di Al-Quran Online", "Bacaan penuh dengan audio"), (SERIBU, "Ayat Seribu Dinar", "Takwa dan tawakal sebagai jalan rezeki"),
             (Q + "doa-murah-rezeki/", "Doa Murah Rezeki", "Doa rezeki daripada hadis dan Al-Quran")])))

# 6 ---------------------------------------------------------------- At-Taubah 128-129
P = "ilmx-tb"
POSTS.append(("akhir-taubah", base(
    ns=P, url=W + "2018/02/rasai-manfaat-asalkan-istiqomah-amalkan.html", published="2018-02-03", pubms="3 Februari 2018",
    title="2 Ayat Terakhir Surah At-Taubah (128–129): Maksud & Amalan",
    desc="Dua ayat terakhir Surah At-Taubah (Laqad ja'akum rasulun dan Hasbiyallah): Arab dan maksud, kisah pengumpulannya, amalan 7 kali pagi petang dan statusnya.",
    h1="2 Ayat Terakhir Surah At-Taubah: Maksud & Amalan", img=img("akhir-surah-at-taubah", "Ayat Amalan", "2 Ayat Terakhir Surah At-Taubah", "Laqad ja'akum rasulun dan Hasbiyallah: maksud & amalan", "حَسْبِيَ اللّٰهُ"),
    alt="Dua ayat terakhir Surah At-Taubah: maksud dan amalan", refshort="Al-Quran, Sahih Al-Bukhari, Sunan Abu Daud",
    lead="Ayat yang menggambarkan kasih Rasulullah SAW kepada umatnya dan kalimah tawakal Hasbiyallah, dengan kisah bagaimana ia ditemui ketika Al-Quran dikumpulkan.",
    crumb=("Amalan", W + "search/label/Amalan"), about=["Surah At-Taubah", "Hasbiyallah", "Tawakal"],
    answer="Dua ayat terakhir At-Taubah (9:128–129) menyebut Rasul yang sangat berat melihat kesusahan umatnya dan kalimah tawakal <strong>“Hasbiyallahu la ilaha illa huwa, 'alaihi tawakkaltu wa huwa rabbul-'arsyil-'azim”</strong>. "
           "Riwayat membaca “Hasbiyallah…” <strong>7 kali pagi dan petang</strong> supaya dicukupkan urusan <em>(HR Abu Daud, no. 5081)</em> ialah perkataan sahabat Abu Ad-Darda' (mauquf), dan sanadnya dipertikai; "
           "ia diamalkan sebagai zikir tawakal tanpa diyakini sebagai sabda Nabi SAW yang pasti.",
    sections=[
        ("bacaan", "Bacaan Dua Ayat Terakhir At-Taubah", qcard(P, "At-Taubah 9:128–129", 9, 128, 129, "Surah At-Taubah, ayat 128–129")),
        ("kisah", "Kisah Pengumpulan Ayat Ini",
         "<p>Ketika Zaid bin Thabit RA mengumpulkan Al-Quran pada zaman Abu Bakar RA, dia menemui dua ayat terakhir At-Taubah tertulis hanya pada Abu Khuzaimah Al-Ansari, sedangkan ayat itu sudah dihafal oleh ramai sahabat."
         + ref("HR Al-Bukhari, no. 4986") + " Kisah ini menunjukkan ketelitian para sahabat: setiap ayat disahkan dengan hafalan dan tulisan.</p>"),
        ("maksud", "Maksud dan Pengajaran",
         ul("<strong>Ayat 128</strong>: Rasul daripada kalangan kamu sendiri, berat hatinya melihat penderitaan kamu, sangat menginginkan kebaikan untuk kamu, penyantun dan penyayang kepada orang beriman. Ia menuntut kita mencintai dan mengikut sunnah Baginda.",
            "<strong>Ayat 129</strong>: jika manusia berpaling, katakan “Cukuplah Allah bagiku”. Ini kalimah tawakal: berusaha sepenuhnya, kemudian menyerahkan hasil kepada Allah.",
            "Kalimah serupa, “Hasbunallah wa ni'mal wakil”, diucapkan Nabi Ibrahim AS ketika dicampak ke dalam api dan oleh Nabi Muhammad SAW ketika diancam musuh" + ref("HR Al-Bukhari, no. 4563") + ".")),
        ("amalan", "Amalan Hasbiyallah 7 Kali Pagi dan Petang",
         card(P, "Hasbiyallah (7×)", e(ZP["hasbiya"][2]), ZP["hasbiya"][3], e(ZP["hasbiya"][4]),
              "HR Abu Daud, no. 5081: perkataan Abu Ad-Darda' (mauquf); riwayat marfu'nya dinilai lemah",
              "Dibaca tujuh kali pada waktu pagi dan petang sebagai zikir tawakal.")
         + f'<p>Zikir ini termasuk dalam senarai <a href="{Q}zikir-pagi-petang/">Zikir Pagi & Petang dengan kaunter</a>.</p>'),
    ],
    faq=[("Apakah dua ayat terakhir Surah At-Taubah?", "Ayat 128 (Laqad ja'akum rasulun min anfusikum…) dan ayat 129 (Fa in tawallau fa qul hasbiyallahu la ilaha illa huwa…)."),
         ("Apakah kelebihan membaca Hasbiyallah 7 kali?", "Riwayat Abu Daud (5081) menyebut Allah mencukupkan urusan orang yang membacanya 7 kali pagi dan petang. Ia perkataan Abu Ad-Darda' dan sanadnya dipertikai, tetapi diamalkan sebagai zikir tawakal."),
         ("Apakah maksud Hasbiyallahu la ilaha illa huwa?", "Cukuplah Allah bagiku, tiada tuhan melainkan Dia; kepada-Nya aku bertawakal dan Dia Tuhan Arasy yang agung."),
         ("Siapakah yang menyimpan dua ayat terakhir At-Taubah?", "Abu Khuzaimah Al-Ansari RA, yang mempunyai tulisan ayat itu ketika Zaid bin Thabit mengumpulkan Al-Quran (HR Al-Bukhari 4986).")],
    refs=["Al-Quran: At-Taubah 9:128–129.", "Sahih Al-Bukhari, no. 4563, 4986.", "Sunan Abu Daud, no. 5081."],
    related=[(Q + "zikir-pagi-petang/", "Zikir Pagi & Petang", "Termasuk Hasbiyallah 7 kali"), (SERIBU, "Ayat Seribu Dinar", "Ayat tawakal dan rezeki"),
             (YUNUS, "Doa Nabi Yunus", "Doa ketika dalam kesempitan")])))

# 7 ---------------------------------------------------------------- Ayat Seribu Dinar
P = "ilmx-sd"
POSTS.append(("seribu-dinar", base(
    ns=P, url=SERIBU, published="2020-01-09", pubms="9 Januari 2020",
    title="Ayat Seribu Dinar (Ath-Thalaq 2–3): Maksud, Asal Nama & Kelebihan",
    desc="Ayat Seribu Dinar (Ath-Thalaq 2–3): teks Arab dan maksud, asal usul nama seribu dinar, kelebihan takwa dan tawakal, status riwayat dan hukum menggantungnya.",
    h1="Ayat Seribu Dinar: Maksud, Asal Nama & Kelebihan", img=img("ayat-seribu-dinar", "Ayat Amalan", "Ayat Seribu Dinar", "Ath-Thalaq 2–3: maksud, asal nama dan kelebihan", "وَمَن يَتَّقِ اللّٰهَ"),
    alt="Ayat Seribu Dinar Surah Ath-Thalaq ayat 2 dan 3", refshort="Al-Quran, Sunan At-Tirmizi, Sunan Ibn Majah",
    lead="Dua potong ayat tentang takwa dan tawakal yang terkenal sebagai “Ayat Seribu Dinar”: maksudnya, dari mana nama itu datang, dan cara mengamalkannya dengan betul.",
    crumb=("Amalan", W + "search/label/Amalan"), about=["Ayat Seribu Dinar", "Rezeki", "Tawakal"],
    answer="Ayat Seribu Dinar ialah <strong>Surah Ath-Thalaq ayat 2 (bahagian akhir) dan ayat 3</strong>: sesiapa bertakwa, Allah memberinya jalan keluar dan rezeki dari arah yang tidak disangka; sesiapa bertawakal, Allah mencukupinya. "
           "Nama “seribu dinar” berasal daripada <strong>kisah yang masyhur dalam masyarakat</strong>, bukan daripada hadis. Kelebihannya terletak pada janji Allah dalam ayat itu sendiri, yang bersyarat dengan takwa dan tawakal.",
    sections=[
        ("bacaan", "Bacaan Ayat Seribu Dinar", qcard(P, "Ath-Thalaq 65:2–3", 65, 2, 3, "Surah Ath-Thalaq, ayat 2–3. Bahagian yang masyhur sebagai Ayat Seribu Dinar bermula “wa man yattaqillah…”")),
        ("konteks", "Konteks Ayat: Turun dalam Surah tentang Talak",
         "<p>Ramai tidak menyedari bahawa ayat ini terletak di tengah-tengah hukum <strong>talak dan iddah</strong> dalam Surah Ath-Thalaq. Selepas memerintahkan suami isteri yang berpisah supaya menjaga iddah, "
         "tidak mengusir isteri dari rumah dan berlaku adil, Allah menyelitkan janji ini. Mesejnya: dalam situasi paling sukar, termasuk perceraian dan kesempitan nafkah, "
         "<strong>takwa ialah jalan keluar</strong>, dan berlaku adil walaupun ketika marah tidak akan menyempitkan rezeki.</p>"
         "<p>Kesimpulannya, “Ayat Seribu Dinar” bukan jampi rezeki, tetapi prinsip hidup: patuhi hukum Allah dalam keadaan sukar, maka Allah membuka jalan yang tidak disangka.</p>"),
        ("nama", "Kenapa Dinamakan Ayat Seribu Dinar?",
         "<p>Nama ini datang daripada kisah popular tentang seorang lelaki (dalam sesetengah versi seorang pedagang) yang mendapat seribu dinar selepas mengamalkan ayat ini, atau yang bersedekah seribu dinar dan diganti Allah. "
         "Kisah ini <strong>tidak terdapat dalam kitab hadis yang muktabar</strong> dan versinya berbeza-beza. Ia boleh diambil sebagai cerita motivasi, tetapi bukan dalil.</p>"),
        ("kelebihan", "Kelebihan Ayat Ini dan Status Riwayatnya",
         grade([("Janji jalan keluar dan rezeki dari arah tidak disangka bagi orang bertakwa", "Al-Quran, Ath-Thalaq 65:2–3", "✅ Al-Quran"),
                ("Jika kamu bertawakal dengan sebenar-benarnya, kamu diberi rezeki seperti burung yang keluar lapar dan pulang kenyang", "HR At-Tirmizi, no. 2344", "✅ Hasan sahih"),
                ("Abu Dzar: “Aku tahu satu ayat yang jika manusia berpegang dengannya, ia mencukupi mereka”, lalu membaca ayat ini", "HR Ibn Majah, no. 4220; Ahmad", DHAIF),
                ("Menggantung ayat ini di kedai atau rumah menarik rezeki", "Tiada sumber", "❌ Tiada asas")])),
        ("tawakal", "Tawakal yang Betul: Ikat Unta Dahulu",
         "<p>Seorang lelaki bertanya sama ada dia patut melepaskan untanya dan bertawakal. Nabi SAW menjawab: “Ikatlah ia, kemudian bertawakallah.”" + ref("HR At-Tirmizi, no. 2517; hasan") + " "
         "Tawakal bukan meninggalkan usaha, tetapi menggabungkan usaha yang terbaik dengan penyerahan hati kepada Allah.</p>"
         + table(["Bukan tawakal", "Tawakal yang betul"], [["Menunggu rezeki tanpa bekerja", "Bekerja bersungguh-sungguh, kemudian reda dengan hasilnya"],
                                                         ["Bergantung sepenuhnya pada ayat yang digantung", "Membaca dan memahami ayat, kemudian mengamalkan takwa dalam urusan"],
                                                         ["Berputus asa apabila usaha gagal", "Memperbaiki cara, berdoa dan yakin Allah memilih yang terbaik"]])),
        ("amal", "Cara Mengamalkan dengan Betul",
         ul("Jadikan ayat ini pegangan: <strong>takwa</strong> (meninggalkan yang haram dalam pekerjaan dan perniagaan) dan <strong>tawakal</strong> (berusaha sepenuhnya, kemudian berserah).",
            "Baca dan fahami maksudnya sebagai zikir, terutama selepas solat atau ketika menghadapi masalah kewangan.", "Gabungkan dengan istighfar, sedekah dan doa rezeki yang sahih.")
         + f'<div class="{P}-box amber"><strong>Menggantung ayat:</strong> menggantung ayat Al-Quran sebagai hiasan atau peringatan diharuskan oleh ramai ulama dengan syarat dihormati. '
           "Yang dilarang ialah meyakini kertas atau bingkai itu sendiri mendatangkan rezeki atau menolak bala; rezeki datang daripada Allah melalui takwa dan usaha.</div>"),
    ],
    faq=[("Apakah Ayat Seribu Dinar?", "Surah Ath-Thalaq ayat 2 (bahagian akhir) dan ayat 3: “Wa man yattaqillaha yaj'al lahu makhraja, wa yarzuqhu min haithu la yahtasib…”."),
         ("Kenapa dipanggil Ayat Seribu Dinar?", "Kerana kisah popular tentang seseorang yang mendapat atau diganti seribu dinar selepas mengamalkannya. Kisah ini tiada dalam kitab hadis yang muktabar."),
         ("Apakah kelebihan Ayat Seribu Dinar?", "Janji Allah dalam ayat itu sendiri: jalan keluar dan rezeki dari arah tidak disangka bagi orang bertakwa, dan kecukupan bagi orang bertawakal."),
         ("Bolehkah menggantung Ayat Seribu Dinar di kedai?", "Harus sebagai hiasan atau peringatan dengan syarat dihormati, tetapi jangan meyakini gantungan itu sendiri yang mendatangkan rezeki.")],
    refs=["Al-Quran: Ath-Thalaq 65:2–3.", "Sunan At-Tirmizi, no. 2344.", "Sunan Ibn Majah, no. 4220; Musnad Ahmad (riwayat Abu Dzar, dhaif)."],
    related=[(WAQIAH, "Surah Al-Waqiah & Rezeki", "Status hadis dan amalan rezeki yang sahih"), (Q + "doa-murah-rezeki/", "Doa Murah Rezeki", "Doa rezeki yang sahih"),
             (W + "2018/02/rasai-manfaat-asalkan-istiqomah-amalkan.html", "2 Ayat Terakhir At-Taubah", "Hasbiyallah: kalimah tawakal")])))

# 8 ---------------------------------------------------------------- Doa Nabi Yunus
P = "ilmx-yn"
POSTS.append(("doa-nabi-yunus", base(
    ns=P, url=YUNUS, published="2018-02-01", pubms="1 Februari 2018",
    title="Doa Nabi Yunus: Bacaan, Maksud, Kisah & Kelebihan (Hadis Sahih)",
    desc="Doa Nabi Yunus (La ilaha illa anta subhanaka inni kuntu minaz-zalimin): teks Arab, Rumi dan maksud, kisah dalam perut ikan, kelebihan dan cara mengamalkannya.",
    h1="Doa Nabi Yunus: Bacaan, Kisah & Kelebihan", img=img("doa-nabi-yunus-ayat", "Doa Para Nabi", "Doa Nabi Yunus", "Doa dalam kegelapan yang dijanjikan makbul", "لَا إِلٰهَ إِلَّا أَنتَ"),
    alt="Doa Nabi Yunus: bacaan, maksud dan kelebihan", refshort="Al-Quran, Sunan At-Tirmizi",
    lead="Doa yang dibaca Nabi Yunus AS dalam tiga kegelapan, yang dijanjikan Rasulullah SAW akan dimakbulkan bagi setiap Muslim yang berdoa dengannya.",
    crumb=("Doa", W + "search/label/Doa"), about=["Doa Nabi Yunus", "Doa para nabi"],
    answer="Doa Nabi Yunus ialah <strong>“La ilaha illa anta, subhanaka, inni kuntu minaz-zalimin”</strong> (Al-Anbiya' 21:87). Nabi SAW bersabda: tiada seorang Muslim pun yang berdoa dengannya "
           "dalam apa jua urusan <strong>melainkan Allah memperkenankan doanya</strong> <em>(HR At-Tirmizi, no. 3505; sahih)</em>.",
    sections=[
        ("bacaan", "Bacaan Doa Nabi Yunus", qcard(P, "Al-Anbiya' 21:87–88", 21, 87, 88, "HR At-Tirmizi, no. 3505 · Surah Al-Anbiya', ayat 87–88")),
        ("kisah", "Kisah Nabi Yunus dalam Perut Ikan",
         "<p>Nabi Yunus AS diutus kepada penduduk Ninawa. Apabila mereka enggan beriman, Baginda meninggalkan mereka dalam keadaan marah sebelum diizinkan Allah, lalu menaiki kapal. Undian di atas kapal jatuh kepadanya, "
         "dia dicampak ke laut dan ditelan ikan besar" + ref("As-Saffat 37:139–144") + ". Dalam tiga kegelapan, iaitu perut ikan, dasar laut dan malam, dia bertasbih dan mengakui kesilapannya. "
         "Allah menyelamatkannya, dan kaumnya akhirnya beriman" + ref("As-Saffat 37:145–148") + ".</p>"
         f'<p>Kisah penuh dengan semua ayat yang menyebut nama Baginda: <a href="{Q}kisah-nabi/nabi-yunus/">Kisah Nabi Yunus</a>.</p>'),
        ("kandungan", "Tiga Unsur dalam Doa Ini",
         table(["Lafaz", "Maksud", "Unsur"], [["La ilaha illa anta", "Tiada tuhan melainkan Engkau", "Tauhid"], ["Subhanaka", "Maha Suci Engkau", "Tasbih (menyucikan Allah)"],
                                             ["Inni kuntu minaz-zalimin", "Sesungguhnya aku termasuk orang yang zalim", "Pengakuan dosa dan taubat"]])
         + "<p>Doa ini tidak menyebut hajat secara langsung; ia mendahulukan tauhid, pujian dan taubat. Ulama menjelaskan adab ini membuka pintu makbulnya doa.</p>"),
        ("amal", "Cara Mengamalkan",
         ul("Baca ketika ditimpa kesusahan, kebimbangan, penyakit atau ketika merasa bersalah.", "Fahami maksudnya dan hadirkan rasa taubat.",
            "Tiada bilangan tertentu yang ditetapkan oleh hadis; sesetengah ulama mengamalkannya berulang kali sebagai zikir, dan ini harus.", "Selepas itu, mohonlah hajat anda dengan bahasa sendiri.")
         + f'<p>Lihat juga <a href="{Q}doa-nabi-yunus/">Doa Nabi Yunus di Al-Quran Online</a> dan <a href="{Q}doa-hilangkan-resah/">doa ketika resah</a>.</p>'),
    ],
    faq=[("Apakah doa Nabi Yunus?", "La ilaha illa anta, subhanaka, inni kuntu minaz-zalimin: Tiada tuhan melainkan Engkau, Maha Suci Engkau, sesungguhnya aku termasuk orang yang zalim (Al-Anbiya' 21:87)."),
         ("Apakah kelebihan doa Nabi Yunus?", "Tiada Muslim yang berdoa dengannya dalam apa jua urusan melainkan Allah memperkenankannya (HR At-Tirmizi 3505)."),
         ("Berapa kali doa Nabi Yunus perlu dibaca?", "Tiada bilangan yang ditetapkan oleh hadis. Bacalah dengan penuh penghayatan; mengulanginya sebagai zikir dibenarkan."),
         ("Di manakah doa Nabi Yunus dalam Al-Quran?", "Surah Al-Anbiya' ayat 87. Ayat 88 menyebut Allah memperkenankan doanya dan menyelamatkannya, dan demikianlah Allah menyelamatkan orang beriman.")],
    refs=["Al-Quran: Al-Anbiya' 21:87–88; As-Saffat 37:139–148.", "Sunan At-Tirmizi, no. 3505."],
    related=[(Q + "doa-nabi-yunus/", "Doa Nabi Yunus di Al-Quran Online", "Bacaan dengan audio"), (Q + "kisah-nabi/nabi-yunus/", "Kisah Nabi Yunus", "Kisah penuh dengan ayat-ayat Al-Quran"),
             (Q + "doa-hilangkan-resah/", "Doa Hilangkan Resah", "Doa sahih ketika gelisah")])))

# 9 ---------------------------------------------------------------- Ruqyah syar'iyyah (4 posts merged)
P = "ilmx-rq"
JIBRIL = ("بِاسْمِ اللّٰهِ أَرْقِيكَ، مِنْ كُلِّ شَيْءٍ يُؤْذِيكَ، مِنْ شَرِّ كُلِّ نَفْسٍ أَوْ عَيْنِ حَاسِدٍ، اللّٰهُ يَشْفِيكَ، بِاسْمِ اللّٰهِ أَرْقِيكَ",
          "Bismillahi arqik, min kulli syai'in yu'zik, min syarri kulli nafsin au 'aini hasid, Allahu yasyfik, bismillahi arqik.",
          "Dengan nama Allah aku meruqyahmu, daripada segala sesuatu yang menyakitimu, daripada kejahatan setiap jiwa atau mata yang dengki. Allah menyembuhkanmu. Dengan nama Allah aku meruqyahmu.")
POSTS.append(("ruqyah", base(
    ns=P, url=RUQYAH, published="2020-02-28", pubms="28 Februari 2020",
    title="Ruqyah Syar'iyyah: Ayat, Doa Pendinding & Tanda Gangguan",
    desc="Ruqyah syar'iyyah: ayat dan doa ruqyah daripada sunnah, zikir pendinding harian, tanda gangguan, bila perlu ke doktor dan ciri perawat yang perlu dielakkan.",
    h1="Ruqyah Syar'iyyah: Ayat, Doa & Pendinding Diri", img=img("ruqyah-syariyyah", "Panduan Sunnah", "Ruqyah Syar'iyyah", "Ayat, doa pendinding dan cara memilih perawat yang betul", "الرُّقْيَةُ"),
    alt="Ruqyah syar'iyyah: ayat dan doa pendinding diri", refshort="Sahih Al-Bukhari & Muslim, Sunan Abu Daud & At-Tirmizi",
    lead="Ruqyah yang diajar Rasulullah SAW: ayat dan doanya, zikir pendinding harian, tanda yang sering dikaitkan dengan gangguan, dan cara membezakan perawat yang patuh syarak.",
    crumb=("Amalan", W + "search/label/Amalan"), about=["Ruqyah", "Pendinding diri", "Gangguan jin"],
    answer="Ruqyah syar'iyyah ialah rawatan dengan <strong>ayat Al-Quran, nama dan sifat Allah serta doa yang difahami</strong>, dengan yakin bahawa penyembuh hanyalah Allah. Nabi SAW bersabda: "
           "<strong>“Tidak mengapa ruqyah selagi ia tidak mengandungi syirik”</strong> <em>(HR Muslim, no. 2200)</em>. Ayat utamanya: Al-Fatihah, Ayat Kursi, dua ayat terakhir Al-Baqarah dan tiga Qul. "
           "Simptom yang dikaitkan dengan gangguan sering bertindih dengan masalah perubatan, jadi <strong>rawatan doktor tetap perlu</strong>.",
    sections=[
        ("syarat", "Syarat Ruqyah yang Dibenarkan",
         ul("Menggunakan ayat Al-Quran, nama dan sifat Allah, atau doa yang thabit.", "Dalam bahasa yang difahami; jampi yang tidak difahami maknanya wajib dielakkan.",
            "Meyakini bahawa ruqyah hanyalah sebab; yang menyembuhkan ialah Allah.", "Tiada unsur syirik: tiada seruan kepada jin, tiada tangkal, tiada sembelihan untuk selain Allah." + ref("HR Muslim, no. 2200"))),
        ("ayat", "Ayat-ayat Ruqyah daripada Sunnah",
         table(["Ayat / surah", "Dalil", "Bacaan"], [
             ["Al-Fatihah", "Sahabat meruqyah ketua kabilah yang disengat (HR Al-Bukhari, no. 5007)", f'<a href="{W}2018/02/11-hikmah-dan-keutamaan-membaca-surah.html">Kelebihan Al-Fatihah</a>'],
             ["Ayat Kursi (Al-Baqarah 255)", "Dibaca sebelum tidur, dipelihara hingga pagi (HR Al-Bukhari, no. 2311)", f'<a href="{Q}ayat-kursi/">Ayat Kursi</a>'],
             ["Dua ayat terakhir Al-Baqarah (285–286)", "Mencukupi bagi yang membacanya pada waktu malam (HR Al-Bukhari, no. 5009)", f'<a href="{Q}amanar-rasul/">Amanar Rasul</a>'],
             ["Al-Ikhlas, Al-Falaq, An-Nas", "Nabi SAW membacanya, meniup ke tapak tangan dan menyapu badan (HR Al-Bukhari, no. 5017)", f'<a href="{IKHLAS}">9 waktu membaca Al-Ikhlas</a>']])),
        ("doa", "Doa Ruqyah daripada Hadis",
         card(P, "Ruqyah Jibril kepada Nabi SAW", e(JIBRIL[0]), JIBRIL[1], e(JIBRIL[2]), "HR Muslim, no. 2186", "Ketika meruqyah diri sendiri, tukar “arqik” kepada lafaz doa untuk diri.")
         + hd(P, "orang-sakit", "Diletakkan tangan kanan pada tempat yang sakit atau pada pesakit sambil membacanya.")),
        ("cara", "Cara Meruqyah Diri Sendiri",
         ul("Berwuduk dan duduk di tempat yang bersih dan tenang.", "Mulakan dengan istighfar dan selawat.", "Baca Al-Fatihah, Ayat Kursi, dua ayat terakhir Al-Baqarah, dan tiga Qul.",
            "Tiup perlahan ke kedua-dua tapak tangan selepas membaca tiga Qul, kemudian sapu ke seluruh badan yang dapat dicapai, bermula dari kepala dan muka; ulang tiga kali" + ref("HR Al-Bukhari, no. 5017") + ".",
            "Letakkan tangan pada tempat yang sakit dan baca “Bismillah” tiga kali, kemudian “A'uzu bi'izzatillahi wa qudratihi min syarri ma ajidu wa uhaziru” tujuh kali" + ref("HR Muslim, no. 2202") + ".",
            "Akhiri dengan doa memohon kesembuhan dengan bahasa sendiri.", ordered=True)),
        ("rumah", "Pendinding Rumah",
         ul("Membaca Surah Al-Baqarah di rumah: “Jangan jadikan rumah kamu seperti kubur; sesungguhnya syaitan lari dari rumah yang dibaca padanya Surah Al-Baqarah.”" + ref("HR Muslim, no. 780"),
            "Menyebut nama Allah ketika masuk rumah dan ketika makan: syaitan berkata tiada tempat bermalam dan tiada makan malam bagi mereka." + ref("HR Muslim, no. 2018"),
            "Menutup pintu dan menyebut nama Allah pada waktu malam." + ref("HR Al-Bukhari, no. 3280"),
            "Menjauhkan gambar dan patung bernyawa serta anjing (bukan untuk berburu atau menjaga) daripada rumah, kerana malaikat rahmat tidak memasukinya." + ref("HR Al-Bukhari, no. 3225"))),
        ("pendinding", "Zikir Pendinding Harian",
         zp(P, "bismillah") + zp(P, "kursi")
         + f'<p>Senarai penuh dengan kaunter: <a href="{Q}zikir-pagi-petang/">Zikir Pagi & Petang</a>. Pendinding terbaik ialah solat lima waktu, zikir pagi petang dan menjauhi maksiat.</p>'),
        ("tanda", "Tanda yang Sering Dikaitkan dengan Gangguan, dan Bila ke Doktor",
         "<p>Antara keadaan yang sering dikaitkan masyarakat dengan gangguan jin atau sihir: mimpi ngeri berulang, rasa berat atau sakit yang berpindah-pindah tanpa punca, benci mendengar azan atau Al-Quran, "
         "perubahan emosi mendadak dan pertengkaran tanpa sebab.</p>"
         + f'<div class="{P}-box amber"><strong>Penting:</strong> semua tanda ini juga boleh berpunca daripada masalah perubatan seperti kemurungan, kebimbangan, gangguan tidur, epilepsi atau ketidakseimbangan hormon. '
           "Jangan meninggalkan rawatan doktor. Ruqyah dan perubatan moden boleh berjalan seiring; Nabi SAW bersabda: “Berubatlah, kerana Allah tidak menurunkan penyakit melainkan diturunkan juga ubatnya” (HR Abu Daud, no. 3855).</div>"),
        ("perawat", "Ciri Perawat yang Perlu Dielakkan",
         table(["Tanda bahaya", "Sebab"], [["Bertanya nama ibu atau tarikh lahir untuk “menilik”", "Amalan bomoh dan tilikan, bukan ruqyah"], ["Membaca jampi yang tidak difahami maknanya", "Bercanggah dengan syarat ruqyah"],
                                          ["Memberi tangkal, azimat atau benda untuk ditanam atau digantung", "Tangkal dilarang (HR Ahmad, no. 17422)"], ["Menyuruh menyembelih binatang tertentu atau membuat sajian", "Boleh membawa kepada syirik"],
                                          ["Menuduh ahli keluarga tertentu sebagai penyihir", "Menimbulkan fitnah tanpa bukti"], ["Menyentuh pesakit berlainan jantina tanpa keperluan atau tanpa mahram", "Melanggar batas syarak"]])
         + "<p>Pilih perawat yang mengamalkan ruqyah secara terbuka dengan ayat dan doa yang difahami, dan yang menggalakkan anda terus mendapatkan rawatan perubatan.</p>"),
    ],
    faq=[("Apakah ruqyah syar'iyyah?", "Rawatan dengan ayat Al-Quran, nama Allah dan doa yang thabit, dalam bahasa yang difahami, tanpa unsur syirik, dengan yakin Allah yang menyembuhkan (HR Muslim 2200)."),
         ("Apakah ayat ruqyah yang utama?", "Al-Fatihah, Ayat Kursi, dua ayat terakhir Al-Baqarah serta Al-Ikhlas, Al-Falaq dan An-Nas."),
         ("Bolehkah meruqyah diri sendiri?", "Boleh. Nabi SAW meruqyah dirinya dengan tiga Qul dan menyapu badan (HR Al-Bukhari 5017)."),
         ("Adakah perlu ke doktor jika rasa diganggu?", "Ya. Banyak simptom yang dikaitkan dengan gangguan juga merupakan simptom perubatan. Ruqyah dan rawatan doktor boleh dilakukan serentak (HR Abu Daud 3855)."),
         ("Apakah doa pendinding diri setiap hari?", "Bismillahillazi la yadhurru ma'asmihi syai'un… tiga kali pagi dan petang (HR Abu Daud 5088; At-Tirmizi 3388), Ayat Kursi, dan tiga Qul.")],
    refs=["Sahih Al-Bukhari, no. 2311, 5007, 5009, 5017.", "Sahih Muslim, no. 2186, 2200.", "Sunan Abu Daud, no. 3855, 5088; Sunan At-Tirmizi, no. 3388.", "Musnad Ahmad, no. 17422."],
    disclaimer="Artikel ini panduan agama, bukan nasihat perubatan. Dapatkan rawatan doktor untuk sebarang simptom fizikal atau emosi yang berpanjangan.",
    related=[(Q + "ayat-kursi/", "Ayat Kursi", "Bacaan, maksud dan kelebihan"), (Q + "zikir-pagi-petang/", "Zikir Pagi & Petang", "Pendinding harian dengan kaunter"),
             (Q + "doa-orang-sakit/", "Doa Orang Sakit", "Doa ketika sakit dan menziarahi pesakit")])))

# 10 ---------------------------------------------------------------- syirik
P = "ilmx-sy"
POSTS.append(("dosa-syirik", base(
    ns=P, url=W + "2018/03/baca-dan-fahami-allah-tidak.html", published="2020-01-03", pubms="3 Januari 2020",
    title="Allah Mengampunkan Semua Dosa Kecuali Syirik: Maksud & Jenis Syirik",
    desc="Maksud An-Nisa' 48: Allah tidak mengampunkan syirik tetapi mengampunkan dosa lain, jenis syirik besar dan kecil, contoh di Malaysia dan pintu taubat.",
    h1="Allah Mengampunkan Semua Dosa Kecuali Syirik", img=img("dosa-syirik", "Akidah", "Dosa yang Tidak Diampunkan: Syirik", "An-Nisa' 48, jenis syirik dan pintu taubat", "الشِّرْكُ"),
    alt="Allah mengampunkan semua dosa kecuali syirik", refshort="Al-Quran, Sahih Muslim, Sunan At-Tirmizi, Musnad Ahmad",
    lead="Ayat yang paling menakutkan dan paling memberi harapan sekaligus: maksud An-Nisa' 48, jenis-jenis syirik termasuk yang tersembunyi, dan pintu taubat yang terbuka hingga nyawa di kerongkong.",
    crumb=("Islamik", W + "search/label/Islamik"), about=["Syirik", "Taubat", "Akidah"],
    answer="Allah berfirman: <strong>“Sesungguhnya Allah tidak mengampunkan dosa syirik, dan mengampunkan dosa selain itu bagi sesiapa yang Dia kehendaki”</strong> (An-Nisa' 4:48). Maksudnya: orang yang "
           "<strong>mati dalam keadaan syirik tanpa bertaubat</strong> tidak diampunkan. Namun sesiapa yang <strong>bertaubat sebelum mati</strong>, termasuk daripada syirik, Allah menerima taubatnya (Az-Zumar 39:53; Al-Furqan 25:68–70).",
    sections=[
        ("ayat", "Ayat Al-Quran", qcard(P, "An-Nisa' 4:48", 4, 48, 48, "Surah An-Nisa', ayat 48") + qcard(P, "Az-Zumar 39:53: jangan berputus asa", 39, 53, 53, "Surah Az-Zumar, ayat 53")),
        ("maksud", "Maksud Sebenar Ayat Ini",
         ul("Ayat An-Nisa' 48 merujuk kepada orang yang <strong>meninggal dunia</strong> dalam keadaan syirik. Selagi hidup, pintu taubat terbuka.",
            "Az-Zumar 39:53 ditujukan kepada mereka yang bertaubat: Allah mengampunkan <strong>semua</strong> dosa.",
            "Dalam hadis qudsi, Allah berfirman: “Wahai anak Adam, jika kamu datang kepada-Ku dengan dosa sepenuh bumi, kemudian kamu menemui-Ku tanpa menyekutukan-Ku dengan sesuatu, nescaya Aku datang kepadamu dengan keampunan sepenuh bumi.”" + ref("HR At-Tirmizi, no. 3540"),
            "“Sesiapa yang mati tidak menyekutukan Allah dengan sesuatu, dia masuk syurga.”" + ref("HR Muslim, no. 93"))),
        ("jenis", "Jenis-jenis Syirik",
         table(["Jenis", "Maksud", "Hukum"], [["Syirik besar (akbar)", "Menyembah, berdoa atau bergantung kepada selain Allah dalam perkara yang hanya Allah mampu", "Mengeluarkan daripada Islam; tidak diampunkan jika mati tanpa taubat"],
                                             ["Syirik kecil (asghar)", "Seperti riya' (beribadah untuk dilihat orang) dan bersumpah dengan selain Allah", "Dosa besar, tidak mengeluarkan daripada Islam. Nabi SAW menyebut riya' sebagai “syirik kecil” (HR Ahmad, no. 23630)"],
                                             ["Syirik tersembunyi (khafi)", "Niat yang bercampur keinginan pujian dalam hati", "Dibersihkan dengan memperbetulkan niat dan doa"]])),
        ("contoh", "Contoh Amalan Berisiko Syirik di Malaysia",
         table(["Amalan", "Penjelasan"], [["Memakai tangkal atau azimat dengan keyakinan ia melindungi", "Tangkal dilarang (HR Ahmad, no. 17422)"],
                                          ["Meminta bantuan bomoh yang menyeru jin atau membuat sajian", "Boleh membawa kepada syirik besar"], ["Percaya nombor, hari atau burung membawa sial", "Tathayyur dilarang: “Tiada sial” (HR Al-Bukhari, no. 5757)"],
                                          ["Mempercayai tilikan dan ramalan nasib", "Solat 40 hari tidak diterima bagi yang bertanya kepada tukang tilik (HR Muslim, no. 2230)"],
                                          ["Beribadah atau bersedekah untuk dipuji", "Riya': syirik kecil"]])),
        ("taubat", "Pintu Taubat Sentiasa Terbuka",
         qcard(P, "Al-Furqan 25:70: dosa ditukar menjadi kebaikan", 25, 70, 70, "Surah Al-Furqan, ayat 70")
         + "<p>Selepas menyebut dosa syirik, membunuh dan zina dalam ayat 68–69, Allah mengecualikan orang yang bertaubat, beriman dan beramal soleh: kejahatan mereka ditukar menjadi kebaikan. "
           "Taubat diterima selagi nyawa belum sampai ke kerongkong" + ref("HR At-Tirmizi, no. 3537") + ".</p>"
         + f'<p>Lafaz istighfar terbaik: <a href="{Q}doa-taubat/">Doa taubat & Sayyidul Istighfar</a>.</p>'),
    ],
    faq=[("Adakah dosa syirik tidak diampunkan langsung?", "Ia tidak diampunkan jika seseorang mati dalam keadaan syirik tanpa bertaubat (An-Nisa' 4:48). Jika bertaubat sebelum mati, Allah menerima taubatnya (Az-Zumar 39:53; Al-Furqan 25:70)."),
         ("Apakah contoh syirik kecil?", "Riya' (beribadah untuk dipuji), yang Nabi SAW sebut sebagai syirik kecil (HR Ahmad 23630), dan bersumpah dengan nama selain Allah."),
         ("Adakah memakai tangkal termasuk syirik?", "Memakai tangkal dengan keyakinan ia melindungi dilarang dan boleh membawa kepada syirik (HR Ahmad 17422)."),
         ("Sampai bilakah taubat diterima?", "Selagi nyawa belum sampai ke kerongkong (HR At-Tirmizi 3537) dan sebelum matahari terbit dari barat.")],
    refs=["Al-Quran: An-Nisa' 4:48; Az-Zumar 39:53; Al-Furqan 25:68–70.", "Sahih Muslim, no. 93, 2230; Sahih Al-Bukhari, no. 5757.", "Sunan At-Tirmizi, no. 3537, 3540.", "Musnad Ahmad, no. 17422, 23630."],
    disclaimer="Panduan akidah ringkas mengikut Ahli Sunnah wal Jamaah. Untuk persoalan peribadi, rujuk pejabat agama Islam negeri anda.",
    related=[(Q + "doa-taubat/", "Doa Taubat", "Sayyidul Istighfar dan doa taubat yang sahih"), (RUQYAH, "Ruqyah Syar'iyyah", "Rawatan tanpa syirik dan ciri perawat yang perlu dielakkan"),
             (Q + "asmaul-husna/", "Asmaul Husna", "99 nama Allah dengan maksud")])))

# duplicate posts folded into the posts above: old URL -> (target slug in POSTS, short reason)
MERGES = [
    (W + "2020/01/surah-yasin-ayat-58.html", "kelebihan-yasin", "Yasin ayat 58"),
    (W + "2018/01/rawat-jiwa-kacau-dengan-11-ayat-dalam.html", "ad-dhuha", "Ad-Dhuha untuk jiwa"),
    (W + "2018/02/rawat-jiwa-yang-tidak-tenang-dengan.html", "ad-dhuha", "Ad-Dhuha untuk jiwa"),
    (W + "2020/01/doa-pembatal-sihir-ayat-pendinding-diri.html", "ruqyah", "doa pendinding"),
    (W + "2018/02/ayat-ruqyah-untuk-menghancurkan-sihir.html", "ruqyah", "ayat ruqyah"),
]


def merge_stub(target_url, target_title):
    """Body for a merged duplicate: a visible link for readers and a JS redirect that Google follows like a redirect."""
    return (f'<div style="border:1px solid #bfe3c9;background:#effaf2;border-radius:12px;padding:16px;font-family:inherit">'
            f'<p style="margin:0 0 8px"><strong>Artikel ini telah dikemas kini dan digabungkan.</strong></p>'
            f'<p style="margin:0">Baca versi terkini dan lengkap: <a href="{target_url}">{e(target_title)}</a></p></div>'
            f'<script>location.replace({json.dumps(target_url)});</script>')


if __name__ == "__main__":
    write(POSTS)
    by = {s: p for s, p in POSTS}
    stubs = [{"url": u, "target": by[s]["url"], "title": by[s]["title"], "content": merge_stub(by[s]["url"], by[s]["title"])} for u, s, _ in MERGES]
    json.dump(stubs, open(f"{OUT}/batch2-merges.json", "w"), ensure_ascii=False, indent=1)
    print("merges", len(stubs))
