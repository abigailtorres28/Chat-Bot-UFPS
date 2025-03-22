import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

load_dotenv()

# Ruta de la base de datos vectorial
VECTOR_DB_DIR = "backend/vector_db/"

# Cargar la base de datos vectorial
openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key= openai_api_key)
vector_store = FAISS.load_local(VECTOR_DB_DIR, embeddings)

# Función para recuperar información
def retrieve_context(query, k=3):
    """Busca los fragmentos más relevantes en la base de datos vectorial."""
    docs = vector_store.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])
