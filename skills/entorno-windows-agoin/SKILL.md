---
name: entorno-windows-agoin
description: "[WINDOWS] Trampas del entorno de trabajo de AGOIN que ya han hecho perder horas. Cubre Windows 11, Git Bash y PowerShell, el servidor de la oficina, las varias cuentas de GitHub, Google/Firebase y Cloudflare, Docker Desktop y el espacio en disco. Úsala antes de lanzar comandos de consola, scripts largos o compilaciones en Windows, al trabajar con rutas del servidor (\\\\servidorw12), al hacer git push, al desplegar o usar gcloud, firebase o cloudflared, y cuando un comando falle de forma rara («Repository not found», 403, rutas cambiadas, caracteres raros, disco lleno, archivo bloqueado)."
metadata:
  etiquetas: "WINDOWS"
---

# El entorno de AGOIN (Windows)

## Servidor de la oficina

- **`\\servidorw12` es de solo lectura para ti.**
  - Cualquier escritura necesita confirmación expresa para esa operación o ese lote: mover, renombrar, borrar, sobrescribir, e incluso crear carpetas o repositorios.
  - Antes, haz una copia; después, deja registro.
  - El orden es: vista previa, confirmación y ejecución.
  - Palabras del usuario: «no toques nada, no borres nada, que la liamos».
- **No compiles desde rutas UNC.**
  - cmd.exe no acepta un directorio UNC, así que npm, vite, tsc o firebase fallan. Trabaja en un clon local.
  - Leer y editar archivos en rutas UNC sí funciona.

## Consola

- **Git Bash convierte las rutas que empiezan por `/`** (`/app`, `/tmp`) en rutas de Windows.
  - Usa `MSYS_NO_PATHCONV=1` o PowerShell.
  - En Bash, `JAVA_HOME` y `PATH` van con la forma `/d/...`.
- **No metas código largo en la línea de comandos.**
  - Los heredocs de más de unos 40 KB fallan.
  - `python -c` y `node -e` se comen comillas y `$`, y lo que va entre comillas invertidas se ejecuta.
  - Escribe un archivo y ejecútalo. Para parchear un archivo, usa la herramienta de edición.
- **Rutas de Windows dentro de cadenas de Python.**
  - `\a`, `\n` y las secuencias octales las corrompen: `dynamo\162` acabó en `dynamor`. Usa cadenas raw o barras normales.
  - En la herramienta Bash de Claude Code, una doble barra invertida dentro de un heredoc llega al archivo como una sola, **incluso con `<<'EOF'`**. Se comprobó el 27/10/2026.
    - Escribe los scripts con la herramienta de escritura de archivos, y cualquier cambio que lleve barras invertidas, con la herramienta de edición. En CHIVERO pasó otras cinco veces (`\n` convertido en salto de línea, `\162` en «r»), y volvió a pasar al escribir esta misma regla.
    - O usa `/` o `chr(92)` en las rutas y en las expresiones regulares.
- **Dos cuelgues de la herramienta Bash:** un `cat > archivo` sin entrada estándar colgó una tarea en segundo plano, y un heredoc con `< /dev/null` rompió el intérprete de Python. Escribe los archivos con la herramienta de escritura.
- **`python -I` aísla también los imports locales:** los scripts del proyecto que importan módulos hermanos fallan. Úsalo solo para leer datos descargados; los scripts propios, sin `-I`.
- **Registra los servidores MCP con `claude mcp add-json` desde Bash:** el `claude.ps1` de PowerShell se come el `--`.
- **Node ESM necesita `file:///C:/...`** para las rutas absolutas.
- **PowerShell:**
  - `| Select-Object -First N` corta el comando que lo alimenta en cuanto llegan N objetos. Así se paró un servicio en producción.
  - `-Last N` espera a toda la salida.
  - En PowerShell 5.1, `Get-ScheduledTask` se cuelga: usa `schtasks.exe`.
  - El COM desde PowerShell necesita la versión 5.1 con `-STA`.
  - En PowerShell 7, `ConvertFrom-Json` convierte las fechas ISO en DateTime, y la configuración española intercambia día y mes.
  - Las variables no distinguen mayúsculas: `$t` pisó a `$T`.
  - El entorno bloquea `Remove-Item` con rutas que contienen una letra de unidad dentro de una variable.
    - Escribe la ruta literal, para que el permiso se pueda revisar.
    - No lo esquives metiendo el borrado en un script. Si el bloqueo parece un falso positivo, pregunta al usuario.
- **Codificación:**
  - respeta los finales de línea de cada archivo (CRLF o LF);
  - **en cualquier script de Python que imprima en la consola**, fuerza la salida en UTF-8 (`PYTHONIOENCODING=utf-8` o `sys.stdout.reconfigure(encoding="utf-8")`), no solo en las tareas programadas: los textos de PDF traen caracteres que cp1252 no imprime (viñetas, «≈», «→») y el script se cae a mitad, a veces en el último `print`, después de haberlo escrito todo;
  - abre y escribe los archivos con `encoding="utf-8"` explícito; un JSON guardado en cp1252 estropeó los textos de una web;
  - sigue la convención de idioma de cada repositorio; los textos que lee el usuario van con tildes.
- **Tareas programadas que corren solas:**
  - `npx` puede quedarse esperando un «Ok to proceed?»: usa `npx --yes` o instala la dependencia;
  - una tarea con la opción «no iniciar una nueva instancia» y un límite de 72 h dejó una sincronización parada 20 días;
  - enseña lo recientes que son los datos con un indicador verde, ámbar o rojo.

## Cuentas

- **GitHub tiene varias identidades en el mismo equipo: la de la empresa (AGOIN17) y otras personales.**
  - Un «Repository not found» o un push denegado suele significar que la cuenta activa es la equivocada, no que las credenciales estén mal.
  - Cambia con `gh auth switch --user <cuenta>` y, al terminar, vuelve a dejar la que estaba.
  - No extraigas tokens para pegarlos en URLs: usa `gh auth switch` y el ayudante de credenciales de gh (`git -c credential.helper= -c "credential.helper=!gh auth git-credential" push …`), y vuelve a dejar la cuenta que estaba. El token nunca se imprime.
  - No cambies la identidad global de git. Si hace falta, configúrala solo en ese repositorio.
- **Google: hay varias cuentas en firebase y gcloud.**
  - Pasa `--account` y el proyecto de forma explícita. El proyecto por defecto de gcloud es de otra app.
  - Las credenciales por defecto de aplicación (ADC) son otra identidad, distinta del inicio de sesión de la CLI.
- **Cloudflare: hay dos cuentas.** Un túnel creado en la cuenta equivocada da error 1033 aunque el CNAME esté bien.
- **Contraseñas:**
  - las teclea el usuario;
  - no las leas de almacenes de credenciales;
  - no las escribas en código, archivos .md, memoria ni registros.

## Disco, Docker y procesos

- **Mira el espacio libre antes de compilaciones grandes, renders o generaciones masivas.**
  - Un disco al 100 % tumbó Docker y producción.
  - Revit se cierra o no guarda cuando el disco se llena.
  - No borres Windows.old a mano.
- **Docker Desktop no arranca solo y pide permisos de administrador.** Una actualización automática puede dejarlo parado en un diálogo.
- **Las tareas en segundo plano tienen un límite de 1 hora** por defecto (comprobado en octubre de 2026). Cómo esperar bien: ver `optimizar-trabajo`.
- **Windows no deja mover ni sobrescribir un archivo abierto** (`PermissionError`), ni por tu propio script ni por el usuario.
  - Antes de regenerar, mira qué entregables están bloqueados, regenera el resto y pide en un solo mensaje que cierre esos archivos concretos. Hubo que pedirlo dos veces.
  - Cierra el documento en tu script antes de `os.replace`.
  - Escribe los entregables grandes (vídeo, PDF, BC3) con un nombre temporal y renómbralos al terminar.
  - Si el usuario va a editar un archivo mientras trabajas, dale una copia y no escribas en ella mientras la tenga abierta.
- **No toques otros proyectos de Docker, ni puertos ya en uso, ni el antivirus,** sin preguntar.
