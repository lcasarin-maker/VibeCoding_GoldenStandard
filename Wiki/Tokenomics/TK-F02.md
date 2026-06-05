# TK-F02: Poda contextual primitiva

| Campo | Detalle |
|---|---|
| **ID** | `TK-F02` |
| **Categoría** | Tokenomics |
| **Estado** | **DOC_ONLY** |
| **Severidad** | **low** |
| **Profundidad** | 🟢 Deep |
| **Tags** | `tokenomics`, `doc-only` |
| **Downstream Verification** | `required` |
| **Mecanismo de Validación** | `DOC_ONLY` |

---

### Síntoma (Signal)
> Tareas pequeñas cargan documentos completos

### Causa (Cause)
Recuperacion no selectiva

### Aplicación / Mitigación
Extraer solo fragmentos relevantes

### Relevancia Operativa
Behavioral/doctrinal tokenomics vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_d10_tokenomics to DOC_ONLY.

### ❌ Ejemplo del vicio (Bad)
```python
# Tarea minuscula que carga el documento entero.
ctx = open("manual_500p.md").read()
answer = call(model, ctx + "cual es el limite de reintentos?")
```

### ✅ Versión corregida (Good)
```python
# Recuperar solo el fragmento relevante.
ctx = retrieve("manual_500p.md", query="limite de reintentos", k=1)
answer = call(model, ctx + "...")
```

### 🔎 Detección concreta
Cargar documentos completos para consultas localizadas en vez de recuperar
fragmentos relevantes.

### 📚 Evidencia externa
- **vexp.dev / HumanLayer ACE** — el contexto sin estructura consume 3-5x mas tokens; recuperacion selectiva, caching y compactacion son las palancas centrales.

---
[[Tokenomics_Map|Volver al Mapa de Tokenomics]] | [[Tokenomics_Index|Volver al Índice de Tokenomics]] | [[Home|Inicio]]
