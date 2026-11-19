"""Vuelca las entidades de una zona del modelo con sus propiedades. Uso: ref_dump.py dxf x0 x1 y0 y1"""
import sys, ezdxf
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
X0, X1, Y0, Y1 = map(float, sys.argv[2:6])
cache = bbox.Cache()
for e in msp:
    b = bbox.extents([e], fast=True, cache=cache)
    if not b.has_data or b.extmax.x < X0 or b.extmin.x > X1 or b.extmax.y < Y0 or b.extmin.y > Y1:
        continue
    t = e.dxftype()
    base = f"{t:10s} L={e.dxf.layer} c={e.dxf.get('color')} lt={e.dxf.get('linetype')} lw={e.dxf.get('lineweight')} ltscale={e.dxf.get('ltscale')}"
    ext = f"x[{b.extmin.x:.4f},{b.extmax.x:.4f}] y[{b.extmin.y:.4f},{b.extmax.y:.4f}]"
    if t == 'HATCH':
        extra = f"pat={e.dxf.pattern_name} sc={e.dxf.get('pattern_scale')} ang={e.dxf.get('pattern_angle')} solid={e.dxf.solid_fill} tc={e.dxf.get('true_color')} bg={getattr(e,'bgcolor',None)}"
    elif t == 'CIRCLE':
        extra = f"c=({e.dxf.center.x:.4f},{e.dxf.center.y:.4f}) r={e.dxf.radius:.4f}"
    elif t == 'LWPOLYLINE':
        pts = [(round(p[0], 4), round(p[1], 4), round(p[4], 3)) for p in e.get_points()]
        extra = f"n={len(pts)} closed={e.closed} pts={pts[:14]}"
    elif t == 'INSERT':
        extra = f"blk={e.dxf.name} ins=({e.dxf.insert.x:.3f},{e.dxf.insert.y:.3f}) sc={e.dxf.xscale:.3f}"
    elif t == 'LINE':
        extra = f"({e.dxf.start.x:.4f},{e.dxf.start.y:.4f})-({e.dxf.end.x:.4f},{e.dxf.end.y:.4f})"
    else:
        extra = ''
    print(base, ext, extra)
