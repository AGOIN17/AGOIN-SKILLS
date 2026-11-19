import sys, ezdxf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ezdxf import path as ezpath, bbox
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
X0, X1, Y0, Y1 = map(float, sys.argv[2:6])
fig, ax = plt.subplots(figsize=(16, 11), dpi=110)
cache = bbox.Cache()
for e in msp:
    if e.dxftype() in ("TEXT", "MTEXT", "DIMENSION"):
        if e.dxftype() in ("TEXT", "MTEXT"):
            p = e.dxf.insert
            if X0 <= p.x <= X1 and Y0 <= p.y <= Y1:
                ax.text(p.x, p.y, (e.dxf.text if e.dxftype() == "TEXT" else e.plain_text())[:40], fontsize=5, color="m")
        continue
    b = bbox.extents([e], fast=True, cache=cache)
    if not b.has_data or b.extmax.x < X0 or b.extmin.x > X1 or b.extmax.y < Y0 or b.extmin.y > Y1:
        continue
    ents = list(e.virtual_entities()) if e.dxftype() == "INSERT" else [e]
    for ve in ents:
        try:
            ps = ezpath.from_hatch(ve) if ve.dxftype() == "HATCH" else [ezpath.make_path(ve)]
        except Exception:
            continue
        for p in ps:
            pts = list(p.flattening(0.002))
            if len(pts) < 2:
                continue
            xs = [v.x for v in pts]; ys = [v.y for v in pts]
            if ve.dxftype() == "HATCH":
                ax.fill(xs, ys, alpha=0.15, color="tab:orange", lw=0)
            else:
                ax.plot(xs, ys, lw=0.5, color="k")
ax.set_xlim(X0, X1); ax.set_ylim(Y0, Y1); ax.set_aspect("equal"); ax.grid(alpha=0.3)
fig.savefig(sys.argv[6], bbox_inches="tight")
