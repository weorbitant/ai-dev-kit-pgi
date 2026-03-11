# ADR Template — English

Use this template when the detected language is English.

## Format

```markdown
# [Descriptive decision title]

**Start date**: YYYY-MM-DD
**Status**: Proposed | Under discussion | Accepted | Deprecated | Superseded by [ADR-xxx]
**Deciders**: [names, roles, or "team"]

## Context

[Define the key domain concepts involved. What each entity is, why it exists,
how it relates to the problem. Anyone reading this ADR should understand it
without looking elsewhere.]

[Current system situation. What motivated the need for this decision.]

## Problem

[What we need to solve concretely. A focused description of the problem,
not the solution.]

## Alternatives

### Option A: [Descriptive name]

[Brief description of the alternative.]

- **Pros**: [concrete advantages]
- **Cons**: [concrete disadvantages]

### Option B: [Descriptive name]

[Brief description of the alternative.]

- **Pros**: [concrete advantages]
- **Cons**: [concrete disadvantages]

[Add more options as needed.]

## Log

### YYYY-MM-DD

- [What was researched, discussed, or decided that day]
- [Relevant findings]
- [Identified pending items]

## Decision

[What was chosen and why. Reference the chosen option from the Alternatives section.
If not yet decided, leave empty or write "Pending decision".]

## Consequences

### Positive

- [Concrete benefit]

### Negative / Trade-offs

- [Accepted cost or risk]
```

## Style rules

- Direct language, no fluff
- Short sentences
- Use lists when there are more than 2 items
- Inline code with backticks for technical names (`EntityManager`, `deadline_config`)
- Code blocks for multi-line examples
- No emojis
- Empty sections: write "Pending" or "N/A", never remove the section
