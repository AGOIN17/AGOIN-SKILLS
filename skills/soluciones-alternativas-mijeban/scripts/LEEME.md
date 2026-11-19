# Scripts de Cigarral Montealegre (sesión del 05 al 10/11/2026)

Son copias literales de la carpeta temporal de la sesión, con su misma estructura de subcarpetas.

- **Rutas.** Muchos llevan rutas absolutas a `C:\Users\usuario\AppData\Local\Temp\claude\...\scratchpad`, que ya no existe, o rutas relativas a esa carpeta (`f7/…`, `med/…`). Antes de usarlos, cambia las rutas y lee la cabecera.
- **Codificación.** Algunos van en UTF-8 con BOM; Python los ejecuta igual.
- **Cómo se ejecutan.** Desde una carpeta propia y sin `-I`, porque los paquetes están en el site de usuario.

## Fichas (DWG/DXF con ezdxf)

| Script | Qué hace |
|---|---|
| `f8/ficha02_termo.py` | **Generador completo de la ficha 02 con Termocerec 24.** A partir del DXF de la 02 B v3: rehace la axonometría 3D (cajas por capa, caras ocultas, bloque con huecos en tres tonos, machihembrado, traba, testa cortada), la sección (hiladas con huecos cortados), cotas, números y ventana; recalcula la U; reescribe y recoloca los textos; comprueba que no se pisan ni quedan palabras prohibidas. Uso: `python ficha02_termo.py f7/f02b_v3.dxf f8/ficha02.dxf` |
| `f8/p8.scr` | Guion de accoreconsole: SAVEAS 2018 y trazado de FICHA-A4 a PDF |
| `f8/insp.py`, `f8/dump_ps.py`, `f8/dump_sec.py`, `f8/axo_lin.py`, `f8/clasifica.py` | Inspección de una ficha: ventanas, textos del papel con su handle, entidades de la sección, contornos de la axonometría y sombreados clasificados por capa y cara |
| `f02b_v2.py`, `f02b_v3.py`, `f02b_modelo.py` | Cambios de texto por handle en la ficha 02 B (ejemplo mínimo de «editar sin generador») |
| `ficha01.py`, `regen01.ps1` | Generador de la ficha 01 de suelos (forjado con nervio y bovedilla, capas, tetones), y su regeneración DXF → DWG → PDF → PNG |
| `ficha03_v5.py`, `ficha03_v6.py`, `hacer_v6.py`, `regen05.ps1`, `regen06.ps1` | Generadores de la ficha 03 de cubierta (alero con peto, durmiente, banda) |
| `editar_axo.py`, `editar_v4b.py`, `editar_v4_seccion.py`, `axo_dump.py`, `nuevos_v4.py` | Retoques de la axonometría y la sección de la ficha 03 v4 (pares y durmiente en 3D, ocultos con shapely) |
| `alero_A.py`, `alero_B.py`, `boceto_alero.py` | Esquemas del alero con matplotlib |
| `ps_dump.py`, `sec_dump.py`, `ref_dump.py`, `ref_capas.py`, `ref_insp.py`, `ver_ref.py`, `trama_insp.py`, `ver_det.py` | Volcados y vistas rápidas de zonas de un DXF (capas, tramas, colores) |
| `prueba_txt.py`, `prueba_txt6.py`, `pie_txt.py`, `chk_cfg.py` | Pruebas de corte de textos con la fuente y de la configuración de trazado |
| `*.scr` en `f1/`, `f4/`, `f5/`, `f6/`, `f7/`, `det/`, `med/`, `est/` | Guiones de DXFOUT y de trazado de cada versión |

## Informe Word + PDF

| Script | Qué hace |
|---|---|
| `informe/informe_docx.py` | Informe «Primer lote» (v6) con python-docx. Uso: `python informe_docx.py <carpeta de figuras> <salida.docx>` |
| `informe/informe_docx_v5.py` | Versión anterior («Esquema estructural», con fachada) |
| `informe/figuras.py` | Recortes de las láminas EST en JPG. Uso: `python figuras.py <pdf> <carpeta>` |
| `informe/fig3_sin_espesores.py` | Quita «20+5cm» y «24 cm» de la figura 3 (redacción de PyMuPDF en memoria) |
| `informe/fig1_sin_espesor.py` | Tapa la nota «25+5 (30 cm)» de la figura 1 (imagen, con Pillow) |

## Mediciones y BC3

| Script | Qué hace |
|---|---|
| `medicion_fachadas.py` | Medición de fachadas desde los DWG, con la comprobación de cada línea, BC3 y PDF A3 |
| `medicion_cubierta.py`, `cub_extraer.py` | Medición de la cubierta (A-03 y E-07) |
| `bc3_conjunto.py` | Une las líneas de fachadas y cubierta en un BC3 sin precios |
| `check_bc3.py` | Comprobador independiente del BC3 |
| `lic_bc3.py`, `lic_buscar.py` | Licitación BC3 → JSON, y búsqueda en ese JSON |
| `med_*.py` | Extracción de vistas y plantas, piloto W1, revisión en planta, piedra, hastiales, carpinterías y etiquetas |
| `med/cotas_pb.py`, `med/recorte_pb.py`, `med/cotas_muro.py` | Grosores de muro en las plantas del proyecto (450 / 400) |
| `det/corte.py`, `det/capas_muro.py`, `det/cotas.py`, `det/zoom_muro.py` | Capas y grosor del muro en el DET-01 |
| `medir.py` | Utilidad de medida |

## Lectura de documentos y normativa

| Script | Qué hace |
|---|---|
| `est/buscar.py`, `est/pag.py` | Buscar y leer por páginas en la memoria o el geotécnico sacados a texto (en el caso Cigarral, `references/cigarral-montealegre/datos/` de la copia local; no está en el repositorio) |
| `est/dxf_txt.py`, `est/capas.py`, `est/recorte*.py` | Textos y recortes de las láminas EST |
| `pdf_buscar.py`, `pdf_pag.py`, `pdf_txt.py` | Buscar, leer y sacar texto de un PDF |
| `boe_toledo.py`, `boe_hs6_texto.py`, `boe_hs6_32.py` | Lectura del RD 732/2019 (zona de radón de Toledo y DB HS 6) |
