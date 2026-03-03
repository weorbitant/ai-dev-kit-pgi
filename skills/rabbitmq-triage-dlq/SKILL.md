---
name: rabbitmq-triage-dlq
description: Use when investigating why messages are failing in a RabbitMQ Dead Letter Queue (DLQ), diagnosing root causes of message rejections, or analyzing DLQ message patterns. Use when user says "triage DLQ", "why are messages failing", "analyze DLQ", "diagnose DLQ", "analiza esta cola", or wants to understand message failures before deciding whether to reprocess or purge.
---

# Triaging RabbitMQ DLQ Messages

## Overview

Systematic diagnosis of why messages end up in a Dead Letter Queue. Analyzes message payloads, headers, subscriber DTOs, handler logic, and database state to identify root causes and recommend actions. After triage, use `rabbitmq-reprocess-dlq` to act on findings.

## Infrastructure Context

See `infra-portforward` skill for service names, ports, and credential retrieval. See `rabbitmq-reprocess-dlq` for queue naming conventions.

Key facts for triage:
- Consumer pods are in namespace `plataformadato`
- App code is in `/app/dist/src/` inside pods
- Subscriber pattern: `/app/dist/src/application/amqp/<entity>-subscriber/`
- Config pattern: `/app/dist/src/config/production.config.js`
- DB access via PgBouncer (no `psql` in pods, use `node -e` with `pg` module)
- PgBouncer does NOT support parameterized queries (`$1::uuid[]`). Use inline SQL.

## Triage Process

```
1. Survey queues           → How many messages? Active consumers?
2. Fetch messages           → Via Management API (needs port-forward)
3. Analyze message patterns → Schema, headers, failure classification
4. Inspect subscriber code  → DTO validation + handler logic from pod
5. Verify external state    → DB lookups for referenced entities
6. Check consumer logs      → Trigger 1-message reprocess if needed
7. Present findings         → Root cause + recommendation
```

### Step 1: Survey queues

```bash
kubectl --context=<env> get pods -n shared-infra | grep rabbit

# List ALL DLQs with messages
kubectl --context=<env> exec -n shared-infra <pod> -- \
  rabbitmqctl list_queues -p data_platform name messages consumers state \
  | grep "dead_letter" | awk '$2 > 0'

# Check specific service (main + DLQ)
kubectl --context=<env> exec -n shared-infra <pod> -- \
  rabbitmqctl list_queues -p data_platform name messages consumers state \
  | grep "<service>"
```

If main queue has 0 consumers, the service may be down — check pods in `plataformadato` first.

### Step 2: Fetch messages

Requires port-forward + credentials (see `infra-portforward` skill for setup). **Never hardcode credentials.**

```bash
# Fetch messages (non-destructive peek)
curl -s -u <user>:<password> \
  -X POST -H "Content-Type: application/json" \
  'http://localhost:15672/api/queues/data_platform/<url-encoded-queue>/get' \
  -d '{"count": <N>, "ackmode": "ack_requeue_true", "encoding": "auto"}' \
  > /tmp/dlq_messages.json
```

**URL-encode queue names**: replace `:` with `%3A`.

### Step 3: Analyze message patterns

Run the analysis script from this skill's `scripts/` directory:

```bash
python3 ~/.claude/skills/rabbitmq-triage-dlq/scripts/analyze_messages.py /tmp/dlq_messages.json
python3 ~/.claude/skills/rabbitmq-triage-dlq/scripts/analyze_messages.py /tmp/dlq_messages.json --fields clientId,family,category --detail 10
```

The script covers: header analysis (immediateNack, x-death counts), schema variations, field distributions, and message detail. See [scripts/analyze_messages.py](scripts/analyze_messages.py) for full source.

**Classification:**

| Indicator | Meaning | Next step |
|---|---|---|
| `immediateNack: true` | Rascal rejected (death history or DTO fail) | Check DTO or republish clean |
| `immediateNack: false` + error logs | Handler exception | Check handler logic + logs |
| `immediateNack: false` + no logs | DTO validation in rascal pipeline | Check DTO fields |
| `x-death count > 1` | Retried multiple times | Persistent issue |
| Schema variations | Producer changed payload over time | Compare schemas against DTO |

### Step 4: Inspect subscriber code

Read the DTO and handler directly from the running pod:

```bash
# Find consumer pods
kubectl --context=<env> get pods -n plataformadato | grep <service>

# Find subscriber files
kubectl --context=<env> exec -n plataformadato <pod> -- \
  find /app/dist -type f -name "*.js" | grep -i "<entity>.*subscriber"

# Read the DTO (most critical file)
kubectl --context=<env> exec -n plataformadato <pod> -- \
  cat /app/dist/src/application/amqp/<entity>-subscriber/dto/<entity>-dto.js

# Read the handler
kubectl --context=<env> exec -n plataformadato <pod> -- \
  cat /app/dist/src/application/amqp/<entity>-subscriber/<entity>.subscriber.js
```

**DTO analysis checklist:**
- Compare every `@IsNotEmpty()` field against actual message payloads
- Check nested DTOs (`jiraRefs`, `erpRef`, `sourceSystems`) — they have their own validations
- `@ValidateNested()` on arrays means each element must pass validation
- Field in DTO as `@IsNotEmpty()` but missing in messages? **That's the bug.**

### Step 5: Verify external state

If the handler does DB lookups (`getClientById`, etc.), check whether referenced entities exist.

```bash
# Read DB config
kubectl --context=<env> exec -n plataformadato <pod> -- \
  cat /app/dist/src/config/production.config.js

# Query via node.js (no psql available in pods)
kubectl --context=<env> exec -n plataformadato <pod> -- sh -c '
node -e "
const { Client } = require(\"pg\");
const c = new Client({
  host: \"<pgbouncer-host>\", port: 6432,
  database: \"<database>\", user: \"postgres\",
  password: process.env.POSTGRES_PASSWORD
});
const ids = [\"uuid1\", \"uuid2\"];
const inClause = ids.map(id => \"\\x27\" + id + \"\\x27\").join(\",\");
c.connect()
  .then(() => c.query(\"SELECT id FROM <table> WHERE id IN (\" + inClause + \")\"))
  .then(r => {
    const found = new Set(r.rows.map(x => x.id));
    const missing = ids.filter(id => !found.has(id));
    console.log(\"Found: \" + found.size + \"/\" + ids.length);
    if (missing.length > 0) console.log(\"Missing: \" + JSON.stringify(missing));
    c.end();
  }).catch(e => { console.error(e.message); c.end(); });
"
'
```

### Step 6: Check consumer logs

```bash
kubectl --context=<env> logs <pod> -n plataformadato --since=30m 2>&1 \
  | grep -i "error\|exception\|reject\|nack\|<entity>" | tail -40
```

**If no errors appear**: the failure is DTO validation (happens before the handler, produces no log output).

**If you need live errors**: trigger a 1-message reprocess and watch logs simultaneously:

```bash
# Terminal 1: watch logs
kubectl --context=<env> logs -f <pod> -n plataformadato | grep -i "error\|<entity>"

# Terminal 2: reprocess 1 message via shovel
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmqctl set_parameter -p data_platform shovel "test-1msg" \
  '{"src-protocol":"amqp091","src-uri":"amqp:///data_platform","src-queue":"<dlq-queue>","src-prefetch-count":1,"dest-protocol":"amqp091","dest-uri":"amqp:///data_platform","dest-queue":"<main-queue>","src-delete-after":"1"}'
```

This moves exactly 1 message so you can observe the error in real-time.

## Root Cause Decision Tree

```
Messages in DLQ
├── immediateNack = true
│   └── Rascal rejected due to x-death history
│       → Republish with clean headers (reprocessing skill)
│
├── DTO validation error (no handler logs)
│   ├── Missing required fields
│   │   └── Fix: @IsNotEmpty() → @IsOptional() in DTO
│   ├── Type mismatch
│   │   └── Fix: adjust types or add @Transform()
│   └── Nested DTO validation
│       └── Fix: check nested DTO classes
│
├── Handler error (visible in logs)
│   ├── "entity not found"
│   │   ├── Entity now exists → Reprocess with shovel
│   │   └── Entity won't exist → Purge
│   ├── DB constraint violation
│   │   └── Fix: check unique constraints, missing columns
│   └── Unexpected null/undefined
│       └── Fix: add null checks
│
└── Unknown
    └── Reprocess 1 message + watch logs in real-time (Step 6)
```

## Known Failure Patterns

| Pattern | Service | Root cause | Fix |
|---|---|---|---|
| `jiraRefs` validation | backoffice-api, obligations-api | `summary`/`status` as `@IsNotEmpty()`, producer sends `id`/`href`/`issueType` only | `@IsOptional()` |
| `client not found` | backoffice-api | Client not yet synced when event arrives | Reprocess after sync |
| Schema drift | Any | Producer added/removed fields | Make new fields `@IsOptional()` |

## Output Template

Present findings in this format:

```
## DLQ Triage: <service>:<entity>

**Queue**: <full-queue-name>
**Environment**: DEV/PROD
**Messages**: N
**Failure mode**: DTO validation / Handler error / immediateNack

### Root cause
<description>

### Evidence
- <log lines, field comparisons, schema diffs>

### Recommendation
- [ ] Fix required: <code change description>
- [ ] Reprocessable: yes/no (after fix)
- [ ] Jira ticket: <if needed>
```
