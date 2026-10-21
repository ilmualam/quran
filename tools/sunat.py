"""Content for /solat-sunat/ and its eight prayer pages (tools/pages7.py). Same rules as ibadah.py / ibadah2.py: Quranic text
is read from data-surah/ by reference, never typed; every hadith-based text carries its book and number, and a weak (dhaif)
narration is labelled as such. Niat follow the usual Malaysian (Syafi'i) lafaz; the lafaz is sunat, the niat is in the heart.
The step player reuses ibadah2.BACAAN; the extra steps below only add what these prayers do differently."""
import ibadah2 as I2
import tahlil as T

# extra player steps: same shape as ibadah2.BACAAN (title, how, arabic | ("Q", s, a1, a2) | "", rumi, maksud, source)
_TA = I2.BACAAN["tahiyat-akhir"]
_SEL_AR = "اللّٰهُمَّ صَلِّ عَلٰى مُحَمَّدٍ وَعَلٰى آلِ مُحَمَّدٍ" + _TA[2].split("اللّٰهُمَّ صَلِّ عَلٰى مُحَمَّدٍ وَعَلٰى آلِ مُحَمَّدٍ", 1)[1]
_SEL_RU = "Allahumma solli 'ala Muhammad wa 'ala ali Muhammad" + _TA[3].split("Allahumma solli 'ala Muhammad wa 'ala ali Muhammad", 1)[1]
_SEL_MN = ("Ya Allah, limpahkanlah selawat ke atas Muhammad dan keluarga Muhammad sebagaimana Engkau limpahkan selawat ke atas Ibrahim dan keluarga Ibrahim; "
           "sesungguhnya Engkau Maha Terpuji lagi Maha Mulia. Ya Allah, berkatilah Muhammad dan keluarga Muhammad sebagaimana Engkau berkati Ibrahim dan keluarga Ibrahim; "
           "sesungguhnya Engkau Maha Terpuji lagi Maha Mulia.")


def _surah(s, a2, name, rk, note=""):
    return (f"Membaca Surah {name}", f"Selepas Al-Fatihah pada rakaat {rk}, baca Surah {name}.{(' ' + note) if note else ''}",
            ("Q", s, 1, a2), "", "", "Sunat membaca surah selepas Al-Fatihah; HR Al-Bukhari, no. 776")


BACAAN = {
    "s-syams": _surah(91, 15, "Asy-Syams", "pertama", "Inilah amalan biasa di Malaysia bagi solat Dhuha; surah lain juga sah."),
    "s-dhuha": _surah(93, 11, "Ad-Dhuha", "kedua"),
    "s-kafirun": _surah(109, 6, "Al-Kafirun", "pertama", "Imam An-Nawawi menganjurkan Al-Kafirun dan Al-Ikhlas bagi solat sunat dua rakaat seperti istikharah."),
    "s-ikhlas": _surah(112, 4, "Al-Ikhlas", "kedua"),
    "s-ala": _surah(87, 19, "Al-A'la", "pertama witir", "Sunnah Rasulullah SAW dalam witir tiga rakaat (HR Abu Daud, no. 1423; At-Tirmizi, no. 462)."),
    "s-kafirun2": _surah(109, 6, "Al-Kafirun", "kedua witir"),
    "s-qul3": ("Membaca Al-Ikhlas, Al-Falaq & An-Nas", "Pada rakaat witir yang terakhir, baca Al-Ikhlas, kemudian Al-Falaq dan An-Nas (di bawah: Al-Ikhlas).",
               ("Q", 112, 1, 4), "", "", "HR Abu Daud, no. 1424; At-Tirmizi, no. 463"),
    # solat jenazah: four takbir, standing throughout, no rukuk or sujud
    "j-niat": ("Niat", "Berdiri di sisi jenazah: bagi imam atau orang yang solat seorang diri, setentang kepala jenazah lelaki dan setentang punggung jenazah perempuan. Niat dalam hati bersama takbir pertama.",
               "", "", "", "Rukun; kedudukan imam HR Abu Daud, no. 3194 dan At-Tirmizi, no. 1034"),
    "j-t1": ("Takbir Pertama & Al-Fatihah", "Angkat tangan dan bertakbir “Allahu akbar”, letak tangan kanan di atas tangan kiri, kemudian terus membaca Al-Fatihah (tiada doa iftitah atau surah).",
             ("Q", 1, 1, 7), "", "", "Rukun; HR Al-Bukhari, no. 1335 (Ibn 'Abbas membaca Al-Fatihah dalam solat jenazah)"),
    "j-t2": ("Takbir Kedua & Selawat", "Bertakbir “Allahu akbar” (sunat mengangkat tangan), kemudian membaca selawat ke atas Nabi; sekurang-kurangnya “Allahumma solli 'ala Muhammad”, afdalnya selawat Ibrahimiyyah:",
             _SEL_AR, _SEL_RU, _SEL_MN, "Rukun; selawat Ibrahimiyyah HR Al-Bukhari, no. 3370"),
    "j-t3": ("Takbir Ketiga & Doa untuk Jenazah", "Bertakbir “Allahu akbar”, kemudian mendoakan jenazah. Kata ganti mengikut jenazah (pilih di atas):",
             T.DOA["l"][0], T.DOA["l"][1], T.DOA["l"][2], "Rukun (doa khusus untuk jenazah); HR Muslim, no. 963"),
    "j-t4": ("Takbir Keempat & Doa", "Bertakbir “Allahu akbar”, kemudian sunat membaca doa ini:",
             "اللّٰهُمَّ لَا تَحْرِمْنَا أَجْرَهُ، وَلَا تَفْتِنَّا بَعْدَهُ، وَاغْفِرْ لَنَا وَلَهُ", "Allahumma la tahrimna ajrahu, wa la taftinna ba'dahu, waghfir lana wa lahu.",
             "Ya Allah, janganlah Engkau halang kami daripada pahalanya, janganlah Engkau timpakan fitnah kepada kami selepas pemergiannya, dan ampunilah kami dan dia.",
             "Sunat; HR Abu Daud, no. 3201; Ibn Majah, no. 1498"),
    "j-salam": ("Memberi Salam", "Memberi salam ke kanan (rukun) dan ke kiri (sunat), dalam keadaan berdiri.", "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللّٰهِ",
                "Assalamu'alaikum wa rahmatullah.", "Salam sejahtera ke atas kamu dan rahmat Allah.", "Rukun"),
}

# solat jenazah, by who is being prayed for: one man (l), one woman (p), men or mixed (ll), women (pp)
JENAZAH = {
    "l": {"niat": ("أُصَلِّي عَلَى هٰذَا الْمَيِّتِ أَرْبَعَ تَكْبِيرَاتٍ فَرْضَ كِفَايَةٍ لِلّٰهِ تَعَالَى", "Usolli 'ala hazal-mayyiti arba'a takbiratin fardha kifayatin lillahi ta'ala.",
                   "Sahaja aku solat ke atas jenazah (lelaki) ini empat takbir, fardu kifayah kerana Allah Taala."),
           "t4": ("اللّٰهُمَّ لَا تَحْرِمْنَا أَجْرَهُ، وَلَا تَفْتِنَّا بَعْدَهُ، وَاغْفِرْ لَنَا وَلَهُ", "Allahumma la tahrimna ajrahu, wa la taftinna ba'dahu, waghfir lana wa lahu.",
                  "Ya Allah, janganlah Engkau halang kami daripada pahalanya, janganlah Engkau timpakan fitnah kepada kami selepas pemergiannya, dan ampunilah kami dan dia.")},
    "p": {"niat": ("أُصَلِّي عَلَى هٰذِهِ الْمَيِّتَةِ أَرْبَعَ تَكْبِيرَاتٍ فَرْضَ كِفَايَةٍ لِلّٰهِ تَعَالَى", "Usolli 'ala hazihil-mayyitati arba'a takbiratin fardha kifayatin lillahi ta'ala.",
                   "Sahaja aku solat ke atas jenazah (perempuan) ini empat takbir, fardu kifayah kerana Allah Taala."),
           "t4": ("اللّٰهُمَّ لَا تَحْرِمْنَا أَجْرَهَا، وَلَا تَفْتِنَّا بَعْدَهَا، وَاغْفِرْ لَنَا وَلَهَا", "Allahumma la tahrimna ajraha, wa la taftinna ba'daha, waghfir lana wa laha.",
                  "Ya Allah, janganlah Engkau halang kami daripada pahalanya, janganlah Engkau timpakan fitnah kepada kami selepas pemergiannya, dan ampunilah kami dan dia (perempuan).")},
    "ll": {"niat": ("أُصَلِّي عَلَى هٰؤُلَاءِ الْمَوْتَى أَرْبَعَ تَكْبِيرَاتٍ فَرْضَ كِفَايَةٍ لِلّٰهِ تَعَالَى", "Usolli 'ala ha'ula'il-mauta arba'a takbiratin fardha kifayatin lillahi ta'ala.",
                    "Sahaja aku solat ke atas jenazah-jenazah ini empat takbir, fardu kifayah kerana Allah Taala."),
            "t4": ("اللّٰهُمَّ لَا تَحْرِمْنَا أَجْرَهُمْ، وَلَا تَفْتِنَّا بَعْدَهُمْ، وَاغْفِرْ لَنَا وَلَهُمْ", "Allahumma la tahrimna ajrahum, wa la taftinna ba'dahum, waghfir lana wa lahum.",
                   "Ya Allah, janganlah Engkau halang kami daripada pahala mereka, janganlah Engkau timpakan fitnah kepada kami selepas pemergian mereka, dan ampunilah kami dan mereka.")},
    "pp": {"niat": ("أُصَلِّي عَلَى هٰؤُلَاءِ الْمَيِّتَاتِ أَرْبَعَ تَكْبِيرَاتٍ فَرْضَ كِفَايَةٍ لِلّٰهِ تَعَالَى", "Usolli 'ala ha'ula'il-mayyitati arba'a takbiratin fardha kifayatin lillahi ta'ala.",
                    "Sahaja aku solat ke atas jenazah-jenazah (perempuan) ini empat takbir, fardu kifayah kerana Allah Taala."),
            "t4": ("اللّٰهُمَّ لَا تَحْرِمْنَا أَجْرَهُنَّ، وَلَا تَفْتِنَّا بَعْدَهُنَّ، وَاغْفِرْ لَنَا وَلَهُنَّ", "Allahumma la tahrimna ajrahunna, wa la taftinna ba'dahunna, waghfir lana wa lahunna.",
                   "Ya Allah, janganlah Engkau halang kami daripada pahala mereka, janganlah Engkau timpakan fitnah kepada kami selepas pemergian mereka, dan ampunilah kami dan mereka.")},
}
for k in JENAZAH:
    JENAZAH[k]["t3"] = T.DOA[k]


def steps(surahs, qunut=False):
    """[(step id, rakaat)] for a sunat prayer; surahs = one surah step id per rakaat (None: no surah)."""
    n, out = len(surahs), []
    for r, s in enumerate(surahs, 1):
        if r == 1:
            out += [("niat", 1), ("takbir", 1), ("iftitah", 1)]
        out.append(("fatihah", r))
        if s:
            out.append((s, r))
        out += [("rukuk", r), ("iktidal", r)]
        if qunut and r == n:
            out.append(("qunut", r))
        out += [("sujud", r), ("duduk", r), ("sujud2", r)]
        out += [("tahiyat-akhir", r), ("doa-akhir", r), ("salam", r)] if r == n else [("bangun", r)]
    return out


JENAZAH_STEPS = [("j-niat", 1), ("j-t1", 1), ("j-t2", 2), ("j-t3", 3), ("j-t4", 4), ("j-salam", 4)]


def niat(name_ar, name_ru, name_ms, rk_ar="رَكْعَتَيْنِ", rk_ru="rak'ataini", rk_ms="dua rakaat", extra_ar="", extra_ru="", extra_ms=""):
    return (f"أُصَلِّي {name_ar} {rk_ar}{(' ' + extra_ar) if extra_ar else ''} لِلّٰهِ تَعَالَى",
            f"Usolli {name_ru} {rk_ru}{(' ' + extra_ru) if extra_ru else ''} lillahi ta'ala.",
            f"Sahaja aku solat {name_ms} {rk_ms}{(' ' + extra_ms) if extra_ms else ''} kerana Allah Taala.")


SAYYIDUL = next(z for z in __import__("ibadah").Z_PAGI_PETANG if z[0] == "sayyidul")

# doa cards: (id, title, arabic | "Q:s:a1-a2", rumi, maksud, source, note)
DOA_ISTIKHARAH = ("doa-istikharah", "Doa Istikharah",
                  "اللَّهُمَّ إِنِّي أَسْتَخِيرُكَ بِعِلْمِكَ، وَأَسْتَقْدِرُكَ بِقُدْرَتِكَ، وَأَسْأَلُكَ مِنْ فَضْلِكَ الْعَظِيمِ، فَإِنَّكَ تَقْدِرُ وَلَا أَقْدِرُ، وَتَعْلَمُ وَلَا أَعْلَمُ، وَأَنْتَ عَلَّامُ الْغُيُوبِ. "
                  "اللَّهُمَّ إِنْ كُنْتَ تَعْلَمُ أَنَّ هٰذَا الْأَمْرَ خَيْرٌ لِي فِي دِينِي وَمَعَاشِي وَعَاقِبَةِ أَمْرِي فَاقْدُرْهُ لِي وَيَسِّرْهُ لِي ثُمَّ بَارِكْ لِي فِيهِ، "
                  "وَإِنْ كُنْتَ تَعْلَمُ أَنَّ هٰذَا الْأَمْرَ شَرٌّ لِي فِي دِينِي وَمَعَاشِي وَعَاقِبَةِ أَمْرِي فَاصْرِفْهُ عَنِّي وَاصْرِفْنِي عَنْهُ، وَاقْدُرْ لِيَ الْخَيْرَ حَيْثُ كَانَ ثُمَّ أَرْضِنِي بِهِ",
                  "Allahumma inni astakhiruka bi'ilmika, wa astaqdiruka biqudratika, wa as'aluka min fadhlikal-'azim, fa innaka taqdiru wa la aqdir, wa ta'lamu wa la a'lam, wa anta 'allamul-ghuyub. "
                  "Allahumma in kunta ta'lamu anna hazal-amra khairun li fi dini wa ma'asyi wa 'aqibati amri faqdurhu li wa yassirhu li thumma barik li fih, "
                  "wa in kunta ta'lamu anna hazal-amra syarrun li fi dini wa ma'asyi wa 'aqibati amri fasrifhu 'anni wasrifni 'anh, waqdur liyal-khaira haithu kana thumma ardhini bih.",
                  "Ya Allah, aku memohon pilihan-Mu dengan ilmu-Mu, aku memohon kekuatan dengan kekuasaan-Mu, dan aku memohon kurnia-Mu yang agung; sesungguhnya Engkau berkuasa sedangkan aku tidak, Engkau mengetahui sedangkan aku tidak, dan Engkaulah Yang Maha Mengetahui perkara ghaib. "
                  "Ya Allah, jika Engkau mengetahui bahawa urusan ini [HAJAT] baik bagiku dalam agamaku, kehidupanku dan kesudahan urusanku, maka takdirkanlah ia untukku, mudahkanlah ia bagiku dan berkatilah aku padanya. "
                  "Dan jika Engkau mengetahui bahawa urusan ini [HAJAT] buruk bagiku dalam agamaku, kehidupanku dan kesudahan urusanku, maka jauhkanlah ia daripadaku dan jauhkanlah aku daripadanya, takdirkanlah kebaikan untukku di mana sahaja ia berada, kemudian jadikanlah aku reda dengannya.",
                  "HR Al-Bukhari, no. 1162 dan no. 6382 (Jabir bin Abdillah: Rasulullah SAW mengajar istikharah dalam semua urusan seperti mengajar surah Al-Quran)",
                  "Ketika menyebut “hazal-amra” (urusan ini), sebut atau hadirkan dalam hati urusan anda.")
DOA_HAJAT = ("doa-hajat", "Doa Solat Hajat",
             "لَا إِلٰهَ إِلَّا اللّٰهُ الْحَلِيمُ الْكَرِيمُ، سُبْحَانَ اللّٰهِ رَبِّ الْعَرْشِ الْعَظِيمِ، الْحَمْدُ لِلّٰهِ رَبِّ الْعَالَمِينَ، أَسْأَلُكَ مُوجِبَاتِ رَحْمَتِكَ، وَعَزَائِمَ مَغْفِرَتِكَ، "
             "وَالْغَنِيمَةَ مِنْ كُلِّ بِرٍّ، وَالسَّلَامَةَ مِنْ كُلِّ إِثْمٍ، لَا تَدَعْ لِي ذَنْبًا إِلَّا غَفَرْتَهُ، وَلَا هَمًّا إِلَّا فَرَّجْتَهُ، وَلَا حَاجَةً هِيَ لَكَ رِضًا إِلَّا قَضَيْتَهَا يَا أَرْحَمَ الرَّاحِمِينَ",
             "La ilaha illallahul-halimul-karim, subhanallahi rabbil-'arsyil-'azim, alhamdulillahi rabbil-'alamin. As'aluka mujibati rahmatik, wa 'aza'ima maghfiratik, "
             "wal-ghanimata min kulli birr, was-salamata min kulli ithm. La tada' li zanban illa ghafartah, wa la hamman illa farrajtah, wa la hajatan hiya laka ridhan illa qadhaitaha ya arhamar-rahimin.",
             "Tiada tuhan melainkan Allah Yang Maha Penyantun lagi Maha Pemurah. Maha Suci Allah, Tuhan Arasy yang agung. Segala puji bagi Allah, Tuhan sekalian alam. Aku memohon kepada-Mu perkara yang mendatangkan rahmat-Mu, "
             "keampunan-Mu yang pasti, keuntungan daripada setiap kebaikan dan keselamatan daripada setiap dosa. Janganlah Engkau tinggalkan bagiku satu dosa pun melainkan Engkau ampunkan, tiada satu kesusahan melainkan Engkau lapangkan, "
             "dan tiada satu hajat yang Engkau redai melainkan Engkau tunaikan [HAJAT], wahai Tuhan Yang Maha Mengasihani.",
             "HR At-Tirmizi, no. 479; Ibn Majah, no. 1384. Sanadnya dhaif menurut At-Tirmizi sendiri; diamalkan oleh ramai ulama sebagai fadhail amal",
             "Selepas doa ini, mintalah hajat anda dengan bahasa sendiri.")
DOA_DHUHA = ("doa-dhuha", "Doa Selepas Solat Dhuha",
             "اللّٰهُمَّ إِنَّ الضُّحَاءَ ضُحَاؤُكَ، وَالْبَهَاءَ بَهَاؤُكَ، وَالْجَمَالَ جَمَالُكَ، وَالْقُوَّةَ قُوَّتُكَ، وَالْقُدْرَةَ قُدْرَتُكَ، وَالْعِصْمَةَ عِصْمَتُكَ. "
             "اللّٰهُمَّ إِنْ كَانَ رِزْقِي فِي السَّمَاءِ فَأَنْزِلْهُ، وَإِنْ كَانَ فِي الْأَرْضِ فَأَخْرِجْهُ، وَإِنْ كَانَ مُعْسَرًا فَيَسِّرْهُ، وَإِنْ كَانَ حَرَامًا فَطَهِّرْهُ، وَإِنْ كَانَ بَعِيدًا فَقَرِّبْهُ، "
             "بِحَقِّ ضُحَائِكَ وَبَهَائِكَ وَجَمَالِكَ وَقُوَّتِكَ وَقُدْرَتِكَ، آتِنِي مَا آتَيْتَ عِبَادَكَ الصَّالِحِينَ",
             "Allahumma innad-dhuha'a dhuha'uk, wal-baha'a baha'uk, wal-jamala jamaluk, wal-quwwata quwwatuk, wal-qudrata qudratuk, wal-'ismata 'ismatuk. "
             "Allahumma in kana rizqi fis-sama'i fa anzilh, wa in kana fil-ardhi fa akhrijh, wa in kana mu'saran fa yassirh, wa in kana haraman fa tahhirh, wa in kana ba'idan fa qarribh, "
             "bihaqqi dhuha'ika wa baha'ika wa jamalika wa quwwatika wa qudratik, atini ma atita 'ibadakas-solihin.",
             "Ya Allah, sesungguhnya waktu dhuha itu waktu-Mu, keagungan itu keagungan-Mu, keindahan itu keindahan-Mu, kekuatan itu kekuatan-Mu, kekuasaan itu kekuasaan-Mu dan pemeliharaan itu pemeliharaan-Mu. "
             "Ya Allah, jika rezekiku di langit, turunkanlah; jika di bumi, keluarkanlah; jika sukar, mudahkanlah; jika haram, sucikanlah; jika jauh, dekatkanlah; "
             "dengan hak waktu dhuha-Mu, keagungan-Mu, keindahan-Mu, kekuatan-Mu dan kekuasaan-Mu, kurniakanlah kepadaku apa yang Engkau kurniakan kepada hamba-hamba-Mu yang soleh.",
             "Doa amalan ulama (dinukil dalam I'anah at-Talibin), bukan hadis Nabi SAW. Boleh juga berdoa dengan bahasa sendiri",
             "")
DOA_WITIR = ("doa-witir", "Selepas Witir: Subḥānal-Malikil-Quddūs", "سُبْحَانَ الْمَلِكِ الْقُدُّوسِ", "Subhanal-malikil-quddus. (3×, dipanjangkan pada kali ketiga)",
             "Maha Suci Allah, Raja Yang Maha Suci.", "HR Abu Daud, no. 1430; An-Nasa'i, no. 1699", "")
DOA_TAUBAT = ("sayyidul", "Sayyidul Istighfar (penghulu istighfar)", SAYYIDUL[2], SAYYIDUL[3], SAYYIDUL[4],
              "HR Al-Bukhari, no. 6306: sesiapa membacanya dengan yakin lalu mati pada hari itu, dia ahli syurga", "")
AYAT_TAUBAT = ("ayat-taubat", "Ayat Taubat: Ali 'Imran 135", "Q:3:135", "", "", "Ayat yang dibaca Rasulullah SAW selepas menyebut hadis solat taubat (HR Abu Daud, no. 1521)", "")
AYAT_TAHAJJUD = ("ayat-tahajjud", "Perintah Tahajjud: Al-Isra' 79", "Q:17:79", "", "", "", "")

HUB = "solat-sunat/"
# (key, slug, name, short) in the hub's order; each prayer page is /solat-sunat/<slug>/
PRAYERS = [
    ("taubat", "solat-taubat", "Solat Taubat", "2 rakaat selepas melakukan dosa, diikuti istighfar"),
    ("dhuha", "solat-dhuha", "Solat Dhuha", "2–8 rakaat selepas matahari naik hingga sebelum Zohor"),
    ("hajat", "solat-hajat", "Solat Hajat", "2 rakaat (hingga 12) apabila berhajat kepada Allah"),
    ("jenazah", "solat-jenazah", "Solat Jenazah", "4 takbir berdiri, fardu kifayah"),
    ("witir", "solat-witir", "Solat Witir", "Rakaat ganjil (1–11) selepas Isyak hingga Subuh"),
    ("istikharah", "solat-istikharah", "Solat Istikharah", "2 rakaat untuk memohon pilihan terbaik"),
    ("tahajjud", "solat-tahajjud", "Solat Tahajjud", "2 rakaat atau lebih pada malam selepas tidur"),
    ("tarawih", "solat-tarawih", "Solat Tarawih", "8 atau 20 rakaat pada malam Ramadan, diakhiri witir"),
]

# rawatib (sunat before/after fardu): (prayer, before, after, muakkad note)
RAWATIB = [("Subuh", "2 rakaat (muakkad)", "–"), ("Zohor", "2 atau 4 rakaat (2 muakkad)", "2 atau 4 rakaat (2 muakkad)"),
           ("Asar", "2 atau 4 rakaat (ghairu muakkad)", "– (dilarang selepas solat Asar)"), ("Maghrib", "2 rakaat (ghairu muakkad)", "2 rakaat (muakkad)"),
           ("Isyak", "2 rakaat (ghairu muakkad)", "2 rakaat (muakkad)")]
