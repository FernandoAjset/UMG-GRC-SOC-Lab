# Fase 4: Herramientas — Docker Lab, SIEM Simulado y Scripts de Análisis

## Universidad Mariano Gálvez de Guatemala
**Curso:** Gobierno, Riesgo y Cumplimiento | **Catedrático:** MS.c. Erick Enrique Blanco Acevedo  
**Organización:** TechGuard Guatemala S.A.

---

## 4.1 Introducción

La fase de herramientas documenta el laboratorio técnico completo: la infraestructura Docker con sus 3 contenedores, los 5 scripts Python de análisis SOC, el motor SIEM simulado con correlación de eventos y el dashboard web de monitoreo. Esta fase es el núcleo práctico de la tarea.

---

## 4.2 Infraestructura Docker — 3 Contenedores

### Credenciales y Accesos por Contenedor

| Contenedor | Imagen | IP | Puerto | Usuario | Contraseña | Rol |
|---|---|---|---|---|---|---|
| `grc-soc-lab` | Ubuntu 22.04 | 172.20.0.10 | SSH: 2222 | root | GRC2026! | Servidor SOC Principal |
| `grc-soc-lab` | Ubuntu 22.04 | 172.20.0.10 | SSH: 2222 | student | Student2026! | Usuario de práctica |
| `grc-attacker` | Alpine 3.18 | 172.20.0.20 | SSH: 2223 | root | Attacker2026! | Nodo Atacante Simulado |
| `grc-siem` | Python 3.11 | 172.20.0.30 | HTTP: 8080 | — | — | Dashboard SIEM Web |

### Comandos de Conexión SSH

```bash
# ── Servidor SOC Principal (usuario root)
ssh root@localhost -p 2222
# Contraseña: GRC2026!

# ── Servidor SOC Principal (usuario estudiante)
ssh student@localhost -p 2222
# Contraseña: Student2026!

# ── Nodo Atacante Simulado
ssh root@localhost -p 2223
# Contraseña: Attacker2026!

# ── Dashboard SIEM (navegador web)
# Abrir: http://localhost:8080
# APIs: http://localhost:8080/api/status
#       http://localhost:8080/api/alerts
#       http://localhost:8080/api/metrics
```

---

## 4.3 Comandos de Gestión del Laboratorio

```bash
# ── LEVANTAR EL LABORATORIO COMPLETO
docker compose up -d --build

# ── VER ESTADO DE CONTENEDORES
docker compose ps

# ── VER LOGS EN TIEMPO REAL
docker compose logs -f

# ── ACCEDER A UN CONTENEDOR DIRECTAMENTE
docker exec -it grc-soc-lab bash
docker exec -it grc-attacker sh
docker exec -it grc-siem bash

# ── DETENER EL LABORATORIO
docker compose down

# ── REINICIAR UN CONTENEDOR ESPECÍFICO
docker compose restart grc-soc-lab

# ── VER RECURSOS UTILIZADOS
docker stats --no-stream

# ── LIMPIAR COMPLETAMENTE EL ENTORNO
docker compose down -v --remove-orphans
docker system prune -f
```

---

## 4.4 Scripts del Laboratorio — Guía de Ejecución

### Estructura de Archivos

```
Implementar GRC/
├── docker-compose.yml          # Orquestación Docker
├── Dockerfile.soc              # Imagen Ubuntu SOC
├── scripts/
│   ├── soc_basico.py           # Módulo 1: Detección fuerza bruta
│   ├── soc_avanzado.py         # Módulo 2: Análisis multi-amenaza
│   ├── ransomware_sim.py       # Módulo 3: Simulación ransomware
│   ├── siem_simulado.py        # Módulo 4: Motor SIEM correlación
│   ├── dashboard_grc.py        # Módulo 5: KPIs / KRIs dashboard
│   └── siem_dashboard_web.py   # Módulo 6: Dashboard web Flask
├── logs/                       # Logs de autenticación
├── siem_data/                  # Logs SOC avanzados y JSON exports
└── lab_ransom/                 # Archivos para simulación ransomware
```

### Ejecución Local (sin Docker)

```bash
# Ir al directorio del proyecto
cd "Implementar GRC"

# ── Módulo 1: SOC Básico
python3 scripts/soc_basico.py

# ── Módulo 2: SOC Avanzado
python3 scripts/soc_avanzado.py

# ── Módulo 3: Ransomware Simulado
python3 scripts/ransomware_sim.py

# ── Módulo 4: SIEM Motor de Correlación
python3 scripts/siem_simulado.py

# ── Módulo 5: Dashboard KPIs/KRIs
python3 scripts/dashboard_grc.py

# ── Módulo 6: Dashboard Web (sin dependencias externas)
python3 scripts/siem_dashboard_web.py
# Luego abrir: http://localhost:8080

# Si el puerto 8080 está ocupado:
python3 scripts/siem_dashboard_web.py 8081
```

### Ejecución Dentro de Docker

```bash
# Conectarse al servidor SOC
ssh root@localhost -p 2222
# Contraseña: GRC2026!

# Ejecutar todos los módulos en secuencia
python3 /soc/scripts/soc_basico.py
python3 /soc/scripts/soc_avanzado.py
python3 /soc/scripts/ransomware_sim.py
python3 /soc/scripts/siem_simulado.py
python3 /soc/scripts/dashboard_grc.py

# Ver archivos generados
ls -la /logs/
ls -la /siem_data/
ls -la /lab_ransom/

# Ver reporte JSON del SIEM
cat /siem_data/alertas_siem.json

# Ver métricas exportadas
cat /siem_data/dashboard_metricas.json
```

---

## 4.5 Módulo SIEM — Reglas de Correlación

El motor SIEM implementado simula el funcionamiento de Wazuh/Splunk con las siguientes reglas:

| Rule ID | Nombre | Condición de Disparo | Severidad | MITRE | NIST |
|---|---|---|---|---|---|
| GRC-1001 | Ataque Fuerza Bruta | LOGIN_FAIL > 2 en misma sesión | CRÍTICO | T1110 | DE.CM-1 |
| GRC-1002 | Acceso Archivos Sistema | FILE_ACCESS con /etc/passwd | ALTO | T1083 | DE.CM-7 |
| GRC-1003 | Exfiltración de Datos | DATA_EXPORT > 0 | CRÍTICO | T1048 | PR.DS-5 |
| GRC-1004 | Port Scanning | PORT_SCAN detectado | MEDIO | T1046 | DE.CM-1 |
| GRC-1099 | Kill Chain Completo | Fuerza Bruta + Exfiltración correlacionados | CRÍTICO | Múltiples | RS.RP-1 |

### Acciones Automatizadas del SIEM

| Alerta | Acción Automatizada | Destinatario |
|---|---|---|
| GRC-1001 | Bloqueo IP + ticket ServiceDesk | SOC Analyst |
| GRC-1002 | Snapshot del sistema + alerta | DFIR Investigator |
| GRC-1003 | Aislamiento de red + escalamiento P1 | CISO |
| GRC-1004 | Actualización reglas firewall | Cloud Admin |
| GRC-1099 | Activar IR Plan + notificar directorio | CISO + Directorio |

---

## 4.6 Módulo Ransomware — Indicadores de Compromiso (IoCs)

| Indicador | Tipo | Valor | Descripción |
|---|---|---|---|
| `.locked` | Extensión de archivo | *.locked | Extensión añadida por ransomware simulado |
| Velocidad de cambio | Comportamiento | >2 archivos/seg | Modificación masiva anómala |
| Patrón de archivos | Comportamiento | Todos los archivos del directorio | Cifrado indiscriminado |
| Proceso sospechoso | Sistema | python3 ransomware_sim.py | Proceso generador (en lab) |

### Relación MITRE ATT&CK — Técnicas Simuladas

| Táctica | Técnica ID | Nombre | Simulada en |
|---|---|---|---|
| Initial Access | T1190 | Exploit Public-Facing Application | Fuerza bruta SSH |
| Credential Access | T1110 | Brute Force | soc_basico.py |
| Discovery | T1083 | File and Directory Discovery | soc_avanzado.py |
| Discovery | T1046 | Network Service Discovery | Port scan en logs |
| Exfiltration | T1048 | Exfiltration Over Alt Protocol | soc_avanzado.py |
| Impact | T1486 | Data Encrypted for Impact | ransomware_sim.py |

---

## 4.7 Dashboard Web SIEM (http://localhost:8080)

El dashboard web expone 4 endpoints REST con librería estándar de Python:

```bash
# Estado general del SOC
curl http://localhost:8080/api/status

# Lista de alertas activas
curl http://localhost:8080/api/alerts

# Métricas KPIs/KRIs
curl http://localhost:8080/api/metrics

# Vista ejecutiva consolidada
curl http://localhost:8080/api/executive

# Generar nuevo periodo SOC simulado y refrescar datos
curl -X POST http://localhost:8080/api/simulate
```

### Respuesta de ejemplo — /api/status

```json
{
  "status": "OPERATIONAL",
  "timestamp": "2026-05-14T17:30:00",
  "soc": "TechGuard Guatemala S.A.",
  "period": "Mayo 2026",
  "events_analyzed": 288,
  "active_alerts": 5,
  "critical_open": 1,
  "mttr_min": 14,
  "mttd_min": 3,
  "sla_compliance": 92,
  "availability": 99.8,
  "residual_risk_pct": 18,
  "financial_exposure_usd": 257500
}
```

---

## 4.8 Conclusiones de la Fase

1. El laboratorio Docker de 3 contenedores replica fielmente un entorno SOC real con costo operativo cero.
2. Los 5 scripts Python implementan detección progresiva: desde fuerza bruta básica hasta correlación de Kill Chain completo.
3. El motor SIEM con 5 reglas de correlación (GRC-1001 a GRC-1099) permite detectar todos los escenarios del PDF original.
4. La técnica más avanzada detectada es el **Kill Chain (GRC-1099)**: correlación automática de fuerza bruta + acceso exitoso + exfiltración de datos.
5. El dashboard web REST proporciona una interfaz de monitoreo en tiempo real, equivalente conceptualmente a Splunk o Wazuh.

---

*Documento generado como parte de la Tarea Semana 5 — GRC | Universidad Mariano Gálvez de Guatemala*
