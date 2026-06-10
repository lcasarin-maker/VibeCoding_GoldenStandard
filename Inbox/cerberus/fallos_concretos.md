# Fallos Concretos (Rescued from HISTORICO_PROTOCOLO)

1. **D7 Code Completeness** está documentado, pero no implementado. `rg D7` solo aparece en historial, no en scripts.
2. **scripts/audit_6d.py:88** valida que `SPEC.md` tenga una sección, no que el proyecto cumpla esa especificación.
3. **scripts/audit_6d.py:102** valida docstrings y cantidad de documentación, no que las funciones estén conectadas, usadas o correctas.
4. **scripts/audit_6d.py:164** valida manejo de errores buscando el texto "try". Un archivo grande con un try inútil pasa.
5. **scripts/audit_6d_expanded.py:89** ejecuta tests del protocolo, pero no exige tests específicos del proyecto auditado ni prueba startup real.
6. **scripts/audit_6d_expanded.py:125** solo exige validación humana si hay archivos UI cambiados. Si una UI ya rota no cambió en este commit, pasa.
7. **scripts/empirical_proof_checker.py:98** acepta evidencia JSON reciente, pero no valida que screenshot/log exista, corresponda al código actual o pruebe el flujo.
8. **scripts/chunking_validator.py:67** protege contra truncamiento, pero no contra “archivo lleno pero funcionalmente muerto”.
9. **Los tests en tests/** tienen demasiados `assertIn(...)`: validan que existan textos como “MANDATO S1”, no que esos mandatos se ejecuten.
10. **python scripts/audit_6d.py --project-path .** falla porque el script no soporta `--project-path`; lo interpreta como carpeta. Eso es un bug de interfaz que puede confundir agentes.
