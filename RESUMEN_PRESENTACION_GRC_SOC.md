# Resumen para Presentación — Proyecto GRC con SOC Simulado

**Proyecto:** Modelo GRC con SOC Simulado  
**Organización:** TechGuard Guatemala S.A.  
**Objetivo:** demostrar gobierno, riesgo, cumplimiento, monitoreo SOC, respuesta a incidentes y métricas ejecutivas usando laboratorio Docker, scripts Python y dashboard gerencial.

---

## 1. Resumen Ejecutivo

| Elemento | Explicación |
|---|---|
| Problema | TechGuard enfrenta riesgos de fuerza bruta, exfiltración, ransomware, accesos indebidos y brechas de cumplimiento. |
| Solución | Implementar modelo GRC práctico con laboratorio SOC, reglas SIEM, métricas, KRIs, KPIs y dashboard ejecutivo. |
| Resultado | Se integró documentación GRC, simulación técnica, detección de incidentes y visualización gerencial. |
| Valor para dirección | El dashboard convierte eventos técnicos en decisiones: riesgo residual, cumplimiento, exposición financiera y acciones prioritarias. |

---

## 2. Matriz General por Fase

| Fase | Qué se hizo | Cómo cumple la tarea | Cómo explicarlo en presentación |
|---|---|---|---|
| Fase 1: Planeación y análisis | Se definió TechGuard, contexto, activos críticos, amenazas, madurez y riesgo inicial. | Cumple análisis inicial GRC y justifica necesidad de controles. | "Primero analizamos organización, activos y amenazas para medir riesgo inicial antes de aplicar controles." |
| Fase 2: Diseño | Se diseñó arquitectura SOC/GRC, controles, responsables y relación con ISO 27001, NIST y PCI-DSS. | Integra teoría GRC con controles concretos. | "Aquí convertimos riesgos en controles y responsables." |
| Fase 3: Implementación | Se desarrollaron scripts Python para fuerza bruta, exfiltración, port scanning, ransomware y acceso a archivos sensibles. | Cumple parte práctica porque genera eventos y evidencia técnica. | "Los ataques no solo están descritos; se simulan y producen logs analizables." |
| Fase 4: Herramientas | Se creó laboratorio Docker con servidor SOC, atacante y dashboard SIEM/GRC. | Cumple requerimiento de laboratorio técnico y dashboard SOC. | "Docker separa roles y permite demostrar arquitectura de monitoreo." |
| Fase 5: Monitoreo | Se definieron KPIs/KRIs y dashboard con gráficas, alertas, riesgos y plan de acción. | Cumple dashboard de métricas y monitoreo continuo. | "El dashboard traduce logs técnicos a indicadores ejecutivos." |
| Cierre: Conclusiones | Se documentaron mejoras, brechas y recomendaciones. | Cierra ciclo GRC con mejora continua. | "No termina en detectar; termina en decidir qué remediar primero." |

---

## 3. Matriz de Cumplimiento de Requerimientos

| Requerimiento de la tarea | Evidencia entregada | Estado |
|---|---|---:|
| Planeación GRC | `docs/01_FASE1_Planeacion_Analisis.md` | Cumple |
| Diseño de arquitectura y riesgos | `docs/02_FASE2_Diseno.md` | Cumple |
| Implementación técnica | Scripts en `scripts/*.py` | Cumple |
| Laboratorio práctico | `docker-compose.yml`, `Dockerfile.soc` | Cumple |
| SIEM o simulación SOC | `scripts/siem_simulado.py`, alertas `GRC-*` | Cumple |
| Dashboard de métricas | `scripts/dashboard.html`, `scripts/siem_dashboard_web.py` | Cumple |
| KPIs/KRIs | `docs/05_FASE5_Monitoreo_KPIs.md`, dashboard | Cumple |
| Integración teoría + práctica | ISO/NIST/PCI + logs + dashboard | Cumple |
| Conclusiones y mejora continua | `docs/06_Conclusiones_Recomendaciones.md` | Cumple |

---

## 4. Matriz Técnica del Laboratorio

| Componente | Rol | Evidencia | Uso en presentación |
|---|---|---|---|
| `grc-soc-lab` | Servidor SOC principal | Contenedor Ubuntu con scripts y logs | Mostrar que existe ambiente controlado de monitoreo. |
| `grc-attacker` | Atacante simulado | Contenedor Alpine | Explicar origen de eventos ofensivos simulados. |
| `grc-siem` | Dashboard y API | Puerto `8080` | Abrir dashboard para evidenciar monitoreo ejecutivo. |
| `logs/auth.log` | Logs de autenticación | Intentos fallidos, login exitoso, acceso a archivos | Evidencia técnica forense. |
| `siem_data/*.json` | Datos para dashboard | Alertas y métricas exportadas | Prueba de conexión entre scripts y visualización. |

---

## 5. Matriz de Escenarios Simulados

| Escenario | Qué representa | Detección | Riesgo asociado | Control GRC relacionado |
|---|---|---|---|---|
| Fuerza bruta SSH | Intentos repetidos de acceso | Regla `GRC-1001` | Compromiso de credenciales | MFA, monitoreo, bloqueo IP |
| Acceso a `/etc/passwd` | Exploración de archivos sensibles | Regla `GRC-1002` | Escalada de privilegios | Hardening, control de acceso |
| Exfiltración 2GB | Salida no autorizada de datos | Regla `GRC-1003` | Fuga de información | DLP, respuesta a incidentes |
| Port scanning | Reconocimiento externo | Regla `GRC-1004` | Preparación de ataque | Firewall, IDS, monitoreo |
| Kill Chain | Correlación de eventos | Regla `GRC-1099` | Ataque avanzado | SIEM, IR plan, escalamiento |
| Ransomware simulado | Archivos `.locked` | Script `ransomware_sim.py` | Impacto operativo | Backups, recuperación, BCP |

---

## 6. Matriz de KPIs y KRIs

| Indicador | Tipo | Valor usado | Meta | Interpretación ejecutiva |
|---|---|---:|---:|---|
| Riesgo residual | KRI | 18% base / variable en simulación | <= 20% | Mide riesgo restante después de controles. |
| MTTR | KPI | 14 min base / variable | <= 15 min | Tiempo promedio de respuesta del SOC. |
| MTTD | KPI | 3 min base / variable | <= 5 min | Tiempo promedio de detección. |
| SLA SOC | KPI | 92% base / variable | >= 90% | Incidentes resueltos dentro del tiempo esperado. |
| ISO 27001 | KRI | 78% base / variable | >= 85% | Brecha de madurez de controles. |
| PCI-DSS | KRI | 55% base / variable | >= 80% | Brecha relevante si hay datos de pago/clientes. |
| MFA privilegiado | KRI | 55% base / variable | 100% | Riesgo alto de acceso no autorizado. |
| Vulnerabilidades críticas | KRI | 3 base / variable | 0 | Riesgo técnico pendiente de remediar. |

---

## 7. Matriz del Dashboard

| Sección del dashboard | Qué muestra | Para qué sirve |
|---|---|---|
| KPIs superiores | Riesgo residual, exposición, alertas, MTTR, SLA, ISO | Resumen rápido para dirección. |
| Evolución de riesgo | Riesgo antes/después o por periodo | Demuestra mejora y tendencia. |
| Cumplimiento y controles | Actual vs meta | Muestra brechas ISO, PCI, MFA, logs, backups. |
| Distribución de incidentes | Tipos de ataques | Explica qué amenaza domina. |
| Registro ejecutivo de riesgos | Riesgo, dueño, tratamiento, score | Conecta SOC con GRC. |
| Plan de acción | Prioridad, responsable, plazo, estado | Convierte hallazgos en acciones. |
| Alertas SIEM | Reglas y eventos detectados | Evidencia monitoreo técnico. |
| Consola técnica | Logs crudos | Soporte forense para defender la simulación. |
| Botón Simular periodo SOC | Genera nuevo escenario | Demuestra monitoreo continuo y datos variables. |

---

## 8. Cómo Presentarlo

| Orden | Qué mostrar | Frase sugerida |
|---:|---|---|
| 1 | Problema | "TechGuard enfrenta amenazas técnicas y brechas de cumplimiento; por eso se propone un modelo GRC integrado con SOC." |
| 2 | Fases | "El proyecto sigue ciclo completo: análisis, diseño, implementación, herramientas, monitoreo y mejora continua." |
| 3 | Arquitectura Docker | "El laboratorio separa servidor SOC, atacante y dashboard para simular un entorno empresarial." |
| 4 | Scripts SOC | "Los scripts generan eventos técnicos: fuerza bruta, exfiltración, port scanning y ransomware." |
| 5 | Dashboard | "Aquí se traducen esos eventos a KPIs, KRIs, gráficas y acciones ejecutivas." |
| 6 | Botón Simular periodo SOC | "Este botón genera un nuevo periodo operativo y cambia alertas, métricas y riesgos." |
| 7 | Brechas | "Aunque el SOC está operacional, quedan brechas: MFA, PCI-DSS, ISO y vulnerabilidades críticas." |
| 8 | Cierre | "El valor del proyecto es integrar teoría GRC con evidencia técnica y toma de decisiones." |

---

## 9. Guion Corto de Defensa

| Momento | Guion |
|---|---|
| Inicio | "Este proyecto implementa un modelo GRC con SOC simulado para TechGuard Guatemala. El objetivo fue unir gobierno, riesgo, cumplimiento y monitoreo técnico." |
| Metodología | "Se trabajó por fases: primero diagnóstico, luego diseño de controles, implementación de scripts, laboratorio Docker, métricas y mejora continua." |
| Técnica | "El laboratorio genera logs de ataques simulados y el SIEM correlaciona eventos mediante reglas GRC-1001 a GRC-1099." |
| Gerencial | "El dashboard muestra lo que dirección necesita: riesgo residual, exposición financiera, cumplimiento, incidentes y plan de acción." |
| Simulación | "Con el botón Simular periodo SOC se genera otro escenario y se actualizan KPIs y gráficas, demostrando monitoreo continuo." |
| Cierre | "La principal conclusión es que el SOC mejora detección y respuesta, pero GRC identifica brechas pendientes: MFA, PCI-DSS, ISO y vulnerabilidades críticas." |

---

## 10. Frase Final

| Frase |
|---|
| "Este proyecto integra GRC y SOC: identifica riesgos, los relaciona con controles, simula incidentes, mide respuesta y presenta métricas ejecutivas para toma de decisiones." |

