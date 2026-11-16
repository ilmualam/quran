"""Batch 4 (fiqh harian, keluarga, amalan): the last 15 refreshed www.ilmualam.com posts. Each targets the primary keyword chosen
from Ubersuggest Malaysia data (Nov 2026) and keeps its original URL. Merged duplicates already redirect here (applied with the triage).
Run from tools/blog: PYTHONPATH=.. python3 batch4.py"""
from gen import write, Q
from cards import card as img
from batch3 import ul, ref, dc, grade, base, SAHIH, HASAN, DHAIF, NOSRC, qcard, table

W = "https://www.ilmualam.com/"
MOD, MODMS = "2026-11-17", "17 November 2026"
U = {
    "air-mazi": W + "2018/01/beza-air-mani-yang-keluar-dari-kemaluan.html",
    "bismillah-5": W + "2020/04/khasiat-bismillah-5-rumi-dan-terjemahan.html",
    "tanggungjawab-suami": W + "2018/02/inilah-dosa-suami-kesan-kepada-isteri.html",
    "sunnah-nabi": W + "2020/07/7-sunnah-nabi-yang-mudah-diamalkan.html",
    "sunnah-fitrah": W + "2018/02/kenapa-kita-perlu-cukur-bulu-kemaluan.html",
    "sedekah-jariah": W + "2020/01/7-amalan-yang-pahalanya-terus-mengalir.html",
    "amalan-pahala-besar": W + "2020/02/8-amalan-yang-amat-besar-ganjaran.html",
    "wanita-neraka": W + "2017/12/tahukah-kamu-ternyata-wanita-adalah.html",
    "hari-jadi": W + "2020/01/hukum-tiup-lilin-kek-hari-jadi-ulang.html",
    "mengungkit": W + "2020/01/hukum-bersedekah-tapi-mengungkit.html",
    "suara-wanita": W + "2018/02/hukum-wanita-menyanyi-disisi-islam.html",
    "keras-hati": W + "2018/01/tanda-tanda-penyakit-keras-hati-dan.html",
    "akidah-anak": W + "2018/01/3-cara-menanamkan-akidah-pada-anak-anak.html",
    "kalimah-dibenci": W + "2018/02/sering-diucapkan-padahal-kalimat-ini.html",
    "doa-syirik": W + "2018/01/doa-berlindung-dari-kesyirikan.html",
}
SEDEKAH = W + "2025/11/apa-itu-sedekah.html"
SOLAT_ANAK = W + "2026/07/cara-ajar-anak-solat-awal.html"
DOA_ANAK = W + "2026/05/doa-anak-soleh-solehah.html"
DOA_SUAMI = W + "2026/05/doa-suami-berubah-sikap.html"
MANDI = W + "2020/01/cara-mandi-wajib-yang-betul.html"
PUASA = W + "2020/04/perkara-yang-membatalkan-puasa-ramadhan.html"
SYIRIK = W + "2020/01/baca-dan-fahami-allah-tidak.html"
MUQALLIB = W + "2018/02/doa-mohon-allah-swt-tetapkan-hidayah.html"
TERANIAYA = W + "2017/11/hati-hati-terhadap-doa-orang-yang.html"
MALAIKAT = W + "2017/11/7-jenis-manusia-yang-didoakan-malaikat.html"


def b4(**k):
    k.setdefault("modified", MOD); k.setdefault("modms", MODMS)
    return base(**k)


POSTS = []

# 1 ---------------------------------------------------------------- Air mazi, mani, wadi (air mazi 4,400/mo, SD 13)
P = "ilmx-mz"
POSTS.append(("air-mazi", b4(
    ns=P, url=U["air-mazi"], published="2018-01-28", pubms="28 Januari 2018",
    title="Air Mazi, Mani & Wadi: Beza, Hukum Mandi Wajib & Puasa (Syafi'i)",
    desc="Beza air mazi, mani dan wadi bagi lelaki dan perempuan: ciri, najis atau suci, perlu mandi wajib atau tidak, batal puasa atau tidak, dan cara membersihkannya.",
    h1="Air Mazi, Mani & Wadi: Beza dan Hukumnya",
    img=img("air-mazi-mani-wadi", "Fiqh Taharah", "Air Mazi, Mani & Wadi", "Beza, hukum mandi wajib & puasa", "الطَّهَارَة"),
    alt="Beza air mazi, mani dan wadi menurut mazhab Syafi'i", refshort="Sahih Al-Bukhari, Sahih Muslim, kitab fiqh Syafi'i",
    lead="Jadual perbezaan tiga cecair yang paling kerap ditanya, hukumnya dalam mazhab Syafi'i bagi lelaki dan perempuan, serta kesannya kepada wuduk, mandi wajib, solat dan puasa.",
    crumb=("Fiqh", W + "search/label/Fiqh"), about=["Air mazi", "Air mani", "Air wadi"],
    answer="<strong>Air mazi</strong> ialah cecair jernih dan licin yang keluar ketika syahwat mula bangkit, tanpa memancut dan tanpa rasa lazat yang memuncak. Ia <strong>najis, membatalkan wuduk, tetapi tidak mewajibkan mandi</strong>: basuh kemaluan dan bahagian yang terkena, kemudian berwuduk <em>(HR Al-Bukhari, no. 269; Muslim, no. 303)</em>. "
           "<strong>Air mani</strong> pula suci tetapi <strong>mewajibkan mandi</strong>, manakala <strong>air wadi</strong> ialah cecair putih pekat selepas kencing yang najis dan membatalkan wuduk sahaja. Dalam mazhab Syafi'i, <strong>keluar mazi tidak membatalkan puasa</strong>.",
    sections=[
        ("jadual", "Jadual Beza Air Mazi, Mani dan Wadi",
         table(["Perkara", "Air mazi", "Air mani", "Air wadi"], [
             ["Rupa", "Jernih, licin, sedikit", "Pekat (lelaki); cair kekuningan (perempuan)", "Putih keruh dan pekat"],
             ["Bila keluar", "Ketika syahwat mula bangkit, bergurau atau berkhayal", "Ketika syahwat memuncak, bersama rasa lazat", "Selepas kencing atau mengangkat barang berat"],
             ["Cara keluar", "Meleleh, tidak memancut", "Memancut (lelaki), diikuti lemah badan", "Meleleh"],
             ["Bau", "Tiada bau khusus", "Seperti mayang kurma atau adunan tepung ketika basah", "Seperti air kencing"],
             ["Hukum zat", "Najis mutawassitah", "Suci (mazhab Syafi'i)", "Najis mutawassitah"],
             ["Kesan pada wuduk", "Batal", "Batal", "Batal"],
             ["Mandi wajib", "Tidak wajib", "Wajib", "Tidak wajib"],
             ["Puasa", "Tidak batal (muktamad Syafi'i)", "Batal jika keluar kerana sentuhan atau perbuatan sengaja; tidak batal jika mimpi", "Tidak batal"]])),
        ("mazi", "Air Mazi: Hukum dan Cara Membersihkannya",
         "<p>Ali bin Abi Talib RA berkata dia seorang yang kerap keluar mazi, lalu meminta Al-Miqdad bertanya kepada Nabi SAW. Baginda bersabda: <strong>“Hendaklah dia membasuh kemaluannya dan berwuduk”</strong>"
         + ref("HR Al-Bukhari, no. 269; Muslim, no. 303") + ". Daripada hadis ini ulama mengambil tiga hukum:</p>"
         + ul("Mazi <strong>najis</strong>, maka kemaluan dan pakaian yang terkena wajib dibasuh dengan air sehingga hilang kesannya.",
              "Mazi <strong>membatalkan wuduk</strong>, maka perlu berwuduk semula sebelum solat.",
              "Mazi <strong>tidak mewajibkan mandi</strong>, kerana Nabi SAW hanya menyuruh berwuduk.")
         + "<p>Dalam mazhab Syafi'i, pakaian yang terkena mazi wajib <strong>dibasuh</strong>, bukan sekadar direnjis. Hukum ini sama bagi lelaki dan perempuan. Wanita juga mengeluarkan mazi ketika syahwat, dan ia berbeza daripada keputihan biasa.</p>"),
        ("mani", "Air Mani: Tanda-Tanda dan Kewajipan Mandi",
         "<p>Menurut mazhab Syafi'i, cecair dianggap mani jika ada <strong>salah satu</strong> daripada tiga tanda: keluar memancut, disertai rasa lazat, atau berbau seperti adunan tepung ketika basah. Ummu Sulaim bertanya adakah wanita wajib mandi jika bermimpi, "
         "Baginda menjawab: <strong>“Ya, apabila dia melihat air”</strong>" + ref("HR Al-Bukhari, no. 282; Muslim, no. 313") + ".</p>"
         + ul("Mani <strong>suci</strong> dalam mazhab Syafi'i, tetapi disunatkan membasuh kesannya pada pakaian" + ref("HR Muslim, no. 288: Aisyah RA mengikis kesan mani daripada pakaian Nabi SAW"),
              "Keluar mani dengan apa jua sebab mewajibkan <strong>mandi wajib</strong>.",
              "Jika ragu sama ada mani atau mazi, ulama Syafi'i memberi pilihan: anggap mani lalu mandi, atau anggap mazi lalu basuh dan berwuduk. Mandi lebih berhati-hati.")
         + f'<p>Cara mandi wajib yang betul: <a href="{MANDI}">Cara Mandi Wajib, Niat & Rukun</a>.</p>'),
        ("wadi", "Air Wadi",
         "<p>Wadi ialah cecair putih pekat yang keluar selepas kencing atau ketika badan letih. Ibn Abbas RA berkata: mani mewajibkan mandi, manakala mazi dan wadi hanya perlu dibasuh kemaluan dan berwuduk"
         + ref("riwayat Al-Baihaqi, As-Sunan Al-Kubra") + ". Ia najis dan membatalkan wuduk, sama seperti air kencing.</p>"),
        ("puasa", "Air Mazi dan Puasa",
         "<p>Pendapat muktamad mazhab Syafi'i: <strong>keluar mazi tidak membatalkan puasa</strong>, sama ada lelaki atau perempuan, walaupun kerana bercumbu. Namun bercumbu hingga dikhuatiri keluar mani adalah haram ketika berpuasa. "
         "Yang membatalkan puasa ialah keluar <strong>mani</strong> dengan sebab sentuhan atau perbuatan sengaja; mimpi basah tidak membatalkan puasa.</p>"
         + f'<p>Senarai penuh: <a href="{PUASA}">Perkara yang Membatalkan Puasa</a>.</p>'),
        ("was", "Jika Selalu Keluar Mazi atau Was-Was",
         ul("Basuh kemaluan selepas kencing dan jangan terlalu lama memeriksa; was-was itu daripada syaitan.",
            "Jika mazi keluar berterusan tanpa kawalan, hukumnya seperti salisul baul: basuh, balut, berwuduk selepas masuk waktu dan solat segera.",
            "Jika keluar terlalu kerap tanpa sebab syahwat, rujuk doktor kerana ia mungkin tanda jangkitan atau masalah prostat."))
    ],
    faq=[("Apakah itu air mazi?", "Cecair jernih dan licin yang keluar ketika syahwat mula bangkit, tanpa memancut dan tanpa rasa lazat yang memuncak. Ia keluar daripada lelaki dan perempuan."),
         ("Adakah keluar air mazi wajib mandi wajib?", "Tidak. Cukup basuh kemaluan dan bahagian yang terkena, kemudian berwuduk (HR Al-Bukhari 269; Muslim 303)."),
         ("Adakah air mazi najis?", "Ya, najis mutawassitah. Pakaian yang terkena wajib dibasuh dalam mazhab Syafi'i."),
         ("Adakah keluar air mazi membatalkan puasa?", "Tidak, menurut pendapat muktamad mazhab Syafi'i. Yang membatalkan puasa ialah keluar mani kerana sentuhan atau perbuatan sengaja."),
         ("Apakah beza air mazi dan air mani?", "Mani keluar memancut bersama rasa lazat dan mewajibkan mandi; mazi meleleh tanpa rasa lazat yang memuncak dan hanya membatalkan wuduk."),
         ("Bagaimana dengan air mazi perempuan?", "Hukumnya sama dengan lelaki: najis, membatalkan wuduk dan tidak mewajibkan mandi. Keputihan biasa pula ialah lendir faraj (rutubah) yang hukumnya berbeza.")],
    refs=["Sahih Al-Bukhari, no. 269, 282.", "Sahih Muslim, no. 288, 303, 313.", "Al-Baihaqi, As-Sunan Al-Kubra, bab mazi dan wadi.",
          "An-Nawawi, Al-Majmu' Syarh Al-Muhadzdzab, bab mandi dan najis.", "Al-Khatib Asy-Syirbini, Mughni Al-Muhtaj, bab puasa."],
    disclaimer="Panduan fiqh mengikut mazhab Syafi'i. Untuk keadaan perubatan seperti lelehan berterusan, rujuk doktor dan pejabat agama Islam negeri anda.",
    related=[(MANDI, "Cara Mandi Wajib", "Niat, rukun dan langkah demi langkah"), (PUASA, "Perkara yang Membatalkan Puasa", "Senarai lengkap menurut mazhab Syafi'i"),
             (Q + "belajar-solat/", "Belajar Solat", "Panduan solat dengan bacaan")])))

# 2 ---------------------------------------------------------------- Bismillah 5 (60,500/mo, SD 20)
P = "ilmx-b5"
B5 = [("بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيمِ", "Bismillahir-rahmanir-rahim", "Dengan nama Allah Yang Maha Pemurah lagi Maha Penyayang", "Ayat Al-Quran (Al-Fatihah 1:1; An-Naml 27:30)", "✅ Al-Quran"),
      ("بِسْمِ اللّٰهِ الشَّافِي", "Bismillahis-syafi", "Dengan nama Allah Yang Maha Menyembuhkan", "Asy-Syafi ialah nama Allah dalam doa Nabi SAW (HR Al-Bukhari, no. 5743); susunan “bismillah” ini amalan ulama", "Amalan ulama"),
      ("بِسْمِ اللّٰهِ الْكَافِي", "Bismillahil-kafi", "Dengan nama Allah Yang Maha Mencukupi", "Maknanya daripada Az-Zumar 39:36 (“Bukankah Allah mencukupi hamba-Nya?”); susunan ini amalan ulama", "Amalan ulama"),
      ("بِسْمِ اللّٰهِ الْمُعَافِي", "Bismillahil-mu'afi", "Dengan nama Allah Yang Memberi afiat (kesejahteraan)", "Amalan ulama; maknanya selari dengan doa memohon afiat (HR Abu Daud, no. 5074)", "Amalan ulama"),
      ("بِسْمِ اللّٰهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ",
       "Bismillahil-lazi la yadhurru ma'asmihi syai'un fil-ardhi wa la fis-sama'i wa huwas-sami'ul-'alim",
       "Dengan nama Allah yang bersama nama-Nya tiada sesuatu pun di bumi dan di langit dapat memberi mudarat, dan Dialah Yang Maha Mendengar lagi Maha Mengetahui",
       "HR Abu Daud, no. 5088; At-Tirmizi, no. 3388 (hasan sahih): dibaca 3 kali pagi dan petang, tiada sesuatu pun memudaratkannya", SAHIH)]
POSTS.append(("bismillah-5", b4(
    ns=P, url=U["bismillah-5"], published="2020-04-09", pubms="9 April 2020",
    title="Bismillah 5 Rumi, Jawi & Maksud: Bacaan, Kelebihan & Statusnya",
    desc="Bacaan Bismillah 5 dalam tulisan Arab (jawi), rumi dan maksud setiap baris, status setiap lafaz, kelebihan yang sahih dan cara mengamalkannya tanpa khurafat.",
    h1="Bismillah 5: Bacaan Rumi, Jawi & Maksud",
    img=img("bismillah-5", "Zikir & Doa", "Bismillah 5", "Rumi, jawi, maksud & status setiap baris", "بِسْمِ اللّٰهِ الشَّافِي"),
    alt="Bacaan Bismillah 5 rumi, jawi dan maksud", refshort="Sunan Abu Daud, Sunan At-Tirmizi, Sahih Al-Bukhari",
    lead="Lima baris Bismillah yang diamalkan di Malaysia, setiap satu dengan teks Arab, rumi, maksud dan status sumbernya, supaya anda mengamalkannya dengan ilmu.",
    crumb=("Doa", W + "search/label/Doa"), about=["Bismillah 5", "Zikir pendinding"],
    answer="Bismillah 5 ialah lima baris: <strong>Bismillahir-rahmanir-rahim, Bismillahis-syafi, Bismillahil-kafi, Bismillahil-mu'afi</strong>, dan <strong>Bismillahil-lazi la yadhurru ma'asmihi syai'un fil-ardhi wa la fis-sama'i wa huwas-sami'ul-'alim</strong>. "
           "Baris kelima ialah <strong>hadis sahih</strong>: sesiapa membacanya 3 kali pagi dan petang, tiada sesuatu pun memudaratkannya <em>(HR Abu Daud, no. 5088; At-Tirmizi, no. 3388)</em>. Susunan lima baris itu sendiri ialah <strong>amalan ulama</strong>, bukan hadis, dan dakwaan ia diajar oleh Nabi Khidir tiada sumber yang sahih.",
    sections=[
        ("bacaan", "Bacaan Bismillah 5: Arab, Rumi dan Maksud",
         "".join(dc(P, f"Baris {i}", ar, ru + ".", mn + ".", src) for i, (ar, ru, mn, src, _) in enumerate(B5, 1))
         + "<p>Tulisan jawi bagi bacaan Al-Quran dan doa ialah tulisan Arab di atas. Rumi hanyalah alat bantu sebutan.</p>"),
        ("status", "Status Setiap Baris",
         grade([(f"Baris {i}: {ru[:40]}{'…' if len(ru) > 40 else ''}", src, st) for i, (ar, ru, mn, src, st) in enumerate(B5, 1)], head="Lafaz")
         + f'<div class="{P}-box amber">Senarai “khasiat” Bismillah 5 yang tersebar di media sosial, seperti menawar bisa ular, mengubati meroyan atau semua penyakit, <strong>tiada sumber hadis</strong>. Ia boleh dibaca sebagai doa dan zikir, '
           "tetapi jangan diyakini ada kesan pasti atau menggantikan rawatan perubatan.</div>"),
        ("kelebihan", "Kelebihan yang Sahih",
         ul("Baris 5: <strong>tiada sesuatu pun memudaratkan</strong> orang yang membacanya 3 kali pada waktu pagi dan petang" + ref("HR Abu Daud, no. 5088; At-Tirmizi, no. 3388"),
            "Rawi hadis, Aban bin Uthman, terkena lumpuh sebelah badan. Apabila ditanya, dia berkata pada hari itu dia terlupa membacanya" + ref("HR At-Tirmizi, no. 3388"),
            "Baris 1: setiap urusan penting dimulakan dengan basmalah, dan ia ayat Al-Quran.",
            "Baris 2–4 ialah tawassul dengan sifat Allah Yang Menyembuhkan, Mencukupi dan Memberi afiat; doa dengan nama dan sifat Allah disuruh dalam Al-A'raf 7:180."),
         ),
        ("amal", "Cara Mengamalkan Bismillah 5",
         ul("Baca 3 kali selepas Subuh dan selepas Asar atau Maghrib, bersama zikir pagi dan petang yang lain.",
            "Ketika sakit, baca sambil meletakkan tangan di tempat sakit. Rasulullah SAW mengajar: letakkan tangan pada tempat yang sakit, baca “Bismillah” 3 kali dan “A'udzu bi'izzatillahi wa qudratihi min syarri ma ajidu wa uhadzir” 7 kali" + ref("HR Muslim, no. 2202"),
            "Tiada bilangan khas 7, 41 atau 100 kali dalam hadis; bilangan seperti itu ijazah guru dan tidak wajib diikuti.",
            "Teruskan rawatan doktor. Doa dan ubat berjalan seiring.")
         + f'<p>Zikir lengkap dengan kaunter: <a href="{Q}zikir-pagi-petang/">Zikir Pagi Petang</a>. Lihat juga <a href="{Q}doa-orang-sakit/">Doa Orang Sakit</a>.</p>'),
        ("enam", "Bismillah 6 dan Bismillah 7",
         "<p>Versi “Bismillah 6” dan “Bismillah 7” menambah lafaz lain kepada senarai yang sama. Kedudukannya serupa: baris yang datang daripada Al-Quran dan hadis sahih kekal sahih, manakala susunan dan bilangannya ialah amalan, bukan sunnah yang ditetapkan. "
         "Artikel lama kami tentang Bismillah 6 telah digabungkan ke halaman ini.</p>"),
    ],
    faq=[("Apakah bacaan Bismillah 5?", "Bismillahir-rahmanir-rahim; Bismillahis-syafi; Bismillahil-kafi; Bismillahil-mu'afi; Bismillahil-lazi la yadhurru ma'asmihi syai'un fil-ardhi wa la fis-sama'i wa huwas-sami'ul-'alim."),
         ("Apakah maksud Bismillah 5?", "Dengan nama Allah Yang Maha Pemurah lagi Maha Penyayang; Yang Menyembuhkan; Yang Mencukupi; Yang Memberi afiat; dan dengan nama Allah yang bersama nama-Nya tiada sesuatu pun di bumi dan di langit dapat memberi mudarat."),
         ("Adakah Bismillah 5 daripada hadis?", "Baris kelima ialah hadis sahih (Abu Daud 5088; At-Tirmizi 3388). Susunan lima baris ialah amalan ulama, dan dakwaan ia diajar Nabi Khidir tiada sumber yang sahih."),
         ("Berapa kali Bismillah 5 perlu dibaca?", "Hadis baris kelima menyebut 3 kali pagi dan petang. Bilangan lain ialah ijazah guru, bukan ketetapan hadis."),
         ("Bolehkah Bismillah 5 dijadikan penawar penyakit?", "Boleh dibaca sebagai doa memohon kesembuhan, tetapi jangan diyakini memberi kesan pasti atau meninggalkan rawatan perubatan.")],
    refs=["Sunan Abu Daud, no. 5074, 5088; Sunan At-Tirmizi, no. 3388.", "Sahih Al-Bukhari, no. 5743; Sahih Muslim, no. 2202.", "Al-Quran: Al-Fatihah 1:1; Az-Zumar 39:36; Al-A'raf 7:180."],
    related=[(Q + "zikir-pagi-petang/", "Zikir Pagi Petang", "Zikir pendinding dengan kaunter"), (Q + "doa-orang-sakit/", "Doa Orang Sakit", "Doa sahih ketika sakit"),
             (W + "2020/02/tanda-tanda-gangguan-jin-sihir.html", "Ruqyah Syar'iyyah", "Rawatan yang menepati syarak")])))

# 3 ---------------------------------------------------------------- Tanggungjawab suami (1,900/mo, SD 14)
P = "ilmx-ts"
POSTS.append(("tanggungjawab-suami", b4(
    ns=P, url=U["tanggungjawab-suami"], published="2018-02-01", pubms="1 Februari 2018",
    title="Tanggungjawab Suami Dalam Islam: 10 Kewajipan & Dosa Suami",
    desc="Tanggungjawab suami terhadap isteri dan keluarga dalam Islam: nafkah, layanan baik, didikan agama, perlindungan, dan dosa suami yang mengabaikannya.",
    h1="Tanggungjawab Suami Dalam Islam",
    img=img("tanggungjawab-suami", "Rumah Tangga", "Tanggungjawab Suami", "10 kewajipan & dosa suami menurut dalil", "قَوَّامُونَ"),
    alt="Tanggungjawab suami terhadap isteri dalam Islam", refshort="Al-Quran, Sahih Al-Bukhari, Sahih Muslim, Sunan Abu Daud",
    lead="Sepuluh tanggungjawab suami menurut Al-Quran dan hadis sahih, apa yang berlaku jika ia diabaikan, dan hak isteri di bawah undang-undang keluarga Islam di Malaysia.",
    crumb=("Keluarga", W + "search/label/Keluarga"), about=["Tanggungjawab suami", "Nafkah", "Rumah tangga Islam"],
    answer="Suami ialah <strong>pemimpin (qawwam)</strong> keluarga <em>(An-Nisa' 4:34)</em> dan bertanggungjawab ke atas <strong>nafkah</strong> isteri dan anak (makanan, pakaian, tempat tinggal), <strong>layanan yang baik</strong> <em>(An-Nisa' 4:19)</em>, "
           "<strong>didikan agama</strong> keluarga <em>(At-Tahrim 66:6)</em> dan perlindungan. Nabi SAW bersabda: <strong>“Sebaik-baik kamu ialah yang terbaik terhadap keluarganya”</strong> <em>(HR At-Tirmizi, no. 3895)</em>, "
           "dan <strong>cukuplah seseorang berdosa apabila dia mensia-siakan orang yang wajib ditanggungnya</strong> <em>(HR Abu Daud, no. 1692)</em>.",
    sections=[
        ("ayat", "Asas Tanggungjawab Suami dalam Al-Quran", qcard(P, "An-Nisa' 4:34", 4, 34, 34, "Surah An-Nisa', ayat 34")
         + "<p>Kepimpinan (qiwamah) dalam ayat ini dikaitkan dengan <strong>nafkah</strong> yang diberikan. Ulama menjelaskan ia amanah untuk menjaga, bukan kuasa untuk menindas.</p>"),
        ("sepuluh", "10 Tanggungjawab Suami terhadap Isteri dan Keluarga",
         table(["#", "Tanggungjawab", "Dalil"], [
             ["1", "Memberi nafkah zahir: makanan, pakaian dan tempat tinggal mengikut kemampuan", "Al-Baqarah 2:233; At-Talaq 65:7"],
             ["2", "Membayar mahar dengan penuh kerelaan", "An-Nisa' 4:4"],
             ["3", "Bergaul dengan isteri secara baik (ma'ruf)", "An-Nisa' 4:19"],
             ["4", "Mendidik keluarga tentang agama dan menyuruh solat", "At-Tahrim 66:6; Taha 20:132"],
             ["5", "Tidak memukul muka, tidak menghina dan tidak memburuk-burukkan isteri", "HR Abu Daud, no. 2142"],
             ["6", "Memenuhi nafkah batin dan menjaga maruah isteri", "An-Nisa' 4:19; HR Muslim, no. 1006"],
             ["7", "Berlaku adil jika berpoligami", "An-Nisa' 4:3; HR Abu Daud, no. 2133"],
             ["8", "Membantu urusan rumah, seperti yang dilakukan Rasulullah SAW", "HR Al-Bukhari, no. 676"],
             ["9", "Bermesyuarat dan berlembut dalam membuat keputusan", "Al-Baqarah 2:233; Ali 'Imran 3:159"],
             ["10", "Menjaga keluarga daripada maksiat dan perkara yang merosakkan", "At-Tahrim 66:6; HR Al-Bukhari, no. 893"]])),
        ("nafkah", "Nafkah: Pahala Paling Besar",
         "<p>Nabi SAW bersabda: “Satu dinar yang kamu belanjakan di jalan Allah, satu dinar untuk memerdekakan hamba, satu dinar yang kamu sedekahkan kepada orang miskin dan satu dinar yang kamu belanjakan untuk keluargamu: "
         "<strong>yang paling besar pahalanya ialah yang kamu belanjakan untuk keluargamu</strong>”" + ref("HR Muslim, no. 995") + ". Malah suapan makanan ke mulut isteri pun berpahala" + ref("HR Al-Bukhari, no. 56") + ".</p>"
         "<p>Di Malaysia, nafkah isteri dan anak ialah hak di bawah Akta (dan Enakmen negeri) Undang-Undang Keluarga Islam. Isteri boleh menuntut nafkah yang tidak dibayar di Mahkamah Syariah, dan Bahagian Sokongan Keluarga (BSK) JKSM membantu penguatkuasaan perintah nafkah.</p>"),
        ("dosa", "Dosa Suami yang Mengabaikan Tanggungjawab",
         grade([("Cukuplah seseorang berdosa apabila dia mensia-siakan orang yang wajib ditanggungnya", "HR Abu Daud, no. 1692; Muslim, no. 996 dengan lafaz “menahan makanan”", SAHIH),
                ("Setiap kamu pemimpin dan akan ditanya tentang orang yang dipimpinnya; lelaki pemimpin bagi keluarganya", "HR Al-Bukhari, no. 893; Muslim, no. 1829", SAHIH),
                ("Dayus (suami yang membiarkan maksiat dalam keluarganya) tidak dipandang Allah pada hari kiamat", "HR An-Nasa'i, no. 2562", HASAN),
                ("Isteri tidak wajib taat kepada suami dalam perkara maksiat", "HR Al-Bukhari, no. 7257; Muslim, no. 1840", SAHIH)], head="Peringatan")
         + "<p>Kisah-kisah tentang dosa suami yang ditanggung isteri, seperti cerita pengisi air yang tersebar dalam artikel lama ini, tidak mempunyai sumber yang sahih dan telah dibuang. "
           "Prinsip Al-Quran jelas: <strong>setiap orang menanggung dosanya sendiri</strong>" + ref("Al-An'am 6:164") + ".</p>"),
        ("bantuan", "Jika Hak Isteri Diabaikan",
         ul("Bincang dengan baik dan dapatkan bantuan keluarga yang dipercayai sebagai orang tengah" + ref("An-Nisa' 4:35"),
            "Dapatkan khidmat kaunseling di Pejabat Agama Islam Daerah atau Jabatan Agama Islam negeri.",
            "Tuntutan nafkah dan perlindungan boleh dibuat di Mahkamah Syariah.",
            "Jika berlaku keganasan rumah tangga, hubungi Talian Kasih 15999 atau polis 999.")
         + f'<p>Doa untuk rumah tangga: <a href="{DOA_SUAMI}">Doa Suami Berubah Sikap & Lembutkan Hati</a>.</p>'),
    ],
    faq=[("Apakah tanggungjawab suami dalam Islam?", "Memberi nafkah zahir dan batin, bergaul dengan baik, mendidik keluarga tentang agama, melindungi keluarga dan berlaku adil (An-Nisa' 4:19, 4:34; At-Tahrim 66:6)."),
         ("Apakah nafkah yang wajib diberi suami?", "Makanan, pakaian dan tempat tinggal mengikut kemampuan suami dan keperluan isteri (Al-Baqarah 2:233; At-Talaq 65:7)."),
         ("Apakah dosa suami yang tidak memberi nafkah?", "Nabi SAW bersabda cukuplah seseorang berdosa apabila dia mensia-siakan orang yang wajib ditanggungnya (HR Abu Daud 1692). Isteri juga boleh menuntut nafkah di Mahkamah Syariah."),
         ("Adakah dosa suami ditanggung isteri?", "Tidak. Setiap orang menanggung dosanya sendiri (Al-An'am 6:164). Namun isteri tidak boleh mentaati suami dalam perkara maksiat."),
         ("Apakah tanggungjawab suami terhadap anak?", "Memberi nafkah, mendidik agama dan akhlak, menyuruh solat sejak 7 tahun (HR Abu Daud 495) dan melindungi mereka daripada perkara yang merosakkan.")],
    refs=["Al-Quran: An-Nisa' 4:3, 4:4, 4:19, 4:34, 4:35; Al-Baqarah 2:233; At-Talaq 65:7; At-Tahrim 66:6; Taha 20:132; Al-An'am 6:164; Ali 'Imran 3:159.",
          "Sahih Al-Bukhari, no. 56, 676, 893, 7257.", "Sahih Muslim, no. 995, 996, 1006, 1829, 1840.", "Sunan Abu Daud, no. 495, 1692, 2133, 2142; Sunan At-Tirmizi, no. 3895; Sunan An-Nasa'i, no. 2562."],
    disclaimer="Untuk tuntutan nafkah, perceraian dan perlindungan, dapatkan nasihat Pejabat Agama Islam atau peguam syarie. Maklumat undang-undang di atas bersifat umum.",
    related=[(DOA_SUAMI, "Doa Suami Berubah Sikap", "Doa melembutkan hati dalam rumah tangga"), (U["akidah-anak"], "Cara Menanam Akidah Pada Anak", "Panduan ibu bapa ikut umur"),
             (TERANIAYA, "Doa Orang Teraniaya", "Hadis dan bacaan doa ketika dizalimi")])))

# 4 ---------------------------------------------------------------- Sunnah Nabi (880/mo, SD 13)
P = "ilmx-sn"
POSTS.append(("sunnah-nabi", b4(
    ns=P, url=U["sunnah-nabi"], published="2020-07-14", pubms="14 Julai 2020",
    title="Sunnah Nabi Muhammad SAW: 15 Amalan Harian Mudah (Hadis Sahih)",
    desc="15 sunnah Nabi Muhammad SAW yang mudah diamalkan setiap hari: bangun tidur, makan dan minum, keluar rumah, bergaul dan sunnah sebelum tidur, dengan hadis sahih.",
    h1="15 Sunnah Nabi Muhammad SAW Setiap Hari",
    img=img("sunnah-nabi", "Amalan Harian", "Sunnah Nabi Muhammad SAW", "15 amalan harian mudah, hadis sahih", "سُنَّةُ النَّبِيِّ"),
    alt="Sunnah Nabi Muhammad SAW yang mudah diamalkan", refshort="Sahih Al-Bukhari, Sahih Muslim",
    lead="Lima belas sunnah yang boleh dimulakan hari ini, disusun mengikut waktu dari bangun tidur hingga tidur semula, setiap satu dengan hadis sahih.",
    crumb=("Amalan", W + "search/label/Amalan"), about=["Sunnah Nabi", "Amalan harian"],
    answer="Antara sunnah Nabi Muhammad SAW yang paling mudah diamalkan setiap hari ialah <strong>bersiwak</strong> <em>(HR Al-Bukhari, no. 887)</em>, <strong>mendahulukan kanan</strong> <em>(HR Al-Bukhari, no. 168)</em>, "
           "<strong>makan dengan tangan kanan dan membaca bismillah</strong> <em>(HR Al-Bukhari, no. 5376)</em>, <strong>memberi salam</strong> <em>(HR Muslim, no. 54)</em>, <strong>tersenyum</strong> <em>(HR At-Tirmizi, no. 1956)</em> "
           "dan <strong>tidur dalam keadaan berwuduk sambil mengiring ke kanan</strong> <em>(HR Al-Bukhari, no. 247)</em>.",
    sections=[
        ("pagi", "Sunnah Pagi: Bangun Tidur hingga Keluar Rumah",
         table(["#", "Sunnah", "Dalil"], [
             ["1", "Membaca doa bangun tidur: “Alhamdulillahil-lazi ahyana ba'da ma amatana wa ilaihin-nusyur”", "HR Al-Bukhari, no. 6312"],
             ["2", "Bersiwak, terutama ketika bangun dan sebelum solat", "HR Al-Bukhari, no. 245, 887"],
             ["3", "Solat sunat 2 rakaat sebelum Subuh: lebih baik daripada dunia dan isinya", "HR Muslim, no. 725"],
             ["4", "Mendahulukan kanan ketika memakai kasut dan pakaian", "HR Al-Bukhari, no. 168"],
             ["5", "Membaca doa keluar rumah: “Bismillahi tawakkaltu 'alallah, la hawla wa la quwwata illa billah”", "HR Abu Daud, no. 5095; At-Tirmizi, no. 3426"]])
         + f'<p>Bacaan lengkap: <a href="{Q}doa-bangun-tidur/">Doa Bangun Tidur</a> dan <a href="{Q}doa-keluar-rumah/">Doa Keluar Rumah</a>.</p>'),
        ("siang", "Sunnah Siang: Makan, Minum dan Bergaul",
         table(["#", "Sunnah", "Dalil"], [
             ["6", "Membaca bismillah, makan dengan tangan kanan dan makan yang terdekat", "HR Al-Bukhari, no. 5376; Muslim, no. 2022"],
             ["7", "Minum sambil duduk dan bernafas di luar bekas, tiga kali", "HR Muslim, no. 2024, 2028"],
             ["8", "Menjilat jari dan membersihkan pinggan selepas makan", "HR Muslim, no. 2033"],
             ["9", "Memberi salam kepada yang dikenali dan tidak dikenali", "HR Al-Bukhari, no. 12; Muslim, no. 54"],
             ["10", "Tersenyum kepada saudara: ia sedekah", "HR At-Tirmizi, no. 1956"],
             ["11", "Menjaga lidah: berkata baik atau diam", "HR Al-Bukhari, no. 6018"]])),
        ("malam", "Sunnah Sebelum Tidur",
         table(["#", "Sunnah", "Dalil"], [
             ["12", "Berwuduk sebelum tidur dan berbaring di atas rusuk kanan", "HR Al-Bukhari, no. 247"],
             ["13", "Membaca Al-Ikhlas, Al-Falaq dan An-Nas, meniup ke tapak tangan dan menyapu badan, 3 kali", "HR Al-Bukhari, no. 5017"],
             ["14", "Membaca Ayat Kursi: dijaga Allah dan syaitan tidak mendekat hingga pagi", "HR Al-Bukhari, no. 2311"],
             ["15", "Bertasbih 33, bertahmid 33 dan bertakbir 34 kali", "HR Al-Bukhari, no. 3705; Muslim, no. 2727"]])
         + "<p>Tiada hadis yang menetapkan berapa jam Nabi SAW tidur. Yang thabit, Baginda tidur awal selepas Isyak dan bangun pada sepertiga malam terakhir untuk solat" + ref("HR Al-Bukhari, no. 1146") + ".</p>"
         + f'<p>Doa tidur lengkap: <a href="{Q}doa-sebelum-tidur/">Doa Sebelum Tidur</a>.</p>'),
        ("mingguan", "Sunnah Mingguan dan Bulanan",
         ul("Puasa Isnin dan Khamis" + ref("HR At-Tirmizi, no. 747"), "Puasa tiga hari setiap bulan (13, 14, 15 Hijrah)" + ref("HR An-Nasa'i, no. 2420"),
            "Memotong kuku, mencukur bulu ketiak dan bulu ari-ari, tidak melebihi 40 hari" + ref("HR Muslim, no. 258"),
            "Mandi, memakai wangian dan membaca Al-Kahfi pada hari Jumaat" + ref("HR Al-Bukhari, no. 880"))
         + f'<p>Sunnah fitrah secara terperinci: <a href="{U["sunnah-fitrah"]}">Sunnah Fitrah: Potong Kuku & Mencukur</a>.</p>'),
        ("mula", "Cara Mula Menghidupkan Sunnah",
         "<p>Pilih <strong>satu sunnah setiap minggu</strong> dan ulangi sehingga menjadi tabiat. Nabi SAW bersabda: “Amalan yang paling disukai Allah ialah yang berterusan walaupun sedikit”"
         + ref("HR Al-Bukhari, no. 6464; Muslim, no. 783") + ". Sesiapa yang menghidupkan sunnah yang baik, dia mendapat pahalanya dan pahala orang yang mengikutinya" + ref("HR Muslim, no. 1017") + ".</p>"),
    ],
    faq=[("Apakah sunnah Nabi yang mudah diamalkan?", "Bersiwak, mendahulukan kanan, makan dengan tangan kanan dan membaca bismillah, memberi salam, tersenyum dan tidur dalam keadaan berwuduk (HR Al-Bukhari 168, 247, 887, 5376; Muslim 54)."),
         ("Apakah sunnah Nabi sebelum tidur?", "Berwuduk, berbaring di atas rusuk kanan, membaca tiga Qul dan menyapu badan, Ayat Kursi, serta tasbih 33, tahmid 33 dan takbir 34 (HR Al-Bukhari 247, 2311, 3705, 5017)."),
         ("Berapa jam Nabi Muhammad tidur?", "Tiada hadis yang menetapkan bilangan jam. Baginda tidur awal selepas Isyak dan bangun pada sepertiga malam terakhir (HR Al-Bukhari 1146)."),
         ("Apakah pahala menghidupkan sunnah?", "Pahala amalan itu dan pahala orang yang mengikutinya tanpa dikurangkan (HR Muslim 1017).")],
    refs=["Sahih Al-Bukhari, no. 12, 168, 245, 247, 880, 887, 1146, 2311, 3705, 5017, 5376, 6018, 6312, 6464.", "Sahih Muslim, no. 54, 258, 725, 783, 1017, 2022, 2024, 2028, 2033, 2727.",
          "Sunan Abu Daud, no. 5095; Sunan At-Tirmizi, no. 747, 1956, 3426; Sunan An-Nasa'i, no. 2420."],
    related=[(Q + "doa-harian/", "Doa Harian", "Himpunan doa harian dengan rujukan"), (U["sunnah-fitrah"], "Sunnah Fitrah", "Potong kuku, mencukur dan tempohnya"),
             (U["amalan-pahala-besar"], "Amalan Ringan Pahala Besar", "Zikir dan amalan seminit")])))

# 5 ---------------------------------------------------------------- Sunnah fitrah (hukum cukur bulu kemaluan, potong kuku ikut sunnah 390/mo)
P = "ilmx-sf"
POSTS.append(("sunnah-fitrah", b4(
    ns=P, url=U["sunnah-fitrah"], published="2020-02-06", pubms="6 Februari 2020",
    title="Sunnah Fitrah: Hukum Mencukur Bulu Ari-Ari, Potong Kuku & Tempoh",
    desc="5 sunnah fitrah: berkhatan, mencukur bulu ari-ari, memotong kuku, mencabut bulu ketiak dan memendekkan misai. Hukum, cara ikut sunnah dan had 40 hari.",
    h1="Sunnah Fitrah: Hukum, Cara & Tempohnya",
    img=img("sunnah-fitrah", "Fiqh Kebersihan", "Sunnah Fitrah", "Hukum, cara ikut sunnah & had 40 hari", "خِصَالُ الْفِطْرَةِ"),
    alt="Lima sunnah fitrah dalam Islam", refshort="Sahih Al-Bukhari, Sahih Muslim",
    lead="Lima amalan kebersihan yang disebut Nabi SAW sebagai fitrah, hukum setiap satu dalam mazhab Syafi'i, cara yang disunatkan dan had masa 40 hari.",
    crumb=("Fiqh", W + "search/label/Fiqh"), about=["Sunnah fitrah", "Kebersihan diri"],
    answer="Nabi SAW bersabda: <strong>“Fitrah itu lima: berkhatan, mencukur bulu ari-ari, memendekkan misai, memotong kuku dan mencabut bulu ketiak”</strong> <em>(HR Al-Bukhari, no. 5889; Muslim, no. 257)</em>. "
           "Mencukur bulu ari-ari hukumnya <strong>sunat</strong>, dan Anas RA berkata had yang ditetapkan untuk memotong kuku, misai, bulu ketiak dan bulu ari-ari ialah <strong>tidak dibiarkan melebihi 40 hari</strong> <em>(HR Muslim, no. 258)</em>.",
    sections=[
        ("lima", "5 Sunnah Fitrah dan Hukumnya",
         table(["Amalan", "Hukum (mazhab Syafi'i)", "Nota"], [
             ["Berkhatan", "Wajib bagi lelaki dan perempuan menurut mazhab Syafi'i", "Bagi perempuan, sekadar memotong sedikit kulit tanpa mudarat; amalan memotong yang memudaratkan diharamkan"],
             ["Mencukur bulu ari-ari (istihdad)", "Sunat", "Boleh dicukur, digunting atau dibuang dengan krim"],
             ["Memendekkan misai", "Sunat", "Dipendekkan hingga nampak bibir atas" + ref("HR Al-Bukhari, no. 5892")],
             ["Memotong kuku", "Sunat", "Termasuk kuku kaki"],
             ["Mencabut bulu ketiak", "Sunat", "Mencabut lebih afdal; mencukur juga mencapai sunnah"]])),
        ("tempoh", "Had Masa 40 Hari",
         "<p>Anas bin Malik RA berkata: “Ditetapkan waktu untuk kami dalam memendekkan misai, memotong kuku, mencabut bulu ketiak dan mencukur bulu ari-ari, supaya tidak dibiarkan lebih daripada 40 malam”" + ref("HR Muslim, no. 258")
         + ". Ulama menjelaskan 40 hari ialah had maksimum; yang terbaik ialah apabila ia panjang, dan ramai mengamalkannya setiap minggu, terutama hari Jumaat.</p>"),
        ("kuku", "Cara Memotong Kuku Ikut Sunnah",
         ul("Mulakan dengan tangan kanan, kemudian kiri; begitu juga kaki. Ini berdasarkan hadis umum mendahulukan kanan" + ref("HR Al-Bukhari, no. 168"),
            "Urutan jari tertentu yang disebut sesetengah kitab ialah pandangan ulama, bukan hadis sahih; ia tidak wajib diikuti.",
            "Tiada hadis sahih yang menetapkan hari tertentu atau melarang memotong kuku pada malam hari.",
            "Menanam potongan kuku dan rambut ialah amalan ulama yang baik, bukan kewajipan.",
            "Bagi wanita yang haid atau orang yang berjunub, memotong kuku tidak haram. Pandangan yang melarangnya tidak bersandarkan dalil yang kuat."),
         ),
        ("ari", "Hukum Mencukur Bulu Ari-Ari",
         ul("Hukumnya sunat bagi lelaki dan perempuan, dan termasuk kebersihan yang dituntut Islam.",
            "Bahagian yang disunatkan ialah bulu di sekitar kemaluan.",
            "Boleh menggunakan pisau cukur, gunting atau krim penanggal bulu; yang penting bersih dan selamat.",
            "Isteri disunatkan menjaga kebersihan ini untuk suami, dan suami untuk isteri, sebagai sebahagian daripada pergaulan yang baik."),
         ),
        ("hikmah", "Hikmah Sunnah Fitrah",
         "<p>Allah menyukai orang yang menyucikan diri" + ref("Al-Baqarah 2:222") + ". Amalan fitrah mengurangkan bau, kuman dan jangkitan, memudahkan istinjak dan mandi wajib, serta membezakan penampilan seorang Muslim yang kemas.</p>"),
    ],
    faq=[("Apakah 5 sunnah fitrah?", "Berkhatan, mencukur bulu ari-ari, memendekkan misai, memotong kuku dan mencabut bulu ketiak (HR Al-Bukhari 5889; Muslim 257)."),
         ("Apakah hukum mencukur bulu ari-ari?", "Sunat bagi lelaki dan perempuan, dan tidak dibiarkan melebihi 40 hari (HR Muslim 258)."),
         ("Bagaimana cara memotong kuku ikut sunnah?", "Mulakan dengan kanan, kemudian kiri. Urutan jari tertentu ialah pandangan ulama, bukan hadis sahih, dan tiada hari khusus yang diwajibkan."),
         ("Bolehkah memotong kuku ketika haid?", "Boleh. Tiada dalil kuat yang melarang wanita haid atau orang berjunub memotong kuku."),
         ("Berapa lama had memotong kuku?", "Tidak melebihi 40 hari (HR Muslim 258). Lebih baik lebih kerap, contohnya setiap Jumaat.")],
    refs=["Sahih Al-Bukhari, no. 168, 5889, 5892.", "Sahih Muslim, no. 257, 258.", "Al-Quran: Al-Baqarah 2:222.", "An-Nawawi, Syarh Sahih Muslim, bab khisal al-fitrah."],
    related=[(U["sunnah-nabi"], "15 Sunnah Nabi Setiap Hari", "Amalan harian dengan hadis sahih"), (MANDI, "Cara Mandi Wajib", "Niat, rukun dan langkah"),
             (U["air-mazi"], "Air Mazi, Mani & Wadi", "Beza dan hukumnya")])))

# 6 ---------------------------------------------------------------- Sedekah jariah / pahala berterusan
P = "ilmx-sj"
POSTS.append(("sedekah-jariah", b4(
    ns=P, url=U["sedekah-jariah"], published="2020-01-13", pubms="13 Januari 2020",
    title="Sedekah Jariah & 7 Amalan Pahala Berterusan Selepas Mati (Hadis)",
    desc="Amalan yang pahalanya terus mengalir selepas mati: sedekah jariah, ilmu bermanfaat, anak soleh, wakaf Al-Quran, masjid dan telaga, dengan hadis dan contoh.",
    h1="Sedekah Jariah & Pahala Berterusan",
    img=img("sedekah-jariah", "Amalan", "Sedekah Jariah", "7 amalan pahala berterusan selepas mati", "صَدَقَةٌ جَارِيَةٌ"),
    alt="Sedekah jariah dan amalan pahala berterusan", refshort="Sahih Muslim, Sunan Ibn Majah",
    lead="Apa yang terus memberi pahala selepas kita meninggal dunia, menurut dua hadis utama, dan cara praktikal melakukannya di Malaysia hari ini.",
    crumb=("Amalan", W + "search/label/Amalan"), about=["Sedekah jariah", "Wakaf", "Pahala berterusan"],
    answer="Nabi SAW bersabda: apabila manusia mati, terputus amalannya kecuali tiga: <strong>sedekah jariah, ilmu yang dimanfaatkan dan anak soleh yang mendoakannya</strong> <em>(HR Muslim, no. 1631)</em>. "
           "Hadis Ibn Majah memperincikan tujuh: <strong>ilmu yang diajar, anak soleh, mushaf yang diwariskan, masjid yang dibina, rumah untuk musafir, sungai yang dialirkan dan sedekah semasa sihat</strong> <em>(HR Ibn Majah, no. 242; hasan)</em>.",
    sections=[
        ("tujuh", "7 Amalan yang Pahalanya Terus Mengalir",
         table(["Amalan", "Contoh hari ini"], [
             ["Ilmu yang diajar dan disebarkan", "Mengajar mengaji, berkongsi ilmu yang sahih, menulis buku atau artikel bermanfaat"],
             ["Anak soleh yang mendoakan", "Mendidik anak solat dan doa, termasuk doa untuk ibu bapa"],
             ["Mushaf yang diwariskan", "Wakaf Al-Quran ke masjid, sekolah tahfiz atau penjara"],
             ["Masjid yang dibina", "Menyumbang kepada pembinaan atau penyelenggaraan masjid dan surau"],
             ["Rumah untuk musafir", "Wakaf rumah transit pesakit atau asrama pelajar"],
             ["Sungai yang dialirkan", "Wakaf telaga, penapis air, atau projek air bersih"],
             ["Sedekah semasa sihat", "Sumbangan tetap bulanan, wakaf tunai melalui Majlis Agama Islam negeri"]])
         + "<p>Sumber: HR Ibn Majah, no. 242 (hasan), dan HR Muslim, no. 1631.</p>"),
        ("jariah", "Apa Itu Sedekah Jariah?",
         "<p>Sedekah jariah ialah sedekah yang manfaatnya <strong>berterusan</strong>, maka pahalanya juga berterusan selagi manfaat itu dinikmati. Contoh paling jelas ialah <strong>wakaf</strong>: Umar RA mewakafkan tanahnya di Khaibar, "
         "asalnya kekal dan hasilnya disedekahkan" + ref("HR Al-Bukhari, no. 2737; Muslim, no. 1632") + ".</p>"
         + f'<p>Asas sedekah, jenis dan bezanya dengan zakat: <a href="{SEDEKAH}">Apa Itu Sedekah</a>.</p>'),
        ("sunnah", "Pahala Memulakan Kebaikan",
         "<p>“Sesiapa yang memulakan dalam Islam satu sunnah yang baik, baginya pahala amalan itu dan pahala orang yang mengamalkannya selepasnya, tanpa dikurangkan sedikit pun daripada pahala mereka”" + ref("HR Muslim, no. 1017")
         + ". Ini termasuk mengajak orang lain bersolat, berkongsi ilmu yang sahih dan memulakan tabung amal.</p>"
         + f'<div class="{P}-box amber">Berkongsi kandungan agama juga boleh menjadi pahala berterusan, tetapi pastikan ia sahih. Menyebarkan hadis palsu pula boleh menjadi dosa yang berterusan.</div>'),
        ("si-mati", "Amalan untuk Ibu Bapa yang Telah Meninggal",
         ul("Doa anak: “Rabbighfir li wa liwalidayya” dan doa umum" + ref("HR Muslim, no. 1631"),
            "Bersedekah bagi pihak mereka; Nabi SAW membenarkan seorang anak bersedekah untuk ibunya" + ref("HR Al-Bukhari, no. 1388"),
            "Menunaikan haji atau umrah badal jika memenuhi syarat" + ref("HR Al-Bukhari, no. 1852"),
            "Membayar hutang mereka dan menyambung silaturahim dengan sahabat mereka" + ref("HR Muslim, no. 2552"))
         + f'<p>Bacaan tahlil dengan nama arwah: <a href="{Q}tahlil-ringkas/">Tahlil Ringkas</a>. Doa untuk ibu bapa: <a href="{Q}doa-untuk-ibu-bapa/">Doa Untuk Ibu Bapa</a>.</p>'),
        ("mula", "Cara Mula Bersedekah Jariah dengan Bajet Kecil",
         ul("Wakaf tunai serendah RM1 hingga RM10 melalui saluran rasmi Majlis Agama Islam negeri anda.",
            "Wakaf satu naskhah Al-Quran (sekitar RM20–RM40).", "Sumbangan bulanan tetap ke tabung masjid atau sekolah tahfiz.",
            "Ajar seorang anak membaca Al-Fatihah dengan betul: ilmu yang diajar juga jariah."))
    ],
    faq=[("Apakah amalan yang pahalanya berterusan selepas mati?", "Sedekah jariah, ilmu yang dimanfaatkan dan anak soleh yang mendoakan (HR Muslim 1631), serta mushaf, masjid, rumah musafir dan sungai yang dialirkan (HR Ibn Majah 242)."),
         ("Apakah contoh sedekah jariah?", "Wakaf tanah atau tunai, wakaf Al-Quran, sumbangan pembinaan masjid, telaga atau penapis air, dan apa-apa sumbangan yang manfaatnya berterusan."),
         ("Apakah beza sedekah jariah dan wakaf?", "Wakaf ialah bentuk sedekah jariah yang asal hartanya kekal dan hanya manfaatnya digunakan. Semua wakaf ialah sedekah jariah, tetapi tidak semua sedekah jariah berbentuk wakaf."),
         ("Bolehkah bersedekah bagi pihak ibu bapa yang telah meninggal?", "Boleh, dan pahalanya sampai kepada mereka (HR Al-Bukhari 1388).")],
    refs=["Sahih Muslim, no. 1017, 1631, 1632, 2552.", "Sahih Al-Bukhari, no. 1388, 1852, 2737.", "Sunan Ibn Majah, no. 242."],
    related=[(SEDEKAH, "Apa Itu Sedekah", "Maksud, jenis, kelebihan dan beza zakat"), (U["mengungkit"], "Hukum Mengungkit Sedekah", "Al-Baqarah 264 dan hadis"),
             (Q + "tahlil-ringkas/", "Tahlil Ringkas", "Bacaan tahlil dengan nama arwah")])))

# 7 ---------------------------------------------------------------- Amalan ringan pahala besar
P = "ilmx-ap"
POSTS.append(("amalan-pahala-besar", b4(
    ns=P, url=U["amalan-pahala-besar"], published="2020-02-16", pubms="16 Februari 2020",
    title="Amalan Ringan Pahala Besar: 10 Zikir & Amalan Seminit (Hadis Sahih)",
    desc="10 amalan dan zikir kurang seminit yang pahalanya besar, seperti Subhanallahi wa bihamdih 100 kali dan Al-Ikhlas, dengan hadis sahih setiap satu.",
    h1="10 Amalan Ringan, Pahala Besar",
    img=img("amalan-pahala-besar", "Zikir & Amalan", "Amalan Ringan Pahala Besar", "10 zikir dan amalan seminit, hadis sahih", "سُبْحَانَ اللّٰهِ وَبِحَمْدِهِ"),
    alt="Amalan ringan yang pahalanya besar menurut hadis sahih", refshort="Sahih Al-Bukhari, Sahih Muslim",
    lead="Sepuluh zikir dan amalan yang mengambil masa kurang seminit, setiap satu dengan ganjaran yang disebut dalam hadis sahih, untuk diisi dalam waktu menunggu harian.",
    crumb=("Zikir", W + "search/label/Zikir"), about=["Amalan pahala besar", "Zikir"],
    answer="Antara amalan paling ringan dengan pahala paling besar ialah <strong>“Subhanallahi wa bihamdih” 100 kali</strong>, yang menghapuskan dosa walaupun sebanyak buih di laut <em>(HR Al-Bukhari, no. 6405)</em>, "
           "<strong>membaca Al-Ikhlas</strong> yang menyamai sepertiga Al-Quran <em>(HR Al-Bukhari, no. 5013)</em>, dan <strong>berselawat sekali</strong> yang dibalas Allah dengan sepuluh rahmat <em>(HR Muslim, no. 408)</em>.",
    sections=[
        ("sepuluh", "10 Amalan Ringan dengan Pahala Besar",
         table(["#", "Amalan", "Ganjaran", "Dalil"], [
             ["1", "Subhanallahi wa bihamdih, 100 kali", "Dosa dihapuskan walaupun sebanyak buih di laut", "HR Al-Bukhari, no. 6405"],
             ["2", "Subhanallahi wa bihamdih, subhanallahil-'azim", "Ringan di lidah, berat di timbangan, dicintai Ar-Rahman", "HR Al-Bukhari, no. 6682"],
             ["3", "Membaca Al-Ikhlas", "Menyamai sepertiga Al-Quran", "HR Al-Bukhari, no. 5013"],
             ["4", "Berselawat ke atas Nabi SAW sekali", "Allah berselawat (memberi rahmat) 10 kali", "HR Muslim, no. 408"],
             ["5", "La hawla wa la quwwata illa billah", "Salah satu perbendaharaan syurga", "HR Al-Bukhari, no. 4205"],
             ["6", "Alhamdulillah; Subhanallah wal-hamdulillah", "Memenuhi timbangan; memenuhi antara langit dan bumi", "HR Muslim, no. 223"],
             ["7", "La ilaha illallahu wahdahu la syarika lah… 100 kali", "Pahala memerdekakan 10 hamba, 100 kebaikan, terpelihara daripada syaitan hari itu", "HR Al-Bukhari, no. 3293"],
             ["8", "Tasbih 33, tahmid 33, takbir 33 selepas solat dan genapkan 100", "Diampunkan dosa walaupun sebanyak buih di laut", "HR Muslim, no. 597"],
             ["9", "Tersenyum kepada saudara", "Dikira sedekah", "HR At-Tirmizi, no. 1956"],
             ["10", "Membuang halangan dari jalan", "Cabang iman dan pahala sedekah", "HR Muslim, no. 35, 1914"]])),
        ("kalimah", "Empat Kalimah yang Paling Dicintai Allah",
         dc(P, "Empat kalimah", "سُبْحَانَ اللّٰهِ، وَالْحَمْدُ لِلّٰهِ، وَلَا إِلٰهَ إِلَّا اللّٰهُ، وَاللّٰهُ أَكْبَرُ", "Subhanallah, walhamdulillah, wa la ilaha illallah, wallahu akbar.",
            "Maha Suci Allah, segala puji bagi Allah, tiada tuhan melainkan Allah, dan Allah Maha Besar.", "HR Muslim, no. 2137",
            "Nabi SAW bersabda kalimah ini lebih dicintai Baginda daripada segala yang disinari matahari (HR Muslim, no. 2695).")),
        ("bila", "Bila Mengamalkannya",
         ul("Ketika menunggu: lampu isyarat, giliran di klinik, bas atau LRT.", "Selepas solat fardu: tasbih 33-33-33.", "Sebelum tidur: tasbih, tahmid dan takbir.",
            "Ketika berjalan: berselawat dan beristighfar.")
         + f'<p>Gunakan kaunter digital: <a href="{Q}tasbih-digital/">Tasbih Digital</a> dan <a href="{Q}zikir-pagi-petang/">Zikir Pagi Petang</a>.</p>'),
        ("palsu", "Ganjaran yang Tidak Sahih",
         "<p>Banyak mesej berantai menjanjikan ganjaran khusus, seperti “baca sekali dapat pahala 70,000 malaikat” atau “kongsi 10 orang dapat rumah di syurga”. Kebanyakannya <strong>tiada sumber sahih</strong>. "
         "Senarai di atas hanya mengandungi ganjaran yang disebut dalam hadis sahih, dan ia sudah cukup besar.</p>"),
    ],
    faq=[("Apakah amalan ringan yang pahalanya besar?", "Subhanallahi wa bihamdih 100 kali (HR Al-Bukhari 6405), membaca Al-Ikhlas (HR Al-Bukhari 5013), berselawat (HR Muslim 408) dan la hawla wa la quwwata illa billah (HR Al-Bukhari 4205)."),
         ("Apakah zikir yang menghapuskan dosa sebanyak buih di laut?", "Subhanallahi wa bihamdih 100 kali sehari (HR Al-Bukhari 6405), dan tasbih 33, tahmid 33, takbir 33 selepas solat yang digenapkan 100 (HR Muslim 597)."),
         ("Apakah kalimah yang paling dicintai Allah?", "Subhanallah, walhamdulillah, wa la ilaha illallah, wallahu akbar (HR Muslim 2137).")],
    refs=["Sahih Al-Bukhari, no. 3293, 4205, 5013, 6405, 6682.", "Sahih Muslim, no. 35, 223, 408, 597, 1914, 2137, 2695.", "Sunan At-Tirmizi, no. 1956."],
    related=[(Q + "tasbih-digital/", "Tasbih Digital", "Kaunter zikir dalam telefon"), (U["sedekah-jariah"], "Sedekah Jariah", "7 amalan pahala berterusan"),
             (U["kalimah-dibenci"], "Kalimah Disukai & Dibenci Allah", "Hadis tentang tutur kata")])))

# 8 ---------------------------------------------------------------- Wanita ahli neraka (context)
P = "ilmx-wn"
POSTS.append(("wanita-neraka", b4(
    ns=P, url=U["wanita-neraka"], published="2017-12-08", pubms="8 Disember 2017",
    title="Benarkah Wanita Paling Ramai Ahli Neraka? Maksud & Konteks Hadis",
    desc="Hadis wanita paling ramai ahli neraka: lafaz sahih, sebab yang disebut Nabi SAW, konteks sedekah hari raya, dan hadis bahawa wanita juga ramai di syurga.",
    h1="Benarkah Wanita Paling Ramai Ahli Neraka?",
    img=img("wanita-ahli-neraka", "Kefahaman Hadis", "Wanita & Ahli Neraka", "Maksud dan konteks hadis sahih", "تَصَدَّقْنَ"),
    alt="Maksud dan konteks hadis wanita ahli neraka", refshort="Sahih Al-Bukhari, Sahih Muslim",
    lead="Hadis ini sahih, tetapi sering dipetik tanpa konteks. Artikel ini menerangkan lafaznya, sebab yang disebut, tujuan Nabi SAW menyampaikannya dan hadis lain yang melengkapkannya.",
    crumb=("Hadis", W + "search/label/Hadis"), about=["Hadis wanita ahli neraka", "Kedudukan wanita dalam Islam"],
    answer="Hadis ini <strong>sahih</strong>. Nabi SAW berkhutbah kepada wanita pada hari raya dan bersabda: <strong>“Bersedekahlah, kerana aku melihat kamu paling ramai penghuni neraka”</strong>, kerana <strong>banyak melaknat dan mengingkari kebaikan suami</strong> <em>(HR Al-Bukhari, no. 304; Muslim, no. 79)</em>. "
           "Ia nasihat yang disertai jalan keluar, iaitu sedekah, bukan penghinaan. Hadis lain menunjukkan <strong>wanita juga ramai di syurga</strong> <em>(HR Muslim, no. 2834)</em>, dan ganjaran amal lelaki dan wanita sama di sisi Allah <em>(Ali 'Imran 3:195)</em>.",
    sections=[
        ("lafaz", "Lafaz Hadis dan Konteksnya",
         "<p>Abu Sa'id Al-Khudri RA meriwayatkan bahawa pada hari Aidiladha atau Aidilfitri, Nabi SAW melalui kumpulan wanita dan bersabda: “Wahai kaum wanita, <strong>bersedekahlah</strong>, kerana aku diperlihatkan bahawa kamu paling ramai penghuni neraka.” "
         "Mereka bertanya: “Mengapa, wahai Rasulullah?” Baginda menjawab: “<strong>Kamu banyak melaknat dan mengingkari kebaikan suami</strong>”" + ref("HR Al-Bukhari, no. 304") + ".</p>"
         "<p>Dalam riwayat solat gerhana, Baginda menjelaskan maksud “mengingkari”: jika suami berbuat baik sepanjang masa, kemudian isteri melihat satu perkara yang tidak disukai, dia berkata “aku tidak pernah melihat kebaikan daripadamu”" + ref("HR Al-Bukhari, no. 29, 1052") + ".</p>"),
        ("faham", "Lima Perkara untuk Memahami Hadis Ini dengan Betul",
         ul("<strong>Sebabnya ialah perbuatan, bukan jantina.</strong> Yang disebut ialah melaknat dan mengingkari kebaikan. Lelaki yang melakukan dosa yang sama juga diancam.",
            "<strong>Ia disampaikan bersama penyelesaian.</strong> Perintah pertama dalam hadis ialah “bersedekahlah”, dan para wanita terus menyedekahkan perhiasan mereka.",
            "<strong>Wanita juga ramai di syurga.</strong> Setiap lelaki ahli syurga mempunyai dua isteri daripada manusia" + ref("HR Muslim, no. 2834") + ", dan ulama menyimpulkan wanita juga ramai di syurga.",
            "<strong>Ganjaran amal sama.</strong> “Aku tidak mensia-siakan amal orang yang beramal di antara kamu, lelaki atau perempuan”" + ref("Ali 'Imran 3:195; An-Nahl 16:97"),
            "<strong>Jalan ke syurga dijelaskan.</strong> Wanita yang menjaga solat lima waktu, puasa Ramadan, kehormatan dan mentaati suami dalam kebaikan, masuk syurga dari mana-mana pintu yang dikehendakinya" + ref("HR Ahmad, no. 1661; hasan"))),
        ("palsu", "Kisah Seksaan Wanita yang Tidak Sahih",
         f'<div class="{P}-box amber">Kisah “Nabi melihat wanita digantung dengan rambut, lidah dan buah dada di neraka” yang tersebar dalam artikel lama ini dan media sosial ialah riwayat yang <strong>sangat lemah atau palsu</strong> menurut ulama hadis. '
         "Ia telah dibuang daripada versi ini.</div>"),
        ("amal", "Amalan yang Disebut dalam Hadis",
         ul("Bersedekah, walaupun sedikit, kerana ia dinyatakan sebagai penyelamat dalam hadis ini.", "Menjaga lidah daripada melaknat dan mencela.",
            "Menghargai kebaikan pasangan; ini terpakai kepada suami dan isteri.", "Menjaga solat lima waktu dan puasa Ramadan.")
         + f'<p>Lihat juga <a href="{U["tanggungjawab-suami"]}">tanggungjawab suami dalam Islam</a> dan <a href="{SEDEKAH}">kelebihan sedekah</a>.</p>'),
    ],
    faq=[("Adakah hadis wanita paling ramai ahli neraka sahih?", "Ya, diriwayatkan Al-Bukhari (304) dan Muslim (79). Sebab yang disebut ialah banyak melaknat dan mengingkari kebaikan suami, dan Nabi SAW menyuruh bersedekah sebagai jalan keluar."),
         ("Mengapa wanita ramai di neraka?", "Hadis menyebut dua perbuatan: banyak melaknat dan mengingkari kebaikan suami. Ia berkaitan perbuatan, bukan kerana jantina."),
         ("Adakah wanita juga ramai di syurga?", "Ya. Setiap lelaki ahli syurga mempunyai dua isteri daripada manusia (HR Muslim 2834), dan Allah menyamakan ganjaran amal lelaki dan wanita (Ali 'Imran 3:195)."),
         ("Apakah amalan wanita untuk masuk syurga?", "Menjaga solat lima waktu, puasa Ramadan, kehormatan diri dan mentaati suami dalam kebaikan (HR Ahmad 1661).")],
    refs=["Sahih Al-Bukhari, no. 29, 304, 1052.", "Sahih Muslim, no. 79, 2834.", "Musnad Ahmad, no. 1661.", "Al-Quran: Ali 'Imran 3:195; An-Nahl 16:97."],
    disclaimer="Hadis ini disampaikan dengan konteks penuh. Kisah seksaan yang tidak sahih telah dibuang daripada artikel asal.",
    related=[(U["tanggungjawab-suami"], "Tanggungjawab Suami", "10 kewajipan suami dalam Islam"), (SEDEKAH, "Apa Itu Sedekah", "Kelebihan dan jenis sedekah"),
             (U["kalimah-dibenci"], "Kalimah Disukai & Dibenci Allah", "Menjaga lidah menurut hadis")])))

# 9 ---------------------------------------------------------------- Hari jadi & tiup lilin
P = "ilmx-hj"
POSTS.append(("hari-jadi", b4(
    ns=P, url=U["hari-jadi"], published="2020-01-09", pubms="9 Januari 2020",
    title="Hukum Sambut Hari Jadi & Tiup Lilin Dalam Islam (Pandangan Ulama)",
    desc="Hukum menyambut hari jadi dan meniup lilin kek dalam Islam menurut ulama, syarat sambutan yang dibenarkan, ucapan hari jadi Islamik dan cara mengisinya.",
    h1="Hukum Sambut Hari Jadi & Tiup Lilin",
    img=img("hukum-sambut-hari-jadi", "Hukum Semasa", "Sambut Hari Jadi", "Hukum, tiup lilin & ucapan Islamik", "بَارَكَ اللّٰهُ فِي عُمُرِكَ"),
    alt="Hukum sambut hari jadi dan tiup lilin dalam Islam", refshort="Sahih Muslim, pandangan ulama kontemporari",
    lead="Dua pandangan ulama tentang sambutan hari jadi, syarat yang menjadikannya harus, isu meniup lilin dan “make a wish”, serta ucapan yang sesuai.",
    crumb=("Hukum", W + "search/label/Hukum"), about=["Hukum sambut hari jadi", "Tiup lilin"],
    answer="Ulama berbeza pandangan. <strong>Ramai ulama kontemporari, termasuk pandangan yang dikeluarkan oleh institusi mufti di Malaysia, mengharuskan</strong> sambutan hari jadi sebagai adat, dengan syarat tiada maksiat, pembaziran atau iktikad yang bercanggah dengan akidah. "
           "Sebahagian ulama lain melarangnya kerana menyerupai amalan bukan Islam. <strong>Meniup lilin</strong> sebagai adat kebiasaannya dihukum harus oleh pihak yang mengharuskan sambutan, tetapi <strong>mempercayai hajat akan termakbul dengan meniup lilin</strong> ialah khurafat.",
    sections=[
        ("pandangan", "Dua Pandangan Ulama",
         table(["Pandangan", "Hujah", "Syarat atau catatan"], [
             ["Harus (dibolehkan)", "Sambutan hari jadi ialah adat, bukan ibadah. Asal sesuatu adat adalah harus selagi tiada dalil yang melarang", "Tiada maksiat, pergaulan bebas, pembaziran, atau unsur ritual agama lain"],
             ["Dilarang", "Menyerupai amalan bukan Islam (tasyabbuh) dan menambah perayaan selain dua hari raya", "Pandangan sebahagian ulama, terutama di Arab Saudi"]])
         + "<p>Nabi SAW bersabda: “Sesiapa yang menyerupai sesuatu kaum, dia termasuk dalam kalangan mereka”" + ref("HR Abu Daud, no. 4031")
         + ". Pihak yang mengharuskan menjelaskan tasyabbuh yang dilarang ialah meniru perkara yang menjadi ciri khusus agama lain, manakala sambutan hari jadi hari ini telah menjadi adat umum.</p>"),
        ("lilin", "Hukum Meniup Lilin dan “Make a Wish”",
         ul("<strong>Meniup lilin sebagai adat atau hiburan kanak-kanak</strong>: dihukum harus oleh pihak yang mengharuskan sambutan, kerana tiada iktikad padanya.",
            "<strong>Mempercayai hajat akan tercapai jika lilin ditiup sekali nafas</strong>: khurafat yang bercanggah dengan tauhid. Hajat dipohon kepada Allah sahaja" + ref("Ghafir 40:60"),
            "<strong>Alternatif yang lebih baik</strong>: gantikan “make a wish” dengan doa bersama untuk orang yang menyambut hari jadi."),
         ),
        ("ucapan", "Ucapan Hari Jadi dalam Islam",
         dc(P, "Semoga Allah memberkati umurmu", "بَارَكَ اللّٰهُ فِي عُمُرِكَ", "Barakallahu fi 'umrik.", "Semoga Allah memberkati umurmu.", "Doa umum; boleh juga “Barakallahu fiki” bagi perempuan")
         + "<p>Doa ini tidak dikhususkan oleh hadis untuk hari jadi, tetapi ia doa yang baik. Anda juga boleh mendoakan umur yang panjang dalam ketaatan, ilmu yang bermanfaat dan kesihatan.</p>"),
        ("isi", "Cara Mengisi Hari Jadi dengan Bermakna",
         "<p>Nabi SAW berpuasa pada hari Isnin dan bersabda: “Itulah hari aku dilahirkan”" + ref("HR Muslim, no. 1162") + ". Ini menunjukkan hari lahir boleh diingati dengan ibadah. Cadangan:</p>"
         + ul("Muhasabah: apa yang bertambah baik dalam setahun ini?", "Bersedekah atau sumbangan atas nama anak.", "Majlis makan dengan doa kesyukuran, tanpa pembaziran.",
              "Hadiah yang bermanfaat, seperti buku, Al-Quran atau sumbangan wakaf.")),
    ],
    faq=[("Apakah hukum menyambut hari jadi dalam Islam?", "Ulama berbeza pandangan. Ramai ulama kontemporari mengharuskannya sebagai adat dengan syarat tiada maksiat, pembaziran atau unsur akidah lain; sebahagian ulama melarangnya."),
         ("Apakah hukum meniup lilin hari jadi?", "Sebagai adat tanpa iktikad, ia dihukum harus oleh pihak yang mengharuskan sambutan. Mempercayai hajat termakbul dengan meniup lilin ialah khurafat."),
         ("Apakah ucapan hari jadi dalam Islam?", "“Barakallahu fi 'umrik” (semoga Allah memberkati umurmu), atau doa kebaikan dalam bahasa sendiri."),
         ("Adakah Nabi Muhammad menyambut hari lahirnya?", "Tidak dengan majlis, tetapi Baginda berpuasa pada hari Isnin dan menyebutnya sebagai hari kelahirannya (HR Muslim 1162).")],
    refs=["Sahih Muslim, no. 1162.", "Sunan Abu Daud, no. 4031.", "Al-Quran: Ghafir 40:60.", "Irsyad Al-Fatwa, Pejabat Mufti Wilayah Persekutuan, artikel berkaitan sambutan hari lahir."],
    disclaimer="Persoalan ini termasuk khilaf ulama. Ikuti panduan pejabat mufti negeri anda.",
    related=[(U["sunnah-nabi"], "15 Sunnah Nabi Setiap Hari", "Amalan harian dengan hadis sahih"), (DOA_ANAK, "Doa Anak Soleh & Solehah", "Doa ibu bapa untuk anak"),
             (U["sedekah-jariah"], "Sedekah Jariah", "Hadiah pahala yang berterusan")])))

# 10 --------------------------------------------------------------- Mengungkit sedekah
P = "ilmx-mu"
POSTS.append(("mengungkit", b4(
    ns=P, url=U["mengungkit"], published="2020-01-12", pubms="12 Januari 2020",
    title="Hukum Mengungkit Sedekah & Pemberian: Al-Baqarah 264 & Hadis",
    desc="Hukum mengungkit sedekah dan pemberian kepada keluarga, pasangan atau kawan menurut Al-Baqarah 264 dan hadis sahih, serta cara memberi dengan ikhlas.",
    h1="Hukum Mengungkit Sedekah & Pemberian",
    img=img("mengungkit-sedekah", "Akhlak", "Mengungkit Sedekah", "Al-Baqarah 264 & hadis sahih", "لَا تُبْطِلُوا صَدَقَاتِكُمْ"),
    alt="Hukum mengungkit sedekah dan pemberian dalam Islam", refshort="Al-Quran, Sahih Muslim, Sahih Al-Bukhari",
    lead="Apa kata Al-Quran dan hadis tentang mengungkit pemberian, mengapa ia menghapuskan pahala, dan bagaimana memberi tanpa mengharap balasan.",
    crumb=("Akhlak", W + "search/label/Akhlak"), about=["Mengungkit sedekah", "Ikhlas"],
    answer="Mengungkit sedekah dan pemberian (al-mann) <strong>haram dan menghapuskan pahala</strong> sedekah itu: “Janganlah kamu batalkan sedekah kamu dengan mengungkit-ungkit dan menyakiti” <em>(Al-Baqarah 2:264)</em>. "
           "Nabi SAW menyebut orang yang mengungkit pemberian sebagai salah seorang daripada <strong>tiga golongan yang tidak diajak bicara dan tidak dipandang Allah pada hari kiamat</strong> <em>(HR Muslim, no. 106)</em>.",
    sections=[
        ("ayat", "Al-Baqarah 264: Sedekah yang Terhapus", qcard(P, "Al-Baqarah 2:264", 2, 264, 264, "Surah Al-Baqarah, ayat 264")
         + "<p>Allah mengumpamakan sedekah yang diungkit seperti tanah di atas batu licin yang ditimpa hujan lebat: tiada apa-apa yang tinggal. Ayat sebelumnya menyebut “perkataan yang baik dan pemaafan lebih baik daripada sedekah yang diiringi dengan menyakiti”"
         + ref("Al-Baqarah 2:263") + ".</p>"),
        ("hadis", "Hadis tentang Mengungkit Pemberian",
         grade([("Tiga golongan yang tidak diajak bicara, tidak dipandang dan tidak disucikan Allah: orang yang melabuhkan pakaian kerana sombong, orang yang mengungkit pemberian, dan peniaga yang melariskan barang dengan sumpah palsu", "HR Muslim, no. 106", SAHIH),
                 ("Orang yang meminta kembali hadiahnya seperti anjing yang menjilat semula muntahnya", "HR Al-Bukhari, no. 2589; Muslim, no. 1622", SAHIH),
                 ("Tangan yang di atas (memberi) lebih baik daripada tangan yang di bawah", "HR Al-Bukhari, no. 1429", SAHIH)], head="Hadis")),
        ("contoh", "Contoh Mengungkit dalam Kehidupan Harian",
         ul("Kepada pasangan: “Siapa yang bayar rumah ini selama ini?” ketika bertengkar.", "Kepada anak: mengira-ngira belanja membesarkan mereka untuk menuntut balasan.",
            "Kepada ibu bapa: menyebut-nyebut wang yang diberi kepada mereka.", "Kepada kawan: “Dulu aku tolong kau, sekarang kau buat aku macam ini.”",
            "Di media sosial: menghebahkan sumbangan kepada orang tertentu sehingga memalukan penerima."),
         ),
        ("hebah", "Bolehkah Menghebahkan Sedekah?",
         "<p>Allah berfirman: “Jika kamu menampakkan sedekah, itu baik; dan jika kamu menyembunyikannya dan memberikannya kepada fakir miskin, itu lebih baik bagimu”" + ref("Al-Baqarah 2:271")
         + ". Menghebahkan dengan niat menggalakkan orang lain dibenarkan. Yang dilarang ialah riak, dan memalukan atau menyakiti penerima.</p>"),
        ("ikhlas", "Cara Memberi dengan Ikhlas",
         ul("Niatkan kerana Allah sebelum memberi, dan lupakan selepas memberi.", "Jangan sebut pemberian ketika marah.",
            "Jika terlanjur mengungkit, minta maaf kepada penerima dan beristighfar.", "Utamakan sedekah secara rahsia: salah satu golongan yang dinaungi Arasy ialah orang yang bersedekah sehingga tangan kirinya tidak tahu apa yang diberi tangan kanannya" + ref("HR Al-Bukhari, no. 1423"))
         + f'<p>Asas sedekah: <a href="{SEDEKAH}">Apa Itu Sedekah</a>. Pahala berterusan: <a href="{U["sedekah-jariah"]}">Sedekah Jariah</a>.</p>'),
    ],
    faq=[("Apakah hukum mengungkit sedekah?", "Haram dan menghapuskan pahala sedekah itu (Al-Baqarah 2:264). Orang yang mengungkit pemberian tidak dipandang Allah pada hari kiamat (HR Muslim 106)."),
         ("Apakah maksud mengungkit?", "Menyebut-nyebut pemberian atau jasa kepada penerima dengan tujuan menunjuk-nunjuk, menuntut balasan atau menyakitinya."),
         ("Adakah mengungkit pemberian kepada pasangan atau anak berdosa?", "Ya, larangan itu umum. Nafkah kepada keluarga ialah kewajipan dan pahala, dan mengungkitnya merosakkan pahala dan hubungan."),
         ("Bolehkah meminta semula hadiah?", "Dilarang. Nabi SAW mengumpamakannya seperti anjing yang menjilat semula muntahnya (HR Al-Bukhari 2589), kecuali bapa terhadap anaknya menurut sebahagian ulama.")],
    refs=["Al-Quran: Al-Baqarah 2:262–264, 2:271.", "Sahih Muslim, no. 106, 1622.", "Sahih Al-Bukhari, no. 1423, 1429, 2589."],
    related=[(SEDEKAH, "Apa Itu Sedekah", "Maksud, jenis dan kelebihan"), (U["sedekah-jariah"], "Sedekah Jariah", "Pahala yang terus mengalir"),
             (U["keras-hati"], "Keras Hati", "Tanda dan cara melembutkan hati")])))

# 11 --------------------------------------------------------------- Suara wanita / wanita menyanyi
P = "ilmx-sw"
POSTS.append(("suara-wanita", b4(
    ns=P, url=U["suara-wanita"], published="2018-02-07", pubms="7 Februari 2018",
    title="Adakah Suara Wanita Aurat? Hukum Wanita Menyanyi (Mazhab Syafi'i)",
    desc="Adakah suara wanita aurat menurut mazhab Syafi'i, hukum wanita bercakap, mengaji dan menyanyi di hadapan lelaki ajnabi, serta garis panduan yang dibenarkan.",
    h1="Adakah Suara Wanita Aurat?",
    img=img("suara-wanita-aurat", "Fiqh Wanita", "Adakah Suara Wanita Aurat?", "Hukum bercakap, mengaji & menyanyi", "فَلَا تَخْضَعْنَ بِالْقَوْلِ"),
    alt="Hukum suara wanita dan wanita menyanyi dalam Islam", refshort="Al-Quran, Sahih Al-Bukhari, kitab fiqh Syafi'i",
    lead="Pendapat muktamad mazhab Syafi'i tentang suara wanita, perbezaan antara bercakap biasa dan melunakkan suara, dan garis panduan tentang nyanyian.",
    crumb=("Fiqh", W + "search/label/Fiqh"), about=["Suara wanita", "Hukum menyanyi"],
    answer="Menurut pendapat yang <strong>paling sahih dalam mazhab Syafi'i, suara wanita bukan aurat</strong>. Wanita boleh bercakap, berjual beli dan mengajar lelaki ajnabi dengan suara biasa, sebagaimana isteri-isteri Nabi SAW meriwayatkan hadis kepada para sahabat. "
           "Yang dilarang ialah <strong>melunakkan dan memerdukan suara sehingga menimbulkan fitnah</strong> <em>(Al-Ahzab 33:32)</em>. Atas sebab itu, ramai ulama melarang wanita menyanyi dengan suara merdu di hadapan lelaki ajnabi, terutama jika dikhuatiri fitnah.",
    sections=[
        ("ayat", "Larangan Melunakkan Suara", qcard(P, "Al-Ahzab 33:32", 33, 32, 32, "Surah Al-Ahzab, ayat 32")
         + "<p>Ayat ini tidak melarang wanita bercakap, malah menyuruh mereka “berkata dengan perkataan yang baik”. Yang dilarang ialah <em>khudhu' bil-qaul</em>: melembutkan dan menggoda dengan suara.</p>"),
        ("hukum", "Hukum Mengikut Keadaan",
         table(["Keadaan", "Hukum (mazhab Syafi'i)"], [
             ["Bercakap biasa, berurusan, mengajar, menjawab telefon", "Harus; suara bukan aurat"],
             ["Membaca Al-Quran atau berceramah kepada khalayak lelaki", "Harus dengan suara biasa; jika dikhuatiri fitnah, lebih baik dielakkan"],
             ["Melunakkan atau memerdukan suara di hadapan lelaki ajnabi", "Haram jika dengan tujuan atau kesan menimbulkan fitnah"],
             ["Menyanyi di hadapan wanita atau mahram, dengan lirik yang baik", "Harus"],
             ["Menyanyi dengan suara merdu di hadapan lelaki ajnabi atau khalayak umum", "Dilarang oleh ramai ulama kerana dikhuatiri fitnah"],
             ["Lelaki mendengar suara wanita dengan berlazat-lazat", "Haram, walaupun suaranya biasa"]])),
        ("hadis", "Dalil daripada Sunnah",
         ul("Isteri-isteri Nabi SAW, terutama Aisyah RA, meriwayatkan ribuan hadis kepada sahabat lelaki secara lisan.",
            "Dua orang budak perempuan menyanyi pada hari raya di rumah Aisyah RA dan Nabi SAW membenarkannya" + ref("HR Al-Bukhari, no. 952; Muslim, no. 892"),
            "Seorang wanita bersuara dan berhujah dengan Umar RA di masjid tentang mahar, dan beliau menerimanya (diriwayatkan dalam kitab tafsir dan sirah)."),
         ),
        ("panduan", "Garis Panduan Nyanyian dan Persembahan",
         ul("Lirik yang baik dan tidak bercanggah dengan akidah atau akhlak.", "Menutup aurat dan berpakaian sopan.",
            "Tiada pergaulan bebas dan tiada gerak tubuh yang menggoda.", "Tidak melalaikan daripada solat dan kewajipan.",
            "Persembahan wanita kepada khalayak wanita, atau nasyid kanak-kanak, lebih jauh daripada khilaf."),
         ),
    ],
    faq=[("Adakah suara wanita aurat?", "Menurut pendapat paling sahih mazhab Syafi'i, tidak. Yang dilarang ialah melunakkan suara sehingga menimbulkan fitnah (Al-Ahzab 33:32)."),
         ("Bolehkah wanita mengaji di hadapan lelaki?", "Harus dengan suara biasa. Jika dikhuatiri fitnah, lebih baik dielakkan."),
         ("Apakah hukum wanita menyanyi?", "Harus di hadapan wanita dan mahram dengan lirik yang baik. Ramai ulama melarang wanita menyanyi dengan suara merdu di hadapan lelaki ajnabi kerana dikhuatiri fitnah."),
         ("Bolehkah wanita menjadi penceramah?", "Boleh, dan isteri-isteri Nabi SAW mengajar hadis kepada para sahabat. Ia dengan suara biasa, pakaian sopan dan kandungan yang bermanfaat.")],
    refs=["Al-Quran: Al-Ahzab 33:32.", "Sahih Al-Bukhari, no. 952; Sahih Muslim, no. 892.", "An-Nawawi, Raudhah At-Talibin, bab nikah (hukum suara wanita).", "Al-Khatib Asy-Syirbini, Mughni Al-Muhtaj, bab nikah."],
    disclaimer="Persoalan nyanyian termasuk khilaf ulama. Untuk isu persembahan dan industri seni, rujuk garis panduan pejabat mufti negeri anda.",
    related=[(U["keras-hati"], "Keras Hati", "Tanda dan cara melembutkan hati"), (U["wanita-neraka"], "Benarkah Wanita Ramai Ahli Neraka?", "Maksud dan konteks hadis"),
             (Q + "belajar-solat/", "Belajar Solat", "Panduan solat dengan bacaan")])))

# 12 --------------------------------------------------------------- Keras hati
P = "ilmx-kh"
POSTS.append(("keras-hati", b4(
    ns=P, url=U["keras-hati"], published="2018-01-26", pubms="26 Januari 2018",
    title="Keras Hati: Maksud, 7 Tanda & Cara Melembutkan Hati (Al-Quran)",
    desc="Maksud keras hati dalam Islam, 7 tanda hati yang keras menurut Al-Quran dan hadis, puncanya, dan 7 cara melembutkan hati yang disebut dalam dalil sahih.",
    h1="Keras Hati: Tanda dan Cara Melembutkannya",
    img=img("keras-hati", "Penyakit Hati", "Keras Hati", "Maksud, 7 tanda & cara melembutkan hati", "قَسَتْ قُلُوبُهُمْ"),
    alt="Tanda keras hati dan cara melembutkan hati", refshort="Al-Quran, Sunan At-Tirmizi, Musnad Ahmad",
    lead="Apa yang dimaksudkan dengan hati yang keras menurut Al-Quran, tanda-tandanya dalam kehidupan harian, puncanya dan langkah yang disebut dalam dalil untuk melembutkannya.",
    crumb=("Tazkirah", W + "search/label/Tazkirah"), about=["Keras hati", "Penyakit hati"],
    answer="<strong>Keras hati (qaswatul qalb)</strong> ialah keadaan hati yang tidak lagi tersentuh dengan peringatan Allah, sehingga Al-Quran mengumpamakannya <strong>seperti batu atau lebih keras lagi</strong> <em>(Al-Baqarah 2:74)</em>. "
           "Puncanya ialah dosa yang berterusan sehingga menutup hati <em>(Al-Mutaffifin 83:14; HR At-Tirmizi, no. 3334)</em>. Ia dilembutkan dengan <strong>zikir</strong> <em>(Ar-Ra'd 13:28)</em>, <strong>membaca Al-Quran</strong>, <strong>mengingati mati</strong> dan <strong>mengasihi anak yatim dan orang miskin</strong> <em>(HR Ahmad, no. 7576)</em>.",
    sections=[
        ("ayat", "Keras Hati dalam Al-Quran", qcard(P, "Al-Hadid 57:16", 57, 16, 16, "Surah Al-Hadid, ayat 16")
         + "<p>Ayat ini menyeru orang beriman supaya hati mereka khusyuk dan tidak menjadi seperti orang terdahulu yang hatinya mengeras kerana masa yang panjang tanpa peringatan.</p>"),
        ("punca", "Punca Hati Mengeras",
         "<p>Nabi SAW bersabda: “Apabila seorang hamba melakukan dosa, satu titik hitam ditandakan pada hatinya. Jika dia berhenti, beristighfar dan bertaubat, hatinya dibersihkan. Jika dia mengulanginya, titik itu bertambah sehingga menutup hatinya. "
         "Itulah ar-ran yang disebut Allah”" + ref("HR At-Tirmizi, no. 3334; hasan sahih") + ". Punca lain yang disebut ulama: banyak bercakap tanpa zikir, banyak ketawa" + ref("HR Ibn Majah, no. 4193") + ", cinta dunia berlebihan dan lalai daripada mengingati mati.</p>"),
        ("tanda", "7 Tanda Hati yang Keras",
         ul("Tidak tersentuh ketika mendengar ayat Al-Quran" + ref("Al-Anfal 8:2"), "Malas dan terasa berat melakukan ibadah", "Tidak merasa bersalah selepas berbuat dosa",
            "Nasihat tidak lagi memberi kesan", "Tidak berasa sedih melihat orang susah", "Cinta dunia dan takut kehilangannya", "Jarang mengingati mati dan akhirat", ordered=True)),
        ("cara", "7 Cara Melembutkan Hati",
         table(["Cara", "Dalil"], [
             ["Memperbanyak zikir: hati menjadi tenang dengan mengingati Allah", "Ar-Ra'd 13:28"],
             ["Membaca dan mentadabbur Al-Quran", "Az-Zumar 39:23"],
             ["Mengusap kepala anak yatim dan memberi makan orang miskin", "HR Ahmad, no. 7576 (hasan): Nabi SAW menyarankannya kepada lelaki yang mengadu hatinya keras"],
             ["Mengingati mati dan menziarahi kubur", "HR Muslim, no. 976; Ibn Majah, no. 4258"],
             ["Bertaubat dan beristighfar segera selepas berdosa", "HR At-Tirmizi, no. 3334"],
             ["Berdoa memohon ketetapan hati", "HR At-Tirmizi, no. 2140"],
             ["Bersahabat dengan orang soleh dan menghadiri majlis ilmu", "Al-Kahf 18:28"]])
         + f'<p>Doa tetap hati: <a href="{MUQALLIB}">Doa Ya Muqallibal Qulub</a>.</p>'),
        ("lembut", "Teladan Lemah Lembut Rasulullah SAW",
         qcard(P, "Ali 'Imran 3:159", 3, 159, 159, "Surah Ali 'Imran, ayat 159")),
    ],
    faq=[("Apakah maksud keras hati?", "Hati yang tidak lagi tersentuh dengan peringatan Allah, diumpamakan seperti batu atau lebih keras (Al-Baqarah 2:74)."),
         ("Apakah tanda hati yang keras?", "Tidak tersentuh dengan Al-Quran, malas beribadah, tidak merasa bersalah selepas berdosa, nasihat tidak memberi kesan, dan jarang mengingati mati."),
         ("Bagaimana cara melembutkan hati?", "Zikir (Ar-Ra'd 13:28), membaca Al-Quran, mengusap kepala anak yatim dan memberi makan orang miskin (HR Ahmad 7576), mengingati mati dan bertaubat."),
         ("Apakah punca hati menjadi keras?", "Dosa yang berterusan tanpa taubat sehingga menutup hati (HR At-Tirmizi 3334; Al-Mutaffifin 83:14).")],
    refs=["Al-Quran: Al-Baqarah 2:74; Al-Hadid 57:16; Al-Mutaffifin 83:14; Ar-Ra'd 13:28; Az-Zumar 39:23; Al-Anfal 8:2; Al-Kahf 18:28; Ali 'Imran 3:159.",
          "Sunan At-Tirmizi, no. 2140, 3334; Sunan Ibn Majah, no. 4193, 4258.", "Musnad Ahmad, no. 7576.", "Sahih Muslim, no. 976."],
    related=[(MUQALLIB, "Doa Ya Muqallibal Qulub", "Doa tetap hati dan hidayah"), (Q + "zikir-pagi-petang/", "Zikir Pagi Petang", "Zikir harian dengan kaunter"),
             (U["mengungkit"], "Hukum Mengungkit Sedekah", "Akhlak memberi dengan ikhlas")])))

# 13 --------------------------------------------------------------- Akidah anak
P = "ilmx-aa"
POSTS.append(("akidah-anak", b4(
    ns=P, url=U["akidah-anak"], published="2018-01-11", pubms="11 Januari 2018",
    title="Cara Menanam Akidah Pada Anak Ikut Umur: Panduan Ibu Bapa Muslim",
    desc="Cara menanam akidah pada anak mengikut umur 0 hingga 12 tahun berdasarkan wasiat Luqman dan hadis sahih, dengan aktiviti harian yang mudah untuk ibu bapa.",
    h1="Cara Menanam Akidah Pada Anak Ikut Umur",
    img=img("akidah-anak", "Keibubapaan", "Akidah Anak", "Panduan ikut umur daripada wasiat Luqman", "يَا بُنَيَّ"),
    alt="Cara menanam akidah pada anak mengikut umur", refshort="Al-Quran (Surah Luqman), Sahih Al-Bukhari, Sunan At-Tirmizi",
    lead="Pelan ringkas mengikut umur untuk mengenalkan anak kepada Allah, Rasul dan rukun iman, berpandukan wasiat Luqman kepada anaknya dan cara Nabi SAW mendidik kanak-kanak.",
    crumb=("Keluarga", W + "search/label/Keluarga"), about=["Akidah anak", "Pendidikan anak dalam Islam"],
    answer="Setiap anak dilahirkan dalam keadaan <strong>fitrah</strong>, dan ibu bapalah yang membentuknya <em>(HR Al-Bukhari, no. 1385)</em>. Akidah ditanam secara berperingkat: <strong>kalimah tauhid dan cerita tentang Allah sejak kecil</strong>, "
           "<strong>rukun iman dan sirah ketika 4–6 tahun</strong>, <strong>solat dan makna ibadah pada usia 7 tahun</strong> <em>(HR Abu Daud, no. 495)</em>, dan <strong>hujah serta perbincangan pada usia 10 tahun ke atas</strong>, "
           "seperti wasiat Luqman yang dimulakan dengan larangan syirik <em>(Luqman 31:13)</em>.",
    sections=[
        ("luqman", "Wasiat Luqman: Kurikulum Akidah dalam Al-Quran", qcard(P, "Luqman 31:13", 31, 13, 13, "Surah Luqman, ayat 13")
         + table(["Ayat", "Pengajaran untuk anak"], [["31:13", "Tauhid: jangan sekutukan Allah"], ["31:14–15", "Berbuat baik kepada ibu bapa"], ["31:16", "Allah mengetahui setiap perkara, walaupun sebesar biji sawi"],
                                                    ["31:17", "Solat, menyuruh kebaikan dan sabar"], ["31:18–19", "Akhlak: tidak sombong, sederhana berjalan dan merendahkan suara"]])),
        ("umur", "Panduan Mengikut Umur",
         table(["Umur", "Fokus", "Aktiviti harian"], [
             ["0–3 tahun", "Mendengar nama Allah", "Zikir dan selawat ketika mendodoi, bacakan surah pendek, sebut “Bismillah” sebelum makan"],
             ["4–6 tahun", "Mengenal Allah melalui ciptaan dan cerita", "Kisah nabi sebelum tidur, tanya “Siapa yang cipta hujan?”, hafal Al-Fatihah dan tiga Qul"],
             ["7–9 tahun", "Rukun iman, rukun Islam dan solat", "Ajak solat bersama, terangkan maksud bacaan, tunjukkan Allah melihat walaupun tiada orang"],
             ["10–12 tahun", "Hujah dan soalan besar", "Bincang soalan “kenapa”, sebab ada agama lain, makna syirik dan tawakal"]])
         + f'<p>Panduan solat ikut umur: <a href="{SOLAT_ANAK}">Cara Ajar Anak Solat Awal</a>. Kisah untuk dibacakan: <a href="{Q}kisah-nabi/">Kisah 25 Nabi</a>.</p>'),
        ("ibnabbas", "Cara Nabi SAW Mengajar Akidah kepada Kanak-Kanak",
         "<p>Ibn Abbas RA, ketika masih kanak-kanak, membonceng di belakang Nabi SAW lalu Baginda bersabda: “Wahai anak, aku ajarkan kepadamu beberapa kalimat: <strong>jagalah (perintah) Allah, nescaya Allah menjagamu</strong>. "
         "Jika engkau meminta, mintalah kepada Allah; jika engkau memohon pertolongan, mohonlah kepada Allah”" + ref("HR At-Tirmizi, no. 2516; hasan sahih") + ".</p>"
         + ul("Baginda memanggil dengan panggilan mesra (“wahai anak”).", "Mesej pendek dan mudah diingat.", "Diajar ketika bersama dalam aktiviti biasa, bukan dalam kelas formal.")),
        ("elak", "Perkara yang Perlu Dielakkan",
         ul("Menakut-nakutkan anak dengan neraka sahaja; seimbangkan dengan kasih sayang dan syurga.", "Mengancam “Allah marah” untuk setiap kesalahan kecil.",
            "Kepercayaan khurafat seperti hantu tertentu, angka sial atau tangkal.", "Memarahi soalan; soalan tentang Allah ialah peluang mengajar."),
         ),
        ("doa", "Doa Ibu Bapa untuk Anak",
         qcard(P, "Ibrahim 14:40", 14, 40, 40, "Surah Ibrahim, ayat 40")
         + f'<p>Doa lengkap: <a href="{DOA_ANAK}">Doa Anak Soleh & Solehah</a>.</p>'),
    ],
    faq=[("Bagaimana cara menanam akidah pada anak?", "Secara berperingkat: zikir dan nama Allah sejak bayi, cerita ciptaan dan kisah nabi pada usia 4–6, rukun iman dan solat pada 7 tahun (HR Abu Daud 495), dan perbincangan hujah pada usia 10 ke atas."),
         ("Apakah wasiat Luqman kepada anaknya?", "Jangan syirik, berbuat baik kepada ibu bapa, Allah mengetahui segala-galanya, dirikan solat dan sabar, serta jangan sombong (Luqman 31:13–19)."),
         ("Bilakah anak perlu diajar solat?", "Disuruh solat ketika berumur 7 tahun dan ditegaskan pada usia 10 tahun (HR Abu Daud 495)."),
         ("Apakah hadis tentang fitrah anak?", "Setiap anak dilahirkan dalam keadaan fitrah, ibu bapanyalah yang membentuknya (HR Al-Bukhari 1385).")],
    refs=["Al-Quran: Luqman 31:13–19; Ibrahim 14:40.", "Sahih Al-Bukhari, no. 1385.", "Sunan At-Tirmizi, no. 2516; Sunan Abu Daud, no. 495."],
    related=[(SOLAT_ANAK, "Cara Ajar Anak Solat Awal", "Panduan ikut umur 2–10 tahun"), (DOA_ANAK, "Doa Anak Soleh & Solehah", "Doa ibu bapa untuk anak"),
             (Q + "kisah-nabi/", "Kisah 25 Nabi", "Kisah untuk dibacakan kepada anak")])))

# 14 --------------------------------------------------------------- Kalimah disukai & dibenci Allah
P = "ilmx-kd"
POSTS.append(("kalimah-dibenci", b4(
    ns=P, url=U["kalimah-dibenci"], published="2018-02-08", pubms="8 Februari 2018",
    title="Kalimah Paling Disukai & Dibenci Allah: 'Urus Diri Sendiri' (Hadis)",
    desc="Perkataan yang paling disukai dan paling dibenci Allah menurut hadis, termasuk menjawab nasihat 'bertakwalah' dengan 'urus diri kamu sendiri'.",
    h1="Kalimah Paling Disukai & Dibenci Allah",
    img=img("kalimah-dibenci-allah", "Adab Lisan", "Kalimah Disukai & Dibenci Allah", "Menurut hadis dan atsar sahabat", "اتَّقِ اللّٰهَ"),
    alt="Kalimah yang paling disukai dan dibenci Allah", refshort="Sahih Muslim, Sunan An-Nasa'i Al-Kubra",
    lead="Kalimah yang disebut Nabi SAW dan sahabat sebagai paling dicintai Allah, satu jawapan yang disebut paling dibenci-Nya, dan perkataan lain yang perlu dijaga.",
    crumb=("Akhlak", W + "search/label/Akhlak"), about=["Adab lisan", "Zikir"],
    answer="Abdullah bin Mas'ud RA berkata: perkataan yang paling disukai Allah ialah apabila hamba berkata <strong>“Subhanakallahumma wa bihamdik, wa tabarakasmuk, wa ta'ala jadduk, wa la ilaha ghairuk”</strong>, "
           "dan <strong>perkataan yang paling dibenci Allah</strong> ialah apabila seseorang dinasihati “Bertakwalah kepada Allah”, lalu dia menjawab <strong>“Urus diri kamu sendiri”</strong> <em>(riwayat An-Nasa'i dalam As-Sunan Al-Kubra; dinilai sahih)</em>. "
           "Nabi SAW juga bersabda kalimah paling dicintai Allah ialah <strong>“Subhanallahi wa bihamdih”</strong> <em>(HR Muslim, no. 2731)</em>.",
    sections=[
        ("disukai", "Kalimah yang Paling Disukai Allah",
         dc(P, "Subhanallahi wa bihamdih", "سُبْحَانَ اللّٰهِ وَبِحَمْدِهِ", "Subhanallahi wa bihamdih.", "Maha Suci Allah dan dengan memuji-Nya.", "HR Muslim, no. 2731: “Kalimah yang paling dicintai Allah”")
         + dc(P, "Doa iftitah pendek", "سُبْحَانَكَ اللّٰهُمَّ وَبِحَمْدِكَ، وَتَبَارَكَ اسْمُكَ، وَتَعَالَى جَدُّكَ، وَلَا إِلٰهَ غَيْرُكَ",
              "Subhanakallahumma wa bihamdik, wa tabarakasmuk, wa ta'ala jadduk, wa la ilaha ghairuk.",
              "Maha Suci Engkau ya Allah dan dengan memuji-Mu, Maha Berkat nama-Mu, Maha Tinggi kebesaran-Mu, dan tiada tuhan selain-Mu.",
              "Atsar Ibn Mas'ud (An-Nasa'i, As-Sunan Al-Kubra); bacaan iftitah dalam HR Abu Daud, no. 775")
         + "<p>Empat kalimah “Subhanallah, walhamdulillah, wa la ilaha illallah, wallahu akbar” juga disebut sebagai kalimah paling dicintai Allah" + ref("HR Muslim, no. 2137") + ".</p>"),
        ("dibenci", "Jawapan yang Paling Dibenci Allah",
         "<p>Dalam atsar yang sama, Ibn Mas'ud RA berkata perkataan yang paling dibenci Allah ialah seseorang berkata kepada saudaranya “Ittaqillah” (bertakwalah kepada Allah), lalu dia menjawab “<strong>'Alaika binafsik</strong>” (urus diri kamu sendiri). "
         "Ulama menjelaskan sebabnya: jawapan itu menolak peringatan tentang Allah dengan sombong.</p>"
         + "<p>Allah menyebut sifat ini pada orang munafik: “Apabila dikatakan kepadanya: bertakwalah kepada Allah, bangkitlah kesombongannya untuk berbuat dosa”" + ref("Al-Baqarah 2:206") + ".</p>"
         + f'<div class="{P}-box amber">Ini tidak bermaksud kita mesti menerima setiap teguran kasar. Teguran boleh dijawab dengan adab. Yang dicela ialah menolak peringatan tentang Allah kerana sombong.</div>'),
        ("lain", "Perkataan Lain yang Perlu Dijaga",
         table(["Perkataan", "Dalil"], [
             ["Satu kalimah yang dimurkai Allah, diucapkan tanpa difikirkan, boleh menjerumuskan ke neraka", "HR Al-Bukhari, no. 6478"],
             ["Melaknat dan mencela tidak termasuk sifat orang beriman", "HR At-Tirmizi, no. 1977"],
             ["Mengumpat: menyebut saudaramu dengan apa yang dia tidak suka", "HR Muslim, no. 2589"],
             ["Bersumpah dengan nama selain Allah", "HR Al-Bukhari, no. 6646"],
             ["Mencela masa: Allah berfirman, “Akulah masa”", "HR Al-Bukhari, no. 4826"]])),
        ("amal", "Cara Menjaga Lidah",
         ul("“Sesiapa yang beriman kepada Allah dan hari akhirat, hendaklah dia berkata baik atau diam”" + ref("HR Al-Bukhari, no. 6018"), "Biasakan lidah dengan Subhanallahi wa bihamdih ketika terdiam.",
            "Apabila ditegur tentang agama, jawab “Jazakallahu khairan” walaupun tidak bersetuju sepenuhnya.")
         + f'<p>Zikir harian dengan kaunter: <a href="{Q}tasbih-digital/">Tasbih Digital</a>.</p>'),
    ],
    faq=[("Apakah kalimah yang paling disukai Allah?", "Subhanallahi wa bihamdih (HR Muslim 2731), dan empat kalimah: Subhanallah, walhamdulillah, wa la ilaha illallah, wallahu akbar (HR Muslim 2137)."),
         ("Apakah perkataan yang paling dibenci Allah?", "Menurut atsar Ibn Mas'ud RA, apabila seseorang dinasihati “bertakwalah kepada Allah”, lalu dia menjawab “urus diri kamu sendiri”."),
         ("Apakah dalil larangan menolak nasihat dengan sombong?", "Al-Baqarah 2:206: apabila dikatakan kepadanya bertakwalah kepada Allah, bangkitlah kesombongannya."),
         ("Apakah bacaan Subhanakallahumma wa bihamdik?", "Subhanakallahumma wa bihamdik, wa tabarakasmuk, wa ta'ala jadduk, wa la ilaha ghairuk. Ia juga bacaan iftitah yang diriwayatkan Abu Daud (775).")],
    refs=["Sahih Muslim, no. 2137, 2589, 2731.", "Sahih Al-Bukhari, no. 4826, 6018, 6478, 6646.", "An-Nasa'i, As-Sunan Al-Kubra, kitab 'Amal Al-Yaum wal-Lailah (atsar Ibn Mas'ud).",
          "Sunan Abu Daud, no. 775; Sunan At-Tirmizi, no. 1977.", "Al-Quran: Al-Baqarah 2:206."],
    related=[(U["amalan-pahala-besar"], "Amalan Ringan Pahala Besar", "10 zikir dan amalan seminit"), (Q + "tasbih-digital/", "Tasbih Digital", "Kaunter zikir"),
             (U["keras-hati"], "Keras Hati", "Tanda dan cara melembutkan hati")])))

# 15 --------------------------------------------------------------- Doa berlindung daripada syirik
P = "ilmx-ds"
POSTS.append(("doa-syirik", b4(
    ns=P, url=U["doa-syirik"], published="2018-01-17", pubms="17 Januari 2018",
    title="Doa Berlindung Daripada Syirik: Bacaan Rumi, Maksud & Syirik Kecil",
    desc="Doa berlindung daripada syirik yang diajar Nabi SAW (Arab, Rumi, maksud), statusnya, maksud syirik kecil seperti riak, dan bila doa ini dibaca setiap hari.",
    h1="Doa Berlindung Daripada Syirik",
    img=img("doa-berlindung-syirik", "Doa Sahih", "Doa Berlindung Daripada Syirik", "Bacaan, maksud & syirik kecil", "أَعُوذُ بِكَ أَنْ أُشْرِكَ بِكَ"),
    alt="Doa berlindung daripada syirik: bacaan dan maksud", refshort="Al-Adab Al-Mufrad, Musnad Ahmad",
    lead="Doa yang diajar Nabi SAW untuk perlindungan daripada syirik yang disedari dan yang tidak disedari, berserta penjelasan syirik kecil yang lebih halus daripada langkah semut.",
    crumb=("Doa", W + "search/label/Doa"), about=["Doa berlindung daripada syirik", "Syirik kecil"],
    answer="Doa berlindung daripada syirik ialah <strong>“Allahumma inni a'udzu bika an usyrika bika wa ana a'lam, wa astaghfiruka lima la a'lam”</strong>: Ya Allah, aku berlindung kepada-Mu daripada mensyirikkan-Mu sedangkan aku mengetahui, dan aku memohon ampun atas apa yang aku tidak ketahui. "
           "Nabi SAW mengajarnya selepas bersabda bahawa <strong>syirik dalam umat ini lebih halus daripada langkah semut</strong> <em>(HR Al-Bukhari dalam Al-Adab Al-Mufrad, no. 716; sahih)</em>.",
    sections=[
        ("bacaan", "Bacaan Doa Berlindung Daripada Syirik",
         dc(P, "Doa pertama", "اللّٰهُمَّ إِنِّي أَعُوذُ بِكَ أَنْ أُشْرِكَ بِكَ وَأَنَا أَعْلَمُ، وَأَسْتَغْفِرُكَ لِمَا لَا أَعْلَمُ",
            "Allahumma inni a'udzu bika an usyrika bika wa ana a'lam, wa astaghfiruka lima la a'lam.",
            "Ya Allah, aku berlindung kepada-Mu daripada mensyirikkan-Mu sedangkan aku mengetahuinya, dan aku memohon ampun kepada-Mu atas apa yang tidak aku ketahui.",
            "HR Al-Bukhari, Al-Adab Al-Mufrad, no. 716 (sahih)")
         + dc(P, "Doa kedua (lafaz jamak)", "اللّٰهُمَّ إِنَّا نَعُوذُ بِكَ مِنْ أَنْ نُشْرِكَ بِكَ شَيْئًا نَعْلَمُهُ، وَنَسْتَغْفِرُكَ لِمَا لَا نَعْلَمُهُ",
              "Allahumma inna na'udzu bika min an nusyrika bika syai'an na'lamuh, wa nastaghfiruka lima la na'lamuh.",
              "Ya Allah, kami berlindung kepada-Mu daripada mensyirikkan-Mu dengan sesuatu yang kami ketahui, dan kami memohon ampun kepada-Mu atas apa yang tidak kami ketahui.",
              "HR Ahmad, hadis Abu Musa Al-Asy'ari; dinilai hasan")),
        ("kecil", "Syirik Kecil: Lebih Halus daripada Langkah Semut",
         table(["Syirik kecil", "Contoh", "Dalil"], [
             ["Riak", "Beribadah supaya dipuji, memperelok solat apabila dilihat orang", "HR Ahmad, no. 23630: “Yang paling aku takuti ke atas kamu ialah syirik kecil, iaitu riak”"],
             ["Bersumpah dengan selain Allah", "“Demi mak aku”, “sumpah demi nyawa aku”", "HR At-Tirmizi, no. 1535"],
             ["Tathayyur (percaya sial)", "Membatalkan perjalanan kerana burung, nombor atau bunyi", "HR Abu Daud, no. 3910"],
             ["Ucapan “dengan kehendak Allah dan kehendak kamu”", "Menyamakan kehendak makhluk dengan Allah", "HR An-Nasa'i, no. 3773: katakan “dengan kehendak Allah, kemudian kehendak kamu”"],
             ["Memakai tangkal dengan iktikad ia melindungi", "Gelang, azimat, benang", "HR Ahmad, no. 17422"]])
         + f'<p>Syirik besar dan keampunan Allah: <a href="{SYIRIK}">Allah Mengampunkan Segala Dosa Kecuali Syirik</a>.</p>'),
        ("bila", "Bila Doa Ini Dibaca",
         ul("Pagi dan petang bersama zikir harian; Abu Bakar RA diajar membacanya sebagai amalan berterusan.", "Selepas solat dan sebelum memulakan amal yang berisiko riak, seperti berceramah atau bersedekah secara terbuka.",
            "Ketika teringat amalan yang mungkin bercampur dengan niat yang tidak ikhlas.")
         + f'<p>Zikir harian lengkap: <a href="{Q}zikir-pagi-petang/">Zikir Pagi Petang</a>.</p>'),
        ("ayat", "Peringatan Al-Quran tentang Syirik", qcard(P, "Al-Kahf 18:110", 18, 110, 110, "Surah Al-Kahf, ayat 110")),
    ],
    faq=[("Apakah doa berlindung daripada syirik?", "Allahumma inni a'udzu bika an usyrika bika wa ana a'lam, wa astaghfiruka lima la a'lam (HR Al-Bukhari, Al-Adab Al-Mufrad 716)."),
         ("Apakah maksud syirik kecil?", "Perbuatan atau ucapan yang tidak mengeluarkan seseorang daripada Islam tetapi mencacatkan tauhid, seperti riak, bersumpah dengan selain Allah dan percaya sial."),
         ("Adakah riak termasuk syirik?", "Ya, Nabi SAW menyebut riak sebagai syirik kecil, perkara yang paling Baginda takuti ke atas umatnya (HR Ahmad 23630)."),
         ("Bilakah doa berlindung daripada syirik dibaca?", "Pagi dan petang, selepas solat, dan sebelum amal yang mungkin bercampur riak. Tiada bilangan khusus.")],
    refs=["Al-Bukhari, Al-Adab Al-Mufrad, no. 716.", "Musnad Ahmad, no. 17422, 23630, dan hadis Abu Musa Al-Asy'ari.", "Sunan At-Tirmizi, no. 1535; Sunan Abu Daud, no. 3910; Sunan An-Nasa'i, no. 3773.",
          "Al-Quran: Al-Kahf 18:110."],
    related=[(SYIRIK, "Dosa Syirik & Keampunan Allah", "Syirik besar, syirik kecil dan taubat"), (Q + "zikir-pagi-petang/", "Zikir Pagi Petang", "Zikir perlindungan harian"),
             (U["bismillah-5"], "Bismillah 5", "Bacaan, maksud dan status")])))


if __name__ == "__main__":
    write(POSTS)
