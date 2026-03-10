---
name: db-query
description: Use when needing to query a PostgreSQL database in DEV or PROD, check if records exist, count rows, inspect data, or run read-only SQL queries from within the cluster. Use when user says "consulta la BD", "query", "busca en la tabla", "check database", "db query", or "existe este registro".
argument-hint: "[query description] [environment]"
allowed-tools: Bash, Read, AskUserQuestion
model: sonnet
---

# Database Queries

## Overview

Execute read-only SQL queries against PostgreSQL databases via PgBouncer from within application pods. No `psql` available — use the `pg` module via `node -e`.

## Configuration

Read project-specific values from the project's CLAUDE.md (`## Infrastructure` section):
- kubectl context, namespace, app pod label, database name, config file per environment

## Constraints

- **PgBouncer does NOT support parameterized queries** — use inline SQL with quoted values.
- **Read-only only.** Never run INSERT/UPDATE/DELETE without explicit user confirmation.
- Use `require('/app/node_modules/pg')` — module is not in the global node path.
- Use `development.config.js` for DEV, `production.config.js` for PROD (both files exist in every pod).

## Process

1. Read the project CLAUDE.md for connection details (context, namespace, db name, pod label)
2. Find a running pod: `kubectl --context=<ctx> get pods -n <namespace> | grep <app-label>`
3. Get connection details from the config file inside the pod
4. Run the query using the helper script or inline `node -e`

See [scripts/query.js](scripts/query.js) for the reusable helper (copy to pod with `kubectl cp`).
See [references/query-examples.md](references/query-examples.md) for command templates.

## Common Mistakes

| Mistake | Prevention |
|---|---|
| Not reading CLAUDE.md | Namespace, context, DB name vary per project. |
| Parameterized queries (`$1::uuid[]`) | PgBouncer rejects them. Use inline SQL. |
| `require('pg')` fails | Use `require('/app/node_modules/pg')`. |
| Wrong config file | `production.config.js` in a DEV pod points to PROD db. Use `development.config.js` for DEV. |
| Write queries without confirmation | Always ask before INSERT/UPDATE/DELETE. |
