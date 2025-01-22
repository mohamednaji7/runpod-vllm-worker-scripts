import os
import shutil
import subprocess
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def copy_scripts_to_src_dir():
    SCRIPT_REPO_DIR = "./before_handler_script_repo"
    SCRIPT_SRC_DIR = f"{SCRIPT_REPO_DIR}/src"
    LOCAL_SCRIPT_DIR = f"{os.getcwd()}/"

    # Ensure the local SCRIPT directory exists before copying files
    if not os.path.exists(LOCAL_SCRIPT_DIR):
        os.makedirs(LOCAL_SCRIPT_DIR)

    # Now copy the files
    for item in os.listdir(SCRIPT_SRC_DIR):
        src_path = os.path.join(SCRIPT_SRC_DIR, item)
        dest_path = os.path.join(LOCAL_SCRIPT_DIR, item)
        
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
        else:
            # Ensure the destination directory exists before copying
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            shutil.copy2(src_path, dest_path)
    logging.info("before_handler_script copying completed successfully")

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
    os.environ["MAX_MODEL_LEN"] = 512
    os.environ["QUANTIZATION"] = "bitsandbytes"
    os.environ["TRUST_REMOTE_CODE"] = True
    os.environ["DTYPE"] = "bfloat16"

def set_LoRA_ENV():
    ## LoRA Settings
    os.environ["ENABLE_LORA"] = True
    os.environ["MAX_LORA_RANK"] = 64


def before_handler_script():

    logging.info("I will run before the handler")

    copy_scripts_to_src_dir()

    # Set the environment variables
    set_LLM_ENV()
    set_BitsAndBytes_ENV()
    # set_LoRA_ENV()