"""Extrae las plantas (bloques P-B y P-1 PR. EJECUCION) que se ven en las hojas A-02 y A-01."""
import sys, json, ezdxf
from ezdxf import bbox, path as ezpath
from collections import Counter
doc = ezdxf.readfile(sys.argv[1])
msp = doc.modelspace()
ventanas = {}
for l in doc.layouts:
    if l.name.startswith(("A-01", "A-02")):
        for v in l.query("VIEWPORT"):
            if abs(v.dxf.view_center_point.x) > 1e5:
                w = v.dxf.view_height * v.dxf.width / v.dxf.height
                c = v.dxf.view_center_point
                ventanas[l.name[:4]] = (c.x - w / 2, c.y - v.dxf.view_height / 2, c.x + w / 2, c.y + v.dxf.view_height / 2)
print(ventanas)


def rgb(e):
    tc = e.dxf.get("true_color")
    return [tc >> 16 & 255, tc >> 8 & 255, tc & 255] if tc is not None else None


def geo(e):
    try:
        if e.dxftype() == "HATCH":
            return [[[round(v.x, 4), round(v.y, 4)] for v in p.flattening(0.01)] for p in ezpath.from_hatch(e)]
        p = ezpath.make_path(e)
        return [[[round(v.x, 4), round(v.y, 4)] for v in p.flattening(0.01)]]
    except Exception:
        return []


def explotar(ins, nivel=0):
    for ve in ins.virtual_entities():
        if ve.dxftype() == "INSERT" and nivel < 4 and ve.dxf.layer not in ("0_ELE", "0_SNM", "0_FON", "0_MOB"):
            yield from explotar(ve, nivel + 1)
        else:
            yield ve


salida = []
for hoja, blk in (("A-02", "P-B PR. EJECUCION"), ("A-01", "P-1 PR. EJECUCION")):
    X0, Y0, X1, Y1 = ventanas[hoja]
    for ins in msp.query(f'INSERT[name=="{blk}"]'):
        ents, n_in = [], 0
        for ve in explotar(ins):
            b = bbox.extents([ve], fast=True)
            if not b.has_data or b.extmax.x < X0 or b.extmin.x > X1 or b.extmax.y < Y0 or b.extmin.y > Y1:
                continue
            n_in += 1
            d = {"t": ve.dxftype(), "l": ve.dxf.layer, "c": rgb(ve)}
            if ve.dxftype() in ("TEXT", "MTEXT"):
                d["txt"] = ve.dxf.text if ve.dxftype() == "TEXT" else ve.plain_text()
                d["p"] = [ve.dxf.insert.x, ve.dxf.insert.y]
            elif ve.dxftype() == "INSERT":
                d["blk"] = ve.dxf.name; d["p"] = [ve.dxf.insert.x, ve.dxf.insert.y]
            else:
                d["g"] = geo(ve)
                if ve.dxftype() == "HATCH":
                    d["pat"] = ve.dxf.pattern_name
                if ve.dxftype() == "LWPOLYLINE":
                    d["closed"] = bool(ve.closed)
            ents.append(d)
        if n_in:
            print(hoja, blk, ins.dxf.insert, "entidades en la ventana:", n_in)
            print("   ", Counter((e["l"], e["t"]) for e in ents).most_common(25))
            salida.append({"hoja": hoja, "ventana": ventanas[hoja], "ents": ents})
            break
json.dump(salida, open(sys.argv[2], "w", encoding="utf-8"))
