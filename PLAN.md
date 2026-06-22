# PLAN — GS Sprint B+D (badges + generator + outputs)
**Created:** 2026-06-22 | **Agent:** Claude | **Ref:** SP-010, GS-075
**Blast radius:** COMPLETO (audit.yml descubierto en segunda pasada)

---

## Blast radius por fase

### Fase B — badges/ → docs/badges/

| Archivo | Tipo | Cambio requerido |
|---------|------|-----------------|
| `scripts/metrics.py:21` | writer | `ROOT / "badges"` → `ROOT / "docs" / "badges"` |
| `README.md:8-12` | 5 shields.io URLs | `.../master/badges/` → `.../master/docs/badges/` |
| `.github/workflows/audit.yml:10,22` | CI trigger path | `"badges/**"` → `"docs/badges/**"` |
| `.github/workflows/audit.yml:59` | CI diff check | `badges/` → `docs/badges/` |
| `audit/AUDIT_TRAIL.md` | texto libre | NO es link — no rompe CI |

### Fase D1 — generate_golden_audit.py → scripts/

| Archivo | Tipo | Cambio requerido |
|---------|------|-----------------|
| `pyproject.toml` | pytest config | Agregar `[tool.pytest.ini_options] pythonpath = ["scripts"]` |
| `tests/test_infrastructure.py:25` | aserción CI | `"python generate_golden_audit.py"` → `"python scripts/generate_golden_audit.py"` |
| `tests/test_graph_navigation.py:6` | import | Sin cambio — pythonpath lo resuelve |
| `.github/workflows/audit.yml:6,18` | CI trigger path | `"generate_golden_audit.py"` → `"scripts/generate_golden_audit.py"` |
| `.github/workflows/audit.yml:50` | CI run command | `python generate_golden_audit.py` → `python scripts/generate_golden_audit.py` |
| `README.md:104,107,139,232` | texto/path | 4 refs actualizar |
| `CONTRIBUTING.md` | texto | 1 ref |
| `CONCEPTUAL_FRAMEWORK.md` | texto | 1 ref |
| `Wiki/Home.md` | link | actualizar |
| `Wiki/Graph.md` | ref | verificar y actualizar |
| `Wiki/Vices/VC-030.md` | ref | actualizar |
| `Wiki/Vices/VT-105.md` | ref | actualizar |
| `Wiki/Evidence/generate_golden_audit_py.md` | título/path | actualizar |
| `.claude/settings.local.json` | permisos Claude Code | `"Bash(python generate_golden_audit.py)"` → stale pero no rompe CI; anotar |

**Validator check** `validate_golden_standard_catalogs.py:742`: busca substring `"generate_golden_audit.py"` en audit.yml. Después del cambio audit.yml tendrá `"scripts/generate_golden_audit.py"` — substring sigue presente. ✓ No requiere cambio en el validator.

### Fase D2 — JSON outputs + audit_report → output/

| Archivo | Tipo | Cambio requerido |
|---------|------|-----------------|
| `generate_golden_audit.py:48-49,53` | writer paths | `_ROOT / "golden_standard_*.json"` → `_ROOT / "output" / "..."` |
| `generate_golden_audit.py:49` | writer path | `MARKDOWN_OUTPUT` → `_ROOT / "output" / "golden_standard_audit_report.md"` |
| `scripts/metrics.py:112` | writer | `ROOT / "golden_standard_metrics.json"` → `ROOT / "output" / "golden_standard_metrics.json"` |
| `scripts/analyze_graph.py:174` | reader default | `Path("golden_standard_graph.json")` → `Path("output/golden_standard_graph.json")` |
| `tests/test_graph_navigation.py:69` | reader | `ROOT / "golden_standard_graph.json"` → `ROOT / "output" / "golden_standard_graph.json"` |
| `.github/workflows/audit.yml:7,19` | CI trigger | `"golden_standard*.json"` → `"output/golden_standard*.json"` |
| `.github/workflows/audit.yml:8,20` | CI trigger | `"golden_standard_audit_report.md"` → `"output/golden_standard_audit_report.md"` |
| `.github/workflows/audit.yml:54-58` | CI diff check | todos los paths → `output/golden_standard_*` |
| `audit/sessions/golden_standard_audit_report.md` | git mv | → `output/golden_standard_audit_report.md` (corrección: no es session record) |
| `README.md:88,140` | tree/texto | actualizar paths |
| `Wiki/Home.md:25` | link | `../audit/sessions/...` → `../output/golden_standard_audit_report.md` |
| `Wiki/Graph.md` | link a graph.json | actualizar path |
| `Wiki/Home.md:27` | link a graph.json | verificar y actualizar |
| `.claude/settings.local.json` | permisos | `golden_standard_audit.json` en Bash permissions — stale, no rompe CI |

**Inconsistencia heredada de Phase 2:** `golden_standard_audit_report.md` fue movido a `audit/sessions/` pero el generator lo escribe en root. D2 resuelve: generator escribe a `output/`, git mv mueve el snapshot histórico, validator/wiki links actualizados.

---

## Dependencias

```
B (independiente — solo metrics.py + README + audit.yml)
↓
D1 (independiente de B; actualiza audit.yml en el mismo commit)
↓
D2 (requiere D1 — el generator en scripts/ escribe a output/)
```

B y D1 pueden ir en commits separados o juntos. D2 siempre después de D1.

---

## Pasos numerados

### Fase B (5 cambios + CI)
- B1: `git mv badges/ docs/badges/` (crear docs/badges/ primero si no existe)
- B2: `scripts/metrics.py:21` — `BADGES = ROOT / "docs" / "badges"`
- B3: `README.md:8-12` — 5 URLs shields.io
- B4: `.github/workflows/audit.yml:10,22,59` — paths CI
- B5: CI check local (`pytest` + validator)

### Fase D1 (14 cambios + CI)
- D1-1: `pyproject.toml` — agregar `[tool.pytest.ini_options]`
- D1-2: `git mv generate_golden_audit.py scripts/generate_golden_audit.py`
- D1-3: `.github/workflows/audit.yml:6,18,50` — paths + comando
- D1-4: `tests/test_infrastructure.py:25` — comando CI
- D1-5: `README.md` — 4 refs
- D1-6: `CONTRIBUTING.md` — 1 ref
- D1-7: `CONCEPTUAL_FRAMEWORK.md` — 1 ref
- D1-8: `Wiki/Home.md` — link
- D1-9: `Wiki/Graph.md` — ref
- D1-10: `Wiki/Vices/VC-030.md` — ref
- D1-11: `Wiki/Vices/VT-105.md` — ref
- D1-12: `Wiki/Evidence/generate_golden_audit_py.md` — path
- D1-13: CI check local (`pytest` + validator)

### Fase D2 (13 cambios + CI)
- D2-1: `mkdir output/`
- D2-2: `generate_golden_audit.py:48-49,53` — output paths (ahora en scripts/)
- D2-3: `scripts/metrics.py:112` — metrics output path
- D2-4: `scripts/analyze_graph.py:174` — graph read path
- D2-5: `tests/test_graph_navigation.py:69` — graph read path
- D2-6: `.github/workflows/audit.yml:7,8,19,20,54-58` — todos los output paths
- D2-7: `git mv audit/sessions/golden_standard_audit_report.md output/`
- D2-8: `README.md:88,140` — refs
- D2-9: `Wiki/Home.md:25,27` — links
- D2-10: `Wiki/Graph.md` — link graph.json
- D2-11: Mover los 3 JSON actuales a output/ (o regenerar): `mv golden_standard_*.json output/`
- D2-12: CI check local (`pytest` + validator + verificar que generator escribe en output/)

### Cierre
- E1: STATE.md
- E2: Session record + AUDIT_TRAIL
- E3: HANDOFF.md
- E4: Commit + `rm PLAN.md`

---

## Angry path
1. **pythonpath no resuelve el import:** si pytest no agrega scripts/ al path, `from generate_golden_audit import` falla. Mitigation: D1-1 (pyproject.toml) va ANTES de D1-2 en el mismo commit; si falla, revert y usar `conftest.py` en su lugar.
2. **shields.io CDN lag post-B:** badges muestran error temporalmente. Mitigation: aceptable.
3. **audit.yml diff check falla en CI:** la verificación `git diff --exit-code` compara con HEAD. Si el commit incluye los archivos movidos, el diff sería 0. Mitigation: B, D1, D2 cada uno en un commit limpio — el CI corre contra el estado final del commit.
4. **generator en scripts/ no encuentra ROOT:** `_ROOT = Path(__file__).resolve().parent.parent` apuntaría a `scripts/../` = root GS. Verificar que esta línea existe en el generator antes de ejecutar D1-2.

---

## Acceptance criteria
- [ ] `pytest tests/ -q` → 10 passed
- [ ] `python scripts/validate_golden_standard_catalogs.py` → green
- [ ] `badges/` NO existe en root; `docs/badges/` tiene 6 JSONs
- [ ] `generate_golden_audit.py` NO existe en root; `scripts/generate_golden_audit.py` existe
- [ ] `output/` existe con los 4 artefactos generados
- [ ] 0 archivos `golden_standard_*.json` en root
- [ ] `golden_standard_audit_report.md` NO está en `audit/sessions/`
- [ ] `python scripts/generate_golden_audit.py` corre sin error desde root
- [ ] PLAN.md eliminado
