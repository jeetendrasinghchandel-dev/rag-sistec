import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_chunk_documents(data_dir: str = "data", chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Loads all PDF documents from the specified directory and splits them into chunks.
    """
    documents = []
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created directory: {data_dir}. Please add PDF files here.")
        return documents

    for filename in os.listdir(data_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(data_dir, filename)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
            
    if not documents:
        print(f"No PDF documents found in {data_dir}.")
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks
