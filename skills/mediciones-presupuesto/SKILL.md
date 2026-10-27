---
name: mediciones-presupuesto
description: "Método de AGOIN para medir, revisar y rehacer mediciones y presupuestos de obra con trazabilidad total. Cubre partidas, capítulos, líneas de medición, BC3/FIEBDC para Presto, Excel, presupuesto ciego para licitar, pliego de la oferta y comparativas de soluciones. Úsala siempre que trabajes con partidas, mediciones, BC3, Presto, presupuesto ciego, descompuestos o una licitación de obra. También cuando el usuario pregunte «de dónde sale» o «si es necesaria» una partida."
---

# Mediciones y presupuesto

El objetivo habitual es un presupuesto «perfecto, sin que falte nada».

- Va ciego, sin precios, para que oferten varias constructoras.
- Cada medición está justificada.
- El usuario lo revisa partida a partida y mide él mismo algunas cosas. Detecta enseguida un dato sin fuente. Un ejemplo real: la memoria daba una placa de anclaje de 700×700 mm que el plano dibujaba de 350×350.

## Cómo se revisa una partida

Responde estas cinco preguntas, en este orden:

1. **¿De dónde sale?**
   - Di la fuente: plano (lámina y zona), cuadro, memoria o presupuesto original.
   - Si nadie la encuentra en los planos, probablemente viene de una versión anterior del proyecto (otro uso, otro sistema). Dilo así.
2. **¿Es necesaria?**
   - ¿Duplica otra partida o la incluye otra en su precio?
   - ¿Es obligatoria, recomendable o sobra?
3. **¿Cuánto mide?**
   - Sigue la jerarquía de fuentes (abajo).
   - El texto de la partida dice qué fuente se usó, desglosada por piezas o tramos.
4. **¿Lo confirma el modelo?** Si el elemento está modelado, compara. Si no lo está y se puede, modélalo: modelar saca a la luz los errores.
5. **¿Qué es?** Una frase llana, y una imagen si ayuda. El usuario no tiene por qué conocer cada producto.

**Jerarquía de fuentes** para medir tú, de más a menos fiable. Las cifras que da el usuario mandan sobre ella una vez contrastadas:

1. cuadro del plano;
2. cota escrita;
3. medición justificada del proyecto;
4. escalado sobre el PDF vectorial;
5. recuento de símbolos;
6. dato del usuario;
7. estimación, marcada como tal.

Los cantos y espesores de estructura se leen en los planos de estructura, no en los detalles de arquitectura. Si la estructura se calculó con un programa, se leen en su listado, salvo que el usuario diga qué fuente manda.

## Cómo se trabaja con el usuario

- **Una partida o un bloque cada vez.** Se cierra y se sigue. Si pide un repaso rápido, dale lo esquemático y las medidas clave para que las compruebe él.
- **A «de dónde sale», responde con la fuente y una imagen del plano con lo medido marcado.** Así puede juzgarlo y validarlo.
- **Actúa solo con órdenes explícitas** («quítala de todos lados»). Lo demás queda como recomendación con su criterio.
- **Dudas de criterio** (PVC o ladrillo, lana o XPS, un diámetro u otro):
  - explica el criterio y recomienda;
  - no cambies la cantidad hasta que el usuario decida.
- **Alternativas caras o que cambian el proyecto** (canalón oculto, ascensor accesible, cocina equipada):
  - el presupuesto va con la opción sencilla;
  - aparte, un PDF de comparativa con plano, detalle y costes segregados, para decidir después.
- **Fija cada criterio una vez y aplícalo en todas partes.** Por ejemplo, no contar el empotramiento en jambas en ningún umbral. Escríbelo en el método de medición del proyecto.
- **Partidas que ningún plano define pero hacen falta:** inclúyelas donde lógicamente van y dilo. **Partidas dibujadas que faltan en el presupuesto:** añádelas.
- **Separa las partidas parecidas para no duplicar:** albardilla (coronación de muro), vierteaguas (alféizar de ventana), umbral (puerta), piezas de esquina.
- **Las diferencias por debajo del umbral que fije el usuario no son avisos** (en ALFERECES, el 5 %).
- **Si el usuario decide fuera de la conversación** (en un archivo de decisiones, o hablando con otro asistente):
  - aplica lo que esté claro;
  - pregunta lo que contradiga una decisión anterior o tenga cifras de una fuente equivocada.

## Control de cambios

- **Cada cambio va a un registro** (por ejemplo `cambios.json`) con:
  - id;
  - operación: borrar, insertar, modificar o renumerar;
  - motivo;
  - estado: propuesto, acordado o descartado;
  - si se aplica o no.
- **Los entregables se regeneran desde ese registro.** No se editan a mano.
- **«Quiero más información antes de confirmarlo»** se registra sin aplicar.
- **Si el usuario quiere repasar los cambios al final**, genera un Excel histórico de solo lectura: rojo lo borrado, verde lo añadido, azul lo modificado.
- **Tras cada ronda, regenera y comprueba:**
  - mediciones, versión ciega y BC3;
  - comprobación cruzada de los entregables;
  - lo que depende de ellos: pliego, cambios en planos, cambios en memoria, anejo y web.
  - Todo esto se regenera en local. Publicar la web o enviar documentos sigue necesitando la orden del usuario.
- **Antes de escribir un aviso sobre una partida, lee su historia en el registro**, no solo su texto actual. Un texto viejo llevó al usuario a borrar una partida por una premisa falsa.

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
- **Las mediciones del usuario mandan**, pero se contrastan. Si no cuadran, enséñale la diferencia y de dónde sale.

## BC3 y presupuesto ciego

- **Las mediciones van en las líneas de medición del BC3**, no solo en el texto de la partida.
  - Si una partida tiene varias piezas, cada una va en su línea.
  - Las líneas suman la cantidad.
  - El usuario lo pidió para ver en Presto de dónde sale cada número.
- **Valida el BC3 con un comprobador independiente:**
  - formato FIEBDC-3;
  - árbol de capítulos y partidas;
  - textos;
  - sumas de las líneas;
  - que el ciego no tenga precios;
  - que coincida con el Excel.
- **El ciego no lleva** precios, ni anotaciones internas de revisión, ni la comparación con el modelo. Busca palabras «testigo» internas para que no se cuele nada.
- **El Excel ciego puede ir con las hojas protegidas** y solo la columna de precio editable. Si lo proteges, dile al usuario la contraseña y dónde se fija.
- **Orden de capítulos y partidas:**
  - en orden de ejecución, si el usuario lo aprueba;
  - guarda la tabla de códigos antiguos → nuevos y traduce cada texto una sola vez.
- **Los archivos de Presto (.pzh) no se pueden leer.** Pide una exportación a Excel o BC3.

## Precios, al final

- **Con presupuesto ciego, los precios se revisan los últimos**, cuando el usuario reabra el tema. Antes no gastes esfuerzo en ellos ni propongas cambios de precio.
- **Las bases de precios con licencia** (por ejemplo la del colegio de aparejadores) solo se usan para contrastar internamente. Nunca se publican sus precios ni sus textos.

## Cruce con el modelo

- **Cada partida va enlazada a sus elementos del modelo**: directo, por capa, por estancia, por zona o sin elemento.
- **Lista aparte** los elementos sin partida y las partidas sin elemento.
- **La medida de cada componente puede verla la constructora si el usuario lo decide.** La comparación total y las desviaciones son internas.

## Antes de enviar a licitar

- **Comprueba que los documentos que se envían no se contradicen:** mediciones, pliego, cambios en planos, memoria y anejo. Un pliego excluía los electrodomésticos que las mediciones incluían.
- **Se envía solo con autorización expresa del usuario**, y después de que su equipo lo haya revisado.
