import os
from langchain_community.vectorstores import Chroma
from utils.embeddings import get_embeddings_model
from utils.loader import load_and_chunk_documents

def initialize_vectorstore(persist_directory: str = "vectorstore", data_dir: str = "data"):
    """
    Initializes the Chroma vector store. If it doesn't exist, it processes documents
    from the data directory and persists them.
    """
    embeddings = get_embeddings_model()
    
    # If the directory exists and has files, load it. Otherwise, create new.
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print(f"Loading existing vector store from {persist_directory}...")
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    else:
        print(f"Initializing new vector store. Loading documents from {data_dir}...")
        chunks = load_and_chunk_documents(data_dir=data_dir)
        
        if not chunks:
            print("No documents to index. Please add PDFs to the data directory.")
            # Create an empty vector store to prevent errors
            vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
            return vectorstore

        print(f"Indexing {len(chunks)} chunks...")
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        print("Indexing complete.")
        
    return vectorstore

def get_retriever(vectorstore, search_kwargs={"k": 3}):
    """
    Returns a retriever interface for the vector store.
    """
    return vectorstore.as_retriever(search_kwargs=search_kwargs)
