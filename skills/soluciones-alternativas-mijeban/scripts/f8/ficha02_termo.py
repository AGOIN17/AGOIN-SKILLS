"""Ficha 02 · Fachada: muro de carga de bloque cerámico de arcilla aligerada (Termocerec 24) con aislamiento por el interior.

Parte de la ficha 02 B v3 (f7/f02b_v3.dxf) y cambia la hoja portante de ladrillo tosco de un pie por el bloque Termocerec 24
de Cerámica Millas (declaración de prestaciones nº 052-A-2026/05/19: 295 × 189,6 × 236 mm, G3, fb 10 N/mm², λ 0,28 W/mK,
«con junta fina de mortero»).

- Axonometría: se rehace entera desde un modelo 3D de cajas (una por capa) con las caras ocultas quitadas con shapely.
  El bloque lleva los huecos de la foto del usuario (6 columnas de ranuras en espiga, 2 huecos de agarre, machihembrado
  con 5 machos y taladros redondos), traba a media pieza y junta fina.
- Sección vertical: se rehace la hoja portante (236 mm, huecos verticales cortados) y se desplaza 3 mm todo lo interior.
- Textos, leyenda, cifras y transmitancia: la U sale del cálculo de este script.

Uso: python ficha02_termo.py f7/f02b_v3.dxf f8/ficha02.dxf
"""
import sys, math
import ezdxf
from ezdxf.fonts import fonts
from shapely.geometry import Polygon, LineString, Point, box, MultiPolygon, MultiLineString
from shapely.ops import unary_union
from shapely import affinity

ENT, SAL = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(ENT); E = doc.entitydb; msp = doc.modelspace(); ps = doc.layouts.get('FICHA-A4')
tc = lambda c: (c[0] << 16) | (c[1] << 8) | c[2]
d0 = DX = 0.003                                       # el muro engorda 3 mm (236 frente a 233)

# =============================================================== pieza (declaración de prestaciones de Millas)
L_P, H_P, W_P = 0.295, 0.1896, 0.236                  # largo, alto y ancho declarados
LAMBDA_P, FB = 0.28, 10
# criterio de dibujo (no viene en la declaración): machihembrado de 8 mm y junta fina de 1 mm
T_MH = 0.008; MOD = L_P - T_MH                        # 0,287 entre llagas
JF = 0.001; MOD_V = H_P + JF
CAP = 0.012                                           # tabiquillos de las caras del muro
ZI, ZD = 0.007, 0.015                                 # zona del macho (izquierda) y de la hembra (derecha)
NCOL, ANC_COL = 6, 0.037
TAB = (MOD - ZI - ZD - NCOL * ANC_COL) / (NCOL - 1)  # tabiquillo entre columnas
NFIL, S_R, T_R, D_R = 10, 0.0135, 0.008, 0.005        # ranuras: alto, tabiquillo y desplome (espiga)
assert abs(CAP + (NFIL - 1) * (S_R + T_R) + S_R + D_R - (W_P - CAP)) < 1e-9
MACHOS = [CAP + (W_P - 2 * CAP) * (k + 0.5) / 5 for k in range(5)]
R_TAL = 0.00225


def pieza_uv():
    """Contorno de la tabla (u a lo largo del muro desde la llaga, v desde la cara exterior) y huecos."""
    cont = box(0, 0, MOD, W_P)
    for c in MACHOS:
        cont = cont.union(box(-T_MH, c - 0.010, 0, c + 0.010)).difference(box(MOD - T_MH, c - 0.010, MOD, c + 0.010))
    huecos = []
    for i in range(NCOL):
        u0 = ZI + i * (ANC_COL + TAB); u1 = u0 + ANC_COL
        sg = 1 if i % 2 == 0 else -1
        def ranura(j0, j1):
            a, b = CAP + j0 * (S_R + T_R), CAP + j1 * (S_R + T_R) + S_R
            if sg > 0:
                return Polygon([(u0, a), (u1, a + D_R), (u1, b + D_R), (u0, b)])
            return Polygon([(u0, a + D_R), (u1, a), (u1, b), (u0, b + D_R)])
        agarre = {1: (3, 4), 4: (6, 7)}.get(i)
        j = 0
        while j < NFIL:
            if agarre and j == agarre[0]:
                huecos.append(('agarre', ranura(j, agarre[1]))); j = agarre[1] + 1
            else:
                huecos.append(('ranura', ranura(j, j))); j += 1
    for c in MACHOS:
        huecos.append(('taladro', Point(-0.002, c).buffer(R_TAL, 12)))
    return cont, huecos


CONT_UV, HUECOS_UV = pieza_uv()


def intervalos(u):
    """Tramos de hueco (v0, v1) que corta un plano vertical a la distancia u de la llaga."""
    lin = LineString([(u, -1), (u, 2)]); res = []
    for _, h in HUECOS_UV:
        g = lin.intersection(h)
        for s in getattr(g, 'geoms', [g]):
            if s.length > 1e-6:
                ys = [p[1] for p in s.coords]; res.append((min(ys), max(ys)))
    return sorted(res)


# =============================================================== capas del muro (de fuera a dentro) y transmitancia
CAPAS = [  # n, nombre, espesor, λ (o None si va R), R
    (6, 'monocapa', 0.015, 1.30, None),
    (5, 'bloque', W_P, None, None),
    (4, 'enfoscado', 0.015, 1.30, None),
    (3, 'EPS', 0.100, 0.036, None),
    (2, 'gran formato', 0.067, None, 0.21),            # R con juntas (declaración de Millas, λ 0,29), como en la v3
    (1, 'yeso', 0.015, 0.57, None)]
ESPESOR = sum(c[2] for c in CAPAS)
Y0 = {}; y = 0.0
for n, _, e, _, _ in CAPAS:
    Y0[n] = y; y += e
Y1 = {n: Y0[n] + e for n, _, e, _, _ in CAPAS}
# fábrica de bloque: caminos en paralelo, pieza λ 0,28 y junta fina de 1 mm de mortero λ 1,30 (llagas machihembradas, sin mortero)
R_PIEZA = W_P / LAMBDA_P; R_JUNTA = W_P / 1.30; F_J = JF / MOD_V
R_FAB = 1 / ((1 - F_J) / R_PIEZA + F_J / R_JUNTA)
def transmitancia(l_eps):
    r = 0.04 + 0.13
    for n, nom, e, lam, rr in CAPAS:
        r += R_FAB if nom == 'bloque' else rr if rr else e / (l_eps if nom == 'EPS' else lam)
    return 1 / r
U_NUEVA, U_038, U_PROY = transmitancia(0.036), transmitancia(0.038), 0.27
DIF = round((U_NUEVA / U_PROY - 1) * 100)
fmt = lambda v, d=2: f"{v:.{d}f}".replace('.', ',')
PIEZAS_M2 = 1 / (MOD * MOD_V)
print(f"espesor {ESPESOR*1000:.0f} mm · R fábrica {R_FAB:.3f} · U {U_NUEVA:.4f} (λ 0,038: {U_038:.4f}) · {DIF} % · {PIEZAS_M2:.1f} piezas/m²")

# =============================================================== plantillas (antes de borrar)
def plantilla(h):
    return E[h].copy()
T_HONEY, T_SAND = plantilla('308'), plantilla('1E4')
T_NUM = {k: plantilla(h) for k, h in (('lider', '376'), ('punto', '377'), ('circulo', '378'), ('texto', '379'))}
T_RAYA_SEC = plantilla('F4'); T_LIN_HUECO = plantilla('F5'); T_JUNTA = plantilla('E5')
C_NUM0 = ((0.8639 + 0.9009) / 2, -1.122)              # centro del círculo «1» de la v3
P_NUM0 = (0.6688, -1.1815)                            # su punto

# =============================================================== AXONOMETRÍA
for e in list(msp):
    if e.dxf.layer in ('A-AXO-COLOR', 'A-AXO-LIN', 'A-AXO-DET') or (e.dxf.layer == 'A-NUMEROS' and e.dxf.handle in
                                                                    {f'{i:X}' for i in range(0x376, 0x38E)}):
        msp.delete_entity(e)

C = math.cos(math.radians(30)); OX, OY = 0.0, -1.7
TAN = math.tan(math.radians(20))
def P(X, Y, Z):
    return (OX + C * (X + Y), OY - 0.5 * X + 0.5 * Y + Z)
plano_Z = lambda g, Z: affinity.affine_transform(g, [C, C, -0.5, 0.5, OX, OY + Z])            # g en (X, Y)
plano_X = lambda g, X: affinity.affine_transform(g, [C, 0, 0.5, 1, OX + C * X, OY - 0.5 * X])  # g en (Y, Z)
plano_Y = lambda g, Y: affinity.affine_transform(g, [C, 0, -0.5, 1, OX + C * Y, OY + 0.5 * Y]) # g en (X, Z)
HONDO_Z, HONDO_X = (0.0, -1.0), (-C, 0.5)             # desplazamiento en pantalla por metro de profundidad

ZB = 2 * H_P + JF                                     # dos hiladas de bloque
X1 = {6: 0.15, 5: 0.30, 4: 0.345, 3: 0.40, 2: 0.45, 1: 0.48}
Z1 = {6: 0.15, 5: ZB, 4: 0.42, 3: 0.46, 2: 0.48, 1: 0.52}
J1 = 0.225; J0 = J1 - MOD / 2                         # llagas de la hilada de arriba y de la de abajo (traba a media pieza)
HILADAS = [(0.0, H_P, J0), (H_P + JF, ZB, J1)]


def caras(n):
    x1, y0, y1, z1 = X1[n], Y0[n], Y1[n], Z1[n]
    return {'frente': Polygon([P(0, y0, 0), P(x1, y0, 0), P(x1, y0, z1), P(0, y0, z1)]),
            'arriba': Polygon([P(0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(0, y1, z1)]),
            'testa': Polygon([P(x1, y0, 0), P(x1, y1, 0), P(x1, y1, z1), P(x1, y0, z1)])}
SILUETA = {n: unary_union(list(caras(n).values())) for n in X1}
def tapa(n):                                          # lo que queda delante de la capa n (capas más exteriores)
    g = [SILUETA[m] for m in X1 if Y0[m] < Y0[n]]
    return unary_union(g) if g else Polygon()
def partes(g):
    return [p for p in getattr(g, 'geoms', [g]) if p.geom_type == 'Polygon' and p.area > 2e-8]
def lineas_de(g):
    return [s for s in getattr(g, 'geoms', [g]) if s.geom_type == 'LineString' and s.length > 2e-4]


def mancha(g, rgb, plantilla_patron=None):
    for p in partes(g):
        h = msp.add_hatch(dxfattribs={'layer': 'A-AXO-COLOR'}); h.set_solid_fill(rgb=rgb)
        h.paths.add_polyline_path(list(p.exterior.coords)[:-1], is_closed=True, flags=1)
        for r in p.interiors:
            h.paths.add_polyline_path(list(r.coords)[:-1], is_closed=True, flags=0)
        if plantilla_patron is not None:
            hp = plantilla_patron.copy(); msp.add_entity(hp); hp.paths.clear()
            hp.paths.add_polyline_path(list(p.exterior.coords)[:-1], is_closed=True, flags=1)
            for r in p.interiors:
                hp.paths.add_polyline_path(list(r.coords)[:-1], is_closed=True, flags=0)
def contorno(g, capa, rgb=None):
    a = {'layer': capa}
    if rgb: a['true_color'] = tc(rgb)
    for p in partes(g):
        msp.add_lwpolyline(list(p.exterior.coords), dxfattribs=a)
        for r in p.interiors:
            msp.add_lwpolyline(list(r.coords), dxfattribs=a)
def raya(g, capa='A-AXO-DET', rgb=None):
    a = {'layer': capa}
    if rgb: a['true_color'] = tc(rgb)
    for s in lineas_de(g):
        msp.add_lwpolyline(list(s.coords), dxfattribs=a)
def bandas(vis, lleno, vec, cortes):
    """Pared interior de un hueco en tonos por profundidad: [junto al borde, …, al fondo]."""
    S = lambda d: affinity.translate(lleno, vec[0] * d, vec[1] * d)
    out, prev = [], lleno
    for d in cortes:
        s = S(d); out.append(vis.intersection(prev).difference(s)); prev = s
    out.append(vis.intersection(prev))
    return out


COLORES = {6: ((200, 200, 200), (184, 184, 184), (170, 170, 170)), 4: ((208, 208, 208), (192, 192, 192), (180, 180, 180)),
           3: ((255, 255, 255),) * 3, 1: ((246, 246, 246), (236, 236, 236), (226, 226, 226))}
VISIBLE = {}
for n in (1, 2, 3, 4, 5, 6):                          # de atrás adelante
    VISIBLE[n] = {k: f.difference(tapa(n)) for k, f in caras(n).items()}

# ---------------------------------------------------- 1 yeso, 3 EPS, 4 enfoscado, 6 monocapa: caras lisas
def capa_lisa(n):
    for k, col in zip(('frente', 'arriba', 'testa'), COLORES[n]):
        patron = T_HONEY if n == 3 else (T_SAND if n == 6 and k == 'frente' else None)
        mancha(VISIBLE[n][k], col, patron)
        contorno(VISIBLE[n][k], 'A-AXO-LIN')

# ---------------------------------------------------- 2 gran formato (perfil tomado de la sección, +3 mm)
def poli_sec(h):
    return Polygon([(p[0] + DX, p[1]) for p in E[h].get_points()])
GF_PIEZAS = [poli_sec('143'), poli_sec('151')]
GF_HUECOS = [poli_sec(f'{i:X}') for i in list(range(0x144, 0x150)) + list(range(0x152, 0x15A))]
def capa_gf():
    n = 2; x1, y0, y1, z1 = X1[n], Y0[n], Y1[n], Z1[n]
    corte = box(y0, 0, y1, z1)
    # frente: tono 212 con la junta machihembrada (banda 236)
    vis = VISIBLE[n]['frente']; mancha(vis, (212, 212, 212))
    zj0 = max(p[1] for p in GF_PIEZAS[0].exterior.coords if abs(p[0] - y0) < 1e-6)
    zj1 = min(p[1] for p in GF_PIEZAS[1].exterior.coords if abs(p[0] - y0) < 1e-6)
    junta = plano_Y(box(0, zj0, x1, zj1), y0).intersection(vis); mancha(junta, (236, 236, 236))
    raya(plano_Y(LineString([(0, zj0), (x1, zj0)]), y0).intersection(vis))
    raya(plano_Y(LineString([(0, zj1), (x1, zj1)]), y0).intersection(vis))
    contorno(vis, 'A-AXO-LIN')
    # arriba: corte horizontal por la fila de huecos de z1 → canales a lo largo del muro
    vis = VISIBLE[n]['arriba']; canales = []
    for h in GF_HUECOS:
        zs = [p[1] for p in h.exterior.coords]; ys = [p[0] for p in h.exterior.coords]
        if min(zs) < z1 < max(zs):
            canales.append((box(0, min(ys), x1, max(ys)), z1 - min(zs)))
    mancha(vis.difference(unary_union([plano_Z(c, z1) for c, _ in canales])), (214, 214, 214))
    for c, hondo in canales:
        lleno = plano_Z(c, z1)
        for g, col in zip(bandas(vis.intersection(lleno), lleno, HONDO_Z, (0.004, 0.010)), ((204,) * 3, (190,) * 3, (176,) * 3)):
            mancha(g, col)
        contorno(vis.intersection(lleno), 'A-AXO-DET')
    contorno(vis, 'A-AXO-LIN')
    # testa: corte vertical, con los huecos horizontales vistos de frente
    vis = VISIBLE[n]['testa']
    piezas = [plano_X(p.intersection(corte), x1) for p in GF_PIEZAS]
    huecos = [plano_X(h.intersection(corte), x1) for h in GF_HUECOS if h.intersection(corte).area > 1e-8]
    mancha(vis.intersection(unary_union(piezas)).difference(unary_union(huecos)), (196, 196, 196))
    mancha(vis.difference(unary_union(piezas)), (236, 236, 236))                     # junta
    for p in piezas:
        contorno(vis.intersection(p), 'A-AXO-DET')
    for hh in huecos:
        for g, col in zip(bandas(vis.intersection(hh), hh, HONDO_X, (0.004, 0.010)), ((206,) * 3, (190,) * 3, (176,) * 3)):
            mancha(g, col)
        contorno(vis.intersection(hh), 'A-AXO-DET')
    contorno(vis, 'A-AXO-LIN')

# ---------------------------------------------------- 5 bloque Termocerec 24
def bloques_hilada(llaga, x_fin):
    s = llaga
    while s > -MOD:
        s -= MOD
    res = []
    while s < x_fin:
        res.append(s); s += MOD
    return res
def capa_bloque():
    n = 5; x1, y0, y1, z1 = X1[n], Y0[n], Y1[n], Z1[n]
    # --- tabla de arriba (hilada superior), con los huecos en tres tonos
    vis = VISIBLE[n]['arriba']; rect = box(0, y0, x1, y1)
    huecos_xy = []
    for s in bloques_hilada(HILADAS[1][2], x1):
        for tipo, h in HUECOS_UV:
            g = affinity.translate(h, s, y0)
            if g.intersects(rect):
                huecos_xy.append((g, g.intersection(rect)))
    abiertos = unary_union([plano_Z(gc, z1) for _, gc in huecos_xy])
    mancha(vis.difference(abiertos), (208, 208, 208))
    for g, gc in huecos_xy:
        lleno, ab = plano_Z(g, z1), plano_Z(gc, z1).intersection(vis)
        for b, col in zip(bandas(ab, lleno, HONDO_Z, (0.0025, 0.0055)), ((198,) * 3, (184,) * 3, (170,) * 3)):
            mancha(b, col)
        contorno(ab, 'A-AXO-DET')
    for s in bloques_hilada(HILADAS[1][2], x1):                  # llaga machihembrada
        pts = [(s, 0)]
        for c in MACHOS:
            pts += [(s, c - 0.010), (s - T_MH, c - 0.010), (s - T_MH, c + 0.010), (s, c + 0.010)]
        pts.append((s, W_P))
        raya(plano_Z(affinity.translate(LineString(pts), 0, y0), z1).intersection(vis.buffer(1e-7)))
    contorno(vis, 'A-AXO-LIN')
    # --- frente (cara exterior): piezas, llagas, junta fina y estrías verticales
    vis = VISIBLE[n]['frente']; mancha(vis, (192, 192, 192))
    for za, zb, llaga in HILADAS:
        for s in bloques_hilada(llaga, x1):
            if 0 < s < x1:
                raya(plano_Y(LineString([(s, za), (s, zb)]), y0).intersection(vis))
            for i in range(17):
                xe = s + (i + 0.5) * MOD / 17
                if 0.004 < xe < x1 - 0.004:
                    raya(plano_Y(LineString([(xe, za + 0.004), (xe, zb - 0.004)]), y0).intersection(vis), rgb=(150, 150, 150))
    raya(plano_Y(LineString([(0, H_P + JF / 2), (x1, H_P + JF / 2)]), y0).intersection(vis))
    contorno(vis, 'A-AXO-LIN')
    # --- testa (corte vertical en x1): huecos verticales abiertos en franjas de tres tonos
    vis = VISIBLE[n]['testa']; mancha(vis, (178, 178, 178))
    for za, zb, llaga in HILADAS:
        s = max(b for b in bloques_hilada(llaga, x1) if b <= x1); u = x1 - s
        for v0, v1 in intervalos(u):
            a, b = y0 + v0, y0 + v1; w = b - a
            for (f0, f1), col in zip(((0, 0.3), (0.3, 0.7), (0.7, 1.0)), ((162,) * 3, (175,) * 3, (190,) * 3)):
                mancha(plano_X(box(a + f0 * w, za, a + f1 * w, zb), x1).intersection(vis), col)
            contorno(plano_X(box(a, za, b, zb), x1).intersection(vis), 'A-AXO-DET')
    mancha(plano_X(box(y0, H_P, y1, H_P + JF), x1).intersection(vis), (238, 238, 238))
    raya(plano_X(LineString([(y0, H_P + JF / 2), (y1, H_P + JF / 2)]), x1).intersection(vis))
    contorno(vis, 'A-AXO-LIN')
    return [plano_X(box(y0 + v0, HILADAS[1][0], y0 + v1, HILADAS[1][1]), x1)
            for v0, v1 in intervalos(x1 - max(b for b in bloques_hilada(HILADAS[1][2], x1) if b <= x1))]


capa_lisa(1); capa_gf(); capa_lisa(3); capa_lisa(4); capa_bloque(); capa_lisa(6)
TODO = unary_union(list(SILUETA.values()))
minx, miny, maxx, maxy = TODO.bounds
print(f"axonometría: x {minx:.4f}…{maxx:.4f}  y {miny:.4f}…{maxy:.4f} (alto {maxy - miny:.4f})")

# ---------------------------------------------------- ventana de la axonometría (1:10, alargada hacia abajo)
vp = E['3EF']
VP_TOP, VP_BOT = vp.dxf.center.y + vp.dxf.height / 2, 145.0
vc_x = vp.dxf.view_center_point.x                                   # x del modelo igual que en la v3
mapa_y_old = lambda ym: vp.dxf.center.y + (ym - vp.dxf.view_center_point.y) * 100
alto_vp = VP_TOP - VP_BOT
papel_sup = 235.0                                                    # punto más alto del dibujo en el papel
vc_y = maxy + ((VP_BOT + alto_vp / 2) - papel_sup) / 100
vp.dxf.center = (vp.dxf.center.x, VP_BOT + alto_vp / 2, 0); vp.dxf.height = alto_vp
vp.dxf.view_center_point = (vc_x, vc_y, 0); vp.dxf.view_height = alto_vp / 100
papel = lambda xm, ym: (vp.dxf.center.x + (xm - vc_x) * 100, vp.dxf.center.y + (ym - vc_y) * 100)
print(f"ventana axo: papel y {VP_BOT:.1f}…{VP_TOP:.1f}; dibujo de {papel(0, miny)[1]:.1f} a {papel(0, maxy)[1]:.1f}")
assert papel(0, miny)[1] > VP_BOT + 0.5

# ---------------------------------------------------- números de la axonometría (directrices paralelas a 20°)
R_CIRC = 0.0185; XC = vc_x + (vp.dxf.center.x + vp.dxf.width / 2 - 0.45 - vp.dxf.center.x) / 100 - R_CIRC
XE = XC - R_CIRC - 0.0315
assert XE > maxx + 0.02, (XE, maxx)
OBJETIVO = {1: ('frente',), 2: ('arriba',), 3: ('arriba',), 4: ('frente',), 5: ('testa', 'arriba'), 6: ('frente',)}
def punto_en(n, yc):
    lin = LineString([(XE, yc), (XE - 1.2, yc - 1.2 * TAN)])
    for k in OBJETIVO[n]:
        zona = VISIBLE[n][k].buffer(-0.006)
        segs = [s for s in lineas_de(lin.intersection(zona)) if s.length > 0.012]
        if segs:
            s = max(segs, key=lambda s: max(p[0] for p in s.coords))   # el tramo más a la derecha
            return s.interpolate(0.5, normalized=True)
    return None
Y_NUM = [OY + 0.66 - 0.05 * i for i in range(6)]
for i, yc in enumerate(Y_NUM, start=1):
    p = punto_en(i, yc)
    assert p is not None, f"sin punto para el número {i} a y={yc:.3f}"
    for k in ('circulo', 'texto'):
        e = T_NUM[k].copy(); msp.add_entity(e); e.translate(XC - C_NUM0[0], yc - C_NUM0[1], 0)
        if k == 'texto':
            e.dxf.text = str(i)
    e = T_NUM['punto'].copy(); msp.add_entity(e)
    e.translate(p.x - (P_NUM0[0]), p.y - (P_NUM0[1]), 0)
    e = T_NUM['lider'].copy(); msp.add_entity(e)
    e.set_points([(p.x, p.y), (XE, yc), (XC - R_CIRC, yc)])
    print(f"número {i}: punto ({p.x:.4f},{p.y:.4f}) → papel {tuple(round(v, 1) for v in papel(p.x, p.y))}")

# =============================================================== SECCIÓN VERTICAL
borrar = [f'{i:X}' for i in range(0xE5, 0x142)]
for h in borrar:
    if h in E and E[h].dxf.owner == msp.layout_key:
        msp.delete_entity(E[h])
LIM = 0.2479
mover = ['9C', '9D', '9E', '9F', 'A0', 'A2', 'A3'] + [f'{i:X}' for i in range(0x142, 0x15A)]
mover += [e.dxf.handle for e in msp.query('LWPOLYLINE[layer=="A-DETL-AISL"]')]
for h in mover:
    E[h].translate(DX, 0, 0)
for h in ('15A', '15B'):                                              # líneas de corte, hasta el nuevo borde
    pts = list(E[h].get_points()); pts[-1] = (pts[-1][0] + DX,) + tuple(pts[-1][1:]); E[h].set_points(pts)
t = E['175']; t.dxf.insert = (t.dxf.insert.x + DX, t.dxf.insert.y, 0); t.dxf.align_point = (t.dxf.align_point.x + DX, t.dxf.align_point.y, 0)
for h in ('165', '169', '16D', '171'):                                # puntos 4, 3, 2 y 1
    E[h].translate(DX, 0, 0)
for h in ('164', '168', '16C', '170'):
    pts = list(E[h].get_points()); pts[0] = (pts[0][0] + DX,) + tuple(pts[0][1:]); E[h].set_points(pts)

YA, YB = Y0[5], Y1[5]
SEC_JUNTAS = [0.105 + k * MOD_V for k in range(3)]
cortes_z = [0.0] + SEC_JUNTAS + [0.52]
U_SEC = (0.122, 0.122 + MOD / 2)                                      # hiladas alternas, a media pieza
assert all(len(intervalos(u)) == NFIL for u in U_SEC), [intervalos(u) for u in U_SEC]
tabiques = None
for k in range(len(cortes_z) - 1):
    za, zb = cortes_z[k], cortes_z[k + 1]; iv = intervalos(U_SEC[k % 2])
    h = T_RAYA_SEC.copy(); msp.add_entity(h); h.paths.clear()
    h.paths.add_polyline_path([(YA, za), (YB, za), (YB, zb), (YA, zb)], is_closed=True, flags=1)
    for v0, v1 in iv:
        h.paths.add_polyline_path([(YA + v0, za), (YA + v1, za), (YA + v1, zb), (YA + v0, zb)], is_closed=True, flags=0)
        for x in (YA + v0, YA + v1):
            ln = T_LIN_HUECO.copy(); msp.add_entity(ln); ln.dxf.start = (x, za, 0); ln.dxf.end = (x, zb, 0)
    if za <= 0.40 < zb:
        tabiques = [(YA + iv[j][1], YA + iv[j + 1][0]) for j in range(len(iv) - 1)]
for z in SEC_JUNTAS:
    ln = T_JUNTA.copy(); msp.add_entity(ln); ln.dxf.start = (YA, z, 0); ln.dxf.end = (YB, z, 0)
# número 5 de la sección sobre un tabiquillo cerca de x = 0,065
ta = min(tabiques, key=lambda t: abs((t[0] + t[1]) / 2 - 0.065)); xp = (ta[0] + ta[1]) / 2
E['161'].translate(xp - 0.065, 0, 0)
pts = list(E['160'].get_points()); pts[0] = (xp,) + tuple(pts[0][1:]); E['160'].set_points(pts)

# cotas: se mueven 3 mm las piezas a la derecha de la cara interior del bloque y se cambian los textos
for d in msp.query('DIMENSION'):
    dentro = min(d.dxf.defpoint2.x, d.dxf.defpoint3.x) > LIM
    for k in ('defpoint', 'defpoint2', 'defpoint3', 'text_midpoint'):
        v = d.dxf.get(k)
        if v is not None and (dentro or v.x > LIM):
            d.dxf.set(k, (v.x + DX, v.y, v.z))
    blk = doc.blocks.get(d.dxf.geometry)
    for e in blk:
        t = e.dxftype()
        if t == 'LINE':
            for k in ('start', 'end'):
                v = e.dxf.get(k)
                if dentro or v.x > LIM:
                    e.dxf.set(k, (v.x + DX, v.y, v.z))
        elif t in ('INSERT', 'MTEXT'):
            v = e.dxf.insert
            if dentro or v.x > LIM:
                e.dxf.insert = (v.x + DX, v.y, v.z)
        elif t == 'POINT':
            v = e.dxf.location
            if dentro or v.x > LIM:
                e.dxf.location = (v.x + DX, v.y, v.z)
    med = abs(d.dxf.defpoint3.x - d.dxf.defpoint2.x)
    d.dxf.actual_measurement = med
    for e in blk.query('MTEXT'):
        txt = f"{med * 1000:.0f}"
        if e.text != txt:
            print(f"cota {e.text} → {txt}")
            if e.text == '233':
                e.dxf.insert = ((d.dxf.defpoint2.x + d.dxf.defpoint3.x) / 2, e.dxf.insert.y, 0)
            e.text = txt
cotas = sorted(round(abs(d.dxf.defpoint3.x - d.dxf.defpoint2.x) * 1000) for d in msp.query('DIMENSION'))
assert cotas == sorted([15, 236, 15, 100, 67, 15, round(ESPESOR * 1000)]), cotas

# =============================================================== TEXTOS DE LA FICHA
def cambia(h, viejo, nuevo):
    e = E[h]
    assert e.text.count(viejo) == 1, (h, viejo, e.text)
    e.text = e.text.replace(viejo, nuevo)
def pon(h, nuevo):
    E[h].text = nuevo
U_TXT, U038_TXT = fmt(U_NUEVA), fmt(U_038)
DIF_TXT = f"−{abs(DIF)} %" if DIF < 0 else (f"+{DIF} %" if DIF > 0 else "0 %")
pon('3B8', 'Fachada')
pon('3CE', f'{ESPESOR * 1000:.0f} mm')
pon('3D6', '24 cm'); pon('3D7', f'Bloque Termocerec 24, fb {FB} N/mm²')
cambia('3EB', 'FICHA 02 · FACHADA · ALTERNATIVA B', 'FICHA 02 · FACHADA')
pon('3EE', 'Una hoja portante de bloque de arcilla aligerada de 24 cm, revestida por fuera con monocapa. '
           'El aislamiento pasa al interior: EPS blanco de 100 mm y un trasdosado de ladrillo de gran formato de 7 cm.')
pon('3FE', 'Bloque Termocerec 24, machihembrado, junta fina')
pon('3FF', f'{W_P * 1000:.0f} mm')
pon('40B', 'Propuesta'); pon('40C', U_TXT); pon('40E', DIF_TXT)
pon('410', f'Proyecto: certificado energético (memoria, p. 589). Propuesta: cálculo propio según el CTE con EPS blanco de '
           f'λ 0,036 W/mK y las piezas de las declaraciones de Millas (bloque λ 0,28 y gran formato λ 0,29); con EPS de λ 0,038, U ≈ {U038_TXT}.')
pon('413', '\\T1.3;LA PROPUESTA')
pon('414', 'Bloque de 24 cm portante, monocapa por fuera y enfoscado por dentro; EPS de 100\\~mm, '
           'gran formato de 7 cm y yeso.')
pon('417', 'Monocapa directo sobre el bloque, sin SATE.')
pon('419', 'Bloque de 24 cm: condición C2 del DB-HS\\~1.')       # «\~»: espacio que no parte la línea
cambia('3E9', 'que exige un pie de ladrillo;', 'que exige un pie de ladrillo o 24 cm de bloque;')
cambia('423', 'Ficha 02 B · v3', 'Ficha 02 · v1')
cambia('423', 'plano DET-01, ', 'plano DET-01, DB-HS 1 (2.3.2), ')
cambia('423', 'del «Cerámico tosco de 10»', 'del «Termocerec 24»')
# pie: 3 mm más arriba (en la v3 la última línea quedaba a 0,5 mm del borde del papel)
for h in ('422', '423'):
    E[h].translate(0, 3.0, 0)
# cuarta viñeta de «Qué se gana», copiando la tercera
v4 = E['41B'].copy(); ps.add_entity(v4); v4.text = f'Pieza grande machihembrada: unas {PIEZAS_M2:.0f} por m² y llagas sin mortero.'
c4 = E['41A'].copy(); ps.add_entity(c4)
# barra de la propuesta, a la escala de la del proyecto
b = E['40D']; xs = [v[0] for v in b.paths[0].vertices]; ys = [v[1] for v in b.paths[0].vertices]
ESC_BARRA = (max(xs) - min(xs)) / U_PROY
b.paths.clear(); xb = min(xs) + ESC_BARRA * float(U_TXT.replace(',', '.'))
b.paths.add_polyline_path([(min(xs), min(ys)), (xb, min(ys)), (xb, max(ys)), (min(xs), max(ys))], is_closed=True, flags=1)

# ---------------------------------------------------- reparto vertical: leyenda y «Qué se gana»
FUENTE = {}
def ancho(txt, h):
    if h not in FUENTE:
        FUENTE[h] = fonts.make_font('GOTHIC.TTF', h)
    return FUENTE[h].text_width(txt)
def n_lineas(e):
    import re
    txt = re.sub(r'\\[A-Za-z][^;]*;', '', e.text); h = e.dxf.char_height; w = e.dxf.width
    n = 0
    for par in txt.split('\\P'):
        palabras = par.split(' '); lin = ''; n += 1
        for p in palabras:
            prueba = (lin + ' ' + p).strip()
            if w and ancho(prueba, h) > w and lin:
                n += 1; lin = p
            else:
                lin = prueba
    return n
PASO = lambda e: 1.667 * e.dxf.char_height * e.dxf.line_spacing_factor
y = E['3F1'].dxf.insert.y
for num, des, mm in (('3F1', '3F2', '3F3'), ('3F4', '3F5', '3F6'), ('3F7', '3F8', '3F9'), ('3FA', '3FB', '3FC'),
                     ('3FD', '3FE', '3FF'), ('400', '401', '402')):
    for h in (num, des):
        E[h].dxf.insert = (E[h].dxf.insert.x, y, 0)
    y_mm = y - n_lineas(E[des]) * PASO(E[des])
    E[mm].dxf.insert = (E[mm].dxf.insert.x, y_mm, 0)
    y = y_mm - 5.35
    print(f"leyenda {E[num].text}: {n_lineas(E[des])} líneas")
assert y > 145, y
# viñetas de «Qué se gana»: se reparten según las líneas de cada una (en la v3, 419 y 41B tenían una línea)
paso_v = PASO(E['41B'])
hueco_v = E['419'].dxf.insert.y - E['41B'].dxf.insert.y - paso_v
y = E['417'].dxf.insert.y
for t, c in ((E['417'], E['416']), (E['419'], E['418']), (E['41B'], E['41A']), (v4, c4)):
    dy = y - t.dxf.insert.y
    t.dxf.insert = (t.dxf.insert.x, y, 0); c.translate(0, dy, 0)
    print(f"viñeta {t.text[:30]!r}: {n_lineas(t)} líneas, y {y:.2f}")
    y -= n_lineas(t) * paso_v + hueco_v
assert y > 20, y
for h in ('3EE', '414', '410', '423', '3E9', '3D7'):
    print(f"{h}: {n_lineas(E[h])} líneas")
assert n_lineas(E['3EE']) <= 3 and n_lineas(E['414']) <= 3 and n_lineas(E['410']) <= 2 and n_lineas(E['3D7']) == 1

# ---------------------------------------------------- comprobaciones de texto
import re
cajas = []
for e in ps.query('MTEXT'):
    h = e.dxf.char_height; n = n_lineas(e)
    limpio = re.sub(r'\\[A-Za-z][^;]*;|[{}]|\\~', ' ', e.text)
    w = e.dxf.width or max(ancho(p, h) * (1.3 if '\\T1.' in e.text else 1) for p in limpio.split('\\P'))
    x0, ytop = e.dxf.insert.x, e.dxf.insert.y
    assert e.dxf.attachment_point == 1, e.dxf.handle
    cajas.append((e.dxf.handle, box(x0, ytop - (n - 1) * PASO(e) - h, x0 + w, ytop)))
pisados = [(a, b, round(ga.intersection(gb).area, 2)) for i, (a, ga) in enumerate(cajas) for b, gb in cajas[i + 1:]
           if ga.intersection(gb).area > 0.3]
print('textos que se pisan:', pisados)
assert not pisados, pisados
for e in ps.query('MTEXT'):
    t = e.text
    if e.dxf.handle in ('3B5', '3E5'):            # «SOLUCIONES ALTERNATIVAS»; la nota 1 habla del tosco del proyecto
        continue
    for k in ('tosco', 'ALTERNATIVA', 'Alternativa', 'alternativa', '233', '445', '1 pie', '02 B', 'v3', '0,30 y'):
        assert k not in t, (e.dxf.handle, k, t)
doc.saveas(SAL)
print('guardado', SAL)
