import openlit
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Initialize OpenLIT
openlit.init(otlp_endpoint="http://127.0.0.1:4318",  collect_gpu_stats=True ,
pricing_json="/Users/murtazaicecreamwala/Documents/siyatech/rag/RAG-Agnostic-Guide/openlit/assets/pricing.json"
)

class OpenLitInference:
    def __init__(self, model_name: str = "llama3.2"):
        """Initialize Ollama client with OpenLIT instrumentation"""
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = Ollama(
            model=model_name,
            callback_manager=callback_manager,
            temperature=0.7,
            num_ctx=4096  # Context window size for llama2 3.2
        )
    
    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        print(openlit)
        """Generate text using Ollama with OpenLIT observability"""
        response = self.llm.invoke(prompt)
        return response

def main():
    # Start Prometheus metrics server
    from prometheus_client import start_http_server
    start_http_server(8000)
    print("Prometheus metrics server started on port 8000")
    
    # Initialize inference with Ollama
    inference = OpenLitInference(model_name="llama3.2")
    
    # Example prompts
    prompts = [
        "Explain quantum computing in simple terms.",
        "Write a haiku about artificial intelligence.",
        "What are the benefits of renewable energy?"
    ]
    
    # Generate responses with tracing
    for prompt in prompts:
        try:
            response = inference.generate(prompt)
            print(f"\nPrompt: {prompt}")
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error processing prompt: {str(e)}")

if __name__ == "__main__":
    main()
