# Output Format Reference

Template for the terminal output of `/ticket-analysis`.

## Full Output Template

```
═══════════════════════════════════════════════════════
[TICKET-KEY] · [Title]
Type: [type] | Status: [status] | SP: [points or —]
═══════════════════════════════════════════════════════

📊 RESUMEN
   Fuentes analizadas:
   - Jira:       ✅ / ❌
   - Figma:      ✅ / ⚠️ (Playwright) / ❌ (no URL)
   - Confluence:  ✅ / ❌ (sin resultados)
   - Notion:      ✅ / ❌ (sin resultados)
   - Código:      ✅

   Datos identificados: [N]
   ✅ Claros: [N] | ⚠️ Parciales: [N] | ❌ Desconocidos: [N]

───────────────────────────────────────────────────────
📋 MAPA DE DATOS
───────────────────────────────────────────────────────

📋 [dato 1]
   ¿Qué es?        [definición o ❌ Sin definir]
   ¿De dónde viene? [fuente o ❌ Desconocido]
   ¿Quién lo genera? [actor o ❌ Desconocido]
   ¿Cuándo?        [condición o ❌ Sin especificar]
   ¿Qué valores?   [restricciones o ❌ Sin restricciones conocidas]
   ─────
   En ticket:      [cómo se menciona o "No mencionado"]
   En diseño:      [cómo aparece o "No aparece" o "Sin diseño"]
   En código:      [Entity.field (tipo) o "No existe"]
   En docs:        [link o "No documentado"]
   ─────
   Estado:         [✅ / ⚠️ / ❌]
   Preguntas:      [lista]

[repetir para cada dato]

───────────────────────────────────────────────────────
⚡ CRUCES PROBLEMÁTICOS
───────────────────────────────────────────────────────

👻 Datos fantasma (en ticket/diseño, no en código):
   - [dato]: mencionado en [fuente], no existe en código

🔇 Datos huérfanos (en código, no en ticket/diseño):
   - [Entity.field]: existe en código, no mencionado en ticket

💥 Contradicciones:
   - [dato]: código dice [X], diseño dice [Y], ticket dice [Z]

❓ Sin origen conocido:
   - [dato]: existe pero no se encontró quién lo genera

📝 Sin reglas documentadas:
   - [dato]: existe pero no hay condiciones de cuándo/cómo cambia

(Omitir secciones vacías)

───────────────────────────────────────────────────────
🔴 BLOCKERS (negocio — necesitan respuesta del PO)
───────────────────────────────────────────────────────

1. "[texto citado del ticket]"
   → Técnico: [pregunta específica]
   → Para PO: [pregunta reformulada sin jerga técnica]

───────────────────────────────────────────────────────
🟡 BLOCKERS (técnicos — el equipo dev puede resolver)
───────────────────────────────────────────────────────

2. "[texto citado]"
   → [pregunta]

───────────────────────────────────────────────────────
🟢 NICE TO HAVE
───────────────────────────────────────────────────────

3. "[texto citado]"
   → [pregunta]

───────────────────────────────────────────────────────
🎨 DISEÑO
───────────────────────────────────────────────────────

Fuente: [Figma MCP / Playwright screenshot / No disponible]

Campos en UI:
┌─────────────┬──────────┬──────────┬─────────────┬──────────┐
│ Label       │ Tipo     │ Formato  │ Obligatorio │ Editable │
├─────────────┼──────────┼──────────┼─────────────┼──────────┤
│ [label]     │ [type]   │ [format] │ [sí/no/❓]  │ [sí/no]  │
└─────────────┴──────────┴──────────┴─────────────┴──────────┘

Estados:
✅ Cubiertos: [lista]
❌ Faltantes: [lista]

Correspondencia código ↔ diseño:
- En UI sin código: [campos]
- En código sin UI: [campos]

───────────────────────────────────────────────────────
📄 DOCUMENTACIÓN
───────────────────────────────────────────────────────

Encontrada:
- [Título] — [link]: "[cita relevante]"

Gaps:
- [concepto] — no documentado en ninguna fuente

───────────────────────────────────────────────────────
⚠️ VALIDACIONES ESTRUCTURALES
───────────────────────────────────────────────────────

[✅/❌] Descripción: [presente y suficiente / ausente o < 20 palabras]
[✅/❌] Criterios de aceptación: [presentes / ausentes]
[✅/❌] Link a Figma: [presente / ausente (y se necesita)]
[✅/❌] Story points: [estimados / sin estimar]
[✅/❌] Subtareas: [existen / faltan (descripción sugiere múltiples pasos)]

═══════════════════════════════════════════════════════
📦 SCOPE — QUÉ SE ENTREGA
═══════════════════════════════════════════════════════

✅ SE ENTREGA (con la info disponible):
   - [item concreto]: [qué se implementa exactamente]
   - [item concreto]: [qué se implementa exactamente]

❌ NO SE ENTREGA:
   - [item]: [razón concreta]
   - [item]: [razón concreta]

🚧 BLOQUEADO (no se puede entregar sin respuesta):
   - [item]: bloqueado por pregunta #[N]
   - [item]: bloqueado por pregunta #[N]

⚠️ ASUMIDO (se entrega con supuestos — confirmar):
   - [item]: "Se asume que [supuesto]. Si no es así, [impacto]."

═══════════════════════════════════════════════════════
```

## Section Rules

- **Omit empty sections** — if no contradictions found, don't show "Contradicciones"
- **Number questions sequentially** across all blocker/nice-to-have sections
- **Link blocker numbers to scope items** — "bloqueado por pregunta #3"
- **Data map goes first** — it's the core of the analysis
- **Scope goes last** — it's the conclusion derived from everything above
- **Never invent items** — if a section would be speculative, omit it or mark with ❓

## Glossary Entry Template

For `docs/glossary.md` updates:

```markdown
## [Nombre en español] ([Entity name in code])
- **Qué es**: [definición de negocio — NO técnica]
- **De dónde viene**: [quién lo crea y cuándo — evento, usuario, seed, cálculo]
- **Campos clave**:
  - `fieldName`: [significado en lenguaje de negocio]
  - `fieldName`: [significado en lenguaje de negocio]
- **Condiciones**: [cuándo cambia de estado, reglas de negocio conocidas]
- **Fuente de verdad**: [sistema o proceso que origina este dato]
- **Última revisión**: [YYYY-MM-DD — TICKET-KEY]
```

Rules:
- Only add data confirmed from code or documentation
- Mark unconfirmed with ❓ prefix
- Update `Última revisión` with each analysis
- Keep definitions in business language, not technical
