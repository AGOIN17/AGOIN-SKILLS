---
name: libro-estilo-agoin
description: "[ESTILO · PLANOS] El libro de estilo de AGOIN (LdE V5 y plantilla de Revit AG-PLA-V8) más las correcciones del usuario, para que planos, tipos, vistas, textos, tablas, leyendas y entregables salgan «a la AGOIN»: zonas de la hoja y cajetín en A1 y A3, numeración A.xx / E.xx / IFON…, nombres de tipos (FCH-…=cm) y materiales AG_, etiquetas Mxx/Sxx/Axx/TExx y E/I/C, textos CENT_GOT, colores, plumillas, fondos de texto, fichas de carpintería y de muros, símbolo de apertura, fases, revisiones y nombre de archivos. Úsala siempre que maquetes, nombres, etiquetes o revises planos, tipos, vistas, tablas o leyendas de un proyecto de AGOIN, y cuando el usuario pida «estilo AGOIN», «libro de estilo», «como un estudio top» o «con esas plumillas»."
metadata:
  etiquetas: "ESTILO, PLANOS"
---

# Libro de estilo de AGOIN

El usuario quiere planos «como un estudio de arquitectura top», «con esas plumillas», que sean «de wow», y con el estilo propio del estudio. Ha dicho más de una vez que unas láminas «no son igual que AGOIN»: estas reglas son lo que las hace serlo.

**De dónde sale cada regla:**

- **[LdE]**: el «Manual de Producción de Proyectos BIM – Libro de Estilo» V5 (2022) y la plantilla `AG-PLA-V8`. El detalle, con páginas, está en `references/libro-estilo-LdE-V5.md`. Léelo antes de maquetar un juego completo.
- **[Usuario]**: corrección o petición expresa del usuario. Manda sobre el libro.
- **[Práctica]**: lo que se hizo en un proyecto y el usuario aceptó sin ser regla del libro. Confírmalo en el siguiente.

**Qué manda en cada proyecto.** En un proyecto propio, el LdE. Si el encargo es actualizar un proyecto ya visado con su propia maquetación, se reproduce la de ese proyecto y el LdE se aplica a lo nuevo y a lo que el proyecto no fija. Pregúntalo el primer día.

**Los originales** (PDF del libro, plantilla `.rte`, `AGOIN_Parámetros compartidos.txt`, `AGOIN_Nota clave_por elemento.txt`) los guarda el estudio. Pide al usuario la carpeta, cópialos a `referencias/copias` del proyecto y trabaja sobre las copias. Las plantillas de versiones antiguas de Revit las actualiza el usuario: por API tardan horas.

## 1. Principios

- **El plano sale del modelo**, con tipos bien nombrados. La Marca de tipo es el código del plano, y una leyenda o tabla de la misma hoja explica cada código. [LdE]
- **Pocas láminas, completas y ordenadas** (en juegos nuevos; si se actualiza un juego visado, manda su organización). Planos de conjunto (toda la finca, el ala entera), cada hoja llena, leyendas y tablas en la propia hoja, cada fase clara. «Quizás menos planos pero más completos y mejor ordenados»: 27 hojas por vivienda le parecieron fragmentadas. [Usuario]
- **Nada se da por bueno sin mirarlo como imagen** (PDF a 150 ppp, por zonas). Ver `planos-laminas`. [Práctica]
- **La leyenda explica todo lo que se dibuja.** Un revisor encontró un colector sin línea en la leyenda y elementos amarillos sin explicar. [Práctica]

## 2. La hoja

- **Cajetín `CR-Cajetín con marcas`** (A1, A2, A3, A3_32, A4). Las mediciones, con `CR-Cajetín Mediciones : A1`. En Revit su origen está en la esquina inferior derecha: las coordenadas de hoja salen negativas en x. [LdE; Práctica]
- **A1 (840 × 594):** recuadro a 5 mm del borde; **columna derecha de 100 mm** con el cajetín en sus 153 mm inferiores y la zona de **TABLAS** encima; **leyendas** en una columna izquierda de unos 90 mm o en una banda inferior de unos 60 mm; **vistas** en el centro, que pueden invadir el sitio de leyendas si solo se usa una de las dos zonas. [LdE]
- **Plano mixto:** vistas técnicas (acotadas) arriba y vistas de acabados o calidades abajo, con la columna de tablas a la derecha. [LdE]
- **A3 nativo (420 × 297)** cuando el entregable es A3 («que se vea todo bien en formato A3»): mismo cajetín de 100 mm a la derecha; zona de dibujo de unos 12–303 × 12–286 mm; las hojas de trabajo pueden llegar hasta el marco (8–307 × 8–289). [LdE; Usuario]
  - **Textos de 2 mm como mínimo.** 1,5 mm solo en hojas de trabajo. [Práctica]
  - Si se imprime un A1 reducido a A3: escala gráfica en cada vista y doble escala «(A1) 1:50 / (A3) 1:100». En A3 reducido, la pluma 1 desaparece. [LdE]
- **Cajetín, campos:** PROYECTO, UBICACIÓN, PROMOTOR, ARQUITECTO (Autor, nunca vacío), COD. PROY. (`XX_XX_AAAA`), VERSIÓN con un código corto (un texto largo se desborda sobre CONTENIDO y FECHA), FECHA de emisión (`MM/AAAA`; la fecha de cada revisión, en cambio, va como DD/MM/AAAA), CONTENIDO (unos 55 caracteres como mucho en A3), Nº PLANO, ESCALA y NORTE. Salen de Información de proyecto. [LdE; Práctica]
- **Escala del cajetín:** «Escala auto» pone «E 1/XXX» si todas las vistas comparten escala; si no, «Como se indica» y título con escala en todas las vistas. Si la principal es común pero hay leyendas o moscas, «Escala fija» con el valor en «Escala general» del plano. Las hojas sin vista a escala y los esquemas llevan «S/E». [LdE; Práctica]
- **Norte:** el del cajetín (`Norte`, 90° = arriba; `Norte visible`). Si la planta va girada al eje del edificio, ajústalo en cada hoja y compruébalo a la vista. [LdE]

## 3. Numeración, nombres y versiones

- **Planos:** `<Letra>.<NN> - NOMBRE EN MAYÚSCULAS`. A arquitectura, E estructura, C construcción. Instalaciones con tres letras: IFON (saneamiento y agua), IELE (electricidad y esquema unifilar), IILU, IMEC (calefacción, climatización, ventilación), IPCI, IIGN. Obra: CESS, CGR. Mediciones: MED. **REV es el plano de revisiones**: no lo uses para otra cosa. [LdE; Usuario]
- **Parámetros de plano** `Disciplina plano` (ARQ, EST, INS, OBR, VAR) y `Conjunto plano` (ARQ: 1.SIT, 2.MOB, 3.COT, 4.CON, 5.CAL, 6.DET, 7.SUP, 8.CLI; INS: 1.SAN, 2.FON, 3.ELE, 4.MEC…). El navegador se ordena por disciplina y conjunto. [LdE]
- **Juego mínimo de ejecución:** A.01 situación y emplazamiento, A.02 usos y mobiliario, A.03 cotas, A.04 cubiertas, A.05-A.06 alzados y secciones (juntos si se puede), A.07-A.08 carpinterías (todas en un plano si se puede), A.09 cerrajería, A.10 detalles, E.01-04, instalaciones e **IELE.02 esquema unifilar, obligatorio**. [LdE]
- **Series propias para el cliente y para trabajar** (aceptadas por el usuario, no están en el libro): DUDA.xx, DEC.xx, DIS.xx, Cn.mm, TR.xx, NIV.xx, G.xx, DESP.xx. Ver `decisiones-cliente`. El compositor de láminas no debe borrarlas al rehacer el juego. [Práctica]
- **Vistas:** `<Clase>-<Nivel>-<Conjunto>-<Descripción>`; las que van en hoja omiten la clase. Descripción con mayúscula inicial y sin punto final. Ni «???», ni «Copia de», ni «:». [LdE]
- **Nombre de archivo:** el libro pide `<Nº proyecto>-<código de 4 letras>-<PAN|PBS|PEJ|LIC>-<disciplina>-V<n>-<AAAAMMDD>-R<versión de Revit>`, sin espacios ni tildes. **«V» es la versión del juego y «R» la de Revit: no las mezcles** (en un proyecto los juegos se llamaron R05…R09 mientras el modelo era «_R27»). Si un proyecto ya usa otra convención, mantenla dentro del proyecto y pregunta antes de cambiarla. La versión anterior se conserva. [LdE; Práctica]

## 4. Vistas, títulos y escalas

- **Título nativo** `AG_Título automático con escala` (lee «Título en el plano»). Esquemas, con `AG_Título automático sin escala`. Leyendas, con `AG_Sin título`, porque llevan su propio rótulo. [LdE]
  - Los títulos de más de unos 44 caracteres parten línea y pisan la escala: abrévialos.
- **Escala gráfica** `SI-Escala-Grafica-1-XX` en todas las vistas de plano. No hay de 1:125 ni 1:175; comprueba que la barra corresponde a su escala (en la plantilla, la de 1:200 dibujaba la de 1:100). [LdE; Práctica]
- **Moscas de situación** en toda hoja de alzados, secciones, carpinterías o detalles. [LdE]
- **Corte de las plantas:** si hay unidades a distinto nivel, 1,30 m sobre el suelo de cada unidad («las ventanas no están bien maquetadas»). [Usuario]
- **Secciones:** reserva unos 25 mm a la derecha para las cotas de nivel, que sobresalen del recorte, y colócalas en filas por su ancho real. [Práctica]

## 5. Textos, colores y líneas

- **Tipos de texto** `<FUENTE>_<Color>-<mm>[_Cuadro]`, por ejemplo `CENT_GOT_Gris-2 mm`. Todo en Century Gothic. Directriz con punta rellena de 15°, desfase de 1 mm. [LdE]
- **Jerarquía:** títulos en verde de 4 mm; cabeceras en negro o gris de 2,5 mm; cuerpo de 2 mm. [LdE]
- **Fondo de los textos:** transparente por defecto. Sobre líneas, tramas o imágenes, **un velo blanco al 50 % sin borde, ceñido a las letras.** Que la hoja no se llene de recuadros blancos opacos («hay muchos recuadros blancos»). Las cifras de cota van opacas por defecto (`acotar-planos`) y pasan al velo si la hoja se llena de recuadros. [LdE; Usuario]
- **Cotas de nivel sueltas** (terreno, aceras): un punto negro de 0,8 mm en el sitio exacto y el texto a su derecha sobre el velo. En planos de antes y después, las dos cotas juntas. [Usuario]
- **Coma decimal** en todo el juego (los nombres de tipo, con punto: es la convención del libro, §6). Las unidades sobreviven a las mayúsculas: «kPa» salió «KPA»; escribe «kN/m²» y revisa. [Práctica]
- **Dos verdes distintos:** el **de dibujo** del libro, RGB 0,128,64, para títulos y textos verdes; y el **corporativo** del logotipo, informes y portadas, ≈ RGB 6,87,72 (#065748; en un PDF del estudio se midió 7,87,72). Compruébalo contra el logotipo oficial si importa. [LdE; Práctica]
- **Colores de dibujo** [LdE]: rojo 192,0,0; azul 0,0,225; gris 128; naranja 255,128,64; amarillo 255,225,0.
- **Plumillas:** la tabla del LdE por escala está en la referencia (§5.5). **La tabla de grosores por escala no se edita por API**: es tarea de la plantilla. Comprueba en el PDF que la jerarquía de grosores existe (ver `planos-laminas`). [LdE]
- **Estilos de objeto:** muros proyección 1 y corte 2, negro; ventanas en negro con marco y montante (donde van los barridos) en gris 192; `<Derribado>` negro de trazos; `<Más allá>` y `<Líneas ocultas>` en gris 192. [LdE]
- **Líneas de acabado** de color pegadas a la cara del paramento (`ACA-Acabado …`): alicatado cian, enfoscado rojo, monocapa violeta, yeso verde, aplacado salmón, madera marrón. En baños, la línea cian discontinua «AL» a lo largo de las paredes alicatadas. [LdE; Práctica]
- **Plantas de albañilería y distribución: sin colores de filtro,** con los muros por el material de cada capa. [LdE; Usuario]

## 6. Tipos, materiales y etiquetas

- **Muros, suelos, techos y cubiertas:** `<CLASE>-<núcleo>-<datos opcionales>-(<capas ext.>//<capas int.>)=<total>cm`. Grosores en cm con punto decimal; clase en mayúsculas; `//` solo en elementos completos de exterior a interior. Ejemplo: `INT-PYL-(1.5placa yeso+7aisl+1.5placa yeso)=10cm`. Se pueden crear clases nuevas con el mismo criterio (`EXI-` para los muros de un levantamiento). El usuario eligió esta nomenclatura y no la de otro estudio (RLA). [LdE; Usuario]
- **Materiales** `AG_<descripción>`. **Familias** `<CAT>-<descriptor>` y tipo `<medidas>` (`VEN-2 hojas-Abatible : 150x150 cm`). [LdE]
- **Parámetros obligatorios del tipo:** Marca de tipo (código del plano) y Comentarios de tipo (la clase: FCH, INT…). Además, función del tipo (exterior, interior, retención) y de cada capa. Quita la nota clave de relleno `Md.1` heredada. [LdE]
- **Catálogo:** «una letra + dos números». Mxx muros (rectángulo), Sxx suelos (triángulo), Axx acabados de paramento, TExx techos, Cxx cubiertas. El código es fijo en el catálogo del estudio: no se recodifica por proyecto. Las leyendas de la v8 usan otro sistema (GP-01, AL…): decide uno por proyecto. [LdE]
- **Etiqueta de acabados de la estancia:** recuadro rojo con Sxx arriba y Axx | TExx abajo, bajo la etiqueta de habitación en las plantas de distribución, con la tabla «ACABADOS» y la «SIMBOLOGÍA DE ACABADOS». Si falta un elemento, campo en blanco. Sin directriz: la que no cabe limpia se quita y sus códigos van a una nota «Sin etiqueta por su tamaño». [LdE; Práctica]
- **Carpinterías:** círculo **E** rojo (exterior; las ventanas siempre E), **I** verde (interior), **C** azul (cerrajería). Comprueba si la etiqueta añade la letra: si la añade, la marca es «01»; si no, «E01». Si hace falta distinguir piezas, marca de ejemplar única. [LdE; Práctica]
- **Habitaciones:** «Nombre + Superficie». «Dormitorio principal» (no «ppal.»), «Dormitorio #» solo si hay varios, «Aseo» sin ducha ni bañera, «Pasillo-Circulación», «Instalaciones». [LdE]

## 7. Tablas y leyendas

- **Tablas en la hoja:** sin rejilla, contorno fino, **una fila vacía antes de los datos**; título `CENT_GOT_Verde-4 mm`, cabecera 2,5 mm, cuerpo 2 mm. Las de medición, con cabeceras agrupadas «LOCALIZACIÓN / ESTADO DE MEDICIONES». Una tabla partida en columnas lleva un solo título. Dos viviendas, en tablas lado a lado bajo un título. [LdE; Práctica]
- **Superficies útiles por vivienda:** Portal / Puerta / Número / Nombre / Departamento / Perímetro / Superficie útil. Útiles de las habitaciones; construidas de las áreas. [LdE]
- **Leyendas:** arquitectura, «LEYENDA …» en gris, negrita y mayúsculas; instalaciones, «SIMBOLOGÍA DE …» subrayado. Debajo, NOTAS u OBSERVACIONES numeradas. Adapta las notas de la plantilla al proyecto: quita lo que no aplica y las marcas comerciales sin decidir. [LdE]
- **Instalaciones:** agua fría azul, ACS roja, recirculación naranja, pluviales gris azulado, residuales rojo. Saneamiento: continua por encima del forjado, discontinua colgado (≥ 1 %), trazo y punto enterrado (≥ 2 %). Arqueta: cuadrado; con X registrable; con X y cuadrado interior, sifónica. [LdE]

## 8. Contenidos tipo

- **Fases en planos de reforma:** existente en poché gris, derribo discontinuo, obra nueva marcada, con su leyenda. En planos de trabajo, cada subfase de un color y las fases posteriores en medio tono. [Práctica]
- **Límite entre viviendas:** línea fina de trazo y punto, unos 4 mm dentro de la primera unidad, nunca una franja blanca («la línea que divide las viviendas ahora es blanca y gorda y da lugar a error»). [Usuario]
- **Memoria de carpinterías:** fichas en cuadrícula como la leyenda `ARQ-CARPINTERÍA EXTERIOR`. De arriba abajo: círculo con el código; alzado **visto desde fuera**, acotado (ancho, alto, antepecho), apoyado en una línea «NPT» discontinua gris; separador; texto gris con título en negrita `E01_USO`, «Ventana exterior: A x H mm», hojas y apertura, persiana, «Cant.: n ud», material, acabado y RAL, Um, vidrio con g y Ug (y Uw). Al lado, la tabla de carpinterías y la mosca. [LdE; Práctica]
- **Símbolo de apertura en alzado** («todas las ventanas tienen los abatimientos al revés»): las líneas salen de las **bisagras** y el **vértice apunta al lado que abre** (la manilla). Abatible hacia dentro: vértice arriba. Oscilobatiente: los dos triángulos. Dos hojas: los vértices se encuentran en el centro. Puertas: el vértice a la manilla. Explícalo en una nota de la hoja. [Usuario]
- **Memoria de muros** (y suelos, techos, cubierta): una ficha por tipo, **dibujada** (no con muros de muestra, que se medirían): planta a 1:10 y sección a 1:20 con las capas acotadas, código Mxx, nombre del tipo, capas de exterior a interior con material y grosor, uso, texto de pliego, prestaciones (U, EI, dBA si se conocen) y los m² medidos por fase. «Quiero el detalle de los muros de albañilería, con sus capas, en planta y en sección». [Usuario]
- **Detalles constructivos** a 1:20 y 1:5–1:10, con llamadas que dan el número de plano y de detalle, y mosca. [LdE]
- **Instalaciones:** una planta por instalación, con leyenda y notas; esquema unifilar y esquemas de principio. [LdE]
- **Plano resumen (A.00):** axonometría explotada por fases, secuencia de obra, plazo por fase en barras y coste por fase como estimación, con los trabajos de cada fase («maquetado perfecto, estilo agoin»). [Usuario]

## 9. Hojas hechas fuera de Revit

Las hojas que no necesitan el modelo (bordes, remates, comparativas) pueden hacerse con matplotlib o HTML, con el mismo aspecto: A3, Century Gothic, verde corporativo, franja de cajetín a la derecha, rótulos sobre velo al 50 % y ninguna etiqueta cruzando marcos o carpinterías. Century Gothic no tiene ✔ ● ○: usa DejaVu Sans para esos glifos. [Práctica]

## 10. Antes de emitir

1. Información de proyecto completa (autor, fecha, versión corta, código), norte, revisión activa con las nubes etiquetadas y fecha DD/MM/AAAA. [LdE]
2. Avisos de Revit revisados y rutinas de unión de suelos y muros. [LdE]
3. Cada hoja como imagen a 150 ppp: desbordes del cajetín, títulos largos, textos que se pisan o pisan símbolos o muros, restos del levantamiento o de versiones anteriores, hojas medio vacías, leyendas incompletas. [Práctica]
4. En juegos grandes, revisión independiente por bloques de hojas, con una tabla de gravedad (ver `planos-laminas`). [Práctica]

## Relacionadas

- `planos-laminas`: producir, exportar y revisar las láminas.
- `acotar-planos`: cómo acotar.
- `decisiones-cliente`: hojas de decisión, de dudas y de trabajo.
- `revit-automatizacion`: lo que no se puede hacer por API (plumillas, transferir normas, etiquetas).
