"""The 99 names (Asmaul Husna) in the order commonly taught in Malaysia, which follows the list appended to the hadith in
At-Tirmizi (no. 3507). The hadith that Allah has 99 names is sahih (Al-Bukhari, no. 2736; Muslim, no. 2677); the
enumeration itself is a compilation by the narrators, which the page says. Quranic examples are found automatically in
data-surah/ (the first ayah containing the name in its definite form), never typed here."""
import json, os, re
from tahlil import bare

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (arabic, rumi, maksud)
NAMES = [
    ("الرَّحْمَنُ", "Ar-Rahman", "Yang Maha Pemurah"), ("الرَّحِيمُ", "Ar-Rahim", "Yang Maha Mengasihani"), ("الْمَلِكُ", "Al-Malik", "Yang Maha Merajai"),
    ("الْقُدُّوسُ", "Al-Quddus", "Yang Maha Suci"), ("السَّلَامُ", "As-Salam", "Yang Maha Sejahtera"), ("الْمُؤْمِنُ", "Al-Mu'min", "Yang Maha Memberi Keamanan"),
    ("الْمُهَيْمِنُ", "Al-Muhaimin", "Yang Maha Memelihara"), ("الْعَزِيزُ", "Al-'Aziz", "Yang Maha Perkasa"), ("الْجَبَّارُ", "Al-Jabbar", "Yang Maha Gagah"),
    ("الْمُتَكَبِّرُ", "Al-Mutakabbir", "Yang Maha Memiliki Kebesaran"), ("الْخَالِقُ", "Al-Khaliq", "Yang Maha Pencipta"), ("الْبَارِئُ", "Al-Bari'", "Yang Maha Mengadakan"),
    ("الْمُصَوِّرُ", "Al-Musawwir", "Yang Maha Membentuk Rupa"), ("الْغَفَّارُ", "Al-Ghaffar", "Yang Maha Pengampun"), ("الْقَهَّارُ", "Al-Qahhar", "Yang Maha Menundukkan"),
    ("الْوَهَّابُ", "Al-Wahhab", "Yang Maha Pemberi Kurnia"), ("الرَّزَّاقُ", "Ar-Razzaq", "Yang Maha Pemberi Rezeki"), ("الْفَتَّاحُ", "Al-Fattah", "Yang Maha Pembuka Rahmat"),
    ("الْعَلِيمُ", "Al-'Alim", "Yang Maha Mengetahui"), ("الْقَابِضُ", "Al-Qabidh", "Yang Maha Menyempitkan"), ("الْبَاسِطُ", "Al-Basit", "Yang Maha Melapangkan"),
    ("الْخَافِضُ", "Al-Khafidh", "Yang Maha Merendahkan"), ("الرَّافِعُ", "Ar-Rafi'", "Yang Maha Meninggikan"), ("الْمُعِزُّ", "Al-Mu'izz", "Yang Maha Memuliakan"),
    ("الْمُذِلُّ", "Al-Muzill", "Yang Maha Menghinakan"), ("السَّمِيعُ", "As-Sami'", "Yang Maha Mendengar"), ("الْبَصِيرُ", "Al-Basir", "Yang Maha Melihat"),
    ("الْحَكَمُ", "Al-Hakam", "Yang Maha Menetapkan Hukum"), ("الْعَدْلُ", "Al-'Adl", "Yang Maha Adil"), ("اللَّطِيفُ", "Al-Latif", "Yang Maha Lembut"),
    ("الْخَبِيرُ", "Al-Khabir", "Yang Maha Mengetahui Segala Rahsia"), ("الْحَلِيمُ", "Al-Halim", "Yang Maha Penyantun"), ("الْعَظِيمُ", "Al-'Azim", "Yang Maha Agung"),
    ("الْغَفُورُ", "Al-Ghafur", "Yang Maha Pengampun"), ("الشَّكُورُ", "Asy-Syakur", "Yang Maha Menerima Syukur"), ("الْعَلِيُّ", "Al-'Aliyy", "Yang Maha Tinggi"),
    ("الْكَبِيرُ", "Al-Kabir", "Yang Maha Besar"), ("الْحَفِيظُ", "Al-Hafiz", "Yang Maha Memelihara"), ("الْمُقِيتُ", "Al-Muqit", "Yang Maha Memberi Kecukupan"),
    ("الْحَسِيبُ", "Al-Hasib", "Yang Maha Membuat Perhitungan"), ("الْجَلِيلُ", "Al-Jalil", "Yang Maha Luhur"), ("الْكَرِيمُ", "Al-Karim", "Yang Maha Pemurah"),
    ("الرَّقِيبُ", "Ar-Raqib", "Yang Maha Mengawasi"), ("الْمُجِيبُ", "Al-Mujib", "Yang Maha Memperkenankan Doa"), ("الْوَاسِعُ", "Al-Wasi'", "Yang Maha Luas"),
    ("الْحَكِيمُ", "Al-Hakim", "Yang Maha Bijaksana"), ("الْوَدُودُ", "Al-Wadud", "Yang Maha Mengasihi"), ("الْمَجِيدُ", "Al-Majid", "Yang Maha Mulia"),
    ("الْبَاعِثُ", "Al-Ba'ith", "Yang Maha Membangkitkan"), ("الشَّهِيدُ", "Asy-Syahid", "Yang Maha Menyaksikan"), ("الْحَقُّ", "Al-Haqq", "Yang Maha Benar"),
    ("الْوَكِيلُ", "Al-Wakil", "Yang Maha Tempat Berserah"), ("الْقَوِيُّ", "Al-Qawiyy", "Yang Maha Kuat"), ("الْمَتِينُ", "Al-Matin", "Yang Maha Teguh"),
    ("الْوَلِيُّ", "Al-Waliyy", "Yang Maha Melindungi"), ("الْحَمِيدُ", "Al-Hamid", "Yang Maha Terpuji"), ("الْمُحْصِي", "Al-Muhsi", "Yang Maha Menghitung"),
    ("الْمُبْدِئُ", "Al-Mubdi'", "Yang Maha Memulakan"), ("الْمُعِيدُ", "Al-Mu'id", "Yang Maha Mengembalikan"), ("الْمُحْيِي", "Al-Muhyi", "Yang Maha Menghidupkan"),
    ("الْمُمِيتُ", "Al-Mumit", "Yang Maha Mematikan"), ("الْحَيُّ", "Al-Hayy", "Yang Maha Hidup"), ("الْقَيُّومُ", "Al-Qayyum", "Yang Maha Berdiri Sendiri"),
    ("الْوَاجِدُ", "Al-Wajid", "Yang Maha Kaya (Menemukan)"), ("الْمَاجِدُ", "Al-Majid", "Yang Maha Mulia"), ("الْوَاحِدُ", "Al-Wahid", "Yang Maha Esa"),
    ("الْأَحَدُ", "Al-Ahad", "Yang Maha Tunggal"), ("الصَّمَدُ", "As-Samad", "Yang Menjadi Tumpuan Segala Hajat"), ("الْقَادِرُ", "Al-Qadir", "Yang Maha Berkuasa"),
    ("الْمُقْتَدِرُ", "Al-Muqtadir", "Yang Maha Menentukan"), ("الْمُقَدِّمُ", "Al-Muqaddim", "Yang Maha Mendahulukan"), ("الْمُؤَخِّرُ", "Al-Mu'akhkhir", "Yang Maha Mengakhirkan"),
    ("الْأَوَّلُ", "Al-Awwal", "Yang Maha Awal"), ("الْآخِرُ", "Al-Akhir", "Yang Maha Akhir"), ("الظَّاهِرُ", "Az-Zahir", "Yang Maha Nyata"),
    ("الْبَاطِنُ", "Al-Batin", "Yang Maha Tersembunyi"), ("الْوَالِي", "Al-Wali", "Yang Maha Memerintah"), ("الْمُتَعَالِي", "Al-Muta'ali", "Yang Maha Tinggi Darjat-Nya"),
    ("الْبَرُّ", "Al-Barr", "Yang Maha Melimpahkan Kebaikan"), ("التَّوَّابُ", "At-Tawwab", "Yang Maha Penerima Taubat"), ("الْمُنْتَقِمُ", "Al-Muntaqim", "Yang Maha Membalas"),
    ("الْعَفُوُّ", "Al-'Afuww", "Yang Maha Pemaaf"), ("الرَّءُوفُ", "Ar-Ra'uf", "Yang Maha Belas Kasihan"), ("مَالِكُ الْمُلْكِ", "Malikul-Mulk", "Yang Memiliki Kerajaan"),
    ("ذُو الْجَلَالِ وَالْإِكْرَامِ", "Zul-Jalali wal-Ikram", "Yang Memiliki Keagungan dan Kemuliaan"), ("الْمُقْسِطُ", "Al-Muqsit", "Yang Maha Saksama"),
    ("الْجَامِعُ", "Al-Jami'", "Yang Maha Mengumpulkan"), ("الْغَنِيُّ", "Al-Ghaniyy", "Yang Maha Kaya"), ("الْمُغْنِي", "Al-Mughni", "Yang Maha Memberi Kekayaan"),
    ("الْمَانِعُ", "Al-Mani'", "Yang Maha Mencegah"), ("الضَّارُّ", "Adh-Dharr", "Yang Maha Mendatangkan Mudarat (dengan hikmah)"), ("النَّافِعُ", "An-Nafi'", "Yang Maha Memberi Manfaat"),
    ("النُّورُ", "An-Nur", "Yang Maha Bercahaya"), ("الْهَادِي", "Al-Hadi", "Yang Maha Pemberi Petunjuk"), ("الْبَدِيعُ", "Al-Badi'", "Yang Maha Pencipta Tanpa Contoh"),
    ("الْبَاقِي", "Al-Baqi", "Yang Maha Kekal"), ("الْوَارِثُ", "Al-Warith", "Yang Maha Mewarisi"), ("الرَّشِيدُ", "Ar-Rasyid", "Yang Maha Memberi Bimbingan"),
    ("الصَّبُورُ", "As-Sabur", "Yang Maha Sabar"),
]
assert len(NAMES) == 99


def _key(s):
    """Spelling-insensitive form: no harakat, one alif shape, no alif at all (Uthmani writes many long alifs as a dagger alif)."""
    return bare(s).replace("ى", "ي").replace("ة", "ه").replace("ا", "").replace("ء", "")


# name number -> (surah, ayah) where the name (or its indefinite form) describes Allah; checked against the text below
REF = {1: (1, 3), 2: (1, 3), 3: (59, 23), 4: (59, 23), 5: (59, 23), 6: (59, 23), 7: (59, 23), 8: (59, 23), 9: (59, 23), 10: (59, 23),
       11: (59, 24), 12: (59, 24), 13: (59, 24), 14: (38, 66), 15: (13, 16), 16: (38, 9), 17: (51, 58), 18: (34, 26), 19: (34, 26),
       26: (42, 11), 27: (42, 11), 28: (6, 114), 30: (67, 14), 31: (67, 14), 32: (2, 225), 33: (2, 255), 34: (10, 107), 35: (35, 30),
       36: (2, 255), 37: (22, 62), 38: (11, 57), 39: (4, 85), 40: (4, 6), 42: (82, 6), 43: (4, 1), 44: (11, 61), 45: (2, 115), 46: (59, 24),
       47: (85, 14), 48: (85, 15), 50: (4, 33), 51: (22, 6), 52: (3, 173), 53: (42, 19), 54: (51, 58), 55: (42, 28), 56: (42, 28), 60: (30, 50),
       62: (2, 255), 63: (2, 255), 66: (13, 16), 67: (112, 1), 68: (112, 2), 69: (6, 65), 70: (54, 55), 73: (57, 3), 74: (57, 3), 75: (57, 3),
       76: (57, 3), 77: (13, 11), 78: (13, 9), 79: (52, 28), 80: (2, 37), 81: (32, 22), 82: (4, 43), 83: (2, 143), 84: (3, 26), 85: (55, 27),
       87: (3, 9), 88: (35, 15), 93: (24, 35), 94: (22, 54), 95: (2, 117), 97: (15, 23)}


def quran_refs():
    """[(surah, ayah) or None] per name. Each REF entry must contain the name's letters (without "al-"), so a wrong
    number fails the build instead of linking an unrelated ayah."""
    out = []
    for i, (ar, ru, _) in enumerate(NAMES, 1):
        r = REF.get(i)
        if r:
            text = _key(json.load(open(f"{REPO}/data-surah/surah-{r[0]}.json", encoding="utf8"))[r[1] - 1]["arabic"])
            core = _key(ar.split()[0])
            core = core[1:] if core.startswith("ل") else core
            alts = [core] + ([core[:-1]] if core.endswith("ي") else [])
            assert any(c in text for c in alts), (ru, r, core)
        out.append(r)
    return out


if __name__ == "__main__":
    refs = quran_refs()
    print(sum(1 for r in refs if r), "of 99 found")
    for (ar, ru, _), r in zip(NAMES, refs):
        if not r:
            print("  none:", ru)
