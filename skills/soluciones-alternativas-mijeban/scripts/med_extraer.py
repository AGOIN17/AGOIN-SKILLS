"""Extrae la geometría de las vistas de alzado-sección a un JSON ligero (para iterar sin releer el DXF de 90 MB)."""
import sys, json, ezdxf
from ezdxf import bbox, path as ezpath
doc = ezdxf.readfile(sys.argv[1])
msp = doc.modelspace()
vistas = []
for l in doc.layouts:
    if not l.name.startswith(("A-04", "A-05", "A-06", "A-07")):
        continue
    for v in l.query("VIEWPORT"):
        if abs(v.dxf.view_center_point.x) > 1e6 or v.dxf.height / max(v.dxf.view_height, 1e-9) > 0.9:
            continue
        w = v.dxf.view_height * v.dxf.width / v.dxf.height
        c = v.dxf.view_center_point
        vistas.append({"hoja": l.name, "x0": c.x - w / 2, "y0": c.y - v.dxf.view_height / 2,
                       "x1": c.x + w / 2, "y1": c.y + v.dxf.view_height / 2})


def rgb(e):
    tc = e.dxf.get("true_color")
    return [tc >> 16 & 255, tc >> 8 & 255, tc & 255] if tc is not None else None


def geo(e):
    t = e.dxftype()
    if t == "HATCH":
        out = []
        for p in ezpath.from_hatch(e):
            out.append([[round(v.x, 4), round(v.y, 4)] for v in p.flattening(0.01)])
        return out
    if t in ("LINE", "LWPOLYLINE", "POLYLINE", "ARC", "CIRCLE", "ELLIPSE", "SPLINE"):
        try:
            p = ezpath.make_path(e)
            return [[[round(v.x, 4), round(v.y, 4)] for v in p.flattening(0.01)]]
        except Exception:
            return []
    return []


cache = bbox.Cache()
salida = []
todas = [(e, bbox.extents([e], fast=True, cache=cache)) for e in msp if e.dxftype() != "DIMENSION"]
for i, v in enumerate(vistas):
    ents = []
    for e, b in todas:
        if not b.has_data or b.extmin.x < v["x0"] - 0.5 or b.extmax.x > v["x1"] + 0.5 or b.extmin.y < v["y0"] - 0.5 or b.extmax.y > v["y1"] + 0.5:
            continue
        d = {"h": e.dxf.handle, "t": e.dxftype(), "l": e.dxf.layer, "c": rgb(e), "aci": e.dxf.get("color")}
        if e.dxftype() == "INSERT":
            d["blk"] = e.dxf.name
            d["bb"] = [b.extmin.x, b.extmin.y, b.extmax.x, b.extmax.y]
            sub = []
            for ve in e.virtual_entities():
                for g in geo(ve):
                    sub.append(g)
            d["g"] = sub
        elif e.dxftype() in ("TEXT", "MTEXT"):
            d["txt"] = e.dxf.text if e.dxftype() == "TEXT" else e.plain_text()
            d["p"] = [e.dxf.insert.x, e.dxf.insert.y]
        else:
            d["g"] = geo(e)
            d["closed"] = bool(getattr(e, "closed", False)) if e.dxftype() == "LWPOLYLINE" else None
            if e.dxftype() == "HATCH":
                d["pat"] = e.dxf.pattern_name
        ents.append(d)
    v["ents"] = ents
    salida.append(v)
    print(i, v["hoja"], len(ents))
json.dump(salida, open(sys.argv[2], "w", encoding="utf-8"))
