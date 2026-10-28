# Guía de método · de un proyecto de ejecución a modelo, mediciones, web y vídeo

Escrita el 13/10/2026 a partir del proyecto ALFERECES (dos viviendas y un local, Toledo). Sirve para arrancar otro proyecto con
el mismo sistema: qué hay que tener antes de empezar, cómo ordenar las carpetas, en qué orden se trabaja y con qué reglas.

Para usarla en un proyecto nuevo: copia este archivo a la carpeta del proyecto y pide al asistente que la lea antes de empezar.

---

## 1. Qué se obtiene

| Producto | Para quién | En ALFERECES |
|---|---|---|
| Modelo Revit de arquitectura y estructura al día del proyecto de ejecución | El estudio | `BLAL_AGOIN_ARQ_R27.rvt` |
| Modelo Revit de instalaciones, vinculado al anterior | El estudio | `BLAL_AGOIN_MEP_R27.rvt` |
| Láminas de arquitectura en PDF y DWG, sacadas del modelo | Constructoras | `TRABAJO_REVIT_PE2026/exports` |
| Presupuesto revisado partida a partida, con registro de cada cambio | El estudio y la promotora | `TRABAJO_MEDICIONES` |
| Mediciones sin precios (Excel y BC3) y pliego de condiciones de la oferta | Constructoras | Ídem |
| Web con el modelo 3D enlazado a las partidas, planos, vídeo y descargas | Constructoras y promotora | `WEB` · alfereces.agoin-cde.com |
| Vídeo de la obra (4D) y modelo en IFC | Todos | `TRABAJO_REVIT_PE2026/video` |

---

## 2. Documentos base: qué hay que tener antes de empezar

Sin los cuatro primeros no se puede arrancar. El resto evita rehacer trabajo.

**Imprescindibles**

1. **Planos del proyecto de ejecución en PDF vectorial**, todas las láminas en un archivo (arquitectura, estructura e
   instalaciones). Vectorial quiere decir exportado desde CAD o Revit, no escaneado: sobre el vectorial se leen cotas, se
   cuentan símbolos uno a uno y se sacan perfiles de terreno o despieces. Con un escaneado, nada de eso es fiable.
2. **Memoria completa en PDF**, con anejos de cálculo, memoria de carpinterías y de calidades, y mediciones y presupuesto.
3. **Presupuesto en BC3** (o en Excel con capítulos, partidas, líneas de medición y precios). Si solo existe en PDF, se
   reconstruye, pero cuesta más y hay que avisarlo.
4. **Modelo de partida**, si existe: el `.rvt` (cualquier versión) o los DWG de plantas, alzados y secciones. Se guarda como
   original y no se vuelve a tocar: se trabaja sobre una copia actualizada a la versión de Revit instalada.

**Muy convenientes**

5. **Lista de cambios decididos después del visado** («CAMBIOS»): un documento del estudio con cada decisión, su fecha y a qué
   plano o partida afecta. Es lo que más errores evita.
6. **Datos del solar**: topográfico o, al menos, las cotas de las calles en cada esquina del edificio y el punto de replanteo
   (±0,00). En ALFERECES la pendiente de dos calles se modeló mal al principio por no leerla de los alzados.
7. **Fotos del estado actual** y de las fachadas colindantes; qué está ya demolido o ejecutado.
8. **Referencias de producto ya decididas** (fichas o enlaces): equipos, mecanismos, carpinterías, ventiladores…
9. **Ofertas o precios de referencia** recibidos, si los hay, con su fecha.
10. **Planos de estructura e instalaciones en DWG**, si el estudio los tiene: permiten ofrecerlos en la web.

**Datos de gestión**

11. Promotor, dirección, título oficial del proyecto, código (por ejemplo `BLAL`), cajetín y logotipo.
12. **A quién va cada cosa**: qué ve la promotora y qué ven las constructoras; qué no se publica nunca.
13. Dominio y servidor para la web, si se quiere publicar.
14. Revit instalado con licencia, Dynamo, Python y Blender en el equipo.

---

## 3. Estructura de carpetas recomendada

La de ALFERECES creció sobre la marcha (modelos, PDF y carpetas de trabajo mezclados en la raíz). Para un proyecto nuevo:

```
D:\ARQ\<PROYECTO>\
│  GUIA_METODO_AGOIN.md            esta guía
│  <COD>_ARQ_R27.rvt               modelos de trabajo, en la raíz (Revit los vincula entre sí por ruta)
│  <COD>_MEP_R27.rvt
│
├─ 00_BASE\                        lo recibido o visado. SOLO LECTURA: nada de aquí se modifica
│    <COD>_PLANOS.pdf   <COD>_MEMORIA.pdf   <COD>_PRESUPUESTO.bc3
│    modelo_original\   dwg\   topografico\   fotos\   fichas_producto\
│
├─ 01_DECISIONES\                  CAMBIOS.md (decisiones posteriores al visado), actas y correos que deciden algo
│
├─ 02_MODELO\                      scripts de Dynamo, familias, fichas leídas de los planos
│    dynamo\   MEP\   familias\   copias\ (una copia del .rvt antes de cada cambio grande)
│    exports\ (pdf\  dwg\  ifc\)   registro_cambios.csv
│
├─ 03_MEDICIONES\                  presupuesto de trabajo y entregables
│    herramientas\ (cambios.json y los generadores)   comprobaciones\
│    <COD>_MEDICIONES_TRABAJO.xlsx   <COD>_MEDICIONES_CIEGO.xlsx   <COD>.bc3   <COD>_CIEGO.bc3
│    CONDICIONES_DE_LA_OFERTA.pdf   CAMBIOS_EN_PLANOS.pdf   CAMBIOS_EN_MEMORIA.pdf
│
├─ 04_SEGUIMIENTO\                 la memoria del trabajo: lo primero que se lee al retomarlo
│    CONTEXTO_PARA_CONTINUAR.md   REGISTRO_DE_TRABAJO.md   METODO_DE_MEDICION.md   CRITERIOS.md
│
├─ 05_WEB\                         construir\ (guiones)   fuente\   sitio\ (lo publicado)   sitio_promotora\ (interno)
│
├─ 06_VIDEO\                       blender\   render\   imagenes\ (las que el estudio quiera en la web)
│
└─ 99_HISTORIAL\                   enviados y recibidos, con fecha en el nombre de la carpeta
```

Equivalencia con ALFERECES: `00_BASE` son los `BLAL_*.pdf`, el `.bc3` y el `.rvt` original de la raíz; `02_MODELO` es
`TRABAJO_REVIT_PE2026`; `03_MEDICIONES` es `TRABAJO_MEDICIONES`; `04_SEGUIMIENTO` es `SEGUIMIENTO_MEDICIONES`; `05_WEB` es `WEB`.

**Variante que funcionó en CHIVERO** (rehabilitación, sobre todo trabajo en Revit): una carpeta `TRABAJO_REVIT\` con
`00_PLAN.md` (un único archivo de plan que se lee lo primero), `datos\`, `dynamo\`, `scripts\`, `capturas\`,
`referencias\copias\` (copias del libro de estilo, plantillas y proyectos modelo del estudio) y `copias_seguridad\`.
Las dos sirven: lo que importa es que lo original quede aparte y que haya un archivo de contexto al día.

Tres reglas de la estructura:

- **Lo original no se toca.** Se trabaja sobre copias; el original queda como testigo para comparar.
- **Todo cambio deja rastro en un archivo**, no en una conversación: `cambios.json` para el presupuesto,
  `registro_cambios.csv` para el modelo, `REGISTRO_DE_TRABAJO.md` para los hallazgos.
- **Los entregables se generan, no se editan.** El Excel, el BC3, el pliego, el anexo y la web salen de guiones; si algo
  está mal, se corrige el dato de origen y se vuelve a generar.

---

## 4. Orden de trabajo

1. **Leer todo antes de modelar.** Planos, memoria, presupuesto y cambios. Anotar las contradicciones entre documentos: suele
   haberlas entre arquitectura y estructura, entre planos y presupuesto, y entre la memoria y los dos.
2. **Poner el modelo al día** del proyecto de ejecución y de los cambios, planta a planta, comparando con el PDF. Por fases,
   cada una con su ficha de diferencias en `fichas/`: F0 inventario y preguntas; F1 niveles y ejes; F2 tipos; F3 planta a
   planta; F4 cubierta, escaleras y ascensor; F6 láminas; F7 revisión. Las dudas van numeradas en una sola lista, que el
   usuario contesta con «sí a todo salvo…». Cada planta se aprueba antes de pasar a la siguiente (ver `revision-modelo-bim`).
3. **Sacar las láminas** del modelo y compararlas con las del proyecto.
4. **Modelar las instalaciones** en un modelo aparte, disciplina a disciplina, con comprobación de choques.
5. **Revisar el presupuesto** partida a partida (apartado 5).
6. **Cruzar modelo y presupuesto**: qué partidas tienen elemento, cuánto mide el modelo, qué elementos no tienen partida.
7. **Documentos para ofertar**: mediciones sin precios, pliego, cambios en planos y en memoria, memoria sin presupuesto.
8. **Web y vídeo.**
9. **Rondas de repaso con el usuario**: él recorre las partidas y la web, y pide cambios; cada ronda se cierra regenerando todo.

---

## 5. Cómo se revisa una partida

Para cada partida se responde, por este orden:

1. **¿De dónde sale?** Plano, cuadro, memoria o presupuesto original. Si nadie la encuentra en los planos, probablemente viene
   de una versión anterior del proyecto (en ALFERECES: una puerta de un semisótano que ya no era vivienda, y 45 m de
   conducto de un sistema de ventilación sustituido).
2. **¿Es necesaria?** Si duplica a otra, o si otra ya la incluye en su precio.
3. **¿Cuánto mide?** Por la jerarquía de fuentes de `METODO_DE_MEDICION.md`: cuadro del plano, cota escrita, medición
   justificada del proyecto, escalado sobre el PDF, recuento de símbolos, dato del usuario. Cada partida dice en su texto
   cuál se ha usado.
4. **¿Lo confirma el modelo?** Si el elemento está modelado, se compara. Si no lo está y se puede, se modela (crucetas de
   punzonamiento, aleros, ventiladores).
5. **¿Qué es?** Una imagen y una frase en lenguaje llano, también en las partidas modeladas.

Comprobaciones que han dado resultado:

- **Contar símbolos sobre el vectorial** y confirmar a la vista sobre ampliaciones. El recuento automático solo no basta: los
  símbolos pegados a un muro se funden con él.
- **Leer espesores y cantos en los planos de estructura**, no en los detalles de arquitectura. El alero era de 25 cm en el
  detalle y de 15 cm en estructura.
- **Comprobar qué incluye cada superficie** antes de restar: una medición restaba un alero que no estaba dentro del total.
- **Comparar entre sí los documentos que se publican**: un pliego decía una cosa y las mediciones otra.

---

## 6. Reglas de trabajo del estudio

Son las indicaciones que el usuario ha ido dando. Valen para cualquier proyecto mientras no diga otra cosa.

**Decisiones**

- Proponer no es aprobar. **Aprobado, incorporado y verificado son tres estados distintos**, y cada cambio dice en cuál está.
- Lo que el usuario ordena de forma expresa se hace. Lo demás se deja como propuesta, con su criterio, para que decida.
- Cuando delega una decisión técnica («el que mejor quepa y se use habitualmente»), se decide, se explica el criterio y se
  deja escrito para que pueda revertirla.
- El usuario no edita archivos a mano: los cambios los aplica el asistente y quedan registrados con su motivo.

**Documentación y terceros**

- **No se envía documentación a terceros sin autorización expresa.**
- A las constructoras: mediciones **sin precios**, sin anotaciones internas de revisión y sin la comparación entre modelo y
  presupuesto. La memoria se ofrece sin el capítulo de presupuesto y con un anexo de las modificaciones acordadas.
- La versión con precios y con la comprobación contra el modelo es interna.
- Antes de publicar, comprobar que los documentos no se contradicen.

**Revit**

- Solo se trabaja en los modelos de trabajo. El original no se abre ni se modifica.
- No se cierra Revit ni se maneja su interfaz mientras el usuario lo tiene abierto.
- Copia del `.rvt` antes de cada cambio; cada guion se prueba primero en simulación; toda transacción controla sus avisos.
- El modelo de instalaciones se edita en segundo plano con el vínculo descargado, y se recarga al terminar.
- El IFC no se exporta por la API (cerró Revit): se genera fuera, a partir de la geometría exportada.

**Instalaciones**

- Trazados sencillos y construibles: paralelos a ejes y muros, giros a 90° (45° solo en saneamiento y conductos), una altura
  por sistema, sin diagonales ni quiebros raros.
- El conducto se elige por caudal y por la cámara disponible: plano donde el falso techo no deja sitio, circular en lo demás.

**Web**

- Tema claro. Que siempre se sepa qué se está viendo: cabecera «Estás viendo», partida anterior y siguiente.
- Las descargas, fáciles de encontrar: entrada propia en el menú. PDF, DWG, IFC, Excel y BC3.
- Cada partida, con su imagen y su explicación. Las partidas por longitud, superficie o volumen dicen qué es cada componente,
  y se puede medir sobre el modelo.
- El logotipo es la fachada del edificio. El vídeo va sin música.
- Las imágenes de las viviendas son las que el usuario deja en su carpeta, y solo esas.

**Vídeo**

- Estilo «dibujo de concurso»: plano, casi sin color, sin figuras humanas. Se comprueba contra los planos.
- No se enseña lo que ya está hecho en obra (demoliciones) ni versiones superadas de una instalación.

**Coherencia**

- Un cambio se lleva a todas partes: modelo, presupuesto, mediciones sin precios, BC3, pliego, cambios en planos y en memoria,
  anexo, web, IFC, DWG y registro. Una ronda no está cerrada hasta que todo se ha vuelto a generar y comprobar.

---

## 7. Qué preguntar el primer día en un proyecto nuevo

1. ¿Qué versión del proyecto manda (fecha del visado) y qué cambios se han decidido después?
2. ¿Qué está ya ejecutado o demolido en obra?
3. ¿Existe un modelo? ¿En qué versión y con qué fiabilidad?
4. ¿Dónde está el punto de replanteo y qué cota tienen las calles en las esquinas?
5. ¿Qué documento prevalece si se contradicen (planos, memoria, presupuesto; arquitectura o estructura)?
6. ¿Quién va a ver cada entregable y qué no debe ver?
7. ¿Qué productos están ya decididos (marcas, modelos) y cuáles quedan «o equivalente»?
8. ¿Se quiere web? ¿Con qué dominio y abierta a quién?
9. ¿Qué hará la promotora con el edificio, venderlo o alquilarlo? ¿Con qué alcance se entrega cada unidad (local en bruto o
   con solado y techo; vivienda con cocina amueblada, con o sin electrodomésticos)? Las respuestas cambiaron el presupuesto.
10. ¿Cuál es la fecha de la licencia? Si el proyecto se redactó hace años, revisa la normativa aparecida desde entonces
    (ver la skill `comprobar-normativa`).
11. ¿En qué formato se imprimen los planos (A1 o A3)? ¿Dónde están el libro de estilo y las plantillas del estudio?

**En rehabilitación, además:**

12. ¿Qué manda, el levantamiento o los planos 2D?
13. ¿Qué fases hay y en qué orden se ejecutan?
14. ¿Qué es necesario y qué es extra?
15. ¿Cómo decide el cliente? (hojas A3 de decisión: ver la skill `decisiones-cliente`)

---

## 8. Dónde está cada cosa en ALFERECES, como ejemplo

| Tema | Archivo |
|---|---|
| Estado y cómo continuar | `SEGUIMIENTO_MEDICIONES/CONTEXTO_PARA_CONTINUAR.md` |
| Hallazgos y diario | `SEGUIMIENTO_MEDICIONES/REGISTRO_DE_TRABAJO.md` |
| Método de medición | `SEGUIMIENTO_MEDICIONES/METODO_DE_MEDICION.md` |
| Cambios del presupuesto | `TRABAJO_MEDICIONES/herramientas/cambios.json` |
| Cambios del modelo | `TRABAJO_REVIT_PE2026/registro_cambios.csv` |
| Láminas: qué sale del modelo y qué del proyecto | `TRABAJO_REVIT_PE2026/03_INFORME_PLANOS.md` |
| Modelo de instalaciones | `TRABAJO_REVIT_PE2026/MEP/INFORME_MEP.md` |
| Web: cómo se reconstruye y cómo se despliega | `WEB/LEEME.md` y `WEB/DESPLIEGUE.md` |
