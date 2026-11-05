"""Applies the Cloudflare settings for quran.ilmualam.com only (the zone's other hostnames, e.g. the Blogger site on www, are untouched).
Run by .github/workflows/cloudflare.yml with a CF_API_TOKEN secret (Zone: Read, Config Rules: Edit, Cache Rules: Edit on ilmualam.com).

Every rule this script owns has a ref starting with "quran_". On each run it reads the zone's rules for a phase, drops the
old quran_ rules, appends the current ones and writes the phase back, so other rules in the zone are kept and running it
twice changes nothing. DRY_RUN=1 prints what would be sent without writing.

Config rule (http_config_settings), host = quran.ilmualam.com:
  ssl full            GitHub Pages serves a valid certificate; "full" (not strict) keeps the site up if GitHub's renewal
                      is ever delayed behind the proxy, while Flexible would loop with GitHub's "Enforce HTTPS"
  rocket_loader off,  these inject or rewrite scripts, which the site's Content-Security-Policy blocks (console errors,
  email_obfuscation   broken scripts); the site has no email addresses to hide and loads one deferred script anyway
  off, disable_zaraz,
  disable_rum
  automatic_https_rewrites on
Cache rules (http_request_cache_settings), host = quran.ilmualam.com:
  quran_cache         cache everything, edge and browser TTL from GitHub Pages (max-age=600): pages are served from the
                      nearest Cloudflare PoP for 10 minutes, and the zone-wide "Browser Cache TTL" (1 day) no longer
                      makes browsers keep yesterday's alat.js next to today's HTML
  quran_cache_live    /sw.js and /manifest.webmanifest are never cached at the edge, so a deploy reaches visitors at once
                      (listed last: for cache rules the last matching rule wins)"""
import json, os, sys, urllib.request, urllib.error

API = os.environ.get("CF_API_BASE", "https://api.cloudflare.com/client/v4")
HOST = os.environ.get("CF_HOST", "quran.ilmualam.com")
ZONE = os.environ.get("CF_ZONE", "ilmualam.com")
TOKEN = os.environ.get("CF_API_TOKEN", "")
DRY = os.environ.get("DRY_RUN", "") in ("1", "true", "yes")
HOSTX = f'(http.host eq "{HOST}")'

RULES = {
    "http_config_settings": [
        {"ref": "quran_config", "description": f"[quran] {HOST}: SSL full, no injected scripts", "expression": HOSTX, "action": "set_config",
         "action_parameters": {"ssl": "full", "rocket_loader": False, "email_obfuscation": False, "automatic_https_rewrites": True,
                               "disable_zaraz": True, "disable_rum": True}, "enabled": True},
    ],
    "http_request_cache_settings": [
        {"ref": "quran_cache", "description": f"[quran] {HOST}: cache, TTL from origin", "expression": HOSTX, "action": "set_cache_settings",
         "action_parameters": {"cache": True, "edge_ttl": {"mode": "respect_origin"}, "browser_ttl": {"mode": "respect_origin"}}, "enabled": True},
        {"ref": "quran_cache_live", "description": f"[quran] {HOST}: never cache the service worker and manifest",
         "expression": f'{HOSTX[:-1]} and http.request.uri.path in {{"/sw.js" "/manifest.webmanifest"}})', "action": "set_cache_settings",
         "action_parameters": {"cache": False}, "enabled": True},
    ],
}
KEEP = ("id", "ref", "description", "expression", "action", "action_parameters", "enabled", "logging", "ratelimit", "exposed_credential_check")


def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def die(msg, res=None):
    print(f"::error::{msg}" + (f" {json.dumps(res.get('errors', res))}" if res else ""))
    sys.exit(1)


def main():
    if not TOKEN:
        die("CF_API_TOKEN is empty: add it under Settings > Secrets and variables > Actions.")
    st, res = call("GET", f"/zones?name={ZONE}")
    if st != 200 or not res.get("result"):
        die(f"zone {ZONE} not found or the token cannot read it (needs Zone: Read).", res)
    zid = res["result"][0]["id"]
    print(f"zone {ZONE} ({zid}), host {HOST}{', DRY RUN' if DRY else ''}")
    for phase, mine in RULES.items():
        st, res = call("GET", f"/zones/{zid}/rulesets/phases/{phase}/entrypoint")
        if st == 404:
            existing = []
        elif st == 200:
            existing = res["result"].get("rules", [])
        else:
            die(f"cannot read {phase} (token needs Config Rules: Edit and Cache Rules: Edit).", res)
        others = [{k: r[k] for k in KEEP if k in r} for r in existing if not str(r.get("ref", "")).startswith("quran_")]
        rules = others + mine
        print(f"{phase}: keeping {len(others)} other rule(s), writing {len(mine)} quran rule(s)")
        if DRY:
            print(json.dumps(mine, indent=2))
            continue
        st, res = call("PUT", f"/zones/{zid}/rulesets/phases/{phase}/entrypoint", {"rules": rules})
        if st != 200 or not res.get("success"):
            die(f"writing {phase} failed; nothing in this phase was changed.", res)
        print(f"{phase}: OK")


if __name__ == "__main__":
    main()
