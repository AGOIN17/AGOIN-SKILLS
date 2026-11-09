---
name: gemini-imagenes
description: "[BLENDER · WINDOWS] Cómo convertir vistas 3D de Revit, capturas del visor o perspectivas del modelo en imágenes fotorrealistas con la app de Gemini para Windows del usuario, mediante el MCP «gemini» del plugin agoin: borradores rápidos con Flash, versión buena con «Redo with Pro», trabajo en segundo plano, criterios para que no cambie la geometría ni la cámara, sin personas, privacidad de las imágenes del cliente y comprobación con el original. Úsala cuando el usuario pida dar realismo a una vista, «pasarla por Gemini», un render con IA, mejorar una perspectiva o una axonometría, o escribirle algo a Gemini; también si las herramientas del MCP gemini fallan o no aparecen."
metadata:
  etiquetas: "BLENDER, WINDOWS"
---

# Imágenes fotorrealistas con Gemini

El MCP `gemini` (carpeta `mcp/gemini/` del repositorio) maneja la app de Gemini para Windows del usuario, con su cuenta y su plan.

- **Para qué:** dar realismo a una vista del modelo en un minuto, sin montar una escena de render.
- **El riesgo:** la IA cambia cosas (huecos, carpinterías, porches, entorno). Una imagen que no corresponde al modelo desacredita el proyecto.

## Antes de empezar

- **Comprueba que el MCP está:** herramientas `editar_imagen`, `mejorar_en_pro`, `estado`… (con el plugin se llaman `mcp__plugin_agoin_gemini__*`).
  - Si no aparecen o dicen que falta algo, sigue `mcp/gemini/README.md`: Python con `pywinauto`, `psutil` y `Pillow`, y la app de Gemini instalada y con sesión.
- **Mandar imágenes de un proyecto a Gemini es mandarlas a un tercero (Google).**
  - Hazlo solo si el usuario lo ha pedido para ese proyecto.
  - Si son imágenes de un cliente, propón `temporal: true`. Gemini avisa de que en los chats guardados puede haber revisores humanos; los chats temporales no quedan en el historial (comprobado).
  - Coste de `temporal`: no se puede volver a ese chat, así que `mejorar_en_pro` repite la imagen con Pro desde la original en lugar de usar «Redo with Pro».
- **Exporta la vista del modelo ya revisado** (`revision-modelo-bim`), a unos 2.000–2.500 px de ancho y con fondo limpio. Gemini copia también los errores.

## Flujo

1. **Borradores con Flash:** `editar_imagen` con una o varias imágenes; cada una va en su propio chat.
   - Por defecto va en segundo plano: devuelve un número de trabajo y se consulta con `estado(trabajo, esperar_s)`. Mientras, sigue con otra cosa.
   - En `instrucciones` van solo los detalles del proyecto (materiales, luz, estación, entorno). Los criterios fijos los pone el MCP.
   - Guarda `<nombre>_gemini.jpg` y una ficha `.json` en `Descargas\Gemini`.
2. **Enseña cada borrador al lado de su original** y deja que el usuario elija. Señala lo que haya cambiado.
3. **Versión buena con Pro:** `mejorar_en_pro` solo con los borradores elegidos. Vuelve al chat de cada uno, pulsa «Redo with Pro» y guarda `<nombre>_gemini_pro.jpg`.
   - Con la app en español no existe «Rehacer con Pro». Entonces el MCP repite la imagen con Pro desde la original y sale una imagen nueva, que puede alejarse del borrador. Díselo al usuario antes.
   - Pro gasta el cupo del plan del usuario: no lo uses para tantear.
   - En la prueba de noviembre de 2026, Pro dio **la misma resolución** que Flash (2572×1632), pero una imagen más limpia y fiel al modelo. No prometas más píxeles.
4. **Compara la imagen final con el original y con los planos** antes de enseñarla. Márcala como orientativa (regla de `video-render-arquitectura`).

## Criterios fijos (ya van en el MCP)

- **Misma cámara, encuadre y proyección; misma geometría; no añadir ni quitar elementos.** Sin estos criterios, Gemini pasó una axonometría a perspectiva, quitó un porche y se inventó el paisaje. Con ellos mantuvo todo.
- **Sin personas ni coches.** Es el gusto del estudio: el usuario rechazó las figuras humanas en los vídeos de ALFERECES.
- Si el usuario quiere otra cosa (otro punto de vista, un ambiente), usa `usar_criterios: false` y escribe la petición entera en `instrucciones`.

## Mientras trabaja

- **No toques la ventana de Gemini** ni le pidas al usuario que la use. Si estaba minimizada, el MCP la aparca casi fuera de la vista y al acabar la vuelve a minimizar.
- **No cierres ni mates la app de Gemini:** es la del usuario.
- **Si algo falla,** usa `captura` para ver el estado de la ventana antes de reintentar.
- **No sobrescribe nunca.** Si Windows pregunta por reemplazar un archivo, el MCP contesta «No».

## Trampas conocidas

- **Herramienta que no encuentra un botón** → la app ha cambiado o tiene un nombre que no está en las listas (inglés y español) → ejecuta `diagnostico` y ajusta los nombres `N_*` de `gemini_app.py`.
- **Dos sesiones de Claude con el MCP a la vez** → usan la ventana por turnos: la segunda espera, hasta 15 minutos, a que acabe la primera. No es un cuelgue.
- **El Gemini CLI ya no sirve con cuentas personales** (Google lo cerró en junio de 2026), y la API pide una clave de pago. Por eso el MCP maneja la app.
- **«Falta una librería de Python»** → `python -m pip install -r mcp/gemini/requirements.txt` y reabrir Claude Code.
