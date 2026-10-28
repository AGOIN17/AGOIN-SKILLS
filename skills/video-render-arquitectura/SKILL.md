---
name: video-render-arquitectura
description: "[BLENDER] Cómo hacer vídeos de construcción (4D), animaciones, imágenes y portadas de un proyecto de arquitectura a partir del modelo (Revit → Blender) con el gusto del estudio. Cubre el estilo «dibujo de concurso», plano y casi monocromo, sin figuras humanas; una cámara que siempre deja ver lo que se coloca; una secuencia de obra real; fidelidad a los planos sin parpadeos; y fotos de estancias con criterio de fotografía inmobiliaria. Úsala al preparar o corregir vídeos, renders, imágenes o portadas de un proyecto, o cuando el usuario señale algo raro en un vídeo."
metadata:
  etiquetas: "BLENDER"
---

# Vídeo e imágenes del proyecto

El usuario compara el vídeo con los planos y ve enseguida los fallos: un ladrillo de otro color, un muro que atraviesa una escalera, una losa cruzando una ventana. Un vídeo con errores del modelo desacredita el modelo. Por eso primero se revisa el modelo (skill `revision-modelo-bim`) y después se renderiza.

## Gusto del estudio

- **Estilo «dibujo de concurso»:**
  - casi monocromo y plano;
  - líneas finas, y negro grueso solo en lo cortado (poché);
  - tramas finas en el ladrillo, la cubierta y los pavimentos;
  - sombras suaves y claras, sin superficies oscuras;
  - color solo en las redes de instalaciones, dibujadas como trazos puros.
- **Sin figuras humanas, salvo que el usuario las pida.** En ALFERECES las rechazó dos veces, también como siluetas planas. No las propongas de nuevo.
- **Música:** pregunta antes. En la web el vídeo va sin música.
- **Si se amuebla:** interiorismo con buen gusto, a partir de las referencias que dé el usuario.
- **Imágenes reales:** si el usuario deja sus propias imágenes para un uso, se usan esas y solo esas. Una imagen generada con IA se marca como orientativa y se compara con el original, porque la IA se inventa el entorno.

## Secuencia de obra

- **Sigue un orden de construcción real y coherente,** planificado antes por planta y por oficio.
- **No enseñes lo que ya está hecho en obra.** Si ya se demolió, no hay demoliciones; si solo se excavan pozos y zanjas, no hay vaciado general. Tampoco versiones superadas de una instalación.
- **Cada capa aparece cuando toca:**
  1. estructura;
  2. tabiquería;
  3. instalaciones, con lo que queda delante semitransparente;
  4. suelo radiante, con su panel, su tubo y su mortero;
  5. acabados, al final.
- **Etiquetas en cada instalación,** si ayudan a entender.

## Cámara

- **Siempre se ve lo que se está colocando.** Nada de muros delante; acércate a lo que entra en ese momento.
- **Trayectoria suave** que nunca atraviese el edificio: una órbita muestreada fotograma a fotograma.
- **Tras cambiar la cámara,** compara fotograma a fotograma y renderiza solo lo que ha cambiado.

## Parpadeos y otros defectos

- **Caras coplanares** (zapata enrasada con el fondo, muro contra el terreno, jambas): parpadean. Contrae cada malla unos milímetros hacia dentro, con una prioridad por categoría, y sube el `clip_start` de la cámara.
- **Ocultar objetos en Blender:** la visibilidad está animada. Para ocultar algo, quita antes sus curvas de animación de ocultación.
- **Estilo dibujo, trampas conocidas:**
  - un filtro de Sobel sobre la profundidad marca los planos rasantes: usa el laplaciano, solo del lado lejano;
  - los identificadores de cryptomatte llegan a 1e37: compara ln|id|;
  - la luz física no da interiores planos en un corte: compón pasadas (color difuso × sombra u oclusión suaves + emisión);
  - apaga las sombras de las luces interiores: no se ven y multiplicaban por diez el tiempo de cada fotograma (de 51 s a 5 s).
- **Trampas de Blender 4.4:**
  - con las acciones por «slots», la curva de `ortho_scale` no se puede tocar: crea una acción aparte;
  - un material nuevo puede no traer el nodo «Principled BSDF»: crea los nodos tú;
  - el Python de Blender no trae PIL: genera esas imágenes con el Python del sistema.
- **No renderices fotos y vídeo a la vez en la misma tarjeta gráfica:** el vídeo se arrastró mientras se hacían las fotos.
- **Antes del render completo,** saca cinco fotogramas de prueba y míralos tú.

## Fotos de estancias (tipo inmobiliaria)

- **Cámara:** a nivel, con desplazamiento de lente para que las verticales salgan rectas; a 1,25–1,45 m de altura; objetivo de 16–20 mm.
- **Luz:** de día, con un relleno suave.
- **Escena:** techos limpios (oculta las instalaciones solo para la foto).
- **Ajuste:** balance de blancos.

## Mantenerlo al día

- **Tras un cambio en el modelo:**
  1. vuelve a exportar la geometría;
  2. vuelve a planificar la secuencia (los ids cambian);
  3. monta la escena y saca la prueba;
  4. haz el render, de forma que se pueda reanudar;
  5. monta el vídeo.
- **Un render completo puede llevar horas.** Avisa del tiempo antes, y no lo lances sin que el usuario lo quiera.
- **Numera los fotogramas con ceros a la izquierda y ordénalos por número:** ordenado como texto, s_10006 va antes que s_1006, y el short salió con los fotogramas del final en medio.
- **No identifiques una toma por su número de fotograma** de una versión a otra: el plan de obra cambia de duración. Búscala por su tarea o su nombre. La portada de la web salió con otra cámara porque el plan nuevo tenía 109 fotogramas más.
- **Con vídeos de casi 1 GB, ofrece de entrada una copia ligera:** unos 200 MB, y otra de menos de 30 MB a 1280 px para mensajería.
- **Escribe el vídeo final con un nombre temporal y renómbralo al terminar:** el usuario puede tener abierto el anterior en el reproductor.
- **No publiques un vídeo que ya no corresponde al modelo.** El usuario prefirió quitarlo de la web hasta rehacerlo.
