"""MCP «gemini»: maneja la app nativa de Gemini para Windows.

- Borradores rápidos con Flash (editar_imagen) y versión buena con Pro
  (mejorar_en_pro: vuelve al chat del borrador y pulsa «Redo with Pro»).
- Trabaja en segundo plano: los encargos van a una cola y se consultan con
  «estado». La ventana trabaja aparcada (casi invisible) si estaba minimizada.

Servidor stdio sin SDK de MCP: solo necesita Python 3 con pywinauto, psutil y
Pillow (pip install -r requirements.txt) y la app de Gemini para Windows.
El plugin «agoin» lo registra solo; a mano:
    claude mcp add gemini --scope user -- python <ruta>/mcp/gemini/server.py
No carga nada hasta el primer encargo, así que no molesta a quien no lo use.
"""
import base64
import ctypes
import io
import itertools
import json
import os
import queue
import sys
import threading
import time
import traceback
import uuid

_OUT = sys.stdout.buffer
sys.stdout = sys.stderr  # cualquier print de librerías va a stderr, no al protocolo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_OUT_LOCK = threading.Lock()

g = None  # gemini_app: se importa en el hilo de trabajo (COM y UI Automation viven ahí)


def _downloads():
    """Carpeta Descargas real del usuario (puede estar redirigida, p. ej. D:\\Descargas)."""
    try:
        fid = uuid.UUID("374DE290-123F-4565-9164-39C4925E467B")
        guid = (ctypes.c_byte * 16).from_buffer_copy(fid.bytes_le)
        p = ctypes.c_wchar_p()
        if ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(guid), 0, None, ctypes.byref(p)) == 0:
            path = p.value
            ctypes.windll.ole32.CoTaskMemFree(p)
            return path
    except Exception:
        pass
    return os.path.join(os.path.expanduser("~"), "Downloads")


SALIDA = os.environ.get("GEMINI_SALIDA") or os.path.join(_downloads(), "Gemini")

CRITERIOS = (
    "Convierte esta imagen, una vista 3D de un modelo de arquitectura, en una fotografía fotorrealista. "
    "Mantén exactamente la misma cámara, el mismo encuadre y la misma proyección "
    "(si es una axonometría, que siga siéndolo). "
    "Mantén la geometría tal cual: mismos volúmenes, mismo número y posición de ventanas, puertas, "
    "escaleras, porches, muros y cubiertas; no añadas ni quites elementos. "
    "Cambia solo los materiales, la luz y el entorno inmediato. Sin personas ni coches."
)

_ESPERAR = {"type": "boolean", "default": False,
            "description": "true = esperar al resultado; false (por defecto) = devuelve al momento "
                           "un número de trabajo y se consulta con «estado»."}

TOOLS = [
    {
        "name": "editar_imagen",
        "description": (
            "Borrador fotorrealista con Gemini de una o varias imágenes (vistas 3D de Revit, capturas del visor). "
            "Cada imagen va en su propio chat; guarda <nombre>_gemini.jpg y una ficha <nombre>_gemini.json "
            "(original, petición, chat) en la carpeta de salida. Por defecto usa Flash (rápido) y añade criterios "
            "para no tocar la geometría ni la cámara y no poner personas; 'instrucciones' añade detalles. "
            "Cuando un borrador guste, usa mejorar_en_pro."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "imagenes": {"type": "array", "items": {"type": "string"},
                             "description": "Rutas de las imágenes (png/jpg)."},
                "instrucciones": {"type": "string", "default": "",
                                  "description": "Detalles (materiales, luz, entorno); se suman a los criterios."},
                "usar_criterios": {"type": "boolean", "default": True,
                                   "description": "false = enviar solo 'instrucciones'."},
                "modelo": {"type": "string", "enum": ["flash", "pro"], "default": "flash"},
                "carpeta_salida": {"type": "string", "description": f"Por defecto {SALIDA}"},
                "temporal": {"type": "boolean", "default": False,
                             "description": "Chat temporal (no queda en el historial; luego no se puede usar "
                                            "«Redo with Pro» y mejorar_en_pro lo repite desde el original)."},
                "esperar": _ESPERAR,
            },
            "required": ["imagenes"],
        },
    },
    {
        "name": "mejorar_en_pro",
        "description": (
            "Versión buena de borradores ya hechos: abre el chat de cada borrador (por su ficha .json) y pulsa "
            "«Redo with Pro»; descarga a tamaño completo como <nombre>_gemini_pro.jpg. Si el chat no existe "
            "(temporal o borrado), lo repite con Pro desde la imagen original y la misma petición."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "imagenes": {"type": "array", "items": {"type": "string"},
                             "description": "Rutas de los borradores (_gemini.jpg) o de sus fichas .json."},
                "esperar": _ESPERAR,
            },
            "required": ["imagenes"],
        },
    },
    {
        "name": "estado",
        "description": "Estado de los trabajos en cola. Con 'trabajo' devuelve su resultado; 'esperar_s' "
                       "espera hasta ese tiempo a que termine.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "trabajo": {"type": "integer"},
                "esperar_s": {"type": "integer", "default": 0},
            },
        },
    },
    {
        "name": "preguntar",
        "description": "Envía un mensaje de texto a la app de Gemini del usuario y devuelve la respuesta.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mensaje": {"type": "string"},
                "chat_nuevo": {"type": "boolean", "default": True},
                "temporal": {"type": "boolean", "default": False,
                             "description": "Chat temporal: no queda en el historial de Gemini."},
                "modelo": {"type": "string", "enum": ["flash", "pro"], "default": "flash"},
            },
            "required": ["mensaje"],
        },
    },
    {
        "name": "leer_respuesta",
        "description": "Lee la última respuesta del chat abierto en la app de Gemini.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "captura",
        "description": "Captura la ventana de la app de Gemini (para ver en qué estado está).",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


# ----------------------------------------------------------------- utilidades

def _text(t):
    return {"type": "text", "text": t}


def _preview(path, max_side=768):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80)
    return {"type": "image", "data": base64.b64encode(buf.getvalue()).decode(), "mimeType": "image/jpeg"}


def _size(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return f"{im.width}×{im.height}"
    except Exception:
        return "?"


def _write_card(img_path, data):
    with open(os.path.splitext(img_path)[0] + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _read_card(path):
    card = os.path.splitext(path)[0] + ".json"
    if not os.path.isfile(card):
        raise g.GeminiError(f"No hay ficha {os.path.basename(card)}: no sé de qué chat salió. "
                            "Genera el borrador con editar_imagen.")
    with open(card, encoding="utf-8") as f:
        return json.load(f)


class _Model:
    """Cambia de modelo para un encargo y deja el que había al terminar."""

    def __init__(self, w, kind):
        self.w, self.kind, self.prev = w, kind, None

    def __enter__(self):
        if self.kind:
            prev = g.select_model(self.w, self.kind)
            if g._model_kind(prev) != self.kind:
                self.prev = g._model_kind(prev)
        return self

    def __exit__(self, *exc):
        if self.prev in ("flash", "pro"):
            try:
                g.select_model(self.w, self.prev)
            except Exception:
                pass
        return False


def _run_one(w, original, prompt, folder, base, kind, temporal, progress):
    """Chat nuevo + adjunto + petición + espera + descarga. Devuelve (rutas, texto, url)."""
    g.new_chat(w, temporary=temporal)
    with _Model(w, kind):
        progress("subiendo")
        g.upload_file(w, os.path.normpath(os.path.abspath(original)))
        n = len(g.response_labels(w))
        g.set_prompt(w, prompt)
        g.send(w)
        progress("generando")
        txt, nimg = g.wait_response(w, n, timeout=600 if kind == "pro" else 400)
        url = "" if temporal else g.chat_url(w)
        progress("descargando")
        saved = [s for s in (g.download_last_images(w, folder, base) if nimg else []) if s]
    return saved, txt, url


# ----------------------------------------------------------------- encargos

def job_editar(a, progress):
    imgs = a.get("imagenes") or []
    if isinstance(imgs, str):
        imgs = [imgs]
    if not imgs:
        raise g.GeminiError("Falta la lista 'imagenes'.")
    for p in imgs:
        if not os.path.isfile(p):
            raise g.GeminiError(f"No existe {p}")
    extra = (a.get("instrucciones") or "").strip()
    prompt = (CRITERIOS + (" " + extra if extra else "")) if a.get("usar_criterios", True) else extra
    if not prompt:
        raise g.GeminiError("Sin criterios hace falta 'instrucciones'.")
    folder = os.path.normpath(a.get("carpeta_salida") or SALIDA)
    kind = a.get("modelo") or "flash"
    temporal = bool(a.get("temporal"))
    lines, previews = [], []
    with g.session() as w:
        for i, p in enumerate(imgs, 1):
            name = os.path.basename(p)
            try:
                base = os.path.splitext(name)[0] + ("_gemini_pro" if kind == "pro" else "_gemini")
                saved, txt, url = _run_one(w, p, prompt, folder, base, kind, temporal,
                                           lambda s, i=i, n=name: progress(f"{i}/{len(imgs)} {n}: {s}"))
                for s in saved:
                    _write_card(s, {"original": os.path.abspath(p), "peticion": prompt, "modelo": kind,
                                    "chat_url": url, "temporal": temporal,
                                    "fecha": time.strftime("%Y-%m-%d %H:%M"), "gemini": txt})
                lines.append(f"{name} → " + (", ".join(f"{s} ({_size(s)})" for s in saved) if saved
                                             else "SIN IMAGEN" + (f" · Gemini: {txt[:200]}" if txt else "")))
                if saved and len(previews) < 4:
                    previews.append(_preview(saved[0]))
            except Exception as ex:
                lines.append(f"{name} → ERROR: {ex}")
    return [_text("\n".join(lines))] + previews


def job_pro(a, progress):
    items = a.get("imagenes") or []
    if isinstance(items, str):
        items = [items]
    lines, previews = [], []
    with g.session() as w:
        for i, p in enumerate(items, 1):
            name = os.path.basename(p)
            step = lambda s, i=i, n=name: progress(f"{i}/{len(items)} {n}: {s}")  # noqa: E731
            try:
                card = _read_card(p)
                draft = os.path.splitext(p)[0] + ".jpg" if p.lower().endswith(".json") else p
                folder = os.path.dirname(os.path.abspath(draft))
                base = os.path.splitext(os.path.basename(draft))[0] + "_pro"
                saved, via, txt = [], "", ""
                if card.get("chat_url") and not card.get("temporal"):
                    try:
                        step("abriendo el chat del borrador")
                        g.open_chat(w, card["chat_url"])
                        step("Redo with Pro")
                        txt, nimg = g.redo_with_pro(w)
                        step("descargando")
                        saved = [s for s in g.download_last_images(w, folder, base) if s]
                        via = "Redo with Pro en el chat del borrador"
                    except g.GeminiError as ex:
                        via = f"(no se pudo en el chat: {ex}) "
                if not saved:
                    step("repitiendo con Pro desde el original")
                    saved, txt, url = _run_one(w, card["original"], card["peticion"], folder, base, "pro",
                                               bool(card.get("temporal")), step)
                    card = dict(card, chat_url=url)
                    via += "repetida con Pro desde el original"
                for s in saved:
                    _write_card(s, dict(card, modelo="pro", borrador=os.path.abspath(draft),
                                        fecha=time.strftime("%Y-%m-%d %H:%M"), gemini=txt))
                lines.append(f"{name} → " + (", ".join(f"{s} ({_size(s)})" for s in saved) or "SIN IMAGEN")
                             + f"  [{via}]")
                if saved and len(previews) < 4:
                    previews.append(_preview(saved[0]))
            except Exception as ex:
                lines.append(f"{name} → ERROR: {ex}")
    return [_text("\n".join(lines))] + previews


def job_preguntar(a, progress):
    with g.session() as w:
        if a.get("chat_nuevo", True) or a.get("temporal"):
            g.new_chat(w, temporary=bool(a.get("temporal")))
        with _Model(w, a.get("modelo") or None):
            n = len(g.response_labels(w))
            g.set_prompt(w, a["mensaje"])
            g.send(w)
            txt, nimg = g.wait_response(w, n, timeout=600)
    if nimg:
        txt += f"\n\n[La respuesta incluye {nimg} imagen(es).]"
    return [_text(txt or "(respuesta vacía)")]


def job_leer(a, progress):
    with g.session() as w:
        txt = g.last_response(w)
        nimg = len(g.last_response_images(w))
    extra = f" [{nimg} imagen(es)]" if nimg else ""
    return [_text((txt or "(sin respuesta)") + extra)]


def job_captura(a, progress):
    import tempfile
    path = os.path.join(tempfile.gettempdir(), "gemini_mcp_captura.png")
    with g.session() as w:
        g.capture(w, path)
    return [_preview(path, max_side=1024)]


JOBS_FN = {"editar_imagen": job_editar, "mejorar_en_pro": job_pro, "preguntar": job_preguntar,
           "leer_respuesta": job_leer, "captura": job_captura}
ASYNC_OK = {"editar_imagen", "mejorar_en_pro"}

_ids = itertools.count(1)
JOBS = {}
_Q = queue.Queue()


_REQS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")


def _load():
    """Importa gemini_app en el primer encargo. Devuelve un texto de error o None."""
    global g
    if g is not None:
        return None
    if sys.platform != "win32":
        return "Este MCP solo funciona en Windows (maneja la app de Gemini para Windows)."
    try:
        import gemini_app
    except ImportError as ex:
        return (f"Falta una librería de Python ({ex.name}). Instálalas con:\n"
                f"  python -m pip install -r \"{_REQS}\"\ny vuelve a abrir Claude Code.")
    g = gemini_app
    try:
        g.rescue_window()
    except Exception:
        pass
    return None


def _worker():
    while True:
        job = _Q.get()
        job["estado"] = "en curso"
        job["inicio"] = time.time()

        def progress(msg, job=job):
            job["progreso"] = msg

        try:
            err = _load()
            if err:
                job["resultado"] = [_text(err)]
                job["estado"] = "error"
                job["fin"] = time.time()
                job["hecho"].set()
                continue
            job["resultado"] = JOBS_FN[job["tool"]](job["args"], progress)
            job["estado"] = "terminado"
        except Exception as ex:
            msg = str(ex) if g and isinstance(ex, g.GeminiError) else traceback.format_exc()[-1500:]
            job["resultado"] = [_text(f"Error: {msg}")]
            job["estado"] = "error"
        job["fin"] = time.time()
        job["hecho"].set()


def _submit(tool, args):
    jid = next(_ids)
    JOBS[jid] = {"id": jid, "tool": tool, "args": args, "estado": "en cola", "progreso": "",
                 "creado": time.time(), "hecho": threading.Event(), "resultado": None}
    _Q.put(JOBS[jid])
    return JOBS[jid]


def _summary(job):
    t = job.get("fin", time.time()) - job.get("inicio", job["creado"]) if job.get("inicio") else 0
    n = len(job["args"].get("imagenes") or []) if isinstance(job["args"].get("imagenes"), list) else ""
    s = f"Trabajo {job['id']} ({job['tool']}{f', {n} imagen(es)' if n else ''}): {job['estado']}"
    if job["estado"] == "en curso" and job["progreso"]:
        s += f" · {job['progreso']}"
    if t:
        s += f" · {t:.0f} s"
    return s


def _result(job):
    content = list(job["resultado"] or [])
    return [_text(_summary(job))] + content, job["estado"] == "error"


def handle_call(name, args):
    if name == "estado":
        jid = args.get("trabajo")
        if jid is None:
            if not JOBS:
                return [_text("No hay trabajos.")], False
            return [_text("\n".join(_summary(j) for j in JOBS.values()))], False
        job = JOBS.get(int(jid))
        if job is None:
            return [_text(f"No existe el trabajo {jid}.")], True
        job["hecho"].wait(timeout=max(0, int(args.get("esperar_s") or 0)))
        if not job["hecho"].is_set():
            return [_text(_summary(job))], False
        return _result(job)
    if name not in JOBS_FN:
        return [_text(f"Herramienta desconocida: {name}")], True
    job = _submit(name, args)
    if name in ASYNC_OK and not args.get("esperar", False):
        ahead = sum(1 for j in JOBS.values() if j["estado"] in ("en cola", "en curso") and j["id"] < job["id"])
        return [_text(f"Trabajo {job['id']} en cola" + (f" (delante hay {ahead})" if ahead else "")
                      + ". Consulta con estado(trabajo=" + str(job["id"]) + ", esperar_s=...).")], False
    job["hecho"].wait()
    return _result(job)


# ----------------------------------------------------------------- protocolo

def _send(msg):
    data = (json.dumps(msg, ensure_ascii=False) + "\n").encode("utf-8")
    with _OUT_LOCK:
        _OUT.write(data)
        _OUT.flush()


def main():
    threading.Thread(target=_worker, daemon=True).start()
    for raw in sys.stdin.buffer:
        line = raw.decode("utf-8", "replace").strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        mid, method, params = msg.get("id"), msg.get("method"), msg.get("params") or {}
        if mid is None:
            continue  # notificaciones (initialized, cancelled...)
        try:
            if method == "initialize":
                result = {"protocolVersion": params.get("protocolVersion", "2025-06-18"),
                          "capabilities": {"tools": {}},
                          "serverInfo": {"name": "gemini", "version": "2.0"}}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                content, is_err = handle_call(params.get("name"), params.get("arguments") or {})
                result = {"content": content, "isError": is_err}
            elif method == "ping":
                result = {}
            else:
                _send({"jsonrpc": "2.0", "id": mid,
                       "error": {"code": -32601, "message": f"Método no soportado: {method}"}})
                continue
            _send({"jsonrpc": "2.0", "id": mid, "result": result})
        except Exception as ex:
            _send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": str(ex)}})


if __name__ == "__main__":
    main()
