import sys, re, fitz
d = fitz.open(sys.argv[1])
for i, p in enumerate(d):
    t = p.get_text()
    if 'Toledo' in t:
        j = t.find('Toledo')
        print('p', i + 1)
        print(re.sub(r'\s+', ' ', t[max(0, j - 400):j + 1200]))
        print('---')
