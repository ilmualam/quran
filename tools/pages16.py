"""Pages: one static page per most-searched doa / ayat amalan: /ayat-kursi/, /amanar-rasul/, /doa-qunut/, /doa-iftitah/,
/tahiyat-akhir/, /doa-selepas-solat/, /doa-sebelum-tidur/, /doa-makan/, /doa-masuk-tandas/.

No Arabic is typed here: Quranic text comes from data-surah/ by reference, hadith doa from ibadah.py (DOA_HARIAN, Z_SOLAT,
Z_TIDUR) and solat recitations from ibadah2.py (BACAAN), each with its book and hadith number. The hub collections
(/doa-harian/, /zikir-pagi-petang/, /belajar-solat/) keep the full lists; these pages answer one search each.
kind="tool" so alat.js adds the copy buttons and the daily zikir counters (same ids as /zikir-pagi-petang/)."""
import ibadah as I
import ibadah2 as I2
import plans as P
import rumi_ms as RM
from pages import e, faq_html, hero, side, meta_line, table, tool_cards, SITE
from pages2 import card, quran_block, qref, zref

PUB = "2026-11-07"
H = {d[0]: d for d in I.DOA_HARIAN}
TIDUR = [z for z in I.Z_TIDUR if z[0] != "t-bismika"]  # the sleep doa itself is shown above the list on /doa-sebelum-tidur/


def q_item(id_, title, refs, src, note="", n=None):
    ar, ru, mn = quran_block(refs)
    s, a = refs[0]
    rng = f"{P.NAMES[s - 1]} {s}:{a}" + (f"–{refs[-1][1]}" if len(refs) > 1 else "")
    link = f'<a href="/#surah-{s}-ayat-{a}">{e(rng)}</a>'
    return card(id_, title, ar, ru, mn, f"{e(src)} · {link}" if src else link, extra=note, counter=n, cls="dw zw" if n else "dw")


def h_item(key, title=None):
    _, t, ar, ru, mn, src = H[key]
    return card(key, title or t, e(ar), e(ru), e(mn), e(src))


def b_item(key):
    t, how, ar, ru, mn, src = I2.BACAAN[key]
    return card(key, t, e(ar), e(ru), e(mn), e(src), extra=how)


def z_items(lst):
    out = []
    for i, t, ar, ru, mn, n, src, note in lst:
        if ar.startswith("Q"):
            groups = zref(ar)
            ar_, ru_, mn_ = (" ".join(quran_block(g)[k] for g in groups) for k in range(3))
            src_ = e(src) + " · " + ", ".join(qref(g[0][0], g[0][1]) for g in groups)
            out.append(card(i, t, ar_, ru_, mn_, src_, extra=note, counter=n, cls="dw zw"))
        else:
            out.append(card(i, t, e(ar), e(ru), e(mn), e(src), extra=note, counter=n, cls="dw zw"))
    return "".join(out)


def zsec(id_, h, items_html, count, lead):
    return (f'<section class="zsec" id="{id_}" aria-labelledby="h-{id_}"><div class="zhd"><h2 id="h-{id_}">{h}</h2>'
            f'<p class="zprog" aria-live="polite">0 / {count} selesai hari ini</p><button class="btn2 sm" type="button" data-zreset>⟲ Set semula</button></div>'
            f'<p class="note">{lead}</p>{items_html}</section>')


def where(s, a):
    g = P.gid(s, a)
    juz = next(j for j in range(1, 31) if P.JS[j - 1] <= g < P.JS[j])
    return juz, P.page_of(g)


KJ, KP = where(2, 255)
AJ, AP = where(2, 285)

# path: dict(h1, title, desc, lead, box, sections=[(id, heading, html)], faq, about, llms, zk)
PAGES = [
    ("ayat-kursi/", dict(
        h1="Ayat Kursi: Bacaan Arab, Rumi, Maksud & Kelebihan",
        title="Ayat Kursi: Bacaan Rumi, Arab, Maksud & Kelebihan (2:255)",
        desc="Bacaan Ayat Kursi (Al-Baqarah 255) dalam tulisan Arab, Rumi dan maksud Bahasa Melayu, serta kelebihan dan waktu membacanya dengan rujukan hadis.",
        lead="Ayat Kursi ialah Surah Al-Baqarah ayat 255, ayat yang paling agung dalam Al-Quran. Teks Arab, Rumi dan maksud penuh, dengan audio.",
        box=f"<strong>Ayat Kursi</strong> ialah <strong>Surah Al-Baqarah ayat 255</strong>, dalam Juz {KJ} (muka surat {KP} Mushaf Madinah). Nabi SAW menyebutnya "
            "<strong>ayat yang paling agung</strong> dalam Al-Quran (HR Muslim 810). Ia sunat dibaca <strong>sebelum tidur</strong>, <strong>selepas solat fardu</strong> "
            "dan pada <strong>pagi dan petang</strong>.",
        sections=[
            ("bacaan", "Bacaan Ayat Kursi", q_item("ayat-kursi", "Ayat Kursi (Al-Baqarah 2:255)", [(2, 255)], "")),
            ("kelebihan", "Kelebihan Ayat Kursi", "<ul>"
             "<li>Ayat yang paling agung dalam Al-Quran: Nabi SAW bertanya kepada Ubay bin Ka'ab ayat manakah yang paling agung, lalu dia menjawab Ayat Kursi dan Baginda membenarkannya. <span class=\"nref\">(HR Muslim 810)</span></li>"
             "<li>Dibaca sebelum tidur: dipelihara oleh Allah sepanjang malam dan syaitan tidak mendekati hingga pagi. <span class=\"nref\">(HR Al-Bukhari 2311)</span></li>"
             "<li>Dibaca selepas setiap solat fardu: tiada yang menghalangnya masuk syurga melainkan kematian. <span class=\"nref\">(HR An-Nasa'i dalam As-Sunan Al-Kubra)</span></li>"
             "<li>Dibaca pagi dan petang sebagai pelindung daripada gangguan jin. <span class=\"nref\">(HR An-Nasa'i dalam As-Sunan Al-Kubra; Al-Hakim)</span></li></ul>"),
            ("waktu", "Bila Membaca Ayat Kursi", table(["Waktu", "Bilangan", "Halaman berkaitan"], [
                ["Selepas solat fardu", "1 kali", '<a href="/doa-selepas-solat/">Zikir selepas solat</a>'],
                ["Sebelum tidur", "1 kali", '<a href="/doa-sebelum-tidur/">Doa & zikir sebelum tidur</a>'],
                ["Pagi dan petang", "1 kali", '<a href="/zikir-pagi-petang/">Zikir pagi & petang</a>']], "Waktu membaca Ayat Kursi")),
        ],
        faq=[("Ayat Kursi surah apa dan ayat ke berapa?", f"Ayat Kursi ialah Surah Al-Baqarah (surah ke-2) ayat 255, dalam Juz {KJ}, muka surat {KP} Mushaf Madinah."),
             ("Apakah maksud Kursi?", "Kursi bermaksud kerusi atau tempat letak kaki, disebut dalam ayat ini: “Kursi-Nya meliputi langit dan bumi”. Ulama berbeza pendapat tentang hakikatnya; ramai yang menafsirkannya sebagai ilmu dan kekuasaan Allah, dan kita mengimaninya tanpa menyamakan Allah dengan makhluk."),
             ("Bolehkah membaca Ayat Kursi ketika haid?", "Dalam mazhab Syafi'i, wanita haid tidak dibenarkan membaca Al-Quran dengan niat tilawah, tetapi boleh membaca Ayat Kursi dengan niat zikir atau perlindungan, dan boleh mendengarnya."),
             ("Berapa kali Ayat Kursi dibaca sebelum tidur?", "Sekali. Hadis riwayat Al-Bukhari (2311) menyebut membacanya ketika hendak tidur menjadikan seseorang dipelihara oleh Allah sepanjang malam."),
             ("Apakah ayat sebelum dan selepas Ayat Kursi?", "Sebelumnya Al-Baqarah 254 (seruan berinfak sebelum datang hari tiada jual beli), dan selepasnya Al-Baqarah 256 (“Tiada paksaan dalam agama”). Ayat 255 sahaja ialah Ayat Kursi.")],
        about=["Ayat Kursi", "Al-Baqarah", "Zikir"],
        llms=f"Ayat Kursi (Al-Baqarah 2:255, Juz {KJ}, muka surat {KP}): teks Arab, Rumi, maksud; ayat paling agung (HR Muslim 810); sebelum tidur (HR Al-Bukhari 2311); selepas solat fardu.")),
    ("amanar-rasul/", dict(
        h1="Amanar Rasul (2 Ayat Terakhir Al-Baqarah): Bacaan & Kelebihan",
        title="Amanar Rasul: Bacaan Rumi, Arab & Maksud (Al-Baqarah 285–286)",
        desc="Bacaan Amanar Rasul, dua ayat terakhir Surah Al-Baqarah (285–286), dalam tulisan Arab, Rumi dan maksud, serta kelebihan membacanya pada waktu malam.",
        lead="Amanar Rasul ialah dua ayat terakhir Surah Al-Baqarah (ayat 285–286). Teks Arab, Rumi dan maksud penuh dengan rujukan hadis.",
        box=f"<strong>Amanar Rasul</strong> ialah <strong>Surah Al-Baqarah ayat 285 dan 286</strong>, dua ayat penutup surah itu (Juz {AJ}, muka surat {AP}). "
            "Sesiapa membacanya pada waktu malam, <strong>kedua-dua ayat itu mencukupinya</strong> (HR Al-Bukhari 5009; Muslim 807).",
        sections=[
            ("bacaan", "Bacaan Amanar Rasul", q_item("amanar-rasul", "Al-Baqarah 2:285–286", [(2, 285), (2, 286)], "")),
            ("kelebihan", "Kelebihan Amanar Rasul", "<ul>"
             "<li>Sesiapa membaca dua ayat terakhir Surah Al-Baqarah pada waktu malam, kedua-duanya mencukupinya. <span class=\"nref\">(HR Al-Bukhari 5009; Muslim 807)</span></li>"
             "<li>Malaikat memberitahu Nabi SAW tentang dua cahaya yang tidak diberikan kepada nabi sebelumnya: Al-Fatihah dan penutup Surah Al-Baqarah. <span class=\"nref\">(HR Muslim 806)</span></li>"
             "<li>Ayat 286 mengandungi doa “Rabbana la tu'akhizna…”: memohon tidak dibebani melebihi kemampuan, keampunan dan pertolongan.</li></ul>"),
        ],
        faq=[("Amanar Rasul ayat berapa?", "Surah Al-Baqarah ayat 285 (“Amanar-rasulu bima unzila ilaihi…”) dan ayat 286 (“La yukallifullahu nafsan illa wus'aha…”)."),
             ("Bilakah Amanar Rasul dibaca?", "Pada waktu malam, lazimnya sebelum tidur, berdasarkan HR Al-Bukhari 5009 dan Muslim 807. Ramai juga membacanya sebagai penutup bacaan Surah Al-Baqarah."),
             ("Apakah maksud “kedua-duanya mencukupinya”?", "Ulama menghuraikannya sebagai mencukupi daripada qiamullail, atau memelihara pembacanya daripada keburukan dan gangguan syaitan pada malam itu.")],
        about=["Amanar Rasul", "Al-Baqarah", "Zikir sebelum tidur"],
        llms="Amanar Rasul (Al-Baqarah 2:285–286): teks Arab, Rumi, maksud; dibaca pada waktu malam (HR Al-Bukhari 5009; Muslim 807); dua cahaya (HR Muslim 806).")),
    ("doa-qunut/", dict(
        h1="Doa Qunut Subuh: Bacaan Rumi, Arab, Maksud & Hukum",
        title="Doa Qunut Subuh: Bacaan Rumi, Arab & Maksud (Mazhab Syafi'i)",
        desc="Bacaan doa qunut solat Subuh dalam tulisan Arab, Rumi dan maksud, bila dibaca, lafaz imam, qunut witir dan hukum jika tertinggal mengikut mazhab Syafi'i.",
        lead="Doa qunut dibaca ketika iktidal rakaat kedua solat Subuh. Teks Arab, Rumi dan maksud, dengan cara dan hukumnya dalam mazhab Syafi'i.",
        box="Dalam mazhab Syafi'i, <strong>doa qunut</strong> ialah <strong>sunat ab'adh</strong> yang dibaca ketika <strong>iktidal rakaat kedua solat Subuh</strong> "
            "sambil mengangkat kedua-dua tangan. Jika tertinggal, <strong>sunat sujud sahwi</strong> sebelum salam. Lafaznya daripada HR Abu Daud 1425 dan At-Tirmizi 464.",
        sections=[
            ("bacaan", "Bacaan Doa Qunut", b_item("qunut")),
            ("cara", "Cara dan Hukum Qunut", "<ul>"
             "<li><strong>Bila:</strong> selepas bangun dari rukuk (iktidal) pada rakaat kedua solat Subuh, sebelum sujud.</li>"
             "<li><strong>Hukum:</strong> sunat ab'adh dalam mazhab Syafi'i. Solat tetap sah jika tertinggal, tetapi sunat menggantinya dengan sujud sahwi.</li>"
             "<li><strong>Imam:</strong> ketika berjemaah, imam menukar lafaz tunggal kepada jamak (contohnya “ihdina” bagi “ihdini”) supaya doa meliputi makmum; makmum mengaminkan bahagian doa dan membaca bersama bahagian pujian.</li>"
             "<li><strong>Qunut witir:</strong> dibaca pada rakaat terakhir solat witir pada separuh kedua Ramadan (malam ke-16 hingga akhir) dalam mazhab Syafi'i. Rujuk <a href=\"/solat-sunat/solat-witir/\">cara solat witir</a>.</li>"
             "<li><strong>Qunut nazilah:</strong> dibaca dalam semua solat fardu ketika umat Islam ditimpa musibah besar.</li>"
             "<li><strong>Penutup:</strong> lazimnya ditutup dengan selawat ke atas Nabi SAW.</li></ul>"
             '<p class="note">Mazhab lain (seperti Hanafi dan Hanbali) tidak menjadikan qunut Subuh sunat yang tetap. Ikuti amalan mazhab Syafi\'i yang menjadi pegangan rasmi di Malaysia.</p>'),
        ],
        faq=[("Adakah solat Subuh sah tanpa qunut?", "Sah. Qunut ialah sunat ab'adh, bukan rukun. Dalam mazhab Syafi'i, sunat sujud sahwi jika ia tertinggal."),
             ("Bagaimana jika terlupa membaca qunut?", "Teruskan solat dan lakukan sujud sahwi (dua kali sujud) selepas tahiyat akhir dan sebelum salam."),
             ("Perlukah mengangkat tangan ketika qunut?", "Sunat mengangkat kedua-dua tangan ketika membaca doa qunut menurut pendapat yang muktamad dalam mazhab Syafi'i."),
             ("Bolehkah membaca qunut jika tidak hafal?", "Boleh membaca daripada teks semasa belajar, atau membaca doa lain yang mengandungi pujian dan doa. Usahakan menghafalnya kerana ia dibaca setiap hari.")],
        about=["Doa qunut", "Solat Subuh", "Mazhab Syafi'i"],
        llms="Doa qunut Subuh (HR Abu Daud 1425; At-Tirmizi 464): teks Arab, Rumi, maksud; sunat ab'adh mazhab Syafi'i pada iktidal rakaat kedua; sujud sahwi jika tertinggal; qunut witir separuh kedua Ramadan; qunut nazilah.")),
    ("doa-iftitah/", dict(
        h1="Doa Iftitah: Bacaan Rumi, Arab & Maksud",
        title="Doa Iftitah: Bacaan Rumi, Arab & Maksud Lengkap",
        desc="Bacaan doa iftitah (doa pembuka solat) dalam tulisan Arab, Rumi dan maksud Bahasa Melayu, bila dibaca dan hukumnya, dengan rujukan HR Muslim.",
        lead="Doa iftitah ialah doa pembuka solat yang dibaca selepas takbiratul ihram dan sebelum Al-Fatihah. Teks Arab, Rumi dan maksud lengkap.",
        box="<strong>Doa iftitah</strong> dibaca <strong>selepas takbiratul ihram dan sebelum Al-Fatihah</strong>, pada <strong>rakaat pertama sahaja</strong>. "
            "Hukumnya <strong>sunat</strong>: solat tetap sah tanpanya. Lafaz “Allahu akbaru kabira… wajjahtu wajhiya…” berdasarkan HR Muslim 601 dan 771.",
        sections=[
            ("bacaan", "Bacaan Doa Iftitah", b_item("iftitah")),
            ("cara", "Bila dan Bagaimana", "<ul>"
             "<li>Selepas takbiratul ihram, letak tangan kanan di atas tangan kiri dan baca doa iftitah secara perlahan, termasuk ketika menjadi makmum.</li>"
             "<li>Hanya pada rakaat pertama. Rakaat seterusnya terus dengan Al-Fatihah (didahului ta'awwuz).</li>"
             "<li>Makmum masbuq yang bimbang tidak sempat menghabiskan Al-Fatihah boleh meninggalkannya.</li>"
             "<li>Tidak dibaca dalam solat jenazah.</li></ul>"),
        ],
        faq=[("Apakah hukum membaca doa iftitah?", "Sunat. Solat tetap sah jika tidak dibaca, dan tidak perlu sujud sahwi kerana ia bukan sunat ab'adh."),
             ("Adakah doa iftitah dibaca setiap rakaat?", "Tidak. Ia dibaca pada rakaat pertama sahaja, selepas takbiratul ihram."),
             ("Adakah ada lafaz doa iftitah lain?", "Ada beberapa lafaz sahih, contohnya “Allahumma ba'id baini wa baina khatayaya…” (HR Al-Bukhari 744). Lafaz “wajjahtu wajhiya” di sini paling lazim di Malaysia.")],
        about=["Doa iftitah", "Cara solat"],
        llms="Doa iftitah (HR Muslim 601 & 771): teks Arab, Rumi, maksud; sunat selepas takbiratul ihram pada rakaat pertama.")),
    ("tahiyat-akhir/", dict(
        h1="Bacaan Tahiyat Akhir (dan Tahiyat Awal): Rumi, Arab & Maksud",
        title="Bacaan Tahiyat Akhir & Awal: Rumi, Arab dan Maksud",
        desc="Bacaan tahiyat akhir dan tahiyat awal dalam tulisan Arab, Rumi dan maksud, dengan selawat Ibrahimiyyah, cara duduk dan beza kedua-duanya.",
        lead="Tahiyat akhir ialah rukun solat yang dibaca ketika duduk pada rakaat terakhir. Teks Arab, Rumi dan maksud, serta beza dengan tahiyat awal.",
        box="<strong>Tahiyat akhir</strong> ialah <strong>rukun solat</strong>: tasyahhud diikuti <strong>selawat ke atas Nabi SAW</strong> pada rakaat terakhir, "
            "duduk secara <strong>tawarruk</strong>. <strong>Tahiyat awal</strong> (rakaat kedua solat 3 atau 4 rakaat) pula sunat ab'adh dan berakhir pada “Allahumma solli 'ala Muhammad”.",
        sections=[
            ("bacaan", "Bacaan Tahiyat Akhir", b_item("tahiyat-akhir")),
            ("awal", "Bacaan Tahiyat Awal", b_item("tahiyat-awal")),
            ("beza", "Beza Tahiyat Awal dan Tahiyat Akhir", table(["Perkara", "Tahiyat awal", "Tahiyat akhir"], [
                ["Hukum", "Sunat ab'adh (sujud sahwi jika tertinggal)", "Rukun (solat tidak sah tanpanya)"],
                ["Bila", "Rakaat kedua solat 3 atau 4 rakaat", "Rakaat terakhir setiap solat"],
                ["Cara duduk", "Iftirasy (duduk di atas kaki kiri)", "Tawarruk (punggung kiri di lantai)"],
                ["Bacaan", "Tasyahhud + “Allahumma solli 'ala Muhammad”", "Tasyahhud + selawat Ibrahimiyyah penuh"]], "Beza tahiyat awal dan akhir")),
        ],
        faq=[("Apakah rukun dalam tahiyat akhir?", "Duduk, membaca tasyahhud dan membaca selawat ke atas Nabi SAW. Selawat ke atas keluarga Nabi dan selawat Ibrahimiyyah penuh adalah sunat."),
             ("Bilakah jari telunjuk diangkat?", "Ketika menyebut “illallah” dalam syahadah, dan dibiarkan terangkat hingga salam menurut mazhab Syafi'i."),
             ("Apa dibaca selepas tahiyat akhir sebelum salam?", "Sunat berdoa, contohnya memohon perlindungan daripada azab kubur, azab neraka, fitnah hidup dan mati, dan fitnah Dajjal (HR Al-Bukhari 1377).")],
        about=["Tahiyat akhir", "Tasyahhud", "Cara solat"],
        llms="Tahiyat akhir dan awal (tasyahhud HR Muslim 403; selawat HR Al-Bukhari 3370): teks Arab, Rumi, maksud; rukun vs sunat ab'adh; tawarruk vs iftirasy.")),
    ("doa-selepas-solat/", dict(
        zk=True,
        h1="Zikir & Doa Selepas Solat Fardu: Bacaan Lengkap dengan Rujukan",
        title="Doa & Zikir Selepas Solat Fardu: Rumi, Arab & Bilangan",
        desc="Zikir dan doa selepas solat fardu mengikut sunnah: istighfar, Allahumma antas-salam, Ayat Kursi, tasbih 33, tahmid 33, takbir 33 dan doa, dengan kaunter.",
        lead="Wirid ringkas selepas memberi salam, mengikut urutan dalam hadis sahih: teks Arab, Rumi, maksud, bilangan dan kaunter yang menanda bacaan selesai.",
        box="Selepas salam, baca <strong>istighfar 3 kali</strong>, <strong>“Allahumma antas-salam…”</strong>, <strong>Ayat Kursi</strong>, kemudian "
            "<strong>Subhanallah 33, Alhamdulillah 33, Allahu Akbar 33</strong> dan genapkan 100 dengan tahlil (HR Muslim 597), diikuti 3 Qul dan doa "
            "“Allahumma a'inni 'ala zikrik” (HR Abu Daud 1522). Selepas itu berdoalah dengan apa-apa hajat.",
        sections=[("wirid", None, None)],
        faq=[("Apakah doa selepas solat yang paling ringkas?", "Istighfar 3 kali dan “Allahumma antas-salam wa minkas-salam, tabarakta ya zal-jalali wal-ikram” (HR Muslim 591), kemudian tasbih, tahmid dan takbir 33 kali."),
             ("Adakah wajib berwirid selepas solat?", "Tidak wajib, tetapi sangat digalakkan kerana ia amalan Nabi SAW. Tasbih 33 kali diikuti penutup 100 menghapuskan dosa walaupun sebanyak buih di lautan (HR Muslim 597)."),
             ("Bolehkah berdoa dalam Bahasa Melayu selepas solat?", "Boleh. Selepas wirid, berdoalah dengan apa-apa bahasa yang difahami. Mulakan dengan pujian kepada Allah dan selawat, kemudian hajat anda.")],
        about=["Doa selepas solat", "Zikir", "Wirid"],
        llms="Zikir dan doa selepas solat fardu: istighfar 3 (HR Muslim 591), Allahumma antas-salam, La mani'a (HR Al-Bukhari 844), Ayat Kursi, tasbih/tahmid/takbir 33 + tahlil (HR Muslim 597), 3 Qul, Allahumma a'inni (HR Abu Daud 1522).")),
    ("doa-sebelum-tidur/", dict(
        zk=True,
        h1="Doa Sebelum Tidur & Bangun Tidur: Rumi, Arab dan Amalan",
        title="Doa Sebelum Tidur & Bangun Tidur: Rumi, Arab dan Maksud",
        desc="Doa sebelum tidur dan bangun tidur dalam tulisan Arab, Rumi dan maksud, serta amalan Nabi SAW sebelum tidur: Ayat Kursi, Amanar Rasul, 3 Qul dan tasbih.",
        lead="Doa sebelum tidur dan bangun tidur daripada hadis sahih, serta amalan Rasulullah SAW sebelum tidur dengan kaunter.",
        box="Doa sebelum tidur: <strong>“Bismikallahumma amutu wa ahya”</strong> (HR Al-Bukhari 6324). Doa bangun tidur: <strong>“Alhamdulillahil-lazi ahyana ba'da ma amatana wa ilaihin-nusyur”</strong> "
            "(HR Al-Bukhari 6312). Sebelum tidur juga sunat membaca <a href=\"/ayat-kursi/\">Ayat Kursi</a>, <a href=\"/amanar-rasul/\">Amanar Rasul</a>, 3 Qul dan tasbih 33·33·34.",
        sections=[("doa", "Doa Sebelum Tidur dan Bangun Tidur", h_item("sebelum-tidur") + h_item("bangun-tidur")), ("amalan", None, None)],
        faq=[("Apakah doa sebelum tidur yang ringkas?", "“Bismikallahumma amutu wa ahya” (Dengan nama-Mu ya Allah, aku mati dan aku hidup), HR Al-Bukhari 6324."),
             ("Apakah amalan sebelum tidur menurut sunnah?", "Berwuduk, berbaring di sisi kanan, membaca Ayat Kursi (HR Al-Bukhari 2311), dua ayat terakhir Al-Baqarah (HR Al-Bukhari 5009), 3 Qul sambil meniup ke tapak tangan dan menyapu badan (HR Al-Bukhari 5017), dan tasbih 33, tahmid 33, takbir 34 (HR Al-Bukhari 6318)."),
             ("Apakah doa bangun tidur?", "“Alhamdulillahil-lazi ahyana ba'da ma amatana wa ilaihin-nusyur” (HR Al-Bukhari 6312).")],
        about=["Doa sebelum tidur", "Doa bangun tidur", "Zikir"],
        llms="Doa sebelum tidur (HR Al-Bukhari 6324), bangun tidur (HR Al-Bukhari 6312), amalan sebelum tidur: Ayat Kursi, Amanar Rasul, 3 Qul, tasbih 33/33/34.")),
    ("doa-makan/", dict(
        h1="Doa Makan: Doa Sebelum dan Selepas Makan (Rumi, Arab & Maksud)",
        title="Doa Makan: Sebelum & Selepas Makan (Rumi, Arab dan Maksud)",
        desc="Doa sebelum makan dan doa selepas makan daripada hadis sahih dalam tulisan Arab, Rumi dan maksud, doa jika terlupa bismillah, dan adab makan.",
        lead="Doa sebelum makan, doa jika terlupa membaca bismillah dan doa selepas makan, dengan rujukan hadis dan adab makan.",
        box="Sebelum makan, baca <strong>“Bismillah”</strong>; jika terlupa, baca <strong>“Bismillahi awwalahu wa akhirah”</strong> (HR Abu Daud 3767; At-Tirmizi 1858). "
            "Selepas makan, baca <strong>“Alhamdulillahil-lazi at'amani haza wa razaqanihi min ghairi haulin minni wa la quwwah”</strong>: dosanya yang lalu diampunkan (HR Abu Daud 4023; At-Tirmizi 3458).",
        sections=[
            ("doa", "Bacaan Doa Makan", h_item("sebelum-makan") + h_item("selepas-makan")),
            ("adab", "Adab Makan Mengikut Sunnah", "<ul>"
             "<li>Membaca bismillah, makan dengan tangan kanan dan mengambil makanan yang paling dekat. <span class=\"nref\">(HR Al-Bukhari 5376)</span></li>"
             "<li>Tidak mencela makanan: jika suka dimakan, jika tidak ditinggalkan. <span class=\"nref\">(HR Al-Bukhari 5409)</span></li>"
             "<li>Memuji Allah selepas makan dan minum. <span class=\"nref\">(HR Muslim 2734)</span></li></ul>"
             "<p class=\"note\">Lafaz yang popular di Malaysia, “Allahumma barik lana fima razaqtana wa qina 'azaban-nar”, tidak terdapat dalam hadis sahih; sanad bahagian pertamanya dinilai lemah dan tambahan “wa qina 'azaban-nar” tidak ditemui dalam riwayat makan. "
             "Ia boleh dibaca sebagai doa umum kerana maknanya baik, tetapi doa dalam halaman ini yang thabit daripada Nabi SAW.</p>"),
        ],
        faq=[("Apakah doa sebelum makan yang sahih?", "“Bismillah” (Dengan nama Allah). Jika terlupa di awal, baca “Bismillahi awwalahu wa akhirah” apabila teringat (HR Abu Daud 3767; At-Tirmizi 1858)."),
             ("Apakah doa selepas makan?", "“Alhamdulillahil-lazi at'amani haza wa razaqanihi min ghairi haulin minni wa la quwwah” (HR Abu Daud 4023; At-Tirmizi 3458)."),
             ("Adakah “Allahumma barik lana fima razaqtana” doa makan yang sahih?", "Ia tidak thabit dengan sanad yang sahih sebagai doa makan, dan tambahan “wa qina 'azaban-nar” tiada dalam riwayat tersebut. Ia boleh dibaca sebagai doa umum, tetapi lebih utama membaca lafaz yang sahih.")],
        about=["Doa makan", "Adab makan"],
        llms="Doa sebelum makan: Bismillah; terlupa: Bismillahi awwalahu wa akhirah (HR Abu Daud 3767). Selepas makan: Alhamdulillahil-lazi at'amani haza (HR Abu Daud 4023). Nota status lafaz 'Allahumma barik lana fima razaqtana'.")),
    ("doa-masuk-tandas/", dict(
        h1="Doa Masuk Tandas dan Keluar Tandas: Rumi, Arab & Maksud",
        title="Doa Masuk Tandas & Keluar Tandas: Rumi, Arab dan Maksud",
        desc="Doa masuk tandas dan doa keluar tandas daripada hadis sahih dalam tulisan Arab, Rumi dan maksud, serta adab masuk dan keluar tandas.",
        lead="Doa ketika masuk dan keluar tandas daripada hadis sahih, dengan adab ringkas.",
        box="Sebelum masuk tandas, baca <strong>“Allahumma inni a'uzu bika minal-khubusi wal-khaba'is”</strong> (HR Al-Bukhari 142; Muslim 375). "
            "Selepas keluar, baca <strong>“Ghufranak”</strong> (HR Abu Daud 30; At-Tirmizi 7). Masuk dengan kaki kiri dan keluar dengan kaki kanan.",
        sections=[
            ("doa", "Bacaan Doa Tandas", h_item("masuk-tandas") + h_item("keluar-tandas")),
            ("adab", "Adab Masuk dan Keluar Tandas", "<ul>"
             "<li>Baca doa <strong>sebelum</strong> masuk; jangan berzikir dengan lisan di dalam tandas.</li>"
             "<li>Masuk dengan kaki kiri, keluar dengan kaki kanan.</li>"
             "<li>Tidak membawa masuk barang bertulis nama Allah atau ayat Al-Quran kecuali jika bimbang hilang (dan disimpan tersembunyi).</li>"
             "<li>Ketika buang air di kawasan terbuka, tidak menghadap atau membelakangi kiblat.</li></ul>"),
        ],
        faq=[("Bilakah doa masuk tandas dibaca?", "Sebelum melangkah masuk, bukan di dalam tandas. Jika di kawasan terbuka, ketika hendak menyingsing pakaian."),
             ("Apakah maksud “khubus” dan “khaba'is”?", "Syaitan lelaki dan syaitan perempuan; ada juga ulama yang menafsirkannya sebagai segala kekotoran dan keburukan."),
             ("Apakah maksud “Ghufranak”?", "“(Aku memohon) keampunan-Mu.” Ia dibaca sejurus keluar dari tandas.")],
        about=["Doa masuk tandas", "Adab"],
        llms="Doa masuk tandas: Allahumma inni a'uzu bika minal-khubusi wal-khaba'is (HR Al-Bukhari 142; Muslim 375); keluar: Ghufranak (HR Abu Daud 30).")),
]


def build_pages16(ctx):
    import pages18  # the second batch of doa pages; both batches list each other under "Doa lain"
    return build_doa(PAGES, ctx, PUB, PAGES + pages18.PAGES)


def build_doa(pages, ctx, pub, related):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    out = []
    names = {p: d["title"].split(":")[0] for p, d in related}
    for path, d in pages:
        url = SITE + path
        secs = []
        for sid, h, html in d["sections"]:
            if sid == "wirid":
                secs.append(zsec("wirid", "Wirid Selepas Solat (Mengikut Urutan)", z_items(I.Z_SOLAT), len(I.Z_SOLAT),
                                 "Tekan butang bilangan untuk mengira; kiraan disimpan dalam pelayar anda dan bermula semula setiap hari. "
                                 "Untuk tasbih 33·33·33 dengan butang besar, guna <a href=\"/tasbih-digital/\">Tasbih Digital</a>."))
            elif sid == "amalan":
                secs.append(zsec("amalan", "Amalan Sebelum Tidur (Sunnah)", z_items(TIDUR), len(TIDUR),
                                 "Amalan Rasulullah SAW sebelum tidur, termasuk tasbih Fatimah (33·33·34). Kiraan bermula semula setiap hari."))
            else:
                note = (f'<p class="note">{e(RM.credit())}</p>' if sid == "bacaan" and path in ("ayat-kursi/", "amanar-rasul/") and RM.live(2) else "")
                secs.append(f'<section class="dsec" id="{sid}" aria-labelledby="h-{sid}"><h2 id="h-{sid}">{h}</h2>{html}{note}</section>')
            if len(secs) == 1:
                secs.append(ad(0))
        toc = [(sid, h or ("Wirid" if sid == "wirid" else "Amalan")) for sid, h, _ in d["sections"]] + [("faq", "Soalan lazim"), ("lain", "Doa lain")]
        others = "".join(f'<li><a href="/{p}">{e(names[p])}</a></li>' for p, _ in related if p != path)
        crumb_hub = ("Doa Harian", "doa-harian/")
        body = hero(e(d["h1"]), e(d["lead"]), [crumb_hub, (names[path], None)])
        body += f'''<div class="wrap mn"><div class="ct{" zk" if d.get("zk") else ""}">
<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {d["box"]}</p></div>
{meta_line(T, TMS)}
{share(url, d["title"].split(":")[0] + ":")}
</div>
</section>
{"".join(secs)}
<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim</h2>
{faq_html(d["faq"])}
</section>

<section id="lain" aria-labelledby="h-lain">
<h2 id="h-lain">Doa dan Bacaan Lain</h2>
<ul class="rel sts">{others}</ul>
<p class="note"><a href="/doa-harian/">Semua doa harian</a> · <a href="/zikir-pagi-petang/">Zikir pagi & petang</a> · <a href="/belajar-solat/">Cara solat lengkap</a> · <a href="/surah-yasin/">Surah Yasin</a></p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(None)}</section>
</div>
{side(toc, None)}
</div>'''
        assert len(d["title"]) <= 70 and len(d["desc"]) <= 160, (path, len(d["title"]), len(d["desc"]))
        out.append(dict(path=path, kind="tool", data=False, arabic=True, published=d.get("published", pub), nocache=True, noindex=d.get("noindex", False),
                        title=d["title"], ogtitle=d["title"].split(":")[0], desc=d["desc"], crumbs=[crumb_hub, (names[path], None)],
                        body=body, faq=d["faq"], about=d["about"], ogcard=(d["title"].split(":")[0], "Teks Arab, Rumi & maksud, dengan rujukan hadis"),
                        llms=d["llms"]))
    return out
