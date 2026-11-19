import sys, fitz, re
for path, out in zip(sys.argv[1::2], sys.argv[2::2]):
    d = fitz.open(path)
    txt = []
    for i, p in enumerate(d):
        txt.append(f"\n===== PAG {i+1} =====\n" + p.get_text())
    open(out, 'w', encoding='utf-8').write(''.join(txt))
    print(path[-30:], 'paginas', len(d), 'chars', sum(len(x) for x in txt))
