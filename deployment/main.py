import os
import subprocess

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

    if setup_completed:
        rich_console.info("Setup already completed. Skipping setup.sh.")
    else:
        rich_console.info("Running setup.sh for the first time...")
        try:
            # Run setup.sh
            rich_console.info("Running `setup.sh`...")

            subprocess.run(['bash', 'setup.sh'], check=True)
            
            # Set the environment variable to indicate successful setup (as True)
            os.environ['SETUP_COMPLETED'] = 'True'
            rich_console.info("Setup completed successfully.")
        except subprocess.CalledProcessError as e:
            rich_console.error(f"Error during setup: {e}")

    try:
        # Run set_env_run_handler.sh
        rich_console.info("Running `set_env_run_handler.sh`...")
        res = subprocess.run(['bash', 'set_env_run_handler.sh'], check=True)
        rich_console.info("set_env_run_handler run successfully.")
        rich_console.info(res)

    except subprocess.CalledProcessError as e:
        rich_console.error(f"Error during setup: {e}")

if __name__ == "__main__":
    main()
