"""Content for /haji-umrah/ and its guide pages (tools/pages20.py). Same rules as sunat.py: Quranic text is read from
data-surah/ by reference ("Q:s:a1-a2"), never typed; every hadith-based text carries its book and number, and a weak
(dhaif) narration or a Companion's practice (athar) is labelled as such. Fiqh follows the Syafi'i mazhab as taught in
Malaysian manasik courses (Tabung Haji); where practice depends on the pilgrim's group, the page says to follow the
Tabung Haji / agency briefing instead of guessing. Weights: 1 mud (cupak) = 0.65 kg, 1 sa' (gantang) = 2.6 kg, the same
gantang Baghdad used by /zakat-fitrah/."""

HUB = "haji-umrah/"
MUD_KG = 0.65

# doa cards: (id, title, arabic | "Q:s:a1-a2", rumi, maksud, source, note) -> pages7.doa_cards
TALBIAH = ("talbiah", "Lafaz Talbiah",
           "لَبَّيْكَ اللّٰهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيكَ لَكَ",
           "Labbaikallahumma labbaik, labbaika la syarika laka labbaik, innal-hamda wan-ni'mata laka wal-mulk, la syarika lak.",
           "Aku datang memenuhi panggilan-Mu ya Allah, aku datang memenuhi panggilan-Mu. Aku datang memenuhi panggilan-Mu, tiada sekutu bagi-Mu, aku datang memenuhi panggilan-Mu. "
           "Sesungguhnya segala puji, nikmat dan kerajaan adalah milik-Mu; tiada sekutu bagi-Mu.",
           "HR Al-Bukhari, no. 1549; Muslim, no. 1184 (talbiah Rasulullah SAW)",
           "Lelaki menguatkan suara, wanita memperlahankan suara. Ulang tiga kali setiap kali membacanya.")
TALBIAH_DOA = ("talbiah-doa", "Selepas Talbiah: Selawat & Doa",
               "اللّٰهُمَّ إِنِّي أَسْأَلُكَ رِضَاكَ وَالْجَنَّةَ، وَأَعُوذُ بِكَ مِنْ سَخَطِكَ وَالنَّارِ",
               "Allahumma inni as'aluka ridhaka wal-jannah, wa a'uzu bika min sakhatika wan-nar.",
               "Ya Allah, sesungguhnya aku memohon keredaan-Mu dan syurga, dan aku berlindung dengan-Mu daripada kemurkaan-Mu dan neraka.",
               "Amalan mazhab Syafi'i selepas talbiah (selawat, kemudian doa ini); riwayat Al-Baihaqi daripada Khuzaimah bin Thabit, sanadnya dhaif",
               "Didahului selawat ke atas Nabi SAW. Boleh juga berdoa dengan apa-apa hajat.")

NIAT = {
    "umrah": ("niat-umrah", "Niat Ihram Umrah", "نَوَيْتُ الْعُمْرَةَ وَأَحْرَمْتُ بِهَا لِلّٰهِ تَعَالَى",
              "Nawaitul-'umrata wa ahramtu biha lillahi ta'ala.", "Sahaja aku berniat umrah dan aku berihram dengannya kerana Allah Taala.",
              "Lafaz lazim di Malaysia (mazhab Syafi'i); niat di dalam hati ialah rukun, melafazkannya sunat",
              "Niat sebelum melintasi miqat. Rasulullah SAW juga menyebut “Labbaika 'umratan” (HR Muslim, no. 1251)."),
    "haji": ("niat-haji", "Niat Ihram Haji (Ifrad atau Tamattu')", "نَوَيْتُ الْحَجَّ وَأَحْرَمْتُ بِهِ لِلّٰهِ تَعَالَى",
             "Nawaitul-hajja wa ahramtu bihi lillahi ta'ala.", "Sahaja aku berniat haji dan aku berihram dengannya kerana Allah Taala.",
             "Lafaz lazim di Malaysia (mazhab Syafi'i); niat di dalam hati ialah rukun",
             "Haji tamattu': berniat pada 8 Zulhijjah dari tempat penginapan di Makkah. Haji ifrad: dari miqat."),
    "qiran": ("niat-qiran", "Niat Ihram Haji Qiran (Haji dan Umrah Serentak)", "نَوَيْتُ الْحَجَّ وَالْعُمْرَةَ وَأَحْرَمْتُ بِهِمَا لِلّٰهِ تَعَالَى",
              "Nawaitul-hajja wal-'umrata wa ahramtu bihima lillahi ta'ala.", "Sahaja aku berniat haji dan umrah dan aku berihram dengan kedua-duanya kerana Allah Taala.",
              "Lafaz lazim di Malaysia; asalnya talbiah Rasulullah SAW “Labbaika 'umratan wa hajjan” (HR Muslim, no. 1251)", ""),
    "isytirat": ("isytirat", "Niat Bersyarat (Isytirat)", "اللّٰهُمَّ مَحِلِّي حَيْثُ حَبَسْتَنِي",
                 "Allahumma mahilli haithu habastani.", "Ya Allah, tempat aku bertahallul ialah di mana Engkau menahanku (kerana sakit atau halangan).",
                 "HR Al-Bukhari, no. 5089; Muslim, no. 1207 (Dhuba'ah binti Az-Zubair yang sakit)",
                 "Disebut selepas niat oleh orang yang bimbang tidak dapat menyempurnakan ibadah (sakit, uzur, warga emas). Jika terhalang, dia bertahallul tanpa dam menurut mazhab Syafi'i."),
    "badal-haji": ("niat-badal-haji", "Niat Ihram Badal Haji", "نَوَيْتُ الْحَجَّ عَنْ فُلَانٍ وَأَحْرَمْتُ بِهِ لِلّٰهِ تَعَالَى",
                   "Nawaitul-hajja 'an (sebut nama) wa ahramtu bihi lillahi ta'ala.", "Sahaja aku berniat haji bagi pihak (nama) dan aku berihram dengannya kerana Allah Taala.",
                   "Lafaz lazim di Malaysia; asasnya talbiah “Labbaika 'an Syubrumah” (HR Abu Daud, no. 1811)", "Ganti “fulan” dengan nama penuh orang yang dibadalkan (bin/binti bapanya)."),
    "badal-umrah": ("niat-badal-umrah", "Niat Ihram Badal Umrah", "نَوَيْتُ الْعُمْرَةَ عَنْ فُلَانٍ وَأَحْرَمْتُ بِهَا لِلّٰهِ تَعَالَى",
                    "Nawaitul-'umrata 'an (sebut nama) wa ahramtu biha lillahi ta'ala.", "Sahaja aku berniat umrah bagi pihak (nama) dan aku berihram dengannya kerana Allah Taala.",
                    "Lafaz lazim di Malaysia (mazhab Syafi'i)", ""),
}
NIAT_SOLAT_IHRAM = ("niat-solat-ihram", "Niat Solat Sunat Ihram", "أُصَلِّي سُنَّةَ الْإِحْرَامِ رَكْعَتَيْنِ لِلّٰهِ تَعَالَى",
                    "Usolli sunnatal-ihrami rak'ataini lillahi ta'ala.", "Sahaja aku solat sunat ihram dua rakaat kerana Allah Taala.",
                    "Sunat dalam mazhab Syafi'i sebelum berniat ihram (Rasulullah SAW solat di Zulhulaifah, HR Muslim, no. 1184)",
                    "Rakaat pertama Al-Kafirun, rakaat kedua Al-Ikhlas. Tidak dilakukan pada waktu dilarang solat; jika baru selesai solat fardu, ia memadai.")

TAWAF = [
    ("istilam", "Ketika Isyarat ke Hajarul Aswad", "بِسْمِ اللّٰهِ وَاللّٰهُ أَكْبَرُ", "Bismillahi wallahu akbar.", "Dengan nama Allah, dan Allah Maha Besar.",
     "Takbir ketika isyarat ke Hajarul Aswad: HR Al-Bukhari, no. 1613. Tambahan “Bismillah” amalan Ibn Umar (HR Al-Baihaqi, mauquf sahih)",
     "Dibaca pada permulaan setiap pusingan sambil mengangkat tangan kanan ke arah Hajarul Aswad (isyarat). Tidak perlu berasak untuk mengucupnya."),
    ("rukun-yamani", "Antara Rukun Yamani dan Hajarul Aswad", "Q:2:201", "", "",
     "HR Abu Daud, no. 1892 (Abdullah bin As-Sa'ib: Rasulullah SAW membacanya di antara dua rukun)",
     "Selain bahagian ini, tiada doa khusus yang thabit bagi setiap pusingan; berdoa, berzikir atau membaca Al-Quran dengan apa-apa bahasa."),
    ("maqam", "Menuju Maqam Ibrahim", "Q:2:125", "", "",
     "HR Muslim, no. 1218 (Rasulullah SAW membaca “wattakhizu min maqami Ibrahima musolla” selepas tawaf)",
     "Kemudian solat sunat tawaf dua rakaat di belakang Maqam Ibrahim jika mudah, atau di mana-mana dalam masjid: Al-Kafirun dan Al-Ikhlas (HR Muslim, no. 1218)."),
]
SAIE = [
    ("safa", "Ketika Mendaki Bukit Safa (Kali Pertama)", "Q:2:158", "", "",
     "HR Muslim, no. 1218: Rasulullah SAW membaca ayat ini, kemudian bersabda “Abda'u bima bada'allahu bih” (aku mulakan dengan apa yang Allah mulakan)",
     "Ayat ini dibaca sekali sahaja, ketika menghampiri Safa pada permulaan sa'ie."),
    ("zikir-safa", "Zikir di Atas Safa dan Marwah",
     "اللّٰهُ أَكْبَرُ، اللّٰهُ أَكْبَرُ، اللّٰهُ أَكْبَرُ. لَا إِلٰهَ إِلَّا اللّٰهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ، "
     "لَا إِلٰهَ إِلَّا اللّٰهُ وَحْدَهُ، أَنْجَزَ وَعْدَهُ، وَنَصَرَ عَبْدَهُ، وَهَزَمَ الْأَحْزَابَ وَحْدَهُ",
     "Allahu akbar, Allahu akbar, Allahu akbar. La ilaha illallahu wahdahu la syarika lah, lahul-mulku wa lahul-hamd, wa huwa 'ala kulli syai'in qadir. "
     "La ilaha illallahu wahdah, anjaza wa'dah, wa nasara 'abdah, wa hazamal-ahzaba wahdah.",
     "Allah Maha Besar (3 kali). Tiada tuhan melainkan Allah Yang Maha Esa, tiada sekutu bagi-Nya; bagi-Nya kerajaan dan bagi-Nya segala puji, dan Dia Maha Berkuasa atas segala sesuatu. "
     "Tiada tuhan melainkan Allah Yang Maha Esa; Dia menunaikan janji-Nya, menolong hamba-Nya dan mengalahkan golongan bersekutu dengan sendiri-Nya.",
     "HR Muslim, no. 1218 (dibaca tiga kali sambil menghadap Kaabah, diselangi doa)",
     "Dibaca di atas Safa dan di atas Marwah setiap kali sampai, menghadap ke arah Kaabah sambil mengangkat tangan berdoa."),
    ("lampu-hijau", "Di Antara Dua Lampu Hijau", "رَبِّ اغْفِرْ وَارْحَمْ، إِنَّكَ أَنْتَ الْأَعَزُّ الْأَكْرَمُ",
     "Rabbighfir warham, innaka antal-a'azzul-akram.", "Wahai Tuhanku, ampunilah dan rahmatilah; sesungguhnya Engkau Yang Maha Perkasa lagi Maha Mulia.",
     "Athar Ibn Mas'ud dan Ibn Umar (Ibn Abi Syaibah), bukan sabda Nabi SAW. Berlari-lari anak di kawasan ini thabit dalam HR Muslim, no. 1218",
     "Lelaki berlari-lari anak di antara dua lampu hijau; wanita berjalan biasa."),
]
ARAFAH = ("doa-arafah", "Doa Terbaik pada Hari Arafah",
          "لَا إِلٰهَ إِلَّا اللّٰهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
          "La ilaha illallahu wahdahu la syarika lah, lahul-mulku wa lahul-hamd, wa huwa 'ala kulli syai'in qadir.",
          "Tiada tuhan melainkan Allah Yang Maha Esa, tiada sekutu bagi-Nya; bagi-Nya kerajaan dan bagi-Nya segala puji, dan Dia Maha Berkuasa atas segala sesuatu.",
          "HR At-Tirmizi, no. 3585 (hasan): “Sebaik-baik doa ialah doa hari Arafah, dan sebaik-baik yang aku dan para nabi sebelumku ucapkan ialah…”",
          "Perbanyakkan zikir ini, istighfar, selawat dan doa dengan bahasa sendiri dari tergelincir matahari hingga terbenam.")
MELONTAR = ("takbir-lontar", "Ketika Melontar Jamrah", "اللّٰهُ أَكْبَرُ", "Allahu akbar.", "Allah Maha Besar.",
            "HR Al-Bukhari, no. 1751 (bertakbir pada setiap lontaran; selepas Jamrah Ula dan Wusta berdiri menghadap kiblat dan berdoa panjang)",
            "Satu takbir bagi setiap biji batu, tujuh biji bagi setiap jamrah.")
ZIARAH_SALAM = ("salam-nabi", "Salam kepada Rasulullah SAW, Abu Bakar dan Umar",
                "السَّلَامُ عَلَيْكَ يَا رَسُولَ اللّٰهِ، السَّلَامُ عَلَيْكَ يَا أَبَا بَكْرٍ، السَّلَامُ عَلَيْكَ يَا عُمَرُ",
                "Assalamu 'alaika ya Rasulallah. Assalamu 'alaika ya Aba Bakr. Assalamu 'alaika ya 'Umar.",
                "Salam sejahtera ke atasmu wahai Rasulullah. Salam sejahtera ke atasmu wahai Abu Bakar. Salam sejahtera ke atasmu wahai Umar.",
                "Amalan Ibn Umar setiap kali pulang dari musafir (Al-Muwatta'; Al-Baihaqi, mauquf sahih)",
                "Ucapkan dengan suara perlahan dan beradab. Doa dipanjatkan kepada Allah sambil menghadap kiblat, bukan kepada makam.")

# cara umrah: (id, step name, what to do) -> also the HowTo steps
UMRAH_STEPS = [
    ("persiapan", "Bersiap sebelum miqat", "Potong kuku dan rapikan rambut, mandi sunat ihram, pakai wangian pada badan (bukan pada kain ihram). Lelaki memakai dua helai kain ihram tidak berjahit dan selipar yang menampakkan buku lali; wanita memakai pakaian biasa yang menutup aurat kecuali muka dan tapak tangan."),
    ("miqat", "Solat sunat ihram dan niat di miqat", "Solat sunat ihram dua rakaat jika bukan waktu dilarang, kemudian berniat ihram umrah sebelum melintasi miqat (dalam pesawat, apabila diumumkan). Selepas niat, semua larangan ihram berkuat kuasa."),
    ("talbiah", "Bertalbiah sepanjang perjalanan", "Baca talbiah berulang kali dari miqat hingga tiba di Masjidil Haram. Lelaki menguatkan suara, wanita perlahan. Berhenti bertalbiah apabila memulakan tawaf."),
    ("masuk", "Masuk Masjidil Haram", "Masuk dengan kaki kanan dan membaca doa masuk masjid. Tawaf umrah menggantikan solat tahiyatul masjid."),
    ("tawaf", "Tawaf 7 pusingan", "Dalam keadaan berwuduk, mulakan di garisan Hajarul Aswad dengan Kaabah di sebelah kiri. Isyarat dan bertakbir pada setiap pusingan. Lelaki melakukan idtiba' (bahu kanan terdedah) sepanjang tawaf dan berlari-lari anak (ramal) pada tiga pusingan pertama."),
    ("solat-tawaf", "Solat sunat tawaf dan minum zamzam", "Tutup semula bahu kanan, solat dua rakaat di belakang Maqam Ibrahim atau di mana-mana dalam masjid, kemudian minum air zamzam dan berdoa."),
    ("saie", "Sa'ie 7 kali antara Safa dan Marwah", "Mula di Safa dan berakhir di Marwah: Safa ke Marwah dikira satu, Marwah ke Safa dikira dua, dan seterusnya hingga tujuh. Wuduk tidak wajib tetapi sunat. Lelaki berlari-lari anak di antara dua lampu hijau."),
    ("tahallul", "Tahallul: bercukur atau bergunting", "Selepas sa'ie, lelaki bercukur (lebih afdal) atau menggunting sekurang-kurangnya tiga helai rambut; wanita memotong hujung rambut sepanjang hujung jari. Umrah selesai dan semua larangan ihram terangkat."),
]

# cara haji, by day of Zulhijjah (day, name, steps html-free text, hukum)
HAJI_DAYS = [
    (0, "Sebelum 8 Zulhijjah", "Haji tamattu': tunaikan umrah dan bertahallul, kemudian tinggal di Makkah tanpa ihram. Haji ifrad dan qiran: kekal dalam ihram; sunat tawaf qudum, dan boleh terus melakukan sa'ie haji selepasnya.", "Persediaan"),
    (8, "8 Zulhijjah (Hari Tarwiyah)", "Jemaah tamattu' berniat ihram haji dari tempat penginapan. Sunat ke Mina dan bermalam di sana; Tabung Haji lazimnya membawa jemaah Malaysia terus ke Arafah pada hari ini untuk mengelakkan kesesakan.", "Sunat (bermalam di Mina)"),
    (9, "9 Zulhijjah (Hari Arafah)", "Wukuf di Arafah dari tergelincir matahari hingga terbit fajar 10 Zulhijjah; memadai berada di Arafah sesaat dalam tempoh ini. Solat Zohor dan Asar jamak taqdim dan qasar. Perbanyakkan doa hingga matahari terbenam, kemudian bergerak ke Muzdalifah.", "Rukun (wukuf)"),
    (10, "Malam 10 Zulhijjah (Muzdalifah)", "Solat Maghrib dan Isyak jamak takhir. Bermalam di Muzdalifah (memadai berada di sana seketika selepas separuh malam) dan kutip batu sebesar biji kacang kuda: 7 untuk Jamrah Aqabah, atau 49/70 untuk semua hari melontar.", "Wajib (bermalam)"),
    (10, "10 Zulhijjah (Hari Raya Aidiladha / Hari Nahar)", "Melontar Jamrah Aqabah 7 biji. Sembelih dam tamattu' atau qiran. Bercukur atau bergunting. Tawaf ifadah dan sa'ie haji (jika belum). Selepas dua daripada tiga perkara (melontar, bercukur, tawaf ifadah) jemaah mencapai tahallul awal; selepas ketiga-tiganya, tahallul thani.", "Wajib (melontar) · Rukun (bercukur, tawaf ifadah, sa'ie)"),
    (11, "11 dan 12 Zulhijjah (Hari Tasyrik)", "Selepas tergelincir matahari, melontar ketiga-tiga jamrah mengikut tertib: Ula, Wusta, kemudian Aqabah, 7 biji setiap satu. Bermalam di Mina (lebih separuh malam). Nafar awal: keluar dari Mina sebelum matahari terbenam pada 12 Zulhijjah.", "Wajib"),
    (13, "13 Zulhijjah (Nafar Thani)", "Bagi yang masih di Mina selepas matahari terbenam 12 Zulhijjah: bermalam dan melontar tiga jamrah pada 13 Zulhijjah, kemudian meninggalkan Mina.", "Wajib (jika belum keluar)"),
    (14, "Sebelum pulang", "Tawaf wada' (tawaf selamat tinggal) sebagai urusan terakhir di Makkah. Wanita haid dan nifas dikecualikan.", "Wajib"),
]

RUKUN_HAJI = [("Niat ihram", "Berniat haji dalam bulan haji (Syawal hingga sebelum fajar 10 Zulhijjah)"),
              ("Wukuf di Arafah", "Berada di Arafah antara tergelincir matahari 9 Zulhijjah hingga terbit fajar 10 Zulhijjah"),
              ("Tawaf ifadah", "Tujuh pusingan, bermula selepas separuh malam 10 Zulhijjah; tiada had akhir"),
              ("Sa'ie", "Tujuh kali antara Safa dan Marwah selepas tawaf yang sah (jika belum selepas tawaf qudum)"),
              ("Bercukur atau bergunting", "Sekurang-kurangnya tiga helai rambut, selepas separuh malam 10 Zulhijjah"),
              ("Tertib", "Mengikut susunan bagi kebanyakan rukun: niat dahulu, wukuf sebelum tawaf ifadah dan bercukur")]
RUKUN_UMRAH = [("Niat ihram", "Berniat umrah; boleh pada bila-bila masa sepanjang tahun"), ("Tawaf", "Tujuh pusingan mengelilingi Kaabah"),
               ("Sa'ie", "Tujuh kali antara Safa dan Marwah selepas tawaf"), ("Bercukur atau bergunting", "Sekurang-kurangnya tiga helai rambut"),
               ("Tertib", "Mengikut susunan di atas")]
WAJIB_HAJI = [("Berihram dari miqat", "Dam kambing (tartib dan taqdir)"), ("Bermalam di Muzdalifah (malam 10 Zulhijjah)", "Dam kambing (tartib dan taqdir)"),
              ("Melontar Jamrah Aqabah pada 10 Zulhijjah", "Dam kambing jika tidak dilontar hingga akhir hari tasyrik"),
              ("Melontar tiga jamrah pada hari tasyrik", "Dam kambing jika 3 biji batu atau lebih ditinggalkan; secupak (1 mud) bagi sebiji, dua cupak bagi dua biji"),
              ("Bermalam di Mina pada malam-malam tasyrik", "Dam kambing jika ditinggalkan semua; secupak bagi satu malam, dua cupak bagi dua malam"),
              ("Tawaf wada'", "Dam kambing (gugur bagi wanita haid atau nifas)"), ("Menjauhi larangan ihram", "Dam mengikut jenis larangan (lihat Larangan Ihram)")]
WAJIB_UMRAH = [("Berihram dari miqat", "Dam kambing (tartib dan taqdir)"), ("Menjauhi larangan ihram", "Dam mengikut jenis larangan")]
SYARAT_WAJIB = [("Islam", ""), ("Baligh", "Haji kanak-kanak sah tetapi tidak menggugurkan haji fardu apabila dewasa (HR Muslim, no. 1336)"), ("Berakal", ""), ("Merdeka", ""),
                ("Berkemampuan (istita'ah)", "Belanja perjalanan dan sara hidup keluarga yang ditinggalkan, kesihatan, keselamatan perjalanan, dan bagi wanita: suami, mahram atau rombongan wanita yang dipercayai")]

# dam (Syafi'i): key -> (name, what triggers it, how to pay)
DAM = {
    "tt": ("Dam tartib dan taqdir", "Wajib menyembelih seekor kambing; jika tidak mampu, berpuasa 10 hari: 3 hari semasa dalam ihram haji (sebaik-baiknya sebelum Hari Arafah) dan 7 hari selepas pulang ke tanah air (Al-Baqarah 2:196).",
           "Haji tamattu' dan qiran; meninggalkan wajib haji (ihram dari miqat, bermalam di Muzdalifah atau Mina, melontar, tawaf wada')."),
    "kt": ("Dam takhyir dan taqdir", f"Pilih salah satu: menyembelih seekor kambing, ATAU bersedekah 3 gantang (kira-kira {3 * 4 * MUD_KG:.1f} kg) makanan asasi kepada 6 orang miskin Tanah Haram (setengah gantang seorang), ATAU berpuasa 3 hari.",
           "Melanggar larangan ihram yang bersifat bersenang-senang: bercukur atau memotong 3 helai rambut atau lebih, memotong kuku 3 atau lebih, memakai pakaian berjahit (lelaki), menutup kepala (lelaki) atau muka (wanita), memakai wangian atau minyak rambut, bercumbu dengan syahwat, bersetubuh selepas tahallul awal."),
    "td": ("Dam tartib dan ta'dil", "Menyembelih seekor unta; jika tidak mampu, seekor lembu; jika tidak mampu, 7 ekor kambing; jika tidak mampu, bersedekah makanan senilai harga unta; jika tidak mampu, berpuasa sehari bagi setiap cupak (mud) makanan itu.",
           "Bersetubuh sebelum tahallul awal: haji (atau umrah) rosak, wajib diteruskan hingga selesai dan diqada pada tahun berikutnya. Bagi ihsar (terhalang daripada menyempurnakan ibadah): seekor kambing, jika tidak mampu makanan senilainya, kemudian puasa."),
    "kd": ("Dam takhyir dan ta'dil", "Pilih salah satu: menyembelih binatang ternakan yang setara, ATAU bersedekah makanan senilai harganya, ATAU berpuasa sehari bagi setiap cupak (mud) makanan itu.",
           "Memburu atau membunuh binatang buruan darat yang halal dimakan, dan memotong pokok di Tanah Haram (Makkah)."),
}
# larangan ihram for the checker: (key, label, who, dam key or "", detail)
LARANGAN = [
    ("baju", "Memakai pakaian berjahit atau bersarung badan (baju, seluar, seluar dalam, stokin)", "Lelaki", "kt", "Tali pinggang, jam tangan, cermin mata dan beg sandang dibenarkan."),
    ("kepala", "Menutup kepala dengan sesuatu yang melekat (kopiah, serban, tuala)", "Lelaki", "kt", "Berteduh di bawah payung atau bumbung tidak mengapa."),
    ("muka", "Menutup muka atau memakai sarung tangan", "Wanita", "kt", "Larangan purdah dan sarung tangan bagi wanita berihram: HR Al-Bukhari, no. 1838."),
    ("wangi", "Memakai wangian pada badan atau pakaian (termasuk sabun dan losyen berwangi)", "Lelaki dan wanita", "kt", "Wangian yang dipakai sebelum niat ihram dan masih berbau tidak mengapa."),
    ("minyak", "Meminyakkan rambut kepala atau janggut", "Lelaki dan wanita", "kt", "Minyak pada kulit badan selain kepala dan janggut dibenarkan jika tidak berwangi."),
    ("rambut", "Mencukur, memotong atau mencabut rambut dan bulu (3 helai atau lebih)", "Lelaki dan wanita", "kt", "Satu helai: 1 cupak makanan; dua helai: 2 cupak; tiga helai atau lebih: dam penuh. Yang gugur sendiri tanpa sengaja tidak dikenakan dam."),
    ("kuku", "Memotong kuku (3 atau lebih)", "Lelaki dan wanita", "kt", "Satu kuku: 1 cupak; dua: 2 cupak; tiga atau lebih: dam penuh."),
    ("buruan", "Memburu atau membunuh binatang buruan darat yang halal dimakan", "Lelaki dan wanita", "kd", "Al-Ma'idah 5:95. Binatang perosak seperti tikus, kala jengking dan anjing gila boleh dibunuh (HR Al-Bukhari, no. 1829)."),
    ("pokok", "Memotong atau mencabut pokok di Tanah Haram", "Semua orang di Tanah Haram", "kd", "Larangan ini kerana Tanah Haram, bukan kerana ihram (HR Al-Bukhari, no. 1834)."),
    ("nikah", "Berkahwin, mengahwinkan orang lain atau menjadi wali", "Lelaki dan wanita", "", "Akad nikah tidak sah dan berdosa, tetapi tiada dam (HR Muslim, no. 1409)."),
    ("cumbu", "Bercumbu atau bersentuhan dengan syahwat", "Lelaki dan wanita", "kt", "Dam dikenakan jika bercumbu dengan syahwat walaupun tidak keluar mani."),
    ("jimak1", "Bersetubuh sebelum tahallul awal", "Lelaki dan wanita", "td", "Haji atau umrah rosak tetapi wajib diteruskan, diqada segera, dan dam seekor unta."),
    ("jimak2", "Bersetubuh selepas tahallul awal (sebelum tahallul thani)", "Lelaki dan wanita", "kt", "Haji tidak rosak; dam seekor kambing."),
    ("tamattu", "Melakukan haji tamattu' atau qiran (bukan kesalahan)", "Jemaah tamattu' / qiran", "tt", "Dam nusuk, bukan denda. Asasnya Al-Baqarah 2:196."),
    ("miqat", "Melintasi miqat tanpa berniat ihram", "Lelaki dan wanita", "tt", "Gugur jika kembali ke miqat untuk berniat sebelum memulakan apa-apa amalan (tawaf)."),
    ("wajib", "Tidak bermalam di Muzdalifah/Mina, tidak melontar, atau tidak tawaf wada'", "Jemaah haji", "tt", "Uzur syarie (sakit, menjaga orang sakit, petugas) boleh menggugurkan dam bagi bermalam; rujuk pembimbing ibadah."),
]

# 5 miqat makani (HR Al-Bukhari, no. 1524; Muslim, no. 1181; Zat 'Irq: HR Abu Daud, no. 1739): (name, today's name, for whom, approx km to Makkah)
MIQAT = [("Zulhulaifah", "Bir Ali (Abyar Ali)", "Penduduk Madinah dan jemaah yang ke Madinah dahulu, termasuk jemaah Malaysia yang memulakan perjalanan di Madinah", "±420 km"),
         ("Al-Juhfah", "Rabigh", "Penduduk Syam, Mesir dan Maghribi; juga laluan pesawat dari arah barat laut", "±186 km"),
         ("Qarnul Manazil", "As-Sail Al-Kabir", "Penduduk Najd; pesawat dari Malaysia ke Jeddah lazimnya melintasi kawasan miqat ini atau Yalamlam (anak kapal akan mengumumkannya)", "±80 km"),
         ("Yalamlam", "As-Sa'diyyah", "Penduduk Yaman dan yang datang dari arah selatan, termasuk laluan laut dari Asia", "±100 km"),
         ("Zat 'Irq", "Adh-Dharibah", "Penduduk Iraq dan kawasan timur", "±94 km")]

# senarai semak: (group, [(key, item, note)])
CHECKLIST = [
    ("Dokumen & Wang", [("pasport", "Pasport (sah sekurang-kurangnya 6 bulan dari tarikh pulang)", ""), ("visa", "Visa umrah / haji (salinan cetak dan digital)", ""),
                        ("tiket", "Tiket penerbangan dan jadual perjalanan agensi", ""), ("vaksin", "Sijil vaksin meningitis (ACWY) dan vaksin lain yang diwajibkan", "Semak keperluan terkini Kementerian Kesihatan Arab Saudi"),
                        ("ic", "Kad pengenalan, kad Tabung Haji / kad agensi", ""), ("salinan", "Salinan pasport, visa dan gambar berukuran pasport", "Simpan berasingan daripada yang asal"),
                        ("insurans", "Polisi insurans perjalanan", ""), ("wang", "Wang Riyal Saudi, kad debit atau kad perjalanan", ""), ("hubungi", "Nombor telefon mutawwif, hotel dan kedutaan Malaysia", "")]),
    ("Pakaian Ihram", [("ihram", "2 set kain ihram (lelaki)", "Satu dipakai, satu ganti"), ("talipinggang", "Tali pinggang ihram dengan poket", ""),
                       ("selipar", "Selipar yang menampakkan buku lali dan belakang kaki (lelaki)", ""), ("telekung", "Telekung, jubah longgar dan tudung yang tidak menutup muka (wanita)", ""),
                       ("stokin", "Stokin (wanita) dan pakaian dalam yang selesa", ""), ("pin", "Pin atau penyepit kain ihram (tidak berjahit)", "")]),
    ("Kesihatan & Kebersihan", [("ubat", "Ubat harian peribadi dengan preskripsi doktor", ""), ("ubat2", "Ubat demam, selsema, batuk, cirit-birit dan sakit kepala", ""),
                                ("sabun", "Sabun, syampu dan ubat gigi TANPA pewangi", "Untuk tempoh berihram"), ("krim", "Krim lecet, pelembap bibir dan pelindung matahari tanpa pewangi", ""),
                                ("plaster", "Plaster dan krim untuk kaki melecet", ""), ("pelitup", "Pelitup muka", ""), ("semburan", "Botol semburan air untuk menyejukkan badan", ""),
                                ("haid", "Pil penangguh haid (wanita, selepas berbincang dengan doktor)", "")]),
    ("Ibadah", [("manasik", "Buku panduan manasik / doa kecil", ""), ("tasbih", "Tasbih atau kaunter jari", "Atau guna kaunter tawaf dan sa'ie di laman ini"),
                ("quran", "Al-Quran kecil", ""), ("sejadah", "Sejadah ringan", ""), ("begkasut", "Beg kecil untuk kasut di masjid", "")]),
    ("Barang Lain", [("begsandang", "Beg sandang kecil", ""), ("botol", "Botol air boleh guna semula", ""), ("powerbank", "Power bank dan kabel pengecas", "Bawa dalam beg tangan, bukan bagasi"),
                     ("plug", "Penyesuai palam (Arab Saudi guna palam jenis G seperti Malaysia, juga jenis C)", ""), ("payung", "Payung kecil", "Berteduh dengan payung dibenarkan ketika berihram"),
                     ("gunting", "Gunting kecil untuk tahallul (dalam bagasi, bukan beg tangan)", "")]),
]

VIRTUES = [
    ("Haji mabrur tiada balasan baginya melainkan syurga, dan umrah ke umrah menghapuskan dosa di antara keduanya.", "HR Al-Bukhari, no. 1773; Muslim, no. 1349"),
    ("Sesiapa berhaji tanpa bercakap kotor (rafath) dan tanpa melakukan maksiat, dia pulang seperti hari dilahirkan oleh ibunya.", "HR Al-Bukhari, no. 1521; Muslim, no. 1350"),
    ("Umrah pada bulan Ramadan menyamai (pahala) haji.", "HR Al-Bukhari, no. 1782; Muslim, no. 1256"),
    ("Tiada hari yang Allah membebaskan lebih ramai hamba daripada neraka berbanding Hari Arafah.", "HR Muslim, no. 1348"),
    ("Jihad yang paling afdal bagi wanita ialah haji yang mabrur.", "HR Al-Bukhari, no. 1520"),
    ("Solat di Masjidil Haram lebih baik daripada 100,000 solat di masjid lain, dan solat di Masjid Nabawi lebih baik daripada 1,000 solat.", "HR Ibn Majah, no. 1406 (sahih); Al-Bukhari, no. 1190"),
]
