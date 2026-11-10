"""Name data for /nama-bayi-islam/: the legacy dataset of name.ilmualam.com (tools/nama/legacy.json) cleaned, the curated
names in tools/nama_data.py, and "Abdul + Asmaul Husna" names generated from tools/asmaul.py. Every single-word name is
looked up in data-surah/: a name whose Arabic word occurs in the Quran gets its first ayah and count, so the
"Al-Quran" label is computed, never typed. Writes assets/data/nama-bayi.json (fetched by assets/js/nama.js)."""
import json, os, re
from collections import Counter, defaultdict
import asmaul
import nama_data as ND
from plans import NAMES as SURAH_NAMES

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES = {"c": "Cahaya", "k": "Kekuatan", "b": "Keberkatan", "i": "Ilmu", "m": "Kemuliaan", "e": "Keindahan", "a": "Alam", "h": "Akhlak", "s": "Syurga"}
LEGACY_THEME = {"cahaya": "c", "kekuatan": "k", "keberkatan": "b", "ilmu": "i", "kemuliaan": "m", "keindahan": "e"}
SOURCES = {"n": "Nabi & keluarga Nabi", "s": "Sahabat & tokoh Islam", "u": "Nama Islam umum"}
# extra themes found from the meaning text, for legacy rows that only carry the six original themes
AUTO = {"a": r"\b(bunga|bintang|bulan|matahari|sungai|laut|langit|embun|hujan|awan|pohon|pokok|taman|mutiara|permata|angin|gunung|cahaya bulan|fajar|subuh|rusa|burung|singa|harum|wangi|mawar|melur|pelangi)",
        "h": r"\b(sabar|jujur|amanah|pemaaf|lembut|setia|rendah hati|pemurah|taat|soleh|takwa|bertakwa|ikhlas|penyayang|santun|penyantun|baik hati|bersyukur|syukur|zuhud|tawaduk|benar)",
        "s": r"\b(syurga|jannah|firdaus|kauthar|kautsar|salsabil|tasnim|bidadari|'adn|adn)\b"}

_MARKS = re.compile("[ً-ٰٟۖ-ۭـ]")


def ar_key(w):
    """Spelling key for one Arabic word: no harakat, one alif shape, final ya/ta marbuta unified."""
    w = w.replace("ـ", "")
    w = re.sub("([^ى])ٰ", "\\1ا", w)  # Uthmani dagger alif = a written long alif (but not on alif maqsura)
    w = re.sub("ًا$", "", w)             # tanwin fath + alif: نوحًا -> نوح
    w = _MARKS.sub("", w)
    for a in "ٱأإآٲ":
        w = w.replace(a, "ا")
    return w.replace("ى", "ي").replace("ۥ", "").replace("ۦ", "")


def quran_index():
    """bare word -> [count, first (surah, ayah)], each word also indexed without its prefixes (wa, fa, bi, li, ka, al)."""
    idx = {}
    for s in range(1, 115):
        for v in json.load(open(f"{REPO}/data-surah/surah-{s}.json", encoding="utf8")):
            for raw in v["arabic"].split():
                w = ar_key(raw)
                if len(w) < 2:
                    continue
                forms = {w}
                for p in ("وال", "فال", "بال", "كال", "ال", "لل", "و", "ف", "ب", "ل", "ك"):
                    if w.startswith(p) and len(w) - len(p) >= 2:
                        forms.add(w[len(p):])
                for f in forms:
                    if f in idx:
                        idx[f][0] += 1
                    else:
                        idx[f] = [1, (s, v["id"])]
    return idx


def syllables(name):
    n = name.lower().replace("'", "")
    n = re.sub(r"(aa|ee|ii|oo|uu)", "a", n)
    n = re.sub(r"(?<=[^aeiou])(ai|au)(?=[^aeiou]|$)", "a", n)  # Zai-nab, Hai-kal, Lai-la (but A-i-syah)
    return max(1, len(re.findall(r"[aeiou]+", n.replace("ai", "a i").replace("ua", "u a").replace("ia", "i a").replace("io", "i o"))) or 1)


def _abdul_rumi(ru):
    core = re.sub(r"^(Al|Ar|As|Asy|Az|An|At|Ad|Adh)-", "", ru).replace("'", "")
    core = {"Razzaq": "Razak", "Wahhab": "Wahab", "Aliyy": "Ali", "Qawiyy": "Qawi", "Waliyy": "Wali", "Ghaniyy": "Ghani", "Afuww": "Afuw",
            "Haqq": "Haq", "Mumin": "Mukmin", "Muizz": "Muiz", "Rauf": "Rauf", "Hayy": "Hayy", "Qadir": "Qadir"}.get(core, core)
    return "Abdul " + core


def abdul_names():
    out = []
    for ar, ru, mn in asmaul.NAMES:
        if ru in ND.ABD_SKIP:
            continue
        a = ar.strip()
        a = a[:-1] + "ِ" if a.endswith("ُ") else a
        extra = " Antara nama yang paling disukai Allah (HR Muslim 2132)." if ru == "Ar-Rahman" else ""
        out.append([_abdul_rumi(ru), "عَبْدُ " + a, f"Hamba kepada {mn} ({ru}).{extra}", "L", "u", 0, "b", "b"])
    return out


def parse(block, g):
    rows = []
    for line in block.strip().splitlines():
        name, ar, mn, src, th = line.split("|")
        rows.append([name, ar, mn, g, src, 0, th, "e"])
    return rows


AWALAN = re.compile(r"(ul|us|ur|un|uz|ud|ut|ush|ulh|atul|atus|atun)$", re.I)


def legacy_rows():
    d = json.load(open(f"{REPO}/tools/nama/legacy.json", encoding="utf8"))["names"]
    out, drop = [], Counter()
    for name, ar, mn, g, src, syl, th in d:
        low = name.lower()
        if " " in name:
            drop["nama berganding (dijana semula oleh penjana)"] += 1
            continue
        if low in ND.BLOCK or low in ND.MAKRUH:
            drop["disemak editor: maksud atau bentuk tidak sesuai"] += 1
            continue
        if low in ND.ALLAH_ONLY:
            drop["nama khusus bagi Allah"] += 1
            continue
        if (low.startswith("muhammad") and len(low) > 8) or low in ("yahyawi", "safiahum") or (low.endswith("syah") and "شاه" not in ar):
            drop["gabungan tidak lazim"] += 1
            continue
        flag = "a" if AWALAN.search(name) and ar.strip().endswith("ُ") else ""
        mn = re.sub(r"\b[Yy]ang maha\b", "Yang sangat", mn) if not low.startswith("abd") else mn
        mn = re.sub(r"^Maha\b", "Sangat", mn)
        t = "".join(LEGACY_THEME[x] for x in th if x in LEGACY_THEME)
        for k, rx in AUTO.items():
            if re.search(rx, mn.lower()) and k not in t:
                t += k
        out.append([name, ar.strip(), mn.strip(), g, {"nabi": "n", "sahabat": "s"}.get(src, "u"), syl, t, flag])
    return out, drop


def build():
    legacy, drop = legacy_rows()
    cur = parse(ND.LELAKI, "L") + parse(ND.PEREMPUAN, "P") + parse(ND.UNISEKS, "U") + abdul_names()
    for r in cur:  # inline "(Surah 19:7)" references in curated meanings must point at a real ayah
        for s, a in re.findall(r"\b(\d{1,3}):(\d{1,3})\b", r[2]):
            assert 1 <= int(s) <= 114 and int(a) <= len(json.load(open(f"{REPO}/data-surah/surah-{s}.json", encoding="utf8"))), (r[0], s, a)
    base = {(r[0].lower(), r[3]): r for r in legacy + cur}
    for k in sorted(ND.DERIVE):
        m = base[(k, "L")]
        mn = "; ".join(p for p in m[2].split("; ") if "bin " not in p and "ﷺ" not in p and "Allah;" not in p)
        if (k + "ah", "P") not in base:
            cur.append([m[0] + "ah", m[1].strip() + "َة", mn, "P", "u", 0, m[6], "e"])
    uni = {r[0].lower() for r in cur if r[3] == "U"}
    curk = {(r[0].lower(), r[3]) for r in cur}
    rows, seen = [], set()
    for r in cur + [r for r in legacy if (r[0].lower(), r[3]) not in curk and r[0].lower() not in uni]:
        k = (r[0].lower(), r[3])
        if k in seen:
            continue
        seen.add(k)
        if not r[5]:
            r[5] = sum(syllables(p) for p in r[0].split())
        rows.append(r)
    idx = quran_index()
    import nabi
    kisah = {ar_key(n["ar"]): n["slug"] for n in nabi.NABI}
    kisah[ar_key("أَحْمَد")] = "nabi-muhammad"
    for r in rows:
        q = idx.get(ar_key(r[1])) if " " not in r[1].strip() else None
        r.append(f"{q[1][0]}:{q[1][1]}" if q else "")
        r.append(q[0] if q else 0)
        r.append(kisah.get(ar_key(r[1]), "") if r[3] == "L" and r[4] == "n" else "")
    rows.sort(key=lambda r: (r[0].lower(), r[3]))
    return rows, drop, len(legacy), len(cur)


def write(rows):
    out = {"v": 2, "themes": THEMES, "sources": SOURCES,
           # [name, arabic, meaning, gender L/P/U, source n/s/u, syllables, themes (letters), flags (a = awalan, b = Abdul + Asmaul Husna, e = written or reviewed by the editor),
           #  first ayah "s:a" where the word occurs, Quran count, /kisah-nabi/ slug]
           "sn": SURAH_NAMES, "n": rows}
    open(f"{REPO}/assets/data/nama-bayi.json", "w", encoding="utf8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    rows, drop, nl, nc = build()
    print(len(rows), "rows from", nl, "legacy kept +", nc, "curated; dropped:", dict(drop))
    print(Counter(r[3] for r in rows), Counter(r[4] for r in rows), "awalan", sum(1 for r in rows if r[7] == "a"))
    print("in Quran:", sum(1 for r in rows if r[8]), "unique spellings:", len({r[0].lower() for r in rows}))
