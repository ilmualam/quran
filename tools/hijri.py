"""Hijri calendar for /kalendar-hijrah/ and /tahlil-ringkas/. Official dates come from the Hijri column of JAKIM's
timetable (assets/data/solat/<ZONE>-<YEAR>.json, synced from e-solat.gov.my). Outside the synced range the
arithmetical (tabular) Islamic calendar is used, shifted by the offset it most often has against JAKIM, and every
such date is labelled an estimate. assets/js/alat.js mirrors this file (g2h, h2g, events, month grid) exactly."""
import datetime as dt, json, math, os, collections
import solat as SL

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPOCH = dt.date(1970, 1, 1)
HE = -492148  # tabular epoch (1 Muharram 1 H, Julian 16 July 622) as days since 1970-01-01
BH = ["Muharam", "Safar", "Rabiulawal", "Rabiulakhir", "Jamadilawal", "Jamadilakhir", "Rejab", "Syaaban", "Ramadan", "Syawal", "Zulkaedah", "Zulhijjah"]
BH_AR = ["مُحَرَّم", "صَفَر", "رَبِيعُ الأَوَّل", "رَبِيعُ الآخِر", "جُمَادَى الأُولَى", "جُمَادَى الآخِرَة", "رَجَب", "شَعْبَان", "رَمَضَان", "شَوَّال", "ذُو القَعْدَة", "ذُو الحِجَّة"]
# (key, hijri month, day, name, note); "cuti" = federal public holiday
EVENTS = [
    ("maal-hijrah", 1, 1, "Awal Muharam (Maal Hijrah)", "Tahun baru Hijrah · cuti umum"),
    ("asyura", 1, 10, "Hari Asyura", "Sunat berpuasa 9 dan 10 Muharam"),
    ("maulid", 3, 12, "Maulidur Rasul", "Keputeraan Nabi Muhammad SAW · cuti umum"),
    ("israk", 7, 27, "Israk dan Mikraj", "Cuti di beberapa negeri"),
    ("nisfu", 8, 15, "Nisfu Syaaban", "Pertengahan Syaaban"),
    ("ramadan", 9, 1, "Awal Ramadan", "Mula puasa · tertakluk pengisytiharan Penyimpan Mohor Besar Raja-Raja"),
    ("nuzul", 9, 17, "Nuzul Al-Quran", "Cuti di kebanyakan negeri"),
    ("aidilfitri", 10, 1, "Hari Raya Aidilfitri", "Cuti umum · haram berpuasa · tertakluk pengisytiharan"),
    ("arafah", 12, 9, "Hari Arafah", "Sunat berpuasa bagi yang tidak berhaji"),
    ("aidiladha", 12, 10, "Hari Raya Aidiladha", "Cuti umum · haram berpuasa"),
]


def dn(d):
    return (d - EPOCH).days


def dd(n):
    return EPOCH + dt.timedelta(n)


def tab_h2d(y, m, d):
    return d + math.ceil(29.5 * (m - 1)) + (y - 1) * 354 + (3 + 11 * y) // 30 + HE - 1


def tab_d2h(n):
    y = (30 * (n - HE) + 10646) // 10631
    m = min(12, math.ceil((n - (29 + tab_h2d(y, 1, 1))) / 29.5) + 1)
    return y, m, n - tab_h2d(y, m, 1) + 1


def _official_days():
    """{day number: (hy, hm, hd)} from every synced year (the Hijri column is national, so any zone with it will do)."""
    out, years, d = {}, set(), f"{REPO}/assets/data/solat"
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if len(f) != 15 or f[5] != "-" or not f.endswith(".json"):  # <ZONE>-<YEAR>.json
            continue
        yr = int(f[6:10])
        if yr in years:
            continue
        o = json.load(open(f"{d}/{f}"))
        if not o.get("h") or not all(o["h"]):
            continue
        years.add(yr)
        for i, h in enumerate(o["h"]):
            out[dn(dt.date(yr, 1, 1)) + i] = tuple(map(int, h.split("-")))
    return out


def build_table():
    """Official months [(hy, hm, start day number, length, full?)] + the tabular offset that best matches them.
    A month cut by the edge of the synced data still counts: its start follows from any of its days (day n is hd - 1 days
    after the 1st). Its length is known when the next month's 1st is synced (full); otherwise only the synced days are."""
    days = _official_days()
    by = {}
    for n, (hy, hm, hd) in days.items():
        s = n - hd + 1
        k = by.setdefault((hy, hm), [s, n])
        k[1] = max(k[1], n)
    months = []
    for (hy, hm), (s, last) in sorted(by.items(), key=lambda x: x[1][0]):
        nxt = (hy + 1, 1) if hm == 12 else (hy, hm + 1)
        if nxt in by and by[nxt][0] - s in (29, 30):
            months.append((hy, hm, s, by[nxt][0] - s, True))
        else:
            months.append((hy, hm, s, last - s + 1, False))
    diffs = collections.Counter(n - tab_h2d(*h) for n, h in days.items())
    off = diffs.most_common(1)[0][0] if diffs else 0
    return months, off


MONTHS, OFF = build_table()


def g2h(d):
    """date -> (hy, hm, hd, official?)"""
    n = dn(d)
    for hy, hm, s, ln, _ in MONTHS:
        if s <= n < s + ln:
            return hy, hm, n - s + 1, True
    return tab_d2h(n - OFF) + (False,)


def month_len(hy, hm):
    ny, nm = (hy + 1, 1) if hm == 12 else (hy, hm + 1)
    tab = tab_h2d(ny, nm, 1) - tab_h2d(hy, hm, 1)
    for y, m, s, ln, full in MONTHS:
        if (y, m) == (hy, hm):
            return (ln, True) if full else (max(ln, tab), False)
    return tab, False


def h2g(hy, hm, hd):
    """(hy, hm, hd) -> (date, official?)"""
    for y, m, s, ln, full in MONTHS:
        if (y, m) == (hy, hm):
            return dd(s + hd - 1), full or hd <= ln
    return dd(tab_h2d(hy, hm, hd) + OFF), False


def hstr(h):
    return f"{h[2]} {BH[h[1] - 1]} {h[0]} H"


def events_from(d, n=12):
    """The next n Islamic events on or after date d: [(key, name, note, hijri tuple, date, official?)]."""
    hy = g2h(d)[0]
    out = []
    for y in (hy, hy + 1, hy + 2):
        for k, m, day, name, note in EVENTS:
            g, o = h2g(y, m, day)
            if g >= d:
                out.append((k, name, note, (y, m, day), g, o))
    return sorted(out, key=lambda x: x[4])[:n]


def marks(d):
    """Calendar markers for one day: 'h' haram to fast, 'r' Ramadan, 'a' strong sunat (Arafah, Tasu'a/Asyura, Ayyamul Bidh),
    's' Syawal six-day window, 'w' Monday/Thursday, 'e' an event; same rules as alat.js marks()."""
    hy, hm, hd, _ = g2h(d)
    m = []
    if (hm == 10 and hd == 1) or (hm == 12 and 10 <= hd <= 13):
        m.append("h")
    elif hm == 9:
        m.append("r")
    elif (hm == 12 and hd == 9) or (hm == 1 and hd in (9, 10)) or hd in (13, 14, 15):
        m.append("a")
    elif hm == 10 and hd >= 2:
        m.append("s")
    if d.weekday() in (0, 3) and "h" not in m and "r" not in m:
        m.append("w")
    if any((hm, hd) == (em, ed) for _, em, ed, _, _ in EVENTS):
        m.append("e")
    return m


HARI = ["Isn", "Sel", "Rab", "Kha", "Jum", "Sab", "Ahd"]


def grid_html(y, mo, today):
    """Month grid, Sunday first; assets/js/alat.js gridHtml() must produce the same string."""
    first = dt.date(y, mo, 1)
    nd = (dt.date(y + mo // 12, mo % 12 + 1, 1) - first).days
    lead = (first.weekday() + 1) % 7
    cells = ['<span class="hc x"></span>'] * lead
    for k in range(1, nd + 1):
        d = dt.date(y, mo, k)
        hy, hm, hd, o = g2h(d)
        mk = marks(d)
        cls = " ".join(["hc"] + [f"m{x}" for x in mk] + (["td"] if d == today else []))
        lab = f'<span class="hm">{BH[hm - 1]}</span>' if hd == 1 or k == 1 else ""
        cells.append(f'<span class="{cls}" data-d="{d.isoformat()}"><b>{k}</b><i>{hd}{"" if o else "*"}</i>{lab}</span>')
    head = "".join(f"<span class=\"hw\">{x}</span>" for x in ["Ahd", "Isn", "Sel", "Rab", "Kha", "Jum", "Sab"])
    return head + "".join(cells)


def js_data():
    return {"m": [[a, b, c, d, int(f)] for a, b, c, d, f in MONTHS], "off": OFF, "bh": BH, "ev": [[k, m, d, n, t] for k, m, d, n, t in EVENTS]}


if __name__ == "__main__":
    print(len(MONTHS), "official months", MONTHS[0], "->", MONTHS[-1], "| tabular offset", OFF)
    for d in (dt.date(2026, 10, 19), dt.date(2027, 2, 8), dt.date(2030, 1, 1), dt.date(1990, 5, 1)):
        print(d, g2h(d))
    for e in events_from(dt.date(2026, 10, 19), 6):
        print(e)
