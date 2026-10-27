# Plantilla de script de Dynamo (Python, PythonNet3) que modifica un modelo de Revit.
#   IN[0] = aplicar:  solo un «true» explícito aplica ("[true]", "true", [[true]]). Cualquier otra cosa simula.
#   OUT   = informe en texto: qué ha encontrado, qué ha hecho o haría, y los errores.
# Patrón de ALFERECES (MEP/mep_comun.py, dynamo/113_vecino_plaza.py), con la simulación hecha dentro de un TransactionGroup:
# la transacción se confirma de verdad (así salta el preprocesador de fallos y lo que Revit borra al confirmar) y después
# el grupo se deshace. Una simulación que deshace antes de confirmar puede decir «ok» y fallar en la ejecución real.
import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def es_verdadero(v):
    """Desenvuelve listas anidadas ([[true]] -> true). Solo True o el texto «true» cuentan: ni «false» ni [[false]]."""
    while not isinstance(v, (str, bool)) and hasattr(v, "__len__") and hasattr(v, "__getitem__"):
        if len(v) == 0:
            return False
        v = v[0]
    return v is True or str(v).strip().lower() == "true"


aplicar = es_verdadero(IN[0]) if IN else False
informe = ["MODO: " + ("APLICAR" if aplicar else "SIMULACIÓN"), "documento: " + doc.Title]
ERRORES = []


class SinAvisos(IFailuresPreprocessor):
    """Borra los avisos y deshace la transacción ante un error, sin abrir ningún diálogo.
    Un diálogo modal con una transacción de API abierta bloquea la llamada, y si alguien lo acepta a mano Revit
    puede cerrarse sin archivo de recuperación."""
    __namespace__ = "plantilla_sin_avisos"          # único por script: PythonNet no admite dos clases .NET iguales

    def PreprocessFailures(self, fa):
        for f in list(fa.GetFailureMessages()):
            if f.GetSeverity() == FailureSeverity.Warning:
                fa.DeleteWarning(f)
            else:
                ERRORES.append("{} · ids {}".format(f.GetDescriptionText(), [i.Value for i in f.GetFailingElementIds()]))
                return FailureProcessingResult.ProceedWithRollBack
        return FailureProcessingResult.Continue
    # Variante SOLO para un fallo concreto cuya resolución conoces (p. ej. «no es posible mantener unidos»: la resolución
    # por defecto es separar la unión): si f.HasResolutions(), fa.ResolveFailure(f), anotarlo y devolver ProceedWithCommit.
    # Nunca aceptes en bloque las resoluciones por defecto: en otro proyecto borraron una fachada levantada y sus cotas.
    # Cuenta los elementos antes y después para ver que no ha desaparecido nada.


def transaccion(nombre):
    t = Transaction(doc, nombre)
    op = t.GetFailureHandlingOptions()
    op.SetFailuresPreprocessor(SinAvisos())
    op.SetClearAfterRollback(True)                  # sin diálogo al deshacer por error
    op.SetForcedModalHandling(False)
    t.SetFailureHandlingOptions(op)
    t.Start()
    return t


# ------------------------------------------------------------------ 1. leer y decidir (sin transacción)
# objetivo = doc.GetElement(ElementId(123456))
# informe.append("antes: ...")

# ------------------------------------------------------------------ 2. cambiar
TransactionManager.Instance.ForceCloseTransaction()   # cierra la transacción que Dynamo pueda tener abierta
grupo = TransactionGroup(doc, "AGOIN · descripción corta del cambio")
grupo.Start()
t = transaccion("AGOIN · descripción corta del cambio")
try:
    # ... cambios ...
    doc.Regenerate()
    estado = t.Commit()
    if estado != TransactionStatus.Committed:
        raise Exception("la transacción no se ha confirmado ({}): {}".format(estado, ERRORES[-3:]))
    # ... comprobar leyendo el modelo lo que ha quedado (y contar elementos), y anotarlo en el informe ...
    if aplicar:
        grupo.Assimilate()
        informe.append("aplicado")
    else:
        grupo.RollBack()
        informe.append("simulación: confirmado dentro del grupo y deshecho")
except Exception as ex:
    if t.HasStarted() and not t.HasEnded():
        t.RollBack()
    if grupo.HasStarted() and not grupo.HasEnded():
        grupo.RollBack()
    informe.append("ERROR: {}".format(str(ex)[:400]))

# No llames a doc.Regenerate() fuera de una transacción después de confirmar: lanza una excepción y,
# si la capturas con un RollBack, parecerá que falló algo que sí se aplicó.
OUT = informe + ERRORES
