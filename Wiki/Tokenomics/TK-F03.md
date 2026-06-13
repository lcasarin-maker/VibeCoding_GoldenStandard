# TK-F03: Excessive verbal output

| Field | Detail |
|---|---|
| **ID** | `TK-F03` |
| **Category** | Tokenomics |
| **Status** | **DOC_ONLY** |
| **Severity** | **low** |
| **Depth** | 🟢 Deep |
| **Tags** | `tokenomics`, `doc-only` |
| **Downstream Verification** | `required` |
| **Validation Mechanism** | `DOC_ONLY` |

---

### Symptom (Signal)
> Preambles, explanations, and closings add no value

### Cause
Missing output budget

### Application / Mitigation
Constrain output format and length

### Operational Relevance
Behavioral/doctrinal tokenomics vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_d10_tokenomics to DOC_ONLY.

### ❌ Example of the vice (Bad)
```text
# Prompt with no output budget -> useless preambles and closings.
"Explain why and then give me the JSON"   -> 600 tokens of prose + JSON
```

### ✅ Corrected version (Good)
```text
# Constrain the output format and length.
"Respond ONLY with the JSON, no additional text."   -> ~40 tokens
```

### 🔎 Concrete detection
Outputs with preamble/explanation/closing when the task only requires the
datum; absence of format or length constraints.

### 📚 External evidence
- **vexp.dev / HumanLayer ACE** — unstructured context consumes 3-5x more tokens; selective retrieval, caching, and compaction are the central levers.

---
[[Tokenomics_Map|Back to Tokenomics Map]] | [[Tokenomics_Index|Back to Tokenomics Index]] | [[Home|Home]]
