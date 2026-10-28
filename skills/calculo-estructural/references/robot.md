# Robot Structural Analysis desde Python

Probado con Robot Structural Analysis Professional 2027 en español, octubre de 2026.

## API COM (pywin32)

- **Arranque y cierre:**
  - abre Robot con `win32com.client.gencache.EnsureDispatch("Robot.Application")`; las constantes están en `win32com.client.constants`;
  - si el proceso de Python muere, Robot se cierra con él;
  - no dejes instancias huérfanas y nunca cierres una instancia que no hayas abierto tú.
- **Desde PowerShell,** el COM necesita PowerShell 5.1 con `-STA`.
- **Unidades SI:**
  - cargas en N y N/m;
  - fuerzas en N y momentos en N·m;
  - FX > 0 en barras es compresión.
- **Guardar:** usa `Kernel.ProjectSave`; `Project.Save` falla.
- **Salir:** `Quit(I_QO_DISCARD_CHANGES)` y espera a que el proceso termine.
- **Listas de nudos o barras:** en la configuración española se escriben «775A790» (la A significa «a»). Hay que expandirlas.
- **Secciones:**
  - `I_BST_NS_BOX`: H es la altura del alma entre alas (h − 2·tf).
  - `I_BST_NS_RECT` es hueca. Para una sección maciza, pon el espesor = min(B, H)/2 con `ShapeType = I_BSST_DRECT`.
  - `I_BST_SPECIAL` ignora lo que se le pasa con `SetValue`.
- **Materiales:** comprueba el peso propio que resulta. Un material genérico dio unas 10 veces menos que el real.
  - Usa el nombre exacto de la base de la norma activa («HA - 25» con la EHE). Un nombre que no existe («C25/30» con la EHE) no da error, pero manda las reacciones a grados de libertad bloqueados.
- **Después de borrar o cambiar casos,** los resultados pasan a «no actuales»: recalcula antes de leerlos.
- **Nombres de la API que confunden:** es `CreateContour`, no `CreatePolyliner`; `Objects.Get` devuelve `IRobotDataObject` y hay que convertirlo con `CastTo`.
- **`MakeScreenCapture` no existe en Robot 2027:** no habrá imagen de Robot por esa vía. Dilo en vez de reintentar, o usa `PrintEngine` (abajo).
- **Instancia propia:** abre tu Robot para calcular variantes; no uses el que tenga abierto el usuario.
- **Liberaciones en extremos de barra:** etiqueta `I_LT_BAR_RELEASE`. `I_BERV_STD` libera el grado de libertad; `I_BERV_NONE` lo deja fijo.
- **Pandeo:** la API de Python no da sus resultados. Comprueba los arriostramientos con un caso de carga unitaria.
- **Análisis lineal:** calcula casos simples y combínalos en Python.

## Zapatas como losas sobre terreno elástico (solo a compresión)

- **Panel:** etiqueta de espesor con `ElasticFoundation` y `Uplift = I_TUT_PLUS`.
- **Combinaciones:** no lineales, con `I_CAT_COMB_NONLINEAR`. Los casos de viento sueltos no impiden resolver las combinaciones con peso.
- **Armado de losas con EHE 99:**
  - `StructuralType = I_OST_SLAB`;
  - asigna la etiqueta de armado antes de calcular y luego llama a `o.Update()`;
  - Robot impone un 0,9 ‰ por cara, y con EHE 99 no se puede desactivar.
- **Resultados de elementos finitos:** se leen con `Detailed` y con `Reinforcement(panel, nudo)`. Guarda en memoria las coordenadas de los nudos.
- **Capturas de vistas:**
  - la primera captura sale a menudo negra, y las leyendas a veces se corrompen: reintenta hasta tener fondo claro y una proporción normal de colores;
  - para ver un solo nivel, usa la vista XY con `SetWorkPoint(z)`;
  - vuelve a aplicar el caso y el mapa después de `SetZoom`.
- **Informes:** con `PrintEngine`: `AddScToReport` para capturas, `AddToReport` para tablas y `SaveReportToFile` a RTF.

## Módulo de zapatas (cimentación aislada o combinada)

- **Lo que hace la API:** crear zapatas (`ProjectComponentMngr.Create(I_PCT_FOOT)`, `CreateFromNodes`), dar medidas (`Geometry.SetDim`), calcular (`Calculate`), generar la nota RTF y mostrar el plano (`DisplayDrawing`).
- **Lo que no deja hacer la API:** definir el terreno, el tipo de pilar, las placas ni la separación entre pilares.
  - Por defecto el suelo es una arcilla de unos 0,3 MPa, y en modo diseño agranda las zapatas.
- **Definir el terreno con un preajuste:**
  - es un archivo en `%APPDATA%\Autodesk\Robot Structural Analysis Professional <versión>\CfgUsr\<nombre>.en1997.b.rccx`;
  - se crea copiando la estructura de `Cfg\Standard...`;
  - lleva el método semiempírico «límite de tensiones» con qu y la capa de terreno;
  - es un archivo de la configuración del usuario: díselo y explícale que puede borrarlo.
- **qu se compara con cargas mayoradas.** Si el dato del geotécnico es una tensión admisible de servicio, convertirla es una hipótesis tuya: dila.
- **qref es la presión en la esquina más cargada** (reparto lineal). Es más estricto que comparar la tensión media.
- **Despegue:** exige que la resultante quede en el núcleo central en ELU (s = eB/B + eL/L ≤ 1/6).
- **Cortante:** lo comprueba sin armadura transversal, así que falla donde una propuesta con cercos sí cumple. Explícalo, no lo escondas.
- **Plano:** solo dibuja el armado si la zapata pasa todas sus comprobaciones. Ese armado es el suyo (mínimos), no el de tu propuesta.
- **El fuste 1 es el nudo de número más bajo:** gira la zapata 180° si hace falta para que coincida con tu numeración.
- **Cargas de zapatas combinadas:**
  - cada pilar importado con `CreateFromNodes` queda como un grupo de cargas aparte;
  - suma la N del segundo pilar a los registros del primer grupo (fuste 2) y borra el segundo grupo.
- **Una zapata por archivo:** la ventana del módulo solo carga la zapata que está presente al abrir el archivo. `Activate()` cambia el título pero no recarga, así que usa un archivo y un Robot nuevo para cada zapata.
- **Material de las notas y planos:** rotulan el nombre del material por defecto («HA-30») aunque la resistencia sea otra. Compruébala en la nota.

## Manejar la ventana cuando la API no llega

Las reglas generales están en la skill `automatizar-programas-windows`. Lo específico de Robot:

- **Valores:** se teclean con `type_keys("{HOME}+{END}{DEL}valor{TAB}")` y coma decimal. `WM_SETTEXT` no se registra.
- **«¡Valor sobrepasado!»:** define primero el pilar y la placa, y da un paso previo con dimensiones intermedias.
- **Avisos de Robot** («Hormigón armado» y otros cuadros de mensaje): lee su texto y guárdalo antes de aceptarlos.
- **Plano de ejecución a PDF:** `DisplayDrawing` y Ctrl+P, solo con «Microsoft Print to PDF». Usa el script `imprimir_pdf.py` de `automatizar-programas-windows`.

## Notas RTF

Robot escribe cada nota de zapata como varios RTF pegados, cada uno con su tabla de fuentes y colores. Word solo lee la primera tabla, y el resto del texto sale en Symbol (letras griegas).

`../scripts/rtf_unir_tablas.py` une las tablas y convierte a PDF con Word (`ExportAsFixedFormat 17`).
