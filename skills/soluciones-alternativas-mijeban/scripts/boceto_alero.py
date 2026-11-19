"""Mi lectura de las marcas del usuario sobre el detalle del alero (ficha 03), superpuesta al dibujo actual."""
import sys, fitz
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Polygon as MPoly
for f in (r"C:\Windows\Fonts\GOTHIC.TTF", r"C:\Windows\Fonts\GOTHICB.TTF"):
    fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Century Gothic"
VERDE = (7/255, 87/255, 72/255); AZUL = (0.15, 0.30, 0.80)

pdf, out = sys.argv[1], sys.argv[2]
# ventana del detalle del alero en la ficha v3: centro papel (163,7; 77,0), 1:20 (50 mm/m), centro de vista (−0,026; 0,28449)
CXp, CYp, VX, VY, K = 163.7, 77.0, -0.026, 0.28449, 50.0
mod = lambda px, py: ((px - CXp) / K + VX, (py - CYp) / K + VY)
x0p, x1p, y0p, y1p = 129.0, 199.0, 53.0, 100.0            # papel (mm)
mm = 72 / 25.4
page = fitz.open(pdf)[0]
pix = page.get_pixmap(dpi=300, clip=fitz.Rect(x0p * mm, (297 - y1p) * mm, x1p * mm, (297 - y0p) * mm))
img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[..., :3]
(xm0, ym0), (xm1, ym1) = mod(x0p, y0p), mod(x1p, y1p)

M = 0.268; PU = lambda x: 0.170 + M * x; D = 0.18 / np.cos(np.arctan(M))   # canto del par en vertical
X_CAN, X_T0, X_T1, X_IN = -0.338, 0.015, 0.248, 0.50

fig, axs = plt.subplots(1, 2, figsize=(16.5, 7.4), dpi=120)
for ax, tit in zip(axs, ("AHORA (ficha 03 v3)", "COMO LEO TUS MARCAS")):
    ax.imshow(img, extent=(xm0, xm1, ym0, ym1))
    ax.set_xlim(xm0, xm1); ax.set_ylim(ym0, ym1); ax.axis("off")
    ax.set_title(tit, fontsize=13, fontweight="bold", color=VERDE if "LEO" in tit else "0.3", loc="left")
ax = axs[1]
# par: sale de la fachada hasta bajo el canalón, cara inferior horizontal a la cota del fondo del cajón (0)
par = [(X_CAN, 0.0), (X_T1, 0.0), (X_T1, PU(X_T1) - D), (X_IN, PU(X_IN) - D), (X_IN, PU(X_IN)), (X_CAN, PU(X_CAN))]
ax.add_patch(MPoly(par, closed=True, fc=(0.35, 0.75, 0.25, 0.45), ec=VERDE, lw=2.0, zorder=5))
# durmiente bajado 10 cm dentro del tosco
dur = [(X_T0, -0.10), (X_T1, -0.10), (X_T1, 0.0), (X_T0, 0.0)]
ax.add_patch(MPoly(dur, closed=True, fc=(0.85, 0.90, 1.0, 0.85), ec=AZUL, lw=2.0, zorder=6))
ax.plot([X_T0, X_T1], [-0.10, 0.0], color=AZUL, lw=1.4, zorder=7); ax.plot([X_T0, X_T1], [0.0, -0.10], color=AZUL, lw=1.4, zorder=7)
ax.plot([X_CAN, X_CAN], [0.0, PU(X_CAN)], color=AZUL, lw=3, zorder=8)
kw = dict(fontsize=9.5, zorder=10, bbox=dict(fc="white", ec="none", alpha=0.85, pad=2))
ax.annotate("1 · el par sale de la fachada y llega\n    hasta debajo del canalón", xy=(-0.20, 0.06), xytext=(-0.60, 0.42),
            color=VERDE, arrowprops=dict(arrowstyle="-", color=VERDE), **kw)
ax.annotate("2 · cara inferior del par cortada en\n    horizontal, a la cota del fondo del cajón", xy=(-0.05, 0.0), xytext=(-0.60, -0.26),
            color=VERDE, arrowprops=dict(arrowstyle="-", color=VERDE), **kw)
ax.annotate("3 · durmiente 10 cm más abajo,\n    metido en la coronación del tosco", xy=(0.20, -0.06), xytext=(0.06, -0.33),
            color=AZUL, arrowprops=dict(arrowstyle="-", color=AZUL), **kw)
ax.annotate("4 · fin del par\n    bajo el canalón", xy=(X_CAN, 0.05), xytext=(-0.60, 0.16),
            color=AZUL, arrowprops=dict(arrowstyle="-", color=AZUL), **kw)
fig.tight_layout()
fig.savefig(out, dpi=120)
print("par: cara inferior a 0 entre", X_CAN, "y", X_T1, "| canto en la fachada", round(PU(0) - 0, 3), "| en el extremo", round(PU(X_CAN), 3))
