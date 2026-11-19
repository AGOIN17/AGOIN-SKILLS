import ezdxf, re
from medir import lineas
doc = ezdxf.readfile('f5/v5.dxf'); E = doc.entitydb
t = E['3F5'].text
print(repr(t))
par = t.split('\\P')
for p in par:
    plano = re.sub(r'\{\\f[^;]*;', '', p).replace('}', '')
    l, w = lineas(plano, 1.49, 130.0); print(len(l), round(w, 1))
nuevo = par[-1].replace("mediciones de licitación de 15/06/2026 (cap. 07), fichas de Thermochip TAH y Onduline BT-150 Plus, manual Onduline (2.4), ETE 08/0295 de Thermochip y DB-HS 1",
                        "licitación de 15/06/2026 (cap. 07), fichas Thermochip TAH y Onduline BT-150 Plus, ETE 08/0295 de Thermochip, manual Onduline (2.4) y DB-HS 1")
plano = re.sub(r'\{\\f[^;]*;', '', nuevo).replace('}', '')
l, w = lineas(plano, 1.49, 130.0); print('nuevo', len(l), round(w, 1), l)
