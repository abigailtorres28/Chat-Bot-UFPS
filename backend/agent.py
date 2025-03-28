# agent.py
from retriever import retrieve_context
from langchain.agents import ConversationalAgent
from langchain.schema import SystemMessage, HumanMessage  
from langchain_openai import ChatOpenAI
import os
# Inicialización del modelo de OpenAI
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))

# Función para manejar el flujo de datos y generar respuestas asincrónicas
async def chatbot_agent(query):
    """Función para procesar el flujo de LangChain y retornar una respuesta."""
    
    # 1. Recuperamos el contexto utilizando la función de recuperación
    context = retrieve_context(query)
    print(f"contexto: {context}")

    # 2. Generamos la respuesta utilizando el modelo de OpenAI
    messages = [
        SystemMessage(content="Eres un asistente experto en el reglamento académico y calendario de la UFPS."),
        HumanMessage(content=f"Pregunta: {query}\n\nContexto relevante:\n{context}\n\nRespuesta:")
    ]
    
    # Obtenemos la respuesta del modelo de manera asincrónica
    response = await llm.ainvoke(messages)
    
    # Extraemos el contenido de la respuesta (texto)
    if response and hasattr(response, "content"):
        response_text = response.content
    else:
        response_text = "No se pudo generar una respuesta."
    
    # Imprimir la respuesta generada en la consola
    print(f"Respuesta generada: {response_text}")
    
    # 3. Devolvemos la respuesta en formato diccionario
    return {"response": response_text}