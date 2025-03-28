import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma  # Usamos Chroma en lugar de FAISS

load_dotenv()

# Ruta de la base de datos vectorial
VECTOR_DB_DIR = "backend/vector_db/"

# Cargar la base de datos vectorial
openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

try:
    # Usamos Chroma para cargar el índice (Nota: Chroma maneja la persistencia automáticamente)
    vector_store = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)  # Cargar el índice de Chroma
    print("✅ Índice cargado correctamente")
except Exception as e:
    print(f"❌ Error al cargar el índice: {e}")

# Función para recuperar información
def retrieve_context(query, k=3):
    """Busca los fragmentos más relevantes en la base de datos vectorial."""
    docs = vector_store.similarity_search(query, k=k)
    if not docs:
        print("❌ No se encontraron documentos relevantes.")
    else:
        print(f"✅ Se encontraron {len(docs)} documentos relevantes.")
    return "\n\n".join([doc.page_content for doc in docs])
