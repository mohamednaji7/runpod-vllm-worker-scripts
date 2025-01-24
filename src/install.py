import sys
import subprocess
from pathlib import Path

def install_requirements(rich_console, requirements_file="requirements.txt", verbose=False):
    """
    Installs the Python packages listed in the given requirements file.
    
    Args:
        rich_console (Rich_Console): An instance of Rich_Console for logging.
        requirements_file (str): Path to the requirements.txt file. Default is 'requirements.txt'.
        verbose (bool): If True, enables verbose output during installation.
    """
    req_file_path = Path(requirements_file)

    # Check if the requirements file exists
    if not req_file_path.is_file():
        rich_console.error(f"Error: {requirements_file} does not exist.")
        return

    rich_console.info(f"Starting installation from {requirements_file}...")

    try:
        # Read the contents of the requirements.txt file
        with open(requirements_file, "r") as file:
            packages = file.readlines()

        # Remove any empty lines or comments
        packages = [pkg.strip() for pkg in packages if pkg.strip() and not pkg.startswith("#")]

        total_packages = len(packages)
        rich_console.info(f"Total packages to install: {total_packages}")

        # Run the installation command
        for package in packages:
            rich_console.info(f"Installing package: {package}")
            result = subprocess.run([sys.executable, "-m", "pip", "install", package], text=True, capture_output=not verbose)
            
            if result.returncode == 0:
                rich_console.info(f"Successfully installed: {package}")
            else:
                rich_console.error(f"Error installing: {package}\n{result.stderr if not verbose else ''}")

        rich_console.info("All packages installed successfully!")

    except Exception as e:
        rich_console.error(f"An unexpected error occurred: {e}")