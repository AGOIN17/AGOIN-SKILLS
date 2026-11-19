"""Dibuja una zona de un DXF con colores ACI y tramas (aprox). Uso: ver_ref.py dxf x0 x1 y0 y1 salida.png [dpi]"""
import sys, ezdxf, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ezdxf import path as ezpath, bbox
from ezdxf.colors import aci2rgb
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
X0, X1, Y0, Y1 = map(float, sys.argv[2:6])
dpi = int(sys.argv[7]) if len(sys.argv) > 7 else 120
w = 14; h = w * (Y1 - Y0) / (X1 - X0)
fig, ax = plt.subplots(figsize=(w, max(h, 2)), dpi=dpi)
cache = bbox.Cache()

def col(e):
    c = e.dxf.color
    if c in (256, 0) or c is None:
        lay = doc.layers.get(e.dxf.layer) if doc.layers.has_entry(e.dxf.layer) else None
        c = lay.color if lay else 7
    if c == 7 or c < 1 or c > 255:
        return (0, 0, 0)
    r, g, b = aci2rgb(c)
    return (r / 255, g / 255, b / 255)

for e in msp:
    if e.dxftype() in ('TEXT', 'MTEXT', 'DIMENSION'):
        continue
    b = bbox.extents([e], fast=True, cache=cache)
    if not b.has_data or b.extmax.x < X0 or b.extmin.x > X1 or b.extmax.y < Y0 or b.extmin.y > Y1:
        continue
    try:
        ents = list(e.virtual_entities()) if e.dxftype() == 'INSERT' else [e]
    except Exception:
        continue
    for ve in ents:
        try:
            if ve.dxftype() == 'HATCH':
                ps = ezpath.from_hatch(ve)
                for p in ps:
                    pts = list(p.flattening(0.0005))
                    if len(pts) > 2:
                        ax.fill([v.x for v in pts], [v.y for v in pts], alpha=0.25, color=col(ve), lw=0)
                        ax.text(sum(v.x for v in pts)/len(pts), sum(v.y for v in pts)/len(pts), ve.dxf.pattern_name, fontsize=4, color='b')
                continue
            p = ezpath.make_path(ve)
        except Exception:
            continue
        pts = list(p.flattening(0.0005))
        if len(pts) < 2:
            continue
        ax.plot([v.x for v in pts], [v.y for v in pts], lw=0.4, color=col(ve))
ax.set_xlim(X0, X1); ax.set_ylim(Y0, Y1); ax.set_aspect('equal'); ax.grid(alpha=0.2)
fig.savefig(sys.argv[6], bbox_inches='tight')
