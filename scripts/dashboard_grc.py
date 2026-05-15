#!/usr/bin/env python3
"""
=======================================================
MÓDULO 5: DASHBOARD GRC — KPIs y KRIs de Seguridad
GRC Semana 5 | Universidad Mariano Gálvez de Guatemala
=======================================================
"""

import datetime
import os
import json

print()
print("╔══════════════════════════════════════════════════════════════╗")
print("║       GRC DASHBOARD — MÉTRICAS SOC Y SEGURIDAD              ║")
print("║       TechGuard Guatemala S.A.                               ║")
print(f"║       Período: Mayo 2026 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}               ║")
print("╠══════════════════════════════════════════════════════════════╣")

# ── KPIs Operativos (CUANTIFICABLES)
kpis = {
    "MTTR (Mean Time To Respond)":      {"valor": 14,   "unidad": "min",  "meta": 15,   "estado": "OK"},
    "MTTD (Mean Time To Detect)":       {"valor": 3,    "unidad": "min",  "meta": 5,    "estado": "OK"},
    "Incidentes resueltos en SLA":      {"valor": 92,   "unidad": "%",    "meta": 90,   "estado": "OK"},
    "Disponibilidad del SOC":           {"valor": 99.8, "unidad": "%",    "meta": 99.5, "estado": "OK"},
    "Tiempo promedio análisis forense": {"valor": 2.5,  "unidad": "horas","meta": 3,    "estado": "OK"},
}

# ── KRIs de Riesgo
kris = {
    "% Detección de incidentes":        {"valor": 85,  "unidad": "%", "meta": 80,  "estado": "OK"},
    "% Logs analizados":                {"valor": 92,  "unidad": "%", "meta": 90,  "estado": "OK"},
    "Riesgo residual":                  {"valor": 18,  "unidad": "%", "meta": 20,  "estado": "OK"},
    "Incidentes críticos sin resolver": {"valor": 1,   "unidad": "",  "meta": 0,   "estado": "ALERTA"},
    "Vulnerabilidades críticas abiertas":{"valor": 3,  "unidad": "",  "meta": 0,   "estado": "ALERTA"},
    "Cobertura de controles ISO 27001": {"valor": 78,  "unidad": "%", "meta": 85,  "estado": "ALERTA"},
}

# ── Incidentes del período
incidentes = [
    {"id": "IR-2026-0501", "tipo": "Fuerza Bruta",        "severidad": "CRÍTICO", "estado": "RESUELTO", "mttr": 14},
    {"id": "IR-2026-0502", "tipo": "Exfiltración Datos",  "severidad": "CRÍTICO", "estado": "ACTIVO",   "mttr": None},
    {"id": "IR-2026-0503", "tipo": "Port Scanning",       "severidad": "MEDIO",   "estado": "RESUELTO", "mttr": 8},
    {"id": "IR-2026-0504", "tipo": "Ransomware Simulado", "severidad": "CRÍTICO", "estado": "RESUELTO", "mttr": 22},
    {"id": "IR-2026-0505", "tipo": "Escalada Privilegios","severidad": "ALTO",    "estado": "RESUELTO", "mttr": 18},
]

print("║                                                              ║")
print("║  📊 KPIs OPERATIVOS DEL SOC:                                ║")
print("╠══════════════════════════════════════════════════════════════╣")
print(f"║  {'Indicador':<40} {'Valor':>6} {'Meta':>6} {'Estado':>8} ║")
print("╠══════════════════════════════════════════════════════════════╣")
for nombre, data in kpis.items():
    estado_icon = "✅" if data["estado"] == "OK" else "⚠️ "
    val_str = f"{data['valor']}{data['unidad']}"
    meta_str = f"{data['meta']}{data['unidad']}"
    print(f"║  {nombre:<40} {val_str:>6} {meta_str:>6} {estado_icon:>8} ║")

print("╠══════════════════════════════════════════════════════════════╣")
print("║  📈 KRIs DE RIESGO:                                         ║")
print("╠══════════════════════════════════════════════════════════════╣")
print(f"║  {'Indicador':<40} {'Valor':>6} {'Meta':>6} {'Estado':>8} ║")
print("╠══════════════════════════════════════════════════════════════╣")
for nombre, data in kris.items():
    estado_icon = "✅" if data["estado"] == "OK" else "⚠️ "
    val_str = f"{data['valor']}{data['unidad']}"
    meta_str = f"{data['meta']}{data['unidad']}"
    print(f"║  {nombre:<40} {val_str:>6} {meta_str:>6} {estado_icon:>8} ║")

print("╠══════════════════════════════════════════════════════════════╣")
print("║  🚨 INCIDENTES DEL PERÍODO (Mayo 2026):                     ║")
print("╠══════════════════════════════════════════════════════════════╣")
print(f"║  {'ID':^12} {'Tipo':^22} {'Sev':^8} {'Estado':^10} {'MTTR':^6} ║")
print("╠══════════════════════════════════════════════════════════════╣")
for inc in incidentes:
    sev_icon = "🔴" if inc["severidad"] == "CRÍTICO" else ("🟠" if inc["severidad"] == "ALTO" else "🟡")
    est_icon = "✅" if inc["estado"] == "RESUELTO" else "🔄"
    mttr_str = f"{inc['mttr']}m" if inc["mttr"] else "---"
    print(f"║  {inc['id']:^12} {inc['tipo']:^22} {sev_icon+inc['severidad']:^12} {est_icon+inc['estado']:^12} {mttr_str:^6} ║")

# Cálculo resumen
total_inc = len(incidentes)
resueltos = len([i for i in incidentes if i["estado"] == "RESUELTO"])
criticos = len([i for i in incidentes if i["severidad"] == "CRÍTICO"])
mttr_vals = [i["mttr"] for i in incidentes if i["mttr"]]
mttr_promedio = sum(mttr_vals) / len(mttr_vals) if mttr_vals else 0
riesgo_residual = 18

print("╠══════════════════════════════════════════════════════════════╣")
print("║  📋 RESUMEN EJECUTIVO:                                       ║")
print(f"║  • Total incidentes período:    {total_inc}                            ║")
print(f"║  • Incidentes resueltos:        {resueltos}/{total_inc} ({resueltos/total_inc*100:.0f}%)                    ║")
print(f"║  • Incidentes críticos:         {criticos}                            ║")
print(f"║  • MTTR promedio:              {mttr_promedio:.1f} minutos                    ║")
print(f"║  • Riesgo residual global:      {riesgo_residual}%                          ║")
print(f"║  • Estado SOC:                  {'OPERACIONAL ✅' if riesgo_residual < 20 else 'EN RIESGO ⚠️'}                  ║")
print("╠══════════════════════════════════════════════════════════════╣")
print("║  🎯 RECOMENDACIONES INMEDIATAS:                              ║")
print("║  1. Resolver IR-2026-0502 (Exfiltración activa)             ║")
print("║  2. Cerrar 3 vulnerabilidades críticas pendientes           ║")
print("║  3. Mejorar cobertura ISO 27001 del 78% al 85%             ║")
print("║  4. Implementar MFA en todos los accesos privilegiados      ║")
print("╚══════════════════════════════════════════════════════════════╝")
print()

# Exportar métricas JSON
metricas_json = {
    "timestamp": datetime.datetime.now().isoformat(),
    "organizacion": "TechGuard Guatemala S.A.",
    "periodo": "Mayo 2026",
    "kpis": {k: v for k, v in kpis.items()},
    "kris": {k: v for k, v in kris.items()},
    "incidentes": incidentes,
    "resumen": {
        "total_incidentes": total_inc,
        "resueltos": resueltos,
        "criticos": criticos,
        "mttr_promedio_min": round(mttr_promedio, 1),
        "riesgo_residual_pct": riesgo_residual
    }
}

out_path = "/siem_data/dashboard_metricas.json"
if not os.path.exists("/siem_data"):
    out_path = os.path.join(os.path.dirname(__file__), "../siem_data/dashboard_metricas.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, "w") as f:
    json.dump(metricas_json, f, indent=2, ensure_ascii=False)

print(f"  📁 Métricas exportadas: {out_path}")
print()
