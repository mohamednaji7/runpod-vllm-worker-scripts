from rich_console import Rich_Console
import os
import subprocess
import time
import sys

# Create an instance of Rich_Console
rich_console = Rich_Console()
rich_console.info("Starting the script.")
# sys.exit()

try:
    import rich
except ImportError:
    rich_console.warning("Rich library not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    import rich

# Example usage of rich_console for messages
rich_console.info("Rich library is successfully imported.")

def update():
    try:
        # Perform git pull to update
        subprocess.run(['git', 'pull'], check=True)
        rich_console.info("Git pull successful.")
    except subprocess.CalledProcessError as e:
        rich_console.error(f"Git pull failed: {e}")
        raise

def run(scriptname):
    try:
        # Run the specified script
        rich_console.info(f"Running {scriptname}...")
        # result = subprocess.run(['python3', scriptname], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = subprocess.run(['python3', scriptname], check=True)

        # Log the output
        rich_console.info(f"Script {scriptname} executed successfully.")
        rich_console.info(result.stdout)  # Log standard output from the script
        if result.stderr:
            rich_console.error(result.stderr)  # Log standard error (if any)

    except subprocess.CalledProcessError as e:
        rich_console.error(f"Error occurred while running {scriptname}: {e}")
        rich_console.error(f"{e.stderr}")  # Log the error output
        raise

def try_update_and_run(scriptname):
    try:
        update()
        run(scriptname)
    except Exception as e:
        rich_console.error(f"Error occurred: {e}")
        rich_console.error("Exiting after first failure.")

def keep_try_update_and_run(scriptname):
    try_update_and_run(scriptname)
    while os.getenv('KEEP_TRY') == 'True' or os.getenv('KEEP_RUN') == 'True':
        rich_console.info(f"KEEP_TRY: {os.getenv('KEEP_TRY')}\nKEEP_RUN: {os.getenv('KEEP_RUN')}")
        seconds = int(os.getenv('RETRY_SECONDS', 60))
        rich_console.info(f"Will try again in {seconds} seconds...")
        time.sleep(seconds)
        try_update_and_run(scriptname)

def main():
    scriptname = 'main.py'
    keep_try_update_and_run(scriptname)

if __name__ == "__main__":
    main()
