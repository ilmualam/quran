"""Pages: /juz-1/ … /juz-30/, one static page per juz with every ayah from data-surah/ (Arabic, Rumi, Malay translation),
grouped by surah, with the juz boundaries, Mushaf Madinah pages, sajdah ayat and links to the surah pages
(tools/pages15.py) and the reader for audio. Answers "juz N rumi" / "juz amma"; the list of all 30 stays on
/senarai-juzuk-al-quran/, which links here."""
import plans as P
import rumi_ms as RM
from surahs import S, MADANI
from pages import e, faq_html, hero, side, meta_line, table, tool_cards, SITE
from pages15 import load, BASMALAH, PATH as SPATH

PUB = "2026-11-11"
NICK = {30: "Juz 'Amma", 29: "Juz Tabarak"}  # only the names in universal use; others are just numbered


def path(j):
    return f"juz-{j}/"


def info(j):
    g1, g2 = P.JS[j - 1], P.JS[j] - 1
    (s1, a1), (s2, a2) = P.sa(g1), P.sa(g2)
    segs = P.juz_segments(j)
    sajdah = [(s, a) for s, a in P.META["sajda"] if g1 <= P.gid(s, a) <= g2]
    return dict(s1=s1, a1=a1, s2=s2, a2=a2, n=g2 - g1 + 1, p1=P.page_of(g1), p2=P.page_of(g2), segs=segs, sajdah=sajdah)


def ayat_html(segs, sajdah):
    out = []
    for s, a1, a2 in segs:
        data = load(s)
        whole = a1 == 1 and a2 == len(data)
        rng = "" if whole else f" (ayat {a1}–{a2})"
        out.append(f'<h3 class="jzs" id="surah-{s}">Surah {e(S[s][1])}{rng} <span lang="ar" dir="rtl" class="nar">{e(S[s][0])}</span></h3>'
                   f'<p class="note"><a href="/{SPATH[s]}">Baca Surah {e(S[s][1])} penuh</a> · surah ke-{s}, {"Madaniyyah" if s in MADANI else "Makkiyyah"}, {len(data)} ayat</p>')
        if a1 == 1 and s not in (1, 9):
            out.append(f'<p class="dar sbas" lang="ar" dir="rtl">{e(BASMALAH["arabic"])}</p>')
        for v in data[a1 - 1:a2]:
            a = v["id"]
            sj = " · ۩ ayat sajdah" if (s, a) in sajdah else ""
            out.append(f'<article class="dw sv" id="s{s}-a{a}"><header class="dh"><h4>{e(S[s][1])} {s}:{a}{sj}</h4>'
                       f'<a class="note" href="/#surah-{s}-ayat-{a}" aria-label="Dengar {s}:{a} dalam pembaca">▶ Dengar</a></header>'
                       f'<p class="dar" lang="ar" dir="rtl">{e(v["arabic"])} <span class="an">﴿{a}﴾</span></p>'
                       f'<p class="dru"><em>{e(RM.rumi(s, a, v["rumi"]))}</em></p><p class="dmn">{e(v["translation"])}</p></article>')
    return "".join(out)


def build_pages19(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    pages = []
    for j in range(1, 31):
        f = info(j)
        nm = f"Juz {j}" + (f" ({NICK[j]})" if j in NICK else "")
        url = SITE + path(j)
        start, end = f"{P.NAMES[f['s1'] - 1]} {f['s1']}:{f['a1']}", f"{P.NAMES[f['s2'] - 1]} {f['s2']}:{f['a2']}"
        nsur = len(f["segs"])
        sur_list = ", ".join(f"{S[s][1]}" + ("" if a1 == 1 and a2 == len(load(s)) else f" ({a1}–{a2})") for s, a1, a2 in f["segs"])
        first = load(f["s1"])[f["a1"] - 1]
        open_words = " ".join(first["arabic"].split()[:3])
        rows = [["Bermula", f'<a href="#s{f["s1"]}-a{f["a1"]}">{e(start)}</a>'], ["Berakhir", e(end)],
                ["Kalimah pembuka", f'<span lang="ar" dir="rtl" class="nar">{e(open_words)}</span>'],
                ["Bilangan ayat", P.num(f["n"])], ["Surah", f"{nsur} surah: " + ", ".join(f'<a href="#surah-{s}">{e(S[s][1])}</a>' for s, _, _ in f["segs"])],
                ["Muka surat (Mushaf Madinah)", f"{f['p1']}–{f['p2']} ({f['p2'] - f['p1'] + 1} muka surat)"]]
        if f["sajdah"]:
            rows.append(["Ayat sajdah", ", ".join(f'<a href="#s{s}-a{a}">{e(P.NAMES[s - 1])} {s}:{a}</a>' for s, a in f["sajdah"])])
        nick_txt = (" Ia dikenali sebagai Juz 'Amma sempena kalimah pertamanya, “'Amma yatasa'alun” (An-Naba' 78:1)." if j == 30 else
                    " Ia dikenali sebagai Juz Tabarak sempena kalimah pertama Surah Al-Mulk, “Tabarakallazi”." if j == 29 else "")
        box = (f"{e(nm)} bermula pada <strong>{e(start)}</strong> dan berakhir pada <strong>{e(end)}</strong>, mengandungi <strong>{P.num(f['n'])} ayat</strong> "
               f"daripada {nsur} surah, pada muka surat {f['p1']}–{f['p2']} Mushaf Madinah.{e(nick_txt)}")
        faq = [(f"{nm} bermula dengan surah apa?", f"{nm} bermula dengan {start} dan berakhir dengan {end}."),
               (f"Berapa ayat dalam {nm}?", f"{nm} mengandungi {P.num(f['n'])} ayat daripada {nsur} surah: {sur_list}."),
               (f"{nm} muka surat berapa?", f"Muka surat {f['p1']} hingga {f['p2']} dalam Mushaf Madinah 604 muka surat ({f['p2'] - f['p1'] + 1} muka surat)."),
               (f"Berapa lama membaca {nm}?", "Kira-kira 30 hingga 45 minit dengan bacaan sederhana. Membaca satu juz sehari menghabiskan Al-Quran dalam 30 hari; "
                                              "gunakan Jadual Khatam untuk merancang bacaan.")]
        if f["sajdah"]:
            faq.append((f"Adakah ayat sajdah dalam {nm}?", "Ya: " + ", ".join(f"{P.NAMES[s - 1]} {s}:{a}" for s, a in f["sajdah"]) + ". Sujud tilawah disunatkan apabila membaca atau mendengarnya."))
        prev_next = " · ".join(([f'<a href="/{path(j - 1)}">← Juz {j - 1}</a>'] if j > 1 else []) + ([f'<a href="/{path(j + 1)}">Juz {j + 1} →</a>'] if j < 30 else []))
        allj = "".join(f'<li><a href="/{path(k)}"{" aria-current=page" if k == j else ""}><b>{k}</b></a></li>' for k in range(1, 31))
        body = hero(f"{e(nm)}: Bacaan Penuh Arab, Rumi & Terjemahan",
                    f"Baca {e(nm)} penuh {P.num(f['n'])} ayat ({e(start)} hingga {e(end)}) dalam tulisan Arab, Rumi dan terjemahan Bahasa Melayu, dengan audio ayat demi ayat.",
                    [("Senarai Juzuk", "senarai-juzuk-al-quran/"), (nm, None)],
                    f'<p><a class="btn3" href="/#surah-{f["s1"]}-ayat-{f["a1"]}">🎧 Baca & dengar dalam pembaca</a></p>')
        body += f'''<div class="wrap mn"><div class="ct">
<section aria-labelledby="h-jwp"><div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {box}</p></div>
{meta_line(T, TMS)}
{share(url, f"Baca {nm} penuh: Arab, Rumi & terjemahan:")}
</div></section>
<section id="fakta" aria-labelledby="h-fakta">
<h2 id="h-fakta">Fakta {e(nm)}</h2>
{table(["Perkara", "Keterangan"], rows, f"Fakta {nm}")}
<p class="note">{prev_next} · <a href="/senarai-juzuk-al-quran/">Senarai 30 juzuk</a> · <a href="/jadual-khatam-al-quran/">Jadual khatam</a></p>
</section>
<section class="dsec" id="bacaan" aria-labelledby="h-bacaan">
<h2 id="h-bacaan">Bacaan {e(nm)} Penuh ({P.num(f["n"])} Ayat)</h2>
<p class="note">Teks Arab Uthmani dan terjemahan Abdullah Muhammad Basmeih daripada dataset laman ini, tanpa suntingan. Rumi hanya alat bantu bacaan; belajar tajwid dengan guru. Tekan “▶ Dengar” untuk audio.</p>
{ayat_html(f["segs"], f["sajdah"])}
</section>
{ad(0)}
<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: {e(nm)}</h2>
{faq_html(faq)}
</section>
<section id="juz-lain" aria-labelledby="h-jl">
<h2 id="h-jl">Juz Lain</h2>
<ul class="nbaz nbaz2 jzn">{allj}</ul>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(None)}</section>
</div>
{side([("fakta", "Fakta"), ("bacaan", "Bacaan penuh"), ("faq", "Soalan lazim"), ("juz-lain", "Juz lain")], None)}
</div>'''
        title = f"{nm} Penuh: Arab, Rumi & Terjemahan ({P.num(f['n'])} Ayat)"
        if len(title) > 70:
            title = f"{nm}: Arab, Rumi & Terjemahan"
        desc = f"Baca {nm} penuh: {start} hingga {end}, {P.num(f['n'])} ayat dalam tulisan Arab, Rumi dan terjemahan Melayu, dengan audio dan muka surat Mushaf."
        if len(desc) > 160:
            desc = f"Baca {nm} penuh ({start} – {end}), {P.num(f['n'])} ayat: Arab, Rumi, terjemahan Melayu dan audio."
        pages.append(dict(path=path(j), kind="ref", data=False, arabic=True, published=PUB, nocache=True,
                          title=title, ogtitle=f"{nm}: Bacaan Penuh Arab, Rumi & Terjemahan", desc=desc,
                          crumbs=[("Senarai Juzuk", "senarai-juzuk-al-quran/"), (nm, None)], body=body, faq=faq,
                          about=[nm, "Al-Quran", "Bacaan Rumi"], ogcard=(f"{nm} ({P.num(f['n'])} ayat)", "Bacaan penuh: Arab, Rumi, terjemahan Melayu & audio"),
                          llms=f"{nm}: {start} hingga {end}, {f['n']} ayat, {nsur} surah, muka surat {f['p1']}–{f['p2']}. Teks penuh Arab, Rumi dan terjemahan Melayu."))
    return pages
