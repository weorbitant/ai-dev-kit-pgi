# ai-pgi-dev-kit

Claude Code skills for PGI development and operations.

## Skills

### Infrastructure
| Skill | Description |
|---|---|
| `infra-portforward` | Port-forward to K8s services (RabbitMQ, PostgreSQL, APIs) |
| `infra-pods` | Pod status, diagnostics, events, resource usage |
| `infra-logs` | Pod log analysis and error searching |
| `infra-deploy` | Production deployments |
| `infra-migrations` | Database migrations in remote environments |

### RabbitMQ
| Skill | Description |
|---|---|
| `rabbitmq-list-queues` | Queue status, DLQ counts, consumer health |
| `rabbitmq-triage-dlq` | Diagnose why messages fail in DLQs |
| `rabbitmq-reprocess-dlq` | Reprocess DLQ messages via shovel |

### Database
| Skill | Description |
|---|---|
| `db-query` | Read-only SQL queries from within pods |

### Jira
| Skill | Description |
|---|---|
| `jira-create-bug` | Structured bug reports with root cause analysis |
| `jira-clarify-ticket` | Detect ambiguities in ticket specs |

### Analysis
| Skill | Description |
|---|---|
| `ticket-analysis` | Comprehensive ticket analysis (Jira + Figma + docs + code) |
| `analyze-design` | Extract data fields and states from Figma designs |
| `analyze-docs` | Search Confluence/Notion for documentation |
| `analyze-data-model` | Trace entity fields through the codebase |

### Meta
| Skill | Description |
|---|---|
| `creating-skills` | Guide for authoring new skills |

## Installation

Copy skills to your Claude Code personal skills directory:

```bash
cp -R skills/* ~/.claude/skills/
```

Or symlink for auto-updates:

```bash
for dir in skills/*/; do
  name=$(basename "$dir")
  ln -sfn "$(pwd)/$dir" ~/.claude/skills/"$name"
done
```
