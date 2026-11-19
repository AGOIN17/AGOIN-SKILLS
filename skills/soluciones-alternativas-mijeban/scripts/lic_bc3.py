"""Lee el BC3 de la licitación y vuelca partidas (código, ud, resumen, cantidad, texto, líneas) a JSON.
Uso: python lic_bc3.py <bc3> <salida.json>"""
import sys, json, re

raw = open(sys.argv[1], 'rb').read().decode('cp1252')
regs = [r for r in re.split(r'\r?\n?~', raw) if r.strip()]
C, T, D, M = {}, {}, {}, {}
for r in regs:
    tipo, _, resto = r.partition('|')
    campos = resto.split('|')
    if tipo == 'C':
        cod = campos[0].split('\\')[0]
        C[cod] = {'ud': campos[1], 'resumen': campos[2]}
    elif tipo == 'T':
        T[campos[0]] = campos[1].replace('\r', '').strip()
    elif tipo == 'D':
        partes = campos[1].split('\\')
        hijos = []
        for i in range(0, len(partes) - 2, 3):
            if partes[i]:
                hijos.append((partes[i], float(partes[i + 2] or 0)))
        D[campos[0]] = hijos
    elif tipo == 'M':
        padre, hijo = campos[0].split('\\')
        total = campos[2]
        lin = campos[3].split('\\') if len(campos) > 3 else []
        filas = []
        for i in range(0, len(lin) - 5, 6):
            filas.append(lin[i:i + 6])
        M[hijo] = {'padre': padre, 'total': total, 'lineas': filas}

# cantidad de cada partida desde ~D del capítulo padre
cant = {}
for padre, hijos in D.items():
    for h, q in hijos:
        cant[h] = (padre, q)

out = []
for cod, c in C.items():
    if '#' in cod:
        continue
    padre, q = cant.get(cod, (None, None))
    out.append({'cod': cod, 'cap': padre, 'ud': c['ud'], 'resumen': c['resumen'], 'cant': q,
                'texto': T.get(cod, ''), 'lineas': M.get(cod, {}).get('lineas', [])})
caps = {k: v['resumen'] for k, v in C.items() if '#' in k}
json.dump({'capitulos': caps, 'partidas': out}, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(caps), 'capítulos,', len(out), 'conceptos')
for k, v in caps.items():
    print(' ', k, v)
