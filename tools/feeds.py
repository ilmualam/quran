"""RSS 2.0 feeds for Pinterest auto-publishing (one feed per board) and one combined feed for Flipboard and other readers.
Each item links to the page's canonical URL and carries a 1000x1500 pin image (og.pin). pubDate is the page's first
publication date, so a rebuild never makes old pages look new. Near-duplicate zone/state pages are left out on purpose:
pinning 60 masjid zones or 15 state timetables would look like spam to Pinterest."""
import html, datetime as dt
import og

BOARDS = {
    "nama-bayi": ("Nama Bayi Islam", "Nama bayi Islam lelaki dan perempuan dengan maksud dan tulisan Arab, ikut huruf A–Z."),
    "quran-doa": ("Al-Quran, Doa & Zikir", "Surah pilihan, doa harian, zikir dan Asmaul Husna dengan teks Arab, rumi dan maksud."),
    "surah": ("Surah Al-Quran: Arab, Rumi & Terjemahan", "Bacaan penuh 114 surah Al-Quran dalam tulisan Arab, Rumi dan terjemahan Bahasa Melayu."),
    "kisah-nabi": ("Kisah 25 Nabi", "Kisah 25 nabi dan rasul daripada Al-Quran dengan ayat rujukan."),
    "panduan-ibadah": ("Panduan Ibadah & Kalkulator Islam", "Cara solat, solat sunat, zakat, faraid, kalendar Hijrah dan alat Al-Quran percuma."),
}
KICKER = {"surah": "Surah Al-Quran", "nama-bayi": "Nama Bayi Islam", "quran-doa": "Al-Quran & Doa", "kisah-nabi": "Kisah Nabi", "panduan-ibadah": "Panduan Ibadah"}
QURAN_DOA = ("ayat-kursi", "amanar-rasul", "doa-", "zikir-", "tahlil-", "tahiyat-", "asmaul-husna")
DEEP_SKIP = ("waktu-solat/", "waktu-berbuka-puasa/", "cari-masjid/", "zakat-fitrah/")


def board(pg):
    p = pg["path"]
    if pg.get("noindex") or pg["kind"] == "info" or not p:
        return None
    if any(p.startswith(d) and p != d for d in DEEP_SKIP):
        return None
    if "/maksud-nama-" in p:  # 500 name-meaning pages would flood the board; the hub and letter pages carry it
        return None
    if p.startswith("nama-bayi-islam/"):
        return "nama-bayi"
    if p.startswith("kisah-nabi/"):
        return "kisah-nabi"
    if p.startswith("surah-"):
        return "surah"
    if p.startswith(QURAN_DOA):
        return "quran-doa"
    return "panduan-ibadah"


def _rfc822(d):
    return dt.datetime.strptime(d, "%Y-%m-%d").replace(hour=8, tzinfo=dt.timezone(dt.timedelta(hours=8))).strftime("%a, %d %b %Y %H:%M:%S +0800")


def _rss(site, slug, title, desc, items, today):
    x = lambda s: html.escape(str(s), quote=False)
    body = "".join(
        f"<item><title>{x(t)}</title><link>{x(u)}</link><guid isPermaLink=\"true\">{x(u)}</guid><pubDate>{_rfc822(d)}</pubDate>"
        f"<description>{x(ds)}</description><enclosure url=\"{x(img)}\" length=\"{ln}\" type=\"image/jpeg\"/>"
        f"<media:content url=\"{x(img)}\" medium=\"image\" type=\"image/jpeg\"/></item>\n"
        for t, u, d, ds, img, ln in items)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">\n'
            f"<channel><title>{x(title)}</title><link>{site}</link><description>{x(desc)}</description><language>ms-MY</language>"
            f'<lastBuildDate>{_rfc822(max([today] + [i[2] for i in items]))}</lastBuildDate><atom:link href="{site}{slug}" rel="self" type="application/rss+xml"/>\n{body}</channel></rss>\n')


def build(pages, site, repo, today, published_default):
    import os
    by = {k: [] for k in BOARDS}
    for pg in pages:
        b = board(pg)
        if not b:
            continue
        name = pg["path"].strip("/").replace("/", "--") or "home"
        img = og.pin(name, KICKER[b], pg["ogtitle"], pg["desc"])
        if not img:
            continue
        d = pg.get("published", published_default)
        by[b].append((pg["ogtitle"], site + pg["path"], d, pg["desc"], site + img, os.path.getsize(f"{repo}/{img}")))
    os.makedirs(f"{repo}/feed", exist_ok=True)
    allitems = []
    for b, items in by.items():
        items.sort(key=lambda i: (i[2], i[0]), reverse=True)
        allitems += items
        t, ds = BOARDS[b]
        open(f"{repo}/feed/{b}.xml", "w", encoding="utf8", newline="\n").write(_rss(site, f"feed/{b}.xml", f"{t} – Ilmu Alam", ds, items, today))
    allitems.sort(key=lambda i: (i[2], i[0]), reverse=True)
    open(f"{repo}/feed.xml", "w", encoding="utf8", newline="\n").write(
        _rss(site, "feed.xml", "Al-Quran Online – Ilmu Alam", "Alat dan panduan Islam percuma dalam Bahasa Melayu.", allitems, today))
    return {b: len(i) for b, i in by.items()}
