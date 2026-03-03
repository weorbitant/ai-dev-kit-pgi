---
name: infra-portforward
description: Use when needing to port-forward to any Kubernetes service (RabbitMQ, PostgreSQL, internal APIs). Use when user says "port-forward", "portforward", "connect to", "forward port", or needs local access to a cluster service in DEV or PROD.
argument-hint: "[service] [environment]"
---

# Kubernetes Port-Forward

## Overview

Establish port-forward connections to cluster services. Handles service discovery, credentials retrieval, connectivity verification, and cleanup. Supports RabbitMQ, PostgreSQL, and internal APIs.

## Service Registry

Quick reference for the most common services. For the full inventory (all adapters, gestor documental, etc.), see [references/services.md](references/services.md).

| Service | Namespace | DEV svc | PROD svc | Port |
|---|---|---|---|---|
| RabbitMQ (mgmt) | `shared-infra` | `dev-test-afianza-rabbit-ha` | `rabbitmq` | 15672 |
| RabbitMQ (AMQP) | `shared-infra` | `dev-test-afianza-rabbit-ha` | `rabbitmq` | 5672 |
| PostgreSQL | `plataformadato` | `dev-infra-pgbouncer` | `pd-infra-pgbouncer` | 6432 |
| backoffice-api | `plataformadato` | — | `pd-service-backoffice-api` | 8000 |
| obligations-api | `plataformadato` | — | `mp-service-obligations-api` | 8000 |

## Process

### 1. Find the service

```bash
# If you don't know the exact service name
kubectl --context=<env> get svc -n <namespace> | grep <keyword>

# For pods (when you need to forward to a specific pod)
kubectl --context=<env> get pods -n <namespace> | grep <keyword>
```

### 2. Start port-forward

```bash
# To a service (preferred — survives pod restarts)
kubectl --context=<env> port-forward -n <namespace> svc/<service> <local>:<remote>

# To a specific pod
kubectl --context=<env> port-forward -n <namespace> <pod-name> <local>:<remote>
```

Run in background so the terminal stays available. When running multiple port-forwards, use different local ports to avoid conflicts.

### 3. Verify connectivity

Use the service-specific verification command from the registry above.

### 4. Cleanup

```bash
# Kill port-forward on a specific port
kill $(lsof -ti:<local-port>) 2>/dev/null

# Kill all port-forwards
pkill -f "kubectl.*port-forward" 2>/dev/null
```

## Credentials

**Never hardcode credentials in skills or commands.**

Retrieval order:
1. Ask the user if they know the credentials
2. Try Kubernetes secrets:

```bash
# RabbitMQ - check definitions for username
kubectl --context=<env> get secret rabbitmq-definitions-secret -n shared-infra \
  -o jsonpath='{.data.load_definition\.json}' | base64 -d | \
  python3 -c "import sys,json; [print(u['name']) for u in json.load(sys.stdin).get('users',[])]"

# RabbitMQ - PROD password
kubectl --context=prod get secret rabbitmq -n shared-infra \
  -o jsonpath='{.data.rabbitmq-password}' | base64 -d

# RabbitMQ - DEV password
kubectl --context=dev get secret dev-test-afianza-rabbit-ha-secret \
  -n shared-infra -o jsonpath='{.data.rabbitmq-password}' | base64 -d

# PostgreSQL - read from app pod config
kubectl --context=<env> exec -n plataformadato <app-pod> -- \
  cat /app/dist/src/config/production.config.js | grep -A5 postgresql
```

3. If secrets don't match, ask the user

## Port Conflict Resolution

```bash
# Check what's using a port
lsof -i:<port>

# Use an alternative local port
kubectl --context=<env> port-forward -n <namespace> svc/<service> <alt-local>:<remote>
```

## Common Mistakes

| Mistake | Prevention |
|---|---|
| Port-forward dies silently | Run in background and verify connectivity after starting |
| Port already in use | Check with `lsof -i:<port>` first, kill or use alternative port |
| Forwarding to wrong namespace | RabbitMQ is in `shared-infra`, most apps in `plataformadato` |
| Forgetting to close port-forward | Always cleanup when done with `kill $(lsof -ti:<port>)` |
| Using port-forward when `kubectl exec` suffices | For DB queries or API calls from within the cluster, exec into the pod directly |
