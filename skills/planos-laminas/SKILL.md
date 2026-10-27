---
name: planos-laminas
description: "Cómo producir, exportar y revisar láminas de planos de arquitectura, estructura e instalaciones (desde Revit, AutoCAD u otro programa) con calidad de proyecto de ejecución. Incluye cómo leer planos PDF vectoriales (cotas, símbolos, capas, textos) con PyMuPDF sin caer en sus trampas. Úsala al sacar, rehacer, maquetar, exportar o revisar planos y juegos de láminas, al publicarlos, y al extraer información de un PDF de planos. Para acotar plantas, usa además acotar-planos."
---

# Láminas de planos

El listón del usuario es: «plumillas perfectas, sin incongruencias, cosas raras, solapes ni restos de los planos anteriores, bien maquetados, explicados». Un juego que no lo cumplió («los planos están fatal») se retiró de la web, y se volvió a los planos originales del proyecto hasta rehacerlo.

## Al hacerlas

- **Toma como referencia la maquetación del proyecto de ejecución:** mismo orden, escalas, cajetín y leyendas. Lo que el modelo no dibuja (leyendas, cuadros, detalles) se copia del proyecto en su posición en el papel.
- **Grosores de línea:**
  - por categoría, distinguiendo corte y proyección;
  - lo cortado, con poché.
- **Sin restos de versiones anteriores:** textos, cotas o vistas ocultas que vuelven a aparecer.
- **Notas que explican lo que el dibujo no enseña.** Nada queda sin explicar.
- **Fondos de los textos:**
  - **Cifras de cota sobre un dibujo de líneas:** fondo opaco, como dice la skill `acotar-planos`.
  - **Rótulos, cotas de nivel y etiquetas:** fondo semitransparente al 50 %, sin borde.
  - **Sobre imágenes** (ortofotos, nubes de puntos): siempre semitransparente.
  - **Si la lámina se llena de recuadros blancos,** pasa también las cifras a semitransparente. Un usuario se quejó de «muchos recuadros blancos».
- **Juegos de emplazamiento:** pocas láminas, llenas y con leyenda; el norte, nunca en rojo; las coordenadas, fuera del marco.
- **Versiones:**
  - cada juego lleva su número (v13) y su fecha;
  - el juego anterior pasa a una carpeta de anteriores;
  - no sustituyas el juego publicado hasta que el usuario apruebe el nuevo.
- **En CAD:** líneas rectas y arcos verdaderos, no polilíneas densas.

## Antes de darlas por buenas

1. **Exporta a PDF vectorial y revisa cada lámina ampliada,** a 150–200 ppp y por zonas, no solo la vista general. Los solapes y lo que se sale del marco solo se ven así.
2. **Comprobación automática:**
   - ningún texto pisa otro texto, una línea gruesa, una cota o un símbolo;
   - nada queda fuera del marco;
   - ninguna vista está vacía.
3. **Compara con el juego anterior, píxel a píxel.** Solo debe cambiar lo que has cambiado. Ojo con tres efectos:
   - los muros editados desplazan sus huecos;
   - las plantillas cambiadas vuelven a mostrar elementos ocultos;
   - las vistas sin recorte se mueven en la hoja.
4. **Compara con el plano de referencia del proyecto:** las mismas cifras y los mismos ejes.
5. **Si se entregan DWG, expórtalos y abre una muestra.**
6. **Entrega con la lista de lo que queda abierto** para el usuario.

## Leer planos PDF vectoriales (PyMuPDF)

- **Elige bien el archivo.**
  - Si existe una versión con capas, úsala: cada red de instalaciones o cada elemento viene separado.
  - Comprueba que es geométricamente igual a la visada.
  - Cuidado con los borradores anteriores que tienen el mismo nombre: mira las fechas y los sellos.
- **Una línea dibujada como rectángulo** (de alto o ancho cero) nunca «interseca» nada. Ínflala 0,5 pt.
- **`get_text("dict", clip=...)` corta los caracteres** de un fragmento que caen fuera del recorte («según» → «segú»). Lee la página entera y filtra por el centro de cada fragmento.
- **Hay fragmentos de texto basura de 0 pt** (atributos de bloques). Descarta los de tamaño menor que 1.
- **Los textos convertidos a contorno** (espesores en planos de estructura, etiquetas de circuitos) no salen en `get_text`: no se pueden extraer como texto. Léelos a la vista sobre una imagen, en recortes numerados, y confírmalos.
- **Los símbolos se cuentan por su forma** (por ejemplo, un círculo de radio fijo con 1, 2 o 4 brazos) y se confirman a la vista. Los que tocan un muro se funden con él.
- **Los rellenos vienen triangulados** (un cuadrado hueco son 8 triángulos). Separa los subtrayectos y únelos con shapely.
- **Para pasar de coordenadas del papel a las del modelo:**
  - registra con puntos conocidos, como las burbujas de los ejes;
  - mide el error (RMS);
  - la escala rotulada en el cajetín puede estar mal: mídela.

## Herramientas

- **Revit:** las trampas de láminas, vistas y plantillas están en la skill `revit-automatizacion` (`references/trampas-revit.md`, apartado 8).
- **AutoCAD:** ver la skill `automatizar-programas-windows`.
- **Acotación:** ver la skill `acotar-planos`.
