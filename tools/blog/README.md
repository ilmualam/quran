# www.ilmualam.com post refresh

Source for refreshing old Blogger posts on www.ilmualam.com. Nothing here is deployed to quran.ilmualam.com except the images.

| Path | What |
|---|---|
| `tools/blog/gen.py` | Generates each refreshed post as self-contained Blogger HTML (namespaced `ilmx-*` CSS, Article + FAQPage + BreadcrumbList JSON-LD, copy buttons, tools). Quran text comes from `data-surah/`, verified doa text from `tools/ibadah.py`. Run `python3 tools/blog/gen.py`. |
| `tools/blog/out/<slug>.html` | Final post body to put into Blogger (HTML view). |
| `tools/blog/out/<slug>.json` | Post URL, new title, search description, image file, original publish date. |
| `tools/blog/posts-audit.json` | Audit of all 386 posts (date, words, images, H2 count, labels) used for the triage. |
| `assets/blog/*.webp` | Featured images (1200x675), served at `https://quran.ilmualam.com/assets/blog/<file>`. |

Policy: Malay, mazhab Syafi'i; every hadith with book and number, weak narrations labelled; no fabricated fadhilat; URLs never change.
Note: Google stopped showing FAQ rich results on 7 May 2026, so the FAQ section and its JSON-LD are kept for readers, Bing and AI answer engines, not for a Google rich result.
