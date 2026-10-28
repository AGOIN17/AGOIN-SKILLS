---
name: decisiones-cliente
description: "[ESTILO · PROYECTO] Cómo lleva AGOIN las cuestiones abiertas de un proyecto hasta que el usuario o el cliente deciden: registro de cuestiones, preguntas clave para fijar un criterio, dudas numeradas con respuesta propuesta, hojas A3 de decisión con opciones A/B/C y coste solo de lo que cambia, hojas de propuestas de distribución, hojas de dudas para dibujar a mano con rejilla, planos de trabajo, alternativas modeladas sin opciones de diseño, «solución adoptada» y separar lo necesario de los extras. Úsala cuando haya que preparar algo para que alguien decida, cuando el usuario diga «prepárame unas preguntas», «hazme un planito para dibujar», «que el cliente elija» o «vamos a apuntar las cuestiones», y antes de modelar alternativas."
metadata:
  etiquetas: "ESTILO, PROYECTO"
---

# Decisiones del usuario y del cliente

El usuario quiere decidir «de forma informada y lo más eficiente posible», desde una sola hoja, y revisar «poco a poco». El proyecto no cambia hasta que alguien decide. Las reglas generales de proponer y decidir están en `agoin-forma-de-trabajar` (§2); aquí está el método completo, que se probó en CHIVERO y el usuario aprobó.

## 1. El registro

En el archivo de plan del proyecto (`00_PLAN.md` o el de contexto), arriba del todo:

- **«Cuestiones para proponer al cliente»:** Nº (C1…C10) | Cuestión | Lo que ya hay | Lo que falta para proponer | Estado. Actualiza el estado cada vez que una avance y enlaza su hoja. El usuario lo pidió así: «vamos a apuntar porque hay varias cuestiones que hay que ir solucionando y proponiendo… para pasárselo al cliente y que él vaya decidiendo».
- **«Criterio fijado por el estudio (fecha)»:** las respuestas del usuario citadas.
- **«Decisiones tomadas por Claude, para revisar»:** Fecha | Decisión | Por qué | Alternativa. Cuando el usuario delega mucho («confío en tu criterio… quiero que las tomes y luego revisemos»), decides y avanzas, pero queda claro qué decidiste tú.
- **«Lo que pide el cliente en su croquis y cómo está»:** si el cliente dibujó algo a mano, se respeta punto por punto salvo donde el estudio diga otra cosa, y esta tabla lo demuestra.

**Ordena las cuestiones por dependencias** y propón ese orden: niveles con suelos; techos con la estructura de cubierta; la sala de instalaciones antes que las zanjas; porches con la acera. Al final pueden juntarse en un «cuaderno de decisiones» con índice y estado.

## 2. Fijar un criterio antes de optimizar

Antes de optimizar algo con muchas variables (cotas, tierras, costes), fija el criterio con el usuario:

- **De 5 a 10 preguntas clave numeradas**, cada una con opciones a/b y tu recomendación, para que conteste corto («1a, 2a, 3b…»).
- **Una lista de «doy por supuesto, salvo que me digas otra cosa».**
- Con sus respuestas, escribe el criterio en el archivo de plan, citándolo.

El usuario pidió «hazme unas preguntas clave para establecer un criterio que nos va a dar la solución óptima», contestó en una línea y el criterio sirvió para todas las viviendas.

**Cuando mande una foto o un boceto y pida «dime qué dudas tienes»,** devuelve las dudas numeradas, cada una con la respuesta que propones. Así puede contestar «adelante con lo tuyo» o corregir solo algunas, y tú aplicas las que no ha corregido. Así se cerraron ocho dudas en un mensaje.

## 3. Hojas para decidir

Todas en A3, con el mismo cajetín del estudio (ver `libro-estilo-agoin`). No las numeres REV: en AGOIN, REV es el plano de revisiones.

### Hoja de decisión (DEC.xx o una por cuestión, Cn.mm)

- La cuestión en una frase y la situación actual.
- **Opciones A/B/C** (A = como va el proyecto), en columnas o filas, **con las mismas vistas y el mismo encuadre** en todas: dos axonometrías y una planta, o planta, alzado y secciones tipo.
- Superposiciones que enseñan el problema: rojo lo que falla, azul lo que funciona.
- **Una tabla solo de lo que cambia:** cantidades medidas, coste y diferencia frente a A, diciendo que es una estimación y de qué base sale.
  - **En hojas para el cliente, solo totales y diferencias.** Ni códigos ni precios unitarios de una base de precios con licencia (ver `mediciones-presupuesto`).
- A favor y en contra de cada opción, y una valoración rápida con puntos (aspecto, duración, mantenimiento, coste).
- La recomendación (✔), casillas «Elige» y si las opciones se pueden combinar.
- Al pie, los criterios comunes y lo descartado.
- **Alternativas de instalaciones** (suelo radiante o radiadores, aire o agua): trazado completo de cada una, pros y contras, coste de la diferencia y gasto de energía anual con sus hipótesis a la vista (precio del kWh, rendimiento estacional).

### Hoja de propuestas de distribución (DIS.xx)

- Una fila por propuesta: planta, descripción, a favor y en contra.
- Columna derecha con la duda, la recomendación, las casillas y las notas.
- Di si las opciones se pueden mezclar por estancia.
- Encaja cada mueble a su muro aunque no esté a escuadra, y di cuánto se desvía cada muro.

### Hoja de dudas para dibujar a mano (DUDA.xx)

Petición expresa del usuario: «todas las cosas que tengas dudas, me preparas un planito para imprimir y dibujar a mano la solución».

- Plantas giradas al eje del edificio.
- **Rejilla de 1 m con letras a lo largo y números a lo ancho**, para pasar el croquis escaneado a coordenadas del modelo. Guarda la correspondencia de cada hoja.
- Lo que hay que confirmar, numerado y en rojo; pregunta y casillas en la columna derecha.
- Las dudas rápidas, juntas en una hoja de «decisiones rápidas».

### Plano de trabajo para dibujar encima (TR.xx)

- El conjunto lo más grande que quepa en A3; gíralo 90° si hace falta y usa la hoja hasta el marco.
- Rótulos de vivienda pequeños, de una línea, en gris.
- Nombres de estancia fuera de los edificios, en columnas a lo largo de la fachada, con directriz fina y un punto en la estancia; en cada estancia, su luz libre y su cota de suelo.
- Cotas del terreno en los puntos clave y curvas de nivel cada 0,10 m (maestras cada 0,50 m, rotuladas).
- La nube de puntos de fondo, muy tenue; lo que no toca, en medio tono.
- El usuario dibuja a mano encima y no quiere que nada le estorbe.

## 4. Modelar las alternativas

- **Antes de modelar, confirma en una línea** qué es A, qué es B y qué vas a medir.
- **Modela solo lo que cambia,** con el detalle justo para que cambie el coste o la decisión.
- **Sin opciones de diseño** (no se pueden manejar por API): copias apartadas de los elementos, marcadas y excluidas de la medición del proyecto. Las trampas de copiar en Revit están en `revit-automatizacion` (`trampas-revit.md`, §5).
- Si el usuario quiere pasar de una opción a otra «como en el programa», dale vistas gemelas con el mismo encuadre para alternar con Ctrl+Tab, y ofrece preparar la vía oficial si aun así la quiere.
- **El proyecto sigue con la opción A** hasta que se decida.

## 5. Cuando se decide

1. Aplica la opción a los elementos reales.
2. Borra las copias de las alternativas, con su confirmación.
3. Regenera mediciones, planos y presupuesto.
4. Saca la hoja otra vez como **«solución adoptada»** con la versión siguiente, conservando la de opciones. Las correcciones posteriores van a la versión siguiente.
5. Actualiza el registro y el archivo de plan.

## 6. Qué se propone primero

- **Lo necesario primero, los extras aparte** (porches, jardín), con una comparación con y sin ellos.
- El orden que marcó el usuario: niveles → acabados de suelos, paredes, techos y fachada («para que el cliente se haga una idea») → extras.
- **Siempre con recomendación.** Una cuestión por hoja.
