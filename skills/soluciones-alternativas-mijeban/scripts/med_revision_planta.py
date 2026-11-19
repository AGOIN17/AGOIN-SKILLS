"""Revisión en planta: cada paño de fachada, de dónde se mide, estimación y comparación con la licitación."""
import sys, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
for f in (r"C:\Windows\Fonts\GOTHIC.TTF", r"C:\Windows\Fonts\GOTHICB.TTF"):
    fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Century Gothic"
VERDE = (7/255, 87/255, 72/255); AZUL = (0.15, 0.40, 0.75); NARANJA = (0.88, 0.50, 0.10); ROJO = (0.78, 0.15, 0.15)
OX, OY = 421600, 4412200
V = json.load(open(sys.argv[1], encoding="utf-8")); v = [x for x in V if x["hoja"] == "A-02"][0]

H_LARGA, H_HAST = 3.53, 3.80
SUBIDA = 3.70 * 0.268                    # triángulo del hastial: pendiente 27 % sobre media crujía de 7,40
HAST = 7.40 * H_HAST + 7.40 * SUBIDA / 2
# (código, vista, x0, y0, x1, y1, área neta estimada, nota)
P = []
def larga(cod, vista, x0, x1, y, huecos, nota=""):
    L = x1 - x0
    P.append((cod, vista, x0, y, x1, y, L * H_LARGA - huecos, nota, L))
def hast(cod, x, y0, y1, area, nota=""):
    P.append((cod, "S", x, y0, x, y1, area, nota, y1 - y0))
# fachada norte (W1, ya medida: 128,18 m² netos en total)
for cod, x0, x1, y in (("N-D", 46.502, 51.002, 12.501), ("N-I", 51.002, 54.402, 12.501), ("N-1", 54.402, 60.602, 16.951),
                       ("N-P1", 60.602, 63.602, 9.551), ("N-2", 63.602, 73.602, 16.951), ("N-P2", 73.602, 76.602, 9.551),
                       ("N-3", 76.602, 95.002, 16.951)):
    P.append((cod, "W1", x0, y, x1, y, None, "", x1 - x0))
# fachada sur (1E, estimada desde planta y carpintería)
larga("S-D", "1E", 46.502, 51.002, 5.101, 2.30 * 2.50, "PV-1")
larga("S-P0", "1E", 51.002, 54.002, 8.051, 3.00 * 2.50, "VF-1 (frente del pasillo)")
larga("S-1", "1E", 54.002, 64.002, 0.651, 2 * 2.50 * 2.50, "2 PV-2")
larga("S-P1", "1E", 64.002, 67.002, 8.051, 3.00 * 2.50, "VF-1")
larga("S-2", "1E", 67.002, 77.002, 0.651, 2 * 2.50 * 2.50, "2 PV-2")
larga("S-P2", "1E", 77.002, 80.002, 8.051, 3.00 * 2.50, "VF-1")
larga("S-3", "1E", 80.002, 95.002, 0.651, 14.07 * 2.50, "PV-3")
# hastiales (secciones S)
for cod, x, y0, y1 in (("H-D-O", 46.502, 5.101, 12.501), ("H-1-E", 60.602, 9.551, 16.951), ("H-2-O", 63.602, 9.551, 16.951),
                       ("H-2-E", 73.602, 9.551, 16.951), ("H-3-E", 95.002, 9.551, 16.951), ("H-S1-O", 54.002, 0.651, 8.051),
                       ("H-S1-E", 64.002, 0.651, 8.051), ("H-S2-O", 67.002, 0.651, 8.051), ("H-S2-E", 77.002, 0.651, 8.051),
                       ("H-S3-O", 80.002, 0.651, 8.051)):
    hast(cod, x, y0, y1, HAST)
hast("H-D-E", 51.002, 5.101, 12.501, (7.40 - 2.10 - 1.50) * H_HAST + 7.40 * SUBIDA / 2, "tapado por instalaciones y pasillo")
hast("H-1-O", 54.402, 9.551, 16.951, (7.40 - 2.10) * H_HAST + 7.40 * SUBIDA / 2, "tapado por instalaciones")
hast("H-3-O", 76.602, 9.551, 16.951, (7.40 - 3.30) * H_HAST + 7.40 * SUBIDA / 2, "porche abierto 3,30")
hast("H-S3-E", 95.002, 0.651, 8.051, HAST - 6.22 * 2.50, "PV-4")
P.append(("Pas-E", "S", 95.002, 8.051, 95.002, 9.551, 1.50 * H_LARGA - 1.50 * 2.50, "PV-5", 1.50))

W1_NETO = 128.18
tot = {"W1": W1_NETO, "1E": sum(p[6] for p in P if p[1] == "1E"), "S": sum(p[6] for p in P if p[1] == "S")}
total = sum(tot.values())
print({k: round(x, 2) for k, x in tot.items()}, "total", round(total, 2), "hastial tipo", round(HAST, 2))

fig = plt.figure(figsize=(16.5, 10.5), dpi=130)
ax = fig.add_axes([0.01, 0.10, 0.64, 0.80])
for e in v["ents"]:
    if e["l"] in ("0_GRU", "0_PILARES") and e["t"] != "HATCH":
        for g in e.get("g", []):
            if len(g) >= 2:
                xs, ys = zip(*g); ax.plot([x - OX for x in xs], [y - OY for y in ys], color="0.55", lw=0.4)
    if e["t"] == "HATCH" and e["l"] in ("0_TRM", "0_PILARES"):
        for g in e["g"]:
            xs, ys = zip(*g); ax.fill([x - OX for x in xs], [y - OY for y in ys], color="0.82", lw=0)
col = {"W1": VERDE, "1E": AZUL, "S": NARANJA}
for cod, vista, x0, y0, x1, y1, area, nota, L in P:
    c = col[vista]
    ax.plot([x0, x1], [y0, y1], color=c, lw=4.2, solid_capstyle="butt", alpha=0.9)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    if vista == "S":
        oeste = cod.endswith("O")
        dx = -0.35 if oeste else 0.35
        dy = -1.6 if oeste else 1.6
        ax.text(mx + dx, my + dy, f"{cod}\n{L:.2f}".replace(".", ","), fontsize=6.3, color=c, ha="right" if oeste else "left",
                va="center", rotation=0)
    else:
        dy = 0.45 if (vista == "W1") else -0.45
        ax.text(mx, my + dy, f"{cod} {L:.2f}".replace(".", ","), fontsize=6.3, color=c, ha="center", va="bottom" if dy > 0 else "top")
ax.set_xlim(44.5, 97.5); ax.set_ylim(-2.0, 19.0); ax.set_aspect("equal"); ax.axis("off")
ax.annotate("N", xy=(96.6, 18.3), xytext=(96.6, 16.6), ha="center", fontsize=9, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color="0.2"))
fig.text(0.01, 0.975, "Revisión en planta · fachadas de la vivienda sobre 515,00", fontsize=15, fontweight="bold", color=VERDE, va="top")
fig.text(0.01, 0.945, "Verde: fachada norte, alzado W1 (medida).   Azul: fachada sur, alzado 1E.   Naranja: hastiales, en las secciones 1S–8S.   "
         "Cotas en m, a cara exterior del muro (planta A-02 del DWG).", fontsize=9, color="0.25", va="top")
fig.text(0.01, 0.06, "La fachada sur y los hastiales están estimados desde la planta y la memoria de carpintería: falta medirlos en sus alzados. "
         "Hastial tipo: 7,40 × 3,80 + triángulo de pendiente 27 % = 31,79 m².", fontsize=8.2, color="0.3")

# tabla de comparación
DED = 2.30*2.50 + 3*7.5 + 4*6.25 + 14.07*2.5 + 6.22*2.5 + 1.5*2.5 + (4.90 + 4.38 + 7.5 + 7.5 + 12.5 + 6.25)
TAPADO = 14 * HAST - sum(p[6] for p in P if p[1] == "S" and p[0].startswith("H")) - 6.22 * 2.50
fmt = lambda x: f"{x:,.2f}".replace(",", " ").replace(".", ",")
t = fig.add_axes([0.66, 0.06, 0.33, 0.86]); t.axis("off")
filas = [
    ("", "Licitación", "Esta medición"),
    ("Fachadas largas: longitud", "82,00 m", "82,00 m"),
    ("Fachadas largas: altura", "3,80 m", "3,53 m"),
    ("Frentes del pasillo a los patios", "no", "5 × 3,00 m"),
    ("Hastiales", "14 × 33,15 m²", "14 × 31,79 m²"),
    ("Hastiales tapados (porche, instalaciones)", "no", f"−{fmt(TAPADO)} m²"),
    ("Huecos descontados", "todos: −195,10 m²", f"> 3 m²: −{fmt(DED)} m²"),
    ("TOTAL fachada sobre 515,00", "609,17 m²", f"{total:.2f} m²".replace(".", ",")),
]
y = 0.97
for i, (a, b, c) in enumerate(filas):
    peso = "bold" if i in (0, len(filas) - 1) else "normal"
    t.text(0.0, y, a, fontsize=8.6, fontweight=peso, va="top", wrap=True)
    t.text(0.66, y, b, fontsize=8.6, fontweight=peso, va="top", ha="right")
    t.text(1.0, y, c, fontsize=8.6, fontweight=peso, va="top", ha="right", color=VERDE if i else "k")
    y -= 0.062
    t.plot([0, 1], [y + 0.018, y + 0.018], color="0.85", lw=0.5)
t.set_xlim(0, 1); t.set_ylim(0, 1)
fig.savefig(sys.argv[2], dpi=130)
for p in P:
    print(p[0], p[1], round(p[8], 2), None if p[6] is None else round(p[6], 2), p[7])
ded = 2.30*2.50 + 3*7.5 + 4*6.25 + 14.07*2.5 + 6.22*2.5 + 1.5*2.5 + (4.90 + 4.38 + 7.5 + 7.5 + 12.5 + 6.25)
print("huecos descontados (mi criterio):", round(ded, 2))
