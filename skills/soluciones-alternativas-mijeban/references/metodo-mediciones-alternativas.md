# Mediciones de las alternativas (desde los DWG, con BC3 sin precios)

El método general está en la skill `mediciones-presupuesto`. Aquí va lo que se hizo en Cigarral y se puede repetir.

## Antes de medir: fijar el criterio con preguntas numeradas

El usuario contestó «1a, 2a, 3a, 4a, 5a» a estas cinco preguntas en la fachada:
- a cinta corrida, descontando los huecos de más de 3 m²;
- lo que sale en alzado (planos A-04 a A-07), una vez por cara, desde el terreno dibujado hasta el arranque de la cubierta, con los hastiales completos;
- una partida por tipo con el paquete completo de la alternativa;
- la piedra aparte, separando la de la casa de la de jardín y plataforma;
- los paneles dibujados como carpintería se descuentan como hueco.

Después pidió revisar en planta («habrá zonas que añadir») y comparar con la licitación: «si son números comparables, lo estás haciendo bien». El resultado fueron 607,80 m² frente a 609,17 de la licitación. Las diferencias, que se compensan entre sí, se explicaron una a una.

## Medir desde el DWG

1. **Copia del DWG → DXF con accoreconsole** (`references/metodo-fichas.md`, apartado 2). Los DXF del proyecto pesan hasta 90 MB y van en metros con coordenadas UTM.
2. **Extrae una vez la geometría a un JSON ligero** (`scripts/med_extraer.py` para las vistas y `med_extraer_planta.py` para las plantas) y trabaja sobre él.
3. **Haz un piloto con una vista** (`med_piloto_w1.py`) y enséñalo con una imagen de cada paño coloreado, antes de medir todo.
4. **Trampas:**
   - capas de carpintería duplicadas: hay que deduplicarlas;
   - vistas en espejo respecto a la planta;
   - la piedra en bloques que se salen del muro no sirve para medir áreas: se mide con el contorno de las líneas;
   - restar máscaras no funciona si el terreno no tapa con un relleno.

## Comprobación de cada línea (orden del usuario: «comprueba siempre la línea de medición»)

En cada regeneración se comprueba automáticamente, y la generación se para si algo falla:
- que cada línea sale de su geometría de origen, recalculada;
- que unidades × longitud × altura da el parcial;
- que cada hueco descontado está dentro de su paño y mide más de 3 m²;
- que no hay líneas duplicadas ni a cero;
- que la suma de las líneas da la cantidad de los registros `~M` y `~D` del BC3;
- que el BC3 y las tablas del PDF tienen exactamente las mismas líneas.

Dile al usuario qué cubre esta comprobación: es de forma y de coherencia, y no sustituye a mirar el plano.

## BC3

- **Conjunto:** `scripts/bc3_conjunto.py` une los `lineas.json` de cada sistema en un solo FIEBDC-3 sin precios, con capítulos FAC# y CUB#. Después se relee y se compara.
- **Comprobador independiente:** `scripts/check_bc3.py` lee los bytes tal cual, sin reutilizar nada de los generadores.
- **Orden de regeneración:** fachadas → cubierta → BC3 conjunto → `check_bc3`.
- **Extraer la licitación:**
  - `scripts/lic_bc3.py` vuelca el BC3 a `lic.json`;
  - `lic_buscar.py` busca en ese JSON;
  - `pdf_buscar.py` busca en el PDF de mediciones.
  - Enlaza las versiones por el texto de las partidas, no por el código: el BC3 de Cigarral numeraba la albañilería como 06 y el PDF como 05.

## Hallazgos típicos en una licitación (Cigarral)

- Cumbrera medida como 7 largos de faldón (28,98 m) cuando son unos 81 m.
- El mismo borde lateral medido en dos partidas (112,56 m en cada una).
- Dos remates en el mismo alero.
- El frente del alero hacia el valle, sin medir.
- La piedra de los muros de sótano, cambiada por ladrillo de tejar (300,21 m²), con las líneas copiadas de la partida de muros de hormigón y sin huecos deducidos.
