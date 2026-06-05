# TK-F03: Salida verbal excesiva

| Campo | Detalle |
|---|---|
| **ID** | `TK-F03` |
| **Categoría** | Tokenomics |
| **Estado** | **DOC_ONLY** |
| **Severidad** | **low** |
| **Profundidad** | 🟢 Deep |
| **Tags** | `tokenomics`, `doc-only` |
| **Downstream Verification** | `required` |
| **Mecanismo de Validación** | `DOC_ONLY` |

---

### Síntoma (Signal)
> Preámbulos, explicaciones y cierres no agregan valor

### Causa (Cause)
Presupuesto de salida ausente

### Aplicación / Mitigación
Restringir formato y longitud de salida

### Relevancia Operativa
Behavioral/doctrinal tokenomics vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_d10_tokenomics to DOC_ONLY.

### ❌ Ejemplo del vicio (Bad)
```text
# Prompt sin presupuesto de salida -> preambulos y cierres inutiles.
"Explica por que y luego dame el JSON"   -> 600 tokens de prosa + JSON
```

### ✅ Versión corregida (Good)
```text
# Restringir el formato y la longitud de salida.
"Responde SOLO con el JSON, sin texto adicional."   -> ~40 tokens
```

### 🔎 Detección concreta
Salidas con preambulo/explicacion/cierre cuando la tarea solo requiere el dato;
ausencia de restriccion de formato o longitud.

### 📚 Evidencia externa
- **vexp.dev / HumanLayer ACE** — el contexto sin estructura consume 3-5x mas tokens; recuperacion selectiva, caching y compactacion son las palancas centrales.

---
[[Tokenomics_Map|Volver al Mapa de Tokenomics]] | [[Tokenomics_Index|Volver al Índice de Tokenomics]] | [[Home|Inicio]]
