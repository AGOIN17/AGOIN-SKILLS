import sys, re, collections
f = open(sys.argv[1], encoding='utf-8', errors='replace')
lines = f.read().split('\n')
textos = collections.Counter(); capas = collections.Counter()
ent = None; layer = None
i = 0; n = len(lines)
cur = {}
while i < n - 1:
    c = lines[i].strip(); v = lines[i+1].rstrip('\r')
    if c == '0':
        if cur.get('t') in ('TEXT', 'MTEXT') and cur.get('txt'):
            textos[(cur.get('l'), cur['txt'][:80])] += 1
        if cur.get('t'):
            capas[(cur.get('l'), cur.get('t'))] += 1
        cur = {'t': v.strip()}
    elif c == '8':
        cur['l'] = v.strip()
    elif c == '1' and cur.get('t') in ('TEXT', 'MTEXT'):
        cur['txt'] = re.sub(r'\\[A-Za-z][^;]*;|[{}]', '', v.strip())
    i += 2
pil = sorted({t for (l, t) in textos if re.fullmatch(r'P\d+', t)}, key=lambda x: int(x[1:]))
print('pilares rotulados', len(pil), pil[:5], pil[-5:])
pat = re.compile(sys.argv[2], re.I)
for (l, t), k in sorted(textos.items(), key=lambda kv: -kv[1]):
    if pat.search(t):
        print(k, l, '|', t)
