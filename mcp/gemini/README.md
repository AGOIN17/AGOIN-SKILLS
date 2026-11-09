# MCP «gemini»

Maneja la **app de Gemini para Windows** desde Claude Code. Sirve para escribirle mensajes y, sobre todo, para convertir vistas 3D de Revit o del visor en imágenes fotorrealistas.

- **Sin API ni clave:** maneja la ventana por accesibilidad de Windows (UI Automation), con la cuenta y la suscripción de quien lo usa.
- **Sin molestar:** no mueve el ratón ni quita el foco.

Cuándo y cómo usarlo lo explica la skill [`gemini-imagenes`](../../skills/gemini-imagenes/SKILL.md).

## Requisitos

1. **Windows** con la app de Gemini instalada (`%LOCALAPPDATA%\Google\Gemini\Gemini.exe`) y la sesión de Google iniciada.
2. **Python 3** en el `PATH` (el comando `python`). Instala las librerías:

   ```
   python -m pip install -r requirements.txt
   ```

## Instalación

- **Con el plugin `agoin`:** se registra solo. Aparece en `/mcp` como `plugin:agoin:gemini`.
- **A mano** (si copiaste las skills sueltas):

  ```
  claude mcp add gemini --scope user -- python <ruta-del-repo>/mcp/gemini/server.py
  ```

Usa solo una de las dos formas: con las dos, habría dos servidores manejando la misma ventana.

## Herramientas

| Herramienta | Qué hace |
|---|---|
| `editar_imagen` | Borradores. Cada imagen va en su propio chat. Guarda `<nombre>_gemini.jpg` y su ficha `.json` (original, petición, dirección del chat) en `Descargas\Gemini`. Opciones: `instrucciones`, `modelo` (`flash` o `pro`), `temporal`, `carpeta_salida`, `esperar`. |
| `mejorar_en_pro` | Versión buena de un borrador: vuelve a su chat, pulsa «Redo with Pro» y guarda `<nombre>_gemini_pro.jpg`. Si el chat ya no existe, lo repite con Pro desde la original. |
| `estado` | Estado y resultado de los trabajos en cola (`esperar_s` para esperar). |
| `preguntar` | Manda un texto y devuelve la respuesta. |
| `leer_respuesta` | Lee la última respuesta del chat abierto. |
| `captura` | Imagen de la ventana, para ver en qué estado está. |

`editar_imagen` y `mejorar_en_pro` van en segundo plano por defecto: devuelven un número de trabajo y se consultan con `estado`.

## Cómo se comporta

- **Ventana minimizada:** trabaja «aparcada» (solo asoman 2 px en el borde izquierdo de la pantalla) y al acabar vuelve a quedar minimizada.
- **Ventana abierta:** trabaja a la vista. No uses la ventana de Gemini mientras trabaja.
- **Nunca sobrescribe:** si el nombre existe guarda `_2`, `_3`… y, si Windows pregunta por reemplazar, contesta «No».
- **Tiempos:** unos 45 s por borrador y unos 35 s por «Redo with Pro» (noviembre de 2026).
- **Idioma:** se probó con la interfaz de la app en inglés. Los nombres en español de los botones están puestos, pero sin probar. Si falla con la app en español, revisa las constantes `N_*` de `gemini_app.py`.
- **Cambios de la app:** si Google cambia la app, puede dejar de funcionar hasta que se ajusten esos nombres. Las trampas encontradas al montarlo están al principio de `gemini_app.py`.
