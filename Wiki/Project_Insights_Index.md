# Índice de Insights Satélite

Mapeo de lecciones extraídas de repositorios de referencia y herramientas de auditoría externa.
Las entradas se agrupan por tipo para distinguir principios accionables de meta-comentario del sistema.

---

## 🟢 Principios accionables

_Lecciones transversales que cambian cómo se trabaja._ (17)

*   [[Project_Insights/PI-008|PI-008]] — Batch de autorizaciones previsibles – agrupar permisos, aclaraciones y decisiones antes de una corrida larga para evitar interrupciones, relecturas y trabajo reactivo.
*   [[Project_Insights/PI-009|PI-009]] — Deuda cero antes de avanzar – todo warning o hallazgo no bloqueante se trata como error operativo hasta que se corrija o se bloquee explícitamente. [IMPLEMENTED Sprint 5: [RECOMENDACIONES POR DOMINIO] suprimida de gate APPROVED (ruido no bloqueante); solo aparece cuando hay FAILs de dominio para guiar el fix. Test failing-first valida ambas ramas. Refactor _print_recommendations (C901 compliance).]
*   [[Project_Insights/PI-010|PI-010]] — Higiene de salida y raíz limpia – los artefactos históricos son referencia, no fuente de verdad; al cerrar auditoría la raíz debe quedar libre de residuo operativo.
*   [[Project_Insights/PI-011|PI-011]] — Nombres descriptivos y topología simple – preferir scripts y módulos que expliquen su propósito y aplanar estructura cuando reduzca fricción cognitiva.
*   [[Project_Insights/PI-012|PI-012]] — Exclusiones mínimas y reales – whitelists, excludes, skips, xfails, stubs, mocks y placeholders solo con causa verificable; la cobertura falsa es deuda, no avance.
*   [[Project_Insights/PI-013|PI-013]] — Vigilancia en tiempo real – observar señales, costes y desvíos durante la ejecución, no solo en el post-mortem.
*   [[Project_Insights/PI-015|PI-015]] — Ratchet de circularidad – cada nuevo vicio debe romper una relación circular real y drenar el baseline por lotes; una cobertura que no reduce el círculo sigue siendo teatro.
*   [[Project_Insights/PI-016|PI-016]] — Honestidad DOC_ONLY – si una lección no es falsable por una compuerta física, debe etiquetarse como DOC_ONLY en vez de simular cobertura automática.
*   [[Project_Insights/PI-017|PI-017]] — Anti-cobertura many-to-one – un test que pretende cubrir N vicios a la vez pierde discriminación; cada guardia debe aislar el fallo que dice proteger.
*   [[Project_Insights/PI-019|PI-019]] — Higiene de ejecución y tooling – preferir comandos simples, ediciones declarativas, UTF-8, evidencia auditable y permisos elevados solo como excepción; los helpers temporales deben desaparecer salvo que sean reutilizables y documentados.
*   [[Project_Insights/PI-022|PI-022]] — Lista de incertidumbre operativa – cada sesión o documento de protocolo debe declarar qué subsistemas, rutas o afirmaciones no fueron verificados mecánicamente en ese turno. La ausencia de lista equivale a verificación incompleta. Origen: Cerberus B12 / B25 y control de anti-alucinación.
*   [[Project_Insights/PI-023|PI-023]] — Conciencia de sesión dual – antes de tocar fuentes compartidas, el agente debe verificar estado y últimos commits para no pisar trabajo concurrente. Si hay cambios ajenos, se analiza impacto antes de editar. Origen: Cerberus S21 / B15 / disciplina de coexistencia multiagente.
*   [[Project_Insights/PI-024|PI-024]] — Revisión basada en hubs – los nodos con mayor fan-in o grado de impacto deben revisarse primero cuando cambia un catálogo o índice. El grafo no es decorativo: prioriza riesgo y ordena la auditoría. Origen: Cerberus graph report y heurística de hub-first review.
*   [[Project_Insights/PI-025|PI-025]] — Retrospectiva exportable – cada sesión debe cerrar con una retrospectiva estructurada y parseable que se persista en un ledger durable antes de COMPACT/CLEAR. El chat no es memoria confiable y el conocimiento nuevo debe sobrevivir al reset de contexto. Origen: Cerberus export_retrospective.py y la disciplina de HISTORIAL como fuente de continuidad.
*   [[Project_Insights/PI-026|PI-026]] — Preflight exhaustivo y no reabrir alcance post-ejecución – antes de ejecutar cualquier cambio, el agente debe declarar scope, impactos previsibles, follow-ups fuera de alcance y el runner/loader que se vería afectado si la topología cambia. Si después de ejecutar surge una mejora nueva, se registra primero en backlog; no se ofrece como sugerencia post-ejecución. Origen: Cerberus / GS execution hygiene y la separación formal de auditorías entre conocimiento y consumo.
*   [[Project_Insights/PI-027|PI-027]] — Serialización de operaciones Git – los comandos Git deben ejecutarse de forma serializada dentro de automatizaciones y orquestadores para evitar bloqueos de índice, carreras de estado y resultados inconsistentes. Cuando exista coordinación o tooling concurrente, la disciplina segura es un único flujo Git a la vez con reintentos controlados, no paralelismo oportunista. Origen: Cerberus global learning sobre race conditions y bloqueo de .git/index.lock.
*   [[Project_Insights/PI-035|PI-035]] — Auditoría de sistemas estocásticos – cuando el comportamiento depende de azar, sampling, retries, routing probabilista o generación no determinista, no se evalúa con una sola corrida ni con un valor exacto. La regla es declarar distribución objetivo, semilla cuando aplique, tamaño de muestra, umbrales aceptables y criterio de repetición; si la superficie debería ser determinista, la aleatoriedad se elimina en vez de disfrazarla como controlada. Las afirmaciones sobre estabilidad o corrección deben ser reproducibles en varias ejecuciones, no solo plausibles en una. Origen: GS audit of stochastic systems; complementa VT-028 sobre aleatoriedad controlada.

---

## 🔧 Herramientas y técnicas de referencia

_Punteros a herramientas externas verificadas y patrones reutilizables._ (14)

*   [[Project_Insights/PI-001|PI-001]] — Deptry – reconciliación de imports contra dependencias declaradas para detectar faltantes, no usadas, transitivas, dev mal ubicadas y stdlib declaradas como dependencias.
*   [[Project_Insights/PI-002|PI-002]] — Aserciones diagnósticas – cuando un test falla, el mensaje debe explicar la discrepancia con claridad accionable. Tools reales verificados: assertion rewriting nativo de pytest, pytest-clarity / pytest-icdiff para diffs legibles, flake8-assertive para métodos de aserción correctos. (Corrige una referencia previa a un paquete inexistente — ver VC-129 dependencia alucinada.)
*   [[Project_Insights/PI-003|PI-003]] — Tokencost – metering previo de tokens y conversión a USD para hacer visible el gasto antes de ejecutar una llamada LLM. [REMEDIATED Sprint 5: track_tokens.py cableado al gate D10; visualidad confirma.]
*   [[Project_Insights/PI-004|PI-004]] — Trivy – escaneo multi-superficie (imágenes, filesystem, git, VMs, Kubernetes) para CVEs, secretos, misconfiguraciones, SBOM y licencias.
*   [[Project_Insights/PI-005|PI-005]] — Litellm – gateway agnóstico de proveedor con routing, fallback, cost tracking, guardrails, logging y load balancing. [NOT_APPLICABLE Sprint 10: análisis de 36 repos externos mostró que LiteLLM es útil como referencia arquitectónica pero la capa de abstracción de proveedor ya está cubierta por Cerberus gates; integración declarativa, no ejecutable.]
*   [[Project_Insights/PI-020|PI-020]] — Confidence Tags (Graphify pattern) – toda afirmación de estado en documentos de protocolo debe llevar nivel de confianza explícito: VERIFIED (respaldado por log de terminal o test), INFERRED (deducido de evidencia indirecta), ASSUMED (sin evidencia, supuesto razonable). Afirmaciones sin tag se tratan como ASSUMED. Aplica especialmente a SPEC.md, HISTORIAL.md y comentarios de decisiones arquitectónicas. Origen: safishamsi/graphify confidence tag system para knowledge graphs.
*   [[Project_Insights/PI-021|PI-021]] — Wiki-Lint semántico (Karpathy LLM Wiki pattern) – los documentos de protocolo deben auditarse periódicamente para detectar: contradicciones entre secciones, referencias a archivos inexistentes, mandatos mencionados en un doc pero ausentes en otro, y afirmaciones de versión inconsistentes. El Lint no es sintáctico (eso lo hace sync_binding.py) sino semántico: ¿dos documentos afirman cosas incompatibles sobre el mismo estado? Origen: gist Karpathy LLM Wiki, operación Lint del framework de wiki mantenida por agente.
*   [[Project_Insights/PI-028|PI-028]] — Vibe Check (PV-Bhat/vibe-check-mcp-server, verificado) – servidor MCP de metacognicion que frena tunnel-vision y runaway loops de agentes mediante Chain-Pattern Interrupts; implementacion directa de la mitigacion de VC-120.
*   [[Project_Insights/PI-029|PI-029]] — vibecheck (yuvrajangadsingh/vibecheck, verificado) – ESLint para AI slop: linter local que detecta code smells de codigo generado por IA (secretos hardcodeados, eval, catch vacio); evidencia de que los vicios del catalogo son detectables estaticamente.
*   [[Project_Insights/PI-030|PI-030]] — viberails (refractionPOINT/viberails, verificado) – AI Firewall que intercepta operaciones riesgosas de agentes (Claude Code, Cursor, Gemini CLI) via hooks; capa de enforcement comparable conceptualmente a Cerberus (sin relacion con el homonimo philips-software/cerberus).
*   [[Project_Insights/PI-031|PI-031]] — ratelimit (tomasbasham/ratelimit, verificado) – decorador de rate limiting (@limits + sleep_and_retry) como control concreto contra VC-110 (cuota como sorpresa) y la deuda de tokenomics (TK-044).
*   [[Project_Insights/PI-032|PI-032]] — context7 (upstash/context7, verificado) -- entrega a los LLMs documentacion de codigo up-to-date para evitar llamadas a APIs obsoletas o inexistentes; mitigacion directa de VC-135.
*   [[Project_Insights/PI-033|PI-033]] — Capa de memoria persistente (byterover-cli / zilliztech claude-context-memsearch, verificados) -- memoria durable entre sesiones para agentes; su disciplina (fuente, fecha, reconciliacion) mitiga VC-136.
*   [[Project_Insights/PI-034|PI-034]] — serena (oraios/serena, verificado) -- retrieval y edicion a nivel de simbolo (semantico) para que el contexto recuperado sea correcto; mitiga VC-137 frente al chunking ciego.

---

## ⚪ Meta-sistema (sobre el propio Golden Standard)

_Insights que describen la gobernanza del GS; útiles pero no enseñan una técnica externa._ (4)

*   [[Project_Insights/PI-006|PI-006]] — Cerberus v0.3 – compuerta entre intención y ejecución que impone disciplina de contexto, observabilidad, redacción y control de estado. [ACTIVE Sprint 5-11: WARN→BLOCK en gate APPROVED (recomendaciones solo con FAILs); 12D dominios (D1-D12); 386 tests adversariales; 17 satélites sincronizados; naming verb_noun normalizado; Golden Standard = conocimiento puro (PI-015..PI-018 formalizados).]
*   [[Project_Insights/PI-007|PI-007]] — Gobernanza de salida (diagnóstico Cerberus 2026-05-30) – el sistema tenía gobernanza de ENTRADA (gates de calidad) pero no de SALIDA (poda de huérfanos), por eso acumuló residuo de refactor: 250MB de backups, dead code, 5 docs de plan, scripts espectrales, GLOBAL_LEARNING divergente, base-set stale, IDs TK-043/44/45 declarados sin contenido. Raíz: el gate validaba letra (Path.exists) no vigencia (ruta activa). Orden = el mismo gate que bloquea código malo bloquea la basura que sobra. Ejecutable en PLAN.md P0 (orphan-hunt) / P1 (vulture/VC-118) / P5 (catálogo=ejecución).
*   [[Project_Insights/PI-014|PI-014]] — Golden Standard vivo – conservar conocimiento puro, agnóstico y actualizado con los aprendizajes del proyecto y los satélites sin mezclarlo con herramientas concretas.
*   [[Project_Insights/PI-018|PI-018]] — Ingesta canónica de aprendizajes – normalizar, deduplicar y registrar nuevas lecciones satélite antes de incorporarlas al conocimiento central.

---
[[Home|Volver al Inicio]]
