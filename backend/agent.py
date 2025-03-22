# backend/agent.py
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import StateGraph
from retriever import retrieve_context
from dotenv import load_dotenv
import os

# Inicializar el modelo LLM
load_dotenv()
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))

# Definir el estado del agente
class ChatbotState:
    def __init__(self, query):
        self.query = query
        self.context = None
        self.response = None

# Definir nodo de recuperación de información
def retrieve_information(state: ChatbotState):
    state.context = retrieve_context(state.query)
    return state

# Definir nodo de generación de respuesta
def generate_response(state: ChatbotState):
    """Usa el LLM para mejorar la respuesta basada en el contexto obtenido."""
    messages = [
        SystemMessage(content="Eres un asistente experto en el reglamento académico y calendario de la UFPS."),
        HumanMessage(content=f"Pregunta: {state.query}\n\nContexto relevante:\n{state.context}\n\nRespuesta:")
    ]
    state.response = llm.predict_messages(messages).content
    return state

# Crear el flujo con LangGraph
graph = StateGraph(ChatbotState)
graph.add_node("retriever", retrieve_information)
graph.add_node("llm", generate_response)

# Definir el orden de ejecución: Primero recuperar, luego generar respuesta
graph.set_entry_point("retriever")
graph.add_edge("retriever", "llm")

# Compilar el grafo
executor = graph.compile()

# Función para ejecutar el agente
async def chatbot_agent(query):
    """Ejecuta el flujo conversacional con LangGraph."""
    initial_state = ChatbotState(query)
    final_state = executor.invoke(initial_state)
    return final_state.response
