"""Vuelca el espacio papel de la presentación FICHA-A4 (textos, ventanas, bloques) y el resumen del modelo."""
import sys, collections, ezdxf
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1])
lay = doc.layouts.get('FICHA-A4')
for e in lay:
    t = e.dxftype()
    h = e.dxf.handle
    if t == 'MTEXT':
        p = e.dxf.insert
        print(f"MTEXT {h} ({p.x:.1f},{p.y:.1f}) ch={e.dxf.char_height:.2f} w={e.dxf.get('width',0):.1f} st={e.dxf.style} c={e.dxf.get('color')} tc={e.dxf.get('true_color')} | {e.text[:160]!r}")
    elif t == 'TEXT':
        p = e.dxf.insert
        print(f"TEXT {h} ({p.x:.1f},{p.y:.1f}) h={e.dxf.height:.2f} | {e.dxf.text[:80]!r}")
    elif t == 'VIEWPORT':
        c = e.dxf.center; vc = e.dxf.view_center_point
        print(f"VIEWPORT {h} id={e.dxf.id} centro=({c.x:.1f},{c.y:.1f}) tam=({e.dxf.width:.1f}x{e.dxf.height:.1f}) vista=({vc.x:.3f},{vc.y:.3f}) alto_vista={e.dxf.view_height:.4f} escala=1:{e.dxf.view_height/e.dxf.height*1000 if e.dxf.height else 0:.2f} lock={e.dxf.get('flags')}")
    elif t == 'INSERT':
        print(f"INSERT {h} {e.dxf.name} ({e.dxf.insert.x:.1f},{e.dxf.insert.y:.1f})")
    else:
        try:
            b = bbox.extents([e], fast=True)
            print(f"{t} {h} L={e.dxf.layer} c={e.dxf.get('color')} tc={e.dxf.get('true_color')} x[{b.extmin.x:.1f},{b.extmax.x:.1f}] y[{b.extmin.y:.1f},{b.extmax.y:.1f}]")
        except Exception:
            print(t, h)
print('--- modelo')
msp = doc.modelspace()
print(collections.Counter((e.dxftype(), e.dxf.layer) for e in msp).most_common(40))
print('estilos', [s.dxf.name for s in doc.styles], 'capas', [l.dxf.name for l in doc.layers])
