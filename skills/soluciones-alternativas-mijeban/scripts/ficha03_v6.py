"""Ficha 03 v6 · (v5 + durmiente 150 × 200, ladrillo enrasado, banda impermeable y Onduline sin onda) · cubierta inclinada con peto de ladrillo, sin durmiente y con canalón visto (pizarra del usuario, 2026-11-09).

Parte de la v4 (f4/v4.dxf):
- Sección del alero: se borra entera y se redibuja por un par de cercha. El ladrillo sube a soga hasta la cara superior
  del panel y lo recoge; junta de espuma; par apoyado en el tosco con placa de acero (sin durmiente ni zuncho); canalón
  visto anclado al ladrillo; goterón bajo el Onduline. Onduline como chapa ondulada y teja separada de ella.
- Axonometría: sin durmiente; pares cortados donde acaba el panel; muro de apoyo en gris; peto y canalón en verde.
- Textos: leyenda, cifras, lo que cambia, entradilla, pie (v5) y 2.3.1 «Suelos sobre forjado sanitario y sótano».
Uso: python ficha03_v5.py f4/v4.dxf f5/v5.dxf
"""
import sys, math
sys.path.insert(0, r"C:\Users\usuario\AppData\Local\Temp\claude\db3e6b77c6882b90\bc43d6f6-dd79-406e-a22c-6ef32f44ca96\scratchpad")
import ezdxf
from ezdxf import bbox, path as ezpath
from ezdxf.enums import TextEntityAlignment
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union
from medir import lineas

ENT, SAL = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(ENT); E = doc.entitydb; msp = doc.modelspace(); psp = doc.layouts.get("FICHA-A4")
tc = lambda c: (c[0] << 16) | (c[1] << 8) | c[2]
VERDE, VERDE_T, VERDE_M, VERDE_O = (7, 87, 72), (224, 235, 231), (210, 226, 220), (195, 214, 208)
GRIS_OSC = (40, 40, 40)

def poly(pts, capa, rgb=None, cerrada=False, lw=None, sp=None):
    a = {"layer": capa}
    if rgb is not None: a["true_color"] = tc(rgb)
    if lw is not None: a["lineweight"] = lw
    return (sp or msp).add_lwpolyline(pts, close=cerrada, dxfattribs=a)

def solido(pts, rgb, capa="A-WALL-PATT"):
    h = msp.add_hatch(dxfattribs={"layer": capa}); h.set_solid_fill(rgb=rgb)
    h.paths.add_polyline_path(pts, is_closed=True); return h

def trama(pts, patron, escala, rgb, capa="A-WALL-PATT", ang=0.0):
    h = msp.add_hatch(dxfattribs={"layer": capa, "true_color": tc(rgb)})
    h.set_pattern_fill(patron, scale=escala, angle=ang)
    h.paths.add_polyline_path(pts, is_closed=True); return h

# =====================================================================================================  SECCIÓN DEL ALERO
S = 0.268
CV = 1 / math.cos(math.atan(S))
FR, XP, TB = 0.010 * CV, 0.200 * CV, 0.019 * CV
PANEL = FR + XP + TB
D = 0.180 * CV                         # par GL24h 140 × 180 (licitación 04.12)
SEAT = 0.0                             # el par apoya en el durmiente
XU, XT, XZ1 = 0.098, 0.108, 0.248      # cara interior del peto (= cara exterior del durmiente), testa de panel y par, cara interior del tosco
XD0, XD1, YD0 = 0.098, 0.248, -0.200   # durmiente 150 × 200, a haces con el tosco por dentro
YC, XR = -0.330, 0.500                 # cortes del dibujo
yb = lambda x: SEAT + D + S * (x - XZ1)         # cara inferior del panel = cara superior del par
yt = lambda x: yb(x) + PANEL                     # cara superior del panel = coronación del peto
yv = lambda x: max(yb(x) - D, SEAT)              # cara inferior del par (asiento horizontal sobre la placa)
X_ENF, X_EPS, X_GF, X_YESO, X_INT = 0.248, 0.263, 0.363, 0.430, 0.445

# ---- 0 · se guardan los bucles del v4 (EPS del muro y XPS del panel) y se borra la sección antigua
PU4 = lambda x: 0.096 + (x + 0.276) * S          # cara inferior del panel en la v4
DY = yb(0.0) - PU4(0.0)                          # el panel baja en vertical
bucles_eps, bucles_xps = [], []
borrar = []
for e in msp:
    b = bbox.extents([e], fast=True)
    if not (b.has_data and -0.75 < b.extmin.x and b.extmax.x < 0.70 and -0.45 < b.extmin.y and b.extmax.y < 0.80):
        continue
    if e.dxf.layer == "A-DETL-AISL":
        pts = [(x, y) for x, y in e.get_points("xy")]
        if 0.262 <= b.extmin.x and b.extmax.x <= 0.364 and b.extmax.y < 0.09:
            bucles_eps.append(pts)
        else:
            bucles_xps.append([(x, y + DY) for x, y in pts])
    borrar.append(e)
for e in borrar:
    msp.delete_entity(e)
print(f"sección v4 borrada: {len(borrar)} entidades; bucles EPS {len(bucles_eps)}, XPS {len(bucles_xps)}")

def bucles(lista, region, rgb=(85, 85, 85)):
    n = 0
    for pts in lista:
        g = LineString(pts).intersection(region)
        for s in getattr(g, "geoms", [g]):
            if not s.is_empty and s.geom_type == "LineString" and s.length > 1e-4:
                poly(list(s.coords), "A-DETL-AISL", rgb); n += 1
    return n

# ---- 1 · muro (fachada B), cortado por un par
TOP_I = lambda x: yv(x)                          # las capas interiores llegan a la cara inferior del par
solido([(0, YC), (0.015, YC), (0.015, yt(0.015)), (0, yt(0))], (255, 255, 255))
trama([(0, YC), (0.015, YC), (0.015, yt(0.015)), (0, yt(0))], "AR-SAND", 0.012, (120, 120, 120))
poly([(0, YC), (0, yt(0)), (0.015, yt(0.015)), (0.015, YC)], "A-WALL-CAPAS")                     # monocapa
tosco = [(0.015, YC), (XZ1, YC), (XZ1, YD0), (XD0, YD0), (XD0, 0.0), (0.015, 0.0)]
trama(tosco, "ANSI31", 0.006, (175, 175, 175))
poly([(0.015, 0.0), (0.015, YC)], "A-WALL"); poly([(XZ1, YC), (XZ1, YD0)], "A-WALL")
dur = [(XD0, YD0), (XD1, YD0), (XD1, 0.0), (XD0, 0.0)]
solido(dur, (214, 229, 224)); poly(dur, "A-WALL", VERDE, cerrada=True)
poly([(XD0, YD0), (XD1, 0.0)], "A-DETL-THIN", VERDE); poly([(XD1, YD0), (XD0, 0.0)], "A-DETL-THIN", VERDE)
peto = [(0.015, 0.0), (XU, 0.0), (XU, yt(XU)), (0.015, yt(0.015))]
solido(peto, VERDE_T)
trama(peto, "ANSI31", 0.006, (110, 150, 138))
poly(peto, "A-WALL", VERDE, cerrada=True)
for k in (1, 2, 3):                                                                                # hiladas de 10,6
    poly([(0.015, 0.106 * k), (XU, 0.106 * k)], "A-DETL-THIN", (120, 160, 148))
enf = [(X_ENF, YC), (X_EPS, YC), (X_EPS, TOP_I(X_EPS)), (X_ENF, TOP_I(X_ENF))]
solido(enf, (255, 255, 255)); trama(enf, "AR-SAND", 0.012, (150, 150, 150)); poly(enf, "A-WALL-CAPAS", cerrada=True)
eps = [(X_EPS, YC), (X_GF, YC), (X_GF, TOP_I(X_GF)), (X_EPS, TOP_I(X_EPS))]
solido(eps, (255, 255, 255)); poly(eps, "A-WALL-CAPAS", cerrada=True)
print("bucles EPS:", bucles(bucles_eps, Polygon(eps)))
gf = [(X_GF, YC), (X_YESO, YC), (X_YESO, TOP_I(X_YESO)), (X_GF, TOP_I(X_GF))]
solido(gf, (222, 222, 222)); poly(gf, "A-WALL", cerrada=True)
for k in range(6):                                                                                 # huecos del gran formato
    y0 = -0.316 + 0.053 * k
    for x0 in (0.370, 0.400):
        h = [(x0, y0), (x0 + 0.023, y0), (x0 + 0.023, y0 + 0.045), (x0, y0 + 0.045)]
        solido(h, (255, 255, 255)); poly(h, "A-DETL-THIN", cerrada=True)
poly([(X_GF, 0.011), (X_YESO, 0.011)], "A-WALL-CAPAS")                                            # junta entre piezas
yeso = [(X_YESO, YC), (X_INT, YC), (X_INT, TOP_I(X_INT)), (X_YESO, TOP_I(X_YESO))]
solido(yeso, (255, 255, 255)); trama(yeso, "AR-SAND", 0.012, (185, 185, 185)); poly(yeso, "A-WALL-CAPAS", cerrada=True)

# ---- 2 · placa y par (cortado a lo largo, gris claro con vetas)
xs = [XT + i * (XR - XT) / 80 for i in range(81)]
par = [(x, yv(x)) for x in xs] + [(XR, yb(XR)), (XT, yb(XT))]
solido(par, (238, 238, 238))
poly(par, "A-WALL", GRIS_OSC, cerrada=True)
pol_par = Polygon(par)
for off in (0.045, 0.093, 0.1395):
    l = LineString([(XT - 0.1, yb(XT - 0.1) - off), (XR + 0.1, yb(XR + 0.1) - off)]).intersection(pol_par.buffer(-0.004))
    for s in getattr(l, "geoms", [l]):
        if s.length > 0.01:
            poly(list(s.coords), "A-DETL-THIN", (130, 130, 130))

# ---- 3 · Thermochip: friso, XPS con bucles, aglomerado; testa a plomo contra el ladrillo con junta de espuma
fr = [(XT, yb(XT)), (XR, yb(XR)), (XR, yb(XR) + FR), (XT, yb(XT) + FR)]
xp = [(XT, yb(XT) + FR), (XR, yb(XR) + FR), (XR, yb(XR) + FR + XP), (XT, yb(XT) + FR + XP)]
ag = [(XT, yb(XT) + FR + XP), (XR, yb(XR) + FR + XP), (XR, yt(XR)), (XT, yt(XT))]
solido(fr, (226, 226, 226)); poly(fr, "A-WALL-CAPAS", cerrada=True)
solido(xp, (255, 255, 255)); poly(xp, "A-WALL-CAPAS", cerrada=True)
print("bucles XPS:", bucles(bucles_xps, Polygon(xp).buffer(-0.002)))
solido(ag, (190, 190, 190)); poly(ag, "A-WALL-CAPAS", cerrada=True)
BANDA = [(XD1, YD0 - 0.002), (XD0 - 0.002, YD0 - 0.002), (XD0 - 0.002, yb(XT))]
poly(BANDA, "A-WALL", VERDE, lw=50)
junta = [(XU, yb(XT)), (XT, yb(XT)), (XT, yt(XT)), (XU, yt(XU))]
solido(junta, VERDE); poly(junta, "A-DETL-THIN", VERDE, cerrada=True)

# ---- 4 · goterón, Onduline (chapa ondulada) y teja separada
GOT = [(0.090, yt(0.090) + 0.002), (-0.006, yt(-0.006) + 0.002), (-0.010, yt(-0.010) - 0.004), (-0.010, yt(0) - 0.050)]
poly(GOT, "A-WALL", VERDE, lw=35)
X_OND = -0.050
y_o = lambda x: yt(x) + 0.004
AMP, PASO = 0.024 * CV, 0.048
chapa = [(X_OND, y_o(X_OND)), (XR, y_o(XR)), (XR, y_o(XR) + 0.004), (X_OND, y_o(X_OND) + 0.004)]
solido(chapa, (70, 70, 70)); poly(chapa, "A-WALL-CAPAS", (40, 40, 40), cerrada=True)              # placa cortada en el valle
poly([(X_OND, y_o(X_OND) + AMP), (XR, y_o(XR) + AMP)], "A-DETL-THIN", (110, 110, 110))           # cresta, vista detrás
poly([(X_OND, y_o(X_OND) + 0.004), (X_OND, y_o(X_OND) + AMP)], "A-DETL-THIN", (110, 110, 110))
for i in range(5):                                                                                 # peine de alero
    xp_ = X_OND + 0.006 + i * 0.008
    poly([(xp_, y_o(xp_)), (xp_, y_o(xp_) + AMP + 0.012)], "A-DETL-THIN", VERDE)
y_c = lambda x: y_o(x) + AMP + 0.006                                                               # apoyo de la canal
CAN_T = 0.016
def pieza(x0, x1, base, alto, rgb, capa_lin="A-DETL-THIN", rgb_lin=None):
    pts = [(x0, base(x0)), (x1, base(x1)), (x1, base(x1) + alto), (x0, base(x0) + alto)]
    if rgb is not None:
        solido(pts, rgb)
    poly(pts, capa_lin, rgb_lin, cerrada=True)
    return pts
canales = [(-0.115, 0.285, 0.0), (0.215, XR, CAN_T)]
for x0, x1, d in canales:
    pieza(x0, x1, lambda x, d=d: y_c(x) + d, CAN_T, (200, 200, 200), "A-WALL-CAPAS")
COB_DY = 0.060
for x0, x1, d in ((-0.075, 0.325, 0.0), (0.255, XR, CAN_T)):                                       # cobijas, vistas
    pieza(x0, x1, lambda x, d=d: y_c(x) + COB_DY + d, CAN_T, (240, 240, 240), "A-DETL-THIN", (110, 110, 110))
# aire: bajo la teja, de alero a cumbrera
fl = [(-0.020, y_o(-0.020) + AMP * 0.5), (0.250, y_o(0.250) + AMP * 0.5)]
poly(fl, "A-DETL", VERDE)
ang = math.atan(S); xa, ya_ = fl[1]
poly([(xa - 0.022 * math.cos(ang) - 0.008 * math.sin(ang), ya_ - 0.022 * math.sin(ang) + 0.008 * math.cos(ang)), (xa, ya_),
      (xa - 0.022 * math.cos(ang) + 0.008 * math.sin(ang), ya_ - 0.022 * math.sin(ang) - 0.008 * math.cos(ang))], "A-DETL", VERDE)

# ---- 5 · canalón visto anclado al ladrillo
XGB, XGF = -0.004, -0.174
G_TB = yt(0) - 0.030; G_TF = G_TB - 0.020; G_B = G_TB - 0.135
poly([(XGB, G_TB), (XGB, G_B), (XGF, G_B), (XGF, G_TF), (XGF - 0.012, G_TF)], "A-WALL", VERDE, lw=35)
ya = G_B + 0.050
poly([(0.060, ya), (XGB - 0.003, ya), (XGB - 0.003, G_B - 0.006), (XGF - 0.005, G_B - 0.006), (XGF - 0.005, G_TF - 0.012)],
     "A-DETL", VERDE)
anc = [(0.0, ya - 0.006), (0.060, ya - 0.006), (0.060, ya + 0.006), (0.0, ya + 0.006)]
solido(anc, VERDE_T); poly(anc, "A-DETL-THIN", VERDE, cerrada=True)
assert G_B > 0.15 and G_TB < yt(0) - 0.02

# ---- 6 · cinta estanca por dentro
poly([(X_INT + 0.003, yv(X_INT) - 0.050), (X_INT + 0.003, yv(X_INT) - 0.003), (X_INT + 0.060, yv(X_INT + 0.060) - 0.003)],
     "A-WALL", VERDE, lw=35)

# ---- 7 · líneas de rotura
poly([(-0.020, YC), (0.180, YC), (0.195, YC + 0.020), (0.215, YC - 0.020), (0.230, YC), (X_INT + 0.025, YC)], "A-DETL-THIN")
ytop_r = y_c(XR) + COB_DY + 2 * CAN_T + 0.015
ym = (yv(XR) + ytop_r) / 2
poly([(XR, yv(XR) - 0.025), (XR, ym - 0.015), (XR + 0.018, ym - 0.005), (XR - 0.018, ym + 0.005), (XR, ym + 0.015),
      (XR, ytop_r)], "A-DETL-THIN")

# ---- 8 · textos del dibujo y pendiente
def texto(t, xy, h, rgb, alin=TextEntityAlignment.LEFT, estilo="1-10 (0.20)", capa="A_06_TEXTOS"):
    e = msp.add_text(t, height=h, dxfattribs={"layer": capa, "style": estilo, "true_color": tc(rgb)})
    e.set_placement(xy, align=alin); return e
texto("EXTERIOR", (-0.660, -0.170), 0.036, (110, 110, 110))
texto("FACHADA B (FICHA 02)", (-0.660, -0.215), 0.030, (140, 140, 140))
texto("INTERIOR", (0.470, -0.120), 0.030, (110, 110, 110))
xp27 = 0.040
y27 = y_c(xp27) + COB_DY + CAN_T + 0.095
poly([(xp27, y27), (xp27 + 0.120, y27 + 0.120 * S), (xp27 + 0.120, y27)], "A-DETL-THIN")
texto("27 %", (xp27 + 0.010, y27 - 0.050), 0.036, (110, 110, 110))

# ---- 9 · números (círculo verde con cifra blanca, directriz y punto)
R_C, R_P = 0.037, 0.009
def numero(n, centro, destino):
    cx, cy = centro
    dx, dy = destino[0] - cx, destino[1] - cy; L = math.hypot(dx, dy)
    poly([(cx + dx / L * R_C, cy + dy / L * R_C), destino], "A-NUMEROS", (70, 70, 70), lw=13)
    for c, r in ((destino, R_P), (centro, R_C)):
        h = msp.add_hatch(dxfattribs={"layer": "A-NUMEROS"}); h.set_solid_fill(rgb=VERDE)
        h.paths.add_edge_path().add_arc(c, r, 0, 360)
    t = msp.add_text(str(n), height=0.040, dxfattribs={"layer": "A-NUMEROS", "style": "1-10 NEGRITA", "true_color": tc((255, 255, 255))})
    t.set_placement((cx, cy), align=TextEntityAlignment.MIDDLE_CENTER)
XD, XI = 0.610, -0.662
numero(6, (XD, 0.700), (0.400, y_c(0.400) + CAN_T + CAN_T / 2))
numero(5, (XD, 0.560), (0.440, y_o(0.440) + 0.004))
numero(3, (XD, 0.380), (0.420, yb(0.420) + FR + XP / 2))
numero(2, (XD, 0.150), (0.400, (yv(0.400) + yb(0.400)) / 2))
numero(7, (XI, 0.240), (XGF, 0.260))
numero(4, (XI, 0.095), (0.056, 0.110))
numero(1, (XI, -0.050), ((XD0 + XD1) / 2, YD0 / 2))

# ---- 10 · ventana de la sección: misma posición y tamaño en papel, 1:20
vp = E["3C0"]
K = 50.0                                              # mm de papel por m a 1:20
cont = bbox.extents([e for e in msp if (lambda b: b.has_data and -0.75 < b.extmin.x and b.extmax.x < 0.75 and -0.45 < b.extmin.y and b.extmax.y < 0.85)(bbox.extents([e], fast=True))])
print(f"sección: x {cont.extmin.x:.3f} a {cont.extmax.x:.3f}, y {cont.extmin.y:.3f} a {cont.extmax.y:.3f}")
ancho_m, alto_m = vp.dxf.width / K, vp.dxf.height / K
assert cont.extmax.x - cont.extmin.x < ancho_m - 0.02 and cont.extmax.y - cont.extmin.y < alto_m - 0.02
vp.dxf.view_height = alto_m
vp.dxf.view_center_point = ((cont.extmin.x + cont.extmax.x) / 2, (cont.extmin.y + cont.extmax.y) / 2, 0)

# =====================================================================================================  AXONOMETRÍA
M = 0.268; C = math.cos(math.radians(30)); OX, OY = 0.032, -3.0875
P = lambda X, Y, Z: (OX + C * (X + Y), OY - 0.5 * X + 0.5 * Y + Z)
ZT = lambda Y: 0.074 + M * Y                         # cara superior del par = cara inferior del panel
Y_PANEL = 0.241                                      # cara delantera del panel en la axo (abajo)
DXA = Y_PANEL - XT; DZA = ZT(Y_PANEL) - yb(XT)       # Y = x_sección + DXA ; Z = y_sección + DZA
assert abs(ZT(XT + DXA) - (yb(XT) + DZA)) < 1e-3, (ZT(XT + DXA), yb(XT) + DZA)
Y_ = lambda x: x + DXA; Z_ = lambda y: y + DZA
VENT = (-0.6, 2.3, -4.3, -1.6)
def en_axo(e):
    b = bbox.extents([e], fast=True)
    return b.has_data and VENT[0] < b.extmin.x and b.extmax.x < VENT[1] and VENT[2] < b.extmin.y and b.extmax.y < VENT[3]
QUITAR = [f"{h:X}" for h in range(0x532, 0x550)]       # durmiente, pares y cota de la v4
cota_txt = E["54F"]
TXT_ATTR = {k: cota_txt.dxf.get(k) for k in ("layer", "style", "true_color", "height", "rotation", "width") if cota_txt.dxf.hasattr(k)}
REF_ATTR = {k: E["54A"].dxf.get(k) for k in ("layer", "true_color", "lineweight") if E["54A"].dxf.hasattr(k)}
COTA_ATTR = {k: E["54C"].dxf.get(k) for k in ("layer", "true_color", "lineweight") if E["54C"].dxf.hasattr(k)}
silu = []
for e in msp:
    if e.dxf.handle in QUITAR or not en_axo(e) or e.dxftype() != "HATCH" or e.dxf.layer != "A-AXO-COLOR":
        continue
    for p in ezpath.from_hatch(e):
        pts = [(v.x, v.y) for v in p.flattening(0.0005)]
        if len(pts) >= 3:
            g = Polygon(pts).buffer(0)
            if g.area > 1e-8: silu.append(g)
panel_sil = unary_union(silu)
for h in QUITAR:
    msp.delete_entity(E[h])

def partes(g):
    return [p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and p.area > 2e-7]
def dibuja(g, rgb, rgb_lin=None, capa_lin="A-AXO-LIN"):
    for p in partes(g):
        h = msp.add_hatch(dxfattribs={"layer": "A-AXO-COLOR"}); h.set_solid_fill(rgb=rgb)
        h.paths.add_polyline_path(list(p.exterior.coords)[:-1], is_closed=True, flags=1)
        for r in p.interiors:
            h.paths.add_polyline_path(list(r.coords)[:-1], is_closed=True, flags=0)
        a = {"layer": capa_lin}
        if rgb_lin: a["true_color"] = tc(rgb_lin)
        msp.add_lwpolyline(list(p.exterior.coords), dxfattribs=a)
        for r in p.interiors:
            msp.add_lwpolyline(list(r.coords), dxfattribs=a)
def cara(pts3):
    return Polygon([P(*q) for q in pts3])

# piezas 3D
XA, XB = -0.20, 1.30                                 # durmiente, cortado a ambos lados
XP0, XP1 = 0.12, 0.94                                # ladrillo de delante (abajo gris, peto verde), entre los pares
YW0 = Y_(0.0); YP1 = Y_(XU)
YD_0, YD_1, ZD0, ZD1 = Y_(XD0), Y_(XD1), Z_(YD0), Z_(0.0)
ZTOP = lambda Y: Z_(yt(Y - DXA))
PARES = [(-0.14, 0.0), (1.06, 1.20)]
YPE = Y_(XT)
YB_T, YB_B = 1.0141, 1.0607                          # testas traseras, como en la v4
par_yz = [(YPE, Z_(SEAT)), (Y_(XZ1), Z_(SEAT)), (YB_B, ZT(YB_B) - D), (YB_T, ZT(YB_T)), (YPE, ZT(YPE))]
assert abs(ZT(Y_(XZ1)) - D - Z_(SEAT)) < 2e-3

def caras_par(X0, X1):
    out = [("lado", [(X1, y, z) for y, z in par_yz])]
    for (ya_, za), (yb_, zb) in zip(par_yz, par_yz[1:] + par_yz[:1]):
        ny, nz = zb - za, -(yb_ - ya_)
        if -ny + nz > 1e-9:
            tipo = "testa" if abs(ya_ - YPE) < 1e-6 and abs(yb_ - YPE) < 1e-6 else "arriba"
            out.append((tipo, [(X0, ya_, za), (X1, ya_, za), (X1, yb_, zb), (X0, yb_, zb)]))
    return out

gut_sil = Polygon()                                  # el canalón solo va en la sección
lad_front = [(XP0, YW0, ZD0), (XP1, YW0, ZD0), (XP1, YW0, ZD1), (XP0, YW0, ZD1)]
lad_end = [(XP1, YW0, ZD0), (XP1, YP1, ZD0), (XP1, YP1, ZD1), (XP1, YW0, ZD1)]
peto_front = [(XP0, YW0, ZD1), (XP1, YW0, ZD1), (XP1, YW0, ZTOP(YW0)), (XP0, YW0, ZTOP(YW0))]
peto_top = [(XP0, YW0, ZTOP(YW0)), (XP1, YW0, ZTOP(YW0)), (XP1, YP1, ZTOP(YP1)), (XP0, YP1, ZTOP(YP1))]
peto_end = [(XP1, YW0, ZD1), (XP1, YP1, ZD1), (XP1, YP1, ZTOP(YP1)), (XP1, YW0, ZTOP(YW0))]
peto_sil = unary_union([cara(f) for f in (lad_front, lad_end, peto_front, peto_top, peto_end)])
pares_caras = [(t, f) for X0, X1 in PARES for t, f in caras_par(X0, X1)]
pares_sil = unary_union([cara(f) for _, f in pares_caras])
dur_top = [(XA, YD_0, ZD1), (XB, YD_0, ZD1), (XB, YD_1, ZD1), (XA, YD_1, ZD1)]
dur_front = [(XA, YD_0, ZD0), (XB, YD_0, ZD0), (XB, YD_0, ZD1), (XA, YD_0, ZD1)]
dur_end = [(XB, YD_0, ZD0), (XB, YD_1, ZD0), (XB, YD_1, ZD1), (XB, YD_0, ZD1)]

# 1 · durmiente (verde, como en la v4): lo tapan pares, panel y ladrillo
ocl = unary_union([pares_sil, panel_sil, peto_sil])
for f, rgb in ((dur_top, (224, 235, 231)), (dur_front, (210, 226, 220)), (dur_end, (195, 214, 208))):
    dibuja(cara(f).difference(ocl), rgb, VERDE, "A-AXO-VERDE")
fin = cara(dur_end).difference(ocl)
for a, b in ((0, 2), (1, 3)):                        # aspa: el durmiente está cortado
    l = LineString([P(*dur_end[a]), P(*dur_end[b])]).intersection(fin.buffer(1e-6))
    for s in getattr(l, "geoms", [l]):
        if s.length > 1e-4:
            poly(list(s.coords), "A-AXO-VERDE", VERDE)
# 2 · pares (gris): los tapan el panel y el ladrillo
COL_PAR = {"arriba": (238, 238, 238), "lado": (230, 230, 230), "testa": (222, 222, 222)}
ocl = unary_union([panel_sil, peto_sil])
for t, f in pares_caras:
    dibuja(cara(f).difference(ocl), COL_PAR[t])
# 3 · ladrillo de delante: abajo, el de siempre (gris); arriba, el peto (verde)
for f, rgb in ((lad_front, (232, 232, 232)), (lad_end, (222, 222, 222))):
    dibuja(cara(f), rgb)
for f, rgb in ((peto_front, (228, 238, 234)), (peto_top, (214, 229, 224)), (peto_end, (200, 218, 211))):
    dibuja(cara(f), rgb, VERDE, "A-AXO-VERDE")
for f, col in ((lad_end, (150, 150, 150)), (peto_end, (120, 160, 148))):
    h = msp.add_hatch(dxfattribs={"layer": "A-AXO-DET", "true_color": tc(col)})
    h.set_pattern_fill("ANSI31", scale=0.009); h.paths.add_polyline_path([P(*q) for q in f], is_closed=True)
for k in (1, 2, 3):                                  # hiladas del peto
    zk = ZD1 + 0.106 * k
    for a, b in (((XP0, YW0, zk), (XP1, YW0, zk)), ((XP1, YW0, zk), (XP1, YP1, zk))):
        poly([P(*a), P(*b)], "A-AXO-VERDE", (100, 145, 132), lw=9)

# 5 · cota «1,20 m máx.» delante, por debajo del muro
Y_C, Z_C = YW0 - 0.120, ZD0
xe = [(X0 + X1) / 2 for X0, X1 in PARES]
for x_ in xe:
    msp.add_lwpolyline([P(x_, YD_0 - 0.01, Z_C), P(x_, Y_C - 0.03, Z_C)], dxfattribs=REF_ATTR)
c0, c1 = P(xe[0], Y_C, Z_C), P(xe[1], Y_C, Z_C)
msp.add_lwpolyline([c0, c1], dxfattribs=COTA_ATTR)
for q in (c0, c1):
    msp.add_lwpolyline([(q[0] - 0.0335, q[1] - 0.009), (q[0] + 0.0335, q[1] + 0.009)], dxfattribs=COTA_ATTR)
mid = ((c0[0] + c1[0]) / 2, (c0[1] + c1[1]) / 2)
t = msp.add_text("1,20 m máx.", dxfattribs=TXT_ATTR)
t.set_placement((mid[0] - 0.5 * 0.13, mid[1] - C * 0.13), align=TextEntityAlignment.MIDDLE_CENTER)

# 6 · números: el 1 al durmiente; el 4, nuevo, al peto (copia del 1)
punto_1 = P(1.02, YD_0, (ZD0 + ZD1) / 2)
punto_4 = P(0.45, YW0, Z_(0.20))
assert Point(punto_4).within(cara(peto_front)), "el punto del 4 no se ve"

punto_2 = (1.9296, -2.9055)
assert Point(punto_2).within(unary_union([cara(f) for _, f in pares_caras]).difference(panel_sil).buffer(1e-4)), "el 2 no se ve"
lead1, dot1, circ1, txt1 = E["560"], E["561"], E["562"], E["563"]
def centro_arco(h):
    for p in h.paths:
        for ed in getattr(p, "edges", []):
            if getattr(ed, "EDGE_TYPE", "") == "ArcEdge":
                return (ed.center[0], ed.center[1])
c_old = centro_arco(dot1)
pts = [(x, y) for x, y in lead1.get_points("xy")]
assert Point(punto_1).within(cara(dur_front).difference(unary_union([pares_sil, panel_sil, peto_sil]))), "el punto del 1 no se ve"
DY4 = 0.400
for e in (lead1, dot1, circ1, txt1):
    c = e.copy(); msp.add_entity(c); c.translate(0, DY4, 0)
    if e is txt1:
        c.dxf.text = "4"
    if e is lead1:
        q = [(x, y + DY4) for x, y in pts]; q[0] = punto_4; c.set_points(q, format="xy")
    if e is dot1:
        cc = centro_arco(c); c.translate(punto_4[0] - cc[0], punto_4[1] - cc[1], 0)
pts[0] = punto_1; lead1.set_points(pts, format="xy")
dot1.translate(punto_1[0] - c_old[0], punto_1[1] - c_old[1], 0)
# los números, encima de todo
for h in ("550", "551", "552", "553", "554", "555", "556", "557", "558", "559", "55A", "55B", "55C", "55D", "55E", "55F",
          "560", "561", "562", "563"):
    c = E[h].copy(); msp.add_entity(c); msp.delete_entity(E[h])

# =====================================================================================================  TEXTOS
def cambia(h, t, max_lineas=None):
    e = E[h]
    n0 = len(lineas(e.text.replace("\\P", " "), e.dxf.char_height, e.dxf.width)[0]) if e.dxf.width else e.text.count("\\P") + 1
    n1 = len(lineas(t, e.dxf.char_height, e.dxf.width)[0]) if e.dxf.width else t.count("\\P") + 1
    lim = max_lineas if max_lineas is not None else n0
    print(f"{h}: {n0} → {n1} líneas · {t[:70]}")
    assert n1 <= lim, (h, n0, n1, t)
    e.text = t
cambia("3BD", "\\T1.3;TIPO VENTILADA, SOBRE CERCHAS")
cambia("3BE", "El panel sándwich del proyecto, con friso de abeto visto, sobre cerchas a 1,20 m como máximo apoyadas "
              "en un durmiente. El ladrillo sube y recoge el panel; canalón visto. Placa ventilada y teja sin mortero.")
cambia("3C2", "Durmiente de madera de canto con banda impermeable")
cambia("3C3", "150 × 200 mm, a calcular")
cambia("3C5", "Par de cercha GL24h 140 × 180")

cambia("3CB", "Peto de ladrillo enrasado con el durmiente")
cambia("3D3", "Canalón visto anclado al ladrillo, con goterón", 3)
cambia("39F", "Separación máxima entre cerchas")
cambia("3AA", "Cerchas")
cambia("3AB", "Sin empuje al muro")
cambia("3AC", "Proyecto: pares, atado «opcional»")
cambia("3B1", "Cerchas y durmiente,\\Ppendientes del cálculo\\Pestructural y de la DF.")
cambia("3E4", "Cerchas a 1,20 m como máximo (proyecto: pares hasta 1,83 m).")
cambia("3E6", "Durmiente de madera en lugar de viga de hormigón.")
cambia("3E8", "El ladrillo sube y recoge el panel.")
cambia("3EC", "Canalón visto, anclado al ladrillo.")
cambia("3EE", "Teja con espuma y cumbrera en seco.")
cambia("3F0", "Banda impermeable contra la madera; junta y cinta estanca.", 2)
cambia("3F2", "Panel con cinta en juntas, Onduline y cobijas de derribo.")
cambia("3F3", "\\T1.3;SECCIÓN POR EL ALERO, POR UNA CERCHA")
E["395"].text = "Suelos sobre forjado\\Psanitario y sótano"
for h in ("3EB", "3EC", "3ED", "3EE", "3EF", "3F0"):          # el 3E8 pasa a una línea: se sube lo que viene detrás
    E[h].translate(0, 3.7, 0)
for h in ("396", "397", "398", "399", "39A", "39B"):
    p = E[h].dxf.insert; E[h].dxf.insert = (p.x, p.y - 2.95)
pie = E["3F5"]
assert "· v4 ·" in pie.text, pie.text
pie.text = pie.text.replace("· v4 ·", "· v6 ·")
VIEJO = "mediciones de licitación de 15/06/2026 (cap. 07), fichas de Thermochip TAH y Onduline BT-150 Plus, manual Onduline (2.4) y DB-HS 1"
assert VIEJO in pie.text, pie.text
for cand in ("licitación de 15/06/2026 (cap. 07), fichas Thermochip TAH y Onduline BT-150 Plus, ETE 08/0295 (Thermochip), manual Onduline (2.4) y DB-HS 1",
             "licitación de 15/06/2026 (cap. 07), fichas Thermochip TAH y Onduline BT-150 Plus, ETE 08/0295, manual Onduline (2.4) y DB-HS 1"):
    fuentes = pie.text.replace(VIEJO, cand).split("\\P")[-1]
    if len(lineas(fuentes, pie.dxf.char_height, pie.dxf.width)[0]) <= 2:
        pie.text = pie.text.replace(VIEJO, cand); break
else:
    raise AssertionError("el pie de fuentes no cabe en 2 líneas")
print("pie:", pie.text[-260:])
doc.saveas(SAL)
print("guardado", SAL)
