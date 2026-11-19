import fitz, sys
d = fitz.open(sys.argv[1]); out = sys.argv[2]
p = d[0]; W, H = p.rect.width, p.rect.height
print(W, H)
for im in p.get_images(full=True):
    print('img', im[0], im[2], im[3], p.get_image_rects(im[0]))
# recortes en fracciones de la página (x0,y0,x1,y1)
cajas = {
 'leyenda': (0.875, 0.03, 0.985, 0.32),
 'notas': (0.875, 0.55, 0.985, 0.68),
 'zonas': (0.48, 0.67, 0.87, 0.78),
 'ejes': (0.48, 0.78, 0.87, 0.99),
 'corte2': (0.02, 0.72, 0.48, 0.99),
 'corte2b': (0.30, 0.70, 0.48, 0.90),
 'zonaA': (0.17, 0.15, 0.32, 0.25),
 'zonaB': (0.55, 0.46, 0.80, 0.52),
}
for k, (a, b, c, e) in cajas.items():
    r = fitz.Rect(a*W, b*H, c*W, e*H)
    p.get_pixmap(dpi=170, clip=r).save(f'{out}_{k}.png')
