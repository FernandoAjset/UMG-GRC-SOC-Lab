# Fase 1: Planeación y Análisis — Modelo GRC TechGuard Guatemala

## Universidad Mariano Gálvez de Guatemala
**Curso:** Gobierno, Riesgo y Cumplimiento  
**Catedrático:** MS.c. Erick Enrique Blanco Acevedo  
**Tarea:** Semana 5 — Implementación de un Modelo GRC con Enfoque Tecnológico y SOC Simulado  
**Organización caso de estudio:** TechGuard Guatemala S.A.

---

## 1.1 Introducción

El Gobierno, Riesgo y Cumplimiento (GRC, por sus siglas en inglés: Governance, Risk and Compliance) representa un enfoque integrado para alinear la tecnología de la información con los objetivos estratégicos de una organización, gestionar los riesgos de forma proactiva y garantizar el cumplimiento de marcos normativos, legales y regulatorios aplicables.

En la era digital actual, las organizaciones guatemaltecas enfrentan amenazas cibernéticas en constante evolución. La implementación de un modelo GRC funcional no solo protege los activos de información, sino que también fortalece la confianza de los stakeholders y reduce el riesgo residual a niveles aceptables.

Este documento desarrolla la **Fase 1: Planeación y Análisis** para la empresa ficticia **TechGuard Guatemala S.A.**, una fintech que procesa transacciones financieras para más de 50,000 clientes en Centroamérica.

---

## 1.2 Descripción del Caso de Negocio

### Organización: TechGuard Guatemala S.A.

| Campo | Detalle |
|---|---|
| Nombre | TechGuard Guatemala S.A. |
| Sector | Fintech / Servicios Financieros |
| Ubicación | Ciudad de Guatemala, Zona 10 |
| Empleados | 250 colaboradores |
| Clientes activos | 52,000 usuarios |
| Infraestructura | Servidores on-premise + Cloud (AWS) |
| Regulación aplicable | Ley de Bancos y Grupos Financieros (Decreto 19-2002), PCI-DSS v4.0 |
| Nivel de madurez GRC inicial | 1.5 / 5 (Inicial-Repetible) |

### Descripción del Problema

TechGuard Guatemala S.A. ha experimentado en los últimos 6 meses:

- **3 incidentes de seguridad** documentados (fuerza bruta, exfiltración de datos, acceso no autorizado)
- **Tiempo de detección promedio (MTTD):** 48 horas (meta: 5 minutos)
- **Tiempo de respuesta promedio (MTTR):** 72 horas (meta: 15 minutos)
- **Cumplimiento PCI-DSS:** 45% (mínimo requerido: 100%)
- **Sin un SOC formal** establecido

El directorio ha mandatado la implementación de un modelo GRC en 5 días para reducir el riesgo residual por debajo del 20% y elevar el cumplimiento normativo al 80% como primer hito.

---

## 1.3 Evaluación de Madurez GRC (Modelo CMM Adaptado)

La evaluación de madurez GRC utiliza el modelo CMMI (Capability Maturity Model Integration) adaptado a ciberseguridad, con escala del 1 al 5:

| Nivel | Nombre | Descripción |
|---|---|---|
| 1 | Inicial | Procesos ad-hoc, sin documentación formal |
| 2 | Repetible | Procesos básicos definidos pero no estandarizados |
| 3 | Definido | Procesos documentados, estandarizados y comunicados |
| 4 | Gestionado | Métricas definidas, monitoreo continuo |
| 5 | Optimizado | Mejora continua, innovación proactiva |

### Tabla de Evaluación de Madurez por Dominio

| Dominio GRC | Madurez Actual | Madurez Objetivo | Brecha | Prioridad |
|---|---|---|---|---|
| Gobierno de Seguridad | 1 | 3 | 2 niveles | ALTA |
| Gestión de Riesgos | 2 | 4 | 2 niveles | ALTA |
| Cumplimiento Normativo | 1 | 3 | 2 niveles | ALTA |
| Gestión de Incidentes | 1 | 4 | 3 niveles | CRÍTICA |
| Monitoreo y Detección (SOC) | 1 | 4 | 3 niveles | CRÍTICA |
| Gestión de Vulnerabilidades | 2 | 3 | 1 nivel | MEDIA |
| Continuidad del Negocio (BCP) | 1 | 3 | 2 niveles | ALTA |
| Concienciación en Seguridad | 2 | 3 | 1 nivel | MEDIA |
| Control de Acceso e Identidad | 2 | 4 | 2 niveles | ALTA |
| Seguridad en la Nube | 1 | 3 | 2 niveles | ALTA |
| **PROMEDIO** | **1.4** | **3.4** | **2.0** | — |

> **Interpretación:** TechGuard Guatemala se encuentra en un nivel de madurez INICIAL-REPETIBLE (1.4/5). La brecha promedio de 2 niveles requiere una hoja de ruta de 12-18 meses. La tarea de semana 5 aborda la implementación del hito 1.

---

## 1.4 Definición de Roles del Equipo GRC

### Estructura Organizativa del SOC

| Rol | Responsabilidades | Nivel de Acceso |
|---|---|---|
| **CISO** (Chief Information Security Officer) | Dirección estratégica de seguridad, reporte al directorio, aprobación de presupuesto | Nivel 5 — Máximo |
| **SOC Analyst** (Analista SOC) | Monitoreo continuo de alertas, triaje de incidentes, análisis de logs | Nivel 3 — Operativo |
| **DFIR Investigator** (Digital Forensics & Incident Response) | Investigación forense digital, análisis de malware, cadena de custodia | Nivel 4 — Especialista |
| **Cloud Admin** (Administrador Cloud) | Gestión de infraestructura cloud, seguridad en AWS/GCP, IAM | Nivel 4 — Especialista |
| **GRC Manager** | Cumplimiento normativo, auditorías, gestión de políticas | Nivel 3 — Operativo |

### Matriz RACI del Equipo GRC

| Actividad | CISO | SOC Analyst | DFIR Inv. | Cloud Admin | GRC Manager |
|---|---|---|---|---|---|
| Definir política de seguridad | R | C | C | C | A |
| Monitorear alertas SOC | I | R | C | I | I |
| Responder a incidentes P1 | A | R | R | C | I |
| Investigación forense | A | C | R | C | I |
| Auditoría de cumplimiento | A | I | I | C | R |
| Gestión de vulnerabilidades | A | R | C | R | C |
| Reportes al directorio | R | I | I | I | C |

> **R:** Responsable | **A:** Aprobador | **C:** Consultado | **I:** Informado

---

## 1.5 Marcos de Referencia Seleccionados

Para la implementación del modelo GRC de TechGuard Guatemala, se adoptaron los siguientes marcos:

| Marco | Aplicación | Dominio |
|---|---|---|
| **NIST CSF v2.0** | Marco principal de ciberseguridad (Identificar, Proteger, Detectar, Responder, Recuperar) | Integral |
| **ISO/IEC 27001:2022** | Sistema de Gestión de Seguridad de la Información (SGSI) | Gobierno y Cumplimiento |
| **MITRE ATT&CK** | Modelado de amenazas y TTPs de atacantes | Detección y Respuesta |
| **PCI-DSS v4.0** | Cumplimiento sectorial (procesamiento de pagos) | Cumplimiento |
| **COBIT 2019** | Gobierno TI y alineación con objetivos de negocio | Gobierno |

---

## 1.6 Cronograma del Proyecto (5 Días)

| Día | Fase | Actividades | Responsable |
|---|---|---|---|
| 1 | Planeación | Evaluación madurez, caso negocio, roles | Integrante 1 |
| 2 | Diseño | Arquitectura GRC, matriz de riesgos | Integrante 2 |
| 3 | Implementación | Docker lab, scripts, simulación incidentes | Integrante 3 |
| 4 | Herramientas | SIEM, análisis logs, ransomware sim | Integrante 4 |
| 5 | Monitoreo | KPIs, KRIs, dashboard, reporte final | Integrante 5 |

---

## 1.7 Conclusiones de la Fase

1. TechGuard Guatemala S.A. presenta un nivel de madurez GRC insuficiente (1.4/5) para las exigencias regulatorias del sector financiero guatemalteco.
2. La brecha más crítica se encuentra en Gestión de Incidentes y Monitoreo SOC, áreas que este laboratorio abordará directamente.
3. La definición clara de roles (CISO, SOC, DFIR, Cloud Admin) establece la base para una respuesta coordinada ante incidentes.
4. La adopción de NIST CSF como marco principal permite una implementación progresiva compatible con los recursos actuales de la organización.
5. El caso de negocio justifica la inversión en GRC al demostrar que el costo de no actuar (incidentes no detectados, multas regulatorias) supera el costo de implementación.

---

*Documento generado como parte de la Tarea Semana 5 — GRC | Universidad Mariano Gálvez de Guatemala*
