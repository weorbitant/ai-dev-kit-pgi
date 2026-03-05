# Slack Output Format

Executive format for Slack. One single message whenever possible (max 5000 chars). Uses a code block for the table.

## Slack mrkdwn rules

- *bold* with single asterisks (NOT **double**)
- _italic_ with underscores
- `code` with backticks
- ``` for code blocks (used for the table)
- No emojis, no colored circles, no Unicode box-drawing outside code blocks
- No ## headers

## Format

```
*SPRINT REVIEW · [Sprint Name]*
[N] tickets analizados · [M] pts · [K] sin estimar ([X]%)

*Sistemico:* [N]/[T] sin desc · [N]/[T] sin AC · [N]/[T] sin estimar

*Resumen:* [N] sin asignar · [N] bloqueado externo · [N] sobredimensionado

*Requieren mejor descripcion para diferenciar:*
• DEVPT-X "Title X" ↔ DEVPT-Y "Title Y" — _sin descripcion, no se puede confirmar solapamiento_

*Duplicados potenciales:*
• DEVPT-A "Title A" ↔ DEVPT-B "Title B" — _motivo: [razón concreta]_

​```
Ticket     Titulo                          Asignado      Status   Problema / Accion
─────────  ──────────────────────────────  ────────────  ───────  ──────────────────────────────────
DEVPT-XX   Short title max 30 chars        SIN ASIGNAR   To Do    Sin asignar → Asignar dueño
DEVPT-YY   Another title                   Name S.       Blocked  Bloq:DEVPT-ZZ → Resolver o sacar
DEVPT-ZZ   Title here                      Name S.       In Prog  Sobredim(8pts) → Descomponer
​```

*Acciones prioritarias:*
1. [Most impactful action with specific ticket keys]
2. [Second action]
3. [...]

*Sin hallazgos adicionales:* DEVPT-A, DEVPT-B, DEVPT-C
```

## Rules

- **One message** whenever possible. Only split if exceeding 5000 chars.
- **No emojis, no colored circles.**
- **Table in code block** — fixed-width font renders aligned columns correctly in Slack.
- **5 columns**: Ticket, Titulo, Asignado, Status, Problema/Accion.
- **Only differential findings** in the table. Systemic findings go to the Sistemico line.
- **Unassigned** tickets show `SIN ASIGNAR` in the Asignado column.
- **Compact titles** — truncate to ~30 chars max.
- **Status abbreviations**: In Prog, Review, Blocked, To Do, QA.
- **Problema/Accion column**: `Problem → Action` format, one per line.
- **Sort** by severity: most critical findings first.
- **Acciones prioritarias**: max 5-7 numbered items, most impactful first, with specific ticket keys.
- **Sistemico** section replaces the old Resumen counts for findings >50%. Shows count/total.
- **Resumen** only shows non-systemic finding counts.
- **Omit** sections if empty (no duplicates, no "requieren descripcion", etc.).
- If sprint is healthy and table would be empty:
  `*Sprint bien preparado.* No se encontraron problemas significativos.`
