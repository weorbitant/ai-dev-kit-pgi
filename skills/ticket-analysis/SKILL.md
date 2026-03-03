---
name: ticket-analysis
description: Use when doing comprehensive ticket analysis before implementation. Analyzes Jira ticket, Figma designs, Confluence/Notion docs, and codebase to produce a data map where every field is questioned and scope is explicitly defined. Use when user says "analiza ticket", "ticket analysis", "prepara ticket", "revisar ticket completo", or "qué falta en este ticket".
argument-hint: "[TICKET-KEY or URL]"
allowed-tools: Read, Grep, Glob, Bash, Agent, AskUserQuestion, ToolSearch, Edit, Write, mcp__claude_ai_Atlassian__getJiraIssue, mcp__claude_ai_Atlassian__editJiraIssue, mcp__claude_ai_Atlassian__addCommentToJiraIssue, mcp__claude_ai_Atlassian__searchConfluenceUsingCql, mcp__claude_ai_Atlassian__getConfluencePage, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Figma__get_design_context, mcp__claude_ai_Figma__get_screenshot
---

# Ticket Analysis

Analyze a ticket across 4 sources (Jira, Figma, docs, code) and produce a structured report with fixed format.

## Language

Instructions in this file are in English (for LLM processing). ALL user-facing output MUST be in Spanish, following the template in [references/output-format.md](references/output-format.md).

## Core Principles

1. **Zero assumptions** — if there is the slightest doubt, ask. Never write "se asume que...". Write a question instead.
2. **Traceability** — every finding must cite its source (page title + URL, or file path + line).
3. **Fixed structure** — the output ALWAYS has the same 8 sections in the same order. See [references/output-format.md](references/output-format.md).

## Configuration

- **Confluence Cloud ID:** `afianza-ac.atlassian.net`

## Instructions

### Phase 1: Fetch ticket

Parse `$ARGUMENTS` to extract ticket key. Can be:
- Key: `DEVPT-52` → use as-is
- URL: extract from `selectedIssue=DEVPT-52` or `/browse/DEVPT-52`

```
ToolSearch → "select:mcp__claude_ai_Atlassian__getJiraIssue"
mcp__claude_ai_Atlassian__getJiraIssue(cloudId: "afianza-ac.atlassian.net", issueIdOrKey: "<key>")
```

Extract from ticket content:
- Figma URLs (`figma.com/design/...`, `figma.com/file/...`)
- Confluence URLs (`afianza-ac.atlassian.net/wiki/...`)
- Notion URLs
- ALL data terms: every noun that could be a field, entity, concept, state, or action. Do not filter.

### Phase 2: Parallel analysis

Launch up to 3 agents in parallel using the `Agent` tool. Each agent must receive **complete instructions** — they cannot access skill definitions.

**IMPORTANT**: If any agent fails or returns incomplete data, do NOT retry. Report the failure in FUENTES as `⚠️ Error al analizar [source]: [reason]` and continue with the sources that did succeed.

**Agent 1 — Design** (skip if no Figma URLs):

Prompt must include:
- The Figma URL(s) to analyze
- Instructions to first read the skill file: `Read ~/.claude/skills/analyze-design/SKILL.md` then follow its instructions
- Use `ToolSearch` to load `mcp__claude_ai_Figma__get_design_context` and `mcp__claude_ai_Figma__get_screenshot`
- For each field/input: extract label, type, format, required?, editable?
- For each button/action: what it does, confirmation step?, success/error states?
- Detect covered and missing UI states (empty, loading, error, success, pagination)
- If Figma MCP fails, report it — do NOT attempt Playwright

**Agent 2 — Documentation:**

Prompt must include:
- The key terms to search (extracted from ticket in Phase 1)
- Any Confluence/Notion URLs found in the ticket
- Instructions to first read the skill file: `Read ~/.claude/skills/analyze-docs/SKILL.md` then follow its instructions
- Confluence Cloud ID: `afianza-ac.atlassian.net`
- Use `ToolSearch` to load Atlassian and Notion MCP tools
- Return direct quotes (never paraphrase), business rules, contradictions between sources
- If a platform is unreachable, report it and continue with the other

**Agent 3 — Data model:**

Prompt must include:
- The entity/concept names to analyze (extracted from ticket in Phase 1)
- Instructions to first read the skill file: `Read ~/.claude/skills/analyze-data-model/SKILL.md` then follow its instructions
- For each field: trace origin (who creates it), mutations (who changes it), validations, possible values
- Map relationships between entities (direction, cardinality, cascade behavior)
- Check migrations for recent schema changes

**Inline — Ticket clarification** (main thread, while agents run):
- Detect author's open questions
- Analyze ambiguities
- Structural validations (description, ACs, Figma link, SP, subtasks)

### Phase 3: Cross-reference

Once all agents return, build a flat data table. For EACH data element from ANY source, assign status:

- ✅ **Claro** — fully understood: what it is, where it comes from, what values it has
- ❓ **Dudoso** — partially known, has open questions. MUST have at least one question.
- ❌ **No existe** — mentioned in ticket/design but not found in code/docs. MUST have at least one question.

Detect cross-reference problems:
- Ghost data (in ticket/design, not in code)
- Orphan data (in code, not in ticket/design)
- Contradictions between sources
- Data without known origin
- Data without documented rules

### Phase 4: Build questions

Group ALL questions by who must answer:

**PARA EL PO / NEGOCIO** — non-technical language, with concrete example, stating what it blocks.
**PARA EL TECH LEAD / EQUIPO DEV** — technical questions the team resolves internally.
**PARA DISEÑO** — missing UI states, undefined flows, design gaps.

Each question gets a sequential number (#1, #2, ...) referenced in SCOPE and PRÓXIMOS PASOS.

### Phase 5: Define scope

- **SE ENTREGA** — only items with ✅ data and no blocking questions
- **NO SE ENTREGA** — explicitly excluded items with reason
- **BLOQUEADO** — items waiting on specific question numbers

There is NO "Asumido" section. If there's doubt, it's a question.

### Phase 6: Build next steps

Ordered by priority (what unblocks the most first):
- Each step has a responsible role and references the question it unblocks
- Separate "SE PUEDE EMPEZAR YA" from "REQUIERE RESPUESTA PRIMERO"

### Phase 7: Output

Display the full analysis using the EXACT format in [references/output-format.md](references/output-format.md).

ALL 8 sections ALWAYS appear. If a section has no content, show "Ninguno" or "No aplica".

### Phase 8: Offer actions

Ask the user (multiselect):

1. **Comment on Jira** — post technical analysis + questions as comment
2. **Update description** — add PO questions + proposed scope to ticket description
3. **Update glossary** — add/update entries in `docs/glossary.md`
4. **None**

If commenting: `mcp__claude_ai_Atlassian__addCommentToJiraIssue` (cloudId: `afianza-ac.atlassian.net`).
If updating description: `mcp__claude_ai_Atlassian__editJiraIssue`. Preserve existing content. Only add/replace "Preguntas bloqueantes" and "Scope propuesto" sections.
If updating glossary: Read `docs/glossary.md`, add/update entries using this template:

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

Rules: Only add data confirmed from code or docs. Mark unconfirmed with ❓. Update `Última revisión`. Keep definitions in business language.

## Edge cases

- No Figma URLs → report in FUENTES as "No hay URL de Figma en el ticket". Still show DISEÑO section as "No aplica".
- Confluence/Notion empty → report in FUENTES. Continue with other sources.
- No matching entities in code → ticket describes new functionality. Note in FUENTES.
- No description → analyze summary, ACs, comments.
- Invalid ticket key → tell user and stop.
- Do NOT invent questions. If something is clear, say it's clear.
- Do NOT invent scope items. If there isn't enough info to define scope, say so in SCOPE.
