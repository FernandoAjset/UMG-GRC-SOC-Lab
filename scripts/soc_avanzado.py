#!/usr/bin/env python3
"""
=======================================================
MÓDULO 2: SOC AVANZADO — Análisis Completo de Amenazas
GRC Semana 5 | Universidad Mariano Gálvez de Guatemala
=======================================================
Detecta: Fuerza Bruta, Exfiltración, Escalada de Privilegios,
         Port Scanning, Sesiones Múltiples Anómalas
"""

import os
import datetime
import json

SIEM_LOG = "/siem_data/soc_logs.txt"

if not os.path.exists(SIEM_LOG):
    os.makedirs(os.path.dirname(SIEM_LOG) if os.path.dirname(SIEM_LOG) else ".", exist_ok=True)
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

# Clasificación de eventos
failed_logins    = [l for l in logs if "LOGIN_FAIL" in l]
successful_logins= [l for l in logs if "LOGIN_SUCCESS" in l]
exfiltration     = [l for l in logs if "DATA_EXPORT" in l]
privilege_esc    = [l for l in logs if "FILE_ACCESS" in l and "/etc/passwd" in l]
port_scans       = [l for l in logs if "PORT_SCAN" in l]
multi_sessions   = [l for l in logs if "MULTIPLE_ACCESS" in l]

alertas = []

print("=" * 60)
print("   GRC — SOC DASHBOARD AVANZADO")
print(f"   Analista: Sistema Automatizado (SIEM-GRC)")
print(f"   Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   Organización: TechGuard Guatemala S.A.")
print("=" * 60)
print(f"\n  📡 EVENTOS ANALIZADOS: {len(logs)}")
print()

# ── ANÁLISIS 1: Fuerza Bruta
print("  [1] ANÁLISIS — AUTENTICACIÓN")
print(f"      Fallos de login:         {len(failed_logins)}")
print(f"      Logins exitosos:         {len(successful_logins)}")
if len(failed_logins) >= 3:
    print("      🚨 ALERTA P1: Ataque de fuerza bruta confirmado")
    alertas.append({"tipo": "FUERZA BRUTA", "severidad": "CRÍTICA", "eventos": len(failed_logins)})
    print("         → Control: NIST DE.CM-1 | ISO 27001 A.9.4.2")
print()

# ── ANÁLISIS 2: Exfiltración de datos
print("  [2] ANÁLISIS — EXFILTRACIÓN DE DATOS")
print(f"      Eventos DATA_EXPORT:     {len(exfiltration)}")
if len(exfiltration) > 0:
    print("      🔴 ALERTA CRÍTICA: Posible fuga de datos (2GB)")
    alertas.append({"tipo": "EXFILTRACIÓN", "severidad": "CRÍTICA", "eventos": len(exfiltration)})
    print("         → Control: NIST PR.DS-5 | ISO 27001 A.12.4.1")
    print("         → Acción: Aislar segmento de red. Preservar evidencia.")
print()

# ── ANÁLISIS 3: Escalada de privilegios
print("  [3] ANÁLISIS — ESCALADA DE PRIVILEGIOS")
print(f"      Accesos /etc/passwd:     {len(privilege_esc)}")
if len(privilege_esc) > 0:
    print("      ⚠️  ALERTA P2: Posible escalada de privilegios")
    alertas.append({"tipo": "PRIVILEGE_ESC", "severidad": "ALTA", "eventos": len(privilege_esc)})
    print("         → Control: NIST PR.AC-4 | CIS Control 5")
print()

# ── ANÁLISIS 4: Port Scanning
print("  [4] ANÁLISIS — RECONOCIMIENTO DE RED")
print(f"      Port Scans detectados:  {len(port_scans)}")
if len(port_scans) > 0:
    print("      ⚠️  ALERTA P2: Escaneo de puertos activo")
    alertas.append({"tipo": "PORT_SCAN", "severidad": "MEDIA", "eventos": len(port_scans)})
    print("         → Control: NIST DE.CM-1 | Bloquear IP origen")
print()

# ── ANÁLISIS 5: Sesiones múltiples anómalas
print("  [5] ANÁLISIS — SESIONES ANÓMALAS")
print(f"      Sesiones múltiples:     {len(multi_sessions)}")
if len(multi_sessions) > 0:
    print("      ⚠️  ALERTA: Usuario admin con 8 sesiones simultáneas")
    alertas.append({"tipo": "SESIONES_ANOMALAS", "severidad": "MEDIA", "eventos": len(multi_sessions)})
print()

# ── RESUMEN DE ALERTAS
print("=" * 60)
print(f"  📊 RESUMEN: {len(alertas)} ALERTAS ACTIVAS")
print("=" * 60)
for i, a in enumerate(alertas, 1):
    sev_icon = "🔴" if a["severidad"] == "CRÍTICA" else ("🟠" if a["severidad"] == "ALTA" else "🟡")
    print(f"  {i}. {sev_icon} [{a['severidad']}] {a['tipo']} — {a['eventos']} eventos")

print()
print("  ACCIONES INMEDIATAS REQUERIDAS:")
print("  1. Notificar CISO en próximos 15 minutos")
print("  2. Activar procedimiento IR-001 (Respuesta a Incidentes)")
print("  3. Aislar red segment 185.21.44.0/24")
print("  4. Iniciar forensics en servidor afectado")
print("  5. Preservar cadena de custodia de logs")
print()
print("=" * 60)
print("  [FIN REPORTE SOC AVANZADO]")
print("=" * 60)
