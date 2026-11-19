"""Ficha 01 · Suelos sobre forjado sanitario y sótano.

Parte de la maqueta de la ficha 03 v4 (f4/v4.dxf): vacía el modelo, dibuja la sección (1:5)
con las tramas de la referencia A33c (REFERENCIAS\\A33a-...-A31e.dwg) y la axonometría
escalonada, y rehace los textos del espacio papel.

Uso: python ficha01.py f4/v4.dxf f1/ficha01.dxf
"""
import sys, math
import ezdxf
from ezdxf import colors
from ezdxf.fonts import fonts
from shapely.geometry import Polygon, box, Point, LineString, MultiPolygon, MultiLineString
from shapely.ops import unary_union

SRC, OUT = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(SRC)
msp = doc.modelspace()
ps = doc.layouts.get('FICHA-A4')
for e in list(msp):
    msp.delete_entity(e)

VERDE = (7, 87, 72)
VERDE_INT = colors.rgb2int(VERDE)
GRIS_TXT = 9079434       # gris de los textos secundarios
GRIS_LIN = (70, 70, 70)

# ------------------------------------------------------------------ capas (mm)
# barrera 2 · XPS 60 · panel de tetones 28 en total (base 10 + tetones 18, reparto supuesto)
# · plastón 50 sobre los tetones · cemento cola 5 · gres 15 = 160 mm (usuario, 2026-11-09)
Z_BAR, Z_XPS, Z_PAN, Z_TET, Z_MOR, Z_COLA, Z_GRES = 0.0, 0.002, 0.062, 0.072, 0.140, 0.145, 0.160
Z_TOP_TET = 0.090          # tetones de 18 mm sobre la base de 10: panel de 28 mm
PASO, RW, RC = 0.05, 0.0125, 0.008   # paso de tetones, media anchura del tetón, radio del fondo
ZF = -0.25                  # forjado sanitario 20+5 (usuario; los planos de estructura dicen 25+5)
COTA_PROY = -0.10           # cara superior del forjado en DET-01: 10 cm bajo el suelo acabado
R_TUBO, R_TUBO_INT = 0.008, 0.0061   # PEX 16 x 1,9
FASE_TUBO = 0.025                     # tubos en x = 0,025 + 0,10·j (cada 10 cm)


def arco(cx, cy, r, a0, a1, n=8):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def perfil_tetones(x0, x1, zbase):
    """Polígono del panel de tetones (base + tetones) entre x0 y x1, en el plano (x, z)."""
    pts = []
    m0, m1 = math.floor(x0 / PASO) - 1, math.ceil(x1 / PASO) + 1
    for m in range(m0, m1):
        xm = m * PASO
        pts += [(xm, Z_TOP_TET), (xm + RW, Z_TOP_TET), (xm + RW, Z_TET + RC)]
        pts += arco(xm + RW + RC, Z_TET + RC, RC, 180, 270)[1:]
        pts += arco(xm + PASO - RW - RC, Z_TET + RC, RC, 270, 360)
        pts += [(xm + PASO - RW, Z_TOP_TET)]
    pts += [(m1 * PASO, Z_TOP_TET), (m1 * PASO, zbase), (m0 * PASO, zbase)]
    return Polygon(pts).intersection(box(x0, zbase, x1, Z_TOP_TET + 0.01))


def circulo(cx, cy, r, n=36):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def anillos(polys):
    """Devuelve los anillos (exterior e interiores) de un polígono o multipolígono shapely."""
    out = []
    if polys.is_empty:
        return out
    geoms = polys.geoms if hasattr(polys, 'geoms') else [polys]
    for g in geoms:
        if g.geom_type != 'Polygon' or g.area < 1e-12:
            continue
        out.append((list(g.exterior.coords), [list(i.coords) for i in g.interiors]))
    return out


def trama(space, geom, layer, patron=None, escala=1.0, angulo=0.0, rgb=None, solido=False, lw=None):
    for ext, ints in anillos(geom):
        h = space.add_hatch(dxfattribs={'layer': layer})
        if solido:
            h.set_solid_fill(color=7, rgb=rgb)
        else:
            h.set_pattern_fill(patron, scale=escala, angle=angulo, color=7)
            if rgb:
                h.dxf.true_color = colors.rgb2int(rgb)
        if lw is not None:
            h.dxf.lineweight = lw
        h.paths.add_polyline_path([p[:2] for p in ext], is_closed=True, flags=1)
        for i in ints:
            h.paths.add_polyline_path([p[:2] for p in i], is_closed=True, flags=0)


def linea(space, pts, layer, rgb=None, lw=None, cerrada=False, ltype=None, ltscale=None):
    e = space.add_lwpolyline([p[:2] for p in pts], close=cerrada, dxfattribs={'layer': layer})
    if rgb:
        e.dxf.true_color = colors.rgb2int(rgb)
    if lw is not None:
        e.dxf.lineweight = lw
    if ltype:
        e.dxf.linetype = ltype
    if ltscale:
        e.dxf.ltscale = ltscale
    return e


def contorno(space, geom, layer, rgb=None, lw=None):
    for ext, ints in anillos(geom):
        linea(space, ext, layer, rgb, lw, cerrada=True)
        for i in ints:
            linea(space, i, layer, rgb, lw, cerrada=True)


def burbuja(space, num, centro, objetivo, k, codo=None):
    """Círculo numerado como en las fichas 02 y 03. k = escala / 10 (1:10 -> 1)."""
    r, rp, ht = 0.0185 * k, 0.0045 * k, 0.02 * k
    cx, cy = centro
    lado = -1 if objetivo[0] < cx else 1
    inicio = (cx + lado * r, cy)
    pts = [objetivo] + ([codo] if codo else []) + [inicio]
    linea(space, pts, 'A-NUMEROS', GRIS_LIN, 13)
    trama(space, Polygon(circulo(*objetivo, rp, 16)), 'A-NUMEROS', rgb=VERDE, solido=True)
    trama(space, Polygon(circulo(cx, cy, r, 36)), 'A-NUMEROS', rgb=VERDE, solido=True)
    t = space.add_text(str(num), height=ht, dxfattribs={'layer': 'A-NUMEROS', 'style': '1-10 NEGRITA'})
    t.dxf.true_color = colors.rgb2int((255, 255, 255))
    t.set_placement((cx, cy), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)


def texto(space, s, pos, h, rgb=(70, 70, 70), estilo='1-10 (0.20)', align=None, rot=0):
    t = space.add_text(s, height=h, rotation=rot, dxfattribs={'layer': 'A_06_TEXTOS', 'style': estilo})
    t.dxf.true_color = colors.rgb2int(rgb)
    t.set_placement(pos, align=align or ezdxf.enums.TextEntityAlignment.LEFT)
    return t


# ================================================================== SECCIÓN
W = 0.25                         # ancho dibujado: nervio en el centro y bovedilla a cada lado
VP_SEC = (118.5, 25.0, 198.4, 98.0)
H_SUB = 1.6                      # rótulos bajo las cotas de nivel, en mm de papel


def ancho_txt(s, h, negrita=False):
    return fonts.make_font('GOTHICB.TTF' if negrita else 'GOTHIC.TTF', h).text_width(s)


def medidas_sec(esc):
    """Ancho y alto en papel (mm) de la sección con sus anotaciones, a la escala 1:esc."""
    fs, k = esc / 5, esc / 10
    izq = -0.036 * fs - 0.0185 * k - 0.002 * fs
    xn = W + 0.026 * fs + 0.046 * fs
    der = max(xn + 0.034 * fs,
              xn + 0.007 * fs + ancho_txt('±0,00', 2.0) * esc / 1000,
              xn - 0.007 * fs + ancho_txt('cota de proyecto', H_SUB) * esc / 1000) + 0.002 * fs
    return (der - izq) * 1000 / esc, (Z_GRES - ZF + 0.032 * fs) * 1000 / esc


ESC_SEC = 5.0
while True:
    a_, h_ = medidas_sec(ESC_SEC)
    if a_ <= VP_SEC[2] - VP_SEC[0] - 0.6 and h_ <= VP_SEC[3] - VP_SEC[1] - 0.6:
        break
    ESC_SEC = round(ESC_SEC + 0.05, 2)
K_SEC = ESC_SEC / 10             # tamaños de las fichas (pensados a 1:10) a esta escala
FS = ESC_SEC / 5                 # separaciones de las anotaciones (pensadas a 1:5)
Y_ROT = ZF                       # el forjado se dibuja entero
sec = msp
NERV = (0.06, 0.18)              # (solo para la axonometría)


INTEREJE, MEDIO_NERV = 0.70, 0.06          # intereje de 70 (planos de estructura) y nervio de 12 cm
T_BOV, NCOL, NFIL = 0.012, 7, 3            # bovedilla cerámica de 58 x 20: 7 x 3 celdas, tabiques de 12 mm
W_CEL = (INTEREJE - 2 * MEDIO_NERV - (NCOL + 1) * T_BOV) / NCOL
H_CEL = (-0.05 - ZF - (NFIL + 1) * T_BOV) / NFIL


def vigueta(m):
    return Polygon([(m - 0.05, ZF), (m + 0.05, ZF), (m + 0.05, ZF + 0.035), (m + 0.02, ZF + 0.05), (m + 0.02, ZF + 0.14),
                    (m - 0.02, ZF + 0.14), (m - 0.02, ZF + 0.05), (m - 0.05, ZF + 0.035)])


def forjado(x0, x1, nervios):
    """Forjado unidireccional 20+5 cortado en perpendicular a las viguetas, entre x0 y x1.
    Devuelve: hormigón (capa de compresión + nervios, sin las viguetas), viguetas, bovedillas (tabiques) y celdas."""
    caja_ = box(x0, ZF, x1, 0)
    horm = box(x0, -0.05, x1, 0).union(unary_union([box(m - MEDIO_NERV, ZF, m + MEDIO_NERV, -0.05) for m in nervios]))
    vig = unary_union([vigueta(m) for m in nervios])
    bov_zona = box(x0, ZF, x1, -0.05).difference(horm)
    celdas = []
    m0 = nervios[0]
    for k in range(-3, 4):
        b0 = m0 + MEDIO_NERV + k * INTEREJE                  # arranque de cada bovedilla
        for cx in range(NCOL):
            for cz in range(NFIL):
                xa = b0 + T_BOV + cx * (W_CEL + T_BOV)
                za = ZF + T_BOV + cz * (H_CEL + T_BOV)
                celdas.append(box(xa, za, xa + W_CEL, za + H_CEL))
    celdas = unary_union(celdas).intersection(bov_zona)
    return horm.difference(vig).intersection(caja_), vig.intersection(caja_), bov_zona.difference(celdas), celdas


def bovedillas(x_nerv0, x_nerv1, x0, x1, intereje=0.70):
    """(Compatibilidad con la axonometría) bovedillas y celdas entre x0 y x1 junto a un nervio."""
    _, _, bov, cel = forjado(x0, x1, [(x_nerv0 + x_nerv1) / 2])
    return bov, cel


capas_sec = {}
# forjado 20+5: capa de compresión continua, nervio con su vigueta en el centro y bovedilla cerámica con
# sus celdas a cada lado; las mismas piezas que en la axonometría
horm_sec, vig_sec, bov_sec, huecos_sec = forjado(0, W, [W / 2])
capas_sec['forjado'] = horm_sec
capas_sec['xps'] = box(0, Z_XPS, W, Z_PAN)
panel = perfil_tetones(0, W, Z_PAN)
tubos_x = [x for x in (FASE_TUBO + 0.10 * j for j in range(5)) if x + R_TUBO < W]
tubos = unary_union([Polygon(circulo(x, Z_TET + R_TUBO, R_TUBO)) for x in tubos_x])
mortero = box(0, Z_TET, W, Z_MOR).difference(panel).difference(tubos)
cola = box(0, Z_MOR, W, Z_COLA)
gres = box(0, Z_COLA, W, Z_GRES)

# tramas como la referencia A33c: allí van en pulgadas (MEASUREMENT 0); aquí, en métrico,
# la misma separación real de líneas sale con la escala de la referencia / 25,4
IN = 1 / 25.4
TR = {'AR-CONC': 0.015 * IN, 'HONEY': 0.06 * IN, 'HEX': 0.03 * IN, 'AR-SAND': 0.01 * IN, 'ANSI34': 0.05 * IN}
trama(sec, capas_sec['forjado'], 'A-WALL-PATT', 'AR-CONC', TR['AR-CONC'] * 0.7, rgb=(120, 120, 120), lw=13)
trama(sec, vig_sec, 'A-WALL-PATT', rgb=(215, 215, 215), solido=True)
trama(sec, vig_sec, 'A-WALL-PATT', 'AR-CONC', TR['AR-CONC'] * 0.45, rgb=(100, 100, 100), lw=13)
trama(sec, bov_sec, 'A-WALL-PATT', 'ANSI31', 0.0015 * K_SEC, rgb=(160, 160, 160))
trama(sec, capas_sec['xps'], 'A-WALL-PATT', rgb=(223, 236, 231), solido=True)
trama(sec, capas_sec['xps'], 'A-WALL-PATT', 'HONEY', TR['HONEY'], rgb=VERDE)
trama(sec, panel, 'A-WALL-PATT', 'HONEY', TR['HONEY'] * 0.5, rgb=(140, 140, 140))     # tetones: nido de abeja gris
trama(sec, mortero, 'A-WALL-PATT', 'AR-SAND', TR['AR-SAND'] * 0.6, rgb=(110, 110, 110), lw=25)
trama(sec, cola, 'A-WALL-PATT', rgb=(200, 200, 200), solido=True)
trama(sec, gres, 'A-WALL-PATT', 'ANSI34', TR['ANSI34'] * 0.6, rgb=(120, 120, 120))
# contornos: todas las caras cortadas con el mismo grosor (0,18); celdas y vigueta, finas (0,13)
for g in (capas_sec['xps'], panel, cola, gres):
    contorno(sec, g, 'A-WALL-CAPAS')
for g in (huecos_sec, vig_sec):
    contorno(sec, g, 'A-WALL-CAPAS', lw=13)
contorno(sec, bov_sec.union(huecos_sec).buffer(0), 'A-WALL-CAPAS', lw=13)
linea(sec, [(0, ZF), (W, ZF)], 'A-WALL-CAPAS')
linea(sec, [(0, 0), (W, 0)], 'A-WALL-CAPAS')
linea(sec, [(0, Z_MOR), (W, Z_MOR)], 'A-WALL-CAPAS')
linea(sec, [(0, Z_GRES), (W, Z_GRES)], 'A-WALL-CAPAS', lw=25)
for x in tubos_x:
    linea(sec, circulo(x, Z_TET + R_TUBO, R_TUBO), 'A-WALL-CAPAS', cerrada=True)
    linea(sec, circulo(x, Z_TET + R_TUBO, R_TUBO_INT), 'A-WALL-CAPAS', lw=13, cerrada=True)
# barrera de radón: lámina gruesa a trazos, como las láminas de la referencia, en verde
linea(sec, [(0, 0.001), (W, 0.001)], 'A-WALL', VERDE, 35, ltype='DASHED', ltscale=0.004)
# roturas: abajo y a los lados
def rotura_h(y, x0, x1, xm, a):
    return [(x0, y), (xm - 0.01, y), (xm - 0.005, y + a), (xm + 0.005, y - a), (xm + 0.01, y), (x1, y)]
def rotura_v(x, y0, y1, ym, a):
    return [(x, y0), (x, ym - 0.01), (x + a, ym - 0.005), (x - a, ym + 0.005), (x, ym + 0.01), (x, y1)]
linea(sec, [(0, ZF), (0, Z_GRES)], 'A-DETL-THIN')
linea(sec, [(W, ZF), (W, Z_GRES)], 'A-DETL-THIN')

# números (de dentro, arriba, a fuera, abajo)
XB = -0.036 * FS
for num, yb, objetivo in ((1, 0.1525, (0.02, 0.1525)), (2, 0.118, (0.03, 0.118)), (3, 0.080, (0.05, 0.080)),
                          (4, 0.032, (0.02, 0.032)), (5, -0.001, (0.03, 0.001)), (6, -0.045, (0.03, -0.025))):
    burbuja(sec, num, (XB, yb), objetivo, K_SEC)

# cotas en mm, a la derecha (estilo de la 1:10 de las fichas, escalado)
ds_name = '1-%s (0.20)' % ('%g' % ESC_SEC)
if not doc.dimstyles.has_entry(ds_name):
    ds = doc.dimstyles.duplicate_entry('1-10 (0.20)', ds_name)
    for k_, v_ in (('dimtxt', 0.02), ('dimasz', 0.015), ('dimexo', 0.015), ('dimexe', 0.015),
                   ('dimgap', 0.008), ('dimdle', 0.01)):
        ds.dxf.set(k_, v_ * K_SEC)
XD = W + 0.026 * FS
cortes = [Z_BAR, Z_XPS, Z_PAN, Z_TOP_TET, Z_MOR, Z_COLA, Z_GRES]     # 2 · 60 · 28 · 50 · 5 · 15
for a, b in zip(cortes, cortes[1:]):
    d = msp.add_linear_dim(base=(XD, (a + b) / 2), p1=(W + 0.004, a), p2=(W + 0.004, b), angle=90,
                           dimstyle=ds_name, dxfattribs={'layer': 'C_COD_01'})
    if b - a < 0.01:          # 2 y 5 mm: la cifra, al otro lado de la línea de cota
        d.set_location((XD + 0.0075 * FS, (a + b) / 2 - (0.004 * FS if a == 0 else 0.0)), leader=False, relative=False)
    d.render()
d = msp.add_linear_dim(base=(XD + 0.018 * FS, Z_GRES / 2), p1=(W + 0.004, 0), p2=(W + 0.004, Z_GRES), angle=90,
                       dimstyle=ds_name, dxfattribs={'layer': 'C_COD_01'})
d.render()

# cotas de nivel: suelo acabado, cota de proyecto del forjado (gris) y cota sugerida (verde)
XN = XD + 0.046 * FS
COTA_SUG = -(Z_GRES)
fmt_cota = lambda v: ('−%.2f' % abs(v)).replace('.', ',')


def nivel(y, txt, rgb, lleno=True, sub=None):
    tri = [(XN, y), (XN - 0.004 * FS, y + 0.0065 * FS), (XN + 0.004 * FS, y + 0.0065 * FS)]
    if lleno:
        trama(msp, Polygon(tri), 'A_06_TEXTOS', rgb=rgb, solido=True)
    linea(msp, tri, 'A_06_TEXTOS', rgb, 13, cerrada=True)
    linea(msp, [(XN - 0.008 * FS, y), (XN + 0.034 * FS, y)], 'A_06_TEXTOS', rgb, 13)
    texto(msp, txt, (XN + 0.007 * FS, y + 0.003 * FS), 0.002 * ESC_SEC, rgb)
    if sub:
        texto(msp, sub, (XN - 0.007 * FS, y - 0.0035 * FS - H_SUB / 1000 * ESC_SEC), H_SUB / 1000 * ESC_SEC, rgb)


nivel(Z_GRES, '±0,00', (40, 40, 40), sub='suelo acabado')
nivel(Z_GRES + COTA_PROY, fmt_cota(COTA_PROY), (150, 150, 150), lleno=False, sub='cota de proyecto')
nivel(0.0, fmt_cota(COTA_SUG), VERDE, sub='cota sugerida')
_izq = -0.036 * FS - 0.0185 * K_SEC - 0.002 * FS
_der = max(XN + 0.034 * FS, XN + 0.007 * FS + ancho_txt('±0,00', 2.0) * ESC_SEC / 1000,
           XN - 0.007 * FS + ancho_txt('cota de proyecto', H_SUB) * ESC_SEC / 1000) + 0.002 * FS
SEC_BB = (_izq, ZF - 0.016 * FS, _der, Z_GRES + 0.016 * FS)


# ================================================================== AXONOMETRÍA
AX0, AY0 = 3.0, 0.0
C30 = math.cos(math.radians(30))
LY = 0.425
L = {'forjado': 1.00, 'barrera': 0.94, 'xps': 0.88, 'panel': 0.675, 'mortero': 0.475, 'cola': 0.335, 'gres': 0.315}


def P(X, Y, Z):
    return (AX0 + C30 * (X + Y), AY0 - 0.5 * X + 0.5 * Y + Z)


def cara_frontal(poly_xz):
    """Polígono del plano Y = 0 (x, z) proyectado."""
    if poly_xz.is_empty:
        return poly_xz
    geoms = poly_xz.geoms if hasattr(poly_xz, 'geoms') else [poly_xz]
    out = []
    for g in geoms:
        if g.geom_type != 'Polygon':
            continue
        out.append(Polygon([P(x, 0, z) for x, z in g.exterior.coords], [[P(x, 0, z) for x, z in i.coords] for i in g.interiors]))
    return unary_union(out)


items = []   # (poligono, relleno rgb, trama (patron, escala, rgb) o None, color de línea, grosor)


def add(poly, fill, pat=None, lin=(60, 60, 60), lw=13):
    if poly is not None and not poly.is_empty and poly.area > 1e-9:
        items.append((poly, fill, pat, lin, lw))


def caja(nombre, z0, z1, top, lado, frente, pat_frente=None, lin=(60, 60, 60), frente_xz=None):
    Lx = L[nombre]
    add(Polygon([P(Lx, 0, z0), P(Lx, LY, z0), P(Lx, LY, z1), P(Lx, 0, z1)]), lado, None, lin)
    add(Polygon([P(0, 0, z1), P(Lx, 0, z1), P(Lx, LY, z1), P(0, LY, z1)]), top, None, lin)
    fr = frente_xz if frente_xz is not None else box(0, z0, Lx, z1)
    add(cara_frontal(fr), frente, pat_frente, lin)


G = lambda g: (255 - (255 - g) // 2,) * 3       # grises a la mitad, como en la ficha 03
# forjado 25+5 (solo la parte de arriba con detalle): capa de compresión, nervios y bovedillas
ZF0 = ZF
TA = {k: v * 1.5 for k, v in TR.items()}      # tramas de la axonometría, algo más abiertas
caja('forjado', ZF0, 0.0, G(205), G(160), G(195), ('AR-CONC', TA['AR-CONC'], (160, 160, 160)))
# frente del forjado 20+5: capa de compresión, nervios de 12 cm con vigueta y bovedillas con sus huecos
# (las mismas piezas que en la sección)
horm_ax, vig_ax, bov_ax, cel_ax = forjado(0, L['forjado'], [0.16, 0.86])
add(cara_frontal(bov_ax.union(cel_ax)), G(220), None, (110, 110, 110), 9)
add(cara_frontal(cel_ax), G(185), None, (130, 130, 130), 9)
add(cara_frontal(horm_ax), G(195), ('AR-CONC', TA['AR-CONC'], (160, 160, 160)), (110, 110, 110), 9)
add(cara_frontal(vig_ax), G(165), None, (110, 110, 110), 9)
# barrera de radón (verde oscuro)
caja('barrera', Z_BAR, Z_XPS, VERDE, VERDE, VERDE, None, VERDE)
# XPS (verde claro)
caja('xps', Z_XPS, Z_PAN, (205, 226, 218), (150, 190, 176), (223, 236, 231), ('HONEY', TA['HONEY'], VERDE), VERDE)
# panel de tetones: base gris (EPS con grafito) y su frente con el perfil de tetones
panel_frente = perfil_tetones(0, L['panel'], Z_PAN)
Lp = L['panel']
add(Polygon([P(Lp, 0, Z_PAN), P(Lp, LY, Z_PAN), P(Lp, LY, Z_TET), P(Lp, 0, Z_TET)]), G(150))
add(Polygon([P(0, 0, Z_TET), P(Lp, 0, Z_TET), P(Lp, LY, Z_TET), P(0, LY, Z_TET)]), G(195))

# tetones de la primera fila (cortados por el plano frontal): medio tetón detrás del corte
def teton(X, Y, medio=False):
    n = 24
    angs = [math.pi * i / n for i in range(n + 1)] if medio else [2 * math.pi * i / (2 * n) for i in range(2 * n)]
    top = [P(X + RW * math.cos(a), Y + RW * math.sin(a), Z_TOP_TET) for a in angs]
    bot = [P(X + RW * math.cos(a), Y + RW * math.sin(a), Z_TET) for a in angs]
    lado = unary_union([Polygon(top + bot[::-1]) if medio else Polygon(top).convex_hull.union(Polygon(bot)).convex_hull])
    add(lado, G(160))
    add(Polygon(top) if not medio else Polygon(top), G(205))

xs_tet = [round(PASO * i, 4) for i in range(0, 15) if L['mortero'] < PASO * i < Lp]
for X in xs_tet:
    teton(X, 0.0, medio=True)
add(cara_frontal(panel_frente), G(180), ('HONEY', TA['HONEY'] * 0.5, (130, 130, 130)))
# mortero autonivelante (verde): frente con perfil y tubos
Lm = L['mortero']
tubos_ax = [FASE_TUBO + 0.10 * j for j in range(10) if FASE_TUBO + 0.10 * j < Lp]
tub_m = unary_union([Polygon(circulo(x, Z_TET + R_TUBO, R_TUBO)) for x in tubos_ax if x < Lm])
mort_frente = box(0, Z_TET, Lm, Z_MOR).difference(perfil_tetones(0, Lm, Z_PAN)).difference(tub_m)
add(Polygon([P(Lm, 0, Z_TET), P(Lm, LY, Z_TET), P(Lm, LY, Z_MOR), P(Lm, 0, Z_MOR)]), G(175))
add(Polygon([P(0, 0, Z_MOR), P(Lm, 0, Z_MOR), P(Lm, LY, Z_MOR), P(0, LY, Z_MOR)]), G(215))
add(cara_frontal(mort_frente), G(200), ('AR-SAND', TA['AR-SAND'] * 0.6, (120, 120, 120)))
for x in tubos_ax:
    if x < Lm:
        add(cara_frontal(Polygon(circulo(x, Z_TET + R_TUBO, R_TUBO))), (245, 245, 245))
        add(cara_frontal(Polygon(circulo(x, Z_TET + R_TUBO, R_TUBO_INT))), (255, 255, 255))
# cemento cola y gres
caja('cola', Z_MOR, Z_COLA, G(170), G(150), G(170))
caja('gres', Z_COLA, Z_GRES, (236, 234, 229), (205, 203, 198), (222, 220, 215), ('ANSI34', TA['ANSI34'] * 0.6, (150, 150, 150)))

# tetones y tubos de la franja vista, de atrás hacia delante
pend = []
for X in xs_tet:
    for j in range(1, 9):
        pend.append((X - j * PASO + Z_TOP_TET, 'teton', X, j * PASO))
for x in tubos_ax:
    if Lm < x < Lp:
        pend.append((x - 0 + Z_TET, 'tubo', x, 0))
pend.sort()
for _, tipo, X, Y in pend:
    if tipo == 'teton':
        teton(X, Y)
    else:
        a0 = [P(x_, 0, z_) for x_, z_ in circulo(X, Z_TET + R_TUBO, R_TUBO, 36)]
        a1 = [P(x_, LY, z_) for x_, z_ in circulo(X, Z_TET + R_TUBO, R_TUBO, 36)]
        add(Polygon(a0 + a1).convex_hull, (240, 240, 240))
        add(Polygon(a0), (245, 245, 245))
        add(Polygon([P(x_, 0, z_) for x_, z_ in circulo(X, Z_TET + R_TUBO, R_TUBO_INT, 36)]), (255, 255, 255))

# ocultación: cada cara se recorta con las que tiene delante (las posteriores en la lista)
delante = Polygon()
visibles = []
for poly, fill, pat, lin, lw in reversed(items):
    vis = poly.buffer(0).difference(delante) if not delante.is_empty else poly.buffer(0)
    contornos = [LineString(r) for e_, ints_ in anillos(poly.buffer(0)) for r in [e_] + ints_]
    lin_vis = [c.difference(delante) if not delante.is_empty else c for c in contornos]
    visibles.append((vis, fill, pat, lin, lw, lin_vis))
    delante = unary_union([delante, poly.buffer(1e-7)])
for vis, fill, pat, lin, lw, lin_vis in reversed(visibles):
    trama(msp, vis, 'A-AXO-COLOR', rgb=fill, solido=True)
    if pat:
        trama(msp, vis, 'A-AXO-COLOR', pat[0], pat[1], rgb=pat[2], lw=25 if pat[0] == 'AR-SAND' else 9)
for vis, fill, pat, lin, lw, lin_vis in reversed(visibles):
    for g in lin_vis:
        for s in (g.geoms if hasattr(g, 'geoms') else [g]):
            if s.geom_type == 'LineString' and s.length > 1e-5:
                linea(msp, list(s.coords), 'A-AXO-LIN', lin, lw)

# números de la axonometría (escala 1:15,2 -> k = 1,52)
ESC_AXO = 15.2
K_AXO = ESC_AXO / 10
XB_AX = AX0 + C30 * (L['forjado'] + LY) + 0.075
objetivos = [(1, P(0.16, 0.22, Z_GRES)), (2, P(0.41, 0.26, Z_MOR)), (3, P(0.60, 0.30, Z_TOP_TET)),
             (4, P(0.80, 0.22, Z_PAN)), (5, P(0.915, 0.22, Z_XPS)), (6, P(1.0, 0.25, -0.15))]
ys = []
for num, (ox, oy) in objetivos:
    y = oy + 0.09
    if ys and y > ys[-1] - 0.075:
        y = ys[-1] - 0.075
    ys.append(y)
for (num, (ox, oy)), y in zip(objetivos, ys):
    burbuja(msp, num, (XB_AX, y), (ox, oy), K_AXO, codo=(XB_AX - 0.06, y))

AX_BB = (AX0 - 0.03, P(L['forjado'], 0, ZF0)[1] - 0.03, XB_AX + 0.035, P(0, LY, Z_GRES)[1] + 0.03)
print('caja seccion', [round(v, 3) for v in SEC_BB], 'caja axo', [round(v, 3) for v in AX_BB])


# ================================================================== ESPACIO PAPEL
E = doc.entitydb
fnt = {False: {}, True: {}}


def ancho(s, h, negrita=False):
    key = (h, negrita)
    if key not in fnt[negrita]:
        fnt[negrita][key] = fonts.make_font('GOTHICB.TTF' if negrita else 'GOTHIC.TTF', h)
    return fnt[negrita][key].text_width(s)


def lineas(s, h, w, negrita=False):
    n = 0
    for par in s.split('\\P'):
        palabras, act = par.split(' '), ''
        n += 1
        for p in palabras:
            prueba = (act + ' ' + p).strip()
            if ancho(prueba, h, negrita) > w and act:
                n += 1
                act = p
            else:
                act = prueba
    return n


def T(h, s, y=None, x=None):
    e = E[h]
    e.text = s
    if y is not None or x is not None:
        p = e.dxf.insert
        e.dxf.insert = (x if x is not None else p.x, y if y is not None else p.y)
    return e


def clonar(h):
    src = E[h]
    return ps.add_mtext(src.text, dxfattribs=src.dxfattribs(drop={'handle', 'owner'}))


def borrar(*hs):
    for h in hs:
        if h in E:
            ps.delete_entity(E[h])


# --- cartela
T('388', '01')
T('38A', 'Suelos')
T('391', 'Suelos de planta baja y de\\Psótano sobre cámara sanitaria.')
T('395', 'Suelos sobre forjado\\Psanitario y sótano')
for h in ('394', '395'):
    E[h].dxf.style = 'FICHA NEGRITA'
    E[h].dxf.true_color = 481096
    E[h].dxf.color = 138
DESP = 1.667 * 1.77 * 1.0 + 0.0
for h in ('396', '397', '398', '399', '39A', '39B'):
    p = E[h].dxf.insert
    E[h].dxf.insert = (p.x, p.y - 2.95)
for h in ('39A', '39B'):
    E[h].dxf.style = 'FICHA'
    E[h].dxf.true_color = GRIS_TXT
    E[h].dxf.color = 252
# minilogo: cubierta en gris, suelos en verde, sótano bajo el terreno
E['390'].dxf.true_color = 10132122
E['390'].dxf.const_width = 0.3
E['390'].dxf.layer = 'F-LOGO'
sot = ps.add_hatch(dxfattribs={'layer': 'F-LOGO'})
sot.set_solid_fill(color=7, rgb=(255, 255, 255))
sot.paths.add_polyline_path([(33.0, 203.6), (49.5, 203.6), (49.5, 208.8), (33.0, 208.8)], is_closed=True)
for pts, w_, rgb in (([(33.0, 203.6), (33.0, 208.8)], 0.3, (154, 154, 154)), ([(49.5, 203.6), (49.5, 208.8)], 0.3, (154, 154, 154)),
                     ([(33.0, 209.4), (49.5, 209.4)], 0.3, (154, 154, 154)),
                     ([(16.6, 209.4), (33.0, 209.4)], 0.9, VERDE), ([(33.1, 204.1), (49.4, 204.1)], 0.9, VERDE)):
    e = ps.add_lwpolyline(pts, dxfattribs={'layer': 'F-ACENTO' if rgb == VERDE else 'F-LOGO', 'const_width': w_})
    e.dxf.true_color = colors.rgb2int(rgb)

# --- la propuesta en cifras
cifras = [('39E', '39F', '3A0', '60 mm', 'XPS sobre el forjado', 'Memoria: 40 mm; licitación: sin XPS'),
          ('3A2', '3A3', '3A4', fmt_cota(COTA_SUG), 'Cota sugerida del forjado', 'Proyecto: %s (DET-01)' % fmt_cota(COTA_PROY)),
          ('3A6', '3A7', '3A8', '2 mm', 'Barrera de radón (zona II)', 'Proyecto: calculada, sin partida'),
          ('3AA', '3AB', '3AC', '%d mm' % round(Z_GRES * 1000), 'Del forjado al suelo acabado', 'Proyecto: 100 mm en DET-01')]
for a, b, c, v1, v2, v3 in cifras:
    T(a, v1); T(b, v2); T(c, v3)
    for s, h_ in ((v2, 1.67), (v3, 1.67)):
        if ancho(s, h_) > 42:
            print('AVISO cifra larga:', s, round(ancho(s, h_), 1))
T('3B1', 'Cota sugerida del forjado y\\Pbarrera de radón, pendientes\\Pdel cálculo estructural y de la DF.')

# --- notas sobre el proyecto (letra pequeña)
notas = ['Memoria: XPS de 40 mm, panel de 25 mm y 2 cm de gravilla; U 0,15 y 0,32 en el cálculo energético (PDF p. 35–38 y 255).',
         'DET-01: 10 cm del forjado al suelo acabado, con gres, mortero y suelo radiante; sin XPS ni barrera de radón.',
         'Licitación: panel de 38 mm (22.01) y 9 cm de mortero (10.03.03), sin XPS ni barrera de radón.',
         'Toledo está en zona II de radón (DB-HS 6, apéndice B): barrera y cámara ventilada obligatorias. La memoria las justifica (p. 237).']
nota_hs = [('3B4', '3B5'), ('3B6', '3B7'), ('3B8', '3B9')]
num4 = clonar('3B8'); txt4 = clonar('3B9')
nota_hs.append((num4.dxf.handle, txt4.dxf.handle))
y = 62.6
PASO_NOTA = 1.667 * 1.62 * 1.1532
for (hn, ht), s in zip(nota_hs, notas):
    T(hn, str(nota_hs.index((hn, ht)) + 1), y=y)
    T(ht, s, y=y)
    n = lineas(s, 1.62, 38.3)
    y -= n * PASO_NOTA + 2.6
print('notas acaban en y =', round(y + 2.6, 1))

# --- cabecera, título, entradilla
T('3BB', '\\T1.3;FICHA 01 · SUELOS · FORJADO SANITARIO Y SÓTANO')
T('3BC', 'Suelos sobre forjado\\Psanitario y sótano')
T('3BD', '\\T1.3;TIPO SUELO RADIANTE SOBRE XPS Y BARRERA DE RADÓN')
ent = ('El forjado sanitario ventilado del proyecto, con barrera de radón y 6 cm de XPS bajo el suelo '
       'radiante de tetones. Con la cota sugerida del forjado, el suelo acabado queda donde está.')
T('3BE', ent)
print('entradilla, líneas:', lineas(ent, 2.53, 124))

# --- leyenda de la axonometría (1 arriba -> 6 abajo)
ley = [('Gres porcelánico sobre cemento cola', '15 + 5 mm'),
       ('Plastón de mortero con el tubo del suelo radiante', '50 mm sobre los tetones'),
       ('Panel de tetones de EPS con grafito', '28 mm en total'),
       ('XPS, λ 0,036 W/mK, sobre la barrera', '60 mm'),
       ('Barrera de radón, sellada a la de los muros', '2 mm; difusión < 10{\\H0.6x;\\A2;−11} m²/s'),
       ('Forjado sanitario 20+5', 'sugerida %s (proyecto %s)' % (fmt_cota(COTA_SUG), fmt_cota(COTA_PROY)))]
pares = [('3C1', '3C2', '3C3'), ('3C4', '3C5', '3C6'), ('3C7', '3C8', '3C9'), ('3CA', '3CB', None),
         ('3CC', '3CD', '3CE'), ('3CF', '3D0', '3D1')]
# el 4 no tiene subtítulo en la ficha 03: se copia uno
sub4 = clonar('3C9')
pares[3] = ('3CA', '3CB', sub4.dxf.handle)
y = 234.6
PASO_LEY = 1.667 * 1.82 * 1.0696
for (hn, ht, hs), (t1, t2) in zip(pares, ley):
    T(hn, E[hn].text, y=y)
    T(ht, t1, y=y)
    n = lineas(t1, 1.82, 28.6)
    ys_ = y - n * PASO_LEY
    T(hs, t2, y=ys_)
    n2 = lineas(t2.replace('{\\H0.6x;\\A2;−11}', '-11'), 1.82, 28.6)
    if n2 > 1:
        E[hs].dxf.width = 28.6
    y = ys_ - n2 * PASO_LEY - 2.2
print('leyenda acaba en y =', round(y, 1))
borrar('3D2', '3D3')

# --- banda de transmitancia
T('3D7', '\\T1.3;TRANSMITANCIA DEL SUELO')
T('3D9', 'Licitación')
T('3DC', 'Propuesta')
R_SUP = 0.17 + 0.17
R_FORJ = 0.22            # forjado 20+5 cerámico, estimada
R_PANEL_28 = 0.50        # panel de tetones de 28 mm en EPS con grafito (λ 0,030), estimada
R_GRES_COLA = 0.015 / 1.3 + 0.005 / 1.0
U_LIC = 1 / (R_SUP + R_GRES_COLA + 0.09 / 1.3 + 1.27 + R_FORJ)              # licitación: panel R 1,27 y 9 cm de mortero
U_PRO = 1 / (R_SUP + R_GRES_COLA + 0.05 / 1.3 + R_PANEL_28 + 0.060 / 0.036 + R_FORJ)
print('U licitación %.3f  propuesta %.3f  mejora %.1f %%' % (U_LIC, U_PRO, 100 * (1 - U_PRO / U_LIC)))
fmt = lambda u: ('%.2f' % u).replace('.', ',')
T('3DA', fmt(U_LIC))
T('3DD', fmt(U_PRO))
largo = 27.0
E['3DB'].paths.clear(); E['3DB'].paths.add_polyline_path([(105, 110.9), (105 + largo, 110.9), (105 + largo, 113.3), (105, 113.3)], is_closed=True)
lp = largo * U_PRO / U_LIC
E['3DE'].paths.clear(); E['3DE'].paths.add_polyline_path([(136, 110.9), (136 + lp, 110.9), (136 + lp, 113.3), (136, 113.3)], is_closed=True)
T('3DF', '−%d %%' % round(100 * (1 - U_PRO / U_LIC)))
T('3E0', 'de pérdidas por el suelo\\Pfrente a la licitación.\\PLímite CTE: 0,65.')
nota_u = ('U sin contar la cámara ni el terreno (cálculo propio). Licitación: panel de 38 mm, R 1,27. Propuesta: '
          'panel de 28 mm, R ≈ 0,50 (estimada), y XPS λ 0,036. Límite: DB-HE, zona D3 (memoria, p. 255).')
T('3E1', nota_u)
print('nota U, líneas:', lineas(nota_u, 1.57, 130))

# --- lo que cambia / igual / cotas
cambia = ['XPS de 60 mm sobre el forjado (licitación: sin XPS).',
          'Barrera de radón de 2 mm, sellada a la de los muros.',
          'Cota sugerida del forjado: %s (proyecto: %s).' % (fmt_cota(COTA_SUG), fmt_cota(COTA_PROY))]
viñetas = [('3E3', '3E4'), ('3E5', '3E6'), ('3E7', '3E8')]
borrar('3EB', '3EC')
y = 94.4
PASO_V = 1.667 * 1.93 * 1.1532
for (hq, ht), s in zip(viñetas, cambia):
    T(ht, s, y=y)
    q = E[hq]
    q.paths.clear(); q.paths.add_polyline_path([(68.0, y - 1.9), (69.5, y - 1.9), (69.5, y - 0.4), (68.0, y - 0.4)], is_closed=True)
    E[ht].dxf.width = 46.0
    n = lineas(s, 1.93, 46.0)
    y -= n * PASO_V + 1.0
borrar('3ED', '3EE', '3EF', '3F0')
y -= 1.8
T('3F1', '\\T1.3;IGUAL QUE EN EL PROYECTO', y=y)
igual = ('Forjado sanitario ventilado, panel de tetones, plastón de mortero con el tubo del suelo radiante '
         'y gres porcelánico.')
y -= 4.4
T('3F2', igual, y=y)
E['3F2'].dxf.width = 48.0
y -= lineas(igual, 1.93, 48.0) * PASO_V + 3.2
T('433', '\\T1.3;COTAS', y=y)
abs_ = lambda base, rel: ('%.2f' % (base + rel)).replace('.', ',')
cotas = ('Cara superior del forjado. De proyecto: %s (%s en planta baja y %s en el sótano). '
         'Sugerida: %s (%s y %s). El suelo acabado sigue a 515,00 y 511,85.'
         % (fmt_cota(COTA_PROY), abs_(515.00, COTA_PROY), abs_(511.85, COTA_PROY),
            fmt_cota(COTA_SUG), abs_(515.00, COTA_SUG), abs_(511.85, COTA_SUG)))
y -= 4.4
T('434', cotas, y=y)
E['434'].dxf.width = 48.0
fin = y - lineas(cotas, 1.93, 48.0) * PASO_V
print('bloque izquierdo acaba en y =', round(fin, 1))

# --- pies de los dibujos y pie de página
pie_sec = 'SECCIÓN · COTAS EN MM · EN VERDE, LO QUE CAMBIA'
x_pie = min(127.3, 198.0 - ancho(pie_sec, 1.57) * 1.3)
T('3F3', '\\T1.3;SECCIÓN · COTAS EN MM · {\\c4740871;EN VERDE, LO QUE CAMBIA}', x=x_pie, y=21.6)
print('pie de la sección desde x =', round(x_pie, 1))
borrar('4C6', '4C7')
T('3F5', '{\\fCentury Gothic|b1|i0|c0|p34;Vivienda unifamiliar aislada con garaje y piscina · Cigarral Montealegre, Toledo} '
         '· Base: proyecto básico y de ejecución, febrero 2026 · Ficha 01 · v2 · noviembre 2026.\\P'
         'Fuentes: memoria del proyecto (PDF p. 20–21, 34–38, 92–94, 187, 235–238 y 253–255), plano DET-01, mediciones de '
         'licitación de 15/06/2026 (04.04, 10.03.03 y 22.01), ficha del panel Grafiklett (Fittings Estándar) y '
         'DB-HS 6 (RD 732/2019: 3.1, 3.2 y apéndice B). Capas numeradas igual en la axonometría y en la sección.')

# --- ventanas
def ventana(h, bb, x0, y0, x1, y1, escala=None):
    vp = E[h]
    wpap, hpap = x1 - x0, y1 - y0
    vp.dxf.center = ((x0 + x1) / 2, (y0 + y1) / 2)
    vp.dxf.width, vp.dxf.height = wpap, hpap
    bx0, by0, bx1, by1 = bb
    if escala is None:
        escala = max((bx1 - bx0) / wpap, (by1 - by0) / hpap) * 1000
    vp.dxf.view_center_point = ((bx0 + bx1) / 2, (by0 + by1) / 2)
    vp.dxf.view_height = hpap * escala / 1000
    print(h, 'escala 1:%.2f' % escala)

ventana('3BF', AX_BB, 68.0, 146.0, 161.0, 238.0, ESC_AXO)
ventana('3C0', SEC_BB, *VP_SEC, ESC_SEC)

doc.saveas(OUT)
print('guardado', OUT)
