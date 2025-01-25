# engine.py
import os
import time
import logging
import torch
from unsloth import FastLanguageModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('unsloth_engine.log')
    ]
)
logger = logging.getLogger(__name__)

class UnslothModel:
    def __init__(self):
        """Initialize the Unsloth language model with comprehensive logging."""
        try:
            logger.info("Initializing UnslothModel")
            
            # Model configuration
            model_dir = "unsloth/tinyllama-bnb-4bit"
            cache_dir = './HF_HOME'

            # Model initialization with detailed logging
            logger.info(f"Loading model from {model_dir}")
            dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
            load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.
            max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!

            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=model_dir,
                max_seq_length=max_seq_length,
                dtype=dtype,
                load_in_4bit=load_in_4bit,
                cache_dir=cache_dir,
            )
            
            # Prepare model for inference
            FastLanguageModel.for_inference(self.model)
            logger.info("Model initialized successfully")
        
        except Exception as e:
            logger.error(f"Model initialization failed: {e}", exc_info=True)
            raise

    def generate_response(self, prompt, max_new_tokens=128):
        """Generate a response with comprehensive logging."""
        try:
            logger.info(f"Generating response. Prompt length: {len(prompt)}")
            logger.debug(f"Prompt preview: {prompt[:100]}...")

            # Prepare input
            inputs = self.tokenizer([prompt], return_tensors="pt").to("cuda")
            
            # Generate response
            outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens, use_cache=True)
            response = self.tokenizer.batch_decode(outputs)[0]

            logger.info(f"Response generated. Length: {len(response)}")
            logger.debug(f"Response preview: {response[:100]}...")
            
            return response
        
        except Exception as e:
            logger.error(f"Response generation failed: {e}", exc_info=True)
            raise

class UnslothEngine:
    def __init__(self):
        """Initialize UnslothEngine with logging."""
        logger.info("Initializing UnslothEngine")
        self.model = UnslothModel()

    def format_messages(self, messages):
        """Convert OpenAI-style messages to a single prompt string with logging."""
        try:
            logger.info(f"Formatting {len(messages)} messages")
            prompt = ""
            for msg in messages:
                role = msg['role']
                content = msg['content']
                
                if role == 'system':
                    prompt += f"System: {content}\n"
                elif role == 'user':
                    prompt += f"Human: {content}\n"
                elif role == 'assistant':
                    prompt += f"Assistant: {content}\n"
            
            prompt += "Assistant:"
            logger.debug(f"Formatted prompt: {prompt}")
            return prompt
        
        except Exception as e:
            logger.error(f"Message formatting failed: {e}", exc_info=True)
            raise

    def handle_request(self, messages):
        """Handle OpenAI-compatible request with comprehensive logging."""
        try:
            logger.info("Handling request")
            
            # Format messages
            formatted_prompt = self.format_messages(messages)
            
            # Generate response
            response = self.model.generate_response(formatted_prompt)
            
            # Prepare OpenAI-compatible response
            openai_response = {
                "id": f"chatcmpl-{os.urandom(16).hex()}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "unsloth/tinyllama-bnb-4bit",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response.strip()
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": len(formatted_prompt.split()),
                    "completion_tokens": len(response.split()),
                    "total_tokens": len(formatted_prompt.split()) + len(response.split())
                }
            }
            
            logger.info("Request handled successfully")
            return openai_response
        
        except Exception as e:
            logger.error(f"Request handling failed: {e}", exc_info=True)
            return {
                "error": {
                    "message": str(e),
                    "type": "invalid_request_error",
                    "param": None,
                    "code": None
                }
            }