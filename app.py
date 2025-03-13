from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar el modelo GPT-4o Mini
chat = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))

# Probar el chatbot
respuesta = chat.invoke("Hola, ¿cómo estás?")
print(respuesta.content)
