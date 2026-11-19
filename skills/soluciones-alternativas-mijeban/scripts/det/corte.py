import sys, ezdxf
from ezdxf import path as ezp
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
X0, X1 = 421707.9, 421709.2
for Y in (4412054.0, 4412055.0, 4412055.8):
    cortes = []
    for e in msp:
        if e.dxftype() not in ('LINE', 'LWPOLYLINE', 'POLYLINE', 'HATCH'): continue
        try:
            ps = [ezp.make_path(e)] if e.dxftype() != 'HATCH' else list(ezp.from_hatch(e))
        except Exception:
            continue
        for p in ps:
            v = list(p.flattening(0.001))
            for a, b in zip(v, v[1:]):
                if (a.y - Y) * (b.y - Y) < 0 or (abs(a.y - Y) < 1e-9 and abs(b.y - Y) > 1e-9):
                    if abs(b.y - a.y) < 1e-12: continue
                    x = a.x + (Y - a.y) * (b.x - a.x) / (b.y - a.y)
                    if X0 < x < X1 and abs(b.y - a.y) > 0.3:
                        cortes.append((round(x, 4), e.dxf.layer, e.dxftype()))
    xs = sorted(set((c[0], c[1]) for c in cortes))
    print('Y =', Y)
    prev = None
    for x, l in xs:
        print(f'  x {x:.4f}  +{(x - prev) * 1000 if prev else 0:6.1f} mm  {l}')
        prev = x
