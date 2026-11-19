"""Busca un patrón en un PDF y muestra página y contexto. Uso: python pdf_buscar.py <pdf> <regex> [ctx]"""
import sys, re, fitz
doc = fitz.open(sys.argv[1])
pat = re.compile(sys.argv[2], re.I)
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 160
for i, p in enumerate(doc):
    t = re.sub(r'\s+', ' ', p.get_text())
    for m in pat.finditer(t):
        a, b = max(0, m.start() - ctx), min(len(t), m.end() + ctx)
        print(f"p{i+1}: …{t[a:b]}…\n")
