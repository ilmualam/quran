"""Pages: /zakat-simpanan/ (savings, ASB, Tabung Haji, FD on the lowest balance of the haul, Hijri 2.5% or Gregorian 2.577%,
haul date from the Hijri calendar), /zakat-emas/ (kept and worn gold, state uruf, purity) and /zakat-perniagaan/ (working
capital method, Muslim ownership share). alat.js mirrors zs_result, ze_result and zb_result."""
import json
import solat as SL
import hijri as H
from pages import e, faq_html, hero, side, meta_line, tool_cards, table, SITE
from pages2 import qref, quran_block, card
from pages10 import r2, rm as _rm, NISAB, NISAB_G, GOLD, nisab_of

RATES = {"h": (0.025, "2.5% (tahun Hijrah)"), "m": (0.02577, "2.577% (tahun Masihi)")}
# worn-jewellery exemption (uruf) per state, grams; 0 = no uruf (all gold counts towards the 85 g nisab)
URUF = {"terengganu": 850, "selangor": 800, "kuala-lumpur": 800, "labuan": 800, "kelantan": 600, "perak": 500, "pahang": 500, "johor": 425,
        "pulau-pinang": 250, "negeri-sembilan": 200, "kedah": 200, "melaka": 180, "sabah": 152, "sarawak": 90, "perlis": 0}
PURITY = [(999, "999 (24K)"), (916, "916 (22K)"), (875, "875 (21K)"), (750, "750 (18K)")]
ACC = ["Akaun simpanan & semasa bank", "ASB / ASNB", "Tabung Haji", "Simpanan tetap (FD)", "Lain-lain (unit amanah, akaun pelaburan)"]
NAMES = {s[0]: s[1] for s in SL.STATES}


def rm(x):
    return _rm(r2(x))


def num(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def gram(x):
    return f"{r2(x):,.2f} g"


def state_opts(sel):
    return "".join(f'<option value="{k}"{" selected" if k == sel else ""}>{e(v)}</option>' for k, v in NAMES.items())


def haul_sel(id_):
    return (f'<div class="fl"><label for="{id_}">Tahun haul</label><select id="{id_}"><option value="h" selected>Hijrah (2.5%)</option>'
            '<option value="m">Masihi (2.577%)</option></select></div>')


def fld(id_, label, val, step="1", mx="100000000", note=""):
    return (f'<div class="fl"><label for="{id_}">{label}</label><input id="{id_}" type="number" min="0" max="{mx}" step="{step}" value="{val:g}" inputmode="decimal">'
            f'{f"<small>{note}</small>" if note else ""}</div>')


def nisab_note():
    return f"Selangor {rm(NISAB['selangor'][0])}, WP {rm(NISAB['kuala-lumpur'][0])}; negeri lain ≈ {NISAB_G} g × harga emas"


def verdict(ok, title, z, extra):
    if ok:
        return f'<p class="jvh ok">✅ Wajib {title}</p><p class="zft">{rm(z)}</p>{extra}'
    return f'<p class="jvh no">❌ Belum wajib {title}</p>{extra}'


# ======================= ZAKAT SIMPANAN =======================
ZS_DEF = dict(s="selangor", hy="h", b=[20000, 30000, 0, 0, 0], d=[0, 1500, 0, 0, 0], dv=True, ns=NISAB["selangor"][0])


def zs_result(i):
    rate, rl = RATES[i["hy"]]
    total = sum(i["b"]) + (sum(i["d"]) if i["dv"] else 0)
    if total <= 0:
        return "<p>Masukkan baki terendah simpanan anda.</p>"
    ok = total >= i["ns"]
    z = r2(total * rate) if ok else 0.0
    extra = (f'<p>{rl} × {rm(total)}. Zakat simpanan juga layak rebat cukai pendapatan (Seksyen 6A(3)).</p>' if ok
             else f'<p>Jumlah dikira {rm(total)} kurang daripada nisab {rm(i["ns"])}.</p>')
    tr = "".join(f'<tr><th scope="row">{ACC[k]}</th><td data-l="Baki terendah">{rm(i["b"][k])}</td><td data-l="Dividen/hibah">{rm(i["d"][k]) if i["dv"] else "–"}</td><td data-l="Dikira">{rm(i["b"][k] + (i["d"][k] if i["dv"] else 0))}</td></tr>'
                 for k in range(len(ACC)) if i["b"][k] or i["d"][k])
    return (verdict(ok, "zakat simpanan", z, extra) + '<div class="tw"><table class="zpt rt"><thead><tr><th scope="col">Akaun</th><th scope="col">Baki terendah</th>'
            f'<th scope="col">Dividen/hibah</th><th scope="col">Dikira</th></tr></thead><tbody>{tr}<tr><th scope="row"><strong>Jumlah</strong></th><td></td><td></td>'
            f'<td data-l="Dikira"><strong>{rm(total)}</strong></td></tr></tbody></table></div>')


def build_simpanan(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    path = "zakat-simpanan/"
    d = ZS_DEF
    rows = "".join(f'<div class="zsrow"><span class="zsn">{e(a)}</span>{fld(f"zsb{k}", "Baki terendah setahun (RM)", d["b"][k])}{fld(f"zsd{k}", "Dividen/hibah (RM)", d["d"][k])}</div>'
                   for k, a in enumerate(ACC))
    ex = r2(51500 * 0.025)
    faq = [
        ("Bagaimana cara kira zakat simpanan?", f"Ambil baki terendah setiap akaun dalam tempoh setahun (haul), campurkan semua akaun, tambah dividen atau hibah yang diterima, dan jika jumlahnya mencapai nisab ({NISAB_G} g emas), zakatnya 2.5% (tahun Hijrah) atau 2.577% (tahun Masihi). Contoh: baki terendah RM20,000 + ASB RM30,000 + dividen RM1,500 = RM51,500 × 2.5% = {rm(ex)}."),
        ("Kenapa baki terendah, bukan baki akhir tahun?", "Baki terendah ialah jumlah yang pasti dimiliki sepanjang haul. Wang yang masuk dan keluar dalam tahun itu tidak cukup setahun dalam milikan. Ini kaedah yang digunakan kebanyakan pusat zakat di Malaysia untuk akaun simpanan biasa."),
        ("Adakah ASB dan Tabung Haji kena zakat?", "Ya. ASB/ASNB dan simpanan Tabung Haji ialah simpanan milik penuh, jadi dicampur dengan akaun lain untuk menilai nisab. Bagi ASB, pusat zakat lazimnya mengira baki terendah serta dividen dan bonus; sebahagian ulama berpandangan hanya dividen. Sahkan dengan pusat zakat negeri anda."),
        ("Apa beza kadar 2.5% dan 2.577%?", "2.5% untuk haul tahun Hijrah (354 hari). Jika anda mengira mengikut tahun Masihi (365 hari), kadarnya 2.577% kerana tahun Masihi lebih panjang 11 hari."),
        ("Adakah KWSP kena zakat simpanan?", "Menurut fatwa kebangsaan, simpanan KWSP konvensional tidak dizakatkan selagi belum dikeluarkan kerana belum milik sempurna; zakat dibayar apabila wang dikeluarkan. KWSP Simpanan Shariah kini menawarkan zakat perniagaan secara kolektif bagi ahli yang memilihnya."),
        ("Bila tarikh bayar zakat simpanan?", "Pada hujung haul, iaitu setahun selepas simpanan anda mula mencapai nisab. Masukkan tarikh mula dalam kalkulator di atas untuk dapatkan tarikh tepat mengikut kalendar Hijrah. Ramai memilih satu tarikh tetap setiap tahun (contohnya 1 Ramadan) supaya mudah diingat."),
    ]
    k34 = quran_block([(9, 34)])
    form = f'''<form class="frm" id="zsf" novalidate>
<div class="fl"><label for="zss">Negeri</label><select id="zss">{state_opts(d["s"])}</select></div>
{haul_sel("zsh")}
<div class="zsacc">{rows}</div>
<label class="zck"><input type="checkbox" id="zsdv" checked> Campurkan dividen/hibah yang diterima</label>
<div class="jv" id="zsr" aria-live="polite">{zs_result(d)}</div>
<details class="zpx"><summary>Nisab & tarikh haul</summary><div class="zpd">
{fld("zsn", "Nisab negeri (RM)", d["ns"], note=nisab_note())}
{fld("zsau", "Harga emas (RM segram)", GOLD, step="0.01", note="Mengubah ini mengira semula nisab")}
<div class="fl"><label for="zsmula">Tarikh simpanan mula cukup nisab</label><input type="date" id="zsmula"><small>Tarikh haul dikira mengikut kalendar Hijrah</small></div>
<div class="fl" id="zsho" aria-live="polite"></div>
</div></details>
</form>'''
    body = hero("Kalkulator Zakat Simpanan, ASB & Tabung Haji 2026",
                "Kira zakat wang simpanan bank, ASB, Tabung Haji dan simpanan tetap dengan kaedah baki terendah, kadar Hijrah atau Masihi, dan tarikh cukup haul.",
                [("Zakat Simpanan", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira">🏦 Kalkulator Zakat Simpanan</h2>
{form}
<p class="note">Data disimpan dalam peranti ini sahaja. Anggaran ini panduan; jumlah rasmi ditentukan oleh pusat zakat negeri anda.</p>
<div class="act" id="zsact"><button class="btn2" type="button" data-act="copy">📋 Salin keputusan</button><button class="btn2" type="button" data-act="reset">↺ Set semula</button></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Zakat simpanan wajib apabila <strong>jumlah baki terendah semua akaun</strong> (bank, ASB, Tabung Haji, simpanan tetap) dalam setahun mencapai <strong>nisab {NISAB_G} g emas</strong> ({rm(NISAB['selangor'][0])} di Selangor, {rm(NISAB['kuala-lumpur'][0])} di Wilayah Persekutuan). Kadarnya <strong>2.5%</strong> bagi tahun Hijrah atau <strong>2.577%</strong> bagi tahun Masihi. Contoh: RM51,500 × 2.5% = <strong>{rm(ex)}</strong>.</p></div>
{meta_line(T_, TMS)}
{share(SITE + path, "Kalkulator zakat simpanan, ASB & Tabung Haji 2026:")}
</div>
</section>

<section id="cara" aria-labelledby="h-cara">
<h2 id="h-cara">Cara Kira Zakat Simpanan: 4 Langkah</h2>
<ol class="steps"><li><strong>Cari baki terendah</strong> setiap akaun dalam tempoh setahun (semak penyata bulanan).</li>
<li><strong>Campurkan semua akaun</strong>: bank, ASB/ASNB, Tabung Haji, simpanan tetap, unit amanah.</li>
<li><strong>Tambah dividen/hibah</strong> yang diterima dalam tahun itu.</li>
<li>Jika jumlah ≥ nisab, <strong>zakat = jumlah × 2.5%</strong> (Hijrah) atau 2.577% (Masihi).</li></ol>
</section>
{ad(0)}
<section class="dsec" id="dalil" aria-labelledby="h-dalil">
<h2 id="h-dalil">Hukum & Dalil</h2>
{card("ayat-9-34", "At-Taubah 34: amaran kepada penyimpan emas dan perak", k34[0], k34[1], k34[2], qref(9, 34))}
<ul class="src"><li>Wang kertas mengambil hukum emas dan perak sebagai nilai harta; zakatnya 2.5% apabila cukup nisab dan haul.</li>
<li>“Tidak ada zakat pada harta sehingga berlalu ke atasnya haul (setahun)” (HR Abu Daud, no. 1573; Ibn Majah, no. 1792).</li></ul>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Zakat Simpanan</h2>
{faq_html(faq)}
<p class="note">Lihat juga <a href="/zakat-emas/">zakat emas</a>, <a href="/zakat-pendapatan/">zakat pendapatan</a> dan <a href="/zakat-perniagaan/">zakat perniagaan</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(path)}</section>
</div>
{side([("kira", "Kalkulator"), ("cara", "Cara kira"), ("dalil", "Hukum & dalil"), ("faq", "Soalan lazim")], path)}
</div>'''
    zd = json.dumps({"n": {k: v[0] for k, v in NISAB.items()}, "au": GOLD, "g": NISAB_G, "acc": ACC, "def": ZS_DEF, **H.js_data()}, ensure_ascii=False, separators=(",", ":"))
    return dict(path=path, kind="tool", data=False, arabic=True, extra_data=f'<script type="application/json" id="zsdat">{zd}</script>',
                title="Kalkulator Zakat Simpanan, ASB & Tabung Haji 2026", ogtitle="Kalkulator Zakat Simpanan 2026",
                desc="Kira zakat wang simpanan, ASB, Tabung Haji & simpanan tetap 2026: baki terendah, nisab negeri, kadar 2.5% atau 2.577%, dan tarikh cukup haul.",
                crumbs=[("Zakat Simpanan", None)], body=body, faq=faq, about=["Zakat simpanan", "Zakat", "ASB"],
                app=dict(name="Kalkulator Zakat Simpanan", features=["5 jenis akaun termasuk ASB dan Tabung Haji", "Kaedah baki terendah + dividen", "Kadar Hijrah 2.5% atau Masihi 2.577%", "Tarikh cukup haul mengikut kalendar Hijrah"]),
                llms=f"Zakat simpanan: 2.5% (Hijrah) atau 2.577% (Masihi) daripada jumlah baki terendah semua akaun + dividen jika ≥ nisab {NISAB_G} g emas (Selangor RM{NISAB['selangor'][0]:,}). Contoh RM51,500 → {rm(ex)}.")


# ======================= ZAKAT EMAS =======================
ZE_DEF = dict(s="selangor", hy="h", au=GOLD, g=[100, 150, 0], k=[999, 916, 916])


def ze_calc(i):
    u = URUF[i["s"]]
    kept = i["g"][0] * i["k"][0] / 1000 + i["g"][2] * i["k"][2] / 1000
    exg = max(0.0, i["g"][1] - u) if u else i["g"][1]
    exp = exg * i["k"][1] / 1000
    tot = kept + exp
    ok = tot > 0 and (tot >= NISAB_G or (u > 0 and exg > 0))
    return u, exg, exp, tot, ok


def ze_result(i):
    rate, rl = RATES[i["hy"]]
    if sum(i["g"]) <= 0:
        return "<p>Masukkan berat emas anda.</p>"
    u, exg, exp, tot, ok = ze_calc(i)
    val = r2(tot * i["au"])
    z = r2(val * rate) if ok else 0.0
    un = f"uruf {NAMES[i['s']]} {u} g" if u else f"{NAMES[i['s']]} tiada uruf"
    extra = (f'<p>{gram(tot)} emas tulen × RM{num(i["au"])}/g = {rm(val)} × {rl}.</p>' if ok
             else f'<p>Emas dikira {gram(tot)} tulen, kurang daripada nisab {NISAB_G} g; emas dipakai tidak melebihi {un}.</p>')
    rows = [("Emas simpanan (jongkong, syiling, akaun emas)", 0, i["g"][0] * i["k"][0] / 1000),
            (f"Perhiasan dipakai ({un})", 1, exp),
            ("Perhiasan tidak dipakai / disimpan", 2, i["g"][2] * i["k"][2] / 1000)]
    tr = "".join(f'<tr><th scope="row">{a}</th><td data-l="Berat">{gram(i["g"][k])}</td><td data-l="Ketulenan">{i["k"][k]}</td><td data-l="Dikira (tulen)">{gram(c)}</td></tr>' for a, k, c in rows if i["g"][k])
    return (verdict(ok, "zakat emas", z, extra) + '<div class="tw"><table class="zpt rt"><thead><tr><th scope="col">Jenis</th><th scope="col">Berat</th>'
            f'<th scope="col">Ketulenan</th><th scope="col">Dikira (tulen)</th></tr></thead><tbody>{tr}<tr><th scope="row"><strong>Jumlah</strong></th><td></td><td></td>'
            f'<td data-l="Dikira (tulen)"><strong>{gram(tot)}</strong></td></tr></tbody></table></div>')


def build_emas(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    path = "zakat-emas/"
    d = ZE_DEF
    pur = lambda id_, v: f'<select id="{id_}" aria-label="Ketulenan">' + "".join(f'<option value="{k}"{" selected" if k == v else ""}>{t}</option>' for k, t in PURITY) + "</select>"
    rowh = lambda id_, lab, k: (f'<div class="zsrow"><span class="zsn">{lab}</span>{fld(f"zeg{k}", "Berat (gram)", d["g"][k], step="0.01")}'
                                f'<div class="fl"><label for="zek{k}">Ketulenan</label>{pur(f"zek{k}", d["k"][k])}</div></div>')
    ur = sorted(URUF.items(), key=lambda x: -x[1])
    urows = [[f"<strong>{e(NAMES[k])}</strong>", f"{v} g" if v else "Tiada uruf (semua emas dikira)"] for k, v in ur]
    c0 = ze_calc(d)
    faq = [
        ("Berapa nisab zakat emas?", f"Nisab zakat emas ialah {NISAB_G} gram emas tulen yang disimpan cukup setahun (haul). Kadarnya 2.5% daripada nilai emas pada harga semasa."),
        ("Adakah emas perhiasan yang dipakai kena zakat?", "Emas perhiasan yang dipakai secara uruf (kebiasaan) tidak dikenakan zakat. Jika beratnya melebihi had uruf negeri anda, lebihan itu wajib dizakatkan. Had uruf berbeza mengikut negeri, contohnya Selangor dan Wilayah Persekutuan 800 g, Terengganu 850 g, Kedah 200 g."),
        ("Bagaimana cara kira zakat emas simpanan?", "Darabkan berat emas dengan ketulenannya untuk mendapat berat emas tulen (contoh 100 g emas 916 = 91.6 g tulen). Jika jumlah emas simpanan ≥ 85 g tulen dan cukup setahun, zakat = berat tulen × harga emas segram × 2.5%."),
        ("Harga emas mana yang digunakan?", "Harga emas semasa (biasanya harga belian/jualan emas 999 segram) pada tarikh cukup haul. Masukkan harga terkini dalam kalkulator; pusat zakat negeri juga menerbitkan harga rujukan."),
        ("Emas perhiasan yang disimpan dan tidak dipakai bagaimana?", "Perhiasan yang tidak dipakai (disimpan sebagai simpanan) dikira seperti emas simpanan: dicampur ke dalam nisab 85 g tanpa pengecualian uruf."),
        ("Adakah akaun emas atau emas digital kena zakat?", "Ya. Akaun pelaburan emas dan emas digital ialah emas simpanan; ia dicampur bersama jongkong dan syiling untuk menilai nisab."),
    ]
    k34 = quran_block([(9, 34)])
    form = f'''<form class="frm" id="zef" novalidate>
<div class="fl"><label for="zes">Negeri</label><select id="zes">{state_opts(d["s"])}</select></div>
{haul_sel("zeh")}
{fld("zeau", "Harga emas 999 (RM segram)", d["au"], step="0.01", note="Masukkan harga semasa")}
<div class="zsacc">{rowh("zeg0", "Emas simpanan (jongkong, syiling, akaun emas)", 0)}{rowh("zeg1", "Perhiasan dipakai", 1)}{rowh("zeg2", "Perhiasan tidak dipakai / disimpan", 2)}</div>
<div class="jv" id="zer" aria-live="polite">{ze_result(d)}</div>
</form>'''
    body = hero("Kalkulator Zakat Emas 2026: Simpanan, Perhiasan & Uruf Negeri",
                "Kira zakat emas simpanan dan perhiasan mengikut ketulenan (999, 916, 750) dan had uruf negeri anda.",
                [("Zakat Emas", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira">🥇 Kalkulator Zakat Emas</h2>
{form}
<p class="note">Data disimpan dalam peranti ini sahaja. Anggaran ini panduan; jumlah rasmi ditentukan oleh pusat zakat negeri anda.</p>
<div class="act" id="zeact"><button class="btn2" type="button" data-act="copy">📋 Salin keputusan</button><button class="btn2" type="button" data-act="reset">↺ Set semula</button></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Zakat emas <strong>2.5%</strong> wajib ke atas emas simpanan apabila beratnya mencapai <strong>nisab {NISAB_G} g emas tulen</strong> dan disimpan setahun. Emas perhiasan yang <strong>dipakai</strong> dikecualikan sehingga <strong>had uruf negeri</strong> (contohnya 800 g di Selangor dan Wilayah Persekutuan); hanya lebihannya dizakatkan. Contoh: 100 g emas 999 + 150 g perhiasan 916 dipakai di Selangor = {gram(c0[3])} dikira.</p></div>
{meta_line(T_, TMS)}
{share(SITE + path, "Kalkulator zakat emas 2026 + uruf setiap negeri:")}
</div>
</section>

<section id="uruf" aria-labelledby="h-uruf">
<h2 id="h-uruf">Had Uruf Emas Perhiasan Setiap Negeri</h2>
{table(["Negeri", "Uruf (berat perhiasan dipakai yang dikecualikan)"], urows, "Uruf emas perhiasan setiap negeri")}
<p class="note">Senarai dihimpun daripada fatwa dan laporan negeri (Selangor: fatwa 22 Mei 2018; Kelantan: keputusan MAIK 26 Januari 2025; <a href="https://siraplimau.com/kadar-uruf-emas-2025/" rel="noopener">senarai 2025</a>). Uruf boleh berubah; sahkan dengan majlis agama Islam negeri anda.</p>
</section>
{ad(0)}
<section class="dsec" id="dalil" aria-labelledby="h-dalil">
<h2 id="h-dalil">Hukum & Dalil</h2>
{card("ayat-9-34", "At-Taubah 34: amaran kepada penyimpan emas dan perak", k34[0], k34[1], k34[2], qref(9, 34))}
<ul class="src"><li>Nisab emas 20 dinar (kira-kira 85 g) dan zakatnya setengah dinar, iaitu 2.5% (HR Abu Daud, no. 1573).</li>
<li>Panduan lanjut: <a href="https://www.thebukitbesi.com/2022/01/cara-kira-zakat-emas.html">cara kira zakat emas</a>.</li></ul>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Zakat Emas</h2>
{faq_html(faq)}
<p class="note">Lihat juga <a href="/zakat-simpanan/">zakat simpanan & ASB</a>, <a href="/zakat-pendapatan/">zakat pendapatan</a> dan <a href="/faraid/">kalkulator faraid</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(path)}</section>
</div>
{side([("kira", "Kalkulator"), ("uruf", "Uruf setiap negeri"), ("dalil", "Hukum & dalil"), ("faq", "Soalan lazim")], path)}
</div>'''
    zd = json.dumps({"u": URUF, "nm": NAMES, "g": NISAB_G, "au": GOLD, "def": ZE_DEF}, ensure_ascii=False, separators=(",", ":"))
    return dict(path=path, kind="tool", data=False, arabic=True, extra_data=f'<script type="application/json" id="zedat">{zd}</script>',
                title="Kalkulator Zakat Emas 2026: Simpanan, Perhiasan & Uruf", ogtitle="Kalkulator Zakat Emas 2026",
                desc="Kira zakat emas simpanan & perhiasan 2026 ikut ketulenan 999/916/750 dan had uruf 15 negeri. Nisab 85 g, kadar 2.5%, jadual uruf lengkap.",
                crumbs=[("Zakat Emas", None)], body=body, faq=faq, about=["Zakat emas", "Zakat", "Emas perhiasan"],
                app=dict(name="Kalkulator Zakat Emas", features=["Emas simpanan dan perhiasan", "Ketulenan 999, 916, 875, 750", "Had uruf 15 negeri", "Kadar Hijrah atau Masihi"]),
                llms=f"Zakat emas: 2.5% emas simpanan ≥ {NISAB_G} g tulen setahun; perhiasan dipakai dikecualikan sehingga uruf negeri: " + "; ".join(f"{NAMES[k]} {v} g" for k, v in ur) + ".")


# ======================= ZAKAT PERNIAGAAN =======================
ZB_DEF = dict(s="selangor", hy="h", t=50000, st=80000, p=30000, a=0, l=60000, x=0, m=100, ns=NISAB["selangor"][0])


def zb_result(i):
    rate, rl = RATES[i["hy"]]
    aset = i["t"] + i["st"] + i["p"] + i["a"]
    base0 = max(0.0, aset - i["l"] - i["x"])
    base = base0 * i["m"] / 100
    if aset <= 0:
        return "<p>Masukkan aset semasa perniagaan anda.</p>"
    ok = base >= i["ns"] and base > 0
    z = r2(base * rate) if ok else 0.0
    extra = (f'<p>{rl} × {rm(base)} (modal kerja bersih bahagian Muslim).</p>' if ok
             else f'<p>Modal kerja bersih {rm(base)} kurang daripada nisab {rm(i["ns"])}.</p>')
    rows = [("Jumlah aset semasa", rm(aset)), ("Tolak liabiliti semasa", rm(i["l"])), ("Tolak pelarasan", rm(i["x"])),
            ("Modal kerja bersih", rm(base0)), (f"Bahagian pemilikan Muslim ({num(i['m'])}%)", rm(base)), ("<strong>Zakat perniagaan</strong>", f"<strong>{rm(z)}</strong>")]
    tr = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in rows)
    return verdict(ok, "zakat perniagaan", z, extra) + f'<div class="tw"><table class="zpt"><tbody>{tr}</tbody></table></div>'


def build_perniagaan(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    path = "zakat-perniagaan/"
    d = ZB_DEF
    faq = [
        ("Bagaimana cara kira zakat perniagaan?", "Gunakan kaedah modal kerja: (tunai + stok pada nilai pasaran + penghutang yang dijangka diterima + aset semasa lain) − liabiliti semasa − pelarasan. Jika baki ≥ nisab, zakat = baki × 2.5% (tahun kewangan Hijrah) atau 2.577% (tahun kewangan Masihi). Contoh dalam kalkulator: modal kerja RM100,000 × 2.5% = RM2,500."),
        ("Siapa wajib zakat perniagaan?", "Perniagaan milik Muslim (penuh atau sebahagian) yang cukup nisab dan haul: perniagaan tunggal, perkongsian, syarikat Sdn Bhd dan koperasi. Bagi pemilikan bercampur, hanya bahagian pemegang saham Muslim yang dizakatkan."),
        ("Apakah aset yang tidak dikira?", "Aset tetap seperti bangunan, mesin, kenderaan dan peralatan tidak dizakatkan kerana tidak untuk dijual. Pelarasan juga menolak aset yang tidak dimiliki sempurna atau tidak halal, mengikut garis panduan pusat zakat."),
        ("Adakah zakat perniagaan mengurangkan cukai?", "Bagi individu (perniagaan tunggal/perkongsian), zakat yang dibayar layak sebagai rebat cukai di bawah Seksyen 6A(3). Bagi syarikat, zakat perniagaan dibenarkan sebagai potongan cukai sehingga 2.5% daripada pendapatan agregat (Seksyen 44(11A) Akta Cukai Pendapatan 1967)."),
        ("Bila zakat perniagaan dibayar?", "Pada akhir tahun kewangan perniagaan, berdasarkan penyata kewangan (kunci kira-kira) tarikh tersebut."),
    ]
    k267 = quran_block([(2, 267)])
    form = f'''<form class="frm" id="zbf" novalidate>
<div class="fl"><label for="zbs">Negeri</label><select id="zbs">{state_opts(d["s"])}</select></div>
{haul_sel("zbh")}
{fld("zbt", "Tunai & baki bank (RM)", d["t"])}
{fld("zbst", "Stok / inventori, nilai pasaran (RM)", d["st"])}
{fld("zbp", "Penghutang dijangka diterima (RM)", d["p"])}
{fld("zba", "Aset semasa lain (RM)", d["a"], note="cth: deposit boleh tunai, pelaburan jangka pendek")}
{fld("zbl", "Liabiliti semasa (RM)", d["l"], note="Pemiutang, hutang jangka pendek, cukai belum bayar")}
{fld("zbx", "Pelarasan, tolak (RM)", d["x"], note="Aset tidak dimiliki sempurna atau tidak halal")}
{fld("zbm", "Pemilikan Muslim (%)", d["m"], step="0.01", mx="100")}
<div class="jv" id="zbr" aria-live="polite">{zb_result(d)}</div>
<details class="zpx"><summary>Nisab</summary><div class="zpd">
{fld("zbn", "Nisab negeri (RM)", d["ns"], note=nisab_note())}
{fld("zbau", "Harga emas (RM segram)", GOLD, step="0.01", note="Mengubah ini mengira semula nisab")}
</div></details>
</form>'''
    body = hero("Kalkulator Zakat Perniagaan 2026: Kaedah Modal Kerja",
                "Kira zakat perniagaan tunggal, perkongsian dan syarikat daripada kunci kira-kira: aset semasa, liabiliti, pelarasan dan bahagian pemilikan Muslim.",
                [("Zakat Perniagaan", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira">🏪 Kalkulator Zakat Perniagaan</h2>
{form}
<p class="note">Data disimpan dalam peranti ini sahaja. Anggaran ini panduan; untuk syarikat, rujuk akauntan dan pusat zakat negeri.</p>
<div class="act" id="zbact"><button class="btn2" type="button" data-act="copy">📋 Salin keputusan</button><button class="btn2" type="button" data-act="reset">↺ Set semula</button></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Zakat perniagaan = <strong>(aset semasa − liabiliti semasa ± pelarasan) × 2.5%</strong> (tahun kewangan Hijrah) atau <strong>2.577%</strong> (Masihi), apabila modal kerja bersih mencapai <strong>nisab {NISAB_G} g emas</strong>. Aset tetap (bangunan, mesin, kenderaan) tidak dikira. Contoh: tunai RM50,000 + stok RM80,000 + penghutang RM30,000 − liabiliti RM60,000 = RM100,000 → zakat <strong>RM2,500</strong>.</p></div>
{meta_line(T_, TMS)}
{share(SITE + path, "Kalkulator zakat perniagaan 2026 (kaedah modal kerja):")}
</div>
</section>

<section id="cara" aria-labelledby="h-cara">
<h2 id="h-cara">Kaedah Modal Kerja</h2>
{table(["Masuk", "Tolak"], [["Tunai dan baki bank", "Liabiliti semasa (pemiutang, hutang jangka pendek)"], ["Stok pada nilai pasaran", "Pelarasan: aset tidak dimiliki sempurna"], ["Penghutang yang dijangka diterima", "Pelarasan: hasil tidak halal"], ["Aset semasa lain", "Aset tetap tidak dikira langsung"]], "Kaedah modal kerja")}
</section>
{ad(0)}
<section class="dsec" id="dalil" aria-labelledby="h-dalil">
<h2 id="h-dalil">Hukum & Dalil</h2>
{card("ayat-2-267", "Al-Baqarah 267: belanjakan sebahagian hasil usaha", k267[0], k267[1], k267[2], qref(2, 267))}
<ul class="src"><li>Samurah bin Jundub: Rasulullah SAW menyuruh kami mengeluarkan zakat daripada barang yang kami sediakan untuk jualan (HR Abu Daud, no. 1562; sanadnya diperselisihkan, namun zakat perdagangan disepakati jumhur ulama).</li></ul>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Zakat Perniagaan</h2>
{faq_html(faq)}
<p class="note">Lihat juga <a href="/zakat-pendapatan/">zakat pendapatan</a>, <a href="/zakat-simpanan/">zakat simpanan</a> dan <a href="/zakat-emas/">zakat emas</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(path)}</section>
</div>
{side([("kira", "Kalkulator"), ("cara", "Kaedah modal kerja"), ("dalil", "Hukum & dalil"), ("faq", "Soalan lazim")], path)}
</div>'''
    zd = json.dumps({"n": {k: v[0] for k, v in NISAB.items()}, "au": GOLD, "g": NISAB_G, "def": ZB_DEF}, ensure_ascii=False, separators=(",", ":"))
    return dict(path=path, kind="tool", data=False, arabic=True, extra_data=f'<script type="application/json" id="zbdat">{zd}</script>',
                title="Kalkulator Zakat Perniagaan 2026: Kaedah Modal Kerja", ogtitle="Kalkulator Zakat Perniagaan 2026",
                desc="Kira zakat perniagaan 2026 dengan kaedah modal kerja: aset semasa, liabiliti, pelarasan, pemilikan Muslim, nisab negeri dan kadar 2.5% atau 2.577%.",
                crumbs=[("Zakat Perniagaan", None)], body=body, faq=faq, about=["Zakat perniagaan", "Zakat", "Perniagaan"],
                app=dict(name="Kalkulator Zakat Perniagaan", features=["Kaedah modal kerja", "Pelarasan dan pemilikan Muslim", "Nisab negeri", "Kadar Hijrah atau Masihi"]),
                llms="Zakat perniagaan (kaedah modal kerja): (aset semasa − liabiliti semasa ± pelarasan) × bahagian Muslim × 2.5% (Hijrah) / 2.577% (Masihi) jika ≥ nisab 85 g emas. Aset tetap tidak dikira.")


def build_pages11(ctx):
    return [build_simpanan(ctx), build_emas(ctx), build_perniagaan(ctx)]
