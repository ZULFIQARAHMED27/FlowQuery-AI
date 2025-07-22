# llm_wrapper.py
"""
LLM Wrapper to interface with local Ollama models like Mistral.
Sends prompt and context to Ollama's HTTP API and retrieves the response.
"""

import requests

class LocalLLM:
    def __init__(self, model_name="mistral"):
        self.base_url = "http://localhost:11434/api/generate"
        self.model = model_name

    def generate_answer(self, context, question):
        """
        Generates an answer using the local Ollama LLM (e.g. Mistral).

        Args:
            context (str): Retrieved context from documents.
            question (str): User's question.

        Returns:
            str: Generated answer.
        """
        prompt = f"""Use the context below to answer the question:

        Context: {context}

        Question: {question}
        """
        try:
            response = requests.post(self.base_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })

            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                return f"[LLM ERROR] Status Code {response.status_code}: {response.text}"

        except Exception as e:
            return f"[LLM ERROR] Failed to reach Ollama server: {str(e)}"
