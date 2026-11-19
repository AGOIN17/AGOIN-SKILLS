"""Vuelca las entidades del modelo dentro de una caja (x0 x1 y0 y1): tipo, capa, color, trama, grosor, extensión.
Uso: python sec_dump.py archivo.dxf x0 x1 y0 y1"""
import sys, collections, ezdxf
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
x0, x1, y0, y1 = map(float, sys.argv[2:6])
n = collections.Counter()
for e in msp:
    b = bbox.extents([e], fast=True)
    if not b.has_data or b.extmin.x < x0 or b.extmax.x > x1 or b.extmin.y < y0 or b.extmax.y > y1:
        continue
    t = e.dxftype(); n[(t, e.dxf.layer)] += 1
    extra = ''
    if t == 'HATCH':
        extra = f"pat={e.dxf.pattern_name} solid={e.dxf.solid_fill} sc={e.dxf.get('pattern_scale')} ang={e.dxf.get('pattern_angle')}"
        if e.dxf.solid_fill:
            extra += f" rgb={e.rgb if hasattr(e, 'rgb') else ''}"
    elif t in ('TEXT', 'MTEXT'):
        hh = e.dxf.height if t == 'TEXT' else e.dxf.char_height
        extra = f"txt={(e.dxf.text if t == 'TEXT' else e.text)[:40]!r} h={hh} st={e.dxf.style}"
    elif t == 'LWPOLYLINE':
        extra = f"n={len(e)} closed={e.closed} lt={e.dxf.get('linetype')} ltsc={e.dxf.get('ltscale')}"
    print(f"{t:10s} {e.dxf.handle:>4s} {e.dxf.layer:14s} c={e.dxf.get('color')} tc={e.dxf.get('true_color')} lw={e.dxf.get('lineweight')} "
          f"x[{b.extmin.x:.3f},{b.extmax.x:.3f}] y[{b.extmin.y:.3f},{b.extmax.y:.3f}] {extra}")
print(n)
for lay in doc.layers:
    print('CAPA', lay.dxf.name, 'color', lay.dxf.color, 'tc', lay.dxf.get('true_color'), 'lw', lay.dxf.get('lineweight'), 'lt', lay.dxf.get('linetype'))
