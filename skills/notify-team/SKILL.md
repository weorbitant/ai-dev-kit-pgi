---
name: notify-team
description: Use when sending any communication to the team — incidents, announcements, questions, status updates, or review requests. Use when user says "notifica al equipo", "avisa al equipo", "crea un mensaje", "anuncia", "pregunta al equipo", "draft a message", or wants to communicate anything to the team via Slack.
argument-hint: "[slack] [#channel|@person] [descripción]"
---

# Notify Team

## Overview

Drafts and delivers team messages via Slack. Supports any message type: incidents, announcements, questions, updates, review requests. Always creates a draft first unless the user explicitly says to send.

## Step 1 — Resolve configuration

Infer from context; only ask if genuinely ambiguous.

| Parameter | Options | Default |
|---|---|---|
| **Destination** | Channel or person | Suggest from registry; confirm if unsure |
| **Message type** | incident, announcement, question, update, review | Infer from context |
| **Action** | `draft`, `send` | `draft` |

## Step 2 — Select destination

| Channel | ID | When to use |
|---|---|---|
| `#afianza_pgi_team` | `C0A2HRXEF63` | General comms, questions, data problems |
| `#afianza-alerts-broker-dlq` | `C09PU66T8S1` | DLQ / message broker issues |
| `#afianza-alerts-critical` | `C09PVJJ471C` | Critical PROD incidents |
| `#afianza-alerts-infra` | `C09PG6FQCNB` | Infrastructure issues |

## Step 2.5 — Gather context (when needed)

For **releases/announcements** involving PRs: fetch PR info automatically with `gh` — don't ask the user.

```bash
gh pr view <N> --json title,url
```

Use the PR URLs to build Slack links in the format `<URL|PR#N>` (e.g. `<https://github.com/org/repo/pull/10|PR#10>`).

## Step 3 — Draft the message

Infer the language from the conversation, then load the matching templates file:
- Spanish → [references/templates-es.md](references/templates-es.md)
- English → [references/templates-en.md](references/templates-en.md)

Select the template matching the message type. Adapt freely — don't use templates as rigid structure.

## Step 4 — Deliver

| Action | Tool |
|---|---|
| `draft` | `slack_send_message_draft` |
| `send` | `slack_send_message` |
| Thread reply | `slack_send_message` with `thread_ts` |

## Guidelines

- Never include credentials or passwords
- Be specific: include IDs, queue names, error codes, links — whatever the team needs to act
- End with a clear question or call to action when a response is needed
