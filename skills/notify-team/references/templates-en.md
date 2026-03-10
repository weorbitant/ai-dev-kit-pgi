# Slack Templates (EN)

## 🚨 Incident / Error

```
⚠️ *[PROD] <short title — what broke and where>*

*What's happening?*
One paragraph: what is failing, how it was detected, impact.

*Root cause:*
What is causing it. Specific: error, constraint, affected ID.

*<Extra sections if needed>*
Tables, lists, specific IDs.

*Proposed action:*
What needs to be done. Who should decide or act.

Can anyone confirm / has context on this?
```

## 📢 Announcement / Release

```
📢 *Release · <service> · <environment>*

Deploying the following changes to production:

• <business-language description> (<URL|PR#N>)
• <business-language description> (<URL|PR#N>)

Heads up in case anyone needs to be aware or has a blocker.
```

**Rules for describing changes:**
- Translate the commit title into business language — understandable by a non-technical person
- Use the format `Added / Fixed / Improved...`
- Never copy the raw commit title
- Link each change to its PR: `<https://github.com/org/repo/pull/N|PR#N>`
- Fetch titles and URLs with `gh pr view <N> --json title,url`

## ❓ Question to the team

```
*<direct question in the title>*

<Context needed to answer. Keep it brief.>

*Options:*
• Option A — <description>
• Option B — <description>

Does anyone have context or can decide?
```

## 🔄 Status update

```
*Update: <what changed or was resolved>*

*Status:* ✅ resolved / 🔄 in progress / ❌ blocked

<Next steps if applicable>
```

## 👀 Review request

```
*Review needed: <what needs to be reviewed>*

*Context:* <why review is needed, what decision needs to be made>

<Link or relevant detail>

Can anyone take a look?
```
