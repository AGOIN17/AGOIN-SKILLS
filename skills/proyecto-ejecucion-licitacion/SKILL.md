---
name: proyecto-ejecucion-licitacion
description: "[PLANOS · PROYECTO] Cómo organizar, documentar y revisar un proyecto de ejecución completo para licitar la obra, sobre todo en rehabilitación y patrimonio: juego de planos por oficios con el edificio entero en cada hoja, leyendas redactadas como unidades de obra y con su cantidad, muestrario de materiales con foto, fichas de baños, cocinas, mobiliario y de cada elemento existente a conservar (foto, estado, trabajos), reparaciones por fases, memoria en tres estados (original, actual, reformado), memoria, planos, mediciones y pliego coordinados, y errores que buscar antes de enviar. Sale del análisis de un proyecto ajeno de referencia. Úsala al estructurar el juego de planos o la carpeta de licitación de un proyecto de ejecución, al preparar fichas de baños, cocina, carpinterías o cerrajería existentes, al redactar la memoria de una intervención en un edificio protegido, al revisar un proyecto ajeno o de referencia, y cuando el usuario pida «aprender de este proyecto»."
metadata:
  etiquetas: "PLANOS, PROYECTO"
---

# Proyecto de ejecución para licitar

Lecciones de un proyecto de ejecución de otro estudio que el usuario puso como ejemplo de buen proyecto. Es la conservación y restauración de una vivienda moderna de los años sesenta declarada BIC, preparada para licitar entre constructoras (noviembre de 2025). Lo componen 82 láminas A1, una memoria de 260 páginas, las mediciones con su BC3, un pliego de licitación y un anexo histórico. Se analizó el 03/11/2026.

**Cómo usar esta skill:**
- Lo bueno se copia.
- Lo malo se convierte en una comprobación antes de enviar.
- **Ninguna regla de aquí sale de una corrección del usuario.** Si choca con una indicación suya o con otra skill, manda la otra:
  - `libro-estilo-agoin`: numeración, nombres de archivo, zonas de la hoja, cajetín, textos, etiquetas y fases;
  - `mediciones-presupuesto`: presupuesto ciego, mediciones provisionales y «o similar»;
  - `comprobar-normativa`: citar la norma.
- **El proyecto se cita anonimizado («la referencia»).** Lo ajeno no se identifica en las skills: su pliego exigía confidencialidad.
- El análisis completo, lámina a lámina y con páginas, está en `references/proyecto-referencia-analisis.md`. Léelo si necesitas un ejemplo concreto.

## 1. La carpeta de licitación

- **Cinco partes con nombres claros:** `DOCUMENTACIÓN GRÁFICA`, `MEMORIA`, `MEDICIONES` (PDF y BC3), `PLIEGO LICITACIÓN` y `ANEXO`.
  - **Por qué:** la constructora encuentra cada cosa sin preguntar.
- **Los planos van dos veces:**
  - un PDF unido, con un marcador por lámina;
  - una carpeta con un PDF por lámina.
  - **Por qué:** cada subcontrata recibe solo sus hojas.
  - **Nombre de cada PDF suelto:** la convención de `libro-estilo-agoin`. De la referencia se toman dos ideas:
    - que el orden del juego se vea al listar la carpeta;
    - que archivo, marcador y cajetín lleven el mismo código. En la referencia no coincidían: un archivo «03 DEM 01» era la lámina «CO DEM 01».
- **Un anexo del estado original para la obra:** planos originales escaneados, fotos de época y fotos del estado actual con la fecha en el nombre (`AAAAMMDD_hhmmss.jpg`).
  - En la referencia incluía también fotogramas de una película de la época rodada en la casa.
  - **Por qué:** en una restauración, la constructora y la dirección facultativa tienen que saber cómo era cada cosa para reproducirla.

## 2. Planos por oficios

- **Divide la serie de construcción por oficios, en el orden de la obra.** La referencia los separaba así:
  - demoliciones, muros y tabiques, acabados, solados, falsos techos, rodapié y rodatecho;
  - baños, carpintería interior, cerrajería, carpintería exterior y cocina;
  - forjado sanitario, cubierta y exteriores;
  - después, cada instalación.
  - **Por qué:** cada lámina es el encargo de un oficio, y la constructora la pasa tal cual a su subcontrata.
  - **Numeración:** la de `libro-estilo-agoin` (A.xx, C.xx, IFON…). De la referencia se toma solo la división por oficios dentro de la serie C.
- **Cada lámina muestra el edificio entero, con la planta siempre en la misma posición de la hoja.** La arquitectura va de fondo en gris claro y el oficio en color.
  - **Por qué:** pasando páginas se superponen los oficios, y lo que importa de cada hoja salta a la vista.
- **Divide por oficios, no por zonas, y no fragmentes.** Esto vale para juegos nuevos; si se actualiza un juego visado, manda su organización.
  - Si un oficio no llena una hoja, junta plantas, o junta oficios afines (solados, rodapié y rodatecho en una misma hoja).
  - La referencia tenía 82 láminas para una sola vivienda. Nueve tenían trazo en menos del 3 % de su superficie, casi todas de sótano o cubierta: por ejemplo, la de iluminación de cubierta solo tenía un detalle.
  - Así se cumple «pocas láminas y completas» de `libro-estilo-agoin`.
- **Zonas de la hoja:** las de `libro-estilo-agoin`.
  - Leyenda, en su columna o banda.
  - En la columna de tablas, sobre el cajetín: muestrario de materiales, detalle tipo del oficio (1:5 o 1:10) y notas.
  - Escala gráfica y norte, como dice el libro.
  - **Por qué:** quien abre cualquier hoja encuentra cada cosa en el mismo sitio.
- **Cada línea de la leyenda se redacta como la unidad de obra que representa,** con qué incluye y hasta dónde llega.
  - Ejemplo: «Levantado de solado de gres 20×20 y suelo radiante existente, incluso plastón hasta descubrir el forjado».
  - Distingue «con recuperación» y «sin recuperación» en desmontajes.
  - **Por qué:** cada grafismo del plano corresponde a una partida, y la constructora lo puede leer sin la memoria.
- **Pon la cantidad medida en la leyenda,** con su unidad.
  - Ejemplos: «Rodapié sobre tabique nuevo de pladur — 71,89 m»; «401,82 m de viguetas a reparar».
  - **Por qué:** quien oferta comprueba la medición contra el plano.
  - **Esa cifra sale de la misma medición que el BC3.** Antes de enviar, suma por script la medición de la partida en el BC3 y compárala con la cifra de la leyenda. Una cifra distinta en plano y presupuesto es motivo de reclamación.
- **Muestrario de materiales con foto:** foto de la textura real, código corto y descripción.
  - Ejemplo: «Gres tono marrón 20×20 recibido con mortero adhesivo».
  - Las etiquetas de acabados de las estancias son las de `libro-estilo-agoin` (Sxx, Axx, TExx). De la referencia se copia solo la foto.
- **En la hoja de acabados, tres notas de obra:**
  - se presentarán muestras de todos los acabados a la dirección facultativa para su aprobación;
  - se confirmará en obra el replanteo;
  - cualquier discrepancia entre plano y realidad se consultará con la dirección facultativa.
- **Alzados nombrados por las esquinas de la mosca:** la mosca numera las esquinas del edificio (1, 2, 3, 4) y cada alzado se llama «Alzado 1-2», «Alzado 2-3»…
  - **Por qué:** no hay dudas de qué fachada es en una planta irregular o girada.
- **Estado actual y reformado con la misma estructura de lámina y el mismo cuadro de superficies, fila a fila.**
  - **Por qué:** se comparan pasando la página.
- **Lo existente, en los planos de oficio, con un color por acción** (conservar, sustituir, reproducir).
  - No sustituye la convención de fases de `libro-estilo-agoin` (existente en poché gris, derribo discontinuo, obra nueva marcada) ni las fases de `rehabilitacion-levantamiento`: es una capa más en los planos de oficio.
- **Escribe en el plano de dónde sale lo existente que no se ha comprobado.**
  - Ejemplo: «Geometría y trazado del saneamiento enterrado según los planos del proyecto original».
- **Escribe en el plano lo que queda fuera del alcance.**
  - Ejemplo: «No entra en el alcance: cuadro estándar de piscina».
- **No dejes un plano de licitación «a actualizar por el instalador».** En la referencia, las tres láminas de climatización lo decían.
  - **Por qué:** cada constructora lo interpreta a su manera y los precios dejan de ser comparables.
  - Si no se puede cerrar, trátalo como medición provisional, como dice `mediciones-presupuesto`.

## 3. Fichas

- **Ficha de baño (1:20), una o dos por hoja.** Lleva:
  - planta con el despiece del alicatado;
  - alzado de cada pared, acotado;
  - axonometría en color con los materiales;
  - detalles a 1:5 (encimera con lavabo, toallero);
  - fotos de los aparatos y muestras de los materiales;
  - mosca;
  - un texto con apartados numerados (suelos, paramentos, techo, encimera y lavabo, inodoro, ducha, mueble, accesorios, espejo), cada uno con su producto, acabado y número de unidades.
  - **Producto:** marca y modelo solo si los ha decidido el usuario o el cliente. Si no, producto de referencia «o similar», con prestaciones y marcado como pendiente (ver `decisiones-cliente`). No inventes marcas ni modelos.
  - **Por qué:** con esa hoja se puede pedir precio a un fontanero o a un alicatador sin nada más.
- **Cocina, lavadero y mobiliario a medida:** alzados acotados, axonometría, texto de composición (estructura, baldas, cajones, tiradores, herrajes) y muestras.
  - Una axonometría sola, sin cotas ni texto, no sirve para ofertar. La referencia tenía hojas así.
- **Ficha de cada elemento existente que se conserva o se recupera** (carpintería, armario, celosía, cerrajería). Es lo mejor de la referencia para una rehabilitación.
  - Para lo nuevo sigue valiendo la ficha de carpintería de `libro-estilo-agoin`.
  - La ficha de lo existente lleva:
    - código y nombre;
    - una o dos fotos del estado actual, con la medida principal dibujada sobre la foto;
    - planta o alzado acotado;
    - una tabla con código, descripción, dimensiones, unidades, estado y trabajos a realizar.
  - **El estado** (bueno, regular, malo) solo se pone si lo respalda una inspección o una foto.
  - Ejemplo de trabajos: «Retirar tiradores para lijar y barnizar; rellenar huecos con masilla; pintura esmalte según el proyecto original».
  - **Usa las mismas unidades en el dibujo y en la tabla.** En la referencia, el dibujo acotaba en metros (0,645) y la tabla en milímetros (645 × 2100).
- **Plano de estado de los elementos existentes:** cada código, con el color de lo que se hace.
  - Si son muchos, ponlos en una tabla ordenada por código, con columnas para original o no, acción y ficha. No los pongas en una leyenda larga.
  - En la referencia, la leyenda de carpintería exterior tenía 60 líneas desordenadas (C35 aparecía después de C18) y códigos que se salían de su círculo.
- **Reparación por fases:** secciones a 1:5 de la fase 0 (estado actual) y de cada fase hasta la final, con su texto. Al lado, fotos de la patología. En una nota, las cantidades.
  - Ejemplo: viguetas carbonatadas de un forjado sanitario.
    - Fase 1: retirar el hormigón del fondo hasta descubrir la armadura.
    - Fase 2: pasivante.
    - Fase 3: reponer la sección con mortero de reparación.
  - La solución estructural la valida el estructurista, como dice `calculo-estructural`.
- **Detalles de cubierta:** una leyenda numerada de capas, común a todas las hojas de cubierta, y llamadas con recuadros a los detalles ampliados.
- **Dibuja cada detalle en una sola lámina y remite a ella desde las demás.** En la referencia, el mismo detalle de escaleras estaba en dos láminas: si cambia uno, el otro queda viejo.

## 4. Memoria de una intervención en patrimonio

- **Tres estados con los mismos bloques numerados:** original, actual y reformado.
  - En la referencia eran doce bloques: distribución, solados, acabados, baños, cocina, carpintería interior, cerrajería, carpintería exterior, sótano, cubierta, exteriores e instalaciones.
  - **Por qué:** cada pérdida detectada tiene su respuesta en el estado reformado, en el mismo número.
- **Declara el estado de referencia,** con fecha, fuente y motivo, antes de decidir qué es original y qué es añadido.
  - En la referencia se tomó como original un estado posterior a la construcción, ampliación incluida, documentado con los planos y fotos de época de un archivo.
- **Cita los criterios de la ley de patrimonio y úsalos después** para justificar cada decisión: mínima intervención, diferenciación, reversibilidad.
  - **Cada artículo, con su número, comprobado en la fuente oficial y vigente** (`comprobar-normativa`). La referencia citaba a la vez dos leyes autonómicas de patrimonio sucesivas.
  - **Haz con la ley una lista de lo que tiene que contener el proyecto y comprueba cada punto.**
    - La memoria de la referencia citaba el artículo que exige plan de mantenimiento, plazo, coste y memoria final, y no incluía ninguno.
    - El presupuesto sí pagaba a la constructora la memoria final y el plan de mantenimiento.
- **Patologías:** parte de lo que dice la declaración del bien protegido, compruébalo en tu inspección y amplíalo con fotos.
- **Di qué no se ha podido inspeccionar, por qué y cuándo se resolverá.**
  - Ejemplo: en la referencia no se hicieron catas por ser un BIC, y se dejaron para el inicio de la obra.
  - Refléjalo en las mediciones como medición provisional.
- **Si la administración ha rechazado algo, cita su requerimiento literal y responde con pruebas:**
  - muestras físicas colocadas sobre el material original y fotografiadas;
  - fotos de época, incluso de fuentes no técnicas (un fotograma de una película demostró que un patio no estaba pavimentado).
- **En materiales artesanales, escribe la tolerancia respecto a la muestra.**
  - Ejemplo: «Las piezas sufrirán ligeras alteraciones respecto a las muestras».
  - **Por qué:** constructora y propiedad saben qué esperar, y se evita una reclamación.
- **Di lo que no se recupera y por qué.**
  - Ejemplo: el jardín original no se restituye por el arbolado protegido.
- **La memoria remite a las láminas por su código y a los capítulos del presupuesto.** Añade una tabla que relacione los bloques de la memoria con los capítulos del BC3.
  - La de la referencia no citaba ni una lámina, y el BC3 tenía capítulos (piscina, techos, un sistema de zonificación) que la memoria no describía.
- **Del CTE, pon la tabla «exigencia / proyecto»** de cada sección y los «no procede» razonados, citando los artículos como dice `comprobar-normativa`. No pegues el texto de la norma entero: en la referencia eran trece páginas.
- **Tono técnico, sin adjetivos.** Sobran «lamentable», «deplorable» o «esplendor original».

## 5. Mediciones y pliego atados a los planos

El método general de medir y del BC3 está en `mediciones-presupuesto`. De la referencia se añade lo siguiente.

- **Cada partida cita su lámina o su ficha con el código exacto del cajetín.**
  - Ejemplo bueno: «Ver planos MCI 01 y MCI 11».
  - En la referencia, el plano decía «CO MCE 01» y las partidas «CC MCE 01» (25 veces). Además, 228 de las 303 partidas que no son de instalaciones no citaban ninguna lámina.
  - Compruébalo con un script: cada código citado en las mediciones existe en el índice de planos.
- **Las demoliciones se miden por la leyenda del plano y lo dicen.**
  - Ejemplo: «En todos los locales en que se indica la leyenda FO en los planos DEM 01 y DEM 02».
  - **Por qué:** se evita el listado de estancias y el plano manda.
- **Una partida por elemento existente con ficha,** con su código y su condición en el título y el estado en el texto.
  - Ejemplos de título: «Carpintería exterior ORIGINAL A SUSTITUIR C6» y «NO ORIGINAL A SUSTITUIR C12».
  - En el texto van las medidas, el estado de conservación y los trabajos de la ficha. Si se reproduce, se añade «reproduciendo fielmente el detalle del proyecto original».
- **Desmontaje «con recuperación» y «sin recuperación» en partidas separadas.** La de recuperación incluye siglado, acopio y protección de las piezas.
- **Una partida global de protección de lo existente:** tableros, plásticos, mantenimiento, reposición y retirada.
- **En restauración, las muestras y la mano de obra van dentro de la partida.**
  - Ejemplo de muestras: «Cuantas muestras de 100 × 100 cm solicite la DF hasta alcanzar el tono y la textura adecuados».
  - Ejemplo de mano de obra: «Realizado por personal con experiencia en restauración».
  - Cita la norma de la prestación. Ejemplos: «chorreado grado Sa 2½ según UNE-EN ISO 8501-1» y «mortero R2 según UNE-EN 1504-3».
- **Un capítulo pagado de documentación del proceso de restauración.** Incluye:
  - reportaje fotográfico y vídeo;
  - registro de cada elemento intervenido en una base de datos acordada con la DF;
  - memoria final de intervención;
  - plan de mantenimiento;
  - toma de datos de lo que queda oculto, como el suelo radiante antes de taparlo.
  - **Por qué:** la ley de patrimonio suele pedir esos documentos, y alguien los tiene que producir y cobrar.
- **Las mediciones provisionales** (término y regla de `mediciones-presupuesto`) **se marcan en su línea de medición y la partida dice cómo se liquidan:** según lo realmente ejecutado y medido por la DF.
  - En la referencia había 50 partidas con líneas «previsión» y ninguna decía cómo se liquidaban.
- **Partidas alzadas:** el texto da la base para valorarlas (qué incluye, hasta dónde, con una medida o un porcentaje de referencia). En el ciego no llevan importe.
  - Si el usuario decide fijar un importe de referencia, lo decide él.
  - En la referencia, seguridad y salud, residuos y control de calidad eran «según el plan de la constructora», sin base. Así las ofertas no son comparables.
- **No repitas la misma partida por estancia.** Haz una partida por tipo, con una línea de medición por estancia.
  - En la referencia había 101 partidas de mecanismos eléctricos, una por estancia y con textos idénticos. Una constructora puede ofertar dos precios distintos para lo mismo.
- **El pliego de licitación cierra la forma de la oferta.** Lo bueno de la referencia, para copiar:
  - valorar todas las partidas, aunque no tengan medición;
  - prohibido cambiar textos o mediciones: las correcciones y las mejoras van en un documento aparte y valorado;
  - oferta técnica de cinco hojas como máximo, con tipografía fijada;
  - obras de referencia parecidas;
  - planificación valorada mes a mes, con los recursos;
  - método de demoliciones, acopios y medios auxiliares;
  - técnico de enlace de seguridad y salud valorado;
  - currículum del jefe de obra y del encargado;
  - lista cerrada de subcontratas;
  - forma de pago;
  - confidencialidad.
- **Lo que le faltaba al pliego.** Pregunta al usuario cuáles de estos puntos fija el promotor. No los rellenes con valores propios (ver `decisiones-cliente`):
  - visita de obra y plazo de consultas;
  - plazo de ejecución;
  - aval, seguros y validez de la oferta;
  - revisión de precios;
  - peso de cada criterio de adjudicación;
  - qué se hace con una baja anormal;
  - cómo se liquidan las partidas alzadas y las mediciones provisionales;
  - hora y lugar de entrega.

## 6. Antes de enviar: lo que falló en la referencia y cómo buscarlo

1. **Tipografía con el cero tachado.**
   - **Qué pasó:** la fuente corporativa dibujaba el 0 como Ø. Así «2Ø×2Ø cm» se lee como un diámetro, el modelo «59ØH-4Ø» ya no es una referencia de catálogo válida y la referencia catastral sale mal.
   - **Qué hacer:** en un documento técnico, el cero es un cero. Si una marca usa una fuente así, resérvala para el logotipo.
2. **Cuadros de superficies distintos y totales mal sumados.**
   - **Qué pasó:** había tres versiones del cuadro.
     - La memoria daba 610,95 m² útiles.
     - El plano de estado actual daba 610,22 m².
     - El reformado declaraba 418,28 m², y sus filas suman 630,55.
     - Exteriores: 762,69 m² declarados frente a 867,62 de suma. Parcela: 4.359,29 m² frente a 4.357,35.
   - **Qué hacer:** con un script, suma cada cuadro y compara el mismo dato (superficies, parcela, potencias, número de árboles) en planos, memoria y mediciones.
3. **Títulos del cajetín copiados de otra lámina.**
   - **Qué pasó:** la primera lámina de carpintería exterior se titulaba «Memoria de carpintería interior 01». Además, la misma serie se llamaba de dos maneras («Memoria de muros» y «Memoria muros») y había títulos sin número.
   - **Qué hacer:** genera los títulos desde una lista maestra (el índice) y compáralos con el texto del cajetín.
4. **Material pegado de otros programas sin adaptar.**
   - **Qué pasó:**
     - fichas genéricas del generador de precios de CYPE, con otra fuente, códigos de materiales y el texto `.\ASA010_Img0.bmp` de una imagen que no se exportó;
     - una tabla de Excel en color;
     - un esquema de fontanería con otra simbología.
   - **Qué hacer:** busca en el texto del PDF `.bmp`, `.png`, `.jpg`, `Img` y rutas (`\`), y cuenta las fuentes por lámina. Más de dos fuentes indica material pegado.
5. **Textos ilegibles.**
   - **Qué pasó:** había rótulos de 1 mm en A1, que impresos en A3 se quedan en 0,5 mm.
   - **Qué hacer:** mide el tamaño de los textos y aplica el mínimo de `libro-estilo-agoin`: 2 mm, y 1,5 mm solo en hojas de trabajo.
6. **Escala en esquemas.**
   - **Qué pasó:** «Esquema unifilar 1/100» y «Esquemas de principio 1/100».
   - **Qué hacer:** los esquemas llevan «S/E».
7. **Leyendas que se salen de su recuadro y erratas.**
   - **Qué pasó:** «inlcuso», «cablaeado», «aceroa».
   - **Qué hacer:** revisa la leyenda ampliada y pasa un corrector ortográfico al texto extraído del PDF.
8. **Cajetín sin versión.**
   - **Qué pasó:** no había campo de versión ni de revisión. Un juego que se licita acaba teniendo adendas, y sin versión no se sabe cuál vale.
   - **Qué hacer:** usa el cajetín del libro de estilo, que lleva campo VERSIÓN.
9. **Restos de plantilla en la memoria.**
   - **Qué pasó:** quedaban textos de otra fase o de otro documento.
   - **Qué hacer:** busca:
     - «básico» en un proyecto de ejecución;
     - «no procede» sin razonar;
     - remisiones a apartados o anejos que no existen;
     - fechas de otros documentos (había un plano fechado siete meses después de la memoria).
10. **Datos maestros que no casan.**
    - **Qué pasó:** superficie construida, potencias, número de elementos o fechas cambiaban de un apartado a otro.
    - **Qué hacer:** haz una tabla con cada dato y la página donde aparece, y compárala entre apartados.
11. **Referencias a otras partidas por su número.**
    - **Qué pasó:** tras renumerar, «ver partida 04.04.02» apuntaba a un fieltro.
    - **Qué hacer:** cita las partidas por su nombre, o regenera las referencias con un script después de cada renumeración.
12. **El carácter «|» dentro de un nombre de concepto en el BC3.**
    - **Qué pasó:** había 36 nombres como «DEMOLICIONES | DESMONTADOS». El «|» es el separador de campos del FIEBDC y desplaza la unidad y el precio.
    - **Qué hacer:** usa «/» o una coma.
13. **Restos de la base de precios en el BC3 ciego.**
    - **Qué pasó:** quedaban descompuestos (`~D`) en 17 partidas, con mano de obra y rendimientos, y registros de Presto con «NO SE HA EJECUTADO».
    - **Qué hacer:** antes de enviarlo, compruébalo con un script.
14. **Metadatos y datos personales en los PDF.**
    - **Qué pasó:** el título del PDF de mediciones llevaba una ruta local con el nombre del usuario, y el pliego copiaba los NIF y las direcciones particulares de promotor y arquitectos.
    - **Qué hacer:** revisa los metadatos de cada PDF (título, autor, programa) y deja en el pliego solo los datos de contacto necesarios.

## 7. Analizar un proyecto de referencia

El método que se usó:

1. **Inventario con PyMuPDF:** páginas, formato, programa que lo generó y marcadores de cada PDF.
2. **Tabla de láminas por script:** código, título y escala leídos del cajetín.
3. **Hojas de contactos de 2 × 2 láminas** para ver el juego entero. Después, amplía a 150 ppp (más si hace falta leer cifras pequeñas) el cajetín, las leyendas, las fichas y las tablas.
4. **Comprobaciones por script:**
   - sumas de los cuadros;
   - títulos frente a la serie;
   - porcentaje de trazo por hoja (hojas casi vacías);
   - tamaños de texto;
   - fuentes por hoja;
   - restos (`.bmp`).
5. **La memoria y las mediciones, a dos subagentes en paralelo,** con las skills del estudio como referencia, para separar lo nuevo de lo que ya sabemos. Después, un revisor independiente busca contradicciones con las demás skills antes de subir nada.
6. **Si el texto extraído de una lámina sale cambiado** («A 6 EA 2» en vez de «AQ EA 02»), es la tabla de caracteres de la fuente, no el plano. Míralo como imagen antes de dar un error.
7. **Entrega en tres listas:** bien hecho (copiar), mal hecho (comprobación) y lección nueva. Cada punto con su lámina o su página.
8. **Lo ajeno no se identifica en las skills:** ni el estudio, ni el edificio, ni las personas. La identificación se guarda solo en la memoria local del proyecto.
