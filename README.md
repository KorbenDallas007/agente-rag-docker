# 🤖 Autonomous AI Agent: RAG + Tools & Reasoning

> **Sistema Agéntico Autónomo capaz de razonar, seleccionar herramientas (Calculadora vs. Base Vectorial) y ejecutar tareas complejas. Orquestado con LangChain y desplegado en Microservicios Docker.**

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![LangChain](https://img.shields.io/badge/Orchestration-LangChain-green)
![AI](https://img.shields.io/badge/Model-Llama%203.3-orange)
![DB](https://img.shields.io/badge/Vector%20DB-Qdrant-red)

## 🧠 Arquitectura Funcional (Agentic Workflow)

A diferencia de un chatbot tradicional, este sistema no responde inmediatamente. Utiliza un patrón de **"Tool Calling"**: evalúa la intención del usuario y decide dinámicamente qué herramienta utilizar.

```mermaid
graph TD
    User((👤 Usuario))
    
    subgraph Frontend_Container ["🖥️ Frontend (Streamlit)"]
        UI[Chat Interface]
    end

    subgraph Backend_Container ["⚙️ Backend API (FastAPI + LangChain)"]
        Agent[🤖 Agent Brain]
        Router{⚡ Decision Node}
        
        subgraph Tools ["🧰 Herramientas"]
            Calc[🧮 Calculadora]
            Retriever[🔍 RAG Retriever]
        end
    end

    subgraph Data_Layer ["🗄️ Persistencia"]
        Qdrant[(Qdrant Vector DB)]
        Volume[💾 Docker Volume]
    end

    %% Flujo
    User --> UI
    UI -- "POST /agent/chat" --> Agent
    Agent --> Router
    
    Router -- "Math Query" --> Calc
    Router -- "Tech Query" --> Retriever
    
    Retriever -- "Vector Search" --> Qdrant
    Qdrant -.-> Volume
    
    Calc --> Agent
    Retriever --> Agent
    Agent -- "Final Answer" --> UI
```

## 🛠️ Capacidades del Agente

1.  **Razonamiento Matemático:**
    *   *Usuario:* "Calcula 1234 multiplicado por 5"
    *   *Agente:* Detecta intención matemática $\rightarrow$ Ejecuta herramienta `Calculadora` $\rightarrow$ Retorna resultado exacto.
2.  **Memoria Semántica (RAG):**
    *   *Usuario:* "¿Qué es Docker?"
    *   *Agente:* Detecta consulta técnica $\rightarrow$ Vectoriza la consulta $\rightarrow$ Busca en `Qdrant` $\rightarrow$ Sintetiza respuesta.
3.  **Charla General:**
    *   *Usuario:* "Hola, ¿quién eres?"
    *   *Agente:* Responde directamente sin invocar herramientas.

## 🏗️ Tech Stack

*   **Orquestación:** LangChain (Tool Calling Agent).
*   **Modelo (LLM):** Llama-3.3-70b-versatile (vía Groq API).
*   **Backend:** FastAPI con Inyección de Dependencias Segura.
*   **Frontend:** Streamlit (Thin Client pattern).
*   **Base de Datos:** Qdrant (Persistencia en disco vía Docker Volumes).
*   **Infraestructura:** Docker Compose (Red interna + Volúmenes).

## 🚀 Guía de Despliegue

### Requisitos
*   Docker & Docker Compose.
*   API Key de Groq.

### 1. Clonar y Desplegar
```bash
git clone https://github.com/KorbenDallas007/agente-rag-docker.git
cd agente-rag-docker

# Levantar toda la infraestructura
docker compose up --build -d
```

### 2. Ingesta de Conocimiento (ETL)
Carga los documentos base en la memoria del agente.
```bash
# Ejecutar localmente (requiere python 3)
pip install requests qdrant-client
python3 etl_pipeline.py
```

### 3. Usar el Agente
1.  Ve a `http://localhost:8501`.
2.  Ingresa tu **Groq API Key** en la barra lateral.
3.  ¡Ponlo a prueba!

## 📸 Demo

<img width="735" height="787" alt="image" src="https://github.com/user-attachments/assets/48e11dc4-8c96-41b9-a70e-a64db7c7a3f2" />


---
*Desarrollado por [KorbenDallas007](https://github.com/KorbenDallas007) - AI Solutions Architect Portfolio.*
```
