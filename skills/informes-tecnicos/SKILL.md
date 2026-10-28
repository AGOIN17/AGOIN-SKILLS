---
name: informes-tecnicos
description: "[ESTILO] Cómo redactar y generar informes y documentos técnicos de AGOIN en PDF para el usuario o para terceros (estructurista, promotora, constructoras, administración). Sirve para comprobaciones, propuestas, comparativas de soluciones, hojas de decisión, cambios en memoria, documentos de dudas y ofertas. Exige conclusión primero, cumple / no cumple / quizás, procedencia de cada dato y figura, lo que no cubre, español llano, imagen corporativa y no presentar nada como aprobado; incluye trampas al generar el PDF. Úsala al preparar cualquier informe, nota técnica, comparativa, memoria modificada o documento para que alguien decida."
metadata:
  etiquetas: "ESTILO"
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
- **Las cifras y los veredictos del texto salen de las variables del cálculo,** no se escriben a mano. Tras recalcular, vuelve a leer las frases de conclusión que estaban fijas: quedó escrito «ya cumplía» cuando ya no era cierto, y un armado escrito a mano no casaba con el cálculo.
- **Comparativas para decidir.** Cada opción lleva:
  - plano o esquema y detalle, **a escala** (por ejemplo, dos huecos de ascensor con la huella de una silla de ruedas en discontinua);
  - costes segregados, **sin lo que es común a las opciones**, y la diferencia también en €/m² construido; si van a terceros, sin códigos ni precios unitarios de bases con licencia (ver `mediciones-presupuesto`);
  - lo que no es dinero: si cambia la fachada visada, si afecta a la licencia en un casco histórico, si el detalle de otra obra no se puede trasladar tal cual;
  - ventajas e inconvenientes;
  - el criterio para elegir;
  - la recomendación.
  - Una comparativa así (canalón oculto) la recibió el usuario con un «me encanta».
- **Hojas de decisión, de propuestas, de dudas para dibujar a mano y planos de trabajo para el cliente:** son hojas distintas, cada una con su formato. Están en la skill `decisiones-cliente`. Lo que el usuario tiene que comprobar va resaltado en amarillo.
- **Documento de dudas para resolver con otra persona o con otro asistente:** cada duda debe entenderse sola (contexto, opciones, recomendación y qué cambia según la respuesta), porque quien lo lea no tiene esta conversación. Termina con una plantilla de respuestas (`AV-027: …`, `F-1: añadir / no`) para que la devuelvan rellena y se aplique sin interpretarla.
- **Memoria modificada:**
  - si el original es un PDF visado que no se puede editar, un documento de cambios apartado por apartado y plano por plano: «DICE HOY» (en rojo), «DEBE DECIR» (en verde) y «POR QUÉ», con el texto de sustitución listo para pegar y el origen de cada cambio (contradicción del proyecto, exigencia normativa comprobada o decisión del usuario, con fecha);
  - si se puede editar, una versión limpia;
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
  - verde corporativo RGB(6,87,72), #065748, en ofertas, informes y portadas (en un PDF del estudio se midió 7,87,72). No es el verde de dibujo de los planos (0,128,64): ver `libro-estilo-agoin`;
  - las plantillas oficiales de la administración conservan su propio formato;
  - fotos reales en los dossiers.
- **Antes de entregar:**
  - abre el PDF y mira cada página renderizada: fuentes, tablas cortadas, imágenes;
  - si hay una revisión independiente en marcha, no lo entregues hasta que termine.
- **Enviar a terceros solo con autorización expresa.**

## Generar el PDF

- **HTML a PDF:** Edge sin ventana, `msedge --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=salida.pdf file:///ruta.html`. Añade `--allow-file-access-from-files` si carga imágenes locales. Revisa los saltos de página y las tablas partidas en el resultado.
  - Edge puede terminar antes de que el PDF exista: espera a que aparezca el archivo y a que su tamaño deje de cambiar antes de unirlo o moverlo.
- **PDF con PyMuPDF:**
  - `insert_textbox` no escribe nada, y no avisa, si el rectángulo es pequeño: coloca el texto con `insert_text` en su línea base;
  - las fuentes base-14 no tienen «€» ni la raya «—»: incrusta una TTF (por ejemplo `C:/Windows/Fonts/arial.ttf`) y mide con `fitz.Font(fontfile=…).text_length`;
  - antes de entregar, busca glifos rotos (recuadros en lugar de caracteres): salió uno en lugar de «10⁻¹¹»;
  - reutiliza un módulo propio de maquetación (línea, párrafo, tabla) entre documentos del mismo tipo.
- **Hojas A3 con el aspecto de los planos** (comparativas, remates): matplotlib con el estilo de `libro-estilo-agoin` (§9).
- **Unir el informe y los anejos:** con PyMuPDF (`insert_pdf`). Cuenta las páginas y dilo.
- **RTF de otros programas con varias tablas de fuentes pegadas:** únelas antes de pasar a PDF con `calculo-estructural/scripts/rtf_unir_tablas.py`, o el texto saldrá en letras griegas.
- **Word a PDF:** `ExportAsFixedFormat(ruta, 17)`.
- **No recomiendes Adobe.** El estudio se está pasando a PDF-XChange y se quitó Acrobat a propósito.
