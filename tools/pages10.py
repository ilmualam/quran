"""Page: /zakat-pendapatan/ (income zakat, gross and net methods side by side, state nisab, deduction presets, and the
income-tax rebate under ITA 1967 s.6A(3) that shows what the zakat really costs). alat.js mirrors zp_calc and zp_result."""
import json, math
import solat as SL
from pages import e, faq_html, hero, side, meta_line, tool_cards, table, SITE
from pages2 import qref, quran_block, card

ZP_YEAR = 2026
RATE = 0.025
NISAB_G = 85  # grams of gold
GOLD = 455.86  # RM/g implied by the Selangor nisab below (38,748 / 85); used for states without a published figure
# state: (nisab RM, source label, url or None)
NISAB = {
    "selangor": (38748, "LZS, Julai–Disember 2026", "https://bayarzakat2u.com.my/nisab-zakat-selangor-2026/"),
    "kuala-lumpur": (33996, "PPZ-MAIWP 2026 (laporan)", "https://ecentral.my/zakat-pendapatan/"),
    "labuan": (33996, "PPZ-MAIWP 2026 (laporan)", "https://ecentral.my/zakat-pendapatan/"),
}
# deduction presets: diri, per isteri, per anak (RM a year)
PRESET = {
    "asas": ("Asas lazim", 9000, 3000, 1000),
    "lzs": ("Had kifayah LZS", 14580, 4944, 4896),
}
# resident individual income tax, YA2025 bands: (upper limit of band, rate)
BANDS = [(5000, 0), (20000, .01), (35000, .03), (50000, .06), (70000, .11), (100000, .19), (400000, .25), (600000, .26), (2000000, .28), (math.inf, .30)]
DEFAULT = dict(s="selangor", m="kasar", g=5000, el=0, b=0, o=0, p="lzs", d=14580, ni=1, ai=4944, nk=2, ak=4896, ib=0, kw=11, lt=0, ns=38748, rl=None)


def r2(x):
    """Round half up to sen (Math.floor(x*100+0.5)/100 in alat.js)."""
    return math.floor(x * 100 + 0.5) / 100


def rm(x):
    return f"RM{x:,.2f}"


def nisab_of(state):
    return NISAB[state][0] if state in NISAB else round(NISAB_G * GOLD)


def tax(ci):
    t, lo = 0.0, 0
    for hi, r in BANDS:
        if ci > lo:
            t += (min(ci, hi) - lo) * r
        lo = hi
    if ci <= 35000:
        t -= 400
    return max(0.0, t)


def zp_calc(i):
    """Both methods for one set of inputs; every amount a year."""
    wages = 12 * (i["g"] + i["el"]) + i["b"]
    total = wages + i["o"]
    kwsp = wages * i["kw"] / 100
    ded = i["d"] + i["ni"] * i["ai"] + i["nk"] * i["ak"] + i["ib"] + kwsp + i["lt"]
    relief = i["rl"] if i["rl"] is not None else 9000 + min(kwsp, 4000) + 2000 * i["nk"]
    tx = r2(tax(max(0.0, total - relief)))
    out = {"total": r2(total), "kwsp": r2(kwsp), "relief": r2(relief), "tax": tx}
    for m, base in (("kasar", total), ("bersih", max(0.0, total - ded))):
        z = r2(base * RATE) if base >= i["ns"] and base > 0 else 0.0
        rb = min(z, tx)
        out[m] = {"ded": r2(0 if m == "kasar" else ded), "base": r2(base), "ok": base >= i["ns"] and base > 0, "z": z, "mo": r2(z / 12), "rb": rb, "cost": r2(z - rb)}
    return out


def zp_result(i):
    c = zp_calc(i)
    m = c[i["m"]]
    nm = {"kasar": "kaedah kasar", "bersih": "kaedah bersih (dengan tolakan)"}
    if m["ok"]:
        head = f'<p class="jvh ok">✅ Wajib zakat pendapatan ({nm[i["m"]]})</p><p class="zft">{rm(m["z"])} <small>setahun</small></p>'
        head += (f'<p>Potongan gaji: <strong>{rm(m["mo"])} sebulan</strong> × 12. '
                 + (f'Zakat ini ditolak terus daripada cukai pendapatan (rebat {rm(m["rb"])}), jadi <strong>kos sebenar anda {rm(m["cost"])}</strong>.' if m["rb"] > 0
                    else "Tiada cukai untuk ditolak, jadi tiada rebat cukai.") + "</p>")
    else:
        head = (f'<p class="jvh no">❌ Belum cukup nisab ({nm[i["m"]]})</p><p>Pendapatan dikira {rm(m["base"])} kurang daripada nisab {rm(i["ns"])}. '
                f'Zakat pendapatan belum wajib; bersedekah tetap digalakkan.</p>')
    rows = [("Jumlah pendapatan setahun", rm(c["total"]), rm(c["total"])),
            ("Tolakan", "–", rm(c["bersih"]["ded"])),
            ("Pendapatan dikira", rm(c["kasar"]["base"]), rm(c["bersih"]["base"])),
            ("Cukup nisab?", "Ya" if c["kasar"]["ok"] else "Tidak", "Ya" if c["bersih"]["ok"] else "Tidak"),
            ("<strong>Zakat setahun (2.5%)</strong>", f'<strong>{rm(c["kasar"]["z"])}</strong>', f'<strong>{rm(c["bersih"]["z"])}</strong>'),
            ("Sebulan", rm(c["kasar"]["mo"]), rm(c["bersih"]["mo"])),
            ("Rebat cukai daripada zakat", rm(c["kasar"]["rb"]), rm(c["bersih"]["rb"])),
            ("<strong>Kos sebenar zakat</strong>", f'<strong>{rm(c["kasar"]["cost"])}</strong>', f'<strong>{rm(c["bersih"]["cost"])}</strong>')]
    tr = "".join(f"<tr><th scope=\"row\">{a}</th><td>{b}</td><td>{d}</td></tr>" for a, b, d in rows)
    return (head + '<div class="tw"><table class="zpt"><thead><tr><th scope="col">Perkara</th><th scope="col">Kasar</th><th scope="col">Bersih</th></tr></thead>'
            f'<tbody>{tr}</tbody></table></div><p class="note">Anggaran cukai sebelum zakat: <strong>{rm(c["tax"])}</strong> (pendapatan bercukai {rm(max(0, c["total"] - c["relief"]))} '
            f'selepas pelepasan {rm(c["relief"])}, kadar YA2025{", termasuk rebat diri RM400" if c["total"] - c["relief"] <= 35000 else ""}). '
            f'KWSP pekerja: {rm(c["kwsp"])}.</p>')


def fld(id_, label, val, step="1", mx="10000000", note=""):
    return (f'<div class="fl"><label for="{id_}">{label}</label><input id="{id_}" type="number" min="0" max="{mx}" step="{step}" value="{val:g}" inputmode="decimal">'
            f'{f"<small>{note}</small>" if note else ""}</div>')


def build_zp(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    path = "zakat-pendapatan/"
    names = {s[0]: s[1] for s in SL.STATES}
    d = DEFAULT
    opts = "".join(f'<option value="{k}"{" selected" if k == d["s"] else ""}>{e(v)}</option>' for k, v in names.items())
    c = zp_calc(d)
    nrows = [[f"<strong>{e(names[k])}</strong>", rm(v[0]), f'<a href="{v[2]}" rel="noopener">{e(v[1])}</a>'] for k, v in NISAB.items()]
    nrows.append(["Negeri lain", f"≈ {rm(nisab_of('johor'))}", f"Anggaran {NISAB_G} g emas × RM{GOLD:.2f}/g; sahkan dengan pusat zakat negeri"])
    pr = "".join(f'<button type="button" data-p="{k}" aria-pressed="{str(k == d["p"]).lower()}">{e(v[0])}</button>' for k, v in PRESET.items())
    ex = c["kasar"]
    faq = [
        (f"Berapa nisab zakat pendapatan {ZP_YEAR}?", f"Nisab ialah nilai {NISAB_G} gram emas setahun dan berbeza mengikut negeri. Contohnya Selangor {rm(NISAB['selangor'][0])} (Julai–Disember {ZP_YEAR}, LZS) dan Wilayah Persekutuan {rm(NISAB['kuala-lumpur'][0])} ({ZP_YEAR}, PPZ-MAIWP). Jika pendapatan setahun anda mencapai nisab, zakat 2.5% wajib dikeluarkan."),
        ("Bagaimana cara kira zakat pendapatan?", f"Kaedah kasar: 2.5% × jumlah pendapatan setahun. Contoh gaji RM5,000 sebulan: RM60,000 × 2.5% = {rm(ex['z'])} setahun atau {rm(ex['mo'])} sebulan. Kaedah bersih: tolak dahulu keperluan asas (diri, isteri, anak, ibu bapa, KWSP), kemudian 2.5% daripada bakinya jika masih cukup nisab."),
        ("Kaedah kasar atau bersih, mana satu patut saya pilih?", "Kedua-duanya diterima oleh pusat zakat. Kaedah kasar lebih mudah dan lebih berhati-hati (ihtiyat), dan menjadi pilihan kebanyakan pembayar melalui potongan gaji. Kaedah bersih sesuai jika tanggungan anda besar. Kalkulator di atas memaparkan kedua-duanya supaya anda boleh membandingkan."),
        ("Adakah zakat pendapatan mengurangkan cukai?", "Ya. Zakat yang dibayar kepada pusat zakat negeri ialah rebat cukai di bawah Seksyen 6A(3) Akta Cukai Pendapatan 1967: ia ditolak terus daripada cukai yang perlu dibayar, ringgit demi ringgit, setakat jumlah cukai anda. Simpan resit rasmi dan isikan di bahagian rebat zakat dalam e-Filing. Kalkulator ini menunjukkan kos sebenar zakat selepas rebat."),
        ("Adakah bonus, elaun dan pendapatan sampingan dikenakan zakat?", "Ya. Zakat pendapatan meliputi semua perolehan daripada usaha: gaji, elaun, bonus, insentif, komisen, pendapatan bebas (freelance), sewa, royalti dan dividen. Masukkan semuanya dalam jumlah setahun."),
        ("Bolehkah saya bayar zakat pendapatan setiap bulan?", "Boleh, dan ia cara paling mudah: melalui skim potongan gaji majikan, atau bayaran bulanan dalam talian ke pusat zakat negeri. Potongan bulanan juga diambil kira dalam PCB, jadi cukai bulanan anda turun serta-merta."),
        ("Adakah zakat pendapatan perlu cukup haul (setahun)?", "Menurut amalan pusat zakat di Malaysia, zakat pendapatan dikeluarkan ketika pendapatan diterima (seperti zakat hasil tanaman) dan tidak menunggu haul, berdasarkan pandangan al-mal al-mustafad. Nisab pula dinilai berdasarkan pendapatan setahun."),
    ]
    k267, k103 = quran_block([(2, 267)]), quran_block([(9, 103)])
    form = f'''<form class="frm" id="zpf" novalidate>
<div class="fl"><label for="zps">Negeri</label><select id="zps">{opts}</select></div>
<div class="fl"><label for="zpm">Kaedah</label><select id="zpm"><option value="kasar" selected>Kasar</option><option value="bersih">Bersih (tolakan)</option></select></div>
{fld("zpg", "Gaji pokok sebulan (RM)", d["g"])}
{fld("zpel", "Elaun tetap sebulan (RM)", d["el"])}
{fld("zpb", "Bonus & insentif setahun (RM)", d["b"])}
{fld("zpo", "Pendapatan lain setahun (RM)", d["o"], note="Freelance, sewa, dividen, royalti, komisen")}
<div class="jv" id="zpr" aria-live="polite">{zp_result(d)}</div>
<details class="zpx"><summary>Tolakan (kaedah bersih)</summary><div class="zpd">
<div class="chips2" id="zpp" role="group" aria-label="Pratetap tolakan">{pr}</div>
{fld("zpd", "Diri sendiri setahun (RM)", d["d"])}
{fld("zpni", "Bilangan isteri", d["ni"], mx="4")}
{fld("zpai", "Setiap isteri setahun (RM)", d["ai"])}
{fld("zpnk", "Bilangan anak", d["nk"], mx="30")}
{fld("zpak", "Setiap anak setahun (RM)", d["ak"])}
{fld("zpib", "Pemberian kepada ibu bapa setahun (RM)", d["ib"])}
{fld("zpkw", "Caruman KWSP pekerja (%)", d["kw"], step="0.5", mx="30")}
{fld("zplt", "Tolakan lain setahun (RM)", d["lt"], note="cth: caruman Tabung Haji, mengikut syarat negeri")}
</div></details>
<details class="zpx"><summary>Nisab & cukai pendapatan</summary><div class="zpd">
{fld("zpns", "Nisab negeri (RM)", d["ns"], note=f"Atau kira: {NISAB_G} g × harga emas")}
{fld("zpau", "Harga emas (RM segram)", GOLD, step="0.01", note="Mengubah ini mengira semula nisab")}
{fld("zprl", "Pelepasan cukai (RM)", c["relief"], note="Anggaran auto: individu RM9,000 + KWSP (maks RM4,000) + RM2,000 seorang anak. Ubah ikut borang e-Filing anda.")}
</div></details>
</form>'''
    body = hero(f"Kalkulator Zakat Pendapatan {ZP_YEAR}: Kasar, Bersih & Rebat Cukai",
                "Kira zakat gaji, bonus dan pendapatan sampingan dengan kedua-dua kaedah, semak nisab negeri, dan lihat berapa zakat itu menolak cukai pendapatan anda.",
                [("Zakat Pendapatan", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira">💼 Kalkulator Zakat Pendapatan</h2>
{form}
<p class="note">Data anda disimpan dalam peranti ini sahaja dan tidak dihantar ke mana-mana. Anggaran ini panduan; jumlah rasmi ditentukan oleh pusat zakat negeri anda.</p>
<div class="act"><button class="btn2" type="button" data-act="copy">📋 Salin keputusan</button><button class="btn2" type="button" data-act="reset">↺ Set semula</button></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Zakat pendapatan ialah <strong>2.5% daripada pendapatan setahun</strong> (gaji, elaun, bonus dan pendapatan sampingan) apabila jumlahnya mencapai <strong>nisab {NISAB_G} g emas</strong>: {rm(NISAB['selangor'][0])} di Selangor dan {rm(NISAB['kuala-lumpur'][0])} di Wilayah Persekutuan bagi {ZP_YEAR}. Gaji RM5,000 sebulan = <strong>{rm(ex['z'])} setahun ({rm(ex['mo'])} sebulan)</strong> dengan kaedah kasar. Zakat yang dibayar ditolak terus daripada cukai pendapatan (rebat Seksyen 6A(3)), jadi bagi kebanyakan pembayar cukai kosnya jauh lebih rendah daripada jumlah zakat.</p></div>
{meta_line(T_, TMS)}
{share(SITE + path, f"Kalkulator zakat pendapatan {ZP_YEAR}: kaedah kasar vs bersih + rebat cukai:")}
</div>
</section>

<section id="cara" aria-labelledby="h-cara">
<h2 id="h-cara">Cara Kira Zakat Pendapatan: 2 Kaedah</h2>
{table(["Langkah", "Kaedah kasar (tanpa tolakan)", "Kaedah bersih (dengan tolakan)"], [
        ["1", "Jumlahkan pendapatan setahun", "Jumlahkan pendapatan setahun"],
        ["2", "–", "Tolak keperluan asas: diri, isteri, anak, ibu bapa, KWSP"],
        ["3", "Bandingkan dengan nisab", "Bandingkan baki dengan nisab"],
        ["4", "Zakat = 2.5% × jumlah", "Zakat = 2.5% × baki"],
        ["Contoh gaji RM5,000, isteri 1, anak 2 (Selangor)", f"{rm(c['kasar']['z'])} setahun", f"{rm(c['bersih']['z'])} ({'cukup' if c['bersih']['ok'] else 'belum cukup'} nisab)"]], "Dua kaedah zakat pendapatan")}
<p class="note">Amaun tolakan berbeza mengikut negeri dan disemak semula dari semasa ke semasa. Pratetap “Had kifayah Selangor” menggunakan angka yang dilaporkan bagi LZS ({rm(PRESET['lzs'][1])} diri, {rm(PRESET['lzs'][2])} isteri, {rm(PRESET['lzs'][3])} anak 7–17 tahun); sahkan di kalkulator rasmi pusat zakat negeri anda.</p>
</section>

<section id="nisab" aria-labelledby="h-nisab">
<h2 id="h-nisab">Nisab Zakat Pendapatan {ZP_YEAR}</h2>
{table(["Negeri", "Nisab setahun", "Sumber"], nrows, f"Nisab zakat pendapatan {ZP_YEAR}")}
<p class="note">Nisab mengikut harga emas dan dikemas kini oleh pusat zakat (Selangor: dua kali setahun). Semak semula sebelum membuat bayaran.</p>
</section>
{ad(0)}
<section id="cukai" aria-labelledby="h-cukai">
<h2 id="h-cukai">Zakat Pendapatan & Cukai: Rebat, Bukan Pelepasan</h2>
<ul class="src">
<li><strong>Rebat</strong> ditolak terus daripada cukai yang perlu dibayar; <strong>pelepasan</strong> hanya mengurangkan pendapatan bercukai. Zakat ialah rebat (Seksyen 6A(3) Akta Cukai Pendapatan 1967).</li>
<li>Rebat terhad kepada jumlah cukai anda; zakat yang melebihi cukai tidak dipulangkan sebagai wang.</li>
<li>Zakat mesti dibayar kepada pusat zakat atau majlis agama Islam negeri, dalam tahun yang sama, dengan resit rasmi.</li>
<li>Melalui potongan gaji, zakat bulanan dikira bersama PCB, jadi gaji bersih anda hampir tidak berubah jika cukai bulanan anda melebihi zakat.</li>
</ul>
</section>

<section class="dsec" id="dalil" aria-labelledby="h-dalil">
<h2 id="h-dalil">Hukum & Dalil Zakat Pendapatan</h2>
{card("ayat-2-267", "Al-Baqarah 267: belanjakan sebahagian hasil usaha", k267[0], k267[1], k267[2], qref(2, 267))}
{card("ayat-9-103", "At-Taubah 103: ambillah zakat untuk menyucikan mereka", k103[0], k103[1], k103[2], qref(9, 103))}
<ul class="src"><li>Muzakarah Jawatankuasa Fatwa Majlis Kebangsaan Bagi Hal Ehwal Ugama Islam Malaysia (22 Jun 1997): zakat ke atas pendapatan penggajian adalah wajib bagi orang yang layak mengeluarkan zakat.</li>
<li>Kadar 2.5% dan nisab 85 g emas mengikut zakat wang dan emas; pendapatan dizakatkan ketika diterima menurut pandangan al-mal al-mustafad yang diamalkan pusat zakat di Malaysia.</li>
<li>Penjelasan lanjut: <a href="https://www.ilmualam.com/2025/11/cara-kira-zakat-pendapatan.html">Cara kira zakat pendapatan: hukum & nisab</a> (IlmuAlam).</li></ul>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Zakat Pendapatan</h2>
{faq_html(faq)}
<p class="note">Lihat juga <a href="/zakat-fitrah/">kadar zakat fitrah semua negeri</a> dan <a href="/kalendar-hijrah/">kalendar Hijrah</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(path)}</section>
</div>
{side([("kira", "Kalkulator"), ("cara", "Cara kira: 2 kaedah"), ("nisab", "Nisab ikut negeri"), ("cukai", "Rebat cukai"), ("dalil", "Hukum & dalil"), ("faq", "Soalan lazim")], path)}
</div>'''
    zd = json.dumps({"n": {k: v[0] for k, v in NISAB.items()}, "au": GOLD, "g": NISAB_G, "p": {k: v[1:] for k, v in PRESET.items()}, "bd": [[h if h != math.inf else 1e15, r] for h, r in BANDS],
                     "def": DEFAULT}, ensure_ascii=False, separators=(",", ":"))
    return dict(path=path, kind="tool", data=False, arabic=True, extra_data=f'<script type="application/json" id="zpdat">{zd}</script>',
                title=f"Kalkulator Zakat Pendapatan {ZP_YEAR}: Kasar, Bersih & Rebat Cukai", ogtitle=f"Kalkulator Zakat Pendapatan {ZP_YEAR}",
                desc=f"Kira zakat gaji, bonus & pendapatan sampingan {ZP_YEAR}: kaedah kasar vs bersih, nisab negeri, potongan bulanan dan kos sebenar selepas rebat cukai.",
                crumbs=[("Zakat Pendapatan", None)], body=body, faq=faq, about=["Zakat pendapatan", "Zakat", "Cukai pendapatan"],
                app=dict(name="Kalkulator Zakat Pendapatan", features=["Kaedah kasar dan bersih serentak", "Nisab ikut negeri atau harga emas", "Pratetap tolakan had kifayah", "Potongan gaji bulanan", "Rebat cukai dan kos sebenar zakat"]),
                llms=f"Zakat pendapatan {ZP_YEAR}: 2.5% pendapatan setahun jika cukup nisab 85 g emas (Selangor RM{NISAB['selangor'][0]:,}, WP RM{NISAB['kuala-lumpur'][0]:,}). "
                     f"Gaji RM5,000 sebulan = {rm(ex['z'])} setahun (kaedah kasar). Zakat ialah rebat cukai (s.6A(3) ACP 1967). Kalkulator kasar vs bersih dan kos selepas rebat.")
