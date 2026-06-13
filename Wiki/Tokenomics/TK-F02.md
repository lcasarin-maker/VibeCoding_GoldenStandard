# TK-F02: Primitive context pruning

| Field | Detail |
|---|---|
| **ID** | `TK-F02` |
| **Category** | Tokenomics |
| **Status** | **DOC_ONLY** |
| **Severity** | **low** |
| **Depth** | 🟢 Deep |
| **Tags** | `tokenomics`, `doc-only` |
| **Downstream Verification** | `required` |
| **Validation Mechanism** | `DOC_ONLY` |

---

### Symptom (Signal)
> Small tasks load entire documents

### Cause
Non-selective retrieval

### Application / Mitigation
Extract only the relevant fragments

### Operational Relevance
Behavioral/doctrinal tokenomics vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_d10_tokenomics to DOC_ONLY.

### ❌ Example of the vice (Bad)
```python
# Tiny task that loads the entire document.
ctx = open("manual_500p.md").read()
answer = call(model, ctx + "what is the retry limit?")
```

### ✅ Corrected version (Good)
```python
# Retrieve only the relevant fragment.
ctx = retrieve("manual_500p.md", query="retry limit", k=1)
answer = call(model, ctx + "...")
```

### 🔎 Concrete detection
Loading entire documents for localized queries instead of retrieving the
relevant fragments.

### 📚 External evidence
- **vexp.dev / HumanLayer ACE** — unstructured context consumes 3-5x more tokens; selective retrieval, caching, and compaction are the central levers.

---
[[Tokenomics_Map|Back to Tokenomics Map]] | [[Tokenomics_Index|Back to Tokenomics Index]] | [[Home|Home]]
