import sys, ezdxf
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
for e in msp.query('LWPOLYLINE[layer=="A-AXO-LIN"]'):
    print('LIN', e.dxf.handle, e.closed, e.dxf.get('lineweight'), [(round(p[0], 4), round(p[1], 4)) for p in e.get_points()])
print('---- hatches A-AXO-COLOR')
for e in msp.query('HATCH[layer=="A-AXO-COLOR"]'):
    rgb = tuple(e.rgb) if e.rgb else None
    pts = [[(round(v[0], 4), round(v[1], 4)) for v in p.vertices] for p in e.paths if hasattr(p, 'vertices')]
    n = sum(len(p) for p in pts)
    if not e.dxf.solid_fill or n <= 8:
        print('H', e.dxf.handle, e.dxf.pattern_name if not e.dxf.solid_fill else 'S', e.dxf.get('pattern_scale'), e.dxf.get('pattern_angle'), rgb, pts)
    else:
        print('H', e.dxf.handle, 'S', rgb, 'n', n)
print('---- A-AXO-DET')
for e in list(msp.query('LWPOLYLINE[layer=="A-AXO-DET"]'))[:12]:
    print('DET', e.dxf.handle, e.closed, e.dxf.get('lineweight'), e.dxf.get('true_color'), [(round(p[0], 4), round(p[1], 4)) for p in e.get_points()][:8])
for e in msp.query('*[layer=="A-AXO-LIN" or layer=="A-AXO-DET"]'):
    pass
lay = doc.layers
for n in ('A-AXO-COLOR', 'A-AXO-LIN', 'A-AXO-DET', 'A-NUMEROS', 'A-WALL', 'A-WALL-CAPAS', 'A-WALL-PATT', 'A-DETL-GENF', 'A-DETL-AISL', 'A-DETL-THIN', 'C_COD_01', 'A_06_TEXTOS'):
    l = lay.get(n)
    print('LAYER', n, l.dxf.color, l.dxf.get('true_color'), l.dxf.lineweight, l.dxf.linetype)
