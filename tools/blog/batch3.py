"""Batch 3 (solat, akhirat, doa, kisah & tokoh): 11 refreshed www.ilmualam.com posts. Each post targets the primary keyword chosen
from Ubersuggest Malaysia data (Nov 2026) and keeps its original URL. Duplicates already redirect here (applied with the triage).
Run from tools/blog: PYTHONPATH=.. python3 batch3.py"""
from gen import build, card, qcard, table, write, e, Q
from cards import card as img

W = "https://www.ilmualam.com/"
U = {
    "solat-hujung-waktu": W + "2018/01/azab-akibat-solat-di-hujung-waktu.html",
    "kelebihan-solat": W + "2018/02/9-kemuliaan-orang-menjaga-solat.html",
    "soalan-kubur": W + "2018/02/mampukah-kita-jawab-5-soalan-di-dalam.html",
    "tanda-kiamat": W + "2017/12/tanda-tanda-kiamat-kecil-telah-lengkap.html",
    "syurga-tanpa-hisab": W + "2018/01/11-golongan-yang-masuk-syurga-tanpa.html",
    "didoakan-malaikat": W + "2017/11/7-jenis-manusia-yang-didoakan-malaikat.html",
    "kaum-dibinasakan": W + "2020/01/12-kaum-yang-dibinasakan-Allah.html",
    "imam-syafie": W + "2020/02/pesanan-imam-syafie.html",
    "muqallibal-qulub": W + "2018/02/doa-mohon-allah-swt-tetapkan-hidayah.html",
    "doa-teraniaya": W + "2017/11/hati-hati-terhadap-doa-orang-yang.html",
    "ayam-berkokok": W + "2017/12/bila-ayam-berkokok-di-tengah-malam-maka.html",
}
SAHIH, HASAN, DHAIF, NOSRC = "✅ Sahih", "✅ Hasan", "⚠️ Dhaif", "❌ Tiada sumber sahih"


def ul(*items, ordered=False):
    tag = "ol" if ordered else "ul"
    return f"<{tag}>" + "".join(f"<li>{x}</li>" for x in items) + f"</{tag}>"


def ref(t):
    return f" <em>({t})</em>"


def dc(P, title, ar, ru, mn, src, note=""):
    return card(P, title, e(ar), ru, e(mn), e(src), note)


def grade(rows, head="Perkara yang disebut"):
    return table([head, "Sumber", "Status"], [[e(c), e(s), st] for c, s, st in rows])


def base(**k):
    k.setdefault("badges", ["Dalil Al-Quran & Hadis", "Status Hadis Dinyatakan", "Dikemas kini 2026"])
    k.setdefault("disclaimer", "Hadis dhaif disebut bersama statusnya supaya pembaca tahu kedudukannya. Untuk persoalan hukum peribadi, rujuk pejabat agama Islam negeri anda.")
    return k


POSTS = []

# 1 ---------------------------------------------------------------- Solat di hujung waktu (absorbs 2 merged posts)
P = "ilmx-hw"
POSTS.append(("solat-hujung-waktu", base(
    ns=P, url=U["solat-hujung-waktu"], published="2018-01-31", pubms="31 Januari 2018",
    title="Solat di Hujung Waktu: Hukum, Azab & Kelebihan Solat Awal Waktu",
    desc="Hukum solat di hujung waktu dalam mazhab Syafi'i, azab melewatkan dan meninggalkan solat menurut Al-Quran dan hadis sahih, serta kelebihan solat awal waktu.",
    h1="Solat di Hujung Waktu: Hukum, Azab & Kelebihan Awal Waktu",
    img=img("solat-hujung-waktu", "Fiqh Solat", "Solat di Hujung Waktu", "Hukum, azab dan kelebihan solat awal waktu", "الصَّلَاةُ عَلَى وَقْتِهَا"),
    alt="Hukum solat di hujung waktu dan kelebihan solat awal waktu", refshort="Al-Quran, Sahih Al-Bukhari, Sahih Muslim",
    lead="Bezakan solat di hujung waktu yang sah, melewatkan solat sehingga keluar waktu yang berdosa besar, dan meninggalkan solat. Semuanya dengan dalil dan hukum mazhab Syafi'i.",
    crumb=("Solat", W + "search/label/Solat"), about=["Waktu solat", "Melewatkan solat", "Kelebihan solat awal waktu"],
    answer="Dalam mazhab Syafi'i, solat yang ditunaikan <strong>sebelum waktunya tamat adalah sah dan tidak berdosa</strong>, tetapi luput fadhilat awal waktu. Yang berdosa besar ialah "
           "<strong>sengaja melewatkannya sehingga keluar waktu</strong> tanpa uzur. Amalan yang paling dicintai Allah ialah <strong>solat pada waktunya</strong> <em>(HR Al-Bukhari, no. 527; Muslim, no. 85)</em>, "
           "dan Nabi SAW menyifatkan solat Asar yang sengaja dilewatkan hingga matahari hampir terbenam sebagai <strong>solat orang munafik</strong> <em>(HR Muslim, no. 622)</em>.",
    sections=[
        ("waktu", "Tiga Peringkat Waktu Solat dalam Mazhab Syafi'i",
         "<p>Ulama Syafi'i membahagikan setiap waktu solat kepada beberapa peringkat. Memahaminya menjawab soalan “berdosakah solat di hujung waktu?”.</p>"
         + table(["Peringkat", "Maksud", "Hukum"], [
             ["Waktu fadhilat", "Awal waktu, iaitu tempoh bersiap dan terus menunaikan solat", "Paling afdal; ganjaran paling besar"],
             ["Waktu ikhtiar dan jawaz", "Pertengahan hingga hampir akhir waktu", "Sah dan tidak berdosa"],
             ["Waktu karahah (Asar)", "Matahari sudah kekuningan hingga terbenam", "Sah tetapi makruh jika dilewatkan tanpa uzur"],
             ["Keluar waktu", "Waktu solat berikutnya sudah masuk", "Berdosa besar jika sengaja; wajib qada segera"]])
         + "<p>Sesiapa yang sempat menunaikan <strong>satu rakaat</strong> sebelum waktu tamat, solatnya dikira tunai (ada')"
         + ref("HR Al-Bukhari, no. 579; Muslim, no. 608") + ". Namun ulama menegaskan haram sengaja menangguhkan solat sehingga sebahagiannya jatuh di luar waktu.</p>"
         + f'<p>Semak waktu solat tepat bagi zon anda dalam <a href="{Q}waktu-solat/">Waktu Solat Malaysia (data JAKIM)</a>.</p>'),
        ("azab", "Azab Melewatkan Solat Menurut Al-Quran",
         qcard(P, "Al-Ma'un 107:4–5", 107, 4, 5, "Surah Al-Ma'un, ayat 4–5")
         + "<p>Sa'ad bin Abi Waqqas RA mentafsirkan “orang yang lalai daripada solatnya” sebagai mereka yang <strong>melewatkan solat daripada waktunya</strong>" + ref("Tafsir Ibn Kathir") + ". "
           "Ayat ini tidak ditujukan kepada orang yang meninggalkan solat sama sekali, tetapi kepada orang yang solat namun mempermainkan waktunya.</p>"
         + qcard(P, "Maryam 19:59", 19, 59, 59, "Surah Maryam, ayat 59")
         + "<p>Abdullah bin Mas'ud RA menjelaskan bahawa “mensia-siakan solat” dalam ayat ini bermaksud <strong>melewatkannya daripada waktunya</strong>, bukan meninggalkannya terus" + ref("Tafsir Ibn Kathir") + ".</p>"),
        ("hadis", "Hadis Sahih Tentang Melewatkan Solat",
         table(["Hadis", "Sumber"], [
             ["“Itulah solat orang munafik: dia duduk memerhati matahari, sehingga apabila ia berada di antara dua tanduk syaitan, dia bangun lalu mematuk empat kali, tidak menyebut Allah melainkan sedikit.”", "HR Muslim, no. 622"],
             ["Ditanya amalan yang paling dicintai Allah, Nabi SAW menjawab: “Solat pada waktunya.”", "HR Al-Bukhari, no. 527; Muslim, no. 85"],
             ["“Sesiapa yang terlepas solat Asar, seolah-olah dia kehilangan keluarga dan hartanya.”", "HR Al-Bukhari, no. 552; Muslim, no. 626"],
             ["“Sesiapa yang meninggalkan solat Asar, maka terhapuslah amalannya.”", "HR Al-Bukhari, no. 553"],
             ["“Sesiapa yang tertidur atau terlupa solat, hendaklah dia menunaikannya apabila teringat.”", "HR Al-Bukhari, no. 597; Muslim, no. 684"]])
         + "<p>Hadis terakhir menunjukkan orang yang <strong>tertidur atau terlupa</strong> tidak berdosa, tetapi wajib menunaikan solat sebaik sahaja sedar. Ini berbeza dengan orang yang sengaja menangguhkan.</p>"),
        ("tinggal", "Hukum Meninggalkan Solat",
         "<p>Nabi SAW bersabda: “Sesungguhnya (pemisah) antara seseorang dengan syirik dan kekufuran ialah meninggalkan solat”" + ref("HR Muslim, no. 82") + ". "
         "Dalam mazhab Syafi'i:</p>"
         + ul("Orang yang <strong>mengingkari kewajipan solat</strong> menjadi murtad.",
              "Orang yang meninggalkannya kerana <strong>malas</strong> tetapi masih meyakini kewajipannya tidak kafir, namun melakukan <strong>dosa besar</strong> yang sangat berat dan wajib bertaubat serta mengqada solatnya.",
              "Solat ialah amalan pertama yang dihisab pada hari kiamat; jika ia baik, baiklah seluruh amalan" + ref("HR At-Tirmizi, no. 413; Abu Daud, no. 864") + ".")
         + f'<div class="{P}-box amber">Kisah azab terperinci yang sering tersebar, seperti 15 seksaan bagi peninggal solat, berasal daripada riwayat yang <strong>tidak sahih</strong> menurut ulama hadis. '
           "Dalil sahih di atas sudah cukup menggerunkan tanpa perlu bergantung kepada riwayat palsu.</div>"),
        ("tidak-diterima", "Solat yang Tidak Diterima Menurut Hadis Sahih",
         "<p>Senarai “10 jenis solat yang tidak diterima” yang tersebar luas bercampur antara hadis sahih dan riwayat lemah. Yang thabit ialah:</p>"
         + grade([("Solat tanpa bersuci (wuduk atau mandi wajib)", "HR Muslim, no. 224", SAHIH),
                  ("Solat wanita yang sudah baligh tanpa menutup kepala", "HR Abu Daud, no. 641; At-Tirmizi, no. 377", SAHIH),
                  ("Orang yang bertanya kepada tukang tilik, tidak diterima solatnya 40 malam", "HR Muslim, no. 2230", SAHIH),
                  ("Peminum arak, tidak diterima solatnya 40 hari", "HR At-Tirmizi, no. 1862", HASAN),
                  ("Hamba yang lari, isteri yang tidur sedangkan suaminya marah dengan sebab yang benar, imam yang dibenci kaumnya: solat mereka tidak melepasi telinga", "HR At-Tirmizi, no. 360", HASAN)])
         + "<p>Ulama menjelaskan “tidak diterima” dalam hadis tukang tilik dan arak bermaksud <strong>tiada pahala</strong>, bukan solatnya tidak sah. Kewajipan tetap gugur, dan dia tidak boleh meninggalkan solat.</p>"),
        ("awal", "Kelebihan Solat Awal Waktu",
         ul("Amalan yang paling dicintai Allah" + ref("HR Al-Bukhari, no. 527"),
            "Solat lima waktu menghapuskan dosa kecil seperti mandi di sungai lima kali sehari" + ref("HR Al-Bukhari, no. 528; Muslim, no. 667"),
            "Orang yang awal ke masjid untuk solat berjemaah mendapat pahala seperti berkorban unta" + ref("HR Al-Bukhari, no. 881, untuk solat Jumaat"),
            "Malaikat berdoa untuk orang yang duduk menunggu solat" + ref("HR Al-Bukhari, no. 659"),
            "Hadis “Amalan paling utama ialah solat di awal waktunya” diriwayatkan Abu Daud (no. 426) dan At-Tirmizi (no. 170); sanadnya diperselisihkan, tetapi maknanya disokong hadis Al-Bukhari no. 527.")
         + "<h3>Tip praktikal supaya tidak solat di hujung waktu</h3>"
         + ul("Jadikan azan sebagai “mesyuarat wajib”: berhenti kerja 5 minit sahaja untuk solat.", "Ambil wuduk sebelum waktu masuk, terutama sebelum mesyuarat atau memandu.",
              "Gunakan solat jamak dan qasar ketika musafir yang memenuhi syarat, bukannya melewatkan solat.", "Solat Asar sebelum pulang dari pejabat, bukan selepas sampai di rumah ketika matahari sudah kekuningan.")
         + f'<p>Panduan lanjut: <a href="{Q}solat-jamak-qasar/">Solat Jamak & Qasar</a> dan <a href="{Q}belajar-solat/">Belajar Solat langkah demi langkah</a>.</p>'),
    ],
    faq=[("Berdosakah solat di hujung waktu?", "Tidak berdosa jika solat ditunaikan sepenuhnya sebelum waktu tamat, tetapi luput fadhilat awal waktu. Melewatkan Asar hingga matahari kekuningan tanpa uzur adalah makruh, dan sengaja melewatkan solat sehingga keluar waktu ialah dosa besar."),
         ("Apakah azab melewatkan solat?", "Allah mengancam “wail” bagi orang yang lalai daripada solatnya (Al-Ma'un 107:4–5) dan “ghayy” bagi orang yang mensia-siakan solat (Maryam 19:59). Sahabat mentafsirkan kedua-duanya sebagai melewatkan solat daripada waktunya."),
         ("Adakah sah solat jika satu rakaat sahaja dalam waktu?", "Sah dan dikira tunai jika sempat satu rakaat sebelum waktu tamat (HR Al-Bukhari 579), tetapi haram sengaja melewatkannya sehingga begitu."),
         ("Apa yang perlu dibuat jika tertidur dan terlepas waktu solat?", "Tunaikan solat itu sebaik sahaja bangun. Orang yang tertidur atau terlupa tidak berdosa (HR Al-Bukhari 597; Muslim 684)."),
         ("Adakah orang yang meninggalkan solat kafir?", "Menurut mazhab Syafi'i, jika dia mengingkari kewajipannya, dia murtad. Jika kerana malas, dia tidak kafir tetapi melakukan dosa besar yang wajib ditaubati dan solatnya wajib diqada.")],
    refs=["Al-Quran: Al-Ma'un 107:4–5; Maryam 19:59.", "Sahih Al-Bukhari, no. 527, 528, 552, 553, 579, 597, 659, 881.", "Sahih Muslim, no. 82, 85, 224, 608, 622, 626, 667, 684, 2230.",
          "Sunan At-Tirmizi, no. 170, 360, 377, 413, 1862; Sunan Abu Daud, no. 426, 641, 864.", "Tafsir Ibn Kathir, tafsiran Al-Ma'un dan Maryam 59.", "An-Nawawi, Al-Majmu' Syarh Al-Muhadzdzab, bab waktu solat."],
    related=[(Q + "waktu-solat/", "Waktu Solat Malaysia", "Waktu solat hari ini mengikut zon JAKIM"), (Q + "solat-jamak-qasar/", "Solat Jamak & Qasar", "Syarat, cara dan kalkulator jarak"),
             (U["kelebihan-solat"], "Kelebihan Menjaga Solat", "9 kemuliaan orang yang menjaga solat lima waktu")])))

# 2 ---------------------------------------------------------------- Kelebihan menjaga solat
P = "ilmx-ks"
POSTS.append(("kelebihan-solat", base(
    ns=P, url=U["kelebihan-solat"], published="2018-02-11", pubms="11 Februari 2018",
    title="Kelebihan Menjaga Solat: 9 Kemuliaan Menurut Al-Quran & Hadis Sahih",
    desc="Kelebihan menjaga solat lima waktu: menghapus dosa, cahaya pada hari kiamat, janji syurga, jaminan Allah bagi Subuh dan pahala berjemaah, dengan dalil sahih.",
    h1="Kelebihan Menjaga Solat: 9 Kemuliaan",
    img=img("kelebihan-menjaga-solat", "Fadhilat Amal", "Kelebihan Menjaga Solat", "9 kemuliaan menurut Al-Quran & hadis sahih", "حَافِظُوا عَلَى الصَّلَوَاتِ"),
    alt="Kelebihan menjaga solat lima waktu", refshort="Al-Quran, Sahih Al-Bukhari, Sahih Muslim",
    lead="Sembilan kemuliaan bagi orang yang menjaga solat lima waktu, setiap satu dengan ayat Al-Quran atau hadis sahih, serta cara praktikal untuk istiqamah.",
    crumb=("Solat", W + "search/label/Solat"), about=["Kelebihan solat", "Solat lima waktu"],
    answer="Orang yang menjaga solat lima waktu <strong>dihapuskan dosa-dosa kecilnya</strong> seperti mandi lima kali sehari di sungai <em>(HR Al-Bukhari, no. 528; Muslim, no. 667)</em>, "
           "mendapat <strong>janji Allah untuk dimasukkan ke syurga</strong> <em>(HR Abu Daud, no. 1420)</em>, dan termasuk orang beriman yang <strong>mewarisi syurga Firdaus</strong> <em>(Al-Mu'minun 23:9–11)</em>.",
    sections=[
        ("ayat", "Perintah Menjaga Solat dalam Al-Quran",
         qcard(P, "Al-Mu'minun 23:9–11", 23, 9, 11, "Surah Al-Mu'minun, ayat 9–11")
         + "<p>“Menjaga” solat (<em>yuhafizun</em>) bermaksud menunaikannya pada waktunya, dengan syarat, rukun dan khusyuk, serta tidak meninggalkannya. Ia berbeza dengan sekadar “mendirikan” sekali-sekala.</p>"),
        ("kemuliaan", "9 Kemuliaan Orang yang Menjaga Solat",
         "<h3>1. Dosa kecil dihapuskan setiap hari</h3><p>“Bagaimana pendapat kamu jika ada sungai di depan pintu rumah seseorang, dia mandi di dalamnya lima kali sehari, adakah tinggal lagi kotorannya?” "
         "Para sahabat menjawab tidak. Baginda bersabda: “Begitulah solat lima waktu, Allah menghapuskan dengannya kesalahan-kesalahan”" + ref("HR Al-Bukhari, no. 528; Muslim, no. 667") + ".</p>"
         "<h3>2. Penghapus dosa antara dua solat</h3><p>Solat lima waktu, Jumaat ke Jumaat dan Ramadan ke Ramadan menghapuskan dosa di antaranya selagi dosa besar dijauhi" + ref("HR Muslim, no. 233") + ".</p>"
         "<h3>3. Janji Allah untuk masuk syurga</h3><p>“Lima solat yang Allah wajibkan ke atas hamba-hamba-Nya; sesiapa yang menunaikannya tanpa mensia-siakan sedikit pun kerana meremehkannya, "
         "baginya janji di sisi Allah untuk dimasukkan ke syurga”" + ref("HR Abu Daud, no. 1420; An-Nasa'i, no. 461") + ".</p>"
         "<h3>4. Cahaya, bukti dan keselamatan pada hari kiamat</h3><p>“Sesiapa yang menjaganya, baginya cahaya, bukti dan keselamatan pada hari kiamat”" + ref("HR Ahmad, no. 6576; dinilai hasan oleh sebahagian ulama hadis") + ".</p>"
         "<h3>5. Mencegah daripada perbuatan keji dan mungkar</h3>" + qcard(P, "Al-'Ankabut 29:45", 29, 45, 45, "Surah Al-'Ankabut, ayat 45")
         + "<h3>6. Jaminan syurga bagi penjaga Subuh dan Asar</h3><p>“Sesiapa yang menunaikan dua solat yang sejuk (Subuh dan Asar), dia masuk syurga”" + ref("HR Al-Bukhari, no. 574; Muslim, no. 635")
         + ". “Tidak akan masuk neraka seseorang yang solat sebelum terbit matahari dan sebelum terbenamnya”" + ref("HR Muslim, no. 634") + ".</p>"
         "<h3>7. Berada dalam jaminan Allah sepanjang hari</h3><p>“Sesiapa yang solat Subuh, dia berada dalam jaminan Allah”" + ref("HR Muslim, no. 657") + ".</p>"
         "<h3>8. Pahala solat berjemaah 27 kali ganda</h3><p>Solat berjemaah lebih utama daripada solat bersendirian dengan 27 darjat" + ref("HR Al-Bukhari, no. 645; Muslim, no. 650")
         + ". Sesiapa yang solat Isyak berjemaah seperti qiyam separuh malam, dan jika ditambah Subuh berjemaah seperti qiyam sepanjang malam" + ref("HR Muslim, no. 656") + ".</p>"
         "<h3>9. Darjat diangkat dan dosa gugur pada setiap langkah</h3><p>Setiap langkah ke masjid untuk solat, satu langkah menghapus dosa dan satu langkah mengangkat darjat" + ref("HR Muslim, no. 666") + ".</p>"),
        ("ringkas", "Ringkasan Kemuliaan dan Dalilnya",
         grade([("Dosa kecil dihapuskan seperti mandi lima kali sehari", "HR Al-Bukhari 528; Muslim 667", SAHIH), ("Penghapus dosa antara dua solat", "HR Muslim 233", SAHIH),
                ("Janji Allah untuk masuk syurga", "HR Abu Daud 1420; An-Nasa'i 461", SAHIH), ("Cahaya, bukti dan keselamatan pada hari kiamat", "HR Ahmad 6576", HASAN),
                ("Mencegah keji dan mungkar", "Al-'Ankabut 29:45", "✅ Al-Quran"), ("Penjaga Subuh dan Asar masuk syurga", "HR Al-Bukhari 574; Muslim 635", SAHIH),
                ("Dalam jaminan Allah selepas Subuh", "HR Muslim 657", SAHIH), ("Berjemaah 27 darjat", "HR Al-Bukhari 645; Muslim 650", SAHIH),
                ("Setiap langkah ke masjid mengangkat darjat", "HR Muslim 666", SAHIH)], head="Kemuliaan")),
        ("istiqamah", "Cara Istiqamah Menjaga Solat Lima Waktu",
         ul("<strong>Mula dengan waktu yang paling sukar</strong>: kebanyakan orang tewas pada Subuh dan Asar. Pasang dua penggera dan tidur awal.",
            "<strong>Ikat solat dengan rutin</strong>: Zohor sebelum makan tengah hari, Maghrib sebelum makan malam.",
            "<strong>Pelajari maksud bacaan</strong> supaya solat tidak terasa beban. Lihat <a href=\"" + Q + "belajar-solat/\">Belajar Solat</a>.",
            "<strong>Tambah solat sunat rawatib</strong> sebagai pagar kepada solat fardu. Lihat <a href=\"" + Q + "solat-sunat/\">senarai solat sunat</a>.",
            "<strong>Berdoa supaya diberi istiqamah</strong>: doa Nabi Ibrahim “Rabbij'alni muqimas-solati wa min dhurriyyati” (Ibrahim 14:40).")
         + qcard(P, "Doa Nabi Ibrahim: Ibrahim 14:40", 14, 40, 40, "Surah Ibrahim, ayat 40")),
    ],
    faq=[("Apakah kelebihan menjaga solat lima waktu?", "Dosa kecil dihapuskan setiap hari (HR Al-Bukhari 528), dijanjikan syurga (HR Abu Daud 1420), mendapat cahaya pada hari kiamat (HR Ahmad 6576) dan mewarisi syurga Firdaus (Al-Mu'minun 23:9–11)."),
         ("Apakah kelebihan solat Subuh?", "Orang yang solat Subuh berada dalam jaminan Allah (HR Muslim 657), dan penjaga Subuh dan Asar dijanjikan syurga (HR Al-Bukhari 574)."),
         ("Berapa kali ganda pahala solat berjemaah?", "27 darjat lebih utama daripada solat bersendirian (HR Al-Bukhari 645; Muslim 650)."),
         ("Adakah solat menghapuskan dosa besar?", "Tidak. Solat menghapuskan dosa kecil selagi dosa besar dijauhi (HR Muslim 233). Dosa besar memerlukan taubat.")],
    refs=["Al-Quran: Al-Mu'minun 23:9–11; Al-'Ankabut 29:45; Ibrahim 14:40.", "Sahih Al-Bukhari, no. 528, 574, 645.", "Sahih Muslim, no. 233, 634, 635, 650, 656, 657, 666, 667.",
          "Sunan Abu Daud, no. 1420; Sunan An-Nasa'i, no. 461.", "Musnad Ahmad, no. 6576."],
    disclaimer="Status hadis disebut bersama setiap kemuliaan. Riwayat yang tidak dapat disahkan sumbernya telah dibuang daripada versi asal artikel ini.",
    related=[(U["solat-hujung-waktu"], "Solat di Hujung Waktu", "Hukum, azab dan kelebihan solat awal waktu"), (Q + "belajar-solat/", "Belajar Solat", "Panduan solat lengkap dengan bacaan"),
             (Q + "doa-selepas-solat/", "Doa Selepas Solat", "Zikir dan doa ringkas selepas solat fardu")])))

# 3 ---------------------------------------------------------------- Soalan kubur
P = "ilmx-sk"
POSTS.append(("soalan-kubur", base(
    ns=P, url=U["soalan-kubur"], published="2018-02-11", pubms="11 Februari 2018",
    title="Soalan Kubur: 3 Soalan Malaikat Munkar Nakir & Jawapannya",
    desc="Soalan kubur yang ditanya Malaikat Munkar dan Nakir menurut hadis sahih, jawapannya, amalan pelindung azab kubur dan doa untuk si mati selepas dikebumikan.",
    h1="Soalan Kubur: Soalan Munkar Nakir & Jawapannya",
    img=img("soalan-kubur", "Alam Barzakh", "Soalan Kubur", "3 soalan Munkar Nakir & jawapannya", "مَنْ رَبُّكَ"),
    alt="Soalan kubur Malaikat Munkar Nakir dan jawapannya", refshort="Sunan Abu Daud, Sunan At-Tirmizi, Sahih Al-Bukhari",
    lead="Apa sebenarnya yang ditanya dalam kubur, siapa yang bertanya, bagaimana orang beriman diteguhkan, dan amalan sahih untuk berlindung daripada azab kubur.",
    crumb=("Akidah", W + "search/label/Akidah"), about=["Soalan kubur", "Malaikat Munkar dan Nakir", "Alam barzakh"],
    answer="Menurut hadis sahih Al-Bara' bin 'Azib, dua malaikat mendudukkan si mati dan bertanya <strong>tiga soalan</strong>: <strong>Siapa Tuhanmu? Apa agamamu? Siapa lelaki yang diutus kepada kamu?</strong> "
           "Orang beriman menjawab: <strong>Tuhanku Allah, agamaku Islam, dia Rasulullah SAW</strong> <em>(HR Abu Daud, no. 4753; Ahmad, no. 18534)</em>. "
           "Nama malaikat itu, <strong>Munkar dan Nakir</strong>, disebut dalam riwayat At-Tirmizi (no. 1071, hasan).",
    sections=[
        ("soalan", "3 Soalan Kubur dan Jawapannya",
         table(["Soalan (Arab)", "Maksud", "Jawapan orang beriman"], [
             ["مَنْ رَبُّكَ؟", "Siapa Tuhanmu?", "Rabbiyallah: Tuhanku Allah"],
             ["مَا دِينُكَ؟", "Apa agamamu?", "Dini al-Islam: agamaku Islam"],
             ["مَا هٰذَا الرَّجُلُ الَّذِي بُعِثَ فِيكُمْ؟", "Siapa lelaki yang diutus kepada kamu?", "Huwa Rasulullah: dia Rasulullah SAW"]])
         + dc(P, "Jawapan orang beriman", "رَبِّيَ اللّٰهُ، وَدِينِيَ الْإِسْلَامُ، وَنَبِيِّي مُحَمَّدٌ ﷺ", "Rabbiyallah, wa diniyal Islam, wa nabiyyi Muhammad SAW.",
              "Tuhanku Allah, agamaku Islam, dan nabiku Muhammad SAW.", "HR Abu Daud, no. 4753; Ahmad, no. 18534 (sahih)")
         + "<p>Dalam riwayat yang sama, orang beriman ditanya pula: “Bagaimana engkau tahu?” Dia menjawab: “Aku membaca Kitab Allah, lalu aku beriman dan membenarkannya.” "
           "Orang munafik atau yang ragu-ragu pula menjawab: <em>“Hah, hah, aku tidak tahu. Aku dengar orang berkata sesuatu, maka aku pun mengatakannya”</em>" + ref("HR Al-Bukhari, no. 1338; Abu Daud, no. 4753") + ".</p>"),
        ("lima", "Bagaimana dengan “5 Soalan Kubur”?",
         "<p>Senarai lima atau enam soalan (termasuk “Apa kiblatmu?”, “Siapa imammu?” dan “Siapa saudaramu?”) popular dalam kitab-kitab jawi lama dan talqin. "
         "Namun <strong>hadis sahih hanya menyebut tiga soalan</strong> di atas. Soalan tambahan itu tidak salah dari segi makna, tetapi tidak boleh disandarkan kepada Nabi SAW sebagai sabda yang pasti.</p>"
         + grade([("Tiga soalan: Tuhan, agama, nabi", "HR Abu Daud 4753; Ahmad 18534", SAHIH), ("Nama malaikat Munkar dan Nakir", "HR At-Tirmizi 1071", HASAN),
                  ("Soalan tentang kiblat, imam dan saudara", "Kitab jawi dan teks talqin; tiada hadis sahih", NOSRC)])),
        ("teguh", "Orang Beriman Diteguhkan Allah",
         qcard(P, "Ibrahim 14:27", 14, 27, 27, "Surah Ibrahim, ayat 27")
         + "<p>Nabi SAW menjelaskan ayat ini turun berkenaan <strong>azab kubur</strong>: orang beriman ditanya lalu menjawab dengan kalimah tauhid" + ref("HR Al-Bukhari, no. 1369; Muslim, no. 2871")
         + ". Jawapan tidak boleh dihafal pada saat itu; ia lahir daripada iman dan amalan semasa hidup.</p>"),
        ("barzakh", "Apa yang Berlaku di Alam Kubur",
         ul("Si mati mendengar bunyi tapak kasut orang yang pulang selepas pengebumian" + ref("HR Al-Bukhari, no. 1338"),
            "Orang beriman diluaskan kuburnya, ditunjukkan tempatnya di syurga, dan disuruh tidur seperti pengantin" + ref("HR At-Tirmizi, no. 1071"),
            "Setiap orang ditunjukkan tempat duduknya pagi dan petang, sama ada di syurga atau neraka" + ref("HR Al-Bukhari, no. 1379; Muslim, no. 2866"),
            "Kubur ialah persinggahan pertama akhirat; jika selamat di situ, yang selepasnya lebih mudah" + ref("HR At-Tirmizi, no. 2308; hasan")),
         ),
        ("pelindung", "Amalan Pelindung Azab Kubur",
         grade([("Membaca Surah Al-Mulk (30 ayat yang memberi syafaat)", "HR At-Tirmizi 2891; Abu Daud 1400", HASAN),
                ("Mati syahid dilindungi daripada fitnah kubur", "HR An-Nasa'i 2053", SAHIH),
                ("Berjaga di sempadan (ribath) kerana Allah", "HR Muslim 1913", SAHIH),
                ("Mati pada hari atau malam Jumaat dilindungi fitnah kubur", "HR At-Tirmizi 1074; sanadnya lemah, dikuatkan oleh riwayat lain", DHAIF),
                ("Menjaga diri daripada percikan air kencing dan mengadu domba", "HR Al-Bukhari 216; Muslim 292 (punca azab kubur)", SAHIH)], head="Amalan")
         + dc(P, "Doa berlindung daripada azab kubur (sebelum salam)", "اللّٰهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ عَذَابِ جَهَنَّمَ، وَمِنْ عَذَابِ الْقَبْرِ، وَمِنْ فِتْنَةِ الْمَحْيَا وَالْمَمَاتِ، وَمِنْ شَرِّ فِتْنَةِ الْمَسِيحِ الدَّجَّالِ",
              "Allahumma inni a'udhu bika min 'adhabi jahannam, wa min 'adhabil qabr, wa min fitnatil mahya wal mamat, wa min syarri fitnatil masihid-dajjal.",
              "Ya Allah, aku berlindung kepada-Mu daripada azab Jahannam, azab kubur, fitnah kehidupan dan kematian, dan kejahatan fitnah Al-Masih Ad-Dajjal.", "HR Muslim, no. 588")
         + f'<p>Bacaan penuh dan audio: <a href="{Q}surah-al-mulk/">Surah Al-Mulk</a>.</p>'),
        ("si-mati", "Doa untuk Si Mati Selepas Dikebumikan",
         "<p>Selepas pengebumian, Nabi SAW berdiri di sisi kubur dan bersabda: “Mohonlah keampunan untuk saudara kamu dan mintalah ketetapan (iman) untuknya, kerana sekarang dia sedang ditanya”"
         + ref("HR Abu Daud, no. 3221; sahih") + ".</p>"
         + dc(P, "Doa ringkas di sisi kubur", "اللّٰهُمَّ اغْفِرْ لَهُ وَثَبِّتْهُ", "Allahummaghfir lahu wa thabbit-hu.", "Ya Allah, ampunilah dia dan teguhkanlah dia.", "Berdasarkan HR Abu Daud, no. 3221")
         + "<p>Dalam mazhab Syafi'i, <strong>talqin</strong> selepas pengebumian dihukum sunat oleh Imam An-Nawawi dan ulama Syafi'iyyah, walaupun hadisnya lemah, kerana ia termasuk fadhilat amal dan peringatan kepada yang hadir.</p>"
         + f'<p>Doa dan adab menziarahi kubur: <a href="{Q}doa-ziarah-kubur/">Doa Ziarah Kubur</a>. Tahlil untuk arwah: <a href="{Q}tahlil-ringkas/">Tahlil Ringkas</a>.</p>'),
    ],
    faq=[("Apakah soalan dalam kubur?", "Tiga soalan: Siapa Tuhanmu? Apa agamamu? Siapa lelaki yang diutus kepada kamu? Orang beriman menjawab: Tuhanku Allah, agamaku Islam, dia Rasulullah SAW (HR Abu Daud 4753)."),
         ("Siapakah malaikat yang menyoal dalam kubur?", "Munkar dan Nakir, sebagaimana disebut dalam HR At-Tirmizi 1071 (hasan)."),
         ("Adakah soalan kubur ada lima?", "Hadis sahih menyebut tiga soalan. Soalan tambahan tentang kiblat, imam dan saudara terdapat dalam kitab jawi dan teks talqin, bukan hadis sahih."),
         ("Apakah amalan untuk selamat daripada azab kubur?", "Membaca Surah Al-Mulk (HR At-Tirmizi 2891), berdoa berlindung daripada azab kubur sebelum salam (HR Muslim 588), menjaga kebersihan daripada air kencing dan menjauhi mengadu domba (HR Al-Bukhari 216)."),
         ("Apakah doa selepas mengebumikan jenazah?", "Mohon keampunan dan ketetapan iman untuk si mati, contohnya “Allahummaghfir lahu wa thabbit-hu”, berdasarkan HR Abu Daud 3221.")],
    refs=["Al-Quran: Ibrahim 14:27.", "Sunan Abu Daud, no. 1400, 3221, 4753; Musnad Ahmad, no. 18534.", "Sahih Al-Bukhari, no. 216, 1338, 1369, 1379.",
          "Sahih Muslim, no. 292, 588, 1913, 2866, 2871.", "Sunan At-Tirmizi, no. 1071, 1074, 2308, 2891; Sunan An-Nasa'i, no. 2053.", "An-Nawawi, Al-Adzkar, bab talqin."],
    disclaimer="Panduan akidah ringkas mengikut Ahli Sunnah wal Jamaah. Hadis yang lemah disebut bersama statusnya.",
    related=[(Q + "surah-al-mulk/", "Surah Al-Mulk", "Bacaan, terjemahan dan audio"), (Q + "doa-ziarah-kubur/", "Doa Ziarah Kubur", "Bacaan dan adab ziarah"),
             (U["tanda-kiamat"], "Tanda-Tanda Kiamat", "Senarai tanda kecil dan besar dengan hadis sahih")])))

# 4 ---------------------------------------------------------------- Tanda kiamat (absorbs 3 merged posts)
P = "ilmx-tk"
POSTS.append(("tanda-kiamat", base(
    ns=P, url=U["tanda-kiamat"], published="2017-12-06", pubms="6 Disember 2017",
    title="Tanda-Tanda Kiamat Kecil & Besar: Senarai Lengkap Hadis Sahih",
    desc="Tanda-tanda kiamat kecil yang telah dan sedang berlaku, 10 tanda kiamat besar menurut Sahih Muslim, dan cara menghadapinya, dengan sumber hadis setiap tanda.",
    h1="Tanda-Tanda Kiamat Kecil & Besar",
    img=img("tanda-tanda-kiamat", "Akidah", "Tanda-Tanda Kiamat", "Tanda kecil dan 10 tanda besar menurut hadis sahih", "أَشْرَاطُ السَّاعَةِ"),
    alt="Tanda-tanda kiamat kecil dan besar menurut hadis sahih", refshort="Sahih Al-Bukhari, Sahih Muslim",
    lead="Senarai tanda kiamat kecil dan besar yang thabit dalam hadis sahih, mana yang telah berlaku, dan mengapa tiada sesiapa boleh menentukan tarikh kiamat.",
    crumb=("Akidah", W + "search/label/Akidah"), about=["Tanda-tanda kiamat", "Tanda kiamat kecil", "Tanda kiamat besar"],
    answer="Tanda kiamat terbahagi dua. <strong>Tanda kecil</strong> berlaku lama sebelum kiamat dan banyak yang telah berlaku, seperti diutusnya Nabi Muhammad SAW, ilmu agama diangkat, zina dan arak berleluasa, "
           "dan orang berlumba membina bangunan tinggi <em>(HR Al-Bukhari, no. 81; Muslim, no. 8)</em>. <strong>Tanda besar</strong> ada sepuluh dan berlaku berturut-turut hampir dengan kiamat: "
           "asap, Dajjal, binatang (dabbah), matahari terbit dari barat, turunnya Nabi Isa AS, Ya'juj dan Ma'juj, tiga gerhana bumi dan api dari Yaman <em>(HR Muslim, no. 2901)</em>.",
    sections=[
        ("ayat", "Tanda-Tandanya Telah Datang",
         qcard(P, "Muhammad 47:18", 47, 18, 18, "Surah Muhammad, ayat 18")
         + "<p>Nabi SAW bersabda: “Aku diutus, dan hari kiamat seperti dua ini,” sambil merapatkan jari telunjuk dan jari tengah" + ref("HR Al-Bukhari, no. 6504; Muslim, no. 2951")
         + ". Kerasulan Baginda sendiri ialah tanda kiamat yang pertama.</p>"),
        ("kecil", "Tanda-Tanda Kiamat Kecil",
         table(["Tanda", "Sumber", "Keadaan"], [
             ["Diutusnya Nabi Muhammad SAW dan kewafatan Baginda", "HR Al-Bukhari 6504, 3176", "Telah berlaku"],
             ["Bulan terbelah dua", "Al-Qamar 54:1; HR Al-Bukhari 3637", "Telah berlaku"],
             ["Pembukaan Baitulmaqdis", "HR Al-Bukhari 3176", "Telah berlaku (zaman Khalifah Umar RA, 15–16H)"],
             ["Wabak yang membunuh ramai seperti penyakit kambing", "HR Al-Bukhari 3176", "Ulama menyebut wabak 'Amwas (18H)"],
             ["Api besar di Hijaz yang meneranginya hingga ke Busra", "HR Al-Bukhari 7118; Muslim 2902", "Ulama menyebut letusan di Madinah tahun 654H"],
             ["Amanah disia-siakan, urusan diserahkan kepada yang bukan ahlinya", "HR Al-Bukhari 59", "Sedang berlaku"],
             ["Ilmu agama diangkat, kejahilan, arak dan zina berleluasa", "HR Al-Bukhari 81; Muslim 2671", "Sedang berlaku"],
             ["Penggembala kambing yang miskin berlumba-lumba membina bangunan tinggi", "HR Muslim 8", "Sedang berlaku"],
             ["Masa terasa singkat, banyak pembunuhan (harj) dan gempa bumi", "HR Al-Bukhari 1036, 7121", "Sedang berlaku"],
             ["Orang bermegah-megah dengan masjid", "HR Abu Daud 449", "Sedang berlaku"],
             ["Bilangan wanita ramai sehingga 50 wanita diuruskan seorang lelaki", "HR Al-Bukhari 81", "Belum sepenuhnya"],
             ["Sungai Furat mendedahkan gunung emas yang menjadi rebutan", "HR Al-Bukhari 7119; Muslim 2894", "Belum berlaku"],
             ["Tanah Arab kembali menjadi padang rumput dan sungai", "HR Muslim 1012", "Mula kelihatan; ulama berbeza pandangan"],
             ["Orang lalu di kubur lalu berkata: alangkah baiknya jika aku di tempatnya", "HR Al-Bukhari 7115", "Belum sepenuhnya"]])
         + "<p>Pembukaan Baitulmaqdis sering disebut sebagai “tanda besar” dalam tulisan lama. Hadis Al-Bukhari no. 3176 menyenaraikannya bersama enam perkara sebelum kiamat, "
           "dan ia ialah <strong>tanda kecil yang telah berlaku</strong>, bukan salah satu daripada sepuluh tanda besar.</p>"),
        ("besar", "10 Tanda Kiamat Besar",
         "<p>Huzaifah bin Asid RA meriwayatkan bahawa Nabi SAW bersabda kiamat tidak berlaku sehingga kamu melihat sepuluh tanda" + ref("HR Muslim, no. 2901") + ":</p>"
         + ul("Asap (dukhan)", "Dajjal", "Binatang yang keluar dari bumi (dabbatul ardh)", "Matahari terbit dari barat", "Turunnya Nabi Isa bin Maryam AS", "Ya'juj dan Ma'juj",
              "Gerhana bumi (tanah runtuh) di timur", "Gerhana bumi di barat", "Gerhana bumi di Semenanjung Arab",
              "Api yang keluar dari Yaman, menghalau manusia ke tempat mereka dihimpunkan", ordered=True)
         + "<p>Kemunculan <strong>Imam Mahdi</strong> pula disebut dalam hadis-hadis sunan seperti HR Abu Daud no. 4282 (hasan) dan diterima oleh Ahli Sunnah wal Jamaah. "
           "Selepas matahari terbit dari barat, pintu taubat ditutup" + ref("HR Muslim, no. 157 dan 2703") + ".</p>"
         + f'<p>Perlindungan daripada Dajjal: hafal 10 ayat awal <a href="{Q}surah-al-kahfi/">Surah Al-Kahfi</a>' + ref("HR Muslim, no. 809") + " dan baca doa berlindung sebelum salam" + ref("HR Muslim, no. 588") + ".</p>"),
        ("haudh", "Golongan yang Dihalau dari Telaga Nabi SAW",
         "<p>Nabi SAW bersabda akan ada sebahagian umatnya yang dihalau dari telaga (Al-Haudh) pada hari kiamat. Baginda berkata: “Mereka umatku!” lalu dijawab: "
         "“Engkau tidak tahu apa yang mereka ada-adakan selepasmu”" + ref("HR Al-Bukhari, no. 6585; Muslim, no. 2304") + ". Ulama menjelaskan mereka ialah orang yang mengubah agama dan mengada-adakan bidaah dalam akidah, "
         "maka berpegang dengan Al-Quran dan Sunnah ialah jalan selamat.</p>"),
        ("tarikh", "Tiada Siapa Tahu Bila Kiamat",
         "<p>Allah berfirman pengetahuan tentang kiamat hanya di sisi-Nya" + ref("Al-A'raf 7:187; Luqman 31:34")
         + ". Apabila Jibril bertanya bila kiamat, Nabi SAW menjawab: “Orang yang ditanya tidak lebih mengetahui daripada yang bertanya”" + ref("HR Muslim, no. 8") + ".</p>"
         + f'<div class="{P}-box amber">Berhati-hati dengan ramalan tarikh kiamat, “urutan tepat” tanda kecil, dan mesej berantai yang mengaitkan berita semasa dengan tanda tertentu. '
           "Tiada hadis sahih yang menetapkan urutan tanda kecil, dan menentukan tarikh kiamat bercanggah dengan Al-Quran.</div>"),
        ("bersedia", "Cara Menghadapi Tanda-Tanda Kiamat",
         "<p>Seorang lelaki bertanya bila kiamat. Nabi SAW bertanya kembali: “Apa yang telah engkau sediakan untuknya?” Dia menjawab: “Cintaku kepada Allah dan Rasul-Nya.” "
         "Baginda bersabda: “Engkau bersama orang yang engkau cintai”" + ref("HR Al-Bukhari, no. 3688; Muslim, no. 2639") + ".</p>"
         + ul("Jaga solat lima waktu dan bertaubat sebelum pintunya ditutup.", "Pelajari ilmu agama daripada guru yang muktabar kerana ilmu akan diangkat.",
              "Segera beramal sebelum datang fitnah seperti malam yang gelap" + ref("HR Muslim, no. 118"), "Jangan panik dengan berita; fokus pada amalan yang boleh dikawal.")),
    ],
    faq=[("Apakah tanda-tanda kiamat kecil?", "Antaranya diutusnya Nabi Muhammad SAW, bulan terbelah, pembukaan Baitulmaqdis, amanah disia-siakan, ilmu diangkat, zina dan arak berleluasa, berlumba membina bangunan tinggi dan banyak pembunuhan (HR Al-Bukhari 81, 3176; Muslim 8)."),
         ("Apakah 10 tanda kiamat besar?", "Asap, Dajjal, dabbatul ardh, matahari terbit dari barat, turunnya Nabi Isa AS, Ya'juj dan Ma'juj, tiga gerhana bumi (timur, barat, Semenanjung Arab) dan api dari Yaman (HR Muslim 2901)."),
         ("Adakah tanda kiamat kecil sudah lengkap?", "Banyak tanda kecil telah berlaku, tetapi beberapa belum, seperti Sungai Furat mendedahkan gunung emas (HR Al-Bukhari 7119). Tiada siapa boleh memastikan semuanya telah lengkap."),
         ("Adakah pembukaan Baitulmaqdis tanda kiamat besar?", "Tidak. Ia tanda kecil yang telah berlaku pada zaman Khalifah Umar RA (HR Al-Bukhari 3176)."),
         ("Bilakah kiamat akan berlaku?", "Hanya Allah yang mengetahuinya (Al-A'raf 7:187). Sebarang ramalan tarikh kiamat bercanggah dengan Al-Quran.")],
    refs=["Al-Quran: Muhammad 47:18; Al-Qamar 54:1; Al-A'raf 7:187; Luqman 31:34.", "Sahih Al-Bukhari, no. 59, 81, 1036, 3176, 3637, 3688, 6504, 6585, 7115, 7118, 7119, 7121.",
          "Sahih Muslim, no. 8, 118, 157, 1012, 588, 809, 2304, 2639, 2671, 2703, 2894, 2901, 2902, 2951.", "Sunan Abu Daud, no. 449, 4282."],
    disclaimer="Artikel ini menggabungkan tiga artikel lama tentang tanda kiamat. Keadaan “telah berlaku” berdasarkan pandangan ulama yang masyhur; Allah lebih mengetahui.",
    related=[(U["soalan-kubur"], "Soalan Kubur", "3 soalan Munkar Nakir dan jawapannya"), (Q + "surah-al-kahfi/", "Surah Al-Kahfi", "Pelindung daripada fitnah Dajjal"),
             (U["kaum-dibinasakan"], "Kaum yang Dibinasakan Allah", "Iktibar daripada umat terdahulu")])))

# 5 ---------------------------------------------------------------- Masuk syurga tanpa hisab
P = "ilmx-th"
POSTS.append(("syurga-tanpa-hisab", base(
    ns=P, url=U["syurga-tanpa-hisab"], published="2018-01-28", pubms="28 Januari 2018",
    title="Masuk Syurga Tanpa Hisab: 70,000 Golongan & 4 Sifat Mereka (Sahih)",
    desc="Siapa 70,000 umat yang masuk syurga tanpa hisab menurut Sahih Al-Bukhari dan Muslim, 4 sifat mereka, dan semakan status senarai 11 golongan yang tular.",
    h1="Masuk Syurga Tanpa Hisab: 70,000 Golongan",
    img=img("syurga-tanpa-hisab", "Akhirat", "Masuk Syurga Tanpa Hisab", "70,000 golongan & 4 sifat mereka", "بِغَيْرِ حِسَابٍ"),
    alt="Golongan masuk syurga tanpa hisab menurut hadis sahih", refshort="Sahih Al-Bukhari, Sahih Muslim",
    lead="Hadis sahih tentang 70,000 umat Nabi SAW yang masuk syurga tanpa hisab, empat sifat mereka, dan semakan jujur terhadap senarai 11 golongan yang tersebar.",
    crumb=("Akidah", W + "search/label/Akidah"), about=["Masuk syurga tanpa hisab", "70,000 umat", "Tawakal"],
    answer="Nabi SAW bersabda <strong>70,000 orang daripada umatnya masuk syurga tanpa hisab dan tanpa azab</strong>. Mereka ialah orang yang <strong>tidak meminta diruqyah, tidak bertathayyur (percaya sial), "
           "tidak berubat dengan besi panas (kay), dan kepada Tuhan mereka bertawakal</strong> <em>(HR Al-Bukhari, no. 5705, 6541; Muslim, no. 218, 220)</em>. Wajah mereka bercahaya seperti bulan purnama <em>(HR Al-Bukhari, no. 6542)</em>.",
    sections=[
        ("hadis", "Hadis 70,000 Masuk Syurga Tanpa Hisab",
         "<p>Ibn Abbas RA meriwayatkan bahawa Nabi SAW diperlihatkan umat-umat terdahulu, lalu diperlihatkan umat Baginda yang sangat ramai. Dikatakan: “Ini umatmu, dan bersama mereka "
         "70,000 orang yang masuk syurga tanpa hisab dan tanpa azab.” Para sahabat berbincang siapa mereka, lalu Nabi SAW bersabda: “Mereka ialah orang yang tidak meminta diruqyah, tidak bertathayyur, "
         "tidak berubat dengan kay, dan kepada Tuhan mereka bertawakal.” Ukkasyah bin Mihsan RA berdiri dan meminta didoakan, Baginda bersabda: “Engkau termasuk mereka”" + ref("HR Al-Bukhari, no. 5705; Muslim, no. 220") + ".</p>"
         "<p>Dalam riwayat lain, Allah menambah: <strong>bersama setiap seribu daripada mereka, 70,000 lagi</strong>, ditambah tiga cedokan (hatsiyah) daripada cedokan Tuhan" + ref("HR At-Tirmizi, no. 2437; hasan") + ". Ini menunjukkan rahmat Allah lebih luas daripada angka 70,000.</p>"),
        ("sifat", "4 Sifat Mereka dan Maksudnya",
         table(["Sifat", "Maksud", "Nota fiqh"], [
             ["Tidak meminta diruqyah", "Tidak bergantung kepada orang lain untuk menjampi mereka", "Ruqyah syar'iyyah tetap harus; Nabi SAW sendiri meruqyah dan diruqyah. Yang dipuji ialah tahap tawakal yang tinggi."],
             ["Tidak bertathayyur", "Tidak percaya sial pada burung, nombor, hari, bunyi binatang atau kejadian", "Tathayyur ialah syirik kecil (HR Abu Daud 3910)"],
             ["Tidak berubat dengan kay", "Tidak memilih rawatan besi panas selagi ada rawatan lain", "Berubat tetap disuruh: “Berubatlah, kerana Allah tidak menurunkan penyakit tanpa ubatnya” (HR Abu Daud 3855)"],
             ["Bertawakal kepada Allah", "Hati bergantung sepenuhnya kepada Allah selepas berusaha", "Sifat ini ialah punca kepada tiga sifat sebelumnya"]])
         + "<p>Kesimpulan ulama: hadis ini memuji <strong>kekuatan tawakal</strong>, bukan melarang berubat. Orang yang berubat di hospital tidak terkeluar daripada golongan ini.</p>"),
        ("semakan", "Semakan Senarai “11 Golongan Masuk Syurga Tanpa Hisab”",
         "<p>Versi lama artikel ini menyenaraikan 11 golongan. Selepas disemak, kebanyakannya <strong>tiada sumber sahih yang menyebut “tanpa hisab”</strong>. Ada yang mempunyai ganjaran besar tetapi dengan lafaz lain:</p>"
         + grade([("Orang yang bersabar", "Az-Zumar 39:10: pahala orang sabar disempurnakan tanpa batas (bighairi hisab)", "✅ Al-Quran"),
                  ("Orang yang berkasih sayang kerana Allah", "HR Muslim 2566: dinaungi Allah pada hari kiamat (bukan lafaz tanpa hisab)", SAHIH),
                  ("Orang yang mati syahid", "HR At-Tirmizi 1663: diampunkan pada titisan darah pertama dan dilindungi azab kubur", SAHIH),
                  ("Ahli kemuliaan (ahl al-fadl) dan jiran Allah", "Riwayat Abu Nu'aim dan lain-lain", DHAIF),
                  ("Mati dalam perjalanan ke Mekah", "Tidak ditemui dengan lafaz tanpa hisab", NOSRC),
                  ("Penuntut ilmu, isteri taat dan anak yang berbakti", "Tidak ditemui dengan lafaz tanpa hisab", NOSRC),
                  ("Mengasuh kanak-kanak hingga mengucap la ilaha illallah", "Tidak ditemui sanad yang sahih", NOSRC),
                  ("Mati pada hari Jumaat", "HR At-Tirmizi 1074 menyebut perlindungan fitnah kubur, bukan tanpa hisab; sanadnya lemah", DHAIF),
                  ("Menggali perigi kerana Allah", "Tidak ditemui dengan lafaz tanpa hisab", NOSRC)], head="Golongan dalam senarai lama")
         + f'<div class="{P}-box amber">Kami memadam senarai lama kerana kebanyakan riwayatnya tidak dapat disahkan. Menyandarkan janji “tanpa hisab” kepada Nabi SAW tanpa sumber sahih adalah perkara yang berat.</div>'),
        ("hisab", "Hisab Mudah dan Hisab Teliti",
         "<p>Bagi yang tidak termasuk 70,000, masih ada harapan besar. Allah berfirman orang yang menerima kitab dengan tangan kanan akan dihisab dengan <strong>hisab yang mudah</strong>"
         + ref("Al-Insyiqaq 84:7–8") + ". Nabi SAW bersabda: “Sesiapa yang dihisab (secara teliti), dia akan diazab.” Aisyah RA bertanya tentang ayat hisab yang mudah, Baginda menjawab: "
         "“Itu hanyalah pembentangan (al-'ardh)”" + ref("HR Al-Bukhari, no. 103; Muslim, no. 2876") + ".</p>"
         + qcard(P, "Az-Zumar 39:10", 39, 10, 10, "Surah Az-Zumar, ayat 10")),
        ("amal", "Amalan Membina Tawakal",
         ul("Ikat unta, kemudian bertawakal: berusaha dahulu, kemudian serahkan hasil kepada Allah" + ref("HR At-Tirmizi, no. 2517; hasan"),
            "Buang kepercayaan sial: nombor 4, burung hantu, kucing hitam, rumah “panas” dan seumpamanya.",
            "Amalkan zikir pagi dan petang, termasuk “Hasbiyallahu la ilaha illa huwa, 'alaihi tawakkaltu”.",
            "Jika berubat dengan ruqyah, utamakan meruqyah diri sendiri dengan Al-Fatihah dan Al-Mu'awwidzat.")
         + f'<p>Bacaan zikir lengkap: <a href="{Q}zikir-pagi-petang/">Zikir Pagi Petang</a>.</p>'),
    ],
    faq=[("Siapakah yang masuk syurga tanpa hisab?", "70,000 umat Nabi SAW yang tidak meminta diruqyah, tidak bertathayyur, tidak berubat dengan kay, dan bertawakal kepada Allah (HR Al-Bukhari 5705; Muslim 220)."),
         ("Adakah berubat menghalang seseorang masuk syurga tanpa hisab?", "Tidak. Berubat disuruh oleh Nabi SAW (HR Abu Daud 3855). Hadis ini memuji tahap tawakal yang tinggi, bukan melarang rawatan."),
         ("Benarkah hanya 70,000 orang?", "Riwayat At-Tirmizi (2437, hasan) menyebut bersama setiap seribu, 70,000 lagi, ditambah tiga cedokan daripada Allah. Rahmat Allah lebih luas daripada angka 70,000."),
         ("Adakah senarai 11 golongan masuk syurga tanpa hisab sahih?", "Kebanyakannya tiada sumber sahih dengan lafaz “tanpa hisab”. Yang thabit dengan jelas ialah empat sifat dalam hadis Al-Bukhari dan Muslim, dan pahala orang sabar tanpa batas (Az-Zumar 39:10).")],
    refs=["Al-Quran: Az-Zumar 39:10; Al-Insyiqaq 84:7–8.", "Sahih Al-Bukhari, no. 103, 5705, 6541, 6542.", "Sahih Muslim, no. 216, 218, 220, 2566, 2876.",
          "Sunan At-Tirmizi, no. 1074, 1663, 2437, 2517.", "Sunan Abu Daud, no. 3855, 3910."],
    related=[(W + "2020/02/tanda-tanda-gangguan-jin-sihir.html", "Ruqyah Syar'iyyah", "Rawatan yang menepati syarak"), (Q + "zikir-pagi-petang/", "Zikir Pagi Petang", "Zikir tawakal dan perlindungan"),
             (U["didoakan-malaikat"], "Golongan yang Didoakan Malaikat", "10 amalan menurut hadis sahih")])))

# 6 ---------------------------------------------------------------- Didoakan malaikat
P = "ilmx-dm"
POSTS.append(("didoakan-malaikat", base(
    ns=P, url=U["didoakan-malaikat"], published="2017-11-28", pubms="28 November 2017",
    title="10 Golongan Yang Didoakan Malaikat Menurut Hadis Sahih",
    desc="Golongan yang didoakan malaikat: menunggu solat, saf hadapan, bersedekah, mendoakan saudara, menziarahi orang sakit dan mengajar kebaikan, dengan sumber hadis.",
    h1="10 Golongan yang Didoakan Malaikat",
    img=img("didoakan-malaikat", "Amalan Harian", "Golongan Didoakan Malaikat", "10 amalan menurut hadis sahih", "وَمَلَائِكَتُهُ"),
    alt="Golongan yang didoakan malaikat menurut hadis sahih", refshort="Sahih Al-Bukhari, Sahih Muslim, Sunan At-Tirmizi",
    lead="Sepuluh amalan ringan yang menjadikan malaikat mendoakan anda, setiap satu dengan hadis dan statusnya, serta cara menyusunnya dalam rutin harian.",
    crumb=("Amalan", W + "search/label/Amalan"), about=["Didoakan malaikat", "Amalan harian"],
    answer="Antara golongan yang didoakan malaikat menurut hadis sahih ialah <strong>orang yang duduk menunggu solat</strong> <em>(HR Al-Bukhari, no. 659)</em>, <strong>orang yang mendoakan saudaranya tanpa pengetahuannya</strong> "
           "<em>(HR Muslim, no. 2733)</em>, <strong>orang yang bersedekah</strong> <em>(HR Al-Bukhari, no. 1442)</em>, <strong>orang yang menziarahi orang sakit</strong> <em>(HR At-Tirmizi, no. 969)</em> "
           "dan <strong>orang yang mengajar kebaikan</strong> <em>(HR At-Tirmizi, no. 2685)</em>.",
    sections=[
        ("ayat", "Malaikat Mendoakan Orang Beriman",
         qcard(P, "Al-Ahzab 33:43", 33, 43, 43, "Surah Al-Ahzab, ayat 43")
         + "<p>Malaikat pemikul Arasy juga memohon keampunan bagi orang beriman yang bertaubat" + ref("Ghafir 40:7") + ". “Selawat” malaikat bermaksud doa dan permohonan ampun.</p>"),
        ("senarai", "10 Golongan yang Didoakan Malaikat",
         "<h3>1. Orang yang duduk menunggu solat</h3><p>Malaikat berdoa: “Ya Allah, ampunilah dia. Ya Allah, rahmatilah dia,” selagi dia di tempat solatnya dan tidak berhadas" + ref("HR Al-Bukhari, no. 659; Muslim, no. 649") + ".</p>"
         "<h3>2. Orang di saf hadapan</h3><p>“Sesungguhnya Allah dan malaikat-Nya berselawat ke atas saf-saf hadapan”" + ref("HR Abu Daud, no. 664") + ".</p>"
         "<h3>3. Orang yang menyambung saf</h3><p>“Sesungguhnya Allah dan malaikat-Nya berselawat ke atas orang yang menyambung saf”" + ref("HR Ibn Majah, no. 995; Ahmad") + ".</p>"
         "<h3>4. Orang yang aminnya serentak dengan malaikat</h3><p>“Apabila imam membaca ghairil maghdhubi 'alaihim wa lad-dhallin, maka ucapkanlah amin; sesiapa yang aminnya serentak dengan amin malaikat, diampunkan dosanya yang lalu”"
         + ref("HR Al-Bukhari, no. 780; Muslim, no. 410") + ".</p>"
         "<h3>5. Orang yang mendoakan saudaranya tanpa pengetahuannya</h3><p>Malaikat yang diwakilkan berkata: “Amin, dan bagimu seperti itu”" + ref("HR Muslim, no. 2733") + ".</p>"
         "<h3>6. Orang yang bersedekah</h3><p>Setiap pagi dua malaikat turun; seorang berdoa: “Ya Allah, berilah ganti kepada orang yang berinfak”" + ref("HR Al-Bukhari, no. 1442; Muslim, no. 1010") + ".</p>"
         "<h3>7. Orang yang menziarahi orang sakit</h3><p>Sesiapa yang menziarahi orang sakit pada waktu pagi, 70,000 malaikat berdoa untuknya hingga petang; jika petang, hingga pagi" + ref("HR At-Tirmizi, no. 969; hasan") + ".</p>"
         "<h3>8. Orang yang mengajar kebaikan</h3><p>“Sesungguhnya Allah, malaikat-Nya, penghuni langit dan bumi, hingga semut dalam lubangnya dan ikan, berselawat ke atas orang yang mengajar kebaikan kepada manusia”"
         + ref("HR At-Tirmizi, no. 2685; hasan sahih") + ".</p>"
         "<h3>9. Orang yang tidur dalam keadaan suci</h3><p>Malaikat bermalam bersamanya dan berdoa: “Ya Allah, ampunilah hamba-Mu si fulan kerana dia tidur dalam keadaan suci”" + ref("HR Ibn Hibban, no. 1051; hasan") + ".</p>"
         "<h3>10. Orang yang bersahur dan orang yang berselawat</h3><p>Allah dan malaikat berselawat ke atas orang yang bersahur" + ref("HR Ahmad, no. 11086; Ibn Hibban") + ", dan malaikat berselawat ke atas orang yang berselawat kepada Nabi SAW selama dia berselawat"
         + ref("HR Ibn Majah, no. 907; Ahmad") + ".</p>"),
        ("status", "Ringkasan dan Status Hadis",
         grade([("Menunggu solat", "HR Al-Bukhari 659; Muslim 649", SAHIH), ("Saf hadapan", "HR Abu Daud 664", SAHIH), ("Menyambung saf", "HR Ibn Majah 995", HASAN),
                ("Amin serentak dengan malaikat", "HR Al-Bukhari 780; Muslim 410", SAHIH), ("Mendoakan saudara secara rahsia", "HR Muslim 2733", SAHIH),
                ("Bersedekah", "HR Al-Bukhari 1442; Muslim 1010", SAHIH), ("Menziarahi orang sakit", "HR At-Tirmizi 969", HASAN), ("Mengajar kebaikan", "HR At-Tirmizi 2685", SAHIH),
                ("Tidur dalam keadaan suci", "HR Ibn Hibban 1051", HASAN), ("Bersahur", "HR Ahmad 11086", HASAN), ("Berselawat kepada Nabi SAW", "HR Ibn Majah 907", HASAN)], head="Golongan")
         + "<p>Nota: hadis malaikat bergilir pada waktu Subuh dan Asar" + ref("HR Al-Bukhari, no. 555; Muslim, no. 632")
           + " menyebut malaikat <strong>melaporkan</strong> bahawa mereka mendapati hamba sedang solat. Ia kemuliaan besar, tetapi lafaznya bukan doa, maka kami tidak memasukkannya dalam senarai.</p>"),
        ("rutin", "Susun dalam Rutin Harian",
         table(["Masa", "Amalan"], [["Sebelum tidur", "Ambil wuduk (no. 9) dan doakan seorang sahabat secara rahsia (no. 5)"],
                                    ["Subuh", "Datang awal, duduk menunggu solat (no. 1), pilih saf hadapan (no. 2)"],
                                    ["Pagi", "Sedekah kecil, walaupun RM1 secara dalam talian (no. 6)"],
                                    ["Hujung minggu", "Ziarah saudara atau jiran yang sakit (no. 7)"],
                                    ["Bila-bila masa", "Kongsi ilmu yang sahih (no. 8) dan perbanyak selawat (no. 10)"]])
         + f'<p>Bacaan doa ziarah orang sakit: <a href="{Q}doa-orang-sakit/">Doa Orang Sakit</a>.</p>'),
    ],
    faq=[("Siapakah yang didoakan malaikat?", "Antaranya orang yang menunggu solat, di saf hadapan, mendoakan saudara secara rahsia, bersedekah, menziarahi orang sakit dan mengajar kebaikan (HR Al-Bukhari 659, 1442; Muslim 2733; At-Tirmizi 969, 2685)."),
         ("Apakah doa malaikat untuk orang yang menunggu solat?", "“Ya Allah, ampunilah dia. Ya Allah, rahmatilah dia” (HR Al-Bukhari 659)."),
         ("Berapa malaikat mendoakan orang yang menziarahi orang sakit?", "70,000 malaikat, hingga petang jika ziarah pada waktu pagi, dan hingga pagi jika ziarah pada waktu petang (HR At-Tirmizi 969)."),
         ("Apakah maksud malaikat berselawat?", "Selawat malaikat bermaksud doa dan permohonan ampun untuk orang beriman (Al-Ahzab 33:43).")],
    refs=["Al-Quran: Al-Ahzab 33:43; Ghafir 40:7.", "Sahih Al-Bukhari, no. 555, 659, 780, 1442.", "Sahih Muslim, no. 410, 632, 649, 1010, 2733.",
          "Sunan At-Tirmizi, no. 969, 2685; Sunan Abu Daud, no. 664; Sunan Ibn Majah, no. 907, 995.", "Sahih Ibn Hibban, no. 1051; Musnad Ahmad, no. 11086."],
    related=[(U["syurga-tanpa-hisab"], "Masuk Syurga Tanpa Hisab", "70,000 golongan dan 4 sifat mereka"), (Q + "doa-orang-sakit/", "Doa Orang Sakit", "Doa ketika menziarahi pesakit"),
             (U["kelebihan-solat"], "Kelebihan Menjaga Solat", "9 kemuliaan orang yang menjaga solat")])))

# 7 ---------------------------------------------------------------- Kaum yang dibinasakan
P = "ilmx-kb"
POSTS.append(("kaum-dibinasakan", base(
    ns=P, url=U["kaum-dibinasakan"], published="2020-01-18", pubms="18 Januari 2020",
    title="12 Kaum Yang Dibinasakan Allah: Kaum Nabi Nuh, Ad, Tsamud & Luth",
    desc="12 kaum yang dibinasakan Allah dalam Al-Quran: kaum Nabi Nuh, Ad, Tsamud, kaum Nabi Luth, Madyan, Firaun, Saba' dan lain-lain, dengan dosa, azab dan ayatnya.",
    h1="12 Kaum yang Dibinasakan Allah",
    img=img("kaum-dibinasakan-allah", "Kisah Al-Quran", "12 Kaum Dibinasakan Allah", "Dosa, azab dan iktibar daripada umat terdahulu", "فَكُلًّا أَخَذْنَا بِذَنْبِهِ"),
    alt="12 kaum yang dibinasakan Allah dalam Al-Quran", refshort="Al-Quran, Sahih Al-Bukhari",
    lead="Kisah 12 kaum yang dibinasakan Allah, disusun dalam satu jadual dosa dan azab, dengan huraian kaum Nabi Luth dan ayat rujukan untuk setiap kisah.",
    crumb=("Kisah", W + "search/label/Kisah"), about=["Kaum yang dibinasakan Allah", "Kaum Nabi Luth", "Kisah para nabi"],
    answer="Al-Quran merangkumkan azab umat terdahulu dalam satu ayat: <strong>ada yang dihujani batu (kaum Luth), ada yang dibinasakan dengan pekikan (Tsamud dan Madyan), ada yang ditelan bumi (Qarun) "
           "dan ada yang ditenggelamkan (kaum Nuh dan Firaun)</strong>; Allah tidak menzalimi mereka, merekalah yang menzalimi diri sendiri <em>(Al-'Ankabut 29:40)</em>.",
    sections=[
        ("ayat", "Ayat yang Merangkumkan Azab Umat Terdahulu", qcard(P, "Al-'Ankabut 29:40", 29, 40, 40, "Surah Al-'Ankabut, ayat 40")),
        ("jadual", "Jadual 12 Kaum yang Dibinasakan",
         table(["Kaum", "Nabi", "Dosa utama", "Azab", "Ayat"], [
             ["1. Kaum Nabi Nuh", "Nuh AS", "Menyembah berhala dan menolak dakwah selama 950 tahun", "Banjir besar", "Hud 11:25–48; Al-'Ankabut 29:14"],
             ["2. Kaum 'Ad", "Hud AS", "Sombong dengan kekuatan dan binaan", "Angin sangat sejuk dan kencang 7 malam 8 hari", "Al-Haqqah 69:6–8"],
             ["3. Kaum Tsamud", "Saleh AS", "Menyembelih unta mukjizat", "Pekikan dan gempa", "Hud 11:61–68; Al-A'raf 7:78"],
             ["4. Kaum Nabi Luth", "Luth AS", "Liwat dan merompak", "Negeri diterbalikkan dan hujan batu", "Hud 11:77–83"],
             ["5. Penduduk Madyan", "Syuaib AS", "Menipu timbangan dan sukatan", "Pekikan", "Hud 11:84–95"],
             ["6. Ashab Al-Aikah", "Syuaib AS", "Menipu timbangan", "Azab hari naungan awan", "Asy-Syu'ara' 26:176–189"],
             ["7. Firaun dan tenteranya", "Musa AS", "Mengaku tuhan dan menindas Bani Israil", "Ditenggelamkan di laut", "Yunus 10:90–92"],
             ["8. Qarun", "Musa AS", "Sombong dengan harta", "Ditelan bumi bersama rumahnya", "Al-Qasas 28:76–81"],
             ["9. Kaum Saba'", "—", "Kufur nikmat", "Banjir 'Arim memusnahkan kebun", "Saba' 34:15–19"],
             ["10. Ashab As-Sabt", "—", "Menipu larangan menangkap ikan pada hari Sabtu", "Diubah menjadi kera", "Al-A'raf 7:163–166"],
             ["11. Ashab Al-Fil (tentera Abrahah)", "—", "Ingin meruntuhkan Kaabah", "Batu daripada burung ababil", "Al-Fil 105:1–5"],
             ["12. Ashab Ar-Rass", "—", "Mendustakan rasul", "Dibinasakan (butiran tidak disebut)", "Al-Furqan 25:38; Qaf 50:12"]])
         + "<p>Sebahagian ulama tafsir berpendapat Madyan dan Ashab Al-Aikah ialah kaum yang sama dengan dua nama; sebahagian lagi membezakannya. Kaum Tubba' juga disebut dibinasakan" + ref("Ad-Dukhan 44:37") + ".</p>"),
        ("nuh-ad-tsamud", "Kaum Nabi Nuh, 'Ad dan Tsamud",
         "<p><strong>Kaum Nabi Nuh</strong> menyembah berhala Wadd, Suwa', Yaghuth, Ya'uq dan Nasr" + ref("Nuh 71:23")
         + ". Nabi Nuh AS berdakwah 950 tahun, namun hanya sedikit yang beriman. Anak Baginda sendiri enggan menaiki bahtera dan tenggelam" + ref("Hud 11:42–43") + ".</p>"
         "<p><strong>Kaum 'Ad</strong> di Al-Ahqaf membina bangunan tinggi dan berkata: “Siapakah yang lebih kuat daripada kami?”" + ref("Fussilat 41:15")
         + ". Mereka dibinasakan dengan angin yang sangat sejuk, sehingga bergelimpangan seperti batang kurma yang tumbang" + ref("Al-Haqqah 69:7") + ".</p>"
         "<p><strong>Kaum Tsamud</strong> memahat rumah di gunung. Mereka meminta mukjizat, lalu Allah keluarkan seekor unta; mereka menyembelihnya, lalu diazab selepas tiga hari" + ref("Hud 11:64–67")
         + ". Ketika melalui Al-Hijr, Nabi SAW bersabda: “Janganlah kamu masuk ke tempat orang yang diazab kecuali dalam keadaan menangis”" + ref("HR Al-Bukhari, no. 433") + ".</p>"
         + f'<p>Kisah penuh: <a href="{Q}kisah-nabi/nabi-nuh/">Nabi Nuh</a>, <a href="{Q}kisah-nabi/nabi-hud/">Nabi Hud</a>, <a href="{Q}kisah-nabi/nabi-soleh/">Nabi Soleh</a>.</p>'),
        ("luth", "Kaum Nabi Luth: Dosa dan Azabnya",
         qcard(P, "Hud 11:82", 11, 82, 82, "Surah Hud, ayat 82")
         + "<p>Kaum Nabi Luth tinggal di Sadum (Sodom) berhampiran Laut Mati. Mereka ialah kaum pertama yang melakukan liwat secara terbuka" + ref("Al-A'raf 7:80–81")
         + ", di samping merompak di jalanan dan melakukan kemungkaran dalam majlis mereka" + ref("Al-'Ankabut 29:29") + ".</p>"
         + ul("Malaikat datang dalam rupa lelaki tampan; kaumnya bergegas mahu mengganggu tetamu Nabi Luth AS" + ref("Hud 11:77–78"),
              "Nabi Luth AS dan pengikutnya diperintah keluar pada waktu malam tanpa menoleh; isteri Baginda tertinggal dan turut dibinasakan" + ref("Hud 11:81"),
              "Pada waktu Subuh, negeri itu diterbalikkan dan dihujani batu daripada tanah yang dibakar" + ref("Hud 11:82–83"))
         + f'<p>Iktibar: Islam mengharamkan perbuatan itu, tetapi dakwah dilakukan dengan hikmah dan nasihat, bukan penghinaan. Kisah penuh: <a href="{Q}kisah-nabi/nabi-lut/">Kisah Nabi Luth</a>.</p>'),
        ("lain", "Madyan, Firaun, Qarun dan Saba'",
         "<p><strong>Madyan</strong> menipu dalam timbangan. Nabi Syuaib AS berpesan: “Sempurnakanlah sukatan dan timbangan dengan adil”" + ref("Hud 11:85")
         + ". Iktibar untuk peniaga hari ini sangat jelas.</p>"
         "<p><strong>Firaun</strong> mengaku tuhan. Ketika tenggelam dia mengaku beriman, tetapi sudah terlambat; jasadnya diselamatkan sebagai tanda bagi generasi selepasnya" + ref("Yunus 10:90–92") + ".</p>"
         "<p><strong>Qarun</strong> berkata hartanya diperoleh kerana ilmunya sendiri, lalu dia dan rumahnya ditelan bumi" + ref("Al-Qasas 28:78–81") + ".</p>"
         "<p><strong>Kaum Saba'</strong> diberi dua kebun yang subur, tetapi berpaling daripada bersyukur, lalu banjir 'Arim memusnahkannya" + ref("Saba' 34:15–17") + ".</p>"),
        ("iktibar", "5 Iktibar untuk Kita",
         ul("<strong>Azab datang selepas peringatan</strong>: setiap kaum diberi rasul dan masa yang panjang" + ref("Al-Isra' 17:15"),
            "<strong>Dosa yang dibinasakan bukan hanya syirik</strong>: menipu timbangan, sombong dengan harta dan kufur nikmat juga disebut.",
            "<strong>Umat Nabi Muhammad SAW tidak dibinasakan secara menyeluruh</strong> seperti umat terdahulu, berkat doa Baginda" + ref("HR Muslim, no. 2890"),
            "<strong>Istighfar ialah perisai</strong>: “Allah tidak akan mengazab mereka selagi mereka beristighfar”" + ref("Al-Anfal 8:33"),
            "<strong>Jangan berseronok di tempat azab</strong>: lawatan ke Petra, Mada'in Salih atau Laut Mati wajar disertai rasa takut dan iktibar" + ref("HR Al-Bukhari, no. 433"))),
    ],
    faq=[("Apakah kaum yang dibinasakan Allah?", "Antaranya kaum Nabi Nuh, 'Ad, Tsamud, kaum Nabi Luth, Madyan, Ashab Al-Aikah, Firaun, Qarun, Saba', Ashab As-Sabt, tentera Abrahah dan Ashab Ar-Rass."),
         ("Apakah azab kaum Nabi Luth?", "Negeri mereka diterbalikkan dan dihujani batu daripada tanah yang dibakar (Hud 11:82–83)."),
         ("Apakah dosa kaum Nabi Luth?", "Liwat secara terbuka, merompak di jalanan dan melakukan kemungkaran dalam majlis mereka (Al-A'raf 7:80–81; Al-'Ankabut 29:29)."),
         ("Kaum manakah yang ditenggelamkan?", "Kaum Nabi Nuh dengan banjir besar, dan Firaun bersama tenteranya di laut (Al-'Ankabut 29:40)."),
         ("Adakah umat Nabi Muhammad SAW akan dibinasakan seperti umat terdahulu?", "Tidak secara menyeluruh. Nabi SAW berdoa agar umatnya tidak dibinasakan dengan kebuluran atau tenggelam secara menyeluruh, dan doa itu dikabulkan (HR Muslim 2890).")],
    refs=["Al-Quran: Al-'Ankabut 29:14, 29, 40; Hud 11:25–95; Al-A'raf 7:78–81, 163–166; Al-Haqqah 69:6–8; Fussilat 41:15; Nuh 71:23; Asy-Syu'ara' 26:176–189; Yunus 10:90–92; "
          "Al-Qasas 28:76–81; Saba' 34:15–19; Al-Fil 105; Al-Furqan 25:38; Qaf 50:12; Ad-Dukhan 44:37; Al-Isra' 17:15; Al-Anfal 8:33.",
          "Sahih Al-Bukhari, no. 433; Sahih Muslim, no. 2890.", "Tafsir Ibn Kathir, kisah para nabi."],
    disclaimer="Kisah disusun berdasarkan ayat Al-Quran dan tafsir muktabar. Butiran yang tidak disebut oleh Al-Quran atau hadis sahih tidak ditambah.",
    related=[(Q + "kisah-nabi/", "Kisah 25 Nabi", "Kisah para nabi dengan ayat Al-Quran"), (Q + "kisah-nabi/nabi-lut/", "Kisah Nabi Luth", "Kisah penuh dan ayat-ayatnya"),
             (U["tanda-kiamat"], "Tanda-Tanda Kiamat", "Tanda kecil dan besar menurut hadis sahih")])))

# 8 ---------------------------------------------------------------- Imam Syafie
P = "ilmx-is"
SY = [("Ilmu itu cahaya", "شَكَوْتُ إِلَى وَكِيعٍ سُوءَ حِفْظِي، فَأَرْشَدَنِي إِلَى تَرْكِ الْمَعَاصِي، وَأَخْبَرَنِي بِأَنَّ الْعِلْمَ نُورٌ، وَنُورُ اللّٰهِ لَا يُهْدَى لِعَاصِي",
       "Aku mengadu kepada Waki' tentang lemahnya hafalanku, lalu dia menasihatiku supaya meninggalkan maksiat. Dia memberitahuku bahawa ilmu itu cahaya, dan cahaya Allah tidak diberikan kepada pelaku maksiat."),
      ("Enam syarat menuntut ilmu", "أَخِي لَنْ تَنَالَ الْعِلْمَ إِلَّا بِسِتَّةٍ، سَأُنْبِيكَ عَنْ تَفْصِيلِهَا بِبَيَانِ: ذَكَاءٌ وَحِرْصٌ وَاجْتِهَادٌ وَبُلْغَةٌ، وَصُحْبَةُ أُسْتَاذٍ وَطُولُ زَمَانِ",
       "Saudaraku, engkau tidak akan memperoleh ilmu kecuali dengan enam perkara: kecerdasan, kesungguhan, usaha, bekalan, bimbingan guru dan masa yang panjang."),
      ("Pahitnya belajar", "وَمَنْ لَمْ يَذُقْ مُرَّ التَّعَلُّمِ سَاعَةً، تَجَرَّعَ ذُلَّ الْجَهْلِ طُولَ حَيَاتِهِ",
       "Sesiapa yang tidak merasai pahitnya belajar walau sesaat, dia akan menelan hinanya kejahilan sepanjang hidupnya."),
      ("Merantaulah", "سَافِرْ تَجِدْ عِوَضًا عَمَّنْ تُفَارِقُهُ، وَانْصَبْ فَإِنَّ لَذِيذَ الْعَيْشِ فِي النَّصَبِ، إِنِّي رَأَيْتُ وُقُوفَ الْمَاءِ يُفْسِدُهُ، إِنْ سَاحَ طَابَ وَإِنْ لَمْ يَجْرِ لَمْ يَطِبِ",
       "Merantaulah, engkau akan dapat pengganti bagi yang engkau tinggalkan. Berpenatlah, kerana kemanisan hidup ada pada kepenatan. Aku melihat air yang bertakung menjadi rosak; jika mengalir ia jernih, jika tidak ia keruh."),
      ("Jangan salahkan zaman", "نَعِيبُ زَمَانَنَا وَالْعَيْبُ فِينَا، وَمَا لِزَمَانِنَا عَيْبٌ سِوَانَا",
       "Kita mencela zaman kita, padahal celanya ada pada kita. Zaman kita tiada cela selain kita sendiri."),
      ("Biarkan hari berlalu", "دَعِ الْأَيَّامَ تَفْعَلُ مَا تَشَاءُ، وَطِبْ نَفْسًا إِذَا حَكَمَ الْقَضَاءُ",
       "Biarkan hari-hari berbuat sekehendaknya, dan tenangkan jiwa apabila takdir telah menetapkan."),
      ("Jaga lidah", "لِسَانُكَ لَا تَذْكُرْ بِهِ عَوْرَةَ امْرِئٍ، فَكُلُّكَ عَوْرَاتٌ وَلِلنَّاسِ أَعْيُنُ",
       "Jangan sebut aib orang lain dengan lidahmu, kerana dirimu penuh dengan aib, dan manusia juga mempunyai mata."),
      ("Diam terhadap orang bodoh", "إِذَا نَطَقَ السَّفِيهُ فَلَا تُجِبْهُ، فَخَيْرٌ مِنْ إِجَابَتِهِ السُّكُوتُ",
       "Apabila orang bodoh berbicara, jangan dijawab; diam lebih baik daripada menjawabnya."),
      ("Selepas sempit datang lapang", "وَلَرُبَّ نَازِلَةٍ يَضِيقُ لَهَا الْفَتَى ذَرْعًا، وَعِنْدَ اللّٰهِ مِنْهَا الْمَخْرَجُ، ضَاقَتْ فَلَمَّا اسْتَحْكَمَتْ حَلَقَاتُهَا، فُرِجَتْ وَكُنْتُ أَظُنُّهَا لَا تُفْرَجُ",
       "Betapa banyak musibah yang menyesakkan dada seseorang, sedangkan di sisi Allah ada jalan keluarnya. Ia menyempit, dan apabila rantainya semakin ketat, ia terlerai, padahal aku menyangka ia tidak akan terlerai."),
      ("Mata reda dan mata benci", "وَعَيْنُ الرِّضَا عَنْ كُلِّ عَيْبٍ كَلِيلَةٌ، وَلَٰكِنَّ عَيْنَ السُّخْطِ تُبْدِي الْمَسَاوِيَا",
       "Mata yang reda tidak nampak sebarang aib, tetapi mata yang benci menampakkan segala keburukan.")]
KATA = [("“Apabila hadis itu sahih, maka itulah mazhabku.”", "Dinukil oleh An-Nawawi, Al-Majmu'"),
        ("“Setiap perkataanku yang bercanggah dengan hadis Nabi SAW yang sahih, maka hadis Nabi lebih utama; janganlah kamu bertaqlid kepadaku.”", "Ibn Abi Hatim, Adab Asy-Syafi'i"),
        ("“Aku tidak pernah berdebat dengan seseorang melainkan aku suka jika Allah menzahirkan kebenaran melalui lisannya.”", "Abu Nu'aim, Hilyat Al-Auliya'"),
        ("“Ilmu ialah apa yang bermanfaat, bukan apa yang dihafal.”", "Abu Nu'aim, Hilyat Al-Auliya'"),
        ("“Sesiapa yang menasihati saudaranya secara rahsia, dia telah menasihati dan menghiasinya. Sesiapa yang menasihatinya di khalayak, dia telah memalukan dan mencemarkannya.”", "Abu Nu'aim, Hilyat Al-Auliya'; dinukil An-Nawawi"),
        ("“Menuntut ilmu lebih utama daripada solat sunat.”", "Al-Baihaqi, Manaqib Asy-Syafi'i"),
        ("“Sesiapa yang mahukan dunia, hendaklah dengan ilmu. Sesiapa yang mahukan akhirat, hendaklah dengan ilmu.”", "Dinukil An-Nawawi, Al-Majmu' (muqaddimah)"),
        ("“Pendapatku benar tetapi mungkin salah; pendapat orang lain salah tetapi mungkin benar.”", "Masyhur dinisbahkan kepada Imam Asy-Syafi'i; sanadnya tidak dapat dipastikan")]
POSTS.append(("imam-syafie", base(
    ns=P, url=U["imam-syafie"], published="2020-02-07", pubms="7 Februari 2020",
    title="Kata-Kata Imam Syafie: Pesanan, Syair Ilmu & Biodata Ringkas",
    desc="Kata-kata dan pesanan Imam Syafie tentang ilmu, hidup dan akhlak (Arab dan maksud) daripada Diwan Asy-Syafi'i, serta biodata: nama penuh, guru, murid dan kitab.",
    h1="Kata-Kata Imam Syafie: Pesanan & Syair",
    img=img("kata-kata-imam-syafie", "Tokoh Ulama", "Kata-Kata Imam Syafie", "Pesanan, syair ilmu & biodata ringkas", "الْعِلْمُ نُورٌ"),
    alt="Kata-kata dan pesanan Imam Syafie tentang ilmu", refshort="Diwan Asy-Syafi'i, Hilyat Al-Auliya', Al-Majmu'",
    lead="Pesanan dan syair Imam Asy-Syafi'i yang paling dikenali, dalam teks Arab dan maksud, dengan sumber setiap petikan, diikuti biodata ringkas pengasas mazhab yang diamalkan di Malaysia.",
    crumb=("Tokoh", W + "search/label/Tokoh"), about=["Imam Syafie", "Kata-kata ulama", "Mazhab Syafi'i"],
    answer="Antara kata-kata Imam Syafie yang paling masyhur ialah <strong>“Ilmu itu cahaya, dan cahaya Allah tidak diberikan kepada pelaku maksiat”</strong> <em>(Diwan Asy-Syafi'i)</em> dan "
           "<strong>“Apabila hadis itu sahih, maka itulah mazhabku”</strong> <em>(dinukil An-Nawawi, Al-Majmu')</em>. Imam Syafie, nama penuhnya <strong>Muhammad bin Idris Asy-Syafi'i</strong>, "
           "lahir di Gaza pada 150H dan wafat di Mesir pada 204H. Mazhab beliau menjadi pegangan rasmi umat Islam di Malaysia.",
    sections=[
        ("syair", "10 Syair Imam Syafie (Arab dan Maksud)",
         "<p>Petikan berikut daripada <em>Diwan Al-Imam Asy-Syafi'i</em>, himpunan syair yang dinisbahkan kepada beliau.</p>"
         + "".join(dc(P, t, ar, "", mn, "Diwan Al-Imam Asy-Syafi'i") for t, ar, mn in SY)),
        ("kata", "Pesanan Imam Syafie tentang Ilmu, Hadis dan Akhlak",
         table(["Pesanan", "Sumber"], [[e(k), e(s)] for k, s in KATA])
         + "<p>Pesanan pertama dan kedua menunjukkan Imam Syafie sendiri meletakkan <strong>hadis sahih di atas pendapatnya</strong>. Inilah sebab ulama Syafi'iyyah seperti An-Nawawi "
           "menyemak semula pendapat dalam mazhab berdasarkan dalil.</p>"),
        ("palsu", "Kata-Kata yang Sering Disalah Nisbah",
         "<p>Banyak gambar kata-kata di media sosial dinisbahkan kepada Imam Syafie tanpa sumber, seperti senarai “3 perkara yang perlu dirahsiakan”. "
         "Sebelum berkongsi, semak sama ada petikan itu ada dalam <em>Diwan Asy-Syafi'i</em>, <em>Hilyat Al-Auliya'</em>, <em>Manaqib Asy-Syafi'i</em> oleh Al-Baihaqi atau <em>Adab Asy-Syafi'i</em> oleh Ibn Abi Hatim.</p>"),
        ("biodata", "Biodata Ringkas Imam Syafie",
         table(["Perkara", "Butiran"], [
             ["Nama penuh", "Muhammad bin Idris bin Al-Abbas bin Uthman bin Syafi' bin As-Sa'ib bin 'Ubaid bin 'Abd Yazid bin Hasyim bin Al-Muttalib bin 'Abd Manaf"],
             ["Nasab", "Quraisy, Bani Al-Muttalib; bertemu nasab dengan Nabi SAW pada 'Abd Manaf"],
             ["Lahir", "Gaza, Palestin, tahun 150H (767M), tahun wafatnya Imam Abu Hanifah"],
             ["Wafat", "Fustat, Mesir, malam Jumaat akhir Rejab 204H (820M), usia 54 tahun; dimakamkan di Al-Qarafah, Kaherah"],
             ["Hafalan", "Menghafaz Al-Quran sekitar usia 7 tahun dan Al-Muwatta' sekitar usia 10 tahun"],
             ["Guru utama", "Muslim bin Khalid Az-Zanji dan Sufyan bin 'Uyainah (Mekah), Imam Malik bin Anas (Madinah), Muhammad bin Al-Hasan Asy-Syaibani (Iraq), Waki' bin Al-Jarrah"],
             ["Murid terkenal", "Imam Ahmad bin Hanbal, Al-Muzani, Al-Buwaiti, Ar-Rabi' bin Sulaiman Al-Muradi"],
             ["Karya utama", "Ar-Risalah (kitab usul fiqh pertama yang disusun), Al-Umm"],
             ["Qaul qadim dan qaul jadid", "Pendapat lama ketika di Iraq, dan pendapat baharu selepas berpindah ke Mesir; yang dipegang dalam mazhab ialah qaul jadid kecuali beberapa masalah"]])
         + "<p>Imam Syafie diizinkan berfatwa oleh gurunya Muslim bin Khalid Az-Zanji ketika masih remaja. Beliau menggabungkan pendekatan ahli hadis di Hijaz dan ahli ra'yi di Iraq, "
           "lalu meletakkan kaedah usul fiqh yang menjadi asas kepada mazhab-mazhab selepasnya.</p>"),
        ("malaysia", "Mazhab Syafi'i di Malaysia",
         "<p>Mazhab Syafi'i ialah mazhab rasmi dalam hal ibadah di Malaysia, Brunei, Indonesia, Singapura dan selatan Thailand. Fatwa negeri merujuk kitab-kitab muktabar mazhab seperti "
         "<em>Minhaj At-Talibin</em> (An-Nawawi), <em>Tuhfat Al-Muhtaj</em> (Ibn Hajar Al-Haitami) dan <em>Nihayat Al-Muhtaj</em> (Ar-Ramli). Dalam keadaan tertentu, fatwa boleh mengambil pandangan mazhab lain atas maslahat.</p>"
         + f'<p>Contoh panduan ibadah mengikut mazhab Syafi\'i di laman kami: <a href="{Q}belajar-solat/">Belajar Solat</a> dan <a href="{Q}solat-jamak-qasar/">Solat Jamak & Qasar</a>.</p>'),
    ],
    faq=[("Apakah kata-kata Imam Syafie yang terkenal?", "“Ilmu itu cahaya, dan cahaya Allah tidak diberikan kepada pelaku maksiat” (Diwan Asy-Syafi'i) dan “Apabila hadis itu sahih, maka itulah mazhabku” (dinukil An-Nawawi)."),
         ("Apakah nama penuh Imam Syafie?", "Muhammad bin Idris bin Al-Abbas bin Uthman bin Syafi' bin As-Sa'ib, daripada Bani Al-Muttalib, Quraisy."),
         ("Siapakah guru Imam Syafie?", "Antaranya Muslim bin Khalid Az-Zanji, Sufyan bin 'Uyainah, Imam Malik bin Anas, Muhammad bin Al-Hasan Asy-Syaibani dan Waki' bin Al-Jarrah."),
         ("Bilakah Imam Syafie lahir dan wafat?", "Lahir di Gaza pada 150H dan wafat di Mesir pada 204H, ketika berusia 54 tahun."),
         ("Apakah syair Imam Syafie tentang ilmu?", "Antaranya enam syarat menuntut ilmu: kecerdasan, kesungguhan, usaha, bekalan, bimbingan guru dan masa yang panjang (Diwan Asy-Syafi'i).")],
    refs=["Diwan Al-Imam Asy-Syafi'i.", "Abu Nu'aim Al-Asbahani, Hilyat Al-Auliya', jilid 9.", "Al-Baihaqi, Manaqib Asy-Syafi'i.", "Ibn Abi Hatim, Adab Asy-Syafi'i wa Manaqibuh.",
          "An-Nawawi, Al-Majmu' Syarh Al-Muhadzdzab, muqaddimah.", "Adz-Dzahabi, Siyar A'lam An-Nubala', biografi Asy-Syafi'i."],
    badges=["Teks Arab Asal", "Sumber Setiap Petikan", "Dikemas kini 2026"],
    disclaimer="Syair dalam Diwan Asy-Syafi'i dihimpunkan selepas zaman beliau, dan ulama menyebut sebahagiannya mungkin bukan gubahan beliau sendiri. Petikan yang diragui dinyatakan dengan jelas.",
    related=[(Q + "belajar-solat/", "Belajar Solat", "Panduan solat mengikut mazhab Syafi'i"), (Q + "doa-belajar/", "Doa Belajar", "Doa sebelum dan selepas belajar"),
             (U["kelebihan-solat"], "Kelebihan Menjaga Solat", "9 kemuliaan dengan dalil sahih")])))

# 9 ---------------------------------------------------------------- Ya Muqallibal Qulub (doa hidayah)
P = "ilmx-mq"
POSTS.append(("muqallibal-qulub", base(
    ns=P, url=U["muqallibal-qulub"], published="2020-02-06", pubms="6 Februari 2020",
    title="Doa Ya Muqallibal Qulub: Bacaan, Maksud & Doa Tetap Hati (Sahih)",
    desc="Doa Ya Muqallibal Qulub Thabbit Qalbi 'Ala Dinik: Arab, Rumi dan maksud, hadis sahihnya, serta 6 doa mohon hidayah dan tetap hati daripada Al-Quran dan sunnah.",
    h1="Doa Ya Muqallibal Qulub & Doa Mohon Hidayah",
    img=img("ya-muqallibal-qulub", "Doa Sahih", "Doa Ya Muqallibal Qulub", "Bacaan, maksud & doa tetap hati", "يَا مُقَلِّبَ الْقُلُوبِ"),
    alt="Doa Ya Muqallibal Qulub: bacaan Arab, Rumi dan maksud", refshort="Sunan At-Tirmizi, Sahih Muslim, Al-Quran",
    lead="Doa yang paling kerap dibaca Rasulullah SAW untuk ketetapan hati, berserta lima doa sahih lain untuk memohon hidayah dan taufik bagi diri dan keluarga.",
    crumb=("Doa", W + "search/label/Doa"), about=["Doa Ya Muqallibal Qulub", "Doa hidayah", "Doa tetap hati"],
    answer="<strong>“Ya Muqallibal qulub, thabbit qalbi 'ala dinik”</strong> bermaksud <strong>“Wahai Tuhan yang membolak-balikkan hati, tetapkanlah hatiku di atas agama-Mu.”</strong> "
           "Ummu Salamah RA berkata inilah doa yang <strong>paling banyak dibaca Rasulullah SAW</strong> <em>(HR At-Tirmizi, no. 3522; Ahmad)</em>, dan Anas RA meriwayatkan "
           "Baginda kerap membacanya <em>(HR At-Tirmizi, no. 2140; hasan)</em>.",
    sections=[
        ("bacaan", "Bacaan Doa Ya Muqallibal Qulub",
         dc(P, "Doa tetap hati", "يَا مُقَلِّبَ الْقُلُوبِ ثَبِّتْ قَلْبِي عَلَى دِينِكَ", "Ya Muqallibal qulub, thabbit qalbi 'ala dinik.",
            "Wahai Tuhan yang membolak-balikkan hati, tetapkanlah hatiku di atas agama-Mu.", "HR At-Tirmizi, no. 2140, 3522 (hasan)")
         + "<p>Ummu Salamah RA bertanya mengapa Baginda kerap membaca doa ini. Nabi SAW menjawab: “Wahai Ummu Salamah, tiada seorang anak Adam pun melainkan hatinya berada di antara dua jari daripada jari-jari Ar-Rahman; "
           "sesiapa yang Dia kehendaki, Dia tetapkan, dan sesiapa yang Dia kehendaki, Dia condongkan”" + ref("HR At-Tirmizi, no. 3522") + ".</p>"
         + table(["Lafaz", "Maksud"], [["Ya Muqallib", "Wahai Yang Membolak-balikkan"], ["al-qulub", "hati-hati"], ["thabbit", "tetapkanlah, teguhkanlah"],
                                      ["qalbi", "hatiku"], ["'ala dinik", "di atas agama-Mu"]])),
        ("musarrif", "Doa Mohon Hati Dipalingkan kepada Ketaatan",
         dc(P, "Doa Musarrifal Qulub", "اللّٰهُمَّ مُصَرِّفَ الْقُلُوبِ صَرِّفْ قُلُوبَنَا عَلَى طَاعَتِكَ", "Allahumma musarrifal qulub, sarrif qulubana 'ala ta'atik.",
            "Ya Allah, Tuhan yang memalingkan hati, palingkanlah hati-hati kami kepada ketaatan kepada-Mu.", "HR Muslim, no. 2654")),
        ("quran", "Doa Tetap Hati daripada Al-Quran",
         qcard(P, "Ali 'Imran 3:8: Rabbana la tuzigh qulubana", 3, 8, 8, "Surah Ali 'Imran, ayat 8")
         + "<p>Doa ini ialah doa orang yang mendalam ilmunya (ar-rasikhun fil 'ilm). Selepas memahami ayat-ayat Allah, mereka tidak berbangga dengan ilmu, sebaliknya memohon agar hati tidak dipesongkan.</p>"
         + qcard(P, "Al-Kahf 18:10: doa pemuda Al-Kahfi", 18, 10, 10, "Surah Al-Kahf, ayat 10")),
        ("hidayah", "Doa Mohon Hidayah dan Taufik",
         dc(P, "Doa hidayah, takwa, kesucian dan kecukupan", "اللّٰهُمَّ إِنِّي أَسْأَلُكَ الْهُدَى وَالتُّقَى وَالْعَفَافَ وَالْغِنَى", "Allahumma inni as'alukal huda wat-tuqa wal-'afafa wal-ghina.",
            "Ya Allah, aku memohon kepada-Mu petunjuk, ketakwaan, kesucian diri dan kecukupan.", "HR Muslim, no. 2721")
         + dc(P, "Doa hidayah dan ketepatan", "اللّٰهُمَّ اهْدِنِي وَسَدِّدْنِي", "Allahummahdini wa saddidni.", "Ya Allah, berilah aku petunjuk dan luruskanlah aku.", "HR Muslim, no. 2725")
         + dc(P, "Doa daripada qunut", "اللّٰهُمَّ اهْدِنِي فِيمَنْ هَدَيْتَ", "Allahummahdini fiman hadait.", "Ya Allah, berilah aku petunjuk bersama orang-orang yang telah Engkau beri petunjuk.",
              "HR Abu Daud, no. 1425; At-Tirmizi, no. 464")
         + f'<p>Bacaan qunut penuh: <a href="{Q}doa-qunut/">Doa Qunut Subuh</a>.</p>'),
        ("beza", "Hidayah dan Taufik: Apa Bezanya?",
         "<p>Al-Quran menyebut Nabi SAW <strong>memberi petunjuk ke jalan yang lurus</strong>" + ref("Asy-Syura 42:52") + ", tetapi juga menyebut Baginda <strong>tidak mampu memberi hidayah</strong> kepada orang yang Baginda kasihi" + ref("Al-Qasas 28:56")
         + ". Ulama menjelaskan dua jenis hidayah:</p>"
         + table(["Jenis", "Maksud", "Siapa yang memberi"], [["Hidayah irsyad (bimbingan)", "Menunjukkan jalan melalui ilmu, nasihat dan dakwah", "Nabi, ulama, ibu bapa, guru"],
                                                         ["Hidayah taufik", "Hati menerima dan mengamalkan kebenaran", "Allah sahaja"]])
         + "<p>Sebab itu kita tetap berdakwah kepada keluarga, tetapi terus berdoa kerana taufik hanya milik Allah.</p>"),
        ("keluarga", "Doa Hidayah untuk Anak, Pasangan dan Keluarga",
         "<p>Abu Hurairah RA meminta Nabi SAW mendoakan ibunya yang belum Islam. Baginda berdoa: “Ya Allah, berilah petunjuk kepada ibu Abu Hurairah,” dan ibunya memeluk Islam pada hari itu juga" + ref("HR Muslim, no. 2491") + ".</p>"
         + dc(P, "Contoh doa untuk orang tersayang", "اللّٰهُمَّ اهْدِ ... وَثَبِّتْ قَلْبَهُ عَلَى دِينِكَ", "Allahummahdi (sebut nama), wa thabbit qalbahu 'ala dinik.",
              "Ya Allah, berilah petunjuk kepada (nama), dan tetapkanlah hatinya di atas agama-Mu.", "Disusun berdasarkan HR Muslim 2491 dan HR At-Tirmizi 2140",
              "Gunakan “qalbaha” bagi perempuan. Berdoa untuk orang lain secara rahsia juga didoakan malaikat (HR Muslim 2733).")
         + qcard(P, "Al-Furqan 25:74: doa untuk pasangan dan zuriat", 25, 74, 74, "Surah Al-Furqan, ayat 74")),
        ("amal", "Bila dan Bagaimana Mengamalkannya",
         ul("Selepas solat fardu, dalam sujud, dan antara azan dengan iqamah, iaitu waktu-waktu mustajab.",
            "Ketika merasa iman lemah, malas beribadah atau diuji dengan syubhat.",
            "Tiada bilangan khusus dalam hadis; membacanya berulang kali sebagai zikir dibenarkan.",
            "Iringi dengan sebab-sebab hidayah: majlis ilmu, kawan yang soleh dan menjauhi maksiat.")
         + f'<p>Lihat juga <a href="{Q}doa-selepas-solat/">Doa Selepas Solat</a> dan <a href="{Q}doa-hilangkan-resah/">Doa Hilangkan Resah</a>.</p>'),
    ],
    faq=[("Apakah maksud Ya Muqallibal Qulub?", "“Wahai Tuhan yang membolak-balikkan hati.” Doa lengkapnya “Ya Muqallibal qulub, thabbit qalbi 'ala dinik” bermaksud tetapkanlah hatiku di atas agama-Mu."),
         ("Adakah doa Ya Muqallibal Qulub sahih?", "Ya. Ia diriwayatkan At-Tirmizi (2140, 3522) dan Ahmad dengan status hasan, dan Ummu Salamah RA berkata ia doa yang paling banyak dibaca Nabi SAW."),
         ("Apakah doa mohon hidayah?", "Antaranya “Allahumma inni as'alukal huda wat-tuqa wal-'afafa wal-ghina” (HR Muslim 2721) dan “Allahummahdini wa saddidni” (HR Muslim 2725)."),
         ("Apakah doa tetap iman dalam Al-Quran?", "“Rabbana la tuzigh qulubana ba'da idh hadaitana wa hab lana min ladunka rahmah, innaka antal wahhab” (Ali 'Imran 3:8)."),
         ("Bolehkah mendoakan hidayah untuk orang lain?", "Boleh dan sangat dituntut. Nabi SAW mendoakan hidayah untuk ibu Abu Hurairah dan doa itu dimakbulkan (HR Muslim 2491).")],
    refs=["Al-Quran: Ali 'Imran 3:8; Al-Kahf 18:10; Al-Furqan 25:74; Asy-Syura 42:52; Al-Qasas 28:56.", "Sunan At-Tirmizi, no. 464, 2140, 3522; Musnad Ahmad.",
          "Sahih Muslim, no. 2491, 2654, 2721, 2725, 2733.", "Sunan Abu Daud, no. 1425."],
    related=[(Q + "doa-qunut/", "Doa Qunut", "Bacaan qunut Subuh lengkap"), (Q + "doa-selepas-solat/", "Doa Selepas Solat", "Doa dan zikir selepas solat fardu"),
             (U["doa-teraniaya"], "Doa Orang Teraniaya", "Hadis tiada hijab dan bacaan doa")])))

# 10 --------------------------------------------------------------- Doa orang teraniaya (flagship keyword, 4,400/month)
P = "ilmx-dt"
POSTS.append(("doa-teraniaya", base(
    ns=P, url=U["doa-teraniaya"], published="2017-11-25", pubms="25 November 2017",
    title="Doa Orang Teraniaya: Bacaan Rumi, Hadis Tiada Hijab & Adabnya",
    desc="Doa orang teraniaya dan dizalimi: hadis tiada hijab antara doanya dengan Allah, 7 bacaan doa sahih (Arab, Rumi, maksud), doa ketika difitnah dan adab berdoa.",
    h1="Doa Orang Teraniaya: Hadis, Bacaan & Adab",
    img=img("doa-orang-teraniaya", "Doa Sahih", "Doa Orang Teraniaya", "Tiada hijab antara doanya dengan Allah", "دَعْوَةَ الْمَظْلُومِ"),
    alt="Doa orang teraniaya: hadis dan bacaan doa", refshort="Sahih Al-Bukhari, Sahih Muslim, Sunan At-Tirmizi",
    lead="Mengapa doa orang yang dizalimi begitu dahsyat, tujuh bacaan doa sahih untuk orang yang teraniaya atau difitnah, dan adab supaya doa itu tidak bertukar menjadi kezaliman baharu.",
    crumb=("Doa", W + "search/label/Doa"), about=["Doa orang teraniaya", "Doa orang dizalimi", "Doa mustajab"],
    answer="Nabi SAW bersabda: <strong>“Takutlah kamu terhadap doa orang yang dizalimi, kerana tiada hijab antara doanya dengan Allah”</strong> <em>(HR Al-Bukhari, no. 1496; Muslim, no. 19)</em>. "
           "Ia termasuk <strong>tiga doa yang mustajab tanpa diragui</strong> <em>(HR Abu Daud, no. 1536; At-Tirmizi, no. 1905)</em>. Doa yang paling sesuai dibaca ialah "
           "<strong>“Hasbunallahu wa ni'mal wakil”</strong> <em>(Ali 'Imran 3:173)</em> dan doa Nabi Nuh AS <strong>“Anni maghlubun fantasir”</strong> <em>(Al-Qamar 54:10)</em>.",
    sections=[
        ("hadis", "Hadis Doa Orang Teraniaya",
         dc(P, "Tiada hijab antara doanya dengan Allah", "اتَّقِ دَعْوَةَ الْمَظْلُومِ، فَإِنَّهُ لَيْسَ بَيْنَهَا وَبَيْنَ اللّٰهِ حِجَابٌ", "Ittaqi da'watal mazlum, fa innahu laisa bainaha wa bainallahi hijab.",
            "Takutlah engkau terhadap doa orang yang dizalimi, kerana tiada hijab (penghalang) antara doanya dengan Allah.", "HR Al-Bukhari, no. 1496; Muslim, no. 19")
         + "<p>Pesanan ini diberikan kepada Mu'az bin Jabal RA ketika diutus ke Yaman sebagai gabenor. Ia amaran kepada orang yang berkuasa: kuasa tidak melindungi daripada doa rakyat yang dizalimi.</p>"
         + grade([("Tiada hijab antara doa orang yang dizalimi dengan Allah", "HR Al-Bukhari 1496; Muslim 19", SAHIH),
                  ("Tiga doa mustajab tanpa diragui: orang yang dizalimi, musafir, dan bapa untuk anaknya", "HR Abu Daud 1536; At-Tirmizi 1905", HASAN),
                  ("Doanya diangkat di atas awan dan Allah berfirman: Demi keagungan-Ku, Aku pasti menolongmu walaupun selepas beberapa waktu", "HR At-Tirmizi 3598", HASAN),
                  ("Doa orang yang dizalimi dimakbulkan walaupun dia seorang pendosa; dosanya tanggungan dirinya", "HR Ahmad 8795", HASAN)], head="Kedudukan doa orang dizalimi")
         + "<p>Perhatikan frasa <strong>“walaupun selepas beberapa waktu”</strong>. Pertolongan Allah pasti datang, tetapi waktunya ditentukan Allah. Doa yang belum nampak hasil bukan bermakna ditolak.</p>"),
        ("bacaan", "7 Bacaan Doa Orang Teraniaya (Arab, Rumi & Maksud)",
         "<h3>1. Hasbunallah wa ni'mal wakil</h3>"
         + dc(P, "Doa Nabi Ibrahim dan Nabi Muhammad ketika diancam", "حَسْبُنَا اللّٰهُ وَنِعْمَ الْوَكِيلُ", "Hasbunallahu wa ni'mal wakil.",
              "Cukuplah Allah bagi kami, dan Dialah sebaik-baik Pelindung.", "Ali 'Imran 3:173; HR Al-Bukhari, no. 4563",
              "Ibn Abbas RA berkata kalimah ini diucapkan Nabi Ibrahim AS ketika dicampak ke dalam api, dan Nabi Muhammad SAW ketika diancam musuh.")
         + "<h3>2. Doa Nabi Nuh AS ketika dikalahkan kaumnya</h3>" + qcard(P, "Al-Qamar 54:10", 54, 10, 10, "Surah Al-Qamar, ayat 10")
         + "<h3>3. Doa Nabi Musa AS mohon diselamatkan daripada orang zalim</h3>" + qcard(P, "Al-Qasas 28:21", 28, 21, 21, "Surah Al-Qasas, ayat 21")
         + "<h3>4. Doa Asiah, isteri Firaun</h3>" + qcard(P, "At-Tahrim 66:11", 66, 11, 11, "Surah At-Tahrim, ayat 11")
         + "<p>Asiah dizalimi oleh suaminya sendiri, orang paling berkuasa pada zamannya. Doanya tidak meminta balasan dunia, sebaliknya rumah di sisi Allah. Doa ini sesuai bagi mereka yang dizalimi dalam rumah tangga.</p>"
         + "<h3>5. Doa ketika takut kepada sesuatu kaum</h3>"
         + dc(P, "Doa menghadapi orang yang menzalimi", "اللّٰهُمَّ إِنَّا نَجْعَلُكَ فِي نُحُورِهِمْ، وَنَعُوذُ بِكَ مِنْ شُرُورِهِمْ", "Allahumma inna naj'aluka fi nuhurihim, wa na'udhu bika min syururihim.",
              "Ya Allah, kami jadikan Engkau di hadapan mereka, dan kami berlindung kepada-Mu daripada kejahatan mereka.", "HR Abu Daud, no. 1537 (sahih)")
         + "<h3>6. Doa mohon pertolongan ke atas orang yang menzalimi</h3>"
         + dc(P, "Doa Nabi SAW", "اللّٰهُمَّ مَتِّعْنِي بِسَمْعِي وَبَصَرِي، وَاجْعَلْهُمَا الْوَارِثَ مِنِّي، وَانْصُرْنِي عَلَى مَنْ يَظْلِمُنِي، وَخُذْ مِنْهُ بِثَأْرِي",
              "Allahumma matti'ni bisam'i wa basari, waj'alhumal waritha minni, wansurni 'ala man yazlimuni, wa khudh minhu bitha'ri.",
              "Ya Allah, berilah aku manfaat dengan pendengaran dan penglihatanku, jadikan kedua-duanya kekal hingga akhir hayatku, tolonglah aku menghadapi orang yang menzalimiku, dan ambillah pembalasan untukku daripadanya.",
              "HR At-Tirmizi, Kitab Ad-Da'awat; dinilai hasan gharib oleh At-Tirmizi")
         + "<h3>7. La hawla wa la quwwata illa billah</h3>"
         + dc(P, "Perbendaharaan syurga", "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللّٰهِ", "La hawla wa la quwwata illa billah.", "Tiada daya dan kekuatan melainkan dengan (pertolongan) Allah.",
              "HR Al-Bukhari, no. 4205; Muslim, no. 2704", "Nabi SAW menyebutnya salah satu perbendaharaan syurga. Ia menyerahkan urusan yang di luar kemampuan kita kepada Allah.")),
        ("taif", "Doa Nabi SAW di Taif: Status Hadisnya",
         "<p>Doa “Allahumma ilaika asyku dha'fa quwwati, wa qillata hilati, wa hawani 'alan-nas…” yang dikatakan dibaca Nabi SAW selepas dilempar batu di Taif sangat popular sebagai doa orang teraniaya. "
         "Ia diriwayatkan oleh At-Tabarani, dan <strong>sanadnya dinilai dhaif</strong> oleh ramai ulama hadis. Maknanya baik dan boleh dibaca sebagai munajat, tetapi jangan diyakini sebagai lafaz Nabi SAW yang pasti. "
         "Doa 1 hingga 6 di atas lebih kuat sumbernya.</p>"),
        ("fitnah", "Doa Orang Teraniaya dan Difitnah",
         "<p>Sa'ad bin Abi Waqqas RA difitnah oleh seorang lelaki di Kufah yang mendakwa beliau tidak adil dan tidak keluar berjihad. Sa'ad berdoa: “Ya Allah, jika hamba-Mu ini berdusta kerana riak dan mahu dikenali, "
         "panjangkanlah umurnya, panjangkanlah kefakirannya, dan dedahkanlah dia kepada fitnah.” Lelaki itu kemudian hidup sangat tua dalam keadaan hina dan berkata: “Aku orang tua yang terkena doa Sa'ad”"
         + ref("HR Al-Bukhari, no. 755") + ".</p>"
         "<p>Pengajaran: Sa'ad mensyaratkan doanya, <strong>“jika dia berdusta”</strong>. Ini adab penting ketika kita tidak pasti sepenuhnya niat orang yang menzalimi kita.</p>"
         + qcard(P, "Ibrahim 14:42: Allah tidak lalai", 14, 42, 42, "Surah Ibrahim, ayat 42")),
        ("adab", "Adab: Bolehkah Mendoakan Keburukan ke atas Orang Zalim?",
         qcard(P, "An-Nisa' 4:148", 4, 148, 148, "Surah An-Nisa', ayat 148")
         + "<p>Ayat ini membenarkan orang yang dizalimi menyebut kezaliman yang menimpanya dan mendoakan balasan <strong>setimpal</strong>. Namun ulama menggariskan adab berikut:</p>"
         + ul("<strong>Jangan melampaui batas</strong>: doa yang lebih berat daripada kezaliman yang diterima menjadikan kita pula orang yang zalim.",
              "<strong>Memaafkan lebih utama</strong>: “Balasan kejahatan ialah kejahatan yang setimpal, tetapi sesiapa yang memaafkan dan berdamai, pahalanya di sisi Allah”" + ref("Asy-Syura 42:40"),
              "<strong>Doakan hidayah jika mampu</strong>: Nabi SAW mendoakan kabilah Daus supaya diberi hidayah walaupun mereka menentang Baginda" + ref("HR Al-Bukhari, no. 2937"),
              "<strong>Jangan doakan keburukan ke atas diri, anak dan harta sendiri</strong>, kerana mungkin bertepatan dengan waktu mustajab" + ref("HR Muslim, no. 3009"),
              "<strong>Ambil tindakan yang dibenarkan undang-undang</strong>: berdoa tidak menghalang membuat laporan polis, aduan rasmi atau tuntutan mahkamah.")
         + f'<div class="{P}-box amber">Jika anda menghadapi keganasan rumah tangga atau ancaman, hubungi Talian Kasih 15999 atau polis 999. Doa dan usaha berjalan seiring.</div>'),
        ("zalim", "Jika Anda Pernah Menzalimi Orang Lain",
         "<p>Nabi SAW bersabda: “Sesiapa yang pernah menzalimi saudaranya, sama ada maruahnya atau sesuatu yang lain, hendaklah dia meminta halal daripadanya hari ini, sebelum datang hari yang tiada dinar dan dirham”"
         + ref("HR Al-Bukhari, no. 2449") + ". Orang yang “muflis” di akhirat ialah orang yang membawa pahala solat dan puasa, tetapi pahalanya diambil oleh mereka yang pernah dizaliminya" + ref("HR Muslim, no. 2581") + ".</p>"
         + ul("Bertaubat kepada Allah dengan menyesal dan berhenti.", "Pulangkan hak atau harta yang diambil.", "Minta maaf dan minta dihalalkan.",
              "Jika tidak dapat dihubungi, doakan dan bersedekah bagi pihaknya.")
         + f'<p>Bacaan istighfar: <a href="{Q}doa-taubat/">Doa Taubat & Sayyidul Istighfar</a>.</p>'),
    ],
    faq=[("Apakah doa orang teraniaya?", "Antara doa yang sesuai ialah “Hasbunallahu wa ni'mal wakil” (Ali 'Imran 3:173), doa Nabi Nuh “Anni maghlubun fantasir” (Al-Qamar 54:10) dan doa Nabi Musa “Rabbi najjini minal qaumiz-zalimin” (Al-Qasas 28:21)."),
         ("Adakah doa orang teraniaya makbul?", "Ya. Nabi SAW bersabda tiada hijab antara doa orang yang dizalimi dengan Allah (HR Al-Bukhari 1496), dan Allah berjanji menolongnya walaupun selepas beberapa waktu (HR At-Tirmizi 3598)."),
         ("Apakah hadis doa orang teraniaya?", "“Takutlah kamu terhadap doa orang yang dizalimi, kerana tiada hijab antara doanya dengan Allah” (HR Al-Bukhari 1496; Muslim 19)."),
         ("Apakah doa orang teraniaya dalam Al-Quran?", "Antaranya Ali 'Imran 3:173, Al-Qamar 54:10, Al-Qasas 28:21 dan doa Asiah dalam At-Tahrim 66:11."),
         ("Bolehkah mendoakan keburukan untuk orang yang menzalimi kita?", "Dibenarkan setakat kezaliman yang diterima (An-Nisa' 4:148), tetapi memaafkan lebih utama (Asy-Syura 42:40). Doa yang melampau menjadikan kita pula orang yang zalim."),
         ("Apakah doa ketika difitnah?", "Baca “Hasbunallahu wa ni'mal wakil” dan doa mohon pertolongan ke atas orang yang menzalimi. Sa'ad bin Abi Waqqas RA mensyaratkan doanya “jika dia berdusta” (HR Al-Bukhari 755).")],
    refs=["Al-Quran: Ali 'Imran 3:173; Al-Qamar 54:10; Al-Qasas 28:21; At-Tahrim 66:11; Ibrahim 14:42; An-Nisa' 4:148; Asy-Syura 42:40.",
          "Sahih Al-Bukhari, no. 755, 1496, 2449, 2937, 4205, 4563.", "Sahih Muslim, no. 19, 2581, 2704, 3009.",
          "Sunan Abu Daud, no. 1536, 1537; Sunan At-Tirmizi, no. 1905, 3598, Kitab Ad-Da'awat.", "Musnad Ahmad, no. 8795."],
    related=[(Q + "doa-hilangkan-resah/", "Doa Hilangkan Resah", "Doa sahih ketika gelisah dan tertekan"), (Q + "doa-ditimpa-musibah/", "Doa Ditimpa Musibah", "Inna lillahi dan doa ganti yang lebih baik"),
             (U["muqallibal-qulub"], "Doa Ya Muqallibal Qulub", "Doa tetap hati dan mohon hidayah")])))

# 11 --------------------------------------------------------------- Ayam berkokok tengah malam
P = "ilmx-ab"
POSTS.append(("ayam-berkokok", base(
    ns=P, url=U["ayam-berkokok"], published="2017-12-05", pubms="5 Disember 2017",
    title="Ayam Berkokok Tengah Malam: Maksud Hadis, Doa & Sebab Saintifik",
    desc="Maksud ayam berkokok tengah malam menurut hadis sahih (ia melihat malaikat), doa yang dibaca, sebab saintifik ayam berkokok waktu malam dan mitos yang salah.",
    h1="Ayam Berkokok Tengah Malam: Hadis, Doa & Sains",
    img=img("ayam-berkokok-tengah-malam", "Hadis Sahih", "Ayam Berkokok Tengah Malam", "Maksud hadis, doa & sebab saintifik", "صِيَاحَ الدِّيَكَةِ"),
    alt="Ayam berkokok tengah malam menurut hadis dan sains", refshort="Sahih Al-Bukhari, Sahih Muslim, Sunan Abu Daud",
    lead="Apa kata hadis sahih tentang kokok ayam, doa yang disunatkan, mengapa ayam berkokok pada jam 1 atau 3 pagi menurut kajian saintifik, dan mitos yang tidak berasas.",
    crumb=("Hadis", W + "search/label/Hadis"), about=["Ayam berkokok", "Hadis tentang haiwan", "Qiamullail"],
    answer="Nabi SAW bersabda: <strong>“Apabila kamu mendengar ayam berkokok, mintalah kurnia daripada Allah, kerana ia telah melihat malaikat”</strong> <em>(HR Al-Bukhari, no. 3303; Muslim, no. 2729)</em>. "
           "Doa ringkas yang boleh dibaca ialah <strong>“Allahumma inni as'aluka min fadhlik”</strong>. Dari segi sains, ayam berkokok pada waktu malam kerana <strong>jam biologi (circadian)</strong>, cahaya lampu, bunyi, atau persaingan antara ayam jantan.",
    sections=[
        ("hadis", "Hadis Ayam Berkokok dan Maksudnya",
         dc(P, "Ayam melihat malaikat", "إِذَا سَمِعْتُمْ صِيَاحَ الدِّيَكَةِ فَاسْأَلُوا اللّٰهَ مِنْ فَضْلِهِ، فَإِنَّهَا رَأَتْ مَلَكًا", "Idha sami'tum siyahad-diyakati fas'alullaha min fadhlih, fa innaha ra'at malakan.",
            "Apabila kamu mendengar ayam jantan berkokok, mintalah kurnia daripada Allah, kerana ia telah melihat malaikat.", "HR Al-Bukhari, no. 3303; Muslim, no. 2729")
         + "<p>Sambungan hadis yang sama: “Dan apabila kamu mendengar keldai meringkik, mohonlah perlindungan dengan Allah daripada syaitan, kerana ia telah melihat syaitan.” "
           "Ulama menjelaskan bahawa berdoa ketika malaikat hadir mengharapkan malaikat mengaminkan doa itu.</p>"
         + dc(P, "Jangan mencela ayam jantan", "لَا تَسُبُّوا الدِّيكَ، فَإِنَّهُ يُوقِظُ لِلصَّلَاةِ", "La tasubbud-dik, fa innahu yuqizu lis-solah.",
              "Janganlah kamu mencela ayam jantan, kerana ia membangunkan (manusia) untuk solat.", "HR Abu Daud, no. 5101 (sahih)")),
        ("doa", "Doa Ketika Mendengar Ayam Berkokok",
         dc(P, "Doa memohon kurnia Allah", "اللّٰهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ", "Allahumma inni as'aluka min fadhlik.", "Ya Allah, aku memohon kepada-Mu sebahagian daripada kurnia-Mu.",
            "Lafaz daripada HR Muslim, no. 713", "Hadis ayam berkokok tidak menetapkan lafaz khusus. Lafaz ini daripada doa keluar masjid dan sesuai dengan perintah “mintalah kurnia Allah”. Anda juga boleh berdoa apa-apa hajat dengan bahasa sendiri.")
         + "<h3>Apa yang patut dibuat jika terjaga kerana kokok ayam</h3>"
         + ul("Baca doa bangun tidur dan doa memohon kurnia di atas.", "Jika sudah sepertiga malam terakhir, ambil wuduk dan solat tahajud walaupun dua rakaat.",
              "Mohon hajat kerana sepertiga malam terakhir ialah waktu Allah turun ke langit dunia dan bertanya siapa yang berdoa" + ref("HR Al-Bukhari, no. 1145; Muslim, no. 758"),
              "Aisyah RA meriwayatkan Nabi SAW bangun untuk solat malam apabila mendengar <em>as-sarikh</em>, iaitu ayam berkokok" + ref("HR Al-Bukhari, no. 1132; Muslim, no. 741"))
         + f'<p>Bacaan lengkap: <a href="{Q}doa-bangun-tidur/">Doa Bangun Tidur</a> dan <a href="{Q}solat-sunat/">Solat Sunat Tahajud</a>.</p>'),
        ("sains", "Kenapa Ayam Berkokok Tengah Malam? Penjelasan Saintifik",
         table(["Sebab", "Penjelasan"], [
             ["Jam biologi (circadian)", "Kajian Shimmura dan Yoshimura (Current Biology, 2013) mendapati ayam jantan berkokok sebelum subuh mengikut jam dalaman, walaupun dalam bilik yang sentiasa malap. Kokok pertama biasanya kira-kira dua jam sebelum cahaya pertama."],
             ["Cahaya buatan", "Lampu jalan, lampu rumah atau lampu kenderaan boleh mencetuskan kokok pada jam 1 atau 2 pagi."],
             ["Bunyi dan gangguan", "Kenderaan, anjing, atau pemangsa seperti musang dan ular membuatkan ayam berkokok sebagai amaran."],
             ["Hierarki ayam jantan", "Kajian Shimmura dan rakan-rakan (Scientific Reports, 2015) menunjukkan ayam jantan paling dominan berkokok dahulu, dan yang lain menyusul."],
             ["Kokok berantai", "Seekor ayam berkokok, ayam di kampung sebelah menjawab, lalu kokok bersahut-sahutan."]])
         + "<p>Penjelasan sains tidak bercanggah dengan hadis. Hadis menyebut perkara ghaib yang dilihat ayam, manakala sains menjelaskan mekanisme biologi yang Allah ciptakan pada haiwan itu.</p>"),
        ("mitos", "Mitos Ayam Berkokok yang Perlu Dielakkan",
         table(["Kepercayaan", "Hukum"], [
             ["Ayam berkokok jam 1 pagi tanda ada orang akan mati", "Tiada asas. Ia termasuk tathayyur (percaya sial) yang dilarang"],
             ["Ayam berkokok tengah malam tanda anak dara hamil atau ada maksiat di kampung", "Khurafat. Menuduh tanpa bukti boleh menjadi fitnah dan qazaf"],
             ["Ayam berkokok kerana nampak harimau atau hantu", "Tiada hadis menyebut harimau. Hadis menyebut keldai melihat syaitan, bukan ayam"],
             ["Ayam berkokok waktu maghrib membawa malang", "Tiada asas. Tiada sial pada haiwan atau waktu"]])
         + "<p>Nabi SAW bersabda: “Tiada penyakit berjangkit dengan sendirinya dan tiada sial (tiyarah)”" + ref("HR Al-Bukhari, no. 5757; Muslim, no. 2220")
         + ". Kokok ayam ialah peringatan untuk berdoa dan bangun beribadah, bukan petanda nasib.</p>"),
        ("pengajaran", "Pengajaran daripada Hadis Ini",
         ul("Haiwan boleh melihat perkara ghaib yang tidak dilihat manusia; ia mengingatkan kita tentang alam malaikat.",
            "Setiap bunyi di sekeliling boleh menjadi pencetus zikir: kokok ayam untuk berdoa, ringkikan keldai dan salakan anjing untuk berta'awwudz" + ref("HR Abu Daud, no. 5103"),
            "Ayam jantan dipuji kerana membangunkan orang untuk solat. Orang yang mengejutkan keluarga untuk Subuh mewarisi sifat ini.")),
    ],
    faq=[("Apakah maksud ayam berkokok tengah malam dalam Islam?", "Menurut hadis sahih, ayam berkokok kerana melihat malaikat, maka disunatkan berdoa memohon kurnia Allah (HR Al-Bukhari 3303; Muslim 2729)."),
         ("Apakah doa ketika mendengar ayam berkokok?", "Mintalah kurnia Allah, contohnya “Allahumma inni as'aluka min fadhlik” (Ya Allah, aku memohon kurnia-Mu). Hadis tidak menetapkan lafaz khusus."),
         ("Kenapa ayam berkokok jam 1 atau 3 pagi?", "Kerana jam biologi yang membuatkan ayam berkokok sebelum subuh, cahaya lampu, bunyi atau gangguan pemangsa, dan kokok bersahut antara ayam jantan."),
         ("Adakah ayam berkokok tengah malam petanda buruk?", "Tidak. Mempercayai petanda sial termasuk tathayyur yang dilarang (HR Al-Bukhari 5757)."),
         ("Bolehkah memarahi ayam yang berkokok malam?", "Nabi SAW melarang mencela ayam jantan kerana ia membangunkan manusia untuk solat (HR Abu Daud 5101).")],
    refs=["Sahih Al-Bukhari, no. 1132, 1145, 3303, 5757.", "Sahih Muslim, no. 713, 741, 758, 2220, 2729.", "Sunan Abu Daud, no. 5101, 5103.",
          "Shimmura T, Yoshimura T. Circadian clock determines the timing of rooster crowing. Current Biology, 2013;23(6):R231–R233.",
          "Shimmura T, Ohashi S, Yoshimura T. The highest-ranking rooster has priority to announce the break of dawn. Scientific Reports, 2015;5:11683."],
    badges=["Hadis Sahih", "Rujukan Kajian Saintifik", "Dikemas kini 2026"],
    related=[(Q + "doa-bangun-tidur/", "Doa Bangun Tidur", "Bacaan sahih ketika terjaga"), (Q + "solat-sunat/", "Solat Sunat", "Tahajud, witir dan solat malam"),
             (U["didoakan-malaikat"], "Golongan yang Didoakan Malaikat", "10 amalan menurut hadis sahih")])))


if __name__ == "__main__":
    write(POSTS)
