"""Compara la definición guardada de las tramas (espaciado real de líneas) entre la referencia y la ficha."""
import sys, math, ezdxf
from ezdxf import bbox
def info(path, x0, x1, y0, y1, nombres):
    doc = ezdxf.readfile(path)
    print(path, 'MEASUREMENT', doc.header.get('$MEASUREMENT'))
    vistos = set()
    for e in doc.modelspace().query('HATCH'):
        if e.dxf.pattern_name not in nombres or e.dxf.pattern_name in vistos:
            continue
        b = bbox.extents([e], fast=True)
        if not b.has_data or b.extmax.x < x0 or b.extmin.x > x1 or b.extmax.y < y0 or b.extmin.y > y1:
            continue
        vistos.add(e.dxf.pattern_name)
        pl = e.pattern.lines if e.pattern else []
        sp = [round(math.hypot(*l.offset), 5) for l in pl]
        print('  ', e.dxf.pattern_name, 'sc', e.dxf.pattern_scale, 'n_lineas', len(pl), 'desfase entre líneas', sp[:4], 'trazos', [ [round(d, 5) for d in l.dash_length_items][:4] for l in pl][:2])
nom = {'HEX', 'HONEY', 'AR-SAND', 'AR-CONC', 'ANSI34'}
info(sys.argv[1], 113.9, 117.2, -57.96, -57.3, nom)
info(sys.argv[2], -0.1, 0.4, -0.2, 0.3, nom)
