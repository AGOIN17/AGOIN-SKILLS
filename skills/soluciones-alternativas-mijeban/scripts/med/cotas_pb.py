import sys, ezdxf, pickle
doc = ezdxf.readfile(sys.argv[1])
b = doc.blocks['P-B PR. EJECUCION']
out = []
for e in b.query('DIMENSION'):
    try: m = e.get_measurement()
    except Exception: continue
    if isinstance(m, float) and (abs(m-0.40) < 0.006 or abs(m-0.45) < 0.006 or abs(m-0.485) < 0.006 or abs(m - 0.416) < 0.006):
        p2, p3 = e.dxf.defpoint2, e.dxf.defpoint3
        out.append((round(m, 3), round(p2.x, 3), round(p2.y, 3), round(p3.x, 3), round(p3.y, 3), e.dxf.layer, e.dxf.get('text', '')))
for o in sorted(out): print(o)
import collections
print(collections.Counter(e.dxf.layer for e in b).most_common(25))
