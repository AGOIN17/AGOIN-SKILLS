from ezdxf.fonts import fonts


def lineas(texto, h, ancho, ttf="GOTHIC.TTF", track=1.0):
    """Corta el texto como AutoCAD (palabra a palabra) y devuelve (líneas, ancho máximo)."""
    f = fonts.make_font(ttf, h)
    out, cur = [], ""
    for w in texto.split(" "):
        prueba = (cur + " " + w).strip()
        if f.text_width(prueba) * track <= ancho or not cur:
            cur = prueba
        else:
            out.append(cur); cur = w
    out.append(cur)
    return out, max(f.text_width(l) * track for l in out)
