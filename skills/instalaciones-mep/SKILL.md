---
name: instalaciones-mep
description: "[INSTALACIONES] Criterios para diseñar, modelar, medir y revisar instalaciones de edificación (saneamiento, pluviales, fontanería, climatización y suelo radiante, ventilación, electricidad, telecomunicaciones, protección contra incendios) que se puedan construir. Cubre trazados sencillos, una altura por sistema, coordinación con techos y estructura, recuento fiable de mecanismos y trampas de Revit MEP. Úsala al trazar o revisar redes en un modelo BIM o en planos, al decidir alturas de falso techo o pasos de instalaciones, al modelar instalaciones «como un experto BIM», al comparar alternativas (suelo radiante o radiadores) y al medir partidas de instalaciones."
metadata:
  etiquetas: "INSTALACIONES"
---

# Instalaciones

## Trazados construibles

El usuario vio un colector de pluviales con diagonales y codos raros. Pidió «recorridos sencillos que no entren en conflicto con nada y fáciles de ejecutar en obra». Esto se aplica desde el diseño, no como arreglo después.

- **Paralelos a los ejes del edificio** o al muro que acompañan. Nada de diagonales cruzando estancias ni zigzags cortos.
- **Giros a 90°.** A 45° solo donde es la pieza normal: saneamiento y conductos.
- **Una altura fija por sistema.** Los cruces se resuelven por nivel, no con quiebros ni bajadas locales.
- **En fachadas oblicuas una L puede salirse del edificio.** Comprueba cada ruta contra los contornos de las estancias.
- **Nada por dentro de cuartos de contadores** ni de armarios de otras instalaciones. Si un desagüe pasa por ahí, desvíalo.
- **Con roca o restos arqueológicos, cuanta menos zanja mejor.** Mejor colgar los colectores del techo que enterrarlos.
- **Antes de construir, compruébalo con dos cosas:**
  - un script que busque codos raros;
  - un plano de trazados por franja de techo.
- **Si queda algún cruce inevitable, explícalo.**
- **Diseña las redes como datos (JSON) y compruébalas fuera de Revit** (holguras, choques, codos raros, alturas contra los techos) antes de construirlas. Después de construir, repite la comprobación en el modelo: la del diseño no ve las bajadas a los conectores ni los flexibles. Así hubo menos diálogos de Revit y el suelo radiante se reconstruyó en segundos cuando cambió el criterio.
- **Cada punto de agua y de desagüe llega al aparato real:** el fregadero de una isla, no el muro más cercano. Un revisor encontró desagües de cocina en medio del salón.
- **Sin familias ni tipos MEP** (anteproyecto, básico), modela las redes de criterio como DirectShapes en categorías MEP, con un color por red y una leyenda «Colores del modelo 3D». Ocúltalas en todas las vistas menos en las suyas, y di que el trazado real lo hace el instalador.

## Coordinación

- **Falsos techos:** la altura la decide el usuario.
  - Deja como mínimo el hueco que pida (por ejemplo, 10 cm libres) y comprueba que las redes caben.
  - Lo que no quepa, dilo con números.
- **Conductos:** circulares donde hay sitio, rectangulares planos donde el falso techo va justo. El criterio es el caudal y la cámara disponible.
- **Patinillos compartidos entre viviendas:** antes de compartir un conducto, comprueba la sección, el aislamiento acústico y si linda con dormitorios.
- **Interferencias:**
  - se revisan entre redes, y con la arquitectura y la estructura;
  - los pasos por la estructura se modelan como huecos o pasatubos previstos.
- **Los aparatos de techo cuelgan del techo real.** Ver la skill `revision-modelo-bim`.
- **Orden de reconstrucción:** si una red crea los aparatos de los que cuelga otra, reconstruye en ese orden (saneamiento, fontanería, climatización…). Después, vuelve a pasar las interferencias, los huecos y pasatubos, los circuitos y las comprobaciones: se saltó un paso y salieron pasatubos para rutas antiguas.
- **Antes de fijar diámetros de conexión, lee la ficha técnica del equipo elegido** (sus bocas de entrada y salida). La ficha daba 4 entradas de Ø80 y una salida de Ø125 frente al Ø160 del plano. Los cambios de diámetro, con una pieza cónica gradual.
- **El equipo rotulado en el plano coincide con la memoria y con el suministro:** potencia, monofásico o trifásico, potencia contratada. En un esquema eléctrico se había quedado el bloque de otro proyecto con una aerotermia trifásica mucho mayor.
- **Sala de instalaciones:** va donde la pida el cliente solo si cabe; si no, propón otra y dilo con números. Comprueba que la potencia de los equipos sigue sirviendo cuando entran fases nuevas.
- **En cascos históricos,** mira qué prohíbe la ordenanza en fachada (unidades exteriores de climatización) y escríbelo en la partida: el equipo va a la cubierta o al patio, con su izado (ver `comprobar-normativa`).

## Suelo radiante: criterios que funcionaron

- **Tubo:** en espiral doble por estancia. La separación sale del cálculo de calefacción; en ALFERECES, 15 cm entre tubos y 10 cm a los muros.
- **Idas:** por los pasillos y los huecos de las puertas, en un solo plano y sin cruces.
- **Dónde no va:**
  - bajo platos de ducha, inodoros y unidades interiores;
  - dentro de armarios;
  - en los vestíbulos comunes.
- **Se modela con sus capas** (panel, tubo, mortero y acabado), para que se vea en vídeos e imágenes.
- **Para comparar con radiadores,** modela los radiadores bajo las ventanas con todos sus circuitos, y da el coste de la diferencia y el gasto anual con sus hipótesis (ver `decisiones-cliente`).

## Electricidad y telecomunicaciones

- **Recuenta los mecanismos sobre el plano vectorial,** por la forma de su símbolo, y confírmalos en ampliaciones. Lee las notas de la lámina: «x2» son dos bases.
- **Explica al usuario los elementos que puede no conocer** (clemas, toma coaxial, cajas de termostato, collarines intumescentes):
  - qué son;
  - si son obligatorios;
  - si todavía se usan;
  - el mínimo necesario.
- **Criterios que se explicaron al usuario** (compruébalos con la norma en cada proyecto):
  - termostatos: el RITE pide regulación por estancia (cita la instrucción técnica vigente); uno por vivienda no cumple;
  - base de 25 A: como mínimo una por cocina;
  - toma coaxial: el tubo y el registro siempre; el cable y la toma, solo si lo pide la consulta al operador;
  - interruptor de 16 A: no es obligatorio y sobra salvo para termo o toallero;
  - pasos de tubos de plástico por elementos de compartimentación: collarín intumescente (DB-SI 1); rejilla intumescente solo donde pasa aire entre sectores.
- **Estudio lumínico de proyecto:** método del flujo más un mapa por puntos, con la media de la rejilla escalada a la del método; el factor de luz diurna sin ×100 de más; para la luz natural, «bien / justo / escaso» con la misma cifra que se rotula. Di que no es una simulación DIALux.
- **Acometidas:**
  - si no se sabe dónde llega cada servicio, la partida queda abierta con la nota «a definir en obra»;
  - con una foto o un dato del usuario, se ajusta todo lo que depende de ella: CGP, LGA y registro de enlace.
- **Puesta a tierra en roca:** un anillo bajo la solera más las armaduras de las zapatas, con las picas en los pozos de las zapatas, sin arquetas ni zanja propia. «Cuanto menos haya que picar, mejor».

## Revit MEP: trampas

- **Codos** (umbrales observados en Revit 2027): deben girar entre unos 6° y 90°.
  - Los giros de menos de 3° se omiten.
  - Donde cambia el diámetro, esos giros pequeños fallan: pon la reducción en un tramo recto.
- **Tes:** solo funcionan si la derivación se desvía menos de un 1 % de la perpendicular.
- **Dos codos de 90° en conductos de Ø125:** necesitan unos 0,38 m entre ellos. Si no hay sitio, usa codos de 45°.
- **Recargar una familia con instancias conectadas** abre un diálogo bloqueante. Borra la red antes.
- **Tipo flexible:** elígelo por la clase de sistema. El mismo nombre existe en tuberías y en conductos.
- **Conectores eléctricos:**
  - el sistema es `PowerBalanced`; `PowerCircuit` no tiene tensión ni carga;
  - `VoltageType` va en voltios sin convertir (230, 400).
- **Plantillas españolas de luminarias:** ponen la fuente de luz como una esfera 1,5 m por encima de la luminaria, que da choques falsos. Muévela o exclúyela.
- **Marcas duplicadas:** usa un identificador de diseño como Marca, y el texto descriptivo en otro parámetro.
- **El modelo de instalaciones va aparte y vinculado.** Se edita con el vínculo descargado en el modelo de arquitectura (ver la skill `revit-automatizacion`).
- **No exportes IFC por la API** en la sesión compartida: cerró Revit.
