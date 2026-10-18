"""Fetches every muslim place of worship in Malaysia from OpenStreetMap (Overpass API), one query per state, assigns each
to a JAKIM zone (tools/masjid.py) and writes assets/data/masjid/<ZONE>.json. Runs in GitHub Actions
(.github/workflows/masjid-data.yml). Data © OpenStreetMap contributors, ODbL 1.0: the files keep that notice.
A zone file is replaced only when its state answered completely and the count did not collapse; otherwise the old file stays."""
import json, os, sys, time, datetime as dt, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import masjid as M

ENDPOINTS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter"]
UA = {"User-Agent": "quran.ilmualam.com masjid finder (monthly, 16 queries; +https://quran.ilmualam.com/cari-masjid/)"}
PER_TOWN = 15
MIN_ZONE = 6  # fewer named places than this: also list the nearest ones just outside the zone
NEAR_KM = 30


def overpass(q):
    err = None
    for url in ENDPOINTS:
        for attempt in range(2):
            try:
                req = urllib.request.Request(url, data=urllib.parse.urlencode({"data": q}).encode(), headers=UA)
                with urllib.request.urlopen(req, timeout=240) as r:
                    d = json.loads(r.read().decode("utf-8"))
                if "runtime error" in (d.get("remark") or ""):  # timeout / memory: the answer is partial
                    raise RuntimeError(d["remark"][:200])
                return d.get("elements") or []
            except Exception as e:
                err = e
                print(f"  {url} attempt {attempt + 1}: {e!r}")
                time.sleep(20 * (attempt + 1))
    raise RuntimeError(f"all Overpass endpoints failed: {err!r}")


SELECT = '(nwr["amenity"="place_of_worship"]["religion"="muslim"]{f};nwr["building"="mosque"]{f};);out center tags qt;'


def q_area(codes):
    rx = "|".join(codes)
    return f'[out:json][timeout:200];area["ISO3166-2"~"^({rx})$"]["boundary"="administrative"]->.a;' + SELECT.format(f="(area.a)")


def q_bbox(state):
    pts = [(a[2], a[3]) for a in M.anchors(state)]
    s, w = min(p[0] for p in pts) - .4, min(p[1] for p in pts) - .4
    n, e = max(p[0] for p in pts) + .4, max(p[1] for p in pts) + .4
    return "[out:json][timeout:200];" + SELECT.format(f=f"({s:.3f},{w:.3f},{n:.3f},{e:.3f})")


def clean(s):
    return " ".join(str(s or "").split())


def record(el):
    t = el.get("tags") or {}
    lat, lng = (el.get("lat"), el.get("lon")) if el["type"] == "node" else ((el.get("center") or {}).get("lat"), (el.get("center") or {}).get("lon"))
    name = clean(t.get("name") or t.get("name:ms") or t.get("name:en"))
    if lat is None or not name:
        return None  # unnamed places can't be listed usefully
    addr = ", ".join(x for x in [clean(" ".join(filter(None, [t.get("addr:housenumber"), t.get("addr:street")]))),
                                 clean(t.get("addr:place") or t.get("addr:suburb")),
                                 clean(" ".join(filter(None, [t.get("addr:postcode"), t.get("addr:city")])))] if x)
    extra = {}
    web = clean(t.get("website") or t.get("contact:website"))
    if web.startswith(("http://", "https://")):
        extra["w"] = web
    tel = clean(t.get("phone") or t.get("contact:phone")).split(";")[0].strip()
    if tel:
        extra["p"] = tel
    if t.get("wheelchair") == "yes":
        extra["a"] = 1
    return [name, M.kind(name, t), round(lat, 6), round(lng, 6), addr, el["type"][0] + str(el["id"]), extra]


def dedupe(recs):
    """The same mosque is often mapped twice (a node and the building outline): keep the richer one."""
    out = []
    for r in sorted(recs, key=lambda r: (-len(r[4]) - len(r[6]), r[5])):
        if not any(o[0].lower() == r[0].lower() and M.km(o[2], o[3], r[2], r[3]) < .15 for o in out):
            out.append(r)
    return out


def fetch_state(state):
    els, how = overpass(q_area(M.ISO[state])), "area"
    if not els:  # state boundary not found as an area: bounding box, keeping only places nearest to this state's towns
        els, how = overpass(q_bbox(state)), "bbox"
    recs = dedupe([r for r in map(record, els) if r])
    if how == "bbox":
        allz = [(z, a[1], a[2]) for z, (_, aa) in M.ZONEINFO.items() for a in aa]
        recs = [r for r in recs if M.STATE_OF[min(allz, key=lambda a: M.km(r[2], r[3], a[1], a[2]))[0]] == state]
    if not recs:  # every state has hundreds of mapped mosques: an empty answer is a failed query, not an empty state
        raise RuntimeError("no named places returned")
    return recs, how


def zone_files(state, recs, fetched, how):
    by = {z: [] for z in M.ZONEINFO if M.STATE_OF[z] == state}
    for r in recs:
        hit = M.nearest(state, r[2], r[3])
        if hit:
            by[hit[0]].append((hit[1], r))
    out = {}
    for z, items in by.items():
        towns = []
        for t, la, ln, *_ in M.ZONEINFO[z][1]:
            mine = sorted((r for tt, r in items if tt == t), key=lambda r: (M.km(la, ln, r[2], r[3]), r[0]))
            towns.append({"t": t, "n": len(mine), "m": mine[:PER_TOWN]})
        near = []
        if len(items) < MIN_ZONE:
            _, la, ln, *_ = M.ZONEINFO[z][1][0]
            own = {r[5] for _, r in items}
            cand = sorted((M.km(la, ln, r[2], r[3]), r) for r in recs if r[5] not in own)
            for d, r in cand[:8]:
                if d <= NEAR_KM:
                    near.append(r + [(M.nearest(state, r[2], r[3]) or (z,))[0]])
        cnt = {k: sum(1 for _, r in items if r[1] == k) for k in "mst"}
        out[z] = {"z": z, "fetched": fetched, "src": "OpenStreetMap (Overpass API)", "q": how, "licence": M.LICENCE,
                  "n": cnt, "towns": towns, "near": near}
    return out


def main():
    os.makedirs(M.DATA, exist_ok=True)
    fetched = dt.date.today().isoformat()
    got, kept = {}, []
    for state in M.ISO:
        try:
            got[state] = fetch_state(state)
        except Exception as e:
            print(f"{state}: {e!r}; keeping existing files")
            kept.append(state)
        time.sleep(10)  # Overpass etiquette: one heavy query at a time
    # a place returned for two states (an enclave like Kuala Lumpur inside Selangor's outline) goes to the state of its nearest town
    seen = {}
    for state, (recs, _) in got.items():
        for r in recs:
            hit = M.nearest(state, r[2], r[3])
            if hit and (r[5] not in seen or hit[2] < seen[r[5]][1]):
                seen[r[5]] = (state, hit[2])
    ok = []
    for state, (recs, how) in got.items():
        recs = [r for r in recs if seen.get(r[5], (state,))[0] == state]
        files = zone_files(state, recs, fetched, how)
        for z, d in files.items():
            new, old = sum(d["n"].values()), M.load(z)
            was = sum(old["n"].values()) if old else 0
            if was >= 20 and new < was * .5:  # a collapse is far likelier to be a bad answer than half the mosques vanishing
                print(f"{z}: {new} places vs {was} last time; keeping the old file")
                kept.append(z)
                continue
            json.dump(d, open(f"{M.DATA}/{z}.json", "w", encoding="utf8", newline="\n"), ensure_ascii=False, separators=(",", ":"))
            ok.append(z)
        print(f"{state}: {len(recs)} named places ({how}) ->", ", ".join(f"{z} {sum(d['n'].values())}" for z, d in files.items()))
    print("written:", len(ok), "| kept:", kept or "none")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
