# Fase 5: Monitoreo — KPIs, KRIs y Mejora Continua

## Universidad Mariano Gálvez de Guatemala
**Curso:** Gobierno, Riesgo y Cumplimiento | **Catedrático:** MS.c. Erick Enrique Blanco Acevedo  
**Organización:** TechGuard Guatemala S.A.

---

## 5.1 Introducción

El monitoreo continuo es el componente que diferencia un modelo GRC activo de una documentación estática. Esta fase establece los indicadores clave de rendimiento (KPIs) y de riesgo (KRIs) que permiten medir la efectividad del SOC implementado, genera el reporte ejecutivo del período y define el plan de mejora continua basado en los resultados obtenidos.

El marco de monitoreo adoptado sigue la función **DETECTAR** del NIST CSF v2.0 y el ciclo PDCA (Plan-Do-Check-Act) para la mejora continua del SGSI según ISO 27001.

---

## 5.2 KPIs Operativos del SOC (Excel-Ready)

> Tabla diseñada para importar directamente a Excel. Fórmula de semáforo: Verde si Valor ≤ Meta, Rojo si supera.

| ID | KPI | Descripción | Valor Actual | Meta | Unidad | Tendencia | Estado | Frecuencia Medición |
|---|---|---|---|---|---|---|---|---|
| KPI-01 | MTTR | Mean Time To Respond — Tiempo promedio de respuesta a incidentes | 14 | 15 | minutos | ↓ Mejorando | CUMPLE ✅ | Diaria |
| KPI-02 | MTTD | Mean Time To Detect — Tiempo promedio de detección | 3 | 5 | minutos | ↓ Mejorando | CUMPLE ✅ | Diaria |
| KPI-03 | SLA Cumplimiento | % de incidentes resueltos dentro del SLA definido | 92 | 90 | % | → Estable | CUMPLE ✅ | Semanal |
| KPI-04 | Disponibilidad SOC | Uptime del SOC y sistemas de monitoreo | 99.8 | 99.5 | % | → Estable | CUMPLE ✅ | Mensual |
| KPI-05 | Tiempo forense | Tiempo promedio de análisis forense por incidente | 2.5 | 3 | horas | ↓ Mejorando | CUMPLE ✅ | Por incidente |
| KPI-06 | Falsos positivos | % de alertas SIEM que son falsos positivos | 12 | 10 | % | ↑ Empeorando | NO CUMPLE ⚠️ | Semanal |
| KPI-07 | Parches aplicados | % de vulnerabilidades críticas parcheadas en SLA | 87 | 95 | % | → Estable | NO CUMPLE ⚠️ | Quincenal |

---

## 5.3 KRIs de Riesgo (Excel-Ready)

| ID | KRI | Descripción | Valor Actual | Umbral Alerta | Umbral Crítico | Unidad | Estado | Acción Requerida |
|---|---|---|---|---|---|---|---|---|
| KRI-01 | % Detección incidentes | Porcentaje de incidentes reales detectados por el SOC | 85 | 75 | 60 | % | NORMAL ✅ | Mantener |
| KRI-02 | % Logs analizados | Porcentaje de logs procesados sobre total generado | 92 | 80 | 70 | % | NORMAL ✅ | Mantener |
| KRI-03 | Riesgo residual global | Nivel promedio de riesgo residual de la organización | 18 | 20 | 25 | % | NORMAL ✅ | Mantener |
| KRI-04 | Incidentes críticos activos | Número de incidentes P1 sin resolver | 1 | 0 | 2 | unidades | ALERTA ⚠️ | Resolver IR-0502 |
| KRI-05 | Vulnerabilidades críticas | CVEs críticos (CVSS > 9.0) sin parchear | 3 | 1 | 5 | unidades | ALERTA ⚠️ | Parchear en 72h |
| KRI-06 | Cobertura ISO 27001 | % de controles ISO 27001 implementados | 78 | 85 | 70 | % | ALERTA ⚠️ | Plan de remediación |
| KRI-07 | Cumplimiento PCI-DSS | % de requerimientos PCI-DSS v4.0 cumplidos | 55 | 80 | 50 | % | ALERTA ⚠️ | Prioridad CISO |
| KRI-08 | Usuarios sin MFA | % de usuarios privilegiados sin MFA activo | 45 | 10 | 30 | % | CRÍTICO 🔴 | Acción inmediata |
| KRI-09 | Backups verificados | % de backups verificados y restaurables | 95 | 90 | 80 | % | NORMAL ✅ | Mantener |

---

## 5.4 Reporte de Incidentes del Período (Excel-Ready)

| ID Incidente | Tipo de Incidente | Severidad | Fecha/Hora Ocurrencia | Fecha/Hora Detección | MTTD (min) | Fecha/Hora Resolución | MTTR (min) | Estado | Analista Responsable | Vector Inicial | Impacto | Costo Estimado USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IR-2026-0501 | Ataque Fuerza Bruta SSH | CRÍTICO | 2026-05-01 10:01 | 2026-05-01 10:04 | 3 | 2026-05-01 10:18 | 14 | RESUELTO | SOC Analyst | Red externa — IP 185.21.44.10 | Acceso intentado sin éxito final | $500 |
| IR-2026-0502 | Exfiltración de Datos | CRÍTICO | 2026-05-01 10:04 | 2026-05-01 10:05 | 1 | — | — | ACTIVO | DFIR + CISO | Post-compromiso credenciales | 2GB datos clientes potencialmente comprometidos | $250,000 |
| IR-2026-0503 | Port Scanning | MEDIO | 2026-05-01 10:08 | 2026-05-01 10:09 | 1 | 2026-05-01 10:17 | 8 | RESUELTO | SOC Analyst | Red externa — IP 92.168.1.200 | Reconocimiento de infraestructura | $0 |
| IR-2026-0504 | Ransomware Simulado | CRÍTICO | 2026-05-01 10:12 | 2026-05-01 10:15 | 3 | 2026-05-01 10:37 | 22 | RESUELTO | DFIR | Archivo malicioso ejecutado | 6 archivos corporativos afectados | $5,000 |
| IR-2026-0505 | Escalada de Privilegios | ALTO | 2026-05-01 10:05 | 2026-05-01 10:06 | 1 | 2026-05-01 10:24 | 18 | RESUELTO | SOC + DFIR | Acceso a /etc/passwd | Posible elevación de permisos | $2,000 |

### Resumen Ejecutivo de Incidentes

| Métrica | Valor |
|---|---|
| Total incidentes en el período | 5 |
| Incidentes CRÍTICOS | 3 |
| Incidentes RESUELTOS | 4 (80%) |
| Incidentes ACTIVOS | 1 (20%) |
| MTTD promedio | 1.8 minutos |
| MTTR promedio (resueltos) | 15.5 minutos |
| Costo estimado total | $257,500 USD |

---

## 5.5 Ejecución del Dashboard de Métricas

```bash
# Ejecutar dashboard en servidor SOC
ssh root@localhost -p 2222
# Contraseña: GRC2026!

python3 /soc/scripts/dashboard_grc.py

# Ver métricas exportadas en JSON
cat /siem_data/dashboard_metricas.json
```

---

## 5.6 Plan de Mejora Continua (PDCA)

### Plan (Planificar)

| Acción | Responsable | Plazo | KRI/KPI Asociado |
|---|---|---|---|
| Implementar MFA en 100% usuarios privilegiados | Cloud Admin | 7 días | KRI-08 |
| Resolver incidente IR-2026-0502 (Exfiltración) | DFIR + CISO | Inmediato | KRI-04 |
| Parchear 3 CVEs críticos pendientes | Cloud Admin + Dev | 72 horas | KRI-05 |
| Elevar cobertura ISO 27001 de 78% a 85% | GRC Manager | 60 días | KRI-06 |
| Iniciar programa cumplimiento PCI-DSS | CISO + GRC | 90 días | KRI-07 |
| Reducir falsos positivos SIEM de 12% a 10% | SOC Lead | 30 días | KPI-06 |

### Do (Hacer)

- Ejecutar laboratorio Docker en ambiente controlado ✅
- Simular los 3 escenarios de incidentes ✅
- Generar reportes SOC con métricas reales ✅
- Documentar cadena de custodia de logs ✅

### Check (Verificar)

- MTTR: 14 min vs meta 15 min → **CUMPLE** ✅
- MTTD: 3 min vs meta 5 min → **CUMPLE** ✅
- Detección incidentes: 85% vs meta 80% → **CUMPLE** ✅
- Riesgo residual: 18% vs meta 20% → **CUMPLE** ✅
- MFA usuarios privilegiados: 55% → **NO CUMPLE** ⚠️
- PCI-DSS: 55% → **NO CUMPLE** ⚠️

### Act (Actuar)

El ciclo de mejora continua establece las siguientes prioridades para el próximo período:

1. **Prioridad 1:** Resolver IR-2026-0502 y notificar a autoridades regulatorias
2. **Prioridad 2:** Implementar MFA inmediato (45% de usuarios privilegiados sin MFA)
3. **Prioridad 3:** Iniciar programa formal PCI-DSS (actualmente 55% — mínimo 100%)
4. **Prioridad 4:** Elevar cobertura ISO 27001 al 85% en 60 días

---

## 5.7 Evolución del Riesgo Residual (Antes vs Después del Lab)

| Dominio | Riesgo Pre-Lab | Riesgo Post-Lab | Reducción |
|---|---|---|---|
| Gestión de Incidentes | 22/25 | 8/25 | -64% |
| Monitoreo / Detección | 20/25 | 5/25 | -75% |
| Respuesta a Incidentes | 18/25 | 7/25 | -61% |
| Análisis Forense | 15/25 | 6/25 | -60% |
| Integración de Logs | 20/25 | 4/25 | -80% |
| **Promedio Global** | **19/25 (76%)** | **6/25 (24%)** | **-68%** |

---

## 5.8 Conclusiones de la Fase

1. El 80% de los KPIs operativos **cumplen** con las metas establecidas en el diseño, validando la efectividad del laboratorio.
2. Los 3 KRIs críticos que NO cumplen (KRI-04, KRI-05, KRI-08) están directamente relacionados con la madurez de controles preventivos, no detectivos — área a priorizar.
3. La reducción del riesgo residual promedio del **76% al 24%** representa una mejora del 68% en la postura de seguridad, superando el objetivo del 20% establecido.
4. El único incidente activo (IR-2026-0502, Exfiltración) requiere notificación a la SIB (Superintendencia de Bancos) dentro de las próximas 72 horas según el Decreto 19-2002.
5. El ciclo PDCA establece una hoja de ruta clara para la siguiente iteración del modelo GRC, con foco en MFA y cumplimiento PCI-DSS.

---

*Documento generado como parte de la Tarea Semana 5 — GRC | Universidad Mariano Gálvez de Guatemala*
