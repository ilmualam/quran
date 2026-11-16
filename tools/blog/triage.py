"""Action for every pre-2025 www.ilmualam.com post that was not updated in 2025-26, plus overlap fixes for posts already
refreshed. Actions: DONE (refreshed), MERGED (already redirected), MERGE (redirect into a stronger post: the owner's
2025-26 post where one exists, else a refreshed one), REFRESH (rewrite: no existing post covers it), UNPUBLISH (revert to
draft: removed from the site and Google, reversible). Writes out/triage.json. Keys are URL fragments (unique)."""
import json, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(f"{HERE}/posts-audit.json"))


def url(frag):
    hits = [p["url"] for p in P if frag in p["url"]]
    assert len(hits) == 1, (frag, hits)
    return hits[0]


# fragment: (action, target fragment or batch label, reason)
T = {
    # --- already refreshed / merged (pilot, batch 1, batch 2)
    **{f: ("DONE", None, "Refreshed") for f in [
        "bagaimana-cara-membayar-hutang-puasa", "11-hikmah-dan-keutamaan-membaca-surah", "doa-al-afiyah-ringkas-tapi-power",
        "doa-dan-niat-mandi-besar-selesai-haid", "cara-mandi-wajib-yang-betul", "masa-nifas-menurut-agama", "perkara-yang-membatalkan-puasa",
        "bolehkah-membaca-doa-dzikir-ketika-junub", "cara-sujud-sahwi-bila-terlupa", "allahuakhbar-inilah-sebab-rasulullah",
        "makmum-batal-lewat-depan", "hukum-isteri-kejutkan-suami", "rahsia-mendapat-nikmat-khusyuk", "kelebihan-surah-yasin-dan-fadhilat",
        "subhanallah-inilah-8-kelebihan", "ini-lah-9-waktu-yang-dianjurkan", "bagaimana-surah-ad-dhuha-boleh", "amalan-wirid-membaca-surat-waqiah",
        "rasai-manfaat-asalkan-istiqomah", "kelebihan-ayat-seribu-dinar", "doa-nabi-yunus-amalkan", "tanda-tanda-gangguan-jin-sihir",
        "baca-dan-fahami-allah-tidak"]},
    **{f: ("MERGED", None, "Already redirected") for f in [
        "surah-yasin-ayat-58", "rawat-jiwa-kacau-dengan-11-ayat", "rawat-jiwa-yang-tidak-tenang", "doa-pembatal-sihir-ayat-pendinding",
        "ayat-ruqyah-untuk-menghancurkan"]},

    # --- merge into the owner's own 2025-26 posts (same search intent already covered)
    "5-amalan-megubati-hati-yang-dukacita": ("MERGE", "doa-hilangkan-stress", "Same topic as your 2026 post"),
    "amalkan-7-doa-pendek-yang-dapat": ("MERGE", "doa-hilangkan-stress", "Same topic as your 2026 post"),
    "bacalah-doa-ini-selepas-tahyat-akhir": ("MERGE", "doa-selepas-tahiyat-akhir", "Same topic as your 2025 post"),
    "etika-penting-dalam-berdoa": ("MERGE", "adab-adab-berdoa", "Same topic as your 2025 post"),
    "banyakkan-berdoa-kepada-allah-di-akhir": ("MERGE", "adab-adab-berdoa", "Waktu mustajab is part of adab berdoa"),
    "ingin-10-dosa-diampuni-dan-diangkat-10": ("MERGE", "10-selawat-paling-mustajab", "Same topic as your 2026 post"),
    "sebarkan-4-kelebihan-selawat-yang-patut": ("MERGE", "10-selawat-paling-mustajab", "133 words; covered by your 2026 post"),
    "kelebihan-dan-kebaikan-zikir": ("MERGE", "zikir-harian-sahih", "Same topic as your 2025 post"),
    "amalkan-tujuh-kalimat-yang-mulia-di": ("MERGE", "kalimah-zikir-harian", "Same topic as your 2026 post"),
    "doa-mustajab-ibu-hamil-agar-bayi-lahir": ("MERGE", "doa-ibu-mengandung", "Same topic as your 2026 post"),
    "doa-kebahagiaan-suami-isteri": ("MERGE", "doa-keluarga-bahagia", "Same topic as your updated post"),
    "nak-masuk-ke-rumah-baru-jangan-abaikan": ("MERGE", "doa-masuk-rumah", "Same topic as your 2026 post"),
    "amalan-dan-doa-sebelum-tidur": ("MERGE", "doa-tidur-rumi-bangun-tidur", "Same topic as your 2026 post"),
    "bersihkan-tempat-tidur-sebelum-tidur": ("MERGE", "doa-tidur-rumi-bangun-tidur", "Adab tidur, covered there"),
    "andai-ajal-dalam-tidur": ("MERGE", "doa-tidur-rumi-bangun-tidur", "Amalan sebelum tidur"),
    "saat-tidur-baiknya-lampu-menyala-atau": ("MERGE", "doa-tidur-rumi-bangun-tidur", "Adab tidur"),
    "hukum-memelihara-kucing-salah-satu-hal": ("MERGE", "hukum-menjaga-kucing-dalam-islam", "Same topic as your 2026 post"),
    "rasulullah-saw-berkata-jangan-usir_25": ("MERGE", "hukum-menjaga-kucing-dalam-islam", "Kucing"),
    "bagaimanakah-hukum-bleaching-rambut": ("MERGE", "hukum-warna-rambut", "Same topic as your 2026 post"),
    "4-kelebihan-utama-solat-tahajjud-di": ("MERGE", "cara-solat-tahajjud", "Covered by your 2026 post"),
    "dengan-aurat-terbuka-tanpa-memakai": ("MERGE", "hukum-berhijab-dalam-islam", "Same topic as your 2026 post"),
    "himpunan-doa-doa-harian-yang-mustajab": ("MERGE", "zikir-harian-sahih", "Thin collection; your 2025 post is stronger"),
    "kempulan-doa-doa-pilihan": ("MERGE", "zikir-harian-sahih", "Thin collection"),
    "doa-pembuka-12-pintu-rezeki-paling": ("MERGE", "20-amalan-murah-rezeki-dan-cara-cepat", "Rezeki topic covered by your post"),
    "baca-dua-ayat-ini-tiap-malam-insya": ("MERGE", "20-amalan-murah-rezeki-dan-cara-cepat", "Clickbait rezeki; covered there"),
    "amalan-menjemput-rezeki-tengah-malam": ("MERGE", "20-amalan-murah-rezeki-dan-cara-cepat", "Clickbait rezeki; covered there"),
    "inilah-2-penghalang-utama-rezeki-yang": ("MERGE", "20-amalan-murah-rezeki-dan-cara-cepat", "Rezeki"),
    "cara-uji-diri-sendiri-adakah-terdapat": ("MERGE", "doa-elak-gangguan-jin-syaitan", "Jin topic covered by your 2026 post"),
    "info-bermanfaat-teknik-atau-cara": ("MERGE", "hukum-azimat-tangkal-islam", "Sihir objects; your azimat post covers it"),
    "bacalah-dan-fahamibaca-3-surah": ("MERGE", "ruqyah-ikhlas-falaq-nas", "3 surah perlindungan = your 2025 post"),
    "keajaiban-al-quran-hingga-meremang": ("MERGE", "kebaikan-membaca-al-quran-dan-kelebihan", "Kelebihan Al-Quran"),
    "beginilah-cara-al-quran-membimbing": ("MERGE", "kebaikan-membaca-al-quran-dan-kelebihan", "Thin"),

    # --- merge into a refreshed post
    "inilah-yang-dilakukan-nabi-ketika": ("MERGE", "cara-solat-qada", "Terlewat Subuh = qada"),
    "jika-anda-seorang-yang-banyak": ("MERGE", "cara-solat-qada", "Tertinggal solat = qada"),
    "rugi-jika-diabaikancara-cara-membaca": ("MERGE", "11-hikmah-dan-keutamaan-membaca-surah", "Fatihah 41x; status explained in the refreshed post"),
    "bacalah-ayat-daripada-surah-yassin-ini": ("MERGE", "kelebihan-surah-yasin-dan-fadhilat", "Yasin"),
    "2017/12/bila-ayam-berkokok-di-tengah-malam-maka": ("REFRESH", "Batch 3", "Ayam berkokok (sahih hadith); the 2018 duplicate redirects here"),
    "2018/02/bila-ayam-berkokok-di-tengah-malam-maka": ("MERGE", "2017/12/bila-ayam-berkokok-di-tengah-malam-maka", "Exact duplicate post"),
    "senafas-ke-barzakh-ustaz-ahmad-dusuki": ("MERGE", "mampukah-kita-jawab-5-soalan-di-dalam", "Alam barzakh"),
    "harus-baca-4-tips-menghadapi-dunia": ("MERGE", "tanda-tanda-kiamat-kecil-telah-lengkap", "Akhir zaman"),
    "penaklukan-baitulmaqdis-tanda-besar": ("MERGE", "tanda-tanda-kiamat-kecil-telah-lengkap", "Tanda kiamat; avoids a political post"),
    "dimulai-dengan-sholat-dan-diakhiri": ("MERGE", "9-kemuliaan-orang-menjaga-solat", "Thin"),
    "ancaman-bagi-yang-sengaja-menunda": ("MERGE", "azab-akibat-solat-di-hujung-waktu", "Same topic"),
    "10-jenis-solat-yang-tidak-diterima": ("MERGE", "azab-akibat-solat-di-hujung-waktu", "Solat warnings"),
    "kelebihan-bismillah-6-dan-khasiatnya": ("MERGE", "khasiat-bismillah-5-rumi-dan-terjemahan", "Two Bismillah posts"),

    # --- refresh: no existing post covers the search
    "azab-akibat-solat-di-hujung-waktu": ("REFRESH", "Batch 3", "Solat di hujung waktu (absorbs 2 posts)"),
    "9-kemuliaan-orang-menjaga-solat": ("REFRESH", "Batch 3", "Kelebihan menjaga solat"),
    "mampukah-kita-jawab-5-soalan-di-dalam": ("REFRESH", "Batch 3", "Soalan kubur"),
    "tanda-tanda-kiamat-kecil-telah-lengkap": ("REFRESH", "Batch 3", "Tanda kiamat kecil (absorbs 2 posts)"),
    "11-golongan-yang-masuk-syurga-tanpa": ("REFRESH", "Batch 3", "70,000 masuk syurga tanpa hisab"),
    "7-jenis-manusia-yang-didoakan-malaikat": ("REFRESH", "Batch 3", "Golongan didoakan malaikat"),
    "12-kaum-yang-dibinasakan-Allah": ("REFRESH", "Batch 3", "Kaum yang dibinasakan"),
    "pesanan-imam-syafie": ("REFRESH", "Batch 3", "Pesanan Imam Syafie"),
    "doa-mohon-allah-swt-tetapkan-hidayah": ("REFRESH", "Batch 3", "Doa hidayah / tetap hati"),
    "hati-hati-terhadap-doa-orang-yang": ("REFRESH", "Batch 3", "Doa orang teraniaya (mazlum)"),
    "doa-berlindung-dari-kesyirikan": ("REFRESH", "Batch 4", "Doa berlindung daripada syirik (160 words)"),
    "8-amalan-yang-amat-besar-ganjaran": ("REFRESH", "Batch 4", "Amalan pahala besar"),
    "7-amalan-yang-pahalanya-terus-mengalir": ("REFRESH", "Batch 4", "Pahala berterusan (jariah)"),
    "7-sunnah-nabi-yang-mudah-diamalkan": ("REFRESH", "Batch 4", "Sunnah Nabi"),
    "hukum-tiup-lilin-kek-hari-jadi-ulang": ("REFRESH", "Batch 4", "Hukum tiup lilin"),
    "hukum-bersedekah-tapi-mengungkit": ("REFRESH", "Batch 4", "Mengungkit sedekah"),
    "hukum-wanita-menyanyi-disisi-islam": ("REFRESH", "Batch 4", "Suara wanita"),
    "khasiat-bismillah-5-rumi-dan-terjemahan": ("REFRESH", "Batch 4", "Kelebihan Bismillah, with honest status (absorbs Bismillah 6)"),
    "tanda-tanda-penyakit-keras-hati-dan": ("REFRESH", "Batch 4", "Keras hati"),
    "3-cara-menanamkan-akidah-pada-anak-anak": ("REFRESH", "Batch 4", "Akidah anak"),
    "sering-diucapkan-padahal-kalimat-ini": ("REFRESH", "Batch 4", "Kalimah dibenci Allah"),
    "beza-air-mani-yang-keluar-dari-kemaluan": ("REFRESH", "Batch 4", "Beza mani, mazi, wadi: real fiqh search; neutral title"),
    "kenapa-kita-perlu-cukur-bulu-kemaluan": ("REFRESH", "Batch 4", "5 sunnah fitrah; neutral title"),
    "di-hari-kiamat-nanti-inilah-golongan": ("MERGE", "tanda-tanda-kiamat-kecil-telah-lengkap", "Akhir zaman"),
    "tahukah-kamu-ternyata-wanita-adalah": ("REFRESH", "Batch 4", "Sahih hadith but sensitive: rewrite with context or unpublish"),
    "inilah-dosa-suami-kesan-kepada-isteri": ("REFRESH", "Batch 4", "Tanggungjawab suami (absorbs 'suami dilaknat')"),
    "suami-akan-dilaknat-allah-apabila": ("MERGE", "inilah-dosa-suami-kesan-kepada-isteri", "Clickbait; merged into tanggungjawab suami"),
    "ini-bahayanya-apabila-suami-lebih": ("MERGE", "hukum-suami-lebihkan-ibu-dari-isteri", "Same topic as your updated post"),
    "rezeki-suami-tiba-tiba-mengalir-deras": ("MERGE", "doa-keluarga-bahagia", "Clickbait"),
    "perempuan-yang-bergelar-isteri-wajib": ("MERGE", "doa-keluarga-bahagia", "Thin"),

    # --- unpublish (revert to draft): sensitive, medical claims, clickbait or no value; reversible
    "mengapa-israel-takut-pada-briged-al": ("UNPUBLISH", None, "Political conflict: AdSense sensitive"),
    "hamas-umum-gerakan-intifada-akan": ("UNPUBLISH", None, "Political conflict: AdSense sensitive"),
    "hukum-mengeluarkan-mani-dengan-tangan": ("UNPUBLISH", None, "Adult wording in title"),
    "baca-dan-fahamihukum-onani-atau-melancap": ("UNPUBLISH", None, "Adult wording in title"),
    "jangan-abaikan-ini-cara-cuci-kemaluan": ("UNPUBLISH", None, "Adult wording + clickbait"),
    "dalam-kemaluanmu-itu-ada-sedekah": ("UNPUBLISH", None, "Adult wording in title; 193 words"),
    "lakukan-3-amalan-ini-agar-dosa-zina": ("UNPUBLISH", None, "Sensitive clickbait"),
    "petua-menjaga-kesihatan-supaya-sentiasa": ("UNPUBLISH", None, "Health claims, off-topic"),
    "kaum-wanita-patut-amalkan-10-jenis": ("UNPUBLISH", None, "Health claims, off-topic"),
    "rahsia-perubatan-islam-untuk-yang-kerap": ("UNPUBLISH", None, "Medical claims"),
    "adakah-soya-anda-selamat-atau": ("UNPUBLISH", None, "Health claims, off-topic"),
    "tolong-jangan-panik-jika-munculnya": ("UNPUBLISH", None, "Medical (lipoma), off-topic"),
    "10-khasiat-buah-naga-untuk-kesihatan": ("UNPUBLISH", None, "Health, off-topic"),
    "doktor-asal-mesir-ini-ungkap-rahsia": ("UNPUBLISH", None, "Unverified medical claim"),
    "macam-tak-percaya-misteri-asah-gigi": ("UNPUBLISH", None, "Clickbait, medical"),
    "petua-awet-muda-doa-kecantikan-wajah": ("UNPUBLISH", None, "Cosmetic claims"),
    "lihatlah-otak-manusia-seperti-orang": ("UNPUBLISH", None, "Pseudo-science"),
    "cara-membuat-setan-muntah": ("UNPUBLISH", None, "Clickbait"),
    "maklumat-menafaat-siapa-yang-selalu": ("UNPUBLISH", None, "Clickbait amalan, unsourced"),
    "hebatnya-amalan-ini-jika-diamalkan": ("UNPUBLISH", None, "Clickbait amalan, unsourced"),
    "30k-share-di-fb-lelaki-ini-kongsi-petua": ("UNPUBLISH", None, "Viral clickbait"),
    "sila-baca-meminta-melihat-jasad": ("UNPUBLISH", None, "Unsourced story"),
    "doa-seorang-anak-sebuah-kisah-yang": ("UNPUBLISH", None, "Viral story"),
    "3-hikmah-bagi-lelaki-yang-menikahi": ("UNPUBLISH", None, "Thin"),
    "wanita-lamar-lelaki-amalan-terpuji": ("UNPUBLISH", None, "Thin"),
    "orang-lain-tak-menjamin-dirimu-lebih": ("UNPUBLISH", None, "Thin motivational (check Search Console first)"),
    "apapun-yang-allah-atur-itulah-yang": ("UNPUBLISH", None, "Thin motivational (check Search Console first)"),
    "yakinlah-karana-setiap-ketidakmungkinan": ("UNPUBLISH", None, "Thin motivational (check Search Console first)"),
    "semakin-tinggi-ilmu-seorang-wanita-maka": ("UNPUBLISH", None, "Thin motivational (check Search Console first)"),
    "semua-doamu-akan-terkabul-pada-waktunya": ("MERGE", "sebab-doa-ditolak", "Doa makbul topic covered by your 2025 post"),
    "hikmah-dibalik-adanya-konflik": ("UNPUBLISH", None, "Thin"),
    "merenungkan-kembali-ayat-ucapkanlah": ("UNPUBLISH", None, "Thin (231 words)"),
    "inikah-tujuan-hidup-dan-mati": ("MERGE", "kenapa-allah-mencipta-manusia-alam", "Same topic as your 2026 post"),
    "jika-anda-pernah-alami-ini-anda-dijaga": ("UNPUBLISH", None, "Thin clickbait"),
    "amalkan-3-cara-untuk-menjadi-hamba": ("UNPUBLISH", None, "Thin"),
}

# overlap between refreshed posts and the owner's own 2025-26 posts: owner decides which URL survives
OVERLAP = [
    ("bagaimana-cara-membayar-hutang-puasa", "cara-ganti-puasa-qada", "KEEP BOTH", "Different intent: yours = how to ganti puasa; refreshed = hutang bertahun-tahun + fidyah berganda. Add a link each way."),
    ("rahsia-mendapat-nikmat-khusyuk", "cara-khusyuk-dalam-solat", "MERGE refreshed → yours", "Same search. Your 2026 post likely ranks; I move the best sections into it if you approve."),
    ("amalan-wirid-membaca-surat-waqiah", "kelebihan-surah-al-waqiah", "DECIDE", "Same search. Refreshed post grades the hadith dhaif; check your post's claims match before merging."),
    ("tanda-tanda-gangguan-jin-sihir", "4-ayat-al-quran-penangkal-sihir", "KEEP BOTH", "Different intent (ruqyah guide vs 4 ayat). Add links between them and to your ruqyah 3 surah post."),
]


if __name__ == "__main__":
    pool = {p["url"]: p for p in P}
    rows, seen = [], set()
    for frag, (act, tgt, why) in T.items():
        u = url(frag); seen.add(u)
        tu = url(tgt) if act == "MERGE" else None
        rows.append({"url": u, "title": html.unescape(pool[u]["title"]), "pub": pool[u]["pub"], "words": pool[u]["words"], "action": act,
                     "target": tu, "target_title": html.unescape(pool[tu]["title"]) if tu else (tgt or ""), "reason": why})
    cand = [p for p in P if p["pub"] < "2025-01-01" and p["upd"] < "2025-01-01" and "Waktu Imsak" not in p["labels"]]
    missing = [p["url"] for p in cand if p["url"] not in seen]
    ov = [{"refreshed": url(a), "yours": url(b), "yours_title": html.unescape(pool[url(b)]["title"]), "action": act, "why": why} for a, b, act, why in OVERLAP]
    json.dump({"rows": rows, "overlap": ov}, open(f"{HERE}/out/triage.json", "w"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(r["action"] for r in rows), "| unclassified:", len(missing)); [print("  missing", m) for m in missing]
