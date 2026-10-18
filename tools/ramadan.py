"""Ramadan dates and the fasting timetable (imsak / berbuka) used by /waktu-berbuka-puasa/ and its state pages.
Dates: the expected 1 Ramadan in Malaysia (imkanur rukyah, MABIMS 3° altitude / 6.4° elongation, checked against the
conjunction) until JAKIM's own takwim is synced; then the Hijri column of the official timetable decides (official=True).
The official start is still announced by the Penyimpan Mohor Besar Raja-Raja after rukyah, so pages say so.
Times: the official JAKIM zone timetable when assets/data/solat/<ZONE>-<YEAR>.json exists, otherwise the calibrated
calculation in solat.py (assets/js/alat.js mirrors both)."""
import json, os, datetime as dt
import solat as SL

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# (hijri year, expected 1 Ramadan, expected length). 1448: conjunction 6 Feb 2027 23:57 MYT, crescent visible on the 7th;
# conjunction 8 Mar 2027 17:31 MYT is too late for the 29th, so 30 days and Aidilfitri on 10 Mar 2027.
EXPECTED = [(1448, dt.date(2027, 2, 8), 30), (1449, dt.date(2028, 1, 28), 30)]
REF_ZONES = ["WLY01"] + [z[0] for z in SL.ZONES]  # the Hijri column is national, so any synced zone will do
_F = {}


def official(zone, year):
    k = (zone, year)
    if k not in _F:
        p = f"{REPO}/assets/data/solat/{zone}-{year}.json"
        _F[k] = json.load(open(p)) if os.path.exists(p) else None
    return _F[k]


def season(today):
    """The Ramadan to show on `today`: the first one that has not ended yet (else the last one).
    Returns dict(y, start, n, official)."""
    for y, start, n in EXPECTED:
        days = []
        for yr in (start.year - 1, start.year, start.year + 1):
            d = next((o for o in (official(z, yr) for z in REF_ZONES) if o and o.get("h")), None)
            if d and d.get("h"):
                days += [dt.date(yr, 1, 1) + dt.timedelta(i) for i, h in enumerate(d["h"]) if h.startswith(f"{y}-09-")]
        ok = 29 <= len(days) <= 30 and all((b - a).days == 1 for a, b in zip(days, days[1:]))
        s = dict(y=y, start=days[0], n=len(days), official=True) if ok else dict(y=y, start=start, n=n, official=False)
        if s["start"] + dt.timedelta(s["n"]) > today:
            return s
    return s


def zone_coords(code):
    z = next(z for z in SL.ZONES if z[0] == code)
    return z[3], z[4]


def day_times(zone, d):
    """([imsak, subuh, syuruk, zohor, asar, maghrib, isyak] minutes, official?) for one zone and date."""
    o = official(zone, d.year)
    if o:
        return o["t"][(d - dt.date(d.year, 1, 1)).days], True
    lat, lng = zone_coords(zone)
    return SL.solat_day(d.year, d.month, d.day, lat, lng), False


def timetable(zone, s):
    """[(ramadan day, date, times)] plus whether every day came from the official timetable."""
    rows, allo = [], True
    for i in range(s["n"]):
        d = s["start"] + dt.timedelta(i)
        t, o = day_times(zone, d)
        rows.append((i + 1, d, t))
        allo = allo and o
    return rows, allo


def dur(t):
    m = t[5] - t[1]
    return f"{m // 60}j {m % 60:02d}m"
