# MediTrust AI - Safe Medical RAG Assistant

A robust, AI-powered medical FAQ assistant using Retrieval-Augmented Generation (RAG). The system exclusively sources information from verified health authorities to provide safe, reliable, and citation-based answers.

## Features
- **Strict Guardrails**: Refuses unauthorized advice, self-diagnosis, or emergency treatment.
- **Verified Sources Only**: Answers strictly from the provided PDF documents.
- **Citations**: Provides Document Name, Page Number, and Chunk ID.
- **Local Embeddings**: Uses HuggingFace sentence-transformers locally to ensure data privacy during indexing.
- **Streamlit UI**: Clean and safe interface with persistent disclaimers.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GOOGLE_API_KEY="your-api-key-here"
   ```

3. **Add Data**
   Place your verified medical PDF documents (e.g., WHO guidelines) into the `data/` directory.

4. **Run the App**
   ```bash
   streamlit run app.py
   ```
   The first time you run the app, it will automatically process the PDFs in `data/`, generate embeddings, and create a local vector store in the `vectorstore/` directory.
