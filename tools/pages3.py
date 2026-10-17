"""Per-state prayer-time pages: /waktu-solat/<negeri>/. Each page carries its own official JAKIM data (every zone in the
state, today's times, the month for the capital zone) and month-specific facts, so no two pages share content."""
import json, os, calendar, datetime as dt
import solat as SL
import plans as P
from pages import e, faq_html, hero, side, meta_line, table, tool_cards, SITE, TBB

HB = ["Muharam", "Safar", "Rabiulawal", "Rabiulakhir", "Jamadilawal", "Jamadilakhir", "Rejab", "Syaaban", "Ramadan", "Syawal", "Zulkaedah", "Zulhijjah"]
API = "https://www.e-solat.gov.my/index.php?r=esolatApi/TakwimSolat&period=month&zone="


def load(zone, year):
    p = f"{P.REPO}/assets/data/solat/{zone}-{year}.json"
    return json.load(open(p)) if os.path.exists(p) else None


def areas():
    """Zone -> area wording, preferring JAKIM's own list when the sync saved it."""
    out = {z[0]: z[2] for z in SL.ZONES}
    p = f"{P.REPO}/assets/data/solat/zones.json"
    if os.path.exists(p):
        for x in json.load(open(p, encoding="utf8")):
            if x.get("jakimCode") in out and x.get("daerah"):
                out[x["jakimCode"]] = x["daerah"]
    return out


def state_links(skip=None):
    return '<ul class="rel sts">' + "".join(f'<li><a href="/waktu-solat/{s}/">Waktu Solat {e(n)}</a></li>' for s, n, _, _ in SL.STATES if s != skip) + "</ul>"


def build_state_pages(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    day = dt.date.fromisoformat(ctx.get("SOLAT_DAY") or T)
    share, ad = ctx["share"], ctx["ad"]
    doy = (day - dt.date(day.year, 1, 1)).days
    mon = f"{P.BLN[day.month - 1]} {day.year}"
    AREA = areas()
    pages = []
    for slug, name, cap, capz in SL.STATES:
        zones = [z for z in SL.ZONES if z[1] == slug and load(z[0], day.year)]
        if not zones:
            continue  # nothing official synced for this state yet
        data = {z[0]: load(z[0], day.year) for z in zones}
        cz = next((z for z in zones if z[0] == capz), zones[0])
        cd = data[cz[0]]
        url = f"waktu-solat/{slug}/"
        # the engine on this page offers the state's zones instead of towns
        cities = [[z[0], f"{z[0]} · {AREA[z[0]]}", name, z[3], z[4], z[0]] for z in zones]
        tt = cd["t"][doy]
        times = "".join(f'<li data-i="{i}"><span class="sn">{n}</span><span class="st">{SL.hm(tt[i])}</span></li>' for i, n in enumerate(SL.NAMES))
        dim = calendar.monthrange(day.year, day.month)[1]
        rows = []
        for k in range(1, dim + 1):
            r = cd["t"][doy - day.day + k]
            cls = ' class="today"' if k == day.day else ""
            rows.append(f'<tr{cls}><td>{k} {P.BLS[day.month - 1]}</td>' + "".join(f"<td>{SL.hm(x)}</td>" for x in r) + "</tr>")
        zrows = "".join(f'<tr data-z="{z[0]}"><th scope="row"><a href="#bandar={z[0]}" data-zone="{z[0]}">{z[0]}</a><span class="za">{e(AREA[z[0]])}</span></th>'
                        + "".join(f'<td data-k="{k}">{SL.hm(data[z[0]]["t"][doy][k])}</td>' for k in (1, 3, 4, 5, 6)) + "</tr>" for z in zones)
        opts = "".join(f'<option value="{c[0]}"{" selected" if c[0] == cz[0] else ""}>{e(c[1])}</option>' for c in cities)
        sdata = json.dumps({"api": API, "c": cities, "n": SL.NAMES, "fa": SL.FAJR, "is": SL.ISHA, "tz": SL.TZ, "hb": HB,
                            "def": cz[0], "key": "solat-" + slug}, ensure_ascii=False, separators=(",", ":"))
        # month facts (refreshed by the monthly sync)
        msub = [cd["t"][doy - day.day + k][1] for k in range(1, dim + 1)]
        mmag = [cd["t"][doy - day.day + k][5] for k in range(1, dim + 1)]
        today_sub = sorted((data[z[0]]["t"][doy][1], z[0]) for z in zones)
        today_mag = sorted((data[z[0]]["t"][doy][5], z[0]) for z in zones)
        spread = today_mag[-1][0] - today_mag[0][0]
        qb = SL.qibla(cz[3], cz[4])
        hij = cd["h"][doy] if cd.get("h") else ""
        hijs = ""
        if hij:
            hy, hmn, hd = map(int, hij.split("-"))
            hijs = f"{hd} {HB[hmn - 1]} {hy} H"
        many = len(zones) > 1
        zlist = ", ".join(f"{z[0]} ({AREA[z[0]]})" for z in zones)
        faq = [
            (f"Berapa zon waktu solat di {name}?",
             f"{name} mempunyai {len(zones)} zon waktu solat JAKIM: {zlist}." if many else
             f"{name} menggunakan satu zon waktu solat JAKIM, iaitu {cz[0]} ({AREA[cz[0]]})."),
            (f"Pukul berapa waktu Subuh di {cap} pada {mon}?",
             f"Pada {mon}, waktu Subuh bagi zon {cz[0]} ({cap}) antara {SL.hm(min(msub))} dan {SL.hm(max(msub))}. Imsak ialah 10 minit sebelum Subuh. Jadual harian penuh ada di atas."),
            (f"Bilakah waktu Maghrib (berbuka puasa) di {cap} pada {mon}?",
             f"Pada {mon}, waktu Maghrib bagi zon {cz[0]} ({cap}) antara {SL.hm(min(mmag))} dan {SL.hm(max(mmag))}."),
            (f"Ke arah mana kiblat dari {cap}?",
             f"Kiblat dari {cap} menghala {qb:.1f}° dari utara benar (arah barat laut)."),
        ]
        if many:
            faq.insert(1, (f"Kenapa waktu solat berbeza antara zon di {name}?",
                           f"Waktu solat bergantung pada kedudukan matahari, jadi zon di timur masuk waktu lebih awal. Pada {P.dlong(day)}, Maghrib paling awal di {name} ialah {SL.hm(today_mag[0][0])} (zon {today_mag[0][1]}) dan paling lewat {SL.hm(today_mag[-1][0])} (zon {today_mag[-1][1]}), beza {spread} minit."))
        answer = (f"Waktu solat {cap} hari ini ({P.dlong(day)}, zon {cz[0]}): <strong>Subuh {SL.hm(tt[1])}, Zohor {SL.hm(tt[3])}, Asar {SL.hm(tt[4])}, "
                  f"Maghrib {SL.hm(tt[5])} dan Isyak {SL.hm(tt[6])}</strong>. "
                  + (f"{name} mempunyai {len(zones)} zon JAKIM; pilih zon anda di bawah." if many else f"Seluruh {name} menggunakan zon {cz[0]}."))
        title = f"Waktu Solat {name} Hari Ini (Jadual Rasmi JAKIM)"
        if len(title) > 70:
            title = f"Waktu Solat {name} Hari Ini (JAKIM)"
        desc = (f"Waktu solat {name} hari ini dan sebulan bagi {len(zones)} zon JAKIM: Imsak, Subuh, Zohor, Asar, Maghrib, Isyak, kiraan ke waktu seterusnya dan arah kiblat."
                if many else f"Waktu solat {name} hari ini dan sebulan (zon {cz[0]}): Imsak, Subuh, Zohor, Asar, Maghrib, Isyak, kiraan ke waktu seterusnya dan arah kiblat.")
        if len(desc) > 160:
            desc = f"Waktu solat {name} hari ini bagi {len(zones)} zon JAKIM: Imsak, Subuh, Zohor, Asar, Maghrib, Isyak, jadual sebulan dan arah kiblat."
        body = hero(f"Waktu Solat {e(name)} Hari Ini",
                    f"Jadual rasmi JAKIM bagi {'semua ' + str(len(zones)) + ' zon' if many else 'zon ' + cz[0]} di {e(name)}: waktu hari ini, kiraan ke solat seterusnya dan jadual sebulan.",
                    [("Waktu Solat", "waktu-solat/"), (name, None)])
        body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira" class="sr">Waktu solat {e(name)}</h2>
<form class="frm" id="sf" novalidate>
<div class="fl w2"><label for="sc">Zon</label><select id="sc">{opts}</select></div>
</form>
<div class="act" id="sact"><button class="btn2" type="button" id="sgeo">📍 Zon terdekat saya</button><button class="btn2" type="button" data-act="link">🔗 Salin pautan</button><button class="btn2" type="button" data-act="print">🖨 Cetak jadual</button></div>
<div id="sw" class="sw">
<p class="sdate"><span id="sdate">{P.dlong(day)} · {e(cities[zones.index(cz)][1])}</span><br><span id="shij" class="shij">{e(hijs)}</span></p>
<ol class="stimes" id="stimes">{times}</ol>
<p class="snext" id="snext" aria-live="polite">&nbsp;</p>
<p class="ssrc" id="ssrc">Sumber: <strong>jadual rasmi JAKIM</strong>, zon {cz[0]} ({e(cd["src"])}).</p>
<p class="sqb">🧭 Arah kiblat: <strong id="sqib">{qb:.1f}°</strong> dari utara benar · <a href="{TBB}arah-kiblat/" rel="noopener">Kompas kiblat ↗</a></p>
</div>
<div class="tw" tabindex="0" role="region" aria-label="Jadual waktu solat sebulan"><table class="plan smon" id="smon">
<caption id="smcap">Jadual waktu solat {P.BLN[day.month - 1]} {day.year} – {e(cities[zones.index(cz)][1])}</caption>
<thead><tr><th scope="col">Tarikh</th>{"".join(f'<th scope="col">{n}</th>' for n in SL.NAMES)}</tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {answer}</p></div>
{meta_line(T, TMS)}
{share(SITE + url, f"Waktu solat {name} hari ini (jadual rasmi JAKIM):")}
</div>
</section>

<section id="zon" aria-labelledby="h-zon">
<h2 id="h-zon">{"Semua Zon Waktu Solat " + e(name) + " Hari Ini" if many else "Zon Waktu Solat " + e(name)}</h2>
<p class="note">Waktu bagi <span id="sztd">{P.dlong(day)}</span>. Klik kod zon untuk melihat jadual sebulan zon tersebut.</p>
<div class="tw" tabindex="0" role="region" aria-label="Waktu solat hari ini bagi setiap zon"><table class="plan szt" id="szt">
<thead><tr><th scope="col">Zon & kawasan</th><th scope="col">Subuh</th><th scope="col">Zohor</th><th scope="col">Asar</th><th scope="col">Maghrib</th><th scope="col">Isyak</th></tr></thead>
<tbody>{zrows}</tbody></table></div>
</section>
{ad(0)}
<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Waktu Solat {e(name)}</h2>
{faq_html(faq)}
</section>

<section id="negeri" aria-labelledby="h-negeri">
<h2 id="h-negeri">Waktu Solat Negeri Lain</h2>
{state_links(slug)}
<p class="note">Sumber: takwim waktu solat JAKIM (e-solat.gov.my), disegerakkan setiap bulan. <a href="/waktu-solat/#kaedah">Sumber & kaedah</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("waktu-solat/")}</section>
</div>
{side([("kira", "Waktu hari ini"), ("smon", "Jadual sebulan"), ("zon", "Semua zon" if many else "Zon"), ("faq", "Soalan lazim"), ("negeri", "Negeri lain")], "waktu-solat/")}
</div>'''
        pages.append(dict(path=url, kind="tool", data=False, arabic=False, extra_data=f'<script type="application/json" id="sd">{sdata}</script>',
                          title=title, ogtitle=f"Waktu Solat {name} Hari Ini", desc=desc,
                          crumbs=[("Waktu Solat", "waktu-solat/"), (name, None)], body=body, faq=faq,
                          about=[f"Waktu solat {name}", name, "Solat"], og=f"waktu-solat-{slug}",
                          llms=f"Waktu solat rasmi JAKIM bagi {name}: {len(zones)} zon ({zlist}). {mon}: Subuh {cap} {SL.hm(min(msub))}–{SL.hm(max(msub))}, Maghrib {SL.hm(min(mmag))}–{SL.hm(max(mmag))}. Kiblat {qb:.1f}°."))
    return pages
