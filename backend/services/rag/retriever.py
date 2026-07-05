from pathlib import Path
from langchain_chroma import Chroma
from backend.services.rag.embeddings import get_embedding_model
from backend.utils.logger import logger

VECTOR_DB_PATH = Path("backend/knowledge/chroma_db")

def get_vector_database():

    embedding_model = get_embedding_model()

    vector_db = Chroma(
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=embedding_model,
    )

    return vector_db

def retrieve_documents(query: str, k: int = 3):

    vector_db = get_vector_database()

    logger.info("Retrieving company policies from vector database.")

    documents = vector_db.max_marginal_relevance_search(
    query,
    k=k,
    fetch_k=15,   
    lambda_mult=0.5  
)
    logger.info(f"Retrieved {len(documents)} policy documents.")

    return documents
