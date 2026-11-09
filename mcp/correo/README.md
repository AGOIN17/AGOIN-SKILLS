# MCP «correo-agoin»

Conecta Claude Code con **tu correo de agoin.es** (Dinahosting). Cada persona configura su propio buzón.

- **Recibir:** IMAP, `mail.agoin.es:993`.
- **Enviar:** SMTP, `mail.agoin.es:465`.

Cuándo y cómo usarlo lo explica la skill [`correo-agoin`](../../skills/correo-agoin/SKILL.md).

## Herramientas

| Tipo | Herramientas |
|---|---|
| Lectura | `buscar_correos`, `leer_correo`, `guardar_adjuntos`, `carpetas` |
| Enviar | `enviar_correo`, `responder_correo`, `reenviar_correo`, `guardar_borrador`, `enviar_borrador` |
| Organizar | `marcar_correos` (leído, destacado), `mover_correos`, `borrar_correos`, `crear_carpeta`, `renombrar_carpeta`, `borrar_carpeta` |

**Protecciones:**
- `borrar_correos` manda a la papelera. Para borrar para siempre hace falta `definitivo: true`.
- `borrar_carpeta` solo borra carpetas vacías, y nunca las especiales (entrada, enviados, borradores, papelera, spam).
- Lo que se envía queda guardado en Enviados.
- Leer un correo no lo marca como leído.
- Para dejar solo las herramientas de lectura: variable de entorno `CORREO_SOLO_LECTURA=1`, o `"soloLectura": true` en `config.json`.

## Puesta en marcha (una vez por persona)

1. **Node.js 20 o superior.** El paquete `dist/correo-agoin.mjs` lleva todas las librerías dentro.
2. **Configura tu buzón** en una consola:

   ```
   node "<ruta>/mcp/correo/dist/correo-agoin.mjs" --configurar
   ```

   - Pide tu correo, el nombre que verán los destinatarios y tu contraseña (no se muestra).
   - Guarda `%USERPROFILE%\.correo-agoin\config.json` y la contraseña cifrada con la protección de Windows (DPAPI) en `clave.dpapi`: solo tu usuario de Windows, en ese equipo, puede descifrarla.
   - Al acabar, prueba la conexión de recibir y la de enviar.
   - Con el plugin, la ruta exacta la da el propio conector: si llamas a una herramienta sin haber configurado, te devuelve la orden que hay que ejecutar.
3. **Registro del conector:**
   - con el plugin `agoin`, se registra solo (en `/mcp` aparece como `plugin:agoin:correo-agoin`);
   - a mano: `claude mcp add correo-agoin --scope user -- node <ruta>/mcp/correo/dist/correo-agoin.mjs`.

   Usa solo una de las dos formas.
4. **Reinicia Claude Code.**

**Si algo falla:**
- `--probar` prueba IMAP y SMTP sin enviar nada.
- `--probar-clave` comprueba que la contraseña guardada se descifra, sin mostrarla.
- Si cambias la contraseña del correo, vuelve a ejecutar `--configurar`.

**Opcional en `config.json`:** `"firma"`, un texto que se añade al final de lo que se envía.

## Para desarrollar

- **Código:** está en `server.mjs`. Se regenera el paquete con `npm install` y después `npm run build`.
- **Cómo se probó** (09/11/2026, sobre un buzón real y solo con correos de prueba enviados a uno mismo): 47 comprobaciones, con el código fuente y con el paquete aislado. Se probó enviar con adjunto y tildes, leer sin marcar, marcar, buscar no leídos y destacados, guardar adjuntos, responder citando, reenviar con adjuntos, borradores (guardar, sustituir y enviar), crear, renombrar y borrar carpetas, mover, papelera, borrado definitivo y las protecciones.

## Trampas conocidas

- **PowerShell 7:** el PowerShell clásico lanzado desde PowerShell 7 hereda su `PSModulePath` y no carga `ConvertTo-SecureString`. La versión 1 dejó de descifrar la contraseña por eso. Ahora se lanza sin esa variable y se usa .NET (`ProtectedData`) directamente.
- **Contraseña mal guardada:** una contraseña guardada mal (de 1 carácter) solo da «fallo de conexión». Compruébalo con `--probar-clave`, que enseña la longitud y una huella, nunca la clave.
- **Correos a uno mismo en el spam:** en la prueba, los correos enviados a uno mismo acabaron en Junk aunque el servidor los daba por buenos («X-Spam-Status: No») y van firmados con la DKIM de agoin.es. Los movía allí el filtro de correo no deseado de un programa conectado al buzón.
- **Nombre con el que se presenta:** sin nombre de equipo, el envío se presentaba como «[127.0.0.1]», que algunos filtros penalizan. Ahora usa el nombre del equipo, como Outlook.
