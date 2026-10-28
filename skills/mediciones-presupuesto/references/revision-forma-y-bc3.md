# Revisión automática de forma y trampas del BC3

## Revisión de forma tras cada regeneración

Un script que tarda segundos. Se pasa siempre después de regenerar mediciones, ciego y BC3. La primera vez sacó 103 incidencias. Comprueba que no haya:

- texto de relleno;
- partidas sin descripción o con una descripción muy corta;
- partidas sin el bloque «Medición»;
- códigos duplicados;
- capítulos desordenados o vacíos;
- partidas en un capítulo que no es el suyo;
- huecos de numeración que no expliquen un borrado registrado o el original;
- partidas sin precio (en la versión con precios) o con cantidad cero;
- unidades incoherentes;
- resúmenes repetidos;
- desgloses escritos en el texto que no suman la cantidad;
- palabras testigo de anotaciones internas en el ciego;
- precios en el ciego.

Esta revisión es de **forma**. «0 incidencias» no dice nada de si las mediciones están bien: dilo así al entregarla.

## Trampas del formato FIEBDC-3 (BC3)

- **Juego de caracteres.** Declara «ANSI» en el campo 5 del registro `~V`. Si va vacío, el estándar lo lee como 850 y se estropean tildes y eñes. Una auditoría externa lo encontró; el comprobador propio no, porque leía con la misma suposición que el generador.
- **Codificación del archivo.** Escribe en CP1252 con finales de línea CRLF.
  - Sin caracteres que CP1252 no tenga: superíndices, «≈». Escribe «1·10^-11»; Presto mostraba «1·10?¹¹».
- **Líneas de medición `~M`.** Una línea sin dimensiones lleva su valor en UNIDADES; si no, vale 1.
- **Convención de las líneas en el texto,** para que un script las lea: tras la palabra «Medición:», cada pieza con su valor separada por «;» y al final «Total». Emítelas en `~M` solo si suman la cantidad.
- **Prueba final:** importar en Presto y mirar una partida con tildes («cimentación») y su tabla de mediciones. Si no tienes Presto, pide al usuario que lo haga y dile exactamente qué mirar.
