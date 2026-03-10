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

## Docs

| Document | Description |
|---|---|
| [Ticket Analysis Workflow](docs/workflow-ticket-analysis.md) | Step-by-step workflow for analyzing tickets before implementation (Jira + Figma + Confluence/Notion + codebase) |

## Installation

Clone the repo and symlink the skills into your Claude Code personal directory:

```bash
git clone <repo-url> && cd ai-pgi-dev-kit

for dir in skills/*/; do
  name=$(basename "$dir")
  ln -sfn "$(pwd)/$dir" ~/.claude/skills/"$name"
done
```

The symlinks make `~/.claude/skills/` point directly to the repo files. This means:

| Action | What happens |
|---|---|
| **Use** a skill | Claude Code reads `~/.claude/skills/X` which resolves to the repo via symlink |
| **Edit** a skill | You edit the file in the repo (or via the symlink — same thing) |
| **Share** changes | `git commit && git push` from the repo |
| **Receive** updates | `git pull` — symlinks keep pointing to the same files |

No manual copying needed in either direction.

## Contributing

### Adding a new skill

1. Create a folder under `skills/` with a kebab-case name.
2. Add a `SKILL.md` file with the required frontmatter (`name`, `description`) and instructions. See the `creating-skills` skill for authoring guidelines.
3. Optionally add `references/`, `scripts/`, or `assets/` subfolders for supporting files.
4. Update the skills table in this README.
5. Submit a PR with a clear description of the skill's purpose and trigger conditions.

### Improving an existing skill

1. Test the current behavior by invoking the skill in Claude Code.
2. Make your changes to `SKILL.md` or supporting files.
3. Verify the skill still triggers correctly and produces the expected output.
4. Submit a PR explaining what changed and why.

### General guidelines

- Keep skills focused on a single workflow — avoid catch-all skills.
- Follow the **progressive disclosure** principle: load only what's needed, when it's needed.
- Use `references/` for detailed docs that the skill loads on-demand, rather than embedding everything in `SKILL.md`.
- Write trigger descriptions that are specific enough to avoid false activations.
- Include both English and Spanish trigger phrases in the `description` field where applicable.
