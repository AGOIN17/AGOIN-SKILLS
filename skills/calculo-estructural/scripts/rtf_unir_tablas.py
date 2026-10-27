# Notas RTF de programas técnicos (Robot Structural Analysis) a PDF, sin letras griegas.
#   Robot escribe una nota como varios documentos RTF pegados (p. ej. datos, diseño geotécnico, diseño de hormigón), cada uno con
#   su propia tabla de fuentes y de colores. Word solo lee la primera: el texto de las partes siguientes sale en Symbol (letras
#   griegas) y con los colores cambiados. Este script une las tablas, quita las cabeceras intermedias y convierte con Word.
#   Uso: python rtf_unir_tablas.py nota.rtf [...]      · escribe nota.pdf al lado (necesita Word y pywin32)
#   Probado con las notas del módulo de zapatas de Robot 2027 (octubre de 2026).
import os
import re
import sys

CAB = re.compile(rb"\\rtf1\\ansi\\ansicpg\d+\\deff\d+\\deflang\d+(\{\\fonttbl.*?\}\})\s*(\{\\colortbl[^}]*\})\s*(\{\\\*\\generator[^}]*\})")
FUENTE = re.compile(rb"\{\\f(\d+)\\[a-z]+(?:\\fprq\d+)?\\fcharset(\d+) ([^;]+);\}")
COLOR = re.compile(rb"\\red(\d+)\\green(\d+)\\blue(\d+);")


def tabla_fuentes(ft):
    return [(int(n), int(cs), nom.decode("latin-1")) for n, cs, nom in FUENTE.findall(ft)]


def tabla_colores(ct):
    return [tuple(map(int, c)) for c in COLOR.findall(ct)]


def remapear(texto, mapa, prefijo):
    """\\f3 -> \\f5 (sin tocar \\fs, \\fi...), o \\cf2 -> \\cf4"""
    pat = re.compile(rb"\\" + prefijo + rb"(\d+)(?![0-9])")
    return pat.sub(lambda m: b"\\" + prefijo + str(mapa.get(int(m.group(1)), int(m.group(1)))).encode(), texto)


def arreglar(datos):
    """Devuelve el RTF con una sola tabla de fuentes y de colores (fcharset 1 -> 0, página de códigos 1252)."""
    i_ct = datos.find(b"{\\colortbl")
    cab0 = datos[:i_ct]
    ft0 = cab0[cab0.find(b"{\\fonttbl"):]
    fuentes = [(n, 0 if cs == 1 else cs, nom) for n, cs, nom in tabla_fuentes(ft0)]
    ct0 = datos[i_ct:datos.find(b"}", i_ct) + 1]
    colores = tabla_colores(ct0)
    resto = datos[datos.find(b"}", i_ct) + 1:]
    partes, ultimo = [], 0
    for m in CAB.finditer(resto):
        partes.append((resto[ultimo:m.start()], None))
        partes.append((None, m))
        ultimo = m.end()
    partes.append((resto[ultimo:], None))
    trozos, mapa_f, mapa_c = [], {}, {}
    for texto, m in partes:
        if m is not None:                                   # cabecera de un documento pegado: nuevas tablas
            mapa_f, mapa_c = {}, {}
            for n, cs, nom in tabla_fuentes(m.group(1)):
                cs = 0 if cs == 1 else cs
                idx = next((k for k, (nn, c2, n2) in enumerate(fuentes) if n2 == nom and c2 == cs), None)
                if idx is None:
                    fuentes.append((len(fuentes), cs, nom))
                    idx = len(fuentes) - 1
                mapa_f[n] = fuentes[idx][0]
            for k, c in enumerate(tabla_colores(m.group(2)), start=1):
                if c not in colores:
                    colores.append(c)
                mapa_c[k] = colores.index(c) + 1
            continue
        if mapa_f:
            texto = remapear(texto, mapa_f, rb"f")
        if mapa_c:
            texto = remapear(texto, mapa_c, rb"cf")
        trozos.append(texto)
    familia = {"Symbol": b"\\froman\\fprq2", "Arial": b"\\fswiss", "Courier New": b"\\fmodern\\fprq1"}
    ft = b"{\\fonttbl" + b"".join(b"{\\f%d%s\\fcharset%d %s;}" % (n, familia.get(nom, b"\\fnil"), cs, nom.encode("latin-1"))
                                  for n, cs, nom in fuentes) + b"}"
    ct = b"{\\colortbl ;" + b"".join(b"\\red%d\\green%d\\blue%d;" % c for c in colores) + b"}"
    pre = cab0[:cab0.find(b"{\\fonttbl")].replace(b"\\ansicpg1250", b"\\ansicpg1252")
    return pre + ft + b"\r\n" + ct + b"".join(trozos)


def a_pdf(rutas, sobrescribir=False):
    """Convierte cada RTF a un PDF al lado. No pisa un PDF que ya exista salvo con sobrescribir=True."""
    import tempfile
    import win32com.client
    word = win32com.client.DispatchEx("Word.Application")   # instancia propia: no toca el Word del usuario
    word.Visible = False
    word.DisplayAlerts = 0
    salida = []
    carpeta_tmp = tempfile.mkdtemp(prefix="rtf_unir_")
    try:
        for ruta in rutas:
            ruta = os.path.abspath(ruta)
            pdf = os.path.splitext(ruta)[0] + ".pdf"
            if os.path.exists(pdf) and not sobrescribir:
                print("ya existe, no se sobrescribe:", pdf)
                continue
            tmp = os.path.join(carpeta_tmp, os.path.basename(ruta))
            open(tmp, "wb").write(arreglar(open(ruta, "rb").read()))
            doc = word.Documents.Open(tmp, ConfirmConversions=False, ReadOnly=True, AddToRecentFiles=False)
            try:
                tmp_pdf = os.path.join(carpeta_tmp, os.path.splitext(os.path.basename(ruta))[0] + ".pdf")
                doc.ExportAsFixedFormat(tmp_pdf, 17)         # 17 = wdExportFormatPDF
                n = doc.ComputeStatistics(2)                 # 2 = páginas
            finally:
                doc.Close(False)
            os.replace(tmp_pdf, pdf)
            salida.append((pdf, n))
            print(pdf, n, "páginas")
    finally:
        word.Quit()
        for f in os.listdir(carpeta_tmp):
            try:
                os.remove(os.path.join(carpeta_tmp, f))
            except OSError:
                pass
        try:
            os.rmdir(carpeta_tmp)
        except OSError:
            pass
    return salida


if __name__ == "__main__":
    a_pdf([a for a in sys.argv[1:] if not a.startswith("--")], sobrescribir="--sobrescribir" in sys.argv)
