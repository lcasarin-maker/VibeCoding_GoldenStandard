# TK-F01: Reprocessing stable context

| Field | Detail |
|---|---|
| **ID** | `TK-F01` |
| **Category** | Tokenomics |
| **Status** | **DOC_ONLY** |
| **Severity** | **low** |
| **Depth** | 🟢 Deep |
| **Tags** | `tokenomics`, `doc-only` |
| **Downstream Verification** | `required` |
| **Validation Mechanism** | `DOC_ONLY` |

---

### Symptom (Signal)
> The same block is paid for or processed many times

### Cause
Unmodeled reuse

### Application / Mitigation
Separate stable context from volatile context

### Operational Relevance
Behavioral/doctrinal tokenomics vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_d10_tokenomics to DOC_ONLY.

### ❌ Example of the vice (Bad)
```python
# The same stable block is resent on every call: paid for N times.
for q in questions:
    call(model, system=BIG_STABLE_DOCS + q)     # no cache
```

### ✅ Corrected version (Good)
```python
# Mark the stable prefix as cacheable: paid for once.
call(model, system=[{"text": BIG_STABLE_DOCS, "cache_control": {"type": "ephemeral"}}, q])
```

### 🔎 Concrete detection
Repeated calls that resend the same stable prefix without prompt caching /
cache_control.

### 📚 External evidence
- **vexp.dev / HumanLayer ACE** — unstructured context consumes 3-5x more tokens; selective retrieval, caching, and compaction are the central levers.

---
[[Tokenomics_Map|Back to Tokenomics Map]] | [[Tokenomics_Index|Back to Tokenomics Index]] | [[Home|Home]]
