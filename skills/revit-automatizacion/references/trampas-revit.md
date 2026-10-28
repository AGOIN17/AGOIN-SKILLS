# Trampas de Revit por API y Dynamo

Encontradas con Revit 2027 y Dynamo 4 (PythonNet3), octubre de 2026, en ALFERECES (edificio de viviendas, modelo al día de un proyecto visado) y CHIVERO (rehabilitación por fases sobre un levantamiento con nube de puntos). Cada una costó tiempo una vez.

## Índice

1. Dynamo, PythonNet y el canal de comunicación
2. Muros
3. Suelos, habitaciones, fases y terreno
4. Escaleras y barandillas
5. Familias, instancias y copias
6. Geometría, DirectShape y nube de puntos
7. Cotas
8. Vistas, plantillas, láminas y textos

---

## 1. Dynamo, PythonNet y el canal de comunicación

- **No se puede hacer por API (comprobado en Revit 2027):** opciones de diseño; crear o renombrar fases; transferir normas de proyecto entre archivos; editar la tabla de grosores de línea por escala; crear rótulos (Label) dentro de familias de cajetín o de etiqueta. Usa copias del modelo, edita una copia de la familia, o deja esos pasos al usuario.
- **Guarda antes de crear habitaciones en bucle.** Un bucle de `NewRoom` cerró Revit y se perdió lo no guardado.
- **Revit borra cotas al confirmar** si sus referencias cambian. Anótalas antes y vuelve a dibujarlas después.
- **PythonNet:**
  - `ElementId` como clave de diccionario falla: usa `.Value`;
  - **los parámetros de salida (out) vuelven como tuplas, y una tupla con algo dentro siempre es verdadera.** `if tipo.IsValid(...)` daba por buenas composiciones inválidas, y `CutExistsBetweenElements` devuelve `[bool, motivo]`. Desempaqueta antes de mirar;
  - para saber si un elemento tiene curva de ubicación, usa `isinstance(loc, LocationCurve)`; `hasattr` cerró la llamada.
- **«error return without exception set»:** en PythonNet casi siempre es por indexar una ICollection de .NET, por ejemplo `stairs.GetStairsRuns()[0]` o `CopyElements(...)[0]`.
  - Convierte antes: `list(...)[0]`.
  - En los colectores por tipo, pasa la clase (`StairsRunType`), no `obj.GetType()`.
- **Clases que heredan de una interfaz .NET** (IFailuresPreprocessor): cada una necesita un `__namespace__` único en el script.
- **`doc.Regenerate()` fuera de una transacción** da «Modification of the document is forbidden».
- **Tras borrar elementos,** comprueba `IsValidObject` en las listas que tuvieras guardadas.
- **Rutas dentro de argumentos JSON:** escríbelas con barras normales (`D:/ARQ/...`). Las barras invertidas rompen el JSON con el error «se esperaba closebracket».
- **JSON dentro de una cadena de DesignScript:** `json.dumps(..., ensure_ascii=False)`. Si no, «·» llega como `\u00b7` y los nombres de vista fallan. Si la entrada lleva mucho texto no ASCII, pasa la ruta de un archivo JSON en vez del JSON.
- **Entrada como lista:** si se pasa una lista como entrada, IN[0] es la lista. Un script que espera una cadena necesita la cadena, no `[cadena]`.
- **Un script largo puede agotar el tiempo de la llamada mientras Revit sigue trabajando.**
  - Comprueba si hay un diálogo abierto (EnumWindows). Si no lo hay, Revit sigue ocupado.
  - Espera y consulta el estado antes de relanzar.
- **Tras reiniciar Dynamo**, la primera llamada puede responder «tool not found». Lo que lo arregla es llamar a `tools/list` justo después de `initialize`; reintentar a ciegas tuvo más de 10 minutos de errores.
- **`OpenDocumentFile` sobre un `.rte`** da error interno, y renombrarlo a `.rvt` tampoco sirve: usa `NewProjectDocument(plantilla)`.
- **Archivo de parámetros compartidos nuevo:** créalo vacío, sin escribir cabecera, o da «Error in readParamDatabase».
- **Rutas escritas desde Bash:** en la herramienta Bash de Claude Code, una doble barra invertida dentro de un heredoc llega a Python como una sola, incluso con `<<'EOF'`. Una ruta con `\a` se convirtió en el carácter BEL y `\162` en «r».
  - Escribe los scripts con la herramienta de escritura de archivos.
  - Escribe las rutas con `/`.
  - Cualquier cambio con barras invertidas, con la herramienta de edición.

## 2. Muros

- **Cambiar la curva de un muro desliza sus puertas y ventanas.**
  - Guarda sus posiciones antes de cambiarla.
  - Después, devuélvelas a su sitio moviéndolas solo a lo largo del muro.
  - Siete huecos se movieron entre 5 y 45 cm y nadie lo vio hasta reexportar las láminas.
- **Los muros alineados y unidos por los extremos se arrastran entre sí:** mover uno en perpendicular mueve toda la cadena.
  1. Desactiva las uniones de extremo (`WallUtils.DisallowWallJoinAtEnd`).
  2. Coloca cada muro en su sitio.
  3. Vuelve a activar las uniones.
  - Si al reactivarlas los muros retroceden, déjalas desactivadas: en muros alineados la junta a tope no se ve.
  - Comprueba `Location.Curve` después del commit.
- **Muros nuevos en un levantamiento acotado:** las cotas del levantamiento están ancladas a aristas de muro y a jambas.
  - Crea los muros nuevos con `DisallowWallJoinAtEnd` en los dos extremos.
  - Antes de derribar un hueco en un muro que se queda, «fotografía» todas las cotas.
  - Redibuja las perdidas sobre líneas de detalle de anclaje y comprueba que el número de cotas no baja.
- **«No es posible mantener unidos / cortar elemento unido»:** sale al subir, bajar o recortar un muro unido a losas o vigas. Hay dos salidas:
  - `JoinGeometryUtils.UnjoinGeometry` con cada elemento unido, antes del cambio;
  - un preprocesador que llame a `fa.ResolveFailure(f)` solo para ese fallo (su resolución por defecto es separar la unión) y devuelva `ProceedWithCommit`.
- **Nunca aceptes en bloque las resoluciones por defecto de Revit.** En otro proyecto borraron una fachada levantada y sus cotas. Cuenta los elementos antes y después de cada transacción.
- **Si un script separa uniones en su propia transacción y luego falla, quedan separadas.**
  - Recupera las uniones originales desde una copia de seguridad abierta en segundo plano.
  - Antes de abrirla, descarga sus vínculos con `TransmissionData`. Al terminar, ciérrala sin guardar.
- **`JoinGeometry` solo oculta la arista entre dos muros si son coplanares de verdad.** El usuario ve un escalón de 0,4 mm. Lleva cada cara exterior a su plano y une todos los pares que se tocan.
- **Las uniones de extremo pueden recortar la cara exterior** y dejar ranuras de 2 o 3 cm junto a un rehundido. Búscalas.
- **Tres muros que acaban en el mismo punto no siempre se unen en T,** y dejan agujeros de 30 a 60 cm en la fachada.
  - Lista los nudos (`LocationCurve.get_ElementsAtJoin`).
  - Busca agujeros con segmentos verticales contra los sólidos, a una altura donde existan todos.
  - Rehaz solo los nudos con agujero: rehacer uno bueno rompió una habitación.
- **Revit no forma una T si el extremo del muro que acomete pasa del eje del otro.** Lleva el extremo al eje y une.
- **Voltear un muro sin moverlo:**
  1. pon la línea de ubicación en el eje (`WALL_KEY_REF_PARAM` = 0);
  2. llama a `Flip()`;
  3. restaura el valor original.
  - Si llamas a `Flip()` o cambias la línea de ubicación después de crear el muro, el muro se desplaza su espesor.
- **`Wall.Create` con perfil no rectangular** dio un muro equivocado. Usa muros rectangulares escalonados.
  - Tras crear un muro, mide su cara exterior real (la cara plana más grande con la normal hacia fuera) y muévelo al plano objetivo.
  - `Orientation` puede fallar antes de regenerar. Da a la curva la dirección del muro vecino y pasa su `Flipped` a `Wall.Create`.
- **Mover el extremo de un muro junto a otro alineado:** `AllowWallJoinAtEnd` después de poner la nueva curva devolvió los dos muros cerca de sus extremos antiguos.
- **Puertas correderas junto a una fachada** pueden sacar la hoja por fuera del muro. Revisa las caras exteriores; `flipHand` lo arregló.
- **Muros de un levantamiento:**
  - no siempre tienen la línea de ubicación en su eje, y las booleanas fallan sin avisar en algunos. Para saber si algo los atraviesa, corta un segmento con el sólido del muro;
  - la línea de ubicación termina en el cruce de ejes, así que un rectángulo hecho con sus extremos se queda corto en la esquina exterior. Para saber si una cara está oculta, usa la envolvente de los vértices de la cara. `EdgeLoops` puede devolver aristas invertidas: usa `GetEdgesAsCurveLoops`.
- **Al derribar un hueco, Revit añade sus propios muros de relleno,** que repiten entera la línea del anfitrión. Al buscar «el muro bajo un punto», sáltate los muros cuya caja es mucho más corta que su curva. Esos rellenos no se pueden borrar y no tienen caja: son esperables, no derribos sueltos.
- **Para buscar la cara de un muro por su posición a lo largo de una nave,** filtra también por la distancia al eje de la nave. Si no, coge el muro de la nave vecina («la acera va pegada al muro» tuvo que repetirse dos veces por esto).
- **Cambiar el nivel de una unidad deja cortos sus tabiques y trasdosados** de altura sin conexión. Tras cada cambio de cota, comprueba que cada muro llega a su techo.

## 3. Suelos, habitaciones, fases y terreno

- **`SketchEditScope` es poco fiable desde Dynamo.** A veces no arranca, y otras no se cierra si queda una transacción abierta. Hay dos alternativas:
  - recortar con un hueco: `doc.Create.NewOpening(suelo, curvas, True)`;
  - recrear el suelo con el mismo tipo, nivel, desfase, marca, comentario y fase. El id cambia, así que actualiza todo lo que lo referencia.
  - Después de un fallo, mira `doc.IsInEditMode()`.
- **Si se usa `SketchEditScope`:**
  - una línea de boceto bloqueada no se puede borrar; reutilízala con `SetGeometryCurve(linea, True)`;
  - separa las uniones antes de encoger un suelo;
  - no llames a `doc.Regenerate()` fuera de una transacción después del commit.
- **`Floor.Create` da «No es posible cortar elemento unido»:** pasa `isStructural=False`.
- **`Floor.Create` y `Ceiling.Create` rechazan los contornos que da Revit para las habitaciones** (quiebros de 1 a 3 cm). Usa polígonos limpios, por ejemplo los de superficie útil del DWG, eligiendo el que coincide con el área rotulada.
- **Tipos compuestos (suelos, muros):** `SetCompoundStructure` rechaza `CreateSimpleCompoundStructure` y puede dar «wrong EndCap condition». Duplica un tipo, parte de su `GetCompoundStructure()` y usa `SetLayers`, con las prioridades de capa crecientes desde el núcleo. Los nombres de tipo y de parámetro no admiten «:».
- **Las líneas de contorno de área no encierran nada hasta que su transacción se confirma.** Dibuja las líneas en una transacción y crea las áreas en la siguiente. En la misma transacción, las áreas salen con 0 m².
- **Las habitaciones pueden conservar un área vieja** si su altura de cálculo queda por debajo del arranque de los muros. Al regenerar, caen a 0. Revisa el número de habitaciones y sus áreas cada vez que toques muros.
- **Habitaciones en una fase concreta:** `NewRoom(level, UV)` y `NewRooms2` las crean siempre en «Existente». Lo que respeta la fase:
  1. crear una habitación sin colocar con `doc.Create.NewRoom(fase)`;
  2. colocarla con `NewRoom(room, circuito)` en un circuito de `doc.get_PlanTopology(nivel, fase)`.
  - Antes tiene que existir una vista de planta de ese nivel y esa fase («Cannot find view for the room»).
  - `PlanTopology` no ve las líneas de separación de la misma transacción: coloca las habitaciones en la siguiente.
- **Los trasdosados pegados al muro unen todas las estancias de una fachada.** Hazlos no delimitadores y dibuja la línea de separación en su cara. Una línea de separación a menos de unos 2 cm de la cara de un muro, o dentro de él, hace que Revit ignore una de las dos.
- **Las líneas de separación que acaban justo en el extremo de un muro quedan unidas a él:** moverlas arrastra el muro (una fachada se movió 40 cm). Bórralas y dibuja otras.
- **Una habitación no pasa por un hueco de muro:** un vestíbulo en T son dos habitaciones con el mismo nombre.
- **Etiquetas de habitación y fases:** no se copian a una vista de otra fase (rotula con textos); `GetRoomAtPoint(p, fase)` solo encuentra las de esa fase; `NewRoomTag` y luego mover `TagHeadPosition` falla: crea la etiqueta directamente en el punto, tras comprobar que cabe. Si los volúmenes recortados ocultan las etiquetas, `ComputeVolumes = False` (las áreas no cambian).
- **Las copias (`CopyElement(s)`) toman la fase de la vista activa:** restaura `CreatedPhaseId` desde el original nada más copiar.
- **Revisa los techos nuevos contra los huecos de forjado de encima.** Un techo en la caja de escalera cortaba el tramo.
- **Terreno:**
  - `TopographyEditScope` sigue sirviendo para editar topografías antiguas.
  - `Toposolid.Create(doc, puntos, tipo, nivel)` acepta unos 12.000 puntos; las subdivisiones, con `CreateSubDivision`.
  - El nombre del tipo puede llevar un espacio duro: compara con `.replace('\xa0',' ')`.
  - Borrar toposólidos mientras recorres un colector de toposólidos cierra el script: recorre una lista.
  - Bajo escalones, pon el terreno plano por debajo y haz cada peldaño macizo.
  - Cortar el toposólido del levantamiento con suelos rompe sus cotas de nivel: no lo hagas.
  - Las cotas de las calles se leen en los alzados del proyecto, no en el terreno de un modelo heredado. Una calle en pendiente estaba casi plana.

## 4. Escaleras y barandillas

- **Las escaleras antiguas hechas por boceto no se editan por API.** Rehazlas con `StairsEditScope`.
- **Barandillas:**
  - Revit crea barandillas a los dos lados; borra las del lado del muro.
  - Una barandilla independiente debe alojarse en el tramo (`HostId` = id del tramo) para seguir su pendiente.
- **Un descansillo que no toca el tramo siguiente** abre un diálogo que bloquea la llamada.

## 5. Familias, instancias y copias

- **Familias basadas en nivel:** `NewFamilyInstance(XYZ(x, y, nivel.Elevation), símbolo, nivel, ...)` las coloca al doble de altura, porque la Z se toma como desfase sobre el nivel. Pasa z = 0.
- **Muebles:** colócalos y mídelos por el centro de su caja envolvente en coordenadas del modelo, y desde la cara del muro, no desde su eje (un cabecero y un sofá atravesaban un tabique). Multiplicar la transformación por el centro del símbolo da mal resultado en las instancias reflejadas.
- **`FamilyInstance.GetReferences` devuelve referencias del símbolo, no de la instancia.** Conviértelas antes de acotar con ellas:
  - `Reference.ParseFromStableRepresentation(doc, inst.UniqueId + ":0:INSTANCE:" + r.ConvertToStableRepresentation(doc))`.
- **Recargar una familia que tiene instancias conectadas** (en instalaciones) abre un diálogo bloqueante. Borra la red antes.
- **Familias de instalaciones:** la biblioteca local puede no tenerlas (están en la nube). Créalas con la API de familias, con sus conectores.
- **Si falla una transacción dentro de un documento de familia,** este se queda abierto: haz RollBack en el `except` y cierra el documento huérfano.
- **Puertas:** los parámetros de hoja definidos por fórmula son de solo lectura. Cambia solo el parámetro que manda o crea una familia propia.
- **Parámetro Comentarios:** los Opening y las DetailCurve no lo tienen. Comprueba `None` antes de usarlo.
- **`DirectShape` acepta categorías como Ventanas o Armazón estructural.** Sirve para piezas a medida que necesitan una Marca que otros procesos leen.
- **Ventanas con alféizar propio:** algunas familias traen un alféizar anidado que tapa el de piedra. Ocúltalo en la familia y guarda una copia de la original.
- **Las dimensiones de una ventana** vienen de parámetros de ejemplar, no del tipo, en algunas familias. Usa una sola función que las lea en todos los scripts: dos scripts leían el tipo, con medidas viejas, y los retornos de trasdosado salieron 20 cm dentro de los huecos.
- **Las ventanas de un levantamiento suelen ser genéricas de 1,00 m de alto exacto:** no te fíes de su altura.
- **Si la etiqueta de carpintería lee la Marca de tipo,** pon una marca de ejemplar única (por ejemplo «E20-07») para distinguir cada pieza.
- **`CopyElements` para alternativas:**
  - las puertas y ventanas alojadas viajan siempre con su muro;
  - dos ventanas en el mismo hueco (derribada y nueva) hacen que Revit borre una al azar: borra antes las copias de los huecos derribados;
  - una cubierta con pilares unidos no se copia junto («internal error»);
  - Revit copia también rellenos, bocetos y tramos que no estaban en la lista: vacía la zona antes de copiar y marca todo lo que hay en ella.

## 6. Geometría, DirectShape y nube de puntos

- **No redondees los puntos 3D de una cara inclinada** antes de `CreateExtrusionGeometry`: da «Non-planar CurveLoop». Pasa el origen y los ejes del plano y coordenadas 2D, y reconstruye los puntos en Revit.
- **DirectShape con hueco (en anillo):** `CreateExtrusionGeometry` necesita el lazo exterior en sentido antihorario y el hueco en horario, vistos desde +Z.
- **Las booleanas fallan con caras laterales coincidentes**, no solo con tapas coplanares. Pueden fallar sin avisar o no cortar nada.
  - Desplaza el contorno de corte unos milímetros.
  - Verifica con muestreo de puntos (`Solid.IntersectWithCurve`).
- **`SetShape` rechaza sólidos que salen de booleanas sobre un DirectShape.**
  - Rehaz la forma con extrusiones simples calculadas con shapely, sin astillas: abre 3 mm y ajusta a una rejilla de 1 mm.
  - `IsValidShape` es un método de instancia. Llamado sobre la clase, falla sin avisar si está dentro de un try.
- **«Fuera del eje»:** Revit avisa con líneas que están a menos de unos 0,15° de 0, 45, 90 o 135°. Ajústalas antes de crear nada.
- **Los contornos sacados de imágenes rasterizadas** dan avisos de «línea de boceto ligeramente fuera del eje». Endereza antes las aristas casi ortogonales.
- **Nube de puntos:**
  - `PointCloudInstance.GetPoints` acepta menos de 1.000.000 de puntos por llamada (usa 999.999); los planos del filtro van en coordenadas del modelo; pedir 1 mm de separación devuelve un punto cada unos 4 mm.
  - Revit ignora el medio tono y la transparencia en las nubes. Para un fondo tenue en una hoja: exporta una imagen solo con la nube, aclárala con PIL (opacidad de unos 0,2 sobre blanco) y colócala como `ImageInstance` de fondo; las vistas de la hoja, en alambre, porque en líneas ocultas los suelos tapan la imagen.
  - En las vistas 3D de comprobación, oculta `OST_PointClouds` o la nube lo tapa todo. Borra las vistas temporales antes de guardar.
- **Para muestrear cotas de suelo y terreno,** usa `ReferenceIntersector` con rayos verticales en vistas 3D isométricas temporales, una por fase, con filtro de categoría. Bórralas después.

## 7. Cotas

Ver la skill `acotar-planos`. Lo esencial:

- todas las referencias tienen que ser exactamente perpendiculares a la línea de cota;
- llama a `Regenerate()` dentro de la transacción, justo después de `NewDimension`;
- la línea de cota va en la z del plano de trabajo de la vista;
- referencias desviadas 0,003° también fallan; márcalas con líneas de detalle cortas;
- en un levantamiento acotado, cuenta las cotas antes y después de cada cambio (§2).

## 8. Vistas, plantillas, láminas y textos

- **Las plantillas de vista no se duplican con `View.Duplicate`.** Usa `ElementTransformUtils.CopyElements`.
- **Las vistas creadas por API se quedan con la plantilla por defecto** y sus parámetros salen como de solo lectura. Pon `ViewTemplateId = InvalidElementId` antes de editarlas.
- **Cambiar una plantilla la vuelve a aplicar en todas sus vistas** y deshace lo ocultado vista por vista. Así reaparecieron un vínculo y sus ejes en 40 vistas.
  - Antes, guarda la lista de elementos ocultos.
  - Después, vuelve a ocultarlos y compara las láminas con el juego anterior.
- **Lo que se cuela en las láminas:**
  - una planta con «subyacente» activo dibuja en gris la planta de abajo («tabiques fantasma», 1.284 trazos en una lámina): quítalo en las vistas de lámina;
  - los DWG importados de versiones antiguas salen como líneas sueltas en alzados y secciones: oculta las ImportInstance; un DWG de terreno 3D dibuja curvas bajo los suelos en las secciones;
  - las vistas heredadas pueden exportarse rasterizadas: rehazlas como secciones;
  - las líneas del parquet: oculta la subcategoría «Patrón de superficie» de Suelos;
  - las vistas duplicadas heredan las sombras (`ShadowIntensity = 0`) y pueden ocultar los textos (muestra `OST_TextNotes`).
- **Una vista de planta sin región de recorte se desplaza en la hoja** cuando cambian los límites del modelo. Cambiar el recorte de una vista ya colocada no la mueve.
- **Secciones:** `ViewSection.CreateSection` normaliza la caja y puede darle la vuelta: mira hacia la +BasisZ dada, con el corte en el otro extremo. Para mirar una fachada desde fuera, da BasisX invertida, el origen por dentro y Z de −profundidad a 0. Comprueba `ViewDirection` y `RightDirection` después, y compara cada sección con el proyecto: hacia dónde mira y por dónde corta (una miraba al lado contrario y una cota copiada caía en otro sitio; un corte que parece quebrado puede ser una sola diagonal).
- **No existe `PlanRegion` en esta API.** Para una planta con dos alturas de corte, haz dos vistas con recortes complementarios (`SetCropShape`) y colócalas alineadas por coordenadas del modelo.
- **Girar una planta en la hoja:** gira la vista (el elemento de su región de recorte) y vuelve a poner la forma del recorte, porque Revit la gira como un bloque. No gires la ventana gráfica: gira también los textos.
- **`FilteredElementCollector(doc, vista.Id)` no devuelve lo oculto en esa vista:** busca por `OwnerViewId` en un colector del documento.
- **Fases en las vistas:** las de una fase posterior necesitan el filtro «Reformado» (existente + nuevo). Con «Mostrar completo», lo derribado sale en rojo o amarillo discontinuo.
- **Las sustituciones de patrón de superficie** solo aceptan patrones de dibujo.
- **Las vistas en líneas ocultas no muestran el color de los materiales.** Pasa la vista temporal a sombreado con aristas antes de juzgar un color.
- **Colocar una vista en la hoja con precisión:**
  - Las vistas de planta tienen `GetProjectionToSheetTransform`: T(0,0,0) es el punto de la hoja donde cae el origen del modelo.
  - Las vistas de diseño no lo tienen. Colócala, exporta el PDF, mide un texto conocido y corrige `SetBoxCenter`.
  - Los cajetines del estudio (CR) tienen el origen en la esquina inferior derecha: las coordenadas de hoja salen negativas en x. Convierte antes de comparar con tu maqueta.
- **El contorno de una ventana gráfica en la hoja** es unos 3 mm mayor que su recorte; en una sección, unos 10 mm mientras el recorte de anotaciones esté activo. En una isométrica con caja de sección, ajusta el recorte a la caja proyectada.
- **Copiar a una vista de diseño un dibujo medido en el papel del PDF:**
  - usa escala 1:100; a 1:1 los segmentos cortos quedan por debajo de la tolerancia de 0,8 mm de Revit;
  - recorta la vista al marco y centra la ventana en el recorte.
- **Textos medidos en un PDF:** calibra con una prueba el tamaño y el punto de anclaje. En ALFERECES, altura en Revit ≈ altura en el PDF / 1,42; sin calibrar, los rótulos quedaron 0,7 mm bajos y salían tachados por sus líneas.
- **Las discontinuas vuelven a empezar en cada segmento**, así que una curva hecha de líneas cortas se ve continua. Dibuja tú las discontinuas.
- **`FilledRegion.Create` no funciona sobre una lámina.**
  - Crea la región en una vista de diseño, o dibuja las flechas o barras con un abanico de líneas.
  - Los rellenos de un PDF vienen triangulados. Únelos con shapely y pasa los huecos como CurveLoops adicionales.
- **Las vistas que ocultan la categoría Líneas** no muestran las cruces hechas con líneas de detalle: marca los puntos con pequeñas regiones rellenas.
- **Revit rechaza líneas de menos de unos 1,2 mm en una hoja.**
- **Las líneas de detalle unidas por los extremos no se pueden mover.** Recréalas con la curva desplazada y el mismo estilo de línea.
- **Un estilo de línea que fija un script lo puede resetear otro posterior:** define sus colores en cada script que lo use.
- **Nombres:** los de vistas y hojas no admiten «:» ni «?»; los de tipos de región rellena, tampoco `< > { } [ ] | ; ? ~`.
- **Las notas de texto copiadas conservan el ancho del original** y parten las líneas. Ajusta `Width` después de cambiar el texto.
- **Cajetín y familias de anotación:**
  - los rótulos (Label) de un cajetín no se crean por API: edita una copia de la familia;
  - la casilla de versión suele ser un parámetro de Información de proyecto («Estado del proyecto»), no un texto fijo;
  - el blanco puro (255,255,255) sale negro en el PDF: usa 254;
  - las regiones sólidas de una familia necesitan `IsMasking`;
  - haz una familia por formato: las líneas se movían al cambiar de tipo.
- **Las anotaciones toman el tamaño de la escala a la que se crearon.**
- **Rótulos semitransparentes (velo al 50 %):** texto transparente sobre una región rellena blanca, con `OverrideGraphicSettings.SetSurfaceTransparency(50)` en la vista; contorno con el estilo «<Líneas invisibles>» (`OST_InvisibleLines`), no «<Líneas ocultas>», que es discontinuo. No dimensiones el velo con la caja de la nota de texto: ciñelo a las letras con unos 0,3–0,5 mm de margen y una altura de línea de unos 1,72 × el tamaño de letra.
- **Revisar un modelo cuando Revit está ocupado con otro proyecto:** trabaja sobre una exportación de su geometría (vistas z-buffer, cortes de planta, secciones, rayos).
