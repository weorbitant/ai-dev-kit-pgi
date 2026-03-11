---
name: adr
description: Use when creating, updating, or compacting Architecture Decision Records (ADRs). Use when user says "adr", "crear ADR", "create ADR", "actualizar ADR", "update ADR", "compactar ADR", "compact ADR", "registrar decision", "record decision", "decision record".
argument-hint: "[crear|actualizar|compactar] [slug or path]"
allowed-tools: Read, Grep, Glob, Bash, Agent, AskUserQuestion, ToolSearch, Edit, Write, mcp__atlassian__searchConfluenceUsingCql, mcp__atlassian__getConfluencePage, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch
---

# Architecture Decision Records

Create, update, or compact ADRs with cross-validated research.

## Language

Detect from user's message. Load the matching template:
- Spanish → [references/template-es.md](references/template-es.md)
- English → [references/template-en.md](references/template-en.md)

ALL output in the detected language.

## Modes

Parse `$ARGUMENTS`:

| Pattern | Mode |
|---|---|
| `crear/create <slug>` | **Create** — new ADR |
| `actualizar/update <path>` | **Update** — add log entry |
| `compactar/compact <path>` | **Compact** — reformat verbose ADR |
| No args or just a topic | **Create** — infer slug |

## Create

1. Extract context from conversation. Only ask if the topic or sources to check are unclear.
2. Launch `source-researcher` agent with: topic, sources to check, key terms. Instruct it to define domain concepts.
3. Draft ADR using research summary + language template. Context section must define domain concepts first, then the situation. Show draft before writing.
4. Write to `docs/adr/YYYY-MM-DD-<slug>.md`. Create directory if needed.
5. If researcher found discrepancies, list them as questions (conversation output, not in the ADR file).

## Update

1. Read existing ADR at given path.
2. Extract what was discussed/decided from conversation. Ask only if unclear.
3. If update involves technical decisions, optionally launch `source-researcher` to validate against code.
4. Append entry under Log/Registro with today's date. If the decision changed, update Decision and Status sections too.

## Compact

1. Read verbose ADR. Identify decisions buried in noise, redundancies, missing sections.
2. Rewrite following language template: preserve all decisions and rationale, discard meeting logistics, consolidate pros/cons into Alternatives, move chronological details to Log, keep technical references.
3. Show what changed before writing.

## Rules

- Context must be grounded in sources, not assumptions
- Alternatives must have pros AND cons
- Log is append-only
- If uncertain, it's an open question — never a stated fact
- Max ~200 lines per ADR; split if longer
