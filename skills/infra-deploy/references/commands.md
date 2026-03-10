# Deploy Commands Reference

All placeholders come from the project's CLAUDE.md `## Infrastructure` section.

## Step 1 — Verify PR is merged

```bash
gh pr view <PR-number> --json state,mergedAt,title
```

PR must be `MERGED`. If not, stop.

## Step 2 — Find the image tag (build run ID)

```bash
# Get PR merge date
gh pr view <PR-number> --json mergedAt --jq '.mergedAt'

# List recent build runs, match by date
gh run list --workflow "<build-workflow>" --limit 10

# Confirm image tag from build logs
gh run view <run-id> --log 2>&1 | grep -i "IMAGE_VERSION"
```

The `IMAGE_VERSION` in the logs equals the run ID (image tag).

**Multiple PRs merged since last deploy:** The latest build image includes all of them. Show the user which PRs are included.

## Step 3 — Check what's currently deployed

```bash
gh run list --workflow "<deploy-workflow>" --limit 1
gh run view <last-deploy-run-id> --log 2>&1 | grep -i "<image-tag-input>"
```

## Step 5 — Trigger deployment

```bash
gh workflow run "<deploy-workflow>" -f <image-tag-input>=<run-id>
```

## Step 6 — Verify deployment succeeded

```bash
gh run list --workflow "<deploy-workflow>" --limit 1 \
  --json databaseId,status,conclusion,createdAt
```

Wait for `status: completed` and `conclusion: success`.

## Step 7 — Check for pending migrations

```bash
gh pr view <PR-number> --json files --jq '.files[].path' | grep migrations
```

If migration files found → follow **infra-migrations** skill.
