"""Esquema de la opción A del alero: Thermochip enrasado con la fachada, canalón visto.
Sección entre cerchas. Unidades en metros; x = 0 cara exterior del monocapa, x > 0 hacia dentro; y = 0 cara superior del zuncho.
Uso: python alero_A.py salida.png"""
import sys, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib import font_manager

fam = 'Century Gothic' if any('Century Gothic' in f.name for f in font_manager.fontManager.ttflist) else 'DejaVu Sans'
plt.rcParams['font.family'] = fam

S = 0.268                       # pendiente (DET-01)
CV = 1 / math.cos(math.atan(S))  # paso de espesor normal a vertical
Y0 = 0.170                      # cara inferior del panel en el plano de fachada (DET-01)
yb = lambda x: Y0 + S * x       # cara inferior del panel
FR, XP, TB = 0.010 * CV, 0.200 * CV, 0.019 * CV
yt = lambda x: yb(x) + FR + XP + TB
XT = -0.012                     # testa del panel, a plomo
XR = 0.78                       # corte del dibujo por la derecha
YBOT = -0.30

VERDE = (7/255, 87/255, 72/255)
VCLARO = (0.80, 0.90, 0.86)
G = lambda g: (g/255,)*3

fig, ax = plt.subplots(figsize=(11.5, 7.6), dpi=170)
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-0.42, 1.45); ax.set_ylim(-0.33, 0.83)

def poly(pts, fc, ec='k', lw=0.8, hatch=None, z=2, hc=None):
    p = Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw, hatch=hatch, zorder=z)
    if hc is not None:
        p.set_edgecolor(hc); ax.add_patch(p)
        ax.add_patch(Polygon(pts, closed=True, fc='none', ec=ec, lw=lw, zorder=z + 0.1))
    else:
        ax.add_patch(p)
    return p

def banda(x0, x1, f0, f1, **kw):
    """Banda entre dos líneas paralelas a la pendiente: y = f0(x) .. f1(x)."""
    return poly([(x0, f0(x0)), (x1, f0(x1)), (x1, f1(x1)), (x0, f1(x0))], **kw)

plt.rcParams['hatch.linewidth'] = 0.5

# ---------- muro (fachada B) ----------
poly([(0, YBOT), (0.015, YBOT), (0.015, yb(0.015)), (0, yb(0))], G(235), lw=0.6)                    # monocapa
poly([(0.015, YBOT), (0.248, YBOT), (0.248, -0.25), (0.098, -0.25), (0.098, yb(0.098)), (0.015, yb(0.015))],
     (0.96, 0.87, 0.80), hatch='////', hc=(0.75, 0.55, 0.45))                                       # tosco y ladrillo delante
poly([(0.098, -0.25), (0.248, -0.25), (0.248, 0), (0.098, 0)], G(215), hatch='..', hc=G(120))        # zuncho
poly([(0.098, 0), (0.248, 0), (0.248, yb(0.248)), (0.098, yb(0.098))], VCLARO, ec=VERDE, lw=1.0,
     hatch='xx', hc=(0.55, 0.75, 0.68))                                                             # relleno aislante (nuevo)
poly([(0.248, YBOT), (0.263, YBOT), (0.263, yb(0.263)), (0.248, yb(0.248))], G(230), lw=0.5)         # enfoscado
poly([(0.263, YBOT), (0.363, YBOT), (0.363, yb(0.363)), (0.263, yb(0.263))], 'white', hatch='oo',
     hc=G(150))                                                                                      # EPS 100
poly([(0.363, YBOT), (0.433, YBOT), (0.433, yb(0.433)), (0.363, yb(0.363))], (0.96, 0.87, 0.80),
     hatch='----', hc=(0.75, 0.55, 0.45))                                                            # gran formato
poly([(0.433, YBOT), (0.448, YBOT), (0.448, yb(0.448)), (0.433, yb(0.433))], G(245), lw=0.5)        # yeso
for x0, x1 in ((-0.01, 0.46),):
    ax.plot([x0, x1], [YBOT, YBOT], color='k', lw=0.6, ls=(0, (6, 3)), zorder=5)

# ---------- cercha en proyección (interior) ----------
ax.add_patch(Polygon([(0.448, 0.0), (XR, 0.0), (XR, yb(XR)), (0.448, yb(0.448))], closed=True,
                     fc=G(248), ec=G(150), lw=0.6, ls='--', zorder=1))
ax.plot([0.448, XR], [0.20, 0.20], color=G(160), lw=0.5, ls='--', zorder=1)
ax.text(0.66, 0.035, 'cercha en proyección\n(tirante sobre el zuncho)', fontsize=6.3, color=G(110),
        ha='center', va='center', zorder=6)

# ---------- Thermochip ----------
banda(XT, XR, yb, lambda x: yb(x) + FR, fc=(0.93, 0.83, 0.65), lw=0.6)                                # friso
banda(XT, XR, lambda x: yb(x) + FR, lambda x: yb(x) + FR + XP, fc='white', hatch='oo', hc=G(150), lw=0.6)  # XPS
banda(XT, XR, lambda x: yb(x) + FR + XP, yt, fc=G(200), lw=0.6)                                       # aglomerado
XL = XT + 0.045 * CV                                                                                  # listón de testa
poly([(XT, yb(XT) + FR), (XL, yb(XL) + FR), (XL, yb(XL) + FR + XP), (XT, yb(XT) + FR + XP)],
     (0.80, 0.62, 0.40), ec=VERDE, lw=1.2, hatch='\\\\\\', hc=(0.55, 0.40, 0.25))
ax.plot([XR, XR], [yb(XR) - 0.01, yt(XR) + 0.01], color='k', lw=0.6, ls=(0, (6, 3)))

# ---------- frente y babero de chapa ----------
XF = XT - 0.002
yfb = yb(0) - 0.05
ax.plot([XF, XF, XF - 0.012], [yt(XT), yfb + 0.006, yfb], color=VERDE, lw=2.0, zorder=7, solid_capstyle='butt')
xb0 = 0.16
ax.plot([xb0, XT, XT - 0.006, XT - 0.006, XT - 0.022], [yt(xb0) + 0.003, yt(XT) + 0.003, yt(XT) - 0.004,
        yt(XT) - 0.030, yt(XT) - 0.042], color=VERDE, lw=2.0, zorder=8, solid_joinstyle='miter')

# ---------- canalón visto ----------
XGB, XGF = XF - 0.004, XF - 0.170
ytop_b = yt(XT) - 0.012
ytop_f = ytop_b - 0.020
ybot = ytop_b - 0.135
can = [(XGB, ytop_b), (XGB, ybot), (XGF, ybot), (XGF, ytop_f), (XGF - 0.012, ytop_f)]
ax.plot(*zip(*can), color=VERDE, lw=2.0, zorder=7)
ax.add_patch(Polygon([(XGB, ybot + 0.06), (XGB, ybot), (XGF, ybot), (XGF, ybot + 0.06)], closed=True,
                     fc=(0.85, 0.92, 0.97), ec='none', zorder=3))                                   # agua
ax.plot([XF, XGB - 0.004, XGB - 0.004, XGF - 0.006, XGF - 0.006], [ybot + 0.09, ybot + 0.09, ybot - 0.006,
        ybot - 0.006, ytop_f - 0.01], color=VERDE, lw=0.9, zorder=6)                                  # soporte
ax.plot([XF], [ybot + 0.09], marker='o', ms=2.5, color=VERDE, zorder=9)

# ---------- placa bajo teja y teja ----------
OND = 0.024 * CV
yo = lambda x: yt(x) + 0.004
XO = XT - 0.050
banda(XO, XR, yo, lambda x: yo(x) + OND, fc=G(120), ec='k', lw=0.5)
for i in range(4):                                                                                     # peine
    xp = XO + 0.012 + i * 0.010
    ax.plot([xp, xp], [yo(xp) + OND, yo(xp) + OND + 0.022], color=G(60), lw=0.7, zorder=9)
yc = lambda x: yo(x) + OND + 0.002
for x0, x1, dy in ((XT - 0.115, 0.36, 0.0), (0.27, XR, 0.016)):                                       # canales
    banda(x0, x1, lambda x, d=dy: yc(x) + d, lambda x, d=dy: yc(x) + d + 0.016, fc=(0.80, 0.42, 0.30), lw=0.6, z=4)
for x0, x1 in ((XT - 0.070, 0.40), (0.33, XR)):                                                       # cobijas, en proyección
    banda(x0, x1, lambda x: yc(x) + 0.075, lambda x: yc(x) + 0.091, fc='none', ec=G(130), lw=0.6, z=4)
ax.annotate('', xy=(0.20, yo(0.20) + 0.012), xytext=(-0.02, yo(-0.02) + 0.012),
            arrowprops=dict(arrowstyle='->', color=VERDE, lw=1.0), zorder=10)                       # aire

# ---------- cinta estanca ----------
xi = 0.448
ax.plot([xi - 0.004, xi - 0.004, xi + 0.07], [yb(xi) - 0.06, yb(xi) - 0.004, yb(xi + 0.07) - 0.004],
        color=VERDE, lw=2.2, zorder=9)

# ---------- cotas ----------
def cota_v(x, y0, y1, txt):
    ax.plot([x, x], [y0, y1], color='k', lw=0.5, zorder=9)
    for y in (y0, y1):
        ax.plot([x - 0.008, x + 0.008], [y - 0.008, y + 0.008], color='k', lw=0.7, zorder=9)
    ax.text(x - 0.012, (y0 + y1) / 2, txt, fontsize=6.5, ha='right', va='center', zorder=9,
            bbox=dict(fc='white', ec='none', alpha=0.6, pad=0.3))
cota_v(-0.29, 0, Y0, '17\n(= DET-01)')
ax.plot([-0.30, 0.098], [0, 0], color=G(140), lw=0.4, ls=':', zorder=1)
ax.plot([-0.30, -0.012], [Y0, Y0], color=G(140), lw=0.4, ls=':', zorder=1)
yh = ybot - 0.06
ax.plot([XGF, 0], [yh, yh], color='k', lw=0.5)
for x in (XGF, 0):
    ax.plot([x - 0.008, x + 0.008], [yh - 0.008, yh + 0.008], color='k', lw=0.7)
ax.text(XGF - 0.015, yh, '≈ 19 cm de vuelo total\n(DET-01: 56 cm)', fontsize=6.5, ha='right', va='center')
ax.plot([0, 0], [yh - 0.01, yfb - 0.01], color=G(140), lw=0.4, ls=':')
ax.text(-0.21, -0.20, 'EXTERIOR', fontsize=7.5, color=G(90), ha='center')
ax.text(0.66, -0.24, 'INTERIOR', fontsize=7.5, color=G(90), ha='center')

# ---------- burbujas ----------
def burb(n, p, q):
    ax.plot([p[0], q[0]], [p[1], q[1]], color='k', lw=0.5, zorder=11)
    ax.plot(*p, marker='o', ms=2.2, color='k', zorder=11)
    ax.add_patch(Circle(q, 0.021, fc='white', ec=VERDE if n in VERDES else 'k', lw=1.0, zorder=12))
    ax.text(*q, str(n), fontsize=6.8, ha='center', va='center', zorder=13,
            color=VERDE if n in VERDES else 'k', fontweight='bold')
VERDES = {3, 5, 6, 7, 9, 11}
burb(1, (0.05, yc(0.05) + 0.008), (0.02, 0.62))
burb(2, (0.12, yo(0.12) + 0.012), (0.10, 0.66))
burb(3, (0.08, yt(0.08) + 0.003), (0.18, 0.70))
burb(4, (0.40, yb(0.40) + 0.13), (0.40, 0.74))
burb(5, (XT + 0.02, yb(XT) + 0.10), (-0.13, 0.47))
burb(6, (XF, yb(0) - 0.02), (-0.13, 0.03))
burb(7, (XGF + 0.04, ybot + 0.03), (-0.34, 0.33))
burb(8, (0.05, 0.10), (-0.13, -0.07))
burb(9, (0.17, 0.10), (0.56, 0.30))
burb(10, (0.31, 0.06), (0.56, 0.21))
burb(11, (xi - 0.004, yb(xi) - 0.03), (0.52, 0.40))
burb(12, (0.20, -0.12), (0.56, -0.10))

ley = [
    (1, 'Teja curva: la canal vuela unos 6 cm sobre el canalón; cobijas en proyección'),
    (2, 'Placa bajo teja Onduline: vuela 5 cm; peine de alero que deja entrar el aire'),
    (3, 'Babero de chapa: 15 cm sobre el panel, bajo la placa; gotea dentro del canalón'),
    (4, 'Thermochip TAH 10-200-19, cortado a plomo 1 cm por fuera de la fachada'),
    (5, 'Listón de madera tratada de 45 mm en la testa, encolado y atornillado:\n     cierra el XPS y da agarre al frente y al canalón'),
    (6, 'Frente de chapa sobre el listón: baja 5 cm por delante del monocapa,\n     separado y con goterón'),
    (7, 'Canalón visto colgado del frente; soportes cada 50 cm;\n     borde delantero 2 cm más bajo (si rebosa, cae fuera)'),
    (8, 'Ladrillo de 8 cm hasta el panel: base continua del monocapa'),
    (9, 'Entre cerchas, relleno aislante sobre el zuncho, sin durmiente'),
    (10, 'Aislamiento de la fachada B hasta el panel: envolvente continua'),
    (11, 'Cinta estanca al aire entre el friso y el yeso, por dentro'),
    (12, 'Zuncho de coronación; la cercha apoya en él con herraje de acero'),
]
yy = 0.80
ax.text(0.86, yy, 'OPCIÓN A · SIN ALERO, CANALÓN VISTO', fontsize=9.5, fontweight='bold', color=VERDE, va='top')
ax.text(0.86, yy - 0.042, 'Sección entre cerchas · esquema a escala, cotas en cm\nEn verde, lo que cambia frente a la ficha 03',
        fontsize=6.6, color=G(80), va='top')
yy -= 0.12
for n, t in ley:
    ax.add_patch(Circle((0.875, yy - 0.010), 0.016, fc='white', ec=VERDE if n in VERDES else 'k', lw=0.9))
    ax.text(0.875, yy - 0.010, str(n), fontsize=6.2, ha='center', va='center', fontweight='bold',
            color=VERDE if n in VERDES else 'k')
    ax.text(0.90, yy, t, fontsize=6.6, va='top', linespacing=1.25)
    yy -= 0.040 + 0.030 * t.count('\n')

fig.savefig(sys.argv[1], bbox_inches='tight', pad_inches=0.08, facecolor='white')
print('ok', fam)
