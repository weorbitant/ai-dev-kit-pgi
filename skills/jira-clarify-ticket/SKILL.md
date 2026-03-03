---
name: jira-clarify-ticket
description: Use when analyzing a Jira ticket for ambiguities, missing information, or unclear acceptance criteria. Use when user says "clarify ticket", "review ticket", "analyze ticket", or passes a Jira ticket key like DEVPT-XX. Reads the ticket from Jira, detects vague content, and generates concrete questions.
argument-hint: "[TICKET-KEY or URL]"
allowed-tools: Read, Grep, Glob, AskUserQuestion, mcp__claude_ai_Atlassian__getJiraIssue, mcp__claude_ai_Atlassian__editJiraIssue, mcp__claude_ai_Atlassian__addCommentToJiraIssue
---

# Clarify Ticket

Analyze a Jira ticket like a developer would, detecting ambiguities and generating concrete questions to improve ticket quality before starting work.

## Configuration

- **Cloud ID:** `afianza-ac.atlassian.net`
- **UI keywords** (for Figma validation): "pantalla", "diseño", "formulario", "botón", "vista", "UI", "interfaz", "modal", "dropdown", "tabla", "listado", "dashboard", "layout"

## Instructions

### 1. Parse the argument and fetch the ticket

The argument (`$ARGUMENTS`) can be either a ticket key or a full Jira URL. Extract the ticket key:

- **Key directly:** `DEVPT-127` → use as-is
- **URL:** `https://afianza-ac.atlassian.net/browse/DEVPT-127` → extract `DEVPT-127` (last path segment after `/browse/`)

**Always fetch the ticket from Jira** — never reuse data from a previous call or conversation context.

```
ToolSearch → select:mcp__claude_ai_Atlassian__getJiraIssue
mcp__claude_ai_Atlassian__getJiraIssue(cloudId: "afianza-ac.atlassian.net", issueIdOrKey: "<extracted key>")
```

If no argument is provided, ask the user for the ticket key.

### 2. Detect open questions from the author

Before your own analysis, scan the description and comments for sections the author left as unresolved:

- Headers like "Preguntas pendientes", "Preguntas bloqueantes", "Open questions", "Dudas", "TBD", "TODO", "Por definir"
- Inline markers like `?`, `TBD`, `por confirmar`

If found, collect them — they will be displayed in a dedicated section in the output.

### 3. Analyze the content

Read the ticket as a developer who needs to implement it. Classify each question by severity:

**Blocker** — cannot start work without an answer:
- Undefined core behavior or main flow
- Missing data source or format that drives the implementation
- Contradictions between description and ACs
- Missing data model fields required by the logic described
- References to external systems or entities with no defined integration
- Ambiguous business rules that lead to different implementations

**Nice to have** — can assume a reasonable default, but worth confirming:
- Vague terms ("appropriate", "should handle", "etc.", "as needed")
- Implicit design decisions not made explicit
- Unclear scope (does it include X or not?)
- Unspecified roles or permissions (who can do what?)
- Missing error handling or edge case behavior

**For each ambiguity found**, quote the original text and formulate 1-2 specific questions.

### 4. Check existing comments

Read the ticket's comments (if any are returned in the response). If a comment already answers one of your questions, **drop that question** — do not ask what has already been resolved.

### 5. Run structural validations

Check these fields and report any that fail:

| Validation | Fails when |
|---|---|
| Description | Missing or < 20 words |
| Acceptance criteria | Missing entirely |
| Figma link | Story type AND description/summary contains UI keywords (see Configuration) AND no figma.com link found |
| Story points | Not estimated (check the field, not just the description text) |
| Subtasks | Description suggests multiple steps but no subtasks exist |

### 6. Separate blockers by audience

Classify each **Blocker** from step 3 into two categories:

**Needs business decision** — the answer must come from a PO, stakeholder, or domain expert:
- Missing business rules or domain knowledge (deadlines, eligibility criteria, workflows)
- Undefined user-facing behavior (who does what, when, why)
- Contradictions in functional requirements
- Missing relationships between business concepts

**Technical only** — the dev team can resolve internally:
- Missing fields, indexes, or constraints
- API design choices (pagination, response format)
- Implementation patterns (cron config, lock mechanism)
- Error handling strategy

### 7. Reformulate business blockers for non-technical audience

Only for blockers classified as **"Needs business decision"** in step 6, create a non-technical version.

**Rules for reformulation:**
- Write as if explaining to a non-technical product owner or stakeholder
- Never use technical terms (FK, enum, entity, migration, endpoint, DTO, constraint, etc.)
- Focus on **what information is missing** and **why it prevents progress**, not on the technical gap
- Each question must be self-contained: someone reading it without context should understand the problem
- Include a concrete example when possible to make the question tangible
- End with the consequence: "Sin esto no podemos..." / "Without this we cannot..."

**Example transformation:**
- Technical: "La entidad Obligation no tiene campo `deadlineDay`. FK a Client requerida para constraint UNIQUE."
- Business: "¿Cuál es la fecha límite de presentación de cada obligación? Hoy solo tenemos el nombre y la periodicidad (ej: 'IVA Trimestral'), pero no sabemos qué día vence. Sin esta información no podemos generar tareas con fecha de vencimiento."

Technical-only blockers are **not reformulated** — they stay in technical language.

### 8. Display results in terminal

Use this exact format:

```
TICKET-KEY · Title
   Type: [type] | Status: [status] | SP: [points or —]

   Author's open questions (unresolved):
   - [each question found in step 2]

   Blockers (need business decision):

   1. "[quoted text from ticket]"
      -> Technical: [specific question]
      -> For PO: [reformulated non-technical question from step 7]

   Blockers (technical):

   2. "[quoted text from ticket]"
      -> [specific question]

   Nice to have:

   3. "[quoted text from ticket]"
      -> [specific question]

   Missing information:
   - [each failed validation]
```

Omit any section that has no items. If no ambiguities are found, say so explicitly — the ticket is well-written.

### 9. Offer actions

Ask the user which action to take (can select multiple):

1. **Add technical comment on Jira** — posts the full technical analysis (all blockers + nice to have) as a comment
2. **Update description with business questions** — replaces or adds a "Preguntas bloqueantes (requieren decisión de negocio)" section in the ticket description with ONLY the reformulated business blocker questions from step 7 (not technical blockers)
3. **Both**
4. **None**

#### If adding a technical comment:

Create ONE comment using this format:

```
🔍 Clarification review

**Author's open questions (still unresolved):**
- [question from the ticket itself]

**Blockers:**
- "[quoted text]"
  → [question]

**Nice to have:**
- "[quoted text]"
  → [question]

**Missing information:**
- [ ] [each failed validation as checklist item]
```

Use `mcp__claude_ai_Atlassian__addCommentToJiraIssue` with cloudId `afianza-ac.atlassian.net`.

#### If updating description with business questions:

Only include questions classified as **"Needs business decision"** from step 6, using the reformulated non-technical versions from step 7. **Do not include technical-only blockers** in this section — those belong in the comment.

Read the current description, then:

- If a "Preguntas bloqueantes" or "Preguntas pendientes" section already exists, **replace it** with the new content
- If no such section exists, **append it** at the end of the description

Use this format for the section:

```
### Preguntas bloqueantes (requieren decisión de negocio)

1. **[Short question title]** [Full reformulated question with example and consequence]

2. **[Short question title]** [Full reformulated question with example and consequence]
```

If there are no blockers, do not add the section. If replacing an existing section that had questions but the new analysis finds none, replace with:

```
### Preguntas bloqueantes (requieren decisión de negocio)

_Sin preguntas bloqueantes tras la revisión._
```

Use `mcp__claude_ai_Atlassian__editJiraIssue` with cloudId `afianza-ac.atlassian.net` to update the description field.

Omit empty sections. Use a neutral, professional tone.

## Edge cases

- If the ticket has no description at all, report it but still analyze whatever content exists (summary, ACs, comments).
- If the ticket key is invalid or not found, tell the user clearly and stop.
- Do NOT invent questions just to have output — if the ticket is clear and complete, say so.
- When updating the description, preserve ALL existing content outside the "Preguntas" section. Only modify that section.
- If the codebase is available, optionally cross-reference the ticket against actual entity definitions, enums, and existing endpoints to detect gaps the ticket author may have missed (e.g., missing fields, incompatible types, undefined integrations).
