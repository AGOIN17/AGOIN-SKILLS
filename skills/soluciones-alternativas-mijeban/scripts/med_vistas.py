import sys, ezdxf, pickle
from ezdxf import bbox
from collections import Counter, defaultdict
doc = ezdxf.readfile(sys.argv[1])
msp = doc.modelspace()
vistas = []
for l in doc.layouts:
    if not l.name.startswith("A-0") or l.name.startswith(("A-01", "A-02", "A-03")):
        continue
    for v in l.query("VIEWPORT"):
        if abs(v.dxf.view_center_point.x) > 1e6 or v.dxf.height / max(v.dxf.view_height, 1e-9) > 0.9:
            continue
        w = v.dxf.view_height * v.dxf.width / v.dxf.height
        c = v.dxf.view_center_point
        vistas.append((l.name, c.x - w / 2, c.y - v.dxf.view_height / 2, c.x + w / 2, c.y + v.dxf.view_height / 2))
print(len(vistas), "vistas de alzado-sección")
caches = {}
cache = bbox.Cache()
ents = [(e, bbox.extents([e], fast=True, cache=cache)) for e in msp if e.dxftype() not in ("DIMENSION",)]
for nom, x0, y0, x1, y1 in vistas:
    dentro = [e for e, b in ents if b.has_data and b.extmin.x >= x0 - 0.5 and b.extmax.x <= x1 + 0.5 and b.extmin.y >= y0 - 0.5 and b.extmax.y <= y1 + 0.5]
    t = [e for e in dentro if e.dxftype() in ("TEXT", "MTEXT")]
    tit = [(e.dxf.text if e.dxftype() == "TEXT" else e.plain_text())[:30] for e in t if "SECCI" in (e.dxf.text if e.dxftype() == "TEXT" else e.plain_text()).upper()]
    print(f"\n## {nom}  x {x0:.1f}..{x1:.1f}  y {y0:.1f}..{y1:.1f}  ({x1-x0:.1f} x {y1-y0:.1f} m)  {len(dentro)} ent.  títulos {tit}")
    c = defaultdict(Counter)
    for e in dentro:
        c[e.dxf.layer][e.dxftype()] += 1
    for k in ("ALZ_GRU", "ALZ_FIN", "ALZ_TRM", "ALZ_TRM_Lajas", "ALZ_CAR", "ALZ_CAR_CRS", "ALZ_CAR_AUX", "ALZ_TEJA", "ALZ_AUX", "ALZ_OCULTAS"):
        if c.get(k):
            print(f"   {k:15s} {dict(c[k])}")
    h = Counter()
    for e in dentro:
        if e.dxftype() == "HATCH":
            h[(e.dxf.layer, e.dxf.pattern_name)] += 1
    print("   tramas:", dict(h.most_common(12)))
    cerr = [e for e in dentro if e.dxftype() == "LWPOLYLINE" and e.closed and e.dxf.layer in ("ALZ_CAR", "ALZ_GRU", "ALZ_FIN")]
    print("   polilíneas cerradas (CAR/GRU/FIN):", Counter(e.dxf.layer for e in cerr))
