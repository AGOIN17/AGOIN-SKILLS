"""Medición de fachadas de la vivienda (alternativa B) desde los DWG del proyecto.

Genera, con los mismos datos: líneas de medición, BC3 sin precios (CP1252, CRLF) y PDF de comprobación A3.
Criterios del usuario (06/11/2026): a cinta corrida; huecos de más de 3 m² descontados; lo que sale en alzado,
una vez por cara; fachadas largas a 3,53 m (515,00 → arranque del alero); hastiales hasta la cara inferior
de la cubierta; piedra aparte (casa / jardín).
"""
import sys, json, math, datetime
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Polygon as MPoly
from matplotlib.backends.backend_pdf import PdfPages
from shapely.geometry import LineString, box, Polygon

for f in (r"C:\Windows\Fonts\GOTHIC.TTF", r"C:\Windows\Fonts\GOTHICB.TTF"):
    fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Century Gothic"
VERDE = (7/255, 87/255, 72/255); PIEDRA = (0.62, 0.42, 0.25); JARDIN = (0.80, 0.66, 0.40); ROJO = (0.75, 0.12, 0.12)
GRIS = (0.35, 0.35, 0.35)
COL = {1: VERDE, 2: PIEDRA, 3: JARDIN}

VISTAS = json.load(open(sys.argv[1], encoding="utf-8"))
PLANTAS = json.load(open(sys.argv[2], encoding="utf-8"))
SAL = Path(sys.argv[3]); SAL.mkdir(exist_ok=True)
UMBRAL = 3.0
r2 = lambda x: round(x + 1e-9, 2)

PARTIDAS = {
    1: ("FAC01", "m2", "Fachada completa, alternativa B (aislamiento por el interior)",
        "Fachada completa de la alternativa B (ficha 02 B), de fuera a dentro: revestimiento de mortero monocapa "
        "de 15 mm; fábrica portante de 1 pie de ladrillo cerámico tosco (pieza 233 x 106 x 96 mm, tipo «Cerámico "
        "tosco de 10» de Cerámica Millas o similar) recibida con mortero; enfoscado de mortero de cemento de 15 mm "
        "en la cara interior de la fábrica; aislamiento de EPS blanco de 100 mm pegado; hoja interior de ladrillo "
        "cerámico de gran formato de 70 mm machihembrado (70 x 50 x 7, Cerámica Millas o similar); guarnecido y "
        "enlucido de yeso de 15 mm. Espesor total aproximado 448 mm. Medida a cinta corrida sobre los alzados del "
        "proyecto: fachadas largas desde la cota 515,00 hasta el arranque del alero (3,53 m) y hastiales hasta la "
        "cara inferior de la cubierta; se descuentan los huecos de más de 3 m2. Incluido en el precio, sin medir aparte: "
        "en los 78,60 m de alero exterior de las cubiertas inclinadas, el remate entre pares, detrás del cajón del alero, "
        "de la hoja de fábrica de delante del durmiente y del trasdosado, desde el arranque del alero hasta la cara "
        "inferior del panel de cubierta (unos 0,17 m en la cara exterior, sin monocapa; ficha 03)."),
    2: ("FAC02", "m2", "Muro de la vivienda revestido de piedra (tipo 2)",
        "Muro de la vivienda con revestimiento de piedra (tipo 2), con solución constructiva por definir. Medido "
        "a cinta corrida sobre los alzados del proyecto, con los mismos criterios que la fachada completa: se "
        "descuentan los huecos de más de 3 m2."),
    3: ("FAC03", "m2", "Muro de jardín o de plataforma revestido de piedra (tipo 2)",
        "Muro exterior fuera de la vivienda (plataforma, jardín) con revestimiento de piedra (tipo 2), con "
        "solución constructiva por definir. Medida la cara vista en los alzados del proyecto, desde el terreno "
        "hasta la coronación; se descuentan los huecos de más de 3 m2."),
}

# ---------------------------------------------------------------- paños
# Cada paño: código, tipo, descripción, rect (x0, x1, y0, y1) en coordenadas de su vista o None,
# líneas extra [(comentario, uds, L, H)], huecos [(nombre, x0, x1, y0, y1)] o [(nombre, L, H)], fuente.
PANOS = []
def pano(cod, tipo, desc, vista, rect=None, huecos=(), extra=(), fuente="", plano=None, poly=None, techo=None, fondo=None,
         adoptada=False):
    PANOS.append(dict(cod=cod, tipo=tipo, desc=desc, vista=vista, rect=rect, huecos=list(huecos), extra=list(extra),
                      fuente=fuente, plano=plano, poly=poly, techo=techo, fondo=fondo, adoptada=adoptada))

def cara(cod, tipo, desc, vista, techo, fondo, fuente, plano=None):
    """Cara de muro con coronación horizontal (techo) y pie quebrado (fondo: puntos de izquierda a derecha)."""
    poly = [(fondo[0][0], techo), (fondo[-1][0], techo)] + list(reversed(fondo))
    pano(cod, tipo, desc, vista, poly=poly, techo=techo, fondo=fondo, fuente=fuente, plano=plano)

# origen de cada vista (para dibujar y para comprobar contra el DWG)
ORIGEN = {"W1": (0, 422000.0, 4412100.0), "1E": (2, 422000.0, 4412243.257), "1S": (4, 421800.0, 4412243.257),
          "Este": (9, 422200.0, 4412243.257), "4S": (7, 421800.0, 4412153.257)}

# --- Fachada norte · alzado W1 (vista 0). Origen: X 422000, Y 4412100; 515,00 = 83,257; alero = 86,787
W = dict(i=0, X=422000.0, Y=4412100.0, y515=83.257)
A, S5, G = 86.787, 83.257, 80.107
pano("N-1", 1, "Bloque de servicio y porche de entrada (cinta corrida)", "W1", (73.592, 91.992, S5, A),
     [("Celosía de lamas del recibidor", 85.002, 86.592, S5, 86.337), ("Puerta de entrada", 86.652, 88.132, 83.317, 86.277),
      ("Ventana V-4", 74.742, 76.617, 84.357, 85.757), ("Ventana V-5", 77.517, 78.267, 84.357, 85.757),
      ("Ventana V-6", 82.042, 83.492, 84.357, 85.757)], fuente="alzado W1")
pano("N-2", 1, "Frente del pasillo al patio (entre servicio y dormitorios 6-7)", "W1", (91.992, 94.992, S5, A),
     [("Acristalamiento VF-1", 91.992, 94.992, S5, 85.757)], fuente="alzado W1")
pano("N-3", 1, "Volumen de los dormitorios 6 y 7", "W1", (94.992, 104.992, S5, A),
     [("Puerta-ventana PV-2", 96.842, 99.342, S5, 85.757), ("Puerta-ventana PV-2", 101.492, 103.992, S5, 85.757)], fuente="alzado W1")
pano("N-4", 1, "Frente del pasillo al patio (entre dormitorios 6-7 y 5)", "W1", (104.992, 107.992, S5, A),
     [("Acristalamiento VF-1", 104.992, 107.992, S5, 85.757)], fuente="alzado W1")
pano("N-5", 1, "Volumen del dormitorio 5", "W1", (107.992, 114.192, S5, A),
     [("Puerta-ventana PV-2", 109.842, 112.342, S5, 85.757)], fuente="alzado W1")
pano("N-6", 1, "Unión de instalaciones", "W1", (114.192, 117.592, S5, A),
     [("Ventana fija", 116.667, 117.532, S5, 85.757)], fuente="alzado W1")
pano("N-7", 1, "Volumen D (dormitorio 4)", "W1", (117.592, 122.092, S5, A), [], fuente="alzado W1")
pano("N-8", 2, "Garaje bajo el bloque de servicio", "W1", (73.592, 84.542, G, S5),
     [("Puerta de garaje", 73.992, 77.367, G, 82.607), ("Puerta de garaje", 77.517, 80.892, G, 82.607),
      ("Puerta peatonal con fijo", 82.042, 83.492, G, 82.607)], fuente="alzado W1")

# --- Fachada sur · alzado 1E (vista 2). Origen: X 422000, Y 4412243,257 (515,00 = 0)
E = dict(i=2, X=422000.0, Y=4412243.257, y515=0.0)
pano("S-1", 1, "Volumen D (dormitorio 4)", "1E", (21.423, 25.923, 0.0, 3.53),
     [("Puerta-ventana PV-1", 22.423, 24.923, 0.0, 2.5)], fuente="alzado 1E")
pano("S-2", 1, "Frente del pasillo al patio (entre D y dormitorios 2-3)", "1E", (25.923, 28.923, 0.0, 3.53),
     [("Acristalamiento VF-1", 25.923, 28.923, 0.0, 2.5)], fuente="alzado 1E")
pano("S-3", 1, "Volumen de los dormitorios 2 y 3", "1E", (28.923, 38.923, 0.0, 3.53),
     [("Puerta-ventana PV-2", 30.773, 33.273, 0.0, 2.5), ("Puerta-ventana PV-2", 35.423, 37.923, 0.0, 2.5)], fuente="alzado 1E")
pano("S-4", 1, "Frente del pasillo al patio (entre dormitorios 2-3 y 1)", "1E", (38.923, 41.923, 0.0, 3.53),
     [("Acristalamiento VF-1", 38.923, 41.923, 0.0, 2.5)], fuente="alzado 1E")
pano("S-5", 1, "Volumen del dormitorio 1 y estudio", "1E", (41.923, 51.923, 0.0, 3.53),
     [("Puerta-ventana PV-2", 43.323, 45.823, 0.0, 2.5), ("Puerta-ventana PV-2", 47.973, 50.473, 0.0, 2.5)], fuente="alzado 1E")
pano("S-6", 1, "Frente del pasillo al patio (entre dormitorio 1 y salón)", "1E", (51.923, 54.923, 0.0, 3.53),
     [("Acristalamiento VF-1", 51.923, 54.923, 0.0, 2.5)], fuente="alzado 1E")
pano("S-7", 1, "Salón (fachada acristalada)", "1E", (54.923, 69.923, 0.0, 3.53),
     [("Acristalamiento del salón PV-3", 55.073, 69.773, 0.0, 3.435)], fuente="alzado 1E")
pano("S-8", 2, "Frente del gimnasio (sótano)", "1E", (56.898, 71.598, -3.15, 0.0),
     [("Acristalamiento PV-8", 58.973, 69.523, -3.15, -0.95)], fuente="alzado 1E")
cara("S-9", 3, "Muro de la plataforma, delante de D y de los dormitorios", "1E", 0.0,
     [(21.423, -1.9), (28.923, -1.9), (52.149, -3.15), (56.898, -3.15)], "alzado 1E")
pano("S-10", 3, "Muro de la plataforma, al este del gimnasio", "1E", (71.598, 77.923, -3.15, 0.0),
     [("Paso de la escalera", 73.923, 76.673, -3.15, 0.0)], fuente="alzado 1E")

# --- Muros con piedra que solo salen en el alzado este (vista 9), el oeste (1S) y la sección 4S
cara("E-1", 2, "Cara este del garaje, bajo el hastial del bloque de servicio", "Este", 0.0,
     [(65.965, 0.0), (67.470, -1.0), (68.939, -2.0), (71.807, -2.498)], "alzado este", plano=(95.40, 11.109, 95.40, 16.951))
cara("O-1", 2, "Zócalo bajo el hastial oeste del volumen D", "1S", 0.0,
     [(95.865, -0.421), (99.475, -1.0), (103.265, -1.422)], "alzado oeste (1S)", plano=(46.10, 12.501, 46.10, 5.101))
cara("E-2", 3, "Borde este de la plataforma (cuarto de aerotermia y escalera)", "Este", 0.0,
     [(51.417, -1.643), (55.147, -1.0), (59.142, 0.0)], "alzado este", plano=(102.6, -3.439, 102.6, 4.286))
cara("E-3", 3, "Muro del acceso al garaje, cara este (hacia la rampa)", "Este", 1.1,
     [(71.807, -1.688), (74.273, -2.0), (78.397, -2.457)], "alzado este", plano=(84.05, 16.951, 84.05, 23.541))
cara("G-1", 3, "Muro del acceso al garaje, cara oeste (hacia la terraza norte)", "4S", 1.1,
     [(84.824, -0.419), (87.815, 0.0), (91.415, 0.0)], "sección 4S", plano=(83.65, 16.951, 83.65, 23.541))
cara("O-2", 3, "Borde de la terraza al sur de D, cara oeste", "1S", 0.0,
     [(103.265, -1.422), (107.565, -1.9)], "alzado oeste (1S)", plano=(46.502, 5.101, 46.502, 0.801))
cara("O-3", 3, "Extremo oeste de la plataforma sur", "1S", 0.0,
     [(107.565, -1.9), (111.805, -2.1)], "alzado oeste (1S)", plano=(54.002, 0.801, 54.002, -3.439))
cara("O-4", 3, "Murete del nivel de la piscina, cara oeste", "1S", -3.15,
     [(115.757, -3.15), (117.074, -3.4), (121.805, -3.766)], "alzado oeste (1S)")
pano("PIS", 3, "Muros de la plataforma de la piscina", "licitación", None, [],
     [("tramo 1", 1, 26.00, 0.65), ("tramo 2", 1, 6.00, 0.40), ("tramo 3", 1, 6.00, 0.70)],
     "licitación 05.04 «Muro plataforma piscina», adoptada sin contrastar en planos", adoptada=True)

# --- Hastiales. Perfil medido en el alzado oeste (1S): 7,40 de ancho, 3,70 en los bordes, 4,69 en la cumbrera
HB, HC, AH = 3.70, 0.99, 7.40
def hastial(cod, desc, vista, tapado=None, huecos=(), fuente="", plano=None):
    extra = [("rectángulo", 1, AH, HB), ("triángulo bajo la cubierta", 0.5, AH, HC)]
    if tapado:
        extra.append((f"a deducir: {tapado[0]}", -1, tapado[1], tapado[2]))
    pano(cod, 1, desc, vista, None, list(huecos), extra, fuente, plano)
hastial("H-1", "Hastial oeste del volumen D", "1S", fuente="alzado oeste (1S)", plano=(46.502, 5.101, 46.502, 12.501),
        huecos=[("Ventana V-1", 0.80, 0.80)])
hastial("H-2", "Hastial oeste del dormitorio 5", "1S", tapado=("parte tapada por instalaciones y vestíbulo", 2.95, 3.53),
        fuente="alzado oeste (1S) y planta", plano=(54.402, 9.551, 54.402, 16.951))
hastial("H-3", "Hastial oeste de los dormitorios 2 y 3", "1S", fuente="alzado oeste (1S) y planta", plano=(54.002, 0.651, 54.002, 8.051),
        huecos=[("Ventana V-3", 2.10, 0.75)])
hastial("H-4", "Hastial este del volumen D", "planta", tapado=("parte tapada por instalaciones, vestíbulo y pasillo", 4.45, 3.53),
        fuente="planta A-02 + perfil", plano=(51.002, 5.101, 51.002, 12.501))
hastial("H-5", "Hastial este del dormitorio 5 (patio)", "planta", fuente="planta A-02 + perfil", plano=(60.602, 9.551, 60.602, 16.951),
        huecos=[("Ventana V-3", 2.10, 0.75)])
hastial("H-6", "Hastial oeste de los dormitorios 6 y 7 (patio)", "planta", fuente="planta A-02 + perfil", plano=(63.602, 9.551, 63.602, 16.951),
        huecos=[("Ventana V-2", 0.98, 0.80)])
hastial("H-7", "Hastial este de los dormitorios 6 y 7 (patio)", "planta", fuente="planta A-02 + perfil", plano=(73.602, 9.551, 73.602, 16.951),
        huecos=[("Ventana V-3", 2.10, 0.75)])
hastial("H-8", "Hastial oeste del bloque de servicio (porche)", "planta", tapado=("hueco del porche abierto", 3.30, 3.08),
        fuente="planta A-02 + perfil", plano=(76.602, 9.551, 76.602, 16.951), huecos=[("Acristalamiento VF-2", 1.00, 2.40)])
hastial("H-9", "Hastial este de los dormitorios 2 y 3 (patio)", "planta", fuente="planta A-02 + perfil", plano=(64.002, 0.651, 64.002, 8.051),
        huecos=[("Ventana V-2", 0.98, 0.80)])
hastial("H-10", "Hastial oeste del dormitorio 1 (patio)", "planta", fuente="planta A-02 + perfil", plano=(67.002, 0.651, 67.002, 8.051),
        huecos=[("Puerta PV-6", 1.00, 2.50)])
hastial("H-11", "Hastial este del dormitorio 1 (patio)", "planta", fuente="planta A-02 + perfil", plano=(77.002, 0.651, 77.002, 8.051),
        huecos=[("Puerta PV-6", 1.00, 2.50)])
hastial("H-12", "Hastial oeste del salón (patio)", "planta", fuente="planta A-02 + perfil", plano=(80.002, 0.651, 80.002, 8.051))
hastial("H-13", "Hastial este del bloque de servicio", "Este", fuente="alzado este", plano=(95.002, 9.551, 95.002, 16.951))
hastial("H-14", "Hastial este del salón", "Este", fuente="alzado este", plano=(95.002, 0.651, 95.002, 8.051),
        huecos=[("Acristalamiento PV-4", 6.60, 2.50)])
pano("H-15", 1, "Final este del pasillo", "Este", None, [("Puerta PV-5", 1.50, 2.50)], [("frente del pasillo", 1, 1.50, 3.53)],
     "alzado este", plano=(95.002, 8.051, 95.002, 9.551))
pano("P-1", 2, "Lateral este del porche (muro de la escalera, con piedra)", "planta", None, [],
     [("hasta la viga del porche", 1, 3.30, 3.08)], "planta A-02 y sección 4S", plano=(83.572, 13.651, 83.572, 16.951))

# ---------------------------------------------------------------- líneas de medición
LINEAS = {1: [], 2: [], 3: []}
for p in PANOS:
    L = LINEAS[p["tipo"]]
    base = f"{p['cod']} · {p['desc']}"
    if p["rect"]:
        x0, x1, y0, y1 = p["rect"]
        L.append((base, 1, r2(x1 - x0), r2(y1 - y0)))
    if p.get("fondo"):
        f = p["fondo"]
        for k, ((xa, ya), (xb, yb)) in enumerate(zip(f, f[1:]), 1):
            if xb - xa > 1e-6:
                L.append((base + f" · tramo {k}" + (" (altura media)" if abs(ya - yb) > 1e-6 else ""), 1,
                          r2(xb - xa), r2(p["techo"] - (ya + yb) / 2)))
    for i, (c, n, l, h) in enumerate(p["extra"]):
        L.append((base + (f" · {c}" if (p["rect"] or i) else f" · {c}"), n, r2(l), r2(h)))
    grupos = {}
    for hu in p["huecos"]:
        if len(hu) == 5:
            nom, a0, a1, b0, b1 = hu; l, h = r2(a1 - a0), r2(b1 - b0)
        else:
            nom, l, h = hu
        if l * h > UMBRAL:
            grupos[(nom, l, h)] = grupos.get((nom, l, h), 0) + 1      # huecos iguales del mismo paño: una línea
    for (nom, l, h), k in grupos.items():
        L.append((f"   a deducir: {nom} ({p['cod']})", -k, l, h))
TOTAL = {t: r2(sum(n * l * h for _, n, l, h in LINEAS[t])) for t in LINEAS}
print("TOTALES", TOTAL)

# ---------------------------------------------------------------- comprobación de cada línea
def segmentos(vista):
    vi, X, Y = ORIGEN[vista]
    out = []
    for e in VISTAS[vi]["ents"]:
        if e["l"] not in ("ALZ_FIN", "ALZ_GRU", "ALZ_CAR", "ALZ_AUX", "ALZ_TRM") or e["t"] in ("INSERT", "TEXT", "MTEXT"):
            continue
        for g in e.get("g", []):
            for (xa, ya), (xb, yb) in zip(g, g[1:]):
                out.append((xa - X, ya - Y, xb - X, yb - Y))
    return out
SEG = {v: segmentos(v) for v in ORIGEN}

def cubierto(vista, eje, c, a0, a1, tol=0.012):
    """Fracción del borde (vertical si eje='x', horizontal si 'y') que coincide con líneas del DWG."""
    tramos = []
    for xa, ya, xb, yb in SEG[vista]:
        if eje == "x" and abs(xa - c) < tol and abs(xb - c) < tol:
            tramos.append((min(ya, yb), max(ya, yb)))
        if eje == "y" and abs(ya - c) < tol and abs(yb - c) < tol:
            tramos.append((min(xa, xb), max(xa, xb)))
    tramos.sort(); cub, fin = 0.0, a0
    for s0, s1 in tramos:
        s0, s1 = max(s0, fin), min(s1, a1)
        if s1 > s0:
            cub += s1 - s0; fin = s1
    return cub / (a1 - a0) if a1 > a0 else 1.0

def punto_en_dwg(vista, x, y, tol=0.02):
    for xa, ya, xb, yb in SEG[vista]:
        dx, dy = xb - xa, yb - ya; L2 = dx * dx + dy * dy
        t = 0 if L2 == 0 else max(0, min(1, ((x - xa) * dx + (y - ya) * dy) / L2))
        if math.hypot(xa + t * dx - x, ya + t * dy - y) < tol:
            return True
    return False

def verificar():
    err, sin_dwg, n_bordes, n_ok = [], [], 0, 0
    for t, L in LINEAS.items():
        vistos = set()
        for c, n, l, h in L:
            if n == 0 or l <= 0 or h <= 0:
                err.append(f"línea a cero o negativa: {c}")
            if (c, n, l, h) in vistos:
                err.append(f"línea repetida: {c}")
            vistos.add((c, n, l, h))
    for p in PANOS:
        if p["rect"]:
            x0, x1, y0, y1 = p["rect"]
            for hu in p["huecos"]:
                if len(hu) == 5:
                    nom, a0, a1, b0, b1 = hu
                    if not (x0 - 0.005 <= a0 and a1 <= x1 + 0.005 and y0 - 0.005 <= b0 and b1 <= y1 + 0.005):
                        err.append(f"{p['cod']}: el hueco «{nom}» se sale del paño")
        for hu in p["huecos"]:
            l, h = (r2(hu[2] - hu[1]), r2(hu[4] - hu[3])) if len(hu) == 5 else (hu[1], hu[2])
            descontado = any(f"({p['cod']})" in c and nom_in(hu[0], c) for c, *_ in LINEAS[p["tipo"]])
            if (l * h > UMBRAL) != descontado:
                err.append(f"{p['cod']}: hueco «{hu[0]}» ({l*h:.2f} m²) mal tratado con el umbral de 3 m²")
        if p.get("fondo"):
            area = Polygon(p["poly"]).area
            suma = sum(n * l * h for c, n, l, h in LINEAS[p["tipo"]] if c.startswith(p["cod"] + " ·"))
            if abs(area - suma) > max(0.03, 0.005 * area):
                err.append(f"{p['cod']}: las líneas suman {suma:.2f} y el polígono mide {area:.2f}")
        # contra el DWG
        if p["vista"] in ORIGEN and p["rect"]:
            x0, x1, y0, y1 = p["rect"]
            for nombre, eje, c, a0, a1 in (("izquierda", "x", x0, y0, y1), ("derecha", "x", x1, y0, y1),
                                           ("pie", "y", y0, x0, x1), ("coronación", "y", y1, x0, x1)):
                n_bordes += 1
                if cubierto(p["vista"], eje, c, a0, a1) >= 0.5:
                    n_ok += 1
                else:
                    sin_dwg.append(f"{p['cod']} · borde {nombre}")
            for hu in p["huecos"]:
                if len(hu) == 5 and (hu[2] - hu[1]) * (hu[4] - hu[3]) > UMBRAL:
                    nom, a0, a1, b0, b1 = hu
                    for nombre, eje, c, s0, s1 in (("izquierda", "x", a0, b0, b1), ("derecha", "x", a1, b0, b1),
                                                   ("pie", "y", b0, a0, a1), ("dintel", "y", b1, a0, a1)):
                        n_bordes += 1
                        if cubierto(p["vista"], eje, c, s0, s1) >= 0.5:
                            n_ok += 1
                        else:
                            sin_dwg.append(f"{p['cod']} · {nom} · {nombre}")
        if p["vista"] in ORIGEN and p.get("fondo"):
            for (x, y) in p["fondo"]:
                n_bordes += 1
                if punto_en_dwg(p["vista"], x, y):
                    n_ok += 1
                else:
                    sin_dwg.append(f"{p['cod']} · punto del pie ({x:.2f}; {y:.2f})")
            n_bordes += 1
            xs = [x for x, _ in p["fondo"]]
            if cubierto(p["vista"], "y", p["techo"], min(xs), max(xs)) >= 0.5:
                n_ok += 1
            else:
                sin_dwg.append(f"{p['cod']} · coronación")
    perfil = Polygon([(0, 0), (7.40, 0), (7.40, 3.701), (3.70, 4.693), (0, 3.701)]).area
    if abs(AH * HB + 0.5 * AH * HC - perfil) > 0.05:
        err.append("el hastial de las líneas no coincide con el perfil medido")
    return err, sin_dwg, n_bordes, n_ok

def nom_in(nombre, comentario):
    return f"a deducir: {nombre} (" in comentario

ERR, SIN_DWG, N_BORDES, N_OK = verificar()
print(f"comprobación: {sum(len(L) for L in LINEAS.values())} líneas; {N_OK}/{N_BORDES} bordes y puntos encontrados en el DWG")
for s in SIN_DWG:
    print("   no está en el DWG:", s)
assert not ERR, "\n".join(ERR)

# ---------------------------------------------------------------- BC3
def bc3():
    hoy = datetime.date.today().strftime("%d%m%Y")
    num = lambda x: f"{x:.2f}"
    out = ["~V|AGOIN|FIEBDC-3/2016\\" + hoy + "|AGOIN|Cigarral Montealegre - fachadas alternativa B|ANSI||2|||",
           "~K|\\2\\2\\3\\2\\2\\2\\2\\EUR\\|0|",
           f"~C|CIGARRAL##||Vivienda Cigarral Montealegre - fachadas, alternativa B||{hoy[:4]+hoy[6:]}|0|",
           f"~C|FAC#||FACHADAS||{hoy[:4]+hoy[6:]}|0|",
           "~D|CIGARRAL##|FAC#\\1\\1\\|",
           "~D|FAC#|" + "".join(f"{PARTIDAS[t][0]}\\1\\{num(TOTAL[t])}\\" for t in (1, 2, 3)) + "|"]
    for t in (1, 2, 3):
        cod, ud, res, txt = PARTIDAS[t]
        out.append(f"~C|{cod}|{ud}|{res}||{hoy[:4]+hoy[6:]}|0|")
        out.append(f"~T|{cod}|{txt}|")
        lin = "".join(f"\\{c.strip().replace('|', '/').replace(chr(92), '/')}\\{n:g}\\{num(l)}\\\\{num(h)}\\" for c, n, l, h in LINEAS[t])
        out.append(f"~M|FAC#\\{cod}|{t}\\|{num(TOTAL[t])}|{lin}|")
    texto = "\r\n".join(out) + "\r\n"
    ruta = SAL / "MEDICION FACHADAS ALTERNATIVA B.bc3"
    ruta.write_bytes(texto.encode("cp1252"))
    return ruta, texto

# ---------------------------------------------------------------- dibujo de una vista
def dibuja_vista(ax, vi, X, Y, xr, yr, panos, piedra_zonas=()):
    v = VISTAS[vi]
    capas = {"ALZ_FIN": ("0.5", 0.45), "ALZ_GRU": ("0.2", 1.0), "ALZ_CAR": ("0.4", 0.45), "ALZ_TEJA": ("0.6", 0.35), "ALZ_AUX": ("0.65", 0.35)}
    zonas = [box(*z) for z in piedra_zonas]
    for e in v["ents"]:
        if e["l"] == "ALZ_TRM_Lajas":
            for g in e.get("g", []):
                if len(g) >= 2:
                    s0 = LineString([(x - X, y - Y) for x, y in g])
                    for z in zonas:
                        r = s0.intersection(z)
                        for s in getattr(r, "geoms", [r]):
                            if not s.is_empty and s.geom_type == "LineString":
                                xs, ys = zip(*s.coords); ax.plot(xs, ys, color=(0.5, 0.36, 0.22), lw=0.25)
            continue
        if e["l"] not in capas or e["t"] == "HATCH":
            continue
        c, lw = capas[e["l"]]
        for g in e.get("g", []):
            if len(g) < 2:
                continue
            if e["l"] == "ALZ_GRU" and any(abs(xb - xa) > 0.01 and abs(yb - ya) > 0.01 for (xa, ya), (xb, yb) in zip(g, g[1:])) and len(g) > 3:
                continue
            xs = [x - X for x, y in g]; ys = [y - Y for x, y in g]
            if max(xs) < xr[0] or min(xs) > xr[1] or max(ys) < yr[0] or min(ys) > yr[1]:
                continue
            ax.plot(xs, ys, color=c, lw=lw)
    for p in panos:
        col = COL[p["tipo"]]
        if p["rect"]:
            x0, x1, y0, y1 = p["rect"]
            ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=(*col, 0.22), ec=col, lw=1.5, zorder=5))
            cx, cy = (x0 + x1) / 2, y1 - 0.28
        elif p.get("poly"):
            ax.add_patch(MPoly(p["poly"], closed=True, fc=(*col, 0.25), ec=col, lw=1.5, zorder=5))
            c0 = Polygon(p["poly"]).representative_point(); cx, cy = c0.x, c0.y + 0.2
        else:
            continue
        for hu in p["huecos"]:
            if len(hu) == 5:
                nom, a0, a1, b0, b1 = hu
                if (a1 - a0) * (b1 - b0) > UMBRAL:
                    ax.add_patch(Rectangle((a0, b0), a1 - a0, b1 - b0, fc="white", ec=ROJO, lw=0.9, hatch="////", zorder=6, alpha=0.92))
        ax.text(cx, cy, p["cod"], ha="center", va="top", fontsize=8.5, fontweight="bold", color=col, zorder=9,
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
    ax.set_xlim(*xr); ax.set_ylim(*yr); ax.set_aspect("equal"); ax.axis("off")

def cabecera(fig, titulo, sub):
    fig.text(0.03, 0.965, titulo, fontsize=17, fontweight="bold", color=VERDE, va="top")
    fig.text(0.03, 0.932, sub, fontsize=9.5, color="0.25", va="top")
    fig.text(0.97, 0.965, "MIJEBAN · SOLUCIONES ALTERNATIVAS", fontsize=8, color=VERDE, ha="right", va="top", fontweight="bold")
    fig.text(0.97, 0.945, "Vivienda Cigarral Montealegre · fachadas, alternativa B", fontsize=8, color="0.4", ha="right", va="top")

def pie(fig, n):
    fig.text(0.03, 0.02, "Fuente: DWG «PLANTAS ALZADOS Y SECCIONES» del proyecto (alzados A-04 a A-07, planta A-02, memoria de carpintería DET-02). "
             "Cotas en m. Medición propuesta, sin aprobar.", fontsize=7.5, color="0.45")
    fig.text(0.97, 0.02, f"{n}", fontsize=8, color="0.45", ha="right")

def tabla_lineas(ax, filas, x_cols=(0.0, 0.70, 0.80, 0.89, 1.0), fs=7.6, dy=0.034, y0=0.98):
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    y = y0
    for h, x, ha in zip(("Paño / hueco", "Uds", "Long.", "Altura", "Parcial m²"), x_cols, ("left", "right", "right", "right", "right")):
        ax.text(x, y, h, fontsize=fs + 0.6, fontweight="bold", ha=ha, va="top")
    y -= dy * 1.3
    for fila in filas:
        if fila[0] == "#":
            ax.text(0.0, y, fila[1], fontsize=fs + 0.4, fontweight="bold", color=fila[2], va="top"); y -= dy; continue
        if fila[0] == "=":
            ax.text(x_cols[3], y, "Total", fontsize=fs + 0.4, fontweight="bold", ha="right", va="top")
            ax.text(x_cols[4], y, f"{fila[1]:.2f}".replace(".", ","), fontsize=fs + 0.6, fontweight="bold", ha="right", va="top")
            y -= dy * 1.4; continue
        c, n, l, h = fila
        FILAS_PDF.append((c, n, l, h))
        col = ROJO if n < 0 else "0.1"
        ax.text(0.0, y, c[:125], fontsize=fs, color=col, va="top")
        ax.text(x_cols[1], y, f"{n:g}".replace(".", ","), fontsize=fs, ha="right", va="top", color=col)
        ax.text(x_cols[2], y, f"{l:.2f}".replace(".", ","), fontsize=fs, ha="right", va="top", color=col)
        ax.text(x_cols[3], y, f"{h:.2f}".replace(".", ","), fontsize=fs, ha="right", va="top", color=col)
        ax.text(x_cols[4], y, f"{n*l*h:.2f}".replace(".", ","), fontsize=fs, ha="right", va="top", color=col)
        y -= dy
    return y

def lineas_de(prefijos, tipo):
    return [f for f in LINEAS[tipo] if any(f[0].strip().startswith(pr) or f"({pr})" in f[0] for pr in prefijos)]

# ---------------------------------------------------------------- PDF
def pdf():
    A3 = (16.54, 11.69)
    ruta = SAL / "MEDICION FACHADAS ALTERNATIVA B.pdf"
    pngs = []
    with PdfPages(ruta) as pp:
        # 1 · resumen
        fig = plt.figure(figsize=A3)
        cabecera(fig, "Medición de fachadas · alternativa B", "Resumen, criterios y comparación con la licitación")
        y = 0.86
        for t in (1, 2, 3):
            cod, ud, res, _ = PARTIDAS[t]
            fig.text(0.03, y, cod, fontsize=12, fontweight="bold", color=COL[t])
            fig.text(0.10, y, res, fontsize=12, color="0.1")
            fig.text(0.62, y, f"{TOTAL[t]:,.2f} m²".replace(",", " ").replace(".", ","), fontsize=14, fontweight="bold", color=COL[t], ha="right")
            y -= 0.045
        fig.text(0.03, y - 0.01, "FAC02: piedra en muros de la vivienda (garaje, gimnasio, porche, zócalos bajo fachada).   "
                 "FAC03: piedra en muros de la plataforma, terrazas, accesos y piscina.", fontsize=8.6, color="0.35")
        crit = ["Fuente: alzados del DWG del proyecto (W1, 1E, oeste 1S, este) y planta A-02 para lo que no sale en ningún alzado.",
                "A cinta corrida: cada cara una sola vez; W2 y 2E no se miden (repiten la fachada norte / son sección).",
                "Fachadas largas: de 515,00 al arranque del alero, 3,53 m (decisión del usuario). El remate entre pares tras el cajón,",
                "   hasta el panel (unos 0,17 m, sin monocapa, 78,60 m de alero), va incluido en el precio de FAC01 sin medirse aparte.",
                "Hastiales: perfil medido en el alzado oeste: 7,40 m de ancho, 3,70 m en los bordes y 4,69 m en la cumbrera (31,06 m²).",
                "Huecos: se descuentan los de más de 3 m², con las medidas dibujadas en los alzados; los menores se miden como macizo.",
                "Los 8 hastiales que dan a los patios no salen en alzado en ningún plano: se miden en planta con el mismo perfil.",
                "La franja de 0,85 m entre el pasillo y la unión de instalaciones es un vestíbulo interior (tiene puertas P-1): no es fachada."]
        fig.text(0.03, 0.66, "CRITERIOS", fontsize=10, fontweight="bold", color=VERDE)
        for k, c in enumerate(crit):
            fig.text(0.03, 0.63 - k * 0.0275, ("" if c.startswith("   ") else "■  ") + c, fontsize=9, color="0.15")
        # comparación
        x0 = 0.66
        fig.text(x0, 0.86, "COMPARACIÓN CON LA LICITACIÓN (partida 05.03)", fontsize=10, fontweight="bold", color=VERDE)
        comp = [("", "Licitación", "Esta medición"),
                ("Fachadas largas: longitud", "82,00 m", "82,00 m"),
                ("Fachadas largas: altura", "3,80 m", "3,53 m"),
                ("Hastiales", "14 × 33,15 m²", "14 × 31,06 m²"),
                ("Partes tapadas de hastiales", "—", "porche, instalaciones"),
                ("Frentes del pasillo a los patios", "—", "6 frentes"),
                ("Huecos", "todos (195,10 m²)", "> 3 m²"),
                ("Fachada de la vivienda sobre 515,00", "609,17 m²",
                 f"{TOTAL[1] + 10.16:,.2f} m²".replace(",", " ").replace(".", ","))]
        yy = 0.82
        for i, (a, b, c) in enumerate(comp):
            w = "bold" if i in (0, len(comp) - 1) else "normal"
            fig.text(x0, yy, a, fontsize=8.8, fontweight=w); fig.text(x0 + 0.19, yy, b, fontsize=8.8, ha="right", fontweight=w)
            fig.text(0.97, yy, c, fontsize=8.8, ha="right", fontweight=w, color=VERDE if i else "k")
            yy -= 0.028
        fig.text(x0, yy - 0.005, "La última fila suma FAC01 y el lateral de piedra del porche (P-1), que la licitación mide dentro de 05.03.",
                 fontsize=7.6, color="0.35")
        piedra = f"{TOTAL[2] + TOTAL[3]:.2f}".replace(".", ",")
        fig.text(x0, yy - 0.040, f"Piedra: licitación (05.04, como ladrillo de tejar) 300,21 m²; FAC02 + FAC03: {piedra} m².",
                 fontsize=8.4, color="0.15", fontweight="bold")
        fig.text(x0, yy - 0.062, "Son los mismos muros (acceso al garaje 6,70 m, borde oeste 11,66 m, frente de la", fontsize=7.6, color="0.35")
        fig.text(x0, yy - 0.078, "plataforma 25,81 m). Cambia la altura: la licitación pone 3,40 m a casi todos; aquí", fontsize=7.6, color="0.35")
        fig.text(x0, yy - 0.094, "cada cara se mide de su coronación al terreno dibujado.", fontsize=7.6, color="0.35")
        fig.text(x0, 0.45, "DISCREPANCIAS ENCONTRADAS (carpintería)", fontsize=10, fontweight="bold", color=VERDE)
        disc = ["V-3: la memoria de carpintería da 2,10 × 0,75 m; la licitación, 1,60 × 0,80 m.",
                "PV-1: memoria 2,30 × 2,50 m; dibujada en el alzado sur, 2,50 × 2,50 m.",
                "PV-3 (salón): memoria 14,07 × 2,50 m; el alzado dibuja un marco de 14,70 × 3,44 m.",
                "PV-4: memoria 6,22 × 2,50 m; dibujada, 6,60 × 2,50 m.",
                "PV-5: dos etiquetas en la planta; la licitación mide una unidad.",
                "PV-6: dos en la planta; la licitación no la mide."]
        for k, c in enumerate(disc):
            fig.text(x0, 0.42 - k * 0.026, "■  " + c, fontsize=8.2, color="0.15")
        fig.text(0.03, 0.40, "COMPROBACIÓN DE LAS LÍNEAS DE MEDICIÓN", fontsize=10, fontweight="bold", color=VERDE)
        n_lin = sum(len(L) for L in LINEAS.values())
        comp_l = [f"{n_lin} líneas. Cada una: uds × longitud × altura = parcial; sin líneas repetidas ni a cero; las sumas dan cada cantidad.",
                  f"Bordes de paños y huecos, y puntos de los muros de piedra, buscados en las líneas del DWG: {N_OK} de {N_BORDES} encontrados.",
                  "Cada hueco descontado está dentro de su paño y mide más de 3 m²; los menores no se descuentan.",
                  "Las caras quebradas (muros de piedra) suman lo mismo que su polígono. El BC3, leído de nuevo, tiene las mismas líneas que este PDF.",
                  "Es una comprobación de coherencia con el DWG: no sustituye a mirar cada alzado (páginas 3 a 6)."]
        for k, c in enumerate(comp_l):
            fig.text(0.03, 0.37 - k * 0.028, "■  " + c, fontsize=8.6, color="0.15")
        if SIN_DWG:
            fig.text(0.03, 0.37 - len(comp_l) * 0.028,
                     f"     Los {len(SIN_DWG)} no encontrados son el pie del garaje y de sus puertas (N-8): el alzado no dibuja línea de suelo; "
                     "sale de la cota 511,85 escrita en el alzado y del arranque de las puertas.", fontsize=7.8, color="0.35")
            assert all(s.startswith("N-8") and "pie" in s for s in SIN_DWG), SIN_DWG
        fig.text(0.03, 0.17, "LO QUE QUEDA ABIERTO", fontsize=10, fontweight="bold", color=VERDE)
        falta = ["PIS (muros de la plataforma de la piscina, 23,50 m²): no se pueden leer en los planos; se adopta la medición de la licitación (05.04).",
                 "Altura de las cubiertas de la unión de instalaciones y del pasillo: se toma 3,53 m (la del frente en los alzados)."]
        for k, c in enumerate(falta):
            fig.text(0.03, 0.14 - k * 0.028, "■  " + c, fontsize=8.6, color="0.15")
        pie(fig, 1); pp.savefig(fig); fig.savefig(SAL / "p1.png", dpi=80); plt.close(fig)

        # 2 · planta
        fig = plt.figure(figsize=A3)
        cabecera(fig, "Planta · todas las caras medidas", "Cada cara de fachada de la vivienda, con su código y la vista de donde sale su medida")
        ax = fig.add_axes([0.02, 0.14, 0.96, 0.74])
        v = [x for x in PLANTAS if x["hoja"] == "A-02"][0]; OX, OY = 421600, 4412200
        for e in v["ents"]:
            if e["t"] == "HATCH" and e["l"] in ("0_TRM", "0_PILARES"):
                for g in e["g"]:
                    xs, ys = zip(*g); ax.fill([x - OX for x in xs], [y - OY for y in ys], color="0.85", lw=0)
            elif e["l"] in ("0_GRU",) and e["t"] != "HATCH":
                for g in e.get("g", []):
                    if len(g) >= 2:
                        xs, ys = zip(*g); ax.plot([x - OX for x in xs], [y - OY for y in ys], color="0.6", lw=0.35)
        caras = {"N-1": (76.602, 16.951, 95.002, 16.951), "N-2": (73.602, 9.551, 76.602, 9.551), "N-3": (63.602, 16.951, 73.602, 16.951),
                 "N-4": (60.602, 9.551, 63.602, 9.551), "N-5": (54.402, 16.951, 60.602, 16.951), "N-6": (51.002, 12.501, 54.402, 12.501),
                 "N-7": (46.502, 12.501, 51.002, 12.501), "S-1": (46.502, 5.101, 51.002, 5.101), "S-2": (51.002, 8.051, 54.002, 8.051),
                 "S-3": (54.002, 0.651, 64.002, 0.651), "S-4": (64.002, 8.051, 67.002, 8.051), "S-5": (67.002, 0.651, 77.002, 0.651),
                 "S-6": (77.002, 8.051, 80.002, 8.051), "S-7": (80.002, 0.651, 95.002, 0.651)}
        caras.update({"N-8": (84.052, 17.35, 95.002, 17.35), "S-8": (81.977, -3.5, 96.677, -3.5),
                      "S-10": (96.677, -3.5, 103.0, -3.5), "S-9b": (54.002, -3.5, 81.977, -3.5)})
        caras["S-9"] = (46.502, 1.0, 54.002, 1.0)
        extra_seg = [("S-9", 3, caras.pop("S-9b"))]
        for cod, tipo, (x0_, y0_, x1_, y1_) in extra_seg:
            ax.plot([x0_, x1_], [y0_, y1_], color=COL[tipo], lw=4.5, solid_capstyle="butt", alpha=0.92)
        for p in PANOS:
            seg = caras.get(p["cod"]) or p.get("plano")
            if not seg:
                continue
            x0_, y0_, x1_, y1_ = seg
            ax.plot([x0_, x1_], [y0_, y1_], color=COL[p["tipo"]], lw=4.5, solid_capstyle="butt", alpha=0.92)
            mx, my = (x0_ + x1_) / 2, (y0_ + y1_) / 2
            if abs(x1_ - x0_) < 0.01:
                oeste = p["cod"] in ("H-1", "H-2", "H-3", "H-6", "H-8", "H-10", "H-12", "G-1") or p["cod"].startswith("O-")
                ax.text(mx + (-0.3 if oeste else 0.3), my + (-1.3 if oeste else 1.3), p["cod"], fontsize=8, color=COL[p["tipo"]],
                        ha="right" if oeste else "left", va="center", fontweight="bold")
            else:
                ax.text(mx, my + (0.35 if p["cod"].startswith("N") else -0.35), p["cod"], fontsize=8, color=COL[p["tipo"]],
                        ha="center", va="bottom" if p["cod"].startswith("N") else "top", fontweight="bold")
        ax.text(60.0, -5.2, "PIS · muros de la plataforma de la piscina (más al sur; medición adoptada de la licitación)", fontsize=7.5, color=JARDIN)
        ax.text(58.0, -6.4, "O-4 · murete del nivel de la piscina (alzado oeste)", fontsize=7.5, color=JARDIN)
        ax.annotate("N", xy=(105.5, 22.5), xytext=(105.5, 20.6), ha="center", fontsize=10, fontweight="bold",
                    arrowprops=dict(arrowstyle="-|>", color="0.2"))
        ax.set_xlim(44.5, 107.0); ax.set_ylim(-7.0, 24.5); ax.set_aspect("equal"); ax.axis("off")
        fig.text(0.03, 0.10, "Verde: FAC01, fachada completa.   Marrón: FAC02, muro de la vivienda con piedra.   Ocre: FAC03, muro de plataforma con piedra.",
                 fontsize=8.6, color="0.25")
        fig.text(0.03, 0.075, "N = fachada norte (alzado W1).   S = fachada sur (alzado 1E).   H = hastiales (alzados oeste y este; los de los patios, desde la planta).   "
                 "P-1 = lateral del porche.", fontsize=8.6, color="0.25")
        pie(fig, 2); pp.savefig(fig); fig.savefig(SAL / "p2.png", dpi=80); plt.close(fig)

        # 3 · W1
        fig = plt.figure(figsize=A3)
        cabecera(fig, "Fachada norte · alzado W1", "Paños verdes: FAC01. Marrón: FAC02 (piedra). Rayado rojo: huecos de más de 3 m², descontados")
        ax = fig.add_axes([0.02, 0.50, 0.96, 0.40])
        dibuja_vista(ax, 0, W["X"], W["Y"], (72.5, 123.5), (79.4, 88.6), [p for p in PANOS if p["vista"] == "W1"],
                     piedra_zonas=[(73.592, 80.107, 84.542, 83.257)])
        t = fig.add_axes([0.03, 0.05, 0.94, 0.43])
        filas = [("#", "FAC01 · fachada completa", VERDE)] + lineas_de(["N-1", "N-2", "N-3", "N-4", "N-5", "N-6", "N-7"], 1)
        filas += [("=", sum(n * l * h for _, n, l, h in filas[1:]))]
        filas += [("#", "FAC02 · muro de la vivienda con piedra", PIEDRA)] + lineas_de(["N-8"], 2)
        filas += [("=", sum(n * l * h for _, n, l, h in lineas_de(["N-8"], 2)))]
        tabla_lineas(t, filas, dy=0.036)
        pie(fig, 3); pp.savefig(fig); fig.savefig(SAL / "p3.png", dpi=80); plt.close(fig)

        # 4 · 1E
        fig = plt.figure(figsize=A3)
        cabecera(fig, "Fachada sur · alzado 1E", "Verde: FAC01. Marrón: FAC02 (gimnasio, sótano). Ocre: FAC03 (muro de la plataforma)")
        ax = fig.add_axes([0.02, 0.52, 0.96, 0.38])
        dibuja_vista(ax, 2, E["X"], E["Y"], (20.5, 79.0), (-3.6, 5.3), [p for p in PANOS if p["vista"] == "1E"],
                     piedra_zonas=[(21.423, -3.15, 77.923, 0.0)])
        t = fig.add_axes([0.03, 0.05, 0.94, 0.45])
        cods1 = ["S-1", "S-2", "S-3", "S-4", "S-5", "S-6", "S-7"]
        filas = [("#", "FAC01 · fachada completa", VERDE)] + lineas_de(cods1, 1)
        filas += [("=", sum(n * l * h for _, n, l, h in lineas_de(cods1, 1)))]
        filas += [("#", "FAC02 · muro de la vivienda con piedra", PIEDRA)] + lineas_de(["S-8"], 2)
        filas += [("=", sum(n * l * h for _, n, l, h in lineas_de(["S-8"], 2)))]
        filas += [("#", "FAC03 · muro de plataforma con piedra", JARDIN)] + lineas_de(["S-9", "S-10"], 3)
        filas += [("=", sum(n * l * h for _, n, l, h in lineas_de(["S-9", "S-10"], 3)))]
        tabla_lineas(t, filas, dy=0.030, fs=7.3)
        pie(fig, 4); pp.savefig(fig); fig.savefig(SAL / "p4.png", dpi=80); plt.close(fig)

        # 5 · hastiales
        fig = plt.figure(figsize=A3)
        cabecera(fig, "Hastiales", "Perfil medido en el alzado oeste (1S) y aplicado a los 14 hastiales; los de los patios no salen en ningún alzado")
        ax = fig.add_axes([0.02, 0.60, 0.46, 0.30])
        v1s = dict(X=421800.0, Y=4412243.257)
        dibuja_vista(ax, 4, v1s["X"], v1s["Y"], (89.0, 110.0), (-0.5, 6.2), [])
        prof = [(95.865, 0.0), (103.265, 0.0), (103.265, 3.701), (99.565, 4.693), (95.865, 3.701)]
        ax.add_patch(MPoly(prof, closed=True, fc=(*VERDE, 0.22), ec=VERDE, lw=1.6, zorder=5))
        ax.text(99.565, 2.3, "H-1\n31,06 m²", ha="center", fontsize=9, fontweight="bold", color=VERDE, zorder=9)
        for xx, yy, tx in ((96.1, 3.70, "3,70"), (99.565, 4.75, "4,69"), (99.565, -0.35, "7,40")):
            ax.text(xx, yy, tx, fontsize=7.5, color="0.2", ha="center" if xx > 97 else "left", va="bottom")
        fig.text(0.03, 0.57, "Alzado oeste (1S): hastial del volumen D de frente; detrás, los de los dormitorios 5 (H-2) y 2-3 (H-3).",
                 fontsize=8.5, color="0.3")
        ax2 = fig.add_axes([0.52, 0.60, 0.46, 0.30])
        dibuja_vista(ax2, 9, 422200.0, 4412243.257, (53.5, 73.5), (-0.5, 6.2), [])
        for (a0, a1, cod, hu) in ((55.507, 62.907, "H-14", (55.847, 62.447, 0.0, 2.5)), (64.407, 71.807, "H-13", None)):
            pr = [(a0, 0), (a1, 0), (a1, 3.701), ((a0 + a1) / 2, 4.693), (a0, 3.701)]
            ax2.add_patch(MPoly(pr, closed=True, fc=(*VERDE, 0.22), ec=VERDE, lw=1.6, zorder=5))
            if hu:
                ax2.add_patch(Rectangle((hu[0], hu[2]), hu[1] - hu[0], hu[3] - hu[2], fc="white", ec=ROJO, hatch="////", lw=0.9, zorder=6, alpha=0.92))
            ax2.text((a0 + a1) / 2, 3.2, cod, ha="center", fontsize=9, fontweight="bold", color=VERDE, zorder=9,
                     bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
        ax2.add_patch(Rectangle((62.907, 0), 1.5, 3.53, fc=(*VERDE, 0.22), ec=VERDE, lw=1.4, zorder=5))
        ax2.add_patch(Rectangle((62.907, 0), 1.5, 2.5, fc="white", ec=ROJO, hatch="////", lw=0.9, zorder=6, alpha=0.92))
        ax2.text(63.657, 3.0, "H-15", ha="center", fontsize=8, fontweight="bold", color=VERDE, zorder=9)
        fig.text(0.52, 0.57, "Alzado este: salón (H-14, con PV-4), final del pasillo (H-15, PV-5) y bloque de servicio (H-13).",
                 fontsize=8.5, color="0.3")
        t = fig.add_axes([0.03, 0.05, 0.94, 0.50])
        cods = [f"H-{k}" for k in range(1, 16)]
        filas = [("#", "FAC01 · hastiales y final del pasillo", VERDE)] + lineas_de(cods, 1)
        filas += [("=", sum(n * l * h for _, n, l, h in lineas_de(cods, 1)))]
        filas += [("#", "FAC02 · lateral del porche con piedra", PIEDRA)] + lineas_de(["P-1"], 2)
        filas += [("=", sum(n * l * h for _, n, l, h in lineas_de(["P-1"], 2)))]
        tabla_lineas(t, filas, dy=0.0205, fs=6.6)
        pie(fig, 5); pp.savefig(fig); fig.savefig(SAL / "p5.png", dpi=80); plt.close(fig)

        # 6 · muros con piedra que salen en el alzado este, el oeste y la sección 4S
        fig = plt.figure(figsize=A3)
        cabecera(fig, "Muros con piedra · alzados este y oeste, sección 4S",
                 "Marrón: FAC02 (vivienda). Ocre: FAC03 (plataforma, acceso al garaje, piscina). Cada cara, medida entre su coronación y el terreno dibujado")
        ax = fig.add_axes([0.02, 0.66, 0.60, 0.25])
        dibuja_vista(ax, 9, 422200.0, 4412243.257, (49.5, 80.0), (-3.4, 4.9), [p for p in PANOS if p["vista"] == "Este" and p.get("fondo")],
                     piedra_zonas=[(51.4, -3.2, 59.2, 0.0), (65.9, -2.6, 71.9, 0.0), (71.8, -2.6, 78.4, 1.1)])
        fig.text(0.03, 0.645, "Alzado este: E-1 cara este del garaje; E-2 borde este de la plataforma; E-3 muro del acceso al garaje (cara hacia la rampa).",
                 fontsize=8.3, color="0.3")
        ax = fig.add_axes([0.64, 0.66, 0.34, 0.25])
        dibuja_vista(ax, 7, 421800.0, 4412153.257, (83.5, 92.5), (-1.2, 4.2), [p for p in PANOS if p["vista"] == "4S" and p.get("fondo")],
                     piedra_zonas=[(84.8, -0.5, 91.5, 1.1)])
        fig.text(0.64, 0.645, "Sección 4S: G-1, el mismo muro por su cara hacia la terraza norte.", fontsize=8.3, color="0.3")
        ax = fig.add_axes([0.02, 0.37, 0.96, 0.25])
        dibuja_vista(ax, 4, 421800.0, 4412243.257, (93.0, 123.0), (-4.2, 5.2), [p for p in PANOS if p["vista"] == "1S" and p.get("fondo")],
                     piedra_zonas=[(95.8, -2.2, 111.9, 0.0), (115.7, -3.8, 121.9, -3.15)])
        fig.text(0.03, 0.355, "Alzado oeste: O-1 zócalo bajo el hastial de D; O-2 borde de la terraza al sur de D; O-3 extremo oeste de la plataforma sur; "
                 "O-4 murete del nivel de la piscina.", fontsize=8.3, color="0.3")
        t = fig.add_axes([0.03, 0.05, 0.94, 0.29])
        c2 = ["E-1", "O-1"]; c3 = ["E-2", "E-3", "G-1", "O-2", "O-3", "O-4", "PIS"]
        filas = [("#", "FAC02 · muro de la vivienda con piedra", PIEDRA)] + lineas_de(c2, 2)
        filas += [("=", sum(n * l * h for _, n, l, h in lineas_de(c2, 2)))]
        filas += [("#", "FAC03 · muro de plataforma con piedra (PIS: medición de la licitación, sin contrastar en planos)", JARDIN)] + lineas_de(c3, 3)
        filas += [("=", sum(n * l * h for _, n, l, h in lineas_de(c3, 3)))]
        tabla_lineas(t, filas, dy=0.042, fs=6.9)
        pie(fig, 6); pp.savefig(fig); fig.savefig(SAL / "p6.png", dpi=80); plt.close(fig)
    return ruta

FILAS_PDF = []          # todas las filas que se dibujan en las tablas del PDF
ruta_bc3, texto = bc3()
ruta_pdf = pdf()
# comprobaciones de forma
for t in (1, 2, 3):
    s = r2(sum(n * l * h for _, n, l, h in LINEAS[t]))
    assert abs(s - TOTAL[t]) < 0.005, (t, s, TOTAL[t])
# el BC3, leído de nuevo, tiene exactamente las mismas líneas
leido = {}
for reg in ruta_bc3.read_bytes().decode("cp1252").replace("\r\n", "").split("~")[1:]:
    if reg.startswith("M|"):
        f = reg.split("|"); cod = f[1].split("\\")[-1]; partes = f[4].split("\\")[1:]
        leido[cod] = [(partes[k].strip(), float(partes[k + 1]), float(partes[k + 2]), float(partes[k + 4]))
                      for k in range(0, len(partes) - 5, 6)]
for t in (1, 2, 3):
    esperado = [(c.strip().replace("|", "/"), float(n), l, h) for c, n, l, h in LINEAS[t]]
    assert leido[PARTIDAS[t][0]] == esperado, f"el BC3 no coincide con las líneas de {PARTIDAS[t][0]}"
# el PDF muestra cada línea una sola vez
todas = sorted((c, n, l, h) for t in LINEAS for c, n, l, h in LINEAS[t])
assert sorted(FILAS_PDF) == todas, f"PDF: {len(FILAS_PDF)} filas frente a {len(todas)} líneas"
print("BC3 releído = líneas; PDF = líneas: OK")
n_lin = sum(len(LINEAS[t]) for t in LINEAS)
print("líneas:", n_lin, "| BC3:", ruta_bc3, len(texto), "car. | PDF:", ruta_pdf)
for t in (1, 2, 3):
    print(f"  {PARTIDAS[t][0]}: {TOTAL[t]:.2f} m²  ({len(LINEAS[t])} líneas)")
json.dump({"capitulo": ("FAC#", "FACHADAS (ALTERNATIVA B)"),
           "partidas": {PARTIDAS[t][0]: list(PARTIDAS[t][1:]) for t in (1, 2, 3)},
           "totales": {PARTIDAS[t][0]: TOTAL[t] for t in (1, 2, 3)},
           "lineas": {PARTIDAS[t][0]: [[c, n, l, None, h] for c, n, l, h in LINEAS[t]] for t in (1, 2, 3)}},
          open(SAL / "lineas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
