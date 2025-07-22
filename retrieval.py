# retrieval.py
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain_community.llms import Ollama
import os
import pickle
import sentence_transformers


# Initialize embedding model once
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Global FAISS index (can also be persisted if needed)
vector_store = None

def process_file(uploaded_file):
    if hasattr(uploaded_file, 'name') and uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        text = uploaded_file.read().decode("utf-8")

    # Wrap into LangChain Documents
    document = Document(page_content=text)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents([document])
    return chunks

def process_documents(file_path, index_name, embed_model):
    global vector_store

    if not os.path.exists(file_path):
        return False

    with open(file_path, "rb") as f:
        docs = process_file(f)

    # Build FAISS index
    vector_store = FAISS.from_documents(docs, embed_model)

    # Optional: Save index to disk
    with open(f"{index_name}.pkl", "wb") as f:
        pickle.dump(vector_store, f)

    return True

def get_context_for_query(query, chunks):
    # Embed the query
    query_embedding = embedding_model.embed_query(query)

    # Embed all chunks
    chunk_embeddings = [embedding_model.embed_query(chunk.page_content) for chunk in chunks]

    # Compute cosine similarity manually
    from numpy import dot
    from numpy.linalg import norm
    similarities = [
        (dot(query_embedding, chunk_emb) / (norm(query_embedding) * norm(chunk_emb)), chunk)
        for chunk_emb, chunk in zip(chunk_embeddings, chunks)
    ]

    # Sort by similarity score (descending)
    top_chunks = sorted(similarities, key=lambda x: x[0], reverse=True)[:3]

    return "\n\n".join([chunk.page_content for _, chunk in top_chunks])
