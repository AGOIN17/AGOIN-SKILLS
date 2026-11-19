import sys, json
from shapely.geometry import Polygon, LineString
V = json.load(open(sys.argv[1], encoding="utf-8"))
iv = int(sys.argv[2]); X0, X1, Y0, Y1 = map(float, sys.argv[3:7])
OY = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
v = V[iv]
vert, hor = [], []
for e in v["ents"]:
    if e["l"] not in ("ALZ_FIN", "ALZ_GRU") or e["t"] in ("HATCH", "INSERT"):
        continue
    for g in e.get("g", []):
        for (xa, ya), (xb, yb) in zip(g, g[1:]):
            if not (X0 <= min(xa, xb) and max(xa, xb) <= X1 and Y0 <= min(ya, yb) and max(ya, yb) <= Y1):
                continue
            if abs(xa - xb) < 0.005 and abs(ya - yb) > 1.2:
                vert.append((round(xa, 3), round(min(ya, yb) - OY, 3), round(max(ya, yb) - OY, 3), e["l"]))
            if abs(ya - yb) < 0.005 and abs(xa - xb) > 1.5:
                hor.append((round(ya - OY, 3), round(min(xa, xb), 3), round(max(xa, xb), 3), e["l"]))
print("VERTICALES > 1,2 m (x, y0, y1):")
for t in sorted(set(vert)):
    print("  ", t)
print("HORIZONTALES > 1,5 m (y, x0, x1):")
for t in sorted(set(hor)):
    print("  ", t)
print("CARPINTERÍAS (polilíneas cerradas ALZ_CAR):")
car = []
for e in v["ents"]:
    if e["l"] == "ALZ_CAR" and e["t"] == "LWPOLYLINE" and e.get("closed"):
        g = e["g"][0]
        if len(g) >= 3:
            p = Polygon(g)
            b = p.bounds
            if X0 <= b[0] and b[2] <= X1 and Y0 <= b[1] and b[3] <= Y1:
                car.append((round(b[0], 3), round(b[1] - OY, 3), round(b[2], 3), round(b[3] - OY, 3), round(p.area, 3), e["h"]))
for c in sorted(car):
    print("  ", c, f"ancho {c[2]-c[0]:.3f} alto {c[3]-c[1]:.3f}")
print("TEXTOS:")
for e in v["ents"]:
    if e["t"] in ("TEXT", "MTEXT") and X0 <= e["p"][0] <= X1 and Y0 <= e["p"][1] <= Y1:
        print("  ", e["l"], round(e["p"][0], 2), round(e["p"][1] - OY, 2), repr(e["txt"][:40]))
