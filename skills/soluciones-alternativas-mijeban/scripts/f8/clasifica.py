"""Clasifica los sombreados y líneas de la axonometría v3 por capa y cara (cajas 3D deducidas de A-AXO-LIN)."""
import sys, math, collections, ezdxf
from ezdxf import path as ezpath
from shapely.geometry import Polygon, Point
C = math.cos(math.radians(30)); O = (0.0, -1.7)
P = lambda X, Y, Z: (O[0] + C * (X + Y), O[1] - 0.5 * X + 0.5 * Y + Z)
CAPAS = {  # n: (X1, Y0, Y1, Z1)
    6: (0.12, 0.0, 0.015, 0.12), 5: (0.257, 0.015, 0.248, 0.308), 4: (0.31, 0.248, 0.263, 0.35),
    3: (0.37, 0.263, 0.363, 0.40), 2: (0.43, 0.363, 0.430, 0.42), 1: (0.47, 0.430, 0.445, 0.47)}
def caras(n):
    X1, Y0, Y1, Z1 = CAPAS[n]
    return {'frente': Polygon([P(0, Y0, 0), P(X1, Y0, 0), P(X1, Y0, Z1), P(0, Y0, Z1)]),
            'arriba': Polygon([P(0, Y0, Z1), P(X1, Y0, Z1), P(X1, Y1, Z1), P(0, Y1, Z1)]),
            'testa': Polygon([P(X1, Y0, 0), P(X1, Y1, 0), P(X1, Y1, Z1), P(X1, Y0, Z1)])}
ORDEN = [6, 5, 4, 3, 2, 1]  # de delante a atrás
def donde(pt):
    for n in ORDEN:
        for k, g in caras(n).items():
            if g.buffer(-1e-5).contains(Point(pt)):
                return (n, k)
    for n in ORDEN:
        for k, g in caras(n).items():
            if g.buffer(1e-4).contains(Point(pt)):
                return (n, k)
    return None
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
res = collections.defaultdict(collections.Counter)
for e in msp:
    if e.dxf.layer not in ('A-AXO-COLOR', 'A-AXO-DET', 'A-AXO-LIN'):
        continue
    if e.dxftype() == 'HATCH':
        for p in ezpath.from_hatch(e):
            pts = [(v.x, v.y) for v in p.flattening(0.0005)]
            break
        g = Polygon(pts).buffer(0)
        c = g.representative_point()
        key = ('H', e.dxf.pattern_name if not e.dxf.solid_fill else 'S', e.dxf.get('pattern_scale'), tuple(e.rgb) if e.rgb else None)
        a = g.area
    else:
        pts = [p[:2] for p in e.get_points()]
        from shapely.geometry import LineString
        c = LineString(pts).interpolate(0.5, normalized=True) if len(pts) > 1 else Point(pts[0])
        key = ('L', e.dxf.layer, e.dxf.get('lineweight'), e.dxf.get('true_color'), e.dxf.get('color'))
        a = 1
    res[donde((c.x, c.y))][key] += 1
for k in sorted(res, key=lambda k: (k is None, k)):
    print(k)
    for kk, v in res[k].most_common():
        print('   ', v, kk)
