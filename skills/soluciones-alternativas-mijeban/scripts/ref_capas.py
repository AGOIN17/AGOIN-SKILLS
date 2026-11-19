import sys, collections, ezdxf
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1])
msp = doc.modelspace()
cnt = collections.Counter((e.dxf.layer) for e in msp)
for k, v in cnt.most_common():
    print(v, k)
print('--- hatch patterns')
hp = collections.Counter((e.dxf.pattern_name, e.dxf.layer) for e in msp if e.dxftype() == 'HATCH')
for k, v in hp.most_common(60):
    print(v, k)
print('--- inserts')
ib = collections.Counter(e.dxf.name for e in msp if e.dxftype() == 'INSERT')
for k, v in ib.most_common(60):
    print(v, k)
print('--- layouts: viewports')
for l in doc.layouts:
    if l.name == 'Model':
        continue
    for v in l.query('VIEWPORT'):
        if v.dxf.id == 1:
            continue
        c = v.dxf.view_center_point
        print(l.name, 'centro', round(c.x, 2), round(c.y, 2), 'alto', round(v.dxf.view_height, 2), 'tam', round(v.dxf.width, 1), round(v.dxf.height, 1))
    for e in l:
        if e.dxftype() in ('TEXT', 'MTEXT'):
            t = e.dxf.text if e.dxftype() == 'TEXT' else e.plain_text()
            print('   ', l.name, t.replace('\n', ' ')[:100])
