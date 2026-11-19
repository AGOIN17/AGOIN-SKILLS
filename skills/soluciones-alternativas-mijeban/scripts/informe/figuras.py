import fitz, sys
d = fitz.open(sys.argv[1]); out = sys.argv[2]
figs = {
  'fig1_est00': (0, (0.015, 0.035, 0.99, 0.665), 95),
  'fig2_est01': (1, (0.10, 0.075, 0.85, 0.915), 95),
  'fig3_est03pb': (3, (0.08, 0.245, 0.82, 0.80), 110),
  'fig4_est02': (2, (0.08, 0.18, 0.82, 0.895), 105),
  'fig5_apoyo': (0, (0.022, 0.70, 0.48, 0.985), 130),
}
for k, (n, (a, b, c, e), dpi) in figs.items():
    p = d[n]; W, H = p.rect.width, p.rect.height
    pix = p.get_pixmap(dpi=dpi, clip=fitz.Rect(a*W, b*H, c*W, e*H))
    pix.save(f'{out}\\{k}.jpg', jpg_quality=88)
    print(k, pix.width, pix.height)
