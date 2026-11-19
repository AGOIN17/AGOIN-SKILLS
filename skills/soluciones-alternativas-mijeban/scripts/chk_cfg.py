import ezdxf
from ezdxf.tools import pattern
from ezdxf.fonts import fonts
doc = ezdxf.readfile('f4/v4.dxf')
print('MEASUREMENT', doc.header.get('$MEASUREMENT'), 'INSUNITS', doc.header.get('$INSUNITS'), 'LTSCALE', doc.header.get('$LTSCALE'), 'PSLTSCALE', doc.header.get('$PSLTSCALE'))
print([n for n in ('HEX', 'HONEY', 'AR-SAND', 'AR-CONC', 'ANSI34', 'ANSI31', 'ANSI37') if n in pattern.ISO_PATTERN])
print('linetypes', [l.dxf.name for l in doc.linetypes])
for h in ('3C2', '3B5', '3E4'):
    e = doc.entitydb[h]
    print(h, 'lsf', e.dxf.get('line_spacing_factor'), e.dxf.get('line_spacing_style'))
for l in ('A-AXO-LIN', 'A-AXO-COLOR', 'A-AXO-VERDE', 'A-WALL', 'A-WALL-CAPAS', 'A-WALL-PATT', 'A-DETL-THIN', 'A-NUMEROS', 'A_06_TEXTOS', 'C_COD_01'):
    L = doc.layers.get(l)
    print(l, L.color, L.dxf.get('lineweight'), L.dxf.get('true_color'), L.dxf.get('linetype'))
f = fonts.make_font('GOTHIC.TTF', 1.77)
print('ancho', f.text_width('Suelos sobre forjado sanitario y sótano'))
fb = fonts.make_font('GOTHICB.TTF', 1.77)
print('ancho negrita', fb.text_width('Suelos sobre forjado sanitario y sótano'))
