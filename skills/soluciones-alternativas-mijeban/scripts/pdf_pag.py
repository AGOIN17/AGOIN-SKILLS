import sys, fitz
d = fitz.open(sys.argv[1])
for n in (15, 16):
    p = d[n-1]
    print(n, len(p.get_images()), 'imagenes', len(p.get_drawings()), 'trazos')
    p.get_pixmap(dpi=80).save(sys.argv[2] + f'_p{n}.png')
