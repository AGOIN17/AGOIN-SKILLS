"""Maneja la app nativa de Gemini para Windows (Electron) por UI Automation.

La app bloquea el modo de depuración de Chromium, así que se usa la
accesibilidad de Windows (lo que usan los lectores de pantalla): los botones
se pulsan por UI Automation, la petición se escribe con ValuePattern y los
cuadros de archivo con WM_CHAR. No mueve el ratón ni roba el foco.

Lecciones de la primera prueba (09/11/2026):
- Chromium no publica el árbol de la página hasta que un cliente lo pide:
  la primera consulta puede salir vacía (find_editor reintenta).
- En un chat vacío no hay botón «New Chat».
- «Upload & tools» es un botón de menú: se pulsa con Expand, no con Invoke.
  La opción del menú se llama «Files».
- El cuadro «Abrir/Guardar como» cuelga de la ventana de Gemini en UIA.
- El cuadro de archivo ignora WM_SETTEXT/ValuePattern: hay que teclear con
  WM_CHAR. Si no, guarda con el nombre propuesto y pide reemplazar.
- Las miniaturas adjuntas se reconocen por su botón «close attachment».
- La barra lateral abierta tapa la caja de texto con la ventana estrecha.
- Minimizada, la página se encoge: desaparecen botones («New Chat») y la
  captura sale vacía.
- Fuera de la pantalla (o tapada del todo) Chromium deja de pintar y los
  menús no se abren. Truco: restaurarla dejando asomar 2 px en el borde
  izquierdo del escritorio, «siempre encima» mientras trabaja. Windows no deja
  restaurar fuera de pantalla con SetWindowPlacement (la recoloca): se
  restaura y se mueve con SetWindowPos en el mismo instante.
- HWND_TOPMOST (-1) hay que pasarlo como HWND: como int de 32 bits falla.
- Idiomas (comprobado el 09/11/2026 con la app en inglés y la web en español):
  los nombres de los botones cambian con el idioma de la cuenta de Google. Por
  eso se usan señales que no dependen de él: clases (ql-editor, etiquetas de
  respuesta), la fila de botones de la respuesta (solo aparece al terminar),
  el botón de enviar (aparece al subir un adjunto), el enlace de «conversación
  nueva» por su URL y el nombre del modelo (Flash/Pro). En español el menú
  «Mostrar más opciones» NO ofrece «Rehacer con Pro».
- La barra superior nativa de la app tiene su propio «Menú principal»
  (automation_id «btn-menu»): no es el de la página y se ignora.
- El selector de modo («Open mode picker, currently ...») ofrece 3.5 Flash-Lite,
  3.6 Flash, 3.1 Pro y 4 Argon. Cada imagen tiene «Show more options» →
  «Redo with Pro». La URL del chat sale del ValuePattern del documento y los
  enlaces de la barra lateral llevan la suya.
"""
import subprocess
import ctypes
import os
import re
import time
from ctypes import wintypes

import psutil
from pywinauto.uia_defines import get_elem_interface

APP_DIR = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Gemini").lower()

# Nombres en inglés y en español. Los marcados «sin ver» son traducciones
# probables: si fallan, la herramienta «diagnostico» enseña los reales.
N_NEW_CHAT = {"New Chat", "New chat", "Nueva conversación", "Nuevo chat", "Chat nuevo"}
N_SEND = {"Send message", "Enviar mensaje"}
N_STOP = {"Stop response", "Stop", "Detener respuesta", "Detener la respuesta", "Detener"}  # ES sin ver
N_UPLOAD = {"Upload & tools", "Subidas y herramientas"}
N_UPLOAD_FILES = {"Files", "Archivos", "Upload files", "Subir archivos"}  # + «Subir archivos. …»
N_TEMP = {"Temporary chat", "Chat temporal", "Conversación temporal"}  # ES sin ver
N_CLOSE_SIDEBAR = {"Close sidebar", "Cerrar barra lateral"}
N_MAIN_MENU = {"Main menu", "Menú principal"}
N_MORE = {"Show more options", "Mostrar más opciones", "More options", "Más opciones"}
N_PICKER = ("Open mode picker", "Abrir selector de modo")
NATIVE_IDS = {"btn-menu"}  # botones de la barra nativa de la app, no de la página
CLS_RESPONSE_LABEL = "screen-reader-model-response-label"
CLS_EDITOR = "ql-editor"


class GeminiError(RuntimeError):
    pass


# --------------------------------------------------------------- ventana

def _top_windows(cls, pid=None, exe_prefix=None):
    """Ventanas de primer nivel por clase y proceso con EnumWindows.

    No se usa Desktop().windows(): pregunta por UIA a todas las ventanas y una
    colgada (la Configuración de Windows, 09/11/2026) lo bloqueó minutos y
    acabó diciendo que Gemini no estaba abierta."""
    u32 = ctypes.windll.user32
    found = []
    proto = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def cb(h, _):
        buf = ctypes.create_unicode_buffer(64)
        u32.GetClassNameW(h, buf, 64)
        if buf.value != cls:
            return True
        p = wintypes.DWORD()
        u32.GetWindowThreadProcessId(h, ctypes.byref(p))
        if pid is not None and p.value != pid:
            return True
        if exe_prefix is not None:
            try:
                if not psutil.Process(p.value).exe().lower().startswith(exe_prefix):
                    return True
            except Exception:
                return True
        t = ctypes.create_unicode_buffer(256)
        u32.GetWindowTextW(h, t, 256)
        found.append((h, t.value))
        return True

    u32.EnumWindows(proto(cb), 0)
    return found


def _wrap(hwnd):
    """Envoltorio UIA de una ventana concreta (ElementFromHandle, sin recorrer el escritorio)."""
    from pywinauto.controls.uiawrapper import UIAWrapper
    from pywinauto.uia_element_info import UIAElementInfo
    return UIAWrapper(UIAElementInfo(hwnd))


def find_window():
    """Ventana principal de la app de Gemini (no la de Chrome ni la PWA)."""
    wins = _top_windows("Chrome_WidgetWin_1", exe_prefix=APP_DIR)
    if not wins:
        raise GeminiError("La app de Gemini no está abierta.")
    main = [h for h, t in wins if t == "Gemini"] or [h for h, t in wins if t]
    if not main:
        raise GeminiError("La app de Gemini no tiene ventana principal (¿está en la bandeja del sistema?).")
    return _wrap(main[0])


def _descendants(root, **crit):
    try:
        return root.descendants(**crit)
    except Exception:
        return []


def find_editor(w, timeout=10):
    t0 = time.time()
    while True:
        for e in _descendants(w, control_type="Edit"):
            if CLS_EDITOR in (e.element_info.class_name or ""):
                return e
        if time.time() - t0 >= timeout:
            raise GeminiError("No encuentro la caja de texto de Gemini.")
        time.sleep(0.5)


SW_SHOWNOACTIVATE, SW_SHOWMINNOACTIVE = 4, 7
_NOSIZE, _NOMOVE, _NOZORDER, _NOACTIVATE = 0x1, 0x2, 0x4, 0x10
_TOPMOST, _NOTOPMOST = wintypes.HWND(-1), wintypes.HWND(-2)
_u32 = ctypes.windll.user32


class _WP(ctypes.Structure):
    _fields_ = [("length", wintypes.UINT), ("flags", wintypes.UINT), ("showCmd", wintypes.UINT),
                ("ptMin", wintypes.POINT), ("ptMax", wintypes.POINT), ("rc", wintypes.RECT)]


class _MI(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT), ("rcWork", wintypes.RECT),
                ("dwFlags", wintypes.DWORD)]


_u32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int,
                              ctypes.c_int, ctypes.c_int, wintypes.UINT]
_u32.GetWindowPlacement.argtypes = [wintypes.HWND, ctypes.POINTER(_WP)]
_u32.SetWindowPlacement.argtypes = [wintypes.HWND, ctypes.POINTER(_WP)]
_u32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
_u32.IsIconic.argtypes = [wintypes.HWND]
_u32.MonitorFromPoint.argtypes = [wintypes.POINT, wintypes.DWORD]
_u32.MonitorFromPoint.restype = wintypes.HANDLE
_u32.GetMonitorInfoW.argtypes = [wintypes.HANDLE, ctypes.POINTER(_MI)]
_k32 = ctypes.windll.kernel32
_k32.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
_k32.CreateMutexW.restype = wintypes.HANDLE
_k32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
_k32.WaitForSingleObject.restype = wintypes.DWORD
_k32.ReleaseMutex.argtypes = [wintypes.HANDLE]
_k32.CloseHandle.argtypes = [wintypes.HANDLE]


def _placement(h):
    wp = _WP()
    wp.length = ctypes.sizeof(_WP)
    _u32.GetWindowPlacement(h, ctypes.byref(wp))
    return wp


def _set_placement(h, rc, show):
    wp = _placement(h)
    wp.showCmd = show
    wp.rc = wintypes.RECT(rc.left, rc.top, rc.right, rc.bottom)
    _u32.SetWindowPlacement(h, ctypes.byref(wp))


def _work_area_at(x, y):
    mi = _MI()
    mi.cbSize = ctypes.sizeof(_MI)
    _u32.GetMonitorInfoW(_u32.MonitorFromPoint(wintypes.POINT(x, y), 2), ctypes.byref(mi))
    return mi.rcWork


def _park_xy(width, top):
    """Posición en la que solo asoman 2 px por el borde izquierdo del escritorio."""
    wa = _work_area_at(_u32.GetSystemMetrics(76), top)  # SM_XVIRTUALSCREEN
    return wa.left - width + 2, wa.top


def rescue_window():
    """Si un proceso anterior murió con la ventana aparcada, la devuelve
    (minimizada y con una posición normal visible)."""
    try:
        w = find_window()
    except GeminiError:
        return False
    h = w.handle
    if _u32.IsIconic(h):
        return False
    r = w.rectangle()
    if r.right > _u32.GetSystemMetrics(76) + 50:
        return False
    _u32.SetWindowPos(h, _NOTOPMOST, 0, 0, 0, 0, _NOSIZE | _NOMOVE | _NOACTIVATE)
    wa = _work_area_at(0, 0)
    width, height = r.width(), r.height()
    _u32.ShowWindow(h, SW_SHOWMINNOACTIVE)
    _set_placement(h, wintypes.RECT(wa.left + 40, wa.top + 40, wa.left + 40 + width, wa.top + 40 + height),
                   SW_SHOWMINNOACTIVE)
    return True


class session:
    """Ventana lista para trabajar sin molestar.

    Si estaba minimizada, la restaura «aparcada» (solo asoman 2 px en el borde
    izquierdo, siempre encima para que Chromium la siga pintando) y al salir la
    vuelve a minimizar con su posición de siempre. Si estaba visible, trabaja
    donde está. Nunca la activa ni quita el foco.

        with session() as w: ...
    """

    def __init__(self, hidden=True, wait_turn=900):
        self.hidden = hidden
        self.wait_turn = wait_turn
        self.mutex = None

    def __enter__(self):
        # Turno entre procesos: varias sesiones de Claude Code pueden tener su propio
        # servidor «gemini», y dos a la vez sobre la misma ventana se estorban.
        self.mutex = _k32.CreateMutexW(None, False, "Local\\gemini-mcp-ventana")
        r = _k32.WaitForSingleObject(self.mutex, int(self.wait_turn * 1000))
        if r not in (0, 0x80):  # WAIT_OBJECT_0 o WAIT_ABANDONED (el anterior murió)
            _k32.CloseHandle(self.mutex)
            self.mutex = None
            raise GeminiError(f"Otra sesión lleva más de {self.wait_turn} s usando la app de Gemini.")
        try:
            return self._enter()
        except Exception:
            self._release()
            raise

    def _release(self):
        if self.mutex:
            _k32.ReleaseMutex(self.mutex)
            _k32.CloseHandle(self.mutex)
            self.mutex = None

    def _enter(self):
        self.w = ensure_window()
        h = self.w.handle
        self.was_min = bool(_u32.IsIconic(h))
        self.parked = False
        if self.was_min:
            rc = _placement(h).rc
            self.normal = wintypes.RECT(rc.left, rc.top, rc.right, rc.bottom)
            if self.hidden:
                _set_placement(h, self.normal, SW_SHOWNOACTIVATE)
                x, y = _park_xy(self.normal.right - self.normal.left, self.normal.top)
                _u32.SetWindowPos(h, _TOPMOST, x, y, 0, 0, _NOSIZE | _NOACTIVATE)
                self.parked = True
            else:
                _u32.ShowWindow(h, SW_SHOWNOACTIVATE)
            time.sleep(0.8)
        try:
            self._ready()
        except Exception:
            self.__exit__(None, None, None)  # deja la ventana como estaba
            raise
        return self.w

    def _ready(self):
        try:
            find_editor(self.w, timeout=3)
        except GeminiError:
            # La barra lateral abierta tapa la caja. Su «X» no responde por
            # accesibilidad; el botón «Main menu» sí la cierra.
            if find_button(self.w, N_CLOSE_SIDEBAR) is None:
                raise
            close_sidebar(self.w, settle=0)
            find_editor(self.w)
        return self.w

    def __exit__(self, *exc):
        try:
            h = self.w.handle
            if self.parked:
                _u32.SetWindowPos(h, _NOTOPMOST, 0, 0, 0, 0, _NOSIZE | _NOMOVE | _NOACTIVATE)
            if self.was_min:
                _u32.ShowWindow(h, SW_SHOWMINNOACTIVE)
                _set_placement(h, self.normal, SW_SHOWMINNOACTIVE)
        finally:
            self._release()
        return False


def ensure_window(timeout=40):
    """Ventana de Gemini; si la app está cerrada, la abre y espera."""
    try:
        w = find_window()
    except GeminiError:
        exe = os.path.join(APP_DIR, "Gemini.exe")
        if not os.path.isfile(exe):
            raise GeminiError("No está instalada la app de Gemini para Windows "
                              f"(no existe {exe}). Instálala y abre sesión con tu cuenta de Google.")
        subprocess.Popen([exe], close_fds=True)
        t0 = time.time()
        while True:
            time.sleep(1)
            try:
                w = find_window()
                break
            except GeminiError:
                if time.time() - t0 > timeout:
                    raise
        find_editor(w, timeout=timeout)
    return w


def find_button(w, names, timeout=0.0):
    t0 = time.time()
    while True:
        for b in _descendants(w, control_type="Button"):
            if (b.element_info.name or "").strip() in names and b.element_info.automation_id not in NATIVE_IDS:
                return b
        if time.time() - t0 >= timeout:
            return None
        time.sleep(0.3)


def main_document(w):
    for d in _descendants(w, control_type="Document"):
        if d.element_info.automation_id == "RootWebArea" and "Gemini" in (d.element_info.name or "") \
                and (d.element_info.name or "") != "Gemini":
            return d
    docs = [d for d in _descendants(w, control_type="Document")]
    if not docs:
        raise GeminiError("No encuentro la página de Gemini.")
    return docs[0]


def press(el):
    """Pulsa un control de Chromium: Invoke, desplegar o acción por defecto."""
    for how in ("invoke", "select", "expand", "toggle"):
        try:
            if how == "invoke":
                el.iface_invoke.Invoke()
            elif how == "select":
                el.iface_selection_item.Select()
            elif how == "expand":
                ec = el.iface_expand_collapse
                if ec.CurrentExpandCollapseState == 1:  # ya desplegado
                    return "expanded"
                ec.Expand()
            else:
                el.iface_toggle.Toggle()
            return how
        except Exception:
            continue
    try:
        get_elem_interface(el.element_info.element, "LegacyIAccessible").DoDefaultAction()
        return "default"
    except Exception as ex:
        raise GeminiError(f"No sé pulsar «{el.element_info.name}»: {ex}")


# --------------------------------------------------------------- respuestas

def response_labels(w):
    return [t for t in _descendants(w, control_type="Text")
            if CLS_RESPONSE_LABEL in (t.element_info.class_name or "")]


def _text_of(doc, el):
    """Texto de un elemento con saltos de línea (TextPattern del documento)."""
    try:
        tp = get_elem_interface(doc.element_info.element, "Text")
        rng = tp.RangeFromChild(el.element_info.element)
        return rng.GetText(-1)
    except Exception:
        parts = [t.element_info.name or "" for t in _descendants(el, control_type="Text")]
        return "".join(parts)


def response_container(label):
    """Sube desde la etiqueta «Gemini said» hasta el bloque de la respuesta."""
    el = label
    for _ in range(6):
        el = el.parent()
        if el is None:
            break
        if "presented-response-container" in (el.element_info.class_name or ""):
            return el
    return label.parent().parent()


# Líneas de botones y marcadores que no son texto de la respuesta.
_NOISE = {"￼", "Gemini said", "Copy", "Good response", "Bad response", "Redo", "Share & export",
          "Show more options", "More options", "Copiar", "Buena respuesta", "Mala respuesta",
          "Share image", "Copy image", "Download full size image", "Gemini ha dicho",
          "Compartir imagen", "Copiar imagen", "Descargar imagen a tamaño completo", "Rehacer",
          "Mostrar más opciones", "Previous version", "Next version"}


def last_response(w):
    labels = response_labels(w)
    if not labels:
        return ""
    container = response_container(labels[-1])
    txt = _text_of(main_document(w), container)
    noise = set(_NOISE) | {labels[-1].element_info.name or ""}
    noise |= {(b.element_info.name or "").strip() for b in _descendants(container.parent(), control_type="Button")}
    lines = []
    for ln in txt.replace("\r", "").split("\n"):
        s = ln.replace("\ufffc", "").rstrip()
        if s.strip() in noise or s.startswith(("View source details for citation", "Ver detalles de la fuente")):
            continue
        lines.append(s)
    return "\n".join(lines).strip()


def response_has_actions(w):
    """La fila de botones de la respuesta (copiar, rehacer…) solo aparece al terminar."""
    labels = response_labels(w)
    if not labels:
        return False
    block = response_container(labels[-1]).parent()
    return sum(1 for b in _descendants(block, control_type="Button") if b.element_info.name) >= 2


def is_generating(w):
    """Generando: botón de detener (EN/ES) o respuesta todavía sin su fila de botones."""
    if find_button(w, N_STOP) is not None:
        return True
    return bool(response_labels(w)) and not response_has_actions(w)


# --------------------------------------------------------------- acciones

def _chat_is_empty(w):
    if response_labels(w):
        return False
    return not any("user-query-label" in (t.element_info.class_name or "")
                   for t in _descendants(w, control_type="Text"))


def new_chat(w, temporary=False, _retry=False):
    """Chat nuevo. Con temporary=True, chat temporal (no queda en el historial)."""
    close_sidebar(w, settle=0)
    if not _chat_is_empty(w):
        b = find_button(w, N_NEW_CHAT, timeout=3)
        if b is not None:
            press(b)
        else:
            _new_chat_via_sidebar(w)
        t0 = time.time()
        while not _chat_is_empty(w) and time.time() - t0 < 8:
            time.sleep(0.3)
    if temporary:
        # Tras navegar, el botón tarda en aparecer (una sesión falló a la primera y fue bien al repetir).
        b = find_button(w, N_TEMP, timeout=10)
        if b is None and not _retry:
            time.sleep(1.0)
            return new_chat(w, temporary=True, _retry=True)
        if b is None:
            raise GeminiError("No encuentro el botón de chat temporal (" + " / ".join(sorted(N_TEMP))
                              + "). Usa la herramienta diagnostico para ver su nombre.")
        press(b)
        time.sleep(1.0)
    find_editor(w)


def _new_chat_via_sidebar(w):
    """Conversación nueva con el enlace de la barra lateral (se reconoce por su URL)."""
    if find_button(w, N_CLOSE_SIDEBAR) is None:
        mm = find_button(w, N_MAIN_MENU, timeout=3)
        if mm is None:
            raise GeminiError("No encuentro ni el botón de conversación nueva ni el menú principal.")
        press(mm)
        time.sleep(1.0)
    for lk in _descendants(w, control_type="Hyperlink"):
        try:
            v = (lk.iface_value.CurrentValue or "").split("?")[0].rstrip("/")
        except Exception:
            continue
        if re.fullmatch(r"https://gemini\.google\.com(/u/\d+)?/app", v):
            press(lk)
            return
    raise GeminiError("No encuentro el enlace de conversación nueva en la barra lateral.")


def set_prompt(w, text):
    ed = find_editor(w)
    try:
        ed.iface_value.SetValue(text)
    except Exception as ex:
        raise GeminiError(f"La caja de texto no admite escritura por accesibilidad: {ex}")
    time.sleep(0.5)


def send(w, timeout=10):
    b = find_button(w, N_SEND, timeout=timeout)
    if b is None:
        raise GeminiError("No aparece el botón de enviar (¿se escribió el texto?).")
    press(b)


def last_response_images(w):
    """Imágenes de la última respuesta (elementos Image con tamaño)."""
    labels = response_labels(w)
    if not labels:
        return []
    cont = response_container(labels[-1])
    out = []
    for im in _descendants(cont, control_type="Image"):
        r = im.rectangle()
        if r.width() >= 64 and r.height() >= 64:
            out.append(im)
    return out


def wait_response(w, n_before, timeout=300, poll=1.0):
    """Espera a que haya una respuesta nueva y deje de generarse.

    Devuelve (texto, número de imágenes)."""
    t0 = time.time()
    last, stable = None, 0
    while time.time() - t0 < timeout:
        time.sleep(poll)
        if len(response_labels(w)) <= n_before:
            continue
        if is_generating(w):
            stable = 0
            continue
        sig = (last_response(w), len(last_response_images(w)))
        if (sig[0] or sig[1]) and sig == last:
            stable += 1
            if stable >= 1:
                return sig
        else:
            stable = 0
        last = sig
    raise GeminiError(f"Gemini no ha terminado en {timeout} s.")


# --------------------------------------------------------------- modelo y chats

def _picker(w):
    for b in _descendants(w, control_type="Button"):
        n = b.element_info.name or ""
        if n.startswith(N_PICKER):
            return b
    raise GeminiError("No encuentro el selector de modo.")


def current_model(w):
    """Texto del modo actual, p. ej. «Flash High» o «Pro»."""
    n = _picker(w).element_info.name or ""
    return n.split("currently", 1)[-1].split("actualmente", 1)[-1].strip()


def _model_kind(text):
    """«flash», «pro», «lite» o «argon» según la primera palabra de modelo del texto
    («3.6 Flash Ayuda completa», «Seleccionado 3.1 Pro…», «currently Flash High»)."""
    m = re.search(r"\b(flash-lite|flash|pro|argon)\b", text.lower())
    if not m:
        return "?"
    return {"flash-lite": "lite"}.get(m.group(1), m.group(1))


def select_model(w, kind):
    """Elige «flash» (3.x Flash, no Lite) o «pro» (3.x Pro). Devuelve el modo anterior."""
    prev = current_model(w)
    if _model_kind(prev) == kind:
        return prev

    def radios_now():
        return _descendants(w, control_type="RadioButton")

    def wait_radios(t):
        t0 = time.time()
        while time.time() - t0 < t:
            r = radios_now()
            if r:
                return r
            time.sleep(0.2)
        return []

    target = None
    for attempt in range(2):
        radios = radios_now()  # ¿ya abierto?
        if not radios:
            press(_picker(w))
            radios = wait_radios(4)
        target = next((r for r in radios if _model_kind(r.element_info.name or "") == kind), None)
        if target is not None:
            break
        time.sleep(1.0)  # quizá se estaba cerrando: reintenta una vez
    if target is None:
        _close_picker(w)
        raise GeminiError(f"No encuentro el modo «{kind}» en el selector.")
    press(target)
    t0 = time.time()
    while time.time() - t0 < 6 and _model_kind(current_model(w)) != kind:
        time.sleep(0.3)
    _close_picker(w)
    if _model_kind(current_model(w)) != kind:
        raise GeminiError(f"No se ha podido cambiar al modo «{kind}».")
    return prev


def _close_picker(w):
    """Cierra el selector solo si sigue abierto tras su animación (si no, pulsarlo lo reabriría)."""
    time.sleep(1.0)
    if not _descendants(w, control_type="RadioButton"):
        return
    pk = _picker(w)
    try:
        pk.iface_expand_collapse.Collapse()
    except Exception:
        press(pk)
    time.sleep(0.8)


def close_sidebar(w, settle=1.5):
    """Cierra la barra lateral si sigue abierta tras un momento (tapa la caja de texto)."""
    t0 = time.time()
    while find_button(w, N_CLOSE_SIDEBAR) is not None and time.time() - t0 < settle:
        time.sleep(0.3)
    if find_button(w, N_CLOSE_SIDEBAR) is None:
        return
    press(find_button(w, N_MAIN_MENU, timeout=3) or find_button(w, N_CLOSE_SIDEBAR))
    t0 = time.time()
    while find_button(w, N_CLOSE_SIDEBAR) is not None and time.time() - t0 < 4:
        time.sleep(0.3)


def chat_url(w):
    try:
        return main_document(w).iface_value.CurrentValue or ""
    except Exception:
        return ""


def open_chat(w, url, timeout=15):
    """Abre un chat guardado buscándolo en la barra lateral por su URL."""
    cid = url.rstrip("/").split("/")[-1]
    if chat_url(w).rstrip("/").endswith(cid):
        return True
    if find_button(w, N_CLOSE_SIDEBAR) is None:
        press(find_button(w, N_MAIN_MENU, timeout=3))
    link, t0 = None, time.time()
    while link is None and time.time() - t0 < 6:
        for lk in _descendants(w, control_type="Hyperlink"):
            try:
                v = lk.iface_value.CurrentValue or ""
            except Exception:
                continue
            if v.rstrip("/").endswith(cid):
                link = lk
                break
        time.sleep(0.3)
    if link is None:
        close_sidebar(w, settle=0)
        raise GeminiError("El chat no aparece en la barra lateral (¿temporal, borrado o muy antiguo?).")
    press(link)
    t0 = time.time()
    while time.time() - t0 < timeout:
        if chat_url(w).rstrip("/").endswith(cid) and response_labels(w):
            break
        time.sleep(0.4)
    close_sidebar(w)  # al navegar suele cerrarse sola: no reabrirla
    find_editor(w)
    if not chat_url(w).rstrip("/").endswith(cid):
        raise GeminiError("No se ha podido abrir el chat.")
    time.sleep(1.0)
    return True


def _image_ids(w):
    return {tuple(im.element_info.runtime_id or ()) for im in last_response_images(w)}


def redo_with_pro(w, timeout=600, poll=1.0):
    """«Show more options» → «Redo with Pro» en la última respuesta; espera a la imagen nueva."""
    labels = response_labels(w)
    if not labels:
        raise GeminiError("El chat no tiene respuestas.")
    block = response_container(labels[-1]).parent()
    more = [b for b in _descendants(block, control_type="Button") if (b.element_info.name or "") in N_MORE]
    if not more:
        raise GeminiError("No encuentro «Show more options» en la respuesta.")
    before = _image_ids(w)
    press(more[-1])
    item, t0 = None, time.time()
    while item is None and time.time() - t0 < 6:
        for m in _descendants(w, control_type="MenuItem"):
            n = (m.element_info.name or "").lower()
            if re.search(r"\b(redo|rehacer|regenerar|volver a generar)\b.*\bpro\b", n):
                item = m
                break
        time.sleep(0.2)
    if item is None:
        press(more[-1])
        raise GeminiError("El menú no ofrece «Redo with Pro» (¿ya está hecha con Pro, o la app está "
                          "en español, que no lo ofrece?).")
    press(item)
    t0, last, started = time.time(), None, False
    while time.time() - t0 < timeout:
        time.sleep(poll)
        if is_generating(w):
            started = True
            last = None
            continue
        if not response_has_actions(w):
            continue
        ids = _image_ids(w)
        if not ids or ids == before:
            if started and not ids:
                continue
            if time.time() - t0 < 90:
                continue
        sig = (last_response(w), tuple(sorted(ids)))
        if sig == last and ids and ids != before:
            return sig[0], len(ids)
        last = sig
    raise GeminiError(f"Pro no ha terminado en {timeout} s.")


# --------------------------------------------------------------- archivos

def _dialog(w, timeout=10):
    """Cuadro de archivo (#32770) de Gemini. UIA lo cuelga de la ventana principal."""
    pid = w.process_id()
    t0 = time.time()
    while True:
        for d in _descendants(w, control_type="Window"):
            if d.element_info.class_name == "#32770":
                return d
        for h, _t in _top_windows("#32770", pid=pid):
            return _wrap(h)
        if time.time() - t0 >= timeout:
            return None
        time.sleep(0.3)


def _type_into(edit, text):
    """Escribe en un Edit Win32 con WM_CHAR, como si se tecleara.

    El cuadro de archivo no registra WM_SETTEXT ni ValuePattern: muestra el
    texto pero guarda con el nombre que traía (y pidió reemplazar un archivo)."""
    u = ctypes.windll.user32
    h = edit.element_info.handle
    u.SendMessageW(h, 0x00B1, 0, -1)    # EM_SETSEL: todo
    u.SendMessageW(h, 0x0102, 0x08, 0)  # WM_CHAR retroceso: borra
    for ch in text:
        u.SendMessageW(h, 0x0102, ord(ch), 0)
    time.sleep(0.3)


def _refuse_overwrite(w):
    """Si sale «¿Desea reemplazarlo?», contesta No. Devuelve True si salió."""
    for d in _descendants(w, control_type="Window"):
        texts = " ".join(t.element_info.name or "" for t in _descendants(d, control_type="Text"))
        if "reemplazar" in texts.lower() or "replace" in texts.lower():
            ctypes.windll.user32.SendMessageW(d.element_info.handle, 0x0400 + 102, 7, 0)  # TDM_CLICK_BUTTON IDNO
            time.sleep(0.5)
            return True
    return False


def _fill_dialog(d, path, edit_ids=("1148", "1001")):
    path = os.path.normpath(path)
    ed = None
    for e in _descendants(d, control_type="Edit"):
        if e.element_info.automation_id in edit_ids:
            ed = e
            break
    if ed is None:
        raise GeminiError("No encuentro el campo de nombre en el cuadro de archivo.")
    _type_into(ed, path)
    if (ed.iface_value.CurrentValue or "") != path:
        raise GeminiError("El cuadro de archivo no ha recogido la ruta.")
    ok = [b for b in _descendants(d, control_type="Button") if b.element_info.automation_id == "1"]
    if not ok:
        raise GeminiError("No encuentro el botón Abrir/Guardar.")
    press(ok[0])


def upload_file(w, path, timeout=30):
    """Adjunta un archivo con «Upload & tools» → «Upload files»."""
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise GeminiError(f"No existe {path}")
    before = attachment_count(w)
    d = _dialog(w, timeout=0)  # ¿quedó abierto de un intento anterior?
    if d is not None:
        _fill_dialog(d, path)
        return _wait_attachment(w, before, timeout)
    if find_button(w, N_UPLOAD_FILES) is None:  # el menú no está ya abierto
        b = find_button(w, N_UPLOAD, timeout=5)
        if b is None:
            raise GeminiError("No encuentro el botón «Upload & tools».")
        press(b)
    item, t0 = None, time.time()
    while item is None and time.time() - t0 < 6:
        for el in _descendants(w, control_type="MenuItem") + _descendants(w, control_type="Button"):
            n = (el.element_info.name or "").strip()
            if n in N_UPLOAD_FILES or n.lower().startswith(("upload file", "subir archivo")):
                item = el
                break
        time.sleep(0.3)
    if item is None:
        raise GeminiError("No aparece la opción «Upload files» en el menú.")
    press(item)
    d = _dialog(w)
    if d is None:
        raise GeminiError("No se abrió el cuadro para elegir archivo.")
    _fill_dialog(d, path)
    return _wait_attachment(w, before, timeout)


def attachment_count(w):
    """Adjuntos en la caja (cada uno tiene su botón «close attachment»)."""
    return sum(1 for b in _descendants(w, control_type="Button")
               if any(k in (b.element_info.name or "").lower()
                      for k in ("close attachment", "remove attachment", "remove file", "quitar archivo",
                                "eliminar archivo", "cerrar archivo", "adjunto")))


def _wait_attachment(w, before, timeout):
    """Espera a que aparezca un adjunto más en la caja."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        # Con la caja vacía, el botón de enviar solo aparece si hay un adjunto.
        if attachment_count(w) > before or (before == 0 and find_button(w, N_SEND) is not None):
            time.sleep(1.0)
            return True
        time.sleep(0.5)
    raise GeminiError("El archivo no aparece adjunto.")


def free_name(folder, base, ext=".jpg"):
    """Ruta libre: base.jpg, base_2.jpg, base_3.jpg..."""
    p, k = os.path.join(folder, base + ext), 2
    while os.path.exists(p):
        p, k = os.path.join(folder, f"{base}_{k}{ext}"), k + 1
    return p


def download_last_images(w, folder, base="gemini"):
    """Descarga a tamaño completo las imágenes de la última respuesta.

    Nunca sobrescribe: elige un nombre libre y, si Windows pregunta por
    reemplazar, contesta No y cancela."""
    folder = os.path.normpath(folder)
    os.makedirs(folder, exist_ok=True)
    labels = response_labels(w)
    if not labels:
        return []
    cont = response_container(labels[-1])
    btns = [b for b in _descendants(cont, control_type="Button")
            if (b.element_info.name or "").lower().startswith(("download", "descargar"))]
    saved = []
    for b in btns:
        target = free_name(folder, base)
        press(b)
        d = _dialog(w, timeout=60)  # primero baja la imagen grande y luego pregunta
        if d is None:
            raise GeminiError("No apareció el cuadro «Guardar como» al descargar.")
        try:
            _fill_dialog(d, target, edit_ids=("1001",))
        except GeminiError:
            _cancel_dialog(d)
            raise
        t0 = time.time()
        while time.time() - t0 < 60:
            if _refuse_overwrite(w):
                dd = _dialog(w, timeout=2)
                if dd is not None:
                    _cancel_dialog(dd)
                raise GeminiError("Windows pidió reemplazar un archivo; contestado No y cancelado.")
            if os.path.isfile(target) and os.path.getsize(target) > 0:
                break
            time.sleep(0.5)
        saved.append(target if os.path.isfile(target) else None)
    return saved


def _cancel_dialog(d):
    for b in _descendants(d, control_type="Button"):
        if b.element_info.automation_id == "2":
            press(b)
            return


def diagnose(w):
    """Nombres visibles (botones, menús, opciones) para ajustar los N_* si cambia la app o el idioma."""
    out = {"chat": chat_url(w), "modelo": "", "editor": "", "botones": [], "menus": [], "opciones": []}
    try:
        out["modelo"] = current_model(w)
    except GeminiError:
        pass
    try:
        out["editor"] = find_editor(w, timeout=1).element_info.name
    except GeminiError:
        pass
    seen = set()
    for b in _descendants(w, control_type="Button"):
        n = b.element_info.name or ""
        if n and n not in seen and b.element_info.automation_id not in NATIVE_IDS \
                and not n.startswith(("More options for", "Más opciones para")) and len(n) < 120:
            seen.add(n)
            out["botones"].append(n)
    out["menus"] = [m.element_info.name for m in _descendants(w, control_type="MenuItem") if m.element_info.name]
    out["opciones"] = [r.element_info.name for r in _descendants(w, control_type="RadioButton") if r.element_info.name]
    return out


# --------------------------------------------------------------- captura

def capture(w, path):
    """Captura la ventana con PrintWindow (vale aunque esté tapada)."""
    from PIL import Image
    hwnd = w.handle
    user32, gdi32 = ctypes.windll.user32, ctypes.windll.gdi32
    r = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    wd, ht = r.right - r.left, r.bottom - r.top
    hdc = user32.GetWindowDC(hwnd)
    mdc = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, wd, ht)
    gdi32.SelectObject(mdc, bmp)
    user32.PrintWindow(hwnd, mdc, 2)  # PW_RENDERFULLCONTENT

    class BIH(ctypes.Structure):
        _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG), ("biHeight", wintypes.LONG),
                    ("biPlanes", wintypes.WORD), ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
                    ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG),
                    ("biYPelsPerMeter", wintypes.LONG), ("biClrUsed", wintypes.DWORD), ("biClrImportant", wintypes.DWORD)]

    bih = BIH(ctypes.sizeof(BIH), wd, -ht, 1, 32, 0, 0, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(wd * ht * 4)
    gdi32.GetDIBits(mdc, bmp, 0, ht, buf, ctypes.byref(bih), 0)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mdc)
    user32.ReleaseDC(hwnd, hdc)
    Image.frombuffer("RGBA", (wd, ht), buf, "raw", "BGRA", 0, 1).convert("RGB").save(path)
    return path
