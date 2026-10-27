---
name: revision-modelo-bim
description: "Lista de comprobación para revisar un modelo BIM (Revit u otro) antes de darlo por bueno, enseñarlo o sacar de él planos, vídeo, imágenes o web. Busca que nada flote, que nada atraviese muros ni salga por la fachada, que anclajes y pasos tengan profundidad real, que fachadas y carpinterías sean iguales a los planos, que losas, escaleras, barandillas y techos sean coherentes, y que no haya regresiones respecto a versiones anteriores. Úsala al terminar de modelar o de cambiar algo, cuando el usuario pida comprobar que «todo queda bien» o señale un fallo en el 3D, y antes de cualquier exportación."
---

# Revisar un modelo antes de enseñarlo

El usuario mira el 3D con ojo de arquitecto y de obra. Los fallos que más le molestan son los «descarados»:

- un tubo que sale por la fachada;
- anclajes de pasamanos que atraviesan el muro entero;
- una luminaria flotando o un grifo en el aire;
- una cama cruzada con un muro.

Uno solo de estos fallos hace dudar de todo el modelo, así que hay que encontrarlos antes de que los vea él.

## 1. Lo físicamente imposible

Búscalo siempre.

- **Elementos que no apoyan en nada:** luminarias, ventiladores, aparatos, grifos, rejillas.
  - Deben apoyar en el techo, la pared o el suelo reales que tienen encima o detrás. En escaleras y dobles alturas, el techo no está donde dice el nivel.
  - Calcula la altura a partir del elemento real (lanzando rayos contra la geometría), no con una cota fija.
- **Lo que atraviesa:**
  - anclajes, tacos, pasamuros y tuberías deben tener su profundidad real: un anclaje de pasamanos entra como mucho unos 10 cm;
  - muebles, camas y puertas que cruzan muros;
  - losas que cruzan ventanas;
  - tabiques que atraviesan forjados;
  - barandillas que cruzan muros.
- **Lo que se sale del edificio:**
  - trazados que salen por la fachada; en fachadas oblicuas, una ruta en L se sale, así que compruébala contra los contornos de las estancias;
  - cantos de forjado que asoman en la fachada;
  - muros de sótano que se ven por encima de la acera;
  - piezas que asoman fuera de la cara exterior.
- **Lo que no sigue a su soporte:**
  - barandillas que no acompañan la pendiente de la escalera;
  - techos que cortan un tramo de escalera;
  - puertas que abren contra un muro, o al revés que en el plano.
- **Caras coplanares que se solapan:** parpadean en el render y en el vídeo. Pasa en la zapata enrasada con el fondo del pozo, en los muros contra el terreno y en las jambas.

## 2. Fiel a los planos

- **Fachadas exactamente como los alzados:**
  - materiales y sus juntas: dónde acaba el zócalo y por dónde cae el cambio de paño;
  - paños enrasados, sin aristas visibles salvo en rehundidos y cambios de material;
  - cargaderos y vierteaguas como en el alzado.
- **Carpinterías según su ficha:**
  - el tipo (las ventanas triples, sin ladrillo entre medias);
  - el sentido de apertura;
  - el alféizar visible: algunas familias traen su propio alféizar anidado, que tapa el de piedra.
- **Espesores y cantos de estructura:** se toman de los planos de estructura. Un alero medía 15 cm en estructura y 25 cm en el detalle de arquitectura; manda estructura, salvo que el usuario diga otra cosa.
- **Cotas de calle y del terreno:** se leen en los alzados y las secciones, no en el terreno de un modelo heredado.
- **Lo que el proyecto no define:** modélalo donde lógicamente va y dilo.
- **Contradicciones entre los planos de arquitectura, estructura e instalaciones:** lístalas para el usuario, con la regla de prioridad que haya dado.

## 3. Sin regresiones

- **Compara con el estado anterior:** vídeo, imágenes, láminas o la copia del modelo. Lo que estaba bien debe seguir bien.
  - El usuario recuerda cómo estaba en el primer 3D y pregunta «¿por qué ahora ha cambiado?».
  - Antes de cambiar algo que ya estaba resuelto, mira cómo estaba y por qué.
- **Tras editar muros o plantillas:**
  - compara las posiciones de puertas y ventanas con la copia;
  - compara las láminas con el juego anterior.

## 4. Cómo revisar

- **Pasadas automáticas:**
  - interferencias entre disciplinas y con la arquitectura;
  - elementos fuera de los contornos;
  - elementos sin apoyo;
  - caras coplanares;
  - número y área de las habitaciones.
- **Pasada visual:**
  - cortes por planta;
  - secciones por los huecos y las escaleras;
  - cada fachada frente a su alzado;
  - a una resolución que deje ver los centímetros.
- **Mira tú las imágenes** (en hojas de contactos), no solo los números. El usuario lo pide así: «haz pruebas y visualiza».
- **Si el programa está ocupado con otro proyecto,** revisa sobre una exportación de la geometría: vistas por profundidad, cortes y rayos.
- **Corrige en el modelo los errores reales** y anótalos en el registro. Lo que hayas decidido tú, márcalo como criterio propio.

Para hacerlo en Revit sin tocar la interfaz del usuario, usa la skill `revit-automatizacion`.
