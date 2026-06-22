# Cerberus Golden Standard ID Audit Report
Generated: script.py
Total files with stale references: 85
Priority files (active code/tests): 59

## 1. Priority Files (Dimensions, Tests, Scripts, Rules)

### .protocol/rules/rules.yaml
  - `VC-044` -> `PR-031` (line 11): golden_standard_ref: VC-044
  - `VC-049` -> `PR-034` (line 17): golden_standard_ref: VC-049
  - `VC-070` -> `VC-024` (line 22): message: "Se detectó un valor predeterminado inseguro por defecto (verify=False, debug=True, host='0.0.0.0', CORS origins='*' o similar) prohibido por VC-070."
  - `VC-070` -> `VC-024` (line 23): golden_standard_ref: VC-070

### dimensions/d10_tokenomics.py
  - `PI-007` -> `PR-085` (line 143): Match conservador (substring) para no sobre-acusar (PI-007)."""
  - `TK-016` -> `TK-011` (line 3): """D10 Tokenomics & Context Efficiency (Phase 3, Item D6): TK-016 OutputCompressor,
  - `TK-016` -> `TK-011` (line 27): """D10 — Tokenomics & Context Efficiency (TK-016 / TK-029 / TK-030)."""
  - `TK-016` -> `TK-011` (line 38): # TK-016: critical orchestrators must import OutputCompressor
  - `TK-016` -> `TK-011` (line 49): f"D10: TK-016: {rel} sin OutputCompressor — logs grandes sin comprimir."
  - `TK-016` -> `TK-011` (line 164): """D10 — Tokenomics (TK-016/TK-029/TK-030) + huérfanos de árbol de código."""
  - `TK-029` -> `PR-077` (line 4): TK-029 límites de manifiestos, TK-030 scripts espectrales + huérfanos de árbol.
  - `TK-029` -> `PR-077` (line 27): """D10 — Tokenomics & Context Efficiency (TK-016 / TK-029 / TK-030)."""
  - `TK-029` -> `PR-077` (line 51): # TK-029: Trinity of Memory manifest size gates
  - `TK-029` -> `PR-077` (line 60): f"D10: TK-029: {fname} tiene {lines} lineas (limite: {limit}). Riesgo saturacion contexto."
  - `TK-029` -> `PR-077` (line 164): """D10 — Tokenomics (TK-016/TK-029/TK-030) + huérfanos de árbol de código."""
  - `TK-030` -> `PR-078` (line 4): TK-029 límites de manifiestos, TK-030 scripts espectrales + huérfanos de árbol.
  - `TK-030` -> `PR-078` (line 27): """D10 — Tokenomics & Context Efficiency (TK-016 / TK-029 / TK-030)."""
  - `TK-030` -> `PR-078` (line 62): # TK-030: script references in TOKEN_BUDGET.md / AGENT.md must exist on disk
  - `TK-030` -> `PR-078` (line 76): f"D10: TK-030: {doc} referencia '{ref}' pero el archivo no existe (script espectral)."
  - `TK-030` -> `PR-078` (line 138): """TK-030/TK-043 (gobernanza de salida): todo módulo .py del árbol de código debe
  - `TK-030` -> `PR-078` (line 158): f"D10: TK-030: {c.relative_to(self.project_path).as_posix()} l.1 es espectral — "
  - `TK-030` -> `PR-078` (line 164): """D10 — Tokenomics (TK-016/TK-029/TK-030) + huérfanos de árbol de código."""
  - `TK-043` -> `TK-034` (line 138): """TK-030/TK-043 (gobernanza de salida): todo módulo .py del árbol de código debe

### dimensions/d11_dependency.py
  - `VC-118` -> `VC-052` (line 6): se mueve aquí (S19/VC-118, copiado sin puente) y se añade el chequeo REAL de
  - `VC-129` -> `VC-061` (line 172): f"VC-129 Dependencia alucinada detectada: '{name}' no existe en PyPI",

### dimensions/d15_agent_security.py
  - `VC-074` -> `VC-025` (line 5): Validates against VC-074 to VC-083 coding vices derived from NVIDIA SkillSpector.
  - `VC-074` -> `VC-025` (line 27): "VC-074": (
  - `VC-075` -> `PR-049` (line 45): "VC-075": (
  - `VC-076` -> `VC-026` (line 75): "VC-076": (
  - `VC-078` -> `VC-027` (line 149): "VC-078": (
  - `VC-079` -> `VC-028` (line 190): "VC-079": (
  - `VC-080` -> `VC-029` (line 221): "VC-080": (
  - `VC-081` -> `PR-050` (line 274): "VC-081": (
  - `VC-082` -> `VC-030` (line 308): "VC-082": (
  - `VC-083` -> `VC-031` (line 5): Validates against VC-074 to VC-083 coding vices derived from NVIDIA SkillSpector.
  - `VC-083` -> `VC-031` (line 317): "VC-083": (

### dimensions/d1_integrity.py
  - `VC-118` -> `VC-052` (line 243): f"D1: VC-118 Zombie Compat en {py_file.name} l.{idx}: {label}. "

### dimensions/d2_completeness.py
  - `VC-092` -> `VC-035` (line 208): """Verify Phase 0 purge evidence files for external projects (VC-092 & VC-108)."""
  - `VC-108` -> `PR-064` (line 208): """Verify Phase 0 purge evidence files for external projects (VC-092 & VC-108)."""
  - `VC-111` -> `VC-045` (line 4): gitignore justificado (VC-111) + deuda técnica + anti-stub (D7 Code Completeness).
  - `VC-111` -> `VC-045` (line 178): """D2: Exclusión sin auditoría previa (VC-111).
  - `VC-111` -> `VC-045` (line 203): f"D2: VC-111: .gitignore l.{idx} — Regla de exclusión '{stripped}' sin comentario justificativo previo."
  - `VC-111` -> `VC-045` (line 282): # Validar comentarios en gitignore (VC-111)

### dimensions/d4_anti_spaghetti.py
  - `VC-069` -> `VC-023` (line 3): """D4 Anti-Spaghetti (Phase 3, Item D6): fan-in de módulos (god nodes VC-069),
  - `VC-069` -> `VC-023` (line 144): f"D4 VC-069 god-node: '{mod}' importado por {count} módulos — "

### dimensions/d6_anti_slop.py
  - `VC-076` -> `VC-026` (line 5): protocol_engine/dimensions (VC-076), artefactos de workspace e higiene.
  - `VC-076` -> `VC-026` (line 157): f"D6 VC-076: {f.name} l.{node.lineno} la función pública '{node.name}' no tiene anotación de tipo de retorno."
  - `VC-076` -> `VC-026` (line 171): f"D6 VC-076: {f.name} l.{node.lineno} el argumento '{arg.arg}' en la función pública '{node.name}' no tiene anotación de tipo."
  - `VC-087` -> `VC-032` (line 4): ciega, supresión de warnings sin justificar (VC-087), tipado estricto en
  - `VC-087` -> `VC-032` (line 103): # VC-087: Warning normalizado — bloquear supresión global de warnings sin justificación.
  - `VC-087` -> `VC-032` (line 109): f"D6 VC-087: {f.name}:{lineno} suprime warnings sin justificación "
  - `VC-087` -> `VC-032` (line 110): f"(filterwarnings ignore sin comentario). Añade # VC-087-OK: <razón>."

### protocol_engine/internal_graph.py
  - `VC-069` -> `VC-023` (line 3): """protocol_engine/internal_graph.py — Grafo Capa 1 interno de Cerberus (C3, ancla VC-069).

### protocol_engine/knowledge_loader.py
  - `PI-003` -> `PR-081` (line 601): "insight_id": "PI-003",
  - `VC-048` -> `VC-014` (line 136): # C1 (VC-048): caché del blob de auditoría (8 702 líneas) para no re-parsear en cada

### protocol_engine/rules_engine.py
  - `VC-111` -> `VC-045` (line 18): # Adding a check here is the approved change process (P6.1 / VC-111 equivalent).

### scripts/Full_dimensions_audit.py
  - `TK-031` -> `TK-022` (line 401): ".compact_snooze",  # TK-031 session-snooze flag — operational (CC-16)
  - `VC-067` -> `PR-044` (line 937): """Verifica el formato del campo golden_standard_ref de las reglas (VC-067)."""
  - `VC-113` -> `VC-047` (line 7): Entrypoint primario desde P7.1 (VC-113). Soporte multi-lenguaje (PY, HTML, JS, CSS).
  - `VC-113` -> `VC-047` (line 846): """D6 sub-check (VC-113): el N del filename debe igualar el número de
  - `VC-113` -> `VC-047` (line 879): f"{actual} dimensiones distintas (inline + paquete). Ajustar (VC-113)."

### scripts/check_clean_worktree.py
  - `VC-141` -> `VC-073` (line 3): """check_clean_worktree.py — VC-141: detector de "cambios eludidos / commit parcial".
  - `VC-141` -> `VC-073` (line 49): "VC-141: bloquea el commit si tras stagear queda algo eludido en el working "
  - `VC-141` -> `VC-073` (line 57): "[VC-141] escape CERBERUS_ALLOW_PARTIAL=1 — verificación de tree omitida."
  - `VC-141` -> `VC-073` (line 67): print(f"[VC-141] no se pudo leer git status: {result.stderr.strip()}")
  - `VC-141` -> `VC-073` (line 75): "❌ [VC-141] Cambios eludidos: el working tree tiene archivos sin integrar al commit:"

### scripts/check_handoff_freshness.py
  - `VC-140` -> `VC-072` (line 3): """Hook commit-msg (VC-140, norma de continuidad agnóstica): bloquea el commit si
  - `VC-140` -> `VC-072` (line 71): "ℹ️ [HANDOFF VC-140] uso: check_handoff_freshness.py <archivo-mensaje-commit>; "
  - `VC-140` -> `VC-072` (line 85): print(f"✅ [HANDOFF VC-140] {reason}", file=sys.stderr)
  - `VC-140` -> `VC-072` (line 88): f"❌ [HANDOFF VC-140] BLOQUEADO — {reason}.\n"

### scripts/compact_automation_helper.py
  - `TK-031` -> `TK-022` (line 95): """TK-031: Borra .compact_needed — el usuario corrió /compact, liberar bloqueo."""
  - `TK-031` -> `TK-022` (line 108): # TK-031: liberar bloqueo de herramientas — el usuario inició /compact

### scripts/core_utils.py
  - `TK-041` -> `TK-032` (line 19): # SESSION token budget (TK-041): max tokens allowed for the active working session.
  - `VC-039` -> `VC-012` (line 221): GF-5 / VC-039 declared debt: schema defined, not yet wired to any runtime caller.
  - `VC-117` -> `VC-051` (line 285): """VC-117: escritura atómica de estado crítico (JSON). Escribe a un temporal en el

### scripts/discourse_hook.py
  - `TK-031` -> `TK-022` (line 93): f"[TK-031] Auto-prep compact: historial={'OK' if ok_hist else 'FAIL'}, "
  - `TK-031` -> `TK-022` (line 103): herramientas hasta que el usuario corra /compact (TK-031 enforcement real).
  - `TK-031` -> `TK-022` (line 105): # TK-031 session snooze (conscious escape, gitignored): operator paused the
  - `TK-031` -> `TK-022` (line 117): # TK-031 (Deuda #4, 2º eje): el BLOQUEO depende SOLO de tokens. El conteo de
  - `TK-031` -> `TK-022` (line 129): f"\n🚨 [TK-031] COMPACT REQUERIDO — contexto alto: {', '.join(reason)}\n"
  - `TK-031` -> `TK-022` (line 142): f"[TK-031] PRE-AVISO: {nota} — solo informativo; el bloqueo depende de "
  - `TK-031` -> `TK-022` (line 165): # TK-031: detectar contexto alto con datos reales y forzar compact si aplica.
  - `TK-031` -> `TK-022` (line 183): "contexto alto para forzar /compact (TK-031)."

### scripts/foreign_guard_hook.py
  - `TK-031` -> `TK-022` (line 7): `.protocol/freeze_gate.enabled` (opt-in, anti-TK-031); sin marcador es warn-only (exit 0).

### scripts/hooks/commit-msg
  - `VC-140` -> `VC-072` (line 2): # commit-msg hook Coder Cerberus v0.5 — VC-140 norma de continuidad (handoff agnóstico).

### scripts/hooks/pre-commit
  - `VC-141` -> `VC-073` (line 52): # VC-141 (causa raíz): auto-stage de artefactos canónicos que los checks regeneran
  - `VC-141` -> `VC-073` (line 73): # VC-141 (enforcement): detector de "cambios eludidos / commit parcial". Corre AL
  - `VC-141` -> `VC-073` (line 77): echo "❌ [Pre-commit] BLOQUEADO — VC-141: cambios eludidos sin integrar al commit."

### scripts/install_hooks.ps1
  - `VC-140` -> `VC-072` (line 26): # Install hooks versionados (pre-commit + commit-msg VC-140 + pre-push)

### scripts/install_hooks.sh
  - `VC-140` -> `VC-072` (line 14): # Copiar hooks versionados (pre-commit + commit-msg VC-140 + pre-push)

### scripts/internal_graph.py
  - `VC-069` -> `VC-023` (line 3): """internal_graph.py — CLI de Grafo Capa 1 interno de Cerberus (C3, ancla VC-069).

### scripts/lint_protocol_docs.py
  - `PI-020` -> `PR-098` (line 150): """L5: Afirmaciones de estado en SPEC.md sin confidence tag (PI-020).
  - `PI-020` -> `PR-098` (line 167): f"(PI-020). Considerar añadir VERIFIED/INFERRED/ASSUMED progresivamente."
  - `PI-021` -> `PR-099` (line 4): lint_protocol_docs.py — Wiki-Lint semántico (PI-021 / Karpathy LLM Wiki pattern)
  - `VC-118` -> `VC-052` (line 72): or "VC-118" in line_ctx

### scripts/normalize_golden_audit_consumer_contract.py
  - `VC-152` -> `VC-084` (line 6): ``.protocol/metadata/golden_standard_audit.json``. Per VC-152 (canonical-source-first / no sink
  - `VC-152` -> `VC-084` (line 120): # VC-152: the on-disk consumer artifact is a VERBATIM replica of the GS source; normalization

### scripts/pre_edit_guard.py
  - `TK-031` -> `TK-022` (line 128): """TK-031: Bloquear toda herramienta si el contexto superó umbral y /compact no se ha corrido.
  - `TK-031` -> `TK-022` (line 134): # TK-031 session snooze (conscious escape, gitignored runtime flag): the
  - `TK-031` -> `TK-022` (line 143): f"TK-031 COMPACT REQUERIDO — {reason}\n"
  - `VC-118` -> `VC-052` (line 34): ("backward compat", "S19: 'backward compat' — shim prohibido (VC-118)"),
  - `VC-118` -> `VC-052` (line 35): ("compatibility shim", "S19: shim explícito prohibido (VC-118)"),
  - `VC-118` -> `VC-052` (line 36): ("# for now", "S19: placeholder '# for now' prohibido (VC-118)"),
  - `VC-118` -> `VC-052` (line 37): ("# backward", "S19: comentario de compatibilidad prohibido (VC-118)"),
  - `VC-118` -> `VC-052` (line 38): ("new.exists() or old", "S19: ruta alternativa de adopción prohibida (VC-118)"),
  - `VC-118` -> `VC-052` (line 39): ("fallback to old", "S19: fallback al archivo viejo prohibido (VC-118)"),
  - `VC-118` -> `VC-052` (line 40): ("from old import", "S19: importar del módulo viejo prohibido (VC-118)"),

### scripts/precommit_gate.py
  - `VC-141` -> `VC-073` (line 6): debe correr el gate LIGERO (align-check advisory + clean-worktree VC-141) y JAMÁS

### scripts/repair_failing_tests.py
  - `VC-116` -> `VC-050` (line 118): que el pip-install automático (VC-116): el auto-repair derrotaría al gate. Además la lógica
  - `VC-116` -> `VC-050` (line 131): "    derrotaria al auditor - ver VC-116/ASI-02).\n"

### scripts/run_compliance_tests.py
  - `VC-117` -> `VC-051` (line 270): )  # VC-117: escritura atómica de estado crítico

### scripts/run_self_improvement.py
  - `TK-023` -> `TK-016` (line 56): # TK-023/TK-024: el stdout capturado puede ser enorme. Se conserva completo
  - `TK-023` -> `TK-016` (line 58): # (uso real de OutputCompressor — no un import-teatro para pasar TK-023).
  - `TK-024` -> `TK-017` (line 56): # TK-023/TK-024: el stdout capturado puede ser enorme. Se conserva completo

### scripts/sync_binding.py
  - `VC-117` -> `VC-051` (line 154): """Guardar estado actualizado (VC-117: escritura atómica vía temp + os.replace)."""

### scripts/verify_protocol_adoption.py
  - `VC-141` -> `VC-073` (line 99): # VC-141 idempotencia: solo tocar la fecha si el estado de adopción cambió.

### tests/test_b27_fail_fast.py
  - `PI-009` -> `PR-087` (line 80): with_insight = findings_snapshot({}, ["PI-009 WARN->BLOCK"], [])

### tests/test_catalog_circularity_ratchet.py
  - `VC-152` -> `VC-084` (line 53): handle físico de Cerberus vive en `enforcement.cerberus.mechanism`. Por VC-152 la

### tests/test_cerberus_hygiene.py
  - `VC-087` -> `VC-032` (line 1): """Tests for D6 repository hygiene automation and VC-087 warning suppression."""
  - `VC-087` -> `VC-032` (line 77): """VC-087: filterwarnings('ignore') sin comentario justificativo debe fallar D6."""
  - `VC-087` -> `VC-032` (line 83): """VC-087: script con filterwarnings('ignore') sin comentario es detectado."""
  - `VC-087` -> `VC-032` (line 93): vc087_errors = [e for e in errors if "VC-087" in e]
  - `VC-087` -> `VC-032` (line 95): vc087_errors, "Esperaba error VC-087 por filterwarnings sin comentario"
  - `VC-087` -> `VC-032` (line 100): """VC-087: script con filterwarnings('ignore') + comentario es aceptado."""
  - `VC-087` -> `VC-032` (line 106): 'import warnings\nwarnings.filterwarnings("ignore")  # VC-087-OK: ruido de terceros\n',
  - `VC-087` -> `VC-032` (line 110): vc087_errors = [e for e in errors if "VC-087" in e and "ok.py" in e]
  - `VC-087` -> `VC-032` (line 112): vc087_errors, f"No debería haber errores VC-087: {vc087_errors}"
  - `VC-087` -> `VC-032` (line 116): """VC-087: ningún script de Cerberus suprime warnings sin justificación."""
  - `VC-087` -> `VC-032` (line 118): vc087_errors = [e for e in errors if "VC-087" in e]

### tests/test_clean_worktree.py
  - `VC-141` -> `VC-073` (line 1): """Tests del sprint VC-141: idempotencia de hooks + detector de working tree limpio."""
  - `VC-141` -> `VC-073` (line 40): """VC-141 (idempotencia): si el estado de adopción de un proyecto no cambia,

### tests/test_d10_tokenomics.py
  - `TK-016` -> `TK-011` (line 54): assert any("TK-016" in m and "run_compliance_tests.py" in m for m in msgs)
  - `TK-029` -> `PR-077` (line 30): assert any("TK-029: AGENT.md tiene 200 lineas (limite: 150)" in m for m in msgs)
  - `TK-029` -> `PR-077` (line 38): assert not any("TK-029" in m for m in msgs)
  - `TK-030` -> `PR-078` (line 46): assert any("TK-030" in m and "no_existe.py" in m and "espectral" in m for m in msgs)

### tests/test_d11_dependency.py
  - `VC-129` -> `VC-061` (line 96): """Verifica que un error HTTP 404 en la consulta de PyPI se detecte como VC-129."""
  - `VC-129` -> `VC-061` (line 108): assert "VC-129" in f.message

### tests/test_d13_observable_behavior.py
  - `TK-031` -> `TK-022` (line 180): """C4 (TK-031): tras un /compact, mide SOLO el delta posterior al marcador.

### tests/test_d15_agent_security.py
  - `VC-142` -> `VC-074` (line 38): ("VC-142", "ignore all previous instructions", "Prompt Injection detected"),
  - `VC-143` -> `VC-075` (line 40): "VC-143",
  - `VC-144` -> `VC-076` (line 45): "VC-144",
  - `VC-145` -> `VC-077` (line 49): ("VC-145", "permissions: ['*']", "Privilege Escalation detected"),
  - `VC-146` -> `VC-078` (line 51): "VC-146",
  - `VC-147` -> `VC-079` (line 56): "VC-147",
  - `VC-148` -> `VC-080` (line 60): ("VC-148", "subprocess.call(cmd, shell=True)", "Tool Misuse detected"),
  - `VC-149` -> `VC-081` (line 61): ("VC-149", "open(__file__, 'w')", "Rogue Agent behavior detected"),
  - `VC-150` -> `VC-082` (line 63): "VC-150",
  - `VC-151` -> `VC-083` (line 68): "VC-151",

### tests/test_d17_knowledge.py
  - `VC-001` -> `PR-001` (line 47): lambda: {"VC-001": {"validating_mechanism": "DOC_ONLY"}},

### tests/test_d2_completeness.py
  - `VC-078` -> `VC-027` (line 14): """Mecanismo validador canónico GS (VT-001/VT-002/VT-090, VC-078, VC-092, VC-108, VC-111).
  - `VC-092` -> `VC-035` (line 14): """Mecanismo validador canónico GS (VT-001/VT-002/VT-090, VC-078, VC-092, VC-108, VC-111).
  - `VC-108` -> `PR-064` (line 14): """Mecanismo validador canónico GS (VT-001/VT-002/VT-090, VC-078, VC-092, VC-108, VC-111).
  - `VC-111` -> `VC-045` (line 14): """Mecanismo validador canónico GS (VT-001/VT-002/VT-090, VC-078, VC-092, VC-108, VC-111).
  - `VC-111` -> `VC-045` (line 92): assert any("VC-111" in m and "secret_dir/" in m for m in msgs)
  - `VC-111` -> `VC-045` (line 101): assert not any("VC-111" in m for m in msgs)

### tests/test_d4_anti_spaghetti.py
  - `VC-069` -> `VC-023` (line 50): assert any("VC-069 god-node: 'foolib' importado por 8" in m for m in msgs)

### tests/test_d6_anti_slop.py
  - `VC-076` -> `VC-026` (line 12): """Mecanismo validador canónico GS (VC-076 y otros mapeados a audit_d6_anti_slop).
  - `VC-076` -> `VC-026` (line 82): assert any("VC-076" in m and "do_it" in m for m in msgs)
  - `VC-076` -> `VC-026` (line 90): assert not any("VC-076" in m for m in msgs)
  - `VC-087` -> `VC-032` (line 65): assert any("VC-087" in m and "supress.py" in m for m in msgs)
  - `VC-087` -> `VC-032` (line 70): "import warnings\nwarnings.filterwarnings('ignore')  # VC-087-OK: lib ruidosa\n"
  - `VC-087` -> `VC-032` (line 74): assert not any("VC-087" in m for m in msgs)

### tests/test_dead_defs.py
  - `VC-039` -> `VC-012` (line 15): - defs con marca de DEUDA DECLARADA en docstring (GF-/VC-039) — código guardado a propósito
  - `VC-039` -> `VC-012` (line 83): if "GF-" in doc or "VC-039" in doc or "deuda declarada" in doc.lower():
  - `VC-118` -> `VC-052` (line 132): "string-literal). Cablea o elimina (S5/VC-118):\n  " + "\n  ".join(dead),

### tests/test_discourse_hook.py
  - `TK-031` -> `TK-022` (line 68): """TK-031 Deuda #4 (2º eje): 62 msgs / 13K tokens NO escribe sentinel.

### tests/test_federated_graph.py
  - `VC-141` -> `VC-073` (line 114): """VC-141: regenerar el grafo sin cambios de sustancia NO debe reescribir el

### tests/test_federated_linter.py
  - `VC-001` -> `PR-001` (line 98): "id": "VC-001",
  - `VC-002` -> `PR-002` (line 111): {"id": "VC-002", "status": "PREVENTED", "validating_mechanism": "DOC_ONLY"},
  - `VC-003` -> `VC-001` (line 113): "id": "VC-003",
  - `VC-004` -> `PR-003` (line 117): {"id": "VC-004", "status": "PREVENTED", "validating_mechanism": ""},

### tests/test_golden_standard_compliance.py
  - `VC-001` -> `PR-001` (line 56): "VC-001": {
  - `VC-001` -> `PR-001` (line 57): "id": "VC-001",
  - `VC-001` -> `PR-001` (line 92): self.assertEqual(first["VC-001"]["downstream_verification"], "none")
  - `VC-002` -> `PR-002` (line 110): "VC-002": {
  - `VC-002` -> `PR-002` (line 111): "id": "VC-002",
  - `VC-002` -> `PR-002` (line 141): self.assertIn("VC-002", loaded)
  - `VC-002` -> `PR-002` (line 142): self.assertEqual(loaded["VC-002"]["downstream_verification"], "none")
  - `VC-048` -> `VC-014` (line 46): """C1 (VC-048): load_golden_standard_audit memoiza — dos llamadas devuelven el

### tests/test_governance_vices.py
  - `VC-152` -> `VC-084` (line 4): (VC-152/153) and the workflow-wiring vice (VT-105).
  - `VC-152` -> `VC-084` (line 80): # VC-152 — "Canonical source first (no sink patching)": CC's vendored audit DB is
  - `VC-152` -> `VC-084` (line 88): """VC-152: the vendored CC audit DB must equal the GS source exactly — no invented keys, no hand-patches on disk."""
  - `VC-152` -> `VC-084` (line 95): assert cc_only == [], f"VC-152: sink invented keys absent from GS source: {cc_only}"
  - `VC-152` -> `VC-084` (line 100): ), f"VC-152: sink diverges from GS source on disk (must be identical): {drifted}"
  - `VC-153` -> `VC-085` (line 6): Each test is the *consumer* side (VC-153 source-first): the GS catalog owns the
  - `VC-153` -> `VC-085` (line 110): # VC-153 — "Doctrine before enforcement (source-first ordering)": a Cerberus rule
  - `VC-153` -> `VC-085` (line 127): """VC-153: every golden_standard_ref declared by a Cerberus rule must resolve
  - `VC-153` -> `VC-085` (line 136): ), f"VC-153: rules cite non-existent GS doctrine: {unresolved}"

### tests/test_handoff_freshness.py
  - `VC-140` -> `VC-072` (line 3): """Tests falsables del mecanismo de continuidad VC-140.
  - `VC-140` -> `VC-072` (line 42): """VC-140 endurecido: el token [skip-handoff] en el asunto YA NO escapa (eliminado);
  - `VC-140` -> `VC-072` (line 58): Tras el endurecimiento de VC-140 el token tampoco escapa en el asunto; el mensaje

### tests/test_infrastructure.py
  - `VC-108` -> `PR-064` (line 5): P5.4  Si no hay .git/hooks/pre-commit = fail (VT-105/VC-108)
  - `VC-111` -> `VC-045` (line 7): P5.3+P5.7  hard_excludes solo puede contener entradas del conjunto aprobado (VC-111/VT-106)
  - `VC-111` -> `VC-045` (line 184): """P5.3+P5.7: hard_excludes solo puede tener entradas del conjunto aprobado (VC-111/VT-106).
  - `VC-113` -> `VC-047` (line 6): P5.5  Centinela de dominios: Full_dimensions_audit debe tener exactamente 15 dominios gate (VC-113/VT-108)
  - `VC-113` -> `VC-047` (line 108): """P7.1: Full_dimensions_audit.py debe existir como único entrypoint del auditor (VC-113)."""

### tests/test_internal_graph.py
  - `VC-069` -> `VC-023` (line 3): """Tests falsables del derivador Capa 1 (C3, ancla VC-069).

### tests/test_lint_knowledge.py
  - `TK-038` -> `TK-029` (line 142): "id": "TK-038",
  - `TK-038` -> `TK-029` (line 151): "alias_of": "TK-038",
  - `TK-042` -> `TK-033` (line 149): "id": "TK-042",
  - `TK-042` -> `TK-033` (line 162): assert not any("TK-042" in err for err in errors)
  - `VC-111` -> `VC-045` (line 42): "id": "VC-111",
  - `VC-111` -> `VC-045` (line 73): "id": "VC-111",
  - `VC-111` -> `VC-045` (line 84): "id": "VC-111",
  - `VC-111` -> `VC-045` (line 104): "Duplicate ID found across Golden Standard: 'VC-111'" in err
  - `VC-111` -> `VC-045` (line 196): # Create Home page, VC-111 note and VC-112 note
  - `VC-111` -> `VC-045` (line 198): "Welcome to [[VC-111]] and [[VC-112]]", encoding="utf-8"
  - `VC-111` -> `VC-045` (line 200): (wiki_dir / "VC-111.md").write_text(
  - `VC-111` -> `VC-045` (line 201): "This is VC-111 linking back to [[Home]]", encoding="utf-8"
  - `VC-111` -> `VC-045` (line 204): "This is VC-112 linking to [VC-111](VC-111.md)", encoding="utf-8"
  - `VC-111` -> `VC-045` (line 204): "This is VC-112 linking to [VC-111](VC-111.md)", encoding="utf-8"
  - `VC-111` -> `VC-045` (line 239): # Home links to VC-111, but VC-112 is orphan (no incoming links)
  - `VC-111` -> `VC-045` (line 240): (wiki_dir / "Home.md").write_text("Link to [[VC-111]]", encoding="utf-8")
  - `VC-111` -> `VC-045` (line 241): (wiki_dir / "VC-111.md").write_text("Content", encoding="utf-8")
  - `VC-112` -> `VC-046` (line 49): "id": "VC-112",
  - `VC-112` -> `VC-046` (line 196): # Create Home page, VC-111 note and VC-112 note
  - `VC-112` -> `VC-046` (line 198): "Welcome to [[VC-111]] and [[VC-112]]", encoding="utf-8"
  - `VC-112` -> `VC-046` (line 203): (wiki_dir / "VC-112.md").write_text(
  - `VC-112` -> `VC-046` (line 204): "This is VC-112 linking to [VC-111](VC-111.md)", encoding="utf-8"
  - `VC-112` -> `VC-046` (line 239): # Home links to VC-111, but VC-112 is orphan (no incoming links)
  - `VC-112` -> `VC-046` (line 242): (wiki_dir / "VC-112.md").write_text("Content", encoding="utf-8")
  - `VC-112` -> `VC-046` (line 245): assert "VC-112.md" in orphans
  - `VC-112` -> `VC-046` (line 246): assert any("Orphaned note found: 'VC-112.md'" in err for err in errors)
  - `VC-123` -> `VC-055` (line 112): # VC-ABC instead of VC-123

### tests/test_portability.py
  - `PI-012` -> `PR-090` (line 162): {"id": "D6_test3", "domain": "D6", "golden_standard_ref": "PI-012"},
  - `VC-067` -> `PR-044` (line 160): {"id": "D6_test1", "domain": "D6", "golden_standard_ref": "VC-067"},
  - `VC-111` -> `VC-045` (line 100): fallen la auditoría D2 (VC-111).
  - `VC-111` -> `VC-045` (line 113): "VC-111" in err and "secret_dir/" in err for err in errors
  - `VC-111` -> `VC-045` (line 116): "VC-111" in err and "temp_file.txt" in err for err in errors
  - `VC-111` -> `VC-045` (line 130): "VC-111" in err for err in errors_valid
  - `VC-115` -> `VC-049` (line 161): {"id": "D6_test2", "domain": "D6", "golden_standard_ref": "PENDING:VC-115"},
  - `VC-138` -> `VC-070` (line 265): "golden_standard_ref": "VC-138",

### tests/test_project_insights_integration.py
  - `PI-003` -> `PR-081` (line 64): any(item["insight_id"] == "PI-003" for item in recommendations["D10"])

### tests/test_sprint3_4_giants.py
  - `TK-018` -> `TK-012` (line 22): TK-018 → test_tk018_external_backlog_exists
  - `TK-018` -> `TK-012` (line 206): # ── TK-018: backlog externalizado (no acumular side-quests en el contexto) ────
  - `TK-018` -> `TK-012` (line 212): """TK-018: el backlog/side-quests vive fuera del contexto (review_queue.json), no en prosa.
  - `TK-018` -> `TK-012` (line 227): ), "TK-018: el repo no tiene .protocol/review_queue.json"
  - `VC-082` -> `VC-030` (line 19): VC-082 → test_vc082_ghost_import_detected            VC-109 → test_vc109_absolute_path_in_scripts
  - `VC-082` -> `VC-030` (line 40): # ── VC-082: ghost import (paquete usado pero no declarado en el manifiesto) ───
  - `VC-082` -> `VC-030` (line 71): """VC-082: dependencia importada pero no declarada (ghost import / supply-chain drift)."""
  - `VC-109` -> `VC-043` (line 19): VC-082 → test_vc082_ghost_import_detected            VC-109 → test_vc109_absolute_path_in_scripts
  - `VC-109` -> `VC-043` (line 83): # ── VC-109: rutas absolutas hardcodeadas (acoplamiento de máquina) ───────────
  - `VC-109` -> `VC-043` (line 92): """VC-109: ruta absoluta hardcodeada (acoplamiento de máquina) → no portable.
  - `VC-121` -> `VC-053` (line 20): VC-121 → test_vc121_duplicate_function_names         VC-122 → test_vc122_no_pip_install_in_scripts
  - `VC-121` -> `VC-053` (line 104): # ── VC-121: nombres de función top-level duplicados entre módulos distintos ───
  - `VC-121` -> `VC-053` (line 116): """VC-121: misma función top-level definida en dos módulos (colisión de nomenclatura/copy-paste)."""
  - `VC-122` -> `VC-054` (line 20): VC-121 → test_vc121_duplicate_function_names         VC-122 → test_vc122_no_pip_install_in_scripts
  - `VC-122` -> `VC-054` (line 128): # ── VC-122 / VC-123: invocaciones peligrosas en scripts (pip install / git add -A) ──
  - `VC-122` -> `VC-054` (line 147): """VC-122: `pip install` automático por subprocess en scripts/ (supply-chain). Failing-first
  - `VC-122` -> `VC-054` (line 164): ), f"VC-122: pip install por subprocess en scripts/: {offenders}"
  - `VC-123` -> `VC-055` (line 21): VC-123 → test_vc123_no_git_add_all_in_scripts        TK-005 → test_tk005_status_md_has_required_sections
  - `VC-123` -> `VC-055` (line 128): # ── VC-122 / VC-123: invocaciones peligrosas en scripts (pip install / git add -A) ──
  - `VC-123` -> `VC-055` (line 168): """VC-123: `git add -A` / `git add .` (staging indiscriminado) por el agente en su flujo de

### tests/test_sprint3_security.py
  - `VC-049` -> `PR-034` (line 7): - VC-049: ejecución dinámica de reglas externas (eval/RCE) → rules_engine debe RECHAZAR
  - `VC-049` -> `PR-034` (line 24): # ── VC-049: RCE por eval de reglas externas ──────────────────────────────────
  - `VC-049` -> `PR-034` (line 26): """VC-049: una regla externa con un `check` arbitrario (payload) NO debe ejecutarse;
  - `VC-049` -> `PR-034` (line 90): VC-049/050/051 debe RESOLVER a un script/símbolo real vía el resolvedor federado.
  - `VC-049` -> `PR-034` (line 106): for vid in ("VC-049", "VC-050", "VC-051"):
  - `VC-050` -> `PR-035` (line 9): - VC-050: pip install automático ante ImportError → import_error_guard NO debe instalar.
  - `VC-050` -> `PR-035` (line 46): # ── VC-050: pip install automático prohibido ─────────────────────────────────
  - `VC-050` -> `PR-035` (line 48): """VC-050: ante un ImportError, import_error_guard debe REPORTAR (return False) y NUNCA
  - `VC-050` -> `PR-035` (line 106): for vid in ("VC-049", "VC-050", "VC-051"):
  - `VC-051` -> `PR-036` (line 10): - VC-051: escritura no-atómica de estado crítico → debe existir y usarse escritura atómica.
  - `VC-051` -> `PR-036` (line 72): # ── VC-051: escritura atómica de estado crítico ──────────────────────────────
  - `VC-051` -> `PR-036` (line 74): """VC-051: debe existir un helper de escritura atómica (temp + os.replace) para que
  - `VC-051` -> `PR-036` (line 106): for vid in ("VC-049", "VC-050", "VC-051"):
  - `VC-152` -> `VC-084` (line 94): (VC-152: la copia on-disk es verbatim de GS). CC-C4 (endurecer el sitio hermano): se

### tests/test_sprint5_warn_to_block.py
  - `PI-009` -> `PR-087` (line 1): """Sprint 5 — WARN→BLOCK (PI-009).
  - `TK-030` -> `PR-078` (line 56): # zombie: script en scripts/ no wired a ningún hook/doc/CLI → D1 Zombi + D10 TK-030

## 2. Documentation & Protocol Files

### .agents/AGENTS.md
  - `VC-118` -> `VC-052` (line 141)
  - `VC-118` -> `VC-052` (line 155)
  - `VC-118` -> `VC-052` (line 173)

### .agents/CODEX.md
  - `VC-118` -> `VC-052` (line 150)
  - `VC-118` -> `VC-052` (line 164)
  - `VC-118` -> `VC-052` (line 182)

### .agents/PROTOCOL_BEHAVIOR.md
  - `VC-121` -> `VC-053` (line 14)

### .agents/PROTOCOL_SYSTEM.md
  - `VC-118` -> `VC-052` (line 209)
  - `VC-119` -> `PR-065` (line 213)
  - `VC-124` -> `VC-056` (line 139)

### .claude/CLAUDE.md
  - `VC-118` -> `VC-052` (line 141)
  - `VC-118` -> `VC-052` (line 155)
  - `VC-118` -> `VC-052` (line 173)

### .claude/settings.local.json
  - `TK-016` -> `TK-011` (line 834)
  - `TK-016` -> `TK-011` (line 835)
  - `TK-016` -> `TK-011` (line 838)
  - `TK-016` -> `TK-011` (line 838)
  - `TK-034` -> `TK-025` (line 278)
  ... and 7 more references

### .protocol/metadata/circularity_baseline.json
  - `VC-003` -> `VC-001` (line 8)
  - `VC-031` -> `VC-009` (line 8)
  - `VC-062` -> `VC-019` (line 8)

### .protocol/metadata/golden_standard_audit.json
  - `TK-009` -> `PR-070` (line 283)
  - `TK-009` -> `PR-070` (line 284)
  - `TK-010` -> `PR-071` (line 318)
  - `TK-010` -> `PR-071` (line 319)
  - `TK-011` -> `PR-072` (line 353)
  ... and 224 more references

### AGENT.md
  - `VC-114` -> `VC-048` (line 116)
  - `VC-118` -> `VC-052` (line 41)

### AUDIT_TRAIL.md
  - `PI-001` -> `PR-079` (line 2487)
  - `PI-034` -> `PR-112` (line 2487)
  - `TK-023` -> `TK-016` (line 1712)
  - `TK-031` -> `TK-022` (line 70)
  - `TK-031` -> `TK-022` (line 1582)
  ... and 79 more references

### BACKLOG.md
  - `TK-042` -> `TK-033` (line 51)

### DEPRECATION_LOG.md
  - `PI-001` -> `PR-079` (line 78)
  - `PI-034` -> `PR-112` (line 78)
  - `VC-118` -> `VC-052` (line 60)

### HANDOFF.md
  - `VC-152` -> `VC-084` (line 20)

### PLAN.md
  - `PI-009` -> `PR-087` (line 517)
  - `PI-015` -> `PR-093` (line 521)
  - `PI-018` -> `PR-096` (line 521)
  - `VC-069` -> `VC-023` (line 648)
  - `VC-115` -> `VC-049` (line 133)
  ... and 7 more references

### SPEC.md
  - `PI-020` -> `PR-098` (line 222)
  - `PI-020` -> `PR-098` (line 367)
  - `PI-021` -> `PR-099` (line 221)
  - `TK-016` -> `TK-011` (line 200)
  - `TK-029` -> `PR-077` (line 200)
  ... and 30 more references

### STATUS.md
  - `PI-015` -> `PR-093` (line 42)
  - `PI-018` -> `PR-096` (line 42)
  - `VC-142` -> `VC-074` (line 77)
  - `VC-151` -> `VC-083` (line 77)

### docs/CHECKLIST.md
  - `VC-114` -> `VC-048` (line 40)

### docs/HANDOFF.md
  - `PI-001` -> `PR-079` (line 57)
  - `PI-003` -> `PR-081` (line 57)
  - `PI-003` -> `PR-081` (line 65)
  - `PI-009` -> `PR-087` (line 57)
  - `PI-014` -> `PR-092` (line 57)
  ... and 31 more references

### docs/HANDOFF.template.md
  - `VC-140` -> `VC-072` (line 3)

### docs/MANDATES_BY_PHASE.md
  - `VC-121` -> `VC-053` (line 183)
  - `VC-121` -> `VC-053` (line 196)

### project_insights/.archive/PI-003_tokencost_archived.md
  - `PI-003` -> `PR-081` (line 1)

### project_insights/PI-promotion.yaml
  - `VC-009` -> `PR-007` (line 15)
  - `VC-009` -> `PR-007` (line 15)
  - `VC-015` -> `PR-013` (line 17)
  - `VC-017` -> `VC-004` (line 17)
  - `VC-118` -> `VC-052` (line 20)
  ... and 2 more references

### project_insights/analysis/PI-009_analysis.md
  - `PI-009` -> `PR-087` (line 1)
  - `PI-009` -> `PR-087` (line 60)
  - `PI-014` -> `PR-092` (line 66)
  - `PI-016` -> `PR-094` (line 67)
  - `VC-001` -> `PR-001` (line 68)
  ... and 1 more references

### project_insights/raw/PI-009_debt_zero.md
  - `PI-009` -> `PR-087` (line 1)
  - `VC-009` -> `PR-007` (line 41)

### skills/cerberus/SKILL.md
  - `VC-114` -> `VC-048` (line 126)
  - `VC-118` -> `VC-052` (line 51)
  - `VC-118` -> `VC-052` (line 339)
  - `VC-119` -> `PR-065` (line 343)
  - `VC-124` -> `VC-056` (line 269)

### tests/conftest.py
  - `VC-141` -> `VC-073` (line 14)