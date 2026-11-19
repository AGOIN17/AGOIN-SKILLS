"""Inspección de la ficha 02 B v3: ventanas, y contenido del modelo agrupado por capa, tipo y color."""
import sys, collections, ezdxf
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace(); ps = doc.layouts.get('FICHA-A4')
for v in ps.query('VIEWPORT'):
    print('VP', v.dxf.handle, 'centro papel', tuple(round(c, 2) for c in v.dxf.center), 'w', round(v.dxf.width, 2), 'h', round(v.dxf.height, 2),
          'vista', tuple(round(c, 4) for c in v.dxf.view_center_point), 'alto vista', round(v.dxf.view_height, 4))
g = collections.defaultdict(list)
for e in msp:
    b = bbox.extents([e], fast=True)
    rgb = None
    if e.dxftype() == 'HATCH':
        rgb = (tuple(e.rgb) if e.rgb else None, e.dxf.pattern_name if not e.dxf.solid_fill else 'SOLID')
    elif e.dxf.hasattr('true_color'):
        rgb = e.rgb
    g[(e.dxf.layer, e.dxftype(), str(rgb), e.dxf.get('color'))].append(b)
for k, bs in sorted(g.items()):
    xs = [b.extmin.x for b in bs if b.has_data] + [b.extmax.x for b in bs if b.has_data]
    ys = [b.extmin.y for b in bs if b.has_data] + [b.extmax.y for b in bs if b.has_data]
    print(len(bs), k, f"x[{min(xs):.3f},{max(xs):.3f}] y[{min(ys):.3f},{max(ys):.3f}]" if xs else '')
