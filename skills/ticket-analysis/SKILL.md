---
name: ticket-analysis
description: Use when doing comprehensive ticket analysis before implementation. Analyzes Jira ticket, Figma designs, Confluence/Notion docs, and codebase to produce a data map where every field is questioned and scope is explicitly defined. Use when user says "analiza ticket", "ticket analysis", "prepara ticket", "revisar ticket completo", or "qué falta en este ticket".
argument-hint: "[TICKET-KEY or URL]"
allowed-tools: Read, Grep, Glob, Bash, Agent, AskUserQuestion, ToolSearch, mcp__claude_ai_Atlassian__getJiraIssue, mcp__claude_ai_Atlassian__editJiraIssue, mcp__claude_ai_Atlassian__addCommentToJiraIssue, mcp__claude_ai_Atlassian__searchConfluenceUsingCql, mcp__claude_ai_Atlassian__getConfluencePage, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Figma__get_design_context, mcp__claude_ai_Figma__get_screenshot
---

# Ticket Analysis

Comprehensive ticket analysis that interrogates every data element across 4 sources (Jira, Figma, documentation, code) and produces a unified data map with explicit scope.

## Core Principle

**Do not assume anything.** Every data element must be questioned:
- What does it mean exactly?
- Where does it come from? Who generates it?
- When is it generated? Under what conditions?
- What values can it have? What are the constraints?
- Who consumes it? For what purpose?

A field existing in code does NOT mean it is understood. A label in Figma does NOT mean the data is defined.

## Configuration

- **Confluence Cloud ID:** `afianza-ac.atlassian.net`

## Instructions

### Phase 1: Fetch ticket

Parse `$ARGUMENTS` — can be a ticket key (`DEVPT-52`) or URL (`https://afianza-ac.atlassian.net/browse/DEVPT-52`). Extract the key.

```
ToolSearch → "select:mcp__claude_ai_Atlassian__getJiraIssue"
mcp__claude_ai_Atlassian__getJiraIssue(cloudId: "afianza-ac.atlassian.net", issueIdOrKey: "<key>")
```

From the ticket, extract:
- **Figma URLs**: any `figma.com/design/...` or `figma.com/file/...` links
- **Confluence URLs**: any `afianza-ac.atlassian.net/wiki/...` links
- **Notion URLs**: any Notion links
- **ALL data terms**: every noun that could be a field, entity, concept, state, or action. Do not filter — collect everything, even obvious ones.

### Phase 2: Parallel analysis (launch 3 Agents)

Launch these 3 agents in parallel using the `Agent` tool:

**Agent 1 — Design analysis** (skip if no Figma URLs found):
```
Apply the logic of /analyze-design for each Figma URL found in the ticket.
Analyze: [list of Figma URLs]
For each design, extract every field, action, and state. Question everything.
Return structured output with: data fields found, actions, states covered/missing, questions.
```

**Agent 2 — Documentation search:**
```
Apply the logic of /analyze-docs.
Search Confluence (cloudId: afianza-ac.atlassian.net) and Notion for these terms: [key terms from ticket].
Also fetch these specific URLs if found: [Confluence/Notion URLs from ticket].
Return: definitions found (as direct quotes), business rules, contradictions, gaps.
```

**Agent 3 — Data model analysis:**
```
Apply the logic of /analyze-data-model.
Analyze these entities/concepts mentioned in the ticket: [entity/concept list].
For each field, trace: origin, mutations, validations, relationships.
Return structured field profiles with questions.
```

**Inline — Ticket clarification** (run in main thread while agents execute):

Apply the same logic as `/jira-clarify-ticket`:
- Detect author's open questions
- Analyze ambiguities (blockers vs nice-to-have)
- Separate by audience (business vs technical)
- Reformulate business blockers for PO
- Structural validations (description, ACs, Figma link, SP)

### Phase 3: Cross-reference — Interrogate each data element

Once all agents return, build a **data map**. For EACH data element identified from ANY source:

```
📋 [data name]
   ¿Qué es?        [definition found or "❌ Not defined"]
   ¿De dónde viene? [source: AMQP event / user input / calculation / seed / ❌ Unknown]
   ¿Quién lo genera? [service, external system, user / ❌ Unknown]
   ¿Cuándo?        [creation condition / ❌ Not specified]
   ¿Qué valores?   [enum, range, format / ❌ No known constraints]
   ─────
   En ticket:      [how it's mentioned or "Not mentioned"]
   En diseño:      [how it appears or "Not visible" or "No design"]
   En código:      [Entity.field (type) or "Does not exist"]
   En docs:        [link or "Not documented"]
   ─────
   Estado:         ✅ Clear / ⚠️ Partial / ❌ Unknown
   Preguntas:      [specific questions about this data element]
```

Flag cross-reference problems:
- **Ghost data**: mentioned in ticket/design but not in code or docs
- **Orphan data**: exists in code but not mentioned in ticket or design
- **Contradiction**: code type ≠ design format ≠ ticket description
- **No origin**: exists but nobody knows where it comes from
- **No rules**: exists but no documented conditions for when/how it changes

### Phase 4: Define scope

Based on ALL findings, produce an explicit scope. **Do not invent scope items that aren't supported by the analysis.**

**SE ENTREGA** — only items where:
- The data is understood (✅ or ⚠️ with reasonable assumption)
- The design exists (or is not needed)
- No blockers prevent implementation

**NO SE ENTREGA** — items explicitly excluded:
- Not mentioned in acceptance criteria
- Out of scope per ticket description
- Belongs to a different ticket

**BLOQUEADO** — items that cannot be delivered without answers:
- Linked to specific blocker questions
- Missing data definitions
- Missing design states

**ASUMIDO** — items delivered with assumptions:
- State the assumption clearly
- State the impact if the assumption is wrong

### Phase 5: Output

Display the full analysis in terminal using the format in [references/output-format.md](references/output-format.md).

### Phase 6: Offer actions

Ask the user (multiselect):

1. **Comment on Jira** — post full technical analysis + data map as comment
2. **Update description** — add business blocker questions for PO + proposed scope
3. **Update glossary** — add/update entries in `docs/glossary.md`
4. **None**

#### If commenting on Jira:

Use `mcp__claude_ai_Atlassian__addCommentToJiraIssue` with cloudId `afianza-ac.atlassian.net`. Include data map summary + all questions.

#### If updating description:

Use `mcp__claude_ai_Atlassian__editJiraIssue`. Add/replace sections:
- "Preguntas bloqueantes (requieren decisión de negocio)" — only business blockers, reformulated
- "Scope propuesto" — what will be delivered, what won't, what's blocked

Preserve all existing description content outside these sections.

#### If updating glossary:

Read `docs/glossary.md` (create if doesn't exist). For each data element with status ✅ or ⚠️, add or update an entry. Mark unconfirmed data with ❓.

## Edge cases

- If no Figma URLs in ticket, skip design analysis. Report as gap in output.
- If Confluence/Notion return nothing, report as gap. Continue with other sources.
- If no entities match in code, the ticket may describe new functionality. Note this explicitly.
- If the ticket has no description, analyze whatever exists (summary, ACs, comments).
- If ticket key is invalid, tell user and stop.
- Do NOT invent questions to fill sections. If something is clear, say it's clear.
- The scope section must NEVER include items not supported by the analysis. If there isn't enough information to define scope, say so.
