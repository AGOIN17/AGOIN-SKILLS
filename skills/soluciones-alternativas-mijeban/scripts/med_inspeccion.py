import sys, re, time, ezdxf
from collections import Counter, defaultdict
t0 = time.time()
doc = ezdxf.readfile(sys.argv[1])
print(f"leído en {time.time()-t0:.0f} s; versión {doc.dxfversion}; unidades $INSUNITS={doc.header.get('$INSUNITS')}")
msp = doc.modelspace()
print("presentaciones:", [l.name for l in doc.layouts])
for l in doc.layouts:
    if l.name == "Model":
        continue
    vps = [e for e in l if e.dxftype() == "VIEWPORT" and e.dxf.get("id", 2) != 1]
    txts = [e for e in l if e.dxftype() in ("TEXT", "MTEXT")]
    print(f"  [{l.name}] {len(l)} ent., {len(vps)} ventanas")
    for v in vps[:12]:
        esc = v.dxf.height / v.dxf.view_height if v.dxf.view_height else 0
        print(f"      vp centro_modelo=({v.dxf.view_center_point.x:.1f},{v.dxf.view_center_point.y:.1f}) alto_modelo={v.dxf.view_height:.1f} escala_papel/modelo={esc:.4f}")
xrefs = [b.name for b in doc.blocks if b.block and b.block.dxf.get("xref_path")]
print("xrefs:", [(b, doc.blocks.get(b).block.dxf.get('xref_path')) for b in xrefs])
cap = defaultdict(Counter)
for e in msp:
    cap[e.dxf.layer][e.dxftype()] += 1
print("capas del modelo (entidades):")
for k, v in sorted(cap.items(), key=lambda kv: -sum(kv[1].values())):
    print(f"   {k:40s} {dict(v)}")
print("textos con ALZADO/FACHADA/SECCI/PLANTA en el modelo:")
for e in msp.query("TEXT MTEXT"):
    t = e.dxf.text if e.dxftype() == "TEXT" else e.plain_text()
    if re.search(r"ALZADO|FACHADA|SECCI|PLANTA", t, re.I):
        p = e.dxf.insert
        print(f"   ({p.x:10.1f},{p.y:10.1f}) {e.dxf.layer:25s} {t[:70]!r}")
pat = Counter((e.dxf.layer, e.dxf.pattern_name) for e in msp.query("HATCH"))
print("tramas (capa, patrón):")
for (l, p), n in pat.most_common(60):
    print(f"   {l:35s} {p:15s} {n}")
ins = Counter((e.dxf.layer, e.dxf.name) for e in msp.query("INSERT"))
print("bloques insertados (capa, nombre) más frecuentes:")
for (l, n), c in ins.most_common(50):
    print(f"   {l:30s} {n:40s} {c}")
