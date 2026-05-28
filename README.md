# DataExplorer — Demo de balanceo y métricas

## Resumen
Proyecto de ejemplo que muestra un backend simple (Flask) desplegado en 3 instancias, balanceado por Nginx, con métricas exportadas a Prometheus y visualizadas en Grafana.

## Objetivos del demo
- Mostrar cómo Nginx balancea peticiones entre 3 instancias del backend.
- Generar carga con JMeter y observar las métricas en Prometheus/Grafana.
- Proveer artefactos reproducibles para enseñanza (comandos, plan de JMeter, resultados).

## Estructura del repo
- [docker-compose.yml](docker-compose.yml) — orquestación (backend x3, nginx, prometheus, grafana)
- [backend/app.py](backend/app.py) — aplicación Flask con / y /metrics
- [backend/Dockerfile](backend/Dockerfile)
- [backend/requirements.txt](backend/requirements.txt)
- [nginx/nginx.conf](nginx/nginx.conf) — configuración del reverse-proxy
- [prometheus/prometheus.yml](prometheus/prometheus.yml)
- `apache-jmeter-5.6.3/` — binarios JMeter descargados
- `jmeter_test.jmx` — plan de prueba JMeter
- `jmeter_results.jtl` — resultados (generados por la prueba)

## Requisitos
- Docker Desktop (Windows) — asegurarse de que el daemon esté corriendo.
- Java 8+ (para JMeter)
- (Opcional) Permisos para ejecutar scripts y modificar PATH si quieres ejecutar `jmeter` desde cualquier lugar.

## Quickstart — Levantar la infraestructura
1. Arranca Docker Desktop y espera a que el daemon esté activo.
2. Desde la raíz del repo ejecuta:

```bash
docker-compose up --build -d
```

3. Comprueba que los contenedores están arriba:

```bash
docker ps
```

4. Verifica balanceo con curl repetido (deberías ver alternancia entre instancias):

```bash
# Ejecutar varias veces
curl http://localhost/
```

O en Windows PowerShell:

```powershell
for ($i=0; $i -lt 5; $i++) { Invoke-WebRequest http://localhost/ | Select-Object -Expand Content }
```

## Ejecutar la prueba de carga con JMeter (modo no-GUI)
Se incluye `jmeter_test.jmx` en la raíz del repo. Para ejecutar la prueba que generó 5.000 peticiones (50 hilos x 100 iteraciones):

```powershell
cd apache-jmeter-5.6.3\bin
.\jmeter.bat -n -t ..\..\jmeter_test.jmx -l ..\..\jmeter_results.jtl -Jthreads=50 -Jloops=100 -Jramp=10
```

- Resultado en `jmeter_results.jtl`. Puedes abrirlo con la GUI de JMeter (`jmeter.bat`) y cargar el archivo para ver gráficos.

## Métricas y Grafana
1. Abre Prometheus: http://localhost:9090 — consulta rápida:

```
backend_requests_total
```

2. Abre Grafana: http://localhost:3000 (admin/admin)
3. Añade DataSource: tipo `Prometheus`, URL: `http://prometheus:9090` (desde Grafana en contenedor). En la UI local de Grafana puedes usar `http://localhost:9090` si accedes desde fuera.
4. Panel sugerido (consulta):

```
sum by (instance) (rate(backend_requests_total[30s]))
```

Configura un panel de líneas para observar la tasa por instancia durante la prueba.

## Troubleshooting rápido
- Error: "unable to get image 'prom/prometheus:latest'... check if the daemon is running" → Arranca Docker Desktop.
- Nginx no inicia por error `unknown "proxy_add_x_forwarded" variable` → corregir `nginx/nginx.conf` a `$proxy_add_x_forwarded_for`.
- JMeter no reconocido: ejecuta desde `apache-jmeter-5.6.3\bin` o añade su `bin` al `PATH`.

## Archivos relevantes
- [docker-compose.yml](docker-compose.yml)
- [nginx/nginx.conf](nginx/nginx.conf)
- [jmeter_test.jmx](jmeter_test.jmx)
- [jmeter_results.jtl](jmeter_results.jtl)
