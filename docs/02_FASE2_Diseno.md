# Fase 2: Diseño — Arquitectura GRC y Gestión de Riesgos

## Universidad Mariano Gálvez de Guatemala
**Curso:** Gobierno, Riesgo y Cumplimiento | **Catedrático:** MS.c. Erick Enrique Blanco Acevedo  
**Organización:** TechGuard Guatemala S.A.

---

## 2.1 Introducción

El diseño del modelo GRC establece la arquitectura sobre la cual se construirá la capacidad de seguridad de TechGuard Guatemala S.A. Esta fase define el alcance, prioriza los riesgos mediante metodología cuantitativa y establece la arquitectura técnica del laboratorio SOC simulado, aplicando el principio de **defensa en profundidad**.

---

## 2.2 Alcance del Modelo GRC

### Activos en Alcance

| ID | Categoría | Activo | Criticidad | Propietario |
|---|---|---|---|---|
| A-001 | Datos | BD clientes (52,000 registros) | CRÍTICA | CISO |
| A-002 | Datos | Información financiera transaccional | CRÍTICA | CISO |
| A-003 | Datos | Credenciales de empleados | ALTA | IT Manager |
| A-004 | Sistemas | Servidor producción Ubuntu 22.04 | CRÍTICA | Cloud Admin |
| A-005 | Sistemas | Servidor BD MySQL | CRÍTICA | DBA |
| A-006 | Sistemas | Plataforma web / API REST | ALTA | Dev Lead |
| A-007 | Red | Infraestructura de red corporativa | ALTA | Network Admin |
| A-008 | Red | VPN de acceso remoto | ALTA | Cloud Admin |

---

## 2.3 Metodología de Evaluación de Riesgos

**Fórmula aplicada:**
```
Riesgo Inherente   = Probabilidad (1-5) × Impacto (1-5)
Riesgo Residual    = Riesgo Inherente × (1 - Efectividad del Control)
```

### Escala de Probabilidad

| Valor | Nivel | Frecuencia |
|---|---|---|
| 1 | Muy Baja | Una vez en 5 años |
| 2 | Baja | Una vez al año |
| 3 | Media | Una vez al trimestre |
| 4 | Alta | Una vez al mes |
| 5 | Muy Alta | Semanal o más |

### Escala de Impacto

| Valor | Nivel | Impacto Financiero |
|---|---|---|
| 1 | Mínimo | Sin impacto significativo |
| 2 | Menor | < $10,000 USD |
| 3 | Moderado | $10,000 - $100,000 USD |
| 4 | Mayor | $100,000 - $1,000,000 USD |
| 5 | Catastrófico | > $1,000,000 USD |

---

## 2.4 Matriz de Riesgos (Excel-Ready)

| ID | Amenaza | Categoría | Activo Afectado | Probabilidad | Impacto | Riesgo Inherente | Control Existente | Efectividad % | Riesgo Residual | Prioridad | Tratamiento |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-001 | Ataque fuerza bruta SSH | Acceso No Autorizado | Servidor producción | 5 | 5 | 25 | Contraseña compleja | 30 | 17.5 | CRÍTICO | Mitigar — MFA + fail2ban |
| R-002 | Exfiltración de BD clientes | Pérdida de Datos | BD MySQL | 4 | 5 | 20 | Firewall básico | 25 | 15.0 | CRÍTICO | Mitigar — DLP + cifrado |
| R-003 | Ransomware en servidores | Malware | Servidor producción | 3 | 5 | 15 | Antivirus básico | 40 | 9.0 | ALTO | Mitigar — EDR + backups |
| R-004 | Escalada de privilegios | Acceso No Autorizado | SO Linux | 3 | 4 | 12 | Gestión básica cuentas | 35 | 7.8 | ALTO | Mitigar — PAM + hardening |
| R-005 | Ataque DDoS web | Disponibilidad | API REST | 3 | 4 | 12 | Sin protección DDoS | 10 | 10.8 | ALTO | Mitigar — CDN + rate limit |
| R-006 | Phishing a empleados | Ingeniería Social | Credenciales | 5 | 3 | 15 | Sin capacitación formal | 20 | 12.0 | ALTO | Mitigar — Training + sim |
| R-007 | Vulnerabilidades CVE | Software | Aplicación web | 4 | 3 | 12 | Actualizaciones manuales | 50 | 6.0 | MEDIO | Mitigar — SAST/DAST |
| R-008 | Acceso físico CPD | Físico | Centro de datos | 2 | 4 | 8 | Tarjeta de acceso | 60 | 3.2 | MEDIO | Aceptar con controles |
| R-009 | Insider threat | Amenaza Interna | Datos clientes | 2 | 5 | 10 | Sin DLP | 20 | 8.0 | ALTO | Mitigar — DLP + monitoreo |
| R-010 | Fallo disponibilidad CPD | Continuidad | Infraestructura | 2 | 4 | 8 | Generador eléctrico | 50 | 4.0 | MEDIO | Mitigar — BCP/DRP |
| R-011 | Incumplimiento PCI-DSS | Cumplimiento | Proceso de pagos | 4 | 4 | 16 | Sin programa formal | 15 | 13.6 | CRÍTICO | Mitigar — Programa PCI |
| R-012 | Credenciales robadas | Acceso No Autorizado | Sistemas críticos | 3 | 4 | 12 | Sin MFA | 30 | 8.4 | ALTO | Mitigar — MFA obligatorio |

### Resumen por Nivel de Prioridad

| Prioridad | Cantidad | Riesgo Residual Promedio |
|---|---|---|
| CRÍTICO | 3 | 15.4 |
| ALTO | 6 | 9.2 |
| MEDIO | 3 | 4.4 |
| **TOTAL** | **12** | **9.3** |

---

## 2.5 Arquitectura del Laboratorio GRC (Docker)

```
┌───────────────────────────────────────────────────────┐
│           Red Docker: grc-net (172.20.0.0/24)         │
│                                                       │
│  ┌────────────────┐   Logs   ┌────────────────────┐  │
│  │ grc-soc-lab    │─────────▶│ grc-siem           │  │
│  │ Ubuntu 22.04   │          │ SIEM Python+Flask  │  │
│  │ 172.20.0.10    │          │ 172.20.0.30 :8080  │  │
│  │ SSH :2222      │          └────────────────────┘  │
│  └────────┬───────┘                                   │
│           │ Detecta                                   │
│  ┌────────▼───────┐                                   │
│  │ grc-attacker   │                                   │
│  │ Alpine 3.18    │                                   │
│  │ 172.20.0.20    │                                   │
│  │ SSH :2223      │                                   │
│  └────────────────┘                                   │
└───────────────────────────────────────────────────────┘
```

### Capas de Control — Defensa en Profundidad

| Capa | Tecnología | Control |
|---|---|---|
| Perímetro | Firewall simulado | Bloqueo de IPs atacantes |
| Red | Segmentación Docker | Red aislada 172.20.0.0/24 |
| Host | Ubuntu Hardening | fail2ban, SSH config segura |
| Aplicación | Scripts Python | Detección de anomalías |
| Datos | Logs con integridad | Cadena de custodia SHA256 |
| Monitoreo | SIEM Python | Correlación y alertas automáticas |
| Respuesta | SOC Dashboard | Playbooks de respuesta |

---

## 2.6 Plan de Tratamiento de Riesgos

| Riesgo | Estrategia | Acción | Responsable | Plazo | Costo Estimado |
|---|---|---|---|---|---|
| R-001 Fuerza Bruta | Mitigar | MFA + fail2ban | Cloud Admin | Inmediato | $0 OSS |
| R-002 Exfiltración BD | Mitigar | Cifrado BD + DLP | CISO + DBA | 30 días | $2,000/mes |
| R-003 Ransomware | Mitigar | EDR + backups diarios | Cloud Admin | 15 días | $500/mes |
| R-004 Escalada priv. | Mitigar | PAM + mínimo privilegio | Cloud Admin | 30 días | $1,000/mes |
| R-005 DDoS | Mitigar | WAF + rate limiting | Dev Lead | 15 días | $200/mes |
| R-006 Phishing | Mitigar | Capacitación + simulaciones | GRC Manager | 60 días | $300/mes |
| R-011 PCI-DSS | Mitigar | Programa cumplimiento formal | GRC Manager | 90 días | $5,000 |

---

## 2.7 Conclusiones de la Fase

1. Se identificaron **12 riesgos**, de los cuales **3 son críticos** y requieren acción inmediata (R-001, R-002, R-011).
2. El riesgo residual promedio actual es **9.3/25** (37%); con los controles propuestos bajaría a **~4.5/25** (18%), cumpliendo el objetivo del 20%.
3. La arquitectura de 3 contenedores Docker permite simular un entorno SOC real con costo operativo cero.
4. La adopción de NIST CSF como capa de control brinda trazabilidad de cada amenaza a un control específico y verificable.

---

*Documento generado como parte de la Tarea Semana 5 — GRC | Universidad Mariano Gálvez de Guatemala*
