"""Figura 1 del informe (EST_00) sin la nota «Forjado PB autoportante 25+5 (30 cm), cara sup. 514,90.»:
la nota es imagen, así que se sube el resto de notas 15 px y se blanquea lo que sobra. Medido a ojo en fig1_est00.jpg.
Uso: python fig1_sin_espesor.py <fig1 de entrada> <fig1 de salida>"""
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert('RGB')
assert im.size == (3064, 1401), im.size
X0, X1 = 2712, 2850                      # columna de notas
Y_NOTA, Y_SIG, Y_FIN = 1275, 1290, 1326  # empieza la nota del forjado, empieza la siguiente, fin de las notas
resto = im.crop((X0, Y_SIG, X1, Y_FIN))
im.paste(resto, (X0, Y_NOTA))
fondo = im.getpixel((X0 - 4, Y_FIN + 6))          # color del fondo de la lámina junto a las notas
im.paste(fondo, (X0, Y_NOTA + (Y_FIN - Y_SIG), X1, Y_FIN))
im.save(sys.argv[2], quality=92)
im.crop((2700, 1200, 3064, 1340)).resize((364 * 3, 140 * 3)).save(sys.argv[2].replace('.jpg', '_notas.png'))
print('guardado', sys.argv[2])
