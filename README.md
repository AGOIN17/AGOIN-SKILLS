# AGOIN-SKILLS

Este repositorio reúne las skills de Claude Code de AGOIN.

- **Qué es una skill:** un conjunto de instrucciones que Claude carga solo cuando la tarea lo pide.
- **Qué contienen estas:** cómo trabaja el estudio, su libro de estilo y los procedimientos que ya se han probado.
- **De dónde salen:** de las correcciones que el equipo ha hecho a Claude en proyectos reales. Así no se repiten los mismos errores en sesiones futuras.

## Etiquetas

Cada skill lleva una o dos etiquetas. Se ven al principio de su descripción (por ejemplo `[REVIT]`) y en el campo `metadata.etiquetas` de su `SKILL.md`.

| Etiqueta | De qué trata |
|---|---|
| ESTILO | Cómo hacemos las cosas en AGOIN: forma de trabajar, libro de estilo, informes y decisiones |
| PROYECTO | Arrancar, organizar y rehabilitar proyectos; normativa |
| MEDICIONES | Mediciones, presupuesto, BC3 y licitación |
| REVIT | Revit por API o Dynamo, y revisión del modelo |
| PLANOS | Láminas y acotación |
| INSTALACIONES | Redes de instalaciones construibles |
| ROBOT | Estructura y cimentación con Robot |
| BLENDER | Vídeo, renders e imágenes |
| WEB | Web o visor del proyecto |
| OPTIMIZACIÓN | Trabajar rápido y barato: subagentes, procesos largos, cadenas de regeneración |
| WINDOWS | Entorno de trabajo y manejo de programas y navegador |
| APPS | Aplicaciones internas del estudio |

## Qué hay

### ESTILO

| Skill | Para qué |
|---|---|
| `agoin-forma-de-trabajar` | Reglas generales de cualquier encargo: proponer y decidir, cada dato con su fuente, no inventar, comprobar, coherencia, terceros y secretos. |
| `libro-estilo-agoin` | El libro de estilo del estudio (LdE V5 y plantilla v8) más las correcciones del usuario: hoja y cajetín, numeración, tipos, textos, colores, etiquetas, tablas, leyendas, carpinterías. |
| `informes-tecnicos` | Informes y documentos: estructura, estados, procedencia, comparativas, memoria modificada y generación del PDF. |
| `decisiones-cliente` | Registro de cuestiones, preguntas clave, hojas A3 de decisión, de distribución, de dudas para dibujar a mano y de trabajo. |

### PROYECTO

| Skill | Para qué |
|---|---|
| `nuevo-proyecto-arquitectura` | Arrancar o retomar un proyecto: documentos base, carpetas, orden de trabajo, preguntas del primer día y archivos para continuar. Incluye la guía del método. |
| `rehabilitacion-levantamiento` | Rehabilitar sobre un levantamiento: qué fuente manda, nube de puntos, dron, fases y criterios de rehabilitación del estudio. |
| `comprobar-normativa` | Comprobar normativa citando el artículo, sin alarmar en falso ni dejarse nada. |

### MEDICIONES

| Skill | Para qué |
|---|---|
| `mediciones-presupuesto` | Revisar partidas, medir con trazabilidad, omisiones típicas, BC3, presupuesto ciego, mediciones por fases, control de cambios y licitación. |

### REVIT

| Skill | Para qué |
|---|---|
| `revit-automatizacion` | Revit por API o Dynamo sin riesgos: instancia correcta, simulación, avisos, copias, no tocar el Revit del usuario. Incluye más de 100 trampas conocidas. |
| `revision-modelo-bim` | Lista de comprobación del modelo antes de enseñarlo: nada flotando, nada atravesando, fiel a los planos, sin regresiones. |

### PLANOS

| Skill | Para qué |
|---|---|
| `planos-laminas` | Producir y comprobar láminas con calidad de proyecto de ejecución, y leer planos PDF vectoriales. |
| `acotar-planos` | Acotar plantas limpias y normalizadas, y cómo hacerlo en Revit. |

### INSTALACIONES · ROBOT · BLENDER · WEB

| Skill | Para qué |
|---|---|
| `instalaciones-mep` | Trazados construibles, coordinación, criterios de electricidad y telecomunicaciones, alternativas y trampas de Revit MEP. |
| `calculo-estructural` | Comprobaciones y propuestas para el estructurista, y Robot Structural Analysis (API, módulo de zapatas, notas RTF). |
| `video-render-arquitectura` | Vídeo de obra con Blender, estilo de dibujo de concurso, cámara, parpadeos y fotos de estancias. |
| `web-proyecto` | Web o visor del proyecto: qué es público, interfaz, versión interna con notas, caché, pruebas en vivo y despliegue. |

### OPTIMIZACIÓN · WINDOWS · APPS

| Skill | Para qué |
|---|---|
| `optimizar-trabajo` | Subagentes (cuántos y cómo), esperas en segundo plano, cadenas de regeneración, scripts repetibles y retomar tras un corte. |
| `automatizar-programas-windows` | Manejar ventanas de programas y un navegador con sesión cuando la API no llega, imprimir solo a PDF, Word, Excel y AutoCAD. |
| `entorno-windows-agoin` | Trampas del entorno: servidor de solo lectura, rutas UNC, Git Bash, PowerShell, codificación, cuentas, disco y archivos bloqueados. |
| `desarrollo-apps-agoin` | Apps internas: datos de producción, despliegues, Next.js, Firebase, Docker, integraciones, pruebas y usar una app en producción como usuario. |

## Cómo instalarlas

Usa **solo una** de las dos formas. Si usas las dos, cada skill aparece dos veces.

Si ya tienes alguna de estas skills copiada en `%USERPROFILE%\.claude\skills\` (por ejemplo `acotar-planos`) e instalas el plugin, borra antes la copia suelta.

### A. Como plugin (recomendado para el equipo)

Dentro de Claude Code:

```
/plugin marketplace add AGOIN17/AGOIN-SKILLS
/plugin install agoin@agoin-skills
```

O desde la consola:

```
claude plugin marketplace add AGOIN17/AGOIN-SKILLS
claude plugin install agoin@agoin-skills --scope user
```

**Requisitos.** El repositorio es privado, así que:

- cada persona necesita acceso de lectura;
- git tiene que estar autenticado en el equipo: `gh auth login` y después `gh auth setup-git`;
- sin clave SSH en GitHub, define la variable `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`.

**Cómo se usan.** Con el plugin, las skills se llaman `agoin:<nombre>`. Dentro de las skills, las referencias de una a otra usan el nombre corto.

**Para actualizar:**

```
claude plugin marketplace update agoin-skills
claude plugin update agoin@agoin-skills
```

También se puede activar la actualización automática en `/plugin` › Marketplaces.

### B. Copiando carpetas

1. Copia cada carpeta `skills/<nombre>/` a `%USERPROFILE%\.claude\skills\`.
2. No copies la raíz del repositorio.
3. Para actualizar, vuelve a copiarlas.

### Opcional: que las reglas generales se apliquen siempre

Claude carga cada skill solo cuando cree que la tarea lo pide, y así está bien para la mayoría. Si alguien quiere que tenga siempre presentes las reglas generales, puede añadir esta línea a su `%USERPROFILE%\.claude\CLAUDE.md`:

```
Trabajo para AGOIN: en cualquier encargo, aplica la skill agoin-forma-de-trabajar.
```

## Cómo añadir o mejorar una skill sin empeorar lo que hay

1. **Generalista.** Tiene que servir en cualquier proyecto. Los casos concretos entran solo como ejemplo de por qué existe una regla.
2. **Cada regla con su porqué.** Indica la corrección o el incidente que la originó. Así Claude la aplica con criterio, sin rigidez.
3. **Nada sensible.** Ni contraseñas, ni tokens, ni precios, ni datos personales o de clientes. El repositorio es privado, pero las skills se cargan en cualquier sesión.
4. **Sin contradicciones.**
   - Si cambias un criterio, cambia todas las skills que lo mencionan. Búscalas con `grep -ri "<palabra>" skills/`.
   - Si una regla nueva choca con otra, decide cuál manda y deja solo esa.
5. **Con etiqueta.** Pon una o dos etiquetas de la tabla de arriba al principio de la `description` (`[REVIT] …`) y en `metadata.etiquetas`. Si ninguna encaja, añade una nueva a la tabla.
6. **Una buena `description`.**
   - Dice qué hace la skill y cuándo usarla, con las palabras que usaría quien la pide.
   - Tiene como máximo unos 1.000 caracteres.
   - Claude decide si carga la skill solo por esta descripción.
7. **Corta.**
   - `SKILL.md` por debajo de unas 300 líneas.
   - El detalle va en `references/` y el código reutilizable en `scripts/`.
8. **En español.**
9. **Pruébala antes de subirla.**
   - Abre una sesión nueva y pide una tarea típica. Comprueba que la skill se carga y que ayuda.
   - Valida el repositorio con `claude plugin validate .`.
10. **Sube la versión en `.claude-plugin/plugin.json`** cada vez que publiques cambios. Si no, el plugin no se actualiza en los equipos.
11. **Los cambios grandes van en una rama con pull request**, para que alguien los revise.

La plantilla está en [docs/plantilla-skill.md](docs/plantilla-skill.md).

## Origen

- **1.0 (27/10/2026):** las correcciones de la sesión principal del proyecto ALFERECES (modelo Revit, mediciones, instalaciones, cálculo con Robot, web y vídeo) y las memorias de otros proyectos del equipo (apps internas, Chivero, Trama3D y licitaciones).
- **1.1 (28/10/2026):** etiquetas en todas las skills; lo aprendido en las demás sesiones de ALFERECES (revisión del presupuesto y del BC3, arranque del expediente) y en las sesiones de CHIVERO (libro de estilo, decisiones del cliente, rehabilitación sobre levantamiento, Revit con fases y nube de puntos); y cinco skills nuevas: `libro-estilo-agoin`, `decisiones-cliente`, `rehabilitacion-levantamiento`, `comprobar-normativa` y `optimizar-trabajo`.

`acotar-planos` ya existía antes del repositorio. En la 1.1 solo se le añadieron la etiqueta y lo que enseñó la acotación de ALFERECES (cuando hay plano de referencia, mandan sus cadenas; contar las cotas).
