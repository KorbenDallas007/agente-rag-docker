# 🤖 AI Solutions Architect Agent: RAG con Docker & Llama 3

Este proyecto implementa una arquitectura **RAG (Retrieval-Augmented Generation)** completa, agnóstica a la nube y contenerizada. Diseñada para demostrar patrones de **Ingeniería de Software aplicados a IA Generativa**.

![Arquitectura RAG](https://img.shields.io/badge/Architecture-RAG-blue) ![Docker](https://img.shields.io/badge/Docker-Containerized-blue) ![Model](https://img.shields.io/badge/LLM-Llama%203-orange)

## 🏗️ Arquitectura de la Solución

El sistema sigue un diseño de microservicios desacoplados:

1.  **Frontend (Cliente):** Interfaz web construida con **Streamlit**. Gestiona el chat y la configuración de API Keys.
2.  **Backend (Embeddings API):** Servicio REST con **FastAPI**. Convierte texto en vectores (optimizado para entornos ligeros).
3.  **Vector Database (Memoria):** Instancia de **Qdrant** corriendo en Docker. Almacena el conocimiento semántico.
4.  **GenAI Engine (Cerebro):** Integración con **Groq API** para inferencia ultrarrápida usando **Llama 3.3**.

### 🛠️ Tech Stack

*   **Lenguaje:** Python 3.9+
*   **Contenerización:** Docker & Docker Network
*   **Orquestación:** Scripts Python (ETL & Agent)
*   **IA / ML:**
    *   *LLM:* Llama-3.3-70b-versatile (vía Groq)
    *   *Vector Store:* Qdrant
    *   *Framework:* Requests (HTTP REST puro para máxima compatibilidad)

## 🚀 Cómo ejecutarlo (Quickstart)

Esta arquitectura utiliza **Docker Compose** para orquestar los microservicios y garantizar la persistencia de datos.

### Requisitos
*   Docker instalado.
*   Una API Key de Groq (Gratuita).

### Pasos

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/KorbenDallas007/agente-rag-docker.git
    cd agente-rag-docker
    ```

2.  **Desplegar la Arquitectura (Un solo comando):**
    ```bash
    docker compose up --build -d
    ```
    *Esto levantará:*
    *   🖥️ **Frontend:** http://localhost:8501
    *   ⚙️ **API:** http://localhost:8080
    *   🗄️ **Qdrant:** http://localhost:6333

3.  **Ingestar Conocimiento (ETL):**
    *Este script carga los datos iniciales en la base vectorial.*
    ```bash
    # (Opcional) Crea un entorno virtual si lo ejecutas localmente fuera de Docker
    pip install -r requirements.txt
    python3 etl_pipeline.py
    ```

4.  **Acceder:**
    Abre tu navegador en `http://localhost:8501`.

## 📸 Demo

<img width="774" height="803" alt="image" src="https://github.com/user-attachments/assets/8fc097f1-3271-4b18-a61f-e36871f4e8a9" />


---
*Desarrollado como parte del entrenamiento avanzado para AI Solutions Architect.*
