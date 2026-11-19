"""One-off fixes from the Nov 2026 broken-link scan of every live post (report in the session scratchpad). Each post is backed up
first (never overwriting an existing backup) and only the exact broken fragment is replaced.
Run from the repo root: PYTHONPATH=tools python3 tools/blog/fix_links.py [--dry]"""
import json, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_triage as A

W = "https://www.ilmualam.com"
ZAKAT_OLD = "https://cdn.jsdelivr.net/gh/IlmuAlam/kalkulator-zakat@v1.1.0/kalkulator-zakat.v1.js"
ZAKAT_NEW = "https://cdn.jsdelivr.net/gh/ilmualam/kalkulator-zakat@1.1.0/asset/kalkulator-zakat.v1.js"
DEAD_SCRIPT = re.compile(r'<script src="https://cdn\.jsdelivr\.net/gh/ilmualam/name@v1\.0/asset/data/baby-namesv1\.js[^"]*"[^>]*></script>\s*')
ISLAM_GOV = re.compile(r'https://www\.islam\.gov\.my/ms/pengumuman/4955-[^"\']+')
FB_BAD = re.compile(r'https://www\.facebook\.com/sharer/sharer\.php\?u=(?:CURRENT_URL|/[^"\'&]+)')


def fixes(url, c, internal):
    out = c
    out = out.replace(ZAKAT_OLD, ZAKAT_NEW)
    out = DEAD_SCRIPT.sub("", out)
    out = ISLAM_GOV.sub("https://www.e-solat.gov.my/", out)
    out = FB_BAD.sub("https://www.facebook.com/sharer/sharer.php?u=" + urllib.parse.quote(url, safe=""), out)
    for src, old, new in internal["merge"]:
        if src == url:
            out = re.sub(r'(href=["\'])https?://(?:www\.)?ilmualam\.com' + re.escape(old[len(W):]), lambda m: m.group(1) + new, out)
    for src, old in internal["unpub"]:
        if src == url:  # keep the anchor text, drop the link to a post that no longer exists
            out = re.sub(r'<a[^>]+href=["\']https?://(?:www\.)?ilmualam\.com' + re.escape(old[len(W):]) + r'["\'][^>]*>(.*?)</a>', r'\1', out, flags=re.S)
    return out


def main():
    sp = sys.argv[sys.argv.index("--scan") + 1]
    posts = json.load(open(f"{sp}/live-posts.json")); internal = json.load(open(f"{sp}/internal.json"))
    log = []
    for p in posts:
        new = fixes(p["url"], p["content"], internal)
        if new == p["content"]:
            continue
        full = A.by_url(p["url"]); A.backup(full)
        A.patch(p["id"], {"content": new})
        log.append(p["url"]); print("fixed", p["url"].replace(W, ""))
    json.dump(log, open(f"{A.HERE}/out/links-fixed.json", "w"), indent=1)
    print("posts changed:", len(log))


if __name__ == "__main__":
    main()
