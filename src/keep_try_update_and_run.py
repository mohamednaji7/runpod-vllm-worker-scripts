# Install rich if needed
import os
import subprocess
import time
import sys
import logging
# Setup logging
# Configure logging to output plain text to stdout


# Ensure logs appear in subprocess output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
)

# Flush logs immediately
logging.getLogger().handlers[0].flush = lambda: sys.stdout.flush()

logging.info(f"[keep_try_update_and_run] is here!")

try:
    import rich
except ImportError:
    logging.warning("Rich library not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
import rich
from rich.logging import RichHandler
# Configure logging with Rich
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    stream=sys.stdout,  # Explicitly set output to stdout
    handlers=[RichHandler(
        rich_tracebacks=True,  # Enable rich tracebacks
        tracebacks_show_locals=True,  # Show local variables in traceback
        show_time=True,  # Show timestamp
    )]
)
# Example logging usage
logging.info("This is an info message with Rich formatting")
logging.debug("Debug information looks more colorful")
logging.warning("Warnings stand out")
logging.error("Error messages are highlighted")


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
        seconds = int(os.getenv('RETRY_SECONDS', 60))
        logging.info(f"will try in {seconds} seconds...")
        time.sleep(seconds)
        try_update_and_run(scriptname)

def main():
    scriptname = 'main.py'
    keep_try_update_and_run(scriptname)

if __name__ == "__main__":
    main()
