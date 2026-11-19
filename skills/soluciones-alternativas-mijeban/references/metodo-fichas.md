# Fichas de soluciones alternativas: método

Una ficha por sistema constructivo (01 suelos, 02 fachada, 03 cubierta…), todas con la misma maqueta. La ficha enseña la solución del proyecto, las discrepancias en letra pequeña y, en grande, la solución propuesta. Se centra en el sistema, sin dibujar la sección completa ni sus encuentros.

## 1. Maqueta A4 vertical (aprobada por el usuario)

- **Cartela izquierda** de unos 60 mm, con fondo gris muy claro (#f2f2f1). De arriba abajo:
  - «MIJEBAN» y «SOLUCIONES ALTERNATIVAS»;
  - número grande de la ficha («02») y «SISTEMA ENVOLVENTE»;
  - nombre del sistema («Fachada»);
  - minilogo: sección esquemática del edificio con el sistema resaltado, el interior en blanco y sin rótulos;
  - la envolvente según la memoria (2.3.1 a 2.3.4), con el apartado de la ficha en negrita;
  - «La propuesta en cifras», cada cifra con su valor en el proyecto debajo;
  - sello PROPUESTA («Pendiente de la dirección facultativa y del cálculo estructural»);
  - «Notas sobre el proyecto»: discrepancias numeradas en letra pequeña, cada una con su fuente.
- **Cuerpo:**
  - antetítulo «FICHA 02 · FACHADA» con una raya verde;
  - titular técnico de dos líneas y el tipo debajo («TIPO TRASDOSADO CERÁMICO»);
  - entradilla de tres líneas;
  - axonometría con la leyenda numerada a la derecha;
  - banda de transmitancia: proyecto frente a propuesta, con barras a la misma escala («cuanto menor, mejor») y la diferencia en %;
  - nota de la U con sus fuentes;
  - columna de texto «El proyecto / La propuesta / Qué se gana»;
  - sección vertical numerada igual que la axonometría;
  - pie con la obra, la versión y las fuentes.
- **Un solo color de acento:** RGB 7,87,72 (#075748). Dibujos en escala de grises. Todo debe leerse impreso.
- **Textos:** todos en Century Gothic, estilos FICHA y FICHA NEGRITA. Texto mínimo de unos 1,6 mm en papel.
- **Pies de dibujo** sin escala («Axonometría del sistema», «Sección vertical · cotas en mm») y alineados con el borde del dibujo (la cara exterior del muro), no con la ventana.
- **Plantilla:** `assets/PLANTILLA FICHA A4.dwg`. Tiene la presentación «FICHA-A4» con la maqueta en espacio papel, ventanas bloqueadas a 1:10, zonas guía en el modelo que no se imprimen, el bloque FICHA_NUM con el atributo N, y una presentación «INSTRUCCIONES».
- **Trazado:** papel `ISO_full_bleed_A4_(210.00_x_297.00_MM)`, sin tabla de estilos de trazado. La configuración de página va guardada en el DWG.
- **Pie de página:** la última línea tiene que quedar a 3 mm o más del borde. En la ficha 02 B v3 quedaba a 0,5 mm y se subió.

## 2. Del DWG al DXF y vuelta, con accoreconsole (sin tocar el AutoCAD del usuario)

AutoCAD LT 2023 trae `accoreconsole.exe`, y funciona.

```
& 'C:\Program Files\Autodesk\AutoCAD LT 2023\accoreconsole.exe' /i "<entrada.dwg|.dxf>" /s "<guion.scr>"
```

- **Guion para sacar el DXF** de una copia del DWG:
  ```
  FILEDIA
  0
  _.DXFOUT
  "C:\ruta\x.dxf"
  16
  ```
- **Guion para volver a DWG y trazar a PDF**, abriendo el DXF que ha hecho ezdxf (ejemplo en `scripts/f8/p8.scr`):
  ```
  FILEDIA
  0
  _.SAVEAS
  2018
  "C:\ruta\x.dwg"
  _-PLOT
  _N
  FICHA-A4
  <línea vacía>
  <línea vacía>
  "C:\ruta\x.pdf"
  _N
  _Y
  ```
- **Trampas del guion:**
  - escríbelo en ASCII;
  - sin espacios en las rutas, o con comillas;
  - los comandos con `_.` delante, porque la interfaz está en español;
  - **lanza accoreconsole con la carpeta temporal como directorio de trabajo** (`Set-Location <scratchpad>`): escribe `plot.log` en el directorio actual, y en Cigarral dejó uno en la raíz del proyecto.
- **Comprobación al guardar en el proyecto:** compara el hash del archivo guardado con el generado.

## 3. Editar una ficha sin su generador

1. Saca el DXF de una copia y vuelca los textos de la presentación con su handle, posición, alto, ancho e interlineado (`scripts/f8/dump_ps.py`, `scripts/ps_dump.py`).
2. Cambia los MTEXT por handle con una función que compruebe que el texto viejo aparece **exactamente una vez**:
   ```python
   def cambia(h, viejo, nuevo):
       e = E[h]; assert e.text.count(viejo) == 1, (h, viejo, e.text); e.text = e.text.replace(viejo, nuevo)
   ```
   Para un texto o una viñeta nuevos, copia uno que ya exista: `ps.add_entity(E['41B'].copy())`.
3. **Mide los cortes de línea como AutoCAD:** `ezdxf.fonts.fonts.make_font('GOTHIC.TTF', alto).text_width(texto)`, con un reparto voraz de palabras. Reproduce los cortes de AutoCAD. El paso de línea es 1,667 · alto · interlineado.
4. **Recoloca leyendas y viñetas** según las líneas que ocupa cada texto (función `n_lineas` de `scripts/f8/ficha02_termo.py`). Después pasa una **comprobación de textos que se pisan**: la caja de cada MTEXT contra todas las demás. La generación se para si se solapan más de 0,3 mm². La comprobación salió porque una viñeta partió en dos líneas y pisó la siguiente.
5. **Espacio que no parte la línea** en un MTEXT: `\~` («DB-HS\~1», «100\~mm»), para que no quede «1.» o «mm» solos en otra línea.
6. Al final, busca que no quede ninguna palabra prohibida («tosco», «ALTERNATIVA», «233»…) en los textos de la presentación.
7. Mira el PDF como imagen, entero a 110 ppp y por zonas a 300–900 ppp, antes de darlo por bueno.

## 4. Axonometría 3D con caras ocultas (`scripts/f8/ficha02_termo.py`)

La axonometría no se puede corregir pieza a pieza: es una colección de sombreados planos ya recortados. Para cambiar una capa, **se rehace entera** desde un modelo 3D de cajas.

- **Proyección isométrica a 30°, sin reducción:** `P(X, Y, Z) = (OX + cos30·(X + Y), OY − 0,5·X + 0,5·Y + Z)`. X va a lo largo del muro (hacia abajo a la derecha), Y es el espesor de fuera adentro (hacia arriba a la derecha) y Z la altura.
- **Caras visibles:** frente (−Y, la cara exterior), arriba (+Z) y testa (+X, el corte del extremo).
- **Capas escalonadas:** cada capa interior asoma por arriba y por la derecha. Ejemplo de la ficha 02, en metros:

  | Capa | X1 | Z1 |
  |---|---|---|
  | Monocapa | 0,15 | 0,15 |
  | Bloque | 0,30 | 2 hiladas |
  | Enfoscado | 0,345 | 0,42 |
  | EPS | 0,40 | 0,46 |
  | Gran formato | 0,45 | 0,48 |
  | Yeso | 0,48 | 0,52 |

- **Regla de ocultación:** una capa más exterior (Y menor) tapa a las interiores, y nunca al revés. La razón: un punto delante de otro en la dirección de la vista tiene siempre una Y menor. Por eso, lo visible de cada cara es la cara menos la unión de las siluetas de las capas exteriores. No hace falta ordenar por profundidad.
- **Trabajar en el plano de cada cara y proyectar después** con transformaciones afines de shapely:
  ```python
  plano_Z = lambda g, Z: affinity.affine_transform(g, [C, C, -0.5, 0.5, OX, OY + Z])            # g en (X, Y)
  plano_X = lambda g, X: affinity.affine_transform(g, [C, 0, 0.5, 1, OX + C * X, OY - 0.5 * X])  # g en (Y, Z)
  plano_Y = lambda g, Y: affinity.affine_transform(g, [C, 0, -0.5, 1, OX + C * Y, OY + 0.5 * Y]) # g en (X, Z)
  ```
- **Huecos en tres tonos** («claro junto al borde, más oscuro al fondo»). La pared que se ve a una profundidad d es la boca del hueco menos esa misma boca desplazada d en pantalla. Se usa la función `bandas(vis, lleno, vec, cortes)`:
  - huecos verticales vistos desde arriba: vec = (0, −1);
  - huecos a lo largo de X vistos en la testa: vec = (−cos30, 0,5).
- **Colores:**

  | Elemento | Tonos (gris RGB) |
  |---|---|
  | Yeso (frente / arriba / testa) | 246 / 236 / 226 |
  | Enfoscado (frente / arriba / testa) | 208 / 192 / 180 |
  | Monocapa (frente / arriba / testa) | 200 / 184 / 170 |
  | EPS | blanco con trama HONEY a escala 0,0025, gris 165 |
  | Monocapa, trama del frente | AR-SAND 0,004, gris 150 |
  | Piezas cerámicas: tabla de arriba | 208 |
  | Piezas cerámicas: cara exterior | 192, con estrías verticales en gris 150 |
  | Piezas cerámicas: corte | 178 |
  | Huecos de las piezas, de arriba | 198 / 184 / 170 |
  | Huecos de las piezas, franjas del corte | 162 / 175 / 190 |
  | Juntas | 238 |

  Las aristas, en negro.
- **Tramas con patrón:** copia una trama que ya exista (`E['308'].copy()`), vacía sus contornos y pon los nuevos. No uses los patrones de ezdxf: en metros salen a otra escala.
- **Números:** directrices paralelas a 20°, círculo verde de radio 0,0185 m con la cifra blanca (estilo «1-10 NEGRITA», alto 0,02), punto en la capa y codo antes del círculo. Los círculos van en columna a la derecha, a 0,05 m de distancia, numerados de dentro (1) a fuera. El punto se busca solo, sobre la línea a 20° que sale del codo, dentro de la cara visible de su capa encogida 6 mm (`punto_en`).
- **Ventana:** si el dibujo crece, se alarga la ventana hacia abajo manteniendo 1:10 y el borde izquierdo (x del modelo 0 = cara exterior), y se comprueba que no pisa el pie.

## 5. Sección vertical

- Copia los atributos de las entidades que ya existen (`.copy()` de la trama ANSI31 0,003 gris 175, de las líneas de hueco y de las juntas) antes de borrarlas.
- **Piezas con perforación vertical:** cada hilada es una trama con islas en los tramos de hueco que corta el plano (función `intervalos(u)`), más una línea en cada borde de hueco. Las hiladas alternas se cortan a media pieza de distancia.
- **Mover capas:** si una capa engorda, se trasladan `+dx` todas las entidades a su derecha. Las líneas de rotura solo alargan su último punto.
- **Cotas:** son bloques anónimos (`*Dn`) con líneas, trazos `_OBLIQUE` y un MTEXT.
  - Mueve los puntos del bloque y los `defpoint` de la cota que caen a la derecha del cambio.
  - Cambia el texto del MTEXT y el atributo `actual_measurement`.
  - Comprueba al final que la lista de cotas es la esperada.
- **Aislante en sección:** «bucles», semicírculos alternos de radio 1/6 del espesor unidos en diagonal, en azul (ACI 5) o en gris.
- **Forjado unidireccional:** se corta en perpendicular a las viguetas, con la capa de compresión continua y un nervio con su vigueta visibles. Si se corta solo por una bovedilla, parecen «dos forjados».

## 6. Piezas ya dibujadas (Cerámica Millas, declaraciones de prestaciones en `REFERENCIAS\` de Cigarral)

| Pieza | Medidas | Grupo | λ | Cómo se dibuja |
|---|---|---|---|---|
| Cerámico tosco de 10 | 233 × 106 × 96 | G2, fb 10, P/F0 | 0,30 (fábrica con juntas, R 0,49) | A tizón y trabado. 3 filas de óvalos al tresbolillo: 6 en las de los lados; en la central, 5 más 2 medios huecos en «D» |
| Gran formato 70 × 50 × 7 | real 656 × 506 × 67 | — | 0,29 (R con juntas 0,21) | 2 × 9 huecos horizontales, machihembrado arriba y abajo |
| **Termocerec 24** (termoarcilla) | 295 × 189,6 × 236 | G3, fb 10, cat. II | 0,28 | Ver abajo |

**Dibujo del Termocerec 24.** La declaración no da la forma interior, así que se tomó de la foto del usuario:
- 6 columnas de 13,5 mm en espiga de 5 mm, con tabiquillos de 8 mm;
- 2 huecos de agarre;
- tabiquillos exteriores de 12 mm;
- machihembrado de 8 mm con 5 machos, cada uno con su taladro, y módulo de 287 mm entre llagas;
- junta fina de 1 mm: la declaración dice «con junta fina de mortero», pero no da el espesor;
- llagas sin mortero.

**Transmitancia del muro.** Se calcula por caminos en paralelo, pieza más mortero (λ 1,30), como en el CTE. Superficies: Rse 0,04 y Rsi 0,13. λ de las capas: monocapa y enfoscado 1,30; yeso 0,57; EPS blanco 0,036 (y 0,038 como caso desfavorable).

## 7. Antes de dar la ficha por buena

- Que la leyenda, la axonometría y la sección numeren las capas igual.
- Que las cifras de la cartela, de la leyenda y de las cotas coincidan, todas sacadas de las mismas variables del script.
- Que no se pisen los textos (comprobación automática) y que no quede ninguna palabra prohibida.
- Que el PDF trazado por AutoCAD se haya mirado como imagen: la página entera y las zonas ampliadas.
