import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
pags = re.split(r'\n===== PAG (\d+) =====\n', t)
# pags: ['', '1', texto, '2', texto...]
d = {int(pags[i]): pags[i+1] for i in range(1, len(pags), 2)}
pat = re.compile(sys.argv[2], re.I)
lim = int(sys.argv[3]) if len(sys.argv) > 3 else 400
cnt = 0
for n in sorted(d):
    for m in pat.finditer(d[n]):
        a = max(0, m.start()-150); b = min(len(d[n]), m.end()+250)
        print(f'--- p{n}:', ' '.join(d[n][a:b].split()))
        cnt += 1
        if cnt >= lim: sys.exit()
