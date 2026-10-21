"""Pages: /asmaul-husna/ (99 names with Quranic examples from data-surah/, memorisation tracker, flashcards, quiz, name of
the day) and /zakat-fitrah/ (rates per state, household calculator, rice weight, and the payment timeline of the coming
Ramadan from the Hijri calendar). alat.js mirrors zf_result, zf_timeline and name_of_day."""
import json, datetime as dt
import asmaul as A
import hijri as H
import solat as SL
import plans as P
from pages import e, faq_html, hero, side, meta_line, tool_cards, table, SITE
from pages2 import ayah, qref, quran_block, card

# ======================= ZAKAT FITRAH =======================
# 1447H / 2026 rates per person (RM), lowest first; each state's tiers follow the type of rice eaten
ZF_YEAR, ZF_HIJRI = 2026, 1447
ZF = {
    "perlis": [9], "kedah": [9, 15, 23], "pulau-pinang": [10, 15, 25], "perak": [10, 16, 25], "kelantan": [10, 22], "terengganu": [10, 20],
    "pahang": [8, 14, 21], "selangor": [8, 16, 25], "negeri-sembilan": [7.5, 12, 20], "melaka": [8, 15, 22], "johor": [8, 10, 20],
    "sabah": [7.5, 15], "sarawak": [7.5], "kuala-lumpur": [8, 15, 25], "labuan": [8, 15, 25],
}
ZF_SRC = {"johor": ("Bernama, 5 Februari 2026", "https://bernama.com/en/news.php?id=2520361"),
          "kuala-lumpur": ("Berita RTM (MAIWP)", "https://berita.rtm.gov.my/?p=437858"), "labuan": ("Berita RTM (MAIWP)", "https://berita.rtm.gov.my/?p=437858")}
TIER = ["Beras tempatan / kadar minimum", "Beras import", "Beras premium (cth: basmati)"]
GANTANG = 2.6  # kg of rice in one gantang Baghdad, the measure the councils price


def rm(x):
    return f"RM{x:,.2f}"


def zf_result(state, tier, n):
    """Household total (alat.js zfResult)."""
    r = ZF[state][min(tier, len(ZF[state]) - 1)]
    name = next(s[1] for s in SL.STATES if s[0] == state)
    return (f'<p class="zft">{rm(r * n)}</p><p>{n} orang × {rm(r)} ({e(TIER[min(tier, len(ZF[state]) - 1)])}, {e(name)}). '
            f'Jika dibayar dengan beras: <strong>{GANTANG * n:.1f} kg</strong> ({n} gantang Baghdad).</p>')


def zf_season(day):
    """The Hijri year whose Aidilfitri has not passed yet."""
    hy = H.g2h(day)[0]
    for y in (hy, hy + 1):
        if H.h2g(y, 10, 1)[0] >= day:
            return y
    return hy + 1


def zf_timeline(day):
    """Payment periods of the coming Ramadan (alat.js zfTimeline)."""
    y = zf_season(day)
    r1, o1 = H.h2g(y, 9, 1)
    eid, o2 = H.h2g(y, 10, 1)
    last = eid - dt.timedelta(1)
    rows = [("Harus (boleh) dibayar", f"{P.dlong(r1)} hingga sebelum Maghrib {P.dlong(last)}", "sepanjang Ramadan; ramai membayar awal"),
            ("Wajib", f"Maghrib {P.dlong(last)}", "masuk 1 Syawal: setiap Muslim yang hidup ketika itu wajib dizakatkan"),
            ("Paling afdal", f"Pagi {P.dlong(eid)}", "selepas Subuh hingga sebelum solat sunat Aidilfitri"),
            ("Makruh", f"{P.dlong(eid)}, selepas solat raya", "hingga terbenam matahari 1 Syawal"),
            ("Haram (wajib qada)", f"Selepas Maghrib {P.dlong(eid)}", "melewatkan tanpa uzur berdosa dan wajib diqada")]
    n = (r1 - day).days
    head = f"Ramadan {y} H {'bermula' if o1 else 'dijangka bermula'} {P.dlong(r1)}" + (f" · lagi {n} hari" if n > 0 else "")
    return f'<p class="swh">{head}</p><ul class="swr">' + "".join(f'<li><span class="swl">{a}</span><strong>{b}</strong><em>{c}</em></li>' for a, b, c in rows) + "</ul>"


def build_zakat(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    day = dt.date.fromisoformat(ctx.get("SOLAT_DAY") or T_)
    share, ad = ctx["share"], ctx["ad"]
    path = "zakat-fitrah/"
    names = {s[0]: s[1] for s in SL.STATES}
    rows = [[f"<strong>{e(names[k])}</strong>"] + [rm(v[i]) if i < len(v) else "–" for i in range(3)]
            + [f'<a href="{ZF_SRC[k][1]}" rel="noopener">{e(ZF_SRC[k][0])}</a>' if k in ZF_SRC else "Laporan media, Feb 2026"] for k, v in ZF.items()]
    opts = "".join(f'<option value="{k}"{" selected" if k == "selangor" else ""}>{e(names[k])}</option>' for k in ZF)
    lo, hi = min(v[0] for v in ZF.values()), max(v[-1] for v in ZF.values())
    faq = [
        (f"Berapa kadar zakat fitrah {ZF_YEAR}?", f"Kadar zakat fitrah {ZF_HIJRI}H/{ZF_YEAR} antara {rm(lo)} dan {rm(hi)} seorang, bergantung pada negeri dan jenis beras yang dimakan. Contohnya Selangor {', '.join(rm(x) for x in ZF['selangor'])}; Wilayah Persekutuan {', '.join(rm(x) for x in ZF['kuala-lumpur'])}. Jadual penuh 15 negeri ada di atas."),
        ("Siapa yang wajib membayar zakat fitrah?", "Setiap Muslim yang hidup pada akhir Ramadan dan awal Syawal (ketika terbenam matahari hari terakhir Ramadan) dan mempunyai lebihan makanan untuk diri dan tanggungannya pada hari raya. Ketua keluarga membayar untuk dirinya dan orang di bawah tanggungannya: isteri, anak dan ibu bapa yang ditanggung, termasuk bayi yang lahir sebelum Maghrib akhir Ramadan."),
        ("Bilakah waktu membayar zakat fitrah?", "Harus dibayar sejak awal Ramadan, wajib apabila masuk Maghrib malam raya, paling afdal pada pagi raya sebelum solat sunat Aidilfitri, makruh selepas solat raya, dan haram (wajib qada) jika dilewatkan selepas terbenam matahari 1 Syawal tanpa uzur. Tarikh sebenar Ramadan akan datang dikira di atas."),
        ("Kadar mana yang perlu saya pilih?", "Ikut jenis beras yang biasa dimakan oleh keluarga anda. Jika makan beras tempatan, kadar minimum memadai; jika beras import atau premium seperti basmati, bayar mengikut kadar beras tersebut. Membayar kadar lebih tinggi dibenarkan dan lebih baik."),
        ("Bolehkah zakat fitrah dibayar dengan beras?", f"Boleh menurut mazhab Syafi'i: satu gantang Baghdad (kira-kira {GANTANG} kg) beras makanan asasi bagi setiap orang. Di Malaysia, majlis agama juga menerima pembayaran wang mengikut kadar yang ditetapkan."),
        ("Di negeri mana saya perlu membayar zakat fitrah?", "Di negeri tempat anda berada ketika terbenam matahari pada hari terakhir Ramadan, iaitu ketika zakat fitrah menjadi wajib. Jika anda pulang beraya ke negeri lain sebelum itu, bayarlah mengikut kadar negeri tersebut."),
    ]
    body = hero(f"Kadar Zakat Fitrah {ZF_YEAR} Semua Negeri & Kalkulator",
                f"Kadar zakat fitrah {ZF_HIJRI}H bagi 15 negeri, kalkulator untuk seisi keluarga, berat beras, dan tarikh bayaran untuk Ramadan akan datang.",
                [("Zakat Fitrah", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira">🌾 Kalkulator Zakat Fitrah Keluarga</h2>
<form class="frm" id="zff" novalidate>
<div class="fl"><label for="zfs">Negeri (tempat anda berada pada malam raya)</label><select id="zfs">{opts}</select></div>
<div class="fl"><label for="zft">Jenis beras dimakan</label><select id="zft">{"".join(f'<option value="{i}">{e(TIER[i])}: {rm(ZF["selangor"][i])}</option>' for i in range(len(ZF["selangor"])))}</select></div>
<div class="fl"><label for="zfa">Dewasa (diri sendiri, isteri, ibu bapa ditanggung)</label><input id="zfa" type="number" min="0" max="50" value="2" inputmode="numeric"></div>
<div class="fl"><label for="zfk">Anak & bayi (lahir sebelum Maghrib akhir Ramadan)</label><input id="zfk" type="number" min="0" max="50" value="2" inputmode="numeric"></div>
</form>
<div class="jv" id="zfo" aria-live="polite">{zf_result("selangor", 0, 4)}</div>
<div class="sw2"><h3 id="h-tl">🗓 Bila Perlu Bayar: Ramadan Akan Datang</h3><div id="zfl">{zf_timeline(day)}</div>
<p class="note">Tarikh daripada <a href="/kalendar-hijrah/">kalendar Hijrah</a> (takwim JAKIM apabila tersedia); awal Ramadan dan Syawal tertakluk pengisytiharan rasmi.</p></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Kadar zakat fitrah {ZF_HIJRI}H/{ZF_YEAR} ialah <strong>{rm(lo)} hingga {rm(hi)} seorang</strong> mengikut negeri dan jenis beras; contohnya <strong>Selangor {", ".join(rm(x) for x in ZF["selangor"])}</strong> dan <strong>Wilayah Persekutuan {", ".join(rm(x) for x in ZF["kuala-lumpur"])}</strong>. Ia wajib bagi setiap Muslim (termasuk bayi) yang hidup ketika Maghrib malam raya, dibayar oleh ketua keluarga bagi tanggungannya, paling afdal pada pagi raya sebelum solat sunat Aidilfitri.</p></div>
{meta_line(day.isoformat(), f"{day.day} {P.BLN[day.month - 1]} {day.year}")}
{share(SITE + path, f"Kadar zakat fitrah {ZF_YEAR} semua negeri + kalkulator keluarga:")}
</div>
</section>

<section id="kadar" aria-labelledby="h-kadar">
<h2 id="h-kadar">Kadar Zakat Fitrah {ZF_YEAR} ({ZF_HIJRI}H) Mengikut Negeri</h2>
{table(["Negeri", "Kadar 1", "Kadar 2", "Kadar 3", "Sumber"], rows, f"Kadar zakat fitrah {ZF_YEAR}")}
<p class="note">Kadar seorang, mengikut jenis beras: kadar 1 untuk beras tempatan (minimum), kadar seterusnya untuk beras import dan premium. Kadar ditetapkan oleh majlis agama Islam negeri setiap tahun; sahkan dengan pusat zakat negeri anda sebelum membayar. Kadar {ZF_HIJRI + 1}H/{ZF_YEAR + 1} akan dikemas kini sebaik diumumkan (lazimnya Januari–Februari).</p>
</section>
{ad(0)}
<section id="hukum" aria-labelledby="h-hukum">
<h2 id="h-hukum">Hukum, Syarat & Dalil</h2>
<ul class="src">
<li>“Rasulullah SAW mewajibkan zakat fitrah satu sa' tamar atau satu sa' gandum ke atas setiap Muslim, hamba dan merdeka, lelaki dan perempuan, kecil dan besar, dan baginda memerintahkan supaya ia ditunaikan sebelum orang keluar menunaikan solat (hari raya)” (HR Al-Bukhari, no. 1503; Muslim, no. 984).</li>
<li>Zakat fitrah menyucikan orang yang berpuasa daripada perkara sia-sia dan kata-kata kotor, serta memberi makan orang miskin; sesiapa menunaikannya sebelum solat (hari raya), ia zakat yang diterima, dan selepas solat ia sedekah biasa (HR Abu Daud, no. 1609; Ibn Majah, no. 1827).</li>
<li>Syarat wajib: Islam, hidup ketika terbenam matahari hari terakhir Ramadan, dan mempunyai lebihan makanan bagi diri dan tanggungan pada malam dan hari raya.</li>
</ul>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Zakat Fitrah</h2>
{faq_html(faq)}
<p class="note">Lihat juga <a href="/waktu-berbuka-puasa/">waktu berbuka puasa & imsak</a>, <a href="/kalendar-hijrah/">kalendar Hijrah</a> dan <a href="/solat-sunat/solat-tarawih/">solat tarawih</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(path)}</section>
</div>
{side([("kira", "Kalkulator keluarga"), ("h-tl", "Bila perlu bayar"), ("kadar", "Kadar ikut negeri"), ("hukum", "Hukum & dalil"), ("faq", "Soalan lazim")], path)}
</div>'''
    zd = json.dumps({"r": ZF, "t": TIER, "n": {k: names[k] for k in ZF}, "g": GANTANG, **H.js_data()}, ensure_ascii=False, separators=(",", ":"))
    return dict(path=path, kind="tool", data=False, arabic=False, modified=day.isoformat(), extra_data=f'<script type="application/json" id="zfd">{zd}</script>',
                title=f"Kadar Zakat Fitrah {ZF_YEAR} Semua Negeri & Kalkulator Keluarga", ogtitle=f"Kadar Zakat Fitrah {ZF_YEAR} & Kalkulator",
                desc=f"Kadar zakat fitrah {ZF_HIJRI}H/{ZF_YEAR} 15 negeri (RM{lo:g}–RM{hi:g}), kalkulator seisi keluarga, berat beras dan tarikh bayar Ramadan akan datang.",
                crumbs=[("Zakat Fitrah", None)], body=body, faq=faq, about=["Zakat fitrah", "Ramadan", "Aidilfitri"],
                app=dict(name="Kalkulator Zakat Fitrah", features=["Kadar zakat fitrah 15 negeri", "Jumlah untuk seisi keluarga", "Berat beras (gantang Baghdad)", "Tarikh harus, wajib, afdal dan akhir bayaran"]),
                llms=f"Kadar zakat fitrah {ZF_HIJRI}H/{ZF_YEAR} setiap negeri (RM seorang): " + "; ".join(f"{names[k]} {'/'.join(f'{x:g}' for x in v)}" for k, v in ZF.items())
                     + f". Kalkulator keluarga, beras {GANTANG} kg seorang, tarikh bayaran Ramadan akan datang.")


# ======================= ASMAUL HUSNA =======================
def name_of_day(day):
    """Same index as alat.js: day of the year modulo 99."""
    return ((day - dt.date(day.year, 1, 1)).days) % 99


def build_asmaul(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    day = dt.date.fromisoformat(ctx.get("SOLAT_DAY") or T_)
    share, ad = ctx["share"], ctx["ad"]
    path = "asmaul-husna/"
    refs = A.quran_refs()
    cards = []
    for i, ((ar, ru, mn), r) in enumerate(zip(A.NAMES, refs), 1):
        q = (f'<span class="anq">{qref(*r)}</span>' if r else '<span class="anq">Daripada hadis; tidak disebut dalam bentuk ini dalam Al-Quran</span>')
        cards.append(f'<li class="anc" id="nama-{i}" data-q="{e((ru + " " + mn).lower())}"><span class="ann">{i}</span><span class="ana" lang="ar" dir="rtl">{e(ar)}</span>'
                     f'<span class="anr">{e(ru)}</span><span class="anm">{e(mn)}</span>{q}'
                     f'<label class="anh"><input type="checkbox" data-n="{i}"> Hafal</label></li>')
    t = name_of_day(day)
    ar, ru, mn = A.NAMES[t]
    k7 = quran_block([(7, 180)])
    faq = [
        ("Apakah maksud Asmaul Husna?", "Asmaul Husna bermaksud nama-nama Allah yang paling baik. Allah berfirman: “Dan Allah mempunyai nama-nama yang baik, maka berdoalah kepada-Nya dengan menyebut nama-nama itu” (Al-A'raf 7:180)."),
        ("Apakah kelebihan menghafal 99 nama Allah?", "Rasulullah SAW bersabda: “Sesungguhnya Allah mempunyai 99 nama, seratus kurang satu; sesiapa yang menghafalnya (ahsaha) akan masuk syurga” (HR Al-Bukhari, no. 2736; Muslim, no. 2677). Ulama menjelaskan “ahsaha” merangkumi menghafal, memahami makna dan beramal dengannya."),
        ("Adakah senarai 99 nama ini daripada hadis sahih?", "Hadis bahawa Allah mempunyai 99 nama adalah sahih. Senarai nama satu per satu yang masyhur pula terdapat dalam riwayat At-Tirmizi (no. 3507), dan ramai ulama hadis berpendapat senarai itu himpunan perawi, bukan sabda Nabi SAW. Semua nama dalam senarai ini thabit sebagai nama atau sifat Allah, dan sebahagian besarnya disebut dalam Al-Quran."),
        ("Bagaimana cara berdoa dengan Asmaul Husna?", "Pilih nama yang sesuai dengan hajat: “Ya Razzaq, urzuqni” (wahai Yang Maha Pemberi rezeki, rezekikanlah aku), “Ya Ghafur, ighfirli” (ampunkan aku), “Ya Tawwab, tub 'alayya” (terimalah taubatku). Ini mengikut perintah Al-A'raf 7:180."),
        ("Bagaimana cara cepat menghafal Asmaul Husna?", "Hafal 5 hingga 10 nama sehari bersama maknanya, ulang dengan kad hafalan dan kuiz di atas, dan tandakan “Hafal” untuk menjejak kemajuan. Dalam 2 hingga 3 minggu, 99 nama boleh dihafal dengan konsisten."),
    ]
    body = hero("Asmaul Husna: 99 Nama Allah, Maksud & Dalil Al-Quran",
                "99 nama Allah dengan tulisan Arab, rumi dan maksud, ayat Al-Quran yang menyebutnya, kad hafalan, kuiz dan penjejak hafalan.",
                [("Asmaul Husna", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira" class="sr">Asmaul Husna</h2>
<div class="and" id="and"><p class="swl">Nama hari ini · {P.dlong(day)}</p><p class="ana" lang="ar" dir="rtl" id="anda">{e(ar)}</p><p><strong id="andr">{t + 1}. {e(ru)}</strong> · <span id="andm">{e(mn)}</span></p></div>
<div class="chips2" id="anmode" role="group" aria-label="Mod"><button type="button" data-m="senarai" aria-pressed="true">Senarai</button><button type="button" data-m="kad" aria-pressed="false">Kad hafalan</button><button type="button" data-m="kuiz" aria-pressed="false">Kuiz</button></div>
<div id="anlist">
<div class="frm"><div class="fl w2"><label for="anq">Cari nama atau maksud</label><input id="anq" type="search" autocomplete="off" placeholder="cth: rezeki, pengampun, Ar-Razzaq"></div></div>
<p class="note" id="anp" aria-live="polite">0 / 99 dihafal</p>
<ol class="anl" id="anl">{"".join(cards)}</ol>
</div>
<div id="ankad" hidden><div class="ankd" id="ankd" tabindex="0" role="button" aria-label="Kad hafalan: tekan untuk lihat maksud"></div><div class="act"><button class="btn2" type="button" data-k="-1">‹ Sebelum</button><button class="btn3" type="button" data-k="0">Tunjuk maksud</button><button class="btn2" type="button" data-k="1">Seterusnya ›</button><button class="btn2" type="button" data-k="r">🔀 Rawak</button><button class="btn2" type="button" data-k="s">🔊 Dengar</button></div></div>
<div id="ankuiz" hidden><div class="qz" id="anqz"></div></div>
<div class="act"><button class="btn2" type="button" data-act="print">🖨 Cetak poster 99 nama</button><button class="btn2" type="button" data-act="link">🔗 Salin pautan</button></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Asmaul Husna ialah <strong>99 nama Allah yang paling baik</strong>, bermula dengan <strong>Ar-Rahman</strong> (Yang Maha Pemurah) dan <strong>Ar-Rahim</strong> (Yang Maha Mengasihani) hingga <strong>As-Sabur</strong> (Yang Maha Sabar). Sesiapa yang menghafal dan memahaminya dijanjikan syurga (HR Al-Bukhari, no. 2736; Muslim, no. 2677), dan kita disuruh berdoa dengannya (Al-A'raf 7:180). {sum(1 for r in refs if r)} daripada 99 nama di sini disertakan ayat Al-Quran yang menyebutnya.</p></div>
{meta_line(T_, TMS)}
{share(SITE + path, "Asmaul Husna: 99 nama Allah, maksud & ayat Al-Quran + kad hafalan:")}
</div>
</section>
{ad(0)}
<section class="dsec" id="dalil" aria-labelledby="h-dalil">
<h2 id="h-dalil">Dalil Asmaul Husna</h2>
{card("ayat-7-180", "Al-A'raf 180: berdoalah dengan nama-nama-Nya", k7[0], k7[1], k7[2], qref(7, 180))}
<ul class="src"><li>“Sesungguhnya Allah mempunyai 99 nama, seratus kurang satu; sesiapa yang menghafalnya akan masuk syurga” (HR Al-Bukhari, no. 2736; Muslim, no. 2677).</li>
<li>Senarai 99 nama yang masyhur: riwayat At-Tirmizi (no. 3507); menurut ramai ulama hadis, senarai ini himpunan perawi.</li>
<li>Ayat Al-Quran bagi setiap nama dipilih di mana nama itu jelas menyifatkan Allah, dan teksnya diambil terus daripada mushaf dalam laman ini.</li></ul>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Asmaul Husna</h2>
{faq_html(faq)}
<p class="note">Lihat juga <a href="/doa-harian/">himpunan doa harian</a>, <a href="/zikir-pagi-petang/">zikir pagi & petang</a> dan <a href="/tasbih-digital/">tasbih digital</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(path)}</section>
</div>
{side([("kira", "99 nama & hafalan"), ("dalil", "Dalil"), ("faq", "Soalan lazim")], path)}
</div>'''
    ad_ = json.dumps({"n": A.NAMES}, ensure_ascii=False, separators=(",", ":"))
    il = [{"@type": "ListItem", "position": i, "name": f"{ru} ({ar}): {mn}", "url": SITE + path + f"#nama-{i}"} for i, (ar, ru, mn) in enumerate(A.NAMES, 1)]
    return dict(path=path, kind="tool", data=False, arabic=True, modified=day.isoformat(), extra_data=f'<script type="application/json" id="asd">{ad_}</script>',
                title="Asmaul Husna: 99 Nama Allah, Maksud & Ayat Al-Quran", ogtitle="Asmaul Husna: 99 Nama Allah & Maksud",
                desc="99 nama Allah (Asmaul Husna) dalam Arab, rumi dan maksud Bahasa Melayu, dengan ayat Al-Quran, kad hafalan, kuiz dan penjejak hafalan.",
                crumbs=[("Asmaul Husna", None)], body=body, faq=faq, about=["Asmaul Husna", "Nama-nama Allah"],
                itemlist=dict(name="99 nama Allah (Asmaul Husna)", items=il),
                app=dict(name="Hafalan Asmaul Husna", features=["99 nama Allah dengan Arab, rumi dan maksud", "Ayat Al-Quran bagi setiap nama yang disebut", "Kad hafalan dan kuiz", "Penjejak hafalan 99 nama", "Nama hari ini"]),
                llms="Asmaul Husna (99 nama Allah) dengan Arab, rumi dan maksud Melayu, ayat Al-Quran yang menyebut setiap nama (diambil daripada mushaf), kad hafalan, kuiz, penjejak hafalan. Dalil: Al-A'raf 7:180; HR Al-Bukhari 2736, Muslim 2677; senarai At-Tirmizi 3507.")


def build_pages9(ctx):
    return [build_asmaul(ctx), build_zakat(ctx)]
