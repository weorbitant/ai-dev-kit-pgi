# Migration Commands Reference

All placeholders come from the project's CLAUDE.md `## Infrastructure` section.

## Step 1 — Identify pending migrations

```bash
git fetch origin main
git checkout main && git pull origin main

# List migration files
ls src/migrations/Migration*.ts

# Find which PR introduced a migration file
git log --oneline -- src/migrations/Migration<timestamp>.ts
gh pr view <PR-number> --json title,state,mergedAt
```

## Step 3 — Get DB password from pod

```bash
kubectl --context=<ctx> get pods -n <namespace> | grep <app-label>
kubectl --context=<ctx> exec -n <namespace> <pod-name> -- env | grep POSTGRES_PASSWORD
```

## Step 4 — Port-forward to PgBouncer

Use different local ports per environment to avoid conflicts:

```bash
# DEV
kubectl --context=<ctx-dev> port-forward -n <namespace> svc/<pgbouncer-svc> 16432:6432 &

# PROD
kubectl --context=<ctx-prod> port-forward -n <namespace> svc/<pgbouncer-svc> 16433:6432 &
```

## Step 5 — Run migrations

```bash
# DEV (port 16432)
POSTGRES_DB=<db-dev> POSTGRES_USER=postgres POSTGRES_PASSWORD='<password>' \
POSTGRES_HOST=localhost POSTGRES_PORT=16432 \
<migrations-cmd>

# PROD (port 16433)
POSTGRES_DB=<db-prod> POSTGRES_USER=postgres POSTGRES_PASSWORD='<password>' \
POSTGRES_HOST=localhost POSTGRES_PORT=16433 \
<migrations-cmd>
```

## Step 6 — Verify no pending migrations

```bash
# DEV
POSTGRES_DB=<db-dev> POSTGRES_USER=postgres POSTGRES_PASSWORD='<password>' \
POSTGRES_HOST=localhost POSTGRES_PORT=16432 \
npx mikro-orm migration:pending

# PROD
POSTGRES_DB=<db-prod> POSTGRES_USER=postgres POSTGRES_PASSWORD='<password>' \
POSTGRES_HOST=localhost POSTGRES_PORT=16433 \
npx mikro-orm migration:pending
```

## Step 7 — Close port-forward

```bash
# Kill the background port-forward by PID or:
kill $(lsof -ti:16432)
kill $(lsof -ti:16433)
```
