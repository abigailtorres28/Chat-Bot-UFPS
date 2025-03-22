import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Ruta de los documentos
DATA_DIR = "backend/data/"
VECTOR_DB_DIR = "backend/vector_db/"

# Función para cargar y procesar documentos
load_dotenv()
def load_and_store_documents():
    documents = []
    
    for file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file)
        
        if file.endswith(".pdf"):
            print(f"📄 Cargando PDF: {file}")
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())  # Cargar texto desde PDF
            
        elif file.endswith(".docx"):
            print(f"📝 Cargando DOCX: {file}")
            loader = Docx2txtLoader(file_path)
            documents.extend(loader.load())  # Cargar texto desde DOCX

    if not documents:
        print("⚠️ No se encontraron documentos en la carpeta data/")
        return
    
    # Dividir los documentos en fragmentos pequeños
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Crear embeddings y almacenar en FAISS
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Definir embeddings con la clave API
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_documents(texts, embeddings)
    vector_store.save_local(VECTOR_DB_DIR)

    print("✅ Documentos cargados y almacenados en FAISS")

# Ejecutar la carga
if __name__ == "__main__":
    load_and_store_documents()
