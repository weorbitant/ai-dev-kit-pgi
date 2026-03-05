# Output Format

Use this exact format for terminal display. ALL text must be in Spanish. No emojis — use text labels `[CRIT]` and `[WARN]` for severity.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPRINT REVIEW · [Sprint Name]
[N] tickets analizados · [M] pts estimados · [K] sin estimar
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCORECARD
  SISTEMICO: [N]/[T] sin descripcion · [N]/[T] sin AC · [N]/[T] sin estimar
  CRITICO: [N] sin asignar · [N] bloqueado · [N] duplicados
  WARNING: [N] lenguaje vago · [N] sobredimensionado

REQUIEREN MEJOR DESCRIPCIÓN PARA DIFERENCIAR

  TICKET-1 "Title 1" <-> TICKET-2 "Title 2"
  Motivo: Sin descripción no es posible determinar si el alcance se solapa.
  Accion: Describir ambas con alcance concreto para confirmar que no se pisan.

DUPLICADOS POTENCIALES

  TICKET-3 "Title 3" <-> TICKET-4 "Title 4"
  Motivo: [explicit reason why they deliver the same thing]
  Accion: Verificar con PO. Consolidar o diferenciar.

TICKETS CON HALLAZGOS
┌──────────┬──────────────────────────┬──────────────┬──────────┬──────────────────────────────────────┐
│ Ticket   │ Titulo                   │ Asignado     │ Status   │ Problema / Accion                    │
├──────────┼──────────────────────────┼──────────────┼──────────┼──────────────────────────────────────┤
│ TICKET-1 │ Short title              │ *SIN ASIG.*  │ To Do    │ [CRIT] Sin asignar → Asignar dueño   │
│          │                          │              │          │ [CRIT] Sin estimar → Estimar          │
├──────────┼──────────────────────────┼──────────────┼──────────┼──────────────────────────────────────┤
│ TICKET-2 │ Title here               │ Person Name  │ Blocked  │ [CRIT] Bloq:TICKET-99 → Resolver o   │
│          │                          │              │          │ sacar del sprint                     │
├──────────┼──────────────────────────┼──────────────┼──────────┼──────────────────────────────────────┤
│ TICKET-3 │ Title                    │ Person Name  │ In Prog. │ [WARN] Sobredim(8pts) → Descomponer  │
│          │                          │              │          │ en subtareas de max 5pts             │
└──────────┴──────────────────────────┴──────────────┴──────────┴──────────────────────────────────────┘

SIN HALLAZGOS ADICIONALES: TICKET-A, TICKET-B, TICKET-C, ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESUMEN DE RECOMENDACIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. [Most impactful recommendation with specific ticket keys]
  2. [Second recommendation]
  3. [...]

  Tickets listos para empezar: TICKET-A, TICKET-B, TICKET-C
  Tickets que necesitan trabajo previo: TICKET-D (asignar), TICKET-E (resolver bloqueo)
```

## Rules

- **Ticket-centric**: Each ticket appears ONCE in the table with all findings aggregated. Never repeat a ticket key across multiple sections.
- **No emojis**: Use `[CRIT]` and `[WARN]` text labels for severity.
- **Bordered table**: Use Unicode box-drawing characters for the table.
- **5 columns**: Ticket, Titulo, Asignado, Status, Problema/Accion.
- **Problema/Accion column**: Each line is `[SEVERITY] Problem → Action`. One line per finding.
- **Sort by severity**: Tickets with most critical findings appear first in the table.
- **Unassigned = Critical**: Display as `*SIN ASIG.*` in the Asignado column.
- **Duplicates separate**: Show duplicates BEFORE the table with explicit "Motivo".
- **"Requieren mejor descripción"**: Show BEFORE duplicates. For ticket pairs with similar titles but insufficient info to confirm overlap.
- Omit SCORECARD lines where count is 0.
- Omit DUPLICADOS POTENCIALES section if none found.
- Omit REQUIEREN MEJOR DESCRIPCIÓN section if none found.
- If no findings at all, display:
  ```
  SPRINT BIEN PREPARADO. No se encontraron problemas significativos.
  ```
  Still show the RESUMEN section to confirm readiness.
- Always show the RESUMEN DE RECOMENDACIONES section.
- Keep recommendations actionable and specific. Avoid generic advice.

## Systemic findings

- **Threshold:** If a single check affects >50% of filtered tickets, it becomes **SISTEMICO** in the scorecard.
- **Format:** `SISTEMICO: [N]/[T] sin descripcion · [N]/[T] sin AC` (showing count/total).
- **Table impact:** Tickets whose ONLY findings are systemic do NOT appear in the table. They go to "SIN HALLAZGOS ADICIONALES" line.
- **Table shows only differential findings:** A ticket appears in the table only if it has at least one non-systemic finding (blocked, unassigned, oversized, etc.).
- Systemic findings are still mentioned in RESUMEN DE RECOMENDACIONES as the top priority.

## Filtering (applied BEFORE analysis)

- **Exclude** tickets with status: `Done`, `Closed`, `Desestimada`
- **Exclude** issue type: `Sub-task`
- Header shows "N tickets analizados" (filtered count only)
