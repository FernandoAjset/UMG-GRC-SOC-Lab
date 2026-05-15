#!/usr/bin/env python3
"""
=======================================================
MÓDULO 4: SIEM SIMULADO — Motor de Correlación de Eventos
GRC Semana 5 | Universidad Mariano Gálvez de Guatemala
=======================================================
Simula: Wazuh / Splunk — Correlación y Alertas Automáticas
"""

import os
import datetime
import json

SIEM_LOG = "/siem_data/soc_logs.txt"

# Fallback local
if not os.path.exists(SIEM_LOG):
    SIEM_LOG = os.path.join(os.path.dirname(__file__), "../siem_data/soc_logs.txt")
    os.makedirs(os.path.dirname(SIEM_LOG), exist_ok=True)
    with open(SIEM_LOG, "w") as f:
        f.write("2026-05-01 10:01 LOGIN_FAIL user=admin ip=185.21.44.10\n")
        f.write("2026-05-01 10:02 LOGIN_FAIL user=root ip=185.21.44.11\n")
        f.write("2026-05-01 10:03 LOGIN_FAIL user=admin ip=185.21.44.12\n")
        f.write("2026-05-01 10:04 LOGIN_SUCCESS user=admin ip=185.21.44.10\n")
        f.write("2026-05-01 10:05 FILE_ACCESS /etc/passwd user=admin\n")
        f.write("2026-05-01 10:06 DATA_EXPORT database=clients size=2GB\n")
        f.write("2026-05-01 10:07 LOGIN_FAIL user=dbadmin ip=10.0.0.55\n")
        f.write("2026-05-01 10:08 PORT_SCAN src=92.168.1.200 ports=22,80,443,3306\n")
        f.write("2026-05-01 10:09 MULTIPLE_ACCESS user=admin sessions=8\n")

logs = open(SIEM_LOG).readlines()

# ── Motor SIEM: parseo de eventos
failed_logins = [l for l in logs if "LOGIN_FAIL" in l]
file_changes  = [l for l in logs if "FILE_MODIFIED" in l or "FILE_ACCESS" in l]
data_exports  = [l for l in logs if "DATA_EXPORT" in l]
port_scans    = [l for l in logs if "PORT_SCAN" in l]

# Reglas de correlación (como Wazuh rules)
reglas_disparadas = []

# Regla 1001: Fuerza Bruta (>2 fallos en misma sesión)
if len(failed_logins) > 2:
    reglas_disparadas.append({
        "rule_id": "GRC-1001",
        "descripcion": "Ataque de Fuerza Bruta Detectado",
        "nivel": "CRÍTICO",
        "eventos": len(failed_logins),
        "mitre": "T1110 - Brute Force",
        "nist": "DE.CM-1",
        "iso": "A.9.4.2"
    })

# Regla 1002: Modificación archivos sistema
if len(file_changes) > 0:
    reglas_disparadas.append({
        "rule_id": "GRC-1002",
        "descripcion": "Acceso a Archivos Críticos del Sistema",
        "nivel": "ALTO",
        "eventos": len(file_changes),
        "mitre": "T1083 - File Discovery",
        "nist": "DE.CM-7",
        "iso": "A.12.4.1"
    })

# Regla 1003: Exfiltración de datos
if len(data_exports) > 0:
    reglas_disparadas.append({
        "rule_id": "GRC-1003",
        "descripcion": "Posible Exfiltración de Datos",
        "nivel": "CRÍTICO",
        "eventos": len(data_exports),
        "mitre": "T1048 - Exfiltration Over Alternative Protocol",
        "nist": "PR.DS-5",
        "iso": "A.12.4.1"
    })

# Regla 1004: Port Scanning
if len(port_scans) > 0:
    reglas_disparadas.append({
        "rule_id": "GRC-1004",
        "descripcion": "Escaneo de Puertos — Reconocimiento",
        "nivel": "MEDIO",
        "eventos": len(port_scans),
        "mitre": "T1046 - Network Service Discovery",
        "nist": "DE.CM-1",
        "iso": "A.13.1.1"
    })

# Regla 1099: CORRELACIÓN — Ataque en Cadena (Kill Chain)
if len(failed_logins) > 2 and len(data_exports) > 0:
    reglas_disparadas.append({
        "rule_id": "GRC-1099",
        "descripcion": "⚠️ KILL CHAIN DETECTADO: Fuerza Bruta → Acceso → Exfiltración",
        "nivel": "CRÍTICO",
        "eventos": len(failed_logins) + len(data_exports),
        "mitre": "Múltiples TTPs (Initial Access → Exfiltration)",
        "nist": "RS.RP-1",
        "iso": "A.16.1.5"
    })

# ── OUTPUT DASHBOARD SIEM
print()
print("╔══════════════════════════════════════════════════════════╗")
print("║          SIEM SIMULADO — MOTOR DE CORRELACIÓN           ║")
print("║     TechGuard Guatemala S.A. | SOC Operations Center    ║")
print(f"║     {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                               ║")
print("╠══════════════════════════════════════════════════════════╣")
print(f"║  Eventos recibidos:     {len(logs):<34}║")
print(f"║  Reglas evaluadas:      {150:<34}║")
print(f"║  Reglas disparadas:     {len(reglas_disparadas):<34}║")
print(f"║  Nivel de amenaza:      {'CRÍTICO' if any(r['nivel']=='CRÍTICO' for r in reglas_disparadas) else 'MEDIO':<34}║")
print("╠══════════════════════════════════════════════════════════╣")
print("║  ALERTAS ACTIVAS:                                        ║")
print("╠══════════════════════════════════════════════════════════╣")

for regla in reglas_disparadas:
    nivel_icon = "🔴" if regla["nivel"] == "CRÍTICO" else ("🟠" if regla["nivel"] == "ALTO" else "🟡")
    print(f"║  {nivel_icon} [{regla['rule_id']}] {regla['descripcion']:<39}║")
    print(f"║     Eventos: {regla['eventos']} | MITRE: {regla['mitre'][:30]:<30}║")
    print(f"║     NIST: {regla['nist']} | ISO 27001: {regla['iso']:<28}║")
    print("║                                                          ║")

print("╠══════════════════════════════════════════════════════════╣")
print("║  RESPUESTA AUTOMATIZADA SIEM:                            ║")
print("║  • Notificación enviada → CISO (escalamiento P1)        ║")
print("║  • Ticket IR-2026-0501 creado en ServiceDesk            ║")
print("║  • Log preservado para forensics (cadena de custodia)   ║")
print("║  • Bloqueo de IP 185.21.44.0/24 aplicado               ║")
print("╚══════════════════════════════════════════════════════════╝")
print()

# Exportar alertas como JSON (para dashboard)
alertas_json = {
    "timestamp": datetime.datetime.now().isoformat(),
    "organizacion": "TechGuard Guatemala S.A.",
    "total_eventos": len(logs),
    "alertas": reglas_disparadas
}

output_file = "/siem_data/alertas_siem.json"
if not os.path.exists("/siem_data"):
    output_file = os.path.join(os.path.dirname(__file__), "../siem_data/alertas_siem.json")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w") as f:
    json.dump(alertas_json, f, indent=2, ensure_ascii=False)

print(f"  📁 Reporte JSON exportado: {output_file}")
print()
