---
name: calculo-estructural
description: "Cómo comprobar, calcular o proponer estructura y cimentación para AGOIN, con Robot Structural Analysis (por API o por su ventana), cálculos propios en Python, CTE DB-SE, EHE/EC2 y EC7, y cómo entregarlo al estructurista sin presentarlo como validado. Cubre fuentes originales (estudio geotécnico, listado de cálculo), todas las cargas y combinaciones con viento, hipótesis a la vista, sensibilidad, revisión independiente, resultado cumple / no cumple / quizás, documentos del propio programa y propuestas mínimas parecidas a lo proyectado. Úsala siempre que se pida comprobar, calcular, dimensionar, optimizar o justificar vigas, pilares, zapatas, losas, muros o cimentaciones, o preparar algo para el calculista."
---

# Cálculo estructural

La estructura la firma el estructurista. El trabajo aquí tiene dos destinatarios:

- **el estructurista:** una comprobación honesta, trazable y fácil de revisar;
- **el usuario:** una respuesta clara (cumple, no cumple o quizás) y por qué.

## Antes de calcular

- **Entiende para qué sirve cada elemento.** Un zuncho de arriostramiento contra el viento y el pandeo no es una viga de carga, y una viga de atado tampoco.
- **Reformula el problema al usuario antes de cambiar nada.** Él lo pide así.
- **Lee las fuentes originales:**
  - el estudio geotécnico: tensión admisible, terreno, nivel freático, agresividad;
  - la memoria y el listado del programa de cálculo;
  - los planos de estructura.
  - Los resúmenes no sirven. La memoria del propio estudio atribuía al geotécnico requisitos que el geotécnico no decía.
- **Si el proyecto se calculó con un programa (CYPE…), usa su listado**, no tu interpretación del dibujo.
- **Si las fuentes se contradicen,** por ejemplo el cálculo con zapatas aisladas y el plano con zapatas combinadas, dilo y sigue la que indique el usuario.
- **Antes de proponer otra solución, comprueba si cumple la original.**
  - Si cumple, se queda.
  - Si no cumple, di exactamente qué falla y propone el cambio mínimo.
- **Las propuestas, lo menos invasivas posible y parecidas a lo proyectado.** Los límites reales suelen estar en la obra: excavar en roca, restos arqueológicos, ventanas que no se pueden tocar.

## Cargas e hipótesis

- **Usa las cargas del código (CTE DB-SE-AE) y las de la memoria,** y di cuáles son.
- **Incluye el viento y todas las combinaciones:** ELU, ELS y equilibrio.
  - No dejes fuera un caso porque «seguramente no converge». Pruébalo.
  - Una vez se excluyó el viento por esa suposición; al probarlo, resolvía bien.
- **Deja a la vista las hipótesis del modelo:**
  - apoyos;
  - rigidez del terreno (balasto);
  - rozamiento;
  - placas de anclaje;
  - materiales: un material genérico dio un peso propio unas 10 veces menor que el real.
- **Si una equivalencia es tuya,** dilo y pide que la valide el estructurista. Por ejemplo, convertir una tensión admisible en una carga mayorada con un factor.
- **Haz análisis de sensibilidad en lo incierto,** como el balasto bajo, medio y alto. Si el resultado cambia de sentido, dilo.

## Comprobación

- **Comprueba todo lo que miraría el estructurista:**
  - tensiones, despegue, vuelco y deslizamiento;
  - flexión y cortante (con y sin cercos) y punzonamiento;
  - anclaje de pernos y placas;
  - armado mínimo y fisuración;
  - pandeo y estabilidad global.
- **Pide una revisión independiente:** un segundo agente revisa los scripts de cálculo antes de entregar. Si encuentra un error, corrige, recalcula y regenera.
- **Contrasta tu cálculo con el programa (o al revés).** Explica las diferencias por el método de cada uno, no ajustando los números.
- **Si una herramienta sustituye a una hoja de cálculo existente,** valídala con los resultados de esa hoja y documenta cada desviación.

## Entrega

- **Resultado por elemento:** cumple, no cumple o quizás, con la razón en una línea y el margen.
- **Un recuadro «Para el estructurista»** con los puntos que debe mirar.
- **Procedencia de cada figura y cada plano.**
  - Di qué sale del programa (sus informes, mapas, notas y planos de ejecución) y qué has dibujado tú.
  - El usuario preguntó «¿los has reconstruido tú o son de Robot?» y quiso ver los documentos del propio programa. Cuando existan, inclúyelos en un anejo.
- **Un apartado «Lo que no cubre».**
- **No escribas «aprobado» ni «validado» mientras no lo esté.**
  - Mientras tanto: «propuesta pendiente de validar por el estructurista».
  - Cuando lo apruebe, anota quién y cuándo. En ALFERECES, el calculista dio el visto bueno el 21/10 y así se registró.
- **Ver también la skill `informes-tecnicos`.**

## Robot Structural Analysis

- `references/robot.md`: trampas de la API COM y del módulo de zapatas, y cómo manejar la ventana de Robot cuando la API no llega.
- `scripts/rtf_unir_tablas.py`: convierte las notas RTF de Robot a PDF sin que salgan letras griegas.
