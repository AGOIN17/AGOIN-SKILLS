from medir import lineas
for t, h, w in (
  ("El panel sándwich del proyecto, con friso de abeto visto, sobre cerchas a 1,20 m como máximo apoyadas en un durmiente. El ladrillo sube y recoge el panel; canalón visto. Placa ventilada y teja sin mortero.", 2.53, 124.0),
  ("El panel sándwich del proyecto, con friso de abeto visto, sobre cerchas a 1,20 m como máximo y un durmiente. El ladrillo sube y recoge el panel; canalón visto. Placa ventilada y teja sin mortero.", 2.53, 124.0),
  ("Peto de ladrillo enrasado con el durmiente, que recoge el panel", 1.82, 28.6),
  ("Peto de ladrillo, enrasado con el durmiente; recoge el panel", 1.82, 28.6),
  ("150 × 200 mm, a calcular", 1.82, 1000),
  ("Banda impermeable contra la madera.", 1.93, 50.8),
  ("Banda que protege la madera; junta de espuma.", 1.93, 50.8),
  ("Banda contra la madera, junta y cinta estanca.", 1.93, 50.8),
  ("Durmiente de madera en lugar de viga de hormigón.", 1.93, 50.8),
  ("Sin empuje al muro", 1.67, 42),
  ("Cerchas y durmiente,", 1.62, 38)):
    l, ww = lineas(t, h, w); print(len(l), round(ww, 1), l)
