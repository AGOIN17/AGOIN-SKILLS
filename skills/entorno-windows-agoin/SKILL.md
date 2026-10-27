---
name: entorno-windows-agoin
description: "Trampas del entorno de trabajo de AGOIN que ya han hecho perder horas. Cubre Windows 11, Git Bash y PowerShell, el servidor de la oficina, las varias cuentas de GitHub, Google/Firebase y Cloudflare, Docker Desktop y el espacio en disco. Úsala antes de lanzar comandos de consola, scripts largos o compilaciones en Windows, al trabajar con rutas del servidor (\\\\servidorw12), al hacer git push, al desplegar o usar gcloud, firebase o cloudflared, y cuando un comando falle de forma rara («Repository not found», 403, rutas cambiadas, caracteres raros, disco lleno)."
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
    - Escribe los scripts con la herramienta de escritura de archivos.
    - O usa `/` o `chr(92)` en las rutas y en las expresiones regulares.
- **Node ESM necesita `file:///C:/...`** para las rutas absolutas.
- **PowerShell:**
  - `| Select-Object -First N` corta el comando que lo alimenta en cuanto llegan N objetos. Así se paró un servicio en producción.
  - `-Last N` espera a toda la salida.
  - En PowerShell 5.1, `Get-ScheduledTask` se cuelga: usa `schtasks.exe`.
  - El COM desde PowerShell necesita la versión 5.1 con `-STA`.
  - En PowerShell 7, `ConvertFrom-Json` convierte las fechas ISO en DateTime, y la configuración española intercambia día y mes.
  - El entorno bloquea `Remove-Item` con rutas que contienen una letra de unidad dentro de una variable.
    - Escribe la ruta literal, para que el permiso se pueda revisar.
    - No lo esquives metiendo el borrado en un script.
- **Codificación:**
  - respeta los finales de línea de cada archivo (CRLF o LF);
  - en las tareas programadas, fuerza la salida en UTF-8; si no, cp1252 rompe caracteres como «→» o «ñ»;
  - sigue la convención de idioma de cada repositorio; los textos que lee el usuario van con tildes.
- **Tareas programadas que corren solas:**
  - `npx` puede quedarse esperando un «Ok to proceed?»: usa `npx --yes` o instala la dependencia;
  - una tarea con la opción «no iniciar una nueva instancia» y un límite de 72 h dejó una sincronización parada 20 días;
  - enseña lo recientes que son los datos con un indicador verde, ámbar o rojo.

## Cuentas

- **GitHub tiene varias identidades en el mismo equipo: la de la empresa (AGOIN17) y otras personales.**
  - Un «Repository not found» o un push denegado suele significar que la cuenta activa es la equivocada, no que las credenciales estén mal.
  - Cambia con `gh auth switch --user <cuenta>` y, al terminar, vuelve a dejar la que estaba.
  - Si usas el token de una cuenta, pásalo en una variable sin imprimirlo nunca.
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
- **Las tareas en segundo plano tienen un límite de 1 hora** por defecto.
- **No toques otros proyectos de Docker, ni puertos ya en uso, ni el antivirus,** sin preguntar.
