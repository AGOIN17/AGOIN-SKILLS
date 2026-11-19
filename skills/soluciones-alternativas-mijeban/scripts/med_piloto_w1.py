"""Piloto de medición: alzado W1 (fachada norte de la fila norte). Paños por coordenadas del DWG."""
import sys, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
from shapely.geometry import LineString, box

for f in (r"C:\Windows\Fonts\GOTHIC.TTF", r"C:\Windows\Fonts\GOTHICB.TTF"):
    fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Century Gothic"
VERDE = (7/255, 87/255, 72/255)
PIEDRA = (0.62, 0.42, 0.25)
ROJO = (0.75, 0.12, 0.12)

V = json.load(open(sys.argv[1], encoding="utf-8"))
v = V[0]
X0, Y0 = 422000.0, 4412100.0
Y515, Y51185, YALERO = 83.257, 80.107, 86.787      # 515,00 · 511,85 · arranque del alero
UMBRAL = 3.0

# ---- paños: (código, tipo, descripción, x0, x1, y0, y1, [huecos (descr, x0, x1, y0, y1)])
P = [
    ("W1-1", 1, "Bloque de servicio y porche de entrada (cinta corrida)", 73.592, 91.992, Y515, YALERO,
     [("Ventana V-4", 74.742, 76.617, 84.357, 85.757), ("Ventana V-5", 77.517, 78.267, 84.357, 85.757),
      ("Ventana V-6", 82.042, 83.492, 84.357, 85.757), ("Ventana", 74.742, 82.042, 84.357, 85.757),
      ("Celosía de lamas del recibidor", 85.002, 86.592, Y515, 86.337),
      ("Puerta de entrada", 86.652, 88.132, 83.317, 86.277)]),
    ("W1-2", 1, "Unión entre volúmenes A y B", 91.992, 94.992, Y515, YALERO,
     [("Acristalamiento de la unión", 91.992, 94.992, Y515, 85.757)]),
    ("W1-3", 1, "Volumen B (dormitorios 6 y 7)", 94.992, 104.992, Y515, YALERO,
     [("Puerta-ventana", 96.842, 99.342, Y515, 85.757), ("Puerta-ventana", 101.492, 103.992, Y515, 85.757)]),
    ("W1-4", 1, "Unión entre volúmenes B y C", 104.992, 107.992, Y515, YALERO,
     [("Acristalamiento de la unión", 104.992, 107.992, Y515, 85.757)]),
    ("W1-5", 1, "Volumen C (dormitorio 5)", 107.992, 114.192, Y515, YALERO,
     [("Puerta-ventana", 109.842, 112.342, Y515, 85.757)]),
    ("W1-6", 1, "Unión entre volúmenes C y D", 114.192, 117.592, Y515, YALERO,
     [("Ventana fija", 116.667, 117.532, Y515, 85.757)]),
    ("W1-7", 1, "Volumen D (dormitorio 4)", 117.592, 122.092, Y515, YALERO, []),
    ("W1-8", 2, "Garaje bajo el bloque de servicio (piedra)", 73.592, 84.542, Y51185, Y515,
     [("Puerta de garaje", 73.992, 77.367, Y51185, 82.607), ("Puerta de garaje", 77.517, 80.892, Y51185, 82.607),
      ("Puerta peatonal con fijo", 82.042, 83.492, Y51185, 82.607)]),
]
# la «Ventana» 74.742–82.042 no es un hueco: es la línea de dintel común; se quita
P[0][7].pop(3)

lineas, tot = [], {1: 0.0, 2: 0.0}
for cod, tipo, desc, x0, x1, y0, y1, huecos in P:
    L, H = round(x1 - x0, 2), round(y1 - y0, 2)
    lineas.append((tipo, f"{cod} · {desc}", 1, L, H, L * H))
    tot[tipo] += L * H
    for hd, a0, a1, b0, b1 in huecos:
        l, h = round(a1 - a0, 2), round(b1 - b0, 2)
        if l * h > UMBRAL:
            lineas.append((tipo, f"   a deducir: {hd}", -1, l, h, -l * h))
            tot[tipo] -= l * h

# ---- dibujo
fig = plt.figure(figsize=(16.5, 9.6), dpi=130)
ax = fig.add_axes([0.03, 0.50, 0.94, 0.40])
capas = {"ALZ_FIN": ("0.45", 0.5), "ALZ_GRU": ("0.15", 1.2), "ALZ_CAR": ("0.35", 0.5), "ALZ_TEJA": ("0.55", 0.4),
         "ALZ_AUX": ("0.6", 0.4)}
zona_piedra = box(73.592 + X0, Y51185 + Y0, 84.542 + X0, Y515 + Y0)
for e in v["ents"]:
    if e["l"] == "ALZ_TRM_Lajas":
        for g in e.get("g", []):
            if len(g) >= 2:
                r = LineString(g).intersection(zona_piedra)
                for s in getattr(r, "geoms", [r]):
                    if not s.is_empty and s.geom_type == "LineString":
                        xs, ys = zip(*s.coords)
                        ax.plot([x - X0 for x in xs], [y - Y0 for y in ys], color=(0.45, 0.32, 0.2), lw=0.3)
        continue
    if e["l"] not in capas or e["t"] == "HATCH":
        continue
    c, lw = capas[e["l"]]
    for g in e.get("g", []):
        if len(g) >= 2:
            if e["l"] == "ALZ_GRU" and any(abs(xb - xa) > 0.01 and abs(yb - ya) > 0.01 for (xa, ya), (xb, yb) in zip(g, g[1:])):
                continue            # rasante natural: no es fachada y confunde
            xs, ys = zip(*g)
            if min(xs) < 422068 or max(xs) > 422127 or min(ys) < 4412179.5:
                continue
            ax.plot([x - X0 for x in xs], [y - Y0 for y in ys], color=c, lw=lw)
for cod, tipo, desc, x0, x1, y0, y1, huecos in P:
    col = VERDE if tipo == 1 else PIEDRA
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=(*col, 0.22), ec=col, lw=1.6, zorder=5))
    for hd, a0, a1, b0, b1 in huecos:
        if (a1 - a0) * (b1 - b0) > UMBRAL:
            ax.add_patch(Rectangle((a0, b0), a1 - a0, b1 - b0, fc="white", ec=ROJO, lw=1.0, hatch="////", zorder=6, alpha=0.9))
    ax.text((x0 + x1) / 2, y1 - 0.30, cod, ha="center", va="top", fontsize=9, fontweight="bold", color=col, zorder=8,
            bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
for y, t in ((Y515, "515,00"), (Y51185, "511,85"), (YALERO, "arranque del alero")):
    ax.annotate(t, (122.6, y), xytext=(123.2, y), fontsize=7.5, color="0.3", va="center",
                arrowprops=dict(arrowstyle="-", color="0.5", lw=0.5))
ax.set_xlim(72.5, 127.5); ax.set_ylim(79.3, 88.6); ax.set_aspect("equal"); ax.axis("off")
fig.text(0.03, 0.975, "Piloto de medición · Alzado W1 (fachada norte, fila norte)", fontsize=15, fontweight="bold",
         color=VERDE, va="top")
fig.text(0.03, 0.948, "Verde: tipo 1, fachada completa (alternativa B).  Marrón: tipo 2, muro de la vivienda con piedra.  "
         "Rayado rojo: huecos de más de 3 m², descontados. Los huecos menores se miden como macizo.", fontsize=9, color="0.25", va="top")

# tabla de líneas
ax2 = fig.add_axes([0.03, 0.02, 0.94, 0.47]); ax2.axis("off")
y = 0.98
ax2.text(0.00, y, "Paño / hueco", fontsize=8.5, fontweight="bold"); ax2.text(0.56, y, "Uds", fontsize=8.5, fontweight="bold", ha="right")
ax2.text(0.66, y, "Longitud", fontsize=8.5, fontweight="bold", ha="right"); ax2.text(0.76, y, "Altura", fontsize=8.5, fontweight="bold", ha="right")
ax2.text(0.88, y, "Parcial m²", fontsize=8.5, fontweight="bold", ha="right")
for tipo in (1, 2):
    y -= 0.055
    ax2.text(0.00, y, "TIPO 1 · FACHADA COMPLETA (ALTERNATIVA B)" if tipo == 1 else "TIPO 2 · MURO DE LA VIVIENDA REVESTIDO DE PIEDRA",
             fontsize=8, fontweight="bold", color=VERDE if tipo == 1 else PIEDRA)
    for t, d, n, L, H, par in lineas:
        if t != tipo:
            continue
        y -= 0.042
        ax2.text(0.00, y, d, fontsize=7.6, color=ROJO if n < 0 else "0.1")
        ax2.text(0.56, y, f"{n}", fontsize=7.6, ha="right"); ax2.text(0.66, y, f"{L:.2f}".replace(".", ","), fontsize=7.6, ha="right")
        ax2.text(0.76, y, f"{H:.2f}".replace(".", ","), fontsize=7.6, ha="right")
        ax2.text(0.88, y, f"{par:.2f}".replace(".", ","), fontsize=7.6, ha="right", color=ROJO if n < 0 else "0.1")
    y -= 0.045
    ax2.text(0.76, y, "Total", fontsize=8, fontweight="bold", ha="right")
    ax2.text(0.88, y, f"{tot[tipo]:.2f} m²".replace(".", ","), fontsize=8.5, fontweight="bold", ha="right")
fig.savefig(sys.argv[2], dpi=130)
for t, d, n, L, H, par in lineas:
    print(t, d, n, L, H, round(par, 2))
print("TOTALES", {k: round(v_, 2) for k, v_ in tot.items()})
