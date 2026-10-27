---
name: acotar-planos
description: Cómo acotar plantas de arquitectura de forma limpia y normalizada (cadenas exteriores por fachada, ejes junto a las burbujas, luces libres interiores, sin cifras superpuestas), y cómo hacerlo en Revit por API/Dynamo con referencias al modelo. Usar cuando se pida acotar o reacotar una planta, revisar un plano de acotación "sucio" o con cotas superpuestas, o preparar una hoja de cotas tipo proyecto de ejecución.
---

# Acotar plantas de arquitectura

Fuentes: AIA, *The lost art of dimensioning*; práctica de la UNE-EN ISO 129-1 (representación de cotas). La meta es que
cada medida se lea una vez, sin buscarla y sin ambigüedad: menos cadenas, mejor ordenadas.

## 1. Reglas de dibujo (valen para cualquier programa)

**Qué se acota**
- Cada medida una sola vez. Nada que se deduzca de otras cotas de la misma cadena.
- Cadenas abiertas: la suma de los tramos la da la cadena total, no una cifra más.
- Las cadenas empiezan y acaban en ejes o en caras de muro acabadas, nunca en puntos sueltos.
- Cifras redondas al cm. Un tramo de menos de 10 cm que sale de capas de muro o de quiebros mínimos no es arquitectura: se quita.

**Exterior: por fachada, tres cadenas de dentro afuera**
1. **Huecos y machones**: esquinas y quiebros de la fachada y las jambas de cada hueco cortado por el plano de la planta.
2. **Total** de la fachada.
3. **Ejes**: no se repiten fachada a fachada. Va una cadena por cada familia de ejes paralelos, **junto a las burbujas**, fuera de todo el edificio. Las burbujas van más allá de la última cadena.
- La fachada de menos de 1,5 m, o sin huecos ni quiebros, lleva solo el total, o nada si otra cadena ya lo mide.
- Si una cadena cruza el edificio o otra cadena, se quita la de la fachada más corta.

**Interior**
- Luz libre de cada estancia en sus dos direcciones principales, "en cruz" (las dos líneas de la misma estancia pueden cruzarse entre sí y con nada más).
- A unos 0,6 m del muro, donde la medida se repite (la luz modal), no en un rincón atípico.
- No se acotan las escaleras (tienen su propio detalle) ni los huecos de menos de 0,8 m².

**Separaciones en papel** (a 1:100: 1 mm = 0,10 m)
- Primera cadena a 4,5 mm de la cara más saliente de la fachada; entre cadenas, 3,5 mm (2,5 mm libres entre cifras de 1 mm).
- Líneas de referencia de largo fijo (2,4 mm), separadas 0,75 mm del elemento.
- Cifras a 0,6 mm sobre la línea, con fondo opaco.

**Limpieza: lo que hace un plano "sucio"**
- Ninguna cifra toca otra línea, otra cifra, una etiqueta, una cota de nivel, un símbolo ni el título de la vista.
- La cifra que no cabe en su tramo se pasa al otro lado de la línea, alternando con la vecina, sin directriz. Mide el ancho real: dígito ≈ 0,8 × altura de texto, punto ≈ 0,4.
- Si una anotación (cota de nivel, rótulo de espacio, pendiente) pisa una cadena exterior, se mueve la anotación lo mínimo, con su símbolo. La cadena no se mueve, porque su posición la fija la regla.
- Dos burbujas de ejes casi coincidentes (ejes a pocos cm) se separan con un codo: la segunda, un diámetro hacia fuera.
- El mismo separador decimal en toda la hoja.

**Cuando el modelo no da caras paralelas** (muros de piedra irregulares, cubiertas)
- Se reproducen las cadenas del proyecto de referencia (PE) en su sitio, como cotas nativas con referencias auxiliares.
- Donde no hay nada que medir, se quedan como dibujo estático.
- No se añaden cadenas de fachada que el PE no tiene.

## 2. Comprobación antes de dar el plano por bueno

1. Exportar la hoja a PDF y mirar cada planta ampliada (≥ 200 ppp), no solo la vista general.
2. Recorrer: esquinas de las cadenas, extremos con tramos pequeños, burbujas, cotas de nivel, título de la vista.
3. Compararla con el plano de referencia: las mismas cadenas de ejes con las mismas cifras en todas las plantas.
4. Si se movió un recorte, comprobar en el PDF que el dibujo no se ha desplazado en la hoja (comparar posiciones de textos fijos).

## 3. En Revit (API / Dynamo PythonNet3)

Flujo probado en ALFERECES. Scripts en `D:\ARQ\ALFERECES\TRABAJO_REVIT_PE2026\`:

| paso | script | qué hace |
|---|---|---|
| leer | `dynamo/36_acotar_consulta.py` | Muros cortados: caras laterales con normal y tramo. DirectShape como pseudo-muros de una cara. Huecos con sus referencias. Ejes con el extremo que lleva burbuja. Habitaciones. Anotaciones como obstáculos, incluidos los títulos dibujados en la hoja (hoja→modelo: centro de la ventana = centro del recorte × escala). Cubiertas, recorte. |
| planificar | `scripts/planificar_cotas.py` | Aplica las reglas del apartado 1 y deja `dynamo/cotas_plan_<planta>.json` y una vista previa PNG. |
| crear | `dynamo/37_acotar_crear.py` | Borra la acotación anterior. Aparta anotaciones. Alarga ejes. Crea cada cota en su transacción. Escalona las cifras pequeñas. |
| todo junto | `scripts/acotar.py PLANTA ...` | Consulta, planifica, crea y guarda los ids en `dynamo/anot_ids.json`. |
| codos | `dynamo/38_ejes_codo.py` | Burbujas superpuestas. |
| recorte | `dynamo/40_recorte_ampliar.py` | Sitio para burbujas sin mover el dibujo en la hoja. |

**Referencias de cota: lo que hace que Revit no la rechace**
- Todas las referencias deben ser **exactamente** perpendiculares a la línea de cota (`|n·d| = 1` con tolerancia 1e-9). Si no, Revit la acepta y luego muestra "las referencias han dejado de ser paralelas" y bloquea la transacción.
- Cara de muro: `HostObjectUtils.GetSideFaces`.
- Hueco: `FamilyInstanceReferenceType.Left/Right`, solo si `HandOrientation` es paralela a la cota.
- Eje: `Reference(grid)`, solo si es perpendicular.
- En los demás casos, una línea de detalle invisible de 0,2 m perpendicular a la cota en ese punto (referencia auxiliar).
- `doc.Regenerate()` dentro de la misma transacción, justo tras `NewDimension`. Así el fallo salta ahí y se reintenta con auxiliares.
- Cada transacción con un `IFailuresPreprocessor` que borra avisos y hace `ProceedWithRollBack` en errores. Nunca aceptar a mano un diálogo de aviso con una transacción de API abierta: Revit puede cerrarse sin recuperación.

**Cifras y tipos**
- `DimensionSegment.TextPosition` es el punto inferior-central de la cifra, a "Desfase de texto" de la línea. Para pasarla al otro lado: `origen − n·(desfase + altura + 0,015 m)`.
- En el tipo de cota: "Mostrar directriz al desplazarse el texto" = *Más allá de líneas de referencia*, para que no salgan directrices al escalonar. Fondo de texto opaco (`DIM_TEXT_BACKGROUND = 0`).

**Ejes**
- Alargar en la vista: `SetCurveInView(DatumExtentType.ViewSpecific, ...)` con el punto proyectado sobre la propia línea del eje.
- Codo: `AddLeader(end, view)`. `Anchor` (la burbuja) es de solo lectura y sigue el desfase del `Elbow`, con un desplazamiento propio de Revit. Se fija el codo, se lee dónde quedó la burbuja y se corrige hasta que esté a un diámetro.
- `End` debe quedar sobre la línea del eje y más allá del codo.

**Recorte**
- Cambiar `CropBox` de una vista ya colocada no mueve el dibujo en la hoja: Revit mantiene la posición del modelo.

**Cosas que conviene saber**
- Una planta de cubierta no corta muros, así que la huella sale vacía: usa el conjunto de todas las plantas más el contorno de las cubiertas.
- Las cifras de cotas estáticas del PE ("0,24") son textos unidos a sus líneas: no se mueven sueltas.
- Antes de borrar "lo anterior", distingue por lote del registro de ids qué es copia estática redundante y qué es dibujo del PE sin equivalente en el modelo.
