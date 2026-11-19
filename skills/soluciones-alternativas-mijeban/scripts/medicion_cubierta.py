"""Medición de la cubierta inclinada de la ficha 03 (v4) desde los DWG del proyecto. Sin la estructura de madera.

Fuentes: planta de cubierta A-03 (DWG «PLANTAS ALZADOS Y SECCIONES», bloque 0_TEJA), DET-01 y ficha 03 v4.
E-07 (DWG «Planos de estructura») solo se usa para comprobar los largos de A-03.
Genera las líneas de medición (lineas.json) y el PDF de comprobación A3. El BC3 conjunto lo escribe bc3_conjunto.py.
Decisiones del usuario (06/11/2026): partidas agrupadas (4); la estructura de madera, completamente fuera.
"""
import sys, json, math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

PLANTA, E07, SAL = sys.argv[1], sys.argv[2], Path(sys.argv[3]); SAL.mkdir(exist_ok=True)
for f in (r"C:\Windows\Fonts\GOTHIC.TTF", r"C:\Windows\Fonts\GOTHICB.TTF"):
    fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Century Gothic"
VERDE = (7/255, 87/255, 72/255); NARANJA = (0.85, 0.50, 0.15)
r2 = lambda x: round(x + 1e-9, 2)
fmt = lambda x, d=2: f"{x:,.{d}f}".replace(",", " ").replace(".", ",")

M = 0.268                         # pendiente (DET-01 y ficha 03)
K = math.sqrt(1 + M * M)          # de planta a verdadera magnitud
MEDIO = 3.70                      # media crujía: 7,40 entre fachadas, cumbrera centrada
LABIO = 0.562                     # labio del cajón de composite, desde la fachada (DET-01)
VUELO_H = 0.50                    # vuelo sobre los hastiales
DESC_E07 = 0.40                   # largo del volumen − separación entre los pares extremos de E-07
X0, Y0 = 421600, 4412000

# ---------------------------------------------------------------- geometría de A-03
O = json.load(open(PLANTA, encoding="utf-8"))
H, V = [], []
for o in O:
    if "pts" not in o or not o["capa"].startswith("0_TEJA|0_FIN"):
        continue
    p = o["pts"]
    for (x1, y1), (x2, y2) in zip(p, p[1:]):
        x1 -= X0; x2 -= X0; y1 -= Y0; y2 -= Y0
        if abs(y1 - y2) < 0.005 and abs(x1 - x2) > 0.5:
            H.append((round(y1, 3), min(x1, x2), max(x1, x2)))
        if abs(x1 - x2) < 0.005 and abs(y1 - y2) > 0.5:
            V.append((round(x1, 3), min(y1, y2), max(y1, y2)))

VOLS = [  # código, nombre, caja de búsqueda en A-03, lado del alero exterior
    ("D",  "Volumen D (dormitorio 4)",             (45, 53, 303, 315), "ambos"),
    ("N1", "Fila norte, oeste",                    (53.5, 62, 308.9, 318), "norte"),
    ("N2", "Fila norte, centro",                   (62.5, 75, 308.9, 318), "norte"),
    ("N3", "Fila norte, este (servicio y porche)", (75.5, 96, 308.9, 318), "norte"),
    ("S1", "Fila sur, oeste (dormitorios 2 y 3)",  (53, 65.5, 299.5, 308.7), "sur"),
    ("S2", "Fila sur, centro (dormitorio 1 y estudio)", (65.6, 78.5, 299.5, 308.7), "sur"),
    ("S3", "Fila sur, este (salón)",               (78.6, 96, 299.5, 308.7), "sur"),
]

def cobertura(y, a, b):
    tramos = sorted((max(x1, a), min(x2, b)) for yy, x1, x2 in H if yy == y and x2 > a and x1 < b)
    tot, fin = 0.0, a
    for s0, s1 in tramos:
        s0 = max(s0, fin)
        if s1 > s0:
            tot += s1 - s0; fin = s1
    return tot / (b - a)

GEO = {}
for cod, nom, (a, b, c, d), ext in VOLS:
    xs = sorted({x for x, y1, y2 in V if a <= x <= b and c - 0.3 <= y1 and y2 <= d + 0.3 and y2 - y1 > 8.3})
    assert len(xs) >= 2, (cod, xs)
    x0, x1 = xs[0], xs[-1]
    ys = sorted({y for y, s0, s1 in H if c <= y <= d and cobertura(y, x0, x1) > 0.97}, reverse=True)
    assert len(ys) == (6 if ext == "ambos" else 5), (cod, ys)
    if ext == "norte":
        borde_ext, teja_ext, ra, rb, borde_in = ys
    elif ext == "sur":
        borde_in, ra, rb, teja_ext, borde_ext = ys
    else:
        borde_ext, teja_ext, ra, rb, teja_s, borde_s = ys
    rc = (ra + rb) / 2
    g = dict(cod=cod, nom=nom, ext=ext, x0=x0, x1=x1, L=r2(x1 - x0), ys=ys, rc=rc, franja=r2(ra - rb))
    g["ext_planta"] = abs(teja_ext - rc)
    g["alero"] = abs(borde_ext - rc) - MEDIO
    if ext == "ambos":
        g["ext2_planta"] = abs(teja_s - rc); g["alero2"] = abs(borde_s - rc) - MEDIO
    else:
        g["in_planta"] = abs(borde_in - rc); g["vuelo_in"] = abs(borde_in - rc) - MEDIO
    g["Lv"] = r2(g["L"] - 2 * VUELO_H)
    GEO[cod] = g

# largos entre pares extremos de E-07, solo para comprobar los largos de A-03
E = json.load(open(E07))
def grupos(fila):
    out, cur = [], []
    for x, m in fila:
        if abs(m - 3.40) < 0.01:
            out.append(cur); cur = []
        else:
            cur.append(m)
    out.append(cur)
    return out
CAD = dict(zip(("N1", "N2", "N3"), grupos(E["309"])))
CAD.update(zip(("S1", "S2", "S3"), grupos(E["292"])))
CAD["D"] = grupos(E["305"])[0]

ERR = []
for cod, g in GEO.items():
    if abs(g["franja"] - 0.24) > 0.005: ERR.append(f"{cod}: franja de cumbrera {g['franja']}")
    if abs(g["alero"] - LABIO) > 0.005: ERR.append(f"{cod}: alero exterior {g['alero']:.3f} ≠ labio de DET-01 {LABIO}")
    if g["ext"] == "ambos" and abs(g["alero2"] - LABIO) > 0.005: ERR.append(f"{cod}: alero sur {g['alero2']:.3f}")
    if abs(r2(sum(CAD[cod]) + DESC_E07) - g["Lv"]) > 0.005: ERR.append(f"{cod}: E-07 {sum(CAD[cod]) + DESC_E07:.2f} ≠ A-03 {g['Lv']:.2f}")
assert not ERR, "\n".join(ERR)

# ---------------------------------------------------------------- partidas y líneas
PARTIDAS = {
 "CUB01": ("m2", "Cubierta inclinada completa (ficha 03)",
  "Cubierta inclinada de la ficha 03, de dentro a fuera: panel sándwich Thermochip TAH 10-200-19 o similar (friso de abeto "
  "de 10 mm con lasur de fábrica, núcleo de poliestireno extruido de 200 mm y tablero aglomerado hidrófugo de 19 mm), "
  "machihembrado, con las juntas sobre los pares y selladas con cinta autoadhesiva, fijado a los pares con tornillos "
  "autorroscantes; placa bajo teja Onduline DRS BT-150 Plus o similar, fijada en cresta con tornillo VLS (6 fijaciones/m2 "
  "como mínimo), ventilada de alero a cumbrera, con peine de alero; teja cerámica curva, canales nuevas y cobijas de "
  "recuperación, fijadas a la placa con espuma de poliuretano, sin mortero. Incluso relleno de aislamiento entre pares "
  "sobre el muro, hasta la cara inferior del panel, y banda de estanqueidad al aire entre el panel y la cara interior del "
  "muro en todo el encuentro (aleros y hastiales). Pendiente 27 %. No incluye la estructura de madera. Medida en "
  "verdadera magnitud sobre la planta de cubierta A-03, de la cumbrera al borde de la teja, con los vuelos de alero y de "
  "hastial."),
 "CUB02": ("m", "Cumbrera en seco y ventilada",
  "Cumbrera en seco y ventilada según el manual Onduline Bajo Teja (2.4.2): listón de madera sobre pieza de apoyo en seco, "
  "banda impermeable transpirable Ondulair o similar a los dos lados y caballete cerámico curvo atornillado, con salida del "
  "aire de la cámara bajo teja. Sustituye a la cumbrera recibida con mortero y a las 42 piezas de ventilación del proyecto. "
  "Medida en su longitud, con los vuelos de hastial."),
 "CUB03": ("m", "Alero de composite con canalón oculto (DET-01)",
  "Alero en cajón de composite con frente inclinado y canalón oculto de aluminio en su interior, con babero sobre el panel, "
  "piezas de conexión a bajantes, tapas, esquinas y soportes, según el detalle DET-01 del proyecto. Medido en los aleros "
  "exteriores, en la longitud de la cubierta, con los vuelos de hastial. Las bajantes siguen como en el proyecto (07.04)."),
 "CUB04": ("m", "Remates de chapa en los bordes de los faldones",
  "Remate de chapa de aluminio lacado en los bordes de los faldones: en los bordes laterales, sobre el vuelo de 0,50 m de los "
  "hastiales, cubriendo el canto de todo el paquete de cubierta; y en el frente de los faldones que vierten a las cubiertas "
  "planas en valle, cubriendo el canto del panel y de la placa, con goterón y peine antipájaros. Con piezas especiales, "
  "fijado a la cubierta. El frente al valle no está dibujado en el proyecto ni medido en la licitación: su detalle lo define "
  "la dirección facultativa. Medido en verdadera magnitud en los bordes laterales y en la longitud de la cubierta en el "
  "frente al valle."),
}
LIN = {c: [] for c in PARTIDAS}
def L(cod, com, uds, lon=None, lat=None, alt=None):
    LIN[cod].append((com, uds, None if lon is None else r2(lon), None if lat is None else r2(lat), None if alt is None else r2(alt)))

LADO_IN = {"norte": "sur", "sur": "norte"}
for cod in ("D", "N1", "N2", "N3", "S1", "S2", "S3"):
    g = GEO[cod]
    ext_t = g["ext_planta"] * K
    if g["ext"] == "ambos":
        L("CUB01", f"{cod} · faldón norte, alero exterior (planta {g['ext_planta']:.3f} × {K:.4f})", 1, g["L"], ext_t)
        L("CUB01", f"{cod} · faldón sur, alero exterior (planta {g['ext2_planta']:.3f} × {K:.4f})", 1, g["L"], g["ext2_planta"] * K)
        L("CUB02", f"{cod} · cumbrera", 1, g["L"])
        L("CUB03", f"{cod} · aleros norte y sur", 2, g["L"])
        L("CUB04", f"{cod} · bordes laterales en hastiales, 4 bordes", 4, ext_t)
        continue
    le, li = g["ext"], LADO_IN[g["ext"]]
    in_t = g["in_planta"] * K
    L("CUB01", f"{cod} · faldón {le}, alero exterior (planta {g['ext_planta']:.3f} × {K:.4f})", 1, g["L"], ext_t)
    L("CUB01", f"{cod} · faldón {li}, al valle (planta {g['in_planta']:.3f} × {K:.4f})", 1, g["L"], in_t)
    L("CUB02", f"{cod} · cumbrera", 1, g["L"])
    L("CUB03", f"{cod} · alero {le}", 1, g["L"])
    L("CUB04", f"{cod} · frente del alero {li}, al valle", 1, g["L"])
    L("CUB04", f"{cod} · bordes laterales en hastiales, faldón {le}", 2, ext_t)
    L("CUB04", f"{cod} · bordes laterales en hastiales, faldón {li}", 2, in_t)

parcial = lambda ln: ln[1] * (ln[2] if ln[2] is not None else 1) * (ln[3] if ln[3] is not None else 1) * (ln[4] if ln[4] is not None else 1)
TOTAL = {c: r2(sum(parcial(ln) for ln in LIN[c])) for c in LIN}
FRENTE = r2(sum(parcial(ln) for ln in LIN["CUB04"] if "frente" in ln[0]))
LATERAL = r2(TOTAL["CUB04"] - FRENTE)

# ---------------------------------------------------------------- comprobación de las líneas
def verificar():
    err = []
    for c, ls in LIN.items():
        vistos = set()
        for ln in ls:
            if parcial(ln) <= 0: err.append(f"{c}: línea a cero «{ln[0]}»")
            if ln in vistos: err.append(f"{c}: línea repetida «{ln[0]}»")
            vistos.add(ln)
            if len(ln[0]) > 110: err.append(f"{c}: comentario largo «{ln[0]}»")
    # superficie de cada volumen recalculada con el polígono del campo de teja de A-03
    for cod, g in GEO.items():
        ys = g["ys"]
        prof = ys[0] - ys[3] if g["ext"] == "sur" else ys[1] - ys[4]
        area = (g["x1"] - g["x0"]) * prof * K
        suma = sum(parcial(ln) for ln in LIN["CUB01"] if ln[0].startswith(cod + " ·"))
        tol = 2 * 0.005 * (g["x1"] - g["x0"])                    # cada anchura va redondeada al cm en su línea
        if abs(area - suma) > tol: err.append(f"CUB01 {cod}: líneas {suma:.2f} frente a polígono {area:.2f}")
    # longitudes de borde: cumbrera = suma de largos; alero exterior = largos (D dos veces); frente al valle = largos sin D
    largos = {cod: g["L"] for cod, g in GEO.items()}
    if abs(TOTAL["CUB02"] - sum(largos.values())) > 0.005: err.append("cumbrera ≠ suma de largos")
    if abs(TOTAL["CUB03"] - (sum(largos.values()) + largos["D"])) > 0.005: err.append("alero exterior ≠ largos + D")
    if abs(FRENTE - (sum(largos.values()) - largos["D"])) > 0.005: err.append("frente al valle ≠ largos sin D")
    n_bordes = sum(ln[1] for ln in LIN["CUB04"] if "laterales" in ln[0])
    if n_bordes != 4 * len(GEO): err.append(f"bordes laterales: {n_bordes} en lugar de {4 * len(GEO)}")
    for c, ls in LIN.items():
        if abs(r2(sum(parcial(ln) for ln in ls)) - TOTAL[c]) > 0.005: err.append(f"{c}: suma")
    return err
ERR = verificar()
assert not ERR, "\n".join(ERR)
n_lin = sum(len(v) for v in LIN.values())
print(f"comprobación: {n_lin} líneas; alero de A-03 = DET-01; largos de A-03 = E-07: OK")
for c in PARTIDAS:
    print(f"  {c} {PARTIDAS[c][0]:3s} {TOTAL[c]:9.2f}  {PARTIDAS[c][1]}  ({len(LIN[c])} líneas)")
print(f"  CUB04 = frente al valle {FRENTE:.2f} + bordes laterales {LATERAL:.2f}")

# ---------------------------------------------------------------- comparación con la licitación
LIC_AREA = 644.00
COMP = [("Panel y teja (07.06 y 07.07)", "644,00 m²", f"{fmt(TOTAL['CUB01'])} m²"),
        ("Cumbrera (07.08)", "28,98 m", f"{fmt(TOTAL['CUB02'])} m"),
        ("Piezas de ventilación (07.11)", "42 ud", "no hacen falta"),
        ("Remates del alero exterior (07.03 y 07.10)", "68,50 + 84,10 m", f"{fmt(TOTAL['CUB03'])} m"),
        ("Bordes laterales (07.05 y 07.09)", "112,56 + 112,56 m", f"{fmt(LATERAL)} m"),
        ("Frente del alero al valle", "sin medir", f"{fmt(FRENTE)} m"),
        ("Remates de chapa (CUB04 = las dos filas anteriores)", "", f"{fmt(TOTAL['CUB04'])} m")]

# ---------------------------------------------------------------- PDF
FILAS_PDF = []
def cabecera(fig, titulo, sub):
    fig.text(0.03, 0.965, titulo, fontsize=17, fontweight="bold", color=VERDE, va="top")
    fig.text(0.03, 0.932, sub, fontsize=9.5, color="0.25", va="top")
    fig.text(0.97, 0.965, "MIJEBAN · SOLUCIONES ALTERNATIVAS", fontsize=8, color=VERDE, ha="right", va="top", fontweight="bold")
    fig.text(0.97, 0.945, "Vivienda Cigarral Montealegre · cubierta inclinada, ficha 03", fontsize=8, color="0.4", ha="right", va="top")
def pie(fig, n):
    fig.text(0.03, 0.02, "Fuentes: planta de cubierta A-03 (DWG «PLANTAS ALZADOS Y SECCIONES»), DET-01 y ficha 03 v4; cotas de E-07 para comprobar; "
             "licitación de 15/06/2026 (cap. 07). Cotas en m. Medición propuesta, sin aprobar.", fontsize=7.5, color="0.45")
    fig.text(0.97, 0.02, f"{n}", fontsize=8, color="0.45", ha="right")
U = lambda ud: ud.replace("2", "²").replace("3", "³")

A3 = (16.54, 11.69)
ruta_pdf = SAL / "MEDICION CUBIERTA INCLINADA.pdf"
for viejo in SAL.glob("c*.png"):
    viejo.unlink()
with PdfPages(ruta_pdf) as pp:
    # 1 · resumen
    fig = plt.figure(figsize=A3)
    cabecera(fig, "Medición de la cubierta inclinada · ficha 03", "Resumen, criterios y comparación con la licitación")
    y = 0.86
    for c, (ud, res, _) in PARTIDAS.items():
        fig.text(0.03, y, c, fontsize=12, fontweight="bold", color=VERDE)
        fig.text(0.10, y, res, fontsize=12, color="0.1")
        fig.text(0.56, y, f"{fmt(TOTAL[c])} {U(ud)}", fontsize=14, fontweight="bold", color=VERDE, ha="right")
        y -= 0.045
    fig.text(0.03, y - 0.005, "CUB01 incluye, sin medirlos aparte, el relleno de aislamiento entre pares sobre el muro y la banda de "
             "estanqueidad al aire contra el muro.", fontsize=8.6, color="0.35")
    fig.text(0.03, y - 0.027, f"CUB04 suma los bordes laterales sobre los hastiales ({fmt(LATERAL)} m) y el frente de los faldones "
             f"que vierten al valle ({fmt(FRENTE)} m).", fontsize=8.6, color="0.35")
    crit = ["Planta de cubierta A-03: 7 cubiertas a dos aguas, cumbrera este-oeste, 7,40 m entre fachadas y cumbrera centrada.",
            f"Pendiente 0,268 (27 %): de planta a verdadera magnitud × {K:.4f}.",
            "Superficie: de la cumbrera al borde de la teja dibujado en A-03, con 0,50 m de vuelo en los hastiales;",
            "   alero exterior hasta la teja (0,39 m de la fachada); alero al valle hasta el borde (0,41 m).",
            "Aleros: el borde exterior de A-03 está a 0,562 m de la fachada, el labio del cajón de DET-01.",
            "Bordes laterales en verdadera magnitud; cumbrera, alero y frente al valle en la longitud de cada cubierta.",
            "Fuera de esta medición: la estructura de madera, y las bajantes (07.04) y chimeneas (07.12), iguales que en el proyecto."]
    fig.text(0.03, 0.58, "CRITERIOS", fontsize=10, fontweight="bold", color=VERDE)
    for k, c in enumerate(crit):
        fig.text(0.03, 0.553 - k * 0.027, ("" if c.startswith("   ") else "■  ") + c, fontsize=8.8, color="0.15")
    x0 = 0.60
    fig.text(x0, 0.86, "COMPARACIÓN CON LA LICITACIÓN", fontsize=10, fontweight="bold", color=VERDE)
    yy = 0.83
    fig.text(x0 + 0.235, yy, "Licitación", fontsize=8.8, ha="right", fontweight="bold")
    fig.text(0.97, yy, "Esta medición", fontsize=8.8, ha="right", fontweight="bold")
    yy -= 0.028
    for i, (a, b, c) in enumerate(COMP):
        w = "bold" if i == len(COMP) - 1 else "normal"
        fig.text(x0, yy, a, fontsize=8.6, fontweight=w); fig.text(x0 + 0.235, yy, b, fontsize=8.6, ha="right")
        fig.text(0.97, yy, c, fontsize=8.6, ha="right", color=VERDE, fontweight=w); yy -= 0.026
    dif = [f"Superficie: +{TOTAL['CUB01'] - LIC_AREA:.0f} m² porque la licitación da al volumen D 4,25 m de largo (A-03: 5,50) y para el",
           "   faldón al valle a 3,90 m de la cumbrera, sin el vuelo de 0,41 m que dibuja A-03.",
           "Cumbrera: la licitación mide 7 largos de faldón (7 × 4,14 m), no la cumbrera.",
           "Remates: la licitación mide dos veces el borde lateral (07.05 y 07.09) y pone dos remates en el alero exterior."]
    for k, c in enumerate(dif):
        fig.text(x0, yy - 0.012 - k * 0.024, ("" if c.startswith("   ") else "■  ") + c, fontsize=8.0, color="0.3")
    fig.text(0.03, 0.30, "COMPROBACIÓN DE LAS LÍNEAS DE MEDICIÓN", fontsize=10, fontweight="bold", color=VERDE)
    comp_l = [f"{n_lin} líneas, todas calculadas con las coordenadas de A-03; uds × medidas = parcial; sin líneas repetidas ni a cero.",
              "La superficie de cada volumen coincide con su polígono de teja de A-03 (salvo el redondeo de cada anchura al cm).",
              "Cumbrera = suma de largos; alero exterior = largos (D, dos veces); frente al valle = largos sin D; 4 bordes laterales por cubierta.",
              "El alero de A-03 coincide con el de DET-01 (0,562 m) y los largos de A-03, con las cotas de E-07.",
              "Es una comprobación de coherencia con los planos: no sustituye a mirar la planta (página 2) ni las líneas (página 3)."]
    for k, c in enumerate(comp_l):
        fig.text(0.03, 0.275 - k * 0.025, "■  " + c, fontsize=8.5, color="0.15")
    fig.text(x0, 0.30, "LO QUE QUEDA ABIERTO", fontsize=10, fontweight="bold", color=VERDE)
    ab = ["Frente del alero al valle (dentro de CUB04): no está dibujado; su detalle lo define la dirección facultativa.",
          "La estructura de madera (pares, durmiente, uniones y atado) no está en esta medición."]
    for k, c in enumerate(ab):
        fig.text(x0, 0.275 - k * 0.025, "■  " + c, fontsize=8.5, color="0.15")
    pie(fig, 1); pp.savefig(fig); fig.savefig(SAL / "c1.png", dpi=80); plt.close(fig)

    # 2 · planta
    fig = plt.figure(figsize=A3)
    cabecera(fig, "Planta de cubierta A-03 · lo que se mide", "Cubierta, cumbreras, aleros y remates de chapa")
    ax = fig.add_axes([0.03, 0.10, 0.94, 0.80])
    for cod, g in GEO.items():
        ys = g["ys"]; x0g, x1g = g["x0"], g["x1"]
        yo, yi = max(ys), min(ys)
        ax.add_patch(Rectangle((x0g, yi), x1g - x0g, yo - yi, fc="0.93", ec="0.3", lw=0.8, zorder=1))
        if g["ext"] in ("norte", "ambos"):
            ax.add_patch(Rectangle((x0g, ys[1]), x1g - x0g, ys[0] - ys[1], fc="0.45", ec="none", zorder=2))
        if g["ext"] in ("sur", "ambos"):
            ax.add_patch(Rectangle((x0g, ys[-1]), x1g - x0g, ys[-2] - ys[-1], fc="0.45", ec="none", zorder=2))
        if g["ext"] == "norte":
            ax.plot([x0g, x1g], [ys[-1], ys[-1]], color=NARANJA, lw=2.4, zorder=3)
        if g["ext"] == "sur":
            ax.plot([x0g, x1g], [ys[0], ys[0]], color=NARANJA, lw=2.4, zorder=3)
        ya = ys[1] if g["ext"] in ("norte", "ambos") else ys[0]
        yb = ys[-2] if g["ext"] in ("sur", "ambos") else ys[-1]
        for xb in (x0g, x1g):
            ax.plot([xb, xb], [yb, ya], color=NARANJA, lw=2.4, zorder=3)
        ax.plot([x0g, x1g], [g["rc"], g["rc"]], color="k", lw=1.6, zorder=4)
        ax.text((x0g + x1g) / 2, g["rc"] + 1.2, cod, ha="center", fontsize=12, fontweight="bold", color=VERDE, zorder=6,
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
        ax.text((x0g + x1g) / 2, g["rc"] - 1.6, f"{fmt(g['L'])} m de largo", ha="center", fontsize=8.5, color="0.15", zorder=6,
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
    xs = [g["x0"] for g in GEO.values()] + [g["x1"] for g in GEO.values()]
    ax.set_xlim(min(xs) - 1, max(xs) + 1); ax.set_ylim(299, 318.5); ax.set_aspect("equal"); ax.axis("off")
    ley = [("0.93", "Cubierta completa (CUB01), de la cumbrera al borde de la teja"), ("k", "Cumbrera en seco y ventilada (CUB02)"),
           ("0.45", "Alero de composite con canalón (CUB03)"), (NARANJA, "Remates de chapa: bordes laterales y frente al valle (CUB04)")]
    for k, (c, t) in enumerate(ley):
        fig.add_artist(Rectangle((0.03 + (k % 2) * 0.47, 0.065 - (k // 2) * 0.025), 0.018, 0.012, transform=fig.transFigure, fc=c, ec="0.3", lw=0.5))
        fig.text(0.053 + (k % 2) * 0.47, 0.066 - (k // 2) * 0.025, t, fontsize=8.8, color="0.15")
    pie(fig, 2); pp.savefig(fig); fig.savefig(SAL / "c2.png", dpi=80); plt.close(fig)

    # 3 · líneas
    def tabla(fig, rect, cods):
        ax = fig.add_axes(rect); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        xc = (0.0, 0.64, 0.73, 0.81, 0.89, 1.0)
        y = 0.99; dy = 0.0215; fs = 7.6
        for h, x, ha in zip(("Línea", "Uds", "Long.", "Anch.", "Alt.", "Parcial"), xc, ("left",) + ("right",) * 5):
            ax.text(x, y, h, fontsize=fs + 0.6, fontweight="bold", ha=ha, va="top")
        y -= dy * 1.3
        for c in cods:
            ud, res, _ = PARTIDAS[c]
            ax.text(0, y, f"{c} · {res} ({U(ud)})", fontsize=fs + 0.5, fontweight="bold", color=VERDE, va="top")
            y -= dy
            for ln in LIN[c]:
                FILAS_PDF.append((c,) + ln)
                ax.text(0, y, ln[0], fontsize=fs, va="top", color="0.1")
                ax.text(xc[1], y, f"{ln[1]:g}", fontsize=fs, va="top", ha="right")
                for j in (2, 3, 4):
                    if ln[j] is not None:
                        ax.text(xc[j], y, fmt(ln[j]), fontsize=fs, va="top", ha="right")
                ax.text(xc[5], y, fmt(parcial(ln)), fontsize=fs, va="top", ha="right")
                y -= dy
            ax.text(xc[4], y, "Total", fontsize=fs + 0.4, fontweight="bold", ha="right", va="top")
            ax.text(xc[5], y, fmt(TOTAL[c]), fontsize=fs + 0.5, fontweight="bold", ha="right", va="top")
            y -= dy * 1.5
        assert y > 0, ("la tabla no cabe", cods)
    fig = plt.figure(figsize=A3)
    cabecera(fig, "Líneas de medición", "Las mismas que en el BC3 · uds × longitud × anchura × altura = parcial")
    tabla(fig, [0.03, 0.06, 0.45, 0.85], ("CUB01", "CUB02", "CUB03")); tabla(fig, [0.52, 0.06, 0.45, 0.85], ("CUB04",))
    pie(fig, 3); pp.savefig(fig); fig.savefig(SAL / "c3.png", dpi=80); plt.close(fig)

todas = sorted((c,) + ln for c in LIN for ln in LIN[c])
assert sorted(FILAS_PDF) == todas, f"PDF: {len(FILAS_PDF)} filas frente a {len(todas)} líneas"
print("PDF = líneas: OK ·", ruta_pdf)
json.dump({"capitulo": ("CUB#", "CUBIERTA INCLINADA (FICHA 03)"),
           "partidas": {c: list(v) for c, v in PARTIDAS.items()}, "totales": TOTAL,
           "lineas": {c: [list(ln) for ln in v] for c, v in LIN.items()}},
          open(SAL / "lineas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
