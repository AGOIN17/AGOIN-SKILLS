---
name: planos-laminas
description: "[PLANOS] Cómo producir, exportar y revisar láminas de planos de arquitectura, estructura e instalaciones (desde Revit, AutoCAD u otro programa) con calidad de proyecto de ejecución, y cómo comprobarlas en el PDF antes de darlas por buenas (solapes, grosores, colores, escala, regresiones, revisión por bloques). Incluye cómo leer planos PDF vectoriales (cotas, símbolos, capas, textos, páginas giradas) con PyMuPDF sin caer en sus trampas. Úsala al sacar, rehacer, maquetar, exportar o revisar planos y juegos de láminas, al publicarlos, y al extraer información de un PDF de planos. Para el estilo gráfico de AGOIN usa además libro-estilo-agoin; para acotar, acotar-planos."
metadata:
  etiquetas: "PLANOS"
---

# Láminas de planos

El listón del usuario es: «plumillas perfectas, sin incongruencias, cosas raras, solapes ni restos de los planos anteriores, bien maquetados, explicados». Un juego que no lo cumplió («los planos están fatal») se retiró de la web, y se volvió a los planos originales del proyecto hasta rehacerlo.

**El estilo** (zonas de la hoja, cajetín, numeración, textos, colores, tipos, etiquetas, leyendas, carpinterías) está en `libro-estilo-agoin`. Esta skill trata de producir y comprobar.

## Al hacerlas

- **Prueba el estilo en una lámina antes de rehacer el juego** y enséñala con un antes y un después. Los juegos v03–v12 de ALFERECES se rehicieron enteros sin piloto.
- **Si hay un proyecto de referencia (el visado), toma su maquetación:** mismo orden, escalas, cajetín y leyendas.
  - **Del visado solo se copia lo que no depende de la geometría:** leyendas, notas generales y detalles constructivos.
  - Los nombres de estancia, superficies, cotas, niveles y etiquetas **salen del modelo** o se regeneran tras cada cambio. En una lámina, 223 de 224 textos eran copias fijas del visado y ya no casaban con el modelo.
  - Borra las líneas copiadas que repiten lo que ya dibuja el modelo: 7.430 líneas duplicaban el dibujo.
- **Las superficies de rótulos y cuadros salen de una sola fuente.** Pregunta cuál manda, el modelo o el visado. Una estancia partida en el modelo (baño y ducha) no puede dar dos cifras: los rótulos daban 4,83 m² y el cuadro 6,17.
- **En juegos nuevos, pocas láminas y completas:** planos de conjunto, cada hoja llena, con su leyenda y sus tablas.
- **Grosores de línea por categoría,** distinguiendo corte y proyección; lo cortado, con poché. Compruébalo en el PDF (abajo): una pluma forzada en las plantillas dejó el 92 % de los trazos con el mismo grosor.
- **Sin restos de versiones anteriores:** textos, cotas o vistas ocultas que vuelven a aparecer.
- **Notas que explican lo que el dibujo no enseña.** Nada queda sin explicar.
- **Fondos de los textos:**
  - **Cifras de cota sobre un dibujo de líneas:** fondo opaco, como dice `acotar-planos`.
  - **Rótulos, cotas de nivel y etiquetas:** velo blanco al 50 %, sin borde y ceñido a las letras.
  - **Sobre imágenes** (ortofotos, nubes de puntos): siempre el velo.
  - **Si la lámina se llena de recuadros blancos,** pasa también las cifras al velo. Un usuario se quejó de «muchos recuadros blancos».
- **Versiones:**
  - cada juego lleva su número (v13) y su fecha, y el cajetín la versión al día;
  - cada lámina lleva un recuadro con lo que cambia respecto al visado, con el número de cada cambio. **Un cambio que afecta a una lámina se dibuja;** no basta con nombrarlo en una nota;
  - el juego anterior pasa a una carpeta de anteriores;
  - no sustituyas el juego publicado hasta que el usuario apruebe el nuevo.
- **Juegos de emplazamiento:** pocas láminas, llenas y con leyenda; el norte, nunca en rojo; las coordenadas, fuera del marco.
- **En CAD:** líneas rectas y arcos verdaderos, no polilíneas densas.
- **Unidades:** «kPa» salió «KPA» al pasar a mayúsculas. Escribe las unidades bien y revísalas.

### Plantas con varias unidades o viviendas

- **Límite entre unidades:** línea fina de trazo y punto, nunca una franja blanca. Los recortes de las vistas vecinas encajan exactamente en el eje del muro, sin solaparse (por ejemplo, con una partición de Voronoi de las estancias): si se solapan, el relleno blanco de cada vista sale como rayas blancas en el PDF.
- **Unidades a distinto nivel:** corta cada planta a 1,30 m sobre el suelo de su propia unidad; con un corte común, unas ventanas salían cortadas y otras no.
- **En hojas de conjunto (1:250 a 1:400),** los rótulos de cada unidad van fuera de los edificios, con directriz. Las entradas que no caben se numeran junto a su flecha y su dato va a la columna. Las estancias pequeñas vecinas se rotulan juntas.
- **Rótulos de instalaciones en tres longitudes:** completo, dos líneas y una línea. Si ni el corto cabe dentro, sale fuera de todo el edificio con directriz; nunca a la estancia de otra unidad. No repitas en cada punto lo que ya explica la leyenda.
- **Lo que se modela solo para una vista 3D** (instalaciones esquemáticas, maquetas) se oculta en todas las demás: «en todas las plantas se ven las tuberías… no salen limpias».
- **Una superficie que es un solo plano se dibuja y se rotula como una sola pieza,** aunque parte sea existente y parte ampliación; troceada parece que va a bataches.

### Planos de instalaciones

Criterio usado en ALFERECES, pendiente de que el usuario lo confirme:

- la arquitectura de fondo en medio tono y sin mobiliario, con los nombres de estancia en negro;
- cada red en su color y con pluma gruesa;
- los símbolos tomados de la leyenda del proyecto (o del libro de estilo);
- rótulos sin solaparse, y el diámetro solo en tramos largos, no en cada segmento («demasiados Ø»).

### Planos de terreno y niveles (rehabilitación y urbanización)

- **Movimiento de tierras:** cada estancia, acera o tramo coloreado según se rellene o se vacíe; en cada sitio, la cota de antes y la de después; una tabla de m³ de relleno y de vaciado por unidad, tramo y fase; la leyenda con la sección del pavimento.
- **Estudio de niveles para decidir cotas,** una hoja por fachada larga: el alzado exterior; debajo, una sección interior a 1 m de la fachada mirándola desde dentro, con suelos y techos cortados y el terreno exterior en línea de puntos; el suelo existente a trazos y el proyectado; rayados de recrecido y de rebaje; y un cuadro por unidad para decidir. El terreno y la calle, siempre del estado actual.

### Encajar

- **Elige la escala de cada vista probando:** coloca, mide y baja de escala solo si no cabe (las secciones a 1:150 pasan a 1:200).
- **Coloca las leyendas por prueba:** dibuja, mide y deshaz hasta que todo quepa.
- **Un muro largo que no cabe en un detalle** se rompe con una línea de corte; no bajes la escala.

## Antes de darlas por buenas

1. **Exporta a PDF vectorial y revisa cada lámina ampliada,** a 150–200 ppp y por zonas, no solo la vista general. Los solapes y lo que se sale del marco solo se ven así. Mira el nombre y la fecha del PDF que revisas: la exportación por API puede ponerle otro nombre y se revisó un PDF viejo.
2. **Comprobaciones automáticas sobre el PDF:**
   - ningún texto pisa otro texto, una línea gruesa, una cota o un símbolo (lleva un contador y bájalo a cero: de 34 a 1);
   - nada queda fuera del marco y ninguna vista está vacía;
   - **el reparto de grosores de trazo:** si casi todo sale con el mismo grosor, se ha perdido la jerarquía;
   - **no hay trazos ni rellenos de color en láminas en blanco y negro** (la lana salía en amarillo por el patrón del material);
   - **la escala rotulada y la versión del cajetín coinciden con el dibujo** (una lámina decía 1:100 y estaba a 1:25);
   - **cada cuadro suma bien y da lo mismo que la memoria y las mediciones.**
     - Comprueba superficies, cantidades de leyenda y parcela.
     - En un proyecto ajeno muy cuidado, el cuadro reformado declaraba 418,28 m² y sus filas sumaban 630,55.
     - Para un juego que se licita, pasa además la lista de `proyecto-ejecucion-licitacion`.
3. **Compara con el juego anterior, píxel a píxel.** Solo debe cambiar lo que has cambiado. Ojo con tres efectos:
   - los muros editados desplazan sus huecos;
   - las plantillas cambiadas vuelven a mostrar elementos ocultos;
   - las vistas sin recorte se mueven en la hoja.
4. **Compara con el plano de referencia del proyecto:** las mismas cifras y los mismos ejes. En planos de cotas, cuenta las cotas frente a la referencia (ver `acotar-planos`).
5. **Si colocas anotaciones con un algoritmo de «sitio libre»,** cada vez que lo cambies lánzalo dos veces en simulación: la segunda pasada no debe mover nada. Un fallo silencioso daba por libres etiquetas que se pisaban.
6. **En juegos grandes, revisión por bloques con varios revisores:** una o dos láminas por agente (o bloques de hojas), comparadas con el visado y la lista de cambios. Cada problema con su zona en mm, gravedad (alta, media, baja), por qué está mal, cómo arreglarlo y un recorte comparado. Junta, prioriza, corrige, regenera y vuelve a revisar: hicieron falta tres rondas. Ojo al coste (ver `optimizar-trabajo`).
7. **Si se entregan DWG, expórtalos y abre una muestra.**
8. **Entrega con la lista de lo que queda abierto** para el usuario.

## Leer planos PDF vectoriales (PyMuPDF)

- **Elige bien el archivo.**
  - Si existe una versión con capas, úsala: cada red de instalaciones o cada elemento viene separado.
  - Comprueba que es geométricamente igual a la visada.
  - Cuidado con los borradores anteriores que tienen el mismo nombre: mira las fechas y los sellos.
- **Páginas giradas** (`page.rotation` de 90 o 270): los recortes salieron desplazados. Antes de recortar, comprueba el giro y en qué espacio vienen las coordenadas de cada función (página girada o sin girar; `page.rotation_matrix` y `page.derotation_matrix` convierten) con una prueba sobre un texto conocido, y toma los colores de la leyenda de su columna después de comprobar cuál es.
- **Una línea dibujada como rectángulo** (de alto o ancho cero) nunca «interseca» nada. Ínflala 0,5 pt.
- **`get_text("dict", clip=...)` corta los caracteres** de un fragmento que caen fuera del recorte («según» → «segú»). Lee la página entera y filtra por el centro de cada fragmento.
- **Hay fragmentos de texto basura de 0 pt** (atributos de bloques). Descarta los de tamaño menor que 1.
- **El texto trae espacios duros (U+00A0):** normalízalo antes de buscar con expresiones regulares.
- **Los textos convertidos a contorno** (espesores en planos de estructura, etiquetas de circuitos) no salen en `get_text`. Léelos a la vista sobre una imagen, en recortes numerados, y confírmalos.
- **Los símbolos se cuentan por su forma** (por ejemplo, un círculo de radio fijo con 1, 2 o 4 brazos) y se confirman a la vista. Los que tocan un muro se funden con él.
- **Los rellenos vienen triangulados** (un cuadrado hueco son 8 triángulos). Separa los subtrayectos y únelos con shapely.
- **Para pasar de coordenadas del papel a las del modelo:**
  - registra con al menos dos puntos conocidos, mejor tres (burbujas de ejes, esquinas), y da el error (RMS). Con uno solo, una imagen de fondo puede quedar desplazada sin que se note: una calibración con un solo eje dio una coincidencia falsa;
  - la escala rotulada en el cajetín puede estar mal: mídela. Con dos cotas de ejes contiguas, la distancia entre los centros de sus cifras es la semisuma de los dos tramos; compruébalo en dos tramos distintos.
- **Medir por color sobre una imagen** sirve para detectar que falta algo, no para fijar la cantidad (±10 %).

## Herramientas

- **Revit:** las trampas de láminas, vistas y plantillas están en `revit-automatizacion` (`references/trampas-revit.md`, apartado 8).
- **AutoCAD:** ver `automatizar-programas-windows`.
- **Acotación:** ver `acotar-planos`.
- **Hojas para que decida el cliente** (DEC, DIS, DUDA, TR): ver `decisiones-cliente`.
