import sys, ezdxf, collections
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
X0, X1, Y0, Y1 = 421708.2, 421708.9, 4412054.6, 4412055.8
g = collections.defaultdict(list)
for e in msp:
    b = bbox.extents([e], fast=True)
    if not b.has_data: continue
    if b.extmax.x < X0 or b.extmin.x > X1 or b.extmax.y < Y0 or b.extmin.y > Y1: continue
    if b.extmax.x - b.extmin.x > 0.6: continue
    col = e.dxf.get('color', 256)
    g[(e.dxf.layer, e.dxftype(), col)].append((b.extmin.x, b.extmax.x))
for k, v in sorted(g.items(), key=lambda kv: min(a for a, _ in kv[1])):
    lo = min(a for a, _ in v); hi = max(b for _, b in v)
    print(f'{k[0]:22s} {k[1]:10s} col {k[2]:3d}  n {len(v):4d}  x {lo-421708:.4f} .. {hi-421708:.4f}  ancho {(hi-lo)*1000:6.1f} mm')
