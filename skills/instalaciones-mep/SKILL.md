---
name: instalaciones-mep
description: "Criterios para diseñar, modelar, medir y revisar instalaciones de edificación (saneamiento, pluviales, fontanería, climatización y suelo radiante, ventilación, electricidad, telecomunicaciones, protección contra incendios) que se puedan construir. Cubre trazados sencillos, una altura por sistema, coordinación con techos y estructura, recuento fiable de mecanismos y trampas de Revit MEP. Úsala al trazar o revisar redes en un modelo BIM o en planos, al decidir alturas de falso techo o pasos de instalaciones, al modelar instalaciones «como un experto BIM» y al medir partidas de instalaciones."
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
- **Orden de reconstrucción:** si una red crea los aparatos de los que cuelga otra, reconstruye en ese orden. Después, vuelve a pasar los circuitos y las comprobaciones.

## Suelo radiante: criterios que funcionaron

- **Tubo:** en espiral doble por estancia. La separación sale del cálculo de calefacción; en ALFERECES, 15 cm entre tubos y 10 cm a los muros.
- **Idas:** por los pasillos y los huecos de las puertas, en un solo plano y sin cruces.
- **Dónde no va:**
  - bajo platos de ducha, inodoros y unidades interiores;
  - dentro de armarios;
  - en los vestíbulos comunes.
- **Se modela con sus capas** (panel, tubo, mortero y acabado), para que se vea en vídeos e imágenes.

## Electricidad y telecomunicaciones

- **Recuenta los mecanismos sobre el plano vectorial,** por la forma de su símbolo, y confírmalos en ampliaciones. Lee las notas de la lámina: «x2» son dos bases.
- **Explica al usuario los elementos que puede no conocer** (clemas, toma coaxial, cajas de termostato, collarines intumescentes):
  - qué son;
  - si son obligatorios;
  - si todavía se usan;
  - el mínimo necesario.
- **Acometidas:**
  - si no se sabe dónde llega cada servicio, la partida queda abierta con la nota «a definir en obra»;
  - con una foto o un dato del usuario, se ajusta todo lo que depende de ella: CGP, LGA y registro de enlace.

## Revit MEP: trampas

- **Codos:** deben girar entre unos 6° y 90°.
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
