import json, sys
from shapely.geometry import Polygon
V = json.load(open(sys.argv[1], encoding="utf-8"))
v = [x for x in V if x["hoja"] == "A-02"][0]
OX, OY = 421600, 4412200
vist = set()
for e in v["ents"]:
    if e["t"] == "LWPOLYLINE" and e.get("closed"):
        g = e["g"][0]
        if len(g) >= 4:
            p = Polygon(g)
            if p.area > 15:
                b = p.bounds
                k = (e["l"], tuple(round(x, 2) for x in b))
                if k in vist:
                    continue
                vist.add(k)
                print(f"{e['l']:12s} x {b[0]-OX:7.3f}-{b[2]-OX:7.3f} ({b[2]-b[0]:6.3f})  y {b[1]-OY:7.3f}-{b[3]-OY:7.3f} ({b[3]-b[1]:6.3f})  area {p.area:6.1f}  vert {len(g)}")
ls = set()
for e in v["ents"]:
    if e["l"] in ("0", "0_AUX") and e["t"] in ("LINE", "LWPOLYLINE") and not e.get("closed"):
        for g in e["g"]:
            for (xa, ya), (xb, yb) in zip(g, g[1:]):
                L = ((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5
                if L > 4 and (abs(xa - xb) < 0.01 or abs(ya - yb) < 0.01):
                    ls.add((round(min(xa, xb) - OX, 3), round(min(ya, yb) - OY, 3), round(max(xa, xb) - OX, 3), round(max(ya, yb) - OY, 3), round(L, 2), e["l"]))
print("lineas largas (capa 0):", len(ls))
for l in sorted(ls):
    print("  ", l)
