import sys, ezdxf
from collections import Counter
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1])
msp = doc.modelspace()
print("WIPEOUT en el modelo:", Counter(e.dxf.layer for e in msp.query("WIPEOUT")))
# orden de dibujo: ¿hay tabla SORTENTS?
try:
    st = msp.get_redraw_order()
    print("orden de dibujo propio:", len(list(st)), "entradas")
except Exception as ex:
    print("sin orden propio", ex)
# en la vista 1E (x 422018-422082, y 4412237-4412251): qué rellenos SOLID opacos hay y en qué capa/color
X0, X1, Y0, Y1 = 422018, 422082, 4412236, 4412251
c = Counter()
for e in msp.query("HATCH WIPEOUT SOLID"):
    b = bbox.extents([e], fast=True)
    if b.has_data and X0 <= b.extmin.x and b.extmax.x <= X1 and Y0 <= b.extmin.y and b.extmax.y <= Y1:
        tc = e.dxf.get("true_color")
        c[(e.dxftype(), e.dxf.layer, getattr(e.dxf, "pattern_name", ""), e.dxf.get("color"), tc)] += 1
for k, n in c.most_common(20):
    print(n, k)
