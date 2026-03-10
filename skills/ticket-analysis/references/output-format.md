# Output Format Reference

Template for the terminal output of `/ticket-analysis`.

## Design Principles

1. **Estructura fija** — todas las secciones aparecen siempre, en el mismo orden. Si una sección no tiene contenido, se muestra con "Ninguno" o "No aplica".
2. **Cero asunciones** — si hay la mínima duda, va como pregunta. No existe sección "Asumido".
3. **Trazabilidad** — cada hallazgo indica de dónde sale (fuente + cita o referencia concreta).
4. **Escaneable** — alguien debe poder revisar el output en 2 minutos y saber: qué hay, qué falta, qué hacer.

## Sections (always in this order)

```
1. CABECERA          — ticket key, título, tipo, estado
2. RESUMEN           — 3 líneas: qué pide el ticket, qué se analizó, resultado headline
3. FUENTES           — cada fuente consultada, qué se encontró, estado
4. DATOS             — tabla plana: dato, origen, estado
5. PREGUNTAS         — agrupadas por quién responde, con contexto y bloqueo
6. PRÓXIMOS PASOS    — acciones numeradas con responsable
7. SCOPE             — se entrega / no se entrega / bloqueado
8. VALIDACIONES      — checklist del ticket
```

## Full Output Template

```
═══════════════════════════════════════════════════════
[TICKET-KEY] · [Title]
Type: [type] | Status: [status] | SP: [points or —] | Category: [business-feature/technical-infra/bug-fix/data-integration]
═══════════════════════════════════════════════════════

RESUMEN
  Qué pide:     [1 frase describiendo qué pide el ticket]
  Se analizó:   Jira ✅ | Figma [✅/❌] | Confluence [✅/❌] | Notion [✅/❌] | Código ✅
  Resultado:    [N] datos identificados · [N] preguntas abiertas · [N] bloqueos

───────────────────────────────────────────────────────
FUENTES CONSULTADAS
───────────────────────────────────────────────────────

  JIRA — DEVPT-XXX
  Estado: ✅ Leído
  Hallazgos:
    - [hallazgo 1 — cita breve o resumen de lo encontrado]
    - [hallazgo 2]

  FIGMA — [URL o "No hay URL en el ticket"]
  Estado: [✅ Analizado / ❌ Sin diseño / ⚠️ Playwright fallback]
  Hallazgos:
    - [hallazgo 1]
    - [hallazgo 2]
  (Si no hay Figma: "No se encontró link a Figma en el ticket.")

  CONFLUENCE — [término buscado]
  Estado: [✅ Encontrado / ❌ Sin resultados / ❌ Sin acceso]
  Hallazgos:
    - "[cita textual]" — Página: [título], [link]
  (Si no hay resultados: "No se encontró documentación en Confluence sobre [términos].")

  NOTION — [término buscado]
  Estado: [✅ Encontrado / ❌ Sin resultados]
  Hallazgos:
    - "[cita textual]" — Página: [título], [link]
  (Si no hay resultados: "No se encontró documentación en Notion sobre [términos].")

  CÓDIGO — [entidades/servicios analizados]
  Estado: ✅ Analizado
  Hallazgos:
    - [entidad encontrada + campos relevantes]
    - [servicio encontrado + métodos relevantes]
    - [lo que NO existe y se esperaba encontrar]

  DEPENDENCIAS JIRA:
  (Solo si hay tickets referenciados en descripción, ACs o linked issues)
  - DEVPT-XXX "[Título]" — Estado: [Jira status] — [✅ Resuelto / ⚠️ En progreso / 🚧 Bloqueante]
    Impacto: [qué necesita este ticket del otro]
  - DEVPT-YYY "[Título]" — Estado: [Jira status] — [✅ Resuelto / ⚠️ En progreso / 🚧 Bloqueante]
    Impacto: [qué necesita este ticket del otro]
  (Si no hay tickets referenciados: "No se encontraron dependencias Jira.")

  FACTIBILIDAD TÉCNICA — [enfoque evaluado]
  (Solo si se lanzó Agent 4 — ticket type: technical-infra o propuesta técnica específica)
  Estado: [✅ Viable / ⚠️ Viable con cambios / ❌ Problemas]
  Hallazgos:
    - [dependencia instalada o faltante]
    - [patrón existente encontrado o ausente]
    - [gap de implementación identificado]
    - [riesgo detectado]
  (Si no aplica: esta sección no aparece)

───────────────────────────────────────────────────────
DATOS IDENTIFICADOS
───────────────────────────────────────────────────────

  Cada dato mencionado en cualquier fuente, una línea por dato:

  #  Dato                Tipo       Origen                         Estado
  ── ─────────────────── ────────── ────────────────────────────── ──────
  1  [nombre]            dato       [de dónde sale — fuente]       ✅ / ❓ / ❌
  2  [nombre]            config     [de dónde sale — fuente]       ✅ / ❓ / ❌
  3  [nombre]            mecanismo  [de dónde sale — fuente]       ✅ / ❓ / ❌
  ...

  Tipos:
  dato      — campo de entidad, valor de negocio
  config    — parámetro de configuración (env var, config file, hardcoded)
  mecanismo — concepto técnico (lock, scheduler, cron job, cache strategy)

  Leyenda:
  ✅ Claro    — se sabe qué es, de dónde viene, qué valores tiene
  ❓ Dudoso   — existe pero hay preguntas (ver sección PREGUNTAS)
  ❌ No existe — mencionado en ticket/diseño pero no existe en código ni docs

  Si un dato tiene estado ❓ o ❌, DEBE tener al menos una pregunta
  en la sección PREGUNTAS. Sin excepción.

───────────────────────────────────────────────────────
PREGUNTAS
───────────────────────────────────────────────────────

  Agrupadas por quién debe responder. Cada pregunta tiene:
  - Número secuencial (referenciado en SCOPE y PRÓXIMOS PASOS)
  - Contexto: de dónde sale la duda, con cita de la fuente
  - Pregunta concreta
  - Qué bloquea si no se responde

  PARA EL PO / NEGOCIO:
  (Preguntas en lenguaje no técnico. Sin jerga. Con ejemplo concreto.)

  #1 · [título corto de la pregunta]
       Contexto:  [de dónde sale la duda — fuente + cita]
       Pregunta:  [pregunta concreta, sin jerga técnica]
       Ejemplo:   [ejemplo tangible para que el PO entienda]
       Bloquea:   [qué no se puede hacer sin respuesta]

  #2 · [título corto]
       Contexto:  ...
       Pregunta:  ...
       Ejemplo:   ...
       Bloquea:   ...

  PARA EL TECH LEAD / EQUIPO DEV:
  (Preguntas técnicas que el equipo puede resolver internamente.)

  #N · [título corto]
       Contexto:  [referencia técnica — archivo, línea, migración]
       Pregunta:  [pregunta técnica]
       Bloquea:   [qué no se puede hacer sin respuesta]

  PARA DISEÑO:
  (Solo si hay gaps de diseño detectados.)

  #N · [título corto]
       Contexto:  [qué falta en el diseño]
       Pregunta:  [qué se necesita]
       Bloquea:   [qué no se puede implementar sin diseño]

  (Si un grupo no tiene preguntas, mostrar: "Ninguna pregunta para [rol].")

───────────────────────────────────────────────────────
PRÓXIMOS PASOS
───────────────────────────────────────────────────────

  Acciones concretas numeradas. Cada una tiene responsable.
  Ordenadas por prioridad (lo que desbloquea más primero).

  1. [Responsable] · [acción concreta] — desbloquea pregunta #[N]
  2. [Responsable] · [acción concreta] — desbloquea pregunta #[N]
  3. [Dev] · [lo que se puede empezar ya sin esperar respuestas]
  ...

  SE PUEDE EMPEZAR YA:
  - [item que no depende de ninguna pregunta]

  REQUIERE RESPUESTA PRIMERO:
  - [item] — espera pregunta #[N]

  SUGERENCIA DE ESTRUCTURA:
  (Solo para tickets technical-infra. No aparece en otros tipos.)
  - [Módulo]: ¿Crear [NuevoModule] o extender [ExistenteModule]? [razonamiento]
  - [Servicio]: [NombreService] en [path propuesto] — responsabilidad: [X]
  - [Testing]: [estrategia — TestContainers / mock / in-memory]
  - [Config]: [variables de entorno necesarias]

  (Cuando hay trade-offs:)
  Opción A: [descripción] (Pro: [ventaja] / Contra: [desventaja])
  Opción B: [descripción] (Pro: [ventaja] / Contra: [desventaja])

───────────────────────────────────────────────────────
SCOPE
───────────────────────────────────────────────────────

  ✅ SE ENTREGA:
     - [item concreto]: [qué se implementa exactamente]

  ❌ NO SE ENTREGA:
     - [item]: [razón — "no mencionado en ACs" / "fuera de alcance"]

  🚧 BLOQUEADO:
     - [item]: esperando respuesta a pregunta #[N]

  (No hay sección "Asumido". Si hay duda, va a PREGUNTAS.)

───────────────────────────────────────────────────────
VALIDACIONES DEL TICKET
───────────────────────────────────────────────────────

  [✅/❌] Descripción         [presente / ausente o insuficiente]
  [✅/❌] Criterios aceptación [presentes / ausentes]
  [✅/❌] Link a Figma         [presente / no requerido / ausente y se necesita]
  [✅/❌] Story points         [estimados / sin estimar]
  [✅/❌] Subtareas            [existen / no existen y se sugiere dividir]

═══════════════════════════════════════════════════════
```

## Rules

### Structure
- **ALL 8 sections appear ALWAYS**, in the exact order above.
- If a section has no content, show it with "Ninguno" or "No aplica". NEVER omit a section.
- This makes the output predictable — the reader always knows where to look.

### Zero assumptions
- If there is ANY doubt about a data element, it gets status ❓ or ❌ and a question in PREGUNTAS.
- There is NO "Asumido" section. If you're tempted to write "Se asume que...", write a question instead.
- Better to ask a "dumb" question than to silently assume something wrong.

### Traceability
- Every finding in FUENTES must cite where it came from: page title, URL, or file path.
- Every finding from documentation must include a direct quote in quotes.
- Every finding from code must reference the file (e.g. `obligation.ts:15`).
- The DATOS table's "Origen" column must trace back to a specific source in FUENTES.

### Scannability
- RESUMEN is 3 lines max. It tells you: what, where, how many problems.
- DATOS is a flat table — one line per data element. No nested cards.
- PREGUNTAS are grouped by role — the PO only reads their section.
- PRÓXIMOS PASOS are ordered by priority — do the most impactful first.
- SCOPE is the conclusion — derived from everything above.

### Questions format
- Every question has a sequential number (#1, #2, ...) used across the entire document.
- SCOPE references question numbers: "bloqueado por #3".
- PRÓXIMOS PASOS references question numbers: "desbloquea #3".
- This creates a traceable chain: dato ❓ → pregunta #N → bloqueo en scope → próximo paso.

### Data element status
- ✅ **Claro**: se sabe qué es, de dónde viene, qué valores tiene, quién lo genera, cuándo. No quedan dudas.
- ❓ **Dudoso**: existe parcialmente pero hay al menos una pregunta abierta. MUST have a question in PREGUNTAS.
- ❌ **No existe**: mencionado en ticket/diseño pero no existe en código ni docs. MUST have a question in PREGUNTAS.
