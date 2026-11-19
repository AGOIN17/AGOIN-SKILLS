import sys, ezdxf, collections
doc = ezdxf.readfile(sys.argv[1])
cnt = collections.Counter(); donde = collections.defaultdict(collections.Counter)
def ver(layout, nombre):
    for e in layout.query('DIMENSION'):
        try: m = e.get_measurement()
        except Exception: continue
        if not isinstance(m, float): continue
        if 0.25 <= m <= 0.60:
            k = round(m, 3); cnt[k] += 1; donde[k][nombre] += 1
ver(doc.modelspace(), 'MODEL')
for b in doc.blocks:
    if b.name.startswith('*D'): continue
    ver(b, b.name)
for k, v in sorted(cnt.items()):
    if v >= 2: print(k, v, dict(donde[k].most_common(4)))
