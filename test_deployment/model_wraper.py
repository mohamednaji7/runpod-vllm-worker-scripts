# model_api.py
import os
if os.environ.get('SCRIPT_NAME') is not None:
    import logging
    # Configure logging to output plain text to stdout
    logging.basicConfig(
        level=logging.DEBUG,       # Set the minimum logging level
        format='[%(levelname)s] %(message)s'  # Text-only format
    )
    rich_console = logging

else:
    from rich_console import Rich_Console
    rich_console = Rich_Console()

from unsloth import FastLanguageModel

class UnslothModel:
    def __init__(self):
        """Initialize the Unsloth language model with comprehensive logging."""
        try:
            rich_console.info("Initializing UnslothModel")

            # Model configuration
            model_dir = "unsloth/tinyllama-bnb-4bit"
            self.model_id = model_dir
            cache_dir = './HF_HOME'

            # Model initialization with detailed logging
            rich_console.info(f"Loading model from {model_dir}")
            dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
            load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.
            max_seq_length = 1024 # Choose any! We auto support RoPE Scaling internally!

            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=model_dir,
                max_seq_length=max_seq_length,
                dtype=dtype,
                load_in_4bit=load_in_4bit,
                cache_dir=cache_dir,
            )
            rich_console.info("Model initialized successfully")


            # Prepare model for inference
            rich_console.info("\n", "_"*50, "\n")
            rich_console.info("FastLanguageModel.for_inference")
            FastLanguageModel.for_inference(self.model)
            self.processed_prompt_tokens = -1
            self.processed_completion_tokens = -1

        except Exception as e:
            rich_console.error(f"Model initialization failed: {e}", exc_info=True)
            raise

    def generate_response(self, prompt, max_new_tokens=128):
        """Generate a response with comprehensive logging."""
        try:
            rich_console.info(f"Generating response. Prompt length: {len(prompt)}")
            rich_console.debug(f"Prompt preview: {prompt[:100]}...")

            # Prepare input
            inputs = self.tokenizer([prompt], return_tensors="pt").to("cuda")

            # Generate response
            outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens, use_cache=True)
            response = self.tokenizer.batch_decode(outputs)[0]

            rich_console.info(f"Response generated. Length: {len(response)}")
            rich_console.debug(f"Response preview: {response[:100]}...")

            # Calculate token usage
            self.processed_prompt_tokens  = len(prompt.split())
            self.processed_completion_tokens = len(response.split())
            return response

        except Exception as e:
            rich_console.error(f"Response generation failed: {e}", exc_info=True)
            raise

if __name__ == "__main__":
    UnslothModel()
