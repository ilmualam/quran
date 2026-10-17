"""Khatam/hafazan schedule maths. assets/js/alat.js mirrors these functions line for line; tools/test-alat.mjs checks both
produce byte-identical HTML, so the build-time table is exactly what the script would draw (no flash, no layout shift)."""
import json, os, math, datetime as dt
from surahs import S

SCR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SCR)
META = json.load(open(f"{SCR}/qmeta.json", encoding="utf8"))
COUNT = [len(json.load(open(f"{REPO}/data-surah/surah-{i}.json", encoding="utf8"))) for i in range(1, 115)]
NAMES = [S[n][1] for n in range(1, 115)]
OFF = [0]
for c in COUNT:
    OFF.append(OFF[-1] + c)
TOTAL = OFF[-1]
assert TOTAL == 6236


def gid(s, a):
    return OFF[s - 1] + a


def sa(g):
    s = 1
    while OFF[s] < g:
        s += 1
    return s, g - OFF[s - 1]


PS = [gid(*x) for x in META["pages"]] + [TOTAL + 1]   # first ayah of each of the 604 pages, plus sentinel
JS = [gid(*x) for x in META["juz"]] + [TOTAL + 1]
NP = 604
assert len(PS) == NP + 1 and len(JS) == 31


def page_of(g):
    lo, hi = 0, NP - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if PS[m] <= g:
            lo = m
        else:
            hi = m - 1
    return lo + 1


HARI = ["Ahad", "Isnin", "Selasa", "Rabu", "Khamis", "Jumaat", "Sabtu"]
BLN = ["Januari", "Februari", "Mac", "April", "Mei", "Jun", "Julai", "Ogos", "September", "Oktober", "November", "Disember"]
BLS = ["Jan", "Feb", "Mac", "Apr", "Mei", "Jun", "Jul", "Ogo", "Sep", "Okt", "Nov", "Dis"]


def dow(d):
    return (d.weekday() + 1) % 7


def dshort(d):
    return f"{HARI[dow(d)]}, {d.day} {BLS[d.month - 1]}"


def dlong(d):
    return f"{HARI[dow(d)]}, {d.day} {BLN[d.month - 1]} {d.year}"


def r1(x):
    v = math.floor(x * 10 + 0.5) / 10
    return f"{v:.1f}"


def num(n):
    return f"{n:,}"


def ref(g):
    s, a = sa(g)
    return f"{NAMES[s - 1]} {s}:{a}"


# ---------------- khatam ----------------
def khatam(D, r):
    """D days, r pages already read -> list of (g1, g2) ayah ranges and whether juz-aligned."""
    R = NP - r
    D = max(1, min(D, R))
    if r == 0 and 30 % D == 0:
        k = 30 // D
        return [(JS[i * k], JS[(i + 1) * k] - 1) for i in range(D)], True, D
    base, extra, p, out = R // D, R % D, r, []
    for i in range(D):
        n = base + (1 if i < extra else 0)
        out.append((PS[p], PS[p + n] - 1))
        p += n
    return out, False, D


def khatam_html(D, r, start):
    rows, juz, D = khatam(D, r)
    R = NP - r
    trs = []
    for i, (g1, g2) in enumerate(rows):
        p1, p2 = page_of(g1), page_of(g2)
        s, a = sa(g1)
        d = start + dt.timedelta(days=i)
        pg = str(p1) if p1 == p2 else f"{p1}–{p2}"
        trs.append(f'<tr><td>{i + 1}</td><td>{dshort(d)}</td><td>{pg}</td><td><a href="/#surah-{s}-ayat-{a}">{ref(g1)}</a></td>'
                   f'<td>{ref(g2)}</td><td><input type="checkbox" data-d="{i + 1}" aria-label="Hari {i + 1} selesai"></td></tr>')
    if juz:
        per = f"{30 // D} juzuk sehari"
    else:
        b, x = R // D, R % D
        per = f"{b} muka surat sehari" if x == 0 else f"{b}–{b + 1} muka surat sehari"
    end = start + dt.timedelta(days=D - 1)
    left = f" (baki {R} muka surat)" if r else ""
    summ = (f'<p><strong>Baca {per}</strong> untuk khatam dalam {D} hari{left}: purata <strong>{r1(R / D)} muka surat sehari</strong>, '
            f'atau kira-kira {r1(R / D / 5)} muka surat selepas setiap solat fardu.</p><p>Tarikh khatam: <strong>{dlong(end)}</strong></p>')
    return summ, "".join(trs)


# ---------------- hafazan ----------------
def juz_segments(n):
    g1, g2 = JS[n - 1], JS[n] - 1
    segs = []
    while g1 <= g2:
        s, a = sa(g1)
        last = min(g2, OFF[s])
        segs.append((s, a, last - OFF[s - 1]))
        g1 = last + 1
    return segs


def targets():
    t = []
    for n in (30, 29, 28):
        t.append((f"j{n}", {30: "Juz 30 (Juz 'Amma)", 29: "Juz 29 (Tabarak)", 28: "Juz 28 (Qad Sami'a)"}[n], juz_segments(n)))
    for s in (67, 36, 18, 56, 55, 32, 2):
        t.append((f"s{s}", f"Surah {NAMES[s - 1]}", [(s, 1, COUNT[s - 1])]))
    t.append(("all", "Seluruh Al-Quran (30 juzuk)", [(s, 1, COUNT[s - 1]) for s in range(1, 115)]))
    for n in range(1, 28):
        t.append((f"j{n}", f"Juz {n}", juz_segments(n)))
    return t


TARGETS = targets()
TMAP = {k: (lab, segs) for k, lab, segs in TARGETS}
WEEK = {"7": ("7 hari seminggu", [0, 1, 2, 3, 4, 5, 6]), "6j": ("6 hari seminggu (rehat Jumaat)", [0, 1, 2, 3, 4, 6]),
        "6a": ("6 hari seminggu (rehat Ahad)", [1, 2, 3, 4, 5, 6]), "5s": ("Isnin hingga Jumaat", [1, 2, 3, 4, 5]),
        "5j": ("Ahad hingga Khamis", [0, 1, 2, 3, 4])}
MAXROWS = 400


def hafazan(key, order, unit, n, week, start):
    lab, segs = TMAP[key]
    if order == "pendek" and unit == "ayat":
        segs = list(reversed(segs))
    items = []  # list of lists of ayah gids
    for s, a1, a2 in segs:
        for a in range(a1, a2 + 1):
            g = gid(s, a)
            if unit == "page" and items and page_of(items[-1][-1]) == page_of(g) and items[-1][-1] == g - 1:
                items[-1].append(g)
            else:
                items.append([g])
    sessions = [sum(items[i:i + n], []) for i in range(0, len(items), n)]
    days = WEEK[week][1]
    d, dates = start, []
    for _ in sessions:
        while dow(d) not in days:
            d += dt.timedelta(days=1)
        dates.append(d)
        d += dt.timedelta(days=1)
    return lab, sessions, dates, sum(len(x) for x in items)


def label(gs):
    parts, i = [], 0
    while i < len(gs):
        s, a = sa(gs[i])
        j = i
        while j + 1 < len(gs) and gs[j + 1] == gs[j] + 1 and sa(gs[j + 1])[0] == s:
            j += 1
        b = sa(gs[j])[1]
        parts.append(f"{NAMES[s - 1]} {a}" if a == b else f"{NAMES[s - 1]} {a}–{b}")
        i = j + 1
    return ", ".join(parts)


def hafazan_html(key, order, unit, n, week, start):
    lab, sessions, dates, tot = hafazan(key, order, unit, n, week, start)
    trs = []
    for i, gs in enumerate(sessions[:MAXROWS]):
        s, a = sa(gs[0])
        trs.append(f'<tr><td>{i + 1}</td><td>{dshort(dates[i])}</td><td><a href="/#surah-{s}-ayat-{a}">{label(gs)}</a></td><td>{len(gs)}</td></tr>')
    if len(sessions) > MAXROWS:
        trs.append(f'<tr><td colspan="4">… dan {num(len(sessions) - MAXROWS)} sesi lagi. Cetak atau salin pautan untuk simpan rancangan ini.</td></tr>')
    end = dates[-1]
    weeks = math.ceil(((end - start).days + 1) / 7)
    u = "ayat" if unit == "ayat" else "muka surat"
    summ = (f'<p><strong>{lab}</strong> ({num(tot)} ayat) pada kadar {n} {u} sehari, {WEEK[week][0]}: '
            f'<strong>{num(len(sessions))} sesi hafazan</strong>, dijangka tamat pada <strong>{dlong(end)}</strong> (kira-kira {weeks} minggu).</p>')
    return summ, "".join(trs)


def jsdata():
    """Compact data block shared by the tool scripts."""
    return json.dumps({"n": NAMES, "c": COUNT, "p": PS[:-1], "j": JS[:-1],
                       "t": [[k, lab, segs] for k, lab, segs in TARGETS], "w": {k: v for k, v in WEEK.items()}, "m": MAXROWS},
                      ensure_ascii=False, separators=(",", ":"))
