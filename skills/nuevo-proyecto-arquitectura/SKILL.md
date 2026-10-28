---
name: nuevo-proyecto-arquitectura
description: "[PROYECTO] Cómo arrancar o retomar un proyecto de AGOIN con el método de ALFERECES y CHIVERO. El método cubre el modelo Revit al día del proyecto de ejecución, las instalaciones, las mediciones y el presupuesto revisados, los documentos para licitar, la web y el vídeo. Esta skill da los documentos base que pedir, la estructura de carpetas, el orden de trabajo, los archivos de contexto para continuar entre sesiones y las preguntas del primer día. Úsala cuando el usuario empiece un proyecto o expediente nuevo, pregunte qué documentos necesita o cómo organizar las carpetas, quiera «hacer lo mismo que en ALFERECES» en otra obra o retome un trabajo largo de arquitectura u obra en una sesión nueva."
metadata:
  etiquetas: "PROYECTO"
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
  - quién ve cada entregable;
  - si la promotora venderá o alquilará, y con qué alcance se entrega cada unidad;
  - la fecha de la licencia (normativa aplicable);
  - el formato de los planos y dónde están el libro de estilo y las plantillas;
  - en rehabilitación: qué manda (levantamiento o 2D), qué fases hay, qué es necesario y qué extra, y cómo decide el cliente.
- **Copia las referencias del estudio** (libro de estilo, plantillas, proyectos modelo) a una carpeta `referencias/copias` y trabaja sobre las copias. Las de versión antigua las actualiza el usuario.
- **Organiza las carpetas** según el apartado 3 de la guía (o su variante con un único `00_PLAN.md`):
  - lo recibido, en una carpeta de solo lectura;
  - decisiones;
  - modelo;
  - mediciones;
  - seguimiento;
  - web;
  - vídeo;
  - historial.
- **Comprueba que trabajas con la versión buena de los planos.** Puede haber borradores anteriores con el mismo nombre: mira las fechas y el sello de visado.
- **Para reconstruir el historial administrativo de un expediente,** léelo todo, no una muestra («¿HAS ABIERTO TODAS LAS CARPETAS Y REVISADO TODO?»):
  - reparte las carpetas por años entre pocos agentes en paralelo;
  - en cada entrada, di si se leyó el documento o solo se deduce del nombre de la carpeta, que puede engañar (una carpeta de «informe de excavación» contenía una resolución);
  - anota los documentos de otras obras mal archivados y las fechas o importes que no cuadran;
  - si un PDF grande falla al leerlo, reinténtalo solo o por páginas antes de darlo por ilegible (cuatro se leyeron al reintentar).
- **Si la carpeta del proyecto está en el servidor de la oficina, el servidor es de solo lectura.** Trabaja en una copia local y pide permiso para cualquier escritura.

## Para poder retomar en otra sesión

Lo que se habla en una conversación no pasa a la siguiente; los archivos sí. Mantén estos archivos en la carpeta de seguimiento:

- **`CONTEXTO_PARA_CONTINUAR.md`:** el estado actual, lo que está abierto, lo que espera al usuario y por dónde seguir.
- **`REGISTRO_DE_TRABAJO.md`:** los hallazgos numerados (H-xxx) y un diario.
- **`METODO_DE_MEDICION.md`:** los criterios acordados con el usuario.
- **`CRITERIOS.md`:** las decisiones de criterio, cada una con la regla general que deja.
- **Variante con un único archivo de plan** (`00_PLAN.md`, como en CHIVERO), que se lee lo primero: el encargo; el modelo vigente y los anteriores; los entregables vigentes con su versión; los criterios fijados con fecha y cita; la hoja de ruta; el registro de cuestiones para el cliente; las decisiones tomadas por Claude para revisar; una sección por tema con su cadena de scripts; lo pendiente; y el orden para regenerar todo.
- **Los registros de cambios** del modelo y del presupuesto.

**Cuándo leerlos y cuándo actualizarlos:**

- Al empezar una sesión de un trabajo en marcha, lee esos archivos primero y sigue desde el punto pendiente.
- Al cerrar una etapa, actualízalos sin esperar a que te lo pidan. Apunta el estado, las decisiones, lo pendiente y las trampas, no una lista de commits.
- **Trabaja en una sola copia del proyecto.** Si hay copias antiguas en otra unidad, no las edites: otra sesión editó una copia vieja y hubo que juntar los cambios a mano.
- **Si hace falta una sesión nueva** (por ejemplo, tras instalar un servidor MCP, que solo se carga al arrancar), da al usuario la frase exacta para pegar: «Lee los archivos de seguimiento y continúa desde el punto pendiente del archivo de contexto».

## Skills relacionadas

- `agoin-forma-de-trabajar`
- `libro-estilo-agoin`
- `decisiones-cliente`
- `rehabilitacion-levantamiento`
- `comprobar-normativa`
- `optimizar-trabajo`
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
