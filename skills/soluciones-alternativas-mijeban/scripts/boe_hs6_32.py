import sys, re, fitz
d = fitz.open(sys.argv[1])
t = ''
for i, p in enumerate(d):
    t += f' <<p{i+1}>> ' + p.get_text()
t = re.sub(r'\s+', ' ', t)
for clave in ['3.1 Barrera de protección 1', '3.2 Espacio de contención ventilado 1', '3.1 Barrera de protecci', '3.2 Espacio de contenci']:
    for m in re.finditer(re.escape(clave), t):
        if m.start() < 20000:
            continue
        print(f'[{clave}] {t[m.start():m.start()+2200]}\n')
        break
