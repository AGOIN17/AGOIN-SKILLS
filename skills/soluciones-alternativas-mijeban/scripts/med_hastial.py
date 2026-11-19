import sys, json
V = json.load(open(sys.argv[1], encoding="utf-8"))
v = V[int(sys.argv[2])]
X0, X1, Y515 = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
seg = set()
for e in v["ents"]:
    if e["l"] not in ("ALZ_FIN", "ALZ_GRU") or e["t"] in ("HATCH", "INSERT"):
        continue
    for g in e.get("g", []):
        for (xa, ya), (xb, yb) in zip(g, g[1:]):
            if X0 - 0.6 <= min(xa, xb) and max(xa, xb) <= X1 + 0.6 and min(ya, yb) - Y515 > 3.0 and max(ya, yb) - Y515 < 5.5:
                dx, dy = xb - xa, yb - ya
                if abs(dx) > 0.5 and abs(dy) > 0.05:
                    seg.add((round(xa, 3), round(ya - Y515, 3), round(xb, 3), round(yb - Y515, 3), round(dy / dx, 3), e["l"]))
for s in sorted(seg):
    print(s)
