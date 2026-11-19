"""Figura 3 del informe (EST_03, planta baja) sin los rótulos de espesor: quita «20+5cm» y deja «M.C.24» en «M.C.».
Trabaja sobre el PDF abierto en memoria; el original no se toca.
Uso: python fig3_sin_espesores.py <PDF de láminas> <jpg de salida>"""
import sys, re, fitz
d = fitz.open(sys.argv[1]); p = d[3]; W, H = p.rect.width, p.rect.height
CLIP = fitz.Rect(0.08 * W, 0.245 * H, 0.82 * W, 0.80 * H)
n_forj = n_mc = 0
for b in p.get_text('rawdict')['blocks']:
    for l in b.get('lines', []):
        for s in l['spans']:
            txt = ''.join(c['c'] for c in s['chars'])
            for m in re.finditer(r'20\+5\s*cm|M\.C\.\s*(24(?:\s*cm)?)', txt):
                if m.group(0).startswith('M'):
                    i0, i1 = m.span(1); n_mc += 1
                else:
                    i0, i1 = m.span(0); n_forj += 1
                for c in s['chars'][i0:i1]:
                    p.add_redact_annot(fitz.Rect(c['bbox']), fill=False)
p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
quedan = [w[4] for w in p.get_text('words', clip=CLIP) if re.search(r'20\+5|M\.C\.24|\b24\b|^cm$', w[4])]
print(f'quitados: {n_forj} «20+5cm» y {n_mc} «24» de «M.C.24»; quedan en el recorte: {quedan}')
assert n_forj >= 14 and n_mc >= 25 and not quedan
pix = p.get_pixmap(dpi=110, clip=CLIP)
pix.save(sys.argv[2], jpg_quality=88)
print('guardado', sys.argv[2], pix.width, pix.height)
