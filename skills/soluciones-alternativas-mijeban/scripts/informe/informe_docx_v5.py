"""Informe de la propuesta alternativa de estructura (Cigarral Montealegre) en Word.
Uso: python informe_docx.py <carpeta de figuras> <salida.docx>"""
import re, sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FIG, SALIDA = sys.argv[1], sys.argv[2]
FONT = 'Century Gothic'
VERDE = RGBColor(0x07, 0x57, 0x48)
GRIS = RGBColor(0x59, 0x59, 0x59)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)
ANCHO = 17.0

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.0)
sec.top_margin, sec.bottom_margin = Cm(2.3), Cm(2.0)
sec.header_distance = sec.footer_distance = Cm(1.0)


# ---------- utilidades XML ----------
def ordenar(padre, orden):
    """Reordena los hijos de un elemento según el orden del esquema."""
    hijos = list(padre)
    clave = {qn(t): i for i, t in enumerate(orden)}
    hijos.sort(key=lambda e: clave.get(e.tag, len(orden)))
    for h in hijos:
        padre.remove(h)
    for h in hijos:
        padre.append(h)


ORDEN_PPR = ['w:pStyle', 'w:keepNext', 'w:keepLines', 'w:pageBreakBefore', 'w:framePr', 'w:widowControl',
             'w:numPr', 'w:suppressLineNumbers', 'w:pBdr', 'w:shd', 'w:tabs', 'w:suppressAutoHyphens',
             'w:kinsoku', 'w:wordWrap', 'w:overflowPunct', 'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN',
             'w:bidi', 'w:adjustRightInd', 'w:snapToGrid', 'w:spacing', 'w:ind', 'w:contextualSpacing',
             'w:mirrorIndents', 'w:suppressOverlap', 'w:jc', 'w:textDirection', 'w:textAlignment',
             'w:textboxTightWrap', 'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr', 'w:pPrChange']
ORDEN_TBLPR = ['w:tblStyle', 'w:tblpPr', 'w:tblOverlap', 'w:bidiVisual', 'w:tblStyleRowBandSize',
               'w:tblStyleColBandSize', 'w:tblW', 'w:jc', 'w:tblCellSpacing', 'w:tblInd', 'w:tblBorders',
               'w:shd', 'w:tblLayout', 'w:tblCellMar', 'w:tblLook']
ORDEN_TCPR = ['w:cnfStyle', 'w:tcW', 'w:gridSpan', 'w:hMerge', 'w:vMerge', 'w:tcBorders', 'w:shd', 'w:noWrap',
              'w:tcMar', 'w:textDirection', 'w:tcFitText', 'w:vAlign', 'w:hideMark']


def borde_inferior(par, color='075748', sz=6):
    pPr = par._p.get_or_add_pPr()
    b = OxmlElement('w:pBdr')
    e = OxmlElement('w:bottom')
    for k, v in (('w:val', 'single'), ('w:sz', str(sz)), ('w:space', '4'), ('w:color', color)):
        e.set(qn(k), v)
    b.append(e)
    pPr.append(b)
    ordenar(pPr, ORDEN_PPR)


def fuente(rpr_padre_estilo, nombre=FONT):
    rpr = rpr_padre_estilo
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(a), nombre)
    for a in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        if rf.get(qn(a)) is not None:
            del rf.attrib[qn(a)]


def estilo(nombre, size, bold=False, italic=False, color=None, antes=0, despues=6, interlineado=1.15,
           keep_next=False):
    st = doc.styles[nombre]
    st.font.name = FONT
    st.font.size = Pt(size)
    st.font.bold = bold
    st.font.italic = italic
    if color is not None:
        st.font.color.rgb = color
    fuente(st.element.get_or_add_rPr())
    pf = st.paragraph_format
    pf.space_before, pf.space_after = Pt(antes), Pt(despues)
    pf.line_spacing = interlineado
    pf.keep_with_next = keep_next
    return st


normal = estilo('Normal', 10, despues=6)
lang = OxmlElement('w:lang')
lang.set(qn('w:val'), 'es-ES')
normal.element.get_or_add_rPr().append(lang)
estilo('Heading 1', 13, bold=True, color=VERDE, antes=16, despues=6, keep_next=True)
estilo('Heading 2', 10.5, bold=True, color=VERDE, antes=10, despues=4, keep_next=True)
estilo('List Bullet', 10, despues=3)
pie = doc.styles.add_style('Pie de figura', 1)
pie.base_style = normal
estilo('Pie de figura', 8, italic=True, color=GRIS, antes=3, despues=10)


def runs(par, texto, size=None, color=None, bold=False):
    """Añade texto con **negritas** a un párrafo."""
    for trozo in re.split(r'(\*\*.+?\*\*)', texto):
        if not trozo:
            continue
        b = trozo.startswith('**')
        r = par.add_run(trozo[2:-2] if b else trozo)
        r.bold = b or bold
        if size:
            r.font.size = Pt(size)
        if color is not None:
            r.font.color.rgb = color
    return par


def parrafo(texto, estilo_=None, **kw):
    p = doc.add_paragraph(style=estilo_)
    return runs(p, texto, **kw)


def titulo(texto, pagina_nueva=False):
    p = doc.add_paragraph(texto, style='Heading 1')
    p.paragraph_format.page_break_before = pagina_nueva
    return p


def vineta(texto):
    return parrafo(texto, 'List Bullet')


def figura(nombre, ancho, pie_txt):
    doc.add_picture(f'{FIG}\\{nombre}', width=Cm(ancho))
    p = doc.paragraphs[-1]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(0)
    parrafo(pie_txt, 'Pie de figura')


def sombra(celda, color):
    tcPr = celda._tc.get_or_add_tcPr()
    s = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'), color)
    tcPr.append(s)
    ordenar(tcPr, ORDEN_TCPR)


def texto_celda(celda, texto, size=8.5, bold=False, color=None):
    celda.text = ''
    p = celda.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    runs(p, texto, size=size, color=color, bold=bold)
    celda.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP


def preparar_tabla(t, anchos, bordes):
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    tblPr = t._tbl.tblPr
    for v in tblPr.findall(qn('w:tblStyle')):
        tblPr.remove(v)
    lay = OxmlElement('w:tblLayout')
    lay.set(qn('w:type'), 'fixed')
    tblPr.append(lay)
    b = OxmlElement('w:tblBorders')
    for lado, val, sz, col in bordes:
        e = OxmlElement(f'w:{lado}')
        e.set(qn('w:val'), val)
        if val != 'nil':
            e.set(qn('w:sz'), str(sz))
            e.set(qn('w:space'), '0')
            e.set(qn('w:color'), col)
        b.append(e)
    tblPr.append(b)
    mar = OxmlElement('w:tblCellMar')
    for lado, w in (('top', 45), ('left', 85), ('bottom', 45), ('right', 85)):
        e = OxmlElement(f'w:{lado}')
        e.set(qn('w:w'), str(w))
        e.set(qn('w:type'), 'dxa')
        mar.append(e)
    tblPr.append(mar)
    tw = tblPr.find(qn('w:tblW'))
    if tw is None:
        tw = OxmlElement('w:tblW')
        tblPr.append(tw)
    tw.set(qn('w:w'), str(int(sum(anchos) * 567)))
    tw.set(qn('w:type'), 'dxa')
    ordenar(tblPr, ORDEN_TBLPR)
    grid = t._tbl.tblGrid
    for gc, a in zip(grid.findall(qn('w:gridCol')), anchos):
        gc.set(qn('w:w'), str(int(a * 567)))
    for fila in t.rows:
        trPr = fila._tr.get_or_add_trPr()
        cs = OxmlElement('w:cantSplit')
        trPr.append(cs)
        for c, a in zip(fila.cells, anchos):
            c.width = Cm(a)


BORDES_DATOS = [('top', 'single', 8, '075748'), ('left', 'nil', 0, ''), ('bottom', 'single', 8, '075748'),
                ('right', 'nil', 0, ''), ('insideH', 'single', 4, 'C8C8C8'), ('insideV', 'nil', 0, '')]


def tabla(cab, filas, anchos, col0_negrita=True, ultima_negrita=False):
    assert abs(sum(anchos) - ANCHO) < 0.01, (cab, sum(anchos))
    t = doc.add_table(rows=1 + len(filas), cols=len(cab))
    preparar_tabla(t, anchos, BORDES_DATOS)
    for i, h in enumerate(cab):
        c = t.rows[0].cells[i]
        texto_celda(c, h, bold=True, color=BLANCO)
        sombra(c, '075748')
    th = OxmlElement('w:tblHeader')
    t.rows[0]._tr.get_or_add_trPr().append(th)
    for r, fila in enumerate(filas):
        assert len(fila) == len(cab), fila
        for i, txt in enumerate(fila):
            c = t.rows[r + 1].cells[i]
            texto_celda(c, txt, bold=(i == 0 and col0_negrita) or (ultima_negrita and r == len(filas) - 1))
            if r % 2 == 1:
                sombra(c, 'F4F6F5')
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def recuadro(titulo_txt, lineas):
    t = doc.add_table(rows=1, cols=1)
    preparar_tabla(t, [ANCHO], [('top', 'nil', 0, ''), ('left', 'single', 24, '075748'), ('bottom', 'nil', 0, ''),
                                ('right', 'nil', 0, ''), ('insideH', 'nil', 0, ''), ('insideV', 'nil', 0, '')])
    c = t.rows[0].cells[0]
    sombra(c, 'F2F2F1')
    texto_celda(c, titulo_txt, size=9, bold=True, color=VERDE)
    for ln in lineas:
        p = c.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.1
        runs(p, ln, size=9)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def campo(par, instr, size, color):
    for tipo, txt in (('begin', None), ('instr', instr), ('separate', None), ('texto', '1'), ('end', None)):
        r = par.add_run()
        r.font.size = Pt(size)
        r.font.color.rgb = color
        if tipo == 'instr':
            it = OxmlElement('w:instrText')
            it.set(qn('xml:space'), 'preserve')
            it.text = f' {txt} '
            r._r.append(it)
        elif tipo == 'texto':
            r.text = txt
        else:
            fc = OxmlElement('w:fldChar')
            fc.set(qn('w:fldCharType'), tipo)
            r._r.append(fc)


# ---------- cabecera y pie ----------
for nombre in ('Header', 'Footer'):
    st = doc.styles[nombre]
    st.paragraph_format.tab_stops.clear_all()
    fuente(st.element.get_or_add_rPr())
h = sec.header.paragraphs[0]
h.paragraph_format.tab_stops.add_tab_stop(Cm(ANCHO - 0.05), WD_TAB_ALIGNMENT.RIGHT)
runs(h, 'MIJEBAN · SOLUCIONES ALTERNATIVAS', size=7.5, color=VERDE, bold=True)
runs(h, '\tCigarral Montealegre · Toledo', size=7.5, color=GRIS)
borde_inferior(h, 'BFBFBF', 4)
f = sec.footer.paragraphs[0]
f.paragraph_format.tab_stops.add_tab_stop(Cm(ANCHO - 0.05), WD_TAB_ALIGNMENT.RIGHT)
runs(f, 'Propuesta pendiente del cálculo estructural del arquitecto', size=7.5, color=GRIS)
runs(f, '\tPágina ', size=7.5, color=GRIS)
campo(f, 'PAGE', 7.5, GRIS)
runs(f, ' de ', size=7.5, color=GRIS)
campo(f, 'NUMPAGES', 7.5, GRIS)

# ---------- portada (cabeza de la primera página) ----------
p = parrafo('INFORME · ESQUEMA ESTRUCTURAL', size=8, color=VERDE, bold=True)
p.paragraph_format.space_after = Pt(4)
p = parrafo('Propuesta alternativa de estructura, cimentación y fachada', size=20, color=VERDE, bold=True)
p.paragraph_format.line_spacing = 1.0
p.paragraph_format.space_after = Pt(6)
p = parrafo('Vivienda unifamiliar aislada, cigarral, con garaje y piscina', size=10.5, color=GRIS)
p.paragraph_format.space_after = Pt(10)

datos = [
    ('Situación', 'Callejón de la Bastida s/n, con vuelta a la carretera de San Jerónimo. 45004 Toledo'),
    ('Promotores', '<Promotores>'),
    ('Arquitectos redactores', '<Arquitectos redactores>'),
    ('Técnicos redactores de la propuesta alternativa', 'Técnicos MIJEBAN – AGOIN'),
    ('Fecha', '10 de noviembre de 2026'),
    ('Estado', 'Propuesta. Pendiente del cálculo estructural, que corresponde al arquitecto, y de su aprobación'),
]
t = doc.add_table(rows=len(datos), cols=2)
preparar_tabla(t, [4.6, 12.4], [('top', 'single', 8, '075748'), ('left', 'nil', 0, ''), ('bottom', 'single', 8, '075748'),
                                 ('right', 'nil', 0, ''), ('insideH', 'single', 2, 'D9D9D9'), ('insideV', 'nil', 0, '')])
for (k, v), fila in zip(datos, t.rows):
    texto_celda(fila.cells[0], k.upper(), size=7.5, bold=True, color=VERDE)
    texto_celda(fila.cells[1], v, size=9)
doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ---------- 1. Resumen ----------
titulo('1. Resumen')
parrafo('Se propone sustituir los pilares y vigas de hormigón por muros de carga de ladrillo de un pie, con '
        'cimentación corrida escalonada según el terreno. La propuesta parte de un estudio de la topografía con un '
        'modelo BIM, en el que se ha comparado el terreno natural con las cotas del proyecto.')
parrafo('Los muros siguen las líneas de muro del proyecto y los suelos acabados quedan a las mismas cotas: 515,00 en '
        'planta baja y 511,85 en el sótano. Es una propuesta, no una solución aprobada: queda pendiente del cálculo '
        'estructural, que corresponde al arquitecto.')
tabla(['Elemento', 'Proyecto', 'Propuesta', 'Plano'], [
    ['Terreno', 'Excavación en vaciado: 1.185 m³ en la licitación (01.02)',
     'Plataformas a distintas cotas, según el terreno real', 'EST_00 y EST_01'],
    ['Estructura vertical', '62 pilares de hormigón armado y metálicos, con vigas de hormigón',
     'Muros de carga de ladrillo tosco de un pie (24 cm). Quedan pilares en el salón y el sótano', 'EST_03'],
    ['Cimentación', 'Zapatas aisladas, vigas de atado y losas',
     'Zapata corrida bajo los muros, apoyada en el nivel firme', 'EST_02'],
    ['Suelo de la vivienda', 'Forjado sanitario de viguetas autoportantes 25+5',
     'Forjado sanitario de placa alveolar 20+5', 'EST_03'],
    ['Suelo del sótano', 'Forjado sanitario a −3,25',
     'Solera sobre encachado hasta la línea de la piscina', 'EST_02'],
    ['Garaje y contención', 'Acceso rodado por el norte, entre muros',
     'Acceso por una explanada al norte del garaje y muros de contención ajustados a las plataformas, en estudio',
     'EST_01'],
    ['Fachada', 'Estructura de hormigón y dos hojas de ladrillo (450 mm en los planos)',
     'El muro de carga es la fachada: monocapa, ladrillo de un pie, EPS de 100 mm por dentro y trasdosado (445 mm)',
     'Ficha 02 B'],
], [3.1, 5.0, 6.6, 2.3])
recuadro('PARA DECIDIR', [
    '**Arquitecto:** valorar el sistema de muros de carga y el acceso al garaje, y desarrollar el cálculo estructural.',
    '**Promotores:** dar el visto bueno para seguir con la propuesta.',
    'Las cifras de excavación, relleno y coste se darán con la medición, cuando el esquema esté cerrado.',
])

# ---------- 2. Topografía ----------
titulo('2. Estudio de la topografía con el modelo BIM', True)
parrafo('Se ha medido en un modelo BIM la diferencia entre el terreno natural y la cara inferior de los forjados del '
        'proyecto (plano EST_00). El terreno queda por encima del forjado en el 47 % de la vivienda y en el 88 % del '
        'sótano.')
parrafo('El terreno del modelo se ha obtenido del LiDAR del PNOA, el vuelo con láser del Plan Nacional de '
        'Ortofotografía Aérea, ajustado al levantamiento topográfico. Su precisión es de unos ±0,15–0,20 m. La '
        'implantación se ha comprobado con las rasantes de las secciones del proyecto, con una diferencia media menor '
        'de 0,25 m. Antes de ejecutar se confirmará con taquimetría.')
parrafo('El plano colorea cada punto de la huella: en rojo, el terreno que queda por encima del forjado y hay que '
        'picar; en azul, el que queda por debajo y hay que rellenar o salvar con altura de muro. En cada cruce de ejes '
        'se da la cota del terreno y la diferencia.')
figura('fig1_est00.jpg', ANCHO, 'Figura 1. Terreno natural respecto a la cara inferior del forjado. Plano EST_00, '
       'obtenido del modelo BIM.')
tabla(['Bajo la huella', 'Zona A: planta baja sobre cámara', 'Zona B: sótano y terraza de la piscina'], [
    ['Usos', 'Dormitorios, pasillo y servicio', 'Garaje, gimnasio, instalaciones y terraza'],
    ['Superficie', '666 m²', '534 m²'],
    ['Cara inferior del forjado', '514,60', '511,45'],
    ['Terreno natural', '512,05 a 516,40', '510,33 a 514,95'],
    ['Diferencia con el forjado', '−2,55 a +1,80 m', '−1,12 a +3,50 m'],
    ['Superficie que hay que picar', '47 %', '88 %'],
    ['Terreno sobre la cara inferior', '234 m³', '824 m³'],
    ['A picar, con cámara de 30 cm', '338 m³', '—'],
    ['Hueco bajo la cara inferior', '328 m³', '25 m³'],
], [5.0, 6.0, 6.0])
parrafo('Los volúmenes son sin esponjamiento, solo bajo la huella, y no incluyen zanjas ni zapatas. La vivienda no '
        'apoya en un terreno plano: el norte queda en desmonte y el sur, hasta 2,55 m por debajo del forjado. Por eso '
        'se propone cimentar en plataformas.')

# ---------- 3. Plataformas ----------
titulo('3. Plataformas de cimentación', True)
parrafo('En lugar de un vaciado único, se ha dividido el terreno en nueve plataformas horizontales, más la de los '
        'patios, que siguen la pendiente natural: de 516,00 al norte a 509,85 en la piscina (plano EST_01). En cada '
        'una se indica su cota y el desmonte o el relleno necesarios desde el terreno natural.')
figura('fig2_est01.jpg', 12.5, 'Figura 2. Plataformas de movimiento de tierras, con el desmonte (EX) y el relleno (R) '
       'de cada zona. Plano EST_01.')
tabla(['Plataforma', 'Cota', 'Dónde', 'Desmonte o relleno'], [
    ['1', '516,00', 'Al norte de la casa, extremo oeste', 'Sin desmonte'],
    ['2', '515,50 y 514,70, por confirmar', 'Franja al norte de la fila norte', 'Desmonte de 0,3 a 1,0 m'],
    ['Patios', '514,70', 'Patios entre volúmenes',
     'Desmonte de 0,7 a 1,3 m en los dos del norte; relleno de 0,2 a 1,7 m en los tres del sur'],
    ['3', '514,30', 'Fila norte de la vivienda', 'Desmonte de 0,2 a 1,7 m'],
    ['9', '514,90', 'Al este del gimnasio', 'Relleno de 0,4 m'],
    ['4', '513,00', 'Fila sur de la vivienda', 'Desmonte de 0,1 a 2,0 m'],
    ['5', '512,10', 'Esquina suroeste', 'Desmonte de 0,1 a 0,9 m'],
    ['6', '511,45', 'Sótano, terraza de la piscina y explanada al norte del garaje', 'Desmonte de 0,6 a 2,55 m'],
    ['7', '510,50', 'Al oeste de la piscina', 'Relleno de 1,1 m'],
    ['8', '509,85', 'Vaso de la piscina', '—'],
], [2.2, 3.4, 6.2, 5.2])
parrafo('En la fila norte, donde el terreno firme queda alto, la plataforma la fija el forjado: 514,30 es la cara '
        'inferior (514,60) menos los 30 cm de cámara mínima. Donde el terreno baja, las plataformas bajan con él: '
        '513,00 en la fila sur y 512,10 en la esquina suroeste. La cota de apoyo de cada zapata la fija el estudio '
        'geotécnico (apartado 5).')

# ---------- 4. Estructura ----------
titulo('4. Estructura portante: de pilares a muros de carga', True)
parrafo('Se propone que la vivienda apoye en muros de carga de ladrillo tosco de un pie, de 24 cm, en las fachadas y '
        'en las líneas de muro interiores del proyecto (plano EST_03). Con ello desaparecen los pilares y las vigas de '
        'hormigón de las alas de dormitorios y de servicio.')
figura('fig3_est03pb.jpg', ANCHO, 'Figura 3. Estructura de planta baja: muros de carga (M.C. 24 cm), muros de hormigón '
       'armado (M. H.A.) y forjado de placa alveolar. Plano EST_03.')
parrafo('**El proyecto.** La memoria describe pilares de hormigón armado rectangulares y circulares, pilares '
        'metálicos, vigas de hormigón planas y descolgadas y vigas metálicas (apartados 2.1.2.1 y 2.2.3). Los planos de '
        'estructura numeran 62 pilares, de P1 a P62. La licitación mide 17,81 m³ de hormigón en pilares (03.06) y '
        '31,98 m³ en vigas (04.06).')
parrafo('**La propuesta.**').paragraph_format.keep_with_next = True
vineta('Muros de carga de 24 cm en la vivienda, sobre los que apoya el forjado sanitario de placa alveolar 20+5. La '
       'placa alveolar es una losa prefabricada de hormigón aligerada con huecos a lo largo.')
vineta('Muros de hormigón armado en el perímetro del sótano, que soportan también el forjado de placa alveolar sobre '
       'el garaje y el gimnasio.')
vineta('En el bloque del salón y del sótano (ejes 9 a 13) se mantienen pilares, entre ellos P30, P31, P42, P43, P60 y '
       'P61, con zapata aislada en el sótano.')
parrafo('Una misma hoja de ladrillo hace de estructura y de fachada, y desaparecen los encofrados de pilares y vigas en '
        'la mayor parte de la casa. A cambio, los muros de carga fijan la distribución: cualquier hueco nuevo en esas '
        'líneas tendrá que pasar por el cálculo, y los dinteles de los huecos grandes están sin definir.')

# ---------- 5. Cimentación ----------
titulo('5. Cimentación corrida bajo los muros', True)
parrafo('Se propone apoyar los muros de carga en zapatas corridas, es decir, zapatas continuas a lo largo de todo el '
        'muro. Sustituyen a las zapatas aisladas bajo cada pilar y a las vigas de atado del proyecto (plano EST_02).')
figura('fig4_est02.jpg', 15.0, 'Figura 4. Cimentación: zapatas corridas, soleras del sótano y de la terraza, y '
       'desmontes y rellenos bajo la vivienda. Plano EST_02.')
tabla(['Tipo', 'Ancho × canto', 'Bajo qué'], [
    ['Z.C. I', '60 × 50 cm', 'Muros de carga de 24 cm: fachadas y casi todos los muros interiores'],
    ['Z.C. II', '40 × 50 cm', 'Tres tramos de muro en el extremo oeste (ejes 1 y 3)'],
    ['Z.C. III', '130 × 50 cm', 'Muros de hormigón armado del sótano'],
], [2.2, 3.0, 11.8])
parrafo('Los pilares que se mantienen en el sótano conservan su zapata aislada. En el proyecto, la cimentación es de '
        'zapatas y losas de hormigón armado con vigas de atado (memoria, 2.2.1); la licitación mide 123,03 m³ de '
        'zapatas y zanjas (03.03) y 42,37 m³ de vigas de cimentación (03.04).')
parrafo('**Cota de apoyo.** Cada zapata apoya 0,60 m por debajo del terreno natural, redondeando hacia abajo en '
        'escalones de 0,50 m (plano EST_00, figura 2). A esa profundidad el estudio geotécnico encuentra la unidad IIa, '
        'con 3,0 kp/cm² de tensión admisible en los cuatro ensayos (tablas 5 y 10).')
parrafo('Así, en la vivienda, el apoyo va de 514,30 en el norte a 511,00–511,50 en el suroeste, y el muro entre la '
        'zapata y la cara inferior del forjado mide de 0,30 a 3,60 m. Donde el terreno firme queda por encima de '
        '514,30, manda el forjado y la zapata se coloca bajo la cámara. En el sótano, la zapata apoya bajo la '
        'excavación, como en el proyecto (cara superior de la cimentación a 511,15).')
figura('fig5_apoyo.jpg', ANCHO, 'Figura 5. Cota orientativa de apoyo de la zapata corrida en la vivienda. Plano '
       'EST_00, figura 2.')
parrafo('El geotécnico pide apoyar toda la cimentación en el mismo nivel competente, para evitar asientos '
        'diferenciales (apartado 6.1.1). Las zapatas escalonadas cumplen esa condición si cada escalón llega a la '
        'unidad IIa. Estas cotas son orientativas: la posición de los sondeos y el espesor de la unidad IIa se '
        'confirmarán con el geotécnico.')

# ---------- 6. Suelos ----------
titulo('6. Suelos: forjado sanitario en la vivienda y solera en el sótano')
parrafo('Se mantiene el forjado sanitario ventilado en la planta baja. En el sótano y en la terraza, hasta la línea de '
        'la piscina, se propone una solera de hormigón sobre encachado, que es una capa de grava; la grava es '
        'autocompactante y no necesita compactarse (planos '
        'EST_02 y EST_03).')
tabla(['Zona', 'Proyecto', 'Propuesta'], [
    ['Planta baja', 'Forjado sanitario autoportante 25+5, de viguetas y bovedilla cerámica',
     'Forjado sanitario de placa alveolar 20+5 sobre los muros de carga'],
    ['Garaje', 'Forjado sanitario, cara superior a −3,25',
     'Encachado de grava de 10 cm y solera de hormigón de 15 cm'],
    ['Gimnasio, instalaciones y terraza hasta la piscina', 'Forjado sanitario, cara superior a −3,25',
     'Encachado de grava de 15 cm y solera de hormigón de 10 cm'],
], [4.4, 6.0, 6.6])
parrafo('A los lados del vaso de la piscina, el plano EST_02 indica relleno de grava o zahorra con solera de hormigón. '
        'Los suelos acabados no cambian: 515,00 en planta baja y 511,85 en el sótano.')
parrafo('**Qué supone la solera.**').paragraph_format.keep_with_next = True
vineta('Desaparece la cámara bajo el sótano, de unos 0,85 m en el detalle DET-01 del proyecto. El colector de '
       'saneamiento que ese detalle dibuja dentro de la cámara pasa a ir enterrado bajo la solera.')
vineta('Toledo está en zona II de radón (DB HS 6, apéndice B). Sin cámara ventilada, el DB HS 6 exige una barrera y, '
       'además, un espacio de contención ventilado o la despresurización del terreno, que consiste en extraer el aire '
       'de debajo de la solera para que el gas no entre (apartados 2.1 y 3.1 a 3.3). El encachado puede servir para '
       'despresurizar, con tubos perforados y salida al exterior. El sistema está por definir.')

# ---------- 7. Acceso y contención ----------
titulo('7. Acceso al garaje y muros de contención')
parrafo('Del estudio del terreno se sugiere llegar al garaje por una explanada a la cota del sótano, delante de su '
        'fachada norte, y ajustar los muros de contención a los saltos entre plataformas. Esta parte está en estudio '
        'y se desarrollará en un plano propio.')
parrafo('**El proyecto.** El garaje, de 68,04 m², tiene dos puertas en la fachada norte y su suelo está a 511,85. El '
        'acceso rodado llega por el norte, junto a un muro de contención que sale de la esquina noroeste del garaje y '
        'corona a 516,10. Los muros del sótano son de hormigón armado de 30 cm (memoria, 2.2.2).')
parrafo('**La propuesta** (plano EST_01).').paragraph_format.keep_with_next = True
vineta('La plataforma 6 (511,45) se prolonga al norte del garaje, con un desmonte de 0,6 a 2,55 m. Es la explanada de '
       'llegada.')
vineta('Al oeste de la explanada, el plano dibuja bandas en pendiente que bajan desde las plataformas 1 y 2 (516,00 a '
       '514,70), al norte de la casa. Otra banda en pendiente cierra la explanada por el este.')
vineta('Al este del gimnasio, la plataforma 9 queda a 514,90, unos 3 m por encima del suelo del sótano. El muro de '
       'hormigón de esa cara contiene ese salto.')
vineta('Los muros de hormigón del perímetro enterrado del sótano apoyan en zapata corrida de 130 × 50 cm (plano '
       'EST_02).')
parrafo('Faltan por fijar el trazado y la pendiente del acceso, y la altura, la longitud y el tipo de cada muro de '
        'contención: de hormigón o resuelto con talud.')

# ---------- 8. Fachada ----------
titulo('8. Fachada: el muro de carga es la fachada')
parrafo('Se propone que la fachada sea el propio muro de carga: una hoja de ladrillo tosco de un pie, con monocapa por '
        'fuera y el aislamiento por dentro (ficha 02 B). La transmitancia del paño es la del proyecto, '
        'U = 0,27 W/m²K.')
tabla(['Capa, de fuera a dentro', 'Espesor'], [
    ['Mortero monocapa', '15 mm'],
    ['Ladrillo tosco de un pie, portante, a tizón y trabado (fb 10 N/mm²)', '233 mm'],
    ['Enfoscado de cemento por la cara interior', '15 mm'],
    ['EPS blanco (λ 0,036 W/mK), pegado al enfoscado', '100 mm'],
    ['Trasdosado de ladrillo de gran formato 70 × 50 × 7, machihembrado', '67 mm'],
    ['Guarnecido y enlucido de yeso', '15 mm'],
    ['Total', '445 mm'],
], [13.5, 3.5], col0_negrita=False, ultima_negrita=True)
parrafo('En el proyecto, la fachada es una estructura de hormigón con dos hojas: medio pie revestido, lana de roca de '
        '100 mm, cámara, tabique hueco y yeso. En los planos del proyecto, las fachadas largas miden 450 mm.')
parrafo('**Qué se gana.** El monocapa va directo sobre el ladrillo, sin SATE (aislamiento térmico por el exterior). La '
        'hoja de un pie cumple la condición C2 del DB HS 1 que declara la memoria; la de medio pie del proyecto no la '
        'cumple. El trasdosado protege el aislamiento.')
parrafo('**A tener en cuenta.** La U de 0,27 se ha calculado con los ladrillos de Cerámica Millas y un EPS de '
        'λ 0,036; con λ 0,038 sube a 0,28. Los muros de carga interiores son de la misma fábrica de un pie, con '
        'acabado conforme a proyecto.')

# ---------- 9. Pendiente ----------
titulo('9. Pendiente de cálculo y de decisión')
parrafo('La primera decisión es si se desarrolla el sistema de muros de carga; el resto depende de ella.')
tabla(['Cuestión', 'Qué falta', 'Quién'], [
    ['Sistema de muros de carga', 'Visto bueno para desarrollarlo', 'Arquitecto y promotores'],
    ['Cálculo estructural', 'Muros, forjados y zapatas, con los pilares que se mantienen y los dinteles de los huecos '
     'grandes', 'Arquitecto'],
    ['Cota de apoyo escalonada', 'Confirmar la posición de los sondeos y el espesor de la unidad IIa',
     'Arquitecto, con el geotécnico'],
    ['Terreno', 'Taquimetría antes del replanteo: el modelo tiene ±0,15–0,20 m de precisión', 'Constructora'],
    ['Plataforma 2', 'Fijar sus cotas: 515,50 y 514,70 están sin cerrar', 'Arquitecto'],
    ['Acceso al garaje y muros de contención', 'Trazado, pendiente y tipo de cada muro', 'Arquitecto'],
    ['Solera del sótano', 'Sistema frente al radón', 'Arquitecto'],
    ['Medición y coste', 'Medir y comparar con la licitación cuando el esquema esté cerrado', 'Constructora'],
], [4.4, 8.8, 3.8])

# ---------- 10. Referencias ----------
titulo('10. Documentos de referencia')
doc.add_paragraph('Propuesta (noviembre de 2026)', style='Heading 2')
vineta('Esquema estructural: EST_00 Estudio cimentación – terreno; EST_01 Movimiento de tierras – plataformas; EST_02 '
       'Cimentación; EST_03 Estructura planta baja.')
vineta('Modelo BIM del estudio del terreno, del que sale el plano EST_00.')
vineta('Ficha 02 B, Fachada: muro de carga con aislamiento por el interior.')
doc.add_paragraph('Proyecto básico y de ejecución (febrero de 2026), de <Arquitectos redactores>, '
                  'arquitectos', style='Heading 2')
vineta('Memoria: solución estructural (2.1.2.1), cimentación, contención y estructura (2.2).')
vineta('Planos de estructura, planta bajo rasante y detalle constructivo DET-01.')
vineta('Mediciones de licitación de junio de 2026: partidas 01.02, 03.03, 03.04, 03.06 y 04.06.')
doc.add_paragraph('Otros', style='Heading 2')
vineta('Estudio geotécnico 017-26: tablas 5 y 10 y apartado 6.1.')
vineta('CTE DB HS 6, Protección frente a la exposición al radón (Real Decreto 732/2019).')

doc.core_properties.title = 'Propuesta alternativa de estructura, cimentación y fachada'
doc.core_properties.subject = 'Cigarral Montealegre, Toledo'
doc.core_properties.author = 'MIJEBAN'
doc.save(SALIDA)

# comprobación: no debe quedar el nombre de la constructora en el cuerpo ni la cubierta
texto = '\n'.join(p.text for p in doc.paragraphs) + '\n'.join(c.text for t in doc.tables for r in t.rows for c in r.cells)
cuerpo = texto.replace('Emite\nMIJEBAN', '')
for prohibido in ('nosotros', 'Pedimos', 'propone MIJEBAN', 'MIJEBAN propone', 'cubierta', 'Cubierta', 'madera',
                  '15+5', 'pérgola'):
    assert prohibido not in cuerpo, prohibido
print('MIJEBAN en el cuerpo:', cuerpo.count('MIJEBAN'), '(solo debe estar en «Emite»)')
print('guardado', SALIDA)
