# agent.py
import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from retriever import retrieve_context

# Definimos el estado del agente
class ChatbotState(TypedDict):
    query: str
    context: str
    response: str

# Inicializamos el modelo de OpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

async def retrieve_context_node(state: ChatbotState):
    """Nodo asincrónico para recuperar el contexto relevante para la pregunta con manejo de errores."""
    try:
        context = retrieve_context(state["query"])  
        if not context:
            raise ValueError("No se encontró contexto relevante.")
        #print(f"Contexto recuperado: {context}")
        return {"context": context}
    except Exception as e:
        print(f"Error en la recuperación del contexto: {e}")
        return {"context": "No se pudo recuperar información relevante."}

async def generate_response_node(state: ChatbotState):
    """Nodo asincrónico que genera la respuesta basada en el contexto recuperado con manejo de errores."""
    try:
        messages = [
            SystemMessage(content="Eres un asistente experto en el reglamento academico y calendario de la UFPS, evita responder pregunta que esten fuera del contexto del "
                          "reglamento y el calendario"),
            HumanMessage(content=f"Pregunta: {state['query']}\n\nContexto relevante:\n{state['context']}\n\nRespuesta:")
        ]
        
        response = await llm.ainvoke(messages)  # Llamada asincrónica
        response_text = response.content.strip() if response and response.content else "El modelo no generó una respuesta válida."
        
        #print(f"Respuesta generada: {response_text}")
        return {"response": response_text}
    except Exception as e:
        print(f"Error en la generación de respuesta: {e}")
        return {"response": "Lo siento, hubo un error al generar la respuesta."}

# Crear el flujo de trabajo con LangGraph
workflow = StateGraph(ChatbotState)

# Definir nodos
workflow.add_node("retrieve_context", retrieve_context_node)
workflow.add_node("generate_response", generate_response_node)

# Conectar nodos
workflow.set_entry_point("retrieve_context")
workflow.add_edge("retrieve_context", "generate_response")
workflow.add_edge("generate_response", END)

# Compilar el flujo de trabajo
app = workflow.compile()

# Función asincrónica para ejecutar el chatbot
async def chatbot_agent(query: str):
    """Ejecuta el agente con la consulta del usuario y maneja errores globales."""
    try:
        state = {"query": query}
        result = await app.ainvoke(state)  # Llamada asincrónica
        return result["response"]
    except Exception as e:
        print(f"Error general en el chatbot: {e}")
        return "Lo siento, ocurrió un error inesperado."

