"""Ficha 03 v4 · axonometría: durmiente de canto 150 × 200 bajo los pares y pares enteros hasta el canalón.

La axo es isométrica a 30° sin reducción: X a lo largo del durmiente, Y a lo largo del par (hacia la cumbrera), Z vertical.
Correspondencia con la sección: Y = x_sección − 0,015 ; Z = y_sección − 0,100 (la cara superior del par es la del v3).
Pares y durmiente se rehacen en 3D, se ocultan con el contorno del panel y entre sí, y la ventana se ajusta para que
quepan, manteniendo en papel el tamaño y la posición de los números.
"""
import sys, math
import ezdxf
from ezdxf import path as ezpath, bbox
from ezdxf.enums import TextEntityAlignment
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union

ENT, SAL = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(ENT); E = doc.entitydb; msp = doc.modelspace(); psp = doc.layouts.get("FICHA-A4")
M = 0.268; D = 0.18 / math.cos(math.atan(M)); C = math.cos(math.radians(30))
OX, OY = 0.032, -3.0875
P = lambda X, Y, Z: (OX + C * (X + Y), OY - 0.5 * X + 0.5 * Y + Z)
ZT = lambda Y: 0.074 + M * Y                       # cara superior del par = cara inferior del panel
VERDE = (7, 87, 72)
tc = lambda c: (c[0] << 16) | (c[1] << 8) | c[2]
# la proyección reproduce el v3 (esquina trasera del par derecho y frente del par izquierdo)
assert math.dist(P(1.2, 1.0141, ZT(1.0141)), (1.9494, -2.8347)) < 1e-3
assert math.dist(P(-0.14, 0.0, ZT(0.0)), (-0.0892, -2.9435)) < 1e-3

# ------------------------------------------------ geometría 3D (de la sección v4)
YF0, YF1 = -0.316 - 0.015, -0.338 - 0.015          # fin del par bajo el canalón (fondo / cara superior)
YH = (D - 0.174) / M                               # desde aquí hacia fuera, cara inferior horizontal (fondo del cajón)
YB_T, YB_B = 1.0141, 1.0607                        # testa trasera, como en el v3
ZC = -0.100                                        # fondo del cajón (y = 0 en la sección)
par_yz = [(YF0, ZC), (YH, ZC), (YB_B, ZT(YB_B) - D), (YB_T, ZT(YB_T)), (YF1, ZT(YF1))]
assert abs(ZT(YH) - D - ZC) < 1e-6
PARES = [(-0.14, 0.0), (1.06, 1.20)]               # a 1,20 m entre ejes
XA, XB = -0.18, 1.30                               # durmiente cortado a ambos lados
YD0, YD1, ZD0, ZD1 = 0.098 - 0.015, 0.248 - 0.015, -0.200 - 0.100, 0.0 - 0.100

def caras_par(X0, X1):
    caras = [("lado", [P(X1, y, z) for y, z in par_yz])]
    for (ya, za), (yb, zb) in zip(par_yz, par_yz[1:] + par_yz[:1]):
        ny, nz = zb - za, -(yb - ya)               # normal exterior en el plano YZ (polígono antihorario)
        if -ny + nz > 1e-9:                        # mira al observador (1, −1, 1)
            tipo = "testa" if ya < 0 and yb < 0 and abs(ya - yb) < 0.05 else "arriba"
            caras.append((tipo, [P(X0, ya, za), P(X1, ya, za), P(X1, yb, zb), P(X0, yb, zb)]))
    return caras
COL_PAR = {"arriba": (238, 238, 238), "lado": (230, 230, 230), "testa": (222, 222, 222)}
caras_dur = [("arriba", [P(XA, YD0, ZD1), P(XB, YD0, ZD1), P(XB, YD1, ZD1), P(XA, YD1, ZD1)], (224, 235, 231)),
             ("frente", [P(XA, YD0, ZD0), P(XB, YD0, ZD0), P(XB, YD0, ZD1), P(XA, YD0, ZD1)], (210, 226, 220)),
             ("corte", [P(XB, YD0, ZD0), P(XB, YD1, ZD0), P(XB, YD1, ZD1), P(XB, YD0, ZD1)], (195, 214, 208))]

# ------------------------------------------------ lo que se quita del v3 y contorno del panel (oculta lo de debajo)
viejos = ("330 331 332 333 334 335 336 32E 32F 337 338 339 33A 33B 33C 33D 33E 33F 340 341 342 343 344 345 346 347 "
          "348 349 34A 34B 34C 34D 34E 34F 350 351 352 353 354 355").split()
cota_attr = {k: E["352"].dxf.get(k) for k in ("layer", "lineweight", "true_color", "color") if E["352"].dxf.hasattr(k)}
marca_attr = {k: E["353"].dxf.get(k) for k in ("layer", "lineweight", "true_color", "color") if E["353"].dxf.hasattr(k)}
refer_attr = {k: E["350"].dxf.get(k) for k in ("layer", "lineweight", "true_color", "color") if E["350"].dxf.hasattr(k)}
t355 = E["355"]
txt_attr = {k: t355.dxf.get(k) for k in ("layer", "style", "true_color", "color", "width") if t355.dxf.hasattr(k)}
H_TXT0, ROT_TXT, TEXTO = t355.dxf.height, t355.dxf.rotation, t355.dxf.text
VENT = (-0.2, 2.2, -3.9, -1.65)
def en_axo(e):
    b = bbox.extents([e], fast=True)
    return b.has_data and VENT[0] < b.extmin.x and b.extmax.x < VENT[1] and VENT[2] < b.extmin.y and b.extmax.y < VENT[3]
axo = [e for e in msp if en_axo(e)]
numeros = [e for e in axo if e.dxf.layer == "A-NUMEROS" and e.dxf.handle not in viejos]
assert len(numeros) == 20, len(numeros)                        # 5 números: directriz, punto, círculo y cifra
contenido_viejo = [e for e in axo if e.dxf.handle not in viejos and e.dxf.layer != "A-NUMEROS"]
polis = []
for e in contenido_viejo:
    if e.dxftype() == "HATCH" and e.dxf.layer == "A-AXO-COLOR":
        for p in ezpath.from_hatch(e):
            pts = [(v.x, v.y) for v in p.flattening(0.0005)]
            if len(pts) >= 3:
                g = Polygon(pts).buffer(0)
                if g.area > 1e-8:
                    polis.append(g)
panel = unary_union(polis)
print(f"contorno del panel, placa y tejas: {len(polis)} manchas, {panel.area:.3f} m²")
for h in viejos:
    msp.delete_entity(E[h])
antes = {e.dxf.handle for e in msp}

# ------------------------------------------------ caras visibles
def partes(g):
    return [p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and p.area > 2e-7]
pares_full = []
vis_par = []
for X0, X1 in PARES:
    for tipo, f in caras_par(X0, X1):
        pf = Polygon(f); pares_full.append(pf)
        vis_par.append((tipo, pf.difference(panel)))
ocl_par = unary_union(pares_full)
vis_dur = [(tipo, Polygon(f).difference(panel).difference(ocl_par), col) for tipo, f, col in caras_dur]

def dibuja(g, rgb, capa_lin, rgb_lin=None):
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
for tipo, g, col in vis_dur:
    dibuja(g, col, "A-AXO-VERDE", VERDE)
corte = Polygon(caras_dur[2][1])
for a, b in ((0, 2), (1, 3)):                      # aspa: el durmiente está cortado
    l = LineString([caras_dur[2][1][a], caras_dur[2][1][b]]).intersection(vis_dur[2][1].buffer(1e-6))
    for s in getattr(l, "geoms", [l]):
        if s.length > 1e-4:
            msp.add_lwpolyline(list(s.coords), dxfattribs={"layer": "A-AXO-VERDE", "true_color": tc(VERDE)})
for tipo, g in vis_par:
    dibuja(g, COL_PAR[tipo], "A-AXO-LIN")
area_dur = sum(g.area for _, g, _ in vis_dur); area_par = sum(g.area for _, g in vis_par)
print(f"visible: durmiente {area_dur:.4f} m², pares {area_par:.4f} m² (en proyección)")

# ------------------------------------------------ ventana: que quepa todo, con el canto superior derecho donde estaba
vp = E["3BF"]
k0 = vp.dxf.height / vp.dxf.view_height                       # mm de papel por m
Pc = (vp.dxf.center.x, vp.dxf.center.y); Mc0 = (vp.dxf.view_center_point.x, vp.dxf.view_center_point.y)
nuevos = [e for e in msp if e.dxf.handle not in antes]
caja = bbox.extents(contenido_viejo + nuevos)
Y_C, Z_C = YF1 - 0.11, ZT(YF1)                                # la cota, delante de las testas de los pares, entre ejes
cota = [P(-0.07, Y_C, Z_C), P(1.13, Y_C, Z_C)]
refs = [[P(xe, YF1 - 0.02, Z_C), P(xe, Y_C - 0.03, Z_C)] for xe in (-0.07, 1.13)]
xl, xr = min(caja.extmin.x, cota[0][0] - 0.04), caja.extmax.x
yb, yt = caja.extmin.y, caja.extmax.y
papel = lambda m, k, mc: (Pc[0] + (m[0] - mc[0]) * k, Pc[1] + (m[1] - mc[1]) * k)
pr = papel((xr, yt), k0, Mc0)
izq, abajo = Pc[0] - vp.dxf.width / 2 + 1.5, Pc[1] - vp.dxf.height / 2 + 1.5
k = min(k0, (pr[0] - izq) / (xr - xl), (pr[1] - abajo) / (yt - yb))
Mc = (xr - (pr[0] - Pc[0]) / k, yt - (pr[1] - Pc[1]) / k)
vp.dxf.view_height = vp.dxf.height / k
vp.dxf.view_center_point = (Mc[0], Mc[1], 0)
s = k0 / k
print(f"escala de la axo: 1:{1000 / k:.1f} (antes 1:{1000 / k0:.1f}); números y textos × {s:.3f} para que midan lo mismo en papel")
T = lambda m: (Mc[0] + (m[0] - Mc0[0]) * s, Mc[1] + (m[1] - Mc0[1]) * s)   # mismo sitio en el papel

# ------------------------------------------------ cota «1,20 m máx.» delante de las testas
for r in refs:
    msp.add_lwpolyline(r, dxfattribs=refer_attr)
msp.add_lwpolyline(cota, dxfattribs=cota_attr)
tick = (0.0579 * s, 0.0156 * s)
for q in cota:
    msp.add_lwpolyline([(q[0] - tick[0] / 2, q[1] - tick[1] / 2), (q[0] + tick[0] / 2, q[1] + tick[1] / 2)], dxfattribs=marca_attr)
h_txt = H_TXT0 * s
mid = ((cota[0][0] + cota[1][0]) / 2, (cota[0][1] + cota[1][1]) / 2)
nrm = (-0.5, -C)                                                # perpendicular a la cota, hacia abajo
off = 0.0825 * s + h_txt / 2
t = msp.add_text(TEXTO, height=h_txt, rotation=ROT_TXT, dxfattribs=txt_attr)
t.set_placement((mid[0] + nrm[0] * off, mid[1] + nrm[1] * off), align=TextEntityAlignment.MIDDLE_CENTER)

# ------------------------------------------------ números: mismo tamaño y sitio en papel; directrices encima de todo
punto_1 = P(0.55, YD0, (ZD0 + ZD1) / 2)                         # el 1, al frente del durmiente
assert Point(punto_1).within(vis_dur[1][1]), "el punto del 1 no se ve"
punto_2 = (1.9296, -2.9055)
assert Point(punto_2).within(unary_union([g for tipo, g in vis_par]).buffer(1e-4)), "el punto del 2 no se ve"
def centro_arco(h):
    for p in h.paths:
        for ed in getattr(p, "edges", []):
            if getattr(ed, "EDGE_TYPE", "") == "ArcEdge":
                return (ed.center[0], ed.center[1]), ed.radius
    raise ValueError(f"círculo sin arco: {h.dxf.handle}")
for e in numeros:
    c = e.copy()
    if e.dxftype() == "LWPOLYLINE":
        pts = [(x, y) for x, y in e.get_points("xy")]
        nuevo = pts[:1] + [T(q) for q in pts[1:]]
        if math.dist(pts[0], (0.9262, -3.3967)) < 1e-3:
            nuevo[0] = punto_1
        c.set_points(nuevo, format="xy")
    elif e.dxftype() == "HATCH":
        cen, r = centro_arco(e)
        if r < 0.02:                                            # punto de la directriz: sobre el elemento
            dst = punto_1 if math.dist(cen, (0.9262, -3.3967)) < 2e-3 else cen
            c.translate(-cen[0], -cen[1], 0); c.scale_uniform(s); c.translate(dst[0], dst[1], 0)
        else:                                                   # círculo del número
            dst = T(cen)
            c.translate(-cen[0], -cen[1], 0); c.scale_uniform(s); c.translate(dst[0], dst[1], 0)
    elif e.dxftype() == "TEXT":
        ref = e.dxf.align_point if e.dxf.hasattr("align_point") and (e.dxf.get("halign", 0) or e.dxf.get("valign", 0)) else e.dxf.insert
        dst = T((ref[0], ref[1]))
        c.translate(-ref[0], -ref[1], 0); c.scale_uniform(s); c.translate(dst[0], dst[1], 0)
    msp.add_entity(c)
    msp.delete_entity(e)

doc.saveas(SAL)
print(f"contenido de x {xl:.3f} a {xr:.3f}, y {yb:.3f} a {yt:.3f}; ventana ve x {Mc[0] - vp.dxf.width / 2 / k:.3f} a "
      f"{Mc[0] + vp.dxf.width / 2 / k:.3f}, y {Mc[1] - vp.dxf.view_height / 2:.3f} a {Mc[1] + vp.dxf.view_height / 2:.3f}")
