"""Page: /faraid/ (inheritance calculator per tools/faraid.py, net estate after debts, funeral costs and the one-third bequest
cap, excluded heirs with the reason, Baitulmal or radd). alat.js mirrors faraid_html and the estate line."""
import json
import faraid as FR
from pages import e, faq_html, hero, side, meta_line, tool_cards, table, SITE
from pages2 import qref, quran_block, card

FR_DEF = dict(sx="l", g=300000, db=0, fu=0, ws=0, h={"is": 1, "ib": 1, "bp": 1, "al": 2, "ap": 1})
GROUPS = [("Pasangan, ibu bapa, datuk & nenek", ["su", "is", "bp", "ib", "dt", "ni", "nb"], True),
          ("Anak & cucu", ["al", "ap", "cl", "cp"], True),
          ("Adik-beradik", ["skl", "skp", "sbl", "sbp", "sil", "sip"], False),
          ("Waris lain (anak saudara, bapa saudara, sepupu)", ["ask", "asb", "bsk", "bsb", "spk", "spb"], False)]


def est_line(e_, w):
    return f"Harta bersih selepas hutang, kos jenazah{f' dan wasiat {FR.fmt_sen(w)}' if w else ' dan wasiat'}: <strong>{FR.fmt_sen(e_)}</strong>"


def heir_input(k, d):
    v = d["h"].get(k, 0)
    hid = " hidden" if (k == "su" and d["sx"] == "l") or (k == "is" and d["sx"] == "p") else ""
    if FR.MAXN[k] == 1:
        return f'<label class="zck frck" id="frw-{k}"{hid}><input type="checkbox" id="fr-{k}"{" checked" if v else ""}> {e(FR.LABEL[k])}</label>'
    return (f'<div class="fl" id="frw-{k}"{hid}><label for="fr-{k}">{e(FR.LABEL[k])}</label><input id="fr-{k}" type="number" min="0" max="{FR.MAXN[k]}" value="{v}" inputmode="numeric"></div>')


def build_faraid(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    path = "faraid/"
    d = FR_DEF
    e0, w0 = FR.estate(d["g"] * 100, d["db"] * 100, d["fu"] * 100, d["ws"] * 100)
    groups = "".join(f'<details class="zpx"{" open" if op else ""}><summary>{e(t)}</summary><div class="zpd">{"".join(heir_input(k, d) for k in ks)}</div></details>'
                     for t, ks, op in GROUPS)
    f = lambda id_, lab, v, note="": (f'<div class="fl"><label for="{id_}">{lab}</label><input id="{id_}" type="number" min="0" max="100000000" step="0.01" value="{v:g}" inputmode="decimal">'
                                     f'{f"<small>{note}</small>" if note else ""}</div>')
    form = f'''<form class="frm" id="frf" novalidate>
<div class="fl"><label for="frsx">Si mati</label><select id="frsx"><option value="l" selected>Lelaki</option><option value="p">Perempuan</option></select></div>
{f("frg", "Jumlah harta (RM)", d["g"])}
{f("frdb", "Hutang si mati (RM)", d["db"])}
{f("frfu", "Kos pengurusan jenazah (RM)", d["fu"])}
{f("frws", "Wasiat kepada bukan waris (RM)", d["ws"], "Dihadkan 1/3 harta selepas hutang")}
<p class="fl w2 frest" id="fre">{est_line(e0, w0)}</p>
{groups}
<label class="zck"><input type="checkbox" id="frrd"> Kembalikan baki kepada waris (radd) dan bukan Baitulmal</label>
<div class="jv" id="frr" aria-live="polite">{FR.faraid_html(d["h"], e0)}</div>
</form>'''
    faq = [
        ("Apakah faraid?", "Faraid ialah hukum pembahagian harta pusaka orang Islam kepada waris mengikut kadar yang ditetapkan Al-Quran (An-Nisa' 4:11, 12 dan 176) dan sunnah. Di Malaysia, pembahagian mengikut mazhab Syafi'i dan disahkan melalui Sijil Faraid daripada Mahkamah Syariah."),
        ("Apa yang perlu diselesaikan sebelum harta difaraidkan?", "Mengikut turutan: kos pengurusan jenazah, hutang si mati (termasuk zakat dan nazar yang belum dibayar), wasiat kepada bukan waris (maksimum 1/3 baki harta), kemudian baru baki dibahagikan secara faraid. Tuntutan harta sepencarian oleh pasangan juga diselesaikan dahulu."),
        ("Kenapa anak lelaki mendapat dua kali bahagian anak perempuan?", "Allah berfirman: “bahagian seorang anak lelaki menyamai bahagian dua orang anak perempuan” (An-Nisa' 4:11). Anak lelaki memikul kewajipan nafkah ke atas isteri, anak dan keluarga, manakala harta anak perempuan kekal miliknya sendiri."),
        ("Bila harta pusaka diserahkan kepada Baitulmal?", "Apabila tiada waris langsung, atau terdapat baki selepas bahagian fardu dan tiada waris asabah. Mengikut amalan mazhab Syafi'i di kebanyakan negeri, baki itu diserahkan kepada Baitulmal; sebahagian negeri (contohnya Perlis) boleh memutuskan radd, iaitu dikembalikan kepada waris fardu selain suami/isteri. Kalkulator ini menyediakan kedua-dua pilihan."),
        ("Adakah anak angkat atau waris bukan Islam mendapat faraid?", "Tidak. Anak angkat dan waris bukan Islam tidak mewarisi secara faraid. Mereka boleh diberi melalui hibah semasa hidup atau wasiat (maksimum 1/3 harta)."),
        ("Di mana hendak membuat permohonan pembahagian pusaka?", "Harta pusaka kecil (bernilai sehingga RM5 juta, tanpa wasiat) dipohon di Pejabat Pusaka Kecil (JKPTG); Sijil Faraid dikeluarkan oleh Mahkamah Syariah. Harta alih sahaja boleh diuruskan melalui Amanah Raya Berhad, dan kes yang lebih besar di Mahkamah Tinggi."),
        ("Siapakah yang terhalang (mahjub) daripada menerima pusaka?", "Waris yang lebih dekat menghalang waris yang lebih jauh: contohnya anak lelaki menghalang cucu dan adik-beradik, bapa menghalang datuk dan adik-beradik, dan ibu menghalang nenek. Kalkulator di atas menyenaraikan setiap waris yang terhalang beserta sebabnya."),
    ]
    k11, k12, k176 = quran_block([(4, 11)]), quran_block([(4, 12)]), quran_block([(4, 176)])
    frows = [["Suami", "1/2 (tiada anak/cucu) · 1/4 (ada anak/cucu)"], ["Isteri", "1/4 (tiada anak/cucu) · 1/8 (ada anak/cucu), dikongsi jika lebih seorang"],
             ["Ibu", "1/3 · 1/6 (ada anak/cucu atau 2+ adik-beradik)"], ["Bapa", "1/6 (ada anak lelaki) · 1/6 + baki (ada anak perempuan sahaja) · baki (tiada anak)"],
             ["Anak perempuan", "1/2 (seorang) · 2/3 (dua atau lebih) · baki bersama anak lelaki (2:1)"], ["Anak lelaki", "Asabah: semua baki selepas waris fardu"],
             ["Nenek", "1/6 (dikongsi jika dua)"], ["Saudara seibu", "1/6 (seorang) · 1/3 (dua atau lebih, sama rata)"]]
    body = hero("Kalkulator Faraid: Pembahagian Harta Pusaka Islam",
                "Kira bahagian setiap waris mengikut hukum faraid mazhab Syafi'i: fardu, asabah, 'aul, waris terhalang, dan baki kepada Baitulmal.",
                [("Faraid", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section id="kira" class="tool" aria-labelledby="h-kira">
<h2 id="h-kira">⚖️ Kalkulator Faraid</h2>
{form}
<p class="note">Data disimpan dalam peranti ini sahaja. Keputusan ini panduan pendidikan; pembahagian rasmi melalui Mahkamah Syariah atau Pejabat Pusaka Kecil.</p>
<div class="act" id="fract"><button class="btn2" type="button" data-act="copy">📋 Salin keputusan</button><button class="btn2" type="button" data-act="reset">↺ Set semula</button></div>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Selepas kos jenazah, hutang dan wasiat (maksimum 1/3), harta pusaka dibahagi mengikut faraid: suami/isteri, ibu, bapa dan anak perempuan mendapat <strong>bahagian tetap (fardu)</strong>, manakala <strong>anak lelaki mengambil baki (asabah)</strong> bersama anak perempuan dengan nisbah 2:1. Contoh: si mati meninggalkan isteri, ibu, bapa, 2 anak lelaki dan seorang anak perempuan dengan harta RM300,000: isteri RM37,500 (1/8), ibu dan bapa RM50,000 setiap seorang (1/6), setiap anak lelaki RM65,000 dan anak perempuan RM32,500.</p></div>
{meta_line(T_, TMS)}
{share(SITE + path, "Kalkulator faraid: kira bahagian setiap waris mengikut hukum Islam:")}
</div>
</section>

<section id="bahagian" aria-labelledby="h-bahagian">
<h2 id="h-bahagian">Jadual Bahagian Faraid Utama</h2>
{table(["Waris", "Bahagian"], frows, "Bahagian faraid utama")}
<p class="note">Bahagian yang melebihi harta dikurangkan secara berkadar ('aul); baki tanpa waris asabah diserahkan kepada Baitulmal (mazhab Syafi'i) atau dikembalikan (radd) jika diputuskan sedemikian.</p>
</section>
{ad(0)}
<section class="dsec" id="dalil" aria-labelledby="h-dalil">
<h2 id="h-dalil">Dalil Faraid</h2>
{card("ayat-4-11", "An-Nisa' 11: bahagian anak dan ibu bapa", k11[0], k11[1], k11[2], qref(4, 11))}
{card("ayat-4-12", "An-Nisa' 12: bahagian suami, isteri dan saudara seibu", k12[0], k12[1], k12[2], qref(4, 12))}
{card("ayat-4-176", "An-Nisa' 176: kalalah, saudara seibu sebapa dan sebapa", k176[0], k176[1], k176[2], qref(4, 176))}
<ul class="src"><li>“Berikanlah bahagian faraid kepada yang berhak; bakinya untuk waris lelaki yang paling hampir” (HR Al-Bukhari, no. 6732; Muslim, no. 1615).</li></ul>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Faraid</h2>
{faq_html(faq)}
<p class="note">Lihat juga <a href="/tahlil-ringkas/">tahlil ringkas</a>, <a href="/solat-sunat/solat-jenazah/">solat jenazah</a> dan <a href="/zakat-emas/">zakat emas</a>.</p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(path)}</section>
</div>
{side([("kira", "Kalkulator faraid"), ("bahagian", "Jadual bahagian"), ("dalil", "Dalil"), ("faq", "Soalan lazim")], path)}
</div>'''
    fd = json.dumps({"h": [[k, l, m] for k, l, m, _ in FR.HEIRS], "sh": FR.SHORT, "ch": FR.CHAIN, "nt": FR.NOTES}, ensure_ascii=False, separators=(",", ":"))
    return dict(path=path, kind="tool", data=False, arabic=True, extra_data=f'<script type="application/json" id="frdat">{fd}</script>',
                title="Kalkulator Faraid: Pembahagian Harta Pusaka Islam", ogtitle="Kalkulator Faraid",
                desc="Kira faraid harta pusaka: bahagian suami, isteri, ibu bapa, anak & adik-beradik ikut mazhab Syafi'i, termasuk 'aul, waris terhalang dan Baitulmal.",
                crumbs=[("Faraid", None)], body=body, faq=faq, about=["Faraid", "Harta pusaka", "Hukum waris Islam"],
                app=dict(name="Kalkulator Faraid", features=["23 jenis waris", "Fardu, asabah dan 'aul", "Waris terhalang beserta sebab", "Hutang, kos jenazah dan had wasiat 1/3", "Baitulmal atau radd"]),
                llms="Kalkulator faraid (mazhab Syafi'i): suami 1/2 atau 1/4, isteri 1/4 atau 1/8, ibu 1/3 atau 1/6, bapa 1/6 dan/atau asabah, anak perempuan 1/2 atau 2/3, anak lelaki asabah (2:1). Contoh RM300,000: isteri RM37,500, ibu RM50,000, bapa RM50,000, 2 anak lelaki RM65,000 seorang, anak perempuan RM32,500.")
