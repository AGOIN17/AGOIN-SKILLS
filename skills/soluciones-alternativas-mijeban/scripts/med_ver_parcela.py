"""Planta A-02 y A-01 completas (casa, plataforma, piscina, escaleras): muros fuera de la vivienda."""
import sys, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
P = json.load(open(sys.argv[1], encoding="utf-8"))
OX, OY = 421600, 4412200
fig, axs = plt.subplots(1, 2, figsize=(30, 14), dpi=85)
for ax, (hoja, dy) in zip(axs, (("A-02", 0), ("A-01", 50))):
    v = [x for x in P if x["hoja"] == hoja][0]
    for e in v["ents"]:
        for g in e.get("g", []):
            if len(g) < 2:
                continue
            xs = [x - OX for x, y in g]; ys = [y - OY + dy for x, y in g]
            if e["t"] == "HATCH" and e["l"] in ("0_TRM", "0_PILARES"):
                ax.fill(xs, ys, color="tab:orange", alpha=0.45, lw=0)
            elif e["l"] in ("0_GRU", "0_PILARES"):
                ax.plot(xs, ys, color="k", lw=0.6)
            elif e["l"] in ("0", "0_AUX", "0_PAV", "0_FIN"):
                ax.plot(xs, ys, color="0.7", lw=0.3)
    for e in v["ents"]:
        if e["t"] in ("TEXT", "MTEXT") and any(c.isdigit() for c in e.get("txt", "")) and "," in e.get("txt", ""):
            ax.text(e["p"][0] - OX, e["p"][1] - OY + dy, e["txt"][:10], fontsize=6, color="m")
    ax.set_aspect("equal"); ax.grid(alpha=0.3); ax.set_title(hoja)
    ax.set_xticks(range(40, 110, 5))
fig.savefig(sys.argv[2], bbox_inches="tight")
