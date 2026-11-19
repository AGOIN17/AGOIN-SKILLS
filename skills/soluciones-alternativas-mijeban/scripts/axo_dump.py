"""Analiza la axonometría de la ficha 03 v4: qué hay, y dónde está la cara delantera del panel (en coordenadas 3D)."""
import sys, math, collections, ezdxf
from ezdxf import bbox, path as ezpath
from shapely.geometry import Polygon
from shapely.ops import unary_union
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
M = 0.268; C = math.cos(math.radians(30)); OX, OY = 0.032, -3.0875
VENT = (-0.2, 2.2, -3.9, -1.65)
cnt = collections.Counter(); polis = []
for e in msp:
    b = bbox.extents([e], fast=True)
    if not (b.has_data and VENT[0] < b.extmin.x and b.extmax.x < VENT[1] and VENT[2] < b.extmin.y and b.extmax.y < VENT[3]):
        continue
    col = e.dxf.get('true_color'); rgb = None
    if e.dxftype() == 'HATCH' and e.dxf.solid_fill:
        rgb = tuple(e.rgb) if e.rgb else None
    cnt[(e.dxftype(), e.dxf.layer, rgb)] += 1
    if e.dxf.layer not in ('A-AXO-COLOR',) or rgb in ((238, 238, 238), (230, 230, 230), (222, 222, 222), (224, 235, 231), (210, 226, 220), (195, 214, 208)):
        print(e.dxftype(), e.dxf.handle, e.dxf.layer, rgb, col, f"x[{b.extmin.x:.3f},{b.extmax.x:.3f}] y[{b.extmin.y:.3f},{b.extmax.y:.3f}]",
              (e.dxf.text if e.dxftype() == 'TEXT' else ''))
    if e.dxftype() == 'HATCH' and e.dxf.layer == 'A-AXO-COLOR' and rgb not in ((238, 238, 238), (230, 230, 230), (222, 222, 222), (224, 235, 231), (210, 226, 220), (195, 214, 208)):
        for p in ezpath.from_hatch(e):
            pts = [(v.x, v.y) for v in p.flattening(0.0005)]
            if len(pts) >= 3:
                g = Polygon(pts).buffer(0)
                if g.area > 1e-8:
                    polis.append((g, rgb, e.dxf.handle))
for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]):
    print(v, k)
# colores de los hatches A-AXO-COLOR por área
area = collections.Counter()
for g, rgb, h in polis:
    area[rgb] += g.area
print('areas por color', area.most_common(20))
U = unary_union([g for g, _, _ in polis])
print('silueta', U.bounds)
# vértices más bajos de la silueta
pts = list(U.exterior.coords) if U.geom_type == 'Polygon' else [c for p in U.geoms for c in p.exterior.coords]
pts.sort(key=lambda p: p[1])
for p in pts[:6]:
    sx, sy = p
    # suponiendo que el punto está en la cara inferior del panel (Z = 0,074 + M·Y)
    s = (sx - OX) / C; r = sy - OY - 0.074
    # X + Y = s ; -0.5 X + (0.5 + M) Y = r
    Y = (r + 0.5 * s) / (1 + M); X = s - Y
    print(f"punto bajo ({sx:.4f},{sy:.4f}) -> X {X:.3f} Y {Y:.3f}")
pts.sort(key=lambda p: p[0])
for p in pts[:4]:
    print('izq', p)
