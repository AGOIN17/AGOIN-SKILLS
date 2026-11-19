"""Vuelca los textos de la presentación FICHA-A4 y las entidades de números de la ficha 02 B v3."""
import sys, ezdxf
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace(); ps = doc.layouts.get('FICHA-A4')
for e in ps:
    t = e.dxftype()
    if t in ('MTEXT', 'TEXT'):
        txt = e.text if t == 'MTEXT' else e.dxf.text
        ins = e.dxf.insert
        extra = f" w={e.dxf.get('width')} h={e.dxf.get('char_height') if t=='MTEXT' else e.dxf.height} st={e.dxf.style} lsf={e.dxf.get('line_spacing_factor')}"
        print(f"{t} {e.dxf.handle} L={e.dxf.layer} ({ins.x:.2f},{ins.y:.2f}){extra}\n   {txt!r}")
    else:
        b = bbox.extents([e], fast=True)
        if b.has_data:
            print(f"{t} {e.dxf.handle} L={e.dxf.layer} x[{b.extmin.x:.1f},{b.extmax.x:.1f}] y[{b.extmin.y:.1f},{b.extmax.y:.1f}]")
print('=== A-NUMEROS en el modelo')
for e in msp.query('*[layer=="A-NUMEROS"]'):
    b = bbox.extents([e], fast=True)
    s = f"{e.dxftype()} {e.dxf.handle} x[{b.extmin.x:.4f},{b.extmax.x:.4f}] y[{b.extmin.y:.4f},{b.extmax.y:.4f}]"
    if e.dxftype() == 'TEXT':
        s += f" '{e.dxf.text}' h={e.dxf.height} st={e.dxf.style}"
    if e.dxftype() == 'LWPOLYLINE':
        s += f" pts={[tuple(round(v, 4) for v in p[:2]) for p in e.get_points()]} lw={e.dxf.get('lineweight')}"
    print(s)
