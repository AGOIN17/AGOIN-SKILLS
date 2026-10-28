---
name: revit-automatizacion
description: "[REVIT] Protocolo seguro y trampas conocidas para leer y modificar modelos de Revit desde código (API de Revit, Dynamo con Python, DynamoMCP, puentes MCP como revit-2027). Cubre el modelo y la instancia correctos (varios Revit abiertos, una segunda instancia propia), las copias, la simulación antes de aplicar, las transacciones con IFailuresPreprocessor, no tocar el Revit del usuario, guardar, exportar PDF/DWG/IFC y comprobar después, más de 100 trampas de la API (muros, suelos, habitaciones y fases, familias, DirectShape, nube de puntos, cotas, vistas, láminas). Úsala antes de lanzar cualquier script, grafo o herramienta MCP que toque un archivo .rvt o una familia, aunque sea solo para leer. También cuando Revit no responda o salga un diálogo."
metadata:
  etiquetas: "REVIT"
---

# Revit desde código

Al automatizar Revit, lo que se rompe no suele ser la geometría. Suelen ser tres cosas:

- un diálogo modal con una transacción abierta, que puede cerrar Revit sin archivo de recuperación;
- un script lanzado al Revit equivocado;
- un cambio que arrastra otros elementos sin que nadie lo vea hasta que se exportan los planos.

Este protocolo evita las tres.

## Antes de tocar nada

1. **Comprueba qué Revit y qué modelo.**
   - El usuario puede tener varios Revit abiertos con otros proyectos, cada uno con su Dynamo (puertos 8080, 8081…) y su puente MCP.
   - Lee los títulos de ventana (`Get-Process Revit | select MainWindowTitle`).
   - Confirma que el documento activo es el modelo de trabajo antes de mandar nada. Los scripts que solo deben correr sobre una copia concreta comprueban el título del documento y se niegan si no coincide.
   - Nunca envíes un script a un Dynamo cuyo Revit tiene otro modelo abierto. Las herramientas MCP de la sesión (`mcp__revit-2027__*` o similares) apuntan al puerto de un proyecto concreto: no las uses para otro.
2. **Comprueba la edición y el contenido.** Revit LT no tiene API ni Dynamo: ofrece leer el modelo y los PDF y preparar la lista de cambios para hacerlos a mano. Antes de prometer familias, mira si está instalada la biblioteca de contenido de Revit.
3. **Trabaja solo sobre copias de trabajo.**
   - El original (lo recibido, el levantamiento, el .rvt de otra versión) no se abre ni se modifica. Abrirlo en una versión nueva de Revit lo actualiza sin vuelta atrás.
   - Si otra sesión tiene abierto el .rvt de trabajo, no guardes en él: «Guardar como» una copia nueva, sigue en ella y anota cuál es el modelo vigente.
4. **Haz una copia del .rvt antes de cada cambio grande**, con la fecha en el nombre. Antes, mira la fecha del archivo en disco: tiene que tener el estado actual. Un R27 seguía idéntico byte a byte al de la versión anterior porque nunca se había guardado, y la copia «antes» no habría servido.
5. **Si el modelo no está abierto, pide al usuario que lo abra.** Si hay que abrir Dynamo y eso exige un clic en su interfaz, pídeselo también. Mientras, haz lo que no necesite Revit.
6. **Actualizaciones de plantillas o modelos antiguos** (2019 → 2027): por API pueden tardar horas. Déjaselas al usuario. Un archivo que pide «Revisar» y falla por API (CArchiveException 105, incluso con Audit) solo se abre a mano: pide al usuario que lo abra y guarde una copia.
7. **Vigila el espacio en disco.**
   - Revit se cierra o no guarda si el disco se llena. Ante un cierre raro, mira el espacio libre.
   - Las carpetas temporales de Revit de sesiones ya cerradas ocupan mucho y se pueden borrar. Con varios Revit abiertos, cada uno tiene su carpeta en uso; no basta con mirar cuál es la más reciente.
   - Di al usuario qué vas a borrar y cuánto ocupa, y espera su confirmación antes de hacerlo.
8. **Token de DynamoMCP:** nunca lo saques del almacén de credenciales de Autodesk. Ofrece dos caminos: abrir Revit con la variable de entorno que prevé el propio complemento, solo para esa sesión y desde un .bat (explicando que mientras esté abierto cualquier programa del equipo puede mandar órdenes a Dynamo), o scripts para Dynamo Player.

## Una segunda instancia de Revit para otro proyecto

Si el usuario tiene otro Revit abierto con otra sesión de Claude, lanza una instancia propia con un lanzador que:

- fije el puerto de su puente MCP (variable de entorno del complemento);
- no pise el token del otro proyecto: si el complemento lo escribe en un archivo compartido, restaura ese archivo en cuanto arranque tu instancia, para que el puente del otro proyecto siga funcionando. El token no se imprime ni se copia a archivos de texto del proyecto;
- anote el PID.

Usa un cliente propio que compruebe el título del documento antes de cada llamada. DynamoMCP coge el puerto 8080 si está libre: para que el segundo Dynamo no lo coja, ocúpalo con un `HttpListener` de relleno mientras arranca y suéltalo después; el puerto real está en la última línea «started on» del registro de Dynamo.

Dos agentes con dos Revit en el mismo equipo funcionan si: nunca trabajan sobre el mismo .rvt; las bibliotecas y plantillas comunes se usan solo como copias; y se cuidan los clics reales y los diálogos, porque los dos se disputan el foco. Los mensajes Win32 dirigidos por PID no se cruzan.

## Cada cambio

- **Simula primero.**
  - Todo script que escribe tiene un parámetro `aplicar`.
  - En simulación, confirma la transacción dentro de un `TransactionGroup` y luego deshace el grupo. Así saltan los mismos errores que en la ejecución real.
  - Devuelve un informe de lo que haría.
  - Se lee el informe y solo entonces se lanza con `true`.
- **Cuidado con cómo llega la entrada en Dynamo.**
  - Si el script lee `IN[0][0]` con `bool()`, una entrada `"[[false]]"` o el texto `"false"` cuentan como verdadero. Así un script se aplicó sin simular.
  - Haz que solo un `true` explícito aplique, como en la plantilla.
- **Toda transacción lleva un `IFailuresPreprocessor`.**
  - Borra los avisos y deshace la transacción si hay errores. La plantilla está en `references/plantilla_transaccion_dynamo.py`.
  - Hace falta también en los documentos de familia.
  - Sin él, un aviso abre un diálogo modal y la llamada se queda colgada. Si alguien acepta ese diálogo a mano con la transacción pendiente, Revit puede cerrarse sin archivo de recuperación.
  - **Pon una cabecera común delante de cada script** (`_comun.py`): utilidades, la transacción con su preprocesador y un modo «sondeo» que lista qué fallos daría un cambio sin confirmarlo. Así no se copia el control de avisos en cada script.
- **Una transacción por paso lógico.** Llama a `doc.Regenerate()` después de crear algo que vayas a medir o acotar en la misma transacción.
- **Lo que un script crea, se marca** (prefijo, comentario, marca) **y se borra por esa marca** antes de volver a crearlo. Las listas de ids fallan: tras un cierre inesperado Revit reutiliza los números y borrarías elementos nuevos.
- **Después de aplicar, verifica leyendo el modelo.** No te fíes de un «ok».
  - Guarda, si el usuario te lo permite. Pregunta una vez por proyecto si puedes guardar sin pedirlo cada vez, y anótalo en el archivo de contexto (en ALFERECES dijo que sí).
  - Tras un «Saving failed» del puente, no des por perdido el guardado: comprueba `doc.IsModified`, la hora del .rvt y la rotación de las copias `.00NN`. Si todo está bien, guarda otra vez.
  - En modelos compartidos (worksharing), nunca sincronices con el archivo central sin su permiso.
  - Anota el cambio en el registro del modelo: fecha, script, motivo e ids.
- **Cuenta los elementos antes y después de cada transacción** que pueda arrastrar otros (uniones, huecos, cotas, habitaciones).

## El Revit del usuario no se toca

- **En el Revit del usuario, no pulses botones ni cierres diálogos, y no cierres Revit.**
  - Si una llamada no responde, lista las ventanas (EnumWindows o UI Automation).
  - Lee el texto del diálogo sin tocar nada y pregunta al usuario qué hacer.
  - Si su Revit estorba (por ejemplo, coge los puertos de otro proyecto), pídele que lo cierre.
- **Si el usuario contesta a un diálogo, las peticiones encoladas se ejecutan después**, incluso en orden inverso. Mira qué ha corrido antes de relanzar nada.
- **Con la ventana de Dynamo minimizada, su servidor MCP puede no arrancar.** Pide al usuario que la deje restaurada; no la toques tú.
- **Para ver el modelo sin tocar su interfaz:**
  1. duplica una vista 3D;
  2. ponle caja de sección y recorte;
  3. exporta la imagen;
  4. borra la vista.
- **En Dynamo, deja el espacio de trabajo sin cambios pendientes al terminar cada grafo** (`HasUnsavedChanges = False`). Si no, cada ejecución siguiente abre un «¿Desea guardar los cambios?» que la bloquea. Una vez se apilaron ocho de esos diálogos.

**En una instancia que hayas abierto tú**, avisando al usuario y con mensajes dirigidos a su proceso, sí puedes:

- pulsar «Ignorar y abrir el proyecto» en «Referencias sin resolver» (BM_CLICK por UI Automation);
- deshacer la última transacción con `PostMessage(ventana, WM_COMMAND, 0xE12B, 0)` (`PostCommand(ID_EDIT_UNDO)` lo rechaza la API);
- abrir «Proceso por fases» con `PostCommand(PostableCommand.Phases)` y manejar su rejilla con mensajes (ver `automatizar-programas-windows`);
- capturar un diálogo tapado con `PrintWindow`.
- El botón de Dynamo en la cinta (WPF) solo responde a un clic real del ratón: solo en tu instancia, con permiso, cuando el usuario no esté usando el equipo, y comprobando que el clic no cayó en otra ventana.

## Puentes MCP y DynamoMCP

- **`move_element` puede responder que ha ido bien y no hacer nada.** Pasó con ejes que estaban dentro de un grupo de modelo. Desagrupa primero y comprueba la posición después.
- **Si el cambio provoca un aviso de Revit, la transacción se bloquea,** incluso en `dryRun`, y la llamada agota su tiempo.
- **Después de un tiempo agotado, vuelve a leer el estado del modelo antes de reintentar.**
- **Para consultas de solo lectura,** se puede llamar directamente a la API HTTP del complemento, con una lista de comandos permitidos.
- **DynamoMCP:**
  - `run_graph_from_path` responde «Graph is not trusted»: usa `run_graph_from_json`;
  - si la salida OUT es grande llega paginada o no llega: que el script escriba el resultado en un archivo y léelo;
  - tras reiniciar Dynamo, «tool not found» se arregla llamando a `tools/list` justo después de `initialize`; reintentar a ciegas tuvo más de 10 minutos de errores.
- **Registra los servidores MCP con `claude mcp add-json` desde Bash:** el `claude.ps1` de PowerShell se come el `--`.

## Exportar

- **PDF de láminas:** con la herramienta de exportación, en vectorial. Por API, `FileName` no cuenta y el archivo sale como «Plano-<nombre>.pdf»: después de exportar, mira el nombre y la fecha del archivo que vas a revisar. La exportación deja activa la última hoja, que entonces no se puede borrar: abre otra vista antes de rehacer hojas.
- **DWG:** por API funciona.
- **IFC por API:** en la sesión compartida dejó una transacción abierta y Revit se cerró. No lo hagas. Genera el IFC fuera (IfcOpenShell, a partir de la geometría exportada) o pide que se exporte a mano.
- **Compara siempre con el juego anterior.**
  - Después de cambiar muros, plantillas de vista o vistas colocadas, exporta las láminas y compáralas píxel a píxel con el juego anterior.
  - Las puertas y ventanas se deslizan con el muro.
  - Cambiar una plantilla vuelve a mostrar elementos ocultos en todas sus vistas.
  - Las vistas sin recorte se mueven en la hoja.

## Lo que no se puede hacer por API (Revit 2027)

Opciones de diseño; crear o renombrar fases; transferir normas de proyecto (plantillas de vista, leyendas, tablas entre archivos); editar la tabla de grosores de línea por escala (sí se asigna el número de pluma a una categoría o en una vista); crear rótulos (Label) dentro de una familia de cajetín o de etiqueta (edita una copia de la familia; colocar etiquetas en una vista sí se puede). Usa copias del modelo, edita familias o deja esos pasos al usuario.

## Modelos vinculados (arquitectura + instalaciones)

- El modelo de instalaciones se edita en segundo plano desde la sesión del de arquitectura.
- Antes, descarga el vínculo. Al terminar, cierra el modelo de instalaciones y vuelve a cargar el vínculo.

## Trampas concretas

Lee `references/trampas-revit.md` cuando vayas a trabajar con cualquiera de estos temas:

- Dynamo y el canal de comunicación;
- muros y uniones (también los de un levantamiento);
- suelos, habitaciones, fases y terreno;
- escaleras y barandillas;
- familias, instancias y copias;
- geometría, DirectShape y nube de puntos;
- cotas;
- vistas, plantillas, láminas y textos.

Cada entrada costó horas una vez. Las trampas de instalaciones están en `instalaciones-mep`; los criterios de rehabilitación, en `rehabilitacion-levantamiento`.

## Ejemplos que ya funcionan

En el equipo donde se hicieron, por si sirven de modelo:

- `D:\ARQ\ALFERECES\TRABAJO_REVIT_PE2026\`: `scripts\dynamo_mcp.py` (cliente de DynamoMCP), `MEP\mep_comun.py` (transacción con avisos), `dynamo\q_vista_trabajo.py` (ver el modelo sin tocar la interfaz), `scripts\visor_export\` (revisar el modelo fuera de Revit).
- `D:\ARQ\Chivero\TRABAJO_REVIT\`: segunda instancia con su lanzador, `dynamo\_comun.py` y el compositor de láminas; el orden de regeneración está en `00_PLAN.md`.
