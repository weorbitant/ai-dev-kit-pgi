# Service Registry

Inventory of services available for port-forwarding, organized by namespace.

## shared-infra

### RabbitMQ (Management API)

| Environment | Service | Local port | Remote port |
|---|---|---|---|
| DEV | `svc/dev-test-afianza-rabbit-ha` | 15672 | 15672 |
| PROD | `svc/rabbitmq` | 15672 | 15672 |

- **Verify**: `curl -s -o /dev/null -w "%{http_code}" http://localhost:15672/api/overview -u <user>:<password>` → 200
- **Credentials**: Ask user or retrieve from secrets (see main SKILL.md)

### RabbitMQ (AMQP - rarely needed for port-forward)

| Environment | Service | Local port | Remote port |
|---|---|---|---|
| DEV | `svc/dev-test-afianza-rabbit-ha` | 5672 | 5672 |
| PROD | `svc/rabbitmq` | 5672 | 5672 |

## plataformadato

### PostgreSQL (PgBouncer)

| Environment | Service | Local port | Remote port |
|---|---|---|---|
| DEV | `svc/dev-infra-pgbouncer` | 6432 | 6432 |
| PROD | `svc/pd-infra-pgbouncer` | 6432 | 6432 |

- **Verify**: `pg_isready -h localhost -p 6432` or connect with `psql`
- **Credentials**: `postgres` user, password from `POSTGRES_PASSWORD` env var in app pods
- **Note**: PgBouncer does NOT support parameterized queries. Use inline SQL.

### Application APIs

All on port 8000.

| Service | Description |
|---|---|
| `svc/pd-service-backoffice-api` | Backoffice API (clients, provided services, assignments) |
| `svc/mp-service-obligations-api` | Obligations API (client obligations, tasks) |
| `svc/pd-service-data-factory` | Data factory (ETL, data sync) |
| `svc/af-service-http2bus` | HTTP to RabbitMQ bridge |
| `svc/pd-service-jira-adapter` | Jira integration adapter |
| `svc/pd-service-sage-adapter` | Sage ERP adapter |
| `svc/pd-service-hubspot-adapter` | HubSpot CRM adapter |
| `svc/pd-service-openhr-adapter` | OpenHR adapter |
| `svc/pd-service-cobee-adapter` | Cobee adapter |
| `svc/pd-service-aeat-adapter` | AEAT (tax authority) adapter |
| `svc/pd-service-azuread-adapter` | Azure AD adapter |
| `svc/pd-service-sharepoint-adapter` | SharePoint adapter |
| `svc/pd-service-slango-adapter` | Slango adapter |
| `svc/pd-service-it-adapter` | IT adapter |
| `svc/pd-infra-reverse-proxy` | Reverse proxy |

- **Verify**: `curl -s -o /dev/null -w "%{http_code}" http://localhost:<port>/health`
- **Note**: Most require auth for external access. For internal calls use `kubectl exec` instead.
- **Tip**: Use different local ports when forwarding multiple APIs simultaneously:
  ```bash
  kubectl --context=prod port-forward -n plataformadato svc/pd-service-backoffice-api 8001:8000 &
  kubectl --context=prod port-forward -n plataformadato svc/mp-service-obligations-api 8002:8000 &
  ```

## gestordocumental

| Service | Local port | Remote port |
|---|---|---|
| `svc/pd-service-gestor-documental-api` | 8000 | 8000 |
