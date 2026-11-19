"""Dónde hay piedra en cada vista: unión de las piezas (bloques en ALZ_TRM_Lajas), por encima y por debajo de 515,00."""
import sys, json, re
from shapely.geometry import box, LineString, MultiLineString
from shapely.ops import unary_union
V = json.load(open(sys.argv[1], encoding="utf-8"))
nombres = ["W1", "W2", "1E", "2E", "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S"]
for i, v in enumerate(V):
    y515 = None
    for e in v["ents"]:
        if e["t"] in ("TEXT", "MTEXT") and e["txt"].strip().startswith("515"):
            y515 = e["p"][1] - 0.222       # el texto va 0,22 por encima de la línea de nivel
            break
    piezas = []
    for e in v["ents"]:
        if e["l"] == "ALZ_TRM_Lajas":
            for g in e.get("g", []):
                if len(g) >= 2:
                    piezas.append(LineString(g))
    if not piezas:
        print(f"{nombres[i]:3s} sin piedra"); continue
    zona = unary_union([p.buffer(0.12) for p in piezas]).buffer(-0.08)
    print(f"{nombres[i]:3s} nivel 515 en y={y515:.3f}" if y515 else f"{nombres[i]:3s} sin cota 515")
    for g in sorted(getattr(zona, "geoms", [zona]), key=lambda g: g.bounds[0]):
        if g.area < 0.5:
            continue
        x0, y0, x1, y1 = g.bounds
        rel = f"de {y0 - y515:+.2f} a {y1 - y515:+.2f} m sobre 515" if y515 else ""
        print(f"     x {x0:.2f}–{x1:.2f} ({x1-x0:5.2f} m)  {rel}  área bruta {g.area:6.1f} m²")
