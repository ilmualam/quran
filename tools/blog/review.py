"""Builds a private review page for a batch of refreshed posts: one tab per post with old vs new title, search description,
word count, change notes, then the post body as it will appear in Blogger. Usage:
python3 review.py <out_dir> <title> <slug:old title:old words:note1|note2> ...   (images are copied next to the page)"""
import html, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
e = lambda s: html.escape(str(s), quote=True)


def page(title, intro, posts, note=""):
    tabs, panes, imgs = [], [], []
    for i, (slug, oldt, oldw, changes) in enumerate(posts):
        m = json.load(open(f"{HERE}/out/{slug}.json")); h = open(f"{HERE}/out/{slug}.html").read()
        h = h.replace("https://quran.ilmualam.com/assets/blog/", "img/"); imgs.append(m["img"])
        t = re.sub(r"<style.*?</style>|<script.*?</script>", " ", h, flags=re.S); w = len(re.sub(r"<[^>]+>", " ", t).split())
        tabs.append(f'<button type="button" role="tab" id="t{i}" aria-controls="p{i}" aria-selected="{"true" if i == 0 else "false"}">{e(m["title"].split(":")[0])}</button>')
        ch = "".join(f"<li>{e(c)}</li>" for c in changes)
        panes.append(f'''<section class="pane" id="p{i}" role="tabpanel" aria-labelledby="t{i}"{"" if i == 0 else " hidden"}>
<div class="meta">
 <div class="kv"><span class="k">URL (unchanged)</span><a class="v mono" href="{e(m["url"])}">{e(m["url"].replace("https://www.ilmualam.com", ""))}</a></div>
 <div class="kv"><span class="k">Old title</span><span class="v old">{e(oldt)}</span></div>
 <div class="kv"><span class="k">New title · {len(m["title"])} chars</span><span class="v strong">{e(m["title"])}</span></div>
 <div class="kv"><span class="k">Search description · {len(m["desc"])} chars</span><span class="v">{e(m["desc"])}</span></div>
 <div class="kv"><span class="k">Length</span><span class="v num">{oldw} → {w} words</span></div>
 <div class="kv wide"><span class="k">What changed</span><ul class="v">{ch}</ul></div>
</div>
<p class="frame-label">Preview as it will appear in the Blogger post body</p>
<div class="frame">{h}</div>
</section>''')
    css = """
/* layout: review console, tab per post, metadata sheet above a white "blog body" frame */
:root{--bg:#f3f5f2;--surface:#fff;--fg:#17251b;--muted:#5d6e62;--line:#d9e1db;--accent:#1f6b3a;--accent-soft:#e3f1e7;--gold:#a7801b;
--sans:'Inter',system-ui,-apple-system,sans-serif;--head:'Space Grotesk','Inter',system-ui,sans-serif;--mono:ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#101612;--surface:#18211b;--fg:#e4ece6;--muted:#9fb1a5;--line:#2b3a30;--accent:#6fcf8e;--accent-soft:#1d3325;--gold:#e0b84f;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#101612;--surface:#18211b;--fg:#e4ece6;--muted:#9fb1a5;--line:#2b3a30;--accent:#6fcf8e;--accent-soft:#1d3325;--gold:#e0b84f;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:15px;line-height:1.55}
.wrap{max-width:900px;margin:0 auto;padding-block:24px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1{font-family:var(--head);font-size:1.6rem;margin:0 0 4px;text-wrap:balance}
.sub{color:var(--muted);margin:0 0 18px;max-width:65ch}
[role=tablist]{display:flex;gap:6px;overflow-x:auto;border-bottom:1px solid var(--line);margin-bottom:16px}
[role=tab]{font:inherit;font-weight:600;background:none;border:0;border-bottom:3px solid transparent;color:var(--muted);padding:10px 12px;cursor:pointer;white-space:nowrap}
[role=tab][aria-selected=true]{color:var(--fg);border-bottom-color:var(--accent)}
[role=tab]:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:12px 20px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:16px}
.kv{display:flex;flex-direction:column;gap:2px;min-width:0}.kv.wide{grid-column:1/-1}
.k{font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:700}
.v{overflow-wrap:anywhere}.v.strong{font-weight:700}.v.old{color:var(--muted);text-decoration:line-through}
.mono{font-family:var(--mono);font-size:.85rem;color:var(--accent)}.num{font-variant-numeric:tabular-nums;font-weight:700;color:var(--gold)}
ul.v{margin:4px 0 0;padding-left:1.1rem}ul.v li{margin-bottom:4px}
.frame-label{font-size:.78rem;color:var(--muted);margin:0 0 6px}
.frame{background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px;overflow:hidden}
.note{margin-top:20px;background:var(--accent-soft);border-radius:12px;padding:14px 16px;font-size:.9rem}
"""
    js = """<script>(function(){var t=[].slice.call(document.querySelectorAll('[role=tab]'));function s(i){t.forEach(function(b,j){b.setAttribute('aria-selected',j===i);document.getElementById('p'+j).hidden=j!==i})}
t.forEach(function(b,i){b.addEventListener('click',function(){s(i)});b.addEventListener('keydown',function(ev){var n=ev.key==='ArrowRight'?1:ev.key==='ArrowLeft'?-1:0;if(n){var k=(i+n+t.length)%t.length;t[k].focus();s(k)}})})})();</script>"""
    body = (f'<title>{e(title)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<style>{css}</style>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@600;700&family=Amiri&display=swap">\n'
            f'<div class="wrap"><h1>{e(title)}</h1><p class="sub">{intro}</p><div role="tablist" aria-label="Posts">{"".join(tabs)}</div>{"".join(panes)}'
            + (f'<div class="note">{note}</div>' if note else "") + f"</div>\n{js}")
    return body, imgs


def write(out_dir, title, intro, posts, note=""):
    os.makedirs(f"{out_dir}/img", exist_ok=True)
    body, imgs = page(title, intro, posts, note)
    for f in imgs:
        shutil.copy(f"{REPO}/assets/blog/{f}", f"{out_dir}/img/{f}")
    open(f"{out_dir}/index.html", "w", encoding="utf8").write(body)
    return imgs
