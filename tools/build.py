import json, re, hashlib, html, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from surahs import S, MADANI, ALIAS, POPULAR, ARTICLES
from urllib.parse import quote, urlparse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCR = os.path.dirname(os.path.abspath(__file__))
SITE = "https://quran.ilmualam.com/"
MAIN = "https://www.ilmualam.com/"
TODAY = "2026-10-10"
BULAN = ["Januari", "Februari", "Mac", "April", "Mei", "Jun", "Julai", "Ogos", "September", "Oktober", "November", "Disember"]
TODAYMS = f"{int(TODAY[8:])} {BULAN[int(TODAY[5:7]) - 1]} {TODAY[:4]}"
OGIMG = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhJxqp-Slnk0sIXWrsKrRUlkwOb7NZPN-JVM3fRd5hg4RN6Ppx9k2X0jMNzMhz3Z6JS1vXNpZqEBCA4MyAuwJDs_FZD6wbPG-YiL2_znJmH6880F69I_bZbxUw7HT7xCM79S9KF_MrPcmXLHNPkpyxQiXRHSx0OhfIEyxqiVbOQ142DUKEDaS8BnNzss44/w1200-h630-p-k-no-nu/al-quran-online-baca-digital.webp"
TITLE = "Baca Al-Quran Online (Penuh 30 Juz) dengan Audio & Terjemahan"
DESC = "Baca Al-Quran online penuh 30 juzuk percuma: 114 surah dengan teks Arab, Rumi, terjemahan Bahasa Melayu & audio 5 qari. Mudah dibaca di telefon."

# ---- Google AdSense: paste the publisher ID and up to 3 ad-unit slot IDs, then rebuild ----
# Empty client = no ad code at all. Ads are never placed inside the surah reader.
ADS_CLIENT = ""  # e.g. "ca-pub-1234567890123456"
ADS_SLOTS = ["", "", ""]  # after the surah list, after "Konteks Malaysia", after the FAQ

URLS = ARTICLES
MISSING = [n for n in range(1, 115) if n not in URLS]

# ---- ayah counts straight from the data ----
AYAT = {}
for i in range(1, 115):
    AYAT[i] = len(json.load(open(f"{REPO}/data-surah/surah-{i}.json", encoding="utf8")))
assert sum(AYAT.values()) == 6236, sum(AYAT.values())

def normq(s):
    return re.sub(r"[\s\-'’`‘.]", "", s.lower())

def e(s):
    return html.escape(s, quote=True)

# ---- surah cards ----
cards = []
items = []
for n in range(1, 115):
    ar, ru, mean, juz = S[n]
    kind = "d" if n in MADANI else "k"
    kn = "Madaniyyah" if kind == "d" else "Makkiyyah"
    meta = f"{kn} · Juz {juz}"
    q = normq(f"{n} {ru} {mean} {ar} {ALIAS.get(n, '')}")
    art = (f'<a class="x" href="{URLS[n]}" rel="noopener">Artikel penuh ↗</a>' if n in URLS else "")
    cards.append(
        f'<li class="sc" data-n="{n}" data-t="{kind}" data-q="{e(q)}" data-ar="{e(ar)}" data-name="{e(ru)}" data-mean="{e(mean)}" data-ayat="{AYAT[n]}" data-meta="{meta}">'
        f'<a class="m" href="#surah-{n}"><span class="num">{n}</span><span class="nm">{e(ru)}</span>'
        f'<span class="sa" lang="ar" dir="rtl">{e(ar)}</span>'
        f'<span class="sd">{e(mean)} · {AYAT[n]} ayat · {meta}</span></a>{art}</li>'
    )
    items.append({"@type": "ListItem", "position": n, "name": f"Surah {ru}", "url": URLS.get(n, f"{SITE}#surah-{n}")})
GRID = "\n".join(cards)

POP = "".join(f'<li><a href="#surah-{n}">{e(S[n][1])}</a></li>' for n in POPULAR)

FAQ = [
 ("Adakah sah membaca Al-Quran secara online?",
  "Ya. Membaca Al-Quran melalui laman web atau aplikasi adalah sah dan diterima jumhur ulama selagi teksnya tepat dan tidak diubah. Ganjaran dikira bagi setiap huruf yang dibaca, walau pun melalui mushaf fizikal atau skrin."),
 ("Perlukah berwuduk untuk membuka dan membaca Al-Quran di telefon?",
  "Tidak diwajibkan. Ulama kontemporari umumnya menganggap skrin telefon bukan mushaf sebenar, jadi wuduk tidak menjadi syarat. Namun berwuduk tetap digalakkan sebagai adab terhadap kalam Allah."),
 ("Bolehkah wanita haid atau nifas menggunakan Al-Quran online ini?",
  "Melihat dan membaca dalam hati umumnya dibenarkan, dan mendengar audio qari diharuskan oleh jumhur ulama. Bacaan dengan suara dengan niat tilawah semasa haid atau nifas diperselisihkan; dalam mazhab Syafi'i ia ditegah, manakala sebahagian mazhab lain membenarkannya. Rujuk mufti atau pejabat agama negeri anda untuk keputusan yang tepat bagi keadaan anda."),
 ("Adakah teks Al-Quran di laman ini tepat?",
  "Teks Arab dan terjemahan dimuatkan terus daripada dataset 114 surah yang disimpan dalam laman ini tanpa sebarang suntingan pada paparan. Untuk kepastian tambahan, sentiasa rujuk mushaf bercetak yang disahkan, dan laporkan sebarang kesilapan kepada kami melalui ilmualam.com."),
 ("Boleh saya dengar bacaan daripada qari yang berbeza?",
  "Boleh. Pilihan qari ialah Mishary Rashid Alafasy, Abdul Rahman As-Sudais, Mahmoud Khalil Al-Husary, Abdul Basit dan Saad Al-Ghamadi. Audio dimainkan ayat demi ayat dan boleh disambung secara automatik."),
 ("Bolehkah saya menanda dan menyambung bacaan terakhir?",
  "Boleh. Tanda ayat dan kedudukan bacaan terakhir disimpan secara setempat dalam pelayar (localStorage) di peranti anda sahaja. Tiada akaun diperlukan, dan data itu akan hilang jika anda mengosongkan data pelayar."),
 ("Adakah pahala membaca Al-Quran digital sama dengan mushaf fizikal?",
  "Ya, ganjaran dikira berdasarkan setiap huruf yang dibaca dengan niat ibadah, tanpa mengira medium sama ada mushaf fizikal atau paparan digital. Wallahu a'lam."),
 ("Bolehkah laman ini mengajar tajwid?",
  "Laman ini berfungsi sebagai alat bantu: anda boleh mendengar bacaan qari ayat demi ayat dan mengulanginya. Namun belajar tajwid dan makhraj paling baik secara bertalaqqi dengan guru yang bertauliah."),
]

HUKUM_TITLE = "Hukum Membaca Al-Quran Secara Digital (Mengikut Mazhab Syafi'i)"

def sha(s):
    import base64
    return "sha256-" + base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()

THEME_JS = 'try{var t=localStorage.getItem("ilmq:theme");if(t){t=JSON.parse(t);if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}}catch(e){}'

from cssbuild import build as build_css
css = build_css(f"{SCR}/home.css", f"{REPO}/assets/css/quran.min.css")

graph = {
 "@context": "https://schema.org",
 "@graph": [
  {"@type": "Organization", "@id": MAIN + "#org", "name": "The Ilmu Alam", "url": MAIN,
   "logo": {"@type": "ImageObject", "url": SITE + "assets/icons/icon-512.png", "width": 512, "height": 512},
   "sameAs": ["https://www.facebook.com/ilmualam", "https://twitter.com/ilmualam", "https://www.youtube.com/@theilmualam", "https://ilmualam.bsky.social/"]},
  {"@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": "Al-Quran Online – Ilmu Alam", "inLanguage": "ms-MY", "publisher": {"@id": MAIN + "#org"}},
  {"@type": "WebPage", "@id": SITE + "#webpage", "url": SITE, "name": TITLE, "description": DESC, "inLanguage": "ms-MY",
   "isPartOf": {"@id": SITE + "#website"}, "about": {"@type": "Thing", "name": "Al-Quran"},
   "primaryImageOfPage": {"@type": "ImageObject", "url": OGIMG, "width": 1200, "height": 630},
   "breadcrumb": {"@id": SITE + "#crumbs"}, "datePublished": TODAY, "dateModified": TODAY,
   "mainEntity": {"@id": SITE + "#surah-list"}, "publisher": {"@id": MAIN + "#org"},
   "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".lead", "#utama .box"]}},
  {"@type": "BreadcrumbList", "@id": SITE + "#crumbs", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Ilmu Alam", "item": MAIN},
    {"@type": "ListItem", "position": 2, "name": "Al-Quran Online", "item": SITE}]},
  {"@type": "WebApplication", "@id": SITE + "#app", "name": "Al-Quran Online", "url": SITE, "applicationCategory": "EducationalApplication",
   "operatingSystem": "Any (web browser)", "inLanguage": "ms-MY", "isAccessibleForFree": True,
   "offers": {"@type": "Offer", "price": "0", "priceCurrency": "MYR"}, "publisher": {"@id": MAIN + "#org"},
   "featureList": ["114 surah (30 juzuk)", "Teks Arab, Rumi dan terjemahan Bahasa Melayu", "Audio 5 qari ayat demi ayat", "Tanda ayat dan sambung bacaan", "Mod gelap"]},
  {"@type": "ItemList", "@id": SITE + "#surah-list", "name": "Senarai 114 Surah Al-Quran", "numberOfItems": 114, "itemListOrder": "https://schema.org/ItemListOrderAscending", "itemListElement": items},
  {"@type": "FAQPage", "@id": SITE + "#faq", "inLanguage": "ms-MY",
   "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
 ],
}
JSONLD = json.dumps(graph, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

faq_html = "\n".join(
    f'<details class="q"><summary><h3>{e(q)}</h3></summary><div class="an"><p>{e(a)}</p></div></details>' for q, a in FAQ
)

ICON_LINKS = ('<link rel="icon" href="favicon.ico" sizes="48x48">\n'
              '<link rel="icon" href="assets/icons/favicon-96.png" type="image/png" sizes="96x96">\n'
              '<link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">')

def share_bar(url, text):
    u, t = quote(url, safe=""), quote(text, safe="")
    links = [("wa", "WhatsApp", f"https://wa.me/?text={quote(text + ' ' + url, safe='')}"),
             ("tg", "Telegram", f"https://t.me/share/url?url={u}&amp;text={t}"),
             ("fb", "Facebook", f"https://www.facebook.com/sharer/sharer.php?u={u}"),
             ("x", "X", f"https://x.com/intent/post?text={t}&amp;url={u}")]
    a = "".join(f'<a class="sbtn {k}" href="{h}" target="_blank" rel="noopener nofollow">{n}</a>' for k, n, h in links)
    return (f'<div class="share" role="group" aria-label="Kongsi laman ini"><span class="shl">Kongsi:</span>{a}'
            f'<button class="sbtn cp" type="button" data-share="copy" data-url="{e(url)}">Salin pautan</button>'
            f'<button class="sbtn nt" type="button" data-share="native" data-url="{e(url)}" data-title="{e(text)}" hidden>Lagi…</button></div>')

def ad(i):
    if not ADS_CLIENT or not ADS_SLOTS[i]:
        return ""
    return (f'<aside class="ad" aria-label="Iklan"><span class="adl">Iklan</span><ins class="adsbygoogle" data-ad-client="{e(ADS_CLIENT)}" '
            f'data-ad-slot="{e(ADS_SLOTS[i])}" data-ad-format="auto" data-full-width-responsive="true"></ins></aside>')

ADS_ON = bool(ADS_CLIENT and any(ADS_SLOTS))
if ADS_ON:
    # AdSense loads scripts, frames and pixels from many rotating Google hosts, so the strict policy is relaxed
    csp = (f"default-src 'self'; script-src 'self' '{sha(THEME_JS)}' 'unsafe-inline' 'unsafe-eval' https:; style-src 'unsafe-inline' https:; "
           "img-src 'self' data: https:; font-src 'self' https:; frame-src https:; connect-src 'self' https:; worker-src 'self'; "
           "media-src https://everyayah.com; object-src 'none'; base-uri 'self'; form-action 'none'")
else:
    csp = (f"default-src 'none'; script-src 'self' '{sha(THEME_JS)}'; style-src 'unsafe-inline'; img-src 'self' data:; font-src 'self'; worker-src 'self'; "
           "media-src https://everyayah.com; connect-src 'self'; manifest-src 'self'; base-uri 'self'; form-action 'none'")
ADMETA = f'<meta name="google-adsense-account" content="{e(ADS_CLIENT)}">\n' if ADS_CLIENT else ""
HEADER = open(f"{SCR}/header.html", encoding="utf8").read()
FOOTER = open(f"{SCR}/footer.html", encoding="utf8").read()

def render(tpl, rep):
    for k, v in rep.items():
        tpl = tpl.replace(k, v)
    assert "{{" not in tpl, re.findall(r"\{\{\w+\}\}", tpl)
    return tpl

PAGE = open(f"{SCR}/page.html", encoding="utf8").read()
rep = {
 "{{HEADER}}": HEADER, "{{FOOTER}}": FOOTER, "{{ICONS}}": ICON_LINKS, "{{ADMETA}}": ADMETA,
 "{{SHARE}}": share_bar(SITE, "Baca Al-Quran online percuma – 114 surah, audio & terjemahan Melayu:"),
 "{{AD1}}": ad(0), "{{AD2}}": ad(1), "{{AD3}}": ad(2),
 "{{CSP}}": csp, "{{TITLE}}": e(TITLE), "{{DESC}}": e(DESC), "{{SITE}}": SITE, "{{MAIN}}": MAIN, "{{OGIMG}}": OGIMG,
 "{{CSS}}": css, "{{THEMEJS}}": THEME_JS, "{{JSONLD}}": JSONLD, "{{GRID}}": GRID, "{{POP}}": POP,
 "{{POPIDS}}": ",".join(map(str, POPULAR)), "{{FAQ}}": faq_html, "{{HUKUM}}": e(HUKUM_TITLE), "{{TODAYMS}}": TODAYMS, "{{TODAY}}": TODAY,
}
PAGE = render(PAGE, rep)
open(f"{REPO}/index.html", "w", encoding="utf8", newline="\n").write(PAGE)

PRIV_LD = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "@id": SITE + "dasar-privasi.html", "url": SITE + "dasar-privasi.html",
  "name": "Dasar Privasi, Terma & Penafian – Al-Quran Online", "inLanguage": "ms-MY", "dateModified": TODAY,
  "isPartOf": {"@id": SITE + "#website"}, "publisher": {"@id": MAIN + "#org"}}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
PRIV = render(open(f"{SCR}/privacy.html", encoding="utf8").read(), {
 "{{HEADER}}": HEADER, "{{FOOTER}}": FOOTER, "{{ICONS}}": ICON_LINKS, "{{ADMETA}}": ADMETA, "{{CSP}}": csp, "{{SITE}}": SITE, "{{MAIN}}": MAIN,
 "{{CSS}}": css, "{{THEMEJS}}": THEME_JS, "{{JSONLD}}": PRIV_LD, "{{TODAYMS}}": TODAYMS, "{{TODAY}}": TODAY})
open(f"{REPO}/dasar-privasi.html", "w", encoding="utf8", newline="\n").write(PRIV)

# ---- supporting files ----
BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended"]
robots = f"# robots.txt for {SITE}\n# Everything is public. Search engines and AI answer engines are welcome.\n\nUser-agent: *\nAllow: /\n\n"
robots += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in BOTS) + f"Sitemap: {SITE}sitemap.xml\n"
open(f"{REPO}/robots.txt", "w", newline="\n").write(robots)
open(f"{REPO}/sitemap.xml", "w", newline="\n").write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
 + "".join(f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n" for p in ["", "dasar-privasi.html"])
 + "</urlset>\n")

lines = [f"- [{S[n][1]} ({n}) – {S[n][2]}, {AYAT[n]} ayat]({URLS.get(n, SITE + '#surah-' + str(n))})" for n in range(1, 115)]
open(f"{REPO}/llms.txt", "w", encoding="utf8", newline="\n").write(f"""# Al-Quran Online – Ilmu Alam

> Pembaca Al-Quran online percuma dalam Bahasa Melayu: 114 surah (30 juzuk) dengan teks Arab, bacaan Rumi, terjemahan Bahasa Melayu dan audio murottal daripada 5 qari. Dikendalikan oleh The Ilmu Alam ({MAIN}).

Halaman ini menerangkan hukum membaca Al-Quran secara digital mengikut mazhab Syafi'i (wuduk, haid/nifas, pahala), konteks Malaysia, glosari dan soalan lazim. Ia bukan fatwa; rujuk mufti atau pejabat agama negeri untuk keputusan peribadi.

## Halaman utama
- [{TITLE}]({SITE}): senarai 114 surah, pembaca dalam halaman, FAQ.

## Data
- Teks Arab, Rumi dan terjemahan Melayu setiap surah tersedia dalam /data-surah/surah-N.json (N = 1–114).
- Audio ayat demi ayat: EveryAyah.com (Alafasy, As-Sudais, Al-Husary, Abdul Basit, Al-Ghamadi).

## Senarai surah (artikel penuh di ilmualam.com jika ada)
""" + "\n".join(lines) + "\n")

ICONS = [
 {"src": "assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
 {"src": "assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
 {"src": "assets/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]
SC = [("Surah Yasin", 36), ("Surah Al-Kahfi", 18), ("Surah Al-Mulk", 67), ("Surah Al-Waqi'ah", 56)]
open(f"{REPO}/manifest.webmanifest", "w", encoding="utf8", newline="\n").write(json.dumps({
 "id": "/", "name": "Al-Quran Online – Ilmu Alam", "short_name": "Al-Quran", "description": DESC, "lang": "ms-MY", "dir": "ltr",
 "start_url": "./?utm_source=pwa", "scope": "./", "display": "standalone", "display_override": ["standalone", "minimal-ui"],
 "orientation": "any", "background_color": "#ffffff", "theme_color": "#0c3808", "categories": ["education", "books", "lifestyle"],
 "icons": ICONS,
 "shortcuts": [{"name": n, "short_name": n.replace("Surah ", ""), "url": f"./#surah-{k}", "icons": [ICONS[0]]} for n, k in SC]},
 ensure_ascii=False, indent=2) + "\n")

# ---- Blogger CTA: one script on www.ilmualam.com adds a "read & listen" box to each surah article ----
cta_map = {urlparse(URLS[n]).path: [n, S[n][1], S[n][0], AYAT[n]] for n in URLS}
cta = open(f"{SCR}/surah-cta.js", encoding="utf8").read().replace("{{MAP}}", json.dumps(cta_map, ensure_ascii=False, separators=(",", ":"))).replace("{{SITE}}", SITE)
# pure ASCII (\uXXXX escapes) so the script renders right whatever charset the Blogger theme or CDN declares
cta = "".join(c if ord(c) < 128 else "".join(f"\\u{int.from_bytes(b[i:i + 2], 'big'):04x}" for b in [c.encode("utf-16-be")] for i in range(0, len(b), 2)) for c in cta)
open(f"{REPO}/assets/js/surah-cta.js", "w", encoding="ascii", newline="\n").write(cta)

# service worker: version = hash of everything it precaches, so any deploy busts the old cache
PRE = ["./", "dasar-privasi.html", "assets/js/quran-home.js", "assets/fonts/amiri-arabic-400-normal.woff2", "manifest.webmanifest",
       "favicon.ico", "assets/icons/logo-64.webp", "assets/icons/favicon-96.png", "assets/icons/icon-192.png", "assets/icons/icon-512.png"]
h = hashlib.sha256(PAGE.encode())
for f in PRE[1:]:
    h.update(open(f"{REPO}/{f}", "rb").read())
sw = open(f"{SCR}/sw.js", encoding="utf8").read().replace("{{VER}}", h.hexdigest()[:10]).replace("{{PRE}}", json.dumps(PRE))
open(f"{REPO}/sw.js", "w", encoding="utf8", newline="\n").write(sw)
print("OK", len(PAGE), "bytes; total ayat", sum(AYAT.values()), "| ads", "ON" if ADS_ON else "off", "| surah without article link:", MISSING or "none")
