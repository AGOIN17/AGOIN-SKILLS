---
name: informes-tecnicos
description: "Cómo redactar y generar informes y documentos técnicos de AGOIN en PDF para el usuario o para terceros (estructurista, promotora, constructoras, administración). Sirve para comprobaciones, propuestas, comparativas de soluciones, hojas de decisión, cambios en memoria, documentos de dudas y ofertas. Exige conclusión primero, cumple / no cumple / quizás, procedencia de cada dato y figura, lo que no cubre, español llano, imagen corporativa y no presentar nada como aprobado; incluye trampas al generar el PDF. Úsala al preparar cualquier informe, nota técnica, comparativa, memoria modificada o documento para que alguien decida."
---

# Informes técnicos

## Estructura

1. **Resumen.**
   - La conclusión va en la primera frase: qué cumple, qué no y qué falta decidir.
   - Si hay varios elementos, una tabla: elemento, resultado y por qué, en una línea.
2. **Lo que tiene que mirar quien valida,** en un recuadro aparte («Para el estructurista», «Para decidir»).
3. **Cómo se ha hecho.**
   - Fuentes, con fecha y lámina.
   - Hipótesis y herramientas.
   - Lo que es criterio propio, marcado como tal.
4. **Detalle por elemento.**
5. **Lo que este documento no cubre.**
6. **Ficheros:** dónde está cada cosa y con qué script se regenera.

**Anejos:** los documentos del propio programa (informes, notas, planos), cuando existan.

## Reglas

- **Español llano.** Cada término técnico que el lector puede no conocer se explica la primera vez que aparece.
- **Estados claros:** propuesto, pendiente de validar, o aprobado por quién y cuándo. Nunca escribas «aprobado» si no lo está.
- **Procedencia:**
  - di qué figuras salen del programa y cuáles has dibujado tú;
  - di con qué precisión encaja una imagen de fondo.
- **Números con unidades y con su fuente.** Ninguna cifra sin decir de dónde sale. Ninguna cifra exagerada: «a menos de un centímetro», no «casi al milímetro».
- **Comparativas para decidir.** Cada opción lleva:
  - plano o esquema y detalle;
  - costes segregados;
  - ventajas e inconvenientes;
  - el criterio para elegir;
  - la recomendación.
- **Hojas de decisión para un cliente:**
  - una hoja (A3) por cuestión;
  - opciones A, B y C con pros, contras y diferencia de coste;
  - la recomendación y casillas para marcar;
  - si se dibuja a mano encima, una cuadrícula.
  - Lo que el usuario tiene que comprobar va resaltado en amarillo.
- **Documento de dudas para resolver con otra persona o con otro asistente:** cada duda debe entenderse sola (contexto, opciones, recomendación y qué cambia según la respuesta), porque quien lo lea no tiene esta conversación.
- **Memoria modificada:**
  - una versión limpia;
  - una versión de revisión con lo nuevo en otro color;
  - la relación de modificaciones;
  - las páginas tocadas, marcadas como «no visadas»;
  - sin reproducir la firma.
- **Ofertas a licitaciones públicas del estudio:**
  - El sobre de criterios de juicio de valor nunca adelanta el precio ni ningún otro criterio que se puntúe con fórmula. En una licitación, las visitas de obra se puntuaban con fórmula, así que ni se mencionaba la palabra «visita».
  - Mira en el pliego (PCAP) qué va en cada sobre.
  - Antes de regenerar, mira si alguien editó a mano la copia local o la del servidor (marcas `[COMPLETAR`).
- **Documentos que el usuario ya ha editado a mano** (un Word): no los regeneres por encima. Edita el archivo o limítate a aconsejar.
- **Nombre de archivo con versión o fecha.** El anterior no se sobrescribe.
- **Imagen corporativa de AGOIN:**
  - verde RGB(6,87,72), #065748, en ofertas, informes y portadas;
  - las plantillas oficiales de la administración conservan su propio formato;
  - fotos reales en los dossiers.
- **Antes de entregar:**
  - abre el PDF y mira cada página renderizada: fuentes, tablas cortadas, imágenes;
  - si hay una revisión independiente en marcha, no lo entregues hasta que termine.
- **Enviar a terceros solo con autorización expresa.**

## Generar el PDF

- **HTML a PDF:** Edge sin ventana, `msedge --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=salida.pdf file:///ruta.html`. Añade `--allow-file-access-from-files` si carga imágenes locales. Revisa los saltos de página y las tablas partidas en el resultado.
- **Unir el informe y los anejos:** con PyMuPDF (`insert_pdf`). Cuenta las páginas y dilo.
- **RTF de otros programas con varias tablas de fuentes pegadas:** únelas antes de pasar a PDF con `calculo-estructural/scripts/rtf_unir_tablas.py`, o el texto saldrá en letras griegas.
- **Word a PDF:** `ExportAsFixedFormat(ruta, 17)`.
- **No recomiendes Adobe.** El estudio se está pasando a PDF-XChange y se quitó Acrobat a propósito.
