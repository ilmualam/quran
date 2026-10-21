"""Faraid (Islamic inheritance) per the Shafi'i school as practised in Malaysia: exclusion (hajb hirman), fixed shares,
'umariyyatain, musytarakah, 'aul, asabah (bin-nafs, bil-ghair, ma'al-ghair), and the residue to Baitulmal (or radd to the
non-spouse sharers when chosen). Datuk together with full/paternal siblings (muqasamah) is reported, not computed.
alat.js mirrors faraid() and faraid_html() exactly: all arithmetic is in fractions and integer sen."""
from fractions import Fraction as Fr
from math import lcm

# key, label, max count (1 = yes/no), male?
HEIRS = [
    ("su", "Suami", 1, 1), ("is", "Isteri", 4, 0),
    ("bp", "Bapa", 1, 1), ("ib", "Ibu", 1, 0), ("dt", "Datuk (bapa kepada bapa)", 1, 1),
    ("ni", "Nenek sebelah ibu", 1, 0), ("nb", "Nenek sebelah bapa", 1, 0),
    ("al", "Anak lelaki", 30, 1), ("ap", "Anak perempuan", 30, 0),
    ("cl", "Cucu lelaki (daripada anak lelaki)", 30, 1), ("cp", "Cucu perempuan (daripada anak lelaki)", 30, 0),
    ("skl", "Saudara lelaki seibu sebapa", 30, 1), ("skp", "Saudara perempuan seibu sebapa", 30, 0),
    ("sbl", "Saudara lelaki sebapa", 30, 1), ("sbp", "Saudara perempuan sebapa", 30, 0),
    ("sil", "Saudara lelaki seibu", 30, 1), ("sip", "Saudara perempuan seibu", 30, 0),
    ("ask", "Anak saudara lelaki (daripada saudara lelaki seibu sebapa)", 30, 1), ("asb", "Anak saudara lelaki (daripada saudara lelaki sebapa)", 30, 1),
    ("bsk", "Bapa saudara seibu sebapa (sebelah bapa)", 30, 1), ("bsb", "Bapa saudara sebapa (sebelah bapa)", 30, 1),
    ("spk", "Sepupu lelaki (anak bapa saudara seibu sebapa)", 30, 1), ("spb", "Sepupu lelaki (anak bapa saudara sebapa)", 30, 1),
]
KEYS = [h[0] for h in HEIRS]
LABEL = {h[0]: h[1] for h in HEIRS}
MAXN = {h[0]: h[2] for h in HEIRS}
SHORT = {"al": "anak lelaki", "ap": "anak perempuan", "cl": "cucu lelaki", "cp": "cucu perempuan", "bp": "bapa", "ib": "ibu", "dt": "datuk",
         "skl": "saudara lelaki seibu sebapa", "skp": "saudara perempuan seibu sebapa", "sbl": "saudara lelaki sebapa", "sbp": "saudara perempuan sebapa",
         "ask": "anak saudara lelaki seibu sebapa", "asb": "anak saudara lelaki sebapa", "bsk": "bapa saudara seibu sebapa", "bsb": "bapa saudara sebapa",
         "spk": "sepupu lelaki seibu sebapa", "skp_ag": "saudara perempuan seibu sebapa (asabah ma'al ghair)", "sbp_ag": "saudara perempuan sebapa (asabah ma'al ghair)",
         "ap2": "2 anak perempuan atau lebih", "skp2": "2 saudara perempuan seibu sebapa atau lebih"}
CHAIN = ["al", "cl", "bp", "dt", "skl", "skp_ag", "sbl", "sbp_ag", "ask", "asb", "bsk", "bsb", "spk", "spb"]


def faraid(h, radd=False):
    """h: {key: count}. Returns dict(rows=[(key, n, share Fraction, basis)], ex=[(key, n, reason)], bm Fraction, base, aul, note, bad)."""
    n = {k: max(0, min(MAXN[k], int(h.get(k, 0) or 0))) for k in KEYS}
    ex = {}

    def block(k, reason):
        if n[k] and k not in ex:
            ex[k] = reason

    def live(k):
        return n[k] > 0 and k not in ex

    desc = n["al"] + n["ap"] + n["cl"] + n["cp"] > 0
    if n["al"]:
        block("cl", "al"); block("cp", "al")
    elif n["ap"] >= 2 and not n["cl"]:
        block("cp", "ap2")
    if n["bp"]:
        block("dt", "bp")
    if n["ib"]:
        block("ni", "ib"); block("nb", "ib")
    if n["bp"]:
        block("nb", "bp")
    for k in ("sil", "sip"):
        for b in ("al", "ap", "cl", "cp", "bp", "dt"):
            if live(b):
                block(k, b)
    for k in ("skl", "skp", "sbl", "sbp"):
        for b in ("al", "cl", "bp"):
            if live(b):
                block(k, b)
    if live("dt") and any(live(k) for k in ("skl", "skp", "sbl", "sbp")):
        return dict(rows=[], ex=[], bm=Fr(0), base=0, aul=0, note="", bad=True)
    fdesc = live("ap") or live("cp")
    ag = {"skp_ag": live("skp") and not n["skl"] and fdesc}
    for k in ("sbl", "sbp"):
        if live("skl"):
            block(k, "skl")
        elif ag["skp_ag"]:
            block(k, "skp_ag")
    if live("sbp") and n["skp"] >= 2 and not n["sbl"]:
        block("sbp", "skp2")
    ag["sbp_ag"] = live("sbp") and not n["sbl"] and fdesc
    for i, k in enumerate(CHAIN[8:], 8):
        for b in CHAIN[:i]:
            if (ag.get(b) if b in ag else live(b)):
                block(k, b)
                break

    fard, asab = {}, {}
    basis = {}
    sibs = sum(n[k] for k in ("skl", "skp", "sbl", "sbp", "sil", "sip"))
    spouse = Fr(0)
    if live("su"):
        fard["su"] = spouse = Fr(1, 4) if desc else Fr(1, 2)
    if live("is"):
        fard["is"] = spouse = Fr(1, 8) if desc else Fr(1, 4)
    note = ""
    if live("ib"):
        if desc or sibs >= 2:
            fard["ib"] = Fr(1, 6)
        elif live("bp") and spouse:
            fard["ib"] = (1 - spouse) / 3
            note = "umar"
            basis["ib"] = "1/3 baki ('umariyyatain)"
        else:
            fard["ib"] = Fr(1, 3)
    for k in ("bp", "dt"):
        if live(k):
            if live("al") or live("cl"):
                fard[k] = Fr(1, 6)
            elif desc:
                fard[k] = Fr(1, 6); asab[k] = 1
                basis[k] = "1/6 + asabah"
            else:
                asab[k] = 1
    gm = [k for k in ("ni", "nb") if live(k)]
    for k in gm:
        fard[k] = Fr(1, 6) / len(gm)
    if live("ap"):
        if live("al"):
            asab["al"], asab["ap"] = 2, 1
        else:
            fard["ap"] = Fr(1, 2) if n["ap"] == 1 else Fr(2, 3)
    elif live("al"):
        asab["al"] = 2
    if live("cp"):
        if live("cl"):
            asab["cl"], asab["cp"] = 2, 1
        elif not n["ap"]:
            fard["cp"] = Fr(1, 2) if n["cp"] == 1 else Fr(2, 3)
        else:
            fard["cp"] = Fr(1, 6)
            basis["cp"] = "1/6 (takmilah 2/3)"
    elif live("cl"):
        asab["cl"] = 2
    ut = n["sil"] + n["sip"] if live("sil") or live("sip") else 0
    mus = (ut >= 2 and live("skl") and live("su") and (live("ib") or gm) and not desc and not live("bp") and not live("dt"))
    if ut:
        share = Fr(1, 6) if ut == 1 else Fr(1, 3)
        heads = ut + (n["skl"] + n["skp"] if mus else 0)
        for k in ("sil", "sip") + (("skl", "skp") if mus else ()):
            if live(k):
                fard[k] = share * n[k] / heads
                if mus:
                    basis[k] = "1/3 dikongsi sama rata (musytarakah)"
        if mus:
            note = "mus"
    if not mus:
        if live("skl"):
            asab["skl"] = 2
            if live("skp"):
                asab["skp"] = 1
        elif live("skp"):
            if ag["skp_ag"]:
                asab["skp"] = 1
                basis["skp"] = "Asabah ma'al ghair"
            else:
                fard["skp"] = Fr(1, 2) if n["skp"] == 1 else Fr(2, 3)
        if live("sbl"):
            asab["sbl"] = 2
            if live("sbp"):
                asab["sbp"] = 1
        elif live("sbp"):
            if ag["sbp_ag"]:
                asab["sbp"] = 1
                basis["sbp"] = "Asabah ma'al ghair"
            elif n["skp"] == 1 and live("skp"):
                fard["sbp"] = Fr(1, 6)
                basis["sbp"] = "1/6 (takmilah 2/3)"
            else:
                fard["sbp"] = Fr(1, 2) if n["sbp"] == 1 else Fr(2, 3)
    for k in CHAIN[8:]:
        if live(k):
            asab[k] = 1

    base = lcm(*[f.denominator for f in fard.values()]) if fard else 1
    tot = sum(fard.values(), Fr(0))
    aul = int(tot * base) if tot > 1 else 0
    share = dict(fard)
    if tot > 1:
        share = {k: v / tot for k, v in fard.items()}
    rest = max(Fr(0), 1 - tot)
    bm = Fr(0)
    if rest:
        if asab:
            w = sum(asab[k] * n[k] for k in asab)
            for k in asab:
                share[k] = share.get(k, Fr(0)) + rest * asab[k] * n[k] / w
        else:
            pool = {k: v for k, v in fard.items() if k not in ("su", "is")}
            if radd and pool:
                pt = sum(pool.values(), Fr(0))
                for k, v in pool.items():
                    share[k] += rest * v / pt
                note = note or "radd"
            else:
                bm = rest
    rows = []
    for k in KEYS:
        if live(k):
            sh = share.get(k, Fr(0))
            if k in basis:
                b = basis[k]
            elif k in asab:
                b = "Fardh + asabah" if k in fard else "Asabah" + (" (lelaki 2 : perempuan 1)" if len(set(asab.values())) > 1 else "")
            elif k in ("ni", "nb") and len(gm) == 2:
                b = "1/6 dikongsi"
            elif k in ("sil", "sip") and ut > 1:
                b = "1/3 dikongsi"
            else:
                b = "Fardh" + (" dikongsi" if n[k] > 1 else "")
            rows.append((k, n[k], sh, b))
    exl = [(k, n[k], ex[k]) for k in KEYS if k in ex]
    return dict(rows=rows, ex=exl, bm=bm, base=base if fard else 0, aul=aul, note=note, bad=False)


def sen(x):
    return round(float(x) * 100) if isinstance(x, float) else int(x)


def fmt_sen(s):
    return f"RM{s // 100:,}.{s % 100:02d}"


def part(e, f, cnt=1):
    """Integer sen of estate e (sen) × fraction f / cnt, rounded half up."""
    num, den = e * f.numerator, f.denominator * cnt
    return (2 * num + den) // (2 * den)


def pct(f):
    h = (20000 * f.numerator + f.denominator) // (2 * f.denominator)
    return f"{h // 100}.{h % 100:02d}%"


def frs(f):
    return f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)


def estate(gross, debt, funeral, will):
    """All in sen; the bequest is capped at a third of what remains after debts and funeral costs."""
    net = max(0, gross - debt - funeral)
    w = min(will, net // 3)
    return net - w, w


NOTES = {"umar": "Kes 'umariyyatain: ibu mendapat 1/3 daripada baki selepas bahagian suami/isteri.",
         "mus": "Kes musytarakah (himariyyah): saudara seibu sebapa berkongsi 1/3 bersama saudara seibu (mazhab Syafi'i).",
         "radd": "Baki dikembalikan (radd) kepada waris fardu selain suami/isteri, mengikut nisbah bahagian mereka."}


def faraid_html(h, e, radd=False):
    """e: net estate in sen (after debts, funeral costs and bequest)."""
    r = faraid(h, radd)
    if r["bad"]:
        return ('<p class="jvh mb">⚠️ Kes datuk bersama saudara seibu sebapa/sebapa</p><p>Pembahagian datuk bersama adik-beradik (muqasamah) mempunyai kaedah khas '
                'dan khilaf ulama. Kalkulator ini tidak mengiranya; sila rujuk Mahkamah Syariah atau Pejabat Pusaka Kecil.</p>')
    if not r["rows"] and not r["ex"]:
        return f'<p class="jvh no">Tiada waris dipilih</p><p>Jika tiada waris langsung, keseluruhan harta ({fmt_sen(e)}) diserahkan kepada Baitulmal.</p>'
    head = f'<p class="frs">Harta untuk dibahagi: <strong>{fmt_sen(e)}</strong>'
    if r["base"]:
        head += f' · Asal masalah <strong>{r["base"]}</strong>' + (f", <strong>'aul kepada {r['aul']}</strong>" if r["aul"] else "")
    head += "</p>"
    if r["note"]:
        head += f'<p class="note">{NOTES[r["note"]]}</p>'
    tr = ""
    for k, c, sh, b in r["rows"]:
        tr += (f'<tr><th scope="row">{LABEL[k]}{f" × {c}" if c > 1 else ""}</th><td data-l="Bahagian">{frs(sh)}<small>{b}</small></td><td data-l="%">{pct(sh)}</td>'
               f'<td data-l="Seorang">{fmt_sen(part(e, sh, c))}</td><td data-l="Jumlah">{fmt_sen(part(e, sh))}</td></tr>')
    if r["bm"]:
        tr += (f'<tr><th scope="row">Baitulmal</th><td data-l="Bahagian">{frs(r["bm"])}<small>Baki tanpa asabah</small></td><td data-l="%">{pct(r["bm"])}</td><td data-l="Seorang">–</td>'
               f'<td data-l="Jumlah">{fmt_sen(part(e, r["bm"]))}</td></tr>')
    out = head + ('<div class="tw"><table class="frt rt"><thead><tr><th scope="col">Waris</th><th scope="col">Bahagian</th><th scope="col">%</th>'
                  f'<th scope="col">Seorang</th><th scope="col">Jumlah</th></tr></thead><tbody>{tr}</tbody></table></div>')
    if r["ex"]:
        out += '<p class="frh">Terhalang (mahjub)</p><ul class="frx">' + "".join(
            f'<li><strong>{LABEL[k]}{f" × {c}" if c > 1 else ""}</strong>: terhalang oleh {SHORT[why]}</li>' for k, c, why in r["ex"]) + "</ul>"
    return out


if __name__ == "__main__":
    F = Fr

    def chk(h, want, radd=False, bm=F(0)):
        r = faraid(h, radd)
        got = {k: sh for k, c, sh, b in r["rows"]}
        assert got == want and r["bm"] == bm, (h, got, r["bm"])
        assert sum(got.values(), F(0)) + r["bm"] == 1, h
    chk(dict(su=1, ib=1, bp=1), dict(su=F(1, 2), ib=F(1, 6), bp=F(1, 3)))
    chk(dict(**{"is": 1}, ib=1, bp=1), {"is": F(1, 4), "ib": F(1, 4), "bp": F(1, 2)})
    chk(dict(su=1, skp=2, ib=1), dict(su=F(3, 8), skp=F(4, 8), ib=F(1, 8)))
    chk(dict(su=1, ib=1, sil=1, sip=1, skl=1), dict(su=F(1, 2), ib=F(1, 6), sil=F(1, 9), sip=F(1, 9), skl=F(1, 9)))
    chk(dict(ap=1, skp=1), dict(ap=F(1, 2), skp=F(1, 2)))
    chk(dict(ap=1, cp=1, skl=1), dict(ap=F(1, 2), cp=F(1, 6), skl=F(1, 3)))
    chk(dict(ap=2, cp=1, cl=1), dict(ap=F(2, 3), cl=F(2, 9), cp=F(1, 9)))
    chk(dict(ap=2, cp=1), dict(ap=F(2, 3)), bm=F(1, 3))
    chk({"is": 1, "ib": 1}, {"is": F(1, 4), "ib": F(1, 3)}, bm=F(5, 12))
    chk({"is": 1, "ib": 1}, {"is": F(1, 4), "ib": F(3, 4)}, radd=True)
    chk(dict(su=1, ap=1), dict(su=F(1, 4), ap=F(1, 2)), bm=F(1, 4))
    chk(dict(su=1, ap=1), dict(su=F(1, 4), ap=F(3, 4)), radd=True)
    chk({"is": 1, "ap": 2, "ib": 1, "bp": 1}, {"is": F(3, 27), "ap": F(16, 27), "ib": F(4, 27), "bp": F(4, 27)})
    chk(dict(ib=1, bp=1, skl=2), dict(ib=F(1, 6), bp=F(5, 6)))
    chk(dict(skp=1, sbp=1), dict(skp=F(1, 2), sbp=F(1, 6)), bm=F(1, 3))
    chk(dict(bp=1, ap=1), dict(bp=F(1, 2), ap=F(1, 2)))
    chk(dict(ni=1, nb=1, al=1), dict(ni=F(1, 12), nb=F(1, 12), al=F(5, 6)))
    chk({"is": 1, "ib": 1, "bp": 1, "al": 2, "ap": 1}, {"is": F(1, 8), "ib": F(1, 6), "bp": F(1, 6), "al": F(13, 30), "ap": F(13, 120)})
    chk(dict(ap=1, skp=1, sbl=1), dict(ap=F(1, 2), skp=F(1, 2)))
    chk(dict(su=1, skp=1, sbp=1, sil=1), dict(su=F(3, 8), skp=F(3, 8), sbp=F(1, 8), sil=F(1, 8)))
    chk(dict(dt=1, ib=1), dict(dt=F(2, 3), ib=F(1, 3)))
    chk(dict(su=1, dt=1, ib=1), dict(su=F(1, 2), dt=F(1, 6), ib=F(1, 3)))
    chk(dict(bsk=2, spk=3), dict(bsk=F(1)))
    chk(dict(ask=1, sil=1), dict(sil=F(1, 6), ask=F(5, 6)))
    chk(dict(cp=1, sbp=1), dict(cp=F(1, 2), sbp=F(1, 2)))
    assert faraid(dict(dt=1, skl=1))["bad"] and not faraid(dict(bp=1, dt=1, skl=1))["bad"]
    print("faraid ok")
