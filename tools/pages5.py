"""Masjid & surau finder: /cari-masjid/ (hub, nearest mosque from the visitor's location) and one page per JAKIM zone
(/cari-masjid/<slug>/) with that zone's official prayer times and its mosques from OpenStreetMap (tools/masjid.py).
A zone page is indexed only once its OSM data has been synced; until then it is noindex and only offers the live search."""
import json, re, datetime as dt
import solat as SL
import masjid as M
import ramadan as R
import plans as P
from pages import e, faq_html, hero, side, meta_line, tool_cards, SITE
from pages3 import areas

HUB = "cari-masjid/"
API = "https://www.e-solat.gov.my/index.php?r=esolatApi/TakwimSolat&period=month&zone="
OSM_CREDIT = ('Data masjid & surau © <a href="https://www.openstreetmap.org/copyright" rel="noopener">penyumbang OpenStreetMap</a>, '
              'lesen <abbr title="Open Database License">ODbL</abbr>')
LIST_MAX = 60  # places pre-rendered per zone page (the live search covers the rest)
LD_MAX = 30   # places in the JSON-LD ItemList


TODAY_CLS = ' class="today"'


def anchor_id(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def zcount(d):
    return f' <span class="za">{total(d)} tempat</span>' if d else ""


def url_of(z):
    return f"{HUB}{M.ZONEINFO[z][0]}/"


def short(z, n=2):
    return ", ".join(a[0] for a in M.ZONEINFO[z][1][:n])


def total(d):
    return sum(d["n"].values()) if d else 0


def kinds(d):
    n = d["n"]
    parts = [f"{n['m']} masjid", f"{n['s']} surau"] + ([f"{n['t']} tempat solat lain"] if n["t"] else [])
    return ", ".join(parts[:-1]) + " dan " + parts[-1]


def kmf(x):
    return f"{x:.1f}".replace(".", ",") + " km"


def item_html(r, la, ln, where=""):
    name, k, lat, lng, addr, ref, x = r[:7]
    links = [f'<a href="{M.dir_url(lat, lng)}" rel="noopener nofollow">Arah</a>', f'<a href="{M.osm_url(ref)}" rel="noopener">Peta OSM</a>']
    if x.get("w"):
        links.append(f'<a href="{e(x["w"])}" rel="noopener nofollow ugc">Laman web</a>')
    if x.get("p"):
        links.append(f'<a href="tel:{e(x["p"].replace(" ", ""))}">{e(x["p"])}</a>')
    return (f'<li class="mq" data-lat="{lat}" data-lng="{lng}"><span class="mk {k}">{M.KIND[k]}</span><strong class="mqn">{e(name)}</strong>'
            f'<span class="mqd">{kmf(M.km(la, ln, lat, lng))} dari {e(where)}{" · ♿ akses OKU" if x.get("a") else ""}</span>'
            + (f'<span class="mqa">{e(addr)}</span>' if addr else "") + f'<span class="mql">{" · ".join(links)}</span></li>')


def ld_place(r, state, zone_id):
    name, k, lat, lng, addr, ref, x = r[:7]
    o = {"@type": "Mosque" if k == "m" else "PlaceOfWorship", "name": name,
         "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
         "address": {"@type": "PostalAddress", "addressRegion": state, "addressCountry": "MY"},
         "hasMap": M.osm_url(ref), "containedInPlace": {"@id": zone_id}}
    if addr:
        o["address"]["streetAddress"] = addr
    if x.get("w"):
        o["url"] = x["w"]
    if x.get("p"):
        o["telephone"] = x["p"]
    if x.get("a"):
        o["amenityFeature"] = {"@type": "LocationFeatureSpecification", "name": "Akses kerusi roda", "value": True}
    return o


def times_li(t):
    return "".join(f'<li data-i="{i}"><span class="sn">{n}</span><span class="st">{SL.hm(t[i])}</span></li>' for i, n in enumerate(SL.NAMES))


def js_data(z=None):
    """What alat.js needs: zone (for today's times), and every town anchor so it can tell visitors which zone they are in."""
    an = [[zz, a[1], a[2]] for zz, (_, aa) in M.ZONEINFO.items() for a in aa if len(a) < 4]
    zs = {zz: ["/" + url_of(zz), short(zz)] for zz in M.ZONEINFO}
    d = {"an": an, "zs": zs, "n": SL.NAMES}
    if z:
        zi = next(q for q in SL.ZONES if q[0] == z)
        d.update(z=z, lat=zi[3], lng=zi[4], api=API)
    return f'<script type="application/json" id="md">{json.dumps(d, ensure_ascii=False, separators=(",", ":"))}</script>'


def near_tool(lead, cls="mnear"):
    return f'''<div class="{cls}">
<h3 id="h-dekat">📍 Masjid & surau terdekat dengan anda</h3>
<p class="note">{lead}</p>
<div class="act"><button class="btn3" type="button" id="mgeo">📍 Cari dari lokasi saya</button></div>
<p class="note" id="mstat" aria-live="polite">Lokasi anda hanya digunakan dalam pelayar untuk satu carian OpenStreetMap; ia tidak disimpan oleh kami.</p>
<ol class="mql2" id="mres"></ol>
</div>'''


def build_masjid_pages(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    day = dt.date.fromisoformat(ctx.get("SOLAT_DAY") or T)
    share, ad = ctx["share"], ctx["ad"]
    AREA = areas()
    D = {z: M.load(z) for z in M.ZONEINFO}
    synced = [z for z in M.ZONEINFO if D[z]]
    pages = []

    # ---------------- one page per zone ----------------
    for code, slug_state, _, zlat, zlng in SL.ZONES:
        state = M.STATE_NAME[slug_state]
        slug, anc = M.ZONEINFO[code]
        d = D[code]
        url = url_of(code)
        zid = SITE + url + "#zon"
        town0 = anc[0][0]
        n = total(d)
        t, off = R.day_times(code, day)
        week = [(day + dt.timedelta(i),) + R.day_times(code, day + dt.timedelta(i)) for i in range(7)]
        src = f"jadual rasmi JAKIM (e-solat.gov.my), zon {code}" if off else f"kiraan anggaran parameter JAKIM, zon {code}"
        qb = SL.qibla(zlat, zlng)

        # mosque list, grouped by town
        listed, groups = [], []
        if d:
            per = max(4, LIST_MAX // max(1, sum(1 for tw in d["towns"] if tw["m"])))
            for tw, (tn, la, ln, *_) in zip(d["towns"], anc):
                if not tw["m"]:
                    continue
                rows = tw["m"][:per]
                listed += rows
                groups.append(f'<h3 id="dekat-{anchor_id(tn)}">Masjid & surau berhampiran {e(tn)}</h3>'
                              f'<p class="note">{tw["n"]} tempat solat dipetakan paling hampir dengan {e(tn)} dalam zon {code}'
                              + (f"; {len(rows)} paling dekat disenaraikan." if tw["n"] > len(rows) else ".") + "</p>"
                              f'<ol class="mql2">{"".join(item_html(r, la, ln, "pusat " + tn) for r in rows)}</ol>')
            if d["near"]:
                la, ln = anc[0][1], anc[0][2]
                groups.append(f'<h3 id="luar-zon">Terdekat di luar zon {code}</h3><p class="note">Zon {code} kecil, jadi berikut tempat solat terdekat '
                              f'dalam lingkungan 30 km (zon waktu solatnya dinyatakan).</p><ol class="mql2">'
                              + "".join(item_html(r, la, ln, f"{town0} · zon {r[7]}") for r in d["near"]) + "</ol>")
                listed += d["near"]
        indexed = bool(d) and len(listed) >= 3

        # nearest to the main town, for the short answer and FAQ
        top = sorted(((M.km(anc[0][1], anc[0][2], r[2], r[3]), r) for r in listed), key=lambda x: x[0])[:3]
        mfrom, mto = min(w[1][5] for w in week), max(w[1][5] for w in week)
        tline = f"Subuh {SL.hm(t[1])}, Zohor {SL.hm(t[3])}, Asar {SL.hm(t[4])}, Maghrib {SL.hm(t[5])} dan Isyak {SL.hm(t[6])}"
        if d and n:
            answer = (f"OpenStreetMap memetakan <strong>{n} tempat solat dalam zon {code}</strong> ({e(kinds(d))}). "
                      + (f"Yang paling dekat dengan pusat {e(town0)} ialah <strong>{e(top[0][1][0])}</strong> ({kmf(top[0][0])}). " if top else "")
                      + f"Waktu solat zon {code} pada {P.dlong(day)}: <strong>{tline}</strong>.")
        elif d:
            answer = (f"Belum ada masjid atau surau dipetakan di OpenStreetMap dalam zon {code}. "
                      + (f"Yang terdekat ialah <strong>{e(top[0][1][0])}</strong> ({kmf(top[0][0])} dari {e(town0)}). " if top else "")
                      + f"Waktu solat zon {code} pada {P.dlong(day)}: <strong>{tline}</strong>.")
        else:
            answer = (f"Senarai masjid zon {code} sedang dikemas kini daripada OpenStreetMap. Tekan “Cari dari lokasi saya” untuk carian terus. "
                      f"Waktu solat zon {code} pada {P.dlong(day)}: <strong>{tline}</strong>.")

        faq = []
        if d and n:
            faq.append((f"Berapa banyak masjid dan surau di {short(code, 3)}?",
                        f"OpenStreetMap memetakan {n} tempat solat dalam zon {code} ({kinds(d)}) setakat {d['fetched']}. Jumlah sebenar mungkin lebih tinggi kerana "
                        "tidak semua surau telah dipetakan; senarai ini dikemas kini setiap bulan."))
        if top:
            faq.append((f"Masjid manakah yang paling dekat dengan pusat {town0}?",
                        "Mengikut jarak garis lurus dari pusat " + town0 + ": " + "; ".join(f"{r[0]} ({kmf(x)})" for x, r in top)
                        + ". Tekan butang lokasi untuk masjid terdekat dari tempat anda berada."))
        faq += [
            (f"Pukul berapa waktu solat di zon {code} hari ini?",
             f"Pada {P.dlong(day)}, waktu solat zon {code} ({AREA[code]}): Imsak {SL.hm(t[0])}, {tline}. Sumber: {src}."),
            ("Bagaimana mencari masjid terdekat dari lokasi saya?",
             "Tekan “Cari dari lokasi saya” dan benarkan akses lokasi. Pelayar anda menghantar koordinat sekali sahaja kepada pelayan Overpass "
             "OpenStreetMap untuk mencari masjid dan surau dalam lingkungan 3 km (diperluas jika tiada), kemudian menyusunnya mengikut jarak. Kami tidak menyimpan lokasi anda."),
            ("Masjid atau surau saya tiada dalam senarai. Bagaimana menambahnya?",
             "Senarai ini datang daripada OpenStreetMap, peta dunia yang dikemas kini oleh sukarelawan. Daftar akaun percuma di openstreetmap.org, tandakan bangunan "
             "sebagai tempat ibadat (agama Islam) dan isi namanya. Perubahan akan muncul di sini selepas kemas kini bulanan seterusnya."),
            ("Apakah beza masjid dan surau?",
             "Di Malaysia, masjid ialah tempat solat yang diiktiraf oleh majlis agama Islam negeri untuk mendirikan solat Jumaat. Surau (musolla) ialah tempat solat "
             "berjemaah yang lebih kecil, biasanya tanpa solat Jumaat kecuali dengan kebenaran pihak berkuasa agama negeri."),
            (f"Ke arah mana kiblat dari {town0}?", f"Kiblat dari {town0} menghala {qb:.1f}° dari utara benar (arah barat laut)."),
        ]

        name3 = short(code, 3)
        title = f"Masjid & Surau {name3} ({code}) + Waktu Solat"
        for k in (2, 1):
            if len(title) > 70:
                title = f"Masjid & Surau {short(code, k)} ({code}) + Waktu Solat"
        if len(title) > 70:
            title = f"Masjid & Surau {short(code, 1)} ({code})"
        sname = short(code, 2)
        desc = (f"{n} masjid & surau di {sname} dan sekitar (zon {code}, {state}): alamat, peta, arah dan waktu solat rasmi JAKIM hari ini."
                if n else f"Masjid & surau di {sname} (zon {code}, {state}): carian terdekat dari lokasi anda, peta, arah dan waktu solat rasmi JAKIM hari ini.")
        if len(desc) > 160:
            desc = f"Masjid & surau di {short(code, 1)} (zon {code}): alamat, peta, arah dan waktu solat rasmi JAKIM hari ini."
        others = [z[0] for z in SL.ZONES if z[1] == slug_state and z[0] != code]
        wrows = "".join(f'<tr{TODAY_CLS if i == 0 else ""}><td>{P.dshort(w[0])}</td>' + "".join(f"<td>{SL.hm(x)}</td>" for x in w[1]) + "</tr>" for i, w in enumerate(week))

        body = hero(f"Masjid & Surau di {e(name3)} ({code})",
                    f"Senarai masjid dan surau zon {code} ({e(AREA[code])}, {e(state)}) dengan alamat, peta dan arah, serta waktu solat rasmi JAKIM hari ini.",
                    [("Cari Masjid & Surau", HUB), (f"{code} · {sname}", None)])
        body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira">Waktu Solat Zon {code} Hari Ini</h2>
<div id="mw" class="sw">
<p class="sdate" id="mdate">{P.dlong(day)} · {code} · {e(AREA[code])}</p>
<ol class="stimes" id="mtimes">{times_li(t)}</ol>
<p class="snext" id="mnext" aria-live="polite">&nbsp;</p>
<p class="ssrc" id="msrc">Sumber: <strong>{src}</strong>. Jadual sebulan: <a href="/waktu-solat/{slug_state}/#bandar={code}">Waktu Solat {e(state)} ›</a></p>
</div>
{near_tool(f"Cari masjid dan surau paling hampir dari tempat anda sekarang, disusun mengikut jarak, dengan pautan arah.")}
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {answer}</p></div>
{meta_line(T, TMS)}
{share(SITE + url, f"Masjid & surau di {sname} ({code}) + waktu solat hari ini:")}
</div>
</section>

<section id="senarai" aria-labelledby="h-senarai">
<h2 id="h-senarai">Senarai Masjid & Surau Zon {code}</h2>
{"".join(groups) if groups else '<p>Senarai zon ini sedang disegerakkan daripada OpenStreetMap. Gunakan carian lokasi di atas buat masa ini.</p>'}
<p class="osm">{OSM_CREDIT}{f", dikemas kini {d['fetched']}" if d else ""}. Jarak ialah garis lurus, bukan jarak jalan. Tiada dalam senarai atau maklumat salah?
<a href="https://www.openstreetmap.org/edit#map=14/{zlat:.4f}/{zlng:.4f}" rel="noopener">Tambah atau betulkan di OpenStreetMap</a>.</p>
</section>

<section id="minggu" aria-labelledby="h-minggu">
<h2 id="h-minggu">Waktu Solat Zon {code} 7 Hari</h2>
<div class="tw" tabindex="0" role="region" aria-label="Waktu solat 7 hari"><table class="plan smon">
<caption>Waktu solat zon {code} ({e(AREA[code])}) mulai {P.dlong(day)}</caption>
<thead><tr><th scope="col">Tarikh</th>{"".join(f'<th scope="col">{x}</th>' for x in SL.NAMES)}</tr></thead>
<tbody>{wrows}</tbody></table></div>
<p class="note">Maghrib minggu ini antara {SL.hm(mfrom)} dan {SL.hm(mto)}. Jadual sebulan, semua zon dan arah kiblat: <a href="/waktu-solat/{slug_state}/#bandar={code}">Waktu Solat {e(state)}</a> · <a href="/waktu-solat/">Waktu Solat Malaysia</a>.</p>
</section>
{ad(0)}
<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Masjid & Surau {e(sname)}</h2>
{faq_html(faq)}
</section>

<section id="zon-lain" aria-labelledby="h-zl">
<h2 id="h-zl">{"Zon Lain di " + e(state) if others else "Negeri Lain"}</h2>
<ul class="rel sts">{"".join(f'<li><a href="/{url_of(z)}">{z} · {e(short(z))}</a></li>' for z in others) if others else "".join(f'<li><a href="/{url_of(st[3])}">{e(st[1])}</a></li>' for st in SL.STATES if st[0] != slug_state)}</ul>
<p class="note"><a href="/{HUB}">Semua 60 zon JAKIM</a> · Ramadan: <a href="/waktu-berbuka-puasa/{slug_state}/">waktu berbuka puasa {e(state)}</a> · <a href="/belajar-solat/">Cara solat lengkap</a></p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(HUB)}</section>
</div>
{side([("kira", "Waktu solat hari ini"), ("h-dekat", "Terdekat dengan saya"), ("senarai", "Senarai masjid & surau"), ("minggu", "Waktu solat 7 hari"), ("faq", "Soalan lazim"), ("zon-lain", "Zon lain")], HUB)}
</div>'''
        place = {"@type": "Place", "@id": zid, "name": f"Zon waktu solat {code}: {AREA[code]}",
                 "geo": {"@type": "GeoCoordinates", "latitude": zlat, "longitude": zlng},
                 "hasMap": f"https://www.openstreetmap.org/#map=12/{zlat:.4f}/{zlng:.4f}",
                 "containedInPlace": {"@type": "State", "name": state, "containedInPlace": {"@type": "Country", "name": "Malaysia"}}}
        pages.append(dict(path=url, kind="tool", data=False, arabic=False, noindex=not indexed, nocache=True, schema="CollectionPage",
                          extra_data=js_data(code), title=title, ogtitle=f"Masjid & Surau {sname} ({code})", desc=desc,
                          og="cari-masjid", ogcard=("Cari Masjid & Surau Terdekat", "Masjid dan surau setiap zon JAKIM dengan waktu solat rasmi hari ini."),
                          crumbs=[("Cari Masjid & Surau", HUB), (f"{code} · {sname}", None)], body=body, faq=faq,
                          about=[f"Masjid di {sname}", f"Surau di {sname}", f"Waktu solat {code}"], about_ref=zid, nodes=[place],
                          itemlist=dict(name=f"Masjid & surau zon {code}",
                                        items=[{"@type": "ListItem", "position": i, "item": ld_place(r, state, zid)} for i, r in enumerate(listed[:LD_MAX], 1)]) if listed else None,
                          llms=f"Zon {code} ({AREA[code]}, {state}): " + (f"{n} tempat solat di OpenStreetMap ({kinds(d)}); terdekat dengan {town0}: {top[0][1][0]}. " if d and n and top else "")
                               + f"Waktu solat rasmi JAKIM hari ini dan 7 hari; carian masjid terdekat dari lokasi."))

    # ---------------- hub ----------------
    nall = sum(total(D[z]) for z in synced)
    srows = []
    for slug_state, state, _, _ in SL.STATES:
        zs = [z[0] for z in SL.ZONES if z[1] == slug_state]
        cnt = sum(total(D[z]) for z in zs)
        srows.append(f'<tr><th scope="row"><a href="/waktu-solat/{slug_state}/">{e(state)}</a></th><td><ul class="mzl">'
                     + "".join(f'<li><a href="/{url_of(z)}">{z} · {e(short(z))}</a>{zcount(D[z])}</li>' for z in zs)
                     + f'</ul></td><td>{cnt if cnt else "–"}</td></tr>')
    hfaq = [
        ("Bagaimana mencari masjid terdekat dari lokasi saya?",
         "Tekan “Cari dari lokasi saya” dan benarkan akses lokasi. Senarai masjid dan surau dalam lingkungan 3 km (diperluas hingga 25 km jika tiada) dipaparkan mengikut jarak, "
         "bersama pautan arah. Zon waktu solat JAKIM anda juga dikenal pasti."),
        ("Dari mana data masjid dan surau ini?",
         "Daripada OpenStreetMap (© penyumbang OpenStreetMap, lesen ODbL), peta terbuka yang dikemas kini oleh sukarelawan. Senarai setiap zon disegerakkan setiap bulan, "
         "manakala carian lokasi bertanya terus kepada pelayan Overpass OpenStreetMap."),
        ("Adakah waktu solat di halaman zon rasmi?",
         "Ya. Waktu solat diambil daripada takwim JAKIM (e-solat.gov.my) bagi zon tersebut dan disegerakkan setiap bulan. Jika takwim belum tersedia, halaman menyatakan bahawa ia kiraan anggaran."),
        ("Berapa zon waktu solat di Malaysia?",
         f"JAKIM membahagikan Malaysia kepada {len(SL.ZONES)} zon waktu solat. Setiap zon ada halaman masjid dan surau sendiri di bawah."),
        ("Masjid saya tiada dalam senarai. Bagaimana menambahnya?",
         "Tambahkannya di openstreetmap.org (akaun percuma): tandakan sebagai tempat ibadat, agama Islam, dan isi nama rasmi masjid atau surau. Ia akan muncul di sini selepas kemas kini bulanan."),
    ]
    body = hero("Cari Masjid & Surau Terdekat",
                f"Masjid dan surau berhampiran anda dan di setiap {len(SL.ZONES)} zon waktu solat JAKIM, dengan alamat, peta, arah dan waktu solat rasmi hari ini.",
                [("Cari Masjid & Surau", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira" class="sr">Cari masjid terdekat</h2>
{near_tool(cls="mnear top", lead="Senarai disusun mengikut jarak dari tempat anda, dengan pautan arah Google Maps dan peta OpenStreetMap. Zon waktu solat JAKIM anda juga dipaparkan.")}
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Tekan <strong>“Cari dari lokasi saya”</strong> untuk senarai masjid dan surau terdekat mengikut jarak, atau pilih zon JAKIM anda di bawah. '''
    body += (f"Halaman zon menyenaraikan {nall:,} tempat solat yang dipetakan di OpenStreetMap bersama waktu solat rasmi JAKIM zon tersebut." if nall else
             "Setiap halaman zon memaparkan masjid dan surau zon itu bersama waktu solat rasmi JAKIM.")
    body += f'''</p></div>
{meta_line(T, TMS)}
{share(SITE + HUB, "Cari masjid & surau terdekat + waktu solat hari ini:")}
</div>
</section>

<section id="zon" aria-labelledby="h-zon">
<h2 id="h-zon">Masjid & Surau Ikut Zon Waktu Solat JAKIM</h2>
<div class="tw" tabindex="0" role="region" aria-label="Zon waktu solat mengikut negeri"><table class="plan mzt">
<thead><tr><th scope="col">Negeri</th><th scope="col">Zon</th><th scope="col">Tempat solat</th></tr></thead>
<tbody>{"".join(srows)}</tbody></table></div>
<p class="osm">{OSM_CREDIT}. Waktu solat: takwim JAKIM (e-solat.gov.my). <a href="/waktu-solat/">Waktu solat hari ini ›</a></p>
</section>
{ad(0)}
<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim</h2>
{faq_html(hfaq)}
</section>
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(HUB)}</section>
</div>
{side([("kira", "Terdekat dengan saya"), ("zon", "Ikut zon JAKIM"), ("faq", "Soalan lazim")], HUB)}
</div>'''
    pages.insert(0, dict(path=HUB, kind="tool", data=False, arabic=False, extra_data=js_data(),
                         title="Cari Masjid & Surau Terdekat (60 Zon JAKIM) + Waktu Solat",
                         ogtitle="Cari Masjid & Surau Terdekat", og="cari-masjid",
                         ogcard=("Cari Masjid & Surau Terdekat", "Masjid dan surau setiap zon JAKIM dengan waktu solat rasmi hari ini."),
                         desc=f"Cari masjid dan surau terdekat dari lokasi anda atau ikut {len(SL.ZONES)} zon JAKIM: alamat, peta, arah dan waktu solat rasmi hari ini. Data OpenStreetMap.",
                         crumbs=[("Cari Masjid & Surau", None)], body=body, faq=hfaq, about=["Masjid", "Surau", "Waktu solat"],
                         itemlist=dict(name="Masjid & surau ikut zon waktu solat JAKIM",
                                       items=[{"@type": "ListItem", "position": i, "name": f"Masjid & surau zon {z}: {short(z)}", "url": SITE + url_of(z)}
                                              for i, z in enumerate((q[0] for q in SL.ZONES), 1)]),
                         app=dict(name="Pencari Masjid & Surau", features=["Masjid dan surau terdekat dari lokasi anda", f"Halaman bagi setiap {len(SL.ZONES)} zon waktu solat JAKIM",
                                                                          "Pautan arah dan peta", "Waktu solat rasmi JAKIM hari ini"]),
                         llms=f"Pencari masjid dan surau: carian terdekat dari lokasi (OpenStreetMap/Overpass) dan satu halaman bagi setiap {len(SL.ZONES)} zon JAKIM dengan waktu solat rasmi."))
    return pages

