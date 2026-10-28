---
name: rehabilitacion-levantamiento
description: "[PROYECTO · REVIT] Cómo rehabilitar o reformar un edificio existente a partir de un levantamiento (escáner, nube de puntos, modelo Revit del estado actual, fotos de dron, DWG de reforma): qué fuente manda, pasar el DWG al modelo, fantasmas del levantamiento, leer niveles y aparejos en la nube, georreferenciar fotos, fases de obra en Revit, y criterios del estudio para cotas de suelo, huecos, trasdosados, fachadas de tierra y cal, amianto, porches bajo el alero y exteriores sin muros de contención. Úsala en cualquier proyecto de rehabilitación, reforma, ampliación o cambio de uso sobre algo existente, al trabajar con una nube de puntos o un levantamiento, y al decidir cotas, fases o derribos."
metadata:
  etiquetas: "PROYECTO, REVIT"
---

# Rehabilitar sobre un levantamiento

Salió de CHIVERO: unas naves rurales existentes que se rehabilitan por fases, con un levantamiento por escáner (modelo y nube de puntos), fotos de dron y unos planos 2D de reforma. Las reglas de fuentes y método son generales. Las de diseño (apartado 5) son criterios del estudio: aplícalas como punto de partida y confírmalas en cada obra.

Las trampas de la API de Revit que aparecen aquí (fases, habitaciones, nube de puntos, cotas ancladas) están en `revit-automatizacion` → `references/trampas-revit.md`.

## 1. Qué fuente manda

- **El levantamiento manda sobre los planos 2D aproximados.** «Los planos 2D son aproximados, lo que está bien de verdad es el revit del estado actual». El 2D estaba dibujado sobre una base más vieja, con errores de centímetros hasta casi un metro.
  - Del levantamiento salen los huecos existentes, las caras de muro y los espesores.
  - Del 2D sale la intención: qué estancias, qué tabiques, qué huecos pasan a puerta o ventana, el mobiliario.
  - No fuerces las superficies del modelo para que cuadren con las rotuladas en el 2D.
  - Pregunta el primer día qué fuente manda.
- **El modelo del levantamiento es original: no se toca nunca.** Se trabaja sobre una copia.
- **Las cotas del levantamiento están ancladas a aristas de muro y a jambas.** Cuéntalas antes y después de cada cambio y redibuja las que se pierdan: en una pasada se perdieron 33 de 181.

## 2. Del DWG de reforma al modelo

- **Identifica la convención de capas** antes de nada: existente que se queda, derribo, relleno, trasdosado, tabique nuevo, barridos de puerta, bloques de superficie.
- **Registra el DWG sobre el modelo** con una transformación medida (con varios puntos y su error). En CHIVERO era casi una traslación, con 1 a 2 cm de ajuste por edificio.
- **Lee lo que el dibujo no dice:** los rótulos de zona pueden nombrar lo que tienen a un lado; los barridos de puerta son cuartos de círculo cerrados.
- **Convertir DWG a DXF** con ODA File Converter: comprueba antes su licencia (la gratuita es para uso no comercial).
- **Los modelos de levantamiento traen fantasmas:** elementos por encima del plano de corte que no salen en ninguna planta (un muro diagonal de 7 cm que «ni existe»), ventanas genéricas de 1,00 m de alto exacto, líneas de ubicación fuera del eje. Revisa en 3D y pregunta antes de construir sobre ellos. Cuando el usuario no encuentre un elemento, mándale una captura con él resaltado, no su id.

## 3. Nube de puntos, dron y fotos

- **Niveles reales desde la nube:**
  - cortes cada metro a lo largo de cada nave para la altura útil bajo la estructura de cubierta;
  - una rejilla por estancia para el suelo existente;
  - descarta los cortes donde un techo plano (cañizo) tapa la cubierta.
- **Aparejo de una fachada pintada** (para despieces o para decidir el acabado):
  - lee el relieve, no el color;
  - mide la hilada en una esquina limpia;
  - usa la anisotropía del relieve con un umbral **por fachada**, porque la trama del escáner cambia de una a otra;
  - da la fiabilidad por fachada: qué se revisó pieza a pieza y qué es intuido; «intuir sin inventar cosas evidentes que están mal»;
  - si lo pidió «por probar tus capacidades», trátalo como un ensayo y propón revisarlo juntos.
- **Fotos de dron** (DJI): guardan el GPS y el giro de la cámara en el XMP. Con dos puntos de control (una esquina, una chimenea), una transformación de semejanza lleva la foto al modelo. Si el usuario marca derribos sobre una foto, pásalos a elementos y confirma que lo no marcado se queda.
- **Calcar una propuesta de un dossier** (un jardín): georreferencia la página con varias esquinas del edificio y da el error (en CHIVERO, 8 esquinas y 0,35 m como mucho).
- **La nube como fondo de un plano** se hace con una imagen aclarada, no con medio tono (Revit lo ignora en nubes): ver `revit-automatizacion/references/trampas-revit.md` §6.

## 4. Fases

- **Fases típicas:** Existente → F1A → F1B → F2 → F3 (exteriores). Cada derribo va en la fase en que se hace.
- **Todo lo de una misma partida, en la misma fase,** para que se mida bien. Una red compartida toma la fase más temprana de las unidades que la usan.
- **Para ver el resultado:** vistas por fase con el filtro «Reformado» (existente + nuevo). Si el usuario pregunta «¿cómo puedo verlo por fases?», explícale el filtro y la fase de la vista.
- **Si le distraen las fases siguientes,** trabaja en una copia del modelo solo con las necesarias, deja la completa intacta y di a los scripts cuál es cuál.
- **Mediciones por fase:** ver `mediciones-presupuesto`.

## 5. Criterios de rehabilitación del estudio

Confírmalos en cada proyecto; en CHIVERO los fijó el usuario. Mandan siempre la normativa de habitabilidad, la ordenanza y el CTE aplicables: compruébalos con `comprobar-normativa`.

### Cotas de suelo y techos

- Un solo nivel de suelo y uno de falso techo por vivienda.
- Ninguna estancia vividera por debajo de 2,50 m libres, con el falso techo lo más alto que deje la estructura de cubierta. En baños, pasillos y almacenes, 2,20 m como mínimo absoluto, y solo si evita picar mucho.
- **Picar es más caro que rellenar:** sube el suelo todo lo posible, conserva las soleras sanas y recrece encima.
- Entrada a nivel, con la acera en pendiente hacia fuera; un escalón por debajo solo si protege del agua y ahorra picar.
- **Tras fijar las cotas,** da una tabla con cada hueco existente: antepecho y cargadero respecto al suelo nuevo, y cuáles hay que subir. Revisa los umbrales de las puertas que se conservan: aparecieron umbrales por debajo del suelo nuevo.
- Cambiar el nivel de una unidad deja cortos sus tabiques y trasdosados: comprueba que cada muro llega a su techo.

### Envolvente

- **Trasdosados** en todas las unidades calefactadas; cortados en cada hueco de alféizar a dintel, sin invadir la ventana; con un retorno aislado (unos 3,5 cm) en las jambas hasta el marco («los trasdosados no dan la vuelta en las ventanas»). Si escuadran una estancia, sin comerse mucha superficie.
- **Huecos:** unifica los nuevos donde se pueda, pero los irregulares existentes «tienen gracia». Amplía los que hagan falta para la luz natural (en CHIVERO, hueco de al menos el 12,5 % de la superficie útil de la estancia).
- **Fachadas de adobe, tapial o ladrillo de conservación desconocida:** limpieza, quitar lo que no deja respirar, revoco de cal en toda la fachada, zócalo pintado opcional, y las reparaciones que aparezcan al limpiar, aparte.
- **Remates** (umbrales, vierteaguas, albardillas) a juego con el acabado: con encalado blanco, cemento blanco o piedra artificial blanca, no granito («de granito con el encalado blanco no pegan»). Da alternativas y un remate por hueco.
- **Fibrocemento:** mídelo como amianto, en partida aparte, hasta que se confirme, con una hoja de duda para confirmarlo. Si lo es, su retirada la hace una empresa inscrita en el RERA con plan de trabajo aprobado (RD 396/2006).

### Porches añadidos

- **Arrancan siempre por debajo del alero existente,** para que el agua del tejado caiga sobre ellos. Nunca por encima ni prolongando la cubierta principal con un quiebro. Mide el alero en la nube y pon la cubierta del porche unos 5 cm por debajo.
- Comprueba la altura libre (DB-SUA). Si la teja no cabe por pendiente, chapa de junta alzada con poca pendiente.
- Anclar a un muro de tapial necesita ensayo, o una segunda fila de pilares. El viento de succión suele mandar (ver `calculo-estructural`).

### Exteriores

- **Sin muros de contención si se puede:** desmontes 1:2 plantados y terraplenes 1:3 transitables, anchos y suaves para que se integren (el usuario pidió uno a 1:8).
- Plataformas horizontales o con un 1 % como mucho.
- Escaleras de huella regular de 30 cm, que acaban alineadas con el final del edificio («volúmenes limpios»), con jardinera integrada al lado.
- Aceras pegadas al muro, esquinas pavimentadas, una sola línea recta de borde por nave, siguiendo el terreno natural (pendiente máxima del 10 %) para no picar. Conserva las existentes que se puedan.
- **Escombros pétreos limpios** de los derribos pueden ir a relleno machacados en obra: cuantifícalo con hipótesis explícitas (parte pétrea, rendimiento). Bajo suelos interiores necesita el visto bueno de la dirección facultativa, y la reutilización debe constar en el estudio de gestión de residuos (RD 105/2008).
- **Planos de tierras y niveles:** ver `planos-laminas` (movimiento de tierras, estudio de niveles por fachada).
