---
name: revit-automatizacion
description: "Protocolo seguro y trampas conocidas para leer y modificar modelos de Revit desde código (API de Revit, Dynamo con Python, DynamoMCP, puentes MCP como revit-2027). Cubre el modelo correcto, las copias, la simulación antes de aplicar, las transacciones con IFailuresPreprocessor, no tocar la interfaz del usuario, guardar, exportar PDF/DWG/IFC y comprobar después. Úsala antes de lanzar cualquier script, grafo o herramienta MCP que toque un archivo .rvt o una familia, aunque sea solo para leer. También cuando Revit no responda o salga un diálogo."
---

# Revit desde código

Al automatizar Revit, lo que se rompe no suele ser la geometría. Suelen ser tres cosas:

- un diálogo modal con una transacción abierta, que puede cerrar Revit sin archivo de recuperación;
- un script lanzado al Revit equivocado;
- un cambio que arrastra otros elementos sin que nadie lo vea hasta que se exportan los planos.

Este protocolo evita las tres.

## Antes de tocar nada

1. **Comprueba qué Revit y qué modelo.**
   - El usuario puede tener varios Revit abiertos con otros proyectos, cada uno con su Dynamo (puertos 8080, 8081…).
   - Lee los títulos de ventana (`Get-Process Revit | select MainWindowTitle`).
   - Confirma que el documento activo es el modelo de trabajo antes de mandar nada.
   - Nunca envíes un script a un Dynamo cuyo Revit tiene otro modelo abierto.
2. **Trabaja solo sobre copias de trabajo.**
   - El original (lo recibido, el .rvt de otra versión) no se abre ni se modifica.
   - Abrirlo en una versión nueva de Revit lo actualiza sin vuelta atrás.
3. **Haz una copia del .rvt antes de cada cambio grande**, con la fecha en el nombre.
4. **Si el modelo no está abierto, pide al usuario que lo abra.** Si hay que abrir Dynamo y eso exige un clic en su interfaz, pídeselo también. Mientras, haz lo que no necesite Revit.
5. **Vigila el espacio en disco.**
   - Revit se cierra o no guarda si el disco se llena. Ante un cierre raro, mira el espacio libre.
   - Las carpetas temporales de Revit de sesiones ya cerradas ocupan mucho y se pueden borrar.
   - Con varios Revit abiertos, cada uno tiene su carpeta en uso; no basta con mirar cuál es la más reciente.
   - Di al usuario qué vas a borrar y cuánto ocupa antes de hacerlo.

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
- **Una transacción por paso lógico.** Llama a `doc.Regenerate()` después de crear algo que vayas a medir o acotar en la misma transacción.
- **Después de aplicar, verifica leyendo el modelo.** No te fíes de un «ok».
  - Guarda, si el usuario te lo permite. En ALFERECES dio permiso para guardar siempre que hiciera falta.
  - En modelos compartidos (worksharing), nunca sincronices con el archivo central sin su permiso.
  - Anota el cambio en el registro del modelo: fecha, script, motivo e ids.
- **Limpia el registro de ids tras un cierre inesperado.** Si guardas ids para borrarlos después, Revit reutiliza los números y borrarías elementos nuevos.

## La interfaz del usuario no se toca

- **No pulses botones ni cierres diálogos en el Revit del usuario, y no cierres Revit.**
  - Si una llamada no responde, lista las ventanas (EnumWindows o UI Automation).
  - Lee el texto del diálogo sin tocar nada y pregunta al usuario qué hacer.
- **Si el usuario contesta a un diálogo, las peticiones encoladas se ejecutan después**, incluso en orden inverso. Mira qué ha corrido antes de relanzar nada.
- **Para ver el modelo sin tocar su interfaz:**
  1. duplica una vista 3D;
  2. ponle caja de sección y recorte;
  3. exporta la imagen;
  4. borra la vista.
- **En Dynamo, deja el espacio de trabajo sin cambios pendientes al terminar cada grafo** (`HasUnsavedChanges = False`). Si no, cada ejecución siguiente abre un «¿Desea guardar los cambios?» que la bloquea. Una vez se apilaron ocho de esos diálogos.

## Puentes MCP de Revit (revit-2027 y similares)

- **`move_element` puede responder que ha ido bien y no hacer nada.** Pasó con ejes que estaban dentro de un grupo de modelo. Desagrupa primero y comprueba la posición después.
- **Si el cambio provoca un aviso de Revit, la transacción se bloquea,** incluso en `dryRun`, y la llamada agota su tiempo.
- **Después de un tiempo agotado, vuelve a leer el estado del modelo antes de reintentar.**
- **Para consultas de solo lectura,** se puede llamar directamente a la API HTTP del complemento, con una lista de comandos permitidos.

## Exportar

- **PDF de láminas:** con la herramienta de exportación, en vectorial.
- **DWG:** por API funciona.
- **IFC por API:** en la sesión compartida dejó una transacción abierta y Revit se cerró. No lo hagas. Genera el IFC fuera (IfcOpenShell, a partir de la geometría exportada) o pide que se exporte a mano.
- **Compara siempre con el juego anterior.**
  - Después de cambiar muros, plantillas de vista o vistas colocadas, exporta las láminas y compáralas píxel a píxel con el juego anterior.
  - Las puertas y ventanas se deslizan con el muro.
  - Cambiar una plantilla vuelve a mostrar elementos ocultos en todas sus vistas.
  - Las vistas sin recorte se mueven en la hoja.

## Modelos vinculados (arquitectura + instalaciones)

- El modelo de instalaciones se edita en segundo plano desde la sesión del de arquitectura.
- Antes, descarga el vínculo. Al terminar, cierra el modelo de instalaciones y vuelve a cargar el vínculo.

## Trampas concretas

Lee `references/trampas-revit.md` cuando vayas a trabajar con cualquiera de estos temas:

- muros y uniones;
- suelos y bocetos;
- escaleras y barandillas;
- familias e instancias;
- geometría, booleanas y DirectShape;
- cotas;
- vistas, plantillas, láminas y textos.

Cada entrada costó horas una vez. Las trampas de instalaciones están en la skill `instalaciones-mep`.

## Ejemplos que ya funcionan

Están en `D:\ARQ\ALFERECES\TRABAJO_REVIT_PE2026\`, en el equipo donde se hizo ALFERECES:

- `scripts\dynamo_mcp.py`: cliente de DynamoMCP;
- `MEP\mep_comun.py`: transacción con avisos;
- `dynamo\q_vista_trabajo.py`: ver el modelo sin tocar la interfaz;
- `scripts\visor_export\`: revisar el modelo fuera de Revit.
