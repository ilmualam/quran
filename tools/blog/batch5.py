"""Batch 5: two NEW www.ilmualam.com posts for keyword gaps found in the Nov 2026 research (no existing post on either site):
solat berjemaah (cluster ~3,700/mo, SD 13-24) and Imam Mahdi (2,400/mo, SD 17). Created as Blogger drafts with a short title first so the
permalink is /2026/11/<slug>.html, then given the full title (apply_new.py). Run from tools/blog: PYTHONPATH=.. python3 batch5.py"""
from gen import write, Q
from cards import card as img
from batch3 import ul, ref, dc, grade, base, SAHIH, HASAN, DHAIF, qcard, table

W = "https://www.ilmualam.com/"
MOD, MODMS = "2026-11-20", "20 November 2026"
NEW = {"solat-berjemaah": ("Solat Berjemaah", W + "2026/11/solat-berjemaah.html"),
       "imam-mahdi": ("Imam Mahdi", W + "2026/11/imam-mahdi.html")}
WHEN = {"solat-berjemaah": "2026-11-20T20:30:00+08:00", "imam-mahdi": "2026-11-21T12:30:00+08:00"}
KIAMAT = W + "2017/12/tanda-tanda-kiamat-kecil-telah-lengkap.html"
SOLAT_PAHALA = W + "2018/02/9-kemuliaan-orang-menjaga-solat.html"
MAKMUM = W + "2018/02/makmum-batal-lewat-depan-makmum-lainnya.html"
DIDOAKAN = W + "2017/11/7-jenis-manusia-yang-didoakan-malaikat.html"


def b5(**k):
    k.setdefault("modified", MOD); k.setdefault("modms", MODMS); k.setdefault("published", MOD); k.setdefault("pubms", MODMS)
    return base(**k)


POSTS = []

# 1 ---------------------------------------------------------------- Solat berjemaah
P = "ilmx-sb"
NIAT_MAKMUM = ("أُصَلِّي فَرْضَ الظُّهْرِ أَرْبَعَ رَكَعَاتٍ مُسْتَقْبِلَ الْقِبْلَةِ أَدَاءً مَأْمُومًا لِلّٰهِ تَعَالَى",
               "Usolli fardhaz-zuhri arba'a raka'atin mustaqbilal-qiblati ada'an ma'muman lillahi ta'ala.",
               "Sahaja aku solat fardu Zohor empat rakaat menghadap kiblat, tunai, sebagai makmum kerana Allah Ta'ala.")
NIAT_IMAM = ("أُصَلِّي فَرْضَ الظُّهْرِ أَرْبَعَ رَكَعَاتٍ مُسْتَقْبِلَ الْقِبْلَةِ أَدَاءً إِمَامًا لِلّٰهِ تَعَالَى",
             "Usolli fardhaz-zuhri arba'a raka'atin mustaqbilal-qiblati ada'an imaman lillahi ta'ala.",
             "Sahaja aku solat fardu Zohor empat rakaat menghadap kiblat, tunai, sebagai imam kerana Allah Ta'ala.")
POSTS.append(("solat-berjemaah", b5(
    ns=P, url=NEW["solat-berjemaah"][1],
    title="Solat Berjemaah: Hukum, Niat Makmum, Syarat Sah & Kelebihan (Syafi'i)",
    desc="Panduan solat berjemaah mazhab Syafi'i: hukum, niat imam dan makmum, syarat sah mengikut imam, susunan saf, makmum masbuq dan pahala 27 darjat.",
    h1="Solat Berjemaah: Hukum, Niat & Syarat Sah",
    img=img("solat-berjemaah", "Fiqh Solat", "Solat Berjemaah", "Hukum, niat makmum, syarat sah & kelebihan", "صَلَاةُ الْجَمَاعَةِ"),
    alt="Panduan solat berjemaah: hukum, niat makmum dan syarat sah", refshort="Sahih Al-Bukhari, Sahih Muslim, kitab fiqh Syafi'i",
    lead="Semua yang perlu diketahui sebelum solat berjemaah di masjid atau di rumah: hukum, lafaz niat imam dan makmum, syarat sah mengikut imam, susunan saf dan cara makmum masbuq.",
    crumb=("Solat", W + "search/label/Solat"), about=["Solat berjemaah", "Niat makmum", "Makmum masbuq"],
    answer="Menurut pendapat yang paling sahih dalam mazhab Syafi'i, solat berjemaah bagi solat fardu ialah <strong>fardu kifayah</strong> bagi lelaki yang bermukim, dan <strong>sunat</strong> bagi wanita. "
           "Pahalanya <strong>27 kali ganda</strong> berbanding solat bersendirian <em>(HR Al-Bukhari, no. 645; Muslim, no. 650)</em>. Makmum <strong>wajib berniat mengikut imam</strong> (contoh: “…ada'an ma'muman lillahi ta'ala”), "
           "tidak berdiri di hadapan imam, mengetahui pergerakan imam dan tidak mendahuluinya.",
    sections=[
        ("hukum", "Hukum Solat Berjemaah",
         table(["Golongan", "Hukum (mazhab Syafi'i)", "Nota"], [
             ["Lelaki baligh yang bermukim, solat fardu", "Fardu kifayah (pendapat paling sahih)", "Sebahagian ulama Syafi'i berpendapat sunat muakkad; berdosa jika satu kawasan meninggalkannya sama sekali"],
             ["Solat Jumaat", "Fardu ain bagi lelaki yang cukup syarat", "Berjemaah ialah syarat sah Jumaat"],
             ["Wanita", "Sunat", "Solat di rumah lebih afdal (HR Abu Daud, no. 567), tetapi tidak boleh dihalang ke masjid (HR Al-Bukhari, no. 900)"],
             ["Solat sunat seperti tarawih, gerhana dan hari raya", "Sunat berjemaah", "Rawatib dan dhuha tidak disunatkan berjemaah"]])
         + "<p>Ketegasan Nabi SAW jelas dalam hadis seorang lelaki buta yang meminta keringanan; Baginda bertanya: “Adakah engkau mendengar azan?” Dia menjawab ya. Baginda bersabda: “Maka sahutlah”" + ref("HR Muslim, no. 653") + ".</p>"),
        ("kelebihan", "Kelebihan dan Pahala Solat Berjemaah",
         grade([("Lebih utama 27 darjat daripada solat bersendirian", "HR Al-Bukhari, no. 645; Muslim, no. 650", SAHIH),
                ("Isyak berjemaah seperti qiyam separuh malam; ditambah Subuh berjemaah seperti qiyam sepanjang malam", "HR Muslim, no. 656", SAHIH),
                ("Setiap langkah ke masjid menghapus dosa dan mengangkat darjat", "HR Muslim, no. 666", SAHIH),
                ("Malaikat berdoa untuk orang yang menunggu solat", "HR Al-Bukhari, no. 659", SAHIH),
                ("Sesiapa yang solat 40 hari berjemaah mendapat takbiratul ihram, ditulis baginya dua kelepasan: daripada neraka dan nifaq", "HR At-Tirmizi, no. 241; diperselisihkan, dinilai hasan oleh sebahagian ulama", HASAN)], head="Kelebihan")
         + f'<p>Kelebihan menjaga solat secara umum: <a href="{SOLAT_PAHALA}">9 Kemuliaan Orang yang Menjaga Solat</a>. Golongan yang didoakan malaikat: <a href="{DIDOAKAN}">10 Golongan Didoakan Malaikat</a>.</p>'),
        ("niat", "Niat Solat Berjemaah: Imam dan Makmum",
         dc(P, "Niat makmum (contoh Zohor)", *NIAT_MAKMUM, "Lafaz niat mazhab Syafi'i; niat sebenar di dalam hati ketika takbiratul ihram",
            "Tukar “az-zuhri arba'a” mengikut solat: as-subhi rak'ataini, al-'asri arba'a, al-maghribi thalatha, al-'isya'i arba'a.")
         + dc(P, "Niat imam (contoh Zohor)", *NIAT_IMAM, "Lafaz niat mazhab Syafi'i",
              "Bagi imam, niat menjadi imam sunat untuk mendapat pahala jemaah, kecuali solat Jumaat yang wajib.")
         + "<p>Makmum yang tidak berniat mengikut imam, tetapi menunggu dan mengikut pergerakan imam dengan lama, batal solatnya menurut mazhab Syafi'i. Oleh itu, niat makmum ialah syarat yang wajib.</p>"),
        ("syarat", "Syarat Sah Mengikut Imam",
         ul("Makmum <strong>berniat mengikut imam</strong> (berjemaah atau sebagai makmum).",
            "Makmum <strong>tidak berdiri di hadapan imam</strong>; ukurannya tumit.",
            "Makmum <strong>mengetahui pergerakan imam</strong>, dengan melihat imam, saf hadapan atau mendengar suara muballigh.",
            "Imam dan makmum <strong>berada dalam satu tempat</strong>; dalam masjid sah walaupun jauh, di luar masjid jarak tidak melebihi kira-kira 300 hasta tanpa halangan.",
            "<strong>Tidak mendahului imam</strong> dalam takbiratul ihram, dan tidak ketinggalan dua rukun fi'li tanpa uzur.",
            "<strong>Bentuk solat yang sama</strong>, contohnya tidak sah solat fardu mengikut imam solat jenazah atau gerhana.",
            "Imam bukan seorang makmum, dan solatnya sah menurut pandangan makmum.", ordered=True)
         + "<p>Nabi SAW bersabda: “Tidakkah orang yang mengangkat kepalanya sebelum imam takut Allah menukar kepalanya menjadi kepala keldai?”" + ref("HR Al-Bukhari, no. 691")
         + ". Mendahului imam dengan sengaja hukumnya haram.</p>"
         + f'<p>Jika batal wuduk ketika berjemaah: <a href="{MAKMUM}">Makmum Batal, Lalu di Depan Makmum Lain</a>.</p>'),
        ("saf", "Susunan Saf dan Kedudukan Makmum",
         table(["Keadaan", "Kedudukan"], [
             ["Seorang makmum lelaki", "Di sebelah kanan imam, sedikit ke belakang"],
             ["Dua makmum lelaki atau lebih", "Di belakang imam"],
             ["Suami dan isteri berdua", "Isteri di belakang suami, bukan di sebelahnya" + ref("HR Al-Bukhari, no. 727")],
             ["Lelaki, kanak-kanak dan wanita", "Saf lelaki dewasa, kemudian kanak-kanak lelaki, kemudian wanita"],
             ["Wanita sesama wanita", "Imam wanita berdiri di tengah saf pertama"]])
         + "<p>“Luruskanlah saf kamu, kerana meluruskan saf termasuk kesempurnaan solat”" + ref("HR Al-Bukhari, no. 723; Muslim, no. 433") + ". Rapatkan bahu dan kaki dengan jemaah di sebelah, dan penuhkan saf hadapan dahulu.</p>"),
        ("masbuq", "Makmum Masbuq: Datang Lewat",
         ul("Takbiratul ihram dalam keadaan berdiri, kemudian terus ikut keadaan imam (rukuk, sujud atau duduk).",
            "Jika sempat <strong>rukuk bersama imam dengan tomakninah</strong> sebelum imam bangkit, rakaat itu dikira.",
            "Selepas imam memberi salam, bangun dan sempurnakan rakaat yang tertinggal.",
            "“Apa yang kamu dapati, solatlah; apa yang terlepas, sempurnakanlah”" + ref("HR Al-Bukhari, no. 636; Muslim, no. 602"),
            "Datang ke solat dengan tenang, jangan berlari walaupun iqamah telah dilaungkan" + ref("HR Al-Bukhari, no. 636")),
         ),
        ("rumah", "Solat Berjemaah di Rumah",
         "<p>Solat berjemaah bersama isteri dan anak di rumah <strong>sah dan mendapat pahala jemaah</strong>, dan ia cara terbaik mendidik anak. Namun bagi lelaki, berjemaah di masjid lebih utama kerana syiar dan pahala langkah ke masjid. "
         "Jika berjemaah di rumah, suami menjadi imam, isteri berdiri di belakang, dan anak lelaki yang sudah mumayyiz boleh berdiri di sebelah kanan bapa.</p>"
         + f'<p>Selepas salam, baca zikir dan doa: <a href="{Q}doa-selepas-solat/">Doa Selepas Solat</a>. Panduan setiap rukun: <a href="{Q}belajar-solat/">Belajar Solat</a>.</p>'),
    ],
    faq=[("Apakah hukum solat berjemaah?", "Fardu kifayah bagi lelaki yang bermukim menurut pendapat paling sahih mazhab Syafi'i, fardu ain bagi solat Jumaat, dan sunat bagi wanita."),
         ("Apakah niat solat berjemaah sebagai makmum?", "Contoh Zohor: “Usolli fardhaz-zuhri arba'a raka'atin mustaqbilal-qiblati ada'an ma'muman lillahi ta'ala”. Niat mengikut imam wajib bagi makmum."),
         ("Apakah syarat sah solat berjemaah?", "Makmum berniat mengikut imam, tidak berdiri di hadapan imam, mengetahui pergerakan imam, berada dalam satu tempat, tidak mendahului imam, dan bentuk solat yang sama."),
         ("Berapa pahala solat berjemaah?", "27 darjat lebih utama daripada solat bersendirian (HR Al-Bukhari 645; Muslim 650)."),
         ("Bagaimana kedudukan suami isteri solat berjemaah?", "Suami menjadi imam dan isteri berdiri di belakangnya, bukan di sebelah (HR Al-Bukhari 727)."),
         ("Bilakah makmum masbuq mendapat satu rakaat?", "Apabila sempat rukuk bersama imam dengan tomakninah sebelum imam bangkit daripada rukuk. Rakaat yang tertinggal disempurnakan selepas imam memberi salam.")],
    refs=["Sahih Al-Bukhari, no. 636, 645, 659, 691, 723, 727, 900.", "Sahih Muslim, no. 433, 602, 650, 653, 656, 666.", "Sunan Abu Daud, no. 567; Sunan At-Tirmizi, no. 241.",
          "An-Nawawi, Minhaj At-Talibin dan Al-Majmu', bab solat berjemaah.", "Al-Khatib Asy-Syirbini, Mughni Al-Muhtaj, bab solat berjemaah."],
    disclaimer="Panduan ringkas mengikut mazhab Syafi'i. Untuk kes khusus seperti jemaah di luar masjid atau dalam talian, rujuk pejabat agama Islam negeri anda.",
    related=[(Q + "belajar-solat/", "Belajar Solat", "Panduan setiap rukun dengan bacaan"), (Q + "doa-selepas-solat/", "Doa Selepas Solat", "Zikir dan doa selepas solat fardu"),
             (SOLAT_PAHALA, "Kelebihan Menjaga Solat", "9 kemuliaan dengan dalil sahih")])))

# 2 ---------------------------------------------------------------- Imam Mahdi
P = "ilmx-im"
POSTS.append(("imam-mahdi", b5(
    ns=P, url=NEW["imam-mahdi"][1],
    title="Imam Mahdi Menurut Hadis Sahih: Siapa, Ciri-Ciri & Bila Muncul",
    desc="Siapa Imam Mahdi menurut Ahli Sunnah: nama, keturunan dan ciri-cirinya dalam hadis, status setiap riwayat, kaitan dengan Nabi Isa dan amaran Mahdi palsu.",
    h1="Imam Mahdi Menurut Hadis",
    img=img("imam-mahdi", "Akidah", "Imam Mahdi", "Siapa, ciri-ciri & status setiap hadis", "الْمَهْدِيُّ"),
    alt="Imam Mahdi menurut hadis sahih", refshort="Sunan Abu Daud, Sunan At-Tirmizi, Sahih Muslim",
    lead="Apa yang thabit tentang Imam Mahdi dalam hadis, apa yang tidak, mengapa namanya tidak disebut dalam Al-Quran, dan cara mengenal pasti dakwaan Mahdi palsu.",
    crumb=("Akidah", W + "search/label/Akidah"), about=["Imam Mahdi", "Tanda kiamat"],
    answer="Imam Mahdi ialah seorang lelaki daripada <strong>keturunan Nabi SAW melalui Fatimah RA</strong>, yang <strong>namanya seperti nama Nabi (Muhammad) dan nama bapanya seperti nama bapa Nabi (Abdullah)</strong>. "
           "Dia akan <strong>memenuhi bumi dengan keadilan</strong> sebagaimana bumi dipenuhi kezaliman, menjelang turunnya Nabi Isa AS <em>(HR Abu Daud, no. 4282, 4284, 4285; At-Tirmizi, no. 2230)</em>. "
           "Ahli Sunnah wal Jamaah menerima kemunculannya, tetapi <strong>tiada siapa tahu bila dan di mana</strong> dia akan muncul, dan namanya tidak disebut dalam Al-Quran.",
    sections=[
        ("hadis", "Hadis tentang Imam Mahdi dan Statusnya",
         grade([("Jika dunia tinggal sehari, Allah panjangkan hari itu sehingga diutus seorang lelaki daripada keluargaku; namanya seperti namaku dan nama bapanya seperti nama bapaku", "HR Abu Daud, no. 4282; At-Tirmizi, no. 2230 (hasan sahih)", SAHIH),
                ("Al-Mahdi daripada keturunanku, daripada anak-anak Fatimah", "HR Abu Daud, no. 4284; Ibn Majah, no. 4086", SAHIH),
                ("Al-Mahdi daripadaku: dahinya luas, hidungnya mancung; dia memenuhi bumi dengan keadilan dan memerintah tujuh tahun", "HR Abu Daud, no. 4285", HASAN),
                ("Al-Mahdi daripada kami, ahlul bait; Allah memperbaikinya dalam satu malam", "HR Ibn Majah, no. 4085; diperselisihkan", HASAN),
                ("Isa AS turun, lalu pemimpin umat Islam menjemputnya mengimami solat; Isa menolak: “Sebahagian kamu pemimpin bagi sebahagian yang lain”", "HR Muslim, no. 156 (nama Mahdi tidak disebut; ulama mengaitkannya)", SAHIH),
                ("Dibai'ah di antara Rukun dan Maqam Ibrahim di Mekah selepas perselisihan ketika kematian seorang khalifah", "HR Abu Daud, no. 4286; sanadnya dipertikaikan", DHAIF),
                ("Panji-panji hitam dari Khurasan, di dalamnya ada khalifah Allah Al-Mahdi", "HR Ibn Majah, no. 4084; Ahmad", DHAIF)], head="Riwayat")),
        ("ciri", "Ciri-Ciri Imam Mahdi yang Thabit",
         table(["Ciri", "Sumber"], [["Daripada keturunan Nabi SAW melalui Fatimah RA", "HR Abu Daud 4284"], ["Namanya Muhammad bin Abdullah", "HR Abu Daud 4282"],
                                   ["Dahi luas dan hidung mancung", "HR Abu Daud 4285"], ["Memerintah dengan adil, memenuhi bumi dengan keadilan", "HR Abu Daud 4282, 4285"],
                                   ["Memerintah sekitar tujuh tahun", "HR Abu Daud 4285"], ["Muncul sebelum turunnya Nabi Isa AS dan menjadi imam solat ketika itu", "HR Muslim 156 menurut tafsiran ulama"]])
         + "<p>Ciri-ciri lain yang tersebar, seperti tanda di bahu, tarikh kemunculan, atau nama negeri tertentu di Nusantara, <strong>tiada sumber hadis yang sahih</strong>.</p>"),
        ("quran", "Adakah Imam Mahdi Disebut dalam Al-Quran?",
         "<p><strong>Tidak.</strong> Tiada ayat Al-Quran yang menyebut nama atau sifat Al-Mahdi secara jelas. Kepercayaan tentangnya bersandarkan hadis. Ulama seperti Asy-Syaukani menyebut hadis-hadis Mahdi, secara keseluruhan maknanya, "
         "mencapai tahap mutawatir maknawi, walaupun banyak riwayat secara individu lemah.</p>"),
        ("bila", "Bila dan di Mana Imam Mahdi Akan Muncul?",
         "<p>Hadis yang sahih tidak menyebut tahun atau tempat yang pasti. Riwayat bai'ah di Mekah" + ref("HR Abu Daud, no. 4286") + " sanadnya dipertikaikan. "
         "Pengetahuan tentang hari kiamat dan tanda-tandanya yang terperinci hanya di sisi Allah" + ref("Al-A'raf 7:187") + ".</p>"
         + f'<p>Kedudukan Mahdi antara tanda-tanda kiamat: <a href="{KIAMAT}">Tanda-Tanda Kiamat Kecil & Besar</a>. Perlindungan daripada fitnah Dajjal: <a href="{Q}surah-al-kahfi/">10 ayat awal Surah Al-Kahfi</a>' + ref("HR Muslim, no. 809") + ".</p>"),
        ("palsu", "Amaran: Dakwaan Mahdi Palsu",
         f'<div class="{P}-box amber">Sepanjang sejarah, ramai individu mendakwa diri mereka Al-Mahdi, termasuk di Malaysia, dan beberapa ajaran telah difatwakan sesat oleh pihak berkuasa agama. '
         "Imam Mahdi yang sebenar <strong>tidak perlu mengumpul pengikut secara rahsia, mengutip wang atau menjanjikan kedudukan</strong>; kemunculannya akan diketahui umum.</div>"
         + ul("Tolak sesiapa yang mendakwa dirinya atau gurunya ialah Al-Mahdi.", "Jangan sebarkan ramalan tarikh atau video “tanda Mahdi sudah muncul”.",
              "Rujuk Jabatan Agama Islam negeri jika menemui ajaran yang mendakwa demikian.")
         + "<p>Fahaman Syiah Imamiyyah tentang Al-Mahdi (imam kedua belas yang ghaib sejak abad ketiga Hijrah) berbeza daripada pegangan Ahli Sunnah wal Jamaah, yang meyakini Al-Mahdi akan dilahirkan dan muncul pada masanya.</p>"),
        ("sikap", "Sikap Seorang Muslim",
         "<p>Beriman dengan kemunculan Al-Mahdi tidak bermaksud menunggu tanpa beramal. Nabi SAW bersabda: “Jika kiamat berlaku sedangkan di tangan seseorang ada anak pokok kurma, jika dia mampu menanamnya sebelum kiamat, maka tanamlah”"
         + ref("HR Ahmad, no. 12902; sahih") + ". Teruskan berbuat baik, menjaga solat dan menuntut ilmu.</p>"),
    ],
    faq=[("Siapakah Imam Mahdi?", "Seorang lelaki daripada keturunan Nabi SAW melalui Fatimah RA, bernama Muhammad bin Abdullah, yang memenuhi bumi dengan keadilan menjelang turunnya Nabi Isa AS (HR Abu Daud 4282, 4284)."),
         ("Apakah ciri-ciri Imam Mahdi?", "Daripada ahlul bait, dahinya luas, hidungnya mancung, memerintah dengan adil sekitar tujuh tahun (HR Abu Daud 4285)."),
         ("Adakah Imam Mahdi disebut dalam Al-Quran?", "Tidak. Kepercayaan tentangnya bersandarkan hadis, yang secara keseluruhan diterima oleh Ahli Sunnah wal Jamaah."),
         ("Bilakah Imam Mahdi akan muncul?", "Tiada hadis sahih yang menyebut tarikh atau tempat yang pasti. Sebarang ramalan tarikh tidak berasas."),
         ("Apakah hubungan Imam Mahdi dengan Nabi Isa?", "Ketika Nabi Isa AS turun, pemimpin umat Islam menjemputnya mengimami solat dan Baginda menolak (HR Muslim 156); ulama menyatakan pemimpin itu ialah Al-Mahdi.")],
    refs=["Sunan Abu Daud, no. 4282, 4284, 4285, 4286.", "Sunan At-Tirmizi, no. 2230; Sunan Ibn Majah, no. 4084, 4085, 4086.", "Sahih Muslim, no. 156, 809.", "Musnad Ahmad, no. 12902.",
          "Al-Quran: Al-A'raf 7:187.", "Asy-Syaukani, At-Taudhih fi Tawatur ma Ja'a fil-Mahdi wad-Dajjal wal-Masih."],
    disclaimer="Panduan akidah ringkas mengikut Ahli Sunnah wal Jamaah. Status riwayat dinyatakan supaya pembaca dapat membezakan yang thabit dan yang tidak.",
    related=[(KIAMAT, "Tanda-Tanda Kiamat Kecil & Besar", "Senarai lengkap dengan hadis sahih"), (Q + "surah-al-kahfi/", "Surah Al-Kahfi", "Pelindung daripada fitnah Dajjal"),
             (W + "2018/02/mampukah-kita-jawab-5-soalan-di-dalam.html", "Soalan Kubur", "3 soalan Munkar Nakir dan jawapannya")])))


if __name__ == "__main__":
    write(POSTS)
