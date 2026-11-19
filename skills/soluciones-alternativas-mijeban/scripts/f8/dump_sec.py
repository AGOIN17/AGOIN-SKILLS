"""Vuelca las entidades de la sección vertical (y > -0,3) de la ficha 02 B v3, con todos sus atributos."""
import sys, ezdxf
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
for e in msp:
    b = bbox.extents([e], fast=True)
    if not b.has_data or b.extmin.y < -0.3 or e.dxf.layer == 'A-NUMEROS':
        continue
    t = e.dxftype()
    a = {k: e.dxf.get(k) for k in ('layer', 'color', 'true_color', 'lineweight', 'linetype', 'ltscale') if e.dxf.hasattr(k)}
    s = f"{t} {e.dxf.handle} {a}"
    if t == 'LINE':
        s += f" {tuple(round(v, 4) for v in (e.dxf.start.x, e.dxf.start.y))}->{tuple(round(v, 4) for v in (e.dxf.end.x, e.dxf.end.y))}"
    elif t == 'LWPOLYLINE':
        s += f" closed={e.closed} cw={e.dxf.get('const_width')} pts={[tuple(round(float(v), 4) for v in p[:2]) + ((round(p[4], 3),) if p[4] else ()) for p in e.get_points()]}"
    elif t == 'HATCH':
        s += f" pat={e.dxf.pattern_name} solid={e.dxf.solid_fill} sc={e.dxf.get('pattern_scale')} ang={e.dxf.get('pattern_angle')} rgb={tuple(e.rgb) if e.rgb else None} paths={[[tuple(round(float(c), 4) for c in v[:2]) for v in p.vertices] for p in e.paths if hasattr(p, 'vertices')]}"
    elif t == 'TEXT':
        s += f" '{e.dxf.text}' ins={tuple(round(v, 4) for v in (e.dxf.insert.x, e.dxf.insert.y))} h={e.dxf.height} st={e.dxf.style} al={e.dxf.get('halign')},{e.dxf.get('valign')} align={e.dxf.get('align_point')}"
    elif t == 'DIMENSION':
        s += (f" style={e.dxf.dimstyle} type={e.dxf.dimtype} txt='{e.dxf.get('text')}' p1={tuple(round(v, 4) for v in (e.dxf.defpoint2.x, e.dxf.defpoint2.y))} p2={tuple(round(v, 4) for v in (e.dxf.defpoint3.x, e.dxf.defpoint3.y))}"
              f" dl={tuple(round(v, 4) for v in (e.dxf.defpoint.x, e.dxf.defpoint.y))} tm={tuple(round(v, 4) for v in (e.dxf.text_midpoint.x, e.dxf.text_midpoint.y))} blk={e.dxf.get('geometry')} ovr={e.get_dim_style().dxf.all_existing_dxf_attribs() if False else ''}")
        try:
            print('   override', e.get_acad_dstyle(e.get_dim_style()) if hasattr(e, 'get_acad_dstyle') else '')
        except Exception as ex:
            pass
    print(s)
ds = doc.dimstyles.get(next(iter(msp.query('DIMENSION'))).dxf.dimstyle)
print('DIMSTYLE', ds.dxf.name, ds.dxfattribs())
d = next(iter(msp.query('DIMENSION')))
print('XDATA', d.get_xdata('ACAD') if d.has_xdata('ACAD') else None)

