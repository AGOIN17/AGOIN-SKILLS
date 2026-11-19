import sys, ezdxf
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
for e in msp:
    t = e.dxftype()
    if e.dxf.layer in ('A-NUMEROS', 'C_COD_01', 'A_06_TEXTOS', 'A-WALL-PATT', 'A-DETL-THIN', 'A-WALL', 'A-WALL-CAPAS') or t == 'DIMENSION':
        b = bbox.extents([e], fast=True)
        s = f"{t} {e.dxf.handle} L={e.dxf.layer} c={e.dxf.get('color')} tc={e.dxf.get('true_color')} lw={e.dxf.get('lineweight')} x[{b.extmin.x:.3f},{b.extmax.x:.3f}] y[{b.extmin.y:.3f},{b.extmax.y:.3f}]"
        if t == 'HATCH':
            s += f" pat={e.dxf.pattern_name} sc={e.dxf.get('pattern_scale')} ang={e.dxf.get('pattern_angle')} solid={e.dxf.solid_fill}"
        if t == 'TEXT':
            s += f" h={e.dxf.height} st={e.dxf.style} '{e.dxf.text}' al={e.dxf.get('halign')},{e.dxf.get('valign')}"
        if t == 'LWPOLYLINE':
            s += f" n={len(e)} cw={e.dxf.get('const_width')} pts={[tuple(round(v,3) for v in p[:2]) for p in e.get_points()][:6]}"
        if t == 'DIMENSION':
            s += f" style={e.dxf.dimstyle} txt='{e.dxf.get('text')}' meas={e.get_measurement():.4f}"
        print(s)
print('--- dimstyles')
for ds in doc.dimstyles:
    print(ds.dxf.name, {k: ds.dxf.get(k) for k in ('dimtxt', 'dimasz', 'dimscale', 'dimtsz', 'dimblk', 'dimclrt', 'dimtxsty', 'dimexo', 'dimexe', 'dimgap', 'dimdec', 'dimlfac', 'dimtad', 'dimclrd', 'dimclre', 'dimdle', 'dimlwd', 'dimlwe', 'dimtih', 'dimtoh')})
for st in ('1-10 (0.20)', '1-10 NEGRITA', 'FICHA', 'FICHA NEGRITA'):
    s = doc.styles.get(st)
    print(st, s.dxf.font, s.dxf.get('height'), s.dxf.get('width'), s.get_extended_font_data() if hasattr(s, 'get_extended_font_data') else '')
