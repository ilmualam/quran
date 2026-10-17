"""Fetches the official JAKIM prayer timetable for every zone used in tools/solat.py and writes
assets/data/solat/<ZONE>-<YEAR>.json. Runs in GitHub Actions (.github/workflows/solat-data.yml).
Source 1: www.e-solat.gov.my (JAKIM). Source 2: api.waktusolat.app (open mirror of JAKIM data).
A zone file is written only when a full year passes validation; otherwise the site falls back to calculation."""
import json, os, sys, time, datetime as dt, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solat import CITIES

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{REPO}/assets/data/solat"
UA = {"User-Agent": "Mozilla/5.0 (quran.ilmualam.com timetable sync; +https://quran.ilmualam.com/waktu-solat/)"}
KEYS = ["imsak", "fajr", "syuruk", "dhuhr", "asr", "maghrib", "isha"]
MON = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
MON.update({"mei": 5, "ogo": 8, "okt": 10, "dis": 12})


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))


def mins(v):
    if isinstance(v, (int, float)):  # unix seconds
        t = dt.datetime.fromtimestamp(v, dt.timezone(dt.timedelta(hours=8)))
        return t.hour * 60 + t.minute
    h, m = str(v).split(":")[:2]
    return int(h) * 60 + int(m)


def esolat(zone, year):
    d = get(f"https://www.e-solat.gov.my/index.php?r=esolatApi/TakwimSolat&period=year&zone={zone}")
    out = {}
    for p in d.get("prayerTime") or []:
        dd, mm, yy = p["date"].split("-")
        day = dt.date(int(yy), MON[mm.lower()[:3]], int(dd))
        if day.year != year:
            continue
        fajr = mins(p["fajr"])
        out[day] = ([mins(p["imsak"]) if p.get("imsak") else fajr - 10] + [mins(p[k]) for k in KEYS[1:]], p.get("hijri", ""))
    return out


def waktusolat(zone, year):
    out = {}
    for m in range(1, 13):
        d = get(f"https://api.waktusolat.app/v2/solat/{zone}?year={year}&month={m}")
        for p in d.get("prayers") or []:
            day = dt.date(year, m, int(p["day"]))
            fajr = mins(p["fajr"])
            out[day] = ([mins(p["imsak"]) if p.get("imsak") else fajr - 10] + [mins(p[k]) for k in KEYS[1:]], p.get("hijri", ""))
        time.sleep(0.3)
    return out


def valid(days, year):
    n = (dt.date(year, 12, 31) - dt.date(year, 1, 1)).days + 1
    if len(days) != n:
        return False
    for t, _ in days.values():
        if not (240 <= t[1] <= 400 and t[0] < t[1] < t[2] < t[3] < t[4] < t[5] < t[6] <= 1320):
            return False
    return True


def main():
    years = [int(a) for a in sys.argv[1:]] or [dt.date.today().year]
    os.makedirs(OUT, exist_ok=True)
    zones = sorted({c[5] for c in CITIES if c[5]})
    ok, bad = [], []
    for year in years:
        for z in zones:
            days, src = None, None
            for name, fn in (("JAKIM e-solat", esolat), ("waktusolat.app (JAKIM)", waktusolat)):
                try:
                    got = fn(z, year)
                    if valid(got, year):
                        days, src = got, name
                        break
                    print(f"{z} {year}: {name} returned {len(got)} days, failed validation")
                except Exception as e:  # network / format change: try the next source
                    print(f"{z} {year}: {name} error {e!r}")
            if not days:
                bad.append(f"{z}-{year}")
                continue
            keys = sorted(days)
            json.dump({"z": z, "y": year, "src": src, "fetched": dt.date.today().isoformat(),
                       "t": [days[k][0] for k in keys], "h": [days[k][1] for k in keys]},
                      open(f"{OUT}/{z}-{year}.json", "w"), separators=(",", ":"))
            ok.append(f"{z}-{year}")
            time.sleep(0.5)
    print("written:", len(ok), "| failed:", bad or "none")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
