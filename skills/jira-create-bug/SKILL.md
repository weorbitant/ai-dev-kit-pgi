---
name: jira-create-bug
description: Use when creating a bug report in Jira, reporting an issue found during development or operations, or filing a ticket for a production problem. Use when user says "crea un bug", "reporta bug", "create bug", "file a bug", "abre un ticket", or "report issue".
argument-hint: "[brief description]"
allowed-tools: AskUserQuestion, ToolSearch, mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql, mcp__claude_ai_Atlassian__lookupJiraAccountId, mcp__claude_ai_Atlassian__createJiraIssue, mcp__claude_ai_Atlassian__editJiraIssue
model: sonnet
---

# Create Jira Bug

## Overview

Create well-structured bug reports in Jira with root cause analysis, evidence, and fix recommendations. Uses the DEVPT project and links to the appropriate epic.

## Process

1. **Gather information** — Understand what the bug is, evidence, and root cause if known
2. **Find the right epic** — Search for the relevant epic to link the bug to
3. **Create the bug** — With structured description
4. **Assign** — Ask user who to assign it to

## Finding the Epic

```
Search for epics in DEVPT project:
JQL: project = DEVPT AND issuetype = Epic AND (summary ~ "<keyword>") ORDER BY updated DESC
```

Common epics:
- **DEVPT-25** — "PGI - Bugs, Deuda técnica y mejoras" (catch-all for bugs and tech debt)

If unsure which epic, ask the user or default to DEVPT-25.

## Bug Description Template

Use this structure for the description:

```markdown
## Descripción
<What is happening and what should happen instead>

## Evidencia
- **Entorno**: DEV/PROD
- **Servicio**: <service name>
- <Specific evidence: error messages, message counts, log lines>

## Causa raíz
<Technical explanation of why this is happening>

## Fix requerido
<Specific code change needed, with file paths if known>

## Impacto
<What is affected: messages stuck, data not syncing, users impacted, etc.>
```

## Creating the Bug

Use the Atlassian MCP tools:

1. `searchJiraIssuesUsingJql` — Find the right epic
2. `lookupJiraAccountId` — Find the assignee's account ID
3. `createJiraIssue` — Create with:
   - `projectKey`: "DEVPT"
   - `issueTypeName`: "Bug"
   - `summary`: Concise, includes service name and what's broken
   - `description`: Structured markdown (template above)
   - `parent`: Epic key (e.g., "DEVPT-25")
4. `editJiraIssue` — Assign to the user

## Summary Guidelines

Good summaries:
- `backoffice-api: DTO de jiraRefs requiere summary y status como obligatorios, causando rechazo de mensajes en DLQ`
- `obligations-api: provided-service subscriber falla por campo faltante en erpRef`

Bad summaries:
- `Bug en el servicio` (too vague)
- `Error` (useless)

Format: `<service>: <what's broken and visible effect>`
