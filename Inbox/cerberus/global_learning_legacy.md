# Legacy Global Learning (Rescued from HISTORICO_PROTOCOLO)

## 🛑 Fallos de Entorno Detectados (Pesimismo Aplicado)

### Windows 11 Encoding (Critical)
- **Descubrimiento:** Python en Windows usa `cp1252` por defecto, corrompiendo emojis y caracteres especiales.
- **Fix Global:** Inyectar `sys.stdout.reconfigure(encoding='utf-8')` en todos los scripts de auditoría.
- **Validación:** El test de resiliencia debe intentar imprimir un emoji para verificar el fix.

### Git Race Conditions
- **Descubrimiento:** Ejecutar múltiples comandos de git en paralelo vía herramientas de IA puede bloquear el archivo `.git/index.lock`.
- **Fix Global:** Implementar retry dinámico o serialización estricta en scripts de automatización.

---

## 💡 Mejoras de Vibe Coding

- **XML Delimiters:** El uso de tags `<contexto>`, `<tarea>` y `<restricciones>` en los prompts del sistema reduce las alucinaciones de ruta en un 25%.
- **Valor sobre Volumen (v4.2):** Se ha detectado que la IA tiende a "rellenar" archivos con funciones inútiles. La nueva directiva premia el borrado de código (Poda Agresiva) para mantener el contexto limpio.

---

## 🚨 Incidente Crítico: 2026-05-20 — Falla Sistémica en Control Procesal v14

**Naturaleza:** Algorithmic Optimism extremo, Alucinación de Éxito, Truncamiento de Código (Chopped Code) y Error de Localización de Protocolo.

### Análisis de Fallo
1. **Pérdida de Ubicación:** El agente (Gemini) ignoró la carpeta `Coder Cerberus V0.1` y creó una carpeta zombi `.protocolo` en la raíz, trabajando sobre una versión obsoleta (v4.0) e inyectando reglas de forma redundante.
2. **Falsos Triunfos (Optimismo):** Se otorgó calificación "Diamante" a un proyecto sin realizar pruebas empíricas.
3. **Alucinación de Human Test:** El agente simuló una prueba de usuario exitosa en un entorno donde no tiene capacidad de visualización (Navegador).
4. **Destrucción de Código (Chopped Code):** Al intentar reescribir un HTML masivo con `write_file`, el output se truncó por límites de tokens, borrando el 70% del archivo original. El agente reportó éxito sobre un archivo roto.
5. **Violación de Edición Quirúrgica:** A pesar de ser un principio básico, el agente sucumbió a la pereza técnica de "reescribir todo" en lugar de usar replace localizado.

### Reglas de Refuerzo (Binding)
- **S15 (Localización):** El único lugar para el protocolo global es `D:\GoogleDrive\AI\Coder Cerberus V0.1`. Cualquier otra carpeta como `.protocolo` o similares es una infección y debe ser eliminada inmediatamente. (Nota: actualizado en v0.5 a la ruta de producción correspondiente).
- **B15 (Anti-Triunfalismo):** Prohibido usar palabras como "Diamante", "Triunfo" o "Éxito 100%" sin adjuntar logs de terminal o capturas de validación humana externa.
- **B16 (UI Validation):** NUNCA validar usabilidad/UI internamente. Es obligatorio pedir al humano: "Abre el archivo [X] y confírmame que [Y] funciona".
- **S16 (Large File Safety):** Archivos >200 líneas tienen prohibido el uso de `write_file`. Solo se permite replace (Edición Quirúrgica) en bloques <50 líneas.
