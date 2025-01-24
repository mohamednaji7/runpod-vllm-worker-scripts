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
    # Git Pull
    rich_console.info("Running `update` {git, pull}...")
    res = subprocess.run(['git', 'pull'], check=True)
    rich_console.info(res)

    # Run setup.sh
    rich_console.info("Running setup.sh...")
    subprocess.run(['bash', 'setup.sh'], check=True)

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