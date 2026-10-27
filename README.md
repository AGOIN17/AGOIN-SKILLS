# AGOIN-SKILLS

Este repositorio reúne las skills de Claude Code de AGOIN.

- **Qué es una skill:** un conjunto de instrucciones que Claude carga solo cuando la tarea lo pide.
- **Qué contienen estas:** los criterios de trabajo del estudio y los procedimientos que ya se han probado.
- **De dónde salen:** de las correcciones que el equipo ha hecho a Claude en proyectos reales. Así no se repiten los mismos errores en sesiones futuras.

## Qué hay

| Skill | Para qué |
|---|---|
| `agoin-forma-de-trabajar` | Reglas generales de cualquier encargo: proponer y decidir, cada dato con su fuente, no inventar, comprobar, coherencia, terceros y secretos. |
| `nuevo-proyecto-arquitectura` | Arrancar o retomar un proyecto: documentos base, carpetas, orden de trabajo y archivos para continuar entre sesiones. Incluye la guía del método. |
| `mediciones-presupuesto` | Revisar partidas, medir con trazabilidad, BC3, presupuesto ciego, control de cambios y licitación. |
| `revit-automatizacion` | Revit por API o Dynamo sin riesgos: simulación, avisos, copias, no tocar la interfaz. Incluye las trampas conocidas. |
| `revision-modelo-bim` | Lista de comprobación del modelo antes de enseñarlo: nada flotando, nada atravesando, fiel a los planos, sin regresiones. |
| `planos-laminas` | Láminas con calidad de proyecto de ejecución y lectura de planos PDF vectoriales. |
| `acotar-planos` | Acotar plantas limpias y normalizadas, y cómo hacerlo en Revit. |
| `instalaciones-mep` | Trazados construibles, coordinación, recuentos y trampas de Revit MEP. |
| `calculo-estructural` | Comprobaciones y propuestas para el estructurista, y Robot Structural Analysis (API, módulo de zapatas, notas RTF). |
| `automatizar-programas-windows` | Manejar ventanas de programas cuando la API no llega, imprimir solo a PDF, Word, Excel y AutoCAD. |
| `video-render-arquitectura` | Vídeo de obra, estilo de dibujo de concurso, cámara, parpadeos y fotos de estancias. |
| `web-proyecto` | Web o visor del proyecto: qué es público, interfaz, caché, pruebas en vivo y despliegue. |
| `informes-tecnicos` | Informes y documentos: estructura, estados, procedencia, comparativas, hojas de decisión y generación del PDF. |
| `entorno-windows-agoin` | Trampas del entorno: servidor de solo lectura, rutas UNC, Git Bash, PowerShell, cuentas y disco. |
| `desarrollo-apps-agoin` | Apps internas: datos de producción, despliegues, Next.js, Firebase, Docker, integraciones y pruebas. |

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

### Para que las reglas generales se apliquen siempre

Claude carga cada skill solo cuando cree que la tarea lo pide. Para que tenga siempre presentes las reglas generales, añade esta línea a tu `%USERPROFILE%\.claude\CLAUDE.md`:

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
5. **Una buena `description`.**
   - Dice qué hace la skill y cuándo usarla, con las palabras que usaría quien la pide.
   - Tiene como máximo unos 1.000 caracteres.
   - Claude decide si carga la skill solo por esta descripción.
6. **Corta.**
   - `SKILL.md` por debajo de unas 300 líneas.
   - El detalle va en `references/` y el código reutilizable en `scripts/`.
7. **En español.**
8. **Pruébala antes de subirla.**
   - Abre una sesión nueva y pide una tarea típica. Comprueba que la skill se carga y que ayuda.
   - Valida el repositorio con `claude plugin validate .`.
9. **Sube la versión en `.claude-plugin/plugin.json`** cada vez que publiques cambios. Si no, el plugin no se actualiza en los equipos.
10. **Los cambios grandes van en una rama con pull request**, para que alguien los revise.

La plantilla está en [docs/plantilla-skill.md](docs/plantilla-skill.md).

## Origen

La primera versión es del 27/10/2026. Salió de dos fuentes:

- las correcciones de las sesiones del proyecto ALFERECES: modelo Revit, mediciones, instalaciones, cálculo con Robot, web y vídeo;
- las memorias de otros proyectos del equipo: apps internas, Chivero, Trama3D y licitaciones.

`acotar-planos` ya existía y se incluye sin cambios.
