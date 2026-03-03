---
name: analyze-data-model
description: Use when interrogating the codebase to understand an entity, field, or business concept. Traces data origin, mutations, validations, and relationships without assumptions. Use when user says "analiza entidad", "de dónde viene este dato", "analyze data model", "qué campos tiene", "quién genera este campo", or "explica esta entidad".
argument-hint: "[entity name, field name, or business concept]"
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# Analyze Data Model

Interrogate the codebase to understand an entity or data concept. Trace where each field comes from, who generates it, under what conditions, and what values it can have. A field existing in code does NOT mean it is understood.

## Instructions

### 1. Parse argument

`$ARGUMENTS` can be:
- An entity class name: `Obligation`, `ContractedService`
- A field name: `totalAmount`, `isActive`
- A business concept: `"monto total"`, `"estado activo"`

If not provided, ask the user.

### 2. Locate in code

Search for the entity/concept across the codebase:

```
Glob → src/domain/models/**/*.ts         (entities)
Glob → src/domain/services/**/*.ts       (services)
Glob → src/domain/enums/**/*.ts          (enums)
Glob → src/**/dto/**/*.ts                (DTOs)
Glob → src/migrations/**/*.ts            (migrations)
Grep → "<term>" in src/                  (all references)
```

If the argument is a business concept (not a class name), search broadly — it may appear as a field name, comment, enum value, or variable.

### 3. Interrogate each field

For each field found on the entity, build a profile. **Do not assume anything from the name alone.**

```
[fieldName] (type: X | nullable: yes/no | default: Y)

  ¿Qué significa?
    → [inference from name, comments, or usage — or ❌ "Not clear from code alone"]

  ¿De dónde viene?
    → Search who calls em.persist(), em.assign(), or sets this field
    → Possible sources: AMQP consumer, REST endpoint, seed/migration, calculated
    → If not found: ❌ "No code path found that sets this field"

  ¿Quién lo genera?
    → [ServiceName.methodName() | ConsumerName.handler() | Migration | ❌ Unknown]

  ¿Cuándo se crea?
    → [condition found in code — e.g. "when AMQP event arrives with updatedAt > existing"]
    → If not found: ❌ "No creation condition found"

  ¿Cuándo cambia?
    → Search for assignments to this field after creation
    → [ServiceName.methodName() under condition X | ❌ "Never changes after creation" | ❌ "Not found"]

  ¿Validaciones?
    → Search in DTOs (class-validator decorators), services (manual checks), pipes
    → [list validations found | ❌ "No validation found"]

  ¿Qué valores puede tener?
    → For enums: list all values
    → For booleans: what does true mean? what does false mean?
    → For numbers: any min/max? Is 0 valid? Negative?
    → For strings: any format? Max length?
    → [restrictions found | ❌ "No restrictions visible in code"]
```

### 4. Map relationships

```
Grep → entity name in other entity files (FK references)
```

For each relationship:
- Direction and cardinality (1:M, M:1, M:M)
- Is it eager or lazy loaded?
- Cascade behavior (what happens on delete?)
- Is the FK nullable?

### 5. Check migrations

```
Glob → src/migrations/*.ts
Grep → table name in migrations
```

For recent migrations affecting this entity:
- What changed? (new column, type change, constraint added)
- When? (migration timestamp)
- Why? (commit message if visible)

### 6. Check consumers and endpoints

Search for where this entity is exposed or consumed:

```
Grep → "EntityName" in src/**/controllers/**/*.ts    (REST endpoints)
Grep → "EntityName" in src/**/consumers/**/*.ts      (AMQP consumers)
Grep → "EntityName" in src/**/services/**/*.ts       (internal usage)
```

### 7. Output

```
🔍 ANÁLISIS: [Entity/Concept]
   Archivo: [path to entity file]
   Tabla: [database table name]

   CAMPOS:
   ┌────────────┬─────────┬──────────┬─────────┬──────────────────────────────┐
   │ Campo      │ Tipo    │ Nullable │ Default │ Estado                       │
   ├────────────┼─────────┼──────────┼─────────┼──────────────────────────────┤
   │ id         │ string  │ no       │ uuid4() │ ✅ Claro — PK generado auto │
   │ isActive   │ boolean │ no       │ false   │ ⚠️ ¿Qué significa "activo"? │
   │ totalAmount│ float   │ no       │ 0       │ ❌ ¿Incluye impuestos?      │
   └────────────┴─────────┴──────────┴─────────┴──────────────────────────────┘

   ORIGEN DE DATOS:
   - Creado por: [service/consumer] en [file:line]
     Condición: [when X happens]
   - Modificado por: [service/method] en [file:line]
     Condición: [when Y happens]

   RELACIONES:
   - → Client (M:1 via client_id, nullable: no)
   - ← ClientObligation (1:M)

   VALIDACIONES:
   - [field]: [validation found in DTO or service]
   - [field]: ❌ Sin validación

   MIGRACIONES RECIENTES:
   - [MigrationName]: [change description]

   ENDPOINTS/CONSUMERS:
   - GET /v1/[path] → [what it returns]
   - AMQP [queue] → [what it processes]

   PREGUNTAS:
   1. [field] tiene default 0 — ¿es un valor válido de negocio o indica "no calculado"?
   2. [field] no tiene validación — ¿debería tenerla? ¿qué rango es válido?
   3. ...
```

## Edge cases

- If the entity doesn't exist in code, say so. It may be a concept that hasn't been implemented yet.
- If a field is a JSONB column (like `jiraRefs`, `erpRef`), document its known shape from usage (not from a schema, since JSONB is schema-less).
- If the argument matches multiple entities, analyze all of them and note the relationships.
- For enums imported from external packages (like `@afianza-ac/lib-core-definitions`), note they are external and list values if readable, or mark as "❓ External enum — values not inspectable from this codebase".
