import fitz, sys
d = fitz.open(sys.argv[1]); out = sys.argv[2]
p = d[1]; W, H = p.rect.width, p.rect.height
for nombre, (a, b, c, e) in {'pl_ne': (0.55, 0.12, 0.85, 0.66), 'pl_no': (0.12, 0.12, 0.60, 0.50), 'pl_s': (0.12, 0.42, 0.85, 0.92)}.items():
    p.get_pixmap(dpi=100, clip=fitz.Rect(a*W, b*H, c*W, e*H)).save(f'{out}_{nombre}.png')
