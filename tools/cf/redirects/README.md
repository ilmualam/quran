# ilmualam-redirects (Cloudflare Worker)

301 redirects for the 55 www.ilmualam.com posts merged during the Nov 2026 refresh. `worker.js` is generated from
`tools/blog/out/redirects.json`; each source path has its own Workers route (`www.ilmualam.com/<path>*`), so no other
request runs the Worker and the free-plan request budget is untouched.

Deployed through the Cloudflare API (script `ilmualam-redirects`, zone ilmualam.com). To change a redirect, edit
`redirects.json`, regenerate `worker.js`, upload it again (PUT /accounts/<id>/workers/scripts/ilmualam-redirects) and add
or remove the matching route.

Related zone change (same session): the apex `ilmualam.com` A records are proxied and a redirect rule sends
`ilmualam.com/*` to `https://www.ilmualam.com/*` in one 301, keeping the query string.
