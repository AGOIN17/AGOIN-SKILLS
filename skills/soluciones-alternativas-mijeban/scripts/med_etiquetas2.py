import sys, re, json, ezdxf
from collections import Counter
doc = ezdxf.readfile(sys.argv[1])
msp = doc.modelspace()
OX, OY = 421600, 4412200
VENT = {"A-02": (421641.66, 4412181.95, 421705.16, 4412229.90), "A-01": (421643.07, 4412123.67, 421706.57, 4412181.07)}
res = {}
for hoja, (x0, y0, x1, y1) in VENT.items():
    et = []
    for e in msp.query("TEXT MTEXT"):
        p = e.dxf.insert
        if x0 <= p.x <= x1 and y0 <= p.y <= y1:
            t = (e.dxf.text if e.dxftype() == "TEXT" else e.plain_text()).strip()
            if re.match(r"^(PV|VF|V|P)\s*-\s*\d+", t):
                et.append((t, round(p.x - OX, 2), round(p.y - OY, 2), e.dxf.layer))
    res[hoja] = et
    print("##", hoja, Counter(t for t, *_ in et))
    for x in sorted(et, key=lambda r: (r[0], r[1])):
        print("   ", x)
json.dump(res, open(sys.argv[2], "w", encoding="utf-8"))
