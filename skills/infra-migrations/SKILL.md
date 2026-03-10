---
name: infra-migrations
description: Use when user asks to run database migrations, create tables, apply schema changes, or mentions "migration" in the context of DEV or PROD environments. Use when user mentions "migrate", "migration:up", "create table", or "schema changes" for remote environments.
disable-model-invocation: true
allowed-tools: Bash, Read, AskUserQuestion
model: haiku
---

# Running Database Migrations

## Overview

Run MikroORM migrations on remote environments (DEV/PROD) via port-forward to PgBouncer, since `@mikro-orm/migrations` is a devDependency not available in production images.

## Configuration

Read project-specific values from the project's CLAUDE.md (`## Infrastructure` section):
- kubectl contexts, namespace, PgBouncer service name, database names
- Migration npm script (e.g. `npm run migrations:up`)

## Process

```dot
digraph migrate {
    rankdir=TB;
    node [shape=box];
    fetch [label="1. Identify migrations & source PR"];
    confirm [label="2. Confirm with user"];
    get_password [label="3. Get DB password from pod"];
    port_forward [label="4. Port-forward (local 16432/16433)"];
    run_migration [label="5. Run migration:up"];
    verify [label="6. Verify no pending"];
    close [label="7. Close port-forward"];
    next_env [label="More envs?" shape=diamond];
    fetch -> confirm -> get_password -> port_forward -> run_migration -> verify -> close -> next_env;
    next_env -> get_password [label="yes"];
    next_env -> done [label="no"];
    done [label="Done"];
}
```

See [references/commands.md](references/commands.md) for all shell commands per step.

## Order of Operations

**Always run DEV first.** If DEV fails, do NOT proceed to PROD.

## Common Mistakes

| Mistake | Prevention |
|---|---|
| Running migrations inside the pod | `@mikro-orm/migrations` is a devDependency. Run locally via port-forward. |
| Not reading CLAUDE.md first | Contexts, namespace, DB names, and scripts vary per project. |
| Port conflict between envs | Use local port `16432` for DEV, `16433` for PROD. |
| Not quoting the password | Special chars (`#`, `?`) — always single-quote. |
| Running PROD before DEV | Always verify DEV first. |
| `CheckConstraintViolationException` on UPDATE | `DROP CONSTRAINT IF EXISTS` **before** the UPDATE, re-add after. |
| Ghost entries in `mikro_orm_migrations` | Consolidated/deleted migrations — harmless, MikroORM ignores them. |
