import os
import requests
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

# --- 1. CONFIGURACIÓN ---
api_key = os.getenv("GROQ_API_KEY") 
if not api_key:
    # Si no la tienes exportada, te la pedirá al ejecutar
    api_key = input("Introduce tu Groq API Key: ")

# URLs de tu infraestructura (accedemos vía localhost porque estamos fuera del contenedor)
API_URL = "http://127.0.0.1:8080/embed"
QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "conocimiento_base"

# --- 2. DEFINICIÓN DE HERRAMIENTAS (TOOLS) ---

@tool
def calculadora(expresion: str) -> str:
    """Útil para realizar cálculos matemáticos precisos. 
    La entrada debe ser una expresión matemática simple como '2 + 2' o '34 * 12'."""
    try:
        # Usamos eval de python para resolver matemáticas
        return str(eval(expresion))
    except Exception as e:
        return f"Error calculando: {e}"

@tool
def consultar_base_conocimiento(pregunta: str) -> str:
    """Útil cuando necesitas buscar información técnica (Docker, Pizza, Python, Nubes, etc.)
    almacenada en la memoria vectorial."""
    print(f"\n   🕵️ [Tool Triggered] Consultando Qdrant para: '{pregunta}'...")
    
    try:
        # A. Vectorizar (Llamada a tu API)
        resp = requests.post(API_URL, json={"text": pregunta})
        if resp.status_code != 200: return "Error en API de Embeddings"
        vector = resp.json()["vector"]

        # B. Buscar (Llamada a Qdrant)
        search_url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search"
        payload = {"vector": vector, "limit": 1, "with_payload": True}
        search_resp = requests.post(search_url, json=payload)
        resultados = search_resp.json().get("result", [])

        if resultados:
            texto = resultados[0]["payload"]["contenido"]
            print(f"   ✅ [Tool Result] Encontrado: {texto[:50]}...")
            return f"Contexto encontrado: {texto}"
        else:
            print("   ⚠️ [Tool Result] Nada encontrado.")
            return "No encontré información relevante."
    except Exception as e:
        return f"Error de conexión: {e}"

# Lista de herramientas que le damos al robot
tools = [calculadora, consultar_base_conocimiento]

# --- 3. CEREBRO DEL AGENTE ---

llm = ChatGroq(
    temperature=0, # Precisión máxima
    groq_api_key=api_key, 
    model_name="llama-3.3-70b-versatile"
)

# --- 4. PROMPT DEL SISTEMA (La Personalidad) ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un Asistente Autónomo Avanzado. "
               "Tienes acceso a herramientas específicas. "
               "ANTES de responder, decide si necesitas usar una herramienta. "
               "Si es matemáticas -> Calculadora. "
               "Si es información -> Base de Conocimiento."),
    ("human", "{input}"),
    # El Scratchpad es donde el agente "piensa" y anota los pasos intermedios
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# --- 5. ENSAMBLAJE ---
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- 6. EJECUCIÓN DE PRUEBAS ---
def probar_agente(query):
    print(f"\n👤 PREGUNTA: {query}")
    print("." * 50)
    resultado = agent_executor.invoke({"input": query})
    print(f"🤖 RESPUESTA FINAL: {resultado['output']}")
    print("-" * 50)

if __name__ == "__main__":
    # Caso A: Matemáticas (Debería usar Calculadora)
    probar_agente("Calcula 250 multiplicado por 4")

    # Caso B: RAG (Debería usar Qdrant)
    probar_agente("¿Qué sabes sobre Docker?")

    # Caso C: Chat (No debería usar herramientas)
    probar_agente("Hola, ¿quién eres?")
