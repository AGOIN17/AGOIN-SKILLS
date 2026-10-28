---
name: optimizar-trabajo
description: "[OPTIMIZACIÓN] Cómo trabajar rápido y barato en encargos largos de AGOIN sin perder calidad: cuándo y cómo usar subagentes (cuántos, qué modelo, carpeta propia, salida que se junta con un script), procesos largos y esperas en segundo plano, cadenas de regeneración con comprobación final, scripts que se pueden repetir sin duplicar, ahorrar clics y tiempo al usuario, y retomar tras una compactación o un límite de sesión. Úsala al planificar un trabajo grande, antes de lanzar varios agentes o un proceso de más de unos minutos, al montar un flujo que se regenera muchas veces, y cuando una sesión se corte o se compacte."
metadata:
  etiquetas: "OPTIMIZACIÓN"
---

# Trabajar rápido sin perder calidad

En los proyectos de AGOIN los encargos duran días y se regeneran decenas de veces. Lo caro no suele ser pensar: es repetir trabajo, esperar mal, lanzar demasiados agentes y rehacer lo que se rompió sin verlo. Estas reglas salen de lo que pasó en ALFERECES y en CHIVERO.

## 1. Subagentes

- **Pocos y bien acotados.** Un agente que revisa láminas o cruza una base de precios gasta de 300.000 a 550.000 tokens. Con 5–7 a la vez se llegó al límite de sesión, y con unos 14 grandes, al de gasto mensual.
  - Prefiere 2 o 3 agentes de modelo intermedio con un encargo cerrado (una lámina ya exportada a PDF y la lista de cambios) antes que dejarles explorar.
  - Modelo rápido para lo mecánico, intermedio para buscar y revisar, el más potente solo para el juicio fino.
- **Encargo en español,** con el porqué, las rutas exactas, lo que no deben tocar y que respondan en español.
- **Cada agente escribe en su propia subcarpeta** del scratchpad y con nombres únicos, nunca en la raíz. Un agente dejó `q.py` y `c.py` en la raíz y otros seis podían haberlos pisado.
- **Fija el formato de salida para juntarlo con un script:**
  - el mismo orden que la entrada;
  - un grado cerrado (exacta / parecida / aproximada / sin equivalente);
  - la cuenta de cada ajuste;
  - al final, «las N con más dudas»;
  - si falta un dato, `null` y no `0`.
  - Así se juntaron 246 partidas de siete agentes sin reescribir nada a mano, y sin desviaciones falsas del −100 %.
- **Revisor independiente:**
  - que no ejecute los scripts que reescriben resultados: que importe sus funciones;
  - que no modifique el proyecto;
  - que entregue aparte sus propios scripts de comprobación.
  - Así encontró errores reales en el cálculo de zapatas sin estropear los resultados.
- **Auditoría de un juego de planos:** una o dos láminas por agente, comparadas con el visado y con la lista de cambios. Cada problema con su zona en mm, gravedad, por qué está mal, cómo arreglarlo y un recorte comparado. Después los juntas y priorizas tú.
- **Para leer mucho material** (un expediente por años, transcripts, carpetas enteras), reparte por bloques y pide que cada entrada diga si se leyó el documento o solo se deduce del nombre.
- **Repartos que funcionaron:** tres agentes para mapear partidas a una base de precios, por capítulos; cinco revisores de un juego de 65 hojas, por bloques. Cada uno con una salida fija (tabla o JSON en una ruta) y la orden expresa de no tocar nada fuera.

## 2. Procesos largos y esperas

- **Avisa del tiempo** de un render o un cálculo largo antes de lanzarlo. Si ocupa un programa del usuario (regenerar láminas en su Revit, 10 a 25 minutos), pídele que no lo use mientras tanto; suele contestar «dale caña, yo paro de usarlo».
- **Lanza las regeneraciones largas en segundo plano y espera el aviso de fin,** sin consultar a cada rato. Si la espera se agota, relanza solo la espera, no el proceso.
- **En Claude Code, las esperas largas van en una tarea en segundo plano** (`run_in_background`) que comprueba la condición en bucle.
  - No lances procesos con `&`: quedan duplicados sin control. Una cadena se ejecutó dos veces y hubo que matar procesos a mano.
  - El `sleep` suelto está bloqueado y Monitor caduca a los 30 minutos (comprobado en octubre de 2026; puede cambiar con la versión).
- **Un script de imagen pesado que puede pasar de 2 minutos va en segundo plano.** Rasteriza una sola vez por planta (150 ppp) y reutiliza.
- **Las tareas en segundo plano tienen un límite de 1 hora** por defecto: trocea o reanuda.
- **Los procesos que se pueden cortar se hacen reanudables:** un render que salta los fotogramas ya hechos, una cadena que sabe en qué paso iba.

## 3. Cadenas de regeneración

- **Un único script por flujo guarda el orden de regeneración.** Las piezas dependen unas de otras (saneamiento, luego fontanería, luego climatización; mediciones, luego ciego, luego BC3). Se saltó un paso y salieron pasatubos para rutas antiguas.
- **La cadena termina con una comprobación que falla de forma visible:** «TODOS LOS ENTREGABLES COINCIDEN», «0 errores en la prueba en vivo». Si no lo dice, no ha terminado bien.
- **Todos los entregables de una ronda llevan la misma hora.** Así no hay versiones cruzadas.
- **Deja escrito cómo se regenera todo** en el archivo de contexto del proyecto (`00_PLAN.md` o similar): orden, scripts y qué se exporta.
- **Una sola fuente para los datos que usan muchos scripts** (por ejemplo, una tabla de unidades con cotas y fases en un JSON). Si dos scripts guardan el mismo dato, acabarán diciendo cosas distintas.
- **Marca como obsoletos los generadores antiguos** cuando el modelo ya va por delante de ellos («no volver a lanzar…»), en el propio script y en el archivo de plan.
- **Para ver errores sin esperar la regeneración completa,** haz una pasada de prueba que lo deshace todo al final (unos 2 minutos frente a 8). Conoce antes qué borra tu compositor: pasarle una lista de hojas borraba el juego entero.

## 4. Scripts que se pueden repetir

- **Lo que un script crea o dibuja se marca** (prefijo en el estilo o el tipo, comentario «PE-…:», una marca) y, antes de volver a dibujar, **se borra por esa marca.** No dependas de listas de ids: fallan tras un cierre de Revit, que además reutiliza los números.
- **Parámetro `aplicar`** en todo lo que escribe: primero simula y devuelve un informe, luego aplica (ver `revit-automatizacion`).
- **Entregables grandes** (vídeo, PDF, BC3): escribe con un nombre temporal y renombra al terminar. Windows no deja sobrescribir un archivo abierto, ni por tu script ni por el usuario.
- **Reutiliza módulos propios** entre documentos del mismo tipo (maquetación de PDF, cliente de Dynamo, lectura de PDF de planos) en vez de reescribirlos.
- **Un script que puede cerrar el programa** (bucles de creación en Revit) guarda antes.

## 5. Ahorrar tiempo al usuario

- **Si el usuario puede sacar un dato exacto en un minuto** (una superficie en Revit, una longitud en CAD), pídeselo antes de pasar horas estimándolo.
- **Lanzadores de doble clic** (`.bat`) para lo que repite: abrir Revit con Dynamo local, abrir la web interna de revisión.
- **Una espera en segundo plano que detecte cuándo está listo el programa** y lance sola la cadena pendiente, **solo si el usuario ha autorizado esa cadena concreta**, con copia y simulación hechas, y sin cerrar ni guardar por tu cuenta. El usuario preguntó «¿puedes empezar tú sin yo tocar nada?»; la espera consultaba Dynamo cada 30 s y lanzó la cadena autorizada en cuanto lo abrió.
- **Archivos que el usuario tiene abiertos:** mira antes qué entregables están bloqueados, regenera el resto y pídele en un solo mensaje que cierre esos archivos concretos.
- **Copias ligeras de entrada** de lo pesado: un vídeo de 1 GB con una versión de unos 200 MB, y otra de menos de 30 MB para mensajería.

## 6. Retomar el trabajo

- **Antes de cortar o compactar, el archivo de contexto del proyecto tiene que estar al día:** estado, decisiones, pendientes y cómo regenerar. Actualízalo sin que te lo pidan.
- **Al retomar, lee primero ese archivo y el registro de cambios.** No te fíes del resumen de compactación para cifras, decisiones ni idioma: los resúmenes van en inglés y el inglés se cuela en las respuestas.
- **Si hace falta una sesión nueva** (por ejemplo, tras instalar un servidor MCP, que solo se carga al arrancar), da al usuario la frase exacta para pegar: «Lee los archivos de seguimiento y continúa desde el punto pendiente de 00_PLAN.md».
- **Tras un límite de sesión,** no relances a ciegas lo que estaba en marcha: mira qué terminó, qué archivos quedaron a medias y qué hay que repetir.

## 7. Si el usuario pregunta por su consumo

- Los registros locales solo cuentan este equipo; el límite se comparte entre todos los aparatos de la cuenta. Para verlo por aparato hace falta telemetría (OpenTelemetry) o una cuenta por equipo.
- Para gastar menos: `/clear` o `/compact` entre tareas distintas, un modelo más ligero para lo mecánico y subagentes para las búsquedas pesadas.
- Los precios por token salen de la documentación oficial (la skill `claude-api`, si está disponible), nunca de memoria.
