"""BC3 conjunto de las soluciones alternativas: une las líneas de fachadas y de cubierta en un solo FIEBDC-3 sin precios.

Uso: bc3_conjunto.py fachadas/lineas.json cubierta/lineas.json salida.bc3
Cada capítulo sale de su generador (medicion_fachadas.py, medicion_cubierta.py); aquí no se mide nada.
"""
import sys, json, datetime
from pathlib import Path

fuentes = [json.load(open(p, encoding="utf-8")) for p in sys.argv[1:-1]]
SAL = Path(sys.argv[-1])
hoy = datetime.date.today().strftime("%d%m%Y"); fecha = hoy[:4] + hoy[6:]
num = lambda x: f"{x:.2f}"
limpio = lambda s: s.strip().replace("|", "/").replace("\\", "/")
parcial = lambda ln: ln[1] * (ln[2] if ln[2] is not None else 1) * (ln[3] if ln[3] is not None else 1) * (ln[4] if ln[4] is not None else 1)

out = ["~V|AGOIN|FIEBDC-3/2016\\" + hoy + "|AGOIN|Cigarral Montealegre - soluciones alternativas: fachadas y cubierta|ANSI||2|||",
       "~K|\\2\\2\\3\\2\\2\\2\\2\\EUR\\|0|",
       f"~C|CIGARRAL##||Vivienda Cigarral Montealegre - soluciones alternativas (fachada B y cubierta de la ficha 03)||{fecha}|0|",
       "~D|CIGARRAL##|" + "".join(f"{f['capitulo'][0]}\\1\\1\\" for f in fuentes) + "|"]
esperado = {}
for f in fuentes:
    cap, nom = f["capitulo"]
    out.append(f"~C|{cap}||{nom}||{fecha}|0|")
    out.append(f"~D|{cap}|" + "".join(f"{c}\\1\\{num(f['totales'][c])}\\" for c in f["partidas"]) + "|")
    for pos, (c, (ud, res, txt)) in enumerate(f["partidas"].items(), start=1):
        lineas = f["lineas"][c]
        suma = round(sum(parcial(ln) for ln in lineas) + 1e-9, 2)
        assert abs(suma - f["totales"][c]) < 0.005, (c, suma, f["totales"][c])
        out.append(f"~C|{c}|{ud}|{res}||{fecha}|0|")
        out.append(f"~T|{c}|{txt}|")
        lin = "".join("\\" + limpio(com) + "\\" + f"{n:g}" + "\\" + "\\".join("" if v is None else num(v) for v in (lo, la, al)) + "\\"
                      for com, n, lo, la, al in lineas)
        out.append(f"~M|{cap}\\{c}|{pos}\\|{num(f['totales'][c])}|{lin}|")
        esperado[c] = [(limpio(com), float(n), lo, la, al) for com, n, lo, la, al in lineas]
texto = "\r\n".join(out) + "\r\n"
SAL.write_bytes(texto.encode("cp1252"))          # si un carácter no existe en CP1252, se para aquí

# releído: mismas líneas que los generadores
leido = {}
for reg in SAL.read_bytes().decode("cp1252").replace("\r\n", "").split("~")[1:]:
    if reg.startswith("M|"):
        p = reg.split("|"); c = p[1].split("\\")[-1]; partes = p[4].split("\\")[1:]
        val = lambda s: None if s == "" else float(s)
        leido[c] = [(partes[k].strip(), float(partes[k + 1]), val(partes[k + 2]), val(partes[k + 3]), val(partes[k + 4]))
                    for k in range(0, len(partes) - 5, 6)]
assert leido.keys() == esperado.keys(), (leido.keys(), esperado.keys())
for c in esperado:
    assert leido[c] == esperado[c], f"{c}: el BC3 no reproduce las líneas"
print(f"BC3 conjunto: {len(esperado)} partidas, {sum(len(v) for v in esperado.values())} líneas, releído = generadores: OK · {SAL}")
