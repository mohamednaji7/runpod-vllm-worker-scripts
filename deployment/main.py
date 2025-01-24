import os
import subprocess
import sys

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
    # Define the path to the marker file
    marker_file = Path.home() / ".setup_completed"

    if marker_file.exists():
        rich_console("Setup already completed. Skipping setup.sh.")
    else:
        rich_console("Running setup.sh for the first time...")
        try:
            # Run setup.sh
            rich_console.info("Running setup.sh...")

            subprocess.run(['bash', 'setup.sh'], check=True)
            
            # Create the marker file to indicate successful setup
            marker_file.touch()
            rich_console("Setup completed successfully.")
        except subprocess.CalledProcessError as e:
            rich_console(f"Error during setup: {e}")

    # Change conda environment
    rich_console.info("Activating unsloth_env...")
    os.system("conda activate unsloth_env")

    # Run handler.py
    scriptname = 'handler.py'
    rich_console.info(f"Running `{scriptname}`...")
    result = subprocess.run(['python3', scriptname], check=True)

    # Log the output
    rich_console.info(result)

if __name__ == "__main__":
    main()