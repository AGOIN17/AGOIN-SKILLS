import sys, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
V = json.load(open(sys.argv[1], encoding="utf-8"))
v = [x for x in V if x["hoja"] == sys.argv[2]][0]
col = {"0_GRU": ("k", 0.9), "0_TRM": ("tab:orange", 0.3), "0_CAR": ("tab:blue", 0.6), "0_PILARES": ("tab:red", 0.5),
       "0_FIN": ("0.5", 0.4), "ONDUTHERM": ("tab:purple", 0.3), "0": ("0.75", 0.3), "0_POL": ("tab:green", 0.4)}
fig, ax = plt.subplots(figsize=(26, 20), dpi=90)
for e in v["ents"]:
    if e["l"] not in col:
        continue
    c, lw = col[e["l"]]
    for g in e.get("g", []):
        if len(g) < 2:
            continue
        xs, ys = zip(*g)
        if e["t"] == "HATCH":
            ax.fill(xs, ys, color=c, alpha=0.35, lw=0)
        else:
            ax.plot(xs, ys, color=c, lw=lw)
for e in v["ents"]:
    if e["t"] in ("TEXT", "MTEXT") and e["l"] in ("0_SUP", "0_TXT CARP", "0_CAR", "0_TXT"):
        ax.text(e["p"][0], e["p"][1], e["txt"][:18], fontsize=6, color="m")
ax.set_aspect("equal")
ax.grid(alpha=0.25)
fig.savefig(sys.argv[3], bbox_inches="tight")
