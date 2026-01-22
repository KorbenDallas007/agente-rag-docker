import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Configuración (Simulamos que leemos la variable de entorno o la pedimos)
# IMPORTANTE: Asegúrate de tener tu API Key a mano si no está en el entorno
api_key = os.getenv("GROQ_API_KEY") 
if not api_key:
    # Si no está en variable de entorno, pégala aquí temporalmente para probar
    api_key = input("Introduce tu Groq API Key: ")

# 2. Inicializar el Modelo (El Cerebro)
llm = ChatGroq(
    temperature=0, 
    groq_api_key=api_key, 
    model_name="llama-3.3-70b-versatile"
)

# 3. Crear una Cadena (Chain) - El patrón básico
# Prompt Template: Es como una plantilla de correo
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en ciberseguridad sarcástico."),
    ("human", "{input}"),
])

# La magia de LangChain: El "Pipe" operator (|)
# Prompt -> Modelo
chain = prompt | llm

# 4. Ejecutar
print("🤖 Consultando a LangChain...")
response = chain.invoke({"input": "¿Por qué necesito usar Docker?"})

print("-" * 50)
print(response.content)
print("-" * 50)
