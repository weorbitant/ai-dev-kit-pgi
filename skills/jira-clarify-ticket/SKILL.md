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

### 6-9. Classify, reformulate, display, and act

Follow the detailed instructions in [references/actions-and-format.md](references/actions-and-format.md) for:
- Separating blockers by audience (business vs technical)
- Reformulating business blockers for non-technical stakeholders
- Terminal output format
- Jira actions (comment and/or description update)

## Edge cases

- If the ticket has no description at all, report it but still analyze whatever content exists (summary, ACs, comments).
- If the ticket key is invalid or not found, tell the user clearly and stop.
- Do NOT invent questions just to have output — if the ticket is clear and complete, say so.
- When updating the description, preserve ALL existing content outside the "Preguntas" section. Only modify that section.
- If the codebase is available, optionally cross-reference the ticket against actual entity definitions, enums, and existing endpoints to detect gaps the ticket author may have missed (e.g., missing fields, incompatible types, undefined integrations).
