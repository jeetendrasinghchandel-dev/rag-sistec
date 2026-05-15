import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from utils.retriever import initialize_vectorstore, get_retriever
from utils.prompt import meditrust_prompt

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="MediTrust AI - Safe Medical Assistant",
    page_icon="⚕️",
    layout="centered"
)

# Custom CSS for premium UI
st.markdown("""
<style>
    .reportview-container {
        background: #f4f7f6;
    }
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .safety-banner {
        background-color: #ffe6e6;
        color: #d93025;
        padding: 10px;
        border-radius: 8px;
        font-size: 0.9em;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #ffcccc;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚕️ MediTrust AI")
st.markdown('<div class="safety-banner">⚠️ <b>IMPORTANT:</b> For educational purposes only. Not a substitute for professional medical advice, diagnosis, or treatment. In an emergency, call your local emergency services immediately.</div>', unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

@st.cache_resource
def setup_rag_chain():
    """Initializes the RAG chain (Vectorstore, Retriever, LLM, Prompt)"""
    # 1. Initialize Vector Store
    vectorstore = initialize_vectorstore()
    retriever = get_retriever(vectorstore)
    
    # 2. Initialize LLM (Using Google Gemini as an example)
    # Ensure GOOGLE_API_KEY is in your .env file
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
    
    # 3. Create Chain
    combine_docs_chain = create_stuff_documents_chain(llm, meditrust_prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    
    return retrieval_chain

# Check for API Key
if not os.getenv("GOOGLE_API_KEY"):
    st.error("Please set your GOOGLE_API_KEY in the .env file to use the assistant.")
    st.stop()

# Initialize Chain
try:
    with st.spinner("Initializing MediTrust AI..."):
        rag_chain = setup_rag_chain()
except Exception as e:
    st.error(f"Error initializing system: {e}")
    st.stop()

# User Input
if prompt := st.chat_input("Ask your medical question based on verified sources..."):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Consulting verified sources..."):
            try:
                response = rag_chain.invoke({"input": prompt})
                answer = response["answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"An error occurred while generating the response: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
