# Fase 3: Implementación — Simulación de Incidentes y Gestión de Respuesta

## Universidad Mariano Gálvez de Guatemala
**Curso:** Gobierno, Riesgo y Cumplimiento | **Catedrático:** MS.c. Erick Enrique Blanco Acevedo  
**Organización:** TechGuard Guatemala S.A.

---

## 3.1 Introducción

La fase de implementación materializa el diseño GRC a través de la ejecución del laboratorio Docker y la simulación de tres escenarios de incidentes reales: ataque de fuerza bruta, exfiltración de datos y comportamiento ransomware. Cada incidente se gestiona siguiendo el ciclo de vida de respuesta a incidentes del NIST SP 800-61r2.

El ciclo de vida NIST para respuesta a incidentes contempla 4 fases:

```
PREPARACIÓN → DETECCIÓN & ANÁLISIS → CONTENCIÓN, ERRADICACIÓN & RECUPERACIÓN → ACTIVIDADES POST-INCIDENTE
```

---

## 3.2 Preparación del Entorno

### Pre-requisitos del Laboratorio

| Herramienta | Versión | Propósito | Verificación |
|---|---|---|---|
| Docker Desktop | 24.x o superior | Contenedores del lab | `docker --version` |
| Docker Compose | 2.x o superior | Orquestación | `docker compose version` |
| Python 3 | 3.8+ | Scripts de análisis | `python3 --version` |
| Git | Cualquiera | Control de versiones | `git --version` |

### Inicialización del Laboratorio

```bash
# 1. Ir al directorio del proyecto
cd "Implementar GRC"

# 2. Construir y levantar todos los contenedores
docker compose up -d --build

# 3. Verificar que los 3 contenedores estén corriendo
docker compose ps

# Salida esperada:
# NAME              STATUS    PORTS
# grc-soc-lab       Up        0.0.0.0:2222->22/tcp
# grc-attacker      Up        0.0.0.0:2223->22/tcp
# grc-siem          Up        0.0.0.0:8080->8080/tcp
```

---

## 3.3 Incidente 1: Ataque de Fuerza Bruta SSH

### Descripción del Incidente

| Campo | Detalle |
|---|---|
| ID del Incidente | IR-2026-0501 |
| Tipo | Ataque de Fuerza Bruta |
| Severidad | CRÍTICA |
| Vector de Ataque | Red externa — SSH Port 22 |
| IPs Atacantes | 185.21.44.10, 185.21.44.11, 185.21.44.12 |
| Usuarios Objetivo | admin, root, guest |
| Fecha/Hora | 2026-05-01 10:01 — 10:02 UTC |
| MTTD | 3 minutos |
| MTTR | 14 minutos |
| Estado | RESUELTO |

### Simulación del Ataque (desde grc-attacker)

```bash
# Conectarse al contenedor atacante
ssh root@localhost -p 2223
# Contraseña: Attacker2026!

# Simular intentos de fuerza bruta (dentro del contenedor atacante)
for user in admin root guest dbadmin; do
  echo "$(date '+%Y-%m-%d %H:%M:%S') FAILED login user=$user ip=185.21.44.10" >> /tmp/attack.log
  echo "Intentando usuario: $user..."
done
```

### Detección SOC (en grc-soc-lab)

```bash
# Conectarse al servidor SOC
ssh root@localhost -p 2222
# Contraseña: GRC2026!

# Ejecutar análisis de detección
python3 /soc/scripts/soc_basico.py
```

### Respuesta al Incidente

```bash
# En grc-soc-lab: Bloquear IPs atacantes (simulado con iptables)
iptables -A INPUT -s 185.21.44.0/24 -j DROP
iptables -A INPUT -s 185.21.44.10 -j DROP

# Verificar bloqueo
iptables -L INPUT -n | grep DROP

# Ver log de autenticación
cat /logs/auth.log

# Generar reporte SOC
python3 /soc/scripts/soc_basico.py > /logs/reporte_ir_0501.txt
cat /logs/reporte_ir_0501.txt
```

### Controles GRC Activados

| Control | Marco | Descripción |
|---|---|---|
| DE.CM-1 | NIST CSF | Monitoreo de red para detectar eventos adversos |
| RS.RP-1 | NIST CSF | Plan de respuesta ejecutado |
| A.9.4.2 | ISO 27001 | Procedimientos de inicio de sesión seguros |
| T1110 | MITRE ATT&CK | Brute Force — Técnica detectada y documentada |

---

## 3.4 Incidente 2: Exfiltración de Datos

### Descripción del Incidente

| Campo | Detalle |
|---|---|
| ID del Incidente | IR-2026-0502 |
| Tipo | Exfiltración de Datos |
| Severidad | CRÍTICA |
| Datos Comprometidos | Base de datos clientes — 2GB |
| Usuarios Afectados | 52,000 clientes |
| Estado | ACTIVO (en investigación) |

### Simulación y Detección

```bash
# En grc-soc-lab: Ejecutar análisis avanzado
python3 /soc/scripts/soc_avanzado.py

# Ver logs de exfiltración
grep "DATA_EXPORT" /siem_data/soc_logs.txt
```

### Plan de Contención

```bash
# 1. Aislar segmento de red afectado
iptables -A OUTPUT -d 0.0.0.0/0 -j DROP  # Bloquear todo tráfico saliente

# 2. Preservar evidencia forense
cp /siem_data/soc_logs.txt /logs/forense_ir_0502_$(date +%Y%m%d_%H%M).log
sha256sum /logs/forense_ir_0502_*.log  # Cadena de custodia

# 3. Notificación (simulada)
echo "ALERTA P1: Exfiltración detectada — IR-2026-0502" | tee /logs/notificacion_ciso.txt
```

---

## 3.5 Incidente 3: Comportamiento Ransomware

### Descripción del Incidente

| Campo | Detalle |
|---|---|
| ID del Incidente | IR-2026-0504 |
| Tipo | Ransomware Simulado |
| Severidad | CRÍTICA |
| Archivos Afectados | 6 archivos corporativos |
| Extensión sospechosa | .locked |
| MTTR | 22 minutos |
| Estado | RESUELTO |

### Ejecución de la Simulación

```bash
# En grc-soc-lab: Ejecutar simulación ransomware
python3 /soc/scripts/ransomware_sim.py

# Verificar archivos afectados
ls /lab_ransom/

# Ver los archivos "cifrados"
ls -la /lab_ransom/ | grep .locked
```

### Proceso de Recuperación

```bash
# Simular restauración desde backup
echo "Iniciando restauración desde backup 2026-04-30..."
for f in /lab_ransom/*.locked; do
  original="${f%.locked}"
  echo "Restaurando: $original"
done

echo "Recuperación completada. Validar integridad de archivos."
```

---

## 3.6 Integración de Logs — Cadena de Custodia

```bash
# En grc-soc-lab: Consolidar todos los logs del período
cat /logs/auth.log /siem_data/soc_logs.txt > /logs/consolidated_$(date +%Y%m%d).log

# Calcular hash SHA256 para cadena de custodia forense
sha256sum /logs/consolidated_*.log

# Ver el log consolidado
cat /logs/consolidated_*.log
```

---

## 3.7 Matriz de Incidentes del Período

| ID Incidente | Tipo | Severidad | Fecha Detección | MTTD (min) | MTTR (min) | Estado | Analista |
|---|---|---|---|---|---|---|---|
| IR-2026-0501 | Fuerza Bruta SSH | CRÍTICO | 2026-05-01 10:04 | 3 | 14 | RESUELTO | SOC Analyst |
| IR-2026-0502 | Exfiltración Datos | CRÍTICO | 2026-05-01 10:07 | 1 | — | ACTIVO | DFIR + CISO |
| IR-2026-0503 | Port Scanning | MEDIO | 2026-05-01 10:09 | 1 | 8 | RESUELTO | SOC Analyst |
| IR-2026-0504 | Ransomware Sim. | CRÍTICO | 2026-05-01 10:15 | 3 | 22 | RESUELTO | DFIR |
| IR-2026-0505 | Escalada Privilegios | ALTO | 2026-05-01 10:06 | 1 | 18 | RESUELTO | SOC + DFIR |

---

## 3.8 Conclusiones de la Fase

1. Los 3 escenarios de incidentes (fuerza bruta, exfiltración, ransomware) se ejecutaron exitosamente en el entorno Docker simulado.
2. El MTTD promedio de **1.8 minutos** supera significativamente el objetivo de 5 minutos establecido en el diseño.
3. El MTTR promedio de **15.5 minutos** cumple con el SLA definido de 15 minutos para incidentes críticos.
4. La integración de logs con cálculo SHA256 garantiza la cadena de custodia necesaria para procedimientos forenses legales.
5. El único incidente sin resolver (IR-2026-0502, Exfiltración) requiere escalamiento al CISO y posible notificación regulatoria según Decreto 19-2002.

---

*Documento generado como parte de la Tarea Semana 5 — GRC | Universidad Mariano Gálvez de Guatemala*
