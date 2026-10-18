"""Pages: /waktu-berbuka-puasa/ (+ one per state), /belajar-solat/, /belajar-iqra/, /belajar-mengaji/ (same page-dict contract as pages.py).
Every tool renders its default state at build time with the same markup assets/js/alat.js produces (tools/test-alat.mjs checks)."""
import json, math, datetime as dt
import ibadah2 as I2
import ramadan as R
import solat as SL
import plans as P
from pages import e, faq_html, hero, side, meta_line, table, tool_cards, SITE, TBB
from pages2 import card, ayah, quran_block, qref
from pages3 import areas

PUB = "2026-10-18"
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# ======================= RAMADAN =======================
def r_row(k, d, t, s, today):
    star = ' <span class="lq" title="Malam ganjil 10 terakhir">★</span>' if k >= 21 and k % 2 else ""
    mark = "*" if k == 30 and not s["official"] else ""
    cls = ' class="today"' if d == today else ""
    return (f'<tr data-d="{k}"{cls}><td>{k}{mark}{star}</td><td>{P.dshort(d)}</td>' + "".join(f"<td>{SL.hm(t[i])}</td>" for i in (0, 1, 3, 4))
            + f'<td><strong>{SL.hm(t[5])}</strong></td><td>{SL.hm(t[6])}</td><td>{R.dur(t)}</td>'
            f'<td><input type="checkbox" data-r="{k}" aria-label="Puasa hari ke-{k} selesai"></td></tr>')


def r_src(n_off, n, zone):
    if n_off == n:
        return f"Sumber: <strong>jadual rasmi JAKIM</strong>, zon {zone}."
    if n_off == 0:
        return (f"Sumber: <strong>kiraan anggaran</strong> parameter JAKIM bagi zon {zone} (biasanya dalam lingkungan 1–2 minit). "
                "Jadual rasmi JAKIM menggantikannya secara automatik sebaik sahaja diterbitkan.")
    return f"Sumber: <strong>jadual rasmi JAKIM</strong> bagi {n_off} hari, selebihnya kiraan anggaran, zon {zone}."


def r_phase(s, d):
    end = s["start"] + dt.timedelta(s["n"])
    if d < s["start"]:
        k = (s["start"] - d).days
        return f'🌙 Ramadan {s["y"]}H {"bermula" if s["official"] else "dijangka bermula"} <strong>{P.dlong(s["start"])}</strong> · lagi {k} hari'
    if d < end:
        return f'🌙 Hari ke-{(d - s["start"]).days + 1} Ramadan {s["y"]}H · {P.dlong(d)}'
    return f'🌙 Ramadan {s["y"]}H telah berakhir. Selamat Hari Raya Aidilfitri, maaf zahir dan batin.'


def r_today(t):
    return "".join(f'<li><span>{n}</span><strong>{SL.hm(t[i])}</strong></li>' for i, n in ((0, "Imsak"), (1, "Subuh"), (5, "Maghrib"), (6, "Isyak")))


def lailatul(s):
    return [(k, s["start"] + dt.timedelta(k - 2)) for k in (21, 23, 25, 27, 29)]


def ramadan_tool(zones, defz, AREA, s, day, key, state_name=None):
    """The shared timetable tool: zone picker, status + countdown, 30-day imsakiyah with fasting tracker."""
    rows, _ = R.timetable(defz, s)
    n_off = sum(1 for _, d, _ in rows if R.official(defz, d.year))
    tt, _ = R.day_times(defz, day)
    label = f"{defz} · {AREA[defz]}"
    if state_name:
        opts = "".join(f'<option value="{z[0]}"{" selected" if z[0] == defz else ""}>{e(z[0] + " · " + AREA[z[0]])}</option>' for z in zones)
    else:
        groups = {}
        for z in zones:
            groups.setdefault(z[1], []).append(z)
        names = {st: n for st, n, _, _ in SL.STATES}
        opts = "".join(f'<optgroup label="{e(names[st])}">' + "".join(f'<option value="{z[0]}"{" selected" if z[0] == defz else ""}>{e(z[0] + " · " + AREA[z[0]])}</option>' for z in zs) + "</optgroup>" for st, zs in groups.items())
    yr = s["start"].year
    note30 = "" if s["official"] else "* Hari ke-30 hanya jika anak bulan Syawal tidak kelihatan pada petang 29 Ramadan. "
    data = J({"y": s["y"], "start": s["start"].isoformat(), "n": s["n"], "off": s["official"], "def": defz, "key": key,
              "z": [[z[0], z[1], AREA[z[0]], z[3], z[4]] for z in zones], "fa": SL.FAJR, "is": SL.ISHA, "tz": SL.TZ})
    html = f'''<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira" class="sr">Jadual waktu berbuka puasa dan imsak</h2>
<form class="frm" id="rf" novalidate>
<div class="fl w2"><label for="rz">Zon waktu solat JAKIM</label><select id="rz">{opts}</select></div>
</form>
<div class="rst" id="rst">
<p class="rph" id="rph">{r_phase(s, day)}</p>
<p class="rcd" id="rcd" aria-live="polite">&nbsp;</p>
<p class="rtl"><span id="rtdl">Hari ini, {P.dlong(day)}</span> · <span id="rzl">{e(label)}</span></p>
<ul class="rtd" id="rtd">{r_today(tt)}</ul>
</div>
<div class="act" id="ract"><button class="btn2" type="button" id="rgeo">📍 Zon terdekat saya</button><button class="btn2" type="button" data-ics="b" title="Muat turun fail kalendar (.ics) dengan peringatan 10 minit sebelum berbuka">📅 Alarm berbuka</button><button class="btn2" type="button" data-ics="bi" title="Fail kalendar (.ics): peringatan berbuka dan 30 minit sebelum imsak">⏰ Alarm berbuka + imsak</button><button class="btn2" type="button" data-act="link">🔗 Salin pautan</button><button class="btn2" type="button" data-act="print">🖨 Cetak</button></div>
<p class="ssrc" id="rsrc">{r_src(n_off, len(rows), defz)}</p>
<p class="prog" id="rprog"></p>
<div class="tw" tabindex="0" role="region" aria-label="Jadual imsakiyah Ramadan"><table class="plan rmt" id="rmt">
<caption id="rcap">Jadual imsakiyah Ramadan {s["y"]}H ({yr}) – {e(label)}</caption>
<thead><tr><th scope="col">Puasa</th><th scope="col">Tarikh</th><th scope="col">Imsak</th><th scope="col">Subuh</th><th scope="col">Zohor</th><th scope="col">Asar</th><th scope="col">Berbuka (Maghrib)</th><th scope="col">Isyak</th><th scope="col">Tempoh puasa</th><th scope="col">✓</th></tr></thead>
<tbody>{"".join(r_row(k, d, t, s, day) for k, d, t in rows)}</tbody></table></div>
<p class="note">{note30}★ Malam ganjil 10 malam terakhir (malam bermula pada Maghrib hari sebelumnya). Tempoh puasa dikira dari Subuh hingga Maghrib. Tandakan ✓ hari yang anda berpuasa; tanda disimpan dalam pelayar ini sahaja.</p>
</section>'''
    return html, data, rows


def build_ramadan(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    day = dt.date.fromisoformat(ctx.get("SOLAT_DAY") or T)
    share, ad = ctx["share"], ctx["ad"]
    s = R.season(day)
    y, yr, n = s["y"], s["start"].year, s["n"]
    eid = s["start"] + dt.timedelta(n)
    AREA = areas()
    jang = "" if s["official"] else " (jangkaan)"
    datenote = ("Tarikh mengikut takwim JAKIM. Tarikh rasmi tetap tertakluk kepada pengisytiharan Penyimpan Mohor Besar Raja-Raja."
                if s["official"] else
                "Tarikh jangkaan berdasarkan kiraan hisab dan kriteria imkanur rukyah (MABIMS). Tarikh rasmi diumumkan oleh Penyimpan Mohor Besar Raja-Raja selepas rukyah hilal pada petang 29 Syaaban.")
    pages = []
    caps = []
    for slug, name, cap, capz in SL.STATES:
        rows, _ = R.timetable(capz, s)
        caps.append((slug, name, cap, capz, rows))
    kl = next(c for c in caps if c[3] == "WLY01")
    klr = kl[4]
    mag = [r[2][5] for r in klr]
    durs = [r[2][5] - r[2][1] for r in klr]

    # -------- key dates + doa blocks shared by the hub --------
    lq = lailatul(s)
    kdates = table(["Peristiwa", "Tarikh" + jang, "Catatan"], [
        ["<strong>1 Ramadan</strong> (mula berpuasa)", P.dlong(s["start"]), "Sahur pertama pada pagi hari ini; tarawih pertama malam sebelumnya"],
        ["<strong>Nuzul Al-Quran</strong> (17 Ramadan)", P.dlong(s["start"] + dt.timedelta(16)), "Cuti umum di beberapa negeri"],
        ["<strong>10 malam terakhir</strong>", f"Bermula Maghrib {P.dlong(s['start'] + dt.timedelta(19))}", "Malam 21 Ramadan; masa iktikaf dan mencari Lailatul Qadar"],
        ["<strong>Hari Raya Aidilfitri</strong> (1 Syawal)", P.dlong(eid), "Zakat fitrah wajib dibayar sebelum solat sunat Aidilfitri"],
    ], f"Tarikh penting Ramadan {y}H")
    lqt = table(["Malam", "Bermula Maghrib"], [[f"<strong>Malam {k} Ramadan</strong>", P.dlong(d)] for k, d in lq], "Malam ganjil 10 malam terakhir")
    doa = "".join(card(i, t, e(ar), e(ru), e(mn), e(src), extra=note, cat="ramadan") for i, t, ar, ru, mn, src, note in I2.RAMADAN_DOA)
    hadis = "".join(f"<li><strong>{e(t)}:</strong> {e(x)} <span class=\"dsrc\">({e(src)})</span></li>" for t, x, src in I2.RAMADAN_HADIS)
    ar1, ru1, tr1 = quran_block([(2, 183)])
    ayat183 = card("al-baqarah-183", "Kewajipan berpuasa (Al-Baqarah 2:183)", ar1, ru1, tr1, qref(2, 183), cat="ramadan")
    ar2, ru2, tr2 = quran_block([(97, a) for a in range(1, 6)])
    qadr = card("surah-al-qadr", "Surah Al-Qadr: malam yang lebih baik daripada seribu bulan", ar2, ru2, tr2, qref(97, 1), cat="ramadan")

    # ======== hub ========
    zones = list(SL.ZONES)
    tool, data, rows = ramadan_tool(zones, "WLY01", AREA, s, day, "puasa-zon")
    strows = [[f'<a href="/waktu-berbuka-puasa/{slug}/">{e(name)}</a>', f"{capz} ({e(cap)})", SL.hm(r[0][2][0]), f"<strong>{SL.hm(r[0][2][5])}</strong>", f"<strong>{SL.hm(r[-1][2][5])}</strong>"]
              for slug, name, cap, capz, r in caps]
    early = min(caps, key=lambda c: c[4][0][2][5])
    late = max(caps, key=lambda c: c[4][0][2][5])
    faq = [
        (f"Bilakah puasa Ramadan {yr} bermula di Malaysia?",
         f"1 Ramadan {y}H {'ialah' if s['official'] else 'dijangka jatuh pada'} {P.dlong(s['start'])}. Sahur pertama pada pagi itu dan solat tarawih pertama pada malam sebelumnya. {datenote}"),
        (f"Bilakah Hari Raya Aidilfitri {yr}?",
         f"1 Syawal {y}H {'ialah' if s['official'] else 'dijangka jatuh pada'} {P.dlong(eid)}, selepas {n} hari berpuasa. Tarikh rasmi diumumkan selepas rukyah pada petang 29 Ramadan."),
        (f"Pukul berapa waktu berbuka puasa di Kuala Lumpur pada Ramadan {yr}?",
         f"Waktu berbuka (Maghrib) bagi zon WLY01 (Kuala Lumpur dan Putrajaya) antara {SL.hm(min(mag))} dan {SL.hm(max(mag))} sepanjang Ramadan {y}H. Pada 1 Ramadan, imsak {SL.hm(klr[0][2][0])} dan berbuka {SL.hm(klr[0][2][5])}."),
        ("Bilakah waktu imsak dan bila sahur berakhir?",
         "Imsak ialah 10 minit sebelum Subuh, iaitu waktu berjaga-jaga untuk berhenti makan dan minum. Sahur sebenarnya berakhir apabila masuk waktu Subuh (terbit fajar sadiq); makan selepas Subuh membatalkan puasa."),
        ("Negeri mana yang paling awal dan paling lewat berbuka puasa?",
         f"Pada 1 Ramadan {y}H, {early[1]} ({early[3]}) berbuka paling awal antara ibu negeri, pukul {SL.hm(early[4][0][2][5])}, manakala {late[1]} ({late[3]}) paling lewat, pukul {SL.hm(late[4][0][2][5])}. Bandingkan semua negeri dalam jadual di atas."),
        ("Berapa lama tempoh berpuasa sehari di Malaysia?",
         f"Kira-kira {min(durs) // 60} jam {min(durs) % 60} minit hingga {max(durs) // 60} jam {max(durs) % 60} minit sehari di Kuala Lumpur (dari Subuh hingga Maghrib) sepanjang Ramadan {y}H, kerana Malaysia hampir dengan khatulistiwa."),
        (f"Bilakah malam Lailatul Qadar {yr}?",
         f"Tiada siapa mengetahui tarikhnya dengan pasti. Rasulullah SAW menyuruh mencarinya pada malam ganjil 10 malam terakhir (HR Al-Bukhari, no. 2017): malam 21 Ramadan bermula Maghrib {P.dlong(lq[0][1])}, dan malam 27 bermula Maghrib {P.dlong(lq[3][1])}."),
        ("Apakah doa berbuka puasa yang sahih?",
         "“Zahabaz-zama'u wabtallatil-'uruqu wa thabatal-ajru insya-Allah” (Telah hilang dahaga, telah basah urat-urat dan telah tetap pahala, insya-Allah), riwayat Abu Daud, no. 2357 (hasan). Lafaz “Allahumma laka sumtu…” diriwayatkan secara mursal (Abu Daud, no. 2358)."),
    ]
    title = f"Waktu Berbuka Puasa {yr} & Jadual Imsak Ramadan {y}H Malaysia"
    desc = f"Jadual waktu berbuka puasa dan imsak Ramadan {y}H/{yr} bagi semua zon JAKIM: kiraan ke berbuka, penanda puasa, peringatan kalendar, niat dan doa berbuka."
    answer = (f"Ramadan {y}H {'bermula' if s['official'] else 'dijangka bermula'} <strong>{P.dlong(s['start'])}</strong> dan Aidilfitri {'pada' if s['official'] else 'dijangka pada'} <strong>{P.dlong(eid)}</strong>. "
              f"Di Kuala Lumpur, waktu berbuka puasa (Maghrib) antara <strong>{SL.hm(min(mag))} dan {SL.hm(max(mag))}</strong> dan imsak 10 minit sebelum Subuh. Pilih zon anda di atas untuk jadual 30 hari.")
    body = hero(f"Waktu Berbuka Puasa {yr} & Jadual Imsak Ramadan {y}H",
                f"Jadual imsakiyah 30 hari bagi semua {len(zones)} zon JAKIM: imsak, sahur, berbuka (Maghrib), tempoh puasa, kiraan detik ke berbuka dan penanda puasa harian.",
                [("Alat", "alat/"), ("Waktu Berbuka Puasa", None)])
    body += f'''<div class="wrap mn"><div class="ct">
{tool}

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {answer}</p></div>
{meta_line(T, TMS)}
{share(SITE + "waktu-berbuka-puasa/", f"Jadual waktu berbuka puasa & imsak Ramadan {yr} ikut zon:")}
<p class="note">{datenote}</p>
</div>
</section>

<section id="negeri" aria-labelledby="h-negeri">
<h2 id="h-negeri">Waktu Berbuka Puasa Ikut Negeri ({yr})</h2>
<p>Waktu imsak dan berbuka pada hari pertama dan terakhir Ramadan bagi zon ibu negeri. Klik negeri untuk jadual penuh semua zon.</p>
{table(["Negeri", "Zon (ibu negeri)", "Imsak 1 Ramadan", "Berbuka 1 Ramadan", f"Berbuka {n} Ramadan"], strows, "Waktu berbuka puasa ikut negeri", "szt")}
</section>
{ad(0)}
<section id="tarikh" aria-labelledby="h-tarikh">
<h2 id="h-tarikh">Tarikh Penting Ramadan {y}H / {yr}</h2>
{kdates}
<h3 id="lailatul-qadar">Malam Ganjil 10 Malam Terakhir (Lailatul Qadar)</h3>
{lqt}
</section>

<section class="dsec" id="niat" aria-labelledby="h-niat">
<h2 id="h-niat">🤲 Niat Puasa & Doa Berbuka</h2>
{doa}
</section>

<section id="sunnah" aria-labelledby="h-sunnah">
<div class="prose">
<h2 id="h-sunnah">Sunnah & Kelebihan Berpuasa</h2>
<ul>{hadis}</ul>
</div>
{ayat183}
{qadr}
</section>
{ad(1)}
<section id="batal" aria-labelledby="h-batal">
<div class="prose">
<h2 id="h-batal">Perkara Yang Membatalkan Puasa</h2>
<ol class="steps">{"".join(f"<li>{e(x)}</li>" for x in I2.BATAL_PUASA)}</ol>
<p class="note">Mengikut mazhab Syafi'i. Bagi isu perubatan moden (suntikan, ubat titis, inhaler dan sebagainya), rujuk keputusan Muzakarah Jawatankuasa Fatwa Majlis Kebangsaan Bagi Hal Ehwal Ugama Islam Malaysia atau mufti negeri.</p>
<h2 id="rukhsah">Golongan Yang Diberi Keringanan</h2>
<ul>
<li><strong>Musafir</strong> (perjalanan sekurang-kurangnya dua marhalah, kira-kira 81 km) dan <strong>orang sakit</strong>: boleh berbuka dan wajib qada.</li>
<li><strong>Wanita haid atau nifas</strong>: haram berpuasa dan wajib qada.</li>
<li><strong>Wanita hamil atau menyusu</strong>: boleh berbuka; wajib qada, dan dalam mazhab Syafi'i ditambah fidyah jika berbuka kerana bimbang akan anak sahaja.</li>
<li><strong>Warga emas yang lemah dan pesakit yang tiada harapan sembuh</strong>: membayar fidyah secupak makanan asasi bagi setiap hari. Kira dengan <a href="{TBB}kalkulator-fidyah/" rel="noopener">Kalkulator Fidyah ↗</a>.</li>
</ul>
<h2 id="amalan">Amalan Ramadan Dengan Alat Kami</h2>
<ul>
<li><a href="/jadual-khatam-al-quran/#hari=30">Jadual khatam Al-Quran 30 hari</a>: kira-kira 20 muka surat sehari, atau 4 muka surat selepas setiap solat fardu.</li>
<li><a href="/zikir-pagi-petang/">Zikir pagi & petang</a> dan <a href="/tasbih-digital/">tasbih digital</a> untuk zikir selepas tarawih.</li>
<li><a href="/doa-harian/">Himpunan doa harian</a>, termasuk doa Sapu Jagat dan doa Nabi Yunus.</li>
</ul>
</div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Puasa Ramadan {yr}</h2>
{faq_html(faq)}
</section>
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("waktu-berbuka-puasa/")}</section>
</div>
{side([("kira", "Jadual imsakiyah"), ("negeri", "Ikut negeri"), ("tarikh", "Tarikh penting"), ("lailatul-qadar", "Lailatul Qadar"), ("niat", "Niat & doa berbuka"), ("sunnah", "Sunnah puasa"), ("batal", "Membatalkan puasa"), ("faq", "Soalan lazim")], "waktu-berbuka-puasa/")}
</div>'''
    pages.append(dict(path="waktu-berbuka-puasa/", kind="tool", data=False, arabic=True, published=PUB,
                      extra_data=f'<script type="application/json" id="rd">{data}</script>',
                      title=title, ogtitle=f"Waktu Berbuka Puasa & Imsak Ramadan {yr}", desc=desc,
                      crumbs=[("Alat", "alat/"), ("Waktu Berbuka Puasa", None)], body=body, faq=faq,
                      app=dict(name=f"Jadual Imsakiyah Ramadan {y}H", features=[f"Semua {len(zones)} zon waktu solat JAKIM", "Jadual 30 hari: imsak, Subuh, Maghrib (berbuka), Isyak", "Kiraan detik ke berbuka dan imsak", "Penanda puasa harian dan kiraan qada", "Peringatan kalendar (.ics) berbuka dan imsak", "Niat puasa dan doa berbuka"]),
                      about=["Ramadan", "Puasa", "Iftar", "Sahur"],
                      llms=f"Jadual waktu berbuka puasa dan imsak Ramadan {y}H ({yr}) bagi semua {len(zones)} zon JAKIM. 1 Ramadan {'(rasmi takwim JAKIM)' if s['official'] else '(jangkaan, imkanur rukyah MABIMS)'}: {s['start'].isoformat()}; Aidilfitri: {eid.isoformat()}. Kuala Lumpur (WLY01): berbuka {SL.hm(min(mag))}–{SL.hm(max(mag))}. Imsak = Subuh − 10 minit. Termasuk niat puasa, doa berbuka (Abu Daud 2357), malam ganjil Lailatul Qadar, perkara membatalkan puasa dan fidyah."))

    # ======== per state ========
    for slug, name, cap, capz in SL.STATES:
        sz = [z for z in SL.ZONES if z[1] == slug]
        tool, data, rows = ramadan_tool(sz, capz, AREA, s, day, "puasa-" + slug, name)
        url = f"waktu-berbuka-puasa/{slug}/"
        many = len(sz) > 1
        allz = {z[0]: R.timetable(z[0], s)[0] for z in sz}
        zrows = "".join(f'<tr data-z="{z[0]}"><th scope="row"><a href="#zon={z[0]}" data-zone="{z[0]}">{z[0]}</a><span class="za">{e(AREA[z[0]])}</span></th>'
                        f"<td>{SL.hm(allz[z[0]][0][2][0])}</td><td><strong>{SL.hm(allz[z[0]][0][2][5])}</strong></td>"
                        f"<td>{SL.hm(allz[z[0]][-1][2][0])}</td><td><strong>{SL.hm(allz[z[0]][-1][2][5])}</strong></td></tr>" for z in sz)
        mg = [r[2][5] for r in rows]
        im = [r[2][0] for r in rows]
        first = sorted((allz[z[0]][0][2][5], z[0]) for z in sz)
        faq = [
            (f"Pukul berapa waktu berbuka puasa di {cap} pada Ramadan {yr}?",
             f"Waktu berbuka (Maghrib) bagi zon {capz} ({cap}) antara {SL.hm(min(mg))} dan {SL.hm(max(mg))} sepanjang Ramadan {y}H. Pada 1 Ramadan ({P.dlong(s['start'])}) berbuka pukul {SL.hm(mg[0])}."),
            (f"Bilakah waktu imsak di {cap}?",
             f"Imsak bagi zon {capz} antara {SL.hm(min(im))} dan {SL.hm(max(im))} sepanjang Ramadan {y}H, iaitu 10 minit sebelum Subuh. Sahur mesti dihentikan sebelum masuk waktu Subuh."),
            (f"Bilakah puasa {yr} bermula di {name}?",
             f"1 Ramadan {y}H {'ialah' if s['official'] else 'dijangka jatuh pada'} {P.dlong(s['start'])} di seluruh Malaysia, termasuk {name}, dan Aidilfitri {'pada' if s['official'] else 'dijangka pada'} {P.dlong(eid)}. {datenote}"),
        ]
        if many:
            faq.insert(1, (f"Berapa zon waktu berbuka puasa di {name}?",
                           f"{name} mempunyai {len(sz)} zon JAKIM. Pada 1 Ramadan, berbuka paling awal pukul {SL.hm(first[0][0])} (zon {first[0][1]}) dan paling lewat {SL.hm(first[-1][0])} (zon {first[-1][1]}), beza {first[-1][0] - first[0][0]} minit."))
        title = f"Waktu Berbuka Puasa {name} {yr} & Jadual Imsak Ramadan"
        if len(title) > 70:
            title = f"Waktu Berbuka Puasa {name} {yr} (Imsak Ramadan)"
        desc = f"Waktu berbuka puasa dan imsak {name} Ramadan {y}H/{yr} bagi {len(sz)} zon JAKIM: jadual 30 hari, kiraan detik ke berbuka, penanda puasa dan peringatan kalendar."
        if len(desc) > 160:
            desc = f"Waktu berbuka puasa dan imsak {name} Ramadan {yr} bagi {len(sz)} zon JAKIM: jadual 30 hari, kiraan detik ke berbuka dan peringatan kalendar."
        answer = (f"Di {cap} (zon {capz}), puasa Ramadan {y}H {'bermula' if s['official'] else 'dijangka bermula'} {P.dlong(s['start'])} dengan "
                  f"<strong>imsak {SL.hm(im[0])} dan berbuka {SL.hm(mg[0])}</strong>. Waktu berbuka sepanjang Ramadan antara {SL.hm(min(mg))} dan {SL.hm(max(mg))}."
                  + (f" {name} mempunyai {len(sz)} zon; pilih zon anda di atas." if many else ""))
        body = hero(f"Waktu Berbuka Puasa {e(name)} {yr}",
                    f"Jadual imsak dan berbuka Ramadan {y}H bagi {'semua ' + str(len(sz)) + ' zon' if many else 'zon ' + capz} di {e(name)}, dengan kiraan detik ke berbuka dan penanda puasa harian.",
                    [("Waktu Berbuka Puasa", "waktu-berbuka-puasa/"), (name, None)])
        body += f'''<div class="wrap mn"><div class="ct">
{tool}

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {answer}</p></div>
{meta_line(T, TMS)}
{share(SITE + url, f"Waktu berbuka puasa {name} Ramadan {yr}:")}
<p class="note">{datenote}</p>
</div>
</section>

<section id="zon" aria-labelledby="h-zon">
<h2 id="h-zon">{"Semua Zon " + e(name) + ": Imsak & Berbuka" if many else "Zon " + capz + ": Imsak & Berbuka"}</h2>
<p class="note">Hari pertama dan terakhir Ramadan {y}H. Klik kod zon untuk jadual 30 hari.</p>
<div class="tw" tabindex="0" role="region" aria-label="Imsak dan berbuka setiap zon"><table class="plan szt" id="szt">
<thead><tr><th scope="col">Zon & kawasan</th><th scope="col">Imsak 1 Ramadan</th><th scope="col">Berbuka 1 Ramadan</th><th scope="col">Imsak {n} Ramadan</th><th scope="col">Berbuka {n} Ramadan</th></tr></thead>
<tbody>{zrows}</tbody></table></div>
</section>
{ad(0)}
<section class="dsec" id="niat" aria-labelledby="h-niat">
<h2 id="h-niat">🤲 Niat Puasa & Doa Berbuka</h2>
{"".join(card(i, t, e(ar), e(ru), e(mn), e(src), extra=note, cat="ramadan") for i, t, ar, ru, mn, src, note in I2.RAMADAN_DOA[:1] + I2.RAMADAN_DOA[2:3])}
<p class="note">Niat sebulan, doa Lailatul Qadar, tarikh penting dan perkara yang membatalkan puasa: <a href="/waktu-berbuka-puasa/#niat">panduan Ramadan penuh</a>.</p>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Berbuka Puasa di {e(name)}</h2>
{faq_html(faq)}
</section>

<section id="negeri" aria-labelledby="h-negeri">
<h2 id="h-negeri">Waktu Berbuka Puasa Negeri Lain</h2>
<ul class="rel sts">{"".join(f'<li><a href="/waktu-berbuka-puasa/{s2}/">Berbuka Puasa {e(n2)}</a></li>' for s2, n2, _, _ in SL.STATES if s2 != slug)}</ul>
<p class="note">Waktu solat harian sepanjang tahun: <a href="/waktu-solat/{slug}/">Waktu Solat {e(name)}</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("waktu-berbuka-puasa/")}</section>
</div>
{side([("kira", "Jadual imsakiyah"), ("zon", "Semua zon" if many else "Zon"), ("niat", "Niat & doa berbuka"), ("faq", "Soalan lazim"), ("negeri", "Negeri lain")], "waktu-berbuka-puasa/")}
</div>'''
        pages.append(dict(path=url, kind="tool", data=False, arabic=True, published=PUB, extra_data=f'<script type="application/json" id="rd">{data}</script>',
                          title=title, ogtitle=f"Waktu Berbuka Puasa {name} {yr}", desc=desc,
                          crumbs=[("Waktu Berbuka Puasa", "waktu-berbuka-puasa/"), (name, None)], body=body, faq=faq,
                          about=[f"Ramadan {yr}", f"Waktu berbuka puasa {name}", name], og=f"waktu-berbuka-puasa-{slug}",
                          llms=f"Waktu berbuka puasa dan imsak {name}, Ramadan {y}H ({yr}), {len(sz)} zon JAKIM. {cap} ({capz}): berbuka {SL.hm(min(mg))}–{SL.hm(max(mg))}, imsak {SL.hm(min(im))}–{SL.hm(max(im))}."))
    return pages


# ======================= BELAJAR SOLAT =======================
def solat_data():
    b = {}
    for k, (title, how, ar, ru, mn, src) in I2.BACAAN.items():
        if isinstance(ar, tuple):
            _, sn, a1, a2 = ar
            ar, ru, mn = quran_block([(sn, a) for a in range(a1, a2 + 1)])
            src = f"{e(src)} · {qref(sn, a1)}"
            b[k] = [e(title), e(how), ar, ru, mn, src]
        else:
            b[k] = [e(title), e(how), e(ar), e(ru), e(mn), e(src)]
    w = {k: {"n": n, "r": r, "niat": [e(ar), e(ru), e(mn)]} for k, n, r, ar, ru, mn in I2.SOLAT5}
    st = {k: I2.solat_steps(r, k == "subuh") for k, _, r, _, _, _ in I2.SOLAT5}
    return {"b": b, "w": w, "s": st}


def sp_card(D, w, i):
    sid, r = D["s"][w][i]
    t, how, ar, ru, mn, src = D["b"][sid]
    if sid == "niat":
        ar, ru, mn = D["w"][w]["niat"]
    N, Rk = len(D["s"][w]), D["w"][w]["r"]
    return (f'<p class="spn">Rakaat {r} daripada {Rk} · Langkah {i + 1} / {N}</p><h3 class="spt">{t}</h3><p class="spd">{how}</p>'
            f'<p class="dar" lang="ar" dir="rtl">{ar}</p><p class="dru"><em>{ru}</em></p><p class="dmn"><strong>Maksud:</strong> {mn}</p><p class="dsrc">{src}</p>')


CUR = ' aria-current="step"'


def sp_list(D, w, cur):
    return "".join(f'<li><button type="button" data-i="{i}"{CUR if i == cur else ""}>{D["b"][sid][0]} <small>R{r}</small></button></li>'
                   for i, (sid, r) in enumerate(D["s"][w]))


def qada_html(y, m, d, sets, start):
    days = y * 365 + m * 30 + d
    if days <= 0:
        return "<p>Masukkan tempoh solat fardu yang tertinggal.</p>"
    fd = math.ceil(days / sets)
    end = start + dt.timedelta(fd - 1)
    return (f"<p><strong>{P.num(days * 5)} solat fardu</strong> perlu diqada ({P.num(days)} hari × 5 waktu), iaitu {P.num(days * 17)} rakaat.</p>"
            f"<p>Dengan {sets} set qada sehari (setiap set = Subuh, Zohor, Asar, Maghrib, Isyak), selesai dalam <strong>{P.num(fd)} hari</strong> "
            f"(≈ {P.r1(fd / 30)} bulan): <strong>{P.dlong(end)}</strong>.</p>")


def build_solat(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    start = dt.date.fromisoformat(T)
    D = solat_data()
    chips = "".join(f'<button type="button" data-w="{k}" aria-pressed="{"true" if k == "subuh" else "false"}">{n} ({r})</button>' for k, n, r, _, _, _ in I2.SOLAT5)
    niat = table(["Solat", "Rakaat", "Lafaz niat", "Rumi"],
                 [[f"<strong>{n}</strong>", str(r), f'<span class="tjw" lang="ar" dir="rtl">{e(ar)}</span>', f"<em>{e(ru)}</em>"] for _, n, r, ar, ru, _ in I2.SOLAT5],
                 "Lafaz niat solat fardu lima waktu", "nt")
    order = ["takbir", "iftitah", "fatihah", "rukuk", "iktidal", "sujud", "duduk", "qunut", "tahiyat-awal", "tahiyat-akhir", "doa-akhir", "salam"]
    bcards = "".join(card(k, I2.BACAAN[k][0], D["b"][k][2], D["b"][k][3], D["b"][k][4], D["b"][k][5], extra=I2.BACAAN[k][1], cat="solat") for k in order)
    faq = [
        ("Apakah rukun solat?", "Dalam mazhab Syafi'i, rukun solat ada 13: " + ", ".join(I2.RUKUN).lower() + ". Jika satu rukun tertinggal dengan sengaja, solat batal."),
        ("Bagaimana cara solat Subuh?", "Solat Subuh dua rakaat: niat dan takbiratul ihram, doa iftitah, Al-Fatihah dan surah, rukuk, iktidal, qunut (pada rakaat kedua, sunat dalam mazhab Syafi'i), sujud, duduk antara dua sujud, sujud kedua, kemudian rakaat kedua, tahiyat akhir dan salam. Panduan langkah demi langkah ada di atas."),
        ("Bilakah tahiyat awal dibaca?", "Tahiyat awal dibaca selepas sujud kedua pada rakaat kedua bagi solat tiga dan empat rakaat (Maghrib, Zohor, Asar dan Isyak). Ia sunat ab'adh; jika tertinggal, sunat melakukan sujud sahwi sebelum salam."),
        ("Bagaimana jika lupa bilangan rakaat?", "Ambil bilangan yang paling sedikit (yang diyakini), sempurnakan solat, kemudian sujud sahwi sebelum salam (HR Muslim, no. 571)."),
        ("Apakah bacaan sujud sahwi?", "Sujud sahwi ialah dua kali sujud sebelum salam. Bacaan yang lazim di Malaysia ialah “Subhana man la yanamu wa la yashu” (Maha Suci Tuhan yang tidak tidur dan tidak lupa). Tiada lafaz khusus daripada hadis; membaca tasbih sujud biasa juga memadai."),
        ("Bagaimana cara qada solat yang tertinggal?", "Solat yang ditinggalkan wajib diqada dengan niat qada, contohnya “Usolli fardhaz-zuhri arba'a raka'atin qadha'an lillahi ta'ala”. Ulama Syafi'i menganjurkan qada segera dan mengikut tertib waktu. Guna kalkulator qada di atas untuk merancang tempohnya."),
        ("Perlukah melafazkan niat solat?", "Niat ialah amalan hati dan wajib ketika takbiratul ihram. Melafazkan niat (usolli) sebelum takbir adalah sunat dalam mazhab Syafi'i untuk membantu hati, tetapi tidak wajib."),
    ]
    body = hero("Cara Solat Lengkap: Bacaan, Niat & Langkah demi Langkah",
                "Panduan solat fardu lima waktu mengikut mazhab Syafi'i: setiap pergerakan dengan bacaan Arab, Rumi dan maksud, rukun solat, sujud sahwi dan kalkulator solat qada.",
                [("Alat", "alat/"), ("Belajar Solat", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="panduan" class="tool" aria-labelledby="h-pan">
<h2 id="h-pan">🕌 Panduan Solat Langkah demi Langkah</h2>
<div class="chips2" id="spw" role="group" aria-label="Pilih solat">{chips}</div>
<div class="act"><button class="btn2" type="button" id="sprm" aria-pressed="true">Rumi</button><button class="btn2" type="button" id="spmn" aria-pressed="true">Maksud</button><button class="btn2" type="button" data-act="link">🔗 Salin pautan</button></div>
<div class="spc" id="spc" aria-live="polite">{sp_card(D, "subuh", 0)}</div>
<div class="spnav"><button class="btn2" type="button" id="spprev" disabled>‹ Sebelum</button><progress id="spp" max="{len(D["s"]["subuh"])}" value="1"></progress><button class="btn3" type="button" id="spnext">Seterusnya ›</button></div>
<details class="spx"><summary>Senarai semua langkah</summary><ol class="spl" id="spl">{sp_list(D, "subuh", 0)}</ol></details>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp">Cara Solat Secara Ringkas</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Solat bermula dengan <strong>niat dan takbiratul ihram</strong>, diikuti doa iftitah, <strong>Al-Fatihah</strong> dan surah, <strong>rukuk, iktidal, dua kali sujud</strong> dengan duduk di antaranya. Ulang bagi setiap rakaat (Subuh 2, Maghrib 3, Zohor, Asar dan Isyak 4), baca <strong>tahiyat awal</strong> pada rakaat kedua solat 3 dan 4 rakaat, dan akhiri dengan <strong>tahiyat akhir dan salam</strong>.</p></div>
{meta_line(T, TMS)}
{share(SITE + "belajar-solat/", "Cara solat lengkap dengan bacaan & panduan langkah demi langkah:")}
</div>
</section>

<section id="niat" aria-labelledby="h-niat">
<h2 id="h-niat">Niat Solat Fardu Lima Waktu</h2>
{niat}
<p class="note">Bagi makmum, tambah “makmuman” (مَأْمُومًا) selepas “mustaqbilal-qiblati”; bagi imam, “imaman” (إِمَامًا). Bagi solat qada, tukar “ada'an” kepada “qadha'an” (قَضَاءً). Waktu solat hari ini: <a href="/waktu-solat/">Waktu Solat</a>.</p>
</section>

<section class="dsec" id="bacaan" aria-labelledby="h-bacaan">
<h2 id="h-bacaan">📖 Bacaan Dalam Solat (Arab, Rumi & Maksud)</h2>
{bcards}
</section>
{ad(0)}
<section id="rukun" aria-labelledby="h-rukun">
<div class="prose">
<h2 id="h-rukun">13 Rukun Solat</h2>
<ol class="steps">{"".join(f"<li>{e(x)}</li>" for x in I2.RUKUN)}</ol>
<h2 id="syarat">Syarat Sah Solat</h2>
<ul>{"".join(f"<li>{e(x)}</li>" for x in I2.SYARAT_SAH)}</ul>
<h2 id="batal">Perkara Yang Membatalkan Solat</h2>
<ul>{"".join(f"<li>{e(x)}</li>" for x in I2.BATAL)}</ul>
<h2 id="sahwi">Sujud Sahwi</h2>
<p>Sujud sahwi ialah dua kali sujud sebelum salam kerana: tertinggal sunat ab'adh (tahiyat awal, qunut Subuh), ragu-ragu bilangan rakaat, atau terlebih atau terkurang perbuatan tanpa sengaja. Ia sunat, bukan wajib, dalam mazhab Syafi'i.</p>
</div>
{table(["Solat", "Rakaat", "Bacaan Al-Fatihah", "Tahiyat awal", "Qunut"], [
    ["<strong>Subuh</strong>", "2", "Nyaring (jahar)", "Tiada", "Ya (rakaat 2)"],
    ["<strong>Zohor</strong>", "4", "Perlahan (sirr)", "Rakaat 2", "Tiada"],
    ["<strong>Asar</strong>", "4", "Perlahan (sirr)", "Rakaat 2", "Tiada"],
    ["<strong>Maghrib</strong>", "3", "Nyaring rakaat 1–2", "Rakaat 2", "Tiada"],
    ["<strong>Isyak</strong>", "4", "Nyaring rakaat 1–2", "Rakaat 2", "Tiada"],
], "Bilangan rakaat solat fardu")}
</section>

<section id="qada" class="tool" aria-labelledby="h-qada">
<h2 id="h-qada">🧮 Kalkulator Solat Qada</h2>
<p class="note">Anggarkan tempoh solat yang tertinggal (1 tahun = 365 hari, 1 bulan = 30 hari) dan berapa set qada yang mampu dibuat sehari.</p>
<form class="frm" id="qf" novalidate>
<div class="fl"><label for="qy">Tahun</label><input id="qy" type="number" inputmode="numeric" min="0" max="80" value="1"></div>
<div class="fl"><label for="qm">Bulan</label><input id="qm" type="number" inputmode="numeric" min="0" max="11" value="0"></div>
<div class="fl"><label for="qd">Hari</label><input id="qd" type="number" inputmode="numeric" min="0" max="29" value="0"></div>
<div class="fl"><label for="qs">Set qada sehari</label><select id="qs"><option value="1">1 set (17 rakaat)</option><option value="2">2 set (34 rakaat)</option><option value="3">3 set (51 rakaat)</option><option value="5">5 set (85 rakaat)</option></select></div>
</form>
<div class="sum" id="qsum">{qada_html(1, 0, 0, 1, start)}</div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Cara Solat</h2>
{faq_html(faq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("belajar-solat/")}</section>
</div>
{side([("panduan", "Panduan langkah demi langkah"), ("niat", "Niat solat"), ("bacaan", "Bacaan dalam solat"), ("rukun", "Rukun solat"), ("syarat", "Syarat sah"), ("batal", "Membatalkan solat"), ("sahwi", "Sujud sahwi"), ("qada", "Kalkulator qada"), ("faq", "Soalan lazim")], "belajar-solat/")}
</div>'''
    return [dict(path="belajar-solat/", kind="tool", data=False, arabic=True, published=PUB,
                 extra_data=f'<script type="application/json" id="spd">{J(D)}</script>',
                 title="Cara Solat Lengkap: Bacaan, Niat & Langkah Solat Fardu",
                 ogtitle="Cara Solat Lengkap – Bacaan & Langkah demi Langkah",
                 desc="Cara solat fardu lengkap mengikut mazhab Syafi'i: niat 5 waktu, bacaan Arab-Rumi-maksud setiap rukun, panduan langkah demi langkah dan kalkulator qada.",
                 crumbs=[("Alat", "alat/"), ("Belajar Solat", None)], body=body, faq=faq,
                 app=dict(name="Panduan Solat Langkah demi Langkah", features=["Panduan interaktif solat Subuh, Zohor, Asar, Maghrib dan Isyak", "Bacaan Arab, Rumi dan maksud setiap rukun", "Niat solat fardu lima waktu", "13 rukun solat dan sujud sahwi", "Kalkulator solat qada"]),
                 about=["Solat", "Salah", "Mazhab Syafi'i"],
                 llms="Cara solat fardu mengikut mazhab Syafi'i: niat 5 waktu (usolli…), takbiratul ihram, doa iftitah (Muslim 601, 771), Al-Fatihah, rukuk (Abu Daud 870), iktidal (Muslim 476), qunut Subuh (Abu Daud 1425), sujud, duduk antara dua sujud (At-Tirmizi 284), tahiyat awal/akhir (Muslim 403), selawat Ibrahimiyyah (Al-Bukhari 3370), salam. 13 rukun, syarat sah, perkara membatalkan, sujud sahwi, kalkulator qada (17 rakaat sehari).")]


# ======================= IQRA' =======================
def iq_items():
    """Default Iqra' 1 drill (the same 12 letters alat.js shows before the first 'Jana')."""
    out = []
    for h in I2.HURUF[1:13]:
        c, rumi, heavy = h[0], h[2], h[3]
        out.append(f'<li><button type="button" class="iqi"><span class="iqa" lang="ar" dir="rtl">{c}َ</span><span class="iqr">{rumi}{"o" if heavy else "a"}</span></button></li>')
    return "".join(out)


def build_iqra(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    lv = "".join(f'<button type="button" data-l="{n}" aria-pressed="{"true" if n == 1 else "false"}">{e(t)}</button>' for n, t, *_ in I2.IQRA)
    ex6 = [[s, a, ayah(s, a)["arabic"], ayah(s, a)["rumi"], f"{P.NAMES[s - 1]} {s}:{a}"] for s, a in I2.IQRA6]
    data = {"h": [[c, n, r, hv, cn] for c, n, r, hv, cn, *_ in I2.HURUF], "lv": [[n, t, f, d] for n, t, f, d, *_ in I2.IQRA], "q6": ex6, "qal": I2.QALQALAH}
    rows = [[f"<strong>{e(t)}</strong>", e(f), e(d), f'<span class="tjw" lang="ar" dir="rtl">{e(ar)}</span>' if ar else "Ayat Juz 30", f"<em>{e(ru)}</em>" if ru else "—"] for n, t, f, d, ar, ru in I2.IQRA]
    faq = [
        ("Apakah kaedah Iqra'?", "Iqra' ialah kaedah belajar membaca Al-Quran dalam 6 jilid yang disusun oleh K.H. As'ad Humam di Indonesia dan digunakan secara meluas di Malaysia sejak 1990-an. Pelajar terus membaca suku kata berbaris tanpa mengeja (contohnya “ba”, bukan “ba baris atas ba”), bermula daripada huruf tunggal hingga ayat Al-Quran."),
        ("Berapa lama untuk habis Iqra' 1 hingga 6?", "Ia bergantung pada umur, kekerapan dan bimbingan guru. Dengan latihan 15 hingga 30 minit sehari dan semakan guru, ramai pelajar dewasa menamatkannya dalam beberapa bulan. Kualiti sebutan lebih penting daripada kelajuan."),
        ("Bolehkah orang dewasa belajar Iqra'?", "Boleh. Kaedah Iqra' sesuai untuk semua umur kerana bermula daripada asas. Orang dewasa biasanya lebih cepat memahami peraturan, tetapi perlu lebih banyak latihan sebutan makhraj."),
        ("Selepas Iqra' 6, apa langkah seterusnya?", "Mula membaca Al-Quran (biasanya surah pendek Juz 30 dahulu), belajar hukum tajwid secara berperingkat, dan terus bertalaqqi dengan guru. Gunakan pembaca Al-Quran dengan audio qari untuk mendengar contoh bacaan."),
        ("Adakah latihan di halaman ini sama dengan buku Iqra'?", "Tidak. Latihan di sini dijana secara rawak mengikut fokus setiap tahap Iqra' (bukan salinan buku) sebagai latihan tambahan. Gunakan buku Iqra' bercetak dan bimbingan guru sebagai rujukan utama."),
    ]
    body = hero("Belajar Iqra' 1–6 Online: Latihan Membaca Al-Quran",
                "Latihan interaktif mengikut 6 tahap Iqra': huruf berbaris, mad, tanwin, sukun, qalqalah, alif lam, sabdu hingga ayat Al-Quran. Jana latihan baharu tanpa had.",
                [("Alat", "alat/"), ("Belajar Iqra'", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="latih" class="tool" aria-labelledby="h-latih">
<h2 id="h-latih">📗 Latihan Iqra' Interaktif</h2>
<div class="chips2" id="iql" role="group" aria-label="Tahap Iqra'">{lv}</div>
<p class="iqd" id="iqd"><strong>{e(I2.IQRA[0][2])}.</strong> {e(I2.IQRA[0][3])}</p>
<div class="act"><button class="btn3" type="button" id="iqgen">🔄 Jana latihan baharu</button><button class="btn2" type="button" id="iqrm" aria-pressed="false">Tunjuk rumi</button><button class="btn2" type="button" id="iqtts" hidden>🔊 Suara peranti</button><button class="btn2" type="button" id="iqdone" aria-pressed="false">✓ Tahap selesai</button></div>
<ol class="iqg" id="iqg">{iq_items()}</ol>
<p class="note">Ketik setiap kotak untuk melihat bacaan Rumi. Baca dahulu, kemudian semak. “Suara peranti” menggunakan suara Arab telefon anda (jika ada) dan bukan pengganti guru.</p>
<p class="prog" id="iqprog"></p>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp">Apa Itu Iqra'?</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Iqra' ialah kaedah belajar membaca Al-Quran dalam <strong>6 tahap</strong>: (1) huruf berbaris atas, (2) huruf bersambung dan mad alif, (3) baris bawah, hadapan dan mad ya/wau, (4) tanwin, sukun dan qalqalah, (5) alif lam, sabdu dan waqaf, (6) membaca ayat Al-Quran. Pelajar membaca terus tanpa mengeja, dan setiap tahap disemak oleh guru sebelum naik ke tahap seterusnya.</p></div>
{meta_line(T, TMS)}
{share(SITE + "belajar-iqra/", "Latihan Iqra' 1–6 online percuma:")}
</div>
</section>

<section id="tahap" aria-labelledby="h-tahap">
<h2 id="h-tahap">6 Tahap Iqra' & Contoh Bacaan</h2>
{table(["Tahap", "Fokus", "Apa yang dipelajari", "Contoh", "Rumi"], rows, "Enam tahap Iqra'", "iqt")}
</section>
{ad(0)}
<section id="tips" aria-labelledby="h-tips">
<div class="prose">
<h2 id="h-tips">Cara Belajar Iqra' Dengan Berkesan</h2>
<ol class="steps">
<li><strong>Baca terus tanpa mengeja.</strong> Sebut “ba”, bukan “ba baris atas ba”. Inilah teras kaedah Iqra'.</li>
<li><strong>Sedikit tetapi setiap hari.</strong> 15 minit sehari lebih berkesan daripada 2 jam seminggu sekali.</li>
<li><strong>Jangan naik tahap terlalu cepat.</strong> Naik ke tahap seterusnya hanya apabila boleh membaca halaman semasa dengan lancar dan betul.</li>
<li><strong>Bertalaqqi dengan guru.</strong> Makhraj dan panjang pendek bacaan hanya dapat diperbetulkan oleh guru yang mendengar bacaan anda.</li>
<li><strong>Dengar bacaan qari.</strong> Selepas Iqra' 6, dengar dan ikut bacaan surah pendek dalam <a href="/#surah-78">Juz 30</a> ayat demi ayat.</li>
</ol>
<p>Untuk mengenal huruf dan makhraj terlebih dahulu, mulakan dengan <a href="/belajar-mengaji/">Belajar Mengaji: Huruf Hijaiyah</a>. Selepas Iqra', sambung dengan <a href="/belajar-tajwid/">Belajar Tajwid</a>.</p>
</div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Iqra'</h2>
{faq_html(faq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("belajar-iqra/")}</section>
</div>
{side([("latih", "Latihan interaktif"), ("tahap", "6 tahap Iqra'"), ("tips", "Cara belajar"), ("faq", "Soalan lazim")], "belajar-iqra/")}
</div>'''
    return [dict(path="belajar-iqra/", kind="tool", data=False, arabic=True, published=PUB,
                 extra_data=f'<script type="application/json" id="iqd-data">{J(data)}</script>',
                 title="Belajar Iqra' 1–6 Online: Latihan Membaca Al-Quran Percuma",
                 ogtitle="Belajar Iqra' 1–6 Online – Latihan Interaktif",
                 desc="Latihan Iqra' 1 hingga 6 percuma: huruf berbaris, mad, tanwin, sukun, qalqalah, alif lam dan sabdu, dijana tanpa had dengan rumi, serta ayat Juz 30.",
                 crumbs=[("Alat", "alat/"), ("Belajar Iqra'", None)], body=body, faq=faq,
                 app=dict(name="Latihan Iqra' 1–6", features=["6 tahap mengikut kaedah Iqra'", "Latihan dijana tanpa had", "Rumi tersembunyi untuk menguji bacaan", "Suara Arab peranti (jika ada)", "Penanda tahap selesai", "Ayat Juz 30 untuk Iqra' 6"]),
                 about=["Iqra'", "Membaca Al-Quran", "Huruf hijaiyah"],
                 llms="Belajar Iqra' 1–6: tahap 1 huruf berbaris atas; 2 huruf bersambung dan mad alif; 3 kasrah, dhammah, mad ya/wau; 4 tanwin, sukun, qalqalah (ق ط ب ج د); 5 alif lam qamariah/syamsiah, sabdu, waqaf; 6 ayat Al-Quran (Juz 30). Latihan dijana secara rawak dengan rumi; bukan salinan buku Iqra' (K.H. As'ad Humam).")]


# ======================= MENGAJI =======================
def build_mengaji(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    grid = "".join(f'<button type="button" data-i="{i}" aria-pressed="false"><span class="hjc" lang="ar">{c}</span><span class="hjn">{e(n)}</span></button>' for i, (c, n, *_) in enumerate(I2.HURUF))
    mk = dict(I2.MAKHRAJ)
    mrows = [[f"<strong>{e(mk[g])}</strong>", f'<span class="tjw" lang="ar" dir="rtl">{" ".join(h[0] for h in I2.HURUF if h[5] == g) or "ن م (dengung)"}</span>',
              {"jauf": "Huruf mad: alif, wau dan ya mati selepas baris yang sesuai", "halq": "6 huruf halqi: pangkal, tengah dan hujung halkum",
               "lisan": "Kebanyakan huruf: pangkal, tengah, tepi dan hujung lidah", "syafatan": "Bibir rapat (ب م), dimuncungkan (و), bibir dan gigi (ف)",
               "khaisyum": "Dengung (ghunnah) nun dan mim"}[g]] for g, _ in I2.MAKHRAJ]
    hrows = [["<strong>Fathah</strong> (baris atas)", '<span class="tjw" lang="ar">بَ</span>', "ba"], ["<strong>Kasrah</strong> (baris bawah)", '<span class="tjw" lang="ar">بِ</span>', "bi"],
             ["<strong>Dhammah</strong> (baris hadapan)", '<span class="tjw" lang="ar">بُ</span>', "bu"], ["<strong>Sukun</strong> (tanda mati)", '<span class="tjw" lang="ar">اَبْ</span>', "ab"],
             ["<strong>Tanwin</strong> (baris dua)", '<span class="tjw" lang="ar">بًا بٍ بٌ</span>', "ban, bin, bun"], ["<strong>Syaddah</strong> (sabdu)", '<span class="tjw" lang="ar">اَبَّ</span>', "ab-ba"],
             ["<strong>Mad</strong> (panjang 2 harakat)", '<span class="tjw" lang="ar">بَا بِي بُو</span>', "baa, bii, buu"]]
    ms = "".join(f'<li><label><input type="checkbox" data-m="{k}"> {e(t)}</label></li>' for k, t in I2.MILESTONES)
    modes = [("nama", "Huruf → nama"), ("huruf", "Nama → huruf"), ("bentuk", "Bentuk sambung → huruf"), ("makhraj", "Huruf → makhraj")]
    data = {"h": [list(h) for h in I2.HURUF], "mk": I2.MAKHRAJ}
    faq = [
        ("Berapakah bilangan huruf hijaiyah?", "Huruf hijaiyah lazimnya dikira 29 huruf (termasuk hamzah), bermula dengan alif dan berakhir dengan ya. Sebahagian buku mengira 28 huruf kerana alif dan hamzah dianggap satu, atau 30 dengan lam alif (لا)."),
        ("Bagaimana cara belajar mengaji untuk orang dewasa?", "Mulakan dengan mengenal huruf hijaiyah dan makhrajnya, kemudian baris dan bacaan bersambung melalui kaedah Iqra' atau seumpamanya, diikuti surah pendek Juz 30 dan asas tajwid. Belajar 15 hingga 30 minit setiap hari dan bertalaqqi dengan guru sekurang-kurangnya seminggu sekali."),
        ("Bolehkah belajar mengaji sendiri tanpa guru?", "Mengenal huruf dan peraturan boleh dimulakan sendiri, tetapi sebutan (makhraj, sifat huruf, panjang pendek) perlu didengar dan diperbetulkan oleh guru. Ulama menekankan kaedah talaqqi (berdepan dengan guru) kerana Al-Quran diwarisi secara lisan."),
        ("Apakah makhraj huruf?", "Makhraj ialah tempat keluar huruf. Ia dibahagikan kepada 5 kawasan utama: Al-Jauf (rongga mulut dan tekak), Al-Halq (halkum), Al-Lisan (lidah), Asy-Syafatan (dua bibir) dan Al-Khaisyum (rongga hidung)."),
        ("Apakah huruf yang tidak bersambung dengan huruf selepasnya?", "Enam huruf: ا د ذ ر ز و (serta hamzah ء). Huruf ini hanya bersambung dengan huruf sebelumnya, jadi huruf selepasnya ditulis dalam bentuk awal."),
    ]
    body = hero("Belajar Mengaji: Huruf Hijaiyah, Makhraj & Kuiz",
                "Mula mengaji dari asas: 29 huruf hijaiyah dengan nama, makhraj, bentuk sambung dan baris, kuiz 4 mod, serta senarai semak kemajuan hingga boleh membaca Al-Quran.",
                [("Alat", "alat/"), ("Belajar Mengaji", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="huruf" class="tool" aria-labelledby="h-huruf">
<h2 id="h-huruf">🔤 29 Huruf Hijaiyah Interaktif</h2>
<div class="hjg" id="hjg" role="group" aria-label="Huruf hijaiyah">{grid}</div>
<div class="hjd" id="hjd" aria-live="polite"><p>Pilih huruf untuk melihat nama, makhraj, bentuk sambung dan bacaan dengan setiap baris.</p></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp">Bagaimana Mula Belajar Mengaji?</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Belajar mengaji bermula dengan <strong>mengenal 29 huruf hijaiyah</strong> dan <strong>makhrajnya</strong>, kemudian <strong>baris</strong> (atas, bawah, hadapan), <strong>bacaan bersambung</strong> dan <strong>mad</strong> melalui kaedah seperti <a href="/belajar-iqra/">Iqra'</a>, diikuti surah pendek Juz 30 dan <a href="/belajar-tajwid/">tajwid</a>. Latih 15–30 minit setiap hari dan perdengarkan bacaan kepada guru.</p></div>
{meta_line(T, TMS)}
{share(SITE + "belajar-mengaji/", "Belajar mengaji dari asas: huruf hijaiyah, makhraj & kuiz:")}
</div>
</section>

<section id="kuiz" class="tool" aria-labelledby="h-kuiz">
<h2 id="h-kuiz">📝 Kuiz Huruf Hijaiyah</h2>
<div class="chips2" id="hqm" role="group" aria-label="Jenis kuiz">{"".join(f'<button type="button" data-m="{k}" aria-pressed="{"true" if k == "nama" else "false"}">{e(n)}</button>' for k, n in modes)}</div>
<div class="qz" id="hqz"><p>10 soalan rawak. Markah terbaik bagi setiap jenis kuiz disimpan dalam pelayar anda.</p><button class="btn3" type="button" data-hq>Mula kuiz</button></div>
</section>
{ad(0)}
<section id="makhraj" aria-labelledby="h-makhraj">
<h2 id="h-makhraj">5 Kawasan Makhraj Huruf</h2>
{table(["Kawasan", "Huruf", "Penerangan"], mrows, "Kawasan makhraj huruf")}
<h2 id="baris">Baris & Tanda Bacaan</h2>
{table(["Tanda", "Contoh", "Bacaan"], hrows, "Baris dan tanda bacaan")}
</section>

<section id="kemajuan" class="tool" aria-labelledby="h-kem">
<h2 id="h-kem">✅ Senarai Semak Kemajuan Mengaji</h2>
<p class="prog" id="msp">0 / {len(I2.MILESTONES)} selesai</p>
<ul class="msl" id="msl">{ms}</ul>
<p class="note">Tanda disimpan dalam pelayar ini. Langkah seterusnya: <a href="/belajar-iqra/">Latihan Iqra'</a> · <a href="/belajar-tajwid/">Belajar Tajwid</a> · <a href="/#surah-1">Al-Fatihah dengan audio</a>.</p>
</section>

<section id="langkah" aria-labelledby="h-langkah">
<div class="prose">
<h2 id="h-langkah">Pelan Belajar Mengaji Untuk Dewasa</h2>
<ol class="steps">
<li><strong>Minggu pertama: huruf.</strong> Kenal bentuk dan nama 29 huruf menggunakan grid dan kuiz di atas. Beri perhatian kepada huruf yang hampir sama (ب ت ث, ج ح خ, د ذ, ر ز, س ش, ص ض, ط ظ, ع غ).</li>
<li><strong>Makhraj.</strong> Sebut setiap huruf dengan baris atas dari tempat keluarnya yang betul, terutama huruf halqi (ء ه ع ح غ خ) dan huruf tebal (خ ص ض غ ط ق ظ).</li>
<li><strong>Baris dan bacaan bersambung.</strong> Ikut tahap <a href="/belajar-iqra/">Iqra' 1 hingga 5</a>: baris, mad, tanwin, sukun, qalqalah, alif lam dan sabdu.</li>
<li><strong>Surah pendek.</strong> Mulakan dengan Al-Fatihah, kemudian <a href="/#surah-112">Al-Ikhlas</a>, <a href="/#surah-113">Al-Falaq</a>, <a href="/#surah-114">An-Nas</a> dan surah lain dalam <a href="/senarai-juzuk-al-quran/">Juz 30</a>, sambil mendengar qari ayat demi ayat.</li>
<li><strong>Tajwid.</strong> Pelajari hukum nun mati, mim mati dan mad dalam <a href="/belajar-tajwid/">Belajar Tajwid</a>, kemudian rancang <a href="/jadual-khatam-al-quran/">khatam pertama</a> anda.</li>
</ol>
</div>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Belajar Mengaji</h2>
{faq_html(faq)}
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("belajar-mengaji/")}</section>
</div>
{side([("huruf", "Huruf hijaiyah"), ("kuiz", "Kuiz huruf"), ("makhraj", "Makhraj huruf"), ("baris", "Baris & tanda"), ("kemajuan", "Senarai semak"), ("langkah", "Pelan dewasa"), ("faq", "Soalan lazim")], "belajar-mengaji/")}
</div>'''
    return [dict(path="belajar-mengaji/", kind="tool", data=False, arabic=True, published=PUB,
                 extra_data=f'<script type="application/json" id="hjdata">{J(data)}</script>',
                 title="Belajar Mengaji Dewasa: Huruf Hijaiyah, Makhraj & Kuiz",
                 ogtitle="Belajar Mengaji – Huruf Hijaiyah, Makhraj & Kuiz",
                 desc="Belajar mengaji dari asas: 29 huruf hijaiyah dengan nama, makhraj, bentuk sambung dan baris, kuiz 4 mod, pelan untuk dewasa dan senarai semak kemajuan.",
                 crumbs=[("Alat", "alat/"), ("Belajar Mengaji", None)], body=body, faq=faq,
                 app=dict(name="Belajar Mengaji: Huruf Hijaiyah", features=["29 huruf hijaiyah dengan nama dan makhraj", "Bentuk awal, tengah dan akhir", "Bacaan setiap baris, tanwin, sukun dan sabdu", "Kuiz 4 mod dengan markah terbaik", "Senarai semak 12 langkah kemajuan"]),
                 about=["Huruf hijaiyah", "Makhraj", "Membaca Al-Quran"],
                 llms="Belajar mengaji: 29 huruf hijaiyah (alif hingga ya, termasuk hamzah) dengan nama Melayu, makhraj (Al-Jauf, Al-Halq, Al-Lisan, Asy-Syafatan, Al-Khaisyum), bentuk sambung (huruf tidak bersambung ke kiri: ا د ذ ر ز و ء), baris (fathah, kasrah, dhammah, sukun, tanwin, syaddah, mad), kuiz dan pelan 5 langkah untuk dewasa.")]


def build_pages4(ctx):
    return build_ramadan(ctx) + build_solat(ctx) + build_iqra(ctx) + build_mengaji(ctx)
