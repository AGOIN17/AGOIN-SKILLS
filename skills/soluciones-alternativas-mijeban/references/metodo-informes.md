# Informes para el arquitecto y los promotores (Word + PDF)

Las reglas generales de redacción están en la skill `informes-tecnicos`. Aquí va lo propio de estos informes. Ejemplo completo: `scripts/informe/informe_docx.py` (v6, «Primer lote») y `informe_docx_v5.py`.

## Contenido tipo (informe del primer lote de Cigarral)

- **Cabeza de la primera página:**
  - antetítulo «INFORME · PRIMER LOTE»;
  - título «Primer lote: movimientos de tierra, cimentación, estructuras»;
  - subtítulo con el edificio;
  - tabla de datos: situación, promotores, arquitectos redactores (los del proyecto), técnicos redactores de la propuesta alternativa («Técnicos MIJEBAN – AGOIN»), fecha y estado.
- **1. Resumen:**
  - dos párrafos;
  - tabla de cuatro columnas: elemento, proyecto, propuesta y plano;
  - recuadro «PARA DECIDIR»: al arquitecto, valorar y calcular; a los promotores, el visto bueno; y la frase de las cifras que «se darán con la medición, cuando el esquema esté cerrado».
- **Un apartado por tema, cada uno en página nueva:** topografía con el modelo BIM, plataformas, estructura portante, cimentación, suelos, acceso y contención. Dentro de cada uno, «**El proyecto.**» con sus cifras y fuentes (memoria, planos y partidas de la licitación), y «**La propuesta.**» en viñetas.
- **Pendiente de cálculo y de decisión:** tabla de cuestión, qué falta y quién. El cálculo y lo técnico van al arquitecto; la taquimetría y la medición, a la constructora.
- **Documentos de referencia**, en tres grupos: propuesta, proyecto y otros.
- **Cabecera y pie de página:** «MIJEBAN · SOLUCIONES ALTERNATIVAS» con el lugar a la derecha; «Propuesta pendiente del cálculo estructural del arquitecto» con «Página X de Y».

## Generar el Word con python-docx (no hay Node en este equipo)

- A4 con márgenes de 2 cm, Century Gothic y verde #075748.
- **Títulos con la fuente buena:** borra los atributos `asciiTheme` y `hAnsiTheme` de `rFonts` en los estilos de título. Si no, Word los pinta con la fuente del tema.
- **XML válido:** reordena los hijos de `tblPr`, `tcPr` y `pPr` según el orden del esquema.
- **Tabulador a la derecha en cabecera y pie:** borra antes los tabuladores de los estilos Header y Footer y pon uno a `ANCHO − 0,05` cm.
- **Números de página:** campos PAGE y NUMPAGES construidos con `fldChar`.
- **Funciones útiles:** `runs` (admite `**negrita**`), `parrafo`, `titulo(texto, pagina_nueva)`, `vineta`, `figura(nombre, ancho, pie)`, `tabla(cabecera, filas, anchos)` (comprueba que los anchos suman 17 cm), `recuadro` y `campo`.
- **Comprobación al final del script:**
  - que el cuerpo no contenga ninguna palabra prohibida: «nosotros», «Pedimos», «MIJEBAN propone», «cubierta» (no estaba lista), «tosco», «ladrillo», «un pie», «20+5», «25+5», «EPS»… La lista crece con cada corrección del usuario;
  - que MIJEBAN solo aparezca en la cabecera.

## PDF con Word por COM

```powershell
$w = New-Object -ComObject Word.Application; $w.Visible = $false; $w.DisplayAlerts = 0
$d = $w.Documents.Open($docx, $false, $true); $d.ExportAsFixedFormat($pdf, 17); $d.Close(0)
if ($w.Documents.Count -eq 0) { $w.Quit() }
[void][Runtime.InteropServices.Marshal]::ReleaseComObject($w)
```

Después, renderiza cada página con PyMuPDF y mírala: huecos en blanco, páginas con una sola línea, tablas partidas y títulos solos al pie de una página. Así se corrigieron los saltos de página de la v1 y el apartado 9 de la v6.

## Figuras sacadas de las láminas

- Son recortes del PDF de las láminas con PyMuPDF (`scripts/informe/figuras.py`): página, recorte en fracciones de la página y resolución.
- El pie de cada figura dice de qué plano sale y si se ha retocado.
- **Quitar rótulos que el informe ya no debe decir** (espesores, materiales), sin tocar el PDF original:
  - **Texto vectorial** (`scripts/informe/fig3_sin_espesores.py`):
    - abre el PDF en memoria;
    - busca los caracteres con `get_text('rawdict')`;
    - pon `add_redact_annot(rect, fill=False)` sobre cada uno;
    - aplica `apply_redactions(images=PDF_REDACT_IMAGE_NONE, graphics=PDF_REDACT_LINE_ART_NONE)`, para que no se borren líneas ni imágenes;
    - comprueba con `get_text('words', clip=…)` que no queda nada y renderiza;
    - en Cigarral se quitaron 14 «20+5cm», y los 25 «M.C.24 cm» quedaron en «M.C.». Ojo con el «cm» suelto que queda detrás.
  - **Texto en imagen** (la lámina EST_00 es casi toda imagen): con Pillow, sube las líneas de debajo para tapar la nota y rellena con el color del fondo (`scripts/informe/fig1_sin_espesor.py`). Comprueba el resultado ampliado.
  - Añade al pie «…, sin los rótulos de espesor» o «…, sin la nota del espesor del forjado».

## Guardar

1. Comprueba con un hash que el informe de `DOCUMENTOS\` es tu versión anterior.
2. Muévelo a `DOCUMENTOS\H\` con el sufijo « vN».
3. Copia el nuevo con su nombre (`AAMMDD_INFORME <TEMA>`) y compara los hashes.
4. Windows no admite «:» en los nombres de archivo: «PRIMER LOTE - MOVIMIENTOS DE TIERRA, CIMENTACIÓN, ESTRUCTURAS».
