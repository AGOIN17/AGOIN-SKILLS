"""Comprobador independiente del BC3: lee los bytes tal cual, sin reutilizar nada de los generadores.

Comprueba CRLF, juego de caracteres declarado, que no haya precios, el árbol (raíz → capítulos → partidas), que cada
partida tenga texto y unidad, y que las líneas de cada ~M sumen su total y la cantidad del ~D de su capítulo.
"""
import sys
raw = open(sys.argv[1], "rb").read()
problemas = []
if raw.count(b"\n") != raw.count(b"\r\n"):
    problemas.append("finales de línea no son CRLF")
txt = raw.decode("cp1252")
regs = txt.replace("\r\n", "").split("~")[1:]
V = [r for r in regs if r.startswith("V|")][0].split("|")
if V[5] != "ANSI":
    problemas.append(f"juego de caracteres declarado: {V[5]!r}")
C = {r.split("|")[1]: r.split("|") for r in regs if r.startswith("C|")}
T = {r.split("|")[1] for r in regs if r.startswith("T|")}
D = {}
for r in regs:
    if r.startswith("D|"):
        f = r.split("|"); campos = f[2].split("\\")
        D[f[1]] = {campos[k]: float(campos[k + 2]) for k in range(0, len(campos) - 2, 3)}
raiz = [c for c in C if c.endswith("##")]
if len(raiz) != 1:
    problemas.append(f"raíces: {raiz}")
capitulos = list(D.get(raiz[0], {})) if raiz else []
print("capítulos:", capitulos)
vistos = set()
for cap in capitulos:
    if not cap.endswith("#") or cap not in D:
        problemas.append(f"capítulo sin descomposición: {cap}")
        continue
    for cod, cant in D[cap].items():
        vistos.add(cod)
        if cod not in C or not C[cod][2].strip():
            problemas.append(f"{cod}: sin concepto o sin unidad")
        if cod not in T:
            problemas.append(f"{cod}: sin texto")
for r in regs:
    if r.startswith("M|"):
        f = r.split("|")
        cap, cod = f[1].split("\\")[0], f[1].split("\\")[-1]
        total = float(f[3])
        partes = f[4].split("\\")[1:]
        suma, n = 0.0, 0
        for k in range(0, len(partes) - 5, 6):
            com, uds, lon, lat, alt = partes[k:k + 5]
            v = (float(uds) if uds else 1) * (float(lon) if lon else 1) * (float(lat) if lat else 1) * (float(alt) if alt else 1)
            suma += v; n += 1
            if v == 0:
                problemas.append(f"{cod}: línea a cero «{com}»")
        cant = D.get(cap, {}).get(cod)
        ok = abs(round(suma, 2) - total) < 0.011 and cant is not None and abs(cant - total) < 0.011
        print(f"  {cap:5s} {cod}: {n:3d} líneas, suma {suma:9.2f}, ~M {total:9.2f}, ~D {cant}  {'OK' if ok else 'NO CUADRA'}")
        if not ok:
            problemas.append(f"{cod} no cuadra")
        vistos.discard(cod)
if vistos:
    problemas.append(f"partidas sin líneas: {sorted(vistos)}")
for c, f in C.items():
    if len(f) > 4 and f[4].strip():
        problemas.append("precio en " + c)
for palabra in ("fábrica", "cumbrera", "estanqueidad", "×"):
    print(f"  «{palabra}» aparece {txt.count(palabra)} veces (leído en CP1252)")
print("INCIDENCIAS:", problemas or "ninguna")
sys.exit(1 if problemas else 0)
