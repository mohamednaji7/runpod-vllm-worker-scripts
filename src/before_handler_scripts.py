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

def set_HF_VARs():
    BASE_PATH = "runpod-volume"
    os.environ["BASE_PATH"]=f"/{BASE_PATH}" 
    os.environ["HF_DATASETS_CACHE"]=f"/{BASE_PATH}/huggingface-cache/datasets" 
    os.environ["HUGGINGFACE_HUB_CACHE"]=f"/{BASE_PATH}/huggingface-cache/hub" 
    os.environ["HF_HOME"]=f"/{BASE_PATH}/huggingface-cache/hub" 
    os.environ["HF_HUB_ENABLE_HF_TRANSFER"]=1 


def before_handler_script():

    logging.info("I will run before the handler")

    # Set the environment variables
    set_LLM_ENV()
    set_BitsAndBytes_ENV()
    # set_LoRA_ENV()



def before_handler_script_dummy():
    logging.info("[before_handler_script_dummy]: I will run before the handler")

