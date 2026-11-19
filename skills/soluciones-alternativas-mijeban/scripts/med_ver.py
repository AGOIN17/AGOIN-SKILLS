import sys, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
V = json.load(open(sys.argv[1], encoding="utf-8"))
iv = int(sys.argv[2]); out = sys.argv[3]
x0r = float(sys.argv[4]) if len(sys.argv) > 4 else None
x1r = float(sys.argv[5]) if len(sys.argv) > 5 else None
v = V[iv]
col = {"ALZ_FIN": "0.35", "ALZ_GRU": "k", "ALZ_CAR": "tab:blue", "ALZ_CAR_CRS": "lightblue", "ALZ_TRM_Lajas": "saddlebrown",
       "ALZ_TRM": "tab:orange", "ALZ_TEJA": "tab:red", "ALZ_AUX": "tab:purple", "ALZ_OCULTAS": "0.7"}
fig, ax = plt.subplots(figsize=(30, 8), dpi=110)
cerradas = []
for e in v["ents"]:
    c = col.get(e["l"], "0.8")
    for g in e.get("g", []):
        if len(g) < 2:
            continue
        xs, ys = zip(*g)
        if x0r is not None and (max(xs) < x0r or min(xs) > x1r):
            continue
        if e["t"] == "HATCH":
            ax.fill(xs, ys, color=c, alpha=0.25, lw=0)
        else:
            ax.plot(xs, ys, color=c, lw=0.5 if e["l"] != "ALZ_GRU" else 1.4)
    if e["t"] == "LWPOLYLINE" and e.get("closed") and e["l"] == "ALZ_FIN":
        g = e["g"][0]
        if len(g) >= 3:
            p = Polygon(g)
            if p.area > 0.5:
                cerradas.append((e["h"], round(p.area, 2), [round(a, 2) for a in p.bounds]))
                xs, ys = zip(*g)
                ax.fill(xs, ys, color="tab:green", alpha=0.18, lw=0)
    if e["t"] in ("TEXT", "MTEXT") and e["l"] in ("0_TXT", "ALZ_COT", "0_AUX", "ALZ_FIN", "TEXTO", "0"):
        ax.text(e["p"][0], e["p"][1], e["txt"][:20], fontsize=5, color="m")
if x0r is not None:
    ax.set_xlim(x0r, x1r)
ax.set_aspect("equal")
fig.savefig(out, bbox_inches="tight")
print("cerradas ALZ_FIN > 0,5 m²:", len(cerradas))
for c in sorted(cerradas, key=lambda c: -c[1])[:40]:
    print("  ", c)
