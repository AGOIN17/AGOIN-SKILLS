---
name: soluciones-alternativas-mijeban
description: "[PROYECTO · ESTILO] Cómo prepara AGOIN, para la constructora MIJEBAN, las «soluciones alternativas» a un proyecto de otro estudio: fichas A4 por sistema constructivo (fachada, cubierta, suelos) dibujadas en DWG con axonometría y sección, informes en Word y PDF para arquitecto y promotor, y mediciones con BC3 de las alternativas. Recoge las reglas que fijó el usuario (redacción impersonal, el cálculo es del arquitecto, carpetas y versiones en H, informes por lotes), el método técnico (AutoCAD LT con accoreconsole, edición de DXF con ezdxf, axonometría 3D con caras ocultas, python-docx, limpiar rótulos de figuras) y los scripts del primer caso, Cigarral Montealegre (Toledo). Úsala cuando trabajes para MIJEBAN o para otra constructora, cuando haya que hacer o cambiar una ficha de solución alternativa, un informe para arquitecto y promotor o una medición de alternativas, y al retomar Cigarral Montealegre desde cualquier carpeta."
metadata:
  etiquetas: "PROYECTO · ESTILO"
---

# Soluciones alternativas para una constructora (MIJEBAN)

**El encargo tipo.** MIJEBAN es una constructora; su dueño es el jefe del usuario. AGOIN prepara para ella propuestas que cambian sistemas constructivos de un proyecto ajeno, para abaratar o simplificar la obra. Se entregan fichas por sistema, informes para el arquitecto redactor y los promotores, y mediciones sin precios. El primer caso fue **Cigarral Montealegre** (Toledo, noviembre de 2026).

**Qué hay en esta skill.**

| Archivo | Para qué |
|---|---|
| `references/metodo-fichas.md` | Fichas A4: maqueta, estilo gráfico, DWG con accoreconsole, axonometría 3D, sección, textos |
| `references/metodo-informes.md` | Informes Word + PDF para arquitecto y promotor, y limpieza de figuras |
| `references/metodo-mediciones-alternativas.md` | Medir desde los DWG, líneas de medición, BC3 conjunto y comprobador |
| `scripts/` y `scripts/LEEME.md` | Los 110 scripts de la sesión (generadores de fichas, informe y mediciones), con índice |
| `assets/PLANTILLA FICHA A4.dwg` | Plantilla editable de la ficha (presentación FICHA-A4) |

Los datos y las notas del caso Cigarral Montealegre (texto de la memoria y del geotécnico, licitación, precios, nombres) no se publican en el repositorio. Están en la copia local de esta skill del equipo donde se hizo, en `references/cigarral-montealegre/`, y en la carpeta del proyecto.

Los scripts llevan rutas absolutas a la carpeta temporal de la sesión de Cigarral, que ya no existe. En los del informe, los promotores y los arquitectos redactores van como «<Promotores>» y «<Arquitectos redactores>»: pon los de la obra. Antes de reutilizarlos, cambia las rutas y lee su cabecera.

## Reglas del usuario (con su porqué)

**Carpetas y entregas**
- En el proyecto solo hay tres carpetas base: la que se envió a las constructoras (no se toca), la de auditoría y `SOLUCIONES ALTERNATIVAS`, con una subcarpeta por sistema. En esta última va **solo el documento final**: nada de pruebas, imágenes sueltas ni extractos. Los archivos de trabajo van a la carpeta temporal de la sesión. El usuario no quiere «mil carpetas» ni «multiplicidad de archivos».
- Los informes en Word y PDF van a `SOLUCIONES ALTERNATIVAS\DOCUMENTOS\`, con el nombre `AAMMDD_INFORME <TEMA>`.
- Cuando un documento sustituye a otro, el anterior pasa a una subcarpeta `H` de la misma carpeta, con la versión como sufijo («… v5»). Antes de moverlo, comprueba con un hash que es tu última versión y que nadie lo ha editado.
- «Actualiza» o «sustituye» quiere decir guardar en la carpeta en ese mismo paso. Si el encargo es nuevo y su formato no está acordado, enséñalo primero en el chat.
- Los originales no se tocan, tampoco las láminas del usuario: se trabaja sobre copias. No se toca el AutoCAD LT que el usuario tiene abierto: se usa `accoreconsole` sobre copias.
- No se envía nada a terceros sin autorización.

**Redacción de informes y fichas para el arquitecto y los promotores**
- **Impersonal:** «se propone sustituir», «se ha medido», «se ha comprobado». Nunca «MIJEBAN propone», «pedimos» ni «nosotros». MIJEBAN solo aparece como emisor, en la cabecera.
- **El cálculo estructural es del arquitecto, no de la constructora.** En las tablas de pendientes, el cálculo y las decisiones técnicas van a «Arquitecto»; la constructora solo hace taquimetría y medición. El porqué: el documento sale de la constructora hacia terceros, y asumir el cálculo traslada una responsabilidad que no es suya.
- **Cabecera:** promotores; arquitectos redactores, que son los del proyecto; «Técnicos redactores de la propuesta alternativa: Técnicos MIJEBAN – AGOIN»; fecha y estado («Propuesta. Pendiente del cálculo estructural, que corresponde al arquitecto, y de su aprobación»).
- **Nunca presentes una propuesta como aprobada.** Las fichas llevan el sello PROPUESTA.
- **No enseñes lo que no está listo.** La propuesta de cubierta se quitó del informe por eso.
- **Le gustó esta frase:** «Las cifras de excavación, relleno y coste se darán con la medición, cuando el esquema esté cerrado.»
- **Informes por lotes** (2026-11-10). El de estructura se llama «Primer lote: movimientos de tierra, cimentación, estructuras». Lo que no es del lote se queda fuera; la fachada salió de ese informe.
- **Muros portantes:** «muro de carga», sin material (ni «ladrillo tosco», ni «un pie», ni «24 cm»). **Forjados sin espesor** (ni 20+5 ni 25+5). Si las figuras sacadas de las láminas rotulan espesores, se quitan del recorte y el pie de figura lo dice.
- **No añadas avisos del tipo «hay que rehacer la justificación del DB HS 1 / DB HE»**: el usuario los quitó. El aviso del radón (DB HS 6) sí se quedó, porque cambia la solución.
- **Encachado:** la grava es autocompactante y no se compacta. No escribas «grava compactada».
- **Espesores del proyecto:** se leen en los planos **y** en el detalle, no solo en la memoria. Si no coinciden, se avisa de la discrepancia.
- **En la fachada no pongas** «el aislamiento se corta en cada forjado / puente térmico» ni comparaciones del tipo «el muro es 44 mm más grueso». Para los muros interiores: «acabado conforme a proyecto».
- Si el usuario pide una ficha «que no se llame alternativa», quita «alternativa» de la cabecera y del nombre del archivo, y usa «La propuesta» y «Propuesta» en los textos. «SOLUCIONES ALTERNATIVAS», el nombre de la serie, se mantiene.

**Mediciones**
- «Comprueba siempre la línea de medición»: en cada regeneración, una comprobación automática de cada línea, que para la generación si falla (detalle en `references/metodo-mediciones-alternativas.md`).
- Criterio de agrupación que aceptó el usuario: se juntan las partidas del mismo oficio, material y unidad; lo pequeño que nadie oferta suelto va como «incluso» dentro del paquete; van aparte las piezas lineales con precio propio y lo que cambia frente al proyecto. La estructura de madera de la cubierta quedó fuera de las mediciones de alternativas.

**Fichas (estilo pedido por el usuario)**
- A4 vertical «con aire de revista», un solo color de acento (RGB 7,87,72), dibujos en grises y que todo se lea impreso. Detalle en `references/metodo-fichas.md`.
- Titular = nombre técnico de la solución («Muro de carga con aislamiento por el interior»), con el tipo debajo en pequeño. Pies de los dibujos sin escala y alineados con el borde del dibujo.
- Los huecos de las piezas se dibujan como un corte real, con la pared interior en tres tonos. Las piezas trabadas a media pieza: el centro de cada una sobre la llaga de abajo.

## Herramientas de este equipo (Windows, oficina de AGOIN)

- **No hay Node:** los Word se hacen con python-docx (1.2.0), no con docx-js.
- **PDF desde Word:** Word 2013 por COM, `ExportAsFixedFormat(ruta, 17)`. Abre tu propia instancia y ciérrala solo si `Documents.Count == 0`.
- **AutoCAD LT 2023 sí trae `accoreconsole.exe`**, en `C:\Program Files\Autodesk\AutoCAD LT 2023\`. Sirve para pasar de DWG a DXF y al revés, y para trazar a PDF sin tocar el AutoCAD del usuario (`references/metodo-fichas.md`).
- **Python:** ezdxf (con `ezdxf.fonts` para medir textos), PyMuPDF (fitz), shapely, Pillow y fontTools. No hay scipy.
- **Los paquetes están en el site de usuario**, así que `python -I` no los encuentra. Para leer descargas, guárdalas en una carpeta propia y ejecuta desde otra carpeta, sin `-I`.
- **Fuente de las fichas e informes:** Century Gothic (`C:\Windows\Fonts\GOTHIC.TTF`). Tiene «−», «–», «λ», «²», «×» y «≈».

## Normativa ya comprobada en la fuente oficial

- **DB HS 1, 2.3.2, condición C2** (hoja principal de espesor alto): «1 pie de ladrillo cerámico… o 24 cm de bloque cerámico, bloque de hormigón o piedra natural». Leído en `codigotecnico.org/pdf/Documentos/HS/DBHS.pdf`, p. 22–23.
- **DB HS 6, radón.** Toledo está en la zona 2: lo dice el RD 732/2019 (BOE-A-2019-18528, p. 140632). En esa zona hace falta una barrera (3.1) más un espacio de contención ventilado (3.2) o despresurización del terreno (3.3).
  - Una lámina de 2 mm o más con D < 10⁻¹¹ m²/s vale sin calcularla (3.1.1.2).
  - Las aberturas de ventilación de la cámara suman al menos 10 cm² por metro de perímetro (3.2.3).

## Al empezar en otra obra

1. Pregunta qué sistemas se van a proponer y en qué orden, y quién firma el proyecto (arquitectos y promotores de la cabecera).
2. Crea solo las carpetas que hagan falta, siguiendo las reglas de arriba.
3. Reutiliza la plantilla `assets/PLANTILLA FICHA A4.dwg` y los generadores de `scripts/`, cambiando rutas y datos.
4. Saca a texto, por páginas, la memoria y el geotécnico de la nueva obra (`scripts/est/buscar.py` y `scripts/est/pag.py` sirven para buscar en ellos) y extrae la licitación con `scripts/lic_bc3.py`.

Relacionadas: `agoin-forma-de-trabajar`, `informes-tecnicos`, `mediciones-presupuesto`, `libro-estilo-agoin`, `planos-laminas`, `automatizar-programas-windows`, `comprobar-normativa`.
