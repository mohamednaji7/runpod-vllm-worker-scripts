import os
import subprocess
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Function to install rich if not already installed (removed rich dependency)
def install_rich():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])

# Install rich if needed (removed rich dependency)
try:
    import rich
except ImportError:
    logger.warning("Rich library not found, installing...")
    install_rich()
    import rich

# Remove rich import and instead use logging for output
# Initialize the logger for better visual output (using logging instead of rich)
console = logger

def update():
    try:
        # Perform git pull to update
        subprocess.run(['git', 'pull'], check=True)
        logger.info("Git pull successful.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Git pull failed: {e}")
        raise

def run(scriptname):
    try:
        # Run the specified script
        logger.info(f"Running {scriptname}...")
        result = subprocess.run(['python3', scriptname], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Log the output
        logger.info(f"Script {scriptname} executed successfully.")
        logger.info(result.stdout)  # Log standard output from the script
        logger.error(result.stderr)  # Log standard error (if any)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while running {scriptname}: {e}")
        logger.error(f"{e.stderr}")  # Log the error output
        raise

def try_update_and_run(scriptname):
    try:
        update()
        run(scriptname)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        logger.error("Exiting after first failure.")

def keep_try_update_and_run(scriptname):
    try_update_and_run(scriptname)
    while os.getenv('KEEP_TRY') == 'True' or os.getenv('KEEP_RUN') == 'True':   
        logger.info(f"KEEP_TRY: {os.getenv('KEEP_TRY')}\nKEEP_RUN: {os.getenv('KEEP_RUN')}")
        try_update_and_run(scriptname)

def main():
    scriptname = 'main.py'
    keep_try_update_and_run(scriptname)

if __name__ == "__main__":
    main()
