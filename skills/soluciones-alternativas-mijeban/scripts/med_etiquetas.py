import sys, re, json
V = json.load(open(sys.argv[1], encoding="utf-8"))
OX, OY = 421600, 4412200
for v in V:
    print("##", v["hoja"])
    for e in v["ents"]:
        if e["t"] in ("TEXT", "MTEXT", "INSERT"):
            t = (e.get("txt") or e.get("blk") or "").strip()
            if re.search(r"\b(PV|VF|V)\s*-\s*\d", t):
                print(f"   {e['l']:12s} {e['t']:6s} ({e['p'][0]-OX:7.2f},{e['p'][1]-OY:7.2f}) {t[:40]!r}")
