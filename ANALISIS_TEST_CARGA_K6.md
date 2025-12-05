# Análisis de Test de Carga – Microservicio Alumno (`/alumnos`)

## 1. Contexto de la prueba

- Herramienta: **k6** (CLI)
- Script utilizado: `spike_tests.js`
- Escenario configurado:

  - 10 s de rampa inicial hasta 10 VUs
  - 20 s de carga sostenida hasta 100 VUs
  - 10 s de bajada hasta 0 VUs

- Endpoint probado: `GET /alumnos`
- Entorno de ejecución:
  - Ejecución local en Windows 11
  - Backend: Flask + PostgreSQL (`sysacaddb`)
  - Microservicio expuesto en `http://127.0.0.1:5000`
  - Sin balanceadores ni otros microservicios en cascada

---

## 2. Resultados del spike test

Ejecución de referencia (salida de k6 resumida):

- **Total de requests** (`http_reqs`): ~1.688
- **Errores HTTP** (`http_req_failed`): `0.00 %`
- **Latencia** (`http_req_duration`):

  - Promedio: ~**3.37 ms**
  - p90: ~**3.99 ms**
  - p95: ~**4.23 ms**
  - Máxima: ~**8.02 ms**

- **Checks:**
  - `status 200`: **100 % OK**
  - `response is JSON`: **100 % OK**

- **Thresholds configurados en el script:**

  - `http_req_duration: p(95) < 500 ms` → **Cumplido**
  - `http_req_failed: rate < 0.01` → **Cumplido (0 %)**

---

## 3. Interpretación de los resultados

### 3.1 Rendimiento

- La latencia p95 por debajo de **5 ms** indica que el endpoint `GET /alumnos` responde **muy rápido** bajo el escenario de carga configurado.
- No se observaron timeouts ni respuestas 5xx, lo que sugiere que, para este nivel de concurrencia, la aplicación y la base de datos están correctamente dimensionadas.

### 3.2 Estabilidad

- `http_req_failed = 0.00 %` implica que no hubo:
  - Errores de red
  - Respuestas 5xx
  - Fallas de conexión
- Todas las respuestas cumplieron con:
  - Código HTTP 200
  - `Content-Type` compatible con `application/json`

Lo anterior es consistente con un microservicio **estable** en un entorno controlado de desarrollo.

---

## 4. Impacto en el diseño de la arquitectura

A partir de estos resultados:

1. **Lecturas rápidas y escalables**  
   - El cuello de botella no es la latencia del endpoint de lectura, sino, a futuro, la cantidad de conexiones concurrentes y la integración con otros microservicios.

2. **Necesidad de patrones adicionales (según consigna de cátedra)**  
   - Aunque el endpoint `/alumnos` escala bien en lectura simple, se incorporarán:

     - **Cache de objetos** (Redis/Dragonfly) para acelerar aún más las lecturas repetidas.
     - **Rate limiting** en endpoints de lectura y/o escritura para proteger ante picos descontrolados.
     - **Retry + Circuit Breaker** en llamadas a servicios externos (por ejemplo, futuros microservicios de documentos o gestión académica).

3. **12-Factor App y monitoreo**
   - La configuración por variables de entorno permite replicar esta prueba en otros entornos (staging/prod) cambiando solo URLs y credenciales.
   - La salida de k6 puede integrarse con Grafana para tener gráficos históricos de latencia y tasa de error.

---

## 5. Próximos pasos

1. Implementar **cache** de respuestas de `GET /alumnos` usando Redis/Dragonfly.
2. Agregar **rate limiting** en endpoints sensibles.
3. Diseñar un cliente HTTP interno con **Retry + Circuit Breaker** para integrar el microservicio de alumnos con otros microservicios (por ejemplo, generación de documentos o fichas).
4. Repetir pruebas de carga luego de aplicar cache y rate limit, para comparar resultados y documentar la mejora.
