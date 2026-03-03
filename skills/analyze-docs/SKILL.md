---
name: analyze-docs
description: Use when searching for documentation about a concept, entity, or business term in Confluence and Notion. Extracts definitions and rules without interpretation. Use when user says "busca documentación", "qué dice confluence", "analyze docs", "busca en notion", "hay documentación sobre", or "qué sabemos de".
argument-hint: "[search term or URL]"
allowed-tools: Read, AskUserQuestion, ToolSearch, mcp__claude_ai_Atlassian__searchConfluenceUsingCql, mcp__claude_ai_Atlassian__getConfluencePage, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch
model: sonnet
---

# Analyze Docs

Search Confluence and Notion for documentation about a business concept. Extract definitions and rules as direct quotes — never interpret or paraphrase.

## Configuration

- **Confluence Cloud ID:** `afianza-ac.atlassian.net`

## Instructions

### 1. Parse argument

`$ARGUMENTS` can be:
- A Confluence URL → fetch that page directly
- A Notion URL → fetch that page directly
- Free text (concept/term) → search both platforms

If no argument, ask the user what to search for.

### 2. Search Confluence

```
ToolSearch → "select:mcp__claude_ai_Atlassian__searchConfluenceUsingCql"
```

Search with CQL using the terms. Try multiple queries (pass the CQL string directly as the `cql` parameter — no extra escaping needed):
- Exact term: `text ~ "obligación fiscal"`
- Individual words: `text ~ "obligación" AND text ~ "fiscal"`
- Related terms: synonyms, abbreviations, Spanish/English variants
- By title: `title ~ "obligación"`

For each relevant result, fetch the full page:
```
mcp__claude_ai_Atlassian__getConfluencePage(cloudId: "afianza-ac.atlassian.net", pageId: "<id>")
```

### 3. Search Notion

```
ToolSearch → "+notion search"
mcp__claude_ai_Notion__notion-search(query: "<terms>")
```

For each relevant result:
```
mcp__claude_ai_Notion__notion-fetch(url: "<page-url>")
```

### 4. Extract WITHOUT interpreting

For each document found, extract:

**Definitions** — Quote the exact text. Do not paraphrase.
```
"Una obligación es el compromiso fiscal o contable que..."
— Fuente: [Título página], Confluence, [link]
```

**Business rules** — Quote conditions, triggers, exceptions.
```
"El IVA trimestral se presenta antes del día 20 del mes siguiente..."
— Fuente: [Título página], Confluence, [link]
```

**Diagrams/flows** — Note their existence and describe what they show.

**Data definitions** — Any mention of fields, formats, allowed values.

### 5. Detect contradictions

If the same concept is defined differently in two sources, flag it:
```
⚠️ CONTRADICCIÓN:
   Confluence dice: "[quote A]" — [link A]
   Notion dice: "[quote B]" — [link B]
```

### 6. Output

```
📄 DOCUMENTACIÓN: "[término buscado]"

   CONFLUENCE:
   ┌──────────────────────────────────────────────────┐
   │ [Título página] — [link]                         │
   │ Definición: "[cita textual]"                     │
   │ Reglas: "[cita textual de reglas encontradas]"   │
   └──────────────────────────────────────────────────┘
   (repetir por cada página relevante)

   NOTION:
   ┌──────────────────────────────────────────────────┐
   │ [Título página] — [link]                         │
   │ Definición: "[cita textual]"                     │
   └──────────────────────────────────────────────────┘

   REGLAS DE NEGOCIO ENCONTRADAS:
   1. "[regla — cita directa]" — Fuente: [link]
   2. ...

   CONTRADICCIONES:
   - [fuente A] vs [fuente B]: [descripción]

   NO ENCONTRADO:
   - [términos buscados sin resultados en ninguna plataforma]

   COBERTURA:
   - Confluence: [X páginas encontradas / Y relevantes]
   - Notion: [X páginas encontradas / Y relevantes]
```

## Edge cases

- If Confluence MCP fails, report it and continue with Notion (and vice versa).
- If no results in either platform, say so explicitly — "No se encontró documentación sobre [término]".
- If a page is very long, extract only the sections relevant to the search term.
- Never synthesize or merge definitions from multiple sources. Present each source separately.
- If the argument contains multiple terms, search for each separately and then together.
