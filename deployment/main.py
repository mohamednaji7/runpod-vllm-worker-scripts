import os
import subprocess
from pathlib import Path
import time 

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

def main():
    # Check the environment variable to see if setup is completed (if it exists, treat it as True, otherwise False)
    setup_completed = os.environ.get('SETUP_COMPLETED', 'False') == 'True'
    marker_file = Path(os.getenv("HOME")) / ".setup_completed"


    if marker_file.exists() or setup_completed:
        rich_console.info("\n\nSetup already completed. Skipping setup.sh.\n\n")

        # Wait for 5 seconds
        rich_console.info("Waiting for 5 seconds...")
        time.sleep(5)
        rich_console.info("Done waiting!")
        
    else:
        rich_console.info("Running setup.sh for the first time...")
        try:
            # Run setup.sh
            rich_console.info("Running `setup.sh`...")

            subprocess.run(['bash', 'setup.sh'], check=True)
            
            # Set the environment variable to indicate successful setup (as True)
            os.environ['SETUP_COMPLETED'] = 'True'
            # Create the marker file on successful setup
            marker_file.touch()
            rich_console.info("\nSetup completed successfully.")
        except subprocess.CalledProcessError as e:
            rich_console.error(f"Error during setup: {e}")
            raise 

    try:
        # Run activate_UnslothEnv_run_handler.sh
        rich_console.info("Running `activate_UnslothEnv_run_handler.sh`...")
        res = subprocess.run(['bash', 'activate_UnslothEnv_run_handler.sh'], check=True)
        rich_console.info("activate_UnslothEnv_run_handler run successfully.")
        rich_console.info(res)

    except subprocess.CalledProcessError as e:
        rich_console.error(f"Error during activate_UnslothEnv_run_handler: {e}")
        raise 

if __name__ == "__main__":
    main()
