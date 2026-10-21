"""Pages: /solat-sunat/ (hub: today's sunat windows and forbidden times for a zone, rawatib) and one page per sunat prayer
(/solat-sunat/<slug>/), each with the step player of /belajar-solat/ (same JSON shape, same alat.js engine), niat, doa,
and where it applies a time card computed from the JAKIM timetable (dhuha window, last third of the night, witir window).
The time cards are pre-rendered for the build day and redrawn by alat.js (swCard mirrors sw_card)."""
import json, datetime as dt
import ibadah2 as I2
import sunat as S
import tahlil as T
import solat as SL
import ramadan as R
import plans as P
from pages import e, faq_html, hero, side, meta_line, tool_cards, table, SITE
from pages2 import quran_block, qref, card
from pages3 import areas
from pages4 import sp_card, sp_list

HUB = S.HUB
DEF_ZONE = "WLY01"


def url_of(key):
    return HUB + next(p[1] for p in S.PRAYERS if p[0] == key) + "/"


# ---------------- step player data (same contract as pages4.solat_data) ----------------
def player_data(variants, key):
    """variants: [(wkey, label, rakaat, niat (ar, ru, mn), steps, unit)] -> the JSON the alat.js step player reads."""
    used = {sid for v in variants for sid, _ in v[4]}
    b = {}
    for k in used:
        title, how, ar, ru, mn, src = S.BACAAN.get(k) or I2.BACAAN[k]
        if isinstance(ar, tuple):
            _, sn, a1, a2 = ar
            ar, ru, mn = quran_block([(sn, a) for a in range(a1, a2 + 1)])
            b[k] = [e(title), e(how), ar, ru, mn, f"{e(src)} · {qref(sn, a1)}"]
        else:
            b[k] = [e(title), e(how), e(ar), e(ru), e(mn), e(src)]
    w = {}
    for wk, label, rk, niat, st, unit in variants:
        w[wk] = {"n": label, "r": rk, "niat": [e(x) for x in niat]}
        if unit != "Rakaat":
            w[wk]["u"] = unit
    return {"b": b, "w": w, "s": {v[0]: v[4] for v in variants}, "def": variants[0][0], "key": "sunat-" + key}


def player_html(D, title):
    w = D["def"]
    chips = "".join(f'<button type="button" data-w="{k}" aria-pressed="{"true" if k == w else "false"}">{e(v["n"])}</button>' for k, v in D["w"].items())
    return f'''<h2 id="h-pan">{title}</h2>
<div class="chips2" id="spw" role="group" aria-label="Pilih bentuk solat"{"" if len(D["w"]) > 1 else " hidden"}>{chips}</div>
<div class="act"><button class="btn2" type="button" id="sprm" aria-pressed="true">Rumi</button><button class="btn2" type="button" id="spmn" aria-pressed="true">Maksud</button><button class="btn2" type="button" data-act="link">🔗 Salin pautan</button></div>
<div class="spc" id="spc" aria-live="polite">{sp_card(D, w, 0)}</div>
<div class="spnav"><button class="btn2" type="button" id="spprev" disabled>‹ Sebelum</button><progress id="spp" max="{len(D["s"][w])}" value="1"></progress><button class="btn3" type="button" id="spnext">Seterusnya ›</button></div>
<details class="spx"><summary>Senarai semua langkah</summary><ol class="spl" id="spl">{sp_list(D, w, 0)}</ol></details>'''


# ---------------- time cards (alat.js swCard mirrors this) ----------------
def hmx(x):
    return SL.hm(x % 1440)


def dur(m):
    return f"{m // 60} jam {m % 60} minit"


def sw_card(kind, t, tn, zone, day):
    """t, tn: today's and tomorrow's [imsak, subuh, syuruk, zohor, asar, maghrib, isyak] in minutes."""
    rows = []
    if kind in ("dhuha", "hub"):
        rows += [("Dhuha bermula", hmx(t[2] + 20), f"kira-kira 20 minit selepas syuruk ({hmx(t[2])}), apabila matahari naik setinggi tombak"),
                 ("Dhuha paling afdal", hmx(t[2] + (t[5] - t[2]) // 4), "suku siang, ketika panas mula terasa"),
                 ("Dhuha berakhir", hmx(t[3]), "sebelum masuk Zohor; elakkan beberapa minit sebelumnya (istiwa')")]
    if kind in ("tahajjud", "witir", "hub"):
        night = tn[1] + 1440 - t[5]
        last = tn[1] + 1440 - night // 3
        if kind == "witir":
            rows.append(("Witir bermula", hmx(t[6]), "selepas solat Isyak"))
        if kind == "tahajjud":
            rows += [("Malam bermula", hmx(t[5]), "Maghrib"), ("Separuh malam", hmx(t[5] + night // 2), f"malam ini {dur(night)}")]
        rows.append(("Sepertiga malam terakhir", hmx(last), "waktu paling afdal untuk tahajjud, doa dan witir"))
        rows.append(("Berakhir", hmx(tn[1]), "masuk waktu Subuh esok"))
    if kind == "jamak":
        rows += [("Jamak taqdim Zohor + Asar", f"{hmx(t[3])}–{hmx(t[4])}", "kedua-duanya dalam waktu Zohor"),
                 ("Jamak takhir Zohor + Asar", f"{hmx(t[4])}–{hmx(t[5])}", "dalam waktu Asar; niat takhir dibuat semasa waktu Zohor"),
                 ("Jamak taqdim Maghrib + Isyak", f"{hmx(t[5])}–{hmx(t[6])}", "kedua-duanya dalam waktu Maghrib"),
                 ("Jamak takhir Maghrib + Isyak", f"{hmx(t[6])}–{hmx(tn[1])}", "dalam waktu Isyak hingga sebelum Subuh esok"),
                 ("Subuh", hmx(t[1]), "tidak boleh dijamak atau diqasar")]
    if kind == "hub":
        rows += [("Dilarang: selepas Subuh", f"{hmx(t[1])}–{hmx(t[2] + 20)}", "selepas solat Subuh hingga matahari naik"),
                 ("Dilarang: istiwa'", f"sebelum {hmx(t[3])}", "beberapa minit sebelum Zohor, ketika matahari tegak"),
                 ("Dilarang: selepas Asar", f"{hmx(t[4])}–{hmx(t[5])}", "selepas solat Asar hingga matahari terbenam")]
    li = "".join(f'<li><span class="swl">{a}</span><strong>{b}</strong><em>{c}</em></li>' for a, b, c in rows)
    return f'<p class="swh">{P.dlong(day)} · zon {zone}</p><ul class="swr">{li}</ul>'


def sw_html(kind, day, AREA):
    t, off = R.day_times(DEF_ZONE, day)
    tn, _ = R.day_times(DEF_ZONE, day + dt.timedelta(1))
    opts = "".join(f'<option value="{z[0]}"{" selected" if z[0] == DEF_ZONE else ""}>{z[0]} · {e(AREA[z[0]][:48])}</option>' for z in SL.ZONES)
    title = {"dhuha": "Waktu Solat Dhuha Hari Ini", "tahajjud": "Sepertiga Malam Terakhir Malam Ini", "witir": "Waktu Solat Witir Malam Ini",
             "hub": "Waktu Solat Sunat & Waktu Dilarang Hari Ini"}[kind]
    return (f'<div class="sw2" id="sw2" data-k="{kind}"><h3 id="h-sw">🕰 {title}</h3><div class="fl"><label for="swz">Zon waktu solat</label><select id="swz">{opts}</select></div>'
            f'<div id="swo" aria-live="polite">{sw_card(kind, t, tn, DEF_ZONE, day)}</div>'
            f'<p class="note">Dikira daripada jadual rasmi JAKIM (e-solat.gov.my) bagi zon yang dipilih. Minit tambahan ialah anggaran berhati-hati, bukan waktu rasmi.</p></div>')


def doa_cards(items):
    out = []
    for id_, title, ar, ru, mn, src, note in items:
        if ar.startswith("Q:"):
            s, a = ar[2:].split(":")
            a1, a2 = (map(int, a.split("-")) if "-" in a else (int(a), int(a)))
            ar_, ru_, mn_ = quran_block([(int(s), x) for x in range(a1, a2 + 1)])
            src_ = (e(src) + " · " if src else "") + qref(int(s), a1)
        else:
            ar_, ru_, mn_, src_ = e(ar), e(ru), e(mn), e(src)
        mn_ = mn_.replace(e("[HAJAT]"), '<mark class="hjv">(urusan ini)</mark>')
        out.append(card(id_, title, ar_, ru_, mn_, src_, extra=note))
    return "".join(out)


def niat_card(niat, label):
    return card("niat-" + label.lower().replace(" ", "-"), f"Lafaz Niat {label}", e(niat[0]), e(niat[1]), e(niat[2]), "Niat di dalam hati ketika takbiratul ihram; melafazkannya sunat (mazhab Syafi'i)")


def plinks(skip):
    return '<ul class="rel sts">' + "".join(f'<li><a href="/{HUB}{s}/">{e(n)}</a></li>' for k, s, n, _ in S.PRAYERS if k != skip) + "</ul>"


# ---------------- per-prayer content ----------------
NIAT = {
    "dhuha": S.niat("سُنَّةَ الضُّحَى", "sunnatad-dhuha", "sunat Dhuha"),
    "taubat": S.niat("سُنَّةَ التَّوْبَةِ", "sunnatat-taubati", "sunat Taubat"),
    "hajat": S.niat("سُنَّةَ الْحَاجَةِ", "sunnatal-hajati", "sunat Hajat"),
    "istikharah": S.niat("سُنَّةَ الْاِسْتِخَارَةِ", "sunnatal-istikharati", "sunat Istikharah"),
    "tahajjud": S.niat("سُنَّةَ التَّهَجُّدِ", "sunnatat-tahajjudi", "sunat Tahajjud"),
    "witir2": S.niat("سُنَّةً مِنَ الْوِتْرِ", "sunnatan minal-witri", "sunat sebahagian daripada Witir"),
    "witir1": S.niat("سُنَّةَ الْوِتْرِ", "sunnatal-witri", "sunat Witir", "رَكْعَةً", "rak'atan", "satu rakaat"),
    "tarawih": S.niat("سُنَّةَ التَّرَاوِيحِ", "sunnatat-tarawihi", "sunat Tarawih", extra_ar="مَأْمُومًا", extra_ru="makmuman", extra_ms="sebagai makmum"),
}
KC = ["s-kafirun", "s-ikhlas"]
CONTENT = {
    "taubat": dict(
        variants=[("taubat", "2 rakaat", 2, NIAT["taubat"], S.steps(KC), "Rakaat")],
        title="Solat Taubat: Cara, Niat, Doa & Waktu (Panduan Lengkap)",
        desc="Cara solat sunat taubat 2 rakaat langkah demi langkah: niat, bacaan Arab-Rumi-maksud, Sayyidul Istighfar, syarat taubat dan dalil hadis sahih.",
        lead="Solat sunat dua rakaat untuk memohon keampunan selepas melakukan dosa, diikuti istighfar yang bersungguh-sungguh.",
        answer="Solat taubat ialah <strong>solat sunat 2 rakaat</strong> yang dikerjakan selepas melakukan dosa. Selepas salam, <strong>beristighfar</strong> (afdalnya Sayyidul Istighfar) dengan memenuhi syarat taubat: berhenti daripada dosa, menyesal, berazam tidak mengulanginya dan memulangkan hak orang lain jika ada. Ia boleh dilakukan pada bila-bila masa kecuali waktu yang dilarang.",
        info=[("Bilangan rakaat", "2 rakaat, satu salam"), ("Waktu", "Bila-bila masa selepas berdosa, kecuali waktu dilarang solat"), ("Hukum", "Sunat"),
              ("Surah", "Bebas; contoh Al-Kafirun dan Al-Ikhlas")],
        dalil=["Rasulullah SAW bersabda: “Tiada seorang pun yang melakukan dosa, kemudian dia bangun, bersuci, lalu solat (dua rakaat), kemudian memohon ampun kepada Allah, melainkan Allah mengampunkannya”, kemudian baginda membaca Ali 'Imran 135 (HR Abu Daud, no. 1521; At-Tirmizi, no. 406, hasan).",
               "Syarat taubat diterima: meninggalkan dosa, menyesalinya, berazam tidak mengulanginya, dan jika melibatkan hak manusia, memulangkan hak itu atau meminta halal (disepakati ulama; rujuk Riyadhus Salihin, Bab Taubat)."],
        doa=[S.DOA_TAUBAT, S.AYAT_TAUBAT], extra="taubat",
        faq=[("Bilakah waktu solat taubat?", "Sebaik-baiknya segera selepas menyedari dosa, pada bila-bila masa siang atau malam, kecuali tiga waktu yang dilarang solat: selepas solat Subuh hingga matahari naik, ketika istiwa' dan selepas solat Asar hingga terbenam."),
             ("Berapa rakaat solat taubat?", "Dua rakaat dengan satu salam, sama seperti solat sunat dua rakaat yang lain. Selepas salam, perbanyakkan istighfar dan berdoa."),
             ("Adakah dosa besar diampunkan dengan solat taubat?", "Taubat nasuha menghapuskan dosa sebesar mana pun selagi syaratnya dipenuhi dan dilakukan sebelum nyawa sampai ke halkum (Az-Zumar 39:53). Dosa yang melibatkan hak manusia memerlukan hak itu dipulangkan atau dimaafkan."),
             ("Bolehkah solat taubat dibuat pada malam hari?", "Boleh, dan malam ialah waktu yang sangat baik, terutama sepertiga malam terakhir ketika Allah menerima istighfar hamba-Nya (HR Al-Bukhari, no. 1145).")]),
    "dhuha": dict(
        variants=[("dhuha", "2 rakaat", 2, NIAT["dhuha"], S.steps(["s-syams", "s-dhuha"]), "Rakaat")],
        title="Solat Dhuha: Waktu Hari Ini, Cara, Niat & Doa (Rasmi JAKIM)",
        desc="Waktu solat dhuha hari ini ikut zon JAKIM, cara solat dhuha 2–8 rakaat langkah demi langkah, niat, doa dhuha dan fadhilat daripada hadis sahih.",
        lead="Waktu dhuha hari ini bagi zon anda, cara solat langkah demi langkah, niat dan doa selepas solat dhuha.",
        answer="Waktu solat dhuha bermula <strong>kira-kira 20 minit selepas syuruk</strong> dan berakhir <strong>sebelum masuk waktu Zohor</strong>; waktu paling afdal ialah ketika matahari mula panas (suku siang). Solat dhuha dikerjakan <strong>sekurang-kurangnya 2 rakaat</strong> dan sebaik-baiknya 8 rakaat, dua rakaat satu salam.",
        info=[("Bilangan rakaat", "Sekurang-kurangnya 2; afdal 8 (sebahagian ulama Syafi'i hingga 12), setiap 2 rakaat satu salam"),
              ("Waktu", "Matahari naik setinggi tombak (≈20 minit selepas syuruk) hingga sebelum Zohor"), ("Hukum", "Sunat muakkad menurut mazhab Syafi'i"),
              ("Surah", "Amalan biasa: Asy-Syams dan Ad-Dhuha; surah lain juga sah")],
        dalil=["Setiap sendi manusia perlu bersedekah setiap pagi, dan semuanya dicukupi dengan dua rakaat dhuha (HR Muslim, no. 720).",
               "Wasiat Rasulullah SAW kepada Abu Hurairah: puasa tiga hari setiap bulan, dua rakaat dhuha dan witir sebelum tidur (HR Al-Bukhari, no. 1178; Muslim, no. 721).",
               "Solat awwabin (dhuha) ialah ketika anak unta merasa panas pasir (HR Muslim, no. 748): inilah waktu afdal, kira-kira suku siang.",
               "Ummu Hani' melihat Rasulullah SAW solat dhuha 8 rakaat pada hari pembukaan Mekah (HR Al-Bukhari, no. 1176)."],
        doa=[S.DOA_DHUHA], widget="dhuha", modified=True,
        faq=[("Pukul berapa waktu solat dhuha?", "Dhuha bermula kira-kira 20 minit selepas syuruk dan berakhir sebelum Zohor. Kad di atas mengiranya bagi zon JAKIM anda untuk hari ini; di Kuala Lumpur biasanya sekitar 7:20 pagi hingga 1:00 tengah hari."),
             ("Berapa rakaat solat dhuha?", "Sekurang-kurangnya 2 rakaat. Rasulullah SAW pernah solat dhuha 4 dan 8 rakaat; dalam mazhab Syafi'i, 8 rakaat paling afdal dan sebahagian ulama menyebut hingga 12. Setiap dua rakaat dengan satu salam."),
             ("Apakah surah yang dibaca dalam solat dhuha?", "Tiada surah khusus yang wajib. Amalan biasa di Malaysia ialah Asy-Syams pada rakaat pertama dan Ad-Dhuha pada rakaat kedua; Al-Kafirun dan Al-Ikhlas atau mana-mana surah juga sah."),
             ("Bolehkah solat dhuha selepas pukul 12 tengah hari?", "Boleh, selagi belum masuk waktu Zohor, tetapi elakkan beberapa minit sebelum Zohor (waktu istiwa') kerana solat ketika itu dilarang."),
             ("Adakah doa dhuha daripada hadis?", "Doa “Allahumma innad-dhuha'a dhuha'uk” ialah doa amalan ulama, bukan hadis Nabi SAW. Ia boleh dibaca, dan anda juga boleh berdoa dengan bahasa sendiri.")]),
    "hajat": dict(
        variants=[("hajat", "2 rakaat", 2, NIAT["hajat"], S.steps(KC), "Rakaat")],
        title="Solat Hajat: Cara, Niat, Doa Hajat & Bilangan Rakaat",
        desc="Cara solat hajat 2 rakaat langkah demi langkah: niat, bacaan Arab-Rumi-maksud dan doa hajat lengkap. Tulis hajat anda dan ia dimasukkan ke dalam maksud doa.",
        lead="Solat sunat ketika berhajat kepada Allah: langkah demi langkah, niat dan doa hajat yang boleh dimasukkan hajat anda sendiri.",
        answer="Solat hajat ialah <strong>solat sunat 2 rakaat</strong> (boleh hingga 12, dua rakaat satu salam) yang dikerjakan ketika mempunyai hajat. Selepas salam, <strong>bertahmid dan berselawat</strong>, kemudian membaca <strong>doa hajat</strong> dan menyebut hajat anda. Ia boleh dilakukan pada bila-bila masa kecuali waktu dilarang; afdalnya pada sepertiga malam terakhir.",
        info=[("Bilangan rakaat", "2 rakaat (boleh hingga 12, setiap 2 rakaat satu salam)"), ("Waktu", "Bila-bila masa kecuali waktu dilarang; afdal sepertiga malam terakhir"),
              ("Hukum", "Sunat"), ("Surah", "Bebas; contoh Al-Kafirun dan Al-Ikhlas")],
        dalil=["Hadis solat hajat (HR At-Tirmizi, no. 479; Ibn Majah, no. 1384) diriwayatkan dengan sanad yang dinilai dhaif oleh At-Tirmizi sendiri. Ramai ulama membenarkan beramal dengannya kerana ia termasuk fadhail amal dan bertepatan dengan dalil umum solat dan doa.",
               "Dalil umum: “Mohonlah pertolongan dengan sabar dan solat” (Al-Baqarah 2:45), dan doa pada sepertiga malam terakhir dimakbulkan (HR Al-Bukhari, no. 1145)."],
        doa=[S.DOA_HAJAT], extra="hajat",
        faq=[("Berapa rakaat solat hajat?", "Sekurang-kurangnya 2 rakaat. Sebahagian ulama menyebut hingga 12 rakaat, setiap dua rakaat dengan satu salam."),
             ("Bilakah waktu terbaik solat hajat?", "Pada bila-bila masa kecuali waktu dilarang solat. Waktu paling mustajab ialah sepertiga malam terakhir; lihat kiraannya di halaman Solat Tahajjud."),
             ("Adakah hadis solat hajat sahih?", "Hadis khusus solat hajat (At-Tirmizi, no. 479) dhaif menurut At-Tirmizi. Namun ramai ulama mengharuskan amalan ini kerana ia fadhail amal dan disokong dalil umum tentang solat dan doa."),
             ("Bolehkah solat hajat berjemaah?", "Boleh. Solat hajat berjemaah sering diadakan di masjid dan sekolah, contohnya sebelum peperiksaan; imam membaca doa dan makmum mengaminkan.")]),
    "jenazah": dict(
        variants=[("jenazah", "4 takbir", 4, S.JENAZAH["l"]["niat"], S.JENAZAH_STEPS, "Takbir")],
        title="Solat Jenazah: Cara, Niat & Doa (Lelaki, Perempuan, Ramai)",
        desc="Cara solat jenazah 4 takbir langkah demi langkah dengan niat dan doa yang bertukar ikut jenazah lelaki, perempuan atau ramai. Bacaan Arab, Rumi dan maksud.",
        lead="Empat takbir dalam keadaan berdiri: niat dan doa yang bertukar automatik mengikut jenazah lelaki, perempuan atau ramai.",
        answer="Solat jenazah ialah <strong>fardu kifayah</strong> dengan <strong>4 takbir</strong> dalam keadaan berdiri, tanpa rukuk dan sujud: <strong>takbir 1</strong> baca Al-Fatihah, <strong>takbir 2</strong> selawat, <strong>takbir 3</strong> doa untuk jenazah (“Allahummaghfir lahu…”, “laha” bagi perempuan), <strong>takbir 4</strong> doa “Allahumma la tahrimna ajrahu…”, kemudian salam.",
        info=[("Bilangan takbir", "4 takbir, berdiri, tanpa rukuk dan sujud"), ("Hukum", "Fardu kifayah"), ("Rukun", "Niat, berdiri, 4 takbir, Al-Fatihah, selawat, doa untuk jenazah, salam"),
              ("Kedudukan imam", "Setentang kepala jenazah lelaki; setentang punggung jenazah perempuan")],
        dalil=["Sesiapa menyaksikan jenazah sehingga disolatkan mendapat satu qirat, dan sehingga dikebumikan mendapat dua qirat; satu qirat seperti dua gunung besar (HR Al-Bukhari, no. 1325; Muslim, no. 945).",
               "Rasulullah SAW menyolatkan An-Najasyi dengan empat takbir (HR Al-Bukhari, no. 1333).",
               "Doa takbir ketiga diajar oleh Rasulullah SAW (HR Muslim, no. 963)."],
        doa=[], extra="jenazah",
        faq=[("Apakah bacaan selepas setiap takbir solat jenazah?", "Takbir pertama: Al-Fatihah. Takbir kedua: selawat ke atas Nabi. Takbir ketiga: doa untuk jenazah. Takbir keempat: doa “Allahumma la tahrimna ajrahu wa la taftinna ba'dahu waghfir lana wa lahu”, kemudian salam."),
             ("Apakah beza doa solat jenazah lelaki dan perempuan?", "Kata ganti berubah: “lahu, warhamhu, 'anhu” bagi lelaki; “laha, warhamha, 'anha” bagi perempuan; “lahum” bagi ramai. Pilih jenazah di atas dan semua bacaan bertukar."),
             ("Adakah solat jenazah perlu rukuk dan sujud?", "Tidak. Solat jenazah dikerjakan sepenuhnya dalam keadaan berdiri dengan empat takbir dan diakhiri salam."),
             ("Bolehkah solat jenazah ghaib?", "Boleh menurut mazhab Syafi'i bagi jenazah yang berada di tempat lain, berdasarkan solat Rasulullah SAW ke atas An-Najasyi (HR Al-Bukhari, no. 1333). Niatnya: “Usolli 'alal-mayyitil-gha'ib…”."),
             ("Siapakah yang paling layak menjadi imam solat jenazah?", "Dalam mazhab Syafi'i, wali terdekat (bapa, kemudian datuk, anak lelaki dan seterusnya) lebih berhak menjadi imam, kemudian imam masjid.")]),
    "witir": dict(
        variants=[("witir2", "Witir 2 rakaat (salam)", 2, NIAT["witir2"], S.steps(["s-ala", "s-kafirun2"]), "Rakaat"),
                  ("witir1", "Witir 1 rakaat", 1, NIAT["witir1"], S.steps(["s-qul3"]), "Rakaat")],
        title="Solat Witir: Waktu Malam Ini, Cara 3 Rakaat, Niat & Doa",
        desc="Waktu solat witir malam ini ikut zon JAKIM, cara witir 3 rakaat (2+1) dan 1 rakaat, niat, surah sunnah dan bacaan selepas witir. Panduan langkah demi langkah.",
        lead="Penutup solat malam: waktu witir malam ini, cara 3 rakaat (2 + 1) atau 1 rakaat, niat dan bacaan selepas witir.",
        answer="Solat witir dikerjakan <strong>selepas Isyak hingga sebelum Subuh</strong> dengan bilangan rakaat ganjil, <strong>sekurang-kurangnya 1 rakaat</strong> dan paling banyak 11. Cara biasa ialah <strong>3 rakaat: 2 rakaat salam, kemudian 1 rakaat</strong>, dengan Al-A'la, Al-Kafirun dan Al-Ikhlas (bersama Al-Falaq dan An-Nas). Selepas salam, baca “Subhanal-malikil-quddus” 3 kali.",
        info=[("Bilangan rakaat", "Ganjil: 1, 3, 5 hingga 11; biasa 3 (2 + 1)"), ("Waktu", "Selepas Isyak hingga sebelum Subuh; afdal akhir malam bagi yang yakin bangun"),
              ("Hukum", "Sunat muakkad"), ("Qunut", "Sunat pada rakaat terakhir witir separuh akhir Ramadan (mazhab Syafi'i)")],
        dalil=["“Sesungguhnya Allah itu witir (Esa) dan menyukai witir” (HR Abu Daud, no. 1416; At-Tirmizi, no. 453).",
               "“Jadikanlah witir akhir solat kamu pada waktu malam” (HR Al-Bukhari, no. 998; Muslim, no. 751).",
               "Sesiapa bimbang tidak bangun akhir malam, hendaklah berwitir awal malam; sesiapa yakin bangun, berwitirlah di akhir malam kerana ia disaksikan (HR Muslim, no. 755)."],
        doa=[S.DOA_WITIR], widget="witir", modified=True,
        faq=[("Bilakah waktu solat witir?", "Selepas solat Isyak hingga sebelum masuk Subuh. Kad di atas menunjukkan waktu malam ini bagi zon anda, termasuk sepertiga malam terakhir."),
             ("Berapa rakaat solat witir?", "Sekurang-kurangnya 1 rakaat dan paling banyak 11, dengan bilangan ganjil. Yang biasa diamalkan ialah 3 rakaat: 2 rakaat salam, kemudian 1 rakaat."),
             ("Bolehkah solat witir selepas tahajjud jika sudah witir sebelum tidur?", "Boleh solat tahajjud, tetapi jangan mengulang witir kerana “tiada dua witir dalam satu malam” (HR Abu Daud, no. 1439; At-Tirmizi, no. 470)."),
             ("Bilakah qunut witir dibaca?", "Dalam mazhab Syafi'i, qunut witir sunat dibaca pada rakaat terakhir witir mulai malam 16 Ramadan hingga akhir Ramadan, selepas iktidal.")]),
    "istikharah": dict(
        variants=[("istikharah", "2 rakaat", 2, NIAT["istikharah"], S.steps(KC), "Rakaat")],
        title="Solat Istikharah: Cara, Niat & Doa Istikharah (Hadis Sahih)",
        desc="Cara solat istikharah 2 rakaat langkah demi langkah, niat dan doa istikharah daripada Sahih Al-Bukhari. Tulis urusan anda dan ia dimasukkan ke dalam maksud doa.",
        lead="Memohon pilihan terbaik daripada Allah: langkah demi langkah, niat dan doa istikharah yang boleh dimasukkan urusan anda sendiri.",
        answer="Solat istikharah ialah <strong>solat sunat 2 rakaat</strong> untuk memohon pilihan terbaik dalam sesuatu urusan, diikuti <strong>doa istikharah</strong> daripada Sahih Al-Bukhari (no. 1162). Ketika menyebut “hazal-amra”, hadirkan urusan anda. Keputusan tidak semestinya datang melalui mimpi; teruskan dengan urusan yang dimudahkan Allah dan bermesyuarah dengan orang yang dipercayai.",
        info=[("Bilangan rakaat", "2 rakaat, satu salam"), ("Waktu", "Bila-bila masa kecuali waktu dilarang; boleh diulang beberapa kali"),
              ("Hukum", "Sunat"), ("Surah", "Disunatkan Al-Kafirun dan Al-Ikhlas (Imam An-Nawawi)")],
        dalil=["Jabir bin Abdillah: “Rasulullah SAW mengajar kami istikharah dalam semua urusan sebagaimana baginda mengajar kami surah daripada Al-Quran” (HR Al-Bukhari, no. 1162).",
               "Istikharah tidak menggantikan usaha dan musyawarah: “Bermesyuaratlah dengan mereka dalam urusan itu” (Ali 'Imran 3:159)."],
        doa=[S.DOA_ISTIKHARAH], extra="hajat",
        faq=[("Bilakah doa istikharah dibaca?", "Selepas salam daripada dua rakaat solat istikharah. Sebahagian ulama juga membenarkannya dibaca sebelum salam selepas tahiyat akhir."),
             ("Bagaimana mengetahui jawapan istikharah?", "Jawapan tidak semestinya melalui mimpi atau perasaan tertentu. Teruskan dengan pilihan yang dirasakan baik selepas berfikir dan bermesyuarah; jika ia dimudahkan, itulah tanda kebaikannya, dan jika terhalang, terimalah dengan reda."),
             ("Bolehkah solat istikharah untuk jodoh atau kerja?", "Boleh, untuk apa sahaja urusan harus yang memerlukan keputusan seperti jodoh, pekerjaan, pembelian rumah atau perjalanan. Tulis urusan anda dalam ruangan di atas untuk melihatnya dalam maksud doa."),
             ("Berapa kali boleh solat istikharah?", "Boleh diulang beberapa kali jika masih ragu-ragu; sebahagian ulama menyebut hingga tujuh kali.")]),
    "tahajjud": dict(
        variants=[("tahajjud", "2 rakaat", 2, NIAT["tahajjud"], S.steps(KC), "Rakaat")],
        title="Solat Tahajjud: Sepertiga Malam Terakhir Malam Ini, Cara & Niat",
        desc="Waktu sepertiga malam terakhir malam ini ikut zon JAKIM, cara solat tahajjud langkah demi langkah, niat, bilangan rakaat dan dalil Al-Quran serta hadis sahih.",
        lead="Bila tepatnya sepertiga malam terakhir malam ini di zon anda, dan cara solat tahajjud langkah demi langkah.",
        answer="Solat tahajjud ialah <strong>solat sunat malam selepas bangun tidur</strong>, sekurang-kurangnya <strong>2 rakaat</strong> (dua rakaat satu salam, tanpa had maksimum), dan ditutup dengan witir. Waktunya selepas Isyak hingga Subuh; <strong>paling afdal pada sepertiga malam terakhir</strong>, ketika Allah turun ke langit dunia menerima doa dan istighfar.",
        info=[("Bilangan rakaat", "Sekurang-kurangnya 2; tiada had maksimum (Rasulullah SAW biasanya 8 + witir 3)"),
              ("Waktu", "Selepas Isyak dan tidur hingga sebelum Subuh; afdal sepertiga malam terakhir"), ("Hukum", "Sunat muakkad"),
              ("Surah", "Bebas; panjangkan bacaan jika mampu")],
        dalil=["“Dan pada sebahagian malam, bertahajjudlah sebagai ibadah tambahan bagimu” (Al-Isra' 17:79).",
               "Allah turun ke langit dunia setiap malam ketika tinggal sepertiga malam terakhir dan berfirman: siapa yang berdoa, Aku perkenankan; siapa yang meminta, Aku beri; siapa yang memohon ampun, Aku ampunkan (HR Al-Bukhari, no. 1145; Muslim, no. 758).",
               "“Solat yang paling afdal selepas solat fardu ialah solat malam” (HR Muslim, no. 1163)."],
        doa=[S.AYAT_TAHAJJUD], widget="tahajjud", modified=True,
        faq=[("Bilakah sepertiga malam terakhir?", "Malam dikira dari Maghrib hingga Subuh dan dibahagi tiga; sepertiga terakhir ialah bahagian sebelum Subuh. Kad di atas mengiranya untuk malam ini bagi zon anda; di Kuala Lumpur biasanya bermula sekitar pukul 2:30 hingga 3:00 pagi."),
             ("Perlukah tidur dahulu sebelum solat tahajjud?", "Menurut kebanyakan ulama Syafi'i, tahajjud ialah solat malam selepas tidur walaupun sebentar. Solat malam tanpa tidur tetap qiyamullail dan berpahala."),
             ("Berapa rakaat solat tahajjud?", "Sekurang-kurangnya 2 rakaat, tanpa had maksimum, setiap dua rakaat satu salam. Rasulullah SAW lazimnya solat 8 rakaat kemudian witir 3 rakaat (HR Al-Bukhari, no. 1147)."),
             ("Apakah yang dibaca selepas solat tahajjud?", "Perbanyakkan istighfar, doa dan zikir kerana ia waktu mustajab, kemudian tutup dengan solat witir jika belum berwitir.")]),
    "tarawih": dict(
        variants=[("tarawih", "2 rakaat (setiap salam)", 2, NIAT["tarawih"], S.steps(KC), "Rakaat")],
        title="Solat Tarawih: Cara, Niat, 8 atau 20 Rakaat & Pengira Rakaat",
        desc="Cara solat tarawih langkah demi langkah, niat, hukum 8 atau 20 rakaat, dan pengira rakaat tarawih + witir yang menunjukkan salam ke berapa anda sekarang.",
        lead="Solat malam Ramadan: niat, cara setiap dua rakaat, persoalan 8 atau 20 rakaat, dan pengira rakaat supaya tidak terlupa bilangan.",
        answer="Solat tarawih ialah <strong>solat sunat malam Ramadan</strong> selepas Isyak, dikerjakan <strong>dua rakaat satu salam</strong>, sama ada <strong>8 atau 20 rakaat</strong>, kemudian ditutup dengan <strong>witir</strong>. Kedua-dua bilangan diamalkan: 20 rakaat ialah amalan mazhab Syafi'i sejak zaman Umar RA, dan 8 rakaat berdasarkan hadis Aisyah RA.",
        info=[("Bilangan rakaat", "8 atau 20 rakaat (dua rakaat satu salam), kemudian witir"), ("Waktu", "Malam Ramadan, selepas Isyak hingga sebelum Subuh"),
              ("Hukum", "Sunat muakkad; afdal berjemaah"), ("Niat", "Niat setiap dua rakaat")],
        dalil=["“Sesiapa berqiyam pada bulan Ramadan dengan iman dan mengharap pahala, diampunkan dosanya yang lalu” (HR Al-Bukhari, no. 37; Muslim, no. 759).",
               "Aisyah RA: Rasulullah SAW tidak menambah lebih daripada 11 rakaat pada Ramadan dan bulan lain (HR Al-Bukhari, no. 2013).",
               "Umar RA menghimpunkan orang ramai berjemaah tarawih di belakang Ubay bin Ka'ab (HR Al-Bukhari, no. 2010); 20 rakaat ialah amalan mazhab Syafi'i."],
        doa=[], extra="tarawih",
        faq=[("Berapa rakaat solat tarawih, 8 atau 20?", "Kedua-duanya diamalkan dan sah. 20 rakaat ialah pendapat mazhab Syafi'i dan majoriti ulama berdasarkan amalan zaman Umar RA; 8 rakaat berdasarkan hadis Aisyah RA. Pilih yang anda mampu dan hormati pilihan orang lain."),
             ("Apakah niat solat tarawih?", "“Usolli sunnatat-tarawihi rak'ataini makmuman lillahi ta'ala” bagi makmum; bagi imam “imaman”, dan jika seorang diri gugurkan kedua-duanya. Niat diulang setiap dua rakaat."),
             ("Bolehkah solat tarawih di rumah?", "Boleh, seorang diri atau berjemaah bersama keluarga. Berjemaah di masjid lebih afdal menurut mazhab Syafi'i."),
             ("Bila mula solat tarawih pertama?", "Pada malam pertama Ramadan, iaitu malam sebelum puasa pertama. Lihat tarikhnya di Kalendar Hijrah dan Waktu Berbuka Puasa.")]),
}


def extra_html(kind):
    if kind == "hajat":
        return ('<div class="hjf"><label for="hjin">Tulis urusan atau hajat anda (pilihan)</label><input id="hjin" maxlength="120" autocomplete="off" '
                'placeholder="cth: menerima tawaran kerja di syarikat X"><p class="note">Ia dimasukkan ke dalam maksud doa di bawah supaya anda menghayatinya. Tidak dihantar ke mana-mana.</p></div>')
    if kind == "jenazah":
        return ('<div class="fl"><label for="jj">Jenazah</label><select id="jj">' + "".join(f'<option value="{k}">{e(n)}</option>' for k, n in T.JANTINA)
                + '</select></div><p class="note">Niat, doa takbir ketiga dan doa takbir keempat bertukar mengikut pilihan ini.</p>')
    if kind == "tarawih":
        return ('<div class="trw" id="trw"><h3>🔢 Pengira Rakaat Tarawih</h3><div class="chips2" id="trn" role="group" aria-label="Bilangan rakaat">'
                '<button type="button" data-n="8" aria-pressed="false">8 rakaat</button><button type="button" data-n="20" aria-pressed="true">20 rakaat</button></div>'
                '<p class="trs" id="trs" aria-live="polite">Salam ke-1 daripada 10 · rakaat 1–2</p><div class="act"><button class="btn3" type="button" id="trb">✓ Selesai 2 rakaat</button>'
                '<button class="btn2" type="button" id="tru">↶ Undur</button><button class="btn2" type="button" id="trr">⟲ Mula semula</button></div>'
                '<p class="note">Tekan selepas setiap salam. Kiraan disimpan dalam pelayar anda untuk malam ini sahaja.</p></div>')
    return ""


def build_pages7(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    day = dt.date.fromisoformat(ctx.get("SOLAT_DAY") or T_)
    share, ad = ctx["share"], ctx["ad"]
    AREA = areas()
    zc = {z[0]: [z[3], z[4]] for z in SL.ZONES}
    pages = []
    for key, slug, name, short in S.PRAYERS:
        C = CONTENT[key]
        url = url_of(key)
        D = player_data(C["variants"], key)
        if key == "jenazah":
            D["jz"] = {k: {"niat": [e(x) for x in v["niat"]], "t3": [e(x) for x in v["t3"]], "t4": [e(x) for x in v["t4"]]} for k, v in S.JENAZAH.items()}
        data = json.dumps(D, ensure_ascii=False, separators=(",", ":"))
        sw = json.dumps({"zc": zc, "def": DEF_ZONE}, separators=(",", ":"))
        widget = sw_html(C["widget"], day, AREA) if C.get("widget") else ""
        mod = day.isoformat() if C.get("modified") else T_
        modms = f"{day.day} {P.BLN[day.month - 1]} {day.year}" if C.get("modified") else TMS
        niats = "".join(niat_card(v[3], v[1] if len(C["variants"]) > 1 else name.replace("Solat ", "")) for v in C["variants"])
        info = table(["Perkara", "Keterangan"], [[f"<strong>{a}</strong>", e(b)] for a, b in C["info"]], f"Ringkasan {name}")
        body = hero(f"{e(name)}: Cara, Niat & Doa", e(C["lead"]), [("Solat Sunat", HUB), (name, None)])
        body += f'''<div class="wrap mn"><div class="ct">
<section id="panduan" class="tool" aria-labelledby="h-pan">
{widget}
{extra_html(C.get("extra", ""))}
{player_html(D, f"Cara {e(name)} Langkah demi Langkah")}
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {C["answer"]}</p></div>
{meta_line(mod, modms)}
{share(SITE + url, f"{name}: cara, niat & doa lengkap:")}
</div>
</section>

<section id="ringkasan" aria-labelledby="h-rk">
<h2 id="h-rk">{e(name)} Secara Ringkas</h2>
{info}
</section>

<section class="dsec" id="niat" aria-labelledby="h-niat">
<h2 id="h-niat">Niat {e(name)}</h2>
{niats}
</section>
{f'<section class="dsec" id="doa" aria-labelledby="h-doa"><h2 id="h-doa">Doa & Bacaan</h2>{doa_cards(C["doa"])}</section>' if C["doa"] else ""}
{ad(0)}
<section id="dalil" aria-labelledby="h-dalil">
<h2 id="h-dalil">Dalil & Fadhilat</h2>
<ul class="src">{"".join(f"<li>{e(x)}</li>" for x in C["dalil"])}</ul>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: {e(name)}</h2>
{faq_html(C["faq"])}
</section>

<section id="lain" aria-labelledby="h-lain">
<h2 id="h-lain">Solat Sunat Lain</h2>
{plinks(key)}
<p class="note"><a href="/{HUB}">Semua solat sunat & waktu dilarang solat hari ini</a> · <a href="/belajar-solat/">Cara solat fardu</a> · <a href="/solat-jamak-qasar/">Jamak & qasar (musafir)</a> · <a href="/waktu-solat/">Waktu solat hari ini</a> · <a href="/cari-masjid/">Masjid terdekat</a></p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(HUB)}</section>
</div>
{side([("panduan", "Panduan langkah demi langkah"), ("ringkasan", "Ringkasan"), ("niat", "Niat")] + ([("doa", "Doa & bacaan")] if C["doa"] else []) + [("dalil", "Dalil & fadhilat"), ("faq", "Soalan lazim"), ("lain", "Solat sunat lain")], HUB)}
</div>'''
        w0 = C["variants"][0][0]
        howto = {"@type": "HowTo", "@id": SITE + url + "#cara", "name": f"Cara {name}", "inLanguage": "ms-MY",
                 "step": [{"@type": "HowToStep", "position": i, "name": f"{I2.BACAAN.get(sid, S.BACAAN.get(sid))[0]}"} for i, (sid, _) in enumerate(D["s"][w0], 1)]}
        pages.append(dict(path=url, kind="tool", data=False, arabic=True, modified=mod,
                          extra_data=f'<script type="application/json" id="spd">{data}</script>' + (f'<script type="application/json" id="swd">{sw}</script>' if C.get("widget") else ""),
                          title=C["title"], ogtitle=f"{name}: Cara, Niat & Doa", desc=C["desc"],
                          crumbs=[("Solat Sunat", HUB), (name, None)], body=body, faq=C["faq"], about=[name, "Solat sunat"], nodes=[howto], og="solat-sunat",
                          ogcard=("Solat Sunat: Cara, Niat & Doa", "Taubat, Dhuha, Hajat, Jenazah, Witir, Istikharah, Tahajjud dan Tarawih langkah demi langkah."),
                          llms=f"{name}: {short}. Panduan langkah demi langkah dengan niat, bacaan Arab-Rumi-maksud dan dalil ({'; '.join(C['dalil'])[:220]}…)."))

    # ---------------- hub ----------------
    rows = []
    for key, slug, name, short in S.PRAYERS:
        C = CONTENT[key]
        info = dict(C["info"])
        rows.append([f'<a href="/{HUB}{slug}/"><strong>{e(name)}</strong></a>', e(info.get("Bilangan rakaat") or info.get("Bilangan takbir", "")), e(info.get("Waktu", "Bila ada jenazah")), e(info.get("Hukum", ""))])
    raw = table(["Solat fardu", "Sunat sebelum (qabliyah)", "Sunat selepas (ba'diyah)"], [[f"<strong>{a}</strong>", e(b), e(c)] for a, b, c in S.RAWATIB], "Solat sunat rawatib")
    hfaq = [
        ("Apakah solat sunat yang paling afdal?", "Selepas solat fardu, solat yang paling afdal ialah solat malam (HR Muslim, no. 1163), iaitu tahajjud dan witir. Antara yang paling dituntut juga ialah 2 rakaat sebelum Subuh: “lebih baik daripada dunia dan isinya” (HR Muslim, no. 725)."),
        ("Bilakah waktu dilarang solat sunat?", "Selepas solat Subuh hingga matahari naik setinggi tombak, ketika istiwa' (matahari tegak, beberapa minit sebelum Zohor), dan selepas solat Asar hingga matahari terbenam (HR Al-Bukhari, no. 586; Muslim, no. 831). Dalam mazhab Syafi'i, solat yang ada sebab seperti tahiyatul masjid dan solat jenazah dikecualikan. Kad di atas mengira waktu ini bagi zon anda hari ini."),
        ("Apakah solat sunat rawatib?", "Solat sunat yang mengiringi solat fardu. Yang muakkad ialah 10 rakaat: 2 sebelum Subuh, 2 sebelum dan 2 selepas Zohor, 2 selepas Maghrib dan 2 selepas Isyak (HR Al-Bukhari, no. 1180). Sesiapa menjaga 12 rakaat sehari dibina untuknya rumah di syurga (HR Muslim, no. 728)."),
        ("Adakah niat solat sunat perlu dilafazkan?", "Niat ialah amalan hati ketika takbiratul ihram. Melafazkannya sebelum takbir sunat dalam mazhab Syafi'i untuk membantu hati, tetapi tidak wajib."),
        ("Bolehkah qada solat sunat?", "Solat sunat yang ada waktu tertentu seperti rawatib, dhuha dan witir sunat diqada jika terlepas (pendapat yang muktamad dalam mazhab Syafi'i). Solat sunat yang bersebab seperti tahiyatul masjid tidak diqada."),
    ]
    hub_body = hero("Solat Sunat: Cara, Niat, Doa & Waktu Hari Ini",
                    "Lapan solat sunat yang paling dicari dengan panduan langkah demi langkah, serta waktu dhuha, sepertiga malam terakhir dan waktu dilarang solat hari ini bagi zon anda.",
                    [("Solat Sunat", None)])
    hub_body += f'''<div class="wrap mn"><div class="ct">
<section id="waktu" class="tool" aria-labelledby="h-sw">
{sw_html("hub", day, AREA)}
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Solat sunat ialah solat yang diberi pahala jika dikerjakan dan tidak berdosa jika ditinggalkan. Yang paling dituntut ialah <strong>witir, tahajjud, dhuha dan rawatib</strong> (terutama 2 rakaat sebelum Subuh). Kebanyakannya <strong>2 rakaat satu salam</strong>, kecuali witir (ganjil) dan jenazah (4 takbir berdiri). Solat sunat <strong>dilarang</strong> selepas Subuh hingga matahari naik, ketika istiwa' dan selepas Asar hingga Maghrib.</p></div>
{meta_line(day.isoformat(), f"{day.day} {P.BLN[day.month - 1]} {day.year}")}
{share(SITE + HUB, "Solat sunat: cara, niat, doa & waktu hari ini:")}
</div>
</section>

<section id="senarai" aria-labelledby="h-sen">
<h2 id="h-sen">Senarai Solat Sunat</h2>
{table(["Solat", "Rakaat", "Waktu", "Hukum"], rows, "Senarai solat sunat")}
{plinks(None)}
</section>

<section id="rawatib" aria-labelledby="h-raw">
<h2 id="h-raw">Solat Sunat Rawatib (Sebelum & Selepas Fardu)</h2>
{raw}
<p class="note">Muakkad (sangat dituntut): 2 sebelum Subuh, 2 sebelum dan 2 selepas Zohor, 2 selepas Maghrib, 2 selepas Isyak (HR Al-Bukhari, no. 1180). Cara solatnya sama seperti solat sunat 2 rakaat lain dengan niat “sunnatas-subhi qabliyyatan”, “sunnataz-zuhri ba'diyyatan” dan seterusnya.</p>
</section>
{ad(0)}
<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Solat Sunat</h2>
{faq_html(hfaq)}
<p class="note">Lihat juga <a href="/belajar-solat/">cara solat fardu lengkap</a>, <a href="/kalendar-hijrah/">puasa sunat & kalendar Hijrah</a> dan <a href="/zikir-pagi-petang/">zikir selepas solat</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(HUB)}</section>
</div>
{side([("waktu", "Waktu hari ini"), ("senarai", "Senarai solat sunat"), ("rawatib", "Rawatib"), ("faq", "Soalan lazim")], HUB)}
</div>'''
    pages.insert(0, dict(path=HUB, kind="tool", data=False, arabic=False, modified=day.isoformat(),
                         extra_data=f'<script type="application/json" id="swd">{json.dumps({"zc": zc, "def": DEF_ZONE}, separators=(",", ":"))}</script>',
                         title="Solat Sunat: Cara, Niat, Doa & Waktu Dilarang Solat Hari Ini", ogtitle="Solat Sunat: Cara, Niat & Doa",
                         desc="Panduan solat sunat taubat, dhuha, hajat, jenazah, witir, istikharah, tahajjud & tarawih, rawatib, serta waktu dhuha & waktu dilarang solat hari ini.",
                         crumbs=[("Solat Sunat", None)], body=hub_body, faq=hfaq, about=["Solat sunat", "Solat rawatib", "Waktu dilarang solat"], og="solat-sunat",
                         ogcard=("Solat Sunat: Cara, Niat & Doa", "Taubat, Dhuha, Hajat, Jenazah, Witir, Istikharah, Tahajjud dan Tarawih langkah demi langkah."),
                         itemlist=dict(name="Panduan solat sunat", items=[{"@type": "ListItem", "position": i, "name": n, "url": SITE + HUB + s + "/"} for i, (_, s, n, _) in enumerate(S.PRAYERS, 1)]),
                         llms="Hub solat sunat: waktu dhuha, sepertiga malam terakhir dan waktu dilarang solat hari ini (ikut zon JAKIM), senarai 8 solat sunat dengan rakaat dan waktu, solat rawatib (HR Al-Bukhari 1180, Muslim 728)."))
    return pages
