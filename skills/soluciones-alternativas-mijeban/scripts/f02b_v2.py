"""Ficha 02 B (alternativa elegida): el apartado 2.3.1 pasa a «Suelos sobre forjado sanitario y sótano».
Uso: python f02b_v2.py f1/f02b.dxf f1/f02b_v2.dxf"""
import sys, ezdxf
doc = ezdxf.readfile(sys.argv[1])
E = doc.entitydb
ps = doc.layouts.get('FICHA-A4')
assert E['3C5'].text == 'Suelos sobre el terreno', E['3C5'].text
E['3C5'].text = 'Suelos sobre forjado\\Psanitario y sótano'
for h in ('3C6', '3C7', '3C8', '3C9', '3CA', '3CB'):
    p = E[h].dxf.insert
    E[h].dxf.insert = (p.x, p.y - 2.95)
n = 0
for e in ps.query('MTEXT'):
    if 'Ficha 02 B · v1' in e.text:
        e.text = e.text.replace('Ficha 02 B · v1', 'Ficha 02 B · v2')
        n += 1
print('pie actualizado:', n)
doc.saveas(sys.argv[2])
