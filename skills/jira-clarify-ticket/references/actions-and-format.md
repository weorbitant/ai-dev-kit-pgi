# Actions and Output Format

## Separate blockers by audience

Classify each **Blocker** into two categories:

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

## Reformulate business blockers for non-technical audience

Only for blockers classified as **"Needs business decision"**, create a non-technical version.

**Rules for reformulation:**
- Write as if explaining to a non-technical product owner or stakeholder
- Never use technical terms (FK, enum, entity, migration, endpoint, DTO, constraint, etc.)
- Focus on **what information is missing** and **why it prevents progress**, not on the technical gap
- Each question must be self-contained: someone reading it without context should understand the problem
- Include a concrete example when possible to make the question tangible
- End with the consequence: "Sin esto no podemos..." / "Without this we cannot..."

**Example transformation:**
- Technical: "La entidad Obligation no tiene campo `deadlineDay`. FK a Client requerida para constraint UNIQUE."
- Business: "Cual es la fecha limite de presentacion de cada obligacion? Hoy solo tenemos el nombre y la periodicidad (ej: 'IVA Trimestral'), pero no sabemos que dia vence. Sin esta informacion no podemos generar tareas con fecha de vencimiento."

Technical-only blockers are **not reformulated** — they stay in technical language.

## Output format

Use this exact format for terminal display:

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

## Offer actions

Ask the user which action to take (can select multiple):

1. **Add technical comment on Jira** — posts the full technical analysis (all blockers + nice to have) as a comment
2. **Update description with business questions** — replaces or adds a "Preguntas bloqueantes (requieren decision de negocio)" section in the ticket description with ONLY the reformulated business blocker questions (not technical blockers)
3. **Both**
4. **None**

### If adding a technical comment:

Create ONE comment using this format:

```
Clarification review

**Author's open questions (still unresolved):**
- [question from the ticket itself]

**Blockers:**
- "[quoted text]"
  -> [question]

**Nice to have:**
- "[quoted text]"
  -> [question]

**Missing information:**
- [ ] [each failed validation as checklist item]
```

Use `mcp__claude_ai_Atlassian__addCommentToJiraIssue` with cloudId `afianza-ac.atlassian.net`.

### If updating description with business questions:

Only include questions classified as **"Needs business decision"**, using the reformulated non-technical versions. **Do not include technical-only blockers** in this section — those belong in the comment.

Read the current description, then:

- If a "Preguntas bloqueantes" or "Preguntas pendientes" section already exists, **replace it** with the new content
- If no such section exists, **append it** at the end of the description

Use this format for the section:

```
### Preguntas bloqueantes (requieren decision de negocio)

1. **[Short question title]** [Full reformulated question with example and consequence]

2. **[Short question title]** [Full reformulated question with example and consequence]
```

If there are no blockers, do not add the section. If replacing an existing section that had questions but the new analysis finds none, replace with:

```
### Preguntas bloqueantes (requieren decision de negocio)

_Sin preguntas bloqueantes tras la revision._
```

Use `mcp__claude_ai_Atlassian__editJiraIssue` with cloudId `afianza-ac.atlassian.net` to update the description field.

Omit empty sections. Use a neutral, professional tone. When updating the description, preserve ALL existing content outside the "Preguntas" section. Only modify that section.
