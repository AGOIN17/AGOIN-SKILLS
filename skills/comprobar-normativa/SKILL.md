---
name: comprobar-normativa
description: "[PROYECTO] Cómo comprobar normativa en un proyecto de AGOIN sin alarmar en falso ni dejarse nada: CTE (DB-SE, SI, SUA, HS, HR, HE), Código Estructural, RITE, REBT, ICT, accesibilidad, ordenanzas y planes especiales de cascos históricos. Exige leer el artículo oficial y citarlo, decir si algo está prohibido, restringido o permitido, revisar la normativa aparecida desde que se redactó el proyecto, calcular en vez de suponer y dejar escritas las reservas que el usuario acepta. Úsala cuando el usuario pregunte si algo cumple o se puede hacer, antes de avisar de un incumplimiento, al retomar un proyecto redactado hace años y al preparar la memoria o el pliego."
metadata:
  etiquetas: "PROYECTO"
---

# Comprobar normativa

Un aviso normativo equivocado hace perder tiempo y confianza; uno que falta sale caro en obra. En ALFERECES pasaron las dos cosas: se avisó de que el aluminio quizá no se admitía en el casco histórico (el artículo solo prohibía el PVC) y, a la vez, el proyecto no justificaba el radón aunque el municipio estaba en zona 2.

## 1. La fuente

- **Lee el artículo en la fuente oficial** (BOE, boletín autonómico o provincial, web del ayuntamiento) y **cítalo literalmente**, con su número. Nada de memoria ni de resúmenes de terceros, tampoco de la memoria del propio proyecto.
- **Di el grado:** prohibido, restringido a criterio del técnico o de la comisión, recomendado o permitido. En el caso del aluminio era «restringido», y vetado solo en miradores, que el proyecto no tenía.
- **Di la versión y la fecha** de la norma que aplicas, y por qué es esa (ver el apartado 2).
- **Si un aviso resulta infundado, retíralo de forma expresa** y anótalo en el registro del proyecto, para que no vuelva a salir.

## 2. Qué norma aplica

- **La fecha de la licencia o de la solicitud fija lo aplicable.** Pregúntala si no la tienes.
- **En proyectos redactados hace años que se reactivan, revisa lo aparecido desde entonces** y cómo aplica según esa fecha. Ejemplos:
  - DB-HS 6, protección frente al radón (2019): mira la zona del municipio;
  - Código Estructural (2021) frente a la EHE-08: comprueba que planos, memoria y presupuesto usan la misma;
  - DB-HE de 2019.
  - En ALFERECES los planos usaban el Código Estructural y el presupuesto la EHE-08.
- **Cascos históricos y planes especiales:** materiales y colores de fachada y carpintería, retranqueos, cubiertas, y qué instalaciones no pueden ir en fachada (unidades exteriores de climatización, por ejemplo: van a la cubierta o al patio, y eso se escribe en la partida con su izado).

## 3. Barrido del proyecto

- **Recorre los documentos del CTE uno a uno contra la memoria:** qué justifica, qué no y qué justifica mal. Haz una tabla: exigencia, dónde se justifica, resultado (cumple / no cumple / no justificado / no aplica) y fuente.
- **Lo que pide cálculo se calcula, no se supone:** pararrayos (SUA 8), rampas (SUA 1), ascensor accesible (SUA 9), resistencia al fuego bajo rasante (SI 6), ventilación (HS 3), regulación por estancia (RITE).
- **Antes de decir que algo incumple con medidas sacadas del modelo** (alturas libres, pendientes, gálibos), comprueba que esa zona está modelada como en los planos. Se avisó de alturas libres insuficientes y el usuario contestó: «lo estás midiendo mal… es por culpa de que está mal modelado» (ver `revision-modelo-bim`).
- **Instalaciones:** los criterios de detalle (tomas obligatorias, collarines o rejillas intumescentes, termostatos) están en `instalaciones-mep`. Compruébalos en cada proyecto; no los des por norma sin la cita.

## 4. Lo que se decide

- **Un incumplimiento que el usuario acepta** (por ser existente, por imposibilidad técnica, por criterio del técnico) queda escrito como reserva técnica en el registro del proyecto y, si afecta a la obra, en el pliego. No se vuelve a levantar.
- **Las propuestas para cumplir** siguen las reglas de `agoin-forma-de-trabajar`: opciones, criterio, recomendación, y el cambio mínimo si lo que hay ya cumple casi.
- **Si la respuesta depende de un tercero** (el ayuntamiento, la comisión de patrimonio, la distribuidora), dilo y prepara la consulta lista para enviar, sin enviarla.
