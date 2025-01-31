# model_warper.py
import os
import logging
logging.basicConfig(
    level=logging.INFO,       # Set the minimum logging level
    format='[%(levelname)s] %(message)s'  # Text-only format
)
rich_console = logging

from unsloth import FastLanguageModel

class UnslothModel:
    def __init__(self):
        """Initialize the Unsloth language model with comprehensive logging."""
        try:
            rich_console.info("Initializing UnslothModel")

            # Model configuration
            model_dir = "unsloth/tinyllama-bnb-4bit"
            model_dir = "Commercer/Aba-1.0-Large"

            self.model_id = model_dir
            cache_dir = '/runpod-volume/HF_HOME'

            # Model initialization with detailed logging
            rich_console.info(f"Loading model from {model_dir}")
            dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
            load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.
            # max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
            self.max_seq_length = 2**12 
            self.max_new_tokens = 2**7

            hf_token = os.environ.get('HF_TOKEN')
            hf_token_msg = f"using token: {hf_token[:5]}...{hf_token[-5:]}" if hf_token else 'No token found'
            rich_console.info(hf_token_msg)
            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=model_dir,
                max_seq_length=self.max_seq_length,
                dtype=dtype,
                load_in_4bit=load_in_4bit,
                cache_dir=cache_dir,
                token = hf_token
            )
            rich_console.info("Model initialized successfully")


            # Prepare model for inference
            FastLanguageModel.for_inference(self.model)
            info = "\n"+ "_"*70 + "\n" + "FastLanguageModel.for_inference"
            rich_console.info(info)
            self.processed_prompt_tokens = -1
            self.processed_completion_tokens = -1

        except Exception as e:
            rich_console.error(f"Model initialization failed: {e}", exc_info=True)
            raise

    def generate_response(self, prompt):
        """Generate a response with comprehensive logging."""
        try:
            rich_console.info(f"Generating response. Prompt length: {len(prompt)}")
            rich_console.debug(f"Prompt preview: {prompt[:100]}...")

            # Prepare input
            inputs = self.tokenizer([prompt], return_tensors="pt").to("cuda")

            # Generate response
            outputs = self.model.generate(**inputs, max_new_tokens=self.max_new_tokens, use_cache=True)
            response = self.tokenizer.batch_decode(outputs)[0]
            
            # Remove the prompt from the response
            response = response.replace(prompt, "")

            # Check and remove the BOS token if it exists
            bos_token = self.tokenizer.bos_token
            if bos_token and response.startswith(bos_token):
                response = response[len(bos_token):]
                
            rich_console.info(f"Response generated. Length: {len(response)}")
            rich_console.debug(f"Response preview: {response[:100]}...")

            # Calculate token usage
            self.processed_prompt_tokens  = len(prompt.split())
            self.processed_completion_tokens = len(response.split())
            return response

        except Exception as e:
            rich_console.error(f"Response generation failed: {e}", exc_info=True)
            raise
