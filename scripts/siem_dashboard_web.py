import datetime
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_DIRS = [os.path.join(ROOT_DIR, "siem_data"), "/siem_data"]
LOG_DIRS = [os.path.join(ROOT_DIR, "logs"), "/logs"]


def read_json(filename, fallback):
    for data_dir in DATA_DIRS:
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
    return fallback


def read_tail(filename, dirs, lines=14):
    for data_dir in dirs:
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            with open(path, encoding="utf-8", errors="replace") as fh:
                return fh.readlines()[-lines:]
    return []


def writable_data_dir():
    for data_dir in DATA_DIRS:
        if os.path.isdir(data_dir) and os.access(data_dir, os.W_OK):
            return data_dir
    os.makedirs(DATA_DIRS[-1], exist_ok=True)
    return DATA_DIRS[-1]


def write_json(filename, payload):
    path = os.path.join(writable_data_dir(), filename)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    return path


def append_soc_log(line):
    path = os.path.join(writable_data_dir(), "soc_logs.txt")
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def norm_level(level):
    return {
        "CRÍTICO": "CRITICAL",
        "CRITICO": "CRITICAL",
        "ALTO": "HIGH",
        "MEDIO": "MEDIUM",
        "BAJO": "LOW",
    }.get(str(level).upper(), str(level).upper())


def metric_value(metrics, group, name, default):
    item = metrics.get(group, {}).get(name, {})
    if isinstance(item, dict):
        return item.get("valor", default)
    return default


def current_run_number():
    state = read_json("simulacion_estado.json", {"run": 0})
    return int(state.get("run", 0))


def simulate_period():
    run = current_run_number() + 1
    now = datetime.datetime.now()
    scenario = (run - 1) % 3

    scenarios = [
        {
            "name": "Periodo crítico: exfiltración contenida parcialmente",
            "risk": 22,
            "mttr": 18,
            "mttd": 4,
            "sla": 86,
            "iso": 79,
            "pci": 58,
            "mfa": 62,
            "alerts": [
                ("GRC-1001", "Fuerza Bruta SSH", "CRÍTICO", 6),
                ("GRC-1003", "Exfiltración Datos 1.4GB", "CRÍTICO", 2),
                ("GRC-1099", "Kill Chain Completo", "CRÍTICO", 7),
                ("GRC-1004", "Port Scanning externo", "MEDIO", 3),
            ],
            "incidents": [
                ("IR-2026-SIM01", "Fuerza Bruta SSH", "CRÍTICO", "RESUELTO", 18),
                ("IR-2026-SIM02", "Exfiltración Datos", "CRÍTICO", "ACTIVO", None),
                ("IR-2026-SIM03", "Port Scanning", "MEDIO", "RESUELTO", 9),
                ("IR-2026-SIM04", "Escalada Privilegios", "ALTO", "RESUELTO", 16),
            ],
        },
        {
            "name": "Periodo estable: controles preventivos mejoran",
            "risk": 16,
            "mttr": 11,
            "mttd": 2,
            "sla": 95,
            "iso": 84,
            "pci": 67,
            "mfa": 78,
            "alerts": [
                ("GRC-1001", "Fuerza Bruta bloqueada", "ALTO", 3),
                ("GRC-1004", "Port Scanning mitigado", "MEDIO", 2),
                ("GRC-1002", "Acceso archivo sensible", "ALTO", 1),
            ],
            "incidents": [
                ("IR-2026-SIM05", "Fuerza Bruta", "ALTO", "RESUELTO", 11),
                ("IR-2026-SIM06", "Port Scanning", "MEDIO", "RESUELTO", 6),
                ("IR-2026-SIM07", "Acceso Archivo Sistema", "ALTO", "RESUELTO", 13),
            ],
        },
        {
            "name": "Periodo ransomware: recuperación probada",
            "risk": 19,
            "mttr": 21,
            "mttd": 3,
            "sla": 89,
            "iso": 82,
            "pci": 63,
            "mfa": 71,
            "alerts": [
                ("GRC-1005", "Ransomware simulado detectado", "CRÍTICO", 4),
                ("GRC-1006", "Cambio masivo de archivos .locked", "CRÍTICO", 6),
                ("GRC-1001", "Fuerza Bruta previa", "ALTO", 2),
            ],
            "incidents": [
                ("IR-2026-SIM08", "Ransomware Simulado", "CRÍTICO", "RESUELTO", 21),
                ("IR-2026-SIM09", "Fuerza Bruta", "ALTO", "RESUELTO", 12),
                ("IR-2026-SIM10", "Cambio Masivo Archivos", "CRÍTICO", "RESUELTO", 24),
            ],
        },
    ]

    data = scenarios[scenario]
    alerts_payload = {
        "timestamp": now.isoformat(),
        "simulacion": run,
        "escenario": data["name"],
        "alertas": [
            {"id": alert_id, "desc": desc, "nivel": level, "eventos": events}
            for alert_id, desc, level, events in data["alerts"]
        ],
    }
    metrics_payload = {
        "timestamp": now.isoformat(),
        "organizacion": "TechGuard Guatemala S.A.",
        "periodo": f"Simulación SOC #{run}",
        "kpis": {
            "MTTR (Mean Time To Respond)": {"valor": data["mttr"], "unidad": "min", "meta": 15, "estado": "OK" if data["mttr"] <= 15 else "ALERTA"},
            "MTTD (Mean Time To Detect)": {"valor": data["mttd"], "unidad": "min", "meta": 5, "estado": "OK"},
            "Incidentes resueltos en SLA": {"valor": data["sla"], "unidad": "%", "meta": 90, "estado": "OK" if data["sla"] >= 90 else "ALERTA"},
            "Disponibilidad del SOC": {"valor": 99.7, "unidad": "%", "meta": 99.5, "estado": "OK"},
        },
        "kris": {
            "% Detección de incidentes": {"valor": 88, "unidad": "%", "meta": 80, "estado": "OK"},
            "% Logs analizados": {"valor": 94, "unidad": "%", "meta": 90, "estado": "OK"},
            "Riesgo residual": {"valor": data["risk"], "unidad": "%", "meta": 20, "estado": "OK" if data["risk"] <= 20 else "ALERTA"},
            "Vulnerabilidades críticas abiertas": {"valor": 2, "unidad": "", "meta": 0, "estado": "ALERTA"},
            "Cobertura de controles ISO 27001": {"valor": data["iso"], "unidad": "%", "meta": 85, "estado": "ALERTA"},
        },
        "incidentes": [
            {"id": inc_id, "tipo": inc_type, "severidad": sev, "estado": status, "mttr": mttr}
            for inc_id, inc_type, sev, status, mttr in data["incidents"]
        ],
        "simulacion": {"run": run, "escenario": data["name"], "pci": data["pci"], "mfa": data["mfa"]},
    }

    write_json("alertas_siem.json", alerts_payload)
    write_json("dashboard_metricas.json", metrics_payload)
    write_json("simulacion_estado.json", {"run": run, "timestamp": now.isoformat(), "escenario": data["name"]})
    append_soc_log(f"{now.strftime('%Y-%m-%d %H:%M:%S')} SIMULATION_RUN run={run} scenario=\"{data['name']}\" risk={data['risk']} mttr={data['mttr']}")
    return {"ok": True, "run": run, "scenario": data["name"], "payload": build_payload()}


def build_payload():
    now = datetime.datetime.now()
    metrics = read_json("dashboard_metricas.json", {})
    alerts_raw = read_json("alertas_siem.json", {"alertas": []})

    alerts = []
    for index, alert in enumerate(alerts_raw.get("alertas", []), start=1):
        alerts.append(
            {
                "id": alert.get("id", f"GRC-{1000 + index}"),
                "level": norm_level(alert.get("nivel", "LOW")),
                "desc": alert.get("desc", "Alerta SIEM"),
                "events": alert.get("eventos", 1),
                "time": f"10:{index + 3:02d}",
            }
        )

    if not alerts:
        alerts = [
            {"id": "GRC-1099", "level": "CRITICAL", "desc": "Kill Chain Detectado: Fuerza Bruta -> Exfiltración", "events": 5, "time": "10:06"},
            {"id": "GRC-1003", "level": "CRITICAL", "desc": "Exfiltración de Datos 2GB - BD Clientes", "events": 1, "time": "10:05"},
            {"id": "GRC-1004", "level": "MEDIUM", "desc": "Port Scanning externo detectado", "events": 1, "time": "10:08"},
        ]

    incidents_raw = metrics.get("incidentes") or [
        {"id": "IR-2026-0501", "tipo": "Fuerza Bruta", "severidad": "CRÍTICO", "estado": "RESUELTO", "mttr": 14},
        {"id": "IR-2026-0502", "tipo": "Exfiltración Datos", "severidad": "CRÍTICO", "estado": "ACTIVO", "mttr": None},
        {"id": "IR-2026-0503", "tipo": "Port Scanning", "severidad": "MEDIO", "estado": "RESUELTO", "mttr": 8},
        {"id": "IR-2026-0504", "tipo": "Ransomware Simulado", "severidad": "CRÍTICO", "estado": "RESUELTO", "mttr": 22},
        {"id": "IR-2026-0505", "tipo": "Escalada Privilegios", "severidad": "ALTO", "estado": "RESUELTO", "mttr": 18},
    ]

    incidents = []
    for incident in incidents_raw:
        incidents.append(
            {
                "id": incident.get("id"),
                "type": incident.get("tipo", incident.get("type", "Incidente")),
                "severity": norm_level(incident.get("severidad", incident.get("severity", "LOW"))),
                "status": incident.get("estado", incident.get("status", "ABIERTO")),
                "mttr": incident.get("mttr"),
                "impact": incident.get("impacto", "Impacto operativo controlado"),
            }
        )

    active_incidents = [i for i in incidents if i["status"] != "RESUELTO"]
    critical_open = len([i for i in active_incidents if i["severity"] == "CRITICAL"])
    total_cost = 257500
    residual_risk = metric_value(metrics, "kris", "Riesgo residual", 18)
    iso_coverage = metric_value(metrics, "kris", "Cobertura de controles ISO 27001", 78)
    simulation = metrics.get("simulacion", {})
    pci_compliance = simulation.get("pci", 55)
    mfa_coverage = simulation.get("mfa", 55)

    logs = read_tail("auth.log", LOG_DIRS, 8) + read_tail("soc_logs.txt", DATA_DIRS, 8)
    logs = [line.rstrip() for line in logs if line.strip()]

    return {
        "status": {
            "status": "OPERATIONAL",
            "timestamp": now.isoformat(),
            "soc": metrics.get("organizacion", "TechGuard Guatemala S.A."),
            "period": metrics.get("periodo", "Mayo 2026"),
            "events_analyzed": sum(a.get("events", 1) for a in alerts) * 24,
            "active_alerts": len(alerts),
            "critical_open": critical_open,
            "mttr_min": metric_value(metrics, "kpis", "MTTR (Mean Time To Respond)", 14),
            "mttd_min": metric_value(metrics, "kpis", "MTTD (Mean Time To Detect)", 3),
            "sla_compliance": metric_value(metrics, "kpis", "Incidentes resueltos en SLA", 92),
            "availability": metric_value(metrics, "kpis", "Disponibilidad del SOC", 99.8),
            "residual_risk_pct": residual_risk,
            "financial_exposure_usd": total_cost,
            "board_message": "SOC operacional, pero con decisión ejecutiva pendiente: contener exfiltración IR-2026-0502, cerrar MFA privilegiado y remediar PCI-DSS.",
        },
        "alerts": {"total": len(alerts), "alerts": alerts},
        "metrics": {
            "kpis": {
                "mttr": metric_value(metrics, "kpis", "MTTR (Mean Time To Respond)", 14),
                "mttd": metric_value(metrics, "kpis", "MTTD (Mean Time To Detect)", 3),
                "sla_compliance": metric_value(metrics, "kpis", "Incidentes resueltos en SLA", 92),
                "availability": metric_value(metrics, "kpis", "Disponibilidad del SOC", 99.8),
                "false_positives": 12,
                "patch_sla": 87,
            },
            "kris": {
                "detection_rate": metric_value(metrics, "kris", "% Detección de incidentes", 85),
                "logs_analyzed": metric_value(metrics, "kris", "% Logs analizados", 92),
                "residual_risk": residual_risk,
                "critical_open": critical_open,
                "vulns_critical": metric_value(metrics, "kris", "Vulnerabilidades críticas abiertas", 3),
                "iso_coverage": iso_coverage,
                "pci_compliance": pci_compliance,
                "mfa_coverage": mfa_coverage,
                "backups_verified": 95,
            },
            "incidents": incidents,
            "risk_trend": [76, 61, 48, 34, 24, residual_risk],
            "incident_distribution": [
                {"label": "Fuerza Bruta", "value": 45, "color": "#2563eb"},
                {"label": "Exfiltración", "value": 15, "color": "#dc2626"},
                {"label": "Ransomware", "value": 10, "color": "#7c3aed"},
                {"label": "Privilegios", "value": 20, "color": "#d97706"},
                {"label": "Port Scan", "value": 10, "color": "#059669"},
            ],
            "controls": [
                {"domain": "ISO 27001", "current": iso_coverage, "target": 85, "owner": "GRC Manager"},
                {"domain": "PCI-DSS v4.0", "current": pci_compliance, "target": 80, "owner": "CISO + GRC"},
                {"domain": "MFA privilegiado", "current": mfa_coverage, "target": 100, "owner": "Cloud Admin"},
                {"domain": "Backups verificados", "current": 95, "target": 90, "owner": "Infraestructura"},
                {"domain": "Logs analizados", "current": 92, "target": 90, "owner": "SOC Lead"},
            ],
            "risk_register": [
                {"risk": "Exfiltración datos clientes", "probability": 4, "impact": 5, "owner": "CISO", "treatment": "Contener + notificar"},
                {"risk": "Usuarios privilegiados sin MFA", "probability": 5, "impact": 4, "owner": "Cloud Admin", "treatment": "MFA obligatorio 7 días"},
                {"risk": "CVEs críticos sin parchear", "probability": 4, "impact": 4, "owner": "Cloud + Dev", "treatment": "Parcheo 72h"},
                {"risk": "Brecha PCI-DSS", "probability": 3, "impact": 4, "owner": "GRC", "treatment": "Roadmap 90 días"},
            ],
            "action_plan": [
                {"priority": "P1", "action": "Resolver IR-2026-0502 y preservar evidencia", "owner": "DFIR + CISO", "due": "Inmediato", "status": "En curso"},
                {"priority": "P1", "action": "Activar MFA para 45% faltante de usuarios privilegiados", "owner": "Cloud Admin", "due": "7 días", "status": "Pendiente"},
                {"priority": "P2", "action": "Cerrar 3 CVEs críticos", "owner": "Cloud + Dev", "due": "72h", "status": "Pendiente"},
                {"priority": "P2", "action": "Subir ISO 27001 de 78% a 85%", "owner": "GRC Manager", "due": "60 días", "status": "Planificado"},
            ],
            "logs": logs,
            "simulation": simulation,
        },
    }


HTML = open(os.path.join(BASE_DIR, "dashboard.html"), encoding="utf-8").read()


class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} {self.address_string()} {fmt % args}")

    def send_json(self, payload, include_body=True):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if include_body:
            self.wfile.write(body)

    def send_html(self, include_body=True):
        body = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if include_body:
            self.wfile.write(body)

    def send_not_found(self):
        body = b'{"error":"not found"}'
        self.send_response(404)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        payload = build_payload()
        if path in ("/", "/index.html"):
            self.send_html()
        elif path == "/api/status":
            self.send_json(payload["status"])
        elif path == "/api/alerts":
            self.send_json(payload["alerts"])
        elif path == "/api/metrics":
            self.send_json(payload["metrics"])
        elif path == "/api/executive":
            self.send_json(payload)
        else:
            self.send_not_found()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/simulate":
            self.send_json(simulate_period())
        else:
            self.send_not_found()

    def do_HEAD(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self.send_html(include_body=False)
        elif path in ("/api/status", "/api/alerts", "/api/metrics", "/api/executive"):
            self.send_json({}, include_body=False)
        else:
            self.send_not_found()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", "8080"))
    print(f"GRC Dashboard: http://localhost:{port}")
    ThreadingHTTPServer(("0.0.0.0", port), DashboardHandler).serve_forever()
