import requests
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

# --- CONFIGURACIÓN DE RED DOCKER ---
API_INTERNAL_URL = "http://localhost:8000/embed"
QDRANT_INTERNAL_URL = "http://qdrant:6333"
COLLECTION_NAME = "conocimiento_base"

# --- DEFINICIÓN DE HERRAMIENTAS ---
@tool
def calculadora(expresion: str) -> str:
    """Útil para realizar cálculos matemáticos precisos."""
    try:
        return str(eval(expresion))
    except Exception as e:
        return f"Error: {e}"

@tool
def consultar_base_conocimiento(pregunta: str) -> str:
    """Útil para buscar información técnica en la memoria vectorial (Qdrant)."""
    try:
        # 1. Vectorizar
        resp = requests.post(API_INTERNAL_URL, json={"text": pregunta})
        if resp.status_code != 200: return "Error vectorizando"
        vector = resp.json()["vector"]

        # 2. Buscar en Qdrant
        search_url = f"{QDRANT_INTERNAL_URL}/collections/{COLLECTION_NAME}/points/search"
        payload = {"vector": vector, "limit": 1, "with_payload": True}
        search_resp = requests.post(search_url, json=payload)
        resultados = search_resp.json().get("result", [])

        if resultados:
            return f"Contexto encontrado: {resultados[0]['payload']['contenido']}"
        else:
            return "No hay info relevante."
    except Exception as e:
        return f"Error conectando a servicios internos: {e}"

# --- FACTORY DEL AGENTE (AHORA CON INYECCIÓN EXPLÍCITA) ---
def get_agent_executor(groq_api_key: str):
    # Ya no leemos os.getenv. Usamos lo que nos pasan por parámetro.
    if not groq_api_key:
        raise ValueError("La API Key llegó vacía al Factory del Agente")

    llm = ChatGroq(
        temperature=0, 
        groq_api_key=groq_api_key, # <--- Aquí se usa directamente
        model_name="llama-3.3-70b-versatile"
    )

    tools = [calculadora, consultar_base_conocimiento]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un Agente de IA experto. "
                   "Usa la calculadora para números. "
                   "Usa la base de conocimiento para temas técnicos."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
