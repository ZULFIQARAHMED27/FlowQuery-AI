# ui_core.py

import streamlit as st
from langchain_community.llms import Ollama  # ✅ FIXED - Direct Ollama import
from retrieval import process_file, get_context_for_query

def run_basic_doc_qa_ui():
    # ✅ FIXED - Use Ollama directly with your available mistral model
    llm = Ollama(model="mistral")

    uploaded_file = st.file_uploader("Upload for quick Q&A", type=["pdf", "txt"], key="basic")

    if "chunks_basic" not in st.session_state:
        st.session_state["chunks_basic"] = []

    if uploaded_file:
        st.session_state["chunks_basic"] = process_file(uploaded_file)
        st.success(f"Uploaded: {uploaded_file.name}")

    user_query = st.text_input("Ask your question here:", key="basic_query")

    if st.button("Answer", key="basic_btn") and user_query:
        if not st.session_state["chunks_basic"]:
            st.warning("Please upload a file first.")
        else:
            context = get_context_for_query(user_query, st.session_state["chunks_basic"])
            
            # ✅ FIXED - Create proper prompt and use Ollama directly
            prompt = f"""Based on the following context, answer the question clearly and concisely:

Context: {context}

Question: {user_query}

Answer:"""
            
            try:
                response = llm.invoke(prompt)  # Use invoke() method for Ollama
                
                st.markdown("### Answer")
                st.success(response)

                with st.expander("Retrieved Context"):
                    st.write(context)
                    
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")