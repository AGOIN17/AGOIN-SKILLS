import sys, re, fitz
res = fitz.open(sys.argv[1])
print("=== RESUMEN (capítulos)")
for p in res:
    for l in p.get_text().splitlines():
        if re.match(r"^\s*\d{2}\s", l) or re.search(r"CAP[IÍ]TULO", l, re.I):
            print("  ", l.strip()[:100])
med = fitz.open(sys.argv[2])
texto = "\n".join(f"<<p{i+1}>>\n" + p.get_text() for i, p in enumerate(med))
# partidas: código NN.NN seguido de unidad y título en mayúsculas
pat = re.compile(r"\n(\d{2}\.\d{2}(?:\.\d{2})?)\n(m2|M2|m²|Ml|ml|m|Ud|ud|u|m3|M3|kg|PA|Pa)\s+([^\n]+)\n", re.I)
claves = re.compile(r"FACHADA|CERRAMIENTO|F[ÁA]BRICA|LADRILLO|TOSCO|TERMOARCILLA|AISLAMIENTO|TRASDOSADO|SATE|MONOCAPA|ENFOSCADO|"
                    r"PIEDRA|LAJA|MAMPOST|CHAPADO|APLACADO|REVESTIMIENTO|DINTEL|VIERTEAGUAS|ALBARDILLA|YESO|ENLUCIDO", re.I)
for m in pat.finditer(texto):
    cod, ud, tit = m.groups()
    if claves.search(tit):
        ini = m.end()
        bloque = texto[ini: ini + 1500]
        pag = texto[:m.start()].count("<<p")
        desc = bloque.split("\n")
        d = " ".join(desc[:6])
        nums = re.findall(r"\n(\d{1,3}(?:\.\d{3})*,\d{2})\n0,00\n0,00", texto[ini: ini + 6000])
        print(f"\n[{cod}] p{pag} {ud} {tit.strip()}\n    {d[:400]}\n    total: {nums[0] if nums else '?'}")
