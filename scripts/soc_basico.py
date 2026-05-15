#!/usr/bin/env python3
"""
=======================================================
MÓDULO 1: SOC BÁSICO — Detección de Fuerza Bruta
GRC Semana 5 | Universidad Mariano Gálvez de Guatemala
=======================================================
"""

import os
import datetime

LOG_FILE = "/logs/auth.log"

# Fallback si no estamos en Docker
if not os.path.exists(LOG_FILE):
    LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/auth.log")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    # Crear logs de prueba
    with open(LOG_FILE, "w") as f:
        f.write("2026-05-01 10:01:05 FAILED login user=admin ip=185.21.44.10\n")
        f.write("2026-05-01 10:01:22 FAILED login user=root ip=185.21.44.11\n")
        f.write("2026-05-01 10:01:38 FAILED login user=admin ip=185.21.44.12\n")
        f.write("2026-05-01 10:01:55 FAILED login user=guest ip=185.21.44.13\n")
        f.write("2026-05-01 10:02:10 SUCCESS login user=admin ip=185.21.44.10\n")
        f.write("2026-05-01 10:03:05 FILE_ACCESS /etc/passwd user=admin ip=185.21.44.10\n")
        f.write("2026-05-01 10:04:30 DATA_EXPORT database=clients size=2GB user=admin\n")

with open(LOG_FILE) as f:
    logs = f.readlines()

# Análisis
fails = [log for log in logs if "FAILED" in log]
success = [log for log in logs if "SUCCESS" in log]
total = len(logs)

# Extraer IPs únicas de los fallos
ips_atacantes = set()
for log in fails:
    for part in log.split():
        if part.startswith("ip="):
            ips_atacantes.add(part.replace("ip=", ""))

print("=" * 55)
print("  SOC BÁSICO — ANÁLISIS DE AUTENTICACIÓN")
print(f"  Fecha análisis: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 55)
print(f"\n  Total eventos en log:         {total}")
print(f"  Intentos FALLIDOS:            {len(fails)}")
print(f"  Inicios EXITOSOS:             {len(success)}")
print(f"  IPs únicas atacantes:         {len(ips_atacantes)}")
print(f"  IPs detectadas: {', '.join(ips_atacantes)}")
print()

if len(fails) > 2:
    print("  🚨 ALERTA SOC: POSIBLE ATAQUE DE FUERZA BRUTA")
    print(f"     → {len(fails)} intentos fallidos detectados")
    print(f"     → Umbral configurado: 2 intentos")
    print()
    print("  📋 RESPUESTA GRC RECOMENDADA:")
    print("     1. Bloquear IPs atacantes en firewall")
    print("     2. Forzar cambio de contraseña usuarios afectados")
    print("     3. Activar MFA en todos los accesos SSH")
    print("     4. Escalar al CISO — Incidente P1")
    print("     5. Registrar en bitácora de incidentes")
    print()
    print("  📊 MÉTRICAS DEL INCIDENTE:")
    print(f"     MTTD (Tiempo detección): 3 minutos")
    print(f"     MTTR (Tiempo respuesta): 14 minutos")
    print(f"     Severidad: ALTA")
    print(f"     Marco de referencia: NIST CSF — DETECTAR (DE.CM-1)")
else:
    print("  ✅ Sin alertas activas. Sistema operando con normalidad.")

print()
print("=" * 55)
print("  [FIN REPORTE SOC BÁSICO]")
print("=" * 55)
