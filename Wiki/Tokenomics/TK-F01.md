# TK-F01: Reprocesamiento de contexto estable

| Campo | Detalle |
|---|---|
| **ID** | `TK-F01` |
| **Categoría** | Tokenomics |
| **Estado** | **DOC_ONLY** |
| **Severidad** | **low** |
| **Profundidad** | 🟢 Deep |
| **Tags** | `tokenomics`, `doc-only` |
| **Downstream Verification** | `required` |
| **Mecanismo de Validación** | `DOC_ONLY` |

---

### Síntoma (Signal)
> El mismo bloque se paga o procesa muchas veces

### Causa (Cause)
Reuso no modelado

### Aplicación / Mitigación
Separar contexto estable y contexto volatil

### Relevancia Operativa
Behavioral/doctrinal tokenomics vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_d10_tokenomics to DOC_ONLY.

### ❌ Ejemplo del vicio (Bad)
```python
# Se reenvia el mismo bloque estable en cada llamada: se paga N veces.
for q in questions:
    call(model, system=BIG_STABLE_DOCS + q)     # sin cache
```

### ✅ Versión corregida (Good)
```python
# Marcar el prefijo estable como cacheable: se paga una vez.
call(model, system=[{"text": BIG_STABLE_DOCS, "cache_control": {"type": "ephemeral"}}, q])
```

### 🔎 Detección concreta
Llamadas repetidas que reenvian un mismo prefijo estable sin prompt caching /
cache_control.

### 📚 Evidencia externa
- **vexp.dev / HumanLayer ACE** — el contexto sin estructura consume 3-5x mas tokens; recuperacion selectiva, caching y compactacion son las palancas centrales.

---
[[Tokenomics_Map|Volver al Mapa de Tokenomics]] | [[Tokenomics_Index|Volver al Índice de Tokenomics]] | [[Home|Inicio]]
