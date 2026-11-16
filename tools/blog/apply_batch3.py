"""Publish batch 3 to Blogger: back up each post (never overwriting an existing backup), then PATCH title and body.
Run from the repo root: python3 tools/blog/apply_batch3.py [--dry]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_triage as A
from batch3 import POSTS

def main():
    log = []
    for slug, _ in POSTS:
        m = json.load(open(f"{A.HERE}/out/{slug}.json")); html = open(f"{A.HERE}/out/{slug}.html").read()
        p = A.by_url(m["url"]); A.backup(p)
        r = A.patch(p["id"], {"title": m["title"], "content": html})
        ok = A.DRY or (r.get("title") == m["title"])
        log.append(["post", slug, m["url"], ok]); print("update", slug, ok)
    json.dump(log, open(f"{A.HERE}/out/batch3-applied.json", "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
