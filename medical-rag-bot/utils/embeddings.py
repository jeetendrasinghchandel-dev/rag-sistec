from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embeddings_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Initializes and returns a HuggingFace embeddings model for local processing.
    This ensures no medical data is sent externally for embedding generation.
    """
    return HuggingFaceEmbeddings(model_name=model_name)
