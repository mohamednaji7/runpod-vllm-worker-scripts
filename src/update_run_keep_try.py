import os
import subprocess
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f"[keep_try_update_and_run] is here!")

def update():
    try:
        # Perform git pull to update
        subprocess.run(['git', 'pull'], check=True)
        logging.info("Git pull successful.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Git pull failed: {e}")
        raise

def run(scriptname):
    try:
        # Run the specified script
        logging.info(f"Running {scriptname}...")
        result = subprocess.run(['python3', scriptname], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Log the output
        logging.info(f"Script {scriptname} executed successfully.")
        logging.info(result.stdout)  # Log standard output from the script
        logging.error(result.stderr)  # Log standard error (if any)
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while running {scriptname}: {e}")
        logging.error(f"{e.stderr}")  # Log the error output
        raise

def try_update_and_run(scriptname):
    try:
        update()
        run(scriptname)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        logging.error("Exiting after first failure.")

def keep_try_update_and_run(scriptname):
    try_update_and_run(scriptname)
    while os.getenv('KEEP_TRY') == 'True' or os.getenv('KEEP_RUN') == 'True':   
        logging.info(f"KEEP_TRY: {os.getenv('KEEP_TRY')}\nKEEP_RUN: {os.getenv('KEEP_RUN')}")
        try_update_and_run(scriptname)

def main():
    scriptname = 'main.py'
    keep_try_update_and_run(scriptname)

if __name__ == "__main__":
    main()
