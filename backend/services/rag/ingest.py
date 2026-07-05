from pathlib import Path
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from backend.services.rag.embeddings import get_embedding_model


DOCUMENTS_PATH = Path("backend/knowledge/documents")
VECTOR_DB_PATH = Path("backend/knowledge/chroma_db")


loader = PyPDFDirectoryLoader(DOCUMENTS_PATH)

documents = loader.load()

#print(f"Loaded {len(documents)} pages")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(documents)

#print(f"Created {len(chunks)} chunks")


embedding_model = get_embedding_model()


Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=str(VECTOR_DB_PATH),
)

print("Knowledge base created successfully.")