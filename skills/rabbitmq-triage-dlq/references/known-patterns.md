# Known Patterns and Output Format

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
