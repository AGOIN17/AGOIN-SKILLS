"""Piedra visible en una vista = zona de las piezas de piedra − rellenos sólidos que la tapan (fachadas, terreno, vidrio)."""
import sys, json
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union
V = json.load(open(sys.argv[1], encoding="utf-8"))
iv = int(sys.argv[2]); Y515 = float(sys.argv[3])
v = V[iv]
piezas, mascaras = [], []
for e in v["ents"]:
    if e["l"] == "ALZ_TRM_Lajas":
        for g in e.get("g", []):
            if len(g) >= 2:
                piezas.append(LineString(g))
    elif e["t"] == "HATCH":
        for g in e.get("g", []):
            if len(g) >= 3:
                p = Polygon(g).buffer(0)
                if p.area > 0.05 and (e.get("pat") == "SOLID" or e["l"].startswith("ALZ_TRM")):
                    mascaras.append((e["l"], e.get("pat"), p))
piedra = unary_union([p.buffer(0.10) for p in piezas]).buffer(-0.07)
tapa = unary_union([p for _, _, p in mascaras])
visible = piedra.difference(tapa)
print(f"vista {iv}: piedra bruta {piedra.area:.1f} m²; tapada {piedra.intersection(tapa).area:.1f}; visible {visible.area:.1f} m²")
from collections import Counter
print("  máscaras:", Counter((l, p) for l, p, _ in mascaras).most_common(8))
for g in sorted(getattr(visible, "geoms", [visible]), key=lambda g: g.bounds[0]):
    if g.area < 0.3:
        continue
    x0, y0, x1, y1 = g.bounds
    print(f"   x {x0:.2f}-{x1:.2f}  y {y0 - Y515:+.2f} a {y1 - Y515:+.2f}  área {g.area:6.2f}")
json.dump([list(g.exterior.coords) for g in getattr(visible, "geoms", [visible]) if g.area >= 0.3],
          open(sys.argv[4], "w"))
