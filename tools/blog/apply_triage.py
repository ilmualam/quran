"""Apply the approved triage (out/triage.json) to Blogger: merge stubs, unpublish (revert to draft), the khusyuk merge, and
republish the 4 expanded batch 1 posts plus the hutang puasa / ruqyah link updates. Every post is backed up to backup/<id>.json
before it is touched, unless a backup already exists (the original is kept, never overwritten).
Run from the repo root: python3 tools/blog/apply_triage.py [--dry]"""
import json, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://www.googleapis.com/blogger/v3"
B = open(f"{HERE}/.blogid").read().strip()
DRY = "--dry" in sys.argv
sys.path.insert(0, HERE)
from batch2 import merge_stub  # noqa: E402

KHUSYUK_OLD = "https://www.ilmualam.com/2018/01/rahsia-mendapat-nikmat-khusyuk-dalam.html"
KHUSYUK_NEW = "https://www.ilmualam.com/2017/12/cara-khusyuk-dalam-solat.html"
REPUBLISH = ["mandi-wajib", "masa-nifas", "batal-puasa", "solat-gerhana", "hutang-puasa", "ruqyah"]


def call(u, data=None, method="GET"):
    h = {"Authorization": "Bearer proxy-injected"}
    if data is not None:
        h["Content-Type"] = "application/json"
    with urllib.request.urlopen(urllib.request.Request(u, data=data, method=method, headers=h), timeout=90) as r:
        body = r.read()
        return json.loads(body) if body else {}


def by_url(url):
    return call(f"{API}/blogs/{B}/posts/bypath?path={urllib.parse.quote(urllib.parse.urlparse(url).path)}&view=ADMIN")


def backup(p):
    f = f"{HERE}/backup/{p['id']}.json"
    if not os.path.exists(f):
        json.dump(p, open(f, "w"), ensure_ascii=False, indent=1)


def patch(pid, body):
    return {} if DRY else call(f"{API}/blogs/{B}/posts/{pid}", json.dumps(body).encode(), "PATCH")


def main():
    T = json.load(open(f"{HERE}/out/triage.json"))
    log = []
    merges = [(r["url"], r["target"], r["target_title"]) for r in T["rows"] if r["action"] == "MERGE"]
    khusyuk_title = "Khusyuk Dalam Solat Itu Rezeki, 13 Cara Ini Buat Otak Fokus"
    merges.append((KHUSYUK_OLD, KHUSYUK_NEW, khusyuk_title))
    for old, target, title in merges:
        p = by_url(old); backup(p)
        patch(p["id"], {"content": merge_stub(target, title)})
        log.append(["merge", old, target]); print("merge    ", old.rsplit("/", 1)[1][:45], "->", target.rsplit("/", 1)[1][:40])
    for r in T["rows"]:
        if r["action"] != "UNPUBLISH":
            continue
        p = by_url(r["url"]); backup(p)
        if not DRY:
            call(f"{API}/blogs/{B}/posts/{p['id']}/revert", b"", "POST")
        log.append(["unpublish", r["url"], None]); print("unpublish", r["url"].rsplit("/", 1)[1][:45])
    for slug in REPUBLISH:
        m = json.load(open(f"{HERE}/out/{slug}.json")); html = open(f"{HERE}/out/{slug}.html").read()
        p = by_url(m["url"]); backup(p)
        patch(p["id"], {"content": html})
        log.append(["update", m["url"], None]); print("update   ", slug)
    json.dump(log, open(f"{HERE}/out/triage-applied.json", "w"), ensure_ascii=False, indent=1)
    print("done:", {k: sum(1 for x in log if x[0] == k) for k in ("merge", "unpublish", "update")})


if __name__ == "__main__":
    main()
