---
name: automatizar-programas-windows
description: "[WINDOWS] Cómo manejar desde un script programas de escritorio de Windows y webs con sesión cuando su API no llega (Robot, AutoCAD, Presto, CYPE, Word, Excel, Chrome…; en el Revit del usuario solo leer sus diálogos, y en una instancia propia ver revit-automatizacion) con pywinauto, UI Automation y COM, sin estropear el trabajo del usuario. Cubre trabajar en una instancia propia y visible, no tocar nunca su ventana de trabajo, teclear en vez de WM_SETTEXT, diálogos anidados, reintentos, capturas, e imprimir solo con «Microsoft Print to PDF» comprobando la impresora. Úsala cuando haya que pulsar, rellenar, leer o imprimir en la ventana de un programa, cuando un diálogo bloquee un proceso, al convertir documentos a PDF en Windows, al automatizar AutoCAD o al manejar una web cuando «Claude in Chrome» no conecta."
metadata:
  etiquetas: "WINDOWS"
---

# Manejar programas de Windows desde código

Cuando un programa no deja hacer algo por su API (definir el terreno en Robot, imprimir un plano), se puede manejar su ventana desde un script. Funciona, pero tiene dos riesgos:

- llevarse por delante el trabajo del usuario;
- mandar decenas de hojas a la impresora física de la oficina.

Estas reglas evitan los dos.

## Reglas

- **Antes de empezar, explica qué vas a hacer y pide el visto bueno** la primera vez; después, avisa cada vez que vayas a manejar la ventana.
  - El usuario verá el programa moverse solo.
  - Pídele que no toque esa ventana mientras trabaja.
- **Trabaja en una instancia del programa abierta por ti, con un archivo copia.**
  - No uses la ventana en la que trabaja el usuario (su Revit, su Excel abierto).
  - No pulses en ella.
- **Al terminar, cierra tu instancia y espera a que el proceso acabe.**
  - Mata solo procesos que hayas abierto tú: guarda su PID.
  - Nunca mates procesos por su nombre.
- **Si un diálogo de un programa del usuario bloquea algo,** lee su texto y sus botones sin pulsar nada, y pregúntale. En una instancia abierta por ti sí puedes manejarlo, avisando y con mensajes dirigidos a su proceso.
- **Imprime solo con «Microsoft Print to PDF».**
  - Selecciónala y comprueba que el desplegable la muestra y que el tipo de impresora dice PDF.
  - Si no se cumple, cancela.
  - Nunca aceptes un diálogo de impresión con otra impresora: la predeterminada de la oficina es física.
  - Usa `scripts/imprimir_pdf.py`: no sobrescribe un PDF que ya exista.
  - **Papel, solo si el usuario lo pide expresamente.** Entonces se imprime en la impresora que él nombre, por línea de comandos (en la oficina, PdfCraft), nunca aceptando un diálogo.
- **Captura la ventana en cada paso importante.** Sirve de prueba para el usuario y para depurar.
- **Si creas archivos en la configuración del usuario** (preajustes, plantillas), díselo y explícale cómo quitarlos.
- **No saltes protecciones:** captchas, bloqueos anti-robot, licencias, el reloj del sistema. Usa las vías legítimas.
- **Las contraseñas las teclea el usuario.** Tú no las manejas.

## Técnica con pywinauto

- **Dos backends:**
  - `uia`, para encontrar ventanas, pestañas y botones e invocarlos con `invoke()`;
  - `win32`, para los controles por id (`child_window(control_id=...)`), los desplegables (`.select()`) y los campos de texto.
- **Los campos se rellenan tecleando:** `edit.type_keys("{HOME}+{END}{DEL}" + valor + "{TAB}")`.
  - Muchos programas no registran `set_edit_text` ni `WM_SETTEXT`.
  - Cuidado con la coma decimal de la configuración española.
- **Busca los diálogos por título y por clase (`#32770`), y solo en el proceso de tu instancia.**
  - Pueden estar anidados: el «Guardar impresión como» aparece dentro de la ventana de progreso de la impresión.
- **Reintenta con espera** todo lo que depende de que la ventana esté lista (pestañas, diálogos). Espera comprobando, no con un `sleep` largo fijo.
- **Barras de herramientas y paneles:** en algunos programas son `Pane` en UIA. Identifícalos por nombre e índice, y confírmalo con una captura.
- **Antes de pulsar un botón de aviso** («Sí», «Aceptar»), lee y guarda su texto.
- **Diálogos MFC** (como los de Revit o Robot), solo en instancias propias: no exponen patrones de UI Automation, pero los botones aceptan BM_CLICK; las rejillas Objective Grid aceptan WM_LBUTTONDOWN y WM_CHAR, y su edición interna (GXEDIT) WM_SETTEXT; `PrintWindow` captura un diálogo aunque esté tapado.
- **Las cintas WPF** (el botón de Dynamo en Revit) no responden a mensajes enviados: hace falta un clic real del ratón. Solo en tu instancia, nunca en la del usuario. Pide permiso, comprueba que la ventana está delante, hazlo cuando el usuario no esté usando el equipo y repite si el clic cayó en otra ventana.
- **Para que un programa no coja un puerto al arrancar** (8080), ocúpalo un rato con un `HttpListener` de relleno en segundo plano y suéltalo después.

## Navegador con sesión

Si hay que manejar una web que pide iniciar sesión y «Claude in Chrome» no conecta (desde la extensión de VS Code no aparecieron sus herramientas, ni con `/chrome` ni con `@browser`):

- abre un Chrome **aparte**, con `--remote-debugging-port=<puerto>` y `--user-data-dir=<perfil vacío propio>`; no toques el Chrome del usuario;
- el usuario teclea su clave en esa ventana: tú no la ves ni la guardas;
- manéjalo con `playwright-core` y `connectOverCDP`;
- pide al usuario que no cierre esa ventana mientras trabajas.

Funcionó a la primera. Si la web es una app de AGOIN en producción, sigue además `desarrollo-apps-agoin` («Usar una app en producción como usuario»).

## COM

- **Instancias:** `win32com.client.gencache.EnsureDispatch(...)` da acceso a constantes y tipos; `DispatchEx` crea una instancia nueva y no se engancha a la del usuario.
- **Muchos programas se cierran cuando muere el proceso de Python que los abrió.** No dejes instancias huérfanas, y no cuentes con ellas después de un fallo.
- **Word a PDF:**
  - abre el documento con `ReadOnly=True` y `AddToRecentFiles=False`, y pon `DisplayAlerts = 0`;
  - exporta con `doc.ExportAsFixedFormat(ruta, 17)`.
- **Excel por COM se cuelga a menudo.**
  - Para leer o crear libros, usa openpyxl o xlrd.
  - Para modificar un libro del usuario, trabaja sobre una copia y comprueba que no se pierden imágenes, gráficos ni macros: openpyxl los puede eliminar.
- **RTF de programas técnicos con varias tablas de fuentes pegadas:** en Word salen en letras griegas. Une las tablas con `calculo-estructural/scripts/rtf_unir_tablas.py`.

## AutoCAD

- **AutoCAD LT no tiene COM.**
  - ODA File Converter convierte DWG y DXF, pero su versión gratuita es para uso no comercial. Comprueba la licencia antes de usarlo en un encargo.
  - La alternativa es guardar el DXF a mano desde AutoCAD LT.
- **AutoCAD completo:**
  - usa `accoreconsole` con guiones `.scr`;
  - pon los comandos con el prefijo `_.`, porque la interfaz está en español;
  - una línea en blanco al final del `.scr` lo deja colgado;
  - borra después el `plot.log` y los informes de error.
- **Los nombres de comando cambian entre versiones.** Revisa los alias.

## PDF en la oficina

- **No recomiendes Adobe.**
  - El estudio se está pasando a PDF-XChange.
  - El usuario quitó Acrobat a propósito.
- **Imprimir un PDF por comandos:**
  - con PdfCraft (`pdfcraft-cli.exe run --script pasos.json`);
  - o con `PDFXEdit.exe /printto`.
- **Plóter:** va por un puerto TCP/IP con IP fija, no por WSD. Si una cola se atasca, revisa primero el puerto.
