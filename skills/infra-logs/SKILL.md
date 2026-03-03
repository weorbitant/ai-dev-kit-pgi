---
name: infra-logs
description: Use when checking pod logs, searching for errors, viewing recent log output, or debugging runtime issues in DEV or PROD. Use when user says "logs de", "ver logs", "qué errores hay", "check logs", "show errors", or mentions log analysis of a service.
argument-hint: "[service-name] [environment]"
allowed-tools: Bash, AskUserQuestion
model: sonnet
---

# Kubernetes Pod Logs

## Overview

Search and analyze logs from pods in the cluster. Supports filtering by time, error patterns, and entities.

## Pod Discovery

```bash
# Find pods for a service
kubectl --context=<env> get pods -n plataformadato | grep <service>

# For infra services
kubectl --context=<env> get pods -n shared-infra | grep <service>
```

Common namespaces:
- `plataformadato` — application services (backoffice-api, obligations-api, data-factory, etc.)
- `shared-infra` — RabbitMQ, monitoring
- `gestordocumental` — gestor documental services

## Log Commands

### Recent errors

```bash
kubectl --context=<env> logs <pod> -n <namespace> --since=<duration> 2>&1 \
  | grep -i "error\|exception\|fail" | tail -50
```

Duration examples: `5m`, `30m`, `1h`, `3h`, `24h`

### Errors for a specific entity/operation

```bash
kubectl --context=<env> logs <pod> -n <namespace> --since=<duration> 2>&1 \
  | grep -i "<entity>\|<operation>" | grep -i "error" | tail -30
```

### Full context around errors (5 lines before/after)

```bash
kubectl --context=<env> logs <pod> -n <namespace> --since=<duration> 2>&1 \
  | grep -B5 -A5 -i "error\|exception" | tail -80
```

### Follow logs in real-time (for live debugging)

```bash
kubectl --context=<env> logs -f <pod> -n <namespace> | grep -i "<pattern>"
```

### Logs from all pods of a deployment

```bash
kubectl --context=<env> logs -l app=<service> -n <namespace> --since=<duration> 2>&1 \
  | grep -i "error" | tail -50
```

### Previous container logs (after a crash/restart)

```bash
kubectl --context=<env> logs <pod> -n <namespace> --previous | tail -100
```

## Output Format

Summarize findings:
- Total error count in the period
- Unique error types/messages
- Frequency patterns (burst vs steady)
- Affected entities (IDs, clients, etc.)

If no errors found, say so explicitly — don't assume the absence of evidence is evidence of absence. Suggest checking a wider time range or different pod.
