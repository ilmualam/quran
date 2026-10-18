"""Content data for /belajar-solat/, /belajar-iqra/, /belajar-mengaji/ and /waktu-berbuka-puasa/.
Same rules as ibadah.py: Quranic text is read from data-surah/ by reference (("Q", surah, first, last)), never typed here;
every hadith-based text carries its book and hadith number so readers can verify it."""

# ======================= SOLAT =======================
# fardu prayers: (key, name, rakaat, niat arabic, niat rumi, niat maksud)
SOLAT5 = [
    ("subuh", "Subuh", 2, "أُصَلِّي فَرْضَ الصُّبْحِ رَكْعَتَيْنِ مُسْتَقْبِلَ الْقِبْلَةِ أَدَاءً لِلّٰهِ تَعَالَى",
     "Usolli fardhas-subhi rak'ataini mustaqbilal-qiblati ada'an lillahi ta'ala.",
     "Sahaja aku solat fardu Subuh dua rakaat menghadap kiblat, tunai kerana Allah Taala."),
    ("zohor", "Zohor", 4, "أُصَلِّي فَرْضَ الظُّهْرِ أَرْبَعَ رَكَعَاتٍ مُسْتَقْبِلَ الْقِبْلَةِ أَدَاءً لِلّٰهِ تَعَالَى",
     "Usolli fardhaz-zuhri arba'a raka'atin mustaqbilal-qiblati ada'an lillahi ta'ala.",
     "Sahaja aku solat fardu Zohor empat rakaat menghadap kiblat, tunai kerana Allah Taala."),
    ("asar", "Asar", 4, "أُصَلِّي فَرْضَ الْعَصْرِ أَرْبَعَ رَكَعَاتٍ مُسْتَقْبِلَ الْقِبْلَةِ أَدَاءً لِلّٰهِ تَعَالَى",
     "Usolli fardhal-'asri arba'a raka'atin mustaqbilal-qiblati ada'an lillahi ta'ala.",
     "Sahaja aku solat fardu Asar empat rakaat menghadap kiblat, tunai kerana Allah Taala."),
    ("maghrib", "Maghrib", 3, "أُصَلِّي فَرْضَ الْمَغْرِبِ ثَلَاثَ رَكَعَاتٍ مُسْتَقْبِلَ الْقِبْلَةِ أَدَاءً لِلّٰهِ تَعَالَى",
     "Usolli fardhal-maghribi thalatha raka'atin mustaqbilal-qiblati ada'an lillahi ta'ala.",
     "Sahaja aku solat fardu Maghrib tiga rakaat menghadap kiblat, tunai kerana Allah Taala."),
    ("isyak", "Isyak", 4, "أُصَلِّي فَرْضَ الْعِشَاءِ أَرْبَعَ رَكَعَاتٍ مُسْتَقْبِلَ الْقِبْلَةِ أَدَاءً لِلّٰهِ تَعَالَى",
     "Usolli fardhal-'isya'i arba'a raka'atin mustaqbilal-qiblati ada'an lillahi ta'ala.",
     "Sahaja aku solat fardu Isyak empat rakaat menghadap kiblat, tunai kerana Allah Taala."),
]

# step id -> (title, what the body does, arabic | ("Q", s, a1, a2) | "" , rumi, maksud, source)
BACAAN = {
    "niat": ("Niat", "Berdiri tegak menghadap kiblat. Niat ialah rukun di dalam hati, dihadirkan bersama takbiratul ihram. Melafazkan niat sebelum takbir adalah sunat dalam mazhab Syafi'i untuk membantu hati.",
             "", "", "", "Rukun solat; HR Al-Bukhari, no. 1 (“Sesungguhnya setiap amalan bergantung pada niat”)"),
    "takbir": ("Takbiratul Ihram", "Berdiri tegak menghadap kiblat. Angkat kedua-dua tangan, tapak tangan setentang bahu dan ibu jari setentang cuping telinga, sambil berniat di dalam hati dan bertakbir.",
               "اللّٰهُ أَكْبَرُ", "Allahu akbar.", "Allah Maha Besar.", "Rukun solat; HR Al-Bukhari, no. 735 (mengangkat tangan)"),
    "iftitah": ("Doa Iftitah", "Letak tangan kanan di atas tangan kiri, di bawah dada dan di atas pusat. Pandangan ke tempat sujud. Doa iftitah sunat dibaca pada rakaat pertama sahaja.",
                "اللّٰهُ أَكْبَرُ كَبِيرًا، وَالْحَمْدُ لِلّٰهِ كَثِيرًا، وَسُبْحَانَ اللّٰهِ بُكْرَةً وَأَصِيلًا. وَجَّهْتُ وَجْهِيَ لِلَّذِي فَطَرَ السَّمٰوَاتِ وَالْأَرْضَ حَنِيفًا مُسْلِمًا وَمَا أَنَا مِنَ الْمُشْرِكِينَ. إِنَّ صَلَاتِي وَنُسُكِي وَمَحْيَايَ وَمَمَاتِي لِلّٰهِ رَبِّ الْعَالَمِينَ، لَا شَرِيكَ لَهُ وَبِذٰلِكَ أُمِرْتُ وَأَنَا مِنَ الْمُسْلِمِينَ",
                "Allahu akbaru kabira, walhamdu lillahi kathira, wa subhanallahi bukratan wa asila. Wajjahtu wajhiya lillazi fataras-samawati wal-ardha hanifan musliman wa ma ana minal-musyrikin. Inna solati wa nusuki wa mahyaya wa mamati lillahi rabbil-'alamin, la syarika lahu wa bizalika umirtu wa ana minal-muslimin.",
                "Allah Maha Besar dengan sebesar-besarnya, segala puji bagi Allah dengan sebanyak-banyaknya, dan Maha Suci Allah pagi dan petang. Aku hadapkan wajahku kepada Tuhan yang menciptakan langit dan bumi, dalam keadaan lurus dan berserah diri, dan aku bukan daripada golongan musyrik. Sesungguhnya solatku, ibadahku, hidupku dan matiku untuk Allah, Tuhan sekalian alam. Tiada sekutu bagi-Nya, dengan itulah aku diperintahkan, dan aku daripada golongan Muslim.",
                "Sunat; HR Muslim, no. 601 dan no. 771"),
    "fatihah": ("Membaca Surah Al-Fatihah", "Baca Al-Fatihah dengan tertib dan tajwid yang betul. Ia rukun pada setiap rakaat; solat tidak sah tanpanya. Selepas tamat, sunat membaca “Amin”.",
                ("Q", 1, 1, 7), "", "", "Rukun solat; HR Al-Bukhari, no. 756"),
    "surah": ("Membaca Surah Pendek", "Sunat membaca surah atau beberapa ayat selepas Al-Fatihah pada rakaat pertama dan kedua. Contoh di bawah: Surah Al-'Asr.",
              ("Q", 103, 1, 3), "", "", "Sunat; HR Al-Bukhari, no. 776"),
    "surah2": ("Membaca Surah Pendek", "Pada rakaat kedua, baca surah lain selepas Al-Fatihah. Contoh di bawah: Surah Al-Ikhlas.",
               ("Q", 112, 1, 4), "", "", "Sunat; HR Al-Bukhari, no. 776"),
    "rukuk": ("Rukuk", "Bertakbir sambil mengangkat tangan, kemudian membongkok sehingga belakang dan kepala lurus, kedua-dua tapak tangan memegang lutut. Diam seketika (tama'ninah) dan baca 3 kali:",
              "سُبْحَانَ رَبِّيَ الْعَظِيمِ وَبِحَمْدِهِ", "Subhana rabbiyal-'azimi wa bihamdih. (3×)",
              "Maha Suci Tuhanku Yang Maha Agung dan dengan memuji-Nya.", "Rukun (rukuk dengan tama'ninah); HR Abu Daud, no. 870"),
    "iktidal": ("Iktidal", "Bangun dari rukuk sambil mengangkat tangan dan membaca “Sami'allahu liman hamidah”, kemudian berdiri tegak dengan tama'ninah dan membaca:",
                "سَمِعَ اللّٰهُ لِمَنْ حَمِدَهُ. رَبَّنَا لَكَ الْحَمْدُ، مِلْءَ السَّمٰوَاتِ وَمِلْءَ الْأَرْضِ، وَمِلْءَ مَا شِئْتَ مِنْ شَيْءٍ بَعْدُ",
                "Sami'allahu liman hamidah. Rabbana lakal-hamdu, mil'as-samawati wa mil'al-ardhi, wa mil'a ma syi'ta min syai'in ba'd.",
                "Allah mendengar pujian orang yang memuji-Nya. Wahai Tuhan kami, bagi-Mu segala puji, sepenuh langit dan sepenuh bumi, dan sepenuh apa sahaja yang Engkau kehendaki selepas itu.",
                "Rukun (iktidal dengan tama'ninah); HR Muslim, no. 476"),
    "qunut": ("Doa Qunut (Subuh)", "Dalam mazhab Syafi'i, qunut ialah sunat ab'adh pada iktidal rakaat kedua solat Subuh. Angkat kedua-dua tangan dan baca:",
              "اللّٰهُمَّ اهْدِنِي فِيمَنْ هَدَيْتَ، وَعَافِنِي فِيمَنْ عَافَيْتَ، وَتَوَلَّنِي فِيمَنْ تَوَلَّيْتَ، وَبَارِكْ لِي فِيمَا أَعْطَيْتَ، وَقِنِي شَرَّ مَا قَضَيْتَ، فَإِنَّكَ تَقْضِي وَلَا يُقْضٰى عَلَيْكَ، وَإِنَّهُ لَا يَذِلُّ مَنْ وَالَيْتَ، تَبَارَكْتَ رَبَّنَا وَتَعَالَيْتَ",
              "Allahummahdini fiman hadait, wa 'afini fiman 'afait, wa tawallani fiman tawallait, wa barik li fima a'tait, wa qini syarra ma qadhait, fa innaka taqdhi wa la yuqdha 'alaik, wa innahu la yazillu man walait, tabarakta rabbana wa ta'alait.",
              "Ya Allah, berilah aku petunjuk bersama orang yang Engkau beri petunjuk, sihatkanlah aku bersama orang yang Engkau sihatkan, peliharalah aku bersama orang yang Engkau pelihara, berkatilah apa yang Engkau kurniakan kepadaku, dan peliharalah aku daripada keburukan apa yang Engkau tetapkan. Sesungguhnya Engkaulah yang menetapkan dan tiada yang menetapkan ke atas-Mu. Sesungguhnya tidak akan hina orang yang Engkau lindungi. Maha Berkat Engkau wahai Tuhan kami dan Maha Tinggi Engkau.",
              "Sunat ab'adh (mazhab Syafi'i); lafaz HR Abu Daud, no. 1425 dan At-Tirmizi, no. 464. Jika tertinggal, sunat sujud sahwi."),
    "sujud": ("Sujud Pertama", "Bertakbir dan turun sujud. Letakkan tujuh anggota di lantai: dahi (bersama hidung), kedua-dua tapak tangan, kedua-dua lutut dan hujung jari kedua-dua kaki. Tama'ninah dan baca 3 kali:",
              "سُبْحَانَ رَبِّيَ الْأَعْلٰى وَبِحَمْدِهِ", "Subhana rabbiyal-a'la wa bihamdih. (3×)",
              "Maha Suci Tuhanku Yang Maha Tinggi dan dengan memuji-Nya.", "Rukun; tujuh anggota sujud HR Al-Bukhari, no. 812; bacaan HR Abu Daud, no. 870"),
    "duduk": ("Duduk Antara Dua Sujud", "Bangun dari sujud sambil bertakbir dan duduk iftirasy (duduk di atas kaki kiri, kaki kanan ditegakkan). Tama'ninah dan baca:",
              "رَبِّ اغْفِرْ لِي، وَارْحَمْنِي، وَاجْبُرْنِي، وَارْفَعْنِي، وَارْزُقْنِي، وَاهْدِنِي، وَعَافِنِي، وَاعْفُ عَنِّي",
              "Rabbighfirli, warhamni, wajburni, warfa'ni, warzuqni, wahdini, wa 'afini, wa'fu 'anni.",
              "Wahai Tuhanku, ampunilah aku, rahmatilah aku, cukupkanlah kekuranganku, angkatlah darjatku, kurniakanlah rezeki kepadaku, berilah aku petunjuk, sihatkanlah aku dan maafkanlah aku.",
              "Rukun (duduk dengan tama'ninah); lafaz dihimpunkan daripada HR At-Tirmizi, no. 284, Abu Daud, no. 850 dan Ibn Majah, no. 898"),
    "sujud2": ("Sujud Kedua", "Bertakbir dan sujud sekali lagi seperti sujud pertama, dengan tama'ninah dan bacaan yang sama 3 kali:",
               "سُبْحَانَ رَبِّيَ الْأَعْلٰى وَبِحَمْدِهِ", "Subhana rabbiyal-a'la wa bihamdih. (3×)",
               "Maha Suci Tuhanku Yang Maha Tinggi dan dengan memuji-Nya.", "Rukun; HR Abu Daud, no. 870"),
    "bangun": ("Bangun ke Rakaat Seterusnya", "Bertakbir dan bangun berdiri untuk rakaat seterusnya. Sunat duduk sebentar (duduk istirahah) sebelum bangun, kemudian bertumpu pada tangan.",
               "اللّٰهُ أَكْبَرُ", "Allahu akbar.", "Allah Maha Besar.", "Duduk istirahah: HR Al-Bukhari, no. 823"),
    "tahiyat-awal": ("Tahiyat (Tasyahhud) Awal", "Selepas sujud kedua rakaat kedua, duduk iftirasy. Letak tangan di atas paha; jari telunjuk kanan diangkat ketika menyebut “illallah”. Baca:",
                     "التَّحِيَّاتُ الْمُبَارَكَاتُ الصَّلَوَاتُ الطَّيِّبَاتُ لِلّٰهِ، السَّلَامُ عَلَيْكَ أَيُّهَا النَّبِيُّ وَرَحْمَةُ اللّٰهِ وَبَرَكَاتُهُ، السَّلَامُ عَلَيْنَا وَعَلٰى عِبَادِ اللّٰهِ الصَّالِحِينَ، أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا اللّٰهُ، وَأَشْهَدُ أَنَّ مُحَمَّدًا رَسُولُ اللّٰهِ. اللّٰهُمَّ صَلِّ عَلٰى مُحَمَّدٍ",
                     "At-tahiyyatul-mubarakatus-solawatut-toyyibatu lillah. As-salamu 'alaika ayyuhan-nabiyyu wa rahmatullahi wa barakatuh. As-salamu 'alaina wa 'ala 'ibadillahis-solihin. Asyhadu an la ilaha illallah, wa asyhadu anna Muhammadar-rasulullah. Allahumma solli 'ala Muhammad.",
                     "Segala penghormatan, keberkatan, solat dan kebaikan adalah bagi Allah. Salam sejahtera ke atasmu wahai Nabi, serta rahmat Allah dan keberkatan-Nya. Salam sejahtera ke atas kami dan ke atas hamba-hamba Allah yang soleh. Aku bersaksi bahawa tiada Tuhan melainkan Allah, dan aku bersaksi bahawa Muhammad ialah pesuruh Allah. Ya Allah, limpahkanlah selawat ke atas Muhammad.",
                     "Sunat ab'adh; lafaz tasyahhud HR Muslim, no. 403 (riwayat Ibn 'Abbas). Jika tertinggal, sunat sujud sahwi."),
    "tahiyat-akhir": ("Tahiyat (Tasyahhud) Akhir", "Pada rakaat terakhir, duduk tawarruk (punggung kiri di lantai, kaki kiri dikeluarkan ke kanan, kaki kanan ditegakkan). Baca tasyahhud seperti tahiyat awal, kemudian selawat Ibrahimiyyah:",
                      "التَّحِيَّاتُ الْمُبَارَكَاتُ الصَّلَوَاتُ الطَّيِّبَاتُ لِلّٰهِ، السَّلَامُ عَلَيْكَ أَيُّهَا النَّبِيُّ وَرَحْمَةُ اللّٰهِ وَبَرَكَاتُهُ، السَّلَامُ عَلَيْنَا وَعَلٰى عِبَادِ اللّٰهِ الصَّالِحِينَ، أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا اللّٰهُ، وَأَشْهَدُ أَنَّ مُحَمَّدًا رَسُولُ اللّٰهِ. اللّٰهُمَّ صَلِّ عَلٰى مُحَمَّدٍ وَعَلٰى آلِ مُحَمَّدٍ، كَمَا صَلَّيْتَ عَلٰى إِبْرَاهِيمَ وَعَلٰى آلِ إِبْرَاهِيمَ، إِنَّكَ حَمِيدٌ مَجِيدٌ. اللّٰهُمَّ بَارِكْ عَلٰى مُحَمَّدٍ وَعَلٰى آلِ مُحَمَّدٍ، كَمَا بَارَكْتَ عَلٰى إِبْرَاهِيمَ وَعَلٰى آلِ إِبْرَاهِيمَ، إِنَّكَ حَمِيدٌ مَجِيدٌ",
                      "At-tahiyyatul-mubarakatus-solawatut-toyyibatu lillah. As-salamu 'alaika ayyuhan-nabiyyu wa rahmatullahi wa barakatuh. As-salamu 'alaina wa 'ala 'ibadillahis-solihin. Asyhadu an la ilaha illallah, wa asyhadu anna Muhammadar-rasulullah. Allahumma solli 'ala Muhammad wa 'ala ali Muhammad, kama sollaita 'ala Ibrahim wa 'ala ali Ibrahim, innaka hamidun majid. Allahumma barik 'ala Muhammad wa 'ala ali Muhammad, kama barakta 'ala Ibrahim wa 'ala ali Ibrahim, innaka hamidun majid.",
                      "… Ya Allah, limpahkanlah selawat ke atas Muhammad dan keluarga Muhammad sebagaimana Engkau limpahkan selawat ke atas Ibrahim dan keluarga Ibrahim; sesungguhnya Engkau Maha Terpuji lagi Maha Mulia. Ya Allah, berkatilah Muhammad dan keluarga Muhammad sebagaimana Engkau berkati Ibrahim dan keluarga Ibrahim; sesungguhnya Engkau Maha Terpuji lagi Maha Mulia.",
                      "Rukun (duduk, tasyahhud dan selawat dalam tahiyat akhir); HR Muslim, no. 403; selawat HR Al-Bukhari, no. 3370"),
    "doa-akhir": ("Doa Sebelum Salam", "Sunat berdoa selepas selawat dan sebelum salam. Antara doa yang diajar Rasulullah SAW:",
                  "اللّٰهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ عَذَابِ الْقَبْرِ، وَمِنْ عَذَابِ النَّارِ، وَمِنْ فِتْنَةِ الْمَحْيَا وَالْمَمَاتِ، وَمِنْ فِتْنَةِ الْمَسِيحِ الدَّجَّالِ",
                  "Allahumma inni a'uzu bika min 'azabil-qabri, wa min 'azabin-nar, wa min fitnatil-mahya wal-mamat, wa min fitnatil-masihid-dajjal.",
                  "Ya Allah, aku berlindung kepada-Mu daripada azab kubur, daripada azab neraka, daripada fitnah kehidupan dan kematian, dan daripada fitnah Al-Masih Ad-Dajjal.",
                  "Sunat; HR Al-Bukhari, no. 1377"),
    "salam": ("Memberi Salam", "Berpaling ke kanan sehingga pipi kanan kelihatan dari belakang sambil memberi salam pertama (rukun), kemudian ke kiri untuk salam kedua (sunat).",
              "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللّٰهِ", "Assalamu'alaikum wa rahmatullah. (kanan, kemudian kiri)",
              "Salam sejahtera ke atas kamu dan rahmat Allah.", "Rukun (salam pertama); HR Muslim, no. 582"),
}


def solat_steps(rakaat, qunut):
    """[(step id, rakaat number)] for one fardu prayer, in the order performed."""
    out = []
    for r in range(1, rakaat + 1):
        if r == 1:
            out += [("niat", 1), ("takbir", 1), ("iftitah", 1)]
        out.append(("fatihah", r))
        if r <= 2:
            out.append(("surah" if r == 1 else "surah2", r))
        out += [("rukuk", r), ("iktidal", r)]
        if qunut and r == 2:
            out.append(("qunut", r))
        out += [("sujud", r), ("duduk", r), ("sujud2", r)]
        if r == rakaat:
            out += [("tahiyat-akhir", r), ("doa-akhir", r), ("salam", r)]
        elif r == 2:
            out += [("tahiyat-awal", r), ("bangun", r)]
        else:
            out.append(("bangun", r))
    return out


RUKUN = ["Niat", "Takbiratul ihram", "Berdiri bagi yang mampu (solat fardu)", "Membaca Al-Fatihah pada setiap rakaat",
         "Rukuk dengan tama'ninah", "Iktidal dengan tama'ninah", "Sujud dua kali dengan tama'ninah", "Duduk antara dua sujud dengan tama'ninah",
         "Duduk tasyahhud akhir", "Membaca tasyahhud akhir", "Selawat ke atas Nabi SAW dalam tasyahhud akhir", "Memberi salam yang pertama", "Tertib (mengikut susunan)"]
SYARAT_SAH = ["Suci daripada hadas kecil dan besar (berwuduk; mandi wajib jika berhadas besar)", "Suci badan, pakaian dan tempat solat daripada najis",
              "Menutup aurat (lelaki: pusat hingga lutut; wanita: seluruh badan kecuali muka dan tapak tangan)", "Menghadap kiblat",
              "Telah masuk waktu solat", "Mengetahui kefarduan solat dan cara melakukannya"]
BATAL = ["Berhadas (contohnya terkentut atau keluar sesuatu dari qubul atau dubur)", "Terkena najis yang tidak dimaafkan dan tidak dibuang serta-merta",
         "Terbuka aurat dan tidak ditutup serta-merta", "Bercakap dengan sengaja walaupun satu huruf yang memberi makna", "Makan atau minum",
         "Banyak bergerak (tiga pergerakan besar berturut-turut) tanpa keperluan", "Berpaling dada dari arah kiblat",
         "Menambah rukun fi'li (perbuatan) dengan sengaja, seperti rukuk dua kali", "Ketawa berdekah-dekah", "Berniat keluar daripada solat atau ragu-ragu untuk meneruskannya"]

# ======================= HURUF HIJAIYAH =======================
# (letter, name, rumi consonant, heavy (tafkhim: fathah sounds like "o"), connects to the next letter, makhraj group, makhraj detail)
MAKHRAJ = [("jauf", "Al-Jauf (rongga mulut dan tekak)"), ("halq", "Al-Halq (halkum)"), ("lisan", "Al-Lisan (lidah)"),
           ("syafatan", "Asy-Syafatan (dua bibir)"), ("khaisyum", "Al-Khaisyum (rongga hidung)")]
HURUF = [
    ("ا", "Alif", "", False, False, "jauf", "Rongga mulut dan tekak; alif sentiasa mati dan menjadi huruf mad (panjang) selepas baris atas."),
    ("ب", "Ba", "b", False, True, "syafatan", "Dua bibir dirapatkan."),
    ("ت", "Ta", "t", False, True, "lisan", "Hujung lidah menyentuh pangkal gigi seri atas."),
    ("ث", "Tsa", "ts", False, True, "lisan", "Hujung lidah di hujung gigi seri atas; lidah sedikit dikeluarkan."),
    ("ج", "Jim", "j", False, True, "lisan", "Tengah lidah menyentuh lelangit keras."),
    ("ح", "Ḥa", "ḥ", False, True, "halq", "Tengah halkum; bunyi desah yang bersih tanpa serak."),
    ("خ", "Kho", "kh", True, True, "halq", "Hujung halkum (dekat mulut); bunyi tebal dan berserak."),
    ("د", "Dal", "d", False, False, "lisan", "Hujung lidah menyentuh pangkal gigi seri atas."),
    ("ذ", "Dzal", "dz", False, False, "lisan", "Hujung lidah di hujung gigi seri atas."),
    ("ر", "Ro", "r", True, False, "lisan", "Hujung lidah, sedikit ke belakang daripada makhraj nun, menyentuh gusi atas."),
    ("ز", "Zai", "z", False, False, "lisan", "Hujung lidah dekat gigi seri bawah; bunyi berdesing (safir)."),
    ("س", "Sin", "s", False, True, "lisan", "Hujung lidah dekat gigi seri bawah; bunyi berdesing (safir)."),
    ("ش", "Syin", "sy", False, True, "lisan", "Tengah lidah dan lelangit keras; angin tersebar di mulut."),
    ("ص", "Sod", "s", True, True, "lisan", "Hujung lidah dekat gigi seri bawah; bunyi tebal dan berdesing."),
    ("ض", "Dhod", "dh", True, True, "lisan", "Tepi lidah (kiri atau kanan) menyentuh geraham atas; bunyi tebal."),
    ("ط", "Tho", "t", True, True, "lisan", "Hujung lidah menyentuh pangkal gigi seri atas; bunyi tebal."),
    ("ظ", "Zho", "z", True, True, "lisan", "Hujung lidah di hujung gigi seri atas; bunyi tebal."),
    ("ع", "'Ain", "'", False, True, "halq", "Tengah halkum; suara tertahan sedikit di tekak."),
    ("غ", "Ghin", "gh", True, True, "halq", "Hujung halkum (dekat mulut); bunyi tebal seperti berkumur."),
    ("ف", "Fa", "f", False, True, "syafatan", "Perut bibir bawah menyentuh hujung gigi seri atas."),
    ("ق", "Qof", "q", True, True, "lisan", "Pangkal lidah (paling dalam) menyentuh lelangit lembut dekat anak tekak; bunyi tebal."),
    ("ك", "Kaf", "k", False, True, "lisan", "Pangkal lidah, sedikit ke depan daripada qof, menyentuh lelangit."),
    ("ل", "Lam", "l", False, True, "lisan", "Tepi hujung lidah menyentuh gusi gigi atas."),
    ("م", "Mim", "m", False, True, "syafatan", "Dua bibir dirapatkan, dengan dengung dari rongga hidung."),
    ("ن", "Nun", "n", False, True, "lisan", "Hujung lidah menyentuh gusi atas, dengan dengung dari rongga hidung."),
    ("و", "Wau", "w", False, False, "syafatan", "Dua bibir dimuncungkan (tidak rapat)."),
    ("ه", "Ha", "h", False, True, "halq", "Pangkal halkum (paling dalam); hembusan nafas yang lembut."),
    ("ء", "Hamzah", "'", False, False, "halq", "Pangkal halkum; suara terhenti sebentar kemudian dilepaskan."),
    ("ي", "Ya", "y", False, True, "lisan", "Tengah lidah menyentuh lelangit keras."),
]
QALQALAH = "قطبجد"

# ======================= IQRA' 1–6 =======================
# (level, title, focus, what is learnt, example arabic, example rumi)
IQRA = [
    (1, "Iqra' 1", "Huruf tunggal berbaris atas (fathah)", "Mengenal 28 huruf hijaiyah dengan baris atas dan membacanya satu-satu, kemudian dua dan tiga huruf berturut-turut tanpa dieja.",
     "بَ تَ ثَ · أَخَذَ", "ba ta tsa · a-kho-dza"),
    (2, "Iqra' 2", "Huruf bersambung dan mad asli (alif)", "Membaca huruf yang bersambung dalam satu kalimah dan bacaan panjang dua harakat apabila baris atas diikuti alif.",
     "بَا تَا · قَالَ", "baa taa · qoo-la"),
    (3, "Iqra' 3", "Baris bawah (kasrah), baris hadapan (dhammah) dan mad ya/wau", "Membaca baris bawah dan hadapan, serta panjang dua harakat bagi baris bawah diikuti ya mati dan baris hadapan diikuti wau mati.",
     "بِ بُ · قِيلَ · يَقُولُ", "bi bu · qii-la · ya-quu-lu"),
    (4, "Iqra' 4", "Tanwin, sukun (huruf mati) dan qalqalah", "Membaca baris dua (tanwin), huruf mati selepas huruf berbaris, dan lantunan qalqalah pada ق ط ب ج د yang mati.",
     "بًا بٍ بٌ · يَقْطَعُ", "ban bin bun · yaq-to-'u"),
    (5, "Iqra' 5", "Alif lam, sabdu (tasydid) dan waqaf", "Membaca alif lam qamariah (lam jelas) dan syamsiah (lam tidak dibaca), huruf bersabdu, serta cara berhenti (waqaf) di hujung ayat.",
     "اَلْقَمَرُ · اَلشَّمْسُ · رَبُّ", "al-qo-ma-ru · asy-syam-su · rab-bu"),
    (6, "Iqra' 6", "Bacaan ayat Al-Quran", "Menggabungkan semua kemahiran untuk membaca ayat Al-Quran sebenar dengan lancar, bermula dengan surah-surah pendek Juz 30.",
     "", ""),
]
# Iqra' 6 practice: short ayat from Juz 30 (surah, ayah) read from data-surah/
IQRA6 = [(1, 2), (1, 4), (1, 5), (97, 1), (103, 1), (103, 2), (108, 1), (108, 2), (108, 3), (110, 1), (112, 1), (112, 2), (112, 3), (112, 4),
         (113, 1), (113, 2), (114, 1), (114, 2), (114, 3), (114, 4), (95, 1), (95, 2), (95, 3), (94, 1), (94, 5), (94, 6), (93, 1), (93, 2), (93, 3),
         (99, 1), (101, 1), (101, 2), (102, 1), (102, 2), (105, 1), (106, 1), (106, 2), (106, 3), (107, 1), (109, 1), (109, 2), (109, 6), (111, 1), (87, 1), (96, 1)]

# milestones for the learning checklist on /belajar-mengaji/
MILESTONES = [
    ("huruf", "Kenal 29 huruf hijaiyah dan namanya"), ("makhraj", "Sebut setiap huruf dari makhraj yang betul"),
    ("baris", "Baca baris atas, bawah dan hadapan"), ("sambung", "Baca huruf bersambung (awal, tengah, akhir)"),
    ("mad", "Baca mad asli 2 harakat (alif, wau, ya)"), ("tanwin", "Baca tanwin dan sukun"), ("qalqalah", "Lantunkan qalqalah ق ط ب ج د"),
    ("alif-lam", "Bezakan alif lam qamariah dan syamsiah"), ("sabdu", "Baca huruf bersabdu (tasydid)"), ("fatihah", "Baca Al-Fatihah dengan betul (semak dengan guru)"),
    ("juz30", "Baca 5 surah pendek Juz 30 dengan lancar"), ("tajwid", "Faham hukum nun mati, mim mati dan mad"),
]

# ======================= RAMADAN =======================
# (id, title, arabic, rumi, maksud, source, note)
RAMADAN_DOA = [
    ("niat-harian", "Niat puasa Ramadan (setiap malam)", "نَوَيْتُ صَوْمَ غَدٍ عَنْ أَدَاءِ فَرْضِ شَهْرِ رَمَضَانَ هٰذِهِ السَّنَةِ لِلّٰهِ تَعَالَى",
     "Nawaitu sauma ghadin 'an ada'i fardhi syahri Ramadhana hazihis-sanati lillahi ta'ala.",
     "Sahaja aku berpuasa esok hari bagi menunaikan fardu bulan Ramadan tahun ini kerana Allah Taala.",
     "Mazhab Syafi'i: niat wajib pada malam hari (tabyit) bagi setiap hari puasa fardu; HR Abu Daud, no. 2454",
     "Niat di dalam hati sudah memadai; lafaz membantu hati. Niat boleh dibuat dari Maghrib hingga sebelum terbit fajar."),
    ("niat-sebulan", "Niat puasa sebulan (bertaqlid mazhab Maliki)", "نَوَيْتُ صَوْمَ جَمِيعِ شَهْرِ رَمَضَانَ هٰذِهِ السَّنَةِ تَقْلِيدًا لِلْإِمَامِ مَالِكٍ فَرْضًا لِلّٰهِ تَعَالَى",
     "Nawaitu sauma jami'i syahri Ramadhana hazihis-sanati taqlidan lil-Imam Malik fardhan lillahi ta'ala.",
     "Sahaja aku berpuasa sepanjang bulan Ramadan tahun ini dengan bertaqlid kepada Imam Malik, fardu kerana Allah Taala.",
     "Amalan berjaga-jaga di Malaysia sekiranya terlupa berniat pada sesuatu malam",
     "Dibaca pada malam pertama Ramadan. Niat harian tetap dianjurkan setiap malam."),
    ("doa-berbuka", "Doa berbuka puasa", "ذَهَبَ الظَّمَأُ وَابْتَلَّتِ الْعُرُوقُ وَثَبَتَ الْأَجْرُ إِنْ شَاءَ اللّٰهُ",
     "Zahabaz-zama'u wabtallatil-'uruqu wa thabatal-ajru insya-Allah.",
     "Telah hilang dahaga, telah basah urat-urat, dan telah tetap pahala, insya-Allah.",
     "HR Abu Daud, no. 2357 (hasan)",
     "Dibaca selepas berbuka (selepas minum). Mulakan dengan “Bismillah”."),
    ("doa-berbuka-2", "Doa berbuka puasa (lafaz popular)", "اللّٰهُمَّ لَكَ صُمْتُ وَعَلٰى رِزْقِكَ أَفْطَرْتُ",
     "Allahumma laka sumtu wa 'ala rizqika aftartu.",
     "Ya Allah, kerana-Mu aku berpuasa dan dengan rezeki-Mu aku berbuka.",
     "HR Abu Daud, no. 2358 (mursal; sanadnya lemah)",
     "Boleh dibaca sebagai doa umum. Tambahan “wa bika amantu…” tidak terdapat dalam riwayat hadis."),
    ("doa-lailatul-qadar", "Doa malam Lailatul Qadar", "اللّٰهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي",
     "Allahumma innaka 'afuwwun tuhibbul-'afwa fa'fu 'anni.",
     "Ya Allah, sesungguhnya Engkau Maha Pemaaf dan suka memaafkan, maka maafkanlah aku.",
     "HR At-Tirmizi, no. 3513 (diajar kepada Aisyah RA untuk malam Lailatul Qadar)",
     "Perbanyakkan pada 10 malam terakhir, terutama malam-malam ganjil."),
]
RAMADAN_HADIS = [
    ("Bersahur", "“Bersahurlah kamu, kerana pada sahur itu ada keberkatan.”", "HR Al-Bukhari, no. 1923; Muslim, no. 1095"),
    ("Segera berbuka", "“Manusia sentiasa dalam kebaikan selagi mereka menyegerakan berbuka.”", "HR Al-Bukhari, no. 1957; Muslim, no. 1098"),
    ("Berbuka dengan kurma", "Rasulullah SAW berbuka dengan beberapa biji kurma basah (rutab); jika tiada, dengan kurma kering; jika tiada, dengan beberapa teguk air.", "HR Abu Daud, no. 2356; At-Tirmizi, no. 696"),
    ("Keampunan", "“Sesiapa berpuasa Ramadan dengan iman dan mengharap pahala, diampunkan dosanya yang telah lalu.”", "HR Al-Bukhari, no. 38; Muslim, no. 760"),
    ("Lailatul Qadar", "“Carilah Lailatul Qadar pada malam-malam ganjil dalam sepuluh malam terakhir Ramadan.”", "HR Al-Bukhari, no. 2017"),
    ("Memberi makan orang berbuka", "“Sesiapa memberi makan orang yang berpuasa untuk berbuka, baginya pahala seperti orang itu tanpa mengurangkan pahalanya sedikit pun.”", "HR At-Tirmizi, no. 807"),
]
BATAL_PUASA = ["Makan atau minum dengan sengaja", "Memasukkan sesuatu ke dalam rongga badan yang terbuka (seperti mulut, hidung, telinga, dubur) dengan sengaja",
               "Muntah dengan sengaja", "Bersetubuh pada siang hari Ramadan (wajib qada dan kafarah)", "Mengeluarkan mani dengan sengaja",
               "Kedatangan haid atau nifas", "Gila", "Murtad"]
