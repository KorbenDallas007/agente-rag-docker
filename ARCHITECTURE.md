# 🏛️ Architecture Decision Record (ADR)

Este documento describe las decisiones de arquitectura tomadas para el proyecto **Agentic RAG System**, alineadas con los pilares del **AWS Well-Architected Framework**.

## 1. Operational Excellence (Excelencia Operativa)
*   **Infrastructure as Code (IaC):** Toda la infraestructura (Redes, Computación) está definida en **Terraform**, permitiendo despliegues repetibles y versionados, eliminando la configuración manual ("ClickOps").
*   **CI/CD Pipeline:** Se utiliza **GitHub Actions** para automatizar la integración y validación del código. Cada commit dispara un proceso de construcción de contenedores y pruebas de humo (sanity checks) antes del despliegue.
*   **Containerization:** El uso de **Docker** garantiza la paridad entre los entornos de desarrollo local y producción en la nube.

## 2. Security (Seguridad)
*   **Authentication:** La API está protegida mediante un middleware de **API Key** personalizada, previniendo acceso no autorizado a los endpoints de inferencia.
*   **Network Isolation:** En el diseño de producción (Terraform/K8s), los servicios de Backend y Base de Datos residen en subredes privadas, expuestos únicamente a través de un Load Balancer (Frontend) o API Gateway.
*   **Secrets Management:** Las credenciales sensibles (Groq API Key) se inyectan en tiempo de ejecución y no están hardcodeadas en el código fuente.

## 3. Reliability (Fiabilidad)
*   **State Management:** La persistencia de datos vectoriales se desacopla del ciclo de vida del contenedor mediante **Docker Volumes (PVCs en K8s)**, garantizando que el reinicio o fallo de un nodo no resulte en pérdida de conocimiento.
*   **Self-Healing:** Se utilizan orquestadores (Docker Compose / Kubernetes) con políticas de `restart: always` y `Liveness Probes` para detectar y recuperar servicios fallidos automáticamente.
*   **High Availability (Design):** El manifiesto de Kubernetes está diseñado para soportar `replicas: N`, permitiendo el balanceo de carga y tolerancia a fallos de instancias individuales.

## 4. Performance Efficiency (Rendimiento)
*   **Model Offloading:** Se delega la inferencia pesada (LLM) a APIs especializadas (Groq/LPU), liberando la CPU local para la lógica de negocio y reduciendo la latencia de inferencia a milisegundos.
*   **Vector Search Optimization:** Se utiliza **Qdrant** como motor especializado, optimizado con índices HNSW para recuperación de información en tiempo O(log N).

## 5. Cost Optimization (Costos)
*   **Cloud Agnostic Design:** La arquitectura contenerizada permite desplegar en la nube con mejor relación precio/rendimiento (ej. OCI Ampere Instances) sin refactorizar código.
*   **Resource Scaling:** El diseño permite escalar el Frontend y el Backend independientemente según la demanda, evitando el sobre-aprovisionamiento de recursos monolíticos.

## 6. Sustainability (Sostenibilidad)
*   **Efficient Compute:** La arquitectura es compatible con procesadores ARM64 (AWS Graviton / OCI Ampere), que ofrecen mejor rendimiento por watt que la arquitectura x86 tradicional.

### Site Reliability Engineering (SRE) Strategy - GCP Alignment
Para entornos de producción en Google Cloud, se definen las siguientes métricas de éxito basadas en el framework de SRE:

*   **SLI (Indicator):** Latencia de respuesta del endpoint `/agent/chat` y Tasa de Errores (HTTP 5xx).
*   **SLO (Objective):**
    *   *Latencia:* El 90% de las consultas deben completarse en < 3000ms (excluyendo el tiempo de generación del LLM externo).
    *   *Disponibilidad:* 99.9% de uptime mensual (permitiendo ~43 min de caída/mes para mantenimiento).
*   **Error Budget Policy:** Si la tasa de errores supera el SLO, se congela el despliegue de nuevas "Features" y el equipo se enfoca exclusivamente en estabilidad y deuda técnica.
