import sys, ezdxf
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
for e in msp:
    h = int(e.dxf.handle, 16)
    if h >= 0x523 or e.dxf.layer == 'A-AXO-VERDE' or (e.dxftype() == 'TEXT' and '1,20' in e.dxf.text):
        b = bbox.extents([e], fast=True)
        rgb = tuple(e.rgb) if e.dxftype() == 'HATCH' and e.dxf.solid_fill and e.rgb else None
        extra = e.dxf.text if e.dxftype() == 'TEXT' else ''
        print(e.dxftype(), e.dxf.handle, e.dxf.layer, rgb, e.dxf.get('true_color'), e.dxf.get('lineweight'), f"x[{b.extmin.x:.3f},{b.extmax.x:.3f}] y[{b.extmin.y:.3f},{b.extmax.y:.3f}]", extra)
