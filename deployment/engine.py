
import logging
from unsloth import FastLanguageModel

class UnslothModel:
    def __init__(self):
        # model_dir="Commercer/Llama-3.1-8B-Instruct-Tuned-not-4bit-Content-Creator"
        model_dir="unsloth/tinyllama-bnb-4bit"
        cache_dir = './HF_HOME'
        max_seq_length = 2**9
        load_in_4bit = True
        dtype = None

        # Initialize model and tokenizer
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_dir,
            max_seq_length=max_seq_length,
            dtype=dtype,
            load_in_4bit=load_in_4bit,
            cache_dir=cache_dir,
        )

        # Prepare model for inference
        FastLanguageModel.for_inference(self.model)

    def generate_response(self, text, max_new_tokens=64):
        # Prepare input
        inputs = self.tokenizer([text], return_tensors="pt").to("cuda")

        # Generate response
        outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens, use_cache=True)
        
        # Decode and return response
        return self.tokenizer.batch_decode(outputs)[0]

class UnslothEngine:
    def __init__(self, host="0.0.0.0", port=30000):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.process = None
        self.model = UnslothModel()
    
    def start_server(self):
        # Placeholder for potential server startup logic
        logging.info("Unsloth model initialized")
    
    def handle_request(self, messages):
        # Extract the last user message
        user_message = messages[-1]['content'] if messages else ""
        
        # Generate response using the Unsloth model
        response = self.model.generate_response(user_message)
        
        # Prepare response in OpenAI-compatible format
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": response
                }
            }]
        }

    def wait_for_server(self, timeout=900, interval=5):
        # Since this is a local model, we can simplify the waiting process
        logging.info("Unsloth model is ready!")
        return True

    def shutdown(self):
        # Cleanup if needed
        logging.critical("Unsloth model shutdown.")
        del self.model

# Optional: Add a request handler similar to OpenAIRequest if needed
class UnslothRequest:
    def __init__(self):
        self.engine = UnslothEngine()
    
    async def request_chat_completions(self, model="unsloth", messages=None, **kwargs):
        if messages is None:
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant"},
                {"role": "user", "content": "List 3 countries and their capitals."},
            ]
        
        # Generate response
        response = self.engine.handle_request(messages)
        
        # Yield the response
        yield response