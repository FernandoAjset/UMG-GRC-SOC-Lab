# Conclusiones y Recomendaciones — Modelo GRC TechGuard Guatemala

## Universidad Mariano Gálvez de Guatemala
**Curso:** Gobierno, Riesgo y Cumplimiento | **Catedrático:** MS.c. Erick Enrique Blanco Acevedo  
**Organización:** TechGuard Guatemala S.A.

---

## Conclusiones Generales del Proyecto

### Conclusión 1 (Integrante 1 — Fase Planeación)

La evaluación de madurez GRC de TechGuard Guatemala S.A. reveló un nivel inicial de **1.4/5**, evidenciando brechas significativas en los dominios de gestión de incidentes y monitoreo SOC. La definición estructurada de roles (CISO, SOC Analyst, DFIR, Cloud Admin) mediante la Matriz RACI demostró que la claridad organizacional es el primer paso indispensable para una implementación GRC efectiva. Sin roles definidos, los controles técnicos más sofisticados resultan inoperantes.

### Conclusión 2 (Integrante 2 — Fase Diseño)

La matriz de riesgos identificó **12 amenazas activas**, de las cuales **3 son críticas** (fuerza bruta, exfiltración de datos, incumplimiento PCI-DSS). La metodología cuantitativa aplicada (Probabilidad × Impacto) permitió priorizar objetivamente las inversiones en controles, evitando el error común de tratar todos los riesgos con igual urgencia. La arquitectura de defensa en profundidad con 3 contenedores Docker demostró que un entorno SOC funcional puede construirse con recursos mínimos.

### Conclusión 3 (Integrante 3 — Fase Implementación)

La simulación de 3 escenarios de incidentes (fuerza bruta, exfiltración, ransomware) confirmó que el ciclo de vida NIST SP 800-61r2 proporciona un marco estructurado y reproducible para la respuesta a incidentes. El MTTD promedio de **1.8 minutos** y el MTTR promedio de **15.5 minutos** superaron las metas establecidas, validando la efectividad del laboratorio. La integración de logs con SHA256 para cadena de custodia es un diferenciador crítico para la admisibilidad forense de evidencia digital.

### Conclusión 4 (Integrante 4 — Fase Herramientas)

El laboratorio Docker con SIEM Python simulado demostró que las herramientas de código abierto son suficientes para implementar detección de amenazas a nivel operativo en organizaciones medianas. La regla de correlación **GRC-1099 (Kill Chain)** — que correlaciona fuerza bruta + acceso exitoso + exfiltración — representa el nivel más sofisticado de detección automatizada, equivalente conceptualmente a las reglas de correlación de Splunk Enterprise Security o Wazuh SIEM.

### Conclusión 5 (Integrante 5 — Fase Monitoreo)

El framework de KPIs/KRIs implementado reveló que el 80% de los indicadores operativos cumplen con sus metas, pero el 44% de los KRIs estratégicos presentan brechas (MFA, PCI-DSS, ISO 27001). Esto refleja una realidad común en organizaciones en transición GRC: los controles detectivos mejoran rápidamente con tecnología, pero los controles preventivos y de cumplimiento requieren tiempo, procesos y cultura organizacional. La reducción del riesgo residual del **76% al 24%** en 5 días valida el retorno de inversión del modelo GRC implementado.

---

## Conclusión General del Equipo

La implementación del modelo GRC con enfoque tecnológico y SOC simulado en TechGuard Guatemala S.A. demostró que la integración de tres dimensiones —**gobierno** (roles y procesos), **riesgo** (matriz cuantitativa y tratamiento) y **cumplimiento** (NIST, ISO 27001, PCI-DSS)— produce una sinergia que ninguno de los tres elementos logra de forma aislada.

El laboratorio Docker materializa el concepto abstracto de GRC en evidencia tangible y reproducible: logs reales, alertas automáticas, métricas medibles y reportes ejecutivos. Esta tangibilidad es lo que diferencia un programa GRC efectivo de uno meramente documental.

---

## Recomendaciones

### Recomendación 1: Implementación Inmediata de MFA

**Hallazgo:** El 45% de los usuarios privilegiados no tiene MFA activo (KRI-08 en estado CRÍTICO).  
**Recomendación:** Implementar autenticación multifactor en todos los accesos privilegiados en un plazo máximo de 7 días. Herramientas recomendadas: Google Authenticator (gratuito), Duo Security ($3/usuario/mes) o Azure MFA (incluido en M365).  
**Marco de referencia:** NIST SP 800-63B, ISO 27001 A.9.4.2  
**Costo estimado:** $0 - $750/mes  
**Reducción de riesgo esperada:** R-001 (fuerza bruta) reduciría de 17.5 a 3.5 (80% de reducción)

### Recomendación 2: Resolver Incidente Activo IR-2026-0502

**Hallazgo:** Exfiltración de 2GB de datos de clientes — incidente activo sin resolver.  
**Recomendación:** Activar el procedimiento de respuesta a brechas de datos: contener, investigar, notificar a la SIB (Superintendencia de Bancos) en 72 horas según Decreto 19-2002, notificar a clientes afectados.  
**Marco de referencia:** NIST SP 800-61r2 — Fase de Notificación  
**Acciones urgentes:** Contratar servicios de monitoreo de identidad para los 52,000 clientes potencialmente afectados.

### Recomendación 3: Programa Formal PCI-DSS v4.0

**Hallazgo:** Cumplimiento actual del 55% — el mínimo requerido es 100% bajo pena de multas y pérdida de la licencia de procesamiento de pagos.  
**Recomendación:** Contratar un QSA (Qualified Security Assessor) certificado para iniciar el proceso de auditoría PCI-DSS formal. Establecer un roadmap de 90 días con hitos mensuales medibles.  
**Costo estimado:** $15,000 - $30,000 USD (auditoría formal)  
**Riesgo de no actuar:** Multas de $5,000 - $100,000 USD/mes + pérdida de licencia Visa/Mastercard

### Recomendación 4: Elevar Cobertura ISO 27001

**Hallazgo:** Cobertura actual del 78% — meta del 85%.  
**Recomendación:** Realizar un análisis GAP formal de los controles del Anexo A de ISO 27001:2022 para identificar los 7 dominios no cubiertos. Priorizar: A.8 (Gestión de activos), A.12 (Operaciones), A.16 (Gestión de incidentes).  
**Plazo:** 60 días para Plan de Tratamiento; 12-18 meses para certificación.

### Recomendación 5: Capacitación en Ciberseguridad

**Hallazgo:** Riesgo R-006 (Phishing) tiene efectividad de control del 20% — sin programa formal de capacitación.  
**Recomendación:** Implementar programa de concientización trimestral con simulaciones de phishing reales. KPI objetivo: reducir tasa de clic en phishing simulado del estimado 35% actual al 5% en 6 meses.  
**Herramientas:** KnowBe4, Proofpoint Security Awareness (desde $20/usuario/año)  
**Marco de referencia:** NIST SP 800-50, CIS Control 14

### Recomendación 6: Automatización del SOC

**Hallazgo:** Algunos procesos de respuesta (bloqueo de IPs, escalamiento de tickets) aún son manuales.  
**Recomendación:** Implementar un SOAR (Security Orchestration, Automation and Response) básico. En etapa inicial, automatizar con scripts Python los playbooks más frecuentes. En etapa avanzada, evaluar TheHive + Cortex (OSS gratuito) como plataforma SOAR.  
**Beneficio esperado:** Reducir MTTR de 14 min a 5 min mediante respuesta automatizada.

---

## Tabla Resumen de Recomendaciones (Excel-Ready)

| ID | Recomendación | Prioridad | Responsable | Plazo | Costo USD | KPI/KRI Impactado | Reducción de Riesgo |
|---|---|---|---|---|---|---|---|
| REC-01 | Implementar MFA en 100% usuarios privilegiados | CRÍTICA | Cloud Admin | 7 días | $0-750/mes | KRI-08 | -80% R-001 |
| REC-02 | Resolver IR-2026-0502 y notificar regulador | CRÍTICA | CISO + DFIR | Inmediato | $50,000 | KRI-04 | Contener brecha |
| REC-03 | Iniciar programa PCI-DSS v4.0 | ALTA | GRC Manager | 90 días | $30,000 | KRI-07 | Cumplimiento 100% |
| REC-04 | Elevar cobertura ISO 27001 al 85% | ALTA | GRC Manager | 60 días | $5,000 | KRI-06 | +7% cobertura |
| REC-05 | Programa capacitación phishing trimestral | MEDIA | RRHH + CISO | 60 días | $20/user/año | KPI-07 | -70% R-006 |
| REC-06 | Implementar SOAR básico (TheHive) | MEDIA | SOC Lead | 30 días | $0 OSS | KPI-01 MTTR | -65% tiempo resp. |

---

*Documento generado como parte de la Tarea Semana 5 — GRC | Universidad Mariano Gálvez de Guatemala*
