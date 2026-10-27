# Plantilla de skill

Pasos para crear una skill nueva:

1. Copia esta plantilla a `skills/<nombre-en-minusculas-con-guiones>/SKILL.md`.
2. Rellena las partes entre ángulos.
3. Borra lo que no uses.

```markdown
---
name: <nombre-en-minusculas-con-guiones>
description: <Qué hace, en una frase.> <Cuándo usarla: tareas, palabras y situaciones en que debe cargarse, aunque el usuario no la nombre.> (máximo unos 1.000 caracteres)
---

# <Título>

<Dos o tres líneas: para qué sirve y qué problema evita.>

## <Bloque 1: reglas o pasos>

- **<Regla.>** <Por qué: la corrección o el incidente que la originó, en una frase.>
- ...

## <Bloque 2>

...

## Trampas conocidas

- <Síntoma> → <causa> → <qué hacer>.

## Ejemplos que funcionan

- <Ruta a un script o documento de referencia, y en qué equipo está.>
```

## Carpetas opcionales

- `references/`: detalle largo que Claude lee solo cuando lo necesita. El `SKILL.md` dice cuándo leerlo.
- `scripts/`: código probado y reutilizable. Indica con qué versión de programa se probó.

## Antes de subirla

- [ ] Sirve para cualquier proyecto, no solo para uno.
- [ ] Cada regla lleva su porqué.
- [ ] No hay contraseñas, tokens, precios ni datos personales.
- [ ] No contradice otra skill del repositorio.
- [ ] La has probado en una sesión nueva.
- [ ] Has subido `version` en `.claude-plugin/plugin.json`.
