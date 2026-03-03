---
name: infra-pods
description: Use when checking pod status, listing running services, investigating crashloops, viewing pod events, or checking resource usage. Use when user says "pods", "qué está corriendo", "pod status", "check pods", "restart", "crashloop", or "pod events".
argument-hint: "[service-name] [environment]"
allowed-tools: Bash, AskUserQuestion
model: haiku
---

# Kubernetes Pod Management

## Overview

Inspect pod status, health, events, and resource usage across cluster environments.

## Pod Status

### List pods for a service

```bash
kubectl --context=<env> get pods -n <namespace> | grep <service>
```

### List all pods in a namespace with status

```bash
kubectl --context=<env> get pods -n <namespace> -o wide
```

### Check for unhealthy pods

```bash
kubectl --context=<env> get pods -n <namespace> | grep -v "Running\|Completed"
```

## Diagnostics

### Pod details and events

```bash
kubectl --context=<env> describe pod <pod> -n <namespace> | tail -30
```

Events show recent scheduling, pulling, starting, and crash info.

### Check restart counts

```bash
kubectl --context=<env> get pods -n <namespace> -o custom-columns=\
NAME:.metadata.name,STATUS:.status.phase,RESTARTS:.status.containerStatuses[0].restartCount,\
AGE:.metadata.creationTimestamp | grep <service>
```

### Pod resource usage

```bash
kubectl --context=<env> top pods -n <namespace> | grep <service>
```

### Environment variables (non-secret)

```bash
kubectl --context=<env> exec -n <namespace> <pod> -- env | grep -iv "pass\|secret\|token\|key" | sort
```

### Check which image/version is running

```bash
kubectl --context=<env> get pod <pod> -n <namespace> \
  -o jsonpath='{.spec.containers[0].image}'
```

## Common Namespaces

| Namespace | Services |
|---|---|
| `plataformadato` | backoffice-api, obligations-api, data-factory, http2bus, pgbouncer, adapters |
| `shared-infra` | RabbitMQ, monitoring |
| `gestordocumental` | gestor documental API |

## Rollout Management

### Check deployment status

```bash
kubectl --context=<env> get deploy -n <namespace> | grep <service>
```

### Restart a deployment (rolling)

```bash
kubectl --context=<env> rollout restart deployment/<deployment> -n <namespace>
```

**Caution:** Always confirm with user before restarting pods in PROD.

### Check rollout history

```bash
kubectl --context=<env> rollout history deployment/<deployment> -n <namespace>
```
