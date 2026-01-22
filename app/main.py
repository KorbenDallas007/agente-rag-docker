from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services import EmbeddingModel
# Importamos el factory
from app.agent_service import get_agent_executor 

app = FastAPI(title="AI Agent Microservice")

# --- MODELOS ---
class TextRequest(BaseModel):
    text: str

class AgentRequest(BaseModel):
    query: str
    api_key: str 

class EmbedResponse(BaseModel):
    vector: list[float]

class AgentResponse(BaseModel):
    response: str

# --- SERVICIOS ---
embedding_service = EmbeddingModel()

@app.get("/")
def health():
    return {"status": "active", "service": "AI Agent API"}

@app.post("/embed", response_model=EmbedResponse)
def create_embedding(req: TextRequest):
    vector = embedding_service.get_embedding(req.text)
    return EmbedResponse(vector=vector)

@app.post("/agent/chat", response_model=AgentResponse)
def chat_with_agent(req: AgentRequest):
    try:
        # ARQUITECTURA LIMPIA:
        # Pasamos la Key explícitamente, sin variables globales mágicas.
        executor = get_agent_executor(groq_api_key=req.api_key)
        
        # Ejecutamos
        result = executor.invoke({"input": req.query})
        
        return AgentResponse(response=result["output"])
    except Exception as e:
        # Imprimimos el error en los logs del contenedor para verlo mejor
        print(f"❌ ERROR EN API: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
