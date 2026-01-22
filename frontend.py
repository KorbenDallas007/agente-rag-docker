import streamlit as st
import requests
import os

# --- CONFIGURACIÓN DE ARQUITECTO ---
# Ahora apuntamos a la raíz de la API, porque usaremos distintos endpoints
BASE_API_URL = os.getenv("API_URL", "http://127.0.0.1:8080")

# Ajuste de URL si viene con /embed (para compatibilidad con versiones previas)
if "/embed" in BASE_API_URL:
    BASE_API_URL = BASE_API_URL.replace("/embed", "")

CHAT_ENDPOINT = f"{BASE_API_URL}/agent/chat"

st.set_page_config(page_title="AI Architect Agent", page_icon="🕵️")

st.title("🕵️ Agente Autónomo con Herramientas")
st.caption(f"Arquitectura: Streamlit -> FastAPI (LangChain Agent) -> [Qdrant + Calculator]")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔐 Llave de Acceso")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    
    st.divider()
    st.info("Este agente puede:\n1. 🧮 Calcular matemáticas\n2. 🧠 Consultar su memoria (RAG)\n3. 💬 Charlar")

# --- HISTORIAL ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DEL CLIENTE (Thin Client) ---
if prompt := st.chat_input("Escribe tu orden (ej: 'Calcula 50*3' o '¿Qué es Docker?')..."):
    
    # 1. Validar Key
    if not api_key:
        st.warning("⚠️ Por favor ingresa tu API Key en la barra lateral.")
        st.stop()

    # 2. Mostrar mensaje usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Llamar al Backend (El Agente)
    with st.chat_message("assistant"):
        with st.spinner("🤖 El Agente está pensando y seleccionando herramientas..."):
            try:
                # Enviamos la Query y la Key al Backend
                payload = {"query": prompt, "api_key": api_key}
                response = requests.post(CHAT_ENDPOINT, json=payload)
                
                if response.status_code == 200:
                    agent_reply = response.json()["response"]
                    st.markdown(agent_reply)
                    
                    # Guardar respuesta
                    st.session_state.messages.append({"role": "assistant", "content": agent_reply})
                else:
                    st.error(f"Error del Servidor: {response.text}")
            
            except Exception as e:
                st.error(f"Error de Conexión: {e}")
