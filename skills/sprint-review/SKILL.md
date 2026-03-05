---
name: sprint-review
description: Use when evaluating a sprint before starting it. Detects duplicates, poorly defined tickets, missing acceptance criteria, estimation gaps, vague language, dependency risks, and balance issues. Use when user says "revisa sprint", "sprint review", "analiza sprint", "sprint health", "evalúa sprint", or provides a list of ticket keys for pre-sprint review.
argument-hint: "[BOARD-ID or TICKET-KEY,TICKET-KEY,... or empty for active sprint]"
allowed-tools: Agent, AskUserQuestion, ToolSearch, mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql, mcp__claude_ai_Atlassian__getJiraIssue, mcp__claude_ai_Slack__slack_send_message_draft, mcp__claude_ai_Slack__slack_search_channels
---

# Sprint Review

Evaluate a sprint's readiness before starting it. Detect quality issues across all tickets and produce a structured report with actionable recommendations.

## Language

Instructions in English (for LLM processing). ALL user-facing output MUST be in Spanish, following the format in [references/output-format.md](references/output-format.md).

## Configuration

- **Cloud ID:** `afianza-ac.atlassian.net`
- **Default project:** `DEVPT`
- **Oversized threshold:** 5 story points
- **Systemic threshold:** 50% of filtered tickets (findings above this become systemic)
- **Vague terms (ES):** "debería", "quizás", "posiblemente", "varios", "algunos", "etc.", "por definir", "TBD", "en general", "eventualmente", "se podría", "a futuro"
- **Vague terms (EN):** "should", "maybe", "possibly", "various", "some", "etc.", "TBD", "in general", "eventually", "could be", "as needed", "appropriate"

## Instructions

### Phase 1: Get sprint tickets

Parse `$ARGUMENTS` to determine input mode:

**Mode A — Sprint from Jira (default):**

If no arguments or a board ID is provided, fetch tickets from the next upcoming or active sprint.

```
ToolSearch → "select:mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql"
```

JQL options (try in order until one returns results):
1. `project = DEVPT AND sprint in futureSprints() ORDER BY rank ASC` (next sprint)
2. `project = DEVPT AND sprint in openSprints() ORDER BY rank ASC` (active sprint)

If a board ID is given as argument, use: `sprint in futureSprints() AND project = DEVPT`

**Mode B — Manual ticket list:**

If arguments contain comma-separated ticket keys (e.g., `DEVPT-100,DEVPT-101,DEVPT-102`), use those directly.

```
ToolSearch → "select:mcp__claude_ai_Atlassian__getJiraIssue"
```

Fetch each ticket individually using `mcp__claude_ai_Atlassian__getJiraIssue(cloudId: "afianza-ac.atlassian.net", issueIdOrKey: "<key>")`.

**For both modes**, extract from each ticket:
- Key, summary, description, acceptance criteria
- Issue type (Story, Bug, Task, Tech Debt, Sub-task)
- Story points (check `story_points` or `customfield_10016`)
- Status, assignee, labels
- Issue links (blocks, is blocked by, duplicates, relates to)
- Sprint name (for report header)

If no tickets are found, tell the user and stop.

### Phase 1.5: Filter tickets

Before running checks, filter the ticket list:

1. **Exclude completed tickets** — Remove any ticket with status `Done`, `Closed`, or `Desestimada`. These are not actionable.
2. **Exclude sub-tasks** — Remove issue type `Sub-task`. They are covered by their parent ticket.
3. Record the original total count for the header (e.g., "50 tickets total") but only analyze the filtered set (e.g., "24 tickets analizados").

### Phase 2: Run checks

Execute ALL checks against the **filtered** ticket list. Each check produces findings with a severity level.

#### Check 1: Duplicate detection

Detect tickets that describe **the same deliverable or scope of work** — i.e., doing one would make the other redundant.

**How to evaluate:**

1. Read the title AND description of each ticket to understand what it delivers.
2. Compare pairs only when titles suggest they could be about the same thing.
3. Flag as **duplicado potencial** ONLY when you can explain concretely why both tickets would produce the same outcome or change.

**What is NOT a duplicate:**
- Tickets in the same functional area but with different deliverables (e.g., "Importar datos empleados baja" vs "Incluir campos apartado baja empleado" — one imports data, the other adds UI fields).
- Tickets assigned to the same person in a similar status — that alone means nothing.
- Tickets that share keywords but do different things (e.g., three document tasks that each fix a different aspect).

**When there is not enough information:**
If two tickets have similar titles but lack description/AC to determine whether they overlap, do NOT flag them as duplicates. Instead, note them in a separate "Requieren mejor descripción para diferenciar" list — the problem is poor definition, not duplication.

**Severity:** Critical (only for confirmed potential duplicates)
**Output per finding:** The ticket keys, their titles, and a concrete explanation of WHY they appear to deliver the same thing.

#### Check 2: Definition quality

For each ticket, check:

| Validation | Fails when | Severity |
|---|---|---|
| Description missing | No description or < 20 words | Critical |
| Acceptance criteria missing | No ACs found (no "criterios", "AC", "acceptance", checklist, or Gherkin) | Critical |
| Description is vague | Description exists but is mostly high-level without concrete details (< 50 words of substance) | Warning |

**Output per finding:** Ticket key + which validation failed.

#### Check 3: Estimation gaps

For each ticket, check if story points are assigned. All tickets must have story points before entering a sprint.

**Severity:** Critical
**Output per finding:** List of unestimated ticket keys.

#### Check 4: Vague language

Scan title + description + ACs for terms from the vague terms lists (see Configuration).

**Severity:** Warning
**Output per finding:** Ticket key, the vague term found, and the surrounding sentence.

#### Check 5: External dependencies

For each ticket, check issue links:
- Links of type "is blocked by" pointing to tickets NOT in this sprint
- Links of type "is blocked by" pointing to tickets with status != Done/Closed

**Severity:** Critical
**Output per finding:** Ticket key, blocking ticket key, blocker's status, whether it's in the sprint.

#### Check 6: Sprint balance

Calculate (using the **filtered** set, excluding sub-tasks and Done):
- Count and percentage of each issue type (Story, Bug, Task/Tech Debt)
- Total story points
- Average story points per ticket (excluding unestimated)

No specific severity — this is informational. Flag if:
- Bugs > 40% of sprint (Warning: "Sprint dominated by bug fixes")
- No stories at all (Warning: "Sprint has no new feature work")
- Total points significantly different from typical (if detectable)

#### Check 7: Oversized tickets

Flag tickets with story points > threshold (see Configuration).

**Severity:** Warning
**Output per finding:** Ticket key, points, recommendation to decompose.

#### Check 8: Unassigned tickets

Flag tickets where `assignee` is null or empty.

**Severity:** Critical
**Output per finding:** Ticket key. No ticket should enter a sprint without an owner.

### Phase 2.5: Classify systemic findings

After running all checks, determine which findings are **systemic**:

- A finding is systemic if it affects **>50%** of the filtered tickets (see Configuration: systemic threshold).
- Example: if 30/35 tickets have no description, "sin descripcion" is systemic.
- Systemic findings are shown in the SCORECARD as `SISTEMICO: [N]/[T] sin descripcion` and are NOT repeated per ticket in the table.
- A ticket that has ONLY systemic findings does NOT appear in the table — it goes to "Sin hallazgos adicionales".
- A ticket appears in the table only if it has at least one **differential** (non-systemic) finding.

### Phase 3: Build report

Organize findings using the format in [references/output-format.md](references/output-format.md).

**Key principle: ticket-centric.** Each ticket appears ONCE in the table with ALL its differential findings aggregated. No ticket key should be repeated across multiple sections.

Order:
1. Header (sprint name, tickets analyzed, total points)
2. Scorecard (three lines: SISTEMICO counts, CRITICO counts, WARNING counts)
3. "Requieren mejor descripción para diferenciar" section (if any)
4. Duplicates section (pairs/groups with explicit motivo)
5. Tickets table (bordered, 5 columns, sorted by severity — only differential findings)
6. Sin hallazgos adicionales (tickets with only systemic findings)
7. Resumen de recomendaciones (numbered, prioritized actions)

### Phase 4: Offer actions

After displaying the terminal report, ask the user which actions to take (multiple choice):

1. **Enviar a Slack** — Send the report as a Slack draft message using the format in [references/output-format-slack.md](references/output-format-slack.md). Ask the user for the channel name, then use `mcp__claude_ai_Slack__slack_search_channels` to find the channel ID, and `mcp__claude_ai_Slack__slack_send_message_draft` to create the draft. If the report exceeds 5000 chars, split into multiple messages.
2. **Comentar en tickets individuales** — Add a comment on each ticket that has Critical findings, noting what needs attention before sprint start. Use `mcp__claude_ai_Atlassian__addCommentToJiraIssue` with cloudId `afianza-ac.atlassian.net`. Keep comments concise and actionable.
3. **Solo el reporte** — No external actions, just the terminal output.

## Edge cases

- If a ticket key is invalid, skip it and note it in the report.
- If JQL returns no results for both future and open sprints, ask the user for ticket keys manually.
- Do NOT invent findings. If a sprint is well-prepared, say so explicitly.
- Duplicate detection is heuristic — always phrase as "potential duplicate" and let the team decide.
- If story points field name differs, try common Jira field names before giving up.
