"""Printable review sheet for the Malay Rumi in tools/rumi_ms.py, for a qualified teacher to check before it is published.

python3 tools/rumi_review.py <out.html> [18,67]   (optional surah list; print it, or save it as PDF from the browser)

Each row: reference, Arabic (from data-surah/), the current English-style Rumi, the proposed Malay Rumi, a box for corrections.
The sheet is not part of the site; write it outside the repository root."""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rumi_ms as R
from surahs import S

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = f"file://{REPO}/assets/fonts/amiri-arabic-400-normal.woff2"
CONV = """- Mad (bacaan panjang) ditulis dengan vokal berganda: aa, ii, uu.
- Huruf 'ain ditulis ' (na'budu). Hamzah di tengah kalimah ditulis - (qur-aan, mu-minuun), di hujung ditulis ' (syaa').
- ث th · ذ z · ش sy · ص s · ض dh · ط t · ظ z · ح h · خ kh · غ gh · ق q
- Ditulis mengikut sebutan: alif lam syamsiah (ar rahmaan), idgham (mir rabbihim, saddaw wa), iqlab (mim ba'di), syaddah digandakan (innaka).
- Hujung setiap ayat ditulis dalam bentuk waqaf (al-hakiim, al-jannah). Koma menandakan tanda waqaf dalam ayat yang lazim diberhentikan.
- Rumi hanya alat bantu; ia tidak menggantikan talaqqi dan tajwid."""


def main(out, only=None):
    rows, last = [], None
    data = {}
    for (s, a), ru in sorted(R.RUMI.items()):
        if only and s not in only:
            continue
        if s not in data:
            data[s] = json.load(open(f"{REPO}/data-surah/surah-{s}.json", encoding="utf8"))
        v = data[s][a - 1]
        if s != last:
            rows.append(f'<tr class="sh"><th colspan="4">Surah {html.escape(S[s][1])} ({s})</th></tr>')
            last = s
        rows.append(f'<tr><td class="ref">{s}:{a}</td><td><p class="ar" lang="ar" dir="rtl">{html.escape(v["arabic"])}</p>'
                    f'<p class="old">Sedia ada: {html.escape(v["rumi"])}</p><p class="new">{html.escape(ru)}</p></td>'
                    f'<td class="ok">☐ Betul</td><td class="fix"></td></tr>')
    conv = html.escape(CONV)
    page = f"""<!doctype html><html lang="ms"><head><meta charset="utf-8"><title>Semakan Rumi Gaya Malaysia</title>
<style>
@font-face{{font-family:Amiri;src:url("{FONT}") format("woff2")}}
body{{font:14px/1.5 system-ui,sans-serif;margin:24px;color:#111}}
h1{{font-size:20px;margin:0 0 4px}} .lead{{margin:0 0 12px}} pre{{white-space:pre-wrap;background:#f4f4f4;padding:10px;font-size:12px}}
table{{width:100%;border-collapse:collapse}} td,th{{border:1px solid #999;padding:6px 8px;vertical-align:top}}
.sh th{{background:#e8f3ea;text-align:left;font-size:15px}} .ref{{width:52px;font-weight:700}}
.ar{{font:22px/2 Amiri,serif;margin:0}} .old{{color:#777;font-size:12px;margin:2px 0}} .new{{font-size:16px;font-weight:600;margin:2px 0}}
.ok{{width:70px;white-space:nowrap}} .fix{{width:30%}}
tr{{break-inside:avoid}} @page{{margin:14mm}}
</style></head><body>
<h1>Semakan Rumi Gaya Malaysia (quran.ilmualam.com)</h1>
<p class="lead">Sila semak setiap baris (huruf tebal) berbanding bacaan riwayat Hafs. Tanda “Betul” atau tulis pembetulan. {sum(1 for k in R.RUMI if not only or k[0] in only)} ayat.
Selepas semakan, nama dan tauliah penyemak akan dipaparkan pada halaman: “Rumi gaya Malaysia, disemak oleh …”.</p>
<p><strong>Nama penyemak:</strong> ______________________ &nbsp; <strong>Tauliah:</strong> ______________________ &nbsp; <strong>Tarikh:</strong> __________</p>
<pre>Konvensyen ejaan:
{conv}</pre>
<table><thead><tr><th>Ayat</th><th>Arab · Rumi sedia ada · <u>Rumi cadangan</u></th><th>Status</th><th>Pembetulan</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></body></html>"""
    open(out, "w", encoding="utf8").write(page)
    print("Review sheet:", out, f"({len(rows) - len({k[0] for k in R.RUMI if not only or k[0] in only})} ayat)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "rumi-review.html", {int(x) for x in sys.argv[2].split(",")} if len(sys.argv) > 2 else None)
