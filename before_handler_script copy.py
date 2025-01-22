import os
import logging


# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def set_LLM_ENV():
    # LLM 
    ## Model Settings
    os.environ["MODEL_NAME"] = "unsloth/tinyllama-bnb-4bit"
    # os.environ["MODEL_REVISION"] = "your-revision"
    ## Tokiner Settings 
    # os.environ["TOKENIZER_NAME"] = "unsloth/tinyllama-bnb-4bit"
    # os.environ["TOKENIZER_REVISION"] = "your-tokenizer-revision"

def set_BitsAndBytes_ENV():
    ## Weights Settings
    os.environ["LOAD_FORMAT"] = "bitsandbytes"
    os.environ["MAX_MODEL_LEN"] = '512'
    os.environ["QUANTIZATION"] = "bitsandbytes"
    os.environ["TRUST_REMOTE_CODE"] = 'True'
    os.environ["DTYPE"] = "bfloat16"

def set_LoRA_ENV():
    ## LoRA Settings
    os.environ["ENABLE_LORA"] = 'True'
    os.environ["MAX_LORA_RANK"] = '64'


def before_handler_script():

    logging.info("I will run before the handler")

    # Set the environment variables
    set_LLM_ENV()
    set_BitsAndBytes_ENV()
    # set_LoRA_ENV()



ENV BASE_PATH="/runpod-volume" \
    HF_DATASETS_CACHE="/runpod-volume/huggingface-cache/datasets" \
    HUGGINGFACE_HUB_CACHE="/runpod-volume/huggingface-cache/hub" \
    HF_HOME="/runpod-volume/huggingface-cache/hub" \
    HF_HUB_ENABLE_HF_TRANSFER=1 
    
# LLM Settings
ENV TRUST_REMOTE_CODE=true \
    LOAD_FORMAT="bitsandbytes" \
    MAX_MODEL_LEN=2048 \
    QUANTIZATION="bitsandbytes"
    
ENV ENABLE_LORA = true
ENV MAX_LORA_RANK = 32

    
ENV MODEL_NAME="Commercer/Llama-3.1-8B-Instruct-Tuned-not-4bit-Content-Creator"



# ENV MODEL_REVISION="your-revision"
# ENV TOKENIZER_NAME="your-tokenizer"
# ENV TOKENIZER_REVISION="your-tokenizer-revision"

ENV PYTHONPATH="/:/vllm-workspace"