# Workflow: Análisis de tickets antes de implementar

Guía para todo el equipo sobre cómo funciona el proceso de análisis de tickets usando las herramientas de Claude Code.

---

## Por qué existe este proceso

Antes teníamos estos problemas recurrentes:

- El dev empieza a implementar y descubre que no entiende qué es un dato
- El diseño en Figma no cubre todos los estados (errores, vacíos, loading)
- Las dudas técnicas se resuelven tarde, cuando ya hay código escrito
- No queda claro qué se entrega y qué no hasta la review
- La documentación está dispersa entre Jira, Figma, Confluence, Notion y código

Este proceso soluciona esto **antes de escribir una línea de código**.

---

## Resumen del flujo

```
┌──────────┐    ┌───────────────┐    ┌──────────────┐    ┌────────────┐
│ Ticket   │ →  │ Análisis      │ →  │ Preguntas +  │ →  │ Implementar│
│ creado   │    │ automático    │    │ Scope claro  │    │ con todo   │
│ en Jira  │    │ (Claude Code) │    │ (equipo)     │    │ definido   │
└──────────┘    └───────────────┘    └──────────────┘    └────────────┘
```

---

## Roles en el proceso

| Rol | Qué hace | Qué recibe |
|-----|----------|------------|
| **Dev** | Ejecuta `/ticket-analysis` antes de implementar | Mapa de datos, preguntas técnicas, scope |
| **PO / Negocio** | Responde preguntas de negocio en el ticket de Jira | Preguntas claras, sin jerga técnica, con ejemplos |
| **Diseño** | Revisa gaps detectados en Figma | Lista de estados faltantes, campos sin correspondencia |
| **QA** | Usa el scope para planificar testing | Lista de qué se entrega, qué no, qué se asume |
| **Tech Lead** | Revisa blockers técnicos y decisiones de arquitectura | Preguntas técnicas separadas de las de negocio |

---

## Paso a paso

### 1. El dev toma un ticket

Cuando un ticket pasa a "In Progress" o el dev lo va a empezar, **antes de escribir código** ejecuta en Claude Code:

```
/ticket-analysis DEVPT-XX
```

Esto lanza un análisis automático que:
- Lee el ticket completo de Jira
- Analiza los diseños de Figma (si hay links)
- Busca documentación en Confluence y Notion
- Interroga el código fuente (entidades, servicios, migraciones)

### 2. El análisis produce un documento

El resultado tiene estas secciones:

#### Mapa de datos
Para **cada dato** mencionado en el ticket, diseño o código:

```
📋 isActive
   ¿Qué es?        ❌ Sin definir — ¿activo para facturar? ¿visible en UI?
   ¿De dónde viene? ❌ Desconocido — ¿lo activa el usuario? ¿viene de otro sistema?
   En código:       ClientObligation.isActive (boolean, default false)
   En diseño:       Toggle switch en la tabla
```

Cada dato se marca como:
- ✅ **Claro** — se entiende completamente
- ⚠️ **Parcial** — se entiende parcialmente, faltan detalles
- ❌ **Desconocido** — no se sabe qué es o de dónde viene

#### Preguntas bloqueantes

Separadas por audiencia:

**Para el PO / negocio** (sin jerga técnica):
> "¿Qué significa exactamente que una obligación esté 'activa'? Por ejemplo, si activo 'IVA Trimestral' para un cliente, ¿se empiezan a generar tareas automáticamente o es solo informativo? Sin esta información no podemos implementar el toggle."

**Para el equipo técnico:**
> "El campo `totalAmount` tiene default 0 — ¿es un valor válido o indica 'no calculado'? ¿Deberíamos validar que sea > 0?"

#### Scope

```
✅ SE ENTREGA:
   - GET /v1/clients/:id/obligations (listado con estado de activación)
   - PATCH toggle isActive

❌ NO SE ENTREGA:
   - Generación automática de tareas (no mencionado en ACs)

🚧 BLOQUEADO:
   - Lógica de vencimiento (no hay campo deadlineDay, pregunta #3)

⚠️ ASUMIDO:
   - Se asume que las 8 obligaciones del seed son las únicas. Si no es así, hay que añadir un CRUD.
```

### 3. Se publican las preguntas

El dev puede elegir que Claude:
- **Comente en Jira** — el análisis técnico completo para el equipo dev
- **Actualice la descripción** — las preguntas de negocio para el PO, en lenguaje claro
- **Ambas cosas**

### 4. El equipo responde

| Quién | Dónde responde | Qué responde |
|-------|----------------|--------------|
| PO | En el ticket de Jira (descripción o comentarios) | Preguntas de negocio |
| Diseño | En Figma (nuevas pantallas) o comentario en Jira | Estados faltantes |
| Tech Lead | Comentario en Jira o conversación directa | Decisiones técnicas |

### 5. Se re-analiza si es necesario

Si las respuestas cambian el scope o generan nuevas dudas, el dev puede volver a ejecutar:

```
/ticket-analysis DEVPT-XX
```

El análisis se ejecuta de nuevo con la información actualizada.

### 6. Se implementa con scope claro

Una vez resueltas las preguntas bloqueantes, el dev implementa **solo lo que está en la sección "SE ENTREGA"**. Lo que está en "BLOQUEADO" o "NO SE ENTREGA" queda explícitamente fuera.

---

## Herramientas disponibles (uso individual)

Además del análisis completo, cada fase se puede ejecutar por separado:

| Comando | Para qué | Ejemplo |
|---------|----------|---------|
| `/ticket-analysis DEVPT-XX` | Análisis completo de un ticket | `/ticket-analysis DEVPT-52` |
| `/analyze-design <url>` | Revisar un diseño de Figma | `/analyze-design https://figma.com/design/abc...` |
| `/analyze-docs <término>` | Buscar documentación sobre un concepto | `/analyze-docs "obligaciones fiscales"` |
| `/analyze-data-model <entidad>` | Entender una entidad del código | `/analyze-data-model ContractedService` |
| `/jira-clarify-ticket DEVPT-XX` | Clarificar un ticket (solo Jira, sin Figma/código) | `/jira-clarify-ticket DEVPT-45` |

**Cuándo usar cada uno:**

- **Antes de un grooming**: `/jira-clarify-ticket` para preparar preguntas
- **Revisando un diseño nuevo**: `/analyze-design` para detectar gaps
- **Antes de implementar**: `/ticket-analysis` (el completo)
- **Investigando un concepto**: `/analyze-docs` + `/analyze-data-model`

---

## El glosario de dominio

Cada análisis alimenta un **glosario vivo** en `docs/glossary.md`. Este glosario documenta:

- Qué es cada concepto de negocio
- De dónde viene cada dato
- Quién lo genera y bajo qué condiciones
- Campos clave con su significado

Los datos no confirmados se marcan con ❓. Se actualiza con cada ticket analizado.

**Esto resuelve** el problema de "nadie sabe qué significa este campo" — la próxima persona que toque ese código tiene un punto de referencia.

---

## Ejemplo real

```
Dev:     /ticket-analysis DEVPT-52

Claude:  ═══════════════════════════════════════════
         DEVPT-52 · Crear vista de obligaciones del cliente
         Type: Story | SP: 5
         ═══════════════════════════════════════════

         📊 RESUMEN
            Fuentes: Jira ✅ | Figma ✅ | Confluence ❌ | Código ✅
            Datos: 8 identificados | 3 claros | 3 parciales | 2 desconocidos

         📋 MAPA DE DATOS
            📋 isActive
               ¿Qué es?        ❌ Sin definir
               En código:       ClientObligation.isActive (boolean)
               En diseño:       Toggle switch
               Preguntas:       ¿Activar = generar tareas? ¿O solo informativo?

         🔴 BLOCKERS (negocio)
            1. "activar obligación"
               → Para PO: ¿Qué pasa cuando un usuario activa una obligación?
                 ¿Se crean tareas automáticas o es solo un registro?

         📦 SCOPE
            ✅ SE ENTREGA: API listado + toggle
            🚧 BLOQUEADO: Generación de tareas (pregunta #1)
            ⚠️ ASUMIDO: Solo las 8 obligaciones del seed

         ¿Qué acción quieres tomar?
         [1] Comentar en Jira  [2] Actualizar descripción  [3] Ambas  [4] Ninguna

Dev:     3

Claude:  ✅ Comentario técnico añadido a DEVPT-52
         ✅ Descripción actualizada con preguntas para el PO
```

El PO abre el ticket y ve:

> ### Preguntas bloqueantes (requieren decisión de negocio)
>
> 1. **Activación de obligaciones** — Cuando un usuario activa una obligación (por ejemplo, "IVA Trimestral") para un cliente, ¿qué debería pasar? ¿Se generan tareas con fechas de vencimiento automáticamente, o solo queda registrado como "activo" sin más efecto? Sin esto no podemos definir qué hace el botón de activar.

---

## FAQ

**¿Cuánto tarda el análisis?**
Entre 1-3 minutos dependiendo de cuántas fuentes haya (Figma, Confluence, etc.).

**¿Y si el ticket no tiene link a Figma?**
El análisis lo reporta como gap. Puedes usar `/analyze-design` después cuando tengas el diseño.

**¿El análisis modifica algo automáticamente?**
No. Siempre pregunta antes de comentar en Jira o actualizar la descripción.

**¿Puedo re-ejecutar el análisis?**
Sí, tantas veces como quieras. Cada ejecución lee la información más reciente.

**¿El glosario se actualiza solo?**
Solo si el dev lo elige como acción al final del análisis. No es automático.

**¿Qué pasa si Figma no está disponible?**
Se usa Playwright para tomar un screenshot del diseño como fallback.

**¿Funciona con cualquier proyecto de Afianza?**
Los skills están instalados a nivel personal (`~/.claude/skills/`), así que funcionan en cualquier proyecto. El glosario es por proyecto (`docs/glossary.md`).
