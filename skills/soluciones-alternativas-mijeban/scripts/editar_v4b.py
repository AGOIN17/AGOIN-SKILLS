"""Ficha 03 v4: alero como DET-01 con durmiente de madera de 200 × 300 en lugar de la viga de hormigón.

- Durmiente 200 × 300 de canto, tras 5 cm de ladrillo, con su cara superior a la cota del fondo del cajón (0).
- El par llega recto (sin cajear), cortado a plomo a 0,14 m de la fachada, en una U de acero e=10 de 0,12 × 0,20
  con 3 pernos, como en DET-01.
- El ladrillo de fachada sube hasta el panel; entre el ladrillo y la testa del par, aislamiento.
- El muro se prolonga en el dibujo hasta −0,33 para ver el durmiente entero; la cumbrera pasa a 1:30.
"""
import sys, math
sys.path.insert(0, r"C:\Users\usuario\AppData\Local\Temp\claude\db3e6b77c6882b90\bc43d6f6-dd79-406e-a22c-6ef32f44ca96\scratchpad")
import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.fonts import fonts
from ezdxf import bbox
from shapely.geometry import LineString, Polygon, box
from medir import lineas

ENT, SAL = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(ENT); E = doc.entitydb; msp = doc.modelspace(); psp = doc.layouts.get("FICHA-A4")
M = 0.268
PU = lambda x: 0.096 + (x + 0.276) * M
D = 0.18 / math.cos(math.atan(M))
X_T0, X_T1 = 0.015, 0.248                 # tosco
X_D0, X_D1 = 0.098, 0.248                 # durmiente 150 de ancho, enrasado con la cara interior del tosco
Y_D0, Y_D1 = -0.200, 0.0                  # 200 de canto
X_U0, X_U1, H_U = X_D0, X_D1, 0.170      # U de acero e=10 sobre todo el durmiente; alas por debajo de la cara superior del par
X_H = (D - 0.096) / M - 0.276             # 0,061: aquí la cara inferior del par llega a la cota del fondo del cajón
X_FIN0, X_FIN1 = -0.316, -0.338           # fin del par bajo el canalón: línea de cierre del cajón (DET-01)
YC_OLD, YC = -0.158, -0.330               # línea de rotura antigua y nueva
VERDE, VERDE_T, GRIS = (7, 87, 72), (214, 229, 224), (40, 40, 40)
tc = lambda c: (c[0] << 16) | (c[1] << 8) | c[2]
assert X_D0 - X_T0 >= 0.05 - 1e-9

def set_hatch(h, pts):
    h.paths.clear(); h.paths.add_polyline_path(pts, is_closed=True)

def set_poly(p, pts, cerrada=None):
    p.set_points(pts, format="xy")
    if cerrada is not None:
        p.closed = cerrada

def bajar_fondo(h_hatch, h_poly):
    """Prolonga hasta YC una banda del muro cortada en YC_OLD."""
    for h in (h_hatch, h_poly):
        if h is None:
            continue
        e = E[h]
        if e.dxftype() == "HATCH":
            pts = []
            for p in e.paths:
                pts = [(v[0], v[1]) for v in p.vertices]
            set_hatch(e, [(x, YC if abs(y - YC_OLD) < 1e-3 else y) for x, y in pts])
        else:
            set_poly(e, [(x, YC if abs(y - YC_OLD) < 1e-3 else y) for x, y in e.get_points("xy")])

def add_poly(pts, capa, rgb=None, cerrada=False, lw=None):
    a = {"layer": capa}
    if rgb: a["true_color"] = tc(rgb)
    if lw: a["lineweight"] = lw
    return msp.add_lwpolyline(pts, close=cerrada, dxfattribs=a)

def add_hatch(pts, rgb, capa="A-WALL-PATT"):
    h = msp.add_hatch(dxfattribs={"layer": capa}); h.set_solid_fill(rgb=rgb)
    h.paths.add_polyline_path(pts, is_closed=True); return h

# ------------------------------------------------ 1 · el muro se prolonga hasta −0,33
for hh, hp in (("9D", "44B"), ("A1", "44D"), ("E6", "451"), ("105", "452")):
    bajar_fondo(hh, hp)
for h in ("453", "454"):                                  # bajante, por fuera
    bajar_fondo(None, h)
E["455"].translate(0, YC - YC_OLD, 0)                     # línea de rotura
for h in ("44E", "450"):                                  # restos de bucles cortados en la rotura antigua
    msp.delete_entity(E[h])
# bucles del EPS: se repite hacia abajo una ventana de dos periodos
banda = box(0.262, YC, 0.364, YC_OLD)
ventana = []
for e in msp.query("LWPOLYLINE[layer=='A-DETL-AISL']"):
    b = bbox.extents([e], fast=True)
    if 0.262 <= b.extmin.x and b.extmax.x <= 0.364 and -0.1501 <= b.extmin.y and b.extmax.y <= -0.0833 + 1e-4:
        ventana.append(e)
n_b = 0
for k in (1, 2, 3):
    for e in ventana:
        g = LineString([(x, y - 0.0667 * k) for x, y in e.get_points("xy")]).intersection(banda)
        for s in getattr(g, "geoms", [g]):
            if not s.is_empty and s.length > 1e-4:
                n = add_poly(list(s.coords), "A-DETL-AISL", (85, 85, 85)); n_b += 1
# bloques del ladrillo de gran formato: se repite la hilada más baja
hilada = []
for e in msp:
    b = bbox.extents([e], fast=True)
    if b.has_data and 0.369 <= b.extmin.x and b.extmax.x <= 0.424 and -0.158 <= b.extmin.y and b.extmax.y <= -0.111 \
            and e.dxftype() in ("HATCH", "LWPOLYLINE"):
        hilada.append(e)
for k in (1, 2, 3):
    for e in hilada:
        c = e.copy(); c.translate(0, -0.053 * k, 0); msp.add_entity(c)
print(f"muro prolongado: {n_b} bucles, {len(hilada) * 3} piezas de gran formato")

# ------------------------------------------------ 2 · tosco: hoja de 5 cm por delante hasta el panel; enfoscado bajo el durmiente
# el ladrillo de delante sube hasta la cara inferior del par (la sección corta por un par)
tosco = [(X_T0, YC), (X_T1, YC), (X_T1, Y_D0), (X_D0, Y_D0), (X_D0, PU(X_D0) - D), (X_H, 0.0), (X_T0, 0.0)]
set_hatch(E["9B"], tosco)
set_poly(E["44A"], [(X_D0, PU(X_D0) - D), (X_D0, Y_D0), (X_T1, Y_D0), (X_T1, YC)], False)
bajar_fondo("9F", "44C")                                   # el enfoscado sigue entero: el durmiente no entra en él

# ------------------------------------------------ 3 · durmiente 200 × 300
dur = [(X_D0, Y_D0), (X_D1, Y_D0), (X_D1, Y_D1), (X_D0, Y_D1)]
set_hatch(E["108"], dur); set_poly(E["109"], dur, True)
E["10A"].dxf.start = (X_D0, Y_D0); E["10A"].dxf.end = (X_D1, Y_D1)
E["10B"].dxf.start = (X_D1, Y_D0); E["10B"].dxf.end = (X_D0, Y_D1)

# ------------------------------------------------ 4 · par entero: del interior a debajo del canalón, recto sobre el durmiente
# solo en el vuelo se corta en horizontal a la cota del fondo del cajón, para no asomar por debajo
par = [(0.5, PU(0.5) - D), (X_H, 0.0), (X_FIN0, 0.0), (X_FIN1, PU(X_FIN1)), (0.5, PU(0.5))]
set_hatch(E["10C"], par); set_poly(E["10D"], par, False)
E["10C"].set_solid_fill(rgb=(238, 238, 238))             # un solo color dentro y fuera; sin verde
E["10D"].dxf.true_color = tc(GRIS)
pol_par = Polygon(par)
assert pol_par.is_valid and Polygon(par).convex_hull.area - pol_par.area < 1e-9
for h, off in (("10E", 0.045), ("10F", 0.093), ("110", 0.1395)):
    l = LineString([(-0.6, PU(-0.6) - off), (0.496, PU(0.496) - off)]).intersection(pol_par.buffer(-0.004))
    seg = max(getattr(l, "geoms", [l]), key=lambda g: g.length)
    set_poly(E[h], list(seg.coords), False)
    E[h].dxf.true_color = tc((130, 130, 130))
# el fondo trasero del cajón (x = 0) ya no corta el par
assert len(E["15F"].get_points("xy")) == 4
set_poly(E["15F"], [(-0.562, 0.266), (-0.491, 0.0), (0.0, 0.0)], False)
# la bajante queda detrás del par: se oculta lo tapado
baj = E["162"]
pts = [(x, y) for x, y in baj.get_points("xy")]
visible = (Polygon(pts).exterior if baj.closed else LineString(pts)).difference(pol_par)
partes = [g for g in getattr(visible, "geoms", [visible]) if g.length > 0.002]
attrs = {k: baj.dxf.get(k) for k in ("layer", "lineweight", "linetype", "true_color", "color") if baj.dxf.hasattr(k)}
msp.delete_entity(baj)
for g in partes:
    msp.add_lwpolyline(list(g.coords), dxfattribs=attrs)
print(f"bajante: {len(partes)} tramos visibles")

# ------------------------------------------------ 5 · U de acero e=10 con 3 pernos (DET-01)
# base cortada bajo el par; las alas quedan detrás del par y van en discontinua; los pernos, cortados
add_hatch([(X_U0, 0.0), (X_U1, 0.0), (X_U1, 0.010), (X_U0, 0.010)], GRIS)
def discontinua(a, b, raya=0.018, hueco=0.010):
    L = math.dist(a, b); ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L; s = 0.0
    while s < L - 1e-6:
        e_ = min(s + raya, L)
        msp.add_line((a[0] + ux * s, a[1] + uy * s), (a[0] + ux * e_, a[1] + uy * e_),
                     dxfattribs={"layer": "A-DETL-THIN", "true_color": tc((90, 90, 90)), "lineweight": 13})
        s = e_ + hueco
ala = [(X_U0, 0.010), (X_U0, H_U), (X_U1, H_U), (X_U1, 0.010)]
for a, b in zip(ala, ala[1:]):
    discontinua(a, b)
assert H_U < PU(X_U0) - 0.01                               # el ala no asoma por encima del par
xb = (X_U0 + X_U1) / 2
for yb in (0.065, 0.105, 0.145):
    c = msp.add_circle((xb, yb), 0.0065, dxfattribs={"layer": "A-DETL", "true_color": tc(GRIS)})
    assert PU(xb) - D + 0.01 < yb < min(H_U, PU(xb)) - 0.01
assert abs((PU(X_U0) - D) - 0.010) < 0.001                 # el par apoya en la base de la U por el borde exterior del durmiente

# ------------------------------------------------ 6 · número 1 al durmiente
cx, cy = (X_D0 + X_D1) / 2, (Y_D0 + Y_D1) / 2
p18a = [(x, y) for x, y in E["18A"].get_points("xy")]
set_poly(E["18A"], [(cx, cy), p18a[-1]], False)
E["18B"].translate(cx - 0.12, cy - 0.05, 0)

# ------------------------------------------------ 7 · ventanas: el alero ve hasta −0,36; la cumbrera pasa a 1:30
vp_alero = E["3C0"]
vp_alero.dxf.center = (vp_alero.dxf.center.x, 72.3, 0); vp_alero.dxf.height = 56.4
vp_alero.dxf.view_height = 56.4 / 50
vp_alero.dxf.view_center_point = (vp_alero.dxf.view_center_point.x, 0.2122 + (72.3 - 73.388) / 50, 0)
print("alero: ve de", round(vp_alero.dxf.view_center_point.y - 0.564, 3), "a", round(vp_alero.dxf.view_center_point.y + 0.564, 3))
vp_cum = [v for v in psp.query("VIEWPORT") if abs(v.dxf.view_center_point.x - 5.0) < 0.01][0]
K30, Y_BASE, YB_W = 1000 / 30, 22.0, -0.268 * 0.27
vp_cum.dxf.center = (vp_cum.dxf.center.x, 30.1, 0); vp_cum.dxf.height = 17.4
vp_cum.dxf.view_height = 17.4 / K30
vp_cum.dxf.view_center_point = (5.0, YB_W + (30.1 - Y_BASE) / K30, 0)
E["3F3"].dxf.insert = (E["3F3"].dxf.insert.x, 42.1, 0)
# rótulos de la cumbrera, mayores para que a 1:30 midan lo mismo en papel
for e in list(msp):
    if e.dxftype() in ("TEXT", "LWPOLYLINE", "HATCH") and e.dxf.layer in ("A_06_TEXTOS", "A-NUMEROS"):
        b = bbox.extents([e], fast=True)
        if b.has_data and 4.2 < b.extmin.x and b.extmax.x < 5.8 and -0.3 < b.extmin.y and b.extmax.y < 0.7:
            msp.delete_entity(e)
H_T = 0.045
f = fonts.make_font("GOTHIC.TTF", H_T)
def rotulo(textos, x_txt, y_txt, destino, lado):
    for i, t in enumerate(textos):
        txt = msp.add_text(t, height=H_T, dxfattribs={"layer": "A_06_TEXTOS", "style": "1-10 (0.20)", "true_color": tc(VERDE)})
        txt.set_placement((5.0 + x_txt, y_txt - i * 0.063), align=TextEntityAlignment.RIGHT if lado < 0 else TextEntityAlignment.LEFT)
        assert abs(x_txt) + f.text_width(t) < 1.0, t
    xd = x_txt + (0.015 if lado < 0 else -0.015)
    msp.add_lwpolyline([(5.0 + xd, y_txt + 0.015), (5.0 + destino[0], destino[1])],
                       dxfattribs={"layer": "A-NUMEROS", "true_color": tc((70, 70, 70)), "lineweight": 13})
    d = msp.add_hatch(dxfattribs={"layer": "A-NUMEROS"}); d.set_solid_fill(rgb=VERDE)
    d.paths.add_edge_path().add_arc((5.0 + destino[0], destino[1]), 0.0135, 0, 360)
YO = lambda x: -M * abs(x) + 0.237 + 0.025
YS = YO(0.1425) + 0.063 + 0.020
rotulo(["Listón sobre", "pieza en seco"], -0.33, 0.37, (-0.004, 0.297), -1)
rotulo(["Paso del aire"], -0.33, 0.205, (-0.075, YO(0.075) + 0.02), -1)
rotulo(["Caballete", "atornillado"], 0.33, 0.37, (0.09, YS + 0.105 * math.sin(math.acos(0.09 / 0.1425))), 1)
rotulo(["Banda", "transpirable"], 0.33, 0.205, (0.18, YO(0.18) + 0.067), 1)

# ------------------------------------------------ 8 · textos (mismo número de líneas)
cambios = {"3C2": "Durmiente de madera de canto, a haces con el tosco por dentro",
           "3C3": "150 × 200 mm, a calcular",
           "3C5": "Par GL24h 140 × 180 hasta el canalón",
           "3E6": "Durmiente de madera en lugar de viga de hormigón.",
           "3BE": ("El panel sándwich del proyecto, con su friso de abeto visto, sobre pares a 1,20 m como máximo, "
                   "apoyados en un durmiente de madera y atados. Placa bajo teja ventilada y teja fijada sin mortero.")}
for h, t in cambios.items():
    e = E[h]
    n0 = len(lineas(e.text, e.dxf.char_height, e.dxf.width)[0]) if e.dxf.width else 1
    n1 = len(lineas(t, e.dxf.char_height, e.dxf.width)[0]) if e.dxf.width else 1
    print(f"{h}: {n0} → {n1} líneas · {t[:58]}")
    assert n1 <= n0, (h, n0, n1)
    e.text = t
pie = E["3F5"]; assert "· v3 ·" in pie.text; pie.text = pie.text.replace("· v3 ·", "· v4 ·")
doc.saveas(SAL)
print(f"durmiente {1000*(X_D1-X_D0):.0f} × {1000*(Y_D1-Y_D0):.0f}; ladrillo delante {1000*(X_D0-X_T0):.0f} mm; "
      f"par de {X_FIN1:.3f} a 0,5; holgura bajo el par sobre la U: {1000*(PU(X_U0)-D-0.010):.0f} a {1000*(PU(X_U1)-D-0.010):.0f} mm")
