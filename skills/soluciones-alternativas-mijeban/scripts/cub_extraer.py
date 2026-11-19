"""Extrae la planta de cubierta (presentación A-03) del DXF de PLANTAS ALZADOS Y SECCIONES a un JSON y una imagen."""
import sys, json
from collections import Counter
import ezdxf
from ezdxf import path as ezpath, bbox
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DXF, SAL_JSON, SAL_PNG = sys.argv[1:4]
doc = ezdxf.readfile(DXF)
msp = doc.modelspace()
CX, CY, H = 421673.8, 4412305.9, 44.7
X0, X1, Y0, Y1 = CX - 40, CX + 40, CY - H / 2 - 2, CY + H / 2 + 2
out, capas = [], Counter()
cache = bbox.Cache()
for e in msp:
    t = e.dxftype()
    if t in ("DIMENSION", "VIEWPORT", "IMAGE"):
        continue
    try:
        b = bbox.extents([e], fast=True, cache=cache)
    except Exception:
        continue
    if not b.has_data or b.extmax.x < X0 or b.extmin.x > X1 or b.extmax.y < Y0 or b.extmin.y > Y1:
        continue
    capas[(e.dxf.layer, t)] += 1
    if t in ("TEXT", "MTEXT"):
        p = e.dxf.insert
        out.append({"t": t, "capa": e.dxf.layer, "txt": e.dxf.text if t == "TEXT" else e.plain_text(), "p": [p.x, p.y]})
        continue
    ents = list(e.virtual_entities()) if t == "INSERT" else [e]
    for ve in ents:
        try:
            ps = ezpath.from_hatch(ve) if ve.dxftype() == "HATCH" else [ezpath.make_path(ve)]
        except Exception:
            continue
        for p in ps:
            pts = [(round(v.x, 4), round(v.y, 4)) for v in p.flattening(0.01)]
            if len(pts) >= 2:
                out.append({"t": ve.dxftype(), "capa": ve.dxf.layer if t != "INSERT" else e.dxf.layer + "|" + ve.dxf.layer,
                            "blk": e.dxf.name if t == "INSERT" else None, "pts": pts})
json.dump(out, open(SAL_JSON, "w", encoding="utf-8"))
for (c, t), n in sorted(capas.items()):
    print(f"{c:35s} {t:12s} {n}")
fig, ax = plt.subplots(figsize=(22, 13), dpi=110)
col = {"0_CERCHAS": "red", "ONDUTHERM": "tab:blue", "ALZ_TEJA": "tab:orange"}
for o in out:
    if "pts" in o:
        xs, ys = zip(*o["pts"])
        base = o["capa"].split("|")[0]
        ax.plot(xs, ys, lw=0.4 if base not in col else 0.7, color=col.get(base, "0.4"))
    else:
        ax.text(o["p"][0], o["p"][1], o["txt"][:25], fontsize=4, color="m")
ax.set_xlim(X0, X1); ax.set_ylim(Y0, Y1); ax.set_aspect("equal"); ax.grid(alpha=0.2)
fig.savefig(SAL_PNG, bbox_inches="tight")
