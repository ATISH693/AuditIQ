from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Load the embedding model.

    Returns:
        HuggingFaceEmbeddings
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    return embedding_model
