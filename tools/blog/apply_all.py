"""Publish every refreshed post in out/ (pilot and batches 1-4) to Blogger in one run: back up each post (never overwriting an
existing backup), PATCH title and body, then log. Re-running is safe: it re-sends the current build.
Run from the repo root: PYTHONPATH=tools python3 tools/blog/apply_all.py [--dry] [slug ...]"""
import glob, json, os, sys, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_triage as A


def posts(only):
    for f in sorted(glob.glob(f"{A.HERE}/out/*.json")):
        m = json.load(open(f))
        slug = os.path.basename(f)[:-5]
        if isinstance(m, dict) and {"url", "title", "desc"} <= m.keys() and (not only or slug in only):
            yield slug, m


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    log = []
    for slug, m in posts(only):
        html = open(f"{A.HERE}/out/{slug}.html").read()
        try:
            p = A.by_url(m["url"])
        except urllib.error.HTTPError as ex:
            if ex.code != 404:
                raise
            print("skip (not on Blogger yet; new posts go through apply_new.py)", slug); continue
        A.backup(p)
        r = A.patch(p["id"], {"title": m["title"], "content": html})
        ok = A.DRY or r.get("title") == m["title"]
        log.append([slug, m["url"], p["id"], ok]); print("update" if ok else "FAILED", slug)
    json.dump(log, open(f"{A.HERE}/out/all-applied.json", "w"), ensure_ascii=False, indent=1)
    print("done:", sum(1 for x in log if x[3]), "of", len(log))


if __name__ == "__main__":
    main()
