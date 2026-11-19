"""Esquema del alero con peto de ladrillo (pizarra del usuario, 2026-11-09).
El ladrillo sube hasta la cara superior del Thermochip y lo recoge; el canalón se ancla al ladrillo; Onduline encima.
Sección por la viga (par de la cercha). Metros; x = 0 cara exterior del monocapa, x > 0 hacia dentro; y = 0 coronación del tosco (apoyo de la viga).
Uso: python alero_B.py salida.png"""
import sys, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib import font_manager

fam = 'Century Gothic' if any('Century Gothic' in f.name for f in font_manager.fontManager.ttflist) else 'DejaVu Sans'
plt.rcParams['font.family'] = fam
plt.rcParams['hatch.linewidth'] = 0.5

S = 0.268
CV = 1 / math.cos(math.atan(S))
FR, XP, TB = 0.010 * CV, 0.200 * CV, 0.019 * CV
PANEL = FR + XP + TB
VIGA = 0.200 * CV                  # canto vertical de la viga de 20 cm
XU = 0.121                         # cara interior del peto (monocapa 15 + ladrillo a soga 106)
XT = XU + 0.010                    # testa del panel y de la viga (1 cm de junta)
XZ1 = 0.248                        # cara interior del tosco
SEAT = 0.010                       # chapa del herraje
# la viga apoya en el tosco: su cara inferior pasa por SEAT en la cara interior del tosco
Y0 = SEAT + VIGA - S * XZ1         # cara inferior del panel en x = 0
yb = lambda x: Y0 + S * x          # cara inferior del panel = cara superior de la viga
yt = lambda x: yb(x) + PANEL       # cara superior del panel = coronación del peto
yv = lambda x: max(yb(x) - VIGA, SEAT)
XR = 0.80
YBOT = -0.30

VERDE = (7/255, 87/255, 72/255)
VCLARO = (0.80, 0.90, 0.86)
LADR = (0.96, 0.87, 0.80); LADR_H = (0.75, 0.55, 0.45)
G = lambda g: (g/255,)*3

fig, ax = plt.subplots(figsize=(11.5, 7.8), dpi=170)
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-0.42, 1.48); ax.set_ylim(-0.33, 0.80)

def poly(pts, fc, ec='k', lw=0.8, hatch=None, z=2, hc=None):
    if hc is not None:
        ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=hc, lw=0, hatch=hatch, zorder=z))
        ax.add_patch(Polygon(pts, closed=True, fc='none', ec=ec, lw=lw, zorder=z + 0.1))
    else:
        ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw, hatch=hatch, zorder=z))

def banda(x0, x1, f0, f1, **kw):
    poly([(x0, f0(x0)), (x1, f0(x1)), (x1, f1(x1)), (x0, f1(x0))], **kw)

# ---------- muro (fachada B) ----------
poly([(0, YBOT), (0.015, YBOT), (0.015, yt(0.015)), (0, yt(0))], G(235), lw=0.6)                       # monocapa
poly([(0.015, YBOT), (XZ1, YBOT), (XZ1, 0), (0.015, 0)], LADR, hatch='////', hc=LADR_H)                  # tosco portante, sin zuncho
poly([(0.015, 0), (XU, 0), (XU, yt(XU)), (0.015, yt(0.015))], LADR, ec=VERDE, lw=1.3, hatch='////', hc=LADR_H)  # peto
for k in range(1, 4):                                                                                  # hiladas
    ax.plot([0.015, XU], [k * 0.106, k * 0.106], color=LADR_H, lw=0.6, zorder=3)
poly([(XT, 0), (XZ1, 0), (XZ1, SEAT), (XT, SEAT)], G(90), lw=0.5, z=4)                                  # placa de acero
for xa in (0.16, 0.21):
    ax.plot([xa, xa], [SEAT, -0.10], color=G(60), lw=1.0, zorder=4)                                    # pernos
poly([(XZ1, YBOT), (0.263, YBOT), (0.263, yv(0.263)), (XZ1, yv(XZ1))], G(230), lw=0.5)                 # enfoscado
poly([(0.263, YBOT), (0.363, YBOT), (0.363, yv(0.363)), (0.263, yv(0.263))], 'white', hatch='oo', hc=G(150))  # EPS
poly([(0.363, YBOT), (0.433, YBOT), (0.433, yv(0.433)), (0.363, yv(0.363))], LADR, hatch='----', hc=LADR_H)   # gran formato
poly([(0.433, YBOT), (0.448, YBOT), (0.448, yv(0.448)), (0.433, yv(0.433))], G(245), lw=0.5)            # yeso
ax.plot([-0.01, 0.46], [YBOT, YBOT], color='k', lw=0.6, ls=(0, (6, 3)), zorder=5)

# ---------- viga (par de la cercha), cortada a lo largo ----------
xs = [XT] + [XT + i * (XR - XT) / 60 for i in range(1, 61)]
low = [yv(x) for x in xs]
pts = [(x, y) for x, y in zip(xs, low)] + [(XR, yb(XR)), (XT, yb(XT))]
poly(pts, (0.93, 0.88, 0.80), lw=0.9, z=3)
for k in range(1, 6):                                                                                  # vetas
    f = k / 6
    xv0 = XT + 0.03 * k
    ax.plot([xv0, XR], [yb(xv0) - VIGA * f if yb(xv0) - VIGA * f > SEAT + 0.005 else SEAT + 0.005 + 0.004 * k,
             yb(XR) - VIGA * f], color=(0.75, 0.66, 0.52), lw=0.4, zorder=3.5)
ax.plot([XR, XR], [yv(XR) - 0.01, yt(XR) + 0.02], color='k', lw=0.6, ls=(0, (6, 3)), zorder=6)
ax.text(0.53, yb(0.53) - VIGA / 2, 'Viga', fontsize=8, color=G(90), ha='center', va='center', rotation=15, zorder=6)

# ---------- Thermochip ----------
banda(XT, XR, yb, lambda x: yb(x) + FR, fc=(0.93, 0.83, 0.65), lw=0.6, z=4)
banda(XT, XR, lambda x: yb(x) + FR, lambda x: yb(x) + FR + XP, fc='white', hatch='oo', hc=G(150), lw=0.6, z=4)
banda(XT, XR, lambda x: yb(x) + FR + XP, yt, fc=G(200), lw=0.6, z=4)
poly([(XU, yb(XU) - 0.004), (XT, yb(XT) - 0.004), (XT, yt(XT)), (XU, yt(XU))], VERDE, ec=VERDE, lw=0.5, z=6)  # junta de espuma

# ---------- Onduline, goterón, teja ----------
OND = 0.024 * CV
yo = lambda x: yt(x) + 0.004
XO = -0.050
banda(XO, XR, yo, lambda x: yo(x) + OND, fc=G(120), ec='k', lw=0.5, z=6)
for i in range(4):                                                                                     # peine
    xp = XO + 0.010 + i * 0.010
    ax.plot([xp, xp], [yo(xp) + OND, yo(xp) + OND + 0.022], color=G(60), lw=0.7, zorder=9)
ax.plot([0.09, -0.006, -0.010, -0.010], [yt(0.09) + 0.002, yt(-0.006) + 0.002, yt(-0.006) - 0.004, yt(0) - 0.055],
        color=VERDE, lw=2.0, zorder=8, solid_joinstyle='miter')                                       # goterón
yc = lambda x: yo(x) + OND + 0.002
for x0, x1, dy in ((-0.110, 0.32, 0.0), (0.24, XR, 0.016)):
    banda(x0, x1, lambda x, d=dy: yc(x) + d, lambda x, d=dy: yc(x) + d + 0.016, fc=(0.80, 0.42, 0.30), lw=0.6, z=7)
for x0, x1 in ((-0.065, 0.36), (0.30, XR)):
    banda(x0, x1, lambda x: yc(x) + 0.075, lambda x: yc(x) + 0.091, fc='none', ec=G(130), lw=0.6, z=7)
ax.annotate('', xy=(0.22, yo(0.22) + 0.012), xytext=(0.00, yo(0.0) + 0.012),
            arrowprops=dict(arrowstyle='->', color=VERDE, lw=1.0), zorder=10)

# ---------- canalón anclado al ladrillo ----------
XGB, XGF = -0.004, -0.174
ytop_b = yt(0) - 0.030
ytop_f = ytop_b - 0.020
ybot = ytop_b - 0.135
ax.plot([XGB, XGB, XGF, XGF, XGF - 0.012], [ytop_b, ybot, ybot, ytop_f, ytop_f], color=VERDE, lw=2.0, zorder=7)
ax.add_patch(Polygon([(XGB, ybot + 0.06), (XGB, ybot), (XGF, ybot), (XGF, ybot + 0.06)], closed=True,
                     fc=(0.85, 0.92, 0.97), ec='none', zorder=3))
ya = ybot + 0.05                                                                                       # soporte y anclaje
ax.plot([0.075, XGB - 0.004, XGB - 0.004, XGF - 0.006, XGF - 0.006], [ya, ya, ybot - 0.006, ybot - 0.006, ytop_f - 0.01],
        color=VERDE, lw=0.9, zorder=8)
poly([(0.0, ya - 0.006), (0.075, ya - 0.006), (0.075, ya + 0.006), (0.0, ya + 0.006)], VCLARO, ec=VERDE, lw=0.8, z=8)

# ---------- cinta estanca ----------
xi = 0.448
ax.plot([xi - 0.004, xi - 0.004, xi + 0.08], [yv(xi) - 0.06, yv(xi) - 0.004, yv(xi + 0.08) - 0.004],
        color=VERDE, lw=2.2, zorder=9)

# ---------- cotas ----------
def cota_v(x, y0, y1, txt):
    ax.plot([x, x], [y0, y1], color='k', lw=0.5, zorder=9)
    for y in (y0, y1):
        ax.plot([x - 0.008, x + 0.008], [y - 0.008, y + 0.008], color='k', lw=0.7, zorder=9)
    ax.text(x - 0.012, (y0 + y1) / 2, txt, fontsize=6.5, ha='right', va='center', zorder=9)
cota_v(-0.24, 0, yt(0), '%d\npeto' % round(yt(0) * 100))
for y in (0, yt(0)):
    ax.plot([-0.25, -0.01 if y else 0.0], [y, y], color=G(140), lw=0.4, ls=':', zorder=1)
yh = ybot - 0.05
ax.plot([XGF, 0], [yh, yh], color='k', lw=0.5)
for x in (XGF, 0):
    ax.plot([x - 0.008, x + 0.008], [yh - 0.008, yh + 0.008], color='k', lw=0.7)
ax.text(XGF / 2, yh - 0.012, '≈ %d cm de vuelo\n(DET-01: 56 cm)' % round(-XGF * 100 + 1), fontsize=6.5, ha='center', va='top')
ax.text(-0.21, -0.22, 'EXTERIOR', fontsize=7.5, color=G(90), ha='center')
ax.text(0.66, -0.22, 'INTERIOR', fontsize=7.5, color=G(90), ha='center')

# ---------- burbujas ----------
VERDES = {3, 5, 6, 7, 11}
def burb(n, p, q):
    c = VERDE if n in VERDES else 'k'
    ax.plot([p[0], q[0]], [p[1], q[1]], color='k', lw=0.5, zorder=11)
    ax.plot(*p, marker='o', ms=2.2, color='k', zorder=11)
    ax.add_patch(Circle(q, 0.021, fc='white', ec=c, lw=1.0, zorder=12))
    ax.text(*q, str(n), fontsize=6.8, ha='center', va='center', zorder=13, color=c, fontweight='bold')
burb(1, (0.06, yc(0.06) + 0.008), (0.03, 0.62))
burb(2, (0.15, yo(0.15) + 0.012), (0.12, 0.66))
burb(3, (0.04, yt(0.04) + 0.003), (0.21, 0.70))
burb(4, (0.40, yb(0.40) + 0.12), (0.42, 0.74))
burb(5, (XU + 0.005, yb(XU) + 0.12), (0.30, 0.03 + 0.5))
burb(6, (0.07, 0.20), (-0.12, 0.05))
burb(7, (XGF + 0.05, ybot + 0.02), (-0.36, 0.45))
burb(8, (0.72, yb(0.72) - 0.12), (0.76, 0.06))
burb(9, (0.19, 0.005), (0.60, -0.12))
burb(10, (0.31, 0.0), (0.60, 0.06))
burb(11, (xi - 0.004, yv(xi) - 0.03), (0.60, -0.03))

ley = [
    (1, 'Teja curva: la canal vuela unos 6 cm sobre el canalón'),
    (2, 'Onduline sobre el Thermochip y sobre el peto; vuela 5 cm dentro\n     del canalón, con peine que deja entrar el aire'),
    (3, 'Goterón de chapa bajo el borde del Onduline: cubre la cabeza\n     del monocapa y vierte dentro del canalón'),
    (4, 'Thermochip TAH 10-200-19, cortado a plomo contra el ladrillo'),
    (5, 'Junta de espuma precomprimida entre la testa del panel y el\n     ladrillo: cierra el XPS y el paso de aire'),
    (6, 'Peto de ladrillo tosco a soga (10,6 cm), 3-4 hiladas, hasta la cara\n     superior del panel; coronación con la pendiente'),
    (7, 'Canalón visto anclado al ladrillo: soportes cada 50 cm con taco\n     químico y tamiz (el tosco es perforado); borde delantero 2 cm más bajo'),
    (8, 'Viga (par de la cercha) apoyada en el tosco, con asiento;\n     testa a 1 cm del ladrillo. Sin durmiente'),
    (9, 'Placa de acero bajo cada viga, anclada al tosco con taco químico'),
    (10, 'Aislamiento de la fachada B hasta la viga (entre vigas, hasta el panel)'),
    (11, 'Cinta estanca al aire por dentro, entre el yeso, la viga y el friso'),
]
yy = 0.78
ax.text(0.88, yy, 'ALERO CON PETO DE LADRILLO · CANALÓN VISTO', fontsize=9.5, fontweight='bold', color=VERDE, va='top')
ax.text(0.88, yy - 0.042, 'Sección por la viga · esquema a escala, cotas en cm\nEn verde, lo que cambia frente a la ficha 03',
        fontsize=6.6, color=G(80), va='top')
yy -= 0.12
for n, t in ley:
    c = VERDE if n in VERDES else 'k'
    ax.add_patch(Circle((0.895, yy - 0.010), 0.016, fc='white', ec=c, lw=0.9))
    ax.text(0.895, yy - 0.010, str(n), fontsize=6.2, ha='center', va='center', fontweight='bold', color=c)
    ax.text(0.92, yy, t, fontsize=6.6, va='top', linespacing=1.25)
    yy -= 0.040 + 0.030 * t.count('\n')

fig.savefig(sys.argv[1], bbox_inches='tight', pad_inches=0.08, facecolor='white')
print('ok', fam, 'cara inf. panel en fachada %.3f, peto %.3f' % (Y0, yt(0)))
