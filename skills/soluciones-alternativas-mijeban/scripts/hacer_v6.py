"""Crea ficha03_v6.py a partir de ficha03_v5.py (cambios pedidos el 2026-11-09 sobre la v5):
durmiente de 150 × 200 a haces con el tosco por dentro; el ladrillo verde enrasado con el durmiente; banda impermeable
que protege la madera; el Onduline sin onda (la sección es paralela a las ondas)."""
import io
src = io.open("ficha03_v5.py", encoding="utf-8").read()
R = []
def rep(a, b):
    global src
    assert src.count(a) == 1, ("no encontrado o repetido", a[:80], src.count(a))
    src = src.replace(a, b)

rep('"""Ficha 03 v5 ·', '"""Ficha 03 v6 · (v5 + durmiente 150 × 200, ladrillo enrasado, banda impermeable y Onduline sin onda) ·')
rep("XU, XT, XZ1 = 0.121, 0.131, 0.248      # cara interior del peto, testa de panel y par, cara interior del tosco",
    "XU, XT, XZ1 = 0.098, 0.108, 0.248      # cara interior del peto (= cara exterior del durmiente), testa de panel y par, cara interior del tosco\n"
    "XD0, XD1, YD0 = 0.098, 0.248, -0.200   # durmiente 150 × 200, a haces con el tosco por dentro")
rep("SEAT = 0.010                           # placa de acero", "SEAT = 0.0                             # el par apoya en el durmiente")
# ---- muro con el durmiente embebido
rep("""tosco = [(0.015, YC), (XZ1, YC), (XZ1, 0.0), (0.015, 0.0)]
trama(tosco, "ANSI31", 0.006, (175, 175, 175))
poly([(0.015, 0.0), (0.015, YC)], "A-WALL"); poly([(XZ1, YC), (XZ1, 0.0), (XU, 0.0)], "A-WALL")""",
"""tosco = [(0.015, YC), (XZ1, YC), (XZ1, YD0), (XD0, YD0), (XD0, 0.0), (0.015, 0.0)]
trama(tosco, "ANSI31", 0.006, (175, 175, 175))
poly([(0.015, 0.0), (0.015, YC)], "A-WALL"); poly([(XZ1, YC), (XZ1, YD0)], "A-WALL")
dur = [(XD0, YD0), (XD1, YD0), (XD1, 0.0), (XD0, 0.0)]
solido(dur, (214, 229, 224)); poly(dur, "A-WALL", VERDE, cerrada=True)
poly([(XD0, YD0), (XD1, 0.0)], "A-DETL-THIN", VERDE); poly([(XD1, YD0), (XD0, 0.0)], "A-DETL-THIN", VERDE)""")
# ---- sin placa ni pernos
rep("""solido([(XT, 0.0), (XZ1, 0.0), (XZ1, SEAT), (XT, SEAT)], GRIS_OSC)
for xa in (0.165, 0.215):
    poly([(xa, 0.0), (xa, -0.10)], "A-DETL", GRIS_OSC, lw=25)
""", "")
# ---- banda impermeable: bajo el durmiente y contra el ladrillo, hasta el panel
rep("""junta = [(XU, yb(XT)), (XT, yb(XT)), (XT, yt(XT)), (XU, yt(XU))]""",
"""BANDA = [(XD1, YD0 - 0.002), (XD0 - 0.002, YD0 - 0.002), (XD0 - 0.002, yb(XT))]
poly(BANDA, "A-WALL", VERDE, lw=50)
junta = [(XU, yb(XT)), (XT, yb(XT)), (XT, yt(XT)), (XU, yt(XU))]""")
# ---- Onduline sin onda: chapa (en el valle) y cresta vista detrás
rep("""onda = []
x = X_OND
while x <= XR + 1e-9:
    s_ = (x - X_OND) * CV
    onda.append((x, y_o(x) + AMP * 0.5 * (1 - math.cos(2 * math.pi * s_ / PASO))))
    x += 0.002
poly(onda, "A-WALL", (60, 60, 60), lw=30)
poly([(X_OND, y_o(X_OND)), (XR, y_o(XR))], "A-DETL-THIN", (150, 150, 150))                      # línea de apoyo de la placa""",
"""chapa = [(X_OND, y_o(X_OND)), (XR, y_o(XR)), (XR, y_o(XR) + 0.004), (X_OND, y_o(X_OND) + 0.004)]
solido(chapa, (70, 70, 70)); poly(chapa, "A-WALL-CAPAS", (40, 40, 40), cerrada=True)              # placa cortada en el valle
poly([(X_OND, y_o(X_OND) + AMP), (XR, y_o(XR) + AMP)], "A-DETL-THIN", (110, 110, 110))           # cresta, vista detrás
poly([(X_OND, y_o(X_OND) + 0.004), (X_OND, y_o(X_OND) + AMP)], "A-DETL-THIN", (110, 110, 110))""")
# ---- textos y números de la sección
rep('texto("EXTERIOR", (-0.660, -0.080), 0.036, (110, 110, 110))', 'texto("EXTERIOR", (-0.660, -0.170), 0.036, (110, 110, 110))')
rep('texto("FACHADA B (FICHA 02)", (-0.660, -0.125), 0.030, (140, 140, 140))', 'texto("FACHADA B (FICHA 02)", (-0.660, -0.215), 0.030, (140, 140, 140))')
rep("""numero(4, (XD, 0.040), (XT - 0.005, yb(XT) + 0.050))
numero(7, (XI, 0.230), (XGF, 0.260))
numero(1, (XI, 0.080), (0.068, 0.120))""",
"""numero(7, (XI, 0.240), (XGF, 0.260))
numero(4, (XI, 0.095), (0.056, 0.110))
numero(1, (XI, -0.050), ((XD0 + XD1) / 2, YD0 / 2))""")
# ---- axonometría: durmiente verde bajo los pares (como la v4) y ladrillo delante entre los pares (abajo gris, peto verde)
rep("DXA, DZA = 0.110, -0.0263                            # Y = x_sección + DXA ; Z = y_sección + DZA",
    "Y_PANEL = 0.241                                      # cara delantera del panel en la axo (abajo)\n"
    "DXA = Y_PANEL - XT; DZA = ZT(Y_PANEL) - yb(XT)       # Y = x_sección + DXA ; Z = y_sección + DZA")
A0 = src.index("# piezas 3D")
A1 = src.index("# 5 · cota «1,20 m máx.»")
src = src[:A0] + '''# piezas 3D
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

''' + src[A1:]
rep("""Y_C, Z_C = YW0 - 0.240, Z_(SEAT)
xe = [(X0 + X1) / 2 for X0, X1 in PARES]
for x_ in xe:
    msp.add_lwpolyline([P(x_, YPE - 0.02, Z_C), P(x_, Y_C - 0.03, Z_C)], dxfattribs=REF_ATTR)""",
"""Y_C, Z_C = YW0 - 0.120, ZD0
xe = [(X0 + X1) / 2 for X0, X1 in PARES]
for x_ in xe:
    msp.add_lwpolyline([P(x_, YD_0 - 0.01, Z_C), P(x_, Y_C - 0.03, Z_C)], dxfattribs=REF_ATTR)""")
rep("""# 6 · números: el 1 al peto; el 7, nuevo, al canalón (copia del 1)
punto_1 = P(0.45, YW0, Z_(0.15))
assert Point(punto_1).within(cara(peto_front).difference(gut_sil)), "el punto del 1 no se ve"
""", """# 6 · números: el 1 al durmiente; el 4, nuevo, al peto (copia del 1)
punto_1 = P(1.02, YD_0, (ZD0 + ZD1) / 2)
punto_4 = P(0.45, YW0, Z_(0.20))
assert Point(punto_4).within(cara(peto_front)), "el punto del 4 no se ve"
""")
rep("""pts = [(x, y) for x, y in lead1.get_points("xy")]

pts[0] = punto_1""", """pts = [(x, y) for x, y in lead1.get_points("xy")]
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
pts[0] = punto_1""")
# ---- textos de la hoja
rep('''cambia("3BE", "El panel sándwich del proyecto, con friso de abeto visto, sobre cerchas a 1,20 m como máximo y sin "
              "durmiente. El ladrillo sube y recoge el panel; canalón visto. Placa ventilada y teja sin mortero.")''',
'''cambia("3BE", "El panel sándwich del proyecto, con friso de abeto visto, sobre cerchas a 1,20 m como máximo apoyadas "
              "en un durmiente. El ladrillo sube y recoge el panel; canalón visto. Placa ventilada y teja sin mortero.")''')
rep('cambia("3C2", "Peto de ladrillo tosco que sube y recoge el panel")', 'cambia("3C2", "Durmiente de madera de canto con banda impermeable")')
rep('cambia("3C3", "a soga, de 10,6 cm")', 'cambia("3C3", "150 × 200 mm, a calcular")')
rep('cambia("3CB", "Junta de espuma contra el ladrillo y cinta estanca")', 'cambia("3CB", "Peto de ladrillo enrasado con el durmiente")')
rep('cambia("3AB", "Sin empuje al muro ni durmiente")', 'cambia("3AB", "Sin empuje al muro")')
rep('cambia("3B1", "Cerchas y apoyo en el muro,\\\\Ppendientes del cálculo\\\\Pestructural y de la DF.")',
    'cambia("3B1", "Cerchas y durmiente,\\\\Ppendientes del cálculo\\\\Pestructural y de la DF.")')
rep('cambia("3E6", "Sin viga de hormigón ni durmiente: la cercha apoya en el tosco.")', 'cambia("3E6", "Durmiente de madera en lugar de viga de hormigón.")')
rep('cambia("3F0", "Junta de espuma y cinta estanca.")', 'cambia("3F0", "Banda impermeable contra la madera; junta y cinta estanca.", 2)')
rep('pie.text = pie.text.replace("· v4 ·", "· v5 ·")', 'pie.text = pie.text.replace("· v4 ·", "· v6 ·")')
io.open("ficha03_v6.py", "w", encoding="utf-8").write(src)
print("ficha03_v6.py escrito")
