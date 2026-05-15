#!/usr/bin/env python3
"""
=======================================================
MÓDULO 3: SIMULACIÓN DE RANSOMWARE (Entorno Controlado)
GRC Semana 5 | Universidad Mariano Gálvez de Guatemala
=======================================================
AVISO: Este script es ÚNICAMENTE educativo.
Solo renombra archivos de prueba — NO cifra datos reales.
"""

import os
import datetime
import time

FOLDER = "/lab_ransom"

# Fallback si no estamos en Docker
if not os.path.exists(FOLDER):
    FOLDER = os.path.join(os.path.dirname(__file__), "../lab_ransom")

os.makedirs(FOLDER, exist_ok=True)

print("=" * 58)
print("  MÓDULO RANSOMWARE SIMULADO — LABORATORIO SEGURO")
print(f"  Organización: TechGuard Guatemala S.A.")
print(f"  Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 58)
print()

# FASE 1: Crear archivos de prueba
print("  [FASE 1] Creando archivos corporativos de prueba...")
archivos_prueba = [
    ("contrato_cliente_001.docx", "Contrato confidencial — Cliente Premium 001"),
    ("reporte_financiero_Q1_2026.xlsx", "Reporte financiero primer trimestre 2026"),
    ("nomina_empleados_mayo.pdf", "Nómina de empleados — Mayo 2026"),
    ("clientes_vip_2026.csv", "Base de datos clientes VIP — CONFIDENCIAL"),
    ("credenciales_produccion.txt", "Credenciales servidor de producción"),
    ("plan_estrategico_2026.pptx", "Plan estratégico corporativo 2026-2030"),
]

# Limpiar archivos locked anteriores primero
for f in os.listdir(FOLDER):
    if f.endswith(".locked"):
        os.remove(os.path.join(FOLDER, f))

for nombre, contenido in archivos_prueba:
    ruta = os.path.join(FOLDER, nombre)
    with open(ruta, "w") as f:
        f.write(contenido)

archivos_iniciales = os.listdir(FOLDER)
print(f"  ✅ {len(archivos_iniciales)} archivos corporativos creados")
for f in sorted(archivos_iniciales):
    print(f"      📄 {f}")
print()

# FASE 2: Simulación del cifrado (renombrado)
print("  [FASE 2] Simulando comportamiento ransomware...")
print("  ⚠️  [ENTORNO CONTROLADO — Solo renombrado de archivos]")
print()
time.sleep(1)

archivos_cifrados = 0
inicio = datetime.datetime.now()

for archivo in os.listdir(FOLDER):
    ruta_original = os.path.join(FOLDER, archivo)
    if os.path.isfile(ruta_original) and not archivo.endswith(".locked"):
        ruta_nueva = ruta_original + ".locked"
        os.rename(ruta_original, ruta_nueva)
        archivos_cifrados += 1
        print(f"      🔒 {archivo} → {archivo}.locked")
        time.sleep(0.2)

fin = datetime.datetime.now()
tiempo_cifrado = (fin - inicio).total_seconds()

print()
print("  [FASE 3] DETECCIÓN SOC — Sistema de Monitoreo Activado...")
print()

locked_files = [f for f in os.listdir(FOLDER) if ".locked" in f]
velocidad = archivos_cifrados / tiempo_cifrado if tiempo_cifrado > 0 else archivos_cifrados

print(f"  📊 INDICADORES DE DETECCIÓN:")
print(f"     Archivos afectados:          {len(locked_files)}")
print(f"     Tiempo de cifrado:           {tiempo_cifrado:.1f} segundos")
print(f"     Velocidad:                   {velocidad:.1f} archivos/seg")
print(f"     Extensión sospechosa:        .locked")
print(f"     Patrón de comportamiento:    MODIFICACIÓN MASIVA")
print()

if len(locked_files) > 2:
    print("  🚨 ALERTA SOC ACTIVADA:")
    print("     COMPORTAMIENTO RANSOMWARE DETECTADO")
    print()
    print("  📋 PROTOCOLO DE RESPUESTA IR-RANSOM-001:")
    print("     1. ✅ CONTENER: Aislar máquina de la red inmediatamente")
    print("     2. ✅ IDENTIFICAR: Determinar vector de entrada (phishing/RDP)")
    print("     3. ✅ ERRADICAR: Eliminar payload del ransomware")
    print("     4. ✅ RECUPERAR: Restaurar desde último backup verificado")
    print("     5. ✅ DOCUMENTAR: Registrar IoCs para inteligencia de amenazas")
    print()
    print("  📊 MÉTRICAS GRC DEL INCIDENTE:")
    print(f"     MTTD (Detección):          3 minutos estimados")
    print(f"     RTO (Recovery Time Obj):   4 horas")
    print(f"     RPO (Recovery Point Obj):  24 horas")
    print(f"     Impacto en CIA:            Confidencialidad ❌ | Integridad ❌ | Disponibilidad ❌")
    print(f"     Nivel de riesgo:           CRÍTICO")
    print()
    print("  🎯 MARCOS DE REFERENCIA APLICADOS:")
    print("     • NIST CSF: DETECTAR (DE.CM-7), RESPONDER (RS.RP-1)")
    print("     • ISO 27001: A.12.4.1 (Logging), A.16.1.5 (Respuesta a incidentes)")
    print("     • MITRE ATT&CK: T1486 (Data Encrypted for Impact)")

print()
print("=" * 58)
print("  [FIN SIMULACIÓN RANSOMWARE]")
print("=" * 58)
