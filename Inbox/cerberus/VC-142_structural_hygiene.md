# Proposal: VC-142 — Repositorio con código vigilado y estructura salvaje

- **ID:** VC-142
- **Title:** Repositorio con código vigilado y estructura salvaje
- **Severity:** high
- **Status:** DOC_ONLY
- **Tags:** ["hygiene", "structure", "observability"]
- **Downstream Verification:** required
- **Validating Mechanism:** audit_d1_integrity

## Sintoma
El proyecto gatea cada línea de código (hooks, tests, auditores) pero nada vigila la *estructura* del repo: archivos muertos se acumulan sin respaldo, READMEs afirman números que el CI no valida, documentos normativos se duplican y derivan, y los directorios de archivo crecen fuera de control. El síntoma típico es descubrir, meses después, que el "archivo histórico" nunca estuvo en git (por ejemplo, descubrir 298/422 archivos de deprecated/ locales fuera de git).

## Causa
Falta de un scanner o validador estático a nivel de sistema de archivos / metadata y falta de un acoplamiento entre la prosa descriptiva de estado (README) y el estado físico de los artefactos.

## Solución
Implementar un chequeador estático en D1 (u otro validador estático del core) que analice la higiene del árbol de archivos: detecte directorios gitignorados con archivos activos, claims de conteo en README desalineados con el catálogo físico, y duplicación de nombres de archivo clave.

## Criterios de Detección
1. Directorio presente en disco Y en `.gitignore` con >N archivos (archivo muerto sin respaldo).
2. Claim numérico en README (`\b\d{2,4}\b entries|tests|vices`) sin mecanismo que lo derive/valide.
3. Basenames normativos duplicados (`*.md` raíz vs `docs/`) con hash divergente.
4. Más de un directorio con semántica de archivo (`archive/`, `deprecated/`, `*_legacy/` en raíz).

## Acción
Crear un scan en D1 para auditar la estructura de archivos y asegurar que la prosa del README se mantenga sincronizada con la base de datos física.
