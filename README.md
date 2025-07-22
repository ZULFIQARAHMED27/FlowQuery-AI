# 🔥 FlowQuery - AI Document Assistant

An intelligent document Q&A system that combines semantic search with LLM-powered answer generation using Ollama.

## Features

### 🔍 Semantic Search
- Upload PDF, TXT, DOCX, or JSON documents
- Advanced document chunking and embedding
- FAISS vector database for fast similarity search
- Retrieve most relevant document sections

### 🤖 AI-Powered Q&A
- **LLM Integration**: Uses Ollama with Mistral model for intelligent answers
- **RAG System**: Retrieval-Augmented Generation for accurate responses
- **Context-Aware**: Answers based on your uploaded documents
- **Dual Interface**: 
  - Full indexing with persistent storage
  - Quick Q&A without indexing

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/FlowQuery_App.git
cd FlowQuery_App
```

2. **Install Python dependencies**
```bash
pip install streamlit langchain langchain-community faiss-cpu sentence-transformers numpy PyPDF2
```

3. **Install and setup Ollama**
```bash
# Install Ollama from https://ollama.ai
# Pull the Mistral model
ollama pull mistral
```

# NOTE : Install all dependencies
pip install -r requirements.txt

# Install Ollama separately (not available via pip)
# Download from: https://ollama.ai
# Then pull the model:
ollama pull mistral

## Usage

1. **Start the application**
```bash
streamlit run streamlit_app.py
```

2. **Upload & Index Documents**
   - Use the sidebar to upload documents
   - Click "🚀 Ingest & Index" to create searchable database
   - Documents are stored as FAISS indexes

3. **Ask Questions**
   - **Main Interface**: Query indexed documents with AI-generated answers
   - **Quick Q&A**: Direct questioning without permanent indexing
   - Adjust "Top Results" slider to control context size

## Technical Details

- **Embeddings**: `all-MiniLM-L6-v2` for semantic understanding
- **Vector Store**: FAISS for efficient similarity search  
- **LLM**: Ollama Mistral for answer generation
- **Framework**: Streamlit for the web interface
- **Document Processing**: PyPDF2, custom text splitters

## Requirements

- Python 3.8+
- Ollama with Mistral model
- 4GB+ RAM recommended
- GPU optional (CPU works fine)

## Previous Version

The previous version supported semantic search only. This version adds:
- ✅ LLM integration with Ollama
- ✅ AI-generated answers
- ✅ RAG (Retrieval-Augmented Generation)
- ✅ Enhanced error handling
- ✅ Dual Q&A interfaces

## Contributing

Feel free to open issues and pull requests for improvements!
