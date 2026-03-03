---
name: db-query
description: Use when needing to query a PostgreSQL database in DEV or PROD, check if records exist, count rows, inspect data, or run read-only SQL queries from within the cluster. Use when user says "consulta la BD", "query", "busca en la tabla", "check database", "db query", or "existe este registro".
argument-hint: "[query description] [environment]"
allowed-tools: Bash, Read, AskUserQuestion
model: sonnet
---

# Database Queries

## Overview

Execute read-only SQL queries against PostgreSQL databases via PgBouncer from within application pods. No `psql` is available in pods — use `node -e` with the `pg` module instead.

## Constraints

- **PgBouncer does NOT support parameterized queries** (`$1::uuid[]` will fail with syntax error). Always use inline SQL with quoted values.
- **Read-only queries only.** Never run INSERT/UPDATE/DELETE without explicit user confirmation.
- Pods don't have `psql`. Use `node -e` with the `pg` module that's already installed in NestJS app pods.

## Process

### 1. Find the database connection details

```bash
kubectl --context=<env> exec -n plataformadato <pod> -- \
  cat /app/dist/src/config/production.config.js
```

Look for the `postgresql` block:
- `host` — PgBouncer service (e.g., `pd-infra-pgbouncer.plataformadato.svc.cluster.local`)
- `port` — Usually `6432`
- `database` — Service-specific (e.g., `pd-service-backoffice-api-prod`)
- `user` — Usually `postgres`
- `password` — `process.env.POSTGRES_PASSWORD`

### 2. Run the query

Copy the helper script to the pod and use it for all query types:

```bash
# Copy script to pod
kubectl --context=<env> cp ~/.claude/skills/db-query/scripts/query.js \
  plataformadato/<pod>:/tmp/query.js

# List tables
kubectl --context=<env> exec -n plataformadato <pod> -- \
  node /tmp/query.js --host <pgbouncer-host> --db <database> --tables

# Describe a table
kubectl --context=<env> exec -n plataformadato <pod> -- \
  node /tmp/query.js --host <pgbouncer-host> --db <database> --describe <table>

# Check if records exist
kubectl --context=<env> exec -n plataformadato <pod> -- \
  node /tmp/query.js --host <pgbouncer-host> --db <database> --exists <table> --ids "uuid1,uuid2"

# Run arbitrary SQL
kubectl --context=<env> exec -n plataformadato <pod> -- \
  node /tmp/query.js --host <pgbouncer-host> --db <database> --sql "SELECT count(*) FROM client"
```

See [scripts/query.js](scripts/query.js) for the full script. It reads `POSTGRES_PASSWORD` from the pod's environment automatically.

**For quick one-off queries** (without copying the script):

```bash
kubectl --context=<env> exec -n plataformadato <pod> -- sh -c '
node -e "
const { Client } = require(\"pg\");
const c = new Client({
  host: \"<host>\", port: 6432,
  database: \"<database>\", user: \"postgres\",
  password: process.env.POSTGRES_PASSWORD
});
c.connect()
  .then(() => c.query(\"<YOUR SQL HERE>\"))
  .then(r => { console.log(JSON.stringify(r.rows, null, 2)); c.end(); })
  .catch(e => { console.error(e.message); c.end(); });
"
'
```

## Known Databases

| Service | Database name pattern |
|---|---|
| backoffice-api | `pd-service-backoffice-api-<env>` |
| obligations-api | `mp-service-obligations-api-<env>` |

## Common Mistakes

| Mistake | Prevention |
|---|---|
| Using `$1::uuid[]` parameterized queries | PgBouncer rejects these. Use inline SQL with `\x27` quoted values |
| Running write queries without confirmation | Always ask user before INSERT/UPDATE/DELETE |
| Wrong pod (pod doesn't have `pg` module) | Use NestJS app pods, not infra pods |
| Forgetting `process.env.POSTGRES_PASSWORD` | The password is in the pod's env, don't hardcode it |
