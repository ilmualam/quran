"""Content data for /doa-harian/, /zikir-pagi-petang/ and /belajar-tajwid/.
Quranic text (Arabic, Rumi, translation) is always read from data-surah/ by reference, never typed here.
Hadith-based texts carry their source (book + hadith number) so readers can verify them."""
import re

# ---------------- doa from Al-Quran: (surah, ayah, title, category); the doa wording is highlighted from `start` word ----------------
DOA_QURAN = [
    (2, 201, "Doa kebaikan dunia dan akhirat (Doa Sapu Jagat)", "rabbana"),
    (2, 127, "Doa amalan diterima (Nabi Ibrahim & Ismail)", "nabi"),
    (2, 128, "Doa menjadi Muslim dan zuriat yang berserah diri", "keluarga"),
    (2, 250, "Doa dikurniakan kesabaran dan keteguhan", "rabbana"),
    (2, 286, "Doa tidak dibebani melebihi kemampuan", "rabbana"),
    (3, 8, "Doa ditetapkan hati di atas hidayah", "rabbana"),
    (3, 16, "Doa keampunan dan dipelihara daripada neraka", "ampun"),
    (3, 53, "Doa dicatat bersama orang yang menjadi saksi", "rabbana"),
    (3, 147, "Doa keampunan dan diteguhkan pendirian", "ampun"),
    (3, 193, "Doa diampunkan dan diwafatkan bersama orang baik", "ampun"),
    (3, 194, "Doa memperoleh janji Allah dan tidak dihinakan", "rabbana"),
    (3, 38, "Doa memohon zuriat yang baik (Nabi Zakaria)", "keluarga"),
    (7, 23, "Doa taubat Nabi Adam dan Hawa", "ampun"),
    (10, 85, "Doa tidak dijadikan fitnah bagi orang zalim", "rabbana"),
    (14, 40, "Doa menjadi orang yang mendirikan solat (Nabi Ibrahim)", "nabi"),
    (14, 41, "Doa keampunan untuk diri, ibu bapa dan orang beriman", "keluarga"),
    (17, 24, "Doa untuk kedua ibu bapa", "keluarga"),
    (17, 80, "Doa dimasukkan dan dikeluarkan dengan cara yang benar", "urusan"),
    (18, 10, "Doa rahmat dan petunjuk (Ashabul Kahfi)", "rabbana"),
    (20, 25, "Doa dilapangkan dada (Nabi Musa)", "urusan"),
    (20, 114, "Doa ditambahkan ilmu", "urusan"),
    (21, 83, "Doa ketika ditimpa kesusahan (Nabi Ayub)", "nabi"),
    (21, 87, "Doa Nabi Yunus dalam perut ikan", "nabi"),
    (21, 89, "Doa tidak dibiarkan bersendirian (Nabi Zakaria)", "keluarga"),
    (23, 97, "Doa berlindung daripada hasutan syaitan", "urusan"),
    (23, 118, "Doa keampunan dan rahmat", "ampun"),
    (25, 65, "Doa dijauhkan daripada azab Jahannam", "rabbana"),
    (25, 74, "Doa pasangan dan zuriat penyejuk mata", "keluarga"),
    (27, 19, "Doa bersyukur dan beramal soleh (Nabi Sulaiman)", "nabi"),
    (28, 16, "Doa pengakuan dosa (Nabi Musa)", "ampun"),
    (28, 24, "Doa memohon rezeki dan kebaikan (Nabi Musa)", "urusan"),
    (37, 100, "Doa dikurniakan anak yang soleh", "keluarga"),
    (59, 10, "Doa untuk saudara seiman dan hati yang bersih", "rabbana"),
    (60, 4, "Doa bertawakal dan kembali kepada Allah", "rabbana"),
    (66, 8, "Doa disempurnakan cahaya dan keampunan", "ampun"),
    (71, 28, "Doa keampunan untuk ibu bapa dan orang beriman (Nabi Nuh)", "keluarga"),
]
# the highlighted doa wording starts at the first "Rabbana"/"Rabbi" in the ayah, except where it opens differently
DOA_START = {(21, 83): 5, (21, 87): 14}
_MARKS = re.compile("[\u064B-\u065F\u0670\u06D6-\u06ED]")


def doa_start(s, a, words):
    if (s, a) in DOA_START:
        return DOA_START[(s, a)]
    for i, w in enumerate(words):
        if _MARKS.sub("", w).replace("ٱ", "ا").replace("آ", "ا") in ("ربنا", "رب"):
            return i
    return 0


DOA_CAT = [("rabbana", "Doa Rabbana"), ("nabi", "Doa Para Nabi"), ("keluarga", "Ibu Bapa & Keluarga"),
           ("ampun", "Taubat & Keampunan"), ("urusan", "Ilmu, Rezeki & Urusan")]

# ---------------- doa harian (hadith); a=Arabic, r=Rumi, m=maksud, s=source ----------------
DOA_HARIAN = [
    ("bangun-tidur", "Doa Bangun Tidur", "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ",
     "Alhamdulillahil-lazi ahyana ba'da ma amatana wa ilaihin-nusyur",
     "Segala puji bagi Allah yang menghidupkan kami setelah mematikan kami, dan kepada-Nya kami dibangkitkan.", "HR Al-Bukhari, no. 6312"),
    ("sebelum-tidur", "Doa Sebelum Tidur", "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
     "Bismikallahumma amutu wa ahya", "Dengan nama-Mu ya Allah, aku mati dan aku hidup.", "HR Al-Bukhari, no. 6324"),
    ("sebelum-makan", "Doa Sebelum Makan", "بِسْمِ اللَّهِ",
     "Bismillah", "Dengan nama Allah. Jika terlupa di awal, baca: Bismillahi awwalahu wa akhirah (Dengan nama Allah pada awal dan akhirnya).",
     "HR Abu Daud, no. 3767; At-Tirmizi, no. 1858"),
    ("selepas-makan", "Doa Selepas Makan", "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَذَا وَرَزَقَنِيهِ مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ",
     "Alhamdulillahil-lazi at'amani haza wa razaqanihi min ghairi haulin minni wa la quwwah",
     "Segala puji bagi Allah yang memberiku makanan ini dan merezekikannya kepadaku tanpa daya dan kekuatan daripadaku.",
     "HR Abu Daud, no. 4023; At-Tirmizi, no. 3458"),
    ("masuk-tandas", "Doa Masuk Tandas", "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبُثِ وَالْخَبَائِثِ",
     "Allahumma inni a'uzu bika minal-khubusi wal-khaba'is", "Ya Allah, aku berlindung kepada-Mu daripada syaitan lelaki dan syaitan perempuan.",
     "HR Al-Bukhari, no. 142; Muslim, no. 375"),
    ("keluar-tandas", "Doa Keluar Tandas", "غُفْرَانَكَ", "Ghufranak", "(Aku memohon) keampunan-Mu.", "HR Abu Daud, no. 30; At-Tirmizi, no. 7"),
    ("keluar-rumah", "Doa Keluar Rumah", "بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ، لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ",
     "Bismillahi tawakkaltu 'alallah, la haula wa la quwwata illa billah",
     "Dengan nama Allah, aku bertawakal kepada Allah. Tiada daya dan kekuatan melainkan dengan (pertolongan) Allah.",
     "HR Abu Daud, no. 5095; At-Tirmizi, no. 3426"),
    ("masuk-masjid", "Doa Masuk Masjid", "اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ",
     "Allahummaftah li abwaba rahmatik", "Ya Allah, bukakanlah untukku pintu-pintu rahmat-Mu.", "HR Muslim, no. 713"),
    ("keluar-masjid", "Doa Keluar Masjid", "اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ",
     "Allahumma inni as'aluka min fadlik", "Ya Allah, sesungguhnya aku memohon kurnia-Mu.", "HR Muslim, no. 713"),
    ("pakai-baju", "Doa Memakai Pakaian", "الْحَمْدُ لِلَّهِ الَّذِي كَسَانِي هَذَا وَرَزَقَنِيهِ مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ",
     "Alhamdulillahil-lazi kasani haza wa razaqanihi min ghairi haulin minni wa la quwwah",
     "Segala puji bagi Allah yang memakaikan aku pakaian ini dan merezekikannya kepadaku tanpa daya dan kekuatan daripadaku.",
     "HR Abu Daud, no. 4023"),
    ("hujan", "Doa Ketika Hujan", "اللَّهُمَّ صَيِّبًا نَافِعًا", "Allahumma sayyiban nafi'a",
     "Ya Allah, jadikanlah hujan ini hujan yang bermanfaat.", "HR Al-Bukhari, no. 1032"),
    ("musibah", "Doa Ditimpa Musibah", "إِنَّا لِلَّهِ وَإِنَّا إِلَيْهِ رَاجِعُونَ، اللَّهُمَّ أْجُرْنِي فِي مُصِيبَتِي وَأَخْلِفْ لِي خَيْرًا مِنْهَا",
     "Inna lillahi wa inna ilaihi raji'un, Allahumma'jurni fi musibati wa akhlif li khairan minha",
     "Sesungguhnya kami milik Allah dan kepada-Nya kami kembali. Ya Allah, berilah aku pahala dalam musibahku dan gantikanlah untukku yang lebih baik daripadanya.",
     "HR Muslim, no. 918"),
    ("dukacita", "Doa Ketika Resah & Dukacita",
     "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ، وَالْعَجْزِ وَالْكَسَلِ، وَالْبُخْلِ وَالْجُبْنِ، وَضَلَعِ الدَّيْنِ وَغَلَبَةِ الرِّجَالِ",
     "Allahumma inni a'uzu bika minal-hammi wal-hazan, wal-'ajzi wal-kasal, wal-bukhli wal-jubn, wa dala'id-daini wa ghalabatir-rijal",
     "Ya Allah, aku berlindung kepada-Mu daripada kerisauan dan kesedihan, kelemahan dan kemalasan, kebakhilan dan sifat pengecut, beban hutang dan penindasan manusia.",
     "HR Al-Bukhari, no. 6369"),
    ("bersin", "Doa Bersin & Menjawabnya", "الْحَمْدُ لِلَّهِ ・ يَرْحَمُكَ اللَّهُ ・ يَهْدِيكُمُ اللَّهُ وَيُصْلِحُ بَالَكُمْ",
     "Alhamdulillah · Yarhamukallah · Yahdikumullahu wa yuslihu balakum",
     "Orang yang bersin: Segala puji bagi Allah. Yang mendengar: Semoga Allah merahmatimu. Orang yang bersin membalas: Semoga Allah memberi petunjuk kepadamu dan memperbaiki keadaanmu.",
     "HR Al-Bukhari, no. 6224"),
]

# ---------------- ayat amalan (Quran refs + hadith on its virtue) ----------------
AYAT_AMALAN = [
    ("ayat-kursi", "Ayat Kursi", [(2, 255)], "Dibaca sebelum tidur: dipelihara oleh Allah sepanjang malam dan syaitan tidak mendekati (HR Al-Bukhari, no. 2311). Dibaca selepas solat fardu (HR An-Nasa'i dalam As-Sunan Al-Kubra)."),
    ("akhir-baqarah", "Dua Ayat Terakhir Surah Al-Baqarah", [(2, 285), (2, 286)], "Sesiapa membacanya pada waktu malam, kedua-duanya mencukupinya (HR Al-Bukhari, no. 5009; Muslim, no. 807)."),
    ("tiga-qul", "Al-Ikhlas, Al-Falaq & An-Nas (3 Qul)", [(112, 1), (113, 1), (114, 1)], "Dibaca tiga kali pada waktu pagi dan petang, mencukupi daripada segala sesuatu (HR Abu Daud, no. 5082; At-Tirmizi, no. 3575). Al-Ikhlas menyamai sepertiga Al-Quran (HR Al-Bukhari, no. 5013)."),
    ("seribu-dinar", "Ayat Seribu Dinar (At-Talaq 2–3)", [(65, 2), (65, 3)], "Janji Allah kepada orang bertakwa: diberi jalan keluar dan rezeki dari arah yang tidak disangka. Nama “Ayat Seribu Dinar” ialah nama popular dalam masyarakat, bukan nama daripada hadis."),
    ("hasbunallah", "Hasbunallah wa Ni'mal Wakil", [(3, 173)], "Kalimah yang diucapkan Nabi Ibrahim ketika dicampak ke dalam api dan Nabi Muhammad SAW ketika diancam musuh (HR Al-Bukhari, no. 4563)."),
]

# ---------------- zikir: (id, title, arabic, rumi, maksud, count, source, note) ----------------
Z_PAGI_PETANG = [
    ("kursi", "Ayat Kursi", "Q2:255", None, None, 1, "Dibaca pagi dan petang: dipelihara daripada gangguan jin (HR An-Nasa'i dalam As-Sunan Al-Kubra; Al-Hakim)", ""),
    ("qul", "Al-Ikhlas, Al-Falaq & An-Nas", "Q112-114", None, None, 3, "HR Abu Daud, no. 5082; At-Tirmizi, no. 3575", "Baca ketiga-tiga surah, ulang 3 kali."),
    ("asbahna", "Asbahna wa asbahal-mulku lillah",
     "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ، رَبِّ أَسْأَلُكَ خَيْرَ مَا فِي هَذَا الْيَوْمِ وَخَيْرَ مَا بَعْدَهُ، وَأَعُوذُ بِكَ مِنْ شَرِّ مَا فِي هَذَا الْيَوْمِ وَشَرِّ مَا بَعْدَهُ، رَبِّ أَعُوذُ بِكَ مِنَ الْكَسَلِ وَسُوءِ الْكِبَرِ، رَبِّ أَعُوذُ بِكَ مِنْ عَذَابٍ فِي النَّارِ وَعَذَابٍ فِي الْقَبْرِ",
     "Asbahna wa asbahal-mulku lillah, walhamdulillah, la ilaha illallahu wahdahu la syarika lah, lahul-mulku wa lahul-hamdu wa huwa 'ala kulli syai'in qadir. Rabbi as'aluka khaira ma fi hazal-yaumi wa khaira ma ba'dah, wa a'uzu bika min syarri ma fi hazal-yaumi wa syarri ma ba'dah. Rabbi a'uzu bika minal-kasali wa su'il-kibar. Rabbi a'uzu bika min 'azabin fin-nari wa 'azabin fil-qabr",
     "Kami berpagi dan kerajaan berpagi milik Allah. Segala puji bagi Allah, tiada tuhan melainkan Allah Yang Esa, tiada sekutu bagi-Nya; bagi-Nya kerajaan dan pujian, dan Dia Maha Berkuasa atas segala sesuatu. Wahai Tuhanku, aku memohon kebaikan hari ini dan kebaikan selepasnya, dan aku berlindung daripada keburukan hari ini dan keburukan selepasnya. Wahai Tuhanku, aku berlindung daripada kemalasan dan keburukan usia tua. Wahai Tuhanku, aku berlindung daripada azab neraka dan azab kubur.",
     1, "HR Muslim, no. 2723", "Petang: tukar “asbahna wa asbahal-mulku” kepada “amsaina wa amsal-mulku” (أَمْسَيْنَا وَأَمْسَى الْمُلْكُ) dan “hazal-yaum” kepada “hazihil-lailah” (هَذِهِ اللَّيْلَةِ)."),
    ("bika", "Allahumma bika asbahna",
     "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ",
     "Allahumma bika asbahna, wa bika amsaina, wa bika nahya, wa bika namutu, wa ilaikan-nusyur",
     "Ya Allah, dengan-Mu kami berpagi, dengan-Mu kami berpetang, dengan-Mu kami hidup, dengan-Mu kami mati, dan kepada-Mu kami dibangkitkan.",
     1, "HR At-Tirmizi, no. 3391", "Petang: “Allahumma bika amsaina, wa bika asbahna, wa bika nahya, wa bika namutu, wa ilaikal-masir” (وَإِلَيْكَ الْمَصِيرُ)."),
    ("sayyidul", "Sayyidul Istighfar",
     "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي، فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ",
     "Allahumma anta rabbi la ilaha illa anta, khalaqtani wa ana 'abduk, wa ana 'ala 'ahdika wa wa'dika mastata't, a'uzu bika min syarri ma sana't, abu'u laka bini'matika 'alayya, wa abu'u bizanbi faghfir li, fa innahu la yaghfiruz-zunuba illa anta",
     "Ya Allah, Engkaulah Tuhanku, tiada tuhan melainkan Engkau. Engkau menciptakan aku dan aku hamba-Mu. Aku berpegang pada janji-Mu sedaya upayaku. Aku berlindung kepada-Mu daripada keburukan perbuatanku. Aku mengakui nikmat-Mu kepadaku dan mengakui dosaku, maka ampunkanlah aku, kerana tiada yang mengampunkan dosa melainkan Engkau.",
     1, "HR Al-Bukhari, no. 6306", "Sesiapa membacanya dengan yakin pada siang hari lalu meninggal sebelum petang, dia ahli syurga; demikian juga pada malam hari."),
    ("bismillah", "Bismillahil-lazi la yadurru",
     "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ",
     "Bismillahil-lazi la yadurru ma'asmihi syai'un fil-ardi wa la fis-sama', wa huwas-sami'ul-'alim",
     "Dengan nama Allah yang tidak memudaratkan sesuatu pun di bumi dan di langit bersama nama-Nya, dan Dia Maha Mendengar lagi Maha Mengetahui.",
     3, "HR Abu Daud, no. 5088; At-Tirmizi, no. 3388", ""),
    ("raditu", "Raditu billahi rabba",
     "رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ نَبِيًّا",
     "Raditu billahi rabba, wa bil-islami dina, wa bi Muhammadin sallallahu 'alaihi wa sallama nabiyya",
     "Aku reda Allah sebagai Tuhan, Islam sebagai agama dan Muhammad SAW sebagai nabi.", 3, "HR Abu Daud, no. 5072", ""),
    ("hasbiya", "Hasbiyallahu la ilaha illa huwa",
     "حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ",
     "Hasbiyallahu la ilaha illa huwa, 'alaihi tawakkaltu wa huwa rabbul-'arsyil-'azim",
     "Cukuplah Allah bagiku, tiada tuhan melainkan Dia. Kepada-Nya aku bertawakal dan Dia Tuhan Arasy yang agung.", 7, "HR Abu Daud, no. 5081", ""),
    ("afini", "Allahumma 'afini fi badani",
     "اللَّهُمَّ عَافِنِي فِي بَدَنِي، اللَّهُمَّ عَافِنِي فِي سَمْعِي، اللَّهُمَّ عَافِنِي فِي بَصَرِي، لَا إِلَهَ إِلَّا أَنْتَ",
     "Allahumma 'afini fi badani, Allahumma 'afini fi sam'i, Allahumma 'afini fi basari, la ilaha illa anta",
     "Ya Allah, sihatkanlah tubuhku. Ya Allah, sihatkanlah pendengaranku. Ya Allah, sihatkanlah penglihatanku. Tiada tuhan melainkan Engkau.",
     3, "HR Abu Daud, no. 5090", ""),
    ("afiah", "Doa memohon keampunan dan keselamatan",
     "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ، اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي دِينِي وَدُنْيَايَ وَأَهْلِي وَمَالِي، اللَّهُمَّ اسْتُرْ عَوْرَاتِي وَآمِنْ رَوْعَاتِي، اللَّهُمَّ احْفَظْنِي مِنْ بَيْنِ يَدَيَّ وَمِنْ خَلْفِي وَعَنْ يَمِينِي وَعَنْ شِمَالِي وَمِنْ فَوْقِي، وَأَعُوذُ بِعَظَمَتِكَ أَنْ أُغْتَالَ مِنْ تَحْتِي",
     "Allahumma inni as'alukal-'afwa wal-'afiyah fid-dunya wal-akhirah. Allahumma inni as'alukal-'afwa wal-'afiyah fi dini wa dunyaya wa ahli wa mali. Allahummastur 'aurati wa amin rau'ati. Allahummahfazni min baini yadayya wa min khalfi wa 'an yamini wa 'an syimali wa min fauqi, wa a'uzu bi'azamatika an ughtala min tahti",
     "Ya Allah, aku memohon keampunan dan keselamatan di dunia dan akhirat. Ya Allah, aku memohon keampunan dan keselamatan dalam agamaku, duniaku, keluargaku dan hartaku. Ya Allah, tutuplah aibku dan tenangkanlah ketakutanku. Ya Allah, peliharalah aku dari hadapan, belakang, kanan, kiri dan atasku, dan aku berlindung dengan keagungan-Mu daripada dibinasakan dari bawahku.",
     1, "HR Abu Daud, no. 5074", ""),
    ("hayyu", "Ya Hayyu ya Qayyum",
     "يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ، أَصْلِحْ لِي شَأْنِي كُلَّهُ، وَلَا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ",
     "Ya Hayyu ya Qayyum, birahmatika astaghis, aslih li sya'ni kullah, wa la takilni ila nafsi tarfata 'ain",
     "Wahai Yang Maha Hidup, wahai Yang Maha Berdiri Sendiri, dengan rahmat-Mu aku memohon pertolongan. Perbaikilah seluruh urusanku dan jangan serahkan aku kepada diriku walau sekelip mata.",
     1, "HR An-Nasa'i dalam As-Sunan Al-Kubra; Al-Hakim", ""),
    ("kalimat", "A'uzu bikalimatillahit-tammat (petang)",
     "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ",
     "A'uzu bikalimatillahit-tammati min syarri ma khalaq", "Aku berlindung dengan kalimah-kalimah Allah yang sempurna daripada keburukan makhluk yang diciptakan-Nya.",
     3, "HR Muslim, no. 2709", "Lazim dibaca pada waktu petang."),
    ("subhanallah-wabihamdih", "Subhanallahi wa bihamdih",
     "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "Subhanallahi wa bihamdih", "Maha Suci Allah dan segala puji bagi-Nya.", 100, "HR Muslim, no. 2692", "Tiada yang membawa amalan lebih baik pada hari kiamat kecuali orang yang membaca sama banyak atau lebih."),
    ("tahlil", "La ilaha illallahu wahdah",
     "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
     "La ilaha illallahu wahdahu la syarika lah, lahul-mulku wa lahul-hamdu wa huwa 'ala kulli syai'in qadir",
     "Tiada tuhan melainkan Allah Yang Esa, tiada sekutu bagi-Nya. Bagi-Nya kerajaan dan bagi-Nya segala puji, dan Dia Maha Berkuasa atas segala sesuatu.",
     100, "HR Al-Bukhari, no. 3293; Muslim, no. 2691", "100 kali sehari: pahala memerdekakan 10 hamba, 100 kebaikan, dihapuskan 100 kesalahan dan terpelihara daripada syaitan hingga petang."),
    ("istighfar", "Astaghfirullah wa atubu ilaih",
     "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ", "Astaghfirullaha wa atubu ilaih", "Aku memohon ampun kepada Allah dan bertaubat kepada-Nya.", 100, "HR Muslim, no. 2702", "Rasulullah SAW beristighfar 100 kali sehari."),
]
Z_SOLAT = [
    ("s-istighfar", "Istighfar", "أَسْتَغْفِرُ اللَّهَ", "Astaghfirullah", "Aku memohon ampun kepada Allah.", 3, "HR Muslim, no. 591", ""),
    ("s-salam", "Allahumma antas-salam",
     "اللَّهُمَّ أَنْتَ السَّلَامُ وَمِنْكَ السَّلَامُ، تَبَارَكْتَ يَا ذَا الْجَلَالِ وَالْإِكْرَامِ",
     "Allahumma antas-salam wa minkas-salam, tabarakta ya zal-jalali wal-ikram",
     "Ya Allah, Engkaulah As-Salam (Maha Sejahtera) dan daripada-Mu kesejahteraan. Maha Berkat Engkau, wahai Tuhan yang mempunyai keagungan dan kemuliaan.", 1, "HR Muslim, no. 591", ""),
    ("s-mani", "La mani'a lima a'tait",
     "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ، اللَّهُمَّ لَا مَانِعَ لِمَا أَعْطَيْتَ، وَلَا مُعْطِيَ لِمَا مَنَعْتَ، وَلَا يَنْفَعُ ذَا الْجَدِّ مِنْكَ الْجَدُّ",
     "La ilaha illallahu wahdahu la syarika lah, lahul-mulku wa lahul-hamdu wa huwa 'ala kulli syai'in qadir. Allahumma la mani'a lima a'taita, wa la mu'tiya lima mana'ta, wa la yanfa'u zal-jaddi minkal-jadd",
     "Tiada tuhan melainkan Allah Yang Esa... Ya Allah, tiada yang dapat menghalang apa yang Engkau beri, tiada yang dapat memberi apa yang Engkau halang, dan kekayaan tidak memberi manfaat kepada pemiliknya di sisi-Mu.",
     1, "HR Al-Bukhari, no. 844; Muslim, no. 593", ""),
    ("s-kursi", "Ayat Kursi", "Q2:255", None, None, 1, "HR An-Nasa'i dalam As-Sunan Al-Kubra: tiada yang menghalangnya masuk syurga melainkan kematian", ""),
    ("s-tasbih", "Subhanallah", "سُبْحَانَ اللَّهِ", "Subhanallah", "Maha Suci Allah.", 33, "HR Muslim, no. 597", ""),
    ("s-tahmid", "Alhamdulillah", "الْحَمْدُ لِلَّهِ", "Alhamdulillah", "Segala puji bagi Allah.", 33, "HR Muslim, no. 597", ""),
    ("s-takbir", "Allahu Akbar", "اللَّهُ أَكْبَرُ", "Allahu Akbar", "Allah Maha Besar.", 33, "HR Muslim, no. 597", ""),
    ("s-tahlil", "Penutup 100",
     "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
     "La ilaha illallahu wahdahu la syarika lah, lahul-mulku wa lahul-hamdu wa huwa 'ala kulli syai'in qadir",
     "Tiada tuhan melainkan Allah Yang Esa, tiada sekutu bagi-Nya. Bagi-Nya kerajaan dan bagi-Nya segala puji, dan Dia Maha Berkuasa atas segala sesuatu.",
     1, "HR Muslim, no. 597", "Dosa diampunkan walaupun sebanyak buih di lautan."),
    ("s-qul", "Al-Ikhlas, Al-Falaq & An-Nas", "Q112-114", None, None, 1, "HR Abu Daud, no. 1523", ""),
    ("s-ainni", "Allahumma a'inni 'ala zikrik",
     "اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ",
     "Allahumma a'inni 'ala zikrika wa syukrika wa husni 'ibadatik", "Ya Allah, bantulah aku untuk mengingati-Mu, bersyukur kepada-Mu dan memperelok ibadahku kepada-Mu.",
     1, "HR Abu Daud, no. 1522", "Wasiat Rasulullah SAW kepada Mu'az bin Jabal untuk dibaca selepas setiap solat."),
]
Z_TIDUR = [
    ("t-kursi", "Ayat Kursi", "Q2:255", None, None, 1, "HR Al-Bukhari, no. 2311", ""),
    ("t-baqarah", "Dua ayat terakhir Al-Baqarah", "Q2:285-286", None, None, 1, "HR Al-Bukhari, no. 5009; Muslim, no. 807", ""),
    ("t-qul", "3 Qul, tiup ke tapak tangan & sapu badan", "Q112-114", None, None, 3, "HR Al-Bukhari, no. 5017", ""),
    ("t-tasbih", "Subhanallah", "سُبْحَانَ اللَّهِ", "Subhanallah", "Maha Suci Allah.", 33, "HR Al-Bukhari, no. 6318; Muslim, no. 2727", ""),
    ("t-tahmid", "Alhamdulillah", "الْحَمْدُ لِلَّهِ", "Alhamdulillah", "Segala puji bagi Allah.", 33, "HR Al-Bukhari, no. 6318; Muslim, no. 2727", ""),
    ("t-takbir", "Allahu Akbar", "اللَّهُ أَكْبَرُ", "Allahu Akbar", "Allah Maha Besar.", 34, "HR Al-Bukhari, no. 6318; Muslim, no. 2727", "Diajar kepada Fatimah dan Ali RA: lebih baik daripada seorang pembantu."),
    ("t-bismika", "Doa sebelum tidur", "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا", "Bismikallahumma amutu wa ahya", "Dengan nama-Mu ya Allah, aku mati dan aku hidup.", 1, "HR Al-Bukhari, no. 6324", ""),
]

# ---------------- tajwid: (rule id, rule name, surah, ayah, word indexes, explanation) ----------------
TAJWID = [
    ("izhar", "Izhar Halqi", 92, 5, [1, 2], "Nun mati bertemu huruf halqum (ء ه ع ح غ خ): nun dibaca jelas tanpa dengung."),
    ("izhar", "Izhar Halqi", 106, 4, [5, 6], "Nun mati bertemu خ: nun dibaca jelas."),
    ("idgham-g", "Idgham Maal Ghunnah", 99, 7, [0, 1], "Nun mati bertemu ي ن م و: nun dimasukkan ke huruf berikutnya dengan dengung 2 harakat."),
    ("idgham-g", "Idgham Maal Ghunnah", 2, 25, [33, 34], "Tanwin bertemu م: dimasukkan dengan dengung."),
    ("idgham-b", "Idgham Bila Ghunnah", 2, 5, [3, 4], "Nun mati bertemu ل atau ر: nun dimasukkan tanpa dengung."),
    ("iqlab", "Iqlab", 104, 4, [2], "Nun mati bertemu ب: nun ditukar kepada bunyi mim dengan dengung (tanda mim kecil ۢ)."),
    ("ikhfa", "Ikhfa' Haqiqi", 113, 2, [0, 1], "Nun mati bertemu salah satu 15 huruf ikhfa': nun disamarkan dengan dengung."),
    ("ikhfa", "Ikhfa' Haqiqi", 97, 4, [6, 7], "Nun mati bertemu ك: dibaca samar dengan dengung."),
    ("ikhfa-s", "Ikhfa' Syafawi", 105, 4, [0, 1], "Mim mati bertemu ب: mim disamarkan dengan dengung."),
    ("idgham-m", "Idgham Mithlain (Mim)", 104, 8, [1, 2], "Mim mati bertemu م: dimasukkan dengan dengung."),
    ("izhar-s", "Izhar Syafawi", 105, 1, [0, 1], "Mim mati bertemu selain ب dan م: mim dibaca jelas."),
    ("qalqalah-s", "Qalqalah Sughra", 112, 3, [0, 1], "Huruf qalqalah (ق ط ب ج د) mati asli di tengah bacaan: dipantulkan ringan."),
    ("qalqalah-k", "Qalqalah Kubra", 113, 1, [3], "Huruf qalqalah di hujung bacaan ketika berhenti (waqaf): dipantulkan lebih kuat."),
    ("qalqalah-k", "Qalqalah Kubra", 112, 1, [3], "Berhenti pada أَحَدٌ: dal dipantulkan kuat."),
    ("mad-asli", "Mad Asli (Tabi'i)", 1, 4, [0], "Huruf mad tanpa sebab hamzah atau sukun: dipanjangkan 2 harakat."),
    ("mad-wajib", "Mad Wajib Muttasil", 110, 1, [1], "Huruf mad bertemu hamzah dalam satu kalimah: 4 atau 5 harakat."),
    ("mad-jaiz", "Mad Jaiz Munfasil", 108, 1, [0, 1], "Huruf mad di hujung kalimah bertemu hamzah di awal kalimah berikutnya: 4 atau 5 harakat (riwayat Hafs, Tariq Asy-Syatibiyyah)."),
    ("mad-aridh", "Mad 'Aridh Lissukun", 1, 2, [3], "Huruf mad sebelum huruf terakhir yang disukunkan kerana waqaf: 2, 4 atau 6 harakat."),
    ("mad-lazim", "Mad Lazim Kalimi Muthaqqal", 1, 7, [8], "Huruf mad bertemu huruf bersyaddah dalam satu kalimah: 6 harakat."),
    ("mad-lin", "Mad Lin", 106, 1, [1], "Wau atau ya mati selepas baris atas, ketika waqaf: 2, 4 atau 6 harakat."),
    ("mad-silah", "Mad Silah Sughra", 110, 3, [5, 6], "Ha dhamir antara dua huruf berbaris tidak bertemu hamzah: dipanjangkan 2 harakat."),
    ("mad-iwadh", "Mad 'Iwadh", 110, 2, [6], "Waqaf pada tanwin baris atas: dibaca alif 2 harakat (afwaja)."),
    ("mad-badal", "Mad Badal", 103, 3, [2], "Hamzah diikuti huruf mad dalam satu kalimah: 2 harakat."),
    ("ghunnah", "Ghunnah Musyaddadah", 108, 3, [0], "Nun atau mim bersyaddah: didengungkan 2 harakat."),
    ("ghunnah", "Ghunnah Musyaddadah", 102, 8, [0], "Mim bersyaddah dalam ثُمَّ: didengungkan."),
    ("syamsiah", "Alif Lam Syamsiah", 91, 1, [0], "Alif lam bertemu huruf syamsiah: lam tidak dibaca, huruf selepasnya bersyaddah."),
    ("syamsiah", "Alif Lam Syamsiah", 1, 4, [2], "Lam tidak dibaca: ad-din."),
    ("qamariah", "Alif Lam Qamariah", 91, 2, [0], "Alif lam bertemu huruf qamariah: lam dibaca jelas (sukun)."),
    ("qamariah", "Alif Lam Qamariah", 2, 2, [1], "Lam dibaca jelas: al-kitab."),
    ("lam-tafkhim", "Lam Jalalah Tafkhim", 112, 1, [1, 2], "Lafaz Allah selepas baris atas atau hadapan: lam dibaca tebal."),
    ("lam-tarqiq", "Lam Jalalah Tarqiq", 1, 1, [0, 1], "Lafaz Allah selepas baris bawah: lam dibaca nipis."),
]

# letters for the nun/mim analyser
HURUF = "ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن و ه ء ي".split()
HALQI = set("ء ه ع ح غ خ".split())
YANMU = set("ي ن م و".split())
LR = set("ل ر".split())
IKHFA = set("ت ث ج د ذ ز س ش ص ض ط ظ ف ق ك".split())
assert len(IKHFA) == 15
