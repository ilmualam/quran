"""Pages: /surah-<nama>/ x10, one static page per most-searched surah (Yasin, Al-Mulk, Al-Kahfi, Al-Waqiah, Ar-Rahman,
Al-Fatihah, As-Sajdah and the three Qul). Every ayah is rendered into the HTML straight from data-surah/ (Arabic, Rumi,
Malay translation), so the full text is crawlable and readable without JavaScript; audio and bookmarks stay in the
in-page reader (/#surah-N), which each ayah links to.

Intent split with www.ilmualam.com: these pages answer "baca surah X" (full text, facts, where it sits in the mushaf);
the Blogger article (ARTICLES) keeps the long-form "kelebihan / tafsir" content and is linked, not duplicated.
Virtues listed here carry the hadith reference and, where scholars grade it weak, say so."""
import json, re
import plans as P
import rumi_ms as RM
from surahs import S, MADANI, ARTICLES
from pages import e, faq_html, hero, side, meta_line, table, tool_cards, SITE

PUB = "2026-11-07"

# n: (slug, readers' everyday name, [(virtue, source, weak?)], when it is usually read)
SURAH = {
    36: ("surah-yasin", "Yasin", [
        ("Disebut sebagai “hati Al-Quran”.", "HR At-Tirmizi 2887; At-Tirmizi sendiri menyebutnya gharib dan ramai ulama hadis menilainya dhaif", True),
        ("Digalakkan dibaca kepada orang yang hampir meninggal dunia.", "HR Abu Dawud 3121 dan Ibnu Majah 1448; dinilai sahih oleh Ibnu Hibban dan dhaif oleh sebahagian ulama", True),
    ], "Malam Jumaat, majlis tahlil dan ketika menziarahi orang yang sakit tenat (amalan masyarakat Malaysia)"),
    67: ("surah-al-mulk", "Al-Mulk (Tabarak)", [
        ("Surah 30 ayat yang memberi syafaat kepada pembacanya sehingga dia diampunkan.", "HR Abu Dawud 1400 dan At-Tirmizi 2891 (hasan)", False),
        ("Nabi SAW tidak tidur sehingga membaca Alif Lam Mim Tanzil (As-Sajdah) dan Tabarak (Al-Mulk).", "HR At-Tirmizi 2892", False),
    ], "Setiap malam sebelum tidur"),
    18: ("surah-al-kahfi", "Al-Kahfi", [
        ("Sesiapa yang menghafal sepuluh ayat awal Surah Al-Kahfi dilindungi daripada fitnah Dajjal.", "HR Muslim 809", False),
        ("Sesiapa membaca Surah Al-Kahfi pada hari Jumaat, dia disinari cahaya antara dua Jumaat.", "HR Al-Hakim dan Al-Baihaqi; dinilai sahih oleh Al-Albani (Sahih al-Jami' 6470)", False),
    ], "Malam Jumaat atau hari Jumaat"),
    56: ("surah-al-waqiah", "Al-Waqiah", [
        ("Sesiapa membaca Surah Al-Waqiah setiap malam tidak akan ditimpa kefakiran.", "Riwayat Ibnu As-Sunni dan Al-Baihaqi (Syu'ab al-Iman); dinilai dhaif oleh ramai ulama hadis, namun sebahagian ulama membenarkan beramal dengannya untuk fadhilat", True),
    ], "Selepas Maghrib atau Isyak setiap malam (amalan masyarakat)"),
    55: ("surah-ar-rahman", "Ar-Rahman", [
        ("Nabi SAW membacakan Surah Ar-Rahman kepada para sahabat dan memberitahu bahawa jin menjawab setiap kali ayat “Fabi ayyi ala'i Rabbikuma tukazziban” dibaca: “Tiada satu pun nikmat-Mu, wahai Tuhan kami, yang kami dustakan; segala puji bagi-Mu.”", "HR At-Tirmizi 3291 (hasan menurut Al-Albani)", False),
    ], "Bila-bila masa; ramai yang membacanya sebagai zikir syukur"),
    1: ("surah-al-fatihah", "Al-Fatihah", [
        ("Tidak sah solat bagi sesiapa yang tidak membaca Al-Fatihah.", "HR Al-Bukhari 756 dan Muslim 394", False),
        ("Surah paling agung dalam Al-Quran, “tujuh ayat yang diulang-ulang” (As-Sab'ul Mathani).", "HR Al-Bukhari 4474; rujuk Al-Hijr 15:87", False),
    ], "Setiap rakaat solat, serta pembuka doa dan majlis"),
    32: ("surah-as-sajdah", "As-Sajdah", [
        ("Nabi SAW membaca As-Sajdah (rakaat pertama) dan Al-Insan (rakaat kedua) dalam solat Subuh hari Jumaat.", "HR Al-Bukhari 891 dan Muslim 880", False),
        ("Nabi SAW tidak tidur sehingga membaca Alif Lam Mim Tanzil (As-Sajdah) dan Tabarak (Al-Mulk).", "HR At-Tirmizi 2892", False),
    ], "Subuh hari Jumaat dan sebelum tidur"),
    112: ("surah-al-ikhlas", "Al-Ikhlas", [
        ("Surah Al-Ikhlas menyamai sepertiga Al-Quran.", "HR Al-Bukhari 5013 dan Muslim 811", False),
        ("Nabi SAW membaca Al-Ikhlas, Al-Falaq dan An-Nas, meniup ke tapak tangan dan menyapu badan setiap malam sebelum tidur.", "HR Al-Bukhari 5017", False),
    ], "Sebelum tidur, selepas solat fardu dan dalam zikir pagi petang"),
    113: ("surah-al-falaq", "Al-Falaq", [
        ("Ayat-ayat yang diturunkan malam itu, tidak pernah dilihat seumpamanya: Qul a'uzu bi rabbil-falaq dan Qul a'uzu bi rabbin-nas.", "HR Muslim 814", False),
        ("Nabi SAW membaca tiga Qul, meniup ke tapak tangan dan menyapu badan setiap malam sebelum tidur.", "HR Al-Bukhari 5017", False),
    ], "Sebelum tidur, selepas solat fardu dan untuk perlindungan (ruqyah)"),
    114: ("surah-an-nas", "An-Nas", [
        ("Ayat-ayat yang diturunkan malam itu, tidak pernah dilihat seumpamanya: Qul a'uzu bi rabbil-falaq dan Qul a'uzu bi rabbin-nas.", "HR Muslim 814", False),
        ("Nabi SAW membaca tiga Qul, meniup ke tapak tangan dan menyapu badan setiap malam sebelum tidur.", "HR Al-Bukhari 5017", False),
    ], "Sebelum tidur, selepas solat fardu dan untuk perlindungan (ruqyah)"),
}
ORDER = [36, 67, 18, 56, 55, 1, 32, 112, 113, 114]  # the most-searched surah, listed on every surah page
assert sorted(ORDER) == sorted(SURAH)
# the other 104 surah: virtues only where a sahih or hasan hadis names the surah; the rest show the general reward of reading
VIRTUE = {
    2: ([("Syaitan lari daripada rumah yang dibacakan Surah Al-Baqarah.", "HR Muslim 780", False),
         ("Al-Baqarah dan Ali Imran datang pada hari kiamat seperti dua awan yang menaungi pembacanya.", "HR Muslim 804", False)], "Di rumah, supaya rumah dijauhi syaitan"),
    3: ([("Al-Baqarah dan Ali Imran datang pada hari kiamat seperti dua awan yang menaungi pembacanya.", "HR Muslim 804", False)], "Bersama Surah Al-Baqarah"),
    11: ([("Nabi SAW bersabda: Hud dan surah-surah yang seumpamanya menyebabkan rambutku beruban.", "HR At-Tirmizi 3297 (hasan)", False)], None),
    17: ([("Nabi SAW tidak tidur sehingga membaca Bani Israil (Al-Isra') dan Az-Zumar.", "HR At-Tirmizi 2920 (hasan)", False)], "Sebelum tidur"),
    39: ([("Nabi SAW tidak tidur sehingga membaca Bani Israil (Al-Isra') dan Az-Zumar.", "HR At-Tirmizi 2920 (hasan)", False)], "Sebelum tidur"),
    48: ([("Nabi SAW bersabda: Telah diturunkan kepadaku malam ini satu surah yang lebih aku cintai daripada apa yang disinari matahari, lalu baginda membaca Al-Fath.", "HR Al-Bukhari 4833", False)], None),
    50: ([("Nabi SAW membaca Qaf dan Al-Qamar dalam solat Hari Raya.", "HR Muslim 891", False),
          ("Ummu Hisyam menghafal Surah Qaf daripada lisan Nabi SAW yang membacanya dalam khutbah Jumaat.", "HR Muslim 873", False)], "Solat Hari Raya dan khutbah Jumaat"),
    54: ([("Nabi SAW membaca Qaf dan Al-Qamar dalam solat Hari Raya.", "HR Muslim 891", False)], "Solat Hari Raya"),
    62: ([("Nabi SAW membaca Al-Jumu'ah dan Al-Munafiqun dalam solat Jumaat.", "HR Muslim 877", False)], "Solat Jumaat"),
    63: ([("Nabi SAW membaca Al-Jumu'ah dan Al-Munafiqun dalam solat Jumaat.", "HR Muslim 877", False)], "Solat Jumaat"),
    76: ([("Nabi SAW membaca As-Sajdah (rakaat pertama) dan Al-Insan (rakaat kedua) dalam solat Subuh hari Jumaat.", "HR Al-Bukhari 891 dan Muslim 880", False)], "Subuh hari Jumaat"),
    87: ([("Nabi SAW membaca Al-A'la dan Al-Ghasyiyah dalam solat Hari Raya dan solat Jumaat.", "HR Muslim 878", False)], "Solat Jumaat dan Hari Raya"),
    88: ([("Nabi SAW membaca Al-A'la dan Al-Ghasyiyah dalam solat Hari Raya dan solat Jumaat.", "HR Muslim 878", False)], "Solat Jumaat dan Hari Raya"),
    109: ([("Nabi SAW membaca Al-Kafirun dan Al-Ikhlas dalam dua rakaat sunat sebelum Subuh.", "HR Muslim 726", False)], "Solat sunat sebelum Subuh"),
}
GENERAL = [("Setiap huruf Al-Quran yang dibaca diberi satu kebaikan, dan satu kebaikan digandakan sepuluh kali.", "HR At-Tirmizi 2910", False),
           ("Orang yang mahir membaca Al-Quran bersama para malaikat yang mulia, dan orang yang membacanya tersekat-sekat dengan susah payah mendapat dua pahala.", "HR Al-Bukhari 4937 dan Muslim 798", False)]
MUQ = {20, 36, 38, 50}  # named after their opening letters (huruf muqatta'ah)
for _n in range(1, 115):
    if _n not in SURAH:
        _v, _w = VIRTUE.get(_n, ([], None))
        SURAH[_n] = ("surah-" + re.sub(r"[^a-z0-9]+", "-", S[_n][1].lower().replace("'", "")).strip("-"), S[_n][1], _v, _w)
PATH = {n: SURAH[n][0] + "/" for n in SURAH}
assert len(set(PATH.values())) == 114


def load(n):
    return json.load(open(f"{P.REPO}/data-surah/surah-{n}.json", encoding="utf8"))


BASMALAH = load(1)[0]


def facts(n, ayat):
    ar, ru, mean, _ = S[n]
    first, last = P.gid(n, 1), P.gid(n, len(ayat))
    p1, p2 = P.page_of(first), P.page_of(last)
    juz = sorted({j for j in range(1, 31) if P.JS[j - 1] <= last and P.JS[j] > first})
    sajdah = [a for s, a in P.META["sajda"] if s == n]
    return dict(ar=ar, ru=ru, mean=mean, n=len(ayat), kind="Madaniyyah" if n in MADANI else "Makkiyyah",
                pages=f"{p1}" if p1 == p2 else f"{p1}–{p2}", npages=p2 - p1 + 1, juz=juz, sajdah=sajdah)


def ayah_list(n, ayat):
    out = []
    if n not in (1, 9):
        out.append(f'<p class="dar sbas" lang="ar" dir="rtl">{e(BASMALAH["arabic"])}</p>'
                   f'<p class="dru sbas"><em>{e(RM.RUMI[(1, 1)] if RM.live(n) else BASMALAH["rumi"])}</em></p>')
    for v in ayat:
        a = v["id"]
        out.append(f'<article class="dw sv" id="ayat-{a}"><header class="dh"><h3>Ayat {a}</h3>'
                   f'<a class="note" href="/#surah-{n}-ayat-{a}" aria-label="Dengar ayat {a} dalam pembaca">▶ Dengar</a></header>'
                   f'<p class="dar" lang="ar" dir="rtl">{e(v["arabic"])} <span class="an">﴿{a}﴾</span></p>'
                   f'<p class="dru"><em>{e(RM.rumi(n, a, v["rumi"]))}</em></p><p class="dmn">{e(v["translation"])}</p></article>')
    return "".join(out)


def build_pages15(ctx):
    T, TMS = ctx["TODAY"], ctx["TODAYMS"]
    share, ad = ctx["share"], ctx["ad"]
    pages = []
    for n in range(1, 115):
        slug, nick, virtues, when = SURAH[n]
        ayat = load(n)
        assert [v["id"] for v in ayat] == list(range(1, len(ayat) + 1)), n
        f = facts(n, ayat)
        nm = f"Surah {f['ru']}"
        url = SITE + PATH[n]
        juz_txt = ", ".join(f"Juz {j}" for j in f["juz"])
        rows = [["Nombor surah", f"{n} daripada 114"], ["Nama Arab", f'<span lang="ar" dir="rtl" class="nar">{e(f["ar"])}</span>'],
                ["Maksud nama", e(f["mean"])], ["Bilangan ayat", str(f["n"])], ["Jenis", f["kind"]], ["Juzuk", juz_txt],
                ["Muka surat (Mushaf Madinah)", f"{f['pages']} ({f['npages']} muka surat)"]]
        if f["sajdah"]:
            rows.append(["Ayat sajdah tilawah", ", ".join(f'<a href="#ayat-{a}">ayat {a}</a>' for a in f["sajdah"])])
        if when:
            rows.append(["Biasa dibaca", e(when)])
        extra = ""
        if n == 55:
            rep = sum(1 for v in ayat if v["arabic"] == ayat[12]["arabic"])
            assert rep == 31, rep
            extra = (f'<p>Ayat <em>“{e(ayat[12]["rumi"])}”</em> ({e(ayat[12]["translation"])}) diulang <strong>{rep} kali</strong> dalam surah ini, '
                     f'bermula pada <a href="#ayat-13">ayat 13</a>.</p>')
            rows.append(["Ayat yang diulang", f"Ayat 13 diulang {rep} kali"])
        own = bool(virtues)
        if not own:
            virtues = GENERAL
        vlist = "".join(f'<li>{e(t)} <span class="nref">({e(src)})</span>{" <strong>[dhaif]</strong>" if weak else ""}</li>' for t, src, weak in virtues)
        weak_note = ('<p class="note">Hadis bertanda <strong>[dhaif]</strong> lemah sanadnya menurut ramai ulama hadis. Membaca surah ini tetap '
                     'berpahala seperti membaca mana-mana ayat Al-Quran; status hadis hanya menentukan sama ada fadhilat khusus itu boleh disandarkan kepada Nabi SAW.</p>'
                     if any(w for _, _, w in virtues) else "")
        # Yasin is named after its opening letters (muqatta'ah), so "Yasin means Yasin" would say nothing
        name_txt = (f"Nama {f['ru']} diambil daripada huruf pembukanya (huruf muqatta'ah), yang maknanya hanya diketahui Allah." if n in MUQ
                    else f"Surah ini dinamakan sempena {f['ru']}, yang disebut di dalamnya." if f["mean"] == f["ru"]
                    else f"Nama {f['ru']} bermaksud “{f['mean']}”.")
        strong = [v for v in virtues if not v[2]]
        box_tail = (f"{strong[0][0]} — {strong[0][1]}." if strong and own else f"Biasa dibaca: {when[0].lower() + when[1:]}." if when
                    else "Setiap huruf yang dibaca diberi ganjaran yang digandakan sepuluh (HR At-Tirmizi 2910).")
        art = ARTICLES.get(n)
        others = [m for m in ([n - 1] if n > 1 else []) + ([n + 1] if n < 114 else []) + ORDER if m != n]
        others = list(dict.fromkeys(others))
        juz1 = f["juz"][0]
        faq = [
            (f"Berapa ayat dalam {nm}?", f"{nm} mengandungi {f['n']} ayat (kiraan Kufah, riwayat Hafs) dan ialah surah ke-{n} dalam Al-Quran."),
            (f"{nm} dalam juzuk berapa?", f"{nm} terletak dalam {juz_txt}, pada muka surat {f['pages']} Mushaf Madinah 604 muka surat."),
            (f"Apakah maksud {nm}?", f"{name_txt} Ia surah {f['kind']}, iaitu diturunkan {'selepas' if f['kind'] == 'Madaniyyah' else 'sebelum'} hijrah Nabi SAW ke Madinah."),
            ((f"Bilakah waktu terbaik membaca {nm}?", f"{when}. " + (f"{strong[0][0]} — {strong[0][1]}." if strong else "Hadis tentang fadhilat khusus surah ini dinilai dhaif oleh ramai ulama, namun membacanya tetap berpahala seperti membaca mana-mana ayat Al-Quran."))
             if when else (f"Adakah hadis tentang kelebihan khusus {nm}?", (f"Ya: {strong[0][0]} ({strong[0][1]})." if own else
                           f"Kami tidak menemui hadis sahih yang masyhur tentang fadhilat khusus {nm}. Ganjaran umum membaca Al-Quran tetap berlaku: setiap huruf diberi satu kebaikan yang digandakan sepuluh (HR At-Tirmizi 2910)."))),
            (f"Adakah bacaan Rumi {nm} di sini cukup untuk belajar membaca?",
             "Rumi hanya alat bantu. Ia tidak dapat menggambarkan makhraj dan hukum tajwid dengan tepat, jadi gunakan bersama audio qari dan sebaik-baiknya belajar secara bertalaqqi dengan guru."),
        ]
        lead = (f"Baca {e(nm)} penuh {f['n']} ayat dalam tulisan Arab, Rumi dan terjemahan Bahasa Melayu, dengan audio ayat demi ayat.")
        body = hero(f"{e(nm)} ({e(f['ar'])}): Bacaan Penuh Arab, Rumi & Terjemahan", lead, [(nm, None)],
                    f'<p><a class="btn3" href="/#surah-{n}">🎧 Baca & dengar dengan audio 5 qari</a></p>')
        body += f'''<div class="wrap mn"><div class="ct">
<section aria-labelledby="h-jwp">
<div class="prose">
<h2 id="h-jwp" class="sr">Ringkasan</h2>
<div class="box"><p><strong>Jawapan ringkas:</strong> {e(nm)} ialah surah ke-{n} dalam Al-Quran, surah <strong>{f["kind"]}</strong> yang mengandungi <strong>{f["n"]} ayat</strong>, dalam {juz_txt} (muka surat {f["pages"]} Mushaf Madinah). {e(name_txt)} {e(box_tail)}</p></div>
{meta_line(T, TMS)}
{share(url, f"Baca {nm} penuh: Arab, Rumi & terjemahan:")}
</div>
</section>

<section id="fakta" aria-labelledby="h-fakta">
<h2 id="h-fakta">Fakta {e(nm)}</h2>
{table(["Perkara", "Keterangan"], rows, f"Fakta {nm}")}
{extra}
</section>

<section class="dsec" id="bacaan" aria-labelledby="h-bacaan">
<h2 id="h-bacaan">Bacaan {e(nm)} Penuh ({f["n"]} Ayat)</h2>
<p class="note">Teks Arab Uthmani dan terjemahan Abdullah Muhammad Basmeih, dipaparkan tanpa suntingan daripada dataset laman ini. {e(RM.credit()) if RM.live(n) else ""} Rumi hanya alat bantu bacaan. Tekan “▶ Dengar” untuk audio ayat itu dalam pembaca.</p>
{ayah_list(n, ayat)}
</section>
{ad(0)}
<section id="kelebihan" aria-labelledby="h-kel">
<h2 id="h-kel">{"Kelebihan " + e(nm) + " (dengan Status Hadis)" if own else "Kelebihan Membaca " + e(nm)}</h2>
{"" if own else f"<p>Tiada hadis sahih yang masyhur tentang fadhilat khusus {e(nm)} setakat semakan kami. Ganjaran membaca Al-Quran secara umum:</p>"}
<ul>{vlist}</ul>
{weak_note}
{f'<p><a href="{art}" rel="noopener">Baca artikel penuh kelebihan dan tafsiran {e(nm)} di ilmualam.com ↗</a></p>' if art else ""}
</section>

<section id="faq" aria-labelledby="h-faq">
<h2 id="h-faq">Soalan Lazim: {e(nm)}</h2>
{faq_html(faq)}
</section>

<section id="surah-lain" aria-labelledby="h-sl">
<h2 id="h-sl">Surah Sebelum, Selepas & Pilihan</h2>
<ul class="rel sts">{"".join(f'<li><a href="/{PATH[m]}">Surah {e(S[m][1])}</a></li>' for m in others)}</ul>
<p class="note"><a href="/#surah">Senarai 114 surah</a> · <a href="/jadual-khatam-al-quran/">Jadual khatam</a> · <a href="/jadual-hafazan-al-quran/">Jadual hafazan</a> · <a href="/senarai-juzuk-al-quran/">Juz {juz1} dan 29 juzuk lain</a> · <a href="/tentang-kami/#semakan">Sumber teks</a></p>
</section>
{ad(1)}
<section aria-labelledby="h-rel"><h2 id="h-rel">Alat Lain</h2>{tool_cards(None)}</section>
</div>
{side([("fakta", "Fakta"), ("bacaan", "Bacaan penuh"), ("kelebihan", "Kelebihan"), ("faq", "Soalan lazim"), ("surah-lain", "Surah lain")], None)}
</div>'''
        title = f"{nm} Penuh: Arab, Rumi, Terjemahan & Audio ({f['n']} Ayat)"
        if len(title) > 70:
            title = f"{nm}: Arab, Rumi & Terjemahan ({f['n']} Ayat)"
        desc = f"Baca {nm} ({f['ar']}) penuh {f['n']} ayat: teks Arab, Rumi, terjemahan Melayu, audio, fakta juzuk & muka surat, serta kelebihan bersumber."
        if len(desc) > 160:
            desc = f"Baca {nm} penuh {f['n']} ayat: Arab, Rumi, terjemahan Melayu, audio dan kelebihan bersumber."
        work = {"@type": "CreativeWork", "@id": url + "#surah", "name": nm, "alternateName": [f["ar"], f"Surah {nick}", f"Surah ke-{n}"],
                "inLanguage": "ar", "position": n, "description": f"Surah ke-{n} Al-Quran, {f['kind']}, {f['n']} ayat. Maksud nama: {f['mean']}.",
                "isPartOf": {"@type": "Book", "name": "Al-Quran", "inLanguage": "ar"},
                "workTranslation": {"@type": "CreativeWork", "name": f"Terjemahan {nm} (Abdullah Muhammad Basmeih)", "inLanguage": "ms"}}
        pages.append(dict(path=PATH[n], kind="ref", data=False, arabic=True, published=PUB, nocache=True,
                          title=title, ogtitle=f"{nm}: Bacaan Penuh Arab, Rumi & Terjemahan", desc=desc,
                          crumbs=[(nm, None)], body=body, faq=faq, about=[nm, "Al-Quran", "Bacaan Rumi"],
                          about_ref=url + "#surah", nodes=[work], ogcard=(f"{nm} ({f['n']} ayat)", "Bacaan penuh: Arab, Rumi, terjemahan Melayu & audio"),
                          llms=f"{nm} ({f['ar']}): surah ke-{n}, {f['kind']}, {f['n']} ayat, {juz_txt}, muka surat {f['pages']}. Teks penuh Arab, Rumi dan terjemahan Melayu; kelebihan dengan rujukan dan status hadis."))
    return pages
