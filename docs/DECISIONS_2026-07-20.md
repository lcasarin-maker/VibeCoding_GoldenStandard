# Decisiones y Trabajo Pendiente — 2026-07-20

## Commits Listos para Aplicar (Rescatados de /tmp)

### Aequitas_OS
**commit_msg_aequitas.txt:** feat: F-75 conecta hallazgos de ruff al ledger único de deuda
- Nuevo backend/scripts/sync_lint_debt.py
- Regenera bloque LINT_DEBT_START/END en PLAN_MIGRACION_ATOM.md
- 18 hallazgos reales de ruff encontrados y corregidos en sesión
- **Status:** Revisar si aún aplica post-reconciliación

### Cerberus
**commit_msg_dead_code.txt:** chore: elimina 2 líneas de código muerto verificado
- vulture verification: 50 candidatos → 2 reales
- cerberus/cli/protocol_cli.py: PROJECT_DIR constante no usada
- dimensions/d3_dead_code.py: checks_total variable no leída
- Ratchet: 11839 → 11838 LOC

**commit_msg_flaky_fix.txt:** fix: D8 adversarial-coverage gap + flaky real
- test_measure_loc_cli_exclusion.py missing adversarial pattern
- test_approved_gate_shows_no_recommendations: multi-iteración race condition
- Solución: check MARKER solo en output post-último === ITERATION
- Verificado: 4 corridas sin flakes

**commit_msg_hooks_path.txt:** fix: git hooks no ven ruff/vulture/bandit/semgrep
- git hooks usan PATH mínimo sin .venv/bin
- Solución: cargar PATH completo en hook o usar rutas absolutas

**commit_msg_ratchet.txt:** chore: sube piso del core ratchet 5000→6000
- ✅ YA APLICADO

**commit_msg_vault_docs.txt:** docs: documentar god_nodes
- ✅ YA DOCUMENTADO en docs/architecture/CORE_UTILS_TOOLING_VAULT.md

### VibeCoding_GoldenStandard
**commit_msg_gs.txt:** feat: gs_lint.py archiva y poda soft_warnings
- gs_lint archive → tasks/backlog/
- Root cause: mismo hallazgo cleanup cross-repo

## Auditorías y Análisis (Archivados en /tmp)

- **d3_findings.txt** (68K): análisis de código muerto
- **audit_out.txt** (142K): auditoría integral 2026-07-20
- **antipragma_results.json** (54K): findings anti-pragmatismo
- **decisions_entry.txt** (2.2K): entradas de decisiones

**Todos resumen hallazgos ya catalogados en backlogs o reconciliación de 2026-07-20.**

## Recomendación

1. **Commits 2-5 (Cerberus):** Aplicar tras verificación
2. **Commit 1 (Aequitas):** Revisar si aplica con nuevo sync
3. **Commit 6 (GS):** Revisar alcance (tasks/backlog/)
4. **Auditorías:** Archivar en docs/ de cada repo
5. **/tmp:** Limpiar completamente

