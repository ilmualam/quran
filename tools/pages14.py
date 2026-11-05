"""Per-zone pages for the multi-zone states: /waktu-solat/<negeri>/<zon>/ and /waktu-berbuka-puasa/<negeri>/<zon>/.
States with a single JAKIM zone (Melaka, Perlis, Pulau Pinang, Kuala Lumpur & Putrajaya, Labuan) keep the state page as
the zone page, so no URL repeats another.

Each page is built from data only that zone has: its own official JAKIM timetable (month table, a 12-month summary of
earliest/latest times, the Ramadan imsakiyah with Lailatul Qadar nights and the 1 Syawal syuruk), the qibla bearing and
distance to the Kaabah from every town in the zone, and how its times differ from the other zones in the state. Zones
without an official timetable for the year fall back to the calibrated calculation in solat.py, labelled as such."""
import json, calendar, datetime as dt
import solat as SL
import masjid as MQ
import ramadan as R
import ibadah2 as I2
import plans as P
from pages import e, faq_html, hero, side, meta_line, table, tool_cards, SITE, TBB
from pages2 import card
from pages3 import areas, load, solat_tool, zpath, HB, API
from pages4 import ramadan_tool, lailatul, PUB
from pages5 import anchor_id

TODAY_CLS = ' class="today"'

STATE = {s[0]: s for s in SL.STATES}  # slug -> (slug, name, capital, capital zone)
OGS = ("waktu-solat-zon", ("Waktu Solat Ikut Zon JAKIM", "Jadual rasmi setiap zon: hari ini, sebulan, setahun dan arah kiblat setiap bandar."))
OGR = ("waktu-berbuka-puasa-zon", ("Waktu Berbuka Puasa Ikut Zon", "Jadual imsak & berbuka Ramadan setiap zon JAKIM, dengan malam Lailatul Qadar."))


def multi(state):
    return sum(1 for z in SL.ZONES if z[1] == state) > 1


def towns(code):
    return [a[0] for a in MQ.ZONEINFO[code][1]]


def tname(code, k):
    """First k towns of the zone, joined for a title: "Shah Alam, Petaling Jaya & Subang Jaya"."""
    t = towns(code)[:k]
    return t[0] if len(t) == 1 else ", ".join(t[:-1]) + " & " + t[-1]


def fit(fmt, code, limit):
    """Longest town list (3 → 1) that keeps fmt within limit characters."""
    for k in (3, 2, 1):
        s = fmt.format(t=tname(code, k))
        if len(s) <= limit:
            return s
    return fmt.format(t=towns(code)[0])[:limit]


def year_times(code, y):
    """(365/366 rows of minutes, official?) for one zone and year."""
    o = load(code, y)
    if o:
        return o, True
    z = next(z for z in SL.ZONES if z[0] == code)
    n = 366 if calendar.isleap(y) else 365
    days = [dt.date(y, 1, 1) + dt.timedelta(i) for i in range(n)]
    return {"t": [SL.solat_day(d.year, d.month, d.day, z[3], z[4]) for d in days], "h": [], "src": "kiraan"}, False


def rng(a):
    lo, hi = min(a), max(a)
    return SL.hm(lo) if lo == hi else f"{SL.hm(lo)}–{SL.hm(hi)}"


def town_rows(code):
    """Each town of the zone: qibla bearing, distance to the Kaabah and a link to its nearby mosques."""
    out, d = [], MQ.load(code)
    has = {a[0] for tw, a in zip(d["towns"], MQ.ZONEINFO[code][1]) if tw["m"]} if d else set()
    base = f"/cari-masjid/{MQ.ZONEINFO[code][0]}/"
    for a in MQ.ZONEINFO[code][1]:
        t, la, ln = a[0], a[1], a[2]
        out.append([f"<strong>{e(t)}</strong>", f"{SL.qibla(la, ln):.1f}°", f"{MQ.km(la, ln, *SL.KAABA):,.0f} km".replace(",", "."),
                    f'<a href="{base}#dekat-{anchor_id(t)}">Masjid & surau ›</a>' if t in has else f'<a href="{base}">Cari terdekat ›</a>'])
    return out


def zlink(base, code, cur, AREA):
    """Area label of a zone row: plain on the zone's own page, a link to the zone's page otherwise."""
    return e(AREA[code]) if code == cur else f'<a href="/{zpath(base, code)}">{e(AREA[code])}</a>'


def place_node(url, code, state_name, area, lat, lng):
    return {"@type": "Place", "@id": url + "#zon", "name": f"Zon {code}: {area}", "address": {"@type": "PostalAddress", "addressRegion": state_name, "addressCountry": "MY"},
            "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
            "containsPlace": [{"@type": "Place", "name": t} for t in towns(code)]}


# ======================= WAKTU SOLAT: one page per zone =======================
def build_solat_zones(ctx, AREA, day):
    T, TMS, share, ad = ctx["TODAY"], ctx["TODAYMS"], ctx["share"], ctx["ad"]
    doy = (day - dt.date(day.year, 1, 1)).days
    dim = calendar.monthrange(day.year, day.month)[1]
    mon = f"{P.BLN[day.month - 1]} {day.year}"
    pages = []
    for code, st, _, lat, lng in SL.ZONES:
        if not multi(st):
            continue
        slug, name, cap, capz = STATE[st]
        zones = [z for z in SL.ZONES if z[1] == st]
        url = zpath("waktu-solat/", code)
        cd, off = year_times(code, day.year)
        t0 = towns(code)
        cities = [[z[0], f"{z[0]} · {AREA[z[0]]}", name, z[3], z[4], z[0]] for z in zones]
        go = {z[0]: "/" + zpath("waktu-solat/", z[0]) for z in zones if z[0] != code}
        tt = cd["t"][doy]
        times = "".join(f'<li data-i="{i}"><span class="sn">{n}</span><span class="st">{SL.hm(tt[i])}</span></li>' for i, n in enumerate(SL.NAMES))
        rows = []
        for k in range(1, dim + 1):
            r = cd["t"][doy - day.day + k]
            cls = ' class="today"' if k == day.day else ""
            rows.append(f'<tr{cls}><td>{k} {P.BLS[day.month - 1]}</td>' + "".join(f"<td>{SL.hm(x)}</td>" for x in r) + "</tr>")
        opts = "".join(f'<option value="{z[0]}"{" selected" if z[0] == code else ""}>{e(z[0] + " · " + AREA[z[0]])}</option>' for z in zones)
        cz = next(z for z in zones if z[0] == code)
        qb = SL.qibla(lat, lng)
        hijs = ""
        if cd.get("h") and cd["h"][doy]:
            hy, hmn, hd = map(int, cd["h"][doy].split("-"))
            hijs = f"{hd} {HB[hmn - 1]} {hy} H"
        src = None if off else (f"Sumber: <strong>kiraan anggaran</strong> parameter JAKIM untuk zon {code}. Jadual rasmi JAKIM menggantikannya secara automatik sebaik sahaja diterbitkan; "
                                'semak <a href="https://www.e-solat.gov.my/" rel="noopener">e-solat.gov.my</a>.')
        tool = solat_tool(f"{t0[0]} ({code})", day, doy, cd, cz, cities, opts, times, rows, qb, hijs, src)
        sdata = json.dumps({"api": API, "c": cities, "n": SL.NAMES, "fa": SL.FAJR, "is": SL.ISHA, "tz": SL.TZ, "hb": HB,
                            "def": code, "key": "solat-z-" + code, "go": go}, ensure_ascii=False, separators=(",", ":"))

        # whole-year facts for this zone
        y0 = dt.date(day.year, 1, 1)
        allt = cd["t"]
        sub = [(r[1], i) for i, r in enumerate(allt)]
        mag = [(r[5], i) for i, r in enumerate(allt)]
        e_sub, l_sub, e_mag, l_mag = min(sub), max(sub), min(mag), max(mag)
        dd = lambda i: P.dlong(y0 + dt.timedelta(i))
        yrows = []
        for m in range(12):
            a = (dt.date(day.year, m + 1, 1) - y0).days
            b = a + calendar.monthrange(day.year, m + 1)[1]
            mt = allt[a:b]
            cls = ' class="today"' if m + 1 == day.month else ""
            yrows.append(f"<tr{cls}><td>{P.BLN[m]}</td>" + "".join(f"<td>{rng([r[i] for r in mt])}</td>" for i in (1, 2, 3, 4, 5, 6)) + "</tr>")
        mmag = [cd["t"][doy - day.day + k][5] for k in range(1, dim + 1)]
        msub = [cd["t"][doy - day.day + k][1] for k in range(1, dim + 1)]

        # the other zones of the state, today (official where synced)
        others = []
        for z in zones:
            zd, _ = year_times(z[0], day.year)
            others.append((z, zd["t"][doy]))
        zrows = "".join(f'<tr data-z="{z[0]}"{TODAY_CLS if z[0] == code else ""}><th scope="row"><a href="#bandar={z[0]}" data-zone="{z[0]}">{z[0]}</a>'
                        f'<span class="za">{zlink("waktu-solat/", z[0], code, AREA)}</span></th>'
                        + "".join(f'<td data-k="{k}">{SL.hm(t[k])}</td>' for k in (1, 3, 4, 5, 6)) + "</tr>" for z, t in others)
        capt = next(t for z, t in others if z[0] == capz)
        dm = tt[5] - capt[5]
        vs = ("" if code == capz else
              f"Hari ini Maghrib zon {code} {'sama dengan' if dm == 0 else (str(abs(dm)) + ' minit ' + ('lebih lewat daripada' if dm > 0 else 'lebih awal daripada'))} zon {capz} ({cap}).")

        tw = tname(code, 3)
        area = AREA[code]
        faq = [
            (f"Pukul berapa waktu solat di {t0[0]} hari ini?",
             f"Pada {P.dlong(day)}, waktu solat zon {code} ({t0[0]}): Imsak {SL.hm(tt[0])}, Subuh {SL.hm(tt[1])}, Syuruk {SL.hm(tt[2])}, Zohor {SL.hm(tt[3])}, Asar {SL.hm(tt[4])}, Maghrib {SL.hm(tt[5])} dan Isyak {SL.hm(tt[6])}."),
            (f"Kawasan mana yang menggunakan zon {code}?",
             f"Zon {code} JAKIM meliputi {area}, {name}. Bandar utama dalam zon ini: {', '.join(t0)}. Semua kawasan ini mengikut jadual waktu solat yang sama."),
            (f"Bilakah Subuh paling awal dan paling lewat di {t0[0]} tahun {day.year}?",
             f"Bagi zon {code}, Subuh paling awal pada tahun {day.year} ialah {SL.hm(e_sub[0])} ({dd(e_sub[1])}) dan paling lewat {SL.hm(l_sub[0])} ({dd(l_sub[1])}). "
             f"Maghrib paling awal {SL.hm(e_mag[0])} ({dd(e_mag[1])}) dan paling lewat {SL.hm(l_mag[0])} ({dd(l_mag[1])})."),
            (f"Bilakah waktu Maghrib di {t0[0]} pada {mon}?",
             f"Pada {mon}, Maghrib zon {code} antara {SL.hm(min(mmag))} dan {SL.hm(max(mmag))}, manakala Subuh antara {SL.hm(min(msub))} dan {SL.hm(max(msub))}. Jadual harian penuh ada di atas."),
            (f"Ke arah mana kiblat dari {t0[0]}?",
             f"Kiblat dari {t0[0]} menghala {SL.qibla(*MQ.ZONEINFO[code][1][0][1:3]):.1f}° dari utara benar (arah barat laut), kira-kira {MQ.km(*MQ.ZONEINFO[code][1][0][1:3], *SL.KAABA):,.0f} km ke Kaabah.".replace(",", ".")
             + (f" Arah bagi {len(t0) - 1} bandar lain dalam zon ini disenaraikan di halaman." if len(t0) > 1 else "")),
        ]
        if vs:
            faq.append((f"Adakah waktu solat {t0[0]} sama dengan {cap}?",
                        f"Tidak semestinya. {t0[0]} dalam zon {code}, manakala {cap} dalam zon {capz}. {vs} Waktu berbeza kerana kedudukan matahari berubah mengikut longitud dan latitud."))
        answer = (f"Waktu solat {e(t0[0])} (zon {code}) hari ini, {P.dlong(day)}: <strong>Subuh {SL.hm(tt[1])}, Zohor {SL.hm(tt[3])}, Asar {SL.hm(tt[4])}, "
                  f"Maghrib {SL.hm(tt[5])} dan Isyak {SL.hm(tt[6])}</strong>. Imsak {SL.hm(tt[0])}, Syuruk {SL.hm(tt[2])}. Jadual yang sama digunakan di {e(area)}." + (f" {vs}" if vs else ""))
        title = fit("Waktu Solat {t} Hari Ini (" + code + ")", code, 70)
        desc = f"Waktu solat {tw} ({code}) hari ini, sebulan & setahun: Imsak, Subuh, Zohor, Asar, Maghrib, Isyak, kiraan ke waktu seterusnya dan kiblat setiap bandar."
        if len(desc) > 160:
            desc = f"Waktu solat {tname(code, 1)} ({code}) hari ini, sebulan & setahun: Subuh, Zohor, Asar, Maghrib, Isyak, kiraan ke waktu seterusnya dan arah kiblat."
        crumbs = [("Waktu Solat", "waktu-solat/"), (name, f"waktu-solat/{st}/"), (f"{code} {t0[0]}", None)]
        body = hero(f"Waktu Solat {e(tw)} Hari Ini ({code})",
                    f"Jadual {'rasmi JAKIM' if off else 'waktu solat'} zon {code}, {e(name)}: waktu hari ini, kiraan ke solat seterusnya, jadual sebulan dan setahun, serta arah kiblat setiap bandar dalam zon.",
                    crumbs)
        body += f'''<div class="wrap mn"><div class="ct">
{tool}

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {answer}</p></div>
{meta_line(T, TMS)}
{share(SITE + url, f"Waktu solat {tname(code, 1)} ({code}) hari ini:")}
</div>
</section>

<section id="bandar" aria-labelledby="h-bandar">
<h2 id="h-bandar">Bandar Dalam Zon {code} & Arah Kiblat</h2>
<p>Zon {code} meliputi <strong>{e(area)}</strong>. Semua bandar di bawah menggunakan waktu solat yang sama; arah kiblat dan jarak ke Kaabah dikira bagi setiap bandar (sudut dari utara benar, bulatan besar).</p>
{table(["Bandar", "Arah kiblat", "Jarak ke Kaabah", "Berhampiran"], town_rows(code), f"Bandar dalam zon {code}")}
<p class="note">Gunakan kompas telefon yang ditentukur atau <a href="{TBB}arah-kiblat/" rel="noopener">kompas kiblat ↗</a>. Sisihan sedikit (beberapa darjah) dimaafkan menurut jumhur ulama apabila arah sebenar sukar dipastikan.</p>
</section>
{ad(0)}
<section id="tahun" aria-labelledby="h-tahun">
<h2 id="h-tahun">Waktu Solat {e(t0[0])} Sepanjang {day.year}</h2>
<p>Julat waktu setiap bulan bagi zon {code} ({'jadual rasmi JAKIM' if off else 'kiraan anggaran'}). Subuh paling awal <strong>{SL.hm(e_sub[0])}</strong> ({dd(e_sub[1])}), paling lewat <strong>{SL.hm(l_sub[0])}</strong> ({dd(l_sub[1])}); Maghrib paling awal <strong>{SL.hm(e_mag[0])}</strong> ({dd(e_mag[1])}), paling lewat <strong>{SL.hm(l_mag[0])}</strong> ({dd(l_mag[1])}).</p>
<div class="tw" tabindex="0" role="region" aria-label="Waktu solat setiap bulan"><table class="plan">
<thead><tr><th scope="col">Bulan</th>{"".join(f'<th scope="col">{SL.NAMES[i]}</th>' for i in (1, 2, 3, 4, 5, 6))}</tr></thead>
<tbody>{"".join(yrows)}</tbody></table></div>
</section>

<section id="zon" aria-labelledby="h-zon">
<h2 id="h-zon">Zon Lain di {e(name)} Hari Ini</h2>
<p class="note">Waktu bagi <span id="sztd">{P.dlong(day)}</span>. {e(vs)} Klik kod zon untuk bertukar zon.</p>
<div class="tw" tabindex="0" role="region" aria-label="Waktu solat hari ini bagi setiap zon"><table class="plan szt" id="szt">
<thead><tr><th scope="col">Zon & kawasan</th><th scope="col">Subuh</th><th scope="col">Zohor</th><th scope="col">Asar</th><th scope="col">Maghrib</th><th scope="col">Isyak</th></tr></thead>
<tbody>{zrows}</tbody></table></div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Waktu Solat {e(t0[0])}</h2>
{faq_html(faq)}
</section>

<section id="pautan" aria-labelledby="h-pautan">
<h2 id="h-pautan">Berkaitan Zon {code}</h2>
<ul class="rel sts">
<li><a href="/{zpath("waktu-berbuka-puasa/", code)}">🌙 Waktu berbuka puasa & imsak {e(t0[0])}</a></li>
<li><a href="/cari-masjid/{MQ.ZONEINFO[code][0]}/">📍 Masjid & surau zon {code}</a></li>
<li><a href="/waktu-solat/{st}/">🕌 Semua zon {e(name)}</a></li>
<li><a href="/solat-sunat/solat-dhuha/">☀️ Waktu solat dhuha hari ini</a></li>
<li><a href="/solat-jamak-qasar/">🚗 Solat jamak & qasar (musafir)</a></li>
<li><a href="/kalendar-hijrah/">🗓 Kalendar Hijrah hari ini</a></li>
</ul>
<p class="note">Sumber: takwim waktu solat JAKIM (e-solat.gov.my), disegerakkan setiap bulan dan dibina semula setiap hari. <a href="/waktu-solat/#kaedah">Sumber & kaedah</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("waktu-solat/")}</section>
</div>
{side([("kira", "Waktu hari ini"), ("smon", "Jadual sebulan"), ("bandar", "Bandar & kiblat"), ("tahun", f"Sepanjang {day.year}"), ("zon", "Zon lain"), ("faq", "Soalan lazim")], "waktu-solat/")}
</div>'''
        pages.append(dict(path=url, kind="tool", data=False, arabic=False, nocache=True, extra_data=f'<script type="application/json" id="sd">{sdata}</script>',
                          title=title, ogtitle=f"Waktu Solat {tname(code, 2)} ({code})", desc=desc, og=OGS[0], ogcard=OGS[1],
                          crumbs=crumbs, body=body, faq=faq, about=[f"Waktu solat {t0[0]}", f"Zon {code}", name, "Solat"],
                          nodes=[place_node(SITE + url, code, name, area, lat, lng)], about_ref=SITE + url + "#zon",
                          llms=f"Waktu solat zon {code} ({area}, {name}) {'rasmi JAKIM' if off else 'kiraan anggaran'}. {mon}: Subuh {SL.hm(min(msub))}–{SL.hm(max(msub))}, Maghrib {SL.hm(min(mmag))}–{SL.hm(max(mmag))}. {day.year}: Subuh {SL.hm(e_sub[0])}–{SL.hm(l_sub[0])}. Kiblat {qb:.1f}°."))
    return pages


# ======================= WAKTU BERBUKA PUASA: one page per zone =======================
def build_ramadan_zones(ctx, AREA, day):
    T, TMS, share, ad = ctx["TODAY"], ctx["TODAYMS"], ctx["share"], ctx["ad"]
    s = R.season(day)
    y, yr, n = s["y"], s["start"].year, s["n"]
    eid = s["start"] + dt.timedelta(n)
    datenote = ("Tarikh mengikut takwim JAKIM. Tarikh rasmi tetap tertakluk kepada pengisytiharan Penyimpan Mohor Besar Raja-Raja."
                if s["official"] else
                "Tarikh jangkaan berdasarkan kiraan hisab dan kriteria imkanur rukyah (MABIMS). Tarikh rasmi diumumkan oleh Penyimpan Mohor Besar Raja-Raja selepas rukyah hilal pada petang 29 Syaaban.")
    pages = []
    for code, st, _, lat, lng in SL.ZONES:
        if not multi(st):
            continue
        slug, name, cap, capz = STATE[st]
        sz = [z for z in SL.ZONES if z[1] == st]
        url = zpath("waktu-berbuka-puasa/", code)
        go = {z[0]: "/" + zpath("waktu-berbuka-puasa/", z[0]) for z in sz if z[0] != code}
        tool, data, rows = ramadan_tool(sz, code, AREA, s, day, "puasa-z-" + code, name, go)
        t0 = towns(code)
        tw = tname(code, 3)
        area = AREA[code]
        mg = [r[2][5] for r in rows]
        im = [r[2][0] for r in rows]
        durs = [r[2][5] - r[2][1] for r in rows]
        n_off = sum(1 for _, d, _ in rows if R.official(code, d.year))
        sy_eid, _ = R.day_times(code, eid)
        lq = lailatul(s)
        # Lailatul Qadar nights start at Maghrib of the day before the Ramadan day (lailatul gives that date)
        lqrows = [[f"<strong>Malam {k} Ramadan</strong>", P.dlong(d), f"<strong>{SL.hm(R.day_times(code, d)[0][5])}</strong>", SL.hm(R.day_times(code, d)[0][6])] for k, d in lq]
        key = [
            ["<strong>1 Ramadan</strong> (puasa pertama)", P.dlong(rows[0][1]), SL.hm(rows[0][2][0]), f"<strong>{SL.hm(rows[0][2][5])}</strong>"],
            ["<strong>17 Ramadan</strong> (Nuzul Al-Quran)", P.dlong(rows[16][1]), SL.hm(rows[16][2][0]), f"<strong>{SL.hm(rows[16][2][5])}</strong>"],
            [f"<strong>{n} Ramadan</strong> (puasa terakhir{'' if s['official'] else ', jika genap 30'})", P.dlong(rows[-1][1]), SL.hm(rows[-1][2][0]), f"<strong>{SL.hm(rows[-1][2][5])}</strong>"],
        ]
        allz = {z[0]: R.timetable(z[0], s)[0] for z in sz}
        zrows = "".join(f'<tr data-z="{z[0]}"{TODAY_CLS if z[0] == code else ""}><th scope="row"><a href="#zon={z[0]}" data-zone="{z[0]}">{z[0]}</a>'
                        f'<span class="za">{zlink("waktu-berbuka-puasa/", z[0], code, AREA)}</span></th>'
                        f"<td>{SL.hm(allz[z[0]][0][2][0])}</td><td><strong>{SL.hm(allz[z[0]][0][2][5])}</strong></td>"
                        f"<td>{SL.hm(allz[z[0]][-1][2][0])}</td><td><strong>{SL.hm(allz[z[0]][-1][2][5])}</strong></td></tr>" for z in sz)
        dm = mg[0] - allz[capz][0][2][5]
        vs = ("" if code == capz else
              f"Pada 1 Ramadan, berbuka di zon {code} {'serentak dengan' if dm == 0 else (str(abs(dm)) + ' minit ' + ('lebih lewat daripada' if dm > 0 else 'lebih awal daripada'))} zon {capz} ({cap}).")
        jang = "" if s["official"] else " (jangkaan)"
        faq = [
            (f"Pukul berapa waktu berbuka puasa di {t0[0]} pada Ramadan {yr}?",
             f"Waktu berbuka (Maghrib) zon {code} ({t0[0]}) antara {SL.hm(min(mg))} dan {SL.hm(max(mg))} sepanjang Ramadan {y}H. Pada 1 Ramadan ({P.dlong(s['start'])}) berbuka pukul {SL.hm(mg[0])}."),
            (f"Bilakah waktu imsak di {t0[0]}?",
             f"Imsak zon {code} antara {SL.hm(min(im))} dan {SL.hm(max(im))} sepanjang Ramadan {y}H, iaitu 10 minit sebelum Subuh. Sahur mesti dihentikan sebelum masuk waktu Subuh."),
            (f"Berapa lama tempoh berpuasa di {t0[0]}?",
             f"Dari Subuh hingga Maghrib, kira-kira {min(durs) // 60} jam {min(durs) % 60} minit hingga {max(durs) // 60} jam {max(durs) % 60} minit sehari bagi zon {code} sepanjang Ramadan {y}H."),
            (f"Bilakah malam Lailatul Qadar di {t0[0]} pada {yr}?",
             f"Tarikhnya tidak diketahui dengan pasti; carilah pada malam ganjil 10 malam terakhir. Di zon {code}, malam 21 Ramadan bermula Maghrib {SL.hm(R.day_times(code, lq[0][1])[0][5])} pada {P.dlong(lq[0][1])}, dan malam 27 bermula Maghrib {SL.hm(R.day_times(code, lq[3][1])[0][5])} pada {P.dlong(lq[3][1])}."),
            (f"Pukul berapa syuruk pada pagi Hari Raya di {t0[0]}?",
             f"Pada 1 Syawal {y}H{jang} ({P.dlong(eid)}), Subuh zon {code} pukul {SL.hm(sy_eid[1])} dan syuruk {SL.hm(sy_eid[2])}. Solat sunat Aidilfitri bermula selepas matahari naik kira-kira segalah (lebih kurang 15–20 minit selepas syuruk); zakat fitrah afdal dibayar sebelumnya."),
        ]
        if vs:
            faq.append((f"Adakah waktu berbuka di {t0[0]} sama dengan {cap}?", f"{vs} Ikut zon tempat anda berada ketika berbuka, bukan zon tempat tinggal."))
        title = fit("Waktu Berbuka Puasa {t} " + str(yr) + " (" + code + ")", code, 70)
        desc = f"Waktu berbuka puasa & imsak {tw} ({code}) Ramadan {y}H/{yr}: jadual 30 hari, kiraan detik ke berbuka, malam Lailatul Qadar dan alarm kalendar."
        if len(desc) > 160:
            desc = f"Waktu berbuka puasa & imsak {tname(code, 1)} ({code}) Ramadan {yr}: jadual 30 hari, kiraan detik ke berbuka, malam Lailatul Qadar dan alarm kalendar."
        answer = (f"Di {e(t0[0])} (zon {code}), Ramadan {y}H {'bermula' if s['official'] else 'dijangka bermula'} {P.dlong(s['start'])} dengan "
                  f"<strong>imsak {SL.hm(im[0])} dan berbuka {SL.hm(mg[0])}</strong>. Sepanjang Ramadan, berbuka antara <strong>{SL.hm(min(mg))} dan {SL.hm(max(mg))}</strong>. "
                  f"Jadual yang sama digunakan di {e(area)}." + (f" {vs}" if vs else ""))
        crumbs = [("Waktu Berbuka Puasa", "waktu-berbuka-puasa/"), (name, f"waktu-berbuka-puasa/{st}/"), (f"{code} {t0[0]}", None)]
        body = hero(f"Waktu Berbuka Puasa {e(tw)} {yr} ({code})",
                    f"Jadual imsak dan berbuka Ramadan {y}H zon {code}, {e(name)}: kiraan detik ke berbuka, penanda puasa harian, alarm kalendar dan waktu malam-malam ganjil.",
                    crumbs)
        body += f'''<div class="wrap mn"><div class="ct">
{tool}

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {answer}</p></div>
{meta_line(T, TMS)}
{share(SITE + url, f"Waktu berbuka puasa {tname(code, 1)} ({code}) Ramadan {yr}:")}
<p class="note">{datenote}</p>
</div>
</section>

<section id="tarikh" aria-labelledby="h-tarikh">
<h2 id="h-tarikh">Tarikh Penting Ramadan {yr} di {e(t0[0])}</h2>
{table(["Hari", "Tarikh" + jang, "Imsak", "Berbuka"], key, f"Tarikh penting Ramadan zon {code}")}
<h3 id="lailatul-qadar">Malam Ganjil 10 Malam Terakhir (zon {code})</h3>
{table(["Malam", "Bermula", "Maghrib", "Isyak"], lqrows, f"Malam ganjil Ramadan zon {code}")}
<p class="note">1 Syawal {y}H{jang}: {P.dlong(eid)} · Subuh {SL.hm(sy_eid[1])} · Syuruk {SL.hm(sy_eid[2])}. Sumber waktu: {'jadual rasmi JAKIM' if n_off == len(rows) else ('kiraan anggaran parameter JAKIM, diganti jadual rasmi sebaik diterbitkan' if not n_off else 'jadual rasmi JAKIM dan kiraan anggaran')}.</p>
</section>
{ad(0)}
<section id="zon" aria-labelledby="h-zon">
<h2 id="h-zon">Zon Lain di {e(name)}: Imsak & Berbuka</h2>
<p class="note">Hari pertama dan terakhir Ramadan {y}H. {e(vs)}</p>
<div class="tw" tabindex="0" role="region" aria-label="Imsak dan berbuka setiap zon"><table class="plan szt" id="szt">
<thead><tr><th scope="col">Zon & kawasan</th><th scope="col">Imsak 1 Ramadan</th><th scope="col">Berbuka 1 Ramadan</th><th scope="col">Imsak {n} Ramadan</th><th scope="col">Berbuka {n} Ramadan</th></tr></thead>
<tbody>{zrows}</tbody></table></div>
</section>

<section class="dsec" id="niat" aria-labelledby="h-niat">
<h2 id="h-niat">🤲 Doa Berbuka Puasa</h2>
{"".join(card(i, t, e(ar), e(ru), e(mn), e(src), extra=note, cat="ramadan") for i, t, ar, ru, mn, src, note in I2.RAMADAN_DOA[2:3])}
<p class="note">Niat puasa, niat sebulan, doa Lailatul Qadar dan perkara yang membatalkan puasa: <a href="/waktu-berbuka-puasa/#niat">panduan Ramadan penuh</a>.</p>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Berbuka Puasa di {e(t0[0])}</h2>
{faq_html(faq)}
</section>

<section id="pautan" aria-labelledby="h-pautan">
<h2 id="h-pautan">Berkaitan Zon {code}</h2>
<ul class="rel sts">
<li><a href="/{zpath("waktu-solat/", code)}">🕌 Waktu solat {e(t0[0])} hari ini</a></li>
<li><a href="/cari-masjid/{MQ.ZONEINFO[code][0]}/">📍 Masjid & surau untuk tarawih</a></li>
<li><a href="/zakat-fitrah/{st}/">🌾 Zakat fitrah {e(name)}</a></li>
<li><a href="/solat-sunat/solat-tarawih/">🌙 Cara solat tarawih</a></li>
<li><a href="/jadual-khatam-al-quran/#hari=30">📅 Jadual khatam 30 hari</a></li>
<li><a href="/waktu-berbuka-puasa/{st}/">🗺 Semua zon {e(name)}</a></li>
</ul>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("waktu-berbuka-puasa/")}</section>
</div>
{side([("kira", "Jadual imsakiyah"), ("tarikh", "Tarikh penting"), ("lailatul-qadar", "Malam ganjil"), ("zon", "Zon lain"), ("niat", "Doa berbuka"), ("faq", "Soalan lazim")], "waktu-berbuka-puasa/")}
</div>'''
        pages.append(dict(path=url, kind="tool", data=False, arabic=True, published=PUB, nocache=True, extra_data=f'<script type="application/json" id="rd">{data}</script>',
                          title=title, ogtitle=f"Waktu Berbuka Puasa {tname(code, 2)} {yr}", desc=desc, og=OGR[0], ogcard=OGR[1],
                          crumbs=crumbs, body=body, faq=faq, about=[f"Ramadan {yr}", f"Waktu berbuka puasa {t0[0]}", f"Zon {code}", name],
                          nodes=[place_node(SITE + url, code, name, area, lat, lng)], about_ref=SITE + url + "#zon",
                          llms=f"Waktu berbuka puasa dan imsak zon {code} ({area}, {name}), Ramadan {y}H ({yr}): berbuka {SL.hm(min(mg))}–{SL.hm(max(mg))}, imsak {SL.hm(min(im))}–{SL.hm(max(im))}; 1 Ramadan {s['start'].isoformat()}{jang}."))
    return pages


def build_pages14(ctx):
    day = dt.date.fromisoformat(ctx.get("SOLAT_DAY") or ctx["TODAY"])
    AREA = areas()
    return build_solat_zones(ctx, AREA, day) + build_ramadan_zones(ctx, AREA, day)
