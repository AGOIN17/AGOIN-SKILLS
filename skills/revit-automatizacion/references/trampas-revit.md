# Trampas de Revit por API y Dynamo

Encontradas con Revit 2027 y Dynamo 4 (PythonNet3), octubre de 2026, en el proyecto ALFERECES. Cada una costó tiempo una vez.

## Índice

1. Dynamo y el canal de comunicación
2. Muros
3. Suelos, bocetos, huecos, habitaciones y terreno
4. Escaleras y barandillas
5. Familias e instancias
6. Geometría, booleanas y DirectShape
7. Cotas
8. Vistas, plantillas, láminas y textos

---

## 1. Dynamo y el canal de comunicación

- **No se puede hacer por API (comprobado en Revit 2027):**
  - opciones de diseño;
  - transferir normas de proyecto entre archivos;
  - parte del manejo de fases.
  
  Usa copias del modelo, o deja esos pasos al usuario, igual que la actualización de plantillas. Las copias de elementos toman la fase de la vista activa.
- **Guarda antes de crear habitaciones en bucle.** Un bucle de `NewRoom` cerró Revit y se perdió lo no guardado.
- **Revit borra cotas al confirmar** si sus referencias cambian. Anótalas antes y vuelve a dibujarlas después.
- **PythonNet:**
  - `ElementId` como clave de diccionario falla: usa `.Value`;
  - los parámetros de salida (out) vuelven como tuplas.
- **Rutas dentro de argumentos JSON:** escríbelas con barras normales (`D:/ARQ/...`). Las barras invertidas rompen el JSON con el error «se esperaba closebracket».
- **Entrada como lista:** si se pasa una lista como entrada, IN[0] es la lista. Un script que espera una cadena necesita la cadena, no `[cadena]`.
- **«error return without exception set»:** en PythonNet casi siempre es por indexar una ICollection de .NET, por ejemplo `stairs.GetStairsRuns()[0]` o `CopyElements(...)[0]`.
  - Convierte antes: `list(...)[0]`.
  - En los colectores por tipo, pasa la clase (`StairsRunType`), no `obj.GetType()`.
- **Clases que heredan de una interfaz .NET** (IFailuresPreprocessor): cada una necesita un `__namespace__` único en el script.
- **Un script largo puede agotar el tiempo de la llamada mientras Revit sigue trabajando.**
  - Comprueba si hay un diálogo abierto (EnumWindows). Si no lo hay, Revit sigue ocupado.
  - Espera y consulta el estado antes de relanzar.
- **Tras reiniciar Dynamo**, la primera llamada puede responder «tool not found». Reintenta una vez.
- **Rutas escritas desde Bash:** en la herramienta Bash de Claude Code, una doble barra invertida dentro de un heredoc llega a Python como una sola, incluso con `<<'EOF'`. Una ruta con `\a` se convirtió en el carácter BEL.
  - Escribe los scripts con la herramienta de escritura de archivos.
  - Escribe las rutas con `/`.
  - O edita los archivos con la herramienta de edición.

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
- **«No es posible mantener unidos / cortar elemento unido»:** sale al subir, bajar o recortar un muro unido a losas o vigas. Hay dos salidas:
  - `JoinGeometryUtils.UnjoinGeometry` con cada elemento unido, antes del cambio;
  - un preprocesador que llame a `fa.ResolveFailure(f)` solo para ese fallo (su resolución por defecto es separar la unión) y devuelva `ProceedWithCommit`.
- **Nunca aceptes en bloque las resoluciones por defecto de Revit.** En otro proyecto borraron una fachada levantada y sus cotas. Cuenta los elementos antes y después de cada transacción.
- **Si un script separa uniones en su propia transacción y luego falla, quedan separadas.**
  - Recupera las uniones originales desde una copia de seguridad abierta en segundo plano.
  - Antes de abrirla, descarga sus vínculos con `TransmissionData`. Al terminar, ciérrala sin guardar.
- **`JoinGeometry` solo oculta la arista entre dos muros si son coplanares de verdad.** El usuario ve un escalón de 0,4 mm. Lleva cada cara exterior a su plano y une todos los pares que se tocan.
- **Las uniones de extremo pueden recortar la cara exterior** y dejar ranuras de 2 o 3 cm junto a un rehundido. Búscalas.
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

## 3. Suelos, bocetos, huecos, habitaciones y terreno

- **`SketchEditScope` es poco fiable desde Dynamo.** A veces no arranca, y otras no se cierra si queda una transacción abierta. Hay dos alternativas:
  - recortar con un hueco: `doc.Create.NewOpening(suelo, curvas, True)`;
  - recrear el suelo con el mismo tipo, nivel, desfase, marca, comentario y fase. El id cambia, así que actualiza todo lo que lo referencia.
  - Después de un fallo, mira `doc.IsInEditMode()`.
- **Si se usa `SketchEditScope`:**
  - una línea de boceto bloqueada no se puede borrar; reutilízala con `SetGeometryCurve(linea, True)`;
  - separa las uniones antes de encoger un suelo;
  - no llames a `doc.Regenerate()` fuera de una transacción después del commit.
- **Las líneas de contorno de área no encierran nada hasta que su transacción se confirma.** Dibuja las líneas en una transacción y crea las áreas en la siguiente. En la misma transacción, las áreas salen con 0 m².
- **Las habitaciones pueden conservar un área vieja** si su altura de cálculo queda por debajo del arranque de los muros. Al regenerar, caen a 0. Revisa el número de habitaciones y sus áreas cada vez que toques muros.
- **Revisa los techos nuevos contra los huecos de forjado de encima.** Un techo en la caja de escalera cortaba el tramo.
- **Terreno y calles:**
  - `TopographyEditScope` sigue sirviendo para editar topografías antiguas.
  - Las cotas de las calles se leen en los alzados del proyecto, no en el terreno de un modelo heredado. Una calle en pendiente estaba casi plana.

## 4. Escaleras y barandillas

- **Las escaleras antiguas hechas por boceto no se editan por API.** Rehazlas con `StairsEditScope`.
- **Barandillas:**
  - Revit crea barandillas a los dos lados; borra las del lado del muro.
  - Una barandilla independiente debe alojarse en el tramo (`HostId` = id del tramo) para seguir su pendiente.
- **Un descansillo que no toca el tramo siguiente** abre un diálogo que bloquea la llamada.

## 5. Familias e instancias

- **Familias basadas en nivel:** `NewFamilyInstance(XYZ(x, y, nivel.Elevation), símbolo, nivel, ...)` las coloca al doble de altura, porque la Z se toma como desfase sobre el nivel. Pasa z = 0.
- **Muebles:** colócalos y mídelos por el centro de su caja envolvente en coordenadas del modelo. Multiplicar la transformación por el centro del símbolo da mal resultado en las instancias reflejadas.
- **`FamilyInstance.GetReferences` devuelve referencias del símbolo, no de la instancia.** Conviértelas antes de acotar con ellas:
  - `Reference.ParseFromStableRepresentation(doc, inst.UniqueId + ":0:INSTANCE:" + r.ConvertToStableRepresentation(doc))`.
- **Recargar una familia que tiene instancias conectadas** (en instalaciones) abre un diálogo bloqueante. Borra la red antes.
- **Familias de instalaciones:** la biblioteca local puede no tenerlas (están en la nube). Créalas con la API de familias, con sus conectores.
- **Parámetro Comentarios:** los Opening y las DetailCurve no lo tienen. Comprueba `None` antes de usarlo.
- **`DirectShape` acepta categorías como Ventanas o Armazón estructural.** Sirve para piezas a medida que necesitan una Marca que otros procesos leen.
- **Ventanas con alféizar propio:** algunas familias traen un alféizar anidado que tapa el de piedra. Ocúltalo en la familia y guarda una copia de la original.

## 6. Geometría, booleanas y DirectShape

- **No redondees los puntos 3D de una cara inclinada** antes de `CreateExtrusionGeometry`: da «Non-planar CurveLoop». Pasa el origen y los ejes del plano y coordenadas 2D, y reconstruye los puntos en Revit.
- **Las booleanas fallan con caras laterales coincidentes**, no solo con tapas coplanares. Pueden fallar sin avisar o no cortar nada.
  - Desplaza el contorno de corte unos milímetros.
  - Verifica con muestreo de puntos (`Solid.IntersectWithCurve`).
- **`SetShape` rechaza sólidos que salen de booleanas sobre un DirectShape.**
  - Rehaz la forma con extrusiones simples calculadas con shapely, sin astillas: abre 3 mm y ajusta a una rejilla de 1 mm.
  - `IsValidShape` es un método de instancia. Llamado sobre la clase, falla sin avisar si está dentro de un try.
- **«Fuera del eje»:** Revit avisa con líneas que están a menos de unos 0,15° de 0, 45, 90 o 135°. Ajústalas antes de crear nada.
- **Los contornos sacados de imágenes rasterizadas** dan avisos de «línea de boceto ligeramente fuera del eje». Endereza antes las aristas casi ortogonales.

## 7. Cotas

Ver la skill `acotar-planos`. Lo esencial:

- todas las referencias tienen que ser exactamente perpendiculares a la línea de cota;
- llama a `Regenerate()` dentro de la transacción, justo después de `NewDimension`;
- la línea de cota va en la z del plano de trabajo de la vista;
- referencias desviadas 0,003° también fallan; márcalas con líneas de detalle cortas.

## 8. Vistas, plantillas, láminas y textos

- **Las plantillas de vista no se duplican con `View.Duplicate`.** Usa `ElementTransformUtils.CopyElements`.
- **Cambiar una plantilla la vuelve a aplicar en todas sus vistas** y deshace lo ocultado vista por vista. Así reaparecieron un vínculo y sus ejes en 40 vistas.
  - Antes, guarda la lista de elementos ocultos.
  - Después, vuelve a ocultarlos y compara las láminas con el juego anterior.
- **Una vista de planta sin región de recorte se desplaza en la hoja** cuando cambian los límites del modelo. Cambiar el recorte de una vista ya colocada no la mueve.
- **Las sustituciones de patrón de superficie** solo aceptan patrones de dibujo.
- **Las vistas en líneas ocultas no muestran el color de los materiales.** Pasa la vista temporal a sombreado con aristas antes de juzgar un color.
- **Colocar una vista en la hoja con precisión:**
  - Las vistas de planta tienen `GetProjectionToSheetTransform`: T(0,0,0) es el punto de la hoja donde cae el origen del modelo.
  - Las vistas de diseño no lo tienen. Colócala, exporta el PDF, mide un texto conocido y corrige `SetBoxCenter`.
- **Copiar a una vista de diseño un dibujo medido en el papel del PDF:**
  - usa escala 1:100; a 1:1 los segmentos cortos quedan por debajo de la tolerancia de 0,8 mm de Revit;
  - recorta la vista al marco y centra la ventana en el recorte.
- **Las discontinuas vuelven a empezar en cada segmento**, así que una curva hecha de líneas cortas se ve continua. Dibuja tú las discontinuas.
- **`FilledRegion.Create` no funciona sobre una lámina.**
  - Crea la región en una vista de diseño, o dibuja las flechas con un abanico de líneas.
  - Los rellenos de un PDF vienen triangulados. Únelos con shapely y pasa los huecos como CurveLoops adicionales.
- **Las líneas de detalle unidas por los extremos no se pueden mover.** Recréalas con la curva desplazada y el mismo estilo de línea.
- **Los nombres de vista no admiten «:».**
- **Las notas de texto copiadas conservan el ancho del original** y parten las líneas. Ajusta `Width` después de cambiar el texto.
- **La casilla de versión del cajetín** suele ser un parámetro de Información de proyecto («Estado del proyecto»), no un texto fijo.
- **El contorno de una ventana gráfica en la hoja** es unos 3 mm mayor que su recorte.
- **Las anotaciones toman el tamaño de la escala a la que se crearon.**
- **Las dimensiones de una ventana** vienen de parámetros de ejemplar, no del tipo, en algunas familias.
- **Rótulos semitransparentes:** para darles un fondo al 50 %, usa una región rellena con transparencia.
- **Revisar un modelo cuando Revit está ocupado con otro proyecto:** trabaja sobre una exportación de su geometría (vistas z-buffer, cortes de planta, secciones, rayos).
