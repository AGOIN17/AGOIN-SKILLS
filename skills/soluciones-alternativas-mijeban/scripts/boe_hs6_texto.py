import sys, re, fitz
d = fitz.open(sys.argv[1])
t = ''
for i, p in enumerate(d):
    s = p.get_text()
    if 'radón' in s or 'Radón' in s:
        t += f'\n<<p{i+1}>>\n' + s
t = re.sub(r'[ \t]+', ' ', t)
for pat in [r'3\.2[^\n]*\n', r'zona II', r'espacio de contención', r'despresurización']:
    for m in re.finditer(pat, t):
        print(f'[{pat}] …{re.sub(chr(10), " ", t[max(0, m.start()-300):m.end()+700])}…\n')
        break
