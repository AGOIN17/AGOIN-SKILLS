import sys, re, json, fitz
from collections import Counter
med = fitz.open(sys.argv[1])
t = "\n".join(p.get_text() for p in med)
i = t.find("\n12.01\n")
fin = t.find("\n13.01\n")
blk = t[i: fin if fin > 0 else i + 40000]
lines = [l.strip() for l in blk.split("\n") if l.strip()]
# partidas del capítulo 12 y sus líneas de medición
out = []
for k, l in enumerate(lines):
    if re.match(r"^12\.\d{2}$", l):
        out.append(f"\n[{l}] {lines[k+1][:90]}")
    elif re.match(r"^(VENTANA|PUERTA|PV|V|VF|P|FIJO|CORREDERA|MURO CORTINA)[\s\-]", l, re.I) or re.match(r"^[A-Z]{1,3}-\d+", l):
        out.append("   " + " | ".join(lines[k:k+6]))
print("\n".join(out)[:9000])
# etiquetas de carpintería en la planta baja
V = json.load(open(sys.argv[2], encoding="utf-8"))
for v in V:
    c = Counter(e["txt"].strip() for e in v["ents"] if e["t"] in ("TEXT", "MTEXT") and e["l"] in ("0_TXT CARP", "0_CAR", "0_TXT")
                and re.match(r"^[A-Z]{1,3}-\d+", e["txt"].strip()))
    print(v["hoja"], dict(sorted(c.items())))
