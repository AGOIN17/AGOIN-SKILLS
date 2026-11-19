import sys, json, re
d = json.load(open(sys.argv[1], encoding='utf-8'))
pat = re.compile(sys.argv[2], re.I)
full = len(sys.argv) > 3
for p in d['partidas']:
    if pat.search(p['resumen']) or pat.search(p['texto']):
        print(f"\n[{p['cod']}] cap {p['cap']} · {p['ud']} · {p['cant']} · {p['resumen']}")
        t = p['texto']
        print('   ', t if full else t[:300])
        if full:
            for l in p['lineas']:
                print('     |', ' | '.join(l))
