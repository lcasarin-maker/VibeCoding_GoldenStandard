# CODERCERBERUS
## Conceptual framework, operational philosophy, and functional architecture

> Deprecated as canonical GS source. The live Golden Standard source of truth is `CONCEPTUAL_FRAMEWORK.md`.
> This file is preserved as historical lineage and should not be extended as the primary doctrine.

## 1. Guiding idea

CoderCerberus takes its name from Cerberus, the guardian of the Underworld. Its symbolic role was to prevent passage for those who did not meet the requirements to enter.

That is the project's central philosophy: CoderCerberus must function as guardian, watcher, and gatekeeper for AI-assisted programming projects.

Its purpose is to prevent any code from reaching production, the repository, or integration:

- badly made;
- malformed;
- fragile;
- undocumented;
- non-reversible;
- non-scalable;
- hard to audit;
- disconnected from real functionality;
- built only to "pass tests";
- a product of vibe-coding anti-patterns;
- a generator of unnecessary rework.

CoderCerberus must not limit itself to checking formalities. Its function is not to verify that files, folders, tests, or documentation exist in a ceremonial way. Its function is to protect the real quality of the software.

The final criterion is not that the project "looks correct." The final criterion is that the software works, is traceable, is reversible, is maintainable, is scalable, and can be used correctly by a human.

---

## 2. Problem it aims to solve

AI-assisted programming, especially under vibe-coding schemes, allows fast progress but creates structural risks.

Among them:

1. Code that appears to work but is poorly designed.
2. Tests that validate security theater.
3. Features implemented only partially.
4. Disconnects between backend, frontend, and user experience.
5. Files created to satisfy instructions, with no real operational value.
6. Non-reversible solutions.
7. Loss of traceability.
8. Disorderly project growth.
9. Accumulation of invisible technical debt.
10. Excessive token consumption due to poor planning, repetition, or lack of structure.
11. Lack of institutional memory across sessions, agents, and projects.
12. Repetition of errors already detected earlier.

CoderCerberus exists to keep those vices from entering, persisting, or reproducing.

---

## 3. Golden Standard

### 3.1. Definition

Golden Standard is the central knowledge library of CoderCerberus.

It is not a specific software project. It is not an isolated prompt. It is not a static list of best practices.

Golden Standard is a living repository of normative, technical, and operational knowledge about how to program with AI without falling into the common vices of vibe coding.

It must be:

- project agnostic;
- agent agnostic;
- dynamic;
- cumulative;
- refinable;
- traceable;
- non-destructive of cognitive load;
- a single source of truth for CoderCerberus.

### 3.2. Function

Golden Standard must contain the principles, rules, anti-patterns, mandates, and validation criteria that govern both CoderCerberus and the projects monitored by CoderCerberus.

Every lesson learned during coding sessions, audits, detected errors, testing failures, or observed bad practices must feed back into Golden Standard.

Golden Standard must not lose knowledge. It must refine it.

The goal is not to simplify by destroying nuance, but to systematize while preserving cognitive load.

### 3.3. Dynamic nature

Golden Standard must grow through use.

Every time CoderCerberus detects a new vice, a new failure, a new form of simulation, a new bad testing practice, or a new efficient tokenomics strategy, that finding must become structured knowledge.

That knowledge must be transformable into:

1. a rule;
2. a mandate;
3. an anti-pattern;
4. a test;
5. a warning;
6. a heuristic;
7. an improvement to CoderCerberus itself.

### 3.4. Normative function

Every internal or external mandate in CoderCerberus must derive from Golden Standard.

There must not be any active rule in Cerberus that cannot be traced back to Golden Standard.

There must not be any critical item in Golden Standard that has no operational reflection in Cerberus.

### 3.5. Mandatory operability rule

No principle, mandate, anti-pattern, criterion, or rule contained in Golden Standard can be considered operational merely because it is documented.

For an element of Golden Standard to be considered operational, it must have, at minimum:

1. an executable rule;
2. an associated test;
3. verifiable execution evidence;
4. a defined consequence in case of noncompliance.

La documentación, por sí sola, no convierte un principio en control real.

Un principio sin regla ejecutable es solo una declaración de intención.

Una regla sin prueba asociada es una hipótesis no verificada.

Una prueba sin evidencia verificable es teatro de seguridad.

Una evidencia sin consecuencia operativa es auditoría decorativa.

Por tanto, CoderCerberus debe imponer desde su diseño una cadena mínima de operatividad:

```text
Golden Standard → Regla ejecutable → Prueba asociada → Evidencia generada → Consecuencia definida
```

Todo elemento que no pueda recorrer esta cadena debe marcarse como:

- no operativo;
- pendiente de implementación;
- pendiente de prueba;
- pendiente de evidencia;
- pendiente de consecuencia.

Ningún elemento no operativo debe utilizarse como base para afirmar que CoderCerberus controla efectivamente un riesgo.

---

## 4. Three main domains

CoderCerberus must be organized around three major domains.

### 4.1. Vibe-coding vices

Este dominio contiene los errores, malas prácticas y desviaciones comunes al programar con inteligencia artificial.

Incluye, entre otros:

- código improvisado;
- soluciones parciales;
- hardcoding indebido;
- rutas absolutas;
- archivos fantasma;
- documentación ficticia;
- tests cosméticos;
- funcionalidades inaccesibles para el usuario;
- falta de reversibilidad;
- falta de trazabilidad;
- falta de arquitectura;
- acumulación de deuda técnica;
- soluciones que funcionan solo en el entorno inmediato;
- parches no integrados al diseño general;
- pérdida de sincronía entre módulos;
- uso de prompts sin control operativo.

### 4.2. Testing vices

Este dominio está al mismo nivel jerárquico que los vicios de vibe coding.

No basta con tener tests. Los tests pueden convertirse en teatro de seguridad si solo verifican apariencias.

CoderCerberus debe detectar y evitar:

- tests que validan existencia de archivos sin validar funcionalidad;
- tests que no ejecutan flujos reales;
- tests omitidos por mala nomenclatura;
- tests desconectados del comportamiento humano esperado;
- tests que pasan aunque la funcionalidad sea inaccesible;
- tests que no cubren integración backend/frontend;
- pruebas que no detectan regresiones reales;
- pruebas que validan mocks irrelevantes;
- pruebas que solo confirman que el código “parece” correcto;
- pruebas sin correspondencia con los riesgos reales del proyecto.

El objetivo no es pasar tests.

El objetivo es que los tests demuestren que el software funciona de verdad.

### 4.3. Tokenomics

Tokenomics es un dominio de gobernanza separado de los vicios. No describe antipatrón, sino eficiencia, headroom y gestión de contexto durante el desarrollo.

Debe considerarse importante, pero subordinado a la pureza del código.

Correct hierarchy:

1. Calidad, seguridad, funcionalidad, trazabilidad y reversibilidad del código.
2. Calidad real del testing.
3. Eficiencia en tokens.

Tokenomics no debe justificar atajos que degraden el software. Su función es evitar desperdicio, repetición, dispersión y sobrecarga innecesaria sin sacrificar calidad.

---

## 5. Principle of hierarchy between domains

Vibe-coding vices and testing vices are at the highest-priority level.

Tokenomics está en un segundo nivel.

La eficiencia en tokens nunca debe prevalecer sobre:

- funcionalidad real;
- trazabilidad;
- reversibilidad;
- arquitectura;
- escalabilidad;
- testing significativo;
- seguridad;
- experiencia del usuario;
- mantenibilidad.

Regla operativa:

> Ahorrar tokens es valioso solo si no reduce la calidad real del proyecto.

---

## 6. Conceptual architecture of CoderCerberus

CoderCerberus must operate across three main layers:

1. Golden Standard.
2. Cerberus al interior.
3. Cerberus al exterior.

---

## 7. Layer 1: Golden Standard

Golden Standard es el repositorio puro de conocimiento.

### 7.1. Characteristics

Debe ser:

- independiente de proyectos concretos;
- independiente de agentes concretos;
- actualizable;
- auditable;
- versionable;
- estructurado;
- no redundante, salvo cuando la redundancia conserve matices útiles;
- protegido contra pérdida de carga cognitiva;
- fuente única de verdad.

### 7.2. Normative function

Every internal or external CoderCerberus mandate must derive from Golden Standard.

No debe existir una regla activa en Cerberus que no pueda rastrearse a Golden Standard.

No debe existir un ítem crítico en Golden Standard que no tenga reflejo operativo en Cerberus.

### 7.3. Mandatory operability rule

Ningún principio de Golden Standard puede considerarse operativo si no tiene:

1. regla ejecutable;
2. prueba asociada;
3. evidencia generada;
4. consecuencia definida.

Esta regla debe operar como filtro de madurez.

Un conocimiento puede existir dentro de Golden Standard como hallazgo, nota, heurística o principio preliminar. Sin embargo, no debe considerarse control activo hasta que pueda demostrar su cadena completa de operatividad.

La clasificación mínima de cada elemento de Golden Standard debe ser:

| Estado | Significado |
|---|---|
| `CONOCIMIENTO` | Existe como hallazgo o principio, pero aún no tiene implementación operativa. |
| `REGLA_DEFINIDA` | Tiene mandato formulado, pero aún no tiene prueba. |
| `PRUEBA_ASOCIADA` | Tiene prueba, pero aún no genera evidencia suficiente. |
| `EVIDENCIA_GENERADA` | Produce evidencia, pero aún no tiene consecuencia definida. |
| `OPERATIVO` | Tiene regla, prueba, evidencia y consecuencia. |
| `BLOQUEANTE` | Además de ser operativo, puede impedir commits, merges o integraciones. |

---

## 8. Layer 2: Cerberus internally

Cerberus internally is the layer that governs the CoderCerberus project itself.

Su objetivo es asegurar que CoderCerberus no incurra en los mismos vicios que pretende prevenir.

### 8.1. Principle of self-regulation

CoderCerberus must audit itself.

Debe existir correspondencia entre:

1. cada ítem del Golden Standard;
2. una regla o mandato operativo de Cerberus;
3. una prueba que valide esa regla;
4. una evidencia de ejecución;
5. una consecuencia si la regla falla.

### 8.2. Exhaustiveness

CoderCerberus debe ser exhaustivo.

Por cada antipatón, vicio, regla o mandato contenido en Golden Standard, debe existir una implementación verificable dentro de Cerberus.

Esa implementación no debe ser decorativa. Debe tener efecto real.

### 8.3. Real tests, not security theater

Cada regla debe contar con una prueba que evalúe la realidad de su cumplimiento.

No basta con comprobar que existe un archivo.

No basta con comprobar que existe una función.

No basta con comprobar que existe documentación.

Debe comprobarse que la regla funciona operativamente.

### 8.4. Automation

CoderCerberus must operate automatically because the user is not a programmer.

El sistema debe reducir al mínimo la necesidad de intervención técnica manual.

La automatización debe cubrir:

- auditoría;
- validación;
- bloqueo;
- generación de reportes;
- trazabilidad;
- retroalimentación al Golden Standard;
- ejecución de pruebas;
- revisión de calidad;
- detección de regresiones;
- validación de correspondencia entre reglas y pruebas.

---

## 9. Layer 3: Cerberus externally

Cerberus externally is the project's main reason for existence.

Su función es vigilar, auditar y bloquear malas prácticas en otros proyectos de programación.

Debe operar en dos momentos:

1. en tiempo real;
2. a posteriori.

### 9.1. Real-time monitoring

CoderCerberus debe actuar como gatekeeper antes de que errores, vicios o malas prácticas entren al repositorio o lleguen a GitHub.

Debe impedir commits, cambios o integraciones que incumplan Golden Standard.

### 9.2. Post-audit

CoderCerberus must also be able to audit existing projects.

Debe detectar:

- deuda técnica;
- errores latentes;
- inconsistencias;
- funcionalidades incompletas;
- tests inservibles;
- documentación falsa o insuficiente;
- problemas de arquitectura;
- problemas de trazabilidad;
- problemas de reversibilidad;
- desconexión entre backend y frontend;
- desviaciones respecto de Golden Standard.

### 9.3. Error blocking

CoderCerberus no debe limitarse a reportar.

Cuando sea posible, debe bloquear.

El sistema debe impedir que pasen a GitHub cambios que incumplan reglas críticas.

---

## 10. Private repositories, traceability, and reversibility

Every AI-developed programming project must have its own private repository.

Este es un principio operativo obligatorio.

La finalidad es garantizar:

- trazabilidad;
- reversibilidad;
- historial de cambios;
- auditoría;
- rollback;
- comparación entre versiones;
- control de deuda técnica;
- control de decisiones;
- reconstrucción del proceso de desarrollo.

Sin repositorio propio, no hay trazabilidad suficiente.

Sin trazabilidad, no hay reversibilidad confiable.

Sin reversibilidad, no hay control real del riesgo.

---

## 11. Repository hygiene, cleanliness, and organization

CoderCerberus must monitor not only code quality but also the repository's cleanliness, organization, and structural maintainability.

Un repositorio desordenado es deuda técnica visible. Aunque el código funcione, la acumulación de archivos temporales, nombres confusos, carpetas innecesarias, logs residuales, scripts descartables y estructuras infladas degrada la trazabilidad, dificulta la auditoría y aumenta el riesgo de errores futuros.

La limpieza del repositorio debe considerarse un principio operativo de primer nivel.

Esta doctrina se expone también como una capa de navegación dedicada dentro del vault, enlazada desde Home y desde la documentación raíz, para que la higiene no quede enterrada dentro de un bloque largo de marco conceptual.

GS define la norma; Cerberus debe ejecutar la vigilancia, la evidencia y la consecuencia operativa en los repositorios que consume.

### 11.1. Clean repository principle

Every project monitored by CoderCerberus must maintain a clear, minimal, readable, and justifiable structure.

El repositorio debe contener únicamente archivos, carpetas, scripts, configuraciones, pruebas, documentación y artefactos que tengan una función vigente, verificable y necesaria.

Debe evitarse la acumulación de:

- scripts temporales ya utilizados;
- archivos duplicados;
- archivos obsoletos;
- carpetas de pruebas abandonadas;
- logs residuales;
- respaldos manuales dentro del repositorio;
- versiones alternativas sin control de Git;
- archivos generados que debieron estar en `.gitignore`;
- salidas de ejecución no necesarias;
- documentos experimentales sin clasificación;
- prompts viejos sin valor operativo;
- pruebas descartadas que ya no forman parte del sistema;
- archivos con nombres ambiguos, grandilocuentes o no descriptivos.

### 11.2. Simple and descriptive names

CoderCerberus must prohibit the vibe-coding tendency to create bombastic, ceremonial, or abstract names that do not accurately describe the real function of a file, folder, module, or script.

Los nombres deben ser:

- sencillos;
- descriptivos;
- consistentes;
- funcionales;
- legibles para un humano;
- proporcionales a la importancia real del componente;
- alineados con convenciones técnicas ordinarias.

Debe evitarse el uso de nombres que aparentan sofisticación sin agregar claridad.

Ejemplos de nombres problemáticos:

- `ultimate_engine.py`;
- `final_super_validator.py`;
- `god_mode_audit.py`;
- `hyper_orchestrator_v3_final.py`;
- `mega_refactor_clean.py`;
- `real_final_tests_backup.py`;
- `golden_absolute_truth_runner.py`.

Ejemplos de nombres preferibles:

- `validate_rules.py`;
- `audit_repository.py`;
- `check_test_coverage.py`;
- `cleanup_temp_files.py`;
- `generate_report.py`;
- `sync_golden_standard.py`;
- `run_pre_commit_checks.py`.

La regla debe ser:

> El nombre debe explicar qué hace el componente, no vender su importancia.

### 11.3. As-flat-as-possible structures

CoderCerberus must favor as-flat-as-possible folder structures, as long as doing so does not sacrifice clarity, separation of responsibilities, or scalability.

Debe evitarse la sobrearquitectura de carpetas creada por agentes de IA para aparentar diseño avanzado.

Una carpeta nueva solo debe existir si cumple al menos una de estas funciones:

1. agrupa archivos con una responsabilidad común real;
2. reduce complejidad de navegación;
3. separa dominios funcionales distintos;
4. permite ejecución, testing o mantenimiento más claro;
5. evita mezcla indebida de artefactos de naturaleza diferente.

Si una carpeta no cumple una función clara, debe eliminarse o fusionarse.

### 11.4. Eliminación de archivos temporales post uso

Todo archivo temporal creado durante auditoría, refactor, prueba, depuración, migración o generación automática debe eliminarse al terminar su función, salvo que exista razón expresa para conservarlo.

Si se conserva, debe clasificarse correctamente.

Los archivos temporales no deben quedar dispersos en el repositorio.

Debe existir una política clara para:

- archivos temporales;
- logs;
- outputs;
- reportes generados;
- caches;
- respaldos;
- scripts de un solo uso;
- archivos de prueba manual;
- artefactos experimentales.

Cuando sea posible, estos archivos deben:

1. excluirse mediante `.gitignore`;
2. colocarse en carpetas explícitas como `/tmp`, `/logs`, `/reports` o `/artifacts`;
3. eliminarse automáticamente después de su uso;
4. registrarse solo si forman parte de evidencia auditable.

### 11.5. Control de versiones como sustituto de copias manuales

CoderCerberus debe impedir que el repositorio se llene de copias manuales de archivos bajo nombres como:

- `backup`;
- `old`;
- `final`;
- `final2`;
- `real_final`;
- `copy`;
- `working`;
- `previous`;
- `before_refactor`.

El control de versiones debe hacerse mediante Git, no mediante duplicación informal de archivos.

La existencia de copias manuales dentro del repositorio debe considerarse señal de falta de disciplina de versionamiento, salvo que exista justificación técnica expresa.

### 11.6. Limpieza como prueba obligatoria

La limpieza del repositorio debe tener pruebas específicas.

CoderCerberus debe poder detectar:

- archivos temporales persistentes;
- logs no ignorados;
- carpetas vacías;
- carpetas sin propósito claro;
- archivos duplicados;
- nombres no descriptivos;
- nombres grandilocuentes;
- copias manuales;
- artefactos generados fuera de rutas permitidas;
- scripts no referenciados;
- tests abandonados;
- documentación obsoleta;
- archivos que no participan en ningún flujo vigente.

Estas pruebas no deben ser meramente estéticas. Deben proteger la mantenibilidad, trazabilidad, reversibilidad y auditabilidad del proyecto.

### 11.7. Evidencia de higiene del repositorio

Toda auditoría de CoderCerberus debe generar evidencia sobre el estado estructural del repositorio.

Como mínimo, debe poder reportar:

1. árbol de carpetas relevante;
2. archivos sospechosos;
3. archivos temporales detectados;
4. logs y artefactos no justificados;
5. nombres ambiguos o grandilocuentes;
6. carpetas innecesariamente profundas;
7. archivos duplicados o copias manuales;
8. scripts no utilizados;
9. pruebas abandonadas;
10. recomendaciones de eliminación, renombrado o reubicación.

### 11.8. Consecuencia operativa

La falta de higiene del repositorio debe tener consecuencias.

Según gravedad, CoderCerberus debe poder:

- advertir;
- recomendar limpieza;
- abrir issue de limpieza;
- bloquear commits con basura evidente;
- impedir merges con artefactos temporales;
- exigir renombrado de archivos críticos;
- exigir eliminación de scripts descartables;
- exigir actualización de `.gitignore`;
- exigir reorganización de carpetas;
- registrar deuda estructural en el reporte de auditoría.

La limpieza del repositorio no debe tratarse como preferencia estética.

Debe tratarse como condición de mantenibilidad y control técnico.

### 11.9. Mandato Golden Standard

Debe incorporarse a Golden Standard un mandato específico de higiene estructural:

> Todo repositorio vigilado por CoderCerberus debe mantenerse limpio, plano en lo razonable, descriptivo en su nomenclatura, libre de basura temporal, sin copias manuales que sustituyan Git, sin carpetas ceremoniales y con evidencia verificable de organización funcional.

Este mandato debe tener regla ejecutable, prueba asociada, evidencia generada y consecuencia definida.

### 11.10. Execution and tooling hygiene

The quality of Golden Standard depends not only on content, but also on how it is inspected, edited, and validated.

Toda interacción con herramientas debe seguir una disciplina de ejecución mínima, estable y reproducible:

- preferir el comando más simple que resuelva el problema;
- dividir tareas grandes en pasos pequeños y verificables;
- usar ediciones declarativas y parches antes que scripts improvisados;
- evitar comandos largos, frágiles o innecesariamente encadenados;
- mantener la codificación y la salida en UTF-8 cuando haya texto internacional;
- no crear scripts temporales si el cambio puede resolverse de forma directa y auditable;
- conservar solo helpers reutilizables o documentados;
- registrar evidencia cuando un comando forme parte de una validación o auditoría;
- tratar la elevación de permisos como excepción, no como rutina;
- preferir operar dentro del workspace de GS antes de cruzar a otros repositorios o rutas externas.

Si una operación falla por complejidad, entorno o sintaxis, la respuesta correcta es simplificar el flujo, no añadir complejidad adicional.

Cuando una herramienta no sea estable o no sea necesaria, GS debe favorecer la alternativa más determinista, legible y reproducible.

Esta regla queda formalizada como `PI-019` para que ejecución e higiene se puedan rastrear como insight satélite y no solo como texto doctrinal.

## 12. Real functional validation

CoderCerberus must validate the software's real functionality.

No basta con verificar que el backend funcione aisladamente.

No basta con verificar que el frontend exista.

No basta con validar endpoints, componentes o archivos separados.

Debe validarse que el software funcione como sistema completo.

### 11.1. Backend y frontend sincronizados

Debe existir sincronía total entre backend y frontend.

Debe evitarse que existan funcionalidades que técnicamente estén implementadas, pero que el usuario no pueda usar.

Una funcionalidad inaccesible para el usuario humano debe considerarse funcionalmente incompleta, aunque el código exista.

### 11.2. Uso humano real

CoderCerberus debe evaluar la intuitividad, accesibilidad y utilidad práctica del software.

El estándar no debe ser únicamente técnico.

Debe incluir la pregunta:

> ¿Puede un usuario humano usar esta funcionalidad de manera clara, real y efectiva?

### 11.3. Prohibición de validación ceremonial

Debe registrarse en Golden Standard como mandato específico que está prohibida la validación ceremonial.

Una validación ceremonial ocurre cuando el sistema pasa pruebas formales sin demostrar funcionamiento sustantivo.

Ejemplos:

- existe el archivo, pero no se usa;
- existe el endpoint, pero no está conectado;
- existe el botón, pero no ejecuta nada útil;
- existe el test, pero no detecta fallos reales;
- existe la documentación, pero no corresponde al código;
- existe una funcionalidad backend, pero no está expuesta al usuario;
- existe una pantalla, pero no se conecta con datos reales.

---

## 13. Project-specific tests

Every project monitored by CoderCerberus must have specific and unique tests.

No basta con aplicar tests genéricos.

Los tests deben corresponder a:

- finalidad del proyecto;
- arquitectura del proyecto;
- flujos reales de usuario;
- riesgos principales;
- funcionalidades críticas;
- integraciones reales;
- errores previsibles;
- antipatrones detectados;
- criterios aplicables del Golden Standard.

### 12.1. Tests against vibe-coding vices

Cada proyecto debe contar con pruebas que detecten malas prácticas típicas del vibe coding.

### 12.2. Tests against testing vices

Cada proyecto debe contar con pruebas que detecten si los propios tests son débiles, ceremoniales, irrelevantes o insuficientes.

### 12.3. Tokenomics tests

Cada proyecto debe desarrollarse y auditarse siguiendo principios de tokenomics, siempre subordinados a la calidad del código.

---

## 14. Feedback loop

Every relevant finding must feed back into the system.

El flujo correcto es:

1. Se detecta un error, vicio, falla o aprendizaje en un proyecto.
2. El hallazgo se documenta.
3. El hallazgo se incorpora o compara contra Golden Standard.
4. Si es nuevo, se agrega a Golden Standard.
5. Si ya existe, se refina sin perder carga cognitiva.
6. Se genera o actualiza una regla interna de Cerberus.
7. Se genera o actualiza una prueba interna de Cerberus.
8. Se genera o actualiza una regla externa aplicable a proyectos vigilados.
9. Se genera o actualiza una prueba externa aplicable a proyectos vigilados.
10. Se conserva trazabilidad del cambio.

El conocimiento no debe quedarse en una sesión aislada.

Todo aprendizaje debe convertirse en sistema.

---

## 15. Total correspondence mandate

There must be a mandatory correspondence matrix between Golden Standard, Cerberus internal, and Cerberus external.

Esta matriz debe demostrar que cada principio de Golden Standard tiene traducción operativa real.

Cada ítem de Golden Standard debe responder:

1. ¿Qué vicio, riesgo o principio regula?
2. ¿Qué regla ejecutable lo implementa?
3. ¿Qué prueba verifica su cumplimiento?
4. ¿Qué evidencia genera la prueba?
5. ¿Qué consecuencia se activa si falla?
6. ¿Qué regla interna de Cerberus lo aplica al propio CoderCerberus?
7. ¿Qué regla externa lo aplica a proyectos vigilados?
8. ¿Cómo se registra la trazabilidad del cumplimiento o incumplimiento?
9. ¿Cómo se retroalimenta Golden Standard si el hallazgo revela una regla incompleta?

Si un ítem de Golden Standard no tiene regla, prueba, evidencia y consecuencia, debe considerarse conocimiento pendiente, no control operativo.

### 14.1. Minimum correspondence matrix

| Campo | Pregunta de control |
|---|---|
| ID Golden Standard | ¿Cuál es el identificador único del principio, regla o antipatón? |
| Dominio | ¿Pertenece a vibe coding, testing o tokenomics? |
| Riesgo regulado | ¿Qué riesgo busca impedir? |
| Regla ejecutable | ¿Qué mandato concreto ejecuta Cerberus? |
| Prueba asociada | ¿Qué test valida la regla? |
| Evidencia | ¿Qué salida, log, reporte o artefacto demuestra cumplimiento? |
| Consecuencia | ¿Qué ocurre si falla? |
| Alcance interno | ¿Cómo aplica al propio CoderCerberus? |
| Alcance externo | ¿Cómo aplica a proyectos vigilados? |
| Estado operativo | ¿Está en conocimiento, regla definida, prueba asociada, evidencia generada, operativo o bloqueante? |
| Retroalimentación | ¿Cómo se actualiza Golden Standard con el hallazgo? |

---

## 16. Principle against security theater

CoderCerberus must fight security theater.

Teatro de seguridad significa que el sistema aparenta controlar riesgos sin controlarlos realmente.

Ejemplos:

- tests que pasan sin ejecutar funcionalidades reales;
- documentación que no coincide con el código;
- reglas que existen pero no bloquean nada;
- auditorías que generan reportes sin consecuencias;
- validaciones que revisan presencia, no comportamiento;
- estructuras que parecen profesionales pero no agregan control;
- prompts extensos sin ejecución verificable;
- reportes que no producen acciones correctivas.

El objetivo de CoderCerberus no es producir apariencia de rigor.

El objetivo es producir control real.

---

## 17. Principle of operational consequence

Every rule must have a consequence.

Una regla sin consecuencia es decoración.

Cada incumplimiento debe generar, según gravedad:

- advertencia;
- bloqueo;
- corrección sugerida;
- apertura de issue;
- actualización de checklist;
- actualización de Golden Standard;
- rechazo de commit;
- rechazo de pull request;
- requerimiento de prueba adicional;
- auditoría ampliada.

---

## 18. Principle of reversibility

Every change must be reversible.

CoderCerberus debe proteger la capacidad de volver a un estado anterior funcional.

Esto exige:

- repositorios privados por proyecto;
- commits claros;
- cambios atómicos cuando sea posible;
- documentación de decisiones relevantes;
- historial legible;
- pruebas antes y después de cambios críticos;
- control de versiones;
- registro de auditorías;
- capacidad de rollback.

La reversibilidad es una condición de seguridad.

---

## 19. Principle of traceability

Every relevant decision must be traceable.

Debe poder saberse:

- qué se cambió;
- por qué se cambió;
- quién o qué agente lo cambió;
- con base en qué regla se cambió;
- qué prueba lo validó;
- qué evidencia se generó;
- qué efecto tuvo;
- qué relación guarda con Golden Standard.

La trazabilidad convierte sesiones dispersas de IA en conocimiento acumulable.

---

## 20. Principle of automation for a non-programmer user

CoderCerberus must be designed under the assumption that the user is not a programmer.

El sistema debe ser usable por una persona que necesita resultados técnicos confiables sin tener que intervenir manualmente en cada detalle.

Debe privilegiarse:

- ejecución automatizada;
- reportes claros;
- instrucciones accionables;
- bloqueo preventivo;
- mínima fricción técnica;
- comandos simples;
- integración con GitHub;
- evidencia entendible;
- resultados auditables.

---

## 21. Resultado esperado

CoderCerberus debe convertirse en un sistema de gobernanza técnica para proyectos programados con inteligencia artificial.

Su función no es programar directamente.

Su función es custodiar la calidad, trazabilidad, reversibilidad, funcionalidad y eficiencia de los proyectos programados con IA.

Debe ser:

- guardián;
- auditor;
- gatekeeper;
- sistema de memoria;
- sistema de pruebas;
- sistema de bloqueo;
- sistema de aprendizaje;
- puente entre Golden Standard y proyectos reales.

---

## 22. Síntesis operativa

CoderCerberus se resume en tres piezas.

### 21.1. Golden Standard

Repositorio puro de conocimiento, project agnostic y agent agnostic.

Es dinámico, actualizable y refinable.

Debe conservar carga cognitiva.

Funciona como fuente única de verdad.

### 21.2. Cerberus al interior

Sistema de autorregulación del propio CoderCerberus.

Debe tener una regla o mandato por cada antipatón o principio de Golden Standard.

Cada regla debe tener una prueba correspondiente.

Cada prueba debe validar cumplimiento real, no teatro de seguridad.

Todo debe operar de forma automatizada y eficiente en tokens.

### 21.3. Cerberus al exterior

Sistema de vigilancia, auditoría y bloqueo aplicable a otros proyectos.

Debe operar en tiempo real y a posteriori.

Debe impedir que entren a GitHub malas prácticas de vibe coding, testing deficiente o desperdicio grave de tokens.

Cada hallazgo debe retroalimentar Golden Standard y reflejarse después en Cerberus interno y externo.

---

## 23. Arquitectura lógica mínima recomendada

```text
/codercerberus
│
├── /golden-standard
│   ├── vibe-coding-antipatterns.md
│   ├── testing-antipatterns.md
│   ├── tokenomics-principles.md
│   ├── rule-registry.md
│   └── maturity-matrix.md
│
├── /cerberus-core
│   ├── rule-engine
│   ├── evidence-engine
│   ├── consequence-engine
│   └── traceability-engine
│
├── /cerberus-tests
│   ├── internal-compliance-tests
│   ├── golden-standard-coverage-tests
│   ├── anti-theater-tests
│   └── regression-tests
│
├── /project-auditor
│   ├── static-analysis
│   ├── functional-analysis
│   ├── testing-analysis
│   ├── repository-hygiene-analysis
│   ├── frontend-backend-sync
│   └── human-usability-analysis
│
├── /github-gatekeeper
│   ├── pre-commit-hooks
│   ├── pre-push-hooks
│   ├── pull-request-checks
│   └── blocking-rules
│
├── /reports
│   ├── audit-reports
│   ├── evidence-logs
│   ├── failure-reports
│   └── remediation-reports
│
└── /feedback-loop
    ├── new-findings
    ├── golden-standard-updates
    ├── rule-updates
    └── test-updates
```

---

## 24. Matriz nuclear del sistema

| Componente | Función | Riesgo que evita |
|---|---|---|
| Golden Standard | Fuente de verdad | Pérdida de conocimiento entre proyectos |
| Cerberus interno | Autorregulación | Que Cerberus incurra en los mismos vicios que combate |
| Cerberus externo | Vigilancia de proyectos | Entrada de código viciado a GitHub |
| Testing real | Validación sustantiva | Teatro de seguridad |
| Tokenomics | Eficiencia secundaria | Desperdicio de tokens sin sacrificar calidad |
| Repos privados | Trazabilidad y reversibilidad | Pérdida de control histórico |
| Feedback loop | Aprendizaje acumulativo | Repetición de errores ya detectados |
| Consequence engine | Consecuencia operativa | Reglas decorativas sin efecto real |
| Evidence engine | Prueba verificable | Auditoría sin evidencia |
| Rule engine | Traducción ejecutable del conocimiento | Golden Standard no operativo |
| Repository hygiene | Limpieza y organización estructural | Basura, nombres confusos, carpetas ceremoniales y deuda técnica visible |

---

## 25. Regla fundacional de diseño

Desde el inicio debe imponerse la siguiente regla de diseño:

> Ningún principio de Golden Standard puede considerarse operativo si no tiene regla ejecutable, prueba asociada, evidencia generada y consecuencia definida.

Esta regla debe ser tratada como axioma estructural de CoderCerberus.

Sin esta regla, CoderCerberus corre el riesgo de convertirse en una biblioteca extensa de buenas prácticas sin capacidad real de control.

Con esta regla, CoderCerberus transforma conocimiento en gobernanza técnica ejecutable.

---

## 26. Tesis central

CoderCerberus debe impedir que la velocidad del vibe coding destruya la calidad del software.

Debe transformar experiencia dispersa en conocimiento acumulativo.

Debe convertir errores detectados en reglas.

Debe convertir reglas en pruebas.

Debe convertir pruebas en evidencia.

Debe convertir evidencia en consecuencias.

Debe convertir consecuencias en trazabilidad.

Debe convertir hallazgos en mejoras del Golden Standard.

CoderCerberus no existe para que el código parezca correcto.

Existe para que el código no pueda avanzar si está viciado.

Sin la cadena:

```text
Golden Standard → Regla ejecutable → Prueba asociada → Evidencia generada → Consecuencia definida
```

no hay control real.
