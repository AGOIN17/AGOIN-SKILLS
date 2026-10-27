"""Imprime a PDF desde un programa de Windows con el diálogo «Imprimir» clásico, usando SOLO «Microsoft Print to PDF».

- Solo pulsa Aceptar después de comprobar que la impresora elegida es «Microsoft Print to PDF» y que su tipo dice PDF.
  Si algo no cuadra (otra impresora, diálogo distinto, control que no aparece), cancela y devuelve el motivo.
- Solo busca diálogos del proceso del programa (y del proceso de impresión de Windows, splwow64.exe).
- No sobrescribe un PDF que ya exista, salvo con sobrescribir=True; entonces guarda con un nombre temporal y sustituye el
  archivo solo si la impresión ha salido bien.

Probado con Robot Structural Analysis 2027 en Windows 11 en español (octubre de 2026). Necesita pywinauto (y psutil).

Uso:
    from imprimir_pdf import imprimir_pdf
    resultado = imprimir_pdf(hwnd_ventana_principal, r"D:/ruta/salida.pdf")     # "ok" o el motivo del fallo
"""
import os
import time

from pywinauto import Application, Desktop

PDF = "Microsoft Print to PDF"
TITULOS_IMPRIMIR = ("Imprimir", "Print")
TITULOS_GUARDAR = ("Guardar impresión como", "Save Print Output As")
ID_COMBO_IMPRESORA = 1139       # diálogo de impresión clásico de Windows (PrintDlg)
ID_TIPO_IMPRESORA = 1098        # texto «Tipo:» de la impresora elegida
ID_NOMBRE_ARCHIVO = 1001        # campo de nombre en «Guardar impresión como»


def _buscar(e, nombre=None, tipo=None, auto=None, prof=8):
    """Primer descendiente (búsqueda en anchura) con ese nombre, tipo de control y AutomationId."""
    cola = [(e, 0)]
    while cola:
        x, n = cola.pop(0)
        ei = x.element_info
        if x is not e and (nombre is None or ei.name == nombre) and (tipo is None or ei.control_type == tipo) \
                and (auto is None or ei.automation_id == auto):
            return x
        if n < prof:
            try:
                cola.extend((c, n + 1) for c in x.children())
            except Exception:
                pass
    return None


def _pids_permitidos(pid):
    pids = {pid}
    try:
        import psutil
        pids |= {p.pid for p in psutil.process_iter(["name"]) if (p.info["name"] or "").lower() == "splwow64.exe"}
    except ImportError:
        pass
    return pids


def _ventanas(pids):
    return [w for w in Desktop(backend="uia").windows() if w.process_id() in pids]


def _dialogo_imprimir(principal, pid, espera):
    fin = time.time() + espera
    while time.time() < fin:
        candidatos = [c for c in principal.children() if c.element_info.control_type == "Window"]
        candidatos += [w for w in _ventanas({pid}) if w.element_info.class_name == "#32770"]
        for c in candidatos:
            if c.window_text() in TITULOS_IMPRIMIR:
                return c
        time.sleep(0.25)
    return None


def _dialogo_guardar(pid, espera):
    """Diálogo «Guardar impresión como» del programa o del proceso de impresión; suele ir anidado en la ventana de progreso."""
    fin = time.time() + espera
    while time.time() < fin:
        for x in _ventanas(_pids_permitidos(pid)):
            if x.window_text() in TITULOS_GUARDAR:
                return x
            if x.element_info.class_name == "#32770":
                for t in TITULOS_GUARDAR:
                    y = _buscar(x, nombre=t, tipo="Window", prof=2)
                    if y is not None:
                        return y
        time.sleep(0.5)
    return None


def _sigue_abierto(d):
    try:
        return d.is_visible()
    except Exception:
        return False


def _cancelar(d):
    """Pulsa Cancelar; si no lo encuentra, Esc. Devuelve True si el diálogo se ha cerrado."""
    b = _buscar(d, auto="2", tipo="Button")                      # IDCANCEL
    try:
        if b is not None:
            b.invoke()
        else:
            Application(backend="win32").connect(handle=d.handle).window(handle=d.handle).type_keys("{ESC}")
    except Exception:
        pass
    for _ in range(20):
        if not _sigue_abierto(d):
            return True
        time.sleep(0.25)
    return False


def _abortar(d, motivo):
    return motivo + (": cancelado" if _cancelar(d) else ": NO SE HA PODIDO CERRAR EL DIÁLOGO, revísalo a mano sin aceptar")


def imprimir_pdf(hwnd_principal, ruta, abrir_con="^p", espera=15, sobrescribir=False):
    """Abre el diálogo de impresión con el atajo `abrir_con`, elige «Microsoft Print to PDF», lo comprueba y guarda en `ruta`."""
    ruta = os.path.abspath(ruta)
    if os.path.exists(ruta) and not sobrescribir:
        return "ya existe %s: no se sobrescribe (usa otro nombre o sobrescribir=True)" % ruta
    destino = ruta + ".tmp.pdf" if os.path.exists(ruta) else ruta
    if os.path.exists(destino):
        return "ya existe el temporal %s: bórralo antes" % destino
    principal = Desktop(backend="uia").window(handle=hwnd_principal).wrapper_object()
    pid = principal.process_id()
    w = Application(backend="win32").connect(handle=hwnd_principal).window(handle=hwnd_principal)
    w.set_focus()
    w.type_keys(abrir_con, set_foreground=True)
    d = _dialogo_imprimir(principal, pid, espera)
    if d is None:
        return "no se abre el diálogo Imprimir"
    try:
        dw = Application(backend="win32").connect(handle=d.handle).window(handle=d.handle)
        cb = dw.child_window(control_id=ID_COMBO_IMPRESORA, class_name="ComboBox")
        if PDF not in cb.item_texts():
            return _abortar(d, "no está instalada «%s»" % PDF)
        cb.select(PDF)
        time.sleep(1.0)
        tipo = dw.child_window(control_id=ID_TIPO_IMPRESORA, class_name="Static").window_text()
        elegida = cb.selected_text()
    except Exception as ex:
        return _abortar(d, "el diálogo no es el clásico esperado (%s)" % str(ex)[:120])
    if elegida != PDF or "PDF" not in tipo:
        return _abortar(d, "la impresora no ha cambiado a PDF")
    ok = _buscar(d, auto="1", tipo="Button")                     # IDOK (Aceptar)
    if ok is None:
        return _abortar(d, "no se encuentra el botón Aceptar")
    ok.invoke()                                                  # solo con la impresora PDF comprobada
    g = _dialogo_guardar(pid, 30)
    if g is None:
        return "no aparece el diálogo para guardar el PDF (mira la cola de impresión)"
    gw = Application(backend="win32").connect(handle=g.handle).window(handle=g.handle)
    campo = gw.child_window(control_id=ID_NOMBRE_ARCHIVO, class_name="Edit")
    campo.set_edit_text(destino)
    time.sleep(0.3)
    if campo.window_text() != destino:                           # si no lo ha tomado, se teclea
        campo.set_focus()
        campo.type_keys("^a{DEL}" + destino, with_spaces=True, set_foreground=True)
        time.sleep(0.3)
    guardar = _buscar(g, auto="1", tipo="Button")
    if guardar is None:
        return "no se encuentra el botón Guardar: revisa el diálogo a mano"
    guardar.invoke()
    fin = time.time() + 30
    while time.time() < fin and not (os.path.exists(destino) and os.path.getsize(destino) > 0):
        time.sleep(0.5)
    time.sleep(2)                                                # que termine de escribir
    if not (os.path.exists(destino) and os.path.getsize(destino) > 0):
        return "no se ha escrito el PDF"
    if destino != ruta:
        os.replace(destino, ruta)
    return "ok"
