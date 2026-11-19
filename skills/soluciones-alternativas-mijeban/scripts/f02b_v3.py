"""Ficha 02 B v3: grosor del proyecto según los planos (450 mm) y sin el bloque «A tener en cuenta».
Uso: python f02b_v3.py f7/src.dxf f7/f02b_v3.dxf"""
import sys, ezdxf
doc = ezdxf.readfile(sys.argv[1])
E = doc.entitydb
ps = doc.layouts.get('FICHA-A4')


def cambia(h, viejo, nuevo):
    e = E[h]
    assert viejo in e.text, (h, e.text)
    assert e.text.count(viejo) == 1, (h, viejo)
    e.text = e.text.replace(viejo, nuevo)


cambia('3D0', 'Proyecto: 401 mm, según la memoria', 'Proyecto: 450 mm, según los planos')
cambia('423', 'Ficha 02 B · v2', 'Ficha 02 B · v3')
cambia('423', 'plano DET-01', 'plantas del proyecto, plano DET-01')

# bloque «A tener en cuenta»: título, dos viñetas y sus dos cuadrados
assert 'A TENER EN CUENTA' in E['41C'].text
assert 'se corta' in E['41E'].text and '44 mm' in E['420'].text
for h in ('41C', '41D', '41E', '41F', '420'):
    ps.delete_entity(E[h])

# comprobación: no queda ninguno de los textos quitados
for e in ps.query('MTEXT'):
    for k in ('401 mm', 'TENER EN CUENTA', 'se corta en cada forjado', '44 mm más grueso', '· v2 ·'):
        assert k not in e.text, (e.dxf.handle, k)
doc.saveas(sys.argv[2])
print('guardado', sys.argv[2])
