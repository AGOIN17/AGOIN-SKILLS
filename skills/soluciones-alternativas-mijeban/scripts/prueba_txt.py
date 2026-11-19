from medir import lineas
c = [
 "El panel sándwich del proyecto, con su friso de abeto visto, sobre cerchas a 1,20 m como máximo y sin durmiente. El ladrillo sube y recoge el panel; canalón visto. Placa ventilada y teja sin mortero.",
 "El panel sándwich del proyecto, con friso de abeto visto, sobre cerchas a 1,20 m como máximo y sin durmiente. El ladrillo sube y recoge el panel; canalón visto. Placa ventilada y teja sin mortero.",
 "Panel sándwich del proyecto, con friso de abeto visto, sobre cerchas a 1,20 m como máximo, sin durmiente. El ladrillo sube y recoge el panel; canalón visto. Placa bajo teja ventilada y teja sin mortero.",
]
for t in c:
    l, w = lineas(t, 2.53, 124.0); print(len(l), round(w,1), l)
for t, h, w in (("Peto de ladrillo tosco que sube y recoge el panel", 1.82, 28.6), ("Par de cercha GL24h 140 × 180 sobre el tosco", 1.82, 28.6),
                ("Junta de espuma contra el ladrillo y cinta estanca", 1.82, 28.6), ("Canalón visto anclado al ladrillo, con goterón", 1.82, 28.6),
                ("a soga, de 10,6 cm", 1.82, 1000), ("a 1,20 m máx.; sin durmiente", 1.82, 1000),
                ("Proyecto: pares, atado «opcional»", 1.67, 42), ("Sin empuje al muro ni durmiente", 1.67, 42),
                ("Cerchas a 1,20 m como máximo (proyecto: pares hasta 1,83 m).", 1.93, 50.8), ("Sin durmiente: la cercha apoya en el tosco.", 1.93, 50.8),
                ("Canalón visto, anclado al ladrillo.", 1.93, 50.8), ("Teja con espuma y cumbrera en seco.", 1.93, 50.8), ("Junta de espuma y cinta estanca.", 1.93, 50.8),
                ("Panel con cinta en juntas, Onduline y cobijas de derribo.", 1.93, 54.4)):
    l, ww = lineas(t, h, w); print(len(l), round(ww, 1), l)
