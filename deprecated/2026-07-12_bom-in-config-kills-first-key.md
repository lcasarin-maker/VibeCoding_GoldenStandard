---
# Manual Finding — BOM in config files silently kills the first key
---

## Metadata

source: manual
author: Luis Casarin (vía Claude, sesión Fase 0 Aequitas)
date_detected: 2026-07-12
session_context: "Migración de secretos de Aequitas OS a D:\AI\.secrets (Fase 0.3): tras mover backend/.env, Settings() cargaba con SECRET_KEY vacío"

## Classification

proposed_domain: VC
proposed_severity: high
tags:
  - configuration
  - encoding
  - silent-failure
refinement_target:
evidence_for:

---

## Finding

### Symptom
Un archivo .env que funcionaba dejó de cargar EXACTAMENTE su primera variable
(AEQUITAS_SECRET_KEY) tras moverse de ubicación. Ningún error, ninguna
advertencia: pydantic-settings simplemente no encontró la clave y aplicó el
default vacío. El resto de las variables cargaba bien, lo que hizo el
diagnóstico engañoso (parecía un problema de alias o de ruta).

### Cause
El archivo llevaba un BOM UTF-8 (EF BB BF) al inicio — invisible en cualquier
editor. Los parsers de dotenv leen la primera línea como "﻿AEQUITAS_SECRET_KEY"
en vez de "AEQUITAS_SECRET_KEY": la clave con BOM pegado no matchea nada.
El BOM lo introducen editores/herramientas Windows (Notepad, algunos Set-Content
de PowerShell 5.1) al guardar como "UTF-8". Es un fallo de la clase
"configuración optimista": el sistema asume que el archivo de config es lo que
aparenta, y el fallo se materializa lejos del origen (la variable llega vacía
en runtime, no al parsear).

### Example
```
$ xxd .env | head -1
00000000: efbb bf41 4551 5549 5441 535f 5345 4352  ...AEQUITAS_SECR
# pydantic-settings: Settings().SECRET_KEY == ""  (sin error alguno)
```

### Detección propuesta (falseable — clase: estatico)
Regla trivial por archivo de config (.env, .yaml, .yml, .json, .toml, .ini):
los primeros 3 bytes NO deben ser EF BB BF. Fixture positivo: archivo con BOM.
Fixture negativo: mismo contenido sin BOM. Implementable en Semgrep (o check
de 5 líneas en pre-commit / PreToolUse de Cerberus — encaja en CC-HOOK-001
como sexto detector barato, y en el pipeline rule-first de GS-RAC-001).

### Mitigación
1. Gate estático: rechazar BOM en archivos de configuración al commit/write.
2. Al escribir configs desde PowerShell: usar New-Object Text.UTF8Encoding($false)
   o Set-Content -Encoding utf8NoBOM (PS7), nunca el "UTF8" default de PS 5.1.
3. Los loaders críticos (secretos) deberían validar que las claves esperadas
   existan tras la carga y FALLAR ruidosamente si la primera clave del archivo
   no aparece (defensa en profundidad contra esta clase completa).

## Resolution
Promoted to: VC-094 (golden_standard_coding_vices.yaml)
Wiki article: Wiki/Vices/VC-094.md
Date promoted: 2026-07-13
Curator: Claude (Sonnet 5), sesion autonoma nocturna
