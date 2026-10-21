"""Page: /solat-jamak-qasar/: the musafir calculator (is this trip 2 marhalah? does the 4-day stay rule end the rukhsah?),
today's jamak windows for the destination's JAKIM zone, and the step player for every jamak/qasar combination (two prayers
back to back, each with its own niat). Niat lafaz are assembled from fixed parts so every combination reads the same way.
alat.js mirrors verdict_html (jamak block) and sw_card("jamak") (pages7)."""
import json, datetime as dt
import ibadah2 as I2
import sunat as S
import solat as SL
import masjid as M
import plans as P
from pages import e, faq_html, hero, side, meta_line, tool_cards, table, SITE
from pages2 import quran_block, qref, card
from pages3 import areas
import pages7 as P7

PATH = "solat-jamak-qasar/"
MARHALAH = 81  # km; 2 marhalah as most Malaysian religious authorities estimate it
MAYBE = 55     # km straight-line; below this the road distance rarely reaches 81 km

AR = {"zohor": "الظُّهْرِ", "asar": "الْعَصْرِ", "maghrib": "الْمَغْرِبِ", "isyak": "الْعِشَاءِ"}
RU = {"zohor": "z-zuhri", "asar": "l-'asri", "maghrib": "l-maghribi", "isyak": "l-'isya'i"}
MS = {"zohor": "Zohor", "asar": "Asar", "maghrib": "Maghrib", "isyak": "Isyak"}
RK_AR = {2: "رَكْعَتَيْنِ", 3: "ثَلَاثَ رَكَعَاتٍ", 4: "أَرْبَعَ رَكَعَاتٍ"}
RK_RU = {2: "rak'ataini", 3: "thalatha raka'atin", 4: "arba'a raka'atin"}
RK_MS = {2: "dua rakaat", 3: "tiga rakaat", 4: "empat rakaat"}


def jniat(p, rk, other=None, taqdim=True):
    """Niat for one fardu prayer: qasar when shortened to 2 from 4, jamak with `other` when combined."""
    qasar = rk == 2
    ar = f"أُصَلِّي فَرْضَ {AR[p]} {RK_AR[rk]}" + (" قَصْرًا" if qasar else "") \
        + (f" مَجْمُوعًا مَعَ {AR[other]} جَمْعَ {'تَقْدِيمٍ' if taqdim else 'تَأْخِيرٍ'}" if other else "") + " لِلّٰهِ تَعَالَى"
    ru = f"Usolli fardha{RU[p]} {RK_RU[rk]}" + (" qasran" if qasar else "") \
        + (f" majmu'an ma'a{RU[other]} jam'a {'taqdimin' if taqdim else "ta'khirin"}" if other else "") + " lillahi ta'ala."
    ms = f"Sahaja aku solat fardu {MS[p]} {RK_MS[rk]}" + (" secara qasar" if qasar else "") \
        + (f", dijamakkan dengan {MS[other]} secara jamak {'taqdim' if taqdim else 'takhir'}" if other else "") + ", kerana Allah Taala."
    return ar, ru, ms


S.BACAAN["niat2"] = ("Niat Solat Kedua", "Berdiri menghadap kiblat dan berniat untuk solat kedua bersama takbiratul ihram; selebihnya sama seperti solat biasa.", "", "", "",
                     "Rukun solat; HR Al-Bukhari, no. 1")
S.BACAAN["sambung"] = ("Terus ke Solat Kedua", "Selepas salam, terus berdiri dan berniat untuk solat kedua tanpa diselangi masa yang lama. Bagi jamak taqdim ini syarat sah (muwalat); bagi jamak takhir ia sunat. Boleh iqamah sebelum solat kedua.",
                       "", "", "", "Syarat jamak taqdim dalam mazhab Syafi'i: tertib, niat jamak dalam solat pertama dan berturut-turut (muwalat)")


def fard(p, rk, niat_id):
    return [(niat_id if sid == "niat" else sid, f"{MS[p]} {r}/{rk}") for sid, r in I2.solat_steps(rk, False)]


# (wkey, label, first, rakaat, second, rakaat, taqdim)
COMBOS = [
    ("za-taqdim", "Zohor + Asar · taqdim · qasar", "zohor", 2, "asar", 2, True),
    ("za-takhir", "Zohor + Asar · takhir · qasar", "zohor", 2, "asar", 2, False),
    ("mi-taqdim", "Maghrib + Isyak · taqdim · qasar", "maghrib", 3, "isyak", 2, True),
    ("mi-takhir", "Maghrib + Isyak · takhir · qasar", "maghrib", 3, "isyak", 2, False),
    ("za-penuh", "Zohor + Asar · taqdim · tanpa qasar", "zohor", 4, "asar", 4, True),
    ("mi-penuh", "Maghrib + Isyak · taqdim · tanpa qasar", "maghrib", 3, "isyak", 4, True),
]


def player():
    variants, niat2 = [], {}
    for wk, label, a, ra, b, rb, tq in COMBOS:
        st = fard(a, ra, "niat") + [("sambung", f"{MS[a]} → {MS[b]}")] + fard(b, rb, "niat2")
        variants.append((wk, label, ra + rb, jniat(a, ra, b, tq), st, "Rakaat"))
        niat2[wk] = jniat(b, rb, a, tq)
    variants.append(("qasar", "Qasar sahaja (Zohor 2 rakaat)", 2, jniat("zohor", 2), fard("zohor", 2, "niat"), "Rakaat"))
    D = P7.player_data(variants, "jamak")
    for wk, n in niat2.items():
        D["w"][wk]["niat2"] = [e(x) for x in n]
    return D


def towns():
    """[name, state, lat, lng, zone] for every town the site knows (prayer-time towns + masjid anchors), by name."""
    out = {}
    for slug, name, state, lat, lng, z in SL.CITIES:
        out.setdefault(name, [name, state.split(",")[0].replace("W.P. ", ""), lat, lng, z])
    for z, (_, aa) in M.ZONEINFO.items():
        for a in aa:
            if len(a) < 4:
                out.setdefault(a[0], [a[0], M.STATE_NAME[M.STATE_OF[z]], a[1], a[2], z])
    return sorted(out.values(), key=lambda t: t[0])


def verdict_html(a, b, stay=None):
    """a, b: town rows; stay: (arrival, departure) dates or None. alat.js jVerdict() returns the same string."""
    km = int(M.km(a[2], a[3], b[2], b[3]) + .5)
    if km >= MARHALAH:
        head, cls, why = "✅ Layak jamak &amp; qasar", "ok", f"Jarak garis lurus {a[0]} → {b[0]} ialah {km} km, melebihi 2 marhalah (≈{MARHALAH} km). Jarak jalan biasanya lebih jauh lagi."
    elif km >= MAYBE:
        head, cls, why = "⚠️ Semak jarak jalan", "mb", f"Jarak garis lurus {km} km. Jarak jalan biasanya 20–40% lebih jauh; jika laluan anda {MARHALAH} km atau lebih, anda layak."
    else:
        head, cls, why = "❌ Belum mencapai 2 marhalah", "no", f"Jarak garis lurus {km} km; jarak jalan jarang mencecah {MARHALAH} km. Solatlah penuh pada waktunya."
    out = (f'<p class="jvh {cls}">{head}</p><p>{why} <a href="https://www.google.com/maps/dir/?api=1&amp;origin={a[2]},{a[3]}&amp;destination={b[2]},{b[3]}" rel="noopener nofollow">Semak jarak jalan di Google Maps ↗</a></p>')
    if stay:
        full = (stay[1] - stay[0]).days - 1
        if full < -1:
            out += "<p>Tarikh pulang mesti selepas tarikh tiba.</p>"
        elif full >= 4:
            out += f"<p>Tinggal <strong>{full} hari penuh</strong> (tidak termasuk hari tiba dan hari pulang): anda dikira bermukim sebaik tiba di {b[0]}; jamak dan qasar hanya semasa perjalanan pergi dan pulang.</p>"
        else:
            out += f"<p>Tinggal <strong>{max(full, 0)} hari penuh</strong> (kurang daripada 4): boleh jamak dan qasar sepanjang berada di {b[0]} hingga pulang.</p>"
    return out + f'<p class="note">Waktu jamak di bawah mengikut zon destinasi, {b[4]}.</p>'


def build_jamak(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    day = dt.date.fromisoformat(ctx.get("SOLAT_DAY") or T_)
    share, ad = ctx["share"], ctx["ad"]
    AREA = areas()
    TW = towns()
    A0, B0 = next(t for t in TW if t[0] == "Kuala Lumpur"), next(t for t in TW if t[0] == "Ipoh")
    D = player()
    ZC = {z[0]: [z[3], z[4]] for z in SL.ZONES}
    sw = sw_jamak(day, AREA, B0[4])
    niats = "".join(P7.niat_card(jniat(a, ra, b, tq), f"{MS[a]} ({'taqdim' if tq else 'takhir'}{', qasar' if ra == 2 else ''})") +
                    P7.niat_card(jniat(b, rb, a, tq), f"{MS[b]} ({'taqdim' if tq else 'takhir'}{', qasar' if rb == 2 else ''})")
                    for _, _, a, ra, b, rb, tq in COMBOS[:4])
    niats += "".join(P7.niat_card(jniat(p, 2), f"{MS[p]} qasar sahaja") for p in ("zohor", "asar", "isyak"))
    ar, ru, mn = quran_block([(4, 101)])
    ayat = card("ayat-qasar", "Dalil qasar: An-Nisa' 101", ar, ru, mn, qref(4, 101))
    syarat = [
        ("Syarat Qasar", ["Perjalanan yang harus (bukan untuk maksiat).", f"Jarak sekurang-kurangnya 2 marhalah (≈{MARHALAH} km) sehala, dan destinasinya diketahui.",
                          "Telah keluar dari sempadan kawasan mukim (kampung atau bandar) sendiri.", "Hanya solat empat rakaat (Zohor, Asar, Isyak) yang tunai atau diqada dalam musafir.",
                          "Berniat qasar ketika takbiratul ihram.", "Tidak menjadi makmum kepada imam yang solat penuh (jika ya, wajib solat 4 rakaat)."]),
        ("Syarat Jamak Taqdim", ["Dilakukan dalam waktu solat pertama (Zohor atau Maghrib).", "Tertib: solat pertama dahulu, kemudian solat kedua.",
                                 "Niat jamak dalam solat pertama, sebaik-baiknya ketika takbiratul ihram.", "Berturut-turut (muwalat) tanpa diselangi masa yang lama.",
                                 "Masih musafir ketika memulakan solat kedua."]),
        ("Syarat Jamak Takhir", ["Berniat jamak takhir semasa masih dalam waktu solat pertama (cukup dalam hati, cth: “aku akan menjamakkan Zohor dengan Asar”).",
                                 "Masih musafir hingga selesai kedua-dua solat.", "Tertib dan berturut-turut adalah sunat, tidak wajib."]),
    ]
    sy = "".join(f'<h3>{h}</h3><ol class="src">{"".join(f"<li>{e(x)}</li>" for x in xs)}</ol>' for h, xs in syarat)
    combos = table(["Gabungan", "Jamak taqdim", "Jamak takhir", "Qasar"],
                   [["<strong>Zohor + Asar</strong>", "Dalam waktu Zohor", "Dalam waktu Asar", "2 + 2 rakaat"],
                    ["<strong>Maghrib + Isyak</strong>", "Dalam waktu Maghrib", "Dalam waktu Isyak", "3 + 2 rakaat (Maghrib tidak diqasar)"],
                    ["<strong>Subuh</strong>", "Tidak boleh", "Tidak boleh", "Tidak boleh (kekal 2 rakaat)"],
                    ["<strong>Asar + Maghrib</strong>", "Tidak boleh", "Tidak boleh", "–"]], "Gabungan solat jamak")
    faq = [
        ("Berapa km jarak untuk solat jamak dan qasar?", f"Sekurang-kurangnya 2 marhalah sehala. Kebanyakan pihak berkuasa agama di Malaysia menganggarkannya kira-kira {MARHALAH} km; sebahagian ulama menyebut hingga 89 km. Kalkulator di atas membandingkan jarak bandar anda dengan had ini; jika jarak anda di sempadan, rujuk pejabat agama negeri."),
        ("Bilakah boleh mula jamak dan qasar?", "Selepas keluar dari sempadan kawasan mukim (kampung atau bandar) anda. Jamak takhir boleh diniatkan sebelum bertolak jika waktu Zohor sudah masuk dan anda akan keluar sebelum waktunya tamat."),
        ("Berapa hari boleh jamak dan qasar di destinasi?", "Dalam mazhab Syafi'i, jika berniat tinggal 4 hari penuh atau lebih (tidak termasuk hari tiba dan hari pulang), anda bermukim sebaik tiba dan tidak lagi boleh jamak dan qasar di sana. Jika kurang daripada itu, rukhsah berterusan hingga pulang. Isi tarikh tiba dan pulang di kalkulator untuk semakan."),
        ("Bolehkah jamak tanpa qasar?", "Boleh. Musafir boleh menjamak solat dengan bilangan rakaat penuh (Zohor 4 + Asar 4) atau hanya qasar tanpa jamak. Pilih “tanpa qasar” dalam panduan langkah demi langkah."),
        ("Bolehkah solat jamak jika bermakmum dengan imam yang tidak musafir?", "Boleh jamak, tetapi tidak boleh qasar: jika bermakmum kepada imam yang solat penuh walaupun seketika, wajib menyempurnakan 4 rakaat."),
        ("Bolehkah solat Jumaat dijamak dengan Asar?", "Musafir tidak wajib solat Jumaat. Jika dia menunaikan Jumaat, menurut mazhab Syafi'i dia boleh menjamak taqdim Asar selepasnya, tetapi tidak boleh jamak takhir."),
        ("Bolehkah jamak kerana hujan atau sakit?", "Mazhab Syafi'i membenarkan jamak taqdim kerana hujan lebat bagi yang solat berjemaah di masjid. Jamak kerana sakit diperselisihkan; sebahagian ulama Syafi'i seperti Imam An-Nawawi menganggapnya kuat berdasarkan hadis Ibn 'Abbas (HR Muslim, no. 705). Ia tidak boleh dijadikan kebiasaan tanpa keperluan."),
    ]
    body = hero("Solat Jamak & Qasar: Kalkulator Musafir, Niat & Cara",
                "Semak sama ada perjalanan anda layak jamak dan qasar, waktu jamak hari ini di destinasi, dan cara solat setiap gabungan dengan niat yang betul.",
                [("Cara Solat", "belajar-solat/"), ("Jamak & Qasar", None)])
    opts = "".join(f'<option value="{e(t[0])}">{e(t[1])}</option>' for t in TW)
    body += f'''<div class="wrap mn"><div class="ct">
<section id="panduan" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira">🚗 Kalkulator Musafir: Boleh Jamak & Qasar?</h2>
<form class="frm" id="jmf" novalidate>
<div class="fl"><label for="jfrom">Dari (bandar mukim)</label><input id="jfrom" list="jtowns" value="{A0[0]}" autocomplete="off"></div>
<div class="fl"><label for="jto">Ke (destinasi)</label><input id="jto" list="jtowns" value="{B0[0]}" autocomplete="off"></div>
<div class="fl"><label for="jt1">Tarikh tiba (pilihan)</label><input type="date" id="jt1"></div>
<div class="fl"><label for="jt2">Tarikh pulang (pilihan)</label><input type="date" id="jt2"></div>
<datalist id="jtowns">{opts}</datalist>
</form>
<div class="act"><button class="btn2" type="button" id="jgeo">📍 Guna lokasi saya sebagai “Dari”</button><button class="btn2" type="button" data-act="link">🔗 Salin pautan</button></div>
<div class="jv" id="jout" aria-live="polite">{verdict_html(A0, B0)}</div>
{sw}
{P7.player_html(D, "Cara Solat Jamak & Qasar Langkah demi Langkah")}
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Musafir yang perjalanannya sekurang-kurangnya <strong>2 marhalah (≈{MARHALAH} km)</strong> boleh <strong>qasar</strong> (memendekkan Zohor, Asar dan Isyak kepada 2 rakaat) dan <strong>jamak</strong> (menghimpunkan <strong>Zohor dengan Asar</strong> atau <strong>Maghrib dengan Isyak</strong>) sama ada <strong>taqdim</strong> (dalam waktu pertama) atau <strong>takhir</strong> (dalam waktu kedua). Subuh dan Maghrib tidak diqasar. Rukhsah tamat di destinasi jika berniat tinggal 4 hari penuh atau lebih.</p></div>
{meta_line(day.isoformat(), f"{day.day} {P.BLN[day.month - 1]} {day.year}")}
{share(SITE + PATH, "Kalkulator musafir: boleh jamak & qasar? + niat dan cara:")}
</div>
</section>

<section id="gabungan" aria-labelledby="h-gab">
<h2 id="h-gab">Solat yang Boleh Dijamak & Diqasar</h2>
{combos}
</section>

<section id="syarat" aria-labelledby="h-sy">
<h2 id="h-sy">Syarat Jamak & Qasar</h2>
{sy}
</section>
{ad(0)}
<section class="dsec" id="niat" aria-labelledby="h-niat">
<h2 id="h-niat">Niat Solat Jamak & Qasar</h2>
<p class="note">Niat ialah amalan hati ketika takbiratul ihram; lafaz di bawah sunat untuk membantu hati (mazhab Syafi'i). Bagi jamak tanpa qasar, gugurkan “qasran” dan sebut bilangan rakaat penuh.</p>
{niats}
</section>

<section class="dsec" id="dalil" aria-labelledby="h-dalil">
<h2 id="h-dalil">Dalil Jamak & Qasar</h2>
{ayat}
<ul class="src">
<li>Qasar ialah “sedekah yang Allah berikan kepada kamu, maka terimalah sedekah-Nya” (HR Muslim, no. 686).</li>
<li>Rasulullah SAW menjamakkan Maghrib dan Isyak apabila perjalanan baginda tergesa-gesa (HR Al-Bukhari, no. 1106).</li>
<li>Ibn 'Abbas: Rasulullah SAW pernah menjamakkan Zohor dengan Asar dan Maghrib dengan Isyak di Madinah supaya tidak menyusahkan umatnya (HR Muslim, no. 705).</li>
<li>Asas had 4 hari: Rasulullah SAW membenarkan Muhajirin tinggal di Mekah tiga hari selepas haji (HR Muslim, no. 1352); tinggal lebih daripada itu dikira bermukim dalam mazhab Syafi'i.</li>
</ul>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Jamak & Qasar</h2>
{faq_html(faq)}
<p class="note">Lihat juga <a href="/belajar-solat/">cara solat fardu</a>, <a href="/solat-sunat/">solat sunat</a>, <a href="/waktu-solat/">waktu solat</a> dan <a href="/cari-masjid/">masjid terdekat di destinasi</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(PATH)}</section>
</div>
{side([("panduan", "Kalkulator musafir"), ("h-sw", "Waktu jamak hari ini"), ("h-pan", "Langkah demi langkah"), ("gabungan", "Gabungan"), ("syarat", "Syarat"), ("niat", "Niat"), ("dalil", "Dalil"), ("faq", "Soalan lazim")], PATH)}
</div>'''
    jd = json.dumps({"tw": TW, "mh": MARHALAH, "mb": MAYBE}, ensure_ascii=False, separators=(",", ":"))
    swd = json.dumps({"zc": ZC, "def": B0[4]}, separators=(",", ":"))
    howto = {"@type": "HowTo", "@id": SITE + PATH + "#cara", "name": "Cara solat jamak taqdim Zohor dan Asar secara qasar", "inLanguage": "ms-MY",
             "step": [{"@type": "HowToStep", "position": i, "name": f"{D['b'][sid][0]} ({r})"} for i, (sid, r) in enumerate(D["s"]["za-taqdim"], 1)]}
    return [dict(path=PATH, kind="tool", data=False, arabic=True, modified=day.isoformat(),
                 extra_data=f'<script type="application/json" id="spd">{json.dumps(D, ensure_ascii=False, separators=(",", ":"))}</script>'
                            f'<script type="application/json" id="swd">{swd}</script><script type="application/json" id="jmd">{jd}</script>',
                 title="Solat Jamak & Qasar: Kalkulator Musafir, Niat, Cara & Waktu", ogtitle="Solat Jamak & Qasar: Kalkulator Musafir",
                 desc=f"Semak boleh jamak & qasar ikut jarak (2 marhalah ≈{MARHALAH} km) dan tempoh tinggal, waktu jamak hari ini, niat dan cara setiap gabungan solat.",
                 crumbs=[("Cara Solat", "belajar-solat/"), ("Jamak & Qasar", None)], body=body, faq=faq, about=["Solat jamak", "Solat qasar", "Musafir"],
                 nodes=[howto], og="solat-jamak-qasar",
                 app=dict(name="Kalkulator Musafir Jamak & Qasar", features=[f"Semakan jarak 2 marhalah (≈{MARHALAH} km) antara {len(TW)} bandar", "Peraturan tinggal 4 hari penuh",
                                                                             "Waktu jamak taqdim dan takhir hari ini ikut zon JAKIM destinasi", "Panduan langkah demi langkah setiap gabungan",
                                                                             "Niat jamak dan qasar Arab, Rumi dan maksud"]),
                 llms=f"Solat jamak & qasar: kalkulator musafir (2 marhalah ≈{MARHALAH} km, garis lurus + pautan jarak jalan; tinggal ≥4 hari penuh = bermukim), waktu jamak taqdim/takhir hari ini ikut zon JAKIM, niat setiap gabungan, syarat, dalil (An-Nisa' 4:101; HR Muslim 686, 705, 1352; Al-Bukhari 1106).")]


def sw_jamak(day, AREA, zone):
    """The pages7 time card in its 'jamak' form, for the destination's zone."""
    import ramadan as R
    t, _ = R.day_times(zone, day)
    tn, _ = R.day_times(zone, day + dt.timedelta(1))
    opts = "".join(f'<option value="{z[0]}"{" selected" if z[0] == zone else ""}>{z[0]} · {e(AREA[z[0]][:48])}</option>' for z in SL.ZONES)
    return (f'<div class="sw2" id="sw2" data-k="jamak"><h3 id="h-sw">🕰 Waktu Jamak Hari Ini</h3><div class="fl"><label for="swz">Zon waktu solat</label><select id="swz">{opts}</select></div>'
            f'<div id="swo" aria-live="polite">{P7.sw_card("jamak", t, tn, zone, day)}</div>'
            f'<p class="note">Daripada jadual rasmi JAKIM (e-solat.gov.my). Zon bertukar mengikut destinasi di kalkulator.</p></div>')
