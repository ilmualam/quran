"""Page: /nama-bayi-islam/ (merged from name.ilmualam.com). Four tools on one page, run by assets/js/nama.js over
assets/data/nama-bayi.json (tools/nama.py): full-name generator, search & filter, name checker (hadith-based warnings),
shortlist with a share link. Everything a crawler or a visitor without JavaScript needs is rendered here: 12 sample full
names, the first 30 names of the list, editor's picks, Quran-verified names, the 25 prophets, Abdul + Asmaul Husna,
names to avoid with their dalil, A-Z counts, method and FAQ."""
import json, random, re
from collections import Counter, defaultdict
import nama as NM
import nama_data as ND
import plans as P
from pages import e, faq_html, hero, side, meta_line, tool_cards, table, SITE
from pages2 import qref, quran_block, card

PATH = "nama-bayi-islam/"
PUB = "2026-11-10"
PER = 30
# (column index of the row lists) name, arabic, meaning, gender, source, syllables, themes, flags, ref, count, kisah
GL = {"L": "Lelaki", "P": "Perempuan", "U": "Uniseks"}
SRC = {"n": "Nabi & keluarga", "s": "Sahabat & tokoh", "u": "Umum"}
PICK_L = ["Muhammad", "Ahmad", "Adam", "Aisy", "Rayyan", "Umar", "Ali", "Hamzah", "Yusuf", "Ibrahim", "Khalid", "Bilal", "Zaid", "Anas", "Muaz",
          "Uwais", "Aiman", "Haikal", "Harith", "Hakimi", "Haziq", "Irfan", "Luqman", "Mikail", "Naufal", "Fateh", "Ammar", "Zayyan", "Ziyad",
          "Arsyad", "Syahmi", "Faris", "Danial", "Iman", "Firdaus", "Hadi", "Nabil", "Qasim", "Rasyid", "Taufiq"]
PICK_P = ["Aisyah", "Fatimah", "Maryam", "Khadijah", "Humaira", "Hana", "Zahra", "Safiyyah", "Sofiyyah", "Hafsah", "Zainab", "Ruqayyah",
          "Sumayyah", "Nusaibah", "Khaulah", "Hawa", "Sarah", "Raihanah", "Aina", "Alya", "Amani", "Dhiya", "Insyirah", "Iffah",
          "Jannah", "Mardhiah", "Madinah", "Nadhirah", "Nuha", "Najwa", "Salsabila", "Sakinah", "Tasnim", "Wardah", "Yasmin", "Yusra", "Zulaikha",
          "Husna", "Mawaddah", "Rahmah"]
PREFIX = {"L": [("m2", "Muhammad + 2 nama", "Muhammad"), ("a2", "Ahmad + 2 nama", "Ahmad"), ("m1", "Muhammad + 1 nama", "Muhammad"),
                ("x2", "2 nama (tanpa awalan)", ""), ("x1", "1 nama sahaja", ""), ("ab", "Abdul + Asmaul Husna", "")],
          "P": [("n2", "Nur + 2 nama", "Nur"), ("n1", "Nur + 1 nama", "Nur"), ("nl1", "Nurul + 1 nama", "Nurul"), ("s1", "Siti + 1 nama", "Siti"),
                ("x2", "2 nama (tanpa awalan)", ""), ("x1", "1 nama sahaja", "")]}

_HAR = re.compile("[ً-ٰٟ]")


def akey(a):
    return _HAR.sub("", a).replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace(" ", "")


def refa(r):
    if r[10]:
        return f'<a href="/kisah-nabi/{r[10]}/">📜 Kisah Nabi</a>'
    if not r[8]:
        return ""
    s, a = map(int, r[8].split(":"))
    return f'<a href="/#surah-{s}-ayat-{a}" title="Perkataan ini terdapat dalam Al-Quran">📖 {e(P.NAMES[s - 1])} {s}:{a}{f" · {r[9]}×" if r[9] > 1 else ""}</a>'


def name_card(r, variants):
    """Same markup as card() in assets/js/nama.js."""
    th = "".join(f"<span>{ND_THEME(t)}</span>" for t in r[6][:2])
    v = [x for x in variants.get((akey(r[1]), r[3]), []) if x != r[0]][:4]
    vline = f'<p class="nbv">Ejaan lain: {e(", ".join(v))}</p>' if v else ""
    aw = '<span class="nbaw">Awalan</span>' if r[7] == "a" else ""
    return (f'<li class="nbc"><button class="nbs" type="button" data-save="{e(r[0])}" aria-pressed="false" aria-label="Simpan {e(r[0])}">♡</button>'
            f'<p class="nbn">{e(r[0])}</p><p class="nba" lang="ar" dir="rtl">{e(r[1])}</p><p class="nbm">{e(r[2])}</p>{vline}'
            f'<p class="nbt"><span class="g{r[3]}">{GL[r[3]]}</span>{aw}<span>{SRC[r[4]]}</span><span>{r[5]} suku kata</span>{th}{refa(r)}</p></li>')


def ND_THEME(t):
    return NM.THEMES[t]


def variants_of(rows):
    v = defaultdict(list)
    for r in rows:
        if r[7] != "a":
            v[(akey(r[1]), r[3])].append(r[0])
    return v


def listable(rows):
    return [r for r in rows if r[7] != "a"]


def combos(rows):
    """How many distinct full names the generator can make with no filters (the number quoted on the page)."""
    L = [r for r in listable(rows) if r[3] in "LU" and r[7] != "b"]
    Pp = [r for r in listable(rows) if r[3] in "PU"]
    nl, np_ = len(L), len(Pp)
    nab = sum(1 for r in rows if r[7] == "b")
    return 2 * nl * (nl - 1) + nl * (nl - 1) + 2 * nl + nab + np_ * (np_ - 1) * 2 + np_ * 4


def sample_full(rows, n=12, seed=2026):
    """Build-time sample for the generator box (Muhammad + 2 names); nama.js replaces it on the first "Jana"."""
    rnd = random.Random(seed)
    pool = [r for r in listable(rows) if r[3] == "L" and r[7] == "e" and r[0] not in ("Muhammad", "Ahmad") and 2 <= r[5] <= 3 and " " not in r[0]]
    m = next(r for r in rows if r[0] == "Muhammad" and r[3] == "L")
    out, seen = [], set()
    while len(out) < n:
        a, b = rnd.sample(pool, 2)
        if akey(a[1]) == akey(b[1]) or (a[0], b[0]) in seen:
            continue
        seen.add((a[0], b[0]))
        out.append([m, a, b])
    return out


def full_card(parts):
    """Same markup as fullCard() in assets/js/nama.js."""
    nm = " ".join(p[0] for p in parts)
    ar = " ".join(p[1] for p in parts)
    mn = " · ".join(f"<b>{e(p[0])}</b>: {e(p[2])}" for p in parts)
    return (f'<li class="nbf"><button class="nbs" type="button" data-save="{e(nm)}" aria-pressed="false" aria-label="Simpan {e(nm)}">♡</button>'
            f'<p class="nbff">{e(nm)}</p><p class="nba" lang="ar" dir="rtl">{e(ar)}</p><p class="nbm">{mn}</p></li>')


def opts(pairs, sel=""):
    return "".join(f'<option value="{e(v)}"{" selected" if v == sel else ""}>{e(t)}</option>' for v, t in pairs)


MIN_SUB = 15  # a letter page needs at least this many names, so no thin pages
GW = {"L": "lelaki", "P": "perempuan"}


def sub_path(g, x):
    return f"{PATH}{GW[g]}-huruf-{x.lower()}/"


def letter_sets(lst):
    """(letter, gender) -> names for that page: the gender's names plus uniseks, editor's names first, then A-Z."""
    d = defaultdict(list)
    for r in lst:
        for g in ("L", "P"):
            if r[3] in (g, "U") and r[7] != "b":
                d[(r[0][0].upper(), g)].append(r)
    return {k: sorted(v, key=lambda r: (r[7] != "e", r[0].lower())) for k, v in d.items() if len(v) >= MIN_SUB}


def sub_page(g, x, names, LET, by, T_, TMS, share, ad):
    w, W = GW[g], GW[g].capitalize()
    path, n = sub_path(g, x), len(names)
    ed = [r for r in names if r[7] == "e"]
    top = (ed or names)[:8]
    qn = [r for r in names if r[8] and not r[10]][:12]
    sn = [r for r in names if r[4] in "ns"][:12]
    rows_ = [[(f'<strong><a href="/{MP[r[0].lower()]}">{e(r[0])}</a></strong>' if r[0].lower() in MP else f"<strong>{e(r[0])}</strong>") + (' ⭐' if r[7] == 'e' else ''), f'<span lang="ar" dir="rtl" class="nbta">{e(r[1])}</span>', e(r[2]),
              refa(r) or "–"] for r in names]
    other = {"L": "P", "P": "L"}[g]
    nav = "".join(f'<li><a href="/{sub_path(g, y)}"{" aria-current=page" if y == x else ""}><b>{y}</b><small>{len(LET[(y, g)])}</small></a></li>'
                  for y in sorted({k[0] for k in LET if k[1] == g}))
    jl = f"/{PATH}#j={g}&c={'m2' if g == 'L' else 'n2'}&h={x}&w=1"
    lst_txt = ", ".join(f"{r[0]} ({r[2].split(';')[0].split(' (')[0].rstrip('.')})" for r in top[:5])
    faq = [(f"Apakah nama bayi {w} Islam bermula dengan huruf {x}?",
            f"Antara pilihan editor: {lst_txt}. Halaman ini menyenaraikan {n} nama bayi {w} Islam bermula dengan huruf {x}, setiap satu dengan tulisan Arab dan maksud."),
           (f"Berapa banyak nama bayi {w} huruf {x} dalam senarai ini?",
            f"{n} nama ({len(ed)} pilihan editor yang disemak), termasuk nama uniseks. {len([r for r in names if r[8]])} daripadanya ialah perkataan yang terdapat dalam Al-Quran, dengan rujukan ayat.")]
    if qn:
        faq.append((f"Nama {w} huruf {x} yang terdapat dalam Al-Quran?",
                    "Perkataan nama berikut dijumpai dalam teks Al-Quran: " + ", ".join(f"{r[0]} ({P.NAMES[int(r[8].split(':')[0]) - 1]} {r[8]})" for r in qn[:8]) + ". Maksud perkataan dalam ayat mungkin berbeza daripada maksud nama."))
    if sn:
        faq.append((f"Nama nabi atau sahabat huruf {x} untuk anak {w}?", ", ".join(f"{r[0]}: {r[2]}" for r in sn[:6]) + "."))
    h1 = f"Nama Bayi {W} Islam Huruf {x}: {n} Nama & Maksud"
    body = hero(h1, f"{n} nama bayi {w} Islam bermula dengan huruf {x}, dengan tulisan Arab, maksud dan rujukan ayat Al-Quran jika perkataannya terdapat dalam Al-Quran.",
                [("Nama Bayi Islam", PATH), (f"{W} huruf {x}", None)])
    body += f'''<div class="wrap mn"><div class="ct">
<section aria-labelledby="h-jwp"><div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Nama bayi {w} Islam huruf {x} pilihan editor: {e(lst_txt)}. Senarai penuh {n} nama di bawah; nama bertanda ⭐ telah disemak editor.</p></div>
{meta_line(T_, TMS)}
<div class="act"><a class="btn3" href="{jl}">✨ Jana nama penuh {w} huruf {x}</a><a class="btn2" href="/{sub_path(other, x)}">Nama {GW[other]} huruf {x}</a></div>
{share(SITE + path, f"Nama bayi {w} Islam huruf {x} dengan maksud dan tulisan Arab:")}
</div></section>
<section id="senarai" aria-labelledby="h-senarai">
<h2 id="h-senarai">Senarai {n} Nama Bayi {W} Huruf {x}</h2>
{table(["Nama", "Arab", "Maksud", "Rujukan"], rows_, f"Nama bayi {w} huruf {x}")}
<p class="note">⭐ pilihan editor. 📖 = perkataan terdapat dalam Al-Quran (ayat pertama dan bilangan kali). Semak nama penuh dengan <a href="/{PATH}#semak">Semak Nama</a>.</p>
</section>
{ad(0)}
<section id="huruf" aria-labelledby="h-huruf">
<h2 id="h-huruf">Nama Bayi {W} Ikut Huruf</h2>
<ul class="nbaz nbaz2">{nav}</ul>
</section>
<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim</h2>
{faq_html(faq)}
<p class="note">Kembali ke <a href="/{PATH}">penjana nama bayi Islam</a> untuk penjana nama penuh, carian maksud dan senarai pendek.</p>
</section>
</div>
{side([("senarai", "Senarai nama"), ("huruf", "Huruf lain"), ("faq", "Soalan lazim")], PATH)}
</div>'''
    items = [{"@type": "ListItem", "position": i, "name": r[0], "description": r[2]} for i, r in enumerate(names, 1)]
    return dict(path=path, kind="ref", data=False, arabic=True, published=PUB, nocache=True, schema="CollectionPage", og=f"nama-bayi-{w}",
                ogcard=(f"Nama Bayi {W} Islam", "Nama ikut huruf A–Z dengan maksud & tulisan Arab"),
                title=f"Nama Bayi {W} Islam Huruf {x} ({n} Nama & Maksud)", ogtitle=f"Nama Bayi {W} Islam Huruf {x}",
                desc=f"{n} nama bayi {w} Islam huruf {x} dengan maksud dan tulisan Arab. Pilihan editor: {', '.join(r[0] for r in top[:4])}. Jana nama penuh dan semak maksud."[:160],
                crumbs=[("Nama Bayi Islam", PATH), (f"{W} huruf {x}", None)], body=body, faq=faq,
                about=[f"Nama bayi {w} Islam", f"Nama bayi {w} huruf {x}", "Maksud nama"],
                itemlist=dict(name=f"Nama bayi {w} Islam huruf {x}", items=items),
                llms=f"{n} nama bayi {w} Islam huruf {x} dengan tulisan Arab dan maksud; pilihan editor: {', '.join(r[0] for r in top[:6])}.")


MP = {}  # name (lower case) -> path of its meaning page, filled by build_pages17 before any page links to it
MPUB = "2026-11-11"


def slug(n):
    return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")


def m_path(n):
    return f"{PATH}maksud-nama-{slug(n)}/"


def maksud_page(name, rs, ed, var, T_, TMS, share, ad):
    """One page per editor-reviewed name: meaning, Arabic, the Quran ayah where the word occurs, spelling variants,
    pairings and names with a similar meaning. rs = the editor rows with this spelling (one per gender)."""
    r = rs[0]
    gs = [GW.get(x[3], "uniseks") if x[3] != "U" else "uniseks" for x in rs]
    gtxt = " dan ".join(dict.fromkeys(gs))
    path = m_path(name)
    rnd = random.Random(slug(name))
    g = r[3]
    same = [x for x in ed if (x[3] == g or g == "U" or x[3] == "U") and x[0] != name and x[7] == "e" and " " not in x[0]]
    th = r[6][:1]
    sim = [x for x in same if th and th in x[6]]
    sim = rnd.sample(sim, min(8, len(sim))) if sim else []
    pool = [x for x in same if x[0][0] != name[0] and akey(x[1]) != akey(r[1])]
    pairs = rnd.sample(pool, min(6, len(pool))) if r[7] != "b" else []
    v = [x for x in var.get((akey(r[1]), r[3]), []) if x != name][:8]
    link = lambda x: f'<a href="/{MP[x[0].lower()]}">{e(x[0])}</a>' if x[0].lower() in MP else e(x[0])
    secs = []
    if r[10]:
        secs.append(("quran", f"Nama {e(name)} dalam Al-Quran",
                     f'<p>{e(name)} ialah nama seorang nabi yang disebut dalam Al-Quran. Baca kisah, mukjizat dan setiap ayat yang menyebut namanya di <a href="/kisah-nabi/{r[10]}/">Kisah Nabi {e(name)}</a>.</p>'))
    elif r[8]:
        s_, a_ = map(int, r[8].split(":"))
        ar, ru, mn = quran_block([(s_, a_)])
        secs.append(("quran", f"Perkataan {e(name)} dalam Al-Quran",
                     f'<p>Perkataan Arab <span lang="ar" dir="rtl" class="nbta">{e(r[1])}</span> terdapat dalam Al-Quran sebanyak <strong>{r[9]} kali</strong>. Ayat pertama yang mengandunginya:</p>'
                     + card(f"ayat-{s_}-{a_}", f"{P.NAMES[s_ - 1]} {s_}:{a_}", ar, ru, mn, qref(s_, a_))
                     + '<p class="note">Maksud perkataan dalam ayat mungkin berbeza sedikit daripada maksud nama, bergantung pada konteks ayat.</p>'))
    if r[7] == "b":
        secs.append(("asmaul", "Abdul dan Asmaul Husna", f'<p>Abdul bermaksud “hamba kepada”. {e(name)} menyambungkan Abdul dengan salah satu <a href="/asmaul-husna/">99 nama Allah</a>, '
                     'jadi maksudnya ialah pengakuan sebagai hamba Allah. “Nama yang paling disukai Allah ialah Abdullah dan Abdul Rahman” (HR Muslim 2132).</p>'))
    if pairs:
        pre = "Muhammad " if g == "L" else ("Nur " if g == "P" else "")
        secs.append(("gabung", f"Cadangan Nama Penuh dengan {e(name)}", '<ul class="nbpair">' + "".join(
                     f"<li><strong>{e(pre)}{e(name)} {link(x)}</strong><span>{e(name)}: {e(r[2].split(';')[0])} · {e(x[0])}: {e(x[2].split(';')[0])}</span></li>" for x in pairs) + "</ul>"
                     + f'<p><a class="btn3" href="/{PATH}#j={"P" if g == "P" else "L"}&c={"n2" if g == "P" else "m2"}&h={name[0].upper()}&w=1">✨ Jana lagi nama penuh huruf {e(name[0].upper())}</a></p>'))
    if sim:
        secs.append(("serupa", "Nama Lain dengan Maksud Serupa", "<ul class=\"nbsim\">" + "".join(f"<li>{link(x)}: {e(x[2].split(';')[0])}</li>" for x in sim) + "</ul>"))
    toc = [("maksud", "Maksud")] + [(i, re.sub("<[^>]+>", "", h)) for i, h, _ in secs] + [("faq", "Soalan lazim")]
    faq = [(f"Apakah maksud nama {name}?", f"{name} ({r[1]}) bermaksud: {r[2]}"),
           (f"Adakah nama {name} terdapat dalam Al-Quran?",
            (f"Ya. {name} ialah nama nabi yang disebut dalam Al-Quran." if r[10] else
             f"Ya. Perkataan Arab {r[1]} terdapat {r[9]} kali dalam Al-Quran, pertama kali dalam {P.NAMES[int(r[8].split(':')[0]) - 1]} {r[8]}." if r[8] else
             f"Perkataan {name} tidak dijumpai sebagai perkataan tunggal dalam teks Al-Quran. Ia tetap nama Islam yang baik maksudnya.")),
           (f"Nama {name} untuk lelaki atau perempuan?", f"{name} ialah nama {gtxt}." + (f" Ejaan lain: {', '.join(v)}." if v else "")),
           (f"Bagaimana menulis nama {name} dalam tulisan Arab?", f"{r[1]}, {r[5]} suku kata.")]
    h1 = f"Maksud Nama {e(name)} dalam Islam"
    body = hero(h1, f"Maksud nama {e(name)}, tulisan Arab, rujukan Al-Quran, ejaan lain dan cadangan nama penuh.",
                [("Nama Bayi Islam", PATH), (f"Maksud nama {name}", None)])
    th_txt = ", ".join(NM.THEMES[t] for t in r[6]) or "–"
    srcl = {"n": "Nabi & keluarga Nabi", "s": "Sahabat & tokoh Islam", "u": "Nama Islam umum"}[r[4]]
    frows = [["Nama", f"<strong>{e(name)}</strong>"], ["Tulisan Arab", f'<span lang="ar" dir="rtl" class="nbta">{e(r[1])}</span>'],
             ["Maksud", e(r[2])], ["Jantina", gtxt.capitalize()], ["Suku kata", str(r[5])], ["Kategori", srcl], ["Tema", th_txt],
             ["Al-Quran", refa(r) or "Tiada sebagai perkataan tunggal"]] + ([["Ejaan lain", e(", ".join(v))]] if v else [])
    facts = '<dl class="nbdl">' + "".join(f"<dt>{k}</dt><dd>{val}</dd>" for k, val in frows) + "</dl>"
    body += f'''<div class="wrap mn"><div class="ct">
<section id="maksud" aria-labelledby="h-maksud"><div class="prose">
<h2 id="h-maksud" class="sr">Maksud</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Nama <strong>{e(name)}</strong> (<span lang="ar" dir="rtl">{e(r[1])}</span>) bermaksud <strong>{e(r[2])}</strong>. Ia nama {e(gtxt)}{", dan perkataannya terdapat dalam Al-Quran" if r[8] and not r[10] else ""}{", nama seorang nabi dalam Al-Quran" if r[10] else ""}.</p></div>
{meta_line(T_, TMS)}
{facts}
<div class="act"><a class="btn2" href="/{PATH}#semak">✅ Semak nama penuh</a><a class="btn2" href="/{PATH}">👶 Penjana nama bayi</a></div>
{share(SITE + path, f"Maksud nama {name} dalam Islam:")}
</div></section>
{"".join(f'<section class="dsec" id="{i}" aria-labelledby="h-{i}"><h2 id="h-{i}">{h}</h2>{html}</section>' + (ad(0) if k == 0 else "") for k, (i, h, html) in enumerate(secs))}
<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim</h2>
{faq_html(faq)}
<p class="note">Senarai penuh: <a href="/{sub_path("P" if g == "P" else "L", name[0].upper())}">nama bayi {"perempuan" if g == "P" else "lelaki"} huruf {e(name[0].upper())}</a> · <a href="/{PATH}">semua nama bayi Islam</a>.</p>
</section>
</div>
{side(toc, PATH)}
</div>'''
    short = re.split(r"[;.] ", r[2])[0].rstrip(".")
    desc = f"Maksud nama {name} dalam Islam: {short}. Tulisan Arab {r[1]}, {'rujukan Al-Quran, ' if r[8] or r[10] else ''}ejaan lain dan cadangan nama penuh."
    if len(desc) > 160:
        desc = (f"Maksud nama {name}: {short}"[:118].rsplit(" ", 1)[0] + "… Tulisan Arab & cadangan nama penuh.")
    tail = "(Tulisan Arab & Al-Quran)" if r[8] or r[10] else "(Tulisan Arab & Ejaan)"
    title = f"Maksud Nama {name} dalam Islam {tail}"
    if len(title) > 70:
        title = f"Maksud Nama {name} dalam Islam"
    return dict(path=path, kind="ref", data=False, arabic=True, published=MPUB, nocache=True, og="nama-bayi-maksud",
                ogcard=("Maksud Nama Bayi Islam", "Maksud, tulisan Arab & rujukan Al-Quran"),
                title=title,
                ogtitle=f"Maksud Nama {name}", desc=desc[:160], crumbs=[("Nama Bayi Islam", PATH), (f"Maksud nama {name}", None)], body=body, faq=faq,
                about=[f"Nama {name}", "Maksud nama", "Nama bayi Islam"],
                nodes=[{"@type": "DefinedTerm", "@id": SITE + path + "#nama", "name": name, "alternateName": r[1], "description": r[2],
                        "inDefinedTermSet": {"@id": SITE + PATH + "#nama"}}],
                llms=f"Maksud nama {name} ({r[1]}): {r[2]}" + (f"; dalam Al-Quran {r[8]} ({r[9]} kali)" if r[8] else ""))


def build_pages17(ctx):
    T_, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    rows, drop, n_legacy, n_cur = NM.build()
    NM.write(rows)
    by = {(r[0], r[3]): r for r in rows}
    lst = listable(rows)
    var = variants_of(rows)
    N = len(lst)
    NQ = sum(1 for r in lst if r[8])
    NLx, NPx = sum(1 for r in lst if r[3] == "L"), sum(1 for r in lst if r[3] == "P")
    C = combos(rows)
    NE = sum(1 for r in lst if r[7] == "e")
    cm = f"{C // 1_000_000} juta" if C >= 2_000_000 else f"{C:,}"
    letters = Counter((r[0][0].upper(), r[3]) for r in lst)
    AZ = sorted({r[0][0].upper() for r in lst})

    gen_form = f'''<form id="nbgf" novalidate><div class="frm">
<div class="fl"><label for="nbgj">Jantina</label><select id="nbgj">{opts([("L", "Lelaki"), ("P", "Perempuan")], "L")}</select></div>
<div class="fl"><label for="nbgc">Corak nama</label><select id="nbgc">{opts([(k, t) for k, t, _ in PREFIX["L"]], "m2")}</select></div>
</div><details class="zpx nbadv"><summary>⚙️ Tetapan lanjut: huruf, tema, sumber, suku kata, nama bapa</summary><div class="frm">
<div class="fl"><label for="nbgh">Huruf awal</label><select id="nbgh">{opts([("", "Semua huruf")] + [(x, x) for x in AZ])}</select></div>
<div class="fl"><label for="nbgt">Tema maksud</label><select id="nbgt">{opts([("", "Semua tema")] + list(NM.THEMES.items()))}</select></div>
<div class="fl"><label for="nbgs">Sumber</label><select id="nbgs">{opts([("", "Semua sumber"), ("q", "Perkataan dalam Al-Quran"), ("ns", "Nabi & sahabat")])}</select></div>
<div class="fl"><label for="nbgk">Maks. suku kata</label><select id="nbgk">{opts([("", "Tiada had"), ("4", "4 suku kata"), ("5", "5 suku kata"), ("6", "6 suku kata"), ("7", "7 suku kata")])}</select><small>Tidak termasuk awalan</small></div>
<div class="fl"><label for="nbgb">Nama bapa (pilihan)</label><input id="nbgb" type="text" maxlength="40" autocomplete="off" placeholder="cth. Ahmad"><small>Untuk bin/binti dan elak nama berulang</small></div>
<label class="zck"><input type="checkbox" id="nbgx"> Huruf awal sama dengan nama bapa</label>
<label class="zck"><input type="checkbox" id="nbgw" checked> Nama pilihan editor sahaja ({NE:,} nama yang lebih lazim). Nyahtanda untuk semua {N:,} nama.</label>
</div></details></form>'''
    sample = "".join(full_card(p) for p in sample_full(rows))
    first = sorted(lst, key=lambda r: (r[0].lower(), r[3]))[:PER]
    list_cards = "".join(name_card(r, var) for r in first)
    list_form = f'''<form class="frm" id="nblf" role="search" novalidate>
<div class="fl w2"><label for="nblq">Cari nama atau maksud</label><input id="nblq" type="search" autocomplete="off" enterkeyhint="search" placeholder="cth. Aisyah, cahaya, syurga"></div>
<div class="fl"><label for="nblg">Jantina</label><select id="nblg">{opts([("", "Semua"), ("L", "Lelaki"), ("P", "Perempuan"), ("U", "Uniseks")])}</select></div>
<div class="fl"><label for="nblh">Huruf awal</label><select id="nblh">{opts([("", "Semua")] + [(x, x) for x in AZ])}</select></div>
<div class="fl"><label for="nble">Berakhir dengan</label><input id="nble" type="text" maxlength="6" autocomplete="off" placeholder="cth. ah, an, ra"></div>
<div class="fl"><label for="nbls">Sumber</label><select id="nbls">{opts([("", "Semua"), ("e", "Pilihan editor (disemak)"), ("q", "Perkataan dalam Al-Quran"), ("n", "Nabi & keluarga Nabi"), ("s", "Sahabat & tokoh Islam"), ("u", "Nama Islam umum")])}</select></div>
<div class="fl"><label for="nblt">Tema</label><select id="nblt">{opts([("", "Semua")] + list(NM.THEMES.items()))}</select></div>
<div class="fl"><label for="nbly">Suku kata</label><select id="nbly">{opts([("", "Semua"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4 atau lebih")])}</select></div>
<div class="fl"><label for="nblo">Susunan</label><select id="nblo">{opts([("az", "A–Z"), ("za", "Z–A"), ("pd", "Paling pendek"), ("rw", "Rawak")])}</select></div>
<label class="zck"><input type="checkbox" id="nbla"> Papar awalan nama berganding (Nurul, Ainul…)</label>
</form>'''

    picks = lambda names, g: [by[(n, g)] if (n, g) in by else by.get((n, "U")) for n in names]
    pick_rows = lambda names, g: [[f"<strong>{e(r[0])}</strong>", f'<span lang="ar" dir="rtl" class="nbta">{e(r[1])}</span>', e(r[2])] for r in picks(names, g) if r]
    cur_names = {ln.split("|")[0] for blk in (ND.LELAKI, ND.PEREMPUAN) for ln in blk.strip().splitlines()}
    qrows = sorted([r for r in lst if r[8] and not r[10] and r[0] in cur_names and r[4] != "n"], key=lambda r: -r[9])[:50]
    qtab = [[f"<strong>{e(r[0])}</strong> <small>({GL[r[3]]})</small>", f'<span lang="ar" dir="rtl" class="nbta">{e(r[1])}</span>', e(r[2]),
             qref(*map(int, r[8].split(":"))) + (f" · {r[9]}×" if r[9] > 1 else "")] for r in qrows]
    import nabi as NB
    nabi_rows = [[f'<a href="/kisah-nabi/{n["slug"]}/">{e(NB.title(n))}</a>', f'<span lang="ar" dir="rtl" class="nbta">{e(n["ar"])}</span>',
                  e(by[(n["nama"], "L")][2]) if (n["nama"], "L") in by else ""] for n in NB.NABI]
    women = [r for r in lst if r[3] == "P" and r[4] in "ns" and r[0] in cur_names]
    wrows = [[f"<strong>{e(r[0])}</strong>", f'<span lang="ar" dir="rtl" class="nbta">{e(r[1])}</span>', e(r[2])] for r in women]
    abd = [r for r in rows if r[7] == "b"]
    arows = [[f"<strong>{e(r[0])}</strong>", f'<span lang="ar" dir="rtl" class="nbta">{e(r[1])}</span>', e(r[2])] for r in abd]
    LET = letter_sets(lst)
    def azcell(x):
        out = []
        for g, w in (("L", "lelaki"), ("P", "perempuan")):
            n = len(LET.get((x, g), []))
            out.append(f'<a href="/{sub_path(g, x)}">{n} {w}</a>' if (x, g) in LET else f"<small>{letters[(x, g)]} {w}</small>")
        return f'<li><b>{x}</b>{"".join(out)}</li>'
    az = "".join(azcell(x) for x in AZ)
    avoid = [
        ["Nama khusus bagi Allah", "Ar-Rahman, Al-Khaliq, Ar-Razzaq, Al-Ahad, As-Samad, Al-Quddus, Al-Jabbar, Al-Qahhar, Al-Qayyum",
         "Gunakan bentuk hamba: Abdul Rahman, Abdul Khaliq, Abdul Razak. Ulama melarang nama yang hanya layak bagi Allah (Ibn al-Qayyim, <em>Tuhfat al-Maudud</em>)."],
        ["Menghambakan diri kepada selain Allah", "Abdul Nabi, Abdul Rasul, Abdul Kaabah, Abdul Husain",
         "Ulama sepakat melarangnya (ijmak dinukil oleh Ibn Hazm). Abdul hanya disambung dengan Asmaul Husna."],
        ["Raja segala raja", "Malikul Muluk, Syahansyah (Shahanshah)",
         "“Nama yang paling hina di sisi Allah ialah seorang lelaki yang dinamakan Raja segala raja” (HR Al-Bukhari 6205; Muslim 2143)."],
        ["Nama yang dimakruhkan", "Yasar, Rabah, Najih, Aflah, Nafi'",
         "Rasulullah ﷺ melarang nama ini kerana jawapan “dia tiada” apabila ditanya tentangnya (HR Muslim 2136–2137). Hukumnya makruh, bukan haram."],
        ["Memuji diri sendiri", "Barrah (yang sangat baik)", "Rasulullah ﷺ menukar nama Barrah kepada Zainab (HR Al-Bukhari 6192)."],
        ["Maksud yang buruk", "Harb (perang), Jahl (kejahilan), ‘Asiyah dengan ain (yang derhaka)",
         "Rasulullah ﷺ menukar nama ‘Asiyah (عَاصِيَة) kepada Jamilah (HR Muslim 2139). Asiah (آسِيَة), isteri Firaun yang beriman, berbeza ejaannya dan maksudnya baik."],
        ["Gelaran keturunan", "Syed, Sharifah, Tengku, Wan, Nik, Megat",
         "Gelaran adat dan keturunan, bukan nama. Gunakan hanya jika anak memang berhak mengikut nasab."],
    ]
    faq = [
        ("Bilakah waktu terbaik memberi nama bayi dalam Islam?",
         "Sunnah memberi nama pada hari ketujuh bersama akikah dan mencukur rambut (HR Abu Dawud 2838; At-Tirmizi 1522, sahih). Memberi nama pada hari lahir juga sunnah: Rasulullah ﷺ menamakan puteranya Ibrahim pada malam dia dilahirkan (HR Muslim 2315). Kedua-duanya dibolehkan."),
        ("Apakah nama yang paling disukai Allah?",
         "“Nama kamu yang paling disukai Allah ialah Abdullah dan Abdul Rahman” (HR Muslim 2132). Nama para nabi juga digalakkan: “Namakanlah dengan namaku” (HR Al-Bukhari 3539; Muslim 2133), dan nama yang membawa maksud baik."),
        ("Bolehkah menggunakan nama Asmaul Husna untuk anak?",
         "Nama yang khusus bagi Allah seperti Ar-Rahman, Al-Khaliq, Ar-Razzaq, Al-Ahad dan As-Samad tidak boleh digunakan secara sendirian; gunakan Abdul Rahman, Abdul Khaliq dan seumpamanya. Sifat yang juga layak bagi manusia seperti Ali, Hakim, Karim dan Rasyid boleh digunakan, dan para sahabat memakai nama ini."),
        ("Apakah maksud label “Perkataan dalam Al-Quran”?",
         f"Ia bermaksud perkataan Arab nama itu terdapat dalam teks Al-Quran, dan alat ini memaparkan ayat pertama yang mengandunginya. Semakan dibuat secara automatik terhadap 6,236 ayat. Ia tidak bermaksud perkataan itu nama seseorang dalam Al-Quran, dan maksudnya dalam ayat mungkin berbeza. {NQ:,} nama dalam senarai ini lulus semakan."),
        ("Adakah nama Nurul Aisyah atau Nur Aisyah betul dari segi bahasa Arab?",
         "Nur bermaksud cahaya. Dalam bahasa Arab, Nurul (نُورُ الْ) sepatutnya disambung dengan perkataan berawalan al-, contohnya Nurul Huda (cahaya petunjuk) atau Nurul Iman (cahaya iman). Gabungan seperti Nurul Aisyah lazim di Malaysia sebagai uruf, tetapi maksudnya bukan terjemahan frasa Arab yang tepat."),
        ("Bolehkah memberi nama Melayu atau bukan Arab kepada anak?",
         "Boleh. Islam tidak mewajibkan nama Arab. Syaratnya maksud nama itu baik, bukan nama khusus bagi agama lain atau sembahan, dan tidak termasuk nama yang dilarang. Ramai sahabat mengekalkan nama asal mereka selepas memeluk Islam, dan Rasulullah ﷺ hanya menukar nama yang maksudnya buruk."),
        ("Bagaimana memastikan maksud nama anak betul?",
         "Semak ejaan Arab, bukan ejaan Rumi sahaja, kerana satu ejaan Rumi boleh datang daripada perkataan Arab yang berbeza (contohnya Asiah آسِيَة dan ‘Asiyah عَاصِيَة). Gunakan Semak Nama di atas, kemudian sahkan dengan guru agama atau kamus Arab sebelum mendaftar di Jabatan Pendaftaran Negara."),
        ("Berapa banyak nama dalam penjana ini?",
         f"{N:,} nama tunggal ({NLx:,} lelaki, {NPx:,} perempuan, selebihnya uniseks) dengan ejaan Arab dan maksud Bahasa Melayu, serta {len(abd)} nama Abdul + Asmaul Husna. Penjana nama penuh boleh menggabungkannya menjadi lebih {cm} nama penuh, dan setiap gabungan memaparkan maksud setiap bahagian."),
        ("Perlukah menukar nama yang maksudnya kurang baik?",
         "Rasulullah ﷺ menukar nama yang buruk maksudnya, contohnya ‘Asiyah kepada Jamilah (HR Muslim 2139). Jika nama anak anda bermaksud buruk, menukarnya digalakkan; pertukaran nama dalam MyKad dibuat melalui Jabatan Pendaftaran Negara."),
    ]
    k197, k336 = quran_block([(19, 7)]), quran_block([(3, 36)])
    body = hero("Nama Bayi Islam: Penjana Nama, Maksud & Ejaan Arab",
                f"{N:,} nama bayi Islam lelaki dan perempuan dengan maksud dan tulisan Arab, {NQ:,} disemak terhadap teks Al-Quran. "
                f"Jana nama penuh, tapis ikut huruf dan tema, dan semak nama mengikut panduan hadis.",
                [("Nama Bayi Islam", None)])
    body += f'''<div class="wrap mn"><div class="ct" id="nbapp">
<section id="jana" class="tool" aria-labelledby="h-jana">
<h2 id="h-jana">✨ Penjana Nama Penuh</h2>
<p>Pilih jantina dan corak, kemudian tekan <strong>Jana</strong>. Setiap nama memaparkan tulisan Arab dan maksud setiap bahagian.</p>
{gen_form}
<div class="act"><button class="btn3" type="button" id="nbgo">🎲 Jana 12 nama</button><button class="btn2" type="button" id="nbgl">🔗 Salin pautan tetapan</button><a class="btn2" href="#simpan">♡ Senarai pendek (<span class="nbcnt">0</span>)</a></div>
<p class="nbsum" id="nbgn" aria-live="polite">Contoh: Muhammad + 2 nama lelaki · lebih {cm} gabungan nama penuh dalam penjana ini</p>
<ol class="nbgl" id="nbgr">{sample}</ol>
</section>

<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> Pilih nama yang <strong>maksudnya baik</strong>, sebaik-baiknya nama nabi, sahabat atau nama yang menghambakan diri kepada Allah seperti <strong>Abdullah dan Abdul Rahman</strong>, nama yang paling disukai Allah (HR Muslim 2132). Elakkan nama yang khusus bagi Allah tanpa “Abdul”, nama yang menghambakan diri kepada selain Allah dan nama yang buruk maksudnya. Nama diberi pada hari lahir atau hari ketujuh bersama akikah. Semak ejaan Arab, bukan Rumi sahaja, kerana satu ejaan Rumi boleh membawa maksud yang berbeza.</p></div>
{meta_line(T_, TMS)}
{share(SITE + PATH, "Penjana nama bayi Islam: maksud, tulisan Arab dan semakan nama ikut hadis:")}
</div>
</section>

<section id="senarai" class="tool" aria-labelledby="h-senarai">
<h2 id="h-senarai">🔎 Cari & Tapis {N:,} Nama</h2>
{list_form}
<p class="nbsum" id="nbln" aria-live="polite">Memaparkan {len(first)} daripada {N:,} nama</p>
<ul class="nbl" id="nblr">{list_cards}</ul>
<div class="act"><button class="btn2" type="button" id="nblm">Papar {PER} lagi</button></div>
<h3 id="h-az">Nama Bayi Islam Ikut Huruf (A–Z)</h3>
<ul class="nbaz" aria-labelledby="h-az">{az}</ul>
</section>
{ad(0)}
<section id="semak" class="tool" aria-labelledby="h-semak">
<h2 id="h-semak">✅ Semak Nama</h2>
<p>Taip nama penuh (boleh dengan bin/binti). Setiap bahagian disemak: maksud, ejaan Arab, Abdul + Asmaul Husna, nama khusus bagi Allah dan nama yang dimakruhkan dalam hadis.</p>
<form class="frm" id="nbkf" novalidate><div class="fl w2"><label for="nbkq">Nama penuh</label><input id="nbkq" type="text" maxlength="120" autocomplete="off" placeholder="cth. Muhammad Rayyan Hakimi bin Ahmad"></div>
<div class="act w2"><button class="btn3" type="submit">Semak nama</button></div></form>
<div id="nbkr" aria-live="polite"><p class="note">Keputusan akan dipaparkan di sini.</p></div>
</section>

<section id="simpan" class="tool" aria-labelledby="h-simpan">
<h2 id="h-simpan">♡ Senarai Pendek (<span class="nbcnt">0</span>)</h2>
<div id="nbsh"></div>
<ol class="nbsv" id="nbsv"><li class="nbe">Tekan ♡ pada mana-mana nama untuk menyimpannya di sini. Senarai disimpan dalam peranti ini sahaja.</li></ol>
<div class="act"><button class="btn2" type="button" data-sv="copy">📋 Salin</button><button class="btn2" type="button" data-sv="wa">💬 Kongsi WhatsApp</button><button class="btn2" type="button" data-sv="link">🔗 Pautan untuk pasangan</button><button class="btn2" type="button" data-sv="clear">🗑 Kosongkan</button></div>
<p class="note">Hantar pautan kepada pasangan atau keluarga: mereka boleh melihat senarai anda dan menyimpannya dalam telefon mereka.</p>
</section>

<section id="pilihan" aria-labelledby="h-pilihan">
<h2 id="h-pilihan">Nama Bayi Lelaki Islam Pilihan Editor</h2>
<p>Nama yang lazim dan mudah disebut di Malaysia, dengan maksud yang baik. Senarai pilihan editor, bukan statistik pendaftaran.</p>
{table(["Nama", "Arab", "Maksud"], pick_rows(PICK_L, "L"), "Nama bayi lelaki pilihan")}
<h2 id="h-pilihan-p">Nama Bayi Perempuan Islam Pilihan Editor</h2>
{table(["Nama", "Arab", "Maksud"], pick_rows(PICK_P, "P"), "Nama bayi perempuan pilihan")}
</section>

<section id="quran" aria-labelledby="h-quran">
<h2 id="h-quran">Nama daripada Perkataan Al-Quran (dengan Ayat)</h2>
<p>Perkataan Arab setiap nama di bawah dijumpai dalam teks Al-Quran. Lajur terakhir ialah ayat pertama yang mengandunginya dan bilangan kali ia muncul; tekan untuk membaca ayat itu.</p>
{table(["Nama", "Arab", "Maksud", "Ayat"], qtab, "Nama daripada perkataan Al-Quran")}
</section>

<section id="nabi" aria-labelledby="h-nabi">
<h2 id="h-nabi">Nama 25 Nabi dan Rasul</h2>
{table(["Nabi", "Arab", "Maksud"], nabi_rows, "Nama 25 nabi")}
<h2 id="h-wanita">Nama Ummahatul Mukminin, Keluarga Nabi & Sahabiyah</h2>
{table(["Nama", "Arab", "Tentang nama"], wrows, "Nama wanita Islam pilihan")}
</section>

<section id="abdul" aria-labelledby="h-abdul">
<h2 id="h-abdul">{len(abd)} Nama Abdul + Asmaul Husna</h2>
<p>Abdul bermaksud “hamba kepada”, jadi ia mesti disambung dengan salah satu <a href="/asmaul-husna/">Asmaul Husna</a>. Nama yang jarang atau kurang sesuai dijadikan nama (seperti Abdul Mumit) tidak disenaraikan.</p>
{table(["Nama", "Arab", "Maksud"], arows, "Nama Abdul dan Asmaul Husna")}
</section>
{ad(1)}
<section id="panduan" class="dsec" aria-labelledby="h-panduan">
<h2 id="h-panduan">Adab Memberi Nama dalam Islam</h2>
<ol class="steps"><li><strong>Pilih maksud yang baik.</strong> Nama ialah doa dan identiti anak sepanjang hayat.</li>
<li><strong>Utamakan</strong> Abdullah, Abdul Rahman dan Abdul + Asmaul Husna, nama para nabi, sahabat dan orang soleh.</li>
<li><strong>Semak ejaan Arab.</strong> Ejaan Rumi yang sama boleh membawa maksud lain.</li>
<li><strong>Beri nama</strong> pada hari lahir atau hari ketujuh bersama akikah.</li>
<li><strong>Elakkan</strong> nama dalam jadual di bawah.</li></ol>
{card("ayat-19-7", "Maryam 7: Allah sendiri menamakan Yahya", k197[0], k197[1], k197[2], qref(19, 7))}
{card("ayat-3-36", "Ali Imran 36: ibu Maryam menamakan anaknya", k336[0], k336[1], k336[2], qref(3, 36))}
<ul class="src"><li>“Nama kamu yang paling disukai Allah ialah Abdullah dan Abdul Rahman” (HR Muslim 2132).</li>
<li>“Setiap bayi tergadai dengan akikahnya, disembelih untuknya pada hari ketujuh, dicukur rambutnya dan diberi nama” (HR Abu Dawud 2838; At-Tirmizi 1522).</li>
<li>“Malam tadi lahir untukku seorang anak lelaki, lalu aku menamakannya dengan nama bapaku, Ibrahim” (HR Muslim 2315).</li></ul>
<h3 id="h-elak">Nama yang perlu dielakkan</h3>
{table(["Jenis", "Contoh", "Dalil & panduan"], avoid, "Nama yang perlu dielakkan")}
</section>

<section id="kaedah" aria-labelledby="h-kaedah">
<h2 id="h-kaedah">Sumber Data & Cara Kami Menyemak</h2>
<ul>
<li><strong>Asal data:</strong> pangkalan data nama IlmuAlam (versi 4.0, Disember 2025; {n_legacy + sum(drop.values()):,} baris) yang sebelum ini di name.ilmualam.com, kini digabungkan di sini.</li>
<li><strong>Dibersihkan:</strong> {sum(drop.values())} baris dibuang: {", ".join(f"{v} {k}" for k, v in drop.items())}. Maksud “Yang Maha …” bagi nama manusia ditukar kepada “Yang sangat …”.</li>
<li><strong>Ditambah dan disunting editor:</strong> {n_cur} nama, termasuk 25 nabi, Ummahatul Mukminin, sahabat dan sahabiyah dengan fakta ringkas, serta {len(abd)} nama Abdul + Asmaul Husna yang dijana daripada <a href="/asmaul-husna/">senarai 99 nama</a>.</li>
<li><strong>Semakan Al-Quran automatik:</strong> setiap nama satu perkataan dicari dalam 6,236 ayat (teks Uthmani, termasuk bentuk dengan awalan al-, wa-, fa-, bi-, li-, ka-). Label “Perkataan dalam Al-Quran” hanya diberi jika perkataan itu dijumpai.</li>
<li><strong>Had:</strong> maksud dan ejaan Arab bagi nama umum belum disahkan satu per satu oleh pakar bahasa Arab, dan ejaan variasi disenaraikan berasingan. Maksud gabungan nama ialah maksud setiap bahagian, bukan terjemahan frasa Arab baharu. Jumpa kesilapan? <a href="/hubungi-kami/">Beritahu kami</a>.</li>
</ul>
<p class="note">Data nama boleh dimuat turun: <a href="/assets/data/nama-bayi.json">nama-bayi.json</a> (JSON).</p>
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: Nama Bayi Islam</h2>
{faq_html(faq)}
<p class="note">Lihat juga <a href="/asmaul-husna/">Asmaul Husna</a>, <a href="/kisah-nabi/">Kisah 25 Nabi</a> dan <a href="/doa-harian/">doa harian</a>.</p>
</section>
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(PATH)}</section>
</div>
{side([("jana", "Penjana nama penuh"), ("senarai", "Cari & tapis nama"), ("semak", "Semak nama"), ("simpan", "Senarai pendek"), ("pilihan", "Pilihan editor"), ("quran", "Nama dari Al-Quran"), ("nabi", "Nama nabi & sahabiyah"), ("abdul", "Abdul + Asmaul Husna"), ("panduan", "Adab & larangan"), ("faq", "Soalan lazim")], PATH)}
</div>'''
    terms = [{"@type": "DefinedTerm", "name": r[0], "alternateName": r[1], "description": r[2], "inDefinedTermSet": {"@id": SITE + PATH + "#nama"}}
             for r in picks(PICK_L, "L") + picks(PICK_P, "P") if r]
    nodes = [{"@type": "DefinedTermSet", "@id": SITE + PATH + "#nama", "name": "Nama bayi Islam pilihan editor dengan maksud", "inLanguage": "ms-MY", "hasDefinedTerm": terms},
             {"@type": "Dataset", "@id": SITE + PATH + "#data", "name": "Pangkalan data nama bayi Islam IlmuAlam", "inLanguage": "ms-MY",
              "description": f"{N:,} nama Islam dengan ejaan Arab, maksud Bahasa Melayu, jantina, suku kata, tema dan rujukan ayat Al-Quran jika perkataan itu terdapat dalam Al-Quran.",
              "isAccessibleForFree": True, "creator": {"@id": "https://www.ilmualam.com/#org"}, "dateModified": T_,
              "distribution": {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": SITE + "assets/data/nama-bayi.json"}}]
    edrows = [r for r in rows if r[7] in ("e", "b")]
    groups = defaultdict(list)
    for r in edrows:
        groups[r[0]].append(r)
    MP.clear()
    MP.update({n.lower(): m_path(n) for n in groups})
    assert len({slug(n) for n in groups}) == len(groups), "two names share a slug"
    mpages = [maksud_page(n, rs, edrows, var, T_, TMS, share, ad) for n, rs in sorted(groups.items())]
    subs = [sub_page(g, x, names, LET, by, T_, TMS, share, ad) for (x, g), names in sorted(LET.items(), key=lambda k: (k[0][1], k[0][0]))]
    return [dict(path=PATH, kind="tool", data=False, arabic=True, published=PUB, scripts=["/assets/js/nama.js"],
                 title="Nama Bayi Islam: Penjana Nama, Maksud & Ejaan Arab",
                 ogtitle="Nama Bayi Islam & Maksud", ogcard=("Nama Bayi Islam", f"{N:,} nama dengan maksud & tulisan Arab · penjana nama penuh · semak nama ikut hadis"),
                 desc=f"{N:,} nama bayi Islam lelaki & perempuan dengan maksud dan tulisan Arab. Jana nama penuh, cari ikut huruf atau tema, dan semak nama ikut hadis.",
                 crumbs=[("Nama Bayi Islam", None)], body=body, faq=faq, nodes=nodes,
                 about=["Nama bayi Islam", "Nama Islam", "Maksud nama", "Nama bayi lelaki", "Nama bayi perempuan", "Akikah"],
                 app=dict(name="Penjana Nama Bayi Islam", features=[f"{N:,} nama dengan tulisan Arab dan maksud", f"Penjana nama penuh (lebih {cm} gabungan)",
                                                                   "Tapis ikut jantina, huruf awal & akhir, tema, sumber dan suku kata", f"{NQ:,} nama disemak terhadap teks Al-Quran",
                                                                   "Semak nama: Abdul + Asmaul Husna, nama khusus bagi Allah, nama makruh", "Senarai pendek dengan pautan kongsi"]),
                 llms=f"Penjana nama bayi Islam: {N:,} nama (lelaki {NLx:,}, perempuan {NPx:,}) dengan tulisan Arab dan maksud Melayu; {NQ:,} perkataan nama disahkan terdapat dalam Al-Quran dengan rujukan ayat; "
                      f"penjana nama penuh (Muhammad/Ahmad/Nur/Nurul/Siti + nama, lebih {cm} gabungan); semak nama ikut hadis (Abdullah & Abdul Rahman paling disukai Allah, HR Muslim 2132; "
                      "nama khusus bagi Allah, Malikul Muluk HR Al-Bukhari 6205, nama makruh HR Muslim 2136-2137). Data: /assets/data/nama-bayi.json.")] + subs + mpages
