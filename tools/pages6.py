"""Pages: /kalendar-hijrah/ (official JAKIM Hijri date, month grid, converter, Islamic events, sunat fasting, Hijri age
and zakat haul) and /tahlil-ringkas/ (personalised tahlil with the doa's pronoun switched, audio, print booklet and a
large-screen majlis mode). Same page-dict contract as pages.py. The build-time HTML for the date-dependent parts must
equal what assets/js/alat.js draws for the same day (tools/test-alat.mjs checks it)."""
import json, datetime as dt
import hijri as H
import tahlil as T
import solat as SL
import ramadan as R
import plans as P
from pages import e, faq_html, hero, side, meta_line, tool_cards, SITE
from pages2 import ayah, qref, quran_block
from pages3 import areas

AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
DEF_ZONE = "WLY01"


def ar_date(h):
    return f"{str(h[2]).translate(AR_DIGITS)} {H.BH_AR[h[1] - 1]} {str(h[0]).translate(AR_DIGITS)} هـ"


def mon_title(y, m):
    """'Oktober 2026 · Rabiulakhir – Jamadilawal 1448 H' (alat.js monTitle)."""
    a = H.g2h(dt.date(y, m, 1))
    b = H.g2h(dt.date(y + m // 12, m % 12 + 1, 1) - dt.timedelta(1))
    if a[:2] == b[:2]:
        span = f"{H.BH[a[1] - 1]} {a[0]} H"
    elif a[0] == b[0]:
        span = f"{H.BH[a[1] - 1]} – {H.BH[b[1] - 1]} {b[0]} H"
    else:
        span = f"{H.BH[a[1] - 1]} {a[0]} – {H.BH[b[1] - 1]} {b[0]} H"
    return f"{P.BLN[m - 1]} {y} · {span}"


def ev_rows(day):
    """Upcoming events table body (alat.js evRows)."""
    out = []
    for k, name, note, h, g, o in H.events_from(day, 12):
        n = (g - day).days
        left = "Hari ini" if n == 0 else f"lagi {n} hari"
        out.append(f'<tr data-k="{k}"><td><strong>{name}</strong><span class="za">{note}</span></td><td>{H.hstr(h)}</td>'
                   f'<td>{P.dlong(g)}{"" if o else "*"}</td><td>{left}</td></tr>')
    return "".join(out)


def sunat_list(day):
    """Next strong sunat fasting days within 60 days (alat.js sunatList)."""
    out = []
    for i in range(60):
        d = day + dt.timedelta(i)
        if "a" in H.marks(d):
            h = H.g2h(d)
            why = "Hari Arafah" if (h[1], h[2]) == (12, 9) else "Tasu'a" if (h[1], h[2]) == (1, 9) else "Asyura" if (h[1], h[2]) == (1, 10) else "Ayyamul Bidh"
            out.append(f"<li><strong>{P.dshort(d)}</strong> · {H.hstr(h)} · {why}</li>")
        if len(out) == 6:
            break
    return "".join(out)


def today_parts(day, zone):
    h = H.g2h(day)
    nh = H.g2h(day + dt.timedelta(1))
    t, _ = R.day_times(zone, day)
    src = "takwim rasmi JAKIM" if h[3] else "anggaran kiraan (takwim JAKIM belum tersedia)"
    return (H.hstr(h), ar_date(h), f"{P.dlong(day)} · {src}",
            f"Hari Hijrah bermula waktu Maghrib: selepas {SL.hm(t[5])} (zon {zone}) masuk malam {nh[2]} {H.BH[nh[1] - 1]}.")


def build_kalendar(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    day = dt.date.fromisoformat(ctx.get("SOLAT_DAY") or T_)
    share, ad = ctx["share"], ctx["ad"]
    AREA = areas()
    h = H.g2h(day)
    big, ar, masihi, mag = today_parts(day, DEF_ZONE)
    evs = H.events_from(day, 12)
    nxt = {k: (hh, g, o) for k, _, _, hh, g, o in reversed(evs)}
    zopts = "".join(f'<option value="{z[0]}"{" selected" if z[0] == DEF_ZONE else ""}>{z[0]} · {e(AREA[z[0]][:48])}</option>' for z in SL.ZONES)
    # Islamic year tables: the current year and the next
    ytabs = []
    for hy in (h[0], h[0] + 1):
        rows = []
        for m in range(1, 13):
            g, o = H.h2g(hy, m, 1)
            ln, lo = H.month_len(hy, m)
            rows.append(f'<tr><td><strong>{m}. {H.BH[m - 1]}</strong> <span lang="ar" dir="rtl">{H.BH_AR[m - 1]}</span></td><td>{P.dlong(g)}{"" if o else "*"}</td>'
                        f'<td>{ln} hari{"" if lo else "*"}</td></tr>')
        g0, _ = H.h2g(hy, 1, 1)
        g1, _ = H.h2g(hy + 1, 1, 1)
        ytabs.append(f'<h3 id="tahun-{hy}">Kalendar Islam {hy} H ({g0.year}–{g1.year})</h3><div class="tw" tabindex="0" role="region" aria-label="Bulan Hijrah {hy}">'
                     f'<table class="plan hyt"><thead><tr><th scope="col">Bulan</th><th scope="col">1 haribulan (Masihi)</th><th scope="col">Bilangan hari</th></tr></thead>'
                     f'<tbody>{"".join(rows)}</tbody></table></div><p class="note">{hy} H: {(g1 - g0).days} hari, dari {P.dlong(g0)} hingga {P.dlong(g1 - dt.timedelta(1))}.</p>')
    ram, fitri, hijrah = nxt.get("ramadan"), nxt.get("aidilfitri"), nxt.get("maal-hijrah")
    lbl = lambda o: "takwim JAKIM" if o else "anggaran; tarikh rasmi diumumkan JAKIM"
    hd = json.dumps({**H.js_data(), "zc": {z[0]: [z[3], z[4]] for z in SL.ZONES}, "def": DEF_ZONE}, ensure_ascii=False, separators=(",", ":"))
    faq = [
        ("Apakah tarikh Hijrah hari ini?",
         f"Hari ini, {P.dlong(day)}, bersamaan {H.hstr(h)} mengikut {'takwim rasmi JAKIM' if h[3] else 'kiraan anggaran'}. Tarikh Hijrah bertukar pada waktu Maghrib, jadi malam ini sudah dikira {H.g2h(day + dt.timedelta(1))[2]} {H.BH[H.g2h(day + dt.timedelta(1))[1] - 1]}."),
    ]
    if ram:
        faq.append((f"Bilakah 1 Ramadan {ram[0][0]} H?", f"1 Ramadan {ram[0][0]} H jatuh pada {P.dlong(ram[1])} ({lbl(ram[2])}). Tarikh mula puasa yang muktamad diisytiharkan oleh Penyimpan Mohor Besar Raja-Raja selepas rukyah."))
    if fitri:
        faq.append((f"Bilakah Hari Raya Aidilfitri {fitri[1].year}?", f"1 Syawal {fitri[0][0]} H jatuh pada {P.dlong(fitri[1])} ({lbl(fitri[2])}), tertakluk pengisytiharan rasmi."))
    if hijrah:
        faq.append((f"Bilakah Awal Muharam (Maal Hijrah) {hijrah[0][0]} H?", f"1 Muharam {hijrah[0][0]} H jatuh pada {P.dlong(hijrah[1])} ({lbl(hijrah[2])})."))
    faq += [
        ("Kenapa hari dalam kalendar Hijrah bermula waktu Maghrib?",
         "Kalendar Hijrah ialah kalendar bulan (qamariah); hari baharu bermula apabila matahari terbenam. Sebab itu malam 1 Ramadan, malam Jumaat dan malam hari raya ialah malam sebelum tarikh Masihinya."),
        ("Kenapa tarikh Hijrah Malaysia kadang-kadang berbeza dengan Arab Saudi?",
         "Malaysia menetapkan awal bulan dengan rukyah dan kriteria imkanur rukyah MABIMS (anak bulan sekurang-kurangnya 3° tinggi dan elongasi 6.4°), manakala Arab Saudi menggunakan takwim Ummul Qura dan pengisytiharan rukyah tempatan. Kedudukan dan kriteria yang berbeza boleh menyebabkan beza satu hari."),
        ("Berapa hari dalam setahun Hijrah?",
         "354 atau 355 hari, kira-kira 11 hari lebih pendek daripada tahun Masihi. Setiap bulan Hijrah ada 29 atau 30 hari. Kerana itu Ramadan dan hari raya datang kira-kira 11 hari lebih awal setiap tahun Masihi."),
        ("Bagaimana mengira haul zakat?",
         "Haul ialah genap satu tahun Hijrah (354 atau 355 hari) harta dimiliki, bukan satu tahun Masihi. Masukkan tarikh mula pemilikan dalam kalkulator haul di atas untuk mendapatkan tarikh cukup haul. Untuk jumlah zakat, rujuk kalkulator zakat dan lembaga zakat negeri anda."),
    ]
    title = f"Tarikh Hijrah Hari Ini & Kalendar Islam {h[0]} H (Rasmi JAKIM)"
    body = hero(f"Tarikh Hijrah Hari Ini & Kalendar Islam {h[0]} H",
                "Tarikh Hijrah rasmi JAKIM, kalendar bulanan dengan hari puasa sunat, penukar tarikh, hari kebesaran Islam, umur Hijrah dan tarikh haul zakat.",
                [("Kalendar Hijrah", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira" class="sr">Tarikh Hijrah hari ini</h2>
<div class="htd">
<p class="hbig" id="hbig">{big}</p>
<p class="har" lang="ar" dir="rtl" id="har">{ar}</p>
<p class="sdate" id="hmas">{masihi}</p>
<p class="snext" id="hmag" aria-live="polite">{mag}</p>
<div class="fl"><label for="hz">Zon waktu Maghrib</label><select id="hz">{zopts}</select></div>
</div>
<div class="hnav"><button class="btn2 sm" type="button" id="hprev" aria-label="Bulan sebelumnya">‹</button><h3 id="hmt" aria-live="polite">{mon_title(day.year, day.month)}</h3><button class="btn2 sm" type="button" id="hnext" aria-label="Bulan seterusnya">›</button><button class="btn2 sm" type="button" id="htod">Hari ini</button></div>
<div class="hgrid" id="hgrid" role="grid" aria-label="Kalendar bulanan Masihi dan Hijrah">{H.grid_html(day.year, day.month, day)}</div>
<ul class="hleg"><li><span class="hc ma"></span>Puasa sunat utama (Ayyamul Bidh, Arafah, Asyura)</li><li><span class="hc mw"></span>Isnin & Khamis</li><li><span class="hc ms"></span>Puasa 6 Syawal</li><li><span class="hc mr"></span>Ramadan</li><li><span class="hc mh"></span>Haram berpuasa</li><li><span class="hc me"></span>Hari kebesaran</li></ul>
<p class="note">Nombor besar: tarikh Masihi · nombor kecil: tarikh Hijrah. * anggaran kiraan, belum ada dalam takwim JAKIM.</p>
<div class="act" id="hact"><button class="btn2" type="button" id="hics">📅 Simpan hari kebesaran & puasa sunat (.ics)</button><button class="btn2" type="button" data-act="link">🔗 Salin pautan</button><button class="btn2" type="button" data-act="print">🖨 Cetak</button></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Tarikh Hijrah hari ini, <strong>{P.dlong(day)}</strong>, ialah <strong id="hans">{big}</strong> mengikut {"takwim rasmi JAKIM" if h[3] else "kiraan anggaran"}. Hari Hijrah bermula waktu Maghrib.{f" 1 Ramadan {ram[0][0]} H jatuh pada <strong>{P.dlong(ram[1])}</strong> dan Aidilfitri pada <strong>{P.dlong(fitri[1])}</strong>." if ram and fitri else ""}</p></div>
{meta_line(day.isoformat(), f"{day.day} {P.BLN[day.month - 1]} {day.year}")}
{share(SITE + "kalendar-hijrah/", "Tarikh Hijrah hari ini & kalendar Islam rasmi JAKIM:")}
</div>
</section>

<section id="tukar" aria-labelledby="h-tukar">
<h2 id="h-tukar">Tukar Tarikh Masihi ↔ Hijrah</h2>
<form class="frm" id="hcf" novalidate>
<div class="fl w2"><label for="hg">Tarikh Masihi</label><input type="date" id="hg" value="{day.isoformat()}"></div>
<p class="hout w2" id="hgo" aria-live="polite">{day.isoformat()} = <strong>{H.hstr(h)}</strong>{"" if h[3] else " (anggaran)"}</p>
<div class="fl"><label for="hhd">Hari</label><select id="hhd">{"".join(f'<option{" selected" if i == h[2] else ""}>{i}</option>' for i in range(1, 31))}</select></div>
<div class="fl"><label for="hhm">Bulan Hijrah</label><select id="hhm">{"".join(f'<option value="{i}"{" selected" if i == h[1] else ""}>{H.BH[i - 1]}</option>' for i in range(1, 13))}</select></div>
<div class="fl"><label for="hhy">Tahun Hijrah</label><input type="number" id="hhy" min="1" max="1600" value="{h[0]}" inputmode="numeric"></div>
<p class="hout w2" id="hho" aria-live="polite">{H.hstr(h)} = <strong>{P.dlong(day)}</strong>{"" if h[3] else " (anggaran)"}</p>
</form>
<p class="note">Tarikh dalam julat takwim JAKIM ({P.dlong(H.dd(min(n for n in H._official_days())))} – {P.dlong(H.dd(max(n for n in H._official_days())))}) adalah rasmi. Di luar julat itu, kalendar tabular Islam digunakan; ia mungkin berbeza satu hari.</p>
</section>

<section id="kebesaran" aria-labelledby="h-keb">
<h2 id="h-keb">Hari Kebesaran Islam Akan Datang</h2>
<div class="tw" tabindex="0" role="region" aria-label="Hari kebesaran Islam"><table class="plan hev" id="hev">
<thead><tr><th scope="col">Peristiwa</th><th scope="col">Hijrah</th><th scope="col">Masihi</th><th scope="col">Lagi</th></tr></thead>
<tbody>{ev_rows(day)}</tbody></table></div>
<p class="note">Awal Ramadan, Aidilfitri dan Aidiladha ditentukan secara rasmi oleh pengisytiharan Penyimpan Mohor Besar Raja-Raja; cuti negeri mengikut warta negeri masing-masing. * anggaran.</p>
</section>
{ad(0)}
<section id="puasa-sunat" aria-labelledby="h-ps">
<h2 id="h-ps">Puasa Sunat Akan Datang</h2>
<ul class="hsl" id="hsl">{sunat_list(day)}</ul>
<ul class="src">
<li><strong>Isnin & Khamis:</strong> amalan dibentangkan kepada Allah pada hari tersebut (HR At-Tirmizi, no. 747).</li>
<li><strong>Ayyamul Bidh (13, 14, 15 setiap bulan Hijrah):</strong> seperti berpuasa sepanjang tahun (HR An-Nasa'i, no. 2420; At-Tirmizi, no. 761). Kecuali 13 Zulhijjah (hari tasyrik).</li>
<li><strong>Hari Arafah (9 Zulhijjah):</strong> menghapus dosa setahun lalu dan setahun akan datang; <strong>Asyura (10 Muharam):</strong> dosa setahun lalu (HR Muslim, no. 1162). Disunatkan juga Tasu'a, 9 Muharam (HR Muslim, no. 1134).</li>
<li><strong>Enam hari Syawal:</strong> seperti berpuasa setahun (HR Muslim, no. 1164).</li>
<li><strong>Haram berpuasa:</strong> Aidilfitri, Aidiladha (HR Al-Bukhari, no. 1990; Muslim, no. 1137) dan hari tasyrik 11–13 Zulhijjah (HR Muslim, no. 1141).</li>
</ul>
</section>

<section id="kalkulator" aria-labelledby="h-kal">
<h2 id="h-kal">Umur Hijrah & Tarikh Haul</h2>
<form class="frm" id="hkf" novalidate>
<div class="fl w2"><label for="hlahir">Tarikh lahir (Masihi)</label><input type="date" id="hlahir"></div>
<div class="hout w2" id="hlo" aria-live="polite"><p>Masukkan tarikh lahir untuk tarikh lahir Hijrah, umur dalam tahun Hijrah dan hari lahir Hijrah seterusnya.</p></div>
<div class="fl w2"><label for="hhaul">Tarikh mula memiliki harta (untuk haul zakat)</label><input type="date" id="hhaul"></div>
<div class="hout w2" id="hho2" aria-live="polite"><p>Haul zakat ialah genap satu tahun Hijrah (354 atau 355 hari).</p></div>
</form>
</section>

<section id="tahun" aria-labelledby="h-tahun">
<h2 id="h-tahun">Kalendar Islam {h[0]} H & {h[0] + 1} H</h2>
{"".join(ytabs)}
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Kalendar Hijrah</h2>
{faq_html(faq)}
<p class="note">Sumber: takwim Hijrah dalam jadual waktu solat JAKIM (e-solat.gov.my), disegerakkan setiap bulan. Untuk bacaan majlis arwah, lihat <a href="/tahlil-ringkas/">Tahlil Ringkas</a>; waktu solat harian di <a href="/waktu-solat/">Waktu Solat</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("kalendar-hijrah/")}</section>
</div>
{side([("kira", "Tarikh hari ini & kalendar"), ("tukar", "Tukar tarikh"), ("kebesaran", "Hari kebesaran"), ("puasa-sunat", "Puasa sunat"), ("kalkulator", "Umur Hijrah & haul"), ("tahun", f"Kalendar {h[0]} H"), ("faq", "Soalan lazim")], "kalendar-hijrah/")}
</div>'''
    return [dict(path="kalendar-hijrah/", kind="tool", data=False, arabic=False, modified=day.isoformat(), extra_data=f'<script type="application/json" id="hd">{hd}</script>',
                 title=title, ogtitle="Tarikh Hijrah Hari Ini & Kalendar Islam",
                 desc=f"Tarikh Hijrah hari ini rasmi JAKIM, kalendar Islam {h[0]} H dengan puasa sunat, penukar tarikh Masihi-Hijrah, hari kebesaran Islam, umur Hijrah & haul zakat.",
                 crumbs=[("Kalendar Hijrah", None)], body=body, faq=faq, about=["Kalendar Hijrah", "Takwim Islam", "Puasa sunat"],
                 app=dict(name="Kalendar Hijrah Malaysia", features=["Tarikh Hijrah hari ini daripada takwim rasmi JAKIM", "Hari Hijrah bertukar ikut waktu Maghrib zon anda",
                                                                     "Kalendar bulanan dengan puasa sunat dan hari haram berpuasa", "Penukar tarikh Masihi ↔ Hijrah",
                                                                     "Hari kebesaran Islam dengan kiraan hari dan fail kalendar (.ics)", "Umur Hijrah dan tarikh haul zakat"]),
                 llms=f"Tarikh Hijrah rasmi JAKIM ({H.hstr(h)} pada {day.isoformat()}), kalendar bulanan Masihi-Hijrah dengan puasa sunat (Isnin-Khamis, Ayyamul Bidh, Arafah, Asyura, 6 Syawal) dan hari haram berpuasa, penukar tarikh, hari kebesaran Islam"
                      + (f" (1 Ramadan {ram[0][0]} H: {ram[1].isoformat()}; Aidilfitri: {fitri[1].isoformat()})" if ram and fitri else "") + ", umur Hijrah dan haul zakat.")]


# ======================================================================================
def step_html(i, st):
    id_, title, kind, pay, n, src, note = st
    play = ""
    if kind == "q":
        refs = [(s, a) for s, a1, a2 in pay for a in range(a1, a2 + 1)]
        ar, ru, mn = quran_block(refs)
        src = (e(src) + " · " if src else "") + ", ".join(qref(s, a1) + (f"–{a2}" if a2 > a1 else "") for s, a1, a2 in pay)
        play = f'<button class="btn2 sm" type="button" data-play="{" ".join(f"{s}:{a}" for s, a in refs)}">▶ Dengar</button>'
    elif kind == "qs":
        s, a, first, ru, mn = pay
        ar = e(T.slice_from(ayah(s, a)["arabic"], first)) + f' <span class="an">﴿{a}﴾</span>'
        ru, mn = e(ru), e(mn)
        src = "Petikan " + qref(s, a)
    elif kind == "z":
        ar, ru, mn = (e(x) for x in pay)
        src = e(src)
    elif kind == "hadiah":
        ar, ru, mn = "", "", f'<span id="tlh">{e(T.hadiah("l"))}</span>'
        src = "Lafaz hadiah dalam Bahasa Melayu"
    else:  # doa
        ar, ru, mn = (f'<span id="tld{k}">{e(x)}</span>' for k, x in zip("arm", T.DOA["l"]))
        src = e(src)
    cnt = f'<button class="zc" type="button" data-id="tl-{id_}" data-n="{n}" data-t="{e(title)}">0 / {n}</button>' if n > 1 else ""
    txt = f"{title}\n\n" + "\n\n".join(x for x in (ar, ru, mn) if x)
    for tag in ('<span class="an">', '<span id="tlh">', '<span id="tlda">', '<span id="tldr">', '<span id="tldm">', "</span>"):
        txt = txt.replace(tag, "")
    return (f'<li class="dw zw tls" id="{id_}" data-txt="{e(txt)}"><header class="dh"><h3><span class="tln">{i}</span> {e(title)}</h3>{f"<span class=zn>{n}×</span>" if n > 1 else ""}</header>'
            + (f'<p class="dar" lang="ar" dir="rtl">{ar}</p>' if ar else "") + (f'<p class="dru"><em>{ru}</em></p>' if ru else "")
            + f'<p class="dmn">{"" if kind == "hadiah" else "<strong>Maksud:</strong> "}{mn}</p>' + (f'<p class="dnote">{e(note)}</p>' if note else "")
            + f'<footer class="df"><span class="dsrc">{src}</span><span class="dbtn">{play}{cnt}<button class="btn2 sm" type="button" data-copy>Salin</button></span></footer></li>')


def build_tahlil(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    steps = "".join(step_html(i, st) for i, st in enumerate(T.STEPS, 1))
    td = json.dumps({"doa": T.DOA, "gel": T.GELARAN, **H.js_data()}, ensure_ascii=False, separators=(",", ":"))
    jopts = "".join(f'<option value="{k}">{e(n)}</option>' for k, n in T.JANTINA)
    faq = [
        ("Apakah susunan bacaan tahlil ringkas?",
         "Hadiah Al-Fatihah, Al-Fatihah, Al-Ikhlas 3 kali, Al-Falaq, An-Nas, Al-Fatihah, awal Al-Baqarah (ayat 1–5), Al-Baqarah 163, Ayat Kursi, akhir Al-Baqarah (284–286), “Irhamna ya arhamar-rahimin” 7 kali, "
         "Hud 73, Al-Ahzab 33 dan 56, selawat, “Hasbunallah wa ni'mal-wakil”, istighfar 3 kali, “La ilaha illallah” (33 atau 100 kali), syahadah, selawat, tasbih, Al-Fatihah dan doa arwah."),
        ("Bagaimana menukar doa arwah untuk lelaki, perempuan atau ramai?",
         "Pilih “Untuk” di atas. Kata ganti dalam doa berubah secara automatik: “lahu, warhamhu” (lelaki), “laha, warhamha” (perempuan), “lahum, warhamhum” (ramai) dan “lahunna, warhamhunna” (ramai perempuan). Nama arwah juga dimasukkan ke dalam lafaz hadiah."),
        ("Bolehkah saya mencetak buku tahlil dengan nama arwah?",
         "Boleh. Isi nama arwah dan tarikh meninggal, pilih paparan (Arab dan Rumi sesuai untuk majlis), kemudian tekan “Cetak buku tahlil”. Kulit buku memaparkan nama arwah serta tarikh meninggal dalam Masihi dan Hijrah. Pilih “Simpan sebagai PDF” untuk berkongsi."),
        ("Bagaimana memaparkan tahlil di TV atau projektor masjid?",
         "Tekan “Mod majlis”. Setiap bacaan dipaparkan satu demi satu dengan tulisan besar; tekan anak panah, ruang kekunci atau ketik skrin untuk ke bacaan seterusnya. Skrin dikekalkan hidup sepanjang majlis jika pelayar menyokongnya."),
        ("Bilakah tarikh haul arwah mengikut kalendar Hijrah?",
         "Masukkan tarikh meninggal (Masihi). Halaman ini menukarnya kepada tarikh Hijrah dan mengira tarikh haul (ulang tahun kematian Hijrah) seterusnya dalam Masihi, kira-kira 11 hari lebih awal setiap tahun."),
        ("Adakah pahala tahlil sampai kepada si mati?",
         "Doa, istighfar dan sedekah untuk si mati disepakati sampai kepadanya (rujuk Al-Hasyr 59:10 dan HR Muslim, no. 1631). Tentang sampainya pahala bacaan Al-Quran, ulama berbeza pendapat; ramai ulama mazhab Syafi'i membenarkannya terutamanya apabila diiringi doa. Majlis tahlil diamalkan secara meluas di Malaysia; rujuk pejabat mufti negeri anda untuk pandangan rasmi."),
    ]
    howto = {"@type": "HowTo", "@id": SITE + "tahlil-ringkas/#cara", "name": "Cara membaca tahlil ringkas", "inLanguage": "ms-MY",
             "step": [{"@type": "HowToStep", "position": i, "name": st[1] + (f" ({st[4]} kali)" if st[4] > 1 else ""), "url": SITE + f"tahlil-ringkas/#{st[0]}"}
                      for i, st in enumerate(T.STEPS, 1)]}
    body = hero("Bacaan Tahlil Ringkas Lengkap: Rumi, Arab & Maksud",
                "Susunan tahlil ringkas dengan nama arwah dan doa yang menyesuaikan kata ganti, audio ayat, kaunter zikir, buku tahlil boleh cetak dan mod paparan besar untuk majlis.",
                [("Tahlil Ringkas", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool tlt" aria-labelledby="h-kira">
<h2 id="h-kira">Sediakan Tahlil untuk Arwah</h2>
<form class="frm" id="tlf" novalidate>
<div class="fl"><label for="tln">Nama arwah</label><input id="tln" maxlength="60" autocomplete="off" placeholder="cth: Ahmad"></div>
<div class="fl"><label for="tlb">Nama bapa (pilihan)</label><input id="tlb" maxlength="60" autocomplete="off" placeholder="cth: Ismail"></div>
<div class="fl"><label for="tlj">Untuk</label><select id="tlj">{jopts}</select></div>
<div class="fl"><label for="tld">Tarikh meninggal (pilihan)</label><input type="date" id="tld"></div>
</form>
<p class="note" id="tlhaul" aria-live="polite">Masukkan tarikh meninggal untuk tarikh Hijrah dan tarikh haul arwah.</p>
<div class="chips2" id="tlv" role="group" aria-label="Paparan"><button type="button" data-v="" aria-pressed="true">Semua</button><button type="button" data-v="ar-ru" aria-pressed="false">Arab + Rumi</button><button type="button" data-v="ar" aria-pressed="false">Arab</button><button type="button" data-v="ru" aria-pressed="false">Rumi</button></div>
<div class="act" id="tlact"><button class="btn3" type="button" id="tlbig">📺 Mod majlis</button><button class="btn2" type="button" id="tlprint">🖨 Cetak buku tahlil</button><button class="btn2" type="button" id="tlshare">🔗 Kongsi pautan tahlil</button><button class="btn2" type="button" id="tlplay">▶ Dengar semua ayat</button><button class="btn2 sm" type="button" data-fs="-1" aria-label="Kecilkan tulisan">A−</button><button class="btn2 sm" type="button" data-fs="1" aria-label="Besarkan tulisan">A+</button></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Tahlil ringkas dimulakan dengan <strong>hadiah Al-Fatihah</strong>, kemudian <strong>Al-Ikhlas (3 kali), Al-Falaq, An-Nas, Al-Fatihah, awal dan akhir Al-Baqarah serta Ayat Kursi</strong>, diikuti <strong>“Irhamna ya arhamar-rahimin” 7 kali</strong>, selawat, istighfar, <strong>“La ilaha illallah” 33 atau 100 kali</strong>, tasbih dan <strong>doa untuk arwah</strong>. Semua {len(T.STEPS)} bacaan ada di bawah mengikut susunan, dengan teks Al-Quran terus daripada mushaf.</p></div>
{meta_line(T_, TMS)}
{share(SITE + "tahlil-ringkas/", "Bacaan tahlil ringkas lengkap (Rumi, Arab & maksud) + doa arwah:")}
</div>
</section>

<section id="bacaan" class="zk tlb" aria-labelledby="h-bacaan">
<div class="tlcov" aria-hidden="true"><p class="tlct">Majlis Tahlil &amp; Doa Arwah</p><p class="tlcn" id="tlcn">Allahyarham [nama arwah]</p><p class="tlcd" id="tlcd"></p><p class="tlcs">quran.ilmualam.com/tahlil-ringkas</p></div>
<div class="zsec"><div class="zhd"><h2 id="h-bacaan">Bacaan Tahlil Ringkas</h2><p class="zprog" aria-live="polite">0 / {sum(1 for s in T.STEPS if s[4] > 1)} selesai hari ini</p><button class="btn2 sm" type="button" data-zreset>⟲ Set semula</button></div>
<ol class="tls-l" id="tls">{steps}</ol></div>
<div class="tlnav" id="tlnav" hidden><button class="btn2" type="button" data-nav="-1" aria-label="Sebelum">‹</button><span id="tlpos">1 / {len(T.STEPS)}</span><button class="btn2" type="button" data-nav="1" aria-label="Seterusnya">›</button><button class="btn2" type="button" data-nav="0" aria-label="Tutup mod majlis">✕</button></div>
</section>
{ad(0)}
<section id="adab" aria-labelledby="h-adab">
<h2 id="h-adab">Adab Majlis Tahlil</h2>
<ul class="src">
<li>Imam atau ketua majlis membaca bahagian pembuka dan doa; jemaah membaca surah dan zikir bersama-sama.</li>
<li>Bacaan zikir berulang (Irhamna 7 kali, La ilaha illallah 33 atau 100 kali) boleh dikira dengan butang kaunter pada setiap bacaan.</li>
<li>Doa untuk si mati disepakati manfaatnya: “Ya Tuhan kami, ampunilah kami dan saudara-saudara kami yang telah mendahului kami dengan iman” (Al-Hasyr 59:10).</li>
<li>Sedekah bagi pihak si mati sampai pahalanya (HR Muslim, no. 1631: amalan yang berterusan ialah sedekah jariah, ilmu bermanfaat dan anak soleh yang mendoakannya).</li>
</ul>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Tahlil</h2>
{faq_html(faq)}
<p class="note">Teks Al-Quran, rumi dan terjemahan diambil terus daripada mushaf dalam laman ini (<a href="/#surah">Baca Al-Quran</a>). Tarikh haul menggunakan <a href="/kalendar-hijrah/">Kalendar Hijrah</a> rasmi JAKIM. Cari <a href="/cari-masjid/">masjid & surau terdekat</a> untuk majlis.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards("tahlil-ringkas/")}</section>
</div>
{side([("kira", "Nama arwah & tetapan"), ("bacaan", "Bacaan tahlil"), ("doa", "Doa arwah"), ("adab", "Adab majlis"), ("faq", "Soalan lazim")], "tahlil-ringkas/")}
</div>'''
    return [dict(path="tahlil-ringkas/", kind="tool", data=False, arabic=True, extra_data=f'<script type="application/json" id="tdat">{td}</script>',
                 title="Bacaan Tahlil Ringkas (Rumi, Arab & Maksud) + Doa Arwah",
                 ogtitle="Bacaan Tahlil Ringkas Lengkap + Doa Arwah",
                 desc="Bacaan tahlil ringkas lengkap dalam Rumi, Arab dan maksud: nama arwah, doa ikut lelaki/perempuan, audio ayat, kaunter zikir, buku tahlil cetak dan mod majlis.",
                 crumbs=[("Tahlil Ringkas", None)], body=body, faq=faq, about=["Tahlil", "Doa arwah", "Majlis tahlil"], nodes=[howto],
                 app=dict(name="Tahlil Ringkas Interaktif", features=["Susunan tahlil ringkas lengkap: Arab, Rumi dan maksud", "Nama arwah dalam lafaz hadiah dan buku cetak",
                                                                       "Doa arwah ikut lelaki, perempuan atau ramai", "Audio ayat Al-Quran (Alafasy)", "Kaunter zikir berulang",
                                                                       "Mod majlis paparan besar untuk TV/projektor", "Tarikh haul arwah dalam kalendar Hijrah"]),
                 llms="Tahlil ringkas mengikut susunan di Malaysia: hadiah Al-Fatihah, Al-Fatihah, Al-Ikhlas 3x, Al-Falaq, An-Nas, Al-Baqarah 1–5, 163, 255, 284–286, Irhamna 7x, Hud 73, Al-Ahzab 33 & 56, selawat, Hasbunallah, istighfar, La ilaha illallah 33/100x, tasbih, doa arwah (HR Muslim 963) dalam 4 bentuk kata ganti, Al-Hasyr 59:10, Nuh 71:28. Cetak buku tahlil bernama, mod majlis, tarikh haul Hijrah.")]


def build_pages6(ctx):
    return build_kalendar(ctx) + build_tahlil(ctx)
