---
name: web-proyecto
description: "Cómo montar, publicar y mantener la web o visor de un proyecto para la promotora y las constructoras (modelo 3D enlazado a las partidas, planos, descargas PDF/DWG/IFC/BC3/Excel, imágenes) sin filtrar lo interno. Cubre qué es público y qué no, una interfaz clara que no pierde al usuario, caché por versión, pruebas en vivo, Docker con túnel de Cloudflare y el diagnóstico cuando «no carga». Úsala al crear, actualizar, desplegar o depurar la web de un proyecto o un visor 3D de mediciones."
---

# Web del proyecto

## Qué se publica

- **Hay dos versiones de la web.**
  - **Pública, para las constructoras:** mediciones ciegas, sin precios, sin la comparación entre modelo y presupuesto y sin notas internas.
  - **Interna:** con precios, desviaciones y notas de revisión. No sale del equipo, salvo que el usuario diga otra cosa.
- **Al montar la web, comprueba con aserciones que en la pública no hay:**
  - precios;
  - la comparación entre modelo y presupuesto;
  - documentos con precios. Por ejemplo, la memoria completa incluye el presupuesto: se publica una copia sin ese capítulo y con un anejo de cambios.
- **Antes de publicar, compara entre sí los documentos que se descargan:** pliego, mediciones y anejo.
- **Publica solo cuando el usuario lo pida.**
  - Si no te ha dado la orden de publicar, enséñale antes lo que vas a subir.
  - Los planos o vídeos que no ha aprobado no se suben; se mantienen los anteriores.
- **Imágenes:** si el usuario deja sus propias imágenes en una carpeta para ese fin, se usan solo esas.

## Interfaz: lo que pidió el usuario en ALFERECES

Son buenos puntos de partida para otros proyectos; si el usuario pide otra cosa, manda lo que pida.

- **Tema claro.** Con el oscuro se perdía.
- **Que siempre se sepa qué se está viendo:**
  - cabecera fija «Estás viendo»;
  - botones de partida anterior y siguiente;
  - la fila pulsada no se mueve de su sitio en la pantalla: se despliega debajo.
- **Búsqueda y navegación:**
  - buscador por texto entre todas las partidas;
  - al pulsar un elemento del 3D, se abre su partida.
- **Descargas fáciles de encontrar,** con entrada propia en el menú: PDF, DWG, IFC, Excel y BC3.
- **Cada partida explicada:**
  - una imagen y una frase llana de qué es, como hace el Arquímedes de CYPE;
  - si se mide por longitud, superficie o volumen, cada componente aparece con su medida;
  - herramientas sencillas para medir distancia, área y volumen.
- **Logotipo:** un dibujo sencillo de la fachada del edificio.
- **Evita el aspecto de «hecho con IA»:** demasiadas cajas y tarjetas, tipografías de moda, numeraciones decorativas.

## Desplegar sin sorpresas

- **Pon la versión en las URL de los scripts y los datos** (`app.js?v=…`), y haz que todas las peticiones pasen por una función que la añada. La caché del CDN mezcló un modelo viejo con datos nuevos.
- **El servidor en vivo puede tener una CSP** (`script-src 'self'`) que el local no tiene. Nada de `<script>` en línea.
- **Después de desplegar:**
  - prueba la URL pública con un navegador automatizado y lee los errores de consola;
  - mira las miniaturas generadas en una hoja de contactos, no solo el resultado de los tests;
  - justo tras desplegar, el primer archivo grande puede tardar (caché fría): vuelve a medir antes de buscar un fallo.
- **Docker y túnel de Cloudflare:**
  - el token del túnel va solo en `.env`; nunca se imprime ni se sube al repositorio;
  - comprueba con qué cuenta de Cloudflare se creó el túnel: uno de otra cuenta da error 1033;
  - no toques otros proyectos de Docker del equipo ni puertos ya usados; pregunta cuáles están libres.
- **No subas documentos del proyecto a servicios de alojamiento externos** sin que el usuario lo pida.

## «No carga en la oficina»

- **Antes de culpar al servidor o al túnel,** mira quién firma el certificado que ve ese equipo (prueba con SslStream en PowerShell).
- **Un antivirus con filtro HTTPS (por ejemplo, ESET)** retiene las descargas grandes mientras las analiza.
  - La solución es una exclusión que hace el usuario o su informático.
  - Tú no toques el antivirus.
