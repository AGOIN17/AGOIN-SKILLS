import sys, json
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union
V = json.load(open(sys.argv[1], encoding="utf-8"))
v = [x for x in V if x["hoja"] == "A-02"][0]
polys = []
for e in v["ents"]:
    if e["t"] == "HATCH" and e["l"] in ("0_TRM", "0_PILARES"):
        for g in e["g"]:
            if len(g) >= 3:
                p = Polygon(g).buffer(0)
                if p.area > 0.002:
                    polys.append(p)
    if e["t"] == "LWPOLYLINE" and e.get("closed") and e["l"] in ("0_GRU", "0_PILARES"):
        g = e["g"][0]
        if len(g) >= 3:
            p = Polygon(g).buffer(0)
            if 0.002 < p.area < 30:
                polys.append(p)
muros = unary_union(polys)
grupos = unary_union([p.buffer(0.25) for p in polys])
print("polígonos de muro:", len(polys), "área muros", round(muros.area, 1))
OX, OY = 421600, 4412200
res = []
for g in sorted(getattr(grupos, "geoms", [grupos]), key=lambda g: g.bounds[0]):
    if g.area < 1.5:
        continue
    m = muros.intersection(g)
    x0, y0, x1, y1 = m.bounds
    res.append((x0, y0, x1, y1, m.area))
    print(f"grupo  x {x0-OX:7.3f}–{x1-OX:7.3f} ({x1-x0:6.3f})   y {y0-OY:7.3f}–{y1-OY:7.3f} ({y1-y0:6.3f})   muro {m.area:5.1f} m²")
json.dump(res, open(sys.argv[2], "w"))
