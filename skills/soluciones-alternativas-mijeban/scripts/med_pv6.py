import sys, re, ezdxf
doc = ezdxf.readfile(sys.argv[1])
msp = doc.modelspace()
txt = []
for e in msp.query("TEXT MTEXT"):
    t = (e.dxf.text if e.dxftype() == "TEXT" else e.plain_text()).strip()
    txt.append((e.dxf.insert.x, e.dxf.insert.y, t, e.dxf.layer))
# zona de la memoria de carpintería (hoja DET-02): textos de tipo y cotas cercanas
for x, y, t, l in txt:
    if re.match(r"^(PV|VF|V)-\d+$", t) and 421700 < x < 421770 and 4412180 < y < 4412220:
        cerca = sorted([(round(abs(x2 - x) + abs(y2 - y), 2), t2) for x2, y2, t2, l2 in txt
                        if abs(x2 - x) < 3.5 and abs(y2 - y) < 5 and (re.search(r"\d[.,]\d", t2) or "x" in t2.lower())])[:8]
        print(f"{t:6s} ({x:.1f},{y:.1f}) cerca: {[c[1][:40] for c in cerca]}")
# cotas (DIMENSION) en la zona de cada tipo
for d in msp.query("DIMENSION"):
    try:
        p = d.dxf.defpoint
    except Exception:
        continue
print("textos con PV-6 en todo el modelo:", [(round(x, 1), round(y, 1), t[:60]) for x, y, t, l in txt if "PV-6" in t or "PV6" in t])
