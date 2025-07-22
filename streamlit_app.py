import streamlit as st
import os
import sys
import traceback
import tempfile

from ui_core import run_basic_doc_qa_ui
from rag import RAGSystem
from retrieval import process_documents, embedding_model
from langchain_community.llms import Ollama  # ✅ FIXED - Use standard Ollama import

st.set_page_config(page_title="🔥 FlowQuery", layout="wide")
st.title("🔥 FlowQuery - AI Document Assistant")

# === Sidebar: Upload & Index ===
st.sidebar.header("📄 Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose file", type=["pdf", "txt", "docx", "json"])

index_name = st.sidebar.text_input("Index Name", value="faiss_index")

if uploaded_file and st.sidebar.button("🚀 Ingest & Index"):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Indexing document..."):
        success = process_documents(tmp_path, index_name, embedding_model)
        if success:
            st.sidebar.success("✅ Indexed successfully!")
        else:
            st.sidebar.error("❌ Indexing failed.")

# === Main Q&A Interface ===
st.markdown("---")
st.subheader("🔍 Ask Questions from Uploaded Documents")
query = st.text_input("Your Question:", "")
num_results = st.slider("Top Results", min_value=1, max_value=10, value=5)


if st.button("🔍 Get Answer", disabled=not query.strip()):
    try:
        with st.spinner("Searching..."):
            llm = Ollama(model="mistral")  # ✅ FIXED - Use your available model
            rag = RAGSystem(index_name, llm=llm)
            results = rag.query(query, k=num_results)

        if results and "formatted_docs" in results:
            st.markdown("### 📄 Retrieved Docs")
            st.code(results["formatted_docs"], language="text")

            if results.get("answer"):
                st.markdown("### 🤖 Answer")
                st.success(results["answer"])
            else:
                st.info("No answer generated.")
        else:
            st.warning("No relevant documents found.")

    except FileNotFoundError:
        st.error(f"Index '{index_name}' not found.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.error(traceback.format_exc())

# === Optional: Lightweight Text Q&A from ui_core ===
st.markdown("---")
st.subheader("🧠 Quick Q&A with a File (No Indexing)")
run_basic_doc_qa_ui()