---
name: rabbitmq-reprocess-dlq
description: Use when needing to reprocess messages from a RabbitMQ Dead Letter Queue (DLQ), move messages between queues using shovel, republish with clean headers, or purge unprocessable messages. Use when user mentions "reprocess", "reprocesar", "shovel", "purge DLQ", or "move messages from DLQ".
---

# Reprocessing RabbitMQ DLQ Messages

## Overview

Move failed messages from a Dead Letter Queue back to the main queue for reprocessing using the RabbitMQ Shovel plugin. For diagnosing **why** messages fail, use the `rabbitmq-triage-dlq` skill first.

## Infrastructure Context

| Environment | Namespace | Pod | Vhost | RabbitMQ service |
|---|---|---|---|---|
| DEV | `shared-infra` | `dev-test-afianza-rabbit-ha-*` (Deployment) | `data_platform` | `svc/dev-test-afianza-rabbit-ha` |
| PROD | `shared-infra` | `rabbitmq-0` (StatefulSet) | `data_platform` | `svc/rabbitmq` |

Queue naming: `<service>:<entity>:persisted` (main) / `<service>:<entity>:persisted.dead_letter` (DLQ)

Consumer pods are in namespace `plataformadato`.

### Credentials & Port-Forward

See the `infra-portforward` skill for service names, ports, and credential retrieval per environment. **Never hardcode credentials.**

## Process

```
1. Identify pod & check queues
2. Verify shovel plugin is enabled
3. Create shovel (rabbitmqctl preferred, Management API as fallback)
4. Monitor until complete
5. If messages bounce back → use triaging-rabbitmq-dlq skill
6. Republish with clean headers or purge
```

### Step 1: Identify pod and check queue status

```bash
# Find RabbitMQ pod
kubectl --context=<env> get pods -n shared-infra | grep rabbit

# Check queues
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmqctl list_queues -p data_platform name messages consumers state \
  | grep "<service>"
```

Note the message count in the DLQ and whether the main queue has active consumers.

### Step 2: Verify shovel plugin

```bash
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmq-plugins list | grep shovel

# Enable if not enabled (look for [ ] vs [E*])
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmq-plugins enable rabbitmq_shovel rabbitmq_shovel_management
```

### Step 3: Create dynamic shovel

**Option A: Via rabbitmqctl (preferred — no port-forward or credentials needed)**

```bash
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmqctl set_parameter -p data_platform shovel \
  "reprocess-<name>-dlq" \
  '{"src-protocol":"amqp091","src-uri":"amqp:///data_platform","src-queue":"<service>:<entity>:persisted.dead_letter","dest-protocol":"amqp091","dest-uri":"amqp:///data_platform","dest-queue":"<service>:<entity>:persisted","src-delete-after":"queue-length"}'
```

**Option B: Via Management API (when you need the API for other operations like fetching messages)**

```bash
# Port-forward in background
kubectl --context=<env> port-forward -n shared-infra svc/<rabbitmq-svc> 15672:15672 &

# Verify connectivity
curl -s -o /dev/null -w "%{http_code}" http://localhost:15672/api/overview -u <user>:<password>

# Create shovel
curl -s -u <user>:<password> \
  -X PUT -H "Content-Type: application/json" \
  'http://localhost:15672/api/parameters/shovel/data_platform/reprocess-<name>-dlq' \
  -d '{
    "value": {
      "src-protocol": "amqp091",
      "src-uri": "amqp:///data_platform",
      "src-queue": "<service>:<entity>:persisted.dead_letter",
      "dest-protocol": "amqp091",
      "dest-uri": "amqp:///data_platform",
      "dest-queue": "<service>:<entity>:persisted",
      "src-delete-after": "queue-length"
    }
  }'
```

The shovel auto-deletes after moving all messages (`src-delete-after: queue-length`).

### Step 4: Monitor progress

```bash
# Monitor queue counts
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmqctl list_queues -p data_platform name messages \
  | grep "<service>"

# Verify shovel auto-deleted (empty = completed)
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmqctl list_parameters -p data_platform | grep shovel
```

Wait until main queue reaches 0. If messages reappear in the DLQ, **use the `rabbitmq-triage-dlq` skill** to diagnose why.

### Step 5: Republish with clean headers (if needed)

When messages fail due to `rascal.immediateNack` (previous death history), republish without `x-death`/`rascal` headers. Requires port-forward + Management API.

```bash
# Fetch messages first
curl -s -u <user>:<password> \
  -X POST -H "Content-Type: application/json" \
  'http://localhost:15672/api/queues/data_platform/<url-encoded-queue>/get' \
  -d '{"count": <N>, "ackmode": "ack_requeue_true", "encoding": "auto"}' \
  > /tmp/dlq_messages.json

# Republish each message as new
curl -s -u <user>:<password> \
  -X POST -H "Content-Type: application/json" \
  'http://localhost:15672/api/exchanges/data_platform/<exchange>/publish' \
  -d '{
    "properties": {"content_type": "application/json", "delivery_mode": 2},
    "routing_key": "<original-routing-key>",
    "payload": "<message-payload>",
    "payload_encoding": "string"
  }'
```

The original routing key is in `rascal.originalRoutingKey` header. Use a Python script to iterate over `/tmp/dlq_messages.json` and republish each message.

**If messages fail again after clean republish**, the issue is message content (not headers). Use triage skill or purge.

### Step 6: Purge unprocessable messages

**Via Management API:**
```bash
curl -s -u <user>:<password> \
  -X DELETE \
  'http://localhost:15672/api/queues/data_platform/<url-encoded-queue>/contents'
```

**Via rabbitmqctl:**
```bash
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmqctl purge_queue -p data_platform "<service>:<entity>:persisted.dead_letter"
```

### Step 7: Cleanup

Close any port-forward processes when done.

## Common Mistakes

| Mistake | Prevention |
|---|---|
| Using Management API when rabbitmqctl suffices | Prefer `rabbitmqctl set_parameter` — no port-forward or credentials needed |
| Forgetting to URL-encode queue names in API calls | Replace `:` with `%3A` in queue names |
| Assuming shovel failed when parameters endpoint is empty | Empty = shovel completed and auto-deleted. Check queue counts |
| Not checking if shovel plugin is enabled | Always verify with `rabbitmq-plugins list` first |
| Reprocessing without diagnosing | If messages bounce back, use `rabbitmq-triage-dlq` first |
