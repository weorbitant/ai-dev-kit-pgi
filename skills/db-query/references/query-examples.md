# Query Command Examples

All placeholders come from the project's CLAUDE.md `## Infrastructure` section.

## Find a pod

```bash
kubectl --context=<ctx> get pods -n <namespace> | grep <app-label>
```

## Read connection details from pod

```bash
# DEV — use development.config.js
kubectl --context=<ctx-dev> exec -n <namespace> <pod> -- \
  cat /app/dist/src/config/development.config.js

# PROD — use production.config.js
kubectl --context=<ctx-prod> exec -n <namespace> <pod> -- \
  cat /app/dist/src/config/production.config.js
```

Look for the `postgresql` block: `host`, `port` (usually 6432), `database`, `user`, `password`.

## Using the helper script (recommended)

```bash
# Copy script to pod
kubectl --context=<ctx> cp ~/.claude/skills/db-query/scripts/query.js \
  <namespace>/<pod>:/tmp/query.js

# List tables
kubectl --context=<ctx> exec -n <namespace> <pod> -- \
  node /tmp/query.js --host <pgbouncer-host> --db <db-name> --tables

# Describe a table
kubectl --context=<ctx> exec -n <namespace> <pod> -- \
  node /tmp/query.js --host <pgbouncer-host> --db <db-name> --describe <table>

# Check if records exist by ID
kubectl --context=<ctx> exec -n <namespace> <pod> -- \
  node /tmp/query.js --host <pgbouncer-host> --db <db-name> --exists <table> --ids "uuid1,uuid2"

# Arbitrary SQL
kubectl --context=<ctx> exec -n <namespace> <pod> -- \
  node /tmp/query.js --host <pgbouncer-host> --db <db-name> --sql "SELECT count(*) FROM mytable"
```

## Quick one-off query (inline)

```bash
kubectl --context=<ctx> exec -n <namespace> <pod> -- sh -c '
node -e "
const { Client } = require(\"/app/node_modules/pg\");
const c = new Client({
  host: \"<pgbouncer-host>\", port: 6432,
  database: \"<db-name>\", user: \"postgres\",
  password: process.env.POSTGRES_PASSWORD
});
c.connect()
  .then(() => c.query(\"SELECT * FROM mytable LIMIT 10\"))
  .then(r => { console.log(JSON.stringify(r.rows, null, 2)); c.end(); })
  .catch(e => { console.error(e.message); c.end(); });
"
'
```
