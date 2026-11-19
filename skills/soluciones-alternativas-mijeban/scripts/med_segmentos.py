import sys, json
from collections import defaultdict
V = json.load(open(sys.argv[1], encoding="utf-8"))
v = V[int(sys.argv[2])]
X0, X1, Y0, Y1, OX, OY = map(float, sys.argv[3:9])
LMIN = float(sys.argv[9]) if len(sys.argv) > 9 else 0.8
segs = set()
for e in v["ents"]:
    if e["l"] in ("ALZ_TRM_Lajas", "ALZ_TEJA", "ALZ_CAR_CRS") or e["t"] in ("INSERT", "TEXT", "MTEXT"):
        continue
    if e["t"] == "HATCH" and e.get("pat") != "SOLID":
        pass
    for g in e.get("g", []):
        for (xa, ya), (xb, yb) in zip(g, g[1:]):
            xa_, xb_, ya_, yb_ = xa - OX, xb - OX, ya - OY, yb - OY
            if min(xa_, xb_) < X0 or max(xa_, xb_) > X1 or min(ya_, yb_) < Y0 or max(ya_, yb_) > Y1:
                continue
            L = ((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5
            if L >= LMIN:
                segs.add((e["l"], e["t"], round(xa_, 3), round(ya_, 3), round(xb_, 3), round(yb_, 3), round(L, 2)))
for s in sorted(segs, key=lambda s: (s[0], min(s[2], s[4]), min(s[3], s[5]))):
    print(s)
