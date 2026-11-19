import sys, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
V = json.load(open(sys.argv[1], encoding="utf-8"))
iv = int(sys.argv[2]); x0, x1, y0, y1 = map(float, sys.argv[3:7]); out = sys.argv[7]
v = V[iv]
col = {"ALZ_FIN": ("0.35", 0.5), "ALZ_GRU": ("k", 1.2), "ALZ_CAR": ("tab:blue", 0.5), "ALZ_TRM": ("tab:orange", 0.4),
       "ALZ_TRM_Lajas": ("saddlebrown", 0.3), "ALZ_TEJA": ("tab:red", 0.4), "ALZ_AUX": ("tab:purple", 0.4), "ALZ_OCULTAS": ("0.7", 0.4)}
fig, ax = plt.subplots(figsize=(18, 9), dpi=110)
for e in v["ents"]:
    if e["l"] not in col:
        continue
    c, lw = col[e["l"]]
    for g in e.get("g", []):
        if len(g) < 2:
            continue
        xs, ys = zip(*g)
        if max(xs) < x0 or min(xs) > x1 or max(ys) < y0 or min(ys) > y1:
            continue
        if e["t"] == "HATCH":
            ax.fill(xs, ys, color=c, alpha=0.3, lw=0)
        else:
            ax.plot(xs, ys, color=c, lw=lw)
for e in v["ents"]:
    if e["t"] in ("TEXT", "MTEXT") and x0 <= e["p"][0] <= x1 and y0 <= e["p"][1] <= y1:
        ax.text(e["p"][0], e["p"][1], e["txt"][:16], fontsize=7, color="m")
ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax.set_yticks([round(y0 + i * 0.25, 2) for i in range(int((y1 - y0) / 0.25) + 1)])
ax.tick_params(labelsize=6)
fig.savefig(out, bbox_inches="tight")
# niveles escritos
for e in v["ents"]:
    if e["t"] in ("TEXT", "MTEXT") and x0 <= e["p"][0] <= x1 and y0 <= e["p"][1] <= y1 and any(ch.isdigit() for ch in e["txt"]):
        print(round(e["p"][0], 3), round(e["p"][1], 3), repr(e["txt"][:20]))
