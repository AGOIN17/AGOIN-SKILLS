import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
pags = re.split(r'\n===== PAG (\d+) =====\n', t)
d = {int(pags[i]): pags[i+1] for i in range(1, len(pags), 2)}
for n in [int(x) for x in sys.argv[2].split(',')]:
    print(f'=== p{n} ===')
    print(' '.join(d[n].split()))
