# Plantillas Slack (ES)

## 🚨 Incidente / Error

```
⚠️ *[PROD] <título corto — qué falló y dónde>*

*¿Qué está pasando?*
Un párrafo: qué falla, cómo se detectó, impacto.

*Causa raíz:*
Qué lo provoca. Específico: error, constraint, ID afectado.

*<Secciones extra si aplica>*
Tablas, listas, IDs concretos.

*Acción propuesta:*
Qué hay que hacer. Quién debe decidir o actuar.

¿Alguien puede confirmar / tiene contexto sobre esto?
```

## 📢 Anuncio / Release

```
📢 *Release · <servicio> · <entorno>*

Voy a desplegar a producción los siguientes cambios:

• <descripción en lenguaje de negocio> (<URL|PR#N>)
• <descripción en lenguaje de negocio> (<URL|PR#N>)

Aviso por si alguien necesita estar pendiente o tiene algún bloqueo.
```

**Reglas para describir los cambios:**
- Traduce el título del commit a lenguaje de negocio — que lo entienda alguien no técnico
- Usa el formato `Se añade / Se corrige / Se mejora...`
- Nunca copies el título del commit tal cual
- Enlaza cada cambio con su PR: `<https://github.com/org/repo/pull/N|PR#N>`
- Obtén títulos y URLs con `gh pr view <N> --json title,url`

## ❓ Pregunta al equipo

```
*<pregunta directa en el título>*

<Contexto necesario para responder. Ser breve.>

*Opciones:*
• Opción A — <descripción>
• Opción B — <descripción>

¿Alguien tiene contexto o puede decidir?
```

## 🔄 Actualización de estado

```
*Update: <qué cambió o se resolvió>*

*Estado:* ✅ resuelto / 🔄 en progreso / ❌ bloqueado

<Próximos pasos si aplica>
```

## 👀 Solicitud de revisión

```
*Revisión necesaria: <qué hay que revisar>*

*Contexto:* <por qué se necesita revisión, qué decisión hay que tomar>

<Enlace o detalle relevante>

¿Alguien puede echarle un ojo?
```
