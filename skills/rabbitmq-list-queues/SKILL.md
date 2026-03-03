---
name: rabbitmq-list-queues
description: Use when checking RabbitMQ queue status, listing queues with messages, checking DLQ counts, or monitoring consumer health. Use when user says "list queues", "lista colas", "queue status", "cuántos mensajes", "check queues", or "DLQ status".
argument-hint: "[service-name] [environment]"
---

# RabbitMQ Queue Status

## Overview

Quick inspection of RabbitMQ queue status across environments. Lists message counts, consumer counts, and identifies DLQs with pending messages.

## Commands

### List all DLQs with messages

```bash
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmqctl list_queues -p data_platform name messages consumers state \
  | grep "dead_letter" | awk '$2 > 0'
```

### Check specific service queues

```bash
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmqctl list_queues -p data_platform name messages consumers state \
  | grep "<service>"
```

### List all queues with messages (non-empty)

```bash
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmqctl list_queues -p data_platform name messages consumers state \
  | awk 'NR==1 || $2 > 0'
```

### Check consumer health (queues with 0 consumers)

```bash
kubectl --context=<env> exec -n shared-infra <rabbitmq-pod> -- \
  rabbitmqctl list_queues -p data_platform name messages consumers state \
  | grep -v "dead_letter" | awk '$3 == 0 && $2 > 0'
```

## Pod Discovery

| Environment | Pod pattern |
|---|---|
| DEV | `kubectl --context=dev get pods -n shared-infra \| grep rabbit` |
| PROD | `rabbitmq-0` (StatefulSet) |

## Output Format

Present results as a table:

```
| Queue | Messages | Consumers | State |
|---|---|---|---|
| service:entity:persisted | 0 | 2 | running |
| service:entity:persisted.dead_letter | 47 | 0 | running |
```

Flag any issues:
- DLQ with messages > 0 → suggest `rabbitmq-triage-dlq`
- Main queue with 0 consumers → service may be down
- Main queue with growing messages → consumers may be slow
