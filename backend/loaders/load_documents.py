import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma  # Usamos Chroma en lugar de FAISS

# Cargar variables de entorno
load_dotenv()

# Rutas de almacenamiento
DATA_DIR = "backend/data/"
VECTOR_DB_DIR = "backend/vector_db/"

def load_and_store_documents():
    """Carga documentos, los procesa en fragmentos y los almacena en una base de datos vectorial (Chroma)."""
    if not os.path.exists(DATA_DIR):
        print("⚠️ La carpeta de documentos no existe.")
        return

    documents = []

    for file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file)
        try:
            if file.endswith(".pdf"):
                print(f"📄 Cargando PDF: {file}")
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())  # Cargar texto desde PDF
                
            elif file.endswith(".docx"):
                print(f"📝 Cargando DOCX: {file}")
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())  # Cargar texto desde DOCX

        except Exception as e:
            print(f"❌ Error al cargar {file}: {str(e)}")

    if not documents:
        print("⚠️ No se encontraron documentos válidos en la carpeta data/")
        return
    
    # Dividir los documentos en fragmentos pequeños
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    if not texts:
        print("⚠️ No se generaron fragmentos de texto.")
        return

    # Obtener API Key de OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ ERROR: No se encontró la clave de API de OpenAI.")
        return

    try:
        # Crear embeddings y almacenar en Chroma
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vector_store = Chroma.from_documents(texts, embeddings, persist_directory=VECTOR_DB_DIR)
        print("✅ Documentos cargados y almacenados en Chroma")
        
    except Exception as e:
        print(f"❌ Error al generar embeddings o almacenar en Chroma: {str(e)}")

# Ejecutar la carga
if __name__ == "__main__":
    load_and_store_documents()
