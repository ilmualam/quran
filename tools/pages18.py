"""Pages, batch 2 of single-doa pages (same template as tools/pages16.py, rendered by pages16.build_doa): one page per
high-volume "doa ..." search. No Arabic is typed here: Quranic doa come from data-surah/ by reference (q_item), hadith
doa from DOA_HARIAN in tools/ibadah.py (h_item), each with its book and hadith number."""
import ibadah as I
from pages import table
from pages16 import q_item, h_item, build_doa
from pages2 import card
from pages import e

PUB = "2026-11-11"
_Z = {z[0]: z for z in I.Z_PAGI_PETANG}


def z_card(key, title=None):
    i, t, ar, ru, mn, n, src, note = _Z[key]
    return card(i, title or t, e(ar), e(ru), e(mn), e(src), extra=note)


def ul(*items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def ref(t):
    return f' <span class="nref">({t})</span>'


PAGES = [
    ("doa-bangun-tidur/", dict(
        h1="Doa Bangun Tidur: Bacaan Rumi, Arab & Maksud",
        title="Doa Bangun Tidur: Bacaan Rumi, Arab & Maksud (Sahih Bukhari)",
        desc="Doa bangun tidur dalam tulisan Arab, Rumi dan maksud Bahasa Melayu daripada Sahih Al-Bukhari, serta amalan sunnah selepas bangun daripada tidur.",
        lead="Doa yang dibaca Rasulullah SAW sebaik sahaja bangun daripada tidur, dengan teks Arab, Rumi, maksud dan sumber hadis.",
        box="Doa bangun tidur ialah <strong>“Alhamdulillahil-lazi ahyana ba'da ma amatana wa ilaihin-nusyur”</strong>: segala puji bagi Allah yang menghidupkan kami "
            "setelah mematikan kami, dan kepada-Nya kami dibangkitkan (HR Al-Bukhari 6312). Tidur disebut “kematian kecil”, jadi bangun ialah nikmat hidup yang baharu.",
        sections=[("bacaan", "Bacaan Doa Bangun Tidur", h_item("bangun-tidur")),
                  ("amalan", "Amalan Sunnah Selepas Bangun Tidur", ul(
                      "Membaca doa bangun tidur di atas." + ref("HR Al-Bukhari 6312"),
                      "Menyapu kesan tidur dari muka dengan tangan." + ref("HR Al-Bukhari 183; Muslim 763"),
                      "Bersugi (menggosok gigi)." + ref("HR Al-Bukhari 245; Muslim 255"),
                      "Menghembus hidung tiga kali ketika berwuduk, kerana syaitan bermalam di hidung." + ref("HR Al-Bukhari 3295; Muslim 238"),
                      "Mencuci tangan tiga kali sebelum memasukkannya ke dalam bekas air." + ref("HR Muslim 278")))],
        faq=[("Apakah doa bangun tidur?", "Alhamdulillahil-lazi ahyana ba'da ma amatana wa ilaihin-nusyur. Maksudnya: Segala puji bagi Allah yang menghidupkan kami setelah mematikan kami, dan kepada-Nya kami dibangkitkan (HR Al-Bukhari 6312)."),
             ("Kenapa tidur disebut mati dalam doa ini?", "Al-Quran menyebut Allah mengambil jiwa manusia ketika tidur (Az-Zumar 39:42). Tidur ialah kematian kecil, maka bangun daripadanya disyukuri sebagai kehidupan semula."),
             ("Bolehkah doa ini dibaca selepas tidur siang?", "Boleh. Doa ini dibaca setiap kali bangun daripada tidur, sama ada malam atau siang.")],
        about=["Doa bangun tidur", "Doa harian"], llms="Doa bangun tidur: Alhamdulillahil-lazi ahyana ba'da ma amatana wa ilaihin-nusyur (HR Al-Bukhari 6312), teks Arab, Rumi, maksud dan amalan sunnah selepas bangun.")),
    ("doa-keluar-rumah/", dict(
        h1="Doa Keluar Rumah: Bacaan Rumi, Arab, Maksud & Kelebihan",
        title="Doa Keluar Rumah: Bacaan Rumi, Arab, Maksud & Kelebihan",
        desc="Doa keluar rumah Bismillahi tawakkaltu 'alallah dalam tulisan Arab, Rumi dan maksud, dengan kelebihannya: dipelihara dan dijauhkan daripada syaitan.",
        lead="Doa ketika melangkah keluar dari rumah, dengan teks Arab, Rumi, maksud dan janji perlindungan dalam hadis.",
        box="Doa keluar rumah ialah <strong>“Bismillahi tawakkaltu 'alallah, la haula wa la quwwata illa billah”</strong>. Sesiapa membacanya akan dikatakan kepadanya: "
            "“Engkau diberi petunjuk, dicukupkan dan dipelihara”, dan syaitan menjauhinya (HR Abu Daud 5095; At-Tirmizi 3426).",
        sections=[("bacaan", "Bacaan Doa Keluar Rumah", h_item("keluar-rumah")),
                  ("kelebihan", "Kelebihan Doa Keluar Rumah", ul(
                      "Diberi petunjuk, dicukupkan keperluan dan dipelihara daripada bahaya." + ref("HR Abu Daud 5095; At-Tirmizi 3426"),
                      "Syaitan berpaling daripadanya kerana dia telah berserah kepada Allah." + ref("HR Abu Daud 5095"),
                      "Melazimi tawakal: berusaha dan menyerahkan hasilnya kepada Allah.")),
                  ("lain", "Doa Berkaitan", ul('<a href="/doa-naik-kenderaan/">Doa naik kenderaan</a>', '<a href="/doa-masuk-masjid/">Doa masuk & keluar masjid</a>', '<a href="/doa-harian/">Semua doa harian</a>'))],
        faq=[("Apakah doa keluar rumah?", "Bismillahi tawakkaltu 'alallah, la haula wa la quwwata illa billah. Maksudnya: Dengan nama Allah, aku bertawakal kepada Allah; tiada daya dan kekuatan melainkan dengan Allah (HR Abu Daud 5095; At-Tirmizi 3426)."),
             ("Apakah kelebihan membaca doa keluar rumah?", "Orang yang membacanya diberi petunjuk, dicukupkan dan dipelihara, dan syaitan menjauhinya (HR Abu Daud 5095)."),
             ("Adakah doa ini dibaca setiap kali keluar?", "Ya, setiap kali keluar dari rumah, termasuk ke tempat kerja, sekolah atau masjid.")],
        about=["Doa keluar rumah", "Doa harian"], llms="Doa keluar rumah: Bismillahi tawakkaltu 'alallah, la haula wa la quwwata illa billah (HR Abu Daud 5095; At-Tirmizi 3426); diberi petunjuk, dicukupkan dan dipelihara.")),
    ("doa-masuk-masjid/", dict(
        h1="Doa Masuk Masjid & Keluar Masjid: Rumi, Arab & Maksud",
        title="Doa Masuk Masjid & Keluar Masjid: Bacaan Rumi, Arab & Maksud",
        desc="Doa masuk masjid dan doa keluar masjid dalam tulisan Arab, Rumi dan maksud daripada Sahih Muslim, serta adab dan solat tahiyatul masjid.",
        lead="Doa ketika masuk dan keluar masjid daripada Sahih Muslim, dengan teks Arab, Rumi, maksud dan adab di masjid.",
        box="Ketika <strong>masuk masjid</strong> baca <strong>“Allahummaftah li abwaba rahmatik”</strong> (Ya Allah, bukakanlah untukku pintu-pintu rahmat-Mu), dan ketika "
            "<strong>keluar</strong> baca <strong>“Allahumma inni as'aluka min fadlik”</strong> (Ya Allah, aku memohon kurnia-Mu) (HR Muslim 713). Sebelum duduk, solat dua rakaat tahiyatul masjid (HR Al-Bukhari 444).",
        sections=[("bacaan", "Bacaan Doa Masuk & Keluar Masjid", h_item("masuk-masjid") + h_item("keluar-masjid")),
                  ("adab", "Adab di Masjid", ul(
                      "Solat dua rakaat tahiyatul masjid sebelum duduk." + ref("HR Al-Bukhari 444; Muslim 714"),
                      "Doa masuk memohon rahmat, doa keluar memohon kurnia (rezeki dan kelebihan dunia)." + ref("HR Muslim 713"),
                      "Tidak melintas di hadapan orang yang sedang solat." + ref("HR Al-Bukhari 510; Muslim 507"),
                      'Cari masjid terdekat dengan <a href="/cari-masjid/">Cari Masjid & Surau</a>.'))],
        faq=[("Apakah doa masuk masjid?", "Allahummaftah li abwaba rahmatik: Ya Allah, bukakanlah untukku pintu-pintu rahmat-Mu (HR Muslim 713)."),
             ("Apakah doa keluar masjid?", "Allahumma inni as'aluka min fadlik: Ya Allah, sesungguhnya aku memohon kurnia-Mu (HR Muslim 713)."),
             ("Bilakah solat tahiyatul masjid dilakukan?", "Sebaik sahaja masuk masjid dan sebelum duduk, dua rakaat (HR Al-Bukhari 444). Jika terus menunaikan solat fardu atau sunat lain, ia sudah mencukupi.")],
        about=["Doa masuk masjid", "Doa keluar masjid", "Adab masjid"], llms="Doa masuk masjid: Allahummaftah li abwaba rahmatik; keluar: Allahumma inni as'aluka min fadlik (HR Muslim 713); tahiyatul masjid (HR Al-Bukhari 444).")),
    ("doa-ketika-hujan/", dict(
        h1="Doa Ketika Hujan & Selepas Hujan: Rumi, Arab & Maksud",
        title="Doa Ketika Hujan & Selepas Hujan: Bacaan Rumi, Arab & Maksud",
        desc="Doa ketika hujan turun Allahumma sayyiban nafi'a dalam tulisan Arab, Rumi dan maksud, doa selepas hujan dan doa ketika hujan lebat, dengan rujukan hadis.",
        lead="Doa yang dibaca Rasulullah SAW apabila hujan turun dan selepas hujan, dengan sumber hadis.",
        box="Apabila hujan turun, baca <strong>“Allahumma sayyiban nafi'a”</strong>: Ya Allah, jadikanlah hujan ini hujan yang bermanfaat (HR Al-Bukhari 1032). "
            "Selepas hujan, ucapkan <strong>“Mutirna bifadlillahi wa rahmatih”</strong>: kami diberi hujan dengan kurnia dan rahmat Allah (HR Al-Bukhari 846; Muslim 71).",
        sections=[("bacaan", "Bacaan Doa Ketika Hujan", h_item("hujan")),
                  ("lain", "Doa Selepas Hujan & Ketika Hujan Lebat", table(["Keadaan", "Bacaan (Rumi)", "Maksud", "Sumber"], [
                      ["Ketika hujan turun", "Allahumma sayyiban nafi'a", "Ya Allah, jadikanlah ia hujan yang bermanfaat", "HR Al-Bukhari 1032"],
                      ["Selepas hujan", "Mutirna bifadlillahi wa rahmatih", "Kami diberi hujan dengan kurnia dan rahmat Allah", "HR Al-Bukhari 846; Muslim 71"],
                      ["Hujan terlalu lebat", "Allahumma hawalaina wa la 'alaina", "Ya Allah, (turunkanlah) di sekeliling kami, bukan ke atas kami", "HR Al-Bukhari 1014; Muslim 897"]], "Doa berkaitan hujan"))],
        faq=[("Apakah doa ketika hujan turun?", "Allahumma sayyiban nafi'a: Ya Allah, jadikanlah hujan ini hujan yang bermanfaat (HR Al-Bukhari 1032)."),
             ("Apakah doa ketika hujan lebat atau banjir?", "Allahumma hawalaina wa la 'alaina: Ya Allah, turunkanlah di sekeliling kami dan bukan ke atas kami (HR Al-Bukhari 1014; Muslim 897). Rasulullah SAW membacanya ketika hujan berterusan."),
             ("Apakah yang diucapkan selepas hujan?", "Mutirna bifadlillahi wa rahmatih: kami diberi hujan dengan kurnia dan rahmat Allah (HR Al-Bukhari 846). Hadis ini juga melarang menisbahkan hujan kepada bintang.")],
        about=["Doa ketika hujan", "Doa harian"], llms="Doa ketika hujan: Allahumma sayyiban nafi'a (HR Al-Bukhari 1032); selepas hujan: Mutirna bifadlillahi wa rahmatih (HR Al-Bukhari 846); hujan lebat: Allahumma hawalaina wa la 'alaina (HR Al-Bukhari 1014).")),
    ("doa-ditimpa-musibah/", dict(
        h1="Doa Ditimpa Musibah & Kematian: Rumi, Arab & Maksud",
        title="Doa Ditimpa Musibah: Bacaan Inna Lillahi, Rumi, Arab & Maksud",
        desc="Doa ditimpa musibah dan kematian: Inna lillahi wa inna ilaihi raji'un dan doa Ummu Salamah, dengan tulisan Arab, Rumi, maksud dan Al-Baqarah 155–157.",
        lead="Ucapan istirja' dan doa yang diajar Rasulullah SAW ketika ditimpa musibah, dengan ayat Al-Quran tentang orang yang sabar.",
        box="Ketika ditimpa musibah atau mendengar berita kematian, ucapkan <strong>“Inna lillahi wa inna ilaihi raji'un, Allahumma'jurni fi musibati wa akhlif li khairan minha”</strong>. "
            "Allah menggantikan dengan yang lebih baik bagi sesiapa yang membacanya (HR Muslim 918), dan orang yang sabar dijanjikan selawat dan rahmat Allah (Al-Baqarah 2:155–157).",
        sections=[("bacaan", "Bacaan Doa Ditimpa Musibah", h_item("musibah")),
                  ("ayat", "Ayat Al-Quran tentang Musibah", q_item("ayat-2-155", "Al-Baqarah 155–157: berita gembira bagi orang yang sabar", [(2, 155), (2, 156), (2, 157)], "")),
                  ("kisah", "Kisah Doa Ini", "<p>Ummu Salamah membaca doa ini ketika suaminya Abu Salamah meninggal dunia. Dia berkata: “Siapakah yang lebih baik daripada Abu Salamah?” "
                   "Lalu Allah menggantikannya dengan Rasulullah SAW sebagai suaminya." + ref("HR Muslim 918") + "</p>")],
        faq=[("Apakah doa ketika ditimpa musibah?", "Inna lillahi wa inna ilaihi raji'un, Allahumma'jurni fi musibati wa akhlif li khairan minha: Sesungguhnya kami milik Allah dan kepada-Nya kami kembali; ya Allah, berilah pahala dalam musibahku dan gantikanlah yang lebih baik (HR Muslim 918)."),
             ("Bilakah Inna lillahi diucapkan?", "Ketika ditimpa apa jua musibah, besar atau kecil: kematian, kehilangan, sakit atau kerugian. Ia disebut dalam Al-Baqarah 2:156."),
             ("Apakah ganjaran orang yang sabar ketika musibah?", "Allah menjanjikan selawat (keampunan dan pujian), rahmat dan petunjuk kepada mereka (Al-Baqarah 2:157).")],
        about=["Doa musibah", "Inna lillahi wa inna ilaihi raji'un", "Sabar"], llms="Doa ditimpa musibah: Inna lillahi wa inna ilaihi raji'un, Allahumma'jurni fi musibati wa akhlif li khairan minha (HR Muslim 918); Al-Baqarah 2:155–157.")),
    ("doa-hilangkan-resah/", dict(
        h1="Doa Hilangkan Resah, Sedih & Gelisah: Rumi, Arab & Maksud",
        title="Doa Hilangkan Resah, Sedih & Gelisah: Bacaan Rumi & Maksud",
        desc="Doa ketika resah, sedih, gelisah dan dihimpit hutang daripada Sahih Bukhari, serta doa Nabi Yunus, dengan tulisan Arab, Rumi dan maksud.",
        lead="Doa Rasulullah SAW untuk berlindung daripada kerisauan, kesedihan, kemalasan dan beban hutang, serta doa Nabi Yunus ketika dalam kegelapan.",
        box="Doa yang sering dibaca Rasulullah SAW ketika resah ialah <strong>“Allahumma inni a'uzu bika minal-hammi wal-hazan…”</strong>: memohon perlindungan daripada kerisauan, "
            "kesedihan, kelemahan, kemalasan, sifat bakhil, pengecut, beban hutang dan penindasan manusia (HR Al-Bukhari 6369). Doa Nabi Yunus (Al-Anbiya' 21:87) juga dimakbulkan bagi sesiapa yang membacanya (HR At-Tirmizi 3505).",
        sections=[("bacaan", "Bacaan Doa Hilangkan Resah", h_item("dukacita")),
                  ("yunus", "Doa Nabi Yunus", q_item("ayat-21-87", "Al-Anbiya' 87: doa Nabi Yunus dalam perut ikan", [(21, 87)], "HR At-Tirmizi 3505")),
                  ("lain", "Amalan Ketika Hati Gelisah", ul("Mengingati Allah: “Ketahuilah, dengan mengingati Allah hati menjadi tenang” (Ar-Ra'd 13:28).",
                                                           'Membaca <a href="/zikir-pagi-petang/">zikir pagi dan petang</a>.', 'Bertasbih dengan <a href="/tasbih-digital/">tasbih digital</a> selepas solat.'))],
        faq=[("Apakah doa ketika resah dan sedih?", "Allahumma inni a'uzu bika minal-hammi wal-hazan, wal-'ajzi wal-kasal, wal-bukhli wal-jubn, wa dala'id-daini wa ghalabatir-rijal (HR Al-Bukhari 6369)."),
             ("Adakah doa ini juga untuk orang yang berhutang?", "Ya. Doa ini memohon perlindungan daripada beban hutang (dala'id-dain) dan penindasan manusia."),
             ("Apakah kelebihan doa Nabi Yunus?", "La ilaha illa anta subhanaka inni kuntu minaz-zalimin. Tidak seorang Muslim berdoa dengannya dalam sesuatu urusan melainkan Allah memperkenankannya (HR At-Tirmizi 3505).")],
        about=["Doa resah", "Doa sedih", "Doa hutang"], llms="Doa hilangkan resah dan sedih: Allahumma inni a'uzu bika minal-hammi wal-hazan... (HR Al-Bukhari 6369); doa Nabi Yunus Al-Anbiya' 21:87 (HR At-Tirmizi 3505).")),
    ("doa-untuk-ibu-bapa/", dict(
        h1="Doa untuk Ibu Bapa: Rumi, Arab & Maksud daripada Al-Quran",
        title="Doa untuk Ibu Bapa: Bacaan Rumi, Arab & Maksud (Al-Quran)",
        desc="Doa untuk ibu bapa yang masih hidup dan yang telah meninggal dunia daripada Al-Quran: Rabbirhamhuma, doa Nabi Ibrahim dan doa Nabi Nuh, dengan Rumi dan maksud.",
        lead="Tiga doa untuk ibu bapa daripada Al-Quran, dibaca untuk ibu bapa yang masih hidup atau telah meninggal dunia.",
        box="Doa untuk ibu bapa yang paling masyhur ialah <strong>“Rabbirhamhuma kama rabbayani saghira”</strong>: Wahai Tuhanku, kasihanilah mereka berdua sebagaimana mereka mendidikku "
            "semasa kecil (Al-Isra' 17:24). Doa anak yang soleh ialah antara tiga amalan yang terus memberi pahala kepada ibu bapa selepas mereka meninggal dunia (HR Muslim 1631).",
        sections=[("bacaan", "Doa untuk Ibu Bapa daripada Al-Quran",
                   q_item("ayat-17-24", "Al-Isra' 24: Rabbirhamhuma", [(17, 24)], "") + q_item("ayat-14-41", "Ibrahim 41: doa Nabi Ibrahim untuk ibu bapa", [(14, 41)], "")
                   + q_item("ayat-71-28", "Nuh 28: doa Nabi Nuh untuk ibu bapa dan orang beriman", [(71, 28)], "")),
                  ("kelebihan", "Kelebihan Mendoakan Ibu Bapa", ul(
                      "Doa anak yang soleh tetap sampai kepada ibu bapa selepas mereka meninggal dunia." + ref("HR Muslim 1631"),
                      "Allah memerintahkan berbuat baik kepada ibu bapa dan mendoakan mereka." + ref("Al-Isra' 17:23–24"),
                      'Untuk arwah ibu bapa, baca juga <a href="/tahlil-ringkas/">tahlil ringkas</a> dan <a href="/surah-yasin/">Surah Yasin</a>.'))],
        faq=[("Apakah doa untuk ibu bapa?", "Rabbirhamhuma kama rabbayani saghira: Wahai Tuhanku, kasihanilah mereka berdua sebagaimana mereka mendidikku semasa kecil (Al-Isra' 17:24)."),
             ("Adakah doa anak sampai kepada ibu bapa yang telah meninggal?", "Ya. Apabila seseorang meninggal dunia, amalannya terputus kecuali tiga: sedekah jariah, ilmu yang bermanfaat dan anak soleh yang mendoakannya (HR Muslim 1631)."),
             ("Bilakah waktu terbaik mendoakan ibu bapa?", "Selepas solat fardu, ketika sujud, pada sepertiga malam terakhir dan pada hari Jumaat, iaitu waktu-waktu doa dimakbulkan.")],
        about=["Doa untuk ibu bapa", "Birrul walidain"], llms="Doa untuk ibu bapa: Rabbirhamhuma kama rabbayani saghira (Al-Isra' 17:24), Ibrahim 14:41, Nuh 71:28; doa anak soleh sampai kepada ibu bapa (HR Muslim 1631).")),
    ("doa-murah-rezeki/", dict(
        h1="Doa Murah Rezeki: Doa daripada Al-Quran & Hadis Sahih",
        title="Doa Murah Rezeki: Bacaan Rumi, Arab & Maksud (Quran & Hadis)",
        desc="Doa murah rezeki daripada Al-Quran dan hadis sahih: doa Nabi Musa, doa selepas Subuh, ayat Seribu Dinar dan istighfar, dengan tulisan Arab, Rumi dan maksud.",
        lead="Doa memohon rezeki yang baik daripada Al-Quran dan hadis sahih, dengan sebab-sebab rezeki dimurahkan yang disebut dalam nas.",
        box="Doa rezeki daripada hadis ialah <strong>“Allahumma inni as'aluka 'ilman nafi'a, wa rizqan tayyiba, wa 'amalan mutaqabbala”</strong>, dibaca selepas salam solat Subuh (HR Ibnu Majah 925). "
            "Daripada Al-Quran, Nabi Musa berdoa <strong>“Rabbi inni lima anzalta ilayya min khairin faqir”</strong> (Al-Qasas 28:24). Takwa dan istighfar juga dijanjikan membuka pintu rezeki (At-Talaq 65:2–3; Nuh 71:10–12).",
        sections=[("bacaan", "Doa Murah Rezeki", h_item("ilmu-rezeki") + q_item("ayat-28-24", "Al-Qasas 24: doa Nabi Musa memohon rezeki", [(28, 24)], "")),
                  ("ayat", "Ayat Al-Quran tentang Pintu Rezeki",
                   q_item("ayat-65-2", "At-Talaq 2–3: rezeki dari arah yang tidak disangka", [(65, 2), (65, 3)], "") + q_item("ayat-71-10", "Nuh 10–12: istighfar mendatangkan hujan, harta dan anak", [(71, 10), (71, 11), (71, 12)], ""))],
        faq=[("Apakah doa murah rezeki daripada hadis sahih?", "Allahumma inni as'aluka 'ilman nafi'a, wa rizqan tayyiba, wa 'amalan mutaqabbala: Ya Allah, aku memohon ilmu yang bermanfaat, rezeki yang baik dan amalan yang diterima (HR Ibnu Majah 925, selepas solat Subuh)."),
             ("Apakah ayat Seribu Dinar?", "At-Talaq 65:2–3: sesiapa bertakwa, Allah memberinya jalan keluar dan rezeki dari arah yang tidak disangka. Nama “Seribu Dinar” ialah gelaran masyarakat, bukan daripada hadis."),
             ("Adakah istighfar memurahkan rezeki?", "Nabi Nuh menyeru kaumnya beristighfar, dan Allah menjanjikan hujan lebat, harta dan anak-anak (Nuh 71:10–12)."),
             ("Bilakah waktu terbaik berdoa untuk rezeki?", "Selepas solat Subuh (HR Ibnu Majah 925), ketika sujud dan pada sepertiga malam terakhir. Doa perlu disertai usaha yang halal.")],
        about=["Doa murah rezeki", "Rezeki", "Istighfar"], llms="Doa murah rezeki: Allahumma inni as'aluka 'ilman nafi'a wa rizqan tayyiba wa 'amalan mutaqabbala (HR Ibnu Majah 925); Al-Qasas 28:24; At-Talaq 65:2–3; Nuh 71:10–12.")),
    ("doa-belajar/", dict(
        h1="Doa Belajar & Doa Sebelum Peperiksaan: Rumi, Arab & Maksud",
        title="Doa Belajar & Sebelum Peperiksaan: Rumi, Arab & Maksud",
        desc="Doa sebelum belajar dan peperiksaan daripada Al-Quran: Rabbisyrahli sadri, Rabbi zidni 'ilma dan doa ilmu bermanfaat, dengan tulisan Arab, Rumi dan maksud.",
        lead="Doa memohon kelapangan dada, kefahaman dan tambahan ilmu daripada Al-Quran dan hadis, sesuai sebelum belajar dan peperiksaan.",
        box="Doa belajar yang paling masyhur ialah doa Nabi Musa <strong>“Rabbisyrahli sadri, wa yassirli amri, wahlul 'uqdatan min lisani, yafqahu qauli”</strong> (Taha 20:25–28) dan "
            "<strong>“Rabbi zidni 'ilma”</strong>: Wahai Tuhanku, tambahkanlah ilmuku (Taha 20:114). Daripada hadis, mohon “ilmu yang bermanfaat” (HR Ibnu Majah 925).",
        sections=[("bacaan", "Doa Belajar daripada Al-Quran",
                   q_item("ayat-20-25", "Taha 25–28: doa Nabi Musa (Rabbisyrahli sadri)", [(20, 25), (20, 26), (20, 27), (20, 28)], "")
                   + q_item("ayat-20-114", "Taha 114: Rabbi zidni 'ilma", [(20, 114)], "")),
                  ("hadis", "Doa Ilmu yang Bermanfaat", h_item("ilmu-rezeki")),
                  ("tip", "Sebelum Peperiksaan", ul("Baca doa di atas, kemudian mulakan dengan Bismillah.", "Solat hajat untuk memohon dipermudahkan: lihat <a href=\"/solat-sunat/solat-hajat/\">cara solat hajat</a>.",
                                                     "Tawakal selepas berusaha: kejayaan ialah kurnia Allah."))],
        faq=[("Apakah doa sebelum belajar?", "Rabbisyrahli sadri, wa yassirli amri, wahlul 'uqdatan min lisani, yafqahu qauli (Taha 20:25–28): Wahai Tuhanku, lapangkanlah dadaku, mudahkanlah urusanku, lepaskanlah kekelatan lidahku supaya mereka faham perkataanku."),
             ("Apakah maksud Rabbi zidni 'ilma?", "Wahai Tuhanku, tambahkanlah ilmuku (Taha 20:114). Ia satu-satunya perkara yang Allah perintahkan Nabi SAW memohon tambahan."),
             ("Adakah doa khusus sebelum peperiksaan?", "Tiada doa khusus peperiksaan dalam hadis sahih. Doa Nabi Musa, Rabbi zidni 'ilma dan doa ilmu yang bermanfaat (HR Ibnu Majah 925) sesuai dibaca.")],
        about=["Doa belajar", "Doa peperiksaan", "Ilmu"], llms="Doa belajar: Rabbisyrahli sadri... (Taha 20:25–28), Rabbi zidni 'ilma (Taha 20:114), doa ilmu bermanfaat (HR Ibnu Majah 925); tiada doa khusus peperiksaan dalam hadis sahih.")),
    ("doa-minta-zuriat/", dict(
        h1="Doa Minta Zuriat & Anak Soleh: Rumi, Arab & Maksud",
        title="Doa Minta Zuriat & Anak Soleh: Bacaan Rumi, Arab & Maksud",
        desc="Doa memohon zuriat dan anak soleh daripada Al-Quran: doa Nabi Zakaria, doa Nabi Ibrahim dan doa penyejuk mata, dengan tulisan Arab, Rumi dan maksud.",
        lead="Doa para nabi memohon zuriat yang baik daripada Al-Quran, untuk pasangan yang menantikan cahaya mata.",
        box="Doa minta zuriat daripada Al-Quran ialah doa Nabi Zakaria <strong>“Rabbi hab li min ladunka zurriyyatan tayyibah”</strong> (Ali Imran 3:38) dan "
            "<strong>“Rabbi la tazarni fardan wa anta khairul-warithin”</strong> (Al-Anbiya' 21:89), yang dimakbulkan dengan kelahiran Nabi Yahya. Nabi Ibrahim berdoa "
            "<strong>“Rabbi hab li minas-salihin”</strong> (As-Saffat 37:100).",
        sections=[("bacaan", "Doa Minta Zuriat daripada Al-Quran",
                   q_item("ayat-3-38", "Ali Imran 38: doa Nabi Zakaria", [(3, 38)], "") + q_item("ayat-21-89", "Al-Anbiya' 89: jangan biarkan aku bersendirian", [(21, 89)], "")
                   + q_item("ayat-37-100", "As-Saffat 100: doa Nabi Ibrahim", [(37, 100)], "") + q_item("ayat-25-74", "Al-Furqan 74: pasangan dan zuriat penyejuk mata", [(25, 74)], "")),
                  ("lain", "Selepas Bayi Lahir", ul('Pilih nama yang baik dengan <a href="/nama-bayi-islam/">penjana nama bayi Islam</a> (sunnah memberi nama pada hari ketujuh bersama akikah).',
                                                   'Baca <a href="/doa-pelindung-anak/">doa perlindungan untuk anak</a>.'))],
        faq=[("Apakah doa minta zuriat?", "Rabbi hab li min ladunka zurriyyatan tayyibah, innaka sami'ud-du'a' (Ali Imran 3:38): Wahai Tuhanku, kurniakanlah kepadaku zuriat yang baik; sesungguhnya Engkau Maha Mendengar doa."),
             ("Doa siapakah yang dimakbulkan dengan kelahiran anak?", "Nabi Zakaria berdoa ketika sudah tua dan isterinya mandul, lalu Allah mengurniakan Yahya (Al-Anbiya' 21:89–90; Maryam 19:7)."),
             ("Apakah doa untuk pasangan dan anak yang soleh?", "Rabbana hab lana min azwajina wa zurriyyatina qurrata a'yun waj'alna lil-muttaqina imama (Al-Furqan 25:74).")],
        about=["Doa minta zuriat", "Doa anak soleh", "Zuriat"], llms="Doa minta zuriat: Ali Imran 3:38, Al-Anbiya' 21:89, As-Saffat 37:100, Al-Furqan 25:74; disambung ke penjana nama bayi Islam.")),
    ("doa-nabi-yunus/", dict(
        h1="Doa Nabi Yunus: La Ilaha Illa Anta Subhanaka, Rumi & Maksud",
        title="Doa Nabi Yunus: Bacaan Rumi, Arab, Maksud & Kelebihan",
        desc="Doa Nabi Yunus dalam perut ikan (Al-Anbiya' 87): La ilaha illa anta subhanaka inni kuntu minaz-zalimin, dengan tulisan Arab, Rumi, maksud dan kelebihannya.",
        lead="Doa Nabi Yunus ketika di dalam perut ikan, dengan teks Arab, Rumi, maksud, kisah dan kelebihannya dalam hadis.",
        box="Doa Nabi Yunus ialah <strong>“La ilaha illa anta subhanaka inni kuntu minaz-zalimin”</strong> (Al-Anbiya' 21:87): Tiada tuhan melainkan Engkau, Maha Suci Engkau, "
            "sesungguhnya aku termasuk orang yang zalim. Tidak seorang Muslim berdoa dengannya dalam sesuatu urusan melainkan Allah memperkenankannya (HR At-Tirmizi 3505).",
        sections=[("bacaan", "Bacaan Doa Nabi Yunus", q_item("ayat-21-87", "Al-Anbiya' 87–88", [(21, 87), (21, 88)], "HR At-Tirmizi 3505")),
                  ("kisah", "Kisah Ringkas", '<p>Nabi Yunus meninggalkan kaumnya dalam keadaan marah, lalu ditelan ikan besar. Dalam tiga kegelapan (malam, laut dan perut ikan) baginda berdoa, '
                   'dan Allah menyelamatkannya. Baca kisah penuh di <a href="/kisah-nabi/nabi-yunus/">Kisah Nabi Yunus</a>.</p>')],
        faq=[("Apakah doa Nabi Yunus?", "La ilaha illa anta subhanaka inni kuntu minaz-zalimin (Al-Anbiya' 21:87)."),
             ("Apakah kelebihan doa Nabi Yunus?", "Tidak seorang Muslim berdoa dengannya dalam sesuatu urusan melainkan Allah memperkenankannya (HR At-Tirmizi 3505)."),
             ("Berapa kali doa Nabi Yunus perlu dibaca?", "Tiada bilangan khusus dalam hadis sahih. Bilangan seperti 40 atau 100 kali ialah amalan sebahagian orang, bukan ketetapan nas.")],
        about=["Doa Nabi Yunus", "Nabi Yunus"], llms="Doa Nabi Yunus: La ilaha illa anta subhanaka inni kuntu minaz-zalimin (Al-Anbiya' 21:87); dimakbulkan (HR At-Tirmizi 3505); tiada bilangan khusus dalam hadis sahih.")),
    ("doa-sapu-jagat/", dict(
        h1="Doa Sapu Jagat (Rabbana Atina): Rumi, Arab, Maksud & Kelebihan",
        title="Doa Sapu Jagat: Bacaan Rabbana Atina, Rumi, Arab & Maksud",
        desc="Doa Sapu Jagat (Al-Baqarah 201) Rabbana atina fid-dunya hasanah dalam tulisan Arab, Rumi dan maksud, doa yang paling kerap dibaca Rasulullah SAW.",
        lead="Doa kebaikan dunia dan akhirat yang paling kerap dibaca Rasulullah SAW, dikenali di Malaysia sebagai Doa Sapu Jagat.",
        box="Doa Sapu Jagat ialah <strong>“Rabbana atina fid-dunya hasanah, wa fil-akhirati hasanah, wa qina 'azaban-nar”</strong> (Al-Baqarah 2:201). "
            "Anas bin Malik berkata ini ialah doa yang paling kerap dibaca Rasulullah SAW (HR Al-Bukhari 6389; Muslim 2690). Ia juga dibaca antara Rukun Yamani dan Hajar Aswad ketika tawaf (HR Abu Daud 1892).",
        sections=[("bacaan", "Bacaan Doa Sapu Jagat", q_item("ayat-2-201", "Al-Baqarah 201", [(2, 201)], "HR Al-Bukhari 6389; Muslim 2690")),
                  ("maksud", "Kenapa Dinamakan Sapu Jagat", "<p>Doa ini merangkumi segala kebaikan dunia (kesihatan, rezeki, ilmu, keluarga) dan akhirat (keampunan dan syurga), "
                   "serta perlindungan daripada neraka. Kerana ia “menyapu” semua kebaikan, masyarakat Melayu menamakannya Doa Sapu Jagat.</p>")],
        faq=[("Apakah doa Sapu Jagat?", "Rabbana atina fid-dunya hasanah, wa fil-akhirati hasanah, wa qina 'azaban-nar (Al-Baqarah 2:201): Wahai Tuhan kami, berilah kami kebaikan di dunia dan kebaikan di akhirat, dan peliharalah kami daripada azab neraka."),
             ("Kenapa doa Sapu Jagat penting?", "Ia doa yang paling kerap dibaca Rasulullah SAW (HR Al-Bukhari 6389; Muslim 2690)."),
             ("Bilakah doa Sapu Jagat dibaca?", "Bila-bila masa: selepas solat, sebagai penutup doa, dan ketika tawaf antara Rukun Yamani dan Hajar Aswad (HR Abu Daud 1892).")],
        about=["Doa Sapu Jagat", "Rabbana atina", "Doa Rabbana"], llms="Doa Sapu Jagat: Rabbana atina fid-dunya hasanah... (Al-Baqarah 2:201), doa paling kerap Rasulullah SAW (HR Al-Bukhari 6389; Muslim 2690); ketika tawaf (HR Abu Daud 1892).")),
    ("doa-naik-kenderaan/", dict(
        h1="Doa Naik Kenderaan & Doa Musafir: Rumi, Arab & Maksud",
        title="Doa Naik Kenderaan: Bacaan Rumi, Arab & Maksud (Az-Zukhruf 13–14)",
        desc="Doa naik kenderaan Subhanallazi sakhkhara lana haza (Az-Zukhruf 13–14) dalam tulisan Arab, Rumi dan maksud, serta cara membacanya ketika musafir.",
        lead="Doa ketika menaiki kereta, motosikal, bas, kapal terbang atau apa jua kenderaan, daripada Al-Quran dengan cara Rasulullah SAW membacanya.",
        box="Doa naik kenderaan ialah <strong>“Subhanallazi sakhkhara lana haza wa ma kunna lahu muqrinin, wa inna ila rabbina lamunqalibun”</strong> (Az-Zukhruf 43:13–14). "
            "Ketika bermusafir, Rasulullah SAW bertakbir tiga kali, kemudian membacanya (HR Muslim 1342). Ali bin Abi Talib memulakan dengan Bismillah dan Alhamdulillah (HR Abu Daud 2602).",
        sections=[("bacaan", "Bacaan Doa Naik Kenderaan", q_item("ayat-43-13", "Az-Zukhruf 13–14", [(43, 13), (43, 14)], "HR Muslim 1342",
                                                                note="Lafaz doa bermula pada “Subhanallazi sakhkhara lana haza” di hujung ayat 13.")),
                  ("cara", "Cara Membaca", table(["Langkah", "Bacaan"], [["1", "Bismillah (ketika menaiki)"], ["2", "Alhamdulillah"], ["3", "Allahu Akbar (3 kali, ketika musafir)"],
                                                                        ["4", "Subhanallazi sakhkhara lana haza… lamunqalibun"]], "Cara membaca doa naik kenderaan")
                   + '<p class="note">Untuk perjalanan jauh, lihat <a href="/solat-jamak-qasar/">solat jamak & qasar</a> dan <a href="/doa-keluar-rumah/">doa keluar rumah</a>.</p>')],
        faq=[("Apakah doa naik kenderaan?", "Subhanallazi sakhkhara lana haza wa ma kunna lahu muqrinin, wa inna ila rabbina lamunqalibun (Az-Zukhruf 43:13–14): Maha Suci Tuhan yang memudahkan kenderaan ini bagi kami, sedangkan kami tidak mampu menguasainya, dan kepada Tuhan kamilah kami akan kembali."),
             ("Adakah doa ini dibaca untuk kereta dan kapal terbang?", "Ya. Ayat ini asalnya tentang kapal dan binatang tunggangan, dan ulama menggunakannya untuk semua jenis kenderaan."),
             ("Apakah doa musafir yang panjang?", "Dalam HR Muslim 1342, selepas ayat ini Rasulullah SAW memohon kebaikan, takwa dan kemudahan dalam perjalanan serta perlindungan untuk keluarga yang ditinggalkan.")],
        about=["Doa naik kenderaan", "Doa musafir"], llms="Doa naik kenderaan: Subhanallazi sakhkhara lana haza... (Az-Zukhruf 43:13–14); takbir 3 kali ketika musafir (HR Muslim 1342); Bismillah dan Alhamdulillah (HR Abu Daud 2602).")),
    ("doa-ziarah-kubur/", dict(
        h1="Doa Ziarah Kubur: Bacaan Rumi, Arab, Maksud & Adab",
        title="Doa Ziarah Kubur: Bacaan Rumi, Arab, Maksud & Adab (Sahih Muslim)",
        desc="Doa ziarah kubur Assalamu 'alaikum ahlad-diyar daripada Sahih Muslim dengan tulisan Arab, Rumi dan maksud, serta adab dan amalan ketika menziarahi kubur.",
        lead="Salam dan doa yang diajar Rasulullah SAW ketika menziarahi kubur, dengan adab dan amalan yang dibenarkan.",
        box="Ketika menziarahi kubur, ucapkan <strong>“Assalamu 'alaikum ahlad-diyari minal-mu'minina wal-muslimin, wa inna in sya Allahu lalahiqun, as'alullaha lana wa lakumul-'afiyah”</strong> "
            "(HR Muslim 975). Ziarah kubur disunatkan kerana ia mengingatkan kepada akhirat (HR Muslim 976).",
        sections=[("bacaan", "Bacaan Doa Ziarah Kubur", h_item("ziarah-kubur")),
                  ("adab", "Adab Ziarah Kubur", ul("Memberi salam dan mendoakan keampunan untuk ahli kubur." + ref("HR Muslim 975"),
                                                   "Tidak duduk atau berjalan di atas kubur." + ref("HR Muslim 971, 972"),
                                                   "Mengambil pengajaran tentang kematian; ia mengingatkan akhirat." + ref("HR Muslim 976"),
                                                   'Membaca <a href="/surah-yasin/">Surah Yasin</a>, <a href="/tahlil-ringkas/">tahlil</a> dan berdoa untuk arwah.'))],
        faq=[("Apakah doa ziarah kubur?", "Assalamu 'alaikum ahlad-diyari minal-mu'minina wal-muslimin, wa inna in sya Allahu lalahiqun, as'alullaha lana wa lakumul-'afiyah (HR Muslim 975)."),
             ("Bolehkah wanita menziarahi kubur?", "Ulama berbeza pendapat. Ramai ulama mazhab Syafi'i berpendapat makruh bagi wanita kerana dikhuatiri tidak dapat menahan perasaan, dan harus jika terpelihara adabnya. Rujuk pejabat agama negeri anda."),
             ("Bilakah waktu menziarahi kubur?", "Tiada waktu khusus dalam hadis sahih. Ia boleh dilakukan bila-bila masa, termasuk selepas Hari Raya.")],
        about=["Doa ziarah kubur", "Ziarah kubur"], llms="Doa ziarah kubur: Assalamu 'alaikum ahlad-diyari minal-mu'minina wal-muslimin... (HR Muslim 975); ziarah mengingatkan akhirat (HR Muslim 976).")),
    ("doa-orang-sakit/", dict(
        h1="Doa untuk Orang Sakit & Doa Cepat Sembuh: Rumi, Arab & Maksud",
        title="Doa Orang Sakit & Cepat Sembuh: Bacaan Rumi, Arab & Maksud",
        desc="Doa untuk orang sakit dan doa cepat sembuh daripada Sahih Bukhari dan Muslim, doa ketika diri sendiri sakit, dengan tulisan Arab, Rumi dan maksud.",
        lead="Doa yang dibaca Rasulullah SAW untuk orang sakit dan doa ketika diri sendiri merasa sakit, daripada hadis sahih.",
        box="Doa untuk orang sakit ialah <strong>“Allahumma rabban-nas, azhibil-ba's, isyfi wa antasy-syafi, la syifa'a illa syifa'uk, syifa'an la yughadiru saqama”</strong> "
            "(HR Al-Bukhari 5675; Muslim 2191). Jika diri sendiri sakit, letakkan tangan pada tempat yang sakit, baca Bismillah 3 kali dan "
            "<strong>“A'uzu billahi wa qudratihi min syarri ma ajidu wa uhaziru”</strong> 7 kali (HR Muslim 2202).",
        sections=[("bacaan", "Doa untuk Orang Sakit", h_item("orang-sakit")),
                  ("sendiri", "Doa Ketika Diri Sendiri Sakit", h_item("sakit-sendiri")),
                  ("ziarah", "Kelebihan Menziarahi Orang Sakit", ul("Orang yang menziarahi saudaranya yang sakit berada di taman syurga sehingga dia pulang." + ref("HR Muslim 2568"),
                                                                    "Doakan kesembuhan dan beri semangat; jangan memberatkan pesakit dengan ziarah yang terlalu lama."))],
        faq=[("Apakah doa untuk orang sakit?", "Allahumma rabban-nas, azhibil-ba's, isyfi wa antasy-syafi, la syifa'a illa syifa'uk, syifa'an la yughadiru saqama (HR Al-Bukhari 5675; Muslim 2191)."),
             ("Apakah doa ketika diri sendiri sakit?", "Letak tangan pada tempat sakit, baca Bismillah 3 kali, kemudian A'uzu billahi wa qudratihi min syarri ma ajidu wa uhaziru 7 kali (HR Muslim 2202)."),
             ("Adakah doa menggantikan rawatan perubatan?", "Tidak. Rasulullah SAW menyuruh berubat (HR Abu Daud 3855). Doa dan rawatan dilakukan bersama.")],
        about=["Doa orang sakit", "Doa cepat sembuh"], llms="Doa orang sakit: Allahumma rabban-nas azhibil-ba's... (HR Al-Bukhari 5675; Muslim 2191); diri sendiri sakit: Bismillah 3x, A'uzu billahi wa qudratihi... 7x (HR Muslim 2202).")),
    ("doa-selepas-wuduk/", dict(
        h1="Doa Selepas Wuduk: Bacaan Rumi, Arab, Maksud & Kelebihan",
        title="Doa Selepas Wuduk: Bacaan Rumi, Arab, Maksud & Kelebihan",
        desc="Doa selepas wuduk dalam tulisan Arab, Rumi dan maksud daripada Sahih Muslim dan At-Tirmizi: dibukakan lapan pintu syurga bagi yang membacanya.",
        lead="Doa yang dibaca selepas selesai berwuduk, dengan kelebihan dibukakan pintu-pintu syurga.",
        box="Selepas wuduk, baca <strong>“Asyhadu alla ilaha illallahu wahdahu la syarika lah, wa asyhadu anna Muhammadan 'abduhu wa rasuluh”</strong>: dibukakan baginya "
            "lapan pintu syurga dan dia masuk dari mana-mana yang dikehendaki (HR Muslim 234). At-Tirmizi (55) menambah <strong>“Allahummaj'alni minat-tawwabin, waj'alni minal-mutatahhirin”</strong>.",
        sections=[("bacaan", "Bacaan Doa Selepas Wuduk", h_item("selepas-wuduk")),
                  ("lain", "Seterusnya", ul('Pelajari rukun dan cara solat di <a href="/belajar-solat/">Cara Solat Lengkap</a>.', 'Solat sunat selepas wuduk ialah amalan Bilal yang didengar terompahnya di syurga (HR Al-Bukhari 1149).'))],
        faq=[("Apakah doa selepas wuduk?", "Asyhadu alla ilaha illallahu wahdahu la syarika lah, wa asyhadu anna Muhammadan 'abduhu wa rasuluh (HR Muslim 234), ditambah Allahummaj'alni minat-tawwabin waj'alni minal-mutatahhirin (HR At-Tirmizi 55)."),
             ("Apakah kelebihan doa selepas wuduk?", "Dibukakan lapan pintu syurga untuknya dan dia boleh masuk dari mana-mana pintu yang dikehendaki (HR Muslim 234)."),
             ("Adakah sunat menadah tangan atau memandang ke langit?", "Riwayat yang menyebut memandang ke langit selepas wuduk dinilai lemah oleh ramai ulama hadis. Yang sahih ialah lafaz doa di atas.")],
        about=["Doa selepas wuduk", "Wuduk"], llms="Doa selepas wuduk: Asyhadu alla ilaha illallahu wahdahu la syarika lah... (HR Muslim 234), Allahummaj'alni minat-tawwabin... (HR At-Tirmizi 55); lapan pintu syurga dibuka.")),
    ("doa-pelindung-anak/", dict(
        h1="Doa Pelindung Anak daripada Gangguan & Ain: Rumi, Arab & Maksud",
        title="Doa Pelindung Anak (Ain & Gangguan): Bacaan Rumi, Arab & Maksud",
        desc="Doa pelindung anak dan bayi daripada gangguan syaitan dan penyakit ain, dibaca Rasulullah SAW untuk Hasan dan Husain (Sahih Bukhari), dengan Rumi & maksud.",
        lead="Doa yang dibaca Rasulullah SAW untuk melindungi cucunya Hasan dan Husain, dengan lafaz untuk seorang anak lelaki, perempuan atau ramai.",
        box="Rasulullah SAW melindungi Hasan dan Husain dengan doa <strong>“U'izukuma bikalimatillahit-tammah, min kulli syaitanin wa hammah, wa min kulli 'ainin lammah”</strong>, "
            "dan baginda berkata Nabi Ibrahim melindungi Ismail dan Ishak dengannya (HR Al-Bukhari 3371). Bagi seorang anak lelaki sebut <strong>U'izuka</strong>, perempuan <strong>U'izuki</strong>, ramai <strong>U'izukum</strong>.",
        sections=[("bacaan", "Bacaan Doa Pelindung Anak", h_item("pelindung-anak")),
                  ("lafaz", "Lafaz Mengikut Bilangan Anak", table(["Untuk", "Awal lafaz (Rumi)"], [["Seorang anak lelaki", "U'izuka…"], ["Seorang anak perempuan", "U'izuki…"],
                                                                                              ["Dua orang anak", "U'izukuma…"], ["Tiga orang atau lebih", "U'izukum…"]], "Lafaz doa pelindung anak")),
                  ("lain", "Amalan Lain untuk Anak", ul('Membaca Al-Ikhlas, Al-Falaq dan An-Nas (3 Qul): lihat <a href="/zikir-pagi-petang/">zikir pagi & petang</a>.',
                                                       'Memilih nama yang baik: <a href="/nama-bayi-islam/">penjana nama bayi Islam</a>.', 'Doa memohon zuriat soleh: <a href="/doa-minta-zuriat/">doa minta zuriat</a>.'))],
        faq=[("Apakah doa pelindung anak?", "U'izukuma bikalimatillahit-tammah, min kulli syaitanin wa hammah, wa min kulli 'ainin lammah (HR Al-Bukhari 3371), dibaca Rasulullah SAW untuk Hasan dan Husain."),
             ("Apakah maksud 'ainin lammah'?", "Pandangan mata yang membawa mudarat (penyakit ain), sama ada daripada rasa dengki atau kagum yang tidak disertai zikir."),
             ("Bagaimana membacanya untuk seorang bayi?", "Untuk bayi lelaki sebut U'izuka, bayi perempuan U'izuki, kemudian sambung bikalimatillahit-tammah hingga akhir.")],
        about=["Doa pelindung anak", "Penyakit ain", "Doa untuk bayi"], llms="Doa pelindung anak: U'izukuma bikalimatillahit-tammah, min kulli syaitanin wa hammah, wa min kulli 'ainin lammah (HR Al-Bukhari 3371); U'izuka (lelaki), U'izuki (perempuan), U'izukum (ramai).")),
    ("doa-taubat/", dict(
        h1="Doa Taubat & Istighfar: Penghulu Istighfar, Doa Nabi Adam & Rumi",
        title="Doa Taubat & Penghulu Istighfar: Bacaan Rumi, Arab & Maksud",
        desc="Doa taubat daripada Al-Quran dan hadis sahih: Sayyidul Istighfar, doa taubat Nabi Adam dan Nabi Musa, dengan tulisan Arab, Rumi, maksud dan syarat taubat.",
        lead="Doa memohon ampun daripada Al-Quran dan Penghulu Istighfar daripada Sahih Bukhari, dengan syarat-syarat taubat nasuha.",
        box="Doa taubat yang paling utama ialah <strong>Sayyidul Istighfar</strong> (Penghulu Istighfar): sesiapa membacanya dengan yakin pada siang hari lalu meninggal sebelum petang, "
            "dia termasuk ahli syurga (HR Al-Bukhari 6306). Daripada Al-Quran, Nabi Adam dan Hawa berdoa <strong>“Rabbana zalamna anfusana…”</strong> (Al-A'raf 7:23).",
        sections=[("bacaan", "Penghulu Istighfar", z_card("sayyidul")),
                  ("quran", "Doa Taubat daripada Al-Quran", q_item("ayat-7-23", "Al-A'raf 23: doa taubat Nabi Adam dan Hawa", [(7, 23)], "") + q_item("ayat-28-16", "Al-Qasas 16: pengakuan Nabi Musa", [(28, 16)], "")),
                  ("syarat", "Syarat Taubat Nasuha", ul("Berhenti daripada dosa itu.", "Menyesal atas perbuatannya.", "Berazam tidak mengulanginya.",
                                                         "Jika berkaitan hak manusia, mengembalikan hak itu atau memohon maaf.", "Allah menyeru taubat nasuha (At-Tahrim 66:8)."))],
        faq=[("Apakah doa taubat yang paling utama?", "Sayyidul Istighfar: Allahumma anta rabbi la ilaha illa anta, khalaqtani wa ana 'abduk… Sesiapa membacanya dengan yakin lalu meninggal pada hari itu, dia termasuk ahli syurga (HR Al-Bukhari 6306)."),
             ("Apakah doa taubat Nabi Adam?", "Rabbana zalamna anfusana wa in lam taghfir lana wa tarhamna lanakunanna minal-khasirin (Al-A'raf 7:23)."),
             ("Apakah syarat taubat diterima?", "Berhenti daripada dosa, menyesal, berazam tidak mengulanginya dan mengembalikan hak orang lain jika ada. Taubat diterima selagi nyawa belum sampai ke kerongkong.")],
        about=["Doa taubat", "Istighfar", "Sayyidul Istighfar"], llms="Doa taubat: Sayyidul Istighfar (HR Al-Bukhari 6306), Al-A'raf 7:23 (Nabi Adam), Al-Qasas 28:16 (Nabi Musa); syarat taubat nasuha (At-Tahrim 66:8).")),
]
for _, d in PAGES:
    d["published"] = PUB


def build_pages18(ctx):
    import pages16
    return build_doa(PAGES, ctx, PUB, pages16.PAGES + PAGES)
