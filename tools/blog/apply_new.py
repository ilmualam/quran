"""Publish NEW posts (batch5.NEW) on Blogger with a clean permalink: create the post with a short title (Blogger builds the URL from the
title at first publish), then PATCH the full title and body. If Blogger's URL differs from the one the build assumed (canonical, JSON-LD),
the body is rebuilt with the real URL before the PATCH. Skips any slug already in out/new-applied.json.
Run from the repo root: PYTHONPATH=tools python3 tools/blog/apply_new.py [--dry]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_triage as A
import batch5
from gen import build

LOG = f"{A.HERE}/out/new-applied.json"


def main():
    done = json.load(open(LOG)) if os.path.exists(LOG) else {}
    for slug, p in batch5.POSTS:
        if slug in done:
            print("skip", slug, done[slug]["url"]); continue
        short, want = batch5.NEW[slug]
        if A.DRY:
            print("would create", slug, "as", repr(short), "->", want); continue
        made = A.call(f"{A.API}/blogs/{A.B}/posts/", json.dumps({"title": short, "content": build(p), "labels": [p["crumb"][0]]}).encode(), "POST")
        url = made["url"]
        if url != want:
            p = dict(p, url=url)
        r = A.patch(made["id"], {"title": p["title"], "content": build(p)})
        done[slug] = {"id": made["id"], "url": url, "title_ok": r.get("title") == p["title"], "url_as_planned": url == want}
        json.dump(done, open(LOG, "w"), ensure_ascii=False, indent=1)
        print("published", slug, url, done[slug])


if __name__ == "__main__":
    main()
