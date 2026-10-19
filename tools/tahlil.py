"""Tahlil ringkas as read in Malaysia (Syafi'i), in order. Quranic text, rumi and translation are read from data-surah/
by reference (whole ayat), or sliced from the ayat at a given word for the short Quranic phrases; nothing Quranic is
typed here. Non-Quranic zikir carry their hadith source. The doa for the deceased (HR Muslim, no. 963) has its pronoun
in four forms so the page can switch between one man, one woman, men/mixed and women."""
import re

# (id, title, kind, payload, count, source, note)
#   kind "q": payload = [(surah, first ayah, last ayah)]
#   kind "qs": payload = (surah, ayah, first word of the slice, rumi, maksud)  -- a phrase cut from one ayah
#   kind "z": payload = (arabic, rumi, maksud)
#   kind "hadiah": the dedication (Malay), personalised with the name of the deceased
#   kind "doa": the doa for the deceased, pronoun switched by the page
STEPS = [
    ("hadiah", "Hadiah Al-Fatihah", "hadiah", None, 0, "", ""),
    ("fatihah1", "Surah Al-Fatihah", "q", [(1, 1, 7)], 1, "", ""),
    ("ikhlas", "Surah Al-Ikhlas", "q", [(112, 1, 4)], 3, "HR Al-Bukhari, no. 5013: menyamai sepertiga Al-Quran",
     "Selepas setiap bacaan: “Lā ilāha illallāhu wallāhu akbar” (لَا إِلٰهَ إِلَّا اللهُ وَاللهُ أَكْبَرُ)."),
    ("falaq", "Surah Al-Falaq", "q", [(113, 1, 5)], 1, "", "Diikuti “Lā ilāha illallāhu wallāhu akbar”."),
    ("nas", "Surah An-Nas", "q", [(114, 1, 6)], 1, "",
     "Diikuti “Lā ilāha illallāhu wallāhu akbar, Allāhu akbar wa lillāhil-ḥamd” (لَا إِلٰهَ إِلَّا اللهُ وَاللهُ أَكْبَرُ، اللهُ أَكْبَرُ وَلِلّٰهِ الْحَمْدُ)."),
    ("fatihah2", "Surah Al-Fatihah", "q", [(1, 1, 7)], 1, "", ""),
    ("baqarah1", "Awal Surah Al-Baqarah (ayat 1–5)", "q", [(2, 1, 5)], 1, "", ""),
    ("baqarah163", "Al-Baqarah ayat 163", "q", [(2, 163, 163)], 1, "", ""),
    ("kursi", "Ayat Kursi (Al-Baqarah 255)", "q", [(2, 255, 255)], 1, "HR Muslim, no. 810: ayat paling agung dalam Al-Quran", ""),
    ("baqarah284", "Akhir Surah Al-Baqarah (ayat 284–286)", "q", [(2, 284, 286)], 1, "HR Al-Bukhari, no. 5009; Muslim, no. 807 (ayat 285–286)", ""),
    ("irhamna", "Irḥamnā yā arḥamar-rāḥimīn", "z", ("ارْحَمْنَا يَا أَرْحَمَ الرَّاحِمِينَ", "Irhamna ya arhamar-rahimin",
     "Rahmatilah kami, wahai Tuhan Yang Maha Pengasih daripada segala yang mengasihani."), 7,
     "Arhamur-Rahimin: sifat Allah dalam Al-A'raf 7:151 dan Yusuf 12:64", ""),
    ("hud73", "Rahmatullāhi wa barakātuh", "qs", (11, 73, "رحمت", "Rahmatullahi wa barakatuhu 'alaikum ahlal-bait, innahu hamidum majid",
     "Rahmat Allah dan berkat-Nya tercurah ke atas kamu, wahai ahlul bait. Sesungguhnya Allah Maha Terpuji lagi Maha Mulia."), 1, "", ""),
    ("ahzab33", "Innamā yurīdullāh", "qs", (33, 33, "إنما", "Innama yuridullahu liyuzhiba 'ankumur-rijsa ahlal-baiti wa yutahhirakum tathira",
     "Sesungguhnya Allah hanya bertujuan hendak menghapuskan dosa daripada kamu, wahai ahlul bait, dan membersihkan kamu sebersih-bersihnya."), 1, "", ""),
    ("ahzab56", "Ayat selawat (Al-Ahzab 56)", "q", [(33, 56, 56)], 1, "", ""),
    ("selawat1", "Selawat ke atas Nabi", "z", ("اللَّهُمَّ صَلِّ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِ سَيِّدِنَا مُحَمَّدٍ",
     "Allahumma solli 'ala saiyidina Muhammad, wa 'ala ali saiyidina Muhammad",
     "Ya Allah, limpahkanlah selawat ke atas penghulu kami Nabi Muhammad dan ke atas keluarga penghulu kami Nabi Muhammad."), 1,
     "Perintah berselawat: Al-Ahzab 33:56; HR Muslim, no. 408 (sepuluh rahmat bagi setiap selawat)", ""),
    ("hasbunallah", "Ḥasbunallāh wa ni'mal-wakīl", "qs", (3, 173, "حسبنا", "Hasbunallahu wa ni'mal-wakil",
     "Cukuplah Allah bagi kami, dan Dia sebaik-baik Pengurus."), 1, "", ""),
    ("nimal", "Ni'mal-maulā wa ni'man-naṣīr", "qs", (8, 40, "نعم", "Ni'mal-maula wa ni'man-nasir",
     "Dialah sebaik-baik Pelindung dan sebaik-baik Penolong."), 1, "", ""),
    ("hawqalah", "Lā ḥaula wa lā quwwata illā billāh", "z", ("وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ",
     "Wa la haula wa la quwwata illa billahil-'aliyyil-'azim", "Tiada daya dan tiada kekuatan melainkan dengan Allah Yang Maha Tinggi lagi Maha Agung."), 1,
     "HR Al-Bukhari, no. 6384; Muslim, no. 2704: salah satu perbendaharaan syurga", ""),
    ("istighfar", "Istighfar", "z", ("أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ", "Astaghfirullahal-'azim", "Aku memohon ampun kepada Allah Yang Maha Agung."), 3,
     "HR Muslim, no. 591 (istighfar 3 kali)", ""),
    ("afdhal", "Afḍaluz-zikr", "z", ("أَفْضَلُ الذِّكْرِ فَاعْلَمْ أَنَّهُ لَا إِلٰهَ إِلَّا اللهُ، حَيٌّ مَوْجُودٌ", "Afdhaluz-zikri fa'lam annahu la ilaha illallah, hayyun maujud",
     "Sebaik-baik zikir, ketahuilah, ialah “Lā ilāha illallāh”; Allah Maha Hidup lagi Maha Wujud."), 1,
     "“Sebaik-baik zikir ialah Lā ilāha illallāh”: HR At-Tirmizi, no. 3383 (hasan)", "Dibaca oleh imam sebagai pembuka tahlil."),
    ("tahlil", "Lā ilāha illallāh", "z", ("لَا إِلٰهَ إِلَّا اللهُ", "La ilaha illallah", "Tiada tuhan melainkan Allah."), 33,
     "HR At-Tirmizi, no. 3383", "Diulang bersama-sama; sebahagian majlis membacanya 100 kali."),
    ("syahadah", "Lā ilāha illallāh Muḥammadur-rasūlullāh", "z", ("لَا إِلٰهَ إِلَّا اللهُ مُحَمَّدٌ رَسُولُ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ",
     "La ilaha illallah, Muhammadur-rasulullah sallallahu 'alaihi wa sallam", "Tiada tuhan melainkan Allah, Muhammad pesuruh Allah, selawat dan salam Allah ke atas baginda."), 1, "", ""),
    ("selawat2", "Selawat", "z", ("اللَّهُمَّ صَلِّ عَلَى سَيِّدِنَا مُحَمَّدٍ، اللَّهُمَّ صَلِّ عَلَيْهِ وَسَلِّمْ",
     "Allahumma solli 'ala saiyidina Muhammad, Allahumma solli 'alaihi wa sallim", "Ya Allah, limpahkanlah selawat ke atas penghulu kami Nabi Muhammad; ya Allah, limpahkanlah selawat dan salam ke atas baginda."), 2,
     "Al-Ahzab 33:56; HR Muslim, no. 408", ""),
    ("tasbih", "Subḥānallāhi wa biḥamdih", "z", ("سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ", "Subhanallahi wa bihamdihi, subhanallahil-'azim",
     "Maha Suci Allah dan segala puji bagi-Nya, Maha Suci Allah Yang Maha Agung."), 3,
     "HR Al-Bukhari, no. 6406; Muslim, no. 2694: ringan di lidah, berat di timbangan", ""),
    ("fatihah3", "Hadiah Al-Fatihah (penutup)", "q", [(1, 1, 7)], 1, "", "Dihadiahkan sekali lagi kepada arwah sebelum doa."),
    ("doa", "Doa untuk arwah", "doa", None, 1, "HR Muslim, no. 963 (doa Rasulullah SAW untuk jenazah)", ""),
    ("doa-ikhwan", "Doa untuk saudara seiman yang telah pergi", "q", [(59, 10, 10)], 1, "", ""),
    ("doa-ibubapa", "Doa untuk ibu bapa", "q", [(71, 28, 28)], 1, "", ""),
    ("doa-akhir", "Doa sapu jagat & penutup", "q", [(2, 201, 201), (37, 180, 182)], 1, "", ""),
]

# doa for the deceased: one man (l), one woman (p), men or mixed (ll), women (pp)
DOA = {
    "l": ("اللَّهُمَّ اغْفِرْ لَهُ وَارْحَمْهُ وَعَافِهِ وَاعْفُ عَنْهُ، وَأَكْرِمْ نُزُلَهُ، وَوَسِّعْ مُدْخَلَهُ",
          "Allahummaghfir lahu warhamhu wa 'afihi wa'fu 'anhu, wa akrim nuzulahu, wa wassi' mudkhalahu",
          "Ya Allah, ampunilah dia (lelaki), rahmatilah dia, sejahterakanlah dia dan maafkanlah dia; muliakanlah tempat persinggahannya dan luaskanlah tempat masuknya."),
    "p": ("اللَّهُمَّ اغْفِرْ لَهَا وَارْحَمْهَا وَعَافِهَا وَاعْفُ عَنْهَا، وَأَكْرِمْ نُزُلَهَا، وَوَسِّعْ مُدْخَلَهَا",
          "Allahummaghfir laha warhamha wa 'afiha wa'fu 'anha, wa akrim nuzulaha, wa wassi' mudkhalaha",
          "Ya Allah, ampunilah dia (perempuan), rahmatilah dia, sejahterakanlah dia dan maafkanlah dia; muliakanlah tempat persinggahannya dan luaskanlah tempat masuknya."),
    "ll": ("اللَّهُمَّ اغْفِرْ لَهُمْ وَارْحَمْهُمْ وَعَافِهِمْ وَاعْفُ عَنْهُمْ، وَأَكْرِمْ نُزُلَهُمْ، وَوَسِّعْ مُدْخَلَهُمْ",
           "Allahummaghfir lahum warhamhum wa 'afihim wa'fu 'anhum, wa akrim nuzulahum, wa wassi' mudkhalahum",
           "Ya Allah, ampunilah mereka, rahmatilah mereka, sejahterakanlah mereka dan maafkanlah mereka; muliakanlah tempat persinggahan mereka dan luaskanlah tempat masuk mereka."),
    "pp": ("اللَّهُمَّ اغْفِرْ لَهُنَّ وَارْحَمْهُنَّ وَعَافِهِنَّ وَاعْفُ عَنْهُنَّ، وَأَكْرِمْ نُزُلَهُنَّ، وَوَسِّعْ مُدْخَلَهُنَّ",
           "Allahummaghfir lahunna warhamhunna wa 'afihinna wa'fu 'anhunna, wa akrim nuzulahunna, wa wassi' mudkhalahunna",
           "Ya Allah, ampunilah mereka (perempuan), rahmatilah mereka, sejahterakanlah mereka dan maafkanlah mereka; muliakanlah tempat persinggahan mereka dan luaskanlah tempat masuk mereka."),
}
JANTINA = [("l", "Seorang lelaki"), ("p", "Seorang perempuan"), ("ll", "Ramai (lelaki / bercampur)"), ("pp", "Ramai perempuan")]
# how the dedication names the deceased: (title prefix, bin/binti)
GELARAN = {"l": ("Allahyarham", "bin"), "p": ("Allahyarhamah", "binti"), "ll": ("", ""), "pp": ("", "")}

_MARKS = re.compile("[ً-ٰٟۖ-ۭ]")


def bare(w):
    return _MARKS.sub("", w).replace("ٱ", "ا").replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")


def slice_from(arabic, first):
    """Words of an ayah from the first word whose bare form is `first` (bare too)."""
    words = arabic.split()
    for i, w in enumerate(words):
        if bare(w) == bare(first):
            return " ".join(words[i:])
    raise ValueError(f"{first!r} not in ayah")


def hadiah(code, nama="", bapa=""):
    """Dedication text in Malay; the page redraws it as the name is typed (alat.js hadiah() is the same)."""
    t, b = GELARAN[code]
    if code in ("ll", "pp"):
        who = "roh-roh " + (nama.strip() or "ahli keluarga kami") + " yang telah kembali ke rahmatullah"
    else:
        who = "roh " + " ".join(x for x in [t, nama.strip() or "[nama arwah]", (b + " " + bapa.strip()) if bapa.strip() else ""] if x)
    return ("Ke hadrat Nabi Muhammad SAW, keluarga dan sahabat baginda, para nabi dan rasul, para wali dan ulama, kedua ibu bapa kami, "
            f"seluruh muslimin dan muslimat, dan khususnya kepada {who}: Al-Fatihah.")
