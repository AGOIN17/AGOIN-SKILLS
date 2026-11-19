import sys, ezdxf, collections
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
print('unidades', doc.header.get('$INSUNITS'), doc.header.get('$MEASUREMENT'))
dims = []
for e in msp.query('DIMENSION'):
    try: m = e.get_measurement()
    except Exception: m = None
    p = e.dxf.get('text_midpoint') or e.dxf.defpoint
    dims.append((round(m, 4) if isinstance(m, float) else m, e.dxf.get('text', ''), round(p.x, 2), round(p.y, 2), e.dxf.layer))
print('cotas', len(dims))
for d in sorted(dims, key=lambda d: (d[3], d[2]))[:120]: print(d)
print('--- textos')
for e in msp.query('TEXT MTEXT'):
    t = e.plain_text() if e.dxftype() == 'MTEXT' else e.dxf.text
    t = ' '.join(t.split())
    if any(k in t.lower() for k in ('ladrillo', 'fachada', 'aislam', 'cámara', 'camara', 'lana', 'monocapa', 'enfoscado', 'trasdos', 'tabique', 'piedra', 'muro', 'cm', 'mm')):
        print(e.dxf.layer, round(e.dxf.insert.x, 2), round(e.dxf.insert.y, 2), '|', t[:110])
