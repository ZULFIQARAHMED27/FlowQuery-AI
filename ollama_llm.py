# ollama_llm.py
import requests

class OllamaLLM:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name

    def generate_answer(self, question, context):
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": self.model_name, "prompt": prompt, "stream": False},
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"[LLM ERROR] Status Code {response.status_code}: {response.text}"
