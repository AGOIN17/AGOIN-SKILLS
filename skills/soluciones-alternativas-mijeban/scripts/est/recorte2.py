import fitz, sys
d = fitz.open(sys.argv[1]); out = sys.argv[2]
def rec(n, nombre, a, b, c, e, dpi=110):
    p = d[n]; W, H = p.rect.width, p.rect.height
    p.get_pixmap(dpi=dpi, clip=fitz.Rect(a*W, b*H, c*W, e*H)).save(f'{out}_{nombre}.png')
rec(0, 'ley2', 0.875, 0.30, 0.985, 0.56, 170)
rec(0, 'c2nota', 0.30, 0.70, 0.48, 0.76, 200)
for n in (2, 3, 4):
    rec(n, f'p{n+1}a', 0.0, 0.0, 0.5, 0.55)
    rec(n, f'p{n+1}b', 0.45, 0.0, 0.87, 0.55)
    rec(n, f'p{n+1}c', 0.0, 0.45, 0.5, 1.0)
    rec(n, f'p{n+1}d', 0.45, 0.45, 0.87, 1.0)
