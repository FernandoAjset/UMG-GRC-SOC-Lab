# CREDENCIALES Y COMANDOS — Laboratorio GRC SOC Simulado

## Universidad Mariano Gálvez de Guatemala
**Tarea:** Semana 5 GRC | **Referencia rápida para pruebas manuales**

---

## CREDENCIALES DE TODOS LOS SERVIDORES

| Contenedor | Rol | Hostname | IP Interna | Puerto Local | Usuario | Contraseña | Notas |
|---|---|---|---|---|---|---|---|
| `grc-soc-lab` | Servidor SOC Principal | soc-server | 172.20.0.10 | SSH: 2222 | root | GRC2026! | Admin completo |
| `grc-soc-lab` | Servidor SOC Principal | soc-server | 172.20.0.10 | SSH: 2222 | student | Student2026! | Usuario práctica |
| `grc-attacker` | Nodo Atacante | attacker-node | 172.20.0.20 | SSH: 2223 | root | Attacker2026! | Simula atacante externo |
| `grc-siem` | Dashboard SIEM | siem-server | 172.20.0.30 | HTTP: 8080 | — | — | Solo acceso web |

---

## PASO 1 — LEVANTAR EL LABORATORIO

```bash
# Desde el directorio del proyecto (donde está docker-compose.yml)
cd <directorio-del-repo>

# Construir imágenes y levantar contenedores
docker compose up -d --build

# Verificar estado
docker compose ps

# Ver logs de inicio
docker compose logs --tail=20
```

**Salida esperada de `docker compose ps`:**
```
NAME              IMAGE            STATUS    PORTS
grc-soc-lab       grc-soc-lab      Up        0.0.0.0:2222->22/tcp
grc-attacker      alpine:3.18      Up        0.0.0.0:2223->22/tcp
grc-siem          python:3.11-slim Up        0.0.0.0:8080->8080/tcp
```

---

## PASO 2 — CONECTARSE A LOS SERVIDORES

### Servidor SOC Principal (USAR ESTE PARA EL LAB)

```bash
# Opción A: como root (administrador)
ssh root@localhost -p 2222
# Contraseña: GRC2026!

# Opción B: como estudiante
ssh student@localhost -p 2222
# Contraseña: Student2026!

# Si pide aceptar fingerprint, escribir: yes
```

### Nodo Atacante (para simular ataques)

```bash
ssh root@localhost -p 2223
# Contraseña: Attacker2026!
```

### Dashboard SIEM Web

```
Navegador: http://localhost:8080
API Status:  http://localhost:8080/api/status
API Alerts:  http://localhost:8080/api/alerts
API Metrics: http://localhost:8080/api/metrics
```

---

## PASO 3 — EJECUTAR MÓDULOS SOC (en grc-soc-lab)

```bash
# Conectarse primero:
ssh root@localhost -p 2222   # Contraseña: GRC2026!

# ── MÓDULO 1: SOC Básico (Detección Fuerza Bruta)
python3 /soc/scripts/soc_basico.py

# ── MÓDULO 2: SOC Avanzado (Multi-Amenaza)
python3 /soc/scripts/soc_avanzado.py

# ── MÓDULO 3: Simulación Ransomware
python3 /soc/scripts/ransomware_sim.py

# ── MÓDULO 4: SIEM Motor de Correlación
python3 /soc/scripts/siem_simulado.py

# ── MÓDULO 5: Dashboard KPIs/KRIs
python3 /soc/scripts/dashboard_grc.py

# ── EJECUTAR TODOS EN SECUENCIA (demo completa)
for script in soc_basico soc_avanzado ransomware_sim siem_simulado dashboard_grc; do
  echo ""
  echo "══════════ Ejecutando: $script.py ══════════"
  python3 /soc/scripts/${script}.py
  sleep 1
done
```

---

## PASO 4 — INSPECCIONAR LOGS Y ARCHIVOS

```bash
# Dentro de grc-soc-lab:

# Ver logs de autenticación
cat /logs/auth.log

# Ver logs SOC avanzados
cat /siem_data/soc_logs.txt

# Ver archivos "ransomware" antes de la simulación
ls -la /lab_ransom/

# Después de correr ransomware_sim.py:
ls -la /lab_ransom/*.locked

# Ver alertas exportadas por SIEM en JSON
cat /siem_data/alertas_siem.json

# Ver métricas exportadas por dashboard
cat /siem_data/dashboard_metricas.json

# Calcular hash SHA256 de logs (cadena de custodia)
sha256sum /logs/auth.log /siem_data/soc_logs.txt
```

---

## PASO 5 — PRUEBAS MANUALES (dentro de los contenedores)

### Ver red interna Docker

```bash
# En grc-soc-lab:
ip addr show          # Ver IPs del contenedor
route -n              # Ver tabla de routing
cat /etc/hosts        # Ver resolución de nombres

# Hacer ping al atacante
ping 172.20.0.20 -c 3

# Ver servicios activos
netstat -tlnp
ss -tlnp
```

### Agregar logs manualmente (simular más eventos)

```bash
# En grc-soc-lab, agregar un evento de ataque manualmente:
echo "$(date '+%Y-%m-%d %H:%M:%S') FAILED login user=admin ip=10.10.10.99" >> /logs/auth.log
echo "$(date '+%Y-%m-%d %H:%M') LOGIN_FAIL user=hacker ip=200.100.50.1" >> /siem_data/soc_logs.txt

# Volver a correr el análisis para ver el nuevo evento detectado
python3 /soc/scripts/soc_basico.py
python3 /soc/scripts/siem_simulado.py
```

### Simular ataque desde el contenedor atacante

```bash
# Conectarse al atacante:
ssh root@localhost -p 2223   # Contraseña: Attacker2026!

# Desde el atacante, intentar conectar al SOC lab:
ssh root@172.20.0.10   # Esto generará tráfico SSH real

# Hacer escaneo de red (si nmap disponible):
# apk add nmap
# nmap -sS 172.20.0.10
```

---

## PASO 6 — COMANDOS DE ADMINISTRACIÓN

```bash
# Ver cuántos recursos consume el lab
docker stats --no-stream

# Ver logs de un contenedor específico
docker logs grc-soc-lab --tail=50
docker logs grc-attacker --tail=20
docker logs grc-siem --tail=30

# Reiniciar un contenedor
docker compose restart grc-soc-lab

# Entrar a un contenedor sin SSH (forma directa)
docker exec -it grc-soc-lab bash
docker exec -it grc-attacker sh

# Copiar archivos desde/hacia el contenedor
docker cp grc-soc-lab:/siem_data/alertas_siem.json ./alertas_exportadas.json
docker cp grc-soc-lab:/logs/auth.log ./auth_log_copia.log

# DETENER y eliminar el laboratorio
docker compose down

# Limpiar TODO (contenedores + imágenes + volúmenes)
docker compose down -v --remove-orphans
docker image rm grc-soc-lab 2>/dev/null || true
```

---

## PASO 7 — VERIFICACIONES RÁPIDAS

```bash
# ── Verificar que SSH funciona en el SOC
nc -zv localhost 2222 && echo "SSH SOC: OK" || echo "SSH SOC: FALLO"

# ── Verificar que SSH funciona en el atacante
nc -zv localhost 2223 && echo "SSH Attacker: OK" || echo "SSH Attacker: FALLO"

# ── Verificar que el dashboard web está activo
curl -s http://localhost:8080/api/status | python3 -m json.tool

# ── One-liner: verificar todo el laboratorio
echo "=== ESTADO DEL LABORATORIO GRC ===" && \
  docker compose ps && \
  echo "" && \
  echo "APIs disponibles:" && \
  curl -s http://localhost:8080/api/status 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "Dashboard no disponible aún"
```

---

## ESTRUCTURA FINAL DEL PROYECTO

```
Implementar GRC/
├── docker-compose.yml              # Orquestación Docker (levantar con: docker compose up -d --build)
├── Dockerfile.soc                  # Imagen Ubuntu 22.04 + SSH + Python3 + herramientas SOC
│
├── scripts/
│   ├── soc_basico.py               # Módulo 1: Detección fuerza bruta
│   ├── soc_avanzado.py             # Módulo 2: Análisis multi-amenaza (5 tipos)
│   ├── ransomware_sim.py           # Módulo 3: Simulación ransomware controlada
│   ├── siem_simulado.py            # Módulo 4: Motor SIEM con 5 reglas correlación
│   ├── dashboard_grc.py            # Módulo 5: Dashboard KPIs/KRIs
│   └── siem_dashboard_web.py       # Módulo 6: API REST Flask (http://localhost:8080)
│
├── logs/                           # Logs de autenticación (auth.log)
├── siem_data/                      # Logs SOC + JSON exports (alertas, métricas)
├── lab_ransom/                     # Directorio simulación ransomware
│
└── docs/
    ├── 01_FASE1_Planeacion_Analisis.md     # Fase 1: Madurez GRC, roles, caso negocio
    ├── 02_FASE2_Diseno.md                  # Fase 2: Matriz riesgos, arquitectura
    ├── 03_FASE3_Implementacion.md          # Fase 3: 3 incidentes simulados + comandos
    ├── 04_FASE4_Herramientas_Lab.md        # Fase 4: Docker, SIEM, scripts, IoCs
    ├── 05_FASE5_Monitoreo_KPIs.md          # Fase 5: KPIs, KRIs, mejora continua
    ├── 06_Conclusiones_Recomendaciones.md  # Conclusiones individuales + recomendaciones
    └── CREDENCIALES_Y_COMANDOS.md          # ESTE ARCHIVO — Referencia rápida
```

---

*TechGuard Guatemala S.A. | GRC Semana 5 | Universidad Mariano Gálvez de Guatemala*
