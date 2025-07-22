import pickle
import os
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class RAGSystem:
    def __init__(self, index_name, llm=None):
        self.index_name = index_name
        self.llm = llm or Ollama(model="mistral")
        self.vector_store = self._load_index()
        
    def _load_index(self):
        """Load the FAISS index from disk"""
        index_path = f"{self.index_name}.pkl"
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file {index_path} not found. Please upload and index a document first.")
        
        with open(index_path, "rb") as f:
            return pickle.load(f)
    
    def query(self, question, k=5):
        """Query the RAG system"""
        if not self.vector_store:
            return {"error": "No vector store available"}
        
        # Create retriever
        retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
        
        # Create a custom prompt template
        prompt_template = """Use the following context to answer the question. If you cannot find the answer in the context, say "I cannot find the answer in the provided context."

Context: {context}

Question: {question}

Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create the QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
        try:
            # Get the answer
            result = qa_chain({"query": question})
            
            # Format the source documents
            source_docs = result.get("source_documents", [])
            formatted_docs = "\n\n".join([
                f"Document {i+1}:\n{doc.page_content[:500]}..."
                for i, doc in enumerate(source_docs)
            ])
            
            return {
                "answer": result.get("result", "No answer generated"),
                "source_documents": source_docs,
                "formatted_docs": formatted_docs
            }
            
        except Exception as e:
            return {"error": f"Error during query: {str(e)}"}