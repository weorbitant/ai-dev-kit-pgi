---
name: analyze-design
description: Use when analyzing Figma designs to extract data fields, UI states, and actions without assumptions. Uses Figma MCP with Playwright fallback. Use when user says "analiza diseño", "revisa el figma", "qué campos tiene el diseño", "analyze design", or shares a Figma URL for review.
argument-hint: "[figma-url]"
allowed-tools: Read, Bash, AskUserQuestion, ToolSearch, mcp__claude_ai_Figma__get_design_context, mcp__claude_ai_Figma__get_screenshot
---

# Analyze Design

Extract every data element, action, and state from a Figma design. Question everything — a label in the UI does NOT mean the data is defined.

## Instructions

### 1. Parse argument

`$ARGUMENTS` is a Figma URL. If not provided, ask the user.

Extract fileKey and nodeId from the URL:
- `figma.com/design/:fileKey/:fileName?node-id=:nodeId` → convert `-` to `:` in nodeId
- `figma.com/design/:fileKey/branch/:branchKey/:fileName` → use branchKey as fileKey

### 2. Get the design

**Attempt 1 — Figma MCP:**

```
ToolSearch → "select:mcp__claude_ai_Figma__get_design_context"
mcp__claude_ai_Figma__get_design_context(fileKey, nodeId)
mcp__claude_ai_Figma__get_screenshot(fileKey, nodeId)
```

**Fallback — Manual screenshot (if MCP fails or unavailable):**

Figma requires authentication, so automated screenshots are not possible. Ask the user:

> "No pude acceder al diseño via Figma MCP. ¿Puedes compartir un screenshot de la pantalla? Puedes arrastrarlo al chat o indicar la ruta del archivo."

Read the screenshot with `Read` for visual analysis.

If the user cannot provide a screenshot, report failure in the output and stop the design analysis.

### 3. Interrogate every element

**For each field/input — do NOT assume anything:**

| Question | Why |
|----------|-----|
| What label does it have? | Labels can be ambiguous ("Total" — total of what?) |
| What input type? (text, select, toggle, date...) | Determines data type |
| Has placeholder text? What does it suggest? | May hint at format/expected values |
| Is it required? How do you know? | If not marked, ask |
| What format? (currency, date, percentage...) | Determines validation rules |
| Is it editable or read-only? | Determines who generates the data |
| What are the possible values? | For selects/toggles, list them |

**For each table column:**

| Question | Why |
|----------|-----|
| What data does it show? | Column header may be abbreviated or ambiguous |
| Where does this data come from? | Not obvious from the design |
| What format? | Dates, numbers, currencies vary |
| Is it sortable/filterable? | Affects implementation |

**For each button/action:**

| Question | Why |
|----------|-----|
| What does it do? | Icon-only buttons are ambiguous |
| Is there a confirmation step? | Design may not show it |
| What happens on success? | Navigate? Toast? Refresh? |
| What happens on failure? | Error state may not be designed |
| Does it change data state? | Side effects must be known |

### 4. Detect covered and missing states

Check for each of these. Mark as covered or missing:

- Empty state (no data yet)
- Loading state
- Error state (API failure, validation errors)
- Success state / confirmation
- Partial data (some fields filled, some not)
- Permission denied (user can't access)
- Pagination / infinite scroll (if table/list)

### 5. Detect implicit flows

- What screens are connected? Is navigation designed?
- Are there modals/drawers that open? Are their contents designed?
- What happens after form submission? Is the next screen designed?
- Are there back/cancel flows?

### 6. Output

```
🎨 ANÁLISIS DE DISEÑO
   Fuente: [Figma MCP / Playwright screenshot]
   URL: [original URL]

   DATOS ENCONTRADOS:
   ┌─────────────┬──────────┬──────────┬─────────────┬──────────┐
   │ Label       │ Tipo     │ Formato  │ Obligatorio │ Editable │
   ├─────────────┼──────────┼──────────┼─────────────┼──────────┤
   │ [label]     │ [type]   │ [format] │ [sí/no/❓]  │ [sí/no]  │
   └─────────────┴──────────┴──────────┴─────────────┴──────────┘

   ACCIONES:
   - [botón/label]: acción=[X], confirmación=[sí/no/❓], error=[diseñado/no]

   ESTADOS:
   ✅ Cubiertos: [lista]
   ❌ Faltantes: [lista]

   FLUJOS:
   - [pantalla A] → [pantalla B]: [trigger]
   - ❓ [flujo implícito no diseñado]

   PREGUNTAS (cada dato que no está claro):
   1. "[label X]" — ¿Qué significa exactamente? ¿De dónde viene este dato?
   2. "[botón Y]" — ¿Qué pasa si falla? No hay estado de error diseñado.
   3. ...
```

## Edge cases

- If the URL is not a Figma URL, tell the user and stop.
- If the design is a component library (not a screen), adapt: list components and their props instead of flows.
- If multiple frames/pages exist, ask which one to analyze or analyze all.
- Never invent data that isn't visible in the design. If a field's meaning is unclear, ask — don't guess.
