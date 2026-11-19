import sys, ezdxf, collections
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
cnt = collections.Counter((e.dxf.layer, e.dxftype()) for e in msp)
for (l, t), k in sorted(cnt.items()):
    if k >= 1: print(k, l, t)
print('--- textos clave')
for e in msp.query('TEXT MTEXT'):
    t = e.plain_text() if e.dxftype() == 'MTEXT' else e.dxf.text
    if any(k in t.upper() for k in ('ACCESO', 'PLATAFORMA', 'GARAJE')) or t.strip() in ('P10', 'P29', 'P30', 'P42', 'P60', 'P61', 'P1', 'P20'):
        print(e.dxf.layer, repr(t[:40]), tuple(round(c, 2) for c in e.dxf.insert)[:2])
print('layouts', [l.name for l in doc.layouts])
