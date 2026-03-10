---
name: infra-deploy
description: Use when user asks to deploy to production, check what's deployed, find a docker image tag for a PR, or trigger a production deployment. Use when user mentions "deploy", "prod", "production", "release", or "ship".
argument-hint: "[PR-number]"
disable-model-invocation: true
allowed-tools: Bash, AskUserQuestion
model: sonnet
---

# Deploying to Production

## Overview

Deploy a merged PR to production by finding its Docker image tag from the CI build and triggering the manual deployment workflow via GitHub CLI.

## Configuration

Read project-specific values from the project's CLAUDE.md (`## Infrastructure` section):
- Build workflow name, deploy workflow name, image tag input field name

The image tag is always the **GitHub Actions run ID** (numeric `databaseId`) of the build workflow run.

## Process

```dot
digraph deploy {
    rankdir=TB;
    node [shape=box];
    verify_merged [label="1. Verify PR is merged"];
    find_image [label="2. Find image tag (build run ID)"];
    check_deployed [label="3. Check what's currently deployed"];
    confirm [label="4. Confirm with user"];
    deploy [label="5. Trigger deployment workflow"];
    verify_deploy [label="6. Verify deployment succeeded"];
    has_migrations [label="PR has migrations?" shape=diamond];
    run_migrations [label="Follow infra-migrations skill"];
    done [label="Done"];
    verify_merged -> find_image -> check_deployed -> confirm -> deploy -> verify_deploy;
    verify_deploy -> has_migrations;
    has_migrations -> run_migrations [label="yes"];
    has_migrations -> done [label="no"];
    run_migrations -> done;
}
```

See [references/commands.md](references/commands.md) for all shell commands per step.

## Common Mistakes

| Mistake | Prevention |
|---|---|
| Not reading CLAUDE.md | Workflow names and input field vary per project. |
| Passing full registry URL as image tag | Only pass the numeric run ID. |
| Deploying a PR that isn't merged | Always verify PR state first. |
| Deploying without confirmation | Always show what will be deployed and ask. |
| Confusing build run ID with deploy run ID | Build = CI on merge. Deploy = manual workflow. |
| Not checking what's currently in prod | Always show current state before deploying. |
