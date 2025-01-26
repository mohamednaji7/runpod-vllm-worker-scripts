import subprocess
import time
import sys

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





def try_update_and_run(scriptname):
    rich_console.info(f"Running `try_update_and_run`...")

    try:
        rich_console.info(f"Running `update` {{git, pull}}...")
        # Perform git pull to update
        res = subprocess.run(['git', 'pull'], check=True)
        rich_console.info(res)

        rich_console.info(f"Running `{scriptname}`...")
        # Run the specified script
        result = subprocess.run(['python3', scriptname], check=True)

        # Log the output
        rich_console.info(result)
    except Exception as e:
        rich_console.error(f"Error occurred: {e}")

def keep_try_update_and_run(scriptname):
    try_update_and_run(scriptname)
    while os.getenv('KEEP_TRY') == 'True' or os.getenv('KEEP_RUN') == 'True':
        rich_console.info(f"KEEP_TRY: {os.getenv('KEEP_TRY')}\nKEEP_RUN: {os.getenv('KEEP_RUN')}")
        seconds = int(os.getenv('RETRY_SECONDS', 60))
        rich_console.info(f"Will try again in {seconds} seconds...")
        time.sleep(seconds)
        try_update_and_run(scriptname)

def main():

    from install import install_requirements
    install_requirements(rich_console)
    scriptname = 'openai_server.py'
    rich_console.info(f"Running `keep_try_update_and_run`...")
    keep_try_update_and_run(scriptname)

if __name__ == "__main__":
    main()
