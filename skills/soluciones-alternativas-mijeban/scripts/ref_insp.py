import sys, collections, ezdxf
doc = ezdxf.readfile(sys.argv[1])
msp = doc.modelspace()
print('units', doc.header.get('$INSUNITS'), 'ext', doc.header.get('$EXTMIN'), doc.header.get('$EXTMAX'))
print(collections.Counter(e.dxftype() for e in msp))
print('layouts', [l.name for l in doc.layouts])
txt = []
for e in msp:
    if e.dxftype() in ('TEXT', 'MTEXT'):
        t = e.dxf.text if e.dxftype() == 'TEXT' else e.plain_text()
        txt.append((round(e.dxf.insert.x, 1), round(e.dxf.insert.y, 1), e.dxf.layer, t.replace('\n', ' ')[:90]))
print(len(txt), 'textos')
for t in sorted(txt, key=lambda a: (-a[1], a[0])):
    print(t)
