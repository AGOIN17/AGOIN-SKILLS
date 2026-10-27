---
name: nuevo-proyecto-arquitectura
description: "Cómo arrancar o retomar un proyecto de AGOIN con el método de ALFERECES. El método cubre el modelo Revit al día del proyecto de ejecución, las instalaciones, las mediciones y el presupuesto revisados, los documentos para licitar, la web y el vídeo. Esta skill da los documentos base que pedir, la estructura de carpetas, el orden de trabajo, los archivos de contexto para continuar entre sesiones y las preguntas del primer día. Úsala cuando el usuario empiece un proyecto o expediente nuevo, pregunte qué documentos necesita o cómo organizar las carpetas, quiera «hacer lo mismo que en ALFERECES» en otra obra o retome un trabajo largo de arquitectura u obra en una sesión nueva."
---

# Arrancar o retomar un proyecto

La guía completa del método está en `references/GUIA_METODO_AGOIN.md`. Se escribió con el usuario el 13/10/2026. Léela entera antes de empezar un proyecto nuevo, y cópiala a la carpeta del proyecto si no está.

## Lo esencial

- **Pide los documentos base** (apartado 2 de la guía).
  - **Imprescindibles:**
    - los planos del proyecto de ejecución en PDF vectorial, con todas las láminas;
    - la memoria completa;
    - el presupuesto en BC3;
    - el modelo o los DWG de partida.
  - **Muy convenientes:**
    - la lista de cambios posteriores al visado;
    - las cotas del solar y de las calles;
    - fotos del estado actual;
    - las referencias de producto ya decididas.
- **Haz las preguntas del primer día antes de modelar** (apartado 7 de la guía):
  - qué versión del proyecto manda;
  - qué está ya hecho o demolido en obra;
  - qué documento prevalece si se contradicen;
  - quién ve cada entregable.
- **Organiza las carpetas** según el apartado 3 de la guía:
  - lo recibido, en una carpeta de solo lectura;
  - decisiones;
  - modelo;
  - mediciones;
  - seguimiento;
  - web;
  - vídeo;
  - historial.
- **Comprueba que trabajas con la versión buena de los planos.** Puede haber borradores anteriores con el mismo nombre: mira las fechas y el sello de visado.
- **Si la carpeta del proyecto está en el servidor de la oficina, el servidor es de solo lectura.** Trabaja en una copia local y pide permiso para cualquier escritura.

## Para poder retomar en otra sesión

Lo que se habla en una conversación no pasa a la siguiente; los archivos sí. Mantén estos archivos en la carpeta de seguimiento:

- **`CONTEXTO_PARA_CONTINUAR.md`:** el estado actual, lo que está abierto, lo que espera al usuario y por dónde seguir.
- **`REGISTRO_DE_TRABAJO.md`:** los hallazgos numerados (H-xxx) y un diario.
- **`METODO_DE_MEDICION.md`:** los criterios acordados con el usuario.
- **Los registros de cambios** del modelo y del presupuesto.

**Cuándo leerlos y cuándo actualizarlos:**

- Al empezar una sesión de un trabajo en marcha, lee esos archivos primero y sigue desde el punto pendiente.
- Al cerrar una etapa, actualízalos sin esperar a que te lo pidan. Apunta el estado, las decisiones, lo pendiente y las trampas, no una lista de commits.
- **Trabaja en una sola copia del proyecto.** Si hay copias antiguas en otra unidad, no las edites: otra sesión editó una copia vieja y hubo que juntar los cambios a mano.

## Skills relacionadas

- `agoin-forma-de-trabajar`
- `mediciones-presupuesto`
- `revit-automatizacion`
- `revision-modelo-bim`
- `planos-laminas`
- `acotar-planos`
- `instalaciones-mep`
- `calculo-estructural`
- `web-proyecto`
- `video-render-arquitectura`
- `informes-tecnicos`
