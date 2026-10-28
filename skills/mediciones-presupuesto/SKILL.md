---
name: mediciones-presupuesto
description: "[MEDICIONES] Método de AGOIN para medir, revisar y rehacer mediciones y presupuestos de obra con trazabilidad total. Cubre partidas, capítulos, líneas de medición, BC3/FIEBDC para Presto, Excel, presupuesto ciego para licitar, partidas que faltan o se pagan dos veces, pliego de la oferta y comparativas de soluciones. Úsala siempre que trabajes con partidas, mediciones, BC3, Presto, presupuesto ciego, descompuestos, bases de precios o una licitación de obra. También cuando el usuario pregunte «de dónde sale» o «si es necesaria» una partida."
metadata:
  etiquetas: "MEDICIONES"
---

# Mediciones y presupuesto

El objetivo habitual es un presupuesto «perfecto, sin que falte nada».

- Va ciego, sin precios, para que oferten varias constructoras.
- Cada medición está justificada.
- El usuario lo revisa partida a partida y mide él mismo algunas cosas. Detecta enseguida un dato sin fuente. Un ejemplo real: la memoria daba una placa de anclaje de 700×700 mm que el plano dibujaba de 350×350.

Listas de apoyo en `references/`:

- `omisiones-tipicas.md`: lo que suele faltar en un presupuesto. Repásala siempre que el encargo sea «que no falte nada».
- `revision-forma-y-bc3.md`: la revisión automática de forma tras cada regeneración y las trampas del formato BC3.

## Cómo se revisa una partida

Responde estas cinco preguntas, en este orden:

1. **¿De dónde sale?**
   - Di la fuente: plano (lámina y zona), cuadro, memoria o presupuesto original.
   - Si nadie la encuentra en los planos, probablemente viene de una versión anterior del proyecto (otro uso, otro sistema). Dilo así.
   - Una «cantidad alzada» sin líneas de medición no tiene respaldo. Búscala en los planos y, si no aparece, dilo («sale solo del presupuesto»).
2. **¿Es necesaria?**
   - ¿Duplica otra partida o la incluye otra en su precio? Lee qué incluye cada unidad, en su descompuesto o en el de la base de precios. Casos reales de doble pago: la tapa ya incluida en la arqueta y medida además aparte; el punto conmutado, que ya incluye los dos conmutadores, contado una vez por conmutador; las líneas frigoríficas incluidas en el equipo y medidas aparte.
   - Antes de crear una partida nueva, busca en todos los textos, también en los «incluso…», si otra ya la incluye.
   - ¿Es obligatoria, recomendable o sobra?
3. **¿Cuánto mide?**
   - Sigue la jerarquía de fuentes (abajo).
   - El texto de la partida dice qué fuente se usó, desglosada por piezas o tramos.
4. **¿Lo confirma el modelo?** Si el elemento está modelado, compara. Si no lo está y se puede, modélalo: modelar saca a la luz los errores.
5. **¿Qué es?** Una frase llana, y una imagen si ayuda. El usuario no tiene por qué conocer cada producto.

**Marca en cada partida cómo se ha comprobado:** medida por ti con su fuente, dato del usuario, adoptada del proyecto sin contrastar, o estimada. Lo adoptado sin contrastar no cuenta como «revisado». Cuenta con un script las partidas de cada grupo, no de memoria: se dijo que había 11 partidas estimadas y eran 16, y en dos bloques se adoptaron mediciones sin contrastar («¿no íbamos a ir poco a poco revisando todo medición por medición?»).

**Jerarquía de fuentes** para medir tú, de más a menos fiable. Las cifras que da el usuario mandan sobre ella una vez contrastadas:

1. cuadro del plano;
2. cota escrita;
3. medición justificada del proyecto;
4. escalado sobre el PDF vectorial;
5. recuento de símbolos;
6. dato del usuario;
7. estimación, marcada como tal.

- **En unidades, el cuadro tiene que coincidir con lo dibujado.** Si no coincide, es una discrepancia que se comunica, no gana el cuadro solo por ser el primero. Una ficha de carpintería decía 3 unidades y solo había una dibujada.
- **Las carpinterías se cuentan con tres fuentes independientes:** las unidades de la ficha, las etiquetas dibujadas en las plantas y el modelo energético del HE 1 (superficie por hueco). El cruce destapó además dos erratas de medidas.
- Los cantos y espesores de estructura se leen en los planos de estructura, no en los detalles de arquitectura. Si la estructura se calculó con un programa, se leen en su listado, salvo que el usuario diga qué fuente manda.
- **Medir por color sobre una imagen sirve para detectar que falta algo, no para fijar la cantidad** (±10 %). Márcalo como aproximado y sustitúyelo por la medición buena del CAD o del usuario.

## Cómo se trabaja con el usuario

- **Una partida o un bloque cada vez.** Se cierra y se sigue.
- **A «de dónde sale», responde con la fuente y una imagen del plano con lo medido marcado.** Así puede juzgarlo y validarlo.
- **Si pide un resumen para comprobar rápido,** dale las medidas clave ordenadas por el dinero que ponen en riesgo: «si las cinco primeras cuadran, tienes controlado el 80 % del dinero dudoso».
- **Si quiere medir a la par** («yo también lo mido a ver si nos sale lo mismo»), dale una lista numerada en tres grupos: longitudes en planta, alturas de la sección y unidades que contar. Luego compara sus cifras con las tuyas.
- **Cuando te dé una superficie o una longitud, pregúntale qué incluye** antes de usarla: huecos de escalera, ascensor y rampa, zapatas, muros existentes. Dio superficies de forjado sin descontar huecos y lo avisó después.
- **Si él puede sacar un dato exacto en un minuto** (superficies de losa por espesor en Revit, una longitud en CAD), pídeselo antes de pasar horas escalando un PDF. Tu medición detecta el problema; la suya lo cierra.
- **Lo que no puedas medir bien tú solo, dilo** y propón hacerlo con él por partes, con las partidas marcadas como provisionales. No lo rellenes con cifras dudosas. Pasó con el recuento de mecanismos eléctricos.
- **Mientras revisa partidas, cambia solo lo que ordene de forma expresa** («quítala de todos lados»). Lo que solo pregunta o duda queda como recomendación con su criterio. Lo que te ha encargado hacer (medir un capítulo, rehacer una partida) lo haces.
- **Dudas de criterio** (PVC o ladrillo, lana o XPS, un diámetro u otro):
  - explica el criterio y recomienda;
  - no cambies la cantidad hasta que el usuario decida.
- **Si delega la decisión** («el que mejor quepa y se use habitualmente»), que no es lo mismo que una duda que tiene que resolver él: decide, explica el criterio y regístralo como `propuesto`.
  - Lo propuesto puede aplicarse a los entregables locales para que lo vea, marcado y reversible.
  - En cada mensaje di qué está aplicado sin confirmar y qué está solo registrado. En ALFERECES unos propuestos estaban aplicados y otros no, y hubo que preguntarlo varias veces.
  - Nada propuesto sin confirmar se envía ni se publica.
- **Alternativas caras o que cambian el proyecto** (canalón oculto, ascensor accesible, cocina equipada):
  - el presupuesto va con la opción sencilla;
  - aparte, un PDF de comparativa con plano, detalle y costes segregados, para decidir después (ver `informes-tecnicos`).
- **Fija cada criterio una vez y aplícalo en todas partes.** Escríbelo en el método de medición del proyecto. Ejemplos generalizables:
  - no contar el empotramiento en jambas en ningún umbral;
  - el trasdosado con aislamiento llega a la cara inferior del forjado, no a la altura del techo;
  - la protección pasiva de pilares se mide por caras expuestas: exentos, en muro y embebidos por separado.
- **Partidas que ningún plano define pero hacen falta:** inclúyelas donde lógicamente van y dilo. **Partidas dibujadas que faltan en el presupuesto:** añádelas.
- **Separa las partidas parecidas para no duplicar:** albardilla (coronación de muro), vierteaguas (alféizar de ventana), umbral (puerta), piezas de esquina.
- **Las diferencias por debajo del umbral que fije el usuario no son avisos** (en ALFERECES, el 5 %).
- **Si el usuario decide fuera de la conversación** (en un archivo de decisiones, o hablando con otro asistente):
  - aplica lo que esté claro;
  - pregunta lo que contradiga una decisión anterior o tenga cifras de una fuente equivocada.
- **Si trae una auditoría o revisión de otro asistente,** comprueba cada punto contra los archivos y clasifícalo: cierto o falso con la prueba, si contradice una decisión ya tomada, y si mejora lo que había. Reconoce los errores propios y rechaza los falsos positivos con su dato.

## Encontrar lo que falta y lo que sobra

- **Repasa `references/omisiones-tipicas.md`.** En ALFERECES faltaba cerca de un 20 % del PEM declarado.
- **Recorre una base de precios capítulo a capítulo** y compara cada subcapítulo con el presupuesto. Busca las exclusiones del tipo «no incluye X, que se mide en su capítulo» y comprueba que ese capítulo existe y la mide. Así salieron 33 faltas, varias excluidas «porque se mide en su capítulo» sin estar en ninguno.
- **Busca restos de otros proyectos del estudio:**
  - nombres de calles u obras ajenas en las líneas de medición (búscalos por texto);
  - bloques de biblioteca en los planos que rotulan otro equipo u otra potencia;
  - tipos o referencias que no aparecen en ningún plano ni en la memoria;
  - documentos de otra obra mal archivados.
  - Una partida de revestimientos estaba medida con las calles de otro edificio.
- **Distingue lo común del edificio de lo de cada vivienda o local.** La acometida, la CGP, el tronco general de agua o la ICT común se cuentan una vez; la CGP estaba medida cuatro veces.
- **Contrasta cada superficie con la útil y la construida del proyecto.** Ninguna partida de suelo puede pasar de la superficie que cubre. Solapes y mermas van en el precio, no en la medición: el suelo radiante medía más que toda la superficie útil.
- **Antes de medir medios auxiliares, mira si ya los incluye otra oferta** (el andamio de la cubierta sirve para la fachada: «podríamos usar ese mismo andamio»).

## Medir por fases y desde el modelo (rehabilitación)

- **Cada elemento con su fase de creación y de derribo;** cada partida con líneas detalladas (uds × L × a × h) por fase; los criterios, en el propio script y en una hoja «Criterios» del libro. Capítulos en orden de obra, con los extras (porches, jardín) al final; renumera al cerrar.
- **Si la herramienta de destino no tiene fases,** empieza el comentario de cada línea con la fase («1A · …»).
- **Cuenta las piezas por hueco del estado reformado, no por instancia de carpintería.** Dos carpinterías en un mismo hueco cuentan una vez; los huecos cegados no son huecos. Contrasta con el plano reformado. «Hay veces que pones dos vierteaguas en una sola ventana».
- **Fachadas:** una prueba solo en planta se deja los testeros en esquinas y escalones, el muro por encima de la cubierta más baja del vecino y las chimeneas; en CHIVERO sumaron 67 m² más. Comprueba que el contorno queda cubierto entero y que ningún paño se cuenta dos veces, y dale al usuario una planta con cada paño coloreado por fase.
- **Movimiento de tierras** por fase y por material (excavación, solera picada, zahorra, encachado, tierra vegetal), con una rejilla común y un dueño por celda para que los solapes no se cuenten dos veces; los taludes, fuera de las piezas. Comprueba cada fórmula con un caso a mano: un `max` que debía ser `min` infravaloró un relleno.
- **Alternativas de acabado que el cliente elegirá** (laminado o porcelánico por vivienda): se miden las dos con la misma cantidad, en partidas paralelas. Lo que no admite opción va aparte. Si la herramienta admite variables o grupos de selección, úsalos; si no, deja la opción por defecto y dilo.

## Pasar partidas a una base de precios o a una herramienta

- **Antes de cargar nada,** prepara una tabla con tu partida, el código elegido, el encaje (exacto, aproximado o sin equivalente), las cantidades por fase y el factor de conversión de unidades (m³ → m², m → m³) escrito en el comentario. Las partidas sin equivalente se enseñan al usuario como «precio propio» antes de crearlas; las dudas se agrupan para el arquitecto.
- **Lee qué trae dentro cada partida de la base:** una de inversor fotovoltaico incluía 27 placas; un suelo radiante «sistema completo» por m² ya incluye tubo, colector y panel que quizá mides aparte. Si la exportación corta los textos, léelos en el BC3.
- **Si la herramienta es una app de AGOIN en producción** (el Generador de precios), sigue las reglas de `desarrollo-apps-agoin`: solo añadir, solo en el presupuesto nombrado, registro reanudable.

## Control de cambios

- **Cada cambio va a un registro** (por ejemplo `cambios.json`) con:
  - id;
  - operación: borrar, insertar, modificar o renumerar;
  - motivo;
  - estado: propuesto, acordado o descartado;
  - si se aplica o no.
- **Los entregables se regeneran desde ese registro.** No se editan a mano.
- **«Quiero más información antes de confirmarlo»** se registra sin aplicar.
- **Cuando cambies una partida, cambia a la vez la cantidad, el resumen, el texto y el desglose.** Un script comprueba después que el desglose escrito suma la cantidad: un texto decía 45,80 m y la cantidad seguía en 65,00.
- **Después de un cambio de proyecto, repasa los textos de las partidas afectadas,** no solo sus cantidades: quedaron «dos locales» cuando ya había uno y «modelo de gres» en un solado de mármol.
- **Si una comprobación cruzada no cuadra, no ajustes el número: abre un hallazgo** con lo que no cuadra. Así salieron un duplicado, unas placas de anclaje de otra estructura y albardillas sin presupuestar.
- **Si el usuario quiere repasar los cambios al final**, genera un Excel histórico de solo lectura: rojo lo borrado, verde lo añadido, azul lo modificado.
- **Tras cada ronda, regenera todo de una vez y siempre en el mismo orden:**
  1. mediciones;
  2. ciego;
  3. BC3;
  4. comprobación cruzada de los entregables;
  5. lo que depende de ellos: pliego, cambios en planos, cambios en memoria, anejo y web.
  - Comprueba que todos llevan la misma hora, para que no haya versiones cruzadas.
  - Pasa la revisión de forma automática de `references/revision-forma-y-bc3.md`: tarda segundos y la primera vez sacó 103 incidencias.
  - Todo esto se regenera en local. Publicar la web o enviar documentos sigue necesitando la orden del usuario.
- **Di qué cubre cada comprobación.** «0 incidencias» en la revisión de forma no significa que las mediciones estén bien. Se presentó como revisión final un «TODO CORRECTO» que solo era de forma.
- **Antes de escribir un aviso sobre una partida, lee su historia en el registro**, no solo su texto actual. Un texto viejo llevó al usuario a borrar una partida por una premisa falsa.
- **Si te piden un informe del método de medición,** incluye tus propios errores (cómo se detectaron y qué lección deja cada uno) y lo que no has medido. Ese apartado le dice al usuario dónde mirar.

## Trampas de medición que ya han pasado

- Se restó algo que no estaba dentro del total: un alero fuera del contorno medido.
- **Contar símbolos solo con un script no basta**: los pegados a un muro se funden con él.
  - Cuenta sobre el PDF vectorial y confirma a la vista en ampliaciones.
  - Lee las notas de la lámina: «x2» junto a un enchufe son dos bases.
- **Los textos convertidos a contorno** (espesores de losa en los planos de estructura) no salen al extraer texto. Solo se leen en una imagen.
- **Las superficies del modelo con acabados no sirven para medir estructura.**
  - Las losas se miden por planta y por espesor sobre los planos de estructura.
  - Se miden hasta la cara exterior de los zunchos, y los huecos por la cara interior.
- **Hay cantidades heredadas de una versión anterior del proyecto.** Si una partida no casa con nada, búscala en los proyectos anteriores.
- **Al empezar, reúne todas las versiones del presupuesto y compáralas:** BC3, Excel y el capítulo de la memoria. Pueden reutilizar los mismos códigos con otro contenido, así que **enlázalas por el texto, no por el código**. El Excel había perdido 10 de 28 huecos que la memoria tenía bien.
- **Al extraer un presupuesto de un PDF, valida cada partida (cantidad × precio = importe) y cada capítulo contra su total impreso.** Lo que no cuadra está mal leído: el subtotal de un subcapítulo desplaza las cifras de la última partida, y un número suelto se toma por un código. No uses la extracción hasta que cuadre.
- **Las mediciones del usuario mandan**, pero se contrastan. Si no cuadran, enséñale la diferencia y de dónde sale.

## BC3 y presupuesto ciego

- **Las mediciones van en las líneas de medición del BC3**, no solo en el texto de la partida.
  - Si una partida tiene varias piezas, cada una va en su línea.
  - Las líneas suman la cantidad.
  - El usuario lo pidió para ver en Presto de dónde sale cada número.
- **Valida el BC3 con un comprobador independiente:** formato FIEBDC-3, árbol de capítulos y partidas, textos, sumas de las líneas, que el ciego no tenga precios y que coincida con el Excel.
  - Independiente de verdad: un comprobador que lee con la misma codificación que el generador dio por bueno un BC3 sin juego de caracteres declarado.
  - **La prueba final es importarlo en Presto** y mirar una partida con tildes y su tabla de mediciones. Las trampas del formato están en `references/revision-forma-y-bc3.md`.
- **El ciego no lleva** precios, ni anotaciones internas de revisión, ni la comparación con el modelo.
  - Limpia las anotaciones con sustituciones exactas y ordenadas, no borrando frases enteras: un filtro por frases dejó una partida sin su cantidad.
  - Haz que la generación se pare si queda alguna palabra «testigo» interna.
- **El Excel ciego puede ir con las hojas protegidas** y solo la columna de precio editable. Si lo proteges, dile al usuario la contraseña y dónde se fija.
- **Cada partida, un concepto único y bien nombrado, sin mezclar:** la zanja aparte de la tubería; la losa aparte de las vigas y los zunchos. Así un programa de presupuestos la reconoce y genera sus descompuestos.
  - Si muchos precios del proyecto son múltiplos exactos de una misma cifra, se pusieron a ojo, sin descompuesto: díselo al usuario.
- **Define cada material para que las ofertas sean comparables:** producto de referencia «o similar» con formato, acabado y gama; prestaciones con su norma (clases UNE-EN); y por escrito los acabados que no se admiten (por ejemplo, un lacado que la ordenanza prohíbe). Si el usuario da como referencia las calidades de otra obra, úsalas como «del estilo o similar».
- **Orden de capítulos y partidas:**
  - en orden de ejecución, si el usuario lo aprueba;
  - guarda la tabla de códigos antiguos → nuevos y traduce cada texto una sola vez.
- **Los archivos de Presto (.pzh) no se pueden leer.** Pide una exportación a Excel o BC3.

## Precios, al final

- **Con presupuesto ciego, los precios se revisan los últimos**, cuando el usuario reabra el tema. Antes no gastes esfuerzo en ellos ni propongas cambios de precio.
- **Si hace falta un precio objetivo interno** antes de eso, usa los precios del propio proyecto y marca los estimados, sin proponer cambios.
- **Para contrastar con una base de precios antigua,** usa solo internamente un coeficiente de actualización con su fuente citada. Las partidas sin equivalente quedan vacías (`null`), no a cero: con ceros salen desviaciones falsas del −100 %.
- **Las bases de precios con licencia** (por ejemplo la del colegio de aparejadores) solo se usan para contrastar internamente. Nunca se publican sus precios ni sus textos.
  - En hojas para el cliente o la promotora, solo totales y diferencias, diciendo que son una estimación; ni códigos ni precios unitarios de la base. La obra recibe el presupuesto del estudio, nunca los precios de la base.

## Cruce con el modelo

- **Cada partida va enlazada a sus elementos del modelo**: directo, por capa, por estancia, por zona o sin elemento.
- **Lista aparte** los elementos sin partida y las partidas sin elemento.
- **La medida de cada componente puede verla la constructora si el usuario lo decide.** La comparación total y las desviaciones son internas.
- **Antes de publicar esas medidas, concilia las partidas con desviaciones grandes** y di cuántas son: las constructoras las van a ver. En ALFERECES, 19 de 43 partidas se desviaban más de un 15 %.

## Antes de enviar a licitar

- **Comprueba que los documentos que se envían no se contradicen:** mediciones, pliego, cambios en planos, memoria y anejo. Un pliego excluía los electrodomésticos que las mediciones incluían.
- **Lo que no se puede cerrar antes de licitar no se deja abierto sin más:**
  - fija una base común escrita en el texto (por ejemplo, «hasta N m de acometida en vía pública, con rotura y reposición») y un precio por metro para el exceso;
  - o declárala en el pliego como medición provisional que se liquida según lo realmente ejecutado;
  - lo especializado, como el ascensor, va incluido para que lo cotice la constructora, con la cláusula de que diga si no lo incluye («debe ir incluido, y si no, que lo digan»).
- **Se envía solo con autorización expresa del usuario**, y después de que su equipo lo haya revisado.
