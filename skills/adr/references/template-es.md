# Template ADR — Español

Usar este template cuando el idioma detectado sea español.

## Formato

```markdown
# [Título descriptivo de la decisión]

**Fecha inicio**: YYYY-MM-DD
**Estado**: Propuesto | En discusión | Aceptado | Deprecado | Reemplazado por [ADR-xxx]
**Decisores**: [nombres, roles, o "equipo"]

## Contexto

[Definir los conceptos clave del dominio involucrados. Qué es cada entidad, por qué existe,
cómo se relaciona con el problema. Cualquiera que lea el ADR debe poder entenderlo sin
buscar en otro sitio.]

[Situación actual del sistema. Qué motivó que se tuviera que tomar esta decisión.]

## Problema

[Qué necesitamos resolver concretamente. Una descripción enfocada del problema,
no de la solución.]

## Alternativas

### Opción A: [Nombre descriptivo]

[Descripción breve de la alternativa.]

- **Pros**: [ventajas concretas]
- **Cons**: [desventajas concretas]

### Opción B: [Nombre descriptivo]

[Descripción breve de la alternativa.]

- **Pros**: [ventajas concretas]
- **Cons**: [desventajas concretas]

[Añadir más opciones si las hay.]

## Registro

### YYYY-MM-DD

- [Qué se investigó, discutió o decidió ese día]
- [Hallazgos relevantes]
- [Pendientes identificados]

## Decisión

[Qué se eligió y por qué. Referencia a la opción elegida de la sección Alternativas.
Si aún no se ha decidido, dejar esta sección vacía o indicar "Pendiente de decisión".]

## Consecuencias

### Positivas

- [Beneficio concreto]

### Negativas / Trade-offs

- [Coste o riesgo aceptado]
```

## Reglas de estilo

- Lenguaje directo, sin rodeos
- Frases cortas
- Usar listas cuando hay más de 2 elementos
- Código inline con backticks para nombres técnicos (`EntityManager`, `deadline_config`)
- Bloques de código para ejemplos de más de una línea
- No usar emojis
- Secciones vacías: escribir "Pendiente" o "No aplica", nunca eliminar la sección
