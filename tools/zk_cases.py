"""Random inputs + the Python output for each, for tools/test-alat.mjs to compare with alat.js (faraid, zakat simpanan/emas/perniagaan)."""
import json, random
import faraid as FR
import pages11 as P

rnd = random.Random(1447)
out = {"fr": [], "zs": [], "ze": [], "zb": []}
for _ in range(400):
    h = {}
    for k in FR.KEYS:
        if rnd.random() < 0.3:
            h[k] = 1 if FR.MAXN[k] == 1 else rnd.choice([1, 1, 2, 3, 5])
    if rnd.random() < 0.5:
        h.pop("su", None)
    else:
        h.pop("is", None)
    e = rnd.randrange(0, 5_000_000_00)
    radd = rnd.random() < 0.3
    out["fr"].append([h, e, radd, FR.faraid_html(h, e, radd)])
money = lambda: rnd.choice([0, 0, rnd.randrange(0, 200000), round(rnd.uniform(0, 90000), 2)])
for _ in range(60):
    i = dict(s="selangor", hy=rnd.choice("hm"), b=[money() for _ in range(5)], d=[money() / 10 for _ in range(5)], dv=rnd.random() < 0.7,
             ns=rnd.choice([38748, 33996, 40000.5]))
    out["zs"].append([i, P.zs_result(i)])
    j = dict(s=rnd.choice(list(P.URUF)), hy=rnd.choice("hm"), au=rnd.choice([455.86, 610.25, 500]), g=[rnd.choice([0, 50, 85, 120.5, 300]) for _ in range(3)],
             k=[rnd.choice([999, 916, 875, 750]) for _ in range(3)])
    j["g"][1] = rnd.choice([0, 100, 250, 900, 1000.25])
    out["ze"].append([j, P.ze_result(j)])
    b = dict(s="selangor", hy=rnd.choice("hm"), t=money(), st=money(), p=money(), a=money(), l=money(), x=money() / 5, m=rnd.choice([100, 51.5, 33.33, 0]),
             ns=38748)
    out["zb"].append([b, P.zb_result(b)])
print(json.dumps(out, ensure_ascii=False))
