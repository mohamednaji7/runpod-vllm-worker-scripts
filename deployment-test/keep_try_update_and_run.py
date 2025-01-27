import subprocess
import time
import os

import logging
logging.basicConfig(
    level=logging.INFO,       # Set the minimum logging level
    format='[%(levelname)s] %(message)s'  # Text-only format
)
rich_console = logging



def try_update_and_run(scriptname):
    rich_console.info(f"Running `try_update_and_run`...")

    try:
        rich_console.info(f"Running `update` {{git, pull}}...")
        # Perform git pull to update
        res = subprocess.run(['git', 'pull'], check=True)
        rich_console.info(res)

        rich_console.info(f"Running `{scriptname}`...")
        # Run the specified script
        if '.py' in scriptname:
            result = subprocess.run(['python3', scriptname], check=True)
        elif '.sh' in scriptname:
            result = subprocess.run(['bash', scriptname], check=True)
        else:
            raise ValueError(f"Unsupported script type: {scriptname}. Only .py and .sh are allowed.")

        # Log the output
        rich_console.info(result)
    except Exception as e:
        rich_console.error(f"Error occurred: {e}")

def keep_try_update_and_run(scriptname):
    try_update_and_run(scriptname)
    while os.getenv('KEEP_TRY') == 'True' or os.getenv('KEEP_RUN') == 'True':
        rich_console.info(f"KEEP_TRY: {os.getenv('KEEP_TRY')}\nKEEP_RUN: {os.getenv('KEEP_RUN')}")
        seconds = int(os.getenv('RETRY_SECONDS', 30))
        rich_console.info(f"Will try again in {seconds} seconds...")
        time.sleep(seconds)
        try_update_and_run(scriptname)

def main():

    # scriptname = 'activate_UnslothEnv_run_handler_echo.sh'
    scriptname = 'activate_UnslothEnv_run_handler.sh'
    rich_console.info(f"Running `keep_try_update_and_run`...")
    keep_try_update_and_run(scriptname)

if __name__ == "__main__":
    main()
