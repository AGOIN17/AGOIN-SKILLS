# Libro de estilo de AGOIN (LdE V5) y plantilla AG-PLA-V8: resumen para producir planos

Resumen práctico para maquetar, nombrar y revisar planos en Revit «a la AGOIN». Se hizo leyendo, página a página:

- **[LdE p.N]**: «Manual de Producción de Proyectos BIM – Libro de Estilo» (`AGOIN-LdE-V5.pdf`), Rev. 05, 15/01/2022, 102 páginas. El anexo 11.1 (p.94) está vacío, con el sello «[EN DESARROLLO]».
- **[Plantilla]**: la plantilla de Revit `AG-PLA-V8-ARQ` (hoja de arranque «AG00 PORTADA/GUARDAR AQUÍ», hojas REV.01-03 y sus filtros).
- **[Leyenda X]**: las 19 leyendas de la plantilla, vistas como imagen.
- **[Cajetín]**: el cuadro de rotulación, medido en milímetros sobre una exportación.
- **[RLA]**: la plantilla de otro estudio. Solo sirve como referencia de buenas prácticas; **no se adopta su nomenclatura**: el estudio eligió la de la v8 (14/10/2026).
- Lo que **no** viene de las fuentes va marcado como **(recomendación)**.
- Los originales (PDF del libro, plantilla `.rte`, `AGOIN_Parámetros compartidos.txt`, `AGOIN_Nota clave_por elemento.txt`) los guarda el estudio; en CHIVERO estaban en `D:\ARQ\Chivero\maquetacion revit`. No los modifiques: trabaja con copias.

> Idea general del libro: el plano sale del modelo («Todos los cambios del modelo deben llevarse a cabo en 3D en lugar de utilizar documentos 2D insertados», p.67), con tipos bien nombrados, *Marca de tipo* como código del plano y leyendas o tablas que explican esos códigos en la misma hoja.

---

## 1. Memoria de muros y catálogo de elementos constructivos

### 1.1 Nombre de los tipos de familias de sistema (muros, suelos, techos y cubiertas) [LdE p.41-42]

Formato: `<CLASE>-<descripción corta (núcleo)>-<dato1-dato2-dato3 opcionales>-(<capas ext.>//<capas int.>)=<grosor total>cm`

- Ejemplo completo del libro (con los campos numerados): `1FCH-2BH20+3tras-hmax=6m-EI90-(41.5apla+1.5enfo5//67aisl+1.5pyla)= 731.5cm`.
- Otros ejemplos del libro: `FCH-Bloque 20 DC-(2.3apla+5.4aisl//2.3alic)=30cm` · `GEN-30cm` · `ACA-Laminado Porcelanosa-(1 made/10rell)=11cm` · `ACA-Enl Yeso=1.5cm`.
- Reglas, punto por punto:
  1. Clase de 3 letras. Si el elemento es genérico, solo `GEN` y el grosor.
  2. Descripción corta, normalmente del núcleo.
  3. Hasta 3 datos relevantes (hmax, EI, dB), y solo cuando son determinantes.
  4. Capas de la cara exterior al núcleo, cada una con su grosor y una abreviatura de 3 letras, unidas con `+`.
  5. `//` separa el acabado exterior del interior; solo se usa en elementos completos exterior-interior.
  6. Capas del núcleo a la cara interior.
  7. `=` y el grosor total en **cm**. Si el muro tiene una sola capa, se salta del punto 3 al 7.
- NOTA 1: elementos genéricos `GEN-grosor`. NOTA 2: en muros cortina, solo una descripción más detallada. NOTA 3 (hoja de arranque de la plantilla): en suelos, techos y cubiertas se dice «superior/inferior» en lugar de «exterior/interior».
- Códigos de clase. TABLA 16 [LdE p.41-42]: `INT` interior · `EXT` exterior · `CON` contención · `FCH` fachadas · `ACA` acabado · `PIL` revestimiento de pilares · `PIS` piscinas · `ALB` albañilería · `CIM` · `CUB` · `FOR` forjados · `HOR` hormigón · `PYL` tabique de PYL · `BTM` bloque de termoarcilla · `BHM` bloque de hormigón · `LAD` ladrillo · `PET` peto. La hoja de arranque de la plantilla añade `TRAS` trasdosados y la v8 usa además `TAB` tabiques, `SMC` muro cortina y `TEC` techos. Se pueden crear clases nuevas «siempre que sigan el criterio» (de ahí `EXI-` en CHIVERO).
- Tipos reales de la v8 que sirven de modelo: `FCH-1/2pie-(1.5mono+12lad hueco+4aisl+7lad+1.5yeso)=26cm` · `FCH-BTM+SATE-(1aca+1mort+12aisl+19bloq arcilla+1mort)=34cm` · `INT-PYL-(1.5placa yeso+7aisl+1.5placa yeso)=10cm` · `TAB-(1.5yeso+7lad hueco+1.5yeso)=10cm` · `TRAS-(4cám+7lad hueco+1.5yeso)=12.5cm` · `CON-25HA+imp=25cm` · `PET-SATE-(1aca+1mort+6aisl+12lad perf+1aca)=21cm`. Suelos: `ACA-gres porcelánico imitacion madera-(2gres+1mor+7rad+10EPS)=20cm`, `FOR-vig=simple-autoport-(25bov+5neg)=30cm`, `FOR-solera=15cm`. Cubiertas: `CUB-inv-(10grav+12aisl+2mor+15h.pend)=39cm`. Techos: `TEC-2cm`. Hay un tipo `NO USAR` como tipo por defecto.
- Componentes (familias cargables) [LdE p.41]: `<Categoría>-<Descriptor1>-<Descriptor2>` con nombres reales de catálogo, por ejemplo `ASA-Ducha-Concetto System.rfa`. Tipo: `<Dimensiones>-<descriptor>`, por ejemplo `1200x800x2200mm`. Los códigos de categoría están en la TABLA 13 [p.39-40]: `PUE` puertas, `VEN` ventanas, `MUR`, `SAC` suelos de acabado, `TEC`, `ASA` aparatos sanitarios, `MOB`, `BAR`, `LUM`, `TUB`, `CON` conductos, `EQE`, `EMC`, `AEL`, `DAI`… En la v8: `PUE-1 hoja : 82x203 cm`, `VEN-2 hojas-Abatible : 150x150 cm`.
- Materiales [LdE p.46-47]: `AG_<tipo>`. Pueden ser genéricos (`AG_Aire`, `AG_Hormigón`) o comerciales, con la descripción exacta del fabricante o de la partida: `AG_Placa de Yeso Laminado - Knauf - Tipo H1`, `AG_Aplacado gres porcelánico 75X150 cm, Keraben Urban Grafito`. Al duplicar un material hay que duplicar también el activo Aspecto (p.64).

### 1.2 Parámetros que tiene que llevar cada tipo [LdE p.36, 60]

| Parámetro | Uso en plano |
|---|---|
| **Marca de tipo*** | Código del plano, el que lee la etiqueta: «una letra seguida de dos números» → `M01`, `S01`… (p.64-65) |
| **Comentarios de tipo*** | Clase del elemento según 7.3.2: `FCH`, `INT`, `FOR`… (p.36, captura p.60 con `FCH` y `M01`). La v8 pone ahí `C`, `H` o `M`, lo que no es coherente con el libro. |
| Código de montaje | Partida del presupuesto (Cost-it / Presto) |
| Resistencia acústica (dBA) | CTE DB HR |
| Clasificación para incendios | Texto, CTE DB SI (EI…) |
| **Función** del tipo | Solo «exterior», «interior» o «de retención». Los medianeros son exteriores (p.60). |
| Función de cada capa | Estructura, sustrato, acabado 1/2, aislamiento, membrana: es lo que resuelve los encuentros solos (p.60) |
| Nota clave | En la v8 casi todos los muros llevan `Md.1` («Muro por defecto – 30 cm» del archivo `AGOIN_Nota clave_por elemento.txt`): es un valor de relleno, no se debe mostrar. |

Los parámetros marcados con * son obligatorios. Tablas que los leen: `+00-Tabla de elementos` (Categoría, Familia, Tipo, Marca de tipo, Comentarios de tipo, Código de montaje, Descripción de montaje, Nota clave, Descripción, Recuento) [Plantilla].

### 1.3 Etiquetado del catálogo en planta [LdE p.64-66, Leyenda ARQ-ETIQUETA CALIDADES Y ACABADOS]

| Elemento | Familia : tipo [Plantilla] | Aspecto | Parámetro |
|---|---|---|---|
| Muros (tabiques, cerramientos, contención) | `ET-Etiqueta de muro : 1.5mm / 2mm` | `Mxx` dentro de un **rectángulo** | Marca de tipo |
| Suelos (acabado o forjado) | `ET-Etiqueta de suelo : 1.5mm / 2mm` | `Sxx` dentro de un **triángulo** con el vértice hacia arriba | Marca de tipo |
| Acabados de la estancia | `ET-Etiqueta de habitación-Acabados general : General` (más las variantes `-Acabado suelo : Suelos` y `-Acabado techo : Techos`) | Recuadro **rojo**: `SXX` arriba, `AXX` y `TEXX` abajo; las llamadas dicen «Acabado Suelo / Acabado Muros / Acabado Techo» | Parámetros de habitación Acabado del suelo, del muro y del techo |
| Nombre y superficie | `ET-Etiqueta de habitación : Nombre / Nombre+Superficie` | «Nombre / 150 m2» | — |
| Áreas | `ET-Etiqueta de área : Nombre / Nombre+Superficie` | ídem | — |
| Material (control) | `ET-Etiqueta de material : Descripción / Grupo / Nombre (sólo para check)` | — | — |

- Prefijos del catálogo [LdE p.66]: **S** suelos · **M** muros · **A** acabados de paramento · **TE** techos. Ejemplos literales: «S01 – Gres porcelánico antideslizante – Imitación madera / M01 – Muro de bloque cerámico / A01 – Enlucido de yeso / TE01 – Techo de Placa de escayola».
- Si una estancia no tiene alguno de los elementos (un patio solo con suelo), los demás campos se dejan **en blanco** (p.66).
- Para rellenar los acabados se recomienda «encarecidamente» la tabla de claves `C-Acabados de habitación`, que en la v8 se llama `TC-Acabados de habitación` y tiene los campos Nombre de la clave, Acabado del suelo, Acabado de muro, Acabado del techo y Altura de techo (p.65).

### 1.4 Leyendas del catálogo [LdE p.66, Leyendas]

- «Existirá una leyenda global, dentro de la plantilla de proyecto de arquitectura, que contendrá el total de elementos de acabado/suelos/muros/techos que se hayan empleado en cualquier proyecto». En cada proyecto se borran los que no aparecen, pero **«no se recodificarán los elementos restantes»**: el código es fijo (p.66).
- Las leyendas se nombran `PREFIJO DE 3 LETRAS POR DISCIPLINA-DESCRIPCIÓN`, por ejemplo `ARQ-CALIDADES DE SUELO` (p.44, 49).
- Las leyendas de la v8 que tocan este punto (todas a 1:50, solo con textos y regiones o líneas, sin componentes de leyenda):
  - **ARQ-ACABADOS**: dos bloques en mayúsculas gris negrita, «ACABADO PARAMENTOS HORIZONTALES» (subtítulos SUELOS y TECHOS) y «ACABADO PARAMENTOS VERTICALES». Debajo, el código y la descripción en gris. Suelos: `GP-01` gres porcelánico imitación madera, `GP-02` antideslizante interior, `GP-03` antideslizante exterior, `H-01` hormigón semipulido, `AJ` ajardinado. Techos: `P` enlucido de yeso con pintura, `FT` falso techo continuo Pladur. Paramentos verticales: código + **muestra de línea discontinua de color** + descripción: `AL` alicatado (cian), `EN` enfoscado (rojo), `MC` monocapa (violeta), `Y` enlucido de yeso (verde), `AP` aplacado de piedra (salmón), `MA` listones o panelado de madera (marrón), `AC` acero cor-ten (gris oscuro), `MO` mortero acrílico (verde claro). Estas líneas son los estilos `ACA-Acabado …` de la plantilla (§5.5): el acabado del muro se dibuja como línea discontinua de color pegada a la cara del paramento.
  - **ARQ-CALIDADES** («CALIDADES DE SUELO»): muestras de color en columna (regiones rellenas `Región rellenada : GP-01_GRES PORCELÁNICO IMITACIÓN MADERA`, etc.) con `AC-01, LC-01, MT-01..03, C-01, GP-01..04, GR-01, GV-01, H-01..03, MA-01, TV-01`. Nota al pie: «TODAS ESTAS CALIDADES SE REFIEREN AL DOCUMENTO MEMORIA DE CALIDADES Y SE REVISARÁN POR LA D.F.»
  - **ARQ-ETIQUETA CALIDADES Y ACABADOS**: explica la etiqueta Sxx/Axx/TExx (§1.3).
  - **ARQ-ALTURA DE TECHOS** («ALTURAS DE TECHOS (m)»): muestras pastel `2.03 m / HUECO DE PASO`, `2.10` … `3.00 m` cada 10 cm, `VARIABLE` y `FORJADO PLANTA SUPERIOR` (gris). Va con la plantilla de vista `ARQ_ALTURAS DE TECHO` (filtros de color `TEC-ALTURA 2.10m…3.00m`, `TEC-SUE ALTURA …`, `PUE-Hueco 2.03m…2.50m`) y con los tipos de región `TEC-2.03 … TEC-3.00`, `TEC-FORJADO`, `TEC-FALSO TECHO-ESPACIO` y `ALTURA VARIABLE`.
- **Hay dos sistemas de códigos que conviven.** El texto del libro usa Sxx/Mxx/Axx/TExx. Las leyendas de la v8 usan GP-01/H-01/P/FT/AL… Hay que decidir uno por proyecto; CHIVERO ya eligió S01/A01/TE01, que es el del libro.
- El libro manda tener **vistas de Albañilería, Calidades y Altura de techos asociadas a los planos de plantas acotadas** (p.50).

### 1.5 Las capas del muro en planta y en sección

- **Regla del libro** (p.60):
  - En las vistas donde no deben verse las capas (sección general, plano de techos) se usa una modificación gráfica fijada en la plantilla de vista.
  - En las vistas donde sí deben verse (plano acotado, plano de mobiliario) no se modifica nada: los rellenos salen del material de cada capa.
  - En la práctica, las plantas de albañilería y de distribución muestran las capas con el patrón de corte de cada material `AG_…`, sin colores de filtro.
- **Estilos de objeto** (captura en p.62):
  - Muros: proyección 1, corte 2, negro; bordes comunes y líneas ocultas a 1.
  - Ventanas: todo negro a 1/1, salvo `Marco/montante` en RGB 192-192-192, que es la subcategoría donde se dibujan los barridos de apertura.
  - Puertas: sin subcategorías, todo RGB 0,0,0.
- **Plantillas de vista que lo resuelven** [Plantilla]:
  - `ARQ_ALBAÑILERÍA` (planta, 1:100, Fino, sin filtros).
  - `ARQ_PLANTAS ACOTADAS` (1:50, Fino; oculta `ASA-Aparatos-Tomas`).
  - `ARQ_PLANTAS GENERALES + DISTRIBUCIÓN` (1:100, Fino).
  - `ARQ_DETALLES EN PLANTA` (Fino).
  - `ARQ_SECCIONES ACOTADAS` y `ARQ_SECCIONES CON SOMBRA` (1:100, Bajo, con filtros `SUE-Suelo estructura`, `SUE-Suelos NO estructura`, `CUB-Cubierta estructura` y `MUR-NO Estructura`, que son los que «aplanan» la sección general).
- **Ni el libro ni la plantilla tienen una leyenda que dibuje la composición de muros por capas.** El catálogo solo existe como texto (nombre del tipo y Mxx) y como etiqueta. La v8 tiene un «Plano de tablas» (REV.02) con `Muros - Descomposición` (Material: Nombre, Área, Volumen).
- **RLA sí la tiene**: una vista de planta `MEMORIA_COMPOSICIÓN_MUROS` a **1:20**, con trozos de cada tipo. Sus nombres de tipo listan las capas en mm con letra de material (`T_(PYL)_13(N)+70(C)+13(N)_96mm`), el parámetro *Descripción* lleva la familia (T, TR, MM, MF, ME) y la etiqueta `DESCRIPCION+MARCA_TIPO` lee, por ejemplo, «T08». En la leyenda de acabados de RLA hay la línea «* Ver tipos en memoria de composición de suelos».
- **Ficha de muro (recomendación**, combinando AGOIN y RLA). Es la «memoria de muros» que falta, para la columna de leyendas del plano de albañilería o para su propio plano 6.DET:
  - Un trozo de muro de cada tipo de ~60 cm, en planta a 1:20 (o un componente de leyenda «Muro» a nivel de detalle Fino).
  - Etiqueta `Mxx` encima y cota del grosor total.
  - A la derecha, el nombre del tipo y la lista de capas de exterior a interior: «1,5 cm enlucido de yeso / 7 cm ladrillo hueco doble / …», con material `AG_…` y grosor.
  - Al pie: Función (ext/int), EI y dBA si se conocen, U (W/m²K) en los de envolvente, y «Marca de tipo = Mxx».
  - Lo mismo para `Sxx` (sección vertical del paquete de suelo a 1:10 o 1:20), `TExx` y `Cxx`/cubiertas.

### 1.6 Reglas de modelado que se ven en los planos [LdE p.56-60]

- Tres niveles por planta, **NPT, NFS y NFI**, con vistas de planta y de techo solo en NPT. Nombre: `P00-NFS-Planta baja`, `E1-P01-NPT-Planta primera` (p.42-43, 56). Plantilla: `NFI - P0` −0,45 / `NFS - P0` −0,15 / `NPT - P0` 0,00.
- Suelo de acabado y forjado van por separado. El de acabado se refiere a NPT, bordea los muros interiores y **rellena los huecos de puerta**, para que no aparezcan líneas falsas en el paso. El forjado se refiere a NFS. En cubierta, forjado más paquete de cubierta, ambos en NFS (p.57-58).
- Los falsos techos van en NPT con desfase: «si se ajusta un desfase de 2,50 m desde NPT, la altura libre será, efectivamente, 2,50 m» (p.59).
- Muros por planta, no continuos (p.59-60):
  - Cerramiento: de NFS a NFI superior (de NFI a NFI en plantas intermedias).
  - Trasdosados y tabiquería: de NFS a NFI superior, unidos al suelo de acabado si llevan acabado.
  - Acabados: de NPT a NFI superior, o desconectados hasta el falso techo.
  - Contención: desde el NFS de cimentación.
  - Petos: de NFI a NCU.
- **Antes de cada emisión de planos**, rutinas de Dynamo Player que unen suelo con muro y muro con muro (p.59, 60).
- Sin pilares arquitectónicos: los cajeados se hacen con muros de acabado o de trasdosado (p.62, 75).

### 1.7 Incoherencias de la fuente (decidir y anotar en 00_PLAN)

- Grosores por capa: el texto dice «cm» en el punto 4 y «mm» en los puntos 5 y 6, pero todos los ejemplos están en cm con punto decimal. **Usar cm.**
- Clase «en minúsculas» (punto 1), pero todos los ejemplos van en mayúsculas. **Usar mayúsculas.**
- Comentarios de tipo: el libro pide la clase (FCH…) y la v8 pone C/H/M.
- Prefijo de las tablas de claves: «C» (p.46) frente a «TC-» (p.84 y v8). Tablas de trabajo: «TRA» (p.46) frente a «TR-» (p.84 y v8). **Usar TC- y TR-.**

---

## 2. Memoria de carpinterías: cuadro y leyenda de carpintería exterior, interior y cerrajería

### 2.1 Lo que fija el libro

- **Etiquetas** (p.65): `ET-Etiqueta de puerta.rfa` y `ET-Etiqueta de ventana.rfa`, con «una letra seguida de dos números».
  - **E** = carpintería exterior, en **rojo**; **I** = interior, en **verde**. El color sale del *tipo* de etiqueta.
  - Parámetro: **Marca de tipo**. «La etiqueta de puertas está configurada para que se muestre E, si es exterior, o bien I, si es interior, por lo que en el parámetro se colocará únicamente el Número correspondiente (01, 02, 03…)».
  - Las ventanas «se supondrán siempre exteriores… mostrándose siempre el prefijo E».
  - Tipos de la v8: `ET-Etiqueta de puerta : Exterior - Círculo grande / Exterior - Círculo pequeño / Interior - Círculo grande / Interior - Círculo pequeño`, `ET-Etiqueta de ventana : Círculo grande / Círculo pequeño`. Cerrajería: `ET-Etiqueta de cerrajería` (multicategoría), con **C** en **azul**. En leyenda se usan las anotaciones genéricas `ET-Etiqueta de carpinterías en leyenda : Exterior / Interior` y `ET-Etiqueta de cerrajería en leyenda : Exterior`. Para marcar la hoja activa existe `ET-Etiqueta de ventana activa : Hoja activa`.
  - **Compruébalo en cada proyecto** antes de rellenar marcas: si la etiqueta añade el prefijo, la marca debe ser «01»; si se escribe «E01», la etiqueta mostraría «EE01». En la v8 las marcas son solo números (puertas 1-19, ventanas 3-13). En CHIVERO las etiquetas cargadas mostraban solo la Marca de tipo, así que se escribió el código entero (E01, I01).
- **Modelado** (p.62):
  - Puertas y ventanas siempre en NPT, con la altura dada por **Altura de antepecho**.
  - Anchura y Altura de la familia de puerta = **hueco real de paso**; el hueco en el muro suma los cercos: «puerta de paso de 82 cm con 5 cm de cerco → hueco 92 cm».
  - Medidas normalizadas salvo casos a medida.
  - En muros compuestos hay que unir geometrías para que el hueco corte el conjunto.
- **Planos de proyecto de ejecución** (p.50-51):
  - `A.07 CARPINTERÍAS INTERIORES`, `A.08 CARPINTERÍAS EXTERIORES`, `A.09 CERRAJERÍA` (conjunto DET).
  - «*(2) Siempre que el proyecto lo permita, se incluirán todas las carpinterías en el mismo plano. En el caso de fusionar planos, se reasignarán los números».
  - Las vistas de carpintería van en el conjunto **A.5.CAL** («Calidades, carpinterías y techos», p.44).
- **Tablas** (p.51-52, v8):

| Tabla | Disciplina | Campos |
|---|---|---|
| `Carpinterías exteriores` | EQP | Familia, Tipo, Marca de tipo, Recuento |
| `Carpinterías interiores` | EQP | Función, Marca de tipo, Recuento |
| `Puertas - General` | EQP | Familia, Tipo, Nivel, Recuento, Altura, Anchura |
| `Ventanas - General` | EQP | Familia, Tipo, Nivel, Recuento, Altura de antepecho, Altura, Anchura, Área acristalamiento, Cargaderos |
| `Puertas/Ventanas certificadas` | OBR | … Certificado |

- **Mosca de carpinterías**: la v8 trae la plantilla de vista `ARQ_MOSCA CARPINTERÍAS` (planta 1:100, Bajo). Es una planta pequeña de situación, con las etiquetas, que va en el plano de carpinterías para localizar cada tipo.

### 2.2 Cómo son las leyendas de la plantilla (de los PNG)

- **ARQ-CARPINTERÍAS LEYENDA** (la que explica las etiquetas): título «LEYENDA CARPINTERÍAS» en gris, mayúsculas negritas. Tres filas, cada una con un círculo y su texto en gris:

| Círculo | Color | Texto |
|---|---|---|
| `EXX` | rojo | CARPINTERÍA EXTERIOR |
| `IXX` | verde | CARPINTERÍA PUERTA INTERIOR |
| `CXX` | azul | CERRAJERÍA |

- **ARQ-CARPINTERÍA EXTERIOR / ARQ-CARPINTERÍA INTERIOR / ARQ-CERRAJERÍA**: las tres son la misma **plantilla de fichas en cuadrícula** (1:50, cero componentes de leyenda) y solo cambia el color de la etiqueta (rojo, verde o azul). Cada ficha, de arriba abajo:
  1. **Etiqueta** circular (E01, I01, C01) centrada sobre la columna.
  2. **Espacio vacío para el alzado** de la carpintería, unos dos tercios de la altura de la ficha. En la plantilla está en blanco (comprobado en el render): se rellena con el componente de leyenda de la familia o con un dibujo de detalle.
  3. **Línea de referencia «NPT»** discontinua gris que cruza toda la fila: el alzado se apoya en ella, así que el antepecho se lee y se acota desde el NPT.
  4. **Línea continua horizontal** que separa el dibujo del texto.
  5. **Bloque de texto** en gris (CENT_GOT), alineado a la izquierda bajo la etiqueta. Puerta: **título en negrita** `E01_PUERTA DE ENTRADA` (código + guion bajo + uso o ubicación en mayúsculas) · `Puerta exterior: 920 x 2200 mm` · `1 hoja abatible` · *(línea en blanco)* · `Cant. / vivienda: 1ud` · *(línea en blanco)* · descripción constructiva («Puerta acorazada con mirilla óptica y herrajes en acabado inoxidable. Acabado exterior color RAL 7016 (gris antracita) y panelado interior en color blanco.») · *(línea en blanco)* · `Transmitancia (U) = 2,90 W/m²K`. Ventana: `E02_BAÑOS 01/02` · `Ventana exterior: 600 x 1000 mm` · `1 hoja abatible` · `Persiana: SI` · `Cant. / vivienda: 1ud` · «Aluminio texturizado con rotura de puente térmico. Acabado exterior color RAL 7016 (gris antracita). Transmitancia Aluminio (Um) = 2,90 W/m²K» · `Vidrio:` (subrayado) · «Luna 6 / Cámara 18 Argón / Luna 4 con Bajo Emisivo + Control Solar Premium» · `Factor solar (g) = 0,29` · `Transmitancia (Ug) = 1,10 W/m²K`.
  6. Las fichas se repiten en **columnas de ancho fijo** (paso ≈ 1/5,7 del ancho de la leyenda) y en **dos filas**, cada una con su propia línea NPT y su línea separadora.
- **Lo que la plantilla no fija y conviene añadir (recomendación)**:
  - El alzado se dibuja **visto desde el exterior** en las carpinterías exteriores y por la cara de apertura en las interiores, con un rótulo «Vista exterior».
  - Cotas del ancho y alto totales del marco y del hueco, y altura de antepecho desde el NPT.
  - **Símbolo de apertura en alzado. Es regla del estudio, no recomendación:** lo corrigió el usuario el 19/10/2026 («todas las ventanas tienen los abatimientos al revés»). Triángulo de líneas finas que salen de las bisagras con el vértice hacia el lado que abre (la manilla; arriba en la abatible), oscilobatiente con los dos triángulos, dos hojas con los vértices al centro, flechas en las correderas. No se deduce de la leyenda, cuyo PNG no dibuja los alzados.
  - **Uw del conjunto**, además de Um y Ug; la sección por el hueco tipo (dintel, alféizar, jamba) remitida a detalle; tipo de vidrio de seguridad si toca; la tabla con el recuento total, y la ubicación (estancias o unidades).

### 2.3 Buenas prácticas de RLA aprovechables

- Una leyenda **por material**: `MEMORIA_CARPINTERIA_MADERA / _METALICA / _ALUMINIO / MEMORIA_CERRAJERÍA`. Cada ficha lleva:
  - código (PM01, PS01, PA01, C01);
  - título con hojas, medida y código, por ejemplo «Puerta blindada de acceso a vivienda 1H 825 x 2100 mm (PM01)»;
  - **«Unidades: ver tabla adjunta»**, porque el recuento sale de la tabla de Revit y no se escribe a mano;
  - texto de partida «Suministro y colocación de …»;
  - **doble escala «(A1) 1 : 50 / (A3) 1 : 100»**.
- Familias de códigos en *Descripción*: `PM` puertas de madera, `PA` aluminio, `PS` metálicas, `VA` ventanas de aluminio, `AA`/`AC` armarios, `RF` puertas RF, `C` cerrajería. La etiqueta muestra *Descripción + Marca*. Las tablas `PUERTAS_MADERA`, `VENTANAS_METÁLICAS_ALUMINIO`… tienen los campos Comentarios de tipo, Descripción, Marca de tipo, Tipo y Recuento.
- Nombres de tipo de puerta con hojas y mano: `P_BALCONERA_(1H-A)+(F.LATERAL)_(MT)` : `1500x2100_(800)_(DCH)`.

### 2.4 Ficha AGOIN que se debe producir (síntesis)

`[círculo Exx/Ixx/Cxx] → alzado acotado sobre la línea NPT → separador → Exx_USO + «Ventana exterior: A x H mm» + hojas y apertura + persiana + «Cant.: n ud» (por unidad) + material, acabado y RAL + Um + vidrio, g, Ug (+Uw) + antepecho`. Debajo o al lado: **tabla `Carpinterías exteriores/interiores`** y **mosca de situación**. Todo en un solo plano si cabe (p.51).

---

## 3. Planos de instalaciones (fontanería, saneamiento, electricidad, clima, ventilación)

### 3.1 Lo que fija el libro

- **Códigos de disciplina** (TABLA 11, p.38): FON fontanería · SAN saneamiento · IGN gas · CLI climatización (choca con CLI comercial) · VEN ventilación · EMT/EBT electricidad de media y baja tensión · COM comunicaciones · PCI (PCI.E extinción, PCI.D detección) · SOL solar · SEG seguridad · SGN servicios generales.
- **Planos de ejecución** (TABLA 28, p.50):

| Número | Nombre del libro |
|---|---|
| IFON.01 | SANEAMIENTO |
| IFON.02 | SUMINISTRO DE AGUA |
| IELE.01 | ELECTRICIDAD |
| IELE.02 | ESQUEMA UNIFILAR |
| IILU.01 | ILUMINACIÓN |
| IMEC.01 | CALEFACCIÓN |
| IMEC.02 | CLIMATIZACIÓN |
| IMEC.03 | VENTILACIÓN |
| (navegador, p.51) | IIGN.01 gas, IPCI.01 PCI |
| OBR CON | CESS.01-04 seguridad y salud, CGR.01 GESTIÓN DE RESIDUOS |

- **Conjuntos de vista y de plano** (p.44-45): `I.1.SAN`, `I.2.FON`, `I.3.ELE` (electricidad, iluminación y telecomunicaciones), `I.4.MEC` (mecánicas, climatización y calefacción), `I.5.PCI`, `I.6.IGN`, `I.7.GDR` (gestión de residuos). En los nombres de plano de instalaciones se usan las mismas abreviaturas de 3 letras que en las vistas (hoja de arranque).
- **Sistemas MEP** (p.19-20):
  - Clasificaciones fijas de Revit. Tuberías: agua caliente sanitaria, agua fría sanitaria, sanitario, PCI húmeda/seca/preventiva/otro, suministro y retorno hidrónico, otro. Conductos: suministro, retorno, aire viciado, otro aire. Electricidad: comunicación, controles, datos, alarma, potencia, seguridad, teléfono…
  - Los **tipos de sistema** se crean dentro de cada clasificación: «aguas grises, aguas negras y pluviales, quedando todas agrupadas según la clasificación de sistema: Sanitario». Gas o humos van en «Otro».
  - Bandejas y tubos no tienen sistema: se usa «Tipo de servicio».
- **Modelado** (p.63):
  - «Los componentes de instalaciones serán, en todo caso, componentes de modelo… Dichos componentes incorporarán el símbolo 2D. Se evitará la colocación de componentes de detalle (2D), salvo que sean situaciones muy particulares».
  - Las vistas de instalaciones se muestran con nivel de detalle **Bajo** (se ve el símbolo, no el 3D) por plantilla de vista.
  - (p.72) Componente de detalle para lo que pide geometría precisa (cuadros, luminarias, terminales, sanitarios) y símbolo de anotación para lo que se representa a escala gráfica (dispositivos).
- **Parámetros**:
  - Mecánicas (p.36): Presión específica, Caudal de aire (m³/h), Caudal (l/s), Volumen, Potencia, Potencia de refrigeración y de calefacción (W o kW).
  - Tubería (p.37): Presión, Caudal (l/s), Volumen, Potencia y **Unidades de desagüe** (CTE DB HS).
  - Eléctricas (p.37): Potencia, Voltaje, Fases (1/3), Intensidad y Tipo de lámpara.
  - Compartidos AGOIN: Cantidad de interruptores, Fondo de arqueta, Lado arqueta, Recinto, Instalador, Fecha próximo mantenimiento.
- **Subproyectos MEP** (p.48, 75): `21.IF` fontanería · `22.SAN` · `23.PCI` · `24.MEC` conductos · `25.CAL` calefacción y suelo radiante · `26.ELE` fuerza · `27.LUM` iluminación, con interruptores y sensores · `30.EMC` equipos.
- **Filtros**: `<Disciplina>-<Elemento>`, por ejemplo `MEC-GruposFrigoríficos` (p.47). Los colores de filtro se aplican siempre desde la plantilla de vista (p.51).
- **Tablas**: disciplinas `FON` (aparatos sanitarios y derivados), `MEC` y `ELE` (p.46).

### 3.2 Plantillas de vista de instalaciones de la v8

En la columna de filtros, `on` = visible y `off` = oculto, según `filtros_plantilla.json`.

| Plantilla | Escala | Detalle | Filtros |
|---|---|---|---|
| `INS_FONTANERIA` | 1:100 | Fino | off: ASA-Aparatos-No tomas, TUB-Suelo radiante |
| `INS_SANEAMIENTO` | **1:200** | Fino | on: TUB-Saneamiento, TUB-Pluviales · off: TUB-Suministro, TUB-Suelo radiante, ASA-Aparatos-Tomas |
| `INS_CLIMATIZACIÓN` | 1:100 | Fino | off: TUB-Suministro, TUB-Saneamiento, ASA-Aparatos-Tomas |
| `INS_CONDUCTOS CLIMATIZACIÓN` | 1:100 | Fino | off: ASA-Aparatos-Tomas |
| `INS_VENTILACIÓN` | 1:100 | Fino | on: CON-Suministro, CON-Retorno, CON-Extracción, CON-TAE · off: ASA-Aparatos-Tomas |
| `INS_ELECTRICIDAD` / `INS_ILUMINACIÓN` / `INS_ELEC- PUESTA A TIERRA` | 1:100 | Fino | — |
| `INS_GESTIÓN DE RESIDUOS` | 1:100 | Bajo | — |

Ojo: la plantilla dice «Fino», aunque el libro pide nivel Bajo con símbolo. Comprobar en cada vista.

### 3.3 Colores y tipos de línea: estilos `MEP-*` de la v8, coherentes con las leyendas

| Red | Estilo | RGB | Grosor | Patrón |
|---|---|---|---|---|
| Agua fría (AFS) | MEP-AFS | 0,0,255 azul | 1 | continuo |
| Agua caliente (ACS) | MEP-ACS | 255,0,0 rojo | 1 | continuo |
| Recirculación ACS | MEP-ACS-R | 236,149,19 naranja | 1 | continuo |
| Residuales | MEP-Saneamiento / colgado / enterrado | 255,0,0 | 1 | continuo / TR1,5+E1,5 / trazo y punto |
| Pluviales | MEP-Pluviales / colgado / enterrado | 72,108,145 azul gris | 1 | ídem |
| Suelo radiante, ida y retorno | MEP-SR Ida / SR Retorno | 255,85,85 / 128,128,255 | 4 | continuo |
| Circuitos de SR por estancia | MEP-SR Baños / Cocinas / Hall-distribución / Seco | 219,130,140 / 230,199,91 / 255,128,64 / 152,185,98 | 1 | continuo |
| Refrigerante | MEP-Refrigerante | 251,165,0 | 4 | TR1,5+E0,75 |
| Circuitos de alumbrado | MEP-Circuitos iluminación | 50,50,255 | 1 | TR1,5+E0,75 |
| Puesta a tierra | MEP-Puesta a tierra | 84,193,11 verde | 8 | trazo y punto |

Convención del saneamiento (de la leyenda): **línea continua con flecha = colector por encima de forjado · discontinua = suspendido de forjado, pendiente mínima 1 % · trazo y punto = enterrado, pendiente mínima 2 %**. Pluviales en azul gris y residuales en rojo.

### 3.4 Leyendas de instalaciones de la v8

Formato común: título «SIMBOLOGÍA DE …» en mayúsculas, **subrayado**, gris oscuro; símbolo a la izquierda y texto gris en mayúsculas; debajo, **NOTAS** u **OBSERVACIONES** numeradas y, a veces, detalles y tablas dentro de la propia leyenda. Todas a 1:50, hechas con componentes de detalle `ED-…` y textos.

- **FON-LEYENDA FONTANERÍA**:
  - Símbolos:
    - Tuberías AFS (azul), ACS (rojo) y recirculación ACS (amarillo naranja).
    - Montantes AFS, ACS y recirculación: círculos de esos colores.
    - Válvulas de corte (pajarita), antirretorno y de equilibrado hidráulico (verde y rojo), filtro y grifo de comprobación.
    - Toma AFS (pajarita con triángulo azul) y toma ACS (triángulo rojo).
    - Bomba de recirculación ACS (círculo con triángulo en recuadro verde), unidad interior de aerotermia (cuadrado con círculo) y armario del contador general (cuadrado partido en diagonal, azul relleno).
  - Incluye el **«DETALLE DE ARMARIO PARA CONTADOR GENERAL DE AGUA»** (alzado y planta: llave de paso de macho esférico, contador, válvula de retención, grifo de comprobación).
  - 22 notas: PE 16 atm hasta el armario de contadores (UNE-EN 12201); PERT-AL-PERT hasta la llave de vivienda; PEX después; distribución por falso techo o por roza a 2,10 m; tubo empotrado protegido con PVC flexible azul/rojo; aislamiento RITE de 10 mm en los tramos finales; AFS a ≥ 4 cm del ACS; agua por debajo de la electricidad a ≥ 30 cm; DN20 mínimo para dos o más aparatos; v ≤ 2 m/s; llave de corte en cada aparato y en cada planta…
- **FON-LEYENDA SANEAMIENTO**:
  - Símbolos:
    - Bajantes de pluviales y residuales (círculo con rayado).
    - Puntos de desagüe pluviales y residuales (círculos rellenos azul gris y rojo).
    - Cazoleta de cubierta.
    - Colectores en tres variantes (§3.3).
    - Arquetas pluviales y residuales: cuadrado vacío = arqueta, con X = registrable, con X y cuadrado interior = sifónica.
    - Canalón ⌀110, tubería de drenaje (verde rayada), sumidero, bote sifónico y rejilla.
  - **Tabla «⌀ MÍNIMO DE SECCIONES»** (aparato / abastecimiento / desagüe): inodoro 12/100 · ducha 12/40 · lavabo 12/32 · bidé 12/32 · fregadero 12/40 · bañera 20/40 mm.
  - Detalles: **ACOMETIDA** (sección transversal y planta de la arqueta de acometida, tapa de hormigón de 60x50, ½ asta de ladrillo macizo, pendiente mínima 2 %, tubería de ⌀20 cm); **DIÁMETRO DE LAS TUBERÍAS en PVC** (sumidero a bote ⌀40, bote a bajante ⌀50, lavabos a bote ⌀40, inodoro a bajante ⌀110); **NTE-ISS-50** arqueta a pie de bajante y **NTE-ISS-51** arqueta de paso, con sección longitudinal y planta acotadas en mm.
  - «ESPECIFICACIONES RED DE SANEAMIENTO»: PVC serie B, arquetas de PVC en la red enterrada, desvíos aislados acústicamente, válvulas de aireación, botes de bajo perfil. Además, 9 notas al instalador: planos de montaje, pruebas, legalización, muestras, **planos de coordinación entre instalaciones «previos al inicio de los trabajos»**.
- **ELEC-LEYENDA ELECTRICIDAD** (símbolos en rojo, azul y verde):
  - Cuadro de mando y protección de vivienda, RTR 50x60x8, CGPM.
  - Derivación individual bajo tubo de 40 mm, toma de tierra.
  - Tomas de teléfono, TV y datos coaxial; zumbador.
  - Tubo PEAD Decaplast 40, videoportero (teléfono y placa de calle).
  - Bases de 25 A, de 16 A y de 16 A estanca.
  - Cajas de empotrar a 1,4 m para termostato y para unidad de control.
  - Pulsador, antena TV.
  - Enchufes con letra L lavadora o lavavajillas, S sauna, E campana o extractor, T toallero (0,5 < h < 1,5).
  - Armario de riego, armario de electricidad, tubo de 20 mm al colector o sonda exterior.
  - Notas 1-10: altura de 1,20 m en la encimera con indicador H, indicador T cerca del techo, «XN» para N tomas, C con clemas, F en falso techo, S en el colector de suelo radiante, luminarias sin referencia a elegir por la propiedad…
- **ILU-LEYENDA ILUMINACIÓN** (en azul):
  - Luminarias: downlight empotrable «tipo Targetti», luminaria de jardín, mural indirecta, regleta estanca, colgadas, bañador de pared, LED de cocina, downlight LED.
  - Interruptores unipolar, conmutador y de cruce; versiones estancas en **recuadro verde**; pulsador de timbre.
  - Puntos de luz: aplique de pared, punto de luz en techo (círculo con X), estancos exteriores (X verde), sofito de baño.
  - Tubo de PVC corrugado libre de halógenos de 20 mm (arco discontinuo).
  - OBSERVACIONES de REBT: alumbrado y fuerza por tubos independientes, dos circuitos como máximo por tubo, curvas B/C/D, cableado libre de halógenos, 30 % de reserva en los cuadros…
- **ELEC-LEYENDA ELECTRICIDAD E ILUMINACIÓN**: las dos anteriores juntas, para un único plano IELE.
- **ELEC-ESQUEMA UNIFILAR** (símbolos): fusible de protección, contador electrónico, interruptor seccionador automático, limitador de sobretensiones, magnetotérmico y diferencial. «OBSERVACIONES»: circuitos en tubos independientes, tubo corrugado libre de halógenos, todo puesto a tierra, secciones según REBT, identificación de circuitos, cuadros de frente muerto, 30 % de reserva, corte omnipolar, curvas B/C/D, poderes de corte mínimos y justificación de la selectividad.
- **ELEC-LEYENDA PUESTA A TIERRA**:
  - Símbolos: conductor de Cu desnudo de 35 mm² (verde a trazos), soldaduras aluminotérmicas (rojo) y toma de tierra en arqueta.
  - Notas: 1,50 m de cable en los pilares, 3 m en el derivador, pica de acero cobrizado de 2 m, clema bimetálica entre armadura y Cu.
  - **4 detalles**: montaje de la red de tierra en la estructura (axonometría), «ARQUETA PARA PUESTA A TIERRA DE VERTICALES (CON PICA) E= 1/20 Cotas en cm» (tapa, cerco, planta y secciones A-A y B-B), puesta a tierra de estructura metálica y de soporte de hormigón (axonometrías con lupa de la soldadura).
- **MEC-LEYENDA CALEFACCIÓN**:
  - Símbolos: impulsión y retorno PPR100 en rojo y azul, calorifugado Armaflex; refrigerante en naranja discontinuo; válvula de bola; serpentín de suelo radiante PE-X/AL/PE-X (magenta); unidad exterior de aerotermia; unidad interior hidrokit con acumulador; colector «SR» de acero inoxidable de 1" (≤ 12 circuitos) en armario de 750x1000x200; caja de unidad de control.
  - Notas de equipos (termostato digital con sonda de humedad por estancia, unidad de control táctil, sonda exterior), de tuberías y de instalación (por falso techo, encima de los conductos; purgadores en los puntos altos y desagües en los bajos; conexiones flexibles; llenado y vaciado; condensados a bote sifónico; «ver esquemas de principio»).
- **MEC-LEYENDA VENTILACIÓN**:
  - Conductos rectangulares de chapa galvanizada por color: **rojo** aspiración de cuartos húmedos y campana, **verde** impulsión a cuartos secos, **amarillo** expulsión al exterior, **azul** admisión del exterior.
  - Entrada de aire higrorregulable, boca de extracción higrorregulable (círculo dentado rojo), vertical circular ⌀150 (círculo medio relleno), grupo de ventilación (dos variantes), aberturas de paso en trasteros.
  - Nota: falso techo **desmontable** bajo el extractor.
- **PCI-LEYENDA PROTECCIÓN CONTRA INCENDIOS**: extintor 21A-113B con señal fotoluminiscente de 21x21, delimitación de sectores (línea roja discontinua), zona no considerada origen de evacuación (rayado con su superficie), «RESISTENCIA AL FUEGO DE LA ESTRUCTURA: R30» y la puerta EI2-45-C5. Trae por error una fila «entrada de aire higrorregulable»: quitarla.
- **CON-GESTIÓN DE RESIDUOS**: contenedores con muestras de color: metálicos naranja, vidrio azul, madera verde, plásticos gris.
- RLA añade, como buena práctica, una **LEYENDA_PCI** más completa: líneas EI45/60/90/120/180 como detalle repetido, rellenos por sector, señalización de evacuación, salidas numeradas, «SIN SALIDA» y «NO USAR EN CASO DE INCENDIO», y una **LEYENDA_ACCESIBILIDAD** con círculos de 1,5 y 1,2 m y pendiente de rampa.

### 3.5 Etiquetas, tablas y piezas 2D MEP de la v8

- Etiquetas: `ET-Etiqueta de tuberías : Tamaño / Tamaño + Sistema`, `ET-Etiqueta de sanitarios : Tamaño / Tamaño + Sistema`, `ET-Etiqueta de espacios`.
- Tabla de claves MEP: `C-Derivaciones individuales` (aparatos sanitarios: Nombre de la clave, **DN AFS, DN ACS**). Con ella se pone el diámetro de la derivación a cada aparato.
- **La biblioteca real de AGOIN dibuja instalaciones en 2D**: unos 140 componentes de detalle `ED-…` (ARQUETA PLUVIALES/RESIDUALES [REGISTRABLE/SIFONICA], BAJANTE, COLECTOR [ENTERRADO / POR ENCIMA / SUSPENDIDO] DE FORJADO, TUBERIA [AFS/ACS/RECIRCULACIÓN/IMPULSION Y RETORNO/REFRIGERANTE/PRIMARIO/SECUNDARIO SOLAR/DRENAJE], ENCHUFE…, INTERRUPTOR…, PUNTO DE LUZ…, DOWNLIGTH…, CUADRO…, FUSIBLE, MAGNETOTERMICO, DIFERENCIAL, LIMITADOR, CONTADOR, EXTINTOR, RECORRIDO DE EVACUACION, ZONA NO EVACUACION, DETALLE ARMARIO CONTADOR, DETALLE ACOMETIDA, DETALLE ARQUETA PUESTA A TIERRA, DETALLE DIAMETRO MINIMO SECCIONES, DETALLE DIAMETRO TUBERIAS PVC…). Choca con el libro (p.63), pero son exactamente los símbolos de las leyendas. Para un anteproyecto o básico sin redes 3D, como CHIVERO, usar estos `ED-` garantiza la coherencia entre plano y leyenda.

### 3.6 Qué planos, esquemas y detalles se esperan

- **Plantas por instalación**: saneamiento a 1:200 con la red general, más interior a 1:100; suministro de agua; electricidad; iluminación; calefacción, climatización y ventilación; puesta a tierra; PCI y gestión de residuos si procede. Cada una con su leyenda en la columna o en la banda de leyendas.
- **Esquema unifilar** (IELE.02): obligatorio en el set de ejecución (p.50), con la simbología de ELEC-ESQUEMA UNIFILAR y sus observaciones.
- **Esquemas de principio**: las notas de la plantilla los dan por existentes («Ver los diámetros de la tubería del secundario solar en el esquema de principio», «Las dimensiones de las tuberías pueden verse en los esquemas de principio y planos», «Véase esquemas de principio»). Como mínimo, uno de ACS y aerotermia y otro de calefacción o climatización. Como vista de diseño (DIS01…, conjunto I.2.FON o I.4.MEC).
- **Detalles tipo de instalaciones** que ya existen como piezas: armario de contador de agua, acometida de saneamiento, arquetas NTE-ISS-50/51, arqueta de puesta a tierra con pica, puesta a tierra de soportes.
- **Tablas en el plano**: ⌀ mínimos por aparato, derivaciones individuales (DN AFS/ACS), cargas y circuitos si procede.

---

## 4. Detalles constructivos

- **Nombre de la vista**: `DET01`, `DET02`… vistas de detalle; `DIS01`… vistas de diseño (p.44). Clase P.PLA o P.OBR y conjunto **A.6.DET** («Detalles constructivos») o **E.5.DET** para estructura. Los navegadores P.OBR y P.PLA tienen la rama «Vistas de diseño / Llamadas» (p.49).
- **Planos**: `A.10 DETALLES CONSTRUCTIVOS` (ARQ · DET) y `E.04 DETALLES DE ESTRUCTURA` (p.50). Las carpinterías y la cerrajería también van en el conjunto DET.
- **Llamadas**: «Las vistas de llamada en otro plano deben mostrar el número de plano y número de detalle (cambiar tipo)» (hoja de arranque). Familia de extremo `ET-Llamadas`; referencia a vista `ET-Referencia a vista`.
- **Plantillas de vista** [Plantilla]: `ARQ_DETALLES CONSTRUCTIVOS 1_20` (sección, **1:20**, Fino) · `ARQ_DETALLES CONSTRUCTIVOS 1_5` (sección, **1:5**, Fino) · `ARQ_DETALLES EN PLANTA` (planta, Fino) · `ARQ_SECCIONES PARA DETALLE` (sección 1:100, Bajo, la sección de la que salen las llamadas) · `ARQ_MOSCA DETALLE` (sección 1:100, Bajo, la mosca que sitúa el detalle).
- **Grosores**: la tabla de plumillas llega a 1:10 (§5.5); a 1:5 se usan los de 1:10.
- **Estilos de línea de detalle** `DET-…`:
  - Fina, gruesa y discontinua en rojo (192,0,0), azul (0,100,150), gris (192) y amarillo (255,225,0); rojo de trazo y punto.
  - `DET_Membrana impermeabilizante` (negro, 6, discontinua).
  - `DET-Aux` (rojo, auxiliar), `DET-Marco línea discontínua`, `DET-Roja etiquetas` (187,0,0, 2) y `DET-Verde etiquetas` (0,128,0, 2).
- **Patrones de dibujo**: Aislamiento - Rígido · Albañilería - Ladrillo / Bloque de hormigón · Hormigón / Hormigón - Denso / Hormigón planta · Madera - Acabado / Natural / Tablero · Metal 2 y 3 líneas · Acero · Aluminio · Yeso-Enlucido · Arena · Grava · Piedra · Plástico · Terreno / Terreno 45º · diagonales, cruces, horizontales y verticales de 0,1 a 3 mm.
- **Componentes de detalle de arquitectura**: muy pocos: `Detalle repetido`, `ED-CARGADERO ACERO : PERFIL EN L`, `ED-CARGADERO SENCILLO`, `ED-Pendiente libre`, `ED-SILUETA`. El resto del detalle se dibuja con regiones y líneas.
- **Notas clave** (p.55, 79):
  - Archivo `AGOIN_Nota clave_por elemento.txt`, «para etiquetar detalles en modelos». Es una lista por familias: B barandilla, C cubierta (C.6 «Plana Invertida no Transitable», C.10 «Teja sobre Rastreles»…), E escalera, M muro (Me.5.2 «APLAC - ENF - 1pLP - ENF – 29,5 cm»…), Pu, S forjado, T techo, V ventana…
  - Etiquetas `ET-Etiqueta de nota clave` / `ET-Nota clave : Ambos / Número / Texto`.
  - Alternativa: cargar el .txt del presupuesto como archivo de notas clave (p.79).
  - En detalles, la nota clave «por elemento» lee la del tipo; por eso los tipos no deben quedarse en `Md.1`.
- **Lo que el libro pide resolver en detalle**: anclajes de barandilla y barandillas embebidas, «en un detalle 2D» (p.61); bordes de forjado vistos u ocultos y el SATE pasante (p.58), que es dónde se corta el forjado frente al aislamiento; arranques de muros sobre NFS y NPT, uniones y acabado contra el suelo (p.59); unión de pilares embebidos (p.62).
- **Detalles mínimos para un ejecución (recomendación, a la vista de lo anterior y de CHIVERO)**:
  - Sección constructiva completa de fachada (cimiento, arranque, suelo, hueco, alero) a 1:20.
  - Hueco tipo con dintel, jamba y alféizar y el retorno del trasdosado, a 1:5 o 1:10.
  - Encuentro de cubierta rehabilitada con el muro y la cumbrera.
  - Paquete de suelo sobre encachado con suelo radiante.
  - Encuentro del trasdosado con el muro existente y el zócalo.
  - Porche (apoyo, durmiente, unión pilar-carrera).
  - Arquetas y acometida (ya en la leyenda de saneamiento).
- **Composición del plano de detalles** (recomendación coherente con p.83):
  - Detalles en cuadrícula por escala, con la mosca de situación arriba a la derecha.
  - Título de cada vista con «AG_Título automático con escala» (escalas mezcladas, así que el cajetín dirá «Como se indica»).
  - Notas clave o textos `CENT_GOT_Gris-2 mm` con directriz de 15°.
  - Leyenda de materiales y notas generales en la columna izquierda.

---

## 5. Formatos y maquetación de las hojas

### 5.1 Cuadros de rotulación (familias y tipos de la v8)

| Familia : tipo | Uso según el libro (p.82) |
|---|---|
| `CR-Cajetín con marcas : A1 / A2 / A3 / A3_32 / A4 / A4 vertical` | **Planos de construcción**, «en el tamaño que sea necesario (desde A4 hasta A1)» |
| `CR-Cajetín Mediciones : A1` | **Solo planos de mediciones** |
| `CR-Plano de revisiones : A1 / A1 Extendido` | Plano de revisiones REV (p.93) |
| `CR-Plano de tablas de revisiones : A1 / A1 Extendido` | «Plano de tablas» (REV.02) |
| `CR-Tabla de revisiones : Proyecto` | Cabecera «TABLA GENERAL DE REVISIONES DE PROYECTO» con el logotipo y la tabla Nº / FECHA / REVISIÓN |
| `CR-Observaciones de plano : Cuadro de observaciones` | Cuadro rojo «CUADRO DE OBSERVACIONES», que se añade si se usa el parámetro *Observaciones* (p.29) |
| `CR-InicioProyecto-ARQ : Formato_Inicio / Formato_Reducido` | Hoja de arranque AG00 «PORTADA/GUARDAR AQUÍ» |

**Geometría medida en los renders**, origen en la esquina superior izquierda de la hoja:

- **A1 (840 × 594, con marcas)**:
  - Recuadro a 5 mm del borde.
  - **Columna derecha de 100 mm de ancho** (x = 730–830, 10 mm hasta el canto), de y = 10 a 584.
  - Dentro de la columna, el **cajetín** ocupa los 153 mm inferiores (y = 431–584) y la zona libre para **TABLAS** encima mide 100 × 420 mm.
  - Marcas de plegado o centrado a 1/4, 1/2 y 3/4 del ancho y a media altura.
  - Texto vertical en el margen izquierdo: la razón social, la dirección y la web del estudio.
  - Zona de vistas: unos 720 × 580 mm.
- **A3 (420 × 297)**:
  - El mismo cajetín de 100 × 152 mm, en una columna de 100 mm (x = 310–410) que llega a 287 mm de alto. La zona de tablas queda en 100 × 125 mm.
  - **La zona de vistas se reduce a unos 300 × 282 mm**: el cajetín se come el 24 % del ancho.
  - Marcas a media anchura.
- **Mediciones A1**: solo el recuadro del cajetín abajo a la derecha (100 × 160 mm). El resto de la hoja queda libre para tablas, con la guía «Guías tablas = Sí».
- **Campos del cajetín** (de arriba abajo):
  - PROYECTO / UBICACIÓN / PROMOTOR / ARQUITECTO.
  - FIRMAS / SELLOS (firma escaneada) | COD. PROY. y VERSIÓN.
  - CONTENIDO | (vacío).
  - Nº PLANO / PLANOS TOTALES | FECHA.
  - ESCALA | NORTE (círculo con la flecha).
  - Bloque del logotipo verde AGOIN con razón social y dirección.
  - Rótulos en mayúsculas negras y valores en gris.
- **De dónde sale cada campo** (Información de proyecto, p.82 y 90):

| Campo del cajetín | Parámetro | Ejemplo de la plantilla |
|---|---|---|
| PROYECTO | Nombre de proyecto | — |
| UBICACIÓN | Dirección de proyecto | — |
| PROMOTOR | Nombre de cliente | — |
| ARQUITECTO | Autor | el nombre del arquitecto |
| COD. PROY. | Número de proyecto | `XX_XX_AAAA` |
| VERSIÓN | Probablemente Estado de proyecto, a comprobar en la familia | `PEJ`, `V1` |
| FECHA | Fecha de emisión de proyecto | `MM/AAAA`, por ejemplo `08/2020` |
| CONTENIDO | Nombre de plano | — |
| Nº PLANO | Número de plano | — |

  En la prueba de CHIVERO, VERSIÓN mostraba un texto largo que **se desbordaba** sobre CONTENIDO y FECHA, FECHA mostraba el literal «Fecha de emisión» y ARQUITECTO salía vacío.
- **Parámetros del cajetín** (ejemplar):
  - `Escala auto` (Sí por defecto) y `Escala fija` + parámetro del plano **`Escala general`**: «la escala automática marcará “E 1/XXX” si y solo si todas las vistas tienen la misma escala… en caso contrario “Como se indica”, por lo que será conveniente mostrar los Títulos de vista». Si las vistas principales comparten escala pero hay leyendas o moscas, se activa *Escala fija* y se escribe la escala en *Escala general* del plano (p.53-54).
  - `Norte` (ángulo; 90° = arriba) y `Norte visible`: **el norte del plano es el del cajetín**.
  - `Datos generales` y `Datos por plano`.
  - `DISTANCIA TEXTO`.
- **Parámetros del plano**: `Disciplina plano` (ARQ, EST, INS, OBR, VARIOS; 00.PORTADA en AG00), `Conjunto plano` (1.SIT, …, MED, REVISIONES; INICIO), `Observaciones` (multilínea) y `Plano terminado` (Sí/No), que aparecen en `+00-Libro de planos`.

### 5.2 Zonas de la hoja (p.82-84)

- **Esquema general** (p.83):
  - **«ESPACIO PARA LEYENDAS VERTICALES»**: columna izquierda de ancho completo, unos 90 mm en A1.
  - **«VISTAS DE PROYECTO»** en el centro: «podrán “invadir” el espacio para leyendas cuando sólo se utilice una de ellas».
  - **«ESPACIO PARA LEYENDAS HORIZONTALES»**: banda inferior desde la columna izquierda hasta el cajetín, unos 60 mm de alto en A1.
  - **«TABLAS»**: columna derecha, encima del cajetín.
  - «Si el plano no contiene leyendas, podrá aprovecharse todo el espacio disponible para el montaje de vistas».
- **Plano mixto** (p.84), «vistas acotadas y vistas de acabados»: **«VISTAS TÉCNICAS»** en la mitad superior y **«VISTAS DE ACABADOS/CALIDADES»** en la mitad inferior, las dos a todo el ancho hasta la columna de **TABLAS**. La misma planta dos veces, una acotada y otra con calidades.
- «NOTA: La disposición de planos anteriormente descrita es una muestra… deberá ajustarse según los contenidos del proyecto».
- **Plano de revisiones** (p.93), formato libre: arriba a la derecha la tabla «CHECKLIST VISTAS REVISIÓN» (casillas que se marcan en el cajetín: 3D Frente, 3D Trasera, 3D Estructura, Alzados, Secciones, Plantas mobiliario, Plantas acotadas, Planta de cubiertas, Plantas cimentación, Plantas estructura, Plantas saneamiento, Plantas ventilación, Plantas climatización) y debajo la tabla de revisiones; a media altura el «Cuadro de observaciones»; abajo, a la izquierda del cajetín, las **tablas de superficies**. Puede ser «A1 extendido».

### 5.3 Títulos de vista, escalas gráficas y norte

- **Tipos de ventana gráfica** [Plantilla], todos sin línea de referencia:
  - `AG_Título automático con escala` (`TV-Titulo de vista : Con escala`)
  - `AG_Título automático sin escala` (`TV-Titulo de vista : Sin escala`)
  - `AG_Título con escala` (`TV-Titulo en el plano : Título + Escala`)
  - `AG_Título sin escala` (`TV-Titulo en el plano : Sin escala`)
  - `AG_Sin título`, para leyendas, que ya llevan su propio rótulo «SIMBOLOGÍA DE …» o «LEYENDA …».
- **Escalas gráficas**: «Las escalas gráficas se añadirán, si procede, mediante símbolos en la ficha Anotar» (hoja de arranque). Familias `SI-Escala-Grafica-1-XX : 1 a XX (Metros)` para 1:10, 20, 25, 30, 50, 75, 100, 150, 200, 250, 300, 400, 500, 600, 750, 1000 y 2000 (no hay 1:125).
- **Cotas**: `AG-2 mm` lineal, radial y diametral (Century Gothic, negro); `AG-1.5 mm`, `AG-2.5 mm`, `AG-3 mm`; angular `AG-2 mm` y `AG-1.5 mm`; cota de nivel `AG-PBP-1.5/2 mm` (relativa al punto base) y `AG-PR-1.5/2 mm` (al punto de reconocimiento); pendiente `AG-1.5/2/2.5 mm Flecha rellena / abierta`. Símbolo `SI-Cota altimétrica : Cota altimétrica de planta`.
- **Niveles en alzados contrapuestos**: que salgan en el mismo lado, pasándolos a 2D (p.56-57). Extremos `NV-Extremo de nivel`, `XN-Extremo de nivel`, `XR-Extremo de rejilla` y `MS-Extremo inicial de sección (-alzado)`.

### 5.4 Numeración y nombre de los planos (p.45-46, 50-51, hoja de arranque)

- **Formato**: `<Letra de disciplina>.<NN> - <NOMBRE EN MAYÚSCULAS>`, por ejemplo `A.01 - MOBILIARIO PLANTA BAJA`, `E.01 - PÓRTICOS`, `I.01 - INSTALACIÓN FONTANERÍA`, `A.01-URBANIZACIÓN`, `I.01-SUMINISTRO DE AGUA`. Letras: A arquitectura, C construcción, E estructura, I instalaciones.
- **Variante con el conjunto** (hoja de arranque): `ACOT.01 - PLANTA 00`.
- **Instalaciones con las tres letras de la vista**: `IFON.01`, `IELE.01`, `IILU.01`, `IMEC.01`, `IPCI.01`, `IIGN.01`. Obra: `O.01`, `CESS.0x`, `CGR.01`. Revisiones: `REV.01`. Mediciones: `MED`, en VARIOS.
- **Set mínimo de ejecución** (TABLA 28):

| Número | Plano |
|---|---|
| A.01 | SITUACIÓN Y EMPLAZAMIENTO · IMPLANTACIÓN Y COTAS DE PARCELA |
| A.02 | PLANTA BAJA. USOS Y MOBILIARIO |
| A.03 | PLANTA BAJA. COTAS |
| A.04 | PLANTA DE CUBIERTAS |
| A.05 | ALZADOS GENERALES (1) |
| A.06 | SECCIONES GENERALES (1) |
| A.07 | CARPINTERÍAS INTERIORES (2) |
| A.08 | CARPINTERÍAS EXTERIORES (2) |
| A.09 | CERRAJERÍA |
| A.10 | DETALLES CONSTRUCTIVOS |
| E.01-04 | CIMENTACIÓN, REPLANTEO DE PILARES, FORJADOS, DETALLES |
| IFON… IMEC.03 | Instalaciones (§3.1) |
| CESS.01-04, CGR.01 | Obra |

  (1) Alzados y secciones en el mismo plano siempre que se pueda. (2) Todas las carpinterías en el mismo plano siempre que se pueda.
- Básico: situación y emplazamiento, implantación, plantas, alzados y secciones. Anteproyecto: situación, plantas, alzados y secciones (p.50).
- **Navegador**: `DISCIPLINA DE PLANO – CONJUNTO DE PLANO` (p.51). Los conjuntos ARQ son 1.SIT, 2.MOB, 3.COT, 4.CON, 5.CAL, 6.DET, 7.SUP y 8.CLI; los demás, en p.45.
- **Vistas**: `<Clase>-<Nivel>-<Conjunto>-<Descripción>`, por ejemplo `TRA-NPT P00-GEN-Planta baja general` o `COT-NPT-Planta primera`. Las vistas finales de plano omiten la clase. Descripción con mayúscula inicial y sin punto final. Prefijo `A2_` para zonas.
  - Parámetros: `Clase de vista` (0.CORD, 1.TRA, P.OBR, P.PLA, R.REF) y `Conjunto de vista` (A.3.COT…).
  - «NO se admitirán vistas “???”»: las mal nombradas se borran en el mantenimiento semanal (p.44).

### 5.5 Textos, colores y grosores

- **Nombre de los tipos de texto** (p.85): `<FUENTE>_<Color>-<altura>_<Comentario>`, por ejemplo **`CENT_GOT_Gris-2 mm_Cuadro`**. Las fuentes largas se abrevian a 3 o 4 letras en mayúsculas, con `_` entre las partes.
- **Tipos de texto de la v8** (todos Century Gothic salvo los ARIAL):

| Color | Tipos |
|---|---|
| Negro | `CENT_GOT_Negro-1 mm`, `1,5 mm`, `2 mm`, `2,5 mm`, `3 mm` |
| Gris (128) | `CENT_GOT_Gris-1,5 mm`, `2 mm`, `2,5 mm` y sus variantes `_Cuadro` |
| Verde (0,128,64) | `CENT_GOT_Verde-1,5 mm`, `2,5 mm`, `4 mm` (más `Verde-2 mm` y `Verde-2.6 mm` en 0,128,0) |
| Otros | `CENT_GOT_Rojo-2 mm` (187,0,0), `CENT_GOT_Azul-2 mm` (0,128,192) |
| Arial | `ARIAL_Negro-1,5 mm`, `ARIAL_Negro-2 mm`, `ARIAL_Gris-1,5 mm`, `ARIAL_Gris-2 mm` |

- **Propiedades fijas** (p.86):
  - Desfase de la directriz o el borde: **1 mm**.
  - Tabulación de 12,70 mm.
  - Directriz con punta de **15° rellena**.
  - **Fondo transparente**, salvo sobre tramas.
  - `_Cuadro` = «Mostrar borde» activado.
  - Grosor de línea 1.
  - Los textos y las cotas tienen tamaño absoluto en mm, no escalan (p.15).
- **Jerarquía de uso** (de las tablas, p.85, y de las leyendas): títulos en **verde de 4 mm**; cabeceras en negro o gris de 2,5 mm; cuerpo en negro o gris de 2 mm. Las leyendas usan gris en mayúsculas para el contenido y gris en negrita (ARQ) o subrayado (instalaciones) para el título.
- **Colores RGB AGOIN** (TABLA 35, p.86): negro 0,0,0 · gris 128,128,128 · blanco · **verde 0,128,64** · **rojo 192,0,0** · **azul 0,0,225** · naranja 255,128,64 · amarillo 255,225,0. «Añadir los colores nuevos al término de cada proyecto». El logotipo del cajetín es otro verde (en CHIVERO, 7,87,72).
- **Tabla de plumillas** (TABLA 31, p.54), en mm por escala:

| Pluma | 1:10-1:50 | 1:100 | 1:200 | 1:500 | Persp./Anot. |
|---|---|---|---|---|---|
| 1 | 0,025 | 0,025 | 0,025 | 0,025 | 0,025 |
| 2 | 0,10 | 0,10 | 0,05 | 0,05 | 0,05 |
| 3 | 0,20 | 0,20 | 0,10 | 0,05 | 0,09 |
| 4 | 0,25 | 0,25 | 0,20 | 0,15 | 0,15 |
| 5 | 0,30 | 0,30 | 0,25 | 0,20 | 0,20 |
| 6 | 0,40 | 0,40 | 0,30 | 0,20 | 0,25 |
| 7 | 0,50 | 0,50 | 0,40 | 0,30 | 0,30 |
| 8 | 0,70 | 0,60 | 0,50 | 0,40 | 0,40 |
| 9 | 1,00 | 0,70 | 0,50 | 0,40 | 0,50 |
| 10 | 1,50 | 1,00 | 1,00 | 0,50 | 0,75 |
| 11-16 | 2,0 / 2,5 / 3 / 4 / 5 / 6 | 1 / 2 / 2 / 3 / 4 / 5 | 1 / 1 / 1 / 2 / 3 / 4 | 0,7 / 1 / 1 / 1 / 2 / 3 | 1 / 1,5 / 2 / 2,5 / 3 / 4 |

- **Estilos de línea útiles**:
  - `<Líneas anchas>` 9 · `<Líneas medias>` 5 · `<Líneas finas>` 1.
  - `<Más allá>` y `<Líneas ocultas>` en gris 192.
  - `<Derribado>` negro TR5+E2,5 · `<Elevado>` gris TR1+E1.
  - `VIS-Sección/alzado` (151,0,0).
  - `OBR-Vallados` (255,128,64, 10).
  - Acabados `ACA-Acabado alicatado` (17,177,255) / `enfoscado` (198,0,0) / `monocapa` (128,0,255) / `yeso` (0,128,0) / `aplacado` (234,170,122) / `madera` (188,124,61) / `acero` (95,95,95) / `chapa perforada` (64,128,128) / `enfoscado/mortero` (202,217,145), todos de grosor 6 y patrón «TR 2mm + E 1mm».

### 5.6 Formato de las tablas en el plano (p.84-85)

- **Tipos de tabla**: `+00-` control e información · sin prefijo = tablas de planificación y cantidades, que son las que **van en los planos** · `TC-` claves · `TR-` de trabajo, que no van en los planos. Para incluir una tabla de trabajo en una entrega hay que renombrarla.
- **Plantilla de las tablas para planos** (`TABLAS_GENERALES`, que el libro llama «TP_Tablas de Planificación»):
  - Rejilla de líneas **desactivada**.
  - Contorno en líneas finas.
  - **«Fila vacía antes de datos»**.
  - Título `CENT_GOT_Verde-4 mm`, cabecera `CENT_GOT_Negro-2,5 mm`, cuerpo `CENT_GOT_Negro-2 mm`.
- **Plantilla de las tablas de claves** (`TABLAS_CLAVES`, «C_Tablas de Claves»):
  - Rejilla en líneas finas, sin contorno y sin fila vacía.
  - Título `Verde-4 mm`, cabecera `CENT_GOT_Gris-2,5 mm`, cuerpo `CENT_GOT_Gris-2 mm_Cuadro`.
- **Ancho de las tablas**: «se resolverán en plano» (p.85).
- **Cabeceras agrupadas** de las tablas de medición (render del plano de tablas): «MUROS DE FACHADA Y PARTICIONES» con los grupos LOCALIZACIÓN (Tipo BIM, Planta, Altura) y ESTADO DE MEDICIONES (N, Longitud, Ancho, Área, Volumen). Igual en Suelos y acabados, Cubiertas, Falsos techos, Escaleras, Barandillas, Puertas, Ventanas, Estructura… Las de superficies son de dos columnas, «SUPERFICIES ÚTILES: Nombre | Superficie».

### 5.7 Impresión y exportación (p.87-90), y el caso A3

- **PDF**:
  - Impresora virtual (Adobe PDF).
  - **«Combinar selección múltiple de vistas/planos en un solo archivo»**.
  - Planos seleccionados y **tamaño de papel en «Configuración»** (ejemplo «A2 - Horizontal»).
  - Nombre del archivo del ejemplo: `AG-PLA-V4-ARQ-R19.pdf`.
- **DWF**:
  - Configuración de impresión «A1 - Horizontal» guardada en la plantilla («no hay que modificarlo, basta con elegir el formato de salida»).
  - Zoom al 100 %, desfase desde la esquina sin margen, procesado vectorial, calidad ráster «Presentación», en color.
  - Ocultar planos de referencia y de trabajo, cajas de referencia y contornos de recorte.
  - **Sin** «Ocultar etiquetas de vista sin referencia» y **sin** «Reemplazar tramado por líneas finas».
  - Revisar antes la Información de proyecto.
- **DWG** «Agoin DWG» (TABLA 32): capas AIA ByLayer, PSLTSCALE = 1, acdbiso.lin y .pat, colores especificados en la vista, metros con coordenadas internas, sin habitaciones, sin vistas en planos ni vínculos como referencias, formato AutoCAD 2010.
- **Nombre de los archivos** (p.38): `<Nº proyecto>-<Código de 4 letras>-<Fase PAN|PBS|PEJ|LIC>-<Disciplina>-<Vn>-<AAAAMMDD>-<R20>`, por ejemplo `19_48-VUCJ-PBS-ARQ-V4-20200803-R20`. Sin espacios ni tildes. «XX» si no aplica.
- **A3**: el libro solo aporta que existe un cajetín A3 (y `A3_32`) y que el tamaño se elige al imprimir. **No da reglas de reducción.** Lo que se deduce de las fuentes, más alguna recomendación:
  1. **Si el entregable es A3, montar hojas A3 nativas** con `CR-Cajetín con marcas : A3`. El cajetín sigue midiendo 100 mm: quedan unos 300 × 282 mm útiles, así que cabe una vista por hoja a 1:100-1:200 y las leyendas tienen que ir a la banda inferior o a otra hoja.
  2. **Si se imprime A1 reducido a A3** (50 %): imprimir «Ajustar a la página»; poner **escala gráfica `SI-Escala-Grafica` en cada vista** (es lo que hace medible la copia reducida) y **doble indicación de escala** como RLA: «(A1) 1:50 / (A3) 1:100», en los títulos o en una nota junto al cajetín. RLA tiene en el plano los parámetros `ESCALA_A1` / `ESCALA_A3` y títulos `NOMBRE+ESCALAS_1/_2`.
  3. Los textos de 2 mm quedan en 1 mm en A3, en el límite de legibilidad, y los de 1,5 mm no se leen (recomendación: nada por debajo de 2 mm en hojas que se vayan a reducir, y títulos y tablas a 2,5 mm o más). Las plumillas finas (0,025-0,10) desaparecen, así que no confiar en la pluma 1 para nada que se tenga que ver.
  4. Las hojas de dudas para dibujar a mano (A3) usan el mismo cajetín A3.

---

## 6. Otras buenas prácticas que se suelen olvidar

- **Revisiones** (p.27-29):
  - Revisiones de proyecto numeradas, con **fecha DD/MM/AAAA** y descripción, «Mostrar: **Nube y etiqueta**».
  - Al validarlas se marca «Emitida» y se rellena «Emitida por».
  - **Plano específico `REV.01 – Plano de revisiones`**, con la misma tabla en la portada.
  - Activar la revisión en el plano («Revisiones en plano» → «Mostrado en tabla de planificación de revisiones»).
  - Las nubes se crean después de la revisión y **siempre etiquetadas** (`ET-Etiqueta de revisión`, `-Comentarios`, `ET-Revisiones`).
  - Para revisar vistas que ya están en plano se usa **«Duplicar como dependiente»**.
  - Parámetro de plano **Observaciones** (multilínea) + cuadro `CR-Observaciones de plano`.
  - Proceso en 7 pasos (p.29): crear, activar en REV o portada, nube y etiqueta, añadir vistas a REV, observaciones en texto, observaciones gráficas, Emitida por y casilla.
- **Libro de planos e índice**: `+00-Libro de planos` (Disciplina plano, Conjunto plano, Número, Nombre, Fecha de emisión, Revisión actual con fecha y descripción, Observaciones, Plano terminado) y `+00-Información de Proyecto`. Ponerlos en la portada o en el primer plano. RLA añade `ESCALA_A1`, `ESCALA_A3` y `TIPO_PLANO` al listado.
- **Tablas base de todo proyecto** (TABLA 30, p.51-52):
  - `+00-Libro de vistas`, `+00-Tabla de elementos`, `+00-Vínculos RVT`.
  - `C/TC-Acabados de habitación`, `TC-Densidades de ocupación`.
  - Mediciones (Acabados y revestimientos, Barandillas, Cubiertas, Escaleras, Falsos techos, Muros, Suelos).
  - EQP (Mobiliario, Puertas, Ventanas), OBR (certificados), EST, SUP (Superficie computable total, Aparcamiento, Superficies útiles), ENT (movimiento de tierras).
  - **«Plano de tablas» REV.02** con todas las mediciones en A1.
- **Cuadro de superficies** (p.79-81):
  - **Superficies útiles** salen de las *Habitaciones* y **construidas** de las *Áreas*, en planos de área. Hay un único tipo de área y, para la urbanización, `AG_Urbanización`.
  - Tablas para planos: «SUPERFICIES ÚTILES» y «SUPERFICIES EXTERIORES» (Nombre | Superficie), «SUPERFICIE CONSTRUIDA» y «SUPERFICIE URBANIZADA».
  - Se **duplica la tabla por planta o vivienda** con filtro: «Superficies Útiles – Vivienda A - Planta baja».
  - Orden de los campos: **Portal / Puerta / Número* / Nombre / Departamento* / Perímetro* / Superficie Útil**.
  - Tablas de gestión: `TR-Superficies Útiles Totales` (T.S.U. Interior / Exterior / S.U. Total) y `TR-Superficie Computable` (% Área computable).
- **Nombres de estancia** (p.34):
  - «Dormitorio principal» (no «ppal.»), «Dormitorio #» solo si hay más de uno, «Baño principal» dentro del dormitorio principal, «Aseo» sin ducha ni bañera, «Pasillo-Circulación», «Armario», «Tendedero», «Lavadero», «Terraza», «Jardín», «Instalaciones», «Bodega».
  - Parámetro **Exterior Sí/No** para separar la superficie útil interior de la exterior.
  - Portal y Puerta cuando hay varias viviendas.
  - Áreas: Vivienda, Terraza cubierta o descubierta, Cuartos técnicos… Número `POR.21-PUE.C`.
- **Documentación comercial** (p.91-92): plantilla de vista `HABITECH ESTANCIAS` con relleno de color por el parámetro de habitación `Habitech: Clase de superficie` (Exterior pavimentada RGB 250-230-2.., Exterior terreno 205-220-1.., Sin uso 200-215-2..), y **«Leyenda de relleno de color»** en el plano.
- **Moscas y vistas de referencia**: `ARQ_MOSCA ALZADOS` y `ARQ_MOSCA SECCIONES` (planta 1:200, Bajo, con filtros `SEC-No alzados`, `SEC-Alzados`, `SEC-No Acotadas`), `ARQ_MOSCA CARPINTERÍAS` y `ARQ_MOSCA DETALLE`. Clase de vista `R.REF`, conjunto `A.6.DET`. Toda hoja de alzados, secciones, carpinterías o detalles lleva su mosca.
- **Escaleras**: ocultar las subcategorías del mamperlán, porque si no cada peldaño sale con línea doble, y los patrones de superficie (p.61).
- **Fases**: todos los elementos de una misma partida en la misma fase, para medir bien (p.78). La v8 tiene una sola fase, «Proyecto». RLA, para reformas, usa **EXISTENTE / DERRIBOS / NUEVA_CONSTRUCCION** con filtros `DERRIBO_*`, `EXISTENTES`, `REFORMADO_*` y materiales de fase `AG_Fase-Existente/Derribo/Temporal/Nueva` (estos también en la v8).
- **Criterio de medición**: «lo que no se ve a escala 1/50 no se modela» (rodapiés, por ejemplo, por longitud de muro o por perímetro de habitación); acabados en los parámetros de la habitación además de en suelos, techos y muros; «hacer partes con los muros» para medir por material; tipo BIM = partida unívoca, con *Código de montaje* (p.75-78).
- **Antes de emitir**:
  - Rutinas Dynamo de unión de suelos y muros (p.59-60).
  - Revisar los avisos (p.67).
  - Información de proyecto completa (p.67, 90): Nombre, Número, Autor, Cliente, Dirección, Fecha de emisión, Estado y Comentarios.
  - Norte real y coordenadas (punto de reconocimiento y punto base), proyecto en metros con 2 decimales.
  - Vista 3D limpia llamada **«Navis»** sin anotaciones (p.88).
  - Entregables: PDF por set de planos y, en ejecución, **«Tablas de datos de superficies y mediciones»** (p.25).
- **Leyendas en más de un plano**: si una vista hace falta en varios planos, valorar convertirla en leyenda (p.66).
- **Etiquetas nuevas**: siempre con parámetros compartidos y bajo la supervisión del BIM Manager (p.64). Archivo único `AGOIN_Parámetros compartidos.txt`, que incluye *Título en el plano*, *Escala general*, *Plano terminado*, *Observaciones*, *Altura techo*, *Exterior*, *Habitech: Clase de superficie*…
