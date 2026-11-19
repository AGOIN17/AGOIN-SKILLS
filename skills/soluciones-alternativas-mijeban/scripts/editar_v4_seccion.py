"""Ficha 03 v4 (sección del alero): durmiente de canto tras medio pie de ladrillo y par volado hasta el canalón."""
import sys, math
sys.path.insert(0, r"C:\Users\usuario\AppData\Local\Temp\claude\db3e6b77c6882b90\bc43d6f6-dd79-406e-a22c-6ef32f44ca96\scratchpad")
import ezdxf
from shapely.geometry import LineString, Polygon
from medir import lineas

ENT, SAL = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(ENT); E = doc.entitydb; msp = doc.modelspace()
M = 0.268
PU = lambda x: 0.096 + (x + 0.276) * M          # cara inferior del panel (friso), igual que en el DWG
D = 0.18 / math.cos(math.atan(M))               # canto del par en vertical
X_T0, X_T1 = 0.015, 0.248                       # caras del tosco
B_DUR, H_DUR = 0.100, 0.140                     # durmiente de canto
X_D0 = X_T1 - B_DUR                             # 0,148: queda 0,133 de ladrillo por delante
X_FIN0, X_FIN1 = -0.316, -0.338                 # extremo del par: la línea de cierre del cajón (DET-01)
assert X_D0 - X_T0 >= 0.05

def set_hatch(h, pts):
    h.paths.clear(); h.paths.add_polyline_path(pts, is_closed=True)

def set_poly(p, pts, cerrada=None):
    p.set_points(pts, format="xy")
    if cerrada is not None:
        p.closed = cerrada

# 1 · durmiente de canto, pegado a la cara interior del tosco, con su cara superior a la cota del fondo del cajón (0)
dur = [(X_D0, -H_DUR), (X_T1, -H_DUR), (X_T1, 0.0), (X_D0, 0.0)]
set_hatch(E["108"], dur); set_poly(E["109"], dur, True)
E["10A"].dxf.start = (X_D0, -H_DUR); E["10A"].dxf.end = (X_T1, 0.0)
E["10B"].dxf.start = (X_T1, -H_DUR); E["10B"].dxf.end = (X_D0, 0.0)

# 2 · tosco en L: medio pie de ladrillo por delante del durmiente hasta la cota 0
YC = -0.158
set_hatch(E["9B"], [(X_T0, YC), (X_T1, YC), (X_T1, -H_DUR), (X_D0, -H_DUR), (X_D0, 0.0), (X_T0, 0.0)])
set_poly(E["44A"], [(X_T0, 0.0), (X_D0, 0.0), (X_D0, -H_DUR), (X_T1, -H_DUR), (X_T1, YC), (X_T0, YC)], False)

# 3 · par: asiento horizontal a la cota 0 y vuelo hasta la línea de cierre del cajón
y_fin = PU(X_FIN1)
par = [(0.5, PU(0.5) - D), (X_T1, PU(X_T1) - D), (X_T1, 0.0), (X_FIN0, 0.0), (X_FIN1, y_fin), (0.5, PU(0.5))]
set_hatch(E["10C"], par); set_poly(E["10D"], par, False)
pol_par = Polygon(par)
# vetas del par, prolongadas hasta el borde del par
for h, off in (("10E", 0.045), ("10F", 0.093), ("110", 0.1395)):
    linea = LineString([(-0.6, PU(-0.6) - off), (0.496, PU(0.496) - off)]).intersection(pol_par.buffer(-0.004))
    seg = max(getattr(linea, "geoms", [linea]), key=lambda g: g.length)
    set_poly(E[h], list(seg.coords), False)
# el fondo trasero del cajón (x = 0) ya no corta el par
set_poly(E["15F"], [(-0.562, 0.266), (-0.491, 0.0), (0.0, 0.0)], False)
# la bajante va por detrás del par: se oculta lo que queda tapado
baj = E["162"]
pts = [(x, y) for x, y in baj.get_points("xy")]
visible = Polygon(pts).exterior.difference(pol_par) if baj.closed else LineString(pts).difference(pol_par)
partes = [g for g in getattr(visible, "geoms", [visible]) if g.length > 0.002]
attrs = {k: baj.dxf.get(k) for k in ("layer", "lineweight", "linetype") if baj.dxf.hasattr(k)}
msp.delete_entity(baj)
for g in partes:
    msp.add_lwpolyline(list(g.coords), dxfattribs=attrs)
print(f"bajante: {len(partes)} tramos visibles")

# 4 · número 1: la directriz va al nuevo durmiente
cx, cy = (X_D0 + X_T1) / 2, -H_DUR / 2
p18a = [(x, y) for x, y in E["18A"].get_points("xy")]
set_poly(E["18A"], [(cx, cy), p18a[-1]], False)
dot = E["18B"]
dot.translate(cx - 0.12, cy - 0.05, 0)

# 5 · textos (mismo número de líneas que antes)
psp = doc.layouts.get("FICHA-A4")
cambios = {
    "3C2": ("Durmiente de madera de canto, tras medio pie de ladrillo", None),
    "3C3": ("100 × 140 mm, a calcular", None),
    "3C5": ("Par GL24h 140 × 180, hasta el canalón", None),
    "3E6": ("Pares sobre durmiente de madera, no en viga con placa.", None),
    "3BE": ("El panel sándwich del proyecto, con su friso de abeto visto, sobre pares a 1,20 m como máximo, "
            "apoyados en un durmiente de madera y atados. Placa bajo teja ventilada y teja fijada sin mortero.", None),
}
for h, (t, _) in cambios.items():
    e = E[h]
    n0 = len(lineas(e.text, e.dxf.char_height, e.dxf.width)[0]) if e.dxf.width else 1
    n1 = len(lineas(t, e.dxf.char_height, e.dxf.width)[0]) if e.dxf.width else 1
    print(f"{h}: {n0} → {n1} líneas · {t[:60]}")
    assert n1 <= n0, (h, n0, n1)
    e.text = t
pie = E["3F5"]; assert "· v3 ·" in pie.text; pie.text = pie.text.replace("· v3 ·", "· v4 ·")

doc.saveas(SAL)
print(f"durmiente {B_DUR*1000:.0f} × {H_DUR*1000:.0f}; ladrillo por delante {(X_D0 - X_T0)*1000:.0f} mm; "
      f"par: canto en la fachada {PU(0.0):.3f}, en el extremo {y_fin:.3f}; vuelo {abs(X_FIN1):.3f} m")
