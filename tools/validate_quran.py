"""Integrity check for data-surah/: fails loudly if any surah, ayah count, ayah id or text changes.

- Ayah counts per surah are pinned to the standard Hafs/Kufah count (6,236 in total).
- Every ayah must have non-empty arabic, rumi and translation, with ids 1..N in order.
- Each surah's Arabic, Rumi and translation are hashed separately and compared with tools/quran-checksums.json,
  so an accidental edit, a bad merge or a re-download from another edition cannot slip into the site unnoticed.

Run:  python3 tools/validate_quran.py            (check; build.py runs this first)
      python3 tools/validate_quran.py --update   (only after a deliberate, reviewed data change: rewrites the checksums)
"""
import hashlib
import json
import os
import sys

SCR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SCR)
SUMS = f"{SCR}/quran-checksums.json"
FIELDS = ("arabic", "rumi", "translation")
COUNTS = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99, 128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69,
          60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11,
          11, 18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29, 19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8,
          19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6]
assert len(COUNTS) == 114 and sum(COUNTS) == 6236


def digests():
    out, errs = {}, []
    for n in range(1, 115):
        d = json.load(open(f"{REPO}/data-surah/surah-{n}.json", encoding="utf8"))
        if len(d) != COUNTS[n - 1]:
            errs.append(f"surah {n}: {len(d)} ayat, expected {COUNTS[n - 1]}")
        if [v.get("id") for v in d] != list(range(1, len(d) + 1)):
            errs.append(f"surah {n}: ayah ids are not 1..{len(d)} in order")
        for v in d:
            for k in FIELDS:
                if not str(v.get(k, "")).strip():
                    errs.append(f"surah {n} ayat {v.get('id')}: empty {k}")
        out[str(n)] = {k: hashlib.sha256("\n".join(v.get(k, "") for v in d).encode("utf8")).hexdigest()[:16] for k in FIELDS}
    return out, errs


def main(update=False):
    got, errs = digests()
    if errs:
        sys.exit("Quran data check FAILED:\n  " + "\n  ".join(errs[:30]))
    if update or not os.path.exists(SUMS):
        open(SUMS, "w", encoding="utf8", newline="\n").write(json.dumps(got, indent=1) + "\n")
        print("Quran checksums written:", SUMS)
        return
    want = json.load(open(SUMS, encoding="utf8"))
    diff = [f"surah {n} {k}" for n in want for k in FIELDS if want[n].get(k) != got.get(n, {}).get(k)]
    if diff:
        sys.exit("Quran text changed versus tools/quran-checksums.json:\n  " + "\n  ".join(diff)
                 + "\nIf the change is deliberate and checked against an approved mushaf, run: python3 tools/validate_quran.py --update")
    print("Quran data OK: 114 surah, 6,236 ayat, checksums match")


if __name__ == "__main__":
    main("--update" in sys.argv)
