# Laboratorio GRC/SOC Simulado — TechGuard Guatemala

**Curso:** Gobierno, Riesgo y Cumplimiento | Universidad Mariano Gálvez de Guatemala  
**Tarea:** Semana 5 — Implementación de un Modelo GRC con Enfoque Tecnológico y SOC Simulado  
**Profesor:** MS.c. Erick Enrique Blanco Acevedo

---

## Requisitos previos

| Herramienta | Versión mínima | Verificar |
|---|---|---|
| Docker Desktop | 24.x | `docker --version` |
| Docker Compose | 2.x | `docker compose version` |
| Python 3 | 3.8+ | `python3 --version` |

Compatible con macOS, Linux y Windows (WSL2).

---

## Levantar el laboratorio

```bash
# 1. Clonar el repositorio
git clone <URL-del-repo>
cd <nombre-del-directorio>

# 2. Construir imágenes y levantar los 3 contenedores
docker compose up -d --build

# 3. Verificar que todo está corriendo
docker compose ps
```

Salida esperada:

```
NAME              STATUS    PORTS
grc-soc-lab       Up        0.0.0.0:2222->22/tcp
grc-attacker      Up        0.0.0.0:2223->22/tcp
grc-siem          Up        0.0.0.0:8080->8080/tcp
```

---

## Acceder a los servidores

```bash
# Servidor SOC principal (usuario administrador)
ssh root@localhost -p 2222
# Contraseña: GRC2026!

# Servidor SOC principal (usuario estudiante)
ssh student@localhost -p 2222
# Contraseña: Student2026!

# Nodo atacante simulado
ssh root@localhost -p 2223
# Contraseña: Attacker2026!

# Dashboard SIEM — abrir en navegador
# http://localhost:8080
```

---

## Ejecutar los módulos SOC

Conectarse primero al servidor SOC (`ssh root@localhost -p 2222`), luego:

```bash
# Módulo 1 — Detección de fuerza bruta
python3 /soc/scripts/soc_basico.py

# Módulo 2 — Análisis multi-amenaza (5 tipos de ataque)
python3 /soc/scripts/soc_avanzado.py

# Módulo 3 — Simulación de comportamiento ransomware
python3 /soc/scripts/ransomware_sim.py

# Módulo 4 — Motor SIEM con correlación de eventos
python3 /soc/scripts/siem_simulado.py

# Módulo 5 — Dashboard KPIs/KRIs
python3 /soc/scripts/dashboard_grc.py

# Ejecutar todos en secuencia (demo completa)
for script in soc_basico soc_avanzado ransomware_sim siem_simulado dashboard_grc; do
  echo "══════════ $script.py ══════════"
  python3 /soc/scripts/${script}.py
  sleep 1
done
```

---

## Dashboard web SIEM

Con el laboratorio activo, abrir `http://localhost:8080` en el navegador.

APIs disponibles:

```bash
curl http://localhost:8080/api/status     # Estado general del SOC
curl http://localhost:8080/api/alerts     # Alertas activas
curl http://localhost:8080/api/metrics    # Métricas KPIs/KRIs
curl http://localhost:8080/api/executive  # Vista ejecutiva
curl -X POST http://localhost:8080/api/simulate  # Generar nuevo período
```

---

## Estructura del proyecto

```
.
├── docker-compose.yml              # Orquestación de los 3 contenedores
├── Dockerfile.soc                  # Imagen Ubuntu 22.04 con SSH + Python3 + herramientas SOC
├── scripts/
│   ├── soc_basico.py               # Módulo 1: fuerza bruta
│   ├── soc_avanzado.py             # Módulo 2: multi-amenaza
│   ├── ransomware_sim.py           # Módulo 3: ransomware controlado
│   ├── siem_simulado.py            # Módulo 4: SIEM con 5 reglas de correlación
│   ├── dashboard_grc.py            # Módulo 5: KPIs/KRIs
│   └── siem_dashboard_web.py       # Módulo 6: API REST web (puerto 8080)
├── logs/                           # Logs de autenticación simulados
├── siem_data/                      # Logs SOC avanzados + exportaciones JSON
├── lab_ransom/                     # Archivos para simulación ransomware
├── docs/
│   ├── 01_FASE1_Planeacion_Analisis.md
│   ├── 02_FASE2_Diseno.md
│   ├── 03_FASE3_Implementacion.md
│   ├── 04_FASE4_Herramientas_Lab.md
│   ├── 05_FASE5_Monitoreo_KPIs.md
│   ├── 06_Conclusiones_Recomendaciones.md
│   └── CREDENCIALES_Y_COMANDOS.md  # Referencia rápida de comandos manuales
├── dashboard_soc_actual.png        # Captura del dashboard en ejecución
└── Tarea_GRC_Semana5_TechGuard.docx  # Entregable Word del laboratorio
```

---

## Detener el laboratorio

```bash
# Detener contenedores (preserva datos)
docker compose down

# Limpiar todo (contenedores + volúmenes + imágenes)
docker compose down -v --remove-orphans
docker image rm grc-soc-lab 2>/dev/null || true
```

---

## Credenciales (entorno de laboratorio local — sin exposición externa)

| Contenedor | Puerto | Usuario | Contraseña |
|---|---|---|---|
| grc-soc-lab | SSH 2222 | root | GRC2026! |
| grc-soc-lab | SSH 2222 | student | Student2026! |
| grc-attacker | SSH 2223 | root | Attacker2026! |
| grc-siem | HTTP 8080 | — | — |

> Estas credenciales son intencionales para el laboratorio educativo. Los contenedores solo son accesibles desde `localhost` y no exponen servicios a internet.

---

*TechGuard Guatemala S.A. | GRC Semana 5 | Universidad Mariano Gálvez de Guatemala*
